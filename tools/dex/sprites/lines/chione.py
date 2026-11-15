"""Chione line: Niflake, Chionyad (Ice, then Ice/Fairy). Chione the snow nymph,
daughter of Boreas the North Wind.

The code drafts below give the icons and follower frames. The battle sprites
are hand-finished in tools/dex/sprites/art/: Niflake's flake was laid from
distance fields at exact arm widths so its frost stays white inside the ink,
and Chionyad's face, circlet, arms, flurry and gown detail are laid by hand
over the draft's hair and gown."""
import math

from mon_lib import C, Mat, Mon, bez, bez3, lens_pts, ellipse_pts, ribbon  # noqa: F401

INK = C.ink


def _at(cx, cy, r, ang, sx=1.0):
    """The point r from (cx, cy) at ang degrees (counterclockwise from +x,
    screen y down), with the x axis foreshortened by sx."""
    a = math.radians(ang)
    return (cx + sx * r * math.cos(a), cy - r * math.sin(a))


def _hexagon(cx, cy, r, ang=90.0, sx=1.0):
    return [_at(cx, cy, r, ang + 60 * i, sx) for i in range(6)]


# --------------------------------------------------------------------------
# Niflake, the snowflake sprite
# --------------------------------------------------------------------------

NIFLAKE_COLORS = [
    ("ink", INK),
    # the core: the darker Aegean blue of the North Wind's sky
    ("deep", (24, 40, 104)), ("core", (40, 80, 168)), ("aegean", (64, 128, 208)),
    # snow: lilac in shadow, sky blue, pale, marble white
    ("lilac", (136, 144, 216)), ("sky", (136, 192, 240)), ("pale", (200, 232, 248)), ("white", (248, 248, 248)),
    ("blush", (224, 168, 208)),
]
NIFLAKE_SHINY = {
    # sun-gold frost, like snow at sunrise
    "deep": (128, 64, 24), "core": (192, 112, 32), "aegean": (232, 160, 48),
    "lilac": (216, 152, 112), "sky": (240, 200, 104), "pale": (248, 232, 176),
    "blush": (240, 160, 136),
}

n_snow = Mat(["lilac", "sky", "pale", "white"], line="aegean", cuts=[0.2, 0.44, 0.7])
n_core = Mat(["deep", "core", "aegean"], line="deep", cuts=[0.3, 0.62])
n_face = Mat(["sky", "pale", "white"], line="aegean", cuts=[0.34, 0.62])

NIFLAKE_ARMS = (90, 30, -30, -90, 150, 210)


def _blade(p, a, b, w, mat, lit, shade, fat=0.45, group=None, sheen=None):
    """A crystal blade from a to b, split along its ridge into a lit half
    (facing the upper-left light) and a shaded half, flat-toned."""
    pts = lens_pts(a, b, p._minw(w), 0.0, fat=fat)
    pid = p.poly(pts, mat, flat=shade, group=group)
    if not p.big or not pid:
        return pid
    n = len(pts) // 2
    left, right = pts[:n + 1], pts[n + 1:][::-1]
    mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(left, right)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    edge = left if dy - dx > 0 else right
    p.poly(edge + mid[::-1], mat, clip=[pid], flat=lit, noline=True)
    return pid


def _flake(p, cx, cy, R, spin=0.0, sx=0.86, w=4.6, group0=10, mat=None, branch=True, bw=3.2, hub=3.0):
    """A six-armed stellar snowflake: crystal blades from the hub, each
    branching into a V of frost and a smaller V near its tip. Each blade
    is lit on the half facing the upper left; arms pointing down and right
    sit a tone darker."""
    mat = mat or n_snow
    for k, a0 in enumerate(NIFLAKE_ARMS):
        a = a0 + spin
        lit_arm = math.cos(math.radians(a - 135)) > -0.3
        lit, shade = (3, 2) if lit_arm else (2, 1)
        g = group0 + k
        _blade(p, _at(cx, cy, hub, a, sx), _at(cx, cy, R, a, sx), w, mat, lit, shade, group=g)
        if branch:
            for frac, ln, ww in ((0.5, 0.38, bw), (0.76, 0.22, bw * 0.8)):
                root = _at(cx, cy, R * frac, a, sx)
                for side in (-1, 1):
                    b = a + side * 58
                    end = (root[0] + sx * R * ln * math.cos(math.radians(b)),
                           root[1] - R * ln * math.sin(math.radians(b)))
                    _blade(p, root, end, ww, mat, lit, shade, fat=0.5, group=g)


