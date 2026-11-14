# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 3 strategies with 20+ scored bets beats the tax; best is pick:AGREE at -10.2% after tax on 65 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 36 settled tickets (win rate 28%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 28, 97% of runs end below the start and 88% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 71 | 69.0% | 66.0% | -10.4% | 7.4 |
| h2h | 86 | 73.3% | 67.0% | -0.4% | 6.8 |
| h2h, odds < 1.30 | 38 | 84.2% | 76.9% | +1.4% | 7.2 |
| h2h, odds >= 1.30 | 48 | 64.6% | 59.2% | -1.9% | 10.8 |
| spreads | 171 | 49.1% | 50.1% | -13.8% | 6.7 |
| spreads, |line| <= 15 | 92 | 48.9% | 50.2% | -14.1% | 9.2 |
| spreads, |line| > 15 | 79 | 49.4% | 50.0% | -13.5% | 9.9 |
| totals | 236 | 52.1% | 52.1% | -12.6% | 5.5 |
| totals Over | 126 | 53.2% | 52.5% | -12.0% | 7.4 |
| totals Under | 110 | 50.9% | 51.7% | -13.4% | 8.2 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.31).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 380 | 49.5% | 50.2% | -14.0% | 4.5 |
| 55-65% | 87 | 59.8% | 58.6% | -9.8% | 8.0 |
| 65-75% | 54 | 77.8% | 71.3% | -2.8% | 7.2 |
| 75-100% | 42 | 85.7% | 77.0% | +2.3% | 6.5 |

## Does the AI add anything to the sharp chance?

564 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23249 |
| 0.10 | 0.23255 |
| 0.20 | 0.23263 |
| 0.35 | 0.23281 |
| 0.50 | 0.23304 |
| 1.00 | 0.23423 |

Live weight 0.20 vs 0: Brier gain -1.4 +- 2.9 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.009 +- 0.042. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.5 points (165), AVOID -1.0 points (129), RISKY +1.1 points (270)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

56 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0410, average of all books 0.0392; paired absolute-error gain of the average over Pinnacle -0.0006 +- 0.0012.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 20 | -0.0053 | 0.0268 |
| betonlineag | 50 | -0.0018 | 0.0355 |
| matchbook | 42 | -0.0047 | 0.0381 |
| sport888 | 60 | -0.0019 | 0.0395 |
| winamax_de | 53 | +0.0019 | 0.0398 |
| williamhill | 56 | -0.0021 | 0.0405 |
| pinnacle | 56 | +0.0051 | 0.0410 |
| betfair_ex_eu | 57 | -0.0045 | 0.0411 |
| nordicbet | 53 | +0.0009 | 0.0412 |
| betsson | 53 | +0.0007 | 0.0413 |
| codere_it | 43 | -0.0012 | 0.0415 |
| winamax_fr | 38 | +0.0104 | 0.0428 |
| coolbet | 41 | -0.0025 | 0.0435 |
| betclic_fr | 33 | +0.0069 | 0.0445 |
| leovegas_se | 64 | -0.0027 | 0.0447 |
| mybookieag | 31 | +0.0006 | 0.0448 |
| unibet_se | 64 | -0.0054 | 0.0450 |
| onexbet | 62 | -0.0052 | 0.0450 |
| gtbets | 39 | -0.0005 | 0.0451 |
| unibet_nl | 46 | -0.0036 | 0.0454 |
| unibet_fr | 30 | +0.0130 | 0.0467 |
| everygame | 23 | +0.0029 | 0.0475 |
| marathonbet | 40 | -0.0014 | 0.0492 |
| pmu_fr | 40 | +0.0095 | 0.0494 |
| tipico_de | 26 | +0.0187 | 0.0623 |
