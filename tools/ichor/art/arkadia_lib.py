"""Shared toolkit for Arkadia's two secondaries (SCRIPT.md Part 10, Arkadia).

  gTileset_Arkadia      the town: cypresses in four shapes, the lamp-trees (unlit
                        and lit), timber-and-stone houses with shingle roofs on
                        terraces, every building's outside, the temple hill and
                        its waterfall cliff, Pan's grotto, the old racecourse.
  gTileset_ArkadiaWood  the Cypress Wood and the Pool of Mnemosyne: the close-knit
                        canopy over a floor in deep shade, the stump clearing under
                        the stars, the Tomb of Kallisto, the Pool's black water,
                        white poplars and asphodel.

Both pair with the aethos primary. They draw with the kithairon lineage's layers,
structures, soft-shape engine, validation and tile merging (kithairon_lib, which
brings agros_lib and eleusa_lib), and add Arkadia's colors and palette groups.
Every 8x8 tile of every layer takes all its colors from one group of its set.

The Wood is a separate secondary because one set's 504 tiles can't hold a town,
a dark forest and a sacred pool (batch 1's rooms and crossing split the same
way). The Wood is entered by a gate warp, so no seam joins the two sets.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_lib as K  # noqa: E402  (registers agros's, Eleusa's and Kithairon's colors)
from kithairon_lib import Layer, Struct, aethos  # noqa: E402,F401

ROOT = K.ROOT
E = K.E
A = K.A

# --------------------------------------------------------------------------
# Colors (new names start with a letter pair no other set uses)
# --------------------------------------------------------------------------

NEW = {
    # the cypresses: near-black blue-green to the lit tips
    "ac0": (16, 32, 40), "ac1": (24, 56, 48), "ac2": (48, 88, 64), "ac3": (80, 120, 80),
    "ac4": (136, 168, 104),
    # clay lamps, and their glow
    "al0": (152, 80, 48), "al1": (232, 136, 48), "al2": (248, 208, 96), "al3": (248, 248, 216),
    # houses: grey stone footings, dark timber, weathered shingles, daub, a red door
    "as0": (56, 56, 64), "as1": (104, 96, 96), "as2": (152, 144, 136), "as3": (200, 192, 176),
    "at0": (48, 32, 24), "at1": (96, 64, 40), "at2": (144, 104, 64),
    "ah0": (48, 40, 40), "ah1": (96, 72, 56), "ah2": (136, 104, 80), "ah3": (184, 152, 112),
    "ap0": (224, 208, 176), "ad0": (128, 48, 40),
    # rock extras: moss, a glint, spring water
    "ar0": (80, 104, 56), "ar1": (248, 232, 136), "ar2": (112, 168, 208),
    # marble, silver and the temple's roof
    "am1": (232, 232, 224), "am2": (200, 200, 192), "am3": (152, 152, 160), "am4": (104, 104, 120),
    "av0": (96, 112, 152), "av1": (168, 184, 216), "av2": (216, 224, 248), "ab0": (32, 48, 104),
    # the town: packed earth, awnings, smoke
    "ae0": (112, 80, 56), "ae1": (160, 120, 80), "ae2": (200, 168, 120),
    "af0": (232, 176, 48), "af1": (176, 56, 40), "ak0": (112, 112, 120), "ak1": (176, 176, 184),
    # the Wood: the floor in deep shade, the canopy, ferns, bark, starlight, embers
    "wf0": (16, 24, 24), "wf1": (32, 40, 32), "wf2": (48, 56, 40), "wf3": (72, 72, 48),
    "wc0": (8, 16, 24), "wc1": (16, 32, 40), "wc2": (32, 64, 56), "wc3": (64, 96, 72),
    "wn0": (48, 88, 56), "wn1": (88, 128, 64), "wb0": (80, 64, 56),
    "ws0": (88, 104, 128), "ws1": (144, 160, 184), "ws2": (208, 216, 232),
    # white poplars, asphodel, the Pool's black water
    "pw0": (176, 176, 168), "pw1": (232, 232, 224), "pk0": (72, 72, 80),
    "pg0": (88, 120, 96), "pg1": (144, 168, 144), "pg2": (200, 216, 192),
    "pa0": (240, 224, 232), "pa1": (184, 144, 176),
    "pb0": (8, 8, 24), "pb1": (16, 24, 48), "pb2": (40, 48, 80),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

TOWN_GROUPS = {
    # the cypresses and the lamp-trees, on grass
    "tree": GRASS4 + ["ac0", "ac1", "ac2", "ac3", "ac4", "k1", "ink", "al0", "al1", "al2", "al3"],
    # timber-and-stone houses, shingle roofs, daub, a lit window, a red door
    "house": ["ink", "as0", "as1", "as2", "as3", "at0", "at1", "at2", "ah0", "ah1", "ah2", "ah3",
              "ap0", "al2", "ad0"],
    # rock (Kithairon's grey limestone, so the climb and the town match), moss,
    # a cave's dark, a glint, the spring
    "rock": GRASS4 + ["rk0", "rk1", "rk2", "rk3", "rk4", "rk5", "ink", "ar0", "cv", "ar1", "ar2"],
    # the Temple of Artemis: marble, silver, the roof, the night-blue frieze
    "sacred": ["ink", "w0", "am1", "am2", "am3", "am4", "av0", "av1", "av2", "tc0", "tc1", "tc2",
               "ab0", "rk1", "rk3"],
    # the racecourse, the Agora's awning, nets, fences, the kiln and its smoke
    "town": GRASS4 + ["ae0", "ae1", "ae2", "at1", "at2", "af0", "af1", "ak0", "ak1", "ink", "al1"],
}

WOOD_GROUPS = {
    # the floor in deep shade, the canopy, ferns, bark, starlight and embers
    "forest": ["wf0", "wf1", "wf2", "wf3", "wc0", "wc1", "wc2", "wc3", "wn0", "wn1", "wb0",
               "ws0", "ws1", "al1", "ws2"],
    # the tomb: earth, old stones, the little marble shrine, moss, bark
    "tomb": ["wf0", "wf1", "wf2", "wf3", "rk1", "rk2", "rk3", "rk4", "am1", "am3", "wb0", "ar0",
             "ws1", "av1", "ink"],
    # the canopy over grass (the Pool's glade edge), with its shadow
    "canopy": GRASS4 + ["wc0", "wc1", "wc2", "wc3", "wb0", "wf1", "ws0", "ink", "ac3", "ac4",
                        "wf2"],
    # white poplars, asphodel, the stone seat, on grass
    "glade": GRASS4 + ["pw0", "pw1", "pk0", "pg0", "pg1", "pg2", "pa0", "pa1", "rk3", "rk4",
                       "ink"],
    # the Pool's black water, its stars and its kerb of pale stones
    "pool": GRASS4 + ["pb0", "pb1", "pb2", "w0", "av1", "rk2", "rk3", "rk4", "rk5", "ink"],
}

for _groups in (TOWN_GROUPS, WOOD_GROUPS):
    assert len(_groups) <= 7
    for g, names in _groups.items():
        assert len(names) <= 15, (g, len(names))
        assert len(set(C[n] for n in names)) == len(names), g
        for n in names:
            assert n in C, n
TOWN_RGB = {g: {C[n] for n in names} for g, names in TOWN_GROUPS.items()}
WOOD_RGB = {g: {C[n] for n in names} for g, names in WOOD_GROUPS.items()}

GROUND_METATILE = K.GROUND_METATILE        # grass 0x001, path 0x1D9, tall 0x00D, shade 0x01C
struct = K.struct
ground = K.ground
put = K.put
blob_key = K.blob_key
hsh = K.hsh


def validate_town(structs):
    return E.validate(structs, TOWN_RGB)


def validate_wood(structs):
    return E.validate(structs, WOOD_RGB)


def grass_px(x, y):
    """aethos grass's color name at (x, y), phase-locked to the 16 px grid."""
    g = aethos(K.GRASS)
    return A.RGB2NAME[tuple(int(v) for v in g[y % 16, x % 16])]


