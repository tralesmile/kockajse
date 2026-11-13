"""Checks for power-method de-margining and its shadows. Run: python tests/test_power.py"""
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bot  # noqa: E402
import backtest  # noqa: E402

tmp = Path(tempfile.mkdtemp())
bot.STATE_PATH = tmp / "state.json"
bot.PICKS_PATH = tmp / "picks.csv"
bot.CLOSING_PATH = tmp / "closing.csv"

# --- power_devig -------------------------------------------------------------
prices = [1.25, 6.0, 12.0]  # heavy favourite, 1X2 with about 5% margin
pw = bot.power_devig(prices)
total = sum(1 / o for o in prices)
prop = [(1 / o) / total for o in prices]
assert abs(sum(pw) - 1) < 1e-9, pw
# Power gives the favourite more and the longshot less than proportional normalisation.
assert pw[0] > prop[0] and pw[2] < prop[2], (pw, prop)
# The power is the same for every outcome: log(p_i) / log(1/o_i) equal.
import math  # noqa: E402
ks = [math.log(p) / math.log(1 / o) for p, o in zip(pw, prices)]
assert max(ks) - min(ks) < 1e-6 and ks[0] > 1, ks
# Even two-way prices stay even; no margin means no change.
assert abs(bot.power_devig([1.91, 1.91])[0] - 0.5) < 1e-9
assert abs(bot.power_devig([2.0, 2.0])[0] - 0.5) < 1e-9
fair2 = bot.power_devig([1.5, 3.0])  # sums to exactly 1: returned as is
assert abs(fair2[0] - 2 / 3) < 1e-9
print("power devig checks passed")


# --- candidates carry power chances ---------------------------------------------
def event(eid, home, away, sharp, soft, best=None, start="2026-11-04T18:00:00Z"):
    def h2h(key, p):
        return {"key": key, "markets": [{"key": "h2h", "outcomes": [
            {"name": home, "price": p[0]}, {"name": away, "price": p[1]}]}]}
    books = [h2h("pinnacle", sharp)] + [h2h(f"soft{i}", soft) for i in range(6)]
    if best:
        books.append(h2h("onexbet", best))
    return {"id": eid, "sport_key": "basketball_nba", "sport_title": "NBA", "home_team": home,
            "away_team": away, "commence_time": start, "bookmakers": books}


# Heavy favourite 1.10: below the ticket's 1.20 floor, so only the wide scan sees it.
fav = event("p1", "Celtics", "Wizards", sharp=(1.09, 9.0), soft=(1.08, 7.5), best=(1.12, 7.0))
assert not [c for c in bot.candidates_from_event(fav) if c["sel"] == "Celtics"]
wide = bot.wide_candidates([fav])
cel = next(c for c in wide if c["sel"] == "Celtics")
sp = bot.power_devig([1.09, 9.0])[0]
assert abs(cel["sharp_power"] - sp) < 1e-9 and cel["sharp_power"] > cel["sharp"], cel
assert cel["best_odds"] == 1.12
# Proportional: 0.892 x 1.12 is short of the tax hurdle; power: 0.906 clears it.
assert bot.taxed_ev(cel["sharp"], 1.12) < 0 < bot.taxed_ev(cel["sharp_power"], 1.12), (
    cel["sharp"], cel["sharp_power"])
assert not bot.taxed_value_bets(wide)
pv = bot.taxed_value_bets(wide, "sharp_power")
assert [c["sel"] for c in pv] == ["Celtics"], pv
# Without a sharp price there is no power value either.
nosharp = dict(fav, id="p2", bookmakers=fav["bookmakers"][1:])
assert not bot.taxed_value_bets(bot.wide_candidates([nosharp]), "sharp_power")

# --- shadows -------------------------------------------------------------------
games = [event("g1", "Lakers", "Kings", sharp=(1.50, 2.75), soft=(1.45, 2.65)),
         event("g2", "Heat", "Nets", sharp=(1.30, 3.80), soft=(1.26, 3.60)),
         event("g3", "Bulls", "Jazz", sharp=(1.70, 2.20), soft=(1.66, 2.15))]
pool = [c for g in games for c in bot.candidates_from_event(g)]
short = {i + 1: dict(c, verdict="AGREE") for i, c in enumerate(pool)}
bot.RESEARCH.clear()
tk = bot.shadow_tickets(pool, short, bot.build_ticket(pool), wide=pool + wide)
d = dict(tk)
assert "power_value" in d and d["power_value"][0]["odds"] == 1.12, [n for n, _ in tk]
assert d["power_value"][0]["book"] == "onexbet"
# The older value shadows still ignore prices under min_leg_odds.
assert not any(l["event_id"] == "p1" for n, legs in tk if n not in ("power_value", "fav_flat") for l in legs)
assert "power_ticket" in d
total = 1.0
for leg in d["power_ticket"]:
    total *= leg["odds"]
assert bot.CONFIG["min_total_odds"] <= round(total, 2) <= bot.CONFIG["max_total_odds"]
rows = bot.shadow_rows("2026-11-04", tk)
pvrow = next(r for r in rows if r["strategy"] == "power_value")
assert abs(pvrow["fair_chance"] - round(sp, 4)) < 1e-9, pvrow
assert pvrow["edge"] == round(round(sp, 4) * 1.12 - 1, 4)
assert all(n in bot.SHADOW_NAMES for n, _ in tk)
assert "power_value" in bot.SHADOW_CLV and "power_value" in bot.SHARP_SHADOWS

# Closing for power_value compares power with power.
pick = dict(pvrow, date="2026-11-04")
close_cand = next(c for c in bot.candidates_from_event(fav, strict=False) if c["sel"] == "Celtics")
row = bot.closing_row(pick, close_cand, datetime(2026, 11, 4, 17, 30, tzinfo=timezone.utc),
                      source="power_value")
assert row["close_sharp"] == round(close_cand["sharp_power"], 4), row
assert abs(row["move"]) < 1e-3, row  # same prices: no move
print("power shadow checks passed")

# --- backtest ------------------------------------------------------------------
r = {"HomeTeam": "A", "AwayTeam": "B", "_date": "2025-01-01", "_hg": 2, "_ag": 0,
     "_src": "t", "PSCH": "1.25", "PSCD": "6.0", "PSCA": "12.0", "AvgCH": "1.22",
     "AvgCD": "5.6", "AvgCA": "11.0", "MaxCH": "1.30", "MaxCD": "6.2", "MaxCA": "13.0"}
cands = backtest.match_candidates(r, 0)
home = next(c for c in cands if c["market"] == "h2h" and c["sel"] == "H")
assert abs(home["prob_power"] - bot.power_devig([1.25, 6.0, 12.0])[0]) < 1e-9
assert home["prob_power"] > home["prob"]
assert {"most_likely_power", "value_taxed_power"} <= set(backtest.STRATEGIES)
bets = backtest.STRATEGIES["value_taxed_power"][1](cands)
assert all(b[0]["best"] and backtest.taxed_ev(b[0]) > 0 for b in
           [[dict(x[0], prob=x[0]["prob_power"])] for x in bets])
print("all power checks passed")
