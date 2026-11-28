# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 27 | 15 | -14.1% | 2.1 | 0% | 0.00 | undecided | - | -15% | 26 |
| Market only (most likely ticket, no AI) | 27 | 13 | -16.1% | 3.0 | 0% | 0.00 | undecided | +0.7 ± 2.5 (10 d) | -12% | 26 |
| The AI's own ticket | 27 | 12 | -18.8% | 1.6 | 0% | 0.00 | undecided | -2.7 ± 1.5 (11 d) | +16% | 26 |
| Best expected return within the AI's verdicts | 26 | 13 | -16.9% | 2.3 | 0% | 0.00 | undecided | -4.1 ± 1.7 (12 d) | +14% | 25 |
| Value ticket at the best bookmaker price | 17 | 13 | -7.5% | 1.4 | 0% | 0.00 | undecided | +9.7 ± 2.1 (10 d) | +1% | 16 |
| Value singles at the best bookmaker price | 84 | 52 | -8.6% | 1.1 | 0% | 0.00 | loses after tax | +7.6 ± 2.0 (12 d) | -19% | 75 |
| Kaunitz singles (best price far above the average) | 2 | 1 | +1.0% | - | - | - | undecided | - | -100% | 2 |
| Late value singles (best price minutes before kick-off) | 60 | 60 | -6.0% | 0.3 | 0% | 0.00 | loses after tax | +8.0 ± 2.1 (13 d) | -2% | 60 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 12 | 12 | +1.4% | 0.7 | 98% | 1.00 | undecided | +15.0 ± 0.6 (5 d) | +2% | 12 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 20 | 20 | -0.2% | 0.3 | 21% | 1.00 | undecided | +17.1 ± 1.7 (5 d) | +4% | 20 |
| The real ticket at the best bookmaker price (price shopping) | 25 | 15 | -8.4% | 2.2 | 0% | 0.01 | undecided | +5.7 ± 0.5 (15 d) | -1% | 24 |
| One single a day (best value pick the AI allows) | 25 | 16 | -8.0% | 0.9 | 0% | 0.00 | undecided | +5.0 ± 2.1 (12 d) | +4% | 24 |
| Value singles that still pay after the 15% tax | 5 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -48% | 5 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 18 | 14 | -1.9% | 1.5 | 11% | 1.00 | undecided | +14.1 ± 1.4 (7 d) | +8% | 18 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 56 | 30 | -1.3% | 0.4 | 0% | 1.00 | undecided | +12.9 ± 2.3 (7 d) | +2% | 50 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 44 | 25 | -1.9% | 0.6 | 0% | 0.86 | undecided | +15.5 ± 1.8 (5 d) | +10% | 36 |
| RETIRED 26 Nov. Agreeing favourites: fav_wide legs where the sharp book is not below the soft bookmakers' average (power chance, best price) | 4 | 4 | -3.8% | 0.9 | 0% | 1.00 | undecided | - | +19% | 4 |
| The previous real-ticket rule (all bet types, best return after tax) | 10 | 5 | -16.4% | 2.2 | 0% | 1.00 | undecided | -1.6 ± 2.4 (5 d) | +124% | 10 |
| Low-floor ticket: one or two moneyline favourites, total odds 1.60-2.50, highest joint chance (best price) | 5 | 3 | -3.1% | 2.7 | 13% | 1.00 | undecided | +13.0 ± 1.9 (3 d) | +52% | 4 |
| Banker: the single most likely bet of the day (power chance, best price) | 12 | 7 | -2.5% | 1.0 | 1% | 1.00 | undecided | +14.9 ± 2.9 (6 d) | -1% | 11 |
| Banker double: the two most likely bets on different matches (best price) | 12 | 6 | -6.0% | 1.4 | 0% | 1.00 | undecided | +11.9 ± 2.9 (6 d) | -2% | 11 |
| Most likely ticket using power-method chances | 25 | 13 | -16.6% | 2.7 | 0% | 0.00 | undecided | -0.0 ± 1.9 (9 d) | -14% | 24 |
| The old ticket rule: most likely ticket within the AI's verdicts | 22 | 13 | -13.7% | 2.2 | 0% | 0.00 | undecided | -0.8 ± 1.3 (11 d) | +43% | 21 |
| The real ticket rule at the best bookmaker prices | 22 | 11 | -7.1% | 2.4 | 0% | 0.06 | undecided | +9.0 ± 1.9 (10 d) | +38% | 21 |
| Market only, best return after tax (no AI) | 22 | 8 | -16.4% | 4.6 | 0% | 1.00 | undecided | +1.0 ± 3.3 (6 d) | +12% | 21 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 12 | 6 | -15.5% | 2.0 | 0% | 1.00 | undecided | -1.6 ± 2.4 (5 d) | +60% | 11 |
| AI as veto only, at the best bookmaker prices | 12 | 6 | -8.0% | 3.2 | 1% | 1.00 | undecided | +7.3 ± 3.8 (6 d) | +21% | 11 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 17 | 5 | -12.7% | 2.4 | 0% | 1.00 | undecided | +4.9 ± 2.1 (4 d) | +34% | 16 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 17 | 2 | -5.0% | 0.1 | 0% | 1.00 | undecided | +10.1 ± 2.1 (2 d) | +31% | 16 |
| Moneyline-only ticket from the matches the AI would have rated before 27 Nov (no AI) | 1 | 0 | - | - | - | - | undecided | - | - | 0 |
| Lead-book ticket: the moneyline-only ticket, chances moved towards BetOnline and the exchanges (no AI) | 2 | 1 | -4.6% | - | - | - | undecided | - | -100% | 1 |
| Lead-book ticket at the best bookmaker prices (no AI) | 2 | 1 | -4.9% | - | - | - | undecided | - | -100% | 1 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 19 | 19 | -16.2% | 0.5 | 0% | 0.00 | undecided | -2.6 ± 2.3 (12 d) | +5% | 19 |
| Late ticket at the best bookmaker prices (no AI) | 19 | 19 | -10.6% | 0.7 | 0% | 0.00 | undecided | +3.1 ± 2.5 (12 d) | +21% | 19 |
| Late low-floor ticket: floor_ticket rule minutes before kick-off (1-2 moneyline favourites, total odds 1.60-2.50, best price) | 5 | 5 | -7.8% | 1.2 | 0% | 1.00 | undecided | +7.6 ± 2.0 (3 d) | +6% | 5 |
| Picks the AI rated AGREE (singles, average price) | 300 | 148 | -9.7% | 0.4 | 0% | 0.00 | loses after tax | +4.4 ± 1.6 (15 d) | -7% | 295 |
| Picks rated RISKY (singles, average price) | 572 | 250 | -11.7% | 0.3 | 0% | 0.00 | loses after tax | +2.2 ± 2.3 (15 d) | -8% | 563 |
| Picks rated AVOID (singles, average price) | 295 | 142 | -13.5% | 0.3 | 0% | 0.00 | loses after tax | +0.2 ± 2.3 (14 d) | -11% | 277 |
