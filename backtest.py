#!/usr/bin/env python3
"""Historical backtest of the bot's selection rules on football-data.co.uk prices.

The live logs grow by one ticket a day, so they need months to say anything. This script
replays the bot's rules on years of European football instead: each match day becomes a
"slate", candidates are built the way the bot builds them, and the bot's own build_ticket()
(same config: legs 1.20-2.00, at most 3 legs, total 2.50-3.50) chooses the ticket.
Results are settled from the real scores and taxed like the owner's tickets.

Prices (football-data.co.uk columns):
  price  = market average (AvgH/AvgD/AvgA, Avg>2.5/Avg<2.5), the closest thing to "a normal
           bookmaker" (the owner's Megawin is not in any feed)
  fair   = Pinnacle with its margin removed (PSH.., P>2.5..), as the bot uses
  best   = market maximum (MaxH.., Max>2.5..), for the value strategies, ignored (no best
           price) when more than 10% above the average, as the live bot's best_offer() does:
           without that cap the maximum is full of stale or erroneous prices and every value
           rule looks hugely profitable (+16% after tax), which no bettor could collect
"close" uses the closing columns (AvgCH, PSCH, ...), nearest to when the bot bets on the
morning of the match; "open" uses the earlier columns (collected a few days before).

Usage:
  python backtest.py --dir <folder with csv files>      (any layout, searched recursively)
  python backtest.py --fetch                            (downloads from football-data.co.uk)
  options: --seasons 2122,2223,2324,2425,2526  --timing close|open  --out data/backtest
Writes <out>/report.md and <out>/summary.json. Standard library only.
"""
import argparse
import csv
import io
import json
import math
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import bot

ROOT = Path(__file__).resolve().parent
LEAGUES = ["E0", "E1", "E2", "SC0", "SC1", "D1", "D2", "SP1", "SP2", "I1", "I2", "F1", "F2",
           "N1", "B1", "P1", "T1"]
URL = "https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
TAX = bot.CONFIG["tax_rate"]
BEST_CAP = 1.10  # same outlier cap as bot.best_offer()


# ------------------------------------------------------------- loading ----
def num(row, key):
    try:
        v = float(row.get(key) or "")
    except ValueError:
        return None
    return v if v > 1 else None


def parse_date(text):
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def read_rows(text, source=""):
    text = text.lstrip("﻿")
    out = []
    for row in csv.DictReader(io.StringIO(text)):
        row = {(k or "").strip(): (v or "").strip() for k, v in row.items()
               if k is not None and isinstance(v, (str, type(None)))}
        if not row.get("HomeTeam") or row.get("FTHG", "") == "":
            continue
        date = parse_date(row.get("Date", ""))
        if not date:
            continue
        try:
            hg, ag = int(float(row["FTHG"])), int(float(row["FTAG"]))
        except (KeyError, ValueError):
            continue
        row.update(_date=date, _hg=hg, _ag=ag, _src=source)
        out.append(row)
    return out


def load_dir(folder, seasons=None):
    rows = []
    for path in sorted(Path(folder).rglob("*.csv")):
        if seasons and not any(s in path.name for s in seasons):
            continue
        try:
            rows.extend(read_rows(path.read_text(encoding="utf-8", errors="replace"), path.name))
        except csv.Error:
            continue
    return rows


def load_web(seasons):
    rows = []
    for season in seasons:
        for league in LEAGUES:
            url = URL.format(season=season, league=league)
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    text = r.read().decode("utf-8", errors="replace")
            except Exception as exc:  # noqa: BLE001 - a missing league is not fatal
                print(f"skip {url}: {exc}", file=sys.stderr)
                continue
            rows.extend(read_rows(text, f"{season}-{league}"))
    return rows


# ---------------------------------------------------------- candidates ----
def devig(prices):
    if not all(prices):
        return None
    total = sum(1 / p for p in prices)
    return [(1 / p) / total for p in prices]


def devig_power(prices):
    if not all(prices):
        return None
    return bot.power_devig(prices)


