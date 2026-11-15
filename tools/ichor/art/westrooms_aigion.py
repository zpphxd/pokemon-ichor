#!/usr/bin/env python3
"""Aigion's pieces: old Tisamenos's house, painted wall to wall with the
Catalogue of Ships, and Helike the goatherd's house built into the hill.
Registered into westrooms_art.STAMPS on import; the ship frieze is a wall
style (westrooms_art.WALLS["ships"])."""
import math

import westrooms_art as WA
from westrooms_art import stamp, grid, blank, over, hflip, STAMPS, recolor, noise, Canvas, OA  # noqa: F401

# ---- Tisamenos's house: the Catalogue of Ships ------------------------------------

DIGITS = {
    "0": ["kkk", "k.k", "k.k", "k.k", "kkk"],
    "1": [".k.", "kk.", ".k.", ".k.", "kkk"],
    "2": ["kkk", "..k", "kkk", "k..", "kkk"],
    "3": ["kkk", "..k", ".kk", "..k", "kkk"],
    "4": ["k.k", "k.k", "kkk", "..k", "..k"],
    "5": ["kkk", "k..", "kkk", "..k", "kkk"],
    "6": ["kkk", "k..", "kkk", "k.k", "kkk"],
    "7": ["kkk", "..k", ".k.", ".k.", ".k."],
    "8": ["kkk", "k.k", "kkk", "k.k", "kkk"],
    "9": ["kkk", "k.k", "kkk", "..k", "kkk"],
}


def _number(c, x, y, n, ink="d"):
    for i, ch in enumerate(str(n)):
        for dy, row in enumerate(DIGITS[ch]):
            for dx, p in enumerate(row):
                if p == "k":
                    c.px(x + i * 4 + dx, y + dy, ink)


def _ship(c, x0, n, sail_stripe):
    """One black ship of the Catalogue, bow to the right, riding the sea:
    a bold black hull with its eye and a red stripe, oars down in the water,
    a dark sail on its yard, and its number painted over the prow."""
    # the hull: long, low and black, stern curling up, the ram forward
    for x in range(x0 + 2, x0 + 26):
        c.vl(x, 17, 23, "k")
    for (dx, y0) in [(0, 11), (1, 13), (2, 15), (3, 16)]:   # the stern post, curling
        c.vl(x0 + dx, y0, 21, "k")
    c.px(x0 + 1, 10, "k")
    c.px(x0 + 2, 10, "k")
    c.hl(x0 + 26, x0 + 29, 22, "k")             # the ram
    c.hl(x0 + 26, x0 + 28, 23, "k")
    c.vl(x0 + 25, 14, 22, "k")                  # the prow
    c.px(x0 + 26, 14, "k")
    c.hl(x0 + 4, x0 + 24, 19, "m")               # a red stripe along the strakes
    c.px(x0 + 23, 18, "c")                       # the eye on the bow
    c.px(x0 + 22, 18, "c")
    for i in range(7):                           # the oar ports
        c.px(x0 + 6 + i * 3, 21, "s")
    # mast, yard and a dark sail
    c.vl(x0 + 13, 4, 16, "k")
    c.hl(x0 + 7, x0 + 19, 5, "k")
    c.rect(x0 + 8, 6, x0 + 18, 13, "d")
    for y in range(7, 14, 2):
        c.hl(x0 + 8, x0 + 18, y, sail_stripe)
    c.hl(x0 + 8, x0 + 18, 14, "k")
    _number(c, x0 + 20, 6, n, ink="k")           # its number over the prow


