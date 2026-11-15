#!/usr/bin/env python3
"""Build Route 5, the Skironian cliffs: layout, events, checks and review renders.

The Sacred Way out of Hecate's Hollow, down the sea cliffs to Eleusa
(design/phase2/SCRIPT.md, "Route 3, the Pine Slopes", and beat 19's road;
design/AETHOS_MAP.md, Route 5; design/phase2/BUILD.md, batch 3). The road is a
switchback in three legs, each a step lower toward the sea:

  A, the cliff road: out of the Hollow's west mouth and east along the brink of
     a tall sea cliff. The first view of the bay; a pine clearing the road
     can't get round (the first forced band); the narrow ledge past the rock
     seat where a king watched his fleet lose (Kynegeiros); the ruined
     watchtower up its knoll behind a fallen column drum (the Girdle, Act II);
     a pine hollow behind a thorn thicket (the Sickle); the fork to the thyme
     meadow and its hives (optional: Aristaios, the Super Repel, the Honey).
  B, the terrace: down a cutting and back west under the cliff. The second
     forced band, then Aphrodite's votive niches cut in the bank (her altar,
     Myrto), and a lookout at the terrace's end.
  C, the shore road: down a cleft stair (Mopsos watches it) to the beach under
     the cliffs. The shore point behind marble rubble (the Hammer), the old
     fisher and his Good Rod, a third forced band, the roadside inn (rest, and
     Xenokles's trade), the great herm, and the olives of Eleusa's plain.

Pieces come by key and name from build/skiron/catalog.json (TILES_skiron.md;
make it with /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile).

Writes:
  data/layouts/Route5_SkironianCliffs/map.bin, border.bin  (68x31, aethos + skiron)
  data/maps/Route5_SkironianCliffs/map.json                 its events and connections
  the layout's size and tilesets in data/layouts/layouts.json

Checks: the seams (Eleusa's west edge at our rows 21-24; aethos metatiles only
in our 8 easternmost columns), the Hollow's mouth is a door, every person,
item, sign and hidden item can be reached and read, the forced bands and the
mandatory trainers' sight lines can't be walked round, and nothing walkable is
cut off from the mouth.

Usage: /usr/bin/python3 tools/ichor/maps/route5.py [--render DIR] [--walk]
  --render DIR  route5.png (2x, with people), route5_walk.png (collision and
                events), screen views along the road and a contact sheet
  --walk        prints the walk map (# solid, . reachable, ? cut off, , grass)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))

CAT = ROOT / "build/skiron/catalog.json"
NAME = "Route5_SkironianCliffs"
MAP_ID = "MAP_ROUTE5_SKIRONIAN_CLIFFS"
LAYOUT_ID = "LAYOUT_ROUTE5_SKIRONIAN_CLIFFS"
MAP_DIR = ROOT / "data/maps" / NAME
LAYOUT_DIR = ROOT / "data/layouts" / NAME
W, H = 68, 31

# ---------------------------------------------------------------------------
# The seams
# ---------------------------------------------------------------------------
# East: Eleusa's west edge is open at its rows 24-27 (BUILD.md, batch 4). Ours
# are 21-24, so Eleusa's y = 0 sits at our y = -3. Eleusa's 8 columns nearest
# the seam are aethos only, and so are ours (MAP_DESIGN.md section 5).
EAST_SEAM = range(21, 25)
ELEUSA_OFFSET = -3            # our right connection; Eleusa's left one is +3
STRIP = 8                     # x >= W - STRIP: aethos metatiles only

# West: Hecate's Hollow's west mouth, a cave door in the cut bank above the
# cliff road. The Hollow agent picks its warp ids in parallel: point at its
# west-mouth warp once it lands (BUILD.md's table has our mouth tile).
MOUTH = (9, 8)
HOLLOW_MAP = "MAP_HECATES_HOLLOW"
HOLLOW_WARP_ID = 0            # placeholder: the Hollow's west-mouth warp id
# Until MAP_HECATES_HOLLOW is registered, the mouth leads back to Emporion (the
# nearest map on the Hollow's side) so the ROM still builds; see dest_hollow().

# ---------------------------------------------------------------------------
# aethos ids (design/phase1/TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS, TALL, FLOWERS = 0x001, 0x00D, 0x004
SIGN, HERM = 0x003, 0x01B
SEA = 0x170
BOULDER = 0x0E0               # tan boulder on grass
CAVE_TOP, CAVE_DOOR = 0x09F, 0x0A7   # General's cave mouth, retextured (MB_NON_ANIMATED_DOOR)
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
SAND = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
        "bl": 0x128, "b": 0x129, "br": 0x12A}           # sand on grass, soft edges
SHORE = {"b": 0x12C, "bl": 0x12B, "br": 0x12D, "l": 0x123, "r": 0x125,
         "c": 0x124}                                       # water with the beach's surf at its edge
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
CYPRESS_BOT_UNDER_TIP = (0x1F4, 0x1F5)
STONE_PINE = ((0x01E, 0x01F), (0x026, 0x027))
# the roadside inn: aethos's farmhouse (General's route house), widened to 5
INN = [[0x008, 0x009, 0x009, 0x009, 0x00A],
       [0x010, 0x011, 0x011, 0x011, 0x012],
       [0x018, 0x01A, 0x019, 0x01A, 0x01A],
       [0x020, 0x019, 0x021, 0x019, 0x022]]
INN_DOOR = (2, 3)


def behavior_names():
    txt = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    out, v = {}, 0
    for name, val in re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", txt, re.M):
        if val:
            v = int(val, 0)
        out[v] = name
        v += 1
    return out


MB = behavior_names()
AETHOS_ATTR = np.fromfile(ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin", "<u2")
SKIRON_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/skiron/porytiles_bin/metatile_attributes.bin", "<u2")


def behavior(mid):
    a = AETHOS_ATTR[mid] if mid < 0x200 else SKIRON_ATTR[mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def noise(x, y, salt=0):
    """A stable 0..99 per cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 100


DIRS8 = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # N NE E SE S SW W NW


def canon(center, neigh):
    """skiron_ground's shape key: diagonals count only when both sides are in."""
    b = list(neigh)
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] == "1" and b[c] == "1"):
            b[d] = "0"
    return center + "|" + "".join(b)


FULL = "1|11111111"


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------
# Ground kinds, before anything stands on them:
#   wood   woods: filled with pines, scrub and rock (impassable)
#   olive  olive grove: aethos olives in 2x2 blocks (impassable; the east strip)
#   grass  plain grass          flowers  grass with anemones
#   path   the limestone road   tall     tall grass   meadow  the thyme meadow
#   sand   the beach            sea      open sea      shore  water at the beach's edge

