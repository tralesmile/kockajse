# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 6 | 1 | -18.1% | - | - | - | undecided | - | -100% | 5 |
| Market only (most likely ticket, no AI) | 6 | 1 | -15.2% | - | - | - | undecided | - | -8% | 5 |
| The AI's own ticket | 6 | 1 | -18.1% | - | - | - | undecided | - | +2% | 5 |
| Best expected return within the AI's verdicts | 5 | 1 | -18.1% | - | - | - | undecided | - | -100% | 4 |
| Value ticket at the best bookmaker price | 3 | 2 | -7.3% | 1.4 | 0% | 1.00 | undecided | - | +48% | 2 |
| Value singles at the best bookmaker price | 16 | 9 | -6.8% | 3.5 | 2% | 1.00 | undecided | - | -35% | 13 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 7 | 7 | -6.1% | 1.3 | 0% | 1.00 | undecided | - | -38% | 7 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 4 | 1 | -12.4% | - | - | - | undecided | - | -100% | 3 |
| One single a day (best value pick the AI allows) | 4 | 1 | -8.4% | - | - | - | undecided | - | -100% | 3 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 3 | 2 | +1.3% | 0.5 | 99% | 1.00 | undecided | - | -46% | 2 |
| Most likely ticket using power-method chances | 4 | 1 | -15.2% | - | - | - | undecided | - | -100% | 3 |
| The old ticket rule: most likely ticket within the AI's verdicts | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| The real ticket rule at the best bookmaker prices | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Market only, best return after tax (no AI) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Picks the AI rated AGREE (singles, average price) | 63 | 10 | -12.4% | 0.6 | 0% | 0.00 | undecided | - | -12% | 53 |
| Picks rated RISKY (singles, average price) | 149 | 25 | -11.0% | 0.8 | 0% | 0.00 | loses after tax | - | -7% | 141 |
| Picks rated AVOID (singles, average price) | 92 | 20 | -12.6% | 0.9 | 0% | 0.00 | loses after tax | - | -11% | 72 |
