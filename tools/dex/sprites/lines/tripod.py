"""Tripod line: Pyrapod, Mantipod (Fire, then Fire/Psychic). The bronze
tripod of the Delphic oracle, where the Pythia sat over the vapors."""
import math

from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts, lerp

INK = C.ink


def _ring(p, cx, cy, rx, ry, w, mat, ang=0.0, **kw):
    """An upright ring handle: a band of width w around an ellipse."""
    pts = ellipse_pts(cx, cy, rx, ry, ang, n=28)
    return p.limb(pts + pts[:2], w, w, mat, cap=False, **kw)


# --------------------------------------------------------------------------
# Pyrapod, the walking brazier
# --------------------------------------------------------------------------

PYRAPOD_COLORS = [
    ("ink", INK),
    # sun-gold and terracotta bronze
    ("br0", (88, 48, 24)), ("br1", (160, 96, 40)), ("br2", (216, 152, 64)), ("br3", (248, 208, 112)),
    # the fire: an ember rim, orange, sun-gold and a white-hot heart
    ("fl0", (168, 48, 24)), ("fl1", (224, 104, 32)), ("fl2", (248, 160, 48)), ("fl3", (248, 216, 96)),
    ("fl4", (248, 248, 200)),
]
PYRAPOD_SHINY = {
    # silver-gray iron, Aegean-blue flames
    "br0": (56, 56, 72), "br1": (104, 104, 120), "br2": (152, 152, 168), "br3": (200, 200, 208),
    "fl0": (24, 48, 112), "fl1": (48, 104, 184), "fl2": (96, 160, 224), "fl3": (168, 208, 240),
    "fl4": (232, 248, 248),
}

p_bronze = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.16, 0.4, 0.64])
p_leg = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.2, 0.44, 0.7])
p_fire = Mat(["fl0", "fl1", "fl2", "fl3", "fl4"], line="fl0", outline="fl0")


def _pflame(p, a, b, w, bend=0.0, tiers=3, **kw):
    """A flame tongue from base a to tip b: orange, with a sun-gold heart and
    a pale core near the base, rimmed in ember red."""
    pid = p.lens(a, b, w, p_fire, bend=bend, fat=0.3, flat=1, **kw)
    kw.pop("group", None)
    if tiers >= 2:
        p.lens(a, lerp(a, b, 0.66), w * 0.62, p_fire, bend=bend * 0.6, fat=0.3, flat=2,
               noline=True, nooutline=True, clip=[pid], **kw)
    if tiers >= 3 and p.big:
        p.lens(a, lerp(a, b, 0.36), w * 0.34, p_fire, bend=bend * 0.3, fat=0.3, flat=3,
               noline=True, nooutline=True, clip=[pid], **kw)
    return pid


def _paw(p, x, y, far=False):
    """A round lion paw, toes forward (left), resting on row y; x is its left end."""
    b = 0.3 if far else 0.0
    p.blob(x + 3.2, y - 1.3, 3.4, 2.2, p_leg, bias=b)
    if p.big:
        p.px(x + 1.5, y - 0.5, "br0")
        p.px(x + 3.5, y - 0.5, "br0")


