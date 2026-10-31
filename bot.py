#!/usr/bin/env python3
"""Daily betting ticket bot.

Every morning (Skopje time) it:
  1. settles open tickets from the scores feed and updates the bankroll,
  2. builds one new combined ticket from that day's odds,
  3. emails the result of yesterday and the ticket for today,
  4. saves everything to data/state.json and data/ledger.csv.

Only the Python standard library is used.
"""
import csv
import re
import html as html_lib
import itertools
import json
import os
import smtplib
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text())
STATE_PATH = ROOT / "data" / "state.json"
LEDGER_PATH = ROOT / "data" / "ledger.csv"
PICKS_PATH = ROOT / "data" / "picks.csv"
CLOSING_PATH = ROOT / "data" / "closing.csv"
CLOSING_BUDGET_PATH = ROOT / "data" / "closing_budget.json"
CLOSING_FIELDS = ["date", "event_id", "sport_key", "match", "market", "sel", "point", "pick",
                  "start", "on_ticket", "captured", "minutes_before", "open_odds",
                  "open_consensus", "open_sharp", "close_odds", "close_consensus",
                  "close_sharp", "close_book", "clv", "move"]
LESSONS_PATH = ROOT / "prompts" / "lessons.md"
LEDGER_FIELDS = ["ticket_no", "date", "picks", "total_odds", "stake", "result", "payout", "tax",
                 "net_profit", "bankroll_after", "mode"]
PICK_FIELDS = ["date", "ticket_no", "mode", "event_id", "sport_key", "sport", "league", "match",
               "start", "market", "sel", "point", "pick", "odds", "market_chance", "verdict",
               "ai_chance", "on_ticket", "result", "score", "consensus_chance", "sharp_chance",
               "sharp_book", "edge"]
# Bookmakers whose prices are the most accurate (low margin, sharp customers allowed), best
# first. Their margin-free price is used as the fair chance when they carry the bet.
SHARP_BOOKS = ["pinnacle", "betfair_ex_eu", "matchbook"]
API = "https://api.the-odds-api.com/v4"
TZ = ZoneInfo(CONFIG["timezone"])
SPORT_NAMES = {"soccer": "Football", "basketball": "Basketball",
               "tennis": "Tennis", "handball": "Handball"}

credits_left = None  # filled from the API response headers
key_index = 0  # which Odds API key is in use
AI_LOG = []  # what happened in each Gemini call, kept for previews
SCOUTED = []  # event ids the AI scout chose today, safest first
SCOUT_NOTE = ""
SCOUT_EXTRA = ""  # matches the scout found outside the feed, as HTML
RESEARCH = {}  # today's research notes and raw AI decision, saved for the review task
LAST_SHORT = None  # (shortlist, chosen ids) from the latest AI decision
SCORES = {}  # final scores fetched during this run, by event id
MODELS_OUT = set()  # (key number, model) pairs that stopped working during this run


# ---------------------------------------------------------------- API ----
def odds_keys():
    """All configured Odds API keys, in the order they should be tried."""
    names = ["ODDS_API_KEY"] + [f"ODDS_API_KEY_{n}" for n in range(2, 10)]
    keys = [os.environ.get(name, "").strip() for name in names]
    return [k for k in dict.fromkeys(keys) if k]


