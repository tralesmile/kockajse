"""Checks for the self-continuing closing watcher (closing_chain_ok and the workflows).
Run: python tests/test_chain.py"""
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"
bot.CLOSING_PATH = tmp / "closing.csv"
bot.CLOSING_BUDGET_PATH = tmp / "closing_budget.json"
bot.ODDS_USAGE_PATH = tmp / "odds_credits.json"  # never the real balance file
# Public repository: the minutes guard sets no limit (tests/test_actions_budget.py covers
# the private case).
bot.ACTIONS_USAGE_PATH = tmp / "actions_usage.json"
bot.ACTIONS_USAGE_PATH.write_text(json.dumps({"private": False, "minutes": 100}))
bot.CONFIG.update(closing_chain=True, closing_chain_max_runs=60, closing_chain_idle_hours=14,
                  max_closing_credits_per_day=20)
START = "2026-11-04T20:00:00Z"
T0 = datetime(2026, 11, 4, 20, 0, tzinfo=timezone.utc)


def at(minutes_before):
    return T0 - timedelta(minutes=minutes_before)


pick = {"event_id": "g1", "sport_key": "soccer_epl", "sport": "Football", "league": "EPL",
        "home": "A", "away": "B", "start": START, "market": "h2h", "sel": "A",
        "point": None, "pick": "A to win", "odds": 1.52, "prob": 0.6, "consensus": 0.6,
        "sharp": 0.6, "sharp_book": "pinnacle", "edge": -0.09, "verdict": "AGREE", "adj": 0.6}
bot.write_picks([])
bot.write_shadow([])

# Nothing logged: no chain.
assert not bot.closing_chain_ok(at(300))

bot.log_picks(1, "paper", "2026-11-04", {1: pick}, [1])
# 13 hours to go (morning ticket for an evening match): keep watching.
assert bot.closing_chain_ok(at(13 * 60))
# More than closing_chain_idle_hours away: let the next daily run start it.
assert not bot.closing_chain_ok(at(20 * 60))
# Runaway guard.
assert not bot.closing_chain_ok(at(120), chain=60)
assert bot.closing_chain_ok(at(120), chain=59)
# Credits used up for the day: stop.
bot.CLOSING_BUDGET_PATH.write_text(json.dumps({"2026-11-04": 20}))
assert not bot.closing_chain_ok(at(120))
bot.CLOSING_BUDGET_PATH.write_text(json.dumps({"2026-11-04": 19}))
assert bot.closing_chain_ok(at(120))
# Switched off in config.
bot.CONFIG["closing_chain"] = False
assert not bot.closing_chain_ok(at(120))
bot.CONFIG["closing_chain"] = True
# The match has started: nothing left, chain ends.
assert not bot.closing_chain_ok(at(-5))

# A near-start capture closes the bet, so the chain ends after it.
bot.api_get = lambda path, **params: []
assert bot.capture_closing(at(30), window_minutes=60) == 1
assert not bot.closing_chain_ok(at(29))

# Private repository with the free minutes nearly used up: no chain.
bot.write_picks([])
bot.log_picks(1, "paper", "2026-11-04", {1: dict(pick, event_id="g2")}, [1])
bot.CLOSING_BUDGET_PATH.write_text("{}")
assert bot.closing_chain_ok(at(120))
bot.ACTIONS_USAGE_PATH.write_text(json.dumps({"private": True, "minutes": 1900,
                                              "cycle_start": "2026-11-01"}))
assert not bot.closing_chain_ok(at(120))
assert bot.closing_plan(at(120), measure=False) == (0, 0)

# Workflows: the closing job can start itself, the daily job starts it, and both may.
closing = yaml.safe_load((ROOT / ".github/workflows/closing.yml").read_text())
daily = yaml.safe_load((ROOT / ".github/workflows/daily.yml").read_text())
for wf in (closing, daily):
    assert wf["permissions"].get("actions") == "write"
on = closing.get("on") or closing.get(True)
assert "chain" in on["workflow_dispatch"]["inputs"]
script = closing["jobs"]["capture"]["steps"][-1]["run"]
assert "--closing-chain" in script and "gh workflow run closing.yml" in script
steps = daily["jobs"]["run"]["steps"]
assert "gh workflow run closing.yml" in steps[-1]["run"]
assert "inputs.preview" in steps[-1]["if"]
assert "steps.bot.outputs.made" in steps[-1]["if"]
run_minutes = json.loads((ROOT / "config.json").read_text())["closing_run_minutes"]
assert closing["jobs"]["capture"]["timeout-minutes"] >= run_minutes + 10
print("test_chain: all checks passed")
