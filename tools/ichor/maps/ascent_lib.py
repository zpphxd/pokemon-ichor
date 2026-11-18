#!/usr/bin/env python3
"""Shared pieces for the Ascent's snow floors on gTileset_Chion (design/LEAGUE.md).

A Snow map is a league_lib.Grid whose terrain comes from a character plan,
autotiled with cave_dark's kit in Chion's colors (tools/ichor/art/chion_props.py):

  #  ice wall (the cave style) or snow-topped ice (the glacier style)
  .  snow floor (MB_CAVE: wild Pokémon anywhere on it)
  ,  slick ice (MB_ICE: the player slides until something stops them)
  ~  glacial water (surf with Poseidon's Conch)

Props from Chion's catalog go on top by key. The Grid's events, save,
reachability and review renders all work as for the other League maps;
reachability here knows that ice slides.

Two small solvers keep the puzzles honest: slide_plan() finds the shortest
key sequence across an ice field (and the build fails when a field can strand
the player), and push_plan() solves a drum-and-plate seal (a tiny Sokoban),
so every seal is proven solvable and the headless test can replay the answer.
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import league_lib as L  # noqa: E402
from league_lib import ROOT, noise  # noqa: E402
import cave_dark_kit as kit  # noqa: E402

kit.FLUTE_SETS.setdefault("glacier", kit.FLUTE_SETS[None])

CHION = json.loads((ROOT / "data/tilesets/secondary/chion/catalog.json").read_text())
PIECES = {p["key"]: p for p in CHION["pieces"]}
DIRS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
WALKABLE = set(".T^v[]D")


def carve(rows, ch, x0, y0, x1, y1):
    for y in range(max(0, y0), min(len(rows), y1 + 1)):
        r = rows[y]
        for x in range(max(0, x0), min(len(r), x1 + 1)):
            r[x] = ch


def blob(rows, ch, cx, cy, rx, ry, salt=0, rough=0.18):
    """An organic chamber: an ellipse with a wobbly edge."""
    for y in range(cy - ry - 2, cy + ry + 3):
        for x in range(cx - rx - 2, cx + rx + 3):
            if not (0 <= y < len(rows) and 0 <= x < len(rows[0])):
                continue
            d = ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2
            if d <= 1.0 + rough * (noise(x, y, salt) / 50.0 - 1.0):
                rows[y][x] = ch


def plan(w, h, fill="#"):
    return [[fill] * w for _ in range(h)]


class Snow(L.Grid):
    """One snow map: a plan, autotiled; props by key; events as league_lib."""

    def __init__(self, name, rows, style=None):
        rows = ["".join(r) for r in rows]
        H, W = len(rows), len(rows[0])
        assert all(len(r) == W for r in rows), name
        super().__init__(name, W, H, secondary="gTileset_Chion", cat=None, base=0x200, base_kind="floor")
        self.rows, self.style = rows, style
        ids = kit.autotile(rows, CHION, style)
        self.kinds = kit.classify(rows)
        for y in range(H):
            for x in range(W):
                self.mt[y, x] = ids[y][x]
                k = self.kinds[y][x]
                self.solid[y, x] = k in ("T", "ft", "fb")
                self.water[y, x] = k == "water"
                self.g[y][x] = {"T": "rock", "ft": "rock", "fb": "rock"}.get(k, k)

    def put(self, key, x, y, cells=None):
        p = PIECES[key]
        for j in range(p["h"]):
            for i in range(p["w"]):
                if cells is not None and (i, j) not in cells:
                    continue
                X, Y = x + i, y + j
                if not self.inside(X, Y):
                    continue
                code = p["walk"][j][i]
                self.set(X, Y, p["ids"][j][i], code not in WALKABLE, key)
        return p

    def pid(self, key, i=0, j=0):
        return PIECES[key]["ids"][j][i]

    def scatter(self, keys, cells, salt, rate):
        """Floor accents on open snow (not ice, not under anything placed)."""
        for (x, y) in cells:
            if self.rows[y][x] == "." and not self.fixed[y, x] and noise(x, y, salt) < rate:
                self.set(x, y, self.pid(keys[noise(x, y, salt + 1) % len(keys)]), False, "accent")

    def accents(self, salt=7, rate=6):
        cells = [(x, y) for y in range(self.H) for x in range(self.W)
                 if self.kinds[y][x] == "floor" and self.kit_plain(x, y)]
        self.scatter(["snow_tracks", "snow_ripples", "snow_stone", "snow_glitter", "snow_ripples"], cells, salt, rate)

    def kit_plain(self, x, y):
        """A floor cell with no wall shadow (only those take accents)."""
        return all(self.kinds[y + dy][x + dx] == "floor" for dx, dy in ((0, -1), (-1, 0), (-1, -1))
                   if 0 <= y + dy < self.H and 0 <= x + dx < self.W)

    def walkable(self, blocked=()):
        """Open cells; every object blocks (item balls too: on ice they stop a slide)."""
        ok = ~self.solid & ~self.water
        for o in self.events["object_events"]:
            if self.inside(o["x"], o["y"]):
                ok[o["y"], o["x"]] = False
        for x, y in blocked:
            if self.inside(x, y):
                ok[y, x] = False
        return ok

    # --- ice ----------------------------------------------------------------------
    def ice(self):
        return np.array([[L.BEH(self, x, y) == "MB_ICE" for x in range(self.W)] for y in range(self.H)])

    def slide(self, ok, ice, x, y, d):
        dx, dy = DIRS[d]
        X, Y = x + dx, y + dy
        if not self.inside(X, Y) or not ok[Y, X]:
            return None
        while ice[Y, X]:
            nx, ny = X + dx, Y + dy
            if not self.inside(nx, ny) or not ok[ny, nx]:
                break
            X, Y = nx, ny
        return X, Y

    def reach(self, start, blocked=()):
        ok = self.walkable(blocked)
        ice = self.ice()
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            for d in DIRS:
                p = self.slide(ok, ice, x, y, d)
                if p and p not in seen:
                    seen.add(p)
                    q.append(p)
        return seen

    def slide_plan(self, start, goal, blocked=()):
        """The shortest key string from start to goal, sliding on ice."""
        ok = self.walkable(blocked)
        ice = self.ice()
        prev, q = {start: None}, deque([start])
        while q:
            p = q.popleft()
            if p == goal:
                break
            for d in DIRS:
                n = self.slide(ok, ice, p[0], p[1], d)
                if n and n not in prev:
                    prev[n] = (p, d)
                    q.append(n)
        if goal not in prev:
            raise SystemExit(f"{self.name}: no way across the ice from {start} to {goal}")
        keys, p = [], goal
        while prev[p]:
            p, d = prev[p]
            keys.append(d)
        return "".join(reversed(keys))

    def check_no_strand(self, start, blocked=()):
        """Every place the ice can leave you must lead back to start."""
        seen = self.reach(start, blocked)
        ok = self.walkable(blocked)
        ice = self.ice()
        bad = []
        for p in seen:
            back, q = {p}, deque([p])
            while q:
                c = q.popleft()
                for d in DIRS:
                    n = self.slide(ok, ice, c[0], c[1], d)
                    if n and n not in back:
                        back.add(n)
                        q.append(n)
            if start not in back:
                bad.append(p)
        if bad:
            raise SystemExit(f"{self.name}: the ice can strand the player at {sorted(bad)[:8]}")


def push_plan(open_cells, drums, plates, start, max_states=400000):
    """Solve a drum seal (Sokoban): open_cells is a set of walkable (x, y);
    drums and plates are lists of (x, y); start is the player. Returns a list
    of (stand_x, stand_y, key): walk to stand, press key to push. None if none."""
    plates = frozenset(plates)

    def walk_region(p, ds):
        seen, q = {p}, deque([p])
        while q:
            x, y = q.popleft()
            for dx, dy in DIRS.values():
                n = (x + dx, y + dy)
                if n in open_cells and n not in ds and n not in seen:
                    seen.add(n)
                    q.append(n)
        return seen

    def canon(p, ds):
        return min(walk_region(p, ds)), ds

    # live cells: where a drum can stand and still reach some plate (reverse pulls)
    live, q = set(plates), deque(plates)
    while q:
        x, y = q.popleft()
        for dx, dy in DIRS.values():
            c, p2 = (x - dx, y - dy), (x - 2 * dx, y - 2 * dy)
            if c in open_cells and p2 in open_cells and c not in live:
                live.add(c)
                q.append(c)

    def hcost(ds):
        return sum(min(abs(x - a) + abs(y - b) for a, b in plates) for x, y in ds)

    import heapq
    s0 = frozenset(drums)
    key0 = canon(start, s0)
    prev = {key0: None}
    heap = [(hcost(s0), 0, 0, start, s0)]
    tick = 0
    while heap and len(prev) < max_states:
        _, g, _, p, ds = heapq.heappop(heap)
        if ds <= plates:
            out = []
            k = canon(p, ds)
            while prev[k]:
                k, move = prev[k]
                out.append(move)
            return list(reversed(out))
        region = walk_region(p, ds)
        here = canon(p, ds)
        for (bx, by) in ds:
            for key, (dx, dy) in DIRS.items():
                stand = (bx - dx, by - dy)
                dest = (bx + dx, by + dy)
                if stand in region and dest in live and dest not in ds:
                    nds = (ds - {(bx, by)}) | {dest}
                    k = canon((bx, by), nds)
                    if k not in prev:
                        prev[k] = (here, (stand[0], stand[1], key))
                        tick += 1
                        heapq.heappush(heap, (g + 1 + 2 * hcost(nds), g + 1, tick, (bx, by), nds))
    return None


def views_of(g, pts):
    return [(f"{i + 1:02d}_{label}", x, y) for i, (label, x, y) in enumerate(pts)]


def render(g, out, views, tag=""):
    return L.render(g, out, views, tag)
