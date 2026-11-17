# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.2% after tax on 27 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 39 settled tickets (win rate 31%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 31, 95% of runs end below the start and 81% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 93 | 68.8% | 65.9% | -11.0% | 6.4 |
| h2h | 99 | 72.7% | 67.0% | -1.1% | 6.4 |
| h2h, odds < 1.30 | 44 | 81.8% | 77.0% | -1.7% | 7.1 |
| h2h, odds >= 1.30 | 55 | 65.5% | 59.0% | -0.6% | 10.0 |
| spreads | 214 | 49.5% | 50.1% | -13.1% | 6.0 |
| spreads, |line| <= 15 | 106 | 49.1% | 50.2% | -13.8% | 8.6 |
| spreads, |line| > 15 | 108 | 50.0% | 50.1% | -12.5% | 8.5 |
| totals | 294 | 52.0% | 52.0% | -12.7% | 4.9 |
| totals Over | 157 | 56.1% | 52.4% | -6.8% | 6.6 |
| totals Under | 137 | 47.4% | 51.6% | -19.4% | 7.3 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.32).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 482 | 49.4% | 50.2% | -14.1% | 4.0 |
| 55-65% | 98 | 59.2% | 58.8% | -10.9% | 7.5 |
| 65-75% | 65 | 80.0% | 71.0% | +0.3% | 6.3 |
| 75-100% | 54 | 85.2% | 76.9% | +1.4% | 5.8 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: late_value (+38.6%, 23 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| late_ticket_best | 17 | 15 | 88% | 66% | +36.9% | 13.9 | 8 | 75% |
| h2h_ticket | 11 | 10 | 91% | 62% | +31.2% | 14.8 | 5 | 80% |
| ai_own | 35 | 26 | 74% | 58% | +8.1% | 11.4 | 15 | 53% |
| h2h_ticket_best | 12 | 10 | 83% | 55% | +26.3% | 18.0 | 5 | 60% |
| tax_best | 24 | 18 | 75% | 55% | +4.4% | 13.4 | 10 | 50% |
| power_ticket | 31 | 22 | 71% | 53% | -1.9% | 11.8 | 13 | 38% |
| likely_ticket | 21 | 15 | 71% | 50% | +4.6% | 15.3 | 10 | 50% |
| fav_flat | 10 | 8 | 80% | 49% | -10.8% | 14.9 | 3 | 33% |
| tax_market | 21 | 14 | 67% | 45% | -2.4% | 16.1 | 10 | 40% |
| actual_best | 29 | 18 | 62% | 44% | -6.8% | 14.3 | 13 | 31% |
| market | 31 | 19 | 61% | 44% | -12.0% | 13.0 | 14 | 36% |
| edge_first | 28 | 17 | 61% | 42% | -2.0% | 15.4 | 14 | 29% |
| actual | 32 | 19 | 59% | 42% | -12.8% | 13.4 | 14 | 29% |
| late_ticket | 17 | 11 | 65% | 41% | -0.9% | 18.9 | 8 | 38% |
| late_value | 23 | 13 | 57% | 37% | +38.6% | 27.3 | 7 | 43% |
| single | 13 | 8 | 62% | 36% | -7.9% | 22.0 | 13 | 62% |
| value_single | 30 | 7 | 23% | 12% | -38.7% | 21.6 | 11 | 9% |

## Does the AI add anything to the sharp chance?

700 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23257 |
| 0.10 | 0.23263 |
| 0.20 | 0.23271 |
| 0.35 | 0.23287 |
| 0.50 | 0.23308 |
| 1.00 | 0.23413 |

Live weight 0.20 vs 0: Brier gain -1.4 +- 2.4 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.011 +- 0.038. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +1.9 points (193), AVOID -0.4 points (171), RISKY +1.2 points (336)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

83 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0379, average of all books 0.0377; paired absolute-error gain of the average over Pinnacle -0.0023 +- 0.0012.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 29 | -0.0066 | 0.0268 |
| betonlineag | 70 | -0.0032 | 0.0338 |
| winamax_de | 75 | -0.0009 | 0.0377 |
| pinnacle | 83 | +0.0016 | 0.0379 |
| sport888 | 93 | -0.0046 | 0.0391 |
| matchbook | 56 | -0.0037 | 0.0392 |
| nordicbet | 82 | -0.0012 | 0.0392 |
| betsson | 82 | -0.0014 | 0.0393 |
| betfair_ex_eu | 71 | -0.0054 | 0.0396 |
| betclic_fr | 52 | +0.0023 | 0.0401 |
| williamhill | 81 | -0.0031 | 0.0402 |
| winamax_fr | 61 | +0.0065 | 0.0403 |
| codere_it | 58 | -0.0057 | 0.0406 |
| mybookieag | 47 | +0.0004 | 0.0410 |
| coolbet | 59 | -0.0048 | 0.0416 |
| onexbet | 90 | -0.0050 | 0.0425 |
| gtbets | 53 | +0.0018 | 0.0430 |
| leovegas_se | 92 | -0.0025 | 0.0432 |
| unibet_se | 92 | -0.0048 | 0.0433 |
| unibet_nl | 71 | -0.0058 | 0.0444 |
| everygame | 27 | +0.0028 | 0.0449 |
| marathonbet | 62 | -0.0022 | 0.0455 |
| unibet_fr | 40 | +0.0125 | 0.0456 |
| pmu_fr | 58 | +0.0097 | 0.0470 |
| tipico_de | 41 | +0.0076 | 0.0546 |
