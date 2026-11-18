"""fav_wide shadow: moneyline favourites to 2.00, chance 60%+, taxed EV above -2%. Run: python tests/test_fav_wide.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"


def cand(i, market, best, power):
    return {"event_id": f"e{i}", "sport_key": "basketball_nba", "match": f"A{i} v B{i}",
            "start": f"2026-11-19T0{i}:00:00Z", "market": market, "sel": "x", "point": None,
            "pick": f"P{i}", "odds": best - 0.02, "prob": power, "power_prob": power,
            "sharp": power, "sharp_power": power, "best_odds": best, "best_book": "onexbet"}


# odds 1.60: taxed EV = p*0.6*0.85 - (1-p) > -0.02  <=>  p > 0.6405 ; odds 1.90: p > 0.5987 (but chance floor 0.60)
pool = [cand(1, "h2h", 1.60, 0.66),   # in
        cand(2, "h2h", 1.60, 0.62),   # taxed EV too low
        cand(3, "h2h", 2.40, 0.50),   # odds above 2.00
        cand(4, "totals", 1.60, 0.70),  # not moneyline
        cand(5, "h2h", 1.90, 0.605),  # in: EV -0.0178 and chance >= 0.60
        cand(6, "h2h", 1.95, 0.58)]   # chance below the 0.60 floor
got = [l for n, l in bot.shadow_tickets(pool) if n == "fav_wide"]
ids = sorted(l[0]["event_id"] for l in got)
assert ids == ["e1", "e5"], ids
assert all(l[0]["market"] == "h2h" and l[0]["odds"] <= 2.0 and l[0]["book"] == "onexbet" for l in got)
assert "fav_wide" in bot.SHADOW_NAMES and "fav_wide" in bot.SHADOW_CLV and "fav_wide" in bot.SHARP_SHADOWS
print("ok")
