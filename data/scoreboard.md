# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 23 | 12 | -13.6% | 2.6 | 0% | 0.00 | undecided | - | -34% | 22 |
| Market only (most likely ticket, no AI) | 23 | 11 | -16.5% | 3.5 | 0% | 0.00 | undecided | +0.6 ± 3.2 (8 d) | -27% | 22 |
| The AI's own ticket | 23 | 10 | -19.9% | 1.7 | 0% | 0.00 | undecided | -3.7 ± 1.6 (9 d) | +26% | 22 |
| Best expected return within the AI's verdicts | 22 | 10 | -16.4% | 2.9 | 0% | 0.00 | undecided | -4.5 ± 2.0 (9 d) | +10% | 21 |
| Value ticket at the best bookmaker price | 14 | 12 | -7.1% | 1.5 | 0% | 0.00 | undecided | +10.7 ± 2.1 (9 d) | -14% | 13 |
| Value singles at the best bookmaker price | 61 | 41 | -8.6% | 1.2 | 0% | 0.00 | loses after tax | +7.6 ± 2.5 (10 d) | -22% | 55 |
| Kaunitz singles (best price far above the average) | 2 | 1 | +1.0% | - | - | - | undecided | - | -100% | 2 |
| Late value singles (best price minutes before kick-off) | 44 | 44 | -5.9% | 0.4 | 0% | 0.00 | loses after tax | +7.1 ± 2.7 (10 d) | +8% | 44 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 10 | 10 | +1.5% | 0.8 | 97% | 1.00 | undecided | +15.2 ± 0.7 (4 d) | -2% | 10 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 13 | 13 | -0.1% | 0.4 | 44% | 1.00 | undecided | +19.4 ± 4.2 (2 d) | -5% | 13 |
| The real ticket at the best bookmaker price (price shopping) | 21 | 12 | -8.3% | 2.8 | 0% | 0.07 | undecided | +5.3 ± 0.5 (12 d) | -22% | 20 |
| One single a day (best value pick the AI allows) | 21 | 13 | -7.5% | 1.1 | 0% | 0.00 | undecided | +4.9 ± 2.5 (10 d) | -1% | 20 |
| Value singles that still pay after the 15% tax | 4 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -100% | 4 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 15 | 12 | -2.2% | 1.7 | 10% | 1.00 | undecided | +14.3 ± 1.6 (6 d) | -8% | 13 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 39 | 21 | -1.0% | 0.4 | 1% | 1.00 | undecided | +12.0 ± 4.1 (4 d) | -3% | 35 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 23 | 14 | -1.4% | 0.8 | 4% | 1.00 | undecided | +18.4 ± 3.8 (2 d) | +3% | 19 |
| The previous real-ticket rule (all bet types, best return after tax) | 7 | 3 | -17.7% | 3.3 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +153% | 6 |
| Low-floor ticket: one or two moneyline favourites, total odds 1.60-2.50, highest joint chance (best price) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Banker: the single most likely bet of the day (power chance, best price) | 8 | 4 | -2.5% | 1.9 | 9% | 1.00 | undecided | +16.3 ± 6.0 (3 d) | -8% | 7 |
| Banker double: the two most likely bets on different matches (best price) | 8 | 3 | -6.4% | 2.5 | 1% | 1.00 | undecided | +13.5 ± 5.6 (3 d) | -17% | 7 |
| Most likely ticket using power-method chances | 21 | 11 | -17.0% | 3.2 | 0% | 0.00 | undecided | -0.2 ± 2.5 (7 d) | -20% | 20 |
| The old ticket rule: most likely ticket within the AI's verdicts | 18 | 11 | -13.9% | 2.6 | 0% | 0.00 | undecided | -1.5 ± 1.5 (9 d) | +37% | 17 |
| The real ticket rule at the best bookmaker prices | 18 | 8 | -6.5% | 3.2 | 2% | 1.00 | undecided | +9.7 ± 2.8 (7 d) | +26% | 17 |
| Market only, best return after tax (no AI) | 18 | 6 | -18.8% | 5.8 | 0% | 1.00 | undecided | -1.5 ± 4.5 (4 d) | -4% | 17 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 8 | 4 | -16.0% | 2.9 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +50% | 7 |
| AI as veto only, at the best bookmaker prices | 8 | 3 | -3.4% | 1.1 | 0% | 1.00 | undecided | +11.2 ± 6.6 (3 d) | +57% | 7 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 13 | 3 | -15.2% | 2.2 | 0% | 1.00 | undecided | +3.8 ± 4.3 (2 d) | +18% | 12 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 13 | 0 | - | - | - | - | undecided | - | +5% | 12 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 15 | 15 | -15.9% | 0.6 | 0% | 0.00 | undecided | -2.9 ± 3.0 (9 d) | +16% | 15 |
| Late ticket at the best bookmaker prices (no AI) | 15 | 15 | -10.8% | 0.8 | 0% | 0.00 | undecided | +2.6 ± 3.3 (9 d) | +19% | 15 |
| Late low-floor ticket: floor_ticket rule minutes before kick-off (1-2 moneyline favourites, total odds 1.60-2.50, best price) | 1 | 1 | -9.0% | - | - | - | undecided | - | -100% | 1 |
| Picks the AI rated AGREE (singles, average price) | 261 | 118 | -9.8% | 0.5 | 0% | 0.00 | loses after tax | +3.9 ± 2.0 (12 d) | -7% | 250 |
| Picks rated RISKY (singles, average price) | 500 | 196 | -11.6% | 0.3 | 0% | 0.00 | loses after tax | +1.9 ± 2.9 (12 d) | -10% | 484 |
| Picks rated AVOID (singles, average price) | 260 | 122 | -13.3% | 0.4 | 0% | 0.00 | loses after tax | -0.3 ± 2.6 (12 d) | -10% | 248 |
