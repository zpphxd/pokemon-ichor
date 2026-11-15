"""Pomegranate line: Rhoaril, Korantha, Persenyx (Grass, branching).
Kore and Persephone, and the pomegranate seed that bound her below.

The two finals are one figure seen twice: the same round head, the same
crown at the brow, the same long locks falling from it and the same petal
gown. Korantha steps forward into the light and reaches; Persenyx stands
still in the dark and offers. Both carry the seed mark on the cheek."""
from mon_lib import C, Mat, Mon, bez, bez3, lens_pts

INK = C.ink


def _drop_body(cx, top, w, h, lean=0.0):
    """A plump teardrop, point up: point at (cx + lean, top), w wide and h
    tall, the shoulders full so it reads as a seed and not a cone."""
    r = w / 2
    tip = (cx + lean, top)
    mid = top + h * 0.58
    bot = top + h
    return (bez3(tip, (cx + lean + r * 0.42, top + h * 0.06), (cx + r, top + h * 0.3), (cx + r, mid))
            + bez3((cx + r, mid), (cx + r, bot - h * 0.12), (cx + r * 0.5, bot), (cx, bot))[1:]
            + bez3((cx, bot), (cx - r * 0.5, bot), (cx - r, bot - h * 0.12), (cx - r, mid))[1:]
            + bez3((cx - r, mid), (cx - r, top + h * 0.3), (cx + lean - r * 0.42, top + h * 0.06), tip)[1:-1])


# --------------------------------------------------------------------------
# Rhoaril, the seed
# --------------------------------------------------------------------------

RHOARIL_COLORS = [
    ("ink", INK),
    # the aril: deep pomegranate in the shadows, terracotta-red in the light
    ("red0", (96, 24, 40)), ("red1", (152, 32, 48)), ("red2", (208, 72, 56)), ("red3", (240, 128, 96)),
    # the pale kernel seen through the flesh, and the gloss
    ("kern", (248, 192, 168)), ("white", C.white),
    # olive sprout
    ("leaf0", (56, 72, 32)), ("leaf1", (96, 120, 48)), ("leaf2", (152, 168, 72)), ("leaf3", (192, 208, 136)),
    # cypress-dark calyx
    ("cyp0", (32, 64, 48)), ("cyp1", (72, 120, 80)),
    # root feet
    ("root", (112, 80, 48)),
]
RHOARIL_SHINY = {
    # a pale sun-gold, unripe fruit
    "red0": (152, 96, 32), "red1": (200, 144, 40), "red2": (232, 192, 72), "red3": (248, 224, 136),
    "kern": (248, 240, 200),
}

r_body = Mat(["red0", "red1", "red2", "red3"], line="red0", cuts=[0.17, 0.44, 0.72])
r_kern = Mat(["red3", "kern"], line="red2", cuts=[0.5])
r_leaf = Mat(["leaf0", "leaf1", "leaf2", "leaf3"], line="leaf0", cuts=[0.2, 0.46, 0.76])
r_cyp = Mat(["cyp0", "cyp1"], line="cyp0", cuts=[0.55])
r_root = Mat(["red0", "root"], line="red0", cuts=[0.5])


def _calyx(p, x, y, L=0, s=1.0):
    """The fruit's crown, a cypress-dark ring of six sepals: five points
    show, splayed outward like a little crown. (x, y) is the center of its
    base, which sits on the seed's tip."""
    def q(dx, dy, lift=0):
        return (x + dx * s, y + (dy - lift) * s)
    back = [q(-3.6, -1.6), q(-3.4, -6.4, L), q(-1.6, -3.0), q(0.4, -7.2, L), q(2.2, -3.0),
            q(4.4, -6.4, L), q(4.8, -1.4)]
    p.poly(back, r_cyp, bias=0.3, group=40)
    front = [q(-4.6, 1.4), q(-6.4, -2.6, L), q(-3.0, -1.0), q(-1.2, -3.2), q(0.6, -1.2), q(3.0, -3.0),
             q(4.2, -0.8), q(7.6, -2.2, L), q(5.6, 1.6), q(2.6, 2.8), q(-1.6, 2.8)]
    p.poly(front, r_cyp, group=41)


