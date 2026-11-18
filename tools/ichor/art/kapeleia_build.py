#!/usr/bin/env python3
"""Build gTileset_Kapeleia (the Great Deigma) and gTileset_Nysa (the Nursery of Nysa).

kapeleia is built exactly as limen is, by ergasteria_build.py's machinery
(compose the rooms, deduplicate the cells, compile with Porytiles, check every
room renders identically on oikos, aethos and building, write the layouts,
renders and docs). Both draw from kapeleia_art.py: limen's palettes and pieces
plus the market's stalls and the nursery's; the market needed a set to itself
(the stalls alone fill most of one), so the nursery has its own. The rooms are in
tools/ichor/maps/kapeleia_rooms.py, which also writes their events.

Usage: /usr/bin/python3 tools/ichor/art/kapeleia_build.py [--no-compile] [--preview DIR]
       (tools/ichor/maps/kapeleia_rooms.py builds this and writes the events)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import ergasteria_build as EB  # noqa: E402
import kapeleia_art as KA  # noqa: E402

KAPELEIA = EB.RoomSet(
    "kapeleia", "gTileset_Kapeleia", KA,
    tiles_doc=ROOT / "design/phase2/TILES_kapeleia.md",
    default_rooms_doc=ROOT / "design/maps/Kapeleia_rooms.md")

NYSA = EB.RoomSet(
    "nysa", "gTileset_Nysa", KA,
    tiles_doc=ROOT / "design/phase2/TILES_kapeleia.md",
    default_rooms_doc=ROOT / "design/maps/Kapeleia_rooms.md")


def main():
    args = EB.parse_args()
    EB.build(KAPELEIA, args)
    EB.build(NYSA, args)


if __name__ == "__main__":
    main()