def api_get(path, **params):
    """GET a JSON document from The Odds API.

    Tries each configured key in turn: when one is refused or out of requests, the bot
    moves to the next and stays on it for the rest of the run.
    """
    global credits_left, key_index
    keys = odds_keys()
    if not keys:
        raise SystemExit("No Odds API key is set.")
    attempt = 0
    while key_index < len(keys):
        params["apiKey"] = keys[key_index]
        url = f"{API}{path}?{urllib.parse.urlencode(params)}"
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                remaining = resp.headers.get("x-requests-remaining")
                if remaining is not None:
                    credits_left = int(float(remaining))
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as err:
            detail = err.read().decode()[:300]
            out_of_credits = "OUT_OF_USAGE_CREDITS" in detail or "quota" in detail.lower()
            if err.code == 429 and not out_of_credits and attempt < 3:
                attempt += 1
                time.sleep(2 + 2 * attempt)  # short-term rate limit: wait and retry
                continue
            if err.code in (401, 403, 429):
                print(f"Odds API key {key_index + 1} of {len(keys)} is unavailable "
                      f"({err.code}); trying the next one.")
                key_index += 1
                attempt = 0
                continue
            if err.code in (404, 422):
                return []
            raise
        except urllib.error.URLError:
            attempt += 1
            if attempt > 3:
                raise
            time.sleep(3)
    raise SystemExit("Every Odds API key was refused or is out of requests.")


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_time(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def sport_of(key):
    return key.split("_", 1)[0]


# ------------------------------------------------------------- picking ----
def all_fixtures(start, end):
    """Every match in the window across all covered leagues (free endpoints only)."""
    sports = api_get("/sports")
    active = [s["key"] for s in sports
              if s.get("active") and not s.get("has_outrights")
              and s["key"].startswith(tuple(CONFIG["sport_prefixes"]))
              and not any(word in s["key"] for word in CONFIG["skip_keys_containing"])]
    priority = [k for k in CONFIG["priority_keys"] if k in active]
    fixtures = []
    for key in priority + sorted(k for k in active if k not in priority):
        fixtures.extend(api_get(f"/sports/{key}/events",
                                commenceTimeFrom=iso(start), commenceTimeTo=iso(end)))
        time.sleep(0.15)
    return fixtures


def default_keys(fixtures):
    """Leagues to price when the AI scout is unavailable: every sport gets a turn."""
    by_sport = {}
    for event in fixtures:
        keys = by_sport.setdefault(sport_of(event["sport_key"]), [])
        if event["sport_key"] not in keys:
            keys.append(event["sport_key"])
    result = []
    queues = [by_sport[s] for s in ("soccer", "basketball", "tennis", "handball") if s in by_sport]
    while any(queues):
        for queue in queues:
            if queue:
                result.append(queue.pop(0))
    return result[:CONFIG["max_odds_requests_per_day"]]


def ai_scout(fixtures, today):
    """Ask Gemini to go through the whole day's fixtures and name the safest matches.

    Returns the chosen event ids, safest first. The AI can only point at fixtures from the
    feed; anything else in its answer is ignored.
    """
    global SCOUT_NOTE, SCOUT_EXTRA
    fixtures = sorted(fixtures, key=lambda e: (e["sport_key"], e["commence_time"]))[:400]
    if not fixtures or not gemini_keys():
        return []
    listing = "\n".join(
        f"F{i}: {SPORT_NAMES.get(sport_of(e['sport_key']), '')}, "
        f"{e.get('sport_title', e['sport_key'])}: {e['home_team']} (home) v {e['away_team']} "
        f"(away), {local_time(e['commence_time'])}"
        for i, e in enumerate(fixtures, 1))
    text = gemini((ROOT / "prompts" / "scout.txt").read_text().format(
        today=f"{today:%A %d %B %Y, %H:%M}", fixtures=listing, lessons=lessons(),
        max_leagues=CONFIG["max_odds_requests_per_day"]), search=True)
    tail = text.rsplit("PICKS:", 1)[-1] if "PICKS:" in text else ""
    extras = [html_lib.escape(line.strip()[1:].strip(" |"))
              for line in text.splitlines() if re.match(r"\s*X\s*\|", line)][:5]
    SCOUT_EXTRA = ("<h3>Other matches the AI found</h3><p style='font-size:14px'>"
                   + "<br>".join(extras) + "</p><p><small>These are not in the odds feed, so "
                   "they are not on the ticket and not tracked. Nothing here was verified: "
                   "check the match and the odds at your bookmaker yourself.</small></p>"
                   ) if extras else ""
    ids, keys = [], []
    for number in re.findall(r"F\s*(\d+)", tail):
        index = int(number)
        if not 1 <= index <= len(fixtures):
            continue
        event = fixtures[index - 1]
        if event["sport_key"] not in keys:
            if len(keys) >= CONFIG["max_odds_requests_per_day"]:
                continue
            keys.append(event["sport_key"])
        if event["id"] not in ids:
            ids.append(event["id"])
    SCOUT_NOTE = (f"The AI went through {len(fixtures)} matches on offer today and chose "
                  f"{len(ids)} as the safest candidates." if ids else
                  f"The AI scout named no matches out of {len(fixtures)}; "
                  "the most likely favourites were researched instead.")
    return ids


def candidates_from_event(event, strict=True):
    """Turn one event into candidate bets with a fair chance for each.

    Covers match winner, double chance (derived from the win/draw/win prices), totals and,
    for basketball, handicaps. For each bookmaker the margin is removed by normalising the
    implied probabilities; the result is averaged across bookmakers ("consensus").
    When a sharp bookmaker (see SHARP_BOOKS) prices the bet, its margin-free chance is used
    as "prob" instead, because sharp prices predict results better than the soft average.
    "edge" is how much the average price pays above that fair chance (prob x odds - 1).
    With strict=False the bookmaker-count and odds-range filters are skipped (used to read
    closing prices, where only matching an earlier bet matters).
    """
    sport = sport_of(event["sport_key"])
    home, away = event["home_team"], event["away_team"]
    unit = "goals" if sport in ("soccer", "handball") else "points"
    groups = {}

    def add(market, sel, point, prob, price):
        g = groups.setdefault((market, sel, point), {"probs": [], "prices": [], "sharp": {}})
        if bkey in SHARP_BOOKS:
            g["sharp"][bkey] = prob
        g["probs"].append(prob)
        g["prices"].append(price)

    for book in event.get("bookmakers", []):
        bkey = book.get("key", "")
        for market in book.get("markets", []):
            outs = [o for o in market.get("outcomes", []) if o.get("price", 0) > 1]
            if len(outs) < 2:
                continue
            total = sum(1 / o["price"] for o in outs)
            fair = {o["name"]: (1 / o["price"]) / total for o in outs}
            price = {o["name"]: o["price"] for o in outs}
            if market["key"] == "h2h":
                for name in fair:
                    add("h2h", name, None, fair[name], price[name])
                if len(outs) == 3 and {home, away, "Draw"} <= set(fair):
                    # Double chance is not in the feed, so its price is worked out from the
                    # three match prices and cut by 3% to stay on the cautious side.
                    for sel, (x, y) in {"1X": (home, "Draw"), "X2": (away, "Draw"),
                                        "12": (home, away)}.items():
                        add("dc", sel, None, fair[x] + fair[y],
                            0.97 / (1 / price[x] + 1 / price[y]))
            elif market["key"] == "totals" and len(outs) == 2 and sport != "tennis":
                point = outs[0].get("point")
                if point is None or point != outs[1].get("point"):
                    continue
                if sport == "soccer" and point % 1 != 0.5:
                    continue  # quarter and whole lines are not offered by local bookmakers
                for o in outs:
                    add("totals", o["name"], point, fair[o["name"]], o["price"])
            elif market["key"] == "spreads" and len(outs) == 2 and sport == "basketball":
                for o in outs:
                    if o.get("point") is not None:
                        add("spreads", o["name"], o["point"], fair[o["name"]], o["price"])

    labels = {"1X": f"{home} or draw (double chance)", "X2": f"{away} or draw (double chance)",
              "12": "No draw: either team wins (double chance)"}
    out = []
    for (market, sel, point), g in groups.items():
        needed = CONFIG["min_bookmakers"] if market in ("h2h", "dc") else CONFIG["min_bookmakers_lines"]
        if strict and len(g["probs"]) < needed:
            continue
        odds = round(sum(g["prices"]) / len(g["prices"]), 2)
        if strict and not CONFIG["min_leg_odds"] <= odds <= CONFIG["max_leg_odds"]:
            continue
        consensus = sum(g["probs"]) / len(g["probs"])
        sharp_book = next((b for b in SHARP_BOOKS if b in g["sharp"]), "")
        sharp = g["sharp"][sharp_book] if sharp_book else None
        if sharp is not None and abs(sharp - consensus) > 0.10:
            sharp, sharp_book = None, ""  # far from every other book: likely a stale price
        prob = sharp if sharp is not None else consensus
        if market == "h2h":
            pick = "Draw" if sel == "Draw" else f"{sel} to win"
        elif market == "dc":
            pick = labels[sel]
        elif market == "totals":
            pick = f"{sel} {point:g} {unit}"
        else:
            pick = f"{sel} {point:+g} (handicap)"
        out.append({
            "event_id": event["id"],
            "sport_key": event["sport_key"],
            "sport": SPORT_NAMES.get(sport, event["sport_key"]),
            "league": event.get("sport_title", event["sport_key"]),
            "home": home,
            "away": away,
            "start": event["commence_time"],
            "market": market,
            "sel": sel,
            "point": point,
            "pick": pick,
            "odds": odds,
            "prob": prob,
            "consensus": consensus,
            "sharp": sharp,
            "sharp_book": sharp_book,
            "edge": round(prob * odds - 1, 4),
            "books": len(g["probs"]),
            "result": "pending",
        })
    return out


def build_ticket(cands):
    """Most likely combination whose total odds are inside the allowed range."""
    ranked = sorted(cands, key=lambda c: c["prob"], reverse=True)
    # Very short prices alone cannot reach the target, so keep some longer ones in the pool.
    longer = [c for c in ranked if c["odds"] >= 1.45]
    pool = ranked[:25] + [c for c in longer[:25] if c not in ranked[:25]]
    best, best_prob = None, 0
    for size in range(1, CONFIG["max_legs"] + 1):
        for combo in itertools.combinations(pool, size):
            if len({c["event_id"] for c in combo}) < size:
                continue
            odds = 1.0
            prob = 1.0
            for c in combo:
                odds *= c["odds"]
                prob *= c["prob"]
            if CONFIG["min_total_odds"] <= odds <= CONFIG["max_total_odds"] and prob > best_prob:
                best, best_prob = combo, prob
    if not best:
        return None
    legs = sorted((dict(c) for c in best), key=lambda c: c["start"])
    total = 1.0
    for leg in legs:
        total *= leg["odds"]
    return {"legs": legs, "total_odds": round(total, 2), "win_prob": round(best_prob, 4)}


def pick_ticket(now):
    start = now + timedelta(minutes=CONFIG["min_minutes_before_start"])
    local = now.astimezone(TZ)
    hours = CONFIG["last_start_hour_local"]
    end = (local.replace(hour=0, minute=0, second=0, microsecond=0)
           + timedelta(days=1, hours=hours))
    fixtures = all_fixtures(start, end)
    SCOUTED[:] = ai_scout(fixtures, local)
    wanted = [e["sport_key"] for e in fixtures if e["id"] in SCOUTED]
    # Leagues the scout chose first, then others until the daily request budget is used.
    keys = list(dict.fromkeys(wanted + default_keys(fixtures)))
    keys = keys[:CONFIG["max_odds_requests_per_day"]]
    cands = []
    for key in keys:
        markets = CONFIG["markets"].get(sport_of(key), "h2h")
        events = api_get(f"/sports/{key}/odds", regions=CONFIG["region"], markets=markets,
                         oddsFormat="decimal", commenceTimeFrom=iso(start),
                         commenceTimeTo=iso(end))
        for event in events:
            cands.extend(candidates_from_event(event))
    return cands


# ------------------------------------------------------------ settling ----
def stake_for(bankroll):
    """Stake for the next ticket: a share of the available bankroll.

    Rounded to the nearest 10 MKD, never below the minimum stake and never more than
    what is available. Returns 0 when the bankroll is below the minimum.
    """
    if bankroll < CONFIG["min_stake"]:
        return 0
    stake = round(bankroll * CONFIG["stake_percent"] / 100 / 10) * 10
    return min(max(stake, CONFIG["min_stake"]), int(bankroll))


def tax_and_payout(stake, odds):
    """Macedonian rule: 15% of (payout - stake), withheld by the bookmaker."""
    gross = round(stake * odds, 2)
    tax = round(max(gross - stake, 0) * CONFIG["tax_rate"], 2)
    return gross, tax, round(gross - tax, 2)


def leg_result(leg, score):
    if not score or not score.get("completed") or not score.get("scores"):
        return "pending"
    try:
        points = {s["name"]: float(s["score"]) for s in score["scores"]}
        home, away = points[score["home_team"]], points[score["away_team"]]
    except (KeyError, TypeError, ValueError):
        return "pending"
    leg["score"] = f"{home:g}:{away:g}"
    market = leg.get("market", "h2h")
    sel = leg.get("sel") or leg["pick"]
    outcome = "1" if home > away else "2" if away > home else "X"
    if market == "dc":
        return "won" if outcome in sel else "lost"
    if market == "totals":
        diff = home + away - leg["point"]
        if diff == 0:
            return "void"
        return "won" if (diff > 0) == (sel == "Over") else "lost"
    if market == "spreads":
        margin = (home - away if sel == score["home_team"] else away - home) + leg["point"]
        return "void" if margin == 0 else "won" if margin > 0 else "lost"
    winner = {"1": score["home_team"], "2": score["away_team"], "X": "Draw"}[outcome]
    return "won" if sel == winner else "lost"


def fetch_scores(keys):
    """Final scores of the last 3 days for these leagues, each league fetched once a run."""
    for key in sorted(set(keys) - FETCHED_KEYS):
        FETCHED_KEYS.add(key)
        for item in api_get(f"/sports/{key}/scores", daysFrom=3):
            SCORES[item["id"]] = item
    return SCORES


FETCHED_KEYS = set()


def settle(state, now):
    """Check every open ticket. Returns the tickets that reached a final result."""
    finished = []
    open_keys = {leg["sport_key"] for t in state["open_tickets"] for leg in t["legs"]
                 if leg["result"] == "pending"}
    scores = fetch_scores(open_keys)

    still_open = []
    for ticket in state["open_tickets"]:
        age_days = (now - parse_time(ticket["created"])).days
        for leg in ticket["legs"]:
            if leg["result"] == "pending":
                leg["result"] = leg_result(leg, scores.get(leg["event_id"]))
            if leg["result"] == "pending" and age_days >= CONFIG["void_after_days"]:
                leg["result"] = "void"  # postponed or no result: counts as odds 1.00
        results = [leg["result"] for leg in ticket["legs"]]
        if "lost" in results:
            ticket.update(result="lost", payout=0.0, tax=0.0, net_profit=-ticket["stake"])
        elif "pending" in results:
            still_open.append(ticket)
            continue
        else:
            odds = 1.0
            for leg in ticket["legs"]:
                odds *= leg["odds"] if leg["result"] == "won" else 1.0
            ticket["settled_odds"] = round(odds, 2)
            gross, tax, net = tax_and_payout(ticket["stake"], round(odds, 2))
            ticket.update(result="void" if odds == 1.0 else "won", payout=gross, tax=tax,
                          net_profit=round(net - ticket["stake"], 2))
            if not ticket.get("paper"):
                state["bankroll"] = round(state["bankroll"] + net, 2)
        if ticket.get("paper"):
            # Paper tickets never touch the real bankroll; only their running result is kept.
            state["paper_profit"] = round(state.get("paper_profit", 0) + ticket["net_profit"], 2)
            ticket["bankroll_after"] = state["paper_profit"]
        else:
            ticket["bankroll_after"] = state["bankroll"]
        finished.append(ticket)
        append_ledger(ticket)
    state["open_tickets"] = still_open
    return finished


def ledger_rows():
    """All settled tickets. Rows written before paper mode existed count as real."""
    if not LEDGER_PATH.exists():
        return []
    with LEDGER_PATH.open() as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        row["mode"] = row.get("mode") or "real"
    return rows


def append_ledger(ticket):
    picks = " | ".join(f"{l['home']} v {l['away']}: {l['pick']} @{l['odds']} ({l['result']})"
                       for l in ticket["legs"])
    rows = ledger_rows()
    rows.append(dict(zip(LEDGER_FIELDS, [
        ticket["no"], ticket["date"], picks, ticket["total_odds"], ticket["stake"],
        ticket["result"], ticket["payout"], ticket["tax"], ticket["net_profit"],
        ticket["bankroll_after"], "paper" if ticket.get("paper") else "real"])))
    with LEDGER_PATH.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, LEDGER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def ledger_summary(mode="real"):
    rows = [r for r in ledger_rows() if r["mode"] == mode]
    won = sum(1 for r in rows if r["result"] == "won")
    lost = sum(1 for r in rows if r["result"] == "lost")
    return {
        "tickets": len(rows), "won": won, "lost": lost,
        "staked": sum(float(r["stake"]) for r in rows),
        "tax": sum(float(r["tax"]) for r in rows),
        "profit": sum(float(r["net_profit"]) for r in rows),
    }


# ------------------------------------------------------------- pick log ----
def read_picks():
    if not PICKS_PATH.exists():
        return []
    with PICKS_PATH.open() as fh:
        return list(csv.DictReader(fh))


def write_picks(rows):
    with PICKS_PATH.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, PICK_FIELDS, restval="")
        writer.writeheader()
        writer.writerows(rows)


