# Learning log

Each review adds an entry here: what was analysed, what was found, and what changed.

## 2026-10-31: starting point

- 21 real tickets settled: 7 won, 14 lost (33%), −274.11 MKD after tax.
- 72 picks on those tickets: 50 won (69%), close to what the odds implied.
- By bet type (ticket picks only, small samples): to win 25/32, over 6/7, double chance
  17/26, under 2/7.
- Changes made by hand: 2-pick tickets allowed (total odds 2.50 to 3.50, picks up to 2.00),
  paper mode on (virtual 100 MKD per ticket), every judged pick now logged to
  `data/picks.csv` with the AI's verdict, and the research saved to `data/research/`.
- Reviews from here on follow `IMPROVING.md`.

## 2026-10-31 (morning review): sharp fair price

Measured (22 settled tickets in the ledger, legs parsed from the ticket text; `picks.csv` has
no settled rows yet):
- Legs: 53 of 75 won (71%) against 73% implied by the odds (margin included), so the picks
  have matched the market, not beaten it. Tickets 8 won of 22; with 3 to 4 legs and a 15% tax
  on winnings, a market-level hit rate loses money.
- By bet type: to win 26/33 (79%, implied 74%), over 7/8 (implied 64%), double chance 18/27
  (67%, implied 75%), under 2/7 (29%, implied 61%). By odds: under 1.35 25/35 (71%, implied
  79%), 1.35 to 1.55 18/21, 1.55 and up 10/19 (53%, implied 61%). Samples are far too small
  for lessons; double chance and unders are the ones to watch.
- No loss review: none of the lost tickets has saved research yet (research starts today).

Researched: sharp bookmakers as the fair price. The Odds API's eu region (already used) carries
Pinnacle, Betfair Exchange and Matchbook. Pinnacle's margin-free price is the industry
benchmark for the true chance and for closing line value; the bot was using the average of
soft books, whose margins and slow lines it was copying.

Changed: each bet's chance now comes from Pinnacle (then Betfair Exchange, then Matchbook)
when it prices the bet, otherwise the old soft average; a sharp price more than 10 points from
the average is ignored as stale. Each bet gets an "edge" (fair chance x average odds - 1),
shown to the AI with an instruction to prefer value and skip picks over 6% below fair.
`picks.csv` gains consensus_chance, sharp_chance, sharp_book and edge columns.

To measure next: share of candidates with a sharp price; win rate of picks with edge >= 0
against edge < 0; whether sharp_chance is better calibrated than consensus_chance (Brier
score) once about 100 picks are settled. Next topic idea: closing line value (record the
Pinnacle price again near kick-off with a small extra workflow; about 5 Odds API requests a
day fits the quota).

Preview run (same morning): worked end to end. Ticket Levante v Atlético Under 3.5 @1.61 +
Leicester v Stevenage Over 2.5 @1.64, both with a sharp price from Matchbook, edge −5.2% and
−5.5%. Because "odds" is the average soft price, a typical edge sits near −5% (the soft
margin), so the "more than 6% below fair" rule is close to the normal range: next review should
check the edge spread across all candidates in `picks.csv` and loosen or tighten it. Gemini key
1 hit its 20 search requests in the preview, as expected after the daily run.

## 2026-10-31 (evening review): closing line value

Measured: nothing new is settled. `picks.csv` has 33 judged picks from today, all pending, and
all logged before the sharp-price change, so they have no sharp_chance or edge yet; the
edge-spread check asked for by the morning review must wait for tomorrow's rows. Ticket 23
(Man City to win @1.67 + Hornets v 76ers Under 215.5 @1.88) is still open. No lost ticket
has saved research yet, so there was no loss review. Odds API key 1 had 181 credits left
after the preview.

Researched: closing line value (CLV). The standard test is whether the price taken beats the
margin-free sharp closing price (Pinnacle as benchmark); it separates skill from luck in
roughly 50 to 100 bets, where win rate needs many hundreds. The Odds API charges markets x
regions per request and accepts an eventIds filter, so one request per league covers every
due pick in it.

Changed: new workflow `closing.yml` runs every 30 minutes (10:11 to 03:41 UTC). It looks at
pending picks in `picks.csv` that start within 45 minutes and, only then, fetches their
league's odds once (ticket legs first, at most 16 credits a day) and writes
`data/closing.csv`: closing average odds, consensus and sharp chance, `clv` (logged odds x
closing fair chance − 1) and `move` (fair chance at close − at pick, sharp to sharp when
both exist). A totals or handicap line that moved away is recorded with blank closing
fields. The daily email gains a "Closing line" table. Tonight's Hornets v 76ers and Bucks v
Cavaliers picks should be the first captures.

To measure next: average `move` and share of picks moved our way, for AGREE vs AVOID and for
ticket legs, once about 40 captures exist (a positive move on AGREE picks is the first real
sign the AI research adds value); how often lines are missing at the close; whether 45
minutes is close enough or GitHub delays cause misses (check minutes_before). Then the
edge spread. Next research topic idea: free injury/lineup sources or a second-pass prompt
that argues against each pick.

## 2026-11-01 (morning review): code picks the most likely ticket, AI chance blended lightly

Measured (`picks.csv`, 33 settled judged picks from 31 Oct, 35 pending from 1 Nov):
- By verdict: AGREE 6/11 (55%, market 54%), RISKY 10/16 (63%, market 56%), AVOID 4/6 (67%,
  market 57%). No sign yet that the verdicts separate winners from losers.
- Brier score: market 0.2235, AI adjusted chance 0.2365 (worse). Blends: 30% AI 0.2270, 50% AI
  0.2295. The AI raises AGREE picks by about 2 points and lowers the rest by 2 to 4.
- Edge spread on 1 Nov (35 candidates): mean −5.8%, range −12.2% to −0.4%; 86% have a sharp
  price. Without a sharp price (soccer/handball totals) the edge averages −8.6%; double chance
  −10.7% (includes the 3% cut). So the "more than 6% below fair" rule removes about half the
  list and is mostly measuring the soft margin, not value.
