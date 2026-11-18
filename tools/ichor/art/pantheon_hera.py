"""gTileset_SeatHera: Olympias's seat, Hera's peacock hall (design/maps/Olympus_Pantheon.md).

A royal hall in plum and gold: columns painted with peacock feathers, their
eyes the hundred eyes of Argos that Hera set in the peacock's tail; torches
on bronze stands up the aisle (cold until Olympias rises, then they catch pair
by pair from the door to her feet); the gold throne on its dais under a great
fanned peacock tail; bronze serpents coiled either side of the throne (Hera
raised the Hydra and set Ladon on the golden apples); pomegranates, her fruit,
in gold urns.

Palette groups: floor (plum marble, gold inlay), wall (deep purple, gold key,
ivory), peacock (feathers and their eyes), torch (bronze and fire), throne
(gold, cushions, the serpents).
"""
from __future__ import annotations

import pantheon_lib as P
from pantheon_lib import (Struct, Layer, flagstones, flat, ink_edge, m_ellipse, m_poly, m_rect, mask, shade,
                          tiled)

C = {
    "k": (24, 8, 24),
    "p0": (56, 24, 56), "p1": (88, 40, 88), "p2": (120, 56, 112), "p3": (144, 80, 136), "p4": (176, 112, 160),
    "g1": (176, 120, 40), "g2": (232, 184, 72), "g3": (248, 232, 152),
    "q0": (32, 16, 40), "q1": (56, 32, 72), "q2": (80, 48, 96), "q3": (112, 72, 128), "w1": (232, 224, 232),
    # peacock
    "e1": (16, 88, 96), "e2": (32, 144, 136), "e3": (80, 200, 168),
    "u0": (16, 24, 64), "u1": (24, 48, 136), "u2": (48, 96, 200), "n1": (40, 112, 48), "n2": (104, 176, 64),
    # torch
    "b0": (80, 48, 24), "b1": (136, 88, 40), "f1": (224, 72, 32), "f2": (248, 152, 48), "f3": (248, 216, 112),
    "f4": (248, 248, 216),
    # pomegranate red
    "r1": (152, 24, 48), "r2": (216, 56, 72),
}

GROUPS = {
    "floor": ["k", "p0", "p1", "p2", "p3", "p4", "g1", "g2", "g3", "q1", "e1", "e2"],
    "wall": ["k", "q0", "q1", "q2", "q3", "g1", "g2", "g3", "w1", "p2", "p3", "e1", "e2", "u1", "u2"],
    "peacock": ["k", "e1", "e2", "e3", "u0", "u1", "u2", "n1", "n2", "g1", "g2", "g3", "q0", "q1", "q2"],
    "torch": ["k", "b0", "b1", "g1", "g2", "g3", "f1", "f2", "f3", "f4", "q1", "q2", "p1", "p2", "p3"],
    "throne": ["k", "g1", "g2", "g3", "q1", "q2", "q3", "w1", "p1", "p2", "p3", "e1", "e2", "e3", "r2"],
    "fruit": ["k", "g1", "g2", "g3", "r1", "r2", "n1", "n2", "p1", "p2", "p3", "q1", "b0", "b1"],
}

GOLD = ["b0", "g1", "g2", "g3"]