def log_picks(ticket_no, mode, today, short, chosen, rules_legs=None):
    """Record every bet the AI judged today (or the rule-picked legs), for the scorecard."""
    rows = read_picks()
    items = [(c, c.get("verdict", ""), c.get("adj"), i in chosen) for i, c in short.items()]
    if rules_legs:
        items = [(leg, "RULES", None, True) for leg in rules_legs]
    for c, verdict, adj, on_ticket in items:
        rows.append({
            "date": today, "ticket_no": ticket_no if on_ticket else "", "mode": mode,
            "event_id": c["event_id"], "sport_key": c["sport_key"], "sport": c["sport"],
            "league": c["league"], "match": f"{c['home']} v {c['away']}", "start": c["start"],
            "market": c.get("market", "h2h"), "sel": c.get("sel") or c["pick"],
            "point": "" if c.get("point") is None else c["point"], "pick": c["pick"],
            "odds": c["odds"], "market_chance": round(c["prob"], 4), "verdict": verdict,
            "ai_chance": "" if adj is None else round(adj, 4),
            "on_ticket": "yes" if on_ticket else "no", "result": "pending", "score": "",
            "consensus_chance": round(c.get("consensus", c["prob"]), 4),
            "sharp_chance": "" if c.get("sharp") is None else round(c["sharp"], 4),
            "sharp_book": c.get("sharp_book", ""),
            "edge": "" if c.get("edge") is None else round(c["edge"], 4)})
    write_picks(rows)


