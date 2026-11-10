"""Break-even (limit) prices for a ticket."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import bot

legs = [{"pick": "A", "odds": 1.5}, {"pick": "B", "odds": 1.8}]
p = 0.5
be = bot.breakeven_prices(legs, p)
# at the break-even total the taxed return is zero
assert abs(bot.taxed_return(p, be["total"])) < 0.01, be
# replacing one leg by its break-even price makes the ticket break even
for i, price in enumerate(be["per_leg"]):
    t = 1.0
    for j, l in enumerate(legs):
        t *= price if i == j else l["odds"]
    assert abs(bot.taxed_return(p, t)) < 0.02, (i, t)
assert bot.breakeven_prices([], 0.5) is None and bot.breakeven_prices(legs, 0) is None
line = bot.breakeven_line({"legs": legs, "win_prob": p, "total_odds": 2.7})
assert "Break-even" in line and "A:" in line
assert bot.breakeven_line({"legs": [], "win_prob": None, "total_odds": 1}) == ""
print("breakeven ok")
