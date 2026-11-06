# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 5 | 1 | -18.1% | - | - | - | undecided | - | -100% | 4 |
| Market only (most likely ticket, no AI) | 5 | 0 | - | - | - | - | undecided | - | +15% | 4 |
| The AI's own ticket | 5 | 1 | -18.1% | - | - | - | undecided | - | -34% | 4 |
| Best expected return within the AI's verdicts | 5 | 1 | -18.1% | - | - | - | undecided | - | -100% | 3 |
| Value ticket at the best bookmaker price | 2 | 1 | -8.7% | - | - | - | undecided | - | +196% | 1 |
| Value singles at the best bookmaker price | 13 | 7 | -3.3% | 1.9 | 4% | 1.00 | undecided | - | -6% | 9 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 5 | 5 | -6.3% | 1.7 | 0% | 1.00 | undecided | - | -46% | 5 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 3 | 1 | -12.4% | - | - | - | undecided | - | -100% | 2 |
| One single a day (best value pick the AI allows) | 3 | 1 | -8.4% | - | - | - | undecided | - | -100% | 2 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 2 | 2 | +1.3% | 0.5 | 99% | 1.00 | undecided | - | -46% | 2 |
| Most likely ticket using power-method chances | 3 | 0 | - | - | - | - | undecided | - | -100% | 2 |
| Picks the AI rated AGREE (singles, average price) | 55 | 11 | -12.4% | 0.5 | 0% | 0.00 | undecided | - | -13% | 50 |
| Picks rated RISKY (singles, average price) | 141 | 23 | -11.0% | 0.9 | 0% | 0.00 | loses after tax | - | -8% | 124 |
| Picks rated AVOID (singles, average price) | 75 | 11 | -12.6% | 1.6 | 0% | 0.00 | undecided | - | -8% | 43 |