def settle_picks(now):
    """Settle logged picks from final scores, the same way ticket legs are settled."""
    rows = read_picks()
    pending = [r for r in rows if r["result"] == "pending"]
    if not pending:
        return
    scores = fetch_scores({r["sport_key"] for r in pending})
    for row in pending:
        score = scores.get(row["event_id"])
        if score:
            # home and away come from the score itself, as for ticket legs.
            leg = {"market": row["market"], "sel": row["sel"], "pick": row["pick"],
                   "point": float(row["point"]) if row["point"] else None}
            row["result"] = leg_result(leg, score)
            row["score"] = leg.get("score", "")
        if row["result"] == "pending" and (now - parse_time(row["start"])).days >= CONFIG["void_after_days"]:
            row["result"] = "void"
    write_picks(rows)


def scorecard_html():
    """How the AI's judgements compare with what actually happened."""
    rows = [r for r in read_picks() if r["result"] in ("won", "lost")]
    if len(rows) < 10:
        return (f"<h3>AI scorecard</h3><p>{len(rows)} judged picks settled so far; the "
                "scorecard starts at 10.</p>")

    def line(label, group):
        if not group:
            return ""
        n = len(group)
        won = sum(r["result"] == "won" for r in group) / n
        market = sum(float(r["market_chance"]) for r in group) / n
        diff = (won - market) * 100
        colour = "#1a7f37" if diff > 0 else "#b42318"
        return (f"<tr><td>{label}</td><td>{n}</td><td>{won:.0%}</td><td>{market:.0%}</td>"
                f"<td style='color:{colour}'>{diff:+.0f}</td></tr>")

    table = ""
    for verdict in ("AGREE", "RISKY", "AVOID", "RULES"):
        table += line(f"Verdict {verdict}", [r for r in rows if r["verdict"] == verdict])
    table += line("On the ticket", [r for r in rows if r["on_ticket"] == "yes"])
    names = {"h2h": "To win", "dc": "Double chance", "totals": "Over/under", "spreads": "Handicap"}
    for market, name in names.items():
        table += line(name, [r for r in rows if r["market"] == market])
    table += line("All judged picks", rows)
    return ("<h3>AI scorecard</h3><table border='1' cellpadding='5' cellspacing='0' "
            "style='border-collapse:collapse;font-size:13px'><tr><th>Group</th><th>Picks</th>"
            "<th>Won</th><th>Odds said</th><th>Difference (points)</th></tr>" + table +
            "</table><p><small>The AI adds value only if its AGREE picks win clearly more "
            "often than the odds said, over 100 or more picks. Small groups are mostly "
            "luck.</small></p>")


# -------------------------------------------------------- closing line ----
def bet_key(event_id, market, sel, point):
    point = "" if point in (None, "") else f"{float(point):g}"
    return (event_id, market, sel, point)


def read_closing():
    if not CLOSING_PATH.exists():
        return []
    with CLOSING_PATH.open() as fh:
        return list(csv.DictReader(fh))


def closing_row(pick, cand, now):
    """One closing-line record: the logged bet next to the prices shortly before the start.

    clv: what the price we logged pays against the closing fair chance (sharp if priced,
    else consensus), as a share; above 0 means we got a better price than the close.
    move: how much the fair chance of our side rose between the pick and the close,
    sharp to sharp when both exist, otherwise consensus to consensus.
    """
    minutes = round((parse_time(pick["start"]) - now).total_seconds() / 60)
    row = {"date": pick["date"], "event_id": pick["event_id"], "sport_key": pick["sport_key"],
           "match": pick["match"], "market": pick["market"], "sel": pick["sel"],
           "point": pick["point"], "pick": pick["pick"], "start": pick["start"],
           "on_ticket": pick["on_ticket"], "captured": iso(now), "minutes_before": minutes,
           "open_odds": pick["odds"],
           "open_consensus": pick.get("consensus_chance") or pick["market_chance"],
           "open_sharp": pick.get("sharp_chance", "")}
    if cand is None:
        return row  # the line moved away (or the bet left the feed): nothing to compare
    close = cand["sharp"] if cand["sharp"] is not None else cand["consensus"]
    row.update(close_odds=cand["odds"], close_consensus=round(cand["consensus"], 4),
               close_sharp="" if cand["sharp"] is None else round(cand["sharp"], 4),
               close_book=cand["sharp_book"],
               clv=round(float(pick["odds"]) * close - 1, 4))
    if row["open_sharp"] and cand["sharp"] is not None:
        row["move"] = round(cand["sharp"] - float(row["open_sharp"]), 4)
    else:
        row["move"] = round(cand["consensus"] - float(row["open_consensus"]), 4)
    return row


