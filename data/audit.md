# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 6 strategies with 20+ scored bets beats the tax; best is fav_flat at -1.0% after tax on 21 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 47 settled tickets (win rate 32%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 32, 93% of runs end below the start and 80% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 104 | 68.3% | 65.6% | -11.5% | 6.1 |
| h2h | 150 | 74.0% | 67.1% | +0.6% | 5.1 |
| h2h, odds < 1.30 | 58 | 81.0% | 77.1% | -2.7% | 6.2 |
| h2h, odds >= 1.30 | 92 | 69.6% | 60.8% | +2.7% | 7.3 |
| spreads | 325 | 50.2% | 50.1% | -12.1% | 4.9 |
| spreads, |line| <= 15 | 169 | 49.7% | 50.2% | -12.7% | 6.8 |
| spreads, |line| > 15 | 156 | 50.6% | 50.1% | -11.3% | 7.0 |
| totals | 442 | 54.3% | 51.9% | -8.6% | 4.0 |
| totals Over | 242 | 58.3% | 52.3% | -2.8% | 5.3 |
| totals Under | 200 | 49.5% | 51.4% | -15.6% | 6.1 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.28).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 725 | 51.0% | 50.2% | -11.1% | 3.2 |
| 55-65% | 139 | 62.6% | 58.8% | -6.0% | 6.2 |
| 65-75% | 88 | 79.5% | 70.9% | +0.3% | 5.5 |
| 75-100% | 68 | 83.8% | 77.0% | -0.2% | 5.4 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: prev_rule (+53.4%, 15 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| prev_rule | 15 | 15 | 100% | 80% | +53.4% | 5.8 | 7 | 100% |
| fav_flat | 39 | 34 | 87% | 73% | -0.9% | 6.2 | 10 | 50% |
| fav_wide | 23 | 21 | 91% | 73% | +5.5% | 7.1 | 5 | 60% |
| banker_double | 16 | 14 | 88% | 64% | -4.6% | 9.4 | 8 | 75% |
| tax_best | 45 | 35 | 78% | 64% | +8.8% | 9.2 | 18 | 56% |
| ai_own | 54 | 41 | 76% | 63% | +10.6% | 8.9 | 23 | 52% |
| late_wide | 14 | 12 | 86% | 60% | -2.2% | 11.3 | 5 | 60% |
| likely_ticket | 37 | 28 | 76% | 60% | +12.2% | 11.0 | 18 | 61% |
| late_ticket_best | 33 | 25 | 76% | 59% | +12.5% | 11.9 | 15 | 47% |
| veto_ticket | 17 | 14 | 82% | 59% | +25.2% | 15.3 | 8 | 62% |
| h2h_ticket | 29 | 22 | 76% | 58% | +9.0% | 12.2 | 13 | 54% |
| power_ticket | 50 | 35 | 70% | 56% | -3.5% | 9.3 | 21 | 38% |
| h2h_ticket_best | 33 | 24 | 73% | 56% | +6.0% | 11.9 | 13 | 46% |
| power_value | 15 | 12 | 80% | 55% | -4.6% | 12.8 | 10 | 70% |
| edge_first | 44 | 30 | 68% | 53% | +9.5% | 11.6 | 22 | 45% |
| late_ticket | 31 | 22 | 71% | 53% | +8.7% | 13.1 | 15 | 47% |
| veto_ticket_best | 20 | 15 | 75% | 53% | +11.7% | 15.4 | 8 | 50% |
| tax_market | 38 | 26 | 68% | 53% | +0.7% | 11.7 | 18 | 44% |
| actual_best | 50 | 33 | 66% | 52% | -3.9% | 10.2 | 21 | 33% |
| actual | 53 | 34 | 64% | 51% | -8.8% | 9.8 | 22 | 32% |
| late_power | 10 | 8 | 80% | 49% | -2.4% | 16.8 | 4 | 50% |
| market | 47 | 29 | 62% | 47% | -9.8% | 10.7 | 22 | 36% |
| single | 21 | 14 | 67% | 45% | +3.1% | 17.0 | 21 | 67% |
| late_value | 46 | 21 | 46% | 32% | +3.5% | 17.7 | 14 | 29% |
| value_single | 61 | 21 | 34% | 24% | -19.5% | 15.2 | 18 | 11% |
| value_ticket | 15 | 6 | 40% | 20% | -7.2% | 31.5 | 14 | 36% |

## Does the AI add anything to the sharp chance?

1021 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23341 |
| 0.10 | 0.23361 |
| 0.20 | 0.23384 |
| 0.35 | 0.23422 |
| 0.50 | 0.23465 |
| 1.00 | 0.23648 |

Live weight 0.20 vs 0: Brier gain -4.2 +- 2.1 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.048 +- 0.031. The AI shift hurts.

Won minus sharp chance by verdict (picks, mean): AGREE +3.0 points (261), AVOID +2.0 points (260), RISKY +2.1 points (500)

## Does a ticket's joint chance predict its win rate? (no-bet gate test)

Settled shadow tickets of every ticket strategy pooled (one ticket = one strategy on one day); joint chance = product of the legs' sharp chances. A win rate that follows the joint chance means a gate on a high joint chance buys a higher hit rate for fewer bets.

| Joint chance | Tickets | Won | Mean joint chance | Mean legs |
|---|---|---|---|---|
| 0-30% | 19 | 32% | 28% | 2.2 |
| 30-45% | 217 | 48% | 36% | 2.3 |
| 45-60% | 7 | 43% | 49% | 2.1 |
| 75-100% | 9 | 78% | 84% | 2.0 |

## Which bookmaker's first price best predicts Pinnacle's closing chance?

151 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0345, average of all books 0.0350; paired absolute-error gain of the average over Pinnacle -0.0030 +- 0.0009.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 45 | -0.0089 | 0.0281 |
| betonlineag | 131 | -0.0019 | 0.0327 |
| pinnacle | 151 | +0.0025 | 0.0345 |
| winamax_de | 123 | -0.0021 | 0.0361 |
| sport888 | 163 | -0.0019 | 0.0365 |
| betsson | 142 | -0.0001 | 0.0368 |
| nordicbet | 141 | -0.0001 | 0.0369 |
| matchbook | 92 | -0.0026 | 0.0372 |
| williamhill | 137 | -0.0012 | 0.0380 |
| onexbet | 157 | -0.0023 | 0.0382 |
| codere_it | 103 | -0.0046 | 0.0383 |
| mybookieag | 73 | +0.0015 | 0.0387 |
| betclic_fr | 92 | +0.0029 | 0.0388 |
| gtbets | 100 | +0.0018 | 0.0389 |
| winamax_fr | 109 | +0.0060 | 0.0389 |
| coolbet | 101 | -0.0048 | 0.0394 |
| unibet_se | 160 | -0.0019 | 0.0400 |
| leovegas_se | 161 | +0.0008 | 0.0402 |
| unibet_nl | 143 | -0.0035 | 0.0403 |
| unibet_fr | 87 | +0.0132 | 0.0406 |
| everygame | 49 | +0.0096 | 0.0407 |
| marathonbet | 107 | -0.0004 | 0.0413 |
| betfair_ex_eu | 129 | -0.0014 | 0.0434 |
| pmu_fr | 95 | +0.0107 | 0.0445 |
| tipico_de | 86 | +0.0111 | 0.0469 |
