#!/usr/bin/env python3
"""Build Elaia Village and its four interiors.

Elaia's outdoor blockdata is composed here from aethos ground and kalliste
structures, with collision and elevation set cell by cell. The interiors copy
the finished room blockdata from design/phase1/rooms/.

  /usr/bin/python3 tools/ichor/maps/elaia.py            # write layouts and renders
  /usr/bin/python3 tools/ichor/maps/elaia.py --check    # also print the walk map

Writes:
  data/layouts/ElaiaVillage/{map,border}.bin
  data/layouts/ElaiaVillage_*/{map,border}.bin (copied rooms)
  design/phase1/img/elaia_village.png            (3x render)
  build/elaia/elaia_village_walk.png             (collision and event overlay)

Kalliste ids come from tools/ichor/art/kalliste_build.py's own packing, so they
always match the compiled tileset. Coordinates of everything the scripts care
about live in SPOTS below and in data/maps/ElaiaVillage/map.json; the --check
pass verifies that every event tile is walkable (or deliberately solid) and
reachable from the player's front door.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))

W, H = 30, 34

# ---------------------------------------------------------------------------
# aethos ids (General's numbering, repainted)
# ---------------------------------------------------------------------------
GRASS = 0x001
FLOWERS = 0x004            # red anemones (animated), walkable
SHADE = 0x01C
SIGN = 0x003               # marble stele
HERM = 0x01B               # roadside herm
SKEP = 0x0E0               # tan boulder on grass: stands in for a straw beehive
WELLHEAD = 0x1A0           # square stone with a dark shaft: stands in for the well
AWNING = [0x030, 0x031, 0x032, 0x033]   # Agora's striped awning: Halia's canopy

OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)          # bottom half with the tip of an olive below
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
CYPRESS_BOT_UNDER_TIP = (0x1F4, 0x1F5)  # cypress bottom under an olive tip (left, right)

PATH = [[0x1D0, 0x1D1, 0x1D2], [0x1D8, 0x1D9, 0x1DA], [0x1E0, 0x1E1, 0x1E2]]

PALAESTRA = [
    [0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
    [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
    [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
    [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
    [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC],
]

# ---------------------------------------------------------------------------
# kalliste ids, packed exactly as kalliste_build.py packs them
# ---------------------------------------------------------------------------


def kalliste_catalog():
    import kalliste_build as kb
    from kalliste_lib import pack
    secs = kb.sections()
    pack([(kb.SECTION_ROWS[n], ss) for n, ss in secs])
    return {s.key: s for _, ss in secs for s in ss}


K = kalliste_catalog()


def kid(key, cx, cy):
    return K[key].ids[cy][cx]


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------
WALK, SOLID = 0, 1


class Grid:
    def __init__(self):
        self.mt = np.full((H, W), GRASS, np.int32)
        self.solid = np.zeros((H, W), bool)
        self.kind = np.full((H, W), "grass", object)   # what's there, for autotiling

    def set(self, x, y, mid, solid, kind=None):
        if 0 <= x < W and 0 <= y < H:
            self.mt[y, x] = mid
            self.solid[y, x] = solid
            if kind:
                self.kind[y, x] = kind

    def struct(self, key, x, y, cx=0, cy=0, w=None, h=None, door_solid=True):
        """Place a kalliste structure (or a sub-rectangle) with its top-left at (x, y).

        The catalog's walk grid sets collision: X solid; . T J D walkable. A door
        (D) is solid when door_solid, for houses nobody can enter.
        """
        s = K[key]
        w = s.w - cx if w is None else w
        h = s.h - cy if h is None else h
        for j in range(h):
            for i in range(w):
                code = s.walk[cy + j][cx + i]
                if code == "-":
                    continue
                solid = code == "X" or (code == "D" and door_solid)
                self.set(x + i, y + j, s.ids[cy + j][cx + i], solid, key)

    def block(self, ids, x, y, solid=True, kind="building"):
        for j, row in enumerate(ids):
            for i, mid in enumerate(row):
                self.set(x + i, y + j, mid, solid, kind)

    # --- trees -------------------------------------------------------------
    def olive(self, x, y, tip=True):
        """A 2x2 olive with its top-left at (x, y); its crown tip goes in row y-1."""
        for i in range(2):
            self.set(x + i, y, OLIVE_TOP[i], SOLID, "olive_top")
            self.set(x + i, y + 1, OLIVE_BOT[i], SOLID, "olive_bot")
        if not tip or y == 0:
            return
        for i in range(2):
            k = self.kind[y - 1, x + i]
            if k == "olive_bot":
                self.mt[y - 1, x + i] = OLIVE_BOT_TIP[i]
            elif k == "cypress_bot":
                self.mt[y - 1, x + i] = CYPRESS_BOT_UNDER_TIP[i]
            elif k in ("grass", "tip", "bed"):
                self.set(x + i, y - 1, OLIVE_TIP_GRASS[i], self.solid[y - 1, x + i] or y == 1, "tip")

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, SOLID, "cypress_top")
        self.set(x, y + 1, CYPRESS_BOT, SOLID, "cypress_bot")

    # --- ground ------------------------------------------------------------
    def fill_kind(self, x0, y0, x1, y1, kind):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.kind[y, x] = kind
                self.solid[y, x] = False

    def autotile(self, kind, pieces, plain_alts=(), also=()):
        """Give every cell of `kind` its 9-slice piece from its four neighbours.

        Cells whose kind is in `also` count as the same ground (pieces that carry
        their own paving, like the garland posts) but keep their metatile.
        """
        def same(x, y):
            return 0 <= x < W and 0 <= y < H and self.kind[y, x] in (kind,) + tuple(also)
        for y in range(H):
            for x in range(W):
                if self.kind[y, x] != kind:
                    continue
                n, s, w, e = same(x, y - 1) or y == 0, same(x, y + 1) or y == H - 1, same(x - 1, y), same(x + 1, y)
                cy = 0 if not n else 2 if not s else 1
                cx = 0 if not w else 2 if not e else 1
                mid = pieces[cy][cx]
                if (cx, cy) == (1, 1) and plain_alts and (x * 7 + y * 3) % 5 == 0:
                    mid = plain_alts[(x + y) % len(plain_alts)]
                self.mt[y, x] = mid


PAVING = [[kid("paving", 0, 0), kid("paving", 1, 0), kid("paving", 2, 0)],
          [kid("paving", 0, 1), kid("paving", 3, 0), kid("paving", 2, 1)],
          [kid("paving", 0, 2), kid("paving", 1, 2), kid("paving", 2, 2)]]
PAVING_ALTS = [kid("paving", 1, 1), kid("paving", 3, 1), kid("paving", 3, 2)]
PAVE_PLAIN = kid("paving", 3, 0)
PAVE_LIKE = ("posts", "altar_square", "well", "stall", "tripod")


# ---------------------------------------------------------------------------
# Composition
#
# Elaia sits on a hillside. The road from Route 1 drops in from the north
# between cypresses. The upper village (the player's house with Melitta's
# hives behind it, Kydippe's house, the blue-domed shrine up on its own
# terrace) looks down on the festival square, where the old olive and Halia's
# striped canopy are the centre of everything. The square is a terrace: its
# retaining wall has two flights of steps, one down a cypress lane to the
# Akademia in its laurel grove (south-west), one through the garland arch of
# the footrace finish into the terraced olive groves (south-east), where the
# course winds down to its starting stele.
# ---------------------------------------------------------------------------
SPOTS = {
    "door_player": (4, 10),
    "door_kydippe": (17, 7),
    "door_akademia": (5, 29),
    "halia": (14, 17),
    "line": [(14, 18), (14, 19), (14, 20)],   # Korinna, Philon, the player
    "kleon": (14, 19),
}

GARDEN = [[0x103, 0x104, 0x105], [0x113, 0x114, 0x115]]
STALL3 = [[0x028, 0x029, 0x02B], [0x030, 0x031, 0x033]]  # a festival stall: tile roof, awning
TRIPOD = (0x130, 0x131)                                  # bronze tripod on a marble plinth
PINE = [[0x01E, 0x01F], [0x026, 0x027]]                  # stone pine
LOW_WALL = (0x148, 0x149, 0x14A)                         # aethos low field wall: W end, run, E end


def noise(x, y, salt=0):
    """Deterministic 0..99 per cell, for sprinkling ground variety."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    return (h ^ (h >> 13)) % 100


