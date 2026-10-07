"""Offline simulation: runs the bot for several days against a fake odds feed.

Usage: python tests/simulate.py
Writes each day's email to out/day-N.html and leaves the real data untouched.
"""
import json
import shutil
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.LEDGER_PATH = tmp / "ledger.csv"
bot.STATE_PATH.write_text(json.dumps({"bankroll": 400, "next_ticket_no": 1, "open_tickets": [],
                                      "last_run_date": None, "stopped": False}))
bot.LEDGER_PATH.write_text("ticket_no,date,picks,total_odds,stake,result,payout,tax,"
                           "net_profit,bankroll_after\n")
bot.time.sleep = lambda *_: None

clock = {"now": None, "day": 0}
# Day -> winners. Day 0 ticket wins, day 1 loses, day 2 has a postponed game.
OUTCOMES = {0: "fav", 1: "dog", 2: "postponed", 3: "dog", 4: "dog", 5: "dog"}


def games(day):
    base = clock["now"].replace(hour=17, minute=0, second=0, microsecond=0)
    base = base - timedelta(days=clock["day"] - day)
    return [
        ("soccer_epl", "EPL", f"s{day}", "Arsenal", "Fulham", base, (1.45, 6.8, 4.4)),
        ("soccer_epl", "EPL", f"t{day}", "Everton", "Leeds", base, (2.5, 2.9, 3.2)),
        ("basketball_nba", "NBA", f"b{day}", "Celtics", "Hornets", base + timedelta(hours=8), (1.5, 2.6)),
        ("tennis_atp_china_open", "ATP China Open", f"x{day}", "Sinner", "Paul", base, (1.3, 3.5)),
        ("handball_germany_bundesliga", "HBL", f"h{day}", "Kiel", "Erlangen", base, (1.4, 8.0, 3.6)),
    ]


def fake_api(path, **params):
    bot.credits_left = 480 - clock["day"] * 15
    day = clock["day"]
    if path == "/sports":
        return [{"key": k, "active": True, "has_outrights": False}
                for k in ("soccer_epl", "basketball_nba", "tennis_atp_china_open",
                          "handball_germany_bundesliga", "soccer_fifa_world_cup_winner")]
    key = path.split("/")[2]
    if path.endswith("/events"):
        return [{"id": g[2], "sport_key": g[0], "sport_title": g[1], "home_team": g[3],
                 "away_team": g[4], "commence_time": bot.iso(g[5])}
                for g in games(day) if g[0] == key]
    if path.endswith("/odds"):
        out = []
        for sk, title, eid, home, away, start, prices in games(day):
            if sk != key:
                continue
            names = [home, away] + (["Draw"] if len(prices) == 3 else [])
            books = [{"key": f"book{i}", "markets": [{"key": "h2h", "outcomes": [
                {"name": n, "price": round(p * (1 + 0.01 * i), 2)} for n, p in zip(names, prices)]}]}
                for i in range(7)]
            out.append({"id": eid, "sport_key": sk, "sport_title": title, "home_team": home,
                        "away_team": away, "commence_time": bot.iso(start), "bookmakers": books})
        return out
    if path.endswith("/scores"):
        out = []
        for d in range(max(0, day - 3), day):
            for sk, _, eid, home, away, _, _ in games(d):
                if sk != key:
                    continue
                mode = OUTCOMES[d]
                if mode == "postponed":
                    out.append({"id": eid, "completed": False, "scores": None,
                                "home_team": home, "away_team": away})
                    continue
                hs, as_ = ("3", "1") if mode == "fav" else ("0", "2")
                out.append({"id": eid, "completed": True, "home_team": home, "away_team": away,
                            "scores": [{"name": home, "score": hs}, {"name": away, "score": as_}]})
        return out
    return []


bot.api_get = fake_api
out_dir = bot.ROOT / "out"
start = datetime(2026, 10, 8, 6, 5, tzinfo=timezone.utc)
for day in range(9):
    clock.update(now=start + timedelta(days=day), day=min(day, 5))
    clock["day"] = day if day <= 5 else 5
    if day > 5:
        OUTCOMES[day] = "dog"
        clock["day"] = day
    ran = bot.run(now=clock["now"])
    state = json.loads(bot.STATE_PATH.read_text())
    print(f"day {day}: ran={ran} bankroll={state['bankroll']} open={len(state['open_tickets'])} "
          f"stopped={state['stopped']}")
    if (out_dir / "email.html").exists():
        shutil.move(out_dir / "email.html", out_dir / f"day-{day}.html")
print(bot.LEDGER_PATH.read_text())
print("too-early check:", bot.run(now=datetime(2026, 11, 20, 6, 5, tzinfo=timezone.utc)))
