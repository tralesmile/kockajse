# Ideas backlog

Every idea the review task considers, with its status and result. Statuses: new, building,
live, measuring, dropped. Newest additions at the top of each section.
Scores: impact / confidence / effort, each 1 (low) to 5 (high).

## Live or measuring

- Row-by-row data merge driver and retried save (infrastructure, 5/5/2, built 9 Nov
  morning). Found: on 9 Nov the daily job made ticket 32 and sent its email, then
  `git pull --rebase` stopped on a conflict in data/actions_usage.json (the closing
  watcher had pushed a minute earlier), so nothing was saved; a second run at 07:36 picked
  ticket 32 again (2.90 then 2.93, two emails), spent ~30 more Odds API credits and the rest
  of key 1's search quota. The pacer then read 78 credits as the day's core use and cut all
  closing captures and the sweep to 0. Now `merge_data.py` is registered as a git merge
  driver for data/*.csv, data/*.json, data/scoreboard.md and the odds archive in both
  workflows: CSV rows matched by identity columns (changed rows from the replayed side,
  new rows from both, none dropped or duplicated), JSON merged per key, reports from the
  replayed side; the daily save retries 5 times and aborts a stuck rebase; the watcher's
  pulls abort a failed rebase instead of leaving the checkout stuck. Verified with a real
  two-clone rebase in tests/test_merge.py (in a rebase %B is the replayed commit). A shared
  concurrency group was rejected: GitHub keeps one pending run per group, so a watcher link
  would cancel a waiting daily run. Measuring: daily save failures (target 0), no day with
  two ticket emails.
- Re-run-aware credit pacer (infrastructure, 4/4/1, built 9 Nov morning): a second daily
  measurement on the same day stores what the re-run spent as `rerun_spent`, left out of
  the core estimate; config `odds_core_skip_days` leaves out known one-off days (9 Nov,
  whose first measurement was lost); `allowance` recomputes the core from the history, so
  extras return today (17 closing + 5 sweep instead of 0 + 0).
- Kick-off sweep fix (bug, built 9 Nov): `write_sweep_plan` unpacked two values from
  `closing_todo`, which returns three, so the plan failed on 8 and 9 Nov whenever a pick
  was pending ("Sweep plan failed: too many values to unpack") and late_sweep never ran.
  The 7 Nov test only covered `plan_sweep`; tests/test_sweep.py now runs the writer with a
  pending pick. Measuring as before (bets per day, xROI vs late_power).
- Honest ticket explanation (email, 2/5/1, built 9 Nov): when the rules replace the AI's
  combination, the email says so, gives both expected returns after tax and labels the
  AI's reasoning as its own suggestion (9 Nov explained a 2.60 ticket with Dallas while
  the real one was 2.93 without it).

- Odds API credit pacer and scores-call filter (infrastructure, 5/4/2, built 7 Nov
  evening). Found: key 1's balance in last_run.json fell 252 -> 194 -> 109 on 5-7 Nov (58
  and 85 credits a day) before the kick-off sweep's 6 a day began; four keys give 2,000 a
  month, 66 a day, so at ~85-90 a day the last key would run dry around 25 Nov and the bot
  would have no odds or feed scores until the reset (like the 6 Nov GitHub minutes stop).
  The Odds API docs say /sports "does not count against the usage quota" and still return
  x-requests-remaining, so the daily run now probes every key for free (`odds_budget.py`,
  `data/odds_credits.json`: balances, 14-day history, core use per day = drop between
  mornings minus what closing + sweep spent, median of 7), and the optional extras get
  D = (pool - 40 - (days left - 1) x core) / days left a day, shared 20:6 between closing
  captures and the sweep (full caps when D >= 26, or when no measurement under 36 h
  exists). Scores calls (2 credits each) now skip leagues whose pending bets have not
  started or are older than the feed's 3-day window (those go to the Gemini fallback).
  The email shows credits on all keys and the date they would run out at full use.
  Measuring: real burn per day from the history, core estimate, days the extras are cut,
  and that no key hits 0 before 1 Dec. Check on 1 Dec that all keys reset on the 1st
  (otherwise set `odds_cycle_day`).

- Kick-off sweep, shadow "late_sweep" (timing/experiments, 4/3/2, built 7 Nov morning). The
  only rule near break-even after tax is the late tax-proof single at the best price
  (backtest at closing prices: 802 bets, +0.2% realised, +1.5% expected; odds 1.05-1.30
  +5.1% +- 2.2), but live "late_power" logged 2 bets in 3 days: the watcher only fetches
  leagues that already hold a logged pick (~12 matches a day). Now the daily run plans up
  to 6 kick-off slots in other leagues (per league, matches within 60 minutes of the
  earliest; busiest slots first, one per league, at least 2 matches, skipped when the
  watcher already fetches that league nearby) in `data/sweep_plan.json`, and the watcher
  fetches each slot's match-winner prices 15 minutes before its first start (1 credit) and
  logs the late_power rule there as "late_sweep". The chain stays alive for planned slots.
  Separate credit count in `closing_budget.json` ("sweep"), skipped when the last Odds API
  key has under 60 credits. At the backtest's 1.9% hit rate, ~30 swept matches a day
  should add about 0.5 bets a day (3-5x late_power). Measuring: bets per day, closing xROI
  and realised return vs late_power (same rule, so they should agree), extra score credits.
  Config `late_sweep_credits_per_day` 0 switches it off.

- GitHub Actions minutes guard (infrastructure, 5/5/2, built 6 Nov evening). Found that
  GitHub stopped every job from 15:57 UTC on 6 Nov ("recent account payments have failed
  or your spending limit needs to be increased"): the private repository's ~2,000 free
  minutes (USD 12 a cycle) were used by 6 Nov, 1,994 of 2,243 by the closing watcher
  (1,199 on 5 Nov alone), and the 7 Nov daily ticket cannot run. The 4 Nov check that
  billing was 0 ms read the per-run "billable" field, which does not measure this. Late
  daily backup crons (14:19-15:24 UTC) each restarted the watcher too. Now
  `actions_budget.py` counts this cycle's minutes from the runs list
  (`data/actions_usage.json`), keeps 45 minutes a day for the ticket run, and gives the
  watcher only an even share of the rest (private: about 9 minutes a day in a fresh month,
  so no 36-minute links; public: no limit); the daily job starts the watcher only after a
  run that made the ticket; closing backup crons hourly; the email shows minutes used and
  warns at 75%. Ticket legs are looked up by the score fallback up to 40 days late, so an
  outage does not void them. Measuring: minutes per day, that the cycle never runs out,
  share of picks still captured near kick-off in private mode. Recommended to the owner:
  make the repository public (standard runners free), or the watcher must stay thin.

- Tax-aware ticket objective, live rule (selection/modelling, bold, 5/4/2, built 6 Nov
  morning). The real ticket no longer maximises the chance of winning; it maximises the
  expected return after the 15% tax, chance x (1 + 0.85 x (total odds - 1)) - 1, using
  power-method chances with the same 20% AI shift and the same verdict rules (no AVOID, at
  most one RISKY). Backtest 2019-2026, 1,534 days: expected -12.3% vs -14.5% (power
  measure) at closing prices and -13.3% vs -15.3% at opening prices; realised -10.0% vs
  -14.2% (close) and -12.9% vs -19.7% (open); it takes slightly higher total odds (2.72 vs
  2.54) and legs priced nearer fair. Supported by Whelan's "Parlay Puzzle" (expected
  return (1-m)^N, at most two legs at 1/3-1/2 chance). Side by side: "likely_ticket" (the
  old rule, same verdicts), "tax_market" (no AI, twin of "market"), "tax_best" (the new
  rule at the best listed prices: backtest -3.0% expected at close, -8.2% realised; vs
  -10.3% for the old rule at the best price). Fallback without AI uses the same objective.
  `ticket_objective` "most_likely" restores the old rule. Measuring: paired closing-price
  xROI actual vs likely_ticket in the scoreboard (expect +2 points; ~25 days for se 1).

- Closing-price scoreboard with an always-valid sequential test (experiments, bold,
  unconventional from online A/B testing and clinical trials, 5/4/2, built 5 Nov evening).
  `scoreboard.py` scores every shadow bet, and every logged pick by verdict, the moment
  its closing price is captured: expected return after the 15% tax if the margin-free
  closing chance (power method where recorded) is true. Per strategy: mean, se, P(beats
  the tax), mSPRT always-valid p (Johari, Pekelis, Walsh 2015; normal mixture tau 0.05,
  burn-in 10 bets: 2.5% false alarms in null simulations at alpha 5%, 17% without the
  burn-in), verdict after 20 bets, and a same-day paired difference against the real
  ticket. Written to `data/scoreboard.md` each daily run and shown in the email. Legs of
  the market, power, edge_first, single, ai_own and actual_best tickets are now captured
  near kick-off too (3 of 8 market legs and 2 of 5 power legs were not in the pick log),
  and captures record `close_power`. Fixed: late_power logged the proportional chance as
  its fair chance; it now logs the power chance it used. First reading (5 Nov, few
  captures): value singles CLV +6.6% before tax but -3.1% ± 2.2 after tax (6 bets);
  picks at average prices -11.5% to -12.5% after tax whatever the verdict. Measuring:
  first verdicts (~2-3 weeks), whether xROI tracks realised returns live; this is the
  input the Thompson-sampling chooser needs.

- Second results source with two-answer agreement (data/measurement, bold, 5/4/2, built
  5 Nov morning). The Odds API scores feed left the ATP Paris Masters (2 and 4 Nov) and the
  Copa del Rey (3 Nov) unsettled: 10 picks and 14 shadow legs, and 2 of the 3 legs of
  ticket 27, were still pending on 5 Nov. After 3 days such legs count as void, so ticket
  27 would have been booked as a win at 1.73 whatever the tennis did (survivorship bias in
  our own ledger). Now, before settling, every bet that started 6+ hours ago without a
  feed score is checked with Google-Search Gemini; two separate calls (second with the
  list reversed) must give the same final score, and the score must be plausible for the
  sport (tennis: sets 2-0/2-1/3-x), or it stays pending. Borrowed from blockchain oracles
  (UMA, Chainlink), which only accept a reported result when independent reporters agree.
  Football is the score after regular time, tennis is h2h only. Audit trail in
  `data/fallback_scores.csv`. Cost: 0-2 search calls a day. Measuring: share of overdue
  events settled (target 90%+), disagreements between the two answers, and any case
  where the feed later shows a different score (should be 0).

- Self-continuing closing watcher (timing/infrastructure, bold, 5/4/2, built 4 Nov evening).
  GitHub ran only 15 of about 160 planned closing runs from 31 Oct to 4 Nov, and on 4 Nov
  the 06:17-09:53 UTC daily crons ran at 14:52-17:36 (community threads #210625 and
  #210925 report the same: 4+ hour delays, missing slots, no staff answer). The GitHub docs
  say workflow_dispatch made with the job's own token always creates a run, so each
  closing run that still has bets to capture now starts its successor before ending (runs
  of up to `closing_run_minutes` = 36), and the daily run starts the chain after logging
  picks. Inside the chain every bet is captured 15-60 minutes before its start, with no
  3-hour fallback capture (saves credits). Stops when nothing is left, the next capture is
  over 14 hours away, the 20 closing credits are used, or after 60 links. Actions usage
  API shows billable 0 ms for these runs (IMPROVING.md: run time is free). Measuring: share
  of picks and value singles with a capture within 60 minutes (was about 30%, target 90%+),
  late_power bets per day (needs near-kick-off feeds, so it was nearly blind), credits per
  day, chain breaks. This replaces the "self-chaining closing job" and "external scheduler"
  ideas; the external scheduler stays a fallback if the chain breaks.

- Late tax-proof power singles, shadow "late_power", and Gemini model rotation (both built
  4 Nov morning):
  - "late_power" (timing, 4/3/1): the closing job, minutes before kick-off, logs every
    single whose best (outlier-capped) price pays after the 15% tax with the power-method
    Pinnacle chance, odds 1.05-4.00, no double chance, one per match. Backtest: the same
    rule found 802 bets at closing prices (+0.2% ± 2.5 realised, +1.5% expected) but only
    168 at opening prices (-3.4% ± 4.9); at closing prices odds 1.05-1.30 gave 238 bets,
    +5.1% ± 2.2 (expected +1.1%). The morning "power_value" shadow is its opening-time
    twin, so the pair measures the timing effect live. Measuring: bets per day, ROI after
    ~150 bets, and whether it beats power_value.
  - Gemini rotation: on 3 and 4 Nov the decision call failed 29 and 33 times (503 "high
    demand", timeouts) because every key of a busy model was tried 4 times. Now at most
    2 attempts per key and 3 busy failures per model per round, then the next model; two
    rounds (three for search, which has one model); a "per day" 429 drops that key at once.
    Measuring: failed calls per run in `last_run.json` (target under 8).

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

- Idempotent daily ticket (infrastructure, unconventional, from payment-API idempotency
  keys and database write-ahead logs, 4/4/2): save today's ticket (state + picks) with a
  push before the email is sent, so any failure after that resends the same ticket
  instead of picking a new one; a re-run with an existing ticket for today only resends.
  The merge driver removes today's cause; build this if a save ever fails again.
- Ticket-leg adverse selection, update 9 Nov: ticket legs won 9 of 20 vs 12.8 expected
  (z about -1.7), but their price-vs-close is -4.5% (8 near captures) against -6.5% for
  other picks (107): the market does not move against our ticket legs, so the gap looks
  like bad luck so far. Keep measuring; check again at ~40 ticket-leg captures.
- FA Cup giant-killing check (leagues, 2/2/1): 2 of the last 6 lost ticket legs were FA
  Cup ties against non-league sides (Boreham Wood 0:3 Wigan at 1.71, Stafford 3:3 Grimsby
  at 1.36). Both were priced by the market; test on football-data cup history only if
  cups keep showing up on tickets.
- NBA back-to-back tag (new data, 2/2/2): today's research mentions back-to-backs for
  three of the six NBA favourites; record it as a field so its effect vs the closing
  price can be measured, rather than trusted in the AI's verdict.

- Value-of-information credit auction (experiments, unconventional, from Bayesian
  experimental design / VOI, 3/2/3): when the pacer cuts the extras, give the credits to
  the experiment whose scoreboard posterior is closest to the break-even line per credit
  (late_power/late_sweep now) instead of a fixed 20:6 split.
- Late sweep ticket (selection/timing, 3/3/2): build the tax-aware ticket from the
  sweep's near-kick-off feed (best capped prices, power chances, no AI, no extra credits)
  and settle it as a shadow; the cheapest live test of a ticket placed late.
- Leaner morning markets (data/credits, 2/3/1): basketball spreads and totals cost 2 of
  each league's 3 credits but won 50.0% vs 50.1% market (62 spreads) and the taxed
  objective rarely needs near-even legs; dropping them would free ~4-6 credits a day.
- Later daily run (timing, 3/3/1): the backtest says the same ticket rule at closing
  prices loses 2-6 points less than at opening prices; moving the run from 08:00 to about
  11:00 local on weekends (most football starts 13:30-21:00) would price nearer the close.
  Needs the owner's agreement on the email time.
- Pre-mortem prompt (prompts, unconventional, from Klein's pre-mortem, 1/2/1): ask the AI
  to assume the ticket lost and name the likeliest cause per leg. Low: the AI's verdicts
  have shown no signal in 266 settled picks, so more AI text is unlikely to help.
- Prediction markets as a second sharp price (re-checked 7 Nov): the only measured study
  found (Edge Lab, Jun 2026, ~1,800 resolved Polymarket sports markets) gives no Brier or
  Pinnacle comparison, almost all markets were priced 75%+, and coverage is mostly NBA,
  NFL and UFC. Still no evidence it beats Pinnacle; stays low.

- Adverse-selection monitor for ticket legs (measurement, unconventional, from market
  microstructure "winner's curse", 3/3/1): ticket legs won 6 of 15 vs 9.5 expected (z about
  -1.9) while all picks won 2.1 points above the market; the taxed objective picks legs
  whose average price is nearest fair, which could be where soft books know something.
  Compare ticket legs' closing move with other picks' once ~40 ticket legs are captured.
- Bet-time advice per leg (timing, unconventional, from execution algorithms /
  implementation shortfall, 3/2/2): from captured drift of our legs by sport and market,
  tell the owner in the email which legs to bet now and which to bet near kick-off. Needs
  ~100 ticket-leg captures (the watcher now gets them).
- Random sweep slot (experiments, unconventional, from survey sampling / mark-recapture,
  2/3/1): make one of the sweep slots a random league instead of the busiest, so the share
  of matches with a tax-proof price can be estimated without bias across the whole feed.
- NFL and NHL in the ticket pool (leagues, 3/2/1): big US markets have low margins at EU
  books and Pinnacle prices; more near-fair legs widen the taxed objective's choice on thin
  weekdays (6 Nov: 27 priced events). Costs 2-3 credits a league in the morning.
- LLM exact-score harness on a Dixon-Coles base (modelling, 1/2/4): arXiv 2608.05030 (Aug
  2026, 150 EPL matches) raised exact-score top-1 from 10.0% to 14.7% but compared with no
  market price, and its 1X2 log loss (0.988) is no better than bookmaker level. Not worth
  building for a market-anchored bot.

- DONE 6 Nov 22:15 UTC by the owner: make the repository public (infrastructure, 5/5/1): standard GitHub
  runners are free in public repositories, which ends the minutes limit at once and lets
  the full closing watcher run. Secrets stay hidden; picks, research and the paper record
  become readable. Recommended in CHANGES.md on 6 Nov evening.
- External timer for closing captures (timing, 4/4/2): cron-job.org (free) calling
  workflow_dispatch with a fine-grained token at the exact capture times, one-pass runs of
  ~1 minute each, instead of a runner napping between bets. Cuts a private-mode day of
  captures to ~10-15 minutes. Needs the owner to create the token and the cron-job.org jobs.
- Cloudflare Worker as the closing watcher (infrastructure, unconventional, from
  serverless edge computing, 4/3/4): free cron triggers and 100k requests a day; the Worker
  fetches the Odds API at capture times and commits closing rows through the GitHub
  contents API, so GitHub Actions only runs the daily ticket. Bigger build, owner setup.
- Capture triage (timing, unconventional, from hospital triage, 3/3/2): with few minutes,
  capture only bets that move a decision (ticket legs, tax-proof and value singles) and
  group starts within 30 minutes into one pass; skip AVOID picks' captures.
- Hedged Gemini requests (AI workflow, unconventional, from Dean and Barroso "The Tail at
  Scale", 3/3/2): on 6 Nov 24 research calls failed with 503s; send the same research call
  to the second key after ~20 seconds and take the first answer, within the 20-a-day
  search quota per key (costs quota on days both answer).
- Batched research (AI workflow, 3/3/2): two or three matches per search call so the 12
  shortlisted matches fit in about 6 search calls and survive 503 storms.
- Outage-aware voiding (measurement, 2/4/1): count how many picks and shadow bets were
  voided only because no run happened, and report them apart from real voids.

- Tax break-even shortlist (selection, 2/3/1): give the AI only picks whose average price
  is within ~5% of the sharp fair price, since the taxed objective rarely uses the rest;
  frees research quota for matches that can matter.
- Two-account recommendation with numbers (bet types, 4/4/1): tax_best is the first
  strategy near break-even in the backtest (-3% expected at close). If its live closing
  xROI holds over ~3 weeks, recommend the owner opens one or two accounts at the books
  that most often carry the best price (from the best_book column).
- NHL and other heavy-favourite pools (leagues, 2/2/1): more legs priced near fair widen
  the taxed optimizer's choice; check The Odds API Pinnacle coverage first.

- Tax break-even curve in the email (selection/bet types, 3/4/1): value singles beat the
  close by +6.6% before tax but lose about 3% after it, because at odds O the tax costs
  about 15% x (O - 1) x chance. Show the owner the CLV needed at each odds band
  (about +7% at 2.0, +3% at 1.3) and restrict value shadows to bets above it.
- Thompson-sampling chooser (selection, unconventional, raised to 3/3/2): the scoreboard's
  "chance it beats the tax" is the posterior weight a bandit needs; once 3+ strategies
  have 20+ scored bets, a shadow "bandit" ticket can follow the best posterior.
- Totals drift test in European cups (timing, 2/2/2): on 5 Nov all three Over 3.5 value
  singles in UEFA games closed 6-14% shorter, and logged Overs drifted +1.1 ± 0.7 points
  (9 captures). Domestic leagues show no such drift (see Dropped); re-test on cup games
  once the archive has ~100 captured totals.
- Closing-price weighting of the AI (modelling, 2/3/2): replace the fixed ai_weight 0.2
  by how much the AI's verdict groups out-close each other in the scoreboard (AGREE vs
  AVOID xROI difference), which needs a fraction of the bets the Brier comparison does.

- ESPN scoreboard as a third results source (data, 3/2/2): free JSON
  (site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard?dates=YYYYMMDD,
  sportsapis.dev, Nov 2026); blocked from the review sandbox and the tennis layout is
  unverified, so add it once fallback_scores.csv shows how often Gemini cannot answer.
- Void-bias audit (measurement, unconventional, from survivorship bias in fund returns,
  3/4/1): count how many settled tickets and shadows had a void leg and recompute their
  result without it; report the gap in the review so voids never flatter the record.
- Tennis retirement rule (bet types, 2/3/1): bookmakers differ (void vs. result stands
  after one set). The fallback leaves retirements pending, so they void; check Megawin's
  rule and settle accordingly.
- Thompson-sampling strategy chooser (selection, unconventional, from multi-armed bandits,
  3/2/2): once shadows have ~60 settled days each, let the real ticket follow the shadow
  with the best posterior taxed return, with a floor of exploration. Premature now (most
  shadows have 0-2 settled tickets).
- Tennis fatigue signal (new data, 2/2/3): minutes on court in the last 3 days from the
  research step as a feature; Paris Masters picks were 2 of the 3 legs of ticket 27.
- Settlement-aware shortlist (selection, 2/4/1): skip leagues whose scores the feed and
  the fallback both fail to settle; superseded unless the fallback misses often.

- Late ticket email (timing, unconventional, 4/3/3, raised from 3/2/3): the watcher now
  sees every logged bet 15-60 minutes before its start, so it can re-price the morning
  ticket and send a short "bet now" email with the late prices (or swap a leg whose price
  fell). Backtest: the same rule at closing prices loses 2-6 points less. Build once the
  chain has run cleanly for a few days and late_power vs power_value shows the gap live.
- Late ticket shadow "late_ticket" (selection/timing, 4/3/2): run build_ticket on the
  watcher's near-kick-off feed (best capped prices, power chances) for the ticket legs'
  leagues and settle it beside "actual"; the cheapest live test of betting later.
- Slow-book move follower (market microstructure, unconventional, 3/2/2): both value
  singles captured on 4 Nov opened at onexbet 1.92 and 1.97 and closed at 1.71 and 1.81
  (CLV +6.3% and +5.8%), i.e. the outlier book's price was the one that moved. If this
  holds over ~30 captures, the value scan is finding real lag, not errors; split CLV by
  book and by minutes since the sharp price last moved.
- Exchange spread as a confidence signal (market microstructure, unconventional, 2/2/2):
  The Odds API's betfair_ex_eu gives back and lay prices; a wide back-lay spread means a
  thin market where the sharp fair chance is less reliable. Down-weight or skip value
  bets there.
- Ice hockey (leagues, 2/2/1): NHL h2h with Pinnacle prices; adds evening-US favourites
  at 1.20-1.50 where the tax costs least, and diversifies away from NCAAB mismatches.
- Actions usage check (reliability, measured 4 Nov evening): WRONG. The per-run usage API
  reported billable 0 ms, but the minutes were counted: the account ran out on 6 Nov. See
  the minutes guard above.

- Fallback score source (data, 3/3/2): Copa del Rey picks of 3 Nov (incl. the ticket's
  Anaitasuna v Alavés leg) and a 2 Nov tennis pick were still unsettled on 4 Nov; The Odds
  API scores feed seems not to cover every league. After 3 days such legs count as void,
  which flatters a lost ticket into a smaller one. ESPN's free scoreboard JSON covers cups,
  NCAAB and tennis, but is blocked from the review sandbox, so it needs a preview to test.
- Verdict coherence check (prompts, 2/3/1): in 4 of 42 complementary pairs (same line,
  both sides) the AI said AGREE to both, e.g. Kansas St -10.5 and South Dakota St +11.5 on
  3 Nov. Downgrade the weaker side to RISKY in code, and tell the prompt.
- Heavy-favourite best-price singles (bet types, 3/3/1): at closing best prices all h2h
  favourites 1.05-1.20 return -0.2% ± 1.5 after tax (average price: -3.9%); the tax-proof
  subset 1.05-1.30 +5.1% ± 2.2. A "favourite at best price" shadow would measure it live;
  late_power covers the tax-proof part first.
- Late ticket email (timing, unconventional, 3/2/3): the backtest says the same rule at
  closing prices loses 2-6 points less than at opening prices. A second, short email an
  hour before the first leg with re-priced legs (or a late ticket) would let the owner bet
  later. Wait for late_power vs power_value to show the timing effect live first.
- Online AI weight (modelling, unconventional, from forecast aggregation, 2/3/2): set
  ai_weight by the running Brier of AI vs market (now 0.2359 vs 0.2330 on 149 picks),
  shrinking to 0 while the AI is worse. Read the market-vs-actual shadow first.

- Shortlist league cap (selection, 2/3/1): on 3 Nov 36 of 41 logged picks were NCAAB
  opening-week mismatches (spreads of 26-30 points) and the ticket took a Copa del Rey tie
  with a fifth-tier side; cap any one league at about half the shortlist so the AI's research
  covers markets it can inform.
- Paired comparison in backtest.py (experiments, 3/4/1): report the per-day paired
  difference and its standard error between any two strategies (done by hand on 3 Nov;
  far tighter than comparing two ROIs).
- Taxed Kelly ranking (modelling, unconventional, from portfolio theory, 2/2/1): rank value
  singles by the Kelly fraction after tax instead of raw value, so short-priced, high-chance
  value comes first; informs a staking recommendation only.

- League margin table (leagues, 3/3/2): the backtest can list the average-price margin per
  league and market; restrict the ticket to the cheapest ones (big leagues are usually
  2-3 points cheaper than second divisions).
- Portfolio staking (unconventional, from quantitative finance, 3/2/2): several small
  uncorrelated singles instead of one ticket give the same expected loss per unit with much
  lower variance, and far less tax. Only as a recommendation; stake rules are the owner's.
- AI forecasting tournament on past matches (unconventional, prompts, 2/1/3): score Gemini on
  backtest matches. Rejected for now: the model may know the results (leakage), so scores
  would be inflated.

- Slow-book value (market microstructure, unconventional, 3/2/2): OddsPapi (Sep 2026)
  measured 1xBet following Pinnacle moves in ~6-12 min but Bet365 in ~47-67 min (follows
  only 59-73% of moves). Value at slow books is more likely real lag than an error; split
  value-single results by bookmaker speed once ~100 exist.
- Sequential testing (experiments, unconventional, from clinical trials, 3/4/2): a SPRT or
  Bayesian A/B on shadow strategies' CLV, so a strategy can be declared better or dropped
  as soon as the evidence is enough, instead of a fixed ~150 bets.
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

- One concurrency group for the daily run and the closing watcher (infrastructure,
  checked 9 Nov): GitHub keeps only one pending run per concurrency group and cancels the
  older pending one, so the next 36-minute watcher link would cancel a waiting daily run.
  The merge driver solves the push race without queuing.

- Soccer Asian handicap or draw-no-bet legs in place of the costly derived double chance
  (bet types, checked 7 Nov): The Odds API's market list says spreads and totals are
  "mainly available for US sports", and draw_no_bet is an additional market for US sports
  and selected books, fetched one event at a time. No affordable feed for it; the bot also
  could not check that Megawin prices them.

- Opening "bookmaker crowd" blend (modelling, unconventional, from forecast aggregation,
  tested 6 Nov on 38,279 football-data matches 2019-2026): a log-linear blend of the
  market-average and Pinnacle opening power chances, weight fitted on 2019-2023, picks
  weight 0.1 on the average; test log loss 0.99001 vs 0.98998 for Pinnacle alone, KL to the
  Pinnacle close 0.00313 vs 0.00314. Value singles chosen with the blend: +2.7% vs +2.5%
  closing xROI before tax, tax-proof ones -0.4% vs -0.3%. Pinnacle opening is already the
  best morning reference.
- Data-quality gate for ticket legs (prompts, tested 6 Nov on 217 settled picks joined to
  the research notes): GOOD +0.9 points won vs market (145), THIN -3.5 (19), NONE 0.0 (7).
  No signal yet; ticket 28's Penn +30.5 leg had THIN data but the sample says nothing.
- Gemini 3.8 flash with search on keys 3 and 4: third-party pricing pages (usagebox, Oct
  2026) and the Google forum say Grounding with Google Search is not available on the
  free tier for Gemini 3 models (paid only, 5,000 prompts a month). Keys 3/4 cannot add
  search quota without paying.

- Morning Over 2.5 drift (timing, unconventional, from momentum in finance, tested 5 Nov
  evening on 38,245 football-data matches 2019-2026, Pinnacle opening vs closing): the
  Over chance drifts -0.14 ± 0.02 points on average (league means -0.55 to +0.21), and
  Over/Under at the opening best price (capped) closes -2.2% / -1.5% before tax. No
  exploitable drift in domestic leagues.

- Arbitrage across bookmakers (unconventional, from arbitrage trading, checked 4 Nov by
  arithmetic): the 15% tax on the winning side's profit turns odds o into 1 + 0.85(o - 1),
  so a two-way 2.10/2.10 "sure bet" pays 1.935 either way and loses 3.3%; a tax-proof arb
  needs about 2.18/2.18 (an 8% gross arb), which the 10% outlier cap all but rules out, and
  it needs several accounts. Not worth a shadow.

- Extremizing / logistic recalibration of Pinnacle chances (unconventional, from forecasting
  tournaments, tested 3 Nov evening): fitted on 2012-2019, tested on 2019-2026; on top of the
  power method the slope is 1.013 and the test log loss does not improve (0.61739 both). The
  power method already removes the favourite-longshot bias; no extra tilt is justified.
- (The old "raise the value-bet odds cap" idea was built on 2 Nov as part of the wide value
  scan.)
