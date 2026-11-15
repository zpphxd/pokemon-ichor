#!/usr/bin/env python3
"""per's furniture: the stamps every Egyptian room is dressed from.

Imported by per_art.py, which defines the palettes, the Canvas and stamp().
Each piece is drawn in one palette (so each 8x8 tile fits it), light from the
top left, with an ink outline. Wall pieces carry `wall` for the catalog.
"""
import numpy as np

import per_art as P
from per_art import Canvas, stamp

M_SOUTH = "MB_SOUTH_ARROW_WARP"


def wall(*names):
    for n in names:
        P.STAMPS[n]["wall"] = True


def nocat(*names):
    for n in names:
        P.STAMPS[n]["nocat"] = True


def cells(img, cx, cy, w=1, h=1):
    return img[cy * 16:(cy + h) * 16, cx * 16:(cx + w) * 16]


def blank(w, h):
    return np.zeros((h * 16, w * 16, 4), np.uint8)


def place(dst, src, x, y):
    """Copy src's opaque pixels into dst at (x, y), in place."""
    h, w = src.shape[:2]
    reg = dst[y:y + h, x:x + w]
    m = src[..., 3] > 0
    reg[m] = src[m]
    return dst


# ===========================================================================
# Shared: the door mat, the two counters, the Pithos
# ===========================================================================

def _mat():
    c = Canvas(32, 16)
    c.box(2, 3, 28, 10, "j")
    for y in range(4, 12):
        for x in range(3, 29):
            # papyrus stems laid crosswise, bound in three places
            ch = "J" if y % 2 == 0 else "j"
            if x in (8, 15, 16, 23):
                ch = "K"
            c.put(x, y, ch)
    c.hline(3, 28, 11, "K")
    return c


stamp("mat", "nature", _mat(), 2, 1, walk={(0, 0), (1, 0)},
      behavior={(0, 0): M_SOUTH, (1, 0): M_SOUTH},
      note="papyrus door mat; both cells are south-arrow warps")

# The healer's counter: civic's, pixel for pixel, in 1x2 columns so a counter
# can be any length (left end, middle, the healer's place, right end).
_ASC_TOP = P.civic_piece("counter_asc_top", "stone")
_ASC_FRONT = P.civic_piece("counter_asc_front", "stone")
for i, part in enumerate("lmr"):
    img = blank(1, 2)
    place(img, cells(_ASC_TOP, i, 0), 0, 0)
    place(img, cells(_ASC_FRONT, i, 0), 0, 16)
    stamp(f"counter_heal_{part}", "stone", img, 1, 2, behavior={(0, 1): "MB_COUNTER"},
          note=f"the Asclepeion's counter ({['left end', 'middle', 'right end'][i]}): civic's, shared")
img = blank(1, 2)
place(img, cells(_ASC_FRONT, 1, 0), 0, 16)
top = blank(1, 2)
place(top, cells(_ASC_TOP, 1, 0), 0, 0)
stamp("counter_heal_staff", "stone", img, 1, 2, top=top, walk={(0, 0)},
      behavior={(0, 1): "MB_COUNTER"},
      note="the healer's place at the counter: the slab is on the top layer, over her")

# The Agora's stall counter: civic's, the same way.
_AGO_TOP = P.civic_piece("counter_ago_top", "wood")
_AGO_FRONT = P.civic_piece("counter_ago_front", "wood")
for i, part in enumerate("lmr"):
    img = blank(1, 2)
    place(img, cells(_AGO_TOP, i, 0), 0, 0)
    place(img, cells(_AGO_FRONT, i, 0), 0, 16)
    stamp(f"counter_stall_{part}", "wood", img, 1, 2, behavior={(0, 1): "MB_COUNTER"},
          note=f"the Agora's stall counter ({['left end', 'middle', 'right end'][i]}): civic's, shared")
