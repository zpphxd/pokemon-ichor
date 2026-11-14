#!/usr/bin/env python3
"""Akti's two newer homes, laid out from the oikia room catalog.

Every house in a town is a home (design/MAP_DESIGN.md section 2), each with a
room of its own. As with Elaia's homes, the rooms are composed with
tools/ichor/art/oikia_build.py's own composer from the pieces in oikia_art.py,
without recompiling gTileset_Oikia: every cell a home uses must already be in
the tileset, and the build stops if one isn't. So the tileset, and every other
room's metatile ids, stay exactly as the art stream committed them.

  /usr/bin/python3 tools/ichor/maps/akti_homes.py     # also run by akti.py

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
    # Akti's sponge divers: Doris, Hydna's grandmother. A low cottage above the
    # beach, its back wall stepping in where the rock behind it does: nets and
    # sponge jars in the deep half, Hydna's water clock (she times her dives by
    # it) and the bed in the shallow half.
    "divers_house": {
        "title": "The divers' house, Akti",
        "map": "MAP_AKTI_TOWN_DIVERS_HOUSE",
        "layout": "AktiTown_DiversHouse",
        "floor": "flags",
        "wall": "blue",
        "grid": [
            "WWWWW####",
            "WWWWWWWWW",
            ".....WWWW",
            ".........",
            ".........",
            ".........",
            ".........",
        ],
        "rugs": [("blue", 2, 4, 3, 2)],
        "stamps": [
            ("nets", 0, 0),
            ("window", 2, 0),
            ("jar_shelf", 3, 0),
            ("herbs", 5, 1),
            ("klepsydra", 6, 1),
            ("window", 7, 1),
            ("pithos", 1, 3),
            ("fish_basket", 2, 3),
            ("fish_basket", 3, 3),
            ("table_round", 5, 5),
            ("stool", 6, 5),
            ("kline", 7, 5),
            ("amphora", 0, 5),
            ("knucklebones", 6, 6),
            ("mat", 3, 6),
        ],
        "spots": [
            ("warp", "door to Akti Town (south-arrow mat)", [(3, 6), (4, 6)]),
            ("npc", "Doris, Hydna's grandmother, by her sponge baskets", (4, 3), "south"),
            ("bg", "Hydna's water clock: she times her dives by it", (6, 2), (6, 3, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # Akti's goatherd: Aigon, whose goats keep the pen by the south gate. A
    # farmhouse kitchen round the hearth, wool and cheese pots, the milk pithos,
    # and a store cut off the corner; a kid wanders the floor.
    "goatherds_house": {
        "title": "The goatherd's farmhouse, Akti",
        "map": "MAP_AKTI_TOWN_GOATHERDS_HOUSE",
        "layout": "AktiTown_GoatherdsHouse",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "........###",
            "........###",
        ],
        "rugs": [("red", 4, 3, 4, 3)],
        "stamps": [
            ("soot", 1, 0),
            ("hearth", 1, 2),
            ("herbs", 3, 0),
            ("window", 4, 0),
            ("jar_shelf", 5, 0),
            ("window", 8, 0),
            ("niche", 9, 0),
            ("kalathos", 3, 2),
            ("kline", 8, 3),
            ("pithos", 10, 3),
            ("table", 5, 4),
            ("mortar", 3, 4),
            ("myrtle", 1, 5),
            ("mat", 3, 6),
        ],
        "spots": [
            ("warp", "door to Akti Town (south-arrow mat)", [(3, 6), (4, 6)]),
            ("npc", "Aigon the goatherd, at his hearth", (3, 3), "west"),
            ("npc", "a Skiddo kid, wandering (keep its range inside x 5-7, y 5-6)", (6, 5), "south"),
            ("bg", "hearth: \"A pot of goat's milk warms by the fire.\"", (1, 3), (1, 4, "north")),
        ],
    },
}


def new_cells():
    """The cells the homes need that gTileset_Oikia doesn't have, by home."""
    base = dict(R.ROOMS)
    base.update(R.catalog(A.STAMPS))
    composed = {n: B.compose(s) for n, s in base.items()}
    order0, _ = B.collect(composed)
    known = {B.cell_key(c) if hasattr(B, "cell_key") else None for c in order0}
    out = {}
    for name, spec in HOMES.items():
        cells = B.compose(spec)
        trial = dict(composed)
        trial[name] = cells
        order, _ = B.collect(trial)
        out[name] = len(order) - len(order0)
    return out, known


def build():
    base = dict(R.ROOMS)
    base.update(R.catalog(A.STAMPS))
    composed = {n: B.compose(s) for n, s in base.items()}
    order0, _ = B.collect(composed)
    homes = {n: B.compose(s) for n, s in HOMES.items()}
    composed.update(homes)
    order, ids = B.collect(composed)
    if len(order) != len(order0):
        per, _ = new_cells()
        raise SystemExit(f"akti_homes: the homes need {len(order) - len(order0)} cells gTileset_Oikia "
                         f"doesn't have ({per}); draw the pieces in oikia_art.py and rebuild the "
                         "tileset first")
    for name in R.ROOMS:                      # the ids are the committed tileset's
        committed = np.fromfile(ROOT / f"design/phase1/rooms/{name}.bin", "<u2")
        if not np.array_equal(B.blockdata(composed[name], ids[name]), committed):
            raise SystemExit(f"akti_homes: {name} no longer matches its committed blockdata; rebuild oikia first")
    for name, spec in HOMES.items():
        cells = homes[name]
        B.check_spots(name, spec, cells)
        h, w = len(cells), len(cells[0])
        blocks = B.blockdata(cells, ids[name])
        got = B.render_compiled(blocks, w, "gTileset_Aethos")
        if not np.array_equal(got, B.image_of(cells)):
            raise SystemExit(f"akti_homes: {name} doesn't render from the compiled tileset as composed")
        d = ROOT / "data/layouts" / spec["layout"]
        d.mkdir(parents=True, exist_ok=True)
        blocks.tofile(d / "map.bin")
        np.array([VOID] * 4, np.uint16).astype("<u2").tofile(d / "border.bin")
        B.save_scaled(got, ROOT / f"design/phase1/img/rooms_{name}.png", 3)
        print(f"akti_homes: {name} {w}x{h} -> data/layouts/{spec['layout']}, design/phase1/img/rooms_{name}.png")


if __name__ == "__main__":
    build()
