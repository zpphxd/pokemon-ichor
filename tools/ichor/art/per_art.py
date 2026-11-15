#!/usr/bin/env python3
"""Pixel art for the per tileset: Egyptian mud-brick interiors.

per (Egyptian *pr*, "house") is the secondary for the Oikoumene's Egyptian
rooms on the oikos primary: Naukratis's and Memphis's interiors (batch 1 of
design/oikoumene/BUILD.md). It is built the way oikia and ergasteria are
(design/phase1/TILES_oikia.md): hand-drawn character grids, one character per
color, '.' for clear, in seven palettes of at most 15 colors, none of which is
an aethos color. per_build.py composes the rooms in
tools/ichor/maps/egypt_rooms.py from these pieces and compiles the set.

Palettes (slots 6-12):
  stone   civic's "marble" palette, colour for colour: limestone greys,
          Egyptian blue, gold and red ochre. The Asclepeion's counter comes
          from civic_art.py pixel for pixel, so every Asclepeion shares it.
  wood    civic's "wood" palette (its one aethos-clashing tone nudged by 8):
          furniture, papyrus and linen, Nile-silt pottery. The Agora's stall
          counter comes from civic_art.py the same way.
  mud     the walls: palm-log beams, mud brick, whitewash, the kheker frieze
  floor   beaten earth, reed matting, limestone pavement, straw, brick
  nature  papyrus and palm, wicker, fish, nets, straw and eggs' straw
  fire    ovens and kilns, fire, soot, eggs, bronze censers
  paint   tomb-painting colours: faience, lapis, carnelian, resin, dye

Light comes from the top left; objects carry a one-pixel ink outline.
"""
import numpy as np

import civic_art as CA

INK = (40, 24, 24)