def rhoaril(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = phase if view == "side" else 0
        # root feet: little nubs with a root tip, the far one in shade
        p.limb([(37, 55), (38, 58.5), (39.5 + step, 60)], 3.8, 2.4, r_root, bias=0.25, group=20)
        p.limb([(28, 55), (27, 58.5), (25.5 - step, 60)], 4.0, 2.6, r_root, group=21)
        # the sprout: a stem from the crown and one curled leaf leaning to the light
        p.limb(bez((33, 33 - L), (32.5, 30 - L), (30.5, 28.5 - 2 * L)), 2.0, 1.6, r_leaf, group=30)
        p.lens((31, 29 - 2 * L), (20.5, 26.5 - 3 * L), 6.4, r_leaf, bend=1.8, fat=0.42, group=31)
        # the body
        body = p.poly(_drop_body(33, 36 - L, 23, 22.5 + L, lean=0.5), r_body, group=1)
        # the kernel glowing through, low in the belly like a heart
        if p.big:
            p.blob(38, 51.5, 2.2, 3.0, r_kern, ang=-20, clip=[body], group=2, noline=True, bias=0.05)
        _calyx(p, 33.5, 36 - L, L)
        if p.big:
            # the near eye catches the light; the far one sits half in shadow
            p.eye(25, 44 - L, 4, 6, shine="white", shine_at=(1, 1))
            p.px(27, 48 - L, "red3")
            p.eye(32, 45 - L, 3, 5, shine=None)
            p.pxs([(32, 45 - L), (33, 45 - L), (34, 45 - L)], "red0")
            p.px(33, 48 - L, "red2")
            p.stroke([(30, 52 - L), (31, 52 - L)], "red0")
            # gloss along the upper-left of the skin
            p.pxs([(26, 41 - L), (27, 40 - L), (28, 39 - L)], "white")
        else:
            p.px(27, 46 - L, "ink")
            p.px(33, 46 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the seed's back, crown and sprout,
        # the face turned right so the near eye still shows
        p.limb(bez((36, 18), (35, 13), (32, 10)), 2.2, 1.6, r_leaf, group=30)
        p.lens((32.5, 10.5), (21, 6), 6.4, r_leaf, bend=1.6, fat=0.45, group=31)
        body = p.poly(_drop_body(32, 19, 36, 54, lean=3), r_body, group=1)
        p.blob(22, 48, 5, 7, r_kern, ang=10, clip=[body], group=2, noline=True, bias=0.1)
        _calyx(p, 35, 19, s=1.25)
        if p.big:
            p.eye(44, 33, 4, 6, shine="white", shine_at=(2, 1))
            p.px(45, 37, "red3")
            p.pxs([(18, 30), (19, 28), (20, 27)], "white")
        return

    if view == "down":
        step = phase
        p.limb([(28.5, 55), (28, 60 - step)], 3.6, 2.8, r_root, group=20)
        p.limb([(35.5, 55), (36, 60 - (1 - step))], 3.6, 2.8, r_root, group=21)
        p.limb(bez((32, 35), (32, 31), (34, 29)), 1.8, 1.4, r_leaf, group=30)
        p.lens((33.5, 29.5), (42, 26), 5, r_leaf, bend=-1.2, group=31)
        p.poly(_drop_body(32, 36.5, 21, 22), r_body, group=1)
        _calyx(p, 32, 36)
        p.eye(26, 44, 4, 6, shine="white", shine_at=(2, 1))
        p.eye(34, 44, 4, 6, shine="white", shine_at=(2, 1))
        p.stroke([(31, 51), (32, 51)], "red0")
        return

    if view == "up":
        step = phase
        p.limb([(28.5, 55), (28, 60 - step)], 3.6, 2.8, r_root, group=20)
        p.limb([(35.5, 55), (36, 60 - (1 - step))], 3.6, 2.8, r_root, group=21)
        p.poly(_drop_body(32, 36.5, 21, 22), r_body, group=1)
        p.limb(bez((32, 35), (32, 31), (30, 29)), 1.8, 1.4, r_leaf, group=30)
        p.lens((30.5, 29.5), (22, 26), 5, r_leaf, bend=1.2, group=31)
        _calyx(p, 32, 36)
        return


# --------------------------------------------------------------------------
# Korantha, Kore of spring
# --------------------------------------------------------------------------

KORANTHA_COLORS = [
    ("ink", INK),
    # olive and silver-leaf greens: hair, bodice, stems, root feet
    ("lf0", (40, 64, 32)), ("lf1", (80, 112, 48)), ("lf2", (136, 168, 72)), ("silver", (192, 208, 152)),
    # marble petals, faintly rosy in the shade
    ("pt0", (176, 152, 168)), ("pt1", (224, 216, 216)), ("pt2", (248, 248, 240)),
    # fairy pink
    ("pk0", (216, 112, 144)), ("pk1", (248, 184, 200)),
    # the pomegranate blossom at the brow
    ("rd0", (144, 32, 48)), ("rd1", (224, 72, 64)),
    # narcissus corona and flower hearts
    ("gold", (240, 200, 72)),
    # skin
    ("sk0", (208, 176, 168)), ("sk1", (248, 232, 224)),
]
KORANTHA_SHINY = {
    # sun-gold petals, a white crown blossom
    "pt0": (200, 144, 40), "pt1": (240, 200, 88), "pt2": (248, 232, 160),
    "rd0": (184, 176, 184), "rd1": (248, 248, 240),
}

k_skin = Mat(["sk0", "sk1"], line="sk0", cuts=[0.5])
k_leaf = Mat(["lf0", "lf1", "lf2", "silver"], line="lf0", cuts=[0.2, 0.46, 0.76])
k_petal = Mat(["pt0", "pt1", "pt2"], line="pt0", cuts=[0.3, 0.62])
k_pink = Mat(["pk0", "pk1"], line="pk0", cuts=[0.5])
k_red = Mat(["rd0", "rd1"], line="rd0", cuts=[0.5])
k_gold = Mat(["gold"])
k_stem = Mat(["lf0", "lf1"], line="lf0", cuts=[0.5])
# the icon's shared palettes have no dark olive, so the icon's hair is drawn
# in the lighter greens to stay green
k_leaf_icon = Mat(["lf2", "lf2", "silver"], line="lf1", cuts=[0.3, 0.7])


def _star(p, x, y, r, mat, n=6, rot=0.0, inner=0.45, **kw):
    """A flower seen face-on: n pointed petals around (x, y)."""
    import math
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180.0 / n)
        rr = r if i % 2 == 0 else r * inner
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    return p.poly(pts, mat, **kw)


# Hand-drawn pieces for Korantha, placed at battle size. o ink, w/m/s the
# petal ramp light to dark, g gold, c/b pomegranate red light/dark, a pink.
K_LEG = {"o": "ink", "w": "pt2", "m": "pt1", "s": "pt0", "g": "gold", "c": "rd1", "b": "rd0",
         "a": "pk1", "p": "pk0", "l": "lf0", "L": "lf1", "G": "lf2", "S": "silver", "e": "sk0", "f": "sk1"}
K_FLOWER = [".o.o.", "owmwo", "omgmo", "owsmo", ".ooo."]
K_BUD = [".oo.", "oapo", "oppo", ".oo."]
K_BLOSSOM = ["...oo.oo...",
             "..oacocco..",
             ".occbcccbo.",
             "oaccgcgccbo",
             "occggggccbo",
             "occcggccbbo",
             ".obccccbbo.",
             "..obbbbbo..",
             "...ooooo..."]
K_NARCISSUS = ["....oo.....",
               ".oo.owo.oo.",
               "owwoowmowmo",
               ".owwwmwwmo.",
               "..owgggmo..",
               ".owwgcgwmo.",
               "owwmgggmmso",
               "owmo.oms.so",
               ".oo..oso.o.",
               ".....oo...."]


def _lock(p, a, b, w, bend=0.0, mat=None, **kw):
    """A long leaf-lock of hair from a (root) to b (tip), with a midrib and
    a silver sheen along its lit edge."""
    pid = p.lens(a, b, w, mat or k_leaf, bend=bend, fat=0.4, **kw)
    if p.big:
        pts = lens_pts(a, b, w, bend, fat=0.4)
        n = len(pts) // 2
        mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(pts[:n], pts[n:][::-1])]
        p.stroke(mid[3:int(n * 0.8)], "lf0")
        edge = pts[n:][::-1] if bend < 0 else pts[:n]
        for i in (int(n * 0.3), int(n * 0.42)):
            ex, ey = edge[i]
            mx, my = mid[i]
            p.px(ex + (mx - ex) * 0.4 - 0.5, ey + (my - ey) * 0.4 - 0.5, "silver")
    return pid