class Grid:
    def __init__(self):
        self.cat = {s["key"]: s for s in json.loads(CAT.read_text())}
        self.g = [["wood"] * W for _ in range(H)]
        self.mt = np.full((H, W), GRASS, np.int32)
        self.solid = np.zeros((H, W), bool)
        self.water = np.zeros((H, W), bool)
        self.fixed = np.zeros((H, W), bool)
        self.path_floor = np.zeros((H, W), bool)   # pieces drawn on the aethos path
        self.kind = np.full((H, W), "", object)    # what stands here, for checks and fills
        self.missing = set()

    # --- regions ----------------------------------------------------------------
    def fill(self, kind, x0, y0, x1, y1):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                self.g[y][x] = kind

    def rows(self, kind, ox, oy, rows):
        """A mask of '#' cells, top-left at (ox, oy)."""
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c == "#":
                    self.g[oy + j][ox + i] = kind

    def at(self, x, y):
        return self.g[y][x] if 0 <= x < W and 0 <= y < H else None

    # --- pieces -------------------------------------------------------------------
    def set(self, x, y, mid, solid, kind="", water=False):
        if 0 <= x < W and 0 <= y < H:
            self.mt[y, x] = mid
            self.solid[y, x] = solid
            self.water[y, x] = water
            self.fixed[y, x] = True
            self.kind[y, x] = kind

    def piece(self, key, x, y, cells=None, kind=None, block_t=False):
        """A Skiron structure, top-left at (x, y). Walk codes: X blocks, . and G
        are open, T (a crown the player walks behind) is open unless block_t."""
        s = self.cat[key]
        for cy in range(s["h"]):
            for cx in range(s["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                X, Y = x + cx, y + cy
                if not (0 <= X < W and 0 <= Y < H):
                    continue
                code = s["walk"][cy][cx]
                solid = code == "X" or (code == "T" and block_t) or (code == "." and kind == "woods")
                sea = s["ground"].get(f"{cx},{cy}") == "sea"
                self.set(X, Y, s["ids"][cy][cx], solid, kind or key, water=sea and not solid)
                if s["ground"].get(f"{cx},{cy}") == "path":
                    self.path_floor[Y, X] = True

    def named(self, key, name, x, y, kind=None):
        s = self.cat[key]
        cx, cy = s["names"][name]
        self.piece(key, x - cx, y - cy, cells={(cx, cy)}, kind=kind)

    def free(self, x, y, w=1, h=1, kinds=("wood",)):
        return all(0 <= x + i < W and 0 <= y + j < H and self.g[y + j][x + i] in kinds
                   and not self.fixed[y + j, x + i] for j in range(h) for i in range(w))

    # --- aethos trees -------------------------------------------------------------
    def olive(self, x, y):
        for i in range(2):
            self.set(x + i, y, OLIVE_TOP[i], True, "olive_top")
            self.set(x + i, y + 1, OLIVE_BOT[i], True, "olive_bot")

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True, "cypress_top")
        self.set(x, y + 1, CYPRESS_BOT, True, "cypress_bot")

    def stone_pine(self, x, y):
        for j in range(2):
            for i in range(2):
                self.set(x + i, y + j, STONE_PINE[j][i], True, "stone_pine")


def fv(x, y, salt=1):
    """A cliff face variant: mostly plain strata, a feature one cell in four."""
    r = noise(x, y, salt)
    return "B" if r < 12 else "C" if r < 25 else "A"


def foot(x, y):
    return "ABC"[noise(x, y, 5) % 3]


# ---------------------------------------------------------------------------
# Where things are (the events below refer to these)
# ---------------------------------------------------------------------------
A_ROWS = (9, 11)              # the cliff road: a 2-wide road on rows 9-10, a verge on 11
A_X = (8, 48)
B_ROWS = (15, 17)             # the terrace: road on 15-16, a verge on 17
B_X = (35, 48)
C_ROWS = (21, 23)             # the shore road: road on 21-22, a verge on 23 (4 wide from x 58)
C_X = (35, W - 1)
WIDE_X = 58                   # the shore road widens to Eleusa's four rows here
CLEARING = (14, 2, 20, 8)     # the pine clearing north of the road
BAND1 = (15, 17)              # columns of the first forced band (clearing and road)
SEAT = (24, 10)               # rock_seat_path, 2x2: the road's one-cell ledge is (24..25, 9)
KNOLL_GAP = 31                # the cleft up to the watchtower's knoll
KNOLL = (26, 2, 36, 5)
TOWER = (33, 2)               # watchtower 2x4
HOLLOW_GAP = 41               # the thicket's gap into the pine hollow
PINE_HOLLOW = (38, 3, 44, 7)
STEP_X = 34                   # where the coast steps south: B's west edge
CUT_AB = (46, 48)             # the cutting from the cliff road down to the terrace
NICHES = (40, 12)             # niches 3x3: brink, face, foot
BAND2 = (43, 45)              # columns of the second forced band, on the terrace
STAIR_X = 38                  # the cleft stair from the terrace down to the shore
LOOKOUT_X = 37                # the rockfall closing the terrace's lookout (35-36)
POINT = (35, 36)              # the shore point's columns, behind the rubble at x = 37
BAND3 = (47, 49)              # columns of the third band, on the shore road
INN_AT = (52, 17)             # the inn's 5x4 front, its door at INN_AT + INN_DOOR
HERM_AT = (58, 20)            # the great herm; its landing tile is south of it
MEADOW = (49, 1, 59, 11)
SALAMIS_ROW = 27              # Salamis's shore across the strait, bottom left


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------

def make_plan(g):
    # the sea: the strait under the cliff road, and the bay past the beach
    g.fill("sea", 0, 15, STEP_X - 1, H - 1)
    g.fill("sea", STEP_X, 22, STEP_X, H - 1)
    g.fill("sea", STEP_X + 1, 27, 55, H - 1)
    # Salamis across the strait: a beach, then its pines
    g.fill("isle_shore", 0, SALAMIS_ROW, 21, SALAMIS_ROW)
    g.fill("isle_edge", 21, SALAMIS_ROW + 1, 21, H - 1)
    g.fill("isle_sand", 0, SALAMIS_ROW + 1, 20, SALAMIS_ROW + 1)
    g.fill("wood", 0, SALAMIS_ROW + 2, 20, H - 1)
    # the cliff road: two wide with a verge to the brink, running to the edge
    # by the mouth, past the seat and at the junction
    g.fill("path", A_X[0], A_ROWS[0], A_X[1], A_ROWS[0] + 1)
    g.fill("grass", A_X[0], A_ROWS[1], A_X[1], A_ROWS[1])
    for x0, x1 in ((A_X[0], 12), (21, 28), (44, A_X[1])):
        g.fill("path", x0, A_ROWS[1], x1, A_ROWS[1])
    # the cutting, the terrace and its verge
    g.fill("path", CUT_AB[0], 12, CUT_AB[1], 14)
    g.fill("path", B_X[0], B_ROWS[0], B_X[1], B_ROWS[0] + 1)
    g.fill("grass", B_X[0], B_ROWS[1], B_X[1], B_ROWS[1])
    g.fill("path", CUT_AB[0], B_ROWS[1], CUT_AB[1], B_ROWS[1])
    g.fill("path", STAIR_X, B_ROWS[1], STAIR_X, 20)
    # the shore road, its verge and the beach; four wide for Eleusa
    g.fill("path", C_X[0], C_ROWS[0], C_X[1], C_ROWS[0] + 1)
    g.fill("grass", C_X[0], C_ROWS[1], WIDE_X - 1, C_ROWS[1])
    g.fill("path", WIDE_X, C_ROWS[1], W - 1, C_ROWS[1] + 1)
    g.fill("sand", POINT[0], 24, 55, 25)
    g.fill("sand", POINT[0], C_ROWS[1], POINT[1], C_ROWS[1])
    g.fill("shore", POINT[0], 26, 55, 26)
    g.fill("grass", 56, 23, WIDE_X - 1, 24)
    # a scrubby rise between the two beaches walls the third band from the sea
    g.fill("grass", BAND3[0] - 1, 24, BAND3[1] + 2, 25)
    g.fill("rise_foot", BAND3[0] - 1, 26, BAND3[1] + 2, 26)
    # the pine clearing: grass among fallen boulders, the band right through it
    x0, y0, x1, y1 = CLEARING
    g.fill("grass", x0, y0 + 1, x1, y1)
    g.rows("tall", 14, 3, [".#####.",
                           ".######",
                           "..#####",
                           ".####..",
                           ".###...",
                           ".###...",
                           ".###...",
                           ".###...",
                           ".###..."])
    # the watchtower's knoll, up the cleft
    x0, y0, x1, y1 = KNOLL
    g.fill("grass", x0, y0, x1, y1)
    g.fill("path", KNOLL_GAP, y1 + 1, KNOLL_GAP, 8)
    g.rows("tall", 27, 2, ["###.",
                           "###.",
                           ".##."])
    # the pine hollow, behind the thicket
    x0, y0, x1, y1 = PINE_HOLLOW
    g.fill("grass", x0 + 1, y0, x1 - 1, y1)
    g.fill("grass", x0, y0 + 1, x1, y1 - 1)
    g.fill("grass", HOLLOW_GAP, y1 + 1, HOLLOW_GAP, 8)
    g.rows("tall", 39, 4, ["..###",
                           "..###",
                           "..##."])
    # the thyme meadow, off the road's east end
    g.rows("grass", 49, 1, [".....######",
                            "...########",
                            "..#########",
                            ".##########",
                            "###########",
                            "###########",
                            "###########",
                            "###########",
                            "###########",
                            "###########",
                            "##########."])
    g.rows("meadow", 50, 2, ["......###..",
                             "....######.",
                             "...#######.",
                             "..######...",
                             ".######....",
                             ".#####.....",
                             "..###......"])
    # bands across the terrace and the shore road
    g.fill("tall", BAND2[0], B_ROWS[0], BAND2[1], B_ROWS[1])
    g.fill("tall", BAND3[0], C_ROWS[0], BAND3[1], C_ROWS[1])
    # the inn's yard and the herm's foot
    g.fill("grass", 57, 18, 59, 20)
    # the olives of Eleusa's plain: the east strip, matching Eleusa's own, with
    # a ragged west edge
    g.fill("olive", 60, 0, W - 1, 20)
    g.fill("olive", WIDE_X, 25, W - 1, H - 1)
    g.fill("olive", 56, 25, 57, H - 1)
    g.fill("olive", 58, 13, 59, 16)
    return g


# ---------------------------------------------------------------------------
# Cliffs and banks
# ---------------------------------------------------------------------------

def bank_run(g, x0, x1, y, ends=(False, False)):
    """A cut bank, three rows from y: brink, face, foot (scree on the path or
    on grass, whichever lies below). ends=(west, east) close the run."""
    for x in range(x0, x1 + 1):
        below = g.at(x, y + 3)
        on_path = below in ("path", "sand")
        if ends[0] and x == x0:
            g.named("bank_end_w", "brink", x, y)
            g.named("bank_end_w", "face_u", x, y + 1)
            g.named("bank_end" if on_path else "bank_end_grass", "foot_w", x, y + 2)
            continue
        if ends[1] and x == x1:
            g.named("bank_end_e", "brink", x, y)
            g.named("bank_end_e", "face_u", x, y + 1)
            g.named("bank_end" if on_path else "bank_end_grass", "foot_e", x, y + 2)
            continue
        g.named("cliff_brink", "bite" if noise(x, y, 9) < 8 else ("B" if noise(x, y, 4) < 22 else "A"), x, y)
        g.named("cliff", "face_u_" + fv(x, y + 1, 2), x, y + 1)
        g.named("bank" if on_path else "bank_grass", "foot_" + foot(x, y + 2), x, y + 2)


def cliffs(g):
    # A's sea cliff, west of the step: brink, face and foot, the strait below
    # (three rows, so the sea shows from the road)
    for x in range(0, STEP_X):
        above_path = g.at(x, 11) == "path"
        key = "cliff_path" if above_path else "cliff_brink"
        g.named(key, "bite" if x in (13, 30) else ("B" if noise(x, 12, 6) < 20 else "A"), x, 12)
        g.named("cliff", "face_u_" + fv(x, 13), x, 13)
        g.named("cliff", "foot_" + foot(x, 14), x, 14)
    # the bank between the cliff road and the terrace: its brink runs on from
    # the sea cliff's, and the terrace's west edge drops to the strait
    g.named("cliff_brink", "A", STEP_X, 12)
    g.named("cliff", "face_u_A", STEP_X, 13)
    for y in range(14, 18):
        g.named("cliff_side", "side_w", STEP_X, y)
    bank_run(g, STEP_X + 1, CUT_AB[0] - 1, 12, ends=(False, True))
    # the niches of Aphrodite, set into that bank
    g.piece("niches", NICHES[0], NICHES[1])
    # east of the cutting the bank runs on under the meadow, over a scrub ledge
    bank_run(g, CUT_AB[1] + 1, 59, 12, ends=(True, False))
    # the bank between the terrace and the shore, with the cleft stair; its
    # west end stands in the sea
    g.named("cliff_end_w", "brink", STEP_X, 18)
    g.named("cliff_end_w", "face_u", STEP_X, 19)
    g.named("cliff_end_w", "face_l", STEP_X, 20)
    g.named("cliff_end_w", "foot", STEP_X, 21)
    bank_run(g, STEP_X + 1, STAIR_X - 1, 18, ends=(False, True))
    bank_run(g, STAIR_X + 1, INN_AT[0] - 1, 18, ends=(True, True))
    # the cut bank over the cliff road, broken by the clearing, the knoll's
    # cleft and the woods round the pine hollow
    bank_run(g, 0, CLEARING[0] - 1, 6, ends=(False, True))
    bank_run(g, CLEARING[2] + 1, KNOLL_GAP - 1, 6, ends=(True, True))
    bank_run(g, KNOLL_GAP + 1, 37, 6, ends=(True, True))
    # the Hollow's west mouth in the bank
    mx, my = MOUTH
    g.set(mx, my - 1, CAVE_TOP, True, "mouth")
    g.set(mx, my, CAVE_DOOR, False, "door")
    g.path_floor[my, mx] = True


# ---------------------------------------------------------------------------
# Woods and groves
# ---------------------------------------------------------------------------

def woods(g):
    """Fill 'wood' with Aleppo pines, kermes oak, rock and boulders, top down,
    so the tree line staggers; every woods cell is solid. Pieces may hang off
    the top edge (their crowns), never into the east strip."""
    def room(x, y, w, h):
        if x < 0 or x + w > W - STRIP:
            return False
        return all(g.g[cy][cx] == "wood" and not g.fixed[cy, cx]
                   for cy in range(max(y, 0), min(y + h, H)) for cx in range(x, x + w)) and y + h - 1 >= 0
    for y in range(-2, H):
        for x in range(0, W):
            if 0 <= y and (g.fixed[y, x] or g.g[y][x] != "wood"):
                continue
            n = noise(x, y, 21)
            if n < 34 and room(x, y, 2, 3):
                g.piece("pine_tall", x, y, block_t=True, kind="woods")
            elif n < 42 and room(x, y, 3, 3):
                g.piece("pine_lean" if noise(x, y, 3) < 50 else "pine_lean_w", x, y, block_t=True, kind="woods")
            elif y >= 0 and n < 60 and room(x, y, 1, 2):
                g.piece("pine_young", x, y, block_t=True, kind="woods")
            elif y >= 0 and n < 64 and room(x, y, 2, 2):
                g.piece("boulders", x, y, kind="woods")
    for y in range(H):
        for x in range(W):
            if g.fixed[y, x] or g.g[y][x] != "wood":
                continue
            if x >= W - STRIP:
                g.set(x, y, BOULDER, True, "woods")
                continue
            n = noise(x, y, 22)
            g.piece("oak" if n < 86 else "rock", x, y, kind="woods")


def olives(g):
    """Olives in 2x2 blocks on even columns and odd rows, like Eleusa's grove
    across the seam (Eleusa's y = ours + 3), with pairs of cypresses breaking
    them up. Each crown tips into the tree above it."""
    def oliveground(x, y):
        return 0 <= x < W and 0 <= y < H and g.g[y][x] == "olive" and not g.fixed[y, x]
    for y in range(-1, H, 2):
        for x in range(0, W, 2):
            cells = [(x + i, y + j) for j in range(2) for i in range(2) if 0 <= y + j < H]
            if not cells or not all(oliveground(cx, cy) for cx, cy in cells):
                continue
            cyp = noise(x, y, 31) < 16 and 0 <= y and y + 1 < H
            for i in range(2):
                if cyp:
                    g.cypress(x + i, y)
                    continue
                if y >= 0:
                    g.set(x + i, y, OLIVE_TOP[i], True, "olive_top")
                if y + 1 < H:
                    g.set(x + i, y + 1, OLIVE_BOT[i], True, "olive_bot")
    for y in range(H):
        for x in range(W):
            if oliveground(x, y):
                g.set(x, y, BOULDER, True, "olive")
    # crown tips: an olive's crown pokes into the cell above it
    for y in range(1, H):
        for x in range(W):
            if g.kind[y, x] != "olive_top":
                continue
            i = 0 if g.mt[y, x] == OLIVE_TOP[0] else 1
            k = g.kind[y - 1, x]
            if k == "olive_bot":
                g.mt[y - 1, x] = OLIVE_BOT_TIP[i]
            elif k == "cypress_bot":
                g.mt[y - 1, x] = CYPRESS_BOT_UNDER_TIP[i]
            elif not g.fixed[y - 1, x] and g.g[y - 1][x] in ("grass", "flowers"):
                g.set(x, y - 1, OLIVE_TIP_GRASS[i], False, "tip")


# ---------------------------------------------------------------------------
# Ground: the road, grass, the meadow, the beach and the sea, by shape
# ---------------------------------------------------------------------------

def region(g, kinds, extra=None):
    m = np.array([[g.g[y][x] in kinds for x in range(W)] for y in range(H)])
    if extra is not None:
        m |= extra
    return m


def shape_key(m, x, y):
    nb = []
    for dx, dy in DIRS8:
        X, Y = min(max(x + dx, 0), W - 1), min(max(y + dy, 0), H - 1)
        nb.append("1" if m[Y, X] else "0")
    return canon("1", nb)


def edge9(n, s, w, e):
    v = "t" if n else "b" if s else ""
    h = "l" if w else "r" if e else ""
    return (v + h) or "c"


def ground(g):
    tall = g.cat["tall"]
    thyme = g.cat["tall_thyme"]["ids"][0][0]
    pathm = region(g, ("path",), g.path_floor)
    tallm = region(g, ("tall", "meadow"))
    sandm = region(g, ("sand",))
    for y in range(H):
        for x in range(W):
            if g.fixed[y, x]:
                continue
            k = g.g[y][x]
            seam = x >= W - STRIP
            if k == "path":
                def out(dx, dy):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < W and 0 <= Y < H):
                        return False
                    return not pathm[Y, X] and g.g[Y][X] in ("grass", "tall", "meadow", "flowers", "olive", "wood")
                n, s, w, e = out(0, -1), out(0, 1), out(-1, 0), out(1, 0)
                key = "c" if (n and s) or (w and e) else edge9(n, s, w, e)
                g.set(x, y, PATH[key], False, "path")
                g.fixed[y, x] = False
            elif k in ("tall", "meadow"):
                key = shape_key(tallm, x, y)
                if key == FULL or seam:
                    mid = thyme if k == "meadow" and noise(x, y, 9) < 65 and not seam else TALL
                elif key in tall["names"]:
                    cx, cy = tall["names"][key]
                    mid = tall["ids"][cy][cx]
                else:
                    g.missing.add(f"{key}@{x},{y}")
                    mid = TALL
                g.set(x, y, mid, False, k)
                g.fixed[y, x] = False
            elif k == "sand":
                def land(dx, dy):
                    X, Y = x + dx, y + dy
                    return 0 <= X < W and 0 <= Y < H and g.g[Y][X] in ("grass", "flowers", "olive", "wood")
                n, s, w, e = land(0, -1), land(0, 1), land(-1, 0), land(1, 0)
                g.set(x, y, SAND[edge9(n, s, w, e)], False, "sand")
                g.fixed[y, x] = False
            elif k == "shore":
                def sandy(dx, dy):
                    X, Y = x + dx, y + dy
                    return 0 <= X < W and 0 <= Y < H and sandm[Y, X]
                if sandy(0, -1):
                    key = "b"
                elif sandy(-1, 0):
                    key = "r"
                else:
                    key = "l"
                g.set(x, y, SHORE[key], False, "shore", water=True)
                g.fixed[y, x] = False
            elif k == "sea":
                g.set(x, y, SEA, False, "sea", water=True)
                g.fixed[y, x] = False
            # Salamis: scenery across the strait. Its beach is solid, so no one
            # surfing over later lands on it.
            elif k == "isle_shore":
                last = g.at(x + 1, y) not in ("isle_shore",)
                g.set(x, y, 0x11D if last else 0x11C, True, "isle")
            elif k == "isle_edge":
                g.set(x, y, 0x125, False, "isle", water=True)
            elif k == "isle_sand":
                down = g.at(x, y + 1) == "wood"
                right = g.at(x + 1, y) == "wood"
                g.set(x, y, SAND["br"] if down and right else SAND["b"] if down else 0x124, True, "isle")
            elif k == "flowers":
                g.set(x, y, FLOWERS, False, "grass")
                g.fixed[y, x] = False
            elif k == "grass":
                g.set(x, y, GRASS, False, "grass")
                g.fixed[y, x] = False


