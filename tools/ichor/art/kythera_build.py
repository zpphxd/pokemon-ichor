#!/usr/bin/env python3
"""Draw, compile, register and catalog Act III's Kythera secondaries.

Kythera Isle and Melos have more distinct pieces than one secondary's 504
tiles can hold, so they are split by map, as Emerald gives each town its own:

  kythera   Skandeia and the Foam Road: the harbor, the coast, the quarry
  paphia    Paphia: the temple town, its stair, houses, dovecotes, jetty
  neraida   the Neraida falls and the Spring of Kallirhoe: falls, pools, mills
  melos     Melos, the sea of Routes 22 and 23, Antikythera, Echo's sea caves

All pair with the aethos primary. They share painters (kythera_coast, _land,
_harbor, _town, _water, melos_art), so a piece two of them need is drawn once
and looks the same in both. For each tileset:

1. Paints its structures, checks each 8x8 tile (over every animation frame)
   draws from one palette group (kythera_lib.GROUPS), then redraws static tiles
   within 2 px of another as that tile.
2. Packs them into the 8-wide sheet from fixed section rows.
3. Writes data/tilesets/secondary/<dir>/porytiles_src: the three layers,
   attributes.csv, and anim/ (one Porytiles animation per animated layer:
   every 8x8 tile that changes between frames becomes an animated tile).
4. Compiles with Porytiles in a scratch project (build/<dir>_porytiles)
   against an empty stand-in primary.
5. Borrows aethos ground: cells drawn on grass, path, sand, sea, shallows or
   falling water get aethos's ground metatile's bottom tiles.
6. Verifies every entry, fails past 504 tiles (the door animations own
   504-511), registers the tileset in src/data/tilesets/*.h (and its
   animation in src/tileset_anims.c), writes the scripted-swap labels, the
   catalog JSON, tools/ichor/maps/kythera_tiles.py (every tileset's catalog as
   a Python dict), the sheet and piece images, and design/phase4/TILES_*.md.

Usage: /usr/bin/python3 tools/ichor/art/kythera_build.py [kythera|paphia|neraida|melos|all]
           [--no-compile]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_lib as K  # noqa: E402

ROOT = K.ROOT
COLS = 8
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 2
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/phase4/img"
TILES_PY = ROOT / "tools/ichor/maps/kythera_tiles.py"
NORMAL, COVERED, SPLIT = 0, 1, 2

# animation frame orders (Porytiles queues one step every 16 frames)
ANIM_ORDER = {
    "surf": ["0", "1", "2", "1"],
    "wheel": ["0", "1", "2", "3"],
    "glint": ["0", "0", "0", "1", "2", "0", "0", "0", "0", "0", "1", "0"],
}


# --------------------------------------------------------------------------
# What each tileset holds
# --------------------------------------------------------------------------

def _all():
    import kythera_coast as Co
    import kythera_harbor as H
    import kythera_land as La
    import kythera_town as T
    import kythera_water as Wa
    by = {}
    for s in Co.build() + La.build() + H.build() + T.build() + Wa.build():
        by[s.key] = s
    by["_flowers_all"] = La.flowers()
    by["_hedge_all"] = La.hedge()
    by["_quarry_all"] = La.quarry()
    by["_trees_all"] = La.trees()
    return by


def spec(name):
    by = _all()
    house = by["house"]
    fl = by["_flowers_all"]
    if name == "kythera":
        return {
            "symbol": "gTileset_Kythera", "dir": "kythera", "label": "Kythera",
            "doc": "TILES_kythera.md", "title": "the Foam Road and the Spring of Kallirhoe",
            "images": [("kythera_foam_beach.png", "A 240 x 160 screen of the Foam Road at Aphrodite's rock (3x; `kythera_foam_beach_1x.png` is 1x)"), ("kythera_foam_road.png", "A wider stretch of the Foam Road: the herm, the spring stair, the quarry and its drums, the cutting, the reef spit"), ("kythera_spring.png", "The Spring of Kallirhoe")],
            "sections": [
                ("coast", [by["surf"], by["sand_decor"], by["shingle"], by["rocks"],
                           by["aphrodite_rock"], by["cliff"]]),
                ("land", [by["myrtle"],
                          K.pick(fl, ["briar", "briar_L", "briar_R", "thrift", "narcissus",
                                      "narcissus_b", "petals"], key="flowers",
                                 notes="On borrowed grass. `briar` is a wild rose bush; `briar_L` "
                                       "`briar_R` a two-cell thicket. Walkable: `thrift`, sea-pink "
                                       "cushions; `narcissus` and `narcissus_b`, the white flower "
                                       "of the spring (ring Kallirhoe's pool with them); `petals`, "
                                       "rose petals blown on the grass."),
                          by["seagrass"], by["quarry"]]),
                ("water", [by["spring_pool"],
                           K.pick(by["falls"], ["thin_fall", "thin_foot", "thin_sea", "basin"],
                                  key="falls",
                                  notes="Freshwater. `thin_fall`: a thin cascade one cell wide, rock "
                                        "either side of the stream (borrowed waterfall, "
                                        "`MB_WATERFALL`): the spring's fall from its rock lip (put "
                                        "`cliff.spring_lip` above it) and the Foam Road's Horn gate "
                                        "off the cliff west of Aphrodite's rock. `thin_foot` is its "
                                        "foot in a pool, `thin_sea` its foot in the sea (both "
                                        "animated foam). `basin`: the Foam Road's rest point, the "
                                        "stone basin under the cliff's `seep` where pilgrims drink "
                                        "(borrowed shallows; impassable, read it)."),
                           K.pick(by["vault_cave"], ["cave_top", "cave_stair"], w=1, key="cave_stair",
                                  notes="Set into a pink cliff face: `cave_top` over `cave_stair`, a "
                                        "rough arch and a rock stair going down into the dark, the "
                                        "spring's way down to Echo's caves. The stair is the door "
                                        "(`MB_NON_ANIMATED_DOOR`).")]),
                ("town", [K.pick(by["herm_shrine"], ["herm", "herm_base"], w=1, key="herm",
                                 notes="Kythera's great herm at the Foam Road's fork: a tall marble "
                                       "pillar with Hermes's bearded head, the oil on his face long "
                                       "dried to a dark stain, on a plinth carved with the roads (on "
                                       "borrowed grass). `herm` (top, drawn over the player) over "
                                       "`herm_base` (impassable; bg event here)."),
                          by["rollers"]]),
            ],
            "rows": {"coast": 0, "land": 18, "water": 36, "town": 44},
            "fronts": [],
            "labels": [("quarry", [("gate_TL", "GirdleGate_TL"), ("gate_TR", "GirdleGate_TR"),
                                   ("gate_BL", "GirdleGate_BL"), ("gate_BR", "GirdleGate_BR"),
                                   ("drag", "GirdleGate_Moved")])],
        }
    if name == "skandeia":
        hedge = by["_hedge_all"]
        return {
            "symbol": "gTileset_Skandeia", "dir": "skandeia", "label": "Skandeia",
            "doc": "TILES_skandeia.md",
            "images": [("skandeia_harbor_street.png", "A 240 x 160 screen of Skandeia's harbor street (3x; `skandeia_harbor_street_1x.png` is 1x)"), ("skandeia_town.png", "Skandeia: the slipways, the Euploia at the gangplank, the quay, the houses on their terraces")], "title": "Skandeia, Kythera's harbor town",
            "sections": [
                ("harbor", [K.pick(by["quay"], ["S", "S_b", "N", "E", "W", "out_SE", "out_SW",
                                                "out_NE", "out_NW", "in_SE", "in_SW", "in_NE",
                                                "in_NW", "steps_E", "steps_S", "ring_S", "N_plank",
                                                "S_plank"], w=8, key="quay",
                                   notes=by["quay"].notes),
                            slips_only(by["slips"]), by["kaiki"], by["trireme"], by["gear"],
                            by["flags"]]),
                ("town", [K.pick(house, ["R_L", "R_M", "R_R", "R_chimney", "R_jar",
                                         "U_L", "U_M", "U_R", "U_window", "U_vine",
                                         "G_L", "G_M", "G_R", "door_white", "door",
                                         "pot_rose", "pot_basil", "G_window", "G_bench", "G_steps",
                                         "R_dove", "R_doves", "U_window_pink", "U_niche", "G_shell"],
                                 w=5, key="house", notes=house.notes),
                          K.pick(by["herm_shrine"], ["shrine", "shrine_base"], w=1, key="shrine",
                                 notes="Aphrodite of the Harbor, at the quay's south end: a marble "
                                       "niche with a bronze dove, its sill heaped with old shells "
                                       "(on borrowed path). `shrine` (top, drawn over the player) "
                                       "over `shrine_base` (impassable; the bg event)."),
                          by["terrace"]]),
                ("coast", [K.pick(by["surf"], ["S", "S2", "N", "E", "W", "out_NW", "out_NE",
                                               "out_SW", "out_SE", "in_SE", "in_SW", "in_NE",
                                               "in_NW"], w=8, key="surf", notes=by["surf"].notes),
                           K.pick(by["sand_decor"], ["lace", "shells", "scallop", "wrack"],
                                  key="sand_decor",
                                  notes="On borrowed sand, walkable: `lace` (a line of dried foam), "
                                        "`shells`, `scallop`, `wrack`."),
                           K.pick(hedge, ["L", "M", "R", "single", "bush"], key="myrtle",
                                  notes="Myrtle on borrowed grass: a run `L` `M` `R`, a `single` "
                                        "clump and a smaller round `bush`. Impassable."),
                           K.pick(fl, ["briar", "thrift", "petals"], key="flowers",
                                  notes="On borrowed grass: `briar`, a wild rose bush (impassable); "
                                        "`thrift` and `petals` (walkable).")]),
            ],
            "rows": {"harbor": 0, "town": 20, "coast": 34},
            "fronts": ["cube", "cube_pot", "long_house", "stair_house"],
            "labels": [("slips", [("slip", "Slip_Empty_TL"), ("slip_boat", "Slip_Boat_TL")])],
        }
    if name == "paphia":
        hedge = by["_hedge_all"]
        trees = by["_trees_all"]
        return {
            "symbol": "gTileset_Paphia", "dir": "paphia", "label": "Paphia",
            "doc": "TILES_paphia.md", "title": "Paphia, the temple town",
            "images": [("paphia_town.png", "Paphia's crown: the temple, the great stair, the terraces, a dovecote, the sculptors")],
            "sections": [
                ("town", [K.pick(house, ["R_L", "R_M", "R_R", "R_dove", "R_doves", "R_chimney",
                                         "U_L", "U_M", "U_R", "U_window", "U_window_pink",
                                         "U_niche", "U_vine", "G_L", "G_M", "G_R", "door",
                                         "door_arch", "door_white", "mirror", "mirror_dim",
                                         "G_shell", "pot_rose", "G_bench", "G_window"],
                                 w=6, key="house", notes=house.notes),
                          by["dovecote"], by["great_stair"], by["temple_front"], by["sculptors"]]),
                ("land", [K.pick(hedge, ["L", "M", "R", "single", "bush", "T", "V", "B"], key="myrtle",
                                 notes="Myrtle on borrowed grass: a run `L` `M` `R`, north-south `T` "
                                       "`V` `B`, a `single` clump and a smaller round `bush`. "
                                       "Impassable."),
                          K.pick(fl, ["briar", "briar_L", "briar_R", "thrift", "petals"],
                                 key="flowers",
                                 notes="On borrowed grass: `briar`, `briar_L` `briar_R` (wild rose, "
                                       "impassable); `thrift` and `petals` (walkable)."),
                          K.pick(trees, ["apple_TL", "apple_TR", "apple_BL", "apple_BR", "gold_L",
                                         "gold_R"], w=2, key="apple",
                                 notes="The orchard on Paphia's north edge: an apple tree 2 x 2 "
                                       "(`apple_TL` `apple_TR`, its crown's top row drawn over the "
                                       "player, over `apple_BL` `apple_BR`, impassable), hung with "
                                       "red apples. `gold_L` `gold_R` are the crown's top row in "
                                       "golden blossom, to swap over an apple's top row."),
                          by["terrace"]]),
                ("harbor", [K.pick(by["quay"], ["S", "N", "E", "W", "out_SE", "out_SW", "out_NE",
                                                "out_NW", "in_SE", "in_SW", "in_NE", "in_NW",
                                                "steps_S", "steps_E", "S_plank"], w=8, key="quay",
                                   notes=by["quay"].notes),
                            by["honey_boat"], by["kaiki"]]),
                ("coast", [K.pick(by["surf"], ["S", "S2", "N", "E", "W", "out_NW", "out_NE",
                                               "out_SW", "out_SE", "in_SE", "in_SW", "in_NE",
                                               "in_NW"], w=8, key="surf", notes=by["surf"].notes),
                           K.pick(by["sand_decor"], ["lace", "shells", "scallop"], key="sand_decor",
                                  notes="On borrowed sand, walkable: `lace` (a line of dried foam), "
                                        "`shells`, `scallop`.")]),
            ],
            "rows": {"town": 0, "land": 22, "harbor": 34, "coast": 44},
            "fronts": ["paphia_house", "paphia_narrow", "chapel_house", "cube"],
            "labels": [("apple", [("gold_L", "AppleGold_L"), ("gold_R", "AppleGold_R"),
                                  ("apple_TL", "Apple_TL"), ("apple_TR", "Apple_TR")]),
                       ("house", [("mirror", "Mirror"), ("mirror_dim", "Mirror_Dim")])],
        }
    if name == "neraida":
        hedge = by["_hedge_all"]
        trees = by["_trees_all"]
        cl = by["cliff"]
        return {
            "symbol": "gTileset_Neraida", "dir": "neraida", "label": "Neraida",
            "doc": "TILES_neraida.md", "title": "the Neraida falls",
            "images": [("neraida_falls.png", "The Neraida ravine: the falls, the plunge pool and the Naiads' altar, the weir, Myles's mill, the plank bridge, the vault door")],
            "sections": [
                ("water", [by["falls"], by["kerb"], by["bridge_weir"], by["mill"],
                           K.pick(by["vault_cave"], ["vault_TL", "vault_TR", "vault_BL",
                                                     "vault_door"], w=2, key="vault",
                                  notes="The Minoan vault door in the cliff behind the upper pool "
                                        "(2 x 2): no handle, only a hollow shaped like a double axe; "
                                        "round its frame old paint flakes, blue dolphins and red "
                                        "bulls. Set it into a pink cliff face. `vault_door` (1, 1) is "
                                        "the door (`MB_NON_ANIMATED_DOOR`): the script opens it with "
                                        "the Labrys."),
                           by["naiad_altar"]]),
                ("coast", [K.pick(cl, ["lip_L", "lip", "lip_R", "side_E", "side_W", "back",
                                       "back_NW", "back_NE", "face_L", "face", "face_R",
                                       "corner_in_E", "corner_in_W", "foot_grass", "spring_lip",
                                       "foot_sand_rocks"], w=8, key="cliff",
                                  notes="The pink cliff kit (see `TILES_kythera.md`): a south-facing "
                                        "cliff is `lip` over `face` over the ground (`foot_grass`); "
                                        "`_L` / `_R` end a run; `side_E` / `side_W`, `back` and its "
                                        "corners finish a plateau; `corner_in_*` turn a face north. "
                                        "Build the falls' cliffs from it, with `falls.face_fall_*` "
                                        "beside the water. `spring_lip`: a jutting rock lip a thin "
                                        "fall pours from.")]),
                ("land", [K.pick(hedge, ["L", "M", "R", "single", "bush", "T", "V", "B"], key="myrtle",
                                 notes="Myrtle on borrowed grass: a run `L` `M` `R`, north-south `T` "
                                       "`V` `B`, a `single` clump and a smaller `bush`. Impassable."),
                          K.pick(fl, ["briar", "oleander", "thrift", "narcissus", "petals"],
                                 key="flowers",
                                 notes="On borrowed grass: `briar` (wild rose) and `oleander` (the "
                                       "ravine's pink shrub), impassable; `thrift`, `narcissus` and "
                                       "`petals`, walkable."),
                          by["seagrass"],
                          K.pick(trees, ["plane_00", "plane_10", "plane_20", "plane_01", "plane_11",
                                         "plane_21", "plane_02", "plane_12", "plane_22"], w=3,
                                 key="plane",
                                 notes="The oriental plane (3 x 3): a broad crown of maple-like "
                                       "leaves over a mottled pale trunk. Its top row is drawn over "
                                       "the player (`T`); the rest is impassable."),
                          by["terrace"]]),
            ],
            "rows": {"water": 0, "coast": 22, "land": 26},
            "fronts": [],
            "labels": [("naiad_altar", [("horn", "Altar_Horn"), ("empty", "Altar_Empty")]),
                       ("mill", [("wheel", "MillWheel_TL"), ("wheel_still", "MillWheelStill_TL")])],
        }
    if name == "melos":
        import melos_art as Me
        import kythera_coast as Co
        rocks_all = Co.tide_rocks()
        return {
            "symbol": "gTileset_Melos", "dir": "melos", "label": "Melos",
            "doc": "TILES_melos.md",
            "images": [("melos_klima.png", "Klima on Melos: boathouses, the well, the terraces and the niche, the obsidian slope, the pumice cliffs")],
            "title": "Melos, the sea of Routes 22 and 23, and Echo's sea caves",
            "sections": [
                ("melos", Me.build_melos() + [
                    K.pick(house, ["R_L", "R_M", "R_R", "R_chimney", "U_L", "U_M", "U_R",
                                   "U_window", "G_L", "G_M", "G_R", "door_white", "pot_basil",
                                   "pot_rose"], w=7, key="house", notes=house.notes),
                    K.pick(by["quay"], ["S", "N", "E", "W", "out_SE", "out_SW", "out_NE", "out_NW",
                                        "steps_S", "N_plank", "S_plank"], w=6, key="quay",
                           notes="The stone jetty where the Euploia's boat lands: the quay kit's "
                                 "edges (see `TILES_skandeia.md`), its top aethos path."),
                    by["kaiki"], Me.obsidian_veins()]),
                ("coast", [K.pick(by["surf"], ["S", "S2", "N", "E", "W", "out_NW", "out_NE",
                                               "out_SW", "out_SE", "in_SE", "in_SW", "in_NE",
                                               "in_NW"], w=8, key="surf", notes=by["surf"].notes),
                           K.pick(by["sand_decor"], ["lace", "shells", "wrack"], key="sand_decor",
                                  notes="On borrowed sand, walkable: `lace`, `shells`, `wrack`."),
                           Co.pumice(),
                           K.pick(rocks_all, ["tide_rock", "tide_rocks", "rock_sand", "rock_grass",
                                              "stake", "stakes", "sunken_column", "sunken_drum"],
                                  key="rocks",
                                  notes="`tide_rock` and `tide_rocks` stand in the surf with breathing "
                                        "foam (animated); `rock_sand`, `rock_grass` on land. The sea "
                                        "marks of Routes 22 and 23: `stake` and `stakes` (the "
                                        "trireme lane), `sunken_column` (a fallen capital awash), "
                                        "`sunken_drum` (a drum under the turquoise shallows, "
                                        "surfable). All on borrowed sea except where named.")]),
                ("sea", Me.build_sea()),
                ("cave", Me.build_cave() + [
                    K.pick(fl, ["thrift", "briar"], key="flowers",
                           notes="On borrowed grass: `thrift` (walkable), `briar` (impassable).")]),
            ],
            "rows": {"melos": 0, "coast": 32, "sea": 44, "cave": 48},
            "fronts": ["cube", "cube_pot"],
            "labels": [("cave", [("brazier_cold", "Brazier_Cold"), ("brazier_lit", "Brazier_Lit")])],
        }
    if name == "temple_aphrodite":
        import temple_aphrodite_art as TA
        return {
            "symbol": "gTileset_TempleAphrodite", "dir": "temple_aphrodite",
            "label": "TempleAphrodite", "doc": "TILES_temple_aphrodite.md",
            "images": [("temple_aphrodite_gallery.png", "The gallery and, through its doorway, the rose court with Galatea's dais")],
            "title": "the Temple of Aphrodite, Galatea's Gallery",
            "sections": [("temple", TA.build())],
            "rows": {"temple": 0},
            "fronts": [], "groups": TA.GROUPS, "primary": "oikos",
            "labels": [("mirrors", [("mirror_N", "Mirror_N"), ("mirror_dim", "Mirror_Dim")])],
        }
    raise SystemExit(f"kythera_build: unknown tileset {name}")


def slips_only(sl):
    """The two slipways (2 x 3 each) side by side, without the keel."""
    s = K.struct("slips", "Slipways, and the boat the Titans left", 4, 3, sl.section,
                 walk=["XXXX", "XXXX", "WWWW"],
                 names={"slip": (0, 0), "slip_boat": (2, 0)},
                 notes="The slipways at the quay's north end, every one empty and chalked with a "
                       "sickle. `slip` (2 wide x 3 tall at its top-left): a stone ramp with timber "
                       "runners down into the sea, its foot on borrowed sea. `slip_boat` (2 x 3): "
                       "the one boat the Titans left, hauled up the same slip, a sickle chalked on "
                       "her bow and, smaller, somebody else's note. After the climax the boats come "
                       "back: swap `slip_boat`'s six cells over a `slip`'s. Impassable; the feet are "
                       "water.")
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = sl.layers[ln].a[0:48, 0:64]
    s.ground = {k: v for k, v in sl.ground.items() if k[0] < 4}
    for (x, y), mb in sl.behaviors.items():
        if x < 4:
            s.behaviors[(x, y)] = mb
    return s


# --------------------------------------------------------------------------
# Packing and sources
# --------------------------------------------------------------------------

def pack(sp):
    used = np.zeros((64, COLS), bool)
    total = 0
    starts = sorted(sp["rows"].values())
    for name, structs in sp["sections"]:
        start = sp["rows"][name]
        end = start
        for s in structs:
            s.ids = [[None] * s.w for _ in range(s.h)]
            for c0 in range(0, s.w, COLS):
                cw = min(COLS, s.w - c0)
                spot = None
                for row in range(start, 64 - s.h + 1):
                    for col in range(0, COLS - cw + 1):
                        if not used[row:row + s.h, col:col + cw].any():
                            spot = (row, col)
                            break
                    if spot:
                        break
                assert spot, f"no room for {s.key}"
                row, col = spot
                used[row:row + s.h, col:col + cw] = True
                for y in range(s.h):
                    for x in range(cw):
                        s.ids[y][c0 + x] = 0x200 + (row + y) * COLS + col + x
                end = max(end, row + s.h)
        later = [st for st in starts if st > start]
        if later:
            assert end <= min(later), f"section {name} overflows into row {min(later)} (ends {end})"
        print(f"  {name}: rows {start}-{end - 1}")
        total = max(total, end)
    return total, used


def write_sources(sp, structs, rows, used):
    src = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_src"
    if src.exists():
        shutil.rmtree(src)
    src.mkdir(parents=True)
    W, H = COLS * 16, rows * 16
    sheets = {ln: np.zeros((H, W, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    beh = {}
    for s in structs:
        for cy in range(s.h):
            for cx in range(s.w):
                i = s.ids[cy][cx] - 0x200
                r, c = divmod(i, COLS)
                for ln in sheets:
                    sheets[ln][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = \
                        s.layers[ln].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        for (x, y), mb in s.behaviors.items():
            beh[s.ids[y][x] - 0x200] = mb
    # a cell no structure uses gets an opaque filler so Porytiles has no holes
    for r in range(rows):
        for c in range(COLS):
            if not used[r, c]:
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16, :3] = K.C["cw1"]
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16, 3] = 255
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(src / f"{ln}.png")
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]
    (src / "attributes.csv").write_text("\n".join(lines) + "\n")
    write_anims(src, structs)
    return src


def static_forms(structs):
    """Every static (non-animated) tile, in all four flips."""
    static = set()
    for s in structs:
        at = K.anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in s.ground:
                        continue
                    if (ln, tx, ty) in at:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    static |= {v.tobytes() for v in K._flips(t)}
    return static


def fix_keys(structs):
    """Make every animated tile's key frame (frame 0) non-empty and unique: a
    tile that is blank in frame 0, or whose frame 0 matches another animated
    tile that moves differently, or a static tile, takes one pixel from its
    own later frames."""
    seen = {}
    nudged = 0
    static = static_forms(structs)
    for s in structs:
        at = K.anim_tiles(s)
        for (ln, tx, ty), name in sorted(at.items(), key=lambda kv: (kv[0][2], kv[0][1], kv[0][0])):
            an = s.anims[name]
            sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            base = s.layers[ln].a
            frames = [f.a[sl] for f in an["frames"]]
            for _ in range(64):
                key = base[sl].copy()
                key[key[..., 3] == 0] = 0
                fr = [key.tobytes()] + [np.where(f[..., 3:4] > 0, f, 0).tobytes() for f in frames]
                kb = key.tobytes()
                empty = not (key[..., 3] > 0).any()
                clash = (kb in seen and seen[kb] != fr) or \
                    any(v.tobytes() in static for v in K._flips(key))
                if not empty and not clash:
                    seen[kb] = fr
                    break
                # take a pixel some later frame has and frame 0 lacks (or differs on)
                done = False
                for f in frames:
                    diff = np.argwhere((f != base[sl]).any(-1) & (f[..., 3] > 0))
                    for (yy, xx) in diff:
                        if not done:
                            base[ty * 8 + yy, tx * 8 + xx] = f[yy, xx]
                            done = True
                            nudged += 1
                    if done:
                        break
                if not done:
                    raise SystemExit(f"kythera_build: can't make {s.key} tile ({tx},{ty})'s key unique")
    if nudged:
        print(f"  nudged {nudged} pixels to make animation key frames unique")


def collect_anims(structs):
    """{anim name: [(key tile RGBA, [frame tiles])]} in a stable order; checks
    one key never animates two ways."""
    out = {}
    seen = {}
    for s in structs:
        at = K.anim_tiles(s)
        for (ln, tx, ty), name in sorted(at.items(), key=lambda kv: (kv[0][2], kv[0][1], kv[0][0])):
            an = s.anims[name]
            sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            key = s.layers[ln].a[sl].copy()
            key[key[..., 3] == 0] = 0
            frames = [key] + [f.a[sl].copy() for f in an["frames"]]
            for f in frames:
                f[f[..., 3] == 0] = 0
            kb = key.tobytes()
            if kb in seen:
                prev = seen[kb]
                if prev[0] != name or any(not np.array_equal(a, b) for a, b in zip(prev[1], frames)):
                    raise SystemExit(f"kythera_build: {s.key} tile ({tx},{ty}) shares its key frame "
                                     f"with another animated tile but animates differently")
                continue
            seen[kb] = (name, frames)
            out.setdefault(name, []).append((key, frames))
    return out


def write_anims(src, structs):
    anims = collect_anims(structs)
    if not anims:
        return {}
    d = src / "anim"
    d.mkdir(parents=True, exist_ok=True)
    meta = {}
    for name, tiles in anims.items():
        n = len(tiles[0][1])
        ad = d / name
        ad.mkdir()
        key = np.concatenate([t[0] for t in tiles], axis=0)
        Image.fromarray(key, "RGBA").save(ad / "key.png")
        for fi in range(n):
            fr = np.concatenate([t[1][fi] for t in tiles], axis=0)
            Image.fromarray(fr, "RGBA").save(ad / f"{fi}.png")
        order = ANIM_ORDER.get(name, [str(i) for i in range(n)])
        meta[name] = {"frames": [str(i) for i in range(n)], "frame_order": order}
        print(f"  anim {name}: {len(tiles)} tiles x {n} frames")
    (d / "anim.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def check_anim_keys(structs):
    """An animated key tile must not also appear as a static tile anywhere."""
    static = set()
    keys = set()
    for s in structs:
        at = K.anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in s.ground:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    forms = {v.tobytes() for v in K._flips(t)}
                    if (ln, tx, ty) in at:
                        keys |= forms
                    else:
                        static |= forms
    clash = keys & static
    if clash:
        raise SystemExit(f"kythera_build: {len(clash)} animated key tiles also appear as static tiles")


# --------------------------------------------------------------------------
# Porytiles, in a scratch project
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-4000:], r.stderr[-4000:])
        sys.exit(f"kythera_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints(groups):
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in groups.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = K.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def suffix(sp):
    return sp["symbol"].replace("gTileset_", "")


def scratch_project(sp, groups):
    name, d = sp["symbol"], sp["dir"]
    sfx = suffix(sp)
    scratch = ROOT / f"build/{d}_porytiles"
    cfg_real = ROOT / "porytiles/tilesets" / name
    bin_real = ROOT / f"data/tilesets/secondary/{d}/porytiles_bin"
    if scratch.exists():
        shutil.rmtree(scratch)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (scratch / "data/tilesets/primary").mkdir(parents=True)
    (scratch / "data/tilesets/secondary").mkdir(parents=True)
    # keep the scratch's C tables free of this tileset: Porytiles rewrites them
    for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "src/tileset_anims.c", "include/tileset_anims.h"):
        p = scratch / rel
        t = p.read_text()
        t = re.sub(rf"(// [^\n]*\n)*const struct Tileset {name}\s*=\s*\{{.*?\}};\n", "", t, flags=re.S)
        t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{sfx}\[\]\[16\]\s*=\s*\{{.*?\}};\n",
                   "", t, flags=re.S)
        t = "\n".join(line for line in t.split("\n")
                      if not re.search(rf"PorytilesManaged_{sfx}\b|tilesets/{d}/generated_anim_code",
                                       line))
        p.write_text(t)
    pt = porytiles()
    run([pt, "create-tileset", "-C", str(scratch), f"gTileset_{sfx}Stub"])
    stub = next((scratch / "data/tilesets/primary").iterdir()) / "porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), f"gTileset_{sfx}Stub"])
    cfg = scratch / "porytiles/tilesets" / name
    cfg.mkdir(parents=True)
    pairing = (f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_{sfx}Stub]\n")
    (cfg / "config.yaml").write_text(pairing)
    run([pt, "create-tileset", "-C", str(scratch), "--secondary", name])
    sec = scratch / f"data/tilesets/secondary/{d}"
    shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(ROOT / f"data/tilesets/secondary/{d}/porytiles_src", sec / "porytiles_src")
    (cfg / "config.yaml").write_text(pairing + palette_hints(groups))
    return scratch, sec, cfg_real, bin_real


def compile_tileset(sp, groups):
    scratch, sec, cfg_real, bin_real = scratch_project(sp, groups)
    name = sp["symbol"]
    r = run([porytiles(), "compile-tileset", "-C", str(scratch), "--no-verify-checksums", name])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if bin_real.exists():
        shutil.rmtree(bin_real)
    shutil.copytree(sec / "porytiles_bin", bin_real)
    cfg_real.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(scratch / "porytiles/tilesets" / name / f, cfg_real / f)
    (cfg_real / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {name} ({sp['title']}).\n"
        "# Written by tools/ichor/art/kythera_build.py, which compiles it against an empty\n"
        "# stand-in primary, then points its ground cells at aethos's grass, path, sand,\n"
        "# sea, shallows and waterfall. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints(groups))
    gen = scratch / f"include/porytiles_generated/tilesets/{sp['dir']}/generated_anim_code.h"
    dst = ROOT / f"include/porytiles_generated/tilesets/{sp['dir']}/generated_anim_code.h"
    if gen.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(gen, dst)
        return True
    if dst.exists():
        dst.unlink()
    return False


def borrow_ground(sp, structs):
    bin_ = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_bin"
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(bin_ / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(bin_ / "metatile_attributes.bin", "<u2")
    patched = {}
    for s in structs:
        for (cx, cy), kind in s.ground.items():
            i = s.ids[cy][cx] - 0x200
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            on_top = bool((s.T.a[sl][..., 3] > 0).any())
            lt = int(attrs[i]) >> 12
            ent = [int(e) for e in meta[i]]
            art = ent[4:8] if any(ent[4:8]) else ent[0:4]
            if on_top and lt == NORMAL:
                art = ent[4:8]
            meta[i, 0:4] = aethos[K.GROUND_METATILE[kind], 0:4]
            meta[i, 4:8] = art
            attrs[i] = (int(attrs[i]) & 0x0FFF) | ((SPLIT if on_top else COVERED) << 12)
            patched[i] = kind
    meta.astype("<u2").tofile(bin_ / "metatiles.bin")
    attrs.astype("<u2").tofile(bin_ / "metatile_attributes.bin")
    return patched


def verify(sp, rows, patched):
    bin_ = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_bin"
    raw = np.fromfile(bin_ / "metatiles.bin", "<u2").reshape(-1, 8)
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        for j, e in enumerate(entries):
            e = int(e)
            if i in patched and j < 4:
                if e != int(aethos[K.GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"kythera_build: entries outside the secondary's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(bin_ / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT or late:
        sys.exit(f"kythera_build: {used} tiles and tiles {late[:8]} referenced; the door "
                 f"animations overwrite tiles {TILE_LIMIT}-511")
    return used, len(raw)


# --------------------------------------------------------------------------
# Registration in the C tables
# --------------------------------------------------------------------------

def register(sp, animated):
    d, name, sfx = sp["dir"], sp["symbol"], suffix(sp)
    gfx = ROOT / "src/data/tilesets/graphics.h"
    t = gfx.read_text()
    if f"gTilesetTiles_PorytilesManaged_{sfx}[]" not in t:
        pals = ",\n".join(f'    INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/palettes/{p:02d}.gbapal")'
                          for p in range(16))
        t = t.rstrip("\n") + (
            f"\n\n// Ichor: {d} ({sp['title']}), written by tools/ichor/art/kythera_build.py\n"
            f"const u32 gTilesetTiles_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U32(\"data/tilesets/secondary/{d}/porytiles_bin/tiles.4bpp.lz\");\n\n"
            f"const u16 gTilesetPalettes_PorytilesManaged_{sfx}[][16] =\n{{\n{pals}\n}};\n")
        gfx.write_text(t)
    met = ROOT / "src/data/tilesets/metatiles.h"
    t = met.read_text()
    if f"gMetatiles_PorytilesManaged_{sfx}[]" not in t:
        t = t.rstrip("\n") + (
            f"\n\n// Ichor: {d}\n"
            f"const u16 gMetatiles_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U16(\"data/tilesets/secondary/{d}/porytiles_bin/metatiles.bin\");\n"
            f"const u16 gMetatileAttributes_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U16(\"data/tilesets/secondary/{d}/porytiles_bin/metatile_attributes.bin\");\n")
        met.write_text(t)
    hdr = ROOT / "src/data/tilesets/headers.h"
    t = hdr.read_text()
    cb = f"InitTilesetAnim_PorytilesManaged_{sfx}" if animated else "NULL"
    if sp.get("primary", "aethos") == "aethos":
        why = (f"// tools/ichor/art/kythera_build.py for the aethos primary: its ground cells\n"
               f"// borrow aethos's grass, path, sand, sea, shallows and waterfall, so rebuild\n"
               f"// it whenever aethos changes.\n")
    else:
        why = (f"// tools/ichor/art/kythera_build.py; it uses only its own tiles and palettes\n"
               f"// 6-12, so it works on any interior primary (it is meant for oikos).\n")
    block = (f"// Ichor: {d}, {sp['title']} (Act III). Porytiles-managed, built by\n" + why +
             f"const struct Tileset {name} =\n{{\n"
             f"    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
             f"    .tiles = gTilesetTiles_PorytilesManaged_{sfx},\n"
             f"    .palettes = gTilesetPalettes_PorytilesManaged_{sfx},\n"
             f"    .metatiles = gMetatiles_PorytilesManaged_{sfx},\n"
             f"    .metatileAttributes = gMetatileAttributes_PorytilesManaged_{sfx},\n"
             f"    .callback = {cb},\n}};\n")
    if f"const struct Tileset {name} =" in t:
        t = re.sub(rf"// Ichor: {d}, .*?const struct Tileset {name}\s*=\s*\{{.*?\}};\n", block, t,
                   flags=re.S)
    else:
        t = t.rstrip("\n") + "\n\n" + block
    hdr.write_text(t)
    # the animation: include the generated code and declare its init
    anc = ROOT / "src/tileset_anims.c"
    anh = ROOT / "include/tileset_anims.h"
    inc = f'#include "porytiles_generated/tilesets/{d}/generated_anim_code.h"'
    dec = f"void InitTilesetAnim_PorytilesManaged_{sfx}(void);"
    t = anc.read_text()
    if animated and inc not in t:
        t = t.rstrip("\n") + f"\n// [Porytiles] Auto-generated include. Do not remove.\n{inc}\n"
    if not animated and inc in t:
        t = t.replace(f"// [Porytiles] Auto-generated include. Do not remove.\n{inc}\n", "")
    anc.write_text(t)
    t = anh.read_text()
    if animated and dec not in t:
        t = t.replace("\n#endif // GUARD_TILESET_ANIMS_H",
                      f"\n// [Porytiles] Auto-generated declaration. Do not remove.\n{dec}\n"
                      "\n#endif // GUARD_TILESET_ANIMS_H")
    if not animated and dec in t:
        t = t.replace(f"// [Porytiles] Auto-generated declaration. Do not remove.\n{dec}\n", "")
    anh.write_text(t)


LABELS = ROOT / "include/constants/metatile_labels.h"


def write_labels(sp, structs):
    want = dict(sp.get("labels", []))
    if not want:
        return
    start = f"// {sp['symbol']} (Ichor: {sp['title']}), written by tools/ichor/art/kythera_build.py"
    end = f"// end {sp['symbol']}"
    lines = [start]
    by = {s.key: s for s in structs}
    for key, items in want.items():
        s = by[key]
        for name, label in items:
            cx, cy = s.names[name]
            lines.append(f"#define METATILE_{sp['label']}_{label:<24} 0x{s.ids[cy][cx]:03X}")
    lines.append(end)
    block = "\n".join(lines) + "\n"
    text = LABELS.read_text()
    if start in text:
        a = text.index(start)
        b = text.index(end, a) + len(end) + 1
        text = text[:a] + block + text[b:]
    else:
        e = text.rindex("#endif")
        text = text[:e] + block + "\n" + text[e:]
    LABELS.write_text(text)


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------

def catalog(sp, structs):
    import kythera_town as T
    data = []
    for sec_name, ss in sp["sections"]:
        for s in ss:
            data.append({
                "key": s.key, "title": s.title, "section": sec_name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
                "ground": {f"{x},{y}": g for (x, y), g in s.ground.items()},
                "anims": sorted(set(K.anim_tiles(s).values())),
            })
    by = {d["key"]: d for d in data}
    fronts = {}
    for k in sp.get("fronts", []):
        f = T.FRONTS[k]
        house = by["house"]
        ids = []
        for row in f["rows"]:
            r = []
            for ref in row:
                cx, cy = house["names"][ref]
                r.append(house["ids"][cy][cx])
            ids.append(r)
        fronts[k] = {**f, "ids": ids}
    out = ROOT / f"build/{sp['dir']}"
    out.mkdir(parents=True, exist_ok=True)
    cat = {"tileset": sp["symbol"], "structures": data, "fronts": fronts}
    (out / "catalog.json").write_text(json.dumps(cat, indent=1))
    return cat


def write_tiles_py(name, cat):
    """tools/ichor/maps/kythera_tiles.py: every Kythera-family tileset's catalog
    as a Python dict, so map builders import ids by key and name."""
    cur = {}
    if TILES_PY.exists():
        ns = {}
        exec(compile(TILES_PY.read_text(), str(TILES_PY), "exec"), ns)
        cur = ns.get("TILESETS", {})
    slim = {"symbol": cat["tileset"], "structures": {}, "fronts": {}}
    for d in cat["structures"]:
        slim["structures"][d["key"]] = {
            "w": d["w"], "h": d["h"], "ids": d["ids"], "walk": d["walk"],
            "names": {k: tuple(v) for k, v in d["names"].items()},
            "ground": d["ground"], "section": d["section"],
        }
    for k, f in cat["fronts"].items():
        slim["fronts"][k] = {"rows": f["rows"], "ids": f["ids"]}
    cur[name] = slim
    body = json.dumps(cur, indent=1, sort_keys=True)
    body = body.replace("true", "True").replace("false", "False").replace("null", "None")
    TILES_PY.parent.mkdir(parents=True, exist_ok=True)
    TILES_PY.write_text(
        '"""Metatile ids of Act III\'s Kythera-family secondaries, for map builders.\n\n'
        "Generated by tools/ichor/art/kythera_build.py; do not edit. One entry per\n"
        "tileset (kythera, skandeia, paphia, neraida, melos, temple_aphrodite), each\n"
        "{'symbol', 'structures':\n"
        "{key: {'w', 'h', 'ids' (rows of metatile ids), 'walk' (rows of walk codes),\n"
        "'names' {piece: (x, y)}, 'ground' {'x,y': aethos ground}, 'section'}},\n"
        "'fronts': {key: {'rows', 'ids'}}}. The catalogs, with what every piece is\n"
        "for, are design/phase4/TILES_*.md.\n\n"
        "    from kythera_tiles import mid\n"
        "    door = mid('skandeia', 'house', 'door_white')\n"
        '"""\n\n'
        f"TILESETS = {body}\n\n\n"
        "def mid(tileset, key, name=None, x=0, y=0):\n"
        '    """The metatile id of a named piece (or of cell (x, y) of a structure)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['ids'][y][x]\n\n\n"
        "def walk(tileset, key, name=None, x=0, y=0):\n"
        '    """The walk code of a named piece: X . T G J D W P F S (see the catalogs)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['walk'][y][x]\n")


