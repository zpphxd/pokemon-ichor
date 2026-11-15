#!/usr/bin/env python3
"""Build Route 4, the Isthmus road: layout, events, checks and review renders.

The old paved road out of Emporion's Isthmus Gate (design/phase2/SCRIPT.md,
"Route 2, the Sacred Way", reconciled as Route 4 in BUILD.md's batch 3). It
leaves the gate north through the potters' quarter, turns east between the
family plots of the dead, climbs to the pass and ends in the cutting where the
Titans pulled a tomb down across it (beat 17), at the mouth of Hecate's Hollow.

  - the potters' quarter by the gate: two kilns, the drying racks, the wasters'
    heap; Exekias, the first trainer, in plain view
  - the tombs: the paving gives out between two walled family plots, and the
    grass has taken it (forced band 1); Myrrhine across the road
  - the hill spur: goat paths, the goatherd's meadow, the great herm with its
    Titanborn guard on a side path, and the terrace orchard behind a thorn
    thicket (Demeter's Sickle, end of Act I)
  - the rise to the pass (forced band 2), the cutting and the runner
  - the procession's camp, the rockslide (three heaps for the Bronze Hammer, in
    a chain, so all three must break) and the Hollow's mouth in the cut bank
  - below the camp, terrace lips drop back to the lower terrace: a loop past the
    walled grave plot and the family tomb a column drum has shut (the Girdle,
    Act II), back to the road among the tombs

Pieces come by key and name from build/skiron/catalog.json (TILES_skiron.md;
make it with /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile).
Only shapes the tileset already has are used, so nothing here rebuilds it.

Writes:
  data/layouts/Route4_Isthmus/map.bin, border.bin  (60x32, aethos + skiron)
  data/maps/Route4_Isthmus/map.json                its events and the city connection
  data/maps/Route4_Isthmus/scripts.pory            the generated block between the markers
  data/maps/EmporionCity/map.json                  only its "up" connection to this map

Checks: the city seam (open at x 7-9 only, aethos only in the 6 rows by it); the
road from the gate to the Hollow's mouth, with the slide shut until its three
heaps break; both forced bands and the three mandatory trainers' sight lines cut
the only way on, and the three optional ones don't; the terrace lips only drop
toward the city; every person, sign, item and hidden item can be reached and read;
the orchard, the family tomb and the woods clearing open only to their relics;
the herm's landing tile; Kleon's run off the city's gate (beat 16) stays clear.

Usage: /usr/bin/python3 tools/ichor/maps/route4.py [--render DIR] [--walk]
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
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))
from skiron_ground import FULL, canon  # noqa: E402

CAT = ROOT / "build/skiron/catalog.json"
NAME = "Route4_Isthmus"
MAP_ID = "MAP_ROUTE4_ISTHMUS"
LAYOUT_ID = "LAYOUT_ROUTE4_ISTHMUS"
MAP_DIR = ROOT / "data/maps" / NAME
LAYOUT_DIR = ROOT / "data/layouts" / NAME
CITY_JSON = ROOT / "data/maps/EmporionCity/map.json"
W, H = 60, 32

# ---------------------------------------------------------------------------
# The seam (BUILD.md): the Isthmus Gate's road crosses the city's north edge at
# x = 7..9, and Route 4 sits straight above the city (offset 0 both ways).
# ---------------------------------------------------------------------------
GATE = range(7, 10)
CITY_OFFSET = 0
STRIP_ROWS = 6                 # aethos only in the 6 rows by an up/down seam (MAP_DESIGN §5)

# ---------------------------------------------------------------------------
# aethos ids (TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS, TALL, FLOWERS, STELE, HERM, BOULDER = 0x001, 0x00D, 0x004, 0x003, 0x01B, 0x0E0
PATH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
        "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
OLIVE_TOP, OLIVE_BOT, OLIVE_BOT_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1DC, 0x1DD)
OLIVE_TIP = {"grass": (0x1CE, 0x1CF), "tall": (0x1C6, 0x1C7)}
CYPRESS_TOP = {"grass": 0x00E, "tall": 0x025}
CYPRESS_BOT, CYPRESS_BOT_UNDER_TIP = 0x016, (0x1F4, 0x1F5)
CYPRESS_TOP_OVER_OLIVE = (0x1EC, 0x1ED)
STONE_PINE = ((0x01E, 0x01F), (0x026, 0x027))
CAVE_TOP, CAVE_DOOR = 0x09F, 0x0A7      # General's cave entrance, retextured (MB_NON_ANIMATED_DOOR below)
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # N NE E SE S SW W NW


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


# ---------------------------------------------------------------------------
# The grid: ground kinds, then pieces on top, then the soft ground auto-tiled
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, cat):
        self.cat = cat
        self.ground = np.full((H, W), "grass", object)    # grass / road / path / tall / flowers
        self.mt = np.full((H, W), GRASS, np.int32)
        self.walk = np.full((H, W), ".", object)            # . X T G J
        self.fixed = np.zeros((H, W), bool)
        self.road_floor = np.zeros((H, W), bool)             # pieces drawn on the road's floor
        self.path_floor = np.zeros((H, W), bool)             # pieces on borrowed aethos path
        self.kind = np.full((H, W), "", object)              # what a placed cell is, for checks and swaps
        self.missing = {"road": set(), "tall": set()}
        self.tips, self.cyps = [], []

    # --- ground regions -------------------------------------------------------
    def fill(self, kind, x0, y0, x1, y1):
        self.ground[max(0, y0):min(H, y1 + 1), max(0, x0):min(W, x1 + 1)] = kind

    def cells(self, kind, pts):
        for (x, y) in pts:
            if 0 <= x < W and 0 <= y < H:
                self.ground[y, x] = kind

    # --- pieces ------------------------------------------------------------------
    def piece(self, key, x, y, cells=None, kind=None):
        s = self.cat[key]
        for cy in range(s["h"]):
            for cx in range(s["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                X, Y = x + cx, y + cy
                if not (0 <= X < W and 0 <= Y < H):
                    continue
                self.mt[Y, X] = s["ids"][cy][cx]
                self.walk[Y, X] = s["walk"][cy][cx]
                self.fixed[Y, X] = True
                self.kind[Y, X] = kind or key
                g = s["ground"].get(f"{cx},{cy}")
                if g == "path":
                    self.path_floor[Y, X] = True
                if key.startswith("rubble"):
                    self.road_floor[Y, X] = True

    def named(self, key, name, x, y, kind=None):
        cx, cy = self.cat[key]["names"][name]
        self.piece(key, x - cx, y - cy, cells={(cx, cy)}, kind=kind)

    def put(self, mid, x, y, walk="X", kind="prop"):
        if 0 <= x < W and 0 <= y < H:
            self.mt[y, x] = mid
            self.walk[y, x] = walk
            self.fixed[y, x] = True
            self.kind[y, x] = kind

    def free(self, x, y, w=1, h=1):
        return all(0 <= x + i < W and 0 <= y + j < H and not self.fixed[y + j, x + i]
                   and self.ground[y + j, x + i] in ("grass", "flowers")
                   for j in range(h) for i in range(w))

    # --- aethos trees ------------------------------------------------------------
    def olive(self, x, y):
        for i in range(2):
            self.put(OLIVE_TOP[i], x + i, y, kind="olive_top")
            self.put(OLIVE_BOT[i], x + i, y + 1, kind="olive_bot")
        self.tips.append((x, y))

    def cypress(self, x, y):
        self.put(CYPRESS_BOT, x, y + 1, kind="cypress_bot")
        self.fixed[y, x] = True
        self.walk[y, x] = "X"
        self.kind[y, x] = "cypress_top"
        self.cyps.append((x, y))

    def stone_pine(self, x, y):
        for j in range(2):
            for i in range(2):
                self.put(STONE_PINE[j][i], x + i, y + j, kind="stone_pine")

    # --- auto-tiling ---------------------------------------------------------------
    def region(self, kind):
        m = self.ground == kind
        if kind == "road":
            m = m | self.road_floor
        if kind == "path":
            # the path runs on under pieces on borrowed path, and into the road
            m = m | self.path_floor | (self.ground == "road") | self.road_floor
        return m

    def key(self, m, x, y):
        nb = []
        for dx, dy in DIRS:
            X, Y = min(max(x + dx, 0), W - 1), min(max(y + dy, 0), H - 1)
            nb.append("1" if m[Y, X] else "0")
        return canon("1", nb)

    def autotile(self):
        road, tall = self.cat["road"], self.cat["tall"]
        rm, tm, pm = self.region("road"), self.region("tall"), self.region("path")
        for y in range(H):
            for x in range(W):
                if self.fixed[y, x]:
                    continue
                g = self.ground[y, x]
                if g == "road":
                    k = self.key(rm, x, y)
                    if k == FULL:
                        r = noise(x, y, 3)
                        name = "mid3" if r < 7 else "mid2" if r < 20 else "mid"
                    else:
                        name = k
                    if name not in road["names"]:
                        self.missing["road"].add(f"{k}@{x},{y}")
                        name = "mid"
                    cx, cy = road["names"][name]
                    self.mt[y, x] = road["ids"][cy][cx]
                    self.kind[y, x] = "road"
                elif g == "tall":
                    k = self.key(tm, x, y)
                    self.walk[y, x] = "G"
                    self.kind[y, x] = "tall"
                    if k == FULL:
                        self.mt[y, x] = TALL
                    elif k in tall["names"]:
                        cx, cy = tall["names"][k]
                        self.mt[y, x] = tall["ids"][cy][cx]
                    else:
                        self.missing["tall"].add(f"{k}@{x},{y}")
                        self.mt[y, x] = TALL
                elif g == "path":
                    def n(dx, dy):
                        X, Y = x + dx, y + dy
                        return not (0 <= X < W and 0 <= Y < H) or pm[Y, X]
                    v = "T" if not n(0, -1) else "B" if not n(0, 1) else ""
                    hs = "L" if not n(-1, 0) else "R" if not n(1, 0) else ""
                    self.mt[y, x] = PATH.get(v + hs, PATH.get(v or hs or "C", PATH["C"]))
                    self.kind[y, x] = "path"
                elif g == "flowers":
                    self.mt[y, x] = FLOWERS
                    self.kind[y, x] = "grass"
                else:
                    self.mt[y, x] = GRASS
                    self.kind[y, x] = "grass"
        # tree tops need to know what they stand over
        for (x, y) in self.cyps:
            under = self.kind[y, x]
            if under in ("olive_bot",):
                pass
            self.mt[y, x] = CYPRESS_TOP["tall" if self.ground[y, x] == "tall" else "grass"]
        for (x, y) in self.tips:
            if y == 0:
                continue
            for i in range(2):
                X, Y = x + i, y - 1
                k = self.kind[Y, X]
                if k == "olive_bot":
                    self.mt[Y, X] = OLIVE_BOT_TIP[i]
                elif k == "cypress_bot":
                    self.mt[Y, X] = CYPRESS_BOT_UNDER_TIP[i]
                elif not self.fixed[Y, X] and k in ("grass", "tall"):
                    self.mt[Y, X] = OLIVE_TIP["tall" if k == "tall" else "grass"][i]
                    if self.walk[Y, X] == ".":
                        self.walk[Y, X] = "T"

    @property
    def solid(self):
        return np.isin(self.walk, ["X", "J"])


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------

# Where things stand (also used by the events and the checks)
HERM_AT = (23, 7)                  # the great herm; its landing tile is (23, 8)
MOUTH = (57, 7)                    # the Hollow's mouth: the warp, entered from (57, 8)
HEAPS = [(52, 9), (53, 9), (54, 9)]    # the rockslide's three heaps, broken in this order
SLIDE = (51, 6, 56, 11)            # the slide's box (x0, y0, x1, y1), for the swap
CAMP = (43, 11, 56, 16)            # the camp's box
STEPS = (18, 4)                    # the orchard's steps, where the thicket stands
DRUM = (42, 23)                    # the family tomb's gate, where the column drum stands
TEACH_RUBBLE = (6, 19)             # the woods clearing's mouth, choked with marble rubble
# Hecate's glade in the woods north of the corner, entered from the road at (8..9, 12)
GLADE_GRASS = {7: (4, 7), 8: (3, 8), 9: (3, 9), 10: (3, 9), 11: (4, 9), 12: (8, 9)}
SHRINE = (6, 7)                    # her crossroads shrine: a bronze tripod on its plinth (6, 8)
GLADE = {(x, y) for y, (x0, x1) in GLADE_GRASS.items() for x in range(x0, x1 + 1)} | {SHRINE}
TRIGGER_X = 48                     # beat 17's first scene: 4 tiles short of the slide


def fv(x, y, salt=1):
    """A cliff face variant: mostly plain strata, a feature one cell in four."""
    r = noise(x, y, salt)
    return "B" if r < 12 else "C" if r < 25 else "A"


def plot(g, x0, y0, x1, y1, gate=None, panel=None, front="south"):
    """A walled family plot: walls on x0, x1, y0 and y1. gate: an x left open on
    the south wall (y1). panel: an x on the north wall carved with the family name."""
    for x in range(x0 + 1, x1):
        g.named("plot_wall", "EW2" if x == panel else "EW", x, y0, kind="plot")
        if gate is not None and x == gate:
            continue
        if gate is not None and x == gate - 1:
            g.named("plot_wall", "W", x, y1, kind="plot")
        elif gate is not None and x == gate + 1:
            g.named("plot_wall", "E", x, y1, kind="plot")
        else:
            g.named("plot_wall", "EW", x, y1, kind="plot")
    for y in range(y0 + 1, y1):
        g.named("plot_wall", "NS", x0, y, kind="plot")
        g.named("plot_wall", "NS", x1, y, kind="plot")
    g.named("plot_wall", "ES", x0, y0, kind="plot")
    g.named("plot_wall", "SW", x1, y0, kind="plot")
    g.named("plot_wall", "NE", x0, y1, kind="plot")
    g.named("plot_wall", "NW", x1, y1, kind="plot")


def woods(g, cells, salt, phase=True, mix=True):
    """Fill a set of cells with trees. Olives go on the border's 2x2 phase (even x
    and y) where they fit, so the edge woods run on into the border; the rest is
    stone pines, cypresses and kermes oak, chosen by noise, so the line is mixed
    and never one tree repeated."""
    cells = set(cells)
    def ring(x, y):        # the two cells by the map's edge, which meet the border's olives
        return phase and (x < 2 or y < 2 or x >= W - 2 or y >= H - 2)
    def fits(x, y, w, h, inner=False):
        return all((x + i, y + j) in cells and not g.fixed[y + j, x + i]
                   and not (inner and ring(x + i, y + j)) for j in range(h) for i in range(w))
    for y in range(H):
        for x in range(W):
            if (x, y) not in cells or g.fixed[y, x]:
                continue
            r = noise(x, y, salt)
            if ring(x, y):
                # by the edge: olives on the border's 2x2 phase, so the wood runs on into it
                if x % 2 == 0 and y % 2 == 0 and fits(x, y, 2, 2):
                    g.olive(x, y)
                    continue
                if fits(x, y, 1, 2):
                    g.cypress(x, y)
                    continue
            # inside: staggered, mixed, never a grid of one tree
            elif fits(x, y, 2, 2, True) and r < (60 if mix else 85):
                g.olive(x, y)
                continue
            elif mix and fits(x, y, 2, 2, True) and r < 74:
                g.stone_pine(x, y)
                continue
            elif fits(x, y, 1, 2, True) and r < 92:
                g.cypress(x, y)
                continue
            if fits(x, y, 2, 2, not ring(x, y)):
                g.olive(x, y)
            elif fits(x, y, 1, 2, not ring(x, y)):
                g.cypress(x, y)
            elif y >= H - STRIP_ROWS:
                g.put(BOULDER, x, y, kind="boulder")      # aethos only by the seam
            else:
                g.piece("oak", x, y)


def rect(x0, y0, x1, y1):
    return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]


def ground(g):
    # --- the road --------------------------------------------------------------
    g.fill("path", 7, 26, 9, H - 1)          # the gate's road, aethos only by the seam
    g.fill("road", 7, 13, 9, 25)             # up from the gate (the paving starts at the strip)
    g.fill("road", 7, 13, 36, 15)            # east among the tombs
    g.fill("road", 34, 8, 36, 12)            # the rise to the pass
    g.fill("road", 34, 8, 57, 10)            # the upper road, to the cutting and the slide
    g.fill("grass", 39, 8, 43, 8)            # the cutting narrows it to two
    # --- forced bands: the paving has gone, the grass has taken it ----------------
    g.fill("tall", 19, 11, 21, 16)           # band 1, between the two plots
    g.fill("tall", 34, 10, 36, 13)           # band 2, on the rise: four deep
    # --- side ways ---------------------------------------------------------------
    g.fill("path", 26, 5, 27, 12)            # the hill spur's goat path
    g.fill("path", 23, 8, 25, 9)             # the herm's side path
    # --- optional grass, each with a reason: drawn as staircases, never boxes -------
    # the goatherd's hill pasture, Menalkas and his goats in it, the Super Potion past it
    meadow(g, {1: (28, 31), 2: (28, 32), 3: (28, 32), 4: (28, 32), 5: (28, 31), 6: (28, 31),
               7: (28, 31), 8: (28, 31), 9: (29, 31)})
    meadow(g, {19: (2, 4), 20: (2, 4), 21: (3, 4)})                     # the woods clearing
    # Hecate's glade in the woods north of the corner: her crossroads shrine, an item
    meadow(g, GLADE_GRASS)
    # the lower terrace: the grave plot's back gate, the mound, the old milestone
    meadow(g, {20: (33, 36), 21: (33, 37), 22: (19, 37), 23: (19, 37), 24: (21, 24)})
    meadow(g, {21: (26, 30)})
    # the east meadow under the camp's terrace lips (the scree nook past it)
    meadow(g, {18: (48, 53), 19: (47, 54), 20: (47, 54), 21: (47, 54), 22: (47, 54), 23: (48, 54)})
    # the orchard's aisles, behind the thicket (the Sun Stone)
    meadow(g, {2: (18, 20), 3: (18, 20)})


def meadow(g, rows):
    """A patch of tall grass, row by row: {y: (x0, x1)}."""
    for y, (x0, x1) in rows.items():
        g.fill("tall", x0, y, x1, y)


def west_and_north_woods(g):
    """The woods the road runs between: west of the gate's road, the north-west
    corner over the first plot, the bottom strip by the city, and the shelterbelt
    that keeps the potters' quarter apart from the lower terrace."""
    cells = set()
    cells |= set(rect(0, 0, 10, 12))                       # north-west corner
    cells |= set(rect(0, 13, 6, 25))                       # west of the gate's road
    cells -= set(rect(2, 17, 5, 21))                       # the woods clearing
    cells -= GLADE                                         # Hecate's glade
    cells -= {TEACH_RUBBLE}
    cells |= set(rect(0, 26, 6, H - 1)) | set(rect(10, 26, W - 1, H - 1))   # the strip by the city
    cells |= set(rect(10, 0, 10, 3))
    woods(g, cells, 11)


