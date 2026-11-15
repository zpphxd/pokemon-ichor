#!/usr/bin/env python3
"""Pixel art for the limen tileset: Emporion's harbor-town interiors.

limen ("harbor") is the secondary for Emporion's rooms that aren't a forge or
an Asclepeion: the Deigma (the merchants' exchange), the Dolphin tavern,
Philoxenos's andron, the widow's room over the rope-walk, the runners'
barracks, Euphronios's workshop and the Titans' hiring hall. ergasteria had
about a hundred tiles left after Aegina, and the Hephaisteion's forge took
them, so these seven rooms get a set of their own, in the same style.

It is built the way oikia and ergasteria are: hand-drawn character grids, one
character per color, '.' for clear, with char_canvas.Canvas for the larger
pieces. Its palettes are oikia's seven, so every piece of the slice's
furniture (tables, couches, jars, the loom, the hearth, the mat) is taken from
oikia_art.py pixel for pixel; the cloth palette gains Tyrian purple for the
Deigma's wool.

Palettes:
  wall    oikia's: beams, whitewash, red and Aegean dados, shutters, sky; also
          the sea through a window, the ashlar, the warehouse's planks
  floor   oikia's: terracotta, boards, limestone
  wood    oikia's: furniture woods, bronze fittings, linen, cloth
  clay    oikia's: pottery, hearth stone, fire, soot, slip; the kiln, the
          wheel, the potter's clay-dust floor
  cloth   oikia's rug colors, plus Tyrian purple: bolts of wool, the curtain
  nature  oikia's: plants, wicker, fish, rope: straw pallets, the hoist
  bronze  oikia's: bronze, flame, water, marble: helmets, the mosaics

limen_build.py builds the set; tools/ichor/maps/emporion_rooms.py lays out
the rooms.
"""
import copy

import numpy as np

import ergasteria_art as EA
import oikia_art as O
from char_canvas import Canvas

INK = O.INK

PALETTES = copy.deepcopy(O.PALETTES)
PALETTES["cloth"].update({
    "p": (96, 32, 88),     # Tyrian purple, dark
    "P": (152, 64, 136),   # Tyrian purple
    "q": (200, 120, 184),  # purple, lit
})

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


def as_text(img, pal):
    """An RGBA piece back to characters of one palette (for recoloring)."""
    inv = {rgb: ch for ch, rgb in PALETTES[pal].items()}
    rows = []
    for y in range(img.shape[0]):
        rows.append("".join(inv[tuple(int(v) for v in img[y, x, :3])] if img[y, x, 3] else "."
                            for x in range(img.shape[1])))
    return rows


# --------------------------------------------------------------------------
# Floors, walls, void, rugs
# --------------------------------------------------------------------------

FLOORS = {k: dict(v) for k, v in O.FLOORS.items()}     # terracotta, boards, flags


def _claydust(variant):
    """Euphronios's floor: trodden earth gray with dried clay and slip, a
    speckle that repeats every 8 pixels, shadowed under the wall."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            h = ((x % 8) * 41 + (y % 8) * 23 + (x % 8) * (y % 8) * 7) % 31
            c.put(x, y, "t" if h in (0, 17) else "s" if h == 21 else "S")
    if variant in ("top", "corner"):
        c.hline(0, 15, 0, "a")
        c.hline(0, 15, 1, "s")
        c.hline(0, 15, 2, "s")
        for x in range(0, 16, 2):
            c.put(x, 3, "s")
    if variant in ("left", "corner"):
        c.vline(0, 0, 15, "a")
        c.vline(1, 0, 15, "s")
    if variant == "alt":
        for (x, y, ch) in [(3, 4, "d"), (4, 4, "m"), (4, 5, "d"), (11, 10, "m"), (12, 10, "l"), (9, 13, "a")]:
            c.put(x, y, ch)
    return grid("clay", c.text())


FLOORS["claydust"] = {v: _claydust(v) for v in ("plain", "alt", "top", "left", "corner")}


def _sea(variant):
    """The harbor beyond the Deigma's open side: blue water with wavelets that
    repeat every 8 pixels. On its left edge ("left") the quay's stone lip."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            ch = "b"
            if (y % 8 == 2 and x % 8 in (1, 2, 3)) or (y % 8 == 6 and x % 8 in (5, 6, 7)):
                ch = "B"
            if y % 8 == 2 and x % 8 == 2 or y % 8 == 6 and x % 8 == 6:
                ch = "a"
            c.put(x, y, ch)
    if variant == "left":
        c.rect(0, 0, 4, 15, "S")
        c.vline(0, 0, 15, "s")
        c.vline(1, 0, 15, "p")
        c.vline(4, 0, 15, "1")
        c.vline(5, 0, 15, "k")
        for y in (3, 11):
            c.hline(1, 4, y, "s")
        c.vline(6, 0, 15, "1")
    return grid("wall", c.text())


FLOORS["sea"] = {"plain": _sea("plain"), "left": _sea("left")}

WALLS = {
    "red": O.WALLS["red"],
    "blue": O.WALLS["blue"],
    "stone": EA.WALLS["stone"],
}


def _wall_timber():
    """The hiring hall's warehouse wall: the roof beam, then upright planks
    nailed to rails, dark at the seams, on a low stone plinth."""
    rows = ["k" * 16, "2" * 16, "3" * 16, "2" * 16, "1" * 16, "k" * 16]
    for y in range(6, 28):
        row = []
        for x in range(16):
            px = x % 8
            if y in (10, 22):
                ch = "1" if y == 10 else "1"
            elif y in (11, 23):
                ch = "3" if px != 0 else "1"
            elif px == 0:
                ch = "k"
            elif px == 1:
                ch = "3"
            elif px == 7:
                ch = "1"
            else:
                ch = "2" if (y * 3 + px) % 11 else "1"
            row.append(ch)
        rows.append("".join(row))
    for (y, x) in ((11, 3), (11, 4), (23, 3), (23, 4)):
        r = list(rows[y])
        r[x] = "k"
        r[x + 8] = "k"
        rows[y] = "".join(r)
    rows += ["k" * 16, "S" * 16, "s" * 16, "k" * 16]
    assert len(rows) == 32
    return grid("wall", "\n".join(rows))


def _wall_tavern():
    """The Dolphin's wall: a low, heavy, smoke-darkened beam, yellowed plaster
    with old smoke at the top, and the red ochre dado of oikia's homes."""
    red = O.WALLS["red"]
    rows = as_text(red, "wall")
    rows = rows[:]
    rows[0:9] = ["k" * 16, "1" * 16, "2" * 16, "3" * 16, "2" * 16, "1" * 16, "1" * 16,
                 "k1k1k1k1k1k1k1k1", "1S1S1S1S1S1S1S1S"]
    for y in range(9, 21):
        r = list(rows[y])
        for x in range(16):
            if r[x] in "pw":
                r[x] = "S" if y < 11 and (x + y) % 3 else ("s" if y < 14 else ("s" if (x * 5 + y) % 7 == 0 else "p"))
        rows[y] = "".join(r)
    return grid("wall", "\n".join(rows))


