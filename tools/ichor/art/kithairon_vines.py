"""The god's vines on the Eleutherai Road: trellised vine rows, the old vines
grown across the road and their cut stumps, the stone wine press and its
treading floor, and the wine-cart with the broken wheel.

Light from the top left; things outlined in ink; small pieces stand on
borrowed aethos grass or road, so their ground costs no tiles.
"""
from __future__ import annotations

import numpy as np

import kithairon_lib as K

SEC = "vines"


def _leaf_clump(L, cx, cy, r, seed):
    """A vine's leaves: a ragged clump of lobed leaves, lit from the top left."""
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            jag = (K.hsh(x, y, seed) % 3) * 0.5
            if d <= r + jag - 0.5:
                u = (x - cx) + (y - cy)
                c = "lf2" if u < -r * 0.6 else ("lf1" if u < r * 0.5 else "lf0")
                if K.hsh(x, y, seed + 1) % 11 == 0:
                    c = "lf0"
                L.px(x, y, c)


def _grapes(L, x, y):
    K.put(L, x, y, [
        "2K.",
        "121",
        "011",
        ".10",
        ".0.",
    ], {"2": "gp2", "1": "gp1", "0": "gp0", "K": "wd1"})


def trellis():
    """A vine row on its trellis, running east-west: chestnut posts, two wires,
    the vines along them heavy with leaf and (in `grapes` cells) bunches."""
    s = K.struct("trellis", "Vine row on a trellis (east-west)", 4, 1, SEC, walk=["XXXX"],
                 on="grass", names={"W": (0, 0), "M": (1, 0), "grapes": (2, 0), "E": (3, 0)},
                 notes="A row of the god's vines. `W` and `E` end the row with a post; `M` "
                       "and `grapes` repeat between (mix them). Rows block: leave a lane "
                       "between rows, or plant tall grass there.")
    M = s.M
    for i, k in enumerate(("W", "M", "grapes", "E")):
        ox = i * 16
        x0 = 4 if k == "W" else 0
        x1 = 12 if k == "E" else 16
        # the shadow on the grass under the row
        for x in range(ox + x0, ox + x1):
            for y in (13, 14):
                if (x + y) % 2 == 0:
                    M.px(x, y, "gd")
        # leaves along the wires
        for j, cx in enumerate(range(ox + x0 + 2, ox + x1, 5)):
            _leaf_clump(M, cx, 7 + (j % 2), 4, 3 + i * 7 + j)
        # posts at the row's ends, wires showing between the leaves
        for x in range(ox + x0, ox + x1):
            for y in (5, 9):
                if not M.a[y, x, 3]:
                    M.px(x, y, "wd2")
        for px in ([ox + 4] if k == "W" else []) + ([ox + 11] if k == "E" else []):
            for y in range(2, 14):
                M.px(px, y, "wd2" if y < 12 else "wd1")
                M.px(px + 1, y, "wd1")
            M.px(px, 1, "ink")
            M.px(px + 1, 1, "ink")
        if k == "grapes":
            _grapes(M, ox + 3, 8)
            _grapes(M, ox + 10, 9)
        elif k == "M":
            _grapes(M, ox + 7, 9)
    return s


