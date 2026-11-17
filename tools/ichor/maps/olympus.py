#!/usr/bin/env python3
"""Build Olympus: the Propylaia, the four seats of the Pantheon, the summit and
the Hall of Heroes (design/LEAGUE.md). Each room is drawn on its own tileset, so
each seat has its own floor, walls and signature motif:

  Olympus_Propylaia       gTileset_TempleHestia  the hearth, the healer, the guard
  Olympus_SeatOfAres      gTileset_Labyrinth     two files of bronze kouroi
  Olympus_SeatOfPoseidon  gTileset_Aegina        the trireme in the sacred basin
  Olympus_SeatOfAthena    gTileset_TempleHermes  scroll walls and the rostrum
  Olympus_SeatOfHera      gTileset_TempleDemeter the throne behind the serpent pits
  Olympus_Summit          gTileset_Aegina        Zeus's altar, the temple of the Twelve
  Olympus_HallOfHeroes    gTileset_Civic         the cella and its record stone

The Elite Four pattern (each seat's entrance locks, its far door opens on a
win) is in the maps' scripts; this file only places the doors' cells, and the
ids the scripts swap are listed in DOORS for scripts.pory to use.

Usage: /usr/bin/python3 tools/ichor/maps/olympus.py [--render DIR] [--tag TAG] [--only NAME,...]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import league_lib as L  # noqa: E402
from league_lib import ROOT, Grid, noise  # noqa: E402

GFX = "OBJ_EVENT_GFX_ICHOR_"


def seat_fields(music="MUS_NONE"):
    return dict(map_type="MAP_TYPE_INDOOR", weather="WEATHER_NONE", show_map_name=False,
                allow_cycling=False, allow_escaping=False, music=music)


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
# The seat of Ares: bronze files under a grey arcade (gTileset_Labyrinth)
# ---------------------------------------------------------------------------
LAB = None


def lab(key, name):
    s = LAB[key]
    cx, cy = s["names"][name]
    return s["ids"][cy][cx]


def lab_col(key, name):
    """An arcade column's three cells, top to bottom."""
    s = LAB[key]
    cx, _ = s["names"][name]
    return [s["ids"][r][cx] for r in range(s["h"])]


ARES_DOOR = (9, 2)


def seat_of_ares():
    global LAB
    LAB = L.catalog("labyrinth")
    W, H = 19, 20
    g = Grid("Olympus_SeatOfAres", W, H, primary="gTileset_Oikos", secondary="gTileset_Labyrinth", cat=None)
    for y in range(H):
        for x in range(W):
            if y == 3:
                mid = lab("floor", "shade_l" if (x + y) % 2 == 0 else "shade_r")
            else:
                mid = lab("floor", "slab_l" if (x + y) % 2 == 0 else "slab_r")
                if (x + y) % 2 == 0 and noise(x, y, 5) < 6:
                    mid = lab("floor", "labrys")
                elif (x + y) % 2 == 1 and noise(x, y, 6) < 6:
                    mid = lab("floor", "crack")
            g.set(x, y, mid, False, "floor")
    # the arcade: piers every fourth cell, the door through the middle pier
    for x in range(W):
        if x == 0:
            col = lab_col("arcade", "side_w")
        elif x == W - 1:
            col = lab_col("arcade", "side_e")
        elif x == ARES_DOOR[0]:
            col = lab_col("arcade", "door_pier")
        elif (x - 1) % 4 == 0:
            col = lab_col("arcade", "pier_sconce" if x in (5, 13) else "pier")
        else:
            col = lab_col("arcade", ("bay_l", "bay_m", "bay_r")[(x - 1) % 4 - 1])
        for y in range(3):
            g.set(x, y, col[y], True, "arcade")
    for y in range(3, H - 1):
        g.set(0, y, lab("edge", "wall_w"), True)
        g.set(W - 1, y, lab("edge", "wall_e"), True)
    for x in range(W):
        g.set(x, H - 1, lab("floor", "void"), True)
    g.set(9, H - 1, lab("edge", "sill_l"), False, "sill")
    g.set(10, H - 1, lab("edge", "sill_r"), False, "sill")
    # the crimson runner up the middle
    run = LAB["runner"]
    for y in range(4, H - 1):
        r = 0 if y == 4 else 2 if y == H - 2 else 1
        g.set(9, y, run["ids"][r][0], False, "runner")
        g.set(10, y, run["ids"][r][1], False, "runner")
    # two files of bronze hoplites, eyes front: the phalanx
    for y in (6, 9, 12, 15):
        for x in (3, 6, 13, 16):
            key = "auto_kouros" if (x + y) % 3 else "auto_kore"
            g.set(x, y, lab(key, "top"), True, "bronze")
            g.set(x, y + 1, lab(key, "base"), True, "bronze")
    for x in (7, 12):
        g.set(x, 4, lab("auto_lamp", "top"), True)
        g.set(x, 5, lab("auto_lamp", "base"), True)
    for x in (1, 17):
        g.set(x, 16, lab("auto_hound", "top"), True)
        g.set(x, 17, lab("auto_hound", "base"), True)
    # the door is shut until Brasidas falls (the scripts open it)
    g.solid[ARES_DOOR[1], ARES_DOOR[0]] = True
    g.person("BRASIDAS", "HOPLITE", 9, 4, "Brasidas", facing="DOWN")
    g.warp(9, H - 1, "Olympus_Propylaia", 0)
    g.warp(*ARES_DOOR, "Olympus_SeatOfPoseidon", 0)
    g.save([lab("floor", "void") | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("brasidas", (9, 4))])
    return g, [("hall", 9, 12), ("dais", 9, 4)]


