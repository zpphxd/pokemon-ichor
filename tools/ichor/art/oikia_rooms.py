#!/usr/bin/env python3
"""Room layouts for the Phase 1 homes, built from the oikia tileset.

Each room is a grid plus a list of placements:
  grid    one string per row. 'W' is back wall (the first W in a column draws
          the wall's upper half, the second its lower half), '.' is floor,
          '#' is void (outside the room).
  floor   floor material: terracotta, boards or flags
  wall    wall style: red (red ochre dado) or blue (Aegean dado)
  rugs    (design, x, y, w, h) woven rugs; walkable, drawn under furniture
  stamps  (stamp name, x, y): the stamp's top-left cell
  spots   named tiles the script needs (NPC spots, bg events, warps)

oikia_build.py composes these into metatiles and writes the layouts to
design/phase1/rooms/<name>.bin. Coordinates are (x, y) in metatiles.
"""

ROOMS = {
    # ------------------------------------------------------------------
    "players_house_1f": {
        "title": "Player's house, 1F (Melitta's hall and kitchen)",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWW",
            "WWWWWWWWWWWW",
            "............",
            "............",
            "............",
            "............",
            "............",
            "............",
            "............",
        ],
        "rugs": [("red", 4, 4, 4, 3)],
        "stamps": [
            ("pithos", 0, 2),
            ("soot", 1, 0),
            ("hearth", 1, 2),
            ("honey_shelf", 3, 0),
            ("pots", 3, 2),
            ("altar", 5, 1),
            ("window", 6, 0),
            ("loom", 7, 0),
            ("niche", 9, 0),
            ("kalathos", 9, 2),
            ("stairs_up_r", 10, 0),
            ("table", 5, 5),
            ("klismos_r", 4, 5),
            ("klismos_l", 7, 5),
            ("kline", 9, 5),
            ("lampstand", 11, 5),
            ("amphora", 0, 5),
            ("myrtle", 11, 7),
            ("mat", 5, 8),
        ],
        "spots": {
            "door (south-arrow warps)": [(5, 8), (6, 8)],
            "stairs up (warp)": [(10, 2)],
            "Mom, at the hearth": [(3, 3)],
            "hearth (bg, face north from (1,4)/(2,4) or west from (3,2)... see notes)": [(1, 3), (2, 3)],
            "Mom's loom (bg, face north)": [(7, 2), (8, 2)],
            "honey shelf (bg, face north)": [(3, 1), (4, 1)],
            "altar of Hestia (bg, face north)": [(5, 2)],
        },
    },
    # ------------------------------------------------------------------
    "players_house_2f": {
        "title": "Player's house, 2F (the player's room)",
        "floor": "boards",
        "wall": "red",
        "grid": [
            "WWWWWWWWWW",
            "WWWWWWWWWW",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
        ],
        "rugs": [("blue", 5, 4, 3, 2)],
        "stamps": [
            ("scrolls", 0, 1),
            ("window", 2, 0),
            ("klepsydra", 4, 0),
            ("chest", 5, 1),
            ("niche_horse", 7, 0),
            ("stairs_down", 8, 0),
            ("lampstand", 9, 2),
            ("desk", 0, 4),
            ("klismos_l", 2, 4),
            ("kline", 3, 5),
            ("knucklebones", 6, 5),
            ("myrtle", 0, 6),
            ("amphora_plain", 9, 6),
        ],
        "spots": {
            "stairs down (warp)": [(8, 1)],
            "stair gate (coord event)": [(8, 2)],
            "new-game start, by the kline": [(5, 5)],
        },
    },
    # ------------------------------------------------------------------
    "kydippe_house": {
        "title": "Kydippe's house (Elaia)",
        "floor": "flags",
        "wall": "red",
        "grid": [
            "WWWWWWWWWW",
            "WWWWWWWWWW",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
        ],
        "rugs": [("red", 3, 4, 3, 2)],
        "stamps": [
            ("herbs", 0, 0),
            ("window", 2, 0),
            ("herbs", 3, 0),
            ("jar_shelf", 5, 0),
            ("niche", 7, 0),
            ("pithos", 9, 1),
            ("klismos_r", 1, 2),
            ("kalathos", 8, 2),
            ("table_round", 4, 4),
            ("stool", 3, 5),
            ("kline", 7, 5),
            ("lampstand", 9, 5),
            ("amphora", 0, 4),
            ("myrtle", 0, 6),
            ("mat", 4, 7),
        ],
        "spots": {},
    },
    # ------------------------------------------------------------------
    "fishers_house": {
        "title": "The Fisher's house (Akti)",
        "floor": "boards",
        "wall": "blue",
        "grid": [
            "WWWWWWWWWW",
            "WWWWWWWWWW",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
        ],
        "rugs": [],
        "stamps": [
            ("nets", 0, 0),
            ("window", 3, 0),
            ("trident", 5, 0),
            ("boat", 6, 0),
            ("amphora_plain", 8, 1),
            ("window", 9, 0),
            ("fish_basket", 0, 2),
            ("fish_basket", 1, 2),
            ("table", 4, 4),
            ("stool", 3, 4),
            ("stool", 6, 4),
            ("chest", 0, 4),
            ("pots", 0, 6),
            ("kline", 7, 5),
            ("pithos", 9, 2),
            ("mat", 4, 7),
        ],
        "spots": {},
    },
}

