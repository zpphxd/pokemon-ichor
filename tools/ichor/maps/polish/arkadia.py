#!/usr/bin/env python3
"""Arkadia: the temenos of Artemis, a dry-stone fold, scarps where the
roads end, and a real terrace step under the upper street.

The temple's facade stays south (the 3/4 view draws every building facing
the viewer); its precinct reads from its walls, its propylon columns at the
head of the stair, and the altar standing outside, across the road, on the
temple's axis.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapedit import Layout  # noqa: E402
from paint import tufts  # noqa: E402

rnd = random.Random(5)
m = Layout("Arkadia")
GRASS = 0x001
WALL_L, WALL_M, WALL_R, STAIR = 0x23A, 0x23B, 0x23C, 0x23D
LEDGE = 0x237           # the low wall as a ledge (clone_metatile.py: 0x23B, MB_JUMP_SOUTH)

# --- the terrace step under the upper street ----------------------------
# The row-12 wall already holds the upper street up with stairs at its gaps;
# two spans become a ledge, so the way down can be a hop.
for x in (20, 21, 22, 25, 26, 27):
    m.put(x, 12, LEDGE, solid=True)

# --- the temenos ----------------------------------------------------------
# north wall of the precinct, behind the podium (row 22, x15-22)
for x in range(15, 23):
    m.put(x, 22, WALL_L if x == 15 else WALL_R if x == 22 else WALL_M, solid=True)
# propylon: a column each side of the stair head
for x in (18, 22):
    m.put(x, 32, 0x058, solid=True)
    m.put(x, 33, 0x060, solid=True)
# the altar outside, across the road on the temple's axis, with offerings
m.put(20, 36, 0x131, solid=True)
for x, y in ((19, 36), (21, 36), (19, 37), (21, 37)):
    m.put(x, y, 0x004, solid=False)

# --- the shepherds' fold (x35-40, rows 31-36): dry stone, not planks -------
for x in range(35, 41):
    top = {35: WALL_L, 36: WALL_M, 37: WALL_R, 38: None, 39: WALL_L, 40: WALL_R}[x]
    if top is None:
        m.put(x, 31, GRASS, solid=False)       # the fold's gate
    else:
        m.put(x, 31, top, solid=True)
    m.put(x, 36, WALL_L if x == 35 else WALL_R if x == 40 else WALL_M, solid=True)
for y in range(32, 36):
    for x in (35, 40):
        m.put(x, y, 0x0E0, solid=True)         # piled stone sides

# --- scarps where the roads end -------------------------------------------
# West road (rows 36-37) ends at x2: a limestone mass x0-1, rows 33-40,
# scree at its foot. Iapetos still steps out from the cypress at its edge.
WEST = {33: (0x083, 0x084), 34: (0x08B, 0x08C), 35: (0x08B, 0x08C), 36: (0x08B, 0x08C),
        37: (0x08B, 0x08C), 38: (0x08B, 0x08C), 39: (0x093, 0x094)}
for y, (a, b) in WEST.items():
    m.put(0, y, a, solid=True)
    m.put(1, y, b, solid=True)
for x, y in ((2, 35), (2, 38), (2, 39)):
    m.put(x, y, 0x0D7, solid=True)
# South road ends at row 41: two rock outcrops (x12-15, rows 42-43) and scree
for x in (12, 14):
    m.put(x, 42, 0x083, solid=True)
    m.put(x + 1, 42, 0x084, solid=True)
    m.put(x, 43, 0x093, solid=True)
    m.put(x + 1, 43, 0x094, solid=True)
for x, y in ((12, 41), (15, 41), (16, 42)):
    m.put(x, y, 0x0D7, solid=True)

# --- the woods: dense cypress instead of a checkerboard --------------------
# Every solid tree cell of the woods becomes part of a cypress stand: each
# column of a run is a stack of cypresses (00E over 016, the stack's tops
# stepping with the run's shape), with a stone pine or an olive dropped in
# where a 2x2 or 2x3 block fits, for variety. Aethos only, so the seams with
# Route 12 and Route 13 match.
TREES = {0x00E, 0x016, 0x01E, 0x01F, 0x026, 0x027, 0x1CE, 0x1CF, 0x1D4, 0x1D5, 0x1DC, 0x1DD,
         0x1E4, 0x1E5, 0x01C}
wood = {(x, y) for y in range(m.h) for x in range(m.w) if m.id(x, y) in TREES and m.solid(x, y)}
done = set()
# variety first: stone pines (2x2) and olives (2x3) in the deep wood
for y in range(m.h - 2):
    for x in range(m.w - 1):
        if rnd.random() > 0.05:
            continue
        olive = rnd.random() < 0.5 and y + 2 < m.h
        cells = [(x + i, y + j) for i in (0, 1) for j in range(3 if olive else 2)]
        ring = [(x + i, y + j) for i in (-1, 0, 1, 2) for j in range(-1, 4 if olive else 3)]
        if not all(c in wood and c not in done for c in cells):
            continue
        if sum(c in wood for c in ring) < len(ring) - 2:
            continue                                   # only well inside the wood
        rows = [(0x1CE, 0x1CF), (0x1D4, 0x1D5), (0x1E4, 0x1E5)] if olive else [(0x01E, 0x01F), (0x026, 0x027)]
        for j, (a, b) in enumerate(rows):
            m.put(x, y + j, a, solid=True)
            m.put(x + 1, y + j, b, solid=True)
        done.update(cells)
# then cypress stacks down every column
for x in range(m.w):
    y = 0
    while y < m.h:
        if (x, y) in wood and (x, y) not in done:
            k = y
            while (x, k + 1) in wood and (x, k + 1) not in done:
                k += 1
            n = k - y + 1
            start = y
            if n % 2:
                if y == 0:
                    m.put(x, 0, 0x016, solid=True)     # a trunk whose top is off the map
                else:
                    m.put(x, y, 0x01C, solid=True)     # shade under the stand
                start = y + 1
            for t in range(start, k + 1):
                m.put(x, t, 0x00E if (t - start) % 2 == 0 else 0x016, solid=True)
            y = k + 1
        else:
            y += 1

m.save()
print("arkadia: done")
