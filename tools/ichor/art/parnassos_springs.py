"""Lebadeia's precinct: the rock face with the bronze grille, the spout and the
votive tablets; the two springs.

  face      south-face cells of a crag (blob key 1|11100011), for the rock the
            oracle's cave opens in:
              grille       the bronze grille shut across the cave mouth (blocks)
              grille_open  the grille swung back: MB_NON_ANIMATED_DOOR, the warp
              spout        the spring of Mnemosyne running out of the rock
              tablets      pilgrims' wooden tablets hung on pegs in the rock
  lethe     the spring of Lethe, 2 x 2: a stone basin of black, still water
  mnemosyne the spring of Mnemosyne, 2 x 2: bright running water (aethos's
            animated water under a stone rim), fed from the spout above it and
            spilling east into the Herkyna through a notch in its rim
"""
from __future__ import annotations

import numpy as np

import kithairon_ground as KG
import kithairon_stone as KS
import parnassos_lib as P

SEC = "springs"
SOUTH_EDGE = KS.SOUTH_EDGE


def _foot(x, y):
    """The precinct's floor at the rock's foot, in shadow (Kithairon's rock names,
    recolored with the rest)."""
    return "rk2"


def _face_cell(L, ox, oy):
    KG.paint_crag_cell(L, ox, oy, SOUTH_EDGE, _foot, dark=False)


def face():
    names = {"grille": (0, 0), "grille_open": (1, 0), "spout": (2, 0), "tablets": (3, 0),
             "plain": (4, 0)}
    s = P.struct("face", "The oracle's rock: grille, spout, tablets", 5, 1, SEC, walk=["XDXXX"],
                 names=names,
                 notes=f"South-face cells of the crag (blob key `{SOUTH_EDGE}`) over the "
                       "precinct's paving, a shadowed foot at their base (`plain` the bare "
                       "face). `grille` the "
                       "bronze grille shut across Trophonios's cave mouth (blocks); "
                       "`grille_open` swung back, MB_NON_ANIMATED_DOOR, the cave's warp (the "
                       "map swaps it in when `FLAG_ICHOR_TROPHONIOS_GRILLE_OPEN` is set); "
                       "`spout` the spring of Mnemosyne running out of the rock; `tablets` "
                       "pilgrims' tablets hung on pegs.")
    tmp = P.Layer(80, 16)
    for cx in range(5):
        _face_cell(tmp, cx * 16, 0)
    for k, v in P.KITH_TO_PARN.items():
        P.recolor(tmp, {k: v})
    B = s.B
    B.a[:] = tmp.a

    # the cave mouth: a low dark arch in the face, the rock's lip over it
    def mouth(ox):
        for y in range(3, 16):
            for x in range(2, 14):
                d = ((x - 7.5) / 6.0) ** 2 + ((y - 15.5) / 12.5) ** 2
                if d <= 1.0:
                    B.px(ox + x, y, "pk0")
                elif d <= 1.25:
                    B.px(ox + x, y, "pk1" if y > 6 else "pk2")
        for x in range(4, 12):
            B.px(ox + x, 15, "pk1")
    mouth(0)
    mouth(16)
    # shut: bronze bars, a crossbar and a lock-plate
    for x in (4, 6, 8, 10, 12):
        for y in range(4, 16):
            if ((x - 7.5) / 6.0) ** 2 + ((y - 15.5) / 12.5) ** 2 <= 1.05:
                B.px(x, y, "bz1")
                B.px(x + 1, y, "pk1" if y % 3 else "pk0")
    for x in range(3, 14):
        B.px(x, 9, "bz1")
        B.px(x, 10, "pk1")
    P.put(B, 7, 8, ["bb", "b4", "bb"], {"b": "bz1", "4": "pk4"})
    # open: the grille folded back against the west jamb, the way down dark
    for x in (17, 18, 19):
        for y in range(5, 16):
            B.px(x, y, "bz1" if x != 18 else "pk2")
    for y in (8, 12):
        B.px(16 + 4, y, "bz1")
    # the spout: a stone lip in the face, water falling down to the basin below
    ox = 32
    P.put(B, ox + 5, 4, ["535", "4444", "2112"], {"5": "pk5", "4": "pk4", "3": "pk3", "2": "pk2",
                                                    "1": "pk0"})
    for y in range(7, 16):
        for x in range(6, 10):
            c = "b3" if (x + y) % 3 else "pk5"
            B.px(ox + x, y, c)
        B.px(ox + 5, y, "pk1")
        B.px(ox + 10, y, "pk2")
    # tablets on pegs
    ox = 48
    for (x, y) in ((2, 4), (7, 3), (11, 6), (4, 9), (9, 10)):
        B.px(ox + x + 1, y, "pk0")                     # the peg
        P.put(B, ox + x, y + 1, ["bbb", "b4b", "bbb", "111"], {"b": "bz1", "4": "pk4", "1": "pk1"})
    return s


