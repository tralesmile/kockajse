# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.0% after tax on 28 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 40 settled tickets (win rate 30%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 31, 95% of runs end below the start and 83% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 93 | 68.8% | 65.9% | -11.0% | 6.4 |
| h2h | 105 | 71.4% | 66.9% | -2.8% | 6.3 |
| h2h, odds < 1.30 | 45 | 80.0% | 77.0% | -3.9% | 7.3 |
| h2h, odds >= 1.30 | 60 | 65.0% | 59.4% | -1.9% | 9.5 |
| spreads | 233 | 49.4% | 50.1% | -13.4% | 5.8 |
| spreads, |line| <= 15 | 115 | 48.7% | 50.2% | -14.4% | 8.2 |
| spreads, |line| > 15 | 118 | 50.0% | 50.0% | -12.4% | 8.1 |
| totals | 311 | 52.1% | 52.0% | -12.5% | 4.8 |
| totals Over | 166 | 56.6% | 52.3% | -5.7% | 6.5 |
| totals Under | 145 | 46.9% | 51.6% | -20.2% | 7.1 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.27).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 516 | 49.4% | 50.2% | -13.9% | 3.8 |
| 55-65% | 103 | 59.2% | 58.8% | -11.1% | 7.3 |
| 65-75% | 67 | 79.1% | 71.0% | -0.6% | 6.3 |
| 75-100% | 55 | 83.6% | 76.9% | -0.5% | 6.0 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: late_value (+39.4%, 28 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| h2h_ticket | 13 | 12 | 92% | 67% | +34.5% | 13.1 | 6 | 83% |
| late_ticket_best | 19 | 16 | 84% | 62% | +29.3% | 14.3 | 9 | 67% |
| ai_own | 37 | 27 | 73% | 57% | +7.0% | 11.3 | 16 | 50% |
| power_ticket | 33 | 23 | 70% | 53% | -3.5% | 11.5 | 14 | 36% |
| fav_flat | 14 | 11 | 79% | 52% | -12.2% | 12.8 | 4 | 25% |
| tax_best | 27 | 19 | 70% | 52% | -2.1% | 13.1 | 11 | 45% |
| tax_market | 23 | 16 | 70% | 49% | +2.4% | 15.1 | 11 | 45% |
| market | 33 | 21 | 64% | 47% | -8.2% | 12.5 | 15 | 40% |
| late_ticket | 19 | 13 | 68% | 46% | +4.6% | 17.3 | 9 | 44% |
| likely_ticket | 23 | 15 | 65% | 45% | -4.5% | 15.3 | 11 | 45% |
| h2h_ticket_best | 15 | 10 | 67% | 42% | +1.0% | 19.6 | 6 | 50% |
| actual_best | 31 | 18 | 58% | 41% | -12.8% | 14.0 | 14 | 29% |
| actual | 34 | 19 | 56% | 39% | -17.9% | 13.1 | 15 | 27% |
| edge_first | 30 | 17 | 57% | 39% | -8.6% | 15.1 | 15 | 27% |
| late_value | 28 | 16 | 57% | 39% | +39.4% | 24.3 | 9 | 44% |
| single | 14 | 8 | 57% | 33% | -14.4% | 21.4 | 14 | 57% |
| value_single | 35 | 9 | 26% | 14% | -36.7% | 19.4 | 12 | 8% |

## Does the AI add anything to the sharp chance?

742 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23413 |
| 0.10 | 0.23426 |
| 0.20 | 0.23441 |
| 0.35 | 0.23468 |
| 0.50 | 0.23500 |
| 1.00 | 0.23649 |

Live weight 0.20 vs 0: Brier gain -2.7 +- 2.5 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.031 +- 0.037. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +1.3 points (206), AVOID +1.2 points (187), RISKY +0.3 points (349)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

84 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0378, average of all books 0.0376; paired absolute-error gain of the average over Pinnacle -0.0023 +- 0.0012.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 29 | -0.0066 | 0.0268 |
| betonlineag | 71 | -0.0029 | 0.0336 |
| winamax_de | 75 | -0.0009 | 0.0377 |
| pinnacle | 84 | +0.0019 | 0.0378 |
| sport888 | 94 | -0.0043 | 0.0389 |
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
| leovegas_se | 93 | -0.0020 | 0.0431 |
| unibet_se | 93 | -0.0043 | 0.0433 |
| unibet_nl | 72 | -0.0052 | 0.0443 |
| everygame | 27 | +0.0028 | 0.0449 |
| marathonbet | 62 | -0.0022 | 0.0455 |
| unibet_fr | 40 | +0.0125 | 0.0456 |
| pmu_fr | 58 | +0.0097 | 0.0470 |
| tipico_de | 41 | +0.0076 | 0.0546 |
