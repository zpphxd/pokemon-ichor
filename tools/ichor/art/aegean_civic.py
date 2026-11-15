#!/usr/bin/env python3
"""Kythera's halls: the Asclepeions' and Agoras' own pieces, in civic's style
(civic_art.py: character grids in civic's LEGEND, no ink outline on floors and
walls, a 1 px dark edge on objects, light from the top left).

Skandeia's Asclepeion: the wide window onto the quay, the hand-bath sunk in the
floor with the sea channel that feeds it, and the nets the healer's husband
hung from the cornice. Skandeia's Agora: Teukros's counter, half a boat with a
painted eye; coils of rope; the dove carved in the beam over the Frankincense.
Paphia's Asclepeion: the freestanding fountain the doves bathe in, rose beds
and the rose hedge round the courtyard. Paphia's Agora: dove cages, honey
cakes on the marble counter, shelves of incense.

define() registers civic's metatiles (civic_tiles.define) and then these, so
the names keep civic's scheme (asc_, ago_, aka_ prefixes).
"""
import numpy as np

import civic_art as CA
import civic_tiles as ct
from aegean_art import Canvas
from civic_art import art

# civic's palette plan, unchanged: every piece below keeps each 8x8 tile in one.
PALETTES = dict(ct.PALETTES)


def rows(c):
    return c.text().split("\n")


# ==========================================================================
# Art
# ==========================================================================

def _sea_window():
    """48x32 over the back wall: a marble frame round a view of the quay, the
    sea, a moored boat's mast and the far shore (spring palette)."""
    c = Canvas(48, 32)
    c.rect(1, 4, 46, 29, "1")
    c.rect(2, 5, 45, 28, "7")
    c.hline(2, 45, 5, "8")
    c.vline(2, 5, 28, "8")
    c.vline(45, 6, 28, "5")
    c.hline(3, 44, 28, "5")
    # the opening: sky, far hills, sea, the quay's edge
    c.rect(5, 8, 42, 25, "F")
    c.rect(5, 8, 42, 10, "C")
    c.rect(5, 15, 42, 15, "4")
    c.paste("....33....3333.........333......33333.....", 5, 14)
    c.rect(5, 16, 42, 22, "c")
    for (x, y, n) in [(8, 17, 5), (22, 19, 6), (33, 17, 4), (13, 21, 4), (38, 21, 3)]:
        c.hline(x, x + n, y, "C")
    c.rect(5, 23, 42, 25, "5")
    c.hline(5, 42, 23, "6")
    # a moored boat and its mast
    c.vline(27, 9, 19, "3")
    c.hline(24, 31, 12, "3")
    c.paste("1111111111\n.13333331.\n..111111..", 23, 19)
    # mullions
    for x in (17, 30):
        c.rect(x, 8, x + 1, 25, "6")
        c.vline(x + 1, 8, 25, "4")
    c.rect(3, 6, 44, 7, "6")
    c.rect(4, 26, 43, 27, "6")
    return rows(c)


art("sea_window", _sea_window())


def _bath(part):
    """A hand-bath sunk in the floor, one row deep: rim, sea water, rim."""
    c = Canvas(16, 16)
    c.rect(0, 0, 15, 15, "5")
    c.rect(0, 0, 15, 1, "7")
    c.rect(0, 3, 15, 12, "B")
    c.rect(0, 4, 15, 12, "b")
    c.hline(0, 15, 13, "1")
    c.rect(0, 14, 15, 15, "6")
    for (x, y, n) in [(2, 7, 4), (9, 10, 4), (6, 5, 3)]:
        c.hline(x, x + n, y, "c")
        c.px(x + 1, y - 1, "C")
    if part == "l":
        c.rect(0, 0, 1, 15, "5")
        c.vline(2, 3, 12, "1")
        c.vline(0, 0, 15, "7")
    if part == "r":
        c.rect(14, 0, 15, 15, "5")
        c.vline(13, 3, 12, "1")
    return rows(c)


