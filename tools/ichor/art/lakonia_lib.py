"""Shared toolkit for Act III's Lakonia secondaries (gytheion, eurotas,
lakonia, stymphalia).

Lakonia is spare and sun-hard: plain flat-roofed houses of plastered mudbrick
on stone footings, beaten sand, red-brown cloaks and bronze shields, plane
trees and Eurotas reeds, and the dark wall of Taygetos behind everything. Its
pieces are split by map (as the Kythera family is) and drawn with
kythera_lib's layers, structures, borrowed aethos ground and animations. This
module adds:

  - The palette plan. One family color table and nine named color groups;
    each tileset takes seven of them for its secondary palettes 6-12, and every
    8x8 tile (over all its animation frames) draws from one group.
  - Fresh water of its own. The Eurotas's green water and Stymphalia's black
    water are periodic, animated bottom-layer textures (water()); banks, reeds,
    boardwalks and bridges are drawn on the middle layer over them, so every
    water cell shares the same few animated tiles.
  - Quadrant autotiles (autotile()). A soft-edged region (a river, a reed bed,
    the agoge's sand yard) is drawn as all 47 blob shapes, but each 8x8
    quadrant depends only on its own two sides and corner, so the whole set
    costs about 20 tiles. Map builders pick a cell with kythera_lib.blob_key.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_lib as K  # noqa: E402
from kythera_lib import (Layer, anim_layer, ground, pick, put, settle,  # noqa: E402,F401
                         struct)

A = K.A
ROOT = K.ROOT
C = K.C

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # Lakonian red, from a cloak's fold to its sunlit wool
    "lr0": (64, 24, 24), "lr1": (120, 32, 32), "lr2": (168, 56, 40), "lr3": (208, 96, 64),
    # Lakonian stone: gray limestone, from the shadow to the sun-bleached top
    "sn0": (56, 48, 48), "sn1": (96, 88, 80), "sn2": (144, 136, 120), "sn3": (184, 176, 152),
    "sn4": (216, 208, 184),
    # lime plaster over mudbrick; flat roofs of beaten clay
    "pw1": (200, 184, 152), "pw2": (232, 224, 200), "ro1": (120, 96, 72), "ro2": (160, 128, 96),
    # holm-oak's dark gloss, hyacinth
    "ho1": (40, 72, 56), "ho2": (64, 104, 80), "hy1": (88, 56, 128), "hy2": (144, 112, 192),
    "kt3": (200, 192, 176),
    # the Eurotas's green water
    "ew0": (32, 64, 64), "ew1": (48, 96, 88), "ew2": (72, 128, 112), "ew3": (112, 168, 144),
    "ew4": (176, 216, 192),
    # reeds, from the wet stem to the dry plume
    "re1": (88, 96, 40), "re2": (136, 136, 64), "re3": (184, 176, 96), "re4": (224, 208, 144),
    # Taygetos: the dark wall, blue-violet rock to pale scree
    "ty0": (24, 24, 40), "ty1": (48, 48, 72), "ty2": (80, 80, 104), "ty3": (120, 120, 136),
    "ty4": (168, 168, 176), "ty5": (208, 208, 208),
    # murex purple, from the vat's dregs to a stained pink
    "pu0": (48, 24, 48), "pu1": (88, 40, 80), "pu2": (136, 64, 120), "pu3": (184, 104, 160),
    "pu4": (224, 168, 200),
    # Stymphalia's black water and its mud
    "bw0": (16, 24, 24), "bw1": (32, 40, 40), "bw2": (48, 64, 56), "bw3": (80, 96, 80),
    "md1": (72, 56, 40),
    # beaten sand of the agoge's yard and the wrestling sands
    "ya0": (160, 128, 88), "ya1": (192, 160, 112), "ya2": (216, 192, 144), "ya3": (240, 224, 184),
    # Route 24's drowned town seen through clear water
    "dt1": (40, 112, 144), "dt2": (64, 144, 168), "dt3": (120, 192, 208),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in C or C[_n] == _c, f"color name clash: {_n}"
    C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)

# --------------------------------------------------------------------------
# Color groups: each tileset takes seven (FAMILY[name]["groups"] in the build)
# --------------------------------------------------------------------------

GROUPS = {
    # Lakonian red and bronze: cloaks, shields, doors, awnings, the bronze gods
    "red": ["lr0", "lr1", "lr2", "lr3", "bz0", "bz1", "bz2", "bz3", "vg1", "sn1", "sn2",
            "sn3", "ink", "w0", "gd"],
    # plain stone, plaster and clay roofs: houses, the stoa, stelai, the ring wall
    "stone": ["sn0", "sn1", "sn2", "sn3", "sn4", "g2", "pw1", "pw2", "ro1", "ro2", "ink",
              "lr1", "lr2", "g1", "gd"],
    # plane, holm-oak, oak, walnut, willow; bark; hyacinths
    "veg": ["g1", "g2", "g3", "gd", "t0", "my1", "my2", "my3", "my4", "kt1", "kt2", "w0",
            "ho1", "ho2", "kt3"],
    # the Eurotas: its green water, banks of mud, reeds and pink oleander
    "river": ["ew0", "ew1", "ew2", "ew3", "ew4", "re1", "re2", "re3", "re4", "op1", "op2",
              "g1", "g2", "g3", "gd"],
    # Taygetos and the Skiritis: dark rock, scree, black pine; foam at a sea cliff's foot
    "mount": ["ty0", "ty1", "ty2", "ty3", "ty4", "ty5", "c1", "c2", "c3", "g1", "g2", "g3", "gd",
              "w0", "b4"],
    # Gytheion's purple: stains, murex shells, lead vats, on the quay's limestone
    "purple": ["pu0", "pu1", "pu2", "pu3", "pu4", "kr0", "kr1", "kr2", "kr3", "w0", "p1",
               "p2", "p3", "ink", "ks2"],
    # Stymphalia: black water, its reeds, mud, bronze feathers
    "marsh": ["bw0", "bw1", "bw2", "bw3", "md1", "re1", "re2", "re3", "re4", "bz2", "bz3",
              "g1", "g2", "g3", "gd"],
    # Route 25's flowers with the trees: hyacinths, oleander
    "vegb": ["g1", "g2", "g3", "gd", "t0", "my1", "my2", "my3", "my4", "kt1", "kt2", "w0",
             "hy1", "hy2", "op2"],
    # timber and thatch: boardwalks, the stilt hut, piles, racks, the barracks' beams
    "wood": ["wd0", "wd1", "wd2", "wd3", "tc1", "tc2", "ink", "w0", "re2", "re3", "re4",
             "sn1", "sn2", "bw0", "lr1"],
    # beaten sand: the agoge's yard, the ring, the wrestling sands, and their stone
    "yard": ["ya0", "ya1", "ya2", "ya3", "sn0", "sn1", "sn2", "sn3", "sn4", "w0", "g1", "g2",
             "gd", "lr1", "ink"],
    # Kythera's groups, for the surf and the boats Gytheion shares with Skandeia
    "foam": list(K.GROUPS["foam"]),
    "terra": list(K.GROUPS["terra"]),
    # Route 24's drowned town under the turquoise shallows
    "deep": ["kq1", "kq2", "b4", "w0", "dt1", "dt2", "dt3", "b1", "b2", "b3", "p3", "kr2",
             "kr3", "ks2", "ks1"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
    for _n in _names:
        assert _n in C, _n


def groups(names):
    return {g: GROUPS[g] for g in names}


def group_rgb(gr):
    return {g: {C[n] for n in names} for g, names in gr.items()}


# aethos ground a cell can borrow; kythera_lib's, plus tall grass and shade
K.GROUND_METATILE.setdefault("tall", 0x00D)
K.GROUND_METATILE.setdefault("shade", 0x01C)

# --------------------------------------------------------------------------
# Ground textures, phase-locked to the 16 px grid
# --------------------------------------------------------------------------


def _aethos_px(mid, X, Y):
    rgb = tuple(int(v) for v in K.aethos(mid)[Y % 16, X % 16])
    return A.RGB2NAME[rgb]


def grass_px(X, Y):
    return _aethos_px(0x001, X, Y)


def path_px(X, Y):
    return _aethos_px(0x1D9, X, Y)


def sand_px(X, Y):
    return _aethos_px(0x124, X, Y)


h, hp = K.h, K.hp


def mx(X):
    """X's distance from its cell's nearer side edge (0..7): textures drawn on
    mx() are mirror-symmetric in each cell, so Porytiles stores a piece and
    its mirror image once."""
    x = X % 16
    return min(x, 15 - x)


def yard_px(X, Y):
    """Beaten sand: packed and trodden, a little grit, no ripples (each cell
    mirror-symmetric)."""
    x, y = mx(X), Y % 16
    k = hp(x, y, 21)
    if k % 23 == 0:
        return "ya0"
    if k % 11 == 0 or (x * 3 + y * 5) % 13 == 0:
        return "ya2"
    return "ya1"


def soft_sand_px(X, Y):
    """The wrestling sands: dug soft and pale, raked in long furrows (each
    cell mirror-symmetric)."""
    x, y = mx(X), Y % 16
    k = hp(x, y, 33)
    if y % 5 == 0 and (x + y) % 7 < 5:
        return "ya2"
    if k % 19 == 0:
        return "ya1"
    return "ya3" if k % 7 == 0 else "ya2"


# --------------------------------------------------------------------------
# Animated fresh water
# --------------------------------------------------------------------------

def _eurotas(x, y, f):
    """The Eurotas: green, slow, a little silt; long ripple dashes that drift
    east a pixel or two each frame, and a few glints."""
    k = K.h(x, y, 5)
    c = "ew1"
    if (x + 2 * y) % 7 == 0 or k % 13 == 0:
        c = "ew0"
    # ripple dashes, 16 px periodic, drifting with the frame
    for (dx, dy, ln) in ((1, 2, 4), (9, 5, 3), (4, 9, 5), (12, 12, 3), (6, 14, 2)):
        xx = (x - dx - 2 * f) % 16
        if y == dy and xx < ln:
            c = "ew2" if xx not in (0, ln - 1) else "ew2"
            if xx == ln // 2 and f == 1:
                c = "ew3"
    if y in (2, 9) and (x - 2 * f) % 16 in (7,):
        c = "ew3"
    if (x, y) == ((13 + f * 5) % 16, 7) or (x, y) == ((3 + f * 3) % 16, 12):
        c = "ew4"
    return c


def _marsh(x, y, f):
    """Stymphalia's black water: nearly still; faint rings and a slow sheen."""
    k = K.h(x, y, 9)
    c = "bw1"
    if k % 9 == 0 or (x * 5 + y * 3) % 11 == 0:
        c = "bw0"
    for (cx, cy, r) in ((4, 4, 2.5), (12, 11, 3.0)):
        d = math.hypot(x - cx, (y - cy) * 1.6)
        rr = r + f * 0.9
        if abs(d - rr) < 0.5 and (x + y + f) % 2 == 0:
            c = "bw2"
    if y in (7, 15) and (x + 3 * f) % 16 in (2, 3, 4):
        c = "bw2"
    if f == 1 and (x, y) in ((10, 2), (2, 13)):
        c = "bw3"
    return c


