#!/usr/bin/env python3
"""Nonakris, the village at Styx Falls: the Inn at the Falls, Horkia's house of
oaths and Kepheus's house with its lean-to. Registered into
arkrooms_art.STAMPS on import.

The inn and Horkia's house are built back into the black cliff of the cirque,
so their back walls are the rock itself (arkrooms_art's "rock" wall); the rest
is whitewash over rubble against the damp, and slate underfoot."""
from arkrooms_art import Canvas, stamp, noise

# ---------------------------------------------------------------------------
# The inn
# ---------------------------------------------------------------------------


def _rock_hearth():
    """2x3: a hearth cut into the cliff. The niche (rows 0-1) is a dark arch in
    the rock with a black cauldron hung on a chain from an iron bar; on the
    floor row, the stone curb, the fire and its logs. Soot licks the rock above
    the arch. All clay: the dark of the niche is the clay palette's ash grey."""
    c = Canvas(32, 48)
    # soot on the rock above and round the arch
    for y in range(0, 12):
        for x in range(4, 28):
            d = abs(x - 15.5) / 12.0 + (12 - y) / 14.0
            if d < 1.0 and noise(x, y, 61) < 1.15 - d:
                c.put(x, y, "a" if d < 0.6 else "s")
    # the arch: a rounded top from y 6, walls down to the floor row
    for y in range(6, 40):
        for x in range(3, 29):
            if y < 14:
                r = ((x - 15.5) / 12.5) ** 2 + ((y - 14) / 8.0) ** 2
                if r > 1.0:
                    continue
                edge = r > 0.78
            else:
                edge = x in (3, 4, 27, 28)
            if edge:
                c.put(x, y, "k")
            else:
                c.put(x, y, "a" if y < 20 or noise(x, y, 3) < 0.7 else "k")
    # the iron bar and chain, the cauldron
    c.hline(6, 25, 10, "s")
    c.hline(6, 25, 11, "k")
    for y in range(12, 22):
        c.put(15, y, "t" if y % 2 else "s")
        c.put(16, y, "s" if y % 2 else "k")
    c.ellipse(15.5, 26, 8.5, 5.5, "s", "k")
    c.hline(8, 23, 21, "k")
    c.hline(9, 22, 22, "t")
    c.hline(9, 22, 23, "S")
    for x in range(9, 23):
        if noise(x, 24, 4) < 0.4:
            c.put(x, 24, "t")
    c.put(10, 26, "t")
    c.put(11, 27, "t")
    # the curb on the floor row, the fire and logs inside it
    c.box(1, 33, 30, 45, "S")
    c.hline(2, 29, 34, "t")
    c.hline(2, 29, 44, "s")
    c.rect(4, 36, 27, 42, "a")
    for (x0, x1, y) in [(6, 25, 41), (8, 23, 40)]:
        c.hline(x0, x1, y, "d")
        if y == 41:
            c.hline(x0, x1, y + 1, "k")
    flames = [(8, 39, "f"), (9, 38, "F"), (10, 37, "f"), (11, 36, "F"), (12, 35, "Y"), (13, 36, "F"),
              (14, 37, "f"), (15, 34, "Y"), (16, 35, "F"), (17, 36, "Y"), (18, 37, "F"), (19, 36, "f"),
              (20, 37, "F"), (21, 38, "f"), (22, 39, "F"), (12, 38, "Y"), (16, 38, "Y"), (19, 39, "Y"),
              (11, 39, "F"), (14, 39, "Y"), (18, 39, "F"), (15, 36, "F"), (15, 37, "Y"), (15, 38, "F")]
    for (x, y, col) in flames:
        c.put(x, y, col)
    for x in range(4, 28):
        if c.get(x, 32) == "k" or c.get(x, 32) == "a":
            c.put(x, 32, "k")
    return c


stamp("rock_hearth", 2, 3, art=[("clay", _rock_hearth())],
      note="the inn's hearth, cut into the cliff: a black cauldron on a chain over the fire")


