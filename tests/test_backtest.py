"""Checks for the historical backtest. Run: python tests/test_backtest.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import backtest as bt  # noqa: E402

HEAD = ("Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,PSH,PSD,PSA,MaxH,MaxD,MaxA,AvgH,AvgD,AvgA,"
        "P>2.5,P<2.5,Max>2.5,Max<2.5,Avg>2.5,Avg<2.5,PSCH,PSCD,PSCA,MaxCH,MaxCD,MaxCA,"
        "AvgCH,AvgCD,AvgCA,PC>2.5,PC<2.5,MaxC>2.5,MaxC<2.5,AvgC>2.5,AvgC<2.5")


def line(day, home, away, hg, ag, h, d, a, avg=(None, None, None), mx=None, over=(1.9, 1.95)):
    avg = tuple(round(x * 0.95, 2) for x in (h, d, a)) if avg[0] is None else avg
    mx = mx or tuple(round(x * 1.02, 2) for x in (h, d, a))
    ou = f"{over[0]},{over[1]},{over[0] + 0.05:.2f},{over[1] + 0.05:.2f},{over[0] - 0.05:.2f},{over[1] - 0.05:.2f}"
    one = f"{h},{d},{a},{mx[0]},{mx[1]},{mx[2]},{avg[0]},{avg[1]},{avg[2]},{ou}"
    return f"E0,{day},15:00,{home},{away},{hg},{ag},{one},{one}"


rows_text = "\n".join([
    "﻿" + HEAD,
    line("01/08/2025", "A", "B", 2, 0, 1.40, 4.8, 8.0),
    line("01/08/2025", "C", "D", 1, 1, 1.55, 4.2, 6.0),
    line("01/08/2025", "E", "F", 0, 3, 1.85, 3.6, 4.4),
    line("01/08/2025", "G", "H", 3, 1, 1.30, 5.5, 10.0),
    line("02/08/2025", "I", "J", 1, 0, 1.45, 4.5, 7.0),
    line("02/08/2025", "K", "L", 0, 0, 1.60, 4.0, 5.5),
    "E0,03/08/2025,15:00,M,N,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",  # not played yet: skipped
])
rows = bt.read_rows(rows_text, "2526-E0")
assert len(rows) == 6 and rows[0]["_date"] == "2025-08-01", rows[:1]

# Candidates: 3 match winner + 3 double chance + 2 totals per match, Pinnacle fair chance.
c = bt.match_candidates(rows[0], 0)
assert len(c) == 8, [x["market"] for x in c]
home = next(x for x in c if x["market"] == "h2h" and x["sel"] == "H")
fair = (1 / 1.40) / (1 / 1.40 + 1 / 4.8 + 1 / 8.0)
assert abs(home["prob"] - fair) < 1e-9 and home["won"] and home["odds"] == round(1.40 * 0.95, 2)
x2 = next(x for x in c if x["sel"] == "X2")
assert not x2["won"] and x2["best"] is None
under = next(x for x in c if x["sel"] == "Under")
assert under["won"] and not next(x for x in c if x["sel"] == "Over")["won"]  # 2 goals
draw_dc = next(x for x in bt.match_candidates(rows[1], 1) if x["sel"] == "1X")
assert draw_dc["won"]  # 1:1 is a draw

# Best price above the 10% outlier cap is dropped.
r = dict(rows[0], MaxCH="1.60")
assert next(x for x in bt.match_candidates(r, 0) if x["sel"] == "H")["best"] is None
assert next(x for x in bt.match_candidates(rows[0], 0) if x["sel"] == "H")["best"] == round(1.40 * 1.02, 2)

# Tax: stake 1 at 3.00 wins 2.00, minus 15% = 1.70; a lost leg loses the stake.
legs = [{"odds": 1.5, "won": True}, {"odds": 2.0, "won": True}]
assert abs(bt.settle(legs) - 1.70) < 1e-9 and abs(bt.settle(legs, tax=0) - 2.0) < 1e-9
assert bt.settle([{"odds": 1.5, "won": True}, {"odds": 2.0, "won": False}]) == -1
assert bt.season_of("2025-08-01") == "2526" and bt.season_of("2026-05-20") == "2526"
assert bt.taxed_ev({"prob": 0.5, "odds": 2.0}) < 0 < bt.taxed_ev({"prob": 0.5}, 2.5)

# A full run over the tiny dataset, from a folder, writes both reports.
tmp = Path(tempfile.mkdtemp())
(tmp / "in").mkdir()
(tmp / "in" / "E0.csv").write_text(rows_text)
bt.main(["--dir", str(tmp / "in"), "--out", str(tmp / "out"), "--seasons", "2526"])
report = (tmp / "out" / "report.md").read_text()
assert "most_likely" in report and "Single legs" in report
import json  # noqa: E402
summary = json.loads((tmp / "out" / "summary.json").read_text())
ml = summary["strategies"]["most_likely"]
assert ml["bets"] >= 1 and summary["meta"]["days"] == 2, ml
for name, s in summary["strategies"].items():
    if s["bets"]:
        assert -1 <= s["roi"] <= 3, (name, s)
print("all backtest checks passed")
