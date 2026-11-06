"""Checks for the GitHub Actions minutes guard (actions_budget.py).
Run: python tests/test_actions_budget.py"""
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import actions_budget as ab  # noqa: E402

CFG = {"actions_included_minutes": 2000, "actions_budget_share": 0.85,
       "actions_daily_reserve_minutes": 45, "actions_closing_max_per_day": 120,
       "actions_cycle_day": 1}
NOW = datetime(2026, 11, 6, 12, 0, tzinfo=timezone.utc)
tmp = Path(tempfile.mkdtemp())


def run(name, start, minutes, conclusion="success", status="completed", path=None):
    s = datetime.fromisoformat(start.replace("Z", "+00:00"))
    e = s.timestamp() + minutes * 60
    return {"name": name, "path": path or f".github/workflows/{name}.yml", "status": status,
            "conclusion": conclusion, "run_started_at": start,
            "updated_at": datetime.fromtimestamp(e, timezone.utc).isoformat()}


# Cycle dates.
assert ab.cycle_start(NOW).isoformat() == "2026-11-01T00:00:00+00:00"
assert ab.cycle_start(NOW, 10).isoformat() == "2026-10-10T00:00:00+00:00"
assert ab.cycle_end(ab.cycle_start(datetime(2026, 12, 5, tzinfo=timezone.utc))).month == 1

# Billed minutes: rounded up; blocked runs (a few seconds, failure) cost nothing.
assert ab.run_minutes(run("daily", "2026-11-06T07:00:00Z", 14.2)) == 15
assert ab.run_minutes(run("daily", "2026-11-06T07:00:00Z", 0.05, "failure")) == 0
assert ab.run_minutes(run("daily", "2026-11-06T07:00:00Z", 0.3)) == 1
assert ab.run_minutes(run("x", "2026-11-06T07:00:00Z", 3, None, "in_progress")) == 3

runs = [run("daily", "2026-11-06T07:00:00Z", 14.5),
        run("closing", "2026-11-06T08:00:00Z", 36),
        run("closing", "2026-11-05T08:00:00Z", 36),
        run("closing", "2026-11-06T16:00:00Z", 0.05, "failure")]
total, today, per = ab.summarise(runs, NOW)
assert (total, today) == (15 + 36 + 36, 36), (total, today)

# measure() saves usage; on API failure it keeps the last saved numbers, marked stale.
path = tmp / "usage.json"
u = ab.measure(CFG, path, NOW, repo="o/r", token="t", fetcher=lambda *a: (True, runs))
assert u["private"] and u["minutes"] == 87 and json.loads(path.read_text())["closing_today"] == 36


def broken(*a):
    raise OSError("network down")


u2 = ab.measure(CFG, path, NOW, repo="o/r", token="t", fetcher=broken)
assert u2["minutes"] == 87 and "stale" in u2
assert ab.measure(CFG, tmp / "none.json", NOW, repo="", token="") == {"stale": "no GitHub repository or token"}

# Allowance: public repository has no limit.
assert ab.closing_allowance(CFG, {"private": False, "minutes": 5000}, NOW) is None
# Nothing measured, or a measurement from an earlier cycle: no extra minutes.
assert ab.closing_allowance(CFG, {}, NOW) == 0
assert ab.closing_allowance(CFG, {"private": True, "minutes": 10, "cycle_start": "2026-10-01"}, NOW) == 0
# Early in the month with little used: 1700 - 100 - 45 x 25 days = 475 spare / 25 = 19 a day.
u = {"private": True, "minutes": 100, "cycle_start": "2026-11-01", "day": "2026-11-06",
     "closing_today": 0}
assert ab.closing_allowance(CFG, u, NOW) == 19, ab.closing_allowance(CFG, u, NOW)
u["closing_today"] = 15
assert ab.closing_allowance(CFG, u, NOW) == 4
u["day"] = "2026-11-05"  # yesterday's watcher minutes do not count against today
assert ab.closing_allowance(CFG, u, NOW) == 19
# The 6 Nov situation (2,100 used): nothing for the watcher, the daily run is never blocked.
u = {"private": True, "minutes": 2100, "cycle_start": "2026-11-01", "day": "2026-11-06"}
assert ab.closing_allowance(CFG, u, NOW) == 0
# A fresh month: 1700 - 45 x 31 = 305 / 31 = 9 a day, so no 36-minute links in private.
dec = datetime(2026, 12, 1, 0, 30, tzinfo=timezone.utc)
assert ab.closing_allowance(CFG, {"private": True, "minutes": 0, "cycle_start": "2026-12-01"}, dec) == 9

# Email line.
assert "public" in ab.summary_line(CFG, {"private": False, "minutes": 10})
line = ab.summary_line(CFG, {"private": True, "minutes": 1600})
assert "80%" in line and "Warning" in line
assert "Warning" not in ab.summary_line(CFG, {"private": True, "minutes": 300})
assert ab.summary_line(CFG, {}) == ""

# bot.closing_plan follows the allowance.
import bot  # noqa: E402
bot.ACTIONS_USAGE_PATH = tmp / "bot_usage.json"
bot.CONFIG.update(CFG, closing_run_minutes=36, closing_chain=True)
bot.ACTIONS_USAGE_PATH.write_text(json.dumps({"private": False}))
assert bot.closing_plan(NOW, measure=False) == (100000, 36 * 60)
bot.ACTIONS_USAGE_PATH.write_text(json.dumps(
    {"private": True, "minutes": 100, "cycle_start": "2026-11-01", "day": "2026-11-06"}))
assert bot.closing_plan(NOW, measure=False) == (18 * 60, 18 * 60)
bot.ACTIONS_USAGE_PATH.write_text(json.dumps(
    {"private": True, "minutes": 2100, "cycle_start": "2026-11-01"}))
assert bot.closing_plan(NOW, measure=False) == (0, 0)
# After a long stop of the runs, old ticket legs are still looked up (pick rows are not).
bot.PICKS_PATH = tmp / "picks.csv"
bot.STATE_PATH = tmp / "state.json"  # shadow.csv lives next to it
bot.write_picks([])
bot.write_shadow([])
bot.SCORES.clear()
leg = {"event_id": "old1", "sport_key": "basketball_euroleague", "home": "A", "away": "B",
       "start": "2026-11-06T19:00:00Z", "market": "h2h", "result": "pending"}
state = {"open_tickets": [{"legs": [leg]}]}
assert "old1" in bot.overdue_events(state, datetime(2026, 12, 1, 7, 0, tzinfo=timezone.utc))
assert "old1" not in bot.overdue_events(state, datetime(2026, 12, 20, 7, 0, tzinfo=timezone.utc))
print("test_actions_budget: all checks passed")
