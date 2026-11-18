"""gTileset_SeatPoseidon: Themistokles's seat, the sea hall of Poseidon (design/maps/Olympus_Pantheon.md).

The hall is a basin of sea water with a causeway up its middle: white marble
coping round the water, coral columns standing out of it, the trireme of
Salamis moored on one side and a leaping bronze dolphin on the other, the
colossal trident planted at the head of the hall over the admiral's dais, a
wave frieze and scallop niches along a deep-sea wall.

Palette groups: floor (pale sea marble and the wave mosaic), wall (deep teal
stone, white waves, gold), water (the basin and its coping), coral (the
columns over water), bronze (trident, dolphin, anchors), wood (the trireme).
"""
from __future__ import annotations

import pantheon_lib as P
from pantheon_lib import (Struct, Layer, flagstones, flat, ink_edge, m_ellipse, m_poly, m_rect, mask, shade,
                          tiled)

C = {
    "k": (8, 16, 32),
    # pale sea marble
    "m0": (88, 112, 128), "m1": (128, 152, 168), "m2": (168, 192, 200), "m3": (200, 216, 224),
    "m4": (224, 232, 240), "m5": (248, 248, 248),
    "t1": (32, 112, 128), "t2": (64, 160, 168),
    # the deep-sea wall
    "d0": (8, 32, 56), "d1": (16, 56, 88), "d2": (32, 88, 120), "d3": (56, 120, 152),
    "g1": (176, 128, 48), "g2": (232, 192, 96),
    # the basin
    "w0": (8, 24, 72), "w1": (16, 48, 112), "w2": (24, 80, 152), "w3": (48, 120, 192),
    "w4": (112, 176, 224), "w5": (200, 240, 248),
    # coral
    "c0": (104, 24, 48), "c1": (176, 56, 64), "c2": (224, 104, 96), "c3": (248, 160, 136), "c4": (248, 216, 192),
    # bronze
    "b0": (56, 40, 24), "b1": (120, 80, 32), "b3": (248, 232, 160),
    "v1": (40, 104, 88), "v2": (72, 152, 120),
    # the trireme's timbers
    "o0": (56, 32, 24), "o1": (104, 64, 40), "o2": (152, 104, 64), "o3": (200, 152, 96),
}

GROUPS = {
    "floor": ["k", "m0", "m1", "m2", "m3", "m4", "m5", "t1", "t2", "d1", "d2", "w2", "w3"],
    "wall": ["k", "d0", "d1", "d2", "d3", "m3", "m4", "m5", "g1", "g2", "t1", "t2", "b1", "c2", "c3"],
    "water": ["k", "w0", "w1", "w2", "w3", "w4", "w5", "m1", "m2", "m3", "m4", "m5", "d1", "t2"],
    "coral": ["k", "c0", "c1", "c2", "c3", "c4", "w0", "w1", "w2", "w3", "w4", "w5", "m4", "t1", "t2"],
    "bronze": ["k", "b0", "b1", "g1", "g2", "b3", "v1", "v2", "w1", "w2", "w3", "w4", "w5", "m1", "m3"],
    "wood": ["k", "o0", "o1", "o2", "o3", "b1", "g1", "g2", "w1", "w2", "w3", "w4", "w5", "c1", "m5"],
}

BRONZE = ["b0", "b1", "g1", "g2", "b3"]
VERD = ["k", "v1", "v2", "g1", "g2"]


# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------

