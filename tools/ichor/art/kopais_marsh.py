"""The Kopais's soft ground: reed beds, marsh water, the open lake, mudflats.

Every set holds one piece per class key the map uses (kopais_lib: '1|' then
the classes of N NE E SE S SW W NW). tools/ichor/maps/kopais.py --shapes lists
them in kopais_shapes.json, and only those are drawn.

  reeds  the marsh's tall grass: MB_LONG_GRASS (encounters; the long-grass
         field effect parts round the player). Tall stems, cattails and plumes,
         swaying on four phases. Outside it: grass, mud, or water.
  marsh  shallow marsh water, murky green, its glints drifting on four phases:
         MB_POND_WATER (surf with the Conch, fish). Banks of mud, then grass.
  lake   the open lake: aethos's animated water, borrowed, ringed by marsh
         water drawn over it. MB_POND_WATER.
  mud    mudflats, cracked and puddled, with birds' prints. Walkable.
  path   the road (agros's painter, as Route 1 and Kithairon).
  barley tall grass on the Phikion spur (agros's painter): MB_TALL_GRASS.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import agros_ground
import kopais_lib as K

SEC = "ground"
SHAPES = Path(__file__).resolve().parent / "kopais_shapes.json"
FULL = "1|11111111"


def wanted(kind, default=None):
    """The class keys a set must hold, interior first."""
    keys = []
    if SHAPES.exists():
        data = json.loads(SHAPES.read_text())
        keys = list(data.get(kind, []))
    if not keys:
        keys = list(default or [FULL])
    if FULL in keys:
        keys.remove(FULL)
    return [FULL] + keys


# --------------------------------------------------------------------------
# Reeds
# --------------------------------------------------------------------------

# The reed bed's stems: (x, head row, kind, lit). Stems run the whole height
# (the bed is continuous); each is brightest just under its head and darkens
# with depth, so the heads scatter instead of lining up in rows. Kinds: C a
# cattail, P a plume, B a blade's tip with a leaf.
STEMS = [(0, 4, "B", True), (2, 12, "B", False), (3, 1, "C", True), (5, 7, "B", True),
         (7, 13, "P", True), (8, 3, "B", False), (10, 9, "C", True), (11, 0, "B", True),
         (13, 6, "B", False), (14, 11, "B", True)]
LEAVES = [(1, 6, 1), (6, 10, -1), (9, 5, 1), (12, 14, -1), (15, 9, -1)]


def _stem_shift(phase, yy, head):
    """A stem's sway at row yy: its head and the rows just under it lean."""
    d = (yy - head) % 16
    return K.sway(phase) if d <= 3 or d == 15 else 0


def reed_px(x, y, phase=0):
    """The reed bed's color at a 16 px periodic pixel, for a phase of the sway."""
    xx, yy = x % 16, y % 16
    for (x0, head, kind, lit) in STEMS:
        sx = (xx - _stem_shift(phase, yy, head)) % 16
        d = (yy - head) % 16
        if kind == "C" and d < 3:
            if sx == x0:
                return "ct1" if d < 2 else "ct0"
            if sx == (x0 + 1) % 16:
                return "ct0"
            continue
        if kind == "P" and d < 2:
            if sx == x0 or (d == 0 and sx == (x0 + 1) % 16):
                return "rpl"
            continue
        if sx != x0:
            continue
        if d == 0:
            return "t3" if lit else "gd"
        if d < 6:
            return "t3" if lit and d < 4 else "gd"
        if d < 11:
            return "gd" if lit else "t1"
        return "t1"
    for (x0, y0, dd) in LEAVES:
        for k in range(3):
            lx, ly = (x0 + dd * k) % 16, (y0 - k) % 16
            s = K.sway(phase) if k == 2 else 0
            if (xx - s) % 16 == lx and yy == ly:
                return "gd" if k < 2 else "t3"
    return "t1" if (xx + 2 * yy) % 11 == 0 else "t0"


def mud_px(x, y):
    """Mudflat: brown crust with darker cracks and a damp patch (16 px periodic)."""
    xx, yy = x % 16, y % 16
    h = K.hsh(xx, yy, 31) % 100
    crack = {(2, 3), (3, 3), (4, 4), (5, 4), (6, 5), (5, 6), (11, 9), (12, 9), (13, 10),
             (12, 11), (8, 13), (9, 13), (10, 14), (1, 11), (2, 12)}
    if (xx, yy) in crack:
        return "md0"
    if (xx, yy) in {(3, 2), (4, 3), (6, 4), (12, 8), (13, 9), (9, 12)}:
        return "md3"
    if 9 <= xx <= 13 and 2 <= yy <= 4 and h < 80:
        return "md1"                       # a damp patch
    if h < 12:
        return "md1"
    if h > 93:
        return "md3"
    return "md2"