def compose():
    g = Grid()

    # ---------------- ground plan: paths and paving ----------------
    g.fill_kind(10, 0, 13, 10, "path")            # the road from Route 1 (seam x 10-13)
    g.fill_kind(14, 8, 18, 9, "path")             # Kydippe's lane
    g.set(8, 7, FLOWERS, WALK, "flowers")
    g.set(9, 8, FLOWERS, WALK, "flowers")
    g.fill_kind(3, 11, 9, 12, "path")             # the player's front path
    g.fill_kind(2, 16, 6, 17, "path")             # the neighbour's yard, onto the square
    # the square: an irregular paved terrace, with a bay for the well
    g.fill_kind(10, 11, 19, 11, "pave")
    g.fill_kind(7, 12, 22, 22, "pave")
    g.fill_kind(8, 23, 21, 23, "pave")
    g.fill_kind(23, 15, 24, 18, "pave")
    g.fill_kind(24, 14, 28, 15, "pave")           # the press yard: a paved threshing floor

    # ---------------- the north band: trees two and three deep ----------------
    for x in (0, 4):
        g.olive(x, 0)
    for x in (2, 6):
        g.olive(x, 1)
    g.cypress(9, 0)
    g.cypress(8, 1)
    g.cypress(14, 0)
    g.cypress(15, 1)
    for x in (16, 20, 24, 28):
        g.olive(x, 0)
    for x in (18, 22, 26):
        g.olive(x, 1)
    g.set(9, 3, HERM, SOLID, "herm")              # road-pillar of Hermes at the gate
    g.set(14, 4, SIGN, SOLID, "sign")             # ELAIA VILLAGE
    g.set(15, 3, FLOWERS, WALK, "flowers")
    g.set(14, 3, FLOWERS, WALK, "flowers")

    # ---------------- the player's house and Melitta's hives ----------------
    g.cypress(0, 2)
    g.olive(0, 4)
    g.cypress(1, 6)
    g.cypress(0, 7)
    g.olive(0, 9)
    g.struct("house_large", 3, 6, door_solid=False)      # door (4,10)
    for x in (2, 4, 6):                                  # three skeps among anemones
        g.set(x, 4, SKEP, SOLID, "skep")
    for x, y in ((3, 4), (5, 4), (7, 4), (2, 3), (3, 3), (6, 3), (7, 3)):
        g.set(x, y, FLOWERS, WALK, "flowers")
    g.set(2, 11, FLOWERS, WALK, "flowers")
    g.set(2, 12, FLOWERS, WALK, "flowers")

    # ---------------- Kydippe's house ----------------
    g.struct("house_small", 16, 5, door_solid=False)     # door (17,7)
    garden(g, 20, 6, 3)                                  # her herb garden
    g.set(19, 7, FLOWERS, WALK, "flowers")
    g.set(19, 4, FLOWERS, WALK, "flowers")

    # ---------------- the shrine on its terrace ----------------
    g.struct("shrine_dome", 23, 3)                       # door (25,7), shut today
    g.fill_kind(22, 8, 28, 8, "pave")                    # its forecourt
    terrace_wall(g, 21, 29, 9, steps=(25,))
    g.cypress(22, 5)
    g.cypress(28, 3)
    g.cypress(29, 5)
    g.cypress(28, 6)
    g.set(22, 4, FLOWERS, WALK, "flowers")

    # ---------------- the square ----------------
    for y in range(13, 16):                              # the old olive's bed
        for x in range(13, 17):
            g.set(x, y, GRASS, SOLID, "bed")
    g.olive(14, 14)
    for x, y in ((13, 14), (13, 15), (16, 14), (16, 15)):
        g.set(x, y, FLOWERS, SOLID, "bed")
    for i, mid in enumerate(AWNING):                     # Halia's striped canopy
        g.set(13 + i, 16, mid, SOLID, "canopy")
    strand(g, 8, 13, 5)                                  # Klotheia garlands
    strand(g, 17, 13, 5)
    g.struct("altar_square", 8, 18)                      # the festival altar
    g.block(STALL3, 19, 17, kind="stall")                # a honey-cake stall
    g.set(24, 16, WELLHEAD, SOLID, "well")               # the well in its bay
    for x, y in ((7, 12), (22, 12), (7, 22), (22, 22)):
        g.set(x, y, FLOWERS, SOLID, "planter")

    # ---------------- west: a neighbour's house and garden ----------------
    g.struct("house_small", 2, 13)                       # nobody home: door (3,15) shut
    g.olive(0, 12)
    g.cypress(6, 13)
    garden(g, 2, 19, 4)
    low_wall(g, 1, 6, 21)                                # the garden's wall
    g.set(1, 19, FLOWERS, WALK, "flowers")
    g.set(1, 20, FLOWERS, WALK, "flowers")
    g.set(6, 19, FLOWERS, WALK, "flowers")
    g.olive(0, 16)

    # ---------------- east: the olive press and its orchard ----------------
    g.struct("olive_press", 25, 11)                      # front row y=13
    g.set(24, 13, FLOWERS, WALK, "flowers")
    g.olive(28, 11)
    g.olive(26, 17)
    g.olive(28, 16)
    g.cypress(29, 13)
    g.olive(25, 20)
    g.olive(28, 19)
    g.olive(23, 21)
    g.cypress(27, 21)

    # ---------------- the retaining wall, the Akademia, the groves ----------------
    terrace_wall(g, 7, 22, 24, steps=(9, 10, 18, 19))
    finish_arch(g, 17, 22)                               # the footrace finishes here
    hedge_west(g)
    hedge_east(g)
    akademia(g)
    groves(g)

    g.autotile("path", PATH)
    g.autotile("pave", PAVING, PAVING_ALTS, also=PAVE_LIKE)
    sprinkle(g)
    seal_pockets(g)
    return g


