"""Trophonios's cave: the furniture. Braziers, the throne of Mnemosyne, the
grille, the ladder, the stairs, the spring, the pilgrims' chalk handprints,
the snake's cleft, the black pool, the bread-oven hole, the offerings, the
votive tablets and lamps of the upper chamber, webs, bones and rocks.

Pieces set into a wall are painted over the face kit's cells (a face two
cells tall under the cap, or the ladder's three-tall free face), so they sit
in any wall the map builder draws. Everything else stands in the middle
layer over the plain floor (or the paving).
"""
from __future__ import annotations

import numpy as np

import trophonios_kit as KIT
import trophonios_lib as T

SEC = "props"


def face_under(s, cx, cy, H=2, r=1, top="c", end="M"):
    """Paint a plain face cell into s's bottom layer at cell (cx, cy)."""
    KIT.paint_face_cell(s, cx * 16, cy * 16, H, r, top, end, L=s.B)


def floor_under(s, cx, cy, variant=0):
    T.floor_cell(s.B, cx * 16, cy * 16, variant)


def pave_under(s, cx, cy):
    def flag_px(x, y):
        row = y // 8
        xo = (x + (4 if row % 2 else 0)) % 8
        if y % 8 == 7 or xo == 7:
            return "fl1"
        if y % 8 == 0 or xo == 0:
            return "pv1" if (x + y) % 5 else "pv2"
        h = T.hsh(x, y, 1) % 100
        return "fl3" if h < 22 else ("fl4" if h < 88 else "pv1")
    for y in range(16):
        for x in range(16):
            s.B.px(cx * 16 + x, cy * 16 + y, flag_px(x, y))


def shadow(s, ox, oy, w, rows=(14, 15), x0=2):
    """A soft contact shadow on the floor under a prop (bottom layer)."""
    for y in rows:
        for x in range(x0, x0 + w):
            cur = s.B.get(ox + x, oy + y)
            if cur in ("fl2", "fl3", "fl1", "pv1", "pv2", "fl4"):
                s.B.px(ox + x, oy + y, "cs0" if (x + y) % 2 == 0 else "fl0")


# --------------------------------------------------------------------------
# Braziers
# --------------------------------------------------------------------------

BRAZIER = [
    # 16 wide, from y 9 of the 16 x 32 column: a wide bronze bowl on three legs
    "..KKKKKKKKKKKK..",
    ".K332222222110K.",
    "K3322222221110K.",
    "K2221111111100K.",
    ".K22111111100K..",
    "..KK2111110KK...",
    "....KK1110K.....",
    "......K10K......",
    "......K10K......",
    ".....KK10KK.....",
    "....K21K100K....",
    "....K1K.K00K....",
    "...K1K...K0K....",
    "...K1K....K0K...",
    "..K1K.....K0K...",
    "..K1K......K0K..",
    ".K21K......K00K.",
    ".KKKK......KKKK.",
    "................",
]


def brazier():
    s = T.struct("brazier", "The bronze brazier, cold and lit", 2, 2, SEC,
                 walk=["XX", "XX"],
                 names={"cold_top": (0, 0), "cold": (0, 1), "lit_top": (1, 0), "lit": (1, 1)},
                 notes="A wide bronze bowl on a tripod, on the cave floor: `cold_top` over `cold`, "
                       "and lit, `lit_top` over `lit`. Swap both cells to light it: "
                       "METATILE_Trophonios_Brazier_*.")
    for cx in range(2):
        for cy in range(2):
            floor_under(s, cx, cy)
        shadow(s, cx * 16, 16, 14, rows=(27, 28), x0=1)
        T.put(s.M, cx * 16, 9, BRAZIER, {"K": "tink", "3": "bz2", "2": "bz2", "1": "bz1", "0": "bz0"})
        for x in range(3, 13):
            s.M.px(cx * 16 + x, 10, "bz2" if x % 4 else "bz1")
    # cold: grey ash heaped in the bowl, a charred stick
    T.put(s.M, 1, 6, ["....1111111....", "..11000000011..", ".1000000000001."],
          {"1": "as1", "0": "as0"})
    s.M.px(9, 5, "as0")
    s.M.px(10, 4, "as0")
    # lit: tall flames, red at the edges, white at the heart; sparks above
    T.put(s.M, 16 + 1, 0, [
        "..1.....1.....",
        "......1.......",
        "...1..21...1..",
        "......121.....",
        "..1..1221.1...",
        "..21.12321.1..",
        ".12211232121..",
        ".12233333221..",
        "1223333333221.",
        "1123333333211.",
    ], {"1": "fx0", "2": "fx1", "3": "fx2"})
    T.put(s.M, 16 + 5, 5, ["..3..", ".333.", "33333"], {"3": "fx3"})
    return s


