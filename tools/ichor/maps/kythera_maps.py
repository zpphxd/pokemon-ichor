"""Shared builder for Act III's Kythera maps (design/phase4/SCRIPT.md Part 2).

Each map's own script (kythera_foam_road.py, kythera_paphia.py and the rest)
composes its layout on a Map grid with pieces placed by key and name from the
Kythera-family catalogs (kythera_tiles.py, design/phase4/TILES_*.md) and the
aethos primary (design/phase1/TILES_aethos.md), declares its events, and calls
build(): that writes the layout, the border, map.json's events and
connections, checks the map (MAP_DESIGN.md §5's seam strips, warps on doors,
people on walkable ground, readable signs, everything the player must reach
reachable) and renders it into design/phase4/img/maps/ at 1x and 3x, with an
events plan and GBA-screen views along the route for the critique passes.

    from kythera_maps import Map, A
    m = Map("KytheraFoamRoad", "kythera", 64, 24)
    m.piece("myrtle", "L", 0, 0)            # a kythera piece; collision from its walk code
    m.olive(4, 3)                           # aethos pieces
    m.obj("ICHOR_FISHER", 10, 8, "KytheraFoamRoad_EventScript_Amphitos", trainer=True, sight=3)
    m.build(starts=[(63, 11)], must_reach=[...])
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_tiles as KT  # noqa: E402

IMG = ROOT / "design/phase4/img/maps"
SOLID, WATER_ELEV, LAND_ELEV = 1 << 10, 1, 3


class A:
    """aethos metatile ids (design/phase1/TILES_aethos.md)."""
    GRASS, GRASS_LEDGE, SHADE, TALL, ANEMONE, REEDS = 0x001, 0x002, 0x01C, 0x00D, 0x004, 0x015
    PATH, SAND, SEA, SHALLOW, FALL, VOID = 0x1D9, 0x124, 0x170, 0x0D1, 0x0B3, 0x000
    PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
             "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
    SAND_GRASS = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122,
                  "BL": 0x128, "B": 0x129, "BR": 0x12A}
    OLIVE_TOP, OLIVE_BOT, OLIVE_BOT_TIP, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1DC, 0x1DD), (0x1CE, 0x1CF)
    OLIVE_TIP_TALL, OLIVE_TIP_SEA = (0x1C6, 0x1C7), (0x1F6, 0x1F7)
    CYP_TOP, CYP_BOT, CYP_TOP_TALL, CYP_TOP_SEA = 0x00E, 0x016, 0x025, 0x035
    PINE_TOP, PINE_BOT = (0x01E, 0x01F), (0x026, 0x027)
    STELE, HERM, TRIPOD_TOP, TRIPOD = 0x003, 0x01B, 0x130, 0x131
    BOULDER_GRASS, BOULDER_SAND, SEA_BOULDER, SEA_ROCK_DEEP = 0x0E0, 0x0E2, 0x0C5, 0x18C
    STEPS, STEPS_B = 0x0AF, 0x0CF
    LEDGE = {"S": 0x087, "W": 0x085, "E": 0x086, "SW": 0x08D, "SE": 0x08E, "SL": 0x0D5, "SR": 0x0D6,
             "in": 0x06E}
    LEDGE_SAND = {"S": 0x097, "W": 0x0A5, "E": 0x0A6, "SW": 0x0AD, "SE": 0x0AE, "SL": 0x0E5, "SR": 0x0E6}
    WALL = {"L": 0x148, "M": 0x149, "R": 0x14A}
    ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
                  [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
    AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
             [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]
    FARMHOUSE = [[0x008, 0x009, 0x00A], [0x010, 0x011, 0x012], [0x018, 0x019, 0x01A], [0x020, 0x021, 0x022]]


# Every aethos metatile a builder may place that blocks the player.
AETHOS_SOLID = {A.STELE, A.HERM, A.TRIPOD, A.BOULDER_GRASS, A.BOULDER_SAND, A.SEA_BOULDER, A.SEA_ROCK_DEEP,
                *A.OLIVE_TOP, *A.OLIVE_BOT, *A.OLIVE_BOT_TIP, A.CYP_BOT, *A.PINE_TOP, *A.PINE_BOT,
                *A.WALL.values(), *[m for r in A.ASCLEPEION + A.AGORA + A.FARMHOUSE for m in r]}
AETHOS_SOLID -= {0x061, 0x041, 0x021}           # the doors


def _behaviors():
    txt = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    out, v = {}, 0
    for name, val in re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", txt, re.M):
        if val:
            v = int(val, 0)
        out[v] = name
        v += 1
    return out


MB = _behaviors()
SURF = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
        "MB_SOOTOPOLIS_DEEP_WATER", "MB_WATERFALL"}
DOORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_SOUTH_ARROW_WARP", "MB_NORTH_ARROW_WARP",
         "MB_EAST_ARROW_WARP", "MB_WEST_ARROW_WARP"}
LEDGES = {"MB_JUMP_SOUTH": (0, 1), "MB_JUMP_NORTH": (0, -1), "MB_JUMP_EAST": (1, 0), "MB_JUMP_WEST": (-1, 0),
          "MB_JUMP_SOUTHEAST": (1, 1), "MB_JUMP_SOUTHWEST": (-1, 1)}
DIRS4 = ((0, -1), (1, 0), (0, 1), (-1, 0))


def _hash(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000


def _attrs(path):
    return np.fromfile(ROOT / path, "<u2")


PRIMARY_DIR = {"aethos": "gTileset_Aethos", "oikos": "gTileset_Oikos"}


class Map:
    def __init__(self, name, tileset, w, h, fill=A.GRASS, primary="aethos"):
        self.name, self.ts, self.w, self.h, self.primary = name, tileset, w, h, primary
        self.cat = KT.TILESETS[tileset]
        self.mid = np.full((h, w), fill, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.pattr = _attrs(f"data/tilesets/primary/{primary}/porytiles_bin/metatile_attributes.bin")
        self.sattr = _attrs(f"data/tilesets/secondary/{tileset}/porytiles_bin/metatile_attributes.bin")
        self.objects, self.warps, self.coords, self.bgs, self.connections = [], [], [], [], []
        self.seams = []            # (side, depth): strips that may hold only primary metatiles
        self.border = [A.SEA] * 4
        self.header = {}
        self.forced_open = set()   # tiles a script opens (a moved gate): count as open for reach checks

    # --- cells ----------------------------------------------------------------------------
    def ok(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def set(self, x, y, mid, solid=None):
        if not self.ok(x, y):
            return
        self.mid[y, x] = mid
        if solid is None:
            solid = mid < 0x200 and mid in AETHOS_SOLID
        self.solid[y, x] = solid

    def rect(self, x0, y0, x1, y1, mid, solid=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, mid, solid)

    def behavior(self, mid):
        a = self.pattr[mid] if mid < 0x200 else self.sattr[mid - 0x200]
        return MB.get(int(a) & 0xFF, "?")

    def s(self, key):
        return self.cat["structures"][key]

    def piece(self, key, name, x, y, solid=None):
        s = self.s(key)
        cx, cy = s["names"][name]
        self.set(x, y, s["ids"][cy][cx], s["walk"][cy][cx] == "X" if solid is None else solid)

    def part(self, key, name, x, y, w, h):
        s = self.s(key)
        cx, cy = s["names"][name]
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], s["walk"][cy + j][cx + i] == "X")

    def put(self, key, x, y, cells=None):
        s = self.s(key)
        for j in range(s["h"]):
            for i in range(s["w"]):
                if cells is None or (i, j) in cells:
                    self.set(x + i, y + j, s["ids"][j][i], s["walk"][j][i] == "X")

    def front(self, key, x, y):
        f = self.cat["fronts"][key]
        house = self.s("house")
        for j, row in enumerate(f["rows"]):
            for i, n in enumerate(row):
                cx, cy = house["names"][n]
                self.set(x + i, y + j, house["ids"][cy][cx], house["walk"][cy][cx] == "X")

    def blob(self, key, rows, ox, oy, ch="#", edge_in=True):
        """Soft-edged ground (seagrass, shingle) from a mask; cells off the mask's
        grid count as in the region only if edge_in."""
        sys.path.insert(0, str(ROOT / "tools/ichor/art"))
        import kythera_lib as KL
        region = [[c == ch for c in r] for r in rows]
        s = self.s(key)
        walk = s["walk"][0][0]
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != ch:
                    continue
                if edge_in:
                    k = KL.blob_key(region, i, j)
                else:
                    pad = [[False] * (len(r) + 2)] + [[False] + rr + [False] for rr in region] + [[False] * (len(r) + 2)]
                    k = KL.blob_key(pad, i + 1, j + 1)
                cx, cy = s["names"][k]
                self.set(ox + i, oy + j, s["ids"][cy][cx], walk == "X")

    def shore(self, rows, ox, oy, key="surf"):
        """A coastline from a mask: '#' sand, '~' sea; the waterline cells between
        are chosen from the surf kit by the sand around each sea cell."""
        H, W = len(rows), len(rows[0])

        def sand(i, j):
            if not (0 <= i < W and 0 <= j < H):
                return None
            return rows[j][i] == "#"
        for j in range(H):
            for i in range(W):
                c, X, Y = rows[j][i], ox + i, oy + j
                if c not in "#~":
                    continue
                if c == "#":
                    self.set(X, Y, A.SAND, False)
                    continue
                n, s_, e, w = sand(i, j - 1), sand(i, j + 1), sand(i + 1, j), sand(i - 1, j)
                ne, nw, se, sw = sand(i + 1, j - 1), sand(i - 1, j - 1), sand(i + 1, j + 1), sand(i - 1, j + 1)
                name = ("in_SE" if n and w else "in_SW" if n and e else "in_NE" if s_ and w else
                        "in_NW" if s_ and e else "S" if n else "N" if s_ else "E" if w else "W" if e else
                        "out_NW" if nw else "out_NE" if ne else "out_SW" if sw else "out_SE" if se else None)
                if name == "S" and (X * 7 + Y * 3) % 5 == 0 and "S2" in self.s(key)["names"]:
                    name = "S2"
                if name:
                    self.piece(key, name, X, Y)
                else:
                    self.set(X, Y, A.SEA, False)

    def path_patch(self, x0, y0, x1, y1, kit=A.PATCH):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                v = "T" if y == y0 else ("B" if y == y1 else "")
                h = "L" if x == x0 else ("R" if x == x1 else "")
                self.set(x, y, kit[(v + h) or "C"], False)

    def path(self, cells, kit=A.PATCH, context=()):
        """A worn path over any set of cells: each takes the patch kit's edge or
        corner by which of its four neighbours are path too, so a path can bend,
        narrow and widen instead of being a rectangle. Cells in `context` (paving,
        a stall standing in a square) count as path for the edges but aren't drawn."""
        cells = set(cells)
        near = cells | set(context)
        for (x, y) in cells:
            n, s_ = (x, y - 1) in near, (x, y + 1) in near
            w, e = (x - 1, y) in near, (x + 1, y) in near
            v = "" if (n and s_) or (not n and not s_) else ("T" if not n else "B")
            h = "" if (w and e) or (not w and not e) else ("L" if not w else "R")
            self.set(x, y, kit[(v + h) or "C"], False)

    def olive(self, x, y):
        """A 2x2 olive at (x, y); its crown tip pokes into the row above."""
        below = self.ok(x, y + 2) and int(self.mid[y + 2, x]) == A.OLIVE_TOP[0]
        bot = A.OLIVE_BOT_TIP if below else A.OLIVE_BOT
        for i in range(2):
            self.set(x + i, y, A.OLIVE_TOP[i], True)
            self.set(x + i, y + 1, bot[i], True)
        if self.ok(x, y - 1):
            above = (int(self.mid[y - 1, x]), int(self.mid[y - 1, x + 1]) if self.ok(x + 1, y - 1) else 0)
            if above == A.OLIVE_BOT:
                for i in range(2):
                    self.set(x + i, y - 1, A.OLIVE_BOT_TIP[i], True)
            elif all(a in (A.GRASS, A.SHADE) for a in above):
                for i in range(2):
                    self.set(x + i, y - 1, A.OLIVE_TIP[i], bool(self.solid[y - 1, x + i]))
            elif all(a == A.TALL for a in above):
                for i in range(2):
                    self.set(x + i, y - 1, A.OLIVE_TIP_TALL[i], bool(self.solid[y - 1, x + i]))

    def cypress(self, x, y):
        top = A.CYP_TOP_TALL if self.ok(x, y) and int(self.mid[y, x]) == A.TALL else A.CYP_TOP
        self.set(x, y, top, False)
        self.set(x, y + 1, A.CYP_BOT, True)

    def pine(self, x, y):
        for i in range(2):
            self.set(x + i, y, A.PINE_TOP[i], True)
            self.set(x + i, y + 1, A.PINE_BOT[i], True)

    def block(self, rows, x, y, solid=True):
        for j, r in enumerate(rows):
            for i, m in enumerate(r):
                if m is not None:
                    self.set(x + i, y + j, m, solid)

    # --- shaped ground (the critique passes' tools) ---------------------------------------
    @staticmethod
    def shape_key(inside, x, y):
        """The soft-edge kit's key for (x, y): '1|' then N NE E SE S SW W NW, a
        diagonal counting only when both of its sides are in (kythera_lib.blob_key)."""
        b = [int(bool(inside(x + dx, y + dy))) for dx, dy in
             ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))]
        for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
            if not (b[a] and b[c]):
                b[d] = 0
        return "1|" + "".join(str(v) for v in b)

    def tallgrass(self, cells, key="seagrass", walls_in=True):
        """Tall grass over a set of cells with a soft outline. Where the patch
        meets a wall (anything already solid, or the map's edge) it runs full to
        it, the way grass grows into a hedge's foot; on open ground it rounds off."""
        cells = set(cells)
        solid_before = self.solid.copy()

        def inside(x, y):
            if (x, y) in cells:
                return True
            if not self.ok(x, y):
                return walls_in
            return walls_in and bool(solid_before[y, x])
        s = self.s(key)
        for (x, y) in cells:
            cx, cy = s["names"][self.shape_key(inside, x, y)]
            self.set(x, y, s["ids"][cy][cx], False)

    def coast(self, sea, key="surf", edge_sea=True, draw=None):
        """The waterline round a set of sea cells: every sea cell beside land (any
        cell not in `sea`) takes the surf kit's piece for where the land is, so
        grass, path or sand all meet the foam. Off-map counts as sea if edge_sea.
        Only the cells in `draw` (default: all of `sea`) are drawn."""
        sea = set(sea)
        draw = sea if draw is None else set(draw) & sea

        def land(x, y):
            if not self.ok(x, y):
                return not edge_sea
            return (x, y) not in sea
        names = self.s(key)["names"]
        for (x, y) in draw:
            n, s_, e, w = land(x, y - 1), land(x, y + 1), land(x + 1, y), land(x - 1, y)
            ne, nw, se, sw = land(x + 1, y - 1), land(x - 1, y - 1), land(x + 1, y + 1), land(x - 1, y + 1)
            name = ("in_SE" if n and w else "in_SW" if n and e else "in_NE" if s_ and w else
                    "in_NW" if s_ and e else "S" if n else "N" if s_ else "E" if w else "W" if e else
                    "out_NW" if nw else "out_NE" if ne else "out_SW" if sw else "out_SE" if se else None)
            if name == "S" and (x * 7 + y * 3) % 5 == 0 and "S2" in names:
                name = "S2"
            if name:
                self.piece(key, name, x, y)
            else:
                self.set(x, y, A.SEA, False)

    def hedge(self, cells, key="myrtle"):
        """A myrtle hedge over any set of cells, each piece chosen by which of its
        four neighbours are hedge too (runs, turns, ends, lone clumps)."""
        cells = set(cells)
        names = self.s(key)["names"]
        piece = {(0, 1, 0, 1): "M", (1, 0, 1, 0): "V", (0, 1, 0, 0): "L", (0, 0, 0, 1): "R",
                 (0, 0, 1, 0): "T", (1, 0, 0, 0): "B", (0, 1, 1, 0): "NW", (0, 0, 1, 1): "NE",
                 (1, 1, 0, 0): "SW", (1, 0, 0, 1): "SE", (0, 0, 0, 0): "single"}
        for (x, y) in cells:
            k = tuple(int(c in cells) for c in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)))
            name = piece.get(k) or ("M" if k[1] and k[3] else "V")
            if name not in names:
                name = {"NW": "L", "SW": "L", "NE": "R", "SE": "R", "T": "single", "B": "single"}.get(name, "M")
                if name not in names:
                    name = "M"
            if name == "M" and "M2" in names and (x * 7 + y) % 5 == 0:
                name = "M2"
            self.piece(key, name, x, y)

    def woods(self, free, salt=0, aethos_only=lambda x, y: False, singles=None, big=(), from_bottom=False):
        """Fill `free` with an uneven wood: 2x2 trees (olives, the odd stone pine,
        and any `big` (key, w, h, chance) pieces) placed in a shuffled order so no
        two rows line up, cypresses in the gaps they leave, then the last single
        cells from `singles` (kythera pieces; shaded grass, blocked, in aethos-only
        strips). Returns the cells it filled."""
        free = set(free)
        filled = set(free)
        # top-down, west to east, so crowns stack; now and then a spot is skipped so
        # the next tree lands a cell over and the rows never settle into a grid
        # (from_bottom: bottom-up instead, so a wood against the map's top edge ends
        # in whole trees along its foot and leaves its odd cells along the edge)
        order = sorted(free, key=lambda c: ((-c[1] if from_bottom else c[1]), c[0]))
        for (x, y) in order:
            if (x, y) not in free:
                continue
            if from_bottom:
                y -= 1
                if not all(c in free for c in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))):
                    continue
            placed = False
            for (bk, bw, bh, chance) in big:
                cells = {(x + i, y + j) for i in range(bw) for j in range(bh)}
                if cells <= free and _hash(x, y, salt + 9) < chance and not any(aethos_only(*c) for c in cells):
                    self.put(bk, x, y)
                    free -= cells
                    placed = True
                    break
            if placed:
                continue
            cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if not all(c in free for c in cells) or _hash(x, y, salt + 5) < 110:
                continue
            r = _hash(x, y, salt + 1)
            if r < 150:
                self.pine(x, y)
            elif r < 230:
                self.cypress(x, y)
                self.cypress(x + 1, y)
            else:
                self.olive(x, y)
            free -= set(cells)
        for (x, y) in sorted(free, key=lambda c: (c[1], c[0])):
            if (x, y) in free and (x, y + 1) in free:
                self.cypress(x, y)
                free -= {(x, y), (x, y + 1)}
        singles = singles if singles is not None else [("myrtle", "bush"), ("myrtle", "bush"), ("flowers", "briar"),
                                                        ("myrtle", "single")]
        for (x, y) in sorted(free):
            if aethos_only(x, y) or not singles:
                # the shade between the trunks, closed
                self.set(x, y, A.SHADE, True)
                continue
            k, n = singles[_hash(x, y, salt + 3) % len(singles)]
            self.piece(k, n, x, y, solid=True)
        # a wood is walked round, never into: its crowns' tops too (the tips that
        # poke out over open ground beyond it stay walkable)
        for (x, y) in filled:
            self.solid[y, x] = True
        return filled

    def sand_rim(self, cells, grassy):
        """Soften where sand meets grass: each sand cell in `cells` with grass
        (`grassy(x, y)`) beside it takes aethos's sand-pit rim on those sides."""
        for (x, y) in cells:
            n, s_, w, e = grassy(x, y - 1), grassy(x, y + 1), grassy(x - 1, y), grassy(x + 1, y)
            v = "T" if n and not s_ else ("B" if s_ and not n else "")
            h = "L" if w and not e else ("R" if e and not w else "")
            if v or h:
                self.set(x, y, A.SAND_GRASS[v + h], False)

    def hidden(self, x, y, item, flag):
        self.bgs.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag})

    def min_grass(self, starts, goals, extra=()):
        """The fewest tall-grass steps on any walk from `starts` to any of `goals`
        (0-1 BFS, ledges one way): a forced band of depth n needs this >= n."""
        goals = set(goals)
        best = {s: 0 for s in starts}
        dq = deque((0, s) for s in starts)
        while dq:
            d, (x, y) = dq.popleft()
            if d > best.get((x, y), 1 << 30):
                continue
            if (x, y) in goals:
                return d
            for dx, dy in DIRS4:
                nx, ny = x + dx, y + dy
                if not self.ok(nx, ny):
                    continue
                b = self.behavior(int(self.mid[ny, nx]))
                if b in LEDGES:
                    lx, ly = LEDGES[b]
                    if (lx, ly) != (dx, dy) and not (ly == 1 and (dx, dy) == (0, 1)):
                        continue
                    nx, ny = nx + dx, ny + dy
                    if not self.walkable(nx, ny, extra):
                        continue
                elif not self.walkable(nx, ny, extra):
                    continue
                nd = d + (self.behavior(int(self.mid[ny, nx])) == "MB_TALL_GRASS")
                if nd < best.get((nx, ny), 1 << 30):
                    best[(nx, ny)] = nd
                    (dq.appendleft if nd == d else dq.append)((nd, (nx, ny)))
        return None

    # --- events ---------------------------------------------------------------------------
    def obj(self, gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
            local_id=None, rx=0, ry=0, item=None):
        if not gfx.startswith("OBJ_EVENT_GFX_"):
            gfx = "OBJ_EVENT_GFX_" + gfx
        e = {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
             "movement_range_x": rx, "movement_range_y": ry,
             "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
             "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag}
        if local_id:
            e = {"local_id": local_id, **e}
        self.objects.append(e)
        return e

    def item_ball(self, x, y, item, flag):
        return self.obj("ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag, item=item)

    def berry_tree(self, x, y, tree_id):
        e = self.obj("BERRY_TREE", x, y, "BerryTreeScript", move="MOVEMENT_TYPE_BERRY_TREE_GROWTH")
        e["trainer_sight_or_berry_tree_id"] = tree_id
        return e

    def warp(self, x, y, dest_map, dest_warp):
        self.warps.append({"x": x, "y": y, "elevation": 0, "dest_map": dest_map, "dest_warp_id": str(dest_warp)})
        return len(self.warps) - 1

    def trigger(self, x, y, script, var="VAR_TEMP_0", value="0"):
        self.coords.append({"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var,
                            "var_value": str(value), "script": script})

    def sign(self, x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
        self.bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing,
                         "script": script})

    def connect(self, direction, offset, dest):
        self.connections.append({"map": dest, "offset": offset, "direction": direction})

    def seam(self, side, depth=None):
        """Mark a seam strip: the `depth` rows/columns nearest `side` ('up', 'down',
        'left', 'right') may hold only primary metatiles (MAP_DESIGN.md §5)."""
        self.seams.append((side, depth or (6 if side in ("up", "down") else 8)))

    # --- output ---------------------------------------------------------------------------
    def encode(self):
        out = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                m = int(self.mid[y, x])
                elev = WATER_ELEV if self.behavior(m) in SURF else LAND_ELEV
                out[y, x] = m | (int(self.solid[y, x]) << 10) | (elev << 12)
        return out

    def layout_dir(self):
        return ROOT / "data/layouts" / self.name

    def write(self):
        d = self.layout_dir()
        d.mkdir(parents=True, exist_ok=True)
        self.encode().astype("<u2").tofile(d / "map.bin")
        np.array(self.border, np.uint16).astype("<u2").tofile(d / "border.bin")
        lp = ROOT / "data/layouts/layouts.json"
        lay = json.loads(lp.read_text())
        for entry in lay["layouts"]:
            if entry.get("blockdata_filepath") == f"data/layouts/{self.name}/map.bin":
                entry["width"], entry["height"] = self.w, self.h
                entry["primary_tileset"] = PRIMARY_DIR[self.primary]
                entry["secondary_tileset"] = self.cat["symbol"]
        lp.write_text(json.dumps(lay, indent=2, ensure_ascii=False) + "\n")
        mp = ROOT / "data/maps" / self.name / "map.json"
        mj = json.loads(mp.read_text())
        mj.update(self.header)
        mj["connections"] = self.connections or None
        mj["object_events"] = self.objects
        mj["warp_events"] = self.warps
        mj["coord_events"] = self.coords
        mj["bg_events"] = self.bgs
        mp.write_text(json.dumps(mj, indent=2, ensure_ascii=False) + "\n")

    # --- checks ---------------------------------------------------------------------------
    def walkable(self, x, y, extra=()):
        if not self.ok(x, y):
            return False
        if (x, y) in extra or (x, y) in self.forced_open:
            return True
        b = self.behavior(int(self.mid[y, x]))
        return not self.solid[y, x] and b not in SURF

    def reach(self, starts, blockers=(), extra=()):
        """Tiles reachable on foot from `starts`, ledges hopped one way; people in
        `blockers` stand in the way."""
        seen, q = set(), deque()
        for s in starts:
            seen.add(s)
            q.append(s)
        block = set(blockers)
        while q:
            x, y = q.popleft()
            for dx, dy in DIRS4:
                nx, ny = x + dx, y + dy
                if (nx, ny) in seen or (nx, ny) in block or not self.ok(nx, ny):
                    continue
                b = self.behavior(int(self.mid[ny, nx]))
                if b in LEDGES:
                    lx, ly = LEDGES[b]
                    if (lx, ly) == (dx, dy) or (ly == 1 and (dx, dy) == (0, 1)):
                        tx, ty = nx + dx, ny + dy
                        if self.walkable(tx, ty, extra) and (tx, ty) not in seen:
                            seen.add((tx, ty))
                            q.append((tx, ty))
                    continue
                if self.walkable(nx, ny, extra) or self.behavior(int(self.mid[ny, nx])) in DOORS:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        return seen

    def check(self, starts, must_reach=(), blockers=(), extra=()):
        errors = []
        for side, depth in self.seams:
            for y in range(self.h):
                for x in range(self.w):
                    inside = ((side == "up" and y < depth) or (side == "down" and y >= self.h - depth)
                              or (side == "left" and x < depth) or (side == "right" and x >= self.w - depth))
                    if inside and int(self.mid[y, x]) >= 0x200:
                        errors.append(f"({x},{y}) holds {self.ts} metatile 0x{int(self.mid[y, x]):03X} within "
                                      f"{depth} of the {side} seam; use {self.primary} there")
        reach = self.reach(starts, blockers, extra)
        for w in self.warps:
            b = self.behavior(int(self.mid[w["y"], w["x"]]))
            if b not in DOORS:
                errors.append(f"warp at ({w['x']},{w['y']}) is on {b}, not a door or mat")
            if (w["x"], w["y"]) not in reach and not w.get("unreached_ok"):
                errors.append(f"warp at ({w['x']},{w['y']}) is unreachable")
        for o in self.objects:
            x, y = o["x"], o["y"]
            if o["graphics_id"].endswith(("BERRY_TREE", "INVISIBLE")) or o.get("_floats"):
                continue
            if not self.walkable(x, y):
                b = self.behavior(int(self.mid[y, x]))
                errors.append(f"object {o.get('local_id') or o['script']} at ({x},{y}) stands on a solid cell ({b})")
        for t in self.coords:
            if (t["x"], t["y"]) not in reach:
                errors.append(f"trigger {t['script']} at ({t['x']},{t['y']}) is unreachable")
        for b in self.bgs:
            x, y = b["x"], b["y"]
            if b["type"] == "hidden_item" or (x, y) in reach:
                continue
            fronts = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
            if not any(p in reach for p in fronts):
                errors.append(f"bg event {b.get('script')} at ({x},{y}) can't be read from any walkable tile")
        for (x, y, what) in must_reach:
            if (x, y) not in reach:
                errors.append(f"{what} at ({x},{y}) is unreachable")
        for c in self.connections:
            side = c["direction"]
            edge = ([(x, 0) for x in range(self.w)] if side == "up" else
                    [(x, self.h - 1) for x in range(self.w)] if side == "down" else
                    [(0, y) for y in range(self.h)] if side == "left" else [(self.w - 1, y) for y in range(self.h)])
            if not any(p in reach for p in edge):
                errors.append(f"the {side} connection to {c['map']} has no reachable edge tile")
        return errors, reach

    # --- renders --------------------------------------------------------------------------
    def _render_bin(self, blocks, width, out, scale):
        tmp = ROOT / "build/kythera_maps" / f"{self.name}.bin"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        blocks.astype("<u2").tofile(tmp)
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                        "--width", str(width), "--primary", f"data/tilesets/primary/{self.primary}", "--secondary",
                        f"data/tilesets/secondary/{self.ts}", "--scale", str(scale), "-o", str(out)], check=True,
                       stdout=subprocess.DEVNULL)

    def render(self, stem, views=(), people=True):
        """stem.png (3x), stem_1x.png, stem_events.png (2x plan) and stem_views.png
        (GBA screens, 15x10, centred on each (x, y) in views, with the border)."""
        from PIL import Image, ImageDraw
        IMG.mkdir(parents=True, exist_ok=True)
        blocks = self.encode()
        self._render_bin(blocks, self.w, IMG / f"{stem}.png", 3)
        self._render_bin(blocks, self.w, IMG / f"{stem}_1x.png", 1)
        # the events plan
        base = ROOT / "build/kythera_maps" / f"{stem}_2x.png"
        self._render_bin(blocks, self.w, base, 2)
        im = Image.open(base).convert("RGBA")
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        c = 32
        for y in range(self.h):
            for x in range(self.w):
                if self.solid[y, x]:
                    d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 48))
        for o in self.objects:
            col = (255, 200, 0, 255) if o["trainer_type"] == "TRAINER_TYPE_NORMAL" else (0, 255, 120, 255)
            if o["graphics_id"].endswith("ITEM_BALL"):
                col = (255, 80, 255, 255)
            d.ellipse([o["x"] * c + 5, o["y"] * c + 5, o["x"] * c + c - 6, o["y"] * c + c - 6], outline=col, width=3)
            if o["trainer_type"] == "TRAINER_TYPE_NORMAL":
                rng = int(o["trainer_sight_or_berry_tree_id"])
                dx, dy = {"MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_UP": (0, -1),
                          "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}.get(o["movement_type"], (0, 1))
                for k in range(1, rng + 1):
                    tx, ty = o["x"] + dx * k, o["y"] + dy * k
                    d.rectangle([tx * c + 12, ty * c + 12, tx * c + c - 13, ty * c + c - 13], fill=(255, 200, 0, 140))
        for w in self.warps:
            d.rectangle([w["x"] * c + 2, w["y"] * c + 2, w["x"] * c + c - 3, w["y"] * c + c - 3], outline=(0, 255, 255, 255), width=3)
        for t in self.coords:
            d.rectangle([t["x"] * c + 9, t["y"] * c + 9, t["x"] * c + c - 10, t["y"] * c + c - 10], fill=(255, 0, 255, 170))
        for b in self.bgs:
            col = (255, 255, 255, 255) if b["type"] != "hidden_item" else (120, 120, 255, 255)
            d.line([b["x"] * c + 4, b["y"] * c + 4, b["x"] * c + c - 5, b["y"] * c + c - 5], fill=col, width=3)
            d.line([b["x"] * c + c - 5, b["y"] * c + 4, b["x"] * c + 4, b["y"] * c + c - 5], fill=col, width=3)
        Image.alpha_composite(im, lay).convert("RGB").save(IMG / f"{stem}_events.png")
        # screens with the border round the map
        if views:
            margin = 8
            bord = np.array(self.border, np.uint16).reshape(2, 2)
            H, W = self.h + 2 * margin, self.w + 2 * margin
            big = np.empty((H, W), np.uint16)
            for y in range(H):
                for x in range(W):
                    big[y, x] = bord[y % 2, x % 2] | (LAND_ELEV << 12)
            big[margin:margin + self.h, margin:margin + self.w] = blocks
            pad = ROOT / "build/kythera_maps" / f"{stem}_pad.png"
            self._render_bin(big, W, pad, 2)
            pim = Image.open(pad).convert("RGB")
            crops = []
            for (px, py) in views:
                x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
                crops.append(pim.crop((x0, y0, x0 + 15 * c, y0 + 10 * c)))
            cols = 3
            rows = -(-len(crops) // cols)
            sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, rows * 10 * c + (rows - 1) * 8), (24, 24, 32))
            for i, cr in enumerate(crops):
                sheet.paste(cr, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
            sheet.save(IMG / f"{stem}_views.png")

    def build(self, stem, starts, must_reach=(), views=(), blockers=(), extra=(), render=True):
        errors, reach = self.check(starts, must_reach, blockers, extra)
        self.write()
        if render:
            self.render(stem, views)
        for e in errors:
            print(f"{self.name} CHECK: {e}")
        print(f"{self.name}: {self.w}x{self.h}, {len(self.objects)} objects, {len(self.warps)} warps, "
              f"{len(self.coords)} triggers, {len(self.bgs)} bg events; {'checks pass' if not errors else f'{len(errors)} problems'}")
        return errors
