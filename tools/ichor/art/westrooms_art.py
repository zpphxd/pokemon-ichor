#!/usr/bin/env python3
"""Pixel art for the nine interiors of the road west (Act II batch 2):
Lebadeia's pilgrims' hall, Herkyna's and the mason's houses; Kirrha's inn,
Agora stall, the muleteer's and the old sweeper's houses; Aigion's old
Achaean's and goatherd's houses.

The base of the art: the seven palettes, the drawing helpers, the floors, the
walls and the stamp registry. The furniture lives in three more modules, which
register their stamps here when imported:

  westrooms_lebadeia.py  the gorge hamlet: rock, river water, stone dust
  westrooms_kirrha.py    the harbor: sailcloth, boats, rope, mules, brooms
  westrooms_aigion.py    the Achaean shore: the ship frieze, goats and cheese

Everything is drawn as character grids (one character per color, '.' clear) in
the style of oikia_art.py and thyrsa_rooms_art.py, or with the small Canvas
below for the shapes that are easier to plot. Each 8x8 tile must take all its
colors from one palette; westrooms_build.py checks that.

Three looks, one per town:
  Lebadeia  whitewash over a band of Herkyna's river-wave, on a footing of grey
            Parnassian limestone; the pilgrims' hall is cut into bare rock.
  Kirrha    harbor whitewash over a sea-blue dado with a rope moulding under
            tarred beams; the stall is a tarred fishing shed, the stable a hay
            loft.
  Aigion    a painted frieze of numbered black ships on cream, like a vase;
            the goatherd's back wall is the living hillside.
"""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import oikia_art as OA  # noqa: E402  (four palettes, floors and a few pieces, reused as drawn)

INK = OA.INK  # (40, 24, 24)

# --------------------------------------------------------------------------
# Palettes. Multiples of 8, none an aethos color (the builder checks), so
# Porytiles can only place these tiles in palettes 6-12. Four are oikia's, so
# its floors and some of its furniture are reused exactly as drawn.
# --------------------------------------------------------------------------

PALETTES = {
    # plaster, beams, the painted dado, shutters and sky (oikia's)
    "wall": dict(OA.PALETTES["wall"]),
    # terracotta, boards, limestone (oikia's; no ink: floors are opaque)
    "floor": dict(OA.PALETTES["floor"]),
    # furniture woods, linen and sailcloth, red and blue cloth, bronze fittings
    "wood": dict(OA.PALETTES["wood"]),
    # pottery, the hearth's stone and fire, soot, white slip, honey (oikia's);
    # the black ships of Tisamenos's frieze are painted in it, like a vase
    "clay": dict(OA.PALETTES["clay"]),
    # leaves, wicker, straw and hay, rope and wool, and a mule's greys
    "nature": {
        "k": INK,
        "G": (40, 72, 48),     # leaf, dark
        "g": (72, 120, 56),    # leaf
        "v": (120, 168, 80),   # leaf, lit
        "V": (184, 216, 128),  # leaf, highlight
        "w": (248, 248, 232),  # fleece, bone, feather
        "K": (120, 88, 48),    # wicker, dark; hay shadow
        "j": (176, 136, 72),   # wicker; hay
        "J": (224, 192, 128),  # wicker, lit; straw
        "n": (208, 184, 144),  # rope, wool shade
        "d": (136, 56, 32),    # pot, dark
        "m": (192, 96, 56),    # pot
        "M": (80, 64, 64),     # mule, dark
        "u": (128, 112, 104),  # mule
        "U": (176, 160, 152),  # mule, muzzle; ash
    },
    # bronze, flame, water, marble (oikia's)
    "bronze": dict(OA.PALETTES["bronze"]),
    # rough stone and living rock, timber and tar, lichen, lamp glow
    "stone": {
        "k": INK,
        "1": (56, 48, 48),     # joint, deepest shadow
        "2": (88, 80, 72),     # stone, dark
        "3": (120, 112, 104),  # stone
        "4": (152, 144, 128),  # stone, lit
        "5": (184, 176, 160),  # stone, highlight
        "6": (224, 216, 200),  # stone, glint; stone dust
        "e": (72, 56, 48),     # timber, dark; tar
        "E": (112, 80, 56),    # timber
        "h": (152, 112, 72),   # timber, lit
        "m": (96, 104, 80),    # lichen, moss
        "M": (136, 144, 104),  # lichen, lit
        "l": (232, 160, 72),   # lamp glow
        "L": (248, 216, 136),  # lamp glow, bright
    },
}

