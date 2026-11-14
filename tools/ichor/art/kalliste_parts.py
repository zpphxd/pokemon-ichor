"""Reusable motifs for the kalliste structures: Cycladic doors and shutters,
Doric columns, flagstones and dry-stone, steps, pots.

Motifs are ASCII grids with a legend, or small procedural painters that put
pixels down the way a Gen 3 artist would (top-left light, 1 px outlines on
objects, none on terrain). Everything paints by color name; see kalliste_lib.
"""
from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------
# Cycladic house motifs (group "cyc")
# --------------------------------------------------------------------------

# Aegean-blue plank door, 12 x 20, set in a whitewash reveal. k ink, L/M/D the
# blue ramp, H the sheen on the lit edge, w the brass-free white knob.
DOOR = [
    "kkkkkkkkkkkk",
    "kHLLLLkHLLLk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLDDDDkLDDDk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLMMwDkLwMMk",
    "kLMMMDkLMMMk",
    "kLDDDDkLDDDk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLMMMDkLMMMk",
    "kLDDDDkLDDDk",
    "kDDDDDkDDDDk",
    "kkkkkkkkkkkk",
]
DOOR_KEY = {"k": "ink", "H": "b3", "L": "b2", "M": "b1", "D": "b0", "w": "w0"}

# A window with its shutters folded back against the wall, 16 x 11.
WINDOW = [
    " kkkk kkkkkk kkkk",
    " kLMk kddddk kLMk",
    " kDDk kdLMdk kDDk",
    " kLMk kdLMdk kLMk",
    " kDDk kkkkkk kDDk",
    " kLMk kdLMdk kLMk",
    " kDDk kdLMdk kDDk",
    " kLMk kddddk kLMk",
    " kkkk kkkkkk kkkk",
    "     cwwwwwwc     ",
    "      333333      ",
]
WINDOW_KEY = {"k": "ink", "L": "b2", "M": "b1", "D": "b0", "d": "dk", "w": "w0",
              "c": "w2", "3": "w3"}

# A small blue-framed window with no shutters (upper floors, the shrine drum).
SMALL_WINDOW = [
    "kkkkkk",
    "kLLLLk",
    "kLddMk",
    "kLddMk",
    "kMMMMk",
    "kkkkkk",
]

# Terracotta pot with a basil or geranium mound, 10 x 11.
POT = [
    "   gG g   ",
    "  gGGgGg  ",
    " gGrGgGrg ",
    " gGGgGGgg ",
    "  gggggg  ",
    " kkkkkkkk ",
    " kTTTTttk ",
    "  kTTttk  ",
    "  kTttTk  ",
    "  kkkkkk  ",
    "  333333  ",
]
POT_KEY = {"g": "ol1", "G": "ol2", "r": "tc1", "k": "ink", "T": "tc2", "t": "tc1",
           "3": "w3"}

# Cycladic chimney: a little whitewashed tower with a pierced cap, 8 x 12.
CHIMNEY = [
    " oooooo ",
    "o011110o",
    "o0kk0k1o",
    "o011110o",
    " o0112o ",
    " o0112o ",
    " o0112o ",
    " o0112o ",
    " o0112o ",
    " oooooo ",
    "  2222 2",
    "   2222 ",
]
CHIMNEY_KEY = {"o": "dk", "0": "w0", "1": "w1", "2": "w2", "k": "dk"}


def flat_roof(L, x, y, w, h, outline="dk"):
    """A whitewashed flat roof seen from above, with a parapet on all sides.
    (x, y, w, h) is the roof's whole box; the front rim is its last 2 rows."""
    L.rect(x, y, w, h, "w1")
    L.hline(x, x + w - 1, y, outline)
    L.vline(x, y, y + h - 1, outline)
    L.vline(x + w - 1, y, y + h - 1, outline)
    # back and side parapet tops, lit from the top left
    L.hline(x + 1, x + w - 2, y + 1, "w0")
    L.vline(x + 1, y + 1, y + h - 3, "w0")
    L.vline(x + w - 2, y + 1, y + h - 3, "w2")
    # the parapets' shade on the roof floor
    L.hline(x + 2, x + w - 3, y + 2, "w2")
    L.vline(x + 2, y + 2, y + h - 4, "w2")
    # front parapet: inner face in shade, then its sunlit top rim
    L.hline(x + 2, x + w - 3, y + h - 3, "w2")
    L.hline(x + 1, x + w - 2, y + h - 2, "w0")
    L.hline(x + 1, x + w - 2, y + h - 1, "w0")
    L.px(x + w - 2, y + h - 2, "w2")
    L.px(x + w - 2, y + h - 1, "w2")


