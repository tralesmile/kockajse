# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 21 | 10 | -11.9% | 2.6 | 0% | 0.00 | undecided | - | -27% | 20 |
| Market only (most likely ticket, no AI) | 21 | 11 | -16.5% | 3.5 | 0% | 0.00 | undecided | +0.6 ± 3.2 (8 d) | -31% | 20 |
| The AI's own ticket | 21 | 8 | -18.4% | 1.6 | 0% | 1.00 | undecided | -3.6 ± 1.9 (7 d) | +27% | 20 |
| Best expected return within the AI's verdicts | 20 | 9 | -15.4% | 3.0 | 0% | 1.00 | undecided | -3.7 ± 2.0 (8 d) | +7% | 19 |
| Value ticket at the best bookmaker price | 12 | 10 | -7.2% | 1.8 | 0% | 0.00 | undecided | +9.3 ± 1.9 (7 d) | -46% | 11 |
| Value singles at the best bookmaker price | 54 | 36 | -8.9% | 1.3 | 0% | 0.00 | loses after tax | +5.7 ± 2.3 (8 d) | -30% | 49 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 37 | 37 | -6.0% | 0.5 | 0% | 0.00 | loses after tax | +4.7 ± 2.4 (8 d) | +20% | 37 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 6 | 6 | +1.3% | 1.4 | 83% | 1.00 | undecided | +15.0 ± 0.9 (3 d) | -16% | 6 |
| Late wide favourites: fav_wide rule minutes before kick-off (to 2.00, chance 60%+, best price) | 7 | 7 | -1.1% | 0.1 | 0% | 1.00 | undecided | - | -24% | 7 |
| The real ticket at the best bookmaker price (price shopping) | 19 | 10 | -6.8% | 2.7 | 1% | 0.19 | undecided | +5.1 ± 0.5 (10 d) | -13% | 18 |
| One single a day (best value pick the AI allows) | 19 | 12 | -7.9% | 1.0 | 0% | 0.00 | undecided | +4.0 ± 2.6 (9 d) | -6% | 18 |
| Value singles that still pay after the 15% tax | 4 | 4 | -11.0% | 1.8 | 0% | 1.00 | undecided | - | -100% | 4 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 13 | 8 | -3.6% | 2.5 | 7% | 1.00 | undecided | +14.2 ± 1.9 (5 d) | -21% | 9 |
| Favourite singles to 1.30, break-even after tax (power chance, best price) | 35 | 15 | -1.7% | 0.5 | 0% | 1.00 | undecided | +11.2 ± 5.6 (3 d) | -8% | 28 |
| Wide favourites: moneyline singles to 2.00, chance 60%+, taxed EV above -2% (power chance, best price) | 19 | 8 | -2.9% | 1.2 | 1% | 1.00 | undecided | - | -4% | 12 |
| The previous real-ticket rule (all bet types, best return after tax) | 5 | 2 | -15.5% | 4.2 | 0% | 1.00 | undecided | -0.6 ± 5.5 (2 d) | +141% | 4 |
| Banker: the single most likely bet of the day (power chance, best price) | 6 | 3 | -0.7% | 0.8 | 19% | 1.00 | undecided | +13.4 ± 9.1 (2 d) | -15% | 5 |
| Banker double: the two most likely bets on different matches (best price) | 6 | 2 | -4.0% | 1.1 | 0% | 1.00 | undecided | +10.9 ± 8.5 (2 d) | -31% | 5 |
| Most likely ticket using power-method chances | 19 | 11 | -17.0% | 3.2 | 0% | 0.00 | undecided | -0.2 ± 2.5 (7 d) | -24% | 18 |
| The old ticket rule: most likely ticket within the AI's verdicts | 16 | 10 | -13.0% | 2.7 | 0% | 0.00 | undecided | -0.6 ± 1.4 (8 d) | +24% | 15 |
| The real ticket rule at the best bookmaker prices | 16 | 6 | -3.7% | 2.1 | 4% | 1.00 | undecided | +10.6 ± 3.8 (5 d) | +27% | 15 |
| Market only, best return after tax (no AI) | 16 | 6 | -18.8% | 5.8 | 0% | 1.00 | undecided | -1.5 ± 4.5 (4 d) | -6% | 15 |
| AI as veto only: market ticket (best return after tax) without the AVOID picks | 6 | 3 | -13.9% | 2.8 | 0% | 1.00 | undecided | -0.6 ± 5.5 (2 d) | -1% | 5 |
| AI as veto only, at the best bookmaker prices | 6 | 2 | -3.5% | 1.8 | 3% | 1.00 | undecided | +11.4 ± 11.4 (2 d) | +16% | 5 |
| Moneyline-only ticket, best return after tax (no handicaps or totals, no AI) | 11 | 3 | -15.2% | 2.2 | 0% | 1.00 | undecided | +3.8 ± 4.3 (2 d) | +41% | 10 |
| Moneyline-only ticket at the best bookmaker prices (no AI) | 11 | 0 | - | - | - | - | undecided | - | +26% | 10 |
| Kick-off sweep: late tax-proof singles in other leagues' busiest slots | 3 | 3 | +4.4% | 1.4 | 100% | 1.00 | undecided | - | -49% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 13 | 13 | -15.8% | 0.6 | 0% | 0.00 | undecided | -5.1 ± 3.2 (7 d) | +13% | 13 |
| Late ticket at the best bookmaker prices (no AI) | 13 | 13 | -10.7% | 0.8 | 0% | 0.00 | undecided | +0.7 ± 3.7 (7 d) | +20% | 13 |
| Picks the AI rated AGREE (singles, average price) | 244 | 107 | -9.5% | 0.5 | 0% | 0.00 | loses after tax | +2.9 ± 2.1 (10 d) | -8% | 236 |
| Picks rated RISKY (singles, average price) | 439 | 171 | -11.6% | 0.3 | 0% | 0.00 | loses after tax | +0.1 ± 3.0 (10 d) | -11% | 429 |
| Picks rated AVOID (singles, average price) | 236 | 112 | -13.3% | 0.4 | 0% | 0.00 | loses after tax | -2.0 ± 2.6 (10 d) | -9% | 232 |
