"""Aegina's dry ground for gTileset_Aegina: the sun-dried grass at the edge of
town and on the hills, its soft edges onto aethos's meadow, golden tall grass
for the detour's encounter bands, the ant hills and an ant trail.

The dry grass is drawn flat with sparse tufts, in aethos's own manner, so it sits
beside aethos grass and paths as one ground. Its edges lie on borrowed aethos
grass: the dry straw is drawn in the middle layer with a soft lip, and the real
meadow shows through past it.
"""
from __future__ import annotations

import math

import numpy as np

from aegina_lib import Struct, ground

SEC = "aegina"

# --------------------------------------------------------------------------
# The straw texture
# --------------------------------------------------------------------------

# Sparse tufts on a flat tawny ground, like aethos's grass: (x, y) of each tuft's
# root within a 16 px cell. A tuft is a small "v" of darker blades lit at the tips.
TUFTS_A = [(4, 5), (12, 3), (9, 11), (2, 14)]
TUFTS_B = [(5, 4), (13, 8), (3, 11), (10, 14)]


def tuft(L, x, y):
    for (dx, dy, c) in ((0, 0, "dg1"), (-1, -1, "dg1"), (1, -1, "dg1"), (-2, -2, "dg3"),
                        (2, -2, "dg3")):
        L.px(x + dx, y + dy, c)


