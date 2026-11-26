#!/usr/bin/env python3
"""Signal lab: does anything known before kick-off say which favourites win, beyond the sharp price?

One row per match: the side Pinnacle (power de-margined, pre-match columns) makes favourite at
MIN_P or more. Signals, all "favourite minus opponent" and all known when the bot picks:
  agree   Pinnacle's logit chance minus the soft market average's (the fav_agree idea)
  best    how much the best price (capped 10% above average) pays above Pinnacle's fair price
  elo     a goal-margin Elo rating's logit expectation minus Pinnacle's logit chance
  form    points per game over the last 5 matches
  shots   shots-on-target difference over the last 6 matches (a free stand-in for xG)
  rest    days since the previous league match (capped at 14)
  tight   played within the last 3 days
  ah      win chance implied by the Asian handicap and over/under 2.5 prices (a goals model)
          minus the 1X2 chance, in logits
  low     chance of under 2.5 goals (more draws)
  home    favourite plays at home
Each is tested walk-forward (fit on earlier seasons only) as a correction ON TOP of Pinnacle's
logit chance: log loss against Pinnacle alone, and what a "pick the favourites the model likes
most" rule wins against their priced chance. Data: football-data.co.uk columns (public mirror,
see IMPROVING.md).  python signal_lab.py --dir <mirror>/data   Needs numpy.
"""
import argparse
import math
from collections import defaultdict, deque
from datetime import date
from pathlib import Path

import numpy as np

import backtest
import bot

ROOT = Path(__file__).resolve().parent
MIN_P = 0.55
SIGNALS = ["agree", "best", "elo", "form", "shots", "rest", "tight", "ah", "low", "home"]
WARMUP = ["1718", "1819"]          # ratings only
SEASONS = ["1920", "2021", "2122", "2223", "2324", "2425", "2526"]
TEST = SEASONS[2:]                  # each fitted on the seasons before it
# untouched earlier seasons, for replication (market columns are named BbAv/BbMx there)
OLD_WARMUP = ["1213"]
OLD_SEASONS = ["1314", "1415", "1516", "1617", "1718", "1819"]
THIRDS = ["shots", "form", "elo", "ah"]
TAX = bot.CONFIG["tax_rate"]


def logit(p):
    p = min(max(p, 1e-6), 1 - 1e-6)
    return math.log(p / (1 - p))


def num(row, key):
    try:
        v = float(row.get(key) or "")
    except ValueError:
        return None
    return v if math.isfinite(v) else None


# --------------------------------------------- goals model from AH + O/U ----
MAXG = 12
FACT = np.array([math.factorial(k) for k in range(MAXG)], dtype=float)


def score_matrix(lh, la):
    k = np.arange(MAXG)
    ph = np.exp(-lh) * lh ** k / FACT
    pa = np.exp(-la) * la ** k / FACT
    m = np.outer(ph, pa)
    return m / m.sum()


def margin_probs(m):
    """{home goal margin: probability}."""
    return {d: float(np.trace(m, offset=-d)) for d in range(-MAXG + 1, MAXG)}


def ah_effective(margins, line):
    """Home side's win share of the decided stake at Asian handicap `line` (quarter lines split)."""
    parts = [line] if abs(line * 2 - round(line * 2)) < 1e-9 else [line - 0.25, line + 0.25]
    win = loss = 0.0
    for part in parts:
        for d, p in margins.items():
            if d + part > 1e-9:
                win += p
            elif d + part < -1e-9:
                loss += p
    return win / (win + loss)


def under_prob(total):
    return math.exp(-total) * (1 + total + total ** 2 / 2)


def total_from_under(p_under):
    lo, hi = 0.3, 7.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if under_prob(mid) > p_under else (lo, mid)
    return (lo + hi) / 2


