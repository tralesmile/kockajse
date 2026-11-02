"""Checks for the closing watcher: early fallback and near-start captures, shadow CLV and
late value bets. Run: python tests/test_closing.py"""
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
bot.CONFIG["max_closing_credits_per_day"] = 20
START = "2026-11-03T18:00:00Z"
T0 = datetime(2026, 11, 3, 18, 0, tzinfo=timezone.utc)


def at(minutes_before):
    return T0 - timedelta(minutes=minutes_before)


def book(key, home_price, away_price):
    return {"key": key, "markets": [{"key": "h2h", "outcomes": [
        {"name": "Celtics", "price": home_price}, {"name": "Hornets", "price": away_price}]}]}


def game(eid, soft_best=None, pinnacle=(1.60, 2.50)):
    books = [book("pinnacle", *pinnacle)] + [book(f"soft{i}", 1.52, 2.45) for i in range(5)]
    if soft_best:
        books.append(book("onexbet", *soft_best))
    return {"id": eid, "sport_key": "basketball_nba", "sport_title": "NBA",
            "home_team": "Celtics", "away_team": "Hornets", "commence_time": START,
            "bookmakers": books}


pick = {"event_id": "g1", "sport_key": "basketball_nba", "sport": "Basketball", "league": "NBA",
        "home": "Celtics", "away": "Hornets", "start": START, "market": "h2h", "sel": "Celtics",
        "point": None, "pick": "Celtics to win", "odds": 1.52, "prob": 0.6, "consensus": 0.6,
        "sharp": 0.6, "sharp_book": "pinnacle", "edge": -0.09, "verdict": "AGREE", "adj": 0.6}
bot.write_picks([])
bot.log_picks(30, "paper", "2026-11-03", {1: pick}, [1])
# A morning value single on the same match, at onexbet's 1.70.
value = dict(pick, odds=1.70, book="onexbet", prob=0.6)
bot.write_shadow(bot.shadow_rows("2026-11-03", [("value_single", [value])]))

calls = []
feed = {"events": [game("g1")]}
bot.api_get = lambda path, **params: calls.append(params) or feed["events"]

# Nothing is due 4 hours out; the wait is until 15 minutes before the start.
assert bot.capture_closing(at(240)) == 0 and not calls
assert bot.closing_next_wait(at(240)) == (240 - 15) * 60

# 2 hours out: the early fallback capture (pick and value single, one request).
assert bot.capture_closing(at(120)) == 2 and len(calls) == 1
rows = bot.read_closing()
assert {r["source"] for r in rows} == {"pick", "value_single"}
assert all(r["minutes_before"] == "120" for r in rows)
# Still to capture near the start, but not again early.
assert bot.capture_closing(at(90)) == 0 and len(calls) == 1
assert bot.closing_next_wait(at(90)) == (90 - 15) * 60

# 15 minutes out: the near-start capture. The value single's CLV uses its own 1.70.
assert bot.capture_closing(at(15)) == 2 and len(calls) == 2
near = [r for r in bot.read_closing() if r["minutes_before"] == "15"]
vs = next(r for r in near if r["source"] == "value_single")
fair = (1 / 1.60) / (1 / 1.60 + 1 / 2.50)
assert abs(float(vs["clv"]) - (1.70 * fair - 1)) < 1e-3, vs
assert vs["open_sharp"] and vs["move"] != ""
assert bot.closing_next_wait(at(15)) is None  # all done
assert bot.capture_closing(at(10)) == 0 and len(calls) == 2

# The email table counts each bet once (its latest capture) and has a value-singles row.
html = bot.clv_html()
assert "Value singles (best price)" in html and "<td>On the ticket</td><td>1</td>" in html, html

# --- late value ------------------------------------------------------------------
# A second match where onexbet still pays 1.70 on Celtics while Pinnacle says 1.60: value.
bot.write_picks([])
later = dict(pick, event_id="g2", start="2026-11-03T21:00:00Z")
bot.log_picks(31, "paper", "2026-11-03", {1: later}, [1])
feed["events"] = [dict(game("g2", soft_best=(1.70, 2.30)), commence_time=later["start"])]
assert bot.capture_closing(datetime(2026, 11, 3, 20, 40, tzinfo=timezone.utc)) == 1
late = [r for r in bot.read_shadow() if r["strategy"] == "late_value"]
assert len(late) == 1 and late[0]["book"] == "onexbet" and late[0]["odds"] == "1.7", late
assert late[0]["shadow_id"].endswith("late_value-1") and float(late[0]["edge"]) > 0.02
# Never twice for the same match.
assert bot.late_value_bets(feed["events"], datetime(2026, 11, 3, 20, 45, tzinfo=timezone.utc)) == []
# A forced re-run of the morning job keeps late bets.
bot.log_shadow("2026-11-03", [])
assert [r["strategy"] for r in bot.read_shadow()] == ["late_value"]
assert "Late value" in bot.SHADOW_NAMES["late_value"]

# Old closing rows without a source column still count as picks.
bot.write_picks([])
bot.log_picks(32, "paper", "2026-11-03", {1: dict(pick, event_id="g3")}, [1])
import csv
with bot.CLOSING_PATH.open("a", newline="") as fh:
    old = {f: "" for f in bot.CLOSING_FIELDS if f != "source"}
    old.update(event_id="g3", market="h2h", sel="Celtics", minutes_before="20", clv="-0.03",
               move="0.01", on_ticket="yes")
    csv.DictWriter(fh, bot.CLOSING_FIELDS, restval="").writerow(old)
assert bot.closing_todo(at(30)) == []
print("all closing checks passed")
