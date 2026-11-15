#!/usr/bin/env python3
"""chalkeon's own furniture: the pieces no Greek house has.

Imported by chalkeon_art.py, which owns the palettes and the stamp() contract
(w, h in metatiles; walk; behavior; top; flatten). Each piece is drawn on a
Canvas of character pixels, lit from the top left, with a one-pixel ink
outline as in oikia. Grouped by the room that first needs them; every room's
layout is in tools/ichor/maps/pontos_rooms.py.
"""
import math

import chalkeon_art as C

Canvas, stamp, lathe = C.Canvas, C.stamp, C.lathe


# ==========================================================================
# Shared: the Colchian window
# ==========================================================================

def _window_lattice():
    """A small square window cut through the logs, its frame pegged, a
    diamond lattice of split wood over the sky."""
    c = Canvas(16, 32)
    c.rect(2, 8, 13, 27, "k")
    c.rect(3, 9, 12, 26, "E")
    for y in range(9, 27):
        for x in range(3, 13):
            if (x + y) % 5 == 0 or (x - y) % 5 == 0:
                c.put(x, y, "L")
            elif y < 13 and (x + y) % 3 == 0:
                c.put(x, y, "e")
    c.hline(2, 13, 8, "l")
    c.vline(2, 8, 27, "l")
    c.vline(13, 9, 27, "1")
    c.hline(1, 14, 28, "l")
    c.hline(1, 14, 29, "L")
    c.hline(1, 14, 30, "k")
    c.put(1, 28, "k")
    c.put(14, 28, "k")
    return c.text()


stamp("window_lattice", "wall", _window_lattice(), 1, 2,
      note="a window cut through the logs: a pegged frame, a diamond lattice of split wood, sky")


# ==========================================================================
# Phineus's house, Salmydessos
# ==========================================================================

def _shutters_shut():
    """Phineus keeps his shutters closed: he has no use for the light."""
    c = Canvas(16, 32)
    c.rect(1, 7, 14, 29, "k")
    c.rect(2, 8, 7, 28, "l")
    c.rect(8, 8, 13, 28, "l")
    for x in (2, 8):
        c.vline(x, 8, 28, "h")
    for x in (7, 13):
        c.vline(x, 8, 28, "m")
    for x in (4, 10):
        c.vline(x, 9, 27, "m")
    for y in (11, 24):
        c.hline(2, 13, y, "m")
        c.hline(2, 13, y + 1, "d")
    c.hline(4, 11, 17, "y")
    c.hline(4, 11, 18, "b")
    c.hline(4, 11, 19, "z")
    c.put(3, 18, "k")
    c.put(12, 18, "k")
    c.hline(0, 15, 29, "h")
    c.hline(0, 15, 30, "m")
    c.hline(0, 15, 31, "k")
    return c.text()


stamp("shutters_shut", "wood", _shutters_shut(), 1, 2,
      note="shutters closed and barred with bronze: the blind seer has no use for the light")


def _claw_marks():
    """Harpies' talon gouges raked down the plaster, and one of their dark
    feathers caught in a crack in the beam."""
    c = Canvas(16, 32)
    # four talons' gouges, raked down and to the right, deepest in the middle
    for i, x0 in enumerate((2, 5, 8, 11)):
        n = 16 if i in (1, 2) else 12
        y0 = 9 + (2 if i in (0, 3) else 0)
        for j in range(n):
            y = y0 + j
            x = x0 + j // 4
            c.put(x, y, "Q")
            c.put(x + 1, y, "t")
            if 2 < j < n - 2:
                c.put(x - 1, y, "w")       # the plaster's torn lip, catching the light
    # a dark feather caught in the beam: quill, then a ragged vane
    c.paste(6, 1, """
.....S..
....Qt..
...QtQ..
..QtQQ..
.QtQQ...
.tQQ....
QQ......
Q.......
""")
    return c.text()


stamp("claw_marks", "floor", _claw_marks(), 1, 2,
      note="the Harpies' talons raked down the plaster; a dark feather caught in the beam")


def _dove_cage(dove=True):
    """A wicker cage hung from a peg in the beam. With the dove: white, grey
    in the wing, a dark eye. Without: its door open, a feather on the floor."""
    c = Canvas(16, 32)
    c.put(7, 2, "k")
    c.put(8, 2, "k")
    c.vline(8, 3, 8, "n")
    # the dome and the bars
    c.ellipse(8, 14, 6.5, 6, "j")
    c.rect(2, 14, 13, 26, "j")
    for y in range(9, 27):
        for x in range(2, 14):
            if c.get(x, y) == "j" and not (x % 3 == 2 or y in (14, 26) or y < 11):
                c.put(x, y, ".")
    c.hline(2, 13, 26, "K")
    c.hline(2, 13, 27, "K")
    c.hline(3, 12, 28, "k")
    c.put(8, 8, "J")
    if dove:
        body = """
....kkk..
...kwwwk.
..kwkwwmk
..kwwwwk.
.kwwwssk.
kwwwssSSk
kwwwwssk.
.kkwwwkk.
...kmmk..
"""
        c.paste(4, 16, body)
    else:
        # the door hangs open on the right, a feather on the floor of the cage
        for y in range(17, 25):
            c.put(13, y, ".")
            c.put(14, y, "j")
        c.put(15, 17, "K")
        c.hline(5, 9, 25, "w")
        c.put(10, 24, "s")
        c.put(4, 25, "s")
    c.outline()
    return c.text()


