"""gTileset_Delphoi: Route 28 (the Sacred Olives, the Kastalian Gorge) and Delphoi.

Delphoi is Delphi on the south face of Parnassos: a sanctuary terraced up a
steep slope under the Phaedriades, the two "shining" cliffs whose pale
limestone turns rose and gold in the low sun. Below it the god's olive plain
runs down to Kirrha; up the gorge between the cliffs the Kastalian spring
falls in two steps, and in Act III the Titans' last muster camps in it.

Drawn with kalliste_lib/emporion_lib's Layer and Struct (the same packing and
the same borrowed aethos ground as every Ichor outdoor secondary).
tools/ichor/art/delphoi_build.py compiles it.

Palette plan (secondary slots 6-12, one group per 8x8 tile):
  cliff   the Phaedriades: rosy-gold limestone in six steps, a shine, scrub
  marble  Parian marble, gilding, painted blue and red: temple, treasuries,
          statues, the Sacred Way's flags, the Omphalos and its net
  stone   grey Parnassos limestone and earth: the polygonal wall, terrace
          walls, steps, the Sibyl's rock, the oldest altar, the stadium's sand
  grove   aethos's grass, laurels, olives, pines and their shadows
  clay    terracotta roofs, warm plaster, shutters: the lower town's houses
  camp    hide, timber, rope, iron, fire and red cloth: the Titans' muster,
          torches, the warden's thatch
  water   the spring: water, bronze lion heads, the basin's marble lip
"""
from __future__ import annotations

import math
import random

import numpy as np

import emporion_lib as E
import kalliste_lib as K
from emporion_lib import Struct, finish
from kalliste_lib import Layer

NAME = "delphoi"

NEW = {
    # the Phaedriades: limestone that shines rose and gold
    "ph0": (88, 64, 64), "ph1": (136, 104, 96), "ph2": (176, 144, 120),
    "ph3": (208, 176, 144), "ph4": (232, 208, 176), "ph5": (248, 240, 216),
    "phr": (200, 136, 104),
    # a shadow on aethos's grass
    "gsh": (120, 128, 64),
    # hide tents
    "hd0": (88, 56, 40), "hd1": (136, 96, 64), "hd2": (184, 144, 96),
    # laurel berries, near black
    "lb": (40, 40, 64),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    "cliff": ["ink", "sk", "ph0", "ph1", "ph2", "ph3", "ph4", "ph5", "phr", "ov0", "ov1", "ov2",
              "c2", "gr1", "gsh"],
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "g0", "g1", "br", "b0", "b1", "b2",
               "b3", "rd"],
    "stone": ["ink", "sk", "s0", "s1", "s2", "s3", "s4", "s5", "wt0", "wt1", "ol1", "ol2", "w0",
              "e1", "e2"],
    "grove": ["ink", "gr0", "gr1", "gr2", "gsh", "ov0", "ov1", "ov2", "ov3", "c1", "c2", "c3",
              "tk0", "tk1", "lb"],
    "clay": ["ink", "tc0", "tc1", "tc2", "tc3", "oc0", "oc1", "oc2", "oc3", "w0", "w2", "b0",
             "b1", "wd0", "wd1"],
    "camp": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "hd0", "hd1", "hd2", "rd", "fl", "fc",
             "ir", "g1", "w0"],
    "water": ["ink", "b0", "wa1", "b1", "wr", "wa3", "b2", "b3", "w0", "br", "g0", "g1", "m2",
              "m3", "m4"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}


def validate(structs):
    """emporion_lib's checks, against Delphoi's palette groups."""
    saved = E.GROUP_RGB
    E.GROUP_RGB = GROUP_RGB
    try:
        return E.validate(structs)
    finally:
        E.GROUP_RGB = saved


def S(key, title, w, h, walk, ground, notes="", names=None):
    s = Struct(key, title, w, h, walk=walk, notes=notes, ground="none")
    if isinstance(ground, str) and len(ground) > 1 and ground in E.BORROWED | E.DRAWN:
        s.set_ground(ground)
    else:
        s.ground_rows(ground)
    s.names = names or {}
    return s


def hsh(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000


# ==========================================================================
# Rock: the Phaedriades and the gorge walls
# ==========================================================================

def _sites(seed, n, w=16, h=32):
    rnd = random.Random(seed)
    return [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(0.8, 1.3)) for _ in range(n)]


SITES = {k: _sites(100 + k, 13, w=32) for k in range(4)}


def rock_face(L, x0, y0, w, h, seed=0, ox=0, oy=0, mask=None):
    """The Phaedriades: tall slabs of limestone, split by vertical joints (the
    cliffs weather into columns), each slab lit on its upper left, with streaks of
    rose where the iron stains run down. A Voronoi field stretched upright on a
    16 x 32 torus, so a face repeats every 16 px across and 32 down."""
    # Rounded masses of rock on a 16 x 32 torus (a Voronoi field, like
    # Acrocorinth's), each lit on its upper left and shadowed lower right, dark
    # crevices between; a faint upright joint every 16 px makes the cliff read
    # as the Phaedriades' columns rather than a heap.
    sites = SITES[seed % 4]
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if mask is not None and not mask(x - x0, y - y0):
                continue
            X, Y = (x - ox) % 32 + 0.5, (y - oy) % 32 + 0.5
            best = []
            for (sx, sy, k) in sites:
                for dx0 in (-32, 0, 32):
                    for dy0 in (-32, 0, 32):
                        dx, dy = X - (sx + dx0), (Y - (sy + dy0)) * 1.15
                        best.append(((dx * dx + dy * dy) ** 0.5 * k, dx, dy))
            best.sort()
            d1, dx, dy = best[0]
            gap = best[1][0] - d1
            if gap < 0.55:
                c = "ph0"
            elif gap < 1.1:
                c = "ph1"
            else:
                lit = -(dx * 0.65 + dy * 0.75)
                c = ("ph5" if lit > 3.8 else "ph4" if lit > 1.0 else "ph3" if lit > -1.4
                     else "ph2")
                if c == "ph2" and int(X) % 6 == 2:
                    c = "phr"
            L.px(x, y, c)


def _scrub(L, x, y):
    for (dx, dy, c) in ((0, 0, "ov2"), (1, 0, "ov1"), (-1, 1, "ov1"), (0, 1, "ov0"), (1, 1, "ov0"),
                        (2, 1, "ov1")):
        L.px(x + dx, y + dy, c)


def cliff_kit():
    """The Phaedriades as a 4 x 4 kit: a crest row (the cliff's lip against the
    slope above), two face rows and a foot row (its base, with its shadow cast
    on the grass), each in a west edge, two middles and an east edge. Rows 1
    and 2 repeat down a tall cliff; columns 1 and 2 alternate along a long one."""
    s = S("phaedriades", "The Phaedriades: cliff kit", 4, 4,
          walk=["XXXX"] * 4,
          ground=["gggg", "gnng", "gnng", "gggg"],
          names={"crest_W": (0, 0), "crest": (1, 0), "crest2": (2, 0), "crest_E": (3, 0),
                 "face_W": (0, 1), "face": (1, 1), "face2": (2, 1), "face_E": (3, 1),
                 "faceb_W": (0, 2), "faceb": (1, 2), "faceb2": (2, 2), "faceb_E": (3, 2),
                 "foot_W": (0, 3), "foot": (1, 3), "foot2": (2, 3), "foot_E": (3, 3)})
    W, H = 64, 64
    # the outline of the rock in the 64 x 64 kit: the lip wanders 3-6 px down
    # the crest row; the west and east edges wander 2-6 px in; the foot ends on
    # row 56 and its shadow lies below it
    def lip(x):
        return 4 + int(2 * math.sin(x * 0.45) + 1.5 * math.sin(x * 1.3 + 1))

    def west(y):
        return 3 + int(2 * math.sin(y * 0.5) + 1.2 * math.sin(y * 1.7))

    def east(y):
        return 60 - int(2 * math.sin(y * 0.43 + 2) + 1.2 * math.sin(y * 1.5))
    FOOT = 56
    full = Layer(W, H)
    for y in range(H):
        for x in range(W):
            inside = lip(x) <= y < FOOT and west(y) <= x <= east(y)
            if inside:
                full.px(x, y, "ph3")
    alpha = full.a[..., 3] > 0
    rock_face(full, 0, 0, W, H, seed=1, mask=lambda x, y: alpha[y, x])
    # the lip: a lit rim with scrub on it
    for x in range(W):
        y = lip(x)
        if west(y) <= x <= east(y):
            full.px(x, y, "ink")
            full.px(x, y + 1, "ph5")
            full.px(x, y + 2, "ph4")
    for x in (9, 26, 41, 53):
        _scrub(full, x, lip(x) + 1)
    # the edges: ink outline, lit west flank, shaded east flank
    for y in range(H):
        if lip(0) <= y < FOOT:
            wx, ex = west(y), east(y)
            full.px(wx, y, "ink")
            full.px(wx + 1, y, "ph5")
            full.px(ex, y, "ink")
            full.px(ex - 1, y, "ph1")
    # the foot: a dark base line, fallen stones and the shadow (rows 56-63, grove)
    for x in range(W):
        if west(FOOT - 1) <= x <= east(FOOT - 1):
            full.px(x, FOOT - 1, "ink")
            full.px(x, FOOT - 2, "ph1")
    shadow = Layer(W, H)
    for x in range(W):
        if west(FOOT) - 1 <= x <= east(FOOT) + 2:
            depth = 3 + (hsh(x, 1) % 3)
            for y in range(FOOT, FOOT + depth):
                shadow.px(x, y, "gsh")
    for (x, y) in ((12, 58), (13, 58), (36, 59), (50, 58)):
        shadow.px(x, y, "gr1")
    # into the struct: borrowed cells draw in the middle layer, drawn cells in
    # the bottom
    for cy in range(4):
        for cx in range(4):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            tgt = s.M if (cx, cy) in s.borrowed else s.B
            tgt.a[sl] = full.a[sl]
            m = shadow.a[sl][..., 3] > 0
            tgt.a[sl][m] = shadow.a[sl][m]
    return finish(s)


