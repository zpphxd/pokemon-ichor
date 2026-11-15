#!/usr/bin/env python3
"""Thyrsa's public rooms: the Asclepeion round the spring of Dirke, the Agora's
market hall, and the Kantharos, a cellar tavern. Registered into
thyrsa_rooms_art.STAMPS on import."""
import math

from thyrsa_rooms_art import stamp, grid, blank, over, hflip, STAMPS, recolor, OA  # noqa: F401


def _canvas(w, h):
    return [["."] * w for _ in range(h)]


def _put(g, x, y, c):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = c


def _text(g):
    return "\n".join("".join(r) for r in g)


# ---- masks (nature: white faces for women's parts, brown for men's) --------

MASKS = {
    "comic": """
................
.....k....k.....
....kjkkkkjk....
...kjJJJJJJjk...
..kJJJJJJJJJJk..
..kJkkJJJJkkJk..
..kJkKJJJJkKJk..
..kJJJJjjJJJJk..
..kJJJJjjJJJJk..
..kJkkkkkkkkJk..
..kJkddddddkJk..
..kJJkddddkJJk..
...kJJkkkkJJk...
...kKJJJJJJKk...
....kkKKKKkk....
................
""",
    "tragic": """
................
....kkkkkkkk....
...kKKKKKKKKk...
..kKKwwwwwwKKk..
..kKwwwwwwwwKk..
..kKwkkwwkkwKk..
..kKkkkwwkkkKk..
..kKwkwwwwkwKk..
..kKwwwnnwwwKk..
..kKwwwnnwwwKk..
..kKwwkkkkwwKk..
..kKwkddddkwKk..
..kKwwkkkkwwKk..
...kKwwwwwwKk...
....kKKKKKKk....
.....kkkkkk.....
""",
    "satyr": """
..k..........k..
.kjk........kjk.
.kjjk.kkkk.kjjk.
..kjkkKKKKkkjk..
...kKKJJJJKKk...
..kKJJJJJJJJKk..
..kJkkJJJJkkJk..
..kJkKJJJJKkJk..
..kJJJJjjJJJJk..
..kJJJjkkjJJJk..
..kJJkkddkkJJk..
..kKJJkddkJJKk..
..kKKKKkkKKKKk..
...kKKKKKKKKk...
....kKKKKKKk....
.....kkkkkk.....
""",
    "elektra": """
................
....kkkkkkkk....
...kSSSSSSSSk...
..kSSwwwwwwSSk..
..kSwwwwwwwwSk..
..kSwkkwwkkwSk..
..kwkpkwwkpkwk..
..kwwkwwwwkwwk..
..kwwwwnnwwwwk..
..kwwwwnnwwwwk..
..kwwwkkkkwwwk..
..kwwkddddkwwk..
..kwwwkkkkwwwk..
...kwwwwwwwwk...
....kwwwwwwk....
.....kkkkkk.....
""",
    "king": """
...k..k..k..k...
..kJkkJkkJkkJk..
..kJJJJJJJJJJk..
..kkkkkkkkkkkk..
..kKjjjjjjjjKk..
..kjkkjjjjkkjk..
..kjkKjjjjKkjk..
..kjjjjnnjjjjk..
..kjjjjnnjjjjk..
..kKjkkkkkkjKk..
..kKKkddddkKKk..
..kKKKkkkkKKKk..
..kKKKKKKKKKKk..
...kKKKKKKKKk...
....kKKKKKKk....
.....kkkkkk.....
""",
    "blank": """
................
.....kkkkkk.....
....knnnnnnk....
...knwwwwwwnk...
...kwwwwwwwwk...
...kwkkwwkkwk...
...kwwwwwwwwk...
...kwwwnnwwwk...
...kwwwnnwwwk...
...kwwwwwwwwk...
...kwwkkkkwwk...
...kwwwwwwwwk...
....kwwwwwwk....
.....kwwwwk.....
......kkkk......
................
""",
}


def mask_on_peg(name, drop=0):
    """A mask hung from a peg, as a 1x1 wall piece (art shifted down by drop)."""
    rows = MASKS[name].strip("\n").split("\n")
    rows = ["." * 16] * drop + rows
    return "\n".join(rows[:16])


for _m in MASKS:
    stamp(f"mask_{_m}", 1, 1, art=[("nature", mask_on_peg(_m))],
          note=f"a {_m} mask hung on the wall")


