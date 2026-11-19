# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 18 | 9 | -10.5% | 2.4 | 0% | 1.00 | undecided | - | -28% | 17 |
| Market only (most likely ticket, no AI) | 18 | 9 | -16.2% | 4.4 | 0% | 1.00 | undecided | -0.3 ± 3.5 (7 d) | -19% | 17 |
| The AI's own ticket | 18 | 7 | -17.6% | 1.6 | 0% | 1.00 | undecided | -4.4 ± 2.1 (6 d) | +35% | 17 |
| Best expected return within the AI's verdicts | 17 | 7 | -14.4% | 3.9 | 0% | 1.00 | undecided | -4.9 ± 1.9 (7 d) | -20% | 16 |
| Value ticket at the best bookmaker price | 9 | 9 | -6.8% | 2.0 | 0% | 1.00 | undecided | +8.5 ± 2.0 (6 d) | -67% | 9 |
| Value singles at the best bookmaker price | 36 | 28 | -9.3% | 1.6 | 0% | 0.00 | loses after tax | +4.2 ± 2.0 (7 d) | -37% | 35 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 32 | 32 | -6.0% | 0.5 | 0% | 0.00 | loses after tax | +4.7 ± 2.4 (8 d) | +28% | 32 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 6 | 6 | +1.3% | 1.4 | 83% | 1.00 | undecided | +15.0 ± 0.9 (3 d) | -16% | 6 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 3 | 3 | -1.0% | 0.1 | 0% | 1.00 | undecided | - | -29% | 3 |
| The real ticket at the best bookmaker price (price shopping) | 16 | 9 | -5.5% | 2.7 | 2% | 1.00 | undecided | +5.0 ± 0.6 (9 d) | -13% | 15 |
| One single a day (best value pick the AI allows) | 16 | 9 | -7.2% | 1.2 | 0% | 1.00 | undecided | +2.5 ± 2.5 (8 d) | -10% | 15 |
| Value singles that still pay after the 15% tax | 4 | 3 | -11.4% | 2.5 | 0% | 1.00 | undecided | - | -100% | 3 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 7 | 6 | -1.5% | 2.9 | 30% | 1.00 | undecided | +14.1 ± 2.5 (4 d) | -2% | 6 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 21 | 9 | -1.6% | 0.6 | 0% | 1.00 | undecided | +5.7 ± 2.4 (2 d) | -13% | 18 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 4 | 0 | - | - | - | - | undecided | - | - | 0 |
| The previous real-ticket rule (all bet types, best return after tax) | 2 | 1 | -11.3% | - | - | - | undecided | - | +163% | 1 |
| Banker: the single most likely bet of the day (power chance, best price) | 3 | 1 | -1.0% | - | - | - | undecided | - | +6% | 2 |
| Banker double: the two most likely bets on different matches (best price) | 3 | 1 | -2.9% | - | - | - | undecided | - | -42% | 2 |
| Most likely ticket using power-method chances | 16 | 9 | -16.8% | 3.9 | 0% | 1.00 | undecided | -1.4 ± 2.6 (6 d) | -24% | 15 |
| The old ticket rule: most likely ticket within the AI's verdicts | 13 | 9 | -12.3% | 2.9 | 0% | 1.00 | undecided | -1.4 ± 1.3 (7 d) | +17% | 12 |
| The real ticket rule at the best bookmaker prices | 13 | 5 | -4.6% | 2.4 | 3% | 1.00 | undecided | +7.0 ± 1.2 (4 d) | +20% | 12 |
| Market only, best return after tax (no AI) | 13 | 5 | -19.3% | 7.1 | 0% | 1.00 | undecided | -4.7 ± 4.4 (3 d) | +17% | 12 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 3 | 1 | -11.3% | - | - | - | undecided | - | +31% | 2 |
| AI as veto only, at the best bookmaker prices | 3 | 1 | -5.3% | - | - | - | undecided | - | +40% | 2 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 8 | 1 | -10.8% | - | - | - | undecided | - | +102% | 7 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 8 | 0 | - | - | - | - | undecided | - | +44% | 7 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 10 | 10 | -15.4% | 0.8 | 0% | 0.00 | undecided | -7.0 ± 3.0 (6 d) | +16% | 10 |
| Late ticket at the best bookmaker prices (no AI) | 10 | 10 | -10.3% | 0.9 | 0% | 0.00 | undecided | -1.8 ± 3.1 (6 d) | +56% | 10 |
| Picks the AI rated AGREE (singles, average price) | 222 | 93 | -9.7% | 0.5 | 0% | 0.00 | loses after tax | +1.5 ± 1.9 (9 d) | -9% | 210 |
| Picks rated RISKY (singles, average price) | 375 | 136 | -11.6% | 0.4 | 0% | 0.00 | loses after tax | -1.3 ± 2.9 (9 d) | -12% | 367 |
| Picks rated AVOID (singles, average price) | 223 | 95 | -13.2% | 0.4 | 0% | 0.00 | loses after tax | -3.2 ± 2.6 (9 d) | -12% | 197 |
