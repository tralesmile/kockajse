"""Git merge driver for the bot's data files.

The daily run and the closing-price watcher both commit to main. When both touch the same
file (for example the daily run settles rows in shadow.csv while the watcher appends late
bets at its end), `git pull --rebase` used to stop with a conflict, the daily job failed
after the email had gone out, nothing was saved, and the next run picked a second ticket
(9 Nov 2026: two emails, ~30 extra Odds API credits, a day of search quota).

Registered by the workflows as
    git config merge.botdata.driver "python merge_data.py %O %A %B %P"
with `data/** merge=botdata` in .gitattributes. Git passes the common ancestor (%O), the
current version (%A, where the result must be written) and the other version (%B). During
`git pull --rebase` %A is the version already on GitHub and %B is the commit being
replayed (this run's own changes).

Rules, chosen so no recorded row is ever lost or duplicated:
- CSV: rows are matched by their identity columns. A row the replayed side changed (vs
  the ancestor) takes that version; otherwise the GitHub version. Rows new on either side
  are kept, GitHub's first, then the replayed side's new rows in their order. A row
  missing on one side is kept (the logs are append-only). Columns: union, new ones last.
- JSON: three-way merge per key; where both sides changed the same value, the replayed
  side wins.
- Anything else (generated reports, archives): the replayed side's version.
Exit 0 on success, 1 when a file cannot be parsed (git then reports a normal conflict).
"""

import csv
import io
import json
import sys
from pathlib import Path

KEYS = {
    "picks.csv": ["date", "event_id", "market", "sel", "point"],
    "shadow.csv": ["date", "strategy", "shadow_id", "event_id", "market", "sel", "point"],
    "closing.csv": ["date", "event_id", "market", "sel", "point", "source", "captured"],
    "ledger.csv": ["ticket_no"],
    "fallback_scores.csv": ["checked", "event_id"],
}


def read_csv(text):
    if not text.strip():
        return [], []
    reader = csv.DictReader(io.StringIO(text))
    return list(reader.fieldnames or []), list(reader)


def keyed(rows, cols):
    """{identity: row}; repeated identities get an occurrence number, in file order."""
    out, seen = {}, {}
    for r in rows:
        base = tuple(r.get(c, "") for c in cols)
        n = seen.get(base, 0)
        seen[base] = n + 1
        out[base + (n,)] = r
    return out


def merge_csv(name, base, cur, other):
    fo, o_rows = read_csv(base)
    fa, a_rows = read_csv(cur)
    fb, b_rows = read_csv(other)
    fields = list(fa)
    for f in fb + fo:
        if f not in fields:
            fields.append(f)
    cols = [c for c in KEYS.get(name, []) if c in fields] or fields[:1]
    o, a, b = keyed(o_rows, cols), keyed(a_rows, cols), keyed(b_rows, cols)
    out = []
    for k, row in a.items():
        if k in b and (k not in o or b[k] != o[k]):
            row = b[k]
        out.append(row)
    out += [row for k, row in b.items() if k not in a]
    buf = io.StringIO()
    ending = "\r\n" if "\r\n" in (cur or other) else "\n"
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore",
                            lineterminator=ending)
    writer.writeheader()
    for row in out:
        writer.writerow({f: row.get(f, "") for f in fields})
    return buf.getvalue()


_MISSING = object()


def merge_json_value(o, a, b):
    if a == b:
        return a
    if a == o:
        return b
    if b == o:
        return a
    if isinstance(a, dict) and isinstance(b, dict):
        o = o if isinstance(o, dict) else {}
        out = {}
        for k in list(a) + [k for k in b if k not in a]:
            va, vb, vo = a.get(k, _MISSING), b.get(k, _MISSING), o.get(k, _MISSING)
            if va is _MISSING:
                if vo is _MISSING or vb != vo:  # new on the replayed side, or changed there
                    out[k] = vb
                continue
            if vb is _MISSING:
                if vo is _MISSING or va != vo:
                    out[k] = va
                continue
            out[k] = merge_json_value(None if vo is _MISSING else vo, va, vb)
        return out
    return b


def merge_json(base, cur, other):
    o = json.loads(base) if base.strip() else {}
    merged = merge_json_value(o, json.loads(cur), json.loads(other))
    return json.dumps(merged, indent=2, ensure_ascii=False) + "\n"


def merge_text(path, base, cur, other):
    name = Path(path).name
    if name.endswith(".csv"):
        return merge_csv(name, base, cur, other)
    if name.endswith(".json"):
        return merge_json(base, cur, other)
    return other


def main(argv):
    base_path, cur_path, other_path = argv[1:4]
    path = argv[4] if len(argv) > 4 else cur_path
    try:
        if not (path.endswith(".csv") or path.endswith(".json")):
            Path(cur_path).write_bytes(Path(other_path).read_bytes())
            return 0
        def read(p):
            with open(p, encoding="utf-8", newline="") as fh:
                return fh.read()
        result = merge_text(path, read(base_path), read(cur_path), read(other_path))
    except Exception as exc:  # noqa: BLE001 - let git report a normal conflict
        print(f"merge_data: cannot merge {path}: {exc}", file=sys.stderr)
        return 1
    with open(cur_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
