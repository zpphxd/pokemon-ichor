#!/usr/bin/env python3
"""The Temple of Artemis grove: Kallisto's rock stands higher, the altar moves
from the forecourt's corner onto its axis, between the torches and before the
propylon gate, and the hedge between glades two and three becomes a ragged
sacred grove.

The hunt reads collision (src/ichor_hunt.c); hound rows (10, 11, 19, 25, 29,
32, 37) and the moonlit boxes are left as they were.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mapedit import Layout  # noqa: E402

m = Layout("Arkadia_TempleOfArtemis")
FACE, FACE2, FOOT = 0x314, 0x31F, 0x318

# --- Kallisto's rock: a three-row face with the stair cut into it ---------
for x in list(range(9, 14)) + list(range(16, 21)):
    m.put(x, 6, FACE if x % 2 else FACE2, solid=True)
for x in list(range(9, 13)) + list(range(16, 21)):
    m.put(x, 7, FOOT, solid=True)
# the cut's cheeks
m.put(13, 6, FACE2, solid=True)
m.put(16, 6, 0x315, solid=True)
m.put(16, 7, 0x319, solid=True)
# rubble fallen from the face lies at its foot, either side of the stair
for x in (10, 18):
    if m.id(x, 8) in (0x200, 0x201, 0x207):
        m.put(x, 8, 0x31C, solid=True)

# --- the altar stands on the axis, before the propylon --------------------
ALTAR = ((0x2F0, 0x2F1, 0x2F2), (0x2F8, 0x2F9, 0x2FA))
old = [(4, 45), (5, 45), (6, 45), (4, 46), (5, 46), (6, 46)]
for (x, y), mid in zip(old, (0x20E, 0x20E, 0x20E, 0x20A, 0x208, 0x20A)):
    m.put(x, y, mid, solid=False)
for j, row in enumerate(ALTAR):
    for i, mid in enumerate(row):
        m.put(13 + i, 46 + j, mid, solid=True)

# --- the hedge under glade three becomes a sacred grove --------------------
# cypresses stand in the hedge line and rise above it; bushes break its foot
for x in (10, 19, 25):
    m.put(x, 21, 0x2A1, solid=True)
    m.put(x, 22, 0x2A9, solid=True)
for x in (12, 16, 22):
    m.put(x, 20, 0x2DB, solid=True)
    m.put(x, 21, 0x2E3, solid=True)
for x, y, mid in ((14, 20, 0x2D0), (18, 20, 0x2D1), (24, 20, 0x2D2),
                  (19, 23, 0x2D1), (17, 23, 0x2D0)):
    m.put(x, y, mid, solid=True)

m.save()
print("artemis: done")
