# How the review task improves the bot

A Claude scheduled task follows this file twice a day (10:20 and 21:20 Skopje time). The
owner wants the best results possible and wants the bot to get better every day, so the
review is free to change anything that could help: the prompts, the way matches are
researched and judged, the code, the data sources, the bet types, the selection logic.
Be open to new ideas and try them. The daily tips email keeps going throughout.

## Be creative

The owner wants the most creative, best possible solution each time, not the safest small
tweak. Every review:

- **Brainstorm widely before choosing.** Write down at least 8 different ideas, spread over
  these areas: new data, modelling and maths, prompts and AI workflow, ticket selection,
  bet types and markets, timing (when we pick, when we re-check), sports and leagues,
  experiments and measurement. Include at least two unconventional ones: borrow from
  quantitative finance, forecasting tournaments, prediction markets, sports analytics
  research, machine learning, or how professional bettors and syndicates work.
- **Research deeply.** Use several sources per topic: academic papers, practitioner blogs,
  open-source betting and sports-modelling projects on GitHub, data-provider docs. Look for
  what has measurably worked for others, then adapt it to this bot's limits.
- **Score and pick.** Rate each idea for expected impact, confidence and effort, and build
  the best one. A bold idea with a big possible upside beats a safe tweak when both fit the
  quota. At least one review per week should ship something bold.
- **Keep a backlog.** `IDEAS.md` holds every idea with its status (new, building, live,
  measuring, dropped) and, once known, its result. Add new ideas each review, move tried ones
  to their outcome, and drop ideas the data rejects. Do not repeat a dropped idea without new
  evidence.
- **Run experiments, not guesses.** Where possible, test an idea side by side instead of
  replacing what works: for example, log the ticket an alternative strategy would have
  chosen ("shadow tickets") and settle it like a real paper ticket, so strategies can be
  compared on the same days. Prefer changes that make the next review smarter.



1. **Learn from results.** With code, measure the pick log (`data/picks.csv`): win rate
   against the market's chance by verdict, bet type, sport, league, odds band, number of
   picks, day of week. For each lost ticket pick, read that day's research
   (`data/research/<date>.json`) and decide whether the loss was foreseeable.
   For questions the live logs are too small to answer, use the historical backtest
   (`backtest.py`, report in `data/backtest/report.md`): it replays the selection rules on
   seven seasons of European football. football-data.co.uk is blocked from the review's
   sandbox; clone the public mirror `https://github.com/huhao930422-debug/football-odds-mirror`
   (shallow) and run `python backtest.py --dir <clone>/data --seasons 1920,...,2526`, or
   start the "Historical backtest" workflow, which downloads the originals.
2. **Research.** Search the web for better methods and data and bring back what applies.
   Rotate topics so each review looks at something new; record what you looked at in
   `data/learning_log.md`. Starting ideas, not limits:
   - Closing line value: record the odds again shortly before kick-off and measure whether
     our picks beat the closing price. It is the standard early sign of a real edge and
     needs far fewer bets than win rate.
   - Use a sharp bookmaker (for example Pinnacle, if the odds feed carries it) as the fair
     price, and prefer picks where other bookmakers' prices are above it.
   - Free data that improves research: confirmed lineups, injury lists, expected goals,
     team ratings (Elo, ClubElo), schedule congestion, travel, weather for outdoor games.
   - Better prompts: structured checklists, asking for sources with dates, a second pass
     that argues against each pick, self-consistency across two runs.
   - Leagues, sports or bet types where the market is weaker or our scorecard is better;
     dropping ones that keep losing.
   - Model choice and quota use (see Limits below).
3. **Improve.** Implement the most promising change. Bigger changes are welcome when the
   evidence or research supports them. Keep each change focused enough that its effect can
   be measured, and note in `prompts/lessons.md` any lesson the AI should apply daily.
4. **Check.** Add or update tests for new code. Run `python tests/test_markets.py`,
   `python tests/test_tracking.py`, `python tests/test_shadow.py`, `python tests/test_closing.py`, `python tests/test_backtest.py`, `python tests/test_power.py`, `python tests/test_late_gemini.py`, `python tests/test_chain.py`, `python tests/test_fallback.py` and `python tests/simulate.py`;
   all must pass. After a
   change to how picks are chosen, you may start one preview run to see it work live:
   `gh api -X POST repos/tralesmile/kockajse/actions/workflows/daily.yml/dispatches -f ref=main -F 'inputs[preview]=true'`
   and read `data/preview.json` when it finishes (about 15 to 25 minutes).
5. **Record and report.**
   - Add an entry to `data/learning_log.md`: what you measured (numbers), what you
     researched, what you concluded, what you changed.
   - If you changed the bot, add a new entry at the top of `CHANGES.md` (under the intro,
     as `## <date>: <short title>` followed by 3 to 6 short bullet points in plain
     language for the owner: what changed, why, and what to expect). Pushing a change to
     `CHANGES.md` emails it to the owner automatically. If nothing changed, do not touch
     `CHANGES.md`, so no email is sent.
   - Commit with a message starting "Review:", `git pull --rebase`, `git push`.

## Firm rules

These protect the owner's money and the honesty of the results, not the scope of ideas.

- **Results are never edited.** Do not change recorded results or history in
  `data/ledger.csv`, `data/picks.csv`, `data/state.json` or `data/research/`. Code may add
  new columns or new files, but past rows stay as they were.
- **Real money is the owner's decision.** Do not turn off `paper_mode` or change
  `paper_stake`, `stake_percent`, `min_stake` or `tax_rate`. If the evidence says real
  betting is justified, say so in `CHANGES.md` as a recommendation and leave it to the owner.
- **The daily run must keep working.** Never push code whose tests fail. Never start the
  daily workflow without `preview`, and never with `force`.
- **No secrets in the repository,** no change to who receives the emails, and only free
  services unless the owner has agreed to pay.

## Limits to plan around

- Gemini: web search works only with `gemini-2.5-flash` on keys 1 and 2, about 20 search
  requests a day each. A daily run uses about 14. Requests without search work on all four
  keys with newer models. Quota resets at 02:00 Skopje time.
- The Odds API: 500 requests a month per key, 4 keys. A daily run uses about 30.
- GitHub Actions run time is free for this repository; a run may take up to 40 minutes.