WATERS = {"eurotas": (_eurotas, 3), "marsh": (_marsh, 3)}


def water_px(kind, X, Y, f=0):
    fn, _ = WATERS[kind]
    return fn(X % 16, Y % 16, f)


def water(s, kind, cells=None, behavior="MB_POND_WATER", walk="P"):
    """Fill the bottom layer of `cells` (default: every cell) with animated
    water. Call it after the rest of the bottom layer is drawn: it starts the
    animation (named after the water) from the bottom layer as it stands.
    Cells keep their walk codes unless `walk` is given for them."""
    fn, n = WATERS[kind]
    cells = cells if cells is not None else [(x, y) for y in range(s.h) for x in range(s.w)]
    cells = list(cells)
    B = s.B
    for (cx, cy) in cells:
        for y in range(16):
            for x in range(16):
                B.px(cx * 16 + x, cy * 16 + y, fn(x, y, 0))
    frames = anim_layer(s, kind, n, layer="bottom")
    for fi, F in enumerate(frames, start=1):
        for (cx, cy) in cells:
            for y in range(16):
                for x in range(16):
                    F.px(cx * 16 + x, cy * 16 + y, fn(x, y, fi))
    if walk or behavior:
        rows = [list(r) for r in s.walk]
        for (cx, cy) in cells:
            if walk and rows[cy][cx] in ".XP":
                if rows[cy][cx] != "X":
                    rows[cy][cx] = walk
            if behavior and rows[cy][cx] == walk:
                s.behaviors[(cx, cy)] = behavior
        s.walk = ["".join(r) for r in rows]
    s.water = set(getattr(s, "water", set())) | set(cells)
    return frames


