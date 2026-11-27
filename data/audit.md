# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 7 strategies with 20+ scored bets beats the tax; best is fav_flat at -1.3% after tax on 27 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 49 settled tickets (win rate 35%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 35, 89% of runs end below the start and 71% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 118 | 68.6% | 65.7% | -11.0% | 5.7 |
| h2h | 164 | 72.6% | 66.6% | -0.7% | 4.9 |
| h2h, odds < 1.30 | 59 | 79.7% | 77.1% | -4.3% | 6.4 |
| h2h, odds >= 1.30 | 105 | 68.6% | 60.8% | +1.3% | 6.9 |
| spreads | 338 | 50.3% | 50.1% | -11.8% | 4.8 |
| spreads, |line| <= 15 | 178 | 50.0% | 50.2% | -12.2% | 6.6 |
| spreads, |line| > 15 | 160 | 50.6% | 50.0% | -11.4% | 6.9 |
| totals | 479 | 54.3% | 52.0% | -8.6% | 3.9 |
| totals Over | 261 | 57.9% | 52.3% | -3.5% | 5.1 |
| totals Under | 218 | 50.0% | 51.5% | -14.8% | 5.8 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.26).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 769 | 51.1% | 50.3% | -11.0% | 3.1 |
| 55-65% | 158 | 63.3% | 58.8% | -4.9% | 5.8 |
| 65-75% | 100 | 78.0% | 71.0% | -1.8% | 5.3 |
| 75-100% | 70 | 82.9% | 77.0% | -1.4% | 5.4 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: prev_rule (+53.6%, 19 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| prev_rule | 19 | 19 | 100% | 83% | +53.6% | 5.0 | 9 | 100% |
| fav_wide | 33 | 31 | 94% | 80% | +9.0% | 5.1 | 7 | 71% |
| fav_flat | 47 | 42 | 89% | 77% | +1.4% | 5.2 | 12 | 58% |
| banker_double | 20 | 18 | 90% | 70% | -1.7% | 7.6 | 10 | 80% |
| tax_best | 50 | 40 | 80% | 67% | +12.8% | 8.5 | 20 | 60% |
| late_wide | 17 | 15 | 88% | 66% | +0.5% | 9.4 | 7 | 71% |
| veto_ticket | 21 | 18 | 86% | 65% | +30.7% | 12.7 | 10 | 70% |
| likely_ticket | 41 | 32 | 78% | 63% | +16.0% | 10.2 | 20 | 65% |
| h2h_ticket | 34 | 27 | 79% | 63% | +14.0% | 10.6 | 15 | 60% |
| h2h_ticket_best | 38 | 29 | 76% | 61% | +11.3% | 10.6 | 15 | 53% |
| ai_own | 58 | 42 | 72% | 60% | +5.7% | 9.0 | 25 | 48% |
| banker | 10 | 9 | 90% | 60% | -1.5% | 11.1 | 10 | 90% |
| power_ticket | 55 | 39 | 71% | 58% | -2.2% | 8.8 | 23 | 39% |
| late_ticket_best | 37 | 27 | 73% | 57% | +9.8% | 11.7 | 17 | 41% |
| power_value | 16 | 13 | 81% | 57% | +5.7% | 15.8 | 11 | 73% |
| tax_market | 42 | 30 | 71% | 56% | +6.0% | 10.9 | 20 | 50% |
| actual_best | 55 | 38 | 69% | 56% | +0.8% | 9.6 | 23 | 39% |
| veto_ticket_best | 24 | 18 | 75% | 55% | +12.5% | 14.1 | 10 | 50% |
| edge_first | 48 | 33 | 69% | 55% | +10.9% | 11.1 | 24 | 46% |
| actual | 58 | 39 | 67% | 54% | -4.3% | 9.2 | 24 | 38% |
| late_ticket | 35 | 24 | 69% | 52% | +5.8% | 12.6 | 17 | 41% |
| market | 51 | 33 | 65% | 51% | -5.1% | 10.1 | 24 | 42% |
| single | 23 | 16 | 70% | 49% | +8.7% | 16.0 | 23 | 70% |
| late_power | 10 | 8 | 80% | 49% | -2.4% | 16.8 | 4 | 50% |
| late_value | 58 | 25 | 43% | 31% | -1.7% | 15.6 | 16 | 25% |
| value_single | 71 | 24 | 34% | 24% | -20.7% | 13.9 | 19 | 11% |
| value_ticket | 16 | 7 | 44% | 23% | +3.2% | 31.2 | 15 | 40% |

## Does the AI add anything to the sharp chance?

1099 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23380 |
| 0.10 | 0.23399 |
| 0.20 | 0.23419 |
| 0.35 | 0.23454 |
| 0.50 | 0.23494 |
| 1.00 | 0.23664 |

Live weight 0.20 vs 0: Brier gain -3.9 +- 2.0 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.045 +- 0.030. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +3.6 points (283), AVOID +1.3 points (275), RISKY +2.1 points (541)

## Does a ticket's joint chance predict its win rate? (no-bet gate test)

Settled shadow tickets of every ticket strategy pooled (one ticket = one strategy on one day); joint chance = product of the legs' sharp chances. A win rate that follows the joint chance means a gate on a high joint chance buys a higher hit rate for fewer bets.

| Joint chance | Tickets | Won | Mean joint chance | Mean legs |
|---|---|---|---|---|
| 0-30% | 22 | 41% | 28% | 2.3 |
| 30-45% | 244 | 51% | 36% | 2.3 |
| 45-60% | 8 | 50% | 49% | 2.1 |
| 75-100% | 11 | 82% | 83% | 2.0 |

## What predicts the sharp price's move before kick-off?

A slope of 1 means Pinnacle moves all the way to the signal by the close, 0 that the signal says nothing. Match-winner prices; the move is far less noisy than results, so this settles questions much sooner. The lead books (BetOnline, Betfair Exchange, Matchbook) were chosen after comparing 22 books on matches up to 26 Nov, so only the later row is a fair test.

| Signal | Matches or picks | Slope | se |
|---|---|---|---|
| Lead books minus Pinnacle, all matches | 161 | +0.84 | 0.30 |
| Lead books minus Pinnacle, first priced from 2026-11-27 (out of sample, 0 so far) | - | - | - |
| AI chance minus sharp chance (logged picks, all bet types) | 332 | +0.02 | 0.03 |

Mean move of the favourite's chance (points): lead books at or above Pinnacle +0.85 +- 0.46 (46); lead books below Pinnacle -0.58 +- 0.30 (115).

Which strategies' match-winner legs lose sharp support after they are picked (closing minus that morning's Pinnacle power chance; negative = the chance used to choose them was too high):

