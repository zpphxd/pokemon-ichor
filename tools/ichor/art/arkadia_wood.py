"""gTileset_ArkadiaWood: the Cypress Wood and the Pool of Mnemosyne.

The Wood is always in deep shade: its floor and its canopy are drawn dark in
their own palettes, so the new moon never depends on the clock (SCRIPT.md Open
questions 1). The stump clearing is the one place the sky shows through: its
floor is pale with starlight. The Pool's glade opens to the sky on aethos grass.

Each 8x8 tile of each layer draws from one of arkadia_lib.WOOD_GROUPS.
"""
from __future__ import annotations

import numpy as np

import arkadia_lib as L
import arkadia_trees as TR

SEC = "wood"


def floor_px(x, y, variant=0):
    """The Wood's floor: fallen needles in deep shade, 16 px periodic."""
    xx, yy = x % 16, y % 16
    h = L.hsh(xx, yy, 21 + variant) % 100
    # short needle strokes running every which way
    if (xx * 3 + yy * 5) % 11 == 0 or (xx * 7 + yy) % 13 == 0:
        return "wf2"
    if h < 7:
        return "wf0"
    if h > 96:
        return "wf3"
    return "wf1"


def clearing_px(x, y, variant=0):
    """The stump clearing: short moss and grass under the open sky, brighter than
    the shaded floor, with dew catching the starlight here and there. (Pass 2: a
    grey-blue floor read as a pond in the render; moss green reads as ground.)"""
    xx, yy = x % 16, y % 16
    h = L.hsh(xx, yy, 31 + variant) % 100
    if h < 1:
        return "ws2"
    if h < 3:
        return "ws1"
    # tufts of grass: short upright strokes
    if (xx * 5 + yy * 3) % 13 == 0 or ((xx * 7 + yy * 11) % 17 == 0 and yy % 2 == 0):
        return "wn1"
    if h > 86 or (xx + yy * 2) % 9 == 0:
        return "wf2"
    return "wn0"