# ---------------------------------------------------------------------------
# Set pieces and props
# ---------------------------------------------------------------------------

def props(g):
    # the mouth: a rockfall closes the road's west end; scree by the cave
    for (key, x, y) in (("boulders", 6, 9), ("rock", 7, 11), ("rock", 6, 11), ("boulders", 3, 10),
                        ("oak", 5, 9), ("rock", 5, 10), ("oak", 5, 11),
                        ("oak", 3, 9), ("rock", 2, 9), ("oak", 2, 10), ("oak", 2, 11), ("rock", 1, 10),
                        ("oak", 0, 9), ("oak", 1, 9), ("oak", 0, 10), ("rock", 0, 11), ("oak", 1, 11)):
        g.piece(key, x, y, block_t=True)
    g.piece("rock_path", A_X[0], 11)
    g.piece("pebbles_path", 11, 10)
    g.piece("rock", 12, 11)                     # the first view's rock, at the brink
    # the clearing: the rockfall that walls it, a young pine, scree
    for (key, x, y) in (("boulders", 15, 1), ("rock", 14, 2), ("boulders", 18, 1), ("rock", 17, 2),
                        ("rock", 20, 3), ("rock", 14, 3), ("pebbles", 20, 7), ("rock", 20, 5),
                        ("pine_young", 19, 6), ("dry_grass", 18, 8), ("thyme", 14, 8), ("pebbles", 21, 4)):
        g.piece(key, x, y, block_t=True)
    # the rock seat on its shoulder of the edge; rocks narrow the road beside it
    g.piece("rock_seat_path", SEAT[0], SEAT[1])
    g.piece("rock_path", SEAT[0] - 1, 11)
    g.piece("pebbles_path", SEAT[0] - 3, 10)
    g.piece("pebbles_path", SEAT[0] + 3, 10)
    # verges along the cliff road: thyme, flowers, dry grass at the brink
    for x in range(A_X[0], A_X[1] + 1):
        if g.g[11][x] == "grass" and not g.fixed[11, x]:
            r = noise(x, 11, 13)
            if r < 14:
                g.piece("thyme", x, 11)
            elif r < 24:
                g.g[11][x] = "flowers"
            elif r < 30:
                g.piece("dry_grass", x, 11)
    # the knoll: the watchtower, rocks, a fallen drum and dry grass
    g.piece("watchtower", TOWER[0], TOWER[1])
    for (key, x, y) in (("rock", 26, 5), ("pebbles", 29, 5), ("dry_grass", 30, 4), ("thyme", 32, 5),
                        ("drum", 35, 3), ("rock", 36, 5), ("dry_grass", 35, 4), ("pine_young", 26, 3)):
        g.piece(key, x, y, block_t=True)
    # the pine hollow: a quiet ring of grass; scree by the gap
    g.piece("dry_grass", 39, 7)
    g.piece("pebbles", 43, 6)
    g.piece("thyme", 38, 5)
    # the pitch-gatherer's jars, by the pines over the road
    g.piece("amphorae", 38, 8)
    # the meadow: hives on their benches, thyme, a lone pine; the beekeeper's
    for (key, x, y) in (("hives", 55, 3), ("hives", 57, 5), ("hives", 53, 8), ("hives", 56, 8),
                        ("thyme", 51, 9), ("thyme", 49, 6), ("thyme", 58, 9), ("thyme", 54, 1),
                        ("thyme", 50, 10), ("thyme", 55, 10), ("thyme", 59, 6), ("thyme", 52, 1),
                        ("dry_grass", 52, 10), ("pebbles", 59, 7), ("pine_young", 50, 1),
                        ("rock", 59, 10), ("pine_tall", 57, 9)):
        g.piece(key, x, y, block_t=True)
    for (x, y) in ((49, 4), (50, 5), (58, 7), (53, 11), (57, 2), (51, 8)):
        if g.g[y][x] == "grass" and not g.fixed[y, x]:
            g.g[y][x] = "flowers"
    # the olive grove's ragged west edge, stepping into the meadow
    g.olive(58, 0)
    g.cypress(59, 4)
    # the terrace: a rockfall closes the lookout at its west end (the rubble in
    # its middle breaks to the Hammer); scree under the niches, flowers on the verge
    g.piece("rock_path", LOOKOUT_X, B_ROWS[0])
    g.piece("rock", LOOKOUT_X, B_ROWS[1])
    g.piece("pebbles_path", 39, 16)
    g.piece("pebbles", B_X[0], B_ROWS[1])
    for x in range(B_X[0], B_X[1] + 1):
        if g.g[B_ROWS[1]][x] == "grass" and not g.fixed[B_ROWS[1], x]:
            r = noise(x, B_ROWS[1], 17)
            if r < 18:
                g.piece("thyme", x, B_ROWS[1])
            elif r < 34:
                g.g[B_ROWS[1]][x] = "flowers"
    # the shore road: a scrubby rise of rock and kermes oak between the two
    # beaches, its foot in the surf, walls the third band from the sea
    x0 = BAND3[0] - 1
    for (key, x, y) in (("boulders", x0, 24), ("oak", x0 + 2, 24), ("rock", x0 + 2, 25),
                        ("boulders", x0 + 3, 24), ("oak", x0 + 5, 24), ("rock", x0 + 5, 25)):
        g.piece(key, x, y)
    for x in range(x0, BAND3[1] + 3):
        g.named("cliff", "foot_" + foot(x, 26), x, 26)
    # the shore point: rocks at its tip
    g.set(POINT[0], 26, 0x18C, True, "rock")
    for x in range(C_X[0], WIDE_X):
        if g.g[C_ROWS[1]][x] == "grass" and not g.fixed[C_ROWS[1], x]:
            r = noise(x, C_ROWS[1], 19)
            if r < 16:
                g.piece("thyme", x, C_ROWS[1])
            elif r < 30:
                g.g[C_ROWS[1]][x] = "flowers"
    # surf rocks and sea stacks in the strait and the bay
    for (x, y, v) in ((3, 16, "A"), (12, 17, "B"), (19, 16, "A"), (27, 18, "B"), (7, 21, "A"),
                      (23, 23, "B"), (15, 22, "A"), (30, 25, "A"), (40, 28, "B"), (49, 29, "A")):
        g.named("surf_rock", v, x, y)
    for (x, y) in ((9, 18), (31, 21), (26, 28), (44, 29), (1, 24), (52, 28)):
        g.set(x, y, 0x18C, True, "rock")
    # the inn, set into the foot of the hill, its yard and stable
    ix, iy = INN_AT
    for j, row in enumerate(INN):
        for i, mid in enumerate(row):
            door = (i, j) == INN_DOOR
            g.set(ix + i, iy + j, mid, not door, "door" if door else "inn")
    g.piece("firewood", 57, 18)
    g.piece("amphorae", 59, 18)
    # the great herm at the foot of the slope, and the signs
    g.set(HERM_AT[0], HERM_AT[1], HERM, True, "herm")
    for (x, y) in SIGNS_AT:
        g.set(x, y, SIGN, True, "sign")


