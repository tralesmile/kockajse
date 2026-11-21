# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.1% after tax on 35 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 43 settled tickets (win rate 30%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 30, 95% of runs end below the start and 83% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 98 | 68.4% | 65.9% | -11.9% | 6.2 |
| h2h | 121 | 72.7% | 67.0% | -0.9% | 5.7 |
| h2h, odds < 1.30 | 49 | 81.6% | 77.0% | -1.8% | 6.7 |
| h2h, odds >= 1.30 | 72 | 66.7% | 60.2% | -0.3% | 8.5 |
| spreads | 286 | 50.0% | 50.1% | -12.3% | 5.2 |
| spreads, |line| <= 15 | 140 | 49.3% | 50.2% | -13.4% | 7.4 |
| spreads, |line| > 15 | 146 | 50.7% | 50.1% | -11.3% | 7.3 |
| totals | 364 | 53.0% | 51.8% | -10.6% | 4.4 |
| totals Over | 193 | 56.5% | 52.2% | -5.6% | 6.0 |
| totals Under | 171 | 49.1% | 51.4% | -16.2% | 6.6 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.28).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 621 | 50.2% | 50.2% | -12.5% | 3.5 |
| 55-65% | 112 | 60.7% | 58.9% | -8.9% | 7.0 |
| 65-75% | 76 | 78.9% | 70.9% | -0.6% | 6.0 |
| 75-100% | 59 | 84.7% | 76.9% | +0.9% | 5.6 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: late_value (+22.1%, 35 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| tax_best | 35 | 27 | 77% | 61% | +7.4% | 10.6 | 14 | 57% |
| fav_flat | 24 | 19 | 79% | 60% | -11.3% | 9.5 | 7 | 29% |
| ai_own | 45 | 33 | 73% | 59% | +6.8% | 10.1 | 19 | 47% |
| h2h_ticket | 19 | 15 | 79% | 57% | +15.8% | 14.8 | 9 | 67% |
| late_ticket_best | 25 | 19 | 76% | 57% | +15.5% | 14.0 | 12 | 50% |
| late_ticket | 25 | 18 | 72% | 52% | +10.5% | 14.6 | 12 | 50% |
| likely_ticket | 29 | 20 | 69% | 51% | +1.2% | 13.2 | 14 | 50% |
| tax_market | 29 | 20 | 69% | 51% | +2.6% | 13.5 | 14 | 43% |
| power_ticket | 39 | 25 | 64% | 48% | -10.4% | 11.1 | 17 | 29% |
| edge_first | 36 | 23 | 64% | 48% | +2.2% | 13.2 | 18 | 39% |
| h2h_ticket_best | 22 | 15 | 68% | 47% | +2.1% | 15.7 | 9 | 44% |
| actual_best | 40 | 25 | 62% | 47% | -8.6% | 11.8 | 17 | 29% |
| actual | 43 | 26 | 60% | 46% | -13.5% | 11.2 | 18 | 28% |
| market | 39 | 23 | 59% | 43% | -14.4% | 11.8 | 18 | 33% |
| single | 17 | 10 | 59% | 36% | -10.2% | 19.5 | 17 | 59% |
| late_value | 35 | 18 | 51% | 36% | +22.1% | 21.2 | 11 | 36% |
| value_single | 39 | 10 | 26% | 15% | -38.5% | 17.9 | 14 | 7% |
| value_ticket | 10 | 1 | 10% | 2% | -70.5% | 29.6 | 10 | 10% |

## Does the AI add anything to the sharp chance?

869 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23414 |
| 0.10 | 0.23435 |
| 0.20 | 0.23459 |
| 0.35 | 0.23500 |
| 0.50 | 0.23547 |
| 1.00 | 0.23748 |

Live weight 0.20 vs 0: Brier gain -4.5 +- 2.4 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.051 +- 0.034. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.0 points (227), AVOID +2.4 points (226), RISKY +0.8 points (416)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

112 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0358, average of all books 0.0354; paired absolute-error gain of the average over Pinnacle -0.0020 +- 0.0010.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 36 | -0.0113 | 0.0309 |
| betonlineag | 97 | -0.0060 | 0.0329 |
| pinnacle | 112 | -0.0002 | 0.0358 |
| winamax_de | 94 | -0.0024 | 0.0369 |
| sport888 | 126 | -0.0039 | 0.0370 |
| nordicbet | 107 | -0.0028 | 0.0374 |
| betsson | 107 | -0.0029 | 0.0374 |
| williamhill | 106 | -0.0041 | 0.0386 |
| betclic_fr | 68 | +0.0019 | 0.0388 |
| winamax_fr | 80 | +0.0051 | 0.0391 |
| matchbook | 65 | -0.0058 | 0.0395 |
| gtbets | 78 | -0.0020 | 0.0395 |
| onexbet | 121 | -0.0056 | 0.0395 |
| codere_it | 74 | -0.0067 | 0.0399 |
| mybookieag | 59 | -0.0013 | 0.0401 |
| leovegas_se | 124 | -0.0034 | 0.0402 |
| unibet_se | 124 | -0.0060 | 0.0404 |
| unibet_nl | 104 | -0.0074 | 0.0406 |
| everygame | 35 | +0.0036 | 0.0414 |
| coolbet | 69 | -0.0071 | 0.0414 |
| unibet_fr | 60 | +0.0110 | 0.0419 |
| marathonbet | 81 | -0.0037 | 0.0428 |
| pmu_fr | 69 | +0.0077 | 0.0453 |
| betfair_ex_eu | 97 | -0.0036 | 0.0471 |
| tipico_de | 56 | +0.0079 | 0.0501 |
