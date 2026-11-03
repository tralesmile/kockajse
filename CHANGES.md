# Changes to the bot

Newest first. Each new entry is emailed automatically.

## 2026-11-03: a more accurate way to read the fair chance from prices

- Bookmakers hide more of their margin in the prices of outsiders than of favourites. The bot removed the margin evenly, which slightly understates how often favourites win. A better method (the "power" method) was checked on 80,000 past matches and in a 2026 study of 90,000; it matches real results more closely.
- In the seven-season history, your ticket rule using the new chances would have lost about 2 points less per ticket (-12% instead of -14% after tax). That is promising but not yet proven, so it starts as a side-by-side experiment.
- Two new paper experiments in the email table: the ticket picked with the new chances, and singles that pay even after the 15% tax using the new chances, now also looking at heavy favourites from odds 1.05 (the tax costs least there). In history these singles roughly broke even after tax (+0.2% over 802 bets), the best of anything tested, but they are rare.
- Your daily ticket is chosen exactly as before. No extra Odds API or Gemini use.
- If the new ticket keeps up over the next few weeks, a later review will switch your ticket to the new chances.

## 2026-11-03: seven seasons of history tested, and what it says about the tax

- New: the bot's ticket rules were replayed on 42,000 past European league matches (2019-2026). Picking the most likely ticket at average prices would have lost about 14-16% of every stake after the 15% tax, almost exactly what the market's own chances predict. Nothing in the picking beat that.
- The biggest costs are the ticket format and the tax, not the choice of matches. One single a day lost about half as much (about -8%) because the tax grows with the total odds, and taking each bet at the best bookmaker price instead of the average saved another 4-6 points.
- Three new side-by-side experiments (paper only): your real ticket at the best listed price, one single a day, and "value" singles strong enough to pay the tax too. The email table will show how they compare with your ticket.
- Your daily ticket is chosen as before. The AI gets two short lessons: trust the market's chances unless there is concrete news, and short-priced favourites win slightly more often than their price suggests.
- Recommendations (your decision; nothing changed): consider singles (or tickets with lower total odds; 2 legs instead of 3 at the same total odds did not help), and having two or three bookmaker accounts to take the best price. Also, the price check before kick-off still misses almost every match because GitHub runs it only every few hours; a free cron-job.org timer with a GitHub token would fix it.
- The history check reruns monthly by itself, with no Odds API or Gemini use.

## 2026-11-02: closing prices are now caught for most bets

- The check of prices just before kick-off (the best early sign of a real edge) had caught only 11 of 116 bets: GitHub ran just 8 of about 70 planned checks over two days.
- Each check that does run now records every bet starting in the next 3 hours, and again within the last hour before kick-off, waiting a few minutes when a start is close.
- The "value" bets are now checked against the closing price too, so within a couple of weeks we can see whether they really beat the market.
- New experiment: shortly before kick-off, when the sharp price is most accurate, the bot logs any bookmaker still paying at least 2% above it ("late value"). Paper only.
- Your ticket is chosen exactly as before. Up to 20 Odds API credits a day for these checks (was 16), well inside the quota.
- Worth a look: the repository is private, so GitHub's free plan allows 2,000 Actions minutes a month; you can see usage under Settings, Billing.

## 2026-11-02: a wider hunt for prices above fair, and every price is now kept

- On today's bets no bookmaker paid more than the fair chance on anything, so the "value" bets added yesterday found nothing. They only looked at odds up to 2.00; the published method they copy found most of its value around 2.30.
- The value experiment now looks at every match in the leagues the bot priced, at odds up to 4.00. A second version follows the 2017 paper's rule exactly, which also works where no sharp bookmaker prices the bet (many football totals).
- Every price the bot downloads is now saved each day, so future reviews can test new ideas on past prices straight away instead of waiting weeks.
- Your daily paper ticket is chosen exactly as before. No extra Odds API or Gemini use.
- Both paper tickets so far lost on one leg each (the Young Boys loss on 1 November was a 76% favourite with sound research behind it, just bad luck).

## 2026-11-01: strategies compared side by side, and the best price is now checked

- Every day the bot now also records five other ways it could have bet, on the same matches, and settles them like paper tickets: the most likely ticket without the AI, the AI's own ticket, the ticket with the best expected return, and "value" bets at the best price any bookmaker offers. A new table in the email compares them.
- Why: on today's 35 bets every price was below the fair chance (by 5.8% on average). With all choices below fair, no way of picking among them can win in the long run; only a price above fair can. Until now the bot only looked at average prices.
- The value bets follow a published method (Kaunitz and others, 2017) that made 6 to 10% over thousands of bets by betting only where one bookmaker paid more than the fair price.
- Your real paper ticket is chosen exactly as before. The value bets may be at bookmakers other than Megawin; if they keep winning, the email will show which ones, and opening an account there would be your decision.
- No extra Odds API or Gemini use.

## 2026-11-01: the most likely ticket is now chosen by code

- The AI still researches every match and says AGREE, RISKY or AVOID for each bet, but the final ticket is now worked out in code: every allowed combination is checked and the one most likely to win is taken.
- Why: on both recent days the AI's own ticket was not the safest one its rules allowed (28% vs 36% chance on 31 Oct, 33% vs 37% on 1 Nov). That is about one winning ticket in five left on the table.
- The chance used is mostly the sharp bookmaker's (80%) with a little of the AI's estimate (20%). So far the AI's own estimates were less accurate than the market's, and research on AI forecasting finds the same.
- Same limits as before: no AVOID picks, at most one RISKY pick, total odds 2.50 to 3.50. If the AI picks the best ticket itself, its choice is kept.
- Expect slightly more 2-pick tickets. Each day's research file records the AI's choice next to the code's, so the next reviews can check this helped.

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
