"""Checks for best prices, value bets and shadow tickets. Run: python tests/test_shadow.py"""
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"
assert bot.shadow_path() == tmp / "shadow.csv"


def event(eid, home, away, sharp, soft, best=None, outlier=None, start="2026-11-02T18:00:00Z"):
    """Two-way basketball match: Pinnacle prices `sharp`, six soft books price `soft`."""
    def h2h(key, prices):
        return {"key": key, "markets": [{"key": "h2h", "outcomes": [
            {"name": home, "price": prices[0]}, {"name": away, "price": prices[1]}]}]}
    books = [h2h("pinnacle", sharp)] + [h2h(f"soft{i}", soft) for i in range(5)]
    books.append(h2h("betfair_ex_eu", (soft[0] + 0.5, soft[1])))  # exchange: never "best"
    if best:
        books.append(h2h("onexbet", best))
    if outlier:
        books.append(h2h("typo_bet", outlier))
    return {"id": eid, "sport_key": "basketball_nba", "sport_title": "NBA", "home_team": home,
            "away_team": away, "commence_time": start, "bookmakers": books}


# --- best price -------------------------------------------------------------
assert bot.best_offer([(1.5, "a"), (1.62, "b"), (2.4, "typo")], 1.55) == (1.62, "b")
assert bot.best_offer([], 1.5) == (None, "")
cands = {c["pick"]: c for c in bot.candidates_from_event(
    event("e1", "Celtics", "Hornets", sharp=(1.60, 2.50), soft=(1.52, 2.45), best=(1.70, 2.40),
          outlier=(2.20, 1.70)))}
cel = cands["Celtics to win"]
assert cel["best_book"] == "onexbet" and cel["best_odds"] == 1.70, cel
fair = (1 / 1.60) / (1 / 1.60 + 1 / 2.50)
assert abs(cel["sharp"] - fair) < 1e-9
assert cel["best_edge"] == round(fair * 1.70 - 1, 4) and cel["best_edge"] > 0.02
assert cel["edge"] < cel["best_edge"]  # the average price pays less than the best one
# The 2.20 outlier is more than 10% above the average, so it is not the best price.
assert cel["best_odds"] < 2.0

# --- value bets ---------------------------------------------------------------
games = [
    event("e1", "Celtics", "Hornets", sharp=(1.60, 2.50), soft=(1.52, 2.45), best=(1.70, 2.40)),
    event("e2", "Lakers", "Kings", sharp=(1.50, 2.75), soft=(1.45, 2.65), best=(1.62, 2.60)),
    event("e3", "Heat", "Nets", sharp=(1.30, 3.80), soft=(1.26, 3.60)),  # no value anywhere
]
pool = [c for g in games for c in bot.candidates_from_event(g)]
values = bot.value_bets(pool)
assert sorted(v["event_id"] for v in values) == ["e1", "e2"], [(v["event_id"], v["best_edge"]) for v in values]
assert all(v["best_edge"] >= bot.CONFIG["value_min_edge"] for v in values)

# --- shadow tickets -----------------------------------------------------------
short = {i + 1: dict(c, verdict="AGREE", adj=c["prob"], blend=c["prob"])
         for i, c in enumerate(pool)}
bot.RESEARCH.clear()
bot.RESEARCH["ai_ticket"] = {"ids": [1, 3], "edge_first_ids": [1, 3]}
ticket = bot.build_ticket(pool)
tickets = bot.shadow_tickets(pool, short, ticket)
names = [s for s, _ in tickets]
core = [n for n in names if n not in ("actual_best", "single")]
assert core[:4] == ["actual", "market", "ai_own", "edge_first"], names
assert "value_ticket" in names and names.count("value_single") == 2, names
vt = dict(tickets)["value_ticket"]
total = 1.0
for leg in vt:
    total *= leg["odds"]
    assert leg["book"] == "onexbet"
assert bot.CONFIG["min_total_odds"] <= round(total, 2) <= bot.CONFIG["max_total_odds"]

# Unknown ids from the AI are ignored instead of crashing.
bot.RESEARCH["ai_ticket"] = {"ids": [99], "edge_first_ids": []}
assert "ai_own" not in [s for s, _ in bot.shadow_tickets(pool, short, None)]