- Ticket choice: the AI's ticket was not the most likely one its own rules allowed. 31 Oct:
  AI ticket (Man City + Under 215.5) had 28.5% market chance; the best allowed (Cavaliers to
  win + PSV v Willem II Under 4.5) had 35.6%. 1 Nov: AI 3-pick ticket 32.8% against 37.0% for a
  2-pick (Santander v Real Madrid Under 4.5 + Lakers). About 20% fewer winning tickets than
  available, caused by the prompt's "AGREE only" preference plus LLM arithmetic.
- Loss review, ticket 23: Man City to win @1.67 lost (market 57%). Research was good (City
  rested starters midweek, Brighton injuries); a 43% outcome, not foreseeable. The AI added 2
  points for public news that was already priced in.

Researched: combining LLM forecasts with market prices. "Forecasting Future Language" (arXiv
2602.21229, Kalshi mention markets, 856 questions): an LLM told to start from the market price
and adjust it scored worse than the market (Brier 0.147 vs 0.140); only a blend of 70% market
+ 30% LLM beat the market, and by a hair (0.139). Same pattern as our own 33 picks.

Changed: after the AI's verdicts, code now searches every allowed ticket (no AVOID, at most one
RISKY, 1 to 3 picks, total odds in range) and takes the one with the highest product of
"blend" = 80% market chance + 20% AI chance (`ai_weight` 0.2 in config; lower than the paper's
0.3 because our own data favours the market). The AI's own ticket is kept when it is within 0.5
points of the best. RISKY is no longer second-class in code (still max one per ticket). The
decide prompt now matches this. `data/research/<date>.json` gains "ai_ticket" with the AI's
choice, its chance and the code's best, so reviews can see how often code overrode it.

To measure next: how often code overrides the AI; the hit rate of tickets against their
win_prob; AGREE vs RISKY win rate against market once about 100 picks are settled (if RISKY
keeps matching AGREE, verdicts may only be useful as an AVOID filter); first CLV `move` values
for ticket legs. Next research topic idea: a second-pass critic prompt, or free injury/lineup
feeds for late news after the morning research.

## 2026-11-01 (evening review): shadow tickets and value bets at the best price

Measured: nothing new settled since the morning (33 settled picks, ticket 24 still open, its
legs play tonight). On the 35 bets judged today every one was below fair at the average
price: mean edge −5.8%, best −0.4%; 30 of 35 had a sharp price. A two-leg ticket therefore
starts near −11% expected return, and the 15% tax on winnings takes roughly another 5 to 8
points. Closing line: 7 captures so far, mean price vs close −4.5% (that is the soft margin
again), chance moved our way on 4 of 7, mean move about 0. No lost ticket today to review.

Ideas considered (scored in IDEAS.md): shadow tickets; value betting at the best price in the
feed; Megawin odds; singles vs accumulators; steam following after sharp moves; prediction
markets as a second sharp price; Poisson/xG totals model; wider odds for value bets; dropping
double chance; self-consistency and critic prompts; late news; Elo ratings.

Researched: Kaunitz, Zhong and Kreiner, "Beating the bookies with their own numbers" (arXiv
1710.02824): bet when the best price across bookmakers beats the consensus fair chance by a
margin; 56,435 historical bets returned +3.5% at closing odds and +9.9% on earlier odds; 672
paper and real bets returned +6.2% before the bookmakers limited the accounts. OddsPapi's
practitioner write-up uses Pinnacle de-vigged (proportional) as fair, EV = price x fair − 1,
a 1% threshold, and treats prices 5%+ above consensus as suspect. The Odds API eu region has
27 books (onexbet, marathonbet, betsson, unibet, williamhill, pinnacle, betfair_ex_eu,
matchbook, ...). Karl Whelan and others on parlays: each leg compounds the margin.

Concluded: the AI and the ticket rules choose among bets that are all priced below fair, so
no selection rule can make the current ticket profitable; the only measurable route to an
edge is a price above fair. We had never looked at the best price, only the average.

Changed: each candidate now carries the best non-exchange price in the feed (outliers more
than 10% above the average ignored), its bookmaker and its value against the sharp fair
chance; `picks.csv` gains best_odds, best_book, best_edge. New `data/shadow.csv` logs and
settles each day: actual, market, ai_own, edge_first, value_ticket and up to 10
value_single bets, all at the virtual paper stake and taxed like real tickets. Shadows only
use leagues on the AI's shortlist, so settling them costs no extra Odds API credits. The
email gains a strategy comparison table. The real ticket is chosen exactly as before.

To measure next: how many value singles appear per day and from which bookmakers (if almost
none, raise the odds cap or add a wider value candidate list); their ROI and their CLV once
~100 are settled (CLV capture does not yet cover shadows; adding it is a cheap next step);
ai_own vs actual (does the code override help?); edge_first vs actual.

## 2026-11-02 (morning review): wide value scan, the Kaunitz rule as published, odds archive

Measured (`picks.csv`, 68 settled judged picks, 48 pending from 2 Nov):
- By verdict: AGREE 9/16 (56%, market 58%), RISKY 26/42 (62%, market 55%), AVOID 8/10 (80%,
  market 61%). Still no sign the verdicts sort winners from losers; AVOID won most.
- By market: h2h 14/19 (74% vs 65%), totals 21/35 (60% vs 54%), spreads 5/10 (50% vs 50%),
  double chance 3/4. Brier: market 0.2278, AI 0.2358 (AI still worse).
- Paper tickets: 23 and 24 both lost (24: Young Boys @1.24 lost, a 76% favourite). Research for
  YB v Zurich was thorough and correct (6-0 at home, 5 straight H2H wins); not foreseeable.
- Value: of the 16 bets judged on 2 Nov with a sharp price, the best price beat fair on none
  (best −0.5%, mean −3.3%). So the value shadows logged zero bets today. Cause: the value
  search only saw the ticket candidates, which stop at odds 2.00, and short favourites carry
  the bookmaker margin most evenly, leaving little room for one book to be above fair.
