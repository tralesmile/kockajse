"""Checks for bet types, settlement and the AI path. Run: python tests/test_markets.py"""
import datetime
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["GEMINI_API_KEY"] = "test"
import bot  # noqa: E402

bot.time.sleep = lambda *_: None


def book(i, markets):
    return {"key": f"b{i}", "markets": markets}


def soccer_event(eid="s1", home="Home FC", away="Away FC", prices=(1.60, 5.5, 4.0)):
    books = []
    for i in range(7):
        k = 1 + 0.005 * i
        books.append(book(i, [
            {"key": "h2h", "outcomes": [{"name": home, "price": prices[0] * k},
                                        {"name": away, "price": prices[1] * k},
                                        {"name": "Draw", "price": prices[2] * k}]},
            {"key": "totals", "outcomes": [{"name": "Over", "price": 1.75, "point": 2.5},
                                           {"name": "Under", "price": 2.05, "point": 2.5}]},
            {"key": "totals", "outcomes": [{"name": "Over", "price": 1.5, "point": 2.25},
                                           {"name": "Under", "price": 2.5, "point": 2.25}]}]))
    return {"id": eid, "sport_key": "soccer_epl", "sport_title": "EPL", "home_team": home,
            "away_team": away, "commence_time": "2026-10-08T17:00:00Z", "bookmakers": books}


def nba_event():
    books = [book(i, [
        {"key": "h2h", "outcomes": [{"name": "Celtics", "price": 1.4},
                                    {"name": "Hornets", "price": 3.0}]},
        {"key": "spreads", "outcomes": [{"name": "Celtics", "price": 1.8, "point": -6.5},
                                        {"name": "Hornets", "price": 2.0, "point": 6.5}]},
        {"key": "totals", "outcomes": [{"name": "Over", "price": 1.83, "point": 221.5},
                                       {"name": "Under", "price": 1.83, "point": 221.5}]}])
        for i in range(7)]
    return {"id": "n1", "sport_key": "basketball_nba", "sport_title": "NBA",
            "home_team": "Celtics", "away_team": "Hornets",
            "commence_time": "2026-10-09T00:00:00Z", "bookmakers": books}


def score(home, away, hs, as_):
    return {"completed": True, "home_team": home, "away_team": away,
            "scores": [{"name": home, "score": str(hs)}, {"name": away, "score": str(as_)}]}


# --- candidates -------------------------------------------------------------
soccer = {c["pick"]: c for c in bot.candidates_from_event(soccer_event())}
assert "Home FC to win" in soccer, soccer.keys()
assert "Over 2.5 goals" in soccer and not any("2.25" in k for k in soccer), soccer.keys()
# A strong favourite's double chance is below the minimum odds, so it is left out.
assert "Home FC or draw (double chance)" not in soccer
even = {c["pick"]: c for c in bot.candidates_from_event(
    soccer_event("s9", "Home FC", "Away FC", (2.3, 3.2, 3.3)))}
dc = even["Home FC or draw (double chance)"]
assert 1.2 <= dc["odds"] <= 1.4 and dc["prob"] > 0.7, dc
assert all(1.2 <= c["odds"] <= 1.85 for c in soccer.values())
nba = {c["pick"]: c for c in bot.candidates_from_event(nba_event())}
assert {"Celtics to win", "Celtics -6.5 (handicap)", "Over 221.5 points",
        "Under 221.5 points"} <= set(nba), nba.keys()

# --- settlement -------------------------------------------------------------
def result(cand, hs, as_):
    return bot.leg_result(dict(cand), score(cand["home"], cand["away"], hs, as_))

assert result(soccer["Home FC to win"], 2, 1) == "won" and result(soccer["Home FC to win"], 1, 1) == "lost"
assert result(dc, 1, 1) == "won" and result(dc, 0, 1) == "lost"
assert result(soccer["Over 2.5 goals"], 2, 1) == "won" and result(soccer["Over 2.5 goals"], 1, 1) == "lost"
assert result(nba["Celtics -6.5 (handicap)"], 110, 103) == "won"
assert result(nba["Celtics -6.5 (handicap)"], 110, 104) == "lost"
assert result(nba["Under 221.5 points"], 110, 104) == "won"
push = dict(nba["Over 221.5 points"], point=214)
assert bot.leg_result(push, score("Celtics", "Hornets", 110, 104)) == "void"
old_leg = {"pick": "Las Vegas Aces"}  # tickets saved before bet types existed
assert bot.leg_result(old_leg, score("Valkyries", "Las Vegas Aces", 70, 80)) == "won"

# --- AI path ----------------------------------------------------------------
cands = (bot.candidates_from_event(soccer_event())
         + bot.candidates_from_event(soccer_event("s2", "Alpha", "Beta", (1.5, 6.5, 4.2)))
         + bot.candidates_from_event(nba_event()))
short = bot.shortlist(cands)
listing = bot.describe(short)
assert listing.count("MATCH:") == 3 and "ID 1:" in listing
ids = {c["pick"] + c["event_id"]: i for i, c in short.items()}
a, b, c3 = ids["Home FC to wins1"], ids["Alpha to wins2"], ids["Celtics to winn1"]
same_match = ids["Over 2.5 goalss1"]
research_calls = []


def fake(answer):
    def g(prompt, search=False, schema=None):
        if search:
            research_calls.append(prompt)
            return "notes"
        return json.dumps(answer)
    return g


picks = [{"id": i, "verdict": "AGREE", "adjusted_chance": cand["prob"] * 100, "summary": "s"}
         for i, cand in short.items()]
now = datetime.datetime.now(bot.TZ)
bot.gemini = fake({"picks": picks, "ticket": [a, b, c3], "ticket_reason": "r"})
ticket, analysis, _ = bot.ai_pick(cands, now)
assert len(research_calls) == 3, len(research_calls)  # one research call per match
assert ticket["picked_by"] == "AI" and 3.0 <= ticket["total_odds"] <= 3.5, ticket
# Two bets on one match must be rejected and rebuilt by the rules.
bot.gemini = fake({"picks": picks, "ticket": [a, same_match, c3], "ticket_reason": "r"})
ticket, _, _ = bot.ai_pick(cands, now)
assert ticket["picked_by"] != "AI" and len({l["event_id"] for l in ticket["legs"]}) == len(ticket["legs"])
assert 3.0 <= ticket["total_odds"] <= 3.5

# --- scout extras -----------------------------------------------------------
fx = [{"id": "s1", "sport_key": "soccer_epl", "sport_title": "EPL", "home_team": "Home FC",
       "away_team": "Away FC", "commence_time": "2026-10-08T17:00:00Z"}]
bot.gemini = lambda *a, **k: ("F1 | Home FC to win | reason\n"
                              "X | Kiel v Minden, Handball DHB Cup, 19:00 | Kiel to win | seen on x\n"
                              "PICKS: F1")
assert bot.ai_scout(fx, now) == ["s1"] and "Kiel v Minden" in bot.SCOUT_EXTRA
rules = bot.build_ticket(cands)
assert rules and 3.0 <= rules["total_odds"] <= 3.5
print("all checks passed;", "AI ticket:", [l["pick"] for l in ticket["legs"]], ticket["total_odds"])