# --- logging, settlement and summary -----------------------------------------
bot.RESEARCH["ai_ticket"] = {"ids": [1, 3], "edge_first_ids": [1, 3]}
bot.log_shadow("2026-11-02", bot.shadow_tickets(pool, short, ticket))
bot.log_shadow("2026-11-02", bot.shadow_tickets(pool, short, ticket))  # re-run replaces
rows = bot.read_shadow()
assert len({r["shadow_id"] for r in rows}) == len(tickets), len(rows)
singles = [r for r in rows if r["strategy"] == "value_single"]
assert singles[0]["book"] == "onexbet" and float(singles[0]["edge"]) > 0


def score(eid, home, away, hs, as_):
    return {"id": eid, "completed": True, "home_team": home, "away_team": away,
            "scores": [{"name": home, "score": str(hs)}, {"name": away, "score": str(as_)}]}


# Celtics and Lakers win, Heat lose; e3 has no score yet.
bot.fetch_scores = lambda keys: {"e1": score("e1", "Celtics", "Hornets", 110, 100),
                                 "e2": score("e2", "Lakers", "Kings", 99, 98)}
bot.settle_shadow(datetime(2026, 11, 3, 7, 0, tzinfo=timezone.utc))
rows = bot.read_shadow()
summary = bot.shadow_summary(rows)
single = summary["value_single"]
assert single["tickets"] == 2 and single["won"] == 2, single
# 100 at 1.70 -> 170, tax 15% of 70 = 10.5 -> +59.5; 100 at 1.62 -> +52.7
expected = round((bot.tax_and_payout(100, 1.70)[2] - 100) + (bot.tax_and_payout(100, 1.62)[2] - 100), 2)
assert single["profit"] == expected, (single, expected)
assert summary["value_ticket"]["won"] == 1
html = bot.shadow_html()
assert "Strategy comparison" in html and "Value singles" in html

# A leg that never gets a score is void after the limit, and an all-void ticket is ignored.
bot.fetch_scores = lambda keys: {}
bot.settle_shadow(datetime(2026, 11, 9, 7, 0, tzinfo=timezone.utc))
assert not [r for r in bot.read_shadow() if r["result"] == "pending"]
bot.shadow_summary()

# Picks log keeps the best price columns.
bot.log_picks(1, "paper", "2026-11-02", {1: dict(short[1])}, [1])
row = bot.read_picks()[0]
assert row["best_book"] == "onexbet" and float(row["best_edge"]) > 0, row
# --- wide value scan, Kaunitz rule and the odds archive (2 Nov) --------------
# A 2.60 underdog is outside the ticket's odds cap but inside the wide value list.
dog = event("e4", "Bucks", "Knicks", sharp=(1.55, 2.60), soft=(1.50, 2.50), best=(1.45, 2.78))
assert not [c for c in bot.candidates_from_event(dog) if c["sel"] == "Knicks"]
wide = bot.wide_candidates([dog])
knicks = next(c for c in wide if c["sel"] == "Knicks")
assert knicks["best_odds"] == 2.78 and knicks["best_edge"] > 0.02, knicks
assert [v["event_id"] for v in bot.value_bets(wide)] == ["e4"]

# Kaunitz: average about 2.55, threshold 1 / (1/2.55 - 0.05) = 2.92. 2.78 is not enough,
# 3.05 is (it is 20% above the average, so only the looser 25% outlier cap keeps it).
assert not bot.kaunitz_bets(wide)
dog2 = event("e5", "Suns", "Jazz", sharp=(1.55, 2.60), soft=(1.50, 2.50), best=(1.45, 3.05))
k = bot.kaunitz_bets(bot.wide_candidates([dog2]))
assert len(k) == 1 and k[0]["sel"] == "Jazz" and k[0]["top_odds"] == 3.05, k
assert k[0]["best_odds"] != 3.05  # the strict best price still drops it as an outlier
# Far outliers (more than 25% above average) never count.
typo = event("e6", "Mavs", "Spurs", sharp=(1.55, 2.60), soft=(1.50, 2.50), best=(1.45, 3.40))
assert not bot.kaunitz_bets(bot.wide_candidates([typo]))

