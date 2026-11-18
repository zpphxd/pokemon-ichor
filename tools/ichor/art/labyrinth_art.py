"""gTileset_Labyrinth: Daedalus's Labyrinth under Knossa (LABYRINTH.md §11).

This batch draws the first part: **Daedalus's workshop**, the hub at the end of
Ring III (LABYRINTH.md §6, scenes D and L). The rings, the forge, the archive,
the tomb and the Starry Chamber come later into the same tileset, so the palette
plan and the sheet's sections are laid out for all of it now.

The look. Daedalus built the whole house, his workshop included, in one stone:
a cool grey Cretan limestone laid in irregular gypsum slabs with red plaster in
the joints, the way Minoan floors were laid. The rings are the same stone in the
dark; the workshop is that stone lit. Bronze, timber, papyrus and terracotta sit
on it as the workshop's own colors.

Palette plan (secondary slots 6-12). LABYRINTH.md §11 names seven palettes. Six
are slots; the seventh, glow, is a palette *variant* (SYSTEMS.md §2: "each dark
tileset needs one extra palette set"), loaded over 6-12 while the torch is
doused, as the Temple of Demeter's is. That leaves a seventh slot, which this
plan gives to timber and papyrus: the workshop's benches, drafting tables, plans
and shelves, and later the archive's shelves and the Titans' furniture.

  stone   dark stone with thread red: the masonry of every map, the thread twins,
          the red plaster, lamp-warm and dawn-cool light on stone, the glow paint
  minoan  Minoan red: red columns, ochre, gypsum, black capitals, terracotta (the
          Pithos), horns of consecration, labrys seals, Minos's tomb
  fresco  fresco blue: blue grounds, dolphins, lilies, saffron, bull-leapers
  bronze  bronze and Titan: automata, grates, dials, bells, mirrors, anchor rings,
          tools, the Titans' slate and gold
  fire    forge fire: flames, embers, molten bronze, iron, clay lamps
  night   starry night: the Starry Chamber, its lustral pool, moonlit marble
  timber  timber and papyrus: benches, tables, shelves, plans, beds, scrolls

  glow    (variant set) black but for the glow paint, the flames and a faint
          thread; written by labyrinth_build.py as porytiles_bin/glow/
  dawn    (variant set) the room dimmed and cooled but for the dawn light, for
          scene L; written as porytiles_bin/dawn/

Every 8x8 tile of every layer draws from one group (validate() checks), every
bottom layer is opaque (so it works on any primary; it is drawn for oikos), and
a metatile uses at most two layers. Floors and walls fill the bottom layer;
objects stand in the middle layer. Surfaces that carry objects (bench tops,
shelving, the lift's deck) fill the bottom layer so their objects can sit in the
middle layer in another palette.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math

import numpy as np

import emporion_lib as E
import kalliste_lib as K
from emporion_lib import tile_colors

# --------------------------------------------------------------------------
# Colors and palette groups
# --------------------------------------------------------------------------

NEW = {
    # stone: a cool grey limestone ramp that warms toward the light
    "lk": (24, 16, 32),
    "ls1": (48, 40, 56), "ls2": (72, 64, 80), "ls3": (104, 96, 104), "ls4": (136, 128, 128),
    "ls5": (168, 160, 152), "ls6": (200, 192, 176),
    # Ariadne's thread, which is also the red plaster in the floor's joints
    "lt0": (120, 40, 40), "lt1": (192, 40, 40), "lt2": (240, 112, 96),
    # lamp-warm and dawn-cool light on stone
    "lj": (152, 120, 112), "lw1": (232, 200, 144),
    "ld0": (160, 176, 192), "ld1": (216, 224, 232),
    # the glow paint, latent: by torchlight it is the stone it is painted on
    "lg": (80, 72, 96),
    # minoan
    "mr0": (104, 24, 24), "mr1": (160, 40, 32), "mr2": (208, 72, 48), "mr3": (232, 128, 96),
    "mo0": (160, 104, 40), "mo1": (216, 160, 64), "mo2": (240, 216, 144),
    "mg0": (184, 176, 160), "mg1": (224, 216, 200), "mg2": (248, 240, 224),
    "mb": (56, 48, 48),
    "mt0": (128, 64, 40), "mt1": (184, 104, 64), "mt2": (224, 152, 104),
    # fresco
    "fw": (248, 248, 240),
    "fb0": (24, 48, 104), "fb1": (40, 88, 168), "fb2": (96, 152, 216), "fb3": (168, 208, 240),
    "fy0": (216, 152, 40), "fy1": (248, 208, 96), "fr": (192, 56, 40), "fs": (168, 88, 56),
    "fg0": (56, 104, 64), "fg1": (120, 168, 96), "fq": (120, 128, 168), "fcr": (232, 216, 184),
    "fp": (232, 160, 152),
    # bronze and Titan
    "bz0": (72, 40, 24), "bz1": (120, 72, 32), "bz2": (168, 112, 48), "bz3": (216, 168, 80),
    "bz4": (248, 224, 144),
    "bv0": (48, 96, 88), "bv1": (96, 152, 128),
    "bi0": (56, 56, 72), "bi1": (104, 104, 120),
    "ts0": (40, 32, 56), "ts1": (80, 72, 104),
    "bw": (248, 248, 232), "be": (248, 176, 48), "brp": (200, 176, 128),
    # fire (fz0-fz2 are bronze's bz1-bz3, so a hand or a lamp's dish in bronze can
    # share a tile with its flame)
    "fe0": (96, 24, 16), "fe1": (176, 48, 24), "ff0": (232, 104, 32), "ff1": (248, 168, 48),
    "ff2": (248, 224, 120), "ff3": (248, 248, 224),
    "fi0": (48, 40, 48), "fi1": (88, 80, 88), "fi2": (136, 128, 128),
    "fc0": (144, 72, 40), "fc1": (200, 128, 80),
    # starry night
    "nk": (8, 8, 24), "nn0": (16, 24, 56), "nn1": (32, 48, 96), "nn2": (56, 80, 144),
    "nn3": (96, 128, 192), "ns0": (248, 248, 248), "ns1": (248, 232, 160),
    "nm0": (120, 128, 152), "nm1": (168, 176, 200), "nm2": (216, 224, 240),
    "np0": (16, 40, 56), "np1": (32, 72, 88), "ng0": (184, 136, 56), "ng1": (232, 200, 104),
    # timber and papyrus
    "tw0": (64, 40, 24), "tw1": (112, 72, 40), "tw2": (160, 112, 64), "tw3": (208, 160, 104),
    "tp0": (176, 152, 104), "tp1": (216, 200, 152), "tp2": (248, 240, 208),
    "tr": (176, 64, 40), "tg": (88, 88, 104), "tx": (224, 176, 64),
    "tb0": (40, 64, 120), "tb1": (80, 120, 184), "tq": (192, 168, 120),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C
# the fire group's bronze, by the bronze names' colors
for _a, _b in (("fz0", "bz1"), ("fz1", "bz2"), ("fz2", "bz3")):
    C[_a] = C[_b]

GROUPS = {
    "stone": ["lk", "ls1", "ls2", "ls3", "ls4", "ls5", "ls6", "lt0", "lt1", "lt2",
              "lj", "lw1", "ld0", "ld1", "lg"],
    "minoan": ["ink", "mr0", "mr1", "mr2", "mr3", "mo0", "mo1", "mo2", "mg0", "mg1", "mg2",
               "mb", "mt0", "mt1", "mt2"],
    "fresco": ["ink", "fw", "fb0", "fb1", "fb2", "fb3", "fy0", "fy1", "fr", "fs", "fg0", "fg1",
               "fq", "fcr", "fp"],
    "bronze": ["ink", "bz0", "bz1", "bz2", "bz3", "bz4", "bv0", "bv1", "bi0", "bi1", "ts0",
               "ts1", "bw", "be", "brp"],
    "fire": ["ink", "fe0", "fe1", "ff0", "ff1", "ff2", "ff3", "fi0", "fi1", "fi2", "fc0",
             "fc1", "fz0", "fz1", "fz2"],
    "night": ["nk", "nn0", "nn1", "nn2", "nn3", "ns0", "ns1", "nm0", "nm1", "nm2", "np0", "np1",
              "ng0", "ng1"],
    "timber": ["ink", "tw0", "tw1", "tw2", "tw3", "tp0", "tp1", "tp2", "tr", "tg", "tx", "tb0",
               "tb1", "tq"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# The variant sets (labyrinth_build.py writes them after compiling).
# glow: the doused torch (SYSTEMS.md §2). Everything is black but these.
LATENT = {"lg": (120, 248, 208)}          # the glow paint, when doused
LATENT_BASE = {"lg": "ls1"}               # ...and the stone it imitates by torchlight:
                                          # the wall tops' fill (labyrinth_kit._fill)
GLOW_KEEP = ["fe1", "ff0", "ff1", "ff2", "ff3"]   # flames stay lit
GLOW_DIM = {"lt0": (48, 8, 8), "lt1": (104, 24, 24), "lt2": (128, 48, 40)}   # the thread, faintly
# dawn: scene L. Every color dimmed and cooled toward the grey morning, but the
# dawn light itself, which stays as drawn.
DAWN_KEEP = ["ld0", "ld1", "lw1"]


def dawn_color(rgb):
    r, g, b = (int(v) for v in rgb)
    lum =(r * 3 + g * 4 + b * 2) / 9
    nr = 0.42 * r + 0.10 * lum + 4
    ng = 0.46 * g + 0.10 * lum + 8
    nb = 0.52 * b + 0.12 * lum + 22
    return tuple(min(248, int(round(v / 8)) * 8) for v in (nr, ng, nb))


SEC = "labyrinth"


# --------------------------------------------------------------------------
# Structures and validation
# --------------------------------------------------------------------------

class Struct(E.Struct):
    def __init__(self, key, title, w, h, walk=None, notes="", section="workshop"):
        super().__init__(key, title, w, h, walk=walk, notes=notes, ground="none",
                         section=section)
        self.names = {}
        self.anims = {}     # name -> {"layer", "frames": [Layer]}: see anim_layer()


def anim_layer(s, name, n, layer="middle"):
    """Start a tile animation on one of s's layers: returns n-1 extra frame
    Layers, each a copy of the layer as it is now (frame 0 is the layer itself).
    Paint the differences into them; every 8x8 tile that changes becomes a
    Porytiles animated tile (labyrinth_build.py writes them)."""
    src = s.layers[layer]
    frames = []
    for _ in range(n - 1):
        L = K.Layer(src.w, src.h)
        L.a[:] = src.a
        frames.append(L)
    s.anims[name] = {"layer": layer, "frames": frames}
    return frames


def anim_tiles(s):
    """{(layer name, tx, ty): anim name} for every tile of s that changes between
    frames."""
    out = {}
    for name, an in getattr(s, "anims", {}).items():
        base = s.layers[an["layer"]].a
        for f in an["frames"]:
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                    if not np.array_equal(base[sl], f.a[sl]):
                        out[(an["layer"], tx, ty)] = name
    return out


def validate(structs, groups=None):
    group_rgb = GROUP_RGB if groups is None else {g: {C[n] for n in ns} for g, ns in groups.items()}
    problems = []
    for s in structs:
        at = anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    cols = tile_colors(layer, tx, ty)
                    if (ln, tx, ty) in at:
                        for f in s.anims[at[(ln, tx, ty)]]["frames"]:
                            cols = cols | tile_colors(f, tx, ty)
                    if cols and not any(cols <= g for g in group_rgb.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                n = sum(1 for layer in s.layers.values() if (layer.a[sl][..., 3] > 0).any())
                if n == 3:
                    problems.append(f"{s.key} ({cx},{cy}) has three layers")
                if not (s.B.a[sl][..., 3] > 0).all():
                    problems.append(f"{s.key} ({cx},{cy}) has a bottom layer that isn't opaque")
    return problems


def finish(s):
    """A cell that drew in both the middle and top layers has its middle layer
    flattened into the bottom (at most two layers per metatile)."""
    for cy in range(s.h):
        for cx in range(s.w):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            if (s.M.a[sl][..., 3] > 0).any() and (s.T.a[sl][..., 3] > 0).any():
                src = s.M.a[sl]
                m = src[..., 3] > 0
                s.B.a[sl][m] = src[m]
                s.M.a[sl] = 0
    return s


def blit(L, rows, legend, x, y, hflip=False):
    L.blit(rows, legend, x, y, hflip=hflip)


def outline(L, x0, y0, w, h, c="ink"):
    """Outline the silhouette of whatever is drawn in the box, on its outside."""
    a = L.a[y0:y0 + h, x0:x0 + w, 3] > 0
    pad = np.pad(a, 1)
    ring = (~a) & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    ys, xs = np.nonzero(ring)
    for yy, xx in zip(ys, xs):
        L.px(x0 + xx, y0 + yy, c)


# --------------------------------------------------------------------------
# The floor: gypsum slabs in red plaster
# --------------------------------------------------------------------------

# Long gypsum slabs, two cells by one, laid in a running bond with red plaster
# in the joints, the way the palace's halls were floored. A slab's left half
# goes on cells where x + y is even, its right half where x + y is odd, so the
# whole floor costs four tiles. Each slab is lit along its top and left edges.
SLAB_PITS = {"l": ((5, 5), (4, 11)), "r": ((11, 5), (12, 11))}


def slab(L, x0, y0, half="l", tone=None):
    """One cell of the slab floor at (x0, y0). tone(x, y) may return a light
    level per pixel: 's' shadow, 'd1'/'d2' dawn light, 'w1'/'w2' lamplight."""
    for y in range(16):
        for x in range(16):
            if y == 0 or (half == "l" and x == 0):
                c = "lj"
            elif y == 1 or (half == "l" and x == 1):
                c = "ls6"
            elif y == 15 or (half == "r" and x == 15):
                c = "ls4"
            else:
                c = "ls5"
                if (x, y) in SLAB_PITS[half]:
                    c = "ls4"
            t = tone(x, y) if tone else None
            if t:
                c = TONE[t].get(c, c)
            L.px(x0 + x, y0 + y, c)


TONE = {
    "s": {"ls6": "ls5", "ls5": "ls4", "ls4": "ls3", "lj": "lt0"},
    "s2": {"ls6": "ls4", "ls5": "ls3", "ls4": "ls3", "lj": "lt0"},
    "w1": {"ls5": "lw1", "ls6": "lw1"},
    "d1": {"ls5": "ld0", "ls6": "ld1", "ls4": "ls5", "lj": "ls4"},
    "d2": {"ls5": "ld1", "ls6": "ld1", "ls4": "ld0", "lj": "ld0"},
}


def floors():
    s = Struct("floor", "Floor: gypsum slabs in red plaster", 8, 1, walk=["X......."],
               section="house",
               notes="Long gypsum slabs, two cells by one, in a running bond. **Lay `slab_l` "
                     "on every cell where x + y is even and `slab_r` where it is odd**, and the "
                     "slabs line up. (0) the void, near-black: the layout's border and every "
                     "cell outside the rooms (block it). (3), (4) the two halves in the shadow a "
                     "north wall casts, for the row in front of it. (5) a left half with a "
                     "mason's labrys cut in it, the house's mark. (6) a right half, cracked. (7) "
                     "a left half with an oil stain, for near the benches.")
    L = s.B
    L.rect(0, 0, 16, 16, "lk")
    for (x, y) in ((3, 4), (11, 9), (7, 13)):
        L.px(x, y, "ls1")
    slab(L, 16, 0, "l")
    slab(L, 32, 0, "r")
    shadow = lambda x, y: "s2" if y < 3 else "s" if y < 6 else None  # noqa: E731
    slab(L, 48, 0, "l", tone=shadow)
    slab(L, 64, 0, "r", tone=shadow)
    slab(L, 80, 0, "l")
    blit(L, ["k.k.k", "kkkkk", "k.k.k", "..k..", "..k.."], {"k": "ls4"}, 80 + 6, 6)
    blit(L, ["l.l.l", "lllll", "l.l.l", "..l..", "..l.."], {"l": "ls6"}, 80 + 6, 7)
    slab(L, 96, 0, "r")
    blit(L, ["k....", ".k...", ".kk..", "...k.", "...kk", "....k"], {"k": "ls3"}, 96 + 5, 5)
    slab(L, 112, 0, "l")
    for (x, y) in ((6, 8), (7, 8), (8, 8), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9),
                   (6, 10), (7, 10), (8, 10), (9, 10), (7, 11)):
        L.px(112 + x, y, "ls4")
    L.px(112 + 7, 9, "ls3")
    s.names = {"void": (0, 0), "slab_l": (1, 0), "slab_r": (2, 0), "shade_l": (3, 0),
               "shade_r": (4, 0), "labrys": (5, 0), "crack": (6, 0), "oil": (7, 0)}
    return s



# --------------------------------------------------------------------------
# The walls: a vaulted arcade
# --------------------------------------------------------------------------

def vault_band(L, x0, w):
    """The top three rows of every north wall: the vault's soffit in shadow."""
    for x in range(x0, x0 + w):
        L.px(x, 0, "lk")
        L.px(x, 1, "ls1")
        L.px(x, 2, "ls1")
        L.px(x, 3, "ls2")


