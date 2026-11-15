"""Kemet's ground: black mud and its edges against grass and water, papyrus (the
encounter reeds and the solid thickets taller than a man), papyrus and lotus in
the water, dune grass on Pharos's sand, and the limestone quays of Naukratis.

Edge pieces follow the map builders' edge_key() names: a piece called "tl" is a
cell of the region whose north and west neighbours lie outside it; "in_nw" is a
cell whose only outside neighbour is the north-west diagonal.
"""
from __future__ import annotations

import math

import numpy as np

import kemet_lib as L
from kemet_lib import Struct, finish

EDGE_KEYS = ["tl", "t", "tr", "l", "r", "bl", "b", "br", "in_nw", "in_ne", "in_sw", "in_se"]
FLAGS = {  # key: (n, s, w, e, nw, ne, sw, se) outside
    "tl": (1, 0, 1, 0, 0, 0, 0, 0), "t": (1, 0, 0, 0, 0, 0, 0, 0), "tr": (1, 0, 0, 1, 0, 0, 0, 0),
    "l": (0, 0, 1, 0, 0, 0, 0, 0), "r": (0, 0, 0, 1, 0, 0, 0, 0),
    "bl": (0, 1, 1, 0, 0, 0, 0, 0), "b": (0, 1, 0, 0, 0, 0, 0, 0), "br": (0, 1, 0, 1, 0, 0, 0, 0),
    "in_nw": (0, 0, 0, 0, 1, 0, 0, 0), "in_ne": (0, 0, 0, 0, 0, 1, 0, 0),
    "in_sw": (0, 0, 0, 0, 0, 0, 1, 0), "in_se": (0, 0, 0, 0, 0, 0, 0, 1),
}
# Each edge's depth into the cell, per pixel along it: period 16, so a run of edge
# cells reads as one ragged line.
WOB_N = [3, 4, 4, 5, 4, 3, 3, 4] * 2
WOB_S = [4, 3, 3, 4, 5, 5, 4, 3] * 2
WOB_W = [3, 3, 4, 5, 5, 4, 3, 4] * 2
WOB_E = [4, 4, 3, 3, 4, 5, 4, 3] * 2


def edge_mask(key, wobble=True, depth=None):
    """True where a 16x16 cell is inside the region, for edge piece `key`."""
    n, s, w, e, nw, ne, sw, se = FLAGS[key]
    m = np.ones((16, 16), bool)
    d = (lambda t, i: t[i]) if wobble else (lambda t, i: depth)
    for y in range(16):
        for x in range(16):
            if n and y < d(WOB_N, x):
                m[y, x] = False
            if s and 15 - y < d(WOB_S, x):
                m[y, x] = False
            if w and x < d(WOB_W, y):
                m[y, x] = False
            if e and 15 - x < d(WOB_E, y):
                m[y, x] = False
    R = 9

    def convex(cx, cy):
        # cx, cy: the corner's own coordinates (0 or 16)
        ax, ay = (R if cx == 0 else 16 - R), (R if cy == 0 else 16 - R)
        for y in range(16):
            for x in range(16):
                inx = x < R if cx == 0 else x >= 16 - R
                iny = y < R if cy == 0 else y >= 16 - R
                if inx and iny and (x + 0.5 - ax) ** 2 + (y + 0.5 - ay) ** 2 > R * R:
                    m[y, x] = False

    def notch(cx, cy, r):
        for y in range(16):
            for x in range(16):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 < r * r:
                    m[y, x] = False
    if n and w:
        convex(0, 0)
    if n and e:
        convex(16, 0)
    if s and w:
        convex(0, 16)
    if s and e:
        convex(16, 16)
    r = 5.5 if wobble else depth + 1.5
    if nw:
        notch(0, 0, r)
    if ne:
        notch(16, 0, r)
    if sw:
        notch(0, 16, r)
    if se:
        notch(16, 16, r)
    return m