- Shadows: 2 Nov logged actual, market, ai_own and edge_first only; nothing settled yet.
- Reliability: Gemini key 1 hit its 20/day search limit on the first research call (likely
  used by an earlier run), keys 3 and 4 cannot use gemini-2.5-flash, many 503s; the decision
  call took 9 tries. The ticket still went out.

Researched: Kaunitz, Zhong and Kreiner (arXiv 1710.02824) in detail: consensus = 1/mean
price, bet when max price > 1/(consensus − 0.05); bets averaged odds 2.30 (SD 0.99), 60% home,
38% away, 2% draws; 5h–1h before kick-off. SharpAPI EV docs: Pinnacle proportional devig,
EV under 2% historically negative after line movement, 2–4% about break-even, 4%+ the real
tier. Data Golf on favourite-longshot bias: longer prices carry more margin even at Pinnacle,
so value at long prices needs a bigger threshold, not a looser one.

Ideas considered (scored in IDEAS.md): wide value scan; Kaunitz rule as published; odds
archive for offline backtests; late value scan in the 5h–1h window; second odds region;
CLV for value shadows; bookmaker dispersion signal; Gemini quota guard; backtest harness.

Changed: value shadows now use every priced match in the shortlisted leagues at odds up to
4.00 (no extra credits; settled from the same score feeds). New "kaunitz_single" shadow uses
the paper's rule exactly (needs no sharp price, so it also covers soccer totals; outliers
allowed to 25% above the average, the strict best price still caps at 10%). Every price the
run fetches is saved to `data/odds/<date>.json.gz` (a few hundred KB) so reviews can backtest
new rules offline. The real ticket is unchanged, so no preview run was started (also saves
the scarce Gemini search quota).

To measure next: value and Kaunitz singles per day and their sports/books; settle results
over ~2 weeks; build the offline backtest script once 5+ archive days exist; check archive
size per day.

## 2026-11-02 (evening review): the closing job was missing most kick-offs

Measured: nothing new settled since the morning (68 settled judged picks; ticket 25 open,
both legs play tonight), so no new lost ticket pick to review. Odds bands of settled picks:
1.00-1.35 6/7 (market 76%), 1.35-1.60 9/12 (64%), 1.60-1.80 12/20 (56%), 1.80-2.10 16/29
(50%); all slightly above the market, well inside noise at this sample size.
Closing line: only 11 captures in total, none for the 48 picks of 2 Nov. Cause: GitHub ran
only 8 of the ~70 scheduled closing jobs from 31 Oct 23:39 to 2 Nov 20:16 (gaps of 3 to 11
hours), and each run only looked 45 minutes ahead. So the earliest-edge metric (CLV) was
starving. The repository is private (2,000 free Actions minutes a month on GitHub's free
plan), so a job that stays awake all day is not an option.

Researched: GitHub docs on GITHUB_TOKEN (workflow_dispatch always creates runs; other
events do not); Runhooks on scheduled-run delays and silent drops, with external
schedulers calling workflow_dispatch as the fix; OddsPapi "Soft book lag" (Sep 2026, 28
fixtures, 1,234 Pinnacle moves): 1xBet follows Pinnacle moves in a median 6-12 minutes,
Bet365 in 47-67 minutes and only 59-73% of the time; Pinnacle reprices 60-73 times in the
last 24 hours; their advice is to grade against the closing line.

Ideas considered (scored in IDEAS.md): reliable closing capture with an early fallback;
late value scan at the near-kick-off sharp price; CLV for value shadows; an external
scheduler; an Actions-minutes guard; slow-book value; sequential testing of strategies;
Gemini 3.8 flash with search on keys 3/4; an AI-weight-0 comparison.

Changed: every closing run now captures each bet starting in the next 3 hours once (a
fallback) and again within 60 minutes of the start, waiting up to 15 minutes in the run when
a start is close (40 minutes per run at most). Value and Kaunitz singles from the shadow
log are captured too (`source` column). Each league request now covers all its matches in
the window (same credit cost), and those prices log new shadow "late_value" singles: best
soft price at least 2% above the Pinnacle fair chance shortly before kick-off. Closing budget
16 -> 20 credits a day. The email's closing table shows each bet once (latest capture) and
adds value- and Kaunitz-single rows. The real ticket is unchanged, so no preview run.

To measure next: share of picks with a capture within 60 minutes (and within 180); CLV of
value singles vs ordinary picks; late_value count per day and which books; closing credits
used per day; whether the 3-hour fallback CLV agrees in sign with the near capture.

## 2026-11-03 (morning review): seven seasons of history say the tax, not the picks, decides

Measured (`picks.csv`, 115 settled judged picks): AGREE 12/20 (60%, market 60%), RISKY
40/68 (59%, 57%), AVOID 18/27 (67%, 60%); h2h 71% vs 67%, totals 58% vs 54%, spreads 47% vs
50%, dc 68% vs 66%. Edge at the average price: 124 picks, mean −6.6%, none positive; best
price positive on none of 29 with a sharp price. Paper tickets: 23, 24, 25 all lost on one
leg. Ticket 25's lost leg (Osasuna or draw @1.64, 56%, RISKY) had research marked THIN with
"no current data" on every point: a coin flip the research could not inform, not
foreseeable. Shadows settled: market ticket won 2 Nov (+128), actual and edge_first lost.
Effect of the 2 Nov evening closing change: GitHub started only 2 closing runs since (02:37
and 06:40 UTC), none near a kick-off, so still 11 captures in total. The fix needs an
external scheduler (owner).
Daily run 3 Nov: key 1 hit the 20 search limit after 5 calls, key 2 did the rest; the
decision call failed 29 times on 503s/timeouts before gemini-3.6-flash on key 3 answered.

