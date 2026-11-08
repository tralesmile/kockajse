# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 7 | 2 | -13.5% | 4.6 | 0% | 1.00 | undecided | - | -100% | 6 |
| Market only (most likely ticket, no AI) | 7 | 2 | -16.6% | 1.4 | 0% | 1.00 | undecided | - | -23% | 6 |
| The AI's own ticket | 7 | 2 | -17.4% | 0.7 | 0% | 1.00 | undecided | -3.9 ± 3.9 (2 d) | -15% | 6 |
| Best expected return within the AI's verdicts | 6 | 2 | -16.8% | 1.3 | 0% | 1.00 | undecided | -3.3 ± 3.3 (2 d) | -100% | 5 |
| Value ticket at the best bookmaker price | 3 | 3 | -5.5% | 2.0 | 0% | 1.00 | undecided | +8.2 ± 1.1 (2 d) | -1% | 3 |
| Value singles at the best bookmaker price | 19 | 12 | -6.8% | 2.6 | 0% | 0.15 | undecided | +8.3 ± 6.4 (2 d) | -25% | 16 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 12 | 12 | -6.4% | 0.8 | 0% | 0.00 | undecided | +7.1 ± 4.7 (2 d) | +18% | 12 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 5 | 2 | -8.1% | 4.3 | 3% | 1.00 | undecided | +5.4 ± 0.3 (2 d) | -100% | 4 |
| One single a day (best value pick the AI allows) | 5 | 2 | -9.1% | 0.7 | 0% | 1.00 | undecided | +4.4 ± 5.3 (2 d) | -56% | 4 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 3 | 3 | +0.6% | 0.7 | 82% | 1.00 | undecided | +13.8 ± 5.5 (2 d) | -26% | 3 |
| Most likely ticket using power-method chances | 5 | 2 | -13.6% | 1.6 | 0% | 1.00 | undecided | - | -43% | 4 |
| The old ticket rule: most likely ticket within the AI's verdicts | 2 | 1 | -15.5% | - | - | - | undecided | - | -100% | 1 |
| The real ticket rule at the best bookmaker prices | 2 | 1 | -2.1% | - | - | - | undecided | - | +141% | 1 |
| Market only, best return after tax (no AI) | 2 | 1 | -15.5% | - | - | - | undecided | - | -100% | 1 |
| Picks the AI rated AGREE (singles, average price) | 69 | 20 | -10.7% | 1.0 | 0% | 0.00 | loses after tax | +2.9 ± 3.0 (2 d) | -11% | 63 |
| Picks rated RISKY (singles, average price) | 173 | 33 | -10.7% | 0.6 | 0% | 0.00 | loses after tax | +3.3 ± 4.1 (2 d) | -6% | 149 |
| Picks rated AVOID (singles, average price) | 96 | 40 | -12.8% | 0.8 | 0% | 0.00 | loses after tax | -0.3 ± 3.8 (2 d) | -9% | 92 |