def seal_pockets(g):
    """Grass that nobody can reach (gaps between trees, the top row) becomes
    solid, so the edges are unambiguous and nothing can spawn in a hole."""
    start = (SPOTS["door_player"][0], SPOTS["door_player"][1] + 1)
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and not g.solid[ny, nx]:
                seen.add((nx, ny))
                q.append((nx, ny))
    for y in range(H):
        for x in range(W):
            if not g.solid[y, x] and (x, y) not in seen:
                g.solid[y, x] = True
    for x in range(W):
        if not 10 <= x <= 13:
            g.solid[0, x] = True


def hedge_west(g):
    """Between the west gardens and the Akademia grove: laurels two deep."""
    g.olive(0, 22)
    g.cypress(2, 22)
    g.olive(3, 23)
    g.cypress(5, 22)
    g.cypress(6, 23)
    g.set(2, 24, FLOWERS, SOLID, "flowers")


def hedge_east(g):
    """Between the press orchard and the south-east groves."""
    g.cypress(23, 23)
    g.olive(24, 24)
    g.olive(26, 23)
    g.cypress(28, 23)
    g.cypress(29, 24)


def terrace_wall(g, x0, x1, y, steps=()):
    """A kalliste retaining wall across row y, lower ground to the south."""
    for x in range(x0, x1 + 1):
        if x in steps:
            g.set(x, y, kid("terrace", 3, 0), WALK, "steps")
        elif x == x0 or (x - 1) in steps:
            g.set(x, y, kid("terrace", 0, 0), SOLID, "terrace")
        elif x == x1 or (x + 1) in steps:
            g.set(x, y, kid("terrace", 4, 0), SOLID, "terrace")
        else:
            g.set(x, y, kid("terrace", 1 + (x % 2), 0), SOLID, "terrace")


