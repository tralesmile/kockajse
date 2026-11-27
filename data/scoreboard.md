# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 26 | 14 | -14.2% | 2.2 | 0% | 0.00 | undecided | - | -12% | 25 |
| Market only (most likely ticket, no AI) | 26 | 12 | -16.5% | 3.2 | 0% | 0.00 | undecided | +0.6 ± 2.8 (9 d) | -8% | 25 |
| The AI's own ticket | 26 | 11 | -19.2% | 1.7 | 0% | 0.00 | undecided | -2.9 ± 1.7 (10 d) | +20% | 25 |
| Best expected return within the AI's verdicts | 25 | 12 | -16.7% | 2.5 | 0% | 0.00 | undecided | -3.8 ± 1.8 (11 d) | +19% | 24 |
| Value ticket at the best bookmaker price | 16 | 12 | -7.1% | 1.5 | 0% | 0.00 | undecided | +10.7 ± 2.1 (9 d) | +7% | 15 |
| Value singles at the best bookmaker price | 75 | 48 | -8.9% | 1.2 | 0% | 0.00 | loses after tax | +7.6 ± 2.2 (11 d) | -21% | 71 |
| Kaunitz singles (best price far above the average) | 2 | 1 | +1.0% | - | - | - | undecided | - | -100% | 2 |
| Late value singles (best price minutes before kick-off) | 58 | 58 | -6.1% | 0.3 | 0% | 0.00 | loses after tax | +7.7 ± 2.3 (12 d) | -2% | 58 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 10 | 10 | +1.5% | 0.8 | 97% | 1.00 | undecided | +15.2 ± 0.7 (4 d) | -2% | 10 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 17 | 17 | -0.3% | 0.3 | 19% | 1.00 | undecided | +17.9 ± 1.9 (4 d) | +1% | 17 |
| The real ticket at the best bookmaker price (price shopping) | 24 | 14 | -8.7% | 2.4 | 0% | 0.01 | undecided | +5.5 ± 0.5 (14 d) | +3% | 23 |
| One single a day (best value pick the AI allows) | 24 | 15 | -7.8% | 1.0 | 0% | 0.00 | undecided | +5.3 ± 2.3 (11 d) | +9% | 23 |
| Value singles that still pay after the 15% tax | 5 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -48% | 5 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 18 | 12 | -2.2% | 1.7 | 10% | 1.00 | undecided | +14.3 ± 1.6 (6 d) | +6% | 16 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 50 | 27 | -1.3% | 0.4 | 0% | 1.00 | undecided | +13.2 ± 2.7 (6 d) | +1% | 47 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 36 | 22 | -2.0% | 0.6 | 0% | 0.97 | undecided | +16.5 ± 1.9 (4 d) | +9% | 33 |
| RETIRED 26 Nov. Agreeing favourites: fav_wide legs where the sharp book is not below the soft bookmakers' average (power chance, best price) | 4 | 4 | -3.8% | 0.9 | 0% | 1.00 | undecided | - | +19% | 4 |
| The previous real-ticket rule (all bet types, best return after tax) | 10 | 4 | -17.7% | 2.3 | 0% | 1.00 | undecided | -2.4 ± 2.9 (4 d) | +148% | 9 |
| Low-floor ticket: one or two moneyline favourites, total odds 1.60-2.50, highest joint chance (best price) | 4 | 2 | -5.2% | 2.9 | 4% | 1.00 | undecided | +12.4 ± 3.2 (2 d) | +53% | 3 |
| Banker: the single most likely bet of the day (power chance, best price) | 11 | 6 | -2.5% | 1.2 | 2% | 1.00 | undecided | +15.8 ± 3.3 (5 d) | -1% | 10 |
| Banker double: the two most likely bets on different matches (best price) | 11 | 5 | -5.6% | 1.6 | 0% | 1.00 | undecided | +13.4 ± 3.1 (5 d) | -4% | 10 |
| Most likely ticket using power-method chances | 24 | 12 | -17.1% | 2.9 | 0% | 0.00 | undecided | -0.2 ± 2.1 (8 d) | -10% | 23 |
| The old ticket rule: most likely ticket within the AI's verdicts | 21 | 12 | -13.9% | 2.4 | 0% | 0.00 | undecided | -1.0 ± 1.4 (10 d) | +51% | 20 |
| The real ticket rule at the best bookmaker prices | 21 | 10 | -7.3% | 2.6 | 0% | 0.10 | undecided | +9.1 ± 2.2 (9 d) | +45% | 20 |
| Market only, best return after tax (no AI) | 21 | 7 | -18.0% | 5.0 | 0% | 1.00 | undecided | -0.4 ± 3.6 (5 d) | +18% | 20 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 11 | 5 | -16.3% | 2.2 | 0% | 1.00 | undecided | -2.4 ± 2.9 (4 d) | +76% | 10 |
| AI as veto only, at the best bookmaker prices | 11 | 5 | -9.2% | 3.6 | 1% | 1.00 | undecided | +6.6 ± 4.6 (5 d) | +33% | 10 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 16 | 4 | -14.7% | 1.6 | 0% | 1.00 | undecided | +3.8 ± 2.5 (3 d) | +43% | 15 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 16 | 1 | -5.1% | - | - | - | undecided | - | +39% | 15 |
| Lead-book ticket: the moneyline-only ticket, chances moved towards BetOnline and the exchanges (no AI) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Lead-book ticket at the best bookmaker prices (no AI) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 17 | 17 | -16.0% | 0.5 | 0% | 0.00 | undecided | -2.2 ± 2.5 (11 d) | +3% | 17 |
| Late ticket at the best bookmaker prices (no AI) | 17 | 17 | -10.7% | 0.7 | 0% | 0.00 | undecided | +3.6 ± 2.7 (11 d) | +5% | 17 |
| Late low-floor ticket: floor_ticket rule minutes before kick-off (1-2 moneyline favourites, total odds 1.60-2.50, best price) | 3 | 3 | -8.7% | 1.6 | 0% | 1.00 | undecided | +9.0 ± 2.5 (2 d) | -35% | 3 |
| Picks the AI rated AGREE (singles, average price) | 295 | 138 | -9.8% | 0.4 | 0% | 0.00 | loses after tax | +4.5 ± 1.7 (14 d) | -6% | 283 |
| Picks rated RISKY (singles, average price) | 563 | 237 | -11.7% | 0.3 | 0% | 0.00 | loses after tax | +2.3 ± 2.5 (14 d) | -9% | 541 |
| Picks rated AVOID (singles, average price) | 277 | 142 | -13.5% | 0.3 | 0% | 0.00 | loses after tax | +0.2 ± 2.3 (14 d) | -11% | 275 |