def match_candidates(row, idx, timing="close"):
    """Candidate bets of one match, in the bot's candidate format (plus 'won' and 'best')."""
    c = "C" if timing == "close" else ""
    hg, ag = row["_hg"], row["_ag"]
    eid = f"{row['_src']}-{idx}"
    start = f"{row['_date']}T{row.get('Time') or '15:00'}:00Z"
    out = []

    def add(market, sel, point, prob, odds, best, won, ppow=None):
        if prob is None or odds is None:
            return
        if best and best > odds * BEST_CAP:
            best = None
        out.append({"event_id": eid, "start": start, "market": market, "sel": sel,
                    "point": point, "odds": round(odds, 2), "prob": prob,
                    "prob_power": ppow if ppow is not None else prob,
                    "best": round(best, 2) if best else None, "won": won,
                    "league": row.get("Div", row["_src"]),
                    "match": f"{row['HomeTeam']} v {row['AwayTeam']}"})

    avg = [num(row, f"Avg{c}{s}") for s in "HDA"]
    mx = [num(row, f"Max{c}{s}") for s in "HDA"]
    fair = devig([num(row, f"PS{c}{s}") for s in "HDA"])
    fpow = devig_power([num(row, f"PS{c}{s}") for s in "HDA"])
    if fair and all(avg):
        res = "H" if hg > ag else "A" if ag > hg else "D"
        for i, s in enumerate("HDA"):
            add("h2h", s, None, fair[i], avg[i], mx[i], res == s, fpow[i])
        wins = {"1X": "HD", "X2": "AD", "12": "HA"}
        for sel, (x, y) in {"1X": (0, 1), "X2": (2, 1), "12": (0, 2)}.items():
            add("dc", sel, None, fair[x] + fair[y], 0.97 / (1 / avg[x] + 1 / avg[y]), None,
                res in wins[sel], fpow[x] + fpow[y])
    over, under = num(row, f"Avg{c}>2.5"), num(row, f"Avg{c}<2.5")
    pfair = devig([num(row, f"P{c}>2.5"), num(row, f"P{c}<2.5")])
    ppow = devig_power([num(row, f"P{c}>2.5"), num(row, f"P{c}<2.5")])
    if pfair and over and under:
        goals = hg + ag
        add("totals", "Over", 2.5, pfair[0], over, num(row, f"Max{c}>2.5"), goals > 2.5,
            ppow[0])
        add("totals", "Under", 2.5, pfair[1], under, num(row, f"Max{c}<2.5"), goals < 2.5,
            ppow[1])
    return out


def slates(rows, timing="close"):
    days = defaultdict(list)
    for i, row in enumerate(rows):
        days[row["_date"]].extend(match_candidates(row, i, timing))
    return dict(sorted(days.items()))


# ---------------------------------------------------------- strategies ----
def in_band(c):
    return bot.CONFIG["min_leg_odds"] <= c["odds"] <= bot.CONFIG["max_leg_odds"]


def edge_ticket(cands):
    """Allowed ticket with the best expected return (chance x odds), the edge_first rule."""
    pool = sorted(cands, key=lambda c: c["prob"] * c["odds"], reverse=True)[:30]
    best, best_ev = None, 0
    lo, hi, legs = (bot.CONFIG["min_total_odds"], bot.CONFIG["max_total_odds"],
                    bot.CONFIG["max_legs"])
    from itertools import combinations
    for size in range(1, legs + 1):
        for combo in combinations(pool, size):
            if len({c["event_id"] for c in combo}) < size:
                continue
            odds = math.prod(c["odds"] for c in combo)
            if lo <= odds <= hi:
                ev = math.prod(c["prob"] * c["odds"] for c in combo)
                if ev > best_ev:
                    best, best_ev = combo, ev
    return list(best) if best else None


def with_max_legs(n, fn, cands):
    old = bot.CONFIG["max_legs"]
    bot.CONFIG["max_legs"] = n
    try:
        return fn(cands)
    finally:
        bot.CONFIG["max_legs"] = old


def most_likely(cands):
    t = bot.build_ticket(cands)
    return t["legs"] if t else None


def as_power(cands):
    """Same candidates with the power-method chance as "prob" (power_value/power_ticket)."""
    return [dict(c, prob=c["prob_power"]) for c in cands]


