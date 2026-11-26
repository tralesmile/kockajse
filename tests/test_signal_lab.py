"""signal_lab: goals model, ratings without leakage, fitting, price adjustment.
Run: python tests/test_signal_lab.py   (needs numpy; skipped without it)"""
import math
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    import numpy as np
except ImportError:
    print("skipped: numpy not installed")
    sys.exit(0)
import signal_lab as L  # noqa: E402

# Asian handicap on a known margin distribution: win by 1 (50%), draw (30%), lose by 1 (20%)
m = {1: 0.5, 0: 0.3, -1: 0.2}
assert abs(L.ah_effective(m, -0.5) - 0.5) < 1e-9
assert abs(L.ah_effective(m, 0.0) - 0.5 / 0.7) < 1e-9          # the draw is returned
assert abs(L.ah_effective(m, -0.25) - 0.5 / (0.5 + 0.2 + 0.15)) < 1e-9   # half the draw lost

# the goals model recovers the sides it was built from
sm = L.score_matrix(1.8, 0.9)
margins = L.margin_probs(sm)
home = sum(p for d, p in margins.items() if d > 0)
under = L.under_prob(2.7)
got = L.goals_model(under, -0.75, L.ah_effective(margins, -0.75))
assert abs(got[0] - home) < 0.01 and abs(sum(got) - 1) < 1e-6, (got, home)

# ratings: nothing before a match includes that match
h = L.History()
b = h.before("A", "B", date(2024, 8, 1))
assert b["H"]["form"] is None and b["H"]["rest"] is None
for i in range(4):
    h.update("A", "B", date(2024, 8, 1 + 2 * i), 3, 0, 8, 2)
b = h.before("A", "B", date(2024, 8, 9))
assert b["H"]["form"] == 3 and b["A"]["form"] == 0 and b["H"]["shots"] == 6
assert b["H"]["rest"] == 2 and b["H"]["elo"] > 0.7 > 0.3 > b["A"]["elo"]

# a favourite row: clear home favourite, away favourite, and no favourite
row = {"PSH": "1.40", "PSD": "4.8", "PSA": "8.0", "BbAvH": "1.38", "BbAvD": "4.6",
       "BbAvA": "7.5", "BbMxH": "1.45", "FTR": "H", "P<2.5": "2.1", "P>2.5": "1.8",
       "AHh": "-1.25", "PAHH": "1.95", "PAHA": "1.95", "PSCH": "1.36", "PSCD": "5.0",
       "PSCA": "8.5"}
f = L.favourite_row(row, h.before("A", "B", date(2024, 8, 9)))
assert f["home"] == 1 and f["won"] == 1 and f["best_odds"] == 1.45 and f["close_p"] > f["p"]
assert f["ah"] is not None
even = dict(row, PSH="2.6", PSD="3.3", PSA="2.7")
assert L.favourite_row(even, h.before("A", "B", date(2024, 8, 9))) is None

# offset fit finds a real signal and leaves noise alone
rng = np.random.default_rng(1)
x = rng.normal(size=20000)
off = rng.normal(0.7, 0.5, size=20000)
y = (rng.random(20000) < 1 / (1 + np.exp(-(off + 0.3 * x)))).astype(float)
beta = L.fit_offset(np.column_stack([np.ones_like(x), x]), y, off)
assert abs(beta[0]) < 0.05 and abs(beta[1] - 0.3) < 0.05, beta

# price adjustment removes what the price already says
rows = []
for i in range(300):
    p = 0.55 + 0.4 * (i % 100) / 100
    rows.append({"p": p, "shots": 2 * L.logit(p) + (i % 3 - 1)})
fit = L.price_adjusted(rows, "shots")
assert abs(fit[1] - 2) < 0.05
tops = [L.third_of(r, "shots", fit) for r in rows]
assert tops[2] == "top" and tops[0] == "bottom" and L.third_of({"p": 0.6, "shots": None},
                                                               "shots", fit) is None

# tax is on the winnings only, as the ledger does it
st = L.subset_stats([{"p": 0.5, "won": 1, "best_odds": 2.0}, {"p": 0.5, "won": 0,
                                                              "best_odds": 2.0}])
assert math.isclose(st["ret"], (1.85 - 1 + -1) / 2) and st["gap"] == 0
print("ok")