# Signs (stelai): the mouth, the meadow fork, the east end
SIGNS_AT = [(8, 9), (47, 8), (57, 24)]


def compose():
    g = Grid()
    make_plan(g)
    cliffs(g)
    props(g)
    olives(g)
    woods(g)
    ground(g)
    return g


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
GFX = "OBJ_EVENT_GFX_ICHOR_"
PX = "Route5_SkironianCliffs_EventScript_"

# Trainers: (local id, graphics, x, y, facing, sight, script, trainer constant)
TRAINERS = [
    # Mandatory, both: each stands beside the one cell out of a 1-wide way (the
    # ledge past the seat, the cleft stair's foot) and sees only that cell, so he
    # never steps into the narrow way and blocks it after the battle.
    ("KYNEGEIROS", GFX + "HOPLITE", SEAT[0] + 2, SEAT[1], "UP", 1, "Kynegeiros", "TRAINER_ICHOR_KYNEGEIROS"),
    ("MELANTHIOS", GFX + "GOATHERD", 32, 9, "LEFT", 3, "Melanthios", "TRAINER_ICHOR_MELANTHIOS"),
    ("MYRTO", GFX + "PILGRIM", 39, 15, "UP", 1, "Myrto", "TRAINER_ICHOR_MYRTO"),
    ("ARISTAIOS", GFX + "HARVESTER", 54, 5, "DOWN", 3, "Aristaios", "TRAINER_ICHOR_ARISTAIOS"),
    ("MOPSOS", GFX + "AUGUR", STAIR_X + 1, C_ROWS[0], "LEFT", 1, "Mopsos", "TRAINER_ICHOR_MOPSOS"),
]
# People: (local id, graphics, x, y, facing, script, hide flag)
PEOPLE = [
    ("PITCH_GATHERER", GFX + "MAN", 39, 9, "UP", "PitchGatherer", "0"),
    ("KID_GOAT", "OBJ_EVENT_GFX_SPECIES(ERIPIP)", 30, 10, "LEFT", "Goat", "0"),
    ("AIGIALEUS", GFX + "FISHER", 41, 25, "DOWN", "Aigialeus", "0"),
    ("PILGRIM_A", GFX + "YOUTH_F", 52, 24, "RIGHT", "PilgrimA", "0"),
    ("PILGRIM_B", GFX + "YOUTH_M", 53, 24, "LEFT", "PilgrimB", "0"),
    ("BOAT_L", GFX + "UPTURNED_BOAT_L", 43, 25, "DOWN", "Boat", "0"),
    ("BOAT_R", GFX + "UPTURNED_BOAT_R", 44, 25, "DOWN", "Boat", "0"),
]
# Relic gates: (local id, graphics, x, y, script, hide flag)
OBSTACLES = [
    ("DRUM", "OBJ_EVENT_GFX_PUSHABLE_BOULDER", KNOLL_GAP, 8, "EventScript_StrengthBoulder", "0"),
    ("THICKET", "OBJ_EVENT_GFX_CUTTABLE_TREE", HOLLOW_GAP, 8, "EventScript_CutTree",
     "FLAG_ICHOR_ROUTE5_THICKET_CUT"),
    ("RUBBLE", "OBJ_EVENT_GFX_BREAKABLE_ROCK", LOOKOUT_X, B_ROWS[0] + 1, "EventScript_RockSmash",
     "FLAG_ICHOR_ROUTE5_RUBBLE_BROKEN"),
]
# Visible items: (item, x, y, flag)
ITEMS = [
    ("ITEM_SUPER_POTION", 19, 4, "FLAG_ICHOR_ITEM_ROUTE5_SUPER_POTION"),
    ("ITEM_GREAT_BALL", SEAT[0] + 2, 11, "FLAG_ICHOR_ITEM_ROUTE5_GREAT_BALL"),
    ("ITEM_PP_UP", 29, 3, "FLAG_ICHOR_ITEM_ROUTE5_PP_UP"),
    ("ITEM_CALCIUM", 42, 4, "FLAG_ICHOR_ITEM_ROUTE5_CALCIUM"),
    ("ITEM_SUPER_REPEL", 58, 3, "FLAG_ICHOR_ITEM_ROUTE5_SUPER_REPEL"),
    ("ITEM_REVIVE", B_X[0], B_ROWS[0], "FLAG_ICHOR_ITEM_ROUTE5_REVIVE"),
]
# Hidden items: (item, x, y, flag)
HIDDEN = [
    ("ITEM_HONEY", 57, 5, "FLAG_ICHOR_HIDDEN_ROUTE5_HONEY"),              # under a hive
    ("ITEM_PRETTY_FEATHER", NICHES[0] + 2, NICHES[1] + 2, "FLAG_ICHOR_HIDDEN_ROUTE5_PRETTY_FEATHER"),
    ("ITEM_HEART_SCALE", POINT[0], 25, "FLAG_ICHOR_HIDDEN_ROUTE5_HEART_SCALE"),   # the point's tip
    ("ITEM_ORAN_BERRY", 59, 19, "FLAG_ICHOR_HIDDEN_ROUTE5_ORAN_BERRY"),  # the inn's yard
]
# Signs and things to read: (x, y, facing, script)
SIGNS = [
    (8, 9, "ANY", "MouthSign"),
    (47, 8, "ANY", "MeadowSign"),
    (57, 24, "ANY", "EastSign"),
    (SEAT[0], SEAT[1], "ANY", "Seat"),
    (SEAT[0] + 1, SEAT[1], "ANY", "Seat"),
    (TOWER[0], TOWER[1] + 3, "ANY", "Watchtower"),
    (NICHES[0], NICHES[1] + 2, "NORTH", "Niches"),
    (55, 3, "ANY", "Hives"),
    (56, 3, "ANY", "Hives"),
    (INN_AT[0] + 1, INN_AT[1] + 3, "NORTH", "InnSign"),
]
ALTAR = (NICHES[0] + 1, NICHES[1] + 2)         # Aphrodite's altar stone, under the goddess's niche
HERM_EVENT = HERM_AT
DIG = [(52, 6)]                                # ICHOR_STUB_DIG: the meadow's daily dig spot


