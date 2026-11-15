#!/usr/bin/env python3
"""Pixel art for the interiors of Styx Falls and Arkadia (Act II batch 3).

The base of the art: the seven palettes, a small canvas for drawing pieces as
character grids, the floors, the walls and the stamp registry. The furniture
lives in three more modules, which register their stamps here when imported:

  arkrooms_styx.py   Nonakris at Styx Falls: the inn, Horkia's, Kepheus's
  arkrooms_civic.py  Arkadia's Asclepeion, the Agora stall, Klymene's upper room
  arkrooms_homes.py  Nyktimos's hall, Hippothoos's hut, Krotos's house and byre

Everything is drawn as character grids, one character per color and '.' for
clear, in the style of oikia_art.py (whose floors and a few of whose pieces are
reused here as they are). Each 8x8 tile of a layer must take all its colors from
one palette; arkrooms_build.py checks that.

Three looks run through the rooms:
  Nonakris  low stone houses roofed with slabs, whitewashed against the damp;
            the black cliff of the Styx is the back wall of two of them.
  Arkadia   a town in a cypress forest: timber the color of cypress heartwood,
            grey mossy limestone, smoke, pelts, hunters' herbs and nets.
  Homes     dark smoked logs, earth shored with timber, straw and goats.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import oikia_art as OA  # noqa: E402  (floors and a few pieces are reused as drawn)

INK = OA.INK  # (40, 24, 24)

# --------------------------------------------------------------------------
# Palettes. Every value is a multiple of 8 and none is an aethos color, so
# Porytiles can only place these tiles in palettes 6-12 (the builder checks).
# Four are oikia's, unchanged, so its pieces are reused exactly as drawn; the
# wall and nature palettes keep the colors oikia's reused pieces need.
# --------------------------------------------------------------------------

PALETTES = {
    # plaster and timber: beams, whitewash, oikia's shutters and sky; cypress
    # heartwood (the Arkadian timber) in place of oikia's red dado
    "wall": {
        "k": INK,
        "1": (80, 48, 32),     # beam, dark
        "2": (120, 72, 40),    # beam
        "3": (160, 104, 56),   # beam, lit
        "w": (248, 240, 232),  # whitewash, lit
        "p": (232, 224, 208),  # whitewash
        "s": (208, 192, 176),  # whitewash, shade
        "S": (168, 152, 136),  # whitewash, deep shade, damp
        "r": (176, 88, 64),    # cypress heartwood, lit
        "R": (128, 56, 48),    # cypress heartwood
        "D": (72, 32, 32),     # cypress, smoked
        "o": (216, 168, 104),  # sapwood, ochre
        "b": (56, 96, 160),    # shutter blue
        "B": (104, 152, 208),  # shutter blue, lit
        "a": (200, 224, 240),  # sky
    },
    "floor": dict(OA.PALETTES["floor"]),
    "wood": dict(OA.PALETTES["wood"]),
    "clay": dict(OA.PALETTES["clay"]),
    # leaves and cypress, fleece, wicker and straw, rope; goat and wolf
    "nature": {
        "k": INK,
        "G": (40, 72, 48),     # leaf, dark; cypress
        "g": (72, 120, 56),    # leaf
        "v": (120, 168, 80),   # leaf, lit
        "V": (184, 216, 128),  # leaf, highlight
        "w": (248, 248, 232),  # fleece, bone, cake
        "K": (120, 88, 48),    # wicker, dark
        "j": (176, 136, 72),   # wicker
        "J": (224, 192, 128),  # wicker, lit; straw
        "n": (208, 184, 144),  # rope, linen
        "d": (96, 64, 40),     # goat, dark brown
        "m": (160, 112, 72),   # goat, tan
        "p": (88, 88, 96),     # wolf, dark grey
        "s": (144, 144, 144),  # wolf, grey
        "S": (192, 192, 184),  # wolf, pale
    },
    "bronze": dict(OA.PALETTES["bronze"]),
    # rock and earth: the Styx's black cliff, Arkadia's grey limestone and moss,
    # earth and logs
    "rock": {
        "k": INK,
        "1": (24, 24, 32),     # black rock, deepest
        "2": (40, 40, 56),     # black rock
        "3": (64, 64, 88),     # black rock, lit
        "4": (104, 112, 136),  # wet sheen
        "5": (168, 184, 208),  # wet glint
        "6": (88, 88, 80),     # limestone, dark
        "7": (128, 128, 112),  # limestone
        "8": (168, 168, 152),  # limestone, lit
        "9": (208, 208, 192),  # limestone, highlight
        "m": (72, 96, 56),     # moss
        "M": (112, 144, 80),   # moss, lit
        "e": (72, 48, 40),     # earth, dark; log shadow
        "E": (112, 80, 56),    # earth; log
        "h": (160, 120, 80),   # log, lit
    },
}

# The order the builder hands these to Porytiles as packing hints.
PALETTE_ORDER = ["wall", "floor", "wood", "clay", "nature", "bronze", "rock"]


def grid(pal, text, w=None, h=None):
    """Parse a character grid into an (h, w, 4) RGBA array ('.' or ' ' = clear)."""
    rows = [r.rstrip() for r in text.strip("\n").split("\n")]
    w = w or max(len(r) for r in rows)
    h = h or len(rows)
    assert len(rows) <= h, f"{len(rows)} rows > {h}"
    out = np.zeros((h, w, 4), np.uint8)
    colors = PALETTES[pal]
    for y, row in enumerate(rows):
        assert len(row) <= w, f"row {y} is {len(row)} wide > {w}: {row!r}"
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            if ch not in colors:
                raise ValueError(f"{pal}: unknown char {ch!r} at ({x},{y}) in {row!r}")
            out[y, x, :3] = colors[ch]
            out[y, x, 3] = 255
    return out


def over(dst, src):
    out = dst.copy()
    m = src[..., 3] > 0
    out[m] = src[m]
    return out


def recolor(img, pal, mapping, pal_to=None):
    """Swap colors by character: {'a': 'b'} turns pal.a into (pal_to or pal).b."""
    src_cols, dst_cols = PALETTES[pal], PALETTES[pal_to or pal]
    out = img.copy()
    for a, b in mapping.items():
        m = (img[..., :3] == src_cols[a]).all(-1) & (img[..., 3] > 0)
        out[m, :3] = dst_cols[b]
    return out


def hflip(img):
    return img[:, ::-1].copy()


def blank(w, h):
    return np.zeros((h * 16, w * 16, 4), np.uint8)


def noise(x, y, seed=0):
    """A cheap deterministic hash in [0, 1)."""
    v = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((v ^ (v >> 16)) & 0xFFFF) / 65536.0


# --------------------------------------------------------------------------
# A character canvas for drawing pieces in code.
# --------------------------------------------------------------------------

class Canvas:
    """A grid of palette characters, '.' clear. Coordinates are pixels."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        """Fill x0..x1, y0..y1 inclusive."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def box(self, x0, y0, x1, y1, fill, edge="k"):
        self.rect(x0, y0, x1, y1, edge)
        if x1 - x0 >= 2 and y1 - y0 >= 2:
            self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def ellipse(self, cx, cy, rx, ry, fill, edge=None):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1.0:
                    inner = ((x - cx) / max(rx - 1, 0.5)) ** 2 + ((y - cy) / max(ry - 1, 0.5)) ** 2
                    self.put(x, y, edge if (edge and inner > 1.0) else fill)

    def paste(self, x, y, text):
        """Paste a small grid; '.' is clear (leaves what's under it)."""
        for dy, row in enumerate(text.strip("\n").split("\n")):
            for dx, c in enumerate(row.rstrip()):
                if c not in ". ":
                    self.put(x + dx, y + dy, c)

    def text(self):
        return "\n".join("".join(r) for r in self.g)

    def img(self, pal):
        return grid(pal, self.text(), self.w, self.h)