# ---- the Asclepeion ---------------------------------------------------------

def _counter(kind):
    """The healer's counter of carved stone: 4x2. Row 0: two empty cells (the
    healing basin stands there), the healer's cell (the slab's lip on the top
    layer) and the slab's end with votives. Row 1: the carved front, all
    MB_COUNTER, a serpent winding through ivy, the runnel's arch under it."""
    W, H = 64, 32
    g = _canvas(W, H)
    top = _canvas(W, H)
    for y in range(6, 16):
        for x in range(32, 63):
            if y == 6 or x == 62:
                c = "k"
            elif y == 7:
                c = "M"
            elif y >= 13:
                c = "n" if y < 15 else "k"
            else:
                c = "M" if (x + y) % 11 else "m"
            (top if x < 48 else g)[y][x] = c
    for y in range(16, 31):
        for x in range(1, 63):
            if x in (1, 62) or y in (16, 30):
                c = "k"
            elif y in (17, 29):
                c = "m"
            elif y in (18, 28):
                c = "n"
            else:
                c = "M"
            g[y][x] = c
    for x in range(3, 61):                      # the serpent
        yy = int(round(23 + 3 * math.sin((x - 3) / 58 * math.pi * 4)))
        g[yy][x] = "z"
        g[yy - 1][x] = "b" if x % 2 else "y"
        if x % 6 == 0:
            for (dx, dy) in ((0, -3), (1, -3), (-1, -2), (0, -2), (1, -2), (2, -2), (0, 3), (1, 3), (0, 2), (1, 2), (-1, 2)):
                if 19 <= yy + dy <= 27:
                    g[yy + dy][x + dx] = "g"
    g[21][60] = "k"
    g[22][60] = "y"
    for (x, y, c) in [(52, 26, "k"), (53, 25, "k"), (54, 25, "k"), (55, 25, "k"), (56, 26, "k"),
                      (52, 27, "k"), (53, 27, "u"), (54, 27, "U"), (55, 27, "u"), (56, 27, "k"),
                      (52, 28, "k"), (53, 28, "U"), (54, 28, "u"), (55, 28, "U"), (56, 28, "k"),
                      (52, 29, "k"), (53, 29, "u"), (54, 29, "U"), (55, 29, "u"), (56, 29, "k")]:
        g[y][x] = c
    for (x, y, c) in [(50, 8, "k"), (51, 8, "z"), (52, 8, "z"), (53, 8, "z"), (53, 9, "z"), (53, 10, "k"),
                      (50, 9, "k"), (51, 9, "b"), (52, 9, "b"), (54, 10, "z"),
                      (56, 7, "k"), (57, 7, "k"), (58, 7, "k"), (59, 7, "k"), (56, 8, "k"), (57, 8, "M"),
                      (58, 8, "u"), (59, 8, "k"), (56, 9, "k"), (57, 9, "k"), (58, 9, "k"), (59, 9, "k")]:
        g[y][x] = c
    return _text(g), _text(top)


_c, _ct = _counter("asc")
stamp("asc_counter", 4, 2, art=[("bronze", _c)], top=[("bronze", _ct)],
      walk={(2, 0)},
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER", (3, 1): "MB_COUNTER"},
      note="the healer's counter, carved stone: a serpent through ivy, the runnel's arch under it")


def _basin():
    """The healing basin beside the counter, 2x2: a bronze serpent spout on the
    wall pours into a marble basin. The party's balls land on its water."""
    g = _canvas(32, 32)
    # spout plate and serpent head on the wall (rows 0-15)
    for y in range(2, 12):
        for x in range(11, 21):
            edge = x in (11, 20) or y in (2, 11)
            g[y][x] = "k" if edge else ("y" if (x + y) % 5 == 0 else "b")
    for (x, y, c) in [(14, 4, "k"), (15, 4, "k"), (16, 4, "k"), (17, 4, "k"), (14, 5, "z"), (15, 5, "y"), (16, 5, "y"),
                      (17, 5, "z"), (15, 6, "k"), (16, 6, "k"), (15, 7, "Y"), (16, 7, "z"), (12, 9, "g"), (13, 8, "g"),
                      (18, 8, "g"), (19, 9, "g"), (12, 3, "g"), (19, 3, "g")]:
        g[y][x] = c
    for y in range(12, 20):                     # the stream of water
        g[y][15] = "U"
        g[y][16] = "M" if y % 3 else "U"
    # the basin (rows 16-31)
    cx, cy = 15.5, 23.0
    for y in range(15, 31):
        for x in range(1, 31):
            dx, dy = (x - cx) / 14.5, (y - cy) / 7.5
            r = dx * dx + dy * dy
            if r > 1.0:
                continue
            ri = (x - cx) ** 2 / 11.5 ** 2 + (y - 21.5) ** 2 / 4.2 ** 2
            if r > 0.86:
                c = "k"
            elif ri <= 1.0:
                c = "u" if ri > 0.75 else ("U" if (x * 3 + y * 5) % 13 else "M")
            elif y > 25:
                c = "n" if r > 0.6 else "m"
            else:
                c = "M"
            g[y][x] = c
    for (x, y) in [(13, 20), (14, 20), (18, 22), (19, 22)]:
        g[y][x] = "M"
    return _text(g)


