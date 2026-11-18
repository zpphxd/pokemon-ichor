"""Shared toolkit for gTileset_Chion, the secondary of Olympus's snows (design/LEAGUE.md).

Chion (Greek: snow) serves the Ascent above the second floor: the Icefall's
ice caves and crystal grottos, the glacier, the snowfield above the cloud line
and the Pantheon's propylaia.

Its terrain kit is cave_dark's (tools/ichor/art/cave_dark_kit.py: rock with
depth, floor, lit floor, still water), recolored: the rock becomes blue ice,
the floor snow, the lit floor a sheet of slick ice (MB_ICE: the player
slides), the water a glacial tarn. A second wall style, "glacier", shares the
ice's tiles under a snow-topped palette, so the open-air cliffs carry snow on
top. Props (crystals, snow pines, the bronze plates and grates of the seals,
shrines, the cloud sea, the propylaia) are drawn in chion_props.py.

Like cave_dark it is self-contained: compiled against an empty stand-in
primary, so its metatiles use only its own tiles and palettes 6-12 and work
on any primary (the maps pair it with aethos).

Palette plan: seven groups, one per secondary palette, at most 15 colors each.
Every 8x8 tile of every layer draws from ONE group; validate() enforces it.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]

C = {
    # blue ice, deep to bright: the walls (cave_dark's k0-k8)
    "i0": (8, 16, 40), "i1": (16, 32, 64), "i2": (32, 56, 96), "i3": (56, 88, 136),
    "i4": (88, 128, 176), "i5": (128, 168, 208), "i6": (168, 200, 232), "i7": (208, 232, 248),
    "i8": (240, 248, 248),
    # meltwater streaks in the ice, frost glitter, rime
    "im": (64, 112, 144), "im2": (104, 160, 184), "fr1": (152, 192, 216), "fr2": (216, 240, 248),
    "ws": (232, 240, 240),
    # snow on the ground, shadow to sunlit (cave_dark's f0-f6)
    "s0": (88, 104, 144), "s1": (128, 144, 184), "s2": (184, 200, 224), "s3": (216, 224, 240),
    "s4": (232, 232, 248), "s5": (248, 248, 248), "s6": (200, 216, 232),
    # slick ice (the lit floor): a sheet you slide on; frozen puddles
    "ic1": (168, 216, 240), "ic2": (208, 240, 248), "ic3": (240, 248, 232),
    "ip1": (96, 152, 200), "ip2": (152, 200, 232),
    # the glacier's snow-topped walls (the ice's tiles under another palette)
    "t0": (64, 88, 136), "t1": (144, 176, 224), "t2": (168, 200, 240), "t3": (120, 152, 200),
    "t4": (200, 216, 240), "t5": (216, 232, 248), "t6": (240, 240, 248), "t7": (184, 208, 232),
    # glacial water
    "w0": (8, 24, 56), "w1": (16, 48, 88), "w2": (32, 80, 120), "w3": (56, 120, 152),
    "w4": (104, 168, 192), "w5": (176, 224, 232),
    # crystal: violet and cyan, a magenta heart; snow pines
    "c0": (24, 16, 56), "c1": (56, 40, 120), "c2": (96, 72, 184), "c3": (144, 120, 224),
    "c4": (200, 176, 248), "cy1": (32, 96, 136), "cy2": (64, 168, 200), "cy3": (128, 224, 240),
    "cyw": (248, 248, 240), "mg": (200, 96, 184),
    "g0": (16, 48, 40), "g1": (32, 80, 56), "g2": (64, 112, 72), "br": (80, 56, 40),
    # marble, gold, Olympian blue and red; bronze and fire
    "m0": (40, 40, 64), "m1": (112, 112, 136), "m2": (168, 168, 184), "m3": (208, 208, 216),
    "m4": (240, 232, 224), "au": (232, 184, 72), "au2": (168, 112, 40), "bl": (40, 64, 136),
    "rd": (168, 48, 40), "b0": (72, 48, 32), "b1": (120, 80, 48), "b2": (176, 128, 72),
    "fl1": (240, 112, 32), "fl2": (248, 208, 96), "dk": (16, 16, 24),
    # the cloud sea and the sky over it
    "cl0": (144, 160, 208), "cl1": (176, 192, 232), "cl2": (216, 224, 248), "cl3": (248, 248, 232),
    "sk1": (88, 144, 216), "sk2": (136, 184, 232), "sk3": (184, 216, 248), "sun": (248, 232, 160),
}

# cave_dark's kit colors -> Chion's, one table per kit family.
ROCK_MAP = {"k0": "i0", "k1": "i1", "k2": "i2", "k3": "i3", "k4": "i4", "k5": "i5", "k6": "i6",
            "k7": "i7", "k8": "i8", "tl1": "im", "tl2": "im2", "ch1": "fr1", "ch2": "fr2",
            "wh": "ws", "f3": "s3"}
SNOWTOP_MAP = {"k0": "t0", "k1": "t1", "k2": "t2", "k3": "t3", "k4": "t4", "k5": "t5", "k6": "t6",
               "k7": "t7"}
FLOOR_MAP = {"f0": "s0", "f1": "s1", "f2": "s2", "f3": "s3", "f4": "s4", "f5": "s5", "f6": "s6",
             "pd1": "ip1", "pd2": "ip2", "mn1": "ic1", "mn2": "ic2", "dl": "ic3", "ch1": "fr1",
             "ch2": "fr2", "k0": "i0"}
WATER_MAP = {"w0": "w0", "w1": "w1", "w2": "w2", "w3": "w3", "w4": "w4", "w5": "w5", "f1": "s1",
             "f2": "s2", "f3": "s3", "f4": "s4", "k0": "i0"}

GROUPS = {
    "rock": ["i0", "i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "im", "im2", "fr1", "fr2", "ws", "s3"],
    "snowtop": ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "i0", "i2", "i4", "i6", "s2", "s3", "s5"],
    "floor": ["i0", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "ip1", "ip2", "ic1", "ic2", "ic3", "fr1", "fr2"],
    "water": ["i0", "w0", "w1", "w2", "w3", "w4", "w5", "s1", "s2", "s3", "s4", "s5", "ic1", "ic2", "fr2"],
    "crystal": ["c0", "c1", "c2", "c3", "c4", "cy1", "cy2", "cy3", "cyw", "mg", "g0", "g1", "g2", "br", "s1"],
    "marble": ["dk", "m0", "m1", "m2", "m3", "m4", "au", "au2", "bl", "rd", "b0", "b1", "b2", "fl1", "fl2"],
    "sky": ["cl0", "cl1", "cl2", "cl3", "sk1", "sk2", "sk3", "sun", "s1", "s2", "s3", "s4", "s5", "i4", "i6"],
}

for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(_names)) == len(_names), _g
    for _n in _names:
        assert _n in C, _n
for _n, _c in C.items():
    assert all(v % 8 == 0 and 0 <= v <= 248 for v in _c), (_n, _c)
assert len({c for c in C.values()}) == len(C), "two names share a color"
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}
RGB2NAME = {c: n for n, c in C.items()}


def h(*args):
    """A small stable hash, for picking variants by position."""
    return int(hashlib.md5(repr(args).encode()).hexdigest()[:8], 16)


# --------------------------------------------------------------------------
# Layers and structures
# --------------------------------------------------------------------------

class Layer:
    """An RGBA pixel layer. Pixels are set by color name; None is transparent."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.uint8)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            if c is None:
                self.a[y, x] = 0
            else:
                self.a[y, x, :3] = C[c]
                self.a[y, x, 3] = 255

    def get(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h) or self.a[y, x, 3] == 0:
            return None
        return RGB2NAME.get(tuple(int(v) for v in self.a[y, x, :3]))

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def hline(self, x0, x1, y, c):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.px(x, y, c)

    def vline(self, x, y0, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def mask_fill(self, mask, c, ox=0, oy=0):
        ys, xs = np.nonzero(mask)
        for y, x in zip(ys, xs):
            self.px(ox + x, oy + y, c)

    def poly(self, pts, c):
        m = Image.new("1", (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon(pts, fill=1)
        self.mask_fill(np.array(m), c)

    def ellipse(self, x0, y0, x1, y1, c):
        m = Image.new("1", (self.w, self.h), 0)
        ImageDraw.Draw(m).ellipse([x0, y0, x1, y1], fill=1)
        self.mask_fill(np.array(m), c)

    def blit(self, rows, legend, x, y, hflip=False):
        """Paint an ASCII grid. Chars missing from the legend (and ' ') are skipped."""
        for j, row in enumerate(rows):
            if hflip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch == " " or ch not in legend:
                    continue
                self.px(x + i, y + j, legend[ch])

    def paste(self, arr, x, y):
        """Copy an RGBA array in, opaque pixels only."""
        hh, ww = arr.shape[:2]
        for j in range(hh):
            for i in range(ww):
                if arr[j, i, 3] and 0 <= x + i < self.w and 0 <= y + j < self.h:
                    self.a[y + j, x + i] = arr[j, i]

    def recolor(self, table):
        for y in range(self.h):
            for x in range(self.w):
                n = self.get(x, y)
                if n in table:
                    self.px(x, y, table[n])


def grid_art(rows, legend):
    """An RGBA array from an ASCII grid (' ' and unknown chars transparent)."""
    hh, ww = len(rows), max(len(r) for r in rows)
    a = np.zeros((hh, ww, 4), np.uint8)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in legend and legend[ch] is not None:
                a[j, i, :3] = C[legend[ch]]
                a[j, i, 3] = 255
    return a


class Struct:
    """A structure: w x h metatiles, layers, behaviors, walk codes and notes.

    walk codes, one string per metatile row:
      X  impassable          .  passable          T  passable, drawn over the player
      J  ledge, jump south   >  ledge, jump east  <  ledge, jump west
      ~  still water (surf)  ^ v [ ]  arrow warps north, south, west, east
    behaviors: {(cx, cy): "MB_..."} on top of what the walk codes imply.
    names: optional {name: (cx, cy)} so map builders can ask for a piece by name.
    """

    WALK_MB = {"J": "MB_JUMP_SOUTH", ">": "MB_JUMP_EAST", "<": "MB_JUMP_WEST",
               "~": "MB_POND_WATER", "^": "MB_NORTH_ARROW_WARP", "v": "MB_SOUTH_ARROW_WARP",
               "[": "MB_WEST_ARROW_WARP", "]": "MB_EAST_ARROW_WARP"}

    def __init__(self, key, title, w, h, section, walk=None, notes="", names=None, floor_mb=None):
        self.key, self.title, self.w, self.h = key, title, w, h
        self.section = section
        self.layers = {n: Layer(w * 16, h * 16) for n in ("bottom", "middle", "top")}
        self.walk = walk or ["X" * w] * h
        self.notes = notes
        self.names = names or {}
        self.behaviors = {}
        self.ids = None
        self.origin = None
        assert len(self.walk) == h and all(len(r) == w for r in self.walk), key
        for cy, row in enumerate(self.walk):
            for cx, ch in enumerate(row):
                if ch in self.WALK_MB:
                    self.behaviors[(cx, cy)] = self.WALK_MB[ch]
                elif ch in ".T" and floor_mb:
                    self.behaviors[(cx, cy)] = floor_mb

    @property
    def B(self):
        return self.layers["bottom"]

    @property
    def M(self):
        return self.layers["middle"]

    @property
    def T(self):
        return self.layers["top"]

    def cell(self, cx, cy):
        """The 16x16 RGBA of each layer at a cell, for building other pieces from it."""
        return {n: L.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16].copy()
                for n, L in self.layers.items()}


def one(key, title, section, layers, walk=".", notes="", floor_mb=None, behavior=None):
    """A 1x1 Struct from {layer: 16x16 RGBA}."""
    s = Struct(key, title, 1, 1, section, walk=[walk], notes=notes, floor_mb=floor_mb)
    for n, a in layers.items():
        if a is not None:
            s.layers[n].a[:] = a
    if behavior:
        s.behaviors[(0, 0)] = behavior
    return s


# --------------------------------------------------------------------------
# Validation, packing and output
# --------------------------------------------------------------------------

def tile_colors(layer, tx, ty):
    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
    m = t[..., 3] > 0
    return {tuple(int(v) for v in p) for p in t[m][:, :3]}


def tile_group(cols):
    for g, rgb in GROUP_RGB.items():
        if cols <= rgb:
            return g
    return None


def validate(structs):
    problems = []
    seen = set()
    for s in structs:
        if s.key in seen:
            problems.append(f"duplicate key {s.key}")
        seen.add(s.key)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    cols = tile_colors(layer, tx, ty)
                    if cols and tile_group(cols) is None:
                        names = sorted(RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                cell = lambda L: (L.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16, 3] > 0)
                n = sum(1 for L in s.layers.values() if cell(L).any())
                if n == 3:
                    problems.append(f"{s.key} metatile ({cx},{cy}) has three layers")
                if n and not (cell(s.B) | cell(s.M)).all():
                    problems.append(f"{s.key} metatile ({cx},{cy}) has holes below the sprites layer")
                if s.walk[cy][cx] == "T" and not cell(s.T).any():
                    problems.append(f"{s.key} metatile ({cx},{cy}) is walk-behind but has no top layer")
    return problems


COLS = 8


def pack(sections):
    """Shelf-pack structures into the 8-wide sheet; each section starts on a fixed row."""
    total = 0
    for start, structs in sections:
        row, col, shelf_h = start, 0, 0
        for s in structs:
            assert s.w <= COLS, s.key
            if col + s.w > COLS:
                row += shelf_h
                col, shelf_h = 0, 0
            s.ids = [[0x200 + (row + y) * COLS + col + x for x in range(s.w)] for y in range(s.h)]
            s.origin = (col, row)
            col += s.w
            shelf_h = max(shelf_h, s.h)
        end = row + shelf_h
        total = max(total, end)
        later = [st for st, _ in sections if st > start]
        if later:
            assert end <= min(later), f"section at row {start} overflows into row {min(later)} (ends {end})"
    return total


def write_sources(structs, rows, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    W, H = COLS * 16, rows * 16
    for ln in ("bottom", "middle", "top"):
        sheet = np.zeros((H, W, 4), np.uint8)
        for s in structs:
            cx, cy = s.origin
            sheet[cy * 16:cy * 16 + s.h * 16, cx * 16:cx * 16 + s.w * 16] = s.layers[ln].a
        Image.fromarray(sheet, "RGBA").save(outdir / f"{ln}.png")
    beh = {}
    for s in structs:
        for (x, y), mb in s.behaviors.items():
            beh[s.ids[y][x] - 0x200] = mb
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]
    (outdir / "attributes.csv").write_text("\n".join(lines) + "\n")


def composite(s):
    comp = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    comp[:] = (255, 0, 255)  # holes would show magenta
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        m = a[..., 3] > 0
        comp[m] = a[..., :3][m]
    return comp


def preview(structs, scale=3, bg=(40, 40, 48), cols=4):
    """All layers composited, structures in a grid, for a quick look while painting."""
    pad = 6
    imgs = [Image.fromarray(composite(s)).resize((s.w * 16 * scale, s.h * 16 * scale), Image.NEAREST)
            for s in structs]
    rows = [imgs[i:i + cols] for i in range(0, len(imgs), cols)]
    W = max(sum(i.width + pad for i in r) for r in rows) + pad
    H = sum(max(i.height for i in r) + pad for r in rows) + pad
    out = Image.new("RGB", (W, H), bg)
    y = pad
    for r in rows:
        x = pad
        for i in r:
            out.paste(i, (x, y))
            x += i.width + pad
        y += max(i.height for i in r) + pad
    return out