def _channel():
    """The sea channel: water running in from the inlet along the floor."""
    c = Canvas(16, 16)
    c.rect(0, 0, 15, 15, "6")
    c.rect(0, 0, 15, 1, "7")
    c.rect(0, 5, 15, 10, "B")
    c.rect(0, 6, 15, 10, "b")
    c.hline(0, 15, 11, "1")
    c.rect(0, 12, 15, 15, "6")
    for (x, n) in [(1, 3), (8, 4)]:
        c.hline(x, x + n, 8, "c")
    # the stream turns up into the wall at the right
    c.rect(10, 0, 14, 10, "b")
    c.vline(9, 0, 10, "1")
    c.vline(15, 0, 10, "5")
    c.px(12, 2, "c")
    c.px(11, 5, "C")
    return rows(c)


def _inlet():
    """A bronze-barred arch at the foot of the wall, sea water spilling out."""
    c = Canvas(16, 16)
    c.paste("""
................
................
................
................
................
....11111111....
...1888888881...
..1866666666B1..
..18BbcbbbbbB1..
..18bGbGbGbGb1..
..18bGbGbGbGb1..
..18bbbbbbbbb1..
..18bbbbcbbbb1..
..11bbbbbbbbb1..
...1bbbcbbbbb1..
...1bbbbbbbbb1..""", 0, 0)
    return rows(c)


art("bath_l", _bath("l"))
art("bath_m", _bath("m"))
art("bath_r", _bath("r"))
art("channel", _channel())
art("inlet", _inlet())


def _nets():
    """32x16 on the wall's top row: a net hung from the cornice in two swags,
    cork floats along its head rope (wood palette)."""
    c = Canvas(32, 16)
    import math
    for x in range(1, 31):
        t = (x - 1) / 29
        sag = int(round(3 + 8 * abs(math.sin(math.pi * t * 2))))
        for y in range(2, 2 + sag):
            if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                c.px(x, y, "p" if (x + y) % 6 else "d")
        c.px(x, 2 + sag, "d")
    c.hline(0, 31, 1, "D")
    for x in range(2, 31, 5):
        c.paste("Dt\ntT", x, 1)
    for x in (0, 31):
        c.vline(x, 0, 2, "D")
    return rows(c)


art("nets_cornice", _nets())


def _nets_hung():
    """32x32 over the wall's two rows: a whole net hung from two pegs under
    the cornice, sagging to the dado, floats on its head rope, lead sinkers
    on its foot (wood palette)."""
    import math
    c = Canvas(32, 32)
    top = 7
    for x in range(2, 30):
        t = (x - 2) / 27
        bottom = int(round(top + 8 + 12 * math.sin(math.pi * t)))
        for y in range(top + 1, bottom):
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                c.px(x, y, "p" if (x + y) % 8 else "d")
        c.px(x, bottom, "d")
        if x % 3 == 1:
            c.px(x, bottom + 1, "D")
    c.hline(1, 30, top, "D")
    for x in range(3, 29, 4):
        c.paste("Dt\ntT", x, top - 1)
    for x in (1, 30):
        c.vline(x, top - 3, top, "D")
    return rows(c)


art("nets_hung", _nets_hung())


