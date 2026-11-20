# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 19 | 9 | -10.5% | 2.4 | 0% | 1.00 | undecided | - | -32% | 18 |
| Market only (most likely ticket, no AI) | 19 | 10 | -16.4% | 3.9 | 0% | 0.01 | undecided | -0.3 ± 3.5 (7 d) | -24% | 18 |
| The AI's own ticket | 19 | 7 | -17.6% | 1.6 | 0% | 1.00 | undecided | -4.4 ± 2.1 (6 d) | +27% | 18 |
| Best expected return within the AI's verdicts | 18 | 7 | -14.4% | 3.9 | 0% | 1.00 | undecided | -4.9 ± 1.9 (7 d) | -10% | 17 |
| Value ticket at the best bookmaker price | 10 | 9 | -6.8% | 2.0 | 0% | 1.00 | undecided | +8.5 ± 2.0 (6 d) | -67% | 9 |
| Value singles at the best bookmaker price | 39 | 29 | -9.3% | 1.6 | 0% | 0.00 | loses after tax | +4.2 ± 2.0 (7 d) | -38% | 36 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 32 | 32 | -6.0% | 0.5 | 0% | 0.00 | loses after tax | +4.7 ± 2.4 (8 d) | +28% | 32 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 6 | 6 | +1.3% | 1.4 | 83% | 1.00 | undecided | +15.0 ± 0.9 (3 d) | -16% | 6 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 5 | 5 | -0.9% | 0.1 | 0% | 1.00 | undecided | - | -15% | 5 |
| The real ticket at the best bookmaker price (price shopping) | 17 | 9 | -5.5% | 2.7 | 2% | 1.00 | undecided | +5.0 ± 0.6 (9 d) | -19% | 16 |
| One single a day (best value pick the AI allows) | 17 | 10 | -7.6% | 1.2 | 0% | 0.00 | undecided | +2.5 ± 2.5 (8 d) | -16% | 16 |
| Value singles that still pay after the 15% tax | 4 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -100% | 4 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 8 | 7 | -2.7% | 2.7 | 16% | 1.00 | undecided | +14.1 ± 2.5 (4 d) | -16% | 7 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 24 | 11 | -1.4% | 0.5 | 1% | 1.00 | undecided | +5.7 ± 2.4 (2 d) | -10% | 21 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 8 | 3 | -3.6% | 3.2 | 13% | 1.00 | undecided | - | -17% | 4 |
| The previous real-ticket rule (all bet types, best return after tax) | 3 | 1 | -11.3% | - | - | - | undecided | - | +152% | 2 |
| Banker: the single most likely bet of the day (power chance, best price) | 4 | 2 | -0.1% | 0.9 | 46% | 1.00 | undecided | - | +6% | 3 |
| Banker double: the two most likely bets on different matches (best price) | 4 | 1 | -2.9% | - | - | - | undecided | - | -23% | 3 |
| Most likely ticket using power-method chances | 17 | 10 | -17.0% | 3.5 | 0% | 0.00 | undecided | -1.4 ± 2.6 (6 d) | -29% | 16 |
| The old ticket rule: most likely ticket within the AI's verdicts | 14 | 9 | -12.3% | 2.9 | 0% | 1.00 | undecided | -1.4 ± 1.3 (7 d) | +8% | 13 |
| The real ticket rule at the best bookmaker prices | 14 | 5 | -4.6% | 2.4 | 3% | 1.00 | undecided | +7.0 ± 1.2 (4 d) | +29% | 13 |
| Market only, best return after tax (no AI) | 14 | 5 | -19.3% | 7.1 | 0% | 1.00 | undecided | -4.7 ± 4.4 (3 d) | +8% | 13 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 4 | 2 | -11.1% | 0.2 | 0% | 1.00 | undecided | - | -12% | 3 |
| AI as veto only, at the best bookmaker prices | 4 | 1 | -5.3% | - | - | - | undecided | - | -7% | 3 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 9 | 2 | -14.5% | 3.7 | 0% | 1.00 | undecided | - | +76% | 8 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 9 | 0 | - | - | - | - | undecided | - | +26% | 8 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 11 | 11 | -15.7% | 0.8 | 0% | 0.00 | undecided | -7.0 ± 3.0 (6 d) | +5% | 11 |
| Late ticket at the best bookmaker prices (no AI) | 11 | 11 | -10.2% | 0.8 | 0% | 0.00 | undecided | -1.8 ± 3.1 (6 d) | +42% | 11 |
| Picks the AI rated AGREE (singles, average price) | 227 | 96 | -9.5% | 0.5 | 0% | 0.00 | loses after tax | +1.5 ± 1.9 (9 d) | -8% | 222 |
| Picks rated RISKY (singles, average price) | 416 | 140 | -11.7% | 0.4 | 0% | 0.00 | loses after tax | -1.3 ± 2.9 (9 d) | -12% | 375 |
| Picks rated AVOID (singles, average price) | 226 | 106 | -13.1% | 0.4 | 0% | 0.00 | loses after tax | -3.2 ± 2.6 (9 d) | -9% | 223 |
