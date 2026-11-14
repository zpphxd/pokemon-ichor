#!/usr/bin/env python3
"""Build Elaia Village and its four interiors.

Elaia's outdoor blockdata is composed here from aethos ground and kalliste
structures, with collision and elevation set cell by cell. The interiors copy
the finished room blockdata from design/phase1/rooms/.

  /usr/bin/python3 tools/ichor/maps/elaia.py            # write layouts, events and renders
  /usr/bin/python3 tools/ichor/maps/elaia.py --check    # also print the walk map

Writes:
  data/layouts/ElaiaVillage/{map,border}.bin
  data/layouts/ElaiaVillage_*/{map,border}.bin   (copied rooms)
  data/maps/ElaiaVillage/map.json                (its events)
  design/phase1/img/elaia_village.png            (3x render)
  build/elaia/elaia_village_walk.png             (collision and event overlay)
  build/elaia/view_*.png                         (GBA-screen crops along the route)

Kalliste ids come from tools/ichor/art/kalliste_build.py's own packing, so they
always match the compiled tileset. Coordinates the scripts care about live in
SPOTS and the event tables below; data/maps/ElaiaVillage/scripts.pory follows
them. The check pass verifies that every event tile is reachable, that the
cutscene walks cross only open ground, and that no story trigger can be
walked around.
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
SHADE = 0x01C              # grass in deep shade
FLOWERS = 0x004            # red anemones (animated), walkable
TROUGH = 0x006             # a whitewashed trough of anemones (a planter)
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
CYPRESS_TOP_OVER_OLIVE = (0x1EC, 0x1ED)  # cypress top in front of an olive bottom (left, right)
CYPRESS_BOT_UNDER_TIP = (0x1F4, 0x1F5)   # cypress bottom under an olive tip (left, right)
PINE = [[0x01E, 0x01F], [0x026, 0x027]]  # stone pine

PATH = [[0x1D0, 0x1D1, 0x1D2], [0x1D8, 0x1D9, 0x1DA], [0x1E0, 0x1E1, 0x1E2]]
GARDEN = [[0x103, 0x104, 0x105], [0x10B, 0x10C, 0x10D], [0x113, 0x114, 0x115]]
LEDGE = {"s": 0x087, "sw": 0x08D, "se": 0x08E, "s_l": 0x0D5, "s_r": 0x0D6}
UNDER_LEDGE = 0x002        # grass with a ledge's shadow line on top

PALAESTRA = [
    [0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
    [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
    [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
    [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
    [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC],
]
STALL3 = [[0x028, 0x029, 0x02B], [0x030, 0x031, 0x033]]  # a festival stall: tile roof, awning
TRIPOD = (0x130, 0x131)                                  # bronze tripod on a marble plinth

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


PAVING = [[kid("paving", 0, 0), kid("paving", 1, 0), kid("paving", 2, 0)],
          [kid("paving", 0, 1), kid("paving", 3, 0), kid("paving", 2, 1)],
          [kid("paving", 0, 2), kid("paving", 1, 2), kid("paving", 2, 2)]]
PAVING_ALTS = [kid("paving", 1, 1), kid("paving", 3, 1), kid("paving", 3, 2)]
PAVE_LIKE = ("posts", "altar_square", "stall", "well", "tripod")
WALL = {  # wall_drystone: whitewashed caps on dry stone
    "w": kid("wall_drystone", 0, 0), "a": kid("wall_drystone", 1, 0), "b": kid("wall_drystone", 2, 0),
    "e": kid("wall_drystone", 3, 0), "pier": kid("wall_drystone", 4, 0),
    "ns": kid("wall_drystone", 0, 1), "n": kid("wall_drystone", 1, 1),
    "nw": kid("wall_drystone", 2, 1), "ne": kid("wall_drystone", 3, 1),
}

# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------
WALK, SOLID = 0, 1


class Grid:
    def __init__(self):
        self.mt = np.full((H, W), GRASS, np.int32)
        self.solid = np.zeros((H, W), bool)
        self.kind = np.full((H, W), "grass", object)   # what's there, for autotiling and checks

    def set(self, x, y, mid, solid, kind=None):
        if 0 <= x < W and 0 <= y < H:
            self.mt[y, x] = mid
            self.solid[y, x] = solid
            if kind:
                self.kind[y, x] = kind

    def struct(self, key, x, y, door_solid=True):
        """Place a kalliste structure with its top-left at (x, y). Its walk grid
        sets collision: X solid; . T J D walkable (a D door is solid when
        door_solid, for houses nobody can enter)."""
        s = K[key]
        for j in range(s.h):
            for i in range(s.w):
                code = s.walk[j][i]
                if code == "-":
                    continue
                solid = code == "X" or (code == "D" and door_solid)
                self.set(x + i, y + j, s.ids[j][i], solid, key)

    def block(self, ids, x, y, solid=True, kind="building"):
        for j, row in enumerate(ids):
            for i, mid in enumerate(row):
                self.set(x + i, y + j, mid, solid, kind)

    def ground(self, cells, kind):
        for x, y in cells:
            self.kind[y, x] = kind
            self.solid[y, x] = False

    def rect(self, x0, y0, x1, y1, kind):
        self.ground([(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)], kind)

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
            elif k in ("grass", "shade", "bed", "flowers"):
                self.set(x + i, y - 1, OLIVE_TIP_GRASS[i], self.solid[y - 1, x + i], "tip")

    def cypress(self, x, y):
        """A cypress spire, top at (x, y). In front of an olive's bottom row the
        top uses the piece that keeps the olive's trunk behind it."""
        k = self.kind[y, x]
        if k == "olive_bot":
            half = 0 if self.mt[y, x] in (OLIVE_BOT[0], OLIVE_BOT_TIP[0]) else 1
            self.set(x, y, CYPRESS_TOP_OVER_OLIVE[half], SOLID, "cypress_top")
        else:
            self.set(x, y, CYPRESS_TOP, SOLID, "cypress_top")
        self.set(x, y + 1, CYPRESS_BOT, SOLID, "cypress_bot")

    def pine(self, x, y):
        self.block(PINE, x, y, kind="pine")

    # --- autotiling ---------------------------------------------------------
    def autotile(self, kind, pieces, plain_alts=(), also=()):
        """Give every cell of `kind` its 9-slice piece from its four neighbours.
        Cells whose kind is in `also` count as the same ground but keep their
        metatile (pieces that carry their own paving, like the garland posts)."""
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
                if (cx, cy) == (1, 1) and plain_alts and noise(x, y, 5) < 22:
                    mid = plain_alts[noise(x, y, 6) % len(plain_alts)]
                self.mt[y, x] = mid


