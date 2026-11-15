#!/usr/bin/env python3
"""The country houses' pieces: Myles's mill at the Neraida falls and Melos's
three households (design/phase4/ROOMS_aegean.md).

The millstone, grain sacks, flour on the floor and the bread oven; Kentrios's
hoe on its pegs, his shelf of field finds and his barley; Melanippos's
obsidian flakes, anvil stone, antler hammers, cores and black mirror; the
boathouse's slip and rollers, the sea under its painted doors, and the cradle
in the room over the boat. Drawn in oikia's palettes (aegean_art.PALETTES).
"""
import math

import numpy as np

from aegean_art import Canvas, stamp

# ==========================================================================
# Myles's mill
# ==========================================================================


def _millstone():
    """The runner stone on its bed stone, seen from above and a little in
    front: dressed with radial furrows, the shaft standing in its eye, the
    hopper's spout over it and a heap of meal at the lip."""
    c = Canvas(32, 32)
    # bed stone (the lower ring, its front face showing)
    c.ellipse(16, 18, 15, 12, fill="s")
    c.ellipse(16, 16, 15, 12, fill="S")

    # the runner stone, lit from the top left
    def sh(x, y, nx, ny):
        v = -0.5 * nx - 0.85 * ny
        return "t" if v > 0.35 else "S" if v > -0.55 else "s"
    c.ellipse(16, 14, 12.5, 9.5, shade=sh)
    # its dressing: eight furrows running from the eye to the rim, each set a
    # little off the radius (the millers' "harp"), a lit land beside each
    for k in range(8):
        a = k * math.pi / 4 + 0.35
        x0, y0 = 16 + 3.5 * math.cos(a - 0.35), 14 + 2.7 * math.sin(a - 0.35)
        x1, y1 = 16 + 11.0 * math.cos(a), 14 + 8.3 * math.sin(a)
        c.line(x0, y0, x1, y1, "a")
        c.line(x0 + 1, y0, x1 + 1, y1, "t" if math.sin(a) < 0.2 else "S")
    # the eye and the shaft
    c.ellipse(16, 14, 3, 2.4, fill="a")
    c.paste(".kk.\nkmlk\nkmlk\nkmlk\nkmlk\nkmlk\nkmlk\nkmlk", 14, 0)
    c.paste("kkkkkkkk\nkdmllmdk\nkkkkkkkk", 12, 3)
    # meal spilled at the front
    c.paste("..ccc..\n.ccctc.\nctccctc", 20, 24)
    c.outline()
    return c


stamp("millstone", "clay", _millstone(), 2, 2,
      note="the great millstone turning on its shaft, meal at its lip")


def _sack(c, x, y, tilt=0):
    c.paste("""
...kk...
..kCck..
...kk...
.kcccck.
kccccCCk
kcccccCk
kcncccCk
kccccCCk
kcccCCCk
.kCCCCk.
..kkkk..""", x, y)


def _sacks(seed):
    c = Canvas(16, 16)
    if seed == 0:
        _sack(c, 0, 4)
        _sack(c, 7, 5)
        c.paste("..oo..\n.oyyo.", 5, 14)
    else:
        _sack(c, 4, 4)
        c.paste("..oyo.\n.oyyoo\noyoyyo", 9, 13)
    return c


stamp("sacks", "cloth", _sacks(0), 1, 1, note="sacks of grain, tied at the neck")
stamp("sack", "cloth", _sacks(1), 1, 1, note="a sack of grain, a little spilled")


def _flour(seed, n):
    rnd = np.random.RandomState(seed)
    c = Canvas(16, 16)
    for _ in range(n):
        x, y = rnd.randint(0, 14), rnd.randint(0, 14)
        c.paste("cc\nCc" if rnd.randint(2) else "c.\ncc", x, y)
    return c


stamp("flour", "cloth", _flour(1, 11), 1, 1, walk={(0, 0)}, note="flour dusted over the floor (walkable)")
stamp("flour_b", "cloth", _flour(2, 6), 1, 1, walk={(0, 0)}, note="a little flour on the floor (walkable)")


def _oven():
    """A domed bread oven against the wall, its mouth glowing, two loaves on
    the ledge."""
    c = Canvas(32, 32)

    def sh(x, y, nx, ny):
        v = -0.55 * nx - 0.85 * ny
        return "t" if v > 0.5 else "S" if v > -0.2 else "s"
    c.ellipse(16, 18, 14, 13, shade=sh)
    c.rect(2, 20, 29, 29, "S")
    c.hline(2, 29, 29, "s")
    c.vline(29, 18, 29, "s")
    # whitewash on the dome
    for (x, y) in [(9, 9), (13, 7), (8, 13), (17, 6)]:
        c.px(x, y, "c")
    c.paste("""
...kkkkkk...
..kaaaaaak..
.kaafFFfaak.
kaafFYYFfaak
kafFYYYYFfak
kfFYYYYYYFfk""", 10, 18)
    c.rect(2, 26, 29, 27, "t")
    c.hline(2, 29, 28, "S")
    c.paste(".kkkk.\nkhllmk\nkmmmdk", 3, 23)
    c.paste(".kkkk.\nkhllmk\nkmmmdk", 22, 23)
    c.outline()
    return c