def low_wall(g, x0, x1, y):
    for x in range(x0, x1 + 1):
        mid = LOW_WALL[0] if x == x0 else LOW_WALL[2] if x == x1 else LOW_WALL[1]
        g.set(x, y, mid, SOLID, "lowwall")


def akademia(g):
    """The Akademia: a palaestra in a laurel grove, down a cypress lane."""
    g.fill_kind(9, 25, 10, 29, "path")                   # the lane from the steps
    g.fill_kind(3, 30, 10, 31, "pave")                   # its paved forecourt
    g.block(PALAESTRA, 2, 25)
    g.solid[29, 5] = True                                # animated door: warp on facing it
    for y in (25, 27):
        g.cypress(8, y)
        g.cypress(11, y)
    g.cypress(11, 29)
    g.olive(0, 26)
    g.cypress(0, 28)
    g.cypress(1, 29)
    g.block([[TRIPOD[0]], [TRIPOD[1]]], 3, 30, kind="tripod")   # a bronze dedication
    g.set(8, 29, SIGN, SOLID, "sign")                    # THE AKADEMIA, by the lane
    g.set(2, 31, FLOWERS, WALK, "flowers")
    south_band(g, 0, 12)


def south_band(g, x0, x1):
    """The southern edge: olives on the last two rows, cypresses in the gaps,
    and an olive stepped forward wherever the row above is free, so the edge
    reads as a grove two deep rather than a fence of identical trees."""
    prev = None
    for x in range(x0, x1, 2):
        free = all(g.kind[H - 3, x + i] == "grass" and not g.solid[H - 3, x + i] for i in (0, 1))
        options = ["olive", "cypress", "forward"] if free else ["olive", "cypress"]
        choice = options[noise(x, 0, 7) % len(options)]
        if choice == prev:
            choice = options[(options.index(choice) + 1) % len(options)]
        prev = choice
        if choice == "olive":
            g.olive(x, H - 2)
        elif choice == "cypress":
            g.cypress(x + noise(x, 1, 7) % 2, H - 2)
            other = x + 1 - noise(x, 1, 7) % 2
            g.set(other, H - 2, FLOWERS if noise(x, 2, 7) < 40 else GRASS, SOLID, "edge")
            g.set(other, H - 1, GRASS, SOLID, "edge")
        else:                                            # stepped forward a row
            g.olive(x, H - 3)
            for i in (0, 1):
                g.set(x + i, H - 1, GRASS, SOLID, "edge")


