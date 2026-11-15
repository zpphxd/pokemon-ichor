#!/usr/bin/env python3
"""The Temple of Artemis at Arkadia: the goddess's night garden and the Hunt for the Hind
(design/phase3/SCRIPT.md beat 44 and Part 5), drawn with gTileset_TempleArtemis
(design/phase3/TILES_temple_artemis.md).

PLAN below is the design, one character per cell; this script turns it into
LAYOUT_ARKADIA_TEMPLE_OF_ARTEMIS.

1. Auto-tiles the plan (hedges, moonlight and gravel walks by blob shape key, the lawn's
   variants, the shade under every hedge face, the rock from its cell types) and writes
   data/layouts/Arkadia_TempleOfArtemis/map.bin and border.bin, the events in
   data/maps/Arkadia_TempleOfArtemis/map.json, and the generated part of its scripts.pory
   (between two markers): the garden's drawing from the hunt's state, the walk back to
   the current stage's arch, the hunt var's bands, and the hind's runs.
2. Checks the map: people and hounds on walkable tiles, every patrol on open ground, warps
   on the mat, bg events on tiles someone can face; the stages shut in turn (the rock only
   up its stair, the shortcut only through Anthia's gate); the acolytes' sight across the
   only way; no hound's sight ever on an acolyte's line or on an arch the player is walked
   back to; and the hunt itself: a simulator walks each leg against the hounds' patrols,
   frame by frame, and fails if a leg can be walked with no timing at all (the hounds
   wouldn't matter) or can't be walked at all.
3. Renders, in design/phase3/img/ (from the compiled tileset, as the game draws it):
   Arkadia_TempleOfArtemis.png            the layout at 2x, as a player first finds it
   temple_artemis_map_solved.png          after the hunt: the stair's hedge down, the gate open
   temple_artemis_map_events.png          2x plan: people, hounds, patrols and sight, warps
   With --review NAME, sheets drawn straight from the art (no compile needed):
   temple_artemis_NAME_room.png    the garden at 1x, before and after
   temple_artemis_NAME_views.png   GBA-screen views (15 x 10 tiles) along the route, 2x

Usage: /usr/bin/python3 tools/ichor/maps/temple_artemis.py [--check] [--review NAME]
"""
import argparse
import json
import re
import sys
from collections import deque
from math import gcd
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map  # noqa: E402
from eleusa_lib import blob_key  # noqa: E402

LAYOUT_ID = "LAYOUT_ARKADIA_TEMPLE_OF_ARTEMIS"
LAYOUT_DIR = ROOT / "data/layouts/Arkadia_TempleOfArtemis"
MAP_DIR = ROOT / "data/maps/Arkadia_TempleOfArtemis"
CATALOG = ROOT / "build/temple_artemis/catalog.json"
IMG = ROOT / "design/phase3/img"
PREFIX = "Arkadia_TempleOfArtemis_EventScript_"
MPREFIX = "Arkadia_TempleOfArtemis_Movement_"

# --- The design ---------------------------------------------------------------------------
#   #  clipped laurel hedge          .  night lawn             ,  lawn with asphodel
#   :  moonlight                     =  gravel walk            _  the porch's paving
#   o  myrtle                        O  the great myrtle (2x2) t  an old laurel stump
#   i  a stele (its top over the cell above)                  c  a cypress (two cells)
#   C  a tall cypress (three cells)  R  the rock (ROCK below)  M  the doormat
#   A  a hunters' arch (ARCHES)      h  the hedge across the stair
#   G  Anthia's gate (top, face)     P  a multi-cell piece (PIECES)
#   w  a water bowl   e  a leash post   l  a lampstand (its flame over the cell above)
PLAN = """
##############################
##############################
#########RRRRRRRRRRRR#########
#########RRRRRRRRRRRR#########
#########RRRRRRRRRRRR#########
#########RRRRRRRRRRRR#########
#########RRRRRRRRRRRR#########
##.......RRRRRRRRRRRR.......##
##...........Rhh......::::..##
##.,...o.............::::::.##
##......o........i..o::::::.##
##.....o.............::::::.##
##........oOOcccoOOo.::::::.##
##..,.....oOOooooOOo..::::..##
##........oooooooooo....o...##
##..o.....oooOOooooo........##
##........oooOOooooo...,....##
##.c.......,.,......o.......##
##..o.............o.......c.##
##......o........c.......o..##
##.C.AAAA............C......##
#####AAAA#####################
#####AAAA#####################
##...::::::.#####.,..o......##
##.#::::::::#####.::::::::..##
##.#::::::::#####.::::::::.i##
##.#.::::::...oooo::::::::..##
##G#####..........::::::::..##
##G#####.o.....ooo::::::::..##
##.....#o....i.ooo::::::::..##
##.............o.o...o......##
##.....#o........o..........##
##..PP.#.........o..........##
##,....#.........o..........##
#####################AAAA#####
#####################AAAA#####
##,...................==.,..##
##.....i......=========...i.##
##..,.........=OO...o.......##
##.............OO...........##
##oocooooooooo.oooocoooocooo##
##,.......,........,......,.##
##....i................i....##
#############AAAA#############
#############AAAA#############
##__PPP_PP__________PP_PP___##
##__PPP_PPw________wPP_PP___##
##__________l____l____ePP___##
##__________________________##
##############MM##############
"""
W, H = 30, 50

# The rock: cell codes for the rows it fills (x 9..20, y 2..7), by type in
# temple_artemis_art.ROCK_KEYS: fl flat, fb flat_b, fs flat_shade, se seat, li lip,
# st stair_top, cl cliff, cb cliff_b, sr stair, fo foot, sf stair_foot, ru rubble,
# bo boulder, la landing; pl/pr the moon pool. (13,8) is a boulder below the rock.
ROCK_ORIGIN = (9, 2)
ROCK = """
fs fs fs fs fs fs fs fs fs fs fs fs
fl fb pl pr fb fl se fb fl fb fl fb
li li li li li st st li li li li li
cl cb cl cb cl sr sr cl cb cl cb cl
fo fo fo fo fo sr sr fo fo fo fo fo
ru bo ru ru la sf sf ru bo ru ru bo
"""
ROCK_CODE = {"fl": "flat", "fb": "flat_b", "fs": "flat_shade", "se": "seat", "li": "lip",
             "st": "stair_top", "cl": "cliff", "cb": "cliff_b", "sr": "stair", "fo": "foot",
             "sf": "stair_foot", "ru": "rubble", "bo": "boulder", "la": "landing"}
EXTRA_ROCK = {(13, 8): "boulder"}

# Arches: (left post x, wall top row y) -> variant; each is 4 x 3 from (x, y - 1).
ARCHES = {(13, 43): "antlers", (21, 34): "bow", (5, 21): "moon"}
STAIR_HEDGE = {(14, 8): "l", (15, 8): "r"}
GATE_TOP, GATE = (2, 27), (2, 28)       # Anthia's gate: its top and face cells