STRATEGIES = {
    # name: (description, function(slate) -> list of tickets, each a list of legs with odds)
    "most_likely": ("live rule: most likely allowed ticket (code, no AI)",
                    lambda s: [most_likely([c for c in s if in_band(c)])]),
    "most_likely_2": ("same, at most 2 legs",
                      lambda s: [with_max_legs(2, most_likely, [c for c in s if in_band(c)])]),
    "most_likely_no_dc": ("same, double chance not allowed",
                          lambda s: [most_likely([c for c in s if in_band(c)
                                                  and c["market"] != "dc"])]),
    "most_likely_h2h": ("same, match winner only",
                        lambda s: [most_likely([c for c in s if in_band(c)
                                                and c["market"] == "h2h"])]),
    "most_likely_totals": ("same, over/under 2.5 only",
                           lambda s: [most_likely([c for c in s if in_band(c)
                                                   and c["market"] == "totals"])]),
    "edge_first": ("allowed ticket with the best chance x odds (edge_first shadow)",
                   lambda s: [edge_ticket([c for c in s if in_band(c)])]),
    "best_single": ("one single a day: least negative edge at the average price, 1.20-2.00",
                    lambda s: [[max((c for c in s if in_band(c)),
                                    key=lambda c: c["prob"] * c["odds"], default=None)]]),
    "value_single": ("every single where the best price is 2%+ above Pinnacle fair (<= 4.00)",
                     lambda s: [[dict(c, odds=c["best"])] for c in s
                                if c["best"] and c["best"] <= 4.0
                                and c["market"] != "dc" and c["prob"] * c["best"] >= 1.02]),
    "most_likely_best": ("the live rule's ticket, each leg at the best price (price shopping)",
                         lambda s: [at_best(most_likely([c for c in s if in_band(c)]))]),
    "best_single_best": ("best_single at the best price",
                         lambda s: [at_best([max((c for c in s if in_band(c)
                                                  and c["market"] != "dc"),
                                                 key=lambda c: c["prob"] * c["odds"],
                                                 default=None)])]),
    "value_taxed": ("singles at the best price with positive expected profit after tax",
                    lambda s: [[dict(c, odds=c["best"])] for c in s
                               if c["best"] and c["best"] <= 4.0 and c["market"] != "dc"
                               and taxed_ev(c, c["best"]) > 0]),
    "most_likely_power": ("live rule with power-method chances (power_ticket shadow)",
                          lambda s: [most_likely(as_power([c for c in s if in_band(c)]))]),
    "value_taxed_power": ("tax-proof singles at the best price, power-method chance "
                          "(power_value shadow)",
                          lambda s: [[dict(c, odds=c["best"])] for c in as_power(s)
                                     if c["best"] and c["best"] <= 4.0 and c["market"] != "dc"
                                     and c["best"] >= 1.05 and taxed_ev(c, c["best"]) > 0]),
    "value_single_4": ("same with 4%+ value",
                       lambda s: [[dict(c, odds=c["best"])] for c in s
                                  if c["best"] and c["best"] <= 4.0
                                  and c["market"] != "dc" and c["prob"] * c["best"] >= 1.04]),
}


def season_of(date):
    """Football season label, e.g. 2025-08-01 -> 2526 (seasons start in July)."""
    y, m = int(date[:4]), int(date[5:7])
    start = y if m >= 7 else y - 1
    return f"{start % 100:02d}{(start + 1) % 100:02d}"


def settle(legs, stake=1.0, tax=TAX):
    """Net profit of one ticket after the 15% tax on winnings."""
    odds = math.prod(c["odds"] for c in legs)
    if all(c["won"] for c in legs):
        return (stake * odds - stake) * (1 - tax)
    return -stake


def taxed_ev(c, odds=None):
    """Expected profit per unit of a single after the tax on winnings."""
    o = odds or c["odds"]
    return c["prob"] * (o - 1) * (1 - TAX) - (1 - c["prob"])


def at_best(legs):
    if not legs or any(c is None for c in legs):
        return None
    return [dict(c, odds=c["best"] or c["odds"]) for c in legs]


def run(days, names=None):
    out = {}
    for name in names or STRATEGIES:
        desc, fn = STRATEGIES[name]
        bets, profit, wins, exp_wins, exp_ret, odds_sum, sq = 0, 0.0, 0, 0.0, 0.0, 0.0, 0.0
        pre_tax = 0.0
        seasons = defaultdict(lambda: [0, 0.0])
        for slate in days.values():
            for legs in fn(slate):
                if not legs or any(c is None for c in legs):
                    continue
                p = settle(legs)
                pre_tax += settle(legs, tax=0)
                g = seasons[season_of(legs[0]["start"][:10])]
                g[0] += 1
                g[1] += p
                bets += 1
                profit += p
                sq += p * p
                wins += all(c["won"] for c in legs)
                chance = math.prod(c["prob"] for c in legs)
                odds = math.prod(c["odds"] for c in legs)
                exp_wins += chance
                exp_ret += chance * (odds - 1) * (1 - TAX) - (1 - chance)
                odds_sum += odds
        if not bets:
            out[name] = {"desc": desc, "bets": 0}
            continue
        mean = profit / bets
        sd = math.sqrt(max(sq / bets - mean * mean, 0))
        out[name] = {"desc": desc, "bets": bets, "wins": wins,
                     "hit": round(wins / bets, 4), "exp_hit": round(exp_wins / bets, 4),
                     "avg_odds": round(odds_sum / bets, 2), "roi": round(mean, 4),
                     "roi_pre_tax": round(pre_tax / bets, 4),
                     "by_season": {k: round(v[1] / v[0], 4) for k, v in sorted(seasons.items())},
                     "se": round(sd / math.sqrt(bets), 4), "exp_roi": round(exp_ret / bets, 4)}
    return out


