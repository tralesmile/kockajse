# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 15 | 8 | -11.2% | 2.6 | 0% | 1.00 | undecided | - | -48% | 14 |
| Market only (most likely ticket, no AI) | 15 | 8 | -16.3% | 5.0 | 0% | 1.00 | undecided | +1.3 ± 3.6 (6 d) | -34% | 14 |
| The AI's own ticket | 15 | 6 | -17.8% | 1.9 | 0% | 1.00 | undecided | -3.0 ± 1.8 (5 d) | +45% | 14 |
| Best expected return within the AI's verdicts | 14 | 6 | -14.9% | 4.5 | 0% | 1.00 | undecided | -4.7 ± 2.2 (6 d) | -40% | 13 |
| Value ticket at the best bookmaker price | 8 | 8 | -6.3% | 2.2 | 0% | 1.00 | undecided | +8.5 ± 2.0 (6 d) | -63% | 8 |
| Value singles at the best bookmaker price | 30 | 25 | -9.1% | 1.8 | 0% | 0.00 | loses after tax | +4.2 ± 2.0 (7 d) | -39% | 30 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 23 | 23 | -6.1% | 0.7 | 0% | 0.00 | loses after tax | +4.6 ± 2.8 (7 d) | +39% | 23 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 6 | 6 | +1.3% | 1.4 | 83% | 1.00 | undecided | +15.0 ± 0.9 (3 d) | -16% | 6 |
| The real ticket at the best bookmaker price (price shopping) | 13 | 8 | -6.6% | 2.8 | 1% | 1.00 | undecided | +4.6 ± 0.5 (8 d) | -36% | 12 |
| One single a day (best value pick the AI allows) | 13 | 8 | -6.7% | 1.3 | 0% | 1.00 | undecided | +3.7 ± 2.5 (7 d) | -15% | 12 |
| Value singles that still pay after the 15% tax | 1 | 1 | -7.2% | - | - | - | undecided | - | -100% | 1 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 6 | 6 | -1.5% | 2.9 | 30% | 1.00 | undecided | +14.1 ± 2.5 (4 d) | -2% | 6 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 10 | 3 | -2.2% | 1.6 | 8% | 1.00 | undecided | - | -18% | 8 |
| Most likely ticket using power-method chances | 13 | 7 | -18.2% | 5.0 | 0% | 1.00 | undecided | +0.3 ± 2.3 (5 d) | -24% | 12 |
| The old ticket rule: most likely ticket within the AI's verdicts | 10 | 8 | -12.9% | 3.2 | 0% | 1.00 | undecided | -1.3 ± 1.5 (6 d) | +30% | 9 |
| The real ticket rule at the best bookmaker prices | 10 | 4 | -6.4% | 2.0 | 0% | 1.00 | undecided | +6.6 ± 1.7 (3 d) | +5% | 9 |
| Market only, best return after tax (no AI) | 10 | 4 | -20.0% | 9.2 | 1% | 1.00 | undecided | -1.4 ± 5.2 (2 d) | -22% | 9 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 5 | 1 | -10.8% | - | - | - | undecided | - | +73% | 4 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 5 | 0 | - | - | - | - | undecided | - | +17% | 4 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 7 | 7 | -15.7% | 0.9 | 0% | 1.00 | undecided | -6.6 ± 3.7 (5 d) | -0% | 7 |
| Late ticket at the best bookmaker prices (no AI) | 7 | 7 | -10.3% | 0.9 | 0% | 1.00 | undecided | -1.0 ± 3.7 (5 d) | +79% | 7 |
| Picks the AI rated AGREE (singles, average price) | 193 | 80 | -10.0% | 0.5 | 0% | 0.00 | loses after tax | +1.8 ± 2.1 (8 d) | -8% | 189 |
| Picks rated RISKY (singles, average price) | 336 | 115 | -11.6% | 0.4 | 0% | 0.00 | loses after tax | -0.6 ± 3.2 (8 d) | -10% | 320 |
| Picks rated AVOID (singles, average price) | 171 | 77 | -13.1% | 0.5 | 0% | 0.00 | loses after tax | -2.5 ± 2.8 (8 d) | -15% | 155 |