stamp("asc_basin", 2, 2, art=[("bronze", _basin())],
      note="the healing basin: Dirke's water from an ivy-wreathed bronze serpent into a marble bowl")


def _pool():
    """The spring of Dirke in the courtyard's middle: a sunken marble pool, 3x2,
    its water clear and moving, a runnel leaving north toward the counter."""
    W, H = 48, 32
    g = _canvas(W, H)
    for y in range(0, 31):
        for x in range(0, 48):
            ox = min(x - 1, 46 - x)
            oy = min(y - 2, 29 - y)
            if ox < 0 or oy < 0:
                continue
            corner = ox < 3 and oy < 3 and (3 - ox) ** 2 + (3 - oy) ** 2 > 9
            if corner:
                continue
            if ox == 0 or oy == 0:
                c = "k"
            elif ox == 1 or oy == 1:
                c = "M" if (y < 16 or ox == 1) else "m"
            elif ox == 2 or oy == 2:
                c = "n"
            elif ox == 3 or oy == 3:
                c = "z"
            else:
                c = "u" if oy < 6 else "U"
                if oy > 6 and (x % 8, y % 8) in ((1, 2), (2, 2), (5, 6), (6, 6)):
                    c = "M"
            g[y][x] = c
    # a few lily-like leaves of ivy fallen on the water
    for (x, y) in [(10, 18), (11, 18), (11, 17), (36, 12), (37, 12)]:
        g[y][x] = "g"
    # the runnel's mouth at the top rim
    for y in range(0, 6):
        for x in (22, 23, 24, 25):
            g[y][x] = "k" if x in (22, 25) else ("U" if y < 5 else "u")
    return _text(g)


stamp("spring_pool", 3, 2, art=[("bronze", _pool())],
      note="the spring of Dirke: a sunken marble pool in the courtyard, its runnel leaving for the counter")

stamp("runnel", 1, 1, art=[("bronze", """
.....knnnnk.....
.....kUuUuk.....
.....kuUMuk.....
.....kUuUuk.....
.....kuUuUk.....
.....kUuUMk.....
.....kuUuUk.....
.....kUuUuk.....
.....kuMuUk.....
.....kUuUuk.....
.....kuUuUk.....
.....kUuUuk.....
.....kuUuMk.....
.....kUuUuk.....
.....kuUuUk.....
.....knnnnk.....
""")], walk={(0, 0)}, note="the stone runnel carrying the spring's water under the counter")


stamp("asc_statue", 1, 2, art=[("bronze", """
......kkkk......
.....kMMMmk.....
.....kMmmmk.....
......kmmk......
..k..kMMMmk.....
.kgk.kMMMMmk....
kgykkMMMMMmmk...
.kzkkMMgMMMmk...
.kykkMgggMMmk...
.kzk.kMgMMmmk...
.kyk.kMMMMmmk...
.kzk.kMMMMmmk...
.kyk.kMMMMmmk...
.kzkkMMMMMmmmk..
.kykMMMMMMMmmk..
.kzkMMMMMMmmmk..
.kykkMMMMMmmk...
.kzk.kMMMMmmk...
.kyk.kMMmMmmk...
.kzk.kMMmMmmk...
.kyk.kMMmMmnk...
.kzkkMMMmMmnk...
.kkkMMMMmmmnnk..
.kMMMMMMMMMMMk..
kMkkkkkkkkkkkMk.
kMMMMMMMMMMMMMk.
knnnnnnnnnnnnnk.
kmnmnmnmnmnmnmk.
kMMMMMMMMMMMMMk.
knnnnnnnnnnnnnk.
.kkkkkkkkkkkkk..
................
""")], note="Asclepius, his staff wound with a serpent and, for Thyrsa, a little ivy")