def dest_hollow():
    groups = (ROOT / "data/maps/map_groups.json").read_text()
    if '"HecatesHollow"' in groups or HOLLOW_MAP in "".join(
            p.read_text() for p in (ROOT / "data/maps").glob("HecatesHollow*/map.json")):
        return HOLLOW_MAP, HOLLOW_WARP_ID
    return "MAP_EMPORION_CITY", 0


def warps():
    """(x, y, map, warp id), in warp-id order: 0 the Hollow's mouth, 1 the inn door."""
    dmap, did = dest_hollow()
    ix, iy = INN_AT
    return [(MOUTH[0], MOUTH[1], dmap, did),
            (ix + INN_DOOR[0], iy + INN_DOOR[1], "MAP_ROUTE5_REST_HOUSE", 0)]


def write_events(g):
    m = json.loads((MAP_DIR / "map.json").read_text())
    m["music"] = "MUS_ICHOR_ROAD"
    m["weather"] = "WEATHER_SUNNY"
    m["map_type"] = "MAP_TYPE_ROUTE"
    m["show_map_name"] = True
    m["connections"] = [{"map": "MAP_ELEUSA_VILLAGE", "offset": ELEUSA_OFFSET, "direction": "right"}]
    objs = []
    for lid, gfx, x, y, facing, sight, script, trainer in TRAINERS:
        objs.append({
            "local_id": f"LOCALID_ROUTE5_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL", "trainer_sight_or_berry_tree_id": str(sight),
            "script": PX + script, "flag": "0"})
    for lid, gfx, x, y, facing, script, flag in PEOPLE:
        objs.append({
            "local_id": f"LOCALID_ROUTE5_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
            "script": PX + script, "flag": flag})
    for lid, gfx, x, y, script, flag in OBSTACLES:
        objs.append({
            "local_id": f"LOCALID_ROUTE5_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND" if False else "MOVEMENT_TYPE_NONE",
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
            "script": script, "flag": flag})
    for item, x, y, flag in ITEMS:
        objs.append({
            "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": item,
            "script": "Common_EventScript_FindItem", "flag": flag})
    m["object_events"] = objs
    m["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": d, "dest_warp_id": str(i)}
                        for x, y, d, i in warps()]
    m["coord_events"] = []
    bgs = [{"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": PX + s} for x, y, f, s in SIGNS]
    bgs.append({"type": "sign", "x": ALTAR[0], "y": ALTAR[1], "elevation": 0,
                "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": "EventScript_IchorAltar_Aphrodite"})
    bgs.append({"type": "sign", "x": HERM_EVENT[0], "y": HERM_EVENT[1], "elevation": 0,
                "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": "EventScript_IchorGreatHerm"})
    bgs += [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
             "script": PX + "DigSpot"} for x, y in DIG]
    bgs += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
             "quantity": 1, "underfoot": False} for item, x, y, flag in HIDDEN]
    m["bg_events"] = bgs
    (MAP_DIR / "map.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def blockdata(g):
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            mid = int(g.mt[y, x]) & 0x3FF
            if g.solid[y, x]:
                out[y, x] = mid | (1 << 10)
            elif g.water[y, x]:
                out[y, x] = mid | (1 << 12)
            else:
                out[y, x] = mid | (3 << 12)
    return out


def border(g):
    """The mountain's pines past the top and west edges (the camera never sees
    past the bottom: the lowest walkable row is 25, six rows above it)."""
    s = g.cat["pine_tall"]
    return np.array([s["ids"][1][0], s["ids"][1][1], s["ids"][2][0], s["ids"][2][1]], np.uint16) | (1 << 10)


def write_layout(g):
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    blockdata(g).astype("<u2").tofile(LAYOUT_DIR / "map.bin")
    border(g).astype("<u2").tofile(LAYOUT_DIR / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    for l in data["layouts"]:
        if l.get("id") == LAYOUT_ID and (l["width"], l["height"], l["primary_tileset"], l["secondary_tileset"]) != \
                (W, H, "gTileset_Aethos", "gTileset_Skiron"):
            l["width"], l["height"] = W, H
            l["primary_tileset"], l["secondary_tileset"] = "gTileset_Aethos", "gTileset_Skiron"
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def reach_from(g, start, blocked=frozenset(), avoid=None):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if not (0 <= p[0] < W and 0 <= p[1] < H) or p in seen or p in blocked:
                continue
            if g.solid[p[1], p[0]] or g.water[p[1], p[0]]:
                continue
            if avoid and avoid(*p):
                continue
            seen.add(p)
            q.append(p)
    return seen


def sight_cells(t):
    lid, gfx, x, y, facing, sight, *_ = t
    d = {"LEFT": (-1, 0), "RIGHT": (1, 0), "UP": (0, -1), "DOWN": (0, 1)}[facing]
    return {(x + d[0] * k, y + d[1] * k) for k in range(1, sight + 1)}


def check(g):
    problems = []
    m = json.loads((MAP_DIR / "map.json").read_text())
    start = (MOUTH[0], MOUTH[1] + 1)
    gates = {(o["x"], o["y"]) for o in m["object_events"]
             if o["graphics_id"] in ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "OBJ_EVENT_GFX_CUTTABLE_TREE",
                                     "OBJ_EVENT_GFX_BREAKABLE_ROCK")}
    people = {(o["x"], o["y"]) for o in m["object_events"]} - gates
    reach = reach_from(g, start, frozenset(gates))
    reach_all = reach_from(g, start)                     # with every relic in hand
    # the seam: open exactly on Eleusa's rows, aethos only near it
    for y in range(H):
        open_ = not g.solid[y, W - 1] and not g.water[y, W - 1]
        if open_ != (y in EAST_SEAM):
            problems.append(f"east seam: row {y} is {'open' if open_ else 'shut'}")
        for x in range(W - STRIP, W):
            if int(g.mt[y, x]) >= 0x200:
                problems.append(f"Skiron metatile 0x{int(g.mt[y, x]):03X} at ({x},{y}) in the east strip")
    for y in EAST_SEAM:
        if (W - 1, y) not in reach:
            problems.append(f"the seam at ({W - 1},{y}) can't be walked to from the mouth")
    # the west and north edges: nothing walkable near enough to show past them
    for (x, y) in reach_all:
        if x < 7:
            problems.append(f"({x},{y}) is walkable within 7 columns of the west edge (the border shows)")
    # the mouth is a door, and the inn's
    for x, y, d, i in warps():
        if behavior(int(g.mt[y, x])) not in ("MB_NON_ANIMATED_DOOR", "MB_ANIMATED_DOOR"):
            problems.append(f"warp ({x},{y}) to {d} is on {behavior(int(g.mt[y, x]))}, not a door")
        if (x, y + 1) not in reach:
            problems.append(f"warp ({x},{y}): its doorstep is unreachable")
    # people, items and gates on open ground the player can reach
    for o in m["object_events"]:
        x, y = o["x"], o["y"]
        who = o.get("local_id") or f"{o['trainer_sight_or_berry_tree_id']}@{x},{y}"
        if g.solid[y, x]:
            problems.append(f"{who} stands on a solid cell ({x},{y})")
        r = reach_all if o["flag"] != "0" and "ITEM" in o["flag"] else reach_all
        if (x, y) not in r and not any((x + dx, y + dy) in r for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            problems.append(f"{who} at ({x},{y}) can't be reached")
    still = reach_from(g, start, frozenset(people | gates))
    still_all = reach_from(g, start, frozenset(people))
    for o in m["object_events"]:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in still_all for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            problems.append(f"{o.get('local_id', o['graphics_id'])} at ({x},{y}) can't be talked to past the others")
    for b in m["bg_events"]:
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and not g.solid[y, x] and b["script"] != PX + "DigSpot":
            problems.append(f"sign ({x},{y}) {b['script']} stands on walkable ground")
        spots = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))]
        if b.get("player_facing_dir", "").endswith("NORTH"):
            spots = [(x, y + 1)]
        if not any(s in still_all for s in spots):
            problems.append(f"bg event ({x},{y}) {b.get('script', b.get('item'))} can't be read from anywhere")
    # nothing walkable cut off from the mouth (with every relic)
    pockets = [(x, y) for y in range(H) for x in range(W)
               if not g.solid[y, x] and not g.water[y, x] and (x, y) not in reach_all]
    if pockets:
        problems.append(f"walkable but cut off: {pockets[:12]}{' …' if len(pockets) > 12 else ''}")
    # the forced bands: no way from the mouth to Eleusa without tall grass
    goal = (W - 1, EAST_SEAM[1])
    is_tall = lambda x, y: behavior(int(g.mt[y, x])) == "MB_TALL_GRASS"
    if goal in reach_from(g, start, frozenset(gates), avoid=is_tall):
        problems.append("the road to Eleusa can be walked without crossing tall grass")
    for name, cols, rows in (("band 1", BAND1, A_ROWS), ("band 2", BAND2, B_ROWS), ("band 3", BAND3, C_ROWS)):
        road = {(x, y) for x in range(cols[0], cols[1] + 1) for y in range(rows[0], rows[1] + 1)}
        band = {(x, y) for x in range(cols[0], cols[1] + 1) for y in range(H) if is_tall(x, y)}
        if goal in reach_from(g, start, frozenset(gates), avoid=lambda x, y, b=band: (x, y) in b):
            problems.append(f"{name} can be walked round")
        if not all(is_tall(x, y) for x, y in road):
            problems.append(f"{name} has cells that aren't tall grass")
    # mandatory trainers: their sight lines cut the road
    for t in TRAINERS:
        if t[0] in ("KYNEGEIROS", "MOPSOS"):
            cells = sight_cells(t)
            if goal in reach_from(g, start, frozenset(gates | people), avoid=lambda x, y, c=cells: (x, y) in c):
                problems.append(f"{t[0]}'s sight can be walked round")
    # a trainer who spots the player walks up and stays there: he must never end
    # up standing in the only way on
    for t in TRAINERS:
        lid, gfx, x, y, facing, sight, *_ = t
        d = {"LEFT": (-1, 0), "RIGHT": (1, 0), "UP": (0, -1), "DOWN": (0, 1)}[facing]
        for k in range(1, sight):
            stop = (x + d[0] * k, y + d[1] * k)
            others = frozenset((gates | people | {stop}) - {(x, y)})
            if goal not in reach_from(g, start, others):
                problems.append(f"{lid} could stop at {stop} after spotting the player and block the road")
    if g.missing:
        problems.append(f"tall-grass shapes Skiron lacks (drawn plain): {sorted(g.missing)}")
    return problems, reach_all