def noise(x, y, salt=0):
    """Deterministic 0..99 per cell, for scattering ground variety."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177
    return (h ^ (h >> 16)) % 100


# ---------------------------------------------------------------------------
# Composition
#
# Elaia sits on a hillside above its olive groves. The road from Route 1 comes
# down from the north through the forest; the upper village (Melitta's house
# with her hives behind it, Kydippe's house, the blue-domed shrine up on its
# own terrace) looks down on the festival square. The square's centrepiece is
# the old olive between two cypresses, with Halia's striped canopy at its
# foot. The square is a terrace: its retaining wall has two flights of steps,
# one down a cypress allee to the Akademia in its grove (south-west), one
# under the footrace's finish arch into the terraced olive groves
# (south-east), where the course winds down to its starting stele.
#
# The forest at the map's edges is planted on the same 2x2 phase as the
# layout's border (olive tops at even x and even y), so where the camera runs
# past the edge, the trees carry on without a seam. Its inner face steps in
# and out, with cypresses and single olives stood in front of it.
# ---------------------------------------------------------------------------
SPOTS = {
    "door_player": (5, 8),
    "door_kydippe": (17, 6),
    "door_akademia": (5, 29),
    "halia": (14, 15),
    "line": [(14, 16), (14, 17), (14, 18)],   # Korinna, Philon, the player
    "kleon": (14, 17),                         # beat 4; the player faces him from (14,19)
    "exit_column": 11,                         # Kleon and Alethea leave north up this column
}

# The edge forest, as 2x2 blocks on the border's phase (block bx covers x 2bx..2bx+1).
FOREST_BLOCKS = [
    #  bx: 0123456789ABCDE
    "FFFFF..FFFFFFFF",   # y 0-1   the road comes in at x 10-13
    "F.......FFF...F",   # y 2-3   hives behind the house; a clearing by the gate; the shrine
    "F.............F",   # y 4-5
    "F.............F",   # y 6-7
    "F.............F",   # y 8-9
    "F.............F",   # y 10-11
    "F.............F",   # y 12-13
    "F.............F",   # y 14-15
    "F.............F",   # y 16-17
    "F............FF",   # y 18-19
    "FF...........FF",   # y 20-21
    "FF............F",   # y 22-23
    "F.............F",   # y 24-25
    "F.............F",   # y 26-27
    "F.............F",   # y 28-29
    "F.............F",   # y 30-31
    "FFFFFFFFFFFFFFF",   # y 32-33
]


def compose():
    g = Grid()
    edge_forest(g)
    north(g)
    upper_village(g)
    square(g)
    west(g)
    east(g)
    lower_terrace(g)
    finish(g)
    return g


def edge_forest(g):
    """The forest band. Blocks on the map's outer edge are mostly olives, so
    they run on into the border's olives; inside the band, stone pines and
    pairs of cypresses break the olives up."""
    blocks = {(bx, by) for by, row in enumerate(FOREST_BLOCKS) for bx, c in enumerate(row) if c == "F"}
    kinds = {}
    for bx, by in sorted(blocks, key=lambda b: (b[1], b[0])):
        buried = all((bx + dx, by + dy) in blocks or not (0 <= bx + dx < 15 and 0 <= by + dy < 17)
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        n = noise(bx, by, 11)
        if buried and n < 70:
            kind = "olive"
        else:
            kind = "pine" if n < 16 else "cypress" if n < 40 else "olive"
        kinds[(bx, by)] = kind
    for (bx, by), kind in list(kinds.items()):    # an olive's crown can't tip into a pine
        if kind == "pine" and kinds.get((bx, by + 1)) == "olive":
            kinds[(bx, by)] = "cypress"
    for (bx, by) in sorted(blocks, key=lambda b: (b[1], b[0])):
        x, y = 2 * bx, 2 * by
        kind = kinds[(bx, by)]
        if kind == "olive":
            g.olive(x, y)
        elif kind == "pine":
            g.pine(x, y)
        else:
            g.cypress(x, y)
            g.cypress(x + 1, y)


def face_cypresses(g, spots):
    """Cypresses stood in front of the forest's face, on its bottom row, so the
    face steps forward. Each needs open grass below for its foot."""
    for x, y in spots:
        if g.kind[y, x] in ("olive_bot", "grass") and g.kind[y + 1, x] == "grass":
            g.cypress(x, y)


def flowers(g, cells):
    for x, y in cells:
        if g.kind[y, x] == "grass":
            g.set(x, y, FLOWERS, WALK, "flowers")


def north(g):
    """The road from Route 1 and the gate: a herm and two cypresses mark it."""
    g.rect(10, 0, 13, 2, "path")              # the seam with Route 1: x 10-13
    g.rect(10, 3, 12, 10, "path")             # down to the square
    g.set(9, 4, HERM, SOLID, "herm")          # road-pillar of Hermes at the gate
    g.cypress(9, 1)
    g.cypress(13, 3)
    flowers(g, [(15, 3), (15, 4), (15, 2)])


def upper_village(g):
    # --- Melitta's house, her hives behind it, her yard in front ---
    g.struct("house_large", 4, 4, door_solid=False)          # door (5,8)
    for x, y in ((3, 2), (5, 2), (7, 2)):                     # three skeps along the forest's foot
        g.set(x, y, SKEP, SOLID, "skep")
    g.set(2, 6, SKEP, SOLID, "skep")                         # and one more round the side
    flowers(g, [(2, 2), (4, 2), (6, 2), (8, 2), (2, 3), (4, 3), (6, 3), (3, 4), (2, 5), (3, 7), (2, 8)])
    g.rect(5, 9, 9, 10, "path")                               # from the door to the road
    garden(g, 2, 9, 3, 2)                                     # Melitta's kitchen garden
    low_wall_ew(g, 2, 7, 11)                                  # the yard's wall above the square
    g.set(8, 11, TROUGH, SOLID, "trough")
    g.set(9, 8, TROUGH, SOLID, "trough")
    # --- Kydippe's house and herb garden ---
    g.struct("house_small", 16, 4, door_solid=False)          # door (17,6)
    g.rect(13, 7, 18, 8, "path")                              # from her door to the road
    garden(g, 19, 8, 3, 2)                                    # her herb garden
    g.set(20, 6, TROUGH, SOLID, "trough")
    g.set(14, 5, SIGN, SOLID, "sign")                         # ELAIA VILLAGE
    flowers(g, [(20, 4), (21, 5), (20, 7), (15, 5), (15, 6)])
    # --- the shrine on its terrace ---
    g.struct("shrine_dome", 22, 2)                            # door (24,6), shut today
    g.cypress(27, 3)
    g.cypress(27, 5)
    g.cypress(21, 2)
    g.rect(21, 7, 27, 7, "pave")                              # its forecourt
    terrace_wall(g, 22, 27, 8, steps=(24,))


def square(g):
    # an irregular paved terrace
    g.rect(9, 11, 18, 11, "pave")
    g.rect(7, 12, 21, 20, "pave")
    g.rect(8, 21, 20, 21, "pave")
    g.rect(22, 13, 23, 16, "pave")                            # the well's bay
    # the old olive between two cypresses, Halia's canopy at its foot
    for y in range(11, 15):
        for x in range(12, 18):
            g.set(x, y, FLOWERS if (x * 2 + y) % 3 == 0 else GRASS, SOLID, "bed")
    g.olive(14, 12)
    g.cypress(12, 11)
    g.cypress(17, 11)
    g.set(12, 13, TROUGH, SOLID, "bed")
    g.set(17, 13, TROUGH, SOLID, "bed")
    for i, mid in enumerate(AWNING):
        g.set(13 + i, 14, mid, SOLID, "canopy")
    g.set(12, 14, FLOWERS, SOLID, "bed")
    g.set(17, 14, FLOWERS, SOLID, "bed")
    strand(g, 6, 11, 5)                                       # Klotheia garlands
    strand(g, 18, 11, 5)
    g.struct("altar_square", 7, 16)                           # the festival altar
    g.block(STALL3, 19, 16, kind="stall")                     # a honey-cake stall
    g.set(23, 14, WELLHEAD, SOLID, "well")
    g.olive(7, 19)                                            # shade trees in the square's corners
    g.olive(20, 19)
    g.set(7, 13, TROUGH, SOLID, "trough")
    g.set(21, 13, TROUGH, SOLID, "trough")


def west(g):
    """A neighbour's house, shut for the festival, and its walled garden."""
    g.struct("house_small", 2, 12)                            # door (3,14) shut
    g.rect(3, 15, 6, 16, "path")                              # its doorstep, out to the square
    garden(g, 2, 17, 3, 2)
    low_wall_ew(g, 2, 5, 19)
    g.cypress(6, 12)
    g.set(5, 17, TROUGH, SOLID, "trough")
    flowers(g, [(5, 18), (6, 18), (2, 16), (6, 14)])
    g.pine(2, 20)
    g.cypress(5, 20)


