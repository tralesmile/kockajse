# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 6 strategies with 20+ scored bets beats the tax; best is fav_flat at -1.0% after tax on 24 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 48 settled tickets (win rate 33%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 33, 91% of runs end below the start and 76% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 117 | 69.2% | 65.8% | -10.3% | 5.7 |
| h2h | 157 | 72.6% | 66.7% | -0.9% | 5.0 |
| h2h, odds < 1.30 | 58 | 81.0% | 77.1% | -2.7% | 6.2 |
| h2h, odds >= 1.30 | 99 | 67.7% | 60.6% | +0.1% | 7.1 |
| spreads | 338 | 50.3% | 50.1% | -11.8% | 4.8 |
| spreads, |line| <= 15 | 178 | 50.0% | 50.2% | -12.2% | 6.6 |
| spreads, |line| > 15 | 160 | 50.6% | 50.0% | -11.4% | 6.9 |
| totals | 461 | 54.2% | 51.9% | -8.7% | 3.9 |
| totals Over | 251 | 57.8% | 52.3% | -3.6% | 5.2 |
| totals Under | 210 | 50.0% | 51.4% | -14.8% | 5.9 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.28).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 756 | 51.2% | 50.3% | -10.9% | 3.2 |
| 55-65% | 149 | 62.4% | 58.8% | -6.4% | 6.0 |
| 65-75% | 97 | 78.4% | 71.0% | -1.5% | 5.3 |
| 75-100% | 69 | 84.1% | 77.0% | +0.0% | 5.3 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: prev_rule (+53.3%, 17 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| prev_rule | 17 | 17 | 100% | 82% | +53.3% | 5.6 | 8 | 100% |
| fav_wide | 29 | 27 | 93% | 78% | +7.6% | 5.7 | 6 | 67% |
| fav_flat | 44 | 39 | 89% | 76% | +0.5% | 5.6 | 11 | 55% |
| banker_double | 18 | 16 | 89% | 67% | -3.2% | 8.4 | 9 | 78% |
| tax_best | 47 | 37 | 79% | 65% | +11.1% | 9.0 | 19 | 58% |
| late_wide | 16 | 14 | 88% | 64% | -0.8% | 9.9 | 6 | 67% |
| veto_ticket | 19 | 16 | 84% | 62% | +28.1% | 13.9 | 9 | 67% |
| likely_ticket | 39 | 30 | 77% | 62% | +14.2% | 10.6 | 19 | 63% |
| h2h_ticket | 32 | 25 | 78% | 61% | +11.2% | 11.1 | 14 | 57% |
| ai_own | 56 | 41 | 73% | 60% | +6.6% | 9.0 | 24 | 50% |
| h2h_ticket_best | 36 | 27 | 75% | 59% | +9.1% | 11.0 | 14 | 50% |
| late_ticket_best | 37 | 27 | 73% | 57% | +9.8% | 11.7 | 17 | 41% |
| power_value | 16 | 13 | 81% | 57% | +5.7% | 15.8 | 11 | 73% |
| veto_ticket_best | 22 | 17 | 77% | 57% | +15.5% | 14.3 | 9 | 56% |
| power_ticket | 53 | 37 | 70% | 56% | -4.1% | 9.0 | 22 | 36% |
| edge_first | 46 | 32 | 70% | 55% | +12.3% | 11.3 | 23 | 48% |
| tax_market | 40 | 28 | 70% | 55% | +3.3% | 11.3 | 19 | 47% |
| actual_best | 52 | 35 | 67% | 54% | -1.4% | 10.0 | 22 | 36% |
| actual | 55 | 36 | 65% | 52% | -6.5% | 9.6 | 23 | 35% |
| late_ticket | 35 | 24 | 69% | 52% | +5.8% | 12.6 | 17 | 41% |
| market | 49 | 31 | 63% | 49% | -7.3% | 10.4 | 23 | 39% |
| late_power | 10 | 8 | 80% | 49% | -2.4% | 16.8 | 4 | 50% |
| single | 22 | 15 | 68% | 47% | +6.5% | 16.5 | 22 | 68% |
| late_value | 54 | 23 | 43% | 30% | -3.7% | 16.0 | 16 | 25% |
| value_single | 71 | 24 | 34% | 24% | -20.7% | 13.9 | 19 | 11% |
| value_ticket | 16 | 7 | 44% | 23% | +3.2% | 31.2 | 15 | 40% |

## Does the AI add anything to the sharp chance?

1073 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23344 |
| 0.10 | 0.23363 |
| 0.20 | 0.23384 |
| 0.35 | 0.23419 |
| 0.50 | 0.23460 |
| 1.00 | 0.23632 |

Live weight 0.20 vs 0: Brier gain -3.9 +- 2.0 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.045 +- 0.031. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +3.6 points (273), AVOID +1.5 points (270), RISKY +2.0 points (530)

## Does a ticket's joint chance predict its win rate? (no-bet gate test)

Settled shadow tickets of every ticket strategy pooled (one ticket = one strategy on one day); joint chance = product of the legs' sharp chances. A win rate that follows the joint chance means a gate on a high joint chance buys a higher hit rate for fewer bets.

| Joint chance | Tickets | Won | Mean joint chance | Mean legs |
|---|---|---|---|---|
| 0-30% | 19 | 32% | 28% | 2.2 |
| 30-45% | 234 | 50% | 36% | 2.3 |
| 45-60% | 8 | 50% | 49% | 2.1 |
| 75-100% | 10 | 80% | 84% | 2.0 |

## Which bookmaker's first price best predicts Pinnacle's closing chance?

165 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0335, average of all books 0.0338; paired absolute-error gain of the average over Pinnacle -0.0024 +- 0.0008.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 51 | -0.0080 | 0.0268 |
| betonlineag | 147 | -0.0018 | 0.0316 |
| pinnacle | 165 | +0.0024 | 0.0335 |
| winamax_de | 135 | -0.0017 | 0.0349 |
| betsson | 158 | +0.0003 | 0.0356 |
| matchbook | 103 | -0.0027 | 0.0357 |
| nordicbet | 157 | +0.0002 | 0.0357 |
| sport888 | 179 | -0.0019 | 0.0360 |
| williamhill | 153 | -0.0008 | 0.0368 |
| codere_it | 115 | -0.0044 | 0.0368 |
| onexbet | 174 | -0.0025 | 0.0371 |
| betclic_fr | 101 | +0.0031 | 0.0373 |
| mybookieag | 81 | +0.0019 | 0.0374 |
| gtbets | 115 | +0.0011 | 0.0376 |
| coolbet | 112 | -0.0046 | 0.0378 |
| winamax_fr | 121 | +0.0066 | 0.0379 |
| unibet_se | 177 | -0.0026 | 0.0392 |
| unibet_nl | 160 | -0.0041 | 0.0392 |
| leovegas_se | 178 | +0.0001 | 0.0394 |
| marathonbet | 119 | -0.0007 | 0.0395 |
| unibet_fr | 99 | +0.0144 | 0.0400 |
| everygame | 50 | +0.0094 | 0.0403 |
| betfair_ex_eu | 145 | -0.0017 | 0.0418 |
| pmu_fr | 107 | +0.0106 | 0.0429 |
| tipico_de | 90 | +0.0106 | 0.0459 |
