"""The Arkadian climb's ground: grass, roads, the gorge's limestone and its
cliff faces, the Styx's black rock, white water, still black water.

Soft sets hold one piece per blob shape key (kithairon_lib.blob_keys); the
map builder (tools/ichor/maps/heights.py --shapes) lists the keys its maps use
in heights_shapes.json, and only those are drawn.

  tall        barley tall grass on aethos grass (agros's painter): MB_TALL_GRASS
  meadow_tall Kyllene's wind-combed grass, gentians in it: MB_TALL_GRASS
  path        the limestone road (agros's painter)
  rock        the gorge's limestone seen from above: plateaus, buttresses, the
              far wall. Where nothing of the rock lies south of a cell it shows
              a short face of its own; where a cliff face (`face`) continues
              below, the top runs flush to the cell's foot.
  face        the tall cliff faces: one piece per (lip, foot, open west, open
              east) shape, so a face band 1-4 rows tall and any width stacks:
              its top row carries the lip (grass or rock above it), its bottom
              row the dark foot and rubble.
  black, bface  the same for the Styx's black rock (no ferns: nothing grows)
  water       a still pool on aethos's animated sea, a gravel bank: MB_POND_WATER
  blackpool   the Styx's pool: still black water, obols on the bottom, no
              ripples. MB_POND_WATER (a rod gets "Not even a nibble")
  gravel      a walkable gravel bank (the river spur)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import agros_ground
import heights_lib as H

SEC = "ground"
SHAPES = Path(__file__).resolve().parent / "heights_shapes.json"
LOWFACE = 11      # a rock top's own short south face, in pixels
GREY = ("qr0", "qr1", "qr2", "qr3", "qr4", "qr5")
BLACK = ("qb0", "qb1", "qb2", "qb3", "qb4", "qm0")
TO_BLACK = dict(zip(GREY, BLACK))


def wanted(kind, default=None):
    """The shape keys a set must hold (heights_shapes.json), or a default."""
    if SHAPES.exists():
        data = json.loads(SHAPES.read_text())
        if kind in data and data[kind]:
            keys = list(data[kind])
            full = "1|11111111"
            if full in keys:
                keys.remove(full)
                keys.insert(0, full)
            return keys
    if default is not None:
        return list(default)
    keys = H.K.blob_keys()
    keys.remove("1|11111111")
    return ["1|11111111"] + keys


# --------------------------------------------------------------------------
# Tall grass, the road, Kyllene's meadow
# --------------------------------------------------------------------------

def tall():
    return H.shape_set("tall", "Tall grass with soft edges", SEC, wanted("tall"),
                       lambda s, ox, oy, k: agros_ground.paint_tall(s.B, ox, oy, k), "G",
                       "Barley tall grass on aethos grass, cut from one field so any outline "
                       "works (agros's painter, as on Route 1). MB_TALL_GRASS. Names are blob "
                       "shape keys (`1|NNEESESSWWNW`).", behavior="MB_TALL_GRASS")


def path():
    return H.shape_set("path", "The road with soft edges", SEC, wanted("path"),
                       lambda s, ox, oy, k: agros_ground.paint_path(s.B, ox, oy, k), ".",
                       "The limestone road, scalloped where it meets the grass (agros's "
                       "painter). Names are blob shape keys.")


def combed(x, y):
    """Kyllene's grass, combed by the wind toward the east: 16 px periodic.
    Blades lean right in diagonal strokes; silver tips catch the light."""
    xx, yy = x % 16, y % 16
    # strokes: each blade a short diagonal run, offset per row band
    band = yy // 4
    phase = (xx - yy // 2 + band * 5) % 8
    h = H.hsh(xx, yy, 31) % 100
    if phase == 0:
        return "qg0"
    if phase == 1:
        return "qg1"
    if phase in (2, 3):
        return "qg3" if (yy % 4 == 0 and h < 70) else "qg2"
    if phase == 7:
        return "qg1"
    return "qg2" if h < 55 else "qg1"


FLOWERS = [(3, 5, "qf1"), (11, 2, "qf2"), (7, 12, "qf1"), (14, 9, "w0"), (1, 14, "qy")]


def paint_meadow_tall(L, ox, oy, key):
    vis, _ = agros_ground.visible(key, margin=1.0, radius=3.0, amp=1.4, seed=6.7, jag=1.0)
    L.texture(H.GRASS, ox, oy, 16, 16)
    for y, x in np.argwhere(vis):
        L.px(ox + x, oy + y, combed(x, y))
    for (fx, fy, c) in FLOWERS:
        if vis[fy, fx] and (fy == 0 or vis[fy - 1, fx]):
            L.px(ox + fx, oy + fy, c)
            if fy + 1 < 16 and vis[fy + 1, fx]:
                L.px(ox + fx, oy + fy + 1, "qg0")
    for y, x in np.argwhere(agros_ground.ring(vis)):
        L.px(ox + x, oy + y, "qg0" if (x + y) % 3 else "qg1")
    # combed tips leaning out of the clump's top edge, to the east
    for y, x in np.argwhere(agros_ground.halo(vis)):
        if y + 1 < 16 and vis[y + 1, x] and (x * 5 + y * 3) % 6 == 0 and x + 1 < 16:
            L.px(ox + x, oy + y, "qg2")
            if y - 1 >= 0 and not vis[y - 1, x + 1]:
                L.px(ox + x + 1, oy + y - 1, "qg3")


def meadow_tall():
    return H.shape_set("meadow_tall", "Kyllene's wind-combed grass", SEC, wanted("meadow_tall"),
                       lambda s, ox, oy, k: paint_meadow_tall(s.B, ox, oy, k), "G",
                       "Mount Kyllene's high meadow grass, combed east by the wind, with "
                       "gentians and crocus in it: the climb's own tall grass. MB_TALL_GRASS. "
                       "Names are blob shape keys.", behavior="MB_TALL_GRASS")


# --------------------------------------------------------------------------
# The gorge's limestone: rock tops and their cliff faces
# --------------------------------------------------------------------------

def rock_top(x, y, ramp=GREY):
    """The limestone seen from above: weathered, with sparse pits and a faint
    bedding grain that runs east-west. Plain, so its 16 px repeat doesn't show."""
    xx, yy = x % 16, y % 16
    h = H.hsh(xx, yy, 17) % 100
    if (xx, yy) in ((2, 5), (10, 12), (13, 3), (6, 9)):
        return ramp[1]
    if (xx, yy) in ((2, 4), (10, 11), (13, 2), (6, 8), (7, 8)):
        return ramp[4]
    if yy in (6, 14) and (xx * 3 + yy) % 5 < 3:
        return ramp[2]
    if h < 8:
        return ramp[2]
    if h > 95:
        return ramp[4]
    return ramp[3]


