"""Checks for the late tax-proof power shadow and the Gemini model rotation.
Run: python tests/test_late_gemini.py"""
import sys
import tempfile
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"
bot.CLOSING_PATH = tmp / "closing.csv"
bot.CLOSING_BUDGET_PATH = tmp / "closing_budget.json"
bot.CONFIG["max_closing_credits_per_day"] = 20
START = "2026-11-03T18:00:00Z"
NOW = datetime(2026, 11, 3, 17, 40, tzinfo=timezone.utc)


def book(key, home, away):
    return {"key": key, "markets": [{"key": "h2h", "outcomes": [
        {"name": "Celtics", "price": home}, {"name": "Wizards", "price": away}]}]}


def game(eid, pinnacle, soft, best):
    books = ([book("pinnacle", *pinnacle)] + [book(f"soft{i}", *soft) for i in range(6)]
             + [book("onexbet", *best)])
    return {"id": eid, "sport_key": "basketball_nba", "sport_title": "NBA",
            "home_team": "Celtics", "away_team": "Wizards", "commence_time": START,
            "bookmakers": books}


# --- late_power: heavy favourite at 1.12 vs Pinnacle 1.09 / 9.0 -------------------
fav = game("f1", pinnacle=(1.09, 9.0), soft=(1.08, 7.5), best=(1.12, 7.0))
bets = bot.late_shadow_bets([fav], NOW)
kinds = [s for s, _ in bets]
assert kinds == ["late_power"], kinds  # 1.12 is below the 1.20 floor of late_value
c = bets[0][1]
assert c["odds"] == 1.12 and c["book"] == "onexbet" and c["prob"] == c["sharp_power"]
assert bot.taxed_ev(c["prob"], c["odds"]) > 0
# Proportional chance would not clear the tax: the rule really needs the power chance.
assert bot.taxed_ev(c["sharp"], c["odds"]) < 0
# Started matches are skipped.
assert bot.late_shadow_bets([fav], datetime(2026, 11, 3, 18, 1, tzinfo=timezone.utc)) == []

# Captured through the closing job, once per match, with its own id sequence.
pick = {"event_id": "f1", "sport_key": "basketball_nba", "sport": "Basketball", "league": "NBA",
        "home": "Celtics", "away": "Wizards", "start": START, "market": "h2h",
        "sel": "Celtics", "point": None, "pick": "Celtics to win", "odds": 1.08, "prob": 0.9,
        "consensus": 0.9, "sharp": 0.9, "sharp_book": "pinnacle", "edge": -0.03,
        "verdict": "AGREE", "adj": 0.9}
bot.write_picks([])
bot.write_shadow([])
bot.log_picks(40, "paper", "2026-11-03", {1: pick}, [1])
bot.api_get = lambda path, **params: [fav]
assert bot.capture_closing(NOW) == 1
rows = [r for r in bot.read_shadow() if r["strategy"] == "late_power"]
assert len(rows) == 1 and rows[0]["shadow_id"] == "2026-11-03-late_power-1", rows
assert rows[0]["odds"] == "1.12" and rows[0]["book"] == "onexbet"
assert bot.late_shadow_bets([fav], NOW) == []  # never twice for the same match
assert "late_power" in bot.SHADOW_NAMES
print("late power checks passed")


# --- Gemini rotation: a busy model gives way to the next one quickly ----------------
class Busy(urllib.error.HTTPError):
    def __init__(self, code=503, msg="high demand"):
        super().__init__("u", code, "Service Unavailable", {}, None)
        self._msg = msg

    def read(self):
        return self._msg.encode()


calls = []


def post(url, payload, key):
    model = url.split("/models/")[1].split(":")[0]
    calls.append((model, key))
    if model == "m1":
        raise Busy()
    return {"candidates": [{"content": {"parts": [{"text": "ok from " + model}]}}]}


bot._gemini_post = post
bot.GEMINI_SLEEP = lambda s: None
bot.gemini_keys = lambda: ["k1", "k2", "k3", "k4"]
bot.CONFIG["gemini_plain_models"] = ["m1", "m2"]
bot.MODELS_OUT.clear()
assert bot.gemini("hi") == "ok from m2"
# Old loop: 16 failed calls on m1 first. Now 3 (BUSY_LIMIT), then m2 answers.
assert [m for m, _ in calls].count("m1") == bot.BUSY_LIMIT, calls
assert calls[-1] == ("m2", "k1")

# Every model busy: two rounds, then give up with "" (no endless loop).
calls.clear()
bot._gemini_post = lambda url, payload, key: calls.append(url) or (_ for _ in ()).throw(Busy())
assert bot.gemini("hi") == ""
assert len(calls) == 2 * 2 * bot.BUSY_LIMIT, len(calls)

# A daily quota 429 marks that key out at once and moves to the next key.
calls.clear()
bot.CONFIG["gemini_search_models"] = ["s1"]


def quota(url, payload, key):
    calls.append(key)
    if key == "k1":
        raise Busy(429, "Generate content requests per day limit exceeded on Free Tier")
    return {"candidates": [{"content": {"parts": [{"text": "found"}]}}]}


bot._gemini_post = quota
assert bot.gemini("q", search=True) == "found"
assert calls == ["k1", "k2"] and (1, "s1") in bot.MODELS_OUT
calls.clear()
assert bot.gemini("q", search=True) == "found" and calls == ["k2"]  # k1 skipped later
print("all late power and gemini checks passed")