def facade(L, x, y, w, h, outline="dk", base=True):
    """A whitewashed south wall: lit left corner, shaded right corner, eave
    shadow along the top and a painted grey base course."""
    L.rect(x, y, w, h, "w1")
    L.vline(x, y, y + h - 1, outline)
    L.vline(x + w - 1, y, y + h - 1, outline)
    L.vline(x + 1, y, y + h - 1, "w0")
    L.vline(x + w - 2, y, y + h - 1, "w2")
    L.hline(x + 1, x + w - 2, y, "w2")
    if base:
        L.hline(x + 1, x + w - 2, y + h - 3, "w2")
        L.hline(x + 1, x + w - 2, y + h - 2, "w3")
        L.hline(x, x + w - 1, y + h - 1, "w4")


def door(L, x, y, step=True):
    """The blue door (12 x 20) at (x, y), a 1 px reveal around it and a
    whitewashed threshold step under it (14 x 2)."""
    L.rect(x - 1, y - 1, 14, 1, "w3")
    L.vline(x - 1, y, y + 19, "w2")
    L.blit(DOOR, DOOR_KEY, x, y)
    if step:
        L.hline(x - 1, x + 12, y + 20, "w0")
        L.hline(x - 1, x + 12, y + 21, "w3")


def window(L, x, y):
    L.blit(WINDOW, WINDOW_KEY, x - 1, y)


# --------------------------------------------------------------------------
# Columns, steps
# --------------------------------------------------------------------------

