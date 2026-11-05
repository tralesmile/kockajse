"""Checks for the closing-price scoreboard (scoreboard.py) and the extra closing captures
it relies on. Run: python tests/test_scoreboard.py"""
import random
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402
import scoreboard as sb  # noqa: E402

TAX = 0.15


def shadow(sid, strategy, eid, odds, fair="0.5", result="pending", date="2026-11-05",
           market="h2h", sel="A", point=""):
    return {"date": date, "strategy": strategy, "shadow_id": sid, "event_id": eid,
            "sport_key": "soccer_epl", "match": "A v B", "start": "2026-11-05T20:00:00Z",
            "market": market, "sel": sel, "point": point, "pick": sel, "odds": str(odds),
            "book": "x", "fair_chance": fair, "edge": "0", "result": result, "score": ""}


def close(eid, minutes, sharp="", power="", cons="0.5", source="pick", market="h2h", sel="A",
          point=""):
    return {"event_id": eid, "market": market, "sel": sel, "point": point,
            "minutes_before": str(minutes), "close_odds": "1.9", "close_sharp": sharp,
            "close_power": power, "close_consensus": cons, "source": source}


# closing_fair: nearest capture wins; power preferred over proportional; consensus last.
fair = sb.closing_fair([close("e1", 120, sharp="0.40"), close("e1", 30, sharp="0.50"),
                        close("e2", 30, sharp="0.60", power="0.62"), close("e3", 40, cons="0.45"),
                        dict(close("e4", 30), close_odds="")])
assert fair["e1" and ("e1", "h2h", "A", "")] == (0.50, 30)
assert fair[("e2", "h2h", "A", "")] == (0.62, 30)
assert fair[("e3", "h2h", "A", "")] == (0.45, 40)
assert ("e4", "h2h", "A", "") not in fair  # no closing price found: not a capture
# Points are matched whatever their spelling (2.5 vs 2.50).
fair = sb.closing_fair([close("e5", 20, sharp="0.55", market="totals", sel="Over", point="2.50")])
assert ("e5", "totals", "Over", "2.5") in fair

# score_bets: xROI = P_close * (1 + 0.85 (O - 1)) - 1, tickets multiply.
rows = [shadow("s1", "single", "e1", 2.0), shadow("t1", "actual", "e1", 2.0),
        shadow("t1", "actual", "e2", 1.5), shadow("u1", "actual", "e9", 1.8),
        shadow("v1", "market", "e1", 2.0, result="void"),
        shadow("l1", "late_power", "e7", 1.2, fair="0.9", result="won")]
caps = [close("e1", 30, sharp="0.55"), close("e2", 30, sharp="0.70"),
        close("e9", 150, sharp="0.6")]  # e9 only captured early: not a closing price
bets = {b["shadow_id"]: b for b in sb.score_bets(rows, caps, TAX)}
assert abs(bets["s1"]["xroi"] - (0.55 * 1.85 - 1)) < 1e-9
assert abs(bets["t1"]["xroi"] - (0.55 * 0.70 * (1 + 0.85 * 2.0) - 1)) < 1e-9
assert bets["u1"]["xroi"] is None  # not scored without a near-start capture
assert "v1" not in bets  # all legs void: stake returned, nothing to score
assert abs(bets["l1"]["xroi"] - (0.9 * (1 + 0.85 * 0.2) - 1)) < 1e-9  # late: own price is the close
assert abs(bets["l1"]["real"] - 0.85 * 0.2) < 1e-9 and bets["s1"]["real"] is None
lost = sb.score_bets([shadow("a", "actual", "e1", 2.0, result="won"),
                      shadow("a", "actual", "e2", 1.5, result="lost")], caps, TAX)
assert lost[0]["real"] == -1.0

# A void leg drops out of a ticket (odds and chance), as the settlement does.
part = sb.score_bets([shadow("p", "actual", "e1", 2.0), shadow("p", "actual", "e2", 1.5,
                                                               result="void")], caps, TAX)
assert abs(part[0]["xroi"] - (0.55 * 1.85 - 1)) < 1e-9 and part[0]["odds"] == 2.0

# mSPRT: always-valid p stays large on zero-mean noise and gets small on a clear edge.
random.seed(7)
false_alarms = 0
for _ in range(200):
    xs = [random.gauss(0, 0.3) for _ in range(150)]
    false_alarms += sb.msprt(xs) < 0.05
assert false_alarms <= 200 * 0.05 * 1.6, false_alarms  # at most about alpha, read every bet
assert sb.msprt([random.gauss(0.05, 0.03) for _ in range(60)]) < 0.01
assert sb.msprt([0.01]) == 1.0  # one value: no test
# p-values never rise as bets are added (they are running minima).
xs = [random.gauss(0.02, 0.1) for _ in range(80)]
ps = [sb.msprt(xs[:n]) for n in range(1, 81)]
assert all(b <= a for a, b in zip(ps, ps[1:]))

