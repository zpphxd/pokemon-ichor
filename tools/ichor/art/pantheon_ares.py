"""gTileset_SeatAres: Brasidas's seat, the war hall of Ares (design/maps/Olympus_Pantheon.md).

A long hall on a bloodred floor: the bronze Ares on his plinth at its head,
two great braziers on the polemarch's dais, trophies of captured armor
(tropaia) standing down the aisle like a phalanx, tall tripod braziers
between them, racks of spears against the walls, shields hung on a smoke-dark
wall. Lakonian, so nothing painted: blood-red stone, dark stone, bronze.

Palette groups (one per secondary palette): floor (the red flags and the
oxblood runner with its bronze edge), wall (smoke-dark ashlar with hung
shields), bronze (statue, armor, spears), fire (braziers lit and cold).
"""
from __future__ import annotations


import pantheon_lib as P
from pantheon_lib import (Struct, ink_edge, m_ellipse, m_poly, m_rect, mask, shade, flat,
                          tiled, flagstones, Layer)

C = {
    "k": (24, 16, 16),
    # the floor: blood-red flags
    "r0": (64, 16, 16), "r1": (104, 24, 24), "r2": (144, 32, 32), "r3": (160, 48, 40),
    "r4": (184, 64, 48), "r5": (208, 104, 72),
    # the runner: oxblood
    "n1": (72, 16, 24), "n2": (96, 24, 32),
    # smoke-dark ashlar
    "s0": (32, 24, 32), "s1": (56, 40, 48), "s2": (80, 64, 72), "s3": (112, 96, 96), "s4": (152, 136, 128),
    # bronze, deep to bright
    "b0": (64, 40, 16), "b1": (112, 64, 24), "b2": (160, 96, 32), "b3": (200, 136, 48),
    "b4": (232, 184, 88), "b5": (248, 232, 160),
    # crest red, iron, spear-shaft wood
    "c1": (176, 24, 24), "c2": (232, 64, 40),
    "i1": (88, 96, 112), "i2": (152, 160, 176), "i3": (216, 224, 232),
    "w0": (72, 40, 24), "w1": (120, 72, 40), "w2": (168, 112, 64),
    # fire
    "f1": (224, 80, 24), "f2": (248, 152, 40), "f3": (248, 216, 96), "f4": (248, 248, 208),
}

GROUPS = {
    "floor": ["k", "r0", "r1", "r2", "r3", "r4", "r5", "n1", "n2", "b1", "b2", "b3", "b4"],
    "wall": ["k", "s0", "s1", "s2", "s3", "s4", "r1", "r2", "r4", "b1", "b2", "b3", "b4", "b5"],
    "bronze": ["k", "b0", "b1", "b2", "b3", "b4", "b5", "c1", "c2", "i1", "i2", "i3", "w0", "w1", "w2"],
    "fire": ["k", "f1", "f2", "f3", "f4", "b0", "b1", "b2", "b3", "b4", "s1", "s2", "r1", "r2"],
}

BRONZE = ["b0", "b1", "b2", "b3", "b4", "b5"]
IRON = ["i1", "i2", "i3"]
WOOD = ["w0", "w1", "w2"]
STONE = ["s0", "s1", "s2", "s3", "s4"]


# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------