def _boat_counter():
    """Teukros's counter, half an old boat stood up on its cut end: the top
    row is the gunwale seen from above, the dark hull inside crossed by its
    frames and a thwart, the stem post rising at the bow; the front row is the
    planked side, its strakes sweeping up to bow and stern, a red wale, and the
    painted eye at the bow (wood palette). 80x32."""
    c = Canvas(80, 32)
    # top row: a pointed bow at the left, a rounded stern at the right
    for x in range(3, 77):
        t = (x - 3) / 73
        half = 4 if t > 0.12 else max(1, int(4 * t / 0.12))
        c.vline(x, 11 - half, 11 + half, "d")
        c.px(x, 11 - half, "v")
        c.px(x, 11 - half - 1, "D")
        c.px(x, 11 + half + 1, "D")
    for x in range(14, 74, 8):
        c.vline(x, 8, 14, "D")
        c.vline(x + 1, 8, 14, "w")
    c.rect(44, 8, 47, 14, "W")
    c.vline(44, 8, 14, "v")
    # the stem post at the bow, curling up over the counter
    c.paste("""
.DDD.
DvWWD
DWwD.
DWwD.
DWwD.
.DWD.
.DWwD
..DWD""", 0, 0)
    # front row: strakes sweeping up at the ends, the wale, the eye
    for x in range(0, 80):
        t = x / 79
        lift = int(round(6 * (1 - min(t, 1 - t) / 0.18))) if min(t, 1 - t) < 0.18 else 0
        bottom = 30 - lift
        c.vline(x, 16, bottom, "W")
        c.px(x, bottom + 1, "D")
        for y in (21, 25):
            if y < bottom:
                c.px(x, y, "w")
                c.px(x, y + 1, "d")
        c.px(x, 16, "v")
        c.px(x, 18, "R")
        c.px(x, 19, "R")
        c.px(x, 20, "T")
    c.vline(0, 16, 24, "D")
    c.vline(79, 16, 24, "D")
    c.paste("""
...RRRRR...
.RRQQQQQRR.
RQQQ##QQQQR
.RRQ##QQRR.
...RRRRR...""", 5, 21)
    return rows(c)


art("boat_counter", _boat_counter())


def _rope(seed):
    """A coil of rope on the floor, its turns lined in shadow, the loose end
    trailing (wood palette's hemp)."""
    c = Canvas(16, 16, """
................
................
................
................
....DDDDDDD.....
..DDPQPPPQPDD...
.DPQLpppppLQPD..
DPLppPQPPPppLPD.
DPpPQLpppLQPpPD.
DPpPLpDDDpLPpPD.
DPPpLPQPPPLpPPD.
.DPPpppppppPPD..
..DDPPPPPPPDD...
....DDDDDDD.....
................
................""")
    if seed:
        c.paste("..DD\n.DQD\nDPD.\nDD..", 12, 1)
        c.flip()
    return rows(c)


art("rope", _rope(0))
art("rope_b", _rope(1))


def _incense_shelves():
    """32x48 against the wall: a carved dove in the beam over two high
    shelves of Frankincense in jars and baskets (wood palette)."""
    c = Canvas(32, 48)
    # the dove carved in the beam (rows 0-6 of the wall)
    c.paste("""
........QQ.....
.......QQQd....
...PQQQQQQ.....
.PQQQQQQQQPP...
..DPPQQQQQQQPPD
....DDDDPPPPDD.""", 8, 1)
    # two shelf units
    for x0 in (0, 16):
        c.rect(x0, 8, x0 + 15, 47, "D")
        c.rect(x0 + 1, 9, x0 + 14, 46, "d")
        for y in (9, 22, 35):
            c.rect(x0 + 1, y + 10, x0 + 14, y + 11, "v")
            c.hline(x0 + 1, x0 + 14, y + 12, "D")
        # jars of resin, lumps of frankincense in baskets
        for (dx, y) in ((2, 11), (9, 11), (3, 24), (8, 37)):
            c.paste(".RR.\nRutR\nRutR\n.RR.", x0 + dx, y + 3)
        for (dx, y) in ((7, 24), (2, 37)):
            c.paste("QPQP\nWWWW\n.ww.", x0 + dx, y + 4)
    return rows(c)


art("incense_shelves", _incense_shelves())


