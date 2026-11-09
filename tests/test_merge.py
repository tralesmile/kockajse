"""Tests for merge_data.py, the merge driver that lets the daily run and the closing watcher
commit to main at the same time (9 Nov 2026: the daily job failed on a rebase conflict in
data/actions_usage.json after the email was sent, so the ticket was picked twice)."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import merge_data  # noqa: E402

H = "date,strategy,shadow_id,event_id,market,sel,point,odds,result\r\n"


def row(i, result="pending", strategy="market"):
    return f"2026-11-08,{strategy},s{i},e{i},h2h,A,,1.5,{result}\r\n"


def test_csv_settle_and_append():
    base = H + row(1) + row(2)
    gh = H + row(1) + row(2) + row(3, strategy="late_power")       # watcher appended
    mine = H + row(1, "won") + row(2, "lost") + row(4, strategy="single")  # daily settled + new
    out = merge_data.merge_csv("shadow.csv", base, gh, mine)
    assert out == H + row(1, "won") + row(2, "lost") + row(3, strategy="late_power") \
        + row(4, strategy="single"), out
    # the other way round (watcher's commit replayed onto the daily's): same rows
    out2 = merge_data.merge_csv("shadow.csv", base, mine, gh)
    assert sorted(out2.splitlines()) == sorted(out.splitlines())


def test_csv_github_side_change_kept_and_no_row_dropped():
    base = H + row(1) + row(2)
    gh = H + row(1, "won") + row(2)       # settled on GitHub's side
    mine = H + row(1)                       # replayed side lost row 2 (must not drop it)
    out = merge_data.merge_csv("shadow.csv", base, gh, mine)
    assert out == H + row(1, "won") + row(2), out


def test_csv_new_column():
    base = "ticket_no,date\n1,2026-11-01\n"
    gh = "ticket_no,date\n1,2026-11-01\n2,2026-11-02\n"
    mine = "ticket_no,date,mode\n1,2026-11-01,paper\n"
    out = merge_data.merge_csv("ledger.csv", base, gh, mine)
    assert out == "ticket_no,date,mode\n1,2026-11-01,paper\n2,2026-11-02,\n", out


def test_json_three_way():
    o = {"cycle": {"used": 10, "watcher": 5}, "day": "08"}
    a = {"cycle": {"used": 12, "watcher": 7}, "day": "08", "gh_only": 1}
    b = {"cycle": {"used": 11, "watcher": 5}, "day": "09"}
    out = json.loads(merge_data.merge_json(json.dumps(o), json.dumps(a), json.dumps(b)))
    # used changed on both sides -> replayed side; watcher only on GitHub's -> GitHub's
    assert out == {"cycle": {"used": 11, "watcher": 7}, "day": "09", "gh_only": 1}, out


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout


def test_real_rebase():
    """The 9 Nov race end to end: both sides change shadow.csv and actions_usage.json,
    then `git pull --rebase` with the driver configured as the workflows do."""
    if not shutil.which("git"):
        print("git missing, skipped")
        return
    tmp = Path(tempfile.mkdtemp())
    try:
        origin, a, b = tmp / "origin.git", tmp / "watcher", tmp / "daily"
        git(tmp, "init", "-q", "--bare", "-b", "main", str(origin))
        git(tmp, "clone", "-q", str(origin), str(a))
        for repo in (a,):
            git(repo, "config", "user.name", "t")
            git(repo, "config", "user.email", "t@t")
        (a / "data").mkdir()
        shutil.copy(ROOT / "merge_data.py", a / "merge_data.py")
        (a / ".gitattributes").write_text((ROOT / ".gitattributes").read_text())
        (a / "data" / "shadow.csv").write_bytes((H + row(1) + row(2)).encode())
        (a / "data" / "actions_usage.json").write_text(json.dumps({"used": 1, "x": 0}, indent=2))
        git(a, "add", "-A")
        git(a, "commit", "-q", "-m", "base")
        git(a, "push", "-q", "origin", "main")
        git(tmp, "clone", "-q", str(origin), str(b))
        for repo in (a, b):
            git(repo, "config", "user.name", "t")
            git(repo, "config", "user.email", "t@t")
            git(repo, "config", "merge.botdata.driver",
                f"{sys.executable} merge_data.py %O %A %B %P")
        # watcher: append a late bet, bump usage; pushes first
        (a / "data" / "shadow.csv").write_bytes(
            (H + row(1) + row(2) + row(3, strategy="late_power")).encode())
        (a / "data" / "actions_usage.json").write_text(json.dumps({"used": 2, "x": 0}, indent=2))
        git(a, "commit", "-qam", "watcher")
        git(a, "push", "-q", "origin", "main")
        # daily: settles both rows, adds one, bumps usage differently
        (b / "data" / "shadow.csv").write_bytes(
            (H + row(1, "won") + row(2, "lost") + row(4, strategy="single")).encode())
        (b / "data" / "actions_usage.json").write_text(json.dumps({"used": 3, "x": 1}, indent=2))
        git(b, "commit", "-qam", "daily")
        git(b, "pull", "-q", "--rebase")
        git(b, "push", "-q", "origin", "main")
        got = (b / "data" / "shadow.csv").read_bytes().decode()
        assert got == H + row(1, "won") + row(2, "lost") + row(3, strategy="late_power") \
            + row(4, strategy="single"), got
        assert json.loads((b / "data" / "actions_usage.json").read_text()) == {"used": 3, "x": 1}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
    print("All merge tests passed.")