def rim(mask):
    """Inside pixels that touch an outside pixel (4-neighbour), and the next ring."""
    pad = np.pad(mask, 1, constant_values=True)
    out = ~pad
    near = out[:-2, 1:-1] | out[2:, 1:-1] | out[1:-1, :-2] | out[1:-1, 2:]
    r1 = mask & near
    pad2 = np.pad(r1, 1)
    near2 = pad2[:-2, 1:-1] | pad2[2:, 1:-1] | pad2[1:-1, :-2] | pad2[1:-1, 2:]
    r2 = mask & ~r1 & near2
    return r1, r2


def outer_ring(mask):
    """Outside pixels that touch an inside pixel."""
    pad = np.pad(mask, 1)
    near = pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:]
    return ~mask & near


def paint_mud(Ly, ox, oy, mask):
    for y in range(16):
        for x in range(16):
            if mask[y, x]:
                Ly.px(ox + x, oy + y, L.MUD_KEY[L.MUD[y][x]])


# --------------------------------------------------------------------------

def mud_plain():
    s = Struct("mud", "Black mud", 4, 1, walk=["...."], ground="mud",
               notes="The delta's wet black ground, walkable. c is plain; c2 has a puddle "
                     "that holds the sky; c4 dries pale and cracks.")
    B = s.B
    # c2: a puddle
    for y in range(5, 11):
        for x in range(16 + 3, 16 + 13):
            dx, dy = (x - 16 - 8) / 5.0, (y - 8) / 2.6
            if dx * dx + dy * dy <= 1:
                B.px(x, y, "wet")
    for x in range(16 + 5, 16 + 10):
        B.px(x, 6, "wet2")
    B.px(16 + 10, 7, "wet2")
    for x in range(16 + 4, 16 + 12):
        B.px(x, 10, "md0")
    # c4: drying, cracked
    for y in range(16):
        for x in range(48, 64):
            B.px(x, y, "md3" if L._h(x, y, 4) < 200 else "md4")
    for (x0, y0, x1, y1) in ((49, 2, 55, 6), (55, 6, 54, 12), (55, 6, 62, 4), (54, 12, 59, 15),
                             (54, 12, 49, 13), (62, 4, 63, 10), (59, 15, 62, 10)):
        B.line(x0, y0, x1, y1, "md1")
    s.name(c=(0, 0), c2=(1, 0), c4=(3, 0))
    return finish(s)


def mud_edges(ground, key, title, water=False):
    """Mud on aethos ground (grass, or the sea for a bank), one piece per edge_key."""
    s = Struct(key, title, 6, 2, walk=["......", "......"], ground=ground,
               notes=("A mud bank against the water: mud is walkable, the water beyond "
                      "it is decoration. " if water else "Mud fading into the meadow. ")
               + "Place by edge_key against the " + ("sea" if water else "grass") + "; "
               "plain mud (`mud`, part c) fills the middle.")
    order = EDGE_KEYS
    for i, k in enumerate(order):
        cx, cy = i % 6, i // 6
        ox, oy = cx * 16, cy * 16
        m = edge_mask(k)
        paint_mud(s.M, ox, oy, m)
        r1, r2 = rim(m)
        for y in range(16):
            for x in range(16):
                if r1[y, x]:
                    s.M.px(ox + x, oy + y, "wet" if water else "md3")
                elif r2[y, x] and (x + y) % 4 == 0:
                    s.M.px(ox + x, oy + y, "md0" if water else "md2")
        ring = outer_ring(m)
        for y in range(16):
            for x in range(16):
                if not ring[y, x]:
                    continue
                if water:
                    if L._h(x % 8, y % 8, 7) < 120:
                        s.M.px(ox + x, oy + y, "wet2" if L._h(x, y, 2) < 160 else "w0")
                else:
                    # grass blades lean over the mud's rim
                    if L._h(x % 8, y % 8, 9) < 70:
                        s.M.px(ox + x, oy + y, "gr1")
        s.names[k] = (cx, cy)
    return finish(s)


# --------------------------------------------------------------------------
# Papyrus
# --------------------------------------------------------------------------

