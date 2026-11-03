# Ideas backlog

Every idea the review task considers, with its status and result. Statuses: new, building,
live, measuring, dropped. Newest additions at the top of each section.
Scores: impact / confidence / effort, each 1 (low) to 5 (high).

## Live or measuring

- Power-method de-margining, shadows "power_value" and "power_ticket" (3 Nov evening,
  modelling, 4/4/2). Every candidate now also carries a power-method chance (`power_prob`,
  `sharp_power`). Evidence: on 80,832 Pinnacle closing 1X2 prices (2012-2026) a logistic
  refit of the power chance has slope 1.013 (calibrated) vs 1.047 for proportional (which
  understates favourites); Goto et al. 2026 (arXiv 2604.17194, 90,014 matches) find power
  best or near best and proportional worst for all five books. Backtest 2019-2026: the live
  ticket rule with power chances realised -11.8% vs -14.2% at closing prices and -17.7% vs
  -19.7% at opening prices (paired difference +2.5 ± 2.1 and +2.0 ± 2.1 points; same ticket
  on 69% of days). Tax-proof singles at the best price with the power chance (from odds 1.05,
  where the tax costs least): 802 bets, +0.2% ± 2.5 realised after tax, hit 70.6% vs 70.9%
  expected (proportional rule: 248 bets, -2.7% ± 6.0); at opening prices 168 bets, -3.4% ±
  4.9. Replay of the 3 Nov odds archive: 0 bets (mostly even NCAAB lines). Measuring: count
  per day, ROI and CLV of power_value; power_ticket vs actual/market on the same days. If
  power_ticket keeps up with the market shadow for ~3 weeks, make power the ticket's chance.

- Historical backtest on football-data.co.uk (3 Nov morning, bold, experiments, 5/4/3).
  `backtest.py` replays the bot's rules (same build_ticket, same config, 15% tax) on 41,971
  matches in 17 European leagues, 2019-20 to 2025-26, average price vs Pinnacle fair chance.
  Report in `data/backtest/report.md` (closing prices) and `report_open.md`; monthly workflow
  refreshes it. Results (closing, Pinnacle-expected ROI after tax, which has far less noise
  than the realised one): live rule -16.4% (realised -14.2% over 1,534 days); at most 2 legs
  -16.1%; no double chance -15.7%; edge_first -14.4%; same ticket at the best price -10.3%;
  one single a day -8.2%; one single at the best price -4.6%; tax-proof value singles +2.0%
  expected but -2.7% realised (248 bets, se 6%). Nothing reachable beats the tax reliably.
  Without the 10% outlier cap on the best price, value rules look like +16% after tax:
  that is stale prices, not edge. Use the backtest before building any new selection idea.
- Price shopping shadow "actual_best" (3 Nov, selection, 4/4/1): the real ticket's legs at the
  best listed price. Measuring: average total-odds gain per day; backtest says about +6
  points of return (0.19 more total odds per ticket).
- One single a day, shadow "single" (3 Nov, bet types, 4/4/1): the allowed pick with the best
  chance x odds. The tax grows with total odds (about 15% x (1 - chance) of the stake at fair
  prices: 9.6% for a 36% ticket, 3.8% for a 75% single). Measuring: return vs "actual".
  If it keeps losing about half as much, recommend singles to the owner (his decision).
- Tax-proof value singles, shadow "taxed_value" (3 Nov, modelling, 3/2/1): best capped price
  with positive expected profit after the 15% tax (needs +4% value at 1.40, +10% at 2.70).
  Replaces the idea that 2% value is enough: after tax, the 2% value singles were -6.9% in
  the backtest. Measuring: count per day, ROI, CLV.

- Reliable closing capture + late value + CLV for value shadows (2 Nov evening, 5/4/2).
  Found that GitHub ran only 8 of ~70 planned closing jobs from 31 Oct to 2 Nov, so 11 of 116
  picks had a closing price and none of 2 Nov's. Each run now captures every bet starting in
  the next 3 hours as a fallback and again within 60 minutes of the start (waiting up to 15
  min when a start is close); value and Kaunitz singles are captured too (`source` column in
  `closing.csv`). The same fetch (all league matches in the window, same credit cost) logs
  shadow "late_value" singles at the best price vs the near-kick-off Pinnacle price.
  Measuring: share of picks with a near capture (target 80%+), CLV of value singles vs
  picks, late_value bets per day and their ROI, closing credits per day (cap 20).

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

- Gemini decision circuit breaker (AI workflow, 2/4/1): on 3 Nov the decision call failed 29
  times (503 "high demand" and timeouts) before gemini-3.6-flash on key 3 answered. After
  two 503s on a model, move to the next model instead of trying every key; add
  gemini-2.5-flash-lite (no search needed) as the last plain fallback.
- Shortlist league cap (selection, 2/3/1): on 3 Nov 36 of 41 logged picks were NCAAB
  opening-week mismatches (spreads of 26-30 points) and the ticket took a Copa del Rey tie
  with a fifth-tier side; cap any one league at about half the shortlist so the AI's research
  covers markets it can inform.
- Late power value (timing, 3/3/1): the backtest finds 5 times more tax-proof power value at
  closing prices (802) than at opening prices (168); the late_value scan near kick-off could
  use the power chance and the tax test too.
- Paired comparison in backtest.py (experiments, 3/4/1): report the per-day paired
  difference and its standard error between any two strategies (done by hand on 3 Nov;
  far tighter than comparing two ROIs).
- Taxed Kelly ranking (modelling, unconventional, from portfolio theory, 2/2/1): rank value
  singles by the Kelly fraction after tax instead of raw value, so short-priced, high-chance
  value comes first; informs a staking recommendation only.