PALETTES = {
    # civic's marble palette exactly ('#' is 'k' here)
    "stone": {
        "k": INK,
        "1": (72, 64, 64),
        "2": (112, 104, 96),
        "3": (152, 144, 136),
        "4": (184, 176, 160),
        "5": (208, 200, 184),
        "6": (224, 224, 208),
        "7": (240, 240, 232),
        "8": (248, 248, 248),
        "B": (24, 48, 112),    # Egyptian blue, deep
        "b": (48, 96, 168),    # Egyptian blue
        "G": (208, 152, 48),   # gold, deep
        "g": (240, 200, 80),   # gold
        "T": (128, 48, 24),    # red ochre, deep
        "t": (176, 80, 40),    # red ochre
    },
    # civic's wood palette; L moves from (208,184,136), an aethos colour
    "wood": {
        "k": INK,
        "D": (56, 40, 32),
        "d": (96, 64, 40),
        "w": (136, 96, 56),
        "W": (176, 128, 80),
        "v": (208, 168, 112),
        "p": (184, 152, 104),  # papyrus, shade
        "L": (208, 184, 144),  # papyrus
        "P": (232, 216, 168),  # linen, papyrus lit
        "Q": (248, 240, 208),  # linen, lit
        "R": (88, 32, 16),     # silt ware, dark
        "T": (128, 48, 24),
        "t": (176, 80, 40),
        "u": (216, 128, 80),
        "U": (240, 176, 128),
    },
    # walls
    "mud": {
        "k": INK,
        "1": (72, 48, 32),     # palm log, dark
        "2": (112, 72, 40),    # palm log
        "3": (152, 104, 56),   # palm log, lit
        "M": (96, 80, 64),     # mud, dark (joints)
        "m": (128, 104, 80),   # mud brick
        "n": (160, 136, 104),  # mud brick, lit
        "N": (192, 168, 128),  # mud plaster
        "w": (240, 232, 208),  # whitewash, lit
        "p": (224, 216, 184),  # whitewash
        "s": (200, 184, 160),  # whitewash, shade
        "r": (176, 64, 40),    # painted red
        "o": (224, 176, 72),   # painted yellow
        "g": (72, 136, 96),    # painted green
        "b": (56, 96, 168),    # painted blue
    },
    # floors (bottom layer only)
    "floor": {
        "e": (160, 128, 96),   # beaten earth, lit
        "E": (144, 112, 80),   # beaten earth
        "f": (128, 96, 72),    # earth, low
        "F": (104, 80, 56),    # earth, shadow
        "g": (80, 56, 40),     # grout, cracks
        "J": (224, 192, 128),  # reed, lit / straw
        "j": (192, 160, 96),   # reed
        "K": (152, 120, 64),   # reed, dark
        "L": (240, 232, 208),  # limestone, lit
        "l": (224, 216, 192),  # limestone
        "y": (208, 200, 176),  # limestone, second tone
        "q": (184, 176, 152),  # limestone, low
        "Q": (144, 136, 112),  # limestone, seam
        "R": (152, 72, 48),    # dyed red, brick dark
        "r": (184, 112, 72),   # brick
    },
    # plants, wicker, nets, fish
    "nature": {
        "k": INK,
        "G": (40, 72, 48),     # leaf, dark
        "g": (72, 120, 56),    # leaf
        "v": (120, 168, 80),   # leaf, lit
        "V": (184, 216, 128),  # leaf, highlight
        "K": (120, 88, 48),    # wicker, dark
        "j": (176, 136, 72),   # wicker
        "J": (224, 192, 128),  # wicker, lit; straw
        "y": (240, 216, 120),  # straw, bright; papyrus umbel
        "s": (176, 192, 208),  # fish, silver
        "S": (104, 120, 152),  # fish, dark
        "n": (216, 200, 160),  # rope, net, flax
        "w": (248, 248, 232),  # white: lotus, eggs
        "l": (104, 136, 200),  # blue lotus
        "r": (176, 56, 40),    # dates, onion skin
    },
    # ovens, kilns, fire, eggs, censers
    "fire": {
        "k": INK,
        "d": (120, 56, 32),    # fired clay, dark
        "m": (168, 96, 56),    # fired clay
        "l": (208, 136, 88),   # fired clay, lit
        "h": (240, 184, 136),  # fired clay, highlight
        "f": (216, 64, 32),    # fire, red
        "F": (248, 144, 48),   # fire, orange
        "Y": (248, 224, 104),  # fire, yellow
        "a": (64, 56, 56),     # soot
        "A": (104, 96, 96),    # ash, dark
        "s": (176, 168, 168),  # smoke, ash
        "e": (248, 240, 224),  # egg, lit
        "E": (224, 208, 184),  # egg, shade
        "z": (120, 80, 32),    # bronze, dark
        "b": (192, 144, 56),   # bronze
    },
    # paintings, faience, resins, dyes
    "paint": {
        "k": INK,
        "r": (192, 56, 48),    # red
        "R": (128, 32, 32),    # red, dark
        "o": (232, 184, 80),   # yellow ochre
        "O": (168, 120, 48),   # ochre, dark
        "b": (56, 104, 184),   # blue
        "B": (32, 56, 128),    # lapis
        "c": (88, 176, 168),   # faience turquoise
        "C": (168, 224, 208),  # turquoise, lit
        "g": (72, 144, 80),    # malachite
        "w": (248, 240, 224),  # white
        "n": (88, 72, 72),     # black paint, myrrh dark
        "a": (216, 144, 72),   # resin, amber
        "A": (240, 216, 152),  # frankincense, pale
        "i": (112, 64, 136),   # Tyrian purple
    },
}

PALETTE_ORDER = ["stone", "wood", "mud", "floor", "nature", "fire", "paint"]


# --------------------------------------------------------------------------
# Grids and a small drawing canvas
# --------------------------------------------------------------------------

def grid(pal, text, w=None, h=None):
    """Parse a character grid into an (h, w, 4) RGBA array ('.' = clear)."""
    rows = [r.rstrip() for r in text.strip("\n").split("\n")] if isinstance(text, str) else list(text)
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