# --------------------------------------------------------------------------
# Quadrant autotiles
# --------------------------------------------------------------------------

DIR8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
QUAD = {"NW": ("N", "W", "NW", 0, 0), "NE": ("N", "E", "NE", 8, 0),
        "SW": ("S", "W", "SW", 0, 8), "SE": ("S", "E", "SE", 8, 8)}


def blob_keys():
    from agros_ground import blob_keys as bk
    return bk()


def quad_state(key, q):
    bits = dict(zip(DIR8, key.split("|")[1]))
    v, hz, d, _, _ = QUAD[q]
    vin, hin, din = bits[v] == "1", bits[hz] == "1", bits[d] == "1"
    if vin and hin:
        return "full" if din else "inner"
    if vin:
        return "side"      # the region runs on north-south; its edge faces east or west
    if hin:
        return "top"       # the region runs on east-west; its edge faces north or south
    return "outer"


def _wob(t, seed, amp):
    """A small wobble along an edge, 0 at the cell's sides and middle, and
    mirror-symmetric in the cell."""
    u = min(t % 16, 15 - t % 16)
    return amp * math.sin(math.pi * u / 7.5 + seed) * math.sin(math.pi * u / 7.5)


def quad_depth(q, state, x, y, e=4.0, r=3.5, seed=0.0, amp=0.9):
    """Signed depth of pixel (x, y) of a cell (0..15) into the region, for the
    quadrant q in `state`: > 0 inside the region, < 0 outside. The region's
    edge sits `e` px in from the cell's outer side."""
    _, _, _, ox, oy = QUAD[q]
    lx = x - ox if q in ("NW", "SW") else 7 - (x - ox)       # 0 at the outer side
    ly = y - oy if q in ("NW", "NE") else 7 - (y - oy)
    if state == "full":
        return 99.0
    ex = e + _wob(y, seed + 1.3, amp)          # a west/east edge wobbles along y
    ey = e + _wob(x, seed, amp)                # a north/south edge along x
    dx, dy = lx - ex, ly - ey
    if state == "top":
        return dy
    if state == "side":
        return dx
    if state == "outer":
        if dx < r and dy < r:
            return r - math.hypot(r - dx, r - dy)
        return min(dx, dy)
    # inner: the region everywhere but a notch of outside at the outer corner,
    # its point rounded off
    if dx >= 0 or dy >= 0:
        return max(dx, dy)
    rn = 2.5
    if dx > -rn and dy > -rn:
        return math.hypot(dx + rn, dy + rn) - rn
    return max(dx, dy)


