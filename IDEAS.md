# Ideas backlog

Every idea the review task considers, with its status and result. Statuses: new, building,
live, measuring, dropped. Newest additions at the top of each section.
Scores: impact / confidence / effort, each 1 (low) to 5 (high).

## Live or measuring

- Wide value scan + Kaunitz rule + odds archive (2 Nov morning, bold, 5/3/2). Value shadows
  now search every priced match in the shortlisted leagues at odds up to 4.00 (the ticket list
  stops at 2.00; Kaunitz's bets averaged 2.30). New "kaunitz_single" shadow uses the paper's
  exact rule (best price > 1/(1/average − 0.05), no sharp book needed, outliers up to 25%
  allowed). Every fetched price is archived in `data/odds/<date>.json.gz` so later reviews can
  replay any rule offline. Measuring: value singles per day (was 0 on 2 Nov), Kaunitz singles
  per day, their ROI after ~150 bets, which bookmakers carry them.

- Shadow tickets, `data/shadow.csv` (1 Nov evening). Every day the real ticket, a market-only
  ticket, the AI's own ticket and an "edge first" ticket (best chance x odds within the AI's
  verdicts) are logged and settled side by side, plus the two value strategies below.
  Measuring: profit after tax and win rate against expected, per strategy, on the same days.
  Scores 4/5/3.
- Value betting at the best bookmaker price (Kaunitz, Zhong and Kreiner 2017) (1 Nov evening).
  Each bet now records the best non-exchange price in the feed and its bookmaker
  (`best_odds`, `best_book`, `best_edge` in `picks.csv`). Shadow "value singles" (up to 10 a
  day, sharp price needed, at least +2% value, one per match) and a "value ticket" (2.50 to
  3.50 at best prices, highest expected return). Measuring: is there any positive value in
  the feed at all; ROI and CLV of value singles after about 150 bets; which bookmakers carry
  it (the owner bets at Megawin, which is not in the feed, so a hit means opening an account
  where the value is). Scores 5/3/3.
- Sharp bookmaker (Pinnacle, Betfair, Matchbook) as the fair chance, with an edge figure per
  bet (31 Oct). Measuring: do positive-edge picks win more than negative-edge ones? (1 Nov:
  every one of 35 judged bets was below fair at the average price, mean −5.8%, best −0.4%.)
- Closing line value capture, `closing.yml` (31 Oct). Measuring: average move on AGREE vs
  AVOID picks once about 40 captures exist. (1 Nov: 7 captures, mean price vs close −4.5%,
  4 of 7 moved our way.)
- Code chooses the most likely allowed ticket, AI chance blended at 20% (1 Nov). Measuring:
  how often code overrides the AI; ticket hit rate against win_prob. The "ai_own" shadow now
  settles the AI's own choice next to it.

## New

- Late value scan in the Kaunitz window (timing, 4/3/3): the paper's 9.9% came from bets 5h
  to 1h before kick-off, and soft books are slowest then; our scan is at 08:00, often 12h
  before. The closing job could re-scan events of the day (1 credit per league) and log
  shadow value bets there. Check credit budget first (key 1 had 404 left on 2 Nov).
- Second odds region (data, 3/2/2): adding "uk" (Betfred, Coral, Paddy Power, Sky Bet ...)
  to the value scan widens the best-price search; costs 1 credit per league. Try only if the
  archive shows near-misses (best_edge between 0 and 2%) are common.
- CLV for value shadows (measurement, 4/4/2): closing job captures prices only for judged
  picks; adding value and Kaunitz singles gives an early read of whether they are real value.
- Bookmaker dispersion as a signal (modelling, unconventional, from market microstructure,
  2/2/2): high spread between books on one outcome means stale prices or news; test on the
  odds archive whether high-dispersion favourites win more or less than their chance.
- Gemini search quota guard (AI workflow, 3/4/2): on 2 Nov key 1 hit its daily limit of 20
  search calls at the start of the run and keys 3 and 4 cannot use gemini-2.5-flash; plan the
  research calls to fit one key's 20 and skip re-tries that burn quota on 503s.
- Offline backtest harness over `data/odds/` (experiments, 4/4/3): once a week of archives
  exists, a script that replays any rule against settled scores, so ideas are judged in
  minutes instead of weeks of shadow logging.
- Megawin prices (new data, 4/2/3): the owner's real odds are unknown; every figure assumes
  the European average. Find whether Megawin publishes odds in a readable form (site JSON or
  an aggregator such as OddsPortal listing it) and log them, so value and tax maths use real
  prices. Check terms of use first.
- Singles instead of accumulators (bet types, 4/4/2): every extra leg multiplies the margin
  (Whelan on parlays). Once the value singles have ~100 settled bets, compare their return
  with the ticket strategies and recommend to the owner if singles win clearly (stake rules
  stay the owner's).
- Steam following / latency (timing, unconventional, from syndicate practice, 4/2/3): when
  the closing job sees the Pinnacle chance move by 3+ points since the morning, soft books
  often lag; log a shadow bet at the lagging soft price at that moment.
- Prediction markets as a second sharp reference (data, unconventional, 3/2/3): Polymarket
  and Kalshi list big football and NBA games with free APIs; average them with Pinnacle where
  both exist, and use them where Pinnacle is missing (soccer and handball totals).
- Poisson / Dixon-Coles totals model from free xG (modelling, 3/2/4): the totals with no sharp
  price average −8.6% edge; a model could give an independent fair chance there.
- Drop double chance (selection, 2/3/1): derived price is cut 3% and averages −10.7% edge;
  check its record in the shadows before dropping.
- Self-consistency: run the decision prompt twice and keep only verdicts both runs agree on
  (prompts, 2/2/2).
- Second-pass critic prompt that argues against each pick before the decision (2/2/2).
- Late news check: re-check lineups and injuries an hour before kick-off and flag picks
  whose situation changed (3/2/4).
- Free team ratings (ClubElo for football, basketball ratings) as an independent chance to
  compare with the market (2/3/3).

## Dropped

(none yet. The old "raise the value-bet odds cap" idea was built on 2 Nov as part of the
wide value scan above.)
