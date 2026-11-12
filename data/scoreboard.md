# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 11 | 4 | -9.3% | 5.0 | 3% | 1.00 | undecided | - | -51% | 10 |
| Market only (most likely ticket, no AI) | 11 | 4 | -19.7% | 10.0 | 2% | 1.00 | undecided | +3.4 ± 12.6 (2 d) | -54% | 10 |
| The AI's own ticket | 11 | 3 | -19.2% | 1.8 | 0% | 1.00 | undecided | -3.9 ± 3.9 (2 d) | +53% | 10 |
| Best expected return within the AI's verdicts | 10 | 4 | -13.6% | 6.4 | 2% | 1.00 | undecided | -4.3 ± 2.6 (4 d) | -74% | 9 |
| Value ticket at the best bookmaker price | 5 | 4 | -8.2% | 3.0 | 0% | 1.00 | undecided | +8.2 ± 1.1 (2 d) | -26% | 4 |
| Value singles at the best bookmaker price | 23 | 16 | -8.1% | 2.1 | 0% | 0.00 | undecided | +7.0 ± 3.9 (3 d) | -27% | 21 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 14 | 14 | -6.5% | 0.7 | 0% | 0.00 | undecided | +2.5 ± 4.5 (4 d) | +38% | 14 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 9 | 4 | -4.7% | 5.3 | 19% | 1.00 | undecided | +4.6 ± 0.8 (4 d) | -35% | 8 |
| One single a day (best value pick the AI allows) | 9 | 5 | -5.9% | 2.0 | 0% | 1.00 | undecided | +1.7 ± 3.9 (4 d) | -25% | 8 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 5 | 4 | -3.4% | 4.1 | 20% | 1.00 | undecided | +13.8 ± 5.5 (2 d) | -15% | 4 |
| Most likely ticket using power-method chances | 9 | 4 | -20.9% | 8.8 | 1% | 1.00 | undecided | +1.0 ± 4.1 (2 d) | -71% | 8 |
| The old ticket rule: most likely ticket within the AI's verdicts | 6 | 5 | -12.0% | 5.4 | 1% | 1.00 | undecided | -2.2 ± 2.2 (3 d) | +42% | 5 |
| The real ticket rule at the best bookmaker prices | 6 | 3 | -6.3% | 2.8 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | -6% | 5 |
| Market only, best return after tax (no AI) | 6 | 3 | -24.4% | 11.3 | 2% | 1.00 | undecided | - | -54% | 5 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 3 | 3 | -14.7% | 0.8 | 0% | 1.00 | undecided | - | -20% | 3 |
| Late ticket at the best bookmaker prices (no AI) | 3 | 3 | -9.2% | 1.3 | 0% | 1.00 | undecided | - | +159% | 3 |
| Picks the AI rated AGREE (singles, average price) | 148 | 46 | -10.0% | 0.8 | 0% | 0.00 | loses after tax | +0.4 ± 3.9 (4 d) | -11% | 133 |
| Picks rated RISKY (singles, average price) | 260 | 66 | -11.2% | 0.5 | 0% | 0.00 | loses after tax | -2.5 ± 6.2 (4 d) | -9% | 244 |
| Picks rated AVOID (singles, average price) | 117 | 46 | -12.9% | 0.7 | 0% | 0.00 | loses after tax | -4.9 ± 5.0 (4 d) | -15% | 108 |