def _post(masks=(), canopy=True):
    """A pergola post, 1x2: the post (nature wicker-browns) with thank-offering
    masks hung on it in the lower cell; the upper cell and the vine canopy over
    it go on the top layer, so walkers pass behind."""
    mid = _canvas(16, 32)
    top = _canvas(16, 32)
    for y in range(0, 31):
        tgt = top if y < 16 else mid
        for (x, c) in ((6, "k"), (7, "J"), (8, "j"), (9, "K"), (10, "k")):
            tgt[y][x] = c
        if y % 6 == 0:
            tgt[y][8] = "K"
    for x in range(5, 12):
        mid[30][x] = "k"
        mid[31][x] = "k" if x in (5, 11) else "K"
    if canopy:
        leaves = ["...G..GG...G....", "..GgGGvgG.GgG...", ".GvVgGgVggGvgG..", "GgVvggGgvVggVgGG",
                  "GgvgGVggGgvgGvgG", ".GgGvgPpgGgVgG..", "..GGgpPpGGgG....", "...kGpPpkGG.....",
                  "....kpPk........", ".....kk........."]
        for dy, row in enumerate(leaves):
            for dx, c in enumerate(row):
                if c != ".":
                    top[dy][dx] = c
    for (name, dy, dx) in masks:
        rows = MASKS[name].strip("\n").split("\n")
        for yy, row in enumerate(rows):
            for xx, c in enumerate(row):
                if c != "." and 0 <= dy + yy < 32:
                    if dx + xx < 0 or dx + xx > 15:
                        continue
                    mid[dy + yy][dx + xx] = c
    return _text(mid), _text(top)


_m, _t = _post(masks=(("comic", 16, 4),))
stamp("post_comic", 1, 2, art=[("nature", _m)], top=[("nature", _t)], walk={(0, 0)},
      note="a pergola post under the vine, a comic mask hung on it in thanks")
_m, _t = _post(masks=(("tragic", 16, 4),))
stamp("post_tragic", 1, 2, art=[("nature", _m)], top=[("nature", _t)], walk={(0, 0)},
      note="a pergola post, a tragic mask hung on it: an actor, well again")
_m, _t = _post(masks=(("satyr", 16, 4),))
stamp("post_satyr", 1, 2, art=[("nature", _m)], top=[("nature", _t)], walk={(0, 0)},
      note="a pergola post, a satyr mask hung on it: the kordax, survived")


def _vines(seed):
    """The pergola's canopy between posts, 1x1 on the top layer: a beam lost in
    vine leaves, a bunch of grapes hanging through."""
    g = _canvas(16, 16)
    for x in range(16):
        g[2][x] = "k"
        g[3][x] = "J"
        g[4][x] = "K"
        g[5][x] = "k"
    for y in range(0, 11):
        for x in range(16):
            n = (x * 7 + y * 13 + seed * 5) % 11
            band = abs(y - 5) < 6 - (1 if (x + seed) % 5 == 0 else 0)
            if band and n < 9:
                g[y][x] = "G" if n < 2 else "g" if n < 5 else "v" if n < 6 else "V"
    bx = 5 + seed * 4
    for (dx, dy, c) in [(0, 8, "k"), (1, 8, "p"), (2, 8, "k"), (-1, 9, "k"), (0, 9, "P"), (1, 9, "s"), (2, 9, "P"),
                        (3, 9, "k"), (0, 10, "p"), (1, 10, "P"), (2, 10, "p"), (0, 11, "k"), (1, 11, "p"), (2, 11, "k"),
                        (1, 12, "k"), (-1, 10, "k"), (3, 10, "k")]:
        _put(g, bx + dx, dy, c)
    return _text(g)


stamp("vines_a", 1, 1, top=[("nature", _vines(0))], walk={(0, 0)},
      note="the pergola's vine canopy, a bunch of grapes hanging through")
stamp("vines_b", 1, 1, top=[("nature", _vines(1))], walk={(0, 0)},
      note="the pergola's vine canopy")

