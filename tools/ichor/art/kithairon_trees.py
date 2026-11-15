"""Kithairon's trees: black firs, scrub oak, wild pear, and Pentheus's fir.

Light from the top left. Every tree stands on borrowed aethos grass, so its
grass costs no tiles; a fir's spire pokes into the row above it, which is a
walk-behind cell (top layer), as aethos's olives do.

  fir, fir_b      a tall black fir and a slimmer one: tip row (T), crown, base
  fir_stack(_b)   a fir's base row with the next fir's spire over it, for woods
                  where firs stand one behind another (a column of firs then
                  repeats crown, stack, crown, stack... and ends with a base)
  fir_young       a young fir, 1 x 2, top half drawn over the player
  oak, pear       2 x 2 broadleaves: scrub oak, and a wild pear in flower
  pentheus_fir    the enormous fir with one great branch torn away (beat 28)
"""
from __future__ import annotations

import numpy as np

import kithairon_lib as K

SEC = "trees"


def _fir_mask(w, h, apex, tiers, cx):
    """A fir's silhouette: tiers of drooping boughs, each a triangle widening
    downward with a scalloped lower edge."""
    m = np.zeros((h, w), bool)
    for (y0, y1, hw) in tiers:
        for y in range(y0, y1):
            t = (y - y0 + 1) / (y1 - y0)
            half = hw * t
            for x in range(w):
                d = abs(x + 0.5 - cx)
                # the tier's ragged lower edge: bough tips droop at its sides
                if d <= half and not (y > y1 - 3 and ((x + y) % 3 == 0) and d > half - 3):
                    m[y, x] = True
    m[:apex] = False
    return m


def paint_fir(L, ox, oy, w, h, tiers, cx, trunk_y, light=0):
    m = _fir_mask(w, h, tiers[0][0], tiers, cx)
    # tier membership, for the shading under each tier
    for y in range(h):
        for x in range(w):
            if not m[y, x]:
                continue
            d = (x + 0.5 - cx)
            # which tier's lower edge is nearest below
            shade = False
            for (y0, y1, hw) in tiers[:-1]:
                if y1 - 3 <= y < y1 + 1 and abs(d) <= hw:
                    shade = True
            lit = d < -1.5 - (y % 3 == 0)
            edge = not (0 < y < h - 1 and 0 < x < w - 1 and m[y - 1, x] and m[y, x - 1] and m[y, x + 1])
            if edge:
                c = "fr0" if d > -2 else "fr1"
            elif shade:
                c = "fr0" if d > 0 else "fr1"
            elif lit:
                c = "fr3" if (x * 2 + y) % 5 == 0 else "fr2"
            elif d > 3:
                c = "fr1" if (x + y) % 4 else "fr0"
            else:
                c = "fr2" if (x * 3 + y) % 4 == 0 else "fr1"
            if light and c == "fr1" and (x + 2 * y) % 3 == 0:
                c = "fr2"
            L.px(ox + x, oy + y, c)
    # the trunk and its shadow
    for y in range(trunk_y, trunk_y + 4):
        for x in range(int(cx) - 2, int(cx) + 2):
            if not m[y, x]:
                L.px(ox + x, oy + y, "k1" if x < cx else "fr0")
    return m


FIR_TIERS = [(5, 18, 6.5), (11, 29, 10.5), (21, 42, 15.0)]
FIR_B_TIERS = [(4, 16, 5.0), (10, 27, 8.5), (19, 41, 12.5)]


def _fir_struct(key, title, tiers, light):
    s = K.struct(key, title, 2, 3, SEC, walk=["TT", "XX", "XX"], on="grass",
                 notes="A black fir. The top row is its spire over the grass of the row "
                       "above: walkable, drawn over the player. Rows 1-2 block.")
    # spire on the top layer, the rest on the middle layer
    tmp = K.Layer(32, 48)
    paint_fir(tmp, 0, 0, 32, 48, tiers, 16.0, 42, light)
    _shadow(tmp)
    s.T.a[0:16] = tmp.a[0:16]
    s.M.a[16:48] = tmp.a[16:48]
    return s, tmp


def _shadow(L, y0=43, y1=48):
    """A soft shadow on the grass round the fir's foot, dithered."""
    for y in range(y0, y1):
        for x in range(4, 29):
            if L.a[y, x, 3]:
                continue
            d = ((x - 16.5) / 13.0) ** 2 + ((y - 44.0) / 3.6) ** 2
            if d <= 1 and (x + y) % 2 == 0:
                L.px(x, y, "gd")