def walk_text(g, reach):
    rows = ["    " + "".join(str(x % 10) for x in range(W))]
    for y in range(H):
        line = ""
        for x in range(W):
            if g.water[y, x]:
                line += "~"
            elif g.solid[y, x]:
                line += "#"
            elif (x, y) not in reach:
                line += "?"
            elif behavior(int(g.mt[y, x])) == "MB_TALL_GRASS":
                line += ","
            else:
                line += "."
        rows.append(f"{y:3d} {line}")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

def renderer():
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R, R.Renderer(R.Tileset(R.resolve_tileset("gTileset_Aethos", syms)),
                         R.Tileset(R.resolve_tileset("gTileset_Skiron", syms)))


FRAME = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}


def sprite(gfx, facing):
    from PIL import Image
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
        name = gfx[len("OBJ_EVENT_GFX_SPECIES("):-1]
        stub = (ROOT / "include/constants/ichor_species_stubs.h").read_text()
        mm = re.search(rf"SPECIES_{name}\s+SPECIES_(\w+)", stub)
        sp = (mm.group(1) if mm else name).lower()
        sheet = Image.open(ROOT / f"graphics/pokemon/{sp}/overworld.png")
        fw = sheet.height
    elif gfx == "OBJ_EVENT_GFX_ITEM_BALL":
        sheet = Image.open(ROOT / "graphics/object_events/pics/misc/item_ball.png")
        fw = 16
    elif gfx in ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "OBJ_EVENT_GFX_CUTTABLE_TREE", "OBJ_EVENT_GFX_BREAKABLE_ROCK"):
        sheet = Image.open(ROOT / f"graphics/object_events/pics/misc/{gfx[len('OBJ_EVENT_GFX_'):].lower()}.png")
        fw = 16
        facing = "DOWN"
    elif gfx.startswith(GFX + "UPTURNED_BOAT"):
        sheet = Image.open(ROOT / f"graphics/object_events/pics/misc/ichor/{gfx[len(GFX):].lower()}.png")
        fw = sheet.width
    elif gfx.startswith(GFX):
        sheet = Image.open(ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png")
        fw = 16
    else:
        raise FileNotFoundError(gfx)
    frame = 0 if gfx == "OBJ_EVENT_GFX_ITEM_BALL" else FRAME[facing]
    fh = sheet.height
    crop = sheet.crop((frame * fw, 0, frame * fw + fw, fh))
    spr = crop.convert("RGBA")
    if sheet.mode == "P":
        idx, px = crop.load(), spr.load()
        for j in range(fh):
            for i in range(fw):
                if idx[i, j] == 0:
                    px[i, j] = (0, 0, 0, 0)
    if facing == "RIGHT":
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    return spr, fw, fh


def people(im, pad=0):
    ents = [(gfx, x, y, f) for _, gfx, x, y, f, *_ in TRAINERS] + \
           [(gfx, x, y, f) for _, gfx, x, y, f, *_ in PEOPLE] + \
           [(gfx, x, y, "DOWN") for _, gfx, x, y, *_ in OBSTACLES] + \
           [("OBJ_EVENT_GFX_ITEM_BALL", x, y, "DOWN") for _, x, y, _ in ITEMS]
    for gfx, x, y, facing in ents:
        try:
            spr, fw, fh = sprite(gfx, facing)
        except FileNotFoundError:
            continue
        im.paste(spr, ((x + pad) * 16 + 8 - fw // 2, (y + pad) * 16 + 16 - fh), spr)
    return im


# Where the player stands for each 15x10 review view, along the road.
VIEWS = [
    ("01_mouth", 10, 10), ("02_clearing", 17, 7), ("03_seat", 25, 9), ("04_knoll", 31, 6),
    ("05_hollow", 40, 9), ("06_fork", 47, 10), ("07_meadow", 54, 6), ("08_cutting", 46, 15),
    ("09_niches", 40, 16), ("10_stair", 38, 20), ("11_point", 37, 23), ("12_fisher", 42, 23),
    ("13_band3", 48, 22), ("14_inn", 54, 22), ("15_east", 62, 22),
]


def render(out_dir, g):
    from PIL import Image, ImageDraw
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    R, r = renderer()
    blocks = np.fromfile(LAYOUT_DIR / "map.bin", "<u2")
    flat = R.render_blocks(r, blocks, W)
    whole = people(flat.convert("RGBA"))
    whole.convert("RGB").resize((W * 32, H * 32), Image.NEAREST).save(out_dir / "route5.png")
    m = json.loads((MAP_DIR / "map.json").read_text())
    im = flat.convert("RGBA").resize((W * 32, H * 32), Image.NEAREST)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = 32
    for y in range(H):
        for x in range(W):
            if blocks[y * W + x] >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif behavior(int(blocks[y * W + x]) & 0x3FF) == "MB_TALL_GRASS":
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 255, 0, 50))
    for t in TRAINERS:
        for (sx, sy) in sight_cells(t):
            d.rectangle([sx * c + 6, sy * c + 6, sx * c + c - 7, sy * c + c - 7], outline=(255, 160, 0, 255), width=2)
    for o in m["object_events"]:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5],
                  outline=(255, 255, 0, 255), width=3)
    for w_ in m["warp_events"]:
        d.rectangle([w_["x"] * c + 3, w_["y"] * c + 3, w_["x"] * c + c - 4, w_["y"] * c + c - 4],
                    outline=(0, 255, 255, 255), width=3)
    for b in m["bg_events"]:
        col = (255, 120, 255, 255) if b["type"] == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 4, b["y"] * c + 4, b["x"] * c + c - 5, b["y"] * c + c - 5], fill=col, width=3)
        d.line([b["x"] * c + c - 5, b["y"] * c + 4, b["x"] * c + 4, b["y"] * c + c - 5], fill=col, width=3)
    Image.alpha_composite(im, ov).convert("RGB").save(out_dir / "route5_walk.png")
    # GBA screen views, with the border past the edges and Eleusa past the seam
    pad = 8
    bw, bh = W + 2 * pad, H + 2 * pad
    bord = border(g)
    big = np.zeros((bh, bw), np.uint16)
    for y in range(bh):
        for x in range(bw):
            big[y, x] = bord[((x - pad) % 2) + 2 * ((y - pad) % 2)]
    big[pad:pad + H, pad:pad + W] = blocks.reshape(H, W)
    # Eleusa's west columns across the seam (they're aethos only, so they draw right here)
    try:
        lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
        el = next(l for l in lay["layouts"] if l.get("id") == "LAYOUT_ELEUSA_VILLAGE")
        eb = np.fromfile(ROOT / el["blockdata_filepath"], "<u2").reshape(el["height"], el["width"])
        for y in range(bh):
            ey = y - pad - ELEUSA_OFFSET
            if 0 <= ey < el["height"]:
                big[y, pad + W:] = eb[ey, :pad]
    except (StopIteration, FileNotFoundError):
        pass
    padded = people(R.render_blocks(r, big.reshape(-1), bw).convert("RGBA"), pad).convert("RGB")
    views = []
    for name, px, py in VIEWS:
        x0, y0 = (px - 7 + pad) * 16, (py - 4 + pad) * 16 - 8
        v = padded.crop((x0, y0, x0 + 240, y0 + 160))
        v.resize((480, 320), Image.NEAREST).save(out_dir / f"view_{name}.png")
        views.append((name, v))
    cols = 3
    rows = (len(views) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 248 + 8, rows * 178 + 8), (24, 24, 32))
    sd = ImageDraw.Draw(sheet)
    for i, (name, v) in enumerate(views):
        x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
        sheet.paste(v, (x, y + 10))
        sd.text((x, y - 2), name, fill=(230, 230, 200))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / "route5_views.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    g = compose()
    write_layout(g)
    write_events(g)
    problems, reach = check(g)
    if args.walk:
        print(walk_text(g, reach))
    if args.render:
        render(args.render, g)
    for p in problems:
        print("PROBLEM:", p)
    print(f"route5: {W}x{H}, {len(TRAINERS)} trainers, {len(PEOPLE)} people, {len(ITEMS)} items, "
          f"{len(HIDDEN)} hidden, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
