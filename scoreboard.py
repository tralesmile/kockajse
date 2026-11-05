"""Strategy scoreboard scored at closing prices, with an always-valid sequential test.

Why: win/loss results need hundreds of bets to tell strategies apart (a 3-leg ticket at
2.5-3.5 has a standard deviation of about 130% of the stake per bet). The closing price is
the best known estimate of the true chance (Pinnacle's close beats every model we have
tried), so each bet can be scored the moment the watcher captures its closing price:

    xROI = P_close * (1 + (1 - tax) * (O - 1)) - 1

with O the bet's (ticket's) odds and P_close the product of its legs' margin-free closing
chances. In the 2019-2026 backtest this "expected ROI" tracked the realised ROI of every
strategy (data/backtest/report.md) with a small fraction of its noise.

The scoreboard then asks, per strategy, "is the mean xROI after tax above zero?" with the
mixture sequential probability ratio test (mSPRT, Johari, Pekelis and Walsh 2015,
arXiv 1512.04922): normal data, mixing distribution N(0, tau^2) on the mean,

    Lambda_n = sqrt(s^2 / (s^2 + n tau^2)) * exp(n^2 tau^2 m^2 / (2 s^2 (s^2 + n tau^2)))

and the always-valid p-value p_n = min(p_{n-1}, 1 / Lambda_n). Unlike a fixed-sample test
it may be read after every bet (as the email does) without inflating false alarms, so a
strategy can be declared better or worse as soon as the evidence is enough.

Nothing here changes which ticket is emailed; it only reads the logs.
Run: python scoreboard.py   (writes data/scoreboard.md and prints it)
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NEAR_MINUTES = 60   # a capture this close to the start counts as the closing price
TAU = 0.05          # prior scale of a strategy's true mean xROI (edges of a few %)
MIN_SIGMA = 0.05    # floor on the per-bet spread while few bets exist
MIN_BETS = 20       # no verdict before this many scored bets
BURN_IN = 10        # the variance is estimated from the data, so the test starts here:
                    # from bet 2 the plug-in variance made 17% false alarms in 200 null
                    # simulations of 150 bets (sd 0.3); from bet 10, 2.5% (alpha 5%)
ALPHA = 0.05


def _key(event_id, market, sel, point):
    point = "" if point in (None, "") else f"{float(point):g}"
    return (event_id, market, sel, point)


def _f(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def closing_fair(closing_rows):
    """Bet key -> (margin-free closing chance, minutes before start) of its nearest capture.

    The power-method chance (close_power) is preferred where recorded (it is calibrated on
    80,832 Pinnacle closes, slope 1.013); older rows have only the proportional sharp
    chance (close_sharp), or for rows logged by power_value close_sharp is already power.
    Without a sharp book, the de-margined average (close_consensus)."""
    out = {}
    for r in closing_rows:
        minutes = _f(r.get("minutes_before"))
        if minutes is None or _f(r.get("close_odds")) is None:
            continue
        p = _f(r.get("close_power")) or _f(r.get("close_sharp")) or _f(r.get("close_consensus"))
        if p is None:
            continue
        key = _key(r["event_id"], r["market"], r["sel"], r["point"])
        has_power = _f(r.get("close_power")) is not None or r.get("source") == "power_value"
        best = out.get(key)
        if best is None or (minutes, not has_power) < (best[1], not best[2]):
            out[key] = (p, minutes, has_power)
    return {k: (p, m) for k, (p, m, _) in out.items()}


def score_bets(shadow_rows, closing_rows, tax):
    """One record per shadow bet (shadow_id): date, strategy, xROI at the close (None when
    a leg has no closing capture within NEAR_MINUTES), and the realised return per unit
    once settled (None while pending)."""
    fair = closing_fair(closing_rows)
    bets = {}
    for r in shadow_rows:
        bets.setdefault(r["shadow_id"], []).append(r)
    out = []
    for sid, legs in bets.items():
        strategy, date = legs[0]["strategy"], legs[0]["date"]
        late = strategy.startswith("late_")  # logged minutes before the start: its price is the close
        live = [l for l in legs if l["result"] != "void"]
        if not live:
            continue
        odds, chance, scored = 1.0, 1.0, True
        for l in live:
            odds *= float(l["odds"])
            if late:
                p = _f(l["fair_chance"])
            else:
                hit = fair.get(_key(l["event_id"], l["market"], l["sel"], l["point"]))
                p = hit[0] if hit and hit[1] <= NEAR_MINUTES else None
            if p is None:
                scored = False
            else:
                chance *= p
        payout = 1 + (1 - tax) * (odds - 1)
        xroi = chance * payout - 1 if scored else None
        results = [l["result"] for l in live]
        if "lost" in results:
            real = -1.0
        elif "pending" in results:
            real = None
        else:
            real = payout - 1
        out.append({"shadow_id": sid, "date": date, "strategy": strategy,
                    "odds": odds, "xroi": xroi, "real": real})
    return out


def pick_bets(pick_rows):
    """The AI's judged picks as shadow-like singles at the logged (average) price, grouped by
    verdict ("pick:AGREE", ...), so the closing price tests the AI's judgement directly: if
    its verdicts carry information, AGREE picks should close better than AVOID picks."""
    out = []
    for i, r in enumerate(pick_rows):
        verdict = r.get("verdict") or "NONE"
        out.append(dict(r, strategy=f"pick:{verdict}", shadow_id=f"{r['date']}-pick-{i}",
                        fair_chance=r.get("market_chance", "")))
    return out


def msprt(values, tau=TAU, min_sigma=MIN_SIGMA, burn_in=BURN_IN):
    """Always-valid p-value for "mean = 0" after each value, in order; returns the last."""
    p = 1.0
    for n in range(max(2, burn_in), len(values) + 1):
        xs = values[:n]
        m = sum(xs) / n
        var = max(sum((x - m) ** 2 for x in xs) / (n - 1), min_sigma ** 2)
        t2 = tau ** 2
        log_lam = 0.5 * math.log(var / (var + n * t2)) + n * n * t2 * m * m / (2 * var * (var + n * t2))
        p = min(p, math.exp(-log_lam) if log_lam < 700 else 0.0)
    return p


def _phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def strategy_stats(bets, min_bets=MIN_BETS, alpha=ALPHA):
    """Per strategy: bets logged, scored share, mean xROI, its se, P(mean > 0) under a flat
    prior (the Thompson-sampling weight a bandit would use), always-valid p, verdict, and
    the realised ROI of settled bets for comparison (luck = realised - expected)."""
    groups = {}
    for b in sorted(bets, key=lambda b: (b["date"], b["shadow_id"])):
        groups.setdefault(b["strategy"], []).append(b)
    actual = {}
    for b in groups.get("actual", []):
        if b["xroi"] is not None:
            actual.setdefault(b["date"], []).append(b["xroi"])
    out = {}
    for strategy, items in groups.items():
        xs = [b["xroi"] for b in items if b["xroi"] is not None]
        reals = [b["real"] for b in items if b["real"] is not None]
        n = len(xs)
        s = {"logged": len(items), "scored": n, "mean": None, "se": None, "p_pos": None,
             "p_value": None, "verdict": "undecided", "settled": len(reals),
             "real": sum(reals) / len(reals) if reals else None, "paired": None}
        if n:
            m = sum(xs) / n
            s["mean"] = m
            if n >= 2:
                sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
                se = max(sd, 1e-9) / math.sqrt(n)
                s["se"] = se
                s["p_pos"] = _phi(m / se)
                s["p_value"] = msprt(xs)
                if n >= min_bets and s["p_value"] < alpha:
                    s["verdict"] = "beats the tax" if m > 0 else "loses after tax"
        if strategy != "actual":  # same days, day by day, against the real ticket
            days = {}
            for b in items:
                if b["xroi"] is not None and b["date"] in actual:
                    days.setdefault(b["date"], []).append(b["xroi"])
            diffs = [sum(v) / len(v) - sum(actual[d]) / len(actual[d]) for d, v in days.items()]
            if len(diffs) >= 2:
                md = sum(diffs) / len(diffs)
                sd = math.sqrt(sum((d - md) ** 2 for d in diffs) / (len(diffs) - 1))
                s["paired"] = (md, sd / math.sqrt(len(diffs)), len(diffs))
        out[strategy] = s
    return out


def _pct(x, digits=1):
    return "-" if x is None else f"{x * 100:+.{digits}f}%"


def table_rows(stats, names):
    order = [k for k in names if k in stats] + sorted(k for k in stats if k not in names)
    rows = []
    for k in order:
        s = stats[k]
        paired = "-"
        if s["paired"]:
            md, se, days = s["paired"]
            paired = f"{md * 100:+.1f} ± {se * 100:.1f} ({days} d)"
        rows.append([names.get(k, k), str(s["logged"]), str(s["scored"]), _pct(s["mean"]),
                     "-" if s["se"] is None else f"{s['se'] * 100:.1f}",
                     "-" if s["p_pos"] is None else f"{s['p_pos']:.0%}",
                     "-" if s["p_value"] is None else f"{s['p_value']:.2f}",
                     s["verdict"], paired, _pct(s["real"], 0), str(s["settled"])])
    return rows


HEADER = ["Strategy", "Bets", "Scored at close", "Expected return after tax", "se (points)",
          "Chance it beats the tax", "Always-valid p", "Verdict", "vs real ticket, same days",
          "Realised return", "Settled"]


def markdown(stats, names):
    lines = ["# Strategy scoreboard at closing prices", "",
             "Each bet is scored when its closing price is captured: expected return per unit "
             "after the 15% tax if the margin-free closing chance is the true chance. Verdicts "
             f"use an always-valid sequential test (mSPRT, alpha {ALPHA}, at least {MIN_BETS} "
             "scored bets), so the table may be read every day. Built by scoreboard.py.", "",
             "| " + " | ".join(HEADER) + " |", "|" + "---|" * len(HEADER)]
    lines += ["| " + " | ".join(r) + " |" for r in table_rows(stats, names)]
    return "\n".join(lines) + "\n"


def html(stats, names):
    if not any(s["scored"] for s in stats.values()):
        return ""
    keep = [0, 1, 2, 3, 5, 7, 9]  # a compact subset for the email
    head = "".join(f"<th>{HEADER[i]}</th>" for i in keep)
    body = "".join("<tr>" + "".join(f"<td>{r[i]}</td>" for i in keep) + "</tr>"
                   for r in table_rows(stats, names))
    return ("<h3>Scoreboard at closing prices</h3><table border='1' cellpadding='5' "
            "cellspacing='0' style='border-collapse:collapse;font-size:13px'><tr>" + head
            + "</tr>" + body + "</table><p><small>Each bet is scored as soon as its price "
            "shortly before kick-off is known: what it would return on average after tax if "
            "that closing price is right. This settles which strategy is better within weeks "
            "instead of months; a verdict appears once the evidence is strong enough.</small></p>")


PICK_NAMES = {"pick:AGREE": "Picks the AI rated AGREE (singles, average price)",
              "pick:RISKY": "Picks rated RISKY (singles, average price)",
              "pick:AVOID": "Picks rated AVOID (singles, average price)"}


def build(shadow_rows, closing_rows, tax, names=None, pick_rows=None):
    names = dict(names or {}, **PICK_NAMES)
    rows = list(shadow_rows) + pick_bets(pick_rows or [])
    stats = strategy_stats(score_bets(rows, closing_rows, tax))
    return stats, markdown(stats, names), html(stats, names)


def _read(path):
    if not path.exists():
        return []
    with path.open() as fh:
        return list(csv.DictReader(fh))


def write(data_dir=None, tax=None, names=None, picks_path=None, closing_path=None):
    """Read data/shadow.csv, closing.csv and picks.csv, write data/scoreboard.md; return
    (stats, markdown, html)."""
    data_dir = Path(data_dir or ROOT / "data")
    picks_path = Path(picks_path or data_dir / "picks.csv")
    closing_path = Path(closing_path or data_dir / "closing.csv")
    if tax is None:
        import json
        tax = json.loads((ROOT / "config.json").read_text())["tax_rate"]
    stats, md, page = build(_read(data_dir / "shadow.csv"), _read(closing_path), tax, names,
                            _read(picks_path))
    (data_dir / "scoreboard.md").write_text(md)
    return stats, md, page


if __name__ == "__main__":
    try:
        from bot import SHADOW_NAMES as _names
    except Exception:  # bot needs its environment; the table works without the long names
        _names = {}
    print(write(names=_names)[1])
