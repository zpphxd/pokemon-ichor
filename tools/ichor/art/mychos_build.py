#!/usr/bin/env python3
"""Draw, compile and catalog the Labyrinth's heart: gTileset_Mychos and gTileset_Astra.

design/LABYRINTH_MAZE.md §4: the deeper you go, the more the cave wins. The heart
(Rings V-VII and the rooms below them) is built into karst caves, so its two
secondaries carry the house's masonry *and* a natural cave kit:

- **mychos** ("the innermost part of a house"): Ring V (the Hunt: the lake, the
  skylight pools, the cracked walls, the bell), Ring VI (the Titans' forge in its
  magma cavern, the Hall of Dials, the archive, the vault, the Mistress's shrine).
- **astra** ("the stars"): Ring VII (the Choros under its natural dome, the mirrors'
  beam, the dancing floor), the Starry Chamber (crystal stars in a cave ceiling),
  and the Icarus Shaft (a natural chimney to the sky).

Both start from world-act3's mychos art (tools/ichor/art/mychos_base/: the source
sheets and the piece catalog, kept here so this builder needs nothing else) and
add, from tools/ichor/art/cave_dark_kit.py, Ichor's cave kit (rock in 3/4 view with
rims, flowstone faces, cave floor, still water) recolored into the Labyrinth's own
stone and night palettes, plus the pieces drawn here: Ariadne's thread on the cave
floor, sunlit skylight pools, stalagmites and columns, dripstone faces, rubble,
the cracked wall, chasms, magma, a waterfall, a flowstone climb, holes, crystals,
the bronze bell and the chimney's sky.

Every 8x8 tile draws from one of the seven palettes world-act3 planned
(mychos_base/06.pal-12.pal); the build checks it and compiles each tileset with
Porytiles against an empty stand-in primary (as cave_dark_build.py does), then
writes data/tilesets/secondary/<name>/porytiles_{src,bin}, the sheets in
design/phase4/img/, and tools/ichor/maps/mychos_tiles.py, the catalog map builders
read.

Usage: /usr/bin/python3 tools/ichor/art/mychos_build.py [--no-compile]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import cave_dark_kit as kit  # noqa: E402
import cave_dark_lib as clib  # noqa: E402

BASE = HERE / "mychos_base"
TILE_LIMIT = 504
COLS = 8

# --------------------------------------------------------------------------
# Palettes: world-act3's seven groups, read from the compiled base
# --------------------------------------------------------------------------


def read_pal(path):
    lines = path.read_text().split("\n")[3:]
    out = []
    for ln in lines:
        if ln.strip():
            out.append(tuple(int(v) for v in ln.split()))
    return out


PAL_ROLE = {"06": "bronze", "07": "fire", "08": "fresco", "09": "minoan", "10": "stone",
            "11": "night", "12": "timber"}
PALS = {}
for _n, _role in PAL_ROLE.items():
    cols = list(dict.fromkeys(c for c in read_pal(BASE / f"{_n}.pal")[1:] if c != (0, 0, 0)))
    PALS[_role] = cols

# The colors this builder paints with, by name: every one is in exactly one group's
# palette, so a tile painted from one name family fits one palette.
S = {  # stone: the house's limestone ramp, its thread reds and its two lights
    "lk": (24, 16, 32), "ls1": (48, 40, 56), "ls2": (72, 64, 80), "ls3": (104, 96, 104),
    "ls4": (136, 128, 128), "ls5": (168, 160, 152), "ls6": (200, 192, 176),
    "lt0": (120, 40, 40), "lt1": (192, 40, 40), "lt2": (240, 112, 96),
    "lj": (152, 120, 112), "lw1": (232, 200, 144), "ld0": (160, 176, 192), "ld1": (216, 224, 232),
}
N = {  # night: the starry pool, water, crystals, sky
    "nk": (8, 8, 24), "nn0": (16, 24, 56), "nn1": (32, 48, 96), "nn2": (56, 80, 144),
    "nn3": (96, 128, 192), "ns0": (248, 248, 248), "ns1": (248, 232, 160),
    "nm0": (120, 128, 152), "nm1": (168, 176, 200), "nm2": (216, 224, 240),
    "np0": (16, 40, 56), "np1": (32, 72, 88), "ng0": (184, 136, 56), "ng1": (232, 200, 104),
}
F = {  # fire: magma and the forge's glow
    "fk": (32, 24, 24), "fg1": (48, 40, 48), "fg2": (88, 80, 88), "fg3": (136, 128, 128),
    "fm0": (96, 24, 16), "fm1": (176, 48, 24), "fm2": (232, 104, 32), "fm3": (248, 168, 48),
    "fm4": (248, 224, 120), "fm5": (248, 248, 224), "fb1": (120, 72, 32), "fb2": (168, 112, 48),
    "fb3": (216, 168, 80), "fc1": (144, 72, 40), "fc2": (200, 128, 80),
}
B = {  # bronze: the bell, the rope's pegs
    "bk": (32, 24, 24), "bv0": (40, 32, 56), "bv1": (48, 96, 88), "bz0": (72, 40, 24),
    "bz1": (120, 72, 32), "bz2": (168, 112, 48), "bz3": (216, 168, 80), "bz4": (248, 176, 48),
    "bg": (200, 176, 128), "bw": (248, 248, 232), "bl": (248, 224, 144), "bs": (56, 56, 72),
    "bs2": (80, 72, 104), "bs3": (104, 104, 120), "bt": (96, 152, 128),
}
T = {  # timber: the rope
    "tk": (32, 24, 24), "tw0": (64, 40, 24), "tw1": (112, 72, 40), "tw2": (160, 112, 64),
    "tw3": (208, 160, 104), "tp1": (192, 168, 120), "tp2": (216, 200, 152), "tq": (176, 152, 104),
}
COL = {}
for _fam in (S, N, F, B, T):
    COL.update(_fam)
for _role, _set in (("stone", S), ("night", N), ("fire", F), ("bronze", B), ("timber", T)):
    for _nm, _c in _set.items():
        assert _c in PALS[_role], (_role, _nm, _c)

# The cave kit's colors (cave_dark_lib.C names) mapped into the Labyrinth's.
ROCK_MAP = {"k0": "lk", "k1": "ls1", "k2": "ls2", "k3": "ls3", "k4": "ls3", "k5": "ls4",
            "k6": "ls5", "k7": "ls6", "k8": "ld1", "tl1": "ls2", "tl2": "ld0", "ch1": "ls3",
            "ch2": "ls5", "wh": "ld1", "f3": "ls3"}
FLOOR_MAP = {"k0": "lk", "f0": "lk", "f1": "ls1", "f2": "ls2", "f3": "ls3", "f4": "lj",
             "f5": "ls5", "f6": "ls6", "pd1": "ls2", "pd2": "ld0", "mn1": "ld0", "mn2": "ld1",
             "dl": "lw1", "ch1": "ls3", "ch2": "ls5"}
WATER_MAP = {"k0": "nk", "w0": "nn0", "w1": "np0", "w2": "np1", "w3": "nn2", "w4": "nn3",
             "w5": "nm2", "f1": "nn0", "f2": "nm0", "f3": "nm0", "f4": "nm1", "al1": "np1",
             "al2": "nn2", "an": "nm1", "sf": "nm2"}
MAGMA_MAP = {"k0": "fk", "w0": "fm0", "w1": "fm1", "w2": "fm2", "w3": "fm3", "w4": "fm4",
             "w5": "fm5", "f1": "fg1", "f2": "fg2", "f3": "fg3", "f4": "fg3", "al1": "fm1",
             "al2": "fm2", "an": "fm2", "sf": "fm3"}
PIT_MAP = {"k0": "lk", "w0": "lk", "w1": "lk", "w2": "lk", "w3": "ls1", "w4": "ls1",
           "w5": "ls2", "f1": "lk", "f2": "ls1", "f3": "ls2", "f4": "ls3", "al1": "lk",
           "al2": "lk", "an": "lk", "sf": "lk"}


def remap(a, table):
    """Recolor an RGBA array from cave_dark's palette into ours."""
    out = a.copy()
    m = a[..., 3] > 0
    if not m.any():
        return out
    for name, target in table.items():
        src = clib.C[name]
        hit = m & (a[..., 0] == src[0]) & (a[..., 1] == src[1]) & (a[..., 2] == src[2])
        out[hit, :3] = COL[target]
    return out


