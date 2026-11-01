# Ideas backlog

Every idea the review task considers, with its status and result. Statuses: new, building,
live, measuring, dropped. Newest additions at the top of each section.

## Live or measuring

- Sharp bookmaker (Pinnacle, Betfair, Matchbook) as the fair chance, with an edge figure per
  bet (31 Oct). Measuring: do positive-edge picks win more than negative-edge ones?
- Closing line value capture, `closing.yml` (31 Oct). Measuring: average move on AGREE vs
  AVOID picks once about 40 captures exist.
- Code chooses the most likely allowed ticket, AI chance blended at 20% (1 Nov). Measuring:
  how often code overrides the AI; ticket hit rate against win_prob.

## New

- Shadow tickets: each day also log and settle the tickets other strategies would have
  picked (market only, AI only, edge-first, 2-pick only), to compare strategies on the same
  matches.
- Second-pass critic prompt that argues against each pick before the decision.
- Late news check: re-check lineups and injuries an hour before kick-off and flag picks
  whose situation changed.
- Free team ratings (ClubElo for football, basketball ratings) as an independent chance to
  compare with the market.

## Dropped

(none yet)
