#!/usr/bin/env python3
"""Styx Falls: a high bowl of black cliff, the oath village on its terrace,
and the south road switching back down a limestone scree slope.

Rows 24-29 meet Route 12 (Kyllene), so they use only the metatiles the two
secondaries share (0x200-0x2A7) and Aethos.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapedit import Layout  # noqa: E402
from paint import tufts  # noqa: E402
from autopath import lay, learn  # noqa: E402

rnd = random.Random(7)
m = Layout("StyxFalls")
PATH_IDS = set(range(0x200, 0x220))
table = learn(PATH_IDS, ["Route12_CypressRoad", "StyxFalls"])
table[(True,) * 8] = 0x200
table[(False,) * 4] = 0x201
path = {(x, y) for y in range(m.h) for x in range(m.w) if m.id(x, y) in PATH_IDS}

TOP, FACE, BASE = (0x2B3, 0x2B4, 0x2B5), (0x2A8, 0x2A9, 0x2AA), (0x2AD, 0x2AE, 0x2AF)

# --- the bowl: the back wall runs on east, then turns down the east side --
for x in range(27, 36):
    m.put(x, 6, rnd.choice(TOP), solid=True)
    for y in range(7, 12):
        m.put(x, y, rnd.choice(FACE), solid=True)
    m.put(x, 12, rnd.choice(FACE), solid=True)
# the pool's east shore stays open (x28-30); the east wall stands from x31
for y in range(12, 21):
    m.put(31, y, 0x2AC, solid=True)
    for x in range(32, 36):
        m.put(x, y, rnd.choice(FACE), solid=True)
m.put(31, 21, 0x2B1, solid=True)
for x in range(32, 36):
    m.put(x, 21, rnd.choice(BASE), solid=True)
# the corner where the back wall's foot meets the east wall
for x in (27, 28, 29, 30):
    m.put(x, 12, rnd.choice(BASE), solid=True)

# --- the oath village terrace ---------------------------------------------
# a dry-stone retaining wall under the Oath House, with steps down to the yard
for x, mid in zip(range(1, 7), (0x290, 0x291, 0x296, 0x291, 0x291, 0x292)):
    m.put(x, 15, mid, solid=(mid != 0x296))
# the plank fence by the stone house becomes dry stone too
for x, mid in zip(range(1, 5), (0x290, 0x291, 0x291, 0x292)):
    m.put(x, 18, mid, solid=True)

# --- the switchback down the scree (rows 24-29, x24-35) -------------------
# The road turns down at x30-31, cuts back west along row 25, drops at
# x25-26, runs east along row 27 and leaves south at x30-31. Between the two
# legs the slope breaks in a limestone band; its west half is a ledge, so the
# way back up is the long way and the way down can hop.
RUBBLE = (0x0D7, 0x0D7, 0x2A1, 0x29C, 0x29B, 0x001)
for y in range(24, 30):
    for x in range(24, 36):
        if x >= 32 and y < 25:
            continue                          # pines hold the slope's east shoulder
        path.discard((x, y))
        m.put(x, y, rnd.choice(RUBBLE), solid=True)
# the field wall runs along the top of the slope to where the road turns down
for x in range(12, 30):
    m.put(x, 24, 0x290 if x == 12 else 0x292 if x == 29 else 0x291, solid=True)
legs = [(30, 24), (31, 24)]
legs += [(x, 25) for x in range(25, 32)]
legs += [(25, 26), (26, 26)]
legs += [(x, 27) for x in range(25, 32)]
legs += [(x, y) for y in (28, 29) for x in (30, 31)]
path.update(legs)
for x, mid in zip(range(27, 31), (0x0D5, 0x087, 0x087, 0x0D6)):
    m.put(x, 26, mid, solid=True)
m.put(31, 26, 0x253, solid=True)
for x in range(32, 35):
    m.put(x, 26, 0x250 if x % 2 else 0x251, solid=True)
m.put(35, 26, 0x252, solid=True)
m.put(24, 26, 0x29D, solid=True)          # a boulder come down the scree

path.discard((19, 23))
lay(m, path, table, 0x200)
m.put(19, 23, 0x29D, solid=True)          # a boulder rolled against the wall narrows the road

# worn ground and pebbles across the bowl floor
tufts(m, (1, 13, 30, 23), variants=(0x002, 0x29B, 0x29C), share=0.12, seed=9)
m.save()
print("styx: done")
