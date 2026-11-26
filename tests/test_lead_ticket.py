"""Lead-book chance, the lead_ticket shadows, their closing captures and the price-move audit.
Run: python tests/test_lead_ticket.py"""
import gzip
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import audit  # noqa: E402
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"

SOFT = ["unibet_se", "williamhill", "sport888", "betsson", "coolbet", "nordicbet"]


def event(i, pin, lead=None, soft=(1.45, 2.80)):
    def book(key, prices):
        return {"key": key, "markets": [{"key": "h2h", "outcomes": [
            {"name": f"H{i}", "price": prices[0]}, {"name": f"A{i}", "price": prices[1]}]}]}
    books = [book("pinnacle", pin)] + [book(k, soft) for k in SOFT]
    books += [book(k, v) for k, v in (lead or {}).items()]
    return {"id": f"e{i}", "sport_key": "basketball_nba", "sport_title": "NBA", "home_team": f"H{i}",
            "away_team": f"A{i}", "commence_time": "2026-11-30T20:00:00Z", "bookmakers": books}


def home(ev):
    return next(c for c in bot.candidates_from_event(ev) if c["market"] == "h2h" and c["sel"].startswith("H"))


# lead_prob moves Pinnacle's power chance LEAD_WEIGHT of the way to the lead books' average
c = home(event(1, (1.45, 2.90), {"betonlineag": (1.40, 3.10), "matchbook": (1.40, 3.15)}))
pb = bot.power_devig([1.40, 3.10])[0]
pm = bot.power_devig([1.40, 3.15])[0]
gap = (pb + pm) / 2 - c["sharp_power"]
assert gap > 0 and abs(c["lead_gap"] - gap) < 1e-9
assert abs(c["lead_prob"] - (c["sharp_power"] + bot.LEAD_WEIGHT * gap)) < 1e-9
# no lead book: unchanged
c = home(event(2, (1.45, 2.90)))
assert c["lead_gap"] is None and c["lead_prob"] == c["power_prob"]
# a lead price far from Pinnacle is treated as stale
c = home(event(3, (1.45, 2.90), {"betonlineag": (2.20, 1.70)}))
assert c["lead_gap"] is None and c["lead_prob"] == c["power_prob"]
# without Pinnacle there is no lead adjustment
ev = event(4, (1.45, 2.90), {"betonlineag": (1.40, 3.10)})
ev["bookmakers"] = ev["bookmakers"][1:]
assert home(ev)["lead_gap"] is None

# the twin uses the same pool and rule but the lead chance: two matches the lead books rate
# lower and two they rate higher, otherwise identical
down = {"betonlineag": (1.68, 2.25), "betfair_ex_eu": (1.68, 2.25)}
up = {"betonlineag": (1.56, 2.52), "betfair_ex_eu": (1.56, 2.52)}
events = [event(i, (1.62, 2.38), up, soft=(1.60, 2.30)) for i in (1, 2)]
events += [event(i, (1.61, 2.40), down, soft=(1.60, 2.30)) for i in (3, 4)]
cands = [x for e in events for x in bot.candidates_from_event(e)]
tickets = dict(bot.shadow_tickets(cands))
assert {"h2h_ticket", "lead_ticket", "lead_ticket_best"} <= set(tickets), tickets.keys()
assert {l["event_id"] for l in tickets["lead_ticket"]} == {"e1", "e2"}, tickets["lead_ticket"]
assert {l["event_id"] for l in tickets["h2h_ticket"]} != {"e1", "e2"}
# the recorded fair chance stays Pinnacle's, so the move to the close tests the choice
assert all(l["sharp"] == l["sharp_power"] for l in tickets["lead_ticket"])
assert {"lead_ticket", "lead_ticket_best"} <= set(bot.SHADOW_NAMES)

# closing prices of the moneyline-ticket legs are requested (they were not before 26 Nov)
for name in ("h2h_ticket", "h2h_ticket_best", "lead_ticket", "lead_ticket_best"):
    assert name in bot.SHADOW_LEGS_CLV, name
    bot.write_shadow(bot.shadow_rows("2026-11-30", [(name, tickets["lead_ticket"])]))
    todo = bot.closing_todo(datetime(2026, 11, 30, 8, tzinfo=timezone.utc), captures={})
    assert [t[0] for t in todo] == [name, name], todo

# price-move audit: the close moves half of the lead gap in this made-up archive
odds = tmp / "odds"
odds.mkdir()
snap, closing = [], []
for i in range(40):
    o = 1.30 + (i % 8) * 0.07
    lead_o = o + ((i % 5) - 2) * 0.02
    pin = bot.power_devig([o, 3.0])[0]
    gap = bot.power_devig([lead_o, 3.0])[0] - pin
    snap.append({"id": f"m{i}", "sport_key": "x", "home": "H", "away": "A", "start": "",
                 "books": {"pinnacle": {"h2h": [["H", None, o], ["A", None, 3.0]]},
                           "betonlineag": {"h2h": [["H", None, lead_o], ["A", None, 3.0]]}}})
    closing.append({"event_id": f"m{i}", "market": "h2h", "sel": "H", "point": "", "source": "pick",
                    "close_power": str(pin + 0.5 * gap), "close_book": "pinnacle", "minutes_before": "30",
                    "close_sharp": "0.62", "open_sharp": "0.60"})
with gzip.open(odds / "2026-11-28.json.gz", "wt") as fh:
    json.dump({"events": snap}, fh)
picks = [{"event_id": f"m{i}", "market": "h2h", "sel": "H", "point": "", "ai_chance": "0.65",
          "sharp_chance": str(0.60 + (i % 3) * 0.01)} for i in range(40)]
shadow = [{"strategy": "h2h_ticket", "date": "2026-11-28", "event_id": f"m{i}", "market": "h2h",
           "sel": "H"} for i in range(10)]
res = audit.price_move_signals(odds, picks, closing, shadow, bot.power_devig)
assert abs(res["lead"][0] - 0.5) < 1e-6 and res["lead"][2] == 40, res["lead"]
assert abs(res["fresh"][0] - 0.5) < 1e-6 and res["fresh_n"] == 40
assert abs(res["ai"][0]) < 1e-6
assert res["drift"][0][0] == "h2h_ticket" and res["drift"][0][1] == 10
assert "out of sample, 40 so far" in "\n".join(audit.price_move_markdown(res))
# nothing to measure: no error, dashes in the table
empty = audit.price_move_signals(tmp / "none", [], [], [], bot.power_devig)
assert empty["lead"] is None and empty["fresh_n"] == 0
assert "| - | - | - |" in "\n".join(audit.price_move_markdown(empty))
print("ok")
