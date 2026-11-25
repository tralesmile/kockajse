"""fav_agree shadow: fav_wide legs where sharp >= consensus. Run: python tests/test_fav_agree.py"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"


def cand(i, sharp, cons, power=0.70, best=1.55):
    return {"event_id": f"e{i}", "sport_key": "basketball_nba", "match": f"A{i} v B{i}",
            "start": f"2026-11-19T0{i}:00:00Z", "market": "h2h", "sel": "x", "point": None,
            "pick": f"P{i}", "odds": best - 0.02, "prob": cons, "consensus": cons, "power_prob": power,
            "sharp": sharp, "sharp_power": power, "best_odds": best, "best_book": "onexbet"}


pool = [cand(1, 0.70, 0.68), cand(2, 0.66, 0.70), cand(3, None, 0.70), cand(4, 0.70, 0.70)]
ag = sorted(l[0]["event_id"] for n, l in bot.shadow_tickets(pool) if n == "fav_agree")
wide = sorted(l[0]["event_id"] for n, l in bot.shadow_tickets(pool) if n == "fav_wide")
assert ag == ["e1", "e4"], ag
assert "e2" in wide and "e2" not in ag
assert "fav_agree" in bot.SHADOW_NAMES and "fav_agree" in bot.SHADOW_CLV and "fav_agree" in bot.SHARP_SHADOWS
print("ok")