# ----------------------------------------------------------------------
# Catalog layouts. Not delivered as rooms: they make sure every stamp exists
# on every floor and wall it can stand on, so the director can re-dress rooms
# in Porymap, and they render the reference sheet.
# ----------------------------------------------------------------------

WALL_HUNG = ["window", "niche", "niche_horse", "klepsydra", "herbs", "honey_shelf",
             "jar_shelf", "trident", "boat", "nets", "stairs_down"]
BACK = ["loom", "chest", "scrolls", "altar", "stairs_up", "stairs_up_r"]
FREE = ["kline", "klismos_r", "klismos_l", "stool", "table", "table_round", "desk",
        "amphora", "amphora_plain", "pithos", "pots", "myrtle", "kalathos",
        "fish_basket", "knucklebones", "lampstand", "column", "mat"]


def _row_pack(names, stamps, width, y0, x0=1, gap=1):
    """Lay stamps out left to right in rows starting at y0."""
    out, x, y, rowh = [], x0, y0, 0
    for n in names:
        w, h = stamps[n]["w"], stamps[n]["h"]
        if x + w > width:
            x, y, rowh = x0, y + rowh + gap, 0
        out.append((n, x, y))
        x += w + gap
        rowh = max(rowh, h)
    return out, y + rowh


def catalog(stamps):
    """Catalog layouts, one per floor material, plus the blue-wall strip."""
    cats = {}
    width = 24
    for floor, wall in (("terracotta", "red"), ("boards", "blue"), ("flags", "red")):
        placed = []
        # wall-hung pieces across the back wall
        x = 0
        for n in WALL_HUNG:
            placed.append((n, x, 0))
            x += stamps[n]["w"]
        placed.append(("soot", x, 0))
        placed.append(("hearth", x, 2))
        x += 2
        # pieces that stand against the back wall
        for n in BACK:
            h = stamps[n]["h"]
            placed.append((n, x, 3 - h))
            x += stamps[n]["w"]
        width = max(width, x)
        free, bottom = _row_pack(FREE, stamps, width, 5)
        placed += free
        rug_y = bottom + 1
        height = rug_y + 4
        grid = ["W" * width, "W" * width] + ["." * width for _ in range(height - 2)]
        cats[f"catalog_{floor}"] = {
            "title": f"Catalog on {floor}, {wall} wall",
            "floor": floor,
            "wall": wall,
            "grid": grid,
            "rugs": [("red", 1, rug_y, 3, 3), ("blue", 5, rug_y, 3, 3)],
            "stamps": placed,
            "spots": {},
        }
    return cats
