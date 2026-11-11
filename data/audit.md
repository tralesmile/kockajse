# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Real-money go / no-go

NO-GO: none of 3 strategies with 20+ scored bets beats the tax; best is pick:AGREE at -10.5% after tax on 41 bets (negative).

## Does the AI add anything to the sharp chance?

431 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23080 |
| 0.10 | 0.23087 |
| 0.20 | 0.23098 |
| 0.35 | 0.23120 |
| 0.50 | 0.23150 |
| 1.00 | 0.23300 |

Live weight 0.20 vs 0: Brier gain -1.8 +- 3.8 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.007 +- 0.048. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE -0.5 points (109), AVOID -0.2 points (101), RISKY +3.8 points (221)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

40 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0447, average of all books 0.0427; paired absolute-error gain of the average over Pinnacle -0.0001 +- 0.0014.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betonlineag | 39 | -0.0045 | 0.0384 |
| betfair_ex_eu | 41 | -0.0056 | 0.0393 |
| coolbet | 35 | -0.0043 | 0.0397 |
| matchbook | 35 | -0.0069 | 0.0405 |
| nordicbet | 35 | -0.0004 | 0.0413 |
| betsson | 35 | -0.0007 | 0.0414 |
| sport888 | 42 | -0.0016 | 0.0425 |
| winamax_de | 40 | +0.0015 | 0.0427 |
| codere_it | 39 | -0.0019 | 0.0432 |
| williamhill | 40 | -0.0021 | 0.0433 |
| gtbets | 28 | -0.0029 | 0.0438 |
| unibet_nl | 34 | -0.0045 | 0.0442 |
| leovegas_se | 44 | -0.0020 | 0.0447 |
| pinnacle | 40 | +0.0056 | 0.0447 |
| unibet_se | 44 | -0.0051 | 0.0452 |
| onexbet | 42 | -0.0040 | 0.0452 |
| winamax_fr | 25 | +0.0065 | 0.0462 |
| everygame | 22 | +0.0020 | 0.0483 |
| betclic_fr | 24 | +0.0064 | 0.0483 |
| pmu_fr | 25 | +0.0089 | 0.0484 |
| unibet_fr | 25 | +0.0097 | 0.0484 |
| mybookieag | 20 | +0.0020 | 0.0486 |
| marathonbet | 25 | +0.0008 | 0.0487 |
| tipico_de | 25 | +0.0176 | 0.0629 |