def goals_model(p_under, line, ah_home):
    """(home win, draw, away win) of two Poisson sides matching the O/U 2.5 and AH prices."""
    total = total_from_under(p_under)
    lo, hi = -total + 0.05, total - 0.05          # supremacy = home mean - away mean
    for _ in range(30):
        mid = (lo + hi) / 2
        m = score_matrix((total + mid) / 2, (total - mid) / 2)
        lo, hi = (mid, hi) if ah_effective(margin_probs(m), line) < ah_home else (lo, mid)
    sup = (lo + hi) / 2
    margins = margin_probs(score_matrix((total + sup) / 2, (total - sup) / 2))
    home = sum(p for d, p in margins.items() if d > 0)
    away = sum(p for d, p in margins.items() if d < 0)
    return home, margins[0], away


# ------------------------------------------------------------- ratings ----
class History:
    """Per-team Elo (goal-margin weighted) and recent results, fed in date order."""

    def __init__(self, k=20.0, home_adv=65.0):
        self.k, self.home_adv = k, home_adv
        self.elo = defaultdict(lambda: 1500.0)
        self.points = defaultdict(lambda: deque(maxlen=5))
        self.shots = defaultdict(lambda: deque(maxlen=6))
        self.last = {}

    def expect(self, home, away):
        """Expected score (win 1, draw 0.5) of the home side."""
        return 1 / (1 + 10 ** (-(self.elo[home] + self.home_adv - self.elo[away]) / 400))

    def before(self, home, away, day):
        def mean(q):
            return sum(q) / len(q) if len(q) >= 3 else None

        def rest(t):
            return min((day - self.last[t]).days, 14) if t in self.last else None
        e = self.expect(home, away)
        return {s: {"elo": se, "form": mean(self.points[t]), "shots": mean(self.shots[t]),
                    "rest": rest(t)}
                for s, t, se in (("H", home, e), ("A", away, 1 - e))}

    def update(self, home, away, day, hg, ag, hst=None, ast=None):
        score = 1.0 if hg > ag else 0.5 if hg == ag else 0.0
        mult = math.log(abs(hg - ag) + 1) + 1
        delta = self.k * mult * (score - self.expect(home, away))
        self.elo[home] += delta
        self.elo[away] -= delta
        self.points[home].append(3 if hg > ag else 1 if hg == ag else 0)
        self.points[away].append(3 if ag > hg else 1 if hg == ag else 0)
        if hst is not None and ast is not None:
            self.shots[home].append(hst - ast)
            self.shots[away].append(ast - hst)
        self.last[home] = self.last[away] = day


# ---------------------------------------------------------------- rows ----
def favourite_row(row, hist_before):
    """The favourite's signals for one match, or None (no sharp price or no clear favourite)."""
    pre = [num(row, f"PS{s}") for s in "HDA"]
    avg = [num(row, f"Avg{s}") or num(row, f"BbAv{s}") for s in "HDA"]
    if not all(v and v > 1 for v in pre + avg):
        return None
    sharp, soft = bot.power_devig(pre), bot.power_devig(avg)
    side = 0 if sharp[0] >= sharp[2] else 2
    p = sharp[side]
    if p < MIN_P:
        return None
    s, o = ("H", "A") if side == 0 else ("A", "H")
    best = num(row, f"Max{s}") or num(row, f"BbMx{s}")
    price = bot.best_offer([(best, "max")], avg[side])[0] if best and best > 1 else None
    price = max(price or avg[side], avg[side])
    me, them = hist_before[s], hist_before[o]

    def diff(k):
        return None if me[k] is None or them[k] is None else me[k] - them[k]
    out = {"p": p, "avg_odds": avg[side], "best_odds": price,
           "won": 1 if row["FTR"] == s else 0,
           "agree": logit(p) - logit(soft[side]),
           "best": p * price - 1,
           "elo": logit(me["elo"]) - logit(p),
           "form": diff("form"), "shots": diff("shots"), "rest": diff("rest"),
           "tight": None if me["rest"] is None else float(me["rest"] <= 3),
           "ah": None, "low": None, "home": float(side == 0)}
    under = [num(row, "P<2.5"), num(row, "P>2.5")]
    line, ah_h, ah_a = num(row, "AHh"), num(row, "PAHH"), num(row, "PAHA")
    if all(v and v > 1 for v in under):
        pu = bot.power_devig(under)[0]
        out["low"] = pu
        if line is not None and ah_h and ah_a and ah_h > 1 and ah_a > 1:
            q = (1 / ah_h) / (1 / ah_h + 1 / ah_a)
            model = goals_model(pu, line, q)
            out["ah"] = logit(model[side]) - logit(p)
    close = [num(row, f"PSC{x}") for x in "HDA"]
    out["close_p"] = bot.power_devig(close)[side] if all(v and v > 1 for v in close) else None
    return out


