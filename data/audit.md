# Standing audits

Built by audit.py from recorded data; nothing here changes a recorded result.

## Does the AI add anything to the sharp chance?

392 settled picks. Brier score (lower is better) of the sharp chance shifted toward the AI's chance by weight w:

| w | Brier |
|---|---|
| 0.00 | 0.23024 |
| 0.10 | 0.23036 |
| 0.20 | 0.23052 |
| 0.35 | 0.23083 |
| 0.50 | 0.23121 |
| 1.00 | 0.23303 |

Live weight 0.20 vs 0: Brier gain -2.9 +- 4.0 (x0.0001; positive means the AI helps). Correlation of (AI chance - sharp chance) with (outcome - sharp chance): -0.021 +- 0.051. No measurable benefit from the AI shift yet.

Won minus sharp chance by verdict (picks, mean): AGREE -3.9 points (96), AVOID +1.4 points (96), RISKY +4.2 points (200)

## Which bookmaker's first price best predicts Pinnacle's closing chance?

38 match sides. RMSE of the first-seen chance against the closing power chance: Pinnacle 0.0455, average of all books 0.0433; paired absolute-error gain of the average over Pinnacle -0.0001 +- 0.0014.

| Bookmaker | Matches | Bias | RMSE |
|---|---|---|---|
| betonlineag | 39 | -0.0045 | 0.0384 |
| betfair_ex_eu | 40 | -0.0047 | 0.0393 |
| coolbet | 35 | -0.0043 | 0.0397 |
| matchbook | 35 | -0.0069 | 0.0405 |
| nordicbet | 33 | +0.0001 | 0.0421 |
| betsson | 33 | -0.0002 | 0.0421 |
| winamax_de | 40 | +0.0015 | 0.0427 |
| codere_it | 39 | -0.0019 | 0.0432 |
| sport888 | 39 | -0.0016 | 0.0436 |
| williamhill | 39 | -0.0015 | 0.0436 |
| gtbets | 26 | -0.0030 | 0.0449 |
| unibet_nl | 31 | -0.0035 | 0.0451 |
| pinnacle | 38 | +0.0057 | 0.0455 |
| onexbet | 39 | -0.0029 | 0.0456 |
| leovegas_se | 41 | -0.0014 | 0.0456 |
| unibet_se | 41 | -0.0047 | 0.0461 |
| winamax_fr | 25 | +0.0065 | 0.0462 |
| everygame | 22 | +0.0020 | 0.0483 |
| betclic_fr | 24 | +0.0064 | 0.0483 |
| pmu_fr | 25 | +0.0089 | 0.0484 |
| unibet_fr | 25 | +0.0097 | 0.0484 |
| mybookieag | 20 | +0.0020 | 0.0486 |
| marathonbet | 25 | +0.0008 | 0.0487 |
| tipico_de | 25 | +0.0176 | 0.0629 |
