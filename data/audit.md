# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.1% after tax on 23 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 39 settled tickets (win rate 31%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 31, 95% of runs end below the start and 81% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 93 | 68.8% | 65.9% | -11.0% | 6.4 |
| h2h | 99 | 72.7% | 67.0% | -1.1% | 6.4 |
| h2h, odds < 1.30 | 44 | 81.8% | 77.0% | -1.7% | 7.1 |
| h2h, odds >= 1.30 | 55 | 65.5% | 59.0% | -0.6% | 10.0 |
| spreads | 214 | 49.5% | 50.1% | -13.1% | 6.0 |
| spreads, |line| <= 15 | 106 | 49.1% | 50.2% | -13.8% | 8.6 |
| spreads, |line| > 15 | 108 | 50.0% | 50.1% | -12.5% | 8.5 |
| totals | 294 | 52.0% | 52.0% | -12.7% | 4.9 |
| totals Over | 157 | 56.1% | 52.4% | -6.8% | 6.6 |
| totals Under | 137 | 47.4% | 51.6% | -19.4% | 7.3 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.32).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 482 | 49.4% | 50.2% | -14.1% | 4.0 |
| 55-65% | 98 | 59.2% | 58.8% | -10.9% | 7.5 |
| 65-75% | 65 | 80.0% | 71.0% | +0.3% | 6.3 |
| 75-100% | 54 | 85.2% | 76.9% | +1.4% | 5.8 |

## Does the AI add anything to the sharp chance?

700 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23257 |
| 0.10 | 0.23263 |
| 0.20 | 0.23271 |
| 0.35 | 0.23287 |
| 0.50 | 0.23308 |
| 1.00 | 0.23413 |

Live weight 0.20 vs 0: Brier gain -1.4 +- 2.4 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.011 +- 0.038. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +1.9 points (193), AVOID -0.4 points (171), RISKY +1.2 points (336)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

79 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0377, average of all books 0.0374; paired absolute-error gain of the average over Pinnacle -0.0026 +- 0.0013.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 26 | -0.0052 | 0.0274 |
| betonlineag | 67 | -0.0028 | 0.0344 |
| matchbook | 50 | -0.0049 | 0.0377 |
| pinnacle | 79 | +0.0030 | 0.0377 |
| winamax_de | 68 | -0.0014 | 0.0382 |
| sport888 | 85 | -0.0039 | 0.0386 |
| nordicbet | 75 | -0.0017 | 0.0395 |
| betsson | 75 | -0.0018 | 0.0395 |
| betfair_ex_eu | 71 | -0.0054 | 0.0396 |
| williamhill | 73 | -0.0024 | 0.0400 |
| winamax_fr | 54 | +0.0060 | 0.0405 |
| mybookieag | 42 | -0.0008 | 0.0409 |
| betclic_fr | 49 | +0.0022 | 0.0412 |
| codere_it | 55 | -0.0056 | 0.0413 |
| coolbet | 53 | -0.0063 | 0.0426 |
| onexbet | 82 | -0.0050 | 0.0427 |
| gtbets | 49 | +0.0003 | 0.0428 |
| leovegas_se | 84 | -0.0023 | 0.0432 |
| unibet_se | 84 | -0.0048 | 0.0434 |
| unibet_nl | 64 | -0.0057 | 0.0442 |
| unibet_fr | 34 | +0.0121 | 0.0448 |
| everygame | 27 | +0.0028 | 0.0449 |
| marathonbet | 54 | -0.0028 | 0.0459 |
| pmu_fr | 51 | +0.0102 | 0.0481 |
| tipico_de | 38 | +0.0097 | 0.0562 |
