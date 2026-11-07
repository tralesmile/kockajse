"""Odds API credit pacer.

Why (7 Nov 2026 evening review): the bot has four Odds API keys of 500 credits a month
(2,000 in all), but the daily run's own figure showed key 1 falling 252 -> 194 -> 109 on
5, 6 and 7 Nov: 58 and 85 credits a day, before the kick-off sweep (up to 6 more a day)
started. 2,000 credits last 66 a day for a 30-day month, so at 85-90 a day the last key
would run dry around 25 November and the bot would get no odds at all (no ticket, no
settling from the feed) until the keys reset. The GitHub minutes outage of 6 Nov showed
how a silent quota stops everything.

The Odds API says the /sports endpoint "does not count against the usage quota" and still
returns the x-requests-remaining header, so the daily run can read every key's balance for
free. This module:

- measures the credits left on every key (free) and keeps a short history in
  data/odds_credits.json, so a review can see the real burn per day;
- estimates the "core" credits a day (morning odds + scores, which the ticket needs) from
  that history, minus what the optional extras spent;
- gives the optional extras (closing-price captures and the kick-off sweep) only what is
  left after reserving the core for every remaining day of the month, with a safety margin;
- writes a one-line summary for the email: credits left, how long they last at this pace.

It fails safe in the other direction from the minutes guard: if the balance cannot be read
the extras keep their configured caps (the old behaviour), because a probe failure should
not switch experiments off; the daily ticket is never limited by this module.
"""
import json
import math
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.the-odds-api.com/v4"


def _time(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def cycle_end(now, cycle_day=1):
    """First moment (UTC midnight) of the next quota cycle after now."""
    day = max(1, min(28, int(cycle_day)))
    end = now.replace(day=day, hour=0, minute=0, second=0, microsecond=0)
    if end <= now:
        month = end.month % 12 + 1
        year = end.year + (1 if end.month == 12 else 0)
        end = end.replace(year=year, month=month)
    return end


def days_left(now, cycle_day=1):
    """Days still to pay for in this cycle, today included (at least 1)."""
    end = cycle_end(now, cycle_day)
    return max(1, math.ceil((end - now).total_seconds() / 86400))


def probe_key(key, opener=None):
    """Credits left on one key, read from the free /sports endpoint. None if unknown;
    0 if the key is refused or out of credits."""
    opener = opener or urllib.request.urlopen
    try:
        with opener(f"{API}/sports?apiKey={key}", timeout=20) as resp:
            value = resp.headers.get("x-requests-remaining")
            return None if value is None else max(0, int(float(value)))
    except urllib.error.HTTPError as err:
        return 0 if err.code in (401, 403, 429) else None
    except Exception:  # noqa: BLE001  network trouble: unknown, not empty
        return None


def load(path):
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return {}


def core_per_day(history, default):
    """Median of the measured core use per day: drop in the total between two morning
    measurements, minus what the extras spent in between. Falls back to the default."""
    days = sorted(history)
    values = []
    for a, b in zip(days, days[1:]):
        ha, hb = history[a], history[b]
        gap = (_time(b + "T00:00:00+00:00") - _time(a + "T00:00:00+00:00")).days
        if gap != 1 or ha.get("total") is None or hb.get("total") is None:
            continue
        drop = ha["total"] - hb["total"]
        if drop < 0:  # a key reset in between
            continue
        values.append(max(0, drop - int(hb.get("extras_before", 0) or 0)))
    values = values[-7:]
    if not values:
        return float(default)
    values.sort()
    mid = len(values) // 2
    med = values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2
    return float(max(med, 1))


def allowance(config, usage, now):
    """Credits the optional extras may spend today: (closing, sweep).

    Pool P (all keys, measured after the morning run), n days left including today,
    core C a day: the extras get D = (P - margin - (n - 1) x C) / n today, so the same
    split stays affordable every day to the reset. D is shared between closing and sweep
    in proportion to their caps. Without a measurement the caps apply unchanged.
    """
    cap_c = int(config.get("max_closing_credits_per_day", 16))
    cap_s = int(config.get("late_sweep_credits_per_day", 0))
    if not usage or usage.get("total") is None or not config.get("odds_pacing", True):
        return cap_c, cap_s
    # Only a measurement from the last 36 hours counts (the morning run makes one daily);
    # an old or future one leaves the caps unchanged rather than guessing.
    try:
        age = (now - _time(usage["measured"])).total_seconds() / 3600
    except (KeyError, TypeError, ValueError):
        return cap_c, cap_s
    if not 0 <= age <= 36:
        return cap_c, cap_s
    n = days_left(now, config.get("odds_cycle_day", 1))
    core = usage.get("core") or float(config.get("odds_core_per_day", 45))
    spare = (usage["total"] - int(config.get("odds_reserve_credits", 40))
             - (n - 1) * core) / n
    spare = max(0.0, spare)
    caps = cap_c + cap_s
    if caps <= 0 or spare >= caps:
        return cap_c, cap_s
    scale = spare / caps
    return int(math.floor(cap_c * scale)), int(math.floor(cap_s * scale))


def measure(config, path, now, keys, extras_spent=0, opener=None):
    """Probe every key (free), update the history and save. Returns the usage dict."""
    usage = load(path)
    balances = [probe_key(k, opener) for k in keys]
    known = [b for b in balances if b is not None]
    total = sum(known) if known else None
    if known and len(known) < len(balances) and usage.get("keys"):
        # Fill an unreadable key with its last known balance rather than counting it as 0.
        old = usage["keys"]
        total = sum(b if b is not None else (old[i] if i < len(old) and old[i] else 0)
                    for i, b in enumerate(balances))
    today = now.date().isoformat()
    history = usage.get("history", {})
    if total is not None:
        history[today] = {"total": total, "extras_before": int(extras_spent or 0)}
    history = {d: history[d] for d in sorted(history)[-14:]}
    core = core_per_day(history, config.get("odds_core_per_day", 45))
    usage = {"measured": now.isoformat(timespec="seconds"), "day": today,
             "keys": balances, "total": total, "core": core, "history": history}
    c, s = allowance(config, usage, now)
    usage["closing_allowance"], usage["sweep_allowance"] = c, s
    try:
        path.write_text(json.dumps(usage, indent=2) + "\n")
    except Exception:  # noqa: BLE001
        pass
    return usage


def run_out_date(usage, config, now):
    """Day the credits would run out if every day used the core plus the full caps."""
    if not usage or usage.get("total") is None:
        return None
    per_day = (usage.get("core") or config.get("odds_core_per_day", 45)) + int(
        config.get("max_closing_credits_per_day", 16)) + int(
        config.get("late_sweep_credits_per_day", 0))
    return (now + timedelta(days=usage["total"] / max(per_day, 1))).date()


def summary_line(config, usage, now):
    if not usage or usage.get("total") is None:
        return ""
    end = cycle_end(now, config.get("odds_cycle_day", 1)).date()
    out = run_out_date(usage, config, now)
    keys = usage.get("keys") or []
    shown = ", ".join("?" if b is None else str(b) for b in keys)
    c, s = allowance(config, usage, now)
    text = (f"Odds API credits left on all {len(keys)} keys: {usage['total']} ({shown}); "
            f"the ticket needs about {usage.get('core', 0):.0f} a day.")
    if out and out < end:
        text += (f" At full use they would run out on {out:%d %b}, before the reset on "
                 f"{end:%d %b}, so today's price checks are limited to {c} credits and "
                 f"the kick-off sweep to {s}.")
    else:
        text += f" Enough for full use until the reset on {end:%d %b}."
    return text