def _petal(p, a, b, w, bend=0.0, tip=0.3, fat=0.6, **kw):
    """A gown petal from a (waist) to b (hem point), its tip blushing pink."""
    pid = p.lens(a, b, w, k_petal, bend=bend, fat=fat, **kw)
    if p.big and tip:
        kw.pop("bias", None)
        g = kw.pop("group", None)
        tx, ty = a[0] + (b[0] - a[0]) * (1 - tip), a[1] + (b[1] - a[1]) * (1 - tip)
        p.lens((tx, ty), b, w * 0.55, k_pink, bend=bend * 0.3, clip=[pid], group=g, noline=True, **kw)
    return pid


def korantha(p, view, phase):
    if view in ("front", "side", "icon"):
        # frame 2: the flower nods toward her hand as she reaches for it, and
        # her hair stirs
        L = 1 if (phase == 1 and view == "front") else 0
        sw = phase if view == "front" else 0
        hair = k_leaf_icon if view == "icon" else k_leaf

        # the narcissus she reaches for, growing at her feet
        if p.big:
            p.lens((12, 60.5), (7, 47), 3.0, k_leaf, bend=0.8, bias=0.15, group=61)
            p.limb(bez((12.5, 60), (14.5, 42), (11 + L, 27 + L)), 3.0, 2.4, k_stem, group=60)
            p.lens((13, 60.5), (17.5, 50), 2.8, k_leaf, bend=-0.6, group=62)
            _star(p, 10 + L, 24 + L, 5.4, k_petal, rot=-12 + 10 * sw, inner=0.55, group=63)
            p.circle(10 + L, 24 + L, 2.0, k_gold, group=64)

        # long leafy hair falling behind, back layer first
        _lock(p, (40, 9), (56 - sw, 27 + 2 * sw), 7.4, bend=-2.2, bias=0.3, group=50, mat=hair)
        _lock(p, (39, 13), (52 - sw, 41 + sw), 8.2, bend=-2.0, bias=0.2, group=51, mat=hair)
        _lock(p, (36, 19), (44 - sw, 45), 6.8, bend=-0.8, bias=0.1, group=52, mat=hair)

        # far arm, back and down, hand at the hip
        p.limb(bez((36, 28), (40, 31), (41.5, 36)), 3.0, 2.4, k_skin, bias=0.35, group=20)

        # the peplos: long petals falling to the ground and trailing back
        # as she steps, a short tier of pink-tipped petals over the hips
        _petal(p, (37, 38), (57, 58), 11, bend=-2.4, bias=0.3, group=30, fat=0.66)
        _petal(p, (36, 39), (50, 60.5), 11, bend=-1.4, bias=0.22, group=31, fat=0.66)
        _petal(p, (32, 39), (20.5, 60), 10, bend=1.8, bias=0.1, group=32, fat=0.7)
        _petal(p, (34.5, 39), (42, 61), 10, bend=-0.6, bias=0.06, group=33, fat=0.7)
        _petal(p, (33, 39), (30.5, 61), 9.5, bend=0.4, bias=-0.04, group=34, fat=0.7)
        p.lens((36, 37), (46, 46), 7, k_pink, bend=-1.0, fat=0.6, bias=0.1, group=35)
        p.lens((32.5, 37), (25.5, 47), 7, k_pink, bend=1.0, fat=0.6, group=36)
        p.lens((34, 37.5), (36.5, 48.5), 7, k_pink, bend=-0.2, fat=0.6, bias=-0.1, group=37)

        # bare root foot stepping forward
        p.limb([(26.5, 57), (24.5, 60), (21, 60.5)], 3.4, 2.4, k_stem, group=40)

        # torso: a bodice of petals, slim waist, a pink sash
        p.limb([(31.5, 27), (33, 33), (33.5, 38.5)], 9, 5.6, k_petal, group=10)
        p.lens((28, 37.5), (38, 37), 3.4, k_pink, bend=0.4, group=13)
        p.lens((26.5, 26.5), (36, 25), 5.0, k_leaf, bend=-1.2, group=11)
        p.limb([(30.5, 22), (31, 25.5)], 3.2, 3.6, k_skin, group=12)

        # the head: hair mass, then the face
        p.blob(33, 13.5, 10.2, 9.6, hair, group=4)
        p.blob(27.5, 16.5, 7.4, 7.2, k_skin, group=3)
        # bangs: leaves sweeping over the brow and down the cheek
        p.lens((39, 8), (23, 11), 6.4, hair, bend=1.8, group=5)
        p.lens((36, 12), (31, 16), 4.0, k_leaf, bend=0.8, group=6)
        p.lens((37.5, 14), (35, 25), 4.8, hair, bend=-0.8, group=7)

        # crown of spring flowers around a pomegranate blossom
        if not p.big:
            p.blob(22.5, 7, 4.5, 3.6, k_red, group=72)
            for x, y in ((30, 4.5), (36, 3.8), (41.5, 7)):
                p.circle(x, y, 2.4, k_petal, group=70)

        # near arm reaching for the flower
        p.limb(bez((29, 27), (24, 30), (19.5, 28)), 3.4, 2.8, k_skin, group=21)
        p.limb(bez((19.5, 28), (17.5, 27), (15.5 - L, 25.5 - L)), 2.8, 2.2, k_skin, group=21)

        if p.big:
            for x, y in ((30, 2), (39, 3)):
                p.patch(x, y, K_FLOWER, K_LEG)
            for x, y in ((35, 1), (43, 6)):
                p.patch(x, y, K_BUD, K_LEG)
            p.patch(18, 4, K_BLOSSOM, K_LEG)
            p.patch(5 + L, 18 + L, K_NARCISSUS, K_LEG)
            p.eye(22, 14, 4, 7, iris="pk0", shine="sk1", shine_at=(1, 1))
            p.eye(28, 14, 3, 7, iris="pk0", shine="sk1", shine_at=(1, 1))
            p.pxs([(22, 22), (23, 22)], "pk0")
            p.px(28, 22, "pk0")
        else:
            p.px(23, 16, "ink")
            p.px(29, 16, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x, the head turned right in profile,
        # the leafy hair falling down her back, the crown on top
        # the gown: one drape of white petals from the shoulders, a pink tier
        # of petals over the hips
        p.limb(bez((46, 40), (51, 44), (52, 52)), 5.4, 4.4, k_skin, bias=0.1, group=20)
        p.poly(bez3((27, 44), (22, 52), (16, 60), (12, 64)) + [(60, 64)]
               + bez3((58, 64), (54, 58), (50, 50), (48, 42)), k_petal, group=10)
        p.blob(37, 42, 12, 5, k_petal, group=10)
        for a, b, bend in (((31, 49), (22, 66), 1.0), ((38, 49), (42, 66), -0.4), ((44, 48), (56, 64), -1.0)):
            _petal(p, a, b, 8, bend=bend, tip=0, bias=0.05, group=36)
        for a, b, bend, bias in (((33, 50), (16, 58), 1.4, 0.05), ((36, 51), (30, 62), 0.4, -0.05),
                                 ((39, 51), (46, 61), -0.4, 0.05), ((42, 49), (55, 56), -1.2, 0.15)):
            p.lens(a, b, 8, k_pink, bend=bend, fat=0.55, bias=bias, group=31)
        p.lens((29, 50), (46, 49.5), 3.6, k_pink, bend=0.6, group=13)
        p.limb([(40, 37), (42, 28)], 6, 5.4, k_skin, group=12)
        p.lens((27, 40), (51, 39), 6.4, k_leaf, bend=-1.4, group=11)
        # hair: the back of the head, then locks swept over the near shoulder
        p.blob(38, 19, 11.5, 11, k_leaf, group=4)
        p.blob(46.5, 22, 6, 7, k_skin, group=3)
        _lock(p, (31, 12), (11, 30), 7.6, bend=1.6, bias=0.15, group=50)
        _lock(p, (32, 18), (12, 45), 8.6, bend=1.6, bias=0.08, group=51)
        _lock(p, (36, 23), (22, 54), 9.0, bend=1.2, group=52)
        _lock(p, (40, 26), (35, 50), 6.4, bend=0.4, bias=-0.05, group=54)
        _lock(p, (44, 14), (50, 26), 5.0, bend=-0.8, group=53)
        if p.big:
            for x, y in ((27, 4), (37, 2)):
                p.patch(x, y, K_FLOWER, K_LEG)
            for x, y in ((33, 2), (23, 8)):
                p.patch(x, y, K_BUD, K_LEG)
            p.patch(42, 4, K_BLOSSOM, K_LEG)
            p.eye(48, 17, 3, 7, iris="pk0", shine="sk1", shine_at=(1, 1))
            p.px(48, 25, "pk0")
        return

    if view == "down":
        step = phase
        p.limb([(29.5, 52), (29, 61 - 2 * step)], 3, 2.4, k_stem, group=40)
        p.limb([(34.5, 52), (35, 61 - 2 * (1 - step))], 3, 2.4, k_stem, group=41)
        p.lens((24, 30), (18, 50 + step), 7, k_leaf, bend=-0.6, group=50)
        p.lens((40, 30), (46, 50 + 1 - step), 7, k_leaf, bend=0.6, group=51)
        for a, b in (((31, 38), (21, 55)), ((33, 38), (43, 55)), ((32, 38), (32, 57))):
            _petal(p, a, b, 10, fat=0.66, group=30)
        for a, b in (((31, 37), (24, 47)), ((33, 37), (40, 47)), ((32, 37), (32, 48))):
            p.lens(a, b, 7, k_pink, fat=0.6, group=35)
        p.limb([(32, 27), (32, 38)], 8, 6, k_petal, group=10)
        p.limb([(27, 29), (23, 40)], 2.8, 2.4, k_skin, group=20)
        p.limb([(37, 29), (41, 40)], 2.8, 2.4, k_skin, group=21)
        p.blob(32, 16, 9.6, 9, k_leaf, group=4)
        p.blob(32, 19, 6.8, 6.6, k_skin, group=3)
        p.lens((40, 9), (27, 12), 5.6, k_leaf, bend=1.4, group=5)
        p.blob(25, 9, 3.6, 3.2, k_red, group=72)
        for x in (30, 36, 41):
            p.circle(x, 7, 2.2, k_petal, group=70)
        p.eye(27, 17, 3, 5, iris="pk0", shine="sk1", shine_at=(1, 1))
        p.eye(34, 17, 3, 5, iris="pk0", shine="sk1", shine_at=(1, 1))
        return

    if view == "up":
        step = phase
        p.limb([(29.5, 52), (29, 61 - 2 * step)], 3, 2.4, k_stem, group=40)
        p.limb([(34.5, 52), (35, 61 - 2 * (1 - step))], 3, 2.4, k_stem, group=41)
        for a, b in (((31, 38), (21, 55)), ((33, 38), (43, 55)), ((32, 38), (32, 57))):
            _petal(p, a, b, 10, fat=0.66, group=30)
        for a, b in (((31, 37), (24, 47)), ((33, 37), (40, 47)), ((32, 37), (32, 48))):
            p.lens(a, b, 7, k_pink, fat=0.6, group=35)
        p.limb([(32, 27), (32, 38)], 8, 6, k_petal, group=10)
        p.limb([(27, 29), (23, 40)], 2.8, 2.4, k_skin, group=20)
        p.limb([(37, 29), (41, 40)], 2.8, 2.4, k_skin, group=21)
        p.blob(32, 16, 9.6, 9, k_leaf, group=4)
        for a, b, bend in (((28, 18), (22, 42 + step), -0.6), ((36, 18), (42, 42 + 1 - step), 0.6),
                           ((32, 20), (32, 44), 0.0)):
            _lock(p, a, b, 7, bend=bend)
        p.blob(25, 9, 3.6, 3.2, k_red, group=72)
        for x in (30, 36, 41):
            p.circle(x, 7, 2.2, k_petal, group=70)
        return

# --------------------------------------------------------------------------
# Persenyx, the queen below
# --------------------------------------------------------------------------

PERSENYX_COLORS = [
    ("ink", INK),
    # the cypress-dark veil
    ("cy0", (32, 56, 48)), ("cy1", (56, 88, 72)), ("cy2", (96, 128, 104)),
    # marble-pale skin, cool in the shade
    ("sk0", (168, 160, 184)), ("sk1", (216, 208, 224)), ("sk2", (248, 248, 240)),
    # the ash-gray robe and withered stems
    ("as0", (80, 80, 96)), ("as1", (128, 128, 144)), ("as2", (176, 176, 192)),
    # the split pomegranate: rind and glowing seeds
    ("rd0", (112, 16, 40)), ("rd1", (200, 40, 64)), ("glow", (248, 152, 136)),
    # ghostly violet
    ("vi0", (104, 72, 152)), ("vi1", (176, 144, 224)),
]
PERSENYX_SHINY = {
    # an Aegean-blue veil; the seeds glow sun-gold
    "cy0": (24, 48, 104), "cy1": (40, 88, 160), "cy2": (96, 144, 208),
    "rd1": (208, 152, 40), "glow": (248, 232, 136),
}

n_veil = Mat(["cy0", "cy1", "cy2"], line="cy0", cuts=[0.3, 0.64])
n_skin = Mat(["sk0", "sk1", "sk2"], line="sk0", cuts=[0.34, 0.7])
n_robe = Mat(["as0", "as1", "as2"], line="as0", cuts=[0.3, 0.64])
n_stem = Mat(["as0", "as1", "as2"], line="as0", cuts=[0.35, 0.7])
n_dry = Mat(["rd0", "as1"], line="rd0", cuts=[0.55])
n_rind = Mat(["rd0", "rd1"], line="rd0", cuts=[0.6])
n_wisp = Mat(["vi0", "vi1"], line="vi0", cuts=[0.5])


def _vlock(p, a, b, w, bend=0.0, **kw):
    """A long dark leaf of the veil, with a midrib and a pale sheen."""
    pid = p.lens(a, b, w, n_veil, bend=bend, fat=0.4, **kw)
    if p.big:
        pts = lens_pts(a, b, w, bend, fat=0.4)
        n = len(pts) // 2
        mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(pts[:n], pts[n:][::-1])]
        p.stroke(mid[3:int(n * 0.8)], "cy0")
    return pid