def east(g):
    """The olive press and its threshing floor; the orchard behind."""
    g.struct("olive_press", 25, 9)                            # front row y=11
    g.rect(24, 12, 27, 13, "pave")                            # the threshing floor
    g.olive(25, 15)
    g.olive(24, 18)
    g.cypress(27, 17)
    g.olive(22, 20)
    flowers(g, [(24, 11), (26, 14), (27, 15), (23, 17), (26, 20)])


def lower_terrace(g):
    # the square's retaining wall: steps to the Akademia (west) and the groves (east)
    terrace_wall(g, 4, 25, 22, steps=(9, 10, 18, 19))
    finish_arch(g, 17, 20)
    # --- the Akademia in its grove ---
    g.rect(9, 23, 10, 29, "path")                             # the allee
    g.rect(2, 30, 10, 31, "pave")                             # the forecourt
    g.block(PALAESTRA, 2, 25)                                 # door (5,29)
    g.solid[29, 5] = True                                     # animated door: walk into it
    for y in (23, 25, 27):
        g.cypress(8, y)
        g.cypress(11, y)
    g.olive(2, 23)
    g.pine(4, 23)
    g.cypress(6, 23)
    g.cypress(7, 24)
    g.block([[TRIPOD[0]], [TRIPOD[1]]], 8, 29, kind="tripod")  # a bronze dedication
    g.set(11, 29, SIGN, SOLID, "sign")                         # THE AKADEMIA
    flowers(g, [(11, 30), (12, 31), (11, 31)])
    # --- the terraced groves and the race course ---
    g.rect(18, 23, 19, 25, "path")
    g.rect(18, 24, 23, 25, "path")
    g.rect(22, 24, 23, 29, "path")
    g.rect(22, 28, 26, 29, "path")
    g.set(27, 28, SIGN, SOLID, "sign")                        # the starting stele
    # olives planted in rows on two terraces, the lower one behind a dry-stone lip
    for x, y in ((12, 24), (15, 24), (26, 24), (13, 29), (16, 29), (19, 29), (25, 30)):
        g.olive(x, y)
    ledge_row(g, 12, 21, 27)
    ledge_row(g, 24, 27, 27)
    g.cypress(21, 23)
    g.cypress(24, 23)
    flowers(g, [(14, 23), (17, 26), (20, 26), (12, 26), (18, 31), (21, 30), (23, 31), (27, 26)])


