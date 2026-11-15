# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 14 | 7 | -11.3% | 3.0 | 0% | 1.00 | undecided | - | -62% | 13 |
| Market only (most likely ticket, no AI) | 14 | 7 | -17.1% | 5.7 | 0% | 1.00 | undecided | +1.7 ± 4.4 (5 d) | -47% | 13 |
| The AI's own ticket | 14 | 6 | -17.8% | 1.9 | 0% | 1.00 | undecided | -3.0 ± 1.8 (5 d) | +38% | 13 |
| Best expected return within the AI's verdicts | 13 | 5 | -15.8% | 5.4 | 0% | 1.00 | undecided | -5.6 ± 2.4 (5 d) | -55% | 12 |
| Value ticket at the best bookmaker price | 8 | 7 | -7.0% | 2.4 | 0% | 1.00 | undecided | +8.4 ± 2.5 (5 d) | -58% | 7 |
| Value singles at the best bookmaker price | 30 | 20 | -8.9% | 2.2 | 0% | 0.00 | loses after tax | +4.8 ± 2.3 (6 d) | -38% | 25 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 20 | 20 | -6.6% | 0.5 | 0% | 0.00 | loses after tax | +4.1 ± 3.3 (6 d) | +52% | 20 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 3 | 3 | -0.6% | 1.2 | 30% | 1.00 | undecided | +15.7 ± 0.9 (2 d) | -27% | 3 |
| The real ticket at the best bookmaker price (price shopping) | 12 | 7 | -6.6% | 3.2 | 2% | 1.00 | undecided | +4.7 ± 0.5 (7 d) | -53% | 11 |
| One single a day (best value pick the AI allows) | 12 | 7 | -6.6% | 1.5 | 0% | 1.00 | undecided | +3.8 ± 2.9 (6 d) | -24% | 11 |
| Value singles that still pay after the 15% tax | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 6 | 5 | -2.1% | 3.4 | 27% | 1.00 | undecided | +14.9 ± 3.4 (3 d) | -9% | 5 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 8 | 0 | - | - | - | - | undecided | - | -11% | 5 |
| Most likely ticket using power-method chances | 12 | 6 | -19.4% | 5.7 | 0% | 1.00 | undecided | +0.5 ± 2.9 (4 d) | -38% | 11 |
| The old ticket rule: most likely ticket within the AI's verdicts | 9 | 8 | -12.9% | 3.2 | 0% | 1.00 | undecided | -1.3 ± 1.5 (6 d) | +18% | 8 |
| The real ticket rule at the best bookmaker prices | 9 | 3 | -6.3% | 2.8 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | -13% | 8 |
| Market only, best return after tax (no AI) | 9 | 3 | -24.4% | 11.3 | 2% | 1.00 | undecided | - | -42% | 8 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 4 | 0 | - | - | - | - | undecided | - | +54% | 3 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 4 | 0 | - | - | - | - | undecided | - | +56% | 3 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 5 | 5 | -14.9% | 0.5 | 0% | 1.00 | undecided | -5.5 ± 4.5 (4 d) | -6% | 5 |
| Late ticket at the best bookmaker prices (no AI) | 5 | 5 | -9.3% | 0.7 | 0% | 1.00 | undecided | -0.2 ± 4.7 (4 d) | +55% | 5 |
| Picks the AI rated AGREE (singles, average price) | 189 | 72 | -10.0% | 0.6 | 0% | 0.00 | loses after tax | +2.1 ± 2.4 (7 d) | -8% | 175 |
| Picks rated RISKY (singles, average price) | 320 | 101 | -11.6% | 0.5 | 0% | 0.00 | loses after tax | -0.4 ± 3.7 (7 d) | -10% | 298 |
| Picks rated AVOID (singles, average price) | 155 | 70 | -13.0% | 0.5 | 0% | 0.00 | loses after tax | -2.4 ± 3.3 (7 d) | -15% | 145 |