def images(sp, structs):
    IMG.mkdir(parents=True, exist_ok=True)
    d = sp["dir"]
    K.shelf_preview(structs, scale=2, width=1400).save(IMG / f"{d}_pieces.png")
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", sp["symbol"],
         "--primary", sp.get("primary", "aethos"), "--scale", "2", "-o", str(IMG / f"{d}_sheet.png")])
    print(f"design/phase4/img/{d}_pieces.png, design/phase4/img/{d}_sheet.png")


# --------------------------------------------------------------------------

def build_one(name, compile_=True):
    sp = spec(name)
    groups = sp.get("groups", K.GROUPS)
    group_rgb = {g: {K.C[n] for n in names} for g, names in groups.items()}
    structs = [s for _, ss in sp["sections"] for s in ss]
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), f"duplicate structure keys in {name}"
    probs = K.validate(structs, group_rgb)
    if not probs:
        before = len(K.tiles_of(structs))
        merges = K.merge_near_duplicates(structs, NEAR_DUPLICATE_PX, group_rgb)
        print(f"{name}: merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(K.tiles_of(structs))} tiles")
        probs = K.validate(structs, group_rgb)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    fix_keys(structs)
    check_anim_keys(structs)
    rows, used = pack(sp)
    write_sources(sp, structs, rows, used)
    cat = catalog(sp, structs)
    write_tiles_py(name, cat)
    write_labels(sp, structs)
    if not compile_:
        return
    animated = compile_tileset(sp, groups)
    patched = borrow_ground(sp, structs)
    register(sp, animated)
    n_tiles, n_meta = verify(sp, rows, patched)
    images(sp, structs)
    import kythera_catalog
    kythera_catalog.main(name, sp, n_tiles, n_meta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="kythera")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    names = (["kythera", "skandeia", "paphia", "neraida", "melos", "temple_aphrodite"]
             if args.tileset == "all" else [args.tileset])
    for n in names:
        build_one(n, not args.no_compile)


if __name__ == "__main__":
    main()