Built and ran a historical backtest (`backtest.py`) on football-data.co.uk (via a public
GitHub mirror, the site is blocked here): 41,971 matches, 17 leagues, 2019-20 to 2025-26,
1,812 match days; bot's own build_ticket and config, average price, Pinnacle fair chance,
15% tax. Pinnacle-expected ROI after tax (closing prices): live rule −16.4% (realised
−14.2% ± 2.8), 2 legs −16.1%, no double chance −15.7%, h2h only −16.1%, totals only
−16.4%, edge_first −14.4%, ticket at best price −10.3% (realised −8.0%), one single a day
−8.2% (−9.7%), single at best price −4.6% (−5.9%), 2% value singles −5.5% (−6.9%, +2.1%
before tax), tax-proof value +2.0% (−2.7% ± 6.0, 248 bets). Opening prices are 1-3 points
worse. Without the 10% outlier cap on the best price, tax-proof value shows +16% after
tax in every season: stale or wrong maximum prices, not edge (Kaunitz's accounts were also
limited on such prices). Single legs at the average price: h2h 1.20-1.40 realised +1.1%
(Pinnacle said −4.1%), dc −8% to −10%, totals −3.5% to −5.8%.
De-margining check (26,791 Pinnacle closing 1X2): proportional (what the bot uses)
understates favourites (bucket 70-80%: 74.5% predicted, 78.4% won); power and additive
methods are better (74.4% → 77.4%, log loss 0.98851 vs 0.98899).

Researched: Whelan, "The Parlay Puzzle" (2026): expected return r^N − 1, parlays hold 17-19%
for books vs 3-5% for singles in New Jersey, at most 2 legs is optimal even with an edge
unless legs are above ~53%; Moshrefi (arXiv 2607.14430): parlay prices on Kalshi add about
3% per leg; Hegarty and Whelan on loss rates: longshots carry more margin than the overround
implies. Data Golf (favourite-longshot bias at sharp books). football-data.co.uk notes on
Max/Avg columns.

Ideas considered (scored in IDEAS.md): historical backtest; price-shopping shadow; one
single a day; tax-proof value; power/Shin de-margining; league margin table; self-chaining
closing job; portfolio staking; AI forecasting tournament on past matches (rejected,
leakage); dropping double chance (updated with backtest evidence).