# --------------------------------------------------------------------------
# The upper chamber: the throne of Mnemosyne, tablets, lamps, offerings
# --------------------------------------------------------------------------

def throne():
    s = T.struct("throne", "The throne of Mnemosyne", 1, 2, SEC, walk=["X", "X"],
                 names={"back": (0, 0), "seat": (0, 1)},
                 notes="A white stone chair on the paving: its high back (`back`) over the seat "
                       "(`seat`), where the pilgrims are set after the descent. The player is "
                       "placed on `seat` for beat 35C.")
    pave_under(s, 0, 0)
    pave_under(s, 0, 1)
    shadow(s, 0, 16, 15, rows=(29, 30), x0=1)
    T.put(s.M, 0, 0, [
        "................",
        "....KKKKKKKK....",
        "...K33333332K...",
        "..K3322222211K..",
        "..K3211111101K..",
        "..K3210000001K..",
        "..K3210330001K..",
        "..K3210320001K..",
        "..K3210000001K..",
        "..K3211111101K..",
        "..K3222222211K..",
        ".KKK222222211KKK",
        "K3332222222211K.",
        "K3222222222221K.",
        "K3211111111111K.",
        "K3210000000001K.",
        # the seat: a slab between the arms, the legs below
        "K3233333333331K.",
        "K3222222222221K.",
        "K3111111111111K.",
        "KKKKKKKKKKKKKKK.",
        ".K32K00000K21K..",
        ".K32K00000K21K..",
        ".K32K.....K21K..",
        ".K21K.....K10K..",
        ".KKKK.....KKKK..",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
    ], {"K": "tink", "3": "mb3", "2": "mb2", "1": "mb1", "0": "mb0"})
    return s


TABLET_SETS = {
    "tablets_a": [(1, 3, 5, 6), (8, 2, 6, 5), (3, 10, 4, 4), (9, 9, 5, 5)],
    "tablets_b": [(2, 2, 4, 5), (7, 4, 6, 6), (1, 9, 6, 5), (10, 10, 4, 4)],
}


