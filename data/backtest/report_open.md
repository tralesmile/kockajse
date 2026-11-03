# Historical backtest (open prices)

41971 matches on 1812 match days, seasons 1920, 2021, 2122, 2223, 2324, 2425, 2526, leagues: 17. Data: football-data.co.uk (Joseph Buchdahl). Re-run: `python backtest.py --fetch`.
Price = market average; fair chance = Pinnacle without margin; tickets taxed 15% on winnings; stake 1 per ticket. ROI is profit per unit staked, se its standard error. exp_roi is what Pinnacle's chances predicted.

| strategy | bets | hit | expected hit | avg odds | ROI | se | expected ROI | ROI before tax |
|---|---|---|---|---|---|---|---|---|
| most_likely | 1537 | 34.9% | 35.9% | 2.54 | -19.7% | 2.8% | -17.3% | -11.7% |
| most_likely_2 | 1353 | 34.8% | 36.1% | 2.53 | -19.9% | 3.0% | -16.9% | -11.9% |
| most_likely_no_dc | 1532 | 37.0% | 36.1% | 2.55 | -14.4% | 2.9% | -16.4% | -5.9% |
| most_likely_h2h | 1315 | 36.1% | 35.0% | 2.64 | -13.9% | 3.2% | -16.5% | -5.0% |
| most_likely_totals | 1529 | 35.1% | 35.5% | 2.58 | -18.4% | 2.8% | -17.1% | -10.2% |
| edge_first | 1537 | 32.4% | 31.8% | 2.97 | -14.3% | 3.2% | -15.8% | -4.9% |
| best_single | 1684 | 58.2% | 57.5% | 1.71 | -7.9% | 1.9% | -9.0% | -1.9% |
| value_single | 8104 | 36.7% | 36.6% | 3.02 | -6.4% | 1.4% | -6.6% | +3.6% |
| most_likely_best | 1537 | 34.9% | 35.9% | 2.70 | -14.9% | 3.0% | -12.4% | -6.0% |
| best_single_best | 1684 | 58.1% | 57.4% | 1.77 | -5.1% | 2.0% | -6.1% | +1.4% |
| value_taxed | 39 | 51.3% | 49.2% | 2.67 | +19.6% | 21.2% | +4.4% | +31.7% |
| value_single_4 | 1912 | 33.7% | 34.4% | 3.21 | -7.4% | 3.1% | -5.3% | +3.0% |

ROI after tax by season:

| strategy | 1920 | 2021 | 2122 | 2223 | 2324 | 2425 | 2526 |
|---|---|---|---|---|---|---|---|
| most_likely | -21% | -27% | -31% | -14% | -12% | -12% | -22% |
| most_likely_2 | -21% | -25% | -31% | -15% | -14% | -12% | -23% |
| most_likely_no_dc | -17% | -16% | -23% | -12% | -14% | -4% | -17% |
| most_likely_h2h | -29% | -14% | -12% | -21% | -3% | -5% | -15% |
| most_likely_totals | -24% | -23% | -15% | -13% | -15% | -13% | -35% |
| edge_first | -23% | +3% | -11% | -31% | -19% | -7% | -16% |
| best_single | -9% | -2% | -11% | -17% | -9% | -3% | -2% |
| value_single | -8% | -8% | -5% | -6% | -5% | -9% | +0% |
| most_likely_best | -15% | -21% | -26% | -9% | -7% | -7% | -18% |
| best_single_best | -6% | +2% | -8% | -15% | -7% | +0% | -1% |
| value_taxed |  | +32% | +7% | -5% | -4% | +139% | -29% |
| value_single_4 | -9% | -17% | -5% | +1% | -6% | -10% | +2% |

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
| dc 1.20-1.40 | 51832 | 71.8% | -8.2% | -8.4% |
| dc 1.40-1.60 | 15117 | 61.2% | -9.1% | -8.6% |
| dc 1.60-1.80 | 8911 | 54.2% | -8.8% | -9.1% |
| dc 1.80-2.00 | 4941 | 46.9% | -11.5% | -9.6% |
| dc 2.00-3.00 | 8102 | 37.2% | -14.2% | -9.7% |
| dc 3.00-6.00 | 2839 | 21.4% | -20.5% | -10.5% |
| h2h 1.20-1.40 | 2681 | 75.6% | -1.5% | -4.4% |
| h2h 1.40-1.60 | 3794 | 66.0% | -1.2% | -4.5% |
| h2h 1.60-1.80 | 5265 | 57.7% | -2.1% | -4.5% |
| h2h 1.80-2.00 | 5595 | 50.8% | -3.8% | -4.6% |
| h2h 2.00-3.00 | 30141 | 38.5% | -5.7% | -5.6% |
| h2h 3.00-6.00 | 59181 | 25.2% | -7.6% | -6.4% |
| totals 1.20-1.40 | 1267 | 70.0% | -6.7% | -5.5% |
| totals 1.40-1.60 | 9282 | 63.2% | -4.3% | -5.1% |
| totals 1.60-1.80 | 18580 | 57.3% | -2.8% | -5.1% |
| totals 1.80-2.00 | 17468 | 50.0% | -5.5% | -5.3% |
| totals 2.00-3.00 | 28865 | 40.9% | -8.2% | -6.1% |
| totals 3.00-6.00 | 1005 | 27.2% | -10.4% | -6.1% |
