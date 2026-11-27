"""The AI's shortlist includes the matches of the market maths' moneyline tickets, and the old
shortlist runs beside it as a shadow. Run: python tests/test_math_shortlist.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import audit  # noqa: E402
import bot  # noqa: E402

SOFT = ["unibet_se", "williamhill", "sport888", "betsson", "coolbet", "nordicbet"]


def event(eid, home_price, away_price, pin=None, extra=False):
    pin = pin or (home_price, away_price)

    def book(key, prices):
        markets = [{"key": "h2h", "outcomes": [{"name": f"H{eid}", "price": prices[0]},
                                               {"name": f"A{eid}", "price": prices[1]}]}]
        if extra:  # heavy-favourite line bets that outrank the moneyline by chance
            for market, names in (("spreads", (f"H{eid}", f"A{eid}")),):
                markets.append({"key": market, "outcomes": [
                    {"name": names[0], "point": 9.5, "price": 1.22},
                    {"name": names[1], "point": -9.5, "price": 4.0}]})
            markets.append({"key": "totals", "outcomes": [
                {"name": "Over", "point": 150.5, "price": 1.21},
                {"name": "Under", "point": 150.5, "price": 4.1}]})
        return {"key": key, "markets": markets}
    return {"id": eid, "sport_key": "basketball_nba", "sport_title": "NBA",
            "home_team": f"H{eid}", "away_team": f"A{eid}",
            "commence_time": "2026-11-30T20:00:00Z",
            "bookmakers": [book("pinnacle", pin)] + [book(k, (home_price, away_price)) for k in SOFT]}


# Twelve very short favourites (what the scout and the old fill prefer) and two fairly priced
# mid favourites, where the sharp book rates the home side above what the average price implies.
events = [event(f"s{i}", 1.40, 2.95, pin=(1.44, 2.80)) for i in range(3)]
events += [event(f"s{i}", 1.22, 4.2) for i in range(3, 12)]
events += [event(f"m{i}", 1.62, 2.30, pin=(1.55, 2.55), extra=True) for i in range(2)]
cands = [c for e in events for c in bot.candidates_from_event(e)]
bot.SCOUTED[:] = [f"s{i}" for i in range(8)]
bot.CONFIG["ai_shortlist"] = 12
bot.CONFIG["ai_options"] = 2
bot.CONFIG["ai_shortlist_math_tickets"] = 2

wanted = bot.math_matches(cands)
assert ("m0", "Hm0") in wanted and ("m1", "Hm1") in wanted, wanted
assert len({e for e, _ in wanted}) == len(wanted), "the second ticket uses other matches"

old = bot.shortlist(cands, math_tickets=0)
old_ids = list(dict.fromkeys(c["event_id"] for c in old.values()))
assert set(old_ids[:8]) == set(bot.SCOUTED) and len(old_ids) == 12
assert not {"m0", "m1"} & set(old_ids), old_ids

new = bot.shortlist(cands)
new_ids = list(dict.fromkeys(c["event_id"] for c in new.values()))
assert len(new_ids) == 12, "no extra matches, so no extra Gemini searches"
assert {e for e, _ in wanted} <= set(new_ids)
assert list(new) == list(range(1, len(new) + 1))
# the moneyline bet the maths chose is offered even when other bets have higher chances
for eid, sel in wanted:
    opts = [c for c in new.values() if c["event_id"] == eid]
    assert any(c["market"] == "h2h" and c["sel"] == sel for c in opts), opts
    assert len(opts) <= bot.CONFIG["ai_options"]

# switched off: the old behaviour
bot.CONFIG["ai_shortlist_math_tickets"] = 0
assert bot.math_matches(cands) == []
assert [c["event_id"] for c in bot.shortlist(cands).values()] == [c["event_id"] for c in old.values()]
assert "old_shortlist" not in dict(bot.shadow_tickets(cands, bot.shortlist(cands)))
bot.CONFIG["ai_shortlist_math_tickets"] = 2

# the shadow uses only matches of the old shortlist; the maths ticket on the new one is likelier
tickets = dict(bot.shadow_tickets(cands, new))
legs = tickets["old_shortlist"]
assert {l["event_id"] for l in legs} <= set(old_ids) and all(l["market"] == "h2h" for l in legs)
wide = bot.build_taxed_ticket([c for c in cands if c["market"] == "h2h"])
chance = lambda ls: __import__("math").prod(c["power_prob"] for c in ls)
assert chance(wide["legs"]) > chance(legs) and len(wide["legs"]) < len(legs)
assert "old_shortlist" in bot.SHADOW_NAMES and "old_shortlist" in bot.SHADOW_LEGS_CLV
assert "old_shortlist" in audit.TICKET_STRATEGIES
print("math shortlist tests passed")
