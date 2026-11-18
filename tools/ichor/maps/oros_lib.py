#!/usr/bin/env python3
"""Outdoor snow maps on gTileset_Oros / gTileset_Propylon (tools/ichor/art/oros_art.py).

A map is a plan of levels, one character a cell:

  0-9  snow ground at that height       ~  the sea of cloud (solid)

The autotile works the rest out. Where ground is higher than the cell to its
south, a cliff face hangs below it: two rows for each level of drop (a top row
with the snow cornice, a bottom row with the snow piled at its foot), drawn on
the lower cells, which become solid. A plateau's west, east and north edges are
rims (solid); a face's ends are open or tucked against higher ground; a face
over the cloud sea drops into it. Overlays are marked before paint():

  deep(cells)   deep snow (MB_DEEP_SAND: wild Pokémon; you wade in it)
  tarn(cells)   a frozen tarn (MB_ICE: you slide), its shore drawn by shape
  stairs(cells) steps cut into a face (walkable)
  ledge(cells)  a snow cornice you jump down (MB_JUMP_SOUTH)
  scour(cells)  wind-scoured snow
  path(cells)   a path of packed snow

Props go on top by catalog key after paint(). Events, saving, reachability
(ice slides included, from ascent_lib.Snow) and renders work as league_lib's.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascent_lib as A  # noqa: E402
import league_lib as L  # noqa: E402
from league_lib import ROOT, noise  # noqa: E402

FOLDERS = {"gTileset_Oros": "oros", "gTileset_Propylon": "propylon"}
_CAT = {}


def catalog(tileset):
    if tileset not in _CAT:
        d = json.loads((ROOT / f"data/tilesets/secondary/{FOLDERS[tileset]}/catalog.json").read_text())
        _CAT[tileset] = {p["key"]: p for p in d["pieces"]}
    return _CAT[tileset]


class Oros(A.Snow):
    def __init__(self, name, rows, tileset="gTileset_Oros"):
        rows = ["".join(r) for r in rows]
        H, W = len(rows), len(rows[0])
        assert all(len(r) == W for r in rows), name
        L.Grid.__init__(self, name, W, H, secondary=tileset, cat=None, base=0x200, base_kind="floor")
        self.rows, self.style = rows, None
        self.P = catalog(tileset)
        self.lv = np.array([[-1 if c == "~" else int(c) for c in r] for r in rows])
        self.deep_c, self.ice_c, self.stair_c, self.ledge_c, self.scour_c = set(), set(), set(), set(), set()
        self.path_c = set()
        self.marble_c = set()
        self.alpine_c = set()
        self.face = {}
        self.painted = False

    # --- overlays ---------------------------------------------------------------
    def _cells(self, cells):
        return {(x, y) for (x, y) in cells if self.inside(x, y)}

    def deep(self, cells):
        self.deep_c |= self._cells(cells)

    def tarn(self, cells):
        self.ice_c |= self._cells(cells)

    def stairs(self, cells, marble=False):
        self.stair_c |= self._cells(cells)
        if marble:
            self.marble_c |= self._cells(cells)

    def ledge(self, cells):
        self.ledge_c |= self._cells(cells)

    def path(self, cells):
        """A path of packed snow (its fringe follows its shape)."""
        self.path_c |= self._cells(cells)

    def alpine(self, cells):
        """Alpine grass through patchy snow (low on the climb)."""
        self.alpine_c |= self._cells(cells)

    def scour(self, cells):
        self.scour_c |= self._cells(cells)

    # --- the autotile -------------------------------------------------------------
    def L_(self, x, y):
        if not self.inside(x, y):
            return None
        return int(self.lv[y, x])

    def faces(self):
        """{(x, y): (k, n, cloud)}: face cell k of n rows below an edge."""
        out = {}
        for x in range(self.W):
            top = None
            y = 0
            while y < self.H:
                lv = self.lv[y, x]
                if top is not None and lv < top and (x, y - 1) not in self.ledge_c:
                    n = 2 * (top - lv) if lv >= 0 else 2
                    cloud = lv < 0
                    k = 0
                    while k < n and y + k < self.H and self.lv[y + k, x] <= lv:
                        out[(x, y + k)] = (k + 1, n, cloud)
                        k += 1
                    if k:
                        last = out[(x, y + k - 1)]
                        out[(x, y + k - 1)] = (last[1], last[1], cloud) if k < n else last
                    y += max(k, 1)
                    top = lv
                    continue
                top = lv
                y += 1
        return out

    def ground_kind(self, x, y):
        """A walkable cell's metatile key (never a face)."""
        if (x, y) in self.ice_c:
            return self.ice_key(x, y)
        if (x, y) in self.ledge_c:
            left = (x - 1, y) in self.ledge_c
            right = (x + 1, y) in self.ledge_c
            return "ledge_m" if left and right else "ledge_r" if left else "ledge_l" if right else "ledge_m"
        if (x, y) in self.deep_c:
            return "deep%d" % (noise(x, y, 31) % 3)
        if (x, y) in self.path_c:
            Pc = self.path_c
            bits = ((x, y - 1) not in Pc) << 3 | ((x, y + 1) not in Pc) << 2 | ((x + 1, y) not in Pc) << 1 | \
                ((x - 1, y) not in Pc)
            return f"path_{bits}"
        if self.face.get((x, y - 1)):
            return "gs"
        if (x, y) in self.alpine_c:
            return "ag%d" % (noise(x, y, 41) % 3)
        if (x, y) in self.scour_c:
            return "gw%d" % (noise(x, y, 33) % 2)
        r = noise(x, y, 35)
        return "g0" if r < 34 else "g1" if r < 56 else "g2" if r < 62 else "g3" if r < 64 else "g0"

    def ice_key(self, x, y):
        I = lambda X, Y: (X, Y) in self.ice_c
        n, s, w, e = not I(x, y - 1), not I(x, y + 1), not I(x - 1, y), not I(x + 1, y)
        if n and w:
            return "ice_nw"
        if n and e:
            return "ice_ne"
        if s and w:
            return "ice_sw"
        if s and e:
            return "ice_se"
        if n:
            return "ice_n"
        if s:
            return "ice_s"
        if w:
            return "ice_w"
        if e:
            return "ice_e"
        for k, (dx, dy) in (("inw", (-1, -1)), ("ine", (1, -1)), ("isw", (-1, 1)), ("ise", (1, 1))):
            if not I(x + dx, y + dy):
                return "ice_" + k
        return "ice_c" if noise(x, y, 37) % 3 else "ice_c2"

    def lower(self, x, y, me):
        """Is the cell at (x, y) lower ground than level `me`, seen from beside it?"""
        if not self.inside(x, y):
            return False
        return self.lv[y, x] < me

    def paint(self):
        self.face = self.faces()
        for y in range(self.H):
            for x in range(self.W):
                if self.fixed[y, x]:
                    continue
                f = self.face.get((x, y))
                if f and (x, y) not in self.stair_c:
                    k, n, cloud = f
                    row = "t" if k == 1 else "b" if k == n else "m"
                    upper = self.lv[y - k, x] if y - k >= 0 else self.lv[y, x]

                    def end(dx):
                        X = x + dx
                        if not self.inside(X, y):
                            return "n"
                        if (X, y) in self.face:
                            return "n"
                        if self.lv[y, X] > self.lv[y, x]:
                            return "i"
                        return "o"
                    l, r = end(-1), end(1)
                    if cloud:
                        l, r = ("n" if l == "i" else l), ("n" if r == "i" else r)
                        key = f"face_{row}_{l}_{r}_c"
                    elif l == "n" and r == "n" and noise(x, y, 39) < 20:
                        key = f"face_{row}_n_n_v"
                    else:
                        key = f"face_{row}_{l}_{r}"
                    self._set(x, y, key)
                    continue
                if f:
                    k, n, _ = f
                    st = "mstair" if (x, y) in self.marble_c else "stair"
                    self._set(x, y, f"{st}_t" if k == 1 else f"{st}_b" if k == n else f"{st}_m")
                    continue
                me = self.lv[y, x]
                if me < 0:
                    self._set(x, y, f"cloud_{(x % 2) + 2 * (y % 2)}")
                    continue
                N = self.lower(x, y - 1, me)
                W = self.lower(x - 1, y, me)
                E = self.lower(x + 1, y, me)
                a = not (N or W) and self.lower(x - 1, y - 1, me)
                b = not (N or E) and self.lower(x + 1, y - 1, me)
                if N or W or E or a or b:
                    self._set(x, y, "rim_" + "".join(k for k, v in (("N", N), ("W", W), ("E", E), ("a", a), ("b", b))
                                                       if v))
                    continue
                self._set(x, y, self.ground_kind(x, y))
        self.painted = True

    def _set(self, x, y, key):
        p = self.P[key]
        code = p["walk"][0][0]
        self.mt[y, x] = p["ids"][0][0]
        self.solid[y, x] = code not in ".TJ"
        if code == "J":
            self.solid[y, x] = True
        self.water[y, x] = False
        self.g[y][x] = key

    # --- props ---------------------------------------------------------------------
    def put(self, key, x, y, cells=None, solid=None):
        p = self.P[key]
        for j in range(p["h"]):
            for i in range(p["w"]):
                if cells is not None and (i, j) not in cells:
                    continue
                X, Y = x + i, y + j
                if not self.inside(X, Y):
                    continue
                code = p["walk"][j][i]
                blocked = code not in ".TDv^[]" if solid is None else solid
                self.set(X, Y, p["ids"][j][i], blocked, key)
        return p

    def pid(self, key, i=0, j=0):
        return self.P[key]["ids"][j][i]

    def accents(self, *a, **k):
        pass

    def save(self, *a, **k):
        super().save(*a, **k)
        import os
        if os.environ.get("OROS_DEBUG"):
            L.render(self, os.environ["OROS_DEBUG"], (), "_debug")
            st = tuple(int(v) for v in os.environ.get("OROS_START", "0,0").split(","))
            print(self.walk_text(self.reach(st)))

    def border(self):
        c = [self.pid(f"cloud_{i}") | (1 << 10) for i in range(4)]
        return c