def _sleep_bench(blanket):
    """2x1: a sleeping bench of planks on stone feet against the cliff, a
    blanket rolled at one end and a fleece spread on it."""
    c = Canvas(32, 16)
    c.box(0, 3, 31, 11, "l")
    c.hline(1, 30, 4, "h")
    for x in (8, 16, 24):
        c.vline(x, 5, 10, "m")
    c.hline(1, 30, 10, "m")
    c.box(0, 11, 31, 14, "d")
    for x in (2, 3, 28, 29):
        c.vline(x, 14, 15, "k")
    # the fleece
    c.ellipse(18, 7, 10, 3.5, "c", "C")
    for (x, y) in [(12, 6), (16, 5), (21, 6), (24, 8), (14, 9), (19, 8)]:
        c.put(x, y, "C")
    # the rolled blanket at the head
    main, dark = {"red": ("r", "R"), "blue": ("U", "u"), "cream": ("C", "m")}[blanket]
    c.box(2, 2, 9, 11, main)
    for y in range(3, 11):
        c.put(5, y, dark)
        c.put(6, y, main)
    c.hline(3, 8, 3, dark)
    return c


for _b in ("red", "blue", "cream"):
    stamp(f"sleep_bench_{_b}", 2, 1, art=[("wood", _sleep_bench(_b))],
          note=f"a sleeping bench against the cliff, a {_b} blanket rolled at its head")


def _long_table():
    """4x2: the inn's long table, a trestle board scrubbed pale, laid with a
    loaf, bowls, cups and a red jug (all the wood palette's colors)."""
    c = Canvas(64, 32)
    c.box(0, 4, 63, 22, "h")
    c.hline(1, 62, 5, "y")
    for y in (10, 16):
        c.hline(1, 62, y, "l")
    c.box(0, 22, 63, 26, "m")
    c.hline(1, 62, 25, "d")
    for x in (4, 5, 58, 59):
        c.vline(x, 26, 30, "d")
        c.put(x, 31, "k")
    c.hline(4, 59, 28, "d")
    # bowls
    for bx in (6, 22, 40, 54):
        c.ellipse(bx + 3, 13, 3.5, 2.5, "C", "k")
        c.hline(bx + 1, bx + 5, 12, "d")
        c.put(bx + 2, 13, "b")
    # the loaf
    c.ellipse(31, 10, 5, 3.5, "b", "k")
    c.hline(28, 33, 9, "y")
    c.put(29, 11, "z")
    c.put(32, 11, "z")
    # cups
    for (x, y) in [(14, 8), (47, 9), (18, 18)]:
        c.box(x, y, x + 3, y + 3, "r")
        c.hline(x + 1, x + 2, y + 1, "R")
    # the red jug
    c.ellipse(36, 16, 3, 4, "r", "k")
    c.put(36, 11, "k")
    c.put(37, 12, "k")
    c.hline(35, 37, 15, "R")
    c.put(35, 14, "c")
    return c


stamp("long_table", 4, 2, art=[("wood", _long_table())],
      note="the inn's long table, laid with bread, bowls, cups and a red jug")


def _bench(n, seed=0):
    """n x 1: a plain plank bench."""
    w = 16 * n
    c = Canvas(w, 16)
    c.box(1, 5, w - 2, 10, "l")
    c.hline(2, w - 3, 6, "h")
    c.hline(2, w - 3, 9, "m")
    c.box(1, 10, w - 2, 12, "d")
    for x in (3, 4, w - 5, w - 4):
        c.vline(x, 12, 15, "k")
    return c


stamp("bench4", 4, 1, art=[("wood", _bench(4))], note="a long plank bench")
stamp("bench2", 2, 1, art=[("wood", _bench(2))], note="a plank bench")


def _door_hoof():
    """4x1: the inn's door, from inside. Two posts, a lintel over the doorway
    (top layer, so you pass under it), and on a nail at its middle the house's
    luck: a horse's hoof. The doorway's own cells are the exit."""
    posts = Canvas(64, 16)
    for x0 in (5, 48):
        posts.box(x0, 0, x0 + 10, 15, "m")
        posts.vline(x0 + 2, 1, 14, "l")
        posts.vline(x0 + 3, 1, 14, "h")
        posts.vline(x0 + 8, 1, 14, "d")
        posts.hline(x0 + 1, x0 + 9, 0, "h")
        posts.hline(x0 + 1, x0 + 9, 14, "d")
    top = Canvas(64, 16)
    top.box(16, 0, 47, 5, "m")
    top.hline(16, 47, 1, "h")
    top.hline(16, 47, 2, "l")
    top.hline(16, 47, 4, "d")
    # the nail and the hoof, hung heel down, as big as a fist
    top.put(31, 5, "k")
    top.put(32, 5, "k")
    top.paste(27, 6, """
..kkkkkk..
.kdmmmmdk.
kdmlhhlmdk
kdmlllmmdk
kdmk..kmdk
kdk....kdk
.k......k.
""")
    sill = Canvas(64, 16)
    th = _threshold()
    for y in range(16):
        for x in range(32):
            sill.put(16 + x, y, th.get(x, y))
    return posts, top, sill


