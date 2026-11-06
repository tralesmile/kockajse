"""Checks for the tax-aware ticket rule (live since 6 Nov). Run: python tests/test_taxed.py"""
import datetime
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["GEMINI_API_KEY"] = "test"
import bot  # noqa: E402

bot.time.sleep = lambda *_: None
tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
CFG = bot.CONFIG
assert CFG["ticket_objective"] == "taxed_ev"

# --- expected return after tax ---------------------------------------------------
assert abs(bot.taxed_return(0.5, 2.0, 0.15) - (0.5 * 1.85 - 1)) < 1e-12
assert abs(bot.taxed_return(1.0, 3.0, 0.0) - 2.0) < 1e-12
# At fair odds the tax alone costs tax x (1 - chance) of the stake.
assert abs(bot.taxed_return(0.4, 2.5, 0.15) - (-0.15 * 0.6)) < 1e-12


# --- build_taxed_ticket ------------------------------------------------------------
def cand(eid, prob, odds, power=None, best=None, market="h2h"):
    return {"event_id": eid, "start": f"2026-11-06T{10 + len(eid):02d}:00:00Z", "pick": eid,
            "market": market, "sel": eid, "point": None, "home": eid, "away": "x",
            "sport_key": "soccer_epl", "odds": odds, "prob": prob,
            "power_prob": power if power is not None else prob, "best_odds": best,
            "best_book": "bk" if best else ""}


# "likely" pair: 0.68 x 0.52 = 0.354 at 1.40 x 1.82 = 2.55 (legs about 5% below fair):
# -18.1% after tax. "value" pair: 0.60 x 0.57 = 0.342 at 1.62 x 1.72 = 2.79 (legs 2-3%
# below fair): -13.9% after tax.
cs = [cand("a", 0.68, 1.40), cand("b", 0.52, 1.82), cand("c", 0.60, 1.62), cand("d", 0.57, 1.72)]
likely = bot.build_ticket(cs)
taxed = bot.build_taxed_ticket(cs)
assert {l["event_id"] for l in likely["legs"]} == {"a", "b"}, likely
assert {l["event_id"] for l in taxed["legs"]} == {"c", "d"}, taxed
er = lambda t: bot.taxed_return(t["win_prob"], t["total_odds"])  # noqa: E731
assert er(taxed) > er(likely) and abs(taxed["expected_return"] - er(taxed)) < 5e-3
# Legs keep their own fields (prob is still the logged market chance, no helper keys).
assert all("_p" not in l and l["prob"] == next(c["prob"] for c in cs if c["event_id"] ==
                                                 l["event_id"]) for l in taxed["legs"])
assert taxed["legs"] == sorted(taxed["legs"], key=lambda l: l["start"])
# The power chance is what is ranked on: raise d's power chance and the pair changes.
cs2 = cs[:3] + [cand("d", 0.57, 1.72, power=0.50)]
assert "d" not in {l["event_id"] for l in bot.build_taxed_ticket(cs2)["legs"]}
# Total odds must stay inside the range; legs outside the leg-odds band are ignored.
assert CFG["min_total_odds"] <= taxed["total_odds"] <= CFG["max_total_odds"]
assert bot.build_taxed_ticket([cand("a", 0.9, 1.1), cand("b", 0.9, 1.15)]) is None
assert bot.build_taxed_ticket([cand("a", 0.40, 2.6)]) is None  # above max_leg_odds 2.0
# One bet per match.
same = [cand("a", 0.62, 1.60), dict(cand("a", 0.59, 1.70), sel="other")]
assert bot.build_taxed_ticket(same) is None
# At the best price: every leg priced at its best offer (falls back to the average).
cs3 = [cand("c", 0.60, 1.62, best=1.66), cand("d", 0.57, 1.72)]
tb = bot.build_taxed_ticket(cs3, odds_key="best_odds")
assert sorted(l["odds"] for l in tb["legs"]) == [1.66, 1.72], tb
print("taxed ticket rule checks passed")


# --- the AI path chooses by expected return after tax ---------------------------------
def book(i, markets):
    return {"key": f"b{i}", "markets": markets}