img = blank(1, 2)
place(img, cells(_AGO_FRONT, 1, 0), 0, 16)
top = blank(1, 2)
place(top, cells(_AGO_TOP, 1, 0), 0, 0)
stamp("counter_stall_staff", "wood", img, 1, 2, top=top, walk={(0, 0)},
      behavior={(0, 1): "MB_COUNTER"},
      note="the stallkeeper's place: the slab is on the top layer, over them")


def _goods_bread():
    """Conical Egyptian loaves and a beer jug, laid on a counter's slab."""
    c = Canvas(16, 16)
    # three conical loaves
    for (x, h) in ((1, 6), (5, 7), (9, 5)):
        for j in range(h):
            half = j // 2
            c.hline(x + 1 - half // 2, x + 1 + half // 2 + (1 if j > 2 else 0), 8 - h + j, "W" if j < h - 1 else "w")
        c.put(x + 1, 8 - h, "v")
    # a jug at the right
    c.paste(["..kk.",
             ".kUuk",
             "kUutk",
             "kutTk",
             ".kTk.",
             "..k.."], 11, 2)
    c.outline("k", inside="Wwv")
    return c


def _goods_scale():
    """A wooden balance with a weight on one pan and a bundle on the other."""
    c = Canvas(16, 16)
    c.paste(["......vv......",
             ".kkkkkWWkkkkk.",
             ".k....dw....k.",
             ".k....dw....k.",
             "kWWk..dw..kWWk",
             ".kk...dw...kk.",
             ".....kddk.....",
             "....kkkkkk...."], 1, 0)
    c.paste(["kk", "Dk"], 2, 2)
    c.paste(["kQk", "kPk"], 11, 1)
    return c


def _with_goods(part, goods, gx, gy):
    img = P.STAMPS[f"counter_stall_{part}"]["img"].copy()
    g = P.grid("wood", goods.text(), 16, 16)
    place(img, g[:16 - gy, :16 - gx], gx, gy)
    return img


stamp("counter_stall_l_scale", "wood", _with_goods("l", _goods_scale(), 2, 0), 1, 2,
      behavior={(0, 1): "MB_COUNTER"}, note="the stall counter's left end, with a balance")
stamp("counter_stall_r_bread", "wood", _with_goods("r", _goods_bread(), 0, 1), 1, 2,
      behavior={(0, 1): "MB_COUNTER"}, note="the stall counter's right end, with loaves and a beer jug")
nocat("counter_heal_l", "counter_heal_m", "counter_heal_r", "counter_stall_l", "counter_stall_m",
      "counter_stall_r")


def _pithos():
    """The Pithos: a tall Egyptian storage jar in Nile-silt ware, with a white
    band and its conical mud stopper stamped with a seal. 2x2."""
    c = Canvas(32, 32)
    # stopper: a mud cone, its seal impression
    c.paste(["....kkkk....",
             "...kwWWwk...",
             "..kwWvvWwk..",
             ".kwWvLLvWwk.",
             ".kdwWLLWwdk.",
             "kkkkkkkkkkkk"], 10, 0)
    # neck and rim
    c.box(9, 6, 14, 3, "u")
    c.hline(10, 21, 7, "U")
    c.hline(10, 21, 8, "t")
    # body: an ovoid, widest at a third of its height
    for y in range(9, 31):
        t = (y - 9) / 21.0
        half = int(round(13 * (1 - (t - 0.3) ** 2 / 0.49) ** 0.5)) if t < 1 else 3
        half = max(half, 3)
        x0, x1 = 16 - half, 15 + half
        for x in range(x0, x1 + 1):
            f = (x - x0) / max(1, x1 - x0)
            ch = "U" if f < 0.18 else "u" if f < 0.45 else "t" if f < 0.8 else "T"
            c.put(x, y, ch)
        c.put(x0 - 1, y, "k")
        c.put(x1 + 1, y, "k")
    c.hline(13, 18, 31, "k")
    # the white band with a red zigzag, and a lower red line
    for x in range(3, 29):
        if c.get(x, 14) != ".":
            c.put(x, 13, "Q" if c.get(x, 13) not in "k." else c.get(x, 13))
            c.put(x, 14, "P" if c.get(x, 14) not in "k." else c.get(x, 14))
            c.put(x, 15, "Q" if c.get(x, 15) not in "k." else c.get(x, 15))
            zig = 13 + abs((x % 4) - 2)
            if c.get(x, zig) in "QP":
                c.put(x, zig, "T")
    for x in range(5, 27):
        if c.get(x, 22) not in "k.":
            c.put(x, 22, "R")
    c.outline("k")
    return c


stamp("pithos", "wood", _pithos(), 2, 2,
      note="the Pithos: a great silt-ware jar sealed with a stamped mud stopper")

# ===========================================================================
# Walls: windows, the ear stele, wall hangings
# ===========================================================================


def _window_river():
    """A high window with a palm-wood grille, the river and a sail beyond."""
    c = Canvas(16, 32)
    c.box(1, 8, 14, 16, "s")
    # the view: sky, far bank with palms, water, a sail
    for y in range(9, 23):
        for x in range(2, 14):
            if y < 15:
                ch = "s"
            elif y < 17:
                ch = "g" if (x * 3 + y) % 5 else "G"
            else:
                ch = "l" if (x + y) % 6 else "s"
            c.put(x, y, ch)
    c.paste([".v.", "vgv", ".G.", ".G."], 3, 11)      # a palm on the far bank
    c.paste(["w..", "ww.", "www", "KKK"], 9, 13)       # a sail and its hull
    # grille: three palm-wood bars and a sill
    for x in (5, 8, 11):
        c.vline(x, 9, 22, "K")
    c.hline(1, 14, 8, "K")
    c.hline(1, 14, 23, "j")
    c.hline(0, 15, 24, "k")
    c.hline(1, 14, 25, "J")
    return c


stamp("window_river", "nature", _window_river(), 1, 2,
      note="a high window with a palm-wood grille: the Nile, a far bank and a sail")


def _ear_stele():
    """A little round-topped stele of grey limestone, carved with two big
    ears (the god who hears) over a gilt line of text."""
    c = Canvas(16, 32)
    c.paste(["....kkkkkk....",
             "..kk555555kk..",
             ".k5555555544k.",
             ".k5kkk55kkk4k.",
             ".k5k33k5k33kk.",
             ".k5k3k35k3k3k.",
             ".k5k33k5k33k4k",
             ".k5k3k55k3k44k",
             ".k5kkk55kkk44k",
             ".k5555555544k.",
             ".k5gGgGgGgG4k.",
             ".k5555555444k.",
             ".kkkkkkkkkkkk.",
             "..k22222222k..",
             "..kkkkkkkkkk.."], 1, 10)
    return c


stamp("ear_stele", "stone", _ear_stele(), 1, 2,
      note="an ear stele: a votive carved with ears, so the god will hear")


# ===========================================================================
# Furniture shared by homes and halls
# ===========================================================================

def _bed():
    """An Egyptian bed (2x1): a frame on lion's legs, a footboard at the foot,
    a linen sheet under a striped red coverlet, and the wooden headrest where
    a Greek would want a pillow."""
    c = Canvas(32, 16)
    c.box(1, 3, 28, 8, "W")                 # the frame
    c.rect(2, 4, 26, 5, "Q")                # sheet
    c.hline(2, 27, 8, "P")
    for x in range(11, 28):                 # the coverlet over the lower part
        for y in range(4, 9):
            c.put(x, y, "t" if (x // 2) % 2 else "u")
        c.put(x, 4, "U" if (x // 2) % 2 else "u")
    c.vline(11, 4, 8, "T")
    c.hline(2, 27, 9, "w")
    c.hline(1, 28, 10, "k")
    c.box(27, 0, 5, 12, "W")                # footboard
    c.vline(28, 1, 10, "v")
    c.vline(30, 1, 10, "w")
    c.paste(["k...k", "kdkdk", ".kdk.", "kwwwk", "kkkkk"], 3, 1)      # headrest
    for x in (2, 24):
        c.paste(["kwk", "kdk", "kWWk", "kkkk"], x, 11)               # lion's feet
    return c


stamp("bed", "wood", _bed(), 2, 1,
      note="an Egyptian bed on lion's legs, with a footboard and a wooden headrest")


def _stool():
    c = Canvas(16, 16)
    c.paste(["..kkkkkkkkkk..",
             ".kvvvvvvvvvvk.",
             ".kWWWWWWWWWwk.",
             "..kkkkkkkkkk..",
             "...kwk..kwk...",
             "....kwkkwk....",
             ".....kwwk.....",
             "....kwkkwk....",
             "...kwk..kwk...",
             "..kdk....kdk..",
             "..kk......kk.."], 1, 4)
    return c


stamp("stool", "wood", _stool(), 1, 1, note="a folding stool with crossed legs and a leather seat")


def _chair():
    c = Canvas(16, 16)
    c.paste(["..kkkk.......",
             ".kvWWk.......",
             ".kWwWk.......",
             ".kWwWk.......",
             ".kWwWkkkkkkk.",
             ".kWwWvvvvvvWk",
             ".kWwWWWWWWWwk",
             ".kkkkkkkkkkkk",
             "..kWk....kWk.",
             "..kwk....kwk.",
             ".kwdk...kwdk.",
             ".kkk....kkk.."], 2, 3)
    return c


stamp("chair", "wood", _chair(), 1, 1, note="a chair with a slanted back and lion's feet")


def _table():
    """A low round-legged table (1x1) with a bowl of figs."""
    c = Canvas(16, 16)
    c.paste(["...kkkkkk...",
             "..k6uuuuTk..",
             "...kTTTTk..."], 2, 2)
    c.recolor({"6": "U"})
    c.paste([".kkkkkkkkkkkkk.",
             "kvvvvvvvvvvvvWk",
             "kWWWWWWWWWWWWwk",
             ".kkkkkkkkkkkkk.",
             "..kwk.....kwk..",
             "..kwk.....kwk..",
             "..kwk.....kwk..",
             "..kdk.....kdk..",
             "..kkk.....kkk.."], 0, 5)
    return c


stamp("table", "wood", _table(), 1, 1, note="a low table with a bowl of figs")


def _jar():
    """A silt-ware jar on a ring stand."""
    c = Canvas(16, 16)
    c.paste(["....kkkkk....",
             "...kUuuutk...",
             "....kuttk....",
             "..kkUuuttkk..",
             ".kUUuuuttTTk.",
             ".kUuuuutttTk.",
             ".kuuuuuttTTk.",
             ".kuQQQQQQQTk.",
             ".kutttttttTk.",
             "..kuttttTTk..",
             "...kttTTTk...",
             "....kkkkk....",
             "...kWWWWWk...",
             "...kkkkkkk..."], 1, 2)
    return c


stamp("jar", "wood", _jar(), 1, 1, note="a silt-ware jar with a white band, on its ring stand")


def _jars():
    """Three stoppered beer jars leaning together."""
    c = Canvas(16, 16)
    for (x, y) in ((1, 4), (9, 3), (5, 6)):
        c.paste(["..kkk..",
                 ".kdwdk.",
                 ".kkkkk.",
                 "kUuuttk",
                 "kUuuttk",
                 "kuuttTk",
                 "kuuttTk",
                 ".kttTk.",
                 "..kTk..",
                 "...k..."], x, y)
    return c


stamp("jars", "wood", _jars(), 1, 1, note="beer jars, stoppered with mud")


def _chest():
    """A painted chest on short legs, its lid gabled."""
    c = Canvas(16, 16)
    c.paste(["..kkkkkkkkkkk..",
             ".kvvvvvvvvvvvWk.",
             "kWWWWWWWWWWWWWwk",
             "kkkkkkkkkkkkkkkk",
             "kWLLLWLLLWLLLWwk",
             "kWLtLWLtLWLtLWwk",
             "kWLLLWLLLWLLLWwk",
             "kWWWWWWWWWWWWWwk",
             "kwwwwwwwwwwwwwdk",
             "kkkkkkkkkkkkkkkk",
             ".kdk.......kdk..",
             ".kkk.......kkk.."], 0, 3)
    return c


stamp("chest", "wood", _chest(), 1, 1, note="a chest with painted panels and a gabled lid")


def _basket(fill, top_rows, pal="nature"):
    c = Canvas(16, 16)
    c.paste(top_rows, 2, 1)
    c.paste(["kkkkkkkkkkkk",
             "kJjJjJjJjJjk",
             "kjJjJjJjJjKk",
             "kJjJjJjJjJKk",
             ".kjJjJjJjKk.",
             ".kJjJjJjJKk.",
             "..kKKKKKKk..",
             "...kkkkkk..."], 2, 8)
    return c


stamp("basket_dates", "nature", _basket("r", ["...kk.kk....",
                                              "..krrkrrk...",
                                              ".krrkrrkrk..",
                                              "krrkrrkrrrk.",
                                              "krkrrkrrkrrk",
                                              "kkrrkrrkrrrk",
                                              "kkkkkkkkkkkk"]), 1, 1,
      note="a basket of dates")
stamp("basket_eggs", "nature", _basket("w", ["............",
                                             "...kk..kk...",
                                             "..kwwkkwwk..",
                                             ".kwwnkwwnkk.",
                                             "kwwnkwwwkwwk",
                                             "kwnkwwnkwwnk",
                                             "kkkkkkkkkkkk"]), 1, 1,
      note="a wicker basket of eggs")
stamp("basket_fish", "nature", _basket("s", ["............",
                                             ".....kk.....",
                                             "...kkssk....",
                                             "..kSsssskk..",
                                             ".kSsskkSsssk",
                                             "kssSkSsssSSk",
                                             "kkkkkkkkkkkk"]), 1, 1,
      note="a basket of Nile perch")


def _sacks(resin):
    """Two burlap sacks, rolled down at the mouth to show what they hold."""
    c = Canvas(16, 16)
    hi, lo = {"frank": ("Q", "P"), "myrrh": ("t", "T"), "grain": ("v", "L")}[resin]
    sack = ["..kkkkk..",
            ".k12121k.",
            "k1212121k",
            "kvvvvvvvk",
            "kWvWWWWwk",
            "kWWWWWWwk",
            "kWWWWWwwk",
            "kWWWWwwdk",
            ".kWWwwddk",
            "..kkkkkk."]
    c.paste(sack, 6, 2, remap={"1": hi, "2": lo})
    c.paste(sack, 0, 5, remap={"1": hi, "2": lo})
    return c


stamp("sacks_frank", "wood", _sacks("frank"), 1, 1, note="sacks of frankincense: pale gold tears")
stamp("sacks_myrrh", "wood", _sacks("myrrh"), 1, 1, note="sacks of myrrh: red-brown lumps")
stamp("sacks_grain", "wood", _sacks("grain"), 1, 1, note="sacks of emmer wheat")


def _papyrus_column():
    """A closed-bud papyrus column (1x3), as at Saqqara: ribbed shaft, bound
    neck, bud capital, painted blue and red on limestone."""
    c = Canvas(16, 48)
    c.box(3, 0, 10, 3, "3")
    c.hline(4, 11, 1, "5")
    # bud capital
    for y in range(3, 14):
        t = (y - 3) / 10.0
        half = int(round(3 + 3 * (1 - abs(t - 0.6) / 0.6)))
        for x in range(8 - half, 8 + half):
            rel = (x - (8 - half))
            ch = "7" if rel == 1 else "6" if rel < half else "5" if rel < 2 * half - 1 else "4"
            if (x - 8) % 3 == 0:
                ch = "b"
            c.put(x, y, ch)
    for y in (14, 16):
        c.hline(4, 11, y, "G")
    c.hline(4, 11, 15, "t")
    for y in range(17, 44):
        for x in range(4, 12):
            ch = "4" if x in (6, 9) else "8" if x == 5 else "7" if x < 9 else "6" if x < 11 else "5"
            c.put(x, y, ch)
    c.box(3, 44, 10, 3, "4")
    c.hline(4, 11, 45, "6")
    c.outline("k")
    return c


stamp("papyrus_column", "stone", _papyrus_column(), 1, 3,
      note="a closed-bud papyrus column, ribbed, its neck bound in gold and red")


def _papyrus_pot():
    """Papyrus growing in a water pot (1x2): umbels like green fireworks."""
    c = Canvas(16, 32)
    stems = [(3, 6), (8, 2), (12, 7), (6, 10)]
    for (x, y) in stems:
        c.vline(x, y + 3, 22, "g")
    for (x, y) in stems:
        c.paste(["v.V.v", ".vVv.", "VvGvV", ".vgv.", "..g.."], x - 2, y)
    c.paste(["kkkkkkkkkkkk",
             "kllllllllllk",
             "kKjJJJJJjjKk",
             ".kjJJJJjjKk.",
             ".kjjJJjjjKk.",
             "..kjjjjjKk..",
             "..kKKKKKKk..",
             "...kkkkkk..."], 2, 22)
    c.outline("k", inside="vVgG")
    return c


stamp("papyrus_pot", "nature", _papyrus_pot(), 1, 2, note="papyrus growing in a pot of river water")


def _lamp():
    """A clay oil lamp, lit, on a wooden stand (1x2): the flame on top."""
    c = Canvas(16, 32)
    c.paste(["....Y....",
             "...YFY...",
             "...FfF...",
             "....f....",
             "..kkkkk..",
             ".kllmmdk.",
             "kkkkkkkkk",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "....kzk..",
             "...kbzzk.",
             "..kbbzzzk",
             "..kkkkkkk"], 3, 10)
    return c


stamp("lamp", "fire", _lamp(), 1, 2, note="a clay oil lamp, lit, on a bronze stand")


# ===========================================================================
# The Asclepeions: the healing basins and Imhotep
# ===========================================================================

def _basin(memphis=False):
    """A round limestone basin of water on a pedestal (2x2: the wall row and
    the counter row). The heal animation glows on the water (x 9-23, y 8-24).
    Naukratis's is fed from a gold lotus spout; Memphis's stands before an
    offering slab carved with loaves."""
    c = Canvas(32, 32)
    if memphis:
        c.box(5, 0, 22, 9, "6")
        c.hline(6, 25, 1, "7")
        for x in range(7, 25, 4):
            c.paste(["kk", "tt", "TT"], x, 3)
        c.hline(6, 25, 7, "5")
    else:
        c.paste(["...kkk...",
                 "..kgGgk..",
                 ".kgkgkGk.",
                 "..kgGgk..",
                 "...kGk...",
                 "...kgk...",
                 "...kGk...",
                 "....b...."], 12, 0)
    # rim
    c.ellipse(16, 15, 15, 7, "7")
    c.ellipse(16, 14.5, 14, 6, "8")
    c.ellipse(16, 15, 12, 5, "6")
    # water
    c.ellipse(16, 15.5, 11, 4, "b")
    for (x, y) in [(10, 14), (11, 14), (19, 16), (20, 16), (14, 17), (22, 13)]:
        c.put(x, y, "7")
    c.hline(9, 23, 12, "B")
    # front of the bowl
    for y in range(20, 24):
        half = 14 - (y - 20) * 2
        for x in range(16 - half, 16 + half):
            f = (x - (16 - half)) / (2 * half)
            c.put(x, y, "7" if f < 0.3 else "6" if f < 0.7 else "5")
    # pedestal and plinth
    for y in range(24, 29):
        for x in range(12, 20):
            c.put(x, y, "7" if x < 14 else "6" if x < 18 else "5")
    c.box(8, 28, 16, 4, "4")
    c.hline(9, 22, 29, "6")
    c.hline(9, 22, 30, "5")
    c.outline("k")
    return c


stamp("basin_naukratis", "stone", _basin(False), 2, 2,
      note="the healing basin, Naukratis: river water from a gold lotus spout")
stamp("basin_memphis", "stone", _basin(True), 2, 2,
      note="the healing basin, Memphis: an offering table with a pool")


def _imhotep():
    """Imhotep, whom the Greeks call Asclepius, seated with a papyrus open on
    his knees (1x2), on a block throne."""
    c = Canvas(16, 32)
    c.paste(["....kkkkk......",
             "...kBBBBBk.....",
             "..kBBbBBBBk....",
             "..kB5555Bk.....",
             "..k55k5k5k.....",
             "..k555555k.....",
             "...k5tt5k......",
             "...kk55kk......",
             "..k7777777k....",
             ".k777777777k...",
             ".k777g7777g7k..",
             ".k77g7777g77k..",
             ".k7777777777k..",
             ".k55kkkkkkkkk..",
             ".k5k8888888886k",
             ".k5k8B8B8B8B86k",
             ".k5k8888888886k",
             ".k5kkkkkkkkkkkk",
             ".k55777777777k.",
             ".k55777777777k.",
             ".k5577777777k..",
             ".k557k555k77k..",
             ".k555k555k55k..",
             "kkkkkkkkkkkkkkk",
             "k3333333333333k",
             "k4444444444444k",
             "kkkkkkkkkkkkkkk"], 0, 4)
    return c


stamp("imhotep", "stone", _imhotep(), 1, 2,
      note="Imhotep, the Greeks' Asclepius, seated with a papyrus on his knees")

wall("window_river", "ear_stele")

# The counters' fronts alone, where something else (the basin) stands on the
# counter's back row.
stamp("counter_heal_front", "stone", cells(_ASC_FRONT, 1, 0), 1, 1, behavior={(0, 0): "MB_COUNTER"},
      note="the Asclepeion counter's front, under the basin")
stamp("counter_stall_front", "wood", cells(_AGO_FRONT, 1, 0), 1, 1, behavior={(0, 0): "MB_COUNTER"},
      note="the stall counter's front alone")
nocat("counter_heal_front", "counter_stall_front")

# The rod of Asclepius over the Greek healers' counter at Naukratis: civic's
# relief, pixel for pixel (its palette is civic's marble, per's stone).
stamp("relief_rod", "stone", P.civic_piece("relief", "stone"), 1, 2,
      note="the rod of Asclepius painted over the counter (civic's relief)")
wall("relief_rod")


def _amphora_rack():
    """Greek transport amphorae (2x2) leaning in a wooden rack: wine from
    Chios and oil from Samos, landed at Naukratis."""
    c = Canvas(32, 32)
    # one amphora to every 8 pixels, all alike, so the rack's middle shares
    # its tiles: handles, a stamped shoulder band, the long body, the toe
    body = ["..kk..",
            ".kUUk.",
            "kk..kk",
            "kkuukk",
            "kuUUuk",
            "kQQQQk",
            "kuUUuk",
            "kuUUuk",
            "kuuuuk",
            "kuuuuk",
            "kuuuuk",
            "kttttk",
            ".kttk.",
            ".kttk.",
            ".kTTk.",
            "..kk..",
            "..kk.."]
    for col in range(4):
        c.paste(body, col * 8 + 1, 6)
    c.rect(0, 16, 32, 2, "W")       # the rack's rails
    c.hline(0, 31, 16, "v")
    c.rect(0, 26, 32, 2, "W")
    c.hline(0, 31, 26, "v")
    for x in (0, 31):
        c.vline(x, 12, 31, "w")
    c.hline(0, 31, 18, "k")
    c.hline(0, 31, 28, "k")
    return c


stamp("amphora_rack", "wood", _amphora_rack(), 2, 2,
      note="Greek transport amphorae in a rack: wine from Chios, oil from Samos")

import per_pieces_rooms  # noqa: E402,F401  (the rooms' own pieces)