def tablets():
    """Votive tablets on pegs in the chamber's north wall: what each pilgrim saw."""
    s = T.struct("tablets", "Votive tablets on the wall", 2, 1, SEC, walk=["XX"],
                 names={"a": (0, 0), "b": (1, 0)},
                 notes="Small wooden tablets hung on pegs on a face cell (the base row of a "
                       "face two tall): each one a pilgrim's account. `a` and `b` vary.")
    for cx, key in enumerate(("tablets_a", "tablets_b")):
        face_under(s, cx, 0)
        ox = cx * 16
        for (x, y, w, h) in TABLET_SETS[key]:
            # string from a peg
            s.M.px(ox + x + w // 2, y - 1, "rp0")
            s.M.px(ox + x + w // 2, y - 2, "wo0")
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    edge = yy in (y, y + h - 1) or xx in (x, x + w - 1)
                    s.M.px(ox + xx, yy, "wo0" if edge else ("rp1" if (xx + yy) % 2 else "rp0"))
            # scratched lines of writing
            for yy in range(y + 1, y + h - 1, 2):
                for xx in range(x + 1, x + w - 1):
                    if (xx * 3 + yy) % 4:
                        s.M.px(ox + xx, yy, "wo1")
    return s


def lamp():
    """A clay lamp burning in a niche cut in the face."""
    s = T.struct("lamp", "A lamp in a wall niche", 1, 1, SEC, walk=["X"], names={"lamp": (0, 0)},
                 notes="A niche in a face cell (base row of a two-tall face) with a burning clay "
                       "lamp: the priests' light in the upper chamber.")
    face_under(s, 0, 0)
    # the niche, cut dark into the rock (rock group, bottom layer)
    T.put(s.B, 3, 3, [
        "..00000000..",
        ".0000000000.",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "111111111111",
        "222222222222",
    ], {"0": "cp0", "1": "fc1", "2": "fc3"})
    T.put(s.M, 4, 3, [
        "....1.....",
        "...121....",
        "...232....",
        "....3.....",
        "..KKKKKK..",
        ".K011110K.",
    ], {"1": "fx1", "2": "fx2", "3": "fx3", "K": "tink", "0": "br0"})
    for x in range(5, 11):
        s.M.px(x, 8, "br1" if x % 2 else "br0")
    return s


def offerings():
    s = T.struct("offerings", "Bread offerings and honey cakes", 3, 1, SEC, walk=["XX."],
                 names={"bread": (0, 0), "cakes": (1, 0), "crumbs": (2, 0)},
                 notes="`bread` a basket heaped with round loaves, `cakes` honey cakes on a clay "
                       "dish (the pilgrims' gift for the snakes), `crumbs` old cake broken on "
                       "the floor (walkable).")
    for cx in range(3):
        floor_under(s, cx, 0)
    shadow(s, 0, 0, 12, rows=(14, 15), x0=2)
    shadow(s, 16, 0, 12, rows=(13, 14), x0=2)
    # the basket
    T.put(s.M, 1, 7, [
        ".KKKKKKKKKKKK.",
        "K00101010101K",
        "K0101010101K.",
        ".K01010100K..",
        "..KKKKKKKK...",
    ], {"K": "tink", "0": "br0", "1": "br1"})
    for (cx, cy) in ((4, 5), (8, 5), (12, 6), (6, 3), (10, 3)):
        m = T.ellipse_mask(16, 16, cx, cy, 2.6, 2.2)
        for y, x in np.argwhere(m):
            u = (x - cx) + (y - cy)
            s.M.px(x, y, "br2" if u < -1 else ("br1" if u < 2 else "br0"))
        s.M.px(cx - 1, cy - 1, "fx3")
    # the dish of honey cakes
    T.put(s.M, 16 + 1, 8, [
        "..KKKKKKKKKK..",
        ".K0000000000K.",
        "K000000000000K",
        ".KK00000000KK.",
        "...KKKKKKKK...",
    ], {"K": "tink", "0": "br0"})
    for (cx, cy) in ((5, 8), (10, 8), (7.5, 6)):
        m = T.ellipse_mask(16, 16, cx, cy, 2.5, 1.6)
        for y, x in np.argwhere(m):
            s.M.px(16 + x, y, "hn" if y <= cy - 1 else "br1")
        s.M.px(16 + int(cx), int(cy) - 1, "fx2")
    # crumbs
    for (x, y, c) in ((4, 5, "br1"), (5, 5, "br0"), (9, 9, "br2"), (10, 9, "br1"), (6, 11, "br1"),
                      (12, 4, "br0"), (3, 12, "br2"), (11, 12, "hn")):
        s.M.px(32 + x, y, c)
    return s


# --------------------------------------------------------------------------
# Ways in and out: the grille, the ladder, the stairs
# --------------------------------------------------------------------------

def grille():
    """The bronze grille from the precinct: an arch in the north wall with
    bars and daylight behind, and the cut steps below it (the warp)."""
    s = T.struct("grille", "The bronze grille and its steps", 1, 2, SEC, walk=["X", "."],
                 names={"arch": (0, 0), "steps": (0, 1)},
                 notes="In a face two tall under the cap: `arch` (the grille, daylight behind "
                       "its bars) over `steps` (cut steps up to it, walkable; "
                       "MB_NORTH_ARROW_WARP: the warp out to Lebadeia).")
    face_under(s, 0, 0, 2, 0, "c")
    face_under(s, 0, 1, 2, 1, "c")
    # daylight in the arch, behind the bars
    T.put(s.M, 2, 3, [
        "....111111....",
        "..1111111111..",
        ".111111111111.",
        ".111111111111.",
        "11111111111111",
        "11111111111111",
        "11111111111111",
        "10111111111101",
        "00111111111100",
        "00011111111000",
        "00011111111000",
        "00001111110000",
        "00001111110000",
    ], {"1": "dl1", "0": "dl0"})
    for x in (3, 6, 9, 12):
        for y in range(4, 16):
            s.M.px(x, y, "bz1")
            if y % 4 == 0:
                s.M.px(x, y, "bz2")
    for x in range(2, 14):
        s.M.px(x, 8, "bz1")
        s.M.px(x, 9, "bz2" if x % 2 else "bz1")
    T.put(s.M, 1, 2, [
        "....KKKKKK....",
        "..KK......KK..",
        ".K..........K.",
    ], {"K": "tink"})
    # the steps: three cut steps rising north, the top one lit by the day
    for y in range(16):
        for x in range(1, 15):
            step = y // 5
            c = ("mb3", "mb2", "mb1", "mb1")[step] if y % 5 != 4 else "mb0"
            if x in (1, 14):
                c = "tink"
            s.M.px(x, 16 + y, c)
    for x in range(2, 14):
        s.M.px(x, 16, "dl1" if x % 2 else "dl0")
    s.behaviors[(0, 1)] = "MB_NORTH_ARROW_WARP"
    return s


def ladder():
    """A rope ladder down the upper chamber's cliff (a face three tall with
    floor above), and its stakes on the floor at the top."""
    s = T.struct("ladder", "The rope ladder", 1, 4, SEC, walk=[".", ".", ".", "."],
                 names={"stakes": (0, 0), "top": (0, 1), "mid": (0, 2), "foot": (0, 3)},
                 notes="`stakes` (on the paving at the cliff's edge) over the ladder down a face "
                       "three tall with floor above: `top`, `mid`, `foot`. All walkable.")
    pave_under(s, 0, 0)
    for r in range(3):
        KIT.paint_face_cell(s, 0, 16 + r * 16, 3, r, "f", "M", L=s.B)
    # two wooden stakes and the ropes tied to them
    T.put(s.M, 2, 6, [
        ".KK......KK.",
        "K21K....K21K",
        "K21K....K21K",
        "K21K....K21K",
        "K21K....K21K",
        ".KK......KK.",
    ], {"K": "tink", "2": "wo2", "1": "wo1"})
    for y in range(12, 64):
        s.M.px(4, y, "rp0")
        s.M.px(5, y, "rp1")
        s.M.px(10, y, "rp1")
        s.M.px(11, y, "rp0")
        if y % 5 == 2 and y > 18:
            for x in range(5, 11):
                s.M.px(x, y, "wo2")
            for x in range(5, 11):
                s.M.px(x, y + 1, "wo0")
    return s


def stairs():
    s = T.struct("stairs", "Stairs down and up", 2, 2, SEC, walk=["X.", ".."],
                 names={"up_arch": (0, 0), "up": (0, 1), "down": (1, 1), "down_rim": (1, 0)},
                 notes="`down` steps cut into the floor going down into the dark (MB_LADDER: the "
                       "warp to the floor below); `up` steps cut into a face's base going up, "
                       "under `up_arch` (the face's top row): MB_LADDER, the warp up. "
                       "`down_rim` is plain floor beside it.")
    face_under(s, 0, 0, 2, 0, "c")
    face_under(s, 0, 1, 2, 1, "c")
    floor_under(s, 1, 0)
    floor_under(s, 1, 1)
    # up: an opening in the face, steps climbing into black
    T.put(s.B, 1, 4, [
        "....000000....",
        "..0000000000..",
        ".000000000000.",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
    ], {"0": "cp0"})
    for y in range(16):
        for x in range(2, 14):
            k = y // 4
            c = ("fc1", "fc2", "fc3", "fc4")[k] if y % 4 != 0 else "fc0"
            s.B.px(x, 16 + y, c)
        s.B.px(1, 16 + y, "fc0")
        s.B.px(14, 16 + y, "fc0")
    s.behaviors[(0, 1)] = "MB_LADDER"
    # down: a dark pit with steps descending north to south... into the black
    T.put(s.B, 16 + 1, 16 + 1, [
        "KKKKKKKKKKKKKK",
        "K544444444444K",
        "K333333333333K",
        "K111111111111K",
        "K433333333333K",
        "K222222222222K",
        "K000000000000K",
        "K322222222222K",
        "K111111111111K",
        "KKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKK",
        ".KKKKKKKKKKKK.",
    ], {"K": "tink", "5": "fl5", "4": "fl4", "3": "fl3", "2": "fl2", "1": "fl1", "0": "cs0"})
    s.behaviors[(1, 1)] = "MB_LADDER"
    return s


# --------------------------------------------------------------------------
# Water features: the spring, the outlet, the sink, the black pool
# --------------------------------------------------------------------------

def spring():
    s = T.struct("spring", "The spring from the rock", 1, 2, SEC, walk=["X", "X"],
                 names={"seep": (0, 0), "basin": (0, 1)},
                 notes="`seep` (the base row of a face two tall) with cold water running down "
                       "the rock, over `basin`, a rock basin on the floor it fills: B2F's "
                       "midpoint rest.")
    face_under(s, 0, 0)
    floor_under(s, 0, 1)
    # damp rock around the trickle (rock group, bottom layer)
    for y in range(16):
        for x in range(4, 12):
            if (x + y) % 3 and abs(x - 8) < 3 + y // 6:
                s.B.px(x, y, "dm0" if (x + y) % 2 else "dm1")
    for y in range(2, 16):
        x = 7 + (1 if (y // 3) % 2 else 0)
        s.M.px(x, y, "wa4")
        s.M.px(x + 1, y, "fm" if y % 4 == 0 else "wa3")
    # the basin
    T.put(s.M, 1, 17, [
        "...KKKKKKKK...",
        ".KK32222223KK.",
        "K322111111223K",
        "K21wwwwwwww12K",
        "K2wwwvvvvwww2K",
        "K2wwvvwwvvww2K",
        "K21wwwwwwww12K",
        ".K2111111112K.",
        "..KK222222KK..",
        "....KKKKKK....",
    ], {"K": "tink", "3": "fc3", "2": "fc2", "1": "fc1", "w": "wa2", "v": "wa4"})
    for x in (7, 8):
        s.M.px(x, 16, "wa4")
        s.M.px(x, 17, "fm")
    s.M.px(6, 20, "fm")
    s.M.px(9, 21, "fm")
    return s


def outlet():
    s = T.struct("outlet", "Where the stream comes out of the rock", 1, 1, SEC, walk=["X"],
                 names={"outlet": (0, 0)},
                 notes="The base row of a face two tall, with a low black arch the stream runs "
                       "out of. Put the stream's first water cell below it.")
    face_under(s, 0, 0)
    T.put(s.B, 1, 5, [
        "....000000....",
        "..0000000000..",
        ".000000000000.",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
        "00000000000000",
    ], {"0": "cp0"})
    for y in range(10, 16):
        for x in range(2, 14):
            if (x + y * 2) % 5:
                s.M.px(x, y, "wa2" if y < 13 else "wa3")
            else:
                s.M.px(x, y, "fm" if y > 12 else "wa1")
    return s


def sink():
    s = T.struct("sink", "Where the stream goes into the ground", 1, 1, SEC, walk=["X"],
                 names={"sink": (0, 0)},
                 notes="A black hole in the floor the stream pours into from the east. Put it at "
                       "the west end of the stream; blocked.")
    for y in range(16):
        for x in range(16):
            f = T.floor_px(x, y)
            s.B.px(x, y, KIT.WATER_FLOOR.get(f, f))
    for y in range(4, 12):
        for x in range(6, 16):
            s.B.px(x, y, KIT.water_px(x, y))
    m = T.ellipse_mask(16, 16, 7, 8, 6.5, 5.5)
    for y, x in np.argwhere(m):
        s.B.px(x, y, "bk")
    for y, x in np.argwhere(T.ring(m)):
        s.B.px(x, y, "wa1" if x > 7 else "fc1")
    for y, x in np.argwhere(T.halo(m)):
        if x <= 9:
            s.B.px(x, y, "fc2")
    for y in range(5, 11):
        s.B.px(13, y, "fm" if y % 2 else "wa4")
    return s


def pool():
    """The round black pool that reflects nothing."""
    s = T.struct("pool", "The black pool", 3, 3, SEC, walk=["XXX", "XXX", "XXX"],
                 names={f"{x}{y}": (x, y) for y in range(3) for x in range(3)},
                 notes="A still round pool in a stone rim, black even in torchlight: it "
                       "reflects nothing. 3 x 3, blocked; the rim's corners let the floor show.")
    for y in range(48):
        for x in range(48):
            f = T.floor_px(x, y)
            s.B.px(x, y, KIT.WATER_FLOOR.get(f, f))
    m = T.ellipse_mask(48, 48, 23.5, 23.5, 21, 19)
    inner = T.ellipse_mask(48, 48, 23.5, 23.5, 17.5, 15.5)
    for y, x in np.argwhere(m & ~inner):
        u = (x - 23.5) / 21 + (y - 23.5) / 19
        s.B.px(x, y, "fc3" if u < -0.4 else ("fc2" if u < 0.5 else "fc1"))
    for y, x in np.argwhere(T.ring(m)):
        s.B.px(x, y, "tink" if y > 23 else "fc1")
    for y, x in np.argwhere(inner):
        s.B.px(x, y, "bk")
    for y, x in np.argwhere(T.ring(inner)):
        s.B.px(x, y, "wa0" if y < 20 else "bk")
    # rim stones: joints
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x = int(23.5 + math.cos(a) * 19.3)
        y = int(23.5 + math.sin(a) * 17.3)
        s.B.px(x, y, "fc1")
        s.B.px(x + 1, y, "fc1")
    return s


def hole():
    """The oracle's hole: round and black, the size of a bread oven's mouth."""
    s = T.struct("hole", "The hole in the oracle's floor", 2, 2, SEC, walk=["XX", "XX"],
                 names={"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)},
                 notes="A round black hole in the middle of the oracle's chamber, with a worn lip "
                       "like a bread oven's mouth. 2 x 2, blocked; the descent's last step.")
    for cy in range(2):
        for cx in range(2):
            floor_under(s, cx, cy)
    outer = T.ellipse_mask(32, 32, 15.5, 16.5, 12.5, 11)
    mid = T.ellipse_mask(32, 32, 15.5, 17.5, 10, 8.5)
    inner = T.ellipse_mask(32, 32, 15.5, 18.5, 8, 6.5)
    for y, x in np.argwhere(outer):
        u = (x - 15.5) / 12.5 + (y - 16.5) / 11
        s.B.px(x, y, "fl5" if u < -0.6 else ("fl4" if u < 0.2 else "fl3"))
    for y, x in np.argwhere(mid):
        s.B.px(x, y, "fl0" if y < 16 else "fl1")
    for y, x in np.argwhere(inner):
        s.B.px(x, y, "tink")
    for y, x in np.argwhere(mid & ~inner):
        if y < 14:
            s.B.px(x, y, "cs0")
    for y, x in np.argwhere(T.ring(outer)):
        s.B.px(x, y, "fl1" if y > 16 else "fl4")
    return s


# --------------------------------------------------------------------------
# The pilgrims' chalk handprints
# --------------------------------------------------------------------------

def prints():
    """Chalk hands: on a face's base row (`one`, `two`, fingers `N` `E` `S` `W`)
    and on the floor (`fN` `fE` `fS` `fW`). Faint in torchlight; the glow copy
    shows them alone when the torch is doused."""
    wall = ["one", "two", "N", "E", "S", "W"]
    flo = ["fN", "fE", "fS", "fW"]
    names = {k: (i, 0) for i, k in enumerate(wall)}
    names.update({k: (i, 1) for i, k in enumerate(flo)})
    s = T.struct("prints", "The pilgrims' chalk handprints", 6, 2, SEC,
                 walk=["XXXXXX", "......"], names=names,
                 notes="Chalk hands in the glow paint (`ch1`, `ch2`). Wall prints sit on the base "
                       "row of a face two tall: `one`, `two` (a big hand and a smaller one), "
                       "and fingers pointing `N`, `E`, `S`, `W`. Floor prints: `fN` `fE` `fS` "
                       "`fW`, walkable.")
    for i, k in enumerate(wall):
        face_under(s, i, 0)
        ox = i * 16
        if k == "one":
            T.chalk_hand(s.B, ox + 4, 3, "one")
        elif k == "two":
            T.chalk_hand(s.B, ox + 1, 2, "one")
            small = T.Layer(8, 8)
            T.chalk_hand(small, 0, 0, "one")
            # the second, smaller hand: every other pixel of the first, lower right
            for y in range(0, 8, 2):
                for x in range(0, 8, 2):
                    if small.get(x, y):
                        s.B.px(ox + 9 + x // 2 + 1, 8 + y // 2 + 1, "ch2")
                        s.B.px(ox + 9 + x // 2 + 1, 8 + y // 2 + 2, "ch1")
        else:
            T.chalk_hand(s.B, ox + 4, 3, k)
    for i, k in enumerate(flo):
        ox = i * 16
        floor_under(s, i, 1)
        T.chalk_hand(s.B, ox + 4, 16 + 4, k[1])
    return s


# --------------------------------------------------------------------------
# The snake's cleft
# --------------------------------------------------------------------------

def cleft():
    s = T.struct("cleft", "The snake's cleft", 2, 1, SEC, walk=[".."],
                 names={"coils": (0, 0), "empty": (1, 0)},
                 notes="A low cleft across a passage one cell wide: `coils` with something very "
                       "large lying in it (the snake object, invisible, blocks it until fed), "
                       "`empty` once it has gone back into the rock. Walkable art: the object "
                       "does the blocking.")
    for cx in range(2):
        ox = cx * 16
        floor_under(s, cx, 0, 2)
        # the cleft: a dark fissure across the cell
        for x in range(16):
            y0 = 6 + (1 if (x // 4) % 2 else 0)
            for y in range(y0, y0 + 4):
                s.B.px(ox + x, y, "tink" if y in (y0 + 1, y0 + 2) else "cs0")
            s.B.px(ox + x, y0 - 1, "fl4" if x % 3 else "fl3")
    # the coils: thick loops of scaled body, no head
    body = np.zeros((16, 16), bool)
    for (cx, cy, rx, ry) in ((4.5, 8.5, 4.2, 3.5), (11.5, 8, 4.4, 3.7), (8, 5.5, 3.8, 2.8),
                             (8, 11, 4.0, 2.5)):
        body |= T.ellipse_mask(16, 16, cx, cy, rx, ry)
    hole = np.zeros((16, 16), bool)
    for (cx, cy, rx, ry) in ((4.5, 8.5, 1.6, 1.2), (11.5, 8, 1.8, 1.3)):
        hole |= T.ellipse_mask(16, 16, cx, cy, rx, ry)
    body &= ~hole
    for y, x in np.argwhere(body):
        u = (x - 8) / 8 + (y - 7) / 7
        scale = (x + 2 * y) % 4 == 0
        c = "sn3" if u < -0.5 else ("sn2" if u < 0.3 else "sn1")
        if scale:
            c = {"sn3": "sn4", "sn2": "sn3", "sn1": "sn2"}[c]
        s.M.px(x, y, c)
    for y, x in np.argwhere(T.ring(body)):
        s.M.px(x, y, "sn0" if y > 6 else "sn1")
    for y, x in np.argwhere(hole):
        s.M.px(x, y, "cp0")
    return s


# --------------------------------------------------------------------------
# Rocks, stalagmites, bones, webs, the dig spot
# --------------------------------------------------------------------------

def rocks():
    s = T.struct("rocks", "Rocks and stalagmites", 4, 1, SEC, walk=["XXX."],
                 names={"stal": (0, 0), "stal_pair": (1, 0), "boulder": (2, 0), "scree": (3, 0)},
                 notes="On the floor: `stal` a stalagmite, `stal_pair` two, `boulder` a fallen "
                       "block (all blocked); `scree` loose stones (walkable).")
    for cx in range(4):
        floor_under(s, cx, 0)

    def spike(ox, cx, base, top, w):
        for y in range(top, base + 1):
            t = (y - top) / max(base - top, 1)
            half = 0.5 + t * w
            for x in range(16):
                d = x - cx
                if -half <= d <= half:
                    c = "fc4" if d < -half / 3 else ("fc3" if d < half / 3 else "fc1")
                    if y == base:
                        c = "fc0"
                    s.M.px(ox + x, y, c)
            s.M.px(ox + int(cx - half), y, "tink")
            s.M.px(ox + int(cx + half + 0.5), y, "tink")
        s.M.px(ox + int(cx), top - 1, "tink")

    shadow(s, 0, 0, 12, rows=(14, 15), x0=2)
    spike(0, 7.5, 14, 2, 4.2)
    shadow(s, 16, 0, 13, rows=(14, 15), x0=1)
    spike(16, 5, 14, 4, 3.4)
    spike(16, 11, 14, 7, 2.8)
    shadow(s, 32, 0, 14, rows=(14, 15), x0=1)
    m = T.ellipse_mask(16, 16, 8, 8.5, 6.8, 5.8)
    for y, x in np.argwhere(m):
        u = (x - 8) / 6.8 + (y - 8.5) / 5.8
        s.M.px(32 + x, y, "fc4" if u < -0.7 else ("fc3" if u < 0.1 else ("fc2" if u < 0.8 else "fc1")))
    for y, x in np.argwhere(T.ring(m)):
        s.M.px(32 + x, y, "tink")
    for (x, y) in ((5, 7), (6, 8), (7, 9), (8, 9)):
        s.M.px(32 + x, y, "fc1")
    for (x, y) in ((3, 4), (9, 3), (12, 9), (5, 12), (10, 13), (2, 9), (13, 3)):
        s.M.px(48 + x, y, "fc3")
        s.M.px(48 + x + 1, y, "fc2")
        s.M.px(48 + x, y + 1, "fc1")
        s.M.px(48 + x + 1, y + 1, "tink")
    return s


def bones_webs():
    s = T.struct("lair", "Bones and webs", 4, 1, SEC, walk=["..XX"],
                 names={"bones": (0, 0), "strands": (1, 0), "web_face": (2, 0), "web_corner": (3, 0)},
                 notes="`bones` old bones on the floor and `strands` loose web across it "
                       "(walkable); `web_face` a cobweb over a face's base row, `web_corner` a "
                       "web in the top corner of a face's top row under the cap (both blocked).")
    floor_under(s, 0, 0, 1)
    floor_under(s, 1, 0)
    face_under(s, 2, 0)
    face_under(s, 3, 0, 2, 0, "c")
    T.put(s.M, 1, 4, [
        ".11......1.....",
        "1001....101....",
        ".1.10..1.......",
        "....1001.......",
        ".....11...11...",
        "..........1001.",
        "...11......11..",
        "..1001.........",
        "...11..........",
    ], {"1": "bn0", "0": "bn1"})

    def web(L, ox, oy, cx, cy, r, spokes=7):
        import math
        for k in range(spokes):
            a = math.pi * 2 * k / spokes + 0.3
            for t in range(1, r + 1):
                L.px(ox + int(cx + math.cos(a) * t), oy + int(cy + math.sin(a) * t), "wb1" if t % 3 else "wb0")
        for rr in range(3, r, 3):
            for k in range(spokes * 3):
                a = math.pi * 2 * k / (spokes * 3)
                L.px(ox + int(cx + math.cos(a) * rr), oy + int(cy + math.sin(a) * rr * 0.85), "wb0")
    for (x0, y0, x1, y1) in ((0, 3, 15, 11), (0, 12, 10, 2), (4, 15, 15, 6)):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            s.M.px(16 + x0 + (x1 - x0) * i // n, y0 + (y1 - y0) * i // n, "wb0" if i % 4 else "wb1")
    web(s.M, 32, 0, 8, 7, 8, 8)
    web(s.M, 48, 0, 4, 3, 10, 6)
    return s


def dig():
    s = T.struct("dig", "Turned earth on the cave floor", 1, 1, SEC, walk=["."],
                 names={"dig": (0, 0)},
                 notes="A fixed dig spot on the floor (walkable): the earth here has been turned.")
    floor_under(s, 0, 0)
    m = T.ellipse_mask(16, 16, 8, 8.5, 6, 4.5)
    for y, x in np.argwhere(m):
        s.B.px(x, y, "fl1" if (x + y) % 3 else ("fl3" if (x * y) % 2 else "fl0"))
    for y, x in np.argwhere(T.ring(m)):
        s.B.px(x, y, "fl3" if y < 8 else "fl0")
    return s


def build():
    return [brazier(), throne(), tablets(), lamp(), offerings(), grille(), ladder(), stairs(),
            spring(), outlet(), sink(), pool(), hole(), prints(), cleft(), rocks(), bones_webs(),
            dig()]
