"""Checks for the Odds API credit pacer (odds_budget.py) and the scores-call filter.
Run: python tests/test_odds_budget.py"""
import io
import json
import sys
import tempfile
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import odds_budget as ob  # noqa: E402
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
CFG = {"max_closing_credits_per_day": 20, "late_sweep_credits_per_day": 6,
       "odds_cycle_day": 1, "odds_core_per_day": 45, "odds_reserve_credits": 40}
NOW = datetime(2026, 11, 8, 7, 10, tzinfo=timezone.utc)

# Cycle arithmetic.
assert ob.cycle_end(NOW).isoformat() == "2026-12-01T00:00:00+00:00"
assert ob.cycle_end(datetime(2026, 12, 31, 23, tzinfo=timezone.utc)).year == 2027
assert ob.days_left(NOW) == 23  # 8 Nov (rest of it) .. 30 Nov
assert ob.days_left(datetime(2026, 11, 30, 23, 59, tzinfo=timezone.utc)) == 1


# Free probe: header read, refused key = 0, network trouble = unknown.
class Resp:
    def __init__(self, remaining):
        self.headers = {"x-requests-remaining": remaining}

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def opener_for(table):
    def opener(url, timeout=20):
        key = url.split("apiKey=")[1]
        value = table[key]
        if isinstance(value, Exception):
            raise value
        return Resp(value)
    return opener


refused = urllib.error.HTTPError("u", 401, "no", {}, io.BytesIO(b""))
op = opener_for({"a": "109", "b": "500.0", "c": refused, "d": OSError("down")})
assert ob.probe_key("a", op) == 109
assert ob.probe_key("b", op) == 500
assert ob.probe_key("c", op) == 0
assert ob.probe_key("d", op) is None

# Core use per day from the history: drop minus the extras spent in between.
hist = {"2026-11-05": {"total": 1752, "extras_before": 0},
        "2026-11-06": {"total": 1694, "extras_before": 20},   # core 38
        "2026-11-07": {"total": 1609, "extras_before": 26},   # core 59
        "2026-11-08": {"total": 1540, "extras_before": 21}}   # core 48
assert ob.core_per_day(hist, 45) == 48
assert ob.core_per_day({}, 45) == 45
reset = {"2026-11-30": {"total": 50}, "2026-12-01": {"total": 2000}}
assert ob.core_per_day(reset, 45) == 45  # a reset is not a negative use
gap = {"2026-11-01": {"total": 1900}, "2026-11-04": {"total": 1700}}
assert ob.core_per_day(gap, 45) == 45  # only consecutive days count

# Allowance: plenty of credits -> full caps.
usage = {"measured": NOW.isoformat(), "total": 1900, "core": 45}
assert ob.allowance(CFG, usage, NOW) == (20, 6)
# Tight: 1,540 left, 23 days, core 48: D = (1540 - 40 - 22 x 48) / 23 = 19.3 -> scaled.
usage = {"measured": NOW.isoformat(), "total": 1540, "core": 48}
c, s = ob.allowance(CFG, usage, NOW)
assert (c, s) == (14, 4), (c, s)
assert c + s <= 19.3
# Very tight: nothing for the extras, never negative.
usage = {"measured": NOW.isoformat(), "total": 600, "core": 48}
assert ob.allowance(CFG, usage, NOW) == (0, 0)
# The allowance leaves the core for every remaining day.
for total in (700, 1100, 1540, 1800):
    usage = {"measured": NOW.isoformat(), "total": total, "core": 48}
    c, s = ob.allowance(CFG, usage, NOW)
    n = ob.days_left(NOW)
    assert total - (c + s) - (n - 1) * (48 + c + s) >= 40 - 1e-9 or (c, s) == (0, 0)
# No, stale or future measurement: caps unchanged (old behaviour).
assert ob.allowance(CFG, {}, NOW) == (20, 6)
old = {"measured": (NOW - timedelta(hours=40)).isoformat(), "total": 100, "core": 48}
assert ob.allowance(CFG, old, NOW) == (20, 6)
future = {"measured": (NOW + timedelta(hours=5)).isoformat(), "total": 100, "core": 48}
assert ob.allowance(CFG, future, NOW) == (20, 6)
assert ob.allowance({**CFG, "odds_pacing": False}, {"measured": NOW.isoformat(),
                                                    "total": 100}, NOW) == (20, 6)

