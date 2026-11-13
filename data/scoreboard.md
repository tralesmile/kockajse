# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 12 | 5 | -10.2% | 4.0 | 1% | 1.00 | undecided | - | -55% | 11 |
| Market only (most likely ticket, no AI) | 12 | 5 | -19.7% | 7.8 | 1% | 1.00 | undecided | +0.4 ± 7.9 (3 d) | -37% | 11 |
| The AI's own ticket | 12 | 4 | -19.6% | 1.4 | 0% | 1.00 | undecided | -5.0 ± 2.5 (3 d) | +63% | 11 |
| Best expected return within the AI's verdicts | 11 | 5 | -15.8% | 5.4 | 0% | 1.00 | undecided | -5.6 ± 2.4 (5 d) | -46% | 10 |
| Value ticket at the best bookmaker price | 6 | 5 | -5.9% | 3.3 | 3% | 1.00 | undecided | +11.1 ± 3.0 (3 d) | -41% | 5 |
| Value singles at the best bookmaker price | 24 | 18 | -8.8% | 2.4 | 0% | 0.00 | undecided | +5.0 ± 3.4 (4 d) | -33% | 23 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 15 | 15 | -6.6% | 0.6 | 0% | 0.00 | undecided | +2.5 ± 4.5 (4 d) | +49% | 15 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 3 | 3 | -0.6% | 1.2 | 30% | 1.00 | undecided | +15.7 ± 0.9 (2 d) | -27% | 3 |
| The real ticket at the best bookmaker price (price shopping) | 10 | 5 | -5.4% | 4.1 | 10% | 1.00 | undecided | +4.8 ± 0.6 (5 d) | -42% | 9 |
| One single a day (best value pick the AI allows) | 10 | 6 | -6.5% | 1.7 | 0% | 1.00 | undecided | +2.3 ± 3.1 (5 d) | -20% | 9 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 5 | 5 | -2.1% | 3.4 | 27% | 1.00 | undecided | +14.9 ± 3.4 (3 d) | -9% | 5 |
| Most likely ticket using power-method chances | 10 | 5 | -20.6% | 6.8 | 0% | 1.00 | undecided | -1.2 ± 3.3 (3 d) | -49% | 9 |
| The old ticket rule: most likely ticket within the AI's verdicts | 7 | 6 | -12.3% | 4.4 | 0% | 1.00 | undecided | -1.6 ± 1.6 (4 d) | +19% | 6 |
| The real ticket rule at the best bookmaker prices | 7 | 3 | -6.3% | 2.8 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | -22% | 6 |
| Market only, best return after tax (no AI) | 7 | 3 | -24.4% | 11.3 | 2% | 1.00 | undecided | - | -23% | 6 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 2 | 0 | - | - | - | - | undecided | - | +132% | 1 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 2 | 0 | - | - | - | - | undecided | - | +131% | 1 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 4 | 4 | -14.9% | 0.6 | 0% | 1.00 | undecided | -10.0 ± 7.9 (2 d) | -40% | 4 |
| Late ticket at the best bookmaker prices (no AI) | 4 | 4 | -9.1% | 0.9 | 0% | 1.00 | undecided | -5.1 ± 7.2 (2 d) | +94% | 4 |
| Picks the AI rated AGREE (singles, average price) | 165 | 56 | -10.2% | 0.7 | 0% | 0.00 | loses after tax | +0.9 ± 3.1 (5 d) | -10% | 148 |
| Picks rated RISKY (singles, average price) | 270 | 79 | -11.3% | 0.4 | 0% | 0.00 | loses after tax | -1.6 ± 4.9 (5 d) | -9% | 260 |
| Picks rated AVOID (singles, average price) | 129 | 54 | -12.9% | 0.6 | 0% | 0.00 | loses after tax | -3.8 ± 4.0 (5 d) | -15% | 117 |
