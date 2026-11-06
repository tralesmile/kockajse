"""GitHub Actions minutes guard.

Why (6 Nov 2026): the repository is private, and GitHub Free includes about 2,000 Linux
minutes a month for private repositories (USD 12 of compute, reset each billing cycle;
standard runners in public repositories are free). The self-continuing closing watcher
(4 Nov) kept a runner busy almost all day, about 2,000 minutes in six days. From 15:57 UTC
on 6 Nov GitHub refused to start any job ("recent account payments have failed or your
spending limit needs to be increased"), including the daily ticket.

This module measures the minutes this repository has used in the current cycle from the
Actions API (one job per workflow, so a run's wall time rounded up to the minute is its
billed time) and decides how many minutes the closing watcher may spend today, always
keeping a reserve for the daily ticket on every remaining day. In a public repository
there is no limit and the watcher runs as before.

Everything fails safe: when the API cannot be read, the repository counts as private and
only the measured minutes saved earlier (or none) are used; the watcher then gets no extra
minutes, while the daily ticket itself is never blocked by this module.
"""
import json
import math
import os
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"


def _get(path, token):
    req = urllib.request.Request(API + path, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "kockajse-bot"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def _time(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def cycle_start(now, cycle_day=1):
    """Start (UTC midnight) of the billing cycle containing now."""
    day = max(1, min(28, int(cycle_day)))
    start = now.replace(day=day, hour=0, minute=0, second=0, microsecond=0)
    if now < start:
        month = start.month - 1 or 12
        year = start.year - (1 if start.month == 1 else 0)
        start = start.replace(year=year, month=month)
    return start


def cycle_end(start):
    month = start.month % 12 + 1
    year = start.year + (1 if start.month == 12 else 0)
    return start.replace(year=year, month=month)


def run_minutes(run):
    """Billed minutes of one workflow run (all our workflows have one job). Runs GitHub
    refused to start (billing block) or skipped last a few seconds and cost nothing."""
    if run.get("conclusion") in ("skipped",):
        return 0
    started, updated = run.get("run_started_at"), run.get("updated_at")
    if not started or not updated:
        return 0
    seconds = (_time(updated) - _time(started)).total_seconds()
    if run.get("status") != "completed":
        return max(1, math.ceil(seconds / 60))
    if seconds < 15 and run.get("conclusion") == "failure":
        return 0
    return max(1, math.ceil(seconds / 60)) if seconds > 0 else 0


def summarise(runs, now):
    """Minutes per workflow in the cycle, and the closing watcher's minutes today (UTC)."""
    total, closing_today, per = 0, 0, {}
    today = now.date()
    for r in runs:
        m = run_minutes(r)
        total += m
        name = r.get("name", "?")
        per[name] = per.get(name, 0) + m
        if r.get("path", "").endswith("closing.yml") and r.get("run_started_at") \
                and _time(r["run_started_at"]).date() == today:
            closing_today += m
    return total, closing_today, per


def fetch(repo, token, since, max_pages=10):
    """This repository's runs created since the cycle start, plus whether it is private."""
    info = _get(f"/repos/{repo}", token)
    runs = []
    for page in range(1, max_pages + 1):
        data = _get(f"/repos/{repo}/actions/runs?per_page=100&page={page}"
                    f"&created=%3E%3D{since:%Y-%m-%d}", token)
        batch = data.get("workflow_runs", [])
        runs.extend(batch)
        if len(batch) < 100:
            break
    return bool(info.get("private", True)), runs


def measure(config, path, now=None, repo=None, token=None, fetcher=fetch):
    """Measure and save the cycle's usage to path; returns the saved dict, or the last
    saved one (marked stale) when the API cannot be read."""
    now = now or datetime.now(timezone.utc)
    repo = repo or os.environ.get("GITHUB_REPOSITORY", "")
    token = token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    start = cycle_start(now, config.get("actions_cycle_day", 1))
    try:
        if not repo or not token:
            raise RuntimeError("no GitHub repository or token")
        private, runs = fetcher(repo, token, start)
        total, closing_today, per = summarise(runs, now)
        usage = {"measured": now.isoformat(timespec="seconds"), "private": private,
                 "cycle_start": start.date().isoformat(), "minutes": total,
                 "closing_today": closing_today, "day": now.date().isoformat(),
                 "per_workflow": per}
        path.write_text(json.dumps(usage, indent=2) + "\n")
        return usage
    except Exception as e:  # noqa: BLE001 - never stop a run over this
        usage = load(path)
        usage["stale"] = str(e)[:200]
        return usage


def load(path):
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return {}


def closing_allowance(config, usage, now=None):
    """Minutes the closing watcher may still spend today: None means no limit (public
    repository). In a private repository: the cycle's included minutes times a safety
    share, minus what is used, minus a daily reserve for the ticket run on each remaining
    day, spread evenly over the remaining days, minus what the watcher used today."""
    now = now or datetime.now(timezone.utc)
    if usage.get("private") is False:
        return None
    if not usage or usage.get("cycle_start") != cycle_start(
            now, config.get("actions_cycle_day", 1)).date().isoformat():
        return 0
    start = cycle_start(now, config.get("actions_cycle_day", 1))
    days_left = max(1, math.ceil((cycle_end(start) - now) / timedelta(days=1)))
    budget = config.get("actions_included_minutes", 2000) * config.get("actions_budget_share", 0.85)
    reserve = config.get("actions_daily_reserve_minutes", 45) * days_left
    spare = budget - usage.get("minutes", 0) - reserve
    if spare <= 0:
        return 0
    today_used = usage.get("closing_today", 0) if usage.get("day") == now.date().isoformat() else 0
    per_day = min(spare / days_left, config.get("actions_closing_max_per_day", 120))
    return max(0, int(per_day - today_used))


def summary_line(config, usage):
    """One line for the daily email, or "" when nothing was measured."""
    if not usage or "minutes" not in usage:
        return ""
    if usage.get("private") is False:
        return ("GitHub Actions: public repository, run time is free "
                f"({usage['minutes']} minutes this cycle).")
    included = config.get("actions_included_minutes", 2000)
    share = usage["minutes"] / included if included else 0
    text = (f"GitHub Actions: {usage['minutes']} of about {included} free minutes used "
            f"this month ({share:.0%}), private repository.")
    if share >= 0.75:
        text += (" Warning: when they run out GitHub stops every run, including this "
                 "email, until the next month. Making the repository public makes run time free.")
    return text