WALLS["timber"] = _wall_timber()
WALLS["tavern"] = _wall_tavern()

VOID = O.VOID
RUGS = {"red": O.RUGS["red"], "blue": O.RUGS["blue"]}

# --------------------------------------------------------------------------
# Stamps. oikia's contract: w, h in metatiles; walk cells the player may stand
# on; behavior per cell; `top` art over the player; `flatten` puts the art in
# the bottom layer.
# --------------------------------------------------------------------------

STAMPS = {}

SHARED_OIKIA = ["window", "niche", "herbs", "jar_shelf", "honey_shelf", "kline", "klismos_r",
                "klismos_l", "stool", "table", "table_round", "desk", "oars", "scrolls", "chest",
                "loom", "altar", "trident", "nets", "klepsydra", "kalathos", "amphora",
                "amphora_plain", "pithos", "pots", "hearth", "soot", "myrtle", "fish_basket",
                "knucklebones", "lampstand", "column", "mat", "stairs_down_wood", "boat",
                "mortar", "niche_horse"]          # these two for Eleusa's rooms (eleusa_rooms.py)
for _name in SHARED_OIKIA:
    STAMPS[_name] = dict(O.STAMPS[_name], source="oikia")
for _name in ("bench", "scales", "hearth_floor"):
    STAMPS[_name] = dict(EA.STAMPS[_name], source="ergasteria")


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note=""):
    """w, h in metatiles. walk: cells (cx, cy) the player may stand on.
    behavior: {(cx, cy): 'MB_...'}."""
    if isinstance(art, Canvas):
        art = art.text()
    img = art if isinstance(art, np.ndarray) else grid(pal, art, w * 16, h * 16)
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    STAMPS[name] = {
        "pal": pal,
        "img": img,
        "top": grid(pal, top, w * 16, h * 16) if top else None,
        "w": w,
        "h": h,
        "walk": set(walk),
        "behavior": dict(behavior or {}),
        "flatten": flatten,
        "note": note,
        "source": "limen",
    }


def two_palettes(name, top_pal, top_art, bottom_pal, bottom_art, w, note, walk=(), behavior=None):
    """A one-row piece whose upper 8 pixel rows are drawn in one palette and
    lower 8 in another (goods on a trestle): each 8x8 tile keeps one palette."""
    a = grid(top_pal, top_art, w * 16, 16)
    b = grid(bottom_pal, bottom_art, w * 16, 16)
    img = a.copy()
    img[8:] = 0
    m = b[8:, :, 3] > 0
    img[8:][m] = b[8:][m]
    assert not (a[8:, :, 3] > 0).any(), f"{name}: the top art runs below row 8"
    assert not (b[:8, :, 3] > 0).any(), f"{name}: the bottom art runs above row 8"
    stamp(name, top_pal, img, w, 1, walk=walk, behavior=behavior, note=note)


# ===========================================================================
# Trestle tables. Every sample table in the Deigma, the potter's paint table
# and the crew boss's pay table share one trestle (a plank on crossed legs, in
# the bottom 8 pixel rows) under their own goods (everything above, in the
# goods' palette), so each new table costs only its goods' tiles. The samples
# stand 24 pixels tall on 2x2 tables, so they read at a glance; the crew
# boss's is a 2x1 counter.
# ===========================================================================

TRESTLE = """
................................
................................
................................
................................
................................
................................
................................
................................
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
kllllllllllllllllllllllllllllllk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
..kmk..kmk............kmk..kmk..
...kmkkmk..............kmkkmk...
...kkk.kk..............kkk.kk...
"""


def trestle(name, goods_pal, goods, note, behavior=None):
    """A 2x2 trestle: the goods in rows 0-23 (their own palette), the trestle
    in rows 24-31 (wood). The upper cells are all goods, so they read big."""
    a = grid(goods_pal, goods if isinstance(goods, str) else goods.text(), 32, 32)
    base = "\n".join(["." * 32] * 16 + TRESTLE.strip("\n").split("\n"))
    b = grid("wood", base, 32, 32)
    assert not (a[24:, :, 3] > 0).any(), f"{name}: the goods run below row 24"
    img = a.copy()
    m = b[..., 3] > 0
    img[m] = b[m]
    stamp(name, goods_pal, img, 2, 2, behavior=behavior, note=note)


def _amphora_shape(c, x, y, h, body="m", lit="l", dark="d"):
    """A standing transport amphora, 9 wide and h tall, its top-left at (x, y)."""
    c.paste([".k.kkk.k.",
             "kmk" + lit + "h" + lit + "kmk",
             "kmkk" + lit + "kkmk",
             ".kk" + lit + body + body + "kk."], x, y)
    body_rows = h - 7
    for i in range(body_rows):
        t = i / max(body_rows - 1, 1)
        half = 4 if t < 0.45 else (3 if t < 0.7 else (2 if t < 0.88 else 1))
        cx = x + 4
        c.hline(cx - half, cx + half, y + 4 + i, body)
        c.put(cx - half + 1, y + 4 + i, lit)
        c.put(cx + half - 1, y + 4 + i, dark)
        c.put(cx - half - 1, y + 4 + i, "k")
        c.put(cx + half + 1, y + 4 + i, "k")
    c.paste(["...k.....", "..kdk....", "...k....."], x, y + 4 + body_rows)


def _lamps():
    """Lampis's samples: a stepped stand of clay oil lamps, three tiers."""
    c = Canvas(32, 32)
    for (y, n, x0) in ((5, 4, 6), (12, 5, 3), (19, 6, 1)):
        c.box(x0 - 1, y + 3, 32 - x0, y + 4, "b")
        for i in range(n):
            x = x0 + i * 5
            c.paste([".kk..",
                     "kllkk",
                     "kmmmk",
                     ".kkk."], x, y)
            if (i + n) % 3 == 0:
                c.put(x + 4, y - 1, "Y")
                c.put(x + 4, y, "F")
    c.vline(1, 22, 23, "k")
    c.vline(30, 22, 23, "k")
    return c


def _oil():
    """Oil samples: three transport amphorae standing on the trestle, the
    middle one tallest, a stoppered flask beside them."""
    c = Canvas(32, 32)
    _amphora_shape(c, 1, 5, 19)
    _amphora_shape(c, 10, 1, 23, body="l", lit="h", dark="m")
    _amphora_shape(c, 19, 6, 18, body="d", lit="m", dark="d")
    c.paste([".kk.",
             "kchk",
             ".kk.",
             "kmlk",
             "kmmk",
             "kmmk",
             "kddk",
             ".kk."], 28, 16)
    return c


def _wool():
    """The wool merchant's bolts, piled three high: Tyrian purple, saffron,
    madder and blue, a length of purple hanging over the table's edge."""
    c = Canvas(32, 32)

    def bolt(x, y, w, a, b, d):
        c.box(x, y, x + w, y + 5, a)
        c.hline(x + 1, x + w - 1, y + 1, b)
        c.hline(x + 1, x + w - 1, y + 4, d)
        c.paste(["kk", "kc", "kC", "kc", "kk"], x + w - 1, y)
    bolt(0, 17, 10, "P", "q", "p")
    bolt(10, 17, 10, "y", "c", "o")
    bolt(20, 17, 11, "u", "U", "i")
    bolt(4, 11, 10, "r", "o", "R")
    bolt(14, 11, 11, "P", "q", "p")
    bolt(9, 5, 10, "c", "c", "C")
    # a length of purple let down over the front of the table
    c.rect(3, 22, 9, 23, "P")
    c.vline(3, 22, 23, "k")
    c.vline(9, 22, 23, "k")
    return c


