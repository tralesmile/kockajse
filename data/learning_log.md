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
