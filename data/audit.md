# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 6 strategies with 20+ scored bets beats the tax; best is fav_flat at -1.0% after tax on 21 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 45 settled tickets (win rate 31%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 32, 94% of runs end below the start and 82% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 98 | 68.4% | 65.9% | -11.9% | 6.2 |
| h2h | 132 | 73.5% | 67.3% | -0.5% | 5.4 |
| h2h, odds < 1.30 | 53 | 83.0% | 77.0% | -0.2% | 6.3 |
| h2h, odds >= 1.30 | 79 | 67.1% | 60.7% | -0.7% | 8.0 |
| spreads | 292 | 50.0% | 50.1% | -12.3% | 5.1 |
| spreads, |line| <= 15 | 140 | 49.3% | 50.2% | -13.4% | 7.4 |
| spreads, |line| > 15 | 152 | 50.7% | 50.1% | -11.3% | 7.1 |
| totals | 397 | 53.1% | 51.9% | -10.6% | 4.2 |
| totals Over | 213 | 56.3% | 52.3% | -6.1% | 5.7 |
| totals Under | 184 | 49.5% | 51.4% | -15.7% | 6.3 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.31).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 649 | 50.4% | 50.2% | -12.3% | 3.4 |
| 55-65% | 125 | 60.0% | 58.8% | -10.0% | 6.6 |
| 65-75% | 81 | 79.0% | 70.9% | -0.4% | 5.8 |
| 75-100% | 63 | 85.7% | 77.0% | +2.1% | 5.3 |

## Who leads? Win rate and return after tax by shadow strategy

Settled shadow legs, flat stake at the recorded odds, after the tax. Sorted by the lower bound of the 95% win-rate interval, so a small lucky sample does not top the table. Return leader: prev_rule (+51.4%, 11 legs); a return of 0 would be break-even.

| Strategy | Legs | Won | Win rate | 95% lower | Return after tax | se | Days | Days all legs won |
|---|---|---|---|---|---|---|---|---|
| prev_rule | 11 | 11 | 100% | 74% | +51.4% | 7.1 | 5 | 100% |
| fav_flat | 35 | 30 | 86% | 71% | -3.1% | 6.8 | 9 | 44% |
| fav_wide | 19 | 17 | 89% | 69% | +2.9% | 8.4 | 4 | 50% |
| tax_best | 41 | 32 | 78% | 63% | +8.2% | 9.6 | 16 | 56% |
| ai_own | 50 | 38 | 76% | 63% | +10.2% | 9.2 | 21 | 52% |
| late_wide | 13 | 11 | 85% | 58% | -5.1% | 11.8 | 4 | 50% |
| late_ticket_best | 28 | 21 | 75% | 57% | +11.9% | 13.2 | 13 | 46% |
| h2h_ticket | 25 | 19 | 76% | 57% | +8.1% | 13.0 | 11 | 55% |
| likely_ticket | 33 | 24 | 73% | 56% | +7.3% | 12.0 | 16 | 56% |
| banker_double | 12 | 10 | 83% | 55% | -10.4% | 12.1 | 6 | 67% |
| h2h_ticket_best | 28 | 20 | 71% | 53% | +3.9% | 13.1 | 11 | 45% |
| power_ticket | 45 | 30 | 67% | 52% | -8.3% | 10.0 | 19 | 32% |
| late_ticket | 27 | 19 | 70% | 52% | +7.9% | 14.2 | 13 | 46% |
| actual_best | 46 | 30 | 65% | 51% | -6.0% | 10.6 | 19 | 32% |
| power_value | 13 | 10 | 77% | 50% | -8.5% | 14.6 | 9 | 67% |
| veto_ticket | 13 | 10 | 77% | 50% | +14.9% | 19.0 | 6 | 50% |
| edge_first | 40 | 26 | 65% | 50% | +4.5% | 12.5 | 20 | 40% |
| actual | 49 | 31 | 63% | 49% | -10.8% | 10.2 | 20 | 30% |
| late_power | 10 | 8 | 80% | 49% | -2.4% | 16.8 | 4 | 50% |
| veto_ticket_best | 15 | 11 | 73% | 48% | +8.5% | 18.2 | 6 | 50% |
| tax_market | 34 | 22 | 65% | 48% | -5.4% | 12.6 | 16 | 38% |
| market | 43 | 25 | 58% | 43% | -15.4% | 11.2 | 20 | 30% |
| single | 19 | 12 | 63% | 41% | -4.5% | 17.9 | 19 | 63% |
| late_value | 40 | 20 | 50% | 35% | +14.2% | 19.3 | 12 | 33% |
| value_single | 54 | 17 | 31% | 21% | -24.7% | 16.2 | 16 | 6% |
| value_ticket | 13 | 4 | 31% | 13% | -29.7% | 31.9 | 12 | 25% |

## Does the AI add anything to the sharp chance?

919 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23337 |
| 0.10 | 0.23357 |
| 0.20 | 0.23379 |
| 0.35 | 0.23417 |
| 0.50 | 0.23461 |
| 1.00 | 0.23651 |

Live weight 0.20 vs 0: Brier gain -4.2 +- 2.3 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.047 +- 0.033. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.6 points (244), AVOID +2.2 points (236), RISKY +0.9 points (439)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

134 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0331, average of all books 0.0335; paired absolute-error gain of the average over Pinnacle -0.0032 +- 0.0010.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 43 | -0.0093 | 0.0288 |
| betonlineag | 114 | -0.0053 | 0.0309 |
| pinnacle | 134 | +0.0000 | 0.0331 |
| sport888 | 146 | -0.0044 | 0.0353 |
| winamax_de | 111 | -0.0033 | 0.0357 |
| betsson | 124 | -0.0029 | 0.0358 |
| nordicbet | 123 | -0.0029 | 0.0359 |
| matchbook | 78 | -0.0051 | 0.0366 |
| williamhill | 119 | -0.0040 | 0.0368 |
| codere_it | 89 | -0.0074 | 0.0374 |
| onexbet | 139 | -0.0053 | 0.0375 |
| gtbets | 87 | -0.0022 | 0.0378 |
| betclic_fr | 81 | +0.0014 | 0.0378 |
| winamax_fr | 97 | +0.0048 | 0.0381 |
| everygame | 42 | +0.0055 | 0.0385 |
| coolbet | 87 | -0.0080 | 0.0387 |
| unibet_se | 142 | -0.0053 | 0.0388 |
| mybookieag | 63 | -0.0015 | 0.0389 |
| leovegas_se | 143 | -0.0027 | 0.0389 |
| unibet_nl | 125 | -0.0075 | 0.0391 |
| unibet_fr | 75 | +0.0120 | 0.0402 |
| marathonbet | 93 | -0.0035 | 0.0406 |
| pmu_fr | 83 | +0.0085 | 0.0433 |
| betfair_ex_eu | 113 | -0.0035 | 0.0439 |
| tipico_de | 74 | +0.0068 | 0.0451 |
