"""Minos's tomb and the Icarus Shaft, for gTileset_Labyrinth.

  tomb    behind Ring V's cracked wall %1 (LABYRINTH.md §8, scene F): "A low tomb
          behind the broken wall. Painted pillars. Dust older than the palace.
          Carved over the bier: MINOS, WHO JUDGES. WHAT IS HIDDEN, HE SEES. On the
          bier lies a dark leather cap, plain as a farmer's."
  shaft   the Icarus Shaft, 10 x 40 (LABYRINTH.md §7, scene L): the back wall of
          the shaft the player flies up, dark at the foot and brighter course by
          course toward the dawn sky at its mouth.
"""
from __future__ import annotations

import math

import labyrinth_art as A
import labyrinth_kit as KIT
import labyrinth_rings as R
from labyrinth_art import Struct, blit

MN = {"k": "ink", "R": "mr0", "r": "mr1", "e": "mr2", "E": "mr3", "o": "mo0", "O": "mo1",
      "y": "mo2", "g": "mg0", "G": "mg1", "W": "mg2", "b": "mb", "0": "mt0", "1": "mt1",
      "2": "mt2"}
BZ = R.BZ


# --------------------------------------------------------------------------
# Minos's tomb
# --------------------------------------------------------------------------

def pillar():
    """A painted Minoan column: tapering downward, red, a black cushion capital,
    a zigzag band painted round its neck, on a gypsum base."""
    s = Struct("tomb_pillar", "Minos's tomb: a painted pillar", 1, 2, walk=["X", "X"],
               section="deep",
               notes="A Minoan column, two cells: the black cushion capital and a painted "
                     "zigzag band at its neck, the red shaft tapering down to a gypsum base. "
                     "Blocks. `tomb_pillar_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    # the capital: a black cushion over a ochre abacus
    blit(M, [".kkkkkkkkkkkk...",
             "kOOOOOOOOOOOOk..",
             "kooooooooooook..",
             "kkkkkkkkkkkkkk..",
             ".kbbbbbbbbbbk...",
             "kbbbbbbbbbbbbk..",
             "kbbbbbbbbbbbbk..",
             ".kbbbbbbbbbbk...",
             "..kkkkkkkkkk...."], MN, 1, 0)
    for x in range(3, 13):
        M.px(x, 5, "mr0" if x > 9 else "mb")
    M.px(3, 5, "mr1")
    # the shaft, tapering from 10 px wide to 7
    for y in range(9, 28):
        t = (y - 9) / 18
        w = round(10 - 3 * t)
        a = 2 + (10 - w) // 2 + 1
        b = a + w - 1
        for x in range(a - 1, b + 2):
            if x == a - 1 or x == b + 1:
                c = "ink"
            elif x == a:
                c = "mr2"
            elif x == a + 1:
                c = "mr3" if y % 5 else "mr2"
            elif x >= b - 1:
                c = "mr0"
            else:
                c = "mr1"
            M.px(x, y, c)
    # a painted band: black zigzag on ochre
    for y in (11, 12, 13):
        for x in range(3, 13):
            if M.get(x, y) not in (None, "ink"):
                M.px(x, y, "mo1" if y != 12 else ("mb" if (x + y) % 3 == 0 else "mo1"))
    for x in range(3, 13):
        if M.get(x, 11) not in (None, "ink") and x % 3 == 0:
            M.px(x, 11, "mb")
        if M.get(x, 13) not in (None, "ink") and x % 3 == 1:
            M.px(x, 13, "mb")
    # the gypsum base
    blit(M, ["..kkkkkkkkkk....",
             ".kWWWWWWWWWWk...",
             ".kGGGGGGGGGgk...",
             "kWWWWWWWWWWWWk..",
             "kgggggggggggggk.",
             ".kkkkkkkkkkkkk.."], MN, 0, 26)
    s.names = {"top": (0, 0), "base": (0, 1)}
    return R.twins(s)


def bier():
    """The bier: a gypsum couch with Knossos's half-rosette frieze down its
    front, a faded purple cloth folded on it, and at its head the Helm of
    Darkness: a dark leather cap, plain as a farmer's."""
    s = Struct("tomb_bier", "Minos's tomb: the bier, and the cap on it", 4, 2,
               walk=["XXXX", "XXXX"], section="deep",
               notes="Minos's bier, three cells wide (columns 0-2): the gypsum couch, a faded "
                     "purple cloth folded on it, and at its head, (0, 0), the dark leather cap "
                     "that is the Helm of Darkness. Its front is carved with the palace's "
                     "half-rosette frieze. (3, 0) `head_empty`: swap it over (0, 0) once the "
                     "player has taken the Helm. Put the scene's bg event on the front row. "
                     "`tomb_bier_odd` on the odd parity.")
    # the couch's top fills the top row (bottom layer: no floor shows there, so
    # only the front row needs an odd twin); its front stands on the floor
    s.floor_cells = [(x, 1) for x in range(4)]
    R.lay(s)
    B, M = s.B, s.M
    w = 48
    for y in range(0, 30):
        for x in range(0, w):
            if y == 0 or x in (0, w - 1):
                c = "ink"
            elif y < 3:
                c = "mg2"
            elif y < 17:
                c = "mg1" if (x + y) % 8 else "mg2"
            elif y == 17:
                c = "mg2"
            elif y == 18:
                c = "ink"
            elif y < 29:
                c = "mg1"
            else:
                c = "ink"
            (B if y < 16 else M).px(x, y, c)
    B.a[0:16, 48:64] = B.a[0:16, 0:16]
    # the half-rosette frieze down the front: half-rosettes between triglyph bars
    for k in range(6):
        cx = 6 + k * 8
        for y in range(20, 28):
            for x in range(cx - 4, cx + 5):
                if not (2 <= x <= 45):
                    continue
                d = ((x - cx) ** 2 + (y - 28) ** 2) ** 0.5
                if d <= 3.2:
                    M.px(x, y, "mo1" if d > 1.5 else "mr1")
                elif d <= 4.4:
                    M.px(x, y, "mo0")
        bx = cx + 4
        if bx < 46:
            for y in range(20, 28):
                M.px(bx, y, "mb")
    for x in range(2, 46):
        M.px(x, 19, "mg0")
        M.px(x, 28, "mg0")
    # legs
    for x in (3, 4, 43, 44):
        M.px(x, 29, "ink")
        M.px(x, 30, "mg0")
    # the cloth, folded along the couch (purple-red)
    for y in range(8, 15):
        for x in range(14, 44):
            if (x + y) % 11 == 0:
                c = "mr0"
            elif y in (8, 14):
                c = "ink"
            elif y < 11:
                c = "mr1"
            else:
                c = "mr0"
            if x in (14, 43):
                c = "ink"
            M.px(x, y, c)
    for x in range(15, 43, 4):
        M.px(x, 9, "mr2")
    # the empty head (column 3): the couch's head as it is without the cap
    M.a[0:16, 48:64] = M.a[0:16, 0:16]
    # the cap: dark leather, plain, on the bier's head (cell 0, 0)
    blit(M, ["...kkkkk....",
             "..kbbbbbk...",
             ".kbRbbbbbk..",
             ".kbbbbbbbk..",
             "kbbbbbbbbbk.",
             "kkbbbbbbbkk.",
             ".kkkkkkkkk.."], MN, 2, 6)
    M.px(5, 8, "mr0")
    # the empty head (column 3): the couch's head without the cap
    s.names = {"head": (0, 0), "top_m": (1, 0), "top_r": (2, 0), "head_empty": (3, 0),
               "front_l": (0, 1), "front_m": (1, 1), "front_r": (2, 1)}
    return R.twins(s)


GLYPHS = [["k.k", "kkk", ".k."], ["kkk", "k..", "kk."], [".k.", "kkk", "k.k"], ["k..", "kkk", "..k"],
          ["kkk", ".k.", ".k."], ["k.k", ".k.", "k.k"], ["kk.", "k.k", "kk."], [".kk", "k..", ".kk"]]


def inscription():
    """Carved over the bier: MINOS, WHO JUDGES. WHAT IS HIDDEN, HE SEES."""
    s = Struct("tomb_inscription", "Minos's tomb: the inscription over the bier", 3, 1,
               walk=["XXX"], section="deep",
               notes="A face row, three cells, set over the bier: a gypsum panel cut with "
                     "two lines of signs, MINOS, WHO JUDGES. WHAT IS HIDDEN, HE SEES (scene F). "
                     "Put the sign's bg event on its middle. Its ends meet faces that run on.")
    L = s.B
    for i in range(3):
        R.face(L, i * 16, 0)
    for y in range(5, 15):
        for x in range(3, 45):
            c = "ls5"
            if y == 5 or x == 3:
                c = "ls6"
            elif y == 14 or x == 44:
                c = "ls3"
            L.px(x, y, c)
    # two lines of signs, four to every sixteen pixels (so the panel's middle
    # repeats, tile for tile)
    for k in range(10):
        gx = 4 + 4 * k
        if gx + 3 > 43:
            break
        blit(L, GLYPHS[k % 4], {"k": "ls2"}, gx + 1, 7)
        blit(L, GLYPHS[4 + (k + 1) % 4], {"k": "ls2"}, gx + 1, 11)
    s.names = {"l": (0, 0), "m": (1, 0), "r": (2, 0)}
    return s


def grave_goods():
    """Things left with a king: a labrys stand, a stirrup jar, and dust."""
    s = Struct("tomb_goods", "Minos's tomb: a labrys stand, a jar, dust", 3, 2,
               walk=["XX.", "X.."], section="deep",
               notes="(0, 0) `labrys_top` over (0, 1) `labrys_base`: a bronze double axe on a "
                     "tall pole in a stepped stone base, as stood either side of an altar "
                     "(blocks). (1, 0) `jar`: a terracotta jar, banded in black (blocks). Dust "
                     "older than the palace, on floor cells (walkable; the tomb isn't threaded): "
                     "(2, 0) `dust` in soft drifts, (1, 1) `drift` heaped against a wall to the "
                     "north, (2, 1) `prints`: dust with bare footprints in it, someone's, long "
                     "ago. `tomb_goods_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    _dust(M)
    # the labrys on its pole (bronze; the pole stops at its stone base's top)
    blit(M, ["..k.......k.....",
             ".k3k.....k3k....",
             "k343k.k.k343k...",
             "k3443k4k3443k...",
             "k34432423443k...",
             "k3443k2k3443k...",
             "k343k.2.k343k...",
             ".k3k..2..k3k....",
             "..k...1...k.....",
             "......2.........",
             "......1.........",
             "......2.........",
             "......1.........",
             "......2.........",
             "......1.........",
             "......2........."], BZ, 0, 1)
    for y in range(16, 24):
        M.px(6, y, "bz1" if y % 2 else "bz2")
        M.px(5, y, "ink")
        M.px(7, y, "ink")
    blit(M, ["....kkkkk.......",
               "...k66655k......",
               "..k6555543k.....",
               ".k655555433k....",
               "kkkkkkkkkkkkk...",
               "k5555555554442k.",
               "k3333333333222k.",
               ".kkkkkkkkkkkkk.."], R.ST, 0, 24)   # stone (k is lk here)
    # a terracotta jar, banded in black
    blit(M, ["....kkkkkk......",
             "...k221110k.....",
             "....kk11kk......",
             "..kk111110kk....",
             ".k2211111100k...",
             "kbbbbbbbbbbbbk..",
             "k221111111100k..",
             "k2bb11bb11bb0k..",
             "k221111111100k..",
             ".kbbbbbbbbbbk...",
             "..k21111100k....",
             "...kkkkkkkk....."], MN, 16 + 1, 2)
    s.names = {"labrys_top": (0, 0), "jar": (1, 0), "dust": (2, 0),
               "labrys_base": (0, 1), "drift": (1, 1), "prints": (2, 1)}
    return R.twins(s)


def _dust(M):
    """Dust as an overlay (the same on either parity): soft drifts, a heap against
    a wall, footprints."""
    def blob(x, y, k, heavy=0.0):
        v = (math.sin(x * 0.9 + k) + math.sin(y * 1.1 + 2 * k) +
             math.sin((x + y) * 0.55 + 3 * k)) / 3 + heavy * (5 - y) * 0.16
        if v > 0.55:
            return "ls6"
        if v > 0.2 or (v > 0.05 and (x + y) % 2 == 0):
            return "ls5"
        return None
    # three dust tiles, shared by the three cells (light, light, heaped)
    tiles = {k: [[blob(x, y, s, h) for x in range(8)] for y in range(8)]
             for k, s, h in (("a", 1, 0), ("b", 4, 0), ("h", 2, 1))}
    lay_out = {(2, 0): ("a", "b", "b", "a"), (1, 1): ("h", "h", "a", "b"),
               (2, 1): ("b", "a", "a", "b")}
    for (cx, cy), quads in lay_out.items():
        for q, k in enumerate(quads):
            ox, oy = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8
            t = tiles[k]
            for y in range(8):
                for x in range(8):
                    c = t[y][7 - x] if (k == "h" and q == 1) else t[y][x]
                    if c:
                        M.px(ox + x, oy + y, c)
    for (cx, cy, kind) in ((2, 1, "prints"),):
        if kind == "prints":
            # two bare footprints walking north through it
            for (fx, fy) in ((4, 9), (9, 2)):
                for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (1, 3)):
                    M.px(cx * 16 + fx + dx, cy * 16 + fy + dy, "ls3")


# --------------------------------------------------------------------------
# The Icarus Shaft
# --------------------------------------------------------------------------

BANDS = [("lk", "ls1", "ls2"),      # (joint, body, top edge) from the foot up
         ("lk", "ls2", "ls3"),
         ("ls1", "ls3", "ls4"),
         ("ls2", "ls4", "ld0"),
         ("ls3", "ld0", "ld1")]


def _course(L, x0, y0, band, offset):
    """One course of the shaft's back wall, 16 x 8, blocks sixteen wide."""
    j, b, h = BANDS[band]
    for y in range(8):
        for x in range(16):
            jx = (x - offset) % 16
            if y == 7:
                c = j
            elif jx == 0:
                c = j
            elif y == 0 or jx == 1:
                c = h
            else:
                c = b
            L.px(x0 + x, y0 + y, c)


def _side(L, x0, y0, band, west):
    j, b, h = BANDS[band]
    for y in range(8):
        for x in range(16):
            X = x if west else 15 - x
            if X < 10:
                c = "lk"
            elif X == 10:
                c = j
            elif X < 15:
                c = j if y == 7 else b
            else:
                c = h
            L.px(x0 + x, y0 + y, c)


def icarus():
    """The Icarus Shaft's courses, light level by light level."""
    rows = [("sky", None), ("lip", None)]
    for k in range(4, -1, -1):
        rows.append((f"band{k}", (k, k)))
        if k:
            rows.append((f"fade{k}", (k, k - 1)))
    rows.append(("foot", None))
    # two columns of six rows: the top of the shaft on the left, its foot on the right
    s = Struct("icarus", "The Icarus Shaft, foot to mouth", 6, 6,
               walk=["X.XX.X"] * 6, section="deep",
               notes="The shaft Icarus flew from (scene L), 10 wide: column 0 its west wall, "
                     "1-8 its back wall (repeat the middle cell), 9 its east wall. Build it "
                     "from the foot up: `foot` (the grate drawn up, bronze bars hanging over "
                     "the dark), then `band0` repeated, `fade1`, `band1`, `fade2`... each band a "
                     "step brighter toward the dawn, up to `band4`, then `lip` (the shaft's "
                     "mouth, the first sunlight on its edge) and `sky` on the top row. Each "
                     "row's three cells are named `<row>_w`, `<row>_m`, `<row>_e` (the sheet "
                     "holds the top six rows in columns 0-2 and the bottom six in 3-5). The "
                     "middle is walkable (the flight is scripted). Load the `dawn/` palettes "
                     "here, as in scene L: the courses below go grey and the top of the shaft "
                     "blazes.")
    full = A.K.Layer(48, 16 * len(rows))
    fullm = A.K.Layer(48, 16 * len(rows))
    L, M = full, fullm
    for r, (name, bands) in enumerate(rows):
        y0 = r * 16
        if bands:
            up, low = bands
            _side(L, 0, y0, up, True)
            _side(L, 0, y0 + 8, low, True)
            _course(L, 16, y0, up, 0)
            _course(L, 16, y0 + 8, low, 8)
            _side(L, 32, y0, up, False)
            _side(L, 32, y0 + 8, low, False)
        elif name == "lip":
            # the mouth: the sky over the shaft's last course, its edge in sunlight
            for x in range(48):
                for y in range(8):
                    L.px(x, y0 + y, _sky(x, y + 16))
            _side(L, 0, y0 + 8, 4, True)
            _course(L, 16, y0 + 8, 4, 8)
            _side(L, 32, y0 + 8, 4, False)
            for x in range(48):
                L.px(x, y0 + 8, "ld1")
                L.px(x, y0 + 9, "lw1" if 10 <= x <= 37 else "ld0")
        elif name == "sky":
            for x in range(48):
                for y in range(16):
                    L.px(x, y0 + y, _sky(x, y))
        elif name == "foot":
            _side(L, 0, y0, 0, True)
            _side(L, 0, y0 + 8, 0, True)
            _course(L, 16, y0, 0, 0)
            _course(L, 16, y0 + 8, 0, 8)
            _side(L, 32, y0, 0, False)
            _side(L, 32, y0 + 8, 0, False)
            # the grate, drawn up: its bars hang down over the foot of the shaft
            for x in range(16, 32):
                if (x - 16) % 4 == 1:
                    for y in range(0, 12):
                        M.px(x, y0 + y, "bz2" if y < 10 else "bz3")
                    M.px(x, y0 + 12, "bz4")
                    M.px(x - 1, y0 + 11, "ink")
                    M.px(x + 1, y0 + 11, "ink")
                for y in (3, 8):
                    M.px(x, y0 + y, "bz1" if (x - 16) % 4 != 1 else "bz3")
        for c, part in enumerate("wme"):
            s.names[f"{name}_{part}"] = (c + 3 * (r // 6), r % 6)
    # fold the twelve rows into two columns of six
    for half in (0, 1):
        src = slice(half * 96, half * 96 + 96)
        s.B.a[:, half * 48:half * 48 + 48] = full.a[src]
        s.M.a[:, half * 48:half * 48 + 48] = fullm.a[src]
    return s


def _sky(x, y):
    """Dawn straight up the shaft: pale blue; `sky_e` carries a pink streak of
    cloud (lay it wherever a cloud should be)."""
    for (cy, a, b) in ((4, 34, 45), (10, 37, 42)):
        if y == cy and a <= x <= b:
            return "fp"
        if y == cy + 1 and a + 2 <= x <= b - 1:
            return "fw"
    return "fb3"


def build():
    return [*pillar(), *bier(), inscription(), *grave_goods(), icarus()]