def _threshold():
    """The door's threshold, worn slate (flat on the slate floor)."""
    c = Canvas(32, 16)
    c.rect(0, 0, 31, 15, "7")
    c.hline(0, 31, 0, "6")
    c.hline(0, 31, 1, "8")
    c.hline(0, 31, 14, "6")
    c.hline(0, 31, 15, "e")
    for x in range(2, 30):
        if noise(x, 8, 4) < 0.25:
            c.put(x, 8, "8")
    c.hline(10, 21, 7, "9")
    return c


stamp("threshold", 2, 1, flat=[("rock", _threshold())], walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"},
      note="a slate doorstep worn hollow by boots; both cells are the exit")

_p, _t, _s = _door_hoof()
stamp("door_hoof", 4, 1, art=[("wood", _p)], top=[("wood", _t)], flat=[("rock", _s)],
      walk={(1, 0), (2, 0)},
      behavior={(1, 0): "MB_SOUTH_ARROW_WARP", (2, 0): "MB_SOUTH_ARROW_WARP"},
      note="the inn's doorway: two posts, a lintel, and on a nail the horse's hoof, the house's luck")


def _window_falls():
    """1x2 on whitewash: a deep window with its blue shutters open, and across
    the pool the black cliff and the one white thread of the Styx, lost in mist
    at the top and never landing."""
    c = Canvas(16, 32)
    c.box(2, 6, 13, 27, "a", "k")
    c.rect(3, 7, 12, 26, "a")
    # a strip of pale sky, mist on the cliff's top, then the cliff; the falls a
    # white thread down it that thins into mist and never lands
    for y in range(10, 25):
        for x in range(3, 13):
            c.put(x, y, "k" if noise(x, y, 8) > 0.15 else "1")
    for y in (9, 10):
        for x in range(3, 13):
            c.put(x, y, "S" if (x + y) % 3 else "s")
    for y in range(11, 23):
        c.put(8, y, "w" if y % 4 else "p")
        if y > 18:
            c.put(7 + (y % 2) * 2, y, "S")
    for y in (23, 24):
        for x in range(5, 11):
            if (x + y) % 2:
                c.put(x, y, "S")
    for x in range(3, 13):
        c.put(x, 25, "1")
        c.put(x, 26, "k")
    # the frame and the shutters
    c.hline(1, 14, 5, "2")
    c.hline(1, 14, 28, "3")
    c.hline(1, 14, 29, "1")
    c.box(0, 6, 1, 27, "b", "k")
    c.vline(0, 6, 27, "B")
    c.box(14, 6, 15, 27, "b", "k")
    c.vline(15, 6, 27, "b")
    return c


stamp("window_falls", 1, 2, art=[("wall", _window_falls())],
      note="a window across the black pool to the falls, which fall and fall and never seem to land")


def _cup_shelf():
    """2x2 on the wall: the innkeeper's board of cups and jugs on two shelves."""
    c = Canvas(32, 32)
    for y in (13, 27):
        c.box(1, y, 30, y + 3, "m")
        c.hline(2, 29, y + 1, "l")
        c.put(4, y + 4, "k")
        c.put(27, y + 4, "k")
    # cups on the top shelf, jugs below
    for (x, col) in [(4, "r"), (10, "C"), (16, "r"), (22, "C")]:
        c.box(x, 7, x + 4, 12, col)
        c.hline(x + 1, x + 3, 8, "R" if col == "r" else "c")
    for (x, col) in [(4, "r"), (14, "u"), (23, "r")]:
        c.ellipse(x + 3, 22, 3.5, 4.5, col, "k")
        c.put(x + 3, 17, "k")
        c.put(x + 4, 17, "k")
        c.hline(x + 2, x + 4, 22, "R" if col == "r" else "U")
    return c