def potters(g):
    """The potters' quarter by the gate, Corinth's Kerameikos outside the wall."""
    g.piece("kiln", 11, 17)
    g.piece("kiln", 14, 19)
    g.piece("pot_rack", 13, 17)
    g.piece("pot_rack", 12, 23)
    g.piece("firewood", 15, 17)
    # the yard's fence on the road south of Exekias: the road is the only way past him
    g.piece("firewood", 10, 23)
    g.piece("amphorae", 10, 24)
    g.piece("sherds", 10, 25)
    g.piece("sherds", 16, 21)                # the wasters' heap, warm ash: the hidden Ether
    g.piece("sherds", 17, 18)
    g.piece("amphorae", 11, 21)
    g.piece("amphorae", 14, 24)
    g.put(STELE, 10, 28, kind="sign")                       # ROUTE 4, at the south end
    for (k, x, y) in (("pebbles", 13, 19), ("pebbles", 16, 19), ("dry_grass", 12, 20), ("pebbles", 10, 19),
                      ("dry_grass", 15, 22), ("pebbles", 13, 22), ("dry_grass", 11, 25), ("dry_grass", 16, 24),
                      ("pebbles", 10, 16), ("dry_grass", 14, 16)):
        if g.free(x, y):
            g.piece(k, x, y)
    # the shelterbelt on the quarter's east side
    woods(g, rect(17, 22, 18, 25) + [(17, 19), (17, 20), (17, 21)], 21, phase=False)