def water_px(x, y, phase=0):
    """Marsh water: still, murky green; ripple dashes and glints drift east a
    pixel or two per phase."""
    xx, yy = x % 16, y % 16
    for (ry, rx, n) in ((2, 1, 5), (7, 9, 4), (12, 4, 6)):
        if yy == ry and (xx - rx - phase) % 16 < n:
            return "mw2"
        if yy == ry + 1 and (xx - rx - phase - 1) % 16 < n - 2:
            return "mw0"
    for (gx, gy) in ((6, 4), (13, 10), (1, 14)):
        if yy == gy and xx == (gx + 2 * phase) % 16:
            return "mw3"
    return "mw1"


def duckweed(x, y):
    """A few floating duckweed specks on the marsh water (static)."""
    xx, yy = x % 16, y % 16
    return (xx, yy) in {(10, 9), (11, 9), (3, 6)}


# --------------------------------------------------------------------------
# Painters for one 16 x 16 cell
# --------------------------------------------------------------------------

def paint_reeds(s, ox, oy, key, phase=0):
    """The reed bed, edged by the class of each neighbor: grass and mud get a
    dark rim with tips leaning out; water gets stems thinning into it."""
    neigh = key.split("|")[1]
    wet_only = all(c in "1w" for c in neigh) and "w" in neigh
    vis = K.soft(K.binary(key), margin=3.5, radius=3.0, amp=2.4, seed=1.3, jag=1.6)
    cls = K.class_canvas(key)
    c = np.s_[16:32, 16:32]
    v = vis[c]
    L = s.B
    for y in range(16):
        for x in range(16):
            if v[y, x]:
                L.px(ox + x, oy + y, reed_px(x, y, phase))
                continue
            k = cls[y + 16, x + 16]
            if k == "w" and wet_only:
                col = water_px(x, y, phase)
            elif k in ("w", "m"):
                col = mud_px(x, y)
                if col in ("md2", "md3"):
                    col = "md1"            # reedw and reed both hold md0/md1 only
            else:
                col = K.grass_name(x, y)
            L.px(ox + x, oy + y, col)
    # the rim: dark where the bed meets dry ground, tips leaning out of it
    rim = K.ring(vis)[c] & v
    for y, x in np.argwhere(rim):
        k = nearest_out_class(vis, cls, y + 16, x + 16)
        if k in ("g", "m"):
            if L.get(ox + x, oy + y) not in ("ct0", "ct1", "rpl"):
                L.px(ox + x, oy + y, "t1")
    # feathery tops: where the bed's top edge meets anything, the stems that
    # reach it go on up one to three pixels (heads on the lit ones)
    for y, x in np.argwhere(K.halo(vis)[c] & ~v):
        k = cls[y + 16, x + 16]
        if not (y + 1 < 16 and v[y + 1, x]):
            if k == "w" and wet_only and (x * 7 + y * 3) % 6 == 0:
                L.px(ox + x, oy + y, "mw2")      # a ripple ring round the bed
            continue
        under = reed_px(x, y + 1, phase)
        if under in ("t0", "t1") or K.hsh(x, y, 5) % 2 == 0:
            continue
        reach = 1 + K.hsh(x, y, 9) % 3
        for j in range(reach):
            yy = y - j
            if yy < 0 or v[yy, x]:
                break
            if k in ("w", "m") and not wet_only:
                pass
            top = j == reach - 1 and K.hsh(x, y, 13) % 3 == 0
            L.px(ox + x, oy + yy, "t3" if top else "gd")
        if k == "w" and wet_only and y - reach >= 0 and not v[y - reach, x] and (x + y) % 4 == 0:
            L.px(ox + x, oy + y - reach, "mw2")


def nearest_out_class(vis, cls, y, x):
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < 48 and 0 <= xx < 48 and not vis[yy, xx]:
            return cls[yy, xx]
    return "g"


def paint_marsh(s, ox, oy, key, phase=0):
    """Marsh water; outside it, a bank of mud, then grass (or more mud)."""
    vis = K.soft(K.binary(key, "1rsL"), margin=2.0, radius=3.0, amp=1.1, seed=5.1, jag=0.4)
    cls = K.class_canvas(key)
    c = np.s_[16:32, 16:32]
    v = vis[c]
    bank = K.halo(vis)
    bank2 = K.halo(vis | bank)
    bank3 = K.halo(vis | bank | bank2)
    L = s.B
    for y in range(16):
        for x in range(16):
            if v[y, x]:
                col = water_px(x, y, phase)
                if duckweed(x, y):
                    col = "lp2" if (x + y) % 2 else "lp1"
                L.px(ox + x, oy + y, col)
                continue
            k = cls[y + 16, x + 16]
            if k == "m" or bank[y + 16, x + 16] or bank2[y + 16, x + 16]:
                col = mud_px(x, y)
                if bank[y + 16, x + 16]:
                    col = "md0" if (x + y) % 3 == 0 else "md1"     # the wet lip
            elif bank3[y + 16, x + 16] and (x + y) % 2:
                col = "gd"
            else:
                col = K.grass_name(x, y)
            L.px(ox + x, oy + y, col)


