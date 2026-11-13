"""fav_flat shadow: favourite moneyline singles to 1.30, taxed EV above -2%. Run: python tests/test_fav_flat.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"


def cand(i, market, best, power, odds=None):
    return {"event_id": f"e{i}", "sport_key": "basketball_nba", "match": f"A{i} v B{i}",
            "start": f"2026-11-14T0{i}:00:00Z", "market": market, "sel": "x", "point": None,
            "pick": f"P{i}", "odds": odds or best - 0.02, "prob": power, "power_prob": power,
            "sharp": power, "sharp_power": power, "best_odds": best, "best_book": "onexbet"}


# taxed EV at 1.25 with p=0.79: 0.79*0.25*0.85 - 0.21 = -0.042 (too low); p=0.81 -> -0.0185 (in)
pool = [cand(1, "h2h", 1.25, 0.81), cand(2, "h2h", 1.25, 0.79), cand(3, "h2h", 1.40, 0.75),
        cand(4, "totals", 1.25, 0.82), cand(5, "h2h", 1.20, 0.90)]
got = [l for n, l in bot.shadow_tickets(pool) if n == "fav_flat"]
ids = sorted(l[0]["event_id"] for l in got)
assert ids == ["e1", "e5"], ids
assert all(l[0]["market"] == "h2h" and l[0]["odds"] <= 1.30 and l[0]["book"] == "onexbet" for l in got)
assert "fav_flat" in bot.SHADOW_NAMES and "fav_flat" in bot.SHADOW_CLV
# the older rule is unchanged: strictly positive taxed EV, any odds up to 4.0
old = bot.taxed_value_bets(pool, "sharp_power")
assert sorted(c["event_id"] for c in old) == ["e3", "e5"], old
print("ok")
