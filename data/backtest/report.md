# Historical backtest (close prices)

41971 matches on 1812 match days, seasons 1920, 2021, 2122, 2223, 2324, 2425, 2526, leagues: 17. Data: football-data.co.uk (Joseph Buchdahl). Re-run: `python backtest.py --fetch`.
Price = market average; fair chance = Pinnacle without margin; tickets taxed 15% on winnings; stake 1 per ticket. ROI is profit per unit staked, se its standard error. exp_roi is what Pinnacle's chances predicted.

| strategy | bets | hit | expected hit | avg odds | ROI | se | expected ROI | ROI before tax |
|---|---|---|---|---|---|---|---|---|
| most_likely | 1534 | 37.2% | 36.3% | 2.54 | -14.2% | 2.8% | -16.4% | -5.7% |
| most_likely_2 | 1361 | 37.2% | 36.4% | 2.53 | -14.2% | 3.0% | -16.1% | -5.6% |
| most_likely_no_dc | 1532 | 39.0% | 36.4% | 2.55 | -9.7% | 2.9% | -15.7% | -0.7% |
| most_likely_h2h | 1315 | 36.3% | 35.3% | 2.64 | -13.8% | 3.2% | -16.1% | -5.0% |
| most_likely_totals | 1520 | 36.2% | 35.9% | 2.57 | -15.8% | 2.9% | -16.4% | -7.3% |
| edge_first | 1534 | 32.3% | 32.2% | 2.97 | -14.4% | 3.2% | -14.4% | -5.0% |
| best_single | 1683 | 57.1% | 57.9% | 1.71 | -9.7% | 1.9% | -8.2% | -3.8% |
| value_single | 19471 | 41.9% | 42.3% | 2.64 | -6.9% | 0.8% | -5.5% | +2.1% |
| most_likely_best | 1534 | 37.2% | 36.3% | 2.73 | -8.0% | 3.0% | -10.3% | +1.7% |
| best_single_best | 1683 | 57.2% | 57.9% | 1.79 | -5.9% | 2.0% | -4.6% | +0.7% |
| value_taxed | 248 | 55.6% | 58.9% | 2.03 | -2.7% | 6.0% | +2.0% | +4.7% |
| value_single_4 | 6035 | 40.8% | 42.0% | 2.70 | -7.1% | 1.5% | -4.0% | +2.1% |

ROI after tax by season:

| strategy | 1920 | 2021 | 2122 | 2223 | 2324 | 2425 | 2526 |
|---|---|---|---|---|---|---|---|
| most_likely | -8% | -16% | -20% | -14% | -7% | -15% | -25% |
| most_likely_2 | -7% | -12% | -20% | -13% | -8% | -17% | -26% |
| most_likely_no_dc | -3% | -17% | -15% | -6% | +5% | -16% | -20% |
| most_likely_h2h | -25% | -20% | -15% | -7% | +2% | -15% | -20% |
| most_likely_totals | -10% | -18% | -22% | -20% | -11% | -17% | -7% |
| edge_first | -4% | -20% | -13% | -8% | -16% | -21% | -21% |
| best_single | -10% | -8% | -16% | -9% | -15% | +2% | -16% |
| value_single | -5% | -8% | -7% | -10% | -3% | -6% | -10% |
| most_likely_best | -1% | -9% | -13% | -8% | -0% | -9% | -21% |
| best_single_best | -7% | -3% | -12% | -5% | -11% | +5% | -11% |
| value_taxed | -2% | +20% | -16% | -10% | -19% | +43% | +2% |
| value_single_4 | -10% | -12% | -11% | -4% | -2% | +1% | -8% |

Strategies:

- most_likely: live rule: most likely allowed ticket (code, no AI)
- most_likely_2: same, at most 2 legs
- most_likely_no_dc: same, double chance not allowed
- most_likely_h2h: same, match winner only
- most_likely_totals: same, over/under 2.5 only
- edge_first: allowed ticket with the best chance x odds (edge_first shadow)
- best_single: one single a day: least negative edge at the average price, 1.20-2.00
- value_single: every single where the best price is 2%+ above Pinnacle fair (<= 4.00)
- most_likely_best: the live rule's ticket, each leg at the best price (price shopping)
- best_single_best: best_single at the best price
- value_taxed: singles at the best price with positive expected profit after tax
- value_single_4: same with 4%+ value

## Single legs at the average price (no tax)

| market, odds band | n | hit | ROI | Pinnacle edge |
|---|---|---|---|---|
| dc 1.20-1.40 | 51546 | 71.9% | -8.0% | -8.3% |
| dc 1.40-1.60 | 14621 | 61.0% | -9.3% | -8.5% |
| dc 1.60-1.80 | 8895 | 53.7% | -9.6% | -9.0% |
| dc 1.80-2.00 | 4893 | 48.1% | -9.3% | -9.3% |
| dc 2.00-3.00 | 8387 | 37.2% | -14.3% | -9.4% |
| dc 3.00-6.00 | 2964 | 21.3% | -20.3% | -11.0% |
| h2h 1.20-1.40 | 2819 | 76.6% | -0.3% | -4.1% |
| h2h 1.40-1.60 | 3891 | 66.1% | -0.9% | -4.5% |
| h2h 1.60-1.80 | 5184 | 57.5% | -2.5% | -4.5% |
| h2h 1.80-2.00 | 5660 | 50.5% | -4.2% | -4.5% |
| h2h 2.00-3.00 | 29920 | 38.7% | -4.7% | -5.4% |
| h2h 3.00-6.00 | 58859 | 25.0% | -7.9% | -6.3% |
| totals 1.20-1.40 | 1825 | 70.9% | -5.5% | -5.3% |
| totals 1.40-1.60 | 9963 | 63.6% | -3.9% | -5.0% |
| totals 1.60-1.80 | 17697 | 57.0% | -3.5% | -5.0% |
| totals 1.80-2.00 | 16763 | 50.2% | -5.0% | -5.2% |
| totals 2.00-3.00 | 28818 | 40.7% | -7.9% | -6.1% |
| totals 3.00-6.00 | 1561 | 27.1% | -10.1% | -6.0% |