def _ships_wall(first=401, count=7):
    """Tisamenos's walls: one long black-figure frieze of the ships that
    sailed for Troy, each numbered over its prow, on a cream ground between a
    red key band and a black sea. 2 courses, `count` ships two cells each, so
    no ship repeats across the room."""
    W = 32 * count
    c = Canvas(W, 32)
    c.rect(0, 0, W - 1, 31, "c")
    c.hl(0, W - 1, 0, "k")
    c.hl(0, W - 1, 1, "d")
    for x in range(W):                           # the key band under the ceiling
        c.px(x, 2, "m" if (x // 2) % 3 else "d")
    c.hl(0, W - 1, 3, "d")
    for i in range(count):
        _ship(c, i * 32 + 2, first + i, "m" if i % 2 else "d")
    for y in range(24, 30):                      # the sea: black, with red wave lines, like a pot's
        for x in range(W):
            if c.get(x, y) == "c":
                c.px(x, y, "k")
    for x in range(W):
        for base in (25, 28):
            wy = base + int(round(0.8 * math.sin(x / 2.0 + base)))
            if c.get(x, wy) == "k" and (x + base) % 9 not in (0, 1):
                c.px(x, wy, "m")
    for i in range(count):                       # oars down into the sea
        for j in range(7):
            ox = i * 32 + 2 + 6 + j * 3
            c.line(ox, 23, ox - 2, 27, "k")
    c.hl(0, W - 1, 30, "d")
    c.hl(0, W - 1, 31, "k")
    img = c.img("clay")
    upper = [img[0:16, i * 16:(i + 1) * 16] for i in range(2 * count)]
    lower = [img[16:32, i * 16:(i + 1) * 16] for i in range(2 * count)]
    return [upper, lower]


WA.WALLS["ships"] = _ships_wall()


def _model_ship():
    """The model ship on its stand in the middle of the floor: a trireme a
    forearm long, black and red, oars shipped, eyes on her bow. 2x2, clay."""
    c = Canvas(32, 32)
    # the stand: two trestles and a cradle
    for x in (8, 22):
        c.line(x - 3, 30, x, 19, "d")
        c.line(x + 3, 30, x, 19, "d")
        c.hl(x - 4, x + 4, 30, "d")
    c.hl(5, 26, 19, "m")
    # the hull
    for x in range(3, 28):
        top = 13 if 5 < x < 26 else 14
        c.vl(x, top, 18, "k")
    c.vl(2, 9, 16, "k")                          # the stern curling up
    c.px(3, 8, "k")
    c.hl(27, 30, 18, "k")                        # the ram
    c.hl(4, 26, 16, "m")
    c.hl(4, 26, 14, "d")
    c.px(25, 15, "c")                            # her eye
    for x in range(6, 25, 3):                    # oars shipped, sticking out a little
        c.px(x, 19, "k")
    c.vl(15, 3, 12, "d")                         # the mast, the yard, a furled sail
    c.hl(9, 21, 4, "d")
    c.hl(10, 20, 5, "h")
    c.outline("k")
    return c


stamp("model_ship", 2, 2, art=[("clay", _model_ship())],
      note="a model trireme on its stand: black and red, oars shipped, eyes on the bow")


def _tablet_chest():
    """A chest standing open under the window, full of wax tablets: the
    Catalogue, written out, ship by ship. 2x1, wood."""
    c = Canvas(32, 16)
    c.rect(1, 3, 30, 14, "d")                    # the box
    c.rect(2, 4, 29, 13, "m")
    c.hl(2, 29, 4, "l")
    c.rect(3, 5, 28, 9, "k")                     # the open well of it
    for i, x in enumerate(range(4, 28, 4)):      # tablets standing in rows, wax dark, frames pale
        c.rect(x, 5, x + 2, 9, "l")
        c.rect(x + 1, 6, x + 1, 8, "d")
        if i % 2:
            c.px(x + 1, 6, "C")
    c.rect(5, 0, 26, 2, "m")                     # the lid, propped back against the wall
    c.hl(5, 26, 0, "l")
    for x in (6, 25):
        c.vl(x, 10, 13, "b")                     # bronze corners
    c.outline("k")
    return c


stamp("tablet_chest", 2, 1, art=[("wood", _tablet_chest())],
      note="a chest standing open, full of wax tablets: the Catalogue, ship by ship")


def _chair_back():
    """His chair, turned to face the frieze: a klismos seen from behind,
    its curved back rail, a cushion, its legs splayed."""
    return """
................
................
...kkkkkkkkkk...
..khhhhhhhhhhk..
..klllllllllmk..
...kkkkkkkkkk...
....kmk..kmk....
...kuuuuuuuuk...
...kuUUUUUUuk...
...kuuuuuuuuk...
...kkkkkkkkkk...
...kmk....kmk...
..kmk......kmk..
..kdk......kdk..
.kdk........kdk.
.kkk........kkk.
"""


stamp("chair_back", 1, 1, art=[("wood", _chair_back())], note="his chair, turned to face the frieze")

# ---- Helike's house: the goatherd's, half cave --------------------------------------


def _goat_pen():
    """The goat pen in the cave half: a low ring of dry stones round clean
    straw, a hay rack against the rock. 3x2, stone (its lamp-glow golds are
    the straw)."""
    c = Canvas(48, 32)
    c.rect(1, 3, 46, 30, "k")
    c.rect(2, 4, 45, 29, "3")
    c.rect(6, 8, 41, 25, "E")                    # straw inside, trodden
    for y in range(8, 26):
        for x in range(6, 42):
            n = noise(x, y, 14)
            c.px(x, y, "L" if n < 0.08 else ("h" if n < 0.6 else "E"))
    # the dry-stone ring: rounded stones along the four sides
    for x in range(2, 46, 5):
        for y0 in (3, 25):
            c.ell(x + 2, y0 + 2.5, 2.6, 2.2, "4")
            c.px(x + 1, y0 + 1, "5")
            c.px(x + 3, y0 + 4, "2")
    for y in range(7, 25, 5):
        for x0 in (1, 41):
            c.ell(x0 + 2.5, y + 2, 2.2, 2.6, "4")
            c.px(x0 + 1, y + 1, "5")
            c.px(x0 + 4, y + 3, "2")
    c.rect(5, 25, 12, 30, "E")                   # the gap for the gate, a hurdle across it
    for x in range(5, 13):
        c.px(x, 26 + (x % 2), "E")
        c.px(x, 29, "e")
    c.vl(5, 24, 30, "e")
    c.vl(12, 24, 30, "e")
    # the baby's cradle in the straw, on its rockers, a fleece in it: drawn
    # here in the stone palette's timbers so it shares the pen's tiles
    c.paste(["..kkkkkkkkkkk..",
             ".khhhhhhhhhhhek",
             ".kh.........Eek",
             ".kh.........Eek",
             ".kh.........Eek",
             ".khhhhhhhhhhEek",
             "..kEEEEEEEEEek.",
             "...kkkkkkkkkk..",
             "..kek.....kek..",
             ".keeeeeeeeeeeek",
             "..kkkkkkkkkkkk."], 17, 13)
    c.rect(20, 15, 28, 18, "6")                  # the fleece
    c.hl(20, 28, 18, "5")
    c.px(22, 16, "5")
    c.px(26, 17, "5")
    return c


stamp("goat_pen", 3, 2, art=[("stone", _goat_pen())],
      note="the goat pen: a low ring of dry stones round clean straw")


def _cradle():
    """A baby's cradle on rockers, a fleece in it: meant for a baby, used
    for whatever cries. Wood."""
    c = Canvas(16, 16)
    c.paste(["..kkkkkkkkkkk..",
             ".kllllllllllldk",
             ".kl.........mdk",
             ".kl.........mdk",
             ".kl.........mdk",
             ".kllllllllllmdk",
             "..kmmmmmmmmmdk.",
             "...kkkkkkkkkk..",
             "..kdk.....kdk..",
             ".kddddddddddddk",
             "..kkkkkkkkkkkk."], 0, 3)
    c.rect(3, 5, 12, 8, "c")                     # the fleece
    c.hl(3, 12, 8, "C")
    c.px(5, 6, "C")
    c.px(9, 7, "C")
    return c


stamp("cradle", 1, 1, art=[("wood", _cradle())], note="a baby's cradle on rockers, a fleece in it")


def _cheese_rack():
    """Racks of round cheeses ripening in the cool of the cave: three
    shelves of wheels, young and pale at the top, old and golden below.
    2x2, wood."""
    c = Canvas(32, 32)
    c.rect(1, 1, 2, 31, "d")
    c.rect(29, 1, 30, 31, "d")
    for i, y0 in enumerate((9, 19, 29)):
        c.rect(1, y0, 30, y0 + 1, "m")
        c.hl(1, 30, y0, "l")
        for x in range(4, 28, 6):
            col, rim = (("c", "C") if i == 0 else (("C", "l") if i == 1 else ("h", "l")))
            c.ell(x + 1.5, y0 - 3, 2.8, 2.6, rim)
            c.ell(x + 1, y0 - 3.5, 2, 1.8, col)
    c.outline("k")
    return c


stamp("cheese_rack", 2, 2, art=[("wood", _cheese_rack())],
      note="racks of round cheeses ripening in the cool of the cave, pale at the top, golden below")


def _goat_bells():
    """A row of bronze goat bells on a peg rail, from big to tiny, for the
    kids till they stop wandering off. 3x1 on the wall, bronze."""
    c = Canvas(48, 16)
    c.hl(0, 47, 2, "z")
    c.hl(0, 47, 1, "b")
    x = 3
    for size in (7, 6, 5, 4, 3, 3, 2):
        h = size + 2
        c.vl(x + size // 2, 3, 4, "k")          # the thong
        for dy in range(h):
            half = 1 + dy * size // (2 * h)
            c.hl(x + size // 2 - half, x + size // 2 + half, 5 + dy, "y" if dy < 2 else "b")
        c.hl(x, x + size, 5 + h, "z")
        c.px(x + size // 2, 6 + h, "z")          # the clapper
        x += size + 3
    c.outline("k")
    return c


stamp("goat_bells", 3, 1, art=[("bronze", _goat_bells())],
      note="a row of bronze goat bells on a peg rail, from big to tiny")


def _milk_pails():
    c = Canvas(16, 16)
    for (x, y) in [(1, 6), (8, 7)]:
        c.rect(x, y, x + 6, y + 7, "m")
        c.vl(x, y, y + 7, "l")
        c.vl(x + 6, y, y + 7, "d")
        c.hl(x, x + 6, y + 2, "d")
        c.ell(x + 3, y, 3, 1.2, "c")
        c.line(x, y, x + 3, y - 3, "d")
        c.line(x + 3, y - 3, x + 6, y, "d")
    c.outline("k")
    return c


stamp("milk_pails", 1, 1, art=[("wood", _milk_pails())], note="two wooden pails, this morning's milk")


def _goatskins():
    """Goatskins hung on a peg on the plaster, a crook leaning under them.
    1x2 on the wall, nature (the mule's greys for the hides)."""
    c = Canvas(16, 32)
    c.px(7, 4, "k")
    c.paste(["..kk..kk..",
             ".kuukkuuk.",
             "kuUuuuuUuk",
             "kuUUuuUUuk",
             ".kuUUUUuk.",
             ".kuUUwUuk.",
             ".kuuUUuuk.",
             "kuuuuuuuuk",
             "kMuuuuuuMk",
             ".kMk..kMk."], 2, 5)
    c.vl(13, 6, 30, "K")                         # the crook
    c.paste(["kKK.", "K..K", "...K"], 12, 3)
    c.outline("k")
    return c


stamp("goatskins", 1, 2, art=[("nature", _goatskins())], note="goatskins on a peg, a crook leaning under them")
