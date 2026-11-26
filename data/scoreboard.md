# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 25 | 13 | -13.9% | 2.4 | 0% | 0.00 | undecided | - | -19% | 24 |
| Market only (most likely ticket, no AI) | 25 | 11 | -16.5% | 3.5 | 0% | 0.00 | undecided | +0.6 ± 3.2 (8 d) | -14% | 24 |
| The AI's own ticket | 25 | 10 | -19.9% | 1.7 | 0% | 0.00 | undecided | -3.7 ± 1.6 (9 d) | +25% | 24 |
| Best expected return within the AI's verdicts | 24 | 11 | -17.0% | 2.7 | 0% | 0.00 | undecided | -4.7 ± 1.8 (10 d) | +24% | 23 |
| Value ticket at the best bookmaker price | 15 | 12 | -7.1% | 1.5 | 0% | 0.00 | undecided | +10.7 ± 2.1 (9 d) | +7% | 15 |
| Value singles at the best bookmaker price | 71 | 48 | -8.9% | 1.2 | 0% | 0.00 | loses after tax | +7.6 ± 2.2 (11 d) | -21% | 71 |
| Kaunitz singles (best price far above the average) | 2 | 1 | +1.0% | - | - | - | undecided | - | -100% | 2 |
| Late value singles (best price minutes before kick-off) | 54 | 54 | -6.0% | 0.3 | 0% | 0.00 | loses after tax | +7.5 ± 2.5 (11 d) | -4% | 54 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 10 | 10 | +1.5% | 0.8 | 97% | 1.00 | undecided | +15.2 ± 0.7 (4 d) | -2% | 10 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 16 | 16 | -0.2% | 0.3 | 25% | 1.00 | undecided | +18.5 ± 2.6 (3 d) | -1% | 16 |
| The real ticket at the best bookmaker price (price shopping) | 23 | 13 | -8.5% | 2.6 | 0% | 0.03 | undecided | +5.4 ± 0.5 (13 d) | -5% | 22 |
| One single a day (best value pick the AI allows) | 23 | 14 | -7.8% | 1.0 | 0% | 0.00 | undecided | +4.9 ± 2.5 (10 d) | +6% | 22 |
| Value singles that still pay after the 15% tax | 5 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -48% | 5 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 16 | 12 | -2.2% | 1.7 | 10% | 1.00 | undecided | +14.3 ± 1.6 (6 d) | +6% | 16 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 47 | 24 | -1.0% | 0.4 | 0% | 1.00 | undecided | +13.0 ± 3.3 (5 d) | +1% | 44 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 33 | 18 | -1.5% | 0.7 | 1% | 1.00 | undecided | +17.5 ± 2.3 (3 d) | +8% | 29 |
| Agreeing favourites: fav_wide legs where the sharp book is not below the soft bookmakers' average (power chance, best price) | 4 | 0 | - | - | - | - | undecided | - | - | 0 |
| The previous real-ticket rule (all bet types, best return after tax) | 9 | 3 | -17.7% | 3.3 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +148% | 8 |
| Low-floor ticket: one or two moneyline favourites, total odds 1.60-2.50, highest joint chance (best price) | 3 | 1 | -2.3% | - | - | - | undecided | - | +52% | 2 |
| Banker: the single most likely bet of the day (power chance, best price) | 10 | 5 | -2.3% | 1.5 | 6% | 1.00 | undecided | +16.4 ± 4.2 (4 d) | -3% | 9 |
| Banker double: the two most likely bets on different matches (best price) | 10 | 4 | -5.4% | 2.0 | 0% | 1.00 | undecided | +14.0 ± 4.0 (4 d) | -8% | 9 |
| Most likely ticket using power-method chances | 23 | 11 | -17.0% | 3.2 | 0% | 0.00 | undecided | -0.2 ± 2.5 (7 d) | -17% | 22 |
| The old ticket rule: most likely ticket within the AI's verdicts | 20 | 11 | -13.9% | 2.6 | 0% | 0.00 | undecided | -1.5 ± 1.5 (9 d) | +46% | 19 |
| The real ticket rule at the best bookmaker prices | 20 | 9 | -6.9% | 2.9 | 1% | 1.00 | undecided | +9.4 ± 2.4 (8 d) | +38% | 19 |
| Market only, best return after tax (no AI) | 20 | 6 | -18.8% | 5.8 | 0% | 1.00 | undecided | -1.5 ± 4.5 (4 d) | +10% | 19 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 10 | 4 | -16.0% | 2.9 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +68% | 9 |
| AI as veto only, at the best bookmaker prices | 10 | 4 | -7.0% | 3.6 | 3% | 1.00 | undecided | +8.5 ± 5.4 (4 d) | +48% | 9 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 15 | 3 | -15.2% | 2.2 | 0% | 1.00 | undecided | +3.8 ± 4.3 (2 d) | +34% | 14 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 15 | 0 | - | - | - | - | undecided | - | +33% | 14 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 17 | 17 | -16.0% | 0.5 | 0% | 0.00 | undecided | -2.4 ± 2.8 (10 d) | +3% | 17 |
| Late ticket at the best bookmaker prices (no AI) | 17 | 17 | -10.7% | 0.7 | 0% | 0.00 | undecided | +3.3 ± 3.0 (10 d) | +5% | 17 |
| Late low-floor ticket: floor_ticket rule minutes before kick-off (1-2 moneyline favourites, total odds 1.60-2.50, best price) | 2 | 2 | -10.1% | 1.2 | 0% | 1.00 | undecided | - | -3% | 2 |
| Picks the AI rated AGREE (singles, average price) | 283 | 128 | -9.9% | 0.4 | 0% | 0.00 | loses after tax | +4.1 ± 1.8 (13 d) | -6% | 273 |
| Picks rated RISKY (singles, average price) | 541 | 226 | -11.6% | 0.3 | 0% | 0.00 | loses after tax | +2.2 ± 2.6 (13 d) | -9% | 530 |
| Picks rated AVOID (singles, average price) | 275 | 137 | -13.4% | 0.3 | 0% | 0.00 | loses after tax | +0.0 ± 2.4 (13 d) | -11% | 270 |