def season_of(path):
    return path.stem.replace("season-", "")


def build_rows(folder, seasons=SEASONS, warmup=WARMUP):
    matches = []
    for path in sorted(Path(folder).rglob("season-*.csv")):
        s = season_of(path)
        if s in warmup or s in seasons:
            for r in backtest.read_rows(path.read_text(encoding="latin-1")):
                matches.append((r["_date"], s, r))
    matches.sort(key=lambda m: (m[0], m[2]["HomeTeam"]))
    hist, rows = History(), []
    i = 0
    while i < len(matches):                    # one day at a time: no same-day leakage
        j = i
        while j < len(matches) and matches[j][0] == matches[i][0]:
            j += 1
        day = date.fromisoformat(matches[i][0])
        for _, s, r in matches[i:j]:
            if s in seasons:
                f = favourite_row(r, hist.before(r["HomeTeam"], r["AwayTeam"], day))
                if f:
                    rows.append(dict(f, season=s))
        for _, s, r in matches[i:j]:
            hist.update(r["HomeTeam"], r["AwayTeam"], day, r["_hg"], r["_ag"],
                        num(r, "HST"), num(r, "AST"))
        i = j
    return rows


# ------------------------------------------------------------- fitting ----
def fit_offset(X, y, offset, ridge=1.0, steps=30):
    """Logistic regression with a fixed offset (Newton, ridge on the slopes, not the intercept)."""
    beta = np.zeros(X.shape[1])
    pen = np.full(X.shape[1], ridge)
    pen[0] = 0.0
    for _ in range(steps):
        mu = 1 / (1 + np.exp(-(offset + X @ beta)))
        grad = X.T @ (y - mu) - pen * beta
        hess = (X * (mu * (1 - mu))[:, None]).T @ X + np.diag(pen) + 1e-9 * np.eye(len(beta))
        step = np.linalg.solve(hess, grad)
        beta += step
        if np.abs(step).max() < 1e-8:
            break
    return beta


def matrix(rows, names, mean, sd):
    cols = [np.ones(len(rows))]
    for k, m, s in zip(names, mean, sd):
        v = np.array([m if r[k] is None else r[k] for r in rows], dtype=float)
        cols.append((v - m) / s)
    return np.column_stack(cols)


def walk_forward(rows, names, test=TEST):
    """Out-of-sample corrected chance for every test-season row; intercept-only if no names."""
    done, preds = [], []
    for season in test:
        train = [r for r in rows if r["season"] < season]
        hold = [r for r in rows if r["season"] == season]
        if not train or not hold:
            continue
        mean, sd = [], []
        for k in names:
            v = np.array([r[k] for r in train if r[k] is not None], dtype=float)
            mean.append(v.mean())
            sd.append(v.std() or 1.0)
        off = np.array([logit(r["p"]) for r in train])
        beta = fit_offset(matrix(train, names, mean, sd),
                          np.array([r["won"] for r in train], dtype=float), off, ridge=10.0)
        z = np.array([logit(r["p"]) for r in hold]) + matrix(hold, names, mean, sd) @ beta
        done.extend(hold)
        preds.extend(1 / (1 + np.exp(-z)))
    return done, np.array(preds)


def log_loss_gain(rows, preds):
    """Mean log-loss improvement over Pinnacle alone and its standard error (positive = better)."""
    y = np.array([r["won"] for r in rows], dtype=float)
    p = np.array([r["p"] for r in rows])

    def ll(q):
        return -(y * np.log(q) + (1 - y) * np.log(1 - q))
    d = ll(p) - ll(preds)
    return float(d.mean()), float(d.std(ddof=1) / math.sqrt(len(d)))


