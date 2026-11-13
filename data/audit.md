# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 3 strategies with 20+ scored bets beats the tax; best is pick:AGREE at -10.2% after tax on 56 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 35 settled tickets (win rate 29%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 29, 97% of runs end below the start and 86% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 71 | 69.0% | 66.0% | -10.4% | 7.4 |
| h2h | 83 | 73.5% | 66.9% | +0.2% | 6.9 |
| h2h, odds < 1.30 | 36 | 83.3% | 77.0% | +0.3% | 7.6 |
| h2h, odds >= 1.30 | 47 | 66.0% | 59.1% | +0.2% | 10.8 |
| spreads | 152 | 49.3% | 50.1% | -13.5% | 7.1 |
| spreads, |line| <= 15 | 82 | 48.8% | 50.2% | -14.3% | 9.8 |
| spreads, |line| > 15 | 70 | 50.0% | 50.0% | -12.6% | 10.5 |
| totals | 219 | 52.1% | 52.2% | -12.9% | 5.7 |
| totals Over | 118 | 55.1% | 52.6% | -8.8% | 7.6 |
| totals Under | 101 | 48.5% | 51.7% | -17.6% | 8.5 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.31).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 347 | 49.6% | 50.2% | -13.8% | 4.7 |
| 55-65% | 83 | 60.2% | 58.7% | -9.3% | 8.2 |
| 65-75% | 53 | 77.4% | 71.2% | -3.3% | 7.3 |
| 75-100% | 41 | 85.4% | 77.0% | +1.8% | 6.7 |

## Does the AI add anything to the sharp chance?

525 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23163 |
| 0.10 | 0.23171 |
| 0.20 | 0.23181 |
| 0.35 | 0.23202 |
| 0.50 | 0.23229 |
| 1.00 | 0.23363 |

Live weight 0.20 vs 0: Brier gain -1.8 +- 3.1 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.013 +- 0.044. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +1.4 points (148), AVOID -1.1 points (117), RISKY +2.0 points (260)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

51 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0423, average of all books 0.0404; paired absolute-error gain of the average over Pinnacle -0.0005 +- 0.0013.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 17 | -0.0041 | 0.0258 |
| betonlineag | 45 | -0.0025 | 0.0372 |
| matchbook | 41 | -0.0045 | 0.0385 |
| winamax_de | 50 | +0.0028 | 0.0404 |
| sport888 | 54 | -0.0016 | 0.0410 |
| williamhill | 52 | -0.0015 | 0.0414 |
| betfair_ex_eu | 53 | -0.0040 | 0.0416 |
| codere_it | 42 | -0.0014 | 0.0419 |
| pinnacle | 51 | +0.0056 | 0.0423 |
| nordicbet | 49 | +0.0012 | 0.0424 |
| betsson | 49 | +0.0009 | 0.0424 |
| coolbet | 41 | -0.0025 | 0.0435 |
| winamax_fr | 35 | +0.0110 | 0.0437 |
| mybookieag | 28 | +0.0035 | 0.0455 |
| betclic_fr | 30 | +0.0076 | 0.0460 |
| leovegas_se | 58 | -0.0020 | 0.0463 |
| onexbet | 56 | -0.0047 | 0.0465 |
| unibet_se | 58 | -0.0049 | 0.0465 |
| gtbets | 36 | -0.0008 | 0.0468 |
| unibet_nl | 42 | -0.0040 | 0.0472 |
| unibet_fr | 29 | +0.0128 | 0.0474 |
| everygame | 22 | +0.0020 | 0.0483 |
| marathonbet | 37 | -0.0004 | 0.0498 |
| pmu_fr | 37 | +0.0100 | 0.0510 |
| tipico_de | 25 | +0.0176 | 0.0629 |