# Multi-cell pieces by top-left: (structure, rows of piece names).
PIECES = {
    (4, 45): ("altar", [["altar_tl", "altar_tm", "altar_tr"], ["altar_bl", "altar_bm", "altar_br"]]),
    (23, 45): ("statue", [["tl", "tr"], ["ml", "mr"], ["bl", "br"]]),
    (8, 45): ("kennel", [["kennel_tl", "kennel_tr"], ["kennel_bl", "kennel_br"]]),
    (20, 45): ("kennel", [["kennel_tl", "kennel_tr"], ["kennel_bl", "kennel_br"]]),
    (4, 32): ("kennel", [["bench_l", "bench_r"]]),
}

# --- The hunt -------------------------------------------------------------------------------
# VAR_ICHOR_HUNT: the tens are the hunt's stage, the units the times a hound has walked
# the player back in that stage (0-3, for Phylonoe's hint). 0: not yet welcomed; 10 Stage I;
# 20 Stage II; 30 Stage III, the hind at A; 40 the hind at B (one touch); 50 at C (two);
# 60 the third touch (FLAG_ICHOR_HUNT_DONE, the stair's hedge down); 70 the Moon Laurel.
BANDS = [10, 20, 30, 40, 50, 60]
# Where a hound walks the player back to, by band: the arch's lintel, facing in.
ARCH_RETURN = {10: (14, 43), 20: (22, 34), 30: (6, 21), 40: (6, 21), 50: (6, 21), 60: (6, 21)}
DOOR = [(14, 49), (15, 49)]
HIND = {"A": (12, 17), "B": (4, 11), "C": (23, 12)}

# The hounds: (local id, stage, x, y, movement type, range, sight). Moonlit hounds see 6.
HOUNDS = [
    ("LOCALID_ARTEMIS_HOUND_1", 1, 13, 39, "WALK_LEFT_AND_RIGHT", 5, 3),
    ("LOCALID_ARTEMIS_HOUND_2", 2, 21, 27, "ROTATE_CLOCKWISE", 0, 6),
    ("LOCALID_ARTEMIS_HOUND_3", 2, 12, 30, "WALK_SEQUENCE_UP_RIGHT_DOWN_LEFT", 2, 3),
    ("LOCALID_ARTEMIS_HOUND_4", 2, 10, 25, "WALK_LEFT_AND_RIGHT", 5, 6),
    ("LOCALID_ARTEMIS_HOUND_5", 3, 9, 14, "WALK_LEFT_AND_RIGHT", 5, 3),
    ("LOCALID_ARTEMIS_HOUND_6", 3, 16, 11, "WALK_SEQUENCE_UP_RIGHT_DOWN_LEFT", 2, 3),
    ("LOCALID_ARTEMIS_HOUND_7", 3, 24, 11, "ROTATE_CLOCKWISE", 0, 6),
]
SLEEP_ID = "LOCALID_ARTEMIS_SLEEPER_{}"
# People: (local id, graphics, x, y, facing, trainer sight or None, script, hide flag)
PEOPLE = [
    ("LOCALID_ARTEMIS_PHYLONOE", "OBJ_EVENT_GFX_ICHOR_PHYLONOE", 16, 46, "DOWN", None, "Phylonoe", "0"),
    ("LOCALID_ARTEMIS_KYRENE", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 20, 36, "RIGHT", 3, "Kyrene", "0"),
    ("LOCALID_ARTEMIS_ANTHIA", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 2, 31, "LEFT", 1, "Anthia", "0"),
    ("LOCALID_ARTEMIS_PROKRIS", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 13, 7, "RIGHT", 3, "Prokris", "0"),
    ("LOCALID_ARTEMIS_KALLISTO", "OBJ_EVENT_GFX_ICHOR_KALLISTO", 15, 3, "DOWN", None, "Kallisto", "0"),
    ("LOCALID_ARTEMIS_HIND", "OBJ_EVENT_GFX_ICHOR_GOLDEN_HIND", HIND["A"][0], HIND["A"][1], "LEFT",
     None, "Hind", "0"),
    ("LOCALID_ARTEMIS_FEATHER", "OBJ_EVENT_GFX_ITEM_BALL", 6, 32, "DOWN", None, "ItemPrettyFeather",
     "FLAG_ICHOR_ITEM_TEMPLE_ARTEMIS_PRETTY_FEATHER"),
]
ACOLYTES = {"Kyrene", "Anthia", "Prokris"}
TRIGGERS = {
    "Welcome": ([(14, 48), (15, 48)], "VAR_ICHOR_HUNT", "0"),
    # (not VAR_TEMP_2 and _3 together: main's carried-flame code reads that pair as a torch)
    "ArchII": ([(22, 33), (23, 33)], "VAR_TEMP_5", "0"),
    "ArchIII": ([(6, 20), (7, 20)], "VAR_TEMP_6", "0"),
    "Rock": ([(14, 4), (15, 4)], "VAR_TEMP_4", "0"),
}
HIDDEN = {
    (2, 41): ("FLAG_ICHOR_HIDDEN_TEMPLE_ARTEMIS_STARDUST", "ITEM_STARDUST"),
    (27, 23): ("FLAG_ICHOR_HIDDEN_TEMPLE_ARTEMIS_DUSK_BALL", "ITEM_DUSK_BALL"),
    (20, 3): ("FLAG_ICHOR_HIDDEN_TEMPLE_ARTEMIS_STAR_PIECE", "ITEM_STAR_PIECE"),
}
# Signs: (x, y, script, facing): the stelae, each with a myth of the place
SIGNS = [
    (6, 42, "SteleHound", "ANY"), (23, 42, "SteleBears", "ANY"),
    (7, 37, "SteleAktaion", "ANY"), (26, 37, "SteleAtalanta", "ANY"),
    (27, 25, "SteleKeryneia", "ANY"), (13, 29, "SteleWorn", "ANY"),
    (17, 10, "SteleOrion", "ANY"),
]
ELEVATION = 3
LEGS = [
    # (name, stage, start ("prev": where the last leg ended), goal tiles, the hind's place,
    #  gate open, may it need no timing)
    ("Stage I: the arch to Kyrene", 1, (14, 43), [(21, 36), (22, 36), (23, 36)], "A", False, False),
    ("Stage II: the arch to the next", 2, (22, 34), [(6, 23), (7, 23)], "A", False, False),
    ("Stage II: by Anthia's gate", 2, (3, 31), [(6, 23), (7, 23)], "A", True, True),
    ("Stage III: to the hind at A", 3, (6, 21), "hind", "A", False, True),
    ("Stage III: after her to B", 3, "prev", "hind", "B", False, False),
    ("Stage III: after her to C", 3, "prev", "hind", "C", False, False),
    ("Stage III: from C to the stair", 3, "prev", [(14, 9), (15, 9)], "C", False, False),
]


