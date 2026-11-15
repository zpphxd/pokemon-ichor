#!/usr/bin/env python3
"""per's room-specific furniture: Daphne's field station, the egg-ovens, the
incense merchant's, the potter's, the net-loft, and Memphis's market, Apis
stable, scribe's house and embalmer's. Imported by per_pieces.py."""
import per_art as P
from per_art import Canvas, stamp
from per_pieces import _basket, _goods_bread, wall

# ===========================================================================
# Daphne's field station
# ===========================================================================


def _crate(open_=True):
    """A wooden crate (1x1); open, it shows fossils bedded in straw: a coiled
    shell, a domed shell and a lump of amber."""
    c = Canvas(16, 16)
    if open_:
        c.box(1, 3, 14, 4, "v")
        for x in range(2, 14):
            c.put(x, 4, "v" if x % 3 else "W")
            c.put(x, 5, "W" if x % 2 else "v")
        c.paste([".kkk.", "kLpLk", "kpDpk", "kLpPk", ".kkk."], 2, 1)     # coiled shell
        c.paste(["..kkk..", ".kLPLk.", "kLDLDLk", "kkkkkkk"], 7, 2)        # domed shell
        c.paste(["kk..", "kUuk", "kutk", ".kk."], 11, 2)                 # amber
    c.box(1, 6, 14, 10, "W")
    for y in (7, 10, 13):
        c.hline(2, 13, y, "v")
    for y in (9, 12):
        c.hline(2, 13, y, "w")
    c.vline(2, 7, 14, "d")
    c.vline(13, 7, 14, "d")
    c.hline(1, 14, 15, "k")
    return c


stamp("crate_fossils", "wood", _crate(True), 1, 1,
      note="an open crate of fossils bedded in straw: a coiled shell, a dome, amber")
stamp("crate_shut", "wood", _crate(False), 1, 1, note="a shut packing crate")


def _crate_stack():
    c = Canvas(16, 32)
    shut = _crate(False).text().split("\n")
    c.paste(shut, 0, 6)
    c.paste(shut, 0, 16)
    c.paste(["kk...", "kPk..", ".kPk.", "..kPk", "...kP"], 9, 7)    # a rope over the top crate
    for (x, y) in ((4, 9), (5, 9), (6, 9), (4, 10), (6, 10), (5, 11)):
        c.put(x, y, "T")                                       # a painted delta
    return c


stamp("crate_stack", "wood", _crate_stack(), 1, 2, note="two packing crates, roped, marked with a delta")


def _silt_trough():
    """The revival trough (2x1): a wooden trough of black Nile mud, warm from
    two lamps, a coiled fossil half out of the silt."""
    c = Canvas(32, 16)
    c.box(1, 3, 30, 11, "W")
    c.hline(2, 29, 4, "v")
    for y in range(5, 11):
        for x in range(3, 29):
            c.put(x, y, "D" if (x * 5 + y * 3) % 7 else "d")
    c.hline(3, 28, 5, "d")
    c.paste([".kkkk.", "kLpPLk", "kpkkpk", "kLpDLk", "kpLLpk"], 13, 4)     # the fossil rising
    c.hline(1, 30, 13, "k")
    c.hline(2, 29, 12, "w")
    for x in (3, 27):
        c.paste(["kwk", "kdk", "kkk"], x - 1, 13)
    for x in (0, 28):                                                      # lamps at the ends
        c.paste(["..u.", ".uUu", "kkkk", "kTtk"], x, 0)
    return c


stamp("silt_trough", "wood", _silt_trough(), 2, 1,
      note="Daphne's revival trough: black Nile silt, kept warm, a fossil half out of it")


def _desk_notes():
    """A work table (2x1) heaped with papyrus notes, a pot of reed brushes and
    a bone she is drawing."""
    c = Canvas(32, 16)
    c.box(0, 4, 32, 4, "v")
    c.hline(1, 30, 5, "W")
    c.hline(1, 30, 6, "w")
    for x in (2, 28):
        c.paste(["kwk", "kwk", "kwk", "kdk", "kdk", "kkk"], x - 1, 8)
    c.paste(["kkkkkkkkk",
             "kQQQQQQQk",
             "kQkkQkQQk",
             "kPQQQQQPk",
             "kkkkkkkkk"], 3, 0)
    c.paste(["kkkkkkk", "kPLLPPk", "kLkkLLk", "kkkkkkk"], 9, 2)
    c.paste(["..k.k.", ".kwkdk", "kkkkkk", "kTttTk", "kTttTk", ".kkkk."], 19, 0)
    c.paste(["kk...kk", "kPkkkPk", ".kPPPk.", "kPkkkPk", "kk...kk"], 24, 1)
    return c