def niflake(p, view, phase):
    if view in ("front", "side", "icon"):
        bob = 1 if (phase == 1 and view == "front") else 0
        spin = 9 if phase == 1 else 0
        cx, cy = 31.5, 39 - bob

        # loose flakes trailing behind
        for (fx, fy, r) in ((52, 31 - bob, 3.2), (56, 41, 2.2), (49.5, 49 + bob, 1.8)):
            _flake(p, fx, fy, r, spin=20 + spin * 2, sx=0.9, w=2.2, group0=40, branch=False)

        _flake(p, cx, cy, 16.5, spin=12 + spin)
        # the darker Aegean-blue core
        p.poly(_hexagon(cx, cy, 8.4, 102 + spin, 0.92), n_core, group=2)
        # the little crystal arms, reaching forward
        p.taper([(26, 44.5 - bob), (20.5, 46.5 - bob)], 2.6, n_snow, group=30)
        p.taper([(34.5, 45 - bob), (38, 48.5 - bob)], 2.4, n_snow, group=31, bias=0.15)
        # the sleepy round face
        p.blob(30.5, 39.5 - bob, 5.4, 5.2, n_face, group=3)
        if p.big:
            L = bob
            p.patch(26, 38 - L, ["1111.111", ".dd...dd"] if phase == 0 else ["1111.111", ".11...11"],
                    {"1": "ink", "d": "deep"})
            p.px(30, 42 - L, "deep")
            p.pxs([(25, 41 - L), (34, 41 - L)], "blush")
        else:
            p.pxs([(27, 39), (32, 39)], "ink")
        return

    if view == "back":
        cx, cy = 30, 46
        _flake(p, cx, cy, 20, spin=8, w=4.6)
        p.poly(_hexagon(cx, cy, 10.5, 98, 0.92), n_core, group=2)
        p.blob(36, 44, 6.4, 7.4, n_face, group=3)
        if p.big:
            p.patch(39, 43, ["111", ".dd"], {"1": "ink", "d": "deep"})
        return

    if view in ("down", "up"):
        spin = 8 * phase
        cx, cy = 32, 40
        _flake(p, cx, cy, 15, spin=spin, sx=1.0)
        p.poly(_hexagon(cx, cy, 7.8, 90 + spin), n_core, group=2)
        if view == "down":
            p.taper([(27, 45), (22, 48)], 2.6, n_snow, group=30)
            p.taper([(37, 45), (42, 48)], 2.6, n_snow, group=31)
            p.blob(32, 40, 5.8, 5.4, n_face, group=3)
            p.pxs([(28, 40), (29, 40), (35, 40), (36, 40)], "ink")
        return


# --------------------------------------------------------------------------
# Chionyad, the snow nymph
# --------------------------------------------------------------------------

CHIONYAD_COLORS = [
    ("ink", INK),
    # hair: the North Wind's deep Aegean blue
    ("deep", (24, 40, 104)), ("navy", (40, 80, 168)), ("aegean", (64, 128, 208)), ("azure", (112, 176, 240)),
    # the gown of falling snow: lilac in its deepest folds, sky, pale, white
    ("lilac", (128, 136, 208)), ("sky", (160, 200, 240)), ("pale", (208, 232, 248)), ("white", (248, 248, 248)),
    # marble skin, cool in shadow
    ("marble", (232, 232, 240)), ("mshade", (184, 184, 224)),
    # the circlet's sun-gold glint
    ("gold0", (200, 136, 40)), ("gold", (248, 208, 88)),
    ("glow", (216, 248, 248)),
    # her Aegean-blue eyes, which stay blue in the shiny
    ("iris", (48, 112, 208)),
]
CHIONYAD_SHINY = {
    # her gown and hair turn pale sun-gold, like snow lit by dawn
    "deep": (128, 72, 24), "navy": (184, 120, 40), "aegean": (224, 168, 64), "azure": (248, 208, 112),
    "lilac": (216, 168, 112), "sky": (240, 208, 144), "pale": (248, 232, 192), "white": (248, 248, 232),
    "glow": (248, 240, 200),
    # the circlet's glint turns ice blue against the gold
    "gold0": (40, 96, 176), "gold": (120, 184, 240),
}

