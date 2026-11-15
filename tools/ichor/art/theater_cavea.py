"""The cavea, the aisle and the orchestra of Thyrsa's theater, cell by cell.

Every cell from row 10 down is painted here from the shared geometry in
theater_lib: its tier, its facet, the stairs and walkways through it, the
orchestra's circle. Identical cells are stored once, so the whole cavea costs a
few dozen metatiles: one repeating cell per facet, its stairs and its edges.

Each seat cell comes three ways:
  empty   stone only (the bottom layer): the theater on an ordinary day;
  full    the same stone with the audience in the middle layer, in one of three
          arrangements (`crowd_variant`), for the Dionysia. The build stores each
          full cell three times, once per pair of blocks, each on its own copy
          of the crowd's palette, so a pair's pulse can stop on its own.

The engine fills the seats from the table theater.py writes
(src/data/ichor_act2_theater.h); the map's own layout is the empty theater.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import theater_lib as T  # noqa: E402
from theater_lib import C, Layer  # noqa: E402


def _hash(x, y, salt=0):
    h = (x * 73856093 ^ y * 19349663 ^ salt * 83492791) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h >> 8) & 0xFFFF


# --------------------------------------------------------------------------
# What a pixel is
# --------------------------------------------------------------------------

def orchestra_px(px, py):
    """The orchestra's circle: 'earth', its kerb, the drain round it, or None."""
    d = math.hypot(px + 0.5 - T.OX, py + 0.5 - T.OY)
    if d < T.OR - 3:
        return "earth"
    if d < T.OR:
        return "kerb"
    if d < T.OR + 2:
        return "drain"
    return None


def region_px(px, py):
    """(kind, tier, frac, facet) for a pixel at or below the cavea's cut."""
    t, facet = T.tier_coord(px, py)
    tier = int(math.floor(t))
    frac = t - tier
    if facet == "W" and py < T.CUT:
        return ("parodos", tier, frac, facet)
    if tier < 0:
        o = orchestra_px(px, py)
        return (o or "aisle", tier, frac, facet)
    if tier >= T.TIERS:
        return ("terrace", tier, frac, facet)
    if tier in T.PROMENADE:
        return ("promenade", tier, frac, facet)
    if tier in T.DIAZOMA:
        return ("diazoma", tier, frac, facet)
    s = T.stair_at(px, py)
    if s:
        return ("stair" + s, tier, frac, facet)
    return ("seat", tier, frac, facet)


# --------------------------------------------------------------------------
# Stone: seats, steps, paving
# --------------------------------------------------------------------------

def along(px, py, facet):
    """The coordinate along a tier (for joints between seat stones)."""
    x = T.mirror_px(px)
    if facet == "S":
        return px
    if facet == "W":
        return py
    return x + py  # the diagonal runs along x + y


def seat_color(px, py, tier, frac, facet):
    """The bench, seen from above and behind: a bright lip on its front edge
    (toward the stage), the seat, a crease, then the footwell of the row behind."""
    a = along(px, py, facet)
    if tier == T.FRONT_ROW:
        # the front row: marble thrones with backs, for priests and guests
        if frac < 0.10:
            return "qs3"
        if frac < 0.55:
            return "qs3" if (a % 16) not in (0, 15) else "qs1"
        if frac < 0.70:
            return "qs2" if (a % 16) not in (0, 15) else "qs0"
        if frac > 0.92:
            return "qs0"
        return "qs1"
    if frac < 0.08:
        return "qs3"
    if frac < 0.56:
        # seat stones, jointed every 32 px along the straight rows
        if facet != "D" and a % 32 == 0:
            return "qs1"
        return "qs2"
    if frac < 0.64:
        return "qs1"
    if frac > 0.92:
        return "qs0"
    return "qs1" if (a + int(frac * 16)) % 4 else "qs2"


