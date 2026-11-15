"""Kithairon's soft ground: tall grass, the road, crags and their south faces,
the cave's walls, and water with stony, reedy banks.

Each set holds one piece per blob shape key (kithairon_lib.blob_keys). The map
builder (tools/ichor/maps/kithairon.py --shapes) lists the keys its maps use in
kithairon_shapes.json, and only those are drawn, so a set costs metatiles only
for the outlines the maps really have. Every piece is cut from one continuous
field, so pieces meet in any arrangement.

  tall   barley tall grass on aethos grass (agros's painter): MB_TALL_GRASS
  path   the limestone road and goat tracks on grass (agros's painter)
  crag   Kithairon's grey rock: a lit top and a south face with strata, a
         shadow on the grass below it. Blocks.
  cave   the same rock as Antiope's cave walls, on the cave floor
  water  a pool or the Asopos, on aethos's animated sea, with a pebbly bank
         and reeds: MB_POND_WATER (surf and fish)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import agros_ground
import kithairon_lib as K

SEC = "ground"
SHAPES = Path(__file__).resolve().parent / "kithairon_shapes.json"
FACE = 14         # a crag's south face, in pixels


def wanted(kind):
    """The shape keys a set must hold: kithairon_shapes.json's list for the
    kind, or every blob shape if the maps haven't been measured yet."""
    if SHAPES.exists():
        data = json.loads(SHAPES.read_text())
        if kind in data and data[kind]:
            keys = list(data[kind])
            full = "1|11111111"
            if full in keys:                      # the interior first: it's the one used most
                keys.remove(full)
                keys.insert(0, full)
            return keys
    keys = K.blob_keys()
    keys.remove("1|11111111")
    return ["1|11111111"] + keys


# --------------------------------------------------------------------------
# Tall grass and the road: agros's painters, unchanged, so they match Route 1
# --------------------------------------------------------------------------

def tall():
    return K.shape_set("tall", "Tall grass with soft edges", SEC, wanted("tall"),
                       lambda s, ox, oy, k: agros_ground.paint_tall(s.B, ox, oy, k), "G",
                       "Barley tall grass on aethos grass, cut from one field so any outline "
                       "works (agros's painter, as on Route 1). MB_TALL_GRASS throughout. "
                       "Names are blob shape keys (`1|NNEESESSWWNW`).",
                       behavior="MB_TALL_GRASS")


def path():
    return K.shape_set("path", "The road with soft edges", SEC, wanted("path"),
                       lambda s, ox, oy, k: agros_ground.paint_path(s.B, ox, oy, k), ".",
                       "The limestone road and its goat-track branches, scalloped where they "
                       "meet the grass (agros's painter). Names are blob shape keys.")


# --------------------------------------------------------------------------
# Crags
# --------------------------------------------------------------------------

def _crag_fields(key):
    V = K.soft(key, margin=0.0, radius=3.0, amp=1.2, seed=4.3, jag=0.5)
    T = np.zeros_like(V)
    T[:-FACE] = V[FACE:]
    T &= V                                   # the top: rock with rock FACE px below it
    return V, T


_TOP_PTS = [(4, 3), (12, 6), (5, 12), (13, 14)]
_FACE_PTS = [(1, 0), (6, 0), (10, 0), (14, 0)]


def _voronoi(pts, wrap_y=True):
    """For each pixel of a 16 x 16 periodic cell: (index of nearest point, gap
    to the second nearest), on a torus."""
    near = np.zeros((16, 16), int)
    gap = np.zeros((16, 16), float)
    for y in range(16):
        for x in range(16):
            ds = []
            for i, (px, py) in enumerate(pts):
                dx = min(abs(x - px), 16 - abs(x - px))
                dy = min(abs(y - py), 16 - abs(y - py)) if wrap_y else 0
                ds.append((dx * dx + dy * dy * (1 if wrap_y else 0), i))
            ds.sort()
            near[y, x] = ds[0][1]
            gap[y, x] = ds[1][0] ** 0.5 - ds[0][0] ** 0.5
    return near, gap


_TOP_NEAR, _TOP_GAP = _voronoi(_TOP_PTS)