def crack(seed):
    def f(X, Y):
        if P.h(seed, X // 16, Y // 16) % 3:
            return None
        x, y = X % 16, Y % 16
        cx = 4 + P.h(seed, 1, X // 16, Y // 16) % 8
        if abs((x - cx) - (y - 6) // 2) == 0 and 3 <= y <= 13:
            return "r1"
        if abs((x - cx - 1) - (y - 6) // 2) == 0 and 3 <= y <= 13:
            return "r0"
        return None
    return f


def speck(X, Y):
    # sparse 2 px wear: pits and glints, never single pixels
    k = P.h("sp", X // 2, Y // 2) % 37
    if k == 0 and Y % 2 == 0:
        return "r1"
    if k == 1:
        return "r3"
    return None


FLOOR_PERIOD = (64, 32)     # slabs 32 x 16 in running bond: lay floor_{x % 4}_{y % 2}


def floor_px(seed, marks=()):
    return lambda X, Y: flagstones(X, Y, ("r1", "r2", "r3", "r4"), "r1", "ares", slab_w=32, slab_h=16,
                                   period=64, period_y=32, marks=(speck,) + tuple(marks))


def crack_at(cx, cy):
    """A crack across one cell (always drawn)."""
    def f(X, Y):
        x, y = X % 16, Y % 16
        c = 5 + P.h("ck", cx, cy) % 6
        if 2 <= y <= 13 and x == c + (y - 2) // 3:
            return "r1"
        if 2 <= y <= 13 and x == c + (y - 2) // 3 + 1 and y % 3 == 0:
            return "r0"
        return None
    return f


def floor_cell(cx, cy, marks=()):
    return tiled(floor_px("ares", marks), ox=cx * 16, oy=cy * 16)


def shade_cell(cx, cy):
    """The floor under the north wall: the top half in the wall's shade."""
    base = floor_px("ares")

    def f(X, Y):
        c = base(X, Y)
        if Y % 16 < 6 or (Y % 16 < 9 and (X + Y) % 2 == 0 and Y % 16 == 8) :
            return {"r2": "r1", "r3": "r1", "r4": "r2", "r1": "r0", "r0": "k"}.get(c, c)
        if Y % 16 < 9:
            return {"r3": "r2", "r4": "r3"}.get(c, c)
        return c
    return tiled(f, ox=cx * 16, oy=cy * 16)


def glow_cell(cx, cy):
    """The flags lit by a brazier beside them: a step warmer and brighter."""
    base = floor_px("ares")
    up = {"r0": "r1", "r1": "r2", "r2": "r3", "r3": "r4", "r4": "r5"}
    return tiled(lambda X, Y: up.get(base(X, Y), base(X, Y)), ox=cx * 16, oy=cy * 16)


def runner_cell(part, motif=False):
    """The oxblood runner, three cells wide, bronze-edged; the middle cell can
    carry a bronze spear-point chevron."""
    L = Layer(16, 16)
    L.rect(0, 0, 16, 16, "n2")
    for y in range(16):
        for x in range(16):
            if (x + 2 * y) % 7 == 0 and P.h("rn", x, y) % 3 == 0:
                L.px(x, y, "n1")
    if part == "l":
        L.vline(0, 0, 15, "r1")
        L.vline(1, 0, 15, "b1")
        L.vline(2, 0, 15, "b3")
        L.vline(3, 0, 15, "b2")
        L.vline(4, 0, 15, "n1")
        for y in range(0, 16, 4):
            L.px(2, y, "b4")
    if part == "r":
        L.vline(15, 0, 15, "r1")
        L.vline(14, 0, 15, "b1")
        L.vline(13, 0, 15, "b2")
        L.vline(12, 0, 15, "b3")
        L.vline(11, 0, 15, "n1")
        for y in range(2, 16, 4):
            L.px(13, y, "b4")
    if motif:
        # a bronze spear-point, pointing up the hall
        pts = [(8, 2), (12, 9), (9, 8), (9, 13), (7, 13), (7, 8), (4, 9)]
        m = m_poly(mask(16, 16), pts)
        shade(L, m, ["b1", "b2", "b3", "b4"], light=0.35)
        ink_edge(L, m, "n1")
    return L.a.copy()


# ---------------------------------------------------------------------------
# Walls
# ---------------------------------------------------------------------------

def ashlar(X, Y, period=32):
    """Smoke-dark ashlar: big blocks, a bevel, soot toward the top."""
    return flagstones(X, Y, ("s0", "s1", "s2", "s3"), "k", "wall", slab_w=16, slab_h=8, period=period)


def wall_cell(row, cx, motif=None):
    """row 0: the cornice; 1: the face; 2: the base with its red band."""
    L = Layer(16, 16)
    X0 = cx * 16
    if row == 0:
        for y in range(16):
            for x in range(16):
                L.px(x, y, ashlar(X0 + x, y + 16))
        L.rect(0, 0, 16, 3, "s0")
        L.hline(0, 15, 3, "s1")
        L.hline(0, 15, 12, "k")
        L.rect(0, 13, 16, 3, "b1")
        L.hline(0, 15, 13, "b3")
        for x in range(0, 16, 4):
            L.px(X0 % 4 + x, 14, "b4")
            L.px(X0 % 4 + x + 1, 14, "b2")
        L.hline(0, 15, 15, "k")
    elif row == 1:
        for y in range(16):
            for x in range(16):
                L.px(x, y, ashlar(X0 + x, y + 32))
    else:
        for y in range(16):
            for x in range(16):
                L.px(x, y, ashlar(X0 + x, y + 48))
        L.rect(0, 8, 16, 5, "r1")
        L.hline(0, 15, 8, "r2")
        L.hline(0, 15, 9, "r4")
        L.hline(0, 15, 12, "s0")
        L.rect(0, 13, 16, 3, "s1")
        L.hline(0, 15, 13, "s3")
        L.hline(0, 15, 15, "k")
    if motif:
        motif(L)
    return L.a.copy()


def hung_shield(L, ox=0, oy=0):
    """A round hoplon hung on the wall, lit top-left, a bronze lambda boss."""
    m = m_ellipse(mask(16, 16), 2, 1, 13, 12)
    flat(L, m, "b1", ox, oy)
    inner = m_ellipse(mask(16, 16), 3, 2, 12, 11)
    shade(L, inner, ["b1", "b2", "b3", "b4"], light=0.3, ox=ox, oy=oy)
    rim = m_ellipse(mask(16, 16), 4, 3, 11, 10)
    shade(L, rim, ["b1", "b2", "b2", "b3"], light=0.4, ox=ox, oy=oy)
    # the lambda of Lakedaimon
    for i in range(4):
        L.px(ox + 7 - i // 2, oy + 4 + i, "b5" if i < 2 else "b4")
        L.px(ox + 8 + i // 2, oy + 4 + i, "b1")
    L.px(ox + 5, oy + 3, "b5")
    ink_edge(L, m, "k", ox=ox, oy=oy)
    L.hline(ox + 5, ox + 10, oy + 14, "s0")


def crossed_spears(L):
    for t in range(14):
        L.px(2 + t, 15 - t, "b2")
        L.px(13 - t, 15 - t, "b2")
        if t % 3 == 0:
            L.px(3 + t, 15 - t, "b1")
    for (x, y) in ((14, 1), (1, 1)):
        L.rect(x - 1, y, 2, 3, "b3")
        L.px(x - 1, y, "b5")
    L.px(8, 8, "b2")
    L.px(7, 8, "b4")


def banner(L, row):
    """The war banner on the wall face: oxblood cloth, a bronze spear-head."""
    if row == 1:
        L.hline(1, 14, 1, "b1")
        L.hline(1, 14, 2, "b3")
        L.rect(3, 3, 10, 13, "r1")
        L.rect(4, 3, 3, 13, "r2")
        L.vline(12, 3, 15, "s0")
        pts = [(8, 5), (11, 11), (9, 10), (9, 14), (7, 14), (7, 10), (5, 11)]
        m = m_poly(mask(16, 16), pts)
        shade(L, m, ["b1", "b2", "b3", "b4"], light=0.35)
    else:
        L.rect(3, 0, 10, 6, "r1")
        L.rect(4, 0, 3, 6, "r2")
        L.vline(12, 0, 5, "s0")
        for x in range(3, 13):
            if x % 3 != 2:
                L.px(x, 6, "r1")
                L.px(x, 7, "r2" if x % 3 == 0 else "r1")
        L.hline(3, 12, 8, "s0")


# ---------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------

def statue():
    """The bronze Ares on his plinth, 3 x 4: helmet crest, spear, hoplon."""
    s = Struct("statue", "The bronze Ares on his plinth", 3, 4, "props", walk=["XXX"] * 4,
               names={"head": (1, 0), "plinth": (1, 3)})
    W, H = 48, 64
    # the wall behind the top three rows; the floor shade under the plinth row
    for cy in range(3):
        for cx in range(3):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = wall_cell(cy, 7 + cx)
    for cx in range(3):
        s.B.a[48:64, cx * 16:cx * 16 + 16] = shade_cell(8 + cx, 3)
    M = s.M
    # plinth: two drums of iron-grey stone
    pl = m_rect(mask(W, H), 6, 50, 36, 13)
    shade(M, pl, IRON, light=0.25)
    M.hline(6, 41, 50, "i3")
    M.hline(6, 41, 55, "i1")
    M.hline(8, 39, 56, "i2")
    top = m_rect(mask(W, H), 9, 46, 30, 4)
    shade(M, top, ["i1", "i2", "i3"], light=0.25)
    ink_edge(M, pl | top, "k")
    # the god: legs, torso, arms, head
    body = mask(W, H)
    m_poly(body, [(17, 45), (20, 31), (23, 31), (22, 45)])          # left leg
    m_poly(body, [(26, 45), (25, 31), (28, 31), (31, 45)])          # right leg
    m_poly(body, [(17, 31), (16, 19), (19, 15), (29, 15), (32, 19), (31, 31)])  # cuirass
    m_poly(body, [(15, 18), (12, 27), (14, 28), (18, 21)])          # spear arm
    m_ellipse(body, 19, 4, 28, 14)                                   # helmeted head
    shade(M, body, BRONZE[1:], light=0.33, vert=0.25)
    # the kilt of leather strips (pteryges)
    for x in range(18, 31, 2):
        M.vline(x, 30, 33, "b1")
        M.vline(x + 1, 30, 33, "b3")
    M.hline(17, 31, 29, "b0")
    # cuirass muscles
    M.px(21, 20, "b4"), M.px(22, 20, "b4"), M.px(26, 20, "b2"), M.px(27, 20, "b2")
    M.vline(24, 19, 27, "b1")
    M.hline(20, 23, 24, "b4")
    # greaves
    M.vline(19, 38, 44, "b4")
    M.vline(27, 38, 44, "b3")
    # the Corinthian helmet's eye slits and cheek guards
    M.hline(21, 23, 9, "k")
    M.hline(25, 26, 9, "k")
    M.vline(24, 9, 13, "b1")
    # the crest: horsehair, red, front to back over the helmet
    crest = mask(W, H)
    m_poly(crest, [(17, 6), (19, 1), (24, 0), (30, 2), (33, 7), (30, 6), (25, 3), (21, 4)])
    shade(M, crest, ["c1", "c1", "c2"], light=0.3)
    ink_edge(M, crest, "k")
    # the shield on his left arm: a big hoplon, seen three-quarter
    sh = m_ellipse(mask(W, H), 27, 16, 43, 36)
    shade(M, sh, BRONZE[1:], light=0.3)
    rim = m_ellipse(mask(W, H), 29, 18, 41, 34)
    shade(M, rim, ["b1", "b2", "b3"], light=0.45)
    for i in range(5):
        M.px(35 - i // 2, 21 + i, "b5")
        M.px(36 + i // 2, 21 + i, "b1")
    ink_edge(M, body | sh, "k")
    ink_edge(M, crest, "k")
    # the spear: grounded beside him, point above the helmet
    for y in range(2, 46):
        M.px(12, y, "w1")
        M.px(13, y, "w0")
    M.px(12, 27, "b4"), M.px(13, 27, "b3")
    tip = m_poly(mask(W, H), [(12, 0), (15, 5), (13, 9), (11, 5)])
    shade(M, tip, IRON, light=0.3)
    M.px(12, 1, "i3")
    # hand on the spear
    M.rect(12, 26, 3, 3, "b3")
    M.px(12, 26, "b4")
    return s


def brazier_big(lit):
    """A great tripod brazier, 2 x 2, cold or burning."""
    s = Struct(f"brazier_{'lit' if lit else 'cold'}", "The polemarch's brazier", 2, 2, "props",
               walk=["XX", "XX"], names={"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)})
    for cy in range(2):
        for cx in range(2):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = floor_cell(cx, cy + 3)
    M = s.M
    # three legs, lion feet
    for (x0, x1) in ((8, 4), (16, 16), (24, 28)):
        for t in range(14):
            x = round(x0 + (x1 - x0) * t / 13)
            M.px(x, 17 + t, "b1")
            M.px(x + 1, 17 + t, "b3" if x0 < 16 else "b2")
        M.rect(x1 - 1, 30, 4, 2, "b1")
        M.px(x1 - 1, 30, "b3")
    # a ring tying the legs
    M.hline(7, 25, 23, "b2")
    M.hline(7, 25, 24, "b0")
    # the bowl
    bowl = m_ellipse(mask(32, 32), 2, 8, 29, 22)
    bowl[:12] = False
    m_rect(bowl, 2, 11, 28, 2)
    shade(M, bowl, ["b0", "b1", "b2", "b3", "b4"], light=0.3)
    M.hline(2, 29, 11, "b4")
    M.hline(3, 28, 12, "b2")
    for x in range(5, 28, 4):
        M.px(x, 16, "b4")
        M.px(x + 1, 17, "b1")
    ink_edge(M, bowl, "k")
    if lit:
        fl = mask(32, 32)
        m_poly(fl, [(4, 11), (7, 4), (9, 7), (12, 0), (15, 6), (18, 1), (21, 7), (24, 3), (28, 11)])
        for y in range(32):
            for x in range(32):
                if fl[y, x]:
                    d = y
                    c = "f4" if d > 8 and 10 < x < 22 else "f3" if d > 6 else "f2" if d > 3 else "f1"
                    if (x * 7 + y * 3) % 11 == 0 and d < 8:
                        c = "f1"
                    M.px(x, y, c)
        for (x, y) in ((6, 1), (20, 0), (26, 2), (14, 0)):
            M.px(x, y, "f2")
    else:
        # ash and charcoal in the cold bowl
        M.hline(5, 26, 10, "s1")
        M.hline(7, 24, 9, "s2")
        for x in range(8, 24, 3):
            M.px(x, 9, "s1")
            M.px(x + 1, 10, "b0")
    return s


def brazier_tall(lit):
    """A tall tripod brazier on the aisle, 1 x 2."""
    s = Struct(f"tripod_{'lit' if lit else 'cold'}", "A tripod brazier on the aisle", 1, 2, "props",
               walk=["X", "X"], names={"top": (0, 0), "base": (0, 1)})
    s.B.a[0:16] = floor_cell(6, 7)
    s.B.a[16:32] = floor_cell(6, 8)
    M = s.M
    for t in range(16):
        M.px(7, 14 + t, "b2")
        M.px(8, 14 + t, "b3" if t < 12 else "b1")
    for x0, x1 in ((7, 3), (8, 12)):
        for t in range(6):
            x = round(x0 + (x1 - x0) * t / 5)
            M.px(x, 25 + t, "b1")
    M.hline(2, 4, 31, "b1")
    M.hline(11, 13, 31, "b1")
    bowl = m_ellipse(mask(16, 32), 1, 6, 14, 16)
    bowl[:10] = False
    m_rect(bowl, 1, 9, 14, 2)
    shade(M, bowl, ["b0", "b1", "b2", "b3", "b4"], light=0.3)
    M.hline(1, 14, 9, "b4")
    ink_edge(M, bowl, "k")
    if lit:
        fl = m_poly(mask(16, 32), [(2, 9), (4, 3), (6, 5), (8, 0), (10, 5), (12, 2), (14, 9)])
        for y in range(32):
            for x in range(16):
                if fl[y, x]:
                    M.px(x, y, "f4" if y > 6 and 5 < x < 11 else "f3" if y > 5 else "f2" if y > 2 else "f1")
    else:
        M.hline(3, 12, 8, "s1")
        M.hline(4, 11, 7, "s2")
    return s


def tropaion():
    """A trophy: a captured cuirass, helmet and shield on a post, 1 x 2."""
    s = Struct("tropaion", "A tropaion of captured armor", 1, 2, "props", walk=["X", "X"],
               names={"top": (0, 0), "base": (0, 1)})
    s.B.a[0:16] = floor_cell(3, 9)
    s.B.a[16:32] = floor_cell(3, 10)
    M = s.M
    # the post and its crossbar
    m = m_rect(mask(16, 32), 7, 10, 2, 21)
    flat(M, m, "w1")
    M.vline(8, 10, 30, "w0")
    M.rect(5, 29, 6, 2, "w0")
    M.hline(5, 10, 29, "w1")
    # the cuirass on the crossbar
    cu = m_poly(mask(16, 32), [(3, 10), (5, 8), (11, 8), (13, 10), (12, 20), (4, 20)])
    shade(M, cu, BRONZE[1:], light=0.33)
    M.vline(8, 10, 19, "b1")
    M.px(6, 12, "b5"), M.px(10, 12, "b2")
    for x in range(4, 13, 2):
        M.vline(x, 20, 22, "w1")
        M.vline(x + 1, 20, 22, "w0")
    # the helmet on top, crest and all
    he = m_ellipse(mask(16, 32), 4, 1, 11, 8)
    shade(M, he, BRONZE[1:], light=0.33)
    M.hline(5, 7, 5, "k")
    M.hline(9, 10, 5, "k")
    M.vline(8, 5, 8, "b1")
    cr = m_poly(mask(16, 32), [(3, 3), (5, 0), (10, 0), (13, 3), (11, 2), (6, 1)])
    flat(M, cr, "c1")
    M.hline(6, 9, 0, "c2")
    # a spear leaned on it
    for t in range(26):
        M.px(13 - t // 9, 31 - t, "w2" if t % 4 else "w1")
    M.px(11, 4, "i3"), M.px(11, 3, "i2")
    ink_edge(M, cu | he | cr, "k")
    return s


def spear_rack():
    """A rack of spears and two shields leaned on it, 2 x 2, against a wall."""
    s = Struct("spear_rack", "A rack of spears", 2, 2, "props", walk=["XX", "XX"])
    for cy in range(2):
        for cx in range(2):
            s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = floor_cell(1 + cx, 9 + cy)
    M = s.M
    # the frame
    M.rect(2, 10, 28, 3, "w1")
    M.hline(2, 29, 10, "w2")
    M.rect(2, 24, 28, 3, "w1")
    M.hline(2, 29, 24, "w2")
    M.rect(2, 10, 2, 21, "w0")
    M.rect(28, 10, 2, 21, "w0")
    # the spears, points up, a hand's width apart
    for i, x in enumerate(range(6, 27, 4)):
        top = 1 + (i % 2)
        for y in range(top + 5, 30):
            M.px(x, y, "w1")
            M.px(x + 1, y, "w0")
        tip = m_poly(mask(32, 32), [(x, top), (x + 2, top + 3), (x + 1, top + 6), (x - 1, top + 3)])
        flat(M, tip, "i2")
        M.px(x, top + 1, "i3")
        M.px(x + 1, top + 4, "i1")
        M.hline(x, x + 1, top + 7, "b3")
    # two hoplons leaned against the foot
    for ox in (1, 15):
        sh = m_ellipse(mask(32, 32), ox, 18, ox + 15, 31)
        shade(M, sh, BRONZE[1:], light=0.3)
        rim = m_ellipse(mask(32, 32), ox + 2, 20, ox + 13, 29)
        shade(M, rim, ["b1", "b2", "b3"], light=0.45)
        ink_edge(M, sh, "k")
    M.px(8, 23, "b5"), M.px(9, 24, "b5"), M.px(22, 23, "b5"), M.px(23, 24, "b5")
    return s


def helmet_stand():
    """A crested helmet on a short stand, 1 x 1."""
    s = Struct("helmet_stand", "A crested helmet on its stand", 1, 1, "props", walk=["X"])
    s.B.a[:] = floor_cell(4, 11)
    M = s.M
    M.rect(7, 10, 2, 5, "w1")
    M.rect(5, 14, 6, 2, "w0")
    he = m_ellipse(mask(16, 16), 4, 3, 11, 11)
    shade(M, he, BRONZE[1:], light=0.33)
    M.hline(5, 7, 7, "k"), M.hline(9, 10, 7, "k")
    M.vline(8, 7, 10, "b1")
    cr = m_poly(mask(16, 16), [(3, 5), (5, 1), (11, 1), (13, 5), (11, 4), (5, 3)])
    shade(M, cr, ["c1", "c1", "c2"], light=0.3)
    ink_edge(M, he | cr, "k")
    return s


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def one(key, title, arr_b, walk=".", mb=None, arr_m=None, names=None):
    s = Struct(key, title, 1, 1, "kit", walk=[walk], names=names)
    s.B.a[:] = arr_b
    if arr_m is not None:
        s.M.a[:] = arr_m
    if mb:
        s.behaviors[(0, 0)] = mb
    return s


def kit():
    out = []
    for cy in range(2):
        for cx in range(4):
            out.append(one(f"floor_{cx}_{cy}", "The blood-red flags", floor_cell(cx, cy)))
    for cx, cy in ((1, 0), (2, 1), (3, 0)):
        out.append(one(f"crack_{cx}_{cy}", "A cracked flag", floor_cell(cx, cy, (crack_at(cx, cy),))))
    for cy in range(2):
        for cx in range(4):
            out.append(one(f"shade_{cx}_{cy}", "The flags in the north wall's shade", shade_cell(cx, cy)))
    out.append(one("runner_l", "The oxblood runner, west edge", runner_cell("l")))
    out.append(one("runner_m", "The oxblood runner", runner_cell("m")))
    out.append(one("runner_r", "The oxblood runner, east edge", runner_cell("r")))
    out.append(one("runner_point", "The runner's bronze spear-point", runner_cell("m", motif=True)))
    void = Layer(16, 16)
    void.rect(0, 0, 16, 16, "k")
    out.append(one("void", "Outside the hall", void.a.copy(), walk="X"))
    # the threshold: a bronze sill in the south door, MB_SOUTH_ARROW_WARP
    t = Layer(16, 16)
    t.rect(0, 0, 16, 16, "r0")
    t.rect(1, 0, 14, 12, "n2")
    t.rect(1, 12, 14, 4, "b1")
    t.hline(1, 14, 12, "b3")
    t.hline(1, 14, 13, "b2")
    t.vline(0, 0, 15, "k")
    t.vline(15, 0, 15, "k")
    out.append(one("mat", "The south door's bronze sill", t.a.copy(), walk="v"))
    shut = Layer(16, 16)
    shut.rect(0, 0, 16, 16, "k")
    shut.rect(1, 0, 14, 14, "b1")
    shut.vline(7, 0, 13, "k")
    shut.vline(8, 0, 13, "b0")
    for x in (3, 11):
        shut.rect(x, 5, 2, 2, "b3")
    shut.hline(1, 14, 0, "b2")
    out.append(one("mat_shut", "The south door, shut behind the challenger", shut.a.copy(), walk="X"))
    return out


def walls():
    out = []
    for row in range(3):
        for v in range(2):
            out.append(one(f"wall{row}_{v}", f"The north wall, row {row}", wall_cell(row, v), walk="X"))
    out.append(one("wall1_shield", "A hoplon hung on the wall", wall_cell(1, 0, hung_shield), walk="X"))
    out.append(one("wall1_spears", "Crossed spears on the wall", wall_cell(1, 1, crossed_spears), walk="X"))
    out.append(one("wall1_banner", "The war banner", wall_cell(1, 0, lambda L: banner(L, 1)), walk="X"))
    out.append(one("wall2_banner", "The war banner's tail", wall_cell(2, 0, lambda L: banner(L, 2)), walk="X"))
    # the side walls: a dark pier with a bronze edge facing the hall
    for side in ("w", "e"):
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, ashlar(x + (0 if side == "w" else 8), y + 64, period=16))
        edge = 12 if side == "w" else 3
        L.rect(edge if side == "w" else 0, 0, 4, 16, "s0")
        L.vline(edge if side == "w" else 3, 0, 15, "k")
        L.vline(edge - 1 if side == "w" else 4, 0, 15, "s3")
        out.append(one(f"side_{side}", f"The {side} wall", L.a.copy(), walk="X"))
    # the north door: bronze leaves, shut and open
    for state in ("shut", "open"):
        for row in (1, 2):
            L = Layer(16, 16)
            L.a[:] = wall_cell(row, 0)
            if state == "shut":
                L.rect(1, 0 if row == 2 else 3, 14, 16, "b1")
                if row == 1:
                    L.rect(1, 2, 14, 2, "b3")
                    L.hline(1, 14, 2, "b4")
                L.vline(7, 0, 15, "k")
                L.vline(8, 0, 15, "s0")
                for x in (3, 11):
                    for y in range(2 if row == 2 else 6, 16, 6):
                        L.rect(x, y, 2, 2, "b3")
                        L.px(x, y, "b5")
                L.vline(1, 0, 15, "b3")
                L.vline(14, 0, 15, "s0")
            else:
                L.rect(1, 0 if row == 2 else 3, 14, 16, "k")
                if row == 1:
                    L.rect(1, 2, 14, 2, "b3")
                    L.hline(1, 14, 2, "b4")
                L.vline(1, 0 if row == 2 else 4, 15, "b2")
                L.vline(14, 0 if row == 2 else 4, 15, "b1")
                if row == 2:
                    L.rect(2, 12, 12, 4, "s0")
                    L.hline(2, 13, 12, "s1")
            walk = "X" if (state == "shut" or row == 1) else "."
            mb = "MB_NON_ANIMATED_DOOR" if (state == "open" and row == 2) else None
            out.append(one(f"door_{state}{row}", f"The far door, {state}", L.a.copy(), walk=walk, mb=mb))
    return out


def dais():
    """The polemarch's dais: dark stone, bronze-edged, steps in the middle."""
    out = []

    def surface(X, Y):
        x, y = X % 16, Y % 16
        if x == 0 or y == 0:
            return "b1"
        if (x, y) in ((1, 1), (15, 1), (1, 15)):
            return "b3"
        if x == 1 or y == 1:
            return "s2"
        if x == 15 or y == 15:
            return "s0"
        if 6 <= x <= 9 and 6 <= y <= 9 and (x + y) % 2 == 0:
            return "b2"
        return "s1"

    for part in ("l", "m", "r"):
        L = Layer(16, 16)
        for y in range(16):
            for x in range(16):
                L.px(x, y, surface(x + (16 if part == "m" else 0), y))
        if part == "l":
            L.rect(0, 0, 3, 16, "b1")
            L.vline(1, 0, 15, "b3")
            L.vline(0, 0, 15, "k")
        if part == "r":
            L.rect(13, 0, 3, 16, "b1")
            L.vline(13, 0, 15, "b3")
            L.vline(15, 0, 15, "k")
        out.append(one(f"dais_{part}", "The dais", L.a.copy()))
        R = Layer(16, 16)
        R.rect(0, 0, 16, 16, "s1")
        R.rect(0, 0, 16, 3, "b2")
        R.hline(0, 15, 0, "b4")
        R.hline(0, 15, 3, "k")
        R.rect(0, 4, 16, 10, "s1")
        for x in range(0, 16, 8):
            R.vline(x + 3, 4, 13, "s0")
        R.hline(0, 15, 8, "s0")
        R.rect(0, 14, 16, 2, "k")
        if part == "l":
            R.vline(0, 0, 15, "k")
        if part == "r":
            R.vline(15, 0, 15, "k")
        out.append(one(f"riser_{part}", "The dais's riser", R.a.copy(), walk="X"))
    S = Layer(16, 16)
    for i in range(4):
        y = i * 4
        S.rect(0, y, 16, 4, ["s4", "s3", "s2", "s2"][i])
        S.hline(0, 15, y, ["s4", "s4", "s3", "s3"][i])
        S.hline(0, 15, y + 3, "s0")
    S.rect(5, 0, 6, 16, "r2")
    S.vline(5, 0, 15, "b3")
    S.vline(10, 0, 15, "b1")
    for i in range(4):
        S.hline(6, 9, i * 4 + 3, "r1")
    out.append(one("steps", "The dais steps", S.a.copy()))
    return out


def column():
    """A massive smoke-dark column, bronze-capped, 1 x 3."""
    s = Struct("column", "A column of the hall", 1, 3, "props", walk=["X", "X", "X"],
               names={"capital": (0, 0), "shaft": (0, 1), "base": (0, 2)})
    for cy in range(3):
        s.B.a[cy * 16:cy * 16 + 16] = floor_cell(3, cy)
    M = s.M
    sh = m_rect(mask(16, 48), 3, 6, 10, 36)
    shade(M, sh, ["s0", "s1", "s2", "s3", "s4"], light=0.3)
    for y in range(9, 41, 3):
        M.px(5, y, "s4")
        M.px(11, y + 1, "s0")
    cap = m_rect(mask(16, 48), 1, 1, 14, 5)
    shade(M, cap, ["s0", "b1", "b2", "b3", "b4"], light=0.3)
    M.hline(1, 14, 1, "b5")
    M.hline(2, 13, 5, "s0")
    bs = m_rect(mask(16, 48), 1, 42, 14, 5)
    shade(M, bs, ["s0", "b1", "b2", "b3", "b4"], light=0.3)
    M.hline(1, 14, 42, "b4")
    ink_edge(M, sh | cap | bs, "k")
    return s


def props():
    return [column(), statue(), brazier_big(False), brazier_big(True), brazier_tall(False), brazier_tall(True),
            tropaion(), spear_rack(), helmet_stand()]


SECTION_ROWS = {"kit": 0, "walls": 6, "dais": 10, "props": 12}


def sections():
    return [("kit", kit()), ("walls", walls()), ("dais", dais()), ("props", props())]


SEAT = P.Seat("gTileset_SeatAres", "seat_ares", C, GROUPS, sections, SECTION_ROWS)