stamp("dove_cage", "nature", _dove_cage(True), 1, 2,
      note="a wicker cage hung from the beam, a white dove in it: Phineus's gift")
stamp("dove_cage_empty", "nature", _dove_cage(False), 1, 2,
      note="the same cage, its door open, one white feather left")


def _table_bare():
    """Phineus's long table, bare: forty years of Harpies left nothing on it
    but their claw marks."""
    # Drawn as a left end, a middle that repeats every 8 px, and a right end
    # mirroring the left, so the three blocks cost about six tiles.
    c = Canvas(48, 16)
    c.rect(1, 4, 46, 10, "k")
    c.hline(2, 45, 5, "h")
    c.rect(2, 6, 45, 8, "l")
    c.hline(2, 45, 9, "m")
    # the claw marks, three talons at a time, all down the middle
    for x0 in (17, 25, 33):
        for i in range(3):
            x = x0 + i * 2
            c.put(x, 6, "d")
            c.put(x + 1, 7, "d")
            c.put(x + 1, 8, "m")
    # a trestle at each end
    x0 = 3
    c.rect(x0, 11, x0 + 2, 14, "m")
    c.vline(x0, 11, 14, "l")
    c.vline(x0 + 2, 11, 14, "d")
    c.rect(x0 - 1, 15, x0 + 3, 15, "k")
    c.vline(x0 - 1, 11, 14, "k")
    c.vline(x0 + 3, 11, 14, "k")
    for y in range(16):          # the right end mirrors the left
        for x in range(16):
            c.g[y][47 - x] = c.g[y][x]
    return c.text()


stamp("table_bare", "wood", _table_bare(), 3, 1,
      note="a long trestle table, bare but for the Harpies' claw marks")


# ==========================================================================
# The bird-catcher's house, Salmydessos
# ==========================================================================

def _bird(c, x, y, body, belly):
    c.paste(x, y, f"""
.kk..
k{body}{body}k.
k{body}k{body}k
k{body}{belly}{body}k
.k{belly}{belly}k
..kk.
""")


def _cage_stack():
    """The bird-catcher's stock: two long wicker cages stacked on a pole
    rack against the wall, a finch and a robin above, a linnet and a lark
    below. The bars repeat every 4 px, so only the birds cost tiles."""
    c = Canvas(32, 32)
    for (y0, y1) in ((2, 14), (18, 30)):
        c.rect(3, y0, 28, y1, "J")
        for y in range(y0 + 2, y1 - 1):
            for x in range(3, 29):
                if x % 4 != 0:
                    c.put(x, y, ".")
        c.hline(3, 28, y0, "j")
        c.hline(3, 28, y1 - 1, "j")
        c.hline(3, 28, y1, "K")
    _bird(c, 6, 8, "g", "v")
    _bird(c, 21, 8, "m", "J")
    _bird(c, 9, 24, "j", "J")
    _bird(c, 21, 24, "K", "w")
    c.outline()
    c.vline(1, 0, 31, "K")
    c.vline(30, 0, 31, "K")
    c.vline(2, 0, 31, "j")
    c.hline(1, 30, 15, "K")
    c.hline(1, 30, 31, "K")
    return c.text()


stamp("cage_stack", "nature", _cage_stack(), 2, 2,
      note="wicker cages stacked on a pole rack: a finch, a linnet, a robin, a lark")


def _lime_sticks():
    """Lime-sticks: long reeds standing in a pot, their tips smeared with
    mistletoe birdlime that glistens green; a feather stuck in one."""
    c = Canvas(16, 32)
    # four long reeds standing straight up in a tall jar
    for x in (4, 7, 10, 12):
        top = 1 if x in (7, 10) else 3
        c.vline(x, top, 20, "j")
        # the top third smeared with birdlime: a thick, pale, glistening
        # coat, wider than the reed
        for y in range(top, top + 8):
            c.put(x - 1, y, "n")
            c.put(x, y, "w" if (y - top) % 3 == 0 else "V")
        c.put(x, top - 1, "n")
    # a finch's feather stuck fast in the lime
    c.put(13, 6, "K")
    c.put(13, 7, "j")
    c.put(14, 7, "K")
    lathe(c, 8, 19, [3, 3.5, 4, 4.5, 4.5, 4.5, 4.5, 4.5, 4, 3.5, 3], ("J", "j", "j", "K", "K"))
    c.hline(4, 11, 19, "K")
    c.hline(5, 10, 23, "J")
    c.outline()
    return c.text()


stamp("lime_sticks", "nature", _lime_sticks(), 1, 2,
      note="lime-sticks: reeds in a pot, their tips smeared with mistletoe birdlime")


def _decoy_owl():
    """The decoy: a little owl on a post. Small birds come to mob it, and
    stick to the lime."""
    c = Canvas(16, 16)
    c.paste(3, 0, """
..kkkkkk..
.kKjjjjKk.
kKjJJJJjKk
kJJkJJkJJk
kJkkJJkkJk
kjJJKKJJjk
kKjjjjjjKk
.kjwjjwjk.
.kKjwwjKk.
..kjjjjk..
...kJJk...
""")
    c.rect(6, 11, 8, 14, "K")
    c.vline(6, 11, 14, "j")
    c.hline(4, 10, 15, "K")
    c.hline(5, 9, 14, "K")
    c.outline()
    return c.text()


stamp("decoy_owl", "nature", _decoy_owl(), 1, 1,
      note="a little owl on a post, the bird-catcher's decoy")


# ==========================================================================
# The Asclepeion, Aia: bronze and enamel
# ==========================================================================