def lethe():
    s = P.struct("lethe", "The spring of Lethe (2 x 2)", 2, 2, SEC, walk=["XX", "XX"],
                 names={"NW": (0, 0), "NE": (1, 0), "SW": (0, 1), "SE": (1, 1)},
                 notes="A square stone basin of black, still water: forgetting. Blocks. A hidden "
                       "item can sit in it (the Bronze Obol someone threw in to forget "
                       "something).")
    B = s.B
    for y in range(32):
        for x in range(32):
            B.px(x, y, "mb3")
    # the rim: lit on top, a step down to the water, a dark inner edge
    for y in range(32):
        for x in range(32):
            if 3 <= x < 29 and 4 <= y < 28:
                # the water: black, still, a faint sky-glint
                c = "lt0"
                if y in (6, 7) and 8 <= x < 20 and (x + y) % 3:
                    c = "lt1"
                if (x, y) in ((22, 10), (23, 10), (10, 18), (11, 18), (19, 23)):
                    c = "lt2"
                if x == 3 or y == 4:
                    c = "mb0"
                elif x == 4 or y == 5:
                    c = "lt1" if c == "lt0" else c
                B.px(x, y, c)
            elif y < 2 or x < 2:
                B.px(x, y, "mb4")
            elif y >= 30 or x >= 30:
                B.px(x, y, "mb1")
            elif y >= 28:
                B.px(x, y, "mb2")
    for x in range(32):
        B.px(x, 31, "mb0")
    for y in range(32):
        B.px(31, y, "mb0")
    return s


def mnemosyne():
    s = P.struct("mnemosyne", "The spring of Mnemosyne (2 x 2)", 2, 2, SEC, walk=["XX", "XX"],
                 names={"NW": (0, 0), "NE": (1, 0), "SW": (0, 1), "SE": (1, 1)},
                 notes="Bright running water in a stone rim, fed from the spout above (put "
                       "`face`'s `spout` over its west column) and spilling east through a notch "
                       "into the Herkyna: put the river's water cells against its east side and "
                       "count these cells as water when tiling the river. Blocks.")
    P.ground(s, "sea")
    M = s.M
    for y in range(32):
        for x in range(32):
            inside = 3 <= x and 4 <= y < 28
            notch = x >= 29 and 8 <= y < 24          # the outflow east
            if inside and (x < 29 or notch):
                continue
            if y < 2 or x < 2:
                c = "mb4"
            elif y >= 30:
                c = "mb1"
            elif y >= 28:
                c = "mb2"
            elif x >= 30:
                c = "mb1"
            else:
                c = "mb3"
            M.px(x, y, c)
    for x in range(32):
        M.px(x, 31, "mb0")
    for y in list(range(0, 8)) + list(range(24, 32)):
        M.px(31, y, "mb0")
    # inner edge and foam where the spout falls in, and along the outflow
    for x in range(3, 29):
        M.px(x, 4, "mb0" if not 8 <= x < 13 else "w0")
    for y in range(4, 28):
        M.px(3, y, "mb0")
    for (x, y) in ((8, 5), (9, 6), (10, 5), (11, 6), (12, 5), (9, 8), (11, 8), (10, 7), (7, 7), (13, 7)):
        M.px(x, y, "w0")
    for (x, y) in ((8, 6), (12, 6), (10, 9), (8, 9), (12, 9)):
        M.px(x, y, "b4")
    for y in range(8, 24):
        if y % 4 == 1:
            M.px(28 + (y % 3), y, "b4")
    return s


def build():
    return [face(), lethe(), mnemosyne()]
