#!/usr/bin/env python3
"""Build Olympus: the Propylaia, the four seats of the Pantheon, the summit and
the Hall of Heroes (design/LEAGUE.md). Each room is drawn on its own tileset, so
each seat has its own floor, walls and signature motif:

  Olympus_Propylaia       gTileset_Civic         the League's lobby: the healer and Pithos, the merchant, the guard
  Olympus_SeatOf*         gTileset_Seat*         the four seats (tools/ichor/maps/pantheon_halls.py)
  Olympus_Summit          gTileset_Aegina        Zeus's altar, the temple of the Twelve
  Olympus_HallOfHeroes    gTileset_Civic         the cella and its record stone

The Elite Four pattern (each seat's entrance locks, its far door opens on a
win) is in the maps' scripts; this file only places the doors' cells, and the
ids the scripts swap are listed in DOORS for scripts.pory to use.

Usage: /usr/bin/python3 tools/ichor/maps/olympus.py [--render DIR] [--tag TAG] [--only NAME,...]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import league_lib as L  # noqa: E402
from league_lib import Grid, noise  # noqa: E402

GFX = "OBJ_EVENT_GFX_ICHOR_"


def seat_fields(music="MUS_NONE"):
    return dict(map_type="MAP_TYPE_INDOOR", weather="WEATHER_NONE", show_map_name=False,
                allow_cycling=False, allow_escaping=False, music=music, ichor_kind="interior")


# ---------------------------------------------------------------------------
# The Propylaia: Hestia's hearth (gTileset_TempleHestia, design/phase1/TILES_temple.md)
# ---------------------------------------------------------------------------
H_VOID, H_FLOOR, H_VEIN = 0x200, 0x201, (0x202, 0x203)
H_RUNNER, H_RUNNER_S, H_RUNNER_N = 0x204, 0x205, 0x23B
H_TOP, H_CORNER_L, H_CORNER_R, H_SIDE_L, H_SIDE_R = 0x212, 0x213, 0x214, 0x215, 0x216
H_FRIEZE = (0x218, 0x219, 0x21A, 0x21B)
H_HESTIA = (0x21C, 0x21D)
H_LOWER, H_LOWER_WREATH, H_LOWER_LAMPS = 0x217, 0x21E, 0x21F
H_PILASTER = (0x220, 0x228)
H_DOOR = (0x221, 0x229)
H_MAT = (0x20E, 0x20F, 0x210)
H_COLUMN = (0x230, 0x238)
H_STELE = (0x231, 0x239)
H_AMPHORA, H_AMPHORA_RED, H_LAMPS = 0x232, 0x233, 0x235
H_LAUREL = (0x234, 0x23C)
H_TABLE = ((0x236, 0x237), (0x23E, 0x23F))
H_BASIN = (0x283, 0x284)
H_LAMPSTAND = (0x285, 0x286)
H_BRAZIER_LIT, H_BRAZIER_HEARTH_LIT = 0x241, 0x24B
H_HEARTH = [[0x250 + r * 8 + c for c in range(5)] for r in range(5)]
H_ROSETTE = 0x288


def propylaia():
    """The Propylaia, rebuilt grand on 2026-11-18 (design/maps/Olympus_Pantheon.md): the
    League's lobby, the calm before the Pantheon. A wide columned hall on
    gTileset_Civic: the standard Asclepeion station with the Pithos beside it
    (civic_rooms.station_cells, pithos_cells) on the west, the merchant's stall on
    the east, two colonnades, statues down the walls, Hestia's hearth (the great
    mosaic between braziers) in the middle and the inner door in the back wall."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
    import civic_rooms as CR
    import civic_tiles as ct
    ct.define() if not ct.METATILES else None
    W, H = 27, 17
    r = CR.Room("olympus_propylaia", W, H, CR.checker("asc_floor_a", "asc_floor_b"))
    r.row(0, 0, ["asc_wall_top_l"] + ["asc_wall_top"] * (W - 2) + ["asc_wall_top_r"])
    r.row(1, 0, ["asc_wall_l"] + ["asc_wall"] * (W - 2) + ["asc_wall_r"])
    r.row(2, 0, [("asc_floor_a_sh" if x % 2 == 0 else "asc_floor_b_sh") for x in range(W)])
    for y in range(2, H - 1):
        r.set(0, y, "asc_wall_l")
        r.set(W - 1, y, "asc_wall_r")
    for x in range(W):
        r.set(x, H - 1, "void")
    # the healer's station, the standard one, and the Pithos beside it (west)
    hx, hy = 6, 2
    CR.healer_station(r, hx, hy)
    CR.pithos(r, 1)
    # the merchant's stall (east): awning, the counter with the scale, shelves of goods
    r.put("ago_awning", 18, 0, 3, 2)
    r.row(2, 18, ["ago_counter_l", "ago_counter_staff", "ago_counter_r"])
    r.row(3, 18, ["ago_counter_front_l", "ago_counter_front_m", "ago_counter_front_r"])
    for x in (21, 22):
        r.put("ago_shelf", x, 0, 1, 3)
    r.put("ago_amphora", 24, 1, 1, 2)
    r.set(17, 3, "ago_basket_pomegranates")
    r.set(23, 3, "ago_basket_figs")
    # the inner door to the Pantheon, between braziers and the Twelve's relief
    r.set(13, 1, "void")
    r.set(13, 0, "asc_wall_top")
    r.put_checkered("asc_brazier", 11, 2, 1, 2)
    r.put_checkered("asc_brazier", 15, 2, 1, 2)
    # Hestia's hearth: the great mosaic, braziers round it
    r.put("asc_mosaic", 12, 8, 3, 3)
    r.put_checkered("asc_brazier", 10, 8, 1, 2)
    r.put_checkered("asc_brazier", 16, 8, 1, 2)
    # two colonnades down the hall
    for x in (4, 22):
        for y0 in (5, 9, 13):
            if y0 + 2 < H - 1:
                r.put_checkered("asc_column", x, y0, 1, 3)
    # statues of the heroes along the side walls, couches and benches to rest on
    for y0 in (5, 10):
        r.put("asc_statue", 1, y0, 1, 3)
        r.put("asc_statue", W - 2, y0, 1, 3)
    r.put_checkered("asc_kline", 7, 12, 2, 2)
    r.put_checkered("asc_kline", 18, 12, 2, 2)
    r.put_checkered("asc_bench", 7, 5, 2, 1)
    r.put_checkered("asc_bench", 18, 5, 2, 1)
    r.put_checkered("asc_snake", 3, 13)
    g = Grid("Olympus_Propylaia", W, H, primary="gTileset_Oikos", secondary="gTileset_Civic", cat=None)
    blocks = r.blocks().reshape(H, W)
    for y in range(H):
        for x in range(W):
            b = int(blocks[y, x])
            g.set(x, y, b & 0x3FF, bool(b & 0x0400), "room")
    r.set(13, H - 1, "asc_mat")
    g.set(13, H - 1, ct.FIRST_ID + ct.BY_NAME["asc_mat"], False, "mat")
    # people: the healer at her station, the merchant at the counter, the guards at the door
    g.person("HEALER", "HEALER", hx, hy, "Healer", facing="DOWN")
    g.person("MERCHANT", "MERCHANT", 19, 2, "Merchant", facing="DOWN")
    g.person("GUARD", "HOPLITE", 13, 2, "Guard", facing="DOWN")
    g.person("GUARD_B", "HOPLITE", 14, 3, "GuardB", facing="LEFT")
    g.person("PILGRIM", "PILGRIM", 9, 13, "Pilgrim", facing="RIGHT")
    g.warp(13, H - 1, "Ascent_3F", 0)
    g.sign(13, 1, "InnerDoor", facing="NORTH")
    for x in range(12, 15):
        for y in range(8, 11):
            if (x, y) != (13, 9):
                g.sign(x, y, "Hearth")
    g.sign(1, 7, "StatueWest", facing="WEST") if False else None
    g.save([ct.FIRST_ID | 0x400] * 4, seat_fields("MUS_ICHOR_ASCLEPEION"))
    g.check((13, H - 2), [("healer", (hx, hy + 2)), ("merchant", (19, 4)), ("guard", (13, 2)),
                          ("pithos", (1, 3))])
    return g, [("hall", 13, 9), ("healer", 6, 6), ("merchant", 19, 6), ("door", 13, 4)]


