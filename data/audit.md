# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 6 strategies with 20+ scored bets beats the tax; best is fav_flat at -1.0% after tax on 21 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 46 settled tickets (win rate 30%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 30, 95% of runs end below the start and 84% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 100 | 68.0% | 65.8% | -12.5% | 6.2 |
| h2h | 140 | 73.6% | 67.1% | +0.1% | 5.3 |
| h2h, odds < 1.30 | 55 | 81.8% | 77.1% | -1.7% | 6.3 |
| h2h, odds >= 1.30 | 85 | 68.2% | 60.7% | +1.2% | 7.7 |
| spreads | 316 | 50.0% | 50.1% | -12.3% | 4.9 |
| spreads, |line| <= 15 | 162 | 49.4% | 50.2% | -13.3% | 6.9 |
| spreads, |line| > 15 | 154 | 50.6% | 50.1% | -11.3% | 7.1 |
| totals | 426 | 53.8% | 51.8% | -9.3% | 4.1 |
| totals Over | 231 | 57.1% | 52.2% | -4.4% | 5.5 |
| totals Under | 195 | 49.7% | 51.3% | -15.1% | 6.1 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.29).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 703 | 50.8% | 50.2% | -11.5% | 3.3 |
| 55-65% | 130 | 60.8% | 58.8% | -8.8% | 6.5 |
| 65-75% | 83 | 79.5% | 70.9% | +0.2% | 5.6 |
| 75-100% | 65 | 84.6% | 77.0% | +0.8% | 5.4 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: prev_rule (+53.4%, 13 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| prev_rule | 13 | 13 | 100% | 77% | +53.4% | 6.2 | 6 | 100% |
| fav_flat | 35 | 30 | 86% | 71% | -3.1% | 6.8 | 9 | 44% |
| fav_wide | 19 | 17 | 89% | 69% | +2.9% | 8.4 | 4 | 50% |
| tax_best | 43 | 33 | 77% | 62% | +6.8% | 9.5 | 17 | 53% |
| ai_own | 52 | 39 | 75% | 62% | +8.9% | 9.2 | 22 | 50% |
| banker_double | 14 | 12 | 86% | 60% | -7.4% | 10.5 | 7 | 71% |
| late_ticket_best | 33 | 25 | 76% | 59% | +12.5% | 11.9 | 15 | 47% |
| likely_ticket | 35 | 26 | 74% | 58% | +9.9% | 11.5 | 17 | 59% |
| late_wide | 13 | 11 | 85% | 58% | -5.1% | 11.8 | 4 | 50% |
| h2h_ticket | 27 | 20 | 74% | 55% | +5.7% | 12.8 | 12 | 50% |
| veto_ticket | 15 | 12 | 80% | 55% | +21.5% | 17.0 | 7 | 57% |
| power_ticket | 47 | 32 | 68% | 54% | -5.7% | 9.8 | 20 | 35% |
| late_ticket | 31 | 22 | 71% | 53% | +8.7% | 13.1 | 15 | 47% |
| veto_ticket_best | 17 | 13 | 76% | 53% | +15.4% | 16.7 | 7 | 57% |
| h2h_ticket_best | 30 | 21 | 70% | 52% | +2.2% | 12.8 | 12 | 42% |
| edge_first | 42 | 28 | 67% | 52% | +7.3% | 12.1 | 21 | 43% |
| actual_best | 48 | 31 | 65% | 50% | -6.6% | 10.5 | 20 | 30% |
| tax_market | 36 | 24 | 67% | 50% | -2.2% | 12.2 | 17 | 41% |
| power_value | 13 | 10 | 77% | 50% | -8.5% | 14.6 | 9 | 67% |
| actual | 51 | 32 | 63% | 49% | -11.3% | 10.0 | 21 | 29% |
| late_power | 10 | 8 | 80% | 49% | -2.4% | 16.8 | 4 | 50% |
| market | 45 | 27 | 60% | 45% | -12.4% | 11.0 | 21 | 33% |
| single | 20 | 13 | 65% | 43% | -0.5% | 17.4 | 20 | 65% |
| late_value | 44 | 21 | 48% | 34% | +8.2% | 18.2 | 14 | 36% |
| value_single | 55 | 18 | 33% | 22% | -21.5% | 16.2 | 17 | 12% |
| value_ticket | 14 | 5 | 36% | 16% | -17.0% | 32.1 | 13 | 31% |

## Does the AI add anything to the sharp chance?

982 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23385 |
| 0.10 | 0.23404 |
| 0.20 | 0.23426 |
| 0.35 | 0.23463 |
| 0.50 | 0.23506 |
| 1.00 | 0.23688 |

Live weight 0.20 vs 0: Brier gain -4.1 +- 2.2 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.046 +- 0.032. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.6 points (250), AVOID +2.0 points (248), RISKY +1.6 points (484)

## Does a ticket's joint chance predict its win rate? (no-bet gate test)

Settled shadow tickets of every ticket strategy pooled (one ticket = one strategy on one day); joint chance = product of the legs' sharp chances. A win rate that follows the joint chance means a gate on a high joint chance buys a higher hit rate for fewer bets.

| Joint chance | Tickets | Won | Mean joint chance | Mean legs |
|---|---|---|---|---|
| 0-30% | 19 | 32% | 28% | 2.2 |
| 30-45% | 207 | 46% | 36% | 2.3 |
| 75-100% | 7 | 71% | 83% | 2.0 |

## Which bookmaker's first price best predicts Pinnacle's closing chance?

145 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0342, average of all books 0.0349; paired absolute-error gain of the average over Pinnacle -0.0033 +- 0.0009.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 44 | -0.0092 | 0.0285 |
| betonlineag | 125 | -0.0019 | 0.0326 |
| pinnacle | 145 | +0.0026 | 0.0342 |
| winamax_de | 119 | -0.0014 | 0.0362 |
| sport888 | 157 | -0.0019 | 0.0365 |
| betsson | 136 | -0.0000 | 0.0368 |
| nordicbet | 135 | +0.0000 | 0.0369 |
| matchbook | 86 | -0.0024 | 0.0372 |
| williamhill | 131 | -0.0012 | 0.0379 |
| codere_it | 97 | -0.0047 | 0.0381 |
| onexbet | 151 | -0.0026 | 0.0383 |
| betclic_fr | 89 | +0.0037 | 0.0391 |
| winamax_fr | 105 | +0.0069 | 0.0392 |
| gtbets | 98 | +0.0019 | 0.0392 |
| coolbet | 95 | -0.0050 | 0.0394 |
| mybookieag | 70 | +0.0013 | 0.0395 |
| unibet_se | 154 | -0.0019 | 0.0400 |
| leovegas_se | 155 | +0.0007 | 0.0402 |
| unibet_nl | 137 | -0.0036 | 0.0402 |
| everygame | 49 | +0.0096 | 0.0407 |
| unibet_fr | 83 | +0.0140 | 0.0412 |
| marathonbet | 101 | -0.0007 | 0.0416 |
| betfair_ex_eu | 123 | -0.0011 | 0.0437 |
| pmu_fr | 91 | +0.0115 | 0.0451 |
| tipico_de | 82 | +0.0102 | 0.0465 |
