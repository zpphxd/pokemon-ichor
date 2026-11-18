"""Skiron stone: rocks, ledges, the Skironian sea cliff, the road's cut bank,
Aphrodite's niches, the rock seat, the orchard's terrace wall and the ruined
watchtower.

All in the "rock" group: warm limestone and grey, on borrowed aethos grass,
path or sea. Light falls from the top left.

The sea cliff is a vertical profile four cells deep, read top to bottom:

  brink   the road's or the meadow's edge: borrowed ground above a lit stone lip,
          the face beginning below it (impassable: there is no rail)
  face_u  the upper face: bedding planes, fissures, a tuft on a ledge
  face_l  the lower face, in more shadow, streaked white where birds roost
  foot    the wet foot of the cliff, fallen rocks and foam on the animated sea

Its strata depend only on the row, so every variant of a row meets every
other; the variants differ inside the cell (fissures, ledges, caper bushes,
a sea cave). The cut bank above the road reuses the brink and face_u and ends
in bank_foot, scree on the path. The cliff's ends (W, E) and the plateau's
sides and inner corners let a coast step in and out.
"""
from __future__ import annotations

import math

import numpy as np

from skiron_lib import (GRASS, Struct, behave, disc, ground, oval_shadow,
                         regrounded, shade_ramp)

SEC = "stone"
GREY = ("k1", "k2", "k3", "p1", "p2", "p3")          # boulder ramp, dark -> light


def boulder(L, cx, cy, rx, ry, ramp=GREY, crack=True):
    m = disc(L.w, L.h, cx, cy, rx, ry)
    shade_ramp(L, m, ramp, cx, cy, rx, ry, rim="ink")
    if crack:
        L.line(int(cx - rx * 0.1), int(cy - ry * 0.5), int(cx + rx * 0.25), int(cy + ry * 0.15), "k2")


# --------------------------------------------------------------------------
# Rocks and pebbles
# --------------------------------------------------------------------------

def rocks():
    out = []
    s = Struct("rock", "A grey rock", 1, 1, SEC, walk=["X"], notes="One rounded limestone rock.")
    ground(s, "grass")
    oval_shadow(s.M, 8, 13, 7, 2)
    boulder(s.M, 8, 8, 6, 5)
    out.append(s)
    s = Struct("rock_slab", "A split rock", 1, 1, SEC, walk=["X"],
               notes="A flat-topped rock split in two, its halves leaning apart.")
    ground(s, "grass")
    oval_shadow(s.M, 8, 13, 7, 2)
    boulder(s.M, 5, 9, 4, 4, crack=False)
    boulder(s.M, 11, 8, 4, 5, crack=False)
    s.M.vline(8, 5, 12, "k1")
    out.append(s)
    s = Struct("boulders", "Boulders, 2 by 2", 2, 2, SEC, walk=["XX", "XX"],
               notes="A heap of rocks broken off the mountain: hillsides, the rockslide's "
                     "flanks, the cliff top.")
    ground(s, "grass")
    oval_shadow(s.M, 16, 27, 14, 4)
    boulder(s.M, 10, 14, 8, 8)
    boulder(s.M, 22, 17, 8, 9)
    boulder(s.M, 15, 24, 6, 5, crack=False)
    boulder(s.M, 25, 8, 5, 5, crack=False)
    out.append(s)
    for key, title, pts in (
            ("pebbles", "Pebbles in the grass", [(3, 4), (11, 3), (7, 9), (13, 12), (2, 13)]),
            ("pebbles2", "Scree and a tuft", [(4, 6), (9, 11), (12, 5), (3, 12)])):
        s = Struct(key, title, 1, 1, SEC, walk=["."], notes="Walkable: stones in the turf.")
        ground(s, "grass")
        for (x, y) in pts:
            s.M.blit([" a ", "abk", " kk"], {"a": "p2", "b": "k3", "k": "k2"}, x, y)
        if key == "pebbles2":
            s.M.blit(["g g", "ggg"], {"g": "gd"}, 8, 2)
        out.append(s)
    out += [regrounded(out[0], "rock_path", "A grey rock, on the path", "path"),
            regrounded(out[3], "pebbles_path", "Pebbles on the path", "path")]
    # rock_slab and pebbles2 are held for the tile budget
    return [s for s in out if s.key not in ("rock_slab", "pebbles2")]


# --------------------------------------------------------------------------
# Ledges: terrace lips that jump south, east or west
# --------------------------------------------------------------------------