def _helmet():
    """A single bronze helmet on a stand, Corinthian, with a red horsehair
    crest. One helmet, of a kind nobody in Emporion wears."""
    c = Canvas(32, 32)
    # the stand
    c.rect(14, 18, 17, 23, "z")
    c.vline(14, 18, 23, "k")
    c.vline(17, 18, 23, "k")
    c.box(10, 21, 21, 23, "z")
    # the crest, a red brush on a bronze holder
    c.paste(["....kkkkkkkkkk....",
             "..kkrrrrrrrrrrkk..",
             ".krrfrrfrrfrrfrrk.",
             "kkkkkkkkkkkkkkkkkk"], 7, 0)
    c.vline(16, 4, 5, "z")
    # the helmet: dome, the T of the face opening, cheek pieces
    c.paste(["....kkkkkkkkkk....",
             "..kkyYYYyyyybbkk..",
             ".kyYYyyyybbbbbbzk.",
             "kyYyyyybbbbbbbbbzk",
             "kyyyybbkkkkkkbbbzk",
             "kyybbbbkkkkkkbbbzk",
             "kybbbbbbbkkbbbbzzk",
             "kybbbzkk.kk.kkbzzk",
             "kbbbzk..........kk",
             ".kbzk.............",
             "..kk.............."], 7, 6)
    c.put(23, 13, "k")
    return c


def _grain():
    """The grain merchant's samples: two open sacks of barley and wheat with
    their mouths rolled down, a scoop, and a bowl of first fruits."""
    c = Canvas(32, 32)
    for (x, g, G) in ((1, "n", "h"), (13, "b", "n")):
        c.paste(["..kkkkkkkkk..",
                 ".k" + g * 3 + G + g * 5 + "k.",
                 "k" + g * 2 + G + g * 3 + G + g * 3 + "k",
                 "khhhhhhhhhhhk",
                 "kllllllllllllk"[:13],
                 "klhlllllllhlk",
                 "kllllllllllmk",
                 "klllllllllmmk",
                 "kllllllllmmmk",
                 "kmlllllllmmdk",
                 "kmmllllllmmdk",
                 "kmmmmmmmmmddk",
                 ".kmmmmmmmddk.",
                 "..kkkkkkkkk.."], x, 10)
    c.paste(["kkkk.", "kbbkk", "kkkk."], 9, 8)
    c.paste(["..kkkk..",
             ".kfnYfk.",
             "kmmmmmmk",
             ".kddddk.",
             "..kkkk.."], 24, 18)
    return c


def _cups():
    """Euphronios's paint table: a black amphora with a red figure half done,
    two cups, his brushes and a pot of slip."""
    c = Canvas(32, 32)
    c.paste([".k.kkk.k.",
             "kak" + "aaa" + "kak",
             "kakkakkak",
             ".kkaaakk.",
             ".kaaaaak.",
             "kaaaaaaak",
             "kaamlaaak",
             "kaalllaak",
             "kaamlmaak",
             "kaaalaaak",
             ".kaamaak.",
             ".kaaaaak.",
             "..kaaak..",
             "..kaaak..",
             "...kak...",
             "..kkkkk..",
             "..kaaak..",
             "...kkk..."], 2, 6)
    for (x, fig) in ((13, True), (22, False)):
        c.paste(["kkkkkkkkk",
                 "kaaaamaak" if fig else "kmmmmmmmk",
                 "kaamlmaak" if fig else "kllllllmk",
                 ".kaamaak.",
                 "..kkkkk..",
                 "...kak...",
                 "..kkkkk.."], x, 17)
    c.paste(["..kk..", ".kaak.", "kaaaak", "kmmmmk", ".kddk.", "..kk.."], 14, 9)
    c.line(25, 8, 29, 14, "b")
    c.line(27, 8, 30, 13, "b")
    c.put(25, 8, "k")
    c.put(27, 8, "k")
    return c


trestle("trestle_lamps", "clay", _lamps(),
        "Lampis's trestle: a stepped stand of clay oil lamps")
trestle("trestle_oil", "clay", _oil(),
        "a trestle of oil samples: three transport amphorae and a stoppered flask")
trestle("trestle_wool", "cloth", _wool(),
        "the wool merchant's trestle: bolts of Tyrian purple, saffron, madder and blue")
trestle("trestle_helmet", "bronze", _helmet(),
        "a trestle with a single bronze helmet on a stand, a red crest on it")
trestle("trestle_grain", "clay", _grain(),
        "the grain merchant's trestle: open sacks of barley and wheat, a bowl of first fruits")
trestle("trestle_cups", "clay", _cups(),
        "Euphronios's paint table: a black amphora with a red figure half done, cups, brushes")


def _ledger():
    """The crew boss's pay table: the open ledger (two wax tablets), a stylus,
    and a fat purse of silver with coins spilling out."""
    c = Canvas(32, 16)
    c.box(1, 2, 9, 7, "y")
    c.box(9, 2, 17, 7, "y")
    for y in (3, 5):
        c.hline(3, 7, y, "d")
        c.hline(11, 15, y, "d")
    c.hline(3, 6, 4, "d")
    c.hline(11, 14, 6, "d")
    c.line(14, 0, 18, 4, "k")
    c.paste(["...kk....",
             "..kddk...",
             ".kmlmmk..",
             "kmlmmmmk.",
             "kmmmmmdkk",
             ".kddddkcC",
             "..kkkk.kk"], 21, 1)
    for (x, y) in ((29, 6), (30, 7), (27, 7)):
        c.put(x, y, "c")
    return c.text()


two_palettes("trestle_ledger", "wood", _ledger(), "wood", TRESTLE, 2,
             "the crew boss's pay table: an open ledger of wax tablets and a fat purse of silver; "
             "a counter, so he's talked to across it",
             behavior={(0, 0): "MB_COUNTER", (1, 0): "MB_COUNTER"})


# ===========================================================================
# The Deigma
# ===========================================================================

stamp("fish_mounted", "nature", """
................................
................................
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
..kJJJJJJJJJJJJJJJJJJJJJJJJJJk..
..kjj..kkkkkkkkkkkk.......jjk...
..kj.kkSSSSSSSSSSSSkk...kk.jk...
..kjkSSSSSSSSSSSSSSSSk.kSk.jk...
..kkwkSsSsSsSsSsSSSSSSkSSk.jk...
..kkwwkssssssssssssssSSSk..jk...
..kjkwwwssssssssssssssSSSk.jk...
..kj.kkwwwwwwwwwwwwssSk.kSkjk...
..kj...kkkkkkkkkkkkkkk...kkjk...
..kjjjjjjjjjjjjjjjjjjjjjjjjjk...
..kKKKKKKKKKKKKKKKKKKKKKKKKKk...
..kkkkkkkkkkkkkkkkkkkkkkkkkkk...
................................
""", 2, 1, note="a stuffed tunny mounted on a board, glass-eyed, as big as a boy")