def tombs(g):
    """The dead line the road: two walled family plots with the forced band
    between them, stelai and lekythoi on the verges, the mound on the lower terrace."""
    # the north plot (closed): the Kallias family, stelai and lekythoi inside
    plot(g, 11, 6, 20, 10, panel=15)
    for (k, x, y) in (("stele_family", 13, 7), ("lekythos", 16, 7), ("stele_palmette", 18, 7),
                      ("stele_low", 14, 9), ("stele_low", 17, 9), ("stele_low", 19, 9)):
        g.piece(k, x, y)
    g.cypress(12, 7)
    g.put(FLOWERS, 15, 9, ".", "grass")
    g.put(FLOWERS, 12, 9, ".", "grass")
    # the north verge, x 10-18: tombs with gaps
    g.put(STELE, 11, 12, kind="sign")                       # "Walk softly..."
    for (k, x, y) in (("stele_low", 10, 12), ("lekythos", 12, 11), ("stele_family", 14, 11),
                      ("stele_low", 16, 12), ("stele_palmette", 17, 11), ("stele_low", 18, 12)):
        g.piece(k, x, y)
    # past the band: the verge to the spur, Myrrhine's gap at (24, 12)
    for (k, x, y) in (("stele_low", 22, 12), ("lekythos", 23, 11), ("stele_low", 25, 12)):
        g.piece(k, x, y)
    g.cypress(22, 10)
    g.put(STELE, 28, 12, kind="sign")                       # the fork's sign
    for (k, x, y) in (("lekythos", 29, 11), ("stele_low", 30, 12), ("sarcophagus", 31, 12)):
        g.piece(k, x, y)
    g.cypress(33, 11)
    # band 1's walls on its north side
    g.cypress(21, 9)
    # the south plot: the Repel inside, its gate on the south wall, off the band
    plot(g, 18, 17, 27, 21, gate=23, panel=24)
    for (k, x, y) in (("stele_family", 19, 18), ("lekythos", 21, 18), ("sarcophagus", 19, 20),
                      ("stele_palmette", 26, 18), ("stele_low", 22, 20)):
        g.piece(k, x, y)
    g.cypress(24, 18)
    g.put(FLOWERS, 21, 20, ".", "grass")
    # the south verge of the road past the band: low markers, the opening at x 30-31
    for (k, x, y) in (("stele_low", 22, 16), ("stele_low", 26, 16), ("milestone", 28, 16)):
        g.piece(k, x, y)
    for (k, x, y) in (("lekythos", 32, 16), ("stele_low", 33, 17)):
        g.piece(k, x, y)
    g.cypress(28, 17)
    g.cypress(29, 17)
    # the old mound on the lower terrace, older than the road
    g.piece("mound", 29, 19)
    g.piece("stele_low", 32, 19)


def spur(g):
    """The hill spur: the goat path, the herm's side path, the goatherd's meadow
    and the terrace orchard behind its thicket."""
    hx, hy = HERM_AT
    g.put(HERM, hx, hy, kind="herm")
    # the herm's nook: trees round it
    g.cypress(22, 7)
    g.cypress(24, 6)
    g.piece("oak", 25, 7)
    g.piece("oak", 21, 6)
    g.piece("oak", 23, 6)
    g.piece("oak", 25, 6)
    g.piece("oak", 22, 6)
    g.piece("rock", 22, 9)
    g.piece("thyme", 23, 10)
    g.piece("dry_grass", 24, 10)
    g.piece("thyme", 25, 10)
    # the orchard terrace: its wall, the steps the thicket has closed, the olives
    g.named("terrace_wall", "W", 11, 4)
    for x in range(12, 24):
        g.named("terrace_wall", "steps" if x == STEPS[0] else "run", x, 4)
    g.named("terrace_wall", "E", 24, 4)
    for x in range(12, 24, 2):                 # the top row of olives, into the border's
        g.olive(x, 0)
    for x in (12, 16, 21):
        g.olive(x, 2)
    g.piece("thyme", 15, 3)
    # the strip under the terrace wall, west of the steps: scrub
    for (k, x, y) in (("oak", 11, 5), ("thyme", 12, 5), ("oak", 13, 5), ("rock", 14, 5), ("oak", 15, 5),
                      ("dry_grass", 16, 5)):
        g.piece(k, x, y)
    # the corridor to the steps runs along y = 5 from the goat path
    for (k, x, y) in (("pebbles", 19, 5), ("dry_grass", 22, 5)):
        g.piece(k, x, y)
    # the goatherd's meadow, the hilltop's trees above it, and its east side shut
    woods(g, rect(24, 0, 33, 0) + [(24, 1), (25, 1), (33, 1), (33, 2), (23, 2), (23, 3), (24, 2), (24, 3)],
          41, phase=False)
    for (k, x, y) in (("rock", 33, 3), ("oak", 33, 4), ("boulders", 32, 5), ("oak", 33, 7),
                      ("rock", 32, 8), ("oak", 33, 9), ("pine_young", 32, 9), ("rock", 33, 10)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)
    g.cypress(30, 10)
    g.piece("oak", 28, 10)
    g.piece("oak", 29, 10)
    g.piece("oak", 31, 10)
    g.piece("oak", 32, 10)
    g.piece("rock", 32, 11)


