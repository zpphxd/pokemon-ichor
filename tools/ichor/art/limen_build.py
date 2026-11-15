#!/usr/bin/env python3
"""Build gTileset_Limen and gTileset_Domos, Emporion's interiors, and their rooms.

limen is built exactly as ergasteria is, by ergasteria_build.py's machinery
(compose the rooms, deduplicate the cells, compile with Porytiles, check every
room renders identically on oikos, aethos and building, write the layouts,
renders, docs and variant scripts). Only the sets differ: both draw from
limen_art.py; limen builds the harbor's rooms (the Deigma, the Dolphin, the
hiring hall, the widow's room) and domos the town's households and workshops
(Philoxenos's andron, the runners' house, Euphronios's workshop), the rooms in
tools/ichor/maps/emporion_rooms.py whose "set" names them. Seven rooms' pieces
didn't fit one secondary's 504 tiles. The tables go to
design/phase2/TILES_limen.md and ROOMS_emporion.md.

Usage: /usr/bin/python3 tools/ichor/art/limen_build.py [--no-compile] [--preview DIR]
       (tools/ichor/maps/emporion_rooms.py builds this and the other sets)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import ergasteria_build as EB  # noqa: E402
import limen_art as LA  # noqa: E402

LIMEN = EB.RoomSet(
    "limen", "gTileset_Limen", LA,
    tiles_doc=ROOT / "design/phase2/TILES_limen.md",
    default_rooms_doc=ROOT / "design/phase2/ROOMS_emporion.md")

# domos is limen's twin: the same art and palettes, for the town's households
# and workshops (Philoxenos's andron, the runners' barracks, Euphronios's
# workshop), because the seven rooms' pieces didn't fit one set's 504 tiles.
DOMOS = EB.RoomSet(
    "domos", "gTileset_Domos", LA,
    tiles_doc=ROOT / "design/phase2/TILES_limen.md",
    default_rooms_doc=ROOT / "design/phase2/ROOMS_emporion.md")


def main():
    args = EB.parse_args()
    EB.build(LIMEN, args)
    EB.build(DOMOS, args)


if __name__ == "__main__":
    main()