def _counter_top(end):
    """The counter's bronze slab, seen from above and in front: an ink rim, a
    lit edge, the polished top, a dark lip. `end`: 'l', 'm' or 'r'."""
    c = Canvas(16, 16)
    x0 = 1 if end == "l" else 0
    x1 = 14 if end == "r" else 15
    c.rect(x0, 6, x1, 15, "k")
    c.rect(x0 + (1 if end == "l" else 0), 7, x1 - (1 if end == "r" else 0), 14, "y")
    c.hline(x0 + 1, x1 - 1, 7, "Y")
    c.hline(x0 + 1, x1 - 1, 8, "Y")
    c.hline(x0, x1, 13, "b")
    c.hline(x0, x1, 14, "z")
    if end == "l":
        c.vline(2, 8, 12, "Y")
    if end == "r":
        c.vline(13, 8, 12, "b")
    return c.text()


def _counter_front(end, emblem=False):
    """Its front: bronze framing round panels of blue enamel, a red rosette
    in each. The healer's panel carries Asclepius's rod and serpent."""
    c = Canvas(16, 16)
    x0 = 1 if end == "l" else 0
    x1 = 14 if end == "r" else 15
    c.rect(x0, 0, x1, 15, "k")
    c.rect(x0 + (1 if end == "l" else 0), 0, x1 - (1 if end == "r" else 0), 14, "b")
    c.hline(x0, x1, 0, "z")
    c.hline(x0, x1, 1, "y")
    c.rect(x0 + 2, 3, x1 - 2, 12, "z")
    c.rect(x0 + 3, 4, x1 - 3, 11, "u")
    c.hline(x0 + 3, x1 - 3, 4, "U")
    if emblem:
        c.vline(7, 4, 11, "y")
        c.vline(8, 4, 11, "b")
        for (x, y) in [(9, 5), (6, 6), (6, 7), (9, 8), (9, 9), (6, 10)]:
            c.put(x, y, "e")
        c.put(9, 4, "e")
        c.put(10, 4, "r")
    else:
        mx = (x0 + x1) // 2
        c.paste(mx - 1, 6, """
.r.
rYr
.r.
""")
    c.hline(x0, x1, 13, "z")
    c.hline(x0, x1, 14, "z")
    if end == "l":
        c.vline(2, 1, 13, "Y")
    if end == "r":
        c.vline(13, 1, 13, "z")
    return c.text()


for _end in "lmr":
    stamp(f"asc_top_{_end}", "bronze", _counter_top(_end), 1, 1,
          note=f"the healer's counter, bronze slab ({_end})")
    stamp(f"asc_front_{_end}", "bronze", _counter_front(_end), 1, 1,
          behavior={(0, 0): "MB_COUNTER"}, note=f"the counter's front: enamel panels in bronze ({_end})")
stamp("asc_front_rod", "bronze", _counter_front("m", emblem=True), 1, 1,
      behavior={(0, 0): "MB_COUNTER"}, note="the counter's front under the healer: Asclepius's rod in enamel")


def _bull_fountain():
    """The spring (2x2: the wall row, then the counter row). A bronze bull's
    head on the wall pours into a bronze basin. The heal animation sets the
    party's balls at x 9-23, y 8-24 of this piece, on the water. Batch 2's
    palace fountains recolour the water as milk, wine and oil."""
    c = Canvas(32, 32)
    # the bull's head, small, high on the wall
    c.paste(9, 0, """
Y............Y
Yy..........yb
.yYk......kyb.
..kyyyyyyyyzk.
.kyYkyyyykybzk
..kyYyyyyybzk.
...kyyyyyybk..
...kyYyyyybk..
..kbyyyyyyybk.
..kbFkyykFbzk.
...kbbkkbbzk..
....kk..kkk...
""")
    # the water pouring from its mouth
    c.rect(15, 11, 16, 14, "U")
    c.put(15, 12, "a")
    c.put(16, 14, "a")
    # the basin: rim, water, bowl, foot
    c.ellipse(16, 18.5, 14.5, 6.5, "y")
    c.ellipse(16, 18.5, 12.5, 4.8, "u")
    c.ellipse(16, 18, 11, 3.6, "U")
    for (x, y) in [(10, 17), (11, 17), (20, 18), (21, 18), (15, 16), (16, 16), (13, 20), (19, 19)]:
        c.put(x, y, "a")
    for x in range(2, 31):
        for y in range(19, 31):
            t = ((x + 0.5 - 16) / 14.5) ** 2 + ((y + 0.5 - 19) / 11.5) ** 2
            if t <= 1.0 and c.get(x, y) in ".":
                c.put(x, y, "b" if x < 14 else ("z" if x > 22 else "b"))
    for x in range(3, 30):
        if c.get(x, 24) in "bz":
            c.put(x, 24, "y")
    c.rect(12, 29, 19, 31, "z")
    c.hline(12, 19, 29, "b")
    c.outline()
    return c.text()


stamp("bull_fountain", "bronze", _bull_fountain(), 2, 2,
      note="the spring: a bronze bull's head pours into a bronze basin (the heal animation's balls land on its water)")


def lathe_sym(c, cx, y0, widths, ramp):
    """A turned vessel lit from the front, so its two halves mirror each
    other and cost half the tiles. ramp: four characters, centre to edge."""
    hi, lit, mid, low = ramp
    for j, hw in enumerate(widths):
        if hw <= 0:
            continue
        y = y0 + j
        for x in range(int(math.floor(cx - hw)), int(math.ceil(cx + hw))):
            t = abs(x + 0.5 - cx) / hw
            c.put(x, y, hi if t < 0.25 else lit if t < 0.55 else mid if t < 0.82 else low)