def shade_grass_px(L, x, y):
    """Darken a grass pixel already drawn on L (a cast shadow)."""
    c = L.get(x, y)
    L.px(x, y, {"g3": "g1", "g2": "g1", "g1": "gd"}.get(c, c))


# --------------------------------------------------------------------------
# Cypresses
# --------------------------------------------------------------------------

RAMP_TOWN = ("ac0", "ac1", "ac2", "ac3", "ac4")
RAMP_WOOD = ("wc0", "wc1", "wc2", "wc3", "wc3")


def cypress_mask(w, h, cx, top, base, hw, belly=0.66, lean=0.0, wobble=1.0, seed=1):
    """A cypress's silhouette: a flame narrowing to a point at `top`, widest
    (half-width `hw`) a `belly` of the way down, a little narrower at `base`.
    `lean` shifts the crown sideways by that many pixels at the top."""
    m = np.zeros((h, w), bool)
    span = max(1, base - top)
    for y in range(max(0, top), min(h, base + 1)):
        t = (y - top) / span                    # 0 at the tip, 1 at the base
        if t < belly:
            r = hw * math.sin(t / belly * math.pi / 2) ** 0.85
        else:
            r = hw * (1 - 0.18 * (t - belly) / (1 - belly))
        r += wobble * 0.9 * math.sin(y * 0.9 + seed) * min(1.0, t * 3)
        c = cx + lean * (1 - t)
        x0, x1 = int(round(c - r)), int(round(c + r))
        for x in range(max(0, x0), min(w, x1 + 1)):
            m[y, x] = True
    return m


