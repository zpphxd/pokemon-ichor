"""Parnassos's soft ground: tall grass, the road, crags with a south face, the
river Herkyna with pebbly banks, paving, and gullies.

Each set holds one piece per blob shape key (parnassos_lib.blob_keys). The map
builder (tools/ichor/maps/parnassos.py --shapes) lists the keys its maps use in
parnassos_shapes.json, and only those are drawn. Every piece is cut from one
continuous field, so pieces meet in any arrangement.

  tall    barley tall grass on aethos grass (agros's painter, as on every route):
          MB_TALL_GRASS
  path    the limestone road and goat tracks (agros's painter)
  crag    Parnassos's limestone: Kithairon's crag painter, recolored paler and
          warmer. A lit top, a south face with strata, a shadow below. Blocks.
  water   the Herkyna on aethos's animated sea, under a bank of pale pebbles and
          reeds: MB_POND_WATER (surf it, fish it)
  pave    polygonal limestone flags: the crossroads' triangle, the precinct, the
          treasury's floor. Walkable; edges worn into the grass.
  gully   a dry ravine seen from above: its far wall's face, then the dark floor.
          Blocks.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import agros_ground
import kithairon_ground as KG
import parnassos_lib as P

SEC = "ground"
SHAPES = Path(__file__).resolve().parent / "parnassos_shapes.json"
FULL = "1|11111111"


def wanted(kind):
    """The shape keys a set must hold: parnassos_shapes.json's list for the kind,
    or every blob shape if the maps haven't been measured yet."""
    if SHAPES.exists():
        data = json.loads(SHAPES.read_text())
        if data.get(kind):
            keys = list(data[kind])
            if FULL in keys:
                keys.remove(FULL)
            return [FULL] + keys
    keys = P.blob_keys()
    keys.remove(FULL)
    return [FULL] + keys


def tall():
    return P.shape_set("tall", "Tall grass with soft edges", SEC, wanted("tall"),
                       lambda s, ox, oy, k: agros_ground.paint_tall(s.B, ox, oy, k), "G",
                       "Barley tall grass on aethos grass, cut from one field so any outline "
                       "works (agros's painter, as on every route). MB_TALL_GRASS throughout. "
                       "Names are blob shape keys (`1|NNEESESSWWNW`).",
                       behavior="MB_TALL_GRASS")


def path():
    return P.shape_set("path", "The road with soft edges", SEC, wanted("path"),
                       lambda s, ox, oy, k: agros_ground.paint_path(s.B, ox, oy, k), ".",
                       "The limestone road and its goat tracks, scalloped where they meet the "
                       "grass (agros's painter). Names are blob shape keys.")


def _crag(s, ox, oy, k):
    KG.paint_crag_cell(s.B, ox, oy, k, KG.grass_floor)


def crag():
    s = P.shape_set("crag", "Crags: pale limestone with a south face", SEC, wanted("crag"), _crag,
                    "X", "Parnassos's limestone seen from above, its south face showing, on "
                         "aethos grass. Fill any region: the face appears along every south "
                         "edge, with a shadow on the grass below. Impassable. Kithairon's "
                         "painter, recolored. Names are blob shape keys.")
    return P.recolor_struct(s)


def water():
    s = P.shape_set("water", "The Herkyna: water with a pebbly bank", SEC, wanted("water"),
                    KG.paint_water_cell, "X",
                    "Aethos's animated water under a bank of pale pebbles and reeds. "
                    "MB_POND_WATER: surf it with the Conch and fish it. Names are blob shape "
                    "keys; the interior is `1|11111111`.", on="sea", behavior="MB_POND_WATER")
    return P.recolor_struct(s)


# --------------------------------------------------------------------------
# Paving: polygonal limestone flags
# --------------------------------------------------------------------------

_FLAG_PTS = [(3, 3), (11, 2), (7, 9), (14, 11), (2, 13)]


def _flag_cells():
    near = np.zeros((16, 16), int)
    gap = np.zeros((16, 16), float)
    for y in range(16):
        for x in range(16):
            ds = []
            for i, (px, py) in enumerate(_FLAG_PTS):
                dx = min(abs(x - px), 16 - abs(x - px))
                dy = min(abs(y - py), 16 - abs(y - py))
                ds.append(((dx * dx + dy * dy) ** 0.5, i))
            ds.sort()
            near[y, x] = ds[0][1]
            gap[y, x] = ds[1][0] - ds[0][0]
    return near, gap


