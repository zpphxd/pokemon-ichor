#!/usr/bin/env python3
"""Build Route 8, the Kopais shore (MAP_ROUTE8_KOPAIS, 64 x 26; design/phase3/SCRIPT.md
beat 35A, Part 2's Route 8).

West from Thyrsa's Neistan Gate along the south shore of Lake Kopais: the lake on the
north edge, then the reed beds, then the road, then the grey foot of Mount Phikion. The
map is drawn below as a ground grid (legend in GROUND), stamped with the tileset's
structures, then auto-tiled from build/kopais/catalog.json with class keys
(tools/ichor/art/kopais_lib.py). It writes:

  data/layouts/Route8_Kopais/{map,border}.bin and the layout's entry in layouts.json
  data/maps/Route8_Kopais/map.json: events, connections and music
  build/render/kopais/Route8_Kopais.png, _review.png (collision and events) and
  _screens.png (15 x 10 GBA screens along the road)
  design/phase3/img/Route8_Kopais.png (2x), for the director

Usage:
  /usr/bin/python3 tools/ichor/maps/kopais.py            # build the map
  /usr/bin/python3 tools/ichor/maps/kopais.py --shapes   # list the class keys the map
      uses in tools/ichor/art/kopais_shapes.json; then rebuild the tileset
      (tools/ichor/art/kopais_build.py) and run this again
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_lib as KL  # noqa: E402
from kithairon_lib import ROOT, item_ball, obj, sign, trigger  # noqa: E402,F401

KL.SETS["kopais"] = ("gTileset_Kopais", "kopais")
KL.RENDER = ROOT / "build/render/kopais"
CAT = ROOT / "build/kopais/catalog.json"
SHAPES = ROOT / "tools/ichor/art/kopais_shapes.json"
IMG = ROOT / "design/phase3/img"
NAME, LAYOUT = "Route8_Kopais", "LAYOUT_ROUTE8_KOPAIS"
W, H = 64, 26
P = "OBJ_EVENT_GFX_ICHOR_"
S8 = "Route8_Kopais_EventScript_"
MUSIC = "MUS_ICHOR_ROAD"        # SCRIPT.md Part 9: Routes 8 and 9 play the built road cue

# Seams (design/phase3/BUILD.md, batch 2)
WEST_ROAD = 12          # Lebadeia: road rows 12-13, verges 11 and 14, offset 0
EAST_ROAD = 14          # Thyrsa's Neistan Gate (its rows 23-24) meets rows q = 14, 15
SEAM_W = range(0, 8)    # aethos-only columns, both edges
SEAM_E = range(56, 64)

# aethos metatiles (design/phase1/TILES_aethos.md)
GRASS, ANEMONE, TALL, LONG, SEA, STELE = 0x001, 0x004, 0x00D, 0x015, 0x170, 0x003
BOULDER = 0x0E0
PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
         "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
OLIVE_TOP, OLIVE_BOT, OLIVE_STACK, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1DC, 0x1DD), (0x1CE, 0x1CF)
PINE_TOP, PINE_BOT = (0x01E, 0x01F), (0x026, 0x027)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016

# --------------------------------------------------------------------------
# Ground: characters, the class each shows its neighbors, and the set it uses
# --------------------------------------------------------------------------
#   .  grass            ,  reeds (MB_LONG_GRASS)     ~  marsh water      L  the lake
#   m  mudflat          =  the road                  ;  barley (spur)     #  Phikion rock
#   D  the dike         G  Gla                        @  under a stamp on land
#   b  a maquis bush    o  a boulder
CLASS = {",": "r", "~": "w", "L": "L", "m": "m", "D": "s", "G": "s"}
SETS = {"reeds": ",", "marsh": "~", "lake": "L", "mud": "m", "path": "=", "barley": ";",
        "crag": "#"}
ALSO_OWN = {"path": "D"}          # the road runs on over the dike's top


class Catalog:
    def __init__(self):
        if not CAT.exists():
            sys.exit(f"{CAT} is missing: run /usr/bin/python3 tools/ichor/art/kopais_build.py")
        self.s = {d["key"]: d for d in json.loads(CAT.read_text())["structures"]}

    def has(self, key, name=None):
        return key in self.s and (name is None or name in self.s[key]["names"])

    def cell(self, key, cx, cy):
        d = self.s[key]
        return d["ids"][cy][cx], d["walk"][cy][cx]

    def named(self, key, name):
        cx, cy = self.s[key]["names"][name]
        return self.cell(key, cx, cy)


def hsh(x, y, salt=0):
    return KL.hsh(x, y, salt)


class Map:
    def __init__(self):
        self.name, self.w, self.h, self.setname = NAME, W, H, "kopais"
        self.cat = Catalog()
        self.ch = [["."] * W for _ in range(H)]
        self.mt = [[None] * W for _ in range(H)]
        self.walkc = [["."] * W for _ in range(H)]
        self.stamped = set()
        self.force_block, self.force_open = set(), set()
        self.water_cells = set()
        self.shapes_used = {k: set() for k in SETS}
        self.missing = []
        self.no_decor = set()

    def at(self, x, y):
        if 0 <= x < W and 0 <= y < H:
            return self.ch[y][x]
        return None

    def set_ch(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.ch[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(H - 1, y1) + 1):
            for x in range(max(0, x0), min(W - 1, x1) + 1):
                self.ch[y][x] = c

    def cells(self, pts, c):
        for (x, y) in pts:
            self.set_ch(x, y, c)

    # --- stamps ------------------------------------------------------------
    def put(self, x, y, mid, walk="X"):
        if not (0 <= x < W and 0 <= y < H):
            return
        self.mt[y][x] = mid
        self.walkc[y][x] = walk
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

    def olive(self, x, y, tip=True):
        if tip and self.at(x, y - 1) == "." and (x, y - 1) not in self.stamped:
            self.put(x, y - 1, OLIVE_TIP[0], "T")
            self.put(x + 1, y - 1, OLIVE_TIP[1], "T")
        self.put(x, y, OLIVE_TOP[0]); self.put(x + 1, y, OLIVE_TOP[1])
        below_olive = (x, y + 2) in self.olives
        bot = OLIVE_STACK if below_olive else OLIVE_BOT
        self.put(x, y + 1, bot[0]); self.put(x + 1, y + 1, bot[1])

    def pine(self, x, y):
        self.put(x, y, PINE_TOP[0]); self.put(x + 1, y, PINE_TOP[1])
        self.put(x, y + 1, PINE_BOT[0]); self.put(x + 1, y + 1, PINE_BOT[1])

    def cypress(self, x, y):
        self.put(x, y, CYPRESS_TOP, "T")
        self.put(x, y + 1, CYPRESS_BOT)

    # --- class keys ----------------------------------------------------------
    def key(self, setname, x, y):
        """The cell's class key, canonical for its set: classes the set counts as
        its own ground become '1', the rest become what the set paints for them,
        and a diagonal that doesn't count takes its sides' class. Keys that
        would paint the same piece are the same key, so the set stays small."""
        own = SETS[setname] + ALSO_OWN.get(setname, "")
        raw = []
        for dx, dy in KL.NEIGH:
            c = self.at(x + dx, y + dy)
            raw.append("1" if (c is None or c in own) else CLASS.get(c, "g"))
        inside = {"marsh": "1rsL", "mud": "1wr", "lake": "1s"}.get(setname, "1")
        out = ["1" if c in inside else c for c in raw]
        if setname == "reeds":
            out = ["w" if c == "L" else (c if c in "1wm" else "g") for c in out]
            if any(c in "gm" for c in out):
                out = ["m" if c == "w" else c for c in out]
        elif setname == "marsh":
            out = [c if c in "1m" else "g" for c in out]
        else:
            out = [c if c == "1" else "g" for c in out]
        for d, (a, b) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
            if not (out[a] == "1" and out[b] == "1"):
                out[d] = [out[i] for i in (a, b) if out[i] != "1"][0]
        return "1|" + "".join(out)

    def shape(self, setname, x, y):
        k = self.key(setname, x, y)
        self.shapes_used[setname].add(k)
        d = self.cat.s.get(setname)
        if d and k in d["names"]:
            return self.cat.named(setname, k)
        self.missing.append((setname, k))
        return self.cat.named(setname, "1|11111111")

    def seam(self, x):
        return x in SEAM_W or x in SEAM_E

    def patch(self, x, y):
        road = lambda xx, yy: self.at(xx, yy) in ("=", None)
        n, s_, w_, e = road(x, y - 1), road(x, y + 1), road(x - 1, y), road(x + 1, y)
        v = "T" if not n else ("B" if not s_ else "")
        hz = "L" if not w_ else ("R" if not e else "")
        return PATCH.get((v + hz) or "C", PATCH["C"])

    # --- auto-tiling -----------------------------------------------------------
    def autotile(self):
        for y in range(H):
            for x in range(W):
                if self.mt[y][x] is not None:
                    continue
                c = self.ch[y][x]
                seam = self.seam(x)
                if c == ".":
                    self.set(x, y, GRASS, ".")
                elif c == ",":
                    self.set(x, y, *((LONG, "G") if seam else self.shape("reeds", x, y)))
                elif c == "~":
                    assert not seam, (x, y, "marsh in a seam column")
                    self.set(x, y, *self.shape("marsh", x, y))
                    self.water_cells.add((x, y))
                elif c == "L":
                    if seam:
                        self.set(x, y, SEA, "X")
                    else:
                        self.set(x, y, *self.shape("lake", x, y))
                    self.water_cells.add((x, y))
                elif c == "m":
                    assert not seam
                    self.set(x, y, *self.shape("mud", x, y))
                elif c == "=":
                    self.set(x, y, *((self.patch(x, y), ".") if seam else self.shape("path", x, y)))
                elif c == ";":
                    self.set(x, y, *((TALL, "G") if seam else self.shape("barley", x, y)))
                elif c == "#":
                    assert not seam, (x, y, "rock in a seam column")
                    k = self.key("crag", x, y)
                    if k == "1|11111111" and hsh(x, y, 41) < 34:
                        name = ("crack", "boulders", "scrub_rock", "tuft")[hsh(x, y, 5) % 4]
                        self.set(x, y, *self.cat.named("rock_bits", name))
                        self.shapes_used["crag"].add(k)
                    else:
                        self.set(x, y, *self.shape("crag", x, y))
                elif c == "b":
                    assert not seam
                    self.set(x, y, *self.cat.named("rock_bits", "bush" if hsh(x, y, 3) % 2 else "bush_b"))
                elif c == "o":
                    self.set(x, y, BOULDER, "X")
                elif c in "@DG":
                    self.set(x, y, GRASS, ".")
                else:
                    raise ValueError(f"unknown ground {c!r} at {x},{y}")
        self.decorate()

    def decorate(self, rate=6):
        for y in range(H):
            for x in range(W):
                if self.mt[y][x] != GRASS or (x, y) in self.stamped or self.ch[y][x] != ".":
                    continue
                if (x, y) in self.no_decor:
                    continue
                if hsh(x, y, 77) < rate:
                    self.set(x, y, ANEMONE, ".")

    def set(self, x, y, mid, walk):
        self.mt[y][x] = mid
        self.walkc[y][x] = walk

    # --- output --------------------------------------------------------------
    def check_seams(self):
        errs = []
        for y in range(H):
            for x in list(SEAM_W) + list(SEAM_E):
                if self.mt[y][x] >= 0x200:
                    errs.append(f"({x},{y}): 0x{self.mt[y][x]:03X} in an aethos-only seam column")
        return errs

    def collision(self, x, y):
        if (x, y) in self.force_open:
            return 0
        if (x, y) in self.force_block:
            return 1
        return 1 if self.walkc[y][x] in ("X", "J") else 0

    def blocks(self):
        b = np.zeros((H, W), np.uint16)
        for y in range(H):
            for x in range(W):
                m = self.mt[y][x]
                assert m is not None, (x, y)
                if (x, y) in self.water_cells:
                    b[y, x] = m | (1 << 12)          # surfable water: elevation 1, no collision
                elif self.collision(x, y):
                    b[y, x] = m | (1 << 10)
                else:
                    b[y, x] = m | (3 << 12)
        return b


def ledge_cells(m):
    """Cells whose metatile jumps east, for the reachability check."""
    out = set()
    for key, name in (("rock_bits", "ledge_e"), ("rock_bits", "ledge_e_foot")):
        mid, _ = m.cat.named(key, name)
        for y in range(H):
            for x in range(W):
                if m.mt[y][x] == mid:
                    out.add((x, y))
    return out


# ===========================================================================
# Route 8, the Kopais shore
# ===========================================================================

# The ground, row by row as runs ("L5" is five lake cells), x from 0 (Lebadeia) to 63
# (Thyrsa). Rows 0-8: the lake, Gla, the marsh and the reed beds; rows 9-16: the road
# and its three forced reed bands (band 3 x 8-11, band 2 x 27-29, band 1 x 46-48), the
# narrows (x 12-17) and the dike (x 30-38); rows 17-25: Phikion's foot, its scrub
# and rock, the Treasury (x 16-20), Onchestos, the goat path up the spur, the
# Sphinx's ledge (x 23-25, rows 24-25) and the way down east along the gully.
GRID = """
.8 ~1 L11 L34 ~2 .8
.8 ~1 L5 G6 L34 ~2 .8
.8 ~1 L5 G6 L34 ~2 .8
.8 ~1 L3 ~1 L1 G6 L34 ~2 .8
.8 ~5 L1 G6 L2 ~32 ~2 .8
.8 ~5 L8 ~5 ,2 ~13 ,2 ~13 .8
.8 ~1 m3 .1 ~10 ,2 ~13 ,2 ~6 ,3 ~2 ,1 ~4 .8
.8 ~1 m1 .3 ~10 ,1 ~22 ,3 ~2 ,3 ~2 .8
.8 ~1 .4 ~14 ,4 ~8 ,7 ,3 ,5 ~2 .8
.8 ,4 ,1 ,2 ,1 ~2 ,9 ,4 ~8 ,7 ,3 ,5 ,1 .1 .8
.8 ,8 ~2 ,9 ,4 ~8 ,7 ,3 @2 ,4 .1 .8
.8 ,8 ~2 ,9 ,4 ~8 .2 @2 .3 ,3 @2 ,4 .1 .8
=8 ,4 =4 ~2 ,9 ,3 D9 .2 @2 .3 ,3 .3 ,2 .2 .8
=8 ,4 =5 ~1 ,5 .1 @1 .1 ,1 ,3 D9 =7 ,3 .6 .1 .8
.8 #4 #1 .1 .1 =2 ,1 ,4 .1 .1 @1 .1 .1 ,3 D9 =7 ,3 =7 =8
.8 #4 #3 =2 =10 ,3 D9 .3 .4 ,3 =7 =8
.8 F4 #3 =2 =10 ,3 D9 .3 F2 #2 ,3 F7 .8
.8 F4 #3 #1 @5 ;1 @1 .1 ;2 #5 ~7 #1 .3 F1 #3 #3 F7 .8
.8 F4 #4 @5 ;1 @1 @1 ;2 #5 ~7 #1 .1 ;1 .1 F3 #2 F9 .8
.8 F4 #4 @5 @1 .1 .1 ;2 ;1 #4 ~7 #1 .1 ;1 .1 F14 .8
.8 F4 F4 @5 #3 ;2 ;1 #4 #8 ;1 .2 F14 .8
.8 F4 F4 @5 #2 ;1 ;2 #4 #9 .3 F14 .8
.8 F4 F4 @5 ;2 .1 .2 .4 @1 .3 @1 .3 @1 .3 F14 .8
.8 F4 F4 .4 ;2 .2 .2 .4 @1 .3 @1 .3 @1 .3 F14 .8
.8 F4 F4 F6 .1 @3 .1 #15 F14 .8
.8 F4 F4 F6 F1 @3 F1 #15 F14 .8
"""

# rock outcrops in the scrub (variety, and walls where the scrub alone would read thin)
OUTCROPS = [(42, 22, 55, 25), (8, 22, 12, 25), (48, 20, 52, 21), (13, 24, 21, 25)]


def runs(text, width):
    rows = []
    for line in text.strip().splitlines():
        row = "".join(tok[0] * int(tok[1:]) for tok in line.split())
        assert len(row) == width, (len(row), line)
        rows.append(row)
    return rows


def ground(m):
    rows = runs(GRID, W)
    assert len(rows) == H
    for y, r in enumerate(rows):
        m.ch[y] = list(r)
    for (x0, y0, x1, y1) in OUTCROPS:
        m.rect(x0, y0, x1, y1, "#")


def woods(m):
    """Fill 'F' with Phikion's scrub woodland: olives and stone pines in column
    pairs (every other pair a row lower, so they don't stand in ranks), olives
    stacked crown over trunk, maquis bushes in the gaps. All of it blocks."""
    F = lambda x, y: m.at(x, y) == "F" and (x, y) not in m.stamped
    done = set()
    for x in range(0, W - 1, 2):
        y = 0
        while y < H:
            if not (F(x, y) and F(x + 1, y)):
                y += 1
                continue
            y0 = y
            while F(x, y) and F(x + 1, y):
                y += 1
            y1 = y - 1
            start = y0 + (hsh(x, y0, 23) % 2 if y1 - y0 >= 2 else 0)
            yy = start
            prev_olive = None
            trees = []
            while yy + 1 <= y1:
                kind = "olive" if hsh(x, yy, 19) < 55 else "pine"
                trees.append((yy, kind))
                yy += 2
            for i, (ty, kind) in enumerate(trees):
                nxt = trees[i + 1] if i + 1 < len(trees) else None
                if kind == "pine":
                    m.pine(x, ty)
                else:
                    if i == 0 and m.at(x, ty - 1) in (".", ";") and (x, ty - 1) not in m.stamped \
                            and (x + 1, ty - 1) not in m.stamped and m.at(x + 1, ty - 1) in (".", ";"):
                        tip = (0x1C6, 0x1C7) if m.at(x, ty - 1) == ";" else OLIVE_TIP
                        m.put(x, ty - 1, tip[0], "T")
                        m.put(x + 1, ty - 1, tip[1], "T")
                    m.put(x, ty, OLIVE_TOP[0]); m.put(x + 1, ty, OLIVE_TOP[1])
                    stack = nxt is not None and nxt[1] == "olive" and nxt[0] == ty + 2
                    bot = OLIVE_STACK if stack else OLIVE_BOT
                    m.put(x, ty + 1, bot[0]); m.put(x + 1, ty + 1, bot[1])
            for yy in range(y0, y1 + 1):
                done.add((x, yy)); done.add((x + 1, yy))
    for y in range(H):
        for x in range(W):
            if m.at(x, y) == "F" and (x, y) not in m.stamped:
                m.put(x, y, *m.cat.named("rock_bits", "bush" if hsh(x, y, 3) % 2 else "bush_b"))
            if m.at(x, y) == "F":
                m.force_block.add((x, y))


def stamps(m):
    cat = m.cat
    # the Treasury of Minyas (its dromos at (18,22): the drum goes there)
    m.stamp("tholos", 16, 17)
    # the Sphinx's ledge
    m.stamp("sphinx", 23, 24, names={(0, 0): "NW", (1, 0): "N_feathers", (2, 0): "NE",
                                     (0, 1): "SW", (1, 1): "S_dig", (2, 1): "SE"})
    # the goat path's three east-facing ledges
    for x in (30, 34, 38):
        m.named("rock_bits", "ledge_e", x, 22)
        m.named("rock_bits", "ledge_e_foot", x, 23)
    # the dike: cope / top / top / kerb / face, ends at 30 and 38, the sluice at 34
    for x in range(30, 39):
        sfx = "_W" if x == 30 else ("_E" if x == 38 else "")
        sl = x == 34
        m.named("dike", "cope_sluice" if sl else "cope" + sfx, x, 12)
        m.named("dike", ("top_reeds" if x in (32, 37) else "top" + sfx), x, 13)
        m.named("dike", "top" + sfx, x, 14)
        m.named("dike", ("kerb_reeds" if x == 35 else "kerb" + sfx), x, 15)
        m.named("dike", "face_sluice" if sl else "face" + sfx, x, 16)
    m.named("markers", "dig_dike", 36, 14)                       # Alethea's second hole
    m.named("water_bits", "outflow", 34, 17)
    # the fishing jetty (the Super Repel at its end) and Ismenias's step
    m.named("jetty", "end", 36, 8)
    for y in (9, 10, 11):
        m.named("jetty", "mid", 36, y)
    m.named("jetty", "step", 33, 11)
    # the herm at the spur fork, the Onchestos marker
    m.named("markers", "herm_top", 24, 13)
    m.named("markers", "herm", 24, 14)
    m.named("markers", "post_top", 22, 17)
    m.named("markers", "post", 22, 18)
    m.named("markers", "dig", 23, 18)                            # the daily dig at Onchestos
    m.named("markers", "dig", 53, 13)                            # Alethea's first hole
    # Gla
    m.stamp("gla", 14, 1)
    # the eel-smoker's rack and fire, his traps, the fowler's hide and nets
    m.stamp("rack", 41, 11)
    m.named("traps", "trap", 40, 6)
    m.named("traps", "trap_b", 43, 5)
    m.stamp("hide", 49, 10)
    m.named("nets", "W", 52, 10)
    m.named("nets", "E", 53, 10)
    m.named("nest", "nest", 47, 7)
    m.named("nest", "nest", 29, 9)
    m.stamp("boat", 10, 6)
    for (x, y, n) in ((35, 6, "lilies"), (32, 9, "lilies_b"), (44, 5, "lilies"), (19, 7, "lilies_b"),
                      (51, 6, "lilies"), (11, 4, "lilies_b"), (24, 6, "lilies"), (38, 18, "lilies")):
        if m.at(x, y) == "~":
            m.named("water_bits", n, x, y)
    # aethos trees and signs
    m.olives = set()
    edge_walls(m)
    m.put(7, 11, STELE)                                          # the west sign
    m.put(55, 13, STELE)                                         # the east sign
    m.put(39, 12, STELE)                                         # the dike's sign
    m.put(22, 24, STELE)                                         # the Sphinx's sign
    m.put(16, 22, STELE)                                         # the Treasury's sign
    # the west end: pines and olives on the gorge's sides
    for (x, y, kind) in ((0, 1, "olive"), (3, 0, "pine"), (5, 3, "olive"), (1, 5, "pine"),
                         (4, 7, "olive"), (0, 9, "olive"), (2, 16, "pine"), (5, 18, "olive"),
                         (0, 20, "olive"), (3, 22, "pine"), (6, 22, "olive"), (1, 24, "olive")):
        tree(m, x, y, kind)
    for (x, y) in ((7, 2), (6, 9), (7, 20), (4, 13 + 3)):
        if m.at(x, y) == "." and (x, y) not in m.stamped and (x, y + 1) not in m.stamped:
            m.cypress(x, y)
    # the east end: Thyrsa's olive grove runs on down to the shore
    for (x, y, kind) in ((57, 0, "olive"), (60, 2, "olive"), (56, 5, "olive"), (62, 6, "olive"),
                         (59, 8, "olive"), (57, 11, "pine"), (61, 11, "olive"), (58, 17, "olive"),
                         (61, 19, "olive"), (56, 21, "olive"), (59, 23, "pine"), (62, 23, "olive")):
        tree(m, x, y, kind)
    for (x, y) in ((63, 0), (56, 2), (63, 9), (62, 16), (57, 19), (60, 21)):
        if m.at(x, y) == "." and (x, y) not in m.stamped and (x, y + 1) not in m.stamped:
            m.cypress(x, y)
    for (x, y) in ((61, 4), (58, 13), (63, 17), (56, 25), (60, 25)):
        if (x, y) not in m.stamped:
            m.put(x, y, BOULDER)


def edge_walls(m):
    """Close both edges except where the roads cross the seams (Lebadeia's road and
    verges, rows 11-14; Thyrsa's gate road, rows 14-15): a column of olives along each
    edge, stacked crown over trunk, with a boulder where a pair of rows is left over."""
    def column(x, rows):
        rows = list(rows)
        while len(rows) >= 2:
            pass_rows = rows[-2:]
            y = pass_rows[0]
            below = (x, y + 2) in m.olives
            m.put(x, y, OLIVE_TOP[0]); m.put(x + 1, y, OLIVE_TOP[1])
            bot = OLIVE_STACK if below else OLIVE_BOT
            m.put(x, y + 1, bot[0]); m.put(x + 1, y + 1, bot[1])
            m.olives.add((x, y))
            rows = rows[:-2]
        for y in rows:
            m.put(x, y, BOULDER)
            m.put(x + 1, y, BOULDER)
    column(0, range(0, WEST_ROAD - 1))                     # rows 0-10
    column(0, range(WEST_ROAD + 3, H))                     # rows 15-25
    column(62, range(0, EAST_ROAD))                        # rows 0-13
    column(62, range(EAST_ROAD + 2, H))                    # rows 16-25


def tree(m, x, y, kind):
    if any((xx, yy) in m.stamped or m.at(xx, yy) != "." for xx in (x, x + 1) for yy in (y, y + 1)):
        return
    if kind == "pine":
        m.pine(x, y)
    else:
        m.olive(x, y)
        m.olives.add((x, y))


def events(m):
    def note(n, x, y):
        return obj(P + "ALETHEA_NOTE", x, y, S8 + f"Note{n}", "MOVEMENT_TYPE_FACE_DOWN",
                   local_id=f"LOCALID_ROUTE8_NOTE_{n}")

    E = {
        "connections": [
            {"map": "MAP_LEBADEIA", "offset": 0, "direction": "left"},
            # Thyrsa's Neistan Gate: its west edge is open on rows 23-24, Route 8's east
            # edge on rows 14-15 (BUILD.md, q = 14). Thyrsa's side ("left", offset +9) is
            # added at integration.
            {"map": "MAP_THYRSA_CITY", "offset": EAST_ROAD - 23, "direction": "right"},
        ],
        "object_events": [
            # the east end: Gorgidas netting birds at the reed edge, Alethea's first note
            obj(P + "FOWLER", 52, 12, S8 + "Gorgidas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True,
                sight=3, local_id="LOCALID_ROUTE8_GORGIDAS"),
            note(1, 54, 13),
            # the eel-smoker at his fire (the rest point)
            obj(P + "ELDER_M", 43, 12, S8 + "EelSmoker", "MOVEMENT_TYPE_FACE_DOWN",
                local_id="LOCALID_ROUTE8_EEL_SMOKER"),
            # the dike: Ismenias on his fishing step, the note, the jetty's Super Repel
            obj(P + "FISHER", 33, 11, S8 + "Ismenias", "MOVEMENT_TYPE_FACE_DOWN", trainer=True,
                sight=4, local_id="LOCALID_ROUTE8_ISMENIAS"),
            note(2, 35, 14),
            item_ball(36, 8, "ITEM_SUPER_REPEL", "FLAG_ICHOR_ITEM_ROUTE8_SUPER_REPEL"),
            # the herm: the traveler with a pack (a theoxenia decoy)
            obj(P + "MAN", 25, 14, S8 + "Traveler", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_THEOXENIA_START+0x22", local_id="LOCALID_ROUTE8_TRAVELER"),
            # Timoxena in the reeds, facing the water; an Ultra Ball deep in them
            # Pelopidas, crouched in band 2 watching the reeds for birds: his sight
            # runs down through the band (the route standard's sixth trainer)
            obj(P + "FOWLER", 28, 10, S8 + "Pelopidas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True,
                sight=5, local_id="LOCALID_ROUTE8_PELOPIDAS"),
            # Megareus, a runner training at Onchestos's racing post, watching the road
            obj(P + "YOUTH_M", 21, 17, S8 + "Megareus", "MOVEMENT_TYPE_FACE_UP", trainer=True,
                sight=2, local_id="LOCALID_ROUTE8_MEGAREUS"),
            obj(P + "FOWLER_F", 21, 9, S8 + "Timoxena", "MOVEMENT_TYPE_FACE_UP", trainer=True,
                sight=2, local_id="LOCALID_ROUTE8_TIMOXENA"),
            item_ball(18, 10, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_ROUTE8_ULTRA_BALL"),
            # the spur: note 3 at the foot of the Sphinx's rocks; the Sphinx's ledge
            note(3, 23, 19),
            obj("OBJ_EVENT_GFX_SPECIES(ENIGMAW)", 24, 24, S8 + "Enigmaw", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_TEMP_11", local_id="LOCALID_ROUTE8_ENIGMAW"),
            item_ball(25, 25, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_ROUTE8_HYPER_POTION"),
            # the Treasury of Minyas: the column drum in the dromos, the TM inside
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 18, 22, "EventScript_StrengthBoulder",
                "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_ROUTE8_DRUM"),
            # ICHOR_STUB_TMS: TM Ancient Power isn't numbered yet; TM Rock Tomb stands in
            item_ball(17, 19, "ITEM_TM_ROCK_TOMB", "FLAG_ICHOR_ITEM_ROUTE8_TM_ANCIENT_POWER"),
            # the narrows: Perses at the foot of the rock wall
            obj(P + "YOUTH_M", 13, 14, S8 + "Perses", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True,
                sight=3, local_id="LOCALID_ROUTE8_PERSES"),
            # the west shore: the reed-boat boy, Euphrosyne cutting reeds, note 4
            obj(P + "KID_M", 10, 6, S8 + "ReedBoatBoy", "MOVEMENT_TYPE_FACE_UP",
                local_id="LOCALID_ROUTE8_BOY"),
            obj(P + "HARVESTER", 9, 8, S8 + "Euphrosyne", "MOVEMENT_TYPE_FACE_LEFT", trainer=True,
                sight=1, local_id="LOCALID_ROUTE8_EUPHROSYNE"),
            note(4, 12, 6),
            item_ball(12, 8, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_ROUTE8_FULL_HEAL"),
            # Gla (Poseidon's Conch): the Revive on its shore
            item_ball(17, 4, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_ROUTE8_REVIVE"),
            # the west sign: note 5
            note(5, 6, 11),
        ],
        "warp_events": [],
        "coord_events": [],
        "bg_events": [
            sign(55, 13, S8 + "SignEast"),
            sign(53, 13, S8 + "DigEast"),
            sign(39, 12, S8 + "SignDike"),
            sign(36, 14, S8 + "DigDike"),
            sign(24, 14, S8 + "GreatHerm", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(22, 18, S8 + "SignOnchestos"),
            sign(23, 18, S8 + "DigOnchestos"),
            sign(16, 22, S8 + "SignTomb"),
            sign(19, 19, S8 + "DigTreasury"),
            sign(22, 24, S8 + "SignSphinx"),
            sign(24, 25, S8 + "DigSphinx"),
            sign(17, 2, S8 + "DigGla"),
            sign(7, 11, S8 + "SignWest"),
            hidden(42, 10, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_ROUTE8_HEART_SCALE"),
            hidden(30, 15, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ROUTE8_PEARL"),
            hidden(19, 18, "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_ROUTE8_NUGGET"),
            hidden(39, 23, "ITEM_BIG_MUSHROOM", "FLAG_ICHOR_HIDDEN_ROUTE8_BIG_MUSHROOM"),
        ],
    }
    m.dig_spots = [(53, 13), (36, 14), (23, 18), (19, 19), (24, 25), (17, 2)]
    return E


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
            "quantity": 1, "underfoot": False}


def border(m):
    """The border repeats as an olive grove: Phikion's slopes to the south, the far
    shore of the lake to the north."""
    return [OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_STACK[0], OLIVE_STACK[1]]


# ===========================================================================
# Checks
# ===========================================================================

ENTRY = [(63, EAST_ROAD), (63, EAST_ROAD + 1)]
EXIT = [(0, WEST_ROAD), (0, WEST_ROAD + 1)]
UNREACHABLE_OK = {(17, 4), (17, 2)}            # Gla: the Revive and the dig (the Conch)


def reach(m, starts, blocked=()):
    """Cells reachable on foot (ledges hop east), skipping `blocked`."""
    from collections import deque
    ledges = ledge_cells(m)
    blocked = set(blocked)
    ok = lambda x, y: 0 <= x < W and 0 <= y < H and not m.collision(x, y) and \
        (x, y) not in m.water_cells and (x, y) not in blocked
    seen = set(s for s in starts if ok(*s))
    dq = deque(seen)
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in ledges:
                if dx == 1:
                    nx += 1
                else:
                    continue
            if ok(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                dq.append((nx, ny))
    return seen


def check(m, E):
    people = {(o["x"], o["y"]) for o in E["object_events"]}
    drum = {(18, 22)}
    seen = reach(m, ENTRY, blocked=people - drum)
    bad = []
    targets = [(o["x"], o["y"], o["script"].split("_")[-1]) for o in E["object_events"]]
    targets += [(b["x"], b["y"], b.get("script", b.get("item", "?")).split("_")[-1])
                for b in E["bg_events"]]
    for (x, y, what) in targets:
        near = {(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))}
        if not (near & seen) and (x, y) not in UNREACHABLE_OK:
            bad.append(f"{what}@{x},{y}")
    print(f"  {NAME}: {len(seen)} cells reachable" + (f"; OUT OF REACH: {', '.join(bad)}" if bad else ""))
    if not set(EXIT) & seen:
        print("  !! the west exit is not reachable from the east entry")
    # forced grass: each grass patch, removed, cuts the way west?
    grass = {(x, y) for y in range(H) for x in range(W) if m.walkc[y][x] == "G"}
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
    forced = []
    for part in parts:
        r = reach(m, ENTRY, blocked=(people - drum) | part)
        if not (set(EXIT) & r):
            xs = sorted({x for x, _ in part}); ys = sorted({y for _, y in part})
            forced.append(f"x {xs[0]}-{xs[-1]}, y {ys[0]}-{ys[-1]} ({len(part)} cells)")
    print(f"  {NAME}: forced grass bands: {'; '.join(forced) if forced else 'NONE'}")
    total = len(grass)
    print(f"  {NAME}: {total} grass cells ({sum(1 for c in grass if m.ch[c[1]][c[0]] == ',')} reeds)")
    # trainers' sight lines across the road
    for o in E["object_events"]:
        if o["trainer_type"] != "TRAINER_TYPE_NORMAL":
            continue
        d = {"MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_UP": (0, -1),
             "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}[o["movement_type"]]
        n = int(o["trainer_sight_or_berry_tree_id"])
        cells = {(o["x"] + d[0] * k, o["y"] + d[1] * k) for k in range(1, n + 1)}
        r = reach(m, ENTRY, blocked=(people - drum) | cells)
        must = not (set(EXIT) & r)
        print(f"    {o['script'].split('_')[-1]}: sight {n} -> {'MANDATORY' if must else 'optional'}")
        # A trainer who spots the player walks up and stays there: wherever that is,
        # the player must still be able to go on west (and back east).
        home = (o["x"], o["y"])
        for k in range(1, n + 1):
            seen_at = (o["x"] + d[0] * k, o["y"] + d[1] * k)
            if seen_at not in seen:
                continue
            stop = (o["x"] + d[0] * (k - 1), o["y"] + d[1] * (k - 1))
            others = (people - drum - {home}) | {stop}
            fwd = reach(m, [seen_at], blocked=others)
            if not (set(EXIT) & fwd) or not (set(ENTRY) & fwd):
                print(f"    !! {o['script'].split('_')[-1]} standing at {stop} cuts the road for a "
                      f"player seen at {seen_at}")


# ===========================================================================

def build(shapes_only=False, tag=""):
    m = Map()
    ground(m)
    m.olives = set()
    stamps(m)
    woods(m)
    E = events(m)
    m.autotile()
    if shapes_only:
        data = {k: sorted(v) for k, v in m.shapes_used.items()}
        SHAPES.write_text(json.dumps(data, indent=1) + "\n")
        print({k: len(v) for k, v in data.items()}, "->", SHAPES.relative_to(ROOT))
        return m, E
    if m.missing:
        print(f"{len(m.missing)} shape cells drawn with stand-ins: run --shapes, rebuild the art")
    errs = m.check_seams()
    if errs:
        sys.exit("seam errors:\n  " + "\n  ".join(errs[:20]))
    bd = border(m)
    KL.write_layout(LAYOUT, NAME, m, bd)
    KL.write_events(NAME, E, MUSIC, {"weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_ROUTE",
                                      "show_map_name": True, "battle_scene": "MAP_BATTLE_SCENE_NORMAL"})
    views = [(60, 14), (52, 14), (47, 13), (42, 13), (36, 13), (33, 9), (28, 15), (24, 15),
             (20, 16), (18, 20), (24, 21), (32, 22), (40, 18), (15, 13), (10, 12), (10, 7), (3, 12)]
    KL.render(m, E, bd, views, tag)
    IMG.mkdir(parents=True, exist_ok=True)
    shutil.copy2(KL.RENDER / f"{NAME}{tag}.png", IMG / f"{NAME}.png")
    print(f"{NAME}: {W}x{H} -> {(IMG / f'{NAME}.png').relative_to(ROOT)}")
    check(m, E)
    return m, E


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    build(args.shapes, args.tag)


if __name__ == "__main__":
    main()