# --------------------------------------------------------------------------
# Floors: 16x16, opaque, bottom layer. Each has plain, top (under a wall),
# left (along a left edge) and corner variants, and may have an alternate
# plain sprinkled through empty floor.
# --------------------------------------------------------------------------

SHADE = {
    "terracotta": ("floor", {"T": "x", "t": "u", "x": "u", "u": "v", "v": "g"}),
    "boards": ("floor", {"W": "m", "m": "n", "n": "j"}),
    "flags": ("floor", {"L": "y", "l": "q", "y": "q", "q": "Q"}),
    "earth": ("floor", {"W": "m", "m": "n", "n": "j", "u": "v", "j": "g", "x": "u"}),
    "slate": ("rock", {"9": "8", "8": "7", "7": "6", "6": "e", "m": "6"}),
    "darkboards": ("floor", {"n": "j", "j": "g", "W": "n"}),
    "straw": ("nature", {"J": "j", "j": "K", "n": "j", "K": "d", "w": "n"}),
    "charearth": ("rock", {"E": "e", "e": "2", "h": "E", "6": "2", "2": "1"}),
}


def _shade(img, material, mask):
    pal, m = SHADE[material]
    dark = recolor(img, pal, m)
    out = img.copy()
    out[mask] = dark[mask]
    return out


