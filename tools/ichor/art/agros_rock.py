"""Agros stone: rock outcrops, field walls that join in any direction, the
terrace lip ledge, Kronion Hill's natural rock faces and rock-cut stair, the
rocky shore where grass meets the sea, and the alonia (threshing floor).

Warm aethos limestone (l0 l1 p1 p2 p3) with whitewashed caps, on aethos
grass; the shore uses the "water" group's greys and foam.
"""
from __future__ import annotations

import numpy as np

from agros_lib import GRASS, Struct

SEC = "stone"
STONE = ["l0", "l1", "p1", "p2", "p3"]


def grass_floor(s):
    s.B.texture(GRASS, 0, 0, s.w * 16, s.h * 16)


def stones(L, x0, y0, w, h, seed=0, ramp=STONE, mortar="l0"):
    """Dry stone: rough, unequal stones laid without mortar. Each stone is lit
    on its top left, shaded on its bottom right; the gaps between are dark and
    broken, never ruled lines. Phase-locked to x0, y0 so repeats tile."""
    tone = [ramp[2], ramp[1], ramp[2], ramp[3]]
    y = y0
    row = 0
    while y < y0 + h:
        sh = 3 + ((row * 7 + seed) % 3 == 0)
        x = x0 - ((row * 5 + seed) % 5)
        k = 0
        while x < x0 + w:
            sw = 3 + ((row * 3 + k * 7 + seed) % 5)
            body = tone[(row * 2 + k * 3 + seed) % 4]
            for yy in range(y, min(y + sh, y0 + h)):
                for xx in range(max(x, x0), min(x + sw, x0 + w)):
                    i, j = xx - x, yy - y
                    corner = (i == 0 or i == sw - 1) and (j == 0 or j == sh - 1)
                    if i == sw - 1 or j == sh - 1:
                        c = mortar if not corner and (xx + yy) % 3 else ramp[1]
                    elif (i == 0 and j < sh - 1) or j == 0:
                        c = ramp[min(4, ramp.index(body) + 1)]
                    else:
                        c = body
                    if corner:
                        c = mortar
                    L.px(xx, yy, c)
            x += sw
            k += 1
        y += sh
        row += 1


def boulder(L, cx, cy, rx, ry, ramp=("l0", "k2", "k3", "p2", "p3"), rim="ink"):
    """A rounded limestone boulder lit from the top left, with a crack."""
    for y in range(L.h):
        for x in range(L.w):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d > 1:
                continue
            u = ((x - cx) / rx + (y - cy) / ry) / 2
            c = ramp[4] if u < -0.45 else ramp[3] if u < -0.05 else ramp[2] if u < 0.35 else ramp[1]
            if d > 0.78:
                c = rim
            L.px(x, y, c)
    L.line(int(cx - rx * 0.1), int(cy - ry * 0.5), int(cx + rx * 0.2), int(cy + ry * 0.2), ramp[0])