def old_vines():
    """The wall of old vines grown across the road, thick as rope (beat 26),
    and what the Sickle leaves of them."""
    s = K.struct("old_vines", "The old vines across the road, and their cut stumps", 3, 1, SEC,
                 walk=["XXX"], on="path",
                 names={"vines": (0, 0), "vines_b": (1, 0), "stumps": (2, 0)},
                 notes="On borrowed road. `vines` and `vines_b` alternate across the road "
                       "and block; when Demeter's Sickle cuts them, swap each for `stumps` "
                       "(walkable): METATILE_Kithairon_OldVines_* and _Stumps.")
    s.walk = ["XX."]
    M = s.M
    for i in range(2):
        ox = i * 16
        # gnarled trunks, rope-thick, twisting up and across
        for t, (x0, ph) in enumerate(((2 + i, 0.0), (8 - i, 1.7), (13, 3.1))):
            for y in range(0, 16):
                x = ox + x0 + int(round(1.6 * np.sin(y / 2.6 + ph)))
                for dx in range(2):
                    M.px(x + dx, y, "wd1" if dx == 0 else "wd2")
                M.px(x - 1, y, "ink")
                M.px(x + 2, y, "ink")
        for (cx, cy, r) in ((ox + 4, 3, 4), (ox + 12, 5, 4), (ox + 7, 10, 4), (ox + 2, 13, 3),
                            (ox + 14, 13, 3)):
            _leaf_clump(M, cx, cy, r, 20 + i * 5 + cx)
        _grapes(M, ox + 9 - i * 4, 4)
    # the stumps: three pale cut ends in the road, and cut leaves lying about
    ox = 32
    for (x, y) in ((3, 6), (9, 3), (12, 10)):
        K.put(M, ox + x, y, [
            ".KKK.",
            "KwwdK",
            "KdwwK",
            "K112K",
            ".KKK.",
        ], {"K": "ink", "w": "wd2", "d": "wd1", "1": "wd1", "2": "wd2"})
    for (x, y) in ((2, 13), (8, 12), (13, 3), (6, 1)):
        K.put(M, ox + x, y, ["21", ".0"], {"2": "lf2", "1": "lf1", "0": "lf0"})
    return s


