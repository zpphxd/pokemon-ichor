#!/usr/bin/env python3
"""Pixel art for the chalkeon tileset: the Black Sea's interiors.

chalkeon (a bronze-smith's shop, and the bronze it works) is the interior set
for the Black Sea's towns in the Oikoumene: Salmydessos on the Thracian shore
and Aia in Colchis (design/OIKOUMENE.md §4.3 and §7, "a Colchian bronze hall").
Batch 1 builds the two towns' seven rooms from it (tools/ichor/maps/
pontos_rooms.py); batch 2's palace hall (design/oikoumene/PERIODOS.md §4.3)
extends the same set, so the bronze walls, the bull's head and the fountain
basin are drawn to be recoloured and repeated: the bull's head takes a fire
line, the basin takes milk, wine, oil or water.

Three kinds of wall carry the land's look:
  bronze, bronze_enamel  Aietes's city: riveted bronze plates, and the
                         Asclepeion's blue-and-red enamel frieze
  logs                   a Colchian house of whole trees laid flat, the gaps
                         stopped with clay (Vitruvius 2.1.4)
  plaster, wattle        Salmydessos: a Thracian king's whitewashed hall gone
                         bare, and a bird-catcher's woven-withy wall

Drawn as oikia and ergasteria are (design/phase1/TILES_oikia.md): character
grids, one character per colour, '.' clear, in seven palettes of at most 15
colours, none of them an aethos colour. The household furniture a Colchian or
Thracian room shares with a Greek one (couches, stools, jars, the hearth, the
door mat) is oikia's, pixel for pixel, so oikia's wood, clay, nature and bronze
palettes are kept whole; chalkeon's own wall, floor and cloth palettes replace
the other three.

Palettes:
  wall    ink; bronze, darkest to highlight; verdigris; enamel blue and red;
          log timber; clay chinking
  floor   ink; enamel glazes and their bronze grout; plank browns; stone;
          a faded red ochre (also the Thracian plaster's wall)
  wood    oikia's: furniture woods, bronze fittings, linen, cloth
  clay    oikia's: pottery, stone, fire, soot, slip, bronze, honey
  cloth   oikia's rug colours plus linen white and grey and a lit wood:
          linen, flax, the fleece, the loom
  nature  oikia's: plants, wicker, feathers, fish, rope (also the wattle wall)
  bronze  oikia's: bronze, flame, water, marble

chalkeon_build.py assembles the pieces into metatiles.
"""
import copy
import math

import numpy as np

import oikia_art as O

INK = O.INK

PALETTES = {
    "wall": {
        "k": INK,
        "1": (72, 48, 24),     # bronze, darkest / log shadow
        "2": (120, 72, 32),    # bronze, dark
        "3": (184, 128, 48),   # bronze
        "4": (240, 184, 88),   # bronze, lit
        "5": (248, 224, 160),  # bronze, highlight
        "v": (40, 96, 88),     # verdigris, dark
        "V": (88, 152, 128),   # verdigris
        "e": (40, 72, 144),    # enamel blue
        "E": (104, 152, 208),  # enamel blue, lit / sky
        "r": (168, 48, 32),    # enamel red
        "L": (96, 64, 40),     # log
        "l": (144, 104, 64),   # log, lit
        "c": (152, 128, 96),   # clay chinking, shade
        "C": (192, 168, 128),  # clay chinking
    },
    "floor": {
        "k": INK,
        "a": (32, 88, 104),    # glaze, deep
        "b": (56, 128, 136),   # glaze
        "d": (120, 184, 176),  # glaze, lit
        "w": (224, 224, 200),  # white glaze / plaster, lit
        "g": (120, 80, 40),    # bronze grout
        "P": (200, 152, 96),   # plank, lit
        "p": (168, 120, 72),   # plank
        "q": (136, 96, 64),    # plank, low / earth
        "j": (88, 64, 48),     # plank seam / earth, dark
        "S": (200, 192, 168),  # stone, lit / plaster
        "s": (168, 160, 136),  # stone / plaster shade
        "t": (136, 128, 112),  # stone, low
        "Q": (88, 80, 72),     # stone seam
        "R": (160, 64, 48),    # red ochre, faded
    },
    "wood": copy.deepcopy(O.PALETTES["wood"]),
    "clay": copy.deepcopy(O.PALETTES["clay"]),
    "cloth": dict(copy.deepcopy(O.PALETTES["cloth"]), **{
        "L": (248, 240, 224),  # linen, bleached
        "N": (176, 160, 136),  # linen, grey shade
        "B": (152, 104, 64),   # wood, lit (the loom's beams, the fleece's frame)
    }),
    "nature": copy.deepcopy(O.PALETTES["nature"]),
    "bronze": copy.deepcopy(O.PALETTES["bronze"]),
}