def cliff_scree():
    """Single cells to break a cliff's foot: a fallen block, and a tuft of scrub
    on the rock (a face cell)."""
    s = S("scree", "Fallen blocks under the cliffs", 2, 1, walk=["XX"], ground=["gn"],
          names={"block": (0, 0), "face_scrub": (1, 0)})
    L = s.M
    L.ellipse(2, 5, 13, 14, "ph2")
    L.ellipse(3, 5, 11, 11, "ph4")
    L.ellipse(5, 6, 9, 8, "ph5")
    L.hline(3, 12, 15, "gsh")
    s.M.a[:, :16][(s.M.a[:, :16, 3] > 0)]  # noqa: B018 (kept for clarity)
    sil = s.M.a[:16, :16, 3] > 0
    for y in range(16):
        for x in range(16):
            if sil[y, x] and not (sil[max(0, y - 1), x] and sil[min(15, y + 1), x]
                                  and sil[y, max(0, x - 1)] and sil[y, min(15, x + 1)]):
                if y < 15:
                    L.px(x, y, "ink")
    rock_face(s.B, 16, 0, 16, 16, seed=1, oy=16)
    _scrub(s.B, 22, 5)
    _scrub(s.B, 26, 11)
    return finish(s)


# ==========================================================================
# The polygonal wall, terrace walls, the Sacred Way's flags and steps
# ==========================================================================

def _polygons(seed, w, h, n):
    rnd = random.Random(seed)
    return [(rnd.uniform(0, w), rnd.uniform(0, h)) for _ in range(n)]


POLY = _polygons(5, 32, 16, 9)