def ledge_row(g, x0, x1, y):
    """An aethos dry-stone terrace lip along row y: one-way, jump south."""
    for x in range(x0, x1 + 1):
        if g.kind[y, x] != "grass":
            continue
        mid = LEDGE["s_l"] if x == x0 else LEDGE["s_r"] if x == x1 else LEDGE["s"]
        g.set(x, y, mid, WALK, "ledge")


def finish(g):
    face_cypresses(g, [(4, 1), (16, 3), (2, 7), (2, 15), (26, 9), (27, 21), (3, 21), (12, 29), (27, 25)])
    g.autotile("path", PATH, also=("pave", "steps") + PAVE_LIKE)   # paths run flush into the paving
    g.autotile("pave", PAVING, PAVING_ALTS, also=PAVE_LIKE)
    for y in range(H):                                        # a few anemones in the meadows
        for x in range(W):
            if g.kind[y, x] == "grass" and g.mt[y, x] == GRASS and noise(x, y, 2) < 3:
                g.mt[y, x] = FLOWERS
    seal_pockets(g)


def seal_pockets(g):
    """Grass that nobody can reach (gaps between trees) becomes solid, so the
    edges are unambiguous and nothing can stand in a hole."""
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


def low_wall_ew(g, x0, x1, y, gate=()):
    """A whitewashed dry-stone wall along row y, with gaps at `gate`."""
    for x in range(x0, x1 + 1):
        if x in gate:
            continue
        w_end = x == x0 or (x - 1) in gate
        e_end = x == x1 or (x + 1) in gate
        mid = WALL["pier"] if w_end and e_end else WALL["w"] if w_end else WALL["e"] if e_end else \
            WALL["a" if x % 2 else "b"]
        g.set(x, y, mid, SOLID, "wall")