def ground_shadow(L, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if L.get(x, y) in ("g1", "g2", "g3") and (x + y) % 2 == 0:
                L.px(x, y, "gd")


def outcrops():
    s = Struct("outcrop", "Limestone outcrop, 2 by 2", 2, 2, SEC, walk=["XX", "XX"],
               notes="Rocks breaking through the turf, for wood edges and hillsides.")
    grass_floor(s)
    ground_shadow(s.B, 4, 24, 28, 7)
    boulder(s.M, 11, 15, 9, 9)
    boulder(s.M, 22, 18, 9, 10)
    boulder(s.M, 15, 24, 7, 6)
    boulder(s.M, 26, 9, 5, 5)
    r = Struct("rock", "A single rock", 1, 1, SEC, walk=["X"], notes="One limestone rock.")
    grass_floor(r)
    ground_shadow(r.B, 3, 11, 12, 4)
    boulder(r.M, 8, 8, 6, 6)
    return [s, r]


# --------------------------------------------------------------------------
# Field walls: whitewash-capped dry stone that joins N, E, S, W.
# --------------------------------------------------------------------------

WALL_KEYS = ["NS", "N", "S", "EW", "E", "W", "ES", "SW", "NE", "NW", "NES", "ESW", "NSW", "NEW", "NESW", ""]


def _wall_textures():
    """The two stone textures every wall piece cuts from, locked to the cell grid
    so pieces that show the same stretch of wall share their 8x8 tiles."""
    from agros_lib import Layer
    ns, ew, end = Layer(16, 16), Layer(16, 16), Layer(16, 16)
    stones(ns, 4, 0, 8, 16, seed=1)
    stones(ew, 0, 6, 16, 8, seed=2)
    stones(end, 4, 10, 8, 5, seed=3)
    return ns, ew, end


_WALL_TEX = None


def paint_wall(L, ox, oy, key):
    """One wall cell. A north-south run shows its cap from above and its stones
    on the lit west flank; an east-west run shows its south face."""
    global _WALL_TEX
    if _WALL_TEX is None:
        _WALL_TEX = _wall_textures()
    ns, ew, end = _WALL_TEX
    n, e, s_, w = ("N" in key), ("E" in key), ("S" in key), ("W" in key)
    L.texture(GRASS, ox, oy, 16, 16)

    def cut(tex, x0, x1, y0, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = tex.get(x, y)
                if c:
                    L.px(ox + x, oy + y, c)

    # north-south column, 8 px wide
    if n or s_ or not (e or w):
        top = 0 if n else 3
        bot = 15 if s_ else 9
        cut(ns, 4, 11, top, bot)
        for y in range(top, bot + 1):
            L.px(ox + 3, oy + y, "l0")
            L.px(ox + 12, oy + y, "l0")
            L.px(ox + 13, oy + y, "gd")
            L.px(ox + 4, oy + y, "w0")
            L.px(ox + 5, oy + y, "p3")
        if not n:
            L.hline(ox + 4, ox + 11, oy + top, "w0")
            L.hline(ox + 3, ox + 12, oy + top - 1, "l0")
        if not s_:
            # the column's south end shows its face
            cut(end, 4, 11, 10, 14)
            L.hline(ox + 4, ox + 11, oy + 10, "p2")
            L.hline(ox + 3, ox + 12, oy + 15, "l0")
            L.vline(ox + 3, oy + 10, oy + 15, "l0")
            L.vline(ox + 12, oy + 10, oy + 15, "l0")
    # east-west run: cap at y=4-5, face to y=13, shadow at 14-15
    if e or w:
        x0 = 0 if w else 3
        x1 = 15 if e else 12
        cut(ew, x0, x1, 6, 13)
        L.hline(ox + x0, ox + x1, oy + 4, "w0")
        L.hline(ox + x0, ox + x1, oy + 5, "p3")
        L.hline(ox + x0, ox + x1, oy + 3, "l0")
        L.hline(ox + x0, ox + x1, oy + 14, "l0")
        for x in range(x0, x1 + 1):
            if x % 2 == 0:
                L.px(ox + x, oy + 15, "gd")
        if not w:
            L.vline(ox + x0, oy + 3, oy + 14, "l0")
            L.px(ox + x0 + 1, oy + 4, "w0")
        if not e:
            L.vline(ox + x1, oy + 3, oy + 14, "l0")
            L.vline(ox + x1 + 1, oy + 5, oy + 14, "gd")


def walls():
    s = Struct("field_wall", "Field wall: whitewash-capped dry stone, every join", 8, 2, SEC,
               walk=["XXXXXXXX", "XXXXXXXX"],
               names={k or "post": (i % 8, i // 8) for i, k in enumerate(WALL_KEYS)},
               notes="Sixteen pieces named by the sides they join (N E S W), so a wall can "
                     "run, turn, branch and end anywhere in a field. A north-south run "
                     "shows its cap and lit flank; an east-west run its south face.")
    for i, k in enumerate(WALL_KEYS):
        paint_wall(s.B, (i % 8) * 16, (i // 8) * 16, k)
    return s


# --------------------------------------------------------------------------
# The terrace lip: a low stone drop that reads as a ledge.
# --------------------------------------------------------------------------

def ledges():
    s = Struct("lip", "Terrace lip: a stone ledge to jump down", 3, 1, SEC, walk=["JJJ"],
               names={"W": (0, 0), "run": (1, 0), "E": (2, 0)},
               notes="One-way, MB_JUMP_SOUTH: grass above, a short course of stone and its "
                     "shadow below. West end, run, east end.")
    grass_floor(s)
    L = s.B
    for x in range(48):
        top = 8
        if x < 4:
            top = 12 - x
        if x > 43:
            top = 8 + (x - 43)
        L.px(x, top, "p3")
        L.px(x, top + 1, "p2")
        for y in range(top + 2, 14):
            L.px(x, y, "p1" if (x // 5 + y) % 4 else "l1")
            if (x % 5 == 4 and y > top + 2) or y == 13:
                L.px(x, y, "l0")
        L.px(x, 14, "l0" if top < 13 else L.get(x, 14))
        if (x % 2 == 0) and top < 13:
            L.px(x, 15, "gd")
    return s


# --------------------------------------------------------------------------
# Kronion Hill: natural rock faces and a rock-cut stair.
# --------------------------------------------------------------------------

FACE_KEYS = ["run", "run2", "W", "E", "stair"]


def paint_face(L, ox, oy, key):
    """A south-facing band of grey-gold limestone, grass tufting over its brow."""
    L.texture(GRASS, ox, oy, 16, 16)
    brow = [3, 2, 2, 3, 4, 3, 2, 2, 3, 3, 2, 3, 4, 4, 3, 2] if key != "run2" else \
           [2, 3, 4, 3, 2, 2, 3, 3, 2, 2, 3, 4, 3, 2, 2, 3]
    for x in range(16):
        top = brow[x]
        bot = 14
        if key == "W":
            top = max(top, 13 - x)
        if key == "E":
            top = max(top, x - 2)
        if key == "upE" and x > 9:          # the band steps up a row to the east
            top = 0
        if key == "upW" and x < 6:
            top = 0
        if top >= bot:
            continue
        for y in range(oy + top, oy + bot):
            k = y - (oy + top)
            c = "p3" if k == 0 else "p2" if k == 1 else ("p1" if ((x + ox) // 3 + y) % 5 else "l1")
            if ((x + ox) * 7 + y * 3) % 13 == 0 and k > 2:
                c = "l0"
            if (x + ox) % 6 == 5 and k > 3:
                c = "l1"
            L.px(ox + x, y, c)
        L.px(ox + x, oy + bot, "l0")
        if (x + ox) % 2 == 0:
            L.px(ox + x, oy + 15, "gd")
        if top > 0:
            L.px(ox + x, oy + top - 1, "g1")
    if key == "stair":
        for i, y in enumerate((4, 7, 10, 13)):
            L.hline(ox + 3, ox + 12, oy + y - 1, "p3")
            L.hline(ox + 3, ox + 12, oy + y, "p2")
            L.hline(ox + 3, ox + 12, oy + y + 1, "l1")
        L.vline(ox + 2, oy + 2, oy + 15, "l0")
        L.vline(ox + 13, oy + 2, oy + 15, "l0")
        for y in range(oy + 2, oy + 16):
            for x in range(ox + 3, ox + 13):
                if L.get(x, y) in ("g1", "g2", "g3", "gd", None):
                    L.px(x, y, "p1")
    if key in ("upE", "upW"):
        # the side of the step: a short west- or east-facing rock flank
        xs = range(ox + 9, ox + 11) if key == "upE" else range(ox + 5, ox + 7)
        for x in xs:
            for y in range(oy, oy + 14):
                L.px(x, y, "l1" if key == "upE" else "p2")


def faces():
    s = Struct("rockface", "Kronion Hill rock face and rock-cut stair", 5, 1, SEC,
               walk=["XXXX."], names={k: (i, 0) for i, k in enumerate(FACE_KEYS)},
               notes="A south-facing band of natural rock, one cell tall: two runs, west and "
                     "east ends sloping into the grass, a stair cut through it (walkable), and "
                     "two jogs where the band steps up a row (upE: higher to the east).")
    for i, k in enumerate(FACE_KEYS):
        paint_face(s.B, i * 16, 0, k)
    return s


# --------------------------------------------------------------------------
# Rocky shore: grass, then grey rocks and foam, then the aethos sea.
# --------------------------------------------------------------------------

SHORE_KEYS = ["W", "W2", "N", "N2", "NW", "NE", "E", "E2"]


def paint_shore(L, ox, oy, key):
    """Rocks along the sea side of a grass cell. The sea itself is the next
    cell (aethos 0x170), so only foam is drawn here."""
    L.texture(GRASS, ox, oy, 16, 16)
    ramp = ["k2", "k3", "w1", "w0"]
    rocks = {
        "W": [(1, 3, 3, 3), (2, 9, 3, 3), (1, 14, 2, 2), (5, 6, 2, 2)],
        "W2": [(1, 1, 2, 2), (2, 6, 3, 3), (1, 12, 3, 3), (5, 13, 2, 2)],
        "N": [(3, 1, 3, 3), (9, 2, 3, 3), (14, 1, 2, 2), (6, 5, 2, 2)],
        "N2": [(1, 1, 2, 2), (6, 2, 3, 3), (12, 1, 3, 3), (13, 5, 2, 2)],
        "NW": [(1, 2, 3, 3), (6, 1, 3, 3), (12, 1, 2, 2), (2, 8, 3, 3), (1, 13, 2, 2), (6, 6, 2, 2)],
    }
    flip = key in ("E", "E2", "NE")
    base = {"E": "W", "E2": "W2", "NE": "NW"}.get(key, key)
    for (cx, cy, rx, ry) in rocks[base]:
        if flip:
            cx = 15 - cx
        for y in range(16):
            for x in range(16):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d > 1:
                    continue
                u = ((x - cx) / rx + (y - cy) / ry) / 2
                c = ramp[3] if u < -0.4 else ramp[2] if u < 0 else ramp[1] if u < 0.4 else ramp[0]
                if d > 0.75:
                    c = "ink"
                L.px(ox + x, oy + y, c)
    # foam licking the seaward edge
    for i in range(16):
        if base in ("W", "W2", "NW") and i % 3 != 1:
            L.px(ox + (15 if flip else 0), oy + i, "b4")
        if base in ("N", "N2", "NW") and i % 3 != 2:
            L.px(ox + i, oy, "b4")
    if flip:
        # mirrored pieces must stay pixel-mirrored so Porytiles can share tiles
        a = L.a[oy:oy + 16, ox:ox + 16].copy()
        L.a[oy:oy + 16, ox:ox + 16] = a


def shore():
    s = Struct("shore", "Rocky shore: grass meeting the sea", 8, 1, SEC,
               walk=["XXXXXXXX"], names={k: (i, 0) for i, k in enumerate(SHORE_KEYS)},
               notes="Grey rocks and foam on the sea side of a grass cell; the sea is the "
                     "neighboring aethos cell. Named by where the sea is: W, N, E (two runs "
                     "each), and the outer corners NW and NE. Impassable.")
    for i, k in enumerate(SHORE_KEYS):
        paint_shore(s.B, i * 16, 0, k)
    return s


# --------------------------------------------------------------------------
# The alonia: a round threshing floor of flagstones in a ring of upright stones.
# --------------------------------------------------------------------------

def alonia():
    s = Struct("alonia", "Alonia: the round threshing floor", 4, 4, SEC, walk=["...."] * 4,
               notes="A village threshing floor: flagstones in a ring of upright stones, "
                     "open to walk on. Drawn as one quarter mirrored, so it costs a quarter "
                     "of its tiles.")
    grass_floor(s)
    q = np.zeros((32, 32, 4), np.uint8)
    from agros_lib import Layer
    Q = Layer(32, 32)
    Q.texture(GRASS, 0, 0, 32, 32)
    for y in range(32):
        for x in range(32):
            dx, dy = 31.5 - x, 31.5 - y
            r = (dx * dx + dy * dy) ** 0.5
            if r <= 25:
                ring = int(r // 6)
                ang = (np.arctan2(dy, dx) * 180 / np.pi) % 90
                seg = int(ang // (30 if ring >= 2 else 45))
                c = "p2" if (ring + seg) % 2 else "p1"
                if r % 6 < 0.9 or (ang % (30 if ring >= 2 else 45)) < 2.2:
                    c = "l1"
                if ((x * 7 + y * 5) % 17) == 0 and c != "l1":
                    c = "p3"
                Q.px(x, y, c)
            elif r <= 28.5:
                # upright kerb stones round the rim
                a = (np.arctan2(dy, dx) * 180 / np.pi) % 90
                block = int(a // 9) % 2
                Q.px(x, y, "p2" if r < 26.5 else "l1")
                if a % 9 < 1.2:
                    Q.px(x, y, "l0")
                if r >= 27.8:
                    Q.px(x, y, "l0")
            elif r <= 29.5 and (x + y) % 2 == 0 and dy > 0:
                Q.px(x, y, "gd")
    q = Q.a
    full = np.zeros((64, 64, 4), np.uint8)
    full[:32, :32] = q
    full[:32, 32:] = q[:, ::-1]
    full[32:, :32] = q[::-1, :]
    full[32:, 32:] = q[::-1, ::-1]
    s.B.a[:] = full
    return s


def build():
    return [*outcrops(), walls(), ledges(), faces(), shore(), alonia()]
