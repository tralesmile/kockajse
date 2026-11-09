"""Checks for the late ticket shadows (the tax-aware ticket rule run on near-kick-off prices).
Run: python tests/test_late_ticket.py"""
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
bot.ODDS_USAGE_PATH = tmp / "odds_credits.json"
bot.CONFIG.update(late_ticket_window_minutes=90, late_ticket_min_events=3,
                  late_sweep_credits_per_day=0, max_closing_credits_per_day=20)
bot.write_picks([])
bot.write_shadow([])

NOW = datetime(2026, 11, 14, 14, 40, tzinfo=timezone.utc)


def book(key, home, draw, away):
    return {"key": key, "markets": [{"key": "h2h", "outcomes": [
        {"name": "Home", "price": home}, {"name": "Draw", "price": draw},
        {"name": "Away", "price": away}]}]}


def game(eid, start, pin, soft, best=None):
    books = [book("pinnacle", *pin)] + [book(f"soft{i}", *soft) for i in range(6)]
    if best:
        books.append(book("onexbet", *best))
    return {"id": eid, "sport_key": "soccer_epl", "sport_title": "EPL", "home_team": "Home",
            "away_team": "Away", "commence_time": start, "bookmakers": books}


S15 = "2026-11-14T15:00:00Z"
events = [game("g1", S15, (1.40, 4.8, 8.5), (1.38, 4.6, 7.5), (1.45, 4.6, 7.5)),
          game("g2", S15, (1.65, 3.9, 5.4), (1.62, 3.8, 5.0), (1.70, 3.8, 5.0)),
          game("g3", S15, (1.85, 3.6, 4.3), (1.80, 3.5, 4.1)),
          game("g4", S15, (1.50, 4.2, 6.6), (1.48, 4.1, 6.2)),
          game("late", "2026-11-14T19:00:00Z", (1.30, 5.0, 11), (1.28, 5.0, 10)),
          game("gone", "2026-11-14T14:00:00Z", (1.30, 5.0, 11), (1.28, 5.0, 10))]

# --- building ----------------------------------------------------------------------
tickets = dict(bot.late_ticket_bets(events, NOW, shadow=[]))
assert set(tickets) == {"late_ticket", "late_ticket_best"}, tickets
for strategy, legs in tickets.items():
    total = 1.0
    for leg in legs:
        total *= leg["odds"]
        # only matches inside the 90-minute window that have not started
        assert leg["event_id"] in {"g1", "g2", "g3", "g4"}, leg["event_id"]
        assert leg["sharp"] is not None
    assert 2.5 <= round(total, 2) <= 3.5, (strategy, total)
    assert len({l["event_id"] for l in legs}) == len(legs)
assert all(l["book"] == "average" for l in tickets["late_ticket"])
# the best-price twin uses the best listed price where one beats the average
best_books = {l["book"] for l in tickets["late_ticket_best"]}
assert best_books - {"average"}, best_books

# too few matches in the window: nothing
assert bot.late_ticket_bets(events[:2] + events[4:], NOW, shadow=[]) == []
# switched off
bot.CONFIG["late_ticket_window_minutes"] = 0
assert bot.late_ticket_bets(events, NOW, shadow=[]) == []
bot.CONFIG["late_ticket_window_minutes"] = 90

# --- logging: once a day per strategy ------------------------------------------------
assert bot.log_late_tickets(events, NOW) == 2
rows = bot.read_shadow()
ids = {r["shadow_id"] for r in rows}
assert ids == {"2026-11-14-late_ticket-1", "2026-11-14-late_ticket_best-1"}, ids
assert all(r["result"] == "pending" for r in rows)
assert bot.log_late_tickets(events, NOW + timedelta(minutes=5)) == 0
assert len(bot.read_shadow()) == len(rows)
# a failure inside never raises (the watcher must keep running)
assert bot.log_late_tickets([{"broken": True}], NOW + timedelta(days=1)) == 0

# --- the closing pass feeds its fetched leagues to the late ticket -------------------
bot.write_shadow([])
bot.write_picks([{"date": "2026-11-14", "ticket_no": "", "mode": "paper", "event_id": "g1",
                  "sport_key": "soccer_epl", "sport": "Football", "league": "EPL",
                  "match": "Home v Away", "start": S15, "market": "h2h", "sel": "Home",
                  "point": "", "pick": "Home to win", "odds": 1.38, "market_chance": 0.7,
                  "verdict": "AGREE", "ai_chance": 0.7, "on_ticket": "no",
                  "result": "pending", "score": ""}])
calls = []


def fake_get(path, **params):
    calls.append(path)
    return events


bot.api_get = fake_get
bot.odds_extras_allowance = lambda now=None: (20, 0)
bot.capture_closing(NOW)
assert calls == ["/sports/soccer_epl/odds"], calls
strategies = {r["strategy"] for r in bot.read_shadow()}
assert {"late_ticket", "late_ticket_best"} <= strategies, strategies

# --- the scoreboard treats them as late bets (logged price is the close) -------------
import scoreboard  # noqa: E402
scored = [b for b in scoreboard.score_bets(bot.read_shadow(), [], 0.15)
          if b["strategy"] in bot.LATE_TICKETS]
assert len(scored) == 2 and all(b["xroi"] is not None for b in scored), scored
assert "late_ticket" in bot.SHADOW_NAMES and "late_ticket_best" in bot.SHADOW_NAMES

print("late ticket tests passed")