def _pfire_head(p, cx, cy, E=0, small=False, m=1, k=1.0, up=False):
    """Pyrapod's fire: a round head of flame whose tongues lick up and back
    like a crest of hair, with a white-hot face glow in front. m=1 faces
    left, m=-1 faces right; k scales it; up=True is the symmetric view."""
    t = 0 if small else 1
    X = lambda dx: cx + m * dx * k
    Y = lambda dy: cy + dy * k
    if up:
        for a, b, w, bend in (((-7, 2), (-12, -9 - E), 6.4, -1.2), ((7, 2), (12, -9 - E), 6.4, 1.2),
                              ((-3, 0), (-5, -15 - 2 * E), 8.4, -0.8), ((3, 0), (5, -15 - 2 * E), 8.4, 0.8),
                              ((0, -1), (0, -19 - 2 * E), 10, 0.0)):
            _pflame(p, (X(a[0]), Y(a[1])), (X(b[0]), Y(b[1])), w * k, bend=bend, group=30)
    else:
        _pflame(p, (X(9), Y(5)), (X(19), Y(-4.5) - E), 6.0 * k, bend=1.4 * m, group=31)
        _pflame(p, (X(5), Y(1)), (X(15), Y(-13) - 2 * E), 8.0 * k, bend=1.8 * m, group=32)
        _pflame(p, (X(-1), Y(0)), (X(5), Y(-18) - 2 * E), 10 * k, bend=2.0 * m, group=34)
        _pflame(p, (X(-6), Y(0)), (X(-6.5), Y(-11) - E), 6.6 * k, bend=-0.4 * m, group=30)
    head = p.blob(cx, Y(0.5), 10.6 * k, 8.6 * k, p_fire, flat=1, group=35)
    g = 0 if up else 1
    p.blob(X(-1.2 * g), Y(1.8), 9.0 * k, 7.0 * k, p_fire, flat=2, noline=True, clip=[head], group=35)
    p.blob(X(-2.2 * g), Y(2.6), (7.4 * t + 4) * k, (5.6 * t + 2) * k, p_fire, flat=3, noline=True, clip=[head], group=35)
    return head