def upper(g, slide=True, camp=True):
    """The pass: the rise's banks, the cut bank along the upper road with the
    Hollow's mouth in it, the cutting, the slide, the camp and the hillside."""
    # the rise's west bank and the scrub over its top
    for (k, x, y) in (("boulders", 33, 5), ("oak", 33, 12), ("rock", 33, 13), ("oak", 35, 7),
                      ("rock", 34, 7), ("pine_young", 36, 6), ("oak", 34, 6), ("rock", 35, 6),
                      ("oak", 36, 5), ("thyme", 34, 5), ("oak", 35, 5)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)
    # the rise's east bank, the camp's west edge
    for (k, x, y) in (("boulders", 37, 11), ("rock", 37, 13), ("oak", 37, 14), ("rock", 37, 15),
                      ("oak", 37, 16)):
        g.piece(k, x, y)
    # the cut bank along the upper road: brink, face, foot, from x = 38 to the edge
    g.named("bank_end_w", "brink", 37, 5)
    g.named("bank_end_w", "face_u", 37, 6)
    g.named("bank_end_grass", "foot_w", 37, 7)
    for x in range(38, W):
        g.named("cliff_brink", "bite" if x in (44, 50) else ("B" if x % 4 == 1 else "A"), x, 5)
        g.named("cliff", "face_u_" + fv(x, 6), x, 6)
        g.named("bank_grass", "foot_" + "ABC"[noise(x, 7, 2) % 3], x, 7)
    # the Hollow's mouth in the bank
    mx, my = MOUTH
    g.put(CAVE_TOP, mx, my - 1, "X", "mouth")
    g.put(CAVE_DOOR, mx, my, ".", "mouth")
    # the cutting: the hill pressing in on the road from both sides
    for x in range(39, 44):                                # fallen blocks narrow the road to two
        g.piece("rock", x, 8)
    for (k, x, y) in (("boulders", 38, 11), ("rock", 40, 11), ("rock", 42, 11), ("boulders", 42, 12),
                      ("rock", 41, 12), ("oak", 43, 11)):
        g.piece(k, x, y)
    # the scrub between the cutting and the camp
    for (k, x, y) in (("pine_tall", 38, 13), ("oak", 40, 13), ("rock", 40, 14), ("oak", 41, 15),
                      ("thyme", 40, 15), ("oak", 40, 16), ("pine_young", 39, 15), ("rock", 38, 16),
                      ("oak", 41, 14), ("dry_grass", 41, 16), ("oak", 42, 16), ("rock", 42, 14), ("oak", 43, 16)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)
    # the hillside above the bank: Aleppo pines and kermes oak climbing to the pass,
    # thinning to scree and boulders over the slide, where the Titans dug
    for (k, x, y) in (("pine_tall", 34, -1), ("pine_lean", 36, 0), ("pine_tall", 39, -1), ("pine_young", 41, 1),
                      ("pine_tall", 42, 1), ("pine_lean_w", 44, -1), ("pine_tall", 47, 0), ("pine_young", 49, 0),
                      ("boulders", 50, 2), ("boulders", 53, 1), ("pine_tall", 55, -1), ("pine_lean", 57, 0),
                      ("pine_young", 35, 2), ("pine_tall", 38, 2), ("oak", 40, 3), ("pine_young", 45, 2),
                      ("oak", 46, 3), ("rock", 49, 3), ("rock", 52, 3), ("pine_young", 56, 2), ("oak", 58, 3),
                      ("oak", 34, 3), ("oak", 37, 3), ("oak", 44, 3), ("rock", 54, 4), ("pine_young", 59, 1)):
        g.piece(k, x, y)
    for y in range(0, 5):
        for x in range(34, W):
            if g.fixed[y, x]:
                continue
            r = noise(x, y, 51)
            k = ("oak" if r < 30 else "pebbles" if 49 <= x <= 56 and r < 60 else "dry_grass" if r < 62
                 else "thyme" if r < 72 else None)
            if k:
                g.piece(k, x, y)
    # the road's end past the slide: the Hollow's name stone, rocks
    g.put(STELE, 58, 9, kind="sign")
    for (k, x, y) in (("rock", 58, 8), ("rock", 59, 8), ("oak", 59, 9), ("rock", 58, 10), ("rock", 59, 10)):
        g.piece(k, x, y)
    # under the road beyond the camp: the slope below the slide, shut to the edge
    for (k, x, y) in (("rock", 56, 11), ("boulders", 57, 11), ("oak", 59, 11), ("rock", 59, 12),
                      ("oak", 57, 13), ("rock", 58, 13), ("oak", 59, 13), ("rock", 57, 14),
                      ("pine_tall", 58, 14), ("oak", 57, 15), ("rock", 57, 16), ("oak", 58, 17)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)
    if slide:
        rubble_slide(g)
    if camp:
        camp_pieces(g)
    else:
        camp_traces(g)


def rubble_slide(g):
    """Beat 17's rockslide: a toppled tomb pulled down across the cutting. Two
    big heaps on each side, and the three heaps the Hammer breaks in a chain
    down the middle (objects on rubble cells)."""
    g.piece("rubble", 52, 7)
    g.piece("rubble", 54, 7)
    g.piece("rubble", 52, 10)
    g.piece("rubble", 54, 10)
    for (x, y) in HEAPS:
        g.piece("rubble_small", x, y, kind="heap")
    g.piece("rubble_small", 51, 8)
    g.piece("rubble_small", 51, 10)
    for (k, x, y) in (("boulders", 51, 3), ("rock", 53, 4), ("pebbles", 55, 4)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)


def camp_pieces(g):
    """The procession's camp: tents in an arc round the cookfire, the cart and
    its donkey, myrtle and the sacred baskets, Alethea's milestone by the road."""
    g.piece("tent", 44, 14, kind="camp")
    g.piece("tent_b", 47, 12, kind="camp")
    g.piece("tent", 51, 12, kind="camp")
    g.piece("tent_b", 54, 12, kind="camp")
    g.piece("cookfire", 49, 15, kind="camp")
    g.piece("bedrolls", 47, 15, kind="camp")
    g.piece("bedrolls", 51, 15, kind="camp")
    g.piece("myrtle", 44, 13, kind="camp")
    g.piece("myrtle", 44, 16, kind="camp")
    g.piece("baskets", 52, 16, kind="camp")
    g.piece("baskets", 45, 16, kind="camp")
    g.piece("cart", 54, 14, kind="camp")
    g.piece("milestone", 46, 11, kind="camp_milestone")
    for (k, x, y) in (("pebbles", 48, 16), ("dry_grass", 46, 16), ("pebbles", 50, 16), ("pebbles", 49, 13)):
        if not g.fixed[y, x]:
            g.piece(k, x, y, kind="camp")


def camp_traces(g):
    """The camp once the procession has gone on: trampled grass where the tents
    stood, the fire's ring of stones cold, Alethea's milestone by the road."""
    g.piece("milestone", 46, 11, kind="camp_milestone")
    for (x0, y0) in ((44, 14), (47, 12), (51, 12), (54, 12)):           # the tents' footprints
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
            x, y = x0 + dx, y0 + dy
            g.piece("dry_grass" if noise(x, y, 61) < 70 else "pebbles", x, y, kind="camp")
    for (k, x, y) in (("pebbles", 49, 15), ("dry_grass", 48, 15), ("dry_grass", 50, 15), ("pebbles", 54, 14),
                      ("dry_grass", 55, 15), ("dry_grass", 56, 14), ("pebbles", 47, 15), ("dry_grass", 51, 15),
                      ("thyme", 44, 13), ("dry_grass", 45, 16), ("pebbles", 52, 16), ("dry_grass", 49, 13)):
        g.piece(k, x, y, kind="camp")


