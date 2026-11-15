"""Building painters the steppe's town sets share: roofs of terracotta tile,
thatch, turf or felt, walls of mud-brick, timber or whitewash, doors and
windows, all on a 16 px grid so pieces snap together.

A house front is three rows: the roof's upper half (drawn over the player),
its lower half ending in the eave, and the wall with its door. Pieces are
named <part>_<L|M|R> and the right-hand ends are mirror images of the left,
so Porytiles stores them once.
"""
from __future__ import annotations

import math

import farlands_lib as F
from farlands_lib import put


def mirror_cell(L, src, dst):
    """Copy the 16 x 16 cell at src (x, y px) to dst, flipped left-right."""
    sx, sy = src
    dx, dy = dst
    L.a[dy:dy + 16, dx:dx + 16] = L.a[sy:sy + 16, sx:sx + 16][:, ::-1]


# --------------------------------------------------------------------------
# Roofs
# --------------------------------------------------------------------------

def tile_roof_px(X, Y, top=0):
    """Terracotta pantiles in courses: each course lit along its top edge."""
    y = (Y - top) % 6
    x = (X + ((Y - top) // 6) * 2) % 4
    if y == 0:
        return "tc2"
    if y == 5:
        return "tc0"
    if x == 3:
        return "tc0" if y > 2 else "tc1"
    return "tc1" if y > 2 else ("tc2" if x == 0 else "tc1")


def thatch_px(X, Y, top=0):
    """Reed thatch in bundles: streaks running down, a darker course line."""
    y = (Y - top) % 7
    k = F.hp(X, Y, 37)
    c = "sg2" if k % 3 else "sg3"
    if (X * 3 + Y) % 5 == 0:
        c = "sg1"
    if y == 6:
        c = "sg1" if X % 2 else "sg0"
    return c


def turf_px(X, Y, top=0):
    """A turf roof: grass growing over sod, dry in patches."""
    k = F.hp(X, Y, 59)
    c = "g1" if k % 3 else "gd"
    if k % 7 == 0:
        c = "sg2"
    if (Y - top) % 5 == 4 and k % 2:
        c = "gd"
    return c


def roof_cells(L, ox, oy, px_fn, edge, eave, eave_dark, ridge=None):
    """Paint roof pieces A_L A_M (upper) and B_L B_M (lower) at
    (ox, oy) .. two columns, two rows; the caller mirrors the R pieces.
    The roof slopes in at its ends; its ridge sits at y 3 of the upper row."""
    for cx in (0, 1):
        end = cx == 0
        for y in range(32):
            for x in range(16):
                X, Y = ox + cx * 16 + x, oy + y
                if y < 3:
                    continue
                if end and x < max(0, 6 - (y - 3) // 2):
                    continue
                c = px_fn(X, Y, top=oy + 3)
                if end and x < 8 - (y - 3) // 3 and x >= 6 - (y - 3) // 2 - 1:
                    c = edge
                if y == 3:
                    c = ridge or edge
                if y >= 29:
                    c = eave if y == 29 else eave_dark
                L.px(X, Y, c)
        if end:
            for y in range(3, 32):
                for x in range(16):
                    if L.get(ox + x, oy + y):
                        L.px(ox + x, oy + y, edge)
                        break


# --------------------------------------------------------------------------
# Walls
# --------------------------------------------------------------------------

def brick_px(X, Y):
    """Mud-brick laid in courses, plastered thin, the bricks showing through."""
    y = Y % 4
    x = (X + (Y // 4 % 2) * 4) % 8
    k = F.hp(X, Y, 43)
    if y == 3 or x == 7:
        return "mb1"
    return "mb3" if k % 9 == 0 else "mb2"


def timber_wall_px(X, Y):
    """Weathered upright planks between posts."""
    x = X % 16
    k = F.hp(X, Y, 47)
    if x in (0, 1):
        return "tb1" if x == 0 else "tb2"
    if x % 4 == 0:
        return "tb1"
    c = "tb3" if k % 5 else "tb4"
    if k % 11 == 0:
        c = "tb2"
    return c


def wall_cells(L, ox, oy, px_fn, base, outline, kinds, extra=None):
    """Paint wall pieces in a row at (ox, oy): kinds is a list of
    'L', 'M', 'window', 'door', 'shutter'. A base course along the bottom; L
    has the wall's west edge."""
    for i, kind in enumerate(kinds):
        x0 = ox + i * 16
        for y in range(16):
            for x in range(16):
                c = px_fn(x0 + x, oy + y)
                if y >= 13:
                    c = base[0] if y == 13 else base[1]
                if kind == "L" and x < 2:
                    c = outline if x == 0 else base[0]
                L.px(x0 + x, oy + y, c)
        if kind == "window":
            for y in range(3, 10):
                for x in range(4, 12):
                    c = "ink" if y > 3 and 5 <= x <= 10 else outline
                    if y in (3,) or x in (4, 11):
                        c = outline
                    L.px(x0 + x, oy + y, c)
            for x in range(4, 12):
                L.px(x0 + x, oy + 10, base[0])
        if kind == "shutter":
            for y in range(3, 11):
                for x in range(3, 13):
                    c = "tb2" if x < 8 else "tb1"
                    if x in (3, 12) or y in (3, 10):
                        c = outline
                    if x == 7 or x == 8:
                        c = outline
                    L.px(x0 + x, oy + y, c)
        if kind == "door":
            for y in range(2, 16):
                for x in range(3, 13):
                    if y == 2 or x in (3, 12):
                        c = outline
                    else:
                        c = "tb2" if x < 8 else "tb1"
                        if x == 7:
                            c = "tb0"
                    L.px(x0 + x, oy + y, c)
            L.px(x0 + 10, oy + 9, "tb4")
        if extra:
            extra(L, x0, oy, kind)