def firs():
    a, ta = _fir_struct("fir", "Black fir (2 x 3 with its spire)", FIR_TIERS, 0)
    b, tb = _fir_struct("fir_b", "Slim fir (2 x 3 with its spire)", FIR_B_TIERS, 1)
    out = [a, b]
    # stacks: a base row with the next fir's spire drawn over it
    for key, base, tip in (("fir_stack", ta, ta), ("fir_stack_b", tb, tb)):
        s = K.struct(key, "A fir's base with the next fir's spire over it", 2, 1, SEC,
                     walk=["XX"], on="grass",
                     notes="Between two firs in a column: the upper fir's base row, the "
                           "lower fir's spire over it. Blocks.")
        s.M.a[:] = base.a[32:48]
        sp = tip.a[0:16]
        msk = sp[..., 3] > 0
        s.M.a[msk] = sp[msk]
        out.append(s)
    # a young fir, one cell wide
    y = K.struct("fir_young", "Young fir (1 x 2)", 1, 2, SEC, walk=["T", "X"], on="grass",
                 notes="A sapling fir for gaps at the woods' edge. Its top half is drawn over "
                       "the player.")
    tmp = K.Layer(16, 32)
    paint_fir(tmp, 0, 0, 16, 32, [(3, 13, 4.0), (9, 22, 5.5), (16, 29, 7.5)], 8.0, 27, 1)
    for yy in range(29, 32):
        for xx in range(3, 13):
            if not tmp.a[yy, xx, 3] and (xx + yy) % 2 == 0:
                tmp.px(xx, yy, "gd")
    y.T.a[0:16] = tmp.a[0:16]
    y.M.a[16:32] = tmp.a[16:32]
    out.append(y)
    return out


def _crown(L, ox, oy, w, h, blobs, ramp, rim, speck=None):
    """A broadleaf crown from overlapping round blobs, lit from the top left."""
    m = np.zeros((h, w), bool)
    for (cx, cy, rx, ry) in blobs:
        m |= K.ellipse_mask(w, h, cx, cy, rx, ry)
    for y in range(h):
        for x in range(w):
            if not m[y, x]:
                continue
            # light from the nearest blob's centre
            best = min(blobs, key=lambda b: ((x - b[0]) / b[2]) ** 2 + ((y - b[1]) / b[3]) ** 2)
            u = (x - best[0]) / best[2] + (y - best[1]) / best[3]
            c = ramp[0] if u > 0.75 else (ramp[1] if u > -0.1 else ramp[2])
            if speck and (x * 7 + y * 5) % 13 == 0 and u < 0.4:
                c = speck
            L.px(ox + x, oy + y, c)
    edge = m & ~(np.pad(m, 1)[:-2, 1:-1] & np.pad(m, 1)[2:, 1:-1] & np.pad(m, 1)[1:-1, :-2]
                 & np.pad(m, 1)[1:-1, 2:])
    for y, x in np.argwhere(edge):
        L.px(ox + x, oy + y, rim)
    return m


def broadleaves():
    out = []
    oak = K.struct("oak", "Scrub oak (2 x 2)", 2, 2, SEC, walk=["XX", "XX"], on="grass",
                   notes="A low, wide kermes oak of the mountain's lower slopes.")
    M = oak.M
    # trunk
    for y in range(20, 30):
        for x in range(14, 18):
            M.px(x, y, "k1" if x < 16 else "k2" if y < 23 else "k1")
    M.px(12, 27, "k1"); M.px(13, 26, "k1"); M.px(19, 26, "k1"); M.px(20, 27, "k1")
    _crown(M, 0, 0, 32, 32, [(10, 12, 9, 8), (21, 11, 9, 8), (16, 6, 9, 6), (15, 17, 12, 6)],
           ["oa1", "oa2", "oa3"], "iv0" if False else "fr1", speck="oa3")
    # shadow
    for y in range(28, 32):
        for x in range(6, 27):
            if not M.a[y, x, 3] and (x + y) % 2 == 0:
                M.px(x, y, "gd")
    out.append(oak)
    pear = K.struct("pear", "Wild pear in flower (2 x 2)", 2, 2, SEC, walk=["XX", "XX"],
                    on="grass", notes="A wild pear, white with blossom: the mountain's spring.")
    M = pear.M
    for y in range(18, 30):
        for x in range(15, 18):
            M.px(x, y, "k1" if x < 16 else "k2")
    M.px(13, 21, "k1"); M.px(14, 20, "k1"); M.px(19, 20, "k1"); M.px(20, 19, "k1")
    _crown(M, 0, 0, 32, 32, [(11, 11, 7, 7), (21, 10, 7, 7), (16, 5, 7, 5), (16, 15, 9, 5)],
           ["oa1", "oa2", "oa3"], "fr1")
    for (x, y) in ((8, 7), (12, 4), (18, 3), (22, 7), (25, 11), (10, 12), (15, 9), (20, 13),
                   (6, 11), (17, 16), (13, 15), (23, 15), (19, 6), (9, 9)):
        M.px(x, y, "w0")
        M.px(x + 1, y, "w0")
        M.px(x, y + 1, "k2")
    for y in range(28, 32):
        for x in range(8, 25):
            if not M.a[y, x, 3] and (x + y) % 2 == 0:
                M.px(x, y, "gd")
    out.append(pear)
    return out