def subset_stats(rows):
    """Win rate, priced chance, gap in points with se, and flat return after tax at best price."""
    n = len(rows)
    if not n:
        return None
    won = sum(r["won"] for r in rows) / n
    priced = sum(r["p"] for r in rows) / n
    se = math.sqrt(sum(r["p"] * (1 - r["p"]) for r in rows)) / n
    ret = [(1 + (r["best_odds"] - 1) * (1 - TAX)) * r["won"] - 1 for r in rows]
    return {"n": n, "won": won, "priced": priced, "gap": won - priced, "se": se,
            "ret": sum(ret) / n, "odds": sum(r["best_odds"] for r in rows) / n}


def line_of(label, s):
    return (f"| {label} | {s['n']} | {s['won']:.1%} | {s['priced']:.1%} | "
            f"{100 * s['gap']:+.1f} ± {100 * s['se']:.1f} | {s['odds']:.2f} | {s['ret']:+.1%} |")


HEAD = ["| Group | Bets | Won | Priced | Won minus priced (points) | Avg best odds | "
        "Return after tax |", "|---|---|---|---|---|---|---|"]


def price_adjusted(rows, key):
    """(a, b, low cut, high cut): signal minus what the price already implies (a + b*logit p),
    and the thirds of that residual. Raw signals mostly restate how strong the favourite is."""
    sub = [r for r in rows if r[key] is not None]
    A = np.column_stack([np.ones(len(sub)), [logit(r["p"]) for r in sub]])
    v = np.array([r[key] for r in sub], dtype=float)
    coef = np.linalg.lstsq(A, v, rcond=None)[0]
    lo, hi = np.quantile(v - A @ coef, [1 / 3, 2 / 3])
    return float(coef[0]), float(coef[1]), float(lo), float(hi)


def third_of(r, key, fit):
    a, b, lo, hi = fit
    if r[key] is None:
        return None
    res = r[key] - (a + b * logit(r["p"]))
    return "top" if res > hi else "bottom" if res <= lo else "middle"


def mean_move(rows):
    """Average change of Pinnacle's chance from the pre-match price to the close, in points."""
    v = [r["close_p"] - r["p"] for r in rows if r["close_p"] is not None]
    return 100 * sum(v) / len(v) if v else float("nan")


def thirds_report(periods):
    """periods: [(label, rows)]; the thirds are fitted on the first period and only applied
    to the others."""
    out = ["", "## Price-adjusted thirds, with replication on untouched seasons", "",
           "Top third = the signal is better than usual for a favourite at that price. "
           "\"Move\" is how far Pinnacle's chance went by the close. \"Seasons\" counts the "
           "seasons where the top third beat the bottom third (move / won minus priced).", "",
           "| Signal, period, third | Bets | Won | Priced | Won minus priced (points) | "
           "Move (points) | Return after tax | Seasons |", "|---|---|---|---|---|---|---|---|"]
    for key in THIRDS:
        fit = price_adjusted(periods[0][1], key)
        for label, rows in periods:
            groups = {t: [r for r in rows if third_of(r, key, fit) == t]
                      for t in ("top", "bottom")}
            moves = gaps = total = 0
            for season in sorted({r["season"] for r in rows}):
                a, b = ([r for r in groups[t] if r["season"] == season] for t in groups)
                if a and b:
                    total += 1
                    moves += mean_move(a) > mean_move(b)
                    gaps += subset_stats(a)["gap"] > subset_stats(b)["gap"]
            for t, g in groups.items():
                if g:
                    st = subset_stats(g)
                    out.append(
                        f"| {key}, {label}, {t} | {st['n']} | {st['won']:.1%} | "
                        f"{st['priced']:.1%} | {100 * st['gap']:+.1f} ± {100 * st['se']:.1f} | "
                        f"{mean_move(g):+.2f} | {st['ret']:+.1%} | "
                        f"{f'{moves}/{total} and {gaps}/{total}' if t == 'top' else ''} |")
    return "\n".join(out) + "\n"