stamp("desk_notes", "wood", _desk_notes(), 2, 1,
      note="a work table: field notes on papyrus, reed brushes, a bone being drawn")


def _cot():
    """A camp cot (2x1) with a striped blanket and a satchel at its foot."""
    c = Canvas(32, 16)
    c.box(1, 4, 28, 7, "P")
    for x in range(2, 28):
        for y in range(5, 10):
            c.put(x, y, "Q" if x < 9 else ("t" if (x // 2) % 2 else "u"))
    c.hline(2, 27, 10, "w")
    c.paste(["kkkkk", "kQQQk", "kPPPk", "kkkkk"], 3, 2)
    for x in (2, 26):
        c.paste(["kdk", "kdk", "kkk"], x, 11)
    c.paste([".kkkk.", "kWwwWk", "kwWWwk", "kWWwdk", ".kkkk."], 26, 7)
    return c


stamp("cot", "wood", _cot(), 2, 1, note="Daphne's camp cot, a striped blanket and her satchel")


def _chart():
    """Daphne's chart of the Oikoumene on papyrus, pinned to the wall (2x2):
    the river Okeanos round the rim, the inner sea, the Nile's long line
    south, and her route inked in red."""
    c = Canvas(32, 32)
    c.rect(4, 9, 24, 15, "P")
    c.ellipse(16, 16.5, 11.5, 7.5, "p")       # Okeanos round the rim
    c.ellipse(16, 16.5, 10.5, 6.5, "P")
    c.ellipse(13, 14.5, 6, 2.5, "L")          # the inner sea
    c.paste(["d", "d", ".d", ".d", "..d", "..d"], 14, 17)    # the Nile, south
    for (x, y) in [(7, 13), (8, 12), (9, 12), (10, 13), (11, 15), (12, 16), (14, 17)]:
        c.put(x, y, "t")                        # her route, in red
    for (x, y) in [(4, 9), (27, 9), (4, 23), (27, 23)]:
        c.put(x, y, "T")
    c.outline("k")
    return c


stamp("chart", "wood", _chart(), 2, 2, note="Daphne's chart of the Oikoumene, her route inked in red")

stamp("dig_tools", "wood", P.civic_piece("dig_tools", "wood"), 1, 1,
      note="a pick and a brush, laid down for the day (civic's)")

# ===========================================================================
# The egg-ovens
# ===========================================================================


def _bricks(c, x0, x1, y0, y1, shape=None):
    """Lay fired-clay courses (fire palette) over a region; shape(y) gives the
    half-width at a row, centred on (x0 + x1) / 2."""
    cx = (x0 + x1) / 2.0
    for y in range(y0, y1):
        half = shape(y) if shape else (x1 - x0) / 2.0
        left, right = int(round(cx - half)), int(round(cx + half))
        for x in range(left, right):
            # 8-pixel bricks, 4 rows to a course, half-bond: the pattern
            # repeats every 8 pixels, so the wall's middle shares its tiles
            course = (y // 4) % 2
            joint = (y % 4 == 3) or ((x + course * 4) % 8 == 7)
            edge = x - left < 2 or right - x <= 2
            c.put(x, y, "d" if joint else ("d" if edge and x - left >= 2 else "l" if edge or y % 4 == 0 else "m"))


def _egg_oven():
    """An egg-oven (2x2), as Diodorus describes them: a vaulted mud-brick
    chamber; its arched mouth shows eggs on straw, and above it the
    fire-trough's slot glows."""
    c = Canvas(32, 32)
    _bricks(c, 2, 30, 2, 30, lambda y: 14 * (1 - ((10 - y) / 9.0) ** 2) ** 0.5 if y < 10 else 14)
    c.box(9, 9, 14, 5, "a")
    for x in range(10, 22):
        c.put(x, 10, "F" if x % 3 else "Y")
        c.put(x, 11, "f" if x % 2 else "F")
        c.put(x, 12, "a" if x % 4 else "f")
    for y in range(16, 30):
        half = 8 if y > 19 else int(round(8 * (1 - ((19 - y) / 4.0) ** 2) ** 0.5))
        for x in range(16 - half, 16 + half):
            c.put(x, y, "a" if y < 21 else "A")
    for (x, y) in [(10, 24), (13, 23), (16, 24), (19, 23), (12, 26), (15, 26), (18, 26), (21, 25)]:
        c.paste(["ee", "eE"], x, y)
    for x in range(8, 24):
        c.put(x, 28, "h" if x % 2 else "l")
        c.put(x, 29, "l")
    c.outline("k")
    return c


stamp("egg_oven", "fire", _egg_oven(), 2, 2,
      note="an egg-oven of mud brick: eggs on straw below, the fire-trough's slot above")


def _fire_trough():
    """A trough sunk in the floor (1x1), smouldering dung-cake fuel."""
    c = Canvas(16, 16)
    c.box(1, 3, 14, 11, "A")
    for y in range(5, 12):
        for x in range(3, 13):
            k = (x * 7 + y * 5) % 9
            c.put(x, y, "f" if k == 0 else "F" if k == 1 else "a" if k < 5 else "A")
    c.paste(["Y", "F"], 7, 6)
    c.paste(["s.s", ".s."], 4, 0)
    c.hline(2, 13, 4, "a")
    return c


stamp("fire_trough", "fire", _fire_trough(), 1, 1, note="a fire-trough sunk in the floor, smouldering")


def _fuel():
    """Dried dung cakes stacked for fuel (1x1) on a bed of straw."""
    c = Canvas(16, 16)
    for (x, y) in ((1, 9), (6, 9), (11, 9), (3, 5), (8, 5), (5, 1)):
        c.paste([".kkk.", "kmlmk", "kdmdk", ".kkk."], x, y)
    c.hline(1, 15, 13, "h")
    c.hline(2, 14, 14, "l")
    return c


stamp("fuel", "fire", _fuel(), 1, 1, note="dung cakes stacked for the ovens' fires")

# ===========================================================================
# The incense merchant
# ===========================================================================


def _censer():
    """A tall bronze censer on a tripod stand (1x2), coals glowing, smoke
    curling up on the top layer."""
    c = Canvas(16, 32)
    c.paste(["..kkkkkkkkkk..",
             ".kbbbbbbbbbbzk.",
             ".kFfYFfFYfFfzk.",
             "..kbbbbbbbbzk..",
             "...kbbbbbbzk...",
             "....kkbbzkk....",
             "......kbk......",
             "......kbk......",
             "......kbk......",
             "......kzk......",
             "......kzk......",
             "......kzk......",
             ".....kbzzk.....",
             "....kb.k.zk....",
             "...kb..k..zk...",
             "..kk...k...kk.."], 1, 16)
    top = Canvas(16, 32)
    top.paste(["....s.....",
               "...s.s....",
               "....s..s..",
               ".....ss.s.",
               "......s...",
               ".....s.s..",
               "....s...s.",
               ".....s.s..",
               "......s...",
               ".....s....",
               "......s...",
               ".......s..",
               "......s..."], 3, 1)
    return c, top


_c, _t = _censer()
stamp("censer", "fire", _c, 1, 2, top=_t, note="a bronze censer on its tripod, smoke rising")


def _incense_table():
    """The merchant's low table (2x1): a balance and little heaps of resin.
    The player talks across it (MB_COUNTER)."""
    c = Canvas(32, 16)
    c.box(0, 5, 32, 6, "W")
    c.hline(1, 30, 6, "v")
    c.hline(1, 30, 9, "w")
    for x in (1, 28):
        c.paste(["kdk", "kdk", "kdk", "kkk"], x, 11)
    c.paste(["...vv...", "kkkWWkkk", "k..dw..k", "kk.dw.kk", ".k.dw.k.", "...dw..."], 2, 0)
    for (x, ch1, ch2) in ((13, "U", "u"), (19, "u", "t"), (25, "P", "L")):
        c.paste([".kk.", "k12k", "k221k"], x, 2, remap={"1": ch1, "2": ch2})
    return c


stamp("incense_table", "wood", _incense_table(), 2, 1,
      behavior={(0, 0): "MB_COUNTER", (1, 0): "MB_COUNTER"},
      note="the incense merchant's low table: a balance and heaps of resin")


def _shelf(shelves):
    """A four-shelf cabinet (2x2) standing against the wall. Each shelf holds
    one kind of thing, one to every 8 pixels, and the pieces are symmetric,
    so a shelf costs two tiles (its end is the other end flipped)."""
    c = Canvas(32, 32)
    c.vline(0, 0, 31, "k")
    c.vline(1, 0, 31, "w")
    c.vline(30, 0, 31, "w")
    c.vline(31, 0, 31, "k")
    for r, item in enumerate(shelves):
        y0 = r * 8
        c.rect(2, y0, 28, 7, "D")
        c.hline(1, 30, y0 + 7, "v")
        if item is None:
            continue
        w, h = len(item[0]), len(item)
        for col in range(4):
            c.paste(item, col * 8 + (8 - w) // 2, y0 + 7 - h)
    c.hline(0, 31, 0, "k")
    return c


ALABASTRON = [".kk.", "kQQk", "kPPk", "kPPk", "kLLk", ".kk."]
STOPPERED = [".kk.", "kddk", "kuuk", "kttk", ".kk."]
OIL_JAR = ["kkkk", "kTTk", "kuuk", "kttk", "kkkk"]
CHALICE = ["kkkkkk", "kQQQQk", "kTttTk", ".kQQk.", "..kk..", ".kPPk."]
SILT_POT = [".kkkk.", "kuUUuk", "kDDDDk", "kttttk", ".kkkk."]
GREENWARE = [".kkkk.", "kLPPLk", "kppppk", ".kkkk."]
SCROLLS = ["kkkkkk", "kPLLPk", "kkkkkk", "kPLLPk", "kkkkkk", "kQPPQk"]

stamp("jar_shelf", "wood", _shelf([STOPPERED, ALABASTRON, OIL_JAR, ALABASTRON]), 2, 2,
      note="shelves of stoppered jars and alabaster flasks of oil")

# ===========================================================================
# The potter
# ===========================================================================


def _wheel():
    """A potter's turntable (1x1), a pot rising wet on it."""
    c = Canvas(16, 16)
    c.ellipse(8, 11, 7, 3, "w")
    c.ellipse(8, 10.5, 6.5, 2.5, "W")
    c.paste(["..kkkk..", ".kuUutk.", ".kUuttk.", "..kutk..", ".kuUutk.", "kuUuuttk",
             "kUuutttk", ".kkkkkk."], 4, 2)
    c.paste(["kdk", "kdk", "kkk"], 6, 13)
    c.outline("k")
    return c


stamp("wheel", "wood", _wheel(), 1, 1, note="the potter's turntable, a wet pot on it")


def _kiln():
    """The potter's kiln (2x2): the egg-oven's mud-brick vault (so the two
    share their brickwork tiles), but a firing chamber: a vent smoking at
    the top, its fire-mouth roaring below, a stack of pots in the glow."""
    c = Canvas(32, 32)
    _bricks(c, 2, 30, 2, 30, lambda y: 14 * (1 - ((10 - y) / 9.0) ** 2) ** 0.5 if y < 10 else 14)
    c.box(11, 8, 10, 4, "a")
    c.hline(12, 19, 9, "A")
    c.paste(["s.s.", ".s.s"], 13, 6)
    for y in range(16, 30):
        half = 8 if y > 19 else int(round(8 * (1 - ((19 - y) / 4.0) ** 2) ** 0.5))
        for x in range(16 - half, 16 + half):
            c.put(x, y, "f" if (x + y) % 3 == 0 else "F" if (x + y) % 3 == 1 else "Y")
    c.paste([".kk..kk.", "kmlkkmlk", "kmmkkmmk", ".kk..kk."], 12, 19)    # pots in the glow
    for x in range(8, 24):
        c.put(x, 28, "a" if x % 2 else "A")
        c.put(x, 29, "a")
    c.outline("k")
    return c


stamp("kiln", "fire", _kiln(), 2, 2, note="the potter's kiln, its fire-mouth glowing")


stamp("pot_shelf", "wood", _shelf([CHALICE, SILT_POT, CHALICE, GREENWARE]), 2, 2,
      note="shelves of Naukratite pottery: white-slipped chalices with painted bands")


def _clay_tub():
    """A trough of wet clay (1x1) with a scraper in it."""
    c = Canvas(16, 16)
    c.box(1, 5, 14, 9, "W")
    for y in range(6, 12):
        c.hline(2, 13, y, "t" if y % 2 else "T")
    c.hline(2, 13, 6, "u")
    c.paste(["kk", "kvk", ".kvk", "..kk"], 9, 2)
    c.hline(1, 14, 13, "k")
    return c


stamp("clay_tub", "wood", _clay_tub(), 1, 1, note="a trough of wet Nile clay")


def _greenware():
    """Unfired pots drying on a plank (1x1), pale and dull."""
    c = Canvas(16, 16)
    for (x, y) in ((1, 4), (6, 5), (11, 4)):
        c.paste([".kkk.", "kLLpk", "kLppk", "kpppk", ".kkk."], x, y)
    c.box(0, 10, 16, 3, "w")
    c.hline(1, 14, 11, "v")
    return c


stamp("greenware", "wood", _greenware(), 1, 1, note="unfired pots drying on a plank")

# ===========================================================================
# The net-loft
# ===========================================================================


def _net_rack():
    """Nets drying over two poles (2x2), cork floats along the head-rope."""
    c = Canvas(32, 32)
    for x in (2, 28):
        c.vline(x, 2, 30, "K")
        c.vline(x + 1, 2, 30, "j")
    c.hline(2, 29, 3, "n")
    for y in range(4, 25):
        for x in range(4, 28):
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                c.put(x, y, "n")
    for x in range(5, 28, 4):
        c.paste(["kk", "jK"], x, 2)
    c.outline("k", inside="Kjs")
    return c


stamp("net_rack", "nature", _net_rack(), 2, 2, note="nets drying over two poles, cork floats on the head-rope")


def _ground_loom():
    """An Egyptian ground loom (2x2): two beams pegged to the floor, the warp
    stretched between, a length of linen woven at the near end."""
    c = Canvas(32, 32)
    for y in (3, 27):
        c.box(1, y, 30, 3, "W")
        c.hline(2, 29, y + 1, "v")
    for y in (2, 28):
        c.paste(["kk", "kd", ".k"], 0, y)
        c.paste(["kk", "dk", "k."], 30, y)
    for x in range(3, 29, 2):
        c.vline(x, 6, 26, "P")
    for y in range(18, 27):
        c.hline(3, 28, y, "Q" if y % 2 else "P")
    c.box(2, 15, 28, 3, "w")
    c.hline(3, 28, 16, "W")
    return c


stamp("ground_loom", "wood", _ground_loom(), 2, 2,
      note="a ground loom pegged to the floor, a length of linen half woven")


def _flax():
    """Sheaves of retted flax (1x1), leaning, a few blue flowers left."""
    c = Canvas(16, 16)
    for (x, y) in ((2, 1), (7, 2), (11, 1)):
        for i in range(3):
            c.vline(x + i, y + 2, 14, "J" if i == 0 else "j" if i == 1 else "K")
        c.paste(["l.l", ".y."], x, y)
        c.hline(x, x + 2, 9, "n")
    c.outline("k")
    return c


stamp("flax", "nature", _flax(), 1, 1, note="sheaves of flax for linen")

stamp("spindles", "nature", _basket("n", ["....k.......",
                                          "...knk..k...",
                                          "...knk.knk..",
                                          "..kkkkkknkk.",
                                          ".knnnkknnnnk",
                                          "knnwnnkwnnnk",
                                          "kkkkkkkkkkkk"]), 1, 1,
      note="a basket of spindles and linen thread")


def _skiff():
    """A papyrus skiff (2x1): bundled stems, bound, both ends curling up."""
    c = Canvas(32, 16)
    for x in range(1, 31):
        t = abs(x - 15.5) / 15.0
        y0 = 6 - int(5 * t ** 3)
        y1 = 12 - int(3 * t ** 2)
        for y in range(y0, y1):
            c.put(x, y, "J" if y == y0 else "j" if y < y1 - 2 else "K")
    for x in (6, 11, 20, 25):
        c.vline(x, 3, 12, "n")
    c.outline("k")
    return c


stamp("skiff", "nature", _skiff(), 2, 1, note="a papyrus skiff, bound in five places, ends curled up")

# ===========================================================================
# Memphis: the market
# ===========================================================================


def _bread_basket():
    c = Canvas(16, 16)
    c.paste(_goods_bread().text().split("\n")[:10], 0, 0)
    c.paste(["kkkkkkkkkkkkkk",
             "kWvWvWvWvWvWvk",
             "kvWvWvWvWvWvwk",
             ".kWvWvWvWvWwk.",
             "..kwwwwwwwwk..",
             "...kkkkkkkk..."], 1, 9)
    return c


stamp("basket_bread", "wood", _bread_basket(), 1, 1, note="a basket of conical loaves and a jug of beer")


def _onions():
    """Strings of onions and garlic hung on the wall (1x2)."""
    c = Canvas(16, 32)
    for x in (4, 11):
        c.vline(x, 8, 26, "n")
        for y in range(10, 26, 4):
            if x == 4:
                c.paste([".kk.", "krJk", "kJrk", ".kk."], x - 2, y)
            else:
                c.paste([".kk.", "kwnk", "knwk", ".kk."], x - 2, y)
    c.paste(["kkkkkkkkkkkk"], 2, 7)
    return c


stamp("onions", "nature", _onions(), 1, 2, note="strings of onions and garlic, hung up to dry")


def _linen_bolts():
    """Bolts of linen stacked on a stand (1x1), the finest on top."""
    c = Canvas(16, 16)
    for (y, a, b) in ((10, "P", "L"), (6, "Q", "P"), (2, "Q", "Q")):
        c.paste(["kkkkkkkkkkkk",
                 "k" + a * 9 + "bk",
                 "k" + a * 9 + "bk",
                 "kkkkkkkkkkkk"], 2, y, remap={"b": b})
    c.paste(["kk", "kt", "kt"], 12, 3)
    c.hline(1, 14, 14, "w")
    c.hline(1, 14, 15, "k")
    return c


stamp("linen_bolts", "wood", _linen_bolts(), 1, 1, note="bolts of linen, the finest on top")


def _amulets():
    """A tray of faience amulets (1x1): scarabs, eyes and little gods."""
    c = Canvas(16, 16)
    c.box(1, 5, 14, 9, "O")
    c.box(2, 6, 12, 7, "o")
    for (x, y) in ((3, 7), (7, 7), (11, 7), (5, 10), (9, 10)):
        c.paste(["kck", "cCc", "kck"], x - 1, y - 1)
    c.hline(1, 14, 13, "k")
    return c


stamp("amulets", "paint", _amulets(), 1, 1, note="a tray of faience amulets: scarabs and eyes of Horus")

# ===========================================================================
# Memphis: the Apis stable
# ===========================================================================


def _stall_wall():
    """A stall's partition (1x2): a low mud-brick wall running out from the
    back wall, plastered on top, its brick end toward the room."""
    c = Canvas(16, 32)
    c.box(3, 0, 10, 32, "N")
    for y in range(1, 22):
        c.hline(4, 11, y, "N")
        c.put(4, y, "w")
        c.put(5, y, "p")
        c.put(10, y, "n")
        c.put(11, y, "m")
    c.hline(4, 11, 22, "n")
    for y in range(23, 31):                       # the brick end
        r = (y - 23) % 4
        for x in range(4, 12):
            joint = r == 3 or (x + (4 if (y - 23) // 4 else 0)) % 8 == 7
            c.put(x, y, "M" if joint else "n" if r == 0 else "m")
    c.paste(["kk", "3k", "2k", "kk"], 7, 3)      # a tethering peg
    return c


stamp("stall_wall", "mud", _stall_wall(), 1, 2, note="a stall's low partition of whitewashed mud brick")


def _manger():
    """A limestone manger (1x1) heaped with fodder."""
    c = Canvas(16, 16)
    c.box(1, 6, 14, 9, "6")
    c.hline(2, 13, 7, "8")
    c.hline(2, 13, 13, "4")
    for y in range(3, 8):
        for x in range(3, 13):
            if abs(x - 8) + (7 - y) * 2 < 8:
                c.put(x, y, "g" if (x + y) % 3 else "G")
    c.outline("k", inside="gG")
    return c


stamp("manger", "stone", _manger(), 1, 1, note="a limestone manger heaped with fodder")


def _water_trough():
    c = Canvas(32, 16)
    c.box(1, 3, 30, 11, "6")
    c.hline(2, 29, 4, "8")
    c.box(3, 5, 26, 5, "B")
    for x in range(4, 28):
        c.put(x, 6, "b")
        c.put(x, 7, "b" if x % 5 else "7")
        c.put(x, 8, "b")
    c.hline(2, 29, 11, "5")
    c.hline(2, 29, 12, "4")
    return c


stamp("water_trough", "stone", _water_trough(), 2, 1, note="a long limestone water trough")


def _hay():
    c = Canvas(16, 16)
    for y in range(3, 15):
        half = min(7, 2 + (y - 3))
        for x in range(8 - half, 8 + half):
            c.put(x, y, "y" if (x * 3 + y) % 5 == 0 else "J" if (x + y) % 3 else "j")
    c.hline(1, 14, 14, "K")
    c.outline("k")
    return c


stamp("hay", "nature", _hay(), 1, 1, note="a heap of hay")


def _window_apis():
    """The window of appearances (2x2): a stone frame under a cavetto
    cornice and a row of gilded cobras, where the Apis is shown to the
    people."""
    c = Canvas(32, 32)
    c.box(2, 6, 28, 24, "6")
    for x in range(3, 29):
        c.put(x, 7, "b" if x % 4 < 2 else "t")
        c.put(x, 8, "b" if x % 4 < 2 else "t")
        c.put(x, 9, "G")
    for x in range(5, 28, 4):
        c.paste([".g", "gG", "kg"], x, 10)
    c.box(7, 14, 18, 14, "1")
    for y in range(15, 27):
        c.hline(8, 23, y, "2" if y > 20 else "1")
    c.hline(5, 26, 28, "8")
    c.hline(5, 26, 29, "4")
    c.outline("k")
    return c


stamp("window_apis", "stone", _window_apis(), 2, 2,
      note="the window of appearances, under a cornice of gilded cobras")

# ===========================================================================
# Memphis: the scribe of Thoth
# ===========================================================================


SCROLLS_B = ["kkkkkk", "kQPPQk", "kkkkkk", "kPLLPk", "kkkkkk", "kPLLPk"]
stamp("niches", "wood", _shelf([SCROLLS, SCROLLS_B, SCROLLS, SCROLLS_B]), 2, 2,
      note="the scribe's niches: papyrus rolls stacked end-on")


def _scribe_desk():
    """A low writing table (2x1): an unrolled papyrus, the scribe's palette
    with its red and black cakes of ink, reed pens and a water pot."""
    c = Canvas(32, 16)
    c.box(0, 5, 32, 5, "v")
    c.hline(1, 30, 6, "W")
    c.hline(1, 30, 8, "w")
    for x in (2, 28):
        c.paste(["kwk", "kwk", "kdk", "kkk"], x - 1, 10)
    c.paste(["kkkkkkkkkkkk",
             "kQQQQQQQQQQk",
             "kQkQkkQkQkQk",
             "kPQQQQQQQQPk",
             "kkkkkkkkkkkk"], 2, 2)
    c.paste(["kkkkkkkkkk",
             "kWDkTkWWWk",
             "kkkkkkkkkk"], 15, 3)
    c.paste(["....kk", "...kk.", "..kk.."], 18, 0)
    c.paste([".kk.", "kuUk", "kttk", ".kk."], 26, 2)
    return c


stamp("scribe_desk", "wood", _scribe_desk(), 2, 1,
      note="a low writing table: a papyrus, the palette's red and black inks, a water pot")


def _ibis():
    """Thoth as an ibis (1x2) on a gilt-edged pedestal: white body, black
    head, neck and tail, the long curved beak."""
    c = Canvas(16, 32)
    c.paste(["..........",
             "...kk.....",
             "..k11k....",
             "..k1k1k...",
             "...k..1k..",
             ".......1k.",
             "........1k",
             "...kkk..k.",
             "..k1k.....",
             "..k1k.....",
             ".k771k....",
             "k77777kk..",
             "k788777kk.",
             "k7777771k.",
             ".k777771k.",
             "..k7771k..",
             "...k1k....",
             "...k1k....",
             "...k1k....",
             "..kkkkk..."], 3, 1)
    c.box(1, 21, 14, 10, "G")
    c.box(2, 22, 12, 8, "6")
    c.hline(3, 12, 23, "7")
    c.hline(1, 14, 30, "4")
    c.hline(1, 14, 31, "k")
    return c


stamp("ibis", "stone", _ibis(), 1, 2, note="Thoth as an ibis on a gilt-edged pedestal")


def _baboon():
    """Thoth's baboon (1x1), seated, the moon's disc on its head."""
    c = Canvas(16, 16)
    c.paste(["....kgk.....",
             "...kgggk....",
             "..kk3k3kk...",
             "..k34443k...",
             "..k3k4k3k...",
             "..k33333k...",
             ".k3333333k..",
             "k333333332k.",
             "k3322223322k",
             "k332kk23322k",
             ".kkkkkkkkkk.",
             ".k44444444k.",
             ".kkkkkkkkkk."], 2, 2)
    return c


stamp("baboon", "stone", _baboon(), 1, 1, note="Thoth's baboon, seated, the moon's disc on its head")


def _glyphs():
    """A painted panel of hieroglyphs on the wall (2x2), the scribe's riddles:
    an owl, water, a mouth, an eye, a sun, a basket, an ibis."""
    # The panel's edges are symmetric and its glyphs sit one to an 8x8
    # tile, two columns of three: owl, water, mouth; eye, sun, basket.
    c = Canvas(32, 32)
    c.box(3, 2, 26, 29, "w")
    c.hline(4, 27, 3, "b")
    c.hline(4, 27, 29, "b")
    c.vline(4, 4, 28, "o")
    c.vline(27, 4, 28, "o")
    glyphs = {
        (1, 1): ["..nn....", ".nnnn...", ".nwnw...", "..nnn...", "..nnnn..", "...nnn..", "...k.k.."],   # owl: m
        (1, 2): ["........", "b.b.b.b.", ".b.b.b.b", "........", "b.b.b.b.", ".b.b.b.b", "........"],  # water: n
        (1, 3): ["........", ".rrrrrr.", "rr....rr", ".rrrrrr."],                                       # mouth: r
        (2, 1): ["........", ".nnnnn..", "nwwnwwn.", ".nnnnn..", "...n.n..", "...n..n."],                # eye
        (2, 2): ["...rr...", "..rrrr..", ".rrorrr.", "..rrrr..", "...rr..."],                           # sun
        (2, 3): ["........", "nnnnnnn.", ".bbbbb..", "..bbb..."],                                       # basket
    }
    for (col, row), art in glyphs.items():
        c.paste(art, col * 8, row * 8)
    return c


stamp("glyphs", "paint", _glyphs(), 2, 2, note="a painted panel of hieroglyphs: the scribe's riddles")

# ===========================================================================
# Memphis: the embalmer
# ===========================================================================


def _natron_table(bundle=True):
    """An embalming bed of grey stone (2x1), lion-headed at one end, with a
    channel along its edge; on it, a linen-wrapped bundle."""
    c = Canvas(32, 16)
    c.box(1, 5, 28, 7, "4")
    c.hline(2, 27, 6, "5")
    c.hline(2, 27, 9, "3")
    c.hline(2, 27, 10, "2")
    c.paste(["kkk..", "k3kk.", "k333k", "k3k3k", "k333k", ".k32k"], 26, 2)    # the lion's head
    for x in (3, 23):
        c.paste(["k3k", "k2k", "k33k", "kkkk"], x, 12)
    if bundle:
        c.paste([".kkkkkkkkkkkkkkk.",
                 "k78787878787878kk",
                 "k87878787878787k6k",
                 ".kkkkkkkkkkkkkkkk"], 5, 2)
    return c


stamp("natron_table", "stone", _natron_table(True), 2, 1,
      note="an embalming bed of stone, lion-headed, a linen-wrapped bundle on it")


def _natron():
    """A heap of natron (1x1), the drying salt, on a reed tray."""
    c = Canvas(16, 16)
    for y in range(3, 13):
        half = min(7, 1 + (y - 3))
        for x in range(8 - half, 8 + half):
            c.put(x, y, "8" if (x + 2 * y) % 5 == 0 else "7" if x < 8 else "6")
    c.box(0, 12, 16, 3, "G")
    c.hline(1, 14, 13, "g")
    c.outline("k", inside="876")
    return c


stamp("natron", "stone", _natron(), 1, 1, note="a heap of natron, the drying salt, on a reed tray")


def _canopic():
    """Four canopic jars (1x1) of alabaster, their lids the four sons of
    Horus: a man, a baboon, a jackal and a falcon."""
    c = Canvas(16, 16)
    lids = [["kgk", "kgk"], ["k3k", "k3k"], ["k1k", "1k1"], ["kbk", "kBk"]]
    for i, (x, y) in enumerate(((1, 2), (8, 2), (1, 9), (8, 9))):
        c.paste([".kkk.", ".k1k.", "kkkkk", "k776k", "k776k", "k765k", ".kkk."], x + 1, y - 1)
        c.paste(lids[i], x + 2, y - 1)
    return c


stamp("canopic", "stone", _canopic(), 1, 1, note="four canopic jars, lidded with the four sons of Horus")


def _anubis():
    """The jackal mask on its stand (1x2): black, gold-collared, ears up."""
    c = Canvas(16, 32)
    c.paste([".k...k.....",
             "k1k.k1k....",
             "k11k11k....",
             "k1111111k..",
             "k1g11111k..",
             ".k11111111k",
             ".k1111111kk",
             "..k11111k..",
             "..kgggggk..",
             ".kGgGgGgGk.",
             ".kgggggggk.",
             "..kkkkkkk..",
             "....k3k....",
             "....k3k....",
             "....k3k....",
             "....k3k....",
             "....k3k....",
             "....k2k....",
             "...k333k...",
             "..k33332k..",
             "..kkkkkkk.."], 2, 9)
    return c


stamp("anubis", "stone", _anubis(), 1, 2, note="the jackal mask of Anubis on its stand")


def _resin_pot():
    """A pot of resin warming over coals (1x1)."""
    c = Canvas(16, 16)
    c.paste(["..kkkkkkkk..",
             ".kaaaaaaaak.",
             ".kmlllllmdk.",
             ".kmlhllmmdk.",
             "..kmmmmmdk..",
             "...kkkkkk..."], 2, 2)
    c.paste(["s..s", ".s.."], 5, 0)
    c.box(1, 9, 14, 5, "a")
    for x in range(2, 14):
        c.put(x, 10, "f" if x % 3 else "F")
        c.put(x, 11, "F" if x % 2 else "Y")
    c.hline(1, 14, 13, "k")
    return c


stamp("resin_pot", "fire", _resin_pot(), 1, 1, note="a pot of resin warming over coals")

stamp("linen_rolls", "nature", _basket("n", ["............",
                                             "..kkkk......",
                                             ".knwwnk.kk..",
                                             "knwkkwnkwnk.",
                                             "knwkkwnknwnk",
                                             ".knwwnkknwk.",
                                             "kkkkkkkkkkkk"]), 1, 1,
      note="a basket of linen bandage rolls")

wall("chart", "glyphs", "onions", "window_apis")