stamp("pithos_great", 1, 2, art=[("clay", """
....kkkkkkkk....
...kSttttttSk...
...kssSSSSssk...
..kkkkkkkkkkkk..
.kdmllhhhllmmdk.
kdmlhhhhhllmmmdk
kdlhhcnnchlmmmdk
kmlhcnYYnchlmmdk
kmlhcnYYnchmmmdk
kmlhhcnnchlmmddk
kdmlhhhhhlmmmddk
kkkkkkkkkkkkkkkk
kdmllhhhlllmmddk
kdmlllhhllmmmddk
kkkkkkkkkkkkkkkk
kdmllhhhllmmmddk
kdmlllhhllmmmddk
kdmlllhlllmmmddk
.kdmllllllmmddk.
.kdmmlllllmmddk.
.kkkkkkkkkkkkkk.
.kdmmlllllmmddk.
..kdmmlllmmddk..
..kddmmmmmdddk..
...kddmmmmddk...
....kkdddddk....
.....kkkkkk.....
................
................
................
................
................
""")], note="the Pithos: a great storage jar, rope-banded, its golden wax seal faintly glowing")


# ---- the Agora --------------------------------------------------------------

def _wood_counter(goods):
    """A market counter, 3x2: the timber top with goods, the keeper's cell in
    the middle (the counter's lip on the top layer), and a front of planks
    painted with a wine-dark band, MB_COUNTER."""
    W, H = 48, 32
    g = _canvas(W, H)
    top = _canvas(W, H)
    for y in range(8, 16):
        for x in range(1, 47):
            if y == 8 or x in (1, 46):
                c = "k"
            elif y == 9:
                c = "h"
            elif y == 15:
                c = "k"
            elif y == 14:
                c = "m"
            else:
                c = "l"
            (top if 16 <= x < 32 else g)[y][x] = c
    for y in range(16, 31):
        for x in range(1, 47):
            if x in (1, 46) or y in (16, 30):
                c = "k"
            elif y in (19, 20):
                c = "R" if y == 19 else "r"
            elif y == 21:
                c = "y"
            else:
                c = "m" if x % 8 else "d"
            g[y][x] = c
    for (x, y, c) in goods:
        if 0 <= x < W and 0 <= y < H:
            g[y][x] = c
    return _text(g), _text(top)


_GOODS = []
for (ox, oy) in ((4, 2), (10, 3)):              # two neat stacks of flat loaves and a jar
    for (dx, dy, c) in [(0, 0, "k"), (1, 0, "k"), (2, 0, "k"), (3, 0, "k"), (-1, 1, "k"), (0, 1, "h"), (1, 1, "h"),
                        (2, 1, "l"), (3, 1, "l"), (4, 1, "k"), (-1, 2, "k"), (0, 2, "l"), (1, 2, "l"), (2, 2, "m"),
                        (3, 2, "m"), (4, 2, "k"), (0, 3, "k"), (1, 3, "k"), (2, 3, "k"), (3, 3, "k")]:
        _GOODS.append((ox + dx, oy + dy + 4, c))
for (dx, dy, c) in [(36, 4, "k"), (37, 4, "k"), (35, 5, "k"), (36, 5, "c"), (37, 5, "C"), (38, 5, "k"), (35, 6, "k"),
                    (36, 6, "C"), (37, 6, "C"), (38, 6, "k"), (35, 7, "k"), (36, 7, "C"), (37, 7, "d"), (38, 7, "k"),
                    (36, 8, "k"), (37, 8, "k"), (41, 6, "k"), (42, 6, "k"), (43, 6, "k"), (41, 7, "u"), (42, 7, "U"),
                    (43, 7, "u"), (41, 8, "k"), (42, 8, "k"), (43, 8, "k")]:
    _GOODS.append((dx, dy + 3, c))
_c, _ct = _wood_counter(_GOODS)
stamp("ago_counter", 3, 2, art=[("wood", _c)], top=[("wood", _ct)], walk={(1, 0)},
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER"},
      note="the goods counter: loaves, a linen bale, blue dye; its front painted wine-dark")

_WINE = []
for i, ox in enumerate((3, 9, 35, 41)):        # cups and a jug of wine on the counter
    for (dx, dy, c) in [(0, 0, "k"), (1, 0, "k"), (2, 0, "k"), (3, 0, "k"), (0, 1, "k"), (1, 1, "R"), (2, 1, "R"),
                        (3, 1, "k"), (-1, 0, "k" if i % 2 else "."), (4, 0, "k" if i % 2 else "."), (1, 2, "k"), (2, 2, "k")]:
        _WINE.append((ox + dx, dy + 9, c))
