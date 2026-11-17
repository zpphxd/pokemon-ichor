#!/usr/bin/env python3
"""Eleusa's six interiors (batch 4).

Every house is a home and every interior is unique (design/MAP_DESIGN.md
section 2). Who lives in each room and what happens there is in
design/phase2/SCRIPT.md, Part 2, "Eleusa interiors"; the plans and the
render-and-critique passes are in design/phase2/ROOMS_eleusa.md.

No new art. The rooms are composed from pieces that already exist:
  domos   the house of Keleos and Dysaules's farmhouse
  limen   the granary-keeper's house, Euphorion's house and the Agora stall
          (both sets draw from tools/ichor/art/limen_art.py, which carries
          oikia's furniture pixel for pixel; two of its stamps, counter_plank
          and pit_stairs, are existing pieces with another behavior)
  civic   the Asclepeion, with the slice's counter and Pithos (laid out in
          ASCLEPEION below from civic's own metatiles)

Room format: emporion_rooms.py's (aegina_homes.py's grid, floors, walls,
stamps, rugs and spots, plus "set").

  /usr/bin/python3 tools/ichor/maps/eleusa_rooms.py   # builds domos, limen and the Asclepeion

Each room's exit is its door mat, which warps back to the first warp id of its
door in MAP_ELEUSA_VILLAGE (design/phase2/BUILD.md, "Batch 4", the Doors table).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOMS_DOC = ROOT / "design/phase2/ROOMS_eleusa.md"

ROOMS = {
    # ------------------------------------------------------------------
    # The house of Keleos: the oldest house in the village, a hall rather
    # than a room. The great hearth burns in the middle between two posts,
    # the old way, with the baby's cradle (a fleece-lined basket) beside it;
    # the long table worn smooth runs down the left side; Metaneira's loom
    # stands in the back corner; Hestia's altar is against the back wall
    # under the goddess's niche; and the three water jars for the trip to the
    # well wait by the door.
    "keleos": {
        "set": "domos",
        "title": "The house of Keleos, Eleusa",
        "map": "MAP_ELEUSA_VILLAGE_HOUSE_OF_KELEOS",
        "layout": "EleusaVillage_HouseOfKeleos",
        "render": "eleusa_keleos.png",
        "floor": "flags",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWW",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
        ],
        "rugs": [("red", 0, 5, 4, 3)],
        "stamps": [
            ("loom", 0, 0),
            ("stool", 2, 2),
            ("window", 4, 0),
            ("niche", 6, 0),
            ("altar", 7, 1),
            ("niche_horse", 8, 0),
            ("window", 10, 0),
            ("chest", 12, 1),
            ("lampstand", 14, 1),
            ("column", 4, 4),
            ("column", 10, 4),
            ("hearth_floor", 6, 5),
            ("kalathos", 8, 6),
            ("table", 0, 6),
            ("table", 2, 6),
            ("stool", 0, 7),
            ("bench", 1, 7),
            ("stool", 3, 7),
            ("kline", 12, 4),
            ("amphora", 14, 6),
            ("pithos", 0, 8),
            ("water_jar", 10, 8),
            ("water_jar", 11, 8),
            ("water_jar", 12, 8),
            ("mat", 7, 9),
        ],
        "spots": [
            ("warp", "door to Eleusa (south-arrow mat)", [(7, 9), (8, 9)]),
            ("npc", "Metaneira, by the hearth", (5, 6), "south"),
            ("npc", "her youngest daughter, at the long table", (1, 5), "south"),
            ("bg", "the hearth", (6, 6), (6, 7, "north")),
            ("bg", "the cradle", (8, 6), (8, 7, "north")),
            ("bg", "the loom", (1, 2), (1, 3, "north")),
            ("bg", "the water jars by the door", (11, 8), (11, 7, "south")),
            ("bg", "Hestia's altar", (7, 2), (7, 3, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # Dysaules's farmhouse: a farm kitchen, smoky under the beam. The hearth
    # and its cauldron at the back, pots and the barley mortar beside it,
    # herbs drying from the beam; seed jars in a row along the back wall; a
    # stool under the window that faces the Rharian field, worn into a
    # Dysaules-shaped dip; the kitchen table; and the cat (a Galekit, the
    # Greek mouser) asleep on a sack by the barn doors.
    "farmhouse": {
        "set": "domos",
        "title": "Dysaules's farmhouse, Eleusa",
        "map": "MAP_ELEUSA_VILLAGE_FARMHOUSE",
        "layout": "EleusaVillage_Farmhouse",
        "render": "eleusa_farmhouse.png",
        "floor": "terracotta",
        "wall": "tavern",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
        ],
        "rugs": [],
        "stamps": [
            ("soot", 0, 0),
            ("hearth", 0, 2),
            ("pots", 2, 2),
            ("herbs", 2, 0),
            ("herbs", 3, 0),
            ("window", 5, 0),
            ("stool", 5, 2),
            ("pithos", 7, 1),
            ("amphora_plain", 8, 1),
            ("pithos", 9, 1),
            ("amphora", 10, 1),
            ("mortar", 3, 4),
            ("table", 4, 4),
            ("stool", 6, 4),
            ("trestle_grain", 0, 5),
            ("amphora_plain", 10, 3),
            ("sack", 9, 5),
            ("sack", 10, 5),
            ("sack", 10, 6),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "the barn doors to Eleusa (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "Theano, at her kitchen table", (5, 3), "south"),
            ("perch", "the cat, a Galekit, asleep on a sack", (9, 5), (9, 6, "north")),
            ("bg", "Dysaules's stool under the window", (5, 2), (4, 2, "east")),
            ("bg", "the seed jars", (8, 2), (8, 3, "north")),
            ("bg", "the hearth", (1, 3), (1, 4, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The granary-keeper's house: half house, half storeroom. The house half
    # (terracotta, the red dado) has his bed, the painting of the Kore and his
    # writing table; the store half (boards, the timber wall) has jars of
    # seed-corn on every shelf, the tally board of every city's first fruits,
    # sacks and grain on the trestle, the scales, and the steps down to his
    # private grain pit.
    "granary": {
        "set": "limen",
        "title": "The granary-keeper's house, Eleusa",
        "map": "MAP_ELEUSA_VILLAGE_GRANARY_HOUSE",
        "layout": "EleusaVillage_GranaryHouse",
        "render": "eleusa_granary.png",
        "floor": "terracotta",
        "floors": {",": "boards"},
        "wall": "red",
        "walls": {"T": "timber"},
        "grid": [
            "WWWWWWTTTTTTT",
            "WWWWWWTTTTTTT",
            "......,,,,,,,",
            "......,,,,,,,",
            "......,,,,,,,",
            "......,,,,,,,",
            "......,,,,,,,",
            "......,,,,,,,",
            "......,,,,,,,",
        ],
        "rugs": [],
        "stamps": [
            ("kline", 0, 2),
            ("niche", 3, 0),
            ("lampstand", 5, 1),
            ("desk", 2, 5),
            ("stool", 2, 6),
            ("amphora_plain", 0, 6),
            ("pit_stairs", 6, 0),
            ("road_map", 7, 0),
            ("honey_shelf", 9, 0),
            ("honey_shelf", 11, 0),
            ("pithos", 12, 2),
            ("pithos", 12, 4),
            ("amphora", 12, 6),
            ("trestle_grain", 8, 4),
            ("scales", 10, 4),
            ("sack", 7, 7),
            ("sack", 8, 7),
            ("sack", 9, 7),
            ("sack", 8, 6),
            ("mat", 4, 8),
        ],
        "spots": [
            ("warp", "the barn doors to Eleusa (south-arrow mat)", [(4, 8), (5, 8)]),
            ("npc", "Sitokles, at his tally board", (8, 2), "north"),
            ("bg", "the painting of the Kore", (3, 1), (3, 2, "north")),
            ("bg", "a jar of seed-corn", (12, 3), (11, 3, "east")),
            ("bg", "the tally board", (7, 1), (7, 2, "north")),
            ("bg", "the steps down to the grain pit", (6, 1), (6, 2, "north")),
            ("bg", "the bed (the Revive is hidden under it)", (1, 3), (1, 4, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # Euphorion's house: a playwright's room. Wax tablets on every surface
    # (two writing tables and the scroll cabinet), the chorus of clay
    # figurines in a row of niches, the window, his couch; and the stage
    # marked out on the floor, a pale square of flags in the boards.
    "poets": {
        "set": "limen",
        "title": "Euphorion's house, Eleusa",
        "map": "MAP_ELEUSA_VILLAGE_POETS_HOUSE",
        "layout": "EleusaVillage_PoetsHouse",
        "render": "eleusa_poets.png",
        "floor": "boards",
        "floors": {",": "flags"},
        "wall": "red",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...,,,,....",
            "...,,,,....",
            "...,,,,....",
            "...........",
            "...........",
        ],
        "rugs": [],
        "stamps": [
            ("scrolls", 0, 1),
            ("niche", 3, 0),
            ("niche_horse", 4, 0),
            ("niche", 5, 0),
            ("niche_horse", 6, 0),
            ("window", 8, 0),
            ("myrtle", 7, 1),
            ("kline", 9, 2),
            ("desk", 8, 5),
            ("klismos_l", 10, 5),
            ("desk", 0, 5),
            ("stool", 2, 5),
            ("amphora", 0, 6),
            ("lampstand", 10, 6),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Eleusa (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "Euphorion, on his stage", (5, 4), "south"),
            ("npc", "his Pithound, the critic", (4, 4), "east"),
            ("bg", "the desk", (8, 5), (8, 6, "north")),
            ("bg", "the chalked stage", (4, 3), (4, 2, "south")),
        ],
    },
    # ------------------------------------------------------------------
    # The Agora stall: a farmhouse front room turned shop. Sacks of barley
    # heaped to the ceiling in the corner, honey jars in a row on the shelf,
    # the hanging scale, and the counter (a plank on legs) the stallkeeper
    # sells across.
    "agora": {
        "set": "limen",
        "title": "The Agora stall, Eleusa",
        "map": "MAP_ELEUSA_VILLAGE_AGORA",
        "layout": "EleusaVillage_Agora",
        "render": "eleusa_agora.png",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
        ],
        "rugs": [],
        "stamps": [
            ("sack", 0, 0),
            ("sack", 0, 1),
            ("sack", 1, 1),
            ("sack", 0, 2),
            ("sack", 1, 2),
            ("sack", 0, 3),
            ("sack", 1, 3),
            ("honey_shelf", 3, 0),
            ("counter_plank", 2, 3),
            ("counter_plank", 4, 3),
            ("scales", 7, 1),
            ("pithos", 9, 1),
            ("amphora_plain", 10, 1),
            ("trestle_grain", 7, 4),
            ("trestle_oil", 9, 4),
            ("pots", 0, 4),
            ("kalathos", 0, 5),
            ("amphora", 0, 6),
            ("amphora_plain", 10, 6),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Eleusa (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "the stallkeeper, behind her counter (talked to across it)", (3, 2), "south"),
            ("npc", "an old woman, choosing barley", (7, 6), "north"),
            ("bg", "the honey jars", (4, 1), (4, 2, "north")),
            ("bg", "the scale", (7, 2), (7, 3, "north")),
            ("bg", "the sacks of barley", (1, 3), (1, 4, "north")),
        ],
    },
}


# ----------------------------------------------------------------------
# The Asclepeion is built from civic, the slice's set of public halls, so it
# shares Akti's and Emporion's counter, Pithos, statue and couches (MAP_DESIGN
# section 2); it is laid out with civic_rooms.py's Room, a grid of civic
# metatile names, as Emporion's is. A country Asclepeion, low and wide, built
# round a courtyard herb garden that the counter looks out on: the garden open
# to the sky in the middle of the hall, its gate between two posts facing the
# counter, a laurel (Apollo's, Asclepius's father's) over the herbs and the
# poppies; the Pithos alone in the back-left corner; the healer at the
# standard station (civic_rooms.healer_station); herbs drying from the beam and
# the sheaves stacked in the back-right corner; the couches for the sick down
# the left side.
ASCLEPEION = {
    "title": "The Asclepeion, Eleusa",
    "map": "MAP_ELEUSA_VILLAGE_ASCLEPEION",
    "layout": "EleusaVillage_Asclepeion",
    "render": "eleusa_asclepeion.png",
    "size": (17, 10),
    "spots": [
        ("warp", "door to Eleusa (the threshold mosaic)", [(9, 9)]),
        ("perch", "the healer, at the counter, looking out on the garden", (9, 2), (9, 4, "north")),
        ("perch", "the Panacoil, coiled round the garden's gate post", (5, 5), (5, 6, "north")),
        ("npc", "the pilgrim with blisters, on the bench", (14, 6), "west"),
        ("npc", "the farmer, bitten by a Kaplet", (3, 6), "east"),
        ("bg", "the Pithos", (1, 2), (1, 3, "north")),
        ("bg", "the Pithos", (2, 2), (2, 3, "north")),
        ("bg", "the statue of Asclepius", (4, 2), (4, 3, "north")),
        ("bg", "the herb garden", (9, 6), (9, 5, "south")),
        ("bg", "the herbs drying from the beam", (13, 1), (13, 2, "north")),
        ("bg", "the sheaves", (16, 3), (16, 4, "north")),
    ],
}


def asclepeion_room():
    import civic_rooms as CR
    W, H = ASCLEPEION["size"]
    r = CR.Room("eleusa_asclepeion", W, H, CR.checker("asc_floor_a", "asc_floor_b"))
    r.row(0, 0, ["asc_wall_top_l"] + ["asc_wall_top"] * (W - 2) + ["asc_wall_top_r"])
    r.row(1, 0, ["asc_wall_l"] + ["asc_wall"] * (W - 2) + ["asc_wall_r"])
    r.row(2, 0, [("asc_floor_a_sh" if x % 2 == 0 else "asc_floor_b_sh") for x in range(W)])
    # The Pithos alone, back left; Asclepius beside it.
    CR.pithos(r, 1)
    r.put("asc_statue", 4, 0, 1, 3)
    # The healer's station, the same in every Asclepeion (civic_rooms.py).
    CR.healer_station(r, 9, 2)
    # Herbs drying from the beam; the sheaves in the corner.
    r.put("asc_herbs", 13, 0, 1, 2)
    r.put("asc_herbs", 14, 0, 1, 2)
    for (x, y) in ((15, 2), (16, 2), (16, 3)):
        r.put_checkered("asc_basket_grain", x, y, single=True)
    # The courtyard garden, open to the sky: grass and poppies, the laurel,
    # posts at its corners, and its gate facing the counter.
    for y in range(5, 9):
        for x in range(6, 13):
            r.set(x, y, "aka_grass_flowers" if (x + y) % 2 == 0 else "aka_grass")
    r.put("aka_laurel", 11, 5, 2, 3)
    # The garden's gate posts at its two near corners, framing it from the
    # counter; the Panacoil coils round the west one.
    for x in (5, 13):
        r.put_checkered("asc_column", x, 3, 1, 3)
    # The sick on couches down the left; a bench for those waiting on the right.
    r.put_checkered("asc_kline", 0, 4, 2, 2)
    r.put_checkered("asc_kline", 0, 7, 2, 2)
    r.put_checkered("asc_brazier", 3, 4, 1, 2)
    r.put_checkered("asc_brazier", 15, 4, 1, 2)
    r.put_checkered("asc_bench", 14, 7, 2, 1)
    r.put_checkered("asc_snake", 3, 9)
    r.put_checkered("asc_mat", 9, 9, single=True)
    return r


def render_asclepeion(out):
    """Write the Asclepeion's blockdata to build/render and render it (2x) to `out`."""
    import subprocess
    import civic_tiles as ct
    ct.define()
    r = asclepeion_room()
    W, H = ASCLEPEION["size"]
    tmp = ROOT / "build/render/eleusa_asclepeion.bin"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    r.blocks().tofile(tmp)
    subprocess.run(["/usr/bin/python3", str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(W), "--primary", "oikos", "--secondary", "civic", "--scale", "2",
                    "-o", str(out)], cwd=ROOT, check=True, capture_output=True)
    return r