def garden(g, x, y, w, h):
    """A kitchen garden of tilled earth."""
    for j in range(h):
        for i in range(w):
            cx = 0 if i == 0 else 2 if i == w - 1 else 1
            cy = 0 if j == 0 else 2 if j == h - 1 else 1
            g.set(x + i, y + j, GARDEN[cy][cx], SOLID, "garden")


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
    ("HALIA", GFX + "PRIESTESS", 14, 15, "DOWN", "Halia", "0"),
    ("KORINNA", GFX + "YOUTH_F", 14, 16, "UP", "Korinna", "0"),
    ("PHILON", GFX + "YOUTH_M", 14, 17, "UP", "Philon", "0"),
    ("GYLIPPOS", GFX + "ELDER_M", 7, 15, "RIGHT", "Gylippos", "0"),
    ("WOMAN", GFX + "WOMAN", 9, 13, "UP", "FestivalWoman", "0"),
    ("MAN", GFX + "MAN", 16, 20, "RIGHT", "FestivalMan", "0"),
    ("FARMER", GFX + "HARVESTER", 26, 12, "UP", "OliveFarmer", "0"),
    ("KID", GFX + "KID_M", 23, 15, "UP", "Kid", "0"),
    ("WOOLOO", "OBJ_EVENT_GFX_SPECIES(WOOLOO)", 22, 16, "RIGHT", "KidsWooloo", "0"),
    ("SHEPHERD", GFX + "SHEPHERD", 12, 1, "DOWN", "OldShepherd", "0"),
    ("KLEON", GFX + "KLEON", 14, 17, "DOWN", "Kleon", "FLAG_ICHOR_HIDE_KLEON_ELAIA"),
    ("ALETHEA", GFX + "ALETHEA", 5, 29, "DOWN", "0", "FLAG_ICHOR_HIDE_ALETHEA_ELAIA"),
]
ITEMS = [("ITEM_POTION", 24, 11, "FLAG_ICHOR_ITEM_ELAIA_POTION")]
WARPS = [   # order is the warp id; the interiors point back at these
    (17, 6, "MAP_ELAIA_VILLAGE_NEIGHBORS_HOUSE", 0),
    (5, 8, "MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F", 1),
    (5, 29, "MAP_ELAIA_VILLAGE_AKADEMIA", 0),
]
LINE_SPOT = (14, 18)                                   # the player's place in Halia's line
LINE_CORE = {(x, y) for x in range(13, 16) for y in range(15, 19)}
# Where scripts.pory's SetUpVillage stands the watchers for beat 4, ringed round Kleon.
BEAT4_RING = {"KORINNA": (12, 16), "PHILON": (16, 16), "WOMAN": (12, 20), "MAN": (16, 20), "GYLIPPOS": (17, 18)}
KLEON_STEPS = [(9, 22), (10, 22), (18, 22), (19, 22)]  # both flights up from the lower terrace
SHEPHERD_ROW = [(x, 2) for x in range(10, 14)]
SIGNS = [   # x, y, facing, script
    (14, 5, "ANY", "VillageSign"),
    (6, 8, "NORTH", "PlayersHouseSign"),
    (16, 6, "NORTH", "KydippesHouseSign"),
    (11, 29, "ANY", "AkademiaSign"),
    (13, 14, "NORTH", "FestivalBanner"),
    (16, 14, "NORTH", "FestivalBanner"),
    (9, 4, "ANY", "Herm"),
    (24, 6, "NORTH", "ShrineDoor"),
    (3, 14, "NORTH", "NeighboursDoor"),
    (23, 14, "ANY", "Well"),
    (3, 2, "ANY", "Beehives"),
    (7, 2, "ANY", "Beehives"),
    (2, 6, "ANY", "Beehives"),
    (25, 11, "NORTH", "OlivePress"),
    (26, 11, "NORTH", "OlivePress"),
    (27, 11, "NORTH", "OlivePress"),
    (27, 28, "ANY", "RaceStart"),
    (7, 17, "NORTH", "Altar"),
    (8, 17, "NORTH", "Altar"),
    (19, 17, "NORTH", "Stall"),
    (20, 17, "NORTH", "Stall"),
    (21, 17, "NORTH", "Stall"),
]
HIDDEN = [("ITEM_HONEY", 5, 2, "FLAG_HIDDEN_ITEM_ICHOR_ELAIA_HONEY")]


