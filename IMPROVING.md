# How the review task improves the bot

A Claude scheduled task reads this file twice a day and follows it. Its job is to learn
from settled results and make small, evidence-based improvements. Most reviews should
end with "no change": the sample is small and most short-run patterns are luck.

## What to read

- `data/picks.csv`: every bet the AI judged, with the market's chance, the AI's verdict and
  chance, whether it went on the ticket, and the result once settled.
- `data/ledger.csv`: every settled ticket (`mode` is `real` or `paper`).
- `data/research/<date>.json`: that day's research notes and the AI's raw decision.
- `data/state.json`, `data/last_run.json`: open tickets and the last run's AI call log.
- `prompts/scout.txt`, `prompts/research.txt`, `prompts/decide.txt`, `prompts/lessons.md`.
- `data/learning_log.md`: what earlier reviews found and changed.

## What to look for

1. **Calibration.** For each group (verdict, bet type, sport, league, odds band, on/off
   ticket): picks, win rate, average market chance, difference in points. The AI adds value
   only where its AGREE picks beat the market chance.
2. **Losing picks.** For each lost pick on a ticket, open that day's research notes and ask:
   was the loss foreseeable from what the research found or should have found (injury,
   rotation, motivation, weather, a factual error), or was it ordinary bad luck?
3. **Repeated research failures.** Stale or invented facts, contradicting itself, wrong
   competition, missing news that was available before kick-off.
4. **Run problems.** AI fallbacks to rules, quota errors, settlement errors in `last_run.json`.

## What may be changed

- `prompts/lessons.md`: the main tool. At most 15 lessons, each with the evidence behind it
  (counts, dates) and the date added. Remove a lesson when later data no longer supports it.
- Wording in `prompts/scout.txt`, `prompts/research.txt`, `prompts/decide.txt`, to fix a
  repeated research or reasoning failure. Every `{placeholder}` must stay exactly as it is.
- These keys in `config.json`, only within these ranges:
  - `ai_shortlist` 8 to 14, `ai_options` 3 to 8
  - `min_bookmakers` 4 to 10, `min_bookmakers_lines` 3 to 8
  - `min_leg_odds` 1.15 to 1.40, `max_leg_odds` 1.60 to 2.20
  - `priority_keys`, `skip_keys_containing`
  - `markets`: values may only use `h2h`, `totals`, `spreads`

## Evidence needed before a change

- A lesson or config change about a group needs at least 20 settled picks in that group and
  a difference of at least 10 points from the market chance, or a factual research failure
  seen at least 3 times.
- Never act on a single day's results.
- Prefer removing a bad habit over adding a clever rule.

## Never change

- Money and risk settings: `paper_mode`, `paper_stake`, `stake_percent`, `min_stake`,
  `tax_rate`, `min_total_odds`, `max_total_odds`, `max_legs`, `starting_bankroll`.
- `data/state.json`, `data/ledger.csv`, `data/picks.csv`, `data/research/`: read only.
- `.github/`, secrets, API keys, email settings.
- `bot.py`, except to fix a clear bug (a crash or a wrong settlement), with a test that
  shows it.
- Never start the workflow and never place, suggest or size real bets.

## Every review

1. Add an entry to `data/learning_log.md`: date and time, picks analysed, the key numbers,
   what you concluded, and exactly what you changed (or "no change" and why).
2. Run `python tests/test_markets.py`, `python tests/test_tracking.py` and
   `python tests/simulate.py`. If any fails, undo your changes and log that.
3. Commit with a message starting "Review:", then `git pull --rebase` and `git push`.