def rock_top(x, y):
    """Kithairon's rock seen from above: a weathered grey surface with sparse
    specks and pits, plain enough that its 16 px repeat doesn't show. Detail
    (cracks, boulders, tufts, scrub) comes from `crag_detail`'s interior cells,
    which the map builder scatters."""
    xx, yy = x % 16, y % 16
    h = K.hsh(xx, yy, 7) % 100
    if (xx, yy) in ((3, 5), (11, 12), (13, 3)):
        return "rk1"
    if (xx, yy) in ((3, 4), (11, 11), (13, 2), (7, 9)):
        return "rk4"
    if h < 9:
        return "rk2"
    if h > 94:
        return "rk4"
    return "rk3"


def rock_face(x, y, depth):
    """The south face: rough vertical columns, lit on their left, darker toward
    the foot. depth is how far down the face the pixel is (0 at the lip)."""
    xx = x % 16
    if depth == 0:
        return "rk5" if xx % 4 else "rk4"
    if depth >= FACE - 1:
        return "rk0"
    cols = [1, 6, 10, 14]
    sway = (depth // 4) % 2
    edge = [(c + sway * (1 if j % 2 else -1)) % 16 for j, c in enumerate(cols)]
    if xx in edge:
        return "rk0" if depth > FACE // 2 else "rk1"
    if (xx - 1) % 16 in edge:
        return "rk3" if depth < FACE - 3 else "rk2"
    if depth in (4, 9) and (xx * 3 + depth) % 5 < 2:
        return "rk1"
    if depth > FACE - 4:
        return "rk1" if (xx + depth) % 3 == 0 else "rk2"
    return "rk2" if (xx + depth * 3) % 7 else "rk3"


def paint_crag_cell(L, ox, oy, key, floor):
    V, T = _crag_fields(key)
    F = V & ~T
    c = np.s_[16:32, 16:32]
    v, t, f = V[c], T[c], F[c]
    # the floor around and below
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, floor(x, y))
    # a soft shadow below the face, and a thin one beside the rock
    sh = K.halo(V)[c]
    below = np.zeros((48, 48), bool)
    below[1:] = V[:-1] & ~V[1:]
    below2 = np.zeros((48, 48), bool)
    below2[2:] = V[:-2] & ~V[2:] & ~V[1:-1]
    for y, x in np.argwhere((sh | below[c] | below2[c]) & ~v):
        cur = L.get(ox + x, oy + y)
        L.px(ox + x, oy + y, {"g3": "g1", "g2": "g1", "g1": "gd", "rk2": "rk1", "rk3": "rk2"}
             .get(cur, cur))
    # depth of each face pixel below its lip
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
                col = rock_face(x, y, depth[y + 16, x + 16])
            else:
                col = rock_top(x, y)
            L.px(ox + x, oy + y, col)
    # rims on the top surface: lit to the north and west, shaded east
    r = K.ring(T)[c]
    for y, x in np.argwhere(r & t):
        N = not T[y + 15, x + 16]
        W = not T[y + 16, x + 15]
        Ee = not T[y + 16, x + 17]
        if N or W:
            L.px(ox + x, oy + y, "rk5" if (x + y) % 3 else "rk4")
        elif Ee:
            L.px(ox + x, oy + y, "rk2")
    # the silhouette against the floor
    for y, x in np.argwhere(K.ring(V)[c] & v):
        if not T[y + 16, x + 16] and depth[y + 16, x + 16] < FACE - 1:
            # the sides of the face
            L.px(ox + x, oy + y, "rk1")
        elif not (L.get(ox + x, oy + y) in ("rk5",)):
            L.px(ox + x, oy + y, "rk1" if T[y + 16, x + 16] else "rk0")


def grass_floor(x, y):
    g = K.aethos(K.GRASS)
    return A_name(g[y % 16, x % 16])


def A_name(rgb):
    return K.A.RGB2NAME[tuple(int(v) for v in rgb)]


def cave_floor(x, y):
    """Antiope's cave: packed grey earth with a few pebbles (16 px periodic)."""
    xx, yy = x % 16, y % 16
    h = K.hsh(xx, yy, 3) % 100
    if (xx, yy) in ((3, 4), (4, 4), (11, 10), (12, 11), (7, 13)):
        return "rk3"
    if (xx, yy) in ((3, 5), (4, 5), (11, 11), (8, 13)):
        return "rk0"
    return "rk2" if h < 18 else "rk1"