def halia_ring(g):
    """Coord triggers ringing the line at Halia's canopy: walk in and she calls you."""
    out = []
    for y in range(14, 21):
        for x in range(10, 19):
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
    coords = [(x, y, "FLAG_ICHOR_GOT_STARTER", "ShepherdGate") for x, y in SHEPHERD_ROW]
    coords += [(x, y, "FLAG_ICHOR_THREAD_READ", "HaliaCalls") for x, y in halia_ring(g)]
    coords += [(x, y, "FLAG_ICHOR_KLEON_BATTLE_1_DONE", "KleonTrigger") for x, y in KLEON_STEPS]
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
    """Walkable cells sit at elevation 3 and solid ones at 0, as in vanilla
    outdoor maps; the Akademia's animated door is solid at elevation 3, like
    vanilla doors, so the player walks into it."""
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            solid = bool(g.solid[y, x])
            elev = 3 if (not solid or g.mt[y, x] == PALAESTRA[4][3]) else 0
            out[y, x] = (g.mt[y, x] & 0x3FF) | (int(solid) << 10) | (elev << 12)
    return out


BORDER = [OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]]


def write_layout(g):
    d = ROOT / "data/layouts/ElaiaVillage"
    blockdata(g).astype("<u2").tofile(d / "map.bin")
    np.array(BORDER, np.uint16).astype("<u2").tofile(d / "border.bin")