def groves(g):
    """South-east: terraced olive groves and the winding race course."""
    # the course, down the steps and winding east to the starting stele
    g.fill_kind(18, 25, 19, 27, "path")
    g.fill_kind(18, 27, 22, 28, "path")
    g.fill_kind(21, 28, 22, 30, "path")
    g.fill_kind(21, 30, 27, 31, "path")
    g.set(28, 30, SIGN, SOLID, "sign")                   # the starting stele
    g.set(29, 31, FLOWERS, WALK, "flowers")
    g.set(28, 31, FLOWERS, WALK, "flowers")
    # olives in offset rows, as they were planted
    for x, y in ((12, 25), (15, 26), (12, 28), (15, 29), (24, 26), (27, 26),
                 (26, 28), (17, 30)):
        g.olive(x, y)
    g.cypress(23, 28)
    g.olive(12, 30)                                      # closes the grove off from the Akademia's
    g.cypress(20, 25)
    south_band(g, 12, W)


def sprinkle(g):
    """A few anemones in the meadows; nowhere near enough to look like a pattern."""
    for y in range(H):
        for x in range(W):
            if g.kind[y, x] == "grass" and not g.solid[y, x] and g.mt[y, x] == GRASS and noise(x, y, 2) < 4:
                g.mt[y, x] = FLOWERS


def garden(g, x, y, w):
    """A two-row kitchen garden of tilled earth (no berry-soil centre pieces)."""
    for j in range(2):
        for i in range(w):
            col = 0 if i == 0 else 2 if i == w - 1 else 1
            g.set(x + i, y + j, GARDEN[j][col], SOLID, "garden")


def strand(g, x, y, n):
    """Klotheia garland posts: n cells wide from x, post tops in row y, bases in y+1."""
    for i in range(n):
        if i % 2 == 0:
            if i == 0:
                top = kid("klotheia_posts", 3, 0)        # garland right only
            elif i == n - 1:
                top = kid("klotheia_posts", 2, 0)        # garland left only
            else:
                top = kid("klotheia_posts", 0, 0)        # both sides
            g.set(x + i, y, top, WALK, "posts")
            g.set(x + i, y + 1, kid("klotheia_posts", 0, 1), SOLID, "posts")
        else:
            g.set(x + i, y, kid("klotheia_posts", 1, 0), WALK, "posts")
            g.set(x + i, y + 1, kid("klotheia_posts", 1, 1), WALK, "posts")


def finish_arch(g, x, y):
    """Two garlanded posts over the footrace course: the finish line."""
    g.set(x, y, kid("klotheia_posts", 3, 0), WALK, "posts")
    g.set(x + 1, y, kid("klotheia_posts", 1, 0), WALK, "posts")
    g.set(x + 2, y, kid("klotheia_posts", 1, 0), WALK, "posts")
    g.set(x + 3, y, kid("klotheia_posts", 2, 0), WALK, "posts")
    g.set(x, y + 1, kid("klotheia_posts", 0, 1), SOLID, "posts")
    g.set(x + 1, y + 1, kid("klotheia_posts", 1, 1), WALK, "posts")
    g.set(x + 2, y + 1, kid("klotheia_posts", 3, 1), WALK, "posts")
    g.set(x + 3, y + 1, kid("klotheia_posts", 2, 1), SOLID, "posts")



