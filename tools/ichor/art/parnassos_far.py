"""The lookout's view (beat 36B): across a ravine and high above, the Phaidriades,
Delphoi's two shining cliffs, the Kastalian falls coming down the gorge between
them, and the sanctuary's roofs on the slope below.

Seen across a ravine, the far side shows its south faces; it is drawn in a
pale, hazy palette so it reads as distant. Every cell blocks.

  far      the far side, in rows from the top: `top_a`/`top_b` the cliffs' tops,
           `face_a`/`face_b` the cliff faces, `gorge_top`/`gorge` the Kastalian
           gorge and its falls, `foot` the cliffs' foot, `slope` the hazy slope,
           `temple_L`/`temple_R` Apollo's temple, `theater`, `roofs` the
           treasuries, `slope_foot` the slope falling away into the ravine
  ravine   the ravine's dark between the two sides (and `lip`: the lookout's
           near edge, grass to the south, walkable)
"""
from __future__ import annotations

import numpy as np

import parnassos_lib as P

SEC = "far"


# Buttresses of the far cliffs: (left edge, width) across a 32 px period, so two
# 16 px face cells side by side read as one irregular wall.
_BUTTRESS = [(0, 5), (5, 3), (8, 6), (14, 4), (18, 5), (23, 4), (27, 5)]