Changed: new `backtest.py` + `tests/test_backtest.py` + monthly "Historical backtest"
workflow (downloads the originals, commits `data/backtest/`). New shadows: actual_best,
single, taxed_value (closing prices for taxed_value too). Two lessons in
`prompts/lessons.md` (market accuracy; favourites slightly underpriced). The real ticket is
chosen exactly as before (the lessons only touch the AI's wording of verdicts), so no
preview was started, which also keeps key 2's search quota for tomorrow.

To measure next: actual_best odds gain per day; single vs actual return; taxed_value bets
per day; try power de-margining on the value shadows; per-league margins from the backtest.

## 2026-11-03 (evening review): power de-margining, tested on 80,000 matches

Measured: nothing new settled since the morning (115 settled judged picks; ticket 26 open:
Anaitasuna v Alavés Under 4.5 and Kansas St -10.5). Picks by odds band still track the market
(1.00-1.35 77% vs 75%, 1.35-1.60 71% vs 63%, 1.60-1.80 56% vs 56%, 1.80-2.10 51% vs 50%);
Brier market 0.2278 vs AI 0.2323. The closing job did run near a kick-off today (17:44 UTC,
5 captures for the Copa del Rey games), the first since the 2 Nov change. 3 Nov's slate was
36 NCAAB picks of 41 (opening-week mismatches); the new shadows from the morning review
start with tomorrow's run.

Researched: Goto, Takeishi and Yairi (arXiv 2604.17194, 2026; 90,014 football matches,
2012-2024, five books): power or their OO-EPC method has the lowest log loss, proportional
the highest for all five books; fitted power constant 1.06-1.15 (favourite-longshot bias).
`implied` R package docs (proportional "tends to be the least accurate"; additive can go
negative). Edge Lab on 1,892 Polymarket sports markets (no bookmaker match, weak evidence:
kept Polymarket as a low-priority idea).

Tested (football-data mirror, Pinnacle closing 1X2, 80,832 matches 2012-2026): log loss
proportional 0.99573, Shin 0.99554, power 0.99551. Logistic recalibration fitted on 2012-2019
and tested on 2019-2026: proportional slope 1.047 (test log loss 0.61755 -> 0.61746 after
recalibration), power slope 1.013 (0.61739, no change), so power is already calibrated.
Single bets after the 15% tax: heavy favourites at the best price are the only zone near
break-even (h2h 1.01-1.20 at best: 557 bets about +0.2%; at the average price -4%). Tax
hurdle is about 15% x (1 - chance), so it is smallest on favourites.
Backtest 2019-2026 (paired, same days): live ticket rule with power chances -11.8% vs
-14.2% (close), -17.7% vs -19.7% (open), paired +2.5 ± 2.1 and +2.0 ± 2.1 points.
Tax-proof singles at best price with power chance, odds 1.05-4.00: 802 bets +0.2% ± 2.5
(close), 168 bets -3.4% ± 4.9 (open).

Ideas considered (scored in IDEAS.md): power de-margining for value and ticket (built);
heavy-favourite value from odds 1.05 (built, part of it); extremizing/recalibration (tested,
dropped); Gemini decision circuit breaker; shortlist league cap; late power value; paired
comparisons in the backtest; taxed Kelly ranking; Polymarket reference (kept, low).

Changed: `power_devig()` in bot.py; every candidate carries `power_prob` and `sharp_power`.
New shadows "power_value" (tax-proof singles at the best price with the power chance; the
wide scan for it starts at odds 1.05, new config `value_min_odds`) and "power_ticket" (live
rule with power chances); power_value gets closing captures compared power to power.
backtest.py has `most_likely_power` and `value_taxed_power`; reports refreshed. New
`tests/test_power.py`. The real ticket is unchanged, so no preview run.

To measure next: power_value bets per day and CLV; power_ticket vs actual and market; if
power_ticket holds up, switch the ticket's chance to power (backtest says about +2 points).

## 2026-11-04 (morning review): late tax-proof singles and a faster Gemini fallback

Measured: 149 settled judged picks, 58.4% won vs 56.4% market chance. By verdict (won minus
market): AGREE +2.3 points (38), RISKY +0.3 (80), AVOID +6.0 (31), so the AI's verdicts
still do not sort winners from losers. Brier market 0.2330 vs AI 0.2359. In 42 complementary
pairs (both sides of one line) the AI said AGREE to both 4 times; its adjusted chances for a
pair sum to 0.94-1.01. Paper tickets 23-26 all lost (-400); ticket 26's lost leg, Kansas St
-10.5 at 52% (NCAAB season opener), had research quoting a 71-69 projection against it and the
AI still said AGREE (and AGREE to the other side, +11.5): a coin flip, not foreseeable, but a
sign of incoherent verdicts. Unsettled: 3 Nov Copa del Rey picks (incl. the ticket's Under 4.5)
and a 2 Nov tennis pick; the scores feed may not cover them. Closing captures: 36 on 3 Nov,
46-106 minutes before the start; CLV vs closing fair -6.5% on average (the margin). Shadows:
nothing new settled (2 Nov: market won, actual lost; 3 Nov actual = market, lost). Daily run 4
Nov: decision call failed 33 times (503 and timeouts on gemini-3.8-flash, all 4 keys x 4
attempts, then 3.6-flash key 1) before 3.6-flash key 2 answered; key 1 hit its search quota.

Tax rule checked (Zlatna Kopacka rules, art. 21): 15% of the real winnings (payout minus stake),
per winning ticket, no tax-free amount. The bot's model is right. (The state lottery's 5,000
MKD threshold applies to lotto only.)

Backtest (football-data mirror, 2019-2026), tax-proof power singles at the best price:
closing 802 bets +0.2% ± 2.5 (expected +1.5%); by odds 1.05-1.30: 238 bets +5.1% ± 2.2,
1.30-1.60 -0.6% ± 3.8, 1.60-2.20 -3.6% ± 5.6; h2h +1.4% ± 2.7, totals -3.1% ± 5.6; by taxed EV
0-1% -2.1%, 1-2% +4.6%, 2-5% -0.5% (no threshold effect). Opening prices: 168 bets -3.4% ± 4.9.
All h2h favourites, no value filter, after tax: best price 1.05-1.20 -0.2% ± 1.5, 1.20-1.30
-1.8%, 1.30-1.45 -1.5%; average price -3.9%, -4.5%, -3.2%. Power chances are calibrated there
(hit 88.8% vs 88.3% expected). So: price shopping and timing are the levers; the edge rule
matters less.

Researched: Gemini 503 handling (InventiveHQ, dev.to "503 reality check", Google AI forum):
capacity is per model; retry with backoff and jitter, and fall back to another model.
OddsPapi soft-book lag (Sep 2026): 1xBet follows Pinnacle moves in 6-13 minutes, Bet365 in
47-67 and only 59-73% of them, so near-kick-off gaps at slow books can be real.

Ideas considered (scored in IDEAS.md): late tax-proof power singles (built); Gemini model
rotation (built); fallback score source (ESPN, blocked here); verdict coherence check;
heavy-favourite best-price shadow; late ticket email; online AI weight; arbitrage after tax
(dropped by arithmetic: a 2.10/2.10 arb loses 3.3% after tax).

Changed: new shadow "late_power" logged by the closing job (`late_shadow_bets`), the opening-
time twin of power_value. `gemini()` now rotates: 2 attempts per key, after 3 busy failures
(503/500/timeouts) on a model the next model, 2 rounds (3 for search); "per day" 429 drops a
key at once; jittered backoff. New `tests/test_late_gemini.py`. The real ticket is chosen as
before, so no preview run (also keeps search quota).

To measure next: late_power bets per day vs power_value; failed Gemini calls per run (target
under 8); whether Copa del Rey/tennis legs settle; first shadow ROI comparisons.

## 2026-11-04 (evening review): a closing watcher that keeps itself alive

Measured: no pick, ticket or shadow settled since the morning review (149 settled judged
picks, 58.4% won vs 56.4% market; tickets 23-26 lost; ticket 27 and all 35 picks of 4 Nov
pending; the 3 Nov Copa del Rey picks and a 2 Nov tennis pick still unsettled), so no new
lost legs to judge. Closing captures: 74 rows; picks' CLV vs closing fair -6.6% (54 non-
ticket, 2 ticket legs: the margin). First two value singles with a close: RB Leipzig v Man
City Over 3.5 at onexbet 1.92 closed 1.71 (CLV +6.3%), Viking v Sabah Over 3.5 at 1.97
closed 1.81 (+5.8%): the outlier book moved toward the market, which is what real value
looks like; far too few to conclude. The only closing run of 4 Nov (17:56 UTC) captured
the 20:00 matches 123 minutes early and none near kick-off, and no late_power or
late_value bet was logged.

Root cause, measured with the Actions API: 15 closing runs from 31 Oct to 4 Nov against
about 160 scheduled (36 a day); on 4 Nov the 06:17-09:53 UTC daily crons ran at 14:52,
15:26, 15:47, 16:23 and 17:36 UTC. Usage API: billable 0 ms for both daily and closing runs.

Researched: GitHub docs (trigger a workflow): events made with GITHUB_TOKEN start no new
run "with the exception of workflow_dispatch and repository_dispatch", which "always create
workflow runs". Community discussions #210625 (a daily cron created 4h22m late) and
#210925 (slots missing, runs appearing hours later; no staff answer; advice: external
scheduler or workflow_dispatch). So self-dispatch is the free, owner-free fix.

Ideas considered (scored in IDEAS.md): self-continuing closing watcher (built); late ticket
email (now feasible, raised to 4/3/3); late ticket shadow; slow-book move follower; exchange
back-lay spread as confidence; ice hockey; fallback score source (ESPN and TheSportsDB both
blocked from this sandbox, still needs a preview to test); verdict coherence check.