def autotile(key, title, section, paint, walk_code=".", notes="", e=4.0, r=3.5, seed=0.0,
             amp=0.9, w=8, extra=()):
    """All 47 blob shapes of a soft-edged region. paint(L_middle, s, X, Y, d)
    paints absolute pixel (X, Y) of the struct given its depth d into the
    region (d > 0 inside). `extra` names more cells (variants) appended after
    the 47: [(name, key, painter)], painter(s, ox, oy) drawing over the base
    shape `key` at the cell's origin."""
    keys = blob_keys()
    names_ = list(keys) + [n for n, _, _ in extra]
    hh = (len(names_) + w - 1) // w
    names = {k: (i % w, i // w) for i, k in enumerate(names_)}
    s = struct(key, title, w, hh, section, walk=[walk_code * w] * hh, names=names, notes=notes)
    s.autotile = True
    shapes = list(keys) + [k for _, k, _ in extra]
    while len(shapes) < w * hh:
        shapes.append(keys[-1])
    for i, k in enumerate(shapes):
        ox, oy = (i % w) * 16, (i // w) * 16
        for q in QUAD:
            st = quad_state(k, q)
            _, _, _, qx, qy = QUAD[q]
            for y in range(qy, qy + 8):
                for x in range(qx, qx + 8):
                    d = quad_depth(q, st, x, y, e=e, r=r, seed=seed, amp=amp)
                    paint(s, ox + x, oy + y, d)
    for i, (n, k, fn) in enumerate(extra):
        j = len(keys) + i
        fn(s, (j % w) * 16, (j // w) * 16)
    return s


def blob_key(region, x, y):
    return K.blob_key(region, x, y)


# --------------------------------------------------------------------------
# Small drawing helpers
# --------------------------------------------------------------------------

def shadow(L, x0, y0, w, h_, fn=None, dark="gd", light="g1"):
    """Darken the grass under something: dither gd/g1 on empty pixels of L
    inside the box where fn(x, y) is true."""
    for y in range(y0, y0 + h_):
        for x in range(x0, x0 + w):
            if L.get(x, y) is None and (fn is None or fn(x, y)):
                L.px(x, y, dark if (x + y) % 2 == 0 else light)


def ellipse_mask(w, h_, cx, cy, rx, ry, bump=0.0, lobes=7, phase=0.0):
    m = np.zeros((h_, w), bool)
    for y in range(h_):
        for x in range(w):
            a = math.atan2(y - cy, x - cx)
            if math.hypot((x - cx) / rx, (y - cy) / ry) < 1 + bump * math.sin(a * lobes + phase):
                m[y, x] = True
    return m


def stone_course_px(X, Y, top, ramp=("sn4", "sn3", "sn2", "sn1"), course=4, brick=10):
    """Ashlar courses below a coping at row `top`: joints darker, a lit top."""
    y = Y - top
    if y < 0:
        return None
    row = y // course
    if y % course == course - 1:
        return ramp[3]
    if (X + (brick // 2) * (row % 2)) % brick == 0:
        return ramp[3]
    if y % course == 0:
        return ramp[0]
    return ramp[1] if (X * 7 + Y * 3) % 9 else ramp[2]


def flame(L, x, y, f=0):
    """A small fire 5 px wide, 6 tall, at (x, y) top-left; f is the frame."""
    shapes = [
        ["..a..", ".aba.", ".bcb.", "abcba", "bcccb", ".bbb."],
        [".a...", "..ab.", ".bcb.", "abcb.", "bcccb", ".bbb."],
        ["...a.", ".ba..", ".bcb.", ".bcba", "bcccb", ".bbb."],
    ]
    put(L, x, y, shapes[f % 3], {"a": "bz3", "b": "lr3", "c": "w0"})