# ---------------------------------------------------------------------------
# The seat of Poseidon: the wooden wall in the sacred basin (gTileset_Aegina)
# ---------------------------------------------------------------------------
POSEIDON_GATE = (8, 0)       # the gate piece's top-left; its walkable middle is x 9-10


def seat_of_poseidon():
    W, H = 20, 21
    g = Grid("Olympus_SeatOfPoseidon", W, H, secondary="gTileset_Aegina", cat="aegina",
             base=0x209, base_kind="quay")
    for y in range(H):
        for x in range(W):
            g.set(x, y, 0x209, False, "quay")
    # the basin and its trireme, lifted from Aegina's round harbor
    lay = next(l for l in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
               if l.get("id") == "LAYOUT_AEGINA_TOWN")
    src = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2").reshape(lay["height"], lay["width"])
    bx, by = 3, 5
    for j in range(10):
        for i in range(14):
            c = int(src[3 + j, 6 + i])
            mid = c & 0x3FF
            if 0x218 <= mid <= 0x225:          # the kaiki: moored elsewhere
                mid, c = 0x170, 0x170
            if j == 0 and i in (6, 7):         # close the harbor mouth to the north quay
                mid, c = 0x201, 0x201
            water = mid == 0x170 or mid in (0x247, 0x258, 0x25d, 0x270)
            g.set(bx + i, by + j, mid, bool(c & 0x400) or water, "basin")
    # cypress and stone pine close the court; the gate at the north
    for y in range(H):
        for x in (0, W - 1):
            g.set(x, y, L.A_CYPRESS[y % 2], True, "cypress")
    for x in range(1, W - 1):
        g.set(x, H - 1, L.A_CYPRESS[1], True)
        g.set(x, H - 2, L.A_CYPRESS[0], True) if x in (1, 2, 17, 18) else None
    for x in list(range(1, 8)) + list(range(12, W - 1)):
        g.set(x, 0, L.A_CYPRESS[0], True)
        g.set(x, 1, L.A_CYPRESS[1], True)
        if x in (1, 2, 3, 16, 17, 18):
            g.set(x, 2, L.A_CYPRESS[0] if x % 2 else 0x001, True)
    g.piece("gate", *POSEIDON_GATE)
    g.piece("gate_shut", POSEIDON_GATE[0] + 1, POSEIDON_GATE[1] + 2)
    # the way in: the pebble threshold
    g.set(9, H - 1, 0x024, False, "mat")
    g.set(10, H - 1, 0x024, False, "mat")
    g.piece("turtle_mosaic", 9, 16)
    for x, y in ((2, 7), (2, 11), (17, 7), (17, 11)):
        g.piece("bollard_line", x, y)
    g.piece("amphora_stack", 1, 15)
    g.piece("amphora_stack", 17, 15)
    g.piece("rope_coil", 2, 16)
    g.piece("rope_coil", 16, 3)
    g.set(4, 3, L.A_TRIPOD_TOP, False)
    g.set(4, 4, L.A_TRIPOD_BASE, True)
    g.set(15, 3, L.A_TRIPOD_TOP, False)
    g.set(15, 4, L.A_TRIPOD_BASE, True)
    g.person("THEMISTOKLES", "SAILOR", 9, 4, "Themistokles", facing="DOWN")
    g.warp(9, H - 1, "Olympus_SeatOfAres", 1)
    for x in (9, 10):
        g.trigger(x, 1, "ExitGate")
    g.set(16, 17, 0x003, True)
    g.sign(16, 17, "WoodenWall")
    g.save([L.A_CYPRESS[1] | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("themistokles", (9, 4))])
    return g, [("court", 10, 10), ("gate", 9, 4)]


