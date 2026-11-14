#!/usr/bin/env python3
"""Build Route 1 and the Kronion Hill summit: layouts, borders and events.

Both maps are drawn below as ASCII grids on gTileset_Aethos + gTileset_Agros,
with the interior olives listed as anchors and the bigger set pieces (the big
olive, the cart, the bee wall, the spring, the shrine, the threshing floor and
Kronion's ruins) placed in code. This script auto-tiles them:

  - tall grass and the road get soft, curving edges from Agros's shape pieces;
    a grass cell in a stair-step corner becomes a diagonal "half cell"
  - field walls join in any direction; the hill's rock bands end in slopes
  - olives get crown tips above and soft shade below; '%' woods fill with a
    staggered mix of olives, stone pines, figs, cypresses, rocks and shrubs
  - the rocky shore picks its piece by where the sea is

It sets collision and elevation for every cell and writes:

  data/layouts/KallisteRoute1/{map,border}.bin
  data/layouts/KallisteRoute1_KronionHill/{map,border}.bin
  the two layouts' entries in data/layouts/layouts.json (edited in place)
  the events and connections in data/maps/<Map>/map.json

Review images go to build/render/: each map plain at 2x, a copy with collision
tinted red and every event marked, and a sheet of GBA-screen crops (15x10
tiles) along the player's route.

Usage:
  /usr/bin/python3 tools/ichor/maps/route1.py [--no-render]
  /usr/bin/python3 tools/ichor/maps/route1.py --shapes   # list the ground shapes Agros must hold

After --shapes changes tools/ichor/art/agros_shapes.json, rebuild Agros
(tools/ichor/art/agros_build.py), then run this again.

Ground legend (one character per metatile):
  .  grass       ,  tall grass (wild encounters)       *  red anemones
  h  field herbs  y  wild thyme   b  broom   n  oleander   r  a rock
  =  limestone road     -  goat track     d  sand     ~  sea     R  rock in the sea
  q  rocky shore (piece chosen by where the sea is)    B  boulder
  O  olive (2x2)   P  stone pine (2x2)   F  fig (2x2)   Q  outcrop (2x2)   C  cypress (1x2)
  %  woods, filled with a mix of all of the above
  W  field wall (joins its neighbors)    _  terrace lip, jump south
  T  terrace retaining wall   s  steps through it (both from kalliste)
  Z  Kronion's rock band      z  a stair cut through it
  H  roadside herm      S  marble stele      #  set pieces placed in code
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CATALOG = ROOT / "build/agros/catalog.json"
SHAPES = ROOT / "tools/ichor/art/agros_shapes.json"
LAYOUTS = ROOT / "data/layouts/layouts.json"
RENDER = ROOT / "build/render"

PRIMARY = "gTileset_Aethos"
SECONDARY = "gTileset_Agros"

# --- aethos metatiles (General's ids, see design/phase1/TILES_aethos.md) ---
GRASS, TALL, FLOWERS, BOULDER = 0x001, 0x00D, 0x004, 0x0E0
HERM, STELE = 0x01B, 0x003
SEA, SEA_ROCK = 0x170, 0x18C
PATH_MID = 0x1D9
SURF = {"TL": 0x11B, "T": 0x11C, "TR": 0x11D, "L": 0x123, "R": 0x125,
        "BL": 0x12B, "B": 0x12C, "BR": 0x12D,
        "dNW": 0x13D, "dNE": 0x13E, "dSW": 0x145, "dSE": 0x146}
SURF_WALKABLE = {0x11C, 0x13D, 0x13E}
DUNE = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122,
        "BL": 0x128, "B": 0x129, "BR": 0x12A}
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOTTOM = (0x1E4, 0x1E5)
OLIVE_BOTTOM_TIP = (0x1DC, 0x1DD)
OLIVE_TIP = {"grass": (0x1CE, 0x1CF), "tall": (0x1C6, 0x1C7)}
CYPRESS_TOP, CYPRESS_TOP_TALL, CYPRESS_BOTTOM = 0x00E, 0x025, 0x016
PINE = (0x01E, 0x01F, 0x026, 0x027)
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # N NE E SE S SW W NW


# Each map.bin cell: metatile | collision << 10 | elevation << 12. Vanilla's
# conventions: ground is elevation 3; walls, trees and ledges are collision 1
# at elevation 0; the sea is elevation 1 (surfable later), its rocks collision 1.
def walk(mid):
    return mid | (3 << 12)


def block(mid):
    return mid | (1 << 10)


def water(mid):
    return mid | (1 << 12)


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


def hashpct(x, y, salt):
    h = (x * 73856093 ^ y * 19349663 ^ salt * 83492791) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h >> 8) % 100


def load_catalog():
    if not CATALOG.exists():
        sys.exit(f"{CATALOG} is missing: run /usr/bin/python3 tools/ichor/art/agros_build.py")
    return {s["key"]: s for s in json.loads(CATALOG.read_text())}


BLOCKING = "OCPFQ#WTsjHS=~dRB_Zzqbnr"
HALF_LETTERS = {"a": ((0, -1), (1, 0), (1, -1)), "b": ((0, 1), (1, 0), (1, 1)),
                "c": ((0, 1), (-1, 0), (-1, 1)), "d": ((0, -1), (-1, 0), (-1, -1))}


class Grid:
    def __init__(self, rows, name, olives=(), cypresses=(), pines=(), sea_edges=""):
        self.name = name
        self.sea_edges = sea_edges        # map edges the sea lies beyond: some of "NESW"
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
        self.half = {}            # (x, y) -> ("path" | "tall", letter)
        self.protect = set()

    # --- composition passes ------------------------------------------------
    def fill_woods(self):
        """Fill '%' with a staggered mix: olives, stone pines, figs and rock
        outcrops in 2x2 blocks, cypresses in pairs, broom, oleander and rocks
        in the gaps, so wood edges never read as a column of one tree."""
        free = lambda x, y: self.ch(x, y) == "%"
        for y in range(self.h):
            for x in range(self.w):
                if not free(x, y):
                    continue
                square = free(x + 1, y) and free(x, y + 1) and free(x + 1, y + 1)
                pair = free(x, y + 1)
                r = hashpct(x, y, 1)
                if square and not (pair and r < 16):
                    k = hashpct(x, y, 2)
                    kind = "P" if k < 15 else "F" if k < 25 else "Q" if k < 33 else "O"
                    for cx, cy in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)):
                        self.chars[cy][cx] = kind
                elif pair:
                    self.chars[y][x] = self.chars[y + 1][x] = "C"
                else:
                    k = hashpct(x, y, 3)
                    self.chars[y][x] = "b" if k < 35 else "n" if k < 60 else "r"

    def roughen(self, protect, seed=7):
        """Break the straight edges of the drawn tall-grass patches with smooth
        noise. Never on event cells, so trainers, items and signs keep their ground."""
        self.protect = set(protect)
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

    def find_halves(self):
        """Grass cells in a stair-step corner of the road or a meadow become half
        cells, cutting the corner on the diagonal. The road wins ties."""
        for kind, ch in (("path", "="), ("tall", ",")):
            for y in range(self.h):
                for x in range(self.w):
                    if self.chars[y][x] != "." or (x, y) in self.half or (x, y) in self.protect:
                        continue
                    for letter, (a, b, d) in HALF_LETTERS.items():
                        others = [o for o in ((0, -1), (1, 0), (0, 1), (-1, 0)) if o not in (a, b)]
                        if all(self.ch(x + dx, y + dy) == ch for dx, dy in (a, b, d)) and \
                           not any(self.ch(x + dx, y + dy) == ch for dx, dy in others):
                            self.half[(x, y)] = (kind, letter)
                            break

    # --- helpers --------------------------------------------------------------
    def ascii(self):
        return "\n".join("".join(r) for r in self.chars)

    def ch(self, x, y, default=None):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.chars[y][x]
        return default

    def clamp_ch(self, x, y):
        """Off the map, the ground continues as at the nearest edge cell (seams)."""
        return self.chars[min(max(y, 0), self.h - 1)][min(max(x, 0), self.w - 1)]

    def put(self, x, y, value):
        self.cells[y, x] = value
        self.done[y, x] = True

    def is_sea(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            side = ("W" if x < 0 else "E" if x >= self.w else "") + ("N" if y < 0 else "S" if y >= self.h else "")
            return any(s in self.sea_edges for s in side)
        return self.chars[y][x] in ("~", "R")

    def state(self, kind, ch, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            x, y = min(max(x, 0), self.w - 1), min(max(y, 0), self.h - 1)
        if self.chars[y][x] == ch and (x, y) not in self.half:
            return "1"
        h = self.half.get((x, y))
        return h[1] if h and h[0] == kind else "0"

    def shape_key(self, kind, ch, x, y):
        center = self.state(kind, ch, x, y)
        neigh = [self.state(kind, ch, x + dx, y + dy) for dx, dy in DIRS]
        # a diagonal only matters when both of its sides are filled
        for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
            if neigh[a] == "0" or neigh[c] == "0":
                neigh[d] = "0"
        return center + "|" + "".join(neigh)

    def shapes(self):
        """Every ground shape key this map uses, by kind."""
        self.find_halves()
        out = {"tall": set(), "path": set(), "track": set()}
        for y in range(self.h):
            for x in range(self.w):
                c, h = self.chars[y][x], self.half.get((x, y))
                if c == "," or (h and h[0] == "tall"):
                    k = self.shape_key("tall", ",", x, y)
                    if k != "1|11111111":
                        out["tall"].add(k)
                if c == "=" or (h and h[0] == "path"):
                    k = self.shape_key("path", "=", x, y)
                    if k != "1|11111111":
                        out["path"].add(k)
                if c == "-":
                    out["track"].add(self.track_key(x, y))
        return out

    def track_key(self, x, y):
        n = ["1" if self.clamp_ch(x + dx, y + dy) in "-=" else "0" for dx, dy in DIRS]
        for d in (1, 3, 5, 7):
            n[d] = "0"
        return "1|" + "".join(n)

    # --- tiling ---------------------------------------------------------------
    def piece(self, cat, key, name):
        s = cat[key]
        cx, cy = s["names"][name]
        return s["ids"][cy][cx], s["walk"][cy][cx]

    def put_piece(self, x, y, mid, code):
        self.put(x, y, walk(mid) if code in ".TG" else block(mid))

    def place(self, cat, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place cells of a catalog structure, collision from its walk grid.
        Without a catalog (the --shapes pass) it does nothing."""
        if cat is None:
            return
        s = cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.put_piece(x + i, y + j, s["ids"][cy + j][cx + i], s["walk"][cy + j][cx + i])

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
                self.place(cat, "stylobate", x, y, cx, cy, 1, 1)

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
        for x, y in tops:
            for i in (0, 1):
                ax, ay = x + i, y - 1
                if ay < 0 or self.ch(ax, ay) not in (".", ",") or self.done[ay, ax] or (ax, ay) in self.half:
                    continue
                tip = OLIVE_TIP["tall" if self.ch(ax, ay) == "," else "grass"][i]
                self.put(ax, ay, walk(tip))
        return tops

    def shades(self, cat, tops):
        """Soft shade on the grass under each olive."""
        for x, y in tops:
            cells = [(x, y + 2), (x + 1, y + 2)]
            if all(self.ch(cx, cy) == "." and not self.done[cy, cx] and (cx, cy) not in self.half
                   and (cx, cy) not in self.protect for cx, cy in cells):
                s = cat["tree_shade"]
                for i, (cx, cy) in enumerate(cells):
                    self.put_piece(cx, cy, s["ids"][0][i], s["walk"][0][i])

    def blocks2(self, cat):
        """2x2 stone pines (aethos), figs and outcrops (Agros)."""
        for y in range(self.h):
            for x in range(self.w):
                c = self.chars[y][x]
                if c not in "PFQ" or self.done[y, x]:
                    continue
                if c == "P":
                    for i, mid in enumerate(PINE):
                        self.put(x + i % 2, y + i // 2, block(mid))
                else:
                    self.place(cat, "fig" if c == "F" else "outcrop", x, y)

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

    def soft_ground(self, cat):
        """Tall grass, road and track, from Agros's shape pieces."""
        for y in range(self.h):
            for x in range(self.w):
                if self.done[y, x]:
                    continue
                c, h = self.chars[y][x], self.half.get((x, y))
                kind = h[0] if h else {",": "tall", "=": "path", "-": "track"}.get(c)
                if not kind:
                    continue
                if kind == "track":
                    key = self.track_key(x, y)
                else:
                    key = self.shape_key(kind, "," if kind == "tall" else "=", x, y)
                    if key == "1|11111111":
                        self.put(x, y, walk(TALL if kind == "tall" else PATH_MID))
                        continue
                if key not in cat[kind]["names"]:
                    sys.exit(f"{self.name}: ({x},{y}) needs {kind} shape {key}; run route1.py --shapes, "
                             "then tools/ichor/art/agros_build.py")
                self.put_piece(x, y, *self.piece(cat, kind, key))

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
        wet = edge(self.is_sea, SURF, None)
        if wet is None:
            for key, (dx, dy) in (("dNW", (-1, -1)), ("dNE", (1, -1)), ("dSW", (-1, 1)), ("dSE", (1, 1))):
                if self.is_sea(x + dx, y + dy):
                    wet = SURF[key]
                    break
        if wet is not None:
            return walk(wet) if wet in SURF_WALKABLE else water(wet)
        dry = lambda cx, cy: self.ch(cx, cy) is not None and self.ch(cx, cy) != "d" and not self.is_sea(cx, cy)
        return walk(edge(dry, DUNE, DUNE["C"]))

    def shore(self, cat):
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "q":
                    continue
                n, e, w = self.is_sea(x, y - 1), self.is_sea(x + 1, y), self.is_sea(x - 1, y)
                alt = "2" if (x + y) % 2 else ""
                name = ("NE" if n and e else "NW" if n and w else ("N" + alt) if n
                        else ("E" + alt) if e else ("W" + alt) if w else "N")
                self.put_piece(x, y, *self.piece(cat, "shore", name))

    def walls(self, cat):
        isw = lambda x, y: self.ch(x, y) == "W"
        for y in range(self.h):
            for x in range(self.w):
                if not isw(x, y):
                    continue
                key = "".join(d for d, (dx, dy) in zip("NESW", ((0, -1), (1, 0), (0, 1), (-1, 0))) if isw(x + dx, y + dy))
                self.put_piece(x, y, *self.piece(cat, "field_wall", key or "post"))

    def terraces(self, cat):
        ids = cat["terrace"]["ids"]
        band = lambda x, y: self.ch(x, y) in ("T", "s", "_")
        for y in range(self.h):
            for x in range(self.w):
                c = self.chars[y][x]
                if c == "s":
                    self.put(x, y, walk(ids[0][3]))
                elif c == "T":
                    mid = ids[0][0] if not band(x - 1, y) else ids[0][4] if not band(x + 1, y) else ids[0][1 + x % 2]
                    self.put(x, y, block(mid))

    def lips(self, cat):
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "_":
                    continue
                left, right = self.ch(x - 1, y), self.ch(x + 1, y)
                name = "W" if left not in ("_", "T") else "E" if right not in ("_", "T") else "run"
                self.put_piece(x, y, *self.piece(cat, "lip", name))

    def rockfaces(self, cat):
        band = lambda x, y: self.ch(x, y) in ("Z", "z")
        for y in range(self.h):
            for x in range(self.w):
                c = self.chars[y][x]
                if c not in "Zz":
                    continue
                if c == "z":
                    name = "stair"
                elif not band(x - 1, y):
                    name = "W"
                elif not band(x + 1, y):
                    name = "E"
                else:
                    name = "run2" if x % 3 == 1 else "run"
                self.put_piece(x, y, *self.piece(cat, "rockface", name))

    def simple(self, cat):
        table = {
            ".": walk(GRASS), "*": walk(FLOWERS), "B": block(BOULDER), "H": block(HERM), "S": block(STELE),
        }
        singles = {"h": "herbs", "y": "thyme", "b": "broom", "n": "oleander", "r": "rock"}
        for y in range(self.h):
            for x in range(self.w):
                if self.done[y, x]:
                    continue
                c = self.chars[y][x]
                if c in table:
                    self.put(x, y, table[c])
                elif c in singles:
                    self.place(cat, singles[c], x, y)

    def build(self, cat):
        self.find_halves()
        tops = self.trees()
        self.blocks2(cat)
        self.cypresses()
        self.sea()
        self.shore(cat)
        self.walls(cat)
        self.terraces(cat)
        self.lips(cat)
        self.rockfaces(cat)
        self.shades(cat, tops)
        self.soft_ground(cat)
        self.simple(cat)

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
#   leaving Elaia between olive groves; the carter resting by her cart
#   the shepherd's meadow running down to a rocky shore; the threshing floor
#   up a goat track; a terrace lip above
#   Phyllis's grove: the road narrows between the trees; a spring and a fig
#   the ancient olive; the bee terraces climbing east
#   the fork: a herm, a Lakonian drilling, a fallen column by the spur
#   the flock in the wall gap; the cove, the first sight of the sea; a shrine
# ---------------------------------------------------------------------------
ROUTE1 = [
    # 0         1         2
    # 012345678901234567890123456789
    "q%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 0  north seam to Akti
    "q%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 1
    "q%%%......===.C#.,%%%%%%%%%%%%",  # 2  a roadside shrine between cypresses
    "q%%%dd,...===.C#,,%%%%%%%%%%%%",  # 3
    "dddddd,,..===...,,,,..%%%%%%%%",  # 4  the cove: first sight of the sea
    "~~~ddd,,.===..,,,,,,..%%%%%%%%",  # 5
    "~~~~dd,..===..,,,,*.,,%%%%%%%%",  # 6
    "~R~~~dd.===...,,,..,,,%%%%%%%%",  # 7
    "~~~~~dd.===H..,,,.....,,%%%%%%",  # 8  north herm
    "~~~~dd,.===...,,.h*.....%%%%%%",  # 9
    "~~~dd,,..===...,,,....%%%%%%%%",  # 10
    "~~ddd,,,.===...,,.....%%%%%%%%",  # 11
    "dddd.,,,..===...*..y.,%%%%%%%%",  # 12
    "dddd..,,,..===...C..,.%%%%%%%%",  # 13
    "%%WWBWWWWWW===WWWCWWWB%%%%%%%%",  # 14 the flock's wall gap
    "%%.,,,.....===.....###%%%%%%%%",  # 15 Amaryllis; the fallen column
    "%%..,,,....===..h..###C.%%%%%%",  # 16 Agis
    "%%.,,,,....=====...###C.%%%%%%",  # 17
    "%%..,,.....===================",  # 18 the spur east to Kronion Hill
    "%%...,.....===================",  # 19
    "%%.........===H.*.y.,,..%%%%%%",  # 20 fork herm
    "%%..*..h...===...,,,..*.%%%%%%",  # 21
    "%%C####....===.C,,..TTTTTT%%%%",  # 22 the ancient olive; bee terraces
    "%%C####.*..===.CTTsT..*.,,%%%%",  # 23
    "%%C####y...===.C.,.**.###.%%%%",  # 24 the bee wall
    "%%C####....===.C,,..*.###.%%%%",  # 25 the farmer; Komatas
    "%%..*hy*...===.C.,,,.,,...%%%%",  # 26
    "q,.,,,,,,..===.CT____T....%%%%",  # 27 the Ekans patch runs to the shore
    "q,,,,,,,,,.===..,,,...TTTT%%%%",  # 28
    "q.,,,,,,,,,===...,,,,.....%%%%",  # 29
    "q..,,,,,,,.===..,,....*...%%%%",  # 30
    "%%...,,,,..===...,.......*%%%%",  # 31 Phyllis's grove
    "%%###.FF,..===.....,,.......%%",  # 32 a spring under a fig
    "%%###nFF.,.===......,,......%%",  # 33
    "%%.---------===..,,.........%%",  # 34 the spring's track
    "%%.,,,,.....===...,...,.....%%",  # 35
    "%%..,,......===.......,.....%%",  # 36
    "%%..........===.............%%",  # 37 the grove lane
    "%%.....,,...===..,....*.....%%",  # 38
    "%%....,,,...===...........,,%%",  # 39
    "%%...,,,,..===...,,.........%%",  # 40
    "%%..,,,,...===...,,,........%%",  # 41
    "%%........====....,,,....,..%%",  # 42 Poke Ball above the terrace lip
    "%%________===..,,,,.........%%",  # 43
    "%%.,,,,...===...,,,...,,....%%",  # 44 the shepherd's meadow
    "%%..,,,..===...,,,,,..,,,...%%",  # 45
    "q....,,..===......####.....*%%",  # 46 the threshing floor
    "q.......,===....h.####......%%",  # 47
    "q.,,....*===------####......%%",  # 48 Tityros; the track to the floor
    "q,,,......===..h..####......%%",  # 49
    "q......,,.===..*...,,,......%%",  # 50
    "q......,,,===......,,,,,....%%",  # 51
    "q...,,,,...===.,,......B....%%",  # 52
    "%%...,,....===...,..........%%",  # 53
    "%%.......,.===......,,,.....%%",  # 54
    "%%WWWWW....===....###..,....%%",  # 55 youth on the wall; the cart
    "%%,,,,,,..=======.###..,....%%",  # 56 the cart rut
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
    # fork and the terraces
    (2, 16), (20, 20), (19, 29),
    # Phyllis's grove, west of the road ...
    (4, 36), (8, 37), (2, 39), (6, 40),
    # ... and east of it, planted in loose rows around the lane (y=37)
    (15, 32), (22, 32), (18, 33), (25, 33), (16, 35), (20, 35), (23, 35),
    (17, 38), (21, 38), (25, 38), (15, 40), (19, 40), (23, 40),
    # the meadow: the shepherd's lone olive, scrub east of the road
    (3, 50), (2, 44), (20, 43), (25, 46), (14, 50), (19, 52), (25, 50), (26, 41),
    # the south: the carter's shade tree and the grove edges
    (21, 53), (24, 56), (22, 58), (26, 54), (2, 57), (4, 58), (14, 58), (26, 58),
]
ROUTE1_CYPRESSES = [(7, 2), (13, 4), (10, 36), (15, 42), (7, 54)]
ROUTE1_PINES = [(24, 52), (21, 56)]

# ---------------------------------------------------------------------------
# Kronion Hill: the summit, east of Route 1 (connection offset 2: this map's
# row 0 is Route 1's row 2). 24 x 62. From the hill foot (y=16-17, Route 1's
# 18-19) a stair climbs a band of rock, the path doubles back along a shelf to
# a second stair, and the shrine's stylobate stands on top, at the edge of a
# cliff over the sea. Rows 20-61 are only woods: Route 1 shows this map past
# its east edge, so it covers every row a player there can see.
# ---------------------------------------------------------------------------
KRONION = [
    # 0         1         2
    # 012345678901234567890123
    "%%%%q~~~~~~~~~~~~~~~~~~~",  # 0  the sea below the summit's cliffs
    "%%%%q~~~~~~~~~~~~~~~~~~~",  # 1
    "%%%%.qqqqqqqqqqqqqq~~~~~",  # 2  the cliff edge
    "%%%%.###########..q~~~~~",  # 3  the stylobate (x=5-15, y=3-8)
    "%%%%,###########.,q~~~~~",  # 4
    "%%%.,###########..q~~~~~",  # 5
    "%%%..###########,.q~~~~~",  # 6
    "%%%,.###########..q~~~~~",  # 7
    "%%%..###########.,q~~~~~",  # 8  its south face
    "%%%C..............q~~~~~",  # 9
    "%%,C..........S...q~~~~~",  # 10 the scene starts at the stair's top (13,10)
    "%%ZZZZZZZZZZZzZZZZq~~~~~",  # 11 upper rock band, stair at x=13
    "%%.,,...rb..,,,...q~~~~~",  # 12 the shelf
    "%%..,,......y.....q~~~~~",  # 13
    "%%.,,....ZZZZZZZZZ%qqqqq",  # 14 lower band, east half
    "%%ZZZZzZZZZ%%%%%%%%%%%%%",  # 15 lower band, west half, stair at x=6
    "====,,..%%%%%%%%%%%%%%%%",  # 16 hill foot, from Route 1
    "====..,,%%%%%%%%%%%%%%%%",  # 17
    "%%%%%%%%%%%%%%%%%%%%%%%%",  # 18
    "%%%%%%%%%%%%%%%%%%%%%%%%",  # 19
] + ["%" * 24] * 42  # 20-61: the hill's woods, seen past Route 1's east edge
KRONION_OFFSET = 2
KRONION_OLIVES = []
KRONION_CYPRESSES = []


def build_route1_pieces(g, cat):
    """Route 1's set pieces."""
    g.slabs(cat, 19, 15, 21, 17)                      # a fallen column by the spur
    g.place(cat, "ruin_columns", 20, 15, 0, 0, 1, 3)
    g.place(cat, "big_olive", 3, 22)                  # the ancient olive
    g.place(cat, "bee_wall", 22, 24)                  # Komatas's hives
    g.place(cat, "spring", 2, 32)                     # the spring in the grove
    g.place(cat, "shrine", 15, 2)                     # the shrine on the way into Akti
    g.place(cat, "alonia", 18, 46)                    # the threshing floor
    g.place(cat, "cart", 18, 55)                      # the carter's cart


def build_kronion_ruins(g, cat):
    """The shrine on its stylobate (x=5-15, y=3-8)."""
    x0, x1, y0, y1 = 5, 15, 3, 8
    g.slabs(cat, x0, y0, x1, y1)
    for (x, y, cy) in ((12, 4, 0), (15, 7, 1), (7, 5, 1)):
        g.place(cat, "stylobate", x, y, 3, cy, 1, 1)       # cracked and weedy slabs
    for x in (8, 13):
        g.place(cat, "stylobate", x, y1, 3, 2, 1, 1)       # slabs gone from the south step
    for x in (6, 11, 14):
        g.place(cat, "ruin_columns", x, y0, 0, 0, 1, 3)    # standing columns
    g.place(cat, "ruin_columns", 13, y0, 1, 0, 1, 3)       # one snapped
    g.place(cat, "altar_broken", 9, 4, 0, 0, 2, 2)         # the broken altar
    g.place(cat, "dig_site", 9, 6, 0, 0, 2, 2)             # the Titanborn's pit
    g.place(cat, "dig_site", 11, 6, 2, 0, 1, 1)            # spoil heap with the trowel
    g.place(cat, "dig_site", 12, 7, 2, 1, 1, 1)            # plain spoil
    g.place(cat, "dig_site", 8, 6, 3, 0, 1, 1)             # pried-up slabs
    g.place(cat, "dig_site", 12, 5, 3, 1, 1, 1)
    g.place(cat, "ruin_drums", 13, 7, 0, 0, 2, 1)          # fallen drums
    g.place(cat, "ruin_drums", 15, 5, 2, 0, 1, 1)          # a single drum
    g.place(cat, "ruin_drums", 14, 6, 3, 0, 1, 1)          # a toppled capital
    g.place(cat, "ruin_columns", 7, 3, 2, 2, 1, 1)         # a stump
    g.place(cat, "ruin_columns", 6, 7, 3, 2, 1, 1)         # a two-drum stump
    for (x, y, c) in ((5, 3, ","), (15, 3, ","), (5, 7, "."), (15, 4, "."), (5, 4, ".")):
        g.ground(x, y, c)                                  # half-buried edges


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
        obj(P + "WOMAN", 17, 57, R1 + "Carter", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_ROUTE1_CARTER"),
        obj("OBJ_EVENT_GFX_SPECIES(MUDBRAY)", 17, 56, R1 + "Mudbray", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(P + "YOUTH_M", 5, 55, R1 + "WallYouth", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(P + "SHEPHERD", 7, 48, R1 + "Tityros", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
        obj(WOOLOO, 4, 46, R1 + "GrazingWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        obj(WOOLOO, 2, 52, R1 + "GrazingWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        item_ball(3, 42, "ITEM_POKE_BALL", "FLAG_ICHOR_ITEM_ROUTE1_POKE_BALL"),
        obj(P + "HARVESTER", 25, 37, R1 + "Phyllis", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=6),
        item_ball(27, 35, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_ITEM_ROUTE1_MIRACLE_SEED"),
        obj(P + "MAN", 7, 25, R1 + "OliveFarmer", "MOVEMENT_TYPE_FACE_LEFT"),
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
        sign(11, 8, R1 + "HermNorth"),
        hidden(4, 25, "ITEM_ORAN_BERRY", "FLAG_ICHOR_HIDDEN_ROUTE1_ORAN_BERRY"),
        hidden(15, 14, "ITEM_REPEL", "FLAG_ICHOR_HIDDEN_ROUTE1_REPEL"),
        hidden(4, 29, "ITEM_ANTIDOTE", "FLAG_ICHOR_HIDDEN_ROUTE1_ANTIDOTE"),
    ],
}

KRONION_EVENTS = {
    "connections": [
        {"map": "MAP_KALLISTE_ROUTE1", "offset": -KRONION_OFFSET, "direction": "left"},
    ],
    "object_events": [
        obj(P + "ALETHEA", 9, 9, KH + "Alethea", "MOVEMENT_TYPE_FACE_UP",
            flag="FLAG_ICHOR_HIDE_ALETHEA_RUINS", local_id="LOCALID_KRONION_ALETHEA"),
        obj(P + "TITAN_GRUNT", 9, 7, KH + "Grunt", "MOVEMENT_TYPE_FACE_UP",
            flag="FLAG_ICHOR_HIDE_RUINS_GRUNTS", local_id="LOCALID_KRONION_PETROS"),
        obj(P + "TITAN_GRUNT", 10, 7, KH + "Grunt", "MOVEMENT_TYPE_FACE_UP",
            flag="FLAG_ICHOR_HIDE_RUINS_GRUNTS", local_id="LOCALID_KRONION_AMATHOS"),
        obj("OBJ_EVENT_GFX_ICHOR_TABLET", 10, 8, "0", "MOVEMENT_TYPE_FACE_DOWN",
            flag="FLAG_ICHOR_HIDE_TITAN_TABLET", local_id="LOCALID_KRONION_TABLET"),
        item_ball(16, 3, "ITEM_ESCAPE_ROPE", "FLAG_ICHOR_ITEM_KRONION_ESCAPE_ROPE"),
    ],
    "warp_events": [],
    "coord_events": [
        {"type": "trigger", "x": 13, "y": 10, "elevation": 3, "var": "VAR_TEMP_1", "var_value": "0",
         "script": KH + "SummitScene"},
    ],
    "bg_events": [
        sign(14, 10, KH + "Stele"),
        sign(9, 5, KH + "Altar"),
        sign(10, 5, KH + "Altar"),
        sign(9, 6, KH + "Pit"),
        sign(10, 6, KH + "Pit"),
        sign(9, 7, KH + "Pit"),
        sign(10, 7, KH + "Pit"),
        hidden(13, 7, "ITEM_HARD_STONE", "FLAG_ICHOR_HIDDEN_KRONION_HARD_STONE"),
        hidden(10, 4, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_KRONION_STARDUST"),
    ],
}

# Player positions along the route for the screen-sized review crops.
ROUTE1_VIEWS = [(11, 58), (12, 52), (9, 46), (9, 41), (13, 36), (21, 37), (9, 28), (12, 23),
                (19, 25), (13, 19), (22, 18), (12, 15), (8, 8), (11, 3)]
KRONION_VIEWS = [(2, 16), (6, 13), (12, 12), (11, 10), (14, 9), (16, 5)]


# ---------------------------------------------------------------------------
def event_cells(events):
    return {(e["x"], e["y"]) for k in ("object_events", "bg_events", "coord_events") for e in events[k]}


def make_route1():
    g = Grid(ROUTE1, "Route 1", ROUTE1_OLIVES, ROUTE1_CYPRESSES, ROUTE1_PINES, sea_edges="W")
    g.roughen(event_cells(ROUTE1_EVENTS))
    return g


def make_kronion():
    g = Grid(KRONION, "Kronion Hill", KRONION_OLIVES, KRONION_CYPRESSES, sea_edges="NE")
    g.roughen(event_cells(KRONION_EVENTS), seed=11)
    return g


def build_route1(cat):
    g = make_route1()
    build_route1_pieces(g, cat)
    g.build(cat)
    g.check()
    return g


def build_kronion(cat):
    g = make_kronion()
    build_kronion_ruins(g, cat)
    g.build(cat)
    g.check()
    return g


def write_shapes():
    """Merge the ground shapes both maps need into agros_shapes.json."""
    old = json.loads(SHAPES.read_text()) if SHAPES.exists() else {}
    merged = {k: set(old.get(k, [])) for k in ("tall", "path", "track")}
    r1, kh = make_route1(), make_kronion()
    build_route1_pieces(r1, None)
    build_kronion_ruins(kh, None)
    for g in (r1, kh):
        for k, keys in g.shapes().items():
            merged[k] |= keys
    out = {k: sorted(v) for k, v in merged.items()}
    SHAPES.write_text(json.dumps(out, indent=1) + "\n")
    print(SHAPES, {k: len(v) for k, v in out.items()})


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
    for y in range(r1.h):
        if not r1.solid(0, y):
            errs.append(f"Route 1: west edge open at y={y}")
    for y in range(kh.h):
        if not kh.solid(kh.w - 1, y):
            errs.append(f"Kronion Hill: east edge open at y={y}")
    for x in range(kh.w):
        if not kh.solid(x, 0) or not kh.solid(x, kh.h - 1):
            errs.append(f"Kronion Hill: top or bottom edge open at x={x}")
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
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset(PRIMARY, syms)),
                           rm.Tileset(rm.resolve_tileset(SECONDARY, syms)))


def render(g, name, events, border, views, rows=None):
    """Plain render, a review copy with collision and events marked, and a sheet of
    15x10-tile screens around the given player positions (border shown past the edges)."""
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer()
    RENDER.mkdir(parents=True, exist_ok=True)
    blocks = g.blocks()[: rows or g.h]
    img = rm.render_blocks(r, blocks.ravel(), g.w)
    img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(RENDER / f"{name}.png")

    s = 3
    rev = img.resize((img.width * s, img.height * s), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", rev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    font = ImageFont.load_default(size=11)
    cell = 16 * s
    for y in range(blocks.shape[0]):
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
    for i in range(max(g.w, blocks.shape[0])):
        if i < g.w:
            d.text((i * cell + cell // 2 - 6, 0), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0, 255))
        if i < blocks.shape[0]:
            d.text((2, i * cell + cell // 2 - 6), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(rev, over).convert("RGB").save(RENDER / f"{name}_review.png")

    # Screens: the GBA shows 15x10 tiles with the player at column 7, row 5.
    pad = 8
    H = blocks.shape[0]
    W, HH = g.w + 2 * pad, H + 2 * pad
    big = np.zeros((HH, W), np.uint16)
    for y in range(HH):
        for x in range(W):
            big[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
    big[pad:pad + H, pad:pad + g.w] = blocks & 0x3FF
    full = rm.render_blocks(r, big.ravel(), W)
    shots = []
    for (px, py) in views:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16
        shots.append(full.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
    cols = 3
    nrows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 488 + 8, nrows * 328 + 8), (24, 24, 32))
    for i, sh in enumerate(shots):
        sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
    sheet.save(RENDER / f"{name}_screens.png")
    return [RENDER / f"{name}.png", RENDER / f"{name}_review.png", RENDER / f"{name}_screens.png"]


ROUTE1_BORDER = [SEA, SEA, SEA, SEA]
KRONION_BORDER = [SEA, SEA, SEA, SEA]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--shapes", action="store_true", help="update tools/ichor/art/agros_shapes.json and stop")
    args = ap.parse_args()
    if args.shapes:
        write_shapes()
        return
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
        for p in render(r1, "kalliste_route1", ROUTE1_EVENTS, ROUTE1_BORDER, ROUTE1_VIEWS):
            print(p)
        for p in render(kh, "kalliste_route1_kronion_hill", KRONION_EVENTS, KRONION_BORDER, KRONION_VIEWS, rows=20):
            print(p)


if __name__ == "__main__":
    main()