stamp("bread_oven", "clay", _oven(), 2, 2, note="the bread oven, domed and whitewashed, loaves on its ledge")

# ==========================================================================
# Kentrios's farmhouse
# ==========================================================================

stamp("hoe_pegs", "wood", """
................
................
................
................
................
................
................
................
................
....kk.....kk...
....kdk....kdk..
kkkkkkkkkkkkkkk.
khhhhhhhhhhhhhhk
klllllllllllllmk
kmmmmmmmmmmmmdk.
kkkkkkkkkkkkkk..
kyybk...........
kybbzk..........
kbbbzk..........
kzbzzk..........
.kzzk...........
..kk............
................
................
................
................
................
................
................
................
................
................
""", 1, 2, note="the hoe that found the goddess, laid on two pegs, its blade down")

stamp("finds_shelf", "clay", """
................................
................................
................................
................................
................................
................................
................................
................................
................................
................................
.................kkk............
..kk....kkkk....kccck...........
.kmlk..kmlllkk..kcttk.....kk....
.kmdmkkmllllmlk.kcttk....kaak...
kmlddk.kmmmmmk...kcck...kaacak..
kkkkk..kkkkkk....kkk...kaaakak..
..........kkk.........kakkkk....
.........kbYbk.........k........
..........kkk...................
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
kddddddddddddddddddddddddddddddk
kdmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
...kdk....................kdk...
...kdk....................kdk...
....k......................k....
................................
................................
................................
................................
................................
................................
""", 2, 2, note="his shelf of finds: a sherd, a clay lamp, a coin, a marble toe, an obsidian blade")

stamp("barley_basket", "nature", """
................
................
...k..k.k..k....
..kJk.kJkkJk....
..kjJkJjkJjk.k..
...kJjJjJjjkkJk.
..kJjJjJjJjJjJk.
kkkkkkkkkkkkkkkk
kJJJjJJJjJJJjJJk
kjjKjjjKjjjKjjjk
kJjjjJjjjJjjjjJk
kjKjjjKjjjKjjKjk
.kjjjjjjjjjjjjk.
..kKKKKKKKKKKk..
...kkkkkkkkkk...
................
""", 1, 1, note="a basket of barley")

# ==========================================================================
# Melanippos's house
# ==========================================================================


def _flakes(seed, n):
    rnd = np.random.RandomState(seed)
    c = Canvas(16, 16)
    for _ in range(n):
        x, y = rnd.randint(0, 14), rnd.randint(0, 14)
        shape = [["ka", "a."], ["k.", "ak"], [".k", "ka"], ["kc", "a."], ["ak", ".a"]][rnd.randint(5)]
        c.paste(shape, x, y)
    return c


stamp("flakes", "clay", _flakes(1, 14), 1, 1, walk={(0, 0)},
      note="black obsidian flakes on the floor, glinting (walkable)")
stamp("flakes_b", "clay", _flakes(2, 9), 1, 1, walk={(0, 0)}, note="obsidian flakes (walkable)")
stamp("flakes_c", "clay", _flakes(3, 5), 1, 1, walk={(0, 0)}, note="a few obsidian flakes (walkable)")

stamp("anvil_stone", "clay", """
................
................
.........kk.....
....kkkkkchk....
...kcchcccck....
..kdkkkkkkkdk...
.kdmlllllllmdk..
.kkkkkkkkkkkkk..
.ktttttttttttsk.
kStttttttttttssk
kSSttttttttttssk
kSSSSSSSSSSSSssk
kSSSSSSSSSSSssk.
.ksssssssssssk..
..kkkkkkkkkkk...
................
""", 1, 1, note="the knee-high anvil stone with its leather pad")

stamp("antler_hammers", "nature", """
................
................
................
................
................
................
................
................
.kkkkkkkkkkkkkk.
.kjjjjjjjjjjjjk.
.kKKKKKKKKKKKKk.
.kkkkkkkkkkkkkk.
..kk...kk...kk..
..kn...kn...kn..
..kk..kkk...kk..
.kwSkkwwSk.kwSk.
kwwSkkwwSkkwwSk.
kwSk.kwSk.kwSkk.
kwSk.kwSk.kwSkSk
.kwSkkwSk..kwSk.
.kwSk.kwSk.kwSk.
.kKjk.kKjk.kKjk.
.kKKk.kKKk.kKKk.
..kk...kk...kk..
................
................
................
................
................
................
................
................
""", 1, 2, note="antler hammers hung in a row by their thongs, the burrs at the bottom")

