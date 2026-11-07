"""Checks for the kick-off sweep (late tax-proof singles in other leagues' busiest slots).
Run: python tests/test_sweep.py"""
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"
bot.CLOSING_PATH = tmp / "closing.csv"
bot.CLOSING_BUDGET_PATH = tmp / "closing_budget.json"
bot.ODDS_USAGE_PATH = tmp / "odds_credits.json"  # never the real balance file
bot.CONFIG.update(late_sweep_credits_per_day=2, late_sweep_slot_minutes=60,
                  late_sweep_min_events=2, closing_lead_minutes=15,
                  max_closing_credits_per_day=20)
bot.write_picks([])
bot.write_shadow([])


def fx(eid, key, start):
    return {"id": eid, "sport_key": key, "commence_time": start}


S15 = "2026-11-07T15:00:00Z"
fixtures = ([fx(f"a{i}", "soccer_efl_champ", S15) for i in range(5)]
            + [fx("a9", "soccer_efl_champ", "2026-11-07T19:45:00Z")]
            + [fx(f"b{i}", "soccer_england_league1", S15) for i in range(3)]
            + [fx(f"c{i}", "soccer_epl", "2026-11-07T15:30:00Z") for i in range(4)]
            + [fx("d1", "tennis_atp_x", "2026-11-07T12:00:00Z")])

# --- planning ----------------------------------------------------------------------
plan = bot.plan_sweep(fixtures, "2026-11-07")
ids = [s["id"] for s in plan["slots"]]
# Two credits: the two busiest slots (5 and 4 matches), one per league; single-match
# slots (tennis, the 19:45 game) never qualify.
assert ids == ["soccer_efl_champ@2026-11-07T15:00:00Z", "soccer_epl@2026-11-07T15:30:00Z"], ids
assert plan["slots"][0]["events"] == 5
# A league the watcher already fetches near that time is left out.
watched = {"soccer_efl_champ": [datetime(2026, 11, 7, 15, 0, tzinfo=timezone.utc)]}
ids = [s["id"] for s in bot.plan_sweep(fixtures, "2026-11-07", watched)["slots"]]
assert "soccer_efl_champ@2026-11-07T15:00:00Z" not in ids and len(ids) == 2, ids
# Switched off: no slots.
bot.CONFIG["late_sweep_credits_per_day"] = 0
assert bot.plan_sweep(fixtures, "2026-11-07")["slots"] == []
assert bot.sweep_todo(datetime(2026, 11, 7, 14, 0, tzinfo=timezone.utc)) == []
bot.CONFIG["late_sweep_credits_per_day"] = 2
bot.sweep_plan_path().write_text(json.dumps(plan))


# --- the watcher waits for the slot and then sweeps it ------------------------------
def book(key, home, away):
    return {"key": key, "markets": [{"key": "h2h", "outcomes": [
        {"name": "Leeds", "price": home}, {"name": "Luton", "price": away}]}]}


def game(eid, pinnacle, soft, best):
    books = ([book("pinnacle", *pinnacle)] + [book(f"soft{i}", *soft) for i in range(6)]
             + [book("onexbet", *best)])
    return {"id": eid, "sport_key": "soccer_efl_champ", "sport_title": "Championship",
            "home_team": "Leeds", "away_team": "Luton", "commence_time": S15,
            "bookmakers": books}


fav = game("a1", pinnacle=(1.09, 9.0), soft=(1.08, 7.5), best=(1.12, 7.0))
plain = game("a2", pinnacle=(1.60, 2.40), soft=(1.55, 2.35), best=(1.58, 2.38))

early = datetime(2026, 11, 7, 14, 0, tzinfo=timezone.utc)
assert bot.closing_next_wait(early) == 45 * 60  # 15:00 start minus the 15-minute lead
calls = []


def fake_get(path, **params):
    calls.append((path, params))
    return [fav, plain]


bot.api_get = fake_get
assert bot.run_sweep(early) == 0 and calls == []  # not due yet: no request

now = datetime(2026, 11, 7, 14, 47, tzinfo=timezone.utc)
assert bot.capture_closing(now) == 0  # no logged pick, but the sweep runs first
assert len(calls) == 1 and calls[0][0] == "/sports/soccer_efl_champ/odds"
assert calls[0][1]["markets"] == "h2h"  # one credit
rows = [r for r in bot.read_shadow() if r["strategy"] == "late_sweep"]
assert len(rows) == 1 and rows[0]["event_id"] == "a1", rows
assert rows[0]["shadow_id"] == "2026-11-07-late_sweep-1" and rows[0]["odds"] == "1.12"
assert bot.taxed_ev(float(rows[0]["fair_chance"]), 1.12) > 0
budget = json.loads(bot.CLOSING_BUDGET_PATH.read_text())
assert budget["sweep"]["credits"] == 1 and len(budget["sweep"]["done"]) == 1
# The slot is done: the next wait is the 15:30 slot, and no second fetch.
assert bot.closing_next_wait(now) == 28 * 60
assert bot.run_sweep(now) == 0 and len(calls) == 1
# The chain keeps a watcher alive for the planned slot even with no logged bet.
bot.CONFIG["closing_chain"] = True
bot.ACTIONS_USAGE_PATH = tmp / "usage.json"
bot.ACTIONS_USAGE_PATH.write_text(json.dumps({"private": False}))
assert bot.closing_chain_ok(now)

# Second slot: a match already taken by the sweep is never logged twice; the credit
# limit holds afterwards.
later = datetime(2026, 11, 7, 15, 20, tzinfo=timezone.utc)
fav2 = dict(fav, sport_key="soccer_epl", commence_time="2026-11-07T15:30:00Z")
bot.api_get = lambda path, **params: (calls.append(path), [fav2])[1]
assert bot.run_sweep(later) == 0 and len(calls) == 2
budget = json.loads(bot.CLOSING_BUDGET_PATH.read_text())
assert budget["sweep"]["credits"] == 2
assert bot.sweep_todo(later) == [] and bot.closing_next_wait(later) is None

# The scoreboard treats it as a late strategy (its own price is the close).
import scoreboard  # noqa: E402
scored = [b for b in scoreboard.score_bets(bot.read_shadow(), [], 0.15)
          if b["strategy"] == "late_sweep"]
assert len(scored) == 1 and scored[0]["xroi"] is not None and scored[0]["xroi"] > 0, scored
assert "late_sweep" in bot.SHADOW_NAMES

# A forced re-run of the daily job keeps the sweep's bets (log_shadow keeps late_ rows).
bot.log_shadow("2026-11-07", [])
assert any(r["strategy"] == "late_sweep" for r in bot.read_shadow())
print("sweep checks passed")
