#!/usr/bin/env python3
"""Route 12, the Cypress Road: switchbacks, a ford, the north cut, the fold.

- The west trail now switches back across its two terraces: lower stairs at
  x6-7, upper stairs at x1-2, and the upper terrace edge is a ledge, so the
  way down is a hop (MAP_DESIGN.md: ledges drop toward the previous town).
- A herm stands at the fork where the north trail meets the east path.
- The north trail climbs through a limestone cut with its west wall's shadow.
- The dead-end west meadow is a shepherd's fold of piled stone with a beehive
  hut (kalyvi) and its hearth.
- A seasonal stream runs along the foot of the scarp (rows 29-30); the road
  fords it below the stairs.
- The southern tree row becomes ragged groves (Aethos only: Arkadia's seam).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapedit import Layout  # noqa: E402
from paint import paint  # noqa: E402
from autopath import lay, learn  # noqa: E402
from seams import route12_north  # noqa: E402

m = Layout("Route12_CypressRoad")
PATH_IDS = set(range(0x200, 0x220))
table = learn(PATH_IDS, ["Route12_CypressRoad", "StyxFalls"])
table[(True,) * 8] = 0x200
table[(False,) * 4] = 0x201
path = {(x, y) for y in range(m.h) for x in range(m.w) if m.id(x, y) in PATH_IDS}

# --- the west switchback ------------------------------------------------
GRASS, TALL = 0x001, 0x00D
for y in list(range(9, 12)) + [13]:
    for x in (6, 7):
        path.discard((x, y))
        m.put(x, y, GRASS, solid=False)
# the upper terrace edge: a ledge from x3 to x7; stairs move to x1-2
m.put(1, 12, 0x296, solid=False)
m.put(2, 12, 0x296, solid=False)
for x, mid in zip(range(3, 8), (0x0D5, 0x087, 0x087, 0x087, 0x0D6)):
    m.put(x, 12, mid, solid=True)
m.put(5, 13, GRASS, solid=False)
# path: x1-7 along rows 8-9, down x1-2 to the stairs, x1-2 to row 15,
# east along rows 14-15, down x6-7 to the lower stairs
new = [(x, y) for y in (8, 9) for x in range(1, 8)]
new += [(x, y) for y in (10, 11, 13) for x in (1, 2)]
new += [(x, y) for y in (14, 15) for x in range(1, 8)]
new += [(x, y) for y in (16, 17) for x in (6, 7)]
for c in new:
    path.add(c)
# a few tufts where the old trail ran
for x, y in ((6, 10), (7, 11)):
    m.put(x, y, 0x29B, solid=False)

# a fallen block from the terrace wall, so the wall's foot isn't one straight run
m.put(15, 11, 0x2E9, solid=True)

# herm at the fork, on the grass in its north-east corner
m.put(8, 7, 0x298, solid=True)

# --- the north cut --------------------------------------------------------
# west wall (x4-5) ends at the trail, east wall (x8-9) starts after it
CUT = {(2, 1): 0x24E, (3, 1): 0x24B, (4, 1): 0x24C, (5, 1): 0x24D,
       (2, 2): 0x249, (3, 2): 0x245, (4, 2): 0x242, (5, 2): 0x248,
       (8, 1): 0x24E, (9, 1): 0x24C, (10, 1): 0x24B, (11, 1): 0x24D,
       (8, 2): 0x249, (9, 2): 0x241, (10, 2): 0x245, (11, 2): 0x248}
for (x, y), mid in CUT.items():
    m.put(x, y, mid, solid=True)
for x in (2, 3, 4, 5, 8, 9, 10, 11):     # the scarp's top: scrubby ground, no floating pine tips
    m.put(x, 0, 0x01C, solid=True)
# the west wall's shadow falls across the trail's west half
for y in range(1, 4):
    path.discard((6, y))
    m.put(6, y, 0x01C, solid=False)

# --- the shepherd's fold (x1-5, rows 20-25) -------------------------------
for x, mid in zip(range(1, 5), (0x290, 0x291, 0x291, 0x292)):
    m.put(x, 25, mid, solid=True)
# the north wall leaves a gap at x4, so the hop down the lower ledge lands in the fold
for x, mid in zip(range(1, 4), (0x290, 0x291, 0x292)):
    m.put(x, 20, mid, solid=True)
m.put(5, 24, 0x2E9, solid=True)          # piled stone; the gate is rows 22-23
m.put(5, 20, 0x2E8, solid=True)
for y in range(20, 25):
    for x in range(1, 5):
        if y == 20 and x < 4:
            continue
        m.put(x, y, TALL, solid=False)
# beehive hut and its hearth
for (x, y), mid in {(8, 24): 0x2F5, (9, 24): 0x2F6, (8, 25): 0x2FD, (9, 25): 0x2FE}.items():
    m.put(x, y, mid, solid=True)
m.put(7, 25, 0x2EC, solid=True)
m.put(7, 24, GRASS, solid=False)
m.put(6, 24, GRASS, solid=False)
m.put(6, 25, 0x29C, solid=False)
for c in [(6, y) for y in range(20, 24)] + [(7, y) for y in range(20, 24)]:
    path.add(c)
path.update({(5, 22), (5, 23)})

# --- the stream and the ford (rows 29-30, x26-41) -------------------------
# The road crosses on a paved ford: the road's own cells stay road, and the
# water meets them with banks either side. (Puddle cells under the road
# would splash, and the splash draws on the RNG the route's tests replay.)
for x in range(26, 42):
    if x in (29, 30):
        continue
    left, right = x == 31, x == 28
    top = 0x0C8 if left else 0x0CA if right else 0x0C9
    bot = 0x0D8 if left else 0x0DA if right else 0x0D9
    m.put(x, 29, top, solid=True)
    m.put(x, 30, bot, solid=True)

lay(m, path, table, 0x200)

# --- the southern groves (rows 30/31-35, Aethos only) ---------------------
# x0-25 rows 30-35, x26-27 and x32-41 rows 31-35, x42-55 rows 30-35.
WEST = [
    "PPOOOOc,OOOOPPOOOOc.OO..,,",  # 30
    "PPOOOOc;OOOOPPOOOOc.OO....",  # 31
    "OOOOOO,,OOOOOOOOOO..OO:..f",  # 32
    "OOOOOOPPOOOOOOOO,,c.......",  # 33
    "OOOOOOPPOOOOOOOOOOc.OO..c.",  # 34
    "OOOOOOOOOOOOOOOOOOOOOO..c.",  # 35
]
paint(m, 0, 30, WEST, seed=31)
MID = [
    # x26-27 | road x28-31 | x32-41
    "..====..:...c.,.",  # 31
    "f.====......c,OO",  # 32
    "..====.f....OOOO",  # 33
    "c.====..OO..OOOO",  # 34
    "c.====..OO..OOOO",  # 35
]
paint(m, 26, 31, MID, seed=32)
EAST = [
    "OO,,OOOOPPPPOO",  # 30
    "OO,,OOOOPPPPOO",  # 31
    "OOc,OOOO,cOOOO",  # 32
    "OOc,OOOO,cOOOO",  # 33
    "OOOOOOOOOOOOOO",  # 34
    "OOOOOOOOOOOOOO",  # 35
]
paint(m, 42, 30, EAST, seed=33)
# The cypress wall under the meadow (rows 19-20): a few trees stand taller,
# so its top edge steps instead of running 19 cells straight.
for x in (39, 40, 43, 48):
    m.put(x, 17, 0x267, solid=False)
    m.put(x, 18, 0x284, solid=True)
    m.put(x, 19, 0x28C, solid=True)

# a stone pine where the stream slips in under the west wood
for (x, y), mid in {(24, 29): 0x01E, (25, 29): 0x01F, (24, 30): 0x026, (25, 30): 0x027}.items():
    m.put(x, y, mid, solid=True)
route12_north(m)                       # the seam strip, Aethos only (seams.py)
m.save()
print("route12: done")