stamp("cup_shelf", 2, 2, art=[("wood", _cup_shelf())], note="the inn's shelf of cups and jugs")


def _basket():
    """1x1: a wicker basket lined with straw: Gryllos's, on the floor at
    Eubouleus's feet (the piglet is an object sitting in it)."""
    c = Canvas(16, 16)
    c.ellipse(7.5, 10, 7, 5, "j", "k")
    c.ellipse(7.5, 8, 6, 2.5, "K", "k")
    for x in range(2, 14):
        c.put(x, 8, "J" if x % 2 else "j")
    for y in range(10, 14):
        for x in range(2, 14):
            if (x + y) % 3 == 0 and c.get(x, y) == "j":
                c.put(x, y, "K")
    return c


stamp("piglet_basket", 1, 1, art=[("nature", _basket())],
      note="Gryllos's basket, lined with straw")


def _firewood():
    """1x1: split logs stacked by the hearth, end grain out."""
    c = Canvas(16, 16)
    for (cx, cy) in [(4, 12), (9, 12), (14, 12), (6.5, 8), (11.5, 8), (9, 4)]:
        c.ellipse(cx, cy, 2.6, 2.4, "l", "k")
        c.put(int(cx), int(cy), "m")
        c.put(int(cx) - 1, int(cy) - 1, "h")
    for x in range(1, 16):
        if c.get(x, 15) == ".":
            c.put(x, 15, "d")
    return c


stamp("firewood", 1, 1, art=[("wood", _firewood())], note="split logs stacked by the hearth")