# ---------------------------------------------------------------------------
# The seat of Athena: the library and the rostrum (gTileset_TempleHermes)
# ---------------------------------------------------------------------------
TH = dict(void=0x200, slab=0x201, vein_a=0x202, vein_b=0x203, worn=0x204,
          cornice=0x218, cornice_w=0x219, cornice_e=0x21A, side_w=0x21B, side_e=0x21C, acro=0x21E,
          frieze=0x227, frieze_lyre=0x224, lower=0x228, lower_torch=0x229, lower_niche=0x22A,
          lower_plaque=0x22B, side_face_w=0x22E, side_face_e=0x22F, mat=0x233,
          gate_shut=0x24C, gate_open=0x24D,
          ph_wall=((0x270, 0x271), (0x278, 0x279)), cab=((0x272, 0x273), (0x27A, 0x27B)),
          table=(0x280, 0x281), col=(0x284, 0x28C),
          dais=0x298, dais_roundel=0x299, dais_lip=0x29A, edge_w=0x29B, edge_e=0x29C, lectern=0x29D,
          dais_lamp=0x29E, riser=0x2A0, riser_w=0x2A1, riser_e=0x2A2, steps=0x2A3,
          torch=(0x260, 0x268), oil=0x263, basket=0x264)
ATHENA_GATE = (9, 2)


def seat_of_athena():
    W, H = 19, 21
    g = Grid("Olympus_SeatOfAthena", W, H, primary="gTileset_Oikos", secondary="gTileset_TempleHermes", cat=None)
    for y in range(H):
        for x in range(W):
            n = noise(x, y, 8)
            g.set(x, y, TH["vein_a"] if n < 8 else TH["vein_b"] if n < 14 else TH["slab"], False, "floor")
    for x in range(W):
        g.set(x, 0, TH["cornice_w"] if x == 0 else TH["cornice_e"] if x == W - 1 else
              TH["acro"] if x in (4, 14) else TH["cornice"], True)
    # the north wall: walls of scroll pigeonholes either side of the gate
    for x in range(1, W - 1):
        g.set(x, 1, TH["frieze_lyre"] if x == 9 else TH["frieze"], True)
        g.set(x, 2, TH["lower_torch"] if x in (8, 10) else TH["lower"], True)
    for x0 in (1, 3, 5, 12, 14, 16):
        g.stamp(x0, 1, TH["ph_wall"])
    g.set(*ATHENA_GATE, TH["gate_shut"], True, "gate")
    for y in range(1, H - 1):
        g.set(0, y, TH["side_face_w"] if y < 3 else TH["side_w"], True)
        g.set(W - 1, y, TH["side_face_e"] if y < 3 else TH["side_e"], True)
    for x in range(W):
        g.set(x, H - 1, TH["void"], True)
    g.set(9, H - 1, TH["mat"], False, "mat")
    # the rostrum across the head of the hall
    for x in range(5, 14):
        g.set(x, 3, TH["dais_roundel"] if x == 10 else TH["dais_lamp"] if x in (6, 12) else TH["dais"],
              x in (6, 12), "dais")
        g.set(x, 4, TH["dais_lip"], False, "dais")
        g.set(x, 5, TH["steps"] if x in (8, 9, 10) else TH["riser"], x not in (8, 9, 10), "dais")
    g.set(5, 4, TH["edge_w"], True)
    g.set(13, 4, TH["edge_e"], True)
    g.set(5, 5, TH["riser_w"], True)
    g.set(13, 5, TH["riser_e"], True)
    g.set(10, 4, TH["lectern"], True, "lectern")
    # the hall: cabinets of scrolls in rows, reading tables between, columns on the aisle
    for y in (8, 12, 16):
        for x in (1, 4, 13, 16):
            g.stamp(x, y, TH["cab"])
    for y in (10, 14):
        g.stamp(2, y, [list(TH["table"])])
        g.stamp(15, y, [list(TH["table"])])
    for y in (7, 11, 15):
        for x in (7, 11):
            g.set(x, y, TH["col"][0], True)
            g.set(x, y + 1, TH["col"][1], True)
    for x in (1, 17):
        g.set(x, 3, TH["torch"][0], True)
        g.set(x, 4, TH["torch"][1], True)
    g.set(3, 18, TH["basket"], True)
    g.set(15, 18, TH["oil"], True)
    for y in range(6, H - 1):
        if g.mt[y, 9] in (TH["slab"], TH["vein_a"], TH["vein_b"]):
            g.set(9, y, TH["worn"], False)
    g.person("HYPATIA", "AUGUR", 10, 3, "Hypatia", facing="DOWN")
    g.warp(9, H - 1, "Olympus_SeatOfPoseidon", 0)
    g.trigger(9, 2, "ExitGate")
    g.save([TH["void"] | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("hypatia", (10, 5)), ("gate", (9, 3))])
    return g, [("hall", 9, 13), ("rostrum", 9, 5)]


