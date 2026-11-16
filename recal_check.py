"""Backtest check: does stretching/shrinking the sharp (Pinnacle power) chance help favourite bets?

Usage: python recal_check.py <football-odds-mirror>/data [--seasons 1920,2021,...]
Reports Brier score by logit slope k, and favourite-bet return after tax per season.
Review 16 Nov 2026 result: k=1.0 has the best Brier; per-season return is noise (see data/learning_log.md).
"""
import collections
import math
import sys

import backtest as B
import bot

TAX = bot.CONFIG["tax_rate"]


def recal(p, k):
    """Stretch (k>1) or shrink (k<1) a chance on the logit scale."""
    return 1 / (1 + math.exp(-k * math.log(p / (1 - p))))


def observations(rows):
    """(date, power chances, best prices, outcome index) for 1X2 rows that have sharp and best prices."""
    out = []
    for r in rows:
        ps = [B.num(r, k) for k in ("PSCH", "PSCD", "PSCA")]
        mx = [B.num(r, k) for k in ("MaxCH", "MaxCD", "MaxCA")]
        if not all(ps) or not all(mx):
            continue
        res = 0 if r["_hg"] > r["_ag"] else (1 if r["_hg"] == r["_ag"] else 2)
        out.append((r["_date"], bot.power_devig(ps), mx, res))
    return sorted(out)


def brier(obs, k):
    return sum((recal(pc[i], k) - (res == i)) ** 2 for _, pc, _, res in obs for i in range(3)) / len(obs)


def taxed_ev(p, odds):
    return p * (1 + (odds - 1) * (1 - TAX)) - 1


def season(date):
    y, m = int(date[:4]), int(date[5:7])
    s = y if m >= 7 else y - 1
    return f"{s}/{s + 1}"


def favourite_returns(obs, k=1.0, thr=-0.02, min_chance=0.55):
    """{season: (bets, mean return per unit after tax)} for favourites passing the taxed-EV threshold."""
    agg = collections.defaultdict(lambda: [0, 0.0])
    for date, pc, mx, res in obs:
        for i in range(3):
            if pc[i] >= min_chance and taxed_ev(recal(pc[i], k), mx[i]) > thr:
                a = agg[season(date)]
                a[0] += 1
                a[1] += (mx[i] - 1) * (1 - TAX) if res == i else -1
    return {s: (n, t / n) for s, (n, t) in sorted(agg.items())}


def main(argv):
    folder = argv[1]
    seasons = argv[argv.index("--seasons") + 1].split(",") if "--seasons" in argv else None
    obs = observations(B.load_dir(folder, seasons))
    print(len(obs), "matches")
    for k in (0.9, 1.0, 1.1, 1.2):
        print("k", k, "brier", round(brier(obs, k), 5))
    for s, (n, r) in favourite_returns(obs).items():
        print(s, n, f"{r:+.1%}")


if __name__ == "__main__":
    main(sys.argv)
