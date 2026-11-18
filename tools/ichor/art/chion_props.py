"""gTileset_Chion's kit (cave_dark's, recolored) and its props.

kit_structs()    every cave_dark kit cell in ice and snow: the ice walls, the
                 snow floor, the slick ice (lit floor, MB_ICE) and the tarn.
style_structs()  the "glacier" wall style (snow on top of the ice) and the
                 "cloud" style (the tarn's shapes as the cloud sea below the
                 mountain, solid).
props()          crystals, snow pines, ice rocks, the frozen giant, the frozen
                 fall, Crook handholds, the seals' bronze plates and grates,
                 shrines, braziers, tripods, the herm, ladders, cave mouths,
                 snow paving and the propylaia of the Pantheon.

Objects stand on the floor: the floor stays in the bottom layer, the object
is drawn in the middle (or top, when the player walks behind it) layer, so
the floor's tiles are shared and an object's tiles use only its own group.
"""
from __future__ import annotations

import math

import numpy as np

import cave_dark_kit as kit
import cave_dark_lib as cdl
import chion_lib as lib
from chion_lib import Layer, Struct, h, one

# --------------------------------------------------------------------------
# The kit, recolored
# --------------------------------------------------------------------------


def recolor(arr, table):
    """cave_dark RGBA -> Chion RGBA through a name table."""
    out = arr.copy()
    m = arr[..., 3] > 0
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        name = cdl.RGB2NAME[tuple(int(v) for v in arr[y, x, :3])]
        out[y, x, :3] = lib.C[table[name]]
    return out


def family_map(key):
    fam = key.split("|")[0]
    return {"T": lib.ROCK_MAP, "ft": lib.ROCK_MAP, "fb": lib.ROCK_MAP, "floor": lib.FLOOR_MAP,
            "lit": lib.FLOOR_MAP, "water": lib.WATER_MAP}[fam]


_KIT = None


def kit_cells():
    global _KIT
    if _KIT is None:
        _KIT = kit.kit_cells()
    return _KIT


def kit_structs():
    out = []
    order = {"T": 0, "ft": 1, "fb": 2, "floor": 3, "lit": 4, "water": 5}
    cells = kit_cells()
    for key in sorted(cells, key=lambda k: (order[k.split("|")[0]], k)):
        layers, walk, mb = cells[key]
        b = recolor(layers["bottom"], family_map(key))
        if key.startswith("lit"):
            mb = "MB_ICE"
        s = one(key, key, "kit", {"bottom": b}, walk=walk, floor_mb=mb if walk == "." else None)
        out.append(s)
    return out


def style_structs():
    """glacier: the rock's top surface under snow (faces stay ice).
    cloud: the tarn's region shapes as the cloud sea, solid."""
    out = []
    cells = kit_cells()
    for key in sorted(cells):
        layers, walk, mb = cells[key]
        if key.startswith("T|"):
            out.append(one(f"glacier:{key}", key, "styles",
                           {"bottom": recolor(layers["bottom"], SNOWTOP)}, walk="X"))
    return out


# the snow-topped mass: k1 (the dark top) becomes sunlit snow
SNOWTOP = {"k0": "i2", "k1": "t1", "k2": "t2", "k3": "t3", "k4": "t4", "k5": "t5", "k6": "t6", "k7": "t7"}
# the tarn's water becomes cloud; its snowy banks stay snow
CLOUD = {"w0": "cl0", "w1": "cl2", "w2": "cl1", "w3": "cl2", "w4": "cl3", "w5": "cl3",
         "f1": "s1", "f2": "s2", "f3": "s3", "f4": "s4", "k0": "i4"}


def floor_base(variant=0):
    """The snow floor's open cell (16x16 RGBA), for props to stand on."""
    cells = kit_cells()
    key = "floor|..|v2" if variant else "floor|.."
    return recolor(cells[key][0]["bottom"], lib.FLOOR_MAP)


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------

def ice_base():
    """The slick ice's open cell (16x16 RGBA), for stoppers standing in it."""
    return recolor(kit_cells()["lit|...."][0]["bottom"], lib.FLOOR_MAP)


def prop(key, title, w, h_, walk, draw, layer="M", notes="", names=None, behaviors=None, floor=True,
         bottom_fill=None, on_ice=False):
    s = Struct(key, title, w, h_, "props", walk=walk, notes=notes, names=names)
    if floor:
        for cy in range(h_):
            for cx in range(w):
                s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = (
                    ice_base() if on_ice else floor_base(h(key, cx, cy) % 4 == 0))
    if bottom_fill:
        bottom_fill(s)
    draw(s)
    for (x, y), mb in (behaviors or {}).items():
        s.behaviors[(x, y)] = mb
    return s


def shade_poly(L, pts, base, light, dark, lx=-1.0, ly=-1.0):
    """A faceted polygon: fill base, then light the edges facing the upper left."""
    L.poly(pts, base)
    n = len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        nx, ny = (y1 - y0), -(x1 - x0)
        ln = math.hypot(nx, ny) or 1
        d = (nx * lx + ny * ly) / ln
        L.line(int(x0), int(y0), int(x1), int(y1), light if d > 0.2 else dark if d < -0.2 else base)


# --------------------------------------------------------------------------
# Crystals
# --------------------------------------------------------------------------