def vein(X, Y):
    # grey-blue veins wandering across the marble
    t = (X * 3 + Y * 7 + (P.h("v", X // 16, Y // 16) % 16)) % 53
    if t == 0 and P.h("vv", X // 4, Y // 4) % 3 == 0:
        return "m2"
    return None


def floor_px(X, Y):
    return flagstones(X, Y, ("m1", "m2", "m3", "m4"), "m0", "pos", slab_w=16, slab_h=16, period=32,
                      marks=(vein,))


def floor_cell(cx, cy, fn=floor_px):
    return tiled(fn, ox=cx * 16, oy=cy * 16)


def shade_px(X, Y):
    c = floor_px(X, Y)
    if Y % 16 < 7:
        return {"m5": "m3", "m4": "m2", "m3": "m2", "m2": "m1", "m1": "m0"}.get(c, c)
    return c


def wave_band(L, y0, fg="t2", dk="t1", bg=None, phase=0):
    """A running-wave meander 8 px tall at y0 (the Greek 'wave' border)."""
    for x in range(16):
        u = (x + phase) % 16
        # a curl: rise, crest, roll back
        crest = [6, 5, 4, 3, 2, 1, 1, 2, 3, 3, 2, 4, 6, 7, 7, 7][u]
        for y in range(8):
            if y >= crest:
                L.px(x, y0 + y, fg if y > crest else dk)
            elif bg:
                L.px(x, y0 + y, bg)
    for x in range(16):
        u = (x + phase) % 16
        if u in (7, 8):
            L.px(x, y0 + 3, bg or "m5")


def causeway_cell(part):
    """The causeway's mosaic: pale marble with a teal wave band down each side."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            L.px(x, y, "m4" if (x // 4 + y // 4) % 2 else "m3")
            if (x + y) % 4 == 0 and (x // 4 + y // 4) % 2:
                L.px(x, y, "m5")
    if part == "l":
        L.rect(0, 0, 4, 16, "t1")
        L.rect(1, 0, 2, 16, "t2")
        for y in range(0, 16, 4):
            L.px(2, y, "m5")
            L.px(1, y + 1, "m5")
        L.vline(4, 0, 15, "m1")
    if part == "r":
        L.rect(12, 0, 4, 16, "t1")
        L.rect(13, 0, 2, 16, "t2")
        for y in range(2, 16, 4):
            L.px(13, y, "m5")
            L.px(14, y + 1, "m5")
        L.vline(11, 0, 15, "m1")
    if part == "m":
        # a trident mosaic in dark blue, pointing north
        for y in range(3, 14):
            L.px(7, y, "w2")
            L.px(8, y, "w3")
        for x0 in (4, 11):
            L.vline(x0, 3, 7, "w2")
        L.hline(4, 11, 7, "w2")
        for x in (4, 7, 11):
            L.px(x, 2, "w3")
    return L.a.copy()


# ---------------------------------------------------------------------------
# Water
# ---------------------------------------------------------------------------

def water_px(X, Y):
    """Deep basin water: long low swells, each crest a short lit dash."""
    x, y = X % 32, Y % 32
    row = y // 4
    ph = (P.h("wr", row) % 32)
    u = (x + ph) % 32
    c = "w1"
    if y % 4 == 0:
        c = "w2" if u < 20 else "w1"
        if 4 <= u < 9:
            c = "w3"
        if u in (5, 6):
            c = "w4"
    elif y % 4 == 1 and 3 <= u < 12:
        c = "w2"
    elif y % 4 == 3 and 22 <= u < 28:
        c = "w0"
    return c


def water_cell(cx, cy):
    return tiled(water_px, ox=cx * 16, oy=cy * 16)


def coping(L, side):
    """White marble coping round the basin, drawn over a water cell's edge."""
    if side == "n":
        L.rect(0, 0, 16, 4, "m4")
        L.hline(0, 15, 0, "m5")
        L.hline(0, 15, 3, "m2")
        L.hline(0, 15, 4, "k")
        L.rect(0, 5, 16, 2, "w0")       # the coping's shade on the water
    if side == "s":
        L.hline(0, 15, 10, "w4")
        L.hline(0, 15, 11, "w5")
        L.rect(0, 12, 16, 4, "m3")
        L.hline(0, 15, 12, "m5")
        L.hline(0, 15, 15, "m1")
    if side == "w":
        L.rect(0, 0, 4, 16, "m4")
        L.vline(0, 0, 15, "m5")
        L.vline(3, 0, 15, "m2")
        L.vline(4, 0, 15, "k")
        L.rect(5, 0, 2, 16, "w0")
    if side == "e":
        L.vline(11, 0, 15, "w5")
        L.rect(12, 0, 4, 16, "m3")
        L.vline(12, 0, 15, "m5")
        L.vline(15, 0, 15, "m1")


def edge_cell(sides, cx=0, cy=0):
    L = Layer(16, 16)
    L.a[:] = water_cell(cx, cy)
    for s in sides:
        coping(L, s)
    # tidy the corners where two copings meet
    if "n" in sides and "w" in sides:
        L.rect(0, 0, 5, 5, "m4"), L.px(0, 0, "m5")
    if "n" in sides and "e" in sides:
        L.rect(11, 0, 5, 4, "m4")
    if "s" in sides and "w" in sides:
        L.rect(0, 11, 5, 5, "m3")
    if "s" in sides and "e" in sides:
        L.rect(11, 11, 5, 5, "m3")
    return L.a.copy()


# ---------------------------------------------------------------------------
# Walls
# ---------------------------------------------------------------------------

def wall_px(X, Y):
    return flagstones(X, Y, ("d0", "d1", "d2", "d3"), "k", "pw", slab_w=16, slab_h=8, period=32)


def wall_cell(row, cx, motif=None):
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            L.px(x, y, wall_px(cx * 16 + x, row * 16 + y))
    if row == 0:
        L.rect(0, 0, 16, 4, "d0")
        L.hline(0, 15, 4, "g1")
        L.hline(0, 15, 5, "g2")
        L.rect(0, 6, 16, 9, "d1")
        wave_band(L, 6, fg="m4", dk="m5", bg="d1", phase=cx * 16)
        L.hline(0, 15, 14, "g1")
        L.hline(0, 15, 15, "k")
    if row == 2:
        L.rect(0, 10, 16, 6, "d1")
        L.hline(0, 15, 10, "t2")
        L.hline(0, 15, 11, "t1")
        L.hline(0, 15, 15, "k")
    if motif:
        motif(L)
    return L.a.copy()


def shell_niche(L):
    """A scallop shell carved in a niche."""
    L.rect(2, 0, 12, 16, "d0")
    m = m_ellipse(mask(16, 16), 2, 1, 13, 14)
    m[9:] = False
    m_poly(m, [(3, 8), (8, 14), (12, 8)])
    shade(L, m, ["m3", "m4", "m5"], light=0.35)
    for i, x in enumerate((4, 6, 8, 10, 12)):
        L.line(x if x != 12 else 11, 3 if i not in (0, 4) else 6, 8, 13, "m3")
    L.px(8, 13, "g2")
    ink_edge(L, m, "k")


def coral_relief(L):
    """A coral branch carved on the wall, painted."""
    for (x0, y0, x1, y1) in ((8, 15, 8, 6), (8, 10, 4, 4), (8, 9, 12, 3), (6, 7, 6, 2), (10, 6, 11, 1)):
        L.line(x0, y0, x1, y1, "c2")
        L.line(x0 + 1, y0, x1 + 1, y1, "c3")
    L.hline(4, 12, 15, "d0")


# ---------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------

def coral_column():
    """A column of living coral standing out of the basin, 1 x 3."""
    s = Struct("coral_column", "A coral column in the basin", 1, 3, "props", walk=["X", "X", "X"])
    for cy in range(3):
        s.B.a[cy * 16:cy * 16 + 16] = water_cell(0, cy)
    M = s.M
    sh = mask(16, 48)
    for y in range(8, 46):
        w = 4 + (1 if (y // 5) % 2 else 0)
        m_rect(sh, 8 - w // 2 - 1, y, w + 1, 1)
    # branches at the crown
    for (x0, y0, x1, y1) in ((8, 10, 2, 2), (8, 9, 14, 1), (7, 12, 4, 0), (9, 12, 11, 0), (8, 14, 1, 8), (8, 14, 15, 7)):
        m = mask(16, 48)
        n = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(n + 1):
            x = round(x0 + (x1 - x0) * t / n)
            y = round(y0 + (y1 - y0) * t / n)
            m_rect(m, x - 1, y, 3 if t < n * 0.6 else 2, 2)
        sh |= m
    shade(M, sh, ["c0", "c1", "c2", "c3", "c4"], light=0.3)
    # polyp dots
    for y in range(6, 44, 3):
        x = 6 + (y * 7) % 5
        if sh[y, x]:
            M.px(x, y, "c4")
    ink_edge(M, sh, "k")
    # foam where it meets the water
    M.hline(3, 12, 46, "w5")
    M.hline(2, 4, 47, "w4")
    M.hline(11, 13, 47, "w4")
    return s


def trident():
    """The colossal bronze trident planted over the dais, 3 x 4."""
    s = Struct("trident", "Poseidon's trident", 3, 4, "props", walk=["XXX"] * 4,
               names={"head": (1, 0), "plinth": (1, 3)})
    for cy in range(3):
        for cx in range(3):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = wall_cell(cy, cx, shell_niche if cy == 1 and cx != 1 else None)
    for cx in range(3):
        s.B.a[48:64, cx * 16:cx * 16 + 16] = floor_cell(cx, 1, shade_px)
    M = s.M
    # the plinth: a rock with surf at its foot
    rock = m_poly(mask(48, 64), [(6, 63), (8, 52), (16, 47), (32, 47), (40, 52), (42, 63)])
    shade(M, rock, ["k", "m1", "m1", "m3"], light=0.3)
    M.hline(9, 39, 60, "w4")
    M.hline(7, 41, 62, "w3")
    ink_edge(M, rock, "k")
    # the shaft
    sh = m_rect(mask(48, 64), 22, 14, 4, 34)
    shade(M, sh, BRONZE, light=0.3)
    for y in (22, 34):
        M.hline(21, 26, y, "g2")
        M.hline(21, 26, y + 1, "b1")
    # the three prongs and the crossbar
    head = mask(48, 64)
    m_rect(head, 8, 14, 32, 4)
    for x in (8, 22, 36):
        m_rect(head, x, 3, 4, 12)
        m_poly(head, [(x - 2, 4), (x + 2, -1), (x + 6, 4)])
    m_poly(head, [(8, 18), (12, 14), (8, 14)])
    m_poly(head, [(40, 18), (36, 14), (40, 14)])
    shade(M, head, BRONZE, light=0.3)
    for x in (9, 23, 37):
        M.vline(x, 2, 12, "b3")
    ink_edge(M, head | sh, "k")
    return s


def trireme():
    """The trireme of Salamis, moored in the basin: 5 x 2, oars out, ram forward."""
    s = Struct("trireme", "The wooden wall: the trireme of Salamis", 5, 2, "props", walk=["XXXXX", "XXXXX"],
               names={"ram": (0, 1)})
    for cy in range(2):
        for cx in range(5):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = water_cell(cx, cy)
    M = s.M
    W, H = 80, 32
    # oars, under the hull
    for i, x in enumerate(range(16, 70, 5)):
        M.line(x, 14, x - 3, 28, "o2")
        M.px(x - 3, 28, "w5")
        M.px(x - 4, 29, "w4")
    hull = m_poly(mask(W, H), [(2, 22), (10, 14), (72, 12), (78, 6), (76, 15), (68, 22)])
    shade(M, hull, ["o0", "o1", "o2", "o3"], light=0.25)
    M.hline(10, 70, 14, "o3")
    M.hline(8, 68, 18, "o0")
    M.hline(12, 66, 19, "c1")
    # the bronze ram and the painted eye
    ram = m_poly(mask(W, H), [(0, 21), (6, 18), (12, 19), (10, 23), (4, 23)])
    shade(M, ram, ["b1", "g1", "g2"], light=0.3)
    M.rect(14, 15, 3, 2, "m5")
    M.px(15, 15, "k")
    # the deck rail and the stern ornament curling up
    M.hline(14, 70, 11, "o1")
    for x in range(16, 70, 6):
        M.vline(x, 9, 11, "o1")
    M.hline(14, 70, 9, "o2")
    ink_edge(M, hull | ram, "k")
    # wake
    M.hline(4, 74, 24, "w4")
    M.hline(6, 70, 25, "w5")
    for x in range(8, 72, 7):
        M.px(x, 26, "w4")
    return s


def dolphin():
    """A bronze dolphin leaping from the basin, verdigris on its back, 2 x 2."""
    s = Struct("dolphin", "A bronze dolphin leaping", 2, 2, "props", walk=["XX", "XX"])
    for cy in range(2):
        for cx in range(2):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = water_cell(cx, cy)
    M = s.M
    body = m_poly(mask(32, 32), [(4, 24), (6, 14), (12, 6), (20, 3), (27, 5), (24, 8), (18, 9), (13, 15),
                                 (11, 22), (13, 27), (8, 26)])
    shade(M, body, ["b0", "v1", "v2", "g1", "g2"], light=0.35)
    fin = m_poly(mask(32, 32), [(12, 8), (15, 3), (17, 7)])
    flat(M, fin, "v1")
    tail = m_poly(mask(32, 32), [(9, 26), (4, 30), (14, 31)])
    flat(M, tail, "v1")
    M.px(21, 6, "k")
    ink_edge(M, body | fin | tail, "k")
    M.hline(2, 18, 29, "w5")
    M.hline(1, 20, 30, "w4")
    return s


def anchor():
    """A stone anchor and a coil of rope by the dais, 1 x 1."""
    s = Struct("anchor", "A stone anchor", 1, 1, "props", walk=["X"])
    s.B.a[:] = floor_cell(0, 0)
    M = s.M
    st = m_poly(mask(16, 16), [(3, 14), (4, 3), (8, 1), (12, 3), (13, 14)])
    shade(M, st, ["m0", "m1", "m2", "m3"], light=0.3)
    M.rect(7, 4, 2, 2, "k")
    ink_edge(M, st, "k")
    return s


def amphora():
    s = Struct("amphora", "A wine-dark amphora", 1, 1, "props", walk=["X"])
    s.B.a[:] = floor_cell(1, 0)
    M = s.M
    b = m_ellipse(mask(16, 16), 3, 3, 12, 14)
    m_rect(b, 6, 0, 4, 4)
    shade(M, b, ["k", "d1", "d2", "t1", "t2"], light=0.3)
    M.hline(4, 11, 7, "m4")
    M.hline(5, 10, 10, "m4")
    ink_edge(M, b, "k")
    return s


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def one(key, title, arr_b, walk=".", mb=None, names=None):
    s = Struct(key, title, 1, 1, "kit", walk=[walk], names=names)
    s.B.a[:] = arr_b
    if mb:
        s.behaviors[(0, 0)] = mb
    return s


def kit():
    out = []
    for cy in range(2):
        for cx in range(2):
            out.append(one(f"floor_{cx}_{cy}", "Pale sea marble", floor_cell(cx, cy)))
            out.append(one(f"shade_{cx}_{cy}", "The marble in the wall's shade", floor_cell(cx, cy, shade_px)))
    for part in "lmr":
        out.append(one(f"cause_{part}", "The causeway's wave mosaic", causeway_cell(part)))
    void = Layer(16, 16)
    void.rect(0, 0, 16, 16, "k")
    out.append(one("void", "Outside the hall", void.a.copy(), walk="X"))
    t = Layer(16, 16)
    t.a[:] = causeway_cell("x")
    t.rect(0, 11, 16, 5, "d1")
    t.hline(0, 15, 11, "t2")
    t.vline(0, 0, 15, "k"), t.vline(15, 0, 15, "k")
    out.append(one("mat", "The south door's sill", t.a.copy(), walk="v"))
    sh = Layer(16, 16)
    sh.rect(0, 0, 16, 16, "k")
    sh.rect(1, 0, 14, 14, "d1")
    sh.vline(7, 0, 13, "k")
    sh.hline(1, 14, 0, "t2")
    for x in (4, 11):
        sh.rect(x, 5, 2, 2, "t2")
    out.append(one("mat_shut", "The south door, shut", sh.a.copy(), walk="X"))
    return out


def water():
    out = []
    for cy in range(2):
        for cx in range(2):
            out.append(one(f"water_{cx}_{cy}", "The basin", water_cell(cx, cy), walk="X"))
    for name, sides in (("n", "n"), ("s", "s"), ("w", "w"), ("e", "e"), ("nw", "nw"), ("ne", "ne"),
                        ("sw", "sw"), ("se", "se")):
        out.append(one(f"edge_{name}", "The basin's marble coping", edge_cell(sides), walk="X"))
    return out


def walls():
    out = []
    for row in range(3):
        for v in range(2):
            out.append(one(f"wall{row}_{v}", f"The north wall, row {row}", wall_cell(row, v), walk="X"))
    out.append(one("wall1_shell", "A scallop niche", wall_cell(1, 0, shell_niche), walk="X"))
    out.append(one("wall1_coral", "Coral painted on the wall", wall_cell(1, 1, coral_relief), walk="X"))
    for side in ("w", "e"):
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, wall_px(x + 8, y + 8))
        e = 12 if side == "w" else 0
        L.rect(e, 0, 4, 16, "d0")
        L.vline(15 if side == "w" else 0, 0, 15, "k")
        L.vline(12 if side == "w" else 3, 0, 15, "t1")
        out.append(one(f"side_{side}", f"The {side} wall", L.a.copy(), walk="X"))
    for state in ("shut", "open"):
        for row in (1, 2):
            L = Layer(16, 16)
            L.a[:] = wall_cell(row, 0)
            top = 3 if row == 1 else 0
            if state == "shut":
                L.rect(2, top, 12, 16 - top, "d3")
                L.rect(3, top, 4, 16 - top, "t2")
                L.vline(7, top, 15, "k")
                L.vline(8, top, 15, "d1")
                for y in range(top + 2, 16, 4):
                    L.hline(3, 6, y, "m4")
                    L.hline(9, 12, y, "t1")
                    L.px(6, y + 1, "m5")
                L.rect(4, 8 if row == 2 else 9, 2, 2, "g2")
                L.rect(10, 8 if row == 2 else 9, 2, 2, "g1")
            else:
                L.rect(2, top, 12, 16 - top, "k")
                if row == 2:
                    L.rect(3, 10, 10, 6, "d0")
            if row == 1:
                L.rect(1, 0, 14, 3, "g1")
                L.hline(1, 14, 0, "g2")
            L.rect(0, top, 2, 16 - top, "g2")
            L.vline(0, top, 15, "g1")
            L.rect(14, top, 2, 16 - top, "g1")
            L.vline(15, top, 15, "k")
            walk = "X" if (state == "shut" or row == 1) else "."
            out.append(one(f"door_{state}{row}", f"The sea gate, {state}", L.a.copy(), walk=walk))
    return out


def dais():
    out = []

    def surf(X, Y):
        c = flagstones(X, Y, ("d1", "d2", "d3", "t2"), "k", "pd", slab_w=16, slab_h=16, period=32)
        return c

    for part in "lmr":
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, surf(x, y))
        if part == "l":
            L.rect(0, 0, 3, 16, "t1"), L.vline(1, 0, 15, "t2")
        if part == "r":
            L.rect(13, 0, 3, 16, "t1"), L.vline(14, 0, 15, "t2")
        out.append(one(f"dais_{part}", "The admiral's dais", L.a.copy()))
        R = Layer(16, 16)
        R.rect(0, 0, 16, 16, "m2")
        R.hline(0, 15, 0, "m5")
        R.rect(0, 1, 16, 2, "m4")
        R.hline(0, 15, 3, "m1")
        wave_band(R, 5, fg="t2", dk="t1", bg="m2", phase=0)
        R.hline(0, 15, 14, "m1")
        R.hline(0, 15, 15, "k")
        out.append(one(f"riser_{part}", "The dais's riser", R.a.copy(), walk="X"))
    S = Layer(16, 16)
    for i in range(4):
        S.rect(0, i * 4, 16, 4, ["m5", "m4", "m3", "m3"][i])
        S.hline(0, 15, i * 4 + 3, "m1")
    out.append(one("steps", "The dais steps", S.a.copy()))
    return out


def props():
    return [trident(), trireme(), coral_column(), dolphin(), anchor(), amphora()]


SECTION_ROWS = {"kit": 0, "water": 3, "walls": 6, "dais": 10, "props": 12}


def sections():
    return [("kit", kit()), ("water", water()), ("walls", walls()), ("dais", dais()), ("props", props())]


SEAT = P.Seat("gTileset_SeatPoseidon", "seat_poseidon", C, GROUPS, sections, SECTION_ROWS)