Changed: `closing_chain_ok()` and `--closing-chain` in bot.py; closing.yml takes a `chain`
input, naps as long as the run lasts (36 minutes) when chaining is on, captures only bets
within 60 minutes inside the chain, and dispatches the next link before ending; daily.yml
starts the chain after saving the ledger (not for preview, diagnose or resend). Both get
`actions: write`. Config: closing_chain, closing_chain_max_runs 60, closing_chain_idle_hours
14, closing_run_minutes 36, closing_chain_window_minutes 60. New `tests/test_chain.py`; the
workflow loop was also dry-run with stubbed python/gh/sleep. Ticket selection unchanged, so
no preview run. Smoke test: a manual closing run with chain=1 at 20:26 UTC parsed the input,
found nothing due and ended the chain as designed; the first self-dispatch happens on 5 Nov.

To measure next: did the 5 Nov daily run start the chain, and did it run unbroken until
the last bet (Actions list for closing.yml, event workflow_dispatch); share of picks with a
capture within 60 minutes; late_power and late_value bets per day; closing credits per day.

## 2026-11-05 (morning review): a second results source, checked twice

Measured: 182 settled judged picks, 59.9% won vs 57.0% market chance; Brier market 0.2266
vs AI 0.2290. By verdict (won minus market): AGREE +1.8 points (43), RISKY +2.9 (107),
AVOID +3.9 (32): verdicts still do not sort winners. By market: h2h +7.1 (30), dc +3.7
(36), totals +2.9 (77), spreads -1.4 (39). Ticket legs 5/9 won vs 60% expected. Ticket 27
(4 Nov): AEK v Real Madrid Over 3.5 won; both Paris Masters legs (Paul, de Minaur) still
pending. No new lost ticket leg to judge. Shadows settled so far are tiny: market 2/2 won
(+2.6 units), value_single 2/2 (+1.6), actual/ai_own 0/1, edge_first 0/2, kaunitz 0/1.

Found: 10 picks and 14 shadow legs from 2-4 Nov were still pending on 5 Nov, all ATP Paris
Masters (2 and 4 Nov) or Copa del Rey (3 Nov); October tennis legs had settled, so the
Odds API scores feed covers these competitions only patchily. After 3 days they are voided,
so ticket 27 would have counted as a win at 1.73 regardless of the tennis results, and
power_ticket, single, actual_best and ai_own for 4 Nov hinge on the same legs.

Chain check: the 5 Nov daily run (07:05 UTC, on time) started the closing watcher; links
ran 07:14, 07:50, 08:26, 09:02 (36 minutes each) as designed. A second, owner-started daily
run at 07:35 ("already ran") also started a link; the concurrency group cancelled it at
07:50, so the two chains merged into one. Captures for 5 Nov come this evening.

Researched: The Odds API tennis page (covers ATP 1000 incl. Paris Masters for odds; says
nothing about scores); ESPN hidden API (sportsapis.dev, Nov 2026: scoreboard per
league with ?dates=YYYYMMDD, but ESPN, TheSportsDB and Sofascore are all blocked from this
sandbox, so a parser could not be tested); Gemini grounding accuracy reports (grounded
answers are far better than ungrounded but still err); blockchain oracle design (UMA,
Chainlink: accept a result only when independent reporters agree) as the model for a
two-answer agreement rule.

Ideas considered (scored in IDEAS.md): second results source with agreement (built); ESPN
as a third source; void-bias audit; tennis retirement rule; Thompson-sampling strategy
chooser; tennis fatigue signal; settlement-aware shortlist; late ticket shadow (kept).

Changed: `fill_missing_scores()` runs before settling (not in previews): it finds bets that
started 6+ hours ago with no feed score (ticket legs, picks, shadows; tennis only h2h), asks
Gemini with search twice (second call with the list reversed), and uses a score only when
both answers match and it is plausible for the sport; football is the regular-time score.
New prompt `prompts/settle.txt`, audit log `data/fallback_scores.csv`, config
fallback_scores, fallback_after_hours 6, fallback_max_events 12. New
`tests/test_fallback.py`. Ticket selection unchanged, so no preview run.

To measure next: fallback_scores.csv on 6 Nov (did ticket 27's tennis legs and the Copa
del Rey picks settle, did the two answers agree); search calls per run stay under 40;
closing captures within 60 minutes for 5 Nov; late_power bets per day.

## 2026-11-05 (evening review): every strategy scored at closing prices

Measured: no ticket settled since the morning (settlement runs with the daily job), so no
new lost leg to judge; ticket 27 still waits on the Paris Masters legs (the new fallback
first runs on 6 Nov). The closing watcher worked all day: 5 Nov captures at 51, 30, 48 and
42 minutes before kick-off, 16 of 30 picks captured within 60 minutes so far (the NBA
picks start after midnight UTC), 11 of 20 closing credits used. First late shadows logged:
5 late_value and 2 late_power bets. CLV within 60 minutes: picks -5.7% (33, average
price vs closing fair), value singles +6.6% (6, 5 positive), power_value +3.1% (2). But
after the 15% tax the closing-price expected return of the value singles is -3.1% ± 2.2,
and picks at average prices -11.5% to -12.5% for every verdict (AGREE 8, RISKY 20, AVOID
5 captured). Found a logging bug: late_power recorded the proportional sharp chance as its
fair chance instead of the power chance it selected on (edge looked -2% on a +EV bet).

Researched: Johari, Pekelis and Walsh, "Always Valid Inference" (arXiv 1512.04922): the
mixture SPRT, stop when the mixture likelihood ratio reaches 1/alpha, always-valid
p-values that may be checked after every observation. Simulated our use (plug-in
variance): 17% false alarms when testing from bet 2, 2.5% with a 10-bet burn-in (alpha
5%), power about 12% for a +3% edge at sd 0.3 over 150 bets, 100% at sd 0.03 (singles at
short odds are far easier to judge than tickets). Practitioner CLV write-ups agree that
closing value is the low-noise early signal of an edge (search results were mostly thin
blogs; the Pinnacle article could not be fetched). Offline test of a totals drift idea on
the football-odds mirror (38,245 matches, 2019-2026, Pinnacle open vs close): Over 2.5
chance drifts -0.14 ± 0.02 points; nothing to exploit (dropped).