def h32(*v):
    x = 2166136261
    for n in v:
        x = ((x ^ (int(n) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    x ^= x >> 13
    return x


# --- The catalog ----------------------------------------------------------------------------

def load_catalog():
    if not CATALOG.exists():
        sys.exit("temple_artemis: run tools/ichor/art/temple_artemis_build.py first")
    return {s["key"]: s for s in json.loads(CATALOG.read_text())["structures"]}


class Pieces:
    """(structure, piece) <-> metatile id, and walk codes, from the tileset's catalog."""

    def __init__(self, cat):
        self.cat = cat
        self.id, self.walk = {}, {}
        for key, s in cat.items():
            for name, (cx, cy) in s["names"].items():
                mid = s["ids"][cy][cx]
                self.id[(key, name)] = mid
                self.walk[mid] = s["walk"][cy][cx]
            for cy in range(s["h"]):
                for cx in range(s["w"]):
                    self.walk.setdefault(s["ids"][cy][cx], s["walk"][cy][cx])
        self.name = {v: k for k, v in self.id.items()}

    def __call__(self, key, name):
        return self.id[(key, name)]

    def passable(self, mid):
        return self.walk[mid] in ".ST"


def plan_rows():
    rows = PLAN.strip("\n").split("\n")
    if len(rows) != H:
        raise ValueError(f"PLAN is {len(rows)} rows, expected {H}")
    for n, r in enumerate(rows):
        if len(r) != W:
            raise ValueError(f"PLAN row {n} is {len(r)} wide, expected {W}: {r!r}")
    return rows


def arch_cells():
    """{(x, y): (variant, piece name)} for every arch's 4 x 3 block."""
    out = {}
    for (x0, y0), v in ARCHES.items():
        names = [["crown_l", "crown_ml", "crown_mr", "crown_r"],
                 ["cap_l", "lintel_l", "lintel_r", "cap_r"],
                 ["post_l", "open_l", "open_r", "post_r"]]
        for j in range(3):
            for i in range(4):
                out[(x0 + i, y0 - 1 + j)] = (f"arch_{v}", names[j][i])
    return out


def piece_cells():
    out = {}
    for (x0, y0), (key, rows) in PIECES.items():
        for j, row in enumerate(rows):
            for i, nm in enumerate(row):
                out[(x0 + i, y0 + j)] = (key, nm)
    return out


def rock_cells():
    out = {}
    rows = [r.split() for r in ROCK.strip().splitlines()]
    ox, oy = ROCK_ORIGIN
    for j, row in enumerate(rows):
        for i, code in enumerate(row):
            if code in ("pl", "pr"):
                out[(ox + i, oy + j)] = ("pool", "pool_l" if code == "pl" else "pool_r")
            else:
                out[(ox + i, oy + j)] = ("rock", ROCK_CODE[code])
    for xy, nm in EXTRA_ROCK.items():
        out[xy] = ("rock", nm)
    return out


def hedge_mask(rows):
    """Hedge mass: hedge cells, arch posts and Anthia's gate (both flush with the hedge)."""
    m = [[rows[y][x] == "#" for x in range(W)] for y in range(H)]
    for (x, y), (_, nm) in arch_cells().items():
        if nm.startswith(("post", "cap")):
            m[y][x] = True
    for (x, y) in (GATE_TOP, GATE):
        m[y][x] = True
    return m


def grid_ids(pieces, rows=None):
    rows = rows or plan_rows()
    hm = hedge_mask(rows)
    moon = [[rows[y][x] == ":" for x in range(W)] for y in range(H)]
    walk = [[rows[y][x] == "=" for x in range(W)] for y in range(H)]
    arches, multi, rock = arch_cells(), piece_cells(), rock_cells()
    g = [[None] * W for _ in range(H)]
    tops = {}          # (x, y) -> (structure, piece) drawn above a tall thing's base

    def is_face(x, y):
        return 0 <= y < H and 0 <= x < W and hm[y][x] and not (y + 1 < H and hm[y + 1][x]) \
            and y + 1 < H

    for y in range(H):
        for x in range(W):
            ch = rows[y][x]
            v = h32(x, y)
            under_face = y > 0 and is_face(x, y - 1)
            if (x, y) in arches:
                key, nm = arches[(x, y)]
                if ch != "A" and not (nm.startswith("crown") and ch == "."):
                    raise ValueError(f"arch cell ({x},{y}) is {ch!r} in PLAN")
                g[y][x] = pieces(key, nm)
                continue
            if (x, y) in rock:
                if ch != "R":
                    raise ValueError(f"rock cell ({x},{y}) is {ch!r} in PLAN")
                g[y][x] = pieces(*rock[(x, y)])
                continue
            if (x, y) in multi:
                if ch != "P":
                    raise ValueError(f"piece cell ({x},{y}) is {ch!r} in PLAN")
                g[y][x] = pieces(*multi[(x, y)])
                continue
            if ch == "#":
                g[y][x] = pieces("hedge", blob_key(hm, x, y))
            elif ch == "G":
                g[y][x] = pieces("gates", "gate_top" if (x, y) == GATE_TOP else "gate")
            elif ch == ":":
                g[y][x] = pieces("moon", blob_key(moon, x, y))
            elif ch == "=":
                g[y][x] = pieces("walk", blob_key(walk, x, y))
            elif ch in ".,":
                if under_face:
                    g[y][x] = pieces("floor", "lawn_shade_b" if v % 2 else "lawn_shade")
                elif ch == ",":
                    g[y][x] = pieces("floor", "lawn_flowers_b" if v % 2 else "lawn_flowers")
                else:
                    g[y][x] = pieces("floor", ["lawn", "lawn_b", "lawn", "lawn_b", "lawn_tuft"][v % 9 % 5]
                                     if v % 9 < 5 else ("lawn" if v % 2 else "lawn_b"))
            elif ch == "_":
                if under_face:
                    g[y][x] = pieces("floor", "pave_shade")
                else:
                    g[y][x] = pieces("floor", ["pave", "pave_b", "pave_c"][v % 3])
            elif ch == "M":
                g[y][x] = pieces("floor", "mat_l" if rows[y][x + 1] == "M" else "mat_r")
            elif ch == "o":
                g[y][x] = pieces("bush", ["myrtle", "myrtle_b", "myrtle_flowers"][v % 3])
            elif ch == "O":
                tl = rows[y - 1][x] != "O" if y else True
                lf = rows[y][x - 1] != "O" if x else True
                # the 2x2 is aligned by its top-left: count O's above and left
                oy = 0 if (y == 0 or rows[y - 1][x] != "O" or (y >= 2 and rows[y - 2][x] == "O")) else 1
                ox = 0 if (x == 0 or rows[y][x - 1] != "O" or (x >= 2 and rows[y][x - 2] == "O")) else 1
                del tl, lf
                g[y][x] = pieces("bush", "big_" + ("t" if oy == 0 else "b") + ("l" if ox == 0 else "r"))
            elif ch == "t":
                g[y][x] = pieces("bush", "stump")
            elif ch == "i":
                kind = ["deer", "bow", "wreath"][(x * 7 + y * 3) % 3]
                g[y][x] = pieces("tall", f"stele_{kind}")
                tops[(x, y - 1)] = ("tall", f"stele_{kind}_top")
            elif ch == "c":
                kind = "cypress" if v % 2 else "cypress_b"
                g[y][x] = pieces("tall", kind)
                tops[(x, y - 1)] = ("tall", f"{kind}_top")
            elif ch == "C":
                g[y][x] = pieces("tallcypress", "base")
                tops[(x, y - 1)] = ("tallcypress", "mid")
                tops[(x, y - 2)] = ("tallcypress", "top")
            elif ch == "l":
                g[y][x] = pieces("tall", "lamp")
                tops[(x, y - 1)] = ("tall", "lamp_top")
            elif ch == "w":
                g[y][x] = pieces("kennel", "bowl")
            elif ch == "e":
                g[y][x] = pieces("kennel", "leash")
            elif ch == "h":
                g[y][x] = pieces("gates", f"hedge_{STAIR_HEDGE[(x, y)]}")
            else:
                raise ValueError(f"unknown PLAN character {ch!r} at ({x},{y})")
    for (x, y), pc in tops.items():
        under = rows[y][x]
        if under not in ".,_" or (x, y) in arches or (x, y) in multi:
            raise ValueError(f"the top of a tall thing at ({x},{y}) falls on {under!r}")
        g[y][x] = pieces(*pc)
    if any(v is None for r in g for v in r):
        raise ValueError("PLAN left cells unset")
    return g


def staged(pieces, g, done=False, gate=False):
    """The garden at a state of the hunt: done = the stair's hedge down; gate = Anthia's
    gate open."""
    out = [row[:] for row in g]
    if done:
        for (x, y), side in STAIR_HEDGE.items():
            out[y][x] = pieces("gates", f"hedge_lowered_{side}")
    if gate:
        out[GATE_TOP[1]][GATE_TOP[0]] = pieces("gates", "gate_top_open")
        out[GATE[1]][GATE[0]] = pieces("gates", "gate_open")
    return out


def layout_blocks(pieces, g):
    out = []
    for row in g:
        for mid in row:
            out.append(mid | ((0 if pieces.passable(mid) else 1) << 10) | (ELEVATION << 12))
    return np.array(out, "<u2")


def border_blocks(pieces):
    full = "1|11111111"
    return np.array([pieces("hedge", full)] * 4, "<u2")


# --- map.json events ----------------------------------------------------------------------

def hound_events():
    out = []
    for n, (lid, stage, x, y, mt, rng, sight) in enumerate(HOUNDS):
        out.append({
            "local_id": lid, "graphics_id": "OBJ_EVENT_GFX_ICHOR_TEMPLE_HOUND", "x": x, "y": y,
            "elevation": ELEVATION, "movement_type": f"MOVEMENT_TYPE_{mt}",
            "movement_range_x": rng, "movement_range_y": rng,
            "trainer_type": "TRAINER_TYPE_NORMAL", "trainer_sight_or_berry_tree_id": str(sight),
            "script": PREFIX + "Hound", "flag": "FLAG_BADGE05_GET"})
    for n, (lid, stage, x, y, mt, rng, sight) in enumerate(HOUNDS):
        sx, sy = sleeper_spot(n)
        out.append({
            "local_id": SLEEP_ID.format(n + 1), "graphics_id": "OBJ_EVENT_GFX_ICHOR_TEMPLE_HOUND",
            "x": sx, "y": sy, "elevation": ELEVATION, "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
            "script": PREFIX + "SleepingHound", "flag": "FLAG_ICHOR_HIDE_TEMPLE_HOUNDS_ASLEEP"})
    return out


def sleeper_spot(n):
    """Where hound n curls up asleep after the laurel: its patrol's home tile."""
    _, _, x, y, mt, rng, _ = HOUNDS[n]
    return x, y


def events():
    obj = []
    for lid, gfx, x, y, facing, sight, script, flag in PEOPLE:
        obj.append({
            "local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": ELEVATION,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0,
            "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight or 0),
            "script": PREFIX + script, "flag": flag})
    obj += hound_events()
    warps = [{"x": x, "y": y, "elevation": 0, "dest_map": "MAP_ARKADIA", "dest_warp_id": "6"}
             for x, y in DOOR]
    coords = []
    for name, (cellsl, var, val) in TRIGGERS.items():
        for x, y in cellsl:
            coords.append({"type": "trigger", "x": x, "y": y, "elevation": ELEVATION,
                           "var": var, "var_value": val, "script": PREFIX + name})
    bgs = []

    def sign(x, y, script, facing="ANY"):
        bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                    "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{facing}",
                    "script": PREFIX + script})
    cat = load_catalog()
    plan = plan_rows()
    for (x0, y0), (key, rows) in PIECES.items():
        script = {"altar": "Altar", "statue": "Statue", "kennel": "Kennel"}[key]
        if rows[0][0].startswith("bench"):
            continue
        for j, row in enumerate(rows):
            for i, nm in enumerate(row):
                cx, cy = cat[key]["names"][nm]
                x, y = x0 + i, y0 + j
                faced = any(plan[y + dy][x + dx] not in "#P" for dx, dy in DIRV.values())
                if cat[key]["walk"][cy][cx] == "X" and faced:
                    sign(x, y, script)
    for x, y in rock_pool():
        sign(x, y, "Pool")
    for (x, y), (flag, item) in HIDDEN.items():
        bgs.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item,
                    "flag": flag, "quantity": 1, "underfoot": False})
    for x, y, script, facing in SIGNS:
        sign(x, y, script, facing)
    return {"object_events": obj, "warp_events": warps, "coord_events": coords, "bg_events": bgs}