- League margin table (leagues, 3/3/2): the backtest can list the average-price margin per
  league and market; restrict the ticket to the cheapest ones (big leagues are usually
  2-3 points cheaper than second divisions).
- Self-chaining closing job (timing, 4/3/2): since the 2 Nov evening change GitHub started
  only 2 closing runs (02:37 and 06:40 UTC) and none was near a kick-off, so 0 captures. A
  run could dispatch the next one (workflow_dispatch from GITHUB_TOKEN does start runs) at
  the right moment, but waiting costs Actions minutes on a private repository. The external
  scheduler (below) is cheaper; recommend again.
- Portfolio staking (unconventional, from quantitative finance, 3/2/2): several small
  uncorrelated singles instead of one ticket give the same expected loss per unit with much
  lower variance, and far less tax. Only as a recommendation; stake rules are the owner's.
- AI forecasting tournament on past matches (unconventional, prompts, 2/1/3): score Gemini on
  backtest matches. Rejected for now: the model may know the results (leakage), so scores
  would be inflated.

- External scheduler for exact capture times (timing, 4/4/1 for the owner): GitHub's own
  schedule is unreliable (see above). A free cron service (cron-job.org) calling the
  workflow_dispatch API with a fine-grained token (Actions: write on this repo only) would
  wake the closing job on time. Needs the owner to create the token; suggest in CHANGES.md
  if near-capture coverage stays under 80%.
- Actions minutes guard (reliability, 4/4/1): the repository is private, so GitHub's free
  plan gives 2,000 minutes a month; the daily run takes up to 40 and each closing run at
  least 1. Check the billing page usage; if close to the limit, thin the closing schedule.
- Slow-book value (market microstructure, unconventional, 3/2/2): OddsPapi (Sep 2026)
  measured 1xBet following Pinnacle moves in ~6-12 min but Bet365 in ~47-67 min (follows
  only 59-73% of moves). Value at slow books is more likely real lag than an error; split
  value-single results by bookmaker speed once ~100 exist.
- Sequential testing (experiments, unconventional, from clinical trials, 3/4/2): a SPRT or
  Bayesian A/B on shadow strategies' CLV, so a strategy can be declared better or dropped
  as soon as the evidence is enough, instead of a fixed ~150 bets.
- Gemini 3.8 flash with search on keys 3 and 4 (AI workflow, 3/3/1): keys 3/4 answer that
  2.5-flash is "no longer available to new users, use gemini-3.8-flash". If 3.8-flash
  allows Google Search grounding on the free tier, the research quota doubles. Needs a
  diagnose run, which the review may not start; ask the owner or test in a preview.
- AI weight 0 shadow (modelling, 2/3/1): Brier on 68 picks is market 0.2278 vs AI 0.2358;
  a "market + 0% AI" ticket is the "market" shadow already, so read that comparison first.

- Second odds region (data, 3/2/2): adding "uk" (Betfred, Coral, Paddy Power, Sky Bet ...)
  to the value scan widens the best-price search; costs 1 credit per league. Try only if the
  archive shows near-misses (best_edge between 0 and 2%) are common.
- Bookmaker dispersion as a signal (modelling, unconventional, from market microstructure,
  2/2/2): high spread between books on one outcome means stale prices or news; test on the
  odds archive whether high-dispersion favourites win more or less than their chance.
- Gemini search quota guard (AI workflow, 3/4/2): on 2 Nov key 1 hit its daily limit of 20
  search calls at the start of the run and keys 3 and 4 cannot use gemini-2.5-flash; plan the
  research calls to fit one key's 20 and skip re-tries that burn quota on 503s.
- Offline backtest harness over `data/odds/` (experiments, 4/4/3): once a week of archives
  exists, a script that replays any rule against settled scores. Partly done on 3 Nov with
  football-data history (`backtest.py`); the archive replay is still useful for basketball,
  tennis and our real bookmaker list.
- Megawin prices (new data, 4/2/3): the owner's real odds are unknown; every figure assumes
  the European average. Find whether Megawin publishes odds in a readable form (site JSON or
  an aggregator such as OddsPortal listing it) and log them, so value and tax maths use real
  prices. Check terms of use first.
- Singles instead of accumulators (bet types, 4/4/2): every extra leg multiplies the margin
  (Whelan on parlays). Backtest 3 Nov supports it (-8% vs -16% after tax); now live as the
  "single" shadow (above). Once the value singles have ~100 settled bets, compare their return
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
  check its record in the shadows before dropping. Backtest (3 Nov): double chance legs cost
  8-9% at the bot's derived price vs 4-5% for match winners at the same odds, but removing
  them improves the ticket's expected return only 0.7 points (-15.7% vs -16.4%); realised
  +4.5 points is mostly luck. Low priority.
- Self-consistency: run the decision prompt twice and keep only verdicts both runs agree on
  (prompts, 2/2/2).
- Second-pass critic prompt that argues against each pick before the decision (2/2/2).
- Late news check: re-check lineups and injuries an hour before kick-off and flag picks
  whose situation changed (3/2/4).
- Free team ratings (ClubElo for football, basketball ratings) as an independent chance to
  compare with the market (2/3/3).

## Dropped

- Extremizing / logistic recalibration of Pinnacle chances (unconventional, from forecasting
  tournaments, tested 3 Nov evening): fitted on 2012-2019, tested on 2019-2026; on top of the
  power method the slope is 1.013 and the test log loss does not improve (0.61739 both). The
  power method already removes the favourite-longshot bias; no extra tilt is justified.
- (The old "raise the value-bet odds cap" idea was built on 2 Nov as part of the wide value
  scan.)
