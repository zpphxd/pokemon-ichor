#!/usr/bin/env python3
"""Build Route 1 and the Kronion Hill summit: layouts, borders and events.

Both maps are drawn below as ASCII grids on gTileset_Aethos + gTileset_Kalliste,
with the interior olives listed as anchors and stamped on top. This script
auto-tiles them (path edges, olive crowns and their tips, beach and surf, wall
and terrace ends), sets collision and elevation for every cell, places the
Kronion ruins from the kalliste catalog, and writes:

  data/layouts/KallisteRoute1/{map,border}.bin
  data/layouts/KallisteRoute1_KronionHill/{map,border}.bin
  the two layouts' entries in data/layouts/layouts.json (edited in place)
  the events and connections in data/maps/<Map>/map.json

Review images go to build/render/: each map plain at 2x, a copy with collision
tinted red and every event marked, and a sheet of GBA-screen crops (15x10
tiles) along the player's route.

Usage: /usr/bin/python3 tools/ichor/maps/route1.py [--no-render]

Ground legend (one character per metatile):
  .  grass       :  grass in deep shade       '  grass under a terrace lip
  ,  tall grass (wild encounters)             *  red anemones
  =  limestone path                           d  sand (beach edges automatic)
  ~  sea         R  boulder in the sea        B  boulder
  O  olive tree (2x2 blocks; crown tips are added above automatically)
  C  cypress (1x2)
  W  dry-stone wall with a whitewashed cap (kalliste; ends and corners automatic)
  T  terrace retaining wall (kalliste)   s  steps through it   j  its jump-south ledge
  _  low terrace lip, jump south (aethos ledge)
  H  roadside herm      S  marble stele
  #  ruins placed in code on stylobate slabs
  a b k  the carter's load: stacked amphorae (2 cells) and fish crates
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CATALOG = ROOT / "build/kalliste/catalog.json"
LAYOUTS = ROOT / "data/layouts/layouts.json"
RENDER = ROOT / "build/render"

PRIMARY = "gTileset_Aethos"
SECONDARY = "gTileset_Kalliste"

# --- aethos metatiles (General's ids, see design/phase1/TILES_aethos.md) ---
GRASS, SHADE, LIP_GRASS, TALL, FLOWERS, BOULDER = 0x001, 0x01C, 0x002, 0x00D, 0x004, 0x0E0
HERM, STELE = 0x01B, 0x003
SEA, SEA_ROCK = 0x170, 0x18C
PATH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
        "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
# Sand meeting the sea (the sand-island set: the edge names say where the water is)
SURF = {"TL": 0x11B, "T": 0x11C, "TR": 0x11D, "L": 0x123, "R": 0x125,
        "BL": 0x12B, "B": 0x12C, "BR": 0x12D,
        "dNW": 0x13D, "dNE": 0x13E, "dSW": 0x145, "dSE": 0x146}
SURF_WALKABLE = {0x11C, 0x13D, 0x13E}      # vanilla treats the rest as water
# Sand meeting grass
DUNE = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122,
        "BL": 0x128, "B": 0x129, "BR": 0x12A}
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOTTOM = (0x1E4, 0x1E5)          # nothing below
OLIVE_BOTTOM_TIP = (0x1DC, 0x1DD)      # another olive's crown tip below
OLIVE_TIP = {"grass": (0x1CE, 0x1CF), "tall": (0x1C6, 0x1C7)}
CYPRESS_TOP, CYPRESS_TOP_TALL, CYPRESS_BOTTOM = 0x00E, 0x025, 0x016
LEDGE, LEDGE_LEFT, LEDGE_RIGHT = 0x087, 0x0D5, 0x0D6


# Each map.bin cell: metatile | collision << 10 | elevation << 12. Vanilla's
# conventions: ground is elevation 3; walls, trees and ledges are collision 1
# at elevation 0; the sea is elevation 1 (surfable later), its rocks collision 1.
def walk(mid):
    return mid | (3 << 12)


def block(mid):
    return mid | (1 << 10)


def water(mid):
    return mid | (1 << 12)


def load_catalog():
    """build/kalliste/catalog.json, regenerated if missing or stale.

    Packing assigns the metatile ids; only the catalog is written (no tileset
    sources, no compile), so this never touches the Tilesets stream's files.
    """
    cat = json.loads(CATALOG.read_text()) if CATALOG.exists() else []
    if not cat or any(s.get("ids") is None for s in cat):
        sys.path.insert(0, str(ROOT / "tools/ichor/art"))
        import kalliste_build  # noqa: E402
        secs = kalliste_build.sections()
        kalliste_build.pack([(kalliste_build.SECTION_ROWS[n], ss) for n, ss in secs])
        kalliste_build.catalog(secs)
        cat = json.loads(CATALOG.read_text())
    return {s["key"]: s for s in cat}


def noise(x, y, seed, scale=3.0):
    """Smooth value noise in [-1, 1]: a hashed lattice every `scale` cells, blended."""
    def lattice(i, j):
        h = (i * 374761393 + j * 668265263 + seed * 2147483647) & 0xFFFFFFFF
        h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
        return ((h ^ (h >> 16)) & 0xFFFF) / 32767.5 - 1.0
    fx, fy = x / scale, y / scale
    i, j = int(fx // 1), int(fy // 1)
    tx, ty = fx - i, fy - j
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a = lattice(i, j) + (lattice(i + 1, j) - lattice(i, j)) * tx
    b = lattice(i, j + 1) + (lattice(i + 1, j + 1) - lattice(i, j + 1)) * tx
    return a + (b - a) * ty


BLOCKING = "OCP#WTsjHS=~dRB_abk"


class Grid:
    def __init__(self, rows, name, olives=(), cypresses=(), pines=(), sea_west=False):
        self.name = name
        self.sea_west = sea_west          # the sea continues past the west edge
        self.chars = [list(r) for r in rows]
        self.h = len(rows)
        self.w = len(rows[0])
        bad = [i for i, r in enumerate(rows) if len(r) != self.w]
        if bad:
            sys.exit(f"{name}: rows {bad} are not {self.w} wide")
        for kind, anchors, size in (("O", olives, 2), ("P", pines, 2), ("C", cypresses, 1)):
            for (x, y) in anchors:
                for cy in (y, y + 1):
                    for cx in range(x, x + size):
                        if self.chars[cy][cx] in BLOCKING:
                            sys.exit(f"{name}: '{kind}' anchor ({x},{y}) lands on '{self.chars[cy][cx]}' at ({cx},{cy})")
                        self.chars[cy][cx] = kind
        self.fill_woods()
        self.cells = np.zeros((self.h, self.w), np.uint32)
        self.done = np.zeros((self.h, self.w), bool)

    def fill_woods(self, seed=3):
        """Fill '%' (impassable woods) with a mix of olives, stone pines and cypresses.

        Greedy from the top left, with a hashed choice per spot, so the woods come
        out in staggered, mixed depth instead of a grid of identical crowns.
        Leftover single cells become boulders, so the woods never leak."""
        def pct(x, y, salt):
            return (noise(x * 7.3 + salt, y * 5.1 - salt, seed, 1.0) + 1) * 50
        free = lambda x, y: self.ch(x, y) == "%"
        for y in range(self.h):
            for x in range(self.w):
                if not free(x, y):
                    continue
                square = free(x + 1, y) and free(x, y + 1) and free(x + 1, y + 1)
                pair = free(x, y + 1)
                r = pct(x, y, 1)
                if square and not (pair and r < 14):
                    kind = "P" if pct(x, y, 2) < 16 else "O"
                    for cx, cy in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)):
                        self.chars[cy][cx] = kind
                elif pair:
                    self.chars[y][x] = self.chars[y + 1][x] = "C"
                else:
                    self.chars[y][x] = "B"

    def roughen(self, protect, seed=7):
        """Break the straight edges of the drawn tall-grass patches with smooth noise:
        edge cells may thin out, grass beside a patch may grow a tuft. Never on
        event cells, so trainers, items and signs keep their ground."""
        src = [r[:] for r in self.chars]
        def near(x, y):
            return any(0 <= x + dx < self.w and 0 <= y + dy < self.h and src[y + dy][x + dx] == ","
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in protect:
                    continue
                n = noise(x, y, seed)
                c = src[y][x]
                edge = c == "," and any(0 <= x + dx < self.w and 0 <= y + dy < self.h and src[y + dy][x + dx] == "."
                                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if edge and n < -0.3:
                    self.chars[y][x] = "."
                elif c == "." and near(x, y) and n > 0.35:
                    self.chars[y][x] = ","

    def ascii(self):
        return "\n".join("".join(r) for r in self.chars)

    def ch(self, x, y, default=None):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.chars[y][x]
        return default

    def put(self, x, y, value):
        self.cells[y, x] = value
        self.done[y, x] = True

    # --- auto-tiling ---------------------------------------------------
    def trees(self):
        claimed = np.zeros((self.h, self.w), bool)
        tops = []
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "O" or claimed[y, x]:
                    continue
                cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                if any(self.ch(cx, cy) != "O" or claimed[cy, cx] for cx, cy in cells):
                    sys.exit(f"{self.name}: olive at ({x},{y}) is not a free 2x2 block\n{self.ascii()}")
                for cx, cy in cells:
                    claimed[cy, cx] = True
                tops.append((x, y))
        top_set = set(tops)
        for x, y in tops:
            self.put(x, y, block(OLIVE_TOP[0]))
            self.put(x + 1, y, block(OLIVE_TOP[1]))
            pair = OLIVE_BOTTOM_TIP if (x, y + 2) in top_set else OLIVE_BOTTOM
            self.put(x, y + 1, block(pair[0]))
            self.put(x + 1, y + 1, block(pair[1]))
        # Crown tips poke into the walkable cell above a tree (top layer).
        for x, y in tops:
            for i in (0, 1):
                ax, ay = x + i, y - 1
                if ay < 0 or self.ch(ax, ay) not in (".", ","):
                    continue
                tip = OLIVE_TIP["tall" if self.ch(ax, ay) == "," else "grass"][i]
                self.put(ax, ay, walk(tip))

    def pines(self):
        """Stone pines (General's secret-base tree), 2x2, no crown tip."""
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "P" or self.done[y, x]:
                    continue
                for i, mid in enumerate((0x01E, 0x01F, 0x026, 0x027)):
                    self.put(x + i % 2, y + i // 2, block(mid))

    def cypresses(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "C" or self.done[y, x]:
                    continue
                if self.ch(x, y + 1) != "C" or self.done[y + 1, x]:
                    sys.exit(f"{self.name}: cypress at ({x},{y}) has no lower half")
                top = CYPRESS_TOP_TALL if self.ch(x, y - 1) == "," else CYPRESS_TOP
                self.put(x, y, block(top))
                self.put(x, y + 1, block(CYPRESS_BOTTOM))

    def is_path(self, x, y, fx, fy):
        """Path test; off the map edge the road continues (seams and connections)."""
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.chars[y][x] == "="
        return self.chars[fy][fx] == "="

    def paths(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "=":
                    continue
                n = self.is_path(x, y - 1, x, y)
                s = self.is_path(x, y + 1, x, y)
                w = self.is_path(x - 1, y, x, y)
                e = self.is_path(x + 1, y, x, y)
                key = ("T" if not n else "B" if not s else "") + ("L" if not w else "R" if not e else "")
                self.put(x, y, walk(PATH[key or "C"]))

    def is_water(self, x, y):
        if x < 0:
            return self.sea_west and 0 <= y < self.h
        return self.ch(x, y) in ("~", "R")

    def is_sand(self, x, y):
        return self.ch(x, y) == "d"

    def sea(self):
        for y in range(self.h):
            for x in range(self.w):
                c = self.chars[y][x]
                if c == "~":
                    self.put(x, y, water(SEA))
                elif c == "R":
                    self.put(x, y, water(SEA_ROCK) | (1 << 10))
                elif c == "d":
                    self.put(x, y, self.sand_cell(x, y))

    def sand_cell(self, x, y):
        def edge(test, table, center):
            n, s, w, e = test(x, y - 1), test(x, y + 1), test(x - 1, y), test(x + 1, y)
            for key, hit in (("TL", n and w), ("TR", n and e), ("BL", s and w), ("BR", s and e),
                             ("T", n), ("B", s), ("L", w), ("R", e)):
                if hit:
                    return table[key]
            return center
        wet = edge(self.is_water, SURF, None)
        if wet is None:
            for key, (dx, dy) in (("dNW", (-1, -1)), ("dNE", (1, -1)), ("dSW", (-1, 1)), ("dSE", (1, 1))):
                if self.is_water(x + dx, y + dy):
                    wet = SURF[key]
                    break
        if wet is not None:
            return walk(wet) if wet in SURF_WALKABLE else water(wet)
        dry = lambda cx, cy: not self.is_sand(cx, cy) and not self.is_water(cx, cy) and self.ch(cx, cy) is not None
        return walk(edge(dry, DUNE, DUNE["C"]))

    def walls(self, cat):
        ids = cat["wall_drystone"]["ids"]
        isw = lambda x, y: self.ch(x, y) == "W"
        for y in range(self.h):
            for x in range(self.w):
                if not isw(x, y):
                    continue
                n, s, w, e = isw(x, y - 1), isw(x, y + 1), isw(x - 1, y), isw(x + 1, y)
                if (w or e) and s and not n:
                    mid = ids[1][2] if e and not w else ids[1][3]      # NW / NE corner
                elif w or e:
                    if not w:
                        mid = ids[0][0]                               # west end (or SW corner)
                    elif not e:
                        mid = ids[0][3]                               # east end (or SE corner)
                    else:
                        mid = ids[0][1 + x % 2]
                elif n and s:
                    mid = ids[1][0]
                elif s:
                    mid = ids[1][1]                                   # north end
                else:
                    mid = ids[0][4]                                   # pier / south end
                self.put(x, y, block(mid))

    def terraces(self, cat):
        ids = cat["terrace"]["ids"]
        band = lambda x, y: self.ch(x, y) in ("T", "s", "j")
        for y in range(self.h):
            for x in range(self.w):
                c = self.chars[y][x]
                if c == "s":
                    self.put(x, y, walk(ids[0][3]))
                elif c == "j":
                    self.put(x, y, block(ids[1][1 + x % 2]))
                elif c == "T":
                    if not band(x - 1, y):
                        mid = ids[0][0]
                    elif not band(x + 1, y):
                        mid = ids[0][4]
                    else:
                        mid = ids[0][1 + x % 2]
                    self.put(x, y, block(mid))

    def ledges(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "_":
                    continue
                left = self.ch(x - 1, y) != "_"
                right = self.ch(x + 1, y) != "_"
                mid = LEDGE_LEFT if left else LEDGE_RIGHT if right else LEDGE
                self.put(x, y, block(mid))

    def simple(self, cat):
        quay = cat["quay_nets"]["ids"]
        table = {
            ".": walk(GRASS), ":": walk(SHADE), "'": walk(LIP_GRASS), ",": walk(TALL),
            "*": walk(FLOWERS), "B": block(BOULDER), "H": block(HERM), "S": block(STELE),
            "a": block(quay[1][0]), "b": block(quay[1][1]), "k": block(quay[1][2]),
        }
        for y in range(self.h):
            for x in range(self.w):
                if self.done[y, x]:
                    continue
                c = self.chars[y][x]
                if c in table:
                    self.put(x, y, table[c])

    def build(self, cat):
        self.trees()
        self.pines()
        self.cypresses()
        self.paths()
        self.sea()
        self.walls(cat)
        self.terraces(cat)
        self.ledges()
        self.simple(cat)

    def place(self, cat, key, x, y, cx=0, cy=0, w=1, h=1):
        """Place cells of a kalliste structure, collision from its walk grid."""
        s = cat[key]
        for j in range(h):
            for i in range(w):
                mid = s["ids"][cy + j][cx + i]
                code = s["walk"][cy + j][cx + i]
                self.put(x + i, y + j, walk(mid) if code in ".TD" else block(mid))

    def ground(self, x, y, c):
        """Hand a placed cell back to the ground pass (grass growing over ruins)."""
        self.chars[y][x] = c
        self.done[y, x] = False

    def slabs(self, cat, x0, y0, x1, y1):
        """A patch of Kronion stylobate with its edges (south row is the step face)."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                cx = 0 if x == x0 else 2 if x == x1 else 1
                cy = 0 if y == y0 else 2 if y == y1 else 1
                self.place(cat, "stylobate", x, y, cx, cy)

    def check(self):
        missing = [(x, y, self.chars[y][x]) for y in range(self.h) for x in range(self.w) if not self.done[y, x]]
        if missing:
            sys.exit(f"{self.name}: cells left untiled: {missing[:12]}")

    def solid(self, x, y):
        """Impassable on foot: collision set, or not ground level (the sea)."""
        v = int(self.cells[y, x])
        return bool(v >> 10 & 3) or (v >> 12) != 3

    def blocks(self):
        return self.cells.astype("<u2")


# ---------------------------------------------------------------------------
# Route 1: Elaia (south) to Akti (north), along Kalliste's west shore. 30 x 64.
# Road seams at x=10-13 on the top and bottom rows; the Kronion Hill spur
# leaves the east edge at y=18-19. The border is open sea.
#
# The walk north, screen by screen:
#   leaving Elaia between olive groves; the carter resting by her load
#   the shepherd's meadow, a lone olive, Wooloo grazing; a terrace lip above
#   Phyllis's grove: the road narrows between the trees
#   the big olive in its walled garden; the bee terraces climbing east
#   the fork: a herm, a Lakonian drilling, a fallen column by the spur
#   the flock in the wall gap; then the cove, the first sight of the sea
# ---------------------------------------------------------------------------
ROUTE1 = [
    # 0         1         2
    # 012345678901234567890123456789
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 0  north seam to Akti
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 1
    "%%%%......===.C..,%%%%%%%%%%%%",  # 2  cypresses flag the way to town
    "%%%%dd,...===.C,,,%%%%%%%%%%%%",  # 3
    "dddddd,,..===...,,,,..%%%%%%%%",  # 4  the cove: first sight of the sea
    "~~~ddd,,.===..,,,,,,..%%%%%%%%",  # 5
    "~~~~dd,..===..,,,,*.,,%%%%%%%%",  # 6
    "~R~~~dd.===...,,,..,,,%%%%%%%%",  # 7
    "~~~~~dd.===H..,,,.....,,%%%%%%",  # 8  north herm
    "~~~~dd,.===...,,..*.....%%%%%%",  # 9
    "~~~dd,,..===...,,,....%%%%%%%%",  # 10
    "~~ddd,,,.===...,,.....%%%%%%%%",  # 11
    "dddd.,,,..===...*....,%%%%%%%%",  # 12
    "dddd..,,,..===...C..,.%%%%%%%%",  # 13
    "%%WWBWWWWWW===WWWCWWWB%%%%%%%%",  # 14 the flock's wall gap
    "%%.,,,.....===.....###%%%%%%%%",  # 15 Amaryllis; the fallen column
    "%%..,,,....===.....###C.%%%%%%",  # 16 Agis
    "%%.,,,,....=====...###C.%%%%%%",  # 17
    "%%..,,.....===================",  # 18 the spur east to Kronion Hill
    "%%...,.....===================",  # 19
    "%%.........===H.*...,,..%%%%%%",  # 20 fork herm
    "%%.WWWWWW..===...,,,..*.%%%%%%",  # 21 the big olive
    "%%..*..*...===.C,,..TTTTTT%%%%",  # 22 bee terraces
    "%%......*..===.CTTsT..*.,,%%%%",  # 23
    "%%..*......===.C.,.**...,.%%%%",  # 24
    "%%...*.....===.C,,.*.**...%%%%",  # 25 Komatas
    "%%..,,,,...===.C.,,,.,,...%%%%",  # 26
    "%%.,,,,,,..===.CT____T....%%%%",  # 27 the Ekans patch
    "%%,,,,,,,,.===..,,,...TTTT%%%%",  # 28
    "%%.,,,,,,,,===...,,,,.....%%%%",  # 29
    "%%..,,,,,,.===..,,....*...%%%%",  # 30
    "%%...,,,,..===...,.......*%%%%",  # 31 Phyllis's grove
    "%%......,,.===.....,,.......%%",  # 32
    "%%........,===......,,......%%",  # 33
    "%%..,,,.....===..,,.........%%",  # 34
    "%%.,,,,.....===...,...,.....%%",  # 35
    "%%..,,......===.......,.....%%",  # 36
    "%%..........===.............%%",  # 37 the grove lane
    "%%.....,,...===..,....*.....%%",  # 38
    "%%....,,,...===...........,,%%",  # 39
    "%%...,,,,..===...,,.........%%",  # 40
    "%%..,,,,...===...,,,........%%",  # 41
    "%%........====....,,,....,..%%",  # 42 Poke Ball above the terrace
    "%%T______T===..,,,,.........%%",  # 43
    "%%.,,,,...===...,,,...,,....%%",  # 44 the shepherd's meadow
    "%%..,,,..===...,,,,,..,,,...%%",  # 45
    "%%...,,..===.....WWW.WWW...*%%",  # 46 an old field wall, broken
    "%%......,===......,,...*....%%",  # 47
    "%%,,....*===.....,.,........%%",  # 48 Tityros
    "%%,,,.....===....,,,........%%",  # 49
    "%%.....,,.===..*.WW,,,......%%",  # 50
    "%%.....,,,===......,,,,,....%%",  # 51
    "%%..,,,,...===.,,......B....%%",  # 52
    "%%...,,....===...,..........%%",  # 53
    "%%.......,.===......,,,.....%%",  # 54
    "%%WWWWW....===........,,....%%",  # 55 youth on the wall
    "%%,,,,,,..=======abk..,,....%%",  # 56 the carter's load, the cart rut
    "%%,,,,,,..=======..dd.......%%",  # 57
    "%%,,,,,,.H===......dd,,,....%%",  # 58 south herm
    "%%.,,,,...===..,,...........%%",  # 59
    "%%%%%%%%..===...%%%%%%%%%%%%%%",  # 60
    "%%%%%%%%..===...%%%%%%%%%%%%%%",  # 61
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 62
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 63 south seam to Elaia
]

ROUTE1_OLIVES = [
    # north: the ragged edge of the hill woods
    (20, 4), (19, 9), (16, 11),
    # fork, the big olive, olives on the terraces
    (2, 16), (5, 23), (18, 20), (24, 24), (19, 29), (2, 27),
    # Phyllis's grove, west of the road ...
    (2, 33), (6, 32), (9, 34), (4, 36), (8, 37), (2, 39), (6, 40),
    # ... and east of it, planted in loose rows around the lane (y=37)
    (15, 32), (22, 32), (18, 33), (25, 33), (16, 35), (20, 35), (23, 35),
    (17, 38), (21, 38), (25, 38), (15, 40), (19, 40), (23, 40),
    # the meadow: the shepherd's lone olive, scrub east of the road
    (3, 50), (2, 45), (20, 44), (25, 46), (22, 48), (14, 50), (19, 52), (25, 50), (26, 41),
    # the south: the carter's shade tree and the grove edges
    (20, 54), (24, 56), (22, 58), (26, 54), (2, 57), (4, 58), (14, 58), (26, 58),
]
ROUTE1_CYPRESSES = [(7, 2), (13, 4), (10, 36), (15, 42), (7, 54), (3, 22), (3, 24)]
ROUTE1_PINES = [(24, 52), (21, 56)]

# ---------------------------------------------------------------------------
# Kronion Hill: the summit, east of Route 1 (connection offset 2: this map's
# row 0 is Route 1's row 2). 24 x 20. Hill foot at y=16-17 (Route 1's 18-19),
# stair up through two terrace walls, the shrine's stylobate on top.
# ---------------------------------------------------------------------------
KRONION = [
    # 0         1         2
    # 012345678901234567890123
    "%%%%%%%%%%%%%%%%%%%%%%%%",  # 0
    "%%%%%%%%%%%%%%%%%%%%%%%%",  # 1
    "%%,,..C,,,.....,,...C.%%",  # 2  behind the shrine
    "%%.,..C#############C.%%",  # 3  stylobate: north edge
    "%%,,...#############,.%%",  # 4
    "%%.,,..#############,,%%",  # 5
    "%%..,..#############.,%%",  # 6
    "%%.....#############..%%",  # 7
    "%%.,...#############.,%%",  # 8
    "%%..,..#############..%%",  # 9  stylobate: south face
    "%%.C..................%%",  # 10
    "%%.CS.................%%",  # 11 the stele; the scene starts at (5,11)
    "%%TTTsTTTTTTTTTTTTTsTT%%",  # 12 upper terrace wall, steps at x=5 and x=19
    "%%.,,..%%......,,,....%%",  # 13
    "%%,,,..%%.....,,,,....%%",  # 14
    "%%ssTTTTTTT___TTTTTTTT%%",  # 15 lower terrace wall, steps at x=2-3
    "====,,,....,,,,.......%%",  # 16 hill foot, from Route 1
    "====,,......,,,,......%%",  # 17
    "%%%%%%%%%%%%%%%%%%%%%%%%",  # 18
    "%%%%%%%%%%%%%%%%%%%%%%%%",  # 19
]
KRONION_OFFSET = 2
KRONION_OLIVES = []
KRONION_CYPRESSES = []


def build_route1_ruins(g, cat):
    """A fallen column on its scrap of stylobate, by the spur (x=19-21, y=15-17)."""
    g.slabs(cat, 19, 15, 21, 17)
    g.place(cat, "ruin_columns", 20, 15, 0, 0, 1, 3)


def build_kronion_ruins(g, cat):
    """The shrine on its stylobate (x=7-19, y=3-9)."""
    x0, x1, y0, y1 = 7, 19, 3, 9
    g.slabs(cat, x0, y0, x1, y1)
    # worn slabs: cracked, weedy, and missing ones in the crumbling south step
    for (x, y, cy) in ((14, 4, 0), (17, 7, 1), (11, 4, 1)):
        g.place(cat, "stylobate", x, y, 3, cy)
    for x in (9, 15):
        g.place(cat, "stylobate", x, y1, 3, 2)
    # standing columns, and one snapped at mid height
    for x in (8, 13, 18):
        g.place(cat, "ruin_columns", x, y0, 0, 0, 1, 3)
    g.place(cat, "ruin_columns", 16, y0, 1, 0, 1, 3)
    # the broken altar, the Titanborn's pit in front of it, spoil and pried slabs
    g.place(cat, "altar_broken", 10, 5, 0, 0, 2, 2)
    g.place(cat, "dig_site", 10, 7, 0, 0, 2, 2)
    g.place(cat, "dig_site", 12, 6, 2, 0)        # spoil heap with the trowel
    g.place(cat, "dig_site", 13, 8, 2, 1)        # plain spoil
    g.place(cat, "dig_site", 9, 6, 3, 0)         # pried-up slab
    g.place(cat, "dig_site", 14, 6, 3, 1)
    # fallen drums, a capital and two stumps
    g.place(cat, "ruin_drums", 15, 8, 0, 0, 2, 1)
    g.place(cat, "ruin_drums", 17, 5, 2, 0)
    g.place(cat, "ruin_drums", 19, 7, 3, 0)
    g.place(cat, "ruin_columns", 10, 3, 2, 2)    # stump behind the altar's corner
    g.place(cat, "ruin_columns", 8, 7, 3, 2)     # two-drum stump with rubble
    # half-buried: the hill has grown back over the platform's corners and edges
    for (x, y, c) in ((7, 3, ","), (7, 4, "."), (19, 3, ","), (19, 4, ","), (7, 8, ","), (19, 6, "."), (19, 5, ",")):
        g.ground(x, y, c)


# ---------------------------------------------------------------------------
# Events. Scripts refer to objects by the LOCALID_ constants mapjson generates.
# ---------------------------------------------------------------------------
def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
        local_id=None, rx=0, ry=0, item=None):
    e = {
        "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
        "movement_range_x": rx, "movement_range_y": ry,
        "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag,
    }
    if local_id:
        e = {"local_id": local_id, **e}
    return e


def item_ball(x, y, item, flag):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag, item=item)


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag}


P = "OBJ_EVENT_GFX_ICHOR_"
WOOLOO = "OBJ_EVENT_GFX_SPECIES(WOOLOO)"
R1 = "KallisteRoute1_EventScript_"
KH = "KallisteRoute1_KronionHill_EventScript_"

ROUTE1_EVENTS = {
    "connections": [
        {"map": "MAP_AKTI_TOWN", "offset": 0, "direction": "up"},
        {"map": "MAP_ELAIA_VILLAGE", "offset": 0, "direction": "down"},
        {"map": "MAP_KALLISTE_ROUTE1_KRONION_HILL", "offset": KRONION_OFFSET, "direction": "right"},
    ],
    "object_events": [
        # south to north
        obj(P + "WOMAN", 16, 56, R1 + "Carter", "MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_ROUTE1_CARTER"),
        obj("OBJ_EVENT_GFX_SPECIES(MUDBRAY)", 18, 57, R1 + "Mudbray", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(P + "YOUTH_M", 5, 55, R1 + "WallYouth", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(P + "SHEPHERD", 7, 48, R1 + "Tityros", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
        obj(WOOLOO, 6, 46, R1 + "GrazingWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        obj(WOOLOO, 2, 52, R1 + "GrazingWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        item_ball(3, 42, "ITEM_POKE_BALL", "FLAG_ICHOR_ITEM_ROUTE1_POKE_BALL"),
        obj(P + "HARVESTER", 25, 37, R1 + "Phyllis", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=6),
        item_ball(27, 35, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_ITEM_ROUTE1_MIRACLE_SEED"),
        obj(P + "MAN", 7, 24, R1 + "OliveFarmer", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(P + "GOATHERD", 18, 25, R1 + "Komatas", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1),
        item_ball(15, 20, "ITEM_POTION", "FLAG_ICHOR_ITEM_ROUTE1_POTION"),
        obj(P + "HOPLITE", 15, 16, R1 + "Agis", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=4),
        obj(P + "AUGUR", 27, 18, R1 + "Polyeidos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4),
        obj(P + "YOUTH_F", 10, 15, R1 + "Amaryllis", "MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_ROUTE1_AMARYLLIS"),
        obj(WOOLOO, 11, 14, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        obj(WOOLOO, 12, 14, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        obj(WOOLOO, 13, 14, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        obj(WOOLOO, 12, 12, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
    ],
    "warp_events": [],
    "coord_events": [],
    "bg_events": [
        sign(9, 58, R1 + "HermSouth"),
        sign(14, 20, R1 + "HermFork"),
        sign(10, 8, R1 + "HermNorth"),
        hidden(6, 24, "ITEM_ORAN_BERRY", "FLAG_ICHOR_HIDDEN_ROUTE1_ORAN_BERRY"),
        hidden(15, 14, "ITEM_REPEL", "FLAG_ICHOR_HIDDEN_ROUTE1_REPEL"),
        hidden(4, 29, "ITEM_ANTIDOTE", "FLAG_ICHOR_HIDDEN_ROUTE1_ANTIDOTE"),
    ],
}

KRONION_EVENTS = {
    "connections": [
        {"map": "MAP_KALLISTE_ROUTE1", "offset": -KRONION_OFFSET, "direction": "left"},
    ],
    "object_events": [
        obj(P + "ALETHEA", 9, 8, KH + "Alethea", "MOVEMENT_TYPE_FACE_RIGHT",
            flag="FLAG_ICHOR_HIDE_ALETHEA_RUINS", local_id="LOCALID_KRONION_ALETHEA"),
        obj(P + "TITAN_GRUNT", 10, 8, KH + "Grunt", "MOVEMENT_TYPE_FACE_UP",
            flag="FLAG_ICHOR_HIDE_RUINS_GRUNTS", local_id="LOCALID_KRONION_PETROS"),
        obj(P + "TITAN_GRUNT", 11, 8, KH + "Grunt", "MOVEMENT_TYPE_FACE_UP",
            flag="FLAG_ICHOR_HIDE_RUINS_GRUNTS", local_id="LOCALID_KRONION_AMATHOS"),
        obj("OBJ_EVENT_GFX_CLIPBOARD", 8, 11, "0", "MOVEMENT_TYPE_FACE_DOWN",
            flag="FLAG_ICHOR_HIDE_TITAN_TABLET", local_id="LOCALID_KRONION_TABLET"),
        item_ball(12, 8, "ITEM_ESCAPE_ROPE", "FLAG_ICHOR_ITEM_KRONION_ESCAPE_ROPE"),
    ],
    "warp_events": [],
    "coord_events": [
        {"type": "trigger", "x": 5, "y": 11, "elevation": 3, "var": "VAR_TEMP_1", "var_value": "0",
         "script": KH + "SummitScene"},
    ],
    "bg_events": [
        sign(4, 11, KH + "Stele"),
        sign(10, 6, KH + "Altar"),
        sign(11, 6, KH + "Altar"),
        sign(10, 7, KH + "Pit"),
        sign(11, 7, KH + "Pit"),
        sign(10, 8, KH + "Pit"),
        sign(11, 8, KH + "Pit"),
        hidden(15, 8, "ITEM_HARD_STONE", "FLAG_ICHOR_HIDDEN_KRONION_HARD_STONE"),
        hidden(11, 5, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_KRONION_STARDUST"),
    ],
}

# Player positions along the route for the screen-sized review crops.
ROUTE1_VIEWS = [(11, 58), (11, 50), (9, 44), (13, 38), (21, 37), (12, 30), (6, 24), (19, 25),
                (13, 19), (22, 18), (12, 14), (8, 8), (11, 3)]
KRONION_VIEWS = [(1, 16), (4, 13), (7, 11), (13, 8)]


# ---------------------------------------------------------------------------
def event_cells(events):
    cells = {(e["x"], e["y"]) for k in ("object_events", "bg_events", "coord_events") for e in events[k]}
    return cells


def build_route1(cat):
    g = Grid(ROUTE1, "Route 1", ROUTE1_OLIVES, ROUTE1_CYPRESSES, ROUTE1_PINES, sea_west=True)
    g.roughen(event_cells(ROUTE1_EVENTS))
    build_route1_ruins(g, cat)
    g.build(cat)
    g.check()
    return g


def build_kronion(cat):
    g = Grid(KRONION, "Kronion Hill", KRONION_OLIVES, KRONION_CYPRESSES)
    g.roughen(event_cells(KRONION_EVENTS), seed=11)
    build_kronion_ruins(g, cat)
    g.build(cat)
    g.check()
    return g


def check_seams(r1, kh):
    """The fixed seams: x=10-13 walkable on Route 1's top and bottom rows, all else
    impassable; and the Kronion connection walkable on the same rows on both sides."""
    errs = []
    for y in (0, r1.h - 1):
        for x in range(r1.w):
            if r1.solid(x, y) != (x not in range(10, 14)):
                errs.append(f"Route 1 seam row {y} x={x}")
    for ky in range(kh.h):
        ry = ky + KRONION_OFFSET
        a = not r1.solid(r1.w - 1, ry) if 0 <= ry < r1.h else False
        b = not kh.solid(0, ky)
        if a != b:
            errs.append(f"Kronion seam: Route 1 ({r1.w - 1},{ry}) vs Kronion (0,{ky})")
    for ry in range(r1.h):
        ky = ry - KRONION_OFFSET
        if not (0 <= ky < kh.h) and not r1.solid(r1.w - 1, ry):
            errs.append(f"Route 1 east edge y={ry} is open where Kronion has no row")
    for g in (r1, kh):
        for y in range(g.h):
            if not g.solid(0, y) and not (g is kh and 16 <= y <= 17):
                errs.append(f"{g.name}: west edge open at y={y}")
    if errs:
        sys.exit("seam errors:\n  " + "\n  ".join(errs))


def write_layout(layout_id, folder, g, border):
    d = ROOT / "data/layouts" / folder
    g.blocks().tofile(d / "map.bin")
    np.array(border, "<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == layout_id:
            lay.update({"width": g.w, "height": g.h, "primary_tileset": PRIMARY, "secondary_tileset": SECONDARY})
            break
    else:
        sys.exit(f"no layout {layout_id}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_events(folder, events, music):
    path = ROOT / "data/maps" / folder / "map.json"
    m = json.loads(path.read_text())
    m["music"] = music
    m.update(events)
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def renderer():
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset(PRIMARY, syms)), rm.Tileset(rm.resolve_tileset(SECONDARY, syms)))


def render(g, name, events, border, views):
    """Plain render, a review copy with collision and events marked, and a sheet of
    15x10-tile screens around the given player positions (border shown past the edges)."""
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer()
    RENDER.mkdir(parents=True, exist_ok=True)
    img = rm.render_blocks(r, g.blocks().ravel(), g.w)
    img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(RENDER / f"{name}.png")

    s = 3
    rev = img.resize((img.width * s, img.height * s), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", rev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    font = ImageFont.load_default(size=11)
    cell = 16 * s
    for y in range(g.h):
        for x in range(g.w):
            if g.solid(x, y):
                d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=(255, 0, 0, 60))
    colors = {"sign": (255, 220, 0), "hidden_item": (0, 220, 120), "trigger": (255, 0, 255)}
    for e in events["object_events"]:
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 4, y * cell + 4, x * cell + cell - 5, y * cell + cell - 5], outline=(40, 80, 255), width=3)
        label = e["script"].split("_")[-1] if e["script"] != "Common_EventScript_FindItem" else e["trainer_sight_or_berry_tree_id"][5:]
        d.text((x * cell + 2, y * cell + 2), label[:8], fill=(255, 255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for e in events["bg_events"] + events["coord_events"]:
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 10, y * cell + 10, x * cell + cell - 11, y * cell + cell - 11], outline=colors[e["type"]], width=3)
    for i in range(max(g.w, g.h)):
        for txt, pos in ((str(i), (i * cell + cell // 2 - 6, 0)), (str(i), (2, i * cell + cell // 2 - 6))):
            if (pos[1] == 0 and i < g.w) or (pos[0] == 2 and i < g.h):
                d.text(pos, txt, fill=(255, 255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(rev, over).convert("RGB").save(RENDER / f"{name}_review.png")

    # Screens: the GBA shows 15x10 tiles with the player at column 7, row 4/5.
    pad = 8
    W, H = g.w + 2 * pad, g.h + 2 * pad
    big = np.full((H, W), border[0], np.uint16)
    for y in range(H):
        for x in range(W):
            big[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
    big[pad:pad + g.h, pad:pad + g.w] = g.blocks() & 0x3FF
    full = rm.render_blocks(r, big.ravel(), W)
    shots = []
    for (px, py) in views:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16
        shots.append(full.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
    cols = 3
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 488 + 8, rows * 328 + 8), (24, 24, 32))
    for i, sh in enumerate(shots):
        sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
    sheet.save(RENDER / f"{name}_screens.png")
    return [RENDER / f"{name}.png", RENDER / f"{name}_review.png", RENDER / f"{name}_screens.png"]


ROUTE1_BORDER = [SEA, SEA, SEA, SEA]
KRONION_BORDER = [OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOTTOM_TIP[0], OLIVE_BOTTOM_TIP[1]]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()
    cat = load_catalog()
    r1 = build_route1(cat)
    kh = build_kronion(cat)
    check_seams(r1, kh)
    write_layout("LAYOUT_KALLISTE_ROUTE1", "KallisteRoute1", r1, ROUTE1_BORDER)
    write_layout("LAYOUT_KALLISTE_ROUTE1_KRONION_HILL", "KallisteRoute1_KronionHill", kh, KRONION_BORDER)
    write_events("KallisteRoute1", ROUTE1_EVENTS, "MUS_ICHOR_ROUTE1")
    write_events("KallisteRoute1_KronionHill", KRONION_EVENTS, "MUS_ICHOR_ROUTE1")
    RENDER.mkdir(parents=True, exist_ok=True)
    (RENDER / "kalliste_route1.txt").write_text(r1.ascii() + "\n")
    print(f"Route 1 {r1.w}x{r1.h}, Kronion Hill {kh.w}x{kh.h}")
    if not args.no_render:
        for g, name, ev, border, views in (
                (r1, "kalliste_route1", ROUTE1_EVENTS, ROUTE1_BORDER, ROUTE1_VIEWS),
                (kh, "kalliste_route1_kronion_hill", KRONION_EVENTS, KRONION_BORDER, KRONION_VIEWS)):
            for p in render(g, name, ev, border, views):
                print(p)


if __name__ == "__main__":
    main()
