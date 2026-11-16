import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import recal_check as R

assert abs(R.recal(0.7, 1.0) - 0.7) < 1e-9
assert R.recal(0.7, 1.2) > 0.7 > R.recal(0.7, 0.8)
assert R.season("2026-11-16") == "2026/2027" and R.season("2026-03-01") == "2025/2026"
obs = [("2026-08-01", [0.8, 0.1, 0.1], [1.30, 9, 9], 0), ("2026-08-02", [0.8, 0.1, 0.1], [1.30, 9, 9], 2)]
r = R.favourite_returns(obs)
assert r["2026/2027"][0] == 2
assert abs(r["2026/2027"][1] - (0.30 * 0.85 - 1) / 2) < 1e-9
assert R.brier(obs, 1.0) > 0
print("recal ok")