def paving_color(px, py, tier, frac, facet, kind):
    """The diazoma and the promenade: big slabs, a kerb at the inner edge."""
    a = along(px, py, facet)
    span = 2.0  # both walkways are two tiers deep
    f = ((tier - (T.DIAZOMA[0] if kind == "diazoma" else T.PROMENADE[0])) + frac) / span
    if f < 0.05:
        return "qp3"
    if f < 0.10:
        return "qp1"
    if f > 0.95:
        return "qp0"
    joint_a = a % 32 == 0
    joint_f = abs(f - 0.5) < 0.03
    if joint_a or joint_f:
        return "qp1"
    return "qp2"


def stair_color(px, py, tier, frac, facet, which):
    """Two steps per tier, each with a bright tread edge; the stair's sides
    are a kerb."""
    x = T.mirror_px(px)
    if which == "C":
        side = px - T.STAIR_C[0]
        if side in (0, 31):
            return "qp0"
        if side in (1, 30):
            return "qp1"
        step = (py - T.YS) % 8
    elif which == "W":
        side = py - T.STAIR_W[0]
        if side in (0, 15):
            return "qp0"
        if side == 1:
            return "qp1"
        step = (T.XW - 1 - x) % 8
    else:
        v = x + py + 1
        side = v - T.STAIR_D[0]
        if side in (0, 1, 30, 31):
            return "qp0"
        if side in (2, 29):
            return "qp1"
        u = (py - x - (T.YS - T.XS)) % 12
        step = 0 if u == 0 else (7 if u == 11 else 3)
    if step == 0:
        return "qp3"
    if step == 7:
        return "qp1"
    return "qp2"