def lower(g):
    """The lower terrace: the lips down from the camp, the family tomb a column
    drum has shut, the east meadow and its dead end, the olives above the strip."""
    # the lips: the camp's terrace edge, jumping south toward the city
    g.named("lip", "W", 44, 17)
    for x in range(45, 56):
        g.named("lip", "run", x, 17)
    g.named("lip", "E", 56, 17)
    for (k, x, y) in (("rock", 38, 17), ("oak", 39, 17), ("rock", 40, 17), ("oak", 41, 17), ("oak", 42, 17),
                      ("rock", 43, 17), ("oak", 57, 17), ("rock", 58, 17), ("oak", 59, 17),
                      ("thyme", 34, 17), ("oak", 35, 17), ("rock", 36, 17), ("oak", 37, 17)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)
    # the family tomb: a column drum fell into its gate (the Girdle, Act II)
    plot(g, 39, 19, 45, 23, gate=DRUM[0], panel=41)
    g.piece("sarcophagus", 40, 20)
    g.piece("stele_family", 44, 20)
    g.piece("stele_low", 43, 21)
    # the east meadow's dead end: a scree nook at the slope's foot (the Hard Stone)
    for (k, x, y) in (("rock", 57, 17), ("oak", 59, 17), ("boulders", 58, 18), ("rock", 57, 20),
                      ("pebbles", 56, 21), ("boulders", 58, 20), ("rock", 57, 22), ("oak", 58, 22),
                      ("rock", 59, 22), ("pine_young", 58, 23), ("oak", 59, 24), ("rock", 57, 24),
                      ("oak", 57, 23), ("rock", 59, 25), ("oak", 58, 25), ("rock", 55, 19)):
        if not g.fixed[y, x]:
            g.piece(k, x, y)
    # a milestone on the old track across the terrace (the hidden Oran Berry by it)
    g.piece("milestone", 35, 19)
    # the terrace's own dead: a sarcophagus by the track, a column drum from the
    # tomb, a pair of cypresses, a stele leaning in the grass
    g.piece("sarcophagus", 38, 21)
    g.piece("drum", 46, 22)
    g.piece("stele_palmette", 55, 21)
    g.cypress(46, 19)
    g.piece("stele_low", 28, 20)
    # olives above the strip, a ragged grove
    for (x, y) in ((19, 24), (25, 24), (28, 24), (32, 24), (37, 24), (47, 24), (49, 24), (52, 24), (55, 24)):
        if g.free(x, y, 2, 2):
            g.olive(x, y)
    for (k, x, y) in (("thyme", 31, 21), ("dry_grass", 38, 18), ("pebbles", 46, 21), ("thyme", 45, 19),
                      ("dry_grass", 55, 23), ("thyme", 26, 22), ("pebbles", 33, 18), ("dry_grass", 38, 22)):
        if g.free(x, y):
            g.piece(k, x, y)


def glade(g):
    """Hecate's glade: a crossroads shrine older than the paving, where the old
    track forked before the road was laid. Someone leaves her a cake here."""
    x, y = SHRINE
    g.put(0x130, x, y, kind="shrine")          # aethos's bronze tripod, on its marble plinth
    g.put(0x131, x, y + 1, kind="shrine")
    g.piece("stele_low", 8, 7)
    g.piece("thyme", 9, 9)
    g.piece("dry_grass", 3, 11)


def clearing(g):
    """The woods clearing west of the gate's road, its mouth choked with marble
    rubble: the Hammer's first lesson. A forgotten grave, and a Great Ball."""
    g.piece("stele_palmette", 2, 17)
    g.piece("stele_low", 5, 17)
    g.piece("dry_grass", 4, 18)
    g.piece("thyme", 5, 21)


def details(g):
    """Flowers, thyme and dry grass on the open ground, by noise; never on a cell
    a person or item uses (those are kept by the events' reservation)."""
    for y in range(H):
        for x in range(W):
            if g.fixed[y, x] or g.ground[y, x] != "grass":
                continue
            r = noise(x, y, 31)
            if y >= H - STRIP_ROWS:
                if r < 6:
                    g.ground[y, x] = "flowers"
                continue
            if r < 4:
                g.ground[y, x] = "flowers"
            elif r < 7:
                g.piece("dry_grass", x, y)
            elif r < 9:
                g.piece("thyme", x, y)


def compose(slide=True, camp=True, reserve=()):
    cat = {s["key"]: s for s in json.loads(CAT.read_text())}
    g = Grid(cat)
    ground(g)
    tombs(g)
    potters(g)
    spur(g)
    upper(g, slide=slide, camp=camp)
    lower(g)
    clearing(g)
    glade(g)
    west_and_north_woods(g)
    for (x, y) in reserve:                   # people and items stand on plain ground
        if not g.fixed[y, x]:
            g.fixed[y, x] = True
            g.walk[y, x] = "."
            g.kind[y, x] = "reserved"
    details(g)
    for (x, y) in reserve:
        if g.kind[y, x] == "reserved":
            g.fixed[y, x] = False
    g.autotile()
    return g


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
GFX = "OBJ_EVENT_GFX_ICHOR_"
PX = "Route4_Isthmus_EventScript_"
LID = "LOCALID_ROUTE4_"

