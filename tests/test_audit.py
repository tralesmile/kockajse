"""Checks for the standing audits (audit.py). Run: python tests/test_audit.py"""
import gzip
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import audit  # noqa: E402
from bot import power_devig  # noqa: E402


def pick(base, ai, won, verdict="AGREE"):
    return {"result": "won" if won else "lost", "ai_chance": str(ai), "sharp_chance": str(base),
            "market_chance": "0.5", "verdict": verdict}


# Too few picks: no audit.
assert audit.ai_audit([pick(0.6, 0.6, True)] * 5) is None
# An AI that equals the base chance changes nothing; the gain is exactly zero.
rows = [pick(0.6, 0.6, i % 5 != 0) for i in range(50)]
res = audit.ai_audit(rows)
assert res["n"] == 50 and abs(res["gain"]) < 1e-12 and abs(res["brier"][0.0] - res["brier"][1.0]) < 1e-12
# An AI that knows the outcome helps; a contrarian AI hurts.
good = [pick(0.5, 0.9 if i % 2 else 0.1, i % 2 == 1) for i in range(60)]
bad = [pick(0.5, 0.1 if i % 2 else 0.9, i % 2 == 1) for i in range(60)]
g, b = audit.ai_audit(good), audit.ai_audit(bad)
assert g["gain"] > 0 and g["corr"] > 0.9 and b["gain"] < 0 and b["corr"] < -0.9
assert "helps" in audit._judge(g) and "hurts" in audit._judge(b)
assert "helps" in audit.email_line(g) or "helps" in audit.email_line(g).lower()
# Rows without an AI chance or result are skipped; the sharp chance is preferred over the market's.
mixed = rows + [dict(pick(0.6, 0.6, True), ai_chance=""), dict(pick(0.6, 0.6, True), result="pending")]
assert audit.ai_audit(mixed)["n"] == 50

# Lead-lag: book A matches the close exactly, book B is off by 0.1; A must rank first.
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    (tmp / "odds").mkdir()
    events, closing = [], []
    for i in range(20):
        truth = 0.6
        o_true = [1 / truth, 1 / (1 - truth)]
        a = [round(o_true[0], 4), round(o_true[1], 4)]
        b = [1 / 0.5, 1 / 0.5]
        events.append({"id": f"e{i}", "books": {
            "pinnacle": {"h2h": [["H", None, a[0]], ["A", None, a[1]]]},
            "exact": {"h2h": [["H", None, a[0]], ["A", None, a[1]]]},
            "off": {"h2h": [["H", None, b[0]], ["A", None, b[1]]]}}})
        closing.append({"event_id": f"e{i}", "market": "h2h", "sel": "H", "close_power": "0.6"})
    with gzip.open(tmp / "odds" / "2026-11-10.json.gz", "wt") as fh:
        json.dump({"fetched": "x", "events": events}, fh)
    lead = audit.book_lead_lag(tmp / "odds", closing, power_devig)
    assert lead["n_matches"] == 20 and lead["books"][0][0] in ("exact", "pinnacle")
    assert lead["books"][-1][0] == "off" and abs(lead["books"][-1][2] + 0.1) < 1e-6
    assert audit.book_lead_lag(tmp / "odds", closing[:3], power_devig) is None  # too few
    text = audit.markdown(res, lead)
    assert "| off |" in text and "Brier" in text
    assert "Fewer than" in audit.markdown(None, None)
print("audit tests passed")