c_hair = Mat(["deep", "navy", "aegean", "azure"], line="deep", cuts=[0.2, 0.46, 0.74])
c_gown = Mat(["lilac", "sky", "pale", "white"], line="lilac", cuts=[0.24, 0.48, 0.72])
c_skin = Mat(["mshade", "marble", "white"], line="mshade", cuts=[0.4, 0.66])
c_crys = Mat(["aegean", "sky", "pale", "white"], line="aegean", cuts=[0.2, 0.44, 0.7])
c_gold = Mat(["gold0", "gold"], line="gold0", cuts=[0.55])


def _star(p, x, y, r, mat=None, group=None, sx=1.0, spin=0.0):
    """A small six-pointed snow crystal centred on (x, y)."""
    mat = mat or c_crys
    ids = []
    for k in range(3):
        a = spin + 90 + 60 * k
        ids.append(p.poly(lens_pts(_at(x, y, r, a, sx), _at(x, y, r, a + 180, sx), max(1.2, r * 0.55), fat=0.5),
                          mat, group=group))
    return ids


def _lock(p, path, w, mat, start=0.62, **kw):
    """A lock of hair (or a streamer of snow) along a curve: it swells from
    its root and sweeps to a fine point."""
    def width(t):
        return w * max(0.0, math.sin(math.pi * (start * 0.5 + (1 - start * 0.5) * t))) ** 0.75
    return p.poly(ribbon(path, width), mat, **kw)


def chionyad(p, view, phase):
    if view in ("front", "side", "icon"):
        p.oy += 2 * p.s              # the whole figure sits 2 px lower
        try:
            _chionyad_front(p, view, phase)
        finally:
            p.oy -= 2 * p.s
        return
    _chionyad_other(p, view, phase)