def build_asclepeion():
    """Write the Asclepeion's layout and its 2x render; check its spots and
    that it renders the same on three primaries (civic borrows nothing)."""
    import subprocess
    import numpy as np
    from PIL import Image
    import civic_tiles as ct
    ct.define()
    r = asclepeion_room()
    blocks = r.blocks()
    W, H = ASCLEPEION["size"]

    def solid(x, y):
        return not (0 <= x < W and 0 <= y < H) or bool(blocks[y * W + x] & 0x0C00)
    start = ASCLEPEION["spots"][0][2][0]
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and not solid(*n):
                seen.add(n)
                todo.append(n)
    dirs = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    for spot in ASCLEPEION["spots"]:
        kind, label = spot[0], spot[1]
        if kind == "warp":
            for t in spot[2]:
                assert ct.METATILES[ct.BY_NAME[r.grid[t[1]][t[0]]]]["behavior"] == "MB_SOUTH_ARROW_WARP", label
        elif kind == "npc":
            assert not solid(*spot[2]) and spot[2] in seen, f"asclepeion: {label} at {spot[2]} is unreachable"
        elif kind in ("bg", "perch"):
            fx, fy, facing = spot[3]
            assert (fx, fy) in seen, f"asclepeion: {label} is read from {(fx, fy)}, which is unreachable"
            dx, dy = dirs[facing]
            tx, ty = fx + dx, fy + dy
            if kind == "perch" and ct.METATILES[ct.BY_NAME[r.grid[ty][tx]]]["behavior"] == "MB_COUNTER":
                tx, ty = tx + dx, ty + dy       # talked to across the counter
            assert (tx, ty) == spot[2], f"asclepeion: {label}: {(fx, fy)} facing {facing} misses {spot[2]}"
    d = ROOT / "data/layouts" / ASCLEPEION["layout"]
    blocks.tofile(d / "map.bin")
    np.array([(ct.FIRST_ID + ct.BY_NAME["void"]) | 0x0400] * 4, "<u2").tofile(d / "border.bin")
    out = {}
    for prim in ("oikos", "aethos", "building"):
        png = ROOT / f"build/render/eleusa_asclepeion_{prim}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["/usr/bin/python3", str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(d / "map.bin"),
                        "--width", str(W), "--primary", prim, "--secondary", "civic", "--scale", "2",
                        "-o", str(png)], cwd=ROOT, check=True, capture_output=True)
        out[prim] = np.array(Image.open(png).convert("RGB"))
    assert all(np.array_equal(out["oikos"], v) for v in out.values()), "asclepeion: renders differ by primary"
    Image.fromarray(out["oikos"]).save(ROOT / "design/phase2/img" / ASCLEPEION["render"])
    import ergasteria_build as EB
    civic = EB.RoomSet("civic", "gTileset_Civic", EB.EA, tiles_doc=ROOT / "design/phase1/TILES_civic.md")
    EB.update_layouts_json(civic, {ASCLEPEION["layout"]: (W, H)})
    print(f"civic: eleusa asclepeion {W}x{H} -> data/layouts/{ASCLEPEION['layout']}, "
          f"design/phase2/img/{ASCLEPEION['render']}")