def paint_lake(s, ox, oy, key, phase=0):
    """The open lake on borrowed animated water (bottom layer empty), its rim of
    marsh water drawn on the middle layer."""
    vis = K.soft(K.binary(key, "1s"), margin=2.0, radius=4.0, amp=1.5, seed=7.7, jag=0.3)
    c = np.s_[16:32, 16:32]
    v = vis[c]
    edge = K.halo(vis)[c] & ~v
    M = s.M
    for y in range(16):
        for x in range(16):
            if v[y, x]:
                continue
            col = water_px(x, y, phase)
            if edge[y, x]:
                col = "mw2" if (x + y + phase) % 3 else "mw3"
            M.px(ox + x, oy + y, col)


def paint_mud(s, ox, oy, key, phase=0):
    """Mudflats meeting grass: a dried, paler crust at the rim."""
    vis = K.soft(K.binary(key, "1wr"), margin=1.0, radius=3.0, amp=1.4, seed=3.3, jag=0.6)
    c = np.s_[16:32, 16:32]
    v = vis[c]
    L = s.B
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, mud_px(x, y) if v[y, x] else K.grass_name(x, y))
    for y, x in np.argwhere(K.ring(vis)[c] & v):
        L.px(ox + x, oy + y, "md3" if (x + y) % 2 else "md2")
    for y, x in np.argwhere(K.halo(vis)[c] & ~v):
        if (x * 3 + y) % 4 == 0:
            L.px(ox + x, oy + y, "gd")


def shape_set(key, title, keys, painter, walk_code, notes, phase=0, on=None, behavior=None):
    w = 8
    h = max(1, (len(keys) + w - 1) // w)
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = K.struct(key, title, w, h, SEC, walk=[walk_code * w] * h, notes=notes, names=names)
    if on:
        K.ground(s, on)
    for n in range(w * h):
        k = keys[min(n, len(keys) - 1)]
        painter(s, (n % w) * 16, (n // w) * 16, k, phase)
        if behavior:
            s.behaviors[(n % w, n // w)] = behavior
    return s


def build(phase=0):
    reeds = shape_set("reeds", "Reed beds: the marsh's tall grass", wanted("reeds"), paint_reeds, "G",
                      "Tall reeds with cattails and plumes, swaying on four phases (a tile "
                      "animation). MB_LONG_GRASS: wild encounters, and the long-grass field "
                      "effect parts round the player. Names are class keys (`1|` then N NE E "
                      "SE S SW W NW: `1` reeds, `g` grass, `m` mud, `w` water).",
                      phase=phase, behavior="MB_LONG_GRASS")
    marsh = shape_set("marsh", "Marsh water with mud banks", wanted("marsh"), paint_marsh, "X",
                      "Shallow, murky marsh water whose glints drift on four phases. "
                      "MB_POND_WATER: surf it with the Conch and fish it. Banks of wet mud, "
                      "then grass. Reeds, the lake and stonework count as water here (their "
                      "own pieces draw the meeting).", phase=phase, behavior="MB_POND_WATER")
    lake = shape_set("lake", "The open lake", wanted("lake"), paint_lake, "X",
                     "Aethos's animated water, borrowed, ringed by marsh water. "
                     "MB_POND_WATER. Its interior is pure borrowed water.", phase=phase,
                     on="sea", behavior="MB_POND_WATER")
    mud = shape_set("mud", "Mudflats", wanted("mud"), paint_mud, ".",
                    "Cracked mud with damp patches, meeting grass. Walkable.", phase=phase)
    for s in (reeds, marsh, lake):
        K.struct_anim(s, s.key)
    path = agros_set("path", "The road with soft edges", agros_ground.paint_path, ".",
                     "The limestone road, scalloped where it meets the grass (agros's painter).")
    barley = agros_set("barley", "Barley on the Phikion spur", agros_ground.paint_tall, "G",
                       "Barley tall grass on aethos grass (agros's painter), for the spur's rocky "
                       "grass. MB_TALL_GRASS.", behavior="MB_TALL_GRASS")
    return [reeds, marsh, lake, mud, path, barley]


def agros_set(key, title, paint, walk_code, notes, behavior=None):
    keys = wanted(key)
    w = 8
    h = max(1, (len(keys) + w - 1) // w)
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = K.struct(key, title, w, h, SEC, walk=[walk_code * w] * h, notes=notes, names=names)
    for n in range(w * h):
        k = keys[min(n, len(keys) - 1)]
        paint(s.B, (n % w) * 16, (n // w) * 16, K.binary(k))
        if behavior:
            s.behaviors[(n % w, n // w)] = behavior
    return s