_NEAR, _GAP = _flag_cells()
_TONE = ["mb3", "mb3", "mb2", "mb3", "mb3"]


def pave_px(x, y):
    xx, yy = x % 16, y % 16
    if _GAP[yy, xx] < 1.0:
        return "mb1"
    t = _TONE[_NEAR[yy, xx]]
    # a lit upper-left edge on each flag
    if _GAP[(yy - 1) % 16, xx] < 1.0:
        return "mb4"
    if _GAP[(yy + 1) % 16, xx] < 1.0:
        return "mb2"
    h = P.hsh(xx, yy, 21) % 29
    if h == 0:
        return "mb1"
    if h < 3:
        return "mb4" if t == "mb3" else "mb3"
    return t


def paint_pave_cell(s, ox, oy, key):
    V = P.soft(key, margin=0.5, radius=3.0, amp=1.0, seed=2.7, jag=0.4)
    c = np.s_[16:32, 16:32]
    v = V[c]
    L = s.B
    rim = P.ring(V)[c]
    sh = P.halo(V)[c]
    for y in range(16):
        for x in range(16):
            if v[y, x]:
                col = "mb1" if rim[y, x] else pave_px(x, y)
            else:
                col = P.grass_name(x, y)
                if sh[y, x]:
                    col = {"g3": "g1", "g2": "g1", "g1": "gd"}.get(col, col)
            L.px(ox + x, oy + y, col)


def pave():
    return P.shape_set("pave", "Paving: polygonal limestone flags", SEC, wanted("pave"),
                       paint_pave_cell, ".",
                       "Old polygonal flags, worn into the grass at their edges: the "
                       "crossroads' triangle, Lebadeia's precinct, the treasury's floor. "
                       "Walkable. Where paving meets the road, count the road as paving (and "
                       "the paving as road) so they join without a grass seam. Names are blob "
                       "shape keys.")


# --------------------------------------------------------------------------
# Gullies: dry ravines, seen from above
# --------------------------------------------------------------------------

FACE = 11


def paint_gully_cell(s, ox, oy, key):
    """The far (north) wall's face shows, falling into a dark floor; the near
    lips are lit. Outside the gully: grass."""
    V = P.soft(key, margin=1.0, radius=2.5, amp=1.0, seed=6.1, jag=0.5)
    c = np.s_[16:32, 16:32]
    L = s.B
    # depth below the gully's north edge, per column
    depth = np.zeros((48, 48), int)
    for x in range(48):
        run = 0
        for y in range(48):
            run = run + 1 if V[y, x] else 0
            depth[y, x] = run
    rim = P.ring(V)
    sh = P.halo(V)
    for y in range(16):
        for x in range(16):
            yy, xx = y + 16, x + 16
            if not V[yy, xx]:
                col = P.grass_name(x, y)
                if sh[yy, xx]:
                    col = {"g3": "g1", "g2": "g1", "g1": "gd"}.get(col, col)
                L.px(ox + x, oy + y, col)
                continue
            d = depth[yy, xx] - 1
            if d < FACE:
                # the far wall: strata, darkening as it falls
                if d == 0:
                    col = "pk4"
                elif (x + d * 3) % 9 == 0:
                    col = "pk1"
                elif d < 4:
                    col = "pk3" if (x + d) % 5 else "pk2"
                elif d < 8:
                    col = "pk2" if (x * 3 + d) % 7 else "pk1"
                else:
                    col = "pk1" if (x + d) % 3 else "pk0"
            else:
                col = "pk0"
                if P.hsh(x, y, 31) % 11 == 0:
                    col = "pk1"
            if rim[yy, xx] and d >= 1:
                # the near lips: a lit rim on the west, a dark one on the east and south
                W = not V[yy, xx - 1]
                col = "pk4" if W else ("pk2" if not V[yy + 1, xx] else "pk1")
            L.px(ox + x, oy + y, col)


def gully():
    return P.shape_set("gully", "Gullies: a dry ravine from above", SEC, wanted("gully"),
                       paint_gully_cell, "X",
                       "A dry gully: its far wall's face falls into a dark floor, the near "
                       "lips catch the light. Impassable. The treasury's drums roll into "
                       "one; the broken bridge spans another. Names are blob shape keys.")


def build():
    return [tall(), path(), crag(), water(), pave(), gully()]
