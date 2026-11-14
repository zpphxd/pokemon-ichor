"""Shared toolkit for gTileset_Agros, the countryside secondary tileset.

Agros holds the rural art for Route 1, Kronion Hill and later routes: soft
tall-grass and path edges, goat tracks, trees and shrubs, rocks and hill
slopes, farm props, and copies of the kalliste ruins those maps use.

Like kalliste, Agros is self-contained: it is compiled against an empty
stand-in primary, so its metatiles use only its own tiles and palettes 6-12
and keep working whatever aethos becomes. Its ground pieces must still meet
aethos ground seamlessly, so they are painted from aethos's own pixels, read
from the compiled aethos tileset when Agros is built. Rebuild Agros after
aethos's grass, tall grass or path change.

Palette plan: seven groups, one per secondary palette, at most 15 colors each.
Every 8x8 tile of every layer draws from ONE group; validate() enforces it.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]

C = {
    "ink": (32, 24, 24),
    # aethos ground: grass, its shade, tall grass (barley), the limestone path
    "g1": (144, 152, 72), "g2": (184, 184, 104), "g3": (208, 200, 128), "gd": (112, 128, 64),
    "t0": (40, 56, 32), "t1": (72, 88, 48), "t3": (160, 176, 80), "tg": (240, 192, 64),
    "p1": (208, 184, 136), "p2": (232, 216, 176), "p3": (248, 240, 216),
    # aethos limestone (ledges, boulders) and bare earth
    "l0": (120, 96, 64), "l1": (176, 144, 96),
    # aethos olive, pine and cypress foliage and trunks
    "o4": (152, 168, 120), "o5": (200, 208, 176),
    "k1": (88, 72, 56), "k2": (128, 120, 112), "k3": (168, 160, 152),
    "c1": (24, 56, 40), "c2": (40, 88, 56), "c3": (72, 120, 72),
    # whitewash and grey stone
    "w0": (248, 248, 240), "w1": (216, 208, 192),
    # terracotta and wood
    "tc0": (120, 48, 24), "tc1": (184, 88, 48), "tc2": (224, 136, 88),
    "wd1": (128, 88, 56), "wd2": (168, 128, 88),
    # blossoms: oleander, broom, thyme
    "op1": (184, 56, 104), "op2": (232, 120, 160), "op3": (248, 192, 208),
    "y2": (200, 144, 40), "th1": (112, 72, 128), "th2": (168, 128, 184),
    # the Aegean, as aethos paints it
    "b1": (48, 104, 176), "b2": (80, 136, 200), "b3": (112, 168, 224), "b4": (176, 216, 240),
    # kalliste's "stone" group, verbatim, for the copied Kronion ruins and walls
    "sk": (56, 40, 32), "s0": (96, 72, 48), "s1": (136, 104, 72), "s2": (176, 144, 96),
    "s3": (208, 184, 136), "s4": (232, 216, 176), "s5": (248, 240, 216),
    "e1": (152, 104, 64), "e2": (192, 144, 96), "ol1": (96, 112, 48), "ol2": (144, 160, 72),
    "wt0": (80, 80, 88), "wt1": (120, 112, 104), "alg": (80, 112, 72),
}

GROUPS = {
    # soft tall-grass and path edges, goat tracks, herbs on grass
    "field": ["g1", "g2", "g3", "gd", "t0", "t1", "t3", "tg", "p1", "p2", "p3", "l0", "l1",
              "th1", "th2"],
    # trees and their shade
    "grove": ["g1", "g2", "g3", "gd", "t0", "t1", "o4", "o5", "k1", "k2", "k3", "ink",
              "c1", "c2", "c3"],
    # limestone on grass: rocks, ledges, side walls, hill faces, the threshing floor
    "rock": ["g1", "g2", "g3", "gd", "t0", "l0", "l1", "p1", "p2", "p3", "k2", "k3", "w0",
             "ink", "k1"],
    # the cart and the bee wall
    "clay": ["tc0", "tc1", "tc2", "k1", "wd1", "wd2", "l1", "p1", "p2", "ink", "g1", "g2",
             "g3", "gd", "tg"],
    # shrubs in flower
    "bloom": ["g1", "g2", "g3", "gd", "t0", "t1", "op1", "op2", "op3", "tg", "y2", "th1",
              "th2", "ink", "c2"],
    # water and whitewash: the spring, the shore, the roadside shrine
    "water": ["b1", "b2", "b3", "b4", "w0", "w1", "k2", "k3", "l1", "p1", "p2", "g1", "g2",
              "g3", "ink"],
    # kalliste's stone, for the copied ruins, walls and terraces
    "kstone": ["sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "e2", "ol1", "ol2", "wt0",
               "wt1", "alg", "ink"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    for _n in _names:
        assert _n in C, _n
for _n, _c in C.items():
    assert all(v % 8 == 0 and 0 <= v <= 248 for v in _c), (_n, _c)
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}
RGB2NAME = {}
for _n, _c in C.items():
    RGB2NAME.setdefault(_c, _n)


# --------------------------------------------------------------------------
# aethos pixels: the ground textures Agros must match
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _renderer():
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                       rm.Tileset(rm.resolve_tileset("gTileset_Kalliste", syms)))


@lru_cache(maxsize=None)
def aethos(mid):
    """16x16 RGB of an aethos metatile, both layers, as the GBA shows it."""
    img, ok = _renderer().metatile(mid)
    assert ok, hex(mid)
    return img.copy()


GRASS, TALL, PATH, SHADE, SEA = 0x001, 0x00D, 0x1D9, 0x01C, 0x170


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

    def rgb(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x, :3] = rgb
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

    def texture(self, mid, x, y, w, h, mask=None):
        """Fill a box with an aethos metatile's pixels, phase-locked to the 16 px grid."""
        src = aethos(mid)
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if mask is None or mask[yy - y, xx - x]:
                    self.rgb(xx, yy, src[yy % 16, xx % 16])

    def outline(self, color, ref=None):
        """1 px outline on the silhouette edge of the opaque pixels."""
        alpha = (ref if ref is not None else self).a[..., 3] > 0
        pad = np.pad(alpha, 1)
        edge = alpha & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        ys, xs = np.nonzero(edge)
        for y, x in zip(ys, xs):
            self.px(x, y, color)


