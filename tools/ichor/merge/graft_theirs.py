#!/usr/bin/env python3
"""Resolve append-versus-append conflicts by grafting theirs' insertions onto ours.

When both sides append entries at the same anchor (before "// End of Ichor
object events", at the end of a tileset table), git's conflict hunks can
interleave the two sides' structs. This rebuilds the file from the merge's
stages instead: ours (stage 2), plus every block theirs (stage 3) inserted
into the base (stage 1), placed after ours' own insertion at that anchor.
It refuses files where theirs changed or deleted base lines.

  python3 tools/ichor/merge/graft_theirs.py FILE...
"""
import difflib
import subprocess
import sys


def stage(n, path):
    return subprocess.run(["git", "show", f":{n}:{path}"], capture_output=True,
                          text=True, check=True).stdout.splitlines(keepends=True)


def graft(path):
    base, ours, theirs = stage(1, path), stage(2, path), stage(3, path)
    inserts = []  # (base index to insert before, lines)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, theirs, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag != "insert":
            raise ValueError(f"{path}: theirs {tag}s base lines {i1}-{i2}; resolve by hand")
        inserts.append((i1, theirs[j1:j2]))
    # map each base index to the ours index of the same line
    base_to_ours = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, ours, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                base_to_ours[i1 + k] = j1 + k
    out = list(ours)
    for i, lines in sorted(inserts, reverse=True):
        at = base_to_ours.get(i, len(ours)) if i < len(base) else len(ours)
        if i < len(base) and i not in base_to_ours:
            raise ValueError(f"{path}: ours changed the anchor line {i}; resolve by hand")
        out[at:at] = lines
    with open(path, "w") as f:
        f.writelines(out)
    print(f"{path}: grafted {len(inserts)} block(s), {sum(len(l) for _, l in inserts)} lines")


failed = 0
for p in sys.argv[1:]:
    try:
        graft(p)
    except ValueError as e:
        print(e)
        failed = 1
sys.exit(failed)