def floor():
    names = {"plain": (0, 0), "roots": (1, 0), "needles": (2, 0), "lit": (3, 0), "lit2": (4, 0),
             "mats": (5, 0), "dig": (6, 0)}
    s = L.struct("floor", "The Wood's floor", 7, 1, SEC, walk=["......."], names=names,
                 notes="The floor in deep shade (`plain`, `roots` where a tree's roots cross, "
                       "`needles` a drift of them); the stump clearing's starlit floor (`lit`, "
                       "`lit2`); `mats`, the floor brightening toward the gate "
                       "(MB_SOUTH_ARROW_WARP: the way back to Arkadia, on the bottom row); `dig`, "
                       "turned earth (a dig spot).")
    B = s.B
    for cx in range(7):
        for y in range(16):
            for x in range(16):
                if cx in (3, 4):
                    c = clearing_px(x, y, cx)
                else:
                    c = floor_px(x, y, cx)
                B.px(cx * 16 + x, y, c)
    # roots: two runs of bark crossing the cell
    for x in range(16):
        y = 5 + int(2 * np.sin(x * 0.5))
        B.px(16 + x, y, "wb0")
        B.px(16 + x, y + 1, "wf0")
        if x > 6:
            B.px(16 + x, 11 + (x - 6) // 3, "wb0")
    # a drift of needles
    for (x, y) in ((3, 4), (4, 4), (5, 5), (9, 9), (10, 9), (11, 10), (6, 12), (7, 12), (12, 3)):
        B.px(32 + x, y, "wf3")
    # the gate's mats: the floor lightening toward the town
    for y in range(16):
        for x in range(16):
            c = floor_px(x, y, 5)
            k = y + (L.hsh(x, y, 9) % 4) - 1
            if k > 7:
                c = "wf2"
            if k > 11:
                c = "wf3"
            if k > 14:
                c = "ws0"
            B.px(80 + x, y, c)
    s.behaviors[(5, 0)] = "MB_SOUTH_ARROW_WARP"
    # turned earth
    for (x, y) in ((4, 5), (7, 6), (10, 5), (5, 9), (9, 10), (12, 9), (7, 12)):
        B.blit(["23", "02"], {"0": "wf0", "2": "wf3", "3": "wf2"}, 96 + x, y)
    return s


def ferns():
    """The Wood's tall grass: clumps of fern on the needle floor."""
    s = L.struct("ferns", "Ferns (the Wood's tall grass)", 2, 1, SEC, walk=["GG"],
                 names={"a": (0, 0), "b": (1, 0)},
                 notes="Clumps of bracken on the dark floor, each self-contained so any outline "
                       "works: `a` and `b`, alternate them. MB_TALL_GRASS.")
    B = s.B
    for cx in range(2):
        for y in range(16):
            for x in range(16):
                B.px(cx * 16 + x, y, floor_px(x, y, 7 + cx))
        # fronds: arcs out from a few crowns
        crowns = [(4, 6), (11, 5), (7, 12), (13, 13)] if cx == 0 else [(5, 4), (12, 8), (3, 12), (10, 14)]
        for (fx, fy) in crowns:
            for ang in range(-3, 4):
                for r in range(1, 6):
                    x = int(round(fx + ang * r * 0.45))
                    y = int(round(fy - r + abs(ang) * r * 0.18))
                    if 0 <= x < 16 and 0 <= y < 16:
                        B.px(cx * 16 + x, y, "wn1" if r < 3 and ang <= 0 else "wn0")
                        if r == 5 and 0 <= y + 1 < 16:
                            B.px(cx * 16 + x, y + 1, "wc1")
            B.px(cx * 16 + fx, fy, "wc1")
            if fy + 1 < 16:
                B.px(cx * 16 + fx, fy + 1, "wc0")
    for cx in range(2):
        s.behaviors[(cx, 0)] = "MB_TALL_GRASS"
    return s


def stump():
    s = L.struct("stump", "The stump", 1, 1, SEC, walk=["X"],
                 notes="An old cypress stump cut flat, on the clearing's starlit floor: where "
                       "Kleon sits (beat 42).")
    B = s.B
    for y in range(16):
        for x in range(16):
            B.px(x, y, clearing_px(x, y, 3))
    for y in range(3, 15):
        for x in range(2, 14):
            dx, dy = (x - 7.5) / 6, (y - 8.5) / 6
            r = dx * dx + dy * dy
            if y >= 9 and abs(x - 7.5) <= 6 and y <= 14:
                B.px(x, y, "wb0" if x < 9 else "wc1")
            if r <= 1 and y < 9 + 2:
                ring = int(r * 4)
                B.px(x, y, ("wf3", "wf2", "wf3", "wb0")[min(ring, 3)])
    B.px(7, 7, "wf2")
    for x in range(1, 15):
        B.px(x, 15, "wf0")
    return s


def tomb():
    """The Tomb of Kallisto: a high round mound ringed with old stones, the little
    shrine of Artemis Kalliste on top, a fallen trunk across its south face."""
    walk = ["XXXXX", "X.X..", "X....", "XXJJX"]
    s = L.struct("tomb", "The Tomb of Kallisto", 5, 4, SEC, walk=walk,
                 names={"shrine": (2, 1), "earth": (2, 2), "ledge": (2, 3)},
                 notes="The mound, 5x4: its top is walkable from the east (column 4, rows 1-2); "
                       "the shrine at (2,1) (an altar: Artemis's rites); the turned earth at "
                       "(2,2) (prophecy tablet #5's fixed dig); the fallen trunk across the "
                       "south face at (2,3)-(3,3) is a ledge down to the path (MB_JUMP_SOUTH).")
    B = s.B
    W, H = 80, 64
    for y in range(H):
        for x in range(W):
            B.px(x, y, floor_px(x, y))
    # the mound's top: an oval of mossy earth, brighter than the floor
    cx, cy = 40, 28
    for y in range(H):
        for x in range(W):
            dx, dy = (x - cx) / 40, (y - cy) / 22
            r = dx * dx + dy * dy
            if r <= 1 and y < 50:
                c = "wf2" if (x * 3 + y * 5) % 7 else "wf3"
                if (x + y * 3) % 17 == 0:
                    c = "ar0"
                B.px(x, y, c)
    # the south face: banked earth with stones in it, darker to the foot
    for y in range(44, 62):
        for x in range(3, 77):
            dx = (x - cx) / 37
            top = 44 + 4 * dx * dx
            if y >= top:
                d = y - top
                c = "wf1" if d < 10 else "wf0"
                if (x * 7 + y * 3) % 19 == 0:
                    c = "rk2"
                if (x * 5 + y) % 23 == 0:
                    c = "rk1"
                B.px(x, y, c)
    # the ring of old standing stones round the top
    for ang in range(0, 360, 26):
        a = np.radians(ang)
        sx, sy = int(cx + 37 * np.cos(a)), int(cy + 19 * np.sin(a))
        if sy > 44:
            continue
        for y in range(sy - 4, sy + 2):
            for x in range(sx - 1, sx + 2):
                if 0 <= x < W and 0 <= y < H:
                    B.px(x, y, "rk3" if x == sx - 1 else ("rk2" if y < sy + 1 else "rk1"))
    # the east slope: a worn track up onto the top
    for y in range(16, 48):
        for x in range(64, 80):
            if (x - 64) + (y - 16) * 0.2 > 2:
                B.px(x, y, "wf2" if (x + y) % 5 else "wf3")
    # the shrine: a little marble aedicule on a stone base, a crescent on it
    ox, oy = 32, 16
    for y in range(2, 16):
        for x in range(3, 13):
            if y > 12:
                c = "rk2"
            elif y < 5:
                c = "am1" if abs(x - 7.5) < (y - 1) * 2 else None
            else:
                c = "am1" if x < 7 else "am3"
                if 5 <= x <= 10 and 6 <= y <= 11:
                    c = "ink" if y > 7 else "am3"
            if c:
                B.px(ox + x, oy + y, c)
    for (x, y) in ((7, 8), (6, 9), (6, 10), (7, 11), (8, 11)):
        B.px(ox + x, oy + y, "av1")
    # the turned earth by the shrine
    ox, oy = 32, 32
    for (x, y) in ((3, 4), (6, 3), (9, 5), (4, 8), (8, 9), (11, 7), (6, 12)):
        B.blit(["23", "02"], {"0": "wf0", "2": "wf3", "3": "rk3"}, ox + x, oy + y)
    # the fallen trunk across the face: a ledge to hop down
    for y in range(50, 58):
        for x in range(26, 58):
            c = "wb0" if y < 55 else "wf0"
            if y == 50:
                c = "rk3"
            if (x * 3) % 11 == 0 and y < 55:
                c = "wf1"
            B.px(x, y, c)
    for y in range(49, 59):
        B.px(26, y, "rk2")
        B.px(57, y, "wf0")
    s.behaviors[(2, 3)] = "MB_JUMP_SOUTH"
    s.behaviors[(3, 3)] = "MB_JUMP_SOUTH"
    return s


def kiln():
    """Agapenor's kiln in the Wood: an earth mound smoking under the trees."""
    s = L.struct("kiln_wood", "Agapenor's kiln", 2, 2, SEC, walk=["XX", "XX"],
                 notes="A charcoal kiln on the Wood's floor: an earth mound, its vents glowing, "
                       "smoke going up into the canopy. Its ash hides the Charcoal.")
    B = s.B
    for y in range(32):
        for x in range(32):
            B.px(x, y, floor_px(x, y, 4))
    for y in range(32):
        for x in range(32):
            dx, dy = (x - 15.5) / 14.5, (y - 21) / 11
            if dx * dx + dy * dy <= 1 and y >= 10:
                c = "wf3" if dx < -0.2 else ("wf1" if dx > 0.45 else "wf2")
                if dx * dx + dy * dy > 0.82:
                    c = "wf0"
                B.px(x, y, c)
    for (x, y) in ((8, 20), (16, 16), (24, 21), (12, 26), (21, 27)):
        B.blit(["kk", "kh"], {"k": "wc0", "h": "al1"}, x, y)
    for (x, y, c) in ((16, 12, "ws0"), (15, 10, "ws1"), (16, 8, "ws1"), (17, 6, "ws0"), (16, 4, "ws1"),
                      (15, 2, "ws1"), (17, 11, "ws1"), (14, 7, "ws0"), (16, 0, "ws0")):
        B.px(x, y, c)
        B.px(x + 1, y, c)
    return s


def stele():
    s = L.struct("stele", "A stone stele in the Wood", 1, 1, SEC, walk=["X"],
                 notes="A small stele on the Wood's floor, for its signs.")
    B = s.B
    for y in range(16):
        for x in range(16):
            B.px(x, y, floor_px(x, y, 6))
    for y in range(2, 15):
        for x in range(4, 12):
            c = "rk3" if x < 7 else "rk2"
            if y == 2 or x in (4, 11):
                c = "rk1"
            if y in (6, 8, 10) and 5 < x < 10:
                c = "rk1"
            B.px(x, y, c)
    B.hline(3, 12, 15, "ink")
    return s


# --------------------------------------------------------------------------
# The Pool of Mnemosyne
# --------------------------------------------------------------------------

def pool():
    """The Pool: perfectly still black water, its stars fixed, a kerb of pale stones."""
    s = L.struct("pool", "The Pool of Mnemosyne", 4, 3, "glade", walk=["XXXX"] * 3, on="grass",
                 names={"edge_w": (0, 1), "edge_s": (1, 2)},
                 notes="The round pool, 4x3 on grass: still black water reflecting stars that "
                       "never move, ringed by pale stones. Impassable; nothing lives in it.")
    M = s.M
    W, H = 64, 48
    cx, cy, rx, ry = 31.5, 23.5, 30, 21
    rng = np.random.RandomState(7)
    stars = {(int(x), int(y)) for x, y in zip(rng.randint(6, 58, 26), rng.randint(6, 42, 26))}
    for y in range(H):
        for x in range(W):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            r = (dx * dx + dy * dy) ** 0.5
            if r <= 0.84:
                c = "pb0"
                if r > 0.72:
                    c = "pb1"
                if dy < -0.45 and r > 0.6:
                    c = "pb1"
                if (x, y) in stars:
                    c = "w0" if (x + y) % 3 else "av1"
                M.px(x, y, c)
            elif r <= 1.0:
                # the kerb: pale stones, lit to the north-west
                k = int(np.degrees(np.arctan2(dy, dx)) // 18)
                c = "rk4" if dx + dy < 0 else "rk3"
                if k % 2:
                    c = "rk5" if dx + dy < -0.4 else ("rk3" if dx + dy < 0.4 else "rk2")
                if abs(r - 0.92) > 0.07 and (x + y) % 5 == 0:
                    c = "ink"
                M.px(x, y, c)
            elif r <= 1.08 and dy > 0.2:
                M.px(x, y, "gd" if (x + y) % 2 else None)
    # the brightest star, and its double in the water
    M.blit([" w ", "waw", " w "], {"w": "av1", "a": "w0"}, 19, 13)
    return s


def asphodel():
    """Asphodel in the glade's grass: the Pool's tall grass."""
    s = L.struct("asphodel", "Asphodel (the glade's tall grass)", 2, 1, "glade", walk=["GG"],
                 on="grass", names={"a": (0, 0), "b": (1, 0)},
                 notes="Pale asphodel spikes in grey-green leaves, on aethos grass: the glade's "
                       "tall grass, Arkoby country. Self-contained clumps: `a` and `b`, "
                       "alternate them. MB_TALL_GRASS.")
    M = s.M
    for cx in range(2):
        ox = cx * 16
        clumps = [(4, 12), (11, 9), (7, 4)] if cx == 0 else [(3, 7), (10, 13), (12, 4)]
        for (fx, fy) in clumps:
            for d in (-3, -2, -1, 1, 2, 3):
                for r in range(1, 4):
                    x, y = fx + d * r // 2, fy + 2 - r
                    if 0 <= x < 16 and 0 <= y < 16:
                        M.px(ox + x, y, "pg1" if d < 0 else "pg0")
            for y in range(max(0, fy - 6), fy + 2):
                M.px(ox + fx, y, "pg0")
            for y in range(max(0, fy - 6), fy - 1):
                M.px(ox + fx - 1, y, "pa0" if y % 2 else "pa1")
                M.px(ox + fx + 1, y, "pa0" if y % 2 == 0 else "pa1")
            if fy - 7 >= 0:
                M.px(ox + fx, fy - 7, "pa0")
            if fy + 2 < 16:
                M.px(ox + fx, fy + 2, "gd")
                M.px(ox + fx + 1, fy + 2, "gd")
        s.behaviors[(cx, 0)] = "MB_TALL_GRASS"
    return s


def seat():
    s = L.struct("seat", "The stone seat", 2, 1, "glade", walk=["XX"], on="grass",
                 names={"seat": (0, 0), "dig": (1, 0)},
                 notes="`seat`: the stone seat facing the water, where Mnaseas sits; `dig`: "
                       "turned earth in the grass (a dig spot; walkable).")
    s.walk = ["X."]
    M = s.M
    for y in range(4, 14):
        for x in range(1, 15):
            c = "rk4" if y < 7 else "rk3"
            if y == 4 or x in (1, 14):
                c = "ink" if y > 4 else "rk4"
            if y >= 11 and 4 <= x <= 11:
                c = None
            if c:
                M.px(x, y, c)
    for x in range(1, 15):
        M.px(x, 14, "gd")
    for (x, y) in ((4, 5), (7, 4), (10, 5), (5, 9), (9, 10), (12, 9), (7, 12)):
        M.blit(["43", "k4"], {"k": "pk0", "4": "rk4", "3": "rk3"}, 16 + x, y)
    return s


def build(shapes):
    out = [floor(), ferns(), stump(), tomb(), kiln(), stele(),
           TR.great_trunk(lambda x, y: floor_px(x, y, 2)),
           TR.wood_canopy(shapes["wood_canopy"], lambda x, y: floor_px(x, y, 0))]
    out += [TR.glade_canopy(shapes["pool_canopy"]), pool(), asphodel(), seat(),
            TR.poplar("poplar", False, 13), TR.poplar("poplar_b", True, 29)]
    return out
