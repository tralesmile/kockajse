# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 24 | 12 | -13.6% | 2.6 | 0% | 0.00 | undecided | - | -26% | 23 |
| Market only (most likely ticket, no AI) | 24 | 11 | -16.5% | 3.5 | 0% | 0.00 | undecided | +0.6 ± 3.2 (8 d) | -20% | 23 |
| The AI's own ticket | 24 | 10 | -19.9% | 1.7 | 0% | 0.00 | undecided | -3.7 ± 1.6 (9 d) | +31% | 23 |
| Best expected return within the AI's verdicts | 23 | 10 | -16.4% | 2.9 | 0% | 0.00 | undecided | -4.5 ± 2.0 (9 d) | +16% | 22 |
| Value ticket at the best bookmaker price | 15 | 12 | -7.1% | 1.5 | 0% | 0.00 | undecided | +10.7 ± 2.1 (9 d) | -4% | 14 |
| Value singles at the best bookmaker price | 71 | 42 | -8.7% | 1.1 | 0% | 0.00 | loses after tax | +7.6 ± 2.5 (10 d) | -19% | 61 |
| Kaunitz singles (best price far above the average) | 2 | 1 | +1.0% | - | - | - | undecided | - | -100% | 2 |
| Late value singles (best price minutes before kick-off) | 46 | 46 | -6.0% | 0.4 | 0% | 0.00 | loses after tax | +7.1 ± 2.7 (10 d) | +4% | 46 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 10 | 10 | +1.5% | 0.8 | 97% | 1.00 | undecided | +15.2 ± 0.7 (4 d) | -2% | 10 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 14 | 14 | -0.1% | 0.4 | 39% | 1.00 | undecided | +19.4 ± 4.2 (2 d) | -2% | 14 |
| The real ticket at the best bookmaker price (price shopping) | 22 | 12 | -8.3% | 2.8 | 0% | 0.07 | undecided | +5.3 ± 0.5 (12 d) | -13% | 21 |
| One single a day (best value pick the AI allows) | 22 | 14 | -7.8% | 1.0 | 0% | 0.00 | undecided | +4.9 ± 2.5 (10 d) | +3% | 21 |
| Value singles that still pay after the 15% tax | 5 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -100% | 4 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 16 | 12 | -2.2% | 1.7 | 10% | 1.00 | undecided | +14.3 ± 1.6 (6 d) | -5% | 15 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 44 | 21 | -1.0% | 0.4 | 1% | 1.00 | undecided | +12.0 ± 4.1 (4 d) | -1% | 39 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 29 | 14 | -1.4% | 0.8 | 4% | 1.00 | undecided | +18.4 ± 3.8 (2 d) | +6% | 23 |
| The previous real-ticket rule (all bet types, best return after tax) | 8 | 3 | -17.7% | 3.3 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +151% | 7 |
| Low-floor ticket: one or two moneyline favourites, total odds 1.60-2.50, highest joint chance (best price) | 2 | 0 | - | - | - | - | undecided | - | +52% | 1 |
| Banker: the single most likely bet of the day (power chance, best price) | 9 | 4 | -2.5% | 1.9 | 9% | 1.00 | undecided | +16.3 ± 6.0 (3 d) | -4% | 8 |
| Banker double: the two most likely bets on different matches (best price) | 9 | 3 | -6.4% | 2.5 | 1% | 1.00 | undecided | +13.5 ± 5.6 (3 d) | -11% | 8 |
| Most likely ticket using power-method chances | 22 | 11 | -17.0% | 3.2 | 0% | 0.00 | undecided | -0.2 ± 2.5 (7 d) | -13% | 21 |
| The old ticket rule: most likely ticket within the AI's verdicts | 19 | 11 | -13.9% | 2.6 | 0% | 0.00 | undecided | -1.5 ± 1.5 (9 d) | +42% | 18 |
| The real ticket rule at the best bookmaker prices | 19 | 8 | -6.5% | 3.2 | 2% | 1.00 | undecided | +9.7 ± 2.8 (7 d) | +31% | 18 |
| Market only, best return after tax (no AI) | 19 | 6 | -18.8% | 5.8 | 0% | 1.00 | undecided | -1.5 ± 4.5 (4 d) | +4% | 18 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 9 | 4 | -16.0% | 2.9 | 0% | 1.00 | undecided | -3.1 ± 4.0 (3 d) | +61% | 8 |
| AI as veto only, at the best bookmaker prices | 9 | 3 | -3.4% | 1.1 | 0% | 1.00 | undecided | +11.2 ± 6.6 (3 d) | +37% | 8 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 14 | 3 | -15.2% | 2.2 | 0% | 1.00 | undecided | +3.8 ± 4.3 (2 d) | +26% | 13 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 14 | 0 | - | - | - | - | undecided | - | +19% | 13 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 15 | 15 | -15.9% | 0.6 | 0% | 0.00 | undecided | -2.9 ± 3.0 (9 d) | +16% | 15 |
| Late ticket at the best bookmaker prices (no AI) | 15 | 15 | -10.8% | 0.8 | 0% | 0.00 | undecided | +2.6 ± 3.3 (9 d) | +19% | 15 |
| Late low-floor ticket: floor_ticket rule minutes before kick-off (1-2 moneyline favourites, total odds 1.60-2.50, best price) | 1 | 1 | -9.0% | - | - | - | undecided | - | -100% | 1 |
| Picks the AI rated AGREE (singles, average price) | 273 | 119 | -9.8% | 0.5 | 0% | 0.00 | loses after tax | +3.9 ± 2.0 (12 d) | -7% | 261 |
| Picks rated RISKY (singles, average price) | 530 | 204 | -11.6% | 0.3 | 0% | 0.00 | loses after tax | +1.9 ± 2.9 (12 d) | -9% | 500 |
| Picks rated AVOID (singles, average price) | 270 | 128 | -13.3% | 0.3 | 0% | 0.00 | loses after tax | -0.3 ± 2.6 (12 d) | -10% | 260 |
