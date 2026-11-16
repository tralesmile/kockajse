"""banker shadows: the most likely single of the day and the two most likely on different matches."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"


def cand(i, ev, market, best, power):
    return {"event_id": ev, "sport_key": "soccer_epl", "match": f"A{i} v B{i}", "home": "A", "away": "B",
            "start": "2026-11-14T10:00:00Z", "market": market, "sel": "x", "point": None,
            "pick": f"P{i}", "odds": best - 0.01, "prob": power, "power_prob": power,
            "sharp": power, "sharp_power": power, "best_odds": best, "best_book": "bk"}


pool = [cand(1, "e1", "h2h", 1.20, 0.82), cand(2, "e1", "dc", 1.04, 0.93), cand(3, "e2", "h2h", 1.30, 0.75),
        cand(4, "e3", "h2h", 2.0, 0.50), cand(5, "e4", "dc", 1.02, 0.97)]
t = dict(bot.shadow_tickets(pool))
assert [l["event_id"] for l in t["banker"]] == ["e1"] and t["banker"][0]["pick"] == "P2", t["banker"]
assert [l["event_id"] for l in t["banker_double"]] == ["e1", "e2"], t["banker_double"]
assert "banker" in bot.SHADOW_NAMES and "banker_double" in bot.SHADOW_CLV
only_weak = dict(bot.shadow_tickets([cand(4, "e3", "h2h", 2.0, 0.50)]))
assert "banker" not in only_weak
print("ok")