def capture_closing(now=None):
    """Record the prices of logged picks shortly before they start (closing line value).

    Run every 30 minutes by .github/workflows/closing.yml. Picks starting within
    closing_window_minutes are fetched once, one request per league, ticket legs first,
    within a daily credit budget. Makes no request when nothing is about to start.
    """
    now = now or datetime.now(timezone.utc)
    window = timedelta(minutes=CONFIG.get("closing_window_minutes", 45))
    done = {bet_key(r["event_id"], r["market"], r["sel"], r["point"]) for r in read_closing()}
    due = [r for r in read_picks() if r["result"] == "pending"
           and now < parse_time(r["start"]) <= now + window
           and bet_key(r["event_id"], r["market"], r["sel"], r["point"]) not in done]
    if not due:
        print("No logged pick starts soon; nothing to capture.")
        return 0
    today = now.date().isoformat()
    budget = {}
    if CLOSING_BUDGET_PATH.exists():
        budget = json.loads(CLOSING_BUDGET_PATH.read_text())
    used = budget.get(today, 0)
    limit = CONFIG.get("max_closing_credits_per_day", 16)
    leagues = {}
    for r in due:
        leagues.setdefault(r["sport_key"], []).append(r)
    order = sorted(leagues, key=lambda k: (not any(r["on_ticket"] == "yes" for r in leagues[k]),
                                           min(r["start"] for r in leagues[k])))
    rows = read_closing()
    added = 0
    for key in order:
        picks = leagues[key]
        markets = sorted({"h2h" if r["market"] == "dc" else r["market"] for r in picks})
        if used + len(markets) > limit:
            print(f"Closing budget reached ({used}/{limit}); skipping {key}.")
            continue
        ids = sorted({r["event_id"] for r in picks})
        events = api_get(f"/sports/{key}/odds", regions=CONFIG["region"],
                         markets=",".join(markets), oddsFormat="decimal",
                         eventIds=",".join(ids), commenceTimeFrom=iso(now))
        used += len(markets)
        cands = {}
        for event in events or []:
            for c in candidates_from_event(event, strict=False):
                cands[bet_key(c["event_id"], c["market"], c["sel"], c["point"])] = c
        for r in picks:
            rows.append(closing_row(r, cands.get(bet_key(r["event_id"], r["market"], r["sel"],
                                                         r["point"])), now))
            added += 1
    budget = {today: used}  # only today's count is needed
    CLOSING_BUDGET_PATH.write_text(json.dumps(budget) + "\n")
    with CLOSING_PATH.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, CLOSING_FIELDS, restval="")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Captured closing prices for {added} picks ({used}/{limit} credits today).")
    return added


def clv_html():
    """Closing line value summary for the email: the earliest sign of a real edge."""
    rows = [r for r in read_closing() if r.get("clv")]
    if not rows:
        return ""

    def line(label, group):
        if not group:
            return ""
        n = len(group)
        clv = sum(float(r["clv"]) for r in group) / n
        move = sum(float(r["move"]) for r in group) / n
        beat = sum(float(r["move"]) > 0 for r in group) / n
        return (f"<tr><td>{label}</td><td>{n}</td><td>{clv:+.1%}</td><td>{move * 100:+.1f}</td>"
                f"<td>{beat:.0%}</td></tr>")

    table = line("On the ticket", [r for r in rows if r["on_ticket"] == "yes"])
    table += line("All logged picks", rows)
    return ("<h3>Closing line</h3><table border='1' cellpadding='5' cellspacing='0' "
            "style='border-collapse:collapse;font-size:13px'><tr><th>Group</th><th>Picks</th>"
            "<th>Price vs close</th><th>Chance moved (points)</th><th>Moved our way</th></tr>"
            + table + "</table><p><small>Prices are checked again shortly before each start. "
            "Picks whose chance keeps rising before kick-off show a real edge long before "
            "win rates can.</small></p>")


# --------------------------------------------------------------- email ----
def money(value):
    return f"{value:,.2f} {CONFIG['currency']}"


def local_time(text):
    return parse_time(text).astimezone(TZ).strftime("%a %d.%m %H:%M")


def legs_table(legs, with_result):
    head = "<tr><th>Start</th><th>Sport</th><th>Match</th><th>Pick</th><th>Odds</th>"
    head += "<th>Result</th></tr>" if with_result else "</tr>"
    rows = ""
    for leg in legs:
        rows += (f"<tr><td>{local_time(leg['start'])}</td><td>{leg['sport']}<br>"
                 f"<small>{leg['league']}</small></td><td>{leg['home']} v {leg['away']}</td>"
                 f"<td><b>{leg['pick']}</b></td><td>{leg['odds']:.2f}</td>")
        if with_result:
            rows += f"<td>{leg['result']} {leg.get('score', '')}</td>"
        rows += "</tr>"
    return ('<table border="1" cellpadding="6" cellspacing="0" '
            f'style="border-collapse:collapse;font-size:14px">{head}{rows}</table>')


def build_email(state, finished, ticket, note, today):
    parts = [f"<h2>Betting report, {today.strftime('%d.%m.%Y')}</h2>"]

    for t in finished:
        colour = {"won": "#1a7f37", "lost": "#b42318"}.get(t["result"], "#555")
        parts.append(f"<h3>Ticket #{t['no']} ({t['date']}): "
                     f"<span style='color:{colour}'>{t['result'].upper()}</span></h3>")
        parts.append(legs_table(t["legs"], True))
        if t["result"] == "lost":
            parts.append(f"<p>Stake lost: {money(t['stake'])}.</p>")
        else:
            parts.append(
                f"<p>Payout {money(t['payout'])}, tax ({CONFIG['tax_rate']:.0%} of winnings) "
                f"{money(t['tax'])}, you receive {money(t['payout'] - t['tax'])}. "
                f"Net profit: <b>{money(t['net_profit'])}</b>.</p>")

    for t in state["open_tickets"]:
        if ticket and t["no"] == ticket["no"]:
            continue
        parts.append(f"<h3>Ticket #{t['no']} ({t['date']}): still waiting for results</h3>")
        parts.append(legs_table(t["legs"], True))

    if ticket:
        gross, tax, net = tax_and_payout(ticket["stake"], ticket["total_odds"])
        if ticket.get("paper"):
            parts.append(f"<h3>Today's PAPER ticket #{ticket['no']}: do not place</h3>"
                         "<p>Paper mode is on: this ticket is tracked with a virtual stake "
                         "to measure the picks. No real money is involved.</p>")
        else:
            parts.append(f"<h3>Today's ticket #{ticket['no']}</h3>")
        parts.append(legs_table(ticket["legs"], False))
        parts.append(
            f"<p>Total odds: <b>{ticket['total_odds']:.2f}</b><br>"
            f"Stake: <b>{money(ticket['stake'])}</b><br>"
            f"If it wins: payout {money(gross)}, tax {money(tax)}, you receive {money(net)} "
            f"(profit {money(net - ticket['stake'])}).<br>"
            f"Estimated chance from the odds: {ticket['win_prob']:.0%}.<br>"
            f"Picked by: {ticket.get('picked_by', 'rules')}.</p>"
            "<p><small>Odds are the average of European bookmakers and will differ slightly "
            "at Megawin. Double chance odds are estimated from the win/draw/win prices. "
            "Times are Skopje time.</small></p>")
        if ticket.get("analysis"):
            parts.append("<h3>AI analysis</h3>"
                         f"<div style='font-size:14px'>{ticket['analysis']}</div>"
                         "<p><small>Research and verdicts by Gemini from web search; it can "
                         "be wrong. Odds and limits are enforced by the bot.</small></p>")
    else:
        parts.append(f"<h3>No ticket today</h3><p>{note}</p>")

    s = ledger_summary("real")
    reserved = sum(t["stake"] for t in state["open_tickets"] if not t.get("paper"))
    parts.append(
        "<h3>Bankroll</h3>"
        f"<p>Available: <b>{money(state['bankroll'])}</b>"
        + (f" (plus {money(reserved)} on open tickets)" if reserved else "") + "<br>"
        f"Started with: {money(CONFIG['starting_bankroll'])}<br>"
        f"Settled tickets: {s['tickets']} ({s['won']} won, {s['lost']} lost)<br>"
        f"Total staked: {money(s['staked'])}, tax paid: {money(s['tax'])}<br>"
        f"Profit / loss after tax: <b>{money(s['profit'])}</b></p>")
    paper = ledger_summary("paper")
    if CONFIG.get("paper_mode") or paper["tickets"]:
        rate = paper["profit"] / paper["staked"] if paper["staked"] else 0
        parts.append(
            "<h3>Paper results</h3>"
            f"<p>Settled paper tickets: {paper['tickets']} ({paper['won']} won, "
            f"{paper['lost']} lost), each at a virtual {money(CONFIG['paper_stake'])}<br>"
            f"Paper profit / loss after tax: <b>{money(paper['profit'])}</b> "
            f"({rate:+.0%} of the amount staked)</p>")
    parts.append(scorecard_html())
    parts.append(clv_html())
    if credits_left is not None:
        total = len(odds_keys())
        which = f" on key {key_index + 1} of {total}" if total > 1 else ""
        parts.append(f"<p><small>Odds API requests left this month{which}: {credits_left}"
                     "</small></p>")

    if ticket:
        subject = ("PAPER " if ticket.get("paper") else "") + f"Ticket #{ticket['no']}: odds {ticket['total_odds']:.2f}, stake {ticket['stake']} MKD"
    else:
        subject = "No ticket today"
    if finished:
        subject = f"{finished[-1]['result'].upper()} #{finished[-1]['no']} | " + subject
    return subject, "\n".join(parts)


