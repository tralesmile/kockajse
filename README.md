# kockajse

Sends one email every morning at about 08:00 Skopje time with:

- the final result of the previous ticket, with 15% tax on winnings applied,
- the bankroll and the running profit or loss,
- one new combined ticket (total odds between 2.50 and 3.50) for the next 24 hours.

Football, basketball, tennis and handball odds come from The Odds API. Picks are rule-based:
the bookmaker margin is removed from the odds to estimate each outcome's chance, and the most
likely combination inside the odds range is chosen. This does not beat the bookmaker; expect
to lose money over time.

## Setup

Add these under Settings > Secrets and variables > Actions > New repository secret:

| Secret | Value |
|---|---|
| `ODDS_API_KEY` | free key from the-odds-api.com |
| `ODDS_API_KEY_2`, `_3`, `_4` | optional spare keys, used in order when the one before is refused or out of requests |
| `RESEND_API_KEY` | free key from resend.com (sign up with the address that receives the tips) |
| `EMAIL_TO` | the address that receives the tips |
| `GEMINI_API_KEY` | optional: Google Gemini key, adds a written AI check of each pick |
| `GEMINI_API_KEY_2`, `_3`, `_4` | optional spare Gemini keys, used when the one before is refused or out of quota |

To send through Gmail instead of Resend, set `SMTP_USER` and `SMTP_PASSWORD` (an app password).

Run it by hand from the Actions tab: Daily ticket > Run workflow.

## Paper mode

With `"paper_mode": true` in `config.json`, tickets are tracked with a virtual stake
(`paper_stake`) and never touch the real bankroll. The email marks them "do not place".

## Files

- `config.json`: stake (25% of the available bankroll, minimum 50 MKD), odds limits, tax rate, leagues.
- `data/state.json`: bankroll and open tickets.
- `data/ledger.csv`: every settled ticket.
- `prompts/`: the instructions given to Gemini (scout, research, decide) and `lessons.md`,
  the lessons learned from past results that are added to them.
- `data/picks.csv`: every bet the AI judged, with its verdict and the result.
- `data/research/`: each day's research notes and AI decision.
- `data/shadow.csv`: shadow tickets, the bets other strategies would have made each day, settled
  like paper tickets so strategies can be compared.
- `data/learning_log.md`: what each review found and changed.
- `IMPROVING.md`: the rules the twice-daily review task follows.
- `tests/test_tracking.py`: checks for paper mode, the pick log and scorecard.
- `tests/simulate.py`: offline test with fake games.
- `tests/test_markets.py`: checks for bet types, settlement and the AI path.
- `tests/test_shadow.py`: checks for best prices, value bets and shadow tickets.