# ---------------------------------------------------------------------------
# Events: data/maps/ElaiaVillage/map.json's object, warp, coord and bg events.
# scripts.pory moves people around in the cutscenes; its coordinates follow
# these (see the comments there).
# ---------------------------------------------------------------------------
GFX = "OBJ_EVENT_GFX_ICHOR_"
OBJECTS = [
    # local id, gfx, x, y, facing, script, hide flag
    ("HALIA", GFX + "PRIESTESS", 14, 17, "DOWN", "Halia", "0"),
    ("KORINNA", GFX + "YOUTH_F", 14, 18, "UP", "Korinna", "0"),
    ("PHILON", GFX + "YOUTH_M", 14, 19, "UP", "Philon", "0"),
    ("GYLIPPOS", GFX + "ELDER_M", 7, 16, "RIGHT", "Gylippos", "0"),
    ("WOMAN", GFX + "WOMAN", 10, 16, "UP", "FestivalWoman", "0"),
    ("MAN", GFX + "MAN", 16, 23, "RIGHT", "FestivalMan", "0"),
    ("FARMER", GFX + "HARVESTER", 26, 14, "UP", "OliveFarmer", "0"),
    ("KID", GFX + "KID_M", 23, 16, "RIGHT", "Kid", "0"),
    ("WOOLOO", "OBJ_EVENT_GFX_SPECIES(WOOLOO)", 23, 17, "UP", "KidsWooloo", "0"),
    ("SHEPHERD", GFX + "SHEPHERD", 12, 1, "DOWN", "OldShepherd", "0"),
    ("KLEON", GFX + "KLEON", 14, 19, "DOWN", "Kleon", "FLAG_ICHOR_HIDE_KLEON_ELAIA"),
    ("ALETHEA", GFX + "ALETHEA", 5, 29, "DOWN", "0", "FLAG_ICHOR_HIDE_ALETHEA_ELAIA"),
]
ITEMS = [("ITEM_POTION", 24, 12, "FLAG_ICHOR_ITEM_ELAIA_POTION")]
WARPS = [   # order is the warp id; the interiors point back at these
    (17, 7, "MAP_ELAIA_VILLAGE_NEIGHBORS_HOUSE", 0),
    (4, 10, "MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F", 1),
    (5, 29, "MAP_ELAIA_VILLAGE_AKADEMIA", 0),
]
LINE_SPOT = (14, 20)                                   # the player's place in Halia's line
LINE_CORE = {(x, y) for x in range(13, 16) for y in range(17, 21)}
AKADEMIA_STEPS = [(9, 24), (10, 24)]                   # Kleon waits for you at the top
SIGNS = [   # x, y, facing, script
    (14, 4, "ANY", "VillageSign"),
    (3, 10, "NORTH", "PlayersHouseSign"),
    (16, 7, "NORTH", "KydippesHouseSign"),
    (8, 29, "ANY", "AkademiaSign"),
    (16, 16, "NORTH", "FestivalBanner"),
    (9, 3, "ANY", "Herm"),
    (25, 7, "NORTH", "ShrineDoor"),
    (3, 15, "NORTH", "NeighboursDoor"),
    (24, 16, "ANY", "Well"),
    (2, 4, "ANY", "Beehives"),
    (6, 4, "ANY", "Beehives"),
    (25, 13, "NORTH", "OlivePress"),
    (27, 13, "NORTH", "OlivePress"),
    (28, 30, "ANY", "RaceStart"),
    (8, 19, "NORTH", "Altar"),
    (9, 19, "NORTH", "Altar"),
    (19, 18, "NORTH", "Stall"),
    (20, 18, "NORTH", "Stall"),
    (21, 18, "NORTH", "Stall"),
]
HIDDEN = [("ITEM_HONEY", 4, 4, "FLAG_HIDDEN_ITEM_ICHOR_ELAIA_HONEY")]


def halia_ring(g):
    """Coord triggers ringing the line at Halia's canopy: walk in and she calls you."""
    out = []
    for y in range(15, 22):
        for x in range(11, 18):
            if not g.solid[y, x] and (x, y) not in LINE_CORE:
                out.append((x, y))
    return out