def rock_pool():
    return [xy for xy, (k, _) in rock_cells().items() if k == "pool"]


def write_map_json(ev):
    p = MAP_DIR / "map.json"
    d = json.loads(p.read_text())
    d["music"] = "MUS_ICHOR_TEMPLE"   # ICHOR_STUB_MUSIC: MUS_ICHOR_HUNT (SCRIPT.md Part 9, cue 20)
    d.update(ev)
    p.write_text(json.dumps(d, indent=2) + "\n")


# --- The hounds' patrols, frame by frame ---------------------------------------------------
# Measured against the engine (src/event_object_movement.c): a walker steps a tile every 16
# frames and turns at once at a patrol's end; WALK_*_AND_* runs from its home tile to
# home - range and back (WalkBackAndForth flips again on reaching home); a WALK_SEQUENCE
# loop runs range up, range right, range down, range left; ROTATE_CLOCKWISE holds each
# facing TURN frames, south, west, north, east.
STEP = 16
TURN = 49
DIRV = {"S": (0, 1), "N": (0, -1), "W": (-1, 0), "E": (1, 0)}


def patrol(n):
    """Hound n's patrol as (period, state(t) -> ((x, y) now, (x, y) from, facing))."""
    _, _, x0, y0, mt, r, _ = HOUNDS[n]
    if mt == "ROTATE_CLOCKWISE":
        order = "SWNE"

        def state(t):
            return (x0, y0), (x0, y0), order[(t // TURN) % 4]
        return 4 * TURN, state
    if mt.startswith("WALK_SEQUENCE"):
        seq = "N" * r + "E" * r + "S" * r + "W" * r
    else:
        d0 = {"WALK_LEFT_AND_RIGHT": "W", "WALK_RIGHT_AND_LEFT": "E", "WALK_UP_AND_DOWN": "N",
              "WALK_DOWN_AND_UP": "S"}[mt]
        back = {"W": "E", "E": "W", "N": "S", "S": "N"}[d0]
        seq = d0 * r + back * r
    pts = [(x0, y0)]
    for d in seq:
        dx, dy = DIRV[d]
        pts.append((pts[-1][0] + dx, pts[-1][1] + dy))

    def state(t):
        k = (t // STEP) % len(seq)
        return pts[k + 1], pts[k], seq[k]
    return STEP * len(seq), state


def lcm(a, b):
    return a * b // gcd(a, b)


class Hunt:
    """The garden as the hounds see it, for one leg: static walls, fixed people, the hind."""

    def __init__(self, pieces, g, stage, hind, people_xy):
        self.pieces, self.g, self.stage = pieces, g, stage
        self.idx = [n for n, h in enumerate(HOUNDS) if h[1] == stage]
        self.pat = {n: patrol(n) for n in self.idx}
        self.period = 1
        for n in self.idx:
            self.period = lcm(self.period, self.pat[n][0])
        self.fixed = set(people_xy) | {hind}
        self._seen = {}

    def open(self, x, y):
        return 0 <= x < W and 0 <= y < H and self.pieces.passable(self.g[y][x])

    def hounds_at(self, t):
        out = []
        for n in self.idx:
            now, frm, f = self.pat[n][1](t)
            out.append((n, now, frm, f))
        return out

    def seen(self, t):
        """Tiles some hound sees at frame t (from its tile, and from the tile it is leaving)."""
        t %= self.period
        if t in self._seen:
            return self._seen[t]
        hs = self.hounds_at(t)
        bodies = {now for _, now, _, _ in hs} | {frm for _, _, frm, _ in hs} | self.fixed
        out = set()
        for n, now, frm, f in hs:
            sight = HOUNDS[n][6]
            dx, dy = DIRV[f]
            for sx, sy in {now, frm}:
                for k in range(1, sight + 1):
                    x, y = sx + dx * k, sy + dy * k
                    out.add((x, y))
                    if not self.open(x, y) or ((x, y) in bodies and (x, y) not in (now, frm)):
                        break
        self._seen[t] = out
        return out

    def bodies(self, t):
        hs = self.hounds_at(t % self.period)
        return {now for _, now, _, _ in hs} | {frm for _, _, frm, _ in hs} | self.fixed

    def ever_seen(self):
        out = set()
        for t in range(0, self.period, 2):
            out |= self.seen(t)
        return out

    def ever_walked(self):
        out = set()
        for t in range(0, self.period, STEP):
            for _, now, frm, _ in self.hounds_at(t):
                out |= {now, frm}
        return out

    def safe(self, xy, t0, t1, margin=3):
        for t in range(t0 - margin, t1 + margin + 1):
            if xy in self.seen(t):
                return False
        return True

    def static_path(self, start, goals):
        """A path that needs no timing: never on a tile any hound could see or walk."""
        bad = self.ever_seen() | self.ever_walked() | self.fixed
        seen, todo = {start}, deque([start])
        while todo:
            p = todo.popleft()
            if p in goals:
                return True
            for dx, dy in DIRV.values():
                q = (p[0] + dx, p[1] + dy)
                if q not in seen and self.open(*q) and q not in bad:
                    seen.add(q)
                    todo.append(q)
        return False

    def timed_path(self, start, goals, horizon=6000):
        """Breadth-first over (tile, frame): the player steps a tile every 16 frames or waits
        16, and must never stand where a hound sees them. Returns the walk, or None."""
        if not self.safe(start, 0, 0):
            return None
        prev = {(start, 0): None}
        todo = deque([(start, 0)])
        while todo:
            p, t = todo.popleft()
            if p in goals:
                path = []
                k = (p, t)
                while k:
                    path.append(k)
                    k = prev[k]
                return path[::-1]
            if t + STEP > horizon:
                continue
            nt = t + STEP
            cands = [p] + [(p[0] + dx, p[1] + dy) for dx, dy in DIRV.values()]
            for q in cands:
                if q != p and (not self.open(*q) or q in self.bodies(nt) or q in self.bodies(t)):
                    continue
                # the engine polls sight every frame the player has control, mid-step too,
                # against the tile the player is stepping into: q is exposed from the step's start
                ok = self.safe(q, t, nt)
                if not ok:
                    continue
                key = (q, nt % self.period if q == p and False else nt)
                if key in prev:
                    continue
                prev[key] = (p, t)
                todo.append(key)
        return None


def leg_goals(leg):
    name, stage, start, goals, hind, gate, easy = leg
    if goals == "hind":
        hx, hy = HIND[hind]
        goals = [(hx + dx, hy + dy) for dx, dy in DIRV.values()]
    return set(goals)


def simulate(pieces, g, verbose=True):
    """Walk every leg of the hunt against the hounds. Returns (per-leg results, errors);
    each result is (name, trivial, path) with path a list of ((x, y), frame)."""
    people = [(x, y) for lid, gfx, x, y, *_ in PEOPLE if lid not in ("LOCALID_ARTEMIS_HIND",)]
    results, errors = [], []
    last = None
    for leg in LEGS:
        name, stage, start, _, hind, gate, easy = leg
        if start == "prev":
            if last is None:
                errors.append(f"{name}: the leg before it failed")
                results.append((name, False, None))
                continue
            start = last
        grid = staged(pieces, g, gate=gate)
        hunt = Hunt(pieces, grid, stage, HIND[hind], people)
        goals = {q for q in leg_goals(leg) if hunt.open(*q)}
        trivial = hunt.static_path(start, goals)
        path = hunt.timed_path(start, goals)
        results.append((name, trivial, path))
        if path is None:
            last = None
            errors.append(f"{name}: the hounds can't be passed from {start}")
        else:
            last = path[-1][0]
        if verbose:
            steps = None if path is None else sum(1 for a, b in zip(path, path[1:]) if a[0] != b[0])
            waits = None if path is None else sum(1 for a, b in zip(path, path[1:]) if a[0] == b[0])
            print(f"  {name}: " + ("NO PATH" if path is None else f"{steps} steps, {waits} waits")
                  + ("; no timing needed" if trivial else ""))
        if trivial and not easy:
            errors.append(f"{name}: a path past every hound needs no timing")
    return results, errors


# --- Renders ------------------------------------------------------------------------------

def compiled_renderer(layout):
    render_map.read_fieldmap_constants()
    symbols = render_map.scan_tileset_symbols()
    prim = render_map.resolve_tileset(layout["primary_tileset"], symbols)
    sec = render_map.resolve_tileset(layout["secondary_tileset"], symbols)
    return render_map.Renderer(render_map.Tileset(prim), render_map.Tileset(sec))


class SourceRenderer:
    """Draws metatiles straight from the art's layers (no Porytiles compile)."""

    def __init__(self, pieces):
        import eleusa_lib as E
        import temple_artemis_art as T
        self.tiles = {}
        for s in T.build():
            img = E.composite(s)
            d = pieces.cat[s.key]
            for cy in range(s.h):
                for cx in range(s.w):
                    self.tiles[d["ids"][cy][cx]] = img[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        self.void = self.tiles[pieces("hedge", "1|11111111")]

    def render(self, g, margin=0):
        h, w = len(g), len(g[0])
        img = np.empty(((h + 2 * margin) * 16, (w + 2 * margin) * 16, 3), np.uint8)
        for y in range(h + 2 * margin):
            for x in range(w + 2 * margin):
                gx, gy = x - margin, y - margin
                inside = 0 <= gx < w and 0 <= gy < h
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = self.tiles[g[gy][gx]] if inside else self.void
        return Image.fromarray(img)


def scaled(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


def font(size):
    return ImageFont.load_default(size=size)


def labelled(img, text, pad=22):
    out = Image.new("RGB", (img.width, img.height + pad), (40, 40, 48))
    out.paste(img, (0, pad))
    ImageDraw.Draw(out).text((6, 4), text, fill=(230, 230, 200), font=font(14))
    return out


def sheet(images, cols, gap=10, bg=(40, 40, 48)):
    w = max(i.width for i in images)
    h = max(i.height for i in images)
    rows = (len(images) + cols - 1) // cols
    out = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * h + (rows + 1) * gap), bg)
    for n, im in enumerate(images):
        r, c = divmod(n, cols)
        out.paste(im, (gap + c * (w + gap), gap + r * (h + gap)))
    return out


def screen_view(img, margin, cx, cy):
    """The 240 x 160 GBA screen with the camera on tile (cx, cy)."""
    x0 = (cx + margin - 7) * 16
    y0 = (cy + margin) * 16 - 72
    return img.crop((x0, y0, x0 + 240, y0 + 160))


VIEWS = [
    ("the door: Phylonoe, the altar, the kennels", 14, 47), ("the first arch", 14, 42),
    ("Stage I: the glade and the bush", 12, 39), ("Kyrene and the second arch", 20, 37),
    ("Stage II: the first moonlit clearing", 20, 29), ("Stage II: the stele and its hound", 12, 29),
    ("Anthia's grove and her gate", 5, 30), ("Stage II: the second clearing", 8, 24),
    ("the third arch, clearing A", 8, 19), ("Stage III: the west, clearing B", 5, 12),
    ("Stage III: clearing C", 22, 12), ("the stair and the hedge", 14, 9),
    ("the moonlit rock", 14, 4),
]

FACE = {"S": "DOWN", "N": "UP", "W": "LEFT", "E": "RIGHT"}


def objects_overlay(img, ev, pieces, g, s=2, t=0):
    """People and hounds (at frame t of their patrols), their sight and patrols."""
    img = img.convert("RGBA")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    c = 16 * s

    def box(x, y, fill, outline, w=2):
        d.rectangle([x * c + 1, y * c + 1, x * c + c - 2, y * c + c - 2], fill=fill, outline=outline, width=w)

    for b in ev["bg_events"]:
        box(b["x"], b["y"], (80, 160, 255, 50), (80, 160, 255, 200))
    for tr in ev["coord_events"]:
        box(tr["x"], tr["y"], (255, 220, 0, 60), (255, 220, 0, 220))
    for w in ev["warp_events"]:
        d.rectangle([w["x"] * c + 6, w["y"] * c + 6, w["x"] * c + c - 7, w["y"] * c + c - 7],
                    outline=(255, 60, 200, 255), width=2)
    for n, h in enumerate(HOUNDS):
        _, state = patrol(n)
        period = patrol(n)[0]
        walked = {state(tt)[0] for tt in range(0, period, STEP)} | {(h[2], h[3])}
        for (x, y) in walked:
            d.rectangle([x * c + 5, y * c + 5, x * c + c - 6, y * c + c - 6], outline=(255, 150, 40, 255), width=1)
    people = [(x, y) for _, _, x, y, *_ in PEOPLE]
    for lid, gfx, x, y, facing, sight, script, flag in PEOPLE:
        if sight:
            dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[facing]
            for k in range(1, sight + 1):
                xx, yy = x + dx * k, y + dy * k
                if not (0 <= xx < W and 0 <= yy < H and pieces.passable(g[yy][xx])):
                    break
                box(xx, yy, (255, 60, 40, 60), (255, 60, 40, 255))
        box(x, y, (40, 220, 90, 110), (20, 120, 40, 255))
        d.text((x * c + c // 2, y * c - 2), script, fill=(255, 255, 255, 255), font=font(11),
               anchor="md", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for stage in (1, 2, 3):
        hunt = Hunt(pieces, g, stage, HIND["A"], people)
        for (x, y) in hunt.ever_seen():
            if 0 <= x < W and 0 <= y < H and hunt.open(x, y):
                d.rectangle([x * c + 10, y * c + 10, x * c + c - 11, y * c + c - 11], fill=(255, 40, 40, 160))
    for n, h in enumerate(HOUNDS):
        x, y = h[2], h[3]
        box(x, y, (240, 240, 255, 140), (40, 40, 60, 255))
        d.text((x * c + c // 2, y * c - 2), f"H{n + 1}", fill=(255, 255, 255, 255), font=font(11),
               anchor="md", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for k, (x, y) in HIND.items():
        d.ellipse([x * c + 6, y * c + 6, x * c + c - 7, y * c + c - 7], outline=(255, 210, 60, 255), width=3)
        d.text((x * c + c // 2, y * c - 2), k, fill=(255, 210, 60, 255), font=font(12),
               anchor="md", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    img = Image.alpha_composite(img, over)
    key = [((40, 220, 90), "person"), ((255, 60, 40), "an acolyte's sight"),
           ((240, 240, 255), "hound (H1-H7), patrol outlined orange; red dots: tiles a hound ever sees"),
           ((255, 210, 60), "the golden hind's clearings A, B, C"), ((80, 160, 255), "bg event"),
           ((255, 220, 0), "coord event"), ((255, 60, 200), "warp to Arkadia")]
    pad = 18
    out = Image.new("RGBA", (img.width, img.height + pad * len(key) + 8), (40, 40, 48, 255))
    out.paste(img, (0, 0))
    d = ImageDraw.Draw(out)
    for i, (col, text) in enumerate(key):
        y = img.height + 6 + i * pad
        d.rectangle([8, y, 20, y + 12], fill=col)
        d.text((28, y), text, fill=(230, 230, 200), font=font(11))
    return out.convert("RGB")


def review(name, pieces, g):
    r = SourceRenderer(pieces)
    first = r.render(g)
    solved = r.render(staged(pieces, g, done=True, gate=True))
    sheet([labelled(first, "as you first find it"), labelled(solved, "the hunt done, the gate open")],
          2).save(IMG / f"temple_artemis_{name}_room.png")
    margin = 8
    big = r.render(g, margin)
    views = [labelled(scaled(screen_view(big, margin, x, y), 2), f"{t} ({x},{y})") for t, x, y in VIEWS]
    sheet(views, 3).save(IMG / f"temple_artemis_{name}_views.png")
    objects_overlay(scaled(first, 2), events(), pieces, g).save(IMG / f"temple_artemis_{name}_events.png")
    return [IMG / f"temple_artemis_{name}_{k}.png" for k in ("room", "views", "events")]


# --- The generated scripts ----------------------------------------------------------------

SCRIPT_BEGIN = ("// --- Garden scripts: generated by tools/ichor/maps/temple_artemis.py from the "
                "plan. Do not edit. ---")
SCRIPT_END = "// --- End of generated garden scripts. ---"
LABEL = {("gates", "hedge_l"): "StairHedge_L", ("gates", "hedge_r"): "StairHedge_R",
         ("gates", "hedge_lowered_l"): "StairHedge_Lowered_L",
         ("gates", "hedge_lowered_r"): "StairHedge_Lowered_R",
         ("gates", "gate_top"): "GateTop", ("gates", "gate_top_open"): "GateTop_Open",
         ("gates", "gate"): "Gate", ("gates", "gate_open"): "Gate_Open"}
MOVE = {(0, 1): "down", (0, -1): "up", (-1, 0): "left", (1, 0): "right"}


def setmt(pieces, x, y, mid):
    blocked = "FALSE" if pieces.passable(mid) else "TRUE"
    return f"setmetatile({x}, {y}, METATILE_TempleArtemis_{LABEL[pieces.name[mid]]}, {blocked})"


def hind_run(pieces, g, a, b):
    """The hind's bolt from clearing a to clearing b: bounds of two tiles (over bushes,
    stelae, anything) and quick steps, landing only on open lawn that no hound walks and
    no one stands on. Fewest moves, then fewest steps."""
    people = {(x, y) for lid, _, x, y, *_ in PEOPLE if lid != "LOCALID_ARTEMIS_HIND"}
    walked = set()
    for n, h in enumerate(HOUNDS):
        if h[1] == 3:
            period, state = patrol(n)
            walked |= {state(t)[0] for t in range(0, period, STEP)} | {(h[2], h[3])}

    def ok(x, y):
        return (0 <= x < W and 0 <= y < H and pieces.passable(g[y][x])
                and (x, y) not in walked and (x, y) not in people)
    start, goal = HIND[a], HIND[b]
    prev = {start: None}
    todo = deque([start])
    while todo:
        p = todo.popleft()
        if p == goal:
            break
        for (dx, dy), word in MOVE.items():
            for k, verb in ((2, "jump_2"), (1, "walk_faster")):
                q = (p[0] + dx * k, p[1] + dy * k)
                if q not in prev and ok(*q):
                    prev[q] = (p, f"{verb}_{word}")
                    todo.append(q)
    if goal not in prev:
        raise ValueError(f"the hind can't run from {a} to {b}")
    moves = []
    q = goal
    while prev[q]:
        p, mv = prev[q]
        moves.append(mv)
        q = p
    return moves[::-1]


def generated_script(pieces, g):
    out = [SCRIPT_BEGIN, ""]
    done = staged(pieces, g, done=True, gate=True)
    out.append("// The garden from the hunt's state: the stair's hedge down from the hind's third")
    out.append("// touch, Anthia's gate open once she is beaten.")
    out.append(f"script {PREFIX}DrawGarden {{")
    out.append("    if (var(VAR_ICHOR_HUNT) >= 60) {")
    for (x, y) in STAIR_HEDGE:
        out.append("        " + setmt(pieces, x, y, done[y][x]))
    out.append("    }")
    out.append("    if (defeated(TRAINER_ICHOR_ANTHIA)) {")
    for (x, y) in (GATE_TOP, GATE):
        out.append("        " + setmt(pieces, x, y, done[y][x]))
    out.append("    }")
    out.append("    return")
    out.append("}")
    out.append("")
    out.append("// The hind in the clearing she last ran to (A again once the hunt is over).")
    out.append(f"script {PREFIX}PlaceHind {{")
    for band, key in ((50, "C"), (40, "B")):
        kw = "if" if band == 50 else "} elif"
        out.append(f"    {kw} (var(VAR_ICHOR_HUNT) >= {band} && var(VAR_ICHOR_HUNT) < 60) {{")
        out.append(f"        setobjectxyperm(LOCALID_ARTEMIS_HIND, {HIND[key][0]}, {HIND[key][1]})")
    out.append("    }")
    out.append("    return")
    out.append("}")
    out.append("")
    out.append("// A hound walked the player back: one more return in this stage (up to 3).")
    out.append(f"script {PREFIX}AddReturn {{")
    for band in BANDS:
        out.append(f"    if (var(VAR_ICHOR_HUNT) >= {band} && var(VAR_ICHOR_HUNT) < {band + 3}) {{")
        out.append("        addvar(VAR_ICHOR_HUNT, 1)")
        out.append("        return")
        out.append("    }")
    out.append("    return")
    out.append("}")
    out.append("")
    out.append("// In by the door: the returns count again from nothing (SCRIPT.md: VAR_TEMP_1's reset).")
    out.append(f"script {PREFIX}ResetReturns {{")
    for band in BANDS:
        out.append(f"    if (var(VAR_ICHOR_HUNT) > {band} && var(VAR_ICHOR_HUNT) < {band + 10}) {{")
        out.append(f"        setvar(VAR_ICHOR_HUNT, {band})")
        out.append("    }")
    out.append("    return")
    out.append("}")
    out.append("")
    out.append("// Back to the current stage's arch, facing in (the screen is already black).")
    out.append(f"script {PREFIX}ReturnToArch {{")
    groups = {}
    for band, xy in ARCH_RETURN.items():
        groups.setdefault(xy, []).append(band)
    first = True
    for xy, bands in sorted(groups.items(), key=lambda kv: -min(kv[1])):
        kw = "if" if first else "} elif"
        out.append(f"    {kw} (var(VAR_ICHOR_HUNT) >= {min(bands)}) {{")
        out.append(f"        warpsilent(MAP_ARKADIA_TEMPLE_OF_ARTEMIS, {xy[0]}, {xy[1]})")
        first = False
    out.append("    } else {")
    lo = min(ARCH_RETURN)
    out.append(f"        warpsilent(MAP_ARKADIA_TEMPLE_OF_ARTEMIS, {ARCH_RETURN[lo][0]}, {ARCH_RETURN[lo][1]})")
    out.append("    }")
    out.append("    waitstate")
    out.append("    return")
    out.append("}")
    for a, b in (("A", "B"), ("B", "C")):
        out.append("")
        out.append(f"// The hind bolts from clearing {a} to clearing {b}.")
        out.append(f"movement {MPREFIX}HindTo{b} {{")
        for mv in hind_run(pieces, g, a, b):
            out.append(f"    {mv}")
        out.append("    face_down")
        out.append("}")
    out.append("")
    out.append(SCRIPT_END)
    return "\n".join(out)


def spliced_script(pieces, g):
    text = (MAP_DIR / "scripts.pory").read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"temple_artemis: scripts.pory needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    return text[:a] + generated_script(pieces, g) + text[b + len(SCRIPT_END):]


# --- Checks -----------------------------------------------------------------------------

def walkable(pieces, g, x, y):
    return 0 <= y < H and 0 <= x < W and pieces.passable(g[y][x])


def reachable(pieces, g, start, blocked=()):
    seen = {start}
    todo = deque([start])
    while todo:
        x, y = todo.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and n not in blocked and walkable(pieces, g, *n):
                seen.add(n)
                todo.append(n)
    return seen


def metatile_labels():
    text = (ROOT / "include/constants/metatile_labels.h").read_text()
    return {k: int(v, 16) for k, v in re.findall(r"#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+)", text)}


def sight_tiles(pieces, g, x, y, facing, sight):
    dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[facing]
    out = []
    for k in range(1, sight + 1):
        if not walkable(pieces, g, x + dx * k, y + dy * k):
            break
        out.append((x + dx * k, y + dy * k))
    return out


def check(pieces, g, ev):
    errors = []
    people = {(o["x"], o["y"]) for o in ev["object_events"]
              if not o["local_id"].startswith(("LOCALID_ARTEMIS_HOUND", "LOCALID_ARTEMIS_SLEEPER"))}
    done = staged(pieces, g, done=True, gate=True)
    door = DOOR[0]
    for lid, gfx, x, y, *_ in PEOPLE:
        if not walkable(pieces, g, x, y):
            errors.append(f"{lid} stands on a blocking tile")
    for n, h in enumerate(HOUNDS):
        period, state = patrol(n)
        for t in range(0, period, STEP):
            for p in state(t)[:2]:
                if not walkable(pieces, g, *p) or p in people:
                    errors.append(f"H{n + 1}'s patrol crosses a blocked or occupied tile {p}")
    for w in ev["warp_events"]:
        if pieces.name[g[w["y"]][w["x"]]][1] not in ("mat_l", "mat_r"):
            errors.append(f"warp at ({w['x']},{w['y']}) is not on the doormat")
    for xy in HIND.values():
        if not walkable(pieces, g, *xy):
            errors.append(f"the hind's clearing {xy} is blocked")
    everywhere = reachable(pieces, done, door, people)
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        if b["type"] == "hidden_item":
            if (x, y) not in everywhere and not any((x + dx, y + dy) in everywhere
                                                  for dx, dy in DIRV.values()):
                errors.append(f"hidden item at ({x},{y}) can't be reached")
            continue
        if walkable(pieces, g, x, y):
            errors.append(f"bg event at ({x},{y}) is on a walkable tile")
        if not any((x + dx, y + dy) in everywhere for dx, dy in DIRV.values()):
            errors.append(f"bg event at ({x},{y}) can't be faced from anywhere")
    # every walkable tile reachable once the hunt is done and the gate open
    every = {(x, y) for y in range(H) for x in range(W) if walkable(pieces, done, x, y)} - people
    stranded = sorted(every - everywhere)
    if stranded:
        errors.append(f"walkable but unreachable: {stranded}")
    # the rock only up its stair: with the hedge up, no part of it is reachable
    before = reachable(pieces, staged(pieces, g, gate=True), door, people)
    for xy in [(13, 7), (14, 7), (14, 4), (15, 3)]:
        if xy in before:
            errors.append(f"{xy} on the rock is reachable before the stair's hedge lowers")
    # the lane north of Anthia's gate is reachable without the gate (from clearing 2), but the
    # gate is the only way from her grove to it
    grove = reachable(pieces, staged(pieces, g), (3, 31), people | {(7, 30)})
    if (2, 26) in grove:
        errors.append("Anthia's grove reaches the lane without the gate")
    # the acolytes stand across the only way
    for lid, gfx, x, y, facing, sight, script, flag in PEOPLE:
        if script not in ("Kyrene", "Prokris"):
            continue
        line = set(sight_tiles(pieces, done, x, y, facing, sight))
        target = (22, 35) if script == "Kyrene" else (14, 4)
        if target in reachable(pieces, done, door, people | line):
            errors.append(f"{script} can be walked round on the way to {target}")
    # no hound ever looks along an acolyte's line, or at an arch it walks the player back to
    plist = [(x, y) for lid, _, x, y, *_ in PEOPLE if lid != "LOCALID_ARTEMIS_HIND"]
    lines = set()
    for lid, gfx, x, y, facing, sight, script, flag in PEOPLE:
        if sight:
            lines |= set(sight_tiles(pieces, done, x, y, facing, sight)) | {(x, y)}
    for stage in (1, 2, 3):
        for hind in HIND.values():
            hunt = Hunt(pieces, g, stage, hind, plist)
            seen = hunt.ever_seen()
            if seen & lines:
                errors.append(f"a stage {stage} hound sees an acolyte's line at {sorted(seen & lines)}")
            for xy in set(ARCH_RETURN.values()) | {door, DOOR[1]}:
                if xy in seen:
                    errors.append(f"a stage {stage} hound sees the arch tile {xy}")
    # setmetatile() puts a piece's own other state on its cell
    labels = metatile_labels()
    script = (MAP_DIR / "scripts.pory").read_text()
    for x, y, lab in re.findall(r"setmetatile\((\d+),\s*(\d+),\s*(METATILE_\w+)", script):
        x, y = int(x), int(y)
        if lab not in labels:
            errors.append(f"setmetatile uses unknown label {lab}")
        elif labels[lab] not in (g[y][x], done[y][x]):
            errors.append(f"setmetatile({x}, {y}, {lab}) is not a state of {pieces.name[g[y][x]]}")
    if script != spliced_script(pieces, g):
        errors.append("scripts.pory's generated scripts are out of date; run tools/ichor/maps/temple_artemis.py")
    _, sim = simulate(pieces, g, verbose=False)
    errors += sim
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="verify the layout files are current")
    ap.add_argument("--review", metavar="NAME", help="write review sheets from the art")
    args = ap.parse_args()

    pieces = Pieces(load_catalog())
    g = grid_ids(pieces)
    if args.review:
        print("hunt:")
        simulate(pieces, g)
        for p in review(args.review, pieces, g):
            print(p.relative_to(ROOT))
        return

    layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    layout = next(lo for lo in layouts if lo.get("id") == LAYOUT_ID)
    if (layout["width"], layout["height"]) != (W, H):
        sys.exit(f"temple_artemis: layouts.json says {layout['width']}x{layout['height']}, the plan is {W}x{H}")

    blocks, border = layout_blocks(pieces, g), border_blocks(pieces)
    ev = events()
    if args.check:
        stale = [p.name for p, want in ((LAYOUT_DIR / "map.bin", blocks), (LAYOUT_DIR / "border.bin", border))
                 if not p.exists() or not np.array_equal(np.fromfile(p, "<u2"), want)]
        cur = json.loads((MAP_DIR / "map.json").read_text())
        if any(cur[k] != v for k, v in ev.items()):
            stale.append("map.json")
        if stale:
            sys.exit(f"temple_artemis: {', '.join(stale)} out of date; run tools/ichor/maps/temple_artemis.py")
    else:
        LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
        blocks.tofile(LAYOUT_DIR / "map.bin")
        border.tofile(LAYOUT_DIR / "border.bin")
        write_map_json(ev)
        (MAP_DIR / "scripts.pory").write_text(spliced_script(pieces, g))

    print("hunt:")
    simulate(pieces, g)
    errors = check(pieces, g, ev)
    if errors:
        sys.exit("temple_artemis: " + "\n  ".join(["layout check failed:"] + errors))

    if not args.check:
        r = compiled_renderer(layout)
        first = render_map.render_blocks(r, blocks, W)
        solved = render_map.render_blocks(r, layout_blocks(pieces, staged(pieces, g, done=True, gate=True)), W)
        IMG.mkdir(parents=True, exist_ok=True)
        scaled(first, 2).save(IMG / "Arkadia_TempleOfArtemis.png")
        scaled(solved, 2).save(IMG / "temple_artemis_map_solved.png")
        objects_overlay(scaled(first, 2), ev, pieces, g).save(IMG / "temple_artemis_map_events.png")
    print(f"temple_artemis: {W}x{H} on {layout['primary_tileset']} + {layout['secondary_tileset']}, "
          f"{len(ev['object_events'])} objects, {len(ev['coord_events'])} triggers, "
          f"{len(ev['bg_events'])} bg events; checks pass")


if __name__ == "__main__":
    main()
