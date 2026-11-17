#!/usr/bin/env python3
"""BFS on foot between two cells of a map (people who never move are walls).

  reach.py ThyrsaCity 39 36 39 11
"""
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mapdata import Map, Repo  # noqa: E402

m = Map(Repo(), sys.argv[1])
sx, sy, tx, ty = map(int, sys.argv[2:6])
people = {(o["x"], o["y"]) for o in m.json.get("object_events", [])
          if "WANDER" not in o.get("movement_type", "") and "WALK" not in o.get("movement_type", "")}
seen = {(sx, sy): None}
q = deque([(sx, sy)])
while q:
    x, y = q.popleft()
    if (x, y) == (tx, ty):
        break
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        n = (x + dx, y + dy)
        if n in seen or not (0 <= n[0] < m.w and 0 <= n[1] < m.h):
            continue
        if n != (tx, ty) and (not m.open(*n) or n in people):
            continue
        seen[n] = (x, y)
        q.append(n)
if (tx, ty) in seen:
    path, c = [], (tx, ty)
    while c:
        path.append(c)
        c = seen[c]
    print("reachable in", len(path) - 1, "steps:", path[::-1])
else:
    far = sorted(seen, key=lambda c: abs(c[0] - tx) + abs(c[1] - ty))[:5]
    print("NOT reachable; closest reached:", far)