ROOMS = {
    "ElaiaVillage_PlayersHouse_1F": "players_house_1f",
    "ElaiaVillage_PlayersHouse_2F": "players_house_2f",
    "ElaiaVillage_NeighborsHouse": "kydippe_house",
    "ElaiaVillage_Akademia": "elaia_akademia",
}


def write_rooms():
    """The rooms are finished blockdata (design/phase1/ROOMS_*.md). Their border
    is four of the room set's near-black void metatile."""
    for name, room in ROOMS.items():
        d = ROOT / "data/layouts" / name
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f"design/phase1/rooms/{room}.bin", d / "map.bin")
        void = 0x0200 if room == "elaia_akademia" else 0x0210
        np.array([void] * 4, np.uint16).astype("<u2").tofile(d / "border.bin")


def render(out, scale=3):
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "LAYOUT_ELAIA_VILLAGE",
                    "--scale", str(scale), "-o", str(out)], check=True, stdout=subprocess.DEVNULL)


# Screen-sized views along the player's route: (name, player x, y)
VIEWS = [
    ("01_front_door", 5, 9), ("02_hives", 6, 3), ("03_north_gate", 11, 3),
    ("04_kydippe", 17, 7), ("05_square_line", 14, 18), ("06_square_north", 12, 10),
    ("07_well_press", 23, 13), ("08_west", 5, 15), ("09_akademia", 6, 30),
    ("10_finish", 18, 22), ("11_race_start", 23, 28), ("12_shrine", 24, 7),
]


FRAME = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}


