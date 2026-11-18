"""gTileset_SeatAthena: Hypatia's seat, Athena's hall of lamps (design/maps/Olympus_Pantheon.md).

A library at night: an ivory floor inlaid with olive green, night-indigo
walls of scroll pigeonholes, bronze lampstands down the aisle (they burn low
until Hypatia's owl wakes, then every one flares), marble owls on their
pedestals, scroll cabinets, the owl roundel in the floor, and at the head of
the hall the sacred olive growing out of the rostrum, as Athena's grew from
the rock of the Akropolis.

Palette groups: floor (ivory marble, olive inlay), wall (night indigo, gold,
parchment), marble (owls, the rostrum, the planter), olive (the tree), lamp
(bronze stands and their flames).
"""
from __future__ import annotations

import pantheon_lib as P
from pantheon_lib import (Struct, Layer, flagstones, flat, ink_edge, m_ellipse, m_poly, m_rect, mask, shade,
                          tiled)

C = {
    "k": (16, 16, 32),
    # ivory marble and the olive inlay
    "v0": (128, 112, 96), "v1": (176, 160, 136), "v2": (208, 192, 160), "v3": (224, 216, 184),
    "v4": (240, 232, 208), "o1": (88, 104, 48), "o2": (128, 144, 64),
    # night indigo, gold, parchment
    "n0": (16, 16, 48), "n1": (32, 32, 80), "n2": (56, 56, 112), "n3": (88, 88, 144),
    "g1": (176, 128, 48), "g2": (232, 184, 80), "g3": (248, 232, 160),
    "p1": (200, 176, 128), "p2": (240, 224, 184), "r1": (144, 48, 40),
    # marble owls
    "s1": (112, 112, 128), "s2": (168, 168, 184), "s3": (216, 216, 224),
    # the olive
    "l0": (32, 56, 40), "l1": (64, 96, 56), "l2": (104, 136, 72), "l3": (160, 176, 104),
    "t0": (64, 48, 40), "t1": (104, 80, 64), "t2": (144, 120, 96),
    # lampstands and flame
    "b0": (72, 48, 24), "b1": (128, 88, 40), "f1": (232, 120, 40), "f2": (248, 200, 96), "f3": (248, 248, 216),
}

GROUPS = {
    "floor": ["k", "v0", "v1", "v2", "v3", "v4", "o1", "o2", "g1", "g2", "n1", "n2", "s2"],
    "wall": ["k", "n0", "n1", "n2", "n3", "g1", "g2", "g3", "p1", "p2", "r1", "v2", "b1"],
    "marble": ["k", "s1", "s2", "s3", "v1", "v2", "v3", "v4", "g1", "g2", "g3", "n1", "n2", "o1", "o2"],
    "olive": ["k", "l0", "l1", "l2", "l3", "t0", "t1", "t2", "n0", "n1", "n2", "v2", "v3", "s2"],
    "lamp": ["k", "b0", "b1", "g1", "g2", "g3", "f1", "f2", "f3", "v1", "v2", "v3", "v4", "n1", "n2"],
}


def floor_px(X, Y):
    x, y = X % 32, Y % 32
    ix, iy = x % 16, y % 16
    # a gold-and-olive star where four slabs meet
    if (ix, iy) == (0, 0):
        return "g2"
    if (ix, iy) in ((1, 0), (15, 0), (0, 1), (0, 15)):
        return "o2"
    if (ix, iy) in ((1, 1), (15, 15), (1, 15), (15, 1)):
        return "o1"
    c = flagstones(X, Y, ("v0", "v1", "v2", "v3"), "n2", "ath", slab_w=16, slab_h=16, period=32, bond=False)
    # a fine olive-green inlay line round every second slab pair
    return c


def floor_cell(cx, cy, fn=floor_px):
    return tiled(fn, ox=cx * 16, oy=cy * 16)


def shade_px(X, Y):
    c = floor_px(X, Y)
    if Y % 16 < 7:
        return {"v4": "v2", "v3": "v1", "v2": "v1", "v1": "v0", "v0": "n2", "n2": "n1"}.get(c, c)
    return c