Ideas considered (scored in IDEAS.md): closing-price scoreboard with mSPRT (built); tax
break-even curve; Thompson-sampling chooser (raised); totals drift in cups (new) and in
domestic leagues (dropped); closing-price AI weighting; late ticket shadow and email
(kept); Megawin prices; ice hockey.

Changed: new `scoreboard.py` (xROI after tax at the close per bet, per-strategy mean, se,
P(beats tax), mSPRT p, verdict after 20 bets, paired difference vs the real ticket;
picks grouped by verdict as singles) writing `data/scoreboard.md`, called from the email.
`closing_todo` also captures ticket-shadow legs not in the pick log (once per bet);
closing rows record `close_power`; late_power logs its power chance. New
`tests/test_scoreboard.py`; `test_late_gemini.py` updated for the late_power fix. Ticket
selection unchanged, so no preview run.

To measure next: scoreboard coverage (share of ticket-shadow bets scored, target 80%+),
closing credits per day with the extra legs (cap 20), first verdicts in 2-3 weeks,
whether value singles' after-tax xROI stays negative (then restrict them to the tax
break-even curve), fallback_scores.csv on 6 Nov.

## 2026-11-06 (morning review): the ticket now maximises the return after tax

Measured: 217 settled judged picks, 58.5% won vs 56.9% market chance; Brier market 0.2318
vs AI 0.2338. By verdict (won minus market): AGREE -1.7 points (50), RISKY +2.7 (124),
AVOID +2.6 (43): verdicts still do not sort winners. Ticket legs 6/13 won vs 63.5%
expected; six paper tickets lost in a row (23-28). Ticket 28 (5 Nov): Leverkusen v
Marseille (73%, AGREE) lost: research showed mixed form (lost 2 of the last 3 league
games) but nothing decisive, not foreseeable; Penn +30.5 v Illinois (52%, AGREE) lost:
the research had no 2026-27 data (THIN), so AGREE was unjustified, but the price was fair.
Research data quality vs results: GOOD +0.9 points (145), THIN -3.5 (19), NONE 0.0 (7),
no signal. Fallback scores worked: all 5 Paris Masters events settled with two agreeing
answers, ticket 27 settled as lost (de Minaur lost) instead of a false void win.
Scoreboard: still few captures; value singles -3.3% ± 1.9 after tax at the close, picks at
average prices -11% to -13% whatever the verdict. Gemini: 24 failed research calls today
(503s, both search keys hit the 20-a-day limit).

Researched: Whelan, "The Parlay Puzzle" (expected return (1-m)^N; combine at most two legs
when leg chances are 1/3-1/2); parlay pricing write-ups (margin compounds per leg);
Gemini free-tier grounding (usagebox Oct 2026, Google forum: not available on the free tier
for Gemini 3 models, so keys 3/4 cannot add search quota); bookmaker-consensus forecasting
(Goto et al. 2026, Kaunitz et al. 2017). Offline tests on the football-odds mirror: an
opening blend of average and Pinnacle chances does not beat Pinnacle alone (dropped).
Tax-aware ticket objective on 1,534 match days: expected -12.3% vs -14.5% (close) and
-13.3% vs -15.3% (open), realised -10.0% vs -14.2% and -12.9% vs -19.7%; at the best
prices -3.0% expected (vs -10.3% for the old rule at best prices).

Ideas considered (scored in IDEAS.md): tax-aware ticket objective (built); opening crowd
blend (dropped); data-quality gate (dropped); Gemini 3.8 search on keys 3/4 (dropped);
tax break-even shortlist; two-account recommendation from tax_best; NHL favourites; late
ticket shadow and Thompson chooser (kept).

Changed: `taxed_return()` and `build_taxed_ticket()` in bot.py; `ai_pick` builds the
ticket with the best expected return after tax from power chances plus the 20% AI shift
(`blend_power`), keeps the AI's ticket when within 0.5 points; the rules fallback uses the
same objective; config `ticket_objective` "taxed_ev". New shadows likely_ticket (old rule),
tax_best (new rule at best prices), tax_market (no AI); their legs are captured near
kick-off. decide.txt step 2 and lessons.md explain the objective. backtest.py gains
tax_ticket and tax_ticket_best; reports regenerated from the mirror. New tests/test_taxed.py.

To measure next: scoreboard paired xROI of actual vs likely_ticket (expect about +2 points),
tax_best's closing xROI (break-even would justify recommending extra accounts), average
total odds and legs of the new ticket, closing credits per day with three more shadows.
Preview run (09:45 UTC, not counted): the AI path ran and the code built the taxed ticket,
Virtus Bologna +4.5 @1.87 and Everton @1.67 (3.12, 2 legs); the old rule would have taken
3 legs (Rapid Wien 1.21, Celtics 1.28, Everton 1.67); tax_best priced the same legs at
1.91 (williamhill) and 1.74 (onexbet); tax_market and likely_ticket logged as designed.

## 2026-11-06 (evening review): GitHub stopped every run; a minutes guard

Measured: no ticket or pick settled since the morning (217 settled picks, 58.5% won vs
56.9% market; settlement runs with the daily job), so no new lost leg to judge; ticket 29
(Olympiacos to win 1.38, Partizan v Maccabi Over 171.5 1.84, both Euroleague tonight) is
open. Only 2 closing captures today (Sydney FC, 08:07 UTC). Reason: every GitHub job since
15:57 UTC failed in 2-6 seconds with the annotation "The job was not started because
recent account payments have failed or your spending limit needs to be increased". From
the runs list, November minutes (each run's wall time rounded up; all workflows have one
job): 2,243 in all, closing watcher 1,994 (1 to 5 Nov before the chain: 3-5 a day; 5 Nov
1,199; 6 Nov 779), daily 238, notify 11. GitHub Free includes USD 12 of compute a cycle,
about 2,000 Linux minutes; standard runners are free in public repositories (GitHub docs,
"How use of GitHub Actions is measured"). The total crossed 2,000 at about 13:30 UTC, so
the cycle very likely starts on the 1st: unless the owner acts, no daily ticket runs until
1 December. The 4 Nov "billable 0 ms" check read a field that does not measure this.
Also found: the daily backup crons ran 8 hours late (14:19-15:24 UTC) and each one, though
it found the day done, started a new watcher link, which cancelled the queued one.
Gemini: 24 research calls failed today (503s; both search keys hit 20 a day).