class Canvas:
    """A character canvas for drawing pieces by code: '.' is clear."""

    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c != ".":
            self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def rect(self, x, y, w, h, c):
        for j in range(h):
            for i in range(w):
                self.put(x + i, y + j, c)

    def hline(self, x0, x1, y, c):
        for x in range(x0, x1 + 1):
            self.put(x, y, c)

    def vline(self, x, y0, y1, c):
        for y in range(y0, y1 + 1):
            self.put(x, y, c)

    def box(self, x, y, w, h, fill, edge="k"):
        """A filled rectangle with an ink edge."""
        self.rect(x, y, w, h, edge)
        if w > 2 and h > 2:
            self.rect(x + 1, y + 1, w - 2, h - 2, fill)

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                    self.put(x, y, c)

    def paste(self, lines, x, y, remap=None):
        if isinstance(lines, str):
            lines = [r for r in lines.strip("\n").split("\n")]
        for j, row in enumerate(lines):
            for i, c in enumerate(row):
                if c not in ". ":
                    self.put(x + i, y + j, (remap or {}).get(c, c))

    def outline(self, ink="k", inside=None):
        """Ink every clear pixel that touches a drawn one (4-neighbours)."""
        src = [row[:] for row in self.g]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != ".":
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and src[ny][nx] != "." \
                            and (inside is None or src[ny][nx] in inside):
                        self.g[y][x] = ink
                        break

    def recolor(self, mapping, region=None):
        x0, y0, x1, y1 = region or (0, 0, self.w, self.h)
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.g[y][x] = mapping.get(self.g[y][x], self.g[y][x])

    def mirror(self):
        """Copy the left half onto the right, mirrored."""
        for y in range(self.h):
            for x in range(self.w // 2):
                self.g[y][self.w - 1 - x] = self.g[y][x]

    def text(self):
        return "\n".join("".join(r) for r in self.g)


def hflip(img):
    return img[:, ::-1].copy()


def recolor_img(img, pal, mapping):
    """Swap colours by character in an RGBA image."""
    colors = PALETTES[pal]
    out = img.copy()
    for a, b in mapping.items():
        m = (img[..., :3] == colors[a]).all(-1) & (img[..., 3] > 0)
        out[m, :3] = colors[b]
    return out


def civic_piece(name, pal, cx=None, cy=None, w=None, h=None):
    """A civic_art piece (or a cell range of it) as RGBA, its colours checked
    against one of per's palettes."""
    rows = CA.ART[name]
    if cx is not None:
        rows = [r[cx * 16:(cx + (w or 1)) * 16] for r in rows[cy * 16:(cy + (h or 1)) * 16]]
    H, W = len(rows), len(rows[0])
    out = np.zeros((H, W, 4), np.uint8)
    have = set(PALETTES[pal].values())
    nudge = {(208, 184, 136): (208, 184, 144)}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            rgb = nudge.get(CA.LEGEND[ch], CA.LEGEND[ch])
            assert rgb in have, f"civic {name}: {ch} {rgb} is not in per's {pal} palette"
            out[y, x, :3] = rgb
            out[y, x, 3] = 255
    return out


# --------------------------------------------------------------------------
# Floors (16x16, opaque, bottom layer)
# --------------------------------------------------------------------------

def _hash(x, y, k=0):
    return ((x * 73856093) ^ (y * 19349663) ^ (k * 83492791)) & 0xFFFF


def floor_earth(seed=0):
    """Beaten Nile mud, swept smooth: a soft mottle and a hairline crack."""
    c = Canvas(16, 16, "E")
    for y in range(16):
        for x in range(16):
            h = _hash(x, y, seed) % 23
            if h == 0:
                c.put(x, y, "e")
            elif h == 1:
                c.put(x, y, "f")
    # two soft patches, lit and low
    for (px, py, ch) in ((3, 4, "e"), (11, 11, "f")):
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (-1, 0), (2, 1)):
            c.put((px + dx) % 16, (py + dy) % 16, ch)
    # a fine crack
    for (x, y) in [(8, 2), (9, 3), (9, 4), (10, 5)] if seed == 0 else [(2, 9), (3, 10), (4, 10), (5, 11)]:
        c.put(x, y, "f")
    return grid("floor", c.text())


