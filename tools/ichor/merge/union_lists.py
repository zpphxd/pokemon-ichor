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


def union_lines(text):
    def both(m):
        ours = m.group(1).splitlines(keepends=True)
        seen = set(ours)
        return "".join(ours + [l for l in m.group(2).splitlines(keepends=True) if l not in seen])
    return CONFLICT.sub(both, text)


def union_groups(path):
    ours, theirs = json.loads(stage(2, path)), json.loads(stage(3, path))
    out = dict(ours)
    for key, val in theirs.items():
        if key not in out:
            out[key] = val
        elif isinstance(val, list):
            out[key] = out[key] + [v for v in val if v not in out[key]]
    # keep group_order's keys in front, as the file has them
    ordered = {"group_order": out.pop("group_order")}
    ordered.update(out)
    return json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"


for path in sys.argv[1:]:
    if path.endswith("map_groups.json"):
        text = union_groups(path)
    else:
        with open(path) as f:
            text = union_lines(f.read())
    if "<<<<<<<" in text:
        raise SystemExit(f"{path}: unresolved conflict left")
    with open(path, "w") as f:
        f.write(text)
    print(f"resolved {path}")