def _lip_course(L, x0, x1, top_of):
    """A south-facing course of stones from x0 to x1; top_of(x) its top row."""
    for x in range(x0, x1):
        top = top_of(x)
        L.px(x, top, "p3")
        L.px(x, top + 1, "p2")
        for y in range(top + 2, 14):
            c = "p1" if (x // 5 + y) % 4 else "l1"
            if x % 5 == 4 or y == 13:
                c = "l0"
            L.px(x, y, c)
        L.px(x, 14, "k2")
        if x % 2 == 0:
            L.px(x, 15, "gd")


def ledges():
    s = Struct("lip", "Terrace lip: a ledge to jump down (south)", 3, 1, SEC, walk=["JJJ"],
               names={"W": (0, 0), "run": (1, 0), "E": (2, 0)},
               notes="One-way, MB_JUMP_SOUTH: grass above, a course of stone and its shadow "
                     "below. West end, run, east end.")
    ground(s, "grass")
    _lip_course(s.M, 0, 48, lambda x: 12 - x if x < 4 else (8 + x - 44 if x > 44 else 8))
    e = Struct("lip_east", "Terrace lip facing east (jump east)", 1, 3, SEC, walk=["X", "X", "X"],
               names={"N": (0, 0), "run": (0, 1), "S": (0, 2)},
               notes="One-way, MB_JUMP_EAST: the terrace's east edge, for a road that climbs "
                     "westward (the drop is back toward the east). North end, run, south end.")
    ground(e, "grass")
    behave(e, [(0, 0), (0, 1), (0, 2)], "MB_JUMP_EAST")
    M = e.M
    for y in range(48):
        x0 = 8
        if y < 4:
            x0 = 12 - y
        if y > 43:
            x0 = 8 + (y - 43)
        if x0 > 13:
            continue
        M.px(x0, y, "p3")
        M.px(x0 + 1, y, "p2")
        for x in range(x0 + 2, 14):
            c = "p1" if (y // 5 + x) % 4 else "l1"
            if y % 5 == 4:
                c = "l0"
            M.px(x, y, c)
        M.px(14, y, "k2")
        if y % 2 == 0:
            M.px(15, y, "gd")
    w = Struct("lip_west", "Terrace lip facing west (jump west)", 1, 3, SEC, walk=["X", "X", "X"],
               names={"N": (0, 0), "run": (0, 1), "S": (0, 2)},
               notes="One-way, MB_JUMP_WEST: the mirror of lip_east, for a road that climbs "
                     "eastward. North end, run, south end.")
    ground(w, "grass")
    behave(w, [(0, 0), (0, 1), (0, 2)], "MB_JUMP_WEST")
    w.M.a[:] = e.M.a[:, ::-1]
    return [s, e, w]


# --------------------------------------------------------------------------
# The sea cliff
# --------------------------------------------------------------------------

def _wob(x, seed, amp=1.0):
    """A 16 px periodic wobble in whole pixels."""
    t = 2 * math.pi / 16
    return int(round(amp * (0.6 * math.sin(t * x + seed) + 0.4 * math.sin(2 * t * x + 2.1 * seed))))


# Bedding planes (profile rows) and their wobble seeds. Each is a ledge: its
# lit top, then the shadow under its overhang.
BEDS = [(15, 0.0), (25, 1.3), (35, 2.6), (42, 3.9)]
DARKER = {"p3": "p2", "p2": "p1", "p1": "k3", "k3": "l1", "l1": "k2", "k2": "l0", "l0": "k1", "k1": "k1"}

# per band between beds: (lit, body, shade). The face darkens toward the sea.
BAND_TONES = [("p2", "p1", "k3"), ("p1", "k3", "l1"), ("p1", "k3", "l1"), ("k3", "l1", "k2"),
              ("k3", "l1", "k2")]


def face_px(x, y):
    """Color of the cliff face at cell column x, profile row y (7..51)."""
    # Soft strata: each band is lit along its top (a ledge catching the sun),
    # mid-tone down its face, shaded at its foot, then a dark overhang line.
    # Nothing repeats inside the 16 px but the bands' gentle wobble, so a long
    # run doesn't beat out a rhythm; the variants add the cracks and plants.
    tops = [7]
    for (b, seed) in BEDS:
        wb = b + _wob(x, seed)
        if y == wb:
            return "l0" if (x * 5 + b) % 7 else "k1"       # the shadow under a ledge
        tops.append(wb + 1)
    if y >= 48:
        return "k2" if (x * 3 + y) % 4 else "l0"
    band = max(i for i, t in enumerate(tops) if y >= t)
    y0 = tops[band]
    y1 = (BEDS[band][0] + _wob(x, BEDS[band][1]) - 1) if band < len(BEDS) else 47
    lit, body, shade = BAND_TONES[band]
    t = (y - y0) / max(1, y1 - y0)
    d = ((x * 7 + y * 3) % 5) / 10.0                        # dither the tone boundaries
    if y == y0:
        c = lit if (x + band) % 5 else body
    elif t + d < 0.45:
        c = lit if t < 0.2 and (x + y) % 2 else body
    elif t - d < 0.8:
        c = body
    else:
        c = shade
    if (x * 7 + y * 13) % 23 == 0:
        c = DARKER[c]
    return c


def paint_profile(L, ox, oy, y0, y1, xs=range(16)):
    """Paint profile rows y0..y1 (inclusive) of the face at layer offset oy."""
    for y in range(y0, y1 + 1):
        for x in xs:
            L.px(ox + x, oy + y - y0, face_px(x, y))


def brink_top(x):
    return 5 + _wob(x, 0.7)


LIPX = 2          # the column of a plateau side's lip (cliff_side, cliff_end)


def paint_brink(L, ox, oy, variant="A", xs=range(16)):
    """The brink row: ground above (left transparent), the lit lip, the face."""
    for x in xs:
        top = brink_top(x)
        if variant == "bite" and 4 <= x <= 11:
            top = 2 + abs(x - 7) // 2 + (x % 3 == 0)        # the edge has broken away
        L.px(ox + x, oy + top, "p3" if variant != "bite" or not 4 <= x <= 11 else "p1")
        L.px(ox + x, oy + top + 1, "p2" if variant != "bite" or not 4 <= x <= 11 else "l1")
        for y in range(top + 2, 16):
            L.px(ox + x, oy + y, face_px(x, max(y, 7)) if y >= 7 else "k3")
    if variant == "bite":
        # the broken edge: dark gaps and a loose block
        for (x, y) in ((5, 5), (6, 6), (8, 5), (9, 6), (10, 7), (7, 7)):
            L.px(ox + x, oy + y, "k1")
        L.blit(["pp", "lk"], {"p": "p2", "l": "l1", "k": "k2"}, ox + 6, oy + 8)
        for (x, y) in ((3, 1), (12, 2), (11, 0)):
            L.px(ox + x, oy + y, "k2")                       # cracks in the road behind
    if variant == "B":
        # grass hanging over the lip, and a stone about to go
        for (x, y) in ((2, 4), (3, 3), (3, 5), (4, 4), (12, 4), (13, 5), (12, 6)):
            L.px(ox + x, oy + y, "gd")
        L.px(ox + 3, oy + 4, "g1")
        L.blit([" pp ", "pppk", " kk "], {"p": "p2", "k": "k2"}, ox + 7, oy + 2)


def fracture(L, ox, oy, pts):
    """A vertical crevice through the rock: dark, lit on its west lip."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for y in range(y0, y1 + 1):
            x = x0 + (x1 - x0) * (y - y0) // max(1, y1 - y0)
            L.px(ox + x, oy + y, "k1")
            L.px(ox + x + 1, oy + y, "l1")


def bulge(L, ox, oy, cx, cy, rx, ry):
    """A rounded mass of rock standing out of the face, lit top left."""
    m = disc(16, 16, cx, cy, rx, ry)
    for y, x in zip(*np.nonzero(m)):
        u = ((x - cx) / rx + (y - cy) / ry) / 2
        c = "p2" if u < -0.35 else "p1" if u < 0.05 else "k3" if u < 0.4 else "l1"
        L.px(ox + x, oy + y, c)
    for y, x in zip(*np.nonzero(m)):
        if not m[min(15, y + 1), x] or y == 15:
            L.px(ox + x, oy + y + 1, "l0")                       # its shadow below


def caper(L, ox, oy, x, y):
    """A caper bush hanging from a crack: grey-green leaves, one white flower."""
    L.blit([" g g  ", "ggGgg ", "gGwGgg", " ggGg ", "  g g "], {"g": "gd", "G": "g1", "w": "w0"},
           ox + x, oy + y)


def paint_face_features(L, ox, oy, row, variant):
    """Fractures, bulges, caper bushes, white streaks, a sea cave: inside the
    cell only, so any variant meets any other."""
    # A is quiet (use it for most cells); B carries the feature (use it rarely).
    if row == "u":
        if variant == "B":
            caper(L, ox, oy, 2, 5)
            fracture(L, ox, oy, [(11, 0), (12, 7), (12, 15)])
        if variant == "C":
            bulge(L, ox, oy, 8, 6, 6, 5)
            fracture(L, ox, oy, [(3, 4), (2, 14)])
    if row == "l":
        if variant == "C":
            fracture(L, ox, oy, [(5, 0), (4, 8)])
            for y in range(4, 11):
                L.px(ox + 11, oy + y, "w0" if y % 3 else "p3")                # where a gull roosts
        if variant == "B":
            L.ellipse(ox + 3, oy + 5, ox + 11, oy + 16, "ink")               # a sea cave
            L.ellipse(ox + 4, oy + 7, ox + 10, oy + 16, "k1")
            for x in range(3, 12):
                L.px(ox + x, oy + 5 - (x in (3, 11)), "l0")


FOOT_ROCKS = {
    "A": [(5, 10, 6, 4), (13, 13, 2, 2)],
    "B": [(11, 12, 2, 2)],
    "C": [(3, 13, 2, 2), (9, 10, 4, 3)],
}
FOOT_RAMP = ("k1", "k1", "k2", "k3", "p1", "p2")


def paint_foot(L, ox, oy, variant="A", xs=range(16)):
    """The wet foot: the face's dark wet base, fallen rocks, foam; sea below."""
    xs = list(xs)
    for x in xs:
        wl = 5 + _wob(x, 5.1)
        for y in range(0, wl):
            L.px(ox + x, oy + y, face_px(x, 48 + y) if y < 3 else ("k1" if (x + y) % 3 else "l0"))
        L.px(ox + x, oy + wl, "w0" if (x * 5) % 7 else "k3")              # foam along the base
        if x % 2 == 0 or x % 5 == 1:
            L.px(ox + x, oy + wl + 1, "w0")
        if x % 4 == 1:
            L.px(ox + x, oy + wl + 2, "w0")
    for (cx, cy, rx, ry) in FOOT_ROCKS[variant]:
        if not (xs[0] <= cx <= xs[-1]):
            continue
        # foam round the rock's waterline, then the rock
        for x in range(cx - rx - 1, cx + rx + 2):
            if xs[0] <= x <= xs[-1] and (x + cy) % 3:
                L.px(ox + x, oy + min(15, cy + ry), "w0")
        m = disc(16, 16, cx, cy, rx, ry)
        for y, x in zip(*np.nonzero(m)):
            if x not in xs:
                continue
            u = ((x - cx) / rx + (y - cy) / ry) / 2
            c = "p2" if u < -0.45 else "p1" if u < -0.1 else "k3" if u < 0.2 else "k2" if u < 0.5 else "k1"
            L.px(ox + x, oy + y, c)
        for y, x in zip(*np.nonzero(m)):
            if x in xs and not all(m[min(15, max(0, y + dy)), min(15, max(0, x + dx))]
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                L.px(ox + x, oy + y, "ink" if (x - cx) + (y - cy) > -1 else L.get(ox + x, oy + y))


def surf_rocks():
    """Rocks in the surf off the cliff foot, for the sea and the map's border."""
    s = Struct("surf_rock", "Rocks in the surf", 2, 1, SEC, walk=["XX"],
               names={"A": (0, 0), "B": (1, 0)},
               notes="Wet rocks ringed with foam, on the animated sea: scatter them off the "
                     "cliff foot and use them in the map's border so the sea below the cliff "
                     "never looks empty. Impassable.")
    for i, rocks in enumerate(([(6, 8, 5, 4), (12, 11, 2, 2)],
                               [(4, 10, 3, 3), (10, 7, 4, 3), (12, 12, 2, 2)])):
        for (cx, cy, rx, ry) in rocks:
            for x in range(cx - rx - 2, cx + rx + 3):
                for y in (cy + ry - 1, cy + ry, cy + ry + 1):
                    if 0 <= x < 16 and y < 16 and ((x + y) % 3 or y == cy + ry):
                        if abs(x - cx) <= rx + 2 - (y - cy - ry + 1):
                            s.M.px(i * 16 + x, y, "w0")
            m = disc(16, 16, cx, cy, rx, ry)
            for y, x in zip(*np.nonzero(m)):
                u = ((x - cx) / rx + (y - cy) / ry) / 2
                c = "p2" if u < -0.45 else "p1" if u < -0.1 else "k3" if u < 0.2 else "k2" if u < 0.5 else "k1"
                s.M.px(i * 16 + x, y, c)
            pad = np.pad(m, 1)
            edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
            for y, x in zip(*np.nonzero(edge)):
                if (x - cx) + (y - cy) > -1:
                    s.M.px(i * 16 + x, y, "ink")
    ground(s, "sea")
    return s


def cliff():
    """The sea cliff kit: runs of each row, the W and E ends, the plateau's
    sides and inner corners."""
    out = []
    b = Struct("cliff_brink", "Sea cliff: the brink", 3, 1, SEC, walk=["XXX"],
               names={"A": (0, 0), "B": (1, 0), "bite": (2, 0)},
               notes="The top row of the sea cliff and of the cut bank: borrowed grass above a "
                     "lit stone lip, the face beginning below it. There is no rail. `bite` is "
                     "a crumbled edge biting into the ground above. Impassable. `cliff_path` "
                     "is the same art with the aethos path above the lip: the railless road "
                     "running right to the drop.")
    for i, v in enumerate(("A", "B", "bite")):
        paint_brink(b.M, i * 16, 0, v)
    ground(b, "grass")
    out.append(b)
    s = Struct("cliff", "Sea cliff: face and foot", 3, 3, SEC, walk=["XXX"] * 3,
               names={f"{row}_{v}": (i, j) for j, row in enumerate(("face_u", "face_l", "foot"))
                      for i, v in enumerate("ABC")},
               notes="The cliff under a `cliff_brink` row: `face_u`, `face_l` (stack more "
                     "face rows for a taller drop: u, l, u, l...), then `foot`, fallen rocks "
                     "and foam on the animated sea. Any variant of a row meets any other. "
                     "`A` is plain strata: use it for most cells and scatter `B` (a caper "
                     "bush and a crack; a sea cave) and `C` (a jutting boss; a gull's white "
                     "streak) at random, about one cell in four. Impassable.")
    for i, v in enumerate("ABC"):
        paint_profile(s.B, i * 16, 0, 16, 31)
        paint_face_features(s.B, i * 16, 0, "u", v)
        paint_profile(s.B, i * 16, 16, 32, 47)
        paint_face_features(s.B, i * 16, 16, "l", v)
        paint_foot(s.M, i * 16, 32, v)
    ground(s, "sea", [(0, 2), (1, 2), (2, 2)])
    out.append(s)
    p = Struct("cliff_path", "Sea cliff brink, on the path", 3, 1, SEC, walk=["XXX"],
               names={"A": (0, 0), "B": (1, 0), "bite": (2, 0)},
               notes="`cliff_brink` with the aethos limestone path (0x1D9) above the lip.")
    p.M.a[:] = b.M.a[0:16]
    ground(p, "path")
    out.append(p)

    # The west end of a cliff run: the face rounds off, sea beyond. The brink
    # corner paints its own grass (it borrows the sea).
    w = Struct("cliff_end_w", "Sea cliff, west end", 1, 4, SEC, walk=["X"] * 4,
               names={"brink": (0, 0), "face_u": (0, 1), "face_l": (0, 2), "foot": (0, 3)},
               notes="Where the cliff turns away north (a headland's corner): the face rounds "
                     "off to the west, over the sea. Use it only where the cells west of the "
                     "face are sea; beside another face use `cliff_side`. Impassable.")
    M = w.M
    for y in range(64):
        for x in range(16):
            if y < 16:                                   # the brink corner
                top = brink_top(x)
                if x < LIPX - 1:
                    continue                              # sea
                if x == LIPX - 1:
                    M.px(x, y, "k1" if y < top + 2 else "k2")
                elif x == LIPX and y <= top + 1:
                    M.px(x, y, "p2")                      # the side lip coming down
                elif x == LIPX + 1 and y < top:
                    M.px(x, y, "p3")
                elif y < top:
                    M.rgb(x, y, _grass_px(x, y))          # land (the cell borrows the sea)
                elif y == top:
                    M.px(x, y, "p3")
                elif y == top + 1:
                    M.px(x, y, "p2")
                else:
                    M.px(x, y, "p2" if x == LIPX else face_px(x, max(y, 7)))
            elif y < 48:                                  # the face, rounding off
                ex = LIPX + (_wob(y, 1.7) > 0)
                if x < ex - 1:
                    continue
                if x == ex - 1:
                    M.px(x, y, "k1")
                elif x == ex:
                    M.px(x, y, "p2" if y < 40 else "k3")  # the lit corner
                else:
                    M.px(x, y, face_px(x, y))
    paint_foot(M, 0, 48, "A", xs=range(LIPX, 16))
    for y in range(48, 64):
        M.px(LIPX - 1, y, None)
    ground(w, "sea")
    out.append(w)
    e = Struct("cliff_end_e", "Sea cliff, east end", 1, 4, SEC, walk=["X"] * 4,
               names=dict(w.names),
               notes="The mirror of cliff_end_w: the face rounds off to the east.")
    e.M.a[:] = w.M.a[:, ::-1]
    ground(e, "sea")
    out.append(e)
    # the same ends on grass close a cut bank where it runs out into the hillside
    for src, key, side in ((w, "bank_end_w", "west"), (e, "bank_end_e", "east")):
        t = Struct(key, f"Cut bank, {side} end", 1, 2, SEC, walk=["X", "X"],
                   names={"brink": (0, 0), "face_u": (0, 1)},
                   notes=f"The cliff's {side} end on grass instead of sea, to close a run of cut "
                         f"bank: its brink and face_u over a `bank_end` foot.")
        t.M.a[:] = src.M.a[0:32]
        ground(t, "grass")
        out.append(t)

    # The plateau's sides: land with its edge on the west (or east), the drop
    # beyond. And the inner corners where a brink turns into a side.
    sd = Struct("cliff_side", "Sea cliff: the plateau's sides and inner corners", 4, 1, SEC,
                walk=["XXXX"],
                names={"side_w": (0, 0), "side_e": (1, 0), "in_sw": (2, 0), "in_se": (3, 0)},
                notes="`side_w`: land whose west edge drops to the sea (the cell to its west "
                      "is face or sea). `side_e` the mirror. `in_sw`: the land cell east of a "
                      "brink run, where the brink's lip turns south into a side_w below it; "
                      "`in_se` the mirror. On borrowed grass; impassable (the edge).")
    L = sd.M
    for y in range(16):
        L.px(LIPX - 2, y, "k1")
        L.px(LIPX - 1, y, "k2")
        L.px(LIPX, y, "p2")
        L.px(LIPX + 1, y, "p3")
        if y % 5 == 2:
            L.px(LIPX + 2, y, "gd")
    L.a[:, 16:32] = L.a[:, 0:16][:, ::-1]
    # in_sw: the brink lip from the west turns down the west edge
    for x in range(0, LIPX + 2):
        top = brink_top(x)
        if x < LIPX:
            L.px(32 + x, top, "p3")
            L.px(32 + x, top + 1, "p2")
            for y in range(top + 2, 16):
                L.px(32 + x, y, face_px(x, max(y, 7)) if x < LIPX - 1 else "k1")
    for y in range(brink_top(LIPX), 16):
        L.px(32 + LIPX, y, "p2")
        L.px(32 + LIPX + 1, y, "p3")
    L.a[:, 48:64] = L.a[:, 32:48][:, ::-1]
    ground(sd, "grass")
    out.append(sd)
    out.append(surf_rocks())
    return out


_GRASS_CACHE = {}


def _grass_px(x, y):
    from skiron_lib import aethos
    if "g" not in _GRASS_CACHE:
        _GRASS_CACHE["g"] = aethos(GRASS)
    return tuple(int(v) for v in _GRASS_CACHE["g"][y % 16, x % 16])


# --------------------------------------------------------------------------
# The cut bank above the road, and Aphrodite's niches cut into it
# --------------------------------------------------------------------------

def paint_bank_foot(L, ox, oy, xs=range(16)):
    """The bank's foot: the face's lower band, then scree and shadow on the road."""
    for x in xs:
        base = 9 + _wob(x, 3.3)
        for y in range(0, base):
            L.px(ox + x, oy + y, face_px(x, 32 + y))
        L.px(ox + x, oy + base, "l0")
        if x % 2 == 0:
            L.px(ox + x, oy + base + 1, "k2")
    for (x, y) in ((2, 12), (7, 13), (12, 12), (14, 14), (4, 14)):
        if x in xs:
            L.blit([" a", "ak"], {"a": "p2", "k": "k2"}, ox + x, oy + y)


def bank():
    out = []
    s = Struct("bank", "Cut bank above the road", 3, 1, SEC, walk=["XXX"],
               names={"foot_A": (0, 0), "foot_B": (1, 0), "foot_C": (2, 0)},
               notes="The rock the road was cut from, on its uphill side. Stack `cliff` "
                     "brink, then face_u, then a `bank` foot (scree on the path below the "
                     "face); or brink straight onto a foot for a low bank. The foot borrows "
                     "the aethos path; `bank_grass` has grass below instead.")
    for i in range(3):
        paint_bank_foot(s.M, i * 16, 0)
    s.M.blit(["gg g", " ggg"], {"g": "gd"}, 18, 2)
    s.M.px(39, 3, "k1")
    s.M.px(40, 4, "k1")
    ground(s, "path")
    out.append(s)
    out.append(regrounded(s, "bank_grass", "Cut bank above grass", "grass"))
    # the bank's ends: the cliff's end art on grass, and the foot's ends
    ends = Struct("bank_end", "Cut bank ends", 2, 1, SEC, walk=["XX"],
                  names={"foot_w": (0, 0), "foot_e": (1, 0)},
                  notes="Where the bank runs out into the hillside, under `cliff_end_w` / "
                        "`cliff_end_e` brink and face_u regrounded on grass (`bank_end_w`, "
                        "`bank_end_e`). On the path.")
    paint_bank_foot(ends.M, 0, 0, xs=range(5, 16))
    for y in range(0, 10):
        ends.M.px(5, y, "p2")
    ends.M.a[:, 16:32] = ends.M.a[:, 0:16][:, ::-1]
    ground(ends, "path")
    out.append(ends)
    out.append(regrounded(ends, "bank_end_grass", "Cut bank ends, above grass", "grass"))
    return out


def niches():
    """Aphrodite's niches: a stretch of the cut bank cut with dozens of little
    niches, each with a clay dove, a lamp or nothing left, names scratched
    between, a myrtle garland, the goddess's own arched niche in the middle,
    and an altar stone at the foot."""
    s = Struct("niches", "Aphrodite's niches: the votive rock face", 3, 3, SEC,
               walk=["XXX"] * 3,
               notes="A stretch of the cut bank three cells wide (brink, face_u, foot), cut "
                     "with a dozen and a half niches holding clay doves and lamps, names "
                     "scratched between, the goddess's arched niche in the middle with a myrtle "
                     "garland swagged over it, and a low altar stone at the foot. The altar of "
                     "Aphrodite: put the bg event on the foot row's middle cell. The brink "
                     "borrows grass, the foot the path. Place it in a run of cut bank.")
    for i in range(3):
        paint_brink(s.M, i * 16, 0, "A")
        paint_profile(s.B, i * 16, 16, 16, 31)
        paint_bank_foot(s.M, i * 16, 32)
    ground(s, "grass", [(i, 0) for i in range(3)])
    ground(s, "path", [(i, 2) for i in range(3)])

    def put(x, y, c):
        (s.B if 16 <= y < 32 else s.M).px(x, y, c)

    def niche(x, y, w, h, what):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                put(xx, yy, "k1")
        for xx in range(x, x + w):
            put(xx, y, "ink")                              # the lintel's shadow
        for yy in range(y, y + h):
            put(x, yy, "ink")
            put(x + w, yy, "p2")                           # the lit jamb
        for xx in range(x - 1, x + w + 1):
            put(xx, y + h, "p3")                           # the sill
            put(xx, y + h + 1, "k3")
        if what == "dove":
            put(x + 1, y + h - 2, "w0")
            put(x + 2, y + h - 2, "w0")
            put(x + 2, y + h - 1, "w0")
            put(x + 3, y + h - 1, "w0")
            put(x + 1, y + h - 1, "k3")
        elif what == "lamp":
            put(x + 1, y + h - 1, "tc1")
            put(x + 2, y + h - 1, "tc1")
            put(x + 2, y + h - 2, "p3")                    # its flame
        elif what == "two":
            put(x + 1, y + h - 1, "w0")
            put(x + 2, y + h - 2, "w0")
            put(x + 3, y + h - 1, "tc1")

    spots = [
        # in the brink's face (rows 8-15)
        (2, 8, 4, 4, "dove"), (9, 10, 3, 3, "lamp"), (36, 9, 3, 3, "two"), (42, 8, 4, 4, ""),
        # face_u (rows 16-31), round the arched niche in the middle
        (1, 18, 4, 4, "lamp"), (8, 17, 4, 5, "dove"), (34, 18, 4, 4, "dove"), (41, 17, 4, 5, "two"),
        (3, 26, 3, 3, "dove"), (9, 25, 4, 4, "two"), (36, 26, 3, 3, ""), (42, 25, 3, 3, "lamp"),
        # the foot's face (rows 32-40)
        (4, 33, 3, 3, "lamp"), (11, 34, 3, 3, ""), (36, 34, 3, 3, "dove"), (42, 33, 3, 3, "lamp"),
    ]
    for sp in spots:
        niche(*sp)
    # little holes and scratched names between them
    for (x, y) in ((14, 13), (31, 12), (46, 14), (15, 23), (31, 24), (16, 31), (30, 31)):
        put(x, y, "ink")
        put(x + 1, y, "k1")
        put(x, y + 1, "p2")
    for (x, y) in ((5, 14), (38, 14), (2, 24), (44, 23), (7, 31), (40, 31)):
        for i in range(3):
            put(x + i, y + (i == 1), "k2")
    # the goddess's niche: arched, larger, a pale figure on a shell, doves at her feet
    ax, ay, aw, ah = 18, 14, 12, 16
    for yy in range(ay, ay + ah):
        for xx in range(ax, ax + aw):
            r = ((xx - (ax + aw / 2 - 0.5)) / (aw / 2)) ** 2 + ((yy - (ay + 5)) / 5.5) ** 2
            if yy >= ay + 5 or r <= 1.0:
                put(xx, yy, "k1" if yy > ay + 1 else "ink")
    for yy in range(ay + 1, ay + ah):
        put(ax - 1, yy, "p3" if yy > ay + 4 else "p2")
        put(ax + aw, yy, "k2")
    for xx in range(ax - 2, ax + aw + 2):
        put(xx, ay + ah, "p3")
        put(xx, ay + ah + 1, "p2")
        put(xx, ay + ah + 2, "k3")
    fig = ["   ww   ",
           "   ww   ",
           "  wppw  ",
           "  wppw  ",
           "   pp   ",
           "  w  w  ",
           " pppppp ",
           "pp pp pp"]
    for j, row in enumerate(fig):
        for i, ch in enumerate(row):
            if ch != " ":
                put(ax + 2 + i, ay + 5 + j, {"w": "w0", "p": "p2"}[ch])
    put(ax + 1, ay + ah - 1, "w0")
    put(ax + 2, ay + ah - 1, "w0")
    put(ax + aw - 3, ay + ah - 1, "w0")
    put(ax + aw - 2, ay + ah - 1, "w0")
    # a myrtle garland swagged above it, red ribbons at the ends
    for x in range(ax - 5, ax + aw + 5):
        t = (x - (ax - 5)) / (aw + 10)
        y = ay - 3 + int(round(5 * math.sin(math.pi * t)))
        put(x, y, "gd")
        put(x, y + 1, "g1" if x % 2 else "gd")
        if x % 4 == 1:
            put(x, y - 1, "gd")
        if x % 5 == 2:
            put(x, y + 1, "w0")
    for x0 in (ax - 5, ax + aw + 4):
        for yy in range(ay - 3, ay + 3):
            put(x0, yy, "tc1")
    # the altar at the foot, an offering smouldering on it
    a0 = 17
    for yy in range(38, 46):
        for xx in range(a0, a0 + 14):
            put(xx, yy, "p1")
    for xx in range(a0, a0 + 14):
        put(xx, 37, "ink")
        put(xx, 38, "p3")
        put(xx, 39, "p2")
        put(xx, 45, "k2")
    for yy in range(37, 46):
        put(a0 - 1, yy, "ink")
        put(a0 + 14, yy, "ink")
        put(a0 + 13, yy, "l1")
    for xx in range(a0 + 2, a0 + 12, 3):
        put(xx, 42, "l1")                                   # a carved band
    put(a0 + 6, 36, "tc1")
    put(a0 + 7, 35, "tc1")
    put(a0 + 7, 36, "p3")
    put(a0 + 8, 36, "tc1")
    put(a0 + 7, 34, "k3")
    put(a0 + 8, 33, "k3")                                   # a thread of smoke
    return s


# --------------------------------------------------------------------------
# The rock seat
# --------------------------------------------------------------------------

def seat():
    """A rough throne cut into a knob of rock, facing the sea."""
    s = Struct("rock_seat", "The rock seat", 2, 2, SEC, walk=["XX", "XX"],
               notes="Xerxes's seat: a rough throne cut into a knob of rock, its high back "
                     "and arms facing out over the bay. Put the bg event on either bottom cell. "
                     "On borrowed grass; `rock_seat_path` sits on the path.")
    ground(s, "grass")
    M = s.M
    oval_shadow(M, 16, 29, 15, 3)
    # the knob of rock it is cut from: rough, rounded, lit top left
    rock = np.zeros((32, 32), bool)
    for (cx, cy, rx, ry) in ((16, 15, 14, 13), (7, 20, 7, 9), (25, 21, 7, 8), (16, 6, 9, 6)):
        rock |= disc(32, 32, cx, cy, rx, ry)
    rock[29:] = False
    for y, x in zip(*np.nonzero(rock)):
        u = ((x - 13) / 15 + (y - 12) / 14) / 2
        c = "p2" if u < -0.4 else "p1" if u < -0.1 else "k3" if u < 0.2 else "l1" if u < 0.45 else "k2"
        if (x * 7 + y * 5) % 19 == 0:
            c = "k2"
        M.px(x, y, c)
    pad = np.pad(rock, 1)
    edge = rock & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        M.px(x, y, "ink")
    # the throne cut into its front, smooth and pale against the rough rock:
    # a tall round-topped back, two blocky arms, the seat, a step below
    def box(x0, y0, x1, y1, top, face, lit, shade, top_rows=2):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = top if y < y0 + top_rows else face
                if x == x0 and y >= y0 + top_rows:
                    c = lit
                if x == x1:
                    c = shade
                M.px(x, y, c)
        for x in range(x0 - 1, x1 + 2):
            M.px(x, y0 - 1, "ink")
            M.px(x, y1 + 1, "ink")
        for y in range(y0 - 1, y1 + 2):
            M.px(x0 - 1, y, "ink")
            M.px(x1 + 1, y, "ink")
    box(11, 3, 20, 17, "p2", "p1", "p3", "k3", top_rows=1)        # the back
    for (x, y) in ((11, 3), (20, 3)):
        M.px(x, y, "ink")                                        # rounded top corners
    M.rect(13, 6, 6, 9, "l1")                                    # its shadowed inner face
    M.hline(13, 18, 6, "k2")
    box(6, 12, 10, 21, "p3", "p1", "p2", "k3")                   # the west arm, lit
    box(21, 12, 25, 21, "p2", "k3", "p1", "l1")                  # the east arm, in shade
    box(11, 16, 20, 21, "p3", "p1", "p2", "k3", top_rows=3)      # the seat
    M.hline(11, 20, 19, "k3")                                    # the seat's front edge
    box(8, 24, 23, 26, "p2", "k3", "p1", "l1", top_rows=1)       # the step
    for (x, y) in ((15, 9), (17, 11), (14, 12)):
        M.px(x, y, "k3")                                         # chisel marks
    M.blit(["g g", "ggg"], {"g": "gd"}, 26, 4)
    M.blit(["gg"], {"g": "gd"}, 3, 13)
    return [s, regrounded(s, "rock_seat_path", "The rock seat, on the path", "path")]


# --------------------------------------------------------------------------
# The orchard's terrace wall
# --------------------------------------------------------------------------

def paint_drystone(L, x0, y0, w, h, seed=0):
    """Dry stone: rough unequal stones, lit top left, dark gaps between."""
    y = y0
    row = 0
    while y < y0 + h:
        sh = 3 + ((row * 7 + seed) % 3 == 0)
        x = x0 - ((row * 5 + seed) % 5)
        k = 0
        while x < x0 + w:
            sw = 3 + ((row * 3 + k * 7 + seed) % 5)
            body = ("p1", "l1", "p1", "k3")[(row * 2 + k * 3 + seed) % 4]
            for yy in range(y, min(y + sh, y0 + h)):
                for xx in range(max(x, x0), min(x + sw, x0 + w)):
                    i, j = xx - x, yy - y
                    if i == sw - 1 or j == sh - 1:
                        c = "l0" if (xx + yy) % 3 else "k1"
                    elif i == 0 or j == 0:
                        c = "p2"
                    else:
                        c = body
                    L.px(xx, yy, c)
            x += sw
            k += 1
        y += sh
        row += 1


def orchard_wall():
    s = Struct("terrace_wall", "The orchard's terrace wall", 4, 1, SEC, walk=["XXX."],
               names={"W": (0, 0), "run": (1, 0), "E": (2, 0), "steps": (3, 0)},
               notes="A dry-stone retaining wall one row high: the terrace's grass above, the "
                     "wall's face, its shadow on the grass below. West end, run, east end, and "
                     "steps up through it (walkable). For the terrace orchard behind the "
                     "Sickle thicket, and any terraced hillside.")
    ground(s, "grass")
    from skiron_lib import Layer
    M = Layer(80, 16)
    for i in range(4):
        paint_drystone(M, i * 16, 4, 16, 10, seed=i * 3 + 1)
        M.hline(i * 16, i * 16 + 15, 3, "p3")                     # coping
        M.hline(i * 16, i * 16 + 15, 4, "p2")
        for x in range(i * 16, i * 16 + 16):
            M.px(x, 14, "k2")
            if x % 2 == 0:
                M.px(x, 15, "gd")
            if x % 4 == 1:
                M.px(x, 2, "gd")                                   # grass lipping over
    # ends: the wall steps down into the slope
    for y in range(0, 16):
        for x in range(0, 16):
            if x < 7 - y // 3:
                M.px(x, y, None)
            if x > 8 + y // 3:
                M.px(48 + x, y, None)
    for y in range(4, 15):
        M.px(7 - y // 3, y, "p2")
        M.px(56 + y // 3, y, "l0")
    # steps: treads with risers, cut through the wall
    M.rect(64, 2, 16, 13, "p1")
    for y in (3, 7, 11):
        M.hline(66, 77, y, "p3")
        M.hline(66, 77, y + 1, "p2")
        M.hline(66, 77, y + 3, "l0")
    M.vline(65, 2, 14, "k1")
    M.vline(78, 2, 14, "k1")
    M.vline(64, 2, 14, "p2")
    M.vline(79, 2, 14, "l0")
    for i, src in enumerate((0, 1, 3, 4)):
        s.M.a[:, i * 16:i * 16 + 16] = M.a[:, src * 16:src * 16 + 16]
    return [s]


# --------------------------------------------------------------------------
# The ruined watchtower
# --------------------------------------------------------------------------

def ashlar(L, x0, y0, w, h, seed=0, lit=("p2", "p1"), shade="l1"):
    """Isodomic ashlar: even courses of squared blocks, half-offset. The
    pattern repeats every 8 px each way, so a wall's inner tiles are shared."""
    for y in range(y0, y0 + h):
        course = (y - y0) // 4
        off = (course % 2) * 4 + seed
        for x in range(x0, x0 + w):
            jy = (y - y0) % 4 == 3
            jx = (x - x0 + off) % 8 == 7
            if jy:
                c = "k3"
            elif jx:
                c = "l1"
            elif (y - y0) % 4 == 0 or (x - x0 + off) % 8 == 0:
                c = lit[0]
            else:
                c = lit[1]
            L.px(x, y, c)


def watchtower():
    s = Struct("watchtower", "The ruined watchtower", 2, 4, SEC,
               walk=["TT", "XX", "XX", "XX"],
               notes="A square stone tower, a pyrgos for watching the road, its top fallen in. "
                     "The broken crown is drawn over the player (walk behind it); the rest is "
                     "impassable. The doorway is choked with fallen blocks. On borrowed grass.")
    ground(s, "grass")
    M, T = s.M, s.T
    oval_shadow(M, 16, 61, 15, 3)
    x0, x1 = 3, 28                                     # the tower's sides (x1 inclusive)
    # The whole tower is painted on one 32x64 canvas, then row 0 moves to the
    # top layer (walk behind the crown) and rows 1-3 stay in the middle layer.
    from skiron_lib import Layer
    Cv = Layer(32, 64)
    # Seen from above and in front: the back wall's broken top, its inner face
    # in shade, the dark inside, the front wall's broken top, then its face.
    back = lambda x: 2 + (x * 5 // 7) % 3 + (x > 20) * 2 - (12 < x < 17)
    front = lambda x: 10 + (2 if 8 < x < 15 else 0) + (x * 3 // 5) % 2 - (x > 23)
    ashlar(Cv, x0, 0, x1 - x0 + 1, 60, seed=2)
    for x in range(x0, x1 + 1):
        bt, ft = back(x), front(x)
        for y in range(0, bt):
            Cv.px(x, y, None)
        side = x < x0 + 3 or x > x1 - 3                 # the side walls' tops
        for y in range(bt, ft):
            if y == bt:
                c = "p3"
            elif y == bt + 1:
                c = "p2"
            elif side:
                c = "p1" if x < x0 + 3 else "k3"
            elif y < bt + 4:
                c = "k3" if (x + y) % 5 else "k2"          # the back wall's inner face
            else:
                c = "k1" if y < ft - 1 else "ink"         # the dark inside
            Cv.px(x, y, c)
        Cv.px(x, ft, "p3")
        Cv.px(x, ft + 1, "p2")
        Cv.px(x, bt - 1, "ink")
    # the lit west quoins, the shaded east edge, outlines
    for y in range(0, 60):
        if Cv.get(x0, y) is not None and y > back(x0) + 1:
            Cv.px(x0, y, "p3" if (y // 4) % 2 else "p2")
        if Cv.get(x1, y) is not None and y > back(x1) + 1:
            Cv.px(x1, y, "k3")
    for y in range(0, 60):
        if y >= back(x0) - 1:
            Cv.px(x0 - 1, y, "ink")
        if y >= back(x1) - 1:
            Cv.px(x1 + 1, y, "ink")
    Cv.hline(x0 - 1, x1 + 1, 60, "ink")
    # the doorway, choked with fallen blocks
    Cv.rect(11, 42, 10, 18, "ink")
    Cv.rect(12, 43, 8, 17, "k1")
    Cv.rect(10, 40, 12, 2, "p2")
    Cv.hline(10, 21, 40, "p3")
    for (cx, cy, rx, ry) in ((13, 56, 3, 3), (18, 56, 3, 3), (16, 52, 3, 2)):
        boulder(Cv, cx, cy, rx, ry, crack=False)
    # a slit window, a crack, a shrub rooted in the broken top
    Cv.rect(21, 22, 2, 7, "ink")
    Cv.px(21, 29, "p3")
    Cv.px(22, 29, "p3")
    for y in range(13, 38):
        x = 7 + (y // 4) % 2 + (y - 13) // 9
        Cv.px(x, y, "k1")
        Cv.px(x + 1, y, "l1")
    Cv.blit(["  g ", " ggg", "gg g"], {"g": "gd"}, 21, 5)
    Cv.px(22, 6, "g1")
    T.a[0:16] = Cv.a[0:16]
    M.a[16:64][Cv.a[16:64][..., 3] > 0] = Cv.a[16:64][Cv.a[16:64][..., 3] > 0]
    M.a[0:16] = 0
    return [s]


# --------------------------------------------------------------------------
# Pan's Crook's climbable face (WORLD_EXPLORATION §2; tools/ichor/art/crook_marks.py)
# --------------------------------------------------------------------------

CROOK_ROLES = {"H": "ink", "h": "k1", "L": "w0", "W": "p2", "I": "gd", "i": "g1", "v": "g2",
               "V": "k1", "S": "p3"}


def crook():
    """One column of the cliff (or the cut bank) with paired handholds, ivy over
    the brink and the hoof votive at the foot: MB_ROCK_CLIMB, climbed with Pan's
    Crook in either direction. Stack `brink`, any number of `face_u`/`face_l`,
    then `foot`, in place of one column of the plain cliff."""
    import crook_marks as CM
    s = Struct("crook", "Pan's Crook's face: handholds up the cliff", 4, 1, SEC, walk=["XXXX"],
               names={"brink": (0, 0), "face_u": (1, 0), "face_l": (2, 0), "foot": (3, 0)},
               notes="A climbable column for the cliff and the cut bank: `brink` (ivy over the "
                     "lip), `face_u` and `face_l` (stack as many as the drop needs), then `foot` "
                     "(the bank's foot, with the goat-hoof votive). Every cell is MB_ROCK_CLIMB and "
                     "impassable: face it and press A to climb with Pan's Crook, up or down. Put "
                     "walkable ground at both ends. `crook_path` borrows the path above the brink "
                     "and below the foot instead of grass.")
    paint_brink(s.M, 0, 0, "A")
    paint_profile(s.B, 16, 0, 16, 31)
    paint_profile(s.B, 32, 0, 32, 47)
    paint_bank_foot(s.M, 48, 0)
    CM.paint(s.M.px, CM.marks("top", lip=brink_top(1)), CROOK_ROLES, 0, 0)
    CM.paint(s.B.px, CM.marks("face"), CROOK_ROLES, 16, 0)
    CM.paint(s.B.px, CM.marks("face"), CROOK_ROLES, 32, 0)
    CM.paint(s.M.px, CM.marks("foot", foot_base=9 + _wob(2, 3.3)), CROOK_ROLES, 48, 0)
    ground(s, "grass", [(0, 0), (3, 0)])
    behave(s, [(0, 0), (1, 0), (2, 0), (3, 0)], "MB_ROCK_CLIMB")
    return [s, regrounded(s, "crook_path", "Pan's Crook's face, on the path", "path")]


def build():
    return [*rocks(), *ledges(), *cliff(), *bank(), niches(), *seat(), *orchard_wall(), *watchtower(),
            *crook()]