GALLERY = ROOT / "design/phase2/img/batch4_rooms_gallery.png"


def write_gallery():
    """The six rooms' 2x renders on one sheet, titled, in the style of the
    batch 2 gallery: design/phase2/img/batch4_rooms_gallery.png."""
    from PIL import Image, ImageDraw
    order = [(ASCLEPEION["render"], "The Asclepeion"), ("eleusa_agora.png", "The Agora stall"),
             ("eleusa_keleos.png", "The house of Keleos"), ("eleusa_granary.png", "The granary-keeper's house"),
             ("eleusa_poets.png", "Euphorion's house"), ("eleusa_farmhouse.png", "Dysaules's farmhouse")]
    imgs = [(Image.open(ROOT / "design/phase2/img" / f).convert("RGB"), t) for f, t in order]
    pad, title, width = 16, 18, 1200
    rows, row, x = [], [], pad
    for im, t in imgs:
        if row and x + im.width + pad > width:
            rows.append(row)
            row, x = [], pad
        row.append((im, t))
        x += im.width + pad
    rows.append(row)
    height = pad + sum(title + max(im.height for im, _ in r) + pad for r in rows)
    width = max(pad + sum(im.width + pad for im, _ in r) for r in rows)
    sheet = Image.new("RGB", (width, height), (30, 26, 26))
    d = ImageDraw.Draw(sheet)
    y = pad
    for r in rows:
        x = pad
        for im, t in r:
            d.text((x, y), t, fill=(232, 208, 144))
            sheet.paste(im, (x, y + title))
            x += im.width + pad
        y += title + max(im.height for im, _ in r) + pad
    sheet.save(GALLERY)
    print(f"gallery: {GALLERY.relative_to(ROOT)}")


def build_all():
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import ergasteria_build as EB
    import limen_build
    args = EB.parse_args()
    EB.build(limen_build.LIMEN, args)
    EB.build(limen_build.DOMOS, args)
    if not args.no_compile:
        build_asclepeion()
        write_gallery()


if __name__ == "__main__":
    build_all()