# measure(): saves balances, history and allowance; an unreadable key keeps its last value.
path = tmp / "odds_credits.json"
op = opener_for({"a": "94", "b": "500", "c": "500", "d": "500"})
u = ob.measure(CFG, path, NOW - timedelta(days=1), ["a", "b", "c", "d"], 0, op)
assert u["total"] == 1594 and u["keys"] == [94, 500, 500, 500]
op = opener_for({"a": "20", "b": "500", "c": OSError("x"), "d": "500"})
u = ob.measure(CFG, path, NOW, ["a", "b", "c", "d"], 26, op)
assert u["keys"] == [20, 500, None, 500] and u["total"] == 1520, u
assert u["core"] == 48  # 1594 - 1520 - 26
saved = json.loads(path.read_text())
assert saved["closing_allowance"] == u["closing_allowance"]
assert set(saved["history"]) == {"2026-11-07", "2026-11-08"}
line = ob.summary_line(CFG, saved, NOW)
assert "1520" in line and "run out" in line, line
assert "Enough" in ob.summary_line(CFG, {"total": 1900, "core": 30, "keys": [1900],
                                         "measured": NOW.isoformat()}, NOW)
assert ob.summary_line(CFG, {}, NOW) == ""

# A second daily run the same day (re-run after a failed save, 9 Nov) spends ~30 more:
# kept apart as rerun_spent, so the core stays at the normal 48.
op = opener_for({"a": "0", "b": "490", "c": "500", "d": "500"})
u = ob.measure(CFG, path, NOW + timedelta(minutes=30), ["a", "b", "c", "d"], 27, op)
assert u["history"]["2026-11-08"] == {"total": 1490, "extras_before": 27, "rerun_spent": 29}, u
assert u["core"] == 48, u
# Known one-off days can be left out of the estimate by config (falls back to default 45).
hist = {"2026-11-08": {"total": 1571, "extras_before": 15},
        "2026-11-09": {"total": 1490, "extras_before": 3}}
assert ob.core_per_day(hist, 45) == 78
assert ob.core_per_day(hist, 45, ["2026-11-09"]) == 45
when = datetime(2026, 11, 9, 8, 0, tzinfo=timezone.utc)
usage = {"measured": when.isoformat(), "total": 1490, "core": 78, "history": hist}
assert ob.allowance(CFG, usage, when) == (0, 0)
assert ob.allowance({**CFG, "odds_core_skip_days": ["2026-11-09"]}, usage, when) == (17, 5)

# bot.py wiring: closing captures and the sweep obey the pacer's numbers.
bot.ODDS_USAGE_PATH = tmp / "bot_odds.json"
bot.CONFIG.update(CFG)
assert bot.odds_extras_allowance(NOW) == (20, 6)  # no file yet
bot.ODDS_USAGE_PATH.write_text(json.dumps({"measured": NOW.isoformat(), "total": 1540,
                                           "core": 48}))
assert bot.odds_extras_allowance(NOW) == (14, 4)
bot.ODDS_USAGE_PATH.write_text("not json")
assert bot.odds_extras_allowance(NOW) == (20, 6)
bot.CLOSING_BUDGET_PATH = tmp / "budget.json"
bot.CLOSING_BUDGET_PATH.write_text(json.dumps({"2026-11-07": 15,
                                               "sweep": {"date": "2026-11-07", "credits": 4}}))
assert bot.extras_spent() == 19

# Scores calls only for leagues with a started bet inside the feed's 3-day window.
items = [
    {"sport_key": "soccer_epl", "result": "pending", "start": "2026-11-07T15:00:00Z"},
    {"sport_key": "tennis_atp_paris", "result": "pending", "start": "2026-11-03T12:00:00Z"},
    {"sport_key": "basketball_nba", "result": "pending", "start": "2026-11-08T23:00:00Z"},
    {"sport_key": "soccer_italy_serie_a", "result": "won", "start": "2026-11-07T15:00:00Z"},
    {"sport_key": "handball_germany_bundesliga", "result": "pending", "start": ""},
    {"sport_key": "soccer_fa_cup", "result": "pending", "start": "2026-11-05T07:15:00Z"},
]
keys = bot.score_keys(items, NOW)
assert keys == {"soccer_epl", "handball_germany_bundesliga", "soccer_fa_cup"}, keys

print("odds budget: all checks passed")