def paint_foliage(L, mask, ramp=RAMP_TOWN, cx=None, seed=3, outline=True):
    """Fill a cypress mask with layered sprays: lit on the left, shadowed on the
    right, with short dark sprays between the flames of foliage."""
    h, w = mask.shape
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return
    if cx is None:
        cx = (xs.min() + xs.max()) / 2
    k0, k1, k2, k3, k4 = ramp
    for y, x in zip(ys, xs):
        row = np.nonzero(mask[y])[0]
        left, right = row.min(), row.max()
        rw = max(1, right - left)
        u = (x - left) / rw                      # 0 at the left edge, 1 at the right
        # sprays: short diagonal strokes, 6 px apart, offset each row band
        band = (y + seed) // 5
        spray = (x * 2 + y + band * 3 + seed) % 7
        if u < 0.28:
            col = k3 if spray > 1 else k2
            if spray == 4 and (y + x) % 3 == 0:
                col = k4
        elif u < 0.62:
            col = k2 if spray > 1 else k1
            if spray == 5 and (y % 4 == 0):
                col = k3
        else:
            col = k1 if spray > 2 else k0
        if (y + seed) % 5 == 0 and spray in (0, 1):
            col = k1 if u < 0.62 else k0
        L.px(int(x), int(y), col)
    if outline:
        pad = np.pad(mask, 1)
        edge = mask & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        for y, x in np.argwhere(edge):
            row = np.nonzero(mask[y])[0]
            lit = x <= (row.min() + row.max()) / 2 - 2
            L.px(int(x), int(y), k1 if lit and (y % 3) else k0)


def trunk(L, cx, y0, y1, bark="k1", dark="ink"):
    """A short trunk, 3 px wide, under the crown."""
    for y in range(y0, y1 + 1):
        L.px(cx - 1, y, dark)
        L.px(cx, y, bark)
        L.px(cx + 1, y, dark)


def grass_shadow(L, cx, cy, rx, ry):
    """An elliptical cast shadow on grass already drawn on L."""
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                if 0 <= x < L.w and 0 <= y < L.h and L.get(x, y) is not None:
                    shade_grass_px(L, x, y)


def lamp(L, x, y, lit, chain=4):
    """A clay lamp hung on a chain: (x, y) is the chain's top. 5 px wide."""
    for j in range(chain):
        L.px(x + 2, y + j, "ink" if j % 2 else "k1")
    by = y + chain
    if lit:
        # the halo first, then the lamp glowing through it
        for (dx, dy) in ((-1, 1), (5, 1), (-1, 2), (5, 2), (0, 0), (4, 0), (0, 4), (4, 4), (1, -1),
                         (3, -1), (1, 5), (3, 5), (2, 6), (-1, 3), (5, 3)):
            L.px(x + dx, by + dy, "al1")
        L.blit([" 222 ", "23332", "23332", " 222 ", "  1  "],
               {"1": "al1", "2": "al2", "3": "al3"}, x, by)
    else:
        L.blit([" 000 ", "0kkk0", "0aaa0", " 000 "],
               {"0": "ink", "k": "k1", "a": "al0"}, x, by)


# --------------------------------------------------------------------------
# The canopy: a mass of cypress crowns, as a soft blob region
# --------------------------------------------------------------------------

CANOPY_FOOT = 5          # px of trunks and shade at the mass's south edge
SPIRE = 8                # spire spacing along its north edge


def canopy_fields(key):
    """V: the canopy's extent around the cell (48 x 48, the cell in the middle);
    foot: the trunk band along its south edge."""
    V = K.soft(key, margin=0.0, radius=2.5, amp=1.0, seed=2.7, jag=0.0)
    # spires along the north edge: each column keeps its top only where a spire stands
    up = np.zeros((48, 48), int)
    for x in range(48):
        run = 0
        for y in range(48):
            run = run + 1 if V[y, x] else 0
            up[y, x] = run
    tri = np.array([abs(((x + 2) % SPIRE) - SPIRE / 2) for x in range(48)])   # 0 at a spire
    cut = (up <= np.round(tri * 1.4)[None, :]) & V
    # only cut where the north really is open (not where V continues upward off-canvas)
    V2 = V & ~cut
    V2[:16] = V[:16] & ~cut[:16]
    down = np.zeros((48, 48), int)
    for x in range(48):
        run = 0
        for y in range(47, -1, -1):
            run = run + 1 if V2[y, x] else 0
            down[y, x] = run
    foot = V2 & (down <= CANOPY_FOOT)
    return V2, foot