def pier(L, x0, door=False):
    """A pier of the arcade, 16 x 48 (rows 0-2): lit on its left flank, an impost
    block where the arches spring (y 18-21), a plinth at its foot."""
    vault_band(L, x0, 16)
    for y in range(4, 48):
        for x in range(16):
            if x in (0, 15):
                c = "ls2"
            elif x == 1:
                c = "ls6"
            elif x == 2:
                c = "ls5"
            elif x == 14:
                c = "ls3"
            else:
                c = "ls4"
                # block joints, staggered courses 10 px tall
                yy = y - 4
                if yy % 10 == 9:
                    c = "ls3"
                elif (yy // 10) % 2 == 0 and x == 8 and yy % 10 != 9:
                    c = "ls3"
            L.px(x0 + x, y, c)
    # the impost
    for x in range(16):
        L.px(x0 + x, 18, "ls6")
        L.px(x0 + x, 19, "ls5")
        L.px(x0 + x, 20, "ls4")
        L.px(x0 + x, 21, "ls1")
    # the plinth
    for x in range(16):
        L.px(x0 + x, 42, "ls5")
        for y in (43, 44, 45, 46):
            L.px(x0 + x, y, "ls4" if x not in (0, 15) else "ls3")
        L.px(x0 + x, 47, "ls2")
    L.px(x0 + 1, 43, "ls6")
    if door:
        # a low doorway through the pier, rows 1-2: dark beyond
        for y in range(23, 48):
            for x in range(3, 13):
                L.px(x0 + x, y, "lk" if y > 24 else "ls1")
        for y in range(23, 48):
            L.px(x0 + 2, y, "ls3")
            L.px(x0 + 13, y, "ls2")
        for x in range(2, 14):
            L.px(x0 + x, 22, "ls6")


def arch(L, x0, w, rise=16, spring=20, band=5):
    """An elliptical arch over a bay x0..x0+w-1 springing from the piers' imposts
    at y=spring, its crown at spring-rise. Draws the voussoirs, the spandrels
    above and the recess's top; symmetric about the bay's middle. Returns a
    function inside(x, y) -> True under the intrados (the recess)."""
    vault_band(L, x0, w)
    cx = x0 + (w - 1) / 2
    a_i, b_i = w / 2, rise
    a_o, b_o = w / 2 + band, rise + band

    def inside(x, y):
        dx = (x - cx) / a_i
        dy = (y - spring) / b_i
        return y >= spring or dx * dx + dy * dy <= 1.0

    def in_band(x, y):
        dx = (x - cx) / a_o
        dy = (y - spring) / b_o
        return dx * dx + dy * dy <= 1.0

    for y in range(4, 48):
        for x in range(x0, x0 + w):
            if inside(x, y):
                continue
            if in_band(x, y) and y < spring + 1:
                # voussoirs: radial joints every ~14 degrees, lit on the upper rim
                # the angle from the crown, so the arch is symmetric
                ang = math.degrees(math.atan2(abs(x - cx) * b_i / a_i, spring - y))
                rim_o = not in_band(x, y - 1)
                rim_i = inside(x, y + 1)
                joint = ((ang - 9) % 18) < 2.2 and ang > 8 and not rim_o
                c = "ls5"
                if rim_o:
                    c = "ls6"
                elif rim_i:
                    c = "ls3"
                elif joint:
                    c = "ls2"
                elif ang < 8:     # the keystone, a shade brighter
                    c = "ls6" if y < spring - rise + 3 else "ls5"
                L.px(x, y, c)
            else:
                # the spandrel: the wall between the arches, in shadow
                yy = y - 4
                c = "ls3" if yy % 9 else "ls2"
                L.px(x, y, c)
    return inside


def recess(L, x0, w, inside, floor_y=44, shaft=False):
    """The bay behind an arch: a deep recess in shadow, faint courses in its back
    wall, its own floor at the bottom."""
    for y in range(4, 48):
        for x in range(x0, x0 + w):
            if not inside(x, y):
                continue
            if y >= floor_y:
                c = "ls3" if y == floor_y else "ls4"
            else:
                c = "ls1" if y < 26 else "ls2"
                if not shaft and y >= 26 and (y - 26) % 8 == 7:
                    c = "ls1"
            L.px(x, y, c)


def arcade():
    """The north wall's arcade: piers, 3- and 4-cell arches and their recesses."""
    s = Struct("arcade", "Walls: the vaulted arcade", 8, 3,
               walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX"], section="house",
               notes="The north wall of a vaulted room, three rows tall: a pier (column 0), "
                     "then a three-cell bay (columns 1-3) and its recess, and a pier with the "
                     "back door cut through it (column 4: the door is (4, 2), "
                     "MB_NON_ANIMATED_DOOR; put its warp there). Columns 5-7: the side walls' "
                     "cells (west, east) and a pier carrying a bronze sconce, lit, on its "
                     "lower face. Lay a wall as pier, bay, pier, bay... A four-cell bay is "
                     "`arch4`; the Icarus Shaft and the lift use their own bays.")
    L = s.B
    pier(L, 0)
    ins = arch(L, 16, 48)
    recess(L, 16, 48, ins)
    pier(L, 64, door=True)
    side_wall(L, 80, west=True, rows=3)
    side_wall(L, 96, west=False, rows=3)
    pier(L, 112)
    sconce(s.M, 112, 26, lit=True)
    s.walk = ["XXXXXXXX", "XXXXXXXX", "XXXXDXXX"]
    s.behaviors[(4, 2)] = "MB_NON_ANIMATED_DOOR"
    # the back door's leaves, ajar
    door_leaf(s.M, 64)
    s.names = {"pier": (0, 0), "bay_l": (1, 0), "bay_m": (2, 0), "bay_r": (3, 0),
               "door_pier": (4, 0), "side_w": (5, 0), "side_e": (6, 0), "pier_sconce": (7, 0)}
    return s


def side_wall(L, x0, west=True, rows=1, y0=0):
    """The west or east wall seen from above: its top, a lit rim on the room's
    side, and a dark line where it meets the floor."""
    for y in range(y0, y0 + rows * 16):
        for x in range(16):
            X = x if west else 15 - x
            if X < 11:
                c = "ls2"
                if (X * 5 + y * 3) % 61 == 0:
                    c = "ls1"
            elif X == 11:
                c = "ls4"
            elif X == 12:
                c = "ls6"
            elif X == 13:
                c = "ls5"
            elif X == 14:
                c = "ls3"
            else:
                c = "lk"
            L.px(x0 + x, y, c)


def sconce(M, x0, y, lit=True):
    """A bronze sconce on a pier's face with a clay lamp, lit or cold (fire group)."""
    rows = ["......f.........",
            ".....fcf........",
            ".....fyf........",
            "....fcycf.......",
            "...kfcyyfk......",
            "..kzZZZZZzk.....",
            "...kzZZZzk......",
            "....kzzzk.......",
            ".....kzk........",
            "......k........."] if lit else \
           ["................",
            "................",
            "................",
            "................",
            "...k.....k......",
            "..kzZZZZZzk.....",
            "...kzZZZzk......",
            "....kzzzk.......",
            ".....kzk........",
            "......k........."]
    legend = {"f": "ff0", "c": "ff1", "y": "ff3", "k": "ink", "z": "fz0", "Z": "fz2"}
    blit(M, rows, legend, x0 + 1, y - 6)


def door_leaf(M, x0):
    """The back door: a plain plank door of dark timber, bronze-studded, standing
    a hand's breadth ajar (timber)."""
    for y in range(24, 48):
        for x in range(3, 12):
            c = "tw1" if (x - 3) % 3 else "tw0"
            if y == 24:
                c = "tw2"
            M.px(x0 + x, y, c)
        M.px(x0 + 12, y, "ink")
    for y in (28, 40):
        for x in range(3, 12):
            M.px(x0 + x, y, "tw0")
        M.px(x0 + 4, y, "tx")
        M.px(x0 + 10, y, "tx")
    M.px(x0 + 10, 34, "tx")
    M.px(x0 + 10, 35, "tw0")


def arch4():
    s = Struct("arch4", "Walls: a four-cell bay", 4, 3, walk=["XXXX"] * 3, section="house",
               notes="A wider arch and recess for a four-cell bay, symmetric, for the middle "
                     "of a room. The Icarus Shaft is drawn in a bay of this shape.")
    ins = arch(s.B, 0, 64, rise=17)
    recess(s.B, 0, 64, ins)
    s.names = {"l": (0, 0), "ml": (1, 0), "mr": (2, 0), "r": (3, 0)}
    return s


def edges():
    s = Struct("edge", "Edges: side walls by the floor, the south threshold", 4, 1,
               walk=["X..X"], section="house",
               notes="(0), (3) the west and east walls beside the floor rows. (1), (2) the "
                     "threshold down to the rings, for the bottom row, two cells wide: "
                     "MB_SOUTH_ARROW_WARP, warps on both.")
    L = s.B
    side_wall(L, 0, west=True)
    side_wall(L, 48, west=False)
    # the threshold: a lit sill, then steps going down into the dark
    for x in range(16, 48):
        X = x - 16
        L.px(x, 0, "ls5")
        L.px(x, 1, "ls6")
        L.px(x, 2, "ls5")
        L.px(x, 3, "ls4")
        L.px(x, 4, "ls2")
        for y in range(5, 16):
            step = (y - 5) // 3
            c = ("ls3", "ls2", "ls1", "lk")[min(step, 3)]
            if (y - 5) % 3 == 0 and step < 3:
                c = ("ls4", "ls3", "ls2")[step]
            L.px(x, y, c)
        if X in (0, 31):
            for y in range(0, 16):
                L.px(x, y, "lk")
        if X in (1, 30):
            for y in range(3, 16):
                L.px(x, y, "ls1")
    s.behaviors[(1, 0)] = "MB_SOUTH_ARROW_WARP"
    s.behaviors[(2, 0)] = "MB_SOUTH_ARROW_WARP"
    s.names = {"wall_w": (0, 0), "sill_l": (1, 0), "sill_r": (2, 0), "wall_e": (3, 0)}
    return s


# --------------------------------------------------------------------------
# The sheet
# --------------------------------------------------------------------------

# The Labyrinth is two secondaries (LABYRINTH.md §11 planned one; it outgrew 504
# tiles): gTileset_Labyrinth for the outer rings, the workshop, Minos's tomb and
# the Icarus Shaft, and gTileset_Mychos ("the innermost part of a house") for the
# Titan wing, the Choros and the Starry Chamber. Both draw the same house and
# thread sections at the same rows, so those metatile ids are the same in both.
#
# (first sheet row, section key, title, blurb). Each section starts on a fixed
# row of the 8-wide sheet, so adding to one never renumbers another.
HOUSE = (0, "house", "The house: floors and walls",
         "The masonry every map of the Labyrinth shares, the same at the same ids in "
         "`labyrinth` and `mychos`: the workshop's slab floor, the vaulted arcade, the side "
         "walls and the threshold; the rings' corridor walls (an autotile), the bronze anchor "
         "rings and the stairs from ring to ring.")
THREAD = (36, "thread", "The rings' floor and Ariadne's thread",
          "The floor every ring is laid with, and its thread twins (LABYRINTH.md §5.1, "
          "ENGINE_API.md §6), the same at the same ids in both tilesets.")
SECTIONS = {
    # LABYRINTH_MAZE.md (2026-11-17): Rings I-IV are built into the karst, so
    # `labyrinth` trades the workshop (now `daidaleion`) and Ring V (now mychos)
    # for the cave and Ring IV's Titan fixtures.
    "labyrinth": [
        HOUSE,
        (13, "cave", "The cave the house was cut into",
         "The karst under Knossa (LABYRINTH_MAZE.md §1, §4): the cave rock as an autotile, "
         "the earth and gravel floors and the beam bridges with their thread twins, the "
         "underground stream, the chasm, and the breach where ashlar breaks into rock."),
        THREAD,
        (39, "rings", "Rings I to IV, and Minos's tomb",
         "Ring I's braziers and hearth, Ring II's herald plate and gates, cracked walls, "
         "Ring III's webs and glow-marks, the cave's formations, Ring IV's Titan fixtures, "
         "the labrys seals and doorways, niches; then Minos's tomb."),
    ],
    "daidaleion": [
        HOUSE,
        (13, "workshop", "Daedalus's workshop",
         "The hub at the end of Ring III (LABYRINTH.md §6, scenes D and L)."),
        (36, "shaft", "The Icarus Shaft",
         "The natural chimney above the workshop, foot to mouth (scene L), lit by the dawn set."),
    ],
    "mychos": [
        HOUSE,
        (13, "titans", "The Titan wing: Rings IV and VI",
         "Team Titan's quarters: the barracks, the mess hall, the sentry posts, the forge, "
         "the Hall of Dials, the archive, the vault and the Mistress's shrine."),
        THREAD,
        (39, "choros", "Ring VII: the Choros",
         "Starlit marble, the mirrors' beam and the dancing floor (LABYRINTH.md §5.7)."),
        (52, "heart", "The heart: the Starry Chamber",
         "The black lustral pool under Daedalus's star-clock (LABYRINTH.md §6, scene J)."),
    ],
}
SHEET_ROWS = 64       # 512 metatiles in a secondary
# Sections the catalog lists on their own though they pack inside another's rows.
SUBSECTIONS = {
    "deep": ("rings", "Minos's tomb", "The tomb behind Ring V's cracked wall (scene F)."),
    "formations": ("rings", "The cave's formations",
                   "Stalagmites, columns, boulders, roof-fall, ledges and the hole down, on "
                   "the cave's earth (cave_dark's, recolored)."),
    "titans": ("rings", "Ring IV: the Titan wing",
               "Team Titan's first quarters: bunks, the mess table, the helmet locker, the "
               "armory, oil lamps, sickle banners, and the fresco of the dance's steps 1-3."),
}


def pack(sections):
    """First-fit each section's structures into the 8-wide sheet, in build order,
    from the section's first row; a section may not run into the next section's
    first row. Adding a structure never moves one placed before it. Returns the
    rows used."""
    starts = sorted([r for r, _ in sections] + [SHEET_ROWS])
    total = 0
    for start, structs in sections:
        end = min(r for r in starts if r > start)
        used = np.zeros((end - start, 8), bool)
        for s in structs:
            spot = None
            for row in range(0, end - start - s.h + 1):
                for col in range(0, 8 - s.w + 1):
                    if not used[row:row + s.h, col:col + s.w].any():
                        spot = (col, row)
                        break
                if spot:
                    break
            assert spot, f"section at row {start} is full: no room for {s.key} ({s.w}x{s.h})"
            col, row = spot
            used[row:row + s.h, col:col + s.w] = True
            s.origin = (col, start + row)
            s.ids = [[0x200 + (start + row + y) * 8 + col + x for x in range(s.w)]
                     for y in range(s.h)]
        rows_used = int(np.nonzero(used.any(1))[0].max()) + 1 if used.any() else 0
        total = max(total, start + rows_used)
    return total


def build(tileset="labyrinth"):
    """[(first row, [structures])] for one of the tilesets, section by section in
    SECTIONS order."""
    import labyrinth_kit as KIT
    house = [floors(), arcade(), arch4(), edges()] + KIT.house_kit()
    out = {"house": house, "thread": KIT.thread_floors()}
    if tileset == "labyrinth":
        import labyrinth_rings
        import labyrinth_deep
        import labyrinth_cave
        import labyrinth_titans
        out["cave"] = labyrinth_cave.build()
        tomb = labyrinth_deep.tomb()
        for s in tomb:
            s.subsection = "deep"
        forms = labyrinth_cave.formations()
        for s in forms:
            s.subsection = "formations"
        titans = labyrinth_titans.build()
        for s in titans:
            s.subsection = "titans"
        out["rings"] = order_for_packing(labyrinth_rings.build() + forms + titans + tomb)
    elif tileset == "daidaleion":
        import labyrinth_deep
        out["workshop"] = workshop_pieces()
        out["shaft"] = [labyrinth_deep.icarus()]
    else:
        import mychos_titans
        import mychos_heart
        out["titans"] = mychos_titans.build()
        out["choros"] = mychos_heart.choros()
        out["heart"] = mychos_heart.heart()
    secs = []
    for row, key, *_ in SECTIONS[tileset]:
        ss = out[key]
        for s in ss:
            s.section = getattr(s, "subsection", None) or key
            finish(s)
        secs.append((row, ss))
    return secs


def groups_for(tileset):
    """The palette groups a tileset draws from (seven at most: palettes 6-12)."""
    if tileset == "labyrinth":
        import labyrinth_cave
        g = {k: v for k, v in GROUPS.items() if k not in ("night", "stone")}
        return {"stone": labyrinth_cave.GROUPS["stone"], **g, "cave": labyrinth_cave.GROUPS["cave"]}
    if tileset == "daidaleion":
        return {k: v for k, v in GROUPS.items() if k != "night"}
    return GROUPS


def order_for_packing(structs):
    """Largest first (first-fit packs tighter), keeping each odd twin right after
    its even twin; ties keep build order."""
    groups = []
    for s in structs:
        if s.key.endswith("_odd") and groups and groups[-1][0].key == s.key[:-4]:
            groups[-1].append(s)
        else:
            groups.append([s])
    groups.sort(key=lambda g: (-g[0].h, -g[0].w))
    return [s for g in groups for s in g]


def workshop_pieces():
    import labyrinth_workshop
    return labyrinth_workshop.build()


def write_catalog(tileset, used, structs):
    import labyrinth_catalog
    labyrinth_catalog.main(tileset, used, structs)
