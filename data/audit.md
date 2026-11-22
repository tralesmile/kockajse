# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.0% after tax on 37 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 44 settled tickets (win rate 32%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 32, 93% of runs end below the start and 79% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 98 | 68.4% | 65.9% | -11.9% | 6.2 |
| h2h | 127 | 73.2% | 67.2% | -0.6% | 5.5 |
| h2h, odds < 1.30 | 52 | 82.7% | 77.0% | -0.6% | 6.4 |
| h2h, odds >= 1.30 | 75 | 66.7% | 60.4% | -0.6% | 8.3 |
| spreads | 290 | 50.0% | 50.1% | -12.3% | 5.2 |
| spreads, |line| <= 15 | 140 | 49.3% | 50.2% | -13.4% | 7.4 |
| spreads, |line| > 15 | 150 | 50.7% | 50.1% | -11.3% | 7.2 |
| totals | 382 | 53.1% | 51.8% | -10.4% | 4.3 |
| totals Over | 203 | 57.1% | 52.2% | -4.6% | 5.8 |
| totals Under | 179 | 48.6% | 51.4% | -17.1% | 6.4 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.29).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 639 | 50.4% | 50.2% | -12.3% | 3.4 |
| 55-65% | 117 | 60.7% | 58.8% | -8.9% | 6.8 |
| 65-75% | 78 | 78.2% | 70.9% | -1.5% | 6.0 |
| 75-100% | 62 | 85.5% | 76.9% | +1.8% | 5.4 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: late_value (+20.1%, 37 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| fav_flat | 28 | 23 | 82% | 64% | -7.6% | 8.3 | 8 | 38% |
| ai_own | 48 | 36 | 75% | 61% | +8.5% | 9.5 | 20 | 50% |
| tax_best | 38 | 29 | 76% | 61% | +6.4% | 10.3 | 15 | 53% |
| late_ticket_best | 28 | 21 | 75% | 57% | +11.9% | 13.2 | 13 | 46% |
| h2h_ticket | 22 | 17 | 77% | 57% | +11.9% | 13.9 | 10 | 60% |
| fav_wide | 12 | 10 | 83% | 55% | -4.1% | 13.1 | 3 | 33% |
| likely_ticket | 31 | 22 | 71% | 53% | +4.4% | 12.6 | 15 | 53% |
| h2h_ticket_best | 25 | 18 | 72% | 52% | +6.1% | 14.0 | 10 | 50% |
| power_ticket | 42 | 28 | 67% | 52% | -7.4% | 10.5 | 18 | 33% |
| late_ticket | 27 | 19 | 70% | 52% | +7.9% | 14.2 | 13 | 46% |
| actual_best | 43 | 28 | 65% | 50% | -5.4% | 11.1 | 18 | 33% |
| edge_first | 38 | 25 | 66% | 50% | +5.4% | 12.7 | 19 | 42% |
| banker_double | 10 | 8 | 80% | 49% | -14.0% | 14.3 | 5 | 60% |
| actual | 46 | 29 | 63% | 49% | -10.5% | 10.6 | 19 | 32% |
| tax_market | 31 | 20 | 65% | 47% | -4.0% | 13.5 | 15 | 40% |
| market | 41 | 24 | 59% | 43% | -14.9% | 11.5 | 19 | 32% |
| veto_ticket | 10 | 7 | 70% | 40% | +7.0% | 24.0 | 5 | 40% |
| veto_ticket_best | 12 | 8 | 67% | 39% | +2.9% | 22.6 | 5 | 40% |
| single | 18 | 11 | 61% | 39% | -5.9% | 18.9 | 18 | 61% |
| late_value | 37 | 19 | 51% | 36% | +20.1% | 20.4 | 11 | 36% |
| value_single | 49 | 15 | 31% | 20% | -29.8% | 16.2 | 15 | 7% |
| value_ticket | 12 | 3 | 25% | 9% | -47.1% | 29.0 | 11 | 18% |

## Does the AI add anything to the sharp chance?

897 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23380 |
| 0.10 | 0.23400 |
| 0.20 | 0.23422 |
| 0.35 | 0.23461 |
| 0.50 | 0.23506 |
| 1.00 | 0.23697 |

Live weight 0.20 vs 0: Brier gain -4.3 +- 2.4 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.048 +- 0.033. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.1 points (236), AVOID +2.3 points (232), RISKY +1.0 points (429)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

121 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0346, average of all books 0.0344; paired absolute-error gain of the average over Pinnacle -0.0020 +- 0.0009.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 38 | -0.0103 | 0.0303 |
| betonlineag | 105 | -0.0055 | 0.0318 |
| pinnacle | 121 | +0.0002 | 0.0346 |
| sport888 | 134 | -0.0034 | 0.0362 |
| winamax_de | 99 | -0.0015 | 0.0363 |
| betsson | 113 | -0.0021 | 0.0366 |
| nordicbet | 112 | -0.0021 | 0.0367 |
| williamhill | 110 | -0.0038 | 0.0380 |
| matchbook | 70 | -0.0048 | 0.0382 |
| gtbets | 84 | -0.0021 | 0.0382 |
| onexbet | 129 | -0.0050 | 0.0384 |
| betclic_fr | 73 | +0.0036 | 0.0384 |
| codere_it | 79 | -0.0065 | 0.0387 |
| winamax_fr | 85 | +0.0066 | 0.0389 |
| leovegas_se | 133 | -0.0025 | 0.0392 |
| unibet_nl | 112 | -0.0060 | 0.0394 |
| unibet_se | 132 | -0.0049 | 0.0394 |
| mybookieag | 60 | -0.0013 | 0.0397 |
| coolbet | 75 | -0.0066 | 0.0400 |
| everygame | 38 | +0.0050 | 0.0402 |
| unibet_fr | 66 | +0.0121 | 0.0412 |
| marathonbet | 86 | -0.0031 | 0.0417 |
| pmu_fr | 74 | +0.0088 | 0.0445 |
| betfair_ex_eu | 104 | -0.0032 | 0.0456 |
| tipico_de | 61 | +0.0091 | 0.0486 |