def send_email(subject, html):
    to = os.environ.get("EMAIL_TO", "")
    if os.environ.get("RESEND_API_KEY"):
        body = json.dumps({
            "from": os.environ.get("EMAIL_FROM") or "Betting Bot <onboarding@resend.dev>",
            "to": [to], "subject": subject, "html": html}).encode()
        req = urllib.request.Request(
            "https://api.resend.com/emails", data=body, method="POST",
            headers={"Authorization": f"Bearer {os.environ['RESEND_API_KEY']}",
                     "Content-Type": "application/json", "User-Agent": "kockajse-bot/1.0"})
        try:
            urllib.request.urlopen(req, timeout=30).read()
        except urllib.error.HTTPError as err:
            raise SystemExit(f"Email service refused the message: {err.code} {err.read().decode()}")
    elif os.environ.get("SMTP_USER"):
        msg = EmailMessage()
        msg["Subject"], msg["To"] = subject, to
        msg["From"] = os.environ.get("EMAIL_FROM") or os.environ["SMTP_USER"]
        msg.set_content("This email needs an HTML-capable mail app.")
        msg.add_alternative(html, subtype="html")
        host = os.environ.get("SMTP_HOST") or "smtp.gmail.com"
        with smtplib.SMTP_SSL(host, int(os.environ.get("SMTP_PORT") or 465),
                              context=ssl.create_default_context()) as smtp:
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)
    else:
        out = ROOT / "out"
        out.mkdir(exist_ok=True)
        (out / "email.html").write_text(f"<!-- {subject} -->\n{html}")
        print("No email settings found; wrote out/email.html instead.")


# ------------------------------------------------------------------ AI ----
def lessons():
    """Lessons from past results, written by the review task, for the AI prompts."""
    text = LESSONS_PATH.read_text().strip() if LESSONS_PATH.exists() else ""
    return text or "No lessons recorded yet."


def gemini_keys():
    """All configured Gemini keys, in the order they should be tried."""
    names = ["GEMINI_API_KEY"] + [f"GEMINI_API_KEY_{n}" for n in range(2, 10)]
    keys = [os.environ.get(name, "").strip() for name in names]
    return [k for k in dict.fromkeys(keys) if k]


def gemini(prompt, search=False, schema=None):
    """One Gemini call. Returns the reply text, or "" if it fails."""
    keys = gemini_keys()
    if not keys:
        return ""
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"temperature": 0.2}}
    if search:
        payload["tools"] = [{"google_search": {}}]
    if schema:
        payload["generationConfig"].update(responseMimeType="application/json",
                                           responseSchema=schema)
    kind = "research" if search else "decision"
    # Preferred model on every key first, then the fallback model on every key.
    # Web search is only free on some models, so search calls and plain calls use
    # separate model lists and do not eat into each other's daily quota.
    models = CONFIG["gemini_search_models"] if search else CONFIG["gemini_plain_models"]
    for model, (number, key) in itertools.product(models, enumerate(keys, 1)):
        if (number, model) in MODELS_OUT:
            continue
        label = f"{model}, key {number}"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        for attempt in range(4):
            started = time.time()
            try:
                req = urllib.request.Request(
                    url, data=json.dumps(payload).encode(), method="POST",
                    headers={"x-goog-api-key": key, "Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=180) as resp:
                    data = json.loads(resp.read().decode())
                parts = data["candidates"][0]["content"]["parts"]
                text = "".join(p.get("text", "") for p in parts).strip()
                if text:
                    AI_LOG.append(f"{kind} ({label}): ok on attempt {attempt + 1}, "
                                  f"{time.time() - started:.0f}s, {len(text)} chars")
                    return text
                AI_LOG.append(f"{kind} ({label}) attempt {attempt + 1}: empty reply")
            except (urllib.error.URLError, KeyError, IndexError, TimeoutError, ValueError) as err:
                code = getattr(err, "code", None)
                detail = err.read().decode()[:1500] if code else ""
                AI_LOG.append(f"{kind} ({label}) attempt {attempt + 1} failed: {err} {detail}")
                print(AI_LOG[-1])
                quota_gone = code == 429 and ("PerDay" in detail or attempt >= 1)
                if code in (400, 401, 403, 404) or quota_gone:
                    # Bad key, unknown model or used-up quota: waiting will not help.
                    MODELS_OUT.add((number, model))
                    break
            time.sleep(8 + 12 * attempt)
    return ""


DECISION_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "picks": {"type": "ARRAY", "items": {
            "type": "OBJECT",
            "properties": {
                "id": {"type": "INTEGER"},
                "verdict": {"type": "STRING", "enum": ["AGREE", "RISKY", "AVOID"]},
                "adjusted_chance": {"type": "NUMBER"},
                "summary": {"type": "STRING"}},
            "required": ["id", "verdict", "adjusted_chance", "summary"]}},
        "ticket": {"type": "ARRAY", "items": {"type": "INTEGER"}},
        "ticket_reason": {"type": "STRING"}},
    "required": ["picks", "ticket", "ticket_reason"],
}