def umbel(Ly, x, y, big=False, lit=True):
    """A papyrus umbel: a spray of fine rays from the stem's tip, gold at the core."""
    if big:
        rows = [" a.a.a ",
                "a.bab.a",
                ".bbcbb.",
                "  .d.  "]
    else:
        rows = ["a.a.a",
                ".bcb.",
                " .d. "]
    w = len(rows[0])
    leg = {"a": "pg4" if lit else "pg3", "b": "pg3" if lit else "pg2", "c": "um1" if lit else "um0",
           ".": "pg2" if lit else "pg1", "d": "pg2"}
    Ly.blit(rows, leg, x - w // 2, y)


def stem(Ly, x, y0, y1, lean=0, c="pg1", lit=None):
    """A stem from (x, y1) at its foot up to y0, leaning `lean` px over its height."""
    h = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        xx = x + round(lean * (y1 - y) / h)
        Ly.px(xx, y, c)
        if lit and y % 2 == 0:
            Ly.px(xx - 1, y, lit)


def reeds():
    """Walkable papyrus: the encounter reeds, young papyrus a hand over a man's waist."""
    s = Struct("reeds", "Papyrus reeds (wild encounters)", 4, 1, walk=["...."],
               notes="Tall grass for the delta: MB_TALL_GRASS. a and b grow in mud, g in the "
                     "meadow, s in Pharos's sand. Lay a and b in a checker so a field doesn't "
                     "stripe.")
    s.ground_rows(["mmgs"])
    M = s.M
    for cx, seed in ((0, 1), (1, 2), (2, 3), (3, 4)):
        ox = cx * 16
        # sedge at the foot
        for x in range(1, 15):
            if L._h(x, seed, 3) < 150:
                M.px(ox + x, 15, "pg0")
                M.px(ox + x, 14, "pg1" if x % 2 else "pg0")
        clumps = [(3, 4, -1), (8, 2, 0), (12, 5, 1), (5, 7, 1), (10, 8, -1)]
        if seed % 2 == 0:
            clumps = [(4, 3, 0), (9, 5, 1), (13, 2, -1), (2, 8, -1), (7, 9, 0)]
        for (x, top, lean) in clumps:
            stem(M, ox + x, top + 2, 15, lean, "pg1", lit="pg2")
        for (x, top, lean) in clumps:
            umbel(M, ox + x + lean, top, lit=top < 6)
        M.px(ox + 1, 13, "pg2")
        M.px(ox + 14, 12, "pg2")
    for cx in range(4):
        s.behaviors[(cx, 0)] = "MB_TALL_GRASS"
    s.name(a=(0, 0), b=(1, 0), g=(2, 0), s=(3, 0))
    return finish(s)


THICKET_PARTS = {  # name: (n, s, w, e) on the thicket's outside
    "nw": (1, 0, 1, 0), "n": (1, 0, 0, 0), "ne": (1, 0, 0, 1),
    "w": (0, 0, 1, 0), "c": (0, 0, 0, 0), "e": (0, 0, 0, 1),
    "sw": (0, 1, 1, 0), "s": (0, 1, 0, 0), "se": (0, 1, 0, 1),
    "c2": (0, 0, 0, 0),
}


def _wrap8(Ly):
    """Fold a 16-wide strip drawn with spill (columns 4..11 are the 8-px tile, 0..3
    and 12..15 its neighbours) into one 8-px tile that repeats seamlessly."""
    out = L.Layer(8, Ly.h)
    for x in range(16):
        for y in range(Ly.h):
            if Ly.a[y, x, 3]:
                out.a[y, (x - 4) % 8] = Ly.a[y, x]
    return out


def thicket_strip(variant, n=False, s_=False):
    """An 8-px-wide, 16-px-tall strip of solid papyrus that tiles side by side."""
    Ly = L.Layer(16, 16)
    far, near = ((5, 9), 7) if variant == 0 else ((6, 10), 4)
    Ly.rect(4, 0, 8, 16, "pg0")
    for x in far:
        stem(Ly, x, 3, 15, 0, "pg1")
        umbel(Ly, x, 1, lit=False)
    stem(Ly, near, 9, 15, 0, "pg2", lit="pg3")
    umbel(Ly, near, 7, lit=True)
    if n:
        umbel(Ly, near + 1, 0, big=True, lit=True)
    st = _wrap8(Ly)
    if s_:
        for x in range(8):
            st.px(x, 15, "md0")
            st.px(x, 14, "md1" if x in (1, 5) else "pg0")
            if x % 3 == 1:
                st.px(x, 13, "pg1")
    return st


def thicket_cell(dest, dox, doy, n, s_, w, e, variant=0):
    """A cell of solid papyrus: two strips side by side, with the region's edges."""
    st = thicket_strip(variant, n, s_)
    cell = L.Layer(16, 16)
    cell.a[:, 0:8] = st.a
    cell.a[:, 8:16] = st.a
    if w:
        for y in range(16):
            cell.px(0, y, "ink" if y % 4 != 1 else "pg0")
            cell.px(1, y, "pg0")
            if y % 4 == 0:
                cell.px(2, y, "pg2")
    if e:
        for y in range(16):
            cell.px(15, y, "ink" if y % 4 != 3 else "pg0")
            cell.px(14, y, "pg0")
    dest.a[doy:doy + 16, dox:dox + 16] = cell.a


def fringe(Ly, ox, oy, variant=0):
    """The thicket's top rank, poking up into the cell north of it (top layer).
    8-px periodic, like the strips under it."""
    s = L.Layer(16, 16)
    x, y = (8, 9) if variant == 0 else (7, 10)
    stem(s, x, y + 3, 15, 0, "pg2")
    umbel(s, x, y, big=True, lit=True)
    s.px(x, y - 1, "pg4")
    st = _wrap8(s)
    for i in (0, 8):
        for yy in range(16):
            for xx in range(8):
                if st.a[yy, xx, 3]:
                    Ly.a[oy + yy, ox + i + xx] = st.a[yy, xx]


def thicket():
    s = Struct("thicket", "Papyrus thicket (solid)", 5, 3,
               walk=["XXX.T", "XXXXT", "XXX.T"],
               notes="Papyrus taller than a man: the delta's walls. Lay a region of it with "
                     "the 3x3 parts by which sides face out (nw n ne / w c e / sw s se; c2 "
                     "for variety). Above every north-edge cell put a fringe (fringe_mud or "
                     "fringe_grass by the ground there): the top rank's umbels, drawn over "
                     "the player. Every region is at least 2x2.")
    s.ground_rows(["nnnnm", "nnnnm", "nnnng"])
    for name, (cx, cy) in {"nw": (0, 0), "n": (1, 0), "ne": (2, 0), "w": (0, 1), "c": (1, 1),
                           "e": (2, 1), "sw": (0, 2), "s": (1, 2), "se": (2, 2),
                           "c2": (3, 1)}.items():
        n, s_, w, e = THICKET_PARTS[name]
        thicket_cell(s.B, cx * 16, cy * 16, n, s_, w, e, variant=1 if name == "c2" else (cx + cy) % 2)
        s.names[name] = (cx, cy)
    # the fringes: over mud (drawn: mud bottom, umbels on top) and over grass
    for (cx, cy, var) in ((4, 0, 0), (4, 1, 1), (4, 2, 0)):
        fringe(s.T, cx * 16, cy * 16, var)
    s.names.update(fringe_mud=(4, 0), fringe_mud2=(4, 1), fringe_grass=(4, 2))
    # outline the fringes' silhouettes in ink so the umbels read against the ground
    for cy in range(3):
        ox, oy = 64, cy * 16
        a = s.T.a[oy:oy + 16, ox:ox + 16, 3] > 0
        pad = np.pad(a, 1)
        ring = ~a & (pad[:-2, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
        for y in range(16):
            for x in range(16):
                if ring[y, x]:
                    s.T.px(ox + x, oy + y, "ink")
    return finish(s)


def papyrus_water():
    s = Struct("papyrus_water", "Papyrus standing in water", 2, 1, walk=["XX"], ground="sea",
               notes="A clump of papyrus out in the channel: solid, the water round it animated.")
    M = s.M
    for cx, var in ((0, 0), (1, 1)):
        ox = cx * 16
        # ripples round the foot
        for x in range(2, 14):
            M.px(ox + x, 14, "md0" if 4 <= x <= 11 else "wet")
        for x in range(4, 12):
            M.px(ox + x, 15, "wet")
        M.px(ox + 1, 15, "wet2")
        M.px(ox + 14, 15, "wet2")
        clumps = [(4, 2, -1), (8, 0, 0), (11, 3, 1), (6, 5, 0)] if var == 0 else \
                 [(3, 3, -1), (7, 1, 0), (12, 2, 1), (9, 5, 0)]
        for (x, top, lean) in clumps:
            stem(M, ox + x, top + 2, 13, lean, "pg1", lit="pg2")
        for (x, top, lean) in clumps:
            umbel(M, ox + x + lean, top, lit=True)
    s.name(a=(0, 0), b=(1, 0))
    return finish(s)


def lotus():
    s = Struct("lotus", "Lotus pads (surfable)", 2, 1, walk=[".."], ground="sea",
               notes="White lotus on the water, the Egyptians' flower of the morning. Surfable "
                     "(MB_OCEAN_WATER): it rolls water encounters like open water.")
    M = s.M
    pads = [[(3, 4, 3), (10, 9, 4), (5, 12, 2)], [(4, 9, 4), (11, 3, 3), (12, 12, 2)]]
    for cx in range(2):
        ox = cx * 16
        for (x, y, r) in pads[cx]:
            for yy in range(-r, r + 1):
                for xx in range(-r - 1, r + 2):
                    if (xx / (r + 1)) ** 2 + (yy / r) ** 2 <= 1:
                        M.px(ox + x + xx, y + yy, "pg2" if yy < 0 else "pg1")
            M.px(ox + x, y, "pg1")                # the notch
            M.px(ox + x + 1, y + 1, "pg1")
            M.px(ox + x - r, y - 1, "pg3")
        # a flower on the biggest pad
        fx, fy, _ = pads[cx][1]
        M.blit([" w ", "wgw", " w "], {"w": "w0", "g": "gr2"}, ox + fx - 1, fy - 2)
        s.behaviors[(cx, 0)] = "MB_OCEAN_WATER"
    s.name(a=(0, 0), b=(1, 0))
    return finish(s)


def dune_grass():
    s = Struct("dune_grass", "Dune grass on sand (wild encounters)", 2, 1, walk=[".."],
               ground="sand",
               notes="Pharos's encounter grass: marram tufts on aethos's sand. MB_TALL_GRASS.")
    M = s.M
    for cx, tufts in ((0, [(3, 6), (8, 3), (12, 7), (6, 10), (11, 12)]),
                      (1, [(2, 4), (7, 7), (12, 3), (4, 11), (10, 10)])):
        ox = cx * 16
        for (x, y) in tufts:
            for dx, lean in ((-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2)):
                h = 5 - abs(dx)
                for k in range(h):
                    xx = x + dx + round(lean * k / max(1, h))
                    M.px(ox + xx, y + 4 - k, "pg2" if dx <= 0 else "pg1")
            M.px(ox + x, y - 1, "um0")
            M.px(ox + x - 2, y + 1, "um1")
            for dx in range(-2, 3):
                M.px(ox + x + dx, y + 5, "tr2" if abs(dx) < 2 else None)
        s.behaviors[(cx, 0)] = "MB_TALL_GRASS"
    s.name(a=(0, 0), b=(1, 0))
    return finish(s)


# --------------------------------------------------------------------------
# Quays
# --------------------------------------------------------------------------

QUAY_KEYS = EDGE_KEYS


def quay_edges():
    """Limestone quays against the water: the center is drawn ground "quay"; every
    edge is the same ashlar on the sea with its coping and wall face."""
    s = Struct("quay", "Limestone quay", 8, 2, walk=["......X.", "........"],
               notes="Naukratis's harbor. c is solid ashlar ground; the edges stand on the "
                     "sea by edge_key; steps runs down into the water on a north edge (the "
                     "mooring, where Nausikles waits); bollard is a solid mooring stone; c is plain "
                     "quay.")
    for i, k in enumerate(QUAY_KEYS):
        cx, cy = i % 6, i // 6
        s.set_ground("sea", [(cx, cy)])
    s.set_ground("quay", [(6, 0), (7, 0), (7, 1)])
    s.set_ground("sea", [(6, 1)])
    s.names["c"] = (7, 0)
    M = s.M
    for i, k in enumerate(QUAY_KEYS):
        cx, cy = i % 6, i // 6
        ox, oy = cx * 16, cy * 16
        n, s_, w, e, nw, ne, sw, se = FLAGS[k]
        m = np.ones((16, 16), bool)
        top = 2 if n else 0
        bot = 9 if s_ else 16
        lft = 2 if w else 0
        rgt = 14 if e else 16
        m[:top, :] = False
        m[:, :lft] = False
        m[:, rgt:] = False
        m[bot + (6 if s_ else 0):, :] = False
        for (flag, cxp, cyp) in ((nw, 0, 0), (ne, 15, 0), (sw, 0, 15), (se, 15, 15)):
            if flag:
                for y in range(16):
                    for x in range(16):
                        if abs(x - cxp) < 3 and abs(y - cyp) < 3:
                            m[y, x] = False
        # paint ashlar where inside, then the coping and the wall face
        for y in range(16):
            for x in range(16):
                if m[y, x]:
                    tmp_c = None
                    bx, by = x % 8, y % 8
                    tmp_c = "ls1" if (by == 7 or bx == 7) else "ls4" if by == 0 else "ls3"
                    M.px(ox + x, oy + y, tmp_c)
        if n:
            M.hline(ox + lft, ox + rgt - 1, oy + top, "w0")
            M.hline(ox + lft, ox + rgt - 1, oy + top - 1, "ink")
        if w:
            M.vline(ox + lft, oy + top, oy + (bot + 5 if s_ else 15), "w0")
            M.vline(ox + lft - 1, oy + top, oy + (bot + 5 if s_ else 15), "ink")
        if e:
            M.vline(ox + rgt - 1, oy + top, oy + (bot + 5 if s_ else 15), "ls2")
            M.vline(ox + rgt, oy + top, oy + (bot + 5 if s_ else 15), "ink")
        if s_:
            # coping, then the wall face (two courses) down to the waterline
            M.hline(ox + lft, ox + rgt - 1, oy + bot, "w0")
            for y in range(bot + 1, bot + 6):
                for x in range(lft, rgt):
                    c = "ls2" if (y - bot) in (1, 2) else "ls1"
                    if (x + (0 if y - bot < 3 else 4)) % 8 == 7:
                        c = "ls0"
                    M.px(ox + x, oy + y, c)
            M.hline(ox + lft, ox + rgt - 1, oy + bot + 5, "ink")
            for x in range(lft, rgt):
                if x % 3 == 0:
                    M.px(ox + x, oy + bot + 6, "ls0")
        s.names[k] = (cx, cy)
    # the bollard on solid quay
    M2 = s.B
    M2.blit(["  kkkk  ",
             " kwlllk ",
             " k3332k ",
             " kk22kk ",
             "  k21k  ",
             "  k21k  ",
             " k3221k ",
             " kkkkkk "], {"k": "ink", "w": "w0", "l": "ls4", "3": "ls3", "2": "ls2", "1": "ls1"},
            6 * 16 + 4, 4)
    s.names["bollard"] = (6, 0)
    # steps down into the water on a north edge: the mooring, where a gangplank goes
    ox, oy = 6 * 16, 16
    for y in range(3, 16):
        for x in range(16):
            bx, by = x % 8, y % 8
            M.px(ox + x, oy + y, "ls1" if (by == 7 or bx == 7) else "ls4" if by == 0 else "ls3")
    for i, y in enumerate(range(3, 10)):
        for x in range(3, 13):
            M.px(ox + x, oy + y, "w0" if i % 2 == 0 else "ls2")
        M.px(ox + 2, oy + y, "ink")
        M.px(ox + 13, oy + y, "ink")
    M.hline(ox, ox + 15, oy + 2, "ink")
    M.hline(ox + 3, ox + 12, oy + 10, "ls1")
    for x in range(3, 13):
        M.px(ox + x, oy + 3, "ls1")
    s.names["steps"] = (6, 1)
    return finish(s)


def build():
    return [mud_plain(),
            mud_edges("grass", "mud_grass", "Mud on the meadow's edge"),
            mud_edges("sea", "bank", "Mud banks on the water", water=True),
            reeds(), thicket(), papyrus_water(), lotus(), dune_grass(), quay_edges()]
