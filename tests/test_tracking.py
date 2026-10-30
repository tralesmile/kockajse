"""Checks for the pick log, scorecard, paper mode and ledger. Run: python tests/test_tracking.py"""
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
bot.STATE_PATH = tmp / "state.json"

# --- ledger written before paper mode had no "mode" column ------------------
bot.LEDGER_PATH.write_text("ticket_no,date,picks,total_odds,stake,result,payout,tax,net_profit,"
                           "bankroll_after\n1,2026-10-08,x,3.38,100,won,338.0,35.7,202.3,602.3\n")
assert bot.ledger_summary("real")["profit"] == 202.3 and bot.ledger_summary("paper")["tickets"] == 0
leg = {"home": "A", "away": "B", "pick": "A to win", "odds": 1.5, "result": "lost"}
bot.append_ledger({"no": 2, "date": "2026-10-09", "legs": [leg], "total_odds": 1.5, "stake": 100,
                   "result": "lost", "payout": 0, "tax": 0, "net_profit": -100,
                   "bankroll_after": -100, "paper": True})
assert bot.ledger_summary("paper")["profit"] == -100 and bot.ledger_summary("real")["tickets"] == 1
assert bot.LEDGER_PATH.read_text().splitlines()[0].endswith(",mode")

# --- paper settlement leaves the real bankroll alone ------------------------
def score(home, away, hs, as_):
    return {"id": "e1", "completed": True, "home_team": home, "away_team": away,
            "scores": [{"name": home, "score": str(hs)}, {"name": away, "score": str(as_)}]}

bot.fetch_scores = lambda keys: {"e1": score("Home", "Away", 2, 0)}
now = datetime(2026, 10, 31, 7, 0, tzinfo=timezone.utc)
paper_leg = {"event_id": "e1", "sport_key": "soccer_epl", "home": "Home", "away": "Away",
             "pick": "Home to win", "market": "h2h", "sel": "Home", "point": None,
             "odds": 2.0, "result": "pending"}
state = {"bankroll": 75.89, "paper_profit": 0, "open_tickets": [
    {"no": 23, "date": "2026-10-31", "created": "2026-10-31T06:00:00Z", "stake": 100,
     "total_odds": 2.0, "legs": [dict(paper_leg)], "paper": True},
    {"no": 22, "date": "2026-10-30", "created": "2026-10-30T06:00:00Z", "stake": 50,
     "total_odds": 2.0, "legs": [dict(paper_leg)]}]}
done = bot.settle(state, now)
assert len(done) == 2
# Real ticket: 50 at 2.0 = 100 payout, tax 7.50, 92.50 back into the real bankroll.
assert state["bankroll"] == round(75.89 + 92.5, 2), state["bankroll"]
assert state["paper_profit"] == 85.0, state["paper_profit"]  # 100 at 2.0: 200 - 15 tax - 100

# --- pick log, settlement and scorecard ------------------------------------
cands = {}
for i in range(12):
    cands[i + 1] = {"event_id": "e1", "sport_key": "soccer_epl", "sport": "Football",
                    "league": "EPL", "home": "Home", "away": "Away",
                    "start": "2026-10-30T18:00:00Z", "market": "h2h",
                    "sel": "Home" if i % 2 == 0 else "Away", "point": None,
                    "pick": "x", "odds": 1.6, "prob": 0.6,
                    "verdict": "AGREE" if i % 2 == 0 else "AVOID", "adj": 0.62}
bot.log_picks(23, "paper", "2026-10-30", cands, [1, 3])
rows = bot.read_picks()
assert len(rows) == 12 and rows[0]["on_ticket"] == "yes" and rows[1]["on_ticket"] == "no"
bot.settle_picks(now)
rows = bot.read_picks()
assert {r["result"] for r in rows if r["verdict"] == "AGREE"} == {"won"}
assert {r["result"] for r in rows if r["verdict"] == "AVOID"} == {"lost"}
card = bot.scorecard_html()
assert "Verdict AGREE" in card and "+40" in card and "Verdict AVOID" in card, card

# Rule-picked legs are logged as on the ticket with verdict RULES.
bot.log_picks(24, "paper", "2026-10-31", {}, [], rules_legs=[dict(paper_leg, prob=0.5,
              sport="Football", league="EPL", start="2026-10-31T18:00:00Z")])
assert bot.read_picks()[-1]["verdict"] == "RULES"

# --- lessons reach the prompts ----------------------------------------------
assert bot.lessons()
print("all tracking checks passed")