def _fountain():
    """32x32: a freestanding round fountain in the courtyard: a column with a
    bowl spouting water into a basin, a dove on the rim (spring palette). The
    top row stands in front of the hedge, the bottom row on the grass."""
    c = Canvas(32, 32)
    # the basin
    c.ellipse(16, 24, 15, 6.5, fill="1")
    c.ellipse(16, 23.5, 14, 5.5, fill="7")
    c.ellipse(16, 24, 11.5, 4, fill="b")
    c.ellipse(16, 23.5, 10.5, 3, fill="c")
    c.rect(2, 25, 29, 29, "6")
    c.hline(2, 29, 29, "4")
    c.vline(1, 24, 29, "1")
    c.vline(30, 24, 29, "1")
    c.hline(2, 29, 30, "1")
    for (x, y) in [(8, 24), (19, 25), (13, 23), (24, 23)]:
        c.px(x, y, "F")
    # the column and the upper bowl
    c.rect(14, 8, 17, 22, "1")
    c.rect(15, 8, 16, 22, "7")
    c.vline(15, 8, 22, "8")
    c.ellipse(16, 8, 7, 2.6, fill="1")
    c.ellipse(16, 7.5, 6, 1.8, fill="c")
    # the spout's water falling
    for x in (10, 22):
        c.vline(x, 9, 20, "C")
    c.vline(16, 1, 6, "C")
    c.px(16, 0, "F")
    # a dove on the rim
    c.paste(".88.\n8886\n.866\n..1.", 23, 17)
    return rows(c)


art("fountain", _fountain())


def _roses(seed):
    """A rose bush on the grass (grove palette)."""
    rnd = np.random.RandomState(seed)
    c = Canvas(16, 16)

    def sh(x, y, nx, ny):
        v = -0.5 * nx - 0.85 * ny + (rnd.rand() - 0.5) * 0.4
        return "O" if v > 0.5 else "o" if v > 0.0 else "y" if v > -0.5 else "E"
    c.ellipse(8, 8, 7, 6.5, shade=sh)
    for (x, y) in [(4, 5), (10, 4), (7, 9), (12, 9), (4, 11), (9, 12)]:
        x, y = x + rnd.randint(0, 2), y + rnd.randint(0, 2)
        c.paste("AA\nAg", x, y)
    c.outline("e")
    return rows(c)


art("roses", _roses(1))
art("roses_b", _roses(2))


def _rose_bed():
    """Grass with fallen petals and low roses: Panacoil's bed (walkable)."""
    g = list(CA.ART["grass_a"])
    c = Canvas(16, 16, "\n".join(g))
    for (x, y) in [(2, 3), (9, 1), (12, 7), (5, 9), (1, 13), (10, 12), (14, 14), (6, 5)]:
        c.paste("oA\nAy", x, y)
    for (x, y) in [(4, 1), (13, 3), (8, 14)]:
        c.px(x, y, "A")
    return rows(c)


art("rose_bed", _rose_bed())


def _hedge_roses():
    g = list(CA.ART["hedge"])
    c = Canvas(16, 32, "\n".join(g))
    for (x, y) in [(3, 4), (11, 7), (6, 12), (13, 15), (2, 19), (9, 21), (5, 26), (12, 24)]:
        c.paste(".A.\nAgA\n.A.", x, y)
    return rows(c)


art("hedge_roses", _hedge_roses())


def _dove_cage():
    """16x32: a wicker cage of doves on a stand (wood palette)."""
    c = Canvas(16, 32)
    c.paste("""
................
................
................
................
................
................
................
.......DD.......
......DvvD......
....DDDDDDDD....
...DvwvwvwvwD...
..DvDvDvDvDvDD..
..DwDQQDvDQQwD..
..DvDQPQvQPQvD..
..DwDLQDvDLQwD..
..DvDvDvDvDvDD..
..DwDvDvDvDvwD..
..DvQQDvDvDQQD..
..DwQPQvDvQPQD..
..DvLQDvDvDLQD..
..DwDvDvDvDvwD..
..DDDDDDDDDDDD..
..DWWWWWWWWWWD..
..DwwwwwwwwwwD..
...DDDDDDDDDD...
....Dw....wD....
....Dw....wD....
....Dd....dD....
....DD....DD....
................
................
................""", 0, 0)
    return rows(c)


art("dove_cage", _dove_cage())


def _cakes():
    """The counter slab with a plate of honey cakes on it (marble palette)."""
    c = Canvas(16, 16, "\n".join(r[16:32] for r in CA.ART["counter_asc_top"]))
    c.paste("""
...111111111....
..1GgggGgggG1...
.1GgTgGgTgGgG1..
.1tGGtGGtGGtt1..
..1111111111....""", 1, 3)
    return rows(c)


