#!/usr/bin/env python3
"""Arkadia: the crag over Pan's grotto, for "Noon in Arkadia" (WORLD_EXPLORATION §2).

A two-column outcrop of Arkadia's grey limestone stands out of the cypress stand
west of the grotto (x8-9, rows 10-12), a grass ledge on top of it (rows 8-9)
where Krotos's kid is stuck. Its east column is Pan's Crook's face, the first
one the player climbs: the face metatiles come from tools/ichor/art/crook_faces.py
(run it first). The kid and the reeds are events in data/maps/Arkadia/map.json.

Run after polish/arkadia.py. Idempotent: it only puts fixed cells.

Usage: /usr/bin/python3 tools/ichor/maps/polish/arkadia_crook.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "art"))
from mapedit import Layout  # noqa: E402
import crook_faces  # noqa: E402

ids = crook_faces.build("arkadia", crook_faces.FACES["arkadia"], check=True)
GRASS, SHADE = 0x001, 0x01C
m = Layout("Arkadia")
# the shade under the cypress stand, then the ledge
for x in (8, 9):
    m.put(x, 7, SHADE, solid=True, elev=0)
    m.put(x, 8, GRASS, solid=False, elev=3)
    m.put(x, 9, GRASS, solid=False, elev=3)
# the outcrop: its west column plain, its east column the Crook's face
for y, plain in ((10, 0x225), (11, 0x22D), (12, 0x235)):
    m.put(8, y, plain, solid=True, elev=0)
m.put(9, 10, ids["crook_top"], solid=True, elev=0)
m.put(9, 11, ids["crook_face"], solid=True, elev=0)
m.put(9, 12, ids["crook_foot"], solid=True, elev=0)
# open ground at its foot
m.put(8, 13, GRASS, solid=False, elev=3)
m.save()
print("arkadia_crook: the crag at x8-9, the face at (9, 10-12)")