def straw(L, x0, y0, w, h, variant=0, mask=None):
    """Fill a box with dry grass, phase-locked to the 16 px grid. mask(x, y) -> bool
    limits it to a shape (for the edges)."""
    tufts = TUFTS_A if variant == 0 else TUFTS_B
    ok = (lambda x, y: x0 <= x < x0 + w and y0 <= y < y0 + h and (not mask or mask(x, y)))
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if ok(x, y):
                L.px(x, y, "dg2")
    for cy in range(y0 // 16, (y0 + h + 15) // 16):
        for cx in range(x0 // 16, (x0 + w + 15) // 16):
            for (tx, ty) in tufts:
                X, Y = cx * 16 + tx, cy * 16 + ty
                pts = [(X, Y), (X - 1, Y - 1), (X + 1, Y - 1), (X - 2, Y - 2), (X + 2, Y - 2)]
                if all(ok(px, py) for (px, py) in pts):
                    tuft(L, X, Y)
            if variant == 1:                        # a pale pebble
                X, Y = cx * 16 + 12, cy * 16 + 13
                if ok(X, Y) and ok(X + 1, Y + 1):
                    L.px(X, Y, "s4")
                    L.px(X + 1, Y, "s3")
                    L.px(X, Y + 1, "dg1")
                    L.px(X + 1, Y + 1, "dg1")


def soft(i, seed):
    """How far the meadow reaches into an edge cell at position i along it: a
    gentle run of rounded bumps, about 4 px deep."""
    return 4 + 1.5 * math.sin((i + seed) * 0.8) + 0.6 * math.sin((i * 1.7 + seed) * 0.5)


def lip(M, x0, y0, inside):
    """A darker rim of straw where it meets the meadow, on the sunward sides."""
    for y in range(y0, y0 + 16):
        for x in range(x0, x0 + 16):
            if not inside(x, y):
                continue
            for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                X, Y = x + dx, y + dy
                if x0 <= X < x0 + 16 and y0 <= Y < y0 + 16 and not inside(X, Y):
                    M.px(x, y, "dg1")
                    break


# --------------------------------------------------------------------------
# The dry grass patch
# --------------------------------------------------------------------------

def dry_grass():
    """A 5 x 3 kit: a patch (cols 0-2), its inner corners and pebbled fills."""
    s = Struct("dry_grass", "Dry grass: a patch with soft edges onto the meadow", 5, 3, SEC,
               walk=[".....", ".....", "....."],
               notes="Sun-dried grass and straw. Cols 0-2 are the patch: TL T TR / L C R / BL B "
                     "BR, fading onto aethos grass round its edge. Cols 3-4: row 0 the inner "
                     "corners NW and NE (meadow only in that corner), row 1 the inner corners "
                     "SW and SE, row 2 two plain fills with a pebble, to scatter through big "
                     "patches. All walkable, no encounters.")
    ground(s, "grass", [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2),
                        (3, 0), (4, 0), (3, 1), (4, 1)])
    B, M = s.B, s.M
    straw(B, 16, 16, 16, 16, 0)
    straw(B, 48, 32, 16, 16, 1)
    straw(B, 64, 32, 16, 16, 1)

    def edge_cell(cx, cy, n, s_, w, e):
        x0, y0 = cx * 16, cy * 16

        def inside(x, y):
            lx, ly = x - x0, y - y0
            if n and ly < soft(lx, 1):
                return False
            if s_ and 15 - ly < soft(lx, 4):
                return False
            if w and lx < soft(ly, 2):
                return False
            if e and 15 - lx < soft(ly, 6):
                return False
            # round the outer corners off
            if n and w and math.hypot(lx - 8, ly - 8) > 8.5 and lx < 8 and ly < 8:
                return False
            if n and e and math.hypot(lx - 7, ly - 8) > 8.5 and lx > 7 and ly < 8:
                return False
            if s_ and w and math.hypot(lx - 8, ly - 7) > 8.5 and lx < 8 and ly > 7:
                return False
            if s_ and e and math.hypot(lx - 7, ly - 7) > 8.5 and lx > 7 and ly > 7:
                return False
            return True
        straw(M, x0, y0, 16, 16, 0, mask=inside)
        lip(M, x0, y0, inside)

    def inner_corner(cx, cy, corner):
        x0, y0 = cx * 16, cy * 16
        ox = -1 if "w" in corner else 16
        oy = -1 if "n" in corner else 16

        def inside(x, y):
            lx, ly = x - x0, y - y0
            return math.hypot(lx - ox, ly - oy) > 5.5 + 0.7 * math.sin((lx - ly) * 0.9)
        straw(M, x0, y0, 16, 16, 0, mask=inside)
        lip(M, x0, y0, inside)

    edge_cell(0, 0, True, False, True, False)
    edge_cell(1, 0, True, False, False, False)
    edge_cell(2, 0, True, False, False, True)
    edge_cell(0, 1, False, False, True, False)
    edge_cell(2, 1, False, False, False, True)
    edge_cell(0, 2, False, True, True, False)
    edge_cell(1, 2, False, True, False, False)
    edge_cell(2, 2, False, True, False, True)
    inner_corner(3, 0, "nw")
    inner_corner(4, 0, "ne")
    inner_corner(3, 1, "sw")
    inner_corner(4, 1, "se")
    return s


TALL = [   # aethos's tall grass (0x00D), stalk for stalk, so the two read as one kind
    "0G1110111011G011",
    "3011031113010311",
    "3010320103003201",
    "2300320103203201",
    "0332320103323201",
    "0323210103232101",
    "0222110102232101",
    "0211101110211011",
    "1011101110110G11",
    "0311130103113011",
    "3201030032013010",
    "3201032032012300",
    "3201033232010332",
    "2101032321010323",
    "1101022321010222",
    "1011102110110211",
]


def tall_grass():
    """Golden tall grass for the detour's encounter bands (MB_TALL_GRASS): aethos's
    tall grass stalk for stalk, gone to straw, with pale seed heads."""
    s = Struct("dry_tall_grass", "Dry tall grass (wild encounters)", 1, 1, SEC, walk=["."],
               notes="Tall golden grass on the dry hills, for wild encounters: "
                     "MB_TALL_GRASS, drawn stalk for stalk like aethos's 0x00D so the two "
                     "can share a band.")
    s.behaviors[(0, 0)] = "MB_TALL_GRASS"
    s.B.blit(TALL, {"0": "dg0", "1": "dg1", "2": "dg2", "3": "dg3", "G": "s4"}, 0, 0)
    return s


def mound(B, M, cx, cy, rx, ry):
    """An ant hill: a cone of loose red earth with a rounded crown, lit from the
    upper left, a dark entrance at the top, a shadow to the south-east and crumbs
    round its foot. (cx, cy) is the middle of its base; rx its half width at the
    base, ry its height."""
    for y in range(cy - 2, cy + 3):                          # shadow on the straw
        for x in range(cx - rx + 2, cx + rx + 4):
            if ((x - cx - 2) / (rx + 0.5)) ** 2 + ((y - cy) / 2.6) ** 2 <= 1:
                B.px(x, y, "dg1")

    def half(y):
        t = (cy - y) / ry                                    # 0 at the base, 1 at the top
        return rx * (1 - t) ** 0.8 + 1.2 * math.sqrt(max(0.0, 1 - t))
    for y in range(cy - ry, cy + 2):
        hw = half(min(y, cy)) + (0.6 if y > cy else 0)
        for x in range(cx - rx - 1, cx + rx + 2):
            if abs(x - cx) > hw:
                continue
            u, v = (x - cx) / max(hw, 1), (y - cy) / ry
            light = -u * 0.8 - v * 0.5 - 0.2                # toward the upper left
            c = "ea2" if light > 0.45 else ("ea1" if light > -0.35 else "ea0")
            if c == "ea1" and (x * 5 + y * 3) % 7 == 0:
                c = "ea2"                                    # grains of earth
            elif c == "ea2" and (x * 3 + y * 5) % 9 == 0:
                c = "dg3"
            M.px(x, y, c)
    # the rim of the dome and its base line
    a = M.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if abs(x - cx) <= rx + 1 and cy - ry - 1 <= y <= cy + 2:
            M.px(x, y, "ea0" if (x >= cx or y >= cy) else "ea1")
    # the entrance: a dark hole in a little crater at the crown
    top = cy - ry + 1
    M.px(cx - 1, top, "ea2")
    M.px(cx, top, "ink")
    M.px(cx + 1, top, "an0")
    M.px(cx, top + 1, "an0")
    M.px(cx - 1, top + 1, "ea1")
    # crumbs of earth round the foot
    for (dx, dy) in ((-rx - 2, 1), (rx + 2, 1), (-rx + 1, 2), (rx - 1, 2), (3, 2)):
        if M.get(cx + dx, cy + dy) is None:
            M.px(cx + dx, cy + dy, "ea1")


def ant(M, x, y, carrying=False):
    M.px(x, y, "ink")
    M.px(x + 1, y, "an0")
    if carrying:
        M.px(x + 1, y - 1, "dg3")


def anthills():
    """Two ant hills and an ant trail in the dry grass (the Myrmidons' island)."""
    s = Struct("anthills", "An ant hill and an ant trail", 2, 1, SEC, walk=["X."],
               notes="On dry grass: an ant hill (solid) and a walkable trail of ants crossing "
                     "the straw. Scatter the hills in twos and threes where the town gives way "
                     "to the dry hills, and lead trails between them.")
    B, M = s.B, s.M
    straw(B, 0, 0, 32, 16, 0)
    for x in range(0, 16):                     # clear the straw's tufts under the mound
        for y in range(2, 14):
            if B.get(x, y) in ("dg1", "dg3"):
                B.px(x, y, "dg2")
    mound(B, M, 7, 12, 6, 10)
    for (x, y, c) in ((2, 3, True), (13, 4, False), (12, 13, False)):
        ant(M, x, y, c)
    # the trail: a dotted line of ants winding across the straw, some carrying grain
    for k, i in enumerate(range(0, 16, 3)):
        y = 9 + int(round(2.2 * math.sin(i * 0.4)))
        ant(M, 16 + i, y, carrying=(k % 2 == 0))
    for i in range(1, 16, 3):
        M.px(16 + i, 10 + int(round(2.2 * math.sin(i * 0.4))), "dg1")
    return s


def build():
    return [dry_grass(), tall_grass(), anthills()]
