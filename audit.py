"""Two standing audits that tell the reviews (and the owner) whether two parts of the bot earn
their keep. Both read recorded data only and never change it. Run: python audit.py

1. AI value audit. The ticket chance is the sharp (Pinnacle, power method) chance shifted
   `ai_weight` of the way toward the AI's own chance. On 392 settled picks (10 Nov 2026) the
   shift did not help: Brier 0.23024 without it, 0.23052 with the 20% shift, correlation of the
   AI's disagreement with the outcome -0.02. This audit repeats that test every day, with a
   standard error, so a change of the weight rests on evidence rather than on one review.
2. Bookmaker lead-lag. For matches with a captured closing price, how far is each bookmaker's
   first price of the day (margin removed, power method) from Pinnacle's closing chance?
   Idea: price-discovery "information share" (Hasbrouck) and Oikonomidis (2013): some books lead,
   others copy. A book that predicts the close better than Pinnacle's own morning price would
   be a better reference for the ticket. First reading (40 matches): no book beat Pinnacle
   beyond noise, an average of all books was marginally nearer (paired gain 0.0005 +- 0.0014).
"""
import csv
import glob
import gzip
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MIN_PICKS = 30
MIN_MATCHES = 15


def _f(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def _read(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open() as fh:
        return list(csv.DictReader(fh))


def _mean_se(values):
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    mean = sum(values) / n
    if n < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(var / n)


def ai_audit(pick_rows, weights=(0.0, 0.1, 0.2, 0.35, 0.5, 1.0), live_weight=0.2):
    """Brier score of the base chance blended with the AI chance at several weights, on settled
    picks that carry an AI chance. The base is the sharp chance when recorded, else the market's.
    Returns None when there are too few picks."""
    rows = []
    for r in pick_rows:
        if r.get("result") not in ("won", "lost"):
            continue
        ai = _f(r.get("ai_chance"))
        base = _f(r.get("sharp_chance")) or _f(r.get("market_chance"))
        if ai is None or base is None or not 0 < ai < 1 or not 0 < base < 1:
            continue
        rows.append((base, ai, 1.0 if r["result"] == "won" else 0.0, r.get("verdict", "")))
    if len(rows) < MIN_PICKS:
        return None
    briers = {w: sum(((1 - w) * b + w * a - y) ** 2 for b, a, y, _ in rows) / len(rows)
              for w in weights}
    gains = [(b - y) ** 2 - ((1 - live_weight) * b + live_weight * a - y) ** 2
             for b, a, y, _ in rows]
    gain, gain_se = _mean_se(gains)
    xs = [a - b for b, a, y, _ in rows]
    ys = [y - b for b, a, y, _ in rows]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    corr = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(sxx * syy)
            if sxx > 0 and syy > 0 else 0.0)
    verdicts = {}
    for b, a, y, v in rows:
        verdicts.setdefault(v or "?", []).append(y - b)
    return {"n": len(rows), "brier": briers, "live_weight": live_weight,
            "gain": gain, "gain_se": gain_se, "corr": corr, "corr_se": 1 / math.sqrt(len(rows)),
            "verdicts": {v: (len(d), sum(d) / len(d)) for v, d in verdicts.items()}}


def book_lead_lag(odds_dir, closing_rows, power_devig):
    """Per bookmaker: error of its first-seen h2h chance against the closing power chance.
    Returns {"books": [(book, n, bias, rmse)], "n_matches", "pinnacle": rmse, "mean_all": rmse,
    "paired_gain", "paired_se"} or None when too little data."""
    close = {}
    for r in closing_rows:
        power = _f(r.get("close_power"))
        if r.get("market") == "h2h" and power is not None:
            close[(r["event_id"], r["sel"])] = power
    snaps = {}
    for path in sorted(glob.glob(str(Path(odds_dir) / "*.json.gz"))):
        try:
            with gzip.open(path, "rt") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        for event in data.get("events", []):
            snaps.setdefault(event["id"], event)  # the earliest snapshot we hold
    per_book, matches = {}, []
    for (eid, sel), truth in close.items():
        event = snaps.get(eid)
        if not event:
            continue
        chances = {}
        for book, markets in event.get("books", {}).items():
            h2h = markets.get("h2h")
            if not h2h or len(h2h) < 2:
                continue
            try:
                probs = power_devig([x[2] for x in h2h])
            except (ValueError, ZeroDivisionError, TypeError):
                continue
            for x, p in zip(h2h, probs):
                if x[0] == sel:
                    chances[book] = p
                    per_book.setdefault(book, []).append(p - truth)
        if "pinnacle" in chances and len(chances) >= 3:
            matches.append((truth, chances))
    if len(matches) < MIN_MATCHES:
        return None
    books = []
    for book, errs in per_book.items():
        if len(errs) >= MIN_MATCHES:
            books.append((book, len(errs), sum(errs) / len(errs),
                          math.sqrt(sum(e * e for e in errs) / len(errs))))
    books.sort(key=lambda b: b[3])
    pin = [abs(c["pinnacle"] - t) for t, c in matches]
    avg = [abs(sum(c.values()) / len(c) - t) for t, c in matches]
    gain, gain_se = _mean_se([p - a for p, a in zip(pin, avg)])
    rms = lambda v: math.sqrt(sum(x * x for x in v) / len(v))  # noqa: E731
    return {"books": books, "n_matches": len(matches), "pinnacle": rms(pin),
            "mean_all": rms(avg), "paired_gain": gain, "paired_se": gain_se}


def _judge(ai):
    if ai["gain"] > 2 * ai["gain_se"]:
        return "The AI shift helps"
    if ai["gain"] < -2 * ai["gain_se"]:
        return "The AI shift hurts"
    return "No measurable benefit from the AI shift yet"


def go_no_go(stats, min_scored=20):
    """Real-money readout from scoreboard stats: NO-GO unless a strategy with enough scored
    bets has an always-valid 'beats the tax' verdict. Also gives, for the best strategy by
    mean, the bets still needed to detect its current edge (z=1.96) when that edge is positive."""
    rows = [(k, v) for k, v in (stats or {}).items()
            if v.get("scored", 0) >= min_scored and v.get("mean") is not None and v.get("se")]
    if not rows:
        return {"go": False, "best": None, "winners": [], "needed": None,
                "text": f"NO-GO: no strategy has {min_scored} scored bets yet."}
    winners = sorted(k for k, v in rows if v["verdict"] == "beats the tax")
    name, v = max(rows, key=lambda kv: kv[1]["mean"])
    needed = None
    if v["mean"] > 0:
        sd = v["se"] * math.sqrt(v["scored"])
        needed = int(math.ceil((1.96 * sd / v["mean"]) ** 2))
    text = (f"GO candidate: {', '.join(winners)} beats the tax at an always-valid test; "
            "still the owner's decision, paper mode stays on." if winners else
            f"NO-GO: none of {len(rows)} strategies with {min_scored}+ scored bets beats the tax; "
            f"best is {name} at {v['mean'] * 100:+.1f}% after tax on {v['scored']} bets"
            + (f" (about {needed} bets to confirm that edge)." if needed else " (negative)."))
    return {"go": bool(winners), "best": name, "winners": winners, "needed": needed, "text": text}


def bankroll_sim(ledger_rows, tax=0.15, start=400.0, stake_pct=25.0, min_stake=50.0,
                 horizon=30, runs=4000, seed=7, min_tickets=10):
    """Monte Carlo of the owner's money if he followed the ticket rule for real: tickets are
    resampled (with replacement) from the settled paper/real ledger as (won, total odds),
    stake = max(min_stake, stake_pct% of bankroll), win pays stake x (odds-1) after tax on
    the profit. Returns the median bankroll after `horizon` tickets, the chance of ending
    below the start and the chance of ever dropping below the minimum stake (cannot bet)."""
    import random
    pool = []
    for r in ledger_rows:
        res, odds = (r.get("result") or "").strip(), _f(r.get("total_odds"))
        if res in ("won", "lost") and odds and odds > 1:
            pool.append((res == "won", odds))
    if len(pool) < min_tickets:
        return None
    rng = random.Random(seed)
    finals, broke = [], 0
    for _ in range(runs):
        bank, hit = start, False
        for _ in range(horizon):
            if bank < min_stake:
                hit = True
                break
            stake = max(min_stake, bank * stake_pct / 100.0)
            won, odds = rng.choice(pool)
            bank += stake * (odds - 1) * (1 - tax) if won else -stake
        broke += hit or bank < min_stake
        finals.append(bank)
    finals.sort()
    return {"tickets": len(pool), "win_rate": sum(w for w, _ in pool) / len(pool),
            "median": finals[len(finals) // 2], "p_below_start": sum(f < start for f in finals) / runs,
            "p_broke": broke / runs, "horizon": horizon, "start": start}


def markdown(ai, lead, gng=None, sim=None):
    out = ["# Standing audits", "", "Built by audit.py from recorded data; nothing here changes "
           "a recorded result.", ""]
    if gng:
        out += ["## Real-money go / no-go", "", gng["text"], ""]
    if sim:
        out += ["## If the owner bet this ticket rule for real", "",
                f"Resampling the {sim['tickets']} settled tickets (win rate {sim['win_rate']*100:.0f}%) "
                f"at the live stake rule from a bankroll of {sim['start']:.0f}: after {sim['horizon']} "
                f"tickets the median bankroll is {sim['median']:.0f}, {sim['p_below_start']*100:.0f}% of "
                f"runs end below the start and {sim['p_broke']*100:.0f}% fall under the minimum stake "
                "(cannot place another ticket). Small sample, so read it as a rough guide to the "
                "size of the swings, not a forecast.", ""]
    out.append("## Does the AI add anything to the sharp chance?")
    if ai is None:
        out += ["", f"Fewer than {MIN_PICKS} settled picks with an AI chance.", ""]
    else:
        out += ["", f"{ai['n']} settled picks. Brier score (lower is better) of the sharp chance "
                "shifted toward the AI's chance by weight w:", "",
                "| w | Brier |", "|---|---|"]
        out += [f"| {w:.2f} | {b:.5f} |" for w, b in sorted(ai["brier"].items())]
        out += ["", f"Live weight {ai['live_weight']:.2f} vs 0: Brier gain "
                f"{ai['gain'] * 1e4:+.1f} +- {ai['gain_se'] * 1e4:.1f} (x0.0001; positive means "
                f"the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp "
                f"chance): {ai['corr']:+.3f} +- {ai['corr_se']:.3f}. {_judge(ai)}.", "",
                "Won minus sharp chance by verdict (picks, mean): "
                + ", ".join(f"{v} {m * 100:+.1f} points ({n})"
                            for v, (n, m) in sorted(ai["verdicts"].items())), ""]
    out.append("## Which bookmaker's first price best predicts Pinnacle's closing chance?")
    if lead is None:
        out += ["", f"Fewer than {MIN_MATCHES} matches with both an archived price and a "
                "closing capture.", ""]
    else:
        out += ["", f"{lead['n_matches']} match sides. RMSE of the first-seen chance against the "
                f"closing power chance: Pinnacle {lead['pinnacle']:.4f}, average of all books "
                f"{lead['mean_all']:.4f}; paired absolute-error gain of the average over "
                f"Pinnacle {lead['paired_gain']:+.4f} +- {lead['paired_se']:.4f}.", "",
                "| Bookmaker | Matches | Bias | RMSE |", "|---|---|---|---|"]
        out += [f"| {b} | {n} | {bias:+.4f} | {rmse:.4f} |" for b, n, bias, rmse in lead["books"]]
        out.append("")
    return "\n".join(out)


def write(data_dir=None, ai_weight=0.2):
    data_dir = Path(data_dir or ROOT / "data")
    try:
        from bot import power_devig
    except Exception:  # noqa: BLE001 - bot needs its environment; the AI part works without it
        power_devig = None
    ai = ai_audit(_read(data_dir / "picks.csv"), live_weight=ai_weight)
    lead = (book_lead_lag(data_dir / "odds", _read(data_dir / "closing.csv"), power_devig)
            if power_devig else None)
    gng = None
    try:
        import scoreboard
        tax = json.loads((ROOT / "config.json").read_text())["tax_rate"]
        stats = scoreboard.build(_read(data_dir / "shadow.csv"), _read(data_dir / "closing.csv"),
                                 tax, None, _read(data_dir / "picks.csv"))[0]
        gng = go_no_go(stats)
    except Exception:  # noqa: BLE001 - the readout is optional
        gng = None
    sim = None
    try:
        cfg = json.loads((ROOT / "config.json").read_text())
        sim = bankroll_sim(_read(data_dir / "ledger.csv"), cfg["tax_rate"], cfg["starting_bankroll"],
                           cfg["stake_percent"], cfg["min_stake"])
    except Exception:  # noqa: BLE001 - optional
        sim = None
    text = markdown(ai, lead, gng, sim)
    (data_dir / "audit.md").write_text(text)
    return ai, lead, text


def email_line(ai):
    """One sentence for the email; empty when there is no audit."""
    if not ai:
        return ""
    return (f"<p><small>AI check: on {ai['n']} settled picks the AI's shift of the market "
            f"chance: {_judge(ai).lower()} (accuracy gain {ai['gain'] * 1e4:+.1f} +- "
            f"{ai['gain_se'] * 1e4:.1f}, in units of 0.0001).</small></p>")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    print(write()[2])