def _robe(p, a, b, w, bend=0.0, fat=0.62, tip=0.32, **kw):
    """A long faded petal of the robe, its end fraying into a violet wisp."""
    pid = p.lens(a, b, w, n_robe, bend=bend, fat=fat, **kw)
    if p.big and tip:
        kw.pop("bias", None)
        g = kw.pop("group", None)
        tx, ty = a[0] + (b[0] - a[0]) * (1 - tip), a[1] + (b[1] - a[1]) * (1 - tip)
        p.lens((tx, ty), b, w * 0.6, n_wisp, bend=bend * 0.4, clip=[pid], group=g, noline=True, **kw)
    return pid


# Hand-drawn pieces for Persenyx. o ink, b/c rind dark/light, g seed glow,
# v/V violet dark/light, s/S ash, w marble.
N_LEG = {"o": "ink", "b": "rd0", "c": "rd1", "g": "glow", "v": "vi0", "V": "vi1", "s": "as0", "S": "as1",
         "w": "sk2", "k": "cy0"}
N_FRUIT = ["....oo.....",
           "...osso....",
           "..obbbboo..",
           ".obcccbcbo.",
           "obcgcgoocbo",
           "obgcgo..obo",
           "obcgcgoocbo",
           "obbcgcgcbbo",
           ".obbcccbbo.",
           "..oobbboo..",
           "....ooo...."]
