"""AI-as-veto shadow ticket. Run: python tests/test_veto_ticket.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"


def cand(i, odds, prob, verdict, best=None):
    return {"event_id": f"e{i}", "sport_key": "basketball_nba", "match": f"A{i} v B{i}",
            "start": f"2026-11-12T0{i}:00:00Z", "market": "h2h", "sel": "x", "point": None,
            "pick": f"P{i}", "odds": odds, "prob": prob, "power_prob": prob, "sharp_power": prob,
            "best_odds": best or odds, "best_book": "onexbet" if best else "", "verdict": verdict}


short = {1: cand(1, 1.60, 0.62, "AVOID"), 2: cand(2, 1.45, 0.68, "RISKY", 1.5),
         3: cand(3, 1.40, 0.70, "RISKY"), 4: cand(4, 1.50, 0.65, "AGREE")}
pool = list(short.values())
tickets = dict(bot.shadow_tickets(pool, short=short))
assert "veto_ticket" in tickets and "veto_ticket_best" in tickets, tickets.keys()
for name in ("veto_ticket", "veto_ticket_best"):
    assert all(l["verdict"] != "AVOID" for l in tickets[name]), name
    assert name in bot.SHADOW_NAMES
# two RISKY legs are allowed here (no cap), unlike the real ticket rule
assert len(tickets["veto_ticket"]) >= 1
# everything vetoed -> no veto ticket
only = {1: short[1]}
assert "veto_ticket" not in dict(bot.shadow_tickets([short[1]], short=only))
print("ok")