_SWAY = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# per variant: two inner seams (start x, and a row where each jogs one pixel),
# and the bedding ledge's row
_VARIANTS = [((6, 4), (11, 9), 10), ((5, 12), (10, 3), 6), ((7, 7), (12, 13), 12)]


def _facet(xx, yy, variant=0):
    """Which facet of the face a pixel is on, and where across it (0..1).
    Three facets per 16 px; the seam at x=0 is shared by every variant so they
    sit side by side, the inner two differ."""
    (s1, j1), (s2, j2), _ = _VARIANTS[variant]
    b0 = _SWAY[yy] % 16
    b1 = s1 + (1 if yy >= j1 else 0)
    b2 = s2 + (-1 if yy >= j2 else 0)
    bounds = sorted([b0, b1, b2])
    for i in range(3):
        a, b = bounds[i], bounds[(i + 1) % 3] + (16 if i == 2 else 0)
        xv = xx if xx >= a else xx + 16
        if a <= xv < b:
            return i, (xv - a) / max(1, b - a), xv - a, b - xv - 1
    return 0, 0.5, 2, 2


def face_px(x, y, ramp=GREY, ferns=True, variant=0):
    """The cliff face: broad facets lit on their left and shaded on their
    right, split by seams, with one broken bedding ledge. 16 px periodic both
    ways, so a face of any height tiles; three variants mix along a band."""
    xx, yy = x % 16, y % 16
    i, t, from_l, from_r = _facet(xx, yy, variant)
    h = H.hsh(xx, yy, 23 + variant) % 100
    # one bedding ledge, broken: a lit lip over a dark undercut
    ledge = _VARIANTS[variant][2] + (1 if xx in (3, 4, 5, 12) else 0) - (1 if xx in (8, 9) else 0)
    if yy == ledge and i != 1:
        return ramp[4] if h < 80 else ramp[3]
    if yy == ledge + 1 and i != 1:
        if ferns and xx in (4, 13):
            return "qv1"
        return ramp[0] if from_l == 0 or from_r == 0 else ramp[1]
    if ferns and yy == ledge - 1 and i != 1 and xx in (4, 13):
        return "qv2"
    if from_l == 0:
        return ramp[0]                     # the seam
    if from_l == 1:
        return ramp[4] if yy % 5 else ramp[3]   # the facet's lit edge
    if from_r == 0:
        return ramp[1]
    if t < 0.4:
        c = ramp[3]
    elif t < 0.75:
        c = ramp[2]
    else:
        c = ramp[1] if (yy + xx) % 3 else ramp[2]
    if h < 7:
        return ramp[1]
    if h > 94 and t < 0.6:
        return ramp[4]
    return c