def people(im, pad=0):
    """Draw the map's people over a 1x render, as they stand when the village
    first loads (the review renders show the square with its crowd)."""
    from PIL import Image
    for lid, gfx, x, y, facing, script, flag in OBJECTS:
        if flag != "0":
            continue
        if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
            sheet = Image.open(ROOT / f"graphics/pokemon/{gfx[22:-1].lower()}/overworld.png")
            fw = 32
            frame = {"DOWN": 0, "UP": 2, "LEFT": 4, "RIGHT": 4}[facing]
        else:
            sheet = Image.open(ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png")
            fw = 16
            frame = FRAME[facing]
        spr = sheet.convert("RGBA").crop((frame * fw, 0, frame * fw + fw, 32))
        if sheet.mode == "P":   # color 0 is transparent
            idx = sheet.crop((frame * fw, 0, frame * fw + fw, 32)).load()
            px = spr.load()
            for j in range(32):
                for i in range(fw):
                    if idx[i, j] == 0:
                        px[i, j] = (0, 0, 0, 0)
        if facing == "RIGHT":
            spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
        ox = (x + pad) * 16 + 8 - fw // 2
        oy = (y + pad) * 16 + 16 - 32
        im.paste(spr, (ox, oy), spr)
    return im


def screen_views(g, out_dir, scale=2):
    """Render each view as the GBA shows it: 15x10 tiles with the player at
    (7,5), and the layout's border wherever the screen runs past the map (Route
    1's edge stands in to the north)."""
    pad = 8
    bw, bh = W + 2 * pad, H + 2 * pad
    big = np.zeros((bh, bw), np.uint16)
    for y in range(bh):
        for x in range(bw):
            mx, my = x - pad, y - pad
            big[y, x] = BORDER[(mx % 2) + 2 * (my % 2)]
    big[pad:pad + H, pad:pad + W] = g.mt
    tmp = out_dir / "views_blockdata.bin"
    big.astype("<u2").tofile(tmp)
    whole = out_dir / "views_whole.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(bw), "--primary", "aethos", "--secondary", "kalliste", "-o", str(whole)],
                   check=True, stdout=subprocess.DEVNULL)
    from PIL import Image
    im = people(Image.open(whole).convert("RGB"), pad)
    im.save(out_dir / "views_people.png")
    views = []
    for name, px, py in VIEWS:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16
        v = im.crop((x0, y0, x0 + 240, y0 + 160))
        v.resize((240 * scale, 160 * scale), Image.NEAREST).save(out_dir / f"view_{name}.png")
        views.append(v)
    # a contact sheet of every view, 4 across
    cols = 4
    rows = (len(views) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 248, rows * 168), (20, 20, 28))
    for i, v in enumerate(views):
        sheet.paste(v, ((i % cols) * 248 + 4, (i // cols) * 168 + 4))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / "views_sheet.png")


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


# Cutscene walks (scripts.pory's movements), as (start, moves). Every cell they
# cross must be open ground with nobody standing on it.
def cutscene_walks():
    ex = SPOTS["exit_column"]
    kx, ky = SPOTS["kleon"]
    return {
        "Kleon runs north": ((kx, ky), ["L"] * (kx - ex) + ["U"] * (ky - 1)),
        "Alethea comes out": ((5, 29), ["D", "D"] + ["R"] * 4 + ["U"] * 12 + ["R"] * 4),
        "Alethea leaves": ((13, 19), ["L", "L"] + ["U"] * 19),
    }


def check(g, m):
    """Every event reachable from the player's door; seams right; the story
    triggers can't be walked around; the cutscene walks are clear."""
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
            seen.add((nx, ny))
            q.append((nx, ny))
    problems = []
    for x in range(W):
        if (10 <= x <= 13) == bool(solid[0, x]):
            problems.append(f"north seam wrong at x={x}")
    warps = {(w["x"], w["y"]) for w in m["warp_events"]}
    people = {}
    for o in m["object_events"]:
        if solid[o["y"], o["x"]] and (o["x"], o["y"]) not in warps:   # Alethea waits in a doorway
            problems.append(f"object {o.get('local_id', o['graphics_id'])} on a solid cell ({o['x']},{o['y']})")
        if (o["x"], o["y"]) not in seen and (o["x"], o["y"]) not in warps:
            problems.append(f"object {o.get('local_id', o['graphics_id'])} unreachable at ({o['x']},{o['y']})")
        people[(o["x"], o["y"])] = o.get("local_id", o["graphics_id"])
    for c in m["coord_events"]:
        if (c["x"], c["y"]) not in seen:
            problems.append(f"coord ({c['x']},{c['y']}) unreachable")
    for w in m["warp_events"]:
        x, y = w["x"], w["y"]
        if (x, y + 1) not in seen:
            problems.append(f"warp ({x},{y}) has an unreachable front")
    for b in m["bg_events"]:
        x, y = b["x"], b["y"]
        if not any((x + dx, y + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            problems.append(f"bg event ({x},{y}) can't be read from anywhere")
    door = SPOTS["door_akademia"]
    for name, start, goal, gate in (
            ("Kleon", (door[0], door[1] + 1), (14, 10), set(KLEON_STEPS)),
            ("Halia", start, LINE_SPOT, set(halia_ring(g))),
            ("shepherd", start, (11, 0), set(SHEPHERD_ROW))):
        if reachable(g, start, goal, gate):
            problems.append(f"{name}'s trigger can be walked around")
    # The line and the beat-4 ring: the people Kleon gathers are moved by scripts.pory.
    moved = set(BEAT4_RING.values())
    for name, (s, moves) in cutscene_walks().items():
        x, y = s
        for mv in moves:
            x += {"L": -1, "R": 1}.get(mv, 0)
            y += {"U": -1, "D": 1}.get(mv, 0)
            if y < 0:
                break
            if solid[y, x] or ((x, y) in people and people[(x, y)] not in ("LOCALID_ELAIA_SHEPHERD",)):
                problems.append(f"{name}: blocked at ({x},{y})")
            if (x, y) in moved:
                problems.append(f"{name}: crosses a spot a watcher stands on ({x},{y})")
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
    render(out / "elaia_village_1x.png", 1)
    m, ev = map_events()
    from PIL import Image
    people(Image.open(out / "elaia_village_1x.png").convert("RGB")).resize(
        (W * 48, H * 48), Image.NEAREST).save(ROOT / "design/phase1/img/elaia_village.png")
    Image.open(out / "elaia_village_1x.png").resize((W * 48, H * 48), Image.NEAREST).save(out / "elaia_village_3x.png")
    overlay(g, out / "elaia_village_3x.png", out / "elaia_village_walk.png", ev)
    screen_views(g, out)
    problems, seen = check(g, m)
    if args.check:
        print(walk_text(g, seen))
    for p in problems:
        print("PROBLEM:", p)
    print("wrote data/layouts/ElaiaVillage, the rooms, design/phase1/img/elaia_village.png,"
          " build/elaia/elaia_village_walk.png, build/elaia/views_sheet.png")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