def pyrapod(p, view, phase):
    if view in ("front", "side", "icon"):
        walk = view == "side"
        F = phase == 1 and view == "front"      # frame 2: the fire leaps, ears perk
        E = 1 if F else 0

        # ---- far leg, behind the bowl
        far = [(35, 50), (38, 54), (37 if not (walk and phase) else 36, 57.5)]
        p.limb(bez(far[0], (38.5, 51), far[1]) + [far[2]], 4.8, 3.6, p_leg, bias=0.34, group=10)
        _paw(p, far[-1][0] - 3.5, 59.5, far=True)

        # ---- far ring handle: an ear standing out behind the fire
        _ring(p, 46.5, 34.5 - E, 3.0, 3.9, 2.4, p_bronze, ang=28 + 6 * E, bias=0.14, group=20)

        # ---- the fire head
        _pfire_head(p, 32, 30, E, small=not p.big)

        # ---- the bowl: a round-bellied cauldron
        body = bez3((22.5, 39.5), (17.5, 42), (18.5, 52.5), (33, 52.5)) + \
            bez3((33, 52.5), (47.5, 52.5), (48.5, 42), (43.5, 39.5))[1:]
        bowl = p.poly(body, p_bronze, group=1)
        # a band around the belly for the black-figure frieze
        p.poly([(16, 43.5), (50, 43.5), (50, 46.5), (16, 46.5)], p_bronze, clip=[bowl], flat=1,
               noline=True, group=1)
        # the rolled lip, seen a little from above
        p.blob(33, 39.6, 11.6, 2.2, p_bronze, group=2, bias=-0.2)

        # ---- near ring handle (the near "ear")
        _ring(p, 19.5, 34.5 - E, 3.0, 3.9, 2.4, p_bronze, ang=-28 - 6 * E, group=21)

        # ---- near legs: stubby bowed lion legs, the front one stepping
        if walk and phase:
            nl = [(26, 50), (20.5, 54), (21, 57.5)]
            nr = [(41, 50), (45.5, 54), (44.5, 57.5)]
        elif walk:
            nl = [(26, 50), (20, 53.5), (18.5, 56)]
            nr = [(41, 50), (46.5, 54), (46.5, 57.5)]
        else:
            nl = [(26, 50), (21, 52.5), (20, 54.8)]
            nr = [(41, 50), (46.5, 54), (46, 57.5)]
        p.limb(bez(nl[0], (21, 50), nl[1]) + [nl[2]], 5.6, 3.8, p_leg, group=12)
        p.limb(bez(nr[0], (47, 50.5), nr[1]) + [nr[2]], 5.6, 3.8, p_leg, group=13)
        _paw(p, nl[2][0] - 4, nl[2][1] + 2.2)
        _paw(p, nr[2][0] - 3.5, 59.5)

        # ---- face
        if p.big:
            p.eye(24, 29 - E, 3, 5, shine="fl4", shine_at=(1, 1))
            p.eye(30, 29 - E, 3, 5, shine="fl4", shine_at=(1, 1))
            p.pxs([(27, 36 - E), (28, 36 - E)], "fl0")      # little mouth
        else:
            p.px(25, 32, "ink")
            p.px(31, 32, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the bowl's back cropped by the
        # frame, the fire turned right in profile, the ring-ears out wide
        _ring(p, 51.5, 34, 3.6, 4.6, 2.8, p_bronze, ang=26, bias=0.14, group=20)
        _pfire_head(p, 33, 31.5, m=-1, k=1.2)
        body = bez3((14, 43), (8, 47), (8, 64), (20, 66)) + [(46, 66)] + bez3((46, 66), (58, 64), (58, 47), (52, 43))[1:]
        bowl = p.poly(body, p_bronze, group=1)
        p.poly([(0, 50), (64, 50), (64, 54), (0, 54)], p_bronze, clip=[bowl], flat=1, noline=True, group=1)
        p.blob(33, 43, 19.5, 2.8, p_bronze, group=2, bias=-0.2)
        _ring(p, 12.5, 35, 3.6, 4.6, 2.8, p_bronze, ang=-26, group=21)
        if p.big:
            p.eye(40, 28, 3, 5, shine="fl4", shine_at=(1, 1))
            p.pxs([(45, 36), (46, 36)], "fl0")
        return

    if view in ("down", "up"):
        # follower: a three-legged toddle; the near legs swap, the back one
        # shows between them
        st = phase
        far_x = 32
        p.limb([(far_x, 50), (far_x, 57)], 4.4, 3.4, p_leg, bias=0.35, group=10)
        p.blob(far_x, 57.6, 3.0, 1.8, p_leg, bias=0.35, group=10)
        _ring(p, 46.5, 35, 3.0, 3.9, 2.4, p_bronze, ang=24, group=20, bias=0.1)
        _ring(p, 17.5, 35, 3.0, 3.9, 2.4, p_bronze, ang=-24, group=21, bias=0.1)
        _pfire_head(p, 32, 31, E=st, up=True, small=not p.big)
        body = bez3((22, 40), (17, 42), (18, 52.5), (32, 52.5)) + bez3((32, 52.5), (46, 52.5), (47, 42), (42, 40))[1:]
        bowl = p.poly(body, p_bronze, group=1)
        p.poly([(10, 43.5), (54, 43.5), (54, 46.5), (10, 46.5)], p_bronze, clip=[bowl], flat=1, noline=True, group=1)
        p.blob(32, 40, 10.8, 2.2, p_bronze, group=2, bias=-0.2)
        for sx, lift in ((-1, st), (1, 1 - st)):
            x0 = 32 + sx * 7
            p.limb(bez((x0, 50), (x0 + sx * 4, 52), (x0 + sx * 4.5, 56 - lift * 1.5)), 5.0, 3.6, p_leg,
                   group=12 if sx < 0 else 13)
            p.blob(x0 + sx * 4.5, 58 - lift * 1.5, 3.0, 2.0, p_leg, group=12 if sx < 0 else 13)
        if view == "down":
            p.eye(27, 29 + st * 0, 2, 4, shine="fl4", shine_at=(0, 0))
            p.eye(35, 29, 2, 4, shine="fl4", shine_at=(1, 0))
            if p.big:
                p.pxs([(31, 35), (32, 35)], "fl0")
        return


# --------------------------------------------------------------------------
# Mantipod, the oracle tripod
# --------------------------------------------------------------------------

MANTIPOD_COLORS = [
    ("ink", INK),
    # sun-gold and terracotta bronze
    ("br0", (88, 48, 24)), ("br1", (160, 96, 40)), ("br2", (216, 152, 64)), ("br3", (248, 208, 112)),
    # white-hot light: flame hearts, the glowing eyes, the crack in the earth
    ("glint", (248, 240, 176)),
    ("fl1", (216, 80, 24)), ("fl2", (248, 152, 40)),
    # the hollow under the veil
    ("veil", (48, 40, 72)),
    # laurel smoke, marble-white
    ("sm0", (112, 104, 128)), ("sm1", (168, 160, 176)), ("sm2", (216, 208, 208)), ("white", (248, 248, 240)),
    # the laurel wreath
    ("leaf0", (56, 80, 32)), ("leaf1", (136, 160, 64)),
]
MANTIPOD_SHINY = {
    # silver iron, Aegean-blue flames, pale blue smoke
    "br0": (48, 48, 64), "br1": (96, 96, 112), "br2": (152, 152, 168), "br3": (208, 208, 216),
    "glint": (224, 240, 248), "fl1": (40, 88, 176), "fl2": (96, 160, 232), "veil": (24, 32, 72),
    "sm0": (88, 104, 152), "sm1": (136, 160, 200), "sm2": (184, 208, 232), "white": (232, 248, 248),
}

m_bronze = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.16, 0.4, 0.64])
m_leg = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.2, 0.44, 0.7])
m_fire = Mat(["br0", "fl1", "fl2", "br3", "glint"], line="br0", outline="br0")
m_smoke = Mat(["sm0", "sm1", "sm2", "white"], line="sm1", cuts=[0.2, 0.46, 0.72])
m_wisp = Mat(["sm0", "sm1", "sm2", "white"], line="sm0", outline="sm0", cuts=[0.2, 0.46, 0.72])
m_veil = Mat(["veil", "sm0"], line="veil", cuts=[0.7])
m_leaf = Mat(["leaf0", "leaf1"], line="leaf0", cuts=[0.5])
m_light = Mat(["fl2", "br3", "glint"], line="fl2", outline="br0")