def _pithos_great():
    """The Pithos (2x2, standing against the back wall): a great clay jar
    banded with bronze, its lid sealed with honey-coloured wax. Lit from the
    front and drawn symmetric, so half its tiles are flips."""
    c = Canvas(32, 32)
    widths = [4, 5, 5, 5, 7, 9, 10.5, 11.5, 12, 12.5, 12.5, 12.5, 12.5, 12.5, 12, 12, 11.5, 11, 10.5,
              10, 9.5, 9, 8.5, 8, 7.5, 7, 7, 7.5, 8]
    lathe_sym(c, 16, 2, widths, ("h", "l", "m", "d"))
    for y, ch in ((7, "b"), (8, "d"), (19, "b"), (20, "d"), (27, "b")):
        hw = widths[y - 2]
        for x in range(int(16 - hw), int(16 + hw)):
            c.put(x, y, ch)
    # a rope-pattern band in relief, and the lid with its wax seal
    for x in range(4, 28):
        if c.get(x, 13) not in ".":
            c.put(x, 13, "h" if (x % 4) in (0, 3) else "d")
    c.rect(12, 1, 19, 3, "S")
    c.hline(12, 19, 1, "t")
    c.rect(14, 0, 17, 1, "n")
    c.outline()
    c.mirror_x()
    return c.text()


stamp("pithos_great", "clay", _pithos_great(), 2, 2,
      note="the Pithos: a great clay jar banded in bronze, its lid sealed with wax")


def _serpent_post():
    """Asclepius's serpent in bronze, coiled up a post on a round base."""
    c = Canvas(16, 32)
    c.rect(7, 6, 8, 27, "z")
    c.vline(7, 6, 27, "b")
    for j in range(18):
        y = 8 + j
        x = 8 + round(4 * math.sin(j * 0.7))
        c.put(x, y, "y")
        c.put(x + 1, y, "b")
    c.paste(9, 3, """
kk..
yYkr
byyk
.kk.
""")
    c.ellipse(8, 28.5, 6, 2.5, "b")
    c.hline(3, 12, 28, "y")
    c.outline()
    return c.text()


stamp("serpent_post", "bronze", _serpent_post(), 1, 2,
      note="Asclepius's bronze serpent coiled up a post")


# ==========================================================================
# The Agora, Aia
# ==========================================================================

def _stall_top(end):
    """The stall's timber counter: thick boards, end-grain at the ends. The
    left end carries a balance; the right a jug of the Pontic honey."""
    c = Canvas(16, 16)
    x0 = 1 if end == "l" else 0
    x1 = 14 if end == "r" else 15
    c.rect(x0, 7, x1, 15, "k")
    c.rect(x0 + (1 if end == "l" else 0), 8, x1 - (1 if end == "r" else 0), 14, "l")
    c.hline(x0 + 1, x1 - 1, 8, "h")
    c.hline(x0, x1, 12, "m")
    c.hline(x0, x1, 14, "d")
    if end == "l":
        c.paste(3, 0, """
....k....
....b....
kkkkykkkk
.b.....b.
kyk...kyk
kbk...kbk
.k.....k.
""")
    if end == "r":
        c.paste(5, 1, """
..kk..
.kRrk.
kRrrrk
kRrhrk
kRRrrk
.kkkk.
""")
    return c.text()


def _stall_front(end):
    """Its front: vertical planks with a carved boss, and the bronze nails."""
    c = Canvas(16, 16)
    x0 = 1 if end == "l" else 0
    x1 = 14 if end == "r" else 15
    c.rect(x0, 0, x1, 15, "k")
    c.rect(x0 + (1 if end == "l" else 0), 0, x1 - (1 if end == "r" else 0), 14, "m")
    for x in range(x0, x1 + 1):
        if x % 4 == 0:
            c.vline(x, 1, 13, "d")
        elif x % 4 == 1:
            c.vline(x, 1, 13, "l")
    c.hline(x0, x1, 0, "h")
    c.hline(x0, x1, 2, "d")
    for x in range(x0 + 1, x1, 4):
        c.put(x + 1, 3, "y")
        c.put(x + 1, 11, "b")
    c.hline(x0, x1, 13, "d")
    c.hline(x0, x1, 14, "d")
    return c.text()


for _end in "lmr":
    stamp(f"stall_top_{_end}", "wood", _stall_top(_end), 1, 1,
          note=f"the stallkeeper's timber counter ({_end})")
    stamp(f"stall_front_{_end}", "wood", _stall_front(_end), 1, 1,
          behavior={(0, 0): "MB_COUNTER"}, note=f"the counter's plank front ({_end})")


