"""Aegina Town's buildings and street pieces for gTileset_Aegina: the inn on the
waterfront, the mint's strongroom front, old Aiakides's house, the north gate to
the Aphaia Road (open, and its leaves shut for the voyage night) and the turtle
mosaic in the mint's square.

Aegina's houses are not Akti's whitewashed cubes: honey-ochre plaster under
pitched terracotta roofs, with sea-green doors and shutters. The mint is bare
rusticated ashlar under a flat parapet, a bronze turtle stater over its door.
"""
from __future__ import annotations

import math

from aegina_lib import Struct, ground

SEC = "aegina"


# --------------------------------------------------------------------------
# Painters (group "house" unless noted)
# --------------------------------------------------------------------------

def tiled_roof(L, x, y, w, h, chimney=None):
    """A pitched terracotta roof seen from the south: the ridge along the top,
    courses of tiles running down to the eave, cover tiles in ridges lit on their
    left. (x, y, w, h) is the roof's box; the eave is its bottom row."""
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            m = (xx - x) % 4
            c = "tc1"
            if m == 0:
                c = "tc2"
            elif m == 3:
                c = "tc0"
            if (yy - 3) % 4 == 3:
                c = "tc0" if m == 3 else "tc1"     # the lower lip of each course
            if (yy - 3) % 4 == 0 and m in (1, 2):
                c = "tc2"
            L.px(xx, yy, c)
    # the ridge: rounded capping tiles catching the sun
    L.hline(x, x + w - 1, y, "ink")
    L.hline(x + 1, x + w - 2, y + 1, "tc3")
    L.hline(x + 1, x + w - 2, y + 2, "tc2")
    for xx in range(x + 2, x + w - 2, 8):
        L.px(xx, y + 2, "tc0")
    # the gable ends: a dark verge, the eave's shadow line and antefixes
    L.vline(x, y, y + h - 1, "ink")
    L.vline(x + w - 1, y, y + h - 1, "ink")
    L.vline(x + 1, y + 1, y + h - 2, "tc2")
    L.vline(x + w - 2, y + 1, y + h - 2, "tc0")
    L.hline(x, x + w - 1, y + h - 1, "ink")
    for xx in range(x + 2, x + w - 2, 4):
        L.px(xx, y + h - 2, "tc3")
    if chimney:
        cx, cy = chimney
        L.blit([" kkkk ", "k3322k", "k2kk1k", "k2211k", " k21k ", " kkkk "],
               {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"}, cx, cy)


def plaster(L, x, y, w, h, eave_shadow=True, base=True):
    """Honey-ochre plaster: lit on the left corner, shaded on the right, a few
    patches where it has worn, a stone plinth along the foot."""
    # flat, like aethos's and kalliste's walls: plain wall tiles then repeat
    L.rect(x, y, w, h, "oc2")
    L.vline(x, y, y + h - 1, "dk")
    L.vline(x + w - 1, y, y + h - 1, "dk")
    L.vline(x + 1, y, y + h - 1, "oc3")
    L.vline(x + w - 2, y, y + h - 1, "oc1")
    if eave_shadow:
        L.hline(x + 1, x + w - 2, y, "oc0")
        L.hline(x + 1, x + w - 2, y + 1, "oc1")
    if base:
        L.hline(x + 1, x + w - 2, y + h - 4, "oc1")
        L.rect(x + 1, y + h - 3, w - 2, 2, "oc0")
        L.hline(x, x + w - 1, y + h - 1, "dk")
        for xx in range(x + 3, x + w - 2, 8):
            L.px(xx, y + h - 3, "dk")


SHUTTERS = [   # a window between sea-green shutters folded back, 16 x 12
    "kkkk kkkkkk kkkk",
    "k21k kddddk k21k",
    "k10k kd  dk k10k",
    "k21k kd  dk k21k",
    "k10k kkkkkk k10k",
    "k21k kd  dk k21k",
    "k10k kd  dk k10k",
    "k21k kddddk k21k",
    "kkkk kkkkkk kkkk",
    "     o3333o     ",
    "      1111      ",
]
SHUTTERS_KEY = {"k": "ink", "2": "te2", "1": "te1", "0": "te0", "d": "dk", " ": None,
                "o": "oc0", "3": "oc3"}

DOOR = [       # a sea-green plank door, 12 x 20
    "kkkkkkkkkkkk",
    "k2111kk2111k",
    "k1001kk1001k",
    "k1001kk1001k",
    "k1001kk1001k",
    "k1111kk1111k",
    "k2111kk2111k",
    "k1001kk1001k",
    "k1001kk1001k",
    "k1001kk1031k",
    "k1001kk1001k",
    "k1111kk1111k",
    "k2111kk2111k",
    "k1001kk1001k",
    "k1001kk1001k",
    "k1001kk1001k",
    "k1001kk1001k",
    "k1111kk1111k",
    "k0000kk0000k",
    "kkkkkkkkkkkk",
]
DOOR_KEY = {"k": "ink", "2": "te2", "1": "te1", "0": "te0", "3": "oc3"}


def shutters(L, x, y, open_=True):
    rows = SHUTTERS
    if not open_:
        rows = [r.replace(" ", "1") for r in rows]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == " ":
                if 1 <= j <= 7 and 6 <= i <= 9:
                    L.px(x + i, y + j, "ink")
            else:
                L.px(x + i, y + j, SHUTTERS_KEY[ch])
    # a glimpse of the dark room inside, a lamp
    for j in range(2, 8):
        for i in range(6, 10):
            if j != 4:
                L.px(x + i, y + j, "dk" if (i + j) % 3 else "ink")


def door(L, x, y):
    """The sea-green door with a stone threshold under it."""
    L.hline(x - 1, x + 12, y - 1, "oc0")
    L.blit(DOOR, DOOR_KEY, x, y)
    L.hline(x - 2, x + 13, y + 20, "w0")
    L.hline(x - 2, x + 13, y + 21, "oc1")


def amphora(L, x, y):
    """A tall storage amphora standing against a wall, 6 x 13."""
    L.blit(["  kk  ", " k32k ", "  k2k ", " k332k", "k33221k", "k32221k", "k32221k",
            "k32211k", " k2211k", " k2211k", "  k21k ", "  k1k  ", "   k   "],
           {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"}, x, y)


# --------------------------------------------------------------------------
# The inn
# --------------------------------------------------------------------------

def inn():
    """Endeis's inn: two storeys of ochre plaster under a tiled roof, a wooden
    gallery of guest rooms along the upper floor, a turtle sign hung from it,
    amphorae and a bench by the big sea-green door."""
    s = Struct("inn", "The inn on the waterfront", 5, 4, SEC,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               notes="Endeis's inn: two storeys of honey-ochre plaster under a pitched "
                     "terracotta roof, a wooden gallery of guest rooms along the upper floor, a "
                     "painted sea-turtle sign hung from it, amphorae and a bench by the "
                     "sea-green door. Door: row 3, middle column (MB_NON_ANIMATED_DOOR). Put "
                     "its sign's bg event on the cell right of the door.")
    L = s.B
    W = 80
    tiled_roof(L, 0, 0, W, 20)
    plaster(L, 0, 20, W, 44)
    # upper floor: two shuttered doors onto the gallery (placed symmetrically, so
    # the right half's tiles are mostly the left's, flipped)
    for x0 in (10, 54):
        shutters(L, x0, 24)
    # the gallery: a floor beam, posts down to the ground, a railing of turned balusters
    L.hline(1, W - 2, 35, "wd1")
    L.hline(1, W - 2, 36, "tc0")
    L.hline(1, W - 2, 37, "ink")
    L.hline(1, W - 2, 29, "oc0")
    L.hline(1, W - 2, 30, "wd1")
    for xx in range(2, W - 2):                       # balusters, symmetric about the middle
        if xx % 4 in (1, 2):
            L.vline(xx, 31, 34, "oc0")
            L.px(xx, 33, "wd1")
    L.hline(1, W - 2, 38, "oc1")                    # the gallery's shadow on the wall
    for x0, cols in ((3, ("ink", "wd1", "oc0", "ink")), (W - 7, ("ink", "oc0", "wd1", "ink"))):
        for i, c in enumerate(cols):                 # posts, mirror images
            L.vline(x0 + i, 30, 61, c)
        L.hline(x0 - 1, x0 + 4, 61, "ink")
    # ground floor: shuttered windows either side of the door
    shutters(L, 10, 42)
    shutters(L, 54, 42)
    door(L, 34, 41)
    # The front is symmetric: the right half is the left half mirrored, so its
    # tiles are the left's flipped (Porytiles stores them once). The sign, the
    # amphorae, the bench and the chimney go on after.
    L.a[:, 40:80] = L.a[:, 0:40][:, ::-1]
    tiled_roof_chimney = (60, 3)
    L.blit([" kkkk ", "k3322k", "k2kk1k", "k2211k", " k21k ", " kkkk "],
           {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"}, *tiled_roof_chimney)
    # the sign: a board with a sea turtle, hung on two chains from the gallery
    L.vline(51, 38, 40, "dk")
    L.vline(62, 38, 40, "dk")
    L.blit(["kkkkkkkkkkkkkk",
            "k33333333333dk",
            "k33333kk3333dk",
            "k3k333k1k333dk",
            "k33kk01110k3dk",
            "k333k02120k3dk",
            "k33kk01110k3dk",
            "k3k333k1k333dk",
            "k33333kk3333dk",
            "kkkkkkkkkkkkkk"],
           {"k": "ink", "3": "oc3", "d": "oc1", "1": "te1", "0": "te0", "2": "te2"}, 50, 41)
    # amphorae by the door, a bench by the right-hand window
    amphora(L, 22, 49)
    amphora(L, 27, 50)
    L.rect(62, 56, 12, 2, "oc0")
    L.hline(62, 73, 56, "oc1")
    L.hline(62, 73, 58, "ink")
    L.vline(63, 58, 61, "wd1")
    L.vline(72, 58, 61, "wd1")
    return s


# --------------------------------------------------------------------------
# The mint (groups "stone" and "wood")
# --------------------------------------------------------------------------

def ashlar(L, x, y, w, h):
    """Rusticated ashlar: big blocks with chiselled margins, phase-locked to 16 px."""
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            course = yy // 8
            off = 8 if course % 2 else 0
            bx, by = (xx + off) % 16, yy % 8
            if bx == 15 or by == 7:
                c = "sk"
            elif bx == 0 or by == 0:
                c = "s4"
            elif bx == 14 or by == 6:
                c = "s1"
            else:
                c = "s3" if (bx, by) not in ((4, 3), (9, 2), (11, 4)) else "s2"
            L.px(xx, yy, c)


def mint():
    """Pheidon's mint, the strongroom: bare rusticated ashlar under a flat
    parapet, barred slits, and over the iron-bound door a bronze plaque struck
    with the island's sea turtle. A slot in the door lets coins out."""
    s = Struct("mint", "The mint's strongroom front", 3, 4, SEC,
               walk=["XXX", "XXX", "XXX", "XDX"],
               notes="Pheidon's strongroom: rusticated limestone ashlar under a flat parapet, "
                     "two barred slit windows, and over the iron-bound door a bronze plaque "
                     "with the sea turtle of Aegina's coins. A slot in the door lets coins out "
                     "and nothing in. Door: row 3, middle column (MB_NON_ANIMATED_DOOR). Put "
                     "the plaque's bg event on the door's left or right.")
    B = s.B
    W = 48
    # the flat roof seen over its parapet, and a dentil cornice
    B.rect(0, 0, W, 6, "s4")
    B.hline(0, W - 1, 0, "sk")
    B.hline(1, W - 2, 1, "s5")
    B.hline(1, W - 2, 5, "s2")
    B.rect(2, 2, W - 4, 3, "s3")
    B.vline(0, 0, 63, "sk")
    B.vline(W - 1, 0, 63, "sk")
    B.rect(1, 6, W - 2, 3, "s5")
    B.hline(1, W - 2, 8, "s3")
    for xx in range(1, W - 1):                    # dentils
        B.px(xx, 9, "s4" if xx % 3 else "sk")
        B.px(xx, 10, "s2" if xx % 3 else "sk")
    B.hline(1, W - 2, 11, "sk")
    ashlar(B, 1, 12, W - 2, 52)
    B.vline(1, 12, 63, "s4")
    B.vline(W - 2, 12, 63, "s1")
    # a stepped plinth
    B.hline(1, W - 2, 60, "s4")
    B.rect(1, 61, W - 2, 2, "s2")
    B.hline(0, W - 1, 63, "sk")
    # barred slit windows, high up
    for x0 in (5, 35):
        B.rect(x0, 26, 8, 12, "sk")
        B.vline(x0 - 1, 25, 38, "s4")
        B.hline(x0 - 1, x0 + 8, 25, "s4")
        B.hline(x0 - 1, x0 + 8, 38, "s5")
        for xx in (x0 + 2, x0 + 5):
            B.vline(xx, 26, 37, "wt1")
        B.hline(x0, x0 + 7, 31, "wt1")
    # symmetric about the door: the right half mirrors the left (shared tiles)
    B.a[:, 24:48] = B.a[:, 0:24][:, ::-1]
    # the bronze plaque: a square plate with the turtle stater struck on it
    M = s.M
    M.blit(["kkkkkkkkkkkkkkkk",
            "kGGGGGGGGGGGGGgk",
            "kGgggggbbggggggk",
            "kGggggbggbgggggk",
            "kGgggbgGGgbggggk",
            "kGggbgGggGgbgggk",
            "kGgbgGgGgGgGbggk",
            "kGgbGgGGgGgGbggk",
            "kGgbgGgGgGgGbggk",
            "kGggbgGggGgbgggk",
            "kGgggbgGGgbggggk",
            "kGggggbggbgggggk",
            "kGgggggbbggggggk",
            "kGgggggggggggggk",
            "kgbbbbbbbbbbbbbk",
            "kkkkkkkkkkkkkkkk"], {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 16, 16)
    # the turtle on it: shell, head and flippers in bright bronze over the coin
    M.blit(["   G    ", "  GGG   ", " gGgGg  ", "GgGgGgG ", " gGgGg  ", "  GGG   ", " G   G  "],
           {"G": "g1", "g": "br"}, 20, 20)
    # the door: oak bound in iron, studded, with the coin slot
    door_rows = ["kkkkkkkkkkkkkkkk",
                 "k2333333333332kk",
                 "k3k2222kk2222k2k",
                 "k3211111111112ik",
                 "k32111i11i1112ik",
                 "k3211111111112ik",
                 "kiiiiiiiiiiiiiik",
                 "k3211111111112ik",
                 "k32111kkkk1112ik",
                 "k3211111111112ik",
                 "k32111i11i1112ik",
                 "k3211111111112ik",
                 "kiiiiiiiiiiiiiik",
                 "k3211111111112ik",
                 "k32111i11i1112ik",
                 "k3211111111112ik",
                 "k3211111111112ik",
                 "k32111i11i1112ik",
                 "kiiiiiiiiiiiiiik",
                 "k3211111111112ik",
                 "k3211111111112ik",
                 "k0000000000000kk",
                 "kkkkkkkkkkkkkkkk",
                 "kwwwwwwwwwwwwwwk"]
    M.blit(door_rows, {"k": "ink", "3": "wd3", "2": "wd2", "1": "wd1", "0": "wd0", "i": "br",
                       "w": "w0"}, 16, 40)
    return s


# --------------------------------------------------------------------------
# Aiakides's house
# --------------------------------------------------------------------------

def aiakides_house():
    """Old Aiakides's house up the lane: small and plain, ochre plaster under a
    tiled roof, his bronze shield and spear hung by the door, herbs in a pot."""
    s = Struct("house_aiakides", "Aiakides's house", 3, 3, SEC,
               walk=["XXX", "XXX", "XDX"],
               notes="A small house up a lane: ochre plaster under a pitched terracotta roof, "
                     "a sea-green door, one shuttered window, and the old soldier's bronze "
                     "shield and spear hung on the wall. Door: row 2, middle column "
                     "(MB_NON_ANIMATED_DOOR).")
    L = s.B
    W = 48
    tiled_roof(L, 0, 0, W, 17)
    plaster(L, 0, 17, W, 31)
    shutters(L, 2, 24)              # at the inn's windows' place in their tiles: shared
    door(L, 18, 25)
    # the shield: a round hoplite shield in bronze (copper tones), an ant on its face
    sh = ["   kkkkk   ",
          "  k32222k  ",
          " k3221112k ",
          "k322100112k",
          "k321kk0012k",
          "k3210kk012k",
          "k3210kk012k",
          "k221000112k",
          " k2211112k ",
          "  k22222k  ",
          "   kkkkk   "]
    # the spear behind it, leaning
    for k in range(26):
        L.px(44 - k // 5, 19 + k, "wd1")
    L.px(45, 18, "w0")
    L.px(45, 19, "dk")
    L.blit(sh, {"k": "ink", "3": "oc3", "2": "tc3", "1": "tc2", "0": "tc1"}, 33, 22)
    # a pot of thyme by the door
    L.blit(["  1 2 1 ", " 21212  ", "  kkkk  ", " k3221k ", " k3221k ", "  k21k  ",
            "  kkkk  "], {"k": "ink", "3": "tc3", "2": "tc2", "1": "te1"}, 31, 38)
    return s


# --------------------------------------------------------------------------
# The north gate (groups "stone" and "wood")
# --------------------------------------------------------------------------

def pier(L, x, y, h):
    """A gate pier of ashlar, 12 wide, with a moulded cap."""
    for yy in range(y + 4, y + h):
        for xx in range(x, x + 12):
            course = (yy - y) // 6
            bx = (xx - x + (6 if course % 2 else 0)) % 12
            c = "s3"
            if (yy - y) % 6 == 5:
                c = "s1"
            elif bx == 11:
                c = "s1"
            elif bx == 0:
                c = "s4"
            L.px(xx, yy, c)
        L.px(x, yy, "sk")
        L.px(x + 1, yy, "s5")
        L.px(x + 10, yy, "s1")
        L.px(x + 11, yy, "sk")
    L.rect(x - 1, y, 14, 4, "s4")
    L.hline(x - 1, x + 12, y, "sk")
    L.hline(x, x + 11, y + 1, "s5")
    L.hline(x - 1, x + 12, y + 3, "s2")
    L.vline(x - 1, y, y + 3, "sk")
    L.vline(x + 12, y, y + 3, "sk")
    L.hline(x, x + 11, y + h - 1, "sk")


def gate():
    """The north gate to the Aphaia Road: two ashlar piers joined by a stone
    lintel, the gate's leaves folded back against them. 4 x 3; the passage is
    cols 1-2, on aethos's limestone path."""
    s = Struct("gate", "The north gate to the Aphaia Road", 4, 3, SEC,
               walk=["X..X", "X..X", "X..X"],
               notes="The town gate: two ashlar piers (cols 0 and 3, solid) joined by a "
                     "stone lintel the player walks under (row 0), the wooden leaves folded "
                     "back against the piers. The passage, cols 1-2, is aethos's limestone "
                     "path. Join aethos's dry-stone wall (0x148-0x14A) to either side. "
                     "gate_shut swaps in for row 2 of the passage to close it.")
    ground(s, "path")
    M, T = s.M, s.T
    pier(M, 2, 0, 46)
    pier(M, 50, 0, 46)
    # the lintel over the passage: a long stone beam, carved with a running ant
    for x in range(16, 48):
        T.px(x, 1, "sk")
        T.px(x, 2, "s5")
        T.px(x, 3, "s4")
        T.px(x, 4, "s4")
        T.px(x, 5, "s3")
        T.px(x, 6, "s2")
        T.px(x, 7, "s1")
        T.px(x, 8, "sk")
    for x in range(18, 42, 8):                     # a frieze of ants, marching
        T.blit(["k k", " kk", "k k"], {"k": "s1"}, x, 3)
        T.blit(["k k", " kk", "k k"], {"k": "s1"}, x + 4, 4)
    # the leaves folded back: seen edge-on against each pier, studded
    for y in range(17, 46):
        M.px(16, y, "ink")
        M.px(17, y, "wd2")
        M.px(18, y, "wd1")
        M.px(19, y, "ink")
        if y % 6 == 2:
            M.px(17, y, "g0")
    M.hline(16, 19, 16, "ink")
    M.a[16:46, 44:48] = M.a[16:46, 16:20][:, ::-1]   # the right leaf, mirrored
    # the piers' shadows on the path
    for y in range(40, 48):
        for x in (14, 15, 62, 63):
            if M.get(x, y) is None:
                M.px(x, y, "s2" if (x + y) % 2 else None)
    return s


def gate_shut():
    """The gate's leaves shut across the passage, barred for the night."""
    s = Struct("gate_shut", "The north gate, shut for the night", 2, 1, SEC, walk=["XX"],
               notes="Swap these in for the gate's row 2 passage cells (setmetatile, solid) "
                     "while the gate is shut: two oak leaves meeting in the middle, bound in "
                     "iron, a bar across them.")
    ground(s, "path")
    M = s.M
    for x in range(0, 32):
        for y in range(0, 16):
            c = "wd2" if (x % 6) not in (0, 5) else "wd1"
            if x % 6 == 0:
                c = "wd0"
            M.px(x, y, c)
    for y in (3, 12):
        M.hline(0, 31, y, "ink")
        for x in range(1, 31, 4):
            M.px(x, y, "g0")
    M.vline(15, 0, 15, "ink")
    M.vline(16, 0, 15, "wd0")
    M.vline(0, 0, 15, "ink")
    M.vline(31, 0, 15, "ink")
    M.rect(4, 7, 24, 2, "wd3")                    # the bar
    M.hline(4, 27, 9, "ink")
    M.hline(0, 31, 15, "ink")
    return s


# --------------------------------------------------------------------------
# The turtle mosaic (group "poros")
# --------------------------------------------------------------------------

def turtle_mosaic():
    """A round pebble mosaic in the mint's square: the sea turtle of Aegina's
    staters, swimming in a ring of waves."""
    s = Struct("turtle_mosaic", "Turtle pebble mosaic", 2, 2, SEC, walk=["..", ".."],
               notes="A round pebble mosaic laid into the street before the mint: a sea "
                     "turtle, as struck on Aegina's coins, in a border of waves. On aethos's "
                     "limestone path; walkable.")
    ground(s, "path")
    M = s.M
    cx, cy = 15.5, 15.5
    for y in range(32):
        for x in range(32):
            r = math.hypot(x - cx, y - cy)
            if r > 15:
                continue
            if r > 13.5:
                c = "dk"
            elif r > 11.5:
                ang = math.atan2(y - cy, x - cx)
                c = "b1" if math.sin(ang * 9 + r) > 0 else "w0"     # the running waves
            elif r > 10.5:
                c = "dk"
            else:
                c = "po4" if (x + y) % 2 else "po3"                  # pale pebbles
            M.px(x, y, c)
    # the turtle, seen from above, head to the north
    turtle = [
        "      kk      ",
        "     k11k     ",
        "     k11k     ",
        " kk  kkkk  kk ",
        "k11kk2112kk11k",
        " kk121221121k ",
        "   k1d22d21k  ",
        "   k12d22d1k  ",
        "   k1d22d21k  ",
        "   k12d22d1k  ",
        "  kk1d22d21kk ",
        " k11k1111k11k ",
        " kk  kkkk  kk ",
        "      kk      ",
    ]
    M.blit(turtle, {"k": "dk", "1": "te1", "2": "po1", "d": "po0"}, 9, 9)
    M.a[:, 16:32] = M.a[:, 0:16][:, ::-1]          # symmetric: shared tiles
    return s


def build():
    return [inn(), mint(), aiakides_house(), gate(), gate_shut(), turtle_mosaic()]