def common_keys():
    """Terrain keys with the same metatile in Oros and Propylon (tools/ichor/art/oros_art.py:
    the common terrain comes first in both): a connection between an Oros map and a
    Propylon map draws each one's edge with the other's tileset, so seams use only these."""
    a, b = catalog("gTileset_Oros"), catalog("gTileset_Propylon")
    return {k for k in a if k in b and a[k]["ids"] == b[k]["ids"] and a[k]["section"] == "terrain"}


def seam_check(g, rows):
    """Fail if a seam row holds anything but common terrain."""
    ok = common_keys()
    for y in rows:
        for x in range(g.W):
            if g.kind[y, x] or g.g[y][x] not in ok:
                raise SystemExit(f"{g.name}: {g.kind[y, x] or g.g[y][x]} at {x},{y} is in a seam with the other tileset")


def roughen(a, edge_to, salt, rate=30, keep=(), levels=None):
    """Break straight edges: each cell of a region that borders `edge_to` (a level,
    -1 for the cloud) joins it with chance rate/100, unless it is in `keep`.
    Returns the array changed in place."""
    H, W = a.shape
    keep = set(keep)
    flip = []
    for y in range(H):
        for x in range(W):
            v = a[y, x]
            if v == edge_to or (levels is not None and v not in levels) or (x, y) in keep:
                continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and a[y + dy, x + dx] == edge_to
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                if noise(x, y, salt) % 100 < rate:
                    flip.append((x, y))
    for x, y in flip:
        a[y, x] = edge_to
    return a
