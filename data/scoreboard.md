# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 8 | 3 | -13.9% | 2.7 | 0% | 1.00 | undecided | - | -100% | 7 |
| Market only (most likely ticket, no AI) | 8 | 3 | -10.6% | 6.0 | 4% | 1.00 | undecided | +3.4 ± 12.6 (2 d) | -34% | 7 |
| The AI's own ticket | 8 | 2 | -17.4% | 0.7 | 0% | 1.00 | undecided | -3.9 ± 3.9 (2 d) | +10% | 7 |
| Best expected return within the AI's verdicts | 7 | 3 | -19.7% | 3.0 | 0% | 1.00 | undecided | -5.8 ± 3.1 (3 d) | -100% | 6 |
| Value ticket at the best bookmaker price | 4 | 3 | -5.5% | 2.0 | 0% | 1.00 | undecided | +8.2 ± 1.1 (2 d) | -1% | 3 |
| Value singles at the best bookmaker price | 20 | 15 | -7.5% | 2.2 | 0% | 0.02 | undecided | +7.0 ± 3.9 (3 d) | -19% | 19 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 13 | 13 | -6.6% | 0.7 | 0% | 0.00 | undecided | +6.6 ± 2.7 (3 d) | +34% | 13 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 6 | 3 | -9.5% | 2.9 | 0% | 1.00 | undecided | +4.3 ± 1.0 (3 d) | -100% | 5 |
| One single a day (best value pick the AI allows) | 6 | 3 | -9.0% | 0.4 | 0% | 1.00 | undecided | +4.8 ± 3.1 (3 d) | -29% | 5 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 3 | 3 | +0.6% | 0.7 | 82% | 1.00 | undecided | +13.8 ± 5.5 (2 d) | -26% | 3 |
| Most likely ticket using power-method chances | 6 | 3 | -12.2% | 1.6 | 0% | 1.00 | undecided | +1.0 ± 4.1 (2 d) | -54% | 5 |
| The old ticket rule: most likely ticket within the AI's verdicts | 3 | 2 | -15.1% | 0.4 | 0% | 1.00 | undecided | -3.3 ± 3.3 (2 d) | -100% | 2 |
| The real ticket rule at the best bookmaker prices | 3 | 2 | -3.7% | 1.6 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | +20% | 2 |
| Market only, best return after tax (no AI) | 3 | 1 | -15.5% | - | - | - | undecided | - | +14% | 2 |
| Picks the AI rated AGREE (singles, average price) | 96 | 25 | -10.2% | 0.9 | 0% | 0.00 | loses after tax | +4.0 ± 2.0 (3 d) | -11% | 69 |
| Picks rated RISKY (singles, average price) | 200 | 51 | -10.7% | 0.5 | 0% | 0.00 | loses after tax | +3.5 ± 2.3 (3 d) | -9% | 173 |
| Picks rated AVOID (singles, average price) | 96 | 44 | -12.9% | 0.7 | 0% | 0.00 | loses after tax | -0.1 ± 2.2 (3 d) | -11% | 96 |