def crag():
    return K.shape_set("crag", "Crags: grey rock with a south face", SEC, wanted("crag"),
                       lambda s, ox, oy, k: paint_crag_cell(s.B, ox, oy, k, grass_floor), "X",
                       "Kithairon's grey limestone, seen from above with its south face "
                       "showing, on aethos grass. Fill any region with it: the face appears "
                       "along every south edge and the rock casts a shadow on the grass. "
                       "Impassable. Names are blob shape keys.")


def cave():
    return K.shape_set("cave", "Antiope's cave: walls on the cave floor", SEC, wanted("cave"),
                       lambda s, ox, oy, k: paint_crag_cell(s.B, ox, oy, k, cave_floor), "X",
                       "The crag's rock as cave walls, on the cave floor. Impassable. Names "
                       "are blob shape keys; `cave_floor` below is the open floor.")


def cave_floor_struct():
    s = K.struct("cave_floor", "Antiope's cave: the floor", 3, 1, SEC, walk=["..."],
                 names={"plain": (0, 0), "pebbles": (1, 0), "exit": (2, 0)},
                 notes="`plain` the packed floor, `pebbles` a scatter of stones, `exit` "
                       "the floor brightening toward daylight: MB_SOUTH_ARROW_WARP, put the "
                       "warp out there on the cave's bottom row.")
    for x in range(48):
        for y in range(16):
            s.B.px(x, y, cave_floor(x, y))
    for (x, y) in ((19, 3), (26, 9), (22, 12), (28, 4), (17, 13)):
        K.put(s.B, x, y, [".3.", "322", ".0."], {"3": "rk4", "2": "rk3", "0": "rk0"})
    # the exit: light falling in from the south
    for y in range(16):
        for x in range(32, 48):
            k = y + (K.hsh(x, y, 9) % 5) - 2
            if k > 9:
                s.B.px(x, y, "rk4" if k > 13 else "rk3")
    s.behaviors[(2, 0)] = "MB_SOUTH_ARROW_WARP"
    return s


# --------------------------------------------------------------------------
# Water: pools and the Asopos, on aethos's animated sea
# --------------------------------------------------------------------------

def paint_water_cell(s, ox, oy, key):
    W = K.soft(key, margin=2.0, radius=3.0, amp=1.1, seed=5.1, jag=0.4)
    c = np.s_[16:32, 16:32]
    w = W[c]
    M = s.M
    g = K.aethos(K.GRASS)
    bank = K.halo(W)
    bank2 = K.halo(W | bank)
    for y in range(16):
        for x in range(16):
            if w[y, x]:
                continue
            if bank[y + 16, x + 16]:
                h = K.hsh(x, y, 11) % 7
                col = "rk2" if h < 3 else ("rk3" if h < 5 else "rk1")
            elif bank2[y + 16, x + 16]:
                col = "gd" if (x + y) % 2 else "g1"
            else:
                col = A_name(g[y, x])
            M.px(ox + x, oy + y, col)
    # reeds on the bank, here and there: two or three blades
    for y, x in np.argwhere(bank2[c] & ~w):
        if K.hsh(x, y, 13) % 9 == 0 and y >= 3:
            M.px(ox + x, oy + y, "iv1")
            M.px(ox + x, oy + y - 1, "iv2")
            M.px(ox + x, oy + y - 2, "iv2")
            M.px(ox + x, oy + y - 3, "iv0")


def water():
    return K.shape_set("water", "Water with a pebbly bank (pools, the Asopos)", SEC,
                       wanted("water"), paint_water_cell, "X",
                       "Aethos's animated sea under a bank of grey pebbles and reeds. "
                       "MB_POND_WATER: surf it with the Conch and fish it. Names are blob "
                       "shape keys; the interior is `1|11111111`.", on="sea",
                       behavior="MB_POND_WATER")


def build():
    return [tall(), path(), crag(), cave(), cave_floor_struct(), water()]
