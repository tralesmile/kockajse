# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 9 | 3 | -13.9% | 2.7 | 0% | 1.00 | undecided | - | -67% | 8 |
| Market only (most likely ticket, no AI) | 9 | 4 | -19.7% | 10.0 | 2% | 1.00 | undecided | +3.4 ± 12.6 (2 d) | -42% | 8 |
| The AI's own ticket | 9 | 3 | -19.2% | 1.8 | 0% | 1.00 | undecided | -3.9 ± 3.9 (2 d) | +26% | 8 |
| Best expected return within the AI's verdicts | 8 | 3 | -19.7% | 3.0 | 0% | 1.00 | undecided | -5.8 ± 3.1 (3 d) | -100% | 7 |
| Value ticket at the best bookmaker price | 4 | 4 | -8.2% | 3.0 | 0% | 1.00 | undecided | +8.2 ± 1.1 (2 d) | -26% | 4 |
| Value singles at the best bookmaker price | 21 | 16 | -8.1% | 2.1 | 0% | 0.00 | undecided | +7.0 ± 3.9 (3 d) | -23% | 20 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 13 | 13 | -6.6% | 0.7 | 0% | 0.00 | undecided | +6.6 ± 2.7 (3 d) | +34% | 13 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | -47% | 2 |
| The real ticket at the best bookmaker price (price shopping) | 7 | 3 | -9.5% | 2.9 | 0% | 1.00 | undecided | +4.3 ± 1.0 (3 d) | -53% | 6 |
| One single a day (best value pick the AI allows) | 7 | 4 | -6.6% | 2.5 | 0% | 1.00 | undecided | +4.8 ± 3.1 (3 d) | -20% | 6 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 4 | 3 | +0.6% | 0.7 | 82% | 1.00 | undecided | +13.8 ± 5.5 (2 d) | -26% | 3 |
| Most likely ticket using power-method chances | 7 | 4 | -20.9% | 8.8 | 1% | 1.00 | undecided | +1.0 ± 4.1 (2 d) | -62% | 6 |
| The old ticket rule: most likely ticket within the AI's verdicts | 4 | 3 | -12.2% | 2.9 | 0% | 1.00 | undecided | -3.3 ± 3.3 (2 d) | -23% | 3 |
| The real ticket rule at the best bookmaker prices | 4 | 3 | -6.3% | 2.8 | 1% | 1.00 | undecided | +8.1 ± 1.3 (2 d) | -20% | 3 |
| Market only, best return after tax (no AI) | 4 | 2 | -31.2% | 15.7 | 2% | 1.00 | undecided | - | -24% | 3 |
| Late ticket: the ticket rule minutes before kick-off (no AI, average price) | 1 | 1 | -14.7% | - | - | - | undecided | - | -100% | 1 |
| Late ticket at the best bookmaker prices (no AI) | 1 | 1 | -8.1% | - | - | - | undecided | - | +131% | 1 |
| Picks the AI rated AGREE (singles, average price) | 109 | 39 | -10.3% | 0.8 | 0% | 0.00 | loses after tax | +4.0 ± 2.0 (3 d) | -18% | 96 |
| Picks rated RISKY (singles, average price) | 221 | 60 | -11.0% | 0.4 | 0% | 0.00 | loses after tax | +3.5 ± 2.3 (3 d) | -5% | 200 |
| Picks rated AVOID (singles, average price) | 101 | 44 | -12.9% | 0.7 | 0% | 0.00 | loses after tax | -0.1 ± 2.2 (3 d) | -11% | 96 |