# ---------------------------------------------------------------------------
# The seat of Hera: the throne behind the serpent pits (gTileset_TempleDemeter)
# ---------------------------------------------------------------------------
DEM = None


def dem(key, name):
    s = DEM[key]
    if name is None:
        return s["ids"]
    cx, cy = s["names"][name]
    return s["ids"][cy][cx]


HERA_DOOR = (14, 2)


def seat_of_hera():
    global DEM
    DEM = L.catalog("temple_demeter")
    W, H = 19, 22
    g = Grid("Olympus_SeatOfHera", W, H, primary="gTileset_Oikos", secondary="gTileset_TempleDemeter", cat=None)
    for y in range(H):
        for x in range(W):
            n = noise(x, y, 4)
            g.set(x, y, dem("floor", "floor_b" if n < 18 else "floor_c" if n < 26 else
                            "floor_cracked" if n < 29 else "floor"), False, "floor")
    for x in range(W):
        g.set(x, 0, dem("wall", "corner_l" if x == 0 else "corner_r" if x == W - 1 else "top"), True)
        if 0 < x < W - 1:
            g.set(x, 1, dem("frieze", "key"), True)
            g.set(x, 2, dem("wall_lights", "sconce_lit") if x % 4 == 2 else dem("wall", "lower"), True)
    for y in range(1, H - 1):
        g.set(0, y, dem("wall", "side_l"), True)
        g.set(W - 1, y, dem("wall", "side_r"), True)
    g.set(HERA_DOOR[0], 1, dem("wall_lights", "door_top_painted"), True)
    g.set(HERA_DOOR[0], 2, dem("wall_lights", "door_bottom_painted"), True, "door")
    for x in range(W):
        g.set(x, H - 1, dem("floor", "void"), True)
    for i, x in enumerate((8, 9, 10)):
        g.set(x, H - 1, dem("stairs", ("up_L", "up_M", "up_R")[i]), False, "stairs")
    # the dais and the throne
    d = DEM["dais"]
    for x in range(6, 13):
        g.set(x, 3, dem("dais", "L" if x == 6 else "R" if x == 12 else "M"), False, "dais")
        g.set(x, 4, dem("dais", "steps") if x == 9 else
              dem("dais", "riser_L" if x == 6 else "riser_R" if x == 12 else "riser_M"), x != 9, "dais")
    th = dem("throne", None)
    g.set(9, 2, th[0][0], True, "throne")
    g.set(9, 3, th[1][0], True, "throne")
    for x in (5, 13):
        g.set(x, 3, dem("braziers", "top_lit"), True)
        g.set(x, 4, dem("braziers", "summer_lit"), True)
    # a forest of dark columns, torches on the aisle
    for y in (6, 10, 14):
        for x in (2, 5, 13, 16):
            lit = x in (5, 13)
            g.set(x, y, dem("columns", "torch_lit" if lit else "top"), True)
            g.set(x, y + 1, dem("columns", "bottom_lit" if lit else ("bottom_b" if y == 10 else "bottom")), True)
    # the serpent pits between them
    for (x0, y0, w, h) in ((3, 8, 2, 1), (14, 8, 2, 1), (7, 9, 1, 2), (11, 9, 1, 2),
                           (3, 12, 2, 1), (14, 12, 2, 1), (6, 13, 2, 2), (11, 13, 2, 2),
                           (2, 17, 3, 1), (14, 17, 3, 1)):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                g.set(x, y, dem("floor", "void"), True, "pit")
    for x in (8, 10):
        g.set(x, 18, dem("sentinel", None)[0][0], True)
        g.set(x, 19, dem("sentinel", None)[1][0], True)
    g.set(1, 19, dem("vessels", "lamp_lit"), True)
    g.set(17, 19, dem("vessels", "lamp_lit"), True)
    g.set(16, 3, dem("vessels", "kernos"), True)
    g.set(2, 3, dem("vessels", "kylikes"), True)
    g.person("OLYMPIAS", "PRIESTESS", 9, 5, "Olympias", facing="DOWN")
    g.warp(9, H - 1, "Olympus_SeatOfAthena", 0)
    g.warp(*HERA_DOOR, "Olympus_Summit", 0)
    g.save([dem("floor", "void") | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("olympias", (9, 5)), ("door front", (14, 3))])
    return g, [("hall", 9, 12), ("throne", 9, 5)]


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


BUILDERS = {"Propylaia": propylaia, "Ares": seat_of_ares, "Poseidon": seat_of_poseidon,
            "Athena": seat_of_athena, "Hera": seat_of_hera, "Summit": summit, "Hall": hall_of_heroes}


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