def polygonal(L, x0, y0, w, h, ox=0):
    """The polygonal wall under the temple terrace: big many-sided blocks fitted
    without mortar, each joint a fine dark line, the blocks' faces dressed
    smooth and lit from the top left. Repeats every 32 px across."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 32 + 0.5, (y - y0) + 0.5
            ds = []
            for (sx, sy) in POLY:
                for dx0 in (-32, 0, 32):
                    dx, dy = X - (sx + dx0), Y - sy
                    ds.append((dx * dx + dy * dy, dx, dy))
            ds.sort()
            (d1, dx, dy), d2 = ds[0], ds[1][0]
            if d2 ** 0.5 - d1 ** 0.5 < 0.7:
                c = "s0"
            else:
                lit = -(dx * 0.7 + dy * 0.7)
                c = "s5" if lit > 3.5 else "s4" if lit > 0 else "s3" if lit > -3 else "s2"
            L.px(x, y, c)


def polywall_kit():
    """The polygonal wall, one cell tall: a coping of squared stones, the
    polygonal face, its foot on the lower terrace. West end, two middles, east
    end; a stair through it; and the sanctuary's gate (two piers and a lintel)."""
    s = S("polywall", "The polygonal wall", 6, 1, walk=["XXXX.X"], ground=["gnnggg"],
          names={"W": (0, 0), "M": (1, 0), "M2": (2, 0), "E": (3, 0), "stair": (4, 0),
                 "pier": (5, 0)})
    full = Layer(96, 16)
    polygonal(full, 0, 3, 64, 12)
    for x in range(64):
        full.px(x, 0, "ink")
        full.px(x, 1, "s5" if x % 8 else "s2")
        full.px(x, 2, "s3" if x % 8 else "s1")
        full.px(x, 15, "ink")
    # the ends: the west end steps down, the east end too
    for y in range(16):
        for x in range(0, 4 + (y // 6)):
            full.px(x, y, None)
        for x in range(60 - (y // 6), 64):
            full.px(x, y, None)
        full.px(4 + (y // 6), y, "ink")
        full.px(59 - (y // 6), y, "ink")
    # a stair of six treads cut through the wall
    for y in range(16):
        t = y // 3
        for x in range(66, 78):
            c = "s5" if y % 3 == 0 else "s3" if y % 3 == 1 else "s1"
            full.px(x, y, c)
        full.px(65, y, "ink")
        full.px(78, y, "ink")
        full.px(64, y, "s2")
        full.px(79, y, "s2")
        _ = t
    # a gate pier: a squared block with a lit face
    E.ashlar(full, 82, 0, 12, 16, ox=82)
    E.outline_rect(full, 82, 0, 12, 16)
    for cx in range(6):
        sl = np.s_[:, cx * 16:cx * 16 + 16]
        tgt = s.M if (cx, 0) in s.borrowed else s.B
        tgt.a[sl] = full.a[sl]
    return finish(s)


def pezoula_kit():
    """A dry-stone terrace wall (pezoula) a cell tall on the slope: you can hop
    down it southward. Rough rounded fieldstones, grass on top. West end, two
    middles, east end."""
    s = S("pezoula", "Dry-stone terrace wall (a ledge)", 4, 1, walk=["JJJJ"], ground=["gggg"],
          names={"W": (0, 0), "M": (1, 0), "M2": (2, 0), "E": (3, 0)})
    L = s.M
    rnd = random.Random(3)
    for x in range(64):
        top = 7 + (1 if (x // 5) % 3 == 0 else 0)
        if x < 3 or x > 60:
            top += 3
        for y in range(top, 16):
            L.px(x, y, "s2")
    # fieldstones
    for cx in range(0, 64, 5):
        for row, yy in ((0, 9), (1, 13)):
            x = cx + (2 if row else 0) + rnd.randint(0, 1)
            if x < 2 or x > 61:
                continue
            L.ellipse(x - 2, yy - 2, x + 2, yy + 1, "s3")
            L.px(x - 1, yy - 2, "s4")
            L.px(x, yy - 2, "s5")
    for x in range(64):
        for y in range(16):
            if L.get(x, y) is not None and (y == 15 or L.get(x, y - 1) is None):
                L.px(x, y, "ink" if y == 15 else "s1")
    for x in range(3, 61):
        L.px(x, 15, "s0")
    for b in s.behaviors:
        s.behaviors[b] = "MB_JUMP_SOUTH"
    return finish(s)


def way_kit():
    """The Sacred Way: marble flags with a kerb of grey stone where they meet the
    grass. A 3 x 3 patch (its centre is plain flags) and the four inside
    corners; and broad marble steps where the Way climbs a terrace."""
    s = S("way", "The Sacred Way: flags, kerbs, inner corners, steps", 8, 3,
          walk=["........", "........", "........"],
          ground=["gggggppp", "gpgggppp", "ggggpppp"],
          names={"TL": (0, 0), "T": (1, 0), "TR": (2, 0), "L": (0, 1), "C": (1, 1),
                 "R": (2, 1), "BL": (0, 2), "B": (1, 2), "BR": (2, 2),
                 "in_NW": (3, 0), "in_NE": (4, 0), "in_SW": (3, 1), "in_SE": (4, 1),
                 "steps": (5, 0), "steps_W": (6, 0), "steps_E": (7, 0),
                 "flag2": (5, 1), "flag4": (6, 1), "worn": (7, 1),
                 "C2": (4, 2), "steps2": (5, 2), "steps2_W": (6, 2), "steps2_E": (7, 2)})

    def flags(L, x0, y0, keep):
        tmp = Layer(16, 16)
        E.paving(tmp, 0, 0, 16, 16)
        for y in range(16):
            for x in range(16):
                if keep(x, y):
                    L.a[y0 + y, x0 + x] = tmp.a[y, x]
                    if not keep(x - 1, y) or not keep(x + 1, y) or not keep(x, y - 1) \
                            or not keep(x, y + 1):
                        L.px(x0 + x, y0 + y, "m3")

    def edge(n, s_, w, e):
        def keep(x, y):
            if y < 0 or y > 15 or x < 0 or x > 15:
                return False
            wob = (hsh(x, y, 7) % 2)
            if n and y < 3 + wob:
                return False
            if s_ and y > 12 - wob:
                return False
            if w and x < 3 + wob:
                return False
            if e and x > 12 - wob:
                return False
            return True
        return keep
    for (name, n, s_, w, e) in (("TL", 1, 0, 1, 0), ("T", 1, 0, 0, 0), ("TR", 1, 0, 0, 1),
                                ("L", 0, 0, 1, 0), ("R", 0, 0, 0, 1), ("BL", 0, 1, 1, 0),
                                ("B", 0, 1, 0, 0), ("BR", 0, 1, 0, 1)):
        cx, cy = s.names[name]
        flags(s.M, cx * 16, cy * 16, edge(n, s_, w, e))
    # the centre: plain flags
    cx, cy = s.names["C"]
    E.paving(s.B, 16, 16, 16, 16, ox=16, oy=16)
    # inside corners: flags everywhere but one corner nibbled by grass
    for name, (qx, qy) in (("in_NW", (0, 0)), ("in_NE", (1, 0)), ("in_SW", (0, 1)), ("in_SE", (1, 1))):
        cx, cy = s.names[name]

        def keep(x, y, qx=qx, qy=qy):
            if not (0 <= x < 16 and 0 <= y < 16):
                return True
            ax = x if qx == 0 else 15 - x
            ay = y if qy == 0 else 15 - y
            return not (ax < 4 and ay < 4)
        flags(s.M, cx * 16, cy * 16, keep)
    # variants of the centre
    for name, v in (("flag2", 1), ("flag4", 2), ("C2", 1)):
        cx, cy = s.names[name]
        E.paving(s.B, cx * 16, cy * 16, 16, 16, ox=cx * 16, oy=cy * 16, variant=v)
    cx, cy = s.names["worn"]
    E.paving(s.B, cx * 16, cy * 16, 16, 16, ox=cx * 16, oy=cy * 16)
    for (x, y) in ((4, 6), (5, 6), (6, 7), (10, 9), (11, 9), (9, 3)):
        s.B.px(cx * 16 + x, cy * 16 + y, "m2")
    # steps: four treads, each lit along its nose
    for name in ("steps", "steps_W", "steps_E", "steps2", "steps2_W", "steps2_E"):
        cx, cy = s.names[name]
        for y in range(16):
            for x in range(16):
                t = y % 4
                c = "w0" if t == 0 else "m1" if t == 1 else "m2" if t == 2 else "m4"
                s.B.px(cx * 16 + x, cy * 16 + y, c)
        if name.endswith("_W"):
            s.B.vline(cx * 16, cy * 16, cy * 16 + 15, "ink")
            s.B.vline(cx * 16 + 1, cy * 16, cy * 16 + 15, "m3")
        if name.endswith("_E"):
            s.B.vline(cx * 16 + 15, cy * 16, cy * 16 + 15, "ink")
            s.B.vline(cx * 16 + 14, cy * 16, cy * 16 + 15, "m4")
    for cy in range(3):
        for cx in range(8):
            if s.ground.get((cx, cy)) == "pave":
                s.ground[(cx, cy)] = "none"
    return finish(s)


# ==========================================================================
# Trees
# ==========================================================================

def _crown(L, cx, cy, rx, ry, seed, dark="c1", mid="c2", lit="c3", hi="ov3", lobes=7,
           berries=0):
    """A rounded crown of overlapping leaf clumps, lit from the top left: every
    clump outlined in the darkest green where it meets the sky or a clump
    behind it, so the crown reads as many leaves, not a ball."""
    rnd = random.Random(seed)
    clumps = []
    for i in range(lobes):
        a = 2 * math.pi * i / lobes + rnd.uniform(-0.3, 0.3)
        r = rnd.uniform(0.35, 0.6)
        clumps.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r,
                       rx * rnd.uniform(0.42, 0.55), ry * rnd.uniform(0.42, 0.55)))
    clumps.append((cx, cy, rx * 0.55, ry * 0.55))
    clumps.sort(key=lambda c: c[1])          # back clumps first
    for (x, y, a, b) in clumps:
        for yy in range(int(y - b) - 1, int(y + b) + 2):
            for xx in range(int(x - a) - 1, int(x + a) + 2):
                d = ((xx + 0.5 - x) / a) ** 2 + ((yy + 0.5 - y) / b) ** 2
                if d > 1:
                    continue
                lx, ly = (xx + 0.5 - x) / a, (yy + 0.5 - y) / b
                lit_v = -(lx * 0.7 + ly * 0.8)
                if d > 0.78:
                    c = dark
                elif lit_v > 0.75:
                    c = hi
                elif lit_v > 0.15:
                    c = lit
                elif lit_v > -0.5:
                    c = mid
                else:
                    c = dark
                L.px(xx, yy, c)
    for _ in range(berries):
        bx, by = int(cx + rnd.uniform(-rx * 0.6, rx * 0.6)), int(cy + rnd.uniform(-ry * 0.3, ry * 0.6))
        if L.get(bx, by) in (mid, dark):
            L.px(bx, by, "lb")
    # the outline: ink round the whole crown
    a = L.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "ink")


def _trunk(L, x, y0, y1, w=3):
    for y in range(y0, y1):
        L.px(x - 1, y, "ink")
        L.px(x, y, "tk1")
        for i in range(1, w - 1):
            L.px(x + i, y, "tk0")
        L.px(x + w - 1, y, "ink")


def laurels():
    """The god's bay laurels: a dense, dark, glossy crown, taller than wide, with
    dark berries; two silhouettes so a grove never repeats; and the great laurel
    at the top of the grove that drops a sprig a day."""
    out = []
    for key, seed, title in (("laurel", 11, "Bay laurel"), ("laurel_b", 29, "Bay laurel, second shape")):
        s = S(key, title, 2, 2, walk=["XX", "XX"], ground=["gg", "gg"])
        L = Layer(32, 32)
        for x in range(6, 27):
            for y in range(28, 31):
                if (x - 16) ** 2 / 110 + (y - 29) ** 2 / 3 <= 1:
                    L.px(x, y, "gsh")
        _trunk(L, 15, 20, 29)
        crown = Layer(32, 32)
        _crown(crown, 16, 12 if key == "laurel" else 13, 13 if key == "laurel" else 14,
               12 if key == "laurel" else 11, seed, berries=5)
        m = crown.a[..., 3] > 0
        L.a[m] = crown.a[m]
        s.M.a[:] = L.a
        out.append(finish(s))
    s = S("great_laurel", "The great laurel of the grove", 3, 3, walk=["XXX", "XXX", "XXX"],
          ground=["ggg", "ggg", "ggg"])
    L = Layer(48, 48)
    for x in range(6, 43):
        for y in range(42, 47):
            if (x - 24) ** 2 / 300 + (y - 44) ** 2 / 5 <= 1:
                L.px(x, y, "gsh")
    _trunk(L, 21, 30, 44, w=6)
    L.px(22, 36, "tk1")
    L.px(23, 37, "tk1")
    crown = Layer(48, 48)
    _crown(crown, 24, 17, 21, 17, 47, lobes=10, berries=12)
    m = crown.a[..., 3] > 0
    L.a[m] = crown.a[m]
    # a red votive ribbon tied on a low branch
    for (x, y) in ((14, 30), (15, 31), (15, 32), (16, 33)):
        L.px(x, y, "lb")
    s.M.a[:] = L.a
    out.append(finish(s))
    return out


def oldest_olive():
    """The oldest olive on the plain: a vast gnarled trunk split open into a
    hollow you could stand in, under a wide silver-green crown."""
    s = S("oldest_olive", "The oldest olive (hollow trunk)", 3, 3,
          walk=["XXX", "XXX", "XXX"], ground=["ggg", "ggg", "ggg"],
          names={"hollow": (1, 2)})
    L = Layer(48, 48)
    for x in range(4, 45):
        for y in range(42, 47):
            if (x - 24) ** 2 / 360 + (y - 44) ** 2 / 5 <= 1:
                L.px(x, y, "gsh")
    # the trunk: two twisted halves either side of the hollow
    for y in range(24, 45):
        spread = 6 + (y - 24) // 3
        for x in range(24 - spread - 4, 24 + spread + 4):
            dx = x - 24
            if abs(dx) < 3 + (y - 24) // 8 and y > 28:
                c = "ink" if abs(dx) >= 2 + (y - 24) // 8 else "tk0"   # the hollow
                L.px(x, y, c if c != "tk0" else "ink")
                continue
            twist = math.sin(y * 0.5 + dx * 0.4)
            c = "tk1" if twist > 0.3 else "ov0" if twist < -0.5 else "tk0"
            L.px(x, y, c)
        L.px(24 - spread - 4, y, "ink")
        L.px(24 + spread + 3, y, "ink")
    crown = Layer(48, 48)
    _crown(crown, 24, 14, 22, 13, 5, dark="ov0", mid="ov1", lit="ov2", hi="ov3", lobes=11)
    m = crown.a[..., 3] > 0
    L.a[m] = crown.a[m]
    s.M.a[:] = L.a
    return finish(s)


# ==========================================================================
# Buildings
# ==========================================================================

def _pediment(L, x0, y0, w, h, sculpture=True, paint=True):
    """A pediment: an ink-edged triangle of marble with a painted blue tympanum,
    a raking cornice, acroteria at the peak and the ends."""
    peak = x0 + w // 2
    for y in range(y0, y0 + h):
        k = (y - y0) / max(1, h - 1)
        half = int(k * (w // 2))
        for x in range(peak - half, peak + half + (w % 2)):
            L.px(x, y, "m1")
        L.px(peak - half, y, "ink")
        L.px(peak + half - 1 + (w % 2), y, "ink")
        if y > y0 + 2:
            L.px(peak - half + 1, y, "w0")
            for x in range(peak - half + 3, peak + half - 2 + (w % 2)):
                L.px(x, y, "b0" if paint else "m3")
    L.hline(x0, x0 + w - 1, y0 + h - 1, "ink")
    if sculpture and h > 8:
        # little figures in the tympanum
        for i, fx in enumerate(range(peak - (w // 3), peak + (w // 3), 5)):
            top = y0 + h - 3 - min(4, (w // 3 - abs(fx - peak)) // 3)
            L.vline(fx, top, y0 + h - 2, "m1")
            L.px(fx, top - 1, "w0")
    # acroteria
    L.blit([".g.", "ggg"], {"g": "g1"}, peak - 1, y0 - 2)
    L.px(x0, y0 + h - 3, "g0")
    L.px(x0 + w - 1, y0 + h - 3, "g0")


def _entablature(L, x0, y0, w, doric=True):
    """Architrave and frieze: Doric triglyphs (blue) and metopes, or an Ionic
    sculpted band; a red-painted taenia between."""
    L.rect(x0, y0, w, 8, "m1")
    L.hline(x0, x0 + w - 1, y0, "ink")
    L.hline(x0, x0 + w - 1, y0 + 1, "w0")
    L.hline(x0, x0 + w - 1, y0 + 4, "rd")
    for x in range(x0, x0 + w):
        X = (x - x0) % 8
        if doric:
            if X in (1, 2, 3) and True:
                L.px(x, y0 + 2, "b1")
                L.px(x, y0 + 3, "b0" if X == 2 else "b1")
        else:
            if X % 3 == 0:
                L.px(x, y0 + 3, "m3")
    L.hline(x0, x0 + w - 1, y0 + 5, "m2")
    L.hline(x0, x0 + w - 1, y0 + 6, "m3")
    L.hline(x0, x0 + w - 1, y0 + 7, "ink")


def _stylobate(L, x0, y0, w, h):
    for y in range(y0, y0 + h):
        t = (y - y0) % 3
        L.hline(x0, x0 + w - 1, y, "w0" if t == 0 else "m2" if t == 1 else "m4")
    L.hline(x0, x0 + w - 1, y0 + h - 1, "ink")
    L.vline(x0, y0, y0 + h - 1, "ink")
    L.vline(x0 + w - 1, y0, y0 + h - 1, "ink")


def _kore(L, x, y, h):
    """A caryatid: a maiden holding up the porch on her head, in a painted peplos."""
    L.rect(x + 1, y, 5, 2, "m1")            # the capital basket on her head
    L.hline(x, x + 6, y, "ink")
    L.ellipse(x + 1, y + 2, x + 5, y + 6, "m1")   # head
    L.px(x + 2, y + 4, "m4")
    L.px(x + 4, y + 4, "m4")
    for yy in range(y + 7, y + h):
        wid = 3 + min(2, (yy - y - 7) // 5)
        for xx in range(x + 3 - wid // 2 - 1, x + 3 + wid // 2 + 2):
            L.px(xx, yy, "m2" if (xx + yy) % 4 == 0 else "m1")
        L.px(x + 3 - wid // 2 - 1, yy, "ink")
        L.px(x + 3 + wid // 2 + 1, yy, "ink")
    for yy in range(y + 10, y + h, 4):
        L.px(x + 3, yy, "rd")
    L.ellipse(x, y + 1, x + 6, y + 7, None) if False else None


def treasury(key, title, caryatids=False):
    """A treasury on the Sacred Way: a little temple of one room, two columns (or
    two maidens) between the side walls' ends, a door in the middle, on two
    steps. 3 cells wide, 4 tall; the doorway is the bottom middle cell."""
    s = S(key, title, 3, 4, walk=["XXX", "XXX", "XXX", "XDX"],
          ground=["ggg", "nnn", "nnn", "nnn"], names={"door": (1, 3)})
    L = Layer(48, 64)
    _pediment(L, 1, 4, 46, 12, paint=True)
    _entablature(L, 2, 16, 44, doric=not caryatids)
    if caryatids:
        for x in range(2, 46):
            if x % 4 == 0:
                L.px(x, 19, "g0")
                L.px(x, 20, "g1")
    # the cella's shade behind the porch
    L.rect(2, 24, 44, 32, "m4")
    L.rect(6, 24, 36, 4, "m5")
    # antae
    for ax in (2, 40):
        E.shaft(L, ax, 24, 6, 32, fluted=False)
    # the door: bronze leaves, open a crack
    L.rect(18, 32, 12, 24, "ink")
    L.rect(19, 33, 10, 23, "br")
    L.vline(24, 33, 55, "ink")
    for yy in range(36, 54, 6):
        L.px(21, yy, "g0")
        L.px(27, yy, "g0")
    if caryatids:
        _kore(L, 10, 24, 32)
        _kore(L, 31, 24, 32)
    else:
        for cx in (11, 31):
            E.doric_capital(L, cx, 24, 6)
            E.shaft(L, cx, 29, 6, 27)
    _stylobate(L, 0, 56, 48, 8)
    # the step is cut away in front of the door
    L.rect(18, 56, 12, 8, "m2")
    L.hline(18, 29, 56, "w0")
    for cy in range(4):
        for cx in range(3):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            tgt = s.M if (cx, cy) in s.borrowed else s.B
            tgt.a[sl] = L.a[sl]
    # drawn cells must be solid below: back-fill holes with the stylobate's grey
    for cy in range(1, 4):
        for cx in range(3):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            hole = s.B.a[sl][..., 3] == 0
            s.B.a[sl][hole] = list(C["m3"]) + [255]
    return finish(s)


def temple_apollo():
    """The Temple of Apollo's front: a hexastyle Doric porch on a three-step
    krepis, the pediment with Apollo arriving in his chariot, gilded shields on
    the architrave, the great door in the middle under KNOW THYSELF. 7 cells
    wide, 5 tall; the door is the bottom middle cell."""
    s = S("temple_apollo", "The Temple of Apollo (front)", 7, 5,
          walk=["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXDXXX"],
          ground=["ggggggg", "nnnnnnn", "nnnnnnn", "nnnnnnn", "nnnnnnn"],
          names={"door": (3, 4), "inscription": (3, 3)})
    W, H = 112, 80
    L = Layer(W, H)
    _pediment(L, 1, 1, 110, 15, paint=True)
    # the chariot in the tympanum: four horses and the god, gilded
    for i, hx in enumerate(range(38, 62, 6)):
        L.blit(["mmmm.", ".mmmm", ".m..m"], {"m": "w0"}, hx, 11)
    L.blit(["g", "g", "gg"], {"g": "g1"}, 64, 9)
    _entablature(L, 2, 16, 108, doric=True)
    for x in range(10, 104, 16):
        L.ellipse(x, 18, x + 3, 21, "g1")    # the gilded shields of the old war
        L.px(x + 1, 19, "g0")
    L.rect(2, 24, 108, 48, "m4")
    L.rect(4, 24, 104, 5, "m5")
    cols = [5, 23, 41, 65, 83, 101]
    for cx in cols:
        E.doric_capital(L, cx, 24, 6)
        E.shaft(L, cx, 29, 6, 43)
    # the great door, shadowed, with a bronze threshold
    L.rect(48, 34, 16, 38, "ink")
    L.rect(50, 36, 12, 36, "m5")
    L.rect(51, 37, 10, 35, "sk") if False else None
    L.vline(56, 36, 71, "ink")
    for yy in (42, 52, 62):
        L.hline(50, 61, yy, "br")
    # KNOW THYSELF over it: a line of tiny letters
    for x in range(49, 63, 2):
        L.px(x, 31, "ink")
    _stylobate(L, 0, 72, 112, 8)
    L.rect(48, 72, 16, 8, "m2")
    for y in (72, 75, 78):
        L.hline(48, 63, y, "w0")
    for cy in range(5):
        for cx in range(7):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            tgt = s.M if (cx, cy) in s.borrowed else s.B
            tgt.a[sl] = L.a[sl]
            if tgt is s.B:
                hole = s.B.a[sl][..., 3] == 0
                s.B.a[sl][hole] = list(C["m3"]) + [255]
    return finish(s)


def lesche():
    """The Lesche of the Knidians: a long plain clubhouse of stone, its blank
    walls famous for the paintings inside; a porch of two Doric columns at the
    east end, the door under it. 5 x 3; the door is at (3, 2)."""
    s = S("lesche", "The Lesche of the Knidians", 5, 3, walk=["XXXXX", "XXXXX", "XXXDX"],
          ground=["ggggg", "nnnnn", "nnnnn"], names={"door": (3, 2)})
    L = Layer(80, 48)
    E.roof(L, 0, 2, 80, 14, pal="clay")
    for x in range(80):
        L.px(x, 2, "ink")
    L.rect(0, 16, 80, 32, "s3")
    E.ashlar(L, 0, 16, 80, 32, ox=0, oy=0)
    L.hline(0, 79, 16, "ink")
    # the porch at the east end
    L.rect(44, 20, 34, 28, "s1")
    for cx in (46, 70):
        E.doric_capital(L, cx, 18, 5, ramp=("s1", "s2", "s3", "s4", "s5"))
        E.shaft(L, cx, 23, 5, 23, ramp=("s1", "s2", "s3", "s4", "s5"), fluted=False)
    L.rect(52, 26, 13, 20, "ink")
    L.rect(53, 27, 11, 19, "e1")
    L.vline(58, 27, 45, "ink")
    L.hline(0, 79, 47, "ink")
    _copy_cells(s, L)
    return finish(s)


def _copy_cells(s, L, fill="s2"):
    for cy in range(s.h):
        for cx in range(s.w):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            tgt = s.M if (cx, cy) in s.borrowed else s.B
            tgt.a[sl] = L.a[sl]
            if tgt is s.B:
                hole = s.B.a[sl][..., 3] == 0
                s.B.a[sl][hole] = list(C[fill]) + [255]


def house(key, title, w, door, window=None, hives=False, roof_rows=1, plaster=True, byre=False):
    """A lower-town house built into the slope: a terracotta roof over warm
    plastered rubble walls, a blue door, a shuttered window. Variants: the
    melissai's house with clay hive-jars set into its wall, bees at the holes;
    Koretas's with a goat byre's wattle door beside the house door."""
    h = 1 + roof_rows + 1
    walk = ["X" * w] * (h - 1) + ["".join("D" if x == door else "X" for x in range(w))]
    s = S(key, title, w, h, walk=walk, ground=["g" * w] + ["n" * w] * (h - 1),
          names={"door": (door, h - 1)})
    L = Layer(w * 16, h * 16)
    E.roof(L, 0, 4, w * 16, 16 * roof_rows + 8)
    top = 12 + 16 * roof_rows
    if plaster:
        E.stucco(L, 0, top, w * 16, h * 16 - top, base="oc2", lit="oc3", shade="oc1")
    # the rubble footing
    for x in range(w * 16):
        for y in range(h * 16 - 4, h * 16):
            L.px(x, y, "oc0" if (x // 3 + y) % 3 == 0 else "oc1")
    L.hline(0, w * 16 - 1, top, "ink")
    L.vline(0, top, h * 16 - 1, "ink")
    L.vline(w * 16 - 1, top, h * 16 - 1, "ink")
    L.hline(0, w * 16 - 1, h * 16 - 1, "ink")
    dx = door * 16 + 3
    L.rect(dx - 1, top + 3, 12, h * 16 - top - 3, "ink")
    L.rect(dx, top + 4, 10, h * 16 - top - 4, "b0")
    L.vline(dx + 5, top + 4, h * 16 - 2, "ink")
    L.px(dx + 3, top + 12, "w0")
    L.hline(dx - 2, dx + 11, top + 2, "wd1")
    if window is not None:
        wx = window * 16 + 4
        L.rect(wx - 1, top + 3, 10, 9, "ink")
        L.rect(wx, top + 4, 4, 7, "b1")
        L.rect(wx + 4, top + 4, 4, 7, "b0")
        L.hline(wx - 2, wx + 9, top + 12, "w2")
    if hives:
        # a wall of clay hive-jars laid on their sides, mouths outward
        for i, hx in enumerate(range(4, w * 16 - 4, 12)):
            if abs(hx - dx) < 14:
                continue
            for row, hy in enumerate((top + 4, top + 12)):
                xx = hx + (6 if row else 0)
                if xx > w * 16 - 10 or abs(xx - dx) < 14:
                    continue
                L.ellipse(xx, hy, xx + 8, hy + 6, "tc1")
                L.ellipse(xx + 1, hy + 1, xx + 6, hy + 4, "tc2")
                L.ellipse(xx + 3, hy + 2, xx + 5, hy + 4, "ink")
                L.px(xx + 7, hy + 1, "oc3")
    if byre:
        bx = (door + 1) * 16 + 2
        if bx + 12 <= w * 16:
            L.rect(bx - 1, top + 6, 13, h * 16 - top - 6, "ink")
            for xx in range(bx, bx + 11):
                for yy in range(top + 7, h * 16 - 1):
                    L.px(xx, yy, "wd1" if (xx + yy // 2) % 3 else "wd0")
    _copy_cells(s, L, fill="oc1")
    return finish(s)


# ==========================================================================
# The sanctuary's monuments
# ==========================================================================

def omphalos(state):
    """The Omphalos on its plinth in its court: the navel stone, an egg of white
    marble in a net of knotted red wool. 'whole', 'burning' (fire running along
    every knot) and 'open' (split like an egg, a stair going down between the
    halves). 2 x 2, all solid; the stair is taken by a script."""
    key = {"whole": "omphalos", "burning": "omphalos_burning", "open": "omphalos_open"}[state]
    s = S(key, f"The Omphalos ({state})", 2, 2, walk=["XX", "XX"], ground=["nn", "nn"])
    B = s.B
    E.paving(B, 0, 0, 32, 32)
    # the plinth
    _stylobate(B, 4, 24, 24, 6)
    if state != "open":
        # an egg of white marble, broader below, lit on the upper left
        for y in range(3, 26):
            for x in range(8, 24):
                v = (y - 3) / 22.0
                half = 7.5 * math.sin(math.pi * min(1.0, v * 0.92 + 0.04)) ** 0.8 * (0.8 + 0.25 * v)
                dx = x + 0.5 - 16
                if abs(dx) > half:
                    continue
                lit = -(dx / max(1, half)) * 0.8 - (0.5 - v)
                c = "w0" if lit > 0.55 else "m1" if lit > -0.1 else "m2" if lit > -0.6 else "m3"
                # the agrenon: a lozenge net of wool, knotted at every crossing
                a, b = (x + y) % 6, (x - y) % 6
                if a == 0 or b == 0:
                    c = ("rd" if state == "whole" else "br") if lit > -0.3 else "br"
                    if a == 0 and b == 0:
                        c = "ink"
                B.px(x, y, c)
        for y in range(3, 26):
            row = [x for x in range(8, 24) if B.get(x, y) in ("m1", "w0", "m2", "m3", "rd", "br", "ink")]
            if row:
                B.px(min(row) - 1, y, "ink")
                B.px(max(row) + 1, y, "ink")
        B.hline(14, 17, 2, "ink")
    else:
        # two halves fallen apart, a dark stairwell between them
        B.rect(12, 6, 8, 20, "ink")
        for i, y in enumerate(range(8, 26, 3)):
            B.hline(13, 18, y, "m4" if i % 2 else "m5")
        B.ellipse(2, 8, 12, 26, "m1")
        B.ellipse(3, 9, 9, 18, "w0")
        B.ellipse(20, 8, 30, 26, "m1")
        B.ellipse(22, 9, 28, 18, "m2")
        for (x0, x1) in ((2, 12), (20, 30)):
            for y in range(8, 27):
                for x in range(x0, x1 + 1):
                    if B.get(x, y) in ("m1", "w0", "m2") and (x + y) % 6 == 0:
                        B.px(x, y, "m4")
        B.vline(12, 8, 26, "ink")
        B.vline(20, 8, 26, "ink")
    if state == "burning":
        for (x, y) in ((10, 8), (15, 4), (21, 9), (12, 16), (19, 18), (9, 22), (22, 23), (16, 12)):
            E.flame(s.T, x - 2, y - 4)
    return finish(s)


def altar_chians():
    """The great altar of the Chians before the temple: a long block of dark
    marble with a white cornice and base, a ramp up its south side."""
    s = S("altar_chians", "The altar of the Chians", 3, 2, walk=["XXX", "XXX"],
          ground=["ggg", "nnn"])
    L = Layer(48, 32)
    L.rect(1, 8, 46, 22, "m5")
    for y in range(10, 28):
        for x in range(2, 46):
            if (x * 3 + y) % 9 == 0:
                L.px(x, y, "b0")
    L.rect(0, 4, 48, 5, "w0")
    L.hline(0, 47, 4, "ink")
    L.hline(0, 47, 8, "m3")
    L.rect(0, 27, 48, 5, "m1")
    L.hline(0, 47, 31, "ink")
    L.vline(0, 4, 31, "ink")
    L.vline(47, 4, 31, "ink")
    # ash and a laurel garland on the top
    for x in range(6, 42, 5):
        L.px(x, 5, "m3")
        L.px(x + 1, 5, "m2")
    _copy_cells(s, L, fill="m4")
    return finish(s)


def statues():
    out = []
    # Kleobis and Biton: two archaic kouroi, fists at their sides, on one base
    s = S("kleobis_biton", "Kleobis and Biton", 2, 2, walk=["XX", "XX"], ground=["gg", "gg"])
    L = Layer(32, 32)
    for x0 in (4, 18):
        L.ellipse(x0 + 1, 1, x0 + 7, 7, "m1")          # head, with braided hair
        L.hline(x0 + 2, x0 + 6, 1, "m3")
        L.rect(x0 + 1, 8, 7, 9, "m1")                  # chest
        L.vline(x0 + 7, 8, 16, "m2")
        L.rect(x0, 9, 1, 8, "m1")
        L.rect(x0 + 8, 9, 1, 8, "m2")                  # arms
        L.rect(x0 + 2, 17, 2, 8, "m1")
        L.rect(x0 + 5, 17, 2, 8, "m2")                 # legs, left foot forward
        L.px(x0 + 4, 4, "m4")
        L.px(x0 + 6, 4, "m4")
    sil = L.a[..., 3] > 0
    pad = np.pad(sil, 1)
    edge = sil & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "ink")
    _stylobate(L, 1, 25, 30, 6)
    for x in range(1, 31):
        L.px(x, 31, "m5")
    s.M.a[:] = L.a
    out.append(finish(s))
    # the Naxian sphinx on her tall Ionic column
    s = S("sphinx_column", "The Naxians' sphinx on her column", 1, 3, walk=["T", "X", "X"],
          ground=["g", "g", "g"], names={"top": (0, 0)})
    L = Layer(16, 48)
    L.blit(["....ww....",
            "...wmmw...",
            "...wmm.ww.",
            "..wmmmmmmw",
            ".wmmmmmmmw",
            "wmmmmmmmmw",
            "wmmmmmmmw.",
            "wwwwwwwww."], {"w": "ink", "m": "m1"}, 3, 2)
    L.px(6, 4, "m4")
    E.ionic_capital(L, 5, 11, 6)
    E.shaft(L, 5, 16, 6, 26)
    _stylobate(L, 2, 42, 12, 6)
    s.T.a[:16] = L.a[:16]
    s.M.a[16:] = L.a[16:]
    out.append(finish(s))
    return out


def rocks():
    out = []
    # the Rock of the Sibyl: a split crag of grey limestone
    s = S("sibyl_rock", "The Rock of the Sibyl", 2, 2, walk=["XX", "XX"], ground=["gg", "gg"])
    L = Layer(32, 32)
    L.poly([(3, 30), (2, 18), (7, 7), (14, 2), (19, 6), (22, 3), (28, 12), (30, 30)], "s3")
    for y in range(32):
        for x in range(32):
            c = L.get(x, y)
            if c is None:
                continue
            lit = (x + y * 0.6) < 22
            if (x * 5 + y * 3) % 13 == 0:
                c = "s1"
            elif lit and (x + y) % 3:
                c = "s4"
            elif not lit and (x + 2 * y) % 4 == 0:
                c = "s2"
            L.px(x, y, c)
    L.line(18, 6, 15, 18, "s0")       # the split
    L.line(15, 18, 17, 28, "s0")
    sil = L.a[..., 3] > 0
    pad = np.pad(sil, 1)
    edge = sil & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "ink")
    for x in range(3, 31):
        L.px(x, 31, "s1")
    s.M.a[:] = L.a
    out.append(finish(s))
    # the oldest altar: a rough block with a hollow worn in its top
    s = S("oldest_altar", "The oldest altar", 1, 1, walk=["X"], ground=["g"])
    L = s.M
    L.rect(2, 5, 12, 10, "s2")
    L.rect(2, 5, 12, 3, "s4")
    L.rect(5, 5, 6, 2, "s0")
    L.px(6, 5, "e1")
    L.px(8, 6, "e1")
    E.outline_rect(L, 2, 4, 12, 11)
    L.hline(3, 13, 15, "s1")
    out.append(finish(s))
    return out


def theatre_kit():
    """The theatre's tiers: limestone benches cut into the slope, each with a lit
    seat and a shadowed riser. A row's west end, middle and east end; a stair
    of narrow treads where an aisle climbs between wedges; and the curve's
    corners, where a row turns up the slope. All walkable."""
    s = S("tiers", "Theatre and stadium tiers", 6, 1, walk=["......"], ground=["gnnngg"],
          names={"W": (0, 0), "M": (1, 0), "M2": (2, 0), "aisle": (3, 0), "E": (4, 0),
                 "curve_E": (5, 0)})
    L = Layer(96, 16)
    for x in range(96):
        for y in range(16):
            t = y % 8
            c = "s5" if t == 0 else "s4" if t < 3 else "s3" if t < 5 else "s1" if t < 7 else "s0"
            if x % 16 == 15 and t >= 3:
                c = "s1"
            L.px(x, y, c)
    for y in range(16):
        for x in range(48, 64):
            L.px(x, y, "s4" if y % 4 == 0 else "s2" if y % 4 < 3 else "s0")
        L.px(48, y, "ink")
        L.px(63, y, "ink")
    # the ends fade into grass
    for y in range(16):
        for x in range(0, 3 + (y % 8 > 4)):
            L.px(x, y, None)
        L.px(3 + (y % 8 > 4), y, "ink")
        for x in range(77 - (y % 8 > 4), 80):
            L.px(x, y, None)
        L.px(76 - (y % 8 > 4), y, "ink")
        for x in range(80, 96):
            if x - 80 > 15 - y:
                L.px(x, y, None)
        L.px(min(95, 80 + 15 - y), y, "ink")
    _copy_cells(s, L, fill="s2")
    return finish(s)


def fountain_house():
    """The Kastalian spring: a fountain house cut back into the rock of the
    cleft, a marble entablature over three bronze lion heads, the water falling
    from their mouths into a long stone basin. 5 x 3, solid."""
    s = S("kastalia", "The Kastalian spring's fountain house", 5, 3,
          walk=["XXXXX", "XXXXX", "XXXXX"], ground=["nnnnn", "nnnnn", "nnnnn"],
          names={"basin": (2, 2)})
    L = Layer(80, 48)
    rock_face(L, 0, 0, 80, 48, seed=1)
    # the cutting: a smoothed back wall of marble ashlar, whole tiles only
    for y in range(8, 32):
        for x in range(8, 72):
            L.px(x, y, "m2" if (x // 8 + y // 6) % 2 else "m3")
            if y % 6 == 5 or (x + (y // 6) * 4) % 8 == 7:
                L.px(x, y, "m4")
    _entablature(L, 8, 8, 64)
    L.vline(8, 8, 31, "ink")
    L.vline(71, 8, 31, "ink")
    # three lion heads and their streams (water tiles)
    W = Layer(80, 48)
    for lx in (16, 36, 56):
        W.ellipse(lx, 17, lx + 8, 24, "br")
        W.ellipse(lx + 1, 18, lx + 6, 22, "g0")
        W.px(lx + 2, 19, "ink")
        W.px(lx + 6, 19, "ink")
        W.rect(lx + 3, 22, 3, 2, "ink")
        for y in range(24, 37):
            W.px(lx + 4, y, "b3" if y % 3 else "w0")
            W.px(lx + 3, y, "b2")
    # the basin: a lip of marble, water inside
    for x in range(0, 80):
        W.px(x, 36, "ink")
        W.px(x, 37, "m2")
        W.px(x, 38, "m3")
        for y in range(39, 46):
            W.px(x, y, ("wr" if (x + y * 2) % 7 == 0 else "b1") if y < 44 else "b0")
        W.px(x, 46, "m3")
        W.px(x, 47, "ink")
    for lx in (16, 36, 56):
        for (dx, dy) in ((1, 39), (5, 39), (3, 40), (7, 40), (0, 41)):
            W.px(lx + dx, dy, "w0")
    # keep each 8x8 in one group: move the water layer onto whole tiles
    for ty in range(6):
        for tx in range(10):
            sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if (W.a[sl][..., 3] > 0).any():
                if ty >= 4:
                    L.a[sl] = W.a[sl]
                    hole = L.a[sl][..., 3] == 0
                    L.a[sl][hole] = list(C["m3"]) + [255]
                else:
                    s.T.a[sl] = W.a[sl]
    _copy_cells(s, L, fill="ph2")
    return finish(s)


def stadium_pieces():
    """The stadium's starting sill (the balbis): a long stone sill with two
    grooves for the runners' toes, set in the sand of the track; and the
    turning post."""
    s = S("balbis", "The stadium's starting sill and turning post", 2, 1, walk=[".X"],
          ground=["nn"], names={"sill": (0, 0), "post": (1, 0)})
    L = s.B
    for x in range(32):
        for y in range(16):
            L.px(x, y, "s4" if (x * 3 + y * 5) % 11 else "s3")
    L.rect(0, 5, 16, 6, "s2")
    L.hline(0, 15, 5, "s5")
    L.hline(0, 15, 7, "s0")
    L.hline(0, 15, 9, "s0")
    L.hline(0, 15, 10, "s1")
    for x in range(3, 16, 4):
        L.px(x, 6, "ink")
    L.rect(22, 1, 5, 13, "s5")
    L.vline(26, 1, 13, "s2")
    E.outline_rect(L, 21, 0, 7, 15)
    L.hline(20, 28, 15, "s1")
    return finish(s)


# ==========================================================================
# The muster, the warden's hut, the road's furniture
# ==========================================================================

def tents():
    out = []
    for key, w, title in (("tent", 3, "A Titan tent of brown hides"), ("tent_small", 2, "A small hide tent")):
        s = S(key, title, w, 2, walk=["X" * w, "X" * w], ground=["g" * w, "g" * w])
        L = Layer(w * 16, 32)
        mid = w * 8
        for y in range(4, 30):
            half = int((y - 4) * (w * 8 - 1) / 26)
            for x in range(mid - half, mid + half + 1):
                c = "hd1" if x < mid else "hd0"
                if (x - mid + 64) % 6 == 0:
                    c = "hd2" if x < mid else "hd1"
                L.px(x, y, c)
            L.px(mid - half, y, "ink")
            L.px(mid + half, y, "ink")
        L.vline(mid, 2, 29, "wd0")
        L.px(mid, 1, "ink")
        # the door flap, tied back
        for y in range(18, 30):
            k = y - 18
            for x in range(mid - k // 3, mid + k // 3 + 1):
                L.px(x, y, "ink")
        L.line(mid - 6, 20, mid - 3, 24, "rp")
        for x in range(1, w * 16 - 1):
            L.px(x, 30, "ink" if L.get(x, 29) else None)
            L.px(x, 31, "hd0" if abs(x - mid) < w * 8 - 1 else None)
        # guy ropes and pegs
        L.line(2, 31, mid - (w * 8 - 3), 27, "rp")
        s.M.a[:] = L.a
        out.append(finish(s))
    s = S("camp_props", "Camp props: cookfire, banner, shovel rack, crates, bread oven, plank bridge", 8, 2,
          walk=["XTXXXX..", "XXXXXX.."], ground=["gggggggg", "gggggggg"],
          names={"fire": (0, 0), "banner_top": (1, 0), "banner": (1, 1), "rack_W": (2, 0),
                 "rack_E": (3, 0), "crate": (0, 1), "crates": (2, 1), "oven_TL": (4, 0),
                 "oven_TR": (5, 0), "oven_BL": (4, 1), "oven_BR": (5, 1),
                 "bridge_EW": (6, 0), "bridge_NS": (7, 0), "trodden": (6, 1), "ash": (7, 1)})
    L = Layer(128, 32)
    # cookfire: a ring of stones, logs and a flame
    for a in range(0, 360, 40):
        x = 8 + int(5 * math.cos(math.radians(a)))
        y = 11 + int(3 * math.sin(math.radians(a)))
        L.rect(x - 1, y - 1, 2, 2, "ir")
    L.line(4, 12, 11, 10, "wd1")
    L.line(4, 10, 11, 12, "wd0")
    E.flame(L, 5, 3)
    # the sickle banner: a pole, a red banner with a gold sickle
    L.vline(23, 2, 30, "wd0")
    L.px(23, 1, "g1")
    L.rect(24, 4, 6, 14, "rd")
    E.outline_rect(L, 24, 4, 6, 14)
    L.blit(["gg..", "..g.", "..g.", ".g..", "g..."], {"g": "g1"}, 25, 7)
    L.hline(20, 22, 31, "hd0")
    L.hline(24, 26, 31, "hd0")
    # a rack of shovels nobody uses
    L.hline(33, 62, 4, "wd1")
    L.hline(33, 62, 12, "wd1")
    for x in (34, 61):
        L.vline(x, 3, 15, "wd0")
    for x in range(37, 60, 4):
        L.vline(x, 2, 11, "wd2")
        L.rect(x - 1, 11, 3, 4, "ir")
    # crates
    for (x, y) in ((2, 20), (34, 18), (42, 20), (38, 24)):
        L.rect(x, y, 9, 8, "wd2")
        E.outline_rect(L, x, y, 9, 8)
        L.line(x + 1, y + 1, x + 7, y + 6, "wd1")
    # the beehive bread oven (clay group cells)
    oven = Layer(32, 32)
    oven.ellipse(3, 5, 28, 30, "tc1")
    oven.ellipse(5, 7, 20, 22, "tc2")
    oven.ellipse(8, 8, 14, 13, "tc3")
    oven.ellipse(11, 18, 20, 30, "ink")
    oven.ellipse(13, 21, 18, 29, "tc0")
    oven.hline(3, 28, 30, "ink")
    sil = oven.a[..., 3] > 0
    pad = np.pad(sil, 1)
    edge = sil & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        oven.px(x, y, "ink")
    L.a[0:32, 64:96] = oven.a
    # plank bridges, laid straight over the stream (drawn ground: timber)
    for x in range(96, 112):
        for y in range(16):
            c = "wd2" if (y % 5) else "wd0"
            if y in (0, 15):
                c = "ink"
            L.px(x, y, c)
    for x in range(112, 128):
        for y in range(16):
            c = "wd2" if (x % 5) else "wd0"
            if x in (112, 127):
                c = "ink"
            L.px(x, y, c)
    # trodden earth and old ash (camp ground, borrowed grass under)
    for (x, y) in ((99, 20), (100, 21), (104, 25), (108, 19), (101, 27), (106, 22)):
        L.px(x, y, "hd1")
        L.px(x + 1, y, "hd2")
    for (x, y) in ((116, 22), (117, 22), (118, 23), (120, 21), (121, 24), (115, 25)):
        L.px(x, y, "ir")
    s.ground[(6, 0)] = "none"
    s.ground[(7, 0)] = "none"
    for cy in range(2):
        for cx in range(8):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            if (cx, cy) == (1, 0):
                s.T.a[sl] = L.a[sl]
            elif (cx, cy) in s.borrowed:
                s.M.a[sl] = L.a[sl]
            else:
                s.B.a[sl] = L.a[sl]
    out.append(finish(s))
    return out


def hut():
    """Hieron's hut: one room of rough stone built against the oldest olive, a
    roof of reeds held down with stones, a low door, the spring's channel
    running out under it. 3 x 2; the door is the bottom middle."""
    s = S("hut", "The warden's hut", 3, 2, walk=["XXX", "XDX"], ground=["ggg", "nnn"],
          names={"door": (1, 1)})
    L = Layer(48, 32)
    # reed thatch
    for y in range(4, 16):
        for x in range(1 + max(0, 6 - y), 47 - max(0, 6 - y)):
            L.px(x, y, "wd3" if (x + y // 2) % 3 else "wd2")
        L.px(1 + max(0, 6 - y), y, "ink")
        L.px(46 - max(0, 6 - y), y, "ink")
    L.hline(5, 42, 3, "ink")
    for x in (10, 24, 38):
        L.ellipse(x - 2, 4, x + 2, 7, "rp")
    L.hline(0, 47, 15, "wd0")
    # stone walls
    stone = Layer(48, 32)
    for y in range(16, 32):
        for x in range(48):
            stone.px(x, y, "s3" if (x // 5 + (y // 4) * 2) % 3 else "s2")
            if y % 4 == 0 or (x + (y // 4) * 3) % 6 == 0:
                stone.px(x, y, "s1")
    stone.rect(19, 20, 10, 12, "ink")
    stone.rect(20, 21, 8, 11, "s0")
    stone.vline(0, 16, 31, "ink")
    stone.vline(47, 16, 31, "ink")
    stone.hline(0, 47, 31, "ink")
    L.a[16:] = stone.a[16:]
    _copy_cells(s, L, fill="s2")
    return finish(s)


def torches():
    """A torch stand on the Sacred Way, cold, and lit (III-8 lights them one by one)."""
    s = S("torch", "A torch stand (cold, lit)", 2, 1, walk=["XX"], ground=["nn"],
          names={"cold": (0, 0), "lit": (1, 0)})
    E.paving(s.B, 0, 0, 32, 16)
    for ox in (0, 16):
        L = s.M
        L.vline(ox + 7, 5, 14, "ir")
        L.vline(ox + 8, 5, 14, "ink")
        L.hline(ox + 5, ox + 10, 15, "ink")
        L.rect(ox + 4, 2, 8, 3, "wd0")
        L.hline(ox + 4, ox + 11, 2, "ink")
    E.flame(s.M, 18, -2)
    return finish(s)


def _sections(groups):
    sections, start = [], 0
    for name, ss in groups:
        for s in ss:
            s.section = name
        end = K.pack([(start, ss)])
        sections.append((start, ss))
        start = end + 1        # a spare row, so a section can grow a little
    return sections


def ground_kit():
    """Ground variety on aethos's grass: a tuft of dry grass, pebbles, fallen
    olive leaves, a mound of thyme, a scatter of stones, a worn earth patch, a
    shadow under a wall. All walkable, all on borrowed grass."""
    s = S("ground", "Ground variants on grass", 7, 1, walk=["......."], ground=["ggggggg"],
          names={"tuft": (0, 0), "pebbles": (1, 0), "leaves": (2, 0), "thyme": (3, 0),
                 "stones": (4, 0), "worn": (5, 0), "shade_N": (6, 0)})
    L = s.M
    for (x, y) in ((4, 9), (5, 8), (6, 9), (5, 10), (7, 10), (9, 6), (10, 5), (11, 6)):
        L.px(x, y, "gr2")
        L.px(x, y + 1, "gsh")
    for (x, y) in ((19, 4), (24, 9), (28, 5), (21, 12), (27, 13)):
        L.px(x, y, "gsh")
        L.px(x + 1, y, "gr2")
        L.px(x, y - 1, "gr0")
    for (x, y) in ((35, 3), (39, 7), (42, 11), (36, 12), (44, 4)):
        L.px(x, y, "ov3")
        L.px(x + 1, y, "ov2")
        L.px(x + 1, y + 1, "ov1")
    L.ellipse(51, 6, 59, 12, "ov1")
    L.ellipse(52, 6, 57, 9, "ov2")
    for (x, y) in ((53, 7), (56, 8), (54, 10)):
        L.px(x, y, "tk1")
    L.hline(51, 59, 13, "gsh")
    for (x, y) in ((67, 5), (72, 9), (76, 4), (69, 12)):
        L.px(x, y, "gsh")
        L.px(x, y - 1, "gr2")
        L.px(x + 1, y - 1, "gr2")
    for y in range(4, 13):
        for x in range(83, 94):
            if ((x - 88) / 5.5) ** 2 + ((y - 8) / 4.2) ** 2 <= 1 and hsh(x, y, 4) % 5:
                L.px(x, y, "tk1" if hsh(x, y, 5) % 3 else "tk0")
    for x in range(96, 112):
        L.px(x, 0, "gsh")
        if hsh(x, 9) % 2:
            L.px(x, 1, "gsh")
    return finish(s)


def bushes():
    """Maquis that fills the gaps in a wood: a mastic bush and a young laurel,
    one cell each, solid."""
    s = S("bush", "Maquis: a mastic bush, a young laurel", 2, 1, walk=["XX"], ground=["gg"],
          names={"mastic": (0, 0), "laurel": (1, 0)})
    for ox, seed, cols in ((0, 3, ("ov0", "ov1", "ov2", "ov3")), (16, 9, ("c1", "c2", "c3", "ov3"))):
        L = Layer(16, 16)
        for x in range(2, 15):
            L.px(x, 15, "gsh")
        _crown(L, 8, 9, 7, 6, seed, dark=cols[0], mid=cols[1], lit=cols[2], hi=cols[3], lobes=5)
        s.M.a[:, ox:ox + 16] = np.maximum(s.M.a[:, ox:ox + 16], L.a) if False else L.a
    return finish(s)


def build():
    """Delphoi itself. Sections: (start row, structures)."""
    land = [cliff_kit(), cliff_scree(), polywall_kit(), way_kit(), ground_kit(), bushes()]
    trees = laurels()
    town = [house("house_a", "Lower-town house (door west)", 4, 1, window=2),
            house("house_b", "Lower-town house (door east)", 4, 2, window=0),
            house("house_melissai", "The House of the Melissai (hive wall)", 5, 3, hives=True),
            house("house_pilgrims", "The Pilgrims' House", 5, 1, window=3),
            house("house_koretas", "Koretas's house and byre", 4, 1, byre=True),
            lesche()]
    sanctuary = [temple_apollo(), treasury("treasury_astyra", "The treasury of Astyra"),
                 treasury("treasury_siphnos", "The treasury of the Siphnians", caryatids=True),
                 altar_chians(), omphalos("whole"), omphalos("burning"), omphalos("open")]
    sanctuary += statues() + rocks() + [theatre_kit(), fountain_house(), stadium_pieces(), torches()]
    return _sections([("land", land), ("trees", trees), ("town", town), ("sanctuary", sanctuary)])


def build_parnassos():
    """Route 28: the Sacred Olives and the Kastalian Gorge."""
    land = [cliff_kit(), cliff_scree(), pezoula_kit(), ground_kit(), bushes()] + rocks()
    trees = laurels() + [oldest_olive()]
    camp = tents() + [hut()]
    return _sections([("land", land), ("trees", trees), ("camp", camp)])


def write_catalog(used, structs, name=NAME, maps="Delphoi"):
    import json
    lines = [f"# {name} tileset catalog", "",
             f"`gTileset_{name.capitalize()}` is {maps}, on the `aethos` primary. **Generated** by "
             f"`tools/ichor/art/delphoi_build.py {name}`; the art is `tools/ichor/art/delphoi_art.py`.", "",
             f"Built: **{used}** tiles of 504.", "",
             f"![pieces](img/{name}_pieces.png)", "",
             "Map builders place pieces by key and name (`tools/ichor/maps/delphoi_maps.py`, "
             "`build/delphoi/catalog.json`), never by raw id.", "",
             "| Key | Size | Section | What it is | Names |", "|---|---|---|---|---|"]
    for s in structs:
        names = ", ".join(f"`{n}`" for n in getattr(s, "names", {}))
        lines.append(f"| `{s.key}` | {s.w}x{s.h} | {s.section} | {s.title} | {names} |")
    cat = {"symbol": "gTileset_" + "".join(w.capitalize() for w in name.split("_")),
           "fronts": {}, "structures": {}}
    for s in structs:
        cat["structures"][s.key] = {
            "w": s.w, "h": s.h, "ids": s.ids, "walk": s.walk, "section": s.section,
            "names": {n: list(c) for n, c in getattr(s, "names", {}).items()},
            "ground": {f"{x},{y}": g for (x, y), g in sorted(s.ground.items())}}
    out = K.ROOT / f"tools/ichor/maps/catalogs/{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cat, indent=1, sort_keys=True) + "\n")
    path = K.ROOT / f"design/phase4/TILES_{name}.md"
    path.write_text("\n".join(lines) + "\n")
    _ = json