def shard(L, x, y, w, hgt, lean=0, pal=("c1", "c2", "c3", "c4", "c0")):
    """One prism: a pointed shard rising from (x, y) (its base center)."""
    dk, mid, lt, hi, ink = pal
    top = (x + lean, y - hgt)
    pts = [(x - w, y), (x - w, y - hgt + w + 1), top, (x + w, y - hgt + w + 1), (x + w, y)]
    L.poly(pts, mid)
    # the lit face (left) and the shade face (right)
    for yy in range(y - hgt + w + 1, y + 1):
        L.px(x - w + 1, yy, lt)
        L.px(x + w - 1, yy, dk)
        L.px(x, yy, lt if (yy % 3) else hi)
    L.line(x - w, y - hgt + w + 1, top[0], top[1], hi)
    L.line(top[0], top[1], x + w, y - hgt + w + 1, dk)
    L.line(x - w, y, x - w, y - hgt + w + 1, ink)
    L.line(x + w, y, x + w, y - hgt + w + 1, ink)
    L.px(top[0], top[1], hi)


VIOLET = ("c1", "c2", "c3", "c4", "c0")
CYAN = ("cy1", "cy2", "cy3", "cyw", "c0")


def crystal_s(s):
    L = s.M
    shard(L, 6, 14, 2, 9, -1, VIOLET)
    shard(L, 10, 15, 2, 12, 1, CYAN)
    shard(L, 4, 15, 1, 5, -1, CYAN)
    shard(L, 13, 15, 1, 6, 1, VIOLET)
    L.px(10, 4, "cyw")


def crystal_l(s):
    L = s.M
    shard(L, 9, 30, 3, 14, -2, VIOLET)
    shard(L, 16, 31, 4, 26, 0, CYAN)
    shard(L, 23, 30, 3, 18, 2, VIOLET)
    shard(L, 5, 31, 2, 8, -2, CYAN)
    shard(L, 27, 31, 2, 9, 2, CYAN)
    shard(L, 12, 31, 2, 10, -1, ("c1", "mg", "c4", "cyw", "c0"))
    shard(L, 20, 31, 2, 11, 1, ("c1", "c2", "c3", "c4", "c0"))
    for x, y in ((16, 6), (8, 17), (24, 13)):
        L.px(x, y, "cyw")
        L.px(x - 1, y, "cy3")
        L.px(x + 1, y, "cy3")
        L.px(x, y - 1, "cy3")
        L.px(x, y + 1, "cy3")


def crystal_tall(s):
    L = s.M
    shard(L, 8, 31, 3, 28, 0, CYAN)
    shard(L, 4, 31, 2, 9, -1, VIOLET)
    shard(L, 12, 31, 2, 12, 1, VIOLET)


# --------------------------------------------------------------------------
# Ice rocks, boulders, the frozen giant, the frozen fall
# --------------------------------------------------------------------------

