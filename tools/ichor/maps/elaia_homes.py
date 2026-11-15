#!/usr/bin/env python3
"""Elaia's other homes, laid out from the oikia room catalog.

Every house in a town is a home (design/MAP_DESIGN.md section 2), each with a
room of its own. The rooms are composed with tools/ichor/art/oikia_build.py's
own composer, from the pieces in oikia_art.py, but without recompiling
gTileset_Oikia: every cell a home uses must already be in the tileset, and the
build stops if one isn't. So the tileset, and every other room's metatile ids,
stay exactly as the art stream committed them. A home that needs a new piece
means asking for it to be drawn.

  /usr/bin/python3 tools/ichor/maps/elaia_homes.py     # also run by elaia.py

Writes data/layouts/<Map>/{map,border}.bin and design/phase1/img/rooms_<home>.png
(3x) for each home, after checking that:
  - no home cell is new to the tileset, and the committed rooms' ids still match,
  - each home renders from the compiled tileset exactly as it was composed,
  - every warp, person and readable thing is reachable (oikia_build's spot check).
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))

import oikia_art as A  # noqa: E402
import oikia_build as B  # noqa: E402
import oikia_rooms as R  # noqa: E402

VOID = 0x0210   # oikia's near-black void, the rooms' border

# The grid, rugs, stamps and spots follow oikia_rooms.py's format.
HOMES = {
    # ------------------------------------------------------------------
    # Glykera bakes the Klotheia's honey cakes; her stall stands in the square.
    # Her father Kimon pulled an oar on the war triremes for forty years and
    # keeps his corner by the window with his oars and a model ship. An L-shaped
    # room: the bakery runs deep on the left, and Kimon's nook is a shallower
    # bay on the right, under its own stretch of wall.
    "bakers_house": {
        "title": "Glykera's house, Elaia: the honey-cake bakery and Kimon's nook",
        "map": "MAP_ELAIA_VILLAGE_BAKERS_HOUSE",
        "layout": "ElaiaVillage_BakersHouse",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWW####",
            "WWWWWWW####",
            ".......WWWW",
            ".......WWWW",
            "...........",
            "...........",
            "...........",
            "...........",
        ],
        "rugs": [("blue", 7, 5, 3, 2)],
        "stamps": [
            ("honey_shelf", 0, 0),
            ("soot", 2, 0),
            ("window", 4, 0),
            ("jar_shelf", 5, 0),
            ("kalathos", 1, 2),
            ("hearth", 2, 2),
            ("pots", 4, 2),
            ("pithos", 6, 3),
            ("boat", 7, 2),
            ("window", 9, 2),
            ("oars", 10, 2),
            ("amphora", 0, 5),
            ("stool", 1, 5),
            ("table", 2, 5),
            ("stool", 4, 5),
            ("mortar", 4, 6),
            ("klismos_l", 10, 5),
            ("amphora_plain", 10, 6),
            ("mat", 6, 7),
        ],
        "spots": [
            ("warp", "door to Elaia Village (south-arrow mat)", [(6, 7), (7, 7)]),
            ("npc", "Glykera, beside her oven", (1, 3), "south"),
            ("npc", "Kimon, by his chair under the window", (9, 5), "south"),
            ("bg", "the oven (the hearth), right half", (3, 3), (3, 4, "north")),
            ("bg", "honey shelf", (0, 1), (0, 2, "north")),
            ("bg", "the grain jar (pithos)", (6, 4), (6, 5, "north")),
            ("bg", "Kimon's model trireme", (7, 3), (7, 4, "north")),
            ("bg", "Kimon's model trireme, right half", (8, 3), (8, 4, "north")),
            ("bg", "Kimon's window", (9, 3), (9, 4, "north")),
        ],
    },
}


def build():
    base = dict(R.ROOMS)
    base.update(R.catalog(A.STAMPS))
    composed = {n: B.compose(s) for n, s in base.items()}
    order0, _ = B.collect(composed)
    homes = {n: B.compose(s) for n, s in HOMES.items()}
    composed.update(homes)
    order, ids = B.collect(composed)
    if len(order) != len(order0):
        raise SystemExit(f"elaia_homes: the homes need {len(order) - len(order0)} cells gTileset_Oikia doesn't"
                         " have; draw the pieces in oikia_art.py and rebuild the tileset first")
    for name in R.ROOMS:                      # the ids are the committed tileset's
        committed = np.fromfile(ROOT / f"design/phase1/rooms/{name}.bin", "<u2")
        if not np.array_equal(B.blockdata(composed[name], ids[name]), committed):
            raise SystemExit(f"elaia_homes: {name} no longer matches its committed blockdata; rebuild oikia first")
    for name, spec in HOMES.items():
        cells = homes[name]
        B.check_spots(name, spec, cells)
        h, w = len(cells), len(cells[0])
        blocks = B.blockdata(cells, ids[name])
        got = B.render_compiled(blocks, w, "gTileset_Aethos")
        if not np.array_equal(got, B.image_of(cells)):
            raise SystemExit(f"elaia_homes: {name} doesn't render from the compiled tileset as composed")
        d = ROOT / "data/layouts" / spec["layout"]
        d.mkdir(parents=True, exist_ok=True)
        blocks.tofile(d / "map.bin")
        np.array([VOID] * 4, np.uint16).astype("<u2").tofile(d / "border.bin")
        B.save_scaled(got, ROOT / f"design/phase1/img/rooms_{name}.png", 3)
        print(f"elaia_homes: {name} {w}x{h} -> data/layouts/{spec['layout']}, design/phase1/img/rooms_{name}.png")


if __name__ == "__main__":
    build()