def floor_px(X, Y):
    """Square plum slabs laid as a checker, light and dark, with a gold stud
    where four meet and a soft cloud vein in the light ones."""
    x, y = X % 32, Y % 32
    ix, iy = x % 16, y % 16
    light = ((x // 16) + (y // 16)) % 2 == 0
    if (ix, iy) in ((0, 0), (1, 0), (0, 1), (15, 0), (0, 15)):
        return "g2" if (ix, iy) == (0, 0) else "g1"
    if ix == 0 or iy == 0:
        return "p0"
    if ix == 1 or iy == 1:
        return "p4" if light else "p2"
    if ix == 15 or iy == 15:
        return "p1"
    if light:
        if (ix * 2 + iy * 3 + P.h("hv", X // 16, Y // 16) % 5) % 13 == 0 and iy % 2 == 0:
            return "p4"
        return "p3"
    if (ix + iy * 2) % 11 == 0 and ix % 2:
        return "p1"
    return "p2"


def floor_cell(cx, cy, fn=floor_px):
    return tiled(fn, ox=cx * 16, oy=cy * 16)


def shade_px(X, Y):
    c = floor_px(X, Y)
    if Y % 16 < 7:
        return {"p4": "p2", "p3": "p1", "p2": "p1", "p1": "p0", "p0": "k", "g2": "g1"}.get(c, c)
    return c


def runner_cell(part):
    """The aisle runner: deep purple, gold-bordered, a peacock-eye in the middle."""
    L = Layer(16, 16)
    L.rect(0, 0, 16, 16, "q1")
    for y in range(16):
        for x in range(16):
            if (x + y) % 4 == 0:
                L.px(x, y, "p1")
    if part == "l":
        L.vline(0, 0, 15, "k"), L.vline(1, 0, 15, "g1"), L.vline(2, 0, 15, "g2"), L.vline(3, 0, 15, "g1")
    if part == "r":
        L.vline(15, 0, 15, "k"), L.vline(14, 0, 15, "g1"), L.vline(13, 0, 15, "g2"), L.vline(12, 0, 15, "g1")
    if part == "eye":
        m = m_ellipse(mask(16, 16), 3, 1, 12, 14)
        flat(L, m, "e1")
        flat(L, m_ellipse(mask(16, 16), 4, 3, 11, 13), "e2")
        flat(L, m_ellipse(mask(16, 16), 5, 6, 10, 12), "g2")
        flat(L, m_ellipse(mask(16, 16), 6, 7, 9, 11), "q1")
    return L.a.copy()


def wall_px(X, Y):
    return flagstones(X, Y, ("q0", "q1", "q2", "q3"), "k", "hw", slab_w=16, slab_h=8, period=32)


def key_band(L, y0):
    """A gold Greek key on purple, 6 px tall."""
    L.rect(0, y0, 16, 6, "q1")
    for x in range(16):
        u = x % 8
        if u in (0, 1, 2, 3, 4):
            L.px(x, y0 + 1, "g2")
        if u == 4:
            L.vline(x, y0 + 1, y0 + 4, "g2")
        if u in (2, 3, 4):
            L.px(x, y0 + 4, "g2")
        if u == 2:
            L.px(x, y0 + 3, "g2")
        if u in (5, 6, 7):
            L.px(x, y0 + 4, "g1") if u == 7 else None
    L.hline(0, 15, y0, "g1")
    L.hline(0, 15, y0 + 5, "g1")


def wall_cell(row, cx, motif=None):
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            L.px(x, y, wall_px(cx * 16 + x, row * 16 + y))
    if row == 0:
        L.rect(0, 0, 16, 4, "q0")
        key_band(L, 5)
        L.rect(0, 11, 16, 5, "q2")
        L.hline(0, 15, 11, "w1")
        for x in range(1, 16, 4):
            L.rect(x, 12, 2, 3, "q3")
        L.hline(0, 15, 15, "k")
    if row == 2:
        L.rect(0, 9, 16, 7, "q1")
        L.hline(0, 15, 9, "g2")
        L.hline(0, 15, 10, "g1")
        L.hline(0, 15, 15, "k")
    if motif:
        motif(L)
    return L.a.copy()


def feather_eye(L, x, y, big=False, heart="u0"):
    """One peacock eye: a teal ring, blue heart, gold rim."""
    w = 7 if big else 5
    h_ = 9 if big else 7
    flat(L, m_ellipse(mask(L.w, L.h), x, y, x + w, y + h_), "e2")
    flat(L, m_ellipse(mask(L.w, L.h), x + 1, y + 1, x + w - 1, y + h_ - 1), "g2")
    flat(L, m_ellipse(mask(L.w, L.h), x + 1, y + 2, x + w - 1, y + h_ - 1), "u2")
    flat(L, m_ellipse(mask(L.w, L.h), x + 2, y + 3, x + w - 2, y + h_ - 2), heart)


def wall_feather(L):
    """A painted feather on the wall."""
    L.line(8, 15, 8, 4, "g1")
    for t in range(4, 14):
        L.px(8 - (14 - t) // 3, t, "e2")
        L.px(8 + (14 - t) // 3, t, "e1")
    feather_eye(L, 5, 1, heart="u1")


# ---------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------

def peacock_column():
    """A column painted with peacock feathers, 1 x 3, gold capital."""
    s = Struct("pcolumn", "A peacock-feather column", 1, 3, "props", walk=["X", "X", "X"],
               names={"capital": (0, 0), "shaft": (0, 1), "base": (0, 2)})
    for cy in range(3):
        s.B.a[cy * 16:cy * 16 + 16] = floor_cell(0, cy)
    M = s.M
    sh = m_rect(mask(16, 48), 3, 6, 10, 36)
    shade(M, sh, ["q0", "e1", "e2", "e3", "e2"], light=0.3)
    # feathers sweeping up the shaft: barbs and eyes
    for y in range(8, 42, 2):
        M.px(4 + (y // 2) % 3, y, "n2")
        M.px(10 - (y // 2) % 3, y + 1, "n1")
    for i, y in enumerate((8, 20, 31)):
        feather_eye(M, 4 + (i % 2), y, big=True)
    cap = m_rect(mask(16, 48), 1, 1, 14, 5)
    shade(M, cap, ["g1", "g1", "g2", "g3"], light=0.3)
    M.px(2, 5, "g1"), M.px(13, 5, "g1")
    M.hline(2, 13, 0, "g3")
    bs = m_rect(mask(16, 48), 1, 42, 14, 5)
    shade(M, bs, ["g1", "g1", "g2", "g3"], light=0.3)
    ink_edge(M, sh | cap | bs, "k")
    return s


def torch(lit):
    """A torch on a tall bronze stand up the aisle, 1 x 2."""
    s = Struct(f"torch_{'lit' if lit else 'cold'}", "A torch up the aisle", 1, 2, "props", walk=["X", "X"],
               names={"top": (0, 0), "base": (0, 1)})
    s.B.a[0:16] = floor_cell(1, 0)
    s.B.a[16:32] = floor_cell(1, 1)
    M = s.M
    M.vline(7, 10, 29, "b1")
    M.vline(8, 10, 29, "g1")
    for x0, x1 in ((7, 3), (8, 12)):
        for t in range(5):
            M.px(round(x0 + (x1 - x0) * t / 4), 27 + t, "b0")
    cup = m_poly(mask(16, 32), [(3, 7), (12, 7), (10, 12), (5, 12)])
    shade(M, cup, ["b0", "b1", "g1", "g2", "g3"], light=0.3)
    ink_edge(M, cup, "k")
    if lit:
        fl = m_poly(mask(16, 32), [(3, 7), (5, 2), (7, 4), (8, 0), (10, 3), (11, 2), (12, 7)])
        for y in range(32):
            for x in range(16):
                if fl[y, x]:
                    M.px(x, y, "f4" if y > 4 and 6 < x < 10 else "f3" if y > 3 else "f2" if y > 1 else "f1")
    else:
        M.hline(4, 11, 6, "q1")
        M.hline(5, 10, 5, "q2")
    return s


def brazier(lit):
    s = Struct(f"brazier_{'lit' if lit else 'cold'}", "A brazier at the queen's feet", 1, 2, "props",
               walk=["X", "X"], names={"top": (0, 0), "base": (0, 1)})
    s.B.a[0:16] = floor_cell(0, 0, dais_px)
    s.B.a[16:32] = floor_cell(0, 1, dais_px)
    M = s.M
    bowl = m_ellipse(mask(16, 32), 0, 8, 15, 20)
    bowl[:13] = False
    m_rect(bowl, 0, 12, 16, 2)
    shade(M, bowl, ["b0", "g1", "g2", "g3"], light=0.3)
    stand = m_poly(mask(16, 32), [(6, 20), (10, 20), (12, 31), (4, 31)])
    shade(M, stand, ["b0", "b1", "g1", "g2"], light=0.3)
    ink_edge(M, bowl | stand, "k")
    if lit:
        fl = m_poly(mask(16, 32), [(1, 12), (3, 4), (5, 7), (8, 0), (11, 6), (13, 3), (14, 12)])
        for y in range(32):
            for x in range(16):
                if fl[y, x]:
                    M.px(x, y, "f4" if y > 8 and 5 < x < 11 else "f3" if y > 6 else "f2" if y > 3 else "f1")
    else:
        M.hline(2, 13, 12, "q1")
        M.hline(3, 12, 11, "q2")
    return s


def dais_px(X, Y):
    x, y = X % 16, Y % 16
    if x == 0 or y == 0:
        return "g1"
    if x == 1 or y == 1:
        return "g2"
    if x == 15 or y == 15:
        return "q1"
    if (x, y) in ((7, 7), (8, 8), (7, 8), (8, 7)):
        return "g1"
    return "q3" if (x + y) in (9, 10, 21, 22) else "q2"


def throne():
    """Hera's gold throne under a great fanned peacock tail, 7 x 4: the fan
    fills the wall behind, the throne stands on the dais row."""
    import math
    s = Struct("throne", "Hera's throne under the peacock's fan", 7, 4, "props",
               walk=["XXXXXXX", "XXXXXXX", "XXXXXXX", "--XXX--"], names={"seat": (3, 3)})
    for cy in range(3):
        for cx in range(7):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = wall_cell(cy, cx)
    for cx in range(7):
        s.B.a[48:64, cx * 16:cx * 16 + 16] = floor_cell(cx, 1, dais_px)
    M = s.M
    W, H = 112, 64
    cx0, cy0, rx, ry = 56, 47, 55, 46
    fan = mask(W, H)
    for y in range(H):
        for x in range(W):
            dx, dy = (x - cx0) / rx, (cy0 - y) / ry
            if dy > -0.02 and dx * dx + dy * dy < 1 and y < 47:
                fan[y, x] = True
    for y in range(H):
        for x in range(W):
            if not fan[y, x]:
                continue
            dx, dy = (x - cx0) / rx, (cy0 - y) / ry
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            spoke = (a * 18 / math.pi) % 1
            c = "e1" if spoke < 0.16 else "n1" if r < 0.42 else "e2" if r < 0.7 else "n2" if r < 0.9 else "e1"
            if r > 0.95:
                c = "g1"
            M.px(x, y, c)
    for ring, n, big in ((0.8, 15, True), (0.56, 11, True), (0.34, 7, False)):
        for i in range(n):
            a = math.pi * (i + 0.5) / n
            x = int(cx0 + ring * rx * math.cos(a)) - (4 if big else 3)
            y = int(cy0 - ring * ry * math.sin(a)) - (5 if big else 4)
            if y > 0:
                feather_eye(M, x, y, big=big)
    ink_edge(M, fan, "k")
    T = Layer(W, H)
    o = 32
    back = m_poly(mask(W, H), [(o + 10, 60), (o + 10, 22), (o + 14, 14), (o + 24, 10), (o + 34, 14), (o + 38, 22),
                               (o + 38, 60)])
    shade(T, back, ["g1", "g2", "g2", "g3"], light=0.3)
    flat(T, m_poly(mask(W, H), [(o + 14, 52), (o + 14, 24), (o + 18, 18), (o + 24, 16), (o + 30, 18), (o + 34, 24),
                                (o + 34, 52)]), "q2")
    flat(T, m_poly(mask(W, H), [(o + 16, 50), (o + 16, 25), (o + 20, 20), (o + 24, 19), (o + 28, 20), (o + 32, 25),
                                (o + 32, 50)]), "q3")
    feather_eye(T, o + 21, 25, big=True, heart="q1")
    arms = m_rect(mask(W, H), o + 6, 44, 8, 8) | m_rect(mask(W, H), o + 34, 44, 8, 8)
    shade(T, arms, ["g1", "g2", "g3"], light=0.3)
    seat = m_rect(mask(W, H), o + 10, 50, 28, 6)
    flat(T, seat, "q3")
    T.hline(o + 10, o + 37, 50, "w1")
    legs = m_rect(mask(W, H), o + 8, 56, 6, 8) | m_rect(mask(W, H), o + 34, 56, 6, 8)
    shade(T, legs, ["g1", "g2", "g3"], light=0.3)
    ink_edge(T, back | arms | seat | legs, "k")
    M.paste(T.a, 0, 0)
    return s


def serpent():
    """A bronze serpent coiled on a plinth, raised to strike, 1 x 2."""
    s = Struct("serpent", "A coiled bronze serpent", 1, 2, "props", walk=["X", "X"])
    s.B.a[0:16] = floor_cell(0, 0, dais_px)
    s.B.a[16:32] = floor_cell(0, 1, dais_px)
    M = s.M
    pl = m_rect(mask(16, 32), 2, 24, 12, 8)
    shade(M, pl, ["q1", "q2", "q3", "w1"], light=0.25)
    coil = m_ellipse(mask(16, 32), 2, 16, 13, 25)
    m_ellipse(coil, 4, 12, 12, 19)
    shade(M, coil, ["e1", "e2", "e3", "g2"], light=0.3)
    for y in (15, 18, 21):
        M.hline(4, 11, y, "e1")
    neck = m_poly(mask(16, 32), [(9, 13), (6, 6), (7, 2), (11, 1), (12, 4), (9, 6), (11, 13)])
    shade(M, neck, ["e1", "e2", "e3", "g2"], light=0.35)
    M.px(9, 2, "r2")
    M.px(12, 5, "r2"), M.px(13, 6, "r2")
    ink_edge(M, coil | neck | pl, "k")
    return s


def urn():
    """A gold urn heaped with pomegranates, 1 x 2."""
    s = Struct("urn", "A gold urn of pomegranates", 1, 2, "props", walk=["X", "X"])
    s.B.a[0:16] = floor_cell(0, 0)
    s.B.a[16:32] = floor_cell(0, 1)
    M = s.M
    body = m_ellipse(mask(16, 32), 2, 12, 13, 28)
    m_rect(body, 5, 27, 6, 4)
    m_rect(body, 3, 10, 10, 3)
    shade(M, body, ["b0", "g1", "g2", "g3"], light=0.3)
    M.hline(3, 12, 18, "r1")
    M.hline(4, 11, 19, "b1")
    fr = mask(16, 32)
    for (x, y) in ((4, 5), (8, 3), (11, 6), (6, 8), (10, 9)):
        m_ellipse(fr, x - 3, y - 3, x + 2, y + 2)
    shade(M, fr, ["r1", "r1", "r2", "r2"], light=0.3)
    for (x, y) in ((4, 2), (8, 0), (11, 3)):
        M.px(x, y, "n2"), M.px(x + 1, y, "n1")
    ink_edge(M, body | fr, "k")
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
            out.append(one(f"floor_{cx}_{cy}", "Plum marble", floor_cell(cx, cy)))
            out.append(one(f"shade_{cx}_{cy}", "Plum marble in the shade", floor_cell(cx, cy, shade_px)))
    for part in ("l", "m", "r", "eye"):
        out.append(one(f"runner_{part}", "The aisle runner", runner_cell(part)))
    void = Layer(16, 16)
    void.rect(0, 0, 16, 16, "k")
    out.append(one("void", "Outside the hall", void.a.copy(), walk="X"))
    t = Layer(16, 16)
    t.a[:] = runner_cell("m")
    t.rect(0, 11, 16, 5, "g1")
    t.hline(0, 15, 11, "g2")
    t.vline(0, 0, 15, "k"), t.vline(15, 0, 15, "k")
    out.append(one("mat", "The south door's gold sill", t.a.copy(), walk="v"))
    sh = Layer(16, 16)
    sh.rect(0, 0, 16, 16, "k")
    sh.rect(1, 0, 14, 14, "q1")
    sh.vline(7, 0, 13, "k")
    sh.hline(1, 14, 0, "g1")
    out.append(one("mat_shut", "The south door, shut", sh.a.copy(), walk="X"))
    return out


def walls():
    out = []
    for row in range(3):
        for v in range(2):
            out.append(one(f"wall{row}_{v}", f"The north wall, row {row}", wall_cell(row, v), walk="X"))
    out.append(one("wall1_feather", "A painted peacock feather", wall_cell(1, 0, wall_feather), walk="X"))
    for side in ("w", "e"):
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, wall_px(x + 8, y + 8))
        L.rect(12 if side == "w" else 0, 0, 4, 16, "q0")
        L.vline(12 if side == "w" else 3, 0, 15, "g1")
        out.append(one(f"side_{side}", f"The {side} wall", L.a.copy(), walk="X"))
    for state in ("shut", "open"):
        for row in (1, 2):
            L = Layer(16, 16)
            L.a[:] = wall_cell(row, 0)
            top = 3 if row == 1 else 0
            if state == "shut":
                L.rect(2, top, 12, 16 - top, "q3")
                L.vline(7, top, 15, "k")
                L.vline(8, top, 15, "q1")
                for y in range(top + 2, 16, 5):
                    L.rect(4, y, 2, 2, "g2"), L.rect(10, y, 2, 2, "g2")
            else:
                L.rect(2, top, 12, 16 - top, "k")
                if row == 2:
                    L.rect(3, 11, 10, 5, "q0")
            if row == 1:
                L.rect(1, 0, 14, 3, "g1")
                L.hline(1, 14, 0, "g3")
            L.vline(1, top, 15, "g2")
            L.vline(14, top, 15, "g1")
            walk = "X" if (state == "shut" or row == 1) else "."
            mb = "MB_NON_ANIMATED_DOOR" if (state == "open" and row == 2) else None
            out.append(one(f"door_{state}{row}", f"The summit door, {state}", L.a.copy(), walk=walk, mb=mb))
    return out


def dais():
    out = []
    for part in "lmr":
        L = Layer(16, 16)
        L.a[:] = floor_cell(0, 0, dais_px)
        if part == "l":
            L.rect(0, 0, 3, 16, "q0"), L.vline(1, 0, 15, "g2")
        if part == "r":
            L.rect(13, 0, 3, 16, "q0"), L.vline(14, 0, 15, "g2")
        out.append(one(f"dais_{part}", "The queen's dais", L.a.copy()))
        R = Layer(16, 16)
        R.rect(0, 0, 16, 16, "p1")
        R.hline(0, 15, 0, "g3")
        R.rect(0, 1, 16, 2, "g2")
        R.hline(0, 15, 3, "g1")
        for x in range(0, 16, 8):
            R.rect(x + 2, 6, 4, 5, "p2")
            R.px(x + 3, 7, "p3")
        R.hline(0, 15, 13, "g1")
        R.hline(0, 15, 15, "k")
        out.append(one(f"riser_{part}", "The dais's riser", R.a.copy(), walk="X"))
    S = Layer(16, 16)
    for i in range(4):
        S.rect(0, i * 4, 16, 4, ["p4", "p3", "p3", "p2"][i])
        S.hline(0, 15, i * 4 + 3, "p1")
        S.hline(0, 15, i * 4, "g2" if i == 0 else "p4")
    S.rect(5, 0, 6, 16, "q1")
    S.vline(5, 0, 15, "g1"), S.vline(10, 0, 15, "g1")
    out.append(one("steps", "The dais steps", S.a.copy()))
    return out


def props():
    return [throne(), peacock_column(), torch(False), torch(True), brazier(False), brazier(True), serpent(), urn()]


SECTION_ROWS = {"kit": 0, "walls": 4, "dais": 8, "props": 10}


def sections():
    return [("kit", kit()), ("walls", walls()), ("dais", dais()), ("props", props())]


SEAT = P.Seat("gTileset_SeatHera", "seat_hera", C, GROUPS, sections, SECTION_ROWS)
