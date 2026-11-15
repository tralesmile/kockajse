# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 5 strategies with 20+ scored bets beats the tax; best is late_value at -6.6% after tax on 20 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 37 settled tickets (win rate 27%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 26, 98% of runs end below the start and 89% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 90 | 68.9% | 65.9% | -10.7% | 6.5 |
| h2h | 95 | 71.6% | 66.7% | -2.2% | 6.6 |
| h2h, odds < 1.30 | 42 | 81.0% | 77.0% | -2.6% | 7.4 |
| h2h, odds >= 1.30 | 53 | 64.2% | 58.6% | -1.9% | 10.4 |
| spreads | 179 | 49.2% | 50.1% | -13.7% | 6.6 |
| spreads, |line| <= 15 | 100 | 49.0% | 50.2% | -13.9% | 8.8 |
| spreads, |line| > 15 | 79 | 49.4% | 50.0% | -13.5% | 9.9 |
| totals | 254 | 52.8% | 52.2% | -11.8% | 5.3 |
| totals Over | 135 | 54.8% | 52.6% | -9.5% | 7.1 |
| totals Under | 119 | 50.4% | 51.8% | -14.5% | 7.8 |

## Favourite-longshot check: results by market-chance band

Settled picks at the average price, flat stake, after the tax. A calibration slope above 1 means favourites win more often than priced and longshots less often (now 1.29).

| Market chance | Picks | Won | Priced | Return after tax | se |
|---|---|---|---|---|---|
| 45-55% | 409 | 49.4% | 50.3% | -14.1% | 4.3 |
| 55-65% | 95 | 60.0% | 58.8% | -9.7% | 7.6 |
| 65-75% | 62 | 79.0% | 71.1% | -1.0% | 6.6 |
| 75-100% | 51 | 84.3% | 76.9% | +0.4% | 6.1 |

## Does the AI add anything to the sharp chance?

618 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23179 |
| 0.10 | 0.23185 |
| 0.20 | 0.23194 |
| 0.35 | 0.23213 |
| 0.50 | 0.23237 |
| 1.00 | 0.23355 |

Live weight 0.20 vs 0: Brier gain -1.6 +- 2.7 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.012 +- 0.040. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +2.2 points (175), AVOID -0.8 points (145), RISKY +1.4 points (298)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

63 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0411, average of all books 0.0396; paired absolute-error gain of the average over Pinnacle -0.0009 +- 0.0011.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 23 | -0.0054 | 0.0280 |
| betonlineag | 56 | -0.0022 | 0.0360 |
| matchbook | 46 | -0.0052 | 0.0385 |
| winamax_de | 56 | +0.0017 | 0.0397 |
| sport888 | 69 | -0.0025 | 0.0409 |
| pinnacle | 63 | +0.0035 | 0.0411 |
| betfair_ex_eu | 63 | -0.0057 | 0.0412 |
| nordicbet | 62 | +0.0004 | 0.0412 |
| betsson | 62 | +0.0002 | 0.0413 |
| williamhill | 65 | -0.0027 | 0.0418 |
| codere_it | 46 | -0.0032 | 0.0429 |
| winamax_fr | 41 | +0.0104 | 0.0437 |
| coolbet | 44 | -0.0034 | 0.0440 |
| mybookieag | 34 | -0.0005 | 0.0442 |
| betclic_fr | 36 | +0.0066 | 0.0446 |
| onexbet | 71 | -0.0053 | 0.0447 |
| leovegas_se | 73 | -0.0023 | 0.0448 |
| unibet_se | 73 | -0.0049 | 0.0452 |
| gtbets | 42 | +0.0010 | 0.0452 |
| unibet_nl | 52 | -0.0033 | 0.0459 |
| unibet_fr | 30 | +0.0130 | 0.0467 |
| everygame | 23 | +0.0029 | 0.0475 |
| marathonbet | 46 | -0.0028 | 0.0489 |
| pmu_fr | 43 | +0.0095 | 0.0495 |
| tipico_de | 29 | +0.0179 | 0.0609 |
