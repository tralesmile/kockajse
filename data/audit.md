# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 3 strategies with 20+ scored bets beats the tax; best is pick:AGREE at -10.1% after tax on 54 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 34 settled tickets (win rate 29%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 30, 95% of runs end below the start and 83% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

## Which bet types pay after tax?

Settled picks at the average price, flat stake, after the tax. Handicaps and totals are coin flips that only cost margin and tax; moneyline favourites are the one group near break-even (a return of 0 would be break-even).

| Group | Picks | Won | Market chance | Return after tax | se |
|---|---|---|---|---|---|
| dc | 68 | 69.1% | 66.0% | -9.9% | 7.6 |
| h2h | 78 | 71.8% | 66.9% | -2.2% | 7.2 |
| h2h, odds < 1.30 | 33 | 81.8% | 77.1% | -1.6% | 8.2 |
| h2h, odds >= 1.30 | 45 | 64.4% | 59.4% | -2.6% | 11.1 |
| spreads | 141 | 49.6% | 50.1% | -12.9% | 7.4 |
| spreads, |line| <= 15 | 77 | 49.4% | 50.2% | -13.3% | 10.1 |
| spreads, |line| > 15 | 64 | 50.0% | 50.0% | -12.5% | 11.0 |
| totals | 198 | 52.0% | 52.3% | -13.0% | 6.0 |
| totals Over | 108 | 57.4% | 52.7% | -5.1% | 7.9 |
| totals Under | 90 | 45.6% | 51.7% | -22.5% | 9.0 |

## Does the AI add anything to the sharp chance?

485 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23240 |
| 0.10 | 0.23249 |
| 0.20 | 0.23260 |
| 0.35 | 0.23283 |
| 0.50 | 0.23312 |
| 1.00 | 0.23458 |

Live weight 0.20 vs 0: Brier gain -2.0 +- 3.4 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.015 +- 0.045. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE +0.4 points (133), AVOID -0.6 points (108), RISKY +2.0 points (244)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

50 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0427, average of all books 0.0407; paired absolute-error gain of the average over Pinnacle -0.0000 +- 0.0012.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betanysports | 17 | -0.0041 | 0.0258 |
| betonlineag | 45 | -0.0025 | 0.0372 |
| matchbook | 41 | -0.0045 | 0.0385 |
| winamax_de | 50 | +0.0028 | 0.0404 |
| sport888 | 52 | -0.0007 | 0.0414 |
| betfair_ex_eu | 53 | -0.0040 | 0.0416 |
| williamhill | 50 | -0.0005 | 0.0418 |
| codere_it | 42 | -0.0014 | 0.0419 |
| pinnacle | 50 | +0.0057 | 0.0427 |
| nordicbet | 47 | +0.0017 | 0.0431 |
| betsson | 47 | +0.0015 | 0.0432 |
| coolbet | 41 | -0.0025 | 0.0435 |
| winamax_fr | 35 | +0.0110 | 0.0437 |
| mybookieag | 28 | +0.0035 | 0.0455 |
| betclic_fr | 30 | +0.0076 | 0.0460 |
| leovegas_se | 56 | -0.0017 | 0.0469 |
| onexbet | 54 | -0.0042 | 0.0471 |
| unibet_se | 56 | -0.0046 | 0.0472 |
| unibet_fr | 29 | +0.0128 | 0.0474 |
| gtbets | 34 | -0.0001 | 0.0480 |
| unibet_nl | 40 | -0.0035 | 0.0482 |
| everygame | 22 | +0.0020 | 0.0483 |
| marathonbet | 37 | -0.0004 | 0.0498 |
| pmu_fr | 37 | +0.0100 | 0.0510 |
| tipico_de | 25 | +0.0176 | 0.0629 |