def floor_mat():
    """Reed matting, woven in a 2-over-2 twill of 4-pixel strips: it tiles
    every 8 pixels, so the whole floor costs four tiles."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            band = ((x // 4) + (y // 4)) % 2
            if band == 0:   # strips running across
                yy = y % 4
                ch = "J" if yy == 0 else "j" if yy < 3 else "K"
            else:           # strips running down
                xx = x % 4
                ch = "J" if xx == 0 else "j" if xx < 3 else "K"
            c.put(x, y, ch)
    return grid("floor", c.text())


def floor_flags():
    """Limestone pavement in big square slabs, bevelled, as in a temple."""
    c = Canvas(16, 16, "l")
    for y in range(16):
        for x in range(16):
            if x == 15 or y == 15:
                c.put(x, y, "Q")
            elif x == 14 or y == 14:
                c.put(x, y, "q")
            elif x == 0 or y == 0:
                c.put(x, y, "L")
    for (x, y, ch) in [(4, 5, "y"), (5, 5, "y"), (10, 9, "L"), (9, 11, "y"), (3, 11, "y"), (12, 3, "y")]:
        c.put(x, y, ch)
    return grid("floor", c.text())


def floor_flags_alt():
    c = Canvas(16, 16, "y")
    for y in range(16):
        for x in range(16):
            if x == 15 or y == 15:
                c.put(x, y, "Q")
            elif x == 14 or y == 14:
                c.put(x, y, "q")
            elif x == 0 or y == 0:
                c.put(x, y, "l")
    for (x, y, ch) in [(6, 4, "q"), (11, 10, "l"), (12, 10, "l"), (4, 12, "q")]:
        c.put(x, y, ch)
    return grid("floor", c.text())


def floor_brick():
    """Mud-brick paving laid in a basket weave, for the stable and the ovens."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            qx, qy = x // 8, y // 8
            lx, ly = x % 8, y % 8
            horiz = (qx + qy) % 2 == 0
            if horiz:
                edge = ly in (3, 7)
                lit = ly in (0, 4)
            else:
                edge = lx in (3, 7)
                lit = lx in (0, 4)
            c.put(x, y, "g" if edge else "e" if lit else "E")
    return grid("floor", c.text())


FLOOR_SHADE = {
    "earth": {"e": "E", "E": "f", "f": "F", "F": "g"},
    "mat": {"J": "j", "j": "K", "K": "F"},
    "flags": {"L": "y", "l": "q", "y": "q", "q": "Q"},
    "brick": {"e": "E", "E": "f", "f": "F", "g": "g"},
}


def recolor_floor(img, mapping):
    return recolor_img(img, "floor", mapping)


def floor_variants(material, base, alt=None):
    """plain (and an alternate plain), top shadow under the back wall, left
    shadow, and the corner where they meet. The shadows fall on whole 8-pixel
    rows and columns' worth of pattern where they can, to share tiles."""
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    dark = recolor_floor(base, FLOOR_SHADE[material])

    def sh(mask):
        out = base.copy()
        out[mask] = dark[mask]
        return out
    out = {"plain": base, "top": sh(top), "left": sh(left), "corner": sh(top | left)}
    if alt is not None:
        out["alt"] = alt
    return out


FLOORS = {
    "earth": floor_variants("earth", floor_earth(0)),
    "mat": floor_variants("mat", floor_mat()),
    "flags": floor_variants("flags", floor_flags()),
}

# --------------------------------------------------------------------------
# Walls. Each is a 16-wide strip, two blocks tall (rows 0 and 1 of a room).
# --------------------------------------------------------------------------

def _palm_ceiling(c):
    """Rows 0-6: the palm-log ceiling seen edge-on: a dark edge, a log laid
    along the wall, and the round ends of the cross-logs."""
    c.hline(0, 15, 0, "k")
    c.hline(0, 15, 1, "2")
    c.hline(0, 15, 2, "3")
    c.hline(0, 15, 3, "2")
    c.hline(0, 15, 4, "1")
    # the cross-logs' round ends, two to a block, with their growth rings
    for ox in (1, 9):
        c.paste(["k1111k",
                 "1233321"[0:6],
                 "123321",
                 "k1221k"], ox, 4)
    for x in range(16):
        if c.get(x, 5) == ".":
            c.put(x, 5, "M")
        if c.get(x, 6) == ".":
            c.put(x, 6, "M")
        if c.get(x, 7) == ".":
            c.put(x, 7, "s")