# --------------------------------------------------------------------------
# Cells and pieces
# --------------------------------------------------------------------------

class Piece:
    """w x h metatiles: three RGBA layers, walk codes (X . ~ D ^), behaviors, part names."""

    def __init__(self, key, w, h, walk=None, section="new", names=None):
        self.key, self.w, self.h, self.section = key, w, h, section
        self.layers = {n: np.zeros((h * 16, w * 16, 4), np.uint8) for n in ("bottom", "middle", "top")}
        self.walk = walk or ["X" * w] * h
        self.names = names or {}
        self.behaviors = {}
        self.ids = None
        self.origin = None
        self.meta = {}

    def put(self, cx, cy, layers):
        for n, a in layers.items():
            if a is not None:
                self.layers[n][cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = a

    def cell(self, cx, cy, layer="bottom"):
        return self.layers[layer][cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16].copy()


def one(key, layers, walk=".", mb=None, section="new"):
    p = Piece(key, 1, 1, [walk], section)
    p.put(0, 0, layers)
    if mb:
        p.behaviors[(0, 0)] = mb
    return p


class Canvas:
    """A 16x16 (or larger) RGBA layer painted by color name."""

    def __init__(self, w=16, h=16, base=None):
        self.a = np.zeros((h, w, 4), np.uint8) if base is None else base.copy()
        self.h, self.w = self.a.shape[:2]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            if c is None:
                self.a[y, x] = 0
            else:
                self.a[y, x, :3] = COL[c]
                self.a[y, x, 3] = 255

    def get(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h) or self.a[y, x, 3] == 0:
            return None
        rgb = tuple(int(v) for v in self.a[y, x, :3])
        for n, c in COL.items():
            if c == rgb:
                return n
        return None

    def blit(self, rows, legend, x=0, y=0, hflip=False):
        for j, row in enumerate(rows):
            if hflip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch in legend:
                    self.px(x + i, y + j, legend[ch])

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def ellipse(self, box, c):
        m = Image.new("1", (self.w, self.h), 0)
        ImageDraw.Draw(m).ellipse(box, fill=1)
        ys, xs = np.nonzero(np.array(m))
        for y, x in zip(ys, xs):
            self.px(x, y, c)


def hsh(*args):
    return clib.h(*args)


# --------------------------------------------------------------------------
# The base: world-act3's pieces, cut from the old sheets
# --------------------------------------------------------------------------

BASE_PIECES = json.loads((BASE / "pieces.json").read_text())
BASE_SHEETS = {n: np.array(Image.open(BASE / f"{n}.png").convert("RGBA")) for n in ("bottom", "middle", "top")}
BASE_MB = {}
for _ln in (BASE / "attributes.csv").read_text().split("\n")[1:]:
    if _ln.strip():
        _i, _mb = _ln.split(",")
        BASE_MB[int(_i)] = _mb


def base_cell(mid):
    i = mid - 0x200
    r, c = divmod(i, 8)
    return {n: s[r * 16:r * 16 + 16, c * 16:c * 16 + 16].copy() for n, s in BASE_SHEETS.items()}


def base_piece(key):
    b = BASE_PIECES[key]
    p = Piece(key, b["w"], b["h"], list(b["walk"]), "base:" + b["section"], dict(b["names"]))
    for cy, row in enumerate(b["ids"]):
        for cx, mid in enumerate(row):
            p.put(cx, cy, base_cell(mid))
            if mid - 0x200 in BASE_MB:
                p.behaviors[(cx, cy)] = BASE_MB[mid - 0x200]
            if p.walk[cy][cx] == "D":
                p.behaviors[(cx, cy)] = "MB_NON_ANIMATED_DOOR"
    for k in ("twin_of", "runs"):
        if k in b:
            p.meta[k] = b[k]
    return p


def base_floor_void():
    p = Piece("void", 1, 1, ["X"], "house")
    p.put(0, 0, base_cell(0x200))
    return p


# --------------------------------------------------------------------------
# The cave kit, recolored
# --------------------------------------------------------------------------

KIT_FLUTES = ("A", "C", "end", "inner")   # B and D fall back to A and C (cave_dark_kit.fallbacks)


def kit_pieces(with_water=True, with_magma=False, with_pit=False):
    cells = kit.kit_cells()
    out = []
    for key, (layers, walk, mb) in sorted(cells.items()):
        kind = key.split("|")[0]
        a = layers["bottom"]
        if kind in ("T",):
            out.append(one("cave:" + key, {"bottom": remap(a, ROCK_MAP)}, "X", section="cave"))
        elif kind in ("ft", "fb"):
            _, l, r = key.split("|")
            if l not in KIT_FLUTES or r not in KIT_FLUTES:
                continue
            out.append(one("cave:" + key, {"bottom": remap(a, ROCK_MAP)}, "X", section="cave"))
        elif kind == "water":
            if with_water:
                out.append(one("cave:" + key, {"bottom": remap(a, WATER_MAP)}, "~", "MB_DEEP_WATER",
                               section="water"))
            if with_magma:
                out.append(one("magma:" + key, {"bottom": remap(a, MAGMA_MAP)}, "X", section="magma"))
            if with_pit:
                out.append(one("pit:" + key, {"bottom": remap(a, PIT_MAP)}, "X", section="pit"))
    return out


def cave_floor_cell():
    """The cave floor, threadable: cave_dark's plain floor, no contact shadows
    (every walkable cell of a threaded ring must be a registered floor)."""
    return remap(kit.floor_cell(False, False, False), FLOOR_MAP)


def sun_floor_cell():
    """A skylight pool's sunlit floor: the cave floor washed with warm daylight."""
    a = kit.floor_cell(False, False, False)
    table = {"k0": "ls3", "f0": "ls3", "f1": "lj", "f2": "lj", "f3": "lw1", "f4": "ld1",
             "f5": "ld1", "f6": "ld1"}
    return remap(a, table)


# --------------------------------------------------------------------------
# Ariadne's thread on the new floors
# --------------------------------------------------------------------------

THREAD_ORDER = ("h", "v", "ne", "nw", "se", "sw", "cap_n", "cap_s", "cap_w", "cap_e")
THREAD_RED = {COL["lt0"], COL["lt1"], COL["lt2"]}


def thread_masks():
    """Each thread shape's pixels, cut from world-act3's dark_l twins: where the twin
    differs from the plain dark_l floor."""
    b = BASE_PIECES["thread"]
    names = b["names"]
    ids = b["ids"]
    plain = base_cell(ids[names["dark_l"][1]][names["dark_l"][0]])["bottom"]
    out = {}
    for shape in THREAD_ORDER:
        cx, cy = names["dark_l_" + shape]
        twin = base_cell(ids[cy][cx])["bottom"]
        diff = np.any(twin != plain, axis=2)
        out[shape] = (diff, twin)
    return out


def threaded(floor_key, cell, mb):
    """A floor and its ten thread twins, in the engine's order."""
    masks = thread_masks()
    p = Piece(floor_key, 8, 2, ["." * 8, "...XXXXX"], "thread")
    p.put(0, 0, {"bottom": cell})
    p.names[floor_key] = (0, 0)
    for i, shape in enumerate(THREAD_ORDER, start=1):
        m, twin = masks[shape]
        a = cell.copy()
        a[m] = twin[m]
        cx, cy = i % 8, i // 8
        p.put(cx, cy, {"bottom": a})
        p.names[f"{floor_key}_{shape}"] = (cx, cy)
    for cx, cy in [(c, r) for r in range(2) for c in range(8)]:
        if cy * 8 + cx <= 10:
            p.behaviors[(cx, cy)] = mb
    # the unused cells of the block: void
    for k in range(11, 16):
        p.put(k % 8, k // 8, base_cell(0x200))
    return p


# --------------------------------------------------------------------------
# New pieces, drawn here
# --------------------------------------------------------------------------

def stalagmite(variant=0):
    """A stalagmite on the cave floor (middle layer), rim-lit from the upper left."""
    c = Canvas()
    shapes = [
        ["      ..      ",
         "     .65.     ",
         "     .654.    ",
         "    .6543.    ",
         "    .65432.   ",
         "   .665432.   ",
         "   .6654322.  ",
         "  .66543322.  ",
         "  .665433222. ",
         " .6654333222. ",
         " .66543332221.",
         ".666543332221.",
         ".kkkkkkkkkkkk."],
        ["   .5.        ",
         "  .654.   .4. ",
         "  .654.  .542.",
         " .6543. .6532.",
         " .65432..6532.",
         " .654322.6532.",
         ".6654322.65322",
         ".6654322665432",
         ".6654332665432",
         ".66543326654322",
         ".665433366543221",
         ".kkkkkkkkkkkkkk."],
    ]
    rows = shapes[variant % len(shapes)]
    legend = {".": "lk", "k": "lk", "6": "ls6", "5": "ls5", "4": "ls4", "3": "ls3", "2": "ls2", "1": "ls1"}
    c.blit(rows, legend, 1, 16 - len(rows))
    # a soft shadow on the floor at its foot is part of the floor: skip (keeps it threadable)
    return c.a


def column_cells():
    """A dripstone column joining floor to ceiling, two cells tall (middle layer)."""
    c = Canvas(16, 32)
    rows = []
    widths = [12, 11, 10, 9, 8, 7, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7, 7, 8, 9, 10, 11, 12, 13, 14, 14, 14, 14]
    for y, w in enumerate(widths):
        x0 = 8 - (w + 1) // 2
        for x in range(w):
            t = x / max(1, w - 1)
            col = "ls6" if t < 0.18 else "ls5" if t < 0.4 else "ls4" if t < 0.6 else "ls3" if t < 0.8 else "ls2"
            c.px(x0 + x, y, col)
        c.px(x0 - 1, y, "lk")
        c.px(x0 + w, y, "lk")
        if y in (9, 15, 22):   # growth rings
            for x in range(w):
                if (x + y) % 3 == 0:
                    c.px(x0 + x, y, "ls2")
    for x in range(2, 15):
        c.px(x, 31, "lk")
    return c.a[:16], c.a[16:]


def drip_face(base):
    """A face with stalactites hanging from its rim (drawn into the bottom layer)."""
    c = Canvas(base=base)
    for x0, length in ((2, 5), (6, 3), (9, 6), (13, 4)):
        for y in range(length):
            w = max(1, 2 - y // 2)
            for dx in range(w):
                c.px(x0 + dx, 3 + y, "ls5" if dx == 0 else "ls3")
            c.px(x0 - 1, 3 + y, "lk")
            c.px(x0 + w, 3 + y, "ls1")
        c.px(x0, 3 + length, "ld0")   # a bead of water at the tip
    return c.a


def flowstone_face(base):
    """A face draped in flowstone: pale curtains running down it."""
    c = Canvas(base=base)
    for x0 in (3, 7, 12):
        for y in range(0, 16):
            sway = (y // 4) % 2
            c.px(x0 + sway, y, "ls6" if y % 5 else "ld1")
            c.px(x0 + sway + 1, y, "ls4")
            c.px(x0 + sway - 1, y, "ls2")
    return c.a


def rubble():
    """A heap of fallen ashlar on the cave floor: where the house's masonry gave way."""
    c = Canvas()
    blocks = [(1, 8, 6, 5), (6, 10, 6, 5), (9, 5, 5, 4), (3, 4, 5, 4), (11, 11, 4, 4)]
    for x, y, w, h in blocks:
        c.rect(x, y, w, h, "ls5")
        c.rect(x + 1, y + 1, w - 1, h - 1, "ls4")
        c.rect(x, y + h - 1, w, 1, "ls2")
        c.rect(x + w - 1, y, 1, h, "ls3")
        c.px(x, y, "ls6")
        for i in range(w):
            c.px(x + i, y - 1 if y > 0 else y, "lk") if c.get(x + i, y - 1) is None else None
    # mason's labrys mark on one block
    c.blit(["5.5", "555", "5.5"], {"5": "lj"}, 4, 9)
    return c.a


def cracked_face(base):
    """The house's wall face, split by a crack Asterion can widen (LABYRINTH §5.3)."""
    c = Canvas(base=base)
    pts = [(8, 0), (7, 2), (9, 4), (6, 6), (8, 8), (5, 10), (7, 12), (6, 15)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for s in range(steps + 1):
            x = round(x0 + (x1 - x0) * s / steps)
            y = round(y0 + (y1 - y0) * s / steps)
            c.px(x, y, "lk")
            c.px(x + 1, y, "ls5")
    for x, y in ((3, 4), (11, 9), (12, 5), (4, 12)):
        c.px(x, y, "lk")
        c.px(x + 1, y + 1, "lk")
    for x, y in ((2, 14), (10, 13), (13, 14)):   # grit at its foot
        c.px(x, y, "ls2")
    return c.a


def hole_cell(floor):
    """A hole in the cave floor, dropping to the ring below."""
    c = Canvas(base=floor)
    c.ellipse((1, 3, 14, 14), "lk")
    c.ellipse((2, 4, 13, 13), "lk")
    for x in range(3, 13):
        c.px(x, 4, "ls1")
    c.ellipse((4, 6, 11, 12), "lk")
    for x, y in ((1, 8), (14, 9), (5, 14), (11, 2)):
        c.px(x, y, "ls2")
    return c.a


def climb_face(base):
    """Flowstone with cut footholds and a knotted rope: a climb to the ring above
    (MB_NORTH_ARROW_WARP: put a warp on it)."""
    c = Canvas(base=base)
    for y in (2, 6, 10, 14):
        c.rect(5, y, 6, 2, "ls1")
        c.rect(5, y, 6, 1, "lk")
        c.rect(6, y + 1, 4, 1, "ls5")
    return c.a


def climb_rope():
    c = Canvas()
    for y in range(16):
        c.px(8, y, "tw2" if y % 4 else "tw3")
        c.px(9, y, "tw1")
        if y % 4 == 3:
            c.px(7, y, "tw1")
            c.px(10, y, "tw1")
    return c.a


def crystal(variant=0):
    """Glowing crystals, the Starry Chamber's stars (night palette, middle layer)."""
    c = Canvas()
    shards = [[(5, 15, 3, 9), (8, 15, 2, 12), (11, 15, 3, 7)],
              [(3, 15, 3, 7), (7, 15, 3, 11), (10, 15, 2, 6), (12, 15, 2, 4)]][variant % 2]
    for x, base_y, w, hgt in shards:
        for y in range(base_y - hgt, base_y + 1):
            t = (y - (base_y - hgt)) / hgt
            for dx in range(w):
                col = "ns0" if (dx == 0 and t < 0.4) else "nm2" if dx == 0 else "nn3" if t < 0.6 else "nn2"
                c.px(x + dx, y, col)
            c.px(x - 1, y, "nn0")
            c.px(x + w, y, "nn0")
        c.px(x, base_y - hgt - 1, "ns0")
    return c.a


def sparkles(seed):
    """Crystal stars set in the cave's rock (middle layer over solid rock)."""
    c = Canvas()
    rng = np.random.RandomState(seed)
    for _ in range(3):
        x, y = rng.randint(2, 14), rng.randint(2, 14)
        big = rng.rand() < 0.4
        c.px(x, y, "ns0")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.px(x + dx, y + dy, "nn3" if big else "nn2")
        if big:
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
                c.px(x + dx, y + dy, "nn1")
    return c.a


def bell():
    """Daedalus's bronze bell on its yoke (Page V: ring it and Asterion lies down)."""
    c = Canvas()
    c.blit(["kkkkkkkkkkkkkk",
            "k3333333333332k",
            " k1kkkkkkkk1k ",
            " k1k      k1k ",
            " k1k kkkk k1k ",
            " k1kk4433kk1k ",
            " k1k443321k1k ",
            " k1k443321k1k ",
            " k1k4433221k1k",
            " k1k44332211k ",
            " k1k443322211k",
            " k1kk4443322kk",
            " k1k kk3kkkk1k",
            " k1k  k2k  k1k",
            "kk1kk  k  kk1kk",
            "kkkkk     kkkkk"],
           {"k": "bk", "1": "bz1", "2": "bz2", "3": "bz3", "4": "bz4"}, 1, 0)
    return c.a


def waterfall_cell(row):
    """A waterfall, falling south (MB_WATERFALL): row 0 its lip, 1 the fall, 2 the foam."""
    c = Canvas()
    for y in range(16):
        for x in range(16):
            band = (x + (y if row != 1 else y * 2)) % 6
            col = "nn2" if band < 2 else "nn3" if band < 4 else "nm1"
            if row == 0 and y < 5:
                col = "np1" if y < 3 else "nn2"
            if row == 2 and y > 9:
                col = "nm2" if (x + y) % 3 else "ns0"
            c.px(x, y, col)
        if row == 1:
            c.px((y * 3) % 16, y, "nm2")
    return c.a


def sky_cell(row):
    """The chimney's sky, seen straight up the Icarus Shaft (night palette): dawn
    grading from deep blue to pale gold."""
    c = Canvas()
    ramp = ["nn0", "nn1", "nn2", "nn3", "nm1", "nm2", "ng1", "ns1"]
    for y in range(16):
        g = min(len(ramp) - 1, (row * 16 + y) // 8)
        for x in range(16):
            col = ramp[g]
            if (x * 7 + y * 3 + row) % 23 == 0 and g < 3:
                col = "ns0"
            c.px(x, y, col)
    return c.a


def beam_pool():
    """Sunlight falling through a skylight: a shaft seen on a wall face (overlay)."""
    c = Canvas()
    for y in range(16):
        for x in range(4 + y // 4, 12 - y // 4):
            if (x + y) % 2 == 0:
                c.px(x, y, "lw1")
    return c.a


# --------------------------------------------------------------------------
# The two tilesets
# --------------------------------------------------------------------------

def face_base(kind="ft"):
    return remap(kit.face_cell(kind, "A", "A"), ROCK_MAP)


def solid_rock():
    return remap(kit.mass_cell(False, False, False, ()), ROCK_MAP)


def house_face():
    """The house's corridor face_cc, the wall the crack runs through."""
    b = BASE_PIECES["walls"]
    cx, cy = b["names"]["face_cc"]
    return base_cell(b["ids"][cy][cx])["bottom"]


def common_new(floor_cell):
    """Cave pieces both tilesets use."""
    out = []
    cave = threaded("cave", floor_cell, "MB_CAVE")
    out.append(cave)
    f = Piece("formations", 8, 3, ["XXXXXXXX", "XXXXXXXX", "XX.XXXXX"], "formations")
    f.put(0, 0, {"bottom": floor_cell, "middle": stalagmite(0)})
    f.put(1, 0, {"bottom": floor_cell, "middle": stalagmite(1)})
    top, bot = column_cells()
    f.put(2, 0, {"bottom": floor_cell, "middle": top})
    f.put(2, 1, {"bottom": floor_cell, "middle": bot})
    f.put(3, 0, {"bottom": floor_cell, "middle": rubble()})
    f.put(4, 0, {"bottom": drip_face(face_base("ft"))})
    f.put(5, 0, {"bottom": drip_face(face_base("fb"))})
    f.put(6, 0, {"bottom": flowstone_face(face_base("ft"))})
    f.put(7, 0, {"bottom": flowstone_face(face_base("fb"))})
    f.put(0, 1, {"bottom": climb_face(face_base("ft"))})
    f.put(1, 1, {"bottom": climb_face(face_base("fb")), "middle": climb_rope()})
    f.put(3, 1, {"bottom": cracked_face(house_face())})
    f.put(4, 1, {"bottom": hole_cell(floor_cell)})
    f.put(5, 1, {"bottom": floor_cell, "middle": crystal(0)})
    f.put(6, 1, {"bottom": floor_cell, "middle": crystal(1)})
    f.put(7, 1, {"bottom": face_base("fb"), "middle": beam_pool()})
    f.put(0, 2, {"bottom": face_base("fb"), "middle": climb_rope()})
    f.put(1, 2, {"bottom": floor_cell, "middle": bell()})
    f.put(2, 2, {"bottom": floor_cell})          # spare: plain floor, unthreaded (never placed)
    for x in range(3, 8):
        f.put(x, 2, base_cell(0x200))
    f.names = {"mite_a": (0, 0), "mite_b": (1, 0), "column_top": (2, 0), "column_base": (2, 1),
               "rubble": (3, 0), "drip_ft": (4, 0), "drip_fb": (5, 0), "flow_ft": (6, 0),
               "flow_fb": (7, 0), "climb_top": (0, 1), "climb": (1, 1), "cracked": (3, 1),
               "hole": (4, 1), "crystal_a": (5, 1), "crystal_b": (6, 1), "sunshaft": (7, 1),
               "rope_low": (0, 2), "bell": (1, 2)}
    f.behaviors[(1, 1)] = "MB_NORTH_ARROW_WARP"
    f.behaviors[(4, 1)] = "MB_CAVE"
    f.walk = ["XXXXXXXX", "X^XX.XXX", "XXXXXXXX"]
    f.walk[1] = "X.XX.XXX"
    f.walk[0] = "XXXXXXXX"
    out.append(f)
    return out


def build_mychos():
    pieces = [base_floor_void()]
    for k in ("walls", "anchor", "anchor_odd", "stairs", "thread"):
        pieces.append(base_piece(k))
    floor = cave_floor_cell()
    pieces += common_new(floor)
    sun = threaded("sun", sun_floor_cell(), "MB_ICHOR_LIGHT_POOL")
    pieces.append(sun)
    wf = Piece("waterfall", 3, 1, ["~~~"], "water")
    for i in range(3):
        wf.put(i, 0, {"bottom": waterfall_cell(i)})
        wf.behaviors[(i, 0)] = "MB_WATERFALL" if i < 2 else "MB_DEEP_WATER"
    wf.names = {"lip": (0, 0), "fall": (1, 0), "foam": (2, 0)}
    pieces.append(wf)
    for k in ("anvil", "anvil_odd", "archive", "archive_desk", "archive_desk_odd", "banners", "dials",
              "doorways", "forge", "forge_kit", "forge_kit_odd", "fresco_v", "fresco_vi", "grates",
              "lamp_stand", "lamp_stand_odd", "shrine", "shrine_odd", "vault", "vault_odd"):
        pieces.append(base_piece(k))
    pieces += kit_pieces(with_water=True, with_magma=True, with_pit=True)
    return pieces


def build_astra():
    pieces = [base_floor_void()]
    for k in ("walls", "anchor", "anchor_odd", "stairs", "thread", "marble"):
        pieces.append(base_piece(k))
    floor = cave_floor_cell()
    pieces += common_new(floor)
    sky = Piece("sky", 4, 1, ["XXXX"], "sky")
    for i in range(4):
        sky.put(i, 0, {"bottom": sky_cell(i * 2)})
    sky.names = {"s0": (0, 0), "s1": (1, 0), "s2": (2, 0), "s3": (3, 0)}
    pieces.append(sky)
    stars = Piece("stars", 4, 1, ["XXXX"], "stars")
    rock = solid_rock()
    for i in range(4):
        stars.put(i, 0, {"bottom": rock, "middle": sparkles(17 + i)})
    stars.names = {"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (3, 0)}
    pieces.append(stars)
    for k in ("basin", "clock", "horns", "star_anvil", "beam", "dance", "fresco_faded", "fresco_v",
              "fresco_vi", "fresco_iv", "lamp_stand", "lamp_stand_odd"):
        pieces.append(base_piece(k))
    pieces += kit_pieces(with_water=True, with_magma=False, with_pit=True)
    return pieces


# --------------------------------------------------------------------------
# Validation, packing, output
# --------------------------------------------------------------------------

PAL_SETS = {role: set(cols) for role, cols in PALS.items()}


def tile_fits(t):
    m = t[..., 3] > 0
    if not m.any():
        return True
    cols = {tuple(int(v) for v in p) for p in t[m][:, :3]}
    return any(cols <= s for s in PAL_SETS.values())


def validate(pieces):
    bad = []
    keys = set()
    for p in pieces:
        if p.key in keys:
            bad.append(f"duplicate {p.key}")
        keys.add(p.key)
        for ln, a in p.layers.items():
            for ty in range(0, a.shape[0], 8):
                for tx in range(0, a.shape[1], 8):
                    if not tile_fits(a[ty:ty + 8, tx:tx + 8]):
                        cols = {tuple(int(v) for v in q) for q in a[ty:ty + 8, tx:tx + 8][a[ty:ty + 8, tx:tx + 8, 3] > 0][:, :3]}
                        bad.append(f"{p.key} {ln} tile ({tx // 8},{ty // 8}) fits no palette: {sorted(cols)[:6]}")
    return bad


def pack(pieces):
    """Shelf-pack in order: wide pieces first keep the sheet tidy."""
    row, col, shelf = 0, 0, 0
    for p in pieces:
        if col + p.w > COLS:
            row += shelf
            col, shelf = 0, 0
        p.ids = [[0x200 + (row + y) * COLS + col + x for x in range(p.w)] for y in range(p.h)]
        p.origin = (col, row)
        col += p.w
        shelf = max(shelf, p.h)
    return row + shelf


def estimate_tiles(pieces):
    seen = set()
    for p in pieces:
        for a in p.layers.values():
            for ty in range(0, a.shape[0], 8):
                for tx in range(0, a.shape[1], 8):
                    t = a[ty:ty + 8, tx:tx + 8]
                    if not t[..., 3].any():
                        continue
                    forms = [t, t[:, ::-1], t[::-1], t[::-1, ::-1]]
                    ks = [f.tobytes() for f in forms]
                    if not any(k in seen for k in ks):
                        seen.add(ks[0])
    return len(seen)


def write_src(pieces, rows, out):
    out.mkdir(parents=True, exist_ok=True)
    W, H = COLS * 16, rows * 16
    for ln in ("bottom", "middle", "top"):
        sheet = np.zeros((H, W, 4), np.uint8)
        if ln == "bottom":
            # unused cells: the void
            v = base_cell(0x200)["bottom"]
            for r in range(rows):
                for c in range(COLS):
                    sheet[r * 16:r * 16 + 16, c * 16:c * 16 + 16] = v
        for p in pieces:
            cx, cy = p.origin
            sheet[cy * 16:cy * 16 + p.h * 16, cx * 16:cx * 16 + p.w * 16] = p.layers[ln]
        Image.fromarray(sheet, "RGBA").save(out / f"{ln}.png")
    beh = {}
    for p in pieces:
        for (x, y), mb in p.behaviors.items():
            beh[p.ids[y][x] - 0x200] = mb
        for y, row in enumerate(p.walk):
            for x, ch in enumerate(row):
                if ch == "^":
                    beh[p.ids[y][x] - 0x200] = "MB_NORTH_ARROW_WARP"
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh) if beh[k] != "MB_NORMAL"]
    (out / "attributes.csv").write_text("\n".join(lines) + "\n")


def catalog(pieces):
    cat = {"pieces": {}, "kit": {}, "water": {}, "magma": {}, "pit": {}}
    for p in pieces:
        if ":" in p.key and p.key.split(":")[0] in ("cave", "magma", "pit"):
            fam, k = p.key.split(":", 1)
            table = {"cave": "kit", "magma": "magma", "pit": "pit"}[fam]
            if k.startswith("water|"):
                table = "water" if fam == "cave" else table
            cat[table][k] = p.ids[0][0]
            continue
        cat["pieces"][p.key] = {"w": p.w, "h": p.h, "ids": p.ids, "walk": p.walk,
                                "names": p.names, "section": p.section, **p.meta}
    return cat


# --- Porytiles ------------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"mychos_build: failed: {' '.join(map(str, cmd))}")
    return r


def hints_yaml():
    lines = ["  tiles:", "    sharing:", "      packing: biased", "      alignment: greedy",
             "  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for role, cols in PALS.items():
        lines.append(f"        - name: {role}")
        lines.append("          colors:")
        for r, g, b in cols:
            lines.append(f"            - [{r}, {g}, {b}]")
    return "\n".join(lines) + "\n"


def compile_tileset(name, sym, src):
    scratch = ROOT / f"build/{name}_porytiles"
    if scratch.exists():
        shutil.rmtree(scratch)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (scratch / "data/tilesets/primary").mkdir(parents=True)
    (scratch / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    stubname = f"gTileset_{name.capitalize()}Stub"
    run([pt, "create-tileset", "-C", str(scratch), stubname])
    stub = next((scratch / "data/tilesets/primary").iterdir()) / "porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), stubname])
    sec = scratch / "data/tilesets/secondary" / name
    cfg = scratch / "porytiles/tilesets" / sym
    mine = ROOT / "porytiles/tilesets" / sym
    ts_bin = ROOT / "data/tilesets/secondary" / name / "porytiles_bin"
    if (mine / "tileset-manifest.json").exists() and ts_bin.exists():
        # already registered in the copied headers: reuse its manifest instead of creating it
        cfg.mkdir(parents=True, exist_ok=True)
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            if (mine / f).exists():
                shutil.copy2(mine / f, cfg / f)
        shutil.copytree(ts_bin, sec / "porytiles_bin")
    else:
        (scratch / "data/layouts").mkdir(parents=True, exist_ok=True)
        (scratch / "data/layouts/layouts.json").write_text(
            '{"layouts_table_label": "gMapLayouts", "layouts": []}')
        cfg.mkdir(parents=True, exist_ok=True)
        (cfg / "config.yaml").write_text(
            f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stubname}]\n")
        run([pt, "create-tileset", "-C", str(scratch), "--secondary", sym])
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(src, sec / "porytiles_src")
    cfg.mkdir(parents=True, exist_ok=True)
    pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stubname}]\n"
    (cfg / "config.yaml").write_text(pairing + hints_yaml())
    r = run([pt, "compile-tileset", "-C", str(scratch), "--no-verify-checksums", sym])
    if (r.stdout + r.stderr).strip():
        print((r.stdout + r.stderr)[-1500:])
    ts = ROOT / "data/tilesets/secondary" / name
    if (ts / "porytiles_bin").exists():
        shutil.rmtree(ts / "porytiles_bin")
    shutil.copytree(sec / "porytiles_bin", ts / "porytiles_bin")
    mycfg = ROOT / "porytiles/tilesets" / sym
    mycfg.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        if (cfg / f).exists():
            shutil.copy2(cfg / f, mycfg / f)
    (mycfg / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {sym}, the Labyrinth's heart. Written by\n"
        "# tools/ichor/art/mychos_build.py, which compiles it against an empty stand-in primary\n"
        "# so it uses only its own tiles and palettes 6-12. Pair it with oikos.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Oikos]\n" + hints_yaml())
    gen = scratch / "include/porytiles_generated/tilesets" / name
    if gen.exists():
        dst = ROOT / "include/porytiles_generated/tilesets" / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(gen, dst)
    verify(ts)


def verify(ts):
    raw = np.fromfile(ts / "porytiles_bin/metatiles.bin", "<u2").reshape(-1, 8)
    bad = [(0x200 + i, hex(int(e))) for i, entries in enumerate(raw) for e in entries
           if not (int(e) & 0x3FF == 0 and int(e) >> 12 == 0)
           and (int(e) & 0x3FF < 512 or not (6 <= int(e) >> 12 <= 12))]
    if bad:
        sys.exit(f"mychos_build: entries outside the secondary's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(ts / "porytiles_bin/tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    if used > TILE_LIMIT:
        sys.exit(f"mychos_build: {ts.name}: {used} tiles, past {TILE_LIMIT}")
    print(f"{ts.name}: verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")


# --- Anims: keep the base's flame, forge and stars where their tiles are used -----------------

ANIM_USERS = {"flame": ("lamp_stand", "forge"), "forge": ("forge",), "stars": ("basin",)}


def copy_anims(pieces, src):
    keys = {p.key for p in pieces}
    dst = src / "anim"
    if dst.exists():
        shutil.rmtree(dst)
    manifest = json.loads((BASE / "anim/anim.json").read_text())
    keep = {}
    for name, users in ANIM_USERS.items():
        if any(u in keys for u in users):
            shutil.copytree(BASE / "anim" / name, dst / name)
            keep[name] = manifest[name]
    if keep:
        (dst / "anim.json").write_text(json.dumps(keep, indent=2) + "\n")
    return list(keep)


# --- Sheets for review ------------------------------------------------------------------------

def sheet_png(pieces, rows, path, scale=3):
    W, H = COLS * 16, rows * 16
    comp = np.zeros((H, W, 3), np.uint8)
    comp[:] = (255, 0, 255)
    for ln in ("bottom", "middle", "top"):
        for p in pieces:
            cx, cy = p.origin
            a = p.layers[ln]
            m = a[..., 3] > 0
            region = comp[cy * 16:cy * 16 + p.h * 16, cx * 16:cx * 16 + p.w * 16]
            region[m] = a[..., :3][m]
    im = Image.fromarray(comp).resize((W * scale, H * scale), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for r in range(rows):
        for c in range(COLS):
            d.text((c * 16 * scale + 2, r * 16 * scale + 1), f"{0x200 + r * 8 + c:X}", fill=(255, 255, 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def write_catalog_module(cats):
    out = ROOT / "tools/ichor/maps/mychos_tiles.py"
    body = json.dumps(cats, indent=None, sort_keys=True)
    out.write_text(
        '"""Metatile ids of the Labyrinth\'s heart: gTileset_Mychos and gTileset_Astra.\n\n'
        "Generated by tools/ichor/art/mychos_build.py; do not edit. CATALOG[name] has\n"
        "'pieces' {key: {w, h, ids, walk, names, section}}, and the cave kit's autotile\n"
        "tables: 'kit' (rock and faces, cave_dark_kit keys), 'water', 'magma', 'pit'.\n"
        "The map builder that reads it is tools/ichor/maps/labyrinth_heart.py.\n"
        '"""\nimport json\n\nCATALOG = json.loads(r\'\'\'' + body + "''')\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    cats = {}
    for name, sym, build in (("mychos", "gTileset_Mychos", build_mychos),
                             ("astra", "gTileset_Astra", build_astra)):
        pieces = build()
        bad = validate(pieces)
        if bad:
            print("\n".join(bad[:40]))
            sys.exit(f"mychos_build: {name}: {len(bad)} problems")
        rows = pack(pieces)
        assert rows * COLS <= 512, (name, rows)
        print(f"{name}: {sum(p.w * p.h for p in pieces)} metatiles in {rows} rows; "
              f"about {estimate_tiles(pieces)} tiles")
        src = ROOT / "data/tilesets/secondary" / name / "porytiles_src"
        if src.exists():
            shutil.rmtree(src)
        write_src(pieces, rows, src)
        anims = copy_anims(pieces, src)
        print(f"  anims: {anims}")
        sheet_png(pieces, rows, ROOT / f"design/phase4/img/{name}_sheet.png")
        cats[name] = catalog(pieces)
        if not args.no_compile:
            compile_tileset(name, sym, src)
    write_catalog_module(cats)


if __name__ == "__main__":
    main()