class Struct:
    """A structure: w x h metatiles, layers, behaviors, walk codes and notes.

    walk codes, one string per metatile row:
      X  impassable          .  passable          T  passable, drawn over the player
      J  ledge (MB_JUMP_SOUTH)                     G  tall grass (MB_TALL_GRASS)
    names: optional {name: (cx, cy)} so map builders can ask for a piece by name.
    """

    def __init__(self, key, title, w, h, section, walk=None, notes="", names=None):
        self.key, self.title, self.w, self.h = key, title, w, h
        self.section = section
        self.layers = {n: Layer(w * 16, h * 16) for n in ("bottom", "middle", "top")}
        self.walk = walk or ["X" * w] * h
        self.notes = notes
        self.names = names or {}
        self.behaviors = {}
        self.ids = None
        assert len(self.walk) == h and all(len(r) == w for r in self.walk), key
        for cy, row in enumerate(self.walk):
            for cx, ch in enumerate(row):
                if ch == "J":
                    self.behaviors[(cx, cy)] = "MB_JUMP_SOUTH"
                elif ch == "G":
                    self.behaviors[(cx, cy)] = "MB_TALL_GRASS"

    @property
    def B(self):
        return self.layers["bottom"]

    @property
    def M(self):
        return self.layers["middle"]

    @property
    def T(self):
        return self.layers["top"]


def adopt(kstruct, section):
    """Copy a kalliste_lib Struct (pixels, walk, behaviors) into an Agros Struct."""
    s = Struct(kstruct.key, kstruct.title, kstruct.w, kstruct.h, section,
               walk=[r.replace("D", "X") for r in kstruct.walk], notes=kstruct.notes)
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = kstruct.layers[ln].a
    s.behaviors = dict(kstruct.behaviors)
    return s


# --------------------------------------------------------------------------
# Validation, packing and output
# --------------------------------------------------------------------------

def tile_colors(layer, tx, ty):
    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
    m = t[..., 3] > 0
    return {tuple(int(v) for v in p) for p in t[m][:, :3]}


def validate(structs):
    problems = []
    for s in structs:
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    cols = tile_colors(layer, tx, ty)
                    if cols and not any(cols <= g for g in GROUP_RGB.values()):
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


def preview(structs, scale=3, bg=(40, 40, 48)):
    """All layers composited, structures stacked, for a quick look while painting."""
    pad = 6
    imgs = [Image.fromarray(composite(s)).resize((s.w * 16 * scale, s.h * 16 * scale), Image.NEAREST)
            for s in structs]
    out = Image.new("RGB", (max(i.width for i in imgs) + 2 * pad, sum(i.height + pad for i in imgs) + pad), bg)
    y = pad
    for i in imgs:
        out.paste(i, (pad, y))
        y += i.height + pad
    return out