def aisle_color(px, py, tier, frac):
    """Flagstones round the orchestra, the front row's step at their edge."""
    gx, gy = px % 32, py % 32
    if (gx == 0 and (py // 32) % 2 == 0) or gy == 0 or (gx == 16 and (py // 32) % 2 == 1):
        return "qp1"
    return "qp2"


def earth_color(px, py):
    """Beaten earth, tamped smooth: a speckle that repeats every two cells, so
    the orchestra's middle costs four tiles."""
    h = _hash(px % 32, py % 32, 7) % 19
    if h == 0:
        return "qe2"
    if h in (1, 2):
        return "qe0"
    return "qe1"


def ground_color(px, py, kind, tier, frac, facet):
    # the side tiers end at the parodoi in a capped retaining wall
    if facet == "W" and T.CUT <= py < T.CUT + 2 and kind != "parodos":
        stone = kind == "seat"
        if py == T.CUT:
            return "qs0" if stone else "qp0"
        return "qs3" if stone else "qp3"
    if kind == "seat":
        return seat_color(px, py, tier, frac, facet)
    if kind in ("diazoma", "promenade"):
        return paving_color(px, py, tier, frac, facet, kind)
    if kind.startswith("stair"):
        return stair_color(px, py, tier, frac, facet, kind[-1])
    if kind in ("aisle", "parodos"):
        return aisle_color(px, py, tier, frac)
    if kind == "earth":
        return earth_color(px, py)
    if kind == "kerb":
        d = math.hypot(px + 0.5 - T.OX, py + 0.5 - T.OY)
        return "qp3" if d < T.OR - 1.5 else "qp1"
    if kind == "drain":
        return "qp0"
    return None


# --------------------------------------------------------------------------
# The audience
# --------------------------------------------------------------------------

CROWD_VARIANTS = 3


def crowd_variant(cx, cy):
    return _hash(cx, cy, 11) % CROWD_VARIANTS


# Each facet's people per cell, per variant: (x, y, hair, tunic). Positions are
# cell-local; people never cross the cell's edge, so any arrangement can sit
# next to any other.
PEOPLE = {
    "S": [
        [(0, 0, "qh1", "qcw"), (8, 0, "ink", "qcr")],
        [(0, 0, "qcy", "qcb"), (8, 0, "qh2", "qcp")],
        [(0, 0, "ink", "qcy"), (8, 0, "qh1", "qi1")],
    ],
    "W": [
        [(6, 3, "qh1", "qcr")],
        [(6, 3, "ink", "qcw")],
        [(6, 3, "qh2", "qcb")],
    ],
    "D": [
        [(2, 5, "ink", "qcw")],
        [(2, 5, "qh1", "qcp")],
        [(2, 5, "qcy", "qcr")],
    ],
}


def cell_is_seat(cx, cy):
    """A whole cell of seats: no stair, walkway or edge in it."""
    kinds = set()
    for ly in range(0, 16, 3):
        for lx in range(0, 16, 3):
            kinds.add(region_px(cx * 16 + lx, cy * 16 + ly)[0])
    return kinds == {"seat"}


# --------------------------------------------------------------------------
# Painting a cell
# --------------------------------------------------------------------------

def paint_cell(cx, cy, full=False, variant=None):
    """The three layers of cell (cx, cy): ground in the bottom layer, people (if
    full) in the middle. Cells right of the axis are drawn as mirrors of their
    twins on the left, so Porytiles stores one of each."""
    if not T.is_left(cx):
        tw = paint_cell(T.W - 1 - cx, cy, full, variant)
        return {ln: a[:, ::-1].copy() for ln, a in tw.items()}
    B, M, Tp = Layer(16, 16), Layer(16, 16), Layer(16, 16)
    px_kinds = [[region_px(cx * 16 + lx, cy * 16 + ly) for lx in range(16)] for ly in range(16)]
    has_seat = any(k[0] == "seat" for row in px_kinds for k in row)
    has_other = any(k[0] != "seat" for row in px_kinds for k in row)
    mixed = has_seat and has_other
    # the promenade's outer edge meets the terrace's grass: that grass is
    # aethos's own (borrowed by the build), so the paving moves to the middle layer
    on_grass = any(k[0] == "terrace" for row in px_kinds for k in row)
    for ly in range(16):
        for lx in range(16):
            px, py = cx * 16 + lx, cy * 16 + ly
            kind, tier, frac, facet = px_kinds[ly][lx]
            c = ground_color(px, py, kind, tier, frac, facet)
            if on_grass:
                if c:
                    M.px(lx, ly, c)
                continue
            if not mixed:
                if c:
                    B.px(lx, ly, c)
                continue
            # seats run on under the stone; the stone lies over them
            t, f = T.tier_coord(px, py)
            B.px(lx, ly, seat_color(px, py, int(math.floor(t)), t - math.floor(t), f))
            if kind != "seat" and c:
                M.px(lx, ly, c)
    if full and has_seat:
        for (x, y, sprite, hair, tunic) in people_in(cx, cy):
            T.person(M, x, y, sprite, hair, tunic)
    return {"bottom": B.a, "middle": M.a, "top": Tp.a}


def people_for_cell(cx, cy, v):
    """The people sitting in seat cell (cx, cy) on the straight facets:
    (x, y, sprite, hair, tunic), cell-local. South rows hold two people a
    cell, side columns one."""
    facet = T.facet_of_cell(cx, cy)
    if facet == "S":
        return [(x, y, "S", h, t) for (x, y, h, t) in PEOPLE["S"][v]]
    if facet == "W":
        return [(x, y, "W", h, t) for (x, y, h, t) in PEOPLE["W"][v]]
    return []


_PURE = {}


def pure_seat(cx, cy):
    """Every pixel of the cell is seating (no stair, walkway or aisle in it)."""
    if (cx, cy) not in _PURE:
        kinds = {region_px(cx * 16 + lx, cy * 16 + ly)[0] for ly in range(16) for lx in range(16)}
        _PURE[(cx, cy)] = kinds == {"seat"}
    return _PURE[(cx, cy)]


_PURE_T = {}


def pure_tile(tx, ty):
    """Every pixel of the 8x8 tile is seating: a person may sit in it without
    sharing a tile with stone (they would be in different palettes)."""
    if (tx, ty) not in _PURE_T:
        kinds = {region_px(tx * 8 + lx, ty * 8 + ly)[0] for ly in range(8) for lx in range(8)}
        _PURE_T[(tx, ty)] = kinds == {"seat"}
    return _PURE_T[(tx, ty)]


COLORS = [("ink", "qcw"), ("qh1", "qcp"), ("qcy", "qcr"), ("qh2", "qcb"), ("qh1", "qcy"),
          ("ink", "qi1"), ("qh1", "qcw"), ("ink", "qcr")]


def _candidates():
    """Every place a person could sit on the left half, in map pixels, in the
    order they are seated: (x0, y0, sprite, hair, tunic). Each facet seats its
    people along its tiers' seat lines at a spacing that repeats with the cell
    lattice, so a facet's cells still repeat."""
    out = []
    for k in range(T.TIERS):
        if k in T.DIAZOMA or k >= T.PROMENADE[0]:
            continue
        # south rows: two a cell, sitting on the row's front half
        y0 = T.YS + 16 * k
        for n in range(0, T.OX // 8):
            out.append((8 * n, y0, "S") + COLORS[(n % 4) + 4 * (k % 2)])
        # west columns: one a cell, facing the orchestra
        x0 = T.XW - 16 * (k + 1) + 6
        for m in range(0, T.H):
            out.append((x0, 16 * m + 3, "W") + COLORS[(m % 2) * 2 + (k % 2) + 3])
        # diagonals: one each 8 px along the seat line (x + y steps by 16)
        u = (T.YS - T.XS) + 24 * k + 10
        for n in range(0, 80):
            v = 16 * n
            sx, sy = (v - u) // 2, (v + u) // 2
            out.append((sx - 3, sy - 8, "D") + COLORS[(n % 2) + 2 * (k % 3)])
    return out


_PEOPLE = None


def all_people():
    """The audience of the left half: each candidate whose seat point lies on
    its own facet, whose every pixel is in an all-seat cell, and who overlaps
    nobody already seated."""
    global _PEOPLE
    if _PEOPLE is not None:
        return _PEOPLE
    taken = np.zeros((T.H * 16, T.OX), bool)
    out = []
    for (x0, y0, sprite, h, t) in _candidates():
        if x0 < 0 or y0 < 0 or x0 + 7 > T.OX or y0 + 9 > T.H * 16:
            continue
        sx, sy = x0 + 3, y0 + 8
        if T.tier_coord(sx, sy)[1] != sprite:
            continue
        tiles = {((x0 + i) // 8, (y0 + j) // 8) for j in range(0, 9, 4) for i in range(0, 7, 3)}
        if not all(pure_tile(tx, ty) for tx, ty in tiles):
            continue
        cells = {(tx // 2, ty // 2) for tx, ty in tiles}
        if any(T.walk_cell(cx, cy) for cx, cy in cells):
            continue
        if taken[y0:y0 + 9, x0:x0 + 7].any():
            continue
        taken[y0:y0 + 9, x0:x0 + 7] = True
        out.append((x0, y0, sprite, h, t))
    _PEOPLE = out
    return out


def people_in(cx, cy):
    x, y = cx * 16, cy * 16
    found = [(x0 - x, y0 - y, sp, h, t) for (x0, y0, sp, h, t) in all_people()
             if x0 < x + 16 and x0 + 7 > x and y0 < y + 16 and y0 + 9 > y]
    # nearer (lower) people overlap the ones behind them
    return sorted(found, key=lambda p: p[1])


def cavea_cells():
    """Every cell this module paints: rows 8 and below (the parodoi, the
    orchestra, the cavea), the whole width, but not the terrace's grass. The
    map builder lays the stage's front over row 8's middle."""
    out = []
    for cy in range(T.CUT // 16 - 2, T.H):
        for cx in range(T.W):
            kinds = {region_px(cx * 16 + lx, cy * 16 + ly)[0]
                     for ly in (0, 7, 15) for lx in (0, 7, 15)}
            if kinds <= {"terrace"}:
                continue
            out.append((cx, cy))
    return out


def owns(cx, cy):
    return (cx, cy) in set(cavea_cells())


def key_of(layers):
    return b"".join(layers[ln].tobytes() for ln in ("bottom", "middle", "top"))