| Strategy | Legs | Move (points) | se |
|---|---|---|---|
| power_value | 8 | -1.88 | 1.92 |
| tax_market | 18 | -1.84 | 1.10 |
| ai_own | 18 | -1.11 | 1.11 |
| power_ticket | 24 | -1.02 | 0.93 |
| veto_ticket_best | 13 | -1.00 | 0.86 |
| market | 18 | -0.89 | 1.26 |
| fav_wide | 20 | -0.88 | 0.31 |
| banker_double | 13 | -0.80 | 0.39 |
| veto_ticket | 10 | -0.66 | 1.08 |
| h2h_ticket_best | 12 | -0.60 | 0.78 |
| h2h_ticket | 15 | -0.58 | 0.48 |
| fav_flat | 26 | -0.56 | 0.27 |
| value_single | 28 | -0.50 | 0.39 |
| prev_rule | 9 | -0.46 | 1.21 |
| edge_first | 10 | -0.45 | 1.03 |
| actual | 31 | -0.03 | 0.65 |
| actual_best | 31 | -0.03 | 0.65 |
| likely_ticket | 16 | +0.35 | 0.90 |
| tax_best | 32 | +0.35 | 0.56 |
| value_ticket | 9 | +0.78 | 0.52 |

## Which bookmaker's first price best predicts Pinnacle's closing chance?

179 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0329, average of all books 0.0334; paired absolute-error gain of the average over Pinnacle -0.0023 +- 0.0008.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 52 | -0.0078 | 0.0265 |
| betonlineag | 160 | -0.0007 | 0.0311 |
| pinnacle | 179 | +0.0028 | 0.0329 |
| winamax_de | 144 | -0.0008 | 0.0346 |
| matchbook | 116 | -0.0018 | 0.0347 |
| betsson | 171 | +0.0012 | 0.0354 |
| nordicbet | 170 | +0.0011 | 0.0354 |
| sport888 | 193 | -0.0014 | 0.0355 |
| codere_it | 123 | -0.0038 | 0.0360 |
| williamhill | 167 | -0.0003 | 0.0361 |
| onexbet | 188 | -0.0019 | 0.0364 |
| betclic_fr | 115 | +0.0047 | 0.0367 |
| coolbet | 125 | -0.0040 | 0.0368 |
| mybookieag | 82 | +0.0018 | 0.0372 |
| gtbets | 116 | +0.0010 | 0.0375 |
| winamax_fr | 130 | +0.0077 | 0.0377 |
| unibet_nl | 174 | -0.0039 | 0.0385 |
| marathonbet | 132 | +0.0005 | 0.0385 |
| unibet_se | 186 | -0.0026 | 0.0386 |
| leovegas_se | 192 | +0.0006 | 0.0388 |
| everygame | 50 | +0.0094 | 0.0403 |
| unibet_fr | 113 | +0.0165 | 0.0405 |
| betfair_ex_eu | 159 | -0.0012 | 0.0407 |
| pmu_fr | 116 | +0.0113 | 0.0422 |
| tipico_de | 92 | +0.0109 | 0.0456 |