def _haze_face(L, ox, oy, seed):
    """A tall pale cliff of rounded buttresses: each lit on its left, shadowed on
    its right, a dark cleft between; a ledge line here and there."""
    for y in range(16):
        for x in range(16):
            xx = (x + seed * 16) % 32
            for (x0, w) in _BUTTRESS:
                if x0 <= xx < x0 + w:
                    u = xx - x0
                    break
            if u == 0:
                col = "hz0"
            elif u == 1:
                col = "hz3"
            elif u == w - 1:
                col = "hz1"
            else:
                col = "hz2"
            # ledges catching the light, with a shadow under them
            if (y + (xx // 6) * 3) % 11 == 0 and u > 0:
                col = "hz3"
            elif (y + (xx // 6) * 3) % 11 == 1 and u > 0:
                col = "hz1"
            if P.hsh(xx, y, 17) % 29 == 0:
                col = "hz1"
            L.px(ox + x, oy + y, col)


def far():
    names = {"top_a": (0, 0), "top_b": (1, 0), "face_a": (2, 0), "face_b": (3, 0),
             "gorge_top": (4, 0), "gorge": (5, 0), "foot": (6, 0), "slope": (7, 0),
             "temple_L": (0, 1), "temple_R": (1, 1), "theater": (2, 1), "roofs": (3, 1),
             "slope_foot": (4, 1), "gorge_foot": (5, 1), "foot_b": (6, 1), "slope_b": (7, 1)}
    s = P.struct("far", "The far side: the Phaidriades and Delphoi", 8, 2, SEC,
                 walk=["XXXXXXXX", "XXXXXXXX"], names=names,
                 notes="A backdrop across the lookout's ravine, from the top: cliff tops "
                       "(`top_a`, `top_b`), faces (`face_a`, `face_b`) with the Kastalian gorge "
                       "and its falls between them (`gorge_top`, `gorge`, `gorge_foot`), the "
                       "cliffs' foot (`foot`, `foot_b`), the slope with the sanctuary "
                       "(`slope`, `slope_b`, `temple_L` `temple_R`, `theater`, `roofs`), and "
                       "`slope_foot` falling into the ravine. All block.")
    B = s.B
    # cliff tops: hazy rock under scrub and the odd pine, the rim lit
    for ox in (0, 16):
        for y in range(16):
            for x in range(16):
                col = "hz2" if y < 12 else ("hz3" if y == 12 else "hz2")
                h = P.hsh(x + ox, y, 7) % 13
                if y < 11 and h < 3:
                    col = "lr1"
                elif y < 11 and h < 5:
                    col = "hz1"
                if y >= 13:
                    col = "hz1" if (x + y) % 3 else "hz0"
                B.px(ox + x, y, col)
        for (x, y) in ((3, 3), (10, 1), (12, 7), (6, 7)):
            P.put(B, ox + x, y, [".2.", "212", "111", ".p."], {"2": "lr2", "1": "lr1", "p": "pk0"})
    # faces
    _haze_face(B, 32, 0, 0)
    _haze_face(B, 48, 0, 3)
    # the gorge: a dark slot with a white rope of falling water
    for oy, top in ((0, True), (16, False)):
        ox = 64 if top else 80
        for y in range(16):
            for x in range(16):
                if 4 <= x < 12:
                    col = "dk1" if x in (4, 11) else "hz0"
                    if 6 <= x < 10:
                        col = "w0" if (y + x) % 4 else "b4"
                else:
                    col = "hz2" if x not in (1, 14) else "hz1"
                if top and y < 4 and not 4 <= x < 12:
                    col = "hz3"
                B.px(ox + x, y, col)
    # the falls' foot: the water breaks into spray among the trees
    for y in range(16):
        for x in range(16):
            col = "hz2" if y < 6 else ("lr1" if (x + y) % 4 else "lr2")
            if y < 9 and 5 <= x < 11:
                col = "w0" if (x + y) % 3 else "b4"
            elif 9 <= y < 12 and 3 <= x < 13:
                col = "w0" if (x * 3 + y) % 4 else "b4"
            elif y == 12 and 4 <= x < 12:
                col = "b4"
            B.px(80 + x, 16 + y, col)
    # the cliffs' foot: the face darkens into a band of scree and green
    for (ox, oy, seed) in ((96, 0, 1), (96, 16, 4)):
        _haze_face(B, ox, oy, seed)
        for y in range(9, 16):
            for x in range(16):
                k = y + (P.hsh(x, 0, seed) % 3)
                col = "hz1" if k < 12 else ("hz2" if k < 13 else "lr1")
                if k >= 13 and P.hsh(x, y, seed) % 4 == 0:
                    col = "lr2"
                if y == 9:
                    col = "hz0"
                B.px(ox + x, oy + y, col)
    # the slope: hazy green with cypress dots and terrace lines
    def slope(ox, oy, seed):
        for y in range(16):
            for x in range(16):
                col = "lr1" if (x * 3 + y * 2 + seed) % 7 else "lr2"
                if y in (5, 12) and x % 4:
                    col = "hz0"
                B.px(ox + x, oy + y, col)
        for (x, y) in ((3, 1), (11, 6), (6, 13), (14, 9)):
            P.put(B, ox + x, oy + y, ["2", "p", "p"], {"2": "lr2", "p": "pk0"})
    slope(112, 0, 0)
    slope(112, 16, 2)
    # Apollo's temple on its terrace: roof ridge, pediment, a row of columns
    tx, ty = 0, 16
    slope(tx, ty, 1)
    slope(tx + 16, ty, 3)
    P.put(B, tx + 4, ty + 2, [
        "......tttttttttttttttt......",
        "....tTTTTTTTTTTTTTTTTTTt....",
        "..tTTTTTTTTTTTTTTTTTTTTTTt..",
        ".wwwwwwwwwwwwwwwwwwwwwwwwww.",
        ".w0w0w0w0w0w0w0w0w0w0w0w0w..",
        ".w0w0w0w0w0w0w0w0w0w0w0w0w..",
        ".w0w0w0w0w0w0w0w0w0w0w0w0w..",
        ".w0w0w0w0w0w0w0w0w0w0w0w0w..",
        "wwwwwwwwwwwwwwwwwwwwwwwwwwww",
        "hhhhhhhhhhhhhhhhhhhhhhhhhhhh",
    ], {"t": "tc1", "T": "tc2", "w": "w0", "0": "hz1", "h": "hz0"})
    # the theater, a pale half-ring cut into the slope
    slope(32, 16, 5)
    for y in range(16):
        for x in range(16):
            d = ((x - 8) / 7.0) ** 2 + ((y - 12) / 9.0) ** 2
            if d <= 1.0 and y <= 12:
                if d > 0.35:
                    B.px(32 + x, 16 + y, "w1" if (y % 2) else "hz2")
                else:
                    B.px(32 + x, 16 + y, "hz3")
    for x in range(2, 15):
        B.px(32 + x, 16 + 12, "hz0")
    # the treasuries: little roofs up the Sacred Way
    slope(48, 16, 7)
    for (x, y) in ((2, 2), (9, 5), (4, 10), (11, 11)):
        P.put(B, 48 + x, 16 + y, ["ttt", "TTTT", "wwww", "w0w."], {"t": "tc1", "T": "tc2", "w": "w0",
                                                                   "0": "hz1"})
    # the slope falling away into the ravine
    for y in range(16):
        for x in range(16):
            k = y + (P.hsh(x, 0, 9) % 4)
            col = "lr1" if k < 5 else ("hz0" if k < 9 else ("dk1" if k < 13 else "pk0"))
            B.px(64 + x, 16 + y, col)
    return s


def ravine():
    s = P.struct("ravine", "The ravine, and the lookout's lip", 3, 1, SEC, walk=["XX."],
                 names={"dark": (0, 0), "mist": (1, 0), "lip": (2, 0)},
                 notes="`dark` the ravine's depth; `mist` the same with a thread of mist; `lip` "
                       "the lookout's near edge (grass to the south, the drop to the north; "
                       "walkable, the player stops at it).")
    B = s.B
    for y in range(16):
        for x in range(16):
            B.px(x, y, "pk1" if P.hsh(x, y, 41) % 17 == 0 else "pk0")
            col = "pk0"
            if y in (6, 7) and (x + y) % 3:
                col = "pk1"
            if y == 6 and x % 5 == 0:
                col = "pk2"
            B.px(16 + x, y, col)
    for y in range(16):
        for x in range(16):
            if y < 5:
                col = "pk0" if y < 3 else "pk1"
            elif y == 5:
                col = "pk4"
            elif y == 6:
                col = "pk3" if x % 4 else "pk5"
            elif y == 7:
                col = "pk2"
            else:
                col = P.grass_name(x, y)
                if y == 8:
                    col = {"g3": "g1", "g2": "g1", "g1": "gd"}.get(col, col)
            B.px(32 + x, y, col)
    for (x, y) in ((3, 4), (9, 3), (13, 4)):
        B.px(32 + x, y, "iv1")
        B.px(32 + x, y + 1, "iv2")
    return s


def build():
    return [far(), ravine()]