def shortlist(cands):
    """Candidate bets for the AI: the best matches, each with its possible bets, numbered."""
    by_event = {}
    for c in cands:
        by_event.setdefault(c["event_id"], []).append(c)
    events = sorted(by_event.values(), key=lambda opts: max(o["prob"] for o in opts),
                    reverse=True)
    # Matches the AI scout chose come first; the rest fill any remaining places.
    events = ([e for e in events if e[0]["event_id"] in SCOUTED]
              + [e for e in events if e[0]["event_id"] not in SCOUTED])[:CONFIG["ai_shortlist"]]
    short, number = {}, 1
    for options in events:
        for c in sorted(options, key=lambda o: o["prob"], reverse=True)[:CONFIG["ai_options"]]:
            short[number] = c
            number += 1
    return short


def describe(short):
    lines, last = [], None
    for i, c in short.items():
        if c["event_id"] != last:
            last = c["event_id"]
            lines.append(f"MATCH: {c['sport']}, {c['league']}: {c['home']} (home) v {c['away']} "
                         f"(away), starts {local_time(c['start'])} Skopje time.")
        if c.get("sharp") is not None:
            price = (f"Price vs sharp fair price: {c['edge']:+.0%} "
                     f"({'value' if c['edge'] >= 0 else 'below fair'}).")
        else:
            price = "No sharp price for this bet."
        lines.append(f"  ID {i}: {c['pick']}. Odds {c['odds']:.2f}. Market chance {c['prob']:.0%}. "
                     + price)
    return "\n".join(lines)


def valid_combo(legs):
    odds = 1.0
    for leg in legs:
        odds *= leg["odds"]
    return (1 <= len(legs) <= CONFIG["max_legs"]
            and len({l["event_id"] for l in legs}) == len(legs)
            and CONFIG["min_total_odds"] <= round(odds, 2) <= CONFIG["max_total_odds"])


def ai_pick(cands, today):
    """Let Gemini research the shortlist and choose the ticket.

    Returns (ticket, analysis_html, note). ticket is None when the AI says no bet.
    Returns None when the AI is unavailable, so the caller can fall back to the rules.
    Every answer is checked in code: the AI can only choose from the shortlist, the odds
    always come from the feed, and the ticket must meet the odds limits.
    """
    short = shortlist(cands)
    if not short or not gemini_keys():
        return None
    listing = describe(short)
    day = f"{today:%A %d %B %Y, %H:%M}"
    # One search-backed call per match: a single call for all of them only covers a few.
    template = (ROOT / "prompts" / "research.txt").read_text()
    notes, found = [], 0
    for event_id in dict.fromkeys(c["event_id"] for c in short.values()):
        part = {i: c for i, c in short.items() if c["event_id"] == event_id}
        text = gemini(template.format(today=day, candidates=describe(part)), search=True)
        found += bool(text)
        notes.append(text or f"IDs {', '.join(map(str, part))}: NO RESEARCH AVAILABLE. "
                             "Data quality: NONE.")
        time.sleep(7)
    if not found:
        return None
    research = "\n\n".join(notes)
    RESEARCH["notes"] = research
    raw = gemini((ROOT / "prompts" / "decide.txt").read_text().format(
        today=day, candidates=listing, research=research, max_legs=CONFIG["max_legs"],
        lessons=lessons(),
        min_odds=CONFIG["min_total_odds"], max_odds=CONFIG["max_total_odds"]),
        schema=DECISION_SCHEMA)
    RESEARCH["decision"] = raw
    try:
        answer = json.loads(raw)
        verdicts = {int(p["id"]): p for p in answer["picks"] if int(p["id"]) in short}
        chosen = [int(i) for i in answer["ticket"]]
    except (ValueError, KeyError, TypeError):
        print("AI decision could not be read; using the rules instead.")
        return None

    # Missing verdicts count as RISKY; the AI may not raise a chance by more than 8 points.
    for i, c in short.items():
        v = verdicts.get(i, {})
        c["verdict"] = v.get("verdict", "RISKY")
        c["summary"] = str(v.get("summary", "No analysis returned."))[:600]
        try:
            adj = float(v.get("adjusted_chance", c["prob"] * 100)) / 100
        except (TypeError, ValueError):
            adj = c["prob"]
        c["adj"] = max(0.01, min(adj, c["prob"] + 0.08))

    def usable(ids):
        legs = [short[i] for i in ids]
        risky = sum(1 for l in legs if l["verdict"] == "RISKY")
        return (all(l["verdict"] != "AVOID" for l in legs) and risky <= 1
                and valid_combo(legs))

    source = "AI"
    if not (chosen and len(set(chosen)) == len(chosen)
            and all(i in short for i in chosen) and usable(chosen)):
        # The AI's ticket broke a rule (or was empty): build the best one its verdicts allow.
        chosen, best_score = [], 0
        for allow_risky in (False, True):
            pool = [i for i, c in short.items()
                    if c["verdict"] == "AGREE" or (allow_risky and c["verdict"] == "RISKY")]
            pool = sorted(pool, key=lambda i: short[i]["adj"], reverse=True)[:45]
            for size in range(1, CONFIG["max_legs"] + 1):
                for combo in itertools.combinations(pool, size):
                    score = 1.0
                    for i in combo:
                        score *= short[i]["adj"]
                    if usable(combo) and score > best_score:
                        chosen, best_score = list(combo), score
            if chosen:
                break
        source = "AI verdicts, ticket built by the rules"

    lines, last = [], None
    for i, c in short.items():
        if c["event_id"] != last:
            last = c["event_id"]
            lines.append(f"<br><b>{html_lib.escape(c['home'])} v {html_lib.escape(c['away'])}</b> "
                         f"({html_lib.escape(c['league'])})")
        mark = "<b>ON TICKET</b> " if i in chosen else ""
        lines.append(f"{mark}{html_lib.escape(c['pick'])} @ {c['odds']:.2f}: <b>{c['verdict']}</b> "
                     f"(market {c['prob']:.0%}, AI {c['adj']:.0%}). "
                     f"{html_lib.escape(c['summary'])}")
    reason = html_lib.escape(str(answer.get("ticket_reason", ""))[:600])
    analysis = (f"<p>{SCOUT_NOTE}</p><p><b>Why this ticket:</b> {reason}</p><p>"
                + "<br>".join(lines) + "</p>" + SCOUT_EXTRA)

    global LAST_SHORT
    LAST_SHORT = (short, chosen)
    if not chosen:
        return None, analysis, "The AI found no ticket that passes its checks today."
    legs = sorted(({k: v for k, v in short[i].items() if k not in ("adj",)} for i in chosen),
                  key=lambda c: c["start"])
    total, prob = 1.0, 1.0
    for leg in legs:
        total *= leg["odds"]
        prob *= leg["prob"]
    ticket = {"legs": legs, "total_odds": round(total, 2), "win_prob": round(prob, 4),
              "picked_by": source}
    return ticket, analysis, ""