bot.RESEARCH["ai_ticket"] = {}
tk = bot.shadow_tickets(pool, short, ticket, wide=pool + bot.wide_candidates([dog, dog2]))
names = [s for s, _ in tk]
assert "kaunitz_single" in names, names
ks = dict(tk)["kaunitz_single"][0]
assert ks["odds"] == 3.05 and ks["book"] == "onexbet", ks
rows = bot.shadow_rows("2026-11-03", tk)
assert any(r["strategy"] == "kaunitz_single" for r in rows)
assert "Kaunitz" in bot.SHADOW_NAMES["kaunitz_single"]

import gzip, json as _json
path = bot.save_odds_snapshot("2026-11-03", datetime(2026, 11, 3, 7, 0, tzinfo=timezone.utc),
                              [dog, dog2])
snap = _json.loads(gzip.open(path, "rt").read())
assert snap["fetched"] == "2026-11-03T07:00:00Z" and len(snap["events"]) == 2
assert snap["events"][0]["books"]["onexbet"]["h2h"][1] == ["Knicks", None, 2.78]
assert bot.save_odds_snapshot("2026-11-04", datetime.now(timezone.utc), []) is None
print("wide value checks passed")
print("all shadow checks passed")

# --- price shopping, one single a day and tax-proof value (3 Nov) ------------
# After the 15% tax a single needs prob * (odds - 1) * 0.85 > 1 - prob.
assert abs(bot.taxed_ev(0.5, 2.0) - (0.5 * 0.85 - 0.5)) < 1e-12
assert bot.taxed_ev(0.5, 2.0) < 0 < bot.taxed_ev(0.5, 2.40)
# Celtics: sharp 61%, best 1.70 -> +3.7% before tax but -4.3% after: not tax-proof.
assert not bot.taxed_value_bets(pool)
big = event("e7", "Bulls", "Pistons", sharp=(1.60, 2.50), soft=(1.52, 2.45), best=(1.66, 2.62))
fair_p = (1 / 2.50) / (1 / 1.60 + 1 / 2.50)
assert bot.taxed_ev(fair_p, 2.62) < 0  # 2.62 vs fair 2.56 is still not enough
huge = event("e8", "Hawks", "Magic", sharp=(1.30, 4.00), soft=(1.25, 3.60), best=(1.42, 3.40))
tv = bot.taxed_value_bets(bot.wide_candidates([big, huge]))
assert [c["event_id"] for c in tv] == ["e8"], [(c["event_id"], c["sel"], c["best_odds"]) for c in tv]

bot.RESEARCH["ai_ticket"] = {"ids": [1, 3], "edge_first_ids": [1, 3]}
short2 = dict(short)
short2[1] = dict(short2[1], verdict="AVOID")
tk = bot.shadow_tickets(pool, short2, ticket, wide=pool + bot.wide_candidates([huge]))
d = {}
for name, legs in tk:
    d.setdefault(name, legs)
assert "actual_best" in d, [n for n, _ in tk]
for real, shop in zip(ticket["legs"], d["actual_best"]):
    assert shop["odds"] >= real["odds"]
assert any(l["book"] == "onexbet" for l in d["actual_best"])
single = d["single"]
assert len(single) == 1 and single[0]["verdict"] != "AVOID"
best_allowed = max((c for c in short2.values() if c["verdict"] != "AVOID"),
                   key=lambda c: c["prob"] * c["odds"])
assert single[0]["pick"] == best_allowed["pick"]
assert d["taxed_value"][0]["event_id"] == "e8" and d["taxed_value"][0]["odds"] == 1.42
rows = bot.shadow_rows("2026-11-04", tk)
assert {"actual_best", "single", "taxed_value"} <= {r["strategy"] for r in rows}
assert all(n in bot.SHADOW_NAMES for n, _ in tk)
# No real ticket: no actual and no actual_best.
assert "actual_best" not in [n for n, _ in bot.shadow_tickets(pool, short2, None)]
print("price shopping, single and tax-proof value checks passed")