_c, _ct = _wood_counter(_WINE)
stamp("wine_counter", 3, 2, art=[("wood", _c)], top=[("wood", _ct)], walk={(1, 0)},
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER"},
      note="the wine-and-offerings counter: two-handled cups of dark wine")


def _side_counter():
    """The goods counter's arm, running north-south: 1x3, its front facing east,
    every cell MB_COUNTER."""
    g = _canvas(16, 48)
    for y in range(2, 47):
        for x in range(2, 15):
            if x in (2, 14) or y in (2, 46):
                c = "k"
            elif x >= 11:
                c = "R" if x == 11 else ("r" if x == 12 else "d")
            elif x == 3:
                c = "h"
            else:
                c = "l" if x < 9 else "m"
            g[y][x] = c
    for (oy, kind) in ((6, "sack"), (20, "olives"), (34, "sack")):
        if kind == "sack":
            art = ["..kkk..", ".kcccCk", "kcCcCCk", "kcccCCk", "kCcCCCk", ".kCCCk.", "..kkk.."]
        else:
            art = ["..kkk..", ".kmmmk.", "kmoooomk"[:7], "kooookk", "koookok", ".kmmmk.", "..kkk.."]
        for dy, row in enumerate(art):
            for dx, c in enumerate(row):
                if c != ".":
                    g[oy + dy][3 + dx] = c
    return _text(g)


stamp("side_counter", 1, 3, art=[("wood", _side_counter())],
      behavior={(0, 0): "MB_COUNTER", (0, 1): "MB_COUNTER", (0, 2): "MB_COUNTER"},
      note="the goods counter's arm, at right angles: sacks of barley and a bowl of olives")


def _pyramid():
    g = _canvas(32, 32)

    def amph(ox, oy):
        art = ["...kk...", "..kmmk..", "..kdmk..", ".kkmmkk.", "kmlhhlmk", "kmlhllmk", "kmlllmdk",
               "kdmlmmdk", ".kdmmdk.", "..kddk..", "...kk..."]
        for dy, row in enumerate(art):
            for dx, c in enumerate(row):
                if c != ".":
                    _put(g, ox + dx, oy + dy, c)
    for (ox, oy) in [(12, 0), (8, 9), (16, 9), (4, 18), (12, 18), (20, 18)]:
        amph(ox, oy)
    for x in range(2, 30):
        _put(g, x, 29, "k")
        _put(g, x, 30, "s" if 2 < x < 29 else "k")
        _put(g, x, 31, "k")
    return _text(g)


stamp("amphora_pyramid", 2, 2, art=[("clay", _pyramid())],
      note="wine amphorae stacked in a pyramid")

stamp("chalk_board", 1, 2, art=[("clay", """
................
................
..kkkkkkkkkkkk..
..kddddddddddk..
..kdaaaaaaaadk..
..kdaccacacadk..
..kdaaaaaaaadk..
..kdacacaccadk..
..kdaaaaaaaadk..
..kdacaccacadk..
..kdaaaaaaaadk..
..kdaccacacadk..
..kdaaaaaaaadk..
..kdacacaccadk..
..kdaaaaaaaadk..
..kdcaccaacadk..
..kdaaaaaaaadk..
..kddddddddddk..
..kkkkkkkkkkkk..
...kdk....kdk...
...kdk....kdk...
..kdk......kdk..
..kdk......kdk..
.kdk........kdk.
.kdk........kdk.
.kkk........kkk.
................
................
................
................
................
................
""")], note="a chalk board of the day's prices on its easel")