def soccer_event(eid, home, away, prices):
    books = []
    for i in range(7):
        k = 1 + 0.005 * i
        books.append(book(i, [{"key": "h2h", "outcomes": [
            {"name": home, "price": prices[0] * k}, {"name": away, "price": prices[1] * k},
            {"name": "Draw", "price": prices[2] * k}]}]))
    return {"id": eid, "sport_key": "soccer_epl", "sport_title": "EPL", "home_team": home,
            "away_team": away, "commence_time": "2026-11-06T19:00:00Z", "bookmakers": books}


cands = []
for n, prices in enumerate([(1.45, 5.0, 4.6), (1.62, 4.2, 4.0), (1.75, 3.9, 3.8),
                            (1.55, 5.5, 4.2), (1.85, 3.8, 3.6)]):
    cands += bot.candidates_from_event(soccer_event(f"e{n}", f"H{n}", f"A{n}", prices))
short = bot.shortlist(cands)


def fake(answer):
    def g(prompt, search=False, schema=None):
        return "notes" if search else json.dumps(answer)
    return g


now = datetime.datetime.now(bot.TZ)
picks = [{"id": i, "verdict": "AGREE", "adjusted_chance": c["prob"] * 100, "summary": "s"}
         for i, c in short.items()]
bot.gemini = fake({"picks": picks, "ticket": [], "ticket_reason": "r"})
ticket, _, _ = bot.ai_pick(cands, now)
info = bot.RESEARCH["ai_ticket"]
s = bot.LAST_SHORT[0]
assert info["likely_ids"] == info["best_ids"] and info["tax_ids"], info


def ret(ids):
    p = 1.0
    o = 1.0
    for i in ids:
        p *= s[i]["blend_power"]
        o *= s[i]["odds"]
    return bot.taxed_return(p, o)


assert abs(ret(info["tax_ids"]) - info["tax_return"]) < 1e-3
assert ret(info["tax_ids"]) >= ret(info["likely_ids"]) - 1e-9
assert sorted(l["event_id"] for l in ticket["legs"]) == sorted(s[i]["event_id"]
                                                              for i in info["tax_ids"])
assert "after tax" in ticket["picked_by"], ticket["picked_by"]
assert all("blend_power" not in l for l in ticket["legs"])
# AVOID picks never enter the taxed ticket.
avoid = [dict(p, verdict="AVOID") if p["id"] in info["tax_ids"][:1] else p for p in picks]
bot.gemini = fake({"picks": avoid, "ticket": [], "ticket_reason": "r"})
bot.ai_pick(cands, now)
assert info["tax_ids"][0] not in bot.RESEARCH["ai_ticket"]["tax_ids"]
# The AI's own ticket stands when it is the best after tax.
bot.gemini = fake({"picks": picks, "ticket": info["tax_ids"], "ticket_reason": "r"})
ticket, _, _ = bot.ai_pick(cands, now)
assert ticket["picked_by"] == "AI"
# The old objective is still available from config.
CFG["ticket_objective"] = "most_likely"
bot.gemini = fake({"picks": picks, "ticket": [], "ticket_reason": "r"})
ticket, _, _ = bot.ai_pick(cands, now)
assert sorted(l["event_id"] for l in ticket["legs"]) == sorted(s[i]["event_id"]
                                                              for i in info["likely_ids"])
CFG["ticket_objective"] = "taxed_ev"

# --- shadows: old rule, best-price twin and market-only twin ---------------------------
bot.gemini = fake({"picks": picks, "ticket": [], "ticket_reason": "r"})
ticket, _, _ = bot.ai_pick(cands, now)
shadows = dict(bot.shadow_tickets(cands, bot.LAST_SHORT[0], ticket))
for name in ("actual", "likely_ticket", "tax_best", "tax_market", "market"):
    assert name in shadows, (name, list(shadows))
    assert name in bot.SHADOW_NAMES
for name in ("likely_ticket", "tax_best", "tax_market"):
    assert name in bot.SHADOW_LEGS_CLV
assert all(l["book"] != "average" for l in shadows["tax_best"] if l.get("best_odds"))
rows = bot.shadow_rows("2026-11-06", list(shadows.items()))
assert {r["strategy"] for r in rows} >= {"likely_ticket", "tax_best", "tax_market"}
print("taxed AI path and shadow checks passed")