# ---------------------------------------------------------------- main ----
def run(now=None, force=False, resend=False, preview=False):
    now = now or datetime.now(timezone.utc)
    local = now.astimezone(TZ)
    today = local.date().isoformat()
    state = json.loads(STATE_PATH.read_text())
    SCORES.clear()
    FETCHED_KEYS.clear()

    if not force and not resend and not preview:
        if local.hour < CONFIG["send_hour_local"]:
            print(f"Too early ({local:%H:%M} local); nothing to do.")
            return False
        if state.get("last_run_date") == today:
            print("Already ran today; nothing to do.")
            return False

    if resend:
        # Send the report again for the newest open ticket without changing anything else.
        ticket = state["open_tickets"][-1] if state["open_tickets"] else None
        subject, html = build_email(state, [], ticket, "No open ticket.", local)
        send_email(subject, html)
        print(subject)
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
        return True

    # A preview picks and emails a ticket but saves nothing and settles nothing.
    finished = [] if preview else settle(state, now)
    if not preview:
        settle_picks(now)
    paper = bool(CONFIG.get("paper_mode"))
    stake = CONFIG["paper_stake"] if paper else stake_for(state["bankroll"])
    ticket, note = None, ""

    if stake:
        state["stopped"] = False
        cands = pick_ticket(now)
        result = ai_pick(cands, local)
        analysis = ""
        if result is None:
            picked = build_ticket(cands)
            if picked:
                why = ""
                if not gemini_keys():
                    why = "no Gemini key"
                elif any(" 429" in line for line in AI_LOG):
                    why = "Gemini quota used up"
                elif AI_LOG:
                    why = "Gemini did not answer"
                picked["picked_by"] = f"rules, AI unavailable ({why})" if why else "rules"
            note = "No combination of games fits the rules today."
        else:
            picked, analysis, note = result
        if picked:
            ticket = {"no": state["next_ticket_no"], "date": today, "created": iso(now),
                      "stake": stake, **picked}
            ticket["analysis"] = analysis or SCOUT_EXTRA
            if paper:
                ticket["paper"] = True
            state["next_ticket_no"] += 1
            if not paper:
                state["bankroll"] = round(state["bankroll"] - stake, 2)
            state["open_tickets"].append(ticket)
        elif analysis:
            note += analysis
        if not preview:
            mode = "paper" if paper else "real"
            number = ticket["no"] if ticket else ""
            if result is not None and LAST_SHORT:
                log_picks(number, mode, today, *LAST_SHORT)
            if RESEARCH or SCOUT_NOTE:
                folder = STATE_PATH.parent / "research"
                folder.mkdir(exist_ok=True)
                (folder / f"{today}.json").write_text(json.dumps(
                    {"ticket_no": number, "scout": SCOUT_NOTE, **RESEARCH}, indent=2) + "\n")
            elif ticket:
                log_picks(number, mode, today, {}, [], rules_legs=ticket["legs"])
    elif state["open_tickets"]:
        note = "The remaining money is on open tickets. Waiting for their results."
    else:
        note = ("The bankroll is below the minimum stake, so the run is over. "
                "Change the bankroll in data/state.json to start again.")

    # When the run is over, send one final email and then stay quiet.
    silent = state.get("stopped") and not finished and not ticket
    if not paper and not stake_for(state["bankroll"]) and not state["open_tickets"]:
        state["stopped"] = True

    state["last_run_date"] = today
    if not silent:
        subject, html = build_email(state, finished, ticket, note, local)
        if preview:
            subject = "PREVIEW, not counted | " + subject
            (ROOT / "data" / "preview.json").write_text(json.dumps(
                {"when": iso(now), "ticket": ticket, "note": note, "log": AI_LOG,
                 "credits_left": credits_left}, indent=2) + "\n")
        send_email(subject, html)
        print(subject)
    if not preview:
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
        # What the AI calls did on this run, for troubleshooting.
        (STATE_PATH.parent / "last_run.json").write_text(json.dumps(
            {"when": iso(now), "ai_log": [line[:700] for line in AI_LOG],
             "odds_requests_left": credits_left}, indent=2) + "\n")
    return True


def diagnose():
    """Check which Gemini models each key can use, with and without web search."""
    report = {}
    base = "https://generativelanguage.googleapis.com/v1beta/models"
    for number, key in enumerate(gemini_keys(), 1):
        entry = report.setdefault(f"key {number}", {})
        try:
            req = urllib.request.Request(f"{base}?pageSize=200", headers={"x-goog-api-key": key})
            with urllib.request.urlopen(req, timeout=60) as resp:
                names = [m["name"].split("/")[-1] for m in json.loads(resp.read())["models"]
                         if "generateContent" in m.get("supportedGenerationMethods", [])]
        except Exception as err:  # noqa: BLE001 - report whatever went wrong
            entry["list_error"] = str(err)
            continue
        flash = [n for n in names if "flash" in n and not any(
            w in n for w in ("image", "tts", "audio", "live", "preview", "exp"))]
        entry["models"] = flash
        for model in flash[:12]:
            for search in (False, True):
                payload = {"contents": [{"parts": [{"text": "Reply with the word OK."}]}]}
                if search:
                    payload["tools"] = [{"google_search": {}}]
                try:
                    req = urllib.request.Request(
                        f"{base}/{model}:generateContent", data=json.dumps(payload).encode(),
                        method="POST", headers={"x-goog-api-key": key,
                                                "Content-Type": "application/json"})
                    with urllib.request.urlopen(req, timeout=90) as resp:
                        resp.read()
                    outcome = "ok"
                except urllib.error.HTTPError as err:
                    detail = err.read().decode()
                    limit = re.search(r"limit: (\d+)", detail)
                    outcome = f"{err.code}" + (f" (limit {limit.group(1)})" if limit else "")
                except Exception as err:  # noqa: BLE001
                    outcome = str(err)[:80]
                entry[f"{model} {'with search' if search else 'plain'}"] = outcome
                time.sleep(2)
    (ROOT / "data" / "diagnose.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


def notify_changes():
    """Email the newest entry of CHANGES.md (sent when the review task changes the bot)."""
    path = ROOT / "CHANGES.md"
    text = path.read_text() if path.exists() else ""
    entries = re.split(r"(?m)^## ", text)[1:]
    if not entries:
        print("CHANGES.md has no entries.")
        return
    title, _, body = entries[0].partition("\n")
    html, in_list = [f"<h2>Bot update: {html_lib.escape(title.strip())}</h2>"], False
    for line in body.strip().splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{html_lib.escape(stripped[2:])}</li>")
            continue
        if in_list:
            html.append("</ul>")
            in_list = False
        if stripped.startswith("### "):
            html.append(f"<h3>{html_lib.escape(stripped[4:])}</h3>")
        elif stripped:
            html.append(f"<p>{html_lib.escape(stripped)}</p>")
    if in_list:
        html.append("</ul>")
    html.append("<p><small>Full history: CHANGES.md and data/learning_log.md in the "
                "repository.</small></p>")
    send_email(f"Bot update: {title.strip()}", "\n".join(html))
    print(f"Sent: {title.strip()}")


if __name__ == "__main__":
    if "--diagnose" in sys.argv:
        diagnose()
        sys.exit()
    if "--closing" in sys.argv:
        capture_closing()
        sys.exit()
    if "--notify-changes" in sys.argv:
        notify_changes()
        sys.exit()
    run(force="--force" in sys.argv, resend="--resend" in sys.argv,
        preview="--preview" in sys.argv)