def press():
    """The stone wine press: a raised treading floor stained purple, a lip
    with a spout, the sunken vat below it, a basket of grapes by the steps."""
    s = K.struct("press", "Stone wine press and treading floor", 3, 2, SEC,
                 walk=["XXX", "XXX"], on="grass",
                 notes="A treading floor of dressed stone, purple with years of must, "
                       "draining through a spout into a sunken vat. Its sign is the press "
                       "(\"Tread barefoot...\").")
    M = s.M
    # the floor: a stone basin, 40 x 22, raised on a plinth
    for y in range(2, 26):
        for x in range(3, 45):
            edge = x in (3, 4, 43, 44) or y in (2, 3, 24, 25)
            if edge:
                c = "cy4" if (y in (2, 3) or x in (3, 4)) else "cy1"
            else:
                c = "gp1" if (K.hsh(x, y, 1) % 5) else "gp0"
                if (x - 24) ** 2 / 90 + (y - 13) ** 2 / 40 < 1 and K.hsh(x, y, 2) % 3 == 0:
                    c = "gp0"
            M.px(x, y, c)
    for x in range(3, 45):
        M.px(x, 1, "ink")
        M.px(x, 26, "ink")
    for y in range(1, 27):
        M.px(2, y, "ink")
        M.px(45, y, "ink")
    # the plinth's south face
    for y in range(26, 30):
        for x in range(4, 44):
            M.px(x, y, "cy2" if (x // 6 + y) % 2 else "cy1")
    M.hline(4, 43, 30, "ink")
    # the spout and the vat
    K.put(M, 20, 25, ["KccK", "KcpK", ".Kp.", ".KpK"], {"K": "ink", "c": "cy3", "p": "gp1"})
    K.put(M, 16, 29, [
        ".KKKKKKKKKK.",
        "KcccccccccccK"[:12],
        "Kcp0000000pK",
        ".KKKKKKKKKK.",
    ], {"K": "ink", "c": "cy3", "p": "cy2", "0": "gp0"})
    # footprints in the must
    for (x, y) in ((10, 8), (14, 12), (30, 9), (34, 14), (22, 18)):
        K.put(M, x, y, ["00", "0.", "00"], {"0": "gp0"})
    # a basket of grapes by the east end
    K.put(M, 37, 18, [
        ".2112.",
        "211101",
        "K1001K",
        "KwwwwK",
        ".KKKK.",
    ], {"2": "gp1", "1": "gp1", "0": "gp0", "K": "ink", "w": "l0"})
    # grass shadow along the foot
    for x in range(6, 46):
        if x % 2 == 0:
            M.px(x, 31, "gd")
    return s


def cart():
    """The wine-cart with the broken wheel, tipped onto its axle, forty jars
    roped in its bed (two have rolled off)."""
    s = K.struct("cart", "The wine-cart with the broken wheel", 3, 2, SEC,
                 walk=["XXX", "XXX"], on="grass",
                 notes="Tipped onto its axle on the third terrace: a cart of amphorae "
                       "for the Dionysia, its east wheel off and lying flat. The driver "
                       "stands beside it.")
    M = s.M
    # the bed: planks, tipped down to the east
    for x in range(4, 40):
        tilt = (x - 4) // 9
        for y in range(10 + tilt, 22 + tilt):
            c = "wd2" if (y - tilt) in (10, 11) else ("wd1" if (x // 5) % 2 else "wd2")
            if (y - tilt) == 21:
                c = "ink"
            M.px(x, y, c)
        M.px(x, 9 + tilt, "ink")
    for y in range(9, 22):
        M.px(3, y, "ink")
    for y in range(13, 26):
        M.px(40, y, "ink")
    # the jars, standing in rows in the bed
    for j, x in enumerate(range(6, 38, 5)):
        tilt = (x - 4) // 9
        K.put(M, x, 4 + tilt + (j % 2), [
            ".KK.",
            "K21K",
            "K21K",
            "K221K"[:4],
            ".K1K",
            "..K.",
        ], {"K": "ink", "2": "tc2", "1": "tc1"})
    # the west wheel, still on
    for y in range(18, 30):
        for x in range(4, 16):
            d = ((x - 9.5) / 5.5) ** 2 + ((y - 24) / 5.5) ** 2
            if 0.55 < d <= 1:
                M.px(x, y, "wd1" if d < 0.8 else "ink")
            elif d <= 0.55 and (x == 9 or y == 24 or x == 10):
                M.px(x, y, "wd2")
    # the east wheel, off and flat on the grass
    K.put(M, 36, 24, [
        "..KKKKKK..",
        ".KwwddwwK.",
        "KwdKKKKdwK",
        ".KwwddwwK.",
        "..KKKKKK..",
    ], {"K": "ink", "w": "wd2", "d": "wd1"})
    # two jars rolled off into the grass
    K.put(M, 22, 25, ["KKKKK.", "K2111K", "K2111KK", ".KKKKK."], {"K": "ink", "2": "tc2", "1": "tc1"})
    K.put(M, 29, 28, ["KKKK.", "K211K", ".KKKK"], {"K": "ink", "2": "tc2", "1": "tc1"})
    # the shaft resting on the ground to the west
    for x in range(0, 5):
        M.px(x, 20 + x // 3, "wd1")
        M.px(x, 21 + x // 3, "ink")
    return s


def barrier():
    """The herald's barrier: a pole across the road on two trestles, an ivy
    garland twisted round it (beat 26). He lifts it and walks off with it."""
    s = K.struct("barrier", "The herald's barrier pole across the road", 2, 1, SEC, walk=["XX"],
                 on="path", names={"W": (0, 0), "E": (1, 0)},
                 notes="On borrowed road, across a two-wide road: `W` then `E`. Blocks. When "
                       "the herald lifts it, swap both cells back to road "
                       "(METATILE_Kithairon_Barrier_W/_E, aethos's road 0x1D9).")
    M = s.M
    # the trestles: an X of poles at each end
    for ox in (2, 26):
        for i in range(9):
            M.px(ox + i // 2, 4 + i, "wd1")
            M.px(ox + 4 - i // 2, 4 + i, "wd2")
        M.px(ox + 1, 13, "ink")
        M.px(ox + 4, 13, "ink")
    # the pole, with an ivy garland round it
    for x in range(1, 31):
        M.px(x, 6, "ink")
        M.px(x, 7, "wd2")
        M.px(x, 8, "wd1")
        M.px(x, 9, "ink")
        if x % 6 in (1, 2):
            M.px(x, 7, "lf1")
            M.px(x + 1, 8, "lf0")
    M.px(0, 7, "ink")
    M.px(0, 8, "ink")
    M.px(31, 7, "ink")
    M.px(31, 8, "ink")
    for x in range(3, 30):
        if x % 2:
            M.px(x, 14, "wd1")
    return s


def build():
    return [trellis(), old_vines(), press(), cart(), barrier()]
