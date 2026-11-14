"""Boar line: Kaplet, Kaprodon (Ground, then Dark/Ground). Demeter's piglet,
claimed by Artemis's woods and grown into the Calydonian boar."""
from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# Kaplet, the rooting piglet
# --------------------------------------------------------------------------

KAPLET_COLORS = [
    ("ink", INK),
    # limestone-tan hide, a warm shadow under it
    ("hide0", (128, 88, 56)), ("hide1", (176, 136, 88)), ("hide2", (208, 176, 128)), ("hide3", (232, 208, 168)),
    # terracotta mud, wet and dry
    ("mud0", (120, 48, 24)), ("mud1", (168, 80, 40)), ("mud2", (208, 120, 72)),
    # the broad pink snout
    ("snout0", (184, 104, 96)), ("snout1", (232, 160, 144)),
    # cypress-dark bristle ridge
    ("brist0", (24, 56, 40)), ("brist1", (48, 88, 64)),
    ("marble", C.white),
    ("earth", (88, 56, 32)),
]
KAPLET_SHINY = {
    # sun-gold, like a harvest piglet
    "hide0": (168, 104, 24), "hide1": (216, 152, 40), "hide2": (240, 192, 64), "hide3": (248, 224, 136),
}

k_hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.2, 0.46, 0.74])
k_snout = Mat(["snout0", "snout1"], line="hide0", cuts=[0.56])
k_brist = Mat(["brist0", "brist1"], line="brist0", cuts=[0.5])
k_hoof = Mat(["earth", "hide0"], cuts=[0.6])
k_mud = Mat(["mud0", "mud1", "mud2"], line="mud0", cuts=[0.3, 0.64])
k_clod = Mat(["earth", "mud0", "mud1"], line="earth", cuts=[0.3, 0.66])


def _kclods(p, L):
    """Clods of earth flicked up off the snout; L lifts them for frame 2."""
    for x, y, r in ((7.5, 47 - 2 * L, 1.9), (4.5, 41 - 3 * L, 1.4), (13.5, 37 - 2 * L, 1.1)):
        p.circle(x, y, r, k_clod)


