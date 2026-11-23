"""floor_ticket shadow: 1-2 moneyline favourites, total odds 1.60-2.50, highest joint chance."""
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
            "start": f"2026-11-14T1{i}:00:00Z", "market": market, "sel": "x", "point": None,
            "pick": f"P{i}", "odds": best - 0.01, "prob": power, "power_prob": power,
            "sharp": power, "sharp_power": power, "best_odds": best, "best_book": "bk"}


pool = [cand(1, "e1", "h2h", 1.30, 0.75), cand(2, "e2", "h2h", 1.35, 0.72), cand(3, "e3", "h2h", 1.70, 0.58),
        cand(4, "e4", "dc", 1.25, 0.80), cand(5, "e5", "h2h", 1.65, 0.63)]
t = bot.build_floor_ticket(pool)
# e1*e2 = 1.755 odds, chance .54; e5 alone 1.65 odds, .63 -> single wins on chance; dc excluded, e3 below 62%
assert [l["event_id"] for l in t] == ["e5"], t
assert bot.build_floor_ticket([cand(1, "e1", "h2h", 1.20, 0.80)]) is None  # total below the floor
two = bot.build_floor_ticket([cand(1, "e1", "h2h", 1.30, 0.75), cand(2, "e2", "h2h", 1.35, 0.72)])
assert [l["event_id"] for l in two] == ["e1", "e2"] and two[0]["odds"] == 1.30
assert dict(bot.shadow_tickets(pool)).get("floor_ticket"), "shadow missing"
assert "floor_ticket" in bot.SHADOW_NAMES and "floor_ticket" in bot.SHADOW_LEGS_CLV
print("ok")