def _chionyad_front(p, view, phase):
    L = 1 if (phase == 1 and view == "front") else 0     # she rises a pixel
    sw = 2 * phase if view == "front" else 0             # hair and gown stream further

    # hair streaming back in the north wind: one mass from the crown
    # that fans into four broad, curving locks whose tips flick up
    def H(pts):
        # the locks stream back, pulled in a little; in frame 2 they
        # stream further on a gust
        return [(x if x < 28 else 28 + (x - 28) * 0.84 + sw * (x - 28) / 22.0, y - L) for x, y in pts]
    hair = H(bez3((14.5, 9), (14, 4), (20, 1.6), (28, 2)) +
             bez3((28, 2), (38, 2.4), (47, 2.6), (54, 5.4)) +          # the crown's sweep
             bez3((54, 5.4), (58, 7.4), (60, 10), (57, 12.6)) +        # lobe 1, curling under
             bez3((57, 12.6), (55, 13.6), (53, 13.6), (51.6, 13.8)) +
             bez3((51.6, 13.8), (56, 15), (59, 18.6), (55.6, 21.6)) +  # lobe 2
             bez3((55.6, 21.6), (53, 23), (50, 22.6), (48.6, 22.8)) +
             bez3((48.6, 22.8), (53, 25), (54, 29), (49.6, 31)) +      # lobe 3, the lowest
             bez3((49.6, 31), (42, 32), (33, 28), (27, 20)) + [(24, 13), (18, 10)])
    hid = p.poly(hair, c_hair, group=50)
    if p.big:
        # lit bands along the top of each lock, strands between them
        for pts in (bez3((22, 3.4), (34, 3), (46, 3.6), (55, 7.6)) + bez3((55, 7.6), (47, 7), (36, 6.6), (24, 6)),
                    bez3((32, 13.6), (42, 13.4), (52, 14.6), (57, 18.4)) + bez3((57, 18.4), (50, 17), (41, 16.6), (32, 16.4)),
                    bez3((32, 21.6), (40, 22), (48, 23.6), (52, 27.6)) + bez3((52, 27.6), (46, 25.6), (39, 25), (32, 24.4))):
            p.poly(H(pts), c_hair, clip=[hid], flat=3, noline=True)
        for path in (bez3((51.6, 13.8), (44, 12), (36, 11), (28, 10.4)), bez3((48.6, 22.8), (42, 21), (35, 19.6), (29, 18.4))):
            p.stroke(H(path), "deep")

    # the gown of falling snow: fitted at the bodice, then curving
    # down under her and sweeping back into a comet's tail of snow
    front = bez3((18.6, 31), (15.4, 37), (15.6, 45), (23, 49.6))
    hem = bez3((23, 49.6), (31, 52.5), (41, 50), (47 + sw, 46.6)) + [(52 + sw, 43.6), (56.5 + sw, 40)]
    back = bez3((56.5 + sw, 40), (46, 39.4), (34, 38), (27.4, 31))
    gid = p.poly(front + hem + back, c_gown, group=30)
    # it deepens to sky blue toward the hem
    p.poly(bez3((10, 44), (24, 48.5), (40, 45), (64, 36)) + [(64, 64), (10, 64)], c_gown, clip=[gid], group=30,
           bias=0.26)
    # fold shadows streaming back from the waist
    for path in (bez((23.5, 33), (21.5, 41), (24, 49)), bez((26.5, 33.5), (29, 42), (35, 49)),
                 bez((28.5, 33), (37, 39.5), (47, 44))):
        p.shade(ribbon(path, lambda t: 1.2 + 1.6 * t), 0.24)
    # snow drifting from the hem and the tail, thinning away
    if not p.big:
        for (x, y, r) in ((26, 53.6, 2.0), (34, 54, 2.0), (42, 52, 1.8), (50 + sw, 47.6, 1.7)):
            _star(p, x, y, r, c_gown)

    # slender shoulders and chest, the snow bodice under a deep-blue band
    p.blob(19.6, 21.2 - L, 5.2, 2.2, c_skin, group=1)
    p.limb([(19.6, 21.2 - L), (20.4, 29.6)], 7.0, 5.4, c_skin, group=1)
    p.poly([(14.8, 23.4 - L), (17, 22.4 - L), (19.4, 23.2 - L), (21.8, 22.4 - L), (24.4, 23.6 - L), (23.4, 30.2),
            (17.4, 30.2)], c_gown, group=31)
    p.limb([(17.4, 31), (24, 31)], 1.6, 1.6, Mat(["deep", "navy"], line="deep", cuts=[0.5]), group=32)

    # neck and head
    p.limb([(16.6, 17 - L), (17.6, 21 - L)], 2.8, 3.2, c_skin, group=2)
    p.blob(15.8, 11.4 - L, 5.4, 6.2, c_skin, group=3)
    p.blob(14.8, 15.6 - L, 3.2, 2.4, c_skin, ang=-10, group=3)

    # the hair cap over the crown, back from a hairline swept clear of
    # the brow, and the lock falling behind the neck
    p.poly([(10, 8), (12, 3.6), (17.6, 1.6 - L), (24, 3), (25.6, 9), (24.6, 16), (22.6, 21), (20.6, 21),
            (20.4, 13), (19, 7.4 - L), (15, 6.4 - L), (11.6, 7.4)], c_hair, group=40)
    # the circlet: a thin crystal band along the hairline, its snowflake
    # rising at the brow with a sun-gold jewel at its heart
    p.limb([(10.4, 8.4 - L), (13, 6.8 - L), (16.6, 6.2 - L), (20, 6.8 - L)], 1.4, 1.2, c_crys, group=44)
    _star(p, 16, 2.6 - L, 3.2, c_crys, group=45, spin=10)
    p.circle(16, 2.6 - L, 1.0, c_gold, group=46)

    # near arm: down from the shoulder, the forearm up to the hands cupped
    # beneath the flurry
    p.limb([(13.6, 22.6 - L), (12.6, 28.6)], 2.6, 2.2, c_skin, group=22)
    p.limb([(12.6, 28.6), (9.6, 25.6)], 2.2, 2.0, c_skin, group=22)
    p.blob(9, 25.4, 2.6, 1.6, c_skin, ang=-10, group=23)
    # the flurry she holds
    _star(p, 8.6, 20, 2.8, c_crys, group=60, spin=12 + 15 * phase)
    _star(p, 3.6, 15.6, 1.2, c_crys, group=61)
    _star(p, 3.6, 25, 1.2, c_crys, group=62)

    if p.big:
        # big calm Aegean-blue eyes with a shine; no nose, no mouth
        p.patch(10, 10 - L, ["11..1111", "9f..f9f", "1f..f1f", "fe..efe"],
                {"1": "ink", "f": "iris", "9": "white", "e": "glow"})
        p.px(8, 20, "glow")
    else:
        p.pxs([(11, 12 - L), (15.6, 12 - L)], "ink")
    return