def paint_rock_cell(L, ox, oy, key, ramp=GREY, floor=None, ferns=True):
    """A rock top cell (after kithairon_ground.paint_crag_cell), with a short
    south face where the rock ends and a shadow on the grass round it."""
    floor = floor or H.grass_px
    V = H.soft(key, margin=0.0, radius=3.0, amp=1.2, seed=4.9, jag=0.5)
    T = np.zeros_like(V)
    T[:-LOWFACE] = V[LOWFACE:]
    T &= V
    F = V & ~T
    c = np.s_[16:32, 16:32]
    v, f = V[c], F[c]
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, floor(x, y))
    sh = H.halo(V)[c]
    below = np.zeros((48, 48), bool)
    below[1:] = V[:-1] & ~V[1:]
    below2 = np.zeros((48, 48), bool)
    below2[2:] = V[:-2] & ~V[2:] & ~V[1:-1]
    for y, x in np.argwhere((sh | below[c] | below2[c]) & ~v):
        cur = L.get(ox + x, oy + y)
        L.px(ox + x, oy + y, {"g3": "g1", "g2": "g1", "g1": "gd"}.get(cur, cur))
    depth = np.zeros((48, 48), int)
    for x in range(48):
        run = 0
        for y in range(48):
            if F[y, x]:
                depth[y, x] = run
                run += 1
            else:
                run = 0
    for y in range(16):
        for x in range(16):
            if not v[y, x]:
                continue
            if f[y, x]:
                d = depth[y + 16, x + 16]
                if d == 0:
                    col = ramp[5] if x % 4 else ramp[4]
                elif d >= LOWFACE - 2:
                    col = ramp[0] if d == LOWFACE - 1 else ramp[1]
                else:
                    col = face_px(x, d + 1, ramp, ferns)
            else:
                col = rock_top(x, y, ramp)
            L.px(ox + x, oy + y, col)
    r = H.ring(T)[c]
    for y, x in np.argwhere(r & T[c]):
        N = not T[y + 15, x + 16]
        W = not T[y + 16, x + 15]
        Ee = not T[y + 16, x + 17]
        if N or W:
            L.px(ox + x, oy + y, ramp[5] if (x + y) % 3 else ramp[4])
        elif Ee:
            L.px(ox + x, oy + y, ramp[1])
            if x - 1 >= 0 and T[y + 16, x + 15]:
                L.px(ox + x - 1, oy + y, ramp[2])     # a steep east side: a thicker shade
    for y, x in np.argwhere(H.ring(V)[c] & v):
        if not T[y + 16, x + 16] and depth[y + 16, x + 16] < LOWFACE - 1:
            L.px(ox + x, oy + y, ramp[1])
        elif L.get(ox + x, oy + y) != ramp[5]:
            L.px(ox + x, oy + y, ramp[1] if T[y + 16, x + 16] else ramp[0])


def face_key(lip, foot, wopen, eopen, variant=0):
    return f"{lip}{'f' if foot else '-'}{'w' if wopen else '-'}{'e' if eopen else '-'}{variant}"


ALL_FACES = [face_key(l, f, w, e, v) for l in "gr-" for f in (0, 1) for w in (0, 1) for e in (0, 1)
             for v in range(3)]


