#!/usr/bin/env python3
"""Build Route 1 and Kronion Hill (the summit and its high pastures): layouts, borders and events.

Both maps are drawn below as ASCII grids on gTileset_Aethos + gTileset_Agros,
with the interior olives listed as anchors and the bigger set pieces (the big
olive, the cart, the bee wall, the springs, the shrines, the threshing floor and
Kronion's ruins) placed in code. This script auto-tiles them:

  - tall grass and the road get soft, curving edges from Agros's shape pieces;
    a grass cell in a stair-step corner becomes a diagonal "half cell". Agros
    holds only the shapes the maps use and its tiles are nearly spent, so the
    grass's edges are nudged a cell at a time to shapes it already has
    (Grid.snap_shapes)
  - field walls join in any direction; the hill's rock bands end in slopes
  - olives get crown tips above and soft shade below; '%' woods fill with a
    staggered mix of olives, stone pines, figs, cypresses, rocks and shrubs
  - the rocky shore picks its piece by where the sea is

check_route() proves MAP_DESIGN's rules on the built maps: the forced bands,
the checkpoint trainers' lines, a clear climb to the summit, and no ledge that
traps a player.

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
SOLID_TIP = (0x1E8, 0x1E9)     # the tip over "ledge grass": drawn the same, used for gaps inside the woods
CYPRESS_TOP, CYPRESS_TOP_TALL, CYPRESS_BOTTOM = 0x00E, 0x025, 0x016
CYPRESS_BOTTOM_TIP = (0x1F4, 0x1F5)    # a cypress foot over an olive crown's left / right half
# An olive's crown pokes 3 px into the cell above it, so that cell must draw the
# tip. Olive top halves, and the cells that draw a left / right tip, in aethos:
OLIVE_TOP_L, OLIVE_TOP_R = {0x1D4, 0x1D6, 0x1FC}, {0x1D5, 0x1D7, 0x1FD}
TIP_L = {0x1DC, 0x1DE, 0x1F2, 0x1CE, 0x1C6, 0x1E8, 0x1EA, 0x1EE, 0x1F0, 0x1F6, 0x1FE, 0x1F4}
TIP_R = {0x1DD, 0x1DF, 0x1F3, 0x1CF, 0x1C7, 0x1E9, 0x1EB, 0x1EF, 0x1F1, 0x1F7, 0x1FF, 0x1F5}
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


BLOCKING = "OCPFQ#WTsjHS=~dRB_Zzqbnr^"
HALF_LETTERS = {"a": ((0, -1), (1, 0), (1, -1)), "b": ((0, 1), (1, 0), (1, 1)),
                "c": ((0, 1), (-1, 0), (-1, 1)), "d": ((0, -1), (-1, 0), (-1, -1))}


class Grid:
    def __init__(self, rows, name, olives=(), cypresses=(), pines=(), sea_edges="", above=None, below=None,
                 seam_rows=()):
        self.name = name
        self.sea_edges = sea_edges        # map edges the sea lies beyond: some of "NESW"
        # The neighbor's metatiles just past the top / bottom edge (seams), or None.
        self.above, self.below = above, below
        # Rows a player in a neighboring map can see. The game draws a connected
        # map with the tilesets of the map the player stands on, so these rows use
        # aethos (primary) metatiles only: Agros pieces would show as the
        # neighbor's secondary tiles. See seam_prep.
        self.seam_rows = set(seam_rows)
        self.filled = {}                  # woods cells fill_woods chose: (x, y) -> (kind, top-left)
        self.cut_ok = set()               # olives whose crown is knowingly left flat
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
        self.seam_prep()
        self.fill_woods()
        self.settle_crowns()
        self.open_edge_gaps()
        self.cells = np.zeros((self.h, self.w), np.uint32)
        self.done = np.zeros((self.h, self.w), bool)
        self.half = {}            # (x, y) -> ("path" | "tall", letter)
        self.protect = set()

    # --- composition passes ------------------------------------------------
    SEAM_SWAP = {"h": ".", "y": ".", "b": "B", "n": "B", "r": "B", "q": "~"}

    def seam_prep(self):
        """In the seam rows, swap what only Agros can draw for aethos's own:
        herbs become grass, shrubs and rocks become boulders, the rocky shore
        becomes open sea. Woods there fill with olives, stone pines, cypresses
        and boulders only; tall grass takes aethos's plain barley and the road
        aethos's square-edged path patch (soft_ground)."""
        for y in self.seam_rows:
            for x in range(self.w):
                c = self.chars[y][x]
                if c in self.SEAM_SWAP:
                    self.chars[y][x] = self.SEAM_SWAP[c]
                elif c in "FQ-W_TsZz":
                    sys.exit(f"{self.name}: '{c}' at ({x},{y}) is in a seam row, where only aethos pieces may go")

    def fill_woods(self):
        """Fill '%' with a staggered mix: olives, stone pines, figs and rock
        outcrops in 2x2 blocks, cypresses in pairs, broom, oleander and rocks
        in the gaps, so wood edges never read as a column of one tree.

        It fills bottom up, so it always knows which cells must draw the crown
        tip of an olive below (an olive's crown pokes 3 px into the cell above).
        Over an olive it stacks another olive exactly, or puts cypresses, whose
        feet draw the tip; when the olive below sits one column over, it fills a
        single column first so the next block lines up. An olive only goes
        where the cells over its own crown can draw the tip later."""
        free = lambda x, y: self.ch(x, y) == "%"
        tops, _ = self.olive_blocks()
        need = {}                         # cell -> 0 / 1: must draw an olive tip's left / right half
        for x, y in tops + self.seam_olives():
            for i in (0, 1):
                need[(x + i, y - 1)] = i

        def crown_clear(x, cy):
            """Can (x, cy) and (x + 1, cy) draw the tip of an olive below them?"""
            if cy < 0:
                if self.above is None:
                    return True
                return all(x + i < len(self.above) and self.above[x + i] in (TIP_L, TIP_R)[i] for i in (0, 1))
            return all(self.ch(x + i, cy) in "%.," for i in (0, 1))

        def mark(cells, kind, tag, top_left):
            for cx, cy in cells:
                self.chars[cy][cx] = kind
                self.filled[(cx, cy)] = (tag, top_left)

        def column(x, y):
            """A one-wide filling at (x, y): a cypress if there is room, else a shrub
            or, under a crown, a gap the crown's tip fills."""
            if free(x, y - 1) and (need.get((x, y)) is not None or hashpct(x, y, 1) < 40):
                mark([(x, y - 1), (x, y)], "C", "C", (x, y - 1))
            elif need.get((x, y)) is not None:
                mark([(x, y)], "^", "1", (x, y))
            elif y in self.seam_rows:
                mark([(x, y)], "B", "1", (x, y))          # aethos's boulder
            else:
                k = hashpct(x, y, 3)
                mark([(x, y)], "b" if k < 35 else "n" if k < 60 else "r", "1", (x, y))

        for y in range(self.h - 1, -1, -1):
            for x in range(self.w):
                if not free(x, y):
                    continue
                nl, nr = need.get((x, y)), need.get((x + 1, y))
                square = y >= 1 and free(x + 1, y) and free(x, y - 1) and free(x + 1, y - 1)
                block = [(x, y - 1), (x + 1, y - 1), (x, y), (x + 1, y)]
                if nl == 1 or (nl == 0 and nr != 1) or (nl is None and nr == 0):
                    column(x, y)          # line up with the olive below, or tip its right half
                elif nl == 0:             # an olive exactly below: stack one, or two cypresses
                    if square and crown_clear(x, y - 2) and hashpct(x, y, 5) < 80:
                        mark(block, "O", "2x2", (x, y - 1))
                        need[(x, y - 2)], need[(x + 1, y - 2)] = 0, 1
                    else:
                        column(x, y)
                        if free(x + 1, y):
                            column(x + 1, y)
                elif square and hashpct(x, y, 1) >= 16:
                    k = hashpct(x, y, 2)
                    kind = "P" if k < 15 else "F" if k < 25 else "Q" if k < 33 else "O"
                    if kind == "O" and not crown_clear(x, y - 2):
                        kind = "PFQ"[k % 3]
                    if kind in "FQ" and (y in self.seam_rows or y - 1 in self.seam_rows):
                        kind = "P"                            # figs and outcrops are Agros pieces
                    mark(block, kind, "2x2", (x, y - 1))
                    if kind == "O":
                        need[(x, y - 2)], need[(x + 1, y - 2)] = 0, 1
                else:
                    column(x, y)

    OPEN = ".,=-*hyd"                     # ground a player walks on

    def open_edge_gaps(self):
        """A gap ('^') on the north edge of the woods draws an olive's crown tip
        over grass, so it looks walkable. When open ground lies only to its
        north, it becomes grass the player can step into, behind the crown; a
        gap beside open ground any other way stays solid, so no new path opens
        through the woods. Gaps inside the woods stay solid and draw their tip
        with aethos's twin of the grass tip (see trees), so each tip metatile
        is either always open or always solid."""
        src = [r[:] for r in self.chars]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != "^" or not (0 < x < self.w - 1):
                    continue
                opened = [(dx, dy) for dx, dy in STEPS
                          if 0 <= x + dx < self.w and 0 <= y + dy < self.h and src[y + dy][x + dx] in self.OPEN]
                if opened == [(0, -1)]:
                    self.chars[y][x] = "."

    # --- olive crowns -----------------------------------------------------------
    def olive_blocks(self):
        """Top-left cells of the 2x2 olives, and each olive cell's top-left."""
        owner, tops = {}, []
        for y in range(self.h):
            for x in range(self.w):
                if self.chars[y][x] != "O" or (x, y) in owner:
                    continue
                cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                if any(self.ch(cx, cy) != "O" or (cx, cy) in owner for cx, cy in cells):
                    sys.exit(f"{self.name}: olive at ({x},{y}) is not a free 2x2 block\n{self.ascii()}")
                for c in cells:
                    owner[c] = (x, y)
                tops.append((x, y))
        return tops, owner

    def seam_olives(self):
        """The neighbor's olives that start on its first row past the bottom edge."""
        b = self.below
        if b is None:
            return []
        return [(x, self.h) for x in range(min(self.w, len(b)) - 1) if b[x] in OLIVE_TOP_L and b[x + 1] in OLIVE_TOP_R]

    def cypress_foot(self, x, y):
        """Is (x, y) the lower half of a cypress? Cypresses stack in pairs."""
        if self.ch(x, y) != "C":
            return False
        k = 0
        while self.ch(x, y - k - 1) == "C":
            k += 1
        return k % 2 == 1

    def crown_ok(self, cx, cy, x, y, owner):
        """Can the cell above an olive's crown half draw the crown's tip?"""
        if cy < 0:
            if self.above is None:
                return True
            m = self.above[cx] if cx < len(self.above) else None
            return m in (TIP_L if cx == x else TIP_R)
        c = self.ch(cx, cy)
        if c in ".,^":
            return True                                 # a tip over grass or tall grass
        if c == "O":
            return owner.get((cx, cy)) == (x, y - 2)    # an olive stacked exactly above
        return self.cypress_foot(cx, cy)

    def settle_crowns(self):
        """Every olive needs a cell above its crown that can draw the crown's tip:
        grass, an olive stacked exactly above, or a cypress foot. The woods
        fill_woods chose give way, bottom up: a 2x2 over an olive becomes an olive
        stacked on it or two cypresses, and an olive under something fixed (the
        road, a wall, a seam without tips) becomes two cypresses itself. The
        neighbor's olives just past the bottom seam count as fixed olives."""
        def to_cypresses(bx, by):
            for cx, cy in ((bx, by), (bx + 1, by), (bx, by + 1), (bx + 1, by + 1)):
                self.chars[cy][cx] = "C"
                self.filled[(cx, cy)] = ("C", (cx, by))
        for _ in range(10000):
            tops, owner = self.olive_blocks()
            work = self.seam_olives() + sorted(tops, key=lambda t: -t[1])
            for (x, y) in work:
                if (x, y) in self.cut_ok:
                    continue
                bad = [(x + i, y - 1) for i in (0, 1) if not self.crown_ok(x + i, y - 1, x, y, owner)]
                if not bad:
                    continue
                cx, cy = bad[0]
                src = self.filled.get((cx, cy))
                mine = self.filled.get((x, y))
                if src and src[0] == "2x2":
                    bx, by = src[1]
                    if (bx, by) == (x, y - 2) and hashpct(bx, by, 5) < 60:
                        for c2x, c2y in ((bx, by), (bx + 1, by), (bx, by + 1), (bx + 1, by + 1)):
                            self.chars[c2y][c2x] = "O"
                    else:
                        to_cypresses(bx, by)
                elif mine and mine[0] == "2x2":
                    to_cypresses(x, y)
                elif src and src[0] == "1":
                    self.chars[cy][cx] = "^"        # the shrub gives way to a gap the crown fills
                else:
                    print(f"{self.name}: olive ({x},{y}) keeps a flat crown under "
                          f"'{self.ch(cx, cy, '^')}' at ({cx},{cy})")
                    self.cut_ok.add((x, y))
                break
            else:
                return
        sys.exit(f"{self.name}: settle_crowns did not settle")

    def roughen(self, protect, seed=7, keep_rows=()):
        """Break the straight edges of the drawn tall-grass patches with smooth
        noise. Never on event cells, so trainers, items and signs keep their
        ground; never in the forced bands' rows (keep_rows), so a band keeps its
        full depth; never in the seam rows, which take no Agros grass."""
        self.protect = set(protect)
        skip = set(keep_rows) | self.seam_rows
        src = [r[:] for r in self.chars]
        def near(x, y):
            return any(0 <= x + dx < self.w and 0 <= y + dy < self.h and src[y + dy][x + dx] == ","
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in protect or y in skip:
                    continue
                n = noise(x, y, seed)
                c = src[y][x]
                edge = c == "," and any(0 <= x + dx < self.w and 0 <= y + dy < self.h and src[y + dy][x + dx] == "."
                                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if edge and n < -0.3:
                    self.chars[y][x] = "."
                elif c == "." and near(x, y) and n > 0.35:
                    self.chars[y][x] = ","

    def unknown_shapes(self, have):
        """Cells whose soft-ground shape Agros doesn't hold (have: kind -> keys)."""
        self.half = {}
        self.find_halves()
        bad = []
        for y in range(self.h):
            if y in self.seam_rows:
                continue
            for x in range(self.w):
                c, h = self.chars[y][x], self.half.get((x, y))
                for kind, ch in (("tall", ","), ("path", "=")):
                    if c == ch or (h and h[0] == kind):
                        k = self.shape_key(kind, ch, x, y)
                        if k != "1|11111111" and k not in have[kind]:
                            bad.append((x, y))
                if c == "-" and self.track_key(x, y) not in have["track"]:
                    bad.append((x, y))
        return bad

    def snap_shapes(self, cat, keep_rows=()):
        """Agros holds only the ground shapes its maps use, and its tiles are
        nearly all spent. So instead of growing it, nudge the tall grass's edges
        a cell at a time (grass to meadow or back, never on an event, a forced
        band's rows or a seam row) until every shape is one Agros already has.
        Each step takes the nudge near the first odd cell that leaves the fewest
        odd cells, preferring to add grass. Without a catalog it does nothing."""
        if cat is None:
            return
        have = {k: set(cat[k]["names"]) for k in ("tall", "path", "track")}
        frozen = set(self.protect) | {(x, y) for y in set(keep_rows) | self.seam_rows for x in range(self.w)}
        bad = self.unknown_shapes(have)
        while bad:
            best = None
            for x0, y0 in bad:
                for dy in (0, -1, 1):
                    for dx in (0, -1, 1):
                        x, y = x0 + dx, y0 + dy
                        c = self.ch(x, y)
                        if (x, y) in frozen or c not in (".", ","):
                            continue
                        self.chars[y][x] = "." if c == "," else ","
                        n = len(self.unknown_shapes(have))
                        self.chars[y][x] = c
                        if best is None or (n, c == ",") < (best[0], best[3] == ","):
                            best = (n, x, y, c)
                if best is not None and best[0] < len(bad):
                    break                 # this cell's nudge helps: take it
            if best is None or best[0] >= len(bad):
                break
            _, x, y, c = best
            self.chars[y][x] = "." if c == "," else ","
            bad = self.unknown_shapes(have)
        if bad:
            sys.exit(f"{self.name}: no nudge fits these cells' shapes to Agros: {bad[:8]}")

    def find_halves(self):
        """Grass cells in a stair-step corner of the road or a meadow become half
        cells, cutting the corner on the diagonal. The road wins ties."""
        tops, _ = self.olive_blocks()
        crowns = {(x + i, y - 1) for x, y in tops for i in (0, 1)}   # these draw a crown tip instead
        for kind, ch in (("path", "="), ("tall", ",")):
            for y in range(self.h):
                for x in range(self.w):
                    if self.chars[y][x] != "." or (x, y) in self.half or (x, y) in self.protect or (x, y) in crowns \
                            or y in self.seam_rows:
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
            if y in self.seam_rows:
                continue                    # aethos's own pieces there (soft_ground)
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
        tops, _ = self.olive_blocks()
        top_set = set(tops) | set(self.seam_olives())
        self.crown_feet = {}              # cell above an olive crown -> 0 (left half) or 1 (right)
        for x, y in top_set:
            for i in (0, 1):
                self.crown_feet[(x + i, y - 1)] = i
        for x, y in tops:
            self.put(x, y, block(OLIVE_TOP[0]))
            self.put(x + 1, y, block(OLIVE_TOP[1]))
            pair = OLIVE_BOTTOM_TIP if (x, y + 2) in top_set else OLIVE_BOTTOM
            self.put(x, y + 1, block(pair[0]))
            self.put(x + 1, y + 1, block(pair[1]))
        for x, y in top_set:
            for i in (0, 1):
                ax, ay = x + i, y - 1
                if ay < 0 or self.ch(ax, ay) not in (".", ",", "^") or self.done[ay, ax] or (ax, ay) in self.half:
                    continue
                # '^' is a gap in the woods: a tip over grass, but as solid as the trees
                if self.ch(ax, ay) == "^":
                    self.put(ax, ay, block(SOLID_TIP[i]))
                else:
                    self.put(ax, ay, walk(OLIVE_TIP["tall" if self.ch(ax, ay) == "," else "grass"][i]))
        return tops

    def shades(self, cat, tops):
        """Soft shade on the grass under each olive."""
        for x, y in tops:
            cells = [(x, y + 2), (x + 1, y + 2)]
            if all(self.ch(cx, cy) == "." and not self.done[cy, cx] and (cx, cy) not in self.half
                   and (cx, cy) not in self.protect and cy not in self.seam_rows for cx, cy in cells):
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
                half = self.crown_feet.get((x, y + 1))
                self.put(x, y + 1, block(CYPRESS_BOTTOM if half is None else CYPRESS_BOTTOM_TIP[half]))

    AETHOS_PATH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
                   "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}

    def aethos_path(self, x, y):
        """A seam-row road cell from aethos's square path patch. Past the map's
        edge the road carries on as at the edge (it continues into the neighbor)."""
        road = lambda dx, dy: self.clamp_ch(x + dx, y + dy) == "="
        v = "" if road(0, -1) else "T"
        v = v if road(0, 1) else "B"  if not v else v
        if not road(0, -1) and not road(0, 1):
            v = "T"
        h = "" if road(-1, 0) else "L"
        h = h if road(1, 0) else "R"
        key = (v + h) or "C"
        return self.AETHOS_PATH.get(key, self.AETHOS_PATH["C"])

    def soft_ground(self, cat):
        """Tall grass, road and track, from Agros's shape pieces (aethos's own
        path patch in the seam rows)."""
        for y in range(self.h):
            for x in range(self.w):
                if self.done[y, x]:
                    continue
                c, h = self.chars[y][x], self.half.get((x, y))
                kind = h[0] if h else {",": "tall", "=": "path", "-": "track"}.get(c)
                if not kind:
                    continue
                if y in self.seam_rows:
                    self.put(x, y, walk(TALL if kind == "tall" else self.aethos_path(x, y)))
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
# leaves the east edge at y=18-19. The border is open sea. Built to
# design/MAP_DESIGN.md: check_route() proves the rules below hold.
#
# The walk north, beat by beat:
#   out of Elaia between olive groves, straight into grass (band 1, 2 deep)
#   the carter resting by her cart; a walled patch with a hidden Repel
#   Tityros at the meadow wall's only gap: the first trainer, in plain view
#   the shepherd's meadow and the threshing floor; a lip back down for the return
#   Thestylis at the grove narrows' mouth, her line across its narrowest row;
#     the narrows (band 2, 3 deep); a west walk with a Poke Ball, and a lip
#     back into the meadow
#   Phyllis's grove: a spring under a fig, Phyllis on the lane by her seed
#   the ancient olive; the bee terraces climbing east (Komatas, optional)
#   the fork: a herm, the spur east to Kronion Hill past Polyeidos
#   the flock in the wall gap, Agis just past it
#   shore grass across the cove (band 3, 3 deep); a jar on the beach
#   the climb: steps up to the headland and the north herm; a goat path of
#     two lips behind the hedge, past a wayside shrine, makes the trip back quick
# Rows 0-5 and 58-63 are seen from Akti and Elaia, which draw them with their
# own secondary tileset, so they hold aethos pieces only (Grid.seam_prep).
# ---------------------------------------------------------------------------
ROUTE1 = [
    # 0         1         2
    # 012345678901234567890123456789
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 0  north seam to Akti (rows 0-4: aethos only)
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 1
    "%%%%%%....====.....%%%%%%%%%%%",  # 2  Akti's outskirts on the headland
    "%%%%%.*...====..H...%%%%%%%%%%",  # 3  north herm
    "~ddd...*..====......%%%%%%%%%%",  # 4
    "~~ddd.....====........%%%%%%%%",  # 5  cypresses on the headland
    "~~~dd.....====........%%%%%%%%",  # 6
    "~~~~TTTTTTssssTT___TTT%%%%%%%%",  # 7  the climb: steps up to the headland; a lip down the goat path
    "~~~~dd,,..====.%...%%%%%%%%%%%",  # 8  the goat path runs down behind the hedge
    "~~~~,,,,,,,,,,,%..#%%%%%%%%%%%",  # 9  shore grass, from the sea to the hedge (band 3);
    "~~~~~,,,,,,,,,,%..#%%%%%%%%%%%",  # 10 a wayside shrine on the goat path
    "~~~~,,,,,,,,,,,%.y.%%%%%%%%%%%",  # 11
    "~~~~dd.,,,====.%___%%%%%%%%%%%",  # 12 the goat path's last lip
    "~~~ddd.....===.....%%%%%%%%%%%",  # 13 Agis watches the gap; a jar on the cove beach
    "%%WWBWWWWWW===WWWWWWWB%%%%%%%%",  # 14 the flock's wall gap
    "%%.,,,.....===.....###%%%%%%%%",  # 15 Amaryllis; the fallen column
    "%%..,,,....===..h..###C.%%%%%%",  # 16
    "%%.,,,,....=====...###C..%%%%%",  # 17 Polyeidos above the spur
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
    "%%.----.....===..,,.........%%",  # 34 the spring's track; Phyllis on the lane
    "%%.,,,------===...,...,.....%%",  # 35
    "%%..,,......===.......,.....%%",  # 36
    "%%..........===.............%%",  # 37
    "%%......%,,,,,,,%%%%%%%%%%%%%%",  # 38 the grove narrows (band 2); the west walk
    "%%......%,,,,,,%%%%%%%%%%%%%%%",  # 39
    "%%..,...%%,,,,,.%%%%%%%%%%%%%%",  # 40 Thestylis at the narrows' mouth
    "%%______%%===..............%%%",  # 41 the west walk's lip down to the meadow
    "%%..,,,...===....,,,..h......%",  # 42 the shepherd's meadow
    "%%.,,,,...===...,,,,.....,...%",  # 43
    "%%..,,,..===......####..*....%",  # 44 the threshing floor
    "%%.,,,...===..----####.......%",  # 45
    "%%..,....===---...####.....*.%",  # 46
    "%%.......===......####B......%",  # 47
    "%%..*....===..h............,.%",  # 48
    "%%.......===.*......,,,....h.%",  # 49 Tityros at the wall gap
    "%%WWWWWWW===WWWWWWWW_______W%%",  # 50 the meadow wall; a lip back down
    "%%.,,,,..===.................%",  # 51
    "%%WWWWW..===...........B.....%",  # 52 youth on the wall
    "%%,,,,,,..===.....###........%",  # 53 the cart
    "%%,,,,,,..===.....###..*.....%",  # 54
    "%%.,,,,...===......dd........%",  # 55 the carter
    "%%..,,...H===................%",  # 56 south herm
    "%%%%%%%,,,,,,,,,%%%%%%%%%%%%%%",  # 57 the first grass out of Elaia (band 1)
    "%%%%%%%%,,,,,,,%%%%%%%%%%%%%%%",  # 58
    "%%%%%%%%%.====.%%%%%%%%%%%%%%%",  # 59 rows 59-63: aethos only
    "%%%%%%%%%%====.%%%%%%%%%%%%%%%",  # 60
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 61
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 62
    "%%%%%%%%%%====%%%%%%%%%%%%%%%%",  # 63 south seam to Elaia
]

ROUTE1_OLIVES = [
    # the fork
    (2, 16), (19, 29),
    # Phyllis's grove, in loose rows either side of her lane (y=34)
    (15, 31), (19, 31), (23, 31), (16, 35), (20, 35), (24, 36),
    # the meadow: the shepherd's lone olive, scrub to the east
    (6, 47), (24, 42), (25, 47),
    # the carter's shade trees
    (15, 54), (25, 53),
]
# An olive's crown needs grass, another olive or a cypress foot above it (see
# settle_crowns), so none sits right under the road, a wall, a lip or a pine.
ROUTE1_CYPRESSES = [(7, 2), (19, 5), (21, 5), (21, 20), (10, 36), (15, 42), (7, 54)]
# Rows a player still in Akti or Elaia can see: the screen shows four and a
# half rows either side of the player's tile, and a step scrolls one more in
# before the map switches. So six rows each side stay aethos-only.
ROUTE1_SEAM_ROWS = list(range(0, 6)) + list(range(58, 64))
# The forced bands' rows, kept out of roughen() so each keeps its full depth.
ROUTE1_BAND_ROWS = [9, 10, 11, 38, 39, 40, 57, 58]
ROUTE1_PINES = [(21, 55), (26, 55)]

# ---------------------------------------------------------------------------
# Kronion Hill, east of Route 1 (connection offset 2: this map's row 0 is
# Route 1's row 2). 24 x 62. Classed a dungeon (map.json "ichor_kind"): the
# ruined sanctuary is beat 5's story place, the flock holds the Akti road until
# its scene plays, and the dark stair in the pit leads down to the Kronion crypt.
#
# The climb (the main line): from the hill foot (y=16-17, Route 1's 18-19) a
# stair climbs a band of rock, the path doubles back along a shelf to a second
# stair, and the shrine's stylobate stands on top, at the edge of a cliff over
# the sea.
#
# The high pastures (a branch off the hill foot, past the herm): the hill's
# south flank, three terraces stepping down to the sea cliffs on the east.
#   the goat path down; Menalkas at its foot, in plain view
#   the upper pasture and the shepherds' fold
#   steps, or a lip by the fold, down to the spring: Thyrsis sings beside it,
#     facing the water; Pan's shrine; olive terraces with a Burn Heal
#   steps, or a lip, down to the goat terraces; Lykidas above the stair in
#     the rock band, and below it the lookout shelf: the Everstone, and a
#     feather on the tip of the point
# Below the terraces the rows are the hill's woods: Route 1 shows this map
# past its east edge, so it covers every row a player there can see.
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
    "%%%C....======....q~~~~~",  # 9  the worn path forks to the two gaps in the step
    "%%,C........==S...q~~~~~",  # 10 the scene starts at the stair's top (13,10)
    "%%ZZZZZZZZZZZzZZZZq~~~~~",  # 11 upper rock band, stair at x=13
    "%%QQ,.r..,,,==,,.Bq~~~~~",  # 12 the shelf: the path climbs it on the diagonal,
    "%%QQ,,===,,,y..b..q~~~~~",  # 13 through grass across the whole shelf (x=9-11)
    "%%.,,===rZZZZZZZZZ%qq~~~",  # 14 lower band, east half; the sea cliffs turn south
    "%%ZZZZzZZZZ%%%%%%%%%q~~~",  # 15 lower band, west half, stair at x=6
    "===,,==.%%%%%%%%%%%%q~~~",  # 16 hill foot, from Route 1: grass across the path, then
    "===,,,,.H%%%%%%%%%%q~~~~",  # 17 the path runs on to the stair; the herm at the fork
    "%%%%%,,.%%%%%%%%%%%q~~~~",  # 18 the goat path down to the pastures
    "%%%%%.......%%%%%%%%q~~~",  # 19 Menalkas at its foot (9,19)
    "%%%%..,*.....,,,%%%%.q~~",  # 20 the upper pasture
    "%%WWWWW..,,,,,,,%%r..q~~",  # 21 the shepherds' fold
    "%%W...W.,,,,,,,,,..*.q~~",  # 22
    "%%W......,,,,,,,..y.q~~~",  # 23 the fold's gate (6,23)
    "%%W...W.h,,,,...%%..q~~~",  # 24
    "%%WWWWW.*.,,.....%%q~~~~",  # 25
    "%%%TTTTsT%%TTT___TT%q~R~",  # 26 terrace walls: steps (7,26), a lip (14-16,26)
    "%%###...#..,,,....,,.q~~",  # 27 the spring under a stone pine; Pan's shrine
    "%%###...#.,,,,,....,.q~~",  # 28
    "%%.......,,,,,.,,,,.q~~~",  # 29 Thyrsis at the spring (3,29)
    "%%..y...,,,,,...,,,.q~~~",  # 30 the olive terraces
    "%%..h..*.,,......*...q~~",  # 31
    "%%..*..h.....,,,,..,.q~~",  # 32
    "%%.,,,..y...,,,,,,,,q~R~",  # 33
    "%%,,,,,.....,,,,,..q~~~~",  # 34 a Burn Heal (18,34)
    "%%.,,....h.......,,q~~~~",  # 35
    "%%%TTTsTT%%%TT___T%%q~~~",  # 36 terrace walls: steps (6,36), a lip (14-16,36)
    "%%...r.----.yy....b.q~~~",  # 37 the goat terraces: a worn track steps down to Lykidas
    "%%.,,,,,..----.r.....q~~",  # 38
    "%%,,,,,,,..QQ----.b..q~~",  # 39
    "%%.,,,,,.h.QQ..*....q~~R",  # 40 Lykidas (17,40) above the stair
    "%%%%%%%%ZZZZ%%ZZzZZZq~~~",  # 41 a band of rock, broken by a clump of shrubs; stair at x=16
    "%%%%%%%%%%..y.*..,...q~~",  # 42 the lookout shelf: the Everstone (11,44)
    "%%%%%%%%%r.....*......q~",  # 43 the point (22,43)
    "%%%%%%%%%%%.......h...q~",  # 44
    "%%%%%%%%%%%%%%%......q~~",  # 45
    "%%%%%%%%%%%%%%%%%%%%q~~~",  # 46
] + ["%%%%%%%%%%%%%%%%%%%q~~~~"] * 15  # 47-61: the hill's foot woods, seen past Route 1's east edge
KRONION_OFFSET = 2
KRONION_SHOWN = 48          # rows the review renders show: the summit and the pastures
KRONION_BAND_ROWS = [12, 13, 16, 17, 18]
KRONION_OLIVES = [(8, 23), (11, 31), (15, 30), (16, 33)]
KRONION_CYPRESSES = []
KRONION_PINES = [(5, 27), (18, 22), (17, 43)]


def build_route1_pieces(g, cat):
    """Route 1's set pieces."""
    g.slabs(cat, 19, 15, 21, 17)                      # a fallen column by the spur
    g.place(cat, "ruin_columns", 20, 15, 0, 0, 1, 3)
    g.place(cat, "big_olive", 3, 22)                  # the ancient olive
    g.place(cat, "bee_wall", 22, 24)                  # Komatas's hives
    g.place(cat, "spring", 2, 32)                     # the spring in the grove
    g.place(cat, "shrine", 18, 9)                     # the wayside shrine on the goat path
    g.place(cat, "alonia", 18, 44)                    # the threshing floor
    g.place(cat, "cart", 18, 53)                      # the carter's cart


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


def build_kronion_pastures(g, cat):
    """The high pastures' set pieces."""
    g.place(cat, "spring", 2, 27)                     # the spring Thyrsis sings to
    g.place(cat, "shrine", 8, 27)                     # Pan's shrine


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
MAREEP = "OBJ_EVENT_GFX_SPECIES(MAREEP)"
SKIDDO = "OBJ_EVENT_GFX_SPECIES(SKIDDO)"
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
        obj(P + "WOMAN", 17, 55, R1 + "Carter", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_ROUTE1_CARTER"),
        obj("OBJ_EVENT_GFX_SPECIES(MUDBRAY)", 17, 54, R1 + "Mudbray", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(P + "YOUTH_M", 5, 52, R1 + "WallYouth", "MOVEMENT_TYPE_FACE_DOWN"),
        # the first trainer: at the meadow wall's only gap, in plain view
        obj(P + "SHEPHERD", 12, 49, R1 + "Tityros", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3),
        obj(WOOLOO, 4, 44, R1 + "GrazingWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        obj(WOOLOO, 3, 47, R1 + "GrazingWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        item_ball(3, 39, "ITEM_POKE_BALL", "FLAG_ICHOR_ITEM_ROUTE1_POKE_BALL"),
        # the second checkpoint: at the grove narrows' south mouth, her line across its narrowest row
        obj(P + "HARVESTER", 15, 40, R1 + "Thestylis", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=5),
        # optional: she watches her lane, off the road
        obj(P + "HARVESTER", 25, 34, R1 + "Phyllis", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=5),
        item_ball(27, 35, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_ITEM_ROUTE1_MIRACLE_SEED"),
        obj(P + "MAN", 7, 25, R1 + "OliveFarmer", "MOVEMENT_TYPE_FACE_LEFT"),
        # optional: up on the bee terraces
        obj(P + "GOATHERD", 18, 25, R1 + "Komatas", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1),
        # mandatory for Kronion Hill: his line covers both rows of the spur
        obj(P + "AUGUR", 24, 17, R1 + "Polyeidos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
        obj(P + "YOUTH_F", 10, 15, R1 + "Amaryllis", "MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_ROUTE1_AMARYLLIS"),
        obj(WOOLOO, 11, 14, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        obj(WOOLOO, 12, 14, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        obj(WOOLOO, 13, 14, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        obj(WOOLOO, 12, 12, R1 + "FlockWooloo", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_ICHOR_HIDE_ROUTE1_FLOCK"),
        # the hoplite holding the pass, just north of the flock's gap. He stands
        # west of it, looking east across the gap: east of it, (14,13) is the
        # only way out of the goat path's last lip, and a beaten trainer never
        # moves (QA: standing there he walled in anyone who hopped the lip)
        obj(P + "HOPLITE", 9, 13, R1 + "Agis", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=4),
        item_ball(4, 13, "ITEM_POTION", "FLAG_ICHOR_ITEM_ROUTE1_POTION"),
    ],
    "warp_events": [],
    "coord_events": [],
    "bg_events": [
        sign(9, 56, R1 + "HermSouth"),
        sign(14, 20, R1 + "HermFork"),
        sign(16, 3, R1 + "HermNorth"),
        hidden(4, 25, "ITEM_ORAN_BERRY", "FLAG_ICHOR_HIDDEN_ROUTE1_ORAN_BERRY"),
        hidden(2, 54, "ITEM_REPEL", "FLAG_ICHOR_HIDDEN_ROUTE1_REPEL"),
        hidden(4, 29, "ITEM_ANTIDOTE", "FLAG_ICHOR_HIDDEN_ROUTE1_ANTIDOTE"),
    ],
}

# The trainers MAP_DESIGN calls checkpoints: (x, y, facing, sight, the walk their
# line must cut). check_route() proves no path skirts them.
ROUTE1_MANDATORY = {
    "Tityros": (12, 49, "W", 3, "north"),
    "Thestylis": (15, 40, "W", 5, "north"),
    "Agis": (9, 13, "E", 4, "north"),
    "Polyeidos": (24, 17, "S", 2, "kronion"),
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
        # the high pastures, top to bottom
        # the first trainer on the branch: at the goat path's foot, in plain view
        obj(P + "SHEPHERD", 9, 19, KH + "Menalkas", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4),
        obj(WOOLOO, 4, 23, KH + "FoldWooloo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        obj(MAREEP, 3, 22, KH + "FoldMareep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        # optional: he sings to the spring, his back to the path
        obj(P + "SHEPHERD", 3, 29, KH + "Thyrsis", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1),
        item_ball(18, 34, "ITEM_BURN_HEAL", "FLAG_ICHOR_ITEM_KRONION_BURN_HEAL"),
        obj(SKIDDO, 5, 38, KH + "Skiddo", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        # above the only stair down to the lookout shelf
        obj(P + "GOATHERD", 17, 40, KH + "Lykidas", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2),
        item_ball(11, 44, "ITEM_EVERSTONE", "FLAG_ICHOR_ITEM_KRONION_EVERSTONE"),
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
        # the pit's front row: its back row (9-10,6) can't be faced from anywhere
        sign(9, 7, KH + "Pit"),
        sign(10, 7, KH + "Pit"),
        hidden(13, 7, "ITEM_HARD_STONE", "FLAG_ICHOR_HIDDEN_KRONION_HARD_STONE"),
        hidden(10, 4, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_KRONION_STARDUST"),
        sign(8, 17, KH + "HermFork"),
        sign(8, 28, KH + "PanShrine", "BG_EVENT_PLAYER_FACING_NORTH"),
        hidden(22, 43, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_HIDDEN_KRONION_PRETTY_FEATHER"),
    ],
    # Not a route: see the KRONION comment. mapjson ignores the key; map_audit.py reads it.
    "ichor_kind": "dungeon",
}

# The branch's checkpoints: (x, y, facing, sight). check_route() proves every
# walk from the hill foot to what they guard crosses their line.
KRONION_MANDATORY = {
    "Menalkas": (9, 19, "W", 4, [(10, 22)]),            # the upper pasture
    "Lykidas": (17, 40, "W", 2, [(11, 44), (21, 43)]),  # the lookout shelf
}

# Player positions along the route for the screen-sized review crops.
ROUTE1_VIEWS = [(11, 61), (11, 56), (10, 51), (10, 46), (12, 41), (13, 37), (21, 35), (12, 31),
                (12, 25), (19, 25), (12, 20), (23, 19), (12, 16), (12, 13), (9, 8), (11, 3)]
KRONION_VIEWS = [(2, 16), (6, 13), (12, 12), (11, 10), (14, 9), (16, 5),
                 (6, 18), (9, 21), (15, 25), (5, 29), (14, 32), (8, 37), (15, 39), (15, 43)]


# ---------------------------------------------------------------------------
def event_cells(events):
    return {(e["x"], e["y"]) for k in ("object_events", "bg_events", "coord_events") for e in events[k]}


def make_route1():
    # Akti's last row and Elaia's first, as built, so crowns meet across the seams.
    akti, elaia = neighbor("LAYOUT_AKTI_TOWN")[0], neighbor("LAYOUT_ELAIA_VILLAGE")[0]
    g = Grid(ROUTE1, "Route 1", ROUTE1_OLIVES, ROUTE1_CYPRESSES, ROUTE1_PINES, sea_edges="W",
             above=[int(m) & 0x3FF for m in akti[-1]], below=[int(m) & 0x3FF for m in elaia[0]],
             seam_rows=ROUTE1_SEAM_ROWS)
    g.roughen(event_cells(ROUTE1_EVENTS), keep_rows=ROUTE1_BAND_ROWS)
    return g


def make_kronion():
    g = Grid(KRONION, "Kronion Hill", KRONION_OLIVES, KRONION_CYPRESSES, KRONION_PINES, sea_edges="NE")
    g.roughen(event_cells(KRONION_EVENTS), seed=11, keep_rows=KRONION_BAND_ROWS)
    return g


def build_route1(cat):
    g = make_route1()
    build_route1_pieces(g, cat)
    g.snap_shapes(cat, ROUTE1_BAND_ROWS)
    g.build(cat)
    g.check()
    return g


def build_kronion(cat):
    g = make_kronion()
    build_kronion_ruins(g, cat)
    build_kronion_pastures(g, cat)
    g.snap_shapes(cat, KRONION_BAND_ROWS)
    g.build(cat)
    g.check()
    return g


def write_shapes():
    """Merge the ground shapes both maps need into agros_shapes.json."""
    merged = {k: set() for k in ("tall", "path", "track")}    # exactly what the maps use, so Agros stays lean
    r1, kh = make_route1(), make_kronion()
    build_route1_pieces(r1, None)
    build_kronion_ruins(kh, None)
    build_kronion_pastures(kh, None)
    # Fit the grass to the shapes Agros already holds, as the build does, so the
    # list keeps only what the maps use. (A first run, before any catalog, keeps
    # every shape the maps draw.)
    cat = load_catalog() if CATALOG.exists() else None
    r1.snap_shapes(cat, ROUTE1_BAND_ROWS)
    kh.snap_shapes(cat, KRONION_BAND_ROWS)
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
    # The rows Akti and Elaia show (drawn with their own secondary): aethos only.
    b1 = r1.blocks() & 0x3FF
    for y in sorted(r1.seam_rows):
        for x in range(r1.w):
            if b1[y, x] >= 0x200:
                errs.append(f"Route 1: seam row {y} holds Agros metatile {b1[y, x]:#x} at x={x}")
    # Olive crowns: the cell above every olive top half draws its tip, inside
    # each map and across the Akti (north) and Elaia (south) seams, both ways.
    tops = OLIVE_TOP_L | OLIVE_TOP_R
    tip = lambda m, top: m in (TIP_L if top in OLIVE_TOP_L else TIP_R)
    for g in (r1, kh):
        b = g.blocks() & 0x3FF
        for y in range(1, g.h):
            for x in range(g.w):
                if b[y, x] in tops and not tip(b[y - 1, x], b[y, x]):
                    errs.append(f"{g.name}: olive crown cut flat at ({x},{y})")
        for x in range(g.w):
            if g.above is not None and b[0, x] in tops:
                m = g.above[x] if x < len(g.above) else None
                if not tip(m, b[0, x]):
                    errs.append(f"{g.name}: olive crown at ({x},0) cut by the north seam")
            if g.below is not None and x < len(g.below) and g.below[x] in tops and not tip(b[-1, x], g.below[x]):
                errs.append(f"{g.name}: the southern neighbor's olive at x={x} is cut by the seam")
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


def renderer(primary=PRIMARY, secondary=SECONDARY):
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset(primary, syms)),
                           rm.Tileset(rm.resolve_tileset(secondary, syms)))


def neighbor(layout_id):
    """A neighbor's real layout: (blocks h x w, primary, secondary, border)."""
    for lay in json.loads(LAYOUTS.read_text())["layouts"]:
        if lay.get("id") == layout_id:
            w, h = lay["width"], lay["height"]
            blocks = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2").reshape(h, w)
            border = np.fromfile(ROOT / lay["border_filepath"], "<u2")
            return blocks, lay["primary_tileset"], lay["secondary_tileset"], border
    sys.exit(f"no layout {layout_id}")


def render_seams(r1, kh, rows=6):
    """Each seam as the game draws it, every map in its own tilesets: Akti's last
    rows over Route 1's first, Route 1's last over Elaia's first, and Route 1's
    east edge beside Kronion Hill's west edge. Cells no map covers show the
    border of the map the player stands on (both sides are drawn)."""
    from PIL import Image
    rm, r_own = renderer()
    out = []

    def strip(blocks, pair):
        rr = r_own if pair == (PRIMARY, SECONDARY) else renderer(*pair)[1]
        return rm.render_blocks(rr, blocks.ravel(), blocks.shape[1])

    def border_fill(h, w, border, x0=0, y0=0):
        return np.array([[border[((x0 + x) & 1) + ((y0 + y) & 1) * 2] for x in range(w)] for y in range(h)], np.uint16)

    own = r1.blocks() & 0x3FF
    for lid, side in (("LAYOUT_AKTI_TOWN", "N"), ("LAYOUT_ELAIA_VILLAGE", "S")):
        nb, p, s, nborder = neighbor(lid)
        nb = nb & 0x3FF
        w = max(nb.shape[1], r1.w)
        img = Image.new("RGB", (w * 16 + 8, rows * 2 * 16), (24, 24, 32))
        far = nb[-rows:] if side == "N" else nb[:rows]
        near = own[:rows] if side == "N" else own[-rows:]
        # Seen from Route 1: the neighbor where it reaches, Route 1's border past it.
        if far.shape[1] < w:
            pad = border_fill(rows, w - far.shape[1], ROUTE1_BORDER, far.shape[1])
            far_img = Image.new("RGB", (w * 16, rows * 16))
            far_img.paste(strip(far, (p, s)), (0, 0))
            far_img.paste(strip(pad, (PRIMARY, SECONDARY)), (far.shape[1] * 16, 0))
        else:
            far_img = strip(far, (p, s))
        near_img = strip(near, (PRIMARY, SECONDARY))
        top, bottom = (far_img, near_img) if side == "N" else (near_img, far_img)
        img.paste(top, (4, 0))
        img.paste(bottom, (4, rows * 16))
        for x in (0, w * 16 + 4):                      # ticks mark the seam
            img.paste((255, 0, 255), (x, rows * 16 - 2, x + 4, rows * 16 + 2))
        out.append(img)
    # Kronion Hill beside Route 1's east edge, offset 2.
    kb = kh.blocks() & 0x3FF
    ys = range(0, 22)
    left = own[ys.start:ys.stop, -rows:]
    right = np.array([[kb[y - KRONION_OFFSET, x] if 0 <= y - KRONION_OFFSET < kh.h else ROUTE1_BORDER[0]
                       for x in range(rows)] for y in ys], np.uint16)
    img = Image.new("RGB", (rows * 2 * 16, len(ys) * 16 + 8), (24, 24, 32))
    img.paste(strip(left, (PRIMARY, SECONDARY)), (0, 4))
    img.paste(strip(right, (PRIMARY, SECONDARY)), (rows * 16, 4))
    for y in (0, len(ys) * 16 + 4):
        img.paste((255, 0, 255), (rows * 16 - 2, y, rows * 16 + 2, y + 4))
    out.append(img)
    W = sum(i.width for i in out) + 8 * (len(out) + 1)
    H = max(i.height for i in out) + 16
    sheet = Image.new("RGB", (W, H), (24, 24, 32))
    x = 8
    for i in out:
        sheet.paste(i, (x, 8))
        x += i.width + 8
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    path = RENDER / "kalliste_route1_seams.png"
    sheet.save(path)
    return path


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

    # Screens: the GBA shows 15x10 tiles, the player's tile at column 7 and
    # half a row down from row 4 (pixels 72-87), as in-game shots show.
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
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16 + 8
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


# ---------------------------------------------------------------------------
# Walkability: design/MAP_DESIGN.md's route rules, proved on the built maps
# from their metatile behaviors and collision, the way the game reads them.
# ---------------------------------------------------------------------------
STEPS = ((0, -1), (1, 0), (0, 1), (-1, 0))
FACING = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0),
          "MOVEMENT_TYPE_FACE_UP": (0, -1), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0),
          "MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_LEFT": (-1, 0)}


def behavior_ids():
    import re
    text = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    body = text[text.index("enum {") + len("enum {"):]
    return {n: i for i, n in enumerate(re.findall(r"^\s*(MB_\w+)", body, re.M))}


class Walk:
    """Each cell of a built map: 'solid', 'grass' (tall grass), 'ledge' (jump
    south) or 'open'."""

    def __init__(self, blocks, primary, secondary):
        sys.path.insert(0, str(ROOT / "tools/ichor"))
        import render_map as rm
        rm.read_fieldmap_constants()
        syms = rm.scan_tileset_symbols()
        attrs = [np.fromfile(Path(rm.resolve_tileset(n, syms)["metatiles"]).with_name("metatile_attributes.bin"), "<u2")
                 for n in (primary, secondary)]
        mb = behavior_ids()
        self.blocks, (self.h, self.w) = blocks, blocks.shape
        self.kind = {}
        for y in range(self.h):
            for x in range(self.w):
                v = int(blocks[y, x])
                mid = v & 0x3FF
                a = attrs[0][mid] if mid < 512 else attrs[1][mid - 512] if mid - 512 < len(attrs[1]) else 0
                beh = int(a) & 0xFF
                if beh == mb["MB_JUMP_SOUTH"]:
                    k = "ledge"
                elif v >> 10 & 3 or v >> 12 != 3:
                    k = "solid"
                elif beh == mb["MB_TALL_GRASS"]:
                    k = "grass"
                else:
                    k = "open"
                self.kind[(x, y)] = k

    def cost(self, starts, goals, avoid=frozenset(), weight=None):
        """0-1 BFS: the least total weight of the cells entered on a walk from a
        start to a goal (None if there is none). By default a tall-grass cell
        weighs 1, so this counts grass steps. Ledges only work going south: the
        player hops over the ledge cell and lands on the one past it."""
        from collections import deque
        weight = weight or (lambda c: 1 if self.kind[c] == "grass" else 0)
        ok = lambda c: c in self.kind and self.kind[c] in ("open", "grass") and c not in avoid
        dist, dq = {}, deque()
        for s in starts:
            if ok(s):
                dist[s] = weight(s)
                dq.append(s)
        dq = deque(sorted(dq, key=lambda c: dist[c]))
        while dq:
            c = dq.popleft()
            for dx, dy in STEPS:
                n = (c[0] + dx, c[1] + dy)
                if self.kind.get(n) == "ledge" and (dx, dy) == (0, 1):
                    n = (n[0], n[1] + 1)
                if not ok(n):
                    continue
                w = weight(n)
                if n not in dist or dist[c] + w < dist[n]:
                    dist[n] = dist[c] + w
                    (dq.appendleft if w == 0 else dq.append)(n)
        best = [dist[g] for g in goals if g in dist]
        self.dist = dist
        return min(best) if best else None

    def traps(self, starts, people=frozenset()):
        """Cells a walk from the starts reaches but can't come back from (a
        ledge dropped the player somewhere with no way back up). people are
        the cells of objects who never move, walls to the walk: a trainer
        stays on his cell after he is beaten."""
        ok = lambda c: self.kind.get(c) in ("open", "grass") and c not in people
        def moves(c):
            for dx, dy in STEPS:
                n = (c[0] + dx, c[1] + dy)
                if self.kind.get(n) == "ledge" and (dx, dy) == (0, 1):
                    n = (n[0], n[1] + 1)
                if ok(n):
                    yield n
        seen, todo = {s for s in starts if ok(s)}, [s for s in starts if ok(s)]
        back = {}
        while todo:
            c = todo.pop()
            for n in moves(c):
                back.setdefault(n, set()).add(c)
                if n not in seen:
                    seen.add(n)
                    todo.append(n)
        home, todo = {s for s in starts if ok(s)}, [s for s in starts if ok(s)]
        while todo:
            c = todo.pop()
            for p in back.get(c, ()):
                if p not in home:
                    home.add(p)
                    todo.append(p)
        return sorted(seen - home)

    def grass_parts(self):
        seen, parts = set(), []
        for c, k in self.kind.items():
            if k != "grass" or c in seen:
                continue
            part, todo = set(), [c]
            seen.add(c)
            while todo:
                x, y = todo.pop()
                part.add((x, y))
                for dx, dy in STEPS:
                    n = (x + dx, y + dy)
                    if self.kind.get(n) == "grass" and n not in seen:
                        seen.add(n)
                        todo.append(n)
            parts.append(part)
        return parts

    def forced_bands(self, starts, goals):
        """Grass patches every walk from the starts to the goals must cross, with
        the fewest of each band's cells such a walk can get away with (its depth)."""
        bands = []
        for part in self.grass_parts():
            if self.cost(starts, goals, avoid=part) is None:
                depth = self.cost(starts, goals, weight=lambda c, p=part: 1 if c in p else 0)
                bands.append((part, depth))
        return sorted(bands, key=lambda b: -max(y for _, y in b[0]))

    def sight(self, x, y, facing, reach):
        dx, dy = FACING[facing]
        cells = []
        for i in range(1, reach + 1):
            c = (x + dx * i, y + dy * i)
            if self.kind.get(c) not in ("open", "grass"):
                break
            cells.append(c)
        return cells


def standing(events):
    """The cells of objects who are always there and never step aside: no hide
    flag and no wander range (as mapdata.Map.people counts them)."""
    return frozenset((e["x"], e["y"]) for e in events["object_events"]
                     if e.get("flag") in (None, "0", 0, "")
                     and not int(e.get("movement_range_x") or 0) and not int(e.get("movement_range_y") or 0))


def trainers_of(events):
    out = {}
    for e in events["object_events"]:
        if e.get("trainer_type") == "TRAINER_TYPE_NORMAL":
            name = e["script"].split("_")[-1]
            out[name] = (e["x"], e["y"], e["movement_type"], int(e["trainer_sight_or_berry_tree_id"]))
    return out


R1_SOUTH = [(x, 63) for x in range(10, 14)]
R1_NORTH = [(x, 0) for x in range(10, 14)]
R1_SPUR = [(29, 18), (29, 19)]
KH_FOOT, KH_TOP = [(0, 16), (0, 17)], [(13, 10)]


def check_route(r1, kh):
    """MAP_DESIGN's route rules, proved: no grass-free walk from Elaia to Akti,
    at least three forced bands (the first exactly 2 deep), the mandatory
    trainers' lines cut every walk they guard, and Kronion Hill's climb crosses
    grass; on the hill, Menalkas and Lykidas hold what they guard, the climb to
    the summit crosses no trainer's line, and on both maps no ledge traps a
    player. Prints the proof; exits on a broken rule."""
    errs = []
    w = Walk(r1.blocks(), PRIMARY, SECONDARY)
    if w.cost(R1_SOUTH, R1_NORTH) is None:
        errs.append("Route 1: no walk at all from Elaia to Akti")
    bands = w.forced_bands(R1_SOUTH, R1_NORTH)
    for part, depth in bands:
        ys = sorted({y for _, y in part})
        print(f"  Route 1 forced band: rows {ys[0]}-{ys[-1]}, {len(part)} cells, crossed in no fewer than {depth} steps")
    if len(bands) < 3:
        errs.append(f"Route 1: {len(bands)} forced grass bands between Elaia and Akti, want 3")
    if any(d < 2 for _, d in bands):
        errs.append("Route 1: a forced band can be crossed in under 2 steps")
    if bands and bands[0][1] != 2:
        errs.append(f"Route 1: the first band out of Elaia is {bands[0][1]} deep, MAP_DESIGN says 2")
    trainers = {n: (x, y, f, s) for n, (x, y, f, s, _) in ROUTE1_MANDATORY.items()}
    built = trainers_of(ROUTE1_EVENTS)
    for name, (x, y, facing, reach, walk) in ROUTE1_MANDATORY.items():
        bx, by, bf, bs = built[name]
        if (bx, by, FACING[bf], bs) != (x, y, FACING[facing], reach):
            errs.append(f"Route 1: {name}'s event does not match ROUTE1_MANDATORY")
        line = w.sight(x, y, facing, reach)
        starts, goals = (R1_SOUTH, R1_NORTH) if walk == "north" else (R1_SOUTH + R1_NORTH, R1_SPUR)
        skirt = w.cost(starts, goals, avoid=set(line) | {(x, y)})
        print(f"  {name} at ({x},{y}) sees {line}: " + ("cannot be skirted" if skirt is None else "CAN be skirted"))
        if skirt is None and w.cost(starts, goals) is None:
            errs.append(f"Route 1: no walk at all past {name}")
        elif skirt is not None:
            errs.append(f"Route 1: {name}'s line can be skirted")
    for name in sorted(set(built) - set(trainers)):
        print(f"  {name} is optional")
    k = Walk(kh.blocks(), PRIMARY, SECONDARY)
    if k.cost(KH_FOOT, KH_TOP) is None:
        errs.append("Kronion Hill: no walk from the hill foot to the summit")
    kb = k.forced_bands(KH_FOOT, KH_TOP)
    for part, depth in kb:
        ys = sorted({y for _, y in part})
        print(f"  Kronion Hill forced band: rows {ys[0]}-{ys[-1]}, crossed in no fewer than {depth} steps")
    if not kb or any(d < 2 for _, d in kb):
        errs.append("Kronion Hill: the climb needs a band of grass at least 2 deep")
    kt = trainers_of(KRONION_EVENTS)
    for name, (x, y, facing, reach, goals) in KRONION_MANDATORY.items():
        bx, by, bf, bs = kt[name]
        if (bx, by, FACING[bf], bs) != (x, y, FACING[facing], reach):
            errs.append(f"Kronion Hill: {name}'s event does not match KRONION_MANDATORY")
        line = k.sight(x, y, facing, reach)
        if k.cost(KH_FOOT, goals) is None:
            errs.append(f"Kronion Hill: no walk at all from the hill foot to what {name} guards")
        skirt = k.cost(KH_FOOT, goals, avoid=set(line) | {(x, y)})
        print(f"  {name} at ({x},{y}) sees {line}: " + ("cannot be skirted" if skirt is None else "CAN be skirted"))
        if skirt is not None:
            errs.append(f"Kronion Hill: {name}'s line can be skirted")
    # The climb to the summit stays clear of every trainer on the hill: the
    # pastures are a branch, so nobody stops a player headed for the scene.
    seen = set()
    for name, (x, y, f, reach) in kt.items():
        seen |= set(k.sight(x, y, f, reach)) | {(x, y)}
    if k.cost(KH_FOOT, KH_TOP, avoid=seen) is None:
        errs.append("Kronion Hill: the climb to the summit crosses a trainer's line")
    for name in sorted(set(kt) - set(KRONION_MANDATORY)):
        print(f"  {name} is optional")
    # §1: never use a ledge to trap a player away from an exit, nor stand
    # anyone who never moves in a ledge pocket's only way out.
    for name, walk_, starts, events in (("Route 1", w, R1_SOUTH, ROUTE1_EVENTS),
                                        ("Kronion Hill", k, KH_FOOT, KRONION_EVENTS)):
        stuck = walk_.traps(starts, standing(events))
        if stuck:
            errs.append(f"{name}: {len(stuck)} cell(s) a player can reach but not leave, e.g. {stuck[:4]}")
    if errs:
        sys.exit("route rules broken:\n  " + "\n  ".join(errs))
    return w, k


def walk_render(name, blocks, primary, secondary, events, starts, goals, title):
    """The map with what the player can do on it: blocked cells hatched dark,
    open ground tinted by how many grass steps it takes at least to get there
    from the start (each forced band crossed shifts the color), tall grass
    green, forced bands outlined in yellow, ledges marked with a south arrow,
    trainers in magenta with their sight lines."""
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer(primary, secondary)
    base = rm.render_blocks(r, (blocks & 0x3FF).ravel(), blocks.shape[1])
    s = 2
    img = base.resize((base.width * s, base.height * s), Image.NEAREST).convert("RGBA")
    w = Walk(blocks, primary, secondary)
    w.cost(starts, goals)
    dist = dict(w.dist)
    bands = w.forced_bands(starts, goals)
    band_cells = set().union(*[p for p, _ in bands]) if bands else set()
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    cell = 16 * s
    zone = [(80, 160, 255), (255, 150, 60), (190, 90, 255), (60, 220, 220), (255, 90, 140), (160, 255, 90)]
    levels = sorted({v for c, v in dist.items() if w.kind[c] == "open"})
    for (x, y), k in w.kind.items():
        box = [x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1]
        if k == "solid":
            d.rectangle(box, fill=(20, 0, 0, 120))
        elif k == "ledge":
            d.rectangle(box, fill=(40, 90, 255, 110))
            d.polygon([(x * cell + 8, y * cell + 10), (x * cell + cell - 8, y * cell + 10),
                       (x * cell + cell // 2, y * cell + cell - 6)], fill=(255, 255, 255, 230))
        elif k == "grass":
            d.rectangle(box, fill=(0, 255, 0, 70))
        elif (x, y) in dist:
            band = levels.index(dist[(x, y)]) if dist[(x, y)] in levels else 0
            d.rectangle(box, fill=zone[band % len(zone)] + (70,))
        else:
            d.rectangle(box, fill=(0, 0, 0, 90))             # open, but out of reach
    for (x, y) in band_cells:
        d.rectangle([x * cell + 1, y * cell + 1, x * cell + cell - 2, y * cell + cell - 2], outline=(255, 235, 0, 255), width=3)
    for name_, (x, y, f, reach) in trainers_of(events).items():
        for (cx, cy) in w.sight(x, y, f, reach):
            d.rectangle([cx * cell + 6, cy * cell + 6, cx * cell + cell - 7, cy * cell + cell - 7], fill=(255, 0, 255, 150))
        d.rectangle([x * cell + 2, y * cell + 2, x * cell + cell - 3, y * cell + cell - 3], outline=(255, 0, 255, 255), width=4)
    for (x, y) in starts + goals:
        d.rectangle([x * cell + 10, y * cell + 10, x * cell + cell - 11, y * cell + cell - 11], fill=(255, 255, 255, 255))
    out = Image.alpha_composite(img, over)
    font = ImageFont.load_default(size=14)
    cap = Image.new("RGBA", (out.width, 64), (24, 24, 32, 255))
    cd = ImageDraw.Draw(cap)
    lines = [title, f"least grass steps start to goal: {w.cost(starts, goals)}; forced bands: "
             + (", ".join(f"rows {min(y for _, y in p)}-{max(y for _, y in p)} ({dp} deep)" for p, dp in bands) or "none")]
    for i, t in enumerate(lines):
        cd.text((8, 8 + i * 20), t, fill=(255, 255, 255, 255), font=font)
    sheet = Image.new("RGBA", (out.width, out.height + cap.height))
    sheet.paste(cap, (0, 0))
    sheet.paste(out, (0, cap.height))
    path = RENDER / f"{name}.png"
    sheet.convert("RGB").save(path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--shapes", action="store_true", help="update tools/ichor/art/agros_shapes.json and stop")
    ap.add_argument("--walk-of", nargs=4, metavar=("R1_BIN", "R1_JSON", "KH_BIN", "KH_JSON"),
                    help="render the walkability of another build of both maps (say, main's) as "
                         "kalliste_route1_walk_before.png and its Kronion Hill twin, then stop")
    ap.add_argument("--walk-tileset", default="gTileset_Kalliste", help="secondary tileset for --walk-of")
    args = ap.parse_args()
    if args.shapes:
        write_shapes()
        return
    if args.walk_of:
        rb, rj, kb, kj = args.walk_of
        r1b = np.fromfile(rb, "<u2").reshape(64, 30)
        khb = np.fromfile(kb, "<u2").reshape(-1, 24)
        print(walk_render("kalliste_route1_walk_before", r1b, PRIMARY, args.walk_tileset,
                          json.loads(Path(rj).read_text()), R1_SOUTH, R1_NORTH, "Route 1 before: Elaia (bottom) to Akti (top)"))
        print(walk_render("kalliste_route1_kronion_hill_walk_before", khb[:20], PRIMARY, args.walk_tileset,
                          json.loads(Path(kj).read_text()), [(0, 16), (0, 17)], [(5, 11)],
                          "Kronion Hill before: hill foot (left) to the summit"))
        return
    cat = load_catalog()
    r1 = build_route1(cat)
    kh = build_kronion(cat)
    check_seams(r1, kh)
    check_route(r1, kh)
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
        for p in render(kh, "kalliste_route1_kronion_hill", KRONION_EVENTS, KRONION_BORDER, KRONION_VIEWS,
                        rows=KRONION_SHOWN):
            print(p)
        print(render_seams(r1, kh))
        print(walk_render("kalliste_route1_walk", r1.blocks(), PRIMARY, SECONDARY, ROUTE1_EVENTS,
                          R1_SOUTH, R1_NORTH, "Route 1: Elaia (bottom) to Akti (top)"))
        print(walk_render("kalliste_route1_kronion_hill_walk", kh.blocks()[:KRONION_SHOWN], PRIMARY, SECONDARY, KRONION_EVENTS,
                          KH_FOOT, KH_TOP, "Kronion Hill: hill foot (left) to the summit"))


if __name__ == "__main__":
    main()
