#!/usr/bin/env python3
"""Print the longest straight walkable/blocked edges of a map (map_style_audit's 'straight')."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mapdata import Map, Repo  # noqa: E402

m = Map(Repo(), sys.argv[1])
op = {(x, y) for y in range(m.h) for x in range(m.w) if m.open(x, y)}
blocked = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and (x, y) not in op  # noqa: E731
runs = []
for d in (-1, 1):
    for y in range(m.h):
        run = 0
        for x in range(m.w + 1):
            if x < m.w and (x, y) in op and blocked(x, y + d):
                run += 1
            else:
                if run >= 7:
                    runs.append((run, "row", y, x - run, x - 1, "above" if d < 0 else "below"))
                run = 0
    for x in range(m.w):
        run = 0
        for y in range(m.h + 1):
            if y < m.h and (x, y) in op and blocked(x + d, y):
                run += 1
            else:
                if run >= 7:
                    runs.append((run, "col", x, y - run, y - 1, "left" if d < 0 else "right"))
                run = 0
for r in sorted(runs, reverse=True)[:int(sys.argv[2]) if len(sys.argv) > 2 else 10]:
    print(r)
