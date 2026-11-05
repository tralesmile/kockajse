"""Checks for the fallback results source. Run: python tests/test_fallback.py"""
import csv
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.PICKS_PATH = tmp / "picks.csv"
bot.LEDGER_PATH = tmp / "ledger.csv"
bot.FALLBACK_PATH = tmp / "fallback_scores.csv"
bot.shadow_path = lambda: tmp / "shadow.csv"
NOW = datetime(2026, 11, 5, 7, 0, tzinfo=timezone.utc)
bot.gemini_keys = lambda: ["k"]


def leg(eid, key, home, away, sel, start, market="h2h", point=None, odds=1.3):
    return {"event_id": eid, "sport_key": key, "home": home, "away": away, "start": start,
            "market": market, "sel": sel, "point": point, "pick": f"{sel} to win",
            "odds": odds, "result": "pending"}


def reset(feed):
    bot.SCORES.clear()
    bot.FETCHED_KEYS.clear()
    bot.SCORES.update(feed)
    bot.FETCHED_KEYS.update({"tennis_atp_paris_masters", "soccer_spain_copa_del_rey",
                             "soccer_uefa_champs_league"})


def answer(*items):
    return "Here you go:\n```json\n" + json.dumps(list(items)) + "\n```"


T1 = leg("t1", "tennis_atp_paris_masters", "Tommy Paul", "Daniel Merida Aguilar", "Tommy Paul",
         "2026-11-04T11:30:00Z")
T2 = leg("t2", "tennis_atp_paris_masters", "Tomas Martin Etcheverry", "Alex de Minaur",
         "Alex de Minaur", "2026-11-04T12:40:00Z")
F1 = leg("f1", "soccer_uefa_champs_league", "AEK Athens", "Real Madrid", "Over",
         "2026-11-04T17:45:00Z", "totals", 3.5, 1.73)
FRESH = leg("f2", "soccer_spain_copa_del_rey", "A", "B", "A", "2026-11-05T05:00:00Z")


def state():
    return {"bankroll": 0, "paper_profit": 0, "open_tickets": [
        {"no": 27, "date": "2026-11-04", "created": "2026-11-04T07:05:28Z", "stake": 100,
         "total_odds": 2.55, "paper": True,
         "legs": [dict(T1), dict(T2), dict(F1, result="won"), dict(FRESH)]}]}


# --- only overdue, uncovered events are asked about -----------------------
reset({})
todo = bot.overdue_events(state(), NOW)
assert set(todo) == {"t1", "t2"}, todo  # f1 settled, f2 started only 2 hours ago
reset({"t1": {"id": "t1", "completed": True, "scores": []}})
assert set(bot.overdue_events(state(), NOW)) == {"t2"}
# tennis non-winner markets cannot be settled from sets
st = state()
st["open_tickets"][0]["legs"][0]["market"] = "spreads"
reset({})
assert set(bot.overdue_events(st, NOW)) == {"t2"}

# --- parser ------------------------------------------------------------------
got = bot._parse_fallback(answer(
    {"id": "t1", "status": "final", "home_score": 2, "away_score": 0, "source": "atptour.com"},
    {"id": "t2", "status": "unknown", "home_score": None, "away_score": None},
    {"id": "x", "status": "final", "home_score": "a", "away_score": 1}))
assert got == {"t1": (2.0, 0.0, False, "atptour.com")}, got
assert bot._parse_fallback("no json here") == {}
assert bot._parse_fallback("[{broken") == {}
assert bot._plausible("tennis_x", 2, 1) and not bot._plausible("tennis_x", 6, 4)
assert not bot._plausible("tennis_x", 1, 1) and bot._plausible("soccer_x", 1, 1)
assert not bot._plausible("basketball_x", 3, 1) and bot._plausible("basketball_x", 71, 69)

# --- two agreeing answers settle the ticket; disagreement leaves it pending ---
calls = []


def fake(replies):
    def g(prompt, search=False, schema=None):
        assert search
        calls.append(prompt)
        return replies[len(calls) - 1]
    return g


good = answer({"id": "t1", "status": "final", "home_score": 2, "away_score": 1, "source": "a"},
              {"id": "t2", "status": "final", "home_score": 0, "away_score": 2, "source": "b"})
other = answer({"id": "t1", "status": "final", "home_score": 2, "away_score": 1, "source": "c"},
               {"id": "t2", "status": "final", "home_score": 2, "away_score": 0, "source": "d"})
reset({})
bot.gemini = fake([good, other])
st = state()
used = bot.fill_missing_scores(st, NOW)
assert set(used) == {"t1"} and len(calls) == 2, (used, calls)
assert "Tommy Paul v Daniel Merida Aguilar" in calls[0] and "| Tennis |" in calls[0]
rows = list(csv.DictReader(bot.FALLBACK_PATH.open()))
assert [(r["event_id"], r["used"]) for r in rows] == [("t1", "yes"), ("t2", "no")], rows
# settle() then uses the fallback score; t2 is still pending, so the ticket stays open
bot.fetch_scores = lambda keys: bot.SCORES
done = bot.settle(st, NOW)
legs = st["open_tickets"][0]["legs"]
assert not done and legs[0]["result"] == "won" and legs[0]["score"] == "2:1"
assert legs[1]["result"] == "pending"

# both agree on t2 now: de Minaur won in straight sets
calls.clear()
bot.gemini = fake([good, good])
bot.SCORES.pop("t1")
used = bot.fill_missing_scores(st, NOW)
assert set(used) == {"t2"}, used  # t1 is no longer pending
bot.settle(st, NOW)
assert st["open_tickets"][0]["legs"][1]["result"] == "won"

# no answer: one call only, nothing used, nothing written
calls.clear()
bot.FALLBACK_PATH.unlink()
reset({})
bot.gemini = fake(["", ""])
assert bot.fill_missing_scores(state(), NOW) == {} and len(calls) == 1
assert not bot.FALLBACK_PATH.exists()

# switched off: no calls
calls.clear()
bot.CONFIG["fallback_scores"] = False
assert bot.fill_missing_scores(state(), NOW) == {} and not calls
bot.CONFIG["fallback_scores"] = True

# picks.csv and shadow rows are covered too
reset({})
with bot.PICKS_PATH.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=bot.PICK_FIELDS)
    w.writeheader()
    w.writerow({**{k: "" for k in bot.PICK_FIELDS}, "event_id": "c1",
                "sport_key": "soccer_spain_copa_del_rey", "match": "CD Pamplona v SD Eibar",
                "start": "2026-11-03T18:00:00Z", "market": "totals", "sel": "Under",
                "point": "2.5", "pick": "Under 2.5 goals", "result": "pending"})
todo = bot.overdue_events({"open_tickets": []}, NOW)
assert todo == {"c1": ("soccer_spain_copa_del_rey", "CD Pamplona", "SD Eibar",
                       "2026-11-03T18:00:00Z")}, todo
print("fallback tests passed")
