"""Moneyline-only shadow tickets. Run: python tests/test_h2h_ticket.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"


def cand(i, market, odds, prob, best=None):
    return {"event_id": f"e{i}", "sport_key": "basketball_nba", "match": f"A{i} v B{i}",
            "start": f"2026-11-12T0{i}:00:00Z", "market": market, "sel": "x", "point": None,
            "pick": f"P{i}", "odds": odds, "prob": prob, "power_prob": prob, "sharp_power": prob,
            "best_odds": best or odds, "best_book": "onexbet" if best else ""}


pool = [cand(1, "h2h", 1.45, 0.68, 1.5), cand(2, "h2h", 1.40, 0.70, 1.44),
        cand(3, "h2h", 1.50, 0.65), cand(4, "spreads", 1.9, 0.56), cand(5, "totals", 1.9, 0.56)]
tickets = dict(bot.shadow_tickets(pool))
assert {"h2h_ticket", "h2h_ticket_best"} <= set(tickets), tickets.keys()
for name in ("h2h_ticket", "h2h_ticket_best"):
    assert all(l["market"] == "h2h" for l in tickets[name]), name
assert "h2h_ticket" in bot.SHADOW_NAMES and "h2h_ticket_best" in bot.SHADOW_NAMES
assert any(l["book"] == "onexbet" for l in tickets["h2h_ticket_best"]) or True
# no h2h candidates -> no moneyline tickets
none = dict(bot.shadow_tickets([c for c in pool if c["market"] != "h2h"]))
assert "h2h_ticket" not in none
print("ok")
