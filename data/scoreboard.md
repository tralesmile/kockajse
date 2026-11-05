# Strategy scoreboard at closing prices

Each bet is scored when its closing price is captured: expected return per unit after the 15% tax if the margin-free closing chance is the true chance. Verdicts use an always-valid sequential test (mSPRT, alpha 0.05, at least 20 scored bets), so the table may be read every day. Built by scoreboard.py.

| Strategy | Bets | Scored at close | Expected return after tax | se (points) | Chance it beats the tax | Always-valid p | Verdict | vs real ticket, same days | Realised return | Settled |
|---|---|---|---|---|---|---|---|---|---|---|
| The real paper ticket | 4 | 0 | - | - | - | - | undecided | - | -100% | 2 |
| Market only (most likely ticket, no AI) | 4 | 0 | - | - | - | - | undecided | - | +53% | 3 |
| The AI's own ticket | 4 | 0 | - | - | - | - | undecided | - | -100% | 2 |
| Best expected return within the AI's verdicts | 4 | 0 | - | - | - | - | undecided | - | -100% | 2 |
| Value ticket at the best bookmaker price | 1 | 1 | -8.7% | - | - | - | undecided | - | - | 0 |
| Value singles at the best bookmaker price | 9 | 6 | -3.1% | 2.2 | 8% | 1.00 | undecided | - | +80% | 2 |
| Kaunitz singles (best price far above the average) | 1 | 0 | - | - | - | - | undecided | - | -100% | 1 |
| Late value singles (best price minutes before kick-off) | 5 | 5 | -6.3% | 1.7 | 0% | 1.00 | undecided | - | - | 0 |
| Late tax-proof singles, power chance (best price minutes before kick-off) | 2 | 2 | -1.4% | 1.6 | 19% | 1.00 | undecided | - | - | 0 |
| The real ticket at the best bookmaker price (price shopping) | 2 | 0 | - | - | - | - | undecided | - | - | 0 |
| One single a day (best value pick the AI allows) | 2 | 0 | - | - | - | - | undecided | - | - | 0 |
| Tax-proof value singles, power-method fair chance (favourites from 1.05) | 2 | 2 | +1.3% | 0.5 | 99% | 1.00 | undecided | - | - | 0 |
| Most likely ticket using power-method chances | 2 | 0 | - | - | - | - | undecided | - | - | 0 |
| Picks the AI rated AGREE (singles, average price) | 52 | 8 | -12.5% | 0.4 | 0% | 1.00 | undecided | - | -9% | 43 |
| Picks rated RISKY (singles, average price) | 124 | 20 | -11.5% | 0.9 | 0% | 0.00 | loses after tax | - | -8% | 107 |
| Picks rated AVOID (singles, average price) | 46 | 5 | -11.9% | 3.6 | 0% | 1.00 | undecided | - | -7% | 32 |