# The order the builder hands these to Porytiles as packing hints.
PALETTE_ORDER = ["wall", "floor", "wood", "clay", "nature", "bronze", "stone"]


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


def rows_to_grid(pal, rows):
    return grid(pal, "\n".join("".join(r) for r in rows))


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


class Canvas:
    """A character grid to plot on: one character per pixel, '.' is clear."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def box(self, x0, y0, x1, y1, c):
        self.hl(x0, x1, y0, c)
        self.hl(x0, x1, y1, c)
        self.vl(x0, y0, y1, c)
        self.vl(x1, y0, y1, c)

    def hl(self, x0, x1, y, c):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.px(x, y, c)

    def vl(self, x, y0, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.px(int(round(x0 + (x1 - x0) * i / n)), int(round(y0 + (y1 - y0) * i / n)), c)

    def ell(self, cx, cy, rx, ry, c, fill=True):
        """An ellipse centred on (cx, cy), which may be a half-pixel."""
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                d = ((x - cx) / max(rx, 0.5)) ** 2 + ((y - cy) / max(ry, 0.5)) ** 2
                if fill and d <= 1.0:
                    self.px(x, y, c)
                elif not fill and 0.6 <= d <= 1.15:
                    self.px(x, y, c)

    def outline(self, c="k", inside=None):
        """Ring every filled run with c (on clear pixels next to filled ones)."""
        src = [r[:] for r in self.g]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != ".":
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < self.w and 0 <= yy < self.h and src[yy][xx] not in ".":
                        if inside is None or src[yy][xx] in inside:
                            self.g[y][x] = c
                            break

    def paste(self, art, ox, oy):
        rows = art if isinstance(art, list) else art.strip("\n").split("\n")
        for dy, row in enumerate(rows):
            for dx, c in enumerate(row):
                if c not in ". ":
                    self.px(ox + dx, oy + dy, c)

    def replace(self, a, b, region=None):
        x0, y0, x1, y1 = region or (0, 0, self.w - 1, self.h - 1)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.get(x, y) == a:
                    self.px(x, y, b)

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
    "earth": ("floor", {"W": "m", "m": "n", "n": "j", "u": "v", "j": "g", "x": "u", "L": "l", "l": "y",
                        "y": "q"}),
    "stone": ("stone", {"6": "5", "5": "4", "4": "3", "3": "2", "2": "1", "1": "k", "M": "m", "m": "2",
                        "h": "E", "E": "e", "e": "1"}),
    "nature": ("nature", {"J": "j", "j": "K", "K": "M", "n": "j", "w": "n", "v": "g", "g": "G"}),
}


def _shade(img, material, mask):
    pal, m = SHADE[material]
    dark = recolor(img, pal, m)
    out = img.copy()
    out[mask] = dark[mask]
    return out


def floor_variants(shade_as, base, alt=None):
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    out = {"plain": base, "top": _shade(base, shade_as, top), "left": _shade(base, shade_as, left),
           "corner": _shade(base, shade_as, top | left)}
    if alt is not None:
        out["alt"] = alt
    return out


def _earth(seed, pebbles, crack, chips=()):
    """Packed earth in board browns, soft dusty patches, pebbles, a crack.
    chips: (x, y) pale flakes of cut limestone (the mason's floor)."""
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
        g[(y + 1) % 16][x] = "j"
    for (x, y) in crack:
        g[y][x] = "j"
    for (x, y, c) in chips:
        g[y][x] = c
    return rows_to_grid("floor", g)


def floor_rockcut(seed=0):
    """The pilgrims' hall's floor, cut out of the hill: one broad slab of the
    same grey limestone as the wall per cell, the joints where one day's cut
    met the next, worn smooth down the middle by pilgrims' feet. seed 1: a
    slab with an old crack across it."""
    g = [["4"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if x == 15 or y == 15:
                g[y][x] = "3"
            elif x == 0 or y == 0:
                g[y][x] = "5"
            elif noise(x, y, 33) < 0.05:
                g[y][x] = "3"
            elif noise(x, y, 34) > 0.96:
                g[y][x] = "5"
    if seed:
        for (x, y) in [(3, 2), (4, 3), (5, 3), (6, 4), (7, 5), (7, 6), (8, 7), (9, 7), (10, 8)]:
            g[y][x] = "2"
            g[y + 1][x] = "5"
    else:
        for (x, y) in [(5, 6), (11, 10)]:
            g[y][x] = "3"
            g[y][x + 1] = "3"
    return rows_to_grid("stone", g)


def floor_pebbles(seed=0, light=False):
    """River pebbles set in mortar: Herkyna's floor, laid with stones from the
    river under the house (light: Kirrha's courtyard, in bigger sun-bleached
    cobbles). A periodic Voronoi so it tiles."""
    pts = []
    k = 0
    while len(pts) < (5 if light else 7):
        x, y = int(noise(k, 1, seed) * 16), int(noise(1, k, seed + 3) * 16)
        k += 1
        if all(min(abs(x - px), 16 - abs(x - px)) ** 2 + min(abs(y - py), 16 - abs(y - py)) ** 2 >
               (22 if light else 14) for px, py in pts):
            pts.append((x, y))
    tones = "5455" if light else "4544"

    def owner(x, y):
        best, bi = None, 0
        for i, (sx, sy) in enumerate(pts):
            dx = min(abs(x - sx), 16 - abs(x - sx))
            dy = min(abs(y - sy), 16 - abs(y - sy))
            d = dx * dx + dy * dy
            if best is None or d < best:
                best, bi = d, i
        return bi
    own = [[owner(x, y) for x in range(16)] for y in range(16)]
    g = [["3"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            o = own[y][x]
            edge = (own[y][(x + 1) % 16] != o or own[(y + 1) % 16][x] != o)
            lit = (own[(y - 1) % 16][x] != o or own[y][(x - 1) % 16] != o)
            if edge:
                g[y][x] = "3"
            elif lit:
                g[y][x] = "6" if light else "5"
            else:
                g[y][x] = tones[o % 4]
            if not light and o % 4 == 1 and not edge and not lit and noise(x, y, 5) < 0.5:
                g[y][x] = "M"
    return rows_to_grid("stone", g)


def floor_reeds(seed=0):
    """Reed matting, plaited in a herringbone, the mats' edges bound with a
    darker cord every half-cell."""
    g = []
    for y in range(16):
        row = []
        for x in range(16):
            if y % 8 == 7:
                row.append("K")
            else:
                u = (x + (y if (y // 8 + seed) % 2 else -y)) % 4
                row.append("J" if u < 2 else "j")
        g.append(row)
    for (x, y) in [(5, 3), (12, 10)]:
        g[y][x] = "n"
    return rows_to_grid("nature", g)


def floor_straw(seed=0):
    """Stable straw over beaten earth: loose golden stalks lying every which
    way, a little darker where it's trodden in."""
    g = [["j"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            n = noise(x // 2, y // 2, 40 + seed)
            if n < 0.18:
                g[y][x] = "K"
    for i in range(18):
        x0 = int(noise(i, 2, seed) * 16)
        y0 = int(noise(2, i, seed) * 16)
        dx = 1 if noise(i, i, seed) < 0.5 else -1
        flat = noise(i, 7, seed) < 0.6
        for t in range(4):
            g[(y0 + (0 if flat else t // 2)) % 16][(x0 + dx * t) % 16] = "J"
    return rows_to_grid("nature", g)


def floor_planks():
    """Ship's planking, narrow and tarred at the seams, pegged with treenails:
    an old Achaean floors his house with what he knows."""
    g = []
    for y in range(16):
        row = []
        for x in range(16):
            if x % 4 == 3:
                row.append("j")
            elif x % 4 == 0:
                row.append("W")
            else:
                row.append("m" if (x + y) % 7 else "n")
        g.append(row)
    for (x, y) in [(1, 2), (5, 10), (9, 4), (13, 12), (2, 9), (10, 14)]:
        g[y][x] = "j"
    for (x0, y0) in [(4, 6), (12, 1)]:      # butt joints, staggered
        for x in range(x0, x0 + 3):
            g[y0][x] = "j"
    return rows_to_grid("floor", g)


def floor_cave(seed=0):
    """The goatherd's cave half: the hill's own rock, worn level, with
    beaten earth in the hollows."""
    g = [["3"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            n = noise(x // 4, y // 4, 60 + seed)
            n2 = noise(x, y, 61 + seed)
            if n < 0.35:
                g[y][x] = "E" if n2 < 0.85 else "e"
            else:
                g[y][x] = "3" if n2 < 0.8 else "4"
            if n2 > 0.97:
                g[y][x] = "2"
    return rows_to_grid("stone", g)


FLOORS = {
    "terracotta": OA.FLOORS["terracotta"],
    "boards": OA.FLOORS["boards"],
    "flags": OA.FLOORS["flags"],
    "earth": floor_variants("earth", _earth(3, [(3, 4), (11, 10), (13, 2)], [(5, 8), (6, 8), (7, 9), (8, 9)]),
                            _earth(11, [(9, 5), (2, 12)], [])),
    "chips": floor_variants("earth",
                            _earth(5, [(4, 9)], [], [(11, 6, "L"), (12, 6, "l")]),
                            _earth(9, [], [(3, 6), (4, 6)], [(5, 11, "L")])),
    "rockcut": floor_variants("stone", floor_rockcut(0), floor_rockcut(1)),
    "pebbles": floor_variants("stone", floor_pebbles(0), floor_pebbles(7)),
    "cobbles": floor_variants("stone", floor_pebbles(2, True), floor_pebbles(9, True)),
    "reeds": floor_variants("nature", floor_reeds(0), floor_reeds(1)),
    "straw": floor_variants("nature", floor_straw(0), floor_straw(1)),
    "planks": floor_variants("boards", floor_planks()),
    "cave": floor_variants("stone", floor_cave(0), floor_cave(1)),
}

# --------------------------------------------------------------------------
# Walls. A style is a list of courses, top to bottom; each course is a list of
# 16x16 variants, picked by x. A wall n cells tall draws the style's last n
# courses (a taller run repeats the top course).
# --------------------------------------------------------------------------


def _beam(rows, lit="3", mid="2", dark="1", ends=True):
    rows.append("k" * 16)
    rows.append(mid * 16)
    rows.append(lit * 16)
    rows.append(mid * 16)
    rows.append(dark * 16)
    if ends:
        rows.append("s23321sss23321ss")
        rows.append("s12211sss12211ss")
        rows.append("ps1111spps1111sp")
        rows.append("pppssssppppssssp")


def _leb_wall():
    """Lebadeia: a plane-wood beam over whitewash; under it Herkyna's river in
    a band of blue running waves, then a footing of grey Parnassian limestone
    laid in courses."""
    up = []
    _beam(up)
    for _ in range(9, 16):
        up.append("p" * 16)
    up = [list(r) for r in up]
    for (x, y, c) in [(4, 11, "w"), (12, 13, "s"), (9, 10, "w"), (1, 14, "s")]:
        up[y][x] = c
    upper = rows_to_grid("wall", up)
    WAVE = ["bbbbbbbb",
            "bbbBBbbb",
            "bbBbbBbb",
            "bBbbBbBb",
            "BbbBBbbB",
            "pBBbbbBB"]
    lo = [list("s" * 16), list("o" * 16)]
    for wr in WAVE:
        lo.append(list(wr * 2))
    band = rows_to_grid("wall", lo)
    st = ["1111111111111111",
          "4445444514444451",
          "3334333413333341",
          "3333332413333321",
          "2222221212222221",
          "5444451444514444",
          "3333213333213333",
          "kkkkkkkkkkkkkkkk"]
    foot = grid("stone", "\n".join(st))
    return [[upper], [np.concatenate([band, foot], 0)]]


def _kir_wall():
    """Kirrha: a tarred beam lashed with rope, harbor whitewash, a rope
    moulding over a sea-blue dado, and white wavelets breaking along it."""
    up = []
    up.append("k" * 16)
    up.append("1" * 16)
    up.append("2" * 16)
    up.append("1" * 16)
    up.append("k" * 16)
    up.append("ss1kss1sss1kss1s")   # rope lashings hanging off the beam
    up.append("pp1ppp1ppp1ppp1p")
    up.append("pppppppppppppppp")
    for _ in range(8, 16):
        up.append("p" * 16)
    up = [list(r) for r in up]
    for (x, y, c) in [(3, 10, "w"), (11, 12, "w"), (7, 14, "s"), (14, 9, "s")]:
        up[y][x] = c
    upper = rows_to_grid("wall", up)
    lo = []
    for _ in range(6):
        lo.append("p" * 16)
    lo.append("s" * 16)
    lo.append("1o1o1o1o1o1o1o1o")   # the rope moulding, twisted
    lo.append("o1o1o1o1o1o1o1o1")
    lo.append("1" * 16)
    lo.append("B" * 16)
    for y in range(4):
        lo.append("b" * 16)
    lo.append("k" * 16)
    lo = [list(r) for r in lo]
    for (x, y) in [(2, 12), (3, 11), (4, 11), (5, 12), (10, 12), (11, 11), (12, 11), (13, 12)]:
        lo[y][x] = "B"                           # a running wave, one line of it
    lower = rows_to_grid("wall", lo)
    return [[upper], [lower]]


def _shed_wall():
    """The Agora stall: a fishing shed of tarred planks laid edge to edge,
    a heavy beam along the top with pegs for gear."""
    rows = []
    for y in range(32):
        r = []
        for x in range(16):
            if y < 2:
                r.append("k")
            elif y < 7:
                r.append("h" if y == 3 else ("E" if y < 6 else "e"))
            elif y == 7:
                r.append("k")
            else:
                py = (y - 8) % 6
                if py == 5:
                    r.append("k")
                elif py == 0:
                    r.append("h" if noise(x, y, 3) < 0.6 else "E")
                else:
                    r.append("E" if noise(x // 3, y, 4) < 0.55 else "e")
        rows.append(r)
    for (x, y) in [(3, 4), (12, 4)]:            # pegs in the beam
        rows[y][x] = "k"
        rows[y + 1][x] = "6"
    for (x, y) in [(6, 13), (13, 25), (2, 19)]:  # nail heads
        rows[y][x] = "1"
    for x in range(16):
        rows[31][x] = "k"
    img = rows_to_grid("stone", rows)
    return [[img[:16]], [img[16:]]]


def _rock(seed, warm=False, w=3):
    """Living rock, three cells wide so it doesn't repeat often: limestone
    masses split by bedding planes and joints, lit from the top left, darker
    toward the ceiling. warm: the goatherd's hillside, with moss in the
    cracks and a seep of damp."""
    W, H = 16 * w, 32
    pts = []
    k = 0
    while len(pts) < 9 * w // 3 + 3:
        x, y = int(noise(k, 7, seed) * W), int(noise(7, k, seed) * H)
        k += 1
        if all(min(abs(x - px), W - abs(x - px)) ** 2 + ((y - py) * 1.6) ** 2 > 90 for px, py in pts):
            pts.append((x, y))

    def owner(x, y):
        best, bi = None, 0
        for i, (sx, sy) in enumerate(pts):
            dx = min(abs(x - sx), W - abs(x - sx))
            dy = (y - sy) * 1.7               # flattened: bedding runs across
            d = dx * dx + dy * dy
            if best is None or d < best:
                best, bi = d, i
        return bi
    own = [[owner(x, y) for x in range(W)] for y in range(H)]
    g = [["3"] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            o = own[y][x]
            right = own[y][(x + 1) % W]
            down = own[y + 1][x] if y + 1 < H else o
            up = own[y - 1][x] if y > 0 else o
            left = own[y][(x - 1) % W]
            if o != right or o != down:
                g[y][x] = "1"
            elif o != up or o != left:
                g[y][x] = "5"
            else:
                base = "4" if o % 3 == 0 else "3"
                n = noise(x, y, seed + 17)
                g[y][x] = "2" if n < 0.08 else ("5" if n > 0.96 else base)
    for y in range(H - 1, 0, -1):
        for x in range(W):
            if g[y][x] == "1" and g[y - 1][x] in "34":
                g[y - 1][x] = "2"
    # darker toward the ceiling
    for y in range(0, 6):
        for x in range(W):
            if g[y][x] in "45" and noise(x, y, seed + 3) < 0.5 + (6 - y) * 0.08:
                g[y][x] = "3" if g[y][x] == "4" else "4"
            elif g[y][x] == "3" and y < 3:
                g[y][x] = "2"
    if warm:
        for y in range(H):
            for x in range(W):
                if g[y][x] == "1" and noise(x, y, seed + 9) < 0.25:
                    g[y][x] = "m"
                elif g[y][x] == "2" and noise(x, y, seed + 9) < 0.2:
                    g[y][x] = "M" if y > 16 else "m"
                elif g[y][x] == "3" and noise(x // 2, y // 3, seed + 11) < 0.12:
                    g[y][x] = "E"
    g[0] = list("k" * W)
    g[H - 1] = list("k" * W)
    g[H - 2] = ["1" if c != "k" else c for c in g[H - 2]]
    img = rows_to_grid("stone", g)
    upper = [img[0:16, i * 16:(i + 1) * 16] for i in range(w)]
    lower = [img[16:32, i * 16:(i + 1) * 16] for i in range(w)]
    return [upper, lower]


def _rubble():
    """The mason's wall: rough-laid stones, no plaster, eight cells wide so
    no stone repeats. Stones of every size in rough courses, small pinning
    stones in the gaps. Agamedes built it, and left one loose: in the third
    cell from the left on the bottom course, a stone like the rest, with a
    darker gap all round it."""
    W, H = 128, 32
    g = [["1"] * W for _ in range(H)]
    y = 1
    course = 0
    while y < H - 1:
        hgt = 5 + int(noise(course, 2, 4) * 4)
        x = -int(noise(course, 5, 3) * 9)
        while x < W:
            ln = 6 + int(noise(x, course, 8) * 8)
            top = y + int(noise(x, course, 11) * 2)
            bot = min(y + hgt - 1 - int(noise(x, course, 12) * 2), H - 2)
            tone = "34445"[int(noise(x, course, 9) * 5)]
            for yy in range(top, bot + 1):
                for xx in range(x + 1, x + ln):
                    if not 0 <= xx < W:
                        continue
                    corner = (yy in (top, bot)) and (xx in (x + 1, x + ln - 1))
                    if corner:
                        continue
                    if yy == top or xx == x + 1:
                        c = "5" if tone != "5" else "6"
                    elif yy == bot or xx == x + ln - 1:
                        c = "2"
                    else:
                        c = tone if noise(xx, yy, 21) > 0.06 else "3"
                    g[yy][xx] = c
            x += ln
        y += hgt
        course += 1
    for yy in range(1, H - 1):                   # pinning stones wedged in the gaps
        for xx in range(1, W - 1):
            if g[yy][xx] == "1" and g[yy][xx + 1] == "1" and noise(xx, yy, 25) < 0.08:
                g[yy][xx] = "3"
                g[yy][xx + 1] = "2"
    # the loose stone: cell 2's bottom course (x 32-47, y 16-31). Redraw
    # one stone there with a darker gap round it.
    sx0, sy0, sx1, sy1 = 35, 20, 44, 26
    for yy in range(sy0 - 1, sy1 + 2):
        for xx in range(sx0 - 1, sx1 + 2):
            g[yy][xx] = "k" if (yy in (sy0 - 1, sy1 + 1) or xx in (sx0 - 1, sx1 + 1)) else "4"
    for xx in range(sx0, sx1 + 1):
        g[sy0][xx] = "5"
        g[sy1][xx] = "2"
    for yy in range(sy0, sy1 + 1):
        g[yy][sx0] = "5"
        g[yy][sx1] = "2"
    for (xx, yy) in [(sx0 - 1, sy0 - 1), (sx1 + 1, sy0 - 1), (sx0 - 1, sy1 + 1), (sx1 + 1, sy1 + 1)]:
        g[yy][xx] = "1"
    g[0] = list("k" * W)
    g[H - 1] = list("k" * W)
    img = rows_to_grid("stone", g)
    upper = [img[0:16, i * 16:(i + 1) * 16] for i in range(8)]
    lower = [img[16:32, i * 16:(i + 1) * 16] for i in range(8)]
    return [upper, lower]


def _aig_wall():
    """Aigion: rough whitewash under a smoke-dark pole beam, an ochre band
    and a plain earth-red footing: a goatherd's house, not a merchant's."""
    up = []
    up.append("k" * 16)
    up.append("1" * 16)
    up.append("2122212221222122")
    up.append("1" * 16)
    up.append("S" * 16)
    up.append("sssSsssssSssssss")
    for _ in range(6, 16):
        up.append("p" * 16)
    up = [list(r) for r in up]
    for (x, y, c) in [(2, 8, "s"), (9, 9, "w"), (13, 12, "s"), (5, 14, "s"), (11, 7, "s")]:
        up[y][x] = c
    upper = rows_to_grid("wall", up)
    lo = []
    for _ in range(7):
        lo.append("p" * 16)
    lo.append("s" * 16)
    lo.append("o" * 16)
    lo.append("o" * 16)
    lo.append("s" * 16)
    for _ in range(4):
        lo.append("R" * 16)
    lo.append("k" * 16)
    lo = [list(r) for r in lo]
    for (x, y, c) in [(4, 2, "s"), (12, 4, "w"), (7, 12, "D"), (13, 13, "D"), (2, 14, "D")]:
        lo[y][x] = c
    lower = rows_to_grid("wall", lo)
    return [[upper], [lower]]


def _loft():
    """The muleteer's stable: the hay loft over the stalls, seen from below.
    Hay heaped on the loft floor, loose and golden, spilling over its front
    beam, and the dark under it where the mules stand."""
    rows = []
    for y in range(32):
        r = []
        for x in range(16):
            if y < 1:
                r.append("k")
            elif y < 16:
                # heaped hay: soft mounds, stalks catching the light
                hump = 3 + 2 * math.sin((x + 3) / 2.6) + math.sin(x / 1.3)
                if y < 1 + hump * 0.6:
                    r.append("M")
                else:
                    n = noise(x, y, 7)
                    r.append("J" if n < 0.35 else ("j" if n < 0.85 else "K"))
            elif y < 17:
                r.append("K")
            elif y < 21:
                r.append("j" if y == 17 else ("K" if y < 20 else "M"))  # the loft's front beam
            elif y < 31:
                r.append("M")                                     # the dark under the loft
            else:
                r.append("k")
        rows.append(r)
    for x in range(16):                                           # hay wisps hanging over the beam
        if noise(x, 1, 5) < 0.45:
            ln = 1 + int(noise(x, 2, 5) * 4)
            for t in range(ln):
                rows[21 + t][x] = "J" if t == 0 else "j"
            rows[16][x] = "J"
    for (x, y) in [(4, 18), (11, 18)]:                            # pegs in the beam
        rows[y][x] = "k"
    img = rows_to_grid("nature", rows)
    return [[img[:16]], [img[16:]]]


WALLS = {
    "leb": _leb_wall(),
    "kir": _kir_wall(),
    "shed": _shed_wall(),
    "rock": _rock(5),
    "hill": _rock(12, warm=True),
    "rubble": _rubble(),
    "aig": _aig_wall(),
    "loft": _loft(),
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
    """parts: a grid string, an RGBA array, or a list of (palette, grid),
    Canvas or arrays overlaid in order."""
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


def stamp(name, w, h, art=None, top=None, flat=None, walk=(), behavior=None, note=""):
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
    }
    return STAMPS[name]


def reuse(name, oikia_name=None, note=None, **kw):
    """Register one of oikia's pieces as it is drawn (its colors are in these
    palettes)."""
    src = OA.STAMPS[oikia_name or name]
    return stamp(name, src["w"], src["h"], art=src["img"].copy(),
                 top=None if src["top"] is None else src["top"].copy(),
                 walk=kw.get("walk", src["walk"]), behavior=kw.get("behavior", src["behavior"]),
                 note=note or src["note"] + " (oikia)")


# Pieces shared with oikia, unchanged.
for _n in ("window", "kline", "klismos_r", "klismos_l", "stool", "table", "table_round", "desk",
           "amphora", "amphora_plain", "pithos", "pots", "mortar", "hearth", "soot", "kalathos",
           "lampstand", "chest", "herbs", "oars", "honey_shelf"):
    reuse(_n)
reuse("mat", walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"})