def kaplet(p, view, phase):
    if view == "down":
        # follower trotting toward the camera: the round head, snout disc
        # in the middle, ears pricked, front trotters stepping
        st = phase
        p.limb([(27.5, 52), (27.5, 60 - 2 * st)], 4.6, 4.2, k_hide, group=12)
        p.limb([(36.5, 52), (36.5, 60 - 2 * (1 - st))], 4.6, 4.2, k_hide, group=13)
        p.rect(26, 58 - 2 * st, 29, 60 - 2 * st, k_hoof, group=14)
        p.rect(35, 58 - 2 * (1 - st), 38, 60 - 2 * (1 - st), k_hoof, group=15)
        p.blob(32, 50, 10, 7, k_hide, group=1)
        for sx in (-1, 1):
            ear = p.lens((32 + 5 * sx, 36), (32 + 11.5 * sx, 28.5 + st * (sx > 0)), 6.4, k_hide, bend=-1.0 * sx, group=5 + sx)
            p.lens((32 + 5.5 * sx, 35.5), (32 + 10 * sx, 30.5 + st * (sx > 0)), 2.6, k_snout, clip=[ear], group=5 + sx)
        p.blob(32, 42, 9.6, 8.6, k_hide, group=3)
        p.blob(32, 46.5, 4.4, 3.4, k_snout, group=4)
        p.lens((29, 33.5), (35, 33.5), 3, k_brist, group=7)
        if p.big:
            p.eye(26, 39, 2, 3, shine="marble", shine_at=(0, 0))
            p.eye(36, 39, 2, 3, shine="marble", shine_at=(0, 0))
            p.pxs([(30, 46), (33, 46)], "snout0")
            p.pxs([(31, 36), (32, 35), (33, 36)], "marble")
        else:
            p.pxs([(26.5, 40), (36.5, 40)], "ink")
        return

    if view == "up":
        # follower trotting away: the round rump, the curled tail, the
        # bristle ridge running up to the ears
        st = phase
        p.limb([(27, 52), (27, 60 - 2 * st)], 4.8, 4.4, k_hide, group=12)
        p.limb([(37, 52), (37, 60 - 2 * (1 - st))], 4.8, 4.4, k_hide, group=13)
        p.rect(25, 58 - 2 * st, 29, 60 - 2 * st, k_hoof, group=14)
        p.rect(35, 58 - 2 * (1 - st), 39, 60 - 2 * (1 - st), k_hoof, group=15)
        for sx in (-1, 1):
            p.lens((32 + 4.5 * sx, 33), (32 + 10.5 * sx, 25.5 + st * (sx > 0)), 6.0, k_hide, bend=-0.9 * sx, group=5 + sx)
        p.blob(32, 37, 8.4, 6.6, k_hide, group=3)
        p.blob(32, 48, 11, 9.4, k_hide, group=1)
        for y in (32.5, 36, 39.5):
            p.lens((32, y + 3), (32, y - 1), 2.6, k_brist, group=7)
        p.limb(bez3((32, 47), (37, 46.5), (37.5, 40.5), (33.5, 41)), 2.6, 2.2, k_hide, group=20)
        p.limb(bez((33.5, 41), (31.5, 42.5), (33, 44.5)), 2.2, 1.8, k_hide, group=20)
        p.blob(27.5, 52, 2.6, 2.0, k_mud, group=8)
        return

    if view in ("front", "icon", "side"):
        L = 1 if (phase == 1 and view == "front") else 0
        walk = view == "side" and phase == 1

        # far legs, in shade
        p.limb([(30, 52), (30.5 + walk, 58)], 4.4, 4.2, k_hide, bias=0.32, group=10)
        p.rect(29 + walk, 58, 32 + walk, 59, k_hoof, bias=0.3)
        p.limb([(39, 50), (39 - walk, 58)], 4.6, 4.2, k_hide, bias=0.32, group=11)
        p.rect(37 - walk, 58, 40 - walk, 59, k_hoof, bias=0.3)
        # far ear, pricked behind the crown
        fear = p.lens((33, 38.5 - L), (31, 30 - 2 * L), 6.4, k_hide, bend=0.8, fat=0.3, bias=0.22, group=5)
        p.lens((32.4, 37 - L), (31.2, 32 - 2 * L), 2.4, k_snout, fat=0.34, clip=[fear], bias=0.1, group=5)

        # tail: a tight curl on the raised rump
        p.limb(bez3((46, 39), (49.5, 39), (51.5, 35), (49.5, 33)), 2.4, 2.0, k_hide, group=20)
        p.limb(bez((49.5, 33), (47.5, 34), (48.5, 36)), 2.0, 1.6, k_hide, group=20)

        # body: a round barrel rising from the low chest to the round rump
        body = p.blob(35, 46.5, 9.6, 8.6, k_hide, ang=-22, group=1)
        p.blob(41, 42.5, 7.2, 7.8, k_hide, group=1)
        p.blob(30, 50, 6.4, 6.6, k_hide, group=1)
        p.blob(35, 54.5, 7, 2.4, k_hide, bias=0.25, clip=[body], group=1)
        # a splash of terracotta mud on the flank
        p.blob(36.5, 50, 3, 2.2, k_mud, ang=-15, clip=[body], group=8)

        # near hind leg: a plump ham over a short shank, a sock of mud
        p.blob(43.5, 47.5, 5.2, 6.6, k_hide, group=13)
        shank = p.limb([(44, 52), (44.5 - walk, 58)], 4.8, 4.4, k_hide, group=13)
        p.rect(41, 55, 48, 57, k_mud, clip=[shank], group=14)
        p.rect(42 - walk, 58, 46 - walk, 59, k_hoof)

        # head, lowered: a big round skull, the snout down in the dirt
        p.blob(24, 46.5 - L, 9.4, 8.6, k_hide, group=3)
        p.limb([(19.5, 49.5 - L), (15, 52 - L)], 8.6, 7.6, k_hide, group=3)
        # the snout disc, its flat face turned down and out
        p.blob(12, 52.5 - L, 3.1, 3.9, k_snout, ang=20, group=4)
        # the earth it is rooting in
        if view == "front":
            p.poly([(1.5, 60.5), (4, 56), (8, 53.5), (11, 55), (14, 58), (16, 60.5)], k_clod, group=9)

        # near foreleg, braced, a sock of mud
        leg = p.limb([(24.5, 53), (23 - walk, 58)], 5.2, 4.6, k_hide, group=12)
        p.rect(19, 56, 28, 57, k_mud, clip=[leg], group=15)
        p.rect(21 - walk, 58, 25 - walk, 59, k_hoof)

        # near ear: a soft triangle pricked forward, pink inside
        ear = p.lens((29.5, 39.5 - L), (18.5, 33.5 - 2 * L), 8.0, k_hide, bend=1.0, fat=0.3, group=6)
        p.lens((28, 39 - L), (21, 35.5 - 2 * L), 3.0, k_snout, bend=0.2, fat=0.34, clip=[ear], group=6, bias=0.1)

        # bristle ridge, crown to rump: short tufts swept back
        for a, b, w in (((33, 38.5), (35, 35), 2.4), ((36.5, 37), (38.5, 33.5), 2.6), ((40, 36), (42, 32.5), 2.6),
                        ((43.5, 35.5), (45.5, 33), 2.2)):
            p.lens(a, b, w, k_brist, group=7)

        if view == "front":
            _kclods(p, L)

        if p.big:
            p.eye(18, 43 - L, 3, 4, shine="marble", shine_at=(1, 1))
            # crescent on the brow
            p.pxs([(24, 40 - L), (23, 41 - L), (23, 42 - L), (24, 43 - L)], "marble")
            # nostrils
            p.pxs([(11, 52 - L), (13, 53 - L)], "snout0")
            # tusk nubs at the jaw
            p.pxs([(19, 55 - L), (20, 55 - L)], "marble")
        else:
            p.px(19, 45 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the round rump and ridged back, the head turned
        # right in profile, the snout disc toward the foe; cropped below
        # tail, curled on the rump
        p.limb(bez3((9, 47), (3, 46), (2.5, 40), (6.5, 38.5)), 2.8, 2.4, k_hide, group=20)
        p.limb(bez((6.5, 38.5), (9.5, 39.5), (7.5, 42.5)), 2.4, 2.0, k_hide, group=20)
        # far ear behind the head
        fear = p.lens((47, 19), (53, 8), 7.2, k_hide, bend=-1.0, fat=0.3, bias=0.22, group=5)
        p.lens((47.6, 18), (52, 10.5), 2.8, k_snout, fat=0.34, clip=[fear], bias=0.1, group=5)
        # body: the round rump close at the lower left, the back humping
        # up to the shoulders
        p.blob(25, 55, 22.5, 19.5, k_hide, group=1)
        p.blob(38, 41, 12.5, 12, k_hide, group=1)
        # the bristle ridge down the spine
        p.limb(bez3((9, 42), (17, 35), (28, 31.5), (41, 27.5)), 3.4, 3.0, k_brist, group=7)
        for a, b, w in (((10, 41), (6.5, 36.5), 3.0), ((14.5, 38), (12, 33.5), 3.2), ((19.5, 35.5), (17.5, 30.5), 3.4),
                        ((25, 33.5), (23.5, 28.5), 3.4), ((30.5, 32), (30, 27), 3.4), ((36, 30), (36.5, 25.5), 3.2)):
            p.lens(a, b, w, k_brist, fat=0.4, group=7)
        # head in profile, the snout pointing right
        p.blob(46, 26.5, 9.6, 9, k_hide, group=3)
        p.limb([(51, 29.5), (57, 31)], 9.6, 8.4, k_hide, group=3)
        p.blob(59.4, 31, 2.6, 4.6, k_snout, group=4)
        # near ear pricked up and forward
        ear = p.lens((42, 21), (49.5, 7.5), 8.4, k_hide, bend=-1.2, fat=0.3, group=6)
        p.lens((43.5, 20), (48.5, 10.5), 3.2, k_snout, fat=0.34, clip=[ear], bias=0.1, group=6)
        # mud on the rump
        p.blob(15, 52, 3.6, 2.6, k_mud, ang=-20, group=8)
        if p.big:
            p.eye(52, 24, 3, 4, shine="marble", shine_at=(1, 1))
            p.pxs([(50, 20), (51, 19), (52, 19), (53, 20)], "marble")
            p.pxs([(60, 30), (60, 33)], "snout0")
            p.pxs([(56, 35), (57, 35)], "marble")
        return
    return


# --------------------------------------------------------------------------
# Kaprodon, the Calydonian boar
# --------------------------------------------------------------------------

KAPRODON_COLORS = [
    ("ink", INK),
    # cypress-dark hide going to black-figure ink in the shadows
    ("hide0", (32, 40, 40)), ("hide1", (48, 72, 64)), ("hide2", (80, 112, 88)), ("hide3", (128, 160, 128)),
    # limestone tusks with a marble highlight and a moon-silver edge
    ("tusk0", (152, 128, 88)), ("tusk1", (200, 176, 128)), ("tusk2", (232, 216, 176)), ("marble", C.white),
    ("moon", (184, 200, 232)),
    # sun-gold eyes
    ("gold0", (200, 120, 32)), ("gold1", (248, 208, 72)),
    # the snout and mouth
    ("maw", (120, 56, 48)), ("snout", (152, 96, 80)),
    ("dust", (168, 136, 96)),
]
KAPRODON_SHINY = {
    # terracotta hide, sun-gold tusks
    "hide0": (96, 32, 24), "hide1": (144, 64, 32), "hide2": (192, 96, 48), "hide3": (232, 144, 88),
    "tusk0": (168, 112, 24), "tusk1": (216, 160, 40), "tusk2": (240, 208, 88), "marble": (248, 240, 184),
}

r_hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.26, 0.5, 0.76])
r_dark = Mat(["ink", "hide0", "hide1", "hide2"], line="ink", cuts=[0.22, 0.5, 0.8])
r_tusk = Mat(["tusk0", "tusk1", "tusk2", "marble"], line="tusk0", cuts=[0.2, 0.5, 0.78])
r_snout = Mat(["maw", "snout"], line="hide0", cuts=[0.5])
r_hoof = Mat(["ink", "hide0"], cuts=[0.6])