def _kheker(c, y0):
    """The kheker frieze: tied reed bundles in green, red, blue and yellow,
    four pixels apart, rows y0..y0+5."""
    cols = "grbo"
    for i in range(4):
        x0 = i * 4
        col = cols[i % 4]
        c.paste([".kk.",
                 "k" + col + col + "k",
                 ".kk.",
                 "k" + col + col + "k",
                 "k" + col + col + "k",
                 "kkkk"], x0, y0)
    for x in range(16):
        for y in range(y0, y0 + 6):
            if c.get(x, y) == ".":
                c.put(x, y, "p")


def wall_plaster():
    """A whitewashed mud-plaster wall: the palm-log ceiling, the kheker
    frieze, whitewash, and a dado of painted bands over a mud plinth."""
    c = Canvas(16, 32)
    _palm_ceiling(c)
    _kheker(c, 8)
    c.hline(0, 15, 14, "s")
    for y in range(15, 24):
        c.hline(0, 15, y, "p")
    for (x, y, ch) in [(3, 17, "w"), (11, 19, "w"), (6, 21, "s"), (13, 16, "s"), (1, 22, "w")]:
        c.put(x, y, ch)
    c.hline(0, 15, 24, "s")
    c.hline(0, 15, 25, "k")
    c.hline(0, 15, 26, "r")
    c.hline(0, 15, 27, "r")
    c.hline(0, 15, 28, "o")
    c.hline(0, 15, 29, "k")
    c.hline(0, 15, 30, "m")
    c.hline(0, 15, 31, "M")
    return grid("mud", c.text())


def wall_brick():
    """Bare mud brick, the courses staggered, under the palm-log ceiling."""
    c = Canvas(16, 32)
    _palm_ceiling(c)
    for y in range(8, 32):
        r = (y - 8) % 6
        course = (y - 8) // 6
        off = 0 if course % 2 == 0 else 4
        for x in range(16):
            if r == 5:
                ch = "M"
            elif (x + off) % 8 == 7:
                ch = "M"
            elif r == 0:
                ch = "n"
            elif (x + off) % 8 == 0:
                ch = "n"
            else:
                ch = "m"
            c.put(x, y, ch)
    c.hline(0, 15, 31, "1")
    return grid("mud", c.text())


def wall_temple():
    """Painted limestone (stone palette): a blue ceiling with gold stars, a
    cavetto cornice in blue, red and gold, a torus band, limestone blocks and
    a blue dado."""
    c = Canvas(16, 32)
    c.hline(0, 15, 0, "k")
    for y in range(1, 6):
        c.hline(0, 15, y, "B")
    for (x, y) in [(3, 3), (11, 3)]:
        c.put(x, y, "g")
        c.put(x - 1, y, "G"); c.put(x + 1, y, "G"); c.put(x, y - 1, "G"); c.put(x, y + 1, "G")
    c.hline(0, 15, 6, "1")
    # cavetto: upright leaves in blue, red and gold, with a gold fillet
    leaves = "bbt8ggt8bbt8ggt8"
    for y in range(7, 11):
        for x in range(16):
            c.put(x, y, leaves[x] if y < 10 else "G")
    for x in range(16):
        if x % 4 == 3:
            c.put(x, 7, "7")
    # torus: a bound roll
    c.hline(0, 15, 11, "1")
    for x in range(16):
        c.put(x, 12, "5" if x % 3 else "t")
    c.hline(0, 15, 13, "3")
    # limestone blocks
    for y in range(14, 27):
        r = y - 14
        for x in range(16):
            if r == 6 or r == 12:
                ch = "4"
            elif (r < 6 and x == 7) or (6 < r < 12 and x == 15):
                ch = "4"
            elif r in (0, 7):
                ch = "8"
            else:
                ch = "7"
            c.put(x, y, ch)
    c.hline(0, 15, 27, "3")
    c.hline(0, 15, 28, "b")
    c.hline(0, 15, 29, "B")
    c.hline(0, 15, 30, "g")
    c.hline(0, 15, 31, "1")
    return grid("stone", c.text())