# trainers: local id, gfx, x, y, facing, sight, script, trainer, mandatory
TRAINERS = [
    ("EXEKIAS", GFX + "MAN", 10, 22, "LEFT", 3, "Exekias", "TRAINER_ICHOR_EXEKIAS", True),
    ("MYRRHINE", GFX + "PRIESTESS", 24, 12, "DOWN", 4, "Myrrhine", "TRAINER_ICHOR_MYRRHINE", True),
    ("LAAS", GFX + "TITAN_GRUNT", 23, 8, "RIGHT", 2, "Laas", "TRAINER_ICHOR_GRUNT_ROUTE4_LAAS", False),
    ("MENALKAS", GFX + "GOATHERD", 30, 6, "LEFT", 2, "Menalkas", "TRAINER_ICHOR_MENALKAS", False),
    ("PHEIDIPPOS", GFX + "YOUTH_M", 41, 11, "UP", 2, "Pheidippos", "TRAINER_ICHOR_PHEIDIPPOS", True),
    ("KAPELOS", GFX + "MERCHANT", 53, 12, "DOWN", 1, "Kapelos", "TRAINER_ICHOR_KAPELOS", False),
]
# people: local id, gfx, x, y, facing, script, hide flag
PEOPLE = [
    ("KILN_WORKER", GFX + "HARVESTER", 13, 20, "RIGHT", "KilnWorker", "0"),
    ("MOURNER", GFX + "ELDER_F", 15, 12, "LEFT", "Mourner", "0"),
    ("GOAT_1", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 29, 5, "DOWN", "Goat", "0"),
    ("GOAT_2", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 31, 5, "LEFT", "Goat", "0"),
    ("ALETHEA", GFX + "ALETHEA", 46, 11, "DOWN", "Alethea", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
    ("EUDEMOS", GFX + "ELDER_M", 50, 12, "DOWN", "Eudemos", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
    ("HEALER", GFX + "HEALER", 45, 13, "DOWN", "Healer", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
    ("INITIATE_1", GFX + "PRIESTESS", 48, 15, "RIGHT", "InitiateWait", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
    ("INITIATE_2", GFX + "YOUTH_M", 49, 14, "DOWN", "InitiateDonkey", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
    ("INITIATE_3", GFX + "YOUTH_F", 50, 15, "LEFT", "InitiateSecret", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
    ("DONKEY", "OBJ_EVENT_GFX_SPECIES(ONOTIS)", 53, 15, "RIGHT", "Donkey", "FLAG_ICHOR_HIDE_PROCESSION_ROUTE4"),
]
# obstacles: local id, gfx, x, y, script, hide flag
OBSTACLES = [
    ("HEAP_1", "OBJ_EVENT_GFX_BREAKABLE_ROCK", HEAPS[0][0], HEAPS[0][1], "Heap", "FLAG_ICHOR_HIDE_ROCKSLIDE_1"),
    ("HEAP_2", "OBJ_EVENT_GFX_BREAKABLE_ROCK", HEAPS[1][0], HEAPS[1][1], "Heap", "FLAG_ICHOR_HIDE_ROCKSLIDE_2"),
    ("HEAP_3", "OBJ_EVENT_GFX_BREAKABLE_ROCK", HEAPS[2][0], HEAPS[2][1], "Heap", "FLAG_ICHOR_HIDE_ROCKSLIDE_3"),
    # a temp flag, as vanilla's breakable rocks: broken for the visit, back on the next
    ("RUBBLE", "OBJ_EVENT_GFX_BREAKABLE_ROCK", TEACH_RUBBLE[0], TEACH_RUBBLE[1], "@EventScript_RockSmash",
     "FLAG_TEMP_11"),
    ("THICKET", "OBJ_EVENT_GFX_CUTTABLE_TREE", STEPS[0], STEPS[1], "@EventScript_CutTree",
     "FLAG_ICHOR_HIDE_THICKET_ROUTE4"),
    ("DRUM", "OBJ_EVENT_GFX_PUSHABLE_BOULDER", DRUM[0], DRUM[1], "@EventScript_StrengthBoulder", "0"),
]
# items: item, x, y, flag
ITEMS = [
    ("ITEM_POTION", 16, 23, "FLAG_ICHOR_ITEM_ROUTE4_POTION"),
    ("ITEM_REPEL", 25, 19, "FLAG_ICHOR_ITEM_ROUTE4_REPEL"),
    ("ITEM_SUPER_POTION", 32, 1, "FLAG_ICHOR_ITEM_ROUTE4_SUPER_POTION"),
    ("ITEM_SUN_STONE", 19, 2, "FLAG_ICHOR_ITEM_ROUTE4_SUN_STONE"),
    ("ITEM_REVIVE", 41, 21, "FLAG_ICHOR_ITEM_ROUTE4_REVIVE"),
    ("ITEM_GREAT_BALL", 3, 18, "FLAG_ICHOR_ITEM_ROUTE4_GREAT_BALL"),
    ("ITEM_SPELL_TAG", 4, 8, "FLAG_ICHOR_ITEM_ROUTE4_SPELL_TAG"),
]
HIDDEN = [
    ("ITEM_ETHER", 16, 21, "FLAG_ICHOR_HIDDEN_ROUTE4_ETHER"),            # in the kiln's ash (the wasters' heap)
    ("ITEM_ORAN_BERRY", 36, 19, "FLAG_ICHOR_HIDDEN_ROUTE4_ORAN_BERRY"),  # by the milestone
    ("ITEM_STARDUST", 49, 16, "FLAG_ICHOR_HIDDEN_ROUTE4_STARDUST"),      # by the procession's cookfire
    ("ITEM_HARD_STONE", 56, 21, "FLAG_ICHOR_HIDDEN_ROUTE4_HARD_STONE"),  # in the scree under the slide
]
# signs: x, y, facing, script
SIGNS = [
    (10, 28, "ANY", "SouthSign"),
    (11, 12, "ANY", "TombsSign"),
    (28, 12, "ANY", "ForkSign"),
    (58, 9, "ANY", "HollowSign"),
    (HERM_AT[0], HERM_AT[1], "NORTH", "GreatHerm"),
    (15, 10, "NORTH", "KalliasPanel"),
    (SHRINE[0], SHRINE[1] + 1, "ANY", "HecateShrine"),
]
DIG = [(12, 22), (27, 2), (44, 22)]   # ICHOR_STUB_DIG: by the kilns and on the spur (daily); in the tomb (fixed)
TRIGGERS = [(TRIGGER_X, y, "RockslideScene") for y in (8, 9, 10)]
WARPS = [(MOUTH[0], MOUTH[1], "MAP_HECATES_HOLLOW", 0)]


def hollow_registered():
    groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
    return any("HecatesHollow" == m for k, v in groups.items() if k != "group_order" for m in v)


def warp_events():
    out = []
    for i, (x, y, dest, wid) in enumerate(WARPS):
        if dest == "MAP_HECATES_HOLLOW" and not hollow_registered():
            # ICHOR_STUB_HOLLOW: until the Hollow agent's map lands, the mouth warps to
            # itself (the cave gives the player straight back). Rerun this builder after
            # MAP_HECATES_HOLLOW is registered and the mouth leads into it.
            dest, wid = MAP_ID, i
        out.append({"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)})
    return out


def write_events():
    m = json.loads((MAP_DIR / "map.json").read_text())
    m["music"] = "MUS_ICHOR_ROAD"
    m["weather"] = "WEATHER_SUNNY"
    m["map_type"] = "MAP_TYPE_ROUTE"
    m["show_map_name"] = True
    m["connections"] = [{"map": "MAP_EMPORION_CITY", "offset": CITY_OFFSET, "direction": "down"}]
    objs = []
    def obj(lid, gfx, x, y, move, script, flag, ttype="TRAINER_TYPE_NONE", sight="0"):
        objs.append({"local_id": LID + lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
                     "movement_type": move, "movement_range_x": 0, "movement_range_y": 0,
                     "trainer_type": ttype, "trainer_sight_or_berry_tree_id": str(sight),
                     "script": script, "flag": flag})
    for lid, gfx, x, y, facing, sight, script, trainer, _ in TRAINERS:
        flag = "FLAG_ICHOR_HIDE_GRUNT_LAAS" if lid == "LAAS" else "0"
        obj(lid, gfx, x, y, f"MOVEMENT_TYPE_FACE_{facing}", PX + script, flag, "TRAINER_TYPE_NORMAL", sight)
    for lid, gfx, x, y, facing, script, flag in PEOPLE:
        move = "MOVEMENT_TYPE_LOOK_AROUND" if lid.startswith("GOAT") else f"MOVEMENT_TYPE_FACE_{facing}"
        obj(lid, gfx, x, y, move, PX + script, flag)
    for lid, gfx, x, y, script, flag in OBSTACLES:
        obj(lid, gfx, x, y, "MOVEMENT_TYPE_LOOK_AROUND", script[1:] if script.startswith("@") else PX + script, flag)
    for item, x, y, flag in ITEMS:
        objs.append({"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
                     "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0, "movement_range_y": 0,
                     "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": item,
                     "script": "Common_EventScript_FindItem", "flag": flag})
    m["object_events"] = objs
    m["warp_events"] = warp_events()
    m["coord_events"] = [{"type": "trigger", "x": x, "y": y, "elevation": 3, "var": "VAR_TEMP_1",
                          "var_value": "1", "script": PX + s} for x, y, s in TRIGGERS]
    bgs = [{"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": PX + s} for x, y, f, s in SIGNS]
    bgs += [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
             "script": PX + "DigSpot"} for x, y in DIG]
    bgs += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
             "quantity": 1, "underfoot": False} for item, x, y, flag in HIDDEN]
    m["bg_events"] = bgs
    (MAP_DIR / "map.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def write_city_connection():
    """Only the city's "up" connection entry is ours (BUILD.md)."""
    m = json.loads(CITY_JSON.read_text())
    conns = [c for c in (m.get("connections") or []) if c["map"] != MAP_ID]
    conns.append({"map": MAP_ID, "offset": -CITY_OFFSET, "direction": "up"})
    if conns != m.get("connections"):
        m["connections"] = conns
        CITY_JSON.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def reserved_cells():
    cells = [(x, y) for _, _, x, y, *_ in TRAINERS] + [(x, y) for _, _, x, y, *_ in PEOPLE]
    cells += [(x, y) for _, x, y, _ in ITEMS] + [(x, y) for _, x, y, _ in HIDDEN] + DIG
    cells += [(x, y) for x, y, _ in TRIGGERS]
    return cells


# ---------------------------------------------------------------------------
# The generated script block: the slide and the camp, swapped by flag
# ---------------------------------------------------------------------------
SCRIPT_BEGIN = "// --- Generated by tools/ichor/maps/route4.py from the layout. Do not edit. ---"
SCRIPT_END = "// --- End of the generated block. ---"


def diff_cells(a, b, box):
    x0, y0, x1, y1 = box
    out = []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if a.mt[y, x] != b.mt[y, x] or a.solid[y, x] != b.solid[y, x]:
                out.append((x, y, int(b.mt[y, x]), bool(b.solid[y, x])))
    return out


def script_block(g, clear, struck):
    small_cleared = g.cat["rubble_small_cleared"]["ids"][0][0]
    out = [SCRIPT_BEGIN, ""]
    for i, (x, y) in enumerate(HEAPS, 1):
        out += [f"// heap {i} broken: the road under it, white with marble chips",
                f"script {PX}HeapCell{i} {{",
                f"    setmetatile({x}, {y}, 0x{small_cleared:03X}, FALSE)",
                "    return", "}", ""]
    out += ["// FLAG_ICHOR_ROCKSLIDE_CLEARED: the whole slide gone from the road",
            f"script {PX}ClearSlide {{"]
    for x, y, mid, solid in diff_cells(g, clear, SLIDE):
        if (x, y) in HEAPS:
            mid, solid = small_cleared, False
        out.append(f"    setmetatile({x}, {y}, 0x{mid:03X}, {'TRUE' if solid else 'FALSE'})")
    out += ["    return", "}", "",
            "// FLAG_ICHOR_HIDE_PROCESSION_ROUTE4: the camp struck, the ground trampled",
            f"script {PX}StrikeCamp {{"]
    for x, y, mid, solid in diff_cells(g, struck, CAMP):
        out.append(f"    setmetatile({x}, {y}, 0x{mid:03X}, {'TRUE' if solid else 'FALSE'})")
    out += ["    return", "}", "", SCRIPT_END]
    return "\n".join(out)


def splice_script(g, clear, struck):
    path = MAP_DIR / "scripts.pory"
    text = path.read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"route4: {path} needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    new = text[:a] + script_block(g, clear, struck) + text[b + len(SCRIPT_END):]
    if new != text:
        path.write_text(new)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def blockdata(g):
    out = np.zeros((H, W), np.uint16)
    solid = g.solid
    for y in range(H):
        for x in range(W):
            out[y, x] = (int(g.mt[y, x]) & 0x3FF) | (int(solid[y, x]) << 10) | (3 << 12)
    return out


def border():
    return np.array([OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]], np.uint16)


def write_layout(g):
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    blockdata(g).astype("<u2").tofile(LAYOUT_DIR / "map.bin")
    border().astype("<u2").tofile(LAYOUT_DIR / "border.bin")
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
JUMP = {"MB_JUMP_SOUTH": (0, 1), "MB_JUMP_NORTH": (0, -1), "MB_JUMP_EAST": (1, 0), "MB_JUMP_WEST": (-1, 0)}


def reach(g, start, blocked=frozenset(), opened=frozenset()):
    """Cells the player can walk to from start. Ledges jump one way only.
    blocked: extra cells to treat as solid (people, obstacles, grass).
    opened: solid cells to treat as open (an obstacle's cell once it is gone)."""
    solid = g.solid
    def open_(x, y):
        if (x, y) in opened:
            return True
        return 0 <= x < W and 0 <= y < H and not solid[y, x] and (x, y) not in blocked
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            b = behavior(int(g.mt[ny, nx]))
            if b in JUMP and g.walk[ny, nx] == "J":
                if JUMP[b] == (dx, dy):
                    lx, ly = nx + dx, ny + dy
                    if open_(lx, ly) and (lx, ly) not in seen:
                        seen.add((lx, ly))
                        q.append((lx, ly))
                continue
            if open_(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append((nx, ny))
    return seen


def sight_cells(x, y, facing, n):
    dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[facing]
    return {(x + dx * i, y + dy * i) for i in range(1, n + 1)}


def check(g):
    problems = []
    solid = g.solid
    start = (8, H - 1)
    goal = (MOUTH[0], MOUTH[1] + 1)
    people = {(x, y) for _, _, x, y, *_ in TRAINERS} | {(x, y) for _, _, x, y, *_ in PEOPLE}
    obstacles = {(x, y) for _, _, x, y, *_ in OBSTACLES}
    balls = {(x, y) for _, x, y, _ in ITEMS}
    heaps = set(HEAPS)
    things = people | obstacles | balls
    # the seam, and no other way off the map's edges (where a player can get to)
    anywhere = reach(g, start, opened=obstacles | heaps)
    for x in range(W):
        if (not solid[H - 1, x]) != (x in GATE):
            problems.append(f"city seam: column {x} is {'open' if not solid[H - 1, x] else 'shut'}")
        if (x, 0) in anywhere:
            problems.append(f"north edge: column {x} can be walked to")
    for y in range(H):
        for x in (0, W - 1):
            if (x, y) in anywhere:
                problems.append(f"{'west' if x == 0 else 'east'} edge: row {y} can be walked to")
    for y in range(H - STRIP_ROWS, H):
        for x in range(W):
            if g.mt[y, x] >= 0x200:
                problems.append(f"skiron metatile 0x{g.mt[y, x]:03X} at ({x},{y}), inside the city seam's strip")
    # Kleon's run off the gate (beat 16) and the player's way in: open, and no events
    for y in range(H - 3, H):
        for x in GATE:
            if solid[y, x] or (x, y) in things:
                problems.append(f"beat 16: ({x},{y}) by the seam must stay open and empty")
    # the shapes the tileset has
    for k, v in g.missing.items():
        if v:
            problems.append(f"{k} shapes the tileset lacks: {sorted(v)[:8]}")
    # the road: shut by the slide, open once its heaps are gone
    shut = reach(g, start, blocked=things)
    if goal in shut:
        problems.append("the Hollow's mouth can be reached without breaking the slide")
    full = reach(g, start, blocked=things - heaps, opened=heaps)
    if goal not in full:
        problems.append("the Hollow's mouth can't be reached even with the slide broken")
    # each heap is needed: the slide is a chain
    for h in HEAPS:
        if goal in reach(g, start, blocked=(things - heaps) | {h}, opened=heaps - {h}):
            problems.append(f"the heap at {h} can be walked round")
    # forced bands
    bands = {"band 1": set(rect(19, 11, 21, 16)), "band 2": set(rect(34, 10, 36, 13))}
    for name, cells in bands.items():
        g_cells = {c for c in cells if g.walk[c[1], c[0]] == "G"}
        if goal in reach(g, start, blocked=(things - heaps) | g_cells, opened=heaps):
            problems.append(f"{name} can be walked round")
    # trainers: the mandatory ones cut the way on, the optional ones don't
    for lid, gfx, x, y, facing, n, script, trainer, mandatory in TRAINERS:
        sc = sight_cells(x, y, facing, n)
        for c in sc:
            if mandatory and solid[c[1], c[0]]:
                problems.append(f"{lid}: sight cell {c} is solid")
        cut = goal not in reach(g, start, blocked=(things - heaps) | sc | {(x, y)}, opened=heaps)
        if mandatory and not cut:
            problems.append(f"{lid} is meant to be mandatory but the road goes round his sight line")
        if not mandatory and cut:
            problems.append(f"{lid} is meant to be optional but blocks the road")
    # every person, item and sign can be reached and spoken to
    everything_open = reach(g, start, blocked=people - {(x, y) for _, _, x, y, *_ in TRAINERS},
                            opened=obstacles)
    def readable(x, y, pool):
        return any((x + dx, y + dy) in pool for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    free_pool = reach(g, start, blocked=things - heaps, opened=heaps)
    for lid, gfx, x, y, *_ in TRAINERS + PEOPLE:
        if not readable(x, y, free_pool | everything_open):
            problems.append(f"{lid} at ({x},{y}) can't be talked to")
    for lid, gfx, x, y, *_ in OBSTACLES:
        if not readable(x, y, free_pool):
            problems.append(f"obstacle {lid} at ({x},{y}) can't be reached")
    for item, x, y, flag in ITEMS:
        if not readable(x, y, everything_open):
            problems.append(f"{item} at ({x},{y}) can't be reached")
    for item, x, y, flag in HIDDEN:
        if (x, y) not in everything_open and not readable(x, y, everything_open):
            problems.append(f"hidden {item} at ({x},{y}) can't be reached")
    for x, y, f, s in SIGNS:
        if not readable(x, y, everything_open):
            problems.append(f"sign {s} at ({x},{y}) can't be read")
        if not solid[y, x]:
            problems.append(f"sign {s} at ({x},{y}) stands on open ground")
    for x, y in DIG:
        if (x, y) not in everything_open:
            problems.append(f"dig spot ({x},{y}) can't be stood on")
    # what the relics open stays shut without them
    gated = {"the orchard (Sickle)": (19, 2),"the family tomb (Girdle)": (41, 21), "the clearing (Hammer)": (3, 18)}
    for what, cell in gated.items():
        if readable(*cell, free_pool):
            problems.append(f"{what} is open without its relic")
    # the herm's landing tile
    hx, hy = HERM_AT
    if solid[hy + 1, hx] or (hx, hy + 1) not in everything_open:
        problems.append("the great herm's landing tile is blocked")
    # the terrace lips drop toward the city only: from below, the camp is out of reach
    below = reach(g, (36, 20), blocked=(things - heaps) | bands["band 2"])
    if any(c in below for c in rect(44, 12, 56, 16)):
        problems.append("the camp can be climbed to from the lower terrace")
    above = reach(g, (49, 14), blocked=things - heaps)
    if (36, 20) not in above:
        problems.append("the lips don't drop from the camp to the lower terrace")
    # the warp
    for w in warp_events():
        if behavior(int(g.mt[w["y"], w["x"]])) != "MB_NON_ANIMATED_DOOR":
            problems.append(f"warp ({w['x']},{w['y']}) is not on a door")
    # triggers stand on the road
    for x, y, _ in TRIGGERS:
        if solid[y, x]:
            problems.append(f"trigger ({x},{y}) is on a solid cell")
    return problems, full


def walk_text(g, r):
    rows = ["    " + "".join(str(x % 10) for x in range(W))]
    solid = g.solid
    for y in range(H):
        rows.append(f"{y:3d} " + "".join(
            "G" if g.walk[y, x] == "G" and (x, y) in r else
            "J" if g.walk[y, x] == "J" else
            "#" if solid[y, x] else "." if (x, y) in r else "?" for x in range(W)))
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

def renderer(secondary="gTileset_Skiron"):
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R, R.Renderer(R.Tileset(R.resolve_tileset("gTileset_Aethos", syms)),
                         R.Tileset(R.resolve_tileset(secondary, syms)))


FRAME = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}
MISC = {"OBJ_EVENT_GFX_ITEM_BALL": "ball_poke","OBJ_EVENT_GFX_BREAKABLE_ROCK": "breakable_rock",
        "OBJ_EVENT_GFX_CUTTABLE_TREE": "cuttable_tree", "OBJ_EVENT_GFX_PUSHABLE_BOULDER": "pushable_boulder"}


def sprite(gfx, facing):
    from PIL import Image
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
        name = gfx[len("OBJ_EVENT_GFX_SPECIES("):-1]
        stub = (ROOT / "include/constants/ichor_species_stubs.h").read_text()
        mm = re.search(rf"SPECIES_{name}\s+SPECIES_(\w+)", stub)
        sp = (mm.group(1) if mm else name).lower()
        sheet = Image.open(ROOT / f"graphics/pokemon/{sp}/overworld.png")
        fw = sheet.height
        frame = FRAME[facing]
    elif gfx in MISC:
        sheet = Image.open(ROOT / f"graphics/object_events/pics/misc/{MISC[gfx]}.png")
        fw, frame = 16, 0
    else:
        sheet = Image.open(ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png")
        fw, frame = 16, FRAME[facing]
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


def people(im, pad=0, camp=True):
    def paste(gfx, x, y, facing):
        try:
            spr, fw, fh = sprite(gfx, facing)
        except FileNotFoundError:
            return
        im.paste(spr, ((x + pad) * 16 + 8 - fw // 2, (y + pad) * 16 + 16 - fh), spr)
    for lid, gfx, x, y, facing, *_ in TRAINERS:
        paste(gfx, x, y, facing)
    for lid, gfx, x, y, facing, script, flag in PEOPLE:
        if camp or flag == "0":
            paste(gfx, x, y, facing)
    for lid, gfx, x, y, script, flag in OBSTACLES:
        paste(gfx, x, y, "DOWN")
    for item, x, y, flag in ITEMS:
        paste("OBJ_EVENT_GFX_ITEM_BALL", x, y, "DOWN")
    return im


# Where the player stands for each 15x10 review view, along the route.
VIEWS = [
    ("01_gate", 8, 27), ("02_kilns", 10, 20), ("03_corner", 12, 14), ("04_band1", 19, 14),
    ("05_myrrhine", 25, 13), ("06_herm", 25, 8), ("07_spur_top", 26, 3), ("08_orchard", 18, 4),
    ("09_rise", 33, 11), ("10_cutting", 41, 9), ("11_camp", 48, 12), ("12_slide", 53, 9),
    ("13_lower_west", 30, 19), ("14_tomb", 42, 21), ("15_lower_east", 52, 20), ("16_clearing", 5, 19), ("17_glade", 7, 10),
]


def render(out_dir, g, struck, clear):
    from PIL import Image, ImageDraw
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    R, r = renderer()
    blocks = np.fromfile(LAYOUT_DIR / "map.bin", "<u2")
    flat = R.render_blocks(r, blocks, W)
    whole = people(flat.convert("RGBA"))
    whole.convert("RGB").resize((W * 32, H * 32), Image.NEAREST).save(out_dir / "route4.png")
    # after beat 17: the slide gone, the camp struck
    after = blockdata(clear).reshape(-1).copy()
    for x, y, mid, solid in diff_cells(g, struck, CAMP):
        after[y * W + x] = (mid & 0x3FF) | (int(solid) << 10) | (3 << 12)
    R.render_blocks(r, after, W).convert("RGB").resize((W * 32, H * 32), Image.NEAREST).save(out_dir / "route4_after.png")
    # collision overlay with events
    m = json.loads((MAP_DIR / "map.json").read_text())
    im = flat.convert("RGBA").resize((W * 32, H * 32), Image.NEAREST)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = 32
    for y in range(H):
        for x in range(W):
            b = blocks[y * W + x]
            beh = behavior(int(b) & 0x3FF)
            if beh in JUMP:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 80, 255, 90))
            elif b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif beh == "MB_TALL_GRASS":
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 255, 0, 50))
    for o in m["object_events"]:
        col = (255, 255, 0, 255) if o["trainer_type"] == "TRAINER_TYPE_NONE" else (255, 128, 0, 255)
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=col, width=3)
    for lid, gfx, x, y, facing, n, *_ in TRAINERS:
        for (sx, sy) in sight_cells(x, y, facing, n):
            d.rectangle([sx * c + 10, sy * c + 10, sx * c + c - 11, sy * c + c - 11], fill=(255, 128, 0, 160))
    for w_ in m["warp_events"]:
        d.rectangle([w_["x"] * c + 3, w_["y"] * c + 3, w_["x"] * c + c - 4, w_["y"] * c + c - 4],
                    outline=(0, 255, 255, 255), width=3)
    for e in m["coord_events"]:
        d.rectangle([e["x"] * c + 8, e["y"] * c + 8, e["x"] * c + c - 9, e["y"] * c + c - 9],
                    outline=(255, 0, 255, 255), width=2)
    for b in m["bg_events"]:
        col = (255, 120, 255, 255) if b["type"] == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 4, b["y"] * c + 4, b["x"] * c + c - 5, b["y"] * c + c - 5], fill=col, width=3)
        d.line([b["x"] * c + c - 5, b["y"] * c + 4, b["x"] * c + 4, b["y"] * c + c - 5], fill=col, width=3)
    Image.alpha_composite(im, ov).convert("RGB").save(out_dir / "route4_walk.png")
    # the 15x10 screens along the route, with the border (and the city) past the edges
    pad = 8
    city = city_rows(pad)
    bw, bh = W + 2 * pad, H + 2 * pad
    bord = border()
    big = np.zeros((bh, bw), np.uint16)
    for y in range(bh):
        for x in range(bw):
            big[y, x] = bord[((x - pad) % 2) + 2 * ((y - pad) % 2)]
    big[pad:pad + H, pad:pad + W] = blocks.reshape(H, W)
    cw = min(city.shape[1], W + pad)
    big[pad + H:pad + H + pad, pad:pad + cw] = city[:, :cw]
    padded = people(R.render_blocks(r, big.reshape(-1), bw).convert("RGBA"), pad).convert("RGB")
    views = []
    for name, px, py in VIEWS:
        x0, y0 = (px - 7 + pad) * 16, (py - 4 + pad) * 16 - 8
        v = padded.crop((x0, y0, x0 + 240, y0 + 160))
        v.resize((480, 320), Image.NEAREST).save(out_dir / f"view_{name}.png")
        views.append((name, v))
    cols = 4
    rows = (len(views) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 248 + 8, rows * 178 + 8), (24, 24, 32))
    sd = ImageDraw.Draw(sheet)
    for i, (name, v) in enumerate(views):
        x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
        sheet.paste(v, (x, y + 10))
        sd.text((x, y - 2), name, fill=(230, 230, 200))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / "route4_screens.png")
    # the seam from both sides: Route 4 over the city's top rows, drawn with each
    # map's tilesets the way the game draws a connected neighbour
    seam(out_dir, R, r, blocks)


