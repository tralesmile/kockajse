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

## 2026-10-31 (evening review): sharp fair price

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