stamp("notice_board", "wall", """
................
..kkkkkkkkkkkk..
.k333333333332k.
.k3wwwwwwwwww2k.
.k3wspwwwwwww2k.
.k3wsssssswww2k.
.k3wwwwwwwwww2k.
.k3wssssssww.2k.
.k3wwwwwwwwww2k.
.k3wsssssrRw.2k.
.k3wwwwwwRDRw2k.
.k3wwwwwwwRww2k.
.k3wwwwwwwwww2k.
.k2222222222221.
..kkkkk22kkkkk..
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
......k21k......
.....kk21kk.....
....k332211k....
....k221111k....
....kkkkkkkk....
................
................
""", 1, 2, note="the public notice board by the door: a whitened board, a sheet sealed with the Archon's owl")


# ===========================================================================
# Windows, the Dolphin and the widow's room
# ===========================================================================

def _sea_window():
    """A wide window on the harbor, 2x2 over the wall: open shutters, the sky,
    the sea with a sail on it, a sill. Used by the Dolphin and the widow."""
    c = Canvas(32, 32)
    # the opening, then what's through it: sky above the horizon, the sea
    c.box(3, 7, 28, 28, "a", edge="k")
    c.rect(4, 16, 27, 27, "B")
    c.hline(4, 27, 16, "w")
    for y in range(17, 28):
        for x in range(4, 28):
            if (x * 3 + y * 5) % 13 == 0:
                c.put(x, y, "w")
            elif (x + y * 2) % 5 == 0 or y > 23:
                c.put(x, y, "b")
    # a gull, and a sail on the horizon
    c.put(9, 10, "k")
    c.put(10, 11, "k")
    c.put(11, 10, "k")
    c.paste(["...k.",
             "..kwk",
             ".kwwk",
             "kwwsk",
             "kkkkk",
             ".k11k"], 19, 11)
    # shutters, folded back
    c.box(0, 7, 3, 28, "b")
    c.box(28, 7, 31, 28, "b")
    for y in range(9, 28, 3):
        c.hline(1, 2, y, "B")
        c.hline(29, 30, y, "B")
    # the lintel and the sill
    c.rect(2, 4, 29, 6, "2")
    c.hline(2, 29, 4, "3")
    c.hline(2, 29, 6, "1")
    c.rect(1, 28, 30, 30, "3")
    c.hline(1, 30, 30, "1")
    c.hline(1, 30, 31, "k")
    return c


stamp("sea_window", "wall", _sea_window(), 2, 2,
      note="a wide window on the harbor: the shutters open, the sea under the sill, a sail out on it")


def _amphora_rack():
    """The Dolphin's wine store: a timber rack against the wall, amphorae laid
    in it two high, their mouths toward the room."""
    c = Canvas(32, 32)
    for x in (1, 30):
        c.box(x - 1, 4, x + 1, 31, "a")
        c.vline(x, 5, 30, "s")
    for y in (5, 17, 29):
        c.box(0, y, 31, y + 2, "a")
        c.hline(1, 30, y + 1, "s")
    for row, y in enumerate((8, 20)):
        for i in range(3):
            x = 3 + i * 9 + (row * 2)
            if x + 7 > 29:
                continue
            c.paste([".kkkkk.",
                     "kmlllmk",
                     "kmhkhmk",
                     "kmlkldk",
                     "kmmmmdk",
                     ".kdddk.",
                     "..kkk.."], x, y)
    return c


stamp("amphora_rack", "clay", _amphora_rack(), 2, 2,
      note="a timber rack of wine amphorae laid two high, mouths out")


