#!/usr/bin/env python3
"""Resolve the shared-table conflicts when merging an Oikoumene agent's branch (BUILD.md §8).

Run during a conflicted `git merge`:
  python3 tools/ichor/oikoumene_merge.py union FILE...   ours, plus every hunk theirs added, appended at the end
                                                         (tileset and object-event registration files, trainers.party)
  python3 tools/ichor/oikoumene_merge.py wild            wild_encounters.json: ours, plus theirs' new entries by base_label
  python3 tools/ichor/oikoumene_merge.py both FILE...    keep both sides of each conflict block, ours first (flags.h,
                                                         trade.h, event_objects.h, specials.inc); then check the seams by hand

Plain keep-both breaks files where both sides append after the same closing lines (`};`, `.callback = NULL,`):
git puts the shared tail after the conflict, so one side's block loses its end. `union` avoids that.
Afterwards keep one TRAINERS_END_OIKOUMENE line in opponents.h, the highest, and drop FLAG_UNUSED_ lines theirs claimed.
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True).stdout


def union(files):
    base = sh("git", "merge-base", "HEAD", "MERGE_HEAD").strip()
    for f in files:
        ours = sh("git", "show", f"HEAD:{f}")
        hunks, cur = [], None
        for line in sh("git", "diff", "-U0", base, "MERGE_HEAD", "--", f).splitlines():
            if line.startswith("@@"):
                cur = []
                hunks.append(cur)
            elif cur is not None and line.startswith("+") and not line.startswith("+++"):
                cur.append(line[1:])
            elif cur is not None and line.startswith("-") and not line.startswith("---"):
                print(f"{f}: theirs also removes a line, check by hand: {line[:70]}")
        added = "\n".join("\n".join(h) for h in hunks if h)
        Path(f).write_text(ours.rstrip("\n") + "\n" + added + "\n")
        print(f, len(hunks), "hunk(s) appended")


def wild():
    f = "src/data/wild_encounters.json"
    ours, theirs = (json.loads(sh("git", "show", f"{r}:{f}")) for r in ("HEAD", "MERGE_HEAD"))
    og, tg = ours["wild_encounter_groups"][0], theirs["wild_encounter_groups"][0]
    have = {e["base_label"] for e in og["encounters"]}
    new = [e for e in tg["encounters"] if e["base_label"] not in have]
    og["encounters"].extend(new)
    Path(f).write_text(json.dumps(ours, indent=2, ensure_ascii=False) + "\n")
    print(len(new), "encounter entries added")


def both(files):
    for f in files:
        p = Path(f)
        t = p.read_text()
        n = len(re.findall(r"^<<<<<<< ", t, flags=re.M))
        t = re.sub(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", lambda m: m.group(1) + m.group(2),
                   t, flags=re.S | re.M)
        p.write_text(t)
        print(f, n, "block(s) kept both")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"union": lambda: union(args), "wild": wild, "both": lambda: both(args)}[cmd]()