def ice_lump(L, cx, cy, rx, ry, cap=True):
    L.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, "i3")
    L.ellipse(cx - rx + 1, cy - ry + 1, cx + rx - 2, cy + ry - 2, "i4")
    L.ellipse(cx - rx + 2, cy - ry + 1, cx + rx - 4, cy, "i5")
    L.ellipse(cx - rx + 3, cy - ry + 2, cx - 1, cy - ry + 3, "i6")
    if cap:
        L.ellipse(cx - rx + 1, cy - ry - 1, cx + rx - 1, cy - ry + 2, "ws")
        L.hline(cx - rx + 2, cx + rx - 2, cy - ry - 1, "i8")
    # outline
    for yy in range(cy - ry - 2, cy + ry + 1):
        for xx in range(cx - rx - 1, cx + rx + 2):
            if L.get(xx, yy) is None and any(L.get(xx + dx, yy + dy) not in (None, "i2")
                                              for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                L.px(xx, yy, "i2")
    L.hline(cx - rx + 1, cx + rx - 1, cy + ry, "i1")


def ice_rock(s):
    ice_lump(s.M, 8, 10, 6, 4)


def ice_boulders(s):
    L = s.M
    ice_lump(L, 11, 20, 9, 7)
    ice_lump(L, 22, 23, 7, 5)
    ice_lump(L, 7, 26, 5, 3)


def frozen_giant(s):
    """A giant of the Gigantomachy, frozen upright in the glacier: a block of
    old blue ice with a dark shape inside and a bronze spear-butt in the snow."""
    L = s.M
    W, H = 48, 48
    # the block
    L.poly([(3, 47), (2, 12), (8, 3), (20, 0), (34, 1), (44, 8), (46, 20), (45, 47)], "i4")
    L.poly([(6, 46), (5, 14), (10, 6), (20, 3), (33, 4), (41, 10), (43, 21), (42, 46)], "i5")
    # the figure inside: a giant's head, shoulders and raised arm, blurred by the ice
    L.ellipse(19, 8, 29, 18, "i3")
    L.poly([(10, 46), (11, 24), (16, 19), (32, 19), (37, 24), (38, 46)], "i3")
    L.poly([(32, 21), (37, 9), (40, 10), (36, 25)], "i3")
    L.ellipse(21, 10, 27, 16, "i2")
    L.poly([(14, 46), (14, 26), (18, 22), (30, 22), (34, 26), (34, 46)], "i2")
    L.px(22, 12, "i1")
    L.px(26, 12, "i1")
    # cracks and the facets' light
    L.line(8, 30, 14, 36, "i6")
    L.line(36, 14, 41, 28, "i6")
    L.line(6, 15, 9, 7, "i7")
    L.line(9, 7, 20, 2, "i7")
    L.line(20, 2, 33, 3, "i8")
    for x, y in ((12, 9), (30, 30), (40, 40), (8, 40)):
        L.px(x, y, "fr2")
    # snow drifted on the top and against the foot
    L.poly([(4, 13), (9, 4), (20, 1), (34, 2), (43, 9), (40, 11), (30, 6), (18, 5), (8, 10)], "ws")
    L.hline(10, 32, 2, "i8")
    L.poly([(2, 47), (3, 41), (10, 43), (18, 41), (26, 44), (36, 41), (45, 43), (46, 47)], "ws")
    L.hline(4, 44, 47, "s3")
    # outline
    L.line(2, 12, 2, 46, "i2")
    L.line(46, 20, 46, 46, "i2")


def frozen_fall(s):
    """A waterfall frozen in mid-pour down a face: columns of icicles."""
    L = s.M
    L.rect(2, 0, 28, 46, "i5")
    for i, x in enumerate(range(3, 29, 4)):
        top = 0
        bot = 40 + (h("fall", x) % 6)
        L.rect(x, top, 3, bot, "i6" if i % 2 else "i7")
        L.vline(x, top, bot, "i8")
        L.vline(x + 2, top, bot, "i4")
        L.px(x + 1, bot + 1, "i6")
    for y in range(4, 44, 7):
        L.hline(3, 28, y, "i6")
    L.vline(2, 0, 47, "i3")
    L.vline(30, 0, 47, "i3")
    # the pool frozen solid at the foot
    L.ellipse(0, 40, 31, 47, "i7")
    L.ellipse(3, 41, 28, 46, "i8")
    L.hline(4, 27, 47, "i4")


# --------------------------------------------------------------------------
# Snow pines
# --------------------------------------------------------------------------

def fir(L, cx, top, tiers, half, trunk_y):
    """A snow-laden fir: stacked tiers, each a dark skirt under a snow ledge."""
    L.rect(cx - 1, trunk_y - 13, 3, 14, "br")
    L.vline(cx + 1, trunk_y - 13, trunk_y, "g0")
    y = top
    for i in range(tiers):
        hw = 2 + (half - 2) * (i + 1) // tiers
        th = 6
        L.poly([(cx, y), (cx - hw, y + th), (cx + hw, y + th)], "g1")
        L.poly([(cx, y + 1), (cx - hw + 2, y + th), (cx, y + th - 1)], "g2")
        L.line(cx - hw, y + th, cx + hw, y + th, "g0")
        # snow on the tier
        L.line(cx - hw + 1, y + th - 1, cx + hw - 3, y + th - 2, "cyw")
        L.line(cx - 1, y + 1, cx - hw + 2, y + th - 2, "cyw")
        y += th - 2
    L.px(cx, top - 1, "cyw")


def pine_snow(s):
    fir(s.T, 16, 2, 7, 15, 47)
    # the trunk's foot and the snow round it belong to the solid bottom row
    for yy in range(32, 48):
        for xx in range(32):
            if s.T.get(xx, yy) is not None:
                s.M.px(xx, yy, s.T.get(xx, yy))
                s.T.px(xx, yy, None)


def pine_snow_s(s):
    fir(s.T, 8, 2, 5, 7, 31)
    for yy in range(16, 32):
        for xx in range(16):
            if s.T.get(xx, yy) is not None:
                s.M.px(xx, yy, s.T.get(xx, yy))
                s.T.px(xx, yy, None)


# --------------------------------------------------------------------------
# The ice faces: Crook handholds
# --------------------------------------------------------------------------

def handholds(s):
    """Pan's Crook's face (WORLD_EXPLORATION §2): paired handholds cut up the
    ice, a rope's frayed end at the top. Drawn over the ice face cells."""
    L = s.M
    for cy in range(2):
        for y in range(cy * 16 + 3, cy * 16 + 16, 6):
            for x in (4, 10):
                xx = x + (2 if (y // 6) % 2 else 0)
                L.rect(xx, y, 3, 2, "i1")
                L.hline(xx, xx + 2, y - 1, "i7")
    L.vline(8, 0, 6, "b1") if False else None
    for y in range(0, 7):
        L.px(7 + (y % 2), y, "fr2")


# --------------------------------------------------------------------------
# The seals: bronze plates and grates (the Girdle), shrines and fire
# --------------------------------------------------------------------------

def plate(s, pressed=False):
    L = s.M
    L.rect(2, 3, 12, 11, "b0")
    L.rect(3, 4, 10, 9, "b1" if pressed else "b2")
    L.rect(4, 5, 8, 7, "b1")
    L.hline(3, 12, 4, "au" if not pressed else "b2")
    L.vline(3, 4, 12, "au" if not pressed else "b2")
    # the Girdle's knot (Herakles's) incised in the bronze
    for x, y in ((6, 7), (7, 8), (8, 8), (9, 7), (7, 6), (8, 6), (6, 9), (9, 9), (7, 10), (8, 10)):
        L.px(x, y, "b0" if not pressed else "au2")
    if pressed:
        L.hline(2, 13, 3, "dk")
    L.hline(2, 13, 14, "b0")


def grate(s, raised=False):
    """A bronze portcullis across a passage; raised, only its foot shows."""
    L = s.M
    if raised:
        L.rect(0, 0, 16, 3, "b0")
        L.hline(0, 15, 0, "b2")
        for x in (1, 5, 9, 13):
            L.rect(x, 0, 2, 3, "b1")
        return
    L.rect(0, 0, 16, 2, "b0")
    L.hline(0, 15, 0, "au")
    for x in (1, 5, 9, 13):
        L.rect(x, 0, 2, 15, "b1")
        L.vline(x, 1, 14, "b2")
        L.rect(x, 14, 2, 2, "b0")
        L.px(x, 15, "dk")
    for y in (5, 10):
        L.rect(0, y, 16, 2, "b0")
        L.hline(0, 15, y, "b2")


def shrine(s):
    """A small marble stele on a step, a painted relief of one of the Twelve,
    an offering bowl: each floor's shrine, where a fragment of the Olympians'
    story is cut."""
    L = s.M
    L.rect(2, 26, 12, 6, "m1")
    L.rect(3, 26, 10, 4, "m3")
    L.hline(2, 13, 31, "m0")
    L.rect(4, 3, 8, 23, "m2")
    L.rect(5, 4, 6, 21, "m3")
    L.vline(4, 3, 25, "m4")
    L.vline(11, 3, 25, "m1")
    # the pediment and its acroteria
    L.poly([(3, 4), (8, 0), (12, 4)], "m4")
    L.hline(3, 12, 4, "m1")
    L.px(8, 0, "au")
    # the relief: a blue field, a gold figure
    L.rect(6, 7, 4, 10, "bl")
    L.vline(8, 9, 15, "au")
    L.px(8, 8, "au")
    L.px(7, 11, "au")
    L.px(9, 11, "au")
    L.hline(6, 9, 18, "rd")
    L.hline(6, 9, 20, "m1")
    L.hline(6, 9, 22, "m1")
    # the offering bowl at its foot
    L.rect(11, 24, 4, 2, "b2")
    L.hline(11, 14, 24, "au")


def brazier(s, lit=True, frame=0):
    """A bronze tripod brazier on the snow, burning."""
    L = s.M
    for x0, x1 in ((4, 2), (8, 8), (12, 14)):
        L.line(x0, 22, x1, 31, "b0")
    L.line(4, 22, 2, 31, "b1")
    L.rect(2, 17, 12, 5, "b1")
    L.hline(2, 13, 17, "b2")
    L.hline(3, 12, 21, "b0")
    L.rect(3, 16, 10, 1, "au")
    if lit:
        f = [(5, 15), (8, 10 - frame), (11, 15)]
        L.poly([(3, 16), (5, 9 + frame), (7, 12), (8, 5 + frame), (10, 11), (12, 8 - frame), (13, 16)], "fl1")
        L.poly([(5, 16), (7, 11), (8, 8 + frame), (9, 11), (11, 16)], "fl2")
        L.px(8, 13, "m4")


def tripod(s):
    """A bronze victory tripod on its plinth: the processional way's markers."""
    L = s.M
    L.rect(3, 26, 10, 6, "m2")
    L.hline(3, 12, 26, "m4")
    L.hline(3, 12, 31, "m0")
    for x0, x1 in ((4, 4), (8, 8), (12, 12)):
        L.vline(x0, 12, 26, "b1")
    L.line(4, 12, 6, 18, "b2")
    L.line(12, 12, 10, 18, "b2")
    L.ellipse(2, 5, 14, 13, "b1")
    L.ellipse(3, 5, 13, 9, "b2")
    L.hline(4, 12, 6, "au")
    L.rect(5, 2, 2, 4, "au2")
    L.rect(10, 2, 2, 4, "au2")
    L.px(5, 1, "au")
    L.px(11, 1, "au")


def herm(s):
    """A herm of Hermes in snow: a square shaft, a bearded head, a red wool strip."""
    L = s.M
    L.rect(4, 12, 8, 20, "m2")
    L.rect(5, 12, 6, 19, "m3")
    L.vline(4, 12, 31, "m4")
    L.hline(4, 11, 31, "m0")
    L.ellipse(4, 1, 11, 11, "m3")
    L.ellipse(5, 2, 9, 7, "m4")
    L.rect(5, 8, 6, 4, "m2")
    L.px(6, 5, "m0")
    L.px(9, 5, "m0")
    L.hline(4, 11, 13, "rd")
    L.px(12, 14, "rd")
    L.px(12, 15, "rd")
    L.rect(3, 17, 2, 2, "m2")
    L.rect(11, 17, 2, 2, "m2")


# --------------------------------------------------------------------------
# Ladders and mouths
# --------------------------------------------------------------------------

def ladder_down(s):
    """A shaft cut down through the ice, a wooden ladder in it."""
    s.B.rect(2, 2, 12, 12, "i0") if False else None
    L = s.M
    L.ellipse(1, 1, 14, 14, "dk")
    L.ellipse(2, 2, 13, 13, "m0")
    L.ellipse(3, 4, 12, 13, "dk")
    for x in (5, 10):
        L.vline(x, 3, 15, "b1")
    for y in (5, 9, 13):
        L.hline(5, 10, y, "b2")
    L.hline(3, 12, 1, "m3")


def ladder_up(s):
    """A ladder leaning up through a shaft of daylight."""
    L = s.M
    L.rect(3, 0, 10, 16, "m3")
    L.rect(4, 0, 8, 16, "m4")
    for x in (5, 10):
        L.vline(x, 0, 15, "b1")
        L.vline(x + 1, 0, 15, "b0") if False else None
    for y in (2, 6, 10, 14):
        L.hline(5, 10, y, "b2")


def mouth(s, dark=True):
    """A cave mouth in an ice face, 2x2: the arch above (solid), the way in below."""
    L = s.M
    inside = "i0" if dark else "ws"
    L.poly([(3, 32), (3, 12), (7, 6), (16, 3), (25, 6), (29, 12), (29, 32)], "i2")
    L.poly([(5, 32), (5, 13), (9, 8), (16, 6), (23, 8), (27, 13), (27, 32)], inside)
    if dark:
        L.poly([(7, 32), (7, 16), (11, 11), (16, 10), (21, 11), (25, 16), (25, 32)], "i1")
    # icicles hanging in the mouth
    for x in (8, 11, 15, 19, 23):
        ln = 3 + h("mouth", x) % 4
        L.vline(x, 8, 8 + ln, "i7")
        L.px(x, 9 + ln, "i6")
    L.line(3, 12, 7, 6, "i5")
    L.line(7, 6, 16, 3, "i6")
    L.line(16, 3, 25, 6, "i4")


def exit_light(s, arrow="^"):
    """Daylight on the snow at a cave's mouth: the way out."""
    L = s.B
    for y in range(16):
        for x in range(16):
            n = h("light", x, y) % 9
            if (16 - y if arrow == "^" else y) + n > 14:
                L.px(x, y, "s5")
            elif n < 3:
                L.px(x, y, "s4")


# --------------------------------------------------------------------------
# Snow paving and the propylaia
# --------------------------------------------------------------------------

def paving(s, variant=0):
    """Marble flagstones on the processional way, snow in the joints."""
    L = s.B
    L.rect(0, 0, 16, 16, "m3")
    for y in range(16):
        for x in range(16):
            if h("pav", x, y, variant) % 11 == 0:
                L.px(x, y, "m2")
    off = 8 if variant else 0
    L.hline(0, 15, 7, "m1")
    L.hline(0, 15, 15, "m1")
    L.vline((4 + off) % 16, 0, 6, "m1")
    L.vline((12 + off) % 16, 8, 14, "m1")
    L.hline(0, 15, 8, "m4")
    L.hline(0, 15, 0, "m4")
    # snow lodged in the joints
    for x in range(0, 16, 3):
        if h("pavsnow", x, variant) % 3 == 0:
            L.px(x, 7, "m4")


def propylaia(s):
    """The gatehouse of the Pantheon, 7x5: a Doric porch of six columns (one per
    cell, so every column shares its tiles) under a pediment with a gilded Zeus,
    snow on the cornice and capitals, the bronze door in the middle bay."""
    L = s.M
    W, H = 7 * 16, 5 * 16
    # the cella wall behind the columns, in shadow
    L.rect(0, 30, W, 50, "m1")
    L.rect(0, 30, W, 3, "m0")
    # the door bay (cell 3): bronze leaves, open to the dark beyond
    dx = 3 * 16
    L.rect(dx, 36, 16, 44, "m2")
    L.rect(dx + 2, 40, 12, 40, "dk")
    L.rect(dx + 3, 42, 4, 38, "b0")
    L.rect(dx + 9, 42, 4, 38, "b0")
    L.vline(dx + 3, 42, 79, "b1")
    L.vline(dx + 12, 42, 79, "b1")
    L.px(dx + 6, 58, "au")
    L.px(dx + 9, 58, "au")
    L.hline(dx + 1, dx + 14, 38, "au2")
    # the columns: one per cell, fluted, Doric capitals with snow
    for c in (0, 1, 2, 4, 5, 6):
        x0 = c * 16
        L.rect(x0 + 3, 33, 10, 41, "m3")
        L.vline(x0 + 3, 33, 73, "m4")
        L.vline(x0 + 6, 35, 73, "m2")
        L.vline(x0 + 9, 35, 73, "m2")
        L.vline(x0 + 12, 33, 73, "m1")
        L.rect(x0 + 1, 29, 14, 4, "m4")
        L.hline(x0 + 1, x0 + 14, 32, "m1")
        L.hline(x0 + 2, x0 + 13, 28, "m4")
    # the steps under the porch
    L.rect(0, 74, W, 6, "m2")
    L.hline(0, W - 1, 74, "m4")
    L.hline(0, W - 1, 77, "m3")
    L.hline(0, W - 1, 79, "m1")
    L.rect(dx + 1, 74, 14, 6, "m3")
    # the entablature: architrave, the blue frieze with gold triglyphs, cornice
    L.rect(0, 16, W, 12, "m3")
    L.hline(0, W - 1, 16, "m4")
    L.rect(0, 19, W, 6, "bl")
    for x in range(0, W, 8):
        L.rect(x + 1, 19, 3, 6, "m2")
        L.px(x + 2, 20, "m4")
        L.px(x + 6, 22, "au")
    L.hline(0, W - 1, 25, "m1")
    L.hline(0, W - 1, 27, "m0")
    # the pediment: a gold Zeus with the thunderbolt in a blue field, snow on the rake
    zx = W // 2
    L.poly([(0, 16), (zx, 1), (W - 1, 16)], "m4")
    L.poly([(9, 15), (zx, 5), (W - 10, 15)], "bl")
    L.rect(zx - 2, 9, 5, 7, "au")
    L.ellipse(zx - 2, 6, zx + 2, 10, "au")
    L.line(zx + 3, 10, zx + 9, 8, "au")
    L.line(zx + 9, 8, zx + 7, 12, "fl2")
    L.line(zx + 7, 12, zx + 12, 11, "fl2")
    L.line(zx - 3, 12, zx - 8, 14, "au2")
    for x in (24, 34, 78, 88):
        L.rect(x - 1, 12, 3, 3, "au2")
    L.line(0, 16, zx, 1, "m3")
    L.line(1, 15, zx, 0, "m4")
    L.line(zx, 1, W - 1, 16, "m2")
    L.rect(zx - 1, 0, 3, 2, "au")
    L.rect(0, 14, 3, 3, "au")
    L.rect(W - 3, 14, 3, 3, "au")


# --------------------------------------------------------------------------
# The cloud sea below the mountain
# --------------------------------------------------------------------------

# (kx over 64 px, ky over 32 px), amplitude, phase
WAVES = [((1, 0), 1.0, 0.3), ((0, 1), 0.8, 1.7), ((1, 1), 0.8, 2.4), ((2, -1), 0.7, 0.9),
         ((3, 1), 0.45, 4.1), ((2, 2), 0.4, 5.3), ((5, 0), 0.3, 2.2), ((1, 3), 0.25, 0.6),
         ((4, -2), 0.3, 3.3), ((7, 1), 0.15, 1.1)]


def cloud_field(x, y):
    """Tileable lumpy noise, period 64 x 32: the cloud tops' height."""
    v = 0.0
    for (kx, ky), a, ph in WAVES:
        v += a * math.sin(2 * math.pi * (kx * x / 64 + ky * y / 32) + ph)
    return v


def cloud_sea(s):
    """A 4x2 block of cumulus seen from above, tileable in all four directions:
    mostly sunlit white, lavender only in the folds, lit from the upper left."""
    L = s.B
    for y in range(32):
        for x in range(64):
            v = cloud_field(x, y)
            lit = cloud_field(x - 2, y - 2) - v
            if v > 0.2:
                c = "cl3" if lit < 0.25 else "cl2"
            elif v > -0.9:
                c = "cl2" if lit < 0.35 else "cl1"
            elif v > -2.0:
                c = "cl1"
            else:
                c = "cl0"
            if v > 1.3 and lit < -0.2:
                c = "s5"
            L.px(x, y, c)


def cloud_edge(s):
    """Where the snow ends and the cloud begins: a snow lip, then the cloud's
    tops rising in front of the drop, 4 wide (tileable left to right)."""
    L = s.B
    cloud_sea(s)
    for x in range(64):
        lip = 5 + (h("lip", x // 3) % 3)
        for y in range(lip):
            L.px(x, y, "s3" if y < lip - 2 else "s2")
        L.px(x, lip - 1, "s1")
        L.px(x, lip, "i4")
        L.px(x, lip + 1, "cl0")


# --------------------------------------------------------------------------
# Floor accents
# --------------------------------------------------------------------------

def accent(kind):
    def draw(s):
        L = s.B
        if kind == "tracks":
            for x, y in ((4, 3), (7, 7), (4, 11), (7, 15)):
                L.rect(x, y - 1, 2, 2, "s1")
                L.px(x, y - 1, "s0")
        elif kind == "ripples":
            for y in (3, 8, 13):
                for x in range(16):
                    if (x + y) % 7 < 4:
                        L.px(x, y + (1 if (x // 4) % 2 else 0), "s4")
                        L.px(x, y + 1 + (1 if (x // 4) % 2 else 0), "s2")
        elif kind == "stone":
            L.ellipse(5, 7, 11, 11, "s1")
            L.ellipse(5, 6, 10, 9, "s2") if False else None
            L.hline(6, 9, 7, "s4")
            L.hline(5, 11, 11, "s0")
        elif kind == "glitter":
            for x, y in ((3, 4), (11, 2), (8, 9), (13, 12), (4, 13)):
                L.px(x, y, "fr2")
                L.px(x + 1, y, "fr1")
    return draw


def props():
    P = []
    P.append(prop("crystal_s", "A crystal cluster", 1, 1, ["X"], crystal_s))
    P.append(prop("crystal_tall", "A tall crystal prism", 1, 2, ["X", "X"], crystal_tall))
    P.append(prop("crystal_l", "A great crystal geode", 2, 2, ["XX", "XX"], crystal_l))
    P.append(prop("ice_rock", "An ice-glazed rock", 1, 1, ["X"], ice_rock))
    P.append(prop("crystal_s_ice", "A crystal cluster grown up through the ice", 1, 1, ["X"], crystal_s, on_ice=True))
    P.append(prop("ice_rock_ice", "A rock frozen into the ice", 1, 1, ["X"], ice_rock, on_ice=True))
    P.append(prop("ice_boulders", "Snow-capped ice boulders", 2, 2, ["XX", "XX"], ice_boulders))
    P.append(prop("frozen_giant", "A giant of the Gigantomachy, frozen in the glacier", 3, 3,
                  ["XXX", "XXX", "XXX"], frozen_giant))
    P.append(prop("frozen_fall", "A waterfall frozen in mid-pour", 2, 3, ["XX", "XX", "XX"], frozen_fall,
                  floor=False, bottom_fill=fill_fall))
    P.append(prop("pine_snow", "A snow-laden fir", 2, 3, ["TT", "TT", "XX"], pine_snow))
    P.append(prop("pine_snow_s", "A young snow fir", 1, 2, ["T", "X"], pine_snow_s))
    P.append(prop("handholds", "Pan's Crook's handholds up an ice face", 1, 2, ["X", "X"], handholds,
                  names={"top": (0, 0), "foot": (0, 1)}, floor=False, bottom_fill=fill_face))
    P.append(prop("plate", "A bronze pressure plate (the Girdle's seals)", 1, 1, ["."], plate))
    P.append(prop("plate_down", "A pressure plate, pressed", 1, 1, ["."], lambda s: plate(s, True)))
    P.append(prop("grate", "A bronze grate across a passage", 1, 1, ["X"], grate))
    P.append(prop("grate_up", "A grate, raised", 1, 1, ["."], lambda s: grate(s, True)))
    P.append(prop("shrine", "A floor's shrine: a stele of one of the Twelve", 1, 2, ["X", "X"], shrine))
    P.append(prop("brazier", "A bronze brazier burning on the snow", 1, 2, ["X", "X"], brazier))
    P.append(prop("tripod", "A bronze tripod on its plinth", 1, 2, ["X", "X"], tripod))
    P.append(prop("herm", "A herm of Hermes", 1, 2, ["X", "X"], herm))
    P.append(prop("ladder_down", "A shaft with a ladder down", 1, 1, ["."], ladder_down,
                  behaviors={(0, 0): "MB_LADDER"}))
    P.append(prop("ladder_up", "A ladder up into daylight", 1, 1, ["."], ladder_up,
                  behaviors={(0, 0): "MB_LADDER"}))
    P.append(prop("mouth", "A cave mouth in the ice", 2, 2, ["XX", ".."], mouth, floor=False,
                  bottom_fill=lambda s: fill_rock(s), behaviors={(0, 1): "MB_NON_ANIMATED_DOOR",
                                                                  (1, 1): "MB_NON_ANIMATED_DOOR"}))
    P.append(prop("exit_n", "Daylight at a mouth: the way out north", 1, 1, ["^"],
                  lambda s: exit_light(s, "^")))
    P.append(prop("exit_s", "Daylight at a mouth: the way out south", 1, 1, ["v"],
                  lambda s: exit_light(s, "v")))
    P.append(prop("paving", "Snowy marble paving", 1, 1, ["."], lambda s: paving(s, 0), floor=False))
    P.append(prop("paving_b", "Snowy marble paving, offset", 1, 1, ["."], lambda s: paving(s, 1), floor=False))
    P.append(prop("propylaia", "The propylaia of the Pantheon", 7, 5,
                  ["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "XXX.XXX"],
                  propylaia, names={"door": (3, 4)}, behaviors={(3, 4): "MB_NON_ANIMATED_DOOR"}))
    P.append(prop("cloud", "The cloud sea below the mountain", 4, 2, ["XXXX", "XXXX"], cloud_sea, floor=False))
    P.append(prop("cloud_edge", "The snow's edge over the cloud sea", 4, 2, ["XXXX", "XXXX"], cloud_edge,
                  floor=False))
    for k in ("tracks", "ripples", "stone", "glitter"):
        P.append(prop("snow_" + k, "Snow: " + k, 1, 1, ["."], accent(k)))
    return P


def summit_props():
    P = []
    # 2026-11-18, the endgame upgrade: the summit moves onto Chion (above the cloud),
    # and the Deep gets a living fall for the Horn of Achelous. They pack into the empty
    # rows between the styles and the props (chion_build.SECTION_ROWS), so no
    # earlier metatile moves.
    P.append(prop("altar_zeus", "The great ash altar of Zeus, the bronze box on it", 4, 2,
                  ["XXXX", "XXXX"], altar_zeus))
    P.append(prop("temple_twelve", "The temple of the Twelve on the summit", 7, 5,
                  ["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "XXX.XXX"],
                  temple_twelve, names={"door": (3, 4)}, behaviors={(3, 4): "MB_NON_ANIMATED_DOOR"}))
    P.append(prop("meltfall", "Meltwater pouring down an ice face (the Horn of Achelous climbs it)", 2, 3,
                  ["..", "..", ".."], meltfall, floor=False,
                  behaviors={(x, y): "MB_WATERFALL" for x in (0, 1) for y in (0, 1, 2)}))
    return P


def altar_zeus(s):
    """The great altar of Zeus, 4x2: a stepped marble platform with horned
    corners, grey ash heaped on it from every rite, the little bronze box
    (Medon's Knot) in the middle."""
    L = s.M
    W = 64
    # the steps, front and sides
    L.rect(0, 22, W, 10, "m2")
    L.hline(0, W - 1, 22, "m4")
    L.hline(0, W - 1, 26, "m3")
    L.hline(0, W - 1, 31, "m0")
    L.rect(4, 8, W - 8, 15, "m3")
    L.hline(4, W - 5, 8, "m4")
    L.vline(4, 8, 22, "m4")
    L.vline(W - 5, 8, 22, "m1")
    # the frieze on the altar's face: a blue band with gold rosettes
    L.rect(6, 14, W - 12, 5, "bl")
    for x in range(10, W - 8, 8):
        L.px(x, 16, "au")
        L.px(x - 1, 16, "au2")
        L.px(x + 1, 16, "au2")
    L.hline(6, W - 7, 19, "m1")
    # the horned corners (acroteria)
    for x in (3, W - 8):
        L.rect(x, 3, 5, 6, "m4")
        L.px(x + 1, 2, "m4")
        L.px(x + 3, 2, "m3")
        L.vline(x + 4, 3, 8, "m1")
    # the ash of every rite, and the box in the middle
    L.rect(9, 5, W - 18, 4, "m1")
    L.hline(10, W - 11, 4, "m2")
    for x in range(11, W - 11, 5):
        L.px(x, 6, "m0")
    bx = W // 2 - 6
    L.rect(bx, 0, 12, 8, "b1")
    L.rect(bx + 1, 1, 10, 3, "b2")
    L.hline(bx, bx + 11, 4, "au")
    L.px(bx + 5, 6, "au")
    L.px(bx + 6, 6, "au")
    L.hline(bx, bx + 11, 8, "b0")


def temple_twelve(s):
    """The temple of the Twelve, 7x5, facing east over the altar: an Ionic porch
    (gilded volutes, snow on every capital), a red frieze of the twelve seated
    Olympians in gold, an eagle with the thunderbolt in the pediment, gold
    acroteria. The Pantheon's propylaia is Doric and plain; this is the house."""
    L = s.M
    W = 7 * 16
    L.rect(0, 30, W, 50, "m1")
    L.rect(0, 30, W, 3, "m0")
    dx = 3 * 16
    L.rect(dx, 36, 16, 44, "m2")
    L.rect(dx + 2, 40, 12, 40, "dk")
    L.rect(dx + 4, 44, 8, 36, "fl1")
    L.rect(dx + 6, 50, 4, 30, "fl2")           # the fire inside the cella
    L.hline(dx + 1, dx + 14, 38, "au")
    for c in (0, 1, 2, 4, 5, 6):
        x0 = c * 16
        L.rect(x0 + 4, 34, 8, 40, "m3")
        L.vline(x0 + 4, 34, 73, "m4")
        L.vline(x0 + 7, 36, 73, "m2")
        L.vline(x0 + 11, 34, 73, "m1")
        # the Ionic capital: a cushion with two gilded volutes, snow on top
        L.rect(x0 + 1, 30, 14, 4, "m3")
        L.hline(x0 + 1, x0 + 14, 29, "m4")
        L.px(x0 + 2, 32, "au")
        L.px(x0 + 13, 32, "au")
        L.px(x0 + 2, 33, "au2")
        L.px(x0 + 13, 33, "au2")
        L.rect(x0 + 3, 73, 10, 1, "m2")       # the base's torus
    L.rect(0, 74, W, 6, "m2")
    L.hline(0, W - 1, 74, "m4")
    L.hline(0, W - 1, 77, "m3")
    L.hline(0, W - 1, 79, "m1")
    L.rect(dx + 1, 74, 14, 6, "m3")
    # the frieze: the Twelve enthroned, gold on red, one to each 9 px
    L.rect(0, 16, W, 12, "m3")
    L.hline(0, W - 1, 16, "m4")
    L.rect(0, 19, W, 7, "rd")
    for i in range(12):
        x = 3 + i * 9
        L.rect(x + 1, 20, 2, 2, "au")         # a head
        L.rect(x, 22, 4, 2, "au")             # the seated body
        L.vline(x + 4, 21, 25, "au2")         # the throne's back
        L.px(x, 25, "au2")
    L.hline(0, W - 1, 26, "m1")
    L.hline(0, W - 1, 27, "m0")
    # the pediment: an eagle with spread wings and the thunderbolt
    zx = W // 2
    L.poly([(0, 16), (zx, 1), (W - 1, 16)], "m4")
    L.poly([(9, 15), (zx, 5), (W - 10, 15)], "bl")
    L.line(zx - 16, 13, zx - 2, 8, "au")
    L.line(zx - 14, 14, zx - 2, 10, "au2")
    L.line(zx + 16, 13, zx + 2, 8, "au")
    L.line(zx + 14, 14, zx + 2, 10, "au2")
    L.rect(zx - 2, 7, 5, 6, "au")
    L.px(zx, 6, "au")
    L.line(zx - 1, 13, zx - 4, 15, "fl2")
    L.line(zx + 1, 13, zx + 4, 15, "fl2")
    L.line(0, 16, zx, 1, "m3")
    L.line(1, 15, zx, 0, "m4")
    L.line(zx, 1, W - 1, 16, "m2")
    for x0 in (zx - 2, 0, W - 4):
        L.rect(x0, 0 if x0 == zx - 2 else 13, 4, 3, "au")


def meltfall(s):
    """Meltwater pouring down an ice face, 2x3: the one fall on the mountain the
    cold hasn't stopped (a spring from under the cone). Its cells are
    MB_WATERFALL: the Horn of Achelous climbs it from the tarn."""
    L = s.B
    L.rect(0, 0, 32, 48, "w2")
    for x in range(32):
        hgt = h("melt", x) % 7
        c = ("w3", "w4", "w5", "w3", "w4", "s4", "w3")[hgt]
        L.vline(x, 0, 47, c)
        for y in range((h("meltg", x) % 9), 48, 9):
            L.px(x, y, "s5")
            L.px(x, min(47, y + 1), "w5")
    L.vline(0, 0, 47, "w1")
    L.vline(31, 0, 47, "w1")
    for y in range(42, 48):
        for x in range(32):
            if (x + y) % 3:
                L.px(x, y, "s5" if (x * 7 + y) % 5 else "ic2")


def fill_face(s):
    """A two-cell ice face (top with its rim, then the base) behind a piece."""
    cells = kit_cells()
    s.B.a[0:16, 0:16] = recolor(cells["ft|A|A"][0]["bottom"], lib.ROCK_MAP)
    s.B.a[16:32, 0:16] = recolor(cells["fb|A|A"][0]["bottom"], lib.ROCK_MAP)


def fill_fall(s):
    """The fall's ground: the ice face (top, base) above the snow at its foot."""
    cells = kit_cells()
    for cx in range(2):
        s.B.a[0:16, cx * 16:cx * 16 + 16] = recolor(cells["ft|A|A"][0]["bottom"], lib.ROCK_MAP)
        s.B.a[16:32, cx * 16:cx * 16 + 16] = recolor(cells["fb|A|A"][0]["bottom"], lib.ROCK_MAP)
        s.B.a[32:48, cx * 16:cx * 16 + 16] = floor_base()


def fill_rock(s):
    """The mouth's ground: the ice face's base behind the arch, snow at the way in."""
    cells = kit_cells()
    face = recolor(cells["fb|A|A"][0]["bottom"], lib.ROCK_MAP)
    top = recolor(cells["ft|A|A"][0]["bottom"], lib.ROCK_MAP)
    s.B.a[0:16, 0:16] = top
    s.B.a[0:16, 16:32] = top
    s.B.a[16:32, 0:16] = face
    s.B.a[16:32, 16:32] = face
