# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 8 strategies with 20+ scored bets beats the tax; best is late_wide at -0.2% after tax on 20 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 50 settled tickets (win rate 34%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 34, 90% of runs end below the start and 74% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 119 | 68.9% | 65.5% | -10.3% | 5.7 |
| h2h | 172 | 72.7% | 66.9% | -1.2% | 4.8 |
| h2h, odds < 1.30 | 65 | 81.5% | 77.1% | -2.2% | 5.8 |
| h2h, odds >= 1.30 | 107 | 67.3% | 60.6% | -0.5% | 6.9 |
| spreads | 347 | 50.7% | 50.1% | -11.1% | 4.7 |
| spreads, |line| <= 15 | 183 | 50.8% | 50.2% | -10.8% | 6.5 |
| spreads, |line| > 15 | 164 | 50.6% | 50.0% | -11.4% | 6.9 |
| totals | 497 | 53.9% | 51.9% | -9.3% | 3.8 |
| totals Over | 271 | 56.8% | 52.3% | -5.2% | 5.1 |
| totals Under | 226 | 50.4% | 51.5% | -14.1% | 5.7 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.28).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 795 | 51.1% | 50.3% | -11.1% | 3.1 |
| 55-65% | 162 | 63.0% | 58.8% | -5.5% | 5.7 |
| 65-75% | 100 | 78.0% | 71.0% | -1.8% | 5.3 |
| 75-100% | 76 | 84.2% | 77.1% | +0.2% | 5.0 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: prev_rule (+43.6%, 22 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| fav_wide | 36 | 34 | 94% | 82% | +9.8% | 4.7 | 8 | 75% |
| fav_flat | 50 | 45 | 90% | 79% | +2.5% | 4.9 | 13 | 62% |
| prev_rule | 22 | 21 | 95% | 78% | +43.6% | 8.3 | 10 | 90% |
| banker_double | 22 | 20 | 91% | 72% | -0.7% | 6.9 | 11 | 82% |
| late_wide | 20 | 18 | 90% | 70% | +4.2% | 8.2 | 9 | 78% |
| tax_best | 53 | 42 | 79% | 67% | +11.1% | 8.3 | 21 | 57% |
| veto_ticket | 24 | 20 | 83% | 64% | +24.4% | 12.3 | 11 | 64% |
| likely_ticket | 44 | 34 | 77% | 63% | +13.5% | 9.8 | 21 | 62% |
| banker | 11 | 10 | 91% | 62% | -0.5% | 10.1 | 11 | 91% |
| late_ticket_best | 43 | 33 | 77% | 62% | +13.5% | 10.2 | 19 | 47% |
| h2h_ticket | 36 | 28 | 78% | 62% | +11.1% | 10.5 | 16 | 56% |
| power_value | 18 | 15 | 83% | 61% | +7.6% | 14.1 | 12 | 75% |
| h2h_ticket_best | 41 | 31 | 76% | 61% | +9.2% | 10.2 | 16 | 50% |
| ai_own | 61 | 44 | 72% | 60% | +4.4% | 8.7 | 26 | 46% |
| power_ticket | 58 | 41 | 71% | 58% | -3.1% | 8.5 | 24 | 38% |
| actual_best | 58 | 40 | 69% | 56% | -0.1% | 9.2 | 24 | 38% |
| tax_market | 44 | 31 | 70% | 56% | +3.9% | 10.7 | 21 | 48% |
| veto_ticket_best | 27 | 20 | 74% | 55% | +9.0% | 13.2 | 11 | 45% |
| late_power | 12 | 10 | 83% | 55% | +1.9% | 14.2 | 5 | 60% |
| actual | 61 | 41 | 67% | 55% | -5.0% | 8.9 | 25 | 36% |
| late_ticket | 40 | 28 | 70% | 55% | +6.4% | 11.5 | 19 | 42% |
| edge_first | 50 | 33 | 66% | 52% | +6.5% | 11.1 | 25 | 44% |
| market | 54 | 35 | 65% | 51% | -5.9% | 9.7 | 25 | 40% |
| single | 24 | 16 | 67% | 47% | +4.2% | 15.9 | 24 | 67% |
| late_value | 60 | 26 | 43% | 32% | -1.5% | 15.3 | 18 | 28% |
| value_single | 75 | 26 | 35% | 25% | -19.1% | 13.5 | 20 | 10% |
| value_ticket | 18 | 7 | 39% | 20% | -8.2% | 28.8 | 16 | 38% |

## Does the AI add anything to the sharp chance?

1135 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23330 |
| 0.10 | 0.23349 |
| 0.20 | 0.23369 |
| 0.35 | 0.23405 |
| 0.50 | 0.23445 |
| 1.00 | 0.23614 |

Live weight 0.20 vs 0: Brier gain -3.9 +- 1.9 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.047 +- 0.030. The AI shift hurts.

Won minus sharp chance by verdict (picks, mean): AGREE +3.0 points (295), AVOID +1.3 points (277), RISKY +2.4 points (563)

## Does a ticket's joint chance predict its win rate? (no-bet gate test)

Settled shadow tickets of every ticket strategy pooled (one ticket = one strategy on one day); joint chance = product of the legs' sharp chances. A win rate that follows the joint chance means a gate on a high joint chance buys a higher hit rate for fewer bets.

| Joint chance | Tickets | Won | Mean joint chance | Mean legs |
|---|---|---|---|---|
| 0-30% | 22 | 41% | 28% | 2.3 |
| 30-45% | 263 | 48% | 36% | 2.3 |
| 45-60% | 9 | 56% | 49% | 2.1 |
| 60-75% | 5 | 80% | 63% | 1.8 |
| 75-100% | 12 | 83% | 83% | 2.0 |

## What predicts the sharp price's move before kick-off?

A slope of 1 means Pinnacle moves all the way to the signal by the close, 0 that the signal says nothing. Match-winner prices; the move is far less noisy than results, so this settles questions much sooner. The lead books (BetOnline, Betfair Exchange, Matchbook) were chosen after comparing 22 books on matches up to 26 Nov, so only the later row is a fair test.

| Signal | Matches or picks | Slope | se |
|---|---|---|---|
| Lead books minus Pinnacle, all matches | 169 | +0.83 | 0.29 |
| Lead books minus Pinnacle, first priced from 2026-11-27 (out of sample, 8 so far) | - | - | - |
| AI chance minus sharp chance (logged picks, all bet types) | 345 | +0.02 | 0.03 |

Mean move of the favourite's chance (points): lead books at or above Pinnacle +0.78 +- 0.43 (50); lead books below Pinnacle -0.54 +- 0.30 (119).

Which strategies' match-winner legs lose sharp support after they are picked (closing minus that morning's Pinnacle power chance; negative = the chance used to choose them was too high):

