# Changes to the bot

Newest first. Each new entry is emailed automatically.

## 2026-10-31: checking prices again just before kick-off

- A new small job checks the odds of every judged bet again in the last 45 minutes before it starts (the "closing price").
- It records whether the price we were offered was better than the final sharp price, and whether the market moved towards our pick.
- Why: beating the closing price is the standard early sign of a real edge. It needs about 50 to 100 bets to judge, while win rate needs hundreds.
- The daily email gets a "Closing line" table once the first prices are recorded. Tickets are picked exactly as before.
- It uses at most 16 Odds API credits a day, well inside the monthly quota.

## 2026-10-31: chances now come from the sharpest bookmaker

- Each bet's chance is now taken from Pinnacle (or Betfair Exchange) when they price it, instead of the average of ordinary bookmakers. Their prices are known to predict results best.
- Every bet now carries a "value" figure: how much the odds pay above that fair chance. The AI is told to prefer value and to skip bets priced more than 6% below fair.
- Why: over 75 ticket picks so far the bot won 71% against 73% the odds implied. It has matched the bookmakers, not beaten them, which loses money after margins and tax.
- Expect much the same kind of tickets, sometimes with different picks where the sharp price disagrees with the rest. The pick log now records both chances, so future reviews can check whether value picks really win more.

## 2026-10-31: paper mode, 2-pick tickets, scorecard and daily self-improvement

- Paper mode is on: tickets are tracked with a virtual 100 MKD and never touch your real bankroll. Ticket #22 still settles as real.
- Tickets now use 2 or 3 picks with total odds 2.50 to 3.50, preferring 2 picks, because every extra pick adds the bookmaker's margin.
- Every bet the AI judges is logged with the market's chance, the AI's verdict and the result; the daily email shows a scorecard of AI verdicts against results.
- Each day's research and AI decision are saved so losses can be traced.
- A Claude review task runs at 10:20 and 21:20 Skopje time, researches better methods, improves the bot, and sends an email like this one after each change.
