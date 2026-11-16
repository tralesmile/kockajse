# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.1% after tax on 23 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 38 settled tickets (win rate 29%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 29, 96% of runs end below the start and 86% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 90 | 68.9% | 65.9% | -10.7% | 6.5 |
| h2h | 97 | 72.2% | 66.9% | -1.7% | 6.5 |
| h2h, odds < 1.30 | 43 | 81.4% | 77.0% | -2.1% | 7.2 |
| h2h, odds >= 1.30 | 54 | 64.8% | 58.8% | -1.3% | 10.2 |
| spreads | 198 | 49.5% | 50.1% | -13.1% | 6.3 |
| spreads, |line| <= 15 | 106 | 49.1% | 50.2% | -13.8% | 8.6 |
| spreads, |line| > 15 | 92 | 50.0% | 50.1% | -12.4% | 9.2 |
| totals | 279 | 52.3% | 52.1% | -12.2% | 5.0 |
| totals Over | 149 | 55.0% | 52.4% | -8.6% | 6.8 |
| totals Under | 130 | 49.2% | 51.6% | -16.4% | 7.5 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.29).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 453 | 49.4% | 50.2% | -13.9% | 4.1 |
| 55-65% | 95 | 60.0% | 58.8% | -9.7% | 7.6 |
| 65-75% | 63 | 79.4% | 71.1% | -0.6% | 6.5 |
| 75-100% | 52 | 84.6% | 76.9% | +0.7% | 6.0 |

## Does the AI add anything to the sharp chance?

664 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23257 |
| 0.10 | 0.23262 |
| 0.20 | 0.23270 |
| 0.35 | 0.23286 |
| 0.50 | 0.23307 |
| 1.00 | 0.23414 |

Live weight 0.20 vs 0: Brier gain -1.3 +- 2.5 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.009 +- 0.039. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.3 points (189), AVOID -0.7 points (155), RISKY +1.3 points (320)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

76 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0381, average of all books 0.0380; paired absolute-error gain of the average over Pinnacle -0.0027 +- 0.0013.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 23 | -0.0054 | 0.0280 |
| betonlineag | 64 | -0.0027 | 0.0348 |
| matchbook | 50 | -0.0049 | 0.0377 |
| pinnacle | 76 | +0.0029 | 0.0381 |
| winamax_de | 66 | -0.0012 | 0.0387 |
| sport888 | 82 | -0.0039 | 0.0392 |
| nordicbet | 72 | -0.0022 | 0.0401 |
| betsson | 72 | -0.0024 | 0.0401 |
| betfair_ex_eu | 68 | -0.0056 | 0.0401 |
| williamhill | 70 | -0.0022 | 0.0406 |
| codere_it | 55 | -0.0056 | 0.0413 |
| winamax_fr | 51 | +0.0057 | 0.0414 |
| betclic_fr | 46 | +0.0018 | 0.0422 |
| mybookieag | 39 | -0.0006 | 0.0422 |
| coolbet | 53 | -0.0063 | 0.0426 |
| gtbets | 49 | +0.0003 | 0.0428 |
| onexbet | 79 | -0.0048 | 0.0433 |
| leovegas_se | 81 | -0.0020 | 0.0436 |
| unibet_se | 81 | -0.0047 | 0.0438 |
| unibet_nl | 64 | -0.0057 | 0.0442 |
| unibet_fr | 34 | +0.0121 | 0.0448 |
| everygame | 27 | +0.0028 | 0.0449 |
| marathonbet | 51 | -0.0026 | 0.0471 |
| pmu_fr | 48 | +0.0095 | 0.0489 |
| tipico_de | 38 | +0.0097 | 0.0562 |
