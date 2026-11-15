"""gTileset_MaiaCave: the Cave of Maia on Route 12, where Hermes was born.

A shallow, dry cave of warm brown rock with a sandy floor. Its own small set
on the aethos primary (no grass shows inside):

  cwall      the cave's rock seen from above (blob shapes), on the floor
  cface      its back wall's faces (the heights face painter, warm ramp)
  cfloor     `plain`, `pebbles`, `exit` (MB_SOUTH_ARROW_WARP, daylight)
  maia       the god's things: the cradle niche with its folded cloth, the
             tortoise-shell lyre on the wall, the herm's face carved in the
             rock, the altar of Hermes, the priestess's lamp, stool and jar
"""
from __future__ import annotations

import numpy as np

import heights_ground as G
import heights_lib as H
import heights_props as P

SEC = "cave"
RAMP = ("qd0", "qd1", "qd2", "qd3", "qd4", "qd5")
# The rock seen from above sits a step darker than the faces, so the cave's mass
# reads as rock against the pale sand and not as more floor.
TOP_RAMP = ("qd0", "qd0", "qd1", "qd2", "qd3", "qd4")
CAVE = {"K": "ink", "0": "qd0", "1": "qd1", "2": "qd2", "3": "qd3", "4": "qd4", "5": "qd5",
        "a": "qe1", "b": "qe2", "c": "qe3"}


def floor_px(x, y):
    xx, yy = x % 16, y % 16
    h = H.hsh(xx, yy, 9) % 100
    if (xx, yy) in ((3, 4), (11, 10), (7, 13)):
        return "qe3"
    if (xx, yy) in ((3, 5), (11, 11), (8, 13)):
        return "qd2"
    return "qe1" if h < 20 else "qe2"


def cwall():
    return H.shape_set("cwall", "The cave's rock, from above", SEC, G.wanted("cwall"),
                       lambda s, ox, oy, k: G.paint_rock_cell(s.B, ox, oy, k, TOP_RAMP, floor=floor_px,
                                                              ferns=False), "X",
                       "The cave's warm brown rock seen from above, on the sandy floor. "
                       "Impassable. Names are blob shape keys.")


def cface():
    keys = G.wanted("cface", ["r---0", "rf--0", "----0", "-f--0"])
    return H.shape_set("cface", "The cave's back wall", SEC, keys,
                       lambda s, ox, oy, k: G.paint_face_cell(s.B, ox, oy, k, RAMP, ferns=False,
                                                              floor=floor_px), "X",
                       "The back wall's faces, shape keys as the heights `face`. Impassable.")


def cfloor():
    s = H.struct("cfloor", "The cave floor", 3, 1, SEC, walk=["..."],
                 names={"plain": (0, 0), "pebbles": (1, 0), "exit": (2, 0)},
                 notes="`plain` sand, `pebbles` a scatter of stones, `exit` the floor brightening "
                       "toward daylight: MB_SOUTH_ARROW_WARP, the warp out on the bottom row.")
    for x in range(48):
        for y in range(16):
            s.B.px(x, y, floor_px(x, y))
    for (x, y) in ((19, 3), (26, 9), (22, 12), (28, 4), (17, 13)):
        H.put(s.B, x, y, [".3.", "322", ".0."], CAVE)
    for y in range(16):
        for x in range(32, 48):
            k = y + (H.hsh(x, y, 9) % 5) - 2
            if k > 8:
                s.B.px(x, y, "qe3" if k > 12 else "qd5")
    s.behaviors[(2, 0)] = "MB_SOUTH_ARROW_WARP"
    return s


