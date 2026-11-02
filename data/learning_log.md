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