def doric_column(L, x, y, w, h, ramp, outline, capital=True, neck=True, fluted=True,
                 base_line=True):
    """A Doric column, shaft x..x+w-1 from y to y+h-1, capital included at the top.

    ramp: 5 color names dark -> highlight. Light comes from the left: the lit
    flank sits a pixel in from the left edge, the shade runs down the right.
    """
    d2, d1, m, l1, hi = ramp
    top = y
    if capital:
        # abacus: a square slab 2 px wider than the shaft each side
        L.rect(x - 2, top, w + 4, 3, l1)
        L.hline(x - 2, x + w + 1, top, outline)
        L.hline(x - 2, x + w + 1, top + 2, d1)
        L.vline(x - 2, top, top + 2, outline)
        L.vline(x + w + 1, top, top + 2, outline)
        L.hline(x - 1, x + w, top + 1, hi)
        # echinus: the cushion, flaring 1 px
        L.rect(x - 1, top + 3, w + 2, 2, m)
        L.hline(x - 1, x + w, top + 3, l1)
        L.vline(x - 1, top + 3, top + 4, outline)
        L.vline(x + w, top + 3, top + 4, outline)
        L.px(x + w - 1, top + 4, d1)
        top += 5
        if neck:
            L.hline(x, x + w - 1, top, d1)
            top += 1
    bot = y + h - 1
    for yy in range(top, bot + 1):
        for xx in range(x, x + w):
            i = xx - x
            if i == 0 or i == w - 1:
                c = outline
            elif i == 1:
                c = l1
            elif i == 2:
                c = hi
            elif i >= w - 3:
                c = d1 if i == w - 3 else d2
            else:
                c = m
            L.px(xx, yy, c)
        if fluted and w >= 8:
            # flutes: shallow grooves every 2 px across the middle
            for i in range(4, w - 4, 2):
                L.px(x + i, yy, l1 if i < w // 2 else d1)
    if base_line:
        L.hline(x, x + w - 1, bot, d2)


def steps(L, x, y, w, n, tread, riser, outline=None, rise=2, tread_h=1):
    """n horizontal steps from y downward, each a lit tread then a shaded riser."""
    yy = y
    for i in range(n):
        L.rect(x, yy, w, tread_h, tread)
        L.rect(x, yy + tread_h, w, rise, riser)
        yy += tread_h + rise
    if outline:
        L.hline(x, x + w - 1, yy - 1, outline)
    return yy


# --------------------------------------------------------------------------
# Stone textures
# --------------------------------------------------------------------------

def voronoi_labels(w, h, seeds, wrap=True, stretch=(1.0, 1.0)):
    """Nearest-seed label per pixel, optionally on a torus so the texture tiles."""
    ys, xs = np.mgrid[0:h, 0:w]
    best = np.full((h, w), 1e9)
    lab = np.zeros((h, w), int)
    sx, sy = stretch
    for k, (px, py) in enumerate(seeds):
        offs = [(-w, 0), (0, 0), (w, 0)] if wrap else [(0, 0)]
        offs_y = [-h, 0, h] if wrap else [0]
        for ox, _ in offs:
            for oy in offs_y:
                d = ((xs - (px + ox)) * sx) ** 2 + ((ys - (py + oy)) * sy) ** 2
                m = d < best
                best[m] = d[m]
                lab[m] = k
    return lab


def joints(lab, wrap=True):
    """1 px joint where a pixel's right or lower neighbour is another stone."""
    if wrap:
        r = np.roll(lab, -1, axis=1)
        d = np.roll(lab, -1, axis=0)
    else:
        r = np.concatenate([lab[:, 1:], lab[:, -1:]], axis=1)
        d = np.concatenate([lab[1:, :], lab[-1:, :]], axis=0)
    return (lab != r) | (lab != d)


def shade_stones(lab, joint, bases, hi, lo, wrap=True):
    """Color names per pixel: joints None; stones lit on their top-left edges,
    shaded on their bottom-right edges. bases[k] is stone k's body color;
    hi/lo map a body color to its highlight and shade."""
    h, w = lab.shape
    out = np.empty((h, w), object)
    for y in range(h):
        for x in range(w):
            if joint[y, x]:
                out[y, x] = None
                continue
            b = bases[lab[y, x] % len(bases)]

            def J(xx, yy):
                if wrap:
                    return joint[yy % h, xx % w]
                if 0 <= xx < w and 0 <= yy < h:
                    return joint[yy, xx]
                return False
            if J(x, y - 1) or J(x - 1, y):
                out[y, x] = hi.get(b, b)
            elif J(x, y + 1) or J(x + 1, y):
                out[y, x] = lo.get(b, b)
            else:
                out[y, x] = b
    return out


def paint_grid(L, grid, x, y, joint_color=None):
    h, w = grid.shape
    for j in range(h):
        for i in range(w):
            c = grid[j, i]
            if c is None:
                if joint_color:
                    L.px(x + i, y + j, joint_color)
            else:
                L.px(x + i, y + j, c)


# Cycladic flagstones: slate set in thick whitewashed lime, one 16 px torus so any
# arrangement of paving metatiles joins up.
FLAG_SEEDS = [(4, 4), (12, 3), (8, 11), (1, 12)]
_FLAG_LAB = voronoi_labels(16, 16, FLAG_SEEDS, stretch=(1.0, 1.2))
FLAG_JOINT = joints(_FLAG_LAB)


def flagstones(variant=0):
    bases = [["sl3", "sl2", "sl2", "sl3"],
             ["sl2", "sl3", "sl3", "sl2"]][variant]
    hi = {"sl2": "sl3", "sl3": "pj1"}
    lo = {"sl2": "sl1", "sl3": "sl2"}
    return shade_stones(_FLAG_LAB, FLAG_JOINT, bases, hi, lo)


def paint_flagstones(L, x, y, w, h, variant=0):
    """Fill a box with flagstones, phase-locked to 16 px cells."""
    g = flagstones(variant)
    for j in range(h):
        for i in range(w):
            c = g[(y + j) % 16, (x + i) % 16]
            L.px(x + i, y + j, c if c else "w0")
