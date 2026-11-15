"""Shared toolkit for Ichor's battle interface art (healthboxes, bars, menus).

Everything is drawn as palette indices on an IdxCanvas, then written as an
indexed 4bpp PNG whose embedded palette is the one the game loads for it.
Colors are the master palette of design/phase1/PLAN.md (multiples of 8, so
they map exactly to GBA BGR555).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BI = ROOT / "graphics/battle_interface"
BT = ROOT / "graphics/battle_transitions"
IMG = ROOT / "design/phase1/img"

# Master palette (design/phase1/PLAN.md).
INK = (32, 24, 24)
CLAY_DARK = (120, 48, 24)
CLAY = (184, 88, 48)
CLAY_LIGHT = (224, 136, 88)
PARCHMENT = (232, 216, 176)
PARCH_SHADE = (208, 184, 136)
LIMESTONE = (176, 144, 96)
MARBLE_DARK = (168, 160, 152)
MARBLE = (216, 208, 192)
MARBLE_LIGHT = (248, 248, 240)
GOLD = (240, 192, 64)
GOLD_DARK = (200, 144, 40)
AEGEAN_DARK = (24, 56, 120)
AEGEAN = (48, 104, 176)
AEGEAN_LIGHT = (112, 168, 224)
AEGEAN_PALE = (176, 216, 240)
OLIVE_DARK = (56, 72, 32)
OLIVE = (96, 112, 48)
OLIVE_LIGHT = (144, 160, 72)
SILVER_LEAF = (168, 184, 136)
CYPRESS_DARK = (24, 56, 40)
CYPRESS = (40, 88, 56)
# Warm darks between ink and clay, for troughs and glaze.
GLAZE = (64, 40, 32)
# Text red of the dialogue box palette (graphics/text_window MSG_PAL 4).
RED = (192, 48, 32)

TRANSPARENT = (248, 0, 248)  # index 0 stand-in, never shown


def check_palette(pal):
    assert len(pal) == 16, len(pal)
    for c in pal[1:]:
        assert all(v % 8 == 0 and 0 <= v <= 248 for v in c), c
    return pal


class IdxCanvas:
    """A grid of palette indices."""

    def __init__(self, w, h, fill=0):
        self.w, self.h = w, h
        self.px = [[fill] * w for _ in range(h)]

    def set(self, x, y, i):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = i

    def get(self, x, y):
        return self.px[y][x]

    def rect(self, x0, y0, x1, y1, i):
        """Fill the inclusive rectangle [x0, x1] x [y0, y1]."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, i)

    def hline(self, x0, x1, y, i):
        self.rect(x0, y, x1, y, i)

    def vline(self, x, y0, y1, i):
        self.rect(x, y0, x, y1, i)

    def blit(self, x0, y0, rows, key):
        """Stamp a char grid; characters missing from key are skipped."""
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in key:
                    self.set(x0 + x, y0 + y, key[ch])

    def recolor(self, frm, to):
        for row in self.px:
            for x, v in enumerate(row):
                if v == frm:
                    row[x] = to

    def crop(self, x0, y0, w, h):
        c = IdxCanvas(w, h)
        for y in range(h):
            for x in range(w):
                c.px[y][x] = self.px[y0 + y][x0 + x]
        return c

    def paste(self, other, x0, y0, skip0=False):
        for y in range(other.h):
            for x in range(other.w):
                v = other.px[y][x]
                if skip0 and v == 0:
                    continue
                self.set(x0 + x, y0 + y, v)

    def tiles(self):
        """8x8 tiles in row-major order, each a tuple of 64 indices."""
        out = []
        for ty in range(self.h // 8):
            for tx in range(self.w // 8):
                out.append(tuple(self.px[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8)))
        return out

    def image(self, pal):
        im = Image.new("P", (self.w, self.h))
        im.putdata([v for row in self.px for v in row])
        flat = [v for c in check_palette(pal) for v in c]
        im.putpalette(flat)
        return im

    def rgba(self, pal, transparent0=True):
        im = Image.new("RGBA", (self.w, self.h))
        data = []
        for row in self.px:
            for v in row:
                if v == 0 and transparent0:
                    data.append((0, 0, 0, 0))
                else:
                    data.append(tuple(pal[v]) + (255,))
        im.putdata(data)
        return im

    def save(self, path, pal):
        path = Path(path)
        self.image(pal).save(path, bits=4)
        print(f"wrote {path.relative_to(ROOT)}")


def write_jasc(path, pal):
    path = Path(path)
    lines = ["JASC-PAL", "0100", str(len(pal))] + ["%d %d %d" % tuple(c) for c in pal]
    path.write_text("\r\n".join(lines) + "\r\n")
    print(f"wrote {path.relative_to(ROOT)}")


def read_png_palette(path, n=16):
    p = Image.open(path).getpalette()
    return [tuple(p[i * 3:i * 3 + 3]) for i in range(n)]


# --- Lettering -------------------------------------------------------------
# A 3x5 capital face for the little labels painted into the art (HP, EXP,
# the button caps). Black-figure painters lettered names beside their figures
# in just such small, square capitals.
GLYPHS_3x5 = {
    "A": ["###", "#.#", "###", "#.#", "#.#"],
    "B": ["##.", "#.#", "##.", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "F": ["###", "#..", "##.", "#..", "#.."],
    "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#.#", "###", "###", "#.#", "#.#"],
    "N": ["#.#", "###", "###", "###", "#.#"],
    "O": ["###", "#.#", "#.#", "#.#", "###"],
    "P": ["##.", "#.#", "##.", "#..", "#.."],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."],
    "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Z": ["###", "..#", ".#.", "#..", "###"],
}


def text_3x5(c, x, y, s, i, gap=1):
    for ch in s:
        if ch != " ":
            c.blit(x, y, GLYPHS_3x5[ch], {"#": i})
        x += 3 + gap
    return x


# --- The meander -----------------------------------------------------------
# The same running key as the dialogue box (tools/ichor/art/ui_frames.py):
# a 1 px line hooking back on itself, 5 px tall, repeating every 8 px.
MEANDER = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]


def meander_h(c, x0, x1, y, ink, ground, phase=0):
    """Horizontal meander band, 5 rows tall, from x0 to x1 inclusive."""
    for x in range(x0, x1 + 1):
        col = (x - x0 + phase) % 8
        for r in range(5):
            c.set(x, y + r, ink if MEANDER[r][col] == "#" else ground)


def meander_v(c, x, y0, y1, ink, ground, phase=0, mirror=False):
    """Vertical meander band, 5 columns wide, from y0 to y1 inclusive.

    The horizontal band turned a quarter: band rows become columns, so its
    continuous outer stroke runs down the outer side (x, or x + 4 if mirror).
    """
    for y in range(y0, y1 + 1):
        row = (y - y0 + phase) % 8
        for r in range(5):
            xx = x + (4 - r if mirror else r)
            c.set(xx, y, ink if MEANDER[r][row] == "#" else ground)