def runner_cell(part):
    """The aisle: an olive-green band with a gold meander, three cells wide."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            L.px(x, y, floor_px(x, y))
    if part in "lr":
        e = 0 if part == "l" else 10
        L.rect(e, 0, 6, 16, "o1")
        L.vline(e + (5 if part == "l" else 0), 0, 15, "g1")
        # a gold key meander
        for y in range(16):
            u = y % 8
            xx = e + (1 if part == "l" else 1)
            if u in (0, 4):
                L.hline(xx, xx + 3, y, "g2")
            if u in (1, 2, 3):
                L.px(xx + (3 if u < 4 else 0), y, "g2")
            if u in (5, 6, 7):
                L.px(xx, y, "g2")
    return L.a.copy()


def roundel():
    """The owl roundel in the floor, 3 x 3, walkable: an owl in a gold ring."""
    s = Struct("roundel", "The owl roundel", 3, 3, "kit", walk=["..."] * 3)
    for cy in range(3):
        for cx in range(3):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = floor_cell(cx + 1, cy)
    B = s.B
    ring = m_ellipse(mask(48, 48), 2, 2, 45, 45)
    inner = m_ellipse(mask(48, 48), 5, 5, 42, 42)
    flat(B, ring & ~inner, "g1")
    flat(B, m_ellipse(mask(48, 48), 3, 3, 44, 44) & ~m_ellipse(mask(48, 48), 4, 4, 43, 43), "g2")
    flat(B, inner, "n1")
    flat(B, m_ellipse(mask(48, 48), 8, 8, 39, 39), "n2")
    # the owl: body, ear tufts, two great eyes
    body = m_ellipse(mask(48, 48), 15, 13, 32, 38)
    m_poly(body, [(15, 18), (16, 10), (20, 15)])
    m_poly(body, [(32, 18), (31, 10), (27, 15)])
    flat(B, body, "v2")
    flat(B, m_ellipse(mask(48, 48), 18, 24, 29, 37), "v3")
    for ex in (17, 25):
        flat(B, m_ellipse(mask(48, 48), ex, 16, ex + 5, 21), "g2")
        B.rect(ex + 2, 18, 2, 2, "k")
    B.px(23, 22, "g1"), B.px(24, 22, "g1"), B.px(23, 23, "g1")
    for y in range(27, 36, 3):
        B.hline(20, 27, y, "v1")
    B.hline(19, 28, 38, "g1")
    return s


def wall_px(X, Y):
    return flagstones(X, Y, ("n0", "n1", "n2", "n3"), "k", "aw", slab_w=16, slab_h=8, period=32)


def pigeonholes(L, y0, rows=2):
    """Scroll pigeonholes: deep cubbies, each holding a stack of rolled scrolls
    seen end-on (parchment rounds, a red-capped one here and there)."""
    for r in range(rows):
        yy = y0 + r * 7
        L.rect(0, yy, 16, 7, "n2")
        L.hline(0, 15, yy, "g1")
        for c in range(2):
            x = c * 8
            L.rect(x + 1, yy + 1, 7, 6, "n0")
            L.vline(x, yy + 1, yy + 6, "g1")
            seed = P.h("ph", x, yy)
            for j, (sx, sy) in enumerate(((1, 3), (4, 3), (2, 1), (5, 1))):
                col = "r1" if (seed + j) % 4 == 0 else "p2"
                L.rect(x + sx, yy + sy + 1, 2, 2, col)
                L.px(x + sx, yy + sy + 1, "p2" if col == "r1" else "v2")
                L.px(x + sx + 1, yy + sy + 2, "p1")


def wall_cell(row, cx, motif=None):
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            L.px(x, y, wall_px(cx * 16 + x, row * 16 + y))
    if row == 0:
        L.rect(0, 0, 16, 5, "n0")
        L.hline(0, 15, 5, "g1")
        L.rect(0, 6, 16, 6, "n1")
        # an egg-and-dart moulding in gold
        for x in range(0, 16, 4):
            L.rect(x + 1, 7, 2, 3, "g2")
            L.px(x + 1, 7, "g3")
            L.px(x + 3, 9, "g1")
        L.hline(0, 15, 12, "g1")
        L.rect(0, 13, 16, 3, "n2")
        L.hline(0, 15, 15, "k")
    if row == 1:
        pigeonholes(L, 1)
        L.hline(0, 15, 15, "g1")
    if row == 2:
        pigeonholes(L, 0, rows=1)
        L.rect(0, 8, 16, 8, "n1")
        L.hline(0, 15, 8, "g2")
        L.hline(0, 15, 9, "g1")
        L.hline(0, 15, 15, "k")
    if motif:
        motif(L)
    return L.a.copy()


def wall_lamp(L):
    """A hanging lamp against the shelves: a small gold glow."""
    L.vline(8, 0, 5, "g1")
    L.rect(5, 6, 6, 3, "g1")
    L.hline(5, 10, 6, "g3")
    L.rect(7, 3, 2, 3, "g2")
    L.px(7, 2, "g3")


def owl_niche(L):
    L.rect(3, 1, 10, 14, "n0")
    L.hline(3, 12, 1, "g1")
    m = m_ellipse(mask(16, 16), 5, 4, 11, 14)
    m_poly(m, [(5, 6), (5, 2), (8, 5)])
    m_poly(m, [(11, 6), (11, 2), (8, 5)])
    shade(L, m, ["n2", "n3", "p1", "p2"], light=0.35)
    L.px(6, 7, "g3"), L.px(9, 7, "g3")
    L.hline(4, 12, 14, "g1")


# ---------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------

def olive_tree():
    """The sacred olive, 3 x 4: a gnarled trunk out of the rostrum's marble
    planter, a silver-green crown spreading over the shelves."""
    s = Struct("olive", "Athena's sacred olive", 3, 4, "props", walk=["XXX"] * 4,
               names={"crown": (1, 0), "planter": (1, 3)})
    for cy in range(3):
        for cx in range(3):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = wall_cell(cy, cx + 1)
    for cx in range(3):
        s.B.a[48:64, cx * 16:cx * 16 + 16] = floor_cell(cx, 1, shade_px)
    M = s.M
    # the planter, a marble drum
    pl = m_rect(mask(48, 64), 8, 52, 32, 11)
    shade(M, pl, ["s2", "v2", "v3", "v3"], light=0.25)
    M.hline(8, 39, 52, "v3")
    M.hline(8, 39, 56, "s2")
    ink_edge(M, pl, "k")
    # the trunk, twisted, two limbs
    tr = mask(48, 64)
    m_poly(tr, [(19, 52), (21, 40), (18, 32), (22, 24), (27, 24), (29, 33), (26, 42), (29, 52)])
    m_poly(tr, [(21, 30), (12, 20), (15, 18), (24, 27)])
    m_poly(tr, [(26, 30), (36, 18), (38, 21), (28, 32)])
    shade(M, tr, ["t0", "t1", "t2"], light=0.3)
    M.line(23, 50, 22, 36, "t0")
    M.line(25, 46, 27, 34, "t2")
    ink_edge(M, tr, "k")
    # the crown: overlapping leaf masses, lit from the top left
    crown = mask(48, 64)
    for (x0, y0, x1, y1) in ((2, 6, 22, 24), (14, 0, 36, 18), (26, 5, 46, 24), (8, 14, 28, 30), (22, 14, 42, 30)):
        m_ellipse(crown, x0, y0, x1, y1)
    for y in range(64):
        for x in range(48):
            if crown[y, x]:
                v = (x * 0.4 + y * 0.9 + (P.h("ol", x // 3, y // 3) % 7)) / 30
                c = "l3" if v < 0.55 else "l2" if v < 0.95 else "l1" if v < 1.25 else "l0"
                M.px(x, y, c)
    # leaf glints and olives
    for i in range(40):
        x = P.h("lg", i) % 46 + 1
        y = P.h("lgy", i) % 28 + 1
        if crown[y, x] and crown[y, x + 1]:
            M.px(x, y, "s2" if i % 3 else "l3")
            M.px(x + 1, y, "l2")
    for i in range(12):
        x = P.h("ov", i) % 40 + 4
        y = P.h("ovy", i) % 18 + 10
        if crown[y, x]:
            M.px(x, y, "n1")
            M.px(x, y - 1, "n2")
    ink_edge(M, crown, "k", lit="l0")
    return s


def owl_statue():
    """A marble owl on a pedestal, 1 x 2: the top walk-behind."""
    s = Struct("owl", "A marble owl on its pedestal", 1, 2, "props", walk=["X", "X"])
    s.B.a[0:16] = floor_cell(0, 0)
    s.B.a[16:32] = floor_cell(0, 1)
    M = s.M
    ped = m_rect(mask(16, 32), 3, 18, 10, 13)
    shade(M, ped, ["s1", "s2", "s3", "v4"], light=0.25)
    M.rect(2, 16, 12, 3, "s3")
    M.hline(2, 13, 16, "v4")
    M.rect(2, 29, 12, 3, "s2")
    M.hline(4, 11, 23, "g1")
    body = m_ellipse(mask(16, 32), 3, 4, 12, 16)
    m_poly(body, [(3, 6), (4, 1), (7, 5)])
    m_poly(body, [(12, 6), (11, 1), (8, 5)])
    shade(M, body, ["s1", "s2", "s3", "v4"], light=0.3)
    M.rect(4, 6, 3, 3, "v4"), M.rect(9, 6, 3, 3, "v3")
    M.rect(5, 7, 2, 2, "g2"), M.rect(9, 7, 2, 2, "g2")
    M.px(6, 7, "k"), M.px(10, 7, "k")
    M.px(7, 10, "g1"), M.px(8, 10, "g1")
    for y in (12, 14):
        M.hline(5, 10, y, "s1")
    ink_edge(M, body | ped | m_rect(mask(16, 32), 2, 16, 12, 3) | m_rect(mask(16, 32), 2, 29, 12, 3), "k")
    return s


def lampstand(lit):
    """A tall bronze lampstand on the aisle, 1 x 2; burning low or bright."""
    s = Struct(f"lamp_{'lit' if lit else 'dim'}", "A lampstand on the aisle", 1, 2, "props", walk=["X", "X"],
               names={"top": (0, 0), "base": (0, 1)})
    s.B.a[0:16] = floor_cell(0, 0)
    s.B.a[16:32] = floor_cell(0, 1)
    M = s.M
    M.vline(7, 10, 29, "b1")
    M.vline(8, 10, 29, "g1")
    for y in (14, 20, 26):
        M.hline(6, 9, y, "g2")
    for x0, x1 in ((7, 3), (8, 12)):
        for t in range(5):
            M.px(round(x0 + (x1 - x0) * t / 4), 27 + t, "b1")
    M.hline(2, 4, 31, "b0"), M.hline(11, 13, 31, "b0")
    # the lamp dish and its three nozzles
    dish = m_ellipse(mask(16, 32), 2, 6, 13, 12)
    shade(M, dish, ["b0", "b1", "g1", "g2", "g3"], light=0.3)
    ink_edge(M, dish, "k")
    if lit:
        for x, hgt in ((3, 4), (8, 7), (12, 4)):
            fl = m_poly(mask(16, 32), [(x - 2, 7), (x, 7 - hgt), (x + 2, 7)])
            flat(M, fl, "f2")
            M.vline(x, 7 - hgt + 2, 6, "f3")
            M.px(x, 7 - hgt, "f1")
    else:
        for x in (3, 8, 12):
            M.px(x, 5, "f1")
            M.px(x, 4, "f2") if x == 8 else None
    return s


def scroll_case():
    """A cabinet of scrolls against the wall, 2 x 2."""
    s = Struct("scroll_case", "A cabinet of scrolls", 2, 2, "props", walk=["XX", "XX"])
    for cy in range(2):
        for cx in range(2):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = floor_cell(cx, cy)
    M = s.M
    body = m_rect(mask(32, 32), 1, 2, 30, 29)
    flat(M, body, "n1")
    M.rect(1, 2, 30, 3, "g1")
    M.hline(1, 30, 2, "g2")
    for r, yy in enumerate((6, 14, 22)):
        M.rect(3, yy, 26, 7, "n0")
        for i in range(6):
            x = 4 + i * 4
            col = "p2" if (i + r) % 3 else "r1"
            M.rect(x, yy + 3, 3, 3, col)
            M.px(x + 1, yy + 4, "p1")
            M.px(x, yy + 3, "g3" if col == "r1" else "p2")
        M.hline(3, 28, yy + 7, "g1")
    M.rect(1, 29, 30, 2, "n2")
    ink_edge(M, body, "k")
    return s


def scroll_basket():
    s = Struct("basket", "A basket of scrolls", 1, 1, "props", walk=["X"])
    s.B.a[:] = floor_cell(1, 1)
    M = s.M
    b = m_ellipse(mask(16, 16), 2, 5, 13, 15)
    shade(M, b, ["b0", "b1", "g1", "g2"], light=0.3)
    for i, x in enumerate((4, 7, 10)):
        M.rect(x, 2 + i % 2, 2, 6, "v4")
        M.px(x, 2 + i % 2, "v2")
    for y in range(8, 14, 2):
        M.hline(3, 12, y, "b0")
    ink_edge(M, b, "k")
    return s


def reading_table():
    s = Struct("table", "A reading table with an open scroll", 2, 1, "props", walk=["XX"])
    for cx in range(2):
        s.B.a[:, cx * 16:cx * 16 + 16] = floor_cell(cx, 0)
    M = s.M
    top = m_rect(mask(32, 16), 1, 3, 30, 6)
    shade(M, top, ["b0", "b1", "g1", "g2"], light=0.2)
    M.rect(3, 9, 2, 6, "b0"), M.rect(27, 9, 2, 6, "b0")
    M.rect(8, 2, 16, 5, "v4")
    M.rect(7, 2, 2, 6, "v2"), M.rect(23, 2, 2, 6, "v2")
    for y in (3, 5):
        M.hline(10, 21, y, "v1")
    ink_edge(M, top, "k")
    return s


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def one(key, title, arr_b, walk=".", mb=None):
    s = Struct(key, title, 1, 1, "kit", walk=[walk])
    s.B.a[:] = arr_b
    if mb:
        s.behaviors[(0, 0)] = mb
    return s


def kit():
    out = []
    for cy in range(2):
        for cx in range(2):
            out.append(one(f"floor_{cx}_{cy}", "Ivory marble", floor_cell(cx, cy)))
            out.append(one(f"shade_{cx}_{cy}", "Ivory marble in the shade", floor_cell(cx, cy, shade_px)))
    out.append(one("runner_l", "The aisle's olive band", runner_cell("l")))
    out.append(one("runner_r", "The aisle's olive band", runner_cell("r")))
    void = Layer(16, 16)
    void.rect(0, 0, 16, 16, "k")
    out.append(one("void", "Outside the hall", void.a.copy(), walk="X"))
    t = Layer(16, 16)
    t.a[:] = floor_cell(0, 0)
    t.rect(1, 10, 14, 6, "o1")
    t.hline(1, 14, 10, "g2")
    t.vline(0, 0, 15, "k"), t.vline(15, 0, 15, "k")
    out.append(one("mat", "The south door's sill", t.a.copy(), walk="v"))
    sh = Layer(16, 16)
    sh.rect(0, 0, 16, 16, "k")
    sh.rect(1, 0, 14, 14, "n1")
    sh.vline(7, 0, 13, "k")
    sh.hline(1, 14, 0, "g1")
    out.append(one("mat_shut", "The south door, shut", sh.a.copy(), walk="X"))
    out.append(roundel())
    return out


def walls():
    out = []
    for row in range(3):
        for v in range(2):
            out.append(one(f"wall{row}_{v}", f"The north wall, row {row}", wall_cell(row, v), walk="X"))
    out.append(one("wall1_lamp", "A lamp hung on the shelves", wall_cell(1, 0, wall_lamp), walk="X"))
    out.append(one("wall1_owl", "An owl in a niche", wall_cell(1, 1, owl_niche), walk="X"))
    for side in ("w", "e"):
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, wall_px(x + 8, y + 8))
        L.rect(12 if side == "w" else 0, 0, 4, 16, "n0")
        L.vline(12 if side == "w" else 3, 0, 15, "g1")
        out.append(one(f"side_{side}", f"The {side} wall", L.a.copy(), walk="X"))
    for state in ("shut", "open"):
        for row in (1, 2):
            L = Layer(16, 16)
            L.a[:] = wall_cell(row, 0)
            top = 3 if row == 1 else 0
            if state == "shut":
                L.rect(2, top, 12, 16 - top, "b1")
                L.vline(7, top, 15, "k")
                for y in range(top + 2, 16, 5):
                    L.rect(4, y, 2, 2, "g2"), L.rect(10, y, 2, 2, "g2")
            else:
                L.rect(2, top, 12, 16 - top, "k")
                if row == 2:
                    L.rect(3, 11, 10, 5, "n0")
            if row == 1:
                L.rect(1, 0, 14, 3, "g1")
                L.hline(1, 14, 0, "g3")
            L.vline(1, top, 15, "g2")
            L.vline(14, top, 15, "g1")
            walk = "X" if (state == "shut" or row == 1) else "."
            out.append(one(f"door_{state}{row}", f"The library gate, {state}", L.a.copy(), walk=walk))
    return out


def dais():
    out = []

    def surf(X, Y):
        x, y = X % 16, Y % 16
        if x == 0 or y == 0:
            return "g1"
        if x == 1 or y == 1:
            return "v4"
        if x == 15 or y == 15:
            return "v1"
        if 5 <= x <= 10 and 5 <= y <= 10 and abs(x - 7.5) + abs(y - 7.5) < 3:
            return "o2"
        return "v3"

    for part in "lmr":
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, surf(x, y))
        if part == "l":
            L.rect(0, 0, 3, 16, "g1"), L.vline(1, 0, 15, "g2")
        if part == "r":
            L.rect(13, 0, 3, 16, "g1"), L.vline(14, 0, 15, "g2")
        out.append(one(f"dais_{part}", "The rostrum", L.a.copy()))
        R = Layer(16, 16)
        R.rect(0, 0, 16, 16, "s2")
        R.hline(0, 15, 0, "v4")
        R.rect(0, 1, 16, 2, "s3")
        R.hline(0, 15, 3, "s1")
        for x in range(0, 16, 4):
            R.rect(x + 1, 5, 2, 7, "s3")
            R.vline(x + 3, 5, 11, "s1")
        R.hline(0, 15, 13, "o1")
        R.hline(0, 15, 14, "s1")
        R.hline(0, 15, 15, "k")
        out.append(one(f"riser_{part}", "The rostrum's riser", R.a.copy(), walk="X"))
    S = Layer(16, 16)
    for i in range(4):
        S.rect(0, i * 4, 16, 4, ["v4", "s3", "s3", "s2"][i])
        S.hline(0, 15, i * 4 + 3, "s1")
    out.append(one("steps", "The rostrum steps", S.a.copy()))
    return out


def props():
    return [olive_tree(), owl_statue(), lampstand(False), lampstand(True), scroll_case(), scroll_basket(),
            reading_table()]


SECTION_ROWS = {"kit": 0, "walls": 4, "dais": 8, "props": 10}


def sections():
    return [("kit", kit()), ("walls", walls()), ("dais", dais()), ("props", props())]


SEAT = P.Seat("gTileset_SeatAthena", "seat_athena", C, GROUPS, sections, SECTION_ROWS)