PALETTE_ORDER = ["wall", "floor", "wood", "clay", "cloth", "nature", "bronze"]


def grid(pal, text, w=None, h=None):
    """Parse a character grid into an (h, w, 4) RGBA array ('.' = clear)."""
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


def hflip(img):
    return img[:, ::-1].copy()


class Canvas:
    """A character grid to draw on: '.' is clear."""

    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(self.h):
            for x in range(self.w):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                    self.put(x, y, c)

    def paste(self, x0, y0, text):
        """Lay a small grid over the canvas at (x0, y0); '.' stays."""
        rows = [r for r in text.strip("\n").split("\n")]
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch not in ". ":
                    self.put(x0 + i, y0 + j, ch)

    def outline(self, ink="k", diag=False):
        """Ink every clear pixel touching a drawn one."""
        src = [r[:] for r in self.g]
        nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if diag:
            nb += [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != ".":
                    continue
                for dx, dy in nb:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and src[ny][nx] not in ".":
                        self.g[y][x] = ink
                        break

    def mirror_x(self):
        """Copy the left half onto the right, mirrored."""
        for y in range(self.h):
            for x in range(self.w // 2):
                self.g[y][self.w - 1 - x] = self.g[y][x]

    def text(self):
        return "\n".join("".join(r) for r in self.g)


def lathe(c, cx, y0, widths, ramp, edge=None):
    """A turned vessel: `widths` are half-widths per row from y0, the body lit
    from the left. ramp: five characters, highlight to darkest."""
    hi, lit, mid, low, dark = ramp
    for j, hw in enumerate(widths):
        if hw <= 0:
            continue
        y = y0 + j
        for x in range(int(math.floor(cx - hw)), int(math.ceil(cx + hw))):
            t = (x + 0.5 - cx) / hw
            if t < -0.62:
                ch = lit
            elif t < -0.3:
                ch = hi
            elif t < 0.3:
                ch = mid
            elif t < 0.7:
                ch = low
            else:
                ch = dark
            c.put(x, y, ch)
    if edge:
        for j, hw in enumerate(widths):
            if hw > 0:
                c.put(int(math.floor(cx - hw)), y0 + j, edge)


# ==========================================================================
# Floors (16x16, opaque, bottom layer)
# ==========================================================================

def _rows(text):
    return [list(r) for r in text]


def floor_planks(knot=False):
    """Wide Colchian boards running east-west, two to a block, so long their
    butt joints hardly show: a lit edge, a soft seam, a little grain, all of it
    repeating every 8 px so the floor costs few tiles. The alternate block has
    a joint and a knot."""
    def board(grain):
        rows = []
        for y in range(8):
            ch = "P" if y == 0 else ("q" if y == 7 else "p")
            rows.append([ch] * 16)
        for (x, y, n) in grain:
            for i in range(n):
                for rep in (0, 8):
                    if rows[y][(x + i + rep) % 16] == "p":
                        rows[y][(x + i + rep) % 16] = "q"
        return rows
    a = board([(1, 3, 3), (6, 5, 2)])
    b = board([(4, 2, 3), (0, 5, 2)])
    rows = a + b
    if knot:
        for y in range(9, 15):
            rows[y][10] = "j"
            rows[y][11] = "P"
        for (x, y) in [(4, 11), (5, 11), (3, 12), (6, 12), (4, 13), (5, 13)]:
            rows[y][x] = "q"
        rows[12][4] = "j"
        rows[12][5] = "j"
    return grid("floor", "\n".join("".join(r) for r in rows))


def floor_enamel(rosette=False):
    """Glazed tiles set in bronze, one to a block: white glaze inside a bronze
    joint, and where four tiles meet, a sea-green diamond inset. Symmetric both
    ways, so a block is one 8x8 tile and its flips. The alternate tile has a
    green-and-red cross at its heart."""
    q = []
    for y in range(8):
        row = []
        for x in range(8):
            d = x + y
            if d <= 1:
                ch = "b"
            elif d == 2:
                ch = "a"
            elif x == 0 or y == 0:
                ch = "g"
            elif x == 1 or y == 1:
                ch = "S"
            else:
                ch = "w"
            row.append(ch)
        q.append(row)
    if rosette:
        for (x, y, ch) in [(7, 7, "R"), (6, 7, "b"), (7, 6, "b"), (5, 7, "d"), (7, 5, "d"),
                           (4, 7, "b"), (7, 4, "b"), (6, 6, "a")]:
            q[y][x] = ch
    top = [r + r[::-1] for r in q]
    rows = top + top[::-1]
    return grid("floor", "\n".join("".join(r) for r in rows))


def floor_flags(scorch=False):
    """Irregular stone flags, laid as oikia lays its limestone: the stones are
    the cells of a Voronoi diagram on a 16x16 torus, so the pattern tiles
    without a seam, each with a lit top-left edge. The alternate is scorched."""
    seeds = [(3, 3), (11, 4), (6, 11), (14, 12)]

    def owner(x, y):
        best, bi = None, 0
        for i, (sx, sy) in enumerate(seeds):
            dx = min(abs(x - sx), 16 - abs(x - sx))
            dy = min(abs(y - sy), 16 - abs(y - sy))
            d = dx * dx * 1.0 + dy * dy * 1.3
            if best is None or d < best:
                best, bi = d, i
        return bi

    own = [[owner(x, y) for x in range(16)] for y in range(16)]
    seam = [[own[y][x] != own[y][(x + 1) % 16] or own[y][x] != own[(y + 1) % 16][x]
             for x in range(16)] for y in range(16)]
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            if seam[y][x]:
                n = len({own[y][x], own[y][(x + 1) % 16], own[(y + 1) % 16][x],
                         own[(y + 1) % 16][(x + 1) % 16]})
                row.append("Q" if n > 2 else "t")
            elif seam[(y - 1) % 16][x] or seam[y][(x - 1) % 16]:
                row.append("S")
            else:
                row.append("s")
        rows.append(row)
    for (x, y) in [(4, 5), (9, 2), (12, 9), (2, 13), (7, 8)]:
        if rows[y][x] == "s":
            rows[y][x] = "t"
    if scorch:
        for (x, y) in [(5, 6), (6, 6), (7, 6), (4, 7), (5, 7), (8, 7), (5, 8), (6, 8), (7, 8),
                       (9, 8), (6, 9), (8, 9)]:
            if rows[y][x] in "sS":
                rows[y][x] = "t"
        for (x, y) in [(6, 7), (7, 7)]:
            rows[y][x] = "Q"
    return grid("floor", "\n".join("".join(r) for r in rows))


def floor_earth(husks=False):
    """Beaten earth, swept but never clean: speckled, no joints, repeating
    every 8 px. The alternate has spilled seed husks and a small feather."""
    rows = [["q"] * 16 for _ in range(16)]
    specks = [(1, 1, "p"), (5, 2, "j"), (3, 5, "t"), (7, 6, "p"), (6, 3, "t"), (2, 7, "j")]
    for (x, y, ch) in specks:
        for dx in (0, 8):
            for dy in (0, 8):
                rows[y + dy][x + dx] = ch
    if husks:
        for (x, y, ch) in [(4, 4, "P"), (5, 4, "S"), (10, 9, "S"), (11, 9, "S"), (12, 10, "S"),
                           (11, 10, "w"), (12, 11, "w"), (13, 11, "t")]:
            rows[y][x] = ch
    return grid("floor", "\n".join("".join(r) for r in rows))


FLOOR_SHADE = {
    "planks": {"P": "p", "p": "q", "q": "j"},
    "enamel": {"d": "b", "b": "a", "a": "a", "w": "S", "S": "s"},
    "flags": {"S": "s", "s": "t", "t": "Q"},
    "earth": {"P": "p", "p": "q", "q": "j", "S": "s", "w": "s", "t": "Q"},
}


def recolor(img, pal, mapping):
    colors = PALETTES[pal]
    out = img.copy()
    src = img[..., :3]
    for a, b in mapping.items():
        m = (src == colors[a]).all(-1) & (img[..., 3] > 0)
        out[m, :3] = colors[b]
    return out


def shade(img, material, mask):
    dark = recolor(img, "floor", FLOOR_SHADE[material])
    out = img.copy()
    out[mask] = dark[mask]
    return out


def floor_variants(material, base, alt=None):
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    out = {"plain": base, "top": shade(base, material, top), "left": shade(base, material, left),
           "corner": shade(base, material, top | left)}
    if alt is not None:
        out["alt"] = alt
    return out


FLOORS = {
    "planks": floor_variants("planks", floor_planks(), floor_planks(knot=True)),
    "enamel": floor_variants("enamel", floor_enamel(), floor_enamel(rosette=True)),
    "flags": floor_variants("flags", floor_flags()),
    "earth": floor_variants("earth", floor_earth(), floor_earth(husks=True)),
}


# ==========================================================================
# Walls (16 wide, 32 tall: rows 0 and 1 of a room)
# ==========================================================================

def _cornice(rows):
    """The bronze cornice under the ceiling, shared by the two bronze walls:
    an ink edge, a lit roll, a bead-and-reel band, a shadowed soffit."""
    rows.append("k" * 16)
    rows.append("2" * 16)
    rows.append("4" * 16)
    rows.append("5" * 16)
    rows.append("".join("4" if x % 4 in (0, 1) else "2" for x in range(16)))
    rows.append("".join("3" if x % 4 in (0, 1) else "1" for x in range(16)))
    rows.append("1" * 16)


def _plates(rows, top, bottom):
    """Riveted bronze plates, one block wide, from row `top` to `bottom`: a
    lit left seam and a dark right one, a soft sheen falling from the upper
    left, a rivet at each corner."""
    n = bottom - top
    for y in range(top, bottom + 1):
        r = y - top
        row = []
        for x in range(16):
            if x == 15:
                ch = "1"
            elif x == 0:
                ch = "4"
            elif r in (1, n - 1) and x in (2, 13):
                ch = "5"            # rivet heads
            elif r in (2, n) and x in (2, 13):
                ch = "2"            # their shadows
            elif r == 0:
                ch = "4"
            elif r == n:
                ch = "2"
            elif 3 <= x <= 5 and r < n * 0.6 and (x - 3) <= r * 0.25:
                ch = "4"            # the sheen
            elif x >= 12 and r > n * 0.4:
                ch = "2"
            else:
                ch = "3"
            row.append(ch)
        rows.append("".join(row))


def wall_bronze():
    """Aietes's walls: the cornice, then riveted bronze plates to a dark
    plinth. 8-px periodic, so the wall costs few tiles; batch 2's palace halls
    use it as it is."""
    rows = []
    _cornice(rows)
    _plates(rows, 7, 28)
    rows.append("2" * 16)
    rows.append("1" * 16)
    rows.append("k" * 16)
    assert len(rows) == 32, len(rows)
    return grid("wall", "\n".join(rows))


def wall_bronze_enamel():
    """The Asclepeion's wall: the same plates over a frieze of enamel set in
    bronze cells, blue lozenges with red hearts on a white-gold ground."""
    rows = []
    _cornice(rows)
    _plates(rows, 7, 19)
    rows.append("4" * 16)
    rows.append("2" * 16)
    LOZ = [  # 8 wide, one period of the frieze
        "3332E333",
        "332eeE33",
        "32eerEE3",
        "2eerrrE3",
        "32eerEe3",
        "332eee33",
        "3332e333",
    ]
    for r in LOZ:
        rows.append(r * 2)
    rows.append("2" * 16)
    rows.append("4" * 16)
    rows.append("1" * 16)
    assert len(rows) == 32, len(rows)
    return grid("wall", "\n".join(rows))


def wall_logs():
    """A Colchian house: whole trees laid flat one on another, the gaps
    stopped with clay. A ceiling log, then four courses, each with a lit
    crown, bark streaks and a shadowed belly over its chinking."""
    rows = []
    rows.append("k" * 16)
    rows.append("1" * 16)
    rows.append("l" * 16)
    rows.append("L" * 16)
    rows.append("1" * 16)
    # bark streaks, two to a log, repeating every 8 px so the wall is cheap
    streaks = [
        [(3, 2), (4, 2), (6, 3)],
        [(1, 2), (2, 2), (5, 3)],
    ]
    for course in range(4):
        rows.append("C" * 16)                       # chinking, lit
        rows.append("".join("c" if x % 4 == 1 else "C" for x in range(16)))
        body = [list("l" * 16), list("l" * 16), list("L" * 16), list("L" * 16), list("L" * 16), list("1" * 16)]
        body[0] = list("".join("L" if x % 8 == (course * 3) % 8 else "l" for x in range(16)))
        for (x, dy) in streaks[course % 2]:
            body[dy][x] = "1"
            body[dy][x + 8] = "1"
        for b in body:
            rows.append("".join(b))
    rows = rows[:31]
    rows.append("k" * 16)
    assert len(rows) == 32, len(rows)
    return grid("wall", "\n".join(rows))


def wall_plaster():
    """Phineus's hall at Salmydessos: a king's whitewash gone grey, a beam
    above, a red ochre band and a meander frieze half flaked away, a stone
    plinth. Drawn in the floor palette (its stone and ochre)."""
    rows = []
    rows.append("k" * 16)
    rows.append("j" * 16)
    rows.append("P" * 16)
    rows.append("p" * 16)
    rows.append("q" * 16)
    rows.append("j" * 16)
    rows.append("".join("s" if x % 8 in (0, 1, 2) else "S" for x in range(16)))
    for y in range(7, 21):
        rows.append("S" * 16)
    rows.append("s" * 16)
    rows.append("R" * 16)
    MEANDER = [
        "wwwwwwww",
        "wRRRRRRw",
        "wRwwwwRw",
        "wRwRRwRw",
        "wRwwRwww",
        "wRRRRRRR",
    ]
    for r in MEANDER:
        rows.append(r * 2)
    rows.append("R" * 16)
    rows.append("t" * 16)
    rows.append("Q" * 16)
    rows = [list(r) for r in rows]
    # the whitewash's age: grey blooms, and the frieze flaked off here and
    # there to its grey under-coat (every 8 px, so the wall stays cheap)
    for (x, y, ch) in [(3, 9, "s"), (4, 9, "s"), (5, 13, "s"), (2, 18, "s"),
                       (5, 24, "s"), (6, 24, "s"), (5, 25, "s")]:
        rows[y][x] = ch
        rows[y][x + 8] = ch
    assert len(rows) == 32, len(rows)
    return grid("floor", "\n".join("".join(r) for r in rows))


def wall_wattle():
    """The bird-catcher's walls: withies woven between stakes and daubed with
    clay that has cracked off here and there. Drawn in the nature palette
    (its wicker and rope colours)."""
    rows = []
    rows.append("k" * 16)
    rows.append("K" * 16)
    rows.append("J" * 16)
    rows.append("j" * 16)
    rows.append("K" * 16)
    for y in range(5, 30):
        r = (y - 5) % 4
        row = []
        for x in range(16):
            stake = x % 8 == 3
            over = ((x // 4) + ((y - 5) // 4)) % 2 == 0
            if stake:
                ch = "K"
            elif r == 3:
                ch = "K"
            elif r == 0:
                ch = "J" if over else "j"
            else:
                ch = "j" if over else "K"
            row.append(ch)
        rows.append(row)

    # daub: clay smoothed over the weave, cracked here and there; the weave
    # shows only along the foot, where the daub has worn off
    for y in range(5, 25):
        for x in range(16):
            rows[y][x] = "n"
    for (x, y) in [(2, 8), (3, 8), (13, 7), (6, 21), (7, 21), (12, 15)]:
        rows[y][x] = "J"
    for (x, y) in [(1, 11), (2, 12), (3, 12), (4, 13), (10, 18), (11, 19), (11, 20)]:
        rows[y][x] = "j"
    for x in range(16):
        rows[24][x] = "J" if x % 5 else "n"     # the daub's ragged lower edge
    rows[28] = list("j" * 16)
    rows = ["".join(r) if isinstance(r, list) else r for r in rows]
    rows.append("K" * 16)
    rows.append("k" * 16)
    assert len(rows) == 32, len(rows)
    return grid("nature", "\n".join(rows))


WALLS = {
    "bronze": wall_bronze(),
    "bronze_enamel": wall_bronze_enamel(),
    "logs": wall_logs(),
    "plaster": wall_plaster(),
    "wattle": wall_wattle(),
}

VOID = grid("wall", "\n".join(["k" * 16] * 16))
RUGS = {}


# ==========================================================================
# Stamps. Same contract as oikia's and ergasteria's: w, h in metatiles; walk
# cells the player may stand on; behavior per cell; `top` art over the
# player; `flatten` puts the art in the bottom layer.
# ==========================================================================

STAMPS = {}

# Household furniture shared with oikia, pixel for pixel.
SHARED = ["mat", "kline", "pithos", "amphora", "amphora_plain", "pots", "stool", "table", "table_round",
          "klismos_r", "klismos_l", "jar_shelf", "honey_shelf", "altar", "hearth", "soot",
          "boat", "oars", "kalathos", "lampstand"]
for _name in SHARED:
    STAMPS[_name] = dict(O.STAMPS[_name], note=O.STAMPS[_name]["note"], source="oikia")


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note=""):
    img = art if isinstance(art, np.ndarray) else grid(pal, art, w * 16, h * 16)
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    STAMPS[name] = {
        "pal": pal, "img": img,
        "top": grid(pal, top, w * 16, h * 16) if top else None,
        "w": w, "h": h, "walk": set(walk), "behavior": dict(behavior or {}),
        "flatten": flatten, "note": note, "source": "chalkeon",
    }


import chalkeon_pieces  # noqa: E402,F401  (draws the stamps into STAMPS)