def maia():
    names = {"cradle_L": (0, 0), "cradle_R": (1, 0), "lyre": (2, 0), "herm_face": (3, 0),
             "altar_L": (4, 0), "altar_R": (5, 0), "lamp": (6, 0), "jar": (7, 0), "stool": (0, 1),
             "spring": (1, 1)}
    s = H.struct("maia", "The Cave of Maia: the god's things", 8, 2, SEC,
                 walk=["XXXXXXXX", "XX......"], names=names,
                 notes="Back-wall cells (on the wall's foot row): `cradle_L` + `_R` a cradle-shaped "
                       "niche cut in the rock, a scrap of old swaddling folded in it; `lyre` a "
                       "tortoise shell strung with gut, hung on the wall, its crack mended with "
                       "pitch; `herm_face` Hermes's bearded head carved straight out of the rock. "
                       "On the floor: `altar_L` + `_R` the altar of Hermes, a caduceus cut in its "
                       "side; `lamp` the priestess's lamp on its stand, never let go out; `jar` a "
                       "water jar; `stool` her stool; `spring` a seep in the floor (walkable).")
    s.walk = ["XXXXXXXX", "XX......"]
    # back-wall cells: the face (foot row) with things cut into it
    for cx, kind in enumerate(("cradle_L", "cradle_R", "lyre", "herm_face")):
        d = P.L16()
        for y in range(16):
            for x in range(16):
                d.px(x, y, G.face_px(x, y, RAMP, False, cx % 3))
        G_foot(d)
        if kind.startswith("cradle"):
            # a rounded niche running across both cells, deep shadow inside
            left = kind.endswith("L")
            for y in range(3, 12):
                for x in range(16):
                    gx = x if left else x + 16
                    if ((gx - 15.5) / 13.0) ** 2 + ((y - 9.5) / 6.5) ** 2 <= 1 and y >= 4:
                        d.px(x, y, "qd0" if y < 7 else "qd1")
            # the folded cloth
            for x in range(16):
                gx = x if left else x + 16
                if 8 <= gx <= 23:
                    for y in (9, 10):
                        d.px(x, y, "qe3" if y == 9 else "qd4")
            if left:
                d.vline(3, 5, 11, "qd2")
            else:
                d.vline(12, 5, 11, "qd2")
            for x in range(16):
                gx = x if left else x + 16
                if 3 <= gx <= 28:
                    d.px(x, 11, "qd3")
        elif kind == "lyre":
            H.put(d, 3, 1, [
                "..KKKKKKKK..",
                ".K33333333K.",
                "K3c3c3c3c33K",
                "K33333333332",
                "K2c3c3c3c32K",
                ".K22222222K.",
                "..KKKKKKKK..",
            ], {**CAVE, "c": "qd4"})
            for x in (5, 7, 9, 11):
                d.vline(x, 8, 12, "qe3")
            d.vline(4, 8, 13, "qd1")
            d.vline(12, 8, 13, "qd1")
            d.hline(4, 12, 13, "qd1")
            d.px(9, 3, "ink")
            d.px(10, 4, "ink")
        else:
            # the herm's face carved in the rock: brow, eyes, nose, a curled beard
            H.put(d, 3, 1, [
                "...KKKKKK...",
                "..K444443K..",
                ".K44444433K.",
                ".K4K44K433K.",
                ".K4444443K..",
                ".K44K44433K.",
                "..K444433K..",
                "..K3c3c32K..",
                "..K3c3c32K..",
                "...Kc3c2K...",
                "....KKKK....",
            ], {**CAVE, "c": "qd2"})
        H_cave_recolor(d)
        P.place(s, "bottom", cx, 0, d)
    # the altar of Hermes, two cells wide, on the floor
    alt = H.Layer(32, 16)
    for y in range(16):
        for x in range(32):
            alt.px(x, y, floor_px(x, y))
    H.put(alt, 2, 2, [
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "K5555555554444444444333333K.",
        "K5444444444444444433333322K.",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        ".K4444444444444443333332K...",
        ".K44443zz3444444z43333322K..",
        ".K4443z33z34444z3z3333322K..",
        ".K44443zz3444444z43333322K..",
        ".K4444433344444433333332K...",
        ".K4444444444444433333322K...",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKK.",
        "K55544444444444443333222K...",
        "KKKKKKKKKKKKKKKKKKKKKKKKK...",
    ], {"K": "ink", "5": "qm2", "4": "qm3", "3": "qm4", "2": "qm5", "z": "qz"})
    # an offering: a little heap of barley cakes and a sprig
    H.put(alt, 10, 1, ["cc.v", "ccvv"], {"c": "qe3", "v": "qv2"})
    P.place(s, "bottom", 4, 0, H.Layer(16, 16))
    s.B.a[0:16, 64:96] = alt.a
    # the lamp on its bronze stand, flame lit
    d = P.L16()
    for y in range(16):
        for x in range(16):
            d.px(x, y, floor_px(x, y))
    H.put(d, 5, 1, [
        "...y..",
        "..yYy.",
        "..KcK.",
        ".KccK.",
        "KcccccK"[:6],
        ".KKKK.",
        "..zK..",
        "..zK..",
        "..zK..",
        "..zK..",
        ".zzzK.",
        "KKKKKK",
    ], {"K": "ink", "y": "qy", "Y": "qm2", "c": "qc2", "z": "qd2"})
    P.place(s, "bottom", 6, 0, d)
    # a water jar
    d = P.L16()
    for y in range(16):
        for x in range(16):
            d.px(x, y, floor_px(x, y))
    H.put(d, 4, 2, ["..KKKK..", ".KccccK.", "KcCccccK", "KcCccccK", "KcCcccCK", ".KcccCK.",
                    ".KccCCK.", "..KKKK.."], {"K": "ink", "c": "qc2", "C": "qc1"})
    P.place(s, "bottom", 7, 0, d)
    # her stool
    d = P.L16()
    for y in range(16):
        for x in range(16):
            d.px(x, y, floor_px(x, y))
    H.put(d, 3, 4, ["KKKKKKKKKK", "KwwwwwwwwK", "KWWWWWWWWK", "KKKKKKKKKK", ".K.K..K.K.",
                    ".K.K..K.K.", ".K......K."], {"K": "ink", "w": "wd2", "W": "wd1"})
    P.place(s, "bottom", 0, 1, d)
    # a seep in the floor
    d = P.L16()
    for y in range(16):
        for x in range(16):
            d.px(x, y, floor_px(x, y))
            if ((x - 7.5) / 5) ** 2 + ((y - 8) / 3) ** 2 <= 1:
                d.px(x, y, "qd2" if (x + y) % 3 else "qd3")
    P.place(s, "bottom", 1, 1, d)
    # unused tail
    for cx in range(2, 8):
        d = P.L16()
        for y in range(16):
            for x in range(16):
                d.px(x, y, floor_px(x, y))
        P.place(s, "bottom", cx, 1, d)
    return s


def G_foot(d):
    """Darken a back-wall cell's foot, as the face painter's foot row does."""
    for y in range(12, 16):
        for x in range(16):
            c = d.get(x, y)
            if c in RAMP:
                d.px(x, y, RAMP[max(0, RAMP.index(c) - 1)])
    for x in range(16):
        d.px(x, 15, "qd0")


def H_cave_recolor(d):
    pass


def build():
    out = [cwall(), cface(), cfloor(), maia()]
    m = out[-1]
    out[-1] = H.crop(m, "maia", m.title, ["cradle_L", "cradle_R", "lyre", "herm_face", "altar_L",
                                          "altar_R", "lamp", "jar", "stool", "spring"])
    return out