def _chionyad_other(p, view, phase):
    if view == "back":
        # over the shoulder at about 1.2x: her bare back and shoulders, the
        # head turned right into profile under the circlet, her hair
        # streaming back to the left, the gown of snow cropped below
        hair = (bez3((44, 9), (40, 3.4), (30, 3), (22, 5)) +
                bez3((22, 5), (14, 6.4), (7, 6), (3, 9.6)) +              # lobe 1, curling under
                bez3((3, 9.6), (5, 13), (9, 14), (12, 14.4)) +
                bez3((12, 14.4), (7, 16), (3.4, 19), (5, 23)) +           # lobe 2
                bez3((5, 23), (8, 24.6), (12, 24), (15, 24)) +
                bez3((15, 24), (10, 27), (9.4, 31.6), (13, 34)) +         # lobe 3
                bez3((13, 34), (20, 34.6), (28, 32), (34, 28)) + [(38, 22)])
        hid = p.poly(hair, c_hair, group=50)
        if p.big:
            for pts in (bez3((40, 5.6), (30, 4.4), (18, 6.4), (5, 9.6)) + bez3((5, 9.6), (16, 9), (28, 8), (40, 8.4)),
                        bez3((32, 14), (22, 14), (12, 15.6), (5.4, 20.4)) + bez3((5.4, 20.4), (13, 18), (22, 17.4), (32, 17)),
                        bez3((32, 23), (24, 24), (16, 26), (11.6, 31)) + bez3((11.6, 31), (17, 28), (24, 27), (32, 26))):
                p.poly(pts, c_hair, clip=[hid], flat=3, noline=True)
            for path in (bez3((12, 14.4), (20, 12.6), (28, 12), (36, 12.6)), bez3((15, 24), (22, 21.6), (29, 20.6), (36, 20))):
                p.stroke(path, "deep")
        # the gown, cropped by the frame, deepening to blue below
        gid = p.poly(bez3((10, 64), (12, 55), (18, 49), (26, 47.6)) + [(48, 47.6)] +
                     bez3((48, 47.6), (55, 49), (60, 55), (62, 64)), c_gown, group=30)
        p.poly([(0, 56), (64, 54), (64, 64), (0, 64)], c_gown, clip=[gid], group=30, bias=0.24)
        # the bare back, shoulder blades and the line of the spine
        p.blob(38, 37.6, 14.6, 6.6, c_skin, group=1)
        p.limb([(38, 38), (37.6, 48)], 22, 18, c_skin, group=1)
        p.shade(ribbon(bez((39, 33), (39.4, 40), (39, 47)), lambda t: 1.4), 0.2)
        p.shade(ellipse_pts(32, 39, 4.0, 2.2, -20), 0.14)
        p.shade(ellipse_pts(45, 39, 4.0, 2.2, 20), 0.14)
        # the bodice's back and its deep-blue band
        p.poly([(27.6, 44), (32, 42.4), (38, 43.6), (44, 42.4), (48.4, 44), (48.6, 48), (27.4, 48)], c_gown, group=31)
        p.limb([(27, 48.4), (49, 48.4)], 2.0, 2.0, Mat(["deep", "navy"], line="deep", cuts=[0.5]), group=32)
        # the near arm, falling from the shoulder, the forearm reaching forward
        p.limb(bez((25.4, 36), (22.4, 42), (24.4, 48)), 4.8, 4.0, c_skin, group=22)
        # a lock of hair falling down her back from the nape
        lk = _lock(p, bez3((38.6, 26), (36, 33), (37.6, 39), (34.6, 45)), 5.6, c_hair, group=41, start=0.95)
        if p.big:
            _lock(p, bez3((37.4, 27), (35.4, 33), (36.4, 38), (34.6, 43)), 1.8, c_hair, clip=[lk], flat=3, noline=True)
        # neck, then the head turned right in profile
        p.limb([(41, 33), (42.4, 26)], 5.4, 5.0, c_skin, group=2)
        p.blob(44, 18.6, 7.2, 8.2, c_skin, group=3)
        p.blob(47.6, 24.4, 3.6, 2.8, c_skin, ang=24, group=3)
        # the hair over the crown and down the nape, back from the hairline
        p.poly([(33, 10), (36.6, 5.4), (43, 3.6), (49, 5.2), (52, 9.4), (50, 10.6), (47.6, 10.4), (45, 12),
                (43.4, 17.4), (42, 24), (40.6, 30.6), (37, 31), (34, 25)], c_hair, group=40)
        # the circlet: a crystal band, and its snowflake rising at the brow
        p.limb([(45.6, 11.6), (48.6, 10.2), (51.6, 10.6)], 1.4, 1.2, c_crys, group=44)
        _star(p, 48, 6.4, 4.0, c_crys, group=45, spin=-10)
        p.circle(48, 6.4, 1.1, c_gold, group=46)
        if p.big:
            p.patch(48, 16, ["1111", "i9i", "i1i", "eie"], {"1": "ink", "i": "iris", "9": "white", "e": "glow"})
        return

    if view in ("down", "up"):
        # follower: gliding toward or away from the camera, her hair
        # streaming back in wavy locks on both sides, the gown dissolving
        # into snow; the locks and the drifting flakes sway in turn
        sw = phase
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            s_ = sw if sx < 0 else 1 - sw
            hair = [(X(30), 6), (X(38), 5), (X(44), 9), (X(49), 13 + s_), (X(46), 16), (X(50), 21 + s_), (X(45), 24),
                    (X(48), 30 + s_), (X(42), 30), (X(38), 26), (X(34), 20)]
            p.poly(hair, c_hair, group=50 + (sx > 0))
        gown = bez3((28.4, 31), (24, 38), (19, 46), (16, 53)) + [(22, 54.6), (27, 53.4), (32, 55), (37, 53.4), (42, 54.6),
                                                               (48, 53)] + bez3((48, 53), (45, 46), (40, 38), (35.6, 31))
        gid = p.poly(gown, c_gown, group=30)
        p.poly([(0, 46), (64, 46), (64, 64), (0, 64)], c_hair, clip=[gid], group=30, flat=3, noline=True)
        for (x, y, r) in ((19, 58, 2.2), (27, 59, 1.8), (36, 59, 1.8), (45, 58, 2.2)):
            _star(p, x, y + (sw if x < 32 else 1 - sw), r, c_gown)
        p.limb([(32, 22), (32, 31.5)], 7, 6, c_skin, group=1)
        p.poly([(27.6, 26), (30, 25), (32, 26), (34, 25), (36.4, 26), (35.6, 31.6), (28.4, 31.6)], c_gown, group=31)
        p.limb([(28, 31.6), (36, 31.6)], 1.6, 1.6, Mat(["deep", "navy"], line="deep", cuts=[0.5]), group=32)
        if view == "down":
            # arms down to the elbows and the hands cupped before her
            p.limb([(27.4, 23.6), (25.6, 29), (30, 30.4)], 2.6, 2.2, c_skin, group=22)
            p.limb([(36.6, 23.6), (38.4, 29), (34, 30.4)], 2.6, 2.2, c_skin, group=23)
            _star(p, 32, 27 - sw, 2.6, c_crys, group=60, spin=15 * sw)
        else:
            p.limb([(27.4, 23.6), (25.4, 30.4)], 2.6, 2.2, c_skin, group=22)
            p.limb([(36.6, 23.6), (38.6, 30.4)], 2.6, 2.2, c_skin, group=23)
        p.limb([(32, 18), (32, 22.6)], 3.2, 3.4, c_skin, group=2)
        p.blob(32, 13.4, 6.4, 7.0, c_skin, group=3, bias=-0.25)
        if view == "down":
            p.poly(bez3((25.4, 11), (26, 5.4), (38, 5.4), (38.6, 11)) + bez3((38.6, 11), (35, 8.6), (29, 8.6), (25.4, 11)),
                   c_hair, group=40)
            p.poly(lens_pts((26.4, 9), (25.6, 20), 3.0, bend=0.8), c_hair, group=41)
            p.poly(lens_pts((37.6, 9), (38.4, 20), 3.0, bend=-0.8), c_hair, group=42)
            p.limb([(26.6, 10.2), (32, 8.4), (37.4, 10.2)], 1.2, 1.2, c_crys, group=44)
            if p.big:
                p.patch(27, 12, ["111..111", "i9i..i9i", "i1i..i1i", "eie..eie"],
                        {"1": "ink", "i": "iris", "9": "white", "e": "glow"})
            else:
                p.pxs([(28.5, 14), (35, 14)], "ink")
        else:
            p.blob(32, 12.4, 7.0, 7.4, c_hair, group=40)
            _lock(p, bez3((32, 14), (30.6, 22), (33.4, 30), (31, 40)), 7.4, c_hair, group=41, start=0.9)
        _star(p, 32, 4.6, 3.4, c_crys, group=45)
        p.circle(32, 4.6, 1.0, c_gold, group=46)
        return


MONS = [
    # icon palette 4 keeps the Aegean-blue core
    Mon("Niflake", NIFLAKE_COLORS, NIFLAKE_SHINY, niflake, foot="blank", icon_pal=4),
    # icon palette 4 keeps her hair blue and her gown white
    Mon("Chionyad", CHIONYAD_COLORS, CHIONYAD_SHINY, chionyad, foot="blank", icon_pal=4),
]
