"""The marsh people's gear: the fowlers' reed hide and their decoy nets on poles,
eel traps, the eel-smoker's rack and fire, a reed boat pulled up on the mud, a
heron's nest, the fishing step and jetty off the dike, the sluice's outflow,
lily pads. Pieces standing in water or reeds paint that ground on their bottom
layer for each phase, so they sway and glint with the beds around them.
"""
from __future__ import annotations

import numpy as np

import kopais_lib as K
import kopais_marsh as M

SEC = "gear"
G = {"K": "ink", "w": "wd1", "W": "wd2", "s": "st1", "S": "st2", "k": "k1", "f": "fi1",
     "F": "fi2", "m": "sm1", "M": "sm2", "e": "el", "g": "g1", "d": "gd"}


def water_bottom(L, ox, oy, phase):
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, M.water_px(x, y, phase))


def reed_bottom(L, ox, oy, phase):
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, M.reed_px(x, y, phase))


def mud_bottom(L, ox, oy):
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, M.mud_px(x, y))


def hide(phase=0):
    """A fowler's hide: a low hut of bundled reeds with a dark peep-slot."""
    s = K.struct("hide", "A fowler's reed hide", 2, 2, SEC, walk=["XX", "XX"],
                 names={"NW": (0, 0), "NE": (1, 0), "SW": (0, 1), "SE": (1, 1)},
                 notes="A fowler's hide of bundled reeds on grass, its peep-slot facing the "
                       "water. Blocks.")
    K.ground(s, "grass")
    L = s.M
    yy, xx = np.mgrid[0:32, 0:32]
    dome = (((xx - 15.5) / 14.0) ** 2 + ((yy - 20.0) / 13.0) ** 2 <= 1.0) & (yy < 29)
    for y, x in np.argwhere(dome):
        band = (y + (x // 3) % 2) % 4
        c = "st2" if band == 0 else ("st1" if band < 3 else "wd2")
        if x < 6 or x > 25:
            c = "st1" if band else "wd2"
        L.px(x, y, c)
    for y, x in np.argwhere(K.ring(dome)):
        L.px(x, y, "wd1" if y < 20 else "ink")
    for x in range(9, 23):
        L.px(x, 18, "ink")
        L.px(x, 19, "ink" if 11 < x < 21 else "wd1")
    for x in range(4, 28):
        L.px(x, 29, "gd" if x % 2 else "g1")
        L.px(x, 30, "gd")
    # a bundle-tie and a tuft on top
    for x in range(12, 20):
        L.px(x, 10, "k1")
    K.put(L, 13, 5, ["s.S.s", ".sSs.", "..w.."], G)
    return s


def nets(phase=0):
    """Decoy nets on poles, strung across the edge of the reeds."""
    s = K.struct("nets", "Fowlers' nets on poles", 2, 1, SEC, walk=["XX"],
                 names={"W": (0, 0), "E": (1, 0)},
                 notes="A fowlers' net strung between two poles over the reeds. Blocks.")
    reed_bottom(s.B, 0, 0, phase)
    reed_bottom(s.B, 16, 0, phase)
    L = s.M
    for x in (3, 28):
        for y in range(1, 15):
            L.px(x, y, "wd2" if y < 4 else "wd1")
            L.px(x + 1, y, "ink")
    for y in range(3, 13):
        for x in range(5, 28):
            if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                L.px(x, y, "k1")
    for x in range(4, 28):
        L.px(x, 2, "ink" if x % 2 else "k1")
    # a caught bird's feather and a decoy duck on the cord
    K.put(L, 13, 4, [".WW.", "WwWK", ".ww."], G)
    s.anim = "reeds"
    return s


def traps(phase=0):
    """Wicker eel traps standing in the water, and one pulled up on its stake."""
    s = K.struct("traps", "Eel traps in the water", 2, 1, SEC, walk=["XX"],
                 names={"trap": (0, 0), "trap_b": (1, 0)},
                 notes="Wicker eel traps standing in the marsh water. Block.")
    water_bottom(s.B, 0, 0, phase)
    water_bottom(s.B, 16, 0, phase)
    L = s.M
    for ox, (cx, cy) in ((0, (8, 9)), (16, (7, 8))):
        for y in range(3, 14):
            half = 1 + (y - 3) * 5 // 10
            for x in range(cx - half, cx + half + 1):
                c = "st1" if (x + y) % 2 else "wd2"
                if y % 3 == 0:
                    c = "wd1"
                L.px(ox + x, y, c)
            L.px(ox + cx - half - 1, y, "ink")
            L.px(ox + cx + half + 1, y, "ink")
        L.px(ox + cx, 1, "wd1")
        L.px(ox + cx, 2, "wd1")
    s.anim = "marsh"
    return s


def rack(phase=0):
    """The eel-smoker's rack: a timber frame hung with split eels over a low
    fire; the smoke curls up and the flames flicker by phase."""
    s = K.struct("rack", "The eel-smoker's rack and fire", 2, 2, SEC, walk=["XX", "XX"],
                 names={"NW": (0, 0), "NE": (1, 0), "SW": (0, 1), "SE": (1, 1)},
                 notes="A timber smoking rack hung with eels over a smouldering reed fire. "
                       "The flames and smoke move with the marsh's phases. Blocks.")
    K.ground(s, "grass")
    L = s.M
    # posts and the cross-bar
    for x in (3, 27):
        for y in range(4, 28):
            L.px(x, y, "wd2" if x == 3 else "wd1")
            L.px(x + 1, y, "ink")
    for x in range(2, 30):
        L.px(x, 5, "wd2")
        L.px(x, 6, "wd1")
    # eels hanging from the bar
    for i, x in enumerate(range(7, 26, 3)):
        n = 9 + (i * 5) % 5
        for y in range(7, 7 + n):
            L.px(x, y, "el" if y < 7 + n - 1 else "wd1")
            if y % 3 == 0:
                L.px(x + 1, y, "k1")
    # the fire on a ring of stones, under the rack
    for x in range(8, 24):
        L.px(x, 27, "k1" if x % 3 else "ink")
    flick = phase % 2
    for (x, y, c) in ((12, 25, "fi1"), (13, 24, "fi2"), (14, 23 - flick, "fi1"), (15, 25, "fi2"),
                      (16, 24 + flick, "fi1"), (17, 23, "fi2"), (18, 25, "fi1"), (19, 24, "fi1"),
                      (14, 25, "fi2"), (16, 26, "fi2"), (17, 25, "fi1"), (13, 26, "fi1"),
                      (15, 26, "fi1"), (18, 26, "fi2")):
        L.px(x, y, c)
    # smoke, drifting up through the eels
    for k in range(6):
        sx = 15 + ((k + phase) % 3) - 1
        L.px(sx, 21 - 3 * k, "sm2" if k % 2 else "sm1")
        L.px(sx + 1, 20 - 3 * k, "sm1")
    for x in range(4, 29):
        L.px(x, 28, "gd" if x % 2 else "g1")
    s.anim = "rack"
    return s


def boat(phase=0):
    """A reed boat pulled up on the mud: two long bundles lashed together."""
    s = K.struct("boat", "A reed boat pulled up", 2, 1, SEC, walk=["XX"],
                 names={"W": (0, 0), "E": (1, 0)},
                 notes="A little boat of bundled reeds pulled up on the shore mud. The "
                       "reed-boat boy sits in it. Blocks.")
    mud_bottom(s.B, 0, 0)
    mud_bottom(s.B, 16, 0)
    L = s.M
    yy, xx = np.mgrid[0:16, 0:32]
    hull = (((xx - 15.5) / 15.0) ** 2 + ((yy - 9.0) / 5.0) ** 2) <= 1.0
    for y, x in np.argwhere(hull):
        c = "st2" if y < 7 else ("st1" if y < 11 else "wd2")
        if (x % 6) == 0:
            c = "k1"
        L.px(x, y, c)
    for y, x in np.argwhere(K.ring(hull)):
        L.px(x, y, "ink" if y > 8 else "wd1")
    for x in range(1, 4):
        L.px(x, 6 - x, "st1")                   # the prow's curl
        L.px(31 - x, 6 - x, "st1")
    for x in range(5, 27):
        L.px(x, 15, "ink" if x % 2 else "wd1")  # its shadow on the mud
    return s


def nest(phase=0):
    """A heron's nest of sticks in the reeds, two pale eggs."""
    s = K.struct("nest", "A heron's nest in the reeds", 1, 1, SEC, walk=["X"],
                 names={"nest": (0, 0)}, notes="A heron's nest of sticks in the reeds. Blocks.")
    reed_bottom(s.B, 0, 0, phase)
    L = s.M
    yy, xx = np.mgrid[0:16, 0:16]
    m = (((xx - 7.5) / 7.0) ** 2 + ((yy - 9.5) / 4.0) ** 2) <= 1.0
    for y, x in np.argwhere(m):
        L.px(x, y, "wd1" if (x + 2 * y) % 3 else "wd2")
    for y, x in np.argwhere(K.ring(m)):
        L.px(x, y, "ink" if y > 9 else "wd2")
    K.put(L, 5, 7, [".SS.SS", "SSsSSs"], G)
    s.anim = "reeds"
    return s


def jetty(phase=0):
    """The fishing jetty off the dike, and the fishing step: planks on posts."""
    s = K.struct("jetty", "The fishing jetty and step", 3, 1, SEC, walk=["..."],
                 names={"end": (0, 0), "mid": (1, 0), "step": (2, 0)},
                 notes="Planks over the water on posts: `end` the jetty's far end, `mid` its "
                       "run (stack north from the dike), `step` the little fishing step where "
                       "Ismenias stands. Walkable.")
    for cx in range(3):
        water_bottom(s.B, cx * 16, 0, phase)
    L = s.M
    for cx in (0, 1):
        ox = cx * 16
        y0 = 3 if cx == 0 else 0
        for y in range(y0, 16):
            for x in range(3, 13):
                c = "wd2" if (y % 4) else "wd1"
                if x in (3, 12):
                    c = "ink"
                L.px(ox + x, y, c)
        for y in range(y0, 16, 4):
            L.px(ox + 5, y + 1, "k1")
            L.px(ox + 10, y + 1, "k1")
        if cx == 0:
            for x in range(3, 13):
                L.px(ox + x, 3, "ink")
            for (px, py) in ((2, 4), (13, 4)):
                for y in range(py, py + 4):
                    L.px(ox + px, y, "wd1")
    ox = 32
    for y in range(2, 14):
        for x in range(1, 15):
            c = "wd2" if (x % 5) else "wd1"
            if y in (2, 13) or x in (1, 14):
                c = "ink"
            L.px(ox + x, y, c)
    s.anim = "marsh"
    return s


def water_bits(phase=0):
    """Lily pads with a white flower, and the sluice's outflow foaming into the
    lagoon under the dike's culvert (marsh colors, so they sit in the water)."""
    s = K.struct("water_bits", "Lily pads and the sluice's outflow", 3, 1, SEC, walk=["XXX"],
                 names={"lilies": (0, 0), "lilies_b": (1, 0), "outflow": (2, 0)},
                 notes="Marsh water with lily pads (`lilies`, `lilies_b`, scatter them), and "
                       "`outflow`, the sluice's water foaming out under the dike's culvert "
                       "arch. MB_POND_WATER.")
    for cx in range(3):
        water_bottom(s.B, cx * 16, 0, phase)
        s.behaviors[(cx, 0)] = "MB_POND_WATER"
    B = s.B
    for ox, pads in ((0, ((4, 4, 3), (11, 9, 3), (5, 12, 2))), (16, ((10, 4, 3), (4, 10, 3)))):
        for (cx, cy, r) in pads:
            m = K.K.ellipse_mask(16, 16, cx, cy, r + 0.6, r)
            for y, x in np.argwhere(m):
                B.px(ox + x, y, "lp2" if (x - cx) + (y - cy) < 0 else "lp1")
            B.px(ox + cx, cy, "mw1")                # the notch
            B.px(ox + cx + 1, cy - 1, "mw1")
        if ox == 0:
            K.put(B, 10, 7, [".w.", "w4w", ".w."], {"w": "w0", "4": "md3"})
    for y in range(16):
        for x in range(16):
            d = abs(x - 7.5)
            if y < 9 and d < 5 - y * 0.2:
                B.px(32 + x, y, "w0" if (x + y + phase) % 3 == 0 else "mw3")
            elif y < 13 and d < 7 and (x * 3 + y + phase * 2) % 4 == 0:
                B.px(32 + x, y, "mw3")
    s.anim = "marsh"
    return s


def build(phase=0):
    return [hide(phase), nets(phase), traps(phase), rack(phase), boat(phase), nest(phase),
            jetty(phase), water_bits(phase)]