def _cloaks():
    """1x2 on the wall: travellers' cloaks and a straw hat on pegs, a staff
    leaning under them: the pilgrims who came up to swear."""
    c = Canvas(16, 32)
    c.hline(1, 14, 6, "d")
    c.hline(1, 14, 7, "m")
    for (x0, w, main, dark) in ((1, 6, "r", "R"), (8, 7, "u", "U")):
        for y in range(8, 27):
            spread = (y - 8) // 6
            for x in range(x0 - spread // 2, x0 + w + spread // 2):
                c.put(x, y, dark if x in (x0 - spread // 2, x0 + w + spread // 2 - 1) else main)
        c.hline(x0, x0 + w - 1, 8, "k")
    c.ellipse(7.5, 4.5, 5, 2, "y", "z")
    c.hline(5, 10, 3, "b")
    for y in range(4, 31):
        c.put(13 - (y - 4) // 14, y, "l")
    return c


stamp("cloaks", 1, 2, art=[("wood", _cloaks())], note="pilgrims' cloaks and a straw hat on pegs, a staff under them")


def _puddle(seed):
    """1x1, flat on slate: where the cliff weeps onto the floor."""
    c = Canvas(16, 16)
    import math
    for y in range(16):
        for x in range(16):
            r = ((x - 7.5) / (6.5 + seed)) ** 2 + ((y - 7 - seed) / 3.5) ** 2
            r += 0.25 * math.sin(x * 0.9 + seed)
            if r < 1.0:
                # wet slate: just darker stone, a sheen of the cliff's blue in it
                c.put(x, y, "6" if r > 0.5 else ("e" if (x + y) % 3 else "3"))
    c.put(5, 6 + seed, "4")
    c.put(6, 6 + seed, "5")
    c.put(10, 8 + seed, "4")
    return c


stamp("puddle", 1, 1, flat=[("rock", _puddle(0))], walk={(0, 0)}, note="a dark puddle where the cliff weeps")
stamp("puddle_b", 1, 1, flat=[("rock", _puddle(1))], walk={(0, 0)}, note="a dark puddle where the cliff weeps")

# ---------------------------------------------------------------------------
# Horkia's house of oaths
# ---------------------------------------------------------------------------

HOOF = """
.kkkk.
kmhhlk
kmllmk
kdmmdk
kddddk
.kkkk.
"""


def _hoofcups(c, x, y, n, tags=True, seed=0):
    """A row of n hoof-cups at (x, y) (6 px tall, standing on y+6), each with a
    linen scrap tied round it and hanging over the shelf's edge."""
    for i in range(n):
        cx = x + i * 7
        c.paste(cx, y, HOOF)
        if tags:
            ty = y + 3 + int(noise(i, seed, 7) * 2)
            c.put(cx + 4, ty, "c")
            c.put(cx + 5, ty, "c")
            c.put(cx + 5, ty + 1, "c")
            c.put(cx + 5, ty + 2, "C")
            c.put(cx + 6, ty + 3, "c")


def _niche_wall(n):
    """n x 1 on the cliff: ledges cut into the black rock, hoof-cups standing on
    them, linen tags hanging. The recess is flat rock; the cups wood."""
    w = 16 * n
    rock = Canvas(w, 16)
    cups = Canvas(w, 16)
    rock.rect(1, 3, w - 2, 11, "2")
    rock.hline(1, w - 2, 3, "1")
    rock.hline(1, w - 2, 4, "1")
    rock.hline(1, w - 2, 2, "k")
    rock.hline(1, w - 2, 12, "5")
    rock.hline(1, w - 2, 13, "4")
    rock.hline(1, w - 2, 14, "1")
    rock.vline(1, 2, 12, "1")
    rock.vline(w - 2, 2, 12, "3")
    _hoofcups(cups, 3, 6, (w - 6) // 7, seed=n)
    return rock, cups


_r, _c = _niche_wall(2)
stamp("cup_ledge", 2, 1, flat=[("rock", _r)], art=[("wood", _c)],
      note="a ledge cut in the cliff, hoof-cups standing on it, every one tagged with a name")
_r, _c = _niche_wall(1)
stamp("cup_ledge1", 1, 1, flat=[("rock", _r)], art=[("wood", _c)],
      note="a small ledge in the cliff, two hoof-cups on it")


def _hoof_rack(cols):
    """cols x 2: a freestanding rack of three shelves, dozens of hoof-cups on
    it, each tied with a scrap of linen, a name scratched on it."""
    w = 16 * cols
    c = Canvas(w, 32)
    c.box(0, 1, w - 1, 30, "d")
    c.rect(2, 2, w - 3, 28, "k")
    for y in (10, 19, 28):
        c.hline(1, w - 2, y, "l")
        c.hline(1, w - 2, y + 1, "m")
    c.vline(1, 2, 29, "m")
    c.vline(w - 2, 2, 29, "m")
    for i, y in enumerate((4, 13, 22)):
        _hoofcups(c, 3, y, (w - 6) // 7, seed=i + cols)
    c.hline(0, w - 1, 31, "k")
    return c


stamp("hoof_rack2", 2, 2, art=[("wood", _hoof_rack(2))],
      note="a rack of hoof-cups, three shelves deep, each cup tagged with a name")
stamp("hoof_rack1", 1, 2, art=[("wood", _hoof_rack(1))],
      note="a narrow rack of hoof-cups along the wall")


def _oath_table():
    """2x1: Horkia's table: today's wax tablet, open, the stylus by it; a bowl
    of the linen scraps waiting for names."""
    c = Canvas(32, 16)
    c.box(0, 2, 31, 11, "l")
    c.hline(1, 30, 3, "h")
    c.box(0, 11, 31, 13, "d")
    for x in (2, 29):
        c.vline(x, 13, 15, "k")
    # the tablet: two leaves of dark wax in a wooden frame
    c.box(4, 3, 19, 10, "z")
    c.rect(5, 4, 11, 9, "R")
    c.rect(13, 4, 18, 9, "R")
    c.vline(12, 4, 9, "z")
    for y in (5, 7):
        c.hline(6, 10, y, "r")
        c.hline(14, 17, y, "r")
    c.put(8, 9, "r")
    c.put(21, 9, "k")
    c.put(22, 8, "k")
    c.put(23, 7, "y")
    # the bowl of scraps
    c.ellipse(26, 6, 3.5, 2.5, "m", "k")
    c.put(25, 5, "c")
    c.put(27, 6, "c")
    c.put(26, 5, "C")
    return c


stamp("oath_table", 2, 1, art=[("wood", _oath_table())],
      note="the table of the day's oaths: a wax tablet open, the stylus, a bowl of linen scraps")


def _lamp_niche():
    """1x1 on the cliff: a niche with a clay lamp that is never put out. The
    rock round it is lit warm (flat), the lamp and flame bronze."""
    rock = Canvas(16, 16)
    rock.rect(3, 3, 12, 12, "1")
    rock.hline(3, 12, 3, "k")
    rock.hline(3, 12, 13, "4")
    for (x, y) in [(2, 6), (13, 6), (2, 9), (13, 9), (5, 2), (10, 2), (4, 14), (11, 14)]:
        rock.put(x, y, "4")
    for (x, y) in [(1, 8), (14, 8), (7, 1), (8, 15)]:
        rock.put(x, y, "3")
    lamp = Canvas(16, 16)
    lamp.paste(4, 4, """
...e....
..eYe...
..eYe...
...F....
.kkkkkk.
kbyyyybk
.kbbbzk.
..kkkk..
""")
    return rock, lamp


_r, _l = _lamp_niche()
stamp("lamp_niche", 1, 1, flat=[("rock", _r)], art=[("bronze", _l)],
      note="a lamp in a niche in the cliff; it has never been put out")

# ---------------------------------------------------------------------------
# Kepheus's house and lean-to
# ---------------------------------------------------------------------------


def _bars():
    """1x2: crowbars and a long iron lever leaning on the planks, clay greys."""
    c = Canvas(16, 32)
    for (x0, top, lean) in [(3, 3, 1), (7, 1, 2), (11, 5, 1)]:
        for y in range(top, 30):
            x = x0 + (lean * (30 - y)) // 30
            c.put(x, y, "s")
            c.put(x + 1, y, "a")
        c.put(x0 + lean, top, "t")
        c.put(x0 + lean - 1, top + 1, "S")
    c.hline(1, 14, 30, "a")
    c.hline(1, 14, 31, "k")
    return c


stamp("crowbars", 1, 2, art=[("clay", _bars())], note="crowbars and a long iron lever, leaning on the planks")


def _mattocks():
    """1x2: two mattocks and a sledgehammer, heads up, handles worn pale."""
    c = Canvas(16, 32)
    for (x, top) in [(3, 8), (8, 6), (12, 9)]:
        for y in range(top + 3, 31):
            c.put(x, y, "b")
            c.put(x + 1, y, "d")
    c.box(0, 6, 7, 10, "s", "k")
    c.hline(1, 6, 7, "t")
    c.box(6, 3, 11, 8, "S", "k")
    c.box(10, 7, 15, 11, "a", "k")
    c.hline(11, 14, 8, "s")
    c.hline(1, 14, 31, "k")
    return c


stamp("mattocks", 1, 2, art=[("clay", _mattocks())], note="mattocks and a sledgehammer, handles worn pale")


def _sledge():
    """2x2: the stone-sledge on its runners, loaded with stones the falls
    brought down. Rock palette throughout: the runners and deck are its log
    browns, the stones its black and grey."""
    c = Canvas(32, 32)
    # runners, curling up at the front (top)
    for x0 in (3, 25):
        c.box(x0, 4, x0 + 3, 30, "E")
        c.vline(x0 + 1, 5, 29, "h")
        c.put(x0, 3, "k")
        c.put(x0 + 1, 2, "k")
        c.put(x0 + 2, 2, "k")
        c.put(x0 + 1, 3, "h")
        c.put(x0 + 2, 3, "E")
    # the deck
    c.box(2, 12, 29, 27, "E")
    for y in (13, 17, 21, 25):
        c.hline(3, 28, y, "h")
    c.hline(3, 28, 26, "e")
    # the load
    for (cx, cy, rx, ry, tone) in [(9, 17, 5, 4, "2"), (20, 15, 6, 4.5, "6"), (14, 22, 5.5, 4, "7"),
                                   (24, 22, 4, 3.5, "2"), (7, 24, 3.5, 3, "6")]:
        c.ellipse(cx, cy, rx, ry, tone, "k")
        lit = {"2": "3", "6": "7", "7": "8"}[tone]
        c.hline(int(cx - rx / 2), int(cx + rx / 3), int(cy - ry + 1.5), lit)
    # the tow rope
    for x in range(8, 24):
        c.put(x, 5 + abs(x - 16) // 4, "h")
    return c


stamp("sledge", 2, 2, art=[("rock", _sledge())],
      note="the stone-sledge on its runners, loaded with stones the falls brought down")


def _rubble():
    """1x1: a heap of cleared stones by the lean-to wall."""
    c = Canvas(16, 16)
    for (cx, cy, rx, ry, tone) in [(5, 11, 4.5, 3.5, "6"), (11, 12, 4, 3, "2"), (8, 7, 4, 3.5, "7"),
                                   (3, 14, 2.5, 1.5, "2"), (13, 8, 2.5, 2, "6")]:
        c.ellipse(cx, cy, rx, ry, tone, "k")
        lit = {"2": "3", "6": "7", "7": "8"}[tone]
        c.hline(int(cx - rx / 2), int(cx + rx / 3), int(cy - ry + 1.5), lit)
    return c


stamp("rubble", 1, 1, art=[("rock", _rubble())], note="a heap of stones off the terrace, cleared one by one")


def _cirque_model():
    """2x2: a trestle table and on it Kepheus's clay model of the cirque: a
    horseshoe of black cliff, the falls a dribble from a jug he tops up, the
    pool a dish that never quite fills. All clay palette."""
    c = Canvas(32, 32)
    # the table
    c.box(0, 10, 31, 27, "b")
    c.hline(1, 30, 11, "n")
    c.box(0, 27, 31, 29, "d")
    for x in (2, 3, 28, 29):
        c.vline(x, 29, 31, "k")
    # the horseshoe ridge, open to the bottom (north is up)
    for y in range(6, 24):
        for x in range(3, 29):
            r = ((x - 15.5) / 12.5) ** 2 + ((y - 15) / 9.0) ** 2
            ri = ((x - 15.5) / 7.5) ** 2 + ((y - 16) / 5.5) ** 2
            if r <= 1.0 and (ri > 1.0) and y < 22:
                c.put(x, y, "a" if r > 0.8 or y > 14 else "s")
    for x in range(5, 27):
        if c.get(x, 7) in "as":
            c.put(x, 7, "S")
    # the dish in the hollow
    c.ellipse(15.5, 18, 5.5, 3, "t", "k")
    c.ellipse(15.5, 18.5, 4, 1.8, "a")
    c.put(14, 18, "c")
    # the jug on the ridge's top, and its dribble
    c.paste(12, 0, """
..kkkk..
.kmllmk.
kmmllmmk
kmmmmmmk
.kmmmmk.
..kddk..
""")
    for y in range(6, 17):
        c.put(16 + (1 if y > 11 else 0), y, "c" if y % 3 else "t")
    return c


stamp("cirque_model", 2, 2, art=[("clay", _cirque_model())],
      note="a clay model of the cirque on a trestle: the falls a dribble from a jug, the pool a dish")


def _holed_stone():
    """1x1 on the wall: a smooth black stone with a hole worn through it, hung
    by a cord from the slab ceiling. The hole shows the whitewash behind."""
    c = Canvas(16, 16)
    c.vline(8, 0, 4, "h")
    c.put(7, 1, "E")
    c.ellipse(8, 9.5, 5.5, 5, "2", "k")
    c.ellipse(8.5, 9.5, 2, 2, ".")
    for (x, y) in [(5, 7), (6, 6), (7, 6)]:
        c.put(x, y, "4")
    c.put(5, 8, "3")
    c.put(11, 12, "1")
    c.put(10, 13, "1")
    c.put(8, 5, "k")
    return c


stamp("holed_stone", 1, 1, art=[("rock", _holed_stone())],
      note="a smooth black stone with a hole worn through it, hanging from the ceiling")


def _post():
    """1x2: a timber post holding up the lean-to's roof; its upper cell is on
    the top layer."""
    mid, top = Canvas(16, 32), Canvas(16, 32)
    for y in range(0, 31):
        tgt = top if y < 16 else mid
        for (x, col) in ((5, "k"), (6, "h"), (7, "l"), (8, "m"), (9, "m"), (10, "k")):
            tgt.put(x, y, col)
        if y % 7 == 3:
            tgt.put(8, y, "d")
    mid.hline(4, 11, 30, "k")
    mid.hline(4, 11, 31, "d")
    for x in range(5, 11):
        top.put(x, 0, "k")
        top.put(x, 1, "d")
    return mid, top


_m, _t = _post()
stamp("lean_post", 1, 2, art=[("wood", _m)], top=[("wood", _t)], walk={(0, 0)},
      note="a timber post holding up the lean-to's roof")
