"""Market tiers for the real ticket (17 Nov review): moneylines first, then dc, then anything."""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
cfg = json.loads((ROOT / "config.json").read_text())
assert cfg["ticket_market_tiers"] == [["h2h"], ["h2h", "dc"], None], cfg["ticket_market_tiers"]
assert cfg["paper_mode"] is True and cfg["tax_rate"] == 0.15 and cfg["paper_stake"] == 100
src = (ROOT / "bot.py").read_text()
assert "def search_tax(markets)" in src and '"prev_rule"' in src
import bot
assert "prev_rule" in bot.SHADOW_LEGS_CLV and "prev_rule" in bot.LABELS if hasattr(bot, "LABELS") else True
# tier logic mirrored: first tier with a ticket wins, None means anything
def pick(tiers, tickets):
    for t in tiers:
        ok = [x for x in tickets if t is None or all(m in t for m in x["m"])]
        if ok:
            return max(ok, key=lambda x: x["v"])
tk = [{"m": ["spreads", "h2h"], "v": 0.1}, {"m": ["h2h", "dc"], "v": -0.05}, {"m": ["h2h", "h2h"], "v": -0.1}]
assert pick(cfg["ticket_market_tiers"], tk)["m"] == ["h2h", "h2h"]
assert pick(cfg["ticket_market_tiers"], tk[:2])["m"] == ["h2h", "dc"]
assert pick(cfg["ticket_market_tiers"], tk[:1])["m"] == ["spreads", "h2h"]
print("ok")