def pentheus_fir():
    s = K.struct("pentheus_fir", "Pentheus's fir: the enormous one", 3, 4, SEC,
                 walk=["TTT", "XXX", "XXX", "XXX"], on="grass",
                 notes="An enormous old fir, one great branch torn away high up (beat 28). "
                       "The top row is its spire, drawn over the player. Put the landmark's "
                       "sign on its bottom middle cell.")
    tmp = K.Layer(48, 64)
    tiers = [(3, 18, 7.0), (10, 31, 12.5), (20, 45, 18.0), (32, 59, 23.5)]
    paint_fir(tmp, 0, 0, 48, 64, tiers, 24.0, 58, 0)
    # the torn branch: a gap bitten out of the second tier's east side, a pale
    # splintered stump and a hanging broken bough
    hole = np.zeros((64, 48), bool)
    for y in range(19, 31):
        for x in range(30, 40):
            if (x - 37) ** 2 / 20 + (y - 25) ** 2 / 26 < 1:
                hole[y, x] = True
    tmp.a[hole] = 0
    # the bitten edge darkens: the boughs behind show in shadow
    for y, x in np.argwhere(K.halo(hole)):
        if tmp.a[y, x, 3]:
            tmp.px(x, y, "fr0")
    # a pale splintered stump where the branch tore off
    K.put(tmp, 30, 23, ["Kk", "kww", "Kw."], {"k": "k2", "K": "k1", "w": "w0"})
    # the broken bough, hanging down beside the trunk
    for i in range(6):
        tmp.px(32 + i // 3, 32 + i, "k1")
    K.put(tmp, 31, 37, [".f.", "fff", "f.f"], {"f": "fr1"})
    # shadow at the foot
    for y in range(59, 64):
        for x in range(6, 43):
            if not tmp.a[y, x, 3] and (x + y) % 2 == 0 and ((x - 24) / 18) ** 2 + ((y - 60) / 4) ** 2 < 1:
                tmp.px(x, y, "gd")
    s.T.a[0:16] = tmp.a[0:16]
    s.M.a[16:64] = tmp.a[16:64]
    return s


def meadow():
    """Small walkable details for the mountain's open grass: white narcissus,
    yellow mountain crocus, and a tussock. On borrowed grass."""
    s = K.struct("meadow", "Meadow flowers and a tussock", 3, 1, SEC, walk=["..."], on="grass",
                 names={"white": (0, 0), "yellow": (1, 0), "tuft": (2, 0)},
                 notes="Walkable. Scatter through open grass with aethos's red anemones "
                       "(0x004): `white` narcissus, `yellow` mountain crocus, `tuft` a tussock.")
    M = s.M
    for (x, y) in ((3, 4), (10, 2), (7, 9), (13, 11), (2, 12)):
        K.put(M, x, y, [".w.", "wkw", ".w.", ".o."], {"w": "w0", "k": "k2", "o": "oa1"})
    for (x, y) in ((4, 3), (11, 6), (6, 11), (13, 13)):
        K.put(s.layers["middle"], 16 + x, y, [".y.", "yKy", ".i."],
              {"y": "mk", "K": "rk4", "i": "iv1"})
    for (x, y) in ((3, 6), (9, 3), (10, 10)):
        K.put(M, 32 + x, y, ["3.3.3", "13131", "11111", ".t.t."],
              {"3": "t3", "1": "t1", "t": "t0"})
    return s


def build():
    return firs() + broadleaves() + [pentheus_fir(), meadow()]
