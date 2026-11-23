# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 22 | 11 | -12.1% | 2.3 | 0% | 0.00 | undecided | - | -30% | 21 |
| Market only (most likely ticket, no AI) | 22 | 11 | -16.5% | 3.5 | 0% | 0.00 | undecided | +0.6 ± 3.2 (8 d) | -35% | 21 |
| The AI's own ticket | 22 | 9 | -18.8% | 1.5 | 0% | 1.00 | undecided | -4.2 ± 1.7 (8 d) | +32% | 21 |
| Best expected return within the AI's verdicts | 21 | 10 | -16.4% | 2.9 | 0% | 0.00 | undecided | -4.5 ± 2.0 (9 d) | +2% | 20 |
| Value ticket at the best bookmaker price | 13 | 11 | -7.1% | 1.6 | 0% | 0.00 | undecided | +9.2 ± 1.7 (8 d) | -27% | 12 |
| Value singles at the best bookmaker price | 55 | 40 | -8.6% | 1.2 | 0% | 0.00 | loses after tax | +6.0 ± 2.1 (9 d) | -25% | 54 |
| Kaunitz singles (best price far above the average) | 2 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 40 | 40 | -5.9% | 0.4 | 0% | 0.00 | loses after tax | +5.3 ± 2.2 (9 d) | +14% | 40 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 10 | 10 | +1.5% | 0.8 | 97% | 1.00 | undecided | +15.2 ± 0.7 (4 d) | -2% | 10 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 13 | 13 | -0.1% | 0.4 | 44% | 1.00 | undecided | +19.4 ± 4.2 (2 d) | -5% | 13 |
| The real ticket at the best bookmaker price (price shopping) | 20 | 11 | -6.7% | 2.5 | 0% | 0.12 | undecided | +5.4 ± 0.6 (11 d) | -18% | 19 |
| One single a day (best value pick the AI allows) | 20 | 13 | -7.5% | 1.1 | 0% | 0.00 | undecided | +4.9 ± 2.5 (10 d) | -5% | 19 |
| Value singles that still pay after the 15% tax | 4 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -100% | 4 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 13 | 12 | -2.2% | 1.7 | 10% | 1.00 | undecided | +14.3 ± 1.6 (6 d) | -8% | 13 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 35 | 21 | -1.0% | 0.4 | 1% | 1.00 | undecided | +12.0 ± 4.1 (4 d) | -3% | 35 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 19 | 14 | -1.4% | 0.8 | 4% | 1.00 | undecided | +18.4 ± 3.8 (2 d) | +3% | 19 |
| The previous real-ticket rule (all bet types, best return after tax) | 6 | 3 | -17.7% | 3.3 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +149% | 5 |
| Banker: the single most likely bet of the day (power chance, best price) | 7 | 3 | -0.7% | 0.8 | 19% | 1.00 | undecided | +13.4 ± 9.1 (2 d) | -12% | 6 |
| Banker double: the two most likely bets on different matches (best price) | 7 | 2 | -4.0% | 1.1 | 0% | 1.00 | undecided | +10.9 ± 8.5 (2 d) | -23% | 6 |
| Most likely ticket using power-method chances | 20 | 11 | -17.0% | 3.2 | 0% | 0.00 | undecided | -0.2 ± 2.5 (7 d) | -28% | 19 |
| The old ticket rule: most likely ticket within the AI's verdicts | 17 | 11 | -13.9% | 2.6 | 0% | 0.00 | undecided | -1.5 ± 1.5 (9 d) | +31% | 16 |
| The real ticket rule at the best bookmaker prices | 17 | 7 | -3.6% | 1.8 | 2% | 1.00 | undecided | +10.7 ± 3.1 (6 d) | +33% | 16 |
| Market only, best return after tax (no AI) | 17 | 6 | -18.8% | 5.8 | 0% | 1.00 | undecided | -1.5 ± 4.5 (4 d) | -12% | 16 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 7 | 4 | -16.0% | 2.9 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +29% | 6 |
| AI as veto only, at the best bookmaker prices | 7 | 3 | -3.4% | 1.1 | 0% | 1.00 | undecided | +11.2 ± 6.6 (3 d) | +35% | 6 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 12 | 3 | -15.2% | 2.2 | 0% | 1.00 | undecided | +3.8 ± 4.3 (2 d) | +28% | 11 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 12 | 0 | - | - | - | - | undecided | - | +15% | 11 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 13 | 13 | -15.8% | 0.6 | 0% | 0.00 | undecided | -4.7 ± 2.8 (8 d) | +13% | 13 |
| Late ticket at the best bookmaker prices (no AI) | 13 | 13 | -10.7% | 0.8 | 0% | 0.00 | undecided | +0.9 ± 3.2 (8 d) | +20% | 13 |
| Picks the AI rated AGREE (singles, average price) | 250 | 113 | -9.5% | 0.5 | 0% | 0.00 | loses after tax | +3.0 ± 1.9 (11 d) | -7% | 244 |
| Picks rated RISKY (singles, average price) | 484 | 176 | -11.5% | 0.3 | 0% | 0.00 | loses after tax | +0.5 ± 2.7 (11 d) | -11% | 439 |
| Picks rated AVOID (singles, average price) | 248 | 115 | -13.3% | 0.4 | 0% | 0.00 | loses after tax | -1.8 ± 2.4 (11 d) | -10% | 236 |