| Strategy | Legs | Move (points) | se |
|---|---|---|---|
| tax_market | 20 | -1.67 | 1.00 |
| power_value | 10 | -1.51 | 1.54 |
| ai_own | 20 | -1.00 | 1.00 |
| power_ticket | 26 | -0.94 | 0.85 |
| banker_double | 15 | -0.93 | 0.39 |
| fav_wide | 23 | -0.92 | 0.30 |
| veto_ticket_best | 15 | -0.87 | 0.75 |
| market | 20 | -0.80 | 1.13 |
| h2h_ticket_best | 15 | -0.63 | 0.63 |
| fav_flat | 29 | -0.62 | 0.26 |
| veto_ticket | 12 | -0.55 | 0.90 |
| h2h_ticket | 17 | -0.52 | 0.42 |
| edge_first | 10 | -0.45 | 1.03 |
| value_single | 30 | -0.41 | 0.37 |
| prev_rule | 11 | -0.37 | 0.98 |
| actual | 34 | -0.10 | 0.60 |
| actual_best | 34 | -0.10 | 0.60 |
| tax_best | 35 | +0.26 | 0.51 |
| likely_ticket | 18 | +0.31 | 0.80 |
| value_ticket | 9 | +0.78 | 0.52 |

## Which bookmaker's first price best predicts Pinnacle's closing chance?

191 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0324, average of all books 0.0333; paired absolute-error gain of the average over Pinnacle -0.0029 +- 0.0009.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 55 | -0.0077 | 0.0262 |
| betonlineag | 169 | -0.0008 | 0.0309 |
| pinnacle | 191 | +0.0025 | 0.0324 |
| winamax_de | 153 | -0.0020 | 0.0349 |
| matchbook | 118 | -0.0021 | 0.0349 |
| betsson | 182 | -0.0002 | 0.0354 |
| nordicbet | 181 | -0.0003 | 0.0355 |
| sport888 | 206 | -0.0022 | 0.0356 |
| williamhill | 172 | -0.0003 | 0.0357 |
| onexbet | 197 | -0.0019 | 0.0360 |
| codere_it | 132 | -0.0051 | 0.0363 |
| gtbets | 124 | +0.0012 | 0.0365 |
| mybookieag | 85 | +0.0019 | 0.0367 |
| betclic_fr | 124 | +0.0029 | 0.0368 |
| coolbet | 131 | -0.0056 | 0.0372 |
| winamax_fr | 139 | +0.0061 | 0.0377 |
| unibet_se | 195 | -0.0028 | 0.0381 |
| marathonbet | 137 | -0.0000 | 0.0381 |
| unibet_nl | 187 | -0.0051 | 0.0382 |
| leovegas_se | 201 | +0.0003 | 0.0383 |
| everygame | 54 | +0.0093 | 0.0393 |
| unibet_fr | 118 | +0.0160 | 0.0401 |
| betfair_ex_eu | 166 | -0.0014 | 0.0402 |
| pmu_fr | 121 | +0.0106 | 0.0419 |
| tipico_de | 101 | +0.0085 | 0.0446 |