def _mflame(p, a, b, w, bend=0.0, **kw):
    pid = p.lens(a, b, w, m_fire, bend=bend, fat=0.3, flat=1, **kw)
    kw.pop("group", None)
    p.lens(a, lerp(a, b, 0.66), w * 0.62, m_fire, bend=bend * 0.6, fat=0.3, flat=2,
           noline=True, nooutline=True, clip=[pid], **kw)
    if p.big:
        p.lens(a, lerp(a, b, 0.36), w * 0.36, m_fire, bend=bend * 0.3, fat=0.3, flat=3,
               noline=True, nooutline=True, clip=[pid], **kw)
    return pid


def _mpaw(p, x, y, far=False):
    """A big lion paw, toes forward (left), on row y; x is its left end."""
    b = 0.3 if far else 0.0
    p.blob(x + 3.6, y - 1.5, 4.0, 2.5, m_leg, bias=b)
    if p.big:
        for i in (1.5, 3.5):
            p.px(x + i, y - 0.5, "br0")


def _mleg(p, top, knee, ankle, foot, w0=7.0, far=False, group=None, out=1):
    """A long lion leg: a muscled haunch under the bowl, a bowed shin, a fur
    tuft at the back of the ankle and a paw."""
    b = 0.32 if far else 0.0
    p.blob(top[0] + out * 0.5, top[1] + 1.5, w0 * 0.55, w0 * 0.7, m_leg, bias=b, group=group)
    p.limb(bez(top, knee, ankle) + [foot], w0 * 0.8, 3.4, m_leg, bias=b, group=group)
    # the tuft at the back of the ankle
    p.lens((ankle[0] + out * 0.6, ankle[1] - 1.5), (ankle[0] + out * 3.8, ankle[1] + 2.2), 2.4, m_leg,
           bias=b + 0.15, group=group)


