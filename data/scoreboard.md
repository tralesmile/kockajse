# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 13 | 6 | -11.7% | 3.6 | 0% | 1.00 | undecided | - | -59% | 12 |
| Market only (most likely ticket, no AI) | 13 | 6 | -18.6% | 6.4 | 0% | 1.00 | undecided | +1.7 ± 5.7 (4 d) | -43% | 12 |
| The AI's own ticket | 13 | 5 | -19.5% | 1.1 | 0% | 1.00 | undecided | -3.7 ± 2.2 (4 d) | +50% | 12 |
| Best expected return within the AI's verdicts | 12 | 5 | -15.8% | 5.4 | 0% | 1.00 | undecided | -5.6 ± 2.4 (5 d) | -51% | 11 |
| Value ticket at the best bookmaker price | 7 | 6 | -6.9% | 2.8 | 1% | 1.00 | undecided | +10.1 ± 2.3 (4 d) | -51% | 6 |
| Value singles at the best bookmaker price | 25 | 19 | -9.0% | 2.3 | 0% | 0.00 | undecided | +5.4 ± 2.7 (5 d) | -36% | 24 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 19 | 19 | -6.7% | 0.5 | 0% | 0.00 | undecided | +4.4 ± 4.0 (5 d) | +47% | 19 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 3 | 3 | -0.6% | 1.2 | 30% | 1.00 | undecided | +15.7 ± 0.9 (2 d) | -27% | 3 |
| The real ticket at the best bookmaker price (price shopping) | 11 | 6 | -7.1% | 3.8 | 3% | 1.00 | undecided | +4.6 ± 0.6 (6 d) | -48% | 10 |
| One single a day (best value pick the AI allows) | 11 | 7 | -6.6% | 1.5 | 0% | 1.00 | undecided | +3.8 ± 2.9 (6 d) | -28% | 10 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 5 | 5 | -2.1% | 3.4 | 27% | 1.00 | undecided | +14.9 ± 3.4 (3 d) | -9% | 5 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 5 | 0 | - | - | - | - | undecided | - | - | 0 |
| Most likely ticket using power-method chances | 11 | 6 | -19.4% | 5.7 | 0% | 1.00 | undecided | +0.5 ± 2.9 (4 d) | -54% | 10 |
| The old ticket rule: most likely ticket within the AI's verdicts | 8 | 7 | -12.8% | 3.7 | 0% | 1.00 | undecided | -0.6 ± 1.6 (5 d) | +2% | 7 |
| The real ticket rule at the best bookmaker prices | 8 | 3 | -6.3% | 2.8 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | -0% | 7 |
| Market only, best return after tax (no AI) | 8 | 3 | -24.4% | 11.3 | 2% | 1.00 | undecided | - | -34% | 7 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 3 | 0 | - | - | - | - | undecided | - | +132% | 2 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 3 | 0 | - | - | - | - | undecided | - | +134% | 2 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 5 | 5 | -14.9% | 0.5 | 0% | 1.00 | undecided | -5.5 ± 6.4 (3 d) | -6% | 5 |
| Late ticket at the best bookmaker prices (no AI) | 5 | 5 | -9.3% | 0.7 | 0% | 1.00 | undecided | +0.0 ± 6.6 (3 d) | +55% | 5 |
| Picks the AI rated AGREE (singles, average price) | 175 | 65 | -10.2% | 0.6 | 0% | 0.00 | loses after tax | +2.2 ± 2.8 (6 d) | -8% | 165 |
| Picks rated RISKY (singles, average price) | 298 | 84 | -11.3% | 0.4 | 0% | 0.00 | loses after tax | +0.1 ± 4.3 (6 d) | -11% | 270 |
| Picks rated AVOID (singles, average price) | 145 | 62 | -12.7% | 0.6 | 0% | 0.00 | loses after tax | -1.9 ± 3.8 (6 d) | -15% | 129 |