# strategy_stats: verdict only after MIN_BETS and p < alpha; paired difference by day.
bets = []
for d in range(30):
    date = f"2026-11-{d + 1:02d}"
    bets.append({"shadow_id": f"a{d}", "date": date, "strategy": "actual", "odds": 3.0,
                 "xroi": -0.15 + random.gauss(0, 0.01), "real": None})
    bets.append({"shadow_id": f"g{d}", "date": date, "strategy": "good", "odds": 1.3,
                 "xroi": 0.03 + random.gauss(0, 0.01), "real": 0.25 if d % 2 else -1.0})
stats = sb.strategy_stats(bets)
assert stats["actual"]["verdict"] == "loses after tax"
assert stats["good"]["verdict"] == "beats the tax" and stats["good"]["p_pos"] > 0.99
md, se, days = stats["good"]["paired"]
assert days == 30 and 0.16 < md < 0.20 and se < 0.01
assert stats["good"]["settled"] == 30 and abs(stats["good"]["real"] - (-0.375)) < 1e-9
few = sb.strategy_stats(bets[:10])
assert few["good"]["verdict"] == "undecided"  # 5 bets: too few for a verdict

# Picks become singles per verdict, scored at their own (average) price.
picks = [{"date": "2026-11-05", "event_id": "e1", "market": "h2h", "sel": "A", "point": "",
          "odds": "1.80", "verdict": "AGREE", "market_chance": "0.52", "result": "won"}]
pb = sb.score_bets(sb.pick_bets(picks), caps, TAX)
assert pb[0]["strategy"] == "pick:AGREE" and abs(pb[0]["xroi"] - (0.55 * 1.68 - 1)) < 1e-9

# write(): files in, markdown and html out.
tmp = Path(tempfile.mkdtemp())
import csv  # noqa: E402
for name, data in (("shadow.csv", rows), ("closing.csv", caps), ("picks.csv", picks)):
    with (tmp / name).open("w", newline="") as fh:
        w = csv.DictWriter(fh, list(data[0]))
        w.writeheader()
        w.writerows(data)
stats, md, page = sb.write(tmp, TAX, bot.SHADOW_NAMES)
assert (tmp / "scoreboard.md").read_text() == md and "| The real paper ticket |" in md
assert "Scoreboard at closing prices" in page and "Picks the AI rated AGREE" in page
assert sb.html({"x": {"scored": 0}}, {}) == ""

# bot: closing captures now include ticket-shadow legs not in the pick log, once each, and
# record the power-method closing chance; late_power records its power chance.
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks2.csv"
bot.CLOSING_PATH = tmp / "closing2.csv"
bot.CLOSING_BUDGET_PATH = tmp / "budget.json"
(tmp / "shadow.csv").unlink()
START = "2026-11-05T20:00:00Z"
now = datetime(2026, 11, 5, 19, 30, tzinfo=timezone.utc)
base = {"event_id": "g1", "sport_key": "basketball_nba", "sport": "Basketball", "league": "NBA",
        "home": "Celtics", "away": "Hornets", "start": START, "market": "h2h", "sel": "Celtics",
        "point": None, "pick": "Celtics to win", "odds": 1.52, "prob": 0.6, "consensus": 0.6,
        "sharp": 0.6, "sharp_book": "pinnacle", "edge": -0.09}
bot.write_picks([])
bot.log_picks(30, "paper", "2026-11-05", {1: base}, [1])
other = dict(base, sel="Hornets", pick="Hornets to win", odds=2.4, prob=0.4, sharp=0.4)
bot.write_shadow(bot.shadow_rows("2026-11-05", [("market", [base, other]),
                                                ("power_ticket", [other])]))
todo = bot.closing_todo(now)
assert [(s, r["sel"]) for s, r, _ in todo] == [("pick", "Celtics"), ("market", "Hornets")]


def book(key, h, a):
    return {"key": key, "markets": [{"key": "h2h", "outcomes": [
        {"name": "Celtics", "price": h}, {"name": "Hornets", "price": a}]}]}


event = {"id": "g1", "sport_key": "basketball_nba", "sport_title": "NBA", "home_team": "Celtics",
         "away_team": "Hornets", "commence_time": START,
         "bookmakers": [book("pinnacle", 1.30, 3.80)] + [book(f"s{i}", 1.25, 3.5) for i in range(6)]}
bot.api_get = lambda path, **params: [event]
assert bot.capture_closing(now) == 2
caps = bot.read_closing()
assert all(r["close_power"] for r in caps)
fav = [r for r in caps if r["sel"] == "Celtics"][0]
assert float(fav["close_power"]) > float(fav["close_sharp"])  # power gives favourites more
late = [c for s, c in bot.late_shadow_bets([event], now) if s == "late_power"]
for c in late:
    assert c["sharp"] == c["sharp_power"]
print("scoreboard tests passed")