def _dolphin_mosaic():
    """The Dolphin's floor: a pebble mosaic of a leaping dolphin over waves, in
    a frame of dark and white beads, 4x2 and walkable."""
    W, H = 64, 32
    c = Canvas(W, H)
    for y in range(H):
        for x in range(W):
            d = min(x, y, W - 1 - x, H - 1 - y)
            if d == 0:
                ch = "k"
            elif d == 1:
                ch = "M"
            elif d == 2:
                ch = "u" if (x + y) % 2 else "M"
            elif d == 3:
                ch = "k"
            else:
                h = ((x % 8) * 3 + (y % 8) * 5) % 13
                ch = "m" if h == 0 else "M"
            c.put(x, y, ch)
    # waves along the bottom
    for x in range(4, 60):
        y = 24 + (2 if (x // 4) % 2 else 0)
        c.put(x, y, "u")
        c.put(x, y + 1, "U")
        if (x // 4) % 2 == 0:
            c.put(x, y - 1, "U")
    # the dolphin: an arched body, beak, flippers, a tail fluke
    for x in range(10, 54):
        t = (x - 10) / 44.0
        yc = 17 - 9 * (4 * t * (1 - t))
        th = 3.5 * (1 - abs(t - 0.45) * 1.4)
        for y in range(H):
            if abs(y + 0.5 - yc) <= max(th, 1.0) and 4 <= y <= 27:
                ch = "u" if y + 0.5 < yc - 0.5 else "U"
                if y + 0.5 > yc + th - 1.2:
                    ch = "a"
                c.put(x, y, ch)
    c.outline("k", solid=lambda ch: ch in "uUa")
    # beak and eye, dorsal fin, flippers, tail flukes
    c.paste(["kkkk", "kUUak", ".kkk"], 52, 15)
    c.put(48, 13, "k")
    c.paste(["..k", ".ku", "kuu", "kuk"], 28, 4)
    c.paste(["kUk", ".kUk", "..kk"], 38, 13)
    c.paste(["k...k", "kuk.k", ".kuuk", "..kuk", "...k."], 5, 14)
    return c


stamp("dolphin_mosaic", "bronze", _dolphin_mosaic(), 4, 2,
      walk={(x, y) for x in range(4) for y in range(2)}, flatten=True,
      note="a pebble mosaic of a leaping dolphin over the waves: the tavern's sign, on its floor")

def _bones_table():
    """The knucklebones table in the corner: a heavy square table, its top
    worn pale in a hollow where the bones land, four bones and the cup."""
    c = Canvas(32, 16)
    c.box(1, 2, 30, 10, "h")
    c.hline(2, 29, 3, "h")
    c.rect(2, 4, 29, 8, "l")
    c.ellipse(15.5, 6, 9.5, 2.7, "h")
    c.ellipse(15.5, 6, 6.5, 1.8, "c")
    c.rect(2, 9, 29, 9, "m")
    for (x, y) in ((10, 5), (14, 6), (19, 5), (21, 7)):
        c.paste(["kk", "Ck"], x, y)
    c.paste([".kk.", "kmlk", "kmmk", ".kk."], 25, 2)
    c.paste(["kmdk", "kmdk", "kmdk", "kkkk"], 2, 11)
    c.paste(["kmdk", "kmdk", "kmdk", "kkkk"], 26, 11)
    return c


stamp("bones_table", "wood", _bones_table(), 2, 1,
      note="the knucklebones table: its top worn pale in a hollow where the bones land, four bones in it")


def _sack():
    """A grain sack, tied at the neck."""
    c = Canvas(16, 16)
    c.ellipse(8, 10.5, 6, 5.5, "j")
    c.rect(6, 2, 10, 5, "j")
    c.hline(5, 11, 5, "K")
    c.fill_where(lambda x, y: c.get(x, y) == "j" and (x + y) % 4 == 0 and y > 7, "J")
    c.vline(4, 8, 13, "K")
    c.outline("k", solid=lambda ch: ch in "jJK")
    c.paste(["n.n", ".n."], 7, 0)
    return c


stamp("sack", "nature", _sack(), 1, 1, note="a sack of grain tied at the neck")


def _louterion():
    """A marble washbasin on a pillar by the door: a host's first kindness is
    water for a traveler's feet and hands."""
    c = Canvas(16, 32)
    c.ellipse(8, 15.5, 7.5, 2.5, "M")
    c.ellipse(8, 15.5, 5.5, 1.5, "U")
    c.put(6, 15, "a")
    c.rect(1, 16, 14, 17, "m")
    c.outline("k", solid=lambda ch: ch in "MUam")
    c.rect(6, 19, 9, 28, "m")
    c.vline(6, 19, 28, "M")
    c.vline(9, 19, 28, "n")
    c.vline(5, 19, 28, "k")
    c.vline(10, 19, 28, "k")
    c.box(3, 28, 12, 30, "n")
    c.hline(4, 11, 29, "m")
    c.paste(["..k..", ".kyk.", "kyybk", ".kbk."], 11, 9)
    return c


stamp("louterion", "bronze", _louterion(), 1, 2,
      note="a marble washbasin on its pillar by the door, a bronze jug beside it")


def _krater():
    """A big wine-mixing krater on its stand, a ladle hooked on the rim."""
    c = Canvas(16, 32)
    c.paste(["..kkkkkkkkkkkk..",
             ".kddddddddddddk.",
             "kmlhhhhhhhhhhlmk",
             "kkkkkkkkkkkkkkkk",
             ".kmlllllllllmdk.",
             ".kmkkkmmmkkkmdk.",
             ".kmkmkmmmkmkmdk.",
             ".kmmmmmmmmmmmdk.",
             "..kmmlmmmmmmdk..",
             "...kmmmmmmmdk...",
             "....kkmmmdkk....",
             "......kmdk......",
             "......kmdk......",
             ".....kmmmdk.....",
             "....kkkkkkkk....",
             "...ksSSSSSSsk...",
             "...kssssssssk...",
             "....kkkkkkkk...."], 0, 10)
    c.paste(["kk", ".kb", "..kb"], 12, 8)
    return c


stamp("krater", "clay", _krater(), 1, 2,
      note="a big black-figure krater on a stone stand, for mixing the wine with water")


def _oar_hung():
    """Her husband's oar, hung on two pegs across the plaster under the beam,
    its blade painted blue."""
    c = Canvas(32, 16)
    c.hline(0, 21, 11, "k")
    c.hline(0, 21, 12, "l")
    c.hline(0, 21, 13, "m")
    c.hline(0, 21, 14, "k")
    c.vline(0, 11, 14, "k")
    c.paste(["..kkkkkkkk.",
             ".kUUUUUUUUk",
             "kUuuuuuuuuk",
             "kuuuuuuuuuk",
             "kuuuuuuuuuk",
             ".kuuuuuuuuk",
             "..kkkkkkkk."], 21, 9)
    for x in (5, 15):
        c.paste(["kk", "kd"], x, 14)
    return c


stamp("oar_hung", "wood", _oar_hung(), 2, 1,
      note="a single oar hung on two pegs under the beam, its blade painted blue: her husband's")

stamp("starfish_altar", "bronze", """
................
................
....kk....kk....
...kfFk..kMMk...
.kkfeFfkkmMMnk..
kfFFeFFFkkmnk...
.kkfFfkkk.kk....
...kfk.kfk......
kkkkkkkkkkkkkkkk
kMMMMMMMMMMMMMMk
kmMmmmmmmmmmmMmk
kkkkkkkkkkkkkkkk
.kmmMmmmmmmmMmk.
.knmmmmmmmmmmnk.
.knnnnnnnnnnnnk.
.kkkkkkkkkkkkkk.
""", 1, 1, note="a little marble altar of Poseidon: a dried starfish and a shell on it")


def _loom_shroud():
    """oikia's loom, its half-woven cloth undyed linen: a shroud."""
    rows = as_text(O.STAMPS["loom"]["img"], "wood")
    swap = {"U": "c", "u": "C", "r": "C"}
    return "\n".join("".join(swap.get(ch, ch) for ch in r) for r in rows)


stamp("loom_shroud", "wood", _loom_shroud(), 2, 3,
      note="the upright loom with a half-finished shroud of plain linen on it")


# ===========================================================================
# Philoxenos's andron
# ===========================================================================

def _kline_side():
    """A dining couch along a side wall, its length running into the room:
    the scrolled headrest at the top, a linen bolster, a blue coverlet, the
    frame's near rail and its two front legs at the foot."""
    c = Canvas(16, 32)
    c.box(2, 2, 13, 27, "l")                  # the frame
    c.hline(3, 12, 3, "h")
    c.paste(["..kkkkkkkkkkkk..",
             ".kyhhhhhhhhhhyk.",
             ".kbkkkkkkkkkkbk."], 0, 0)       # the scrolled headrest, a bronze boss each side
    c.rect(4, 4, 11, 7, "c")                  # the bolster
    c.hline(4, 11, 7, "C")
    c.box(3, 8, 12, 25, "U")                  # the coverlet
    for y in range(10, 25, 3):
        c.hline(4, 11, y, "u")
    for y in range(9, 25, 6):
        c.put(6, y, "c")
        c.put(9, y + 3, "c")
    c.hline(3, 12, 25, "r")
    c.hline(2, 13, 27, "k")
    c.rect(2, 28, 13, 29, "m")
    c.hline(2, 13, 29, "d")
    c.hline(2, 13, 30, "k")
    c.paste(["kmk", "kdk", "kkk"], 2, 29)
    c.paste(["kmk", "kdk", "kkk"], 11, 29)
    c.vline(1, 2, 28, "k")
    c.vline(14, 2, 28, "k")
    return c


stamp("kline_side", "wood", _kline_side(), 1, 2,
      note="a dining couch along the side wall: scrolled headrest, linen bolster, blue coverlet")
STAMPS["kline_side_r"] = dict(STAMPS["kline_side"], img=hflip(STAMPS["kline_side"]["img"]),
                              note="the same couch along the other wall")


def _host_mosaic():
    """The andron's floor: a host greeting a traveler at his door, in pebbles.
    The traveler, in a broad hat with a staff, comes from the left; the host
    steps out of his doorway on the right with his hand held out. A border of
    red and dark beads frames it. 4x2, walkable."""
    W, H = 64, 32
    c = Canvas(W, H)
    for y in range(H):
        for x in range(W):
            d = min(x, y, W - 1 - x, H - 1 - y)
            if d == 0:
                ch = "k"
            elif d == 1:
                ch = "r" if (x + y) % 2 else "M"
            elif d == 2:
                ch = "k"
            else:
                h = ((x % 8) * 5 + (y % 8) * 3) % 11
                ch = "m" if h == 0 else "M"
            c.put(x, y, ch)
    # the ground line
    c.hline(4, 59, 27, "n")
    # the doorway on the right: posts, lintel, the dark inside
    c.rect(46, 5, 57, 27, "z")
    c.rect(48, 7, 55, 27, "k")
    c.hline(45, 58, 4, "b")
    c.hline(45, 58, 5, "z")
    # the host, stepping out of it, hand out
    c.paste(["..kk..",
             ".kyyk.",
             ".kyyk.",
             "..kk..",
             ".krrk.",
             "krrrrk",
             "rrrrrr",
             "krrrrk",
             ".rrrr.",
             ".krrk.",
             ".rrrr.",
             ".krrk.",
             ".rkkr.",
             ".rk.r.",
             ".k..k.",
             "kk..kk"], 43, 11)
    c.hline(37, 42, 16, "y")                  # his arm, out to the guest
    c.put(36, 16, "k")
    # the traveler: petasos, cloak, staff
    c.paste(["..kkkkk..",
             ".kzzzzzk.",
             "kzzzzzzzk",
             "...kyyk..",
             "...kyyk..",
             "....kk...",
             "...kbbk..",
             "..kbbbbk.",
             "..bbbbbbk",
             "..kbbbbk.",
             "..kbbbbk.",
             "..kbbbbk.",
             "...bkkb..",
             "...b..b..",
             "...k..k..",
             "..kk..kk."], 21, 11)
    c.hline(30, 35, 16, "y")                  # his hand, taking the host's
    c.vline(19, 9, 27, "z")                   # the staff
    c.put(19, 8, "k")
    # a little bundle on his back, a dog at his heels
    c.paste(["kkk", "kbk", "kkk"], 17, 17)
    c.paste(["k.....", "kk.kk.", "kzzzzk", ".k..k."], 9, 23)
    return c


stamp("host_mosaic", "bronze", _host_mosaic(), 4, 2,
      walk={(x, y) for x in range(4) for y in range(2)}, flatten=True,
      note="a pebble mosaic of a host stepping out of his door to greet a traveler: xenia, in the floor")


def _curtain_bed():
    """The guest bed behind a striped curtain on a rod; the near half drawn
    back so the bed's foot shows."""
    c = Canvas(32, 32)
    # the bed behind, its foot showing on the right
    c.box(15, 12, 30, 27, "c")
    c.rect(16, 18, 29, 26, "u")
    c.hline(16, 29, 18, "U")
    c.hline(16, 29, 22, "i")
    c.rect(15, 27, 30, 28, "n")
    c.hline(15, 30, 29, "k")
    c.paste(["knk", "kkk"], 15, 29)
    c.paste(["knk", "kkk"], 28, 29)
    # the rod
    c.hline(0, 31, 3, "k")
    c.hline(0, 31, 4, "n")
    c.hline(0, 31, 5, "k")
    # the curtain: stripes of madder and wool, hanging in folds; drawn back
    # at the right into a gathered bunch
    for y in range(6, 31):
        for x in range(1, 15):
            stripe = (x // 3) % 2
            ch = ("r" if stripe else "c") if (x % 3) else ("R" if stripe else "C")
            c.put(x, y, ch)
    for y in range(6, 24):
        for x in range(28, 31):
            c.put(x, y, "r" if x == 29 else "R")
    c.vline(0, 5, 31, "k")
    c.vline(15, 5, 31, "k")
    c.hline(0, 15, 31, "k")
    c.paste(["kyk", "kok", ".k."], 27, 17)
    c.vline(27, 5, 23, "k")
    c.vline(31, 5, 23, "k")
    return c


stamp("curtain_bed", "cloth", _curtain_bed(), 2, 2,
      note="the guest bed behind a striped curtain, the near half drawn back")


# ===========================================================================
# The runners' house
# ===========================================================================

def _pallet():
    """A straw pallet on the floor, a gray wool blanket rolled at its head."""
    c = Canvas(16, 32)
    c.box(1, 3, 14, 30, "j")
    for y in range(4, 30):
        for x in range(2, 14):
            if (x * 3 + y) % 7 == 0:
                c.put(x, y, "J")
            elif (x + y * 5) % 11 == 0:
                c.put(x, y, "K")
    c.box(1, 3, 14, 10, "s")
    c.hline(2, 13, 4, "w")
    c.hline(2, 13, 8, "S")
    c.hline(2, 13, 9, "S")
    for x in (4, 8, 12):
        c.vline(x, 5, 8, "S")
    c.hline(1, 14, 31, "k")
    return c


stamp("pallet", "nature", _pallet(), 1, 2,
      note="a runner's straw pallet, a gray blanket rolled at its head")

def _sandals_pegs():
    """Three pairs of sandals hung by their laces from a peg rail."""
    c = Canvas(32, 16)
    c.hline(0, 31, 1, "k")
    c.hline(0, 31, 2, "h")
    c.hline(0, 31, 3, "m")
    c.hline(0, 31, 4, "k")
    sole = [".kkk.",
            "klllk",
            "klhlk",
            "kdlmk",
            "klllk",
            "kllmk",
            "kmlmk",
            ".kmmk",
            "..kk."]
    for px in (5, 16, 27):
        c.paste(["kk", "kd"], px - 1, 4)
        c.line(px, 5, px - 3, 7, "d")
        c.line(px, 5, px + 3, 7, "d")
        c.paste(sole, px - 6, 7)
        c.paste(sole, px + 1, 7)
    return c


stamp("sandals_pegs", "wood", _sandals_pegs(), 2, 1,
      note="sandals hung in pairs by their laces from the pegs, ready for the road")


def _road_map():
    """The barracks wall where the runners scratched every road in Aethos,
    with the distances in stades: a scratched plaster panel, 2x2, the coast
    marked in blue."""
    c = Canvas(32, 32)
    c.box(1, 6, 30, 28, "p", edge="S")
    # the coast, and the sea beyond it to the south-east
    coast = [(22, 27), (23, 24), (26, 22), (27, 18), (29, 15)]
    for a, b in zip(coast, coast[1:]):
        c.line(a[0], a[1], b[0], b[1], "b")
    for y in range(16, 28):
        for x in range(24, 30):
            if (x + y) % 3 == 0 and x > 33 - y // 1.6:
                c.put(x, y, "B")
    roads = [((4, 25), (10, 20)), ((10, 20), (17, 21)), ((17, 21), (23, 13)), ((10, 20), (8, 11)),
             ((8, 11), (15, 9)), ((15, 9), (23, 13)), ((23, 13), (26, 20)), ((17, 21), (20, 26)),
             ((4, 25), (3, 15)), ((3, 15), (8, 11))]
    for (a, b) in roads:
        c.line(a[0], a[1], b[0], b[1], "1")
    for (x, y) in ((4, 25), (10, 20), (17, 21), (23, 13), (8, 11), (15, 9), (26, 20), (20, 26), (3, 15)):
        c.rect(x, y, x + 1, y + 1, "k")
    # tally marks for stades along the roads
    for (x, y) in ((13, 22), (20, 15), (11, 8), (25, 16), (6, 16), (18, 24), (4, 19)):
        for i in range(3):
            c.vline(x + i * 2, y, y + 1, "R")
    # Kalliste, the island, a scratched loop out in the sea
    c.paste([".bb.", "b..b", ".bb."], 26, 24)
    c.put(27, 25, "k")
    return c


stamp("road_map", "wall", _road_map(), 2, 2,
      note="every road in Aethos scratched into the plaster, the distances in stades tallied beside them")


def _water_jar():
    """The barracks' big water jar, a bronze ladle hooked on its rim."""
    c = Canvas(16, 32)
    c.paste(["....kkkkkkkk....",
             "...kddddddddk...",
             "...kllhhhhllk...",
             "....kkmmmmkk....",
             "...kkmmmmmmkk...",
             "..kmllllllllmk..",
             ".kmlhhllllllmdk.",
             "kmlhhlllllllmmdk",
             "kmllllllllllmmdk",
             "kmllkkkkkkllmmdk",
             "kmlkcckcckklmmdk",
             "kmlkkkkkkkklmmdk",
             "kmmllllllllmmmdk",
             "kmmmlllllllmmmdk",
             ".kmmmmmmmmmmmdk.",
             ".kmmmmmmmmmmmdk.",
             "..kmmmmmmmmmdk..",
             "...kdmmmmmmdk...",
             "....kkddddkk....",
             ".....kkkkkk....."], 0, 12)
    c.paste(["k......", "kbk....", ".kbk...", "..kbkk.", "...kbbk", "...kbbk", "....kk."], 9, 6)
    return c


stamp("water_jar", "clay", _water_jar(), 1, 2,
      note="a big water jar, a bronze ladle hooked over its rim")


def _ribbon_door():
    """The back door to the yard, with the finishing ribbon nailed over it."""
    c = Canvas(16, 32)
    c.rect(2, 7, 13, 31, "3")
    c.rect(4, 9, 11, 31, "k")
    c.rect(5, 10, 10, 31, "1")
    c.vline(2, 7, 31, "k")
    c.vline(13, 7, 31, "k")
    c.hline(2, 13, 7, "k")
    # the ribbon: red wool, tied across the lintel, its tails hanging
    c.hline(0, 15, 9, "r")
    c.hline(0, 15, 10, "R")
    c.put(0, 9, "k")
    c.put(15, 9, "k")
    c.paste(["kk", "rk", "Rr", ".R", ".r", ".R"], 1, 10)
    c.paste(["kk", "kr", "rR", "R.", "r.", "R."], 13, 10)
    return c


stamp("ribbon_door", "wall", _ribbon_door(), 1, 2,
      note="the back door to the yard, the red finishing ribbon nailed across its lintel")


# ===========================================================================
# Euphronios's workshop
# ===========================================================================

def _kiln():
    """The domed kiln at the back, 2x3: its chimney up through the roof (over
    the wall), the brick dome, and the stoking mouth at its foot, glowing."""
    c = Canvas(32, 48)
    # chimney
    c.box(10, 0, 21, 18, "S")
    c.vline(11, 0, 17, "t")
    c.vline(20, 0, 17, "s")
    for y in (4, 9, 14):
        c.hline(11, 20, y, "s")
    for (x, y) in ((14, 2), (16, 7), (13, 12), (17, 16)):
        c.put(x, y, "a")
    # the dome
    c.ellipse(16, 30, 15.5, 15, "m")
    for y in range(15, 46):
        for x in range(32):
            if c.get(x, y) == "m":
                if (x + (y // 4) * 3) % 6 == 0 or y % 4 == 0:
                    c.put(x, y, "d")
                elif x < 12 and y < 32:
                    c.put(x, y, "l")
    c.outline("k", solid=lambda ch: ch in "mdl")
    c.box(10, 0, 21, 15, "S")
    c.vline(11, 0, 14, "t")
    c.vline(20, 0, 14, "s")
    for y in (4, 9, 14):
        c.hline(11, 20, y, "s")
    # the spyhole and the stoking mouth
    c.box(14, 24, 18, 27, "a")
    c.put(16, 25, "F")
    c.box(9, 37, 22, 46, "k")
    c.rect(10, 39, 21, 46, "f")
    c.rect(12, 41, 19, 46, "F")
    c.rect(14, 43, 17, 46, "Y")
    c.hline(9, 22, 37, "s")
    c.hline(8, 23, 36, "k")
    c.rect(0, 46, 31, 47, "k")
    return c


stamp("kiln", "clay", _kiln(), 2, 3,
      note="the domed kiln, its chimney up through the roof and a fire in its mouth")

def _wheel():
    """The potter's wheel by the door, caked in clay: a broad disc on its
    stem over the kick-wheel, a half-painted cup turning on it."""
    c = Canvas(16, 16)
    c.ellipse(8, 13.5, 6.5, 2.2, "d")
    c.rect(7, 8, 8, 12, "d")
    c.ellipse(8, 8, 7.5, 2.6, "m")
    c.hline(2, 13, 7, "l")
    c.outline("k", solid=lambda ch: ch in "dml")
    # the cup: black glaze, the start of a red figure on it
    c.paste(["kkkkkkk",
             "kaamlak",
             "kaalmak",
             ".kaaak.",
             "..kkk.."], 5, 1)
    return c


stamp("wheel", "clay", _wheel(), 1, 1,
      note="the potter's wheel, caked in clay, a half-painted cup turning on it")

stamp("slip_pots", "clay", """
................
................
................
.......b........
.......b.....b..
..kkk..b..kk.b..
.kaaak.b.kaakb..
kakkkakbkakkakb.
kmaaamk.kmaamk..
kmmmmmk.kmmmmk..
.kdddk...kddk...
..kkk.kkk.kk....
.....kaaak......
....kmmmmmk.....
....kdddddk.....
.....kkkkk......
""", 1, 1, note="pots of black slip, the brushes left standing in them")


def _drying_shelf():
    """Two long shelves of new cups and jars drying, unpainted, on the wall."""
    c = Canvas(32, 32)
    for y in (13, 27):
        c.box(0, y, 31, y + 2, "b")
        c.hline(1, 30, y + 1, "d")
        c.paste(["kbk", ".kk"], 2, y + 3)
        c.paste(["kbk", "kk."], 27, y + 3)
    cups = [".kkkk.", "khhhhk", "kllllk", ".kmmk.", "..kk.."]
    jar = ["..kk..", ".kllk.", "klhhlk", "kllllk", "kmllmk", ".kmmk.", "..kk.."]
    x = 1
    for i in range(5):
        piece = jar if i % 2 else cups
        c.paste(piece, x, 13 - len(piece))
        x += 6
    x = 2
    for i in range(5):
        piece = cups if i % 2 else jar
        c.paste(piece, x, 27 - len(piece))
        x += 6
    return c


stamp("drying_shelf", "clay", _drying_shelf(), 2, 2,
      note="long shelves of new cups and jars drying, not yet painted")


def _scrawl():
    """EUPHRONIOS PAINTED ME, scrawled in black slip on the whitewash. The
    letters sit in the band of plaster under the beam (rows 9-15)."""
    c = Canvas(32, 16)
    letters = {
        "E": ["kkk", "k..", "kk.", "k..", "kkk"],
        "Y": ["k.k", "k.k", ".k.", ".k.", ".k."],
        "F": [".k.", "kkk", "k.k", "kkk", ".k."],   # phi
        "P": ["kk.", "k.k", "kk.", "k..", "k.."],
        "O": [".k.", "k.k", "k.k", "k.k", ".k."],
        "N": ["k.k", "kkk", "kkk", "k.k", "k.k"],
        "I": ["k", "k", "k", "k", "k"],
        "S": ["kkk", ".k.", "..k", ".k.", "kkk"],   # sigma
    }
    x = 1
    for ch in "EYFPONIOS":
        g = letters[ch]
        c.paste(g, x, 10)
        x += len(g[0]) + 1
    return c


stamp("scrawl", "wall", _scrawl(), 2, 1,
      note="EUPHRONIOS PAINTED ME, scrawled in black slip on the plaster (here, the first word)")

stamp("clay_bin", "clay", """
................
................
................
................
................
....kkkkkkk.....
..kkdmmlmmdkk...
.kmdmmllmmmdmk..
.kSkkkkkkkkkSk..
.kSddmmmmmddSk..
.ksSmmlmmmmSsk..
.kssSSSSSSSssk..
..kssssssssssk..
...kkkkkkkkkk...
................
................
""", 1, 1, note="a stone basin of wet clay, kneaded and waiting")


# ===========================================================================
# The hiring hall
# ===========================================================================

CRATE = [
    "..kkkkkkkkkkkk..",
    ".khhhhhhhhhhhhk.",
    ".klllllllllllhk.",
    "kkkkkkkkkkkkkkkk",
    "kmmlmmmmmmmlmmdk",
    "kmklkmmmmmklkmdk",
    "kmmlmmmmmmmlmmdk",
    "kdddddddddddddkk",
    "kmmlmmmmmmmlmmdk",
    "kmklkmmmmmklkmdk",
    "kmmlmmmmmmmlmmdk",
    "kkkkkkkkkkkkkkkk",
]


def _crate(top=None, mark=None):
    c = Canvas(16, 16)
    c.paste(CRATE, 0, 4)
    if top:
        c.paste(top, 0, 0)
    if mark:
        c.paste(mark, 5, 9)
    return c


stamp("crate", "wood", _crate(), 1, 1, note="a plank crate, nailed shut")
stamp("crate_shovels", "wood", _crate(top=[
    "..k....k....k...",
    ".kbk..kbk..kzk..",
    ".kbk..kyk..kbk..",
    "..k....k....k...",
    "..kl...kl...kl..",
    "..kl...kl...kl..",
]), 1, 1, note="a crate of new shovels, their bronze blades up")
stamp("crate_helmets", "wood", _crate(top=[
    "....kkk..kkk....",
    "...kybbkkybbk...",
    "..kyyzbbkyzbbk..",
    "..kbzkbbkbkzbk..",
    "...kk.kk.kk.kk..",
]), 1, 1, note="a crate heaped with bronze helmets")
stamp("crate_sickle", "wood", _crate(mark=[
    "..cc.",
    ".c..c",
    ".c...",
    "..c..",
]), 1, 1, note="a crate with a sickle chalked small on it, almost hidden")


def _crate_stack():
    c = Canvas(16, 32)
    c.paste(CRATE, 0, 20)
    c.paste(CRATE, 0, 8)
    c.paste(["kkkkkkkkkkkkkkkk"], 0, 19)
    return c


stamp("crate_stack", "wood", _crate_stack(), 1, 2, note="two crates stacked")


def _hoist():
    """The rope-and-pulley hoist: a bracket and sheave at the roof beam, the
    rope down the wall, and its hook over a coil of rope on the floor."""
    c = Canvas(16, 48)
    c.box(2, 2, 13, 5, "K")
    c.hline(3, 12, 3, "J")
    c.ellipse(8, 9.5, 4.5, 4.5, "j")
    c.ellipse(8, 9.5, 2, 2, "K")
    c.outline("k", solid=lambda ch: ch in "jK")
    c.put(8, 9, "k")
    for y in range(10, 40):
        c.put(4, y, "n" if y % 2 else "K")
        c.put(12, y, "n" if y % 2 else "K")
    c.paste(["..kk..", ".k..k.", ".k....", "..k...", "...kk."], 9, 38)
    c.ellipse(7, 44, 6.5, 3, "n")
    c.ellipse(7, 44, 3, 1.4, "K")
    c.outline("k", solid=lambda ch: ch in "nK")
    return c


stamp("hoist", "nature", _hoist(), 1, 3,
      note="a rope-and-pulley hoist: the sheave at the beam, the rope, a hook over a coil on the floor")


def _shed_doors():
    """The great double doors out to the shipsheds, barred."""
    c = Canvas(32, 32)
    c.box(0, 4, 31, 31, "m")
    c.vline(15, 5, 31, "k")
    c.vline(16, 5, 31, "k")
    for x in (4, 8, 12, 20, 24, 28):
        c.vline(x, 5, 31, "d")
    for y in (10, 24):
        c.hline(1, 30, y, "l")
        c.hline(1, 30, y + 1, "d")
    c.box(2, 16, 29, 18, "z")
    c.hline(3, 28, 17, "b")
    c.hline(0, 31, 4, "k")
    c.hline(1, 30, 5, "h")
    return c


stamp("shed_doors", "wood", _shed_doors(), 2, 2,
      note="the great double doors out to the shipsheds, barred from inside")


# ===========================================================================
# Eleusa's rooms (tools/ichor/maps/eleusa_rooms.py, batch 4). No new art: each
# is an existing piece with a different behavior, so it costs metatiles, never
# tiles.
# ===========================================================================

# The Agora stall's counter: "a door laid across two barrels". oikia's long
# table, with its bread, jug and olives for sale, is the nearest board on
# legs; as a counter, the stallkeeper is talked to across it.
STAMPS["counter_plank"] = dict(STAMPS["table"], behavior={(0, 0): "MB_COUNTER", (1, 0): "MB_COUNTER"},
                               note="the stall's counter, a board on legs with bread, a jug and olives on it; "
                                    "talked across (oikia's table, as MB_COUNTER)",
                               source="limen")

# The granary's way down to Sitokles's grain pit: oikia's timber stairwell
# without its warp, since the pit isn't a map.
STAMPS["pit_stairs"] = dict(STAMPS["stairs_down_wood"], walk=set(), behavior={},
                            note="the timber steps down to the grain pit (oikia's stairwell, no warp)",
                            source="limen")