def _wreath(p, cx, cy, rx, ry, n=4, lean=0.0):
    """A laurel wreath around the bowl: two sprays of pointed leaves meeting
    at a knot in front."""
    for side in (-1, 1):
        for i in range(n):
            t = (i + 0.45) / n
            ang = math.pi / 2 + side * t * math.pi / 2 * 1.12
            x, y = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
            ang2 = ang - side * 0.5
            up = -1.3 if i % 2 else 1.2
            tx, ty = cx + rx * math.cos(ang2), cy + ry * math.sin(ang2) + up
            back = abs(math.cos(ang)) > 0.9
            p.lens((x, y), (tx, ty), 3.0 if p.big else 2.6, m_leaf, bend=0.6 * side * (1 if up < 0 else -1),
                   bias=0.3 if back else -0.1)


def _mhead(p, S=0, T=None, face=True):
    """The veiled head of laurel smoke, bowed forward over the bowl: a cowl
    rising from a neck of smoke, its veil streaming back in curls, and a dark
    hollow where the face should be. T maps front-view design coordinates
    (the neck's base at (32, 27.5)) to the canvas, for the back view."""
    T = T or (lambda x, y: (x, y))
    k = abs(T(1, 0)[0] - T(0, 0)[0])
    # the veil streaming back behind the head, curling at the ends
    p.lens(T(39, 13 - S), T(56.5, 19.5 - S), 6.0 * k, m_wisp, bend=-3.0 * (T(1, 0)[0] - T(0, 0)[0]),
           bias=0.16, group=60)
    p.lens(T(38, 6 - S), T(55.5, 3.5 - 2 * S), 4.8 * k, m_wisp, bend=2.6 * (T(1, 0)[0] - T(0, 0)[0]),
           bias=0.1, group=61)
    p.circle(*T(56.5, 16.5 - S), 2.2 * k, m_wisp, bias=0.14, group=62)
    p.circle(*T(55.5, 2.6 - 2 * S), 1.7 * k, m_wisp, bias=0.12, group=63)
    # the cowl: puffs of smoke billowing round a hood, the column below
    puffs = [(24.5, 5.5, 4.2), (30.5, 4.2, 4.4), (36.5, 5.8, 4.0), (40.5, 10, 3.6), (18.8, 8.5, 3.8), (16.4, 13.5, 3.4),
             (17.4, 18.6, 3.2), (21.4, 21.6, 3.0), (42, 15, 3.4), (40.6, 20.4, 3.2), (37.4, 24, 3.0), (26.4, 25, 2.8),
             (31.5, 26, 3.4), (35.6, 25.6, 2.8)]
    polys = [ellipse_pts(*T(x, y - S), r * k, r * k, n=20) for x, y, r in puffs]
    polys += [ellipse_pts(*T(29.5, 14 - S), 10.5 * k, 9.5 * k, n=36), ellipse_pts(*T(31, 21 - S), 7 * k, 5 * k, n=28)]
    hid = p.add(p.mask(*polys), m_smoke, group=51)
    # the hollow, rimmed by the veil's lit front edge
    if face:
        c = T(23.2, 13 - S)
        p.blob(c[0], c[1], 5.4 * k, 7.0 * k, m_veil, ang=12 * (T(1, 0)[0] - T(0, 0)[0]) / k, clip=[hid],
               flat=0, group=53)
    return hid