def leg_table(days):
    """ROI of every single candidate at the average price, by market and odds band."""
    bands = [(1.2, 1.4), (1.4, 1.6), (1.6, 1.8), (1.8, 2.0), (2.0, 3.0), (3.0, 6.0)]
    agg = defaultdict(lambda: [0, 0.0, 0.0, 0])
    for slate in days.values():
        for c in slate:
            band = next((b for b in bands if b[0] <= c["odds"] < b[1]), None)
            if not band:
                continue
            g = agg[(c["market"], f"{band[0]:.2f}-{band[1]:.2f}")]
            g[0] += 1
            g[1] += (c["odds"] - 1) if c["won"] else -1  # untaxed single, stake 1
            g[2] += c["prob"] * c["odds"] - 1
            g[3] += c["won"]
    return {f"{m} {b}": {"n": n, "roi": round(r / n, 4), "pinnacle_edge": round(e / n, 4),
                         "hit": round(w / n, 4)}
            for (m, b), (n, r, e, w) in sorted(agg.items()) if n >= 50}


def report(results, legs, meta):
    lines = [f"# Historical backtest ({meta['timing']} prices)", "",
             f"{meta['matches']} matches on {meta['days']} match days, seasons "
             f"{', '.join(meta['seasons'])}, leagues: {meta['leagues']}. Data: "
             "football-data.co.uk (Joseph Buchdahl). Re-run: `python backtest.py --fetch`.",
             "Price = market average; fair chance = Pinnacle without margin; tickets taxed "
             "15% on winnings; stake 1 per ticket. ROI is profit per unit staked, se its "
             "standard error. exp_roi is what Pinnacle's chances predicted.", "",
             "| strategy | bets | hit | expected hit | avg odds | ROI | se | expected ROI | ROI before tax |",
             "|---|---|---|---|---|---|---|---|---|"]
    for name, r in results.items():
        if not r["bets"]:
            lines.append(f"| {name} | 0 | | | | | | | |")
            continue
        lines.append(f"| {name} | {r['bets']} | {r['hit']:.1%} | {r['exp_hit']:.1%} | "
                     f"{r['avg_odds']:.2f} | {r['roi']:+.1%} | {r['se']:.1%} | "
                     f"{r['exp_roi']:+.1%} | {r['roi_pre_tax']:+.1%} |")
    lines += ["", "ROI after tax by season:", "",
              "| strategy | " + " | ".join(meta["seasons"]) + " |",
              "|---|" + "---|" * len(meta["seasons"])]
    for name, r in results.items():
        if r["bets"]:
            lines.append(f"| {name} | " + " | ".join(
                f"{r['by_season'][x]:+.0%}" if x in r["by_season"] else "" for x in meta["seasons"])
                + " |")
    lines += ["", "Strategies:", ""]
    lines += [f"- {n}: {r['desc']}" for n, r in results.items()]
    lines += ["", "## Single legs at the average price (no tax)", "",
              "| market, odds band | n | hit | ROI | Pinnacle edge |", "|---|---|---|---|---|"]
    for k, v in legs.items():
        lines.append(f"| {k} | {v['n']} | {v['hit']:.1%} | {v['roi']:+.1%} | "
                     f"{v['pinnacle_edge']:+.1%} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--seasons", default="2122,2223,2324,2425,2526")
    ap.add_argument("--timing", default="close", choices=["close", "open"])
    ap.add_argument("--out", default=str(ROOT / "data" / "backtest"))
    args = ap.parse_args(argv)
    seasons = [s.strip() for s in args.seasons.split(",") if s.strip()]
    if args.dir:
        # Mirrors name files e.g. season-2425.csv; football-data names them by league.
        rows = load_dir(args.dir, [f"season-{s}" for s in seasons]) or load_dir(args.dir)
    elif args.fetch:
        rows = load_web(seasons)
    else:
        ap.error("give --dir or --fetch")
    days = slates(rows, args.timing)
    results = run(days)
    legs = leg_table(days)
    meta = {"timing": args.timing, "seasons": seasons, "matches": len(rows), "days": len(days),
            "leagues": len({r.get("Div", r["_src"]) for r in rows})}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.timing == "close" else "_open"
    (out / f"report{suffix}.md").write_text(report(results, legs, meta))
    (out / f"summary{suffix}.json").write_text(json.dumps(
        {"meta": meta, "strategies": results, "legs": legs}, indent=1))
    print(report(results, legs, meta))


if __name__ == "__main__":
    main()