def write_events(g):
    path = ROOT / "data/maps/ElaiaVillage/map.json"
    m = json.loads(path.read_text())
    m["music"] = "MUS_ICHOR_ELAIA"
    objs = []
    for lid, gfx, x, y, facing, script, flag in OBJECTS:
        objs.append({
            "local_id": f"LOCALID_ELAIA_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
            "script": "0" if script == "0" else f"ElaiaVillage_EventScript_{script}", "flag": flag})
    for item, x, y, flag in ITEMS:
        objs.append({
            "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": item,
            "script": "Common_EventScript_FindItem", "flag": flag})
    m["object_events"] = objs
    m["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": d, "dest_warp_id": str(i)}
                        for x, y, d, i in WARPS]
    coords = []
    for x in range(10, 14):
        coords.append((x, 2, "FLAG_ICHOR_GOT_STARTER", "ShepherdGate"))
    for x, y in halia_ring(g):
        coords.append((x, y, "FLAG_ICHOR_THREAD_READ", "HaliaCalls"))
    for x, y in AKADEMIA_STEPS:
        coords.append((x, y, "FLAG_ICHOR_KLEON_BATTLE_1_DONE", "KleonTrigger"))
    door = SPOTS["door_akademia"]
    coords.append((door[0], door[1] + 1, "FLAG_ICHOR_THREAD_READ", "AkademiaNote"))
    m["coord_events"] = [{"type": "trigger", "x": x, "y": y, "elevation": 0, "var": flag, "var_value": "0",
                          "script": f"ElaiaVillage_EventScript_{s}"} for x, y, flag, s in coords]
    bgs = [{"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": f"ElaiaVillage_EventScript_{s}"}
           for x, y, f, s in SIGNS]
    bgs += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
             "quantity": 1, "underfoot": False} for item, x, y, flag in HIDDEN]
    m["bg_events"] = bgs
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def blockdata(g):
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            solid = bool(g.solid[y, x])
            elev = 0 if solid else 3
            out[y, x] = (g.mt[y, x] & 0x3FF) | (int(solid) << 10) | (elev << 12)
    return out


def write_layout(g):
    d = ROOT / "data/layouts/ElaiaVillage"
    blockdata(g).astype("<u2").tofile(d / "map.bin")
    border = np.array([OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]], np.uint16)
    border.astype("<u2").tofile(d / "border.bin")


ROOMS = {
    "ElaiaVillage_PlayersHouse_1F": "players_house_1f",
    "ElaiaVillage_PlayersHouse_2F": "players_house_2f",
    "ElaiaVillage_NeighborsHouse": "kydippe_house",
    "ElaiaVillage_Akademia": "elaia_akademia",
}
VOID = {"oikia": 0x0E10 | 0x0400, "civic": 0x0200 | 0x0400}


def write_rooms():
    for name, room in ROOMS.items():
        d = ROOT / "data/layouts" / name
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f"design/phase1/rooms/{room}.bin", d / "map.bin")
        void = 0x0210 if room != "elaia_akademia" else 0x0200
        np.array([void] * 4, np.uint16).astype("<u2").tofile(d / "border.bin")


def render(out, scale=3):
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "LAYOUT_ELAIA_VILLAGE",
                    "--scale", str(scale), "-o", str(out)], check=True, stdout=subprocess.DEVNULL)


# Screen-sized views along the player's route: (name, player x, y)
VIEWS = [
    ("01_front_door", 4, 11), ("02_hives", 5, 5), ("03_north_gate", 11, 4),
    ("04_kydippe", 17, 8), ("05_square_line", 14, 20), ("06_square_north", 14, 12),
    ("07_well_press", 24, 15), ("08_west", 4, 17), ("09_akademia", 6, 30),
    ("10_finish", 18, 24), ("11_race_start", 24, 30), ("12_shrine", 25, 9),
]


def screen_views(g, out_dir, scale=2):
    """Render each view as the GBA shows it: 15x10 tiles, the player at (7,5),
    the layout's border wherever the screen runs past the map."""
    pad = 8
    bw, bh = W + 2 * pad, H + 2 * pad
    big = np.zeros((bh, bw), np.uint16)
    border = [[OLIVE_TOP[0], OLIVE_TOP[1]], [OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]]]
    for y in range(bh):
        for x in range(bw):
            big[y, x] = border[(y - pad) % 2][(x - pad) % 2]
    big[pad:pad + H, pad:pad + W] = g.mt
    tmp = out_dir / "views_blockdata.bin"
    big.astype("<u2").tofile(tmp)
    whole = out_dir / "views_whole.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(bw), "--primary", "aethos", "--secondary", "kalliste", "-o", str(whole)],
                   check=True, stdout=subprocess.DEVNULL)
    from PIL import Image
    im = Image.open(whole)
    for name, px, py in VIEWS:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16
        im.crop((x0, y0, x0 + 240, y0 + 160)).resize((240 * scale, 160 * scale), Image.NEAREST).save(
            out_dir / f"view_{name}.png")


