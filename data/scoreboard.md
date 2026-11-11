# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 10 | 3 | -13.9% | 2.7 | 0% | 1.00 | undecided | - | -71% | 9 |
| Market only (most likely ticket, no AI) | 10 | 4 | -19.7% | 10.0 | 2% | 1.00 | undecided | +3.4 ± 12.6 (2 d) | -49% | 9 |
| The AI's own ticket | 10 | 3 | -19.2% | 1.8 | 0% | 1.00 | undecided | -3.9 ± 3.9 (2 d) | +45% | 9 |
| Best expected return within the AI's verdicts | 9 | 3 | -19.7% | 3.0 | 0% | 1.00 | undecided | -5.8 ± 3.1 (3 d) | -100% | 8 |
| Value ticket at the best bookmaker price | 4 | 4 | -8.2% | 3.0 | 0% | 1.00 | undecided | +8.2 ± 1.1 (2 d) | -26% | 4 |
| Value singles at the best bookmaker price | 21 | 16 | -8.1% | 2.1 | 0% | 0.00 | undecided | +7.0 ± 3.9 (3 d) | -27% | 21 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 14 | 14 | -6.5% | 0.7 | 0% | 0.00 | undecided | +6.6 ± 2.7 (3 d) | +38% | 14 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 8 | 3 | -9.5% | 2.9 | 0% | 1.00 | undecided | +4.3 ± 1.0 (3 d) | -60% | 7 |
| One single a day (best value pick the AI allows) | 8 | 4 | -6.6% | 2.5 | 0% | 1.00 | undecided | +4.8 ± 3.1 (3 d) | -32% | 7 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 4 | 4 | -3.4% | 4.1 | 20% | 1.00 | undecided | +13.8 ± 5.5 (2 d) | -15% | 4 |
| Most likely ticket using power-method chances | 8 | 4 | -20.9% | 8.8 | 1% | 1.00 | undecided | +1.0 ± 4.1 (2 d) | -67% | 7 |
| The old ticket rule: most likely ticket within the AI's verdicts | 5 | 4 | -16.1% | 4.4 | 0% | 1.00 | undecided | -3.3 ± 3.3 (2 d) | +20% | 4 |
| The real ticket rule at the best bookmaker prices | 5 | 3 | -6.3% | 2.8 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | +17% | 4 |
| Market only, best return after tax (no AI) | 5 | 3 | -24.4% | 11.3 | 2% | 1.00 | undecided | - | -43% | 4 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 2 | 2 | -14.0% | 0.7 | 0% | 1.00 | undecided | - | +20% | 2 |
| Late ticket at the best bookmaker prices (no AI) | 2 | 2 | -8.0% | 0.2 | 0% | 1.00 | undecided | - | +143% | 2 |
| Picks the AI rated AGREE (singles, average price) | 133 | 41 | -10.5% | 0.8 | 0% | 0.00 | loses after tax | +4.0 ± 2.0 (3 d) | -13% | 109 |
| Picks rated RISKY (singles, average price) | 244 | 62 | -10.9% | 0.5 | 0% | 0.00 | loses after tax | +3.5 ± 2.3 (3 d) | -6% | 221 |
| Picks rated AVOID (singles, average price) | 108 | 45 | -12.8% | 0.7 | 0% | 0.00 | loses after tax | -0.1 ± 2.2 (3 d) | -14% | 101 |