stamp("cores_shelf", "clay", """
................................
................................
................................
................................
................................
................................
................................
................................
................................
................................
..kkkk.......kkk................
.kaacak....kkaaak......kkkkk....
kaacaaakk.kacaaaak....kaaacak...
kakaaaakak.kaaakak...kacaaaaak..
kaaaakaak..kakaaak...kaaakaaak..
.kkaaaak...kaaaak.....kaaaaak...
...kkkk.....kkkk.......kkkkk....
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
kddddddddddddddddddddddddddddddk
kdmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
...kdk....................kdk...
...kdk....................kdk...
....k......................k....
................................
................................
................................
................................
................................
................................
................................
................................
""", 2, 2, note="cores of black glass on a shelf")


def _obsidian_mirror():
    c = Canvas(16, 32)

    def sh(x, y, nx, ny):
        d = nx * nx + ny * ny
        if d > 0.75:
            return "b"
        v = -0.6 * nx - 0.8 * ny
        return "s" if v > 0.75 else "a" if v > 0.1 else "k"
    c.ellipse(8, 15, 6.5, 6.5, shade=sh)
    c.paste("c\n.c", 4, 11)
    c.px(9, 9, "s")
    c.paste(".k.\nkbk", 7, 6)
    c.outline()
    return c


stamp("obsidian_mirror", "clay", _obsidian_mirror(), 1, 2,
      note="a round mirror of polished black glass; it reflects, darkly")

# ==========================================================================
# The boathouse
# ==========================================================================

stamp("rollers", "wood", """
.kdk.........kdk
.kdk.........kdk
kkkkkkkkkkkkkkkk
hhhhhhhhhhhhhhhh
llllllllllllllll
mmmmmmmmmmmmmmmm
kkkkkkkkkkkkkkkk
.kdk.........kdk
.kdk.........kdk
kkkkkkkkkkkkkkkk
hhhhhhhhhhhhhhhh
llllllllllllllll
mmmmmmmmmmmmmmmm
kkkkkkkkkkkkkkkk
.kdk.........kdk
.kdk.........kdk
""", 1, 1, walk={(0, 0)}, note="log rollers across the slip's timber ways (walkable)")


def _sea(edge, doors=False):
    """Sea water in the boathouse: the slip's stone lip on its top edge."""
    c = Canvas(16, 16)
    c.rect(0, 0, 15, 15, "u")
    for (x, y, n) in [(2, 6, 4), (9, 10, 5), (5, 13, 3), (11, 4, 3)]:
        c.hline(x, x + n, y, "U")
        c.hline(x + 1, x + n - 1, y - 1, "a")
    if edge:
        c.rect(0, 0, 15, 2, "m")
        c.hline(0, 15, 0, "M")
        c.hline(0, 15, 3, "k")
        c.hline(0, 15, 4, "z")
    return c


stamp("sea_edge", "bronze", _sea(True), 1, 1, note="sea water at the foot of the slip")
stamp("sea", "bronze", _sea(False), 1, 1, note="sea water")


def _sea_doors(color, latch):
    """The painted sea doors, seen from inside: planks to the top of the cell,
    the bar across them, the sea glinting in the gap below."""
    c = Canvas(16, 16)
    hi, lo = {"blue": ("B", "b"), "red": ("r", "R")}[color]
    c.rect(0, 0, 15, 12, hi)
    for x in range(0, 16, 4):
        c.vline(x + 3, 0, 12, lo)
        c.vline(x, 0, 12, "k" if x == 0 else lo)
    c.rect(0, 4, 15, 6, "2")
    c.hline(0, 15, 4, "3")
    c.hline(0, 15, 7, "k")
    if latch:
        c.paste("kk\nkk", 13, 4)
    c.hline(0, 15, 12, "k")
    c.rect(0, 13, 15, 15, "a")
    c.paste("bb..bbb.bb..bbbb", 0, 14)
    return c


stamp("sea_doors_l", "wall", _sea_doors("blue", False), 1, 1, note="the painted sea doors, the sea under them")
stamp("sea_doors_m", "wall", _sea_doors("blue", True), 1, 1, note="the painted sea doors, barred")
stamp("sea_doors_r", "wall", _sea_doors("red", False), 1, 1, note="the sea doors' red leaf")

stamp("cradle", "nature", """
..Kn........nK..
..Kn........nK..
..Kn........nK..
..Kn........nK..
...Kn......nK...
...Kn......nK...
....Kn....nK....
.kkkkkkkkkkkkkk.
kJJJJJJJJJJJJJJk
kjkwwwwwwwwwwkjk
kjkwwnwwwwnwwkjk
kjkwwwwwwwwwwkjk
kJkkkkkkkkkkkkJk
.kjjjjjjjjjjjjk.
..kKKKKKKKKKKk..
...kkkkkkkkkk...
""", 1, 1, note="a wicker cradle hung from the beam on ropes")