def overlay(g, src, out, events):
    """Collision (red) and event markers over a 1x render, scaled 3x."""
    from PIL import Image, ImageDraw
    im = Image.open(src).convert("RGBA")
    s = im.width // W
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(H):
        for x in range(W):
            if g.solid[y, x]:
                d.rectangle([x * s, y * s, x * s + s - 1, y * s + s - 1], fill=(255, 0, 0, 70))
    colors = {"obj": (40, 120, 255, 200), "warp": (255, 255, 0, 220), "coord": (255, 0, 255, 120),
              "bg": (0, 220, 120, 200)}
    for kind, x, y in events:
        c = colors[kind]
        pad = s // 4 if kind != "coord" else 2
        d.rectangle([x * s + pad, y * s + pad, x * s + s - 1 - pad, y * s + s - 1 - pad], outline=c, width=3)
    Image.alpha_composite(im, ov).save(out)


def map_events():
    m = json.loads((ROOT / "data/maps/ElaiaVillage/map.json").read_text())
    ev = []
    for o in m["object_events"]:
        ev.append(("obj", o["x"], o["y"]))
    for w in m["warp_events"]:
        ev.append(("warp", w["x"], w["y"]))
    for c in m["coord_events"]:
        ev.append(("coord", c["x"], c["y"]))
    for b in m["bg_events"]:
        ev.append(("bg", b["x"], b["y"]))
    return m, ev


def check(g, m):
    """Every object, coord and warp spot reachable from the player's door; seams right."""
    solid = g.solid.copy()
    start = (SPOTS["door_player"][0], SPOTS["door_player"][1] + 1)
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in seen or solid[ny, nx]:
                continue
            # a ledge is one-way: only enter it moving south
            if g.kind[ny, nx] == "ledge" and dy != 1:
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
    problems = []
    for x in range(W):
        if (10 <= x <= 13) == bool(solid[0, x]):
            problems.append(f"north seam wrong at x={x}")
    warps = {(w["x"], w["y"]) for w in m["warp_events"]}
    for o in m["object_events"]:
        if solid[o["y"], o["x"]] and (o["x"], o["y"]) not in warps:   # Alethea waits in a doorway
            problems.append(f"object {o.get('local_id', o['graphics_id'])} on a solid cell ({o['x']},{o['y']})")
    for c in m["coord_events"]:
        if (c["x"], c["y"]) not in seen:
            problems.append(f"coord ({c['x']},{c['y']}) unreachable")
    for w in m["warp_events"]:
        x, y = w["x"], w["y"]
        front = (x, y + 1)
        if front not in seen:
            problems.append(f"warp ({x},{y}) has an unreachable front")
    # gates: leaving the Akademia must cross Kleon's trigger; reaching the
    # line at the canopy must cross Halia's ring; Route 1 needs the shepherd's row
    for name, start, goal, gate in (
            ("Kleon", (5, 30), (14, 12), set(AKADEMIA_STEPS)),
            ("Halia", (4, 11), LINE_SPOT, set(halia_ring(g))),
            ("shepherd", (4, 11), (11, 0), {(x, 2) for x in range(10, 14)})):
        if reachable(g, start, goal, gate):
            problems.append(f"{name}'s trigger can be walked around")
    return problems, seen


def reachable(g, start, goal, blocked):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and not g.solid[ny, nx]
                    and (nx, ny) not in blocked):
                seen.add((nx, ny))
                q.append((nx, ny))
    return False


def walk_text(g, seen):
    rows = ["    " + "".join(str(x % 10) for x in range(W))]
    for y in range(H):
        line = ""
        for x in range(W):
            if g.solid[y, x]:
                line += "#"
            elif g.kind[y, x] == "ledge":
                line += "v"
            elif (x, y) in seen:
                line += "."
            else:
                line += "?"
        rows.append(f"{y:3d} {line}")
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="print the walk map")
    args = ap.parse_args()
    g = compose()
    write_layout(g)
    write_events(g)
    write_rooms()
    out = ROOT / "build/elaia"
    out.mkdir(parents=True, exist_ok=True)
    render(ROOT / "design/phase1/img/elaia_village.png", 3)
    render(out / "elaia_village_1x.png", 1)
    m, ev = map_events()
    from PIL import Image
    Image.open(out / "elaia_village_1x.png").resize((W * 48, H * 48), Image.NEAREST).save(out / "elaia_village_3x.png")
    overlay(g, out / "elaia_village_3x.png", out / "elaia_village_walk.png", ev)
    screen_views(g, out)
    problems, seen = check(g, m)
    if args.check:
        print(walk_text(g, seen))
    for p in problems:
        print("PROBLEM:", p)
    print("wrote data/layouts/ElaiaVillage, the rooms, design/phase1/img/elaia_village.png,"
          " build/elaia/elaia_village_walk.png")


if __name__ == "__main__":
    main()