# ---------------------------------------------------------------------------
# The four seats: tools/ichor/maps/pantheon_halls.py, each on its own tileset
# (tools/ichor/art/pantheon_build.py), since 2026-11-18.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# The summit: Zeus's altar and the temple of the Twelve (gTileset_Aegina)
# ---------------------------------------------------------------------------
SNOW_ROCK = (0x0B4, 0x0B5, 0x0B6, 0x0B7, 0x0BE, 0x0BF, 0x0D7)
SUMMIT_TEMPLE = (11, 2)
SUMMIT_ALTAR = (13, 11)
SUMMIT_GATE = (12, 20)


def summit():
    W, H = 28, 26
    g = Grid("Olympus_Summit", W, H, secondary="gTileset_Aegina", cat="aegina", base=0x001, base_kind="dry")
    g.fill("snow", 0, 0, W - 1, H - 1)
    g.rows("dry", 3, 1, ["...######################...",
                         "..########################..",
                         ".##########################.",
                         ".##########################.",
                         "############################",
                         "############################",
                         "############################",
                         "############################",
                         ".##########################.",
                         ".##########################.",
                         "..########################..",
                         "..#########################.",
                         "...#######################..",
                         "....#####################...",
                         ".....###################....",
                         "......#################.....",
                         ".......###############......",
                         "........#############.......",
                         "..........#########.........",
                         "...........#######..........",
                         "............######..........",
                         "............######..........",
                         "............######..........",
                         "............######.........."])
    for y in range(H):
        for x in range(W):
            if g.g[y][x] == "snow":
                g.set(x, y, SNOW_ROCK[noise(x, y, 61) % len(SNOW_ROCK)], True, "snow")
            else:
                n = noise(x, y, 62)
                g.set(x, y, 0x2D9 if noise(x // 2, y // 2, 62) < 22 else 0x001, False, "dry")
    # the sacred way from the propylon to the altar
    for y in range(13, H):
        for x in (13, 14):
            g.set(x, y, 0x1D9, False, "way")
    for y in range(8, 14):
        for x in range(10, 18):
            g.set(x, y, 0x209, False, "precinct")
    # the precinct's terrace: a dry-stone lip along its south edge, the sacred way through it
    for x in range(9, 19):
        if x not in (13, 14):
            g.set(x, 14, 0x0D5 if x == 9 else 0x0D6 if x == 18 else 0x087, True, "lip")
    for x, y in ((6, 4), (20, 4), (3, 10), (24, 15), (7, 19), (19, 21), (10, 22), (8, 1), (12, 1), (18, 1), (23, 1)):
        g.set(x, y, 0x0E0, True, "boulder")
    g.piece("temple_aphaia", *SUMMIT_TEMPLE)
    g.piece("altar_zeus", *SUMMIT_ALTAR)
    g.piece("gate", SUMMIT_GATE[0], SUMMIT_GATE[1])
    g.piece("kolona", 4, 6)
    g.piece("kolona_ruins", 22, 9)
    g.piece("pine", 5, 13)
    g.piece("pine", 21, 12)
    g.piece("scrub", 8, 16)
    g.piece("scrub", 18, 17)
    for x, y in ((9, 9), (18, 9)):
        g.set(x, y - 1, L.A_TRIPOD_TOP, False)
        g.set(x, y, L.A_TRIPOD_BASE, True)
    g.set(9, 13, L.A_HERM, True)
    g.set(18, 13, L.A_HERM, True)
    door = (SUMMIT_TEMPLE[0] + 3, SUMMIT_TEMPLE[1] + 3)
    g.set(door[0], door[1], g.mt[door[1], door[0]], False, "doorway")
    g.person("ARISTEIDES", "ELDER_M", 13, 13, "Aristeides", facing="DOWN", flag="FLAG_ICHOR_HIDE_ARCHON_SUMMIT")
    g.warp(13, H - 1, "Olympus_SeatOfHera", 1)
    g.warp(door[0], door[1], "Olympus_HallOfHeroes", 0)
    g.trigger(door[0], door[1], "TempleDoor")
    g.sign(SUMMIT_ALTAR[0], SUMMIT_ALTAR[1] + 1, "Altar", facing="NORTH")
    g.sign(SUMMIT_ALTAR[0] + 1, SUMMIT_ALTAR[1] + 1, "Altar", facing="NORTH")
    g.save([SNOW_ROCK[0] | 0x400, SNOW_ROCK[1] | 0x400, SNOW_ROCK[4] | 0x400, SNOW_ROCK[5] | 0x400],
           dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SUNNY", show_map_name=True, allow_cycling=False,
                allow_escaping=False, music="MUS_NONE", ichor_kind="interior"))
    g.check((13, H - 1), [("altar", (13, 13)), ("temple door", (door[0], door[1] + 1))])
    return g, [("gate", 13, 21), ("altar", 13, 12), ("temple", 14, 6)]


# ---------------------------------------------------------------------------
# The Hall of Heroes: the cella of the Twelve (gTileset_Civic)
# ---------------------------------------------------------------------------
CV = dict(void=0x200, floor_a=0x201, floor_b=0x202, floor_a_sh=0x203, floor_b_sh=0x204,
          top=0x205, top_l=0x206, top_r=0x207, wall=0x208, wall_l=0x209, wall_r=0x20A,
          column=(0x20B, 0x20C, 0x20D), relief=(0x219, 0x21A), statue=(0x227, 0x228, 0x229),
          brazier=(0x23E, 0x23F), mat=0x242, mosaic=[[0x230, 0x231, 0x232], [0x233, 0x234, 0x235], [0x236, 0x237, 0x238]],
          votive=(0x21B, 0x21C))


def hall_of_heroes():
    W, H = 15, 18
    g = Grid("Olympus_HallOfHeroes", W, H, secondary="gTileset_Civic", cat=None)
    for y in range(H):
        for x in range(W):
            a = (x + y) % 2 == 0
            g.set(x, y, (CV["floor_a_sh"] if a else CV["floor_b_sh"]) if y == 2 else
                  (CV["floor_a"] if a else CV["floor_b"]), False, "floor")
    for x in range(W):
        g.set(x, 0, CV["top_l"] if x == 0 else CV["top_r"] if x == W - 1 else CV["top"], True)
        g.set(x, 1, CV["wall_l"] if x == 0 else CV["wall_r"] if x == W - 1 else CV["wall"], True)
    for y in range(2, H - 1):
        g.set(0, y, CV["wall_l"], True)
        g.set(W - 1, y, CV["wall_r"], True)
    for x in range(W):
        g.set(x, H - 1, CV["void"], True)
    g.set(7, H - 1, CV["mat"], False, "mat")
    # the record stone at the head of the nave, braziers either side
    g.set(7, 1, CV["relief"][0], True)
    g.set(7, 2, CV["relief"][1], True)
    for x in (5, 9):
        g.set(x, 2, CV["brazier"][0], False)
        g.set(x, 3, CV["brazier"][1], True)
    # two colonnades, and the heroes of the age along the walls
    for y in (6, 10, 14):
        for x in (4, 10):
            g.set(x, y - 1, CV["column"][0], False)
            g.set(x, y, CV["column"][1], False)
            g.set(x, y + 1, CV["column"][2], True)
    for y in (4, 8, 12):
        for x in (1, 13):
            g.set(x, y, CV["statue"][0], True)
            g.set(x, y + 1, CV["statue"][1], True)
            g.set(x, y + 2, CV["statue"][2], True)
    g.person("ARISTEIDES", "ELDER_M", 8, 16, "Aristeides", facing="UP", flag="FLAG_ICHOR_HIDE_ARCHON_SUMMIT")
    g.warp(7, H - 1, "Olympus_Summit", 1)
    g.save([CV["void"] | 0x400] * 4, seat_fields("MUS_HALL_OF_FAME_ROOM"))
    g.check((7, H - 2), [("record stone", (7, 3))])
    return g, [("nave", 7, 9)]


import pantheon_halls  # noqa: E402

BUILDERS = {"Propylaia": propylaia, **pantheon_halls.BUILDERS, "Hall": hall_of_heroes}
# The summit moved to gTileset_Chion on 2026-11-18 (tools/ichor/maps/ascent_peak.py);
# summit() below is the old Aegina build, kept for reference and no longer run.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render")
    ap.add_argument("--tag", default="")
    ap.add_argument("--only", default=",".join(BUILDERS))
    args = ap.parse_args()
    for key in args.only.split(","):
        g, views = BUILDERS[key]()
        if args.render:
            print(L.render(g, args.render, views, args.tag))


if __name__ == "__main__":
    main()
