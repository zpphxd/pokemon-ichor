#!/usr/bin/env python3
"""Build Olympus: the Propylaia, the four seats of the Pantheon, the summit and
the Hall of Heroes (design/LEAGUE.md). Each room is drawn on its own tileset, so
each seat has its own floor, walls and signature motif:

  Olympus_Propylaia       gTileset_TempleHestia  the hearth, the healer, the guard
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
    W, H = 17, 16
    g = Grid("Olympus_Propylaia", W, H, primary="gTileset_Oikos", secondary="gTileset_TempleHestia",
             cat=None, base=H_FLOOR, base_kind="floor")
    for y in range(H):
        for x in range(W):
            g.set(x, y, H_VEIN[noise(x, y, 3) % 2] if noise(x, y, 7) < 18 else H_FLOOR, False, "floor")
    # walls: cornice, frieze, lower wall; the side walls down both edges
    g.set(0, 0, H_CORNER_L, True)
    g.set(W - 1, 0, H_CORNER_R, True)
    for x in range(1, W - 1):
        g.set(x, 0, H_TOP, True)
        g.set(x, 1, H_FRIEZE[x % 4], True)
        g.set(x, 2, H_LOWER_LAMPS if x in (3, 13) else H_LOWER_WREATH if x in (5, 11) else H_LOWER, True)
    for y in range(1, H - 1):
        g.set(0, y, H_SIDE_L, True)
        g.set(W - 1, y, H_SIDE_R, True)
    g.set(7, 1, H_HESTIA[0], True)
    g.set(9, 1, H_HESTIA[1], True)
    # the inner door to the Pantheon, between pilasters
    g.set(8, 1, H_DOOR[0], True)
    g.set(8, 2, H_DOOR[1], True)
    for x in (6, 10):
        g.set(x, 1, H_PILASTER[0], True)
        g.set(x, 2, H_PILASTER[1], True)
    # the bottom: void, and the mat
    for x in range(W):
        g.set(x, H - 1, H_VOID, True)
    for i, x in enumerate((7, 8, 9)):
        g.set(x, H - 1, H_MAT[i], False, "mat")
    # the great hearth in its pool of light, and the runner through it
    g.stamp(6, 6, H_HEARTH, solid=[[False] * 5] + [[False, True, True, True, False]] * 3 + [[False] * 5])
    for y in range(3, 6):
        g.set(8, y, H_RUNNER, False)
    g.set(8, 3, H_RUNNER_N, False)
    for y in range(11, H - 1):
        g.set(8, y, H_RUNNER, False)
    # colonnades down both sides
    for y in (4, 8, 12):
        for x in (3, 13):
            g.set(x, y, H_COLUMN[0], True)
            g.set(x, y + 1, H_COLUMN[1], True)
    # the guard's lampstands at the door, the lustral basin at the way in
    for x in (6, 10):
        g.set(x, 3, H_LAMPSTAND[0], True)
        g.set(x, 4, H_LAMPSTAND[1], True)
    g.set(5, 12, H_BASIN[0], True)
    g.set(5, 13, H_BASIN[1], True)
    g.set(11, 12, H_STELE[0], True)
    g.set(11, 13, H_STELE[1], True)
    # the healer's corner (west) and the merchant's table (east)
    g.set(1, 5, H_LAUREL[0], True)
    g.set(1, 6, H_LAUREL[1], True)
    g.set(15, 5, H_LAUREL[0], True)
    g.set(15, 6, H_LAUREL[1], True)
    g.set(2, 9, H_LAMPS, True)
    g.stamp(14, 9, H_TABLE)
    g.set(15, 12, H_AMPHORA, True)
    g.set(1, 12, H_AMPHORA_RED, True)
    g.set(2, 7, H_ROSETTE, False)
    # events
    g.person("HEALER", "HEALER", 2, 7, "Healer", facing="RIGHT")
    g.person("MERCHANT", "MERCHANT", 14, 8, "Merchant", facing="DOWN")
    g.person("GUARD", "HOPLITE", 8, 3, "Guard", facing="DOWN")
    g.person("GUARD_B", "HOPLITE", 9, 4, "GuardB", facing="LEFT")
    g.warp(8, H - 1, "Ascent_3F", 0)
    g.sign(8, 2, "InnerDoor", facing="NORTH")
    g.sign(11, 13, "Stele")
    for x in range(7, 10):
        for y in range(7, 10):
            if (x, y) != (8, 8):
                g.sign(x, y, "Hearth")
    g.save([H_VOID | 0x400] * 4, seat_fields("MUS_ICHOR_ASCLEPEION"))
    g.check((8, H - 2), [("healer", (2, 7)), ("merchant", (14, 8)), ("guard", (8, 3))])
    return g, [("hall", 8, 8)]


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