def crown_texture(x, y, ramp):
    """Interlocking cypress crowns seen from above: flames 8 px apart, each lit on
    its left, staggered by half a flame every other column. 32 px periodic."""
    k0, k1, k2, k3, k4 = ramp
    xx, yy = x % 32, y % 32
    col = xx // 8
    fx = xx % 8
    fy = (yy + (col % 2) * 8 + (col // 2) * 4) % 16
    # each flame: a point at fy 0, widest at fy 10
    half = [0.5, 1, 1.5, 2, 2.5, 3, 3.2, 3.5, 3.7, 3.9, 4, 4, 3.8, 3.5, 3.0, 2.5][fy]
    d = fx - 3.5
    if abs(d) > half:
        return k0 if fy > 11 or abs(d) > half + 1 else k1
    if d < -half + 1.2:
        return k3 if (fy + fx) % 5 else k4
    if d > half - 1.2:
        return k1
    return k2 if (fx * 3 + fy) % 7 else k3


def paint_canopy_cell(B, M, ox, oy, key, ramp, floor=None, bark="k1", shadow="grass", dark="ink"):
    """One canopy cell. With `floor` (a color function), the floor is painted in
    B and the canopy in M over it; without, B stays empty (borrowed ground) and
    M holds only the canopy and its shadow."""
    V, foot = canopy_fields(key)
    c = np.s_[16:32, 16:32]
    v, f = V[c], foot[c]
    if floor:
        for y in range(16):
            for x in range(16):
                B.px(ox + x, oy + y, floor(x, y))
    # the shadow on the ground just below the mass and beside its foot
    below = np.zeros((48, 48), bool)
    for d in (1, 2, 3):
        below[d:] |= V[:-d]
    below &= ~V
    side = K.halo(V) & ~V
    for y, x in np.argwhere((below[c] | side[c]) & ~v):
        if shadow == "grass":
            M.px(ox + x, oy + y, "gd" if (x + y) % 2 == 0 or below[y + 16, x + 16] else None)
        else:
            M.px(ox + x, oy + y, shadow if (x + y) % 2 == 0 else None)
    k0 = ramp[0]
    for y in range(16):
        for x in range(16):
            if not v[y, x]:
                continue
            X, Y = ox + x, oy + y
            if f[y, x]:
                # the dark under the crowns, with trunks every 6-8 px
                tx = (x + 3 * ((y + 16) // 16)) % 7
                M.px(X, Y, bark if tx == 0 else (dark if tx == 1 else k0))
            else:
                M.px(X, Y, crown_texture(x, y, ramp))
    # an outline of the darkest green where the mass meets the open floor
    ring = K.ring(V)[c] & v & ~f
    for y, x in np.argwhere(ring):
        if not V[y + 15, x + 16]:          # north edge: catch the light on the tips
            M.px(ox + x, oy + y, ramp[1])
        else:
            M.px(ox + x, oy + y, k0)


def wanted(kind, shapes):
    """The shape keys a set must hold: the maps' list for `kind`, interior first."""
    keys = list(shapes.get(kind) or [])
    full = "1|11111111"
    if not keys:
        keys = K.blob_keys()
    if full in keys:
        keys.remove(full)
    return [full] + keys


def mirror_cells(s, ln="middle"):
    """Make a structure exactly left-right symmetric (its right half becomes the
    mirror of its left half), so Porytiles stores the halves once."""
    L = s.layers[ln]
    w = s.w * 16
    half = w // 2
    L.a[:, w - half:] = L.a[:, :half][:, ::-1]


def mirrored(s, key, title, notes=None):
    """s flipped left to right as a new structure: new metatiles, but its tiles
    are s's flipped, which Porytiles stores once."""
    t = Struct(key, title, s.w, s.h, s.section, walk=[r[::-1] for r in s.walk],
               notes=notes if notes is not None else s.notes,
               names={n: (s.w - 1 - x, y) for n, (x, y) in s.names.items()})
    for ln in ("bottom", "middle", "top"):
        t.layers[ln].a[:] = s.layers[ln].a[:, ::-1]
    t.behaviors = {(s.w - 1 - x, y): mb for (x, y), mb in s.behaviors.items()}
    t.ground = {(s.w - 1 - x, y): g for (x, y), g in getattr(s, "ground", {}).items()}
    return t