def _fleece_frame():
    """A fleece stretched on a frame to dry, gold dust caught in its wool:
    the hill people wash the Phasis's sand through fleeces (Strabo 11.2.19).
    Some say that's all the Golden Fleece ever was."""
    c = Canvas(32, 32)
    # the frame: four poles lashed at the corners
    c.rect(1, 2, 30, 3, "B")
    c.rect(1, 28, 30, 29, "B")
    c.rect(1, 2, 2, 29, "B")
    c.rect(29, 2, 30, 29, "B")
    c.hline(1, 30, 3, "n")
    c.hline(1, 30, 29, "n")
    c.vline(2, 2, 29, "n")
    c.vline(30, 2, 29, "n")
    for (x, y) in [(1, 2), (29, 2), (1, 28), (29, 28)]:
        c.rect(x, y, x + 1, y + 1, "o")
    # the hide: the body, four leg flaps reaching for the corners, the neck
    c.ellipse(16, 16.5, 8.5, 9.5, "c")
    for (x0, y0, x1, y1) in [(9, 10, 5, 6), (23, 10, 27, 6), (9, 22, 5, 26), (23, 22, 27, 26)]:
        for t in range(11):
            x = round(x0 + (x1 - x0) * t / 10)
            y = round(y0 + (y1 - y0) * t / 10)
            c.rect(x - 1, y - 1, x + 1, y + 1, "c")
    c.rect(14, 5, 18, 8, "c")
    # wool: curls in rows, shadowed on the right
    for y in range(4, 28):
        for x in range(4, 28):
            if c.get(x, y) == "c":
                if (x + 2 * (y // 3)) % 5 == 0 and y % 3 == 1:
                    c.put(x, y, "C")
                    c.put(x + 1, y, "C") if c.get(x + 1, y) == "c" else None
                elif x > 20 and (x + y) % 4 == 0:
                    c.put(x, y, "N")
    # gold dust caught in the wool, thickest low down where the water ran out
    for (x, y) in [(13, 10), (19, 9), (10, 15), (16, 14), (21, 16), (12, 19), (17, 19), (20, 21),
                   (14, 22), (9, 23), (22, 24), (16, 24), (18, 25), (11, 21)]:
        c.put(x, y, "y")
        c.put(x, y + 1, "o")
    c.outline()
    # cords from the flaps to the frame's corners
    for (x0, y0, x1, y1) in [(4, 5, 3, 4), (27, 5, 28, 4), (4, 27, 3, 27), (27, 27, 28, 27), (16, 4, 16, 4)]:
        c.line(x0, y0, x1, y1, "n")
    c.mirror_x()        # a stretched hide is symmetric, and so costs half the tiles
    return c.text()


stamp("fleece_frame", "cloth", _fleece_frame(), 2, 2,
      note="a fleece stretched to dry, gold dust from the Phasis caught in its wool")


def _pheasants():
    """Two pheasants hung by the feet from a peg: the Phasis's bird."""
    c = Canvas(16, 32)
    # the peg and the cord
    c.rect(6, 4, 9, 5, "K")
    c.put(6, 4, "J")
    # each bird hangs head down: feet at the cord, the long barred tail
    # pointing back up beside the legs, the copper body, a white neck ring,
    # the green head with its red face
    bird = """
.n.jK
.Kj.K
.Kj.j
.dmjK
dmmmj
mJmdm
dmmmd
mdmJm
dmmmd
.mdm.
.www.
.GgG.
.gmG.
.GGG.
..J..
"""
    c.paste(3, 6, bird)
    c.paste(8, 8, "\n".join(r[::-1] for r in bird.strip("\n").split("\n")))
    c.outline()
    return c.text()


stamp("pheasants", "nature", _pheasants(), 1, 2,
      note="two pheasants hung from a peg: the bird is named for the river Phasis")


def _log_post():
    """A timber post for the market hall, a bronze collar under its head."""
    c = Canvas(16, 48)
    c.rect(4, 0, 11, 45, "L")
    c.vline(4, 0, 45, "l")
    c.vline(5, 0, 45, "l")
    c.vline(11, 0, 45, "1")
    for y0 in range(0, 48, 8):          # bark streaks, repeating every 8 rows
        c.put(7, y0 + 2, "1")
        c.put(7, y0 + 3, "1")
        c.put(9, y0 + 6, "1")
    c.rect(3, 3, 12, 6, "3")
    c.hline(3, 12, 3, "4")
    c.hline(3, 12, 6, "2")
    c.rect(3, 42, 12, 45, "c")
    c.hline(3, 12, 42, "C")
    c.outline()
    return c.text()


stamp("log_post", "wall", _log_post(), 1, 3,
      note="a timber post for the market hall, a bronze collar at its head, on a clay footing")


def _linen_bolts():
    """Folded linen, stacked."""
    c = Canvas(16, 16)
    for i, y in enumerate((3, 7, 11)):
        x0 = 2 + (i % 2)
        c.rect(x0, y, x0 + 10, y + 3, "L")
        c.hline(x0, x0 + 10, y + 3, "C")
        c.vline(x0 + 10, y, y + 3, "N")
        c.put(x0 + 3, y + 1, "c")
        c.put(x0 + 7, y + 2, "c")
    c.outline()
    return c.text()


stamp("linen_bolts", "cloth", _linen_bolts(), 1, 1, note="bolts of folded Colchian linen")


# ==========================================================================
# Phrixos's sons' house, Aia
# ==========================================================================

def _ram_panel():
    """A painted panel in a bronze-bound frame, Greek work: the golden ram
    over the strait with Phrixos on its back, and Helle falling."""
    c = Canvas(32, 32)
    c.rect(2, 3, 29, 27, "z")
    c.rect(3, 4, 28, 26, "U")
    c.rect(3, 19, 28, 26, "u")
    for x in range(3, 29):
        if x % 5 in (0, 1):
            c.put(x, 19, "a")
        if (x + 2) % 6 == 0:
            c.put(x, 22, "a")
    c.hline(2, 29, 3, "y")
    c.vline(2, 3, 27, "y")
    # the ram, flying east, gold
    c.paste(8, 7, """
.......kk.kk...
......kyeekYek.
.kkkkkkyyyeeYk.
kyeeeeeyyyyek..
kYeeeeeeeyyk...
kyyyyyyyyybk...
.kybbkkkbbyk...
.kbk.....kbk...
.kk.......kk...
""")
    # Phrixos on its back, black-figure
    c.paste(12, 3, """
.k.
kkk
.k.
kkk
""")
    # Helle, falling head first into the sea
    c.paste(19, 15, """
k.k
.k.
.k.
kkk
.k.
""")
    c.put(20, 20, "a")
    c.put(19, 21, "a")
    c.put(21, 21, "a")
    c.rect(1, 28, 30, 29, "b")
    c.hline(1, 30, 28, "y")
    c.outline()
    return c.text()


stamp("ram_panel", "bronze", _ram_panel(), 2, 2,
      note="a painted panel: the golden ram over the strait, Phrixos on its back, Helle falling")


# ==========================================================================
# The linen-weaver's house, Aia
# ==========================================================================

def _ground_loom():
    """A ground loom, the Egyptian kind: two beams pegged to the floor, the
    warp stretched between them, a third of the cloth woven, the heddle rod
    resting across, the shuttle on the cloth."""
    c = Canvas(48, 32)
    # warp threads
    for x in range(6, 42):
        c.vline(x, 6, 25, "c" if x % 2 else "C")
    # the woven cloth from the near beam up
    c.rect(6, 15, 41, 25, "L")
    for y in range(15, 26):
        for x in range(6, 42):
            if (x + y) % 4 == 0:
                c.put(x, y, "c")
    c.hline(6, 41, 15, "N")
    # beams and pegs
    for y in (3, 26):
        c.rect(3, y, 44, y + 2, "B")
        c.hline(3, 44, y + 2, "n")
    for (x, y) in [(1, 2), (45, 2), (1, 25), (45, 25)]:
        c.rect(x, y, x + 1, y + 4, "n")
    # heddle rod and its two stones
    c.rect(5, 11, 42, 12, "B")
    c.hline(5, 42, 12, "n")
    for x in (4, 43):
        c.rect(x - 1, 10, x + 1, 13, "C")
    # the shuttle, laid across the middle of the cloth
    c.rect(18, 19, 29, 20, "B")
    c.hline(18, 29, 20, "n")
    c.outline()
    c.mirror_x()        # a loom is symmetric: half its tiles are flips
    return c.text()


stamp("ground_loom", "cloth", _ground_loom(), 3, 2,
      note="a ground loom, the Egyptian kind: beams pegged to the floor, a third of the linen woven")


def _flax():
    """Sheaves of flax leaning on the wall, still in blue flower at the top."""
    c = Canvas(16, 32)
    for i, x0 in enumerate((3, 8, 12)):
        for j in range(22):
            y = 6 + j
            x = x0 + round((j - 11) * 0.06 * (i - 1))
            c.put(x, y, "o" if (j + i) % 3 else "y")
            c.put(x + 1, y, "g" if j < 8 else "o")
        for (dx, dy) in [(-1, 4), (2, 3), (0, 2), (1, 5), (-1, 6)]:
            c.put(x0 + dx, dy, "u")
        c.put(x0, 3, "U")
        c.hline(x0 - 1, x0 + 2, 18, "n")
    c.hline(1, 15, 28, "o")
    c.outline()
    return c.text()


stamp("flax", "cloth", _flax(), 1, 2, note="sheaves of flax leaning on the wall, still in blue flower")


def _linen_line():
    """A cord across the wall from peg to peg, linen hung to bleach on it."""
    # Two lengths of linen on a taut cord, hung at the same place in each
    # block, so the two blocks are one.
    c = Canvas(32, 32)
    c.hline(0, 31, 10, "n")
    c.put(0, 9, "k")
    c.put(31, 9, "k")
    for x0 in (3, 19):
        c.rect(x0, 11, x0 + 9, 27, "L")
        c.vline(x0 + 9, 11, 27, "N")
        c.hline(x0, x0 + 9, 27, "C")
        c.vline(x0 + 4, 12, 26, "c")
        c.put(x0 + 1, 10, "B")
        c.put(x0 + 8, 10, "B")
    c.outline()
    return c.text()


stamp("linen_line", "cloth", _linen_line(), 2, 2, note="linen hung to bleach on a cord across the wall")


def _retting_tub():
    """A tub of water where the flax stalks rot loose from their fibre."""
    c = Canvas(16, 16)
    lathe(c, 8, 4, [7, 7, 7, 6.5, 6.5, 6.5, 6, 6, 6, 5.5], ("h", "l", "m", "d", "d"))
    c.ellipse(8, 5, 5.5, 1.6, "u")
    c.hline(4, 11, 5, "U")
    for y in (7, 11):
        for x in range(1, 15):
            if c.get(x, y) not in ".":
                c.put(x, y, "z")
    for (x, y) in [(5, 2), (6, 3), (9, 1), (9, 2), (10, 3), (12, 2)]:
        c.put(x, y, "o")
    c.outline()
    return c.text()


stamp("retting_tub", "wood", _retting_tub(), 1, 1, note="a tub of water where the flax rets")


# ==========================================================================
# The palace workshop, Aia: Hephaestus's self-moving works
# ==========================================================================

def _bull_head():
    """A bronze bull's head mounted on the wall, embers in its nostrils.
    Hephaestus made Aietes two such bulls whole; batch 2's palace halls set
    heads like this one in the walls, breathing fire down the corridors."""
    c = Canvas(16, 32)
    # a round bronze boss on the wall, then the head over it, front on: the
    # horns sweeping out and up, the broad brow, the ears, the eyes, the long
    # face and the wide muzzle with glowing nostrils and a ring
    c.ellipse(8, 18, 7.5, 7.5, "z")
    c.ellipse(8, 18, 6.5, 6.5, "b")
    c.paste(0, 3, """
Y..............Y
Yy............yb
.Yy..........yb.
.yYy........ybz.
..yYyk....kybz..
...kyYyyyyyybk..
.kkYyyyyyyyyybkk
kyyYykyyyykybzzk
.kkyykkyykkybkk.
...kyYyyyyybzk..
...kyYyyyyybzk..
....kyyyyyybk...
....kyYyyyybk...
....kyyyyyybk...
...kbyyyyyyybk..
..kbYyyyyyyybzk.
..kbkfFkkFfkbzk.
..kbkeFkkFekbzk.
...kbbyyyybbzk..
....kkbkkbkkk...
.....kb..bk.....
......kbbk......
""")
    c.outline()
    return c.text()


stamp("bull_head", "bronze", _bull_head(), 1, 2,
      note="a bronze bull's head on the wall, embers in its nostrils (batch 2's halls breathe fire with it)")


def _golden_maid():
    """One of Hephaestus's golden maids (Iliad 18.417-420): gold, like a
    living girl, with sense in her and a voice. This one holds a jug and
    turns her head to follow you."""
    c = Canvas(16, 32)
    c.paste(4, 1, """
..kkkk..
.kbbbbk.
kbYyyybk
kbYkykbk
kbyyyybk
.kbyybk.
..kyyk..
.kYyyyk.
kYyyyyyk
kYykyyykk
kYyyyykbbk
kYyykyykbk
.kYyyyykbk
.kYyykyk..
.kYyyyyk..
.kYyyykyk.
kYyyyyyyzk
kYyykyyyzk
kYyyyyyyzk
kYyyykyyzk
kYyyyyyyzk
kyyyyyyyzk
kzzzzzzzzk
.kkkkkkkk.
""")
    c.ellipse(8, 28.5, 6.5, 2, "z")
    c.hline(3, 12, 28, "b")
    c.outline()
    return c.text()


stamp("golden_maid", "bronze", _golden_maid(), 1, 2,
      note="one of Hephaestus's golden maids, a jug in her hands; she turns her head to follow you")


def _fire_jar():
    """The fire-jar: a bronze stamnos full of coals that never go out, its
    lid propped, the heat shimmering. Rotom Heat's appliance."""
    c = Canvas(16, 32)
    c.paste(3, 1, """
....e.....
...eFe..e.
..eFfFe.Fe
..FfffF.fF
.kFfkfFkFk
""")
    widths = [4, 4.5, 5, 6, 6.5, 7, 7, 7, 7, 6.5, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3.5, 4, 4.5]
    lathe(c, 8, 6, widths, ("Y", "y", "b", "z", "z"))
    for y in (8, 15):
        for x in range(1, 15):
            if c.get(x, y) in "Yybz":
                c.put(x, y, "f" if y == 8 else "Y")
    c.rect(4, 6, 11, 7, "F")
    c.hline(5, 10, 6, "e")
    c.put(1, 12, "k")
    c.put(14, 12, "k")
    c.put(0, 11, "b")
    c.put(15, 11, "z")
    c.rect(4, 26, 11, 27, "z")
    c.outline()
    return c.text()


stamp("fire_jar", "bronze", _fire_jar(), 1, 2,
      note="the fire-jar: a bronze stamnos of coals that never go out (Rotom's heat form)")


def _wash_basin():
    """The wash-basin: a bronze louter, a wide shallow bowl of water on a
    fluted stand. Rotom's wash form."""
    c = Canvas(16, 32)
    c.ellipse(8, 9, 7.5, 3.5, "y")
    c.ellipse(8, 9, 6, 2.3, "u")
    c.hline(4, 11, 8, "U")
    c.put(6, 9, "a")
    c.put(10, 8, "a")
    for y in range(11, 15):
        hw = 7 - (y - 11) * 1.3
        for x in range(int(8 - hw), int(8 + hw)):
            c.put(x, y, "b" if x < 9 else "z")
    c.rect(6, 15, 9, 25, "b")
    c.vline(6, 15, 25, "y")
    c.vline(9, 15, 25, "z")
    c.vline(7, 16, 24, "Y")
    c.rect(5, 17, 10, 17, "z")
    c.ellipse(8, 27, 5, 2, "b")
    c.hline(4, 11, 26, "y")
    c.put(12, 13, "U")
    c.put(12, 15, "a")
    c.outline()
    return c.text()


stamp("wash_basin", "bronze", _wash_basin(), 1, 2,
      note="the wash-basin: a bronze louter of water on a fluted stand (Rotom's wash form)")


def _cold_krater():
    """The cold krater: a bronze bell krater white with rime, icicles from
    its lip, cold breath rising. Rotom's frost form."""
    c = Canvas(16, 32)
    # cold breath curling up from the mouth
    for (x, y) in [(5, 2), (6, 1), (7, 1), (8, 2), (9, 3), (10, 2), (11, 1), (6, 4), (7, 3)]:
        c.put(x, y, "a")
    # the krater: a bronze bell bowl gone blue-white with rime
    widths = [7.5, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4.5, 4.5, 4, 3.5, 3, 2.5, 2, 2, 2, 3.5, 5, 5.5]
    lathe(c, 8, 6, widths, ("a", "M", "U", "u", "u"))
    # the lip, still bronze under the frost, and the ice on it
    c.hline(1, 14, 6, "y")
    c.hline(1, 14, 7, "b")
    c.hline(2, 13, 6, "a")
    # icicles hanging off the lip
    for (x, h) in [(1, 4), (3, 6), (6, 3), (10, 5), (13, 4)]:
        c.vline(x, 8, 7 + h, "a")
        c.put(x, 8 + h, "M")
    # the foot: bronze showing through
    c.hline(4, 11, 24, "b")
    c.hline(3, 12, 25, "z")
    c.outline()
    return c.text()


stamp("cold_krater", "bronze", _cold_krater(), 1, 2,
      note="the cold krater: a bronze krater white with rime, icicles at its lip (Rotom's frost form)")


def _fan():
    """The fan: a rhipis of bronze leaves on a pole that turns by itself and
    keeps the workshop cool. Rotom's fan form."""
    c = Canvas(16, 32)
    # the fan's head: a half-disc of bronze blades, alternately lit and dark,
    # with a gilt rim, spread above its hub
    cx, cy, R = 7.5, 14.0, 7.6
    for y in range(0, 15):
        for x in range(16):
            dx, dy = x + 0.5 - cx, cy - (y + 0.5)
            r = math.hypot(dx, dy * 1.05)
            if dy < -0.5 or r > R or r < 1.5:
                continue
            a = math.atan2(dy, dx)
            blade = int(a / math.pi * 9)
            if r > R - 1.2:
                ch = "Y"
            elif blade % 2:
                ch = "y"
            else:
                ch = "b"
            c.put(x, y, ch)
    c.ellipse(7.5, 14, 2.2, 1.6, "z")
    c.put(7, 13, "Y")
    # the pole and its three-footed stand
    c.rect(7, 16, 8, 27, "z")
    c.vline(7, 16, 27, "b")
    c.paste(3, 27, """
..kbbbbk..
.kbz..zbk.
kbz....zbk
""")
    c.outline()
    return c.text()


stamp("fan", "bronze", _fan(), 1, 2, note="the fan: a rhipis of bronze leaves on a turning pole (Rotom's fan form)")


def _sledge():
    """The reaping-sledge: a heavy board shod underneath with rows of bronze
    blades, its front curled up, a rope to drag it by. Rotom's mow form."""
    c = Canvas(32, 16)
    # the board, two planks pegged together, seen from above
    c.rect(6, 3, 30, 12, "l")
    c.hline(6, 30, 3, "h")
    c.hline(6, 30, 7, "m")
    c.hline(6, 30, 8, "h")
    c.hline(6, 30, 12, "m")
    # the front curled up like a sledge's runner, with the drag-rope
    c.rect(2, 4, 5, 11, "l")
    c.vline(2, 4, 11, "h")
    c.vline(3, 5, 10, "m")
    c.rect(0, 6, 1, 9, "d")
    c.put(0, 5, "C")
    c.put(0, 10, "C")
    # rows of bronze blades set into it, edges catching the light
    for y in (4, 9):
        for x in range(8, 30, 4):
            c.paste(x, y, "yb\nbz")
    # the pegs
    for x in (12, 22):
        c.put(x, 7, "d")
        c.put(x, 8, "d")
    c.hline(6, 30, 13, "d")
    c.outline()
    return c.text()


stamp("sledge", "wood", _sledge(), 2, 1,
      note="the reaping-sledge: a board shod with rows of bronze blades (Rotom's mow form)")


def _workbench():
    """Tekton's bench: a half-built wheeled tripod, a hammer and tongs."""
    c = Canvas(32, 16)
    c.rect(1, 6, 30, 10, "l")
    c.hline(1, 30, 6, "h")
    c.hline(1, 30, 10, "m")
    for x0 in (3, 26):
        c.rect(x0, 11, x0 + 2, 15, "m")
        c.vline(x0 + 2, 11, 15, "d")
    # the tripod: a bowl on three legs, one wheel on
    c.paste(5, 0, """
.kkkkkkk.
kbyyyyybk
.kzbbbzk.
..kzkzk..
..zkkkz..
.zk.k.kz.
""")
    c.put(4, 5, "y")
    c.put(14, 5, "y")
    # hammer and tongs
    c.rect(18, 3, 21, 4, "z")
    c.hline(21, 26, 4, "m")
    c.line(23, 1, 28, 5, "z")
    c.line(24, 1, 29, 4, "b")
    c.outline()
    return c.text()


stamp("workbench", "wood", _workbench(), 2, 1,
      note="Tekton's workbench: a half-built wheeled tripod, a hammer, tongs")


def _tripod_wheels():
    """One of the self-moving tripods (Iliad 18.373-377): a bronze cauldron
    on three legs, gold wheels under each foot."""
    c = Canvas(16, 16)
    c.paste(1, 1, """
.kkkkkkkkkkkk.
kYyyyyyyyyyybk
.kybbbbbbbbzk.
..kzbbbbbbzk..
...kkzzzzkk...
...kz.kk.zk...
..kz..kk..zk..
..kz..kk..zk..
.kz...kk...zk.
kYyk.kYyk.kYyk
kyzk.kyzk.kyzk
.kk...kk...kk.
""")
    c.outline()
    return c.text()


stamp("tripod_wheels", "bronze", _tripod_wheels(), 1, 1,
      note="a self-moving tripod: a bronze cauldron on three legs, gold wheels under its feet")
