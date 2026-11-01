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