def report(rows):
    out = ["# Signal lab: can anything pick winning favourites better than the sharp price?", "",
           f"{len(rows)} European league matches, seasons {SEASONS[0]}-{SEASONS[-1]}, where "
           f"Pinnacle's pre-match favourite had a {MIN_P:.0%}+ chance. Built by signal_lab.py.",
           "", "## Walk-forward: each signal added on top of Pinnacle's chance", "",
           "Fitted on earlier seasons only, tested on 2021/22 to 2025/26. Gain is log loss "
           "saved per bet (x0.0001); positive and above 2 standard errors would be real.", "",
           "| Signals | Test bets | Gain x0.0001 | se | z |", "|---|---|---|---|---|"]
    sets = [("recalibration only", [])] + [(k, [k]) for k in SIGNALS] + [("all together", SIGNALS)]
    full = None
    for label, names in sets:
        done, preds = walk_forward(rows, names)
        g, se = log_loss_gain(done, preds)
        out.append(f"| {label} | {len(done)} | {g * 1e4:+.1f} | {se * 1e4:.1f} | "
                   f"{g / se if se else 0:+.1f} |")
        if label == "all together":
            full = (done, preds)
    done, preds = full
    lift = preds - np.array([r["p"] for r in done])
    order = np.argsort(-lift)
    third = len(done) // 3
    out += ["", "## Does the all-signal model pick better favourites? (out of sample)", ""] + HEAD
    for label, idx in (("model likes most (top third)", order[:third]),
                       ("middle third", order[third:2 * third]),
                       ("model likes least (bottom third)", order[2 * third:])):
        out.append(line_of(label, subset_stats([done[i] for i in idx])))
    out += ["", "## The single rules, every season (no fitting)", ""] + HEAD
    rules = [("all favourites", lambda r: True),
             ("agree: sharp >= soft (fav_agree rule)", lambda r: r["agree"] >= 0),
             ("sharp below soft", lambda r: r["agree"] < 0),
             ("sharp below soft by 0.05+ logits", lambda r: r["agree"] < -0.05),
             ("favourite rested 3 days or less", lambda r: r["tight"] == 1),
             ("favourite at home", lambda r: r["home"] == 1),
             ("favourite away", lambda r: r["home"] == 0)]
    for floor in (0.55, 0.70):
        for label, rule in rules:
            sub = [r for r in rows if r["p"] >= floor and rule(r)]
            if sub:
                out.append(line_of(f"{label}, chance {floor:.0%}+", subset_stats(sub)))
    out += ["", "## The only lever on hit rate: how short the favourite is", ""] + HEAD
    for lo, hi in ((0.55, 0.60), (0.60, 0.70), (0.70, 0.80), (0.80, 1.01)):
        sub = [r for r in rows if lo <= r["p"] < hi]
        if sub:
            out.append(line_of(f"chance {lo:.0%}-{min(hi, 1):.0%}", subset_stats(sub)))
    moved = [r for r in rows if r["close_p"] is not None]
    if moved:
        out += ["", "## Can the signals foresee Pinnacle's closing move? (closing line value)", "",
                "| Signal | Matches | Correlation with logit move to the close |", "|---|---|---|"]
        move = {id(r): logit(r["close_p"]) - logit(r["p"]) for r in moved}
        for k in SIGNALS:
            sub = [r for r in moved if r[k] is not None]
            x = np.array([r[k] for r in sub], dtype=float)
            y = np.array([move[id(r)] for r in sub])
            out.append(f"| {k} | {len(sub)} | {np.corrcoef(x, y)[0, 1]:+.3f} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=str(ROOT / "data" / "backtest" / "signals.md"))
    args = ap.parse_args()
    rows = build_rows(args.dir)
    text = report(rows)
    old = build_rows(args.dir, OLD_SEASONS, OLD_WARMUP)
    periods = [(f"{SEASONS[0]}-{SEASONS[-1]}", rows)]
    if old:
        periods.append((f"replication {OLD_SEASONS[0]}-{OLD_SEASONS[-1]}", old))
    text += thirds_report(periods)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
