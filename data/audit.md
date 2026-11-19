# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.0% after tax on 32 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 41 settled tickets (win rate 32%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 32, 94% of runs end below the start and 79% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 95 | 68.4% | 65.8% | -11.7% | 6.4 |
| h2h | 109 | 72.5% | 66.9% | -1.2% | 6.1 |
| h2h, odds < 1.30 | 47 | 80.9% | 77.0% | -2.8% | 7.0 |
| h2h, odds >= 1.30 | 62 | 66.1% | 59.3% | -0.0% | 9.3 |
| spreads | 247 | 49.4% | 50.1% | -13.4% | 5.6 |
| spreads, |line| <= 15 | 115 | 48.7% | 50.2% | -14.4% | 8.2 |
| spreads, |line| > 15 | 132 | 50.0% | 50.0% | -12.5% | 7.6 |
| totals | 323 | 52.0% | 52.0% | -12.6% | 4.7 |
| totals Over | 172 | 56.4% | 52.3% | -6.0% | 6.4 |
| totals Under | 151 | 47.0% | 51.6% | -20.0% | 6.9 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.30).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 542 | 49.4% | 50.2% | -13.9% | 3.7 |
| 55-65% | 106 | 59.4% | 58.8% | -10.8% | 7.2 |
| 65-75% | 68 | 79.4% | 71.0% | -0.4% | 6.2 |
| 75-100% | 57 | 84.2% | 76.9% | +0.3% | 5.8 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: h2h_ticket (+37.5%, 15 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| h2h_ticket | 15 | 14 | 93% | 70% | +37.5% | 11.4 | 7 | 86% |
| late_ticket_best | 21 | 17 | 81% | 60% | +23.0% | 14.3 | 10 | 60% |
| ai_own | 39 | 29 | 74% | 59% | +9.8% | 10.9 | 17 | 53% |
| tax_best | 30 | 22 | 73% | 56% | +2.1% | 12.1 | 12 | 50% |
| fav_flat | 18 | 14 | 78% | 55% | -13.2% | 11.3 | 5 | 20% |
| tax_market | 25 | 18 | 72% | 52% | +6.4% | 14.2 | 12 | 50% |
| power_ticket | 35 | 24 | 69% | 52% | -4.1% | 11.4 | 15 | 33% |
| late_ticket | 21 | 15 | 71% | 50% | +9.1% | 16.0 | 10 | 50% |
| likely_ticket | 25 | 17 | 68% | 48% | -0.1% | 14.4 | 12 | 50% |
| h2h_ticket_best | 17 | 12 | 71% | 47% | +7.3% | 17.9 | 7 | 57% |
| market | 35 | 22 | 63% | 46% | -8.5% | 12.3 | 16 | 38% |
| actual_best | 34 | 21 | 62% | 45% | -8.2% | 13.1 | 15 | 33% |
| actual | 37 | 22 | 59% | 43% | -13.5% | 12.3 | 16 | 31% |
| edge_first | 32 | 19 | 59% | 42% | -4.3% | 14.4 | 16 | 31% |
| late_value | 32 | 17 | 53% | 36% | +27.8% | 22.5 | 10 | 40% |
| single | 15 | 9 | 60% | 36% | -10.0% | 20.4 | 15 | 60% |
| value_single | 35 | 9 | 26% | 14% | -36.7% | 19.4 | 12 | 8% |

## Does the AI add anything to the sharp chance?

774 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23373 |
| 0.10 | 0.23383 |
| 0.20 | 0.23397 |
| 0.35 | 0.23421 |
| 0.50 | 0.23450 |
| 1.00 | 0.23587 |

Live weight 0.20 vs 0: Brier gain -2.4 +- 2.4 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.026 +- 0.036. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +1.9 points (210), AVOID +0.6 points (197), RISKY +0.5 points (367)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

94 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0377, average of all books 0.0372; paired absolute-error gain of the average over Pinnacle -0.0022 +- 0.0011.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 33 | -0.0112 | 0.0314 |
| betonlineag | 76 | -0.0051 | 0.0348 |
| pinnacle | 94 | -0.0003 | 0.0377 |
| winamax_de | 79 | -0.0027 | 0.0387 |
| sport888 | 104 | -0.0051 | 0.0387 |
| nordicbet | 88 | -0.0029 | 0.0396 |
| betsson | 88 | -0.0031 | 0.0396 |
| betclic_fr | 57 | +0.0001 | 0.0402 |
| betfair_ex_eu | 77 | -0.0080 | 0.0405 |
| williamhill | 87 | -0.0050 | 0.0405 |
| winamax_fr | 65 | +0.0043 | 0.0410 |
| matchbook | 59 | -0.0068 | 0.0411 |
| codere_it | 62 | -0.0086 | 0.0422 |
| onexbet | 100 | -0.0065 | 0.0423 |
| leovegas_se | 102 | -0.0034 | 0.0426 |
| mybookieag | 49 | -0.0025 | 0.0427 |
| gtbets | 61 | -0.0016 | 0.0427 |
| unibet_se | 102 | -0.0056 | 0.0429 |
| coolbet | 63 | -0.0078 | 0.0430 |
| unibet_nl | 82 | -0.0072 | 0.0436 |
| unibet_fr | 45 | +0.0100 | 0.0443 |
| everygame | 27 | +0.0028 | 0.0449 |
| marathonbet | 66 | -0.0047 | 0.0459 |
| pmu_fr | 62 | +0.0075 | 0.0467 |
| tipico_de | 45 | +0.0057 | 0.0526 |