def paint_face_cell(L, ox, oy, key, ramp=GREY, ferns=True, floor=None):
    """One cliff-face cell. key: lip ('g' grass above, 'r' rock above, '-' face
    above), 'f' its foot (nothing of the face below), 'w'/'e' an open side."""
    floor = floor or H.grass_px
    lip, foot, wopen, eopen = key[0], key[1] == "f", key[2] == "w", key[3] == "e"
    variant = int(key[4]) if len(key) > 4 else 0
    top = 0
    if lip == "g":
        top = 3
    elif lip == "r":
        top = 3
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, face_px(x, y, ramp, ferns, variant))
    # the lip
    if lip == "g":
        prof = [2, 2, 3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 2, 3, 2, 2]     # the grass's ragged edge
        for x in range(16):
            gl = prof[x]
            for y in range(gl):
                L.px(ox + x, oy + y, H.grass_px(x, y))
            L.px(ox + x, oy + gl, "gd" if x % 3 else "g1")       # grass hanging over the edge
            if x in (3, 9, 13):
                L.px(ox + x, oy + gl + 1, "gd")                  # a tuft dangling down
                L.px(ox + x, oy + gl + 2, ramp[4])
                continue
            L.px(ox + x, oy + gl + 1, ramp[5] if x % 4 else ramp[4])
            L.px(ox + x, oy + gl + 2, ramp[4] if (x + 1) % 3 else ramp[3])
    elif lip == "r":
        for x in range(16):
            for y in range(2):
                L.px(ox + x, oy + y, rock_top(x, y, ramp))
            L.px(ox + x, oy + 2, ramp[5] if x % 4 else ramp[4])
            L.px(ox + x, oy + 3, ramp[4] if (x + 1) % 3 else ramp[3])
    # the foot: the face darkens, then a band of fallen blocks
    if foot:
        for x in range(16):
            for y in range(9, 16):
                cur = L.get(ox + x, oy + y)
                if y >= 11:
                    L.px(ox + x, oy + y, H.shade(cur, -1, ramp) if cur in ramp else ramp[1])
        blocks = [(0, 12, 4), (4, 13, 3), (7, 12, 4), (11, 13, 3), (14, 12, 3)]
        for (bx, by, bw) in blocks:
            for x in range(bx, min(16, bx + bw)):
                L.px(ox + x, oy + by, ramp[3])
                for y in range(by + 1, 16):
                    L.px(ox + x, oy + y, ramp[1] if y < 15 else ramp[0])
            if bx + bw - 1 < 16:
                for y in range(by, 16):
                    L.px(ox + min(15, bx + bw - 1), oy + y, ramp[0])
    # open sides: the face turns away; ground shows beyond it
    if wopen:
        for y in range(16):
            edge = 2 + (1 if (y // 3) % 2 else 0)
            if lip != "-" and y < top + 2:
                edge += (top + 2 - y)
            for x in range(edge):
                L.px(ox + x, oy + y, floor(x, y))
            L.px(ox + edge, oy + y, ramp[1])
            L.px(ox + edge + 1, oy + y, ramp[4] if y > top else ramp[5])
    if eopen:
        for y in range(16):
            edge = 13 - (1 if (y // 3) % 2 else 0)
            if lip != "-" and y < top + 2:
                edge -= (top + 2 - y)
            for x in range(edge + 1, 16):
                g = floor(x, y)
                L.px(ox + x, oy + y, {"g3": "g1", "g2": "g1", "g1": "gd"}.get(g, g) if x < edge + 3 else g)
            L.px(ox + edge, oy + y, ramp[0])
            L.px(ox + edge - 1, oy + y, ramp[1])


def rock():
    return H.shape_set("rock", "The gorge's limestone, from above", SEC, wanted("rock"),
                       lambda s, ox, oy, k: paint_rock_cell(s.B, ox, oy, k), "X",
                       "Arkadian limestone seen from above: plateaus, buttresses, the gorge's far "
                       "wall. Where nothing of the rock lies south of a cell it shows a short "
                       "face of its own; where a `face` band continues below, the top runs flush. "
                       "Impassable. Names are blob shape keys.")


def face():
    keys = wanted("face", ["g---0", "gf--0", "r---0", "rf--0", "----0", "-f--0"])
    return H.shape_set("face", "Cliff faces, any height", SEC, keys,
                       lambda s, ox, oy, k: paint_face_cell(s.B, ox, oy, k), "X",
                       "The gorge's tall cliff faces, seen from the south. One piece per shape "
                       "key `<lip><foot><west><east>`: lip `g` (grass above), `r` (rock above) "
                       "or `-` (face above); `f` the bottom row (the dark foot and fallen "
                       "blocks); `w`/`e` an open side where ground shows. Stack rows for a cliff "
                       "1-4 cells tall. Impassable.")


def black():
    return H.shape_set("black", "The Styx's black rock, from above", SEC, wanted("black"),
                       lambda s, ox, oy, k: paint_rock_cell(s.B, ox, oy, k, BLACK, ferns=False), "X",
                       "The cirque's black rock: wet, nothing grows on it. Like `rock`. "
                       "Impassable. Names are blob shape keys.")


def bface():
    keys = wanted("bface", ["g---0", "gf--0", "r---0", "rf--0", "----0", "-f--0"])
    return H.shape_set("bface", "The black cliff's faces", SEC, keys,
                       lambda s, ox, oy, k: paint_face_cell(s.B, ox, oy, k, BLACK, ferns=False), "X",
                       "The cirque's black cliff, wet and bare, with a pale sheen on its ledges. "
                       "Shape keys as `face`. Impassable.")


# --------------------------------------------------------------------------
# Water: the river spur's pool, white water, the Styx's black pool, gravel
# --------------------------------------------------------------------------

def paint_water_cell(s, ox, oy, key):
    W = H.soft(key, margin=2.0, radius=3.0, amp=1.1, seed=5.3, jag=0.4)
    c = np.s_[16:32, 16:32]
    w = W[c]
    bank = H.halo(W)
    bank2 = H.halo(W | bank)
    for y in range(16):
        for x in range(16):
            if w[y, x]:
                continue
            if bank[y + 16, x + 16]:
                h = H.hsh(x, y, 11) % 7
                col = "qr2" if h < 3 else ("qr3" if h < 5 else "qr1")
            elif bank2[y + 16, x + 16]:
                col = "qr3" if (x + y) % 3 == 0 else ("gd" if (x + y) % 2 else "g1")
            else:
                col = H.grass_px(x, y)
            s.M.px(ox + x, oy + y, col)
    # a lip of foam where the water meets the stones
    for y, x in np.argwhere(H.ring(W)[c] & w):
        if (x + 2 * y) % 3:
            s.M.px(ox + x, oy + y, "qs1")


def water():
    return H.shape_set("water", "A still pool with a gravel bank", SEC, wanted("water"),
                       paint_water_cell, "X",
                       "Aethos's animated water under a bank of river gravel: the pool below the "
                       "rapid on Route 11's spur. MB_POND_WATER: fish it. Names are blob shape "
                       "keys.", on="sea", behavior="MB_POND_WATER")


def rapids():
    """White water: foam over aethos's animated sea, for the Krathis's channel.
    Not surfable (its cells block, at the walking elevation)."""
    names = {"a": (0, 0), "b": (1, 0), "c": (2, 0), "lip": (3, 0)}
    s = H.struct("rapids", "White water", 4, 1, SEC, walk=["XXXX"], names=names, on="sea",
                 notes="Foam over aethos's animated water: `a`, `b` and `c` mix through the "
                       "Krathis's channel, `lip` is a rapid's drop (a white curl across the "
                       "stream). Not surfable: lay them at the walking elevation, blocked.")
    M = s.M
    for i, seed in enumerate((3, 7, 11)):
        ox = i * 16
        for y in range(16):
            for x in range(16):
                # streaks running north, the way the river flows
                v = (x * 5 + seed * 3 + (y // 3) * 7) % 11
                h = H.hsh(x, y, seed) % 100
                if v < 2 or (v == 2 and h < 50):
                    M.px(ox + x, y, "qm1" if h < 60 else "qs1")
                elif v == 3 and h < 40:
                    M.px(ox + x, y, "qs0")
    ox = 48
    for x in range(16):
        crest = 6 + (1 if x % 5 == 0 else 0) - (1 if x % 7 == 3 else 0)
        for y in range(crest - 2, crest + 4):
            if y < crest:
                M.px(ox + x, y, "qs0" if (x + y) % 2 else "qs1")
            elif y < crest + 2:
                M.px(ox + x, y, "qm1")
            else:
                M.px(ox + x, y, "qs1" if (x + y) % 2 else "qm1")
        for y in range(crest + 6, 16):
            if (x * 3 + y) % 7 == 0:
                M.px(ox + x, y, "qm1")
    return s


def paint_blackpool_cell(s, ox, oy, key):
    """Still black water: no ripple, no reflection. A rim of wet black stone,
    a sheen line, and obols glinting on the bottom here and there."""
    W = H.soft(key, margin=2.0, radius=3.0, amp=0.9, seed=8.1, jag=0.3)
    c = np.s_[16:32, 16:32]
    w = W[c]
    rim = H.halo(W)
    rim2 = H.halo(W | rim)
    L = s.B
    for y in range(16):
        for x in range(16):
            if w[y, x]:
                col = "qk0" if (x + 3 * y) % 17 else "qk1"
            elif rim[y + 16, x + 16]:
                col = "qb2" if (x + y) % 3 else "qb1"
            elif rim2[y + 16, x + 16]:
                col = "qb3" if (x + y) % 2 else "qb4"
            else:
                col = H.grass_px(x, y)
            L.px(ox + x, oy + y, col)
    for y, x in np.argwhere(H.ring(W)[c] & w):
        if y > 0 and not W[y + 15, x + 16]:
            L.px(ox + x, oy + y, "qb1")        # the water's lip, just below the stone
    # an obol on the bottom, here and there: only deep in the pool
    if key == "1|11111111":
        L.px(ox + 9, oy + 10, "qa1")
        L.px(ox + 10, oy + 10, "qa1")
        L.px(ox + 9, oy + 9, "qa2")


def blackpool_deep():
    """The pool's middle with nothing on the bottom: mix it with the interior."""
    s = H.struct("blackpool_deep", "The Styx's black water, deep", 2, 1, SEC, walk=["XX"],
                 names={"deep": (0, 0), "glint": (1, 0)},
                 notes="Interior cells to mix through the black pool: `deep` bare black water, "
                       "`glint` two obols on the bottom. MB_POND_WATER.")
    for x in range(32):
        for y in range(16):
            s.B.px(x, y, "qk0" if (x + 3 * y) % 17 else "qk1")
    for (x, y) in ((20, 4), (26, 12)):
        s.B.px(x, y, "qa1")
        s.B.px(x + 1, y, "qa1")
        s.B.px(x, y - 1, "qa2")
    s.behaviors[(0, 0)] = "MB_POND_WATER"
    s.behaviors[(1, 0)] = "MB_POND_WATER"
    return s


def blackpool():
    return H.shape_set("blackpool", "The Styx's still black water", SEC, wanted("blackpool"),
                       paint_blackpool_cell, "X",
                       "Still black water, its own palette, no ripple animation: obols glint on "
                       "the bottom. MB_POND_WATER, so a rod casts and gets \"Not even a nibble\" "
                       "(Styx Falls has no fishing table). Names are blob shape keys.",
                       behavior="MB_POND_WATER")


def paint_gravel_cell(L, ox, oy, key):
    vis, _ = agros_ground.visible(key, margin=2.0, radius=2.5, amp=1.2, seed=9.4, jag=0.6)
    L.texture(H.GRASS, ox, oy, 16, 16)
    for y, x in np.argwhere(vis):
        h = H.hsh(x, y, 41) % 100
        col = "qr3" if h < 45 else ("qr4" if h < 70 else ("qr2" if h < 92 else "qr1"))
        L.px(ox + x, oy + y, col)
    for (gx, gy) in ((3, 4), (10, 2), (7, 10), (13, 12), (1, 13)):
        if vis[gy, gx]:
            L.px(ox + gx, oy + gy, "qr5")
            if gy + 1 < 16 and vis[gy + 1, gx]:
                L.px(ox + gx, oy + gy + 1, "qr1")
    for y, x in np.argwhere(agros_ground.ring(vis)):
        if (x + y) % 2:
            L.px(ox + x, oy + y, "qr2")


def gravel():
    return H.shape_set("gravel", "River gravel", SEC, wanted("gravel"),
                       lambda s, ox, oy, k: paint_gravel_cell(s.B, ox, oy, k), ".",
                       "A walkable bank of river gravel, the Krathis's on its spur. Names are "
                       "blob shape keys.")


def build():
    return [tall(), meadow_tall(), path(), rock(), face(), black(), bface(), water(), rapids(),
            blackpool(), blackpool_deep(), gravel()]