N_BUD = ["..o.o..", ".obsbo.", "obbcbbo", ".obbbo.", "..ooo.."]


def persenyx(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        sw = phase if view == "front" else 0

        # crown of withered stems: Korantha's flowers, dried and drooping on
        # crooked stalks
        for (bx, by), (tx, ty), (hx, hy) in (((29, 8), (28.5, 2), (25.5, 4)), ((34, 6), (35.5, 1.5), (39, 3.5)),
                                             ((40, 7), (43, 2.5), (46, 4.5)), ((44, 10), (48.5, 8.5), (50, 11.5))):
            p.limb(bez((bx, by), (tx - 0.5, ty - 1), (hx, hy)), 2.4, 1.8, n_stem, group=70, bias=-0.2)
            p.drop((hx + 0.3, hy + 3.6), hx, hy + 0.8, 1.9, n_dry, group=71)

        # the veil falling behind, long, back layer first
        _vlock(p, (40, 9), (57, 40 + sw), 8.4, bend=-2.4, bias=0.3, group=50)
        _vlock(p, (39, 13), (53, 55 + sw), 9.0, bend=-1.8, bias=0.22, group=51)
        _vlock(p, (37, 18), (46, 58 + sw), 8.0, bend=-0.6, bias=0.14, group=52)

        # the robe: long faded petals hanging still, their ends fraying into
        # violet wisps that curl away to nothing
        _robe(p, (36.5, 37), (50 - sw, 56), 9, bend=-2.0, bias=0.28, group=30, fat=0.62)
        _robe(p, (32.5, 37), (23 + sw, 57), 9, bend=2.0, bias=0.12, group=31, fat=0.62)
        _robe(p, (35, 37), (43 - sw, 59), 9, bend=-1.2, bias=0.05, group=32, fat=0.62)
        _robe(p, (33.5, 37), (31 + sw, 60), 9, bend=1.0, bias=-0.06, group=33, fat=0.62)
        # torso and a high collar of dark leaves
        p.limb([(31.5, 27), (33, 32.5), (33.5, 38)], 9, 6, n_robe, group=10)
        p.lens((26, 26.5), (37, 25), 5.4, n_veil, bend=-1.4, group=11)
        p.limb([(30.5, 22), (31, 25.5)], 3.2, 3.6, n_skin, group=12)

        # head: the veil's crown, then the face
        p.blob(33, 13.5, 10.2, 9.6, n_veil, group=4)
        p.blob(27.5, 16.5, 7.4, 7.2, n_skin, group=3)
        p.lens((39, 8), (23, 11), 6.4, n_veil, bend=1.8, group=5)
        p.lens((37.5, 14), (35, 25), 4.8, n_veil, bend=-0.8, group=7)
        # the near side of the veil, falling past the shoulder
        _vlock(p, (22, 11), (19, 30), 6.0, bend=0.8, group=8)

        # near arm, held out, the hand cupped under the fruit
        p.limb(bez((29, 27), (26, 34), (21.5, 36)), 3.4, 2.8, n_skin, group=21)
        p.blob(19.5, 36, 3.4, 1.8, n_skin, group=22)
        if p.big:
            p.patch(14, 26 - L, N_FRUIT, N_LEG)
            p.patch(19, 6, N_BUD, N_LEG)
            p.eye(22, 14, 4, 7, iris="rd1", shine="sk2", shine_at=(1, 1))
            p.eye(28, 14, 3, 7, iris="rd1", shine="sk2", shine_at=(1, 1))
        else:
            p.blob(19, 31.5, 4.4, 4.0, n_rind, group=23)
            p.px(23, 16, "ink")
            p.px(29, 16, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the head turned right in profile,
        # the veil falling the length of her back, the fruit held out
        for (bx, by), (tx, ty), (hx, hy) in (((30, 10), (27, 3), (22.5, 4.5)), ((35, 8), (36, 2), (40, 3.5)),
                                             ((41, 9), (45, 4), (48, 6)), ((26, 14), (20, 11), (17.5, 13.5))):
            p.limb(bez((bx, by), (tx - 0.5, ty - 1), (hx, hy)), 2.6, 2.0, n_stem, group=70, bias=-0.2)
            p.drop((hx + 0.3, hy + 4.2), hx, hy + 1, 2.2, n_dry, group=71)
        # the robe: one long drape from the shoulders, its petals folding
        p.poly(bez3((26, 44), (20, 52), (14, 60), (10, 64)) + [(60, 64)]
               + bez3((58, 64), (54, 58), (50, 50), (48, 42)), n_robe, group=10)
        p.blob(37, 42, 12, 5, n_robe, group=10)
        for a, b, bend in (((31, 48), (22, 66), 1.0), ((38, 48), (42, 66), -0.4), ((44, 47), (56, 64), -1.0)):
            _robe(p, a, b, 8, bend=bend, tip=0, bias=0.05, group=36)
        p.blob(38, 41, 11, 5, n_robe, group=10)
        p.limb([(40, 37), (42, 28)], 6, 5.4, n_skin, group=12)
        p.lens((27, 40), (51, 39), 6.4, n_veil, bend=-1.4, group=11)
        # the arm reaching forward, the fruit on the palm
        p.limb(bez((47, 41), (53, 45), (55, 40)), 5, 4, n_skin, group=20)
        p.blob(56, 40, 3.2, 2, n_skin, group=21)
        if p.big:
            p.patch(51, 28, N_FRUIT, N_LEG)
        p.blob(38, 19, 11.5, 11, n_veil, group=4)
        p.blob(46.5, 22, 6, 7, n_skin, group=3)
        _vlock(p, (31, 12), (10, 34), 7.6, bend=1.4, bias=0.15, group=50)
        _vlock(p, (32, 18), (10, 52), 8.6, bend=1.4, bias=0.08, group=51)
        _vlock(p, (36, 23), (22, 62), 9.0, bend=1.0, group=52)
        _vlock(p, (40, 26), (36, 60), 6.4, bend=0.4, bias=-0.05, group=54)
        _vlock(p, (44, 14), (50, 27), 5.0, bend=-0.8, group=53)
        if p.big:
            p.patch(45, 8, N_BUD, N_LEG)
            p.eye(48, 18, 3, 6, iris="rd1", shine="sk2", shine_at=(1, 1))
            p.px(48, 25, "vi1")
        return

    if view in ("down", "up"):
        step = phase
        bob = step  # it drifts, rising and sinking
        for a, b in (((31, 38 - bob), (22, 56 - bob)), ((33, 38 - bob), (42, 56 - bob)), ((32, 38 - bob), (32, 58 - bob))):
            _robe(p, a, b, 10, fat=0.62, group=30)
        if view == "down":
            _vlock(p, (25, 18 - bob), (17, 50 - bob), 7, bend=-0.6, group=50)
            _vlock(p, (39, 18 - bob), (47, 50 - bob), 7, bend=0.6, group=51)
        p.limb([(32, 27 - bob), (32, 38 - bob)], 8, 6, n_robe, group=10)
        p.limb([(27, 29 - bob), (24, 36 - bob)], 2.8, 2.4, n_skin, group=20)
        p.limb([(37, 29 - bob), (40, 40 - bob)], 2.8, 2.4, n_skin, group=21)
        p.blob(32, 16 - bob, 9.6, 9, n_veil, group=4)
        for x, tx in ((28, 24), (32, 32), (36, 40)):
            p.limb(bez((x, 9 - bob), (x, 3 - bob), (tx, 4 - bob)), 2, 1.6, n_stem, group=70)
        if view == "down":
            p.blob(32, 19 - bob, 6.8, 6.6, n_skin, group=3)
            p.lens((40, 10 - bob), (27, 13 - bob), 5.6, n_veil, bend=1.4, group=5)
            p.blob(23, 35 - bob, 3.2, 3, n_rind, group=23)
            p.eye(27, 17 - bob, 3, 5, iris="rd1", shine="sk2", shine_at=(1, 1))
            p.eye(34, 17 - bob, 3, 5, iris="rd1", shine="sk2", shine_at=(1, 1))
        else:
            for a, b, bend in (((28, 18), (21, 50), -0.6), ((36, 18), (43, 50), 0.6), ((32, 20), (32, 54), 0.0)):
                _vlock(p, (a[0], a[1] - bob), (b[0] + step, b[1] - bob), 7.4, bend=bend)
        return

MONS = [
    Mon("Rhoaril", RHOARIL_COLORS, RHOARIL_SHINY, rhoaril, foot="root", icon_pal=1),
    # icon palette 1 keeps the green hair green and the gown pink
    Mon("Korantha", KORANTHA_COLORS, KORANTHA_SHINY, korantha, foot="root", icon_pal=1),
    Mon("Persenyx", PERSENYX_COLORS, PERSENYX_SHINY, persenyx, foot="blank"),
]
