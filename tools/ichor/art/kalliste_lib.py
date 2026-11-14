"""Shared toolkit for the kalliste secondary tileset's Greek structures.

Each structure is drawn pixel by pixel into up to three RGBA layers
(bottom/middle/top, as Porytiles reads them). Drawing is by named colors from
the palette groups below, using small primitives and ASCII grids with a legend.

Palette plan. The secondary has palettes 6-12: seven slots of 15 colors. Every
8x8 tile of every layer must draw only from ONE group below, so Porytiles can
always pack the seven groups into the seven slots. `validate()` enforces it.
All values are multiples of 8 (exact BGR555) and come from the PLAN.md master
families or are ramp steps between them.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]

C = {
    # shared
    "ink": (32, 24, 24),
    "w0": (248, 248, 240),
    # G1 Cycladic whitewash and Aegean paint
    "dk": (72, 64, 72),
    "w1": (232, 232, 216), "w2": (208, 200, 184), "w3": (176, 168, 160), "w4": (136, 128, 120),
    "b0": (24, 56, 120), "b1": (48, 104, 176), "b2": (112, 168, 224), "b3": (176, 216, 240),
    "tc0": (120, 48, 24), "tc1": (184, 88, 48), "tc2": (224, 136, 88), "tc3": (240, 184, 136),
    "ol0": (56, 72, 32), "ol1": (96, 112, 48), "ol2": (144, 160, 72), "ol3": (168, 184, 136),
    # G2 marble and hearth bronze
    "m1": (224, 216, 200), "m2": (200, 192, 176), "m3": (168, 160, 152), "m4": (128, 120, 112),
    "m5": (88, 80, 80),
    "br": (120, 72, 24), "g0": (200, 144, 40), "g1": (240, 192, 64),
    "fl": (216, 72, 32), "fc": (248, 232, 160),
    # G3 limestone, earth, weeds, wet stone
    "sk": (56, 40, 32), "s0": (96, 72, 48), "s1": (136, 104, 72), "s2": (176, 144, 96),
    "s3": (208, 184, 136), "s4": (232, 216, 176), "s5": (248, 240, 216),
    "e1": (152, 104, 64), "e2": (192, 144, 96),
    "wt0": (80, 80, 88), "wt1": (120, 112, 104), "alg": (80, 112, 72),
    # G4 wood, rope, boat paint
    "wd0": (72, 48, 32), "wd1": (120, 80, 48), "wd2": (168, 120, 72), "wd3": (208, 168, 112),
    "rp": (224, 208, 160), "rd": (184, 48, 32), "gn": (56, 120, 96), "ir": (96, 96, 104),
    # G6 Cycladic flagstones
    "pj1": (216, 208, 200),
    "sl0": (72, 80, 96), "sl1": (104, 112, 128), "sl2": (136, 144, 152), "sl3": (168, 176, 176),
    # G7 sea: aethos's deep water is b1 with wr ripples
    "wa1": (40, 80, 152), "wr": (80, 136, 200), "wa3": (96, 152, 216),
}

GROUPS = {
    "cyc": ["ink", "dk", "w0", "w1", "w2", "w3", "w4", "b0", "b1", "b2", "b3",
            "tc1", "tc2", "ol1", "ol2"],
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "br", "g0", "g1", "fl", "fc",
               "tc0", "tc1", "tc2"],
    "stone": ["sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "e2", "ol1", "ol2",
              "wt0", "wt1", "alg", "ink"],
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "b0", "b1", "b2", "rd", "g1",
             "gn", "ir", "tc1"],
    "clay": ["ink", "tc0", "tc1", "tc2", "tc3", "ol0", "ol1", "ol2", "ol3", "w0", "g0", "g1",
             "wd1", "wd2", "rd"],
    "paving": ["ink", "w0", "pj1", "sl0", "sl1", "sl2", "sl3", "g0", "g1", "tc1", "b1", "b2",
               "w2", "w3"],
    "sea": ["b0", "wa1", "b1", "wr", "wa3", "b2", "b3", "w0", "ink"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    for n in names:
        assert n in C, n
for n, c in C.items():
    assert all(v % 8 == 0 and 0 <= v <= 248 for v in c), (n, c)
    assert c != (255, 0, 255)
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}


# --------------------------------------------------------------------------
# Layers and drawing
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
        rgb = tuple(int(v) for v in self.a[y, x, :3])
        return RGB2NAME.get(rgb)

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
        """Bresenham line."""
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
        """Paint an ASCII grid. Chars missing from the legend (and ' ') are skipped;
        a legend value of None erases."""
        for j, row in enumerate(rows):
            if hflip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch == " " or ch not in legend:
                    continue
                self.px(x + i, y + j, legend[ch])

    def pattern(self, rows, legend, x, y, w, h, ox=0, oy=0):
        """Fill a box with a repeating ASCII pattern, phase-locked to (ox, oy)."""
        ph, pw = len(rows), len(rows[0])
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                ch = rows[(yy - oy) % ph][(xx - ox) % pw]
                if ch != " " and ch in legend:
                    self.px(xx, yy, legend[ch])

    def replace(self, x, y, w, h, frm, to):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if self.get(xx, yy) == frm:
                    self.px(xx, yy, to)

    def outline(self, color, inside=True, region=None):
        """1 px outline on the silhouette edge of the opaque pixels."""
        alpha = self.a[..., 3] > 0
        pad = np.pad(alpha, 1)
        edge = alpha & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        ys, xs = np.nonzero(edge)
        for y, x in zip(ys, xs):
            if region and not (region[0] <= x < region[0] + region[2] and region[1] <= y < region[1] + region[3]):
                continue
            self.px(x, y, color)

    def copy_from(self, other, x0=0, y0=0, w=None, h=None, dx=0, dy=0):
        w = other.w if w is None else w
        h = other.h if h is None else h
        src = other.a[y0:y0 + h, x0:x0 + w]
        m = src[..., 3] > 0
        dst = self.a[dy:dy + h, dx:dx + w]
        dst[m] = src[m]


RGB2NAME = {}
for _n, _c in C.items():
    RGB2NAME.setdefault(_c, _n)


class Struct:
    """A structure: w x h metatiles, layers, behaviors and placement notes.

    walk: one string per metatile row. Codes:
      X  impassable (set collision 1 when placing)
      .  passable
      D  door: warp event here; behavior MB_NON_ANIMATED_DOOR
      T  passable, drawn above the player (the player walks behind it)
      J  ledge: MB_JUMP_SOUTH
    """

    def __init__(self, key, title, w, h, section, walk=None, notes=""):
        self.key, self.title, self.w, self.h = key, title, w, h
        self.section = section
        self.layers = {n: Layer(w * 16, h * 16) for n in ("bottom", "middle", "top")}
        self.walk = walk or ["X" * w] * h
        self.notes = notes
        self.behaviors = {}  # (cx, cy) -> MB_*
        self.ids = None      # filled by pack()
        assert len(self.walk) == h and all(len(r) == w for r in self.walk), key
        for cy, row in enumerate(self.walk):
            for cx, ch in enumerate(row):
                if ch == "D":
                    self.behaviors[(cx, cy)] = "MB_NON_ANIMATED_DOOR"
                elif ch == "J":
                    self.behaviors[(cx, cy)] = "MB_JUMP_SOUTH"

    @property
    def B(self):
        return self.layers["bottom"]

    @property
    def M(self):
        return self.layers["middle"]

    @property
    def T(self):
        return self.layers["top"]


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
        used = []
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    cols = tile_colors(layer, tx, ty)
                    if not cols:
                        continue
                    if not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        # Porytiles' dual-layer mode: at most two layers per metatile.
        for cy in range(s.h):
            for cx in range(s.w):
                n = sum(1 for layer in s.layers.values()
                        if (layer.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16, 3] > 0).any())
                used.append(n)
                if n == 3:
                    problems.append(f"{s.key} metatile ({cx},{cy}) has three layers")
                b = s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16, 3]
                m = s.M.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16, 3]
                lower = np.maximum(b, m)
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} metatile ({cx},{cy}) has holes below the sprites layer")
    return problems


COLS = 8  # metatiles per row in the Porytiles sheets


def pack(sections):
    """Shelf-pack structures into the 8-wide sheet, section by section.

    sections: list of (start_row, [structs]). Each section starts on a fixed row so
    adding to one section never moves another section's ids.
    Returns total rows.
    """
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
        s_next = None
        for st, _ in sections:
            if st > start:
                s_next = st if s_next is None else min(s_next, st)
        if s_next is not None:
            assert end <= s_next, f"section at row {start} overflows into row {s_next} (ends {end})"
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
    lines = ["id,behavior"]
    beh = {}
    for s in structs:
        for (x, y), mb in s.behaviors.items():
            beh[s.ids[y][x] - 0x200] = mb
    for k in sorted(beh):
        lines.append(f"{k},{beh[k]}")
    (outdir / "attributes.csv").write_text("\n".join(lines) + "\n")


def preview(structs, scale=3, bg=(40, 40, 48)):
    """All layers composited on a neutral backdrop, each structure labeled."""
    pad = 6
    imgs = []
    for s in structs:
        comp = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
        comp[:] = (255, 0, 255)  # holes would show magenta
        for ln in ("bottom", "middle", "top"):
            a = s.layers[ln].a
            m = a[..., 3] > 0
            comp[m] = a[..., :3][m]
        imgs.append(Image.fromarray(comp).resize((s.w * 16 * scale, s.h * 16 * scale), Image.NEAREST))
    width = max(i.width for i in imgs) + 2 * pad
    height = sum(i.height + pad for i in imgs) + pad
    out = Image.new("RGB", (width, height), bg)
    y = pad
    for i in imgs:
        out.paste(i, (pad, y))
        y += i.height + pad
    return out
