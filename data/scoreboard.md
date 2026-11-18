# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 17 | 8 | -11.2% | 2.6 | 0% | 1.00 | undecided | - | -39% | 16 |
| Market only (most likely ticket, no AI) | 17 | 8 | -16.3% | 5.0 | 0% | 1.00 | undecided | +1.3 ± 3.6 (6 d) | -14% | 16 |
| The AI's own ticket | 17 | 6 | -17.8% | 1.9 | 0% | 1.00 | undecided | -3.0 ± 1.8 (5 d) | +26% | 16 |
| Best expected return within the AI's verdicts | 16 | 6 | -14.9% | 4.5 | 0% | 1.00 | undecided | -4.7 ± 2.2 (6 d) | -32% | 15 |
| Value ticket at the best bookmaker price | 9 | 9 | -6.8% | 2.0 | 0% | 1.00 | undecided | +8.5 ± 2.0 (6 d) | -67% | 9 |
| Value singles at the best bookmaker price | 35 | 28 | -9.3% | 1.6 | 0% | 0.00 | loses after tax | +4.2 ± 2.0 (7 d) | -37% | 35 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 28 | 28 | -6.0% | 0.6 | 0% | 0.00 | loses after tax | +4.6 ± 2.8 (7 d) | +39% | 28 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 6 | 6 | +1.3% | 1.4 | 83% | 1.00 | undecided | +15.0 ± 0.9 (3 d) | -16% | 6 |
| The real ticket at the best bookmaker price (price shopping) | 15 | 8 | -6.6% | 2.8 | 1% | 1.00 | undecided | +4.6 ± 0.5 (8 d) | -26% | 14 |
| One single a day (best value pick the AI allows) | 15 | 8 | -6.7% | 1.3 | 0% | 1.00 | undecided | +3.7 ± 2.5 (7 d) | -14% | 14 |
| Value singles that still pay after the 15% tax | 3 | 3 | -11.4% | 2.5 | 0% | 1.00 | undecided | - | -100% | 3 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 6 | 6 | -1.5% | 2.9 | 30% | 1.00 | undecided | +14.1 ± 2.5 (4 d) | -2% | 6 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 18 | 5 | -1.3% | 1.1 | 11% | 1.00 | undecided | - | -12% | 14 |
| The previous real-ticket rule (all bet types, best return after tax) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Banker: the single most likely bet of the day (power chance, best price) | 2 | 0 | - | - | - | - | undecided | - | +6% | 1 |
| Banker double: the two most likely bets on different matches (best price) | 2 | 0 | - | - | - | - | undecided | - | +17% | 1 |
| Most likely ticket using power-method chances | 15 | 8 | -17.0% | 4.4 | 0% | 1.00 | undecided | +0.3 ± 2.3 (5 d) | -18% | 14 |
| The old ticket rule: most likely ticket within the AI's verdicts | 12 | 8 | -12.9% | 3.2 | 0% | 1.00 | undecided | -1.3 ± 1.5 (6 d) | +7% | 11 |
| The real ticket rule at the best bookmaker prices | 12 | 4 | -6.4% | 2.0 | 0% | 1.00 | undecided | +6.6 ± 1.7 (3 d) | +7% | 11 |
| Market only, best return after tax (no AI) | 12 | 4 | -20.0% | 9.2 | 1% | 1.00 | undecided | -1.4 ± 5.2 (2 d) | +6% | 11 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 2 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| AI as veto only, at the best bookmaker prices | 2 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 7 | 1 | -10.8% | - | - | - | undecided | - | +93% | 6 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 7 | 0 | - | - | - | - | undecided | - | +28% | 6 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 9 | 9 | -15.8% | 0.8 | 0% | 1.00 | undecided | -6.6 ± 3.7 (5 d) | +3% | 9 |
| Late ticket at the best bookmaker prices (no AI) | 9 | 9 | -10.9% | 0.9 | 0% | 1.00 | undecided | -1.0 ± 3.7 (5 d) | +73% | 9 |
| Picks the AI rated AGREE (singles, average price) | 210 | 89 | -9.9% | 0.5 | 0% | 0.00 | loses after tax | +1.8 ± 2.1 (8 d) | -10% | 206 |
| Picks rated RISKY (singles, average price) | 367 | 125 | -11.6% | 0.4 | 0% | 0.00 | loses after tax | -0.6 ± 3.2 (8 d) | -12% | 349 |
| Picks rated AVOID (singles, average price) | 197 | 92 | -13.2% | 0.5 | 0% | 0.00 | loses after tax | -2.5 ± 2.8 (8 d) | -11% | 187 |
