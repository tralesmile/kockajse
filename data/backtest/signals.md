# Signal lab: can anything pick winning favourites better than the sharp price?

11646 European league matches, seasons 1920-2526, where Pinnacle's pre-match favourite had a 55%+ chance. Built by signal_lab.py.

## Walk-forward: each signal added on top of Pinnacle's chance

Fitted on earlier seasons only, tested on 2021/22 to 2025/26. Gain is log loss saved per bet (x0.0001); positive and above 2 standard errors would be real.

| Signals | Test bets | Gain x0.0001 | se | z |
|---|---|---|---|---|
| recalibration only | 8275 | -1.0 | 1.6 | -0.6 |
| agree | 8275 | -1.6 | 2.0 | -0.8 |
| best | 8275 | -1.5 | 3.2 | -0.5 |
| elo | 8275 | -2.5 | 1.7 | -1.5 |
| form | 8275 | -1.2 | 1.7 | -0.7 |
| shots | 8275 | +1.7 | 3.1 | +0.6 |
| rest | 8275 | -1.1 | 1.6 | -0.7 |
| tight | 8275 | -1.8 | 1.9 | -0.9 |
| ah | 8275 | -1.2 | 1.9 | -0.6 |
| low | 8275 | -1.7 | 1.9 | -0.9 |
| home | 8275 | +0.1 | 2.0 | +0.0 |
| all together | 8275 | -3.0 | 4.8 | -0.6 |

## Does the all-signal model pick better favourites? (out of sample)

| Group | Bets | Won | Priced | Won minus priced (points) | Avg best odds | Return after tax |
|---|---|---|---|---|---|---|
| model likes most (top third) | 2758 | 65.4% | 63.6% | +1.9 ± 0.9 | 1.58 | -3.1% |
| middle third | 2758 | 68.9% | 67.8% | +1.1 ± 0.9 | 1.51 | -3.2% |
| model likes least (bottom third) | 2759 | 68.2% | 67.0% | +1.2 ± 0.9 | 1.53 | -2.2% |

## The single rules, every season (no fitting)

| Group | Bets | Won | Priced | Won minus priced (points) | Avg best odds | Return after tax |
|---|---|---|---|---|---|---|
| all favourites, chance 55%+ | 11646 | 67.0% | 66.2% | +0.8 ± 0.4 | 1.54 | -3.6% |
| agree: sharp >= soft (fav_agree rule), chance 55%+ | 6518 | 66.0% | 65.4% | +0.6 ± 0.6 | 1.57 | -3.5% |
| sharp below soft, chance 55%+ | 5128 | 68.2% | 67.2% | +1.0 ± 0.6 | 1.51 | -3.7% |
| sharp below soft by 0.05+ logits, chance 55%+ | 496 | 78.8% | 76.8% | +2.0 ± 1.8 | 1.31 | -1.7% |
| favourite rested 3 days or less, chance 55%+ | 1439 | 67.4% | 66.2% | +1.2 ± 1.2 | 1.54 | -3.0% |
| favourite at home, chance 55%+ | 8769 | 66.9% | 66.5% | +0.4 ± 0.5 | 1.54 | -4.1% |
| favourite away, chance 55%+ | 2877 | 67.2% | 65.2% | +2.0 ± 0.9 | 1.56 | -2.0% |
| all favourites, chance 70%+ | 3509 | 78.5% | 77.8% | +0.7 ± 0.7 | 1.30 | -1.9% |
| agree: sharp >= soft (fav_agree rule), chance 70%+ | 1758 | 78.7% | 78.1% | +0.6 ± 1.0 | 1.30 | -1.4% |
| sharp below soft, chance 70%+ | 1751 | 78.4% | 77.6% | +0.8 ± 1.0 | 1.30 | -2.3% |
| sharp below soft by 0.05+ logits, chance 70%+ | 367 | 84.2% | 81.3% | +2.9 ± 2.0 | 1.23 | +0.3% |
| favourite rested 3 days or less, chance 70%+ | 423 | 79.2% | 78.0% | +1.2 ± 2.0 | 1.30 | -1.3% |
| favourite at home, chance 70%+ | 2742 | 78.9% | 78.4% | +0.5 ± 0.8 | 1.29 | -2.0% |
| favourite away, chance 70%+ | 767 | 77.3% | 76.0% | +1.3 ± 1.5 | 1.32 | -1.6% |

