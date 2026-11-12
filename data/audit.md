# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 3 strategies with 20+ scored bets beats the tax; best is pick:AGREE at -10.0% after tax on 46 bets (negative).

## If the owner bet this ticket rule for real

Resampling the 34 settled tickets (win rate 29%) at the live stake rule from a bankroll of 400: after 30 tickets the median bankroll is 30, 95% of runs end below the start and 83% fall under the minimum stake (cannot place another ticket). Small sample, so read it as a rough guide to the size of the swings, not a forecast.

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

42 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0437, average of all books 0.0419; paired absolute-error gain of the average over Pinnacle -0.0004 +- 0.0013.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betonlineag | 41 | -0.0042 | 0.0379 |
| matchbook | 37 | -0.0066 | 0.0395 |
| sport888 | 44 | -0.0018 | 0.0419 |
| winamax_de | 42 | +0.0014 | 0.0419 |
| codere_it | 41 | -0.0018 | 0.0424 |
| williamhill | 42 | -0.0023 | 0.0426 |
| betfair_ex_eu | 45 | -0.0052 | 0.0428 |
| pinnacle | 42 | +0.0055 | 0.0437 |
| coolbet | 39 | -0.0041 | 0.0440 |
| nordicbet | 39 | -0.0004 | 0.0447 |
| betsson | 39 | -0.0007 | 0.0447 |
| winamax_fr | 27 | +0.0066 | 0.0448 |
| unibet_fr | 27 | +0.0103 | 0.0472 |
| everygame | 22 | +0.0020 | 0.0483 |
| betclic_fr | 24 | +0.0064 | 0.0483 |
| onexbet | 46 | -0.0045 | 0.0484 |
| mybookieag | 20 | +0.0020 | 0.0486 |
| gtbets | 32 | -0.0023 | 0.0487 |
| leovegas_se | 48 | -0.0022 | 0.0487 |
| unibet_se | 48 | -0.0051 | 0.0490 |
| unibet_nl | 38 | -0.0046 | 0.0493 |
| marathonbet | 29 | -0.0004 | 0.0527 |
| pmu_fr | 29 | +0.0086 | 0.0542 |
| tipico_de | 25 | +0.0176 | 0.0629 |