art("counter_cakes", _cakes())


# ==========================================================================
# Metatiles
# ==========================================================================

FIRST_NEW = None   # index in civic_tiles.METATILES of the first of these


def define():
    global FIRST_NEW
    ct.define()
    FIRST_NEW = len(ct.METATILES)
    C, mt, obj, shadowed = ct.C, ct.mt, ct.obj, ct.shadowed
    fa, fb = C("floor_marble_a"), C("floor_marble_b")
    fa_sh, fb_sh = shadowed(fa), shadowed(fb)
    atop, abody = C("wall_asc_top"), C("wall_asc_body")
    ft = C("floor_tc")
    ft_sh = shadowed(ft)
    gtop, gbody = C("wall_ago_top"), C("wall_ago_body")
    ga = C("grass_a")
    ga_sh = shadowed(ga)

    # ---- Skandeia's Asclepeion ---------------------------------------------
    obj("asc_seawin", "sea_window", [atop, abody])
    for part in "lmr":
        for suf, f in (("", fa_sh), ("_b", fb_sh)):
            mt(f"asc_bath_{part}{suf}", f, middle=C(f"bath_{part}"), solid=True)
    mt("asc_channel", fa_sh, middle=C("channel"), solid=True)
    mt("asc_channel_b", fb_sh, middle=C("channel"), solid=True)
    mt("asc_inlet", abody, middle=C("inlet"), solid=True)
    obj("asc_nets", "nets_cornice", atop)
    obj("asc_nets_hung", "nets_hung", [atop, abody])

    # ---- Skandeia's Agora --------------------------------------------------
    boat = "boat_counter"
    # the top row: bow, gunwale, the staff cell (the slab on the top layer so
    # Teukros standing in it shows from the waist up), stern
    mt("ago_boat_l", ft_sh, middle=C(boat, 0, 0), solid=True)
    mt("ago_boat_m", ft_sh, middle=C(boat, 1, 0), solid=True)
    mt("ago_boat_staff", ft_sh, top=C(boat, 2, 0))
    mt("ago_boat_m2", ft_sh, middle=C(boat, 3, 0), solid=True)
    mt("ago_boat_r", ft_sh, middle=C(boat, 4, 0), solid=True)
    for i in range(5):
        mt(f"ago_boat_front_{i}", ft, middle=C(boat, i, 1), behavior="MB_COUNTER", solid=True)
    mt("ago_rope", ft, middle=C("rope"), solid=True)
    mt("ago_rope_b", ft, middle=C("rope_b"), solid=True)
    obj("ago_incense", "incense_shelves", [gtop, gbody, ft_sh],
        behavior=lambda x, y: "MB_SHOP_SHELF" if y == 2 else "MB_NORMAL")

    # ---- Paphia's Asclepeion -----------------------------------------------
    hedge_r = [C("hedge_roses", 0, 0), C("hedge_roses", 0, 1)]
    mt("aka_hedge_roses_top", hedge_r[0], solid=True)
    mt("aka_hedge_roses", hedge_r[1], solid=True)
    obj("asc_fountain", "fountain", [hedge_r[1], ga_sh])
    mt("aka_roses", ga, middle=C("roses"), solid=True)
    mt("aka_roses_b", ga, middle=C("roses_b"), solid=True)
    mt("aka_roses_sh", ga_sh, middle=C("roses"), solid=True)
    mt("aka_rose_bed", C("rose_bed"))

    # ---- Paphia's Agora ----------------------------------------------------
    for suf, f in (("", fa), ("_b", fb)):
        obj(f"asc_cage{suf}", "dove_cage", f)
    mt("asc_counter_cakes", fa_sh, middle=C("counter_cakes"), solid=True)
    obj("asc_incense", "incense_shelves", [atop, abody, fa_sh],
        behavior=lambda x, y: "MB_SHOP_SHELF" if y == 2 else "MB_NORMAL")