def floor_variants(material, base, alt=None, shade_as=None):
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    s = shade_as or material
    out = {"plain": base, "top": _shade(base, s, top), "left": _shade(base, s, left),
           "corner": _shade(base, s, top | left)}
    if alt is not None:
        out["alt"] = alt
    return out


def _earth(seed, pebbles, crack):
    """Packed earth from the floor palette's board browns: soft patches, a few
    pebbles and a hairline crack. Periodic over 16, so neighbours join."""
    g = [["n"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            r = noise(x, y, seed)
            if r < 0.10 and noise(x + 1, y, seed) < 0.5:
                g[y][x] = "m"
                if x + 1 < 16:
                    g[y][x + 1] = "m"
            elif r < 0.13:
                g[y][x] = "u"
            elif r < 0.15:
                g[y][x] = "j"
    for (x, y) in pebbles:
        g[y][x] = "W"
        g[y + 1][x] = "j"
    for (x, y) in crack:
        g[y][x] = "j"
    return grid("floor", "\n".join("".join(r) for r in g))


def _slate(seed):
    """Nonakris's floors: big slabs of the grey mountain stone, laid irregularly
    (two to a cell, the joint wandering), cold and worn smooth."""
    g = [["7"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            n = noise(x, y, seed + 50)
            if n < 0.10:
                g[y][x] = "8"
            elif n > 0.95:
                g[y][x] = "6"
    # a stepped horizontal joint (the slabs are different heights), and a
    # vertical joint in each course at a different x, so nothing lines up
    step = 6 + (seed * 5) % 5
    jy_l, jy_r = 6 + seed % 2, 9 - seed % 2
    jx_top = 3 + (seed * 7) % 9
    jx_bot = 10 - (seed * 3) % 6
    for x in range(16):
        jy = jy_l if x < step else jy_r
        g[jy][x] = "6"
        g[15][x] = "6"
        if x == step:
            for y in range(min(jy_l, jy_r), max(jy_l, jy_r) + 1):
                g[y][x] = "6"
    for y in range(0, min(jy_l, jy_r)):
        g[y][jx_top] = "6"
    for y in range(max(jy_l, jy_r) + 1, 15):
        g[y][jx_bot] = "6"
    for y in range(16):
        g[y][15] = "6" if y % 5 else "e"
    # worn: a lit edge under each joint, broken; a fleck of mica
    for y in range(1, 16):
        for x in range(16):
            if g[y][x] == "7" and g[y - 1][x] == "6" and noise(x, y, seed) < 0.7:
                g[y][x] = "8"
    g[(4 + seed * 3) % 14 + 1][(11 + seed) % 14] = "9"
    return grid("rock", "\n".join("".join(r) for r in g))


def _darkboards(seed):
    """Nyktimos's hall: wide planks of old dark wood, smoke-dulled, running
    east-west, each plank 4 px tall with a dark seam and a nail or a knot."""
    # the floor palette's darkest browns: long planks, low-contrast seams, a
    # butt joint in only some planks, so the floor reads calm under the table
    g = [["j"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            row = y % 4
            if row == 3:
                g[y][x] = "g"
            elif row == 0 and noise(x, y, seed + 40) < 0.35:
                g[y][x] = "n"
            elif noise(x, y, seed) < 0.04:
                g[y][x] = "g"
    for i, jx in enumerate([(5 + seed * 3) % 16, None, (11 + seed * 7) % 16, None]):
        if jx is None:
            continue
        for y in range(i * 4, i * 4 + 3):
            g[y][jx] = "g"
    return grid("floor", "\n".join("".join(r) for r in g))


def _straw(seed):
    """The byre's straw, loose over earth: short strokes of three straw tones,
    no two cells alike enough to show a grid."""
    g = [["j"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            n = noise(x, y, seed)
            if n < 0.18:
                g[y][x] = "K"
            elif n > 0.70:
                g[y][x] = "J"
    for i in range(14):
        x0 = int(noise(i, 1, seed + 3) * 16)
        y0 = int(noise(i, 2, seed + 3) * 16)
        dx = 1 if noise(i, 3, seed) < 0.5 else -1
        c = "J" if i % 3 else "n"
        for t in range(4):
            g[(y0 + t // 2) % 16][(x0 + t * dx) % 16] = c
    return grid("nature", "\n".join("".join(r) for r in g))


def _charearth(seed):
    """Hippothoos's floor: earth trodden black with charcoal dust, a few
    crumbs of charcoal and pale ash."""
    g = [["e"] * 16 for _ in range(16)]
    # soft patches of black dust where two neighbours agree, a little bare earth
    for y in range(16):
        for x in range(16):
            n = noise(x, y, seed)
            if n < 0.12 and noise(x + 1, y, seed) < 0.6:
                g[y][x] = "2"
                g[y][(x + 1) % 16] = "2"
            elif n > 0.96:
                g[y][x] = "E"
    for (x, y) in [(3, 4), (11, 10)]:
        x, y = (x + seed * 5) % 15, (y + seed * 3) % 15
        g[y][x] = "1"
        g[y][x + 1] = "1"
    g[(7 + seed) % 16][(13 + seed) % 16] = "6"
    return grid("rock", "\n".join("".join(r) for r in g))


FLOORS = {
    "terracotta": OA.FLOORS["terracotta"],
    "boards": OA.FLOORS["boards"],
    "flags": OA.FLOORS["flags"],
    "earth": floor_variants("earth", _earth(3, [(3, 4), (11, 10), (13, 2)], [(5, 8), (6, 8), (7, 9), (8, 9)]),
                            _earth(11, [(9, 5), (2, 12)], [])),
    "slate": floor_variants("slate", _slate(0), _slate(1)),
    "darkboards": floor_variants("darkboards", _darkboards(0), _darkboards(1)),
    "straw": floor_variants("straw", _straw(0), _straw(5)),
    "charearth": floor_variants("charearth", _charearth(0), _charearth(1)),
}

# --------------------------------------------------------------------------
# Walls. A style is a list of courses, top to bottom; each course is a list of
# 16x16 variants, picked by x. A wall n cells tall draws course 0 on its top
# row, the last course on its bottom row, and the middle courses between
# (arkrooms_build.compose()).
# --------------------------------------------------------------------------

def _boulders(W, H, masses, tones, seed, p=2.6):
    """A rock face drawn as rounded masses, painted top row first so lower
    masses overlap the ones above, each lit along its top and left, dark along
    its underside, outlined dark below. The gaps are the deepest shadow. Wraps
    in x, so the face tiles across a wall. tones: (gap, dark, mid, lit, top).
    Returns a character grid."""
    gap, dark, mid, lit, top = tones
    g = [[gap] * W for _ in range(H)]
    for (cx, cy, rx, ry) in sorted(masses, key=lambda m: m[1]):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            if not 0 <= y < H:
                continue
            for xx in range(int(cx - rx) - 1, int(cx + rx) + 2):
                nx, ny = (xx - cx) / rx, (y - cy) / ry
                d = abs(nx) ** p + abs(ny) ** p
                if d > 1.0:
                    continue
                x = xx % W
                rough = (noise(x, y, seed) - 0.5) * 0.18
                if d > 0.80 + rough and ny > -0.2:
                    c = "k" if ny > 0.35 else dark
                elif ny < -0.62 + rough:
                    c = top
                elif ny < -0.25 + rough or nx < -0.7:
                    c = lit
                elif ny > 0.45 + rough or nx > 0.75:
                    c = dark
                else:
                    c = mid
                    if noise(x, y, seed + 7) < 0.05:
                        c = dark
                g[y][x] = c
    return g



def _cells(g, pal, rows):
    """Split a character grid (rows of 16*n chars) into course lists."""
    img = grid(pal, "\n".join("".join(r) for r in g))
    W = img.shape[1] // 16
    return [[img[r * 16:(r + 1) * 16, i * 16:(i + 1) * 16] for i in range(W)] for r in range(rows)]


def _rock_wall():
    """The Styx's black cliff as a wall: blue-black facets, wet streaks running
    down them, drips glinting, a puddle-dark foot. Three courses, three cells
    wide, so the face doesn't repeat."""
    W, H = 48, 48
    g = [["2"] * W for _ in range(H)]
    # the cliff splits into tall slabs: each lit down its left edge, dark down
    # its right, broken across by fractures at its own heights
    widths = [7, 5, 8, 6, 4, 7, 6, 5]
    x0 = 0
    for i, wdt in enumerate(widths):
        breaks = sorted({4 + int(noise(i, j, 77) * 40) for j in range(3)})
        for x in range(x0, x0 + wdt):
            for y in range(H):
                if x == x0 + wdt - 1:
                    c = "1"
                elif x == x0:
                    c = "3"
                elif x == x0 + wdt - 2 and wdt > 4:
                    c = "1" if noise(x, y, 5) < 0.3 else "2"
                else:
                    c = "2" if noise(x, y, i) > 0.06 else "1"
                g[y][x] = c
        for by in breaks:
            shift = 1 if noise(i, by, 3) < 0.5 else -1
            for x in range(x0, x0 + wdt):
                yy = by + (shift if x > x0 + wdt // 2 else 0)
                if 0 <= yy < H - 1:
                    g[yy][x] = "1"
                    g[yy + 1][x] = "3" if x < x0 + wdt - 1 else "1"
        x0 += wdt
    # wet streaks: thin lines of sheen down the faces, a glint at their heads
    for sx in (3, 14, 22, 31, 43):
        top = 3 + int(noise(sx, 0, 9) * 14)
        for y in range(top, H - 4):
            if g[y][sx] in "23":
                g[y][sx] = "4" if noise(sx, y, 3) < 0.75 else "3"
        g[top][sx] = "5"
    for (x, y) in [(19, 12), (38, 26), (9, 27), (28, 38), (41, 10)]:
        g[y][x] = "5"
    # the ceiling edge, and the wet foot of the wall
    for x in range(W):
        g[0][x] = "k"
        g[1][x] = "1"
        g[H - 1][x] = "k"
        g[H - 2][x] = "1"
        g[H - 3][x] = "4" if noise(x, H, 5) < 0.25 else ("1" if noise(x, H, 6) < 0.5 else g[H - 3][x])
    return _cells(g, "rock", 3)


def _outcrop_wall():
    """Arkadia's grey limestone, where the Asclepeion is built against the
    outcrop: pale facets, moss in the joints near the top, a timber plate along
    the ceiling for the herbs (its own 8 px band, the wall palette's beams)."""
    W, H = 48, 32
    masses = [(5, 9, 10, 6), (24, 8, 12, 6), (42, 10, 9, 6),
              (14, 19, 11, 7), (33, 20, 11, 7), (48, 21, 6, 6),
              (5, 29, 9, 5), (23, 30, 10, 5), (40, 30, 9, 5)]
    g = _boulders(W, H, masses, ("6", "7", "7", "8", "9"), 17, p=2.2)
    # moss on the upward faces and in the joints near the top
    for y in range(0, H):
        for x in range(W):
            if g[y][x] == "9" and noise(x, y, 5) < 0.45:
                g[y][x] = "M" if noise(x, y, 6) < 0.6 else "m"
            elif g[y][x] == "6" and y < 16 and noise(x, y, 4) < 0.35:
                g[y][x] = "m"
    for x in range(W):
        g[H - 1][x] = "k"
        g[H - 2][x] = "6"
    courses = _cells(g, "rock", 2)
    beam = Canvas(16, 8)                         # a full 8 px band, so no tile mixes palettes
    for y, col in enumerate(["k", "1", "3", "3", "2", "2", "1", "k"]):
        beam.hline(0, 15, y, col)
    beam.put(5, 3, "2")
    beam.put(12, 4, "1")
    beam_img = beam.img("wall")
    for i, cell in enumerate(courses[0]):
        c = cell.copy()
        c[0:8] = beam_img[0:8]
        courses[0][i] = c
    return courses


def _nonakris_wall():
    """Nonakris's houses: a ceiling of stone slabs (their ends show as a band of
    grey blocks under the black), whitewash, and a footing of rubble where the
    damp comes through. The slab band and the footing are 8 px rock bands, the
    whitewash between them the wall palette."""
    top = Canvas(16, 16)
    top.hline(0, 15, 0, "k")
    for x in range(16):                          # slab ends, two per cell
        bx = x % 8
        for y in range(1, 7):
            if bx == 7:
                c = "6"
            elif y == 1:
                c = "8"
            elif y == 6:
                c = "6"
            else:
                c = "7" if noise(x, y, 2) > 0.1 else "8"
            top.put(x, y, c)
    top.hline(0, 15, 7, "k")
    top_rock = top.img("rock")
    ww = Canvas(16, 16)
    for y in range(8, 16):
        for x in range(16):
            ww.put(x, y, "S" if y == 8 else ("s" if y == 9 else "p"))
    for (x, y, c) in [(3, 12, "w"), (10, 14, "s"), (13, 11, "w"), (6, 15, "s")]:
        ww.put(x, y, c)
    upper = over(top_rock, ww.img("wall"))
    lo = Canvas(16, 16)
    for y in range(0, 8):
        for x in range(16):
            lo.put(x, y, "p")
    # the damp creeping up from the footing
    for x in range(16):
        h = 1 + int(noise(x // 3, 1, 8) * 3)
        for y in range(8 - h, 8):
            lo.put(x, y, "s" if y < 7 else "S")
    for (x, y, c) in [(2, 1, "s"), (9, 3, "w"), (13, 2, "s")]:
        lo.put(x, y, c)
    wl = lo.img("wall")
    foot = Canvas(16, 16)
    rubble = [
        "k6777k67786k7776",
        "67887677887676887",
        "6777667778766777",
        "k666k66666kk6666",
        "778k6778876k6787",
        "6787667786766778",
        "6666e6666666e666",
        "kkkkkkkkkkkkkkkk",
    ]
    for dy, row in enumerate(rubble):
        for dx, c in enumerate(row[:16]):
            foot.put(dx, 8 + dy, c)
    lower = over(wl, foot.img("rock"))
    return [[upper], [lower]]


def _planks_wall():
    """Kepheus's lean-to: rough vertical boards nailed to a purlin, gaps of dark
    between some of them, all the wood palette's furniture browns."""
    g = Canvas(16, 32)
    g.hline(0, 15, 0, "k")
    for y in range(1, 5):
        g.hline(0, 15, y, ["d", "l", "m", "d"][y - 1])
    g.hline(0, 15, 5, "k")
    widths = [5, 4, 4, 3]
    x = 0
    for i, wdt in enumerate(widths):
        for xx in range(x, x + wdt):
            for y in range(6, 31):
                if xx == x + wdt - 1:
                    c = "k" if i % 2 == 0 else "d"
                elif xx == x:
                    c = "l"
                else:
                    c = "m" if noise(xx, y, i) > 0.08 else "d"
                g.put(xx, y, c)
        g.put(x + 1, 9, "k")
        g.put(x + 1, 26, "k")
        x += wdt
    g.hline(0, 15, 31, "k")
    img = g.img("wood")
    return [[img[:16]], [img[16:]]]


def _timber_wall():
    """Arkadia's timber: horizontal cypress planks, red-brown, under a heavy
    beam; posts every two cells (the agora stall and the Asclepeion's side)."""
    def course(post, top):
        c = Canvas(16, 16)
        for y in range(16):
            for x in range(16):
                row = y % 5
                if row == 4:
                    ch = "D"
                elif row == 0:
                    ch = "r"
                else:
                    ch = "R" if noise(x, y, 12) > 0.08 else "D"
                c.put(x, y, ch)
        if top:
            c.hline(0, 15, 0, "k")
            for y in range(1, 6):
                c.hline(0, 15, y, ["1", "3", "2", "2", "1"][y - 1])
            c.hline(0, 15, 6, "k")
        else:
            c.hline(0, 15, 15, "k")
            c.hline(0, 15, 14, "D")
        if post:
            for y in range(7 if top else 0, 15 if not top else 16):
                c.put(1, y, "k")
                c.put(2, y, "3")
                c.put(3, y, "2")
                c.put(4, y, "1")
                c.put(5, y, "k")
        return c.img("wall")
    return [[course(True, True), course(False, True)], [course(True, False), course(False, False)]]


def _arkwhite_wall():
    """Klymene's bright upper room: whitewash between cypress-red posts and a
    red beam, a sapwood-ochre line at the skirting."""
    up = Canvas(16, 16)
    up.hline(0, 15, 0, "k")
    for y, c in enumerate(["r", "r", "R", "D"], start=1):
        up.hline(0, 15, y, c)
    up.hline(0, 15, 5, "k")
    for y in range(6, 16):
        up.hline(0, 15, y, "w" if y == 6 else "p")
    for (x, y, c) in [(4, 10, "w"), (11, 13, "s"), (14, 8, "w")]:
        up.put(x, y, c)
    lo = Canvas(16, 16)
    for y in range(16):
        lo.hline(0, 15, y, "p")
    lo.hline(0, 15, 11, "s")
    lo.hline(0, 15, 12, "o")
    lo.hline(0, 15, 13, "R")
    lo.hline(0, 15, 14, "D")
    lo.hline(0, 15, 15, "k")
    for (x, y, c) in [(5, 3, "w"), (12, 6, "s")]:
        lo.put(x, y, c)
    up_post, lo_post = Canvas(16, 16), Canvas(16, 16)
    for cv, src in ((up_post, up), (lo_post, lo)):
        cv.g = [r[:] for r in src.g]
    for y in range(5, 16):
        for (x, c) in ((6, "k"), (7, "r"), (8, "R"), (9, "k")):
            up_post.put(x, y, c)
    for y in range(0, 15):
        for (x, c) in ((6, "k"), (7, "r"), (8, "R"), (9, "k")):
            lo_post.put(x, y, c)
    return [[up.img("wall"), up.img("wall"), up_post.img("wall")],
            [lo.img("wall"), lo.img("wall"), lo_post.img("wall")]]


def _smoke_wall():
    """Nyktimos's hall: squared logs laid flat, smoke-blackened toward the top,
    the dark Arkadian timber gone almost black, chinked with grey."""
    g = Canvas(32, 32)
    for y in range(32):
        for x in range(32):
            row = (y - 2) % 6
            if row == 5:
                c = "k"
            elif row == 4:
                c = "1"
            elif row == 0:
                c = "R" if y > 12 else "D"
            else:
                c = "D"
                if y > 12 and noise(x, y, 21) < 0.08:
                    c = "R"
                if y < 12 and noise(x, y, 22) < 0.25:
                    c = "1"
            g.put(x, y, c)
    # the log ends' checks and an old peg
    for (x, y) in [(9, 9), (10, 9), (24, 21), (25, 21), (4, 27)]:
        g.put(x, y, "k")
    g.put(18, 15, "3")
    g.put(18, 16, "2")
    g.hline(0, 31, 0, "k")
    g.hline(0, 31, 31, "k")
    for (x, y) in [(5, 8), (21, 20), (12, 26), (28, 14)]:
        g.put(x, y, "k")
    img = g.img("wall")
    return [[img[0:16, 0:16], img[0:16, 16:32]], [img[16:32, 0:16], img[16:32, 16:32]]]


def _earthlog_wall():
    """Hippothoos's hut is dug half into the hill: the back wall is earth,
    shored with round logs laid one on another between upright posts."""
    g = Canvas(48, 32)
    for y in range(32):
        for x in range(48):
            n = noise(x, y, 33)
            g.put(x, y, "e" if n < 0.55 else ("E" if n < 0.9 else "2"))
    # three logs laid across, each 6 px tall, with gaps of earth between
    for ly in (4, 13, 22):
        for x in range(48):
            for dy, c in enumerate(["k", "h", "E", "E", "e", "k"]):
                g.put(x, ly + dy, c)
            if x % 11 == 3:
                g.put(x, ly + 2, "e")
        # cut log ends at the posts
    for px in (2, 26):
        for y in range(0, 32):
            for (dx, c) in ((0, "k"), (1, "E"), (2, "h"), (3, "E"), (4, "e"), (5, "k")):
                g.put(px + dx, y, c)
        for y in (9, 18, 27):
            g.put(px + 2, y, "e")
    for x in range(48):
        g.put(x, 0, "k")
        g.put(x, 31, "k")
        g.put(x, 30, "e")
    for (x, y) in [(15, 2), (38, 11), (9, 20), (33, 29), (44, 19)]:
        g.put(x, y, "7")
    img = g.img("rock")
    return [[img[0:16, i * 16:(i + 1) * 16] for i in range(3)],
            [img[16:32, i * 16:(i + 1) * 16] for i in range(3)]]


def _byre_wall():
    """Krotos's house and byre: a heavy beam with rafter ends over daub that has
    flaked to show the wattle in places, on a footing of field stones. Daub and
    wattle are 8 px bands in the wall palette; the footing a rock band."""
    up = Canvas(16, 16)
    up.hline(0, 15, 0, "k")
    for y, c in enumerate(["2", "3", "2", "1"], start=1):
        up.hline(0, 15, y, c)
    for x in range(16):
        up.put(x, 5, "k" if x % 8 in (2, 3, 4, 5) else "S")
        up.put(x, 6, "1" if x % 8 in (3, 4) else "s")
        up.put(x, 7, "s")
    for y in range(8, 16):
        for x in range(16):
            up.put(x, y, "p" if noise(x, y, 44) > 0.06 else "s")
    # a flake of daub gone, the wattle showing
    for (x, y, c) in [(10, 10, "S"), (11, 10, "2"), (12, 10, "S"), (10, 11, "2"), (11, 11, "1"), (12, 11, "2"),
                      (10, 12, "S"), (11, 12, "2"), (12, 12, "S"), (13, 11, "S"), (9, 11, "S")]:
        up.put(x, y, c)
    lo = Canvas(16, 16)
    for y in range(8):
        for x in range(16):
            lo.put(x, y, "p" if noise(x, y, 45) > 0.08 else "s")
    lo.hline(0, 15, 7, "S")
    for (x, y, c) in [(3, 3, "o"), (4, 3, "o"), (12, 5, "s")]:
        lo.put(x, y, c)
    foot = Canvas(16, 16)
    stones = [
        "k8877kk7887k8777",
        "8777768777768777",
        "7766677666767666",
        "k666k6666k6k6666",
        "77k8877k877k8877",
        "7667767767767667",
        "6666666e66666666",
        "kkkkkkkkkkkkkkkk",
    ]
    for dy, row in enumerate(stones):
        for dx, c in enumerate(row[:16]):
            foot.put(dx, 8 + dy, c)
    return [[up.img("wall")], [over(lo.img("wall"), foot.img("rock"))]]


WALLS = {
    "rock": _rock_wall(),
    "outcrop": _outcrop_wall(),
    "nonakris": _nonakris_wall(),
    "planks": _planks_wall(),
    "timber": _timber_wall(),
    "arkwhite": _arkwhite_wall(),
    "smoke": _smoke_wall(),
    "earthlog": _earthlog_wall(),
    "byre": _byre_wall(),
}

VOID = grid("wall", "\n".join(["k" * 16] * 16))

# --------------------------------------------------------------------------
# Stamps. A stamp is a whole number of cells. Its art goes on the middle layer
# (drawn under walkers), its `top` art on the top layer (over walkers), and its
# `flat` art into the bottom layer over the floor or wall (the flat art and the
# base must share a palette in every 8x8 tile).
# --------------------------------------------------------------------------

STAMPS = {}


def _art(parts, w, h):
    """parts: a grid string, an RGBA array, a Canvas, or a list of
    (palette, grid or Canvas) or arrays, overlaid in order."""
    if parts is None:
        return None
    if isinstance(parts, np.ndarray):
        assert parts.shape[:2] == (h * 16, w * 16), (parts.shape, w, h)
        return parts
    out = blank(w, h)
    for p in parts:
        if isinstance(p, np.ndarray):
            img = p
        else:
            pal, text = p
            if isinstance(text, Canvas):
                text = text.text()
            img = grid(pal, text, w * 16, h * 16)
        assert img.shape[:2] == (h * 16, w * 16), (img.shape, w, h)
        out = over(out, img)
    return out


def stamp(name, w, h, art=None, top=None, flat=None, walk=(), behavior=None, note="", pal=""):
    """w, h in cells. art/top/flat: see _art. walk: cells (cx, cy) a walker may
    stand on. behavior: {(cx, cy): 'MB_...'}."""
    assert name not in STAMPS, f"stamp {name} defined twice"
    STAMPS[name] = {
        "w": w, "h": h,
        "img": _art(art, w, h) if art is not None else blank(w, h),
        "top": _art(top, w, h),
        "flat": _art(flat, w, h),
        "walk": set(walk),
        "behavior": dict(behavior or {}),
        "note": note,
        "pal": pal,
    }
    return STAMPS[name]


def reuse(name, oikia_name=None, note=None, **kw):
    """Register one of oikia's pieces as it is drawn (its colors are in these
    palettes)."""
    src = OA.STAMPS[oikia_name or name]
    return stamp(name, src["w"], src["h"], art=src["img"].copy(),
                 top=None if src["top"] is None else src["top"].copy(),
                 walk=kw.get("walk", src["walk"]), behavior=kw.get("behavior", src["behavior"]),
                 note=note or src["note"] + " (oikia)", pal=src["pal"])


# Pieces shared with oikia, unchanged.
for _n in ("window", "kline", "klismos_r", "klismos_l", "stool", "table", "table_round", "desk",
           "amphora", "amphora_plain", "pithos", "pots", "mortar", "hearth", "soot", "kalathos",
           "lampstand", "chest", "herbs", "loom", "jar_shelf"):
    reuse(_n)
reuse("mat", walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"})
