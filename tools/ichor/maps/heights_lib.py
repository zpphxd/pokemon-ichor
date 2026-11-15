"""The map-building kit for the Arkadian climb (tools/ichor/maps/heights.py).

A map is drawn as a grid of ground characters plus stamped structures, then
auto-tiled from the tilesets' catalogs (build/heights/<dir>/catalog.json):

  .  grass (aethos)        ,  barley tall grass        ;  Kyllene's combed tall grass
  =  road (soft edges)     #  limestone, seen from above
  |  a cliff face (one to four rows tall below rock, grass or woods)
  !  the Styx's black cliff face                       K  the Styx's black pool
  ~  a still pool (fishable)                           R  white water (blocks)
  F  fir woods             Y  cypress woods            S  deep-shade grass
  r  a terrace's north rim (blocks)                    n  a north ledge (jump north)
  <  a west ledge, >  an east ledge, _  a south ledge (aethos's)
  v  a ravine's dark floor  s  scree                   *  flowers (Kyllene)
  P  paving (aethos's limestone patch)                 @  under a stamp (set in code)

Seam rows: `aethos_rows`/`aethos_cols` may use only aethos metatiles (a
neighbor with another family of tilesets); `core_rows`/`core_cols` only aethos
or the core shared by gTileset_ArkadiaHeights, _StyxFalls and _Kyllene. Both
are enforced when a map is built.
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_lib as _KL  # noqa: E402
from kithairon_lib import (blob_key, grass_cells, hsh, item_ball, sign,  # noqa: E402,F401
                           trigger, warp, write_events)


def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
        local_id=None, rx=0, ry=0, item=None, elevation=3):
    e = _KL.obj(gfx, x, y, script, move, flag, trainer, sight, local_id, rx, ry, item)
    e["elevation"] = elevation
    return e

LEDGE_DIR = {"n": (0, -1), "<": (-1, 0), ">": (1, 0), "_": (0, 1)}


def reach(m, starts, blocked_extra=()):
    """Cells reachable on foot from the starts; ledges hop the way they face."""
    blocked_extra = set(blocked_extra)
    ok = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and not m.collision(x, y) and \
        (x, y) not in m.water_cells and (x, y) not in blocked_extra
    seen = set(s for s in starts if ok(*s))
    dq = deque(seen)
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < m.w and 0 <= ny < m.h and m.walkc[ny][nx] == "J":
                if m.ledge.get((nx, ny)) == (dx, dy):
                    nx, ny = nx + dx, ny + dy
                else:
                    continue
            if ok(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                dq.append((nx, ny))
    return seen

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/heights"
LAYOUTS = ROOT / "data/layouts/layouts.json"
RENDER = ROOT / "build/render/heights"
SHAPES = ROOT / "tools/ichor/art/heights_shapes.json"

SETS = {"heights": ("gTileset_ArkadiaHeights", "arkadia_heights"),
        "styx": ("gTileset_StyxFalls", "styx_falls"),
        "kyllene": ("gTileset_Kyllene", "kyllene"),
        "maia": ("gTileset_MaiaCave", "maia_cave")}
CORE = {"path", "rock", "face", "fir", "fir_stack", "fir_young", "oak", "cypress", "cypress_stack",
        "fir_shade", "fir_stack_shade", "fir_young_shade", "oak_shade", "cypress_shade",
        "cypress_stack_shade", "terraces", "marks", "rock_detail"}
SHAPE_SETS = ("tall", "meadow_tall", "path", "rock", "face", "bface", "water", "blackpool",
              "cwall", "cface")

# aethos metatiles (General's ids; design/phase1/TILES_aethos.md)
GRASS, TALL, SHADE, ANEMONE, UNDER_LIP = 0x001, 0x00D, 0x01C, 0x004, 0x002
PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
         "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
LEDGE_S, LEDGE_S_L, LEDGE_S_R = 0x087, 0x0D5, 0x0D6
LEDGE_W, LEDGE_E = 0x085, 0x086
STELE, BOULDER = 0x003, 0x0E0
WALL_EW, WALL_W, WALL_E, WALL_NS = 0x149, 0x148, 0x14A, 0x132     # aethos's dry-stone walls
SEA_ROCK = (0x0C5, 0x0CD)            # aethos's boulders in the water, a foam ring round them
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
PINE_TOP, PINE_BOT = (0x01E, 0x01F), (0x026, 0x027)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
FACE_CH = {"|": "face", "!": "bface"}


class Catalog:
    def __init__(self, setname):
        p = CAT / SETS[setname][1] / "catalog.json"
        if not p.exists():
            sys.exit(f"{p} is missing: run /usr/bin/python3 tools/ichor/art/heights_build.py")
        self.setname = setname
        self.s = {d["key"]: d for d in json.loads(p.read_text())["structures"]}
        self.core_ids = set()
        for k, d in self.s.items():
            if k in CORE:
                for row in d["ids"]:
                    self.core_ids.update(row)

    def has(self, key, name=None):
        return key in self.s and (name is None or name in self.s[key]["names"])

    def cell(self, key, cx, cy):
        d = self.s[key]
        return d["ids"][cy][cx], d["walk"][cy][cx]

    def named(self, key, name):
        cx, cy = self.s[key]["names"][name]
        return self.cell(key, cx, cy)


class Map:
    def __init__(self, name, w, h, setname):
        self.name, self.w, self.h, self.setname = name, w, h, setname
        self.cat = Catalog(setname)
        self.ch = [["."] * w for _ in range(h)]
        self.mt = [[None] * w for _ in range(h)]
        self.walkc = [["."] * w for _ in range(h)]
        self.elev = {}
        self.ledge = {}
        self.force_block = set()
        self.force_open = set()
        self.aethos_rows, self.core_rows = set(), set()
        self.aethos_cols, self.core_cols = set(), set()
        self.pathlike = set()
        self.no_decor = set()
        self.shapes_used = {k: set() for k in SHAPE_SETS}
        self.missing = []
        self.buttons = set()
        self.water_cells = set()
        self.stamped = set()
        self.seed = sum(map(ord, name))
        self.decor_rate = 7

    # --- the ground grid -------------------------------------------------------
    def grid(self, rows):
        assert len(rows) == self.h, (self.name, len(rows))
        for y, r in enumerate(rows):
            assert len(r) == self.w, (self.name, y, len(r))
            self.ch[y] = list(r)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            for x in range(max(0, x0), min(self.w - 1, x1) + 1):
                self.ch[y][x] = c

    def cells(self, pts, c):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.ch[y][x] = c

    def at(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.ch[y][x]
        return None

    def seam(self, cell):
        x, y = cell
        return y in self.aethos_rows or x in self.aethos_cols

    def core_seam(self, cell):
        x, y = cell
        return y in self.core_rows or x in self.core_cols

    # --- stamps ----------------------------------------------------------------
    def put(self, x, y, mid, walk="X"):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        self.mt[y][x] = mid
        self.walkc[y][x] = walk
        self.ch[y][x] = "@"
        self.stamped.add((x, y))

    def stamp(self, key, x, y, cells=None, names=None):
        d = self.cat.s[key]
        if names:
            for (dx, dy), n in names.items():
                mid, wk = self.cat.named(key, n)
                self.put(x + dx, y + dy, mid, wk)
            return
        for cy in range(d["h"]):
            for cx in range(d["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                mid, wk = self.cat.cell(key, cx, cy)
                self.put(x + cx, y + cy, mid, wk)

    def named(self, key, name, x, y):
        mid, wk = self.cat.named(key, name)
        self.put(x, y, mid, wk)

    def button(self, x, y):
        """A drum's button on the road at (x, y): the road's own shape there, as
        MB_STRENGTH_BUTTON (the `buttons` piece; heights_build.BUTTON_SHAPES)."""
        assert self.ch[y][x] == "=", (self.name, x, y, "a button goes on the road")
        self.buttons.add((x, y))

    def tree(self, kind, x, y):
        """A fir (2 x 3), oak (2 x 2), young fir or cypress (1 x 2/3): (x, y) its
        top-left (the spire row)."""
        self.stamp(kind, x, y)

    def olive(self, x, y):
        if self.at(x, y - 1) == "." and (x, y - 1) not in self.stamped:
            self.put(x, y - 1, OLIVE_TIP[0], "T")
            self.put(x + 1, y - 1, OLIVE_TIP[1], "T")
        self.put(x, y, OLIVE_TOP[0]); self.put(x + 1, y, OLIVE_TOP[1])
        self.put(x, y + 1, OLIVE_BOT[0]); self.put(x + 1, y + 1, OLIVE_BOT[1])

    def pine(self, x, y):
        self.put(x, y, PINE_TOP[0]); self.put(x + 1, y, PINE_TOP[1])
        self.put(x, y + 1, PINE_BOT[0]); self.put(x + 1, y + 1, PINE_BOT[1])

    def acypress(self, x, y):
        """aethos's small cypress (1 x 2), for the seam strips."""
        self.put(x, y, CYPRESS_TOP, "T")
        self.put(x, y + 1, CYPRESS_BOT)

    # --- auto-tiling -----------------------------------------------------------
    def region(self, chars, extra=()):
        extra = set(extra)
        return lambda x, y: (not (0 <= x < self.w and 0 <= y < self.h)) or \
            self.ch[y][x] in chars or (x, y) in extra

    def shape(self, setkey, key):
        self.shapes_used[setkey].add(key)
        d = self.cat.s.get(setkey)
        if d and key in d["names"]:
            return self.cat.named(setkey, key)
        self.missing.append((self.name, setkey, key))
        if d:
            first = next(iter(d["names"]))
            return self.cat.named(setkey, first)
        return (GRASS, ".")

    def patch(self, inside, x, y):
        n, s_, w_, e = inside(x, y - 1), inside(x, y + 1), inside(x - 1, y), inside(x + 1, y)
        v = "T" if not n else ("B" if not s_ else "")
        hz = "L" if not w_ else ("R" if not e else "")
        return PATCH.get((v + hz) or "C", PATCH["C"])

    def face_key(self, x, y, ch):
        """The face piece for (x, y): lip, foot, open sides, a facet variant."""
        fchars = "|!"
        mass = fchars + "#"
        n = self.at(x, y - 1)
        s = self.at(x, y + 1)
        w = self.at(x - 1, y)
        e = self.at(x + 1, y)
        lip = "-" if (n is None or n == ch) else ("r" if n == "#" else "g")
        foot = s is not None and s != ch
        wo = w is not None and w not in mass and w != "@"
        eo = e is not None and e not in mass and e != "@"
        var = hsh(x, y, self.seed + 3) % 3 if not (wo or eo) else 0
        return (f"{lip}{'f' if foot else '-'}{'w' if wo else '-'}{'e' if eo else '-'}{var}")

    def autotile(self):
        ch = self.ch
        tall = self.region(",")
        mtall = self.region(";")
        road = self.region("=", self.pathlike)
        rock = self.region("#|")
        water = self.region("~")
        pool = self.region("K")
        pave = self.region("P")
        for y in range(self.h):
            for x in range(self.w):
                if self.mt[y][x] is not None:
                    continue
                c = ch[y][x]
                aeth = self.seam((x, y))
                if self.setname == "maia":
                    if c == ".":
                        self.set(x, y, *self.cat.named("cfloor", "pebbles" if hsh(x, y, 3) < 14 else "plain"))
                    elif c == "#":
                        self.set(x, y, *self.shape("cwall", blob_key(rock, x, y)))
                    elif c == "|":
                        self.set(x, y, *self.shape("cface", self.face_key(x, y, c)[:4] + "0"))
                    elif c == "@":
                        self.set(x, y, *self.cat.named("cfloor", "plain"))
                    else:
                        raise ValueError(f"{self.name}: unknown cave ground {c!r} at {x},{y}")
                    continue
                if c == ".":
                    self.set(x, y, GRASS, ".")
                elif c == "S":
                    self.set(x, y, SHADE, ".")
                elif c == ",":
                    if aeth or self.core_seam((x, y)):
                        self.set(x, y, TALL, "G")       # aethos's barley at a seam
                    else:
                        self.set(x, y, *self.shape("tall", blob_key(tall, x, y)))
                elif c == ";":
                    if aeth or self.core_seam((x, y)):
                        self.set(x, y, TALL, "G")
                    else:
                        self.set(x, y, *self.shape("meadow_tall", blob_key(mtall, x, y)))
                elif c == "=":
                    if aeth:
                        self.set(x, y, self.patch(self.region("="), x, y), ".")
                    elif (x, y) in self.buttons:
                        key = blob_key(road, x, y)
                        if not self.cat.has("buttons", key):
                            raise ValueError(f"{self.name}: no button on road shape {key} at {x},{y}: "
                                             "add it to heights_build.BUTTON_SHAPES")
                        self.set(x, y, *self.cat.named("buttons", key))
                    else:
                        self.set(x, y, *self.shape("path", blob_key(road, x, y)))
                elif c == "P":
                    self.set(x, y, self.patch(pave, x, y), ".")
                elif c == "#":
                    assert not aeth, (self.name, x, y, "rock in an aethos-only strip")
                    k = blob_key(rock, x, y)
                    if k == "1|11111111" and hsh(x, y, self.seed) < 22 and self.at(x, y + 1) == "#":
                        name = ("crack", "boulders", "juniper", "fern")[hsh(x, y, 5) % 4]
                        self.set(x, y, *self.cat.named("rock_detail", name))
                        self.shapes_used["rock"].add(k)
                    else:
                        self.set(x, y, *self.shape("rock", k))
                elif c in FACE_CH:
                    assert not aeth, (self.name, x, y, "a cliff in an aethos-only strip")
                    self.set(x, y, *self.shape(FACE_CH[c], self.face_key(x, y, c)))
                elif c == "~":
                    assert not aeth
                    self.set(x, y, *self.shape("water", blob_key(self.region("~R"), x, y)))
                    self.water_cells.add((x, y))
                elif c == "K":
                    k = blob_key(pool, x, y)
                    h = hsh(x, y, self.seed + 9) % 10
                    if k == "1|11111111" and h < 7 and self.cat.has("blackpool_deep"):
                        self.set(x, y, *self.cat.named("blackpool_deep", "glint" if h == 0 else "deep"))
                        self.shapes_used["blackpool"].add(k)
                    else:
                        self.set(x, y, *self.shape("blackpool", k))
                    self.water_cells.add((x, y))
                elif c == "w":
                    ns = self.at(x, y - 1) == "w" or self.at(x, y + 1) == "w"
                    we = self.at(x - 1, y) == "w"
                    ea = self.at(x + 1, y) == "w"
                    mid = WALL_NS if (ns and not (we or ea)) else (
                        WALL_EW if (we and ea) else (WALL_W if ea else (WALL_E if we else WALL_EW)))
                    self.set(x, y, mid, "X")
                elif c == "R":
                    # white water: foam in the channel's middle, a gravel bank at its
                    # edges; blocked at the walking elevation, so never surfed or fished
                    k = blob_key(self.region("R~"), x, y)
                    if k == "1|11111111":
                        h = hsh(x, y, 11) % 12
                        if h == 0:
                            self.set(x, y, SEA_ROCK[hsh(x, y, 4) % 2], "X")
                        else:
                            self.set(x, y, *self.cat.named("rapids", ("a", "b", "c")[h % 3]))
                    else:
                        self.set(x, y, self.shape("water", k)[0], "X")
                elif c == "r":
                    l = self.at(x - 1, y) in ("r", "n")
                    rr = self.at(x + 1, y) in ("r", "n")
                    name = "rim" if (l and rr) else ("rim_L" if rr else ("rim_R" if l else "rim"))
                    self.set(x, y, *self.cat.named("terraces", name))
                elif c == "n":
                    l = self.at(x - 1, y) in ("r", "n")
                    rr = self.at(x + 1, y) in ("r", "n")
                    name = "nl" if (l and rr) else ("nl_L" if rr else ("nl_R" if l else "nl"))
                    self.set(x, y, *self.cat.named("terraces", name))
                elif c == "<":
                    self.set(x, y, LEDGE_W, "J")
                elif c == ">":
                    self.set(x, y, LEDGE_E, "J")
                elif c == "_":
                    l = self.at(x - 1, y) == "_"
                    rr = self.at(x + 1, y) == "_"
                    self.set(x, y, LEDGE_S if (l and rr) else (LEDGE_S_L if rr else (LEDGE_S_R if l else LEDGE_S)), "J")
                elif c == "v":
                    self.set(x, y, *self.cat.named("chasm", "void"))
                elif c == "s":
                    self.set(x, y, *self.cat.named("marks", "scree" if hsh(x, y) % 2 else "scree_b"))
                elif c == "b":
                    self.set(x, y, BOULDER, "X")
                elif c == "*":
                    self.set(x, y, *self.cat.named("decor", ("gentian", "crocus", "thyme")[hsh(x, y, 2) % 3]))
                elif c in "FY":
                    pass
                elif c == "@":
                    self.set(x, y, GRASS, ".")
                else:
                    raise ValueError(f"{self.name}: unknown ground {c!r} at {x},{y}")
        self.woods()
        self.decorate()
        self.shadows()

    def shadows(self):
        """The grass at a cliff's foot or under a rim sits in its shadow."""
        for y in range(1, self.h):
            for x in range(self.w):
                if self.mt[y][x] != GRASS or (x, y) in self.stamped or self.seam((x, y)):
                    continue
                if self.ch[y - 1][x] in "|!" and self.cat.has("terraces", "under") is not None:
                    self.set(x, y, UNDER_LIP, ".")

    def decorate(self):
        rate = self.decor_rate
        for y in range(self.h):
            for x in range(self.w):
                if self.mt[y][x] != GRASS or (x, y) in self.stamped or self.ch[y][x] != ".":
                    continue
                if (x, y) in self.no_decor:
                    continue
                h = hsh(x, y, self.seed + 17)
                if h >= rate:
                    continue
                if self.seam((x, y)) or self.core_seam((x, y)) or not self.cat.has("decor"):
                    if h < rate // 2 or self.seam((x, y)):
                        self.set(x, y, ANEMONE if hsh(x, y, 29) % 3 == 0 else GRASS, ".")
                    else:
                        self.set(x, y, *self.cat.named("marks", "scree" if hsh(x, y, 7) % 2 else "scree_b"))
                    continue
                pick = hsh(x, y, 23) % 4
                if pick == 3:
                    self.set(x, y, ANEMONE, ".")
                else:
                    self.set(x, y, *self.cat.named("decor", ("gentian", "crocus", "thyme")[pick]))

    def set(self, x, y, mid, walk):
        self.mt[y][x] = mid
        self.walkc[y][x] = walk
        c = self.ch[y][x]
        if walk == "J" and c in LEDGE_DIR:
            self.ledge[(x, y)] = LEDGE_DIR[c]

    def woods(self):
        """Fill 'F' with firs and 'Y' with cypresses: column pairs (firs) or
        single columns (cypresses), each run stacked spire, crown, stack...,
        foot; every other column a row lower, so the woods don't stand in ranks."""
        F = lambda x, y: 0 <= x < self.w and 0 <= y < self.h and self.ch[y][x] == "F"
        Y = lambda x, y: 0 <= x < self.w and 0 <= y < self.h and self.ch[y][x] == "Y"
        done = set()
        for x in range(0, self.w, 2):
            y = 0
            while y < self.h:
                if not (F(x, y) and F(x + 1, y)):
                    y += 1
                    continue
                y0 = y
                while F(x, y) and F(x + 1, y):
                    y += 1
                self._fir_run(x, y0, y - 1, done)
        for x in range(self.w):
            y = 0
            while y < self.h:
                isf = F(x, y) and (x, y) not in done
                isy = Y(x, y)
                if not (isf or isy):
                    y += 1
                    continue
                y0 = y
                test = (lambda xx, yy: F(xx, yy) and (xx, yy) not in done) if isf else Y
                while test(x, y):
                    y += 1
                self._column(x, y0, y - 1, done, "fir_young" if isf else "cypress")
        for c in done:
            self.force_block.add(c)

    def _spire_ok(self, x, y0, cols=1):
        if y0 <= 0 or self.seam((x, y0 - 1)):
            return False
        return all(self.at(xx, y0 - 1) in (".", "S") and (xx, y0 - 1) not in self.stamped
                   and self.mt[y0 - 1][xx] in (None, GRASS, SHADE) for xx in range(x, x + cols))

    def _column(self, x, y0, y1, done, kind):
        """A single column of young firs (1 x 2) or cypresses (1 x 3)."""
        for yy in range(y0, y1 + 1):
            done.add((x, yy))
        n = y1 - y0 + 1
        if kind == "fir_young":
            yy = y0
            if n % 2 and self._spire_ok(x, y0):
                self.set(x, y0 - 1, *self.cat.cell("fir_young", 0, 0))
                self.set(x, y0, *self.cat.cell("fir_young_shade", 0, 1))
                yy += 1
            elif n % 2:
                self.set(x, yy, SHADE, "X")
                yy += 1
            while yy + 1 <= y1:
                self.set(x, yy, *self.cat.cell("fir_young_shade", 0, 0))
                self.set(x, yy + 1, *self.cat.cell("fir_young_shade", 0, 1))
                yy += 2
            return
        # cypresses: spire over the row above if it can, crown, (stack, crown)..., foot
        lower = (x % 2 == 1) and n >= 4
        top = y0 - 1 if (self._spire_ok(x, y0) and not lower) else y0
        if top == y0 - 1:
            self.set(x, top, *self.cat.cell("cypress", 0, 0))
        else:
            self.set(x, y0, *self.cat.cell("cypress_shade", 0, 0))
        r = top + 1
        while r <= y1:
            self.set(x, r, *self.cat.cell("cypress_shade", 0, 1))
            if r + 1 > y1:
                break
            if r + 2 <= y1:
                self.set(x, r + 1, *self.cat.cell("cypress_stack_shade", 0, 0))
                r += 2
            else:
                self.set(x, r + 1, *self.cat.cell("cypress_shade", 0, 2))
                r += 2

    def _fir_run(self, x, y0, y1, done):
        n = y1 - y0 + 1
        for yy in range(y0, y1 + 1):
            done.add((x, yy))
            done.add((x + 1, yy))
        if n == 1:
            for xx in (x, x + 1):
                self.set(xx, y0, SHADE, "X")
            return
        if n == 2:
            for i in range(2):
                self.set(x + i, y0, *self.cat.cell("fir_young_shade", 0, 0))
                self.set(x + i, y0 + 1, *self.cat.cell("fir_young_shade", 0, 1))
            return
        above_ok = self._spire_ok(x, y0, 2)
        t = y0 - 1 if (above_ok and (y1 - (y0 - 1)) % 2 == 0) else (y0 if (y1 - y0) % 2 == 0 else y0 + 1)
        end = y1
        if (x // 2) % 2 == 1 and n >= 5:
            t, end = t + 1, y1 - 1
        for yy in range(y0, t):
            for xx in (x, x + 1):
                self.set(xx, yy, SHADE, "X")
        for yy in range(end + 1, y1 + 1):
            for xx in (x, x + 1):
                self.set(xx, yy, SHADE, "X")
        if t >= 0:
            for i, xx in enumerate((x, x + 1)):
                self.set(xx, t, *self.cat.cell("fir" if t < y0 else "fir_shade", i, 0))
        r = t + 1
        while r + 1 <= end:
            for i, xx in enumerate((x, x + 1)):
                self.set(xx, r, *self.cat.cell("fir_shade", i, 1))
                last = r + 2 > end - 1
                if last:
                    self.set(xx, r + 1, *self.cat.cell("fir_shade", i, 2))
                else:
                    self.set(xx, r + 1, *self.cat.cell("fir_stack_shade", i, 0))
            r += 2

    # --- output ------------------------------------------------------------------
    def check_seams(self):
        errs = []
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                if self.seam((x, y)) and m >= 0x200:
                    errs.append(f"{self.name} ({x},{y}): 0x{m:03X} in an aethos-only seam strip")
                if self.core_seam((x, y)) and m >= 0x200 and m not in self.cat.core_ids:
                    errs.append(f"{self.name} ({x},{y}): 0x{m:03X} is not core in a core-only seam strip")
        return errs

    def collision(self, x, y):
        if (x, y) in self.force_open:
            return 0
        if (x, y) in self.force_block:
            return 1
        return 1 if self.walkc[y][x] in ("X", "J") else 0

    def blocks(self):
        b = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                assert m is not None, (self.name, x, y)
                if (x, y) in self.water_cells:
                    b[y, x] = m | (1 << 12)
                elif self.collision(x, y):
                    b[y, x] = m | (1 << 10) | (self.elev.get((x, y), 3) << 12)
                else:
                    b[y, x] = m | (self.elev.get((x, y), 3) << 12)
        return b


# --------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------

def write_layout(layout_id, folder, m, border, primary="gTileset_Aethos"):
    d = ROOT / "data/layouts" / folder
    d.mkdir(parents=True, exist_ok=True)
    m.blocks().tofile(d / "map.bin")
    np.array(border, "<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == layout_id:
            lay.update({"width": m.w, "height": m.h, "primary_tileset": primary,
                        "secondary_tileset": SETS[m.setname][0]})
            break
    else:
        sys.exit(f"no layout {layout_id}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# Rendering and checks
# --------------------------------------------------------------------------

def renderer(secondary):
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                           rm.Tileset(rm.resolve_tileset(secondary, syms)))


def render(m, events, border, views, tag=""):
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer(SETS[m.setname][0])
    RENDER.mkdir(parents=True, exist_ok=True)
    blocks = m.blocks()
    img = rm.render_blocks(r, (blocks & 0x3FF).ravel(), m.w)
    plain = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
    plain.save(RENDER / f"{m.name}{tag}.png")
    s = 3
    rev = img.resize((img.width * s, img.height * s), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", rev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    font = ImageFont.load_default(size=11)
    cell = 16 * s
    for y in range(m.h):
        for x in range(m.w):
            if (x, y) in m.water_cells:
                continue
            if m.collision(x, y):
                d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=(255, 0, 0, 55))
            if m.walkc[y][x] == "G":
                d.rectangle([x * cell + 2, y * cell + 2, x * cell + cell - 3, y * cell + cell - 3],
                            outline=(0, 255, 0, 90), width=1)
    colors = {"sign": (255, 220, 0), "hidden_item": (0, 220, 120), "trigger": (255, 0, 255)}
    for e in events.get("object_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 4, y * cell + 4, x * cell + cell - 5, y * cell + cell - 5], outline=(40, 80, 255), width=3)
        label = e["script"].split("_")[-1] if e["script"] != "Common_EventScript_FindItem" else e["trainer_sight_or_berry_tree_id"][5:]
        d.text((x * cell + 2, y * cell + 2), label[:8], fill=(255, 255, 255, 255), font=font, stroke_width=2,
               stroke_fill=(0, 0, 0, 255))
    for e in events.get("bg_events", []) + events.get("coord_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 10, y * cell + 10, x * cell + cell - 11, y * cell + cell - 11],
                    outline=colors.get(e["type"], (255, 255, 255)), width=3)
    for e in events.get("warp_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 14, y * cell + 14, x * cell + cell - 15, y * cell + cell - 15],
                    outline=(0, 255, 255), width=4)
    for i in range(max(m.w, m.h)):
        if i < m.w:
            d.text((i * cell + cell // 2 - 6, 0), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2,
                   stroke_fill=(0, 0, 0, 255))
        if i < m.h:
            d.text((2, i * cell + cell // 2 - 6), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2,
                   stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(rev, over).convert("RGB").save(RENDER / f"{m.name}{tag}_review.png")
    pad = 8
    W, H = m.w + 2 * pad, m.h + 2 * pad
    big = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            big[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
    big[pad:pad + m.h, pad:pad + m.w] = blocks & 0x3FF
    full = rm.render_blocks(r, big.ravel(), W)
    shots = []
    for (px, py) in views:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16 + 8
        shots.append(full.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
    if shots:
        cols = 3
        nrows = (len(shots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 488 + 8, nrows * 328 + 8), (24, 24, 32))
        for i, sh in enumerate(shots):
            sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
        sheet.save(RENDER / f"{m.name}{tag}_screens.png")
    return plain


def forced_bands(m, entries, exits, people=(), opens=()):
    """The grass patches every walk from the entry to the far exit must cross."""
    grass = grass_cells(m)
    parts, left = [], set(grass)
    while left:
        c = left.pop()
        part, todo = {c}, [c]
        while todo:
            x, y = todo.pop()
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                n = (x + dx, y + dy)
                if n in left:
                    left.discard(n)
                    part.add(n)
                    todo.append(n)
        parts.append(part)
    m.force_open |= set(opens)
    forced = []
    for part in parts:
        r = reach(m, entries, blocked_extra=set(people) | part)
        if not (set(exits) & r):
            xs = sorted({x for x, _ in part}); ys = sorted({y for _, y in part})
            forced.append((xs[0], xs[-1], ys[0], ys[-1], len(part)))
    m.force_open -= set(opens)
    return forced, parts