def _vat():
    g = _canvas(32, 32)
    cx, cy = 15.5, 12.0
    for y in range(2, 31):
        for x in range(1, 31):
            dx = (x - cx) / 14.5
            if y <= 12:
                dy = (y - cy) / 9.5
                if dx * dx + dy * dy > 1.0:
                    continue
                rim = dx * dx + ((y - 8.5) / 6.5) ** 2
                inner = dx * dx * 1.2 + ((y - 9.0) / 5.0) ** 2
                if inner <= 1.0:
                    c = "R" if inner > 0.55 else "d"
                elif rim > 0.9 or (dx * dx + dy * dy) > 0.9:
                    c = "k"
                else:
                    c = "h"
            else:
                if abs(dx) > 1.0 - (y - 12) * 0.006:
                    continue
                if abs(dx) > 0.92 - (y - 12) * 0.006 or y == 30:
                    c = "k"
                elif y in (16, 17, 25, 26):
                    c = "b" if y in (16, 25) else "z"
                else:
                    c = "l" if dx < -0.4 else ("m" if dx < 0.5 else "d")
                    if (x % 5) == 0:
                        c = "d"
            g[y][x] = c
    return _text(g)


stamp("tread_vat", 2, 2, art=[("wood", _vat())],
      note="a grape-treading vat by the back door, empty, stained wine-dark")

stamp("back_door", 1, 2, flat=[("wall", """
................
................
................
................
................
................
..kkkkkkkkkkkk..
..k2222222222k..
..k2kkkkkkkk2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332ko2k2k..
..k2k332ko2k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k332332k2k..
..k2k111111k2k..
..k2kkkkkkkk2k..
..kkkkkkkkkkkk..
""")], note="the market hall's back door, shut")

stamp("sacks", 1, 1, art=[("wood", """
................
................
....kk.....kk...
...kcck...kcck..
..kccCck.kccCCk.
.kcCcCCkkcCcCCk.
.kccCcCCkcccCCk.
.kcCcCCCkcCcCCk.
.kccCcCCkccCCCk.
.kcCCCCCkcCCCCk.
..kCCCCk.kCCCk..
...kkkk...kkk...
................
................
................
................
""")], note="sacks of barley")


# ---- the Kantharos ---------------------------------------------------------

_BAR = []
for (ox, oy) in ((4, 4), (11, 5)):            # jugs at one end
    for (dx, dy, c) in [(1, 0, "k"), (2, 0, "k"), (0, 1, "k"), (1, 1, "l"), (2, 1, "m"), (3, 1, "k"), (0, 2, "k"),
                        (1, 2, "h"), (2, 2, "m"), (3, 2, "k"), (4, 2, "k"), (0, 3, "k"), (1, 3, "l"), (2, 3, "d"),
                        (3, 3, "k"), (1, 4, "k"), (2, 4, "k")]:
        _BAR.append((ox + dx, oy + dy + 3, c))
for ox in (35, 40):                            # cups, and the bones' leather cup
    for (dx, dy, c) in [(0, 0, "k"), (1, 0, "k"), (2, 0, "k"), (3, 0, "k"), (0, 1, "k"), (1, 1, "R"), (2, 1, "R"),
                        (3, 1, "k"), (1, 2, "k"), (2, 2, "k")]:
        _BAR.append((ox + dx, dy + 9, c))
_c, _ct = _wood_counter(_BAR)
stamp("bar", 3, 2, art=[("wood", _c)], top=[("wood", _ct)], walk={(1, 0)},
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER"},
      note="the Kantharos's bar: jugs, cups, the dice-cup")

stamp("great_cup", 2, 1, art=[("clay", """
...............kk...............
..............kssk..............
..kkk..........kk..........kkk..
.kaaak.........kk.........kaaak.
kak.kak.......kssk.......kak.kak
kak..kak.kkkkkkkkkkkkkk.kak..kak
kak...kakaaaaaaaaaaaaaakak...kak
.kak..kkcaaaaaaaaaaaaakk..kak...
..kakkkacaaaaaaaaaaaaaaakkkak...
...kkaacaammmmmmmmmmaaaaakk.....
.....kaacaaaaaaaaaaaaaaak.......
......kaacaaaaaaaaaaaaak........
.......kkaaaaaaaaaaaakk.........
.........kkkaaaaaakkk...........
...........kaaaaaak.............
..........kkkkkkkkkk............
""")], note="the great kantharos over the bar, two high handles, black glaze with a red band")


def _pit():
    """The sunken floor, 4x3, stone (flat, over the floor art): a step down all
    round, its north and west risers in shadow, the floor inside darker and worn
    smooth. Walkable."""
    W, H = 64, 48
    g = _canvas(W, H)
    for y in range(H):
        for x in range(W):
            if y == 0 or x == 0:
                c = "k"
            elif y == H - 1 or x == W - 1:
                c = "5"                       # the far lip catches the light
            elif y <= 4 or x <= 3:
                # the north and west risers, seen from above, in shadow
                d = min(y, x)
                c = "1" if d <= 2 else "2"
                if y <= 4 and x > 3 and y == 4:
                    c = "2"
            elif y == H - 2 or x == W - 2:
                c = "4"
            else:
                c = "2"
                if (x % 8, y % 8) in ((2, 3), (6, 7), (5, 1)):
                    c = "3"
            g[y][x] = c
    return _text(g)


