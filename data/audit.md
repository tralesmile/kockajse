# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.0% after tax on 32 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 42 settled tickets (win rate 31%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 32, 94% of runs end below the start and 81% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 95 | 68.4% | 65.8% | -11.7% | 6.4 |
| h2h | 115 | 73.0% | 67.0% | -0.6% | 5.9 |
| h2h, odds < 1.30 | 49 | 81.6% | 77.0% | -1.8% | 6.7 |
| h2h, odds >= 1.30 | 66 | 66.7% | 59.6% | +0.2% | 9.0 |
| spreads | 266 | 50.0% | 50.1% | -12.3% | 5.4 |
| spreads, |line| <= 15 | 126 | 49.2% | 50.2% | -13.5% | 7.9 |
| spreads, |line| > 15 | 140 | 50.7% | 50.1% | -11.2% | 7.4 |
| totals | 344 | 52.9% | 51.9% | -10.9% | 4.6 |
| totals Over | 183 | 57.4% | 52.2% | -4.2% | 6.2 |
| totals Under | 161 | 47.8% | 51.5% | -18.5% | 6.7 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.28).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 581 | 50.3% | 50.2% | -12.5% | 3.6 |
| 55-65% | 109 | 59.6% | 58.9% | -10.5% | 7.1 |
| 65-75% | 71 | 80.3% | 71.0% | +0.9% | 6.0 |
| 75-100% | 58 | 84.5% | 76.9% | +0.6% | 5.7 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: late_value (+27.8%, 32 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| fav_flat | 21 | 17 | 81% | 60% | -9.7% | 9.8 | 6 | 33% |
| tax_best | 33 | 25 | 76% | 59% | +4.8% | 11.1 | 13 | 54% |
| h2h_ticket | 17 | 14 | 82% | 59% | +21.4% | 15.0 | 8 | 75% |
| ai_own | 42 | 31 | 74% | 59% | +8.1% | 10.5 | 18 | 50% |
| late_ticket_best | 23 | 18 | 78% | 58% | +18.0% | 14.1 | 11 | 55% |
| tax_market | 27 | 19 | 70% | 52% | +5.1% | 14.0 | 13 | 46% |
| late_ticket | 23 | 16 | 70% | 49% | +5.0% | 15.3 | 11 | 45% |
| power_ticket | 37 | 24 | 65% | 49% | -9.2% | 11.4 | 16 | 31% |
| likely_ticket | 27 | 18 | 67% | 48% | -2.7% | 13.9 | 13 | 46% |
| actual_best | 37 | 23 | 62% | 46% | -8.6% | 12.4 | 16 | 31% |
| h2h_ticket_best | 19 | 13 | 68% | 46% | +4.8% | 17.3 | 8 | 50% |
| edge_first | 34 | 21 | 62% | 45% | -0.8% | 13.8 | 17 | 35% |
| actual | 40 | 24 | 60% | 45% | -13.6% | 11.7 | 17 | 29% |
| market | 37 | 22 | 59% | 43% | -13.5% | 12.1 | 17 | 35% |
| late_value | 32 | 17 | 53% | 36% | +27.8% | 22.5 | 10 | 40% |
| single | 16 | 9 | 56% | 33% | -15.6% | 19.9 | 16 | 56% |
| value_single | 36 | 9 | 25% | 14% | -38.5% | 18.9 | 13 | 8% |

## Does the AI add anything to the sharp chance?

820 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23372 |
| 0.10 | 0.23394 |
| 0.20 | 0.23419 |
| 0.35 | 0.23462 |
| 0.50 | 0.23511 |
| 1.00 | 0.23720 |

Live weight 0.20 vs 0: Brier gain -4.7 +- 2.6 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.051 +- 0.035. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.2 points (222), AVOID +2.7 points (223), RISKY +0.4 points (375)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

100 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0370, average of all books 0.0365; paired absolute-error gain of the average over Pinnacle -0.0021 +- 0.0011.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 35 | -0.0122 | 0.0312 |
| betonlineag | 83 | -0.0063 | 0.0341 |
| pinnacle | 100 | -0.0011 | 0.0370 |
| winamax_de | 84 | -0.0034 | 0.0381 |
| sport888 | 112 | -0.0056 | 0.0381 |
| nordicbet | 95 | -0.0038 | 0.0386 |
| betsson | 95 | -0.0039 | 0.0386 |
| betclic_fr | 59 | -0.0008 | 0.0398 |
| williamhill | 94 | -0.0058 | 0.0398 |
| winamax_fr | 70 | +0.0033 | 0.0401 |
| matchbook | 62 | -0.0062 | 0.0401 |
| gtbets | 67 | -0.0018 | 0.0411 |
| onexbet | 108 | -0.0071 | 0.0413 |
| codere_it | 65 | -0.0082 | 0.0413 |
| mybookieag | 52 | -0.0022 | 0.0415 |
| leovegas_se | 110 | -0.0041 | 0.0416 |
| unibet_se | 110 | -0.0062 | 0.0419 |
| coolbet | 66 | -0.0073 | 0.0421 |
| unibet_nl | 90 | -0.0080 | 0.0424 |
| unibet_fr | 50 | +0.0089 | 0.0429 |
| marathonbet | 71 | -0.0055 | 0.0448 |
| everygame | 27 | +0.0028 | 0.0449 |
| pmu_fr | 67 | +0.0069 | 0.0456 |
| betfair_ex_eu | 83 | -0.0050 | 0.0498 |
| tipico_de | 47 | +0.0041 | 0.0520 |
