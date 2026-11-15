#!/usr/bin/env python3
"""Resolve append-versus-append merge conflicts in Ichor's registration lists.

Parallel branches each register new maps, so .gitignore, data/ichor_maps.inc
and data/maps/map_groups.json conflict on every merge. Keep both sides:
  - plain line files: ours, then theirs (lines theirs repeats are dropped);
  - map_groups.json: rebuilt from the merge's stage 2 (ours) and 3 (theirs):
    group_order and every group's list are ours plus theirs' new entries, so
    no map already on this branch changes its MAP_NUM.

  python3 tools/ichor/merge/union_lists.py FILE...
"""
import json
import re
import subprocess
import sys

CONFLICT = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)


def stage(n, path):
    return subprocess.run(["git", "show", f":{n}:{path}"], capture_output=True, text=True, check=True).stdout


def union_lines(text, dedupe):
    """Ours, then theirs. With dedupe (path lists such as .gitignore), drop
    non-blank lines theirs repeats; never in code or data, where repeated
    lines (blank lines, "Level: 15") are real."""
    def both(m):
        ours = m.group(1).splitlines(keepends=True)
        theirs = m.group(2).splitlines(keepends=True)
        if dedupe:
            seen = {l for l in ours if l.strip()}
            theirs = [l for l in theirs if l not in seen]
        return "".join(ours + theirs)
    return CONFLICT.sub(both, text)


def union_groups(path):
    """A three-way merge: what both sides removed stays removed (main's Hoenn
    cut), and what either side added is kept, ours first."""
    base, ours, theirs = (json.loads(stage(n, path)) for n in (1, 2, 3))
    out = {}
    for key in list(ours) + [k for k in theirs if k not in ours]:
        b, o, t = base.get(key), ours.get(key), theirs.get(key)
        if o is None or t is None:                 # added on one side, or removed on one
            if (o is None and b is not None) or (t is None and b is not None):
                continue                           # removed by a side: stays removed
            out[key] = o if o is not None else t
        elif isinstance(o, list):
            b = b or []
            keep = [v for v in o if v in t or v not in b]       # drop what theirs removed
            out[key] = keep + [v for v in t if v not in keep and v not in b]
        else:
            out[key] = t if o == b else o
    ordered = {"group_order": out.pop("group_order")}
    ordered.update(out)
    return json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"


def union_heals(path):
    """heal_locations.json: theirs, plus the entries ours added (by id)."""
    base, ours, theirs = (json.loads(stage(n, path)) for n in (1, 2, 3))
    key = next(k for k in theirs if isinstance(theirs[k], list))
    have = {h["id"] for h in theirs[key]}
    old = {h["id"] for h in base[key]}
    ours_by_id = {h["id"]: h for h in ours[key]}
    added = [h for h in ours[key] if h["id"] not in old and h["id"] not in have]
    merged = [ours_by_id.get(h["id"], h) if h["id"] in old else h for h in theirs[key]]
    out = dict(theirs)
    out[key] = merged + added
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


for path in sys.argv[1:]:
    if path.endswith("map_groups.json"):
        text = union_groups(path)
    elif path.endswith("heal_locations.json"):
        text = union_heals(path)
    else:
        with open(path) as f:
            text = union_lines(f.read(), path.endswith((".gitignore", "ichor_maps.inc")))
    if "<<<<<<<" in text:
        raise SystemExit(f"{path}: unresolved conflict left")
    with open(path, "w") as f:
        f.write(text)
    print(f"resolved {path}")