def city_rows(n):
    """The city's top n rows (x 0-47), as Route 4's camera would show them."""
    lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    cl = next(l for l in lay["layouts"] if l.get("id") == "LAYOUT_EMPORION_CITY")
    cb = np.fromfile(ROOT / cl["blockdata_filepath"], "<u2").reshape(cl["height"], cl["width"])
    return cb[:n, :]


def seam(out_dir, R, r, blocks):
    """Two strips: standing at Route 4's foot (its last 10 rows over the city's
    first 5, all in aethos + skiron), and standing at the city's gate (Route 4's
    last 5 rows over the city's first 10, in aethos + emporion). Those are the
    rows each camera can show across the seam."""
    from PIL import Image
    city = city_rows(10)
    cw = 30
    r4 = blocks.reshape(H, W)
    _, rc = renderer("gTileset_Emporion")
    a = R.render_blocks(r, np.vstack([r4[H - 10:, :cw], city[:5, :cw]]).reshape(-1), cw).convert("RGB")
    b = R.render_blocks(rc, np.vstack([r4[H - 5:, :cw], city[:10, :cw]]).reshape(-1), cw).convert("RGB")
    out = Image.new("RGB", (a.width * 2 + 8, a.height), (24, 24, 32))
    out.paste(a, (0, 0))
    out.paste(b, (a.width + 8, 0))
    out.resize((out.width * 2, out.height * 2), Image.NEAREST).save(out_dir / "route4_seam.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    res = reserved_cells()
    g = compose(reserve=res)
    clear = compose(slide=False, reserve=res)
    struck = compose(camp=False, reserve=res)
    write_layout(g)
    write_events()
    write_city_connection()
    splice_script(g, clear, struck)
    problems, r = check(g)
    if args.walk:
        print(walk_text(g, r))
    if args.render:
        render(args.render, g, struck, clear)
    for p in problems:
        print("PROBLEM:", p)
    print(f"route4: {W}x{H}, {len(TRAINERS)} trainers, {len(PEOPLE)} people, {len(ITEMS)} items, "
          f"{len(HIDDEN)} hidden, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