WALLS = {
    "plaster": wall_plaster(),
    "brick": wall_brick(),
    "temple": wall_temple(),
}

VOID = grid("mud", "\n".join(["k" * 16] * 16))


# --------------------------------------------------------------------------
# Rugs: 9-slices on the bottom layer, 48x48, drawn symmetric so each corner
# and edge is a flip of the others.
# --------------------------------------------------------------------------

def _rug(pal, fn):
    c = Canvas(48, 48)
    for y in range(48):
        for x in range(48):
            mx, my = min(x, 47 - x), min(y, 47 - y)
            c.put(x, y, fn(x, y, mx, my))
    return grid(pal, c.text())


STRAW8 = [  # strands lying every which way; tiles every 8 pixels
    "JjjKJjjJ",
    "jKJjjJKj",
    "JjjJKjjJ",
    "KjJjjJjK",
    "jJKjJjJj",
    "JjjJjKjJ",
    "jKJjjJjK",
    "JjjKJjJj",
]


def rug_straw():
    """Straw bedding on beaten earth: thick in the middle, a few stray
    strands at the edges. The texture repeats every 8 pixels, so a whole
    stable's worth costs a handful of tiles."""
    def f(x, y, mx, my):
        d = min(mx, my)
        s = STRAW8[y % 8][x % 8]
        if d < 2:
            return "j" if s == "K" else "E"
        if d < 4:
            return s if s != "j" else "E"
        return s
    return _rug("floor", f)


def rug_mat():
    """A reed mat with a red dyed border, laid on the floor."""
    def f(x, y, mx, my):
        d = min(mx, my)
        if d == 0:
            return "K"
        if d in (1, 6):
            return "R"
        if d < 6:
            return "r" if (x + y) % 4 else "R"
        band = ((x // 4) + (y // 4)) % 2
        if band == 0:
            return "J" if y % 4 == 0 else "j" if y % 4 < 3 else "K"
        return "J" if x % 4 == 0 else "j" if x % 4 < 3 else "K"
    return _rug("floor", f)


def rug_arabian():
    """The incense merchant's woven rug from Arabia: madder field, indigo
    border with ochre lozenges, a white fringe line."""
    def f(x, y, mx, my):
        d = min(mx, my)
        if d == 0:
            return "k"
        if d == 1:
            return "w"
        if d < 8:
            # lozenges along the border, period 8, mirrored about the middle
            along = my if mx < my else mx
            k = abs((along % 8) - 4)
            off = abs(d - 4)
            return "o" if k + off == 2 else "O" if k + off < 2 else "B"
        if d == 8:
            return "o"
        # field: small diamonds every 8
        k = abs(x % 8 - 4) + abs(y % 8 - 4)
        return "o" if k == 0 else "r" if k > 1 else "R"
    return _rug("paint", f)


RUGS = {"straw": rug_straw(), "mat": rug_mat(), "arabian": rug_arabian()}

# --------------------------------------------------------------------------
# Stamps. The contract is oikia's: w, h in metatiles; walk cells the player
# may stand on; behavior per cell; `top` art over the player; `flatten` puts
# the art in the bottom layer.
# --------------------------------------------------------------------------

STAMPS = {}


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note=""):
    """w, h in metatiles. art and top: a grid string, a Canvas or an RGBA array."""
    def img_of(a):
        if a is None:
            return None
        if isinstance(a, np.ndarray):
            return a
        if isinstance(a, Canvas):
            a = a.text()
        return grid(pal, a, w * 16, h * 16)
    img = img_of(art)
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    STAMPS[name] = {
        "pal": pal,
        "img": img,
        "top": img_of(top),
        "w": w,
        "h": h,
        "walk": set(walk),
        "behavior": dict(behavior or {}),
        "flatten": flatten,
        "note": note,
        "source": "per",
    }


import per_pieces  # noqa: E402,F401  (registers the stamps)
