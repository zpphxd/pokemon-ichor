"""Shared toolkit for gTileset_CaveDark, the secondary tileset of Ichor's dark places.

cave_dark serves Hecate's Hollow, the Salt Grotto, Akti's Sea Grotto and the
Kronion Crypt (design/phase2/SCRIPT.md Part 10, design/SYSTEMS.md §2).

Like agros and kalliste it is self-contained: compiled against an empty
stand-in primary, so its metatiles use only its own tiles and palettes 6-12
and work on any primary (the maps pair it with aethos).

Palette plan: seven groups, one per secondary palette, at most 15 colors each.
Every 8x8 tile of every layer draws from ONE group; validate() enforces it.
Objects that stand on the floor keep the floor in the bottom layer and draw
themselves in the middle (or top) layer, so the floor's tiles are shared and
an object's tiles need only its own group.

The glow palette (SYSTEMS.md §2, dousing): the chalk colors are the only
ones that survive in the glow copy. In ordinary light they are faint chalk
on the rock; doused, they glow.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]

C = {
    # ink and the cold limestone ramp of the walls (k0 darkest)
    "k0": (16, 16, 32), "k1": (32, 32, 56), "k2": (48, 48, 80), "k3": (72, 72, 104),
    "k4": (96, 96, 128), "k5": (128, 128, 152), "k6": (160, 160, 184), "k7": (192, 192, 208),
    "k8": (224, 224, 232),
    # wet flowstone streaks and moss on the walls
    "tl1": (56, 88, 104), "tl2": (96, 136, 144),
    # Hecate's chalk: faint in light, the glow copy's only colors when doused
    "ch1": (136, 160, 152), "ch2": (200, 216, 200),
    # web silk and daylight seen through a mouth
    "wh": (240, 240, 232),
    # the floor: cave clay, a little warmer than the walls
    "f0": (24, 24, 32), "f1": (40, 40, 48), "f2": (64, 56, 64), "f3": (88, 80, 88),
    "f4": (112, 104, 112), "f5": (144, 136, 136), "f6": (176, 168, 160),
    "pd1": (40, 64, 88), "pd2": (88, 120, 144),
    # moonlight (or daylight) lying on the floor
    "mn1": (112, 120, 144), "mn2": (152, 160, 184), "dl": (224, 224, 208),
    # still water, deep to bright
    "w0": (16, 24, 48), "w1": (24, 40, 72), "w2": (32, 64, 96), "w3": (56, 96, 120),
    "w4": (96, 144, 160), "w5": (176, 216, 216),
    "al1": (40, 80, 64), "al2": (80, 128, 88), "an": (184, 56, 80), "sf": (232, 136, 72),
    # bronze and fire
    "b0": (64, 40, 32), "b1": (112, 72, 40), "b2": (160, 112, 56), "b3": (216, 168, 96),
    "fr1": (184, 48, 32), "fr2": (232, 112, 40), "fr3": (248, 184, 72), "fr4": (248, 240, 200),
    "ash": (96, 88, 88), "ash2": (136, 128, 120),
    # Hekate's marble: the Hekataion, the sarcophagus, the altar stone
    "m0": (40, 40, 64), "m1": (88, 88, 120), "m2": (136, 136, 168), "m3": (184, 184, 208),
    "m4": (224, 224, 240), "m5": (248, 248, 248), "ck": (200, 152, 88), "ck2": (152, 104, 64),
    # Kronion's poros stone (kalliste's "stone" family, darker underground)
    "sk": (48, 32, 32), "s0": (80, 56, 48), "s1": (112, 88, 64), "s2": (152, 120, 88),
    "s3": (192, 160, 120), "s4": (224, 200, 160), "s5": (240, 232, 208),
    "e1": (128, 88, 48), "tc": (168, 72, 48), "ochre": (200, 152, 64),
    # the sea grottos' wet rock: the cave's rock recolored (it shares the cave's tiles)
    "g0": (8, 16, 24), "g1": (16, 32, 40), "g2": (24, 48, 56), "g3": (40, 64, 72),
    "g4": (56, 88, 96), "g5": (80, 112, 112), "g6": (112, 144, 136), "g7": (152, 184, 168),
    "g8": (208, 232, 216), "sw1": (32, 72, 40), "sw2": (72, 120, 56), "foam": (232, 248, 240),
    "salt": (240, 248, 248), "bn": (176, 168, 152),
}

# Recolors that share the cave's tiles under another palette (Porytiles tile
# sharing). Each is one-to-one on the colors the shared pieces use.
WET = {"k0": "g0", "k1": "g1", "k2": "g2", "k3": "g3", "k4": "g4", "k5": "g5", "k6": "g6",
       "k7": "g7", "k8": "g8", "tl1": "sw1", "tl2": "sw2", "wh": "foam"}
POROS = {"k0": "k0", "k1": "sk", "k2": "s0", "k3": "s1", "k4": "s2", "k5": "s3", "k6": "s4",
         "k7": "s5"}

GROUPS = {
    # the cave's walls: rock mass, rims, flowstone faces, stalactites, webs, chalk
    "rock": ["k0", "k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8", "tl1", "tl2", "ch1", "ch2",
             "wh", "f3"],
    # the floor, its shadows, puddles, moonlight and daylight, chalk
    "floor": ["k0", "f0", "f1", "f2", "f3", "f4", "f5", "f6", "pd1", "pd2", "mn1", "mn2", "dl",
              "ch1", "ch2"],
    # still water and its banks, the tide pool's life
    "water": ["k0", "w0", "w1", "w2", "w3", "w4", "w5", "f1", "f2", "f3", "f4", "al1", "al2",
              "an", "sf"],
    # bronze, flame and ash: braziers, the offering bowl
    "fire": ["k0", "b0", "b1", "b2", "b3", "fr1", "fr2", "fr3", "fr4", "ash", "ash2", "f1",
             "f2", "f3", "f4"],
    # pale marble: the Hekataion, the sarcophagus, the altar; the barley cake
    "marble": ["k0", "m0", "m1", "m2", "m3", "m4", "m5", "b1", "b2", "fr2", "fr3", "fr4", "ck",
               "ck2", "w3"],
    # the crypt's cut poros stone, and its rock (the cave's recolored)
    "crypt": ["k0", "sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "tc", "ochre", "f1", "f2",
              "f3", "k3"],
    # the sea grottos' wet rock (the cave's recolored), weed, foam, salt, barnacles
    "grotto": ["g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "sw1", "sw2", "foam",
               "salt", "bn", "k0"],
}
# The glow copy (dousing): every slot black but the chalk.
GLOW = {"ch1": (32, 136, 112), "ch2": (152, 248, 208)}
GLOW_GROUPS = ("rock", "floor")

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