stamp("pit", 4, 3, flat=[("stone", _pit())],
      walk={(x, y) for x in range(4) for y in range(3)},
      note="the sunken floor where the knucklebones are thrown, worn into a shallow bowl")

stamp("kb_table", 1, 1, art=[("stone", """
....kkkkkkkk....
..kk55555555kk..
.k555444444555k.
k55443333334455k
k54332222223345k
k5432k6k2k6k345k
k5432k66k66k345k
k54322k6kk2k345k
k5433k66k2223345
.k5433333333345k
.k4554444444553k
..kk33333333kk..
...k2k2222k2k...
...k2k....k2k...
...kkk....kkk...
................
""")], note="the knucklebones table: stone worn into a shallow bowl, four bones in the hollow")


def _stairs_up_s():
    """Five steps rising south out of the cellar to the street: 2x1, both cells
    south-arrow warps."""
    g = _canvas(32, 16)
    for y in range(16):
        for x in range(32):
            if x in (0, 31):
                c = "k"
            elif x in (1, 30):
                c = "2"
            else:
                step = y // 3
                c = ["2", "3", "4", "5", "6", "6"][step] if y % 3 else "1"
            g[y][x] = c
    return _text(g)


stamp("stairs_up_s", 2, 1, flat=[("stone", _stairs_up_s())], walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"},
      note="the five steps up to the street; both cells are the exit")


def _rack():
    g = _canvas(32, 32)
    for y in range(4, 31):
        for x in range(1, 31):
            if x in (1, 2, 29, 30) or y in (4, 5, 17, 18, 29, 30):
                c = "k" if (x in (1, 30) or y in (4, 30)) else ("h" if y in (5, 18) else "m")
                g[y][x] = c
    for (oy) in (6, 19):
        for (ox) in (3, 12, 21):
            art = [".kkkkk.", "kdmllhk", "kdmlhhkk", "kdmmllk", ".kkkkk."]
            for dy, row in enumerate(art):
                for dx, c in enumerate(row):
                    if c != ".":
                        _put(g, ox + dx, oy + 2 + dy, c)
            for dy in range(3):
                _put(g, ox + 7, oy + 3 + dy, "d")
                _put(g, ox + 8, oy + 3 + dy, "k")
    return _text(g)


stamp("wine_rack", 2, 2, art=[("wood", _rack())],
      note="a timber rack of wine amphorae lying on their sides")

stamp("wall_lamp", 1, 1, flat=[("stone", """
................
.......ll.......
......lLLl......
.....lLLLLl.....
.....lLLLLl.....
......lLLl......
.......ll.......
................
................
................
................
................
................
................
................
................
""")], art=[("bronze", """
................
................
.......f........
.......F........
......fef.......
......FeF.......
.......k........
....kkkkkkk.....
...kyyyyyybk....
....kzbbbzk.....
......kzk.......
......kbk.......
.....kkbk.......
.....kbbk.......
......kk........
................
""")], note="an oil lamp on a bronze bracket, its glow on the stone")


# ---- pass 3 (in-game): the heal's glow wants something to light -----------

stamp("rod_relief", 1, 2, art=[("bronze", """
................
................
................
................
................
................
....kkkkkkkk....
...kyyyyyyyyk...
...kyMMMMMMbk...
...kyMMkkMMbk...
...kyMkyyMMbk...
...kyMMzkMMbk...
...kyMkzMgMbk...
...kyMMgyMMbk...
...kyMkzkgMbk...
...kyMgyMMMbk...
...kyMkzgMMbk...
...kyMMyMgMbk...
...kyMkzkMMbk...
...kyMgyMMMbk...
...kyMMzMMMbk...
...kyMMzMMMbk...
...kyMMzMMMbk...
...kbbbbbbbbk...
....kkkkkkkk....
................
................
................
................
................
................
................
""")], note="a painted plaque of the rod of Asclepius, its serpent wound with ivy, over the healer")