def mantipod(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase == 1 and view == "front"     # frame 2: it speaks, the veil leans in
        S = 1 if F else 0

        # ---- the crack of light in the earth beneath it
        if p.big:
            crack = [(13, 61), (17, 60), (21, 60.8), (25, 59.6), (29, 60.6), (34, 59.6), (39, 60.6),
                     (43, 59.6), (47, 60.4), (51, 61), (47, 61.8), (43, 61.2), (39, 62), (34, 61.4),
                     (29, 62), (25, 61.4), (21, 62), (17, 61.6)]
            p.poly(crack, m_light, flat=1)
            p.poly([(18, 61), (25, 60.4), (34, 60.6), (43, 60.4), (48, 61), (43, 61), (34, 61.2), (25, 61)],
                   m_light, flat=2, noline=True, nooutline=True)

        # ---- far leg
        _mleg(p, (33, 39), (37, 47), (35, 54), (34.5, 56.5), w0=6, far=True, group=10, out=1)
        _mpaw(p, 30, 59.5, far=True)

        # ---- far ring handle
        _ring(p, 47.5, 23 - S, 3.4, 4.4, 2.6, m_bronze, ang=28, bias=0.14, group=20)

        # ---- fire licking up behind the smoke
        _mflame(p, (39.5, 26), (45, 13 - S), 6.4, bend=1.4, group=33)

        # ---- the veiled head of smoke
        _mhead(p, S)

        # ---- fire in front, at the rim
        _mflame(p, (30, 26.8), (29, 21 - S), 4.4, bend=-0.6, group=34)
        _mflame(p, (36, 26.8), (39, 19.5 - S), 5.6, bend=0.8, group=35)

        # ---- near legs, planted wide, their haunches under the bowl
        _mleg(p, (24, 38), (14.5, 46), (16, 54), (15.5, 56.5), w0=7.6, group=12, out=1)
        _mleg(p, (40, 38), (49.5, 46), (48, 54), (48.5, 56.5), w0=7.6, group=13, out=-1)
        _mpaw(p, 10.5, 59.5)
        _mpaw(p, 44, 59.5)

        # ---- the bowl: deep and round-bottomed, a black-figure frieze round it
        body = bez3((21, 26.5), (18, 32), (22, 41), (32, 41)) + bez3((32, 41), (42, 41), (46, 32), (43, 26.5))[1:]
        bowl = p.poly(body, m_bronze, group=1)
        p.poly([(10, 32), (54, 32), (54, 35.5), (10, 35.5)], m_bronze, clip=[bowl], flat=1, noline=True, group=1)
        p.blob(32, 26.4, 11.6, 2.2, m_bronze, group=2, bias=-0.2)
        _wreath(p, 32, 28.8, 11.8, 2.2)

        # ---- near ring handle
        _ring(p, 16.5, 23 - S, 3.4, 4.4, 2.6, m_bronze, ang=-28, group=21)

        # ---- the word half spoken: a tongue of flame hanging from the veil
        _mflame(p, (23.5, 17.5 - S), (21 - S, 31 + 2 * S), 4.6 + 0.6 * S, bend=2.0, group=70)

        if p.big:
            p.patch(20, 11 - S, [".b..b.", "ggbggb", "gg.gg."], {"g": "glint", "b": "br3"})
        else:
            p.px(21, 12, "glint")
            p.px(24.5, 12, "glint")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the bowl from behind, cropped by
        # the frame, the veil of smoke turned right in profile and its smoke
        # pouring up to the top of the frame
        T = lambda x, y: (32 - 1.2 * (x - 32) + 1, 37.5 + 1.2 * (y - 27.5))
        # smoke rising off the back of the veil toward the sky
        for a, b, w, bend in (((26, 10), (17, 1.2), 6.4, 1.6), ((22, 16), (8, 4), 6.0, -2.0),
                              ((31, 6), (30, 1.2), 5.0, -1.2)):
            p.lens(a, b, w, m_wisp, bend=bend, bias=0.12)
        p.circle(9, 3.2, 2.2, m_wisp, bias=0.14)
        _ring(p, 55.5, 30, 4.2, 5.4, 3.0, m_bronze, ang=18, bias=0.14, group=20)
        _mflame(p, (19, 36), (12.5, 22), 7, bend=-1.4, group=32)
        _mflame(p, (44, 36), (51, 23.5), 6, bend=1.2, group=33)
        _mhead(p, 0, T)
        _mflame(p, (26, 37), (22.5, 27), 6, bend=-1.0, group=34)
        body = bez3((13, 37), (8, 44), (9, 64), (20, 66)) + [(44, 66)] + bez3((44, 66), (55, 64), (56, 44), (51, 37))[1:]
        bowl = p.poly(body, m_bronze, group=1)
        p.poly([(0, 47), (64, 47), (64, 51.5), (0, 51.5)], m_bronze, clip=[bowl], flat=1, noline=True, group=1)
        p.blob(32, 37, 19.6, 3.0, m_bronze, group=2, bias=-0.2)
        _wreath(p, 32, 40.5, 19.8, 3.0, n=5)
        _ring(p, 8.5, 30, 4.2, 5.4, 3.0, m_bronze, ang=-18, group=21)
        # the word half spoken, hanging from the veil
        _mflame(p, T(22, 17), T(20.5, 30.5), 5.0, bend=-2.0, group=70)
        if p.big:
            ex, ey = T(20, 11)
            p.patch(int(ex) - 1, int(ey), [".b.", "gg.", "gg."], {"g": "glint", "b": "br3"})
        return

    if view in ("down", "up"):
        # follower: stalking toward or away from the camera on its three legs
        st = phase
        down = view == "down"
        # far leg, in the middle
        p.limb([(32, 40), (32, 55)], 5, 3.6, m_leg, bias=0.35, group=10)
        p.blob(32, 56.5, 3.4, 2.0, m_leg, bias=0.35, group=10)
        _ring(p, 47, 21, 3.6, 4.6, 2.5, m_bronze, ang=16, group=20, bias=0.1)
        _ring(p, 17, 21, 3.6, 4.6, 2.5, m_bronze, ang=-16, group=21, bias=0.1)
        _mflame(p, (24, 26), (19, 16 - st), 5.4, bend=-1.0, group=32)
        _mflame(p, (40, 26), (45, 16 - (1 - st)), 5.4, bend=1.0, group=33)
        # the veil, seen head-on
        p.limb([(32, 27), (32, 18)], 10, 10, m_smoke, group=50)
        hood = p.blob(32, 11, 10.5, 9.5, m_smoke, group=51)
        p.lens((24, 12), (19.5, 26), 5, m_smoke, bend=-1, group=52, bias=0.1)
        p.lens((40, 12), (44.5, 26), 5, m_smoke, bend=1, group=52, bias=0.1)
        if down:
            p.blob(32, 12.5, 5.6, 6.6, m_veil, clip=[hood], flat=0, group=53)
        else:
            p.lens((32, 3), (32, 24), 4, m_smoke, group=54, bias=-0.1)
        body = bez3((20, 26.5), (17.5, 32), (21, 41), (32, 41)) + bez3((32, 41), (43, 41), (46.5, 32), (44, 26.5))[1:]
        bowl = p.poly(body, m_bronze, group=1)
        p.poly([(10, 33), (54, 33), (54, 36.5), (10, 36.5)], m_bronze, clip=[bowl], flat=1, noline=True, group=1)
        p.blob(32, 26.4, 12.6, 2.4, m_bronze, group=2, bias=-0.2)
        _wreath(p, 32, 29, 12.8, 2.4, n=4)
        for sx, lift in ((-1, st), (1, 1 - st)):
            x0 = 32 + sx * 8
            p.limb(bez((x0, 37), (x0 + sx * 7, 46), (x0 + sx * 6, 55 - lift * 2)), 6.4, 3.8, m_leg,
                   group=12 if sx < 0 else 13)
            p.blob(x0 + sx * 6, 57 - lift * 2, 3.6, 2.2, m_leg, group=12 if sx < 0 else 13)
        if down:
            _mflame(p, (32, 16), (31.5, 29 + st), 4.4, bend=1.2, group=70)
            if p.big:
                p.patch(28, 10, ["gg..gg", "gg..gg"], {"g": "glint"})
            else:
                p.px(29.5, 10.5, "glint")
                p.px(34.5, 10.5, "glint")
        return


MONS = [
    Mon("Pyrapod", PYRAPOD_COLORS, PYRAPOD_SHINY, pyrapod, foot="paw"),
    Mon("Mantipod", MANTIPOD_COLORS, MANTIPOD_SHINY, mantipod, foot="paw"),
]