## The only lever on hit rate: how short the favourite is

| Group | Bets | Won | Priced | Won minus priced (points) | Avg best odds | Return after tax |
|---|---|---|---|---|---|---|
| chance 55%-60% | 3776 | 58.7% | 57.4% | +1.3 ± 0.8 | 1.75 | -4.0% |
| chance 60%-70% | 4361 | 64.8% | 64.4% | +0.3 ± 0.7 | 1.56 | -4.6% |
| chance 70%-80% | 2324 | 75.0% | 74.3% | +0.7 ± 0.9 | 1.36 | -2.4% |
| chance 80%-100% | 1185 | 85.5% | 84.8% | +0.7 ± 1.0 | 1.19 | -0.8% |

## Can the signals foresee Pinnacle's closing move? (closing line value)

| Signal | Matches | Correlation with logit move to the close |
|---|---|---|
| agree | 11643 | -0.083 |
| best | 11643 | -0.030 |
| elo | 11643 | -0.006 |
| form | 11570 | +0.023 |
| shots | 11570 | +0.130 |
| rest | 11614 | -0.000 |
| tight | 11642 | +0.002 |
| ah | 11557 | +0.051 |
| low | 11559 | -0.088 |
| home | 11643 | -0.029 |

## Price-adjusted thirds, with replication on untouched seasons

Top third = the signal is better than usual for a favourite at that price. "Move" is how far Pinnacle's chance went by the close. "Seasons" counts the seasons where the top third beat the bottom third (move / won minus priced).

| Signal, period, third | Bets | Won | Priced | Won minus priced (points) | Move (points) | Return after tax | Seasons |
|---|---|---|---|---|---|---|---|
| shots, 1920-2526, top | 3858 | 68.0% | 66.3% | +1.7 ± 0.7 | +0.39 | -2.2% | 7/7 and 7/7 |
| shots, 1920-2526, bottom | 3858 | 65.3% | 66.4% | -1.1 ± 0.7 | -0.58 | -6.2% |  |
| shots, replication 1314-1819, top | 2363 | 66.7% | 66.3% | +0.4 ± 1.0 | +0.34 | -3.4% | 6/6 and 3/6 |
| shots, replication 1314-1819, bottom | 2705 | 68.6% | 67.3% | +1.3 ± 0.9 | -0.37 | -1.9% |  |
| form, 1920-2526, top | 3858 | 67.5% | 66.3% | +1.2 ± 0.7 | -0.09 | -3.0% | 4/7 and 5/7 |
| form, 1920-2526, bottom | 3858 | 66.6% | 65.9% | +0.7 ± 0.7 | -0.11 | -3.7% |  |
| form, replication 1314-1819, top | 3310 | 66.5% | 66.5% | +0.0 ± 0.8 | -0.05 | -4.3% | 4/6 and 1/6 |
| form, replication 1314-1819, bottom | 3662 | 67.9% | 66.3% | +1.5 ± 0.8 | -0.11 | -1.7% |  |
| elo, 1920-2526, top | 3882 | 67.6% | 66.6% | +1.0 ± 0.7 | -0.23 | -3.2% | 2/7 and 4/7 |
| elo, 1920-2526, bottom | 3882 | 67.9% | 66.2% | +1.7 ± 0.7 | +0.02 | -2.1% |  |
| elo, replication 1314-1819, top | 2893 | 65.8% | 66.3% | -0.4 ± 0.9 | +0.05 | -5.2% | 5/6 and 2/6 |
| elo, replication 1314-1819, bottom | 4038 | 67.1% | 66.9% | +0.3 ± 0.7 | -0.14 | -3.6% |  |
| ah, 1920-2526, top | 3853 | 71.2% | 69.6% | +1.6 ± 0.7 | +0.28 | -2.2% | 7/7 and 4/7 |
| ah, 1920-2526, bottom | 3854 | 67.2% | 66.5% | +0.6 ± 0.7 | -0.46 | -3.4% |  |