Researched: GitHub billing docs (included compute as a money amount, reset each billing
cycle, usage blocked without a payment method, public repositories free); community
threads on scheduled-workflow delays and external timers (cron-job.org, crontap,
runhooks: workflow_dispatch from an outside timer is the usual fix); Cloudflare Workers
free limits (cron triggers on the free plan) as a watcher outside Actions; Dean and
Barroso's hedged requests for the Gemini 503 storms.

Ideas considered (scored in IDEAS.md): minutes guard (built); make the repository public
(recommended, owner's decision); external timer for one-pass captures; Cloudflare Worker
watcher (unconventional); capture triage (unconventional); hedged Gemini requests
(unconventional); batched research; outage-aware voiding; old ticket legs in the score
fallback (built, small).

Changed: new `actions_budget.py` (cycle minutes from the runs API saved to
`data/actions_usage.json`; closing allowance = (2,000 x 0.85 - used - 45 per remaining
day) / remaining days, minus today's watcher minutes; no limit when public; fails safe to
no watcher minutes, never blocks the ticket). `closing_chain_ok` needs a full link of
allowance; `--closing-plan` sets each closing run's nap and run length (private and out
of minutes: one capture pass, about a minute). The daily job measures usage, shows it in
the email (warning at 75%), and starts the watcher only after a run that made the ticket
(`made` step output). Closing backup crons hourly instead of every 30 minutes. The score
fallback looks up ticket legs up to 40 days old, so a stop of the runs does not void them.
config: actions_included_minutes 2000, actions_budget_share 0.85,
actions_daily_reserve_minutes 45, actions_closing_max_per_day 120, actions_cycle_day 1.
New tests/test_actions_budget.py; test_chain.py covers the private case. Ticket
selection unchanged, and no preview run possible while GitHub refuses jobs.

To measure next: whether jobs start again (owner makes the repository public or the
cycle resets), data/actions_usage.json each day (private: under ~65 minutes a day),
whether ticket 29 settles through the fallback when runs resume, closing capture share in
private mode. The tax-aware ticket's first live comparison waits for runs to resume.

Update 22:15 UTC: the owner made the repository public. GitHub starts jobs again: the
failed "Email bot updates" run was re-run (success, so the change email went out) and a
closing watcher link was started by hand; the minutes guard sees a public repository and
sets no limit, so the full watcher runs from the next daily ticket.

## 2026-11-07 (morning review): kick-off sweep for the tax-proof singles

Measured: 266 settled picks won 59.4% vs 57.3% market chance (AGREE 56.6% vs 57.9%, RISKY
60.3% vs 56.4%, AVOID 59.7% vs 58.8%: the AI's verdicts still carry no signal; Brier market
0.2295, AI 0.2311, sharp 0.2226 on 162). By odds: 1.00-1.30 +5.9 points vs market (47),
1.70-2.00 +2.0 (151). Ticket legs won 6 of 15 vs 63% expected (z about -1.9), and paper
tickets 23-29 all lost (-700; seven losses in a row at a ~36% hit rate happen about 4% of
the time). Lost legs judged against the research: Olympiacos (Montero, Dorsey out, Fournier
doubtful, all known and priced), Leverkusen (two defeats in three, priced), Penn +30.5 and
Kansas St -10.5 (research had "NO CURRENT DATA" in opening week; risk visible, direction
not), de Minaur, Partizan Over, Young Boys, Man City: no foreseeable cause. Earlier
changes: tax-aware ticket too new (likely_ticket 1 bet); minutes guard fine (repository
public, 2,650 cycle minutes, watcher 284 today, no limit); Gemini today 1 quota 429 and 3
busy 503s (under the target of 8); fallback scores settled 5 Paris Masters matches.
Scoreboard: tax-proof power singles +1.3% xROI (2 scored), late_power -1.4% (2), every
other strategy -6% to -18%. late_power logged only 2 bets since 4 Nov: the watcher fetches
only leagues with a logged pick.

Researched: The Odds API market list (soccer spreads/draw-no-bet not in featured markets,
"mainly US sports", so Asian handicap legs are out: dropped); arXiv 2608.05030 (LLM
exact-score harness on Dixon-Coles: top-1 10.0% to 14.7% on 150 EPL games, no market
comparison); preprints 202607.0719 (web search cut LLM forecasting hallucinations 75-79%;
supports keeping search in research, nothing to change). Backtest report re-read for the
late tax-proof rule (802 bets at close, +0.2% realised, +1.5% expected; 1.05-1.30 +5.1%).

Ideas considered (scored in IDEAS.md): kick-off sweep (built); soccer Asian handicap /
draw-no-bet legs (dropped, no feed); NFL/NHL in the pool; adverse-selection monitor for
ticket legs (unconventional); bet-time advice per leg (unconventional, execution
algorithms); random sweep slot (unconventional, survey sampling); LLM exact-score harness
(low); hedged Gemini requests and late ticket shadow (kept).

Changed: bot.py `plan_sweep`/`write_sweep_plan` (daily run saves `data/sweep_plan.json`:
up to 6 busiest kick-off slots in leagues the watcher does not already fetch), `run_sweep`
(called first in every closing pass: 15 minutes before a slot's first start, one h2h fetch,
late_power rule logged as shadow "late_sweep"; state and credits in closing_budget.json),
`closing_next_wait` counts planned slots so the chain stays alive for them. config:
late_sweep_credits_per_day 6, late_sweep_slot_minutes 60, late_sweep_min_events 2,
late_sweep_min_credits_left 60. New tests/test_sweep.py. Ticket choice unchanged; no
preview run (selection of the ticket did not change).

To measure next: late_sweep bets per day (expect ~0.5), its xROI and realised return next to
late_power, extra score credits for new leagues, Odds API credits left at month end.