def _spear(p, base, tip, w, **kw):
    """One spear-like bristle: a long blade from base to tip."""
    return p.lens(base, tip, w, r_dark, fat=0.3, **kw)


def _tusk(p, path, w, mat=None, **kw):
    """A tusk along path: thick at the root, holding its width, then
    tapering to a point."""
    a = p._minw(w)
    poly = ribbon(path, lambda t: a * (1 - t ** 3.2) + 0.6 * t)
    return p.add(p.mask(poly, ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12)), mat or r_tusk, **kw)


def kaprodon(p, view, phase):
    if view == "down":
        # follower charging toward the camera: the crescent of tusks round
        # the snout, gold eyes under the brow, the spears a crown behind
        st = phase
        for sx in (-1, 1):
            p.limb([(32 + 7 * sx, 50), (32 + 7.5 * sx, 59 - 2 * (st if sx < 0 else 1 - st))], 5.6, 4.6, r_hide, group=12 + (sx > 0))
            yb = 58 - 2 * (st if sx < 0 else 1 - st)
            p.rect(32 + 7.5 * sx - 2.5, yb, 32 + 7.5 * sx + 2, yb + 2, r_hoof, group=14 + (sx > 0))
        for i, (bx, tx, ty, w) in enumerate(((26, 20, 14, 4.2), (29, 25.5, 8, 4.8), (32, 32, 5, 5.2), (35, 38.5, 8, 4.8), (38, 44, 14, 4.2))):
            _spear(p, (bx, 30), (tx, ty), w, bias=0.1 if i != 2 else -0.05, group=30 + i)
        p.blob(32, 45, 13, 9.5, r_hide, group=1)
        p.blob(32, 35, 10.5, 9, r_hide, group=3)
        p.limb([(32, 38), (32, 47)], 9, 7.4, r_hide, group=3)
        p.lens((24, 32), (31.5, 32.5), 4.4, r_hide, bend=1.0, group=6)
        p.lens((40, 32), (32.5, 32.5), 4.4, r_hide, bend=-1.0, group=6)
        _tusk(p, bez3((28, 47), (20, 48), (20, 37), (27, 32.5)), 4.4, group=40)
        _tusk(p, bez3((36, 47), (44, 48), (44, 37), (37, 32.5)), 4.4, group=41)
        p.blob(32, 48.5, 4.6, 3.2, r_snout, group=4)
        if p.big:
            for ex in (26, 36):
                p.patch(ex, 33, [".11.", "1bc1", ".11."], {"1": "ink", "b": "gold0", "c": "gold1"})
            p.pxs([(30, 48), (33, 48)], "ink")
        else:
            p.pxs([(27, 34), (37, 34)], "gold1")
        return

    if view == "up":
        # follower walking away: the row of spears down the spine, the
        # tail raised with its tassel, the tusk tips showing past the head
        st = phase
        for sx in (-1, 1):
            p.limb([(32 + 7.5 * sx, 50), (32 + 8 * sx, 59 - 2 * (st if sx < 0 else 1 - st))], 5.6, 4.6, r_hide, group=12 + (sx > 0))
            yb = 58 - 2 * (st if sx < 0 else 1 - st)
            p.rect(32 + 8 * sx - 2.5, yb, 32 + 8 * sx + 2, yb + 2, r_hoof, group=14 + (sx > 0))
        _tusk(p, bez((25, 30), (19, 26), (22, 20)), 3.4, bias=0.1, group=40)
        _tusk(p, bez((39, 30), (45, 26), (42, 20)), 3.4, bias=0.1, group=41)
        p.blob(32, 30, 9, 7.6, r_hide, group=3)
        p.blob(32, 45, 13.5, 11, r_hide, group=1)
        for i, (y, h, lean) in enumerate(((28, 17, -2.5), (32.5, 16, 2.5), (37, 14, -1.5), (41.5, 11, 1.5), (46, 8, -0.5))):
            _spear(p, (32, y + 2), (32 + lean + st * 0.5, y - h), 4.8, bias=0.22 - 0.06 * i, group=30 + i)
        p.limb(bez((32, 53), (31, 49), (32.5, 46)), 2.6, 2.0, r_hide, group=20)
        p.lens((32.5, 47), (33.5 - 2 * st, 40), 3.6, r_dark, group=21)
        return

    if view in ("front", "icon", "side"):
        L = 1 if (phase == 1 and view == "front") else 0
        dust = Mat(["tusk0", "dust"], line="tusk0", cuts=[0.5])

        # tail, raised for the charge, a black tassel at its tip
        p.limb(bez((58, 34), (61.5, 30), (60.5, 23)), 2.4, 1.8, r_hide, group=20)
        p.lens((60.5, 24), (59, 16.5 - L), 3.8, r_dark, bend=-0.6, group=21)

        # far legs, in shade: slim dark shanks under heavy forearms
        p.limb([(49, 45), (50, 51)], 6.6, 4.4, r_hide, bias=0.32, group=10)
        p.limb([(50, 51), (49, 57.5)], 3.6, 3.2, r_dark, bias=0.2, group=10)
        p.poly([(46.5, 57.5), (51.5, 57.5), (51.5, 60.5), (46.5, 60.5)], r_hoof, group=10)
        p.limb([(32, 46), (31, 52)], 7.6, 5.2, r_hide, bias=0.32, group=11)
        p.limb([(31, 52), (31.5, 57.5)], 4.2, 3.6, r_dark, bias=0.2, group=11)
        p.poly([(28.5, 57.5), (34, 57.5), (34, 60.5), (28.5, 60.5)], r_hoof, group=11)

        # the spear ridge, brow to back: a dark back rank and a front rank,
        # tallest over the shoulder hump, raked back
        for a, b, w in (((27, 22), (22, 9.5), 4.0), ((31, 19.5), (29, 4), 4.8), ((35.5, 19), (36.5, 2.5), 5.0),
                        ((40, 20), (44, 4.5), 4.8), ((44.5, 22), (50, 9.5), 4.4), ((48.5, 25), (55, 15), 3.8)):
            _spear(p, a, (b[0], b[1] - L), w, bias=0.25, group=30)
        for a, b, w in (((25, 24.5), (18.5, 14), 3.6), ((29, 21), (25.5, 8.5), 4.4), ((33.5, 20), (32.5, 6.5), 4.6),
                        ((38, 20.5), (40, 7.5), 4.6), ((42.5, 21.5), (46.5, 11), 4.2), ((46.5, 23.5), (52, 15.5), 3.8),
                        ((50.5, 26.5), (56, 21), 3.2)):
            _spear(p, a, (b[0], b[1] - L), w, bias=-0.05, group=31)

        # body: the shoulder hump high, the barrel sloping to a small rump
        b1 = p.blob(33, 33, 12.5, 14, r_hide, group=1)
        b2 = p.blob(44, 37, 12.5, 10.5, r_hide, ang=10, group=1)
        b3 = p.blob(53.5, 38, 7, 9, r_hide, group=1)
        p.blob(42, 47, 11, 2.4, r_hide, bias=0.3, clip=[b1, b2, b3], group=1)

        # near hind leg: a heavy ham, the hock, the hoof planted
        p.blob(52.5, 42, 6.6, 8.2, r_hide, group=13)
        p.limb([(53.5, 47), (56, 52)], 6.0, 4.4, r_hide, group=13)
        p.limb([(56, 52), (55, 57.5)], 4.0, 3.4, r_dark, group=13)
        p.poly([(52.5, 57.5), (57.5, 57.5), (57.5, 60.5), (52.5, 60.5)], r_hoof, group=13)

        # head lowered to charge: a great wedge from the hump down to the snout
        p.blob(23, 35 - L, 9.6, 9.6, r_hide, group=3)
        p.limb([(21, 37 - L), (11, 48.5 - L)], 13, 8, r_hide, group=3)
        p.blob(19, 45 - L, 7, 5, r_hide, bias=0.14, group=3)
        # the heavy brow over the eye
        p.lens((15.5, 30.5 - L), (29, 27 - L), 5.4, r_hide, bend=1.0, group=6)
        # far tusk, rising behind the snout, its tip curling in
        _tusk(p, bez3((15, 50.5 - L), (23, 47.5 - L), (22, 33 - L), (13.5, 29.5 - L)), 4.4, bias=0.16, group=40)

        # ear laid back flat against the ridge
        p.lens((28, 26.5 - L), (35, 22.5 - L), 5.0, r_hide, bend=-0.8, group=5)

        # near foreleg pawing the ground: knee forward, the hoof scraping back
        p.blob(27, 44, 7, 7.4, r_hide, group=12)
        p.limb([(26, 47), (21.5, 51.5)], 6.8, 5.4, r_hide, group=12)
        p.limb([(21.5, 51.5), (24, 55)], 4.4, 3.6, r_dark, group=14)
        p.poly([(21.5, 54.5), (26, 54.5), (25.5, 57.5), (22.5, 58)], r_hoof, group=15)
        if view == "front":
            # dust kicked up behind the hoof
            for x, y, r in ((28, 59.6, 1.7), (31 + L, 58.4 - L, 1.2), (25.6, 60.6, 1.3)):
                p.circle(x, y, r, dust, group=16)

        # near tusk sweeping out and up, its tip curling in to meet the far one
        _tusk(p, bez3((11, 51.5 - L), (2, 51.5 - L), (1.6, 35 - L), (8, 30 - L)), 5.2, group=41)
        # snout disc over the tusk roots
        p.blob(9.5, 51.5 - L, 3.8, 2.6, r_snout, ang=-20, group=4)

        if p.big:
            p.patch(23, 31 - L, [".111.", "1bcb1", ".111."], {"1": "ink", "b": "gold0", "c": "gold1"})
            p.pxs([(8, 51 - L), (11, 52 - L)], "ink")
        else:
            p.px(25, 32 - L, "gold1")
        return

    if view == "back":
        # over the shoulder: the great back with its row of spears raised
        # against the sky, the head turned right in profile, the tusk
        # crescent before the burning eye; cropped below
        # tail, raised, at the far left
        p.limb(bez((7, 50), (3, 46), (4, 38)), 3.0, 2.4, r_hide, group=20)
        p.lens((4, 39), (6.5, 30), 4.4, r_dark, bend=0.8, group=21)
        # far tusk behind the snout
        _tusk(p, bez3((52.5, 44), (59, 43), (59.5, 31), (55.5, 26)), 4.2, bias=0.18, group=40)
        # the spear row along the spine, rump to nape; back rank, then front
        spine = [(8, 45), (14.5, 40.5), (21, 36.5), (27.5, 33), (34, 30), (40, 27.5)]
        for i, (x, y) in enumerate(spine[:-1]):
            nx, ny = spine[i + 1]
            mx, my = (x + nx) / 2, (y + ny) / 2
            h = 14 + 3 * min(i, 4 - i)
            _spear(p, (mx + 1, my + 2), (mx - 2.5, my - h), 5.0, bias=0.25, group=30)
        for i, (x, y) in enumerate(spine):
            h = 12 + 4 * min(i, 5 - i)
            _spear(p, (x + 1, y + 2.5), (x - 3, y - h), 5.4, bias=-0.05, group=31)
        # body: the rump close at the lower left, the hump rising to the neck
        p.blob(21, 61, 20, 18, r_hide, group=1)
        p.blob(34, 46, 16, 15.5, r_hide, ang=-20, group=1)
        p.blob(43, 37, 9, 9, r_hide, group=1)
        # head in profile, the snout pointing right
        p.blob(45, 31, 9.6, 9.4, r_hide, group=3)
        p.limb([(48, 33), (57, 39)], 12, 7.6, r_hide, group=3)
        # heavy brow over the eye
        p.lens((40, 25.5), (53, 27.5), 5.6, r_hide, bend=1.0, group=6)
        # ear laid back
        p.lens((42, 23), (34.5, 19.5), 5.6, r_hide, bend=0.8, group=5)
        # near tusk: up from the jaw behind the snout, curling back to the eye
        _tusk(p, bez3((51, 45), (57.5, 45), (58, 33), (53, 27.5)), 5.2, group=41)
        # snout disc out front
        p.blob(59.4, 40, 1.9, 3.6, r_snout, ang=-25, group=4)
        if p.big:
            p.patch(46, 28, [".111.", "1bcb1", ".111."], {"1": "ink", "b": "gold0", "c": "gold1"})
        return
    return


MONS = [
    Mon("Kaplet", KAPLET_COLORS, KAPLET_SHINY, kaplet, foot="hoof"),
    Mon("Kaprodon", KAPRODON_COLORS, KAPRODON_SHINY, kaprodon, foot="hoof"),
]
