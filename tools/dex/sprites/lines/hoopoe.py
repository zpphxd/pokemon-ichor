"""Hoopoe line: Epopoi, Lophops, Basilops (Normal/Flying route bird).
Tereus the hoopoe, and the bird-king of Aristophanes's Birds."""
import math

from mon_lib import C, Mat, Mon, bez

INK = C.ink


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------

def _band(p, a, b, t0, t1, mat, clip, skew=0.0, reach=30, **kw):
    """A stripe across the a->b axis between t0 and t1 (0..1 along it),
    clipped to the `clip` parts. skew slants the stripe."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    nx, ny = -uy, ux
    q = []
    for t, sgn in ((t0, 1), (t1, 1), (t1, -1), (t0, -1)):
        cx, cy = a[0] + dx * t, a[1] + dy * t
        q.append((cx + sgn * (nx * reach + ux * skew * reach), cy + sgn * (ny * reach + uy * skew * reach)))
    return p.poly(q, mat, clip=clip, **kw)


def _barred(p, a, b, w, bands, light, dark, bend=0.0, fat=0.5, skew=0.0, group=None, **kw):
    """A hoopoe wing or tail: a lens from a to b, white, crossed by black bars.
    bands: (t0, t1) spans along the axis that are black."""
    pid = p.lens(a, b, w, light, bend=bend, fat=fat, group=group, **kw)
    g = group if group is not None else pid
    kw.pop("bias", None)
    for t0, t1 in bands:
        _band(p, a, b, t0, t1, dark, [pid], skew=skew, group=g, **kw)
    return pid


def _crest_feather(p, a, b, w, body, white, tip, band=True, **kw):
    """One crest feather: body color, a white band under a black tip."""
    pid = p.lens(a, b, w, body, fat=0.62, **kw)
    kw.pop("bias", None)
    g = kw.pop("group", pid)
    if band:
        _band(p, a, b, 0.6, 0.76, white, [pid], group=g, noline=True)
    _band(p, a, b, 0.76, 1.01, tip, [pid], group=g, noline=True)
    return pid


def _fan(cx, cy, r0, lengths, angles):
    """Feather (base, tip) pairs radiating from (cx, cy); angle 90 is up."""
    out = []
    for L, ang in zip(lengths, angles):
        ca, sa = math.cos(math.radians(ang)), -math.sin(math.radians(ang))
        out.append(((cx + ca * r0, cy + sa * r0), (cx + ca * L, cy + sa * L)))
    return out


def _toes(p, x, y, color="bk0", left=True):
    """Bird toes: three short forward toes on row y from x."""
    if not p.big:
        return
    if left:
        p.pxs([(x - 1, y), (x, y), (x + 1, y), (x + 2, y)], color)
    else:
        p.pxs([(x - 2, y), (x - 1, y), (x, y), (x + 1, y)], color)


# --------------------------------------------------------------------------
# Epopoi, the hoopoe chick
# --------------------------------------------------------------------------

EPOPOI_COLORS = [
    ("ink", INK),
    ("tc0", (152, 72, 48)), ("tc1", (208, 120, 80)), ("tc2", (232, 160, 112)), ("tc3", (248, 200, 152)),
    ("lm0", (208, 184, 136)), ("lm1", (240, 224, 184)),
    ("white", C.white), ("mshade", (184, 176, 168)),
    ("bar0", (64, 56, 64)), ("bar1", (112, 104, 112)),
    ("bk0", (88, 72, 72)), ("bk1", (160, 136, 128)),
    ("mouth", (216, 96, 88)),
]
EPOPOI_SHINY = {
    "tc0": (168, 104, 24), "tc1": (216, 152, 40), "tc2": (240, 192, 64), "tc3": (248, 224, 136),
    "bar0": (24, 64, 136), "bar1": (64, 120, 200),
}

e_tc = Mat(["tc0", "tc1", "tc2", "tc3"], line="tc0", cuts=[0.16, 0.42, 0.7])
e_belly = Mat(["lm0", "lm1"], line="tc1", cuts=[0.55])
e_white = Mat(["mshade", "white"], line="mshade", cuts=[0.62])
e_bar = Mat(["bar0", "bar1"], line="bar0", cuts=[0.66])
e_beak = Mat(["bk0", "bk1"], line="bk0", cuts=[0.52])


def epopoi(p, view, phase):
    """The battle sprites are hand-finished (art/epopoi_*.txt); this draft
    matches them for the icon and the follower."""
    if view in ("front", "side", "icon"):
        call = phase == 1 and view != "side"
        H = 1 if (view == "side" and phase == 1) else 0    # the walk hops
        C_ = 1 if call else 0                               # the crest pops up when it calls
        # tail stub cocked up behind, black with a white band
        _barred(p, (41.5, 46 - H), (47.5, 40 - H), 3.8, [(0.0, 0.38), (0.7, 1.0)], e_white, e_bar, bias=0.1)
        # body, belly, and the big head in front
        body = p.blob(35.5, 50.5 - H, 9.6, 7.4, e_tc, group=1)
        p.blob(32, 55 - H, 8.6, 4.6, e_belly, clip=[body], group=2)
        p.blob(27.5, 41.5 - H, 8.6, 8.2, e_tc, group=3)
        # the tuft: three black-tipped feathers
        for (a, b), bias in zip(_fan(27.5, 34.5 - H, 1, [6.5 + C_, 7.5 + 2 * C_, 6.5 + C_],
                                     [122 + 10 * C_, 92, 62 - 10 * C_]), (0.15, 0.0, 0.1)):
            _crest_feather(p, a, b, 2.8, e_tc, e_white, e_bar, band=False, bias=bias)
        # stubby barred wing held out
        _barred(p, (38.5, 46.5 - H), (46, 52.5 - H), 5.6, [(0.0, 0.25), (0.5, 0.72), (0.88, 1.0)],
                e_white, e_bar, bend=-0.4)
        if not H:
            p.limb([(31, 56), (31, 59.5)], 1.8, 1.6, e_beak, group=20)
            p.limb([(37, 56), (37, 59.5)], 1.8, 1.6, e_beak, group=21)
        # the long beak, open when it calls
        if call:
            p.limb(bez((20, 42.5), (14.5, 42), (9.5, 44)), 2.8, 1.2, e_beak, group=30)
            p.limb(bez((20, 45), (15.5, 46.5), (11.5, 49)), 2.2, 1.0, e_beak, group=31)
        else:
            p.limb(bez((20, 43.5 - H), (14.5, 44 - H), (10, 48.5 - H)), 3.2, 1.2, e_beak, group=30)
        if p.big:
            p.eye(22, 38 - H, 4, 5, shine="white", shine_at=(1, 1))
        else:
            p.pxs([(23, 40 - H), (23, 39 - H)], "ink")
        return

    if view == "back":
        # the hand-finished art replaces this
        body = p.blob(27, 62, 21, 15, e_tc, group=1)
        p.blob(38, 39, 10.8, 10.4, e_tc, group=3)
        p.limb(bez((48, 41), (54, 41), (58, 46)), 3.4, 1.2, e_beak, group=30)
        _barred(p, (30, 51), (7, 63), 10, [(0.3, 0.45), (0.6, 0.75), (0.9, 1)], e_white, e_bar)
        p.eye(42, 35, 4, 5, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: a hopping ball of fluff; when it calls (phase 1) the tuft pops up
        step = phase
        p.limb([(28.5, 56), (28.5, 60 - step)], 2, 1.8, e_beak, group=20)
        p.limb([(35.5, 56), (35.5, 60 - (1 - step))], 2, 1.8, e_beak, group=21)
        if view == "up":
            _barred(p, (32, 52), (32, 59), 4.6, [(0.0, 0.4), (0.7, 1)], e_white, e_bar)
        body = p.blob(32, 50, 9.4, 8, e_tc, group=1)
        if view == "down":
            p.blob(32, 54, 6.4, 4, e_belly, clip=[body], group=2)
        # stubby wings out at the sides
        _barred(p, (24.5, 47), (20, 54 - step), 5, [(0.0, 0.25), (0.5, 0.72), (0.88, 1)], e_white, e_bar)
        _barred(p, (39.5, 47), (44, 54 - step), 5, [(0.0, 0.25), (0.5, 0.72), (0.88, 1)], e_white, e_bar)
        p.blob(32, 40, 8.2, 7.6, e_tc, group=3)
        C_ = step
        for (a, b) in _fan(32, 33, 1, [6.5 + C_, 7.5 + 2 * C_, 6.5 + C_], [124 + 10 * C_, 90, 56 - 10 * C_]):
            _crest_feather(p, a, b, 3.0, e_tc, e_white, e_bar, band=False)
        if view == "down":
            # the long beak points at us, hanging below the face
            p.limb(bez((32, 43), (32.5, 47), (31.5, 51)), 3.0, 1.4, e_beak, group=30)
            p.eye(27, 38, 2, 3, shine="white")
            p.eye(35, 38, 2, 3, shine="white")
        return


# --------------------------------------------------------------------------
# Lophops, the hoopoe of the play
# --------------------------------------------------------------------------

LOPHOPS_COLORS = [
    ("ink", INK),
    ("sl0", (136, 64, 40)), ("sl1", (192, 104, 64)), ("sl2", (224, 144, 96)), ("sl3", (240, 184, 136)),
    ("lm0", (208, 184, 136)), ("lm1", (240, 224, 184)),
    ("white", C.white), ("marble", (216, 208, 200)), ("mshade", (160, 152, 152)),
    ("bar0", (56, 48, 56)), ("bar1", (104, 96, 104)),
    ("bk0", (72, 64, 64)), ("bk1", (136, 120, 112)),
    ("mouth", (200, 80, 80)),
]
LOPHOPS_SHINY = {
    "sl0": (168, 104, 24), "sl1": (216, 152, 40), "sl2": (240, 192, 64), "sl3": (248, 224, 136),
    "bar0": (24, 64, 136), "bar1": (64, 120, 200),
}

l_sl = Mat(["sl0", "sl1", "sl2", "sl3"], line="sl0", cuts=[0.16, 0.42, 0.7])
l_belly = Mat(["lm0", "lm1"], line="sl1", cuts=[0.55])
l_white = Mat(["mshade", "marble", "white"], line="mshade", cuts=[0.4, 0.66])
l_bar = Mat(["bar0", "bar1"], line="bar0", cuts=[0.66])
l_beak = Mat(["bk0", "bk1"], line="bk0", cuts=[0.52])

L_CREST_ANG = [168, 148, 128, 108, 88, 68, 48, 28]
L_CREST_LEN = [9, 11, 12.5, 13, 13, 12.5, 11, 9]


def lophops(p, view, phase):
    """Battle sprites are hand-finished (art/lophops_*.txt); this draft
    matches them for the icon and the follower."""
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "side") else 0
        walk = view == "side" and phase == 1
        # tail, down and back
        _barred(p, (43, 49), (56, 56), 5.6, [(0.0, 0.45), (0.68, 1.0)], l_white, l_bar, bias=0.1)
        # far wing, half raised
        _barred(p, (37, 37), (51, 21 - L), 7.4, [(0.0, 0.2), (0.4, 0.58), (0.8, 1)], l_white, l_bar,
                bend=-1.2, bias=0.3)
        # legs
        if walk:
            p.limb([(33.5, 52), (32, 59.5)], 2.2, 2, l_beak, group=20)
            p.limb([(39.5, 52), (41, 59.5)], 2.2, 2, l_beak, group=21)
        else:
            p.limb([(33.5, 52), (33.5, 59.5)], 2.2, 2, l_beak, group=20)
            p.limb([(39.5, 52), (39.5, 59.5)], 2.2, 2, l_beak, group=21)
        # crest: rear feathers behind the head
        fan = _fan(29, 25 - L, 1, [v + L for v in (9.5, 11.5, 12.5, 13, 13.2, 13, 12.5, 11.5, 9.5)],
                   [166, 148, 130, 112, 94, 76, 58, 40, 22])
        for i in (8, 7, 6, 5):
            _crest_feather(p, fan[i][0], fan[i][1], 3.8, l_sl, l_white, l_bar, bias=0.12)
        # body, breast and limestone belly
        body = p.blob(37, 47, 10, 7.2, l_sl, ang=-18, group=1)
        p.blob(30.5, 43, 6.8, 6.6, l_sl, group=1)
        p.blob(36, 52, 8.6, 3.6, l_belly, ang=-10, clip=[body], group=2)
        p.limb([(31, 42), (27, 32 - L)], 7.6, 6.6, l_sl, group=1)
        p.blob(25.5, 30 - L, 6.8, 6.2, l_sl, group=3)
        for i in (4, 3, 2, 1, 0):
            _crest_feather(p, fan[i][0], fan[i][1], 3.8, l_sl, l_white, l_bar)
        # beak open mid-call
        p.limb(bez((20, 29.5 - L), (14, 29.5 - L), (8, 32.5 - L)), 2.8, 1.1, l_beak, group=30)
        p.limb(bez((20, 32 - L), (15, 34), (11, 37)), 2.2, 1.0, l_beak, group=31)
        # near wing, half raised: the bold bars on show
        _barred(p, (37, 41), (52, 23 - L), 7, [(0.0, 0.18)], l_white, l_bar, bias=0.0)
        _barred(p, (41, 40), (57, 44), 13, [(0.12, 0.3), (0.48, 0.66), (0.84, 1)], l_white, l_bar,
                bend=2.4, fat=0.4)
        if p.big:
            p.eye(22, 27 - L, 4, 4, shine="white")
        else:
            p.pxs([(23, 28 - L), (23, 29 - L)], "ink")
        return

    if view == "back":
        # the hand-finished art replaces this
        p.blob(36, 69, 18, 21, l_sl, group=1)
        p.blob(42.5, 31, 7.4, 7, l_sl, group=3)
        _barred(p, (31, 52), (6, 40), 16, [(0.15, 0.3), (0.45, 0.6), (0.8, 1)], l_white, l_bar)
        p.eye(44, 27, 4, 4, shine="white")
        return

    if view in ("down", "up"):
        # follower: a perching walk, crest fanned, the barred wings half open
        step = phase
        p.limb([(29.5, 53), (29, 60 - step)], 2.2, 2, l_beak, group=20)
        p.limb([(34.5, 53), (35, 60 - (1 - step))], 2.2, 2, l_beak, group=21)
        if view == "up":
            _barred(p, (32, 50), (32, 61), 6, [(0.0, 0.45), (0.7, 1)], l_white, l_bar)
        _barred(p, (26, 40), (14, 50 - step), 8, [(0.0, 0.2), (0.42, 0.6), (0.82, 1)], l_white, l_bar, bend=-1)
        _barred(p, (38, 40), (50, 50 - (1 - step)), 8, [(0.0, 0.2), (0.42, 0.6), (0.82, 1)], l_white, l_bar,
                bend=1)
        body = p.blob(32, 46, 8, 9, l_sl, group=1)
        if view == "down":
            p.blob(32, 51, 5.6, 4.2, l_belly, clip=[body], group=2)
        fan = _fan(32, 28, 1, [10, 12, 13, 12, 10], [160, 125, 90, 55, 20])
        if view == "up":
            p.blob(32, 32, 6.4, 6, l_sl, group=3)
        for a, b in fan:
            _crest_feather(p, a, b, 3.8, l_sl, l_white, l_bar)
        if view == "down":
            p.blob(32, 32, 6.4, 6, l_sl, group=3)
            p.limb(bez((32, 35), (32.5, 40), (31, 44)), 2.6, 1.1, l_beak, group=30)
            p.eye(28, 30, 2, 3, shine="white")
            p.eye(35, 30, 2, 3, shine="white")
        return


# --------------------------------------------------------------------------
# Basilops, king of the birds
# --------------------------------------------------------------------------

BASILOPS_COLORS = [
    ("ink", INK),
    ("sl0", (136, 64, 40)), ("sl1", (192, 104, 64)), ("sl2", (224, 144, 96)), ("sl3", (240, 184, 136)),
    ("g0", (160, 96, 24)), ("g1", (216, 152, 40)), ("g2", (248, 208, 88)), ("glint", (248, 240, 176)),
    ("white", C.white), ("marble", (208, 200, 192)), ("mshade", (152, 144, 144)),
    ("bar0", (56, 48, 56)), ("bar1", (104, 96, 104)),
    ("bk0", (72, 64, 64)),
]
BASILOPS_SHINY = {
    "sl0": (144, 136, 128), "sl1": (192, 184, 176), "sl2": (224, 216, 208), "sl3": (248, 240, 232),
    "g0": (32, 64, 136), "g1": (64, 120, 192), "g2": (136, 184, 232), "glint": (216, 240, 248),
}

b_sl = Mat(["sl0", "sl1", "sl2", "sl3"], line="sl0", cuts=[0.16, 0.42, 0.7])
b_gold = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.3, 0.62])
b_white = Mat(["mshade", "marble", "white"], line="mshade", cuts=[0.4, 0.66])
b_bar = Mat(["bar0", "bar1"], line="bar0", cuts=[0.66])
b_beak = Mat(["bk0", "mshade"], line="bk0", cuts=[0.52])
b_cloud = Mat(["mshade", "marble", "white"], line="mshade", cuts=[0.34, 0.62])

B_CROWN_ANG = [170, 154, 138, 122, 106, 90, 74, 58, 42, 26, 10]
B_CROWN_LEN = [11, 13, 14.5, 15.5, 16, 16.5, 16, 15.5, 14.5, 13, 11]


def _cloud(p, cx, cy, sc=1.0, lift=0):
    """The woven cloud nest."""
    for x, y, rx, ry in ((-13, 0.5, 6.4, 4.4), (-4.5, 1.6, 7.6, 4.2), (6, 1.2, 7.6, 4.4), (14, -1, 5.6, 4.0),
                         (-9, -3, 6.4, 3.6), (3, -3.4, 7.6, 3.6), (12.5, -3.6, 4.6, 3.0)):
        p.blob(cx + x * sc, cy + y * sc - lift, rx * sc, ry * sc, b_cloud, group=40)
    if p.big:
        for x0, y0, x1, y1 in ((-15, -1, -10, 1), (-7, 0, -1, 2.5), (2, 0, 8, 2.5), (10, -1, 15, -2.5),
                               (-11, -4, -6, -2), (0, -4.5, 6, -2.5)):
            p.stroke([(cx + x0 * sc, cy + y0 * sc - lift), (cx + x1 * sc, cy + y1 * sc - lift)], "marble")


def _mantle(p, shoulder, wrist, tips, w, bands, bias=0.0):
    """A wing mantled like a cloak: feathers hang from points along the
    leading edge (shoulder -> wrist), outermost first, barred across."""
    n = len(tips)
    for i, tip in enumerate(tips):
        t = 1 - i / max(n - 1, 1)
        a = (shoulder[0] + (wrist[0] - shoulder[0]) * t, shoulder[1] + (wrist[1] - shoulder[1]) * t)
        pid = p.lens(a, tip, w, b_white, fat=0.4, bias=bias + 0.04 * (n - i))
        for t0, t1 in bands:
            _band(p, a, tip, t0, t1, b_bar, [pid], group=pid)
    # the arm: a thick black leading edge with a white bar
    p.limb([shoulder, wrist], 5.4, 4.2, b_bar, bias=bias)


def basilops(p, view, phase):
    """Battle sprites are hand-finished (art/basilops_*.txt); this draft
    matches them for the icon and the follower."""
    BANDS = [(0.0, 0.18), (0.36, 0.52), (0.7, 0.84), (0.92, 1.01)]
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "side") else 0
        D = 1 if (view == "side" and phase == 1) else 0   # the cloud drifts between steps
        # far wing mantled low behind, near wing raised high and mantled over the nest
        _mantle(p, (27, 39 - D), (12, 36 - L - D), [(5, 45 - D), (8, 52 - D), (13, 57 - D)], 7.2, BANDS, bias=0.2)
        _mantle(p, (38, 34 - D), (56, 12 - L - D), [(61, 23 - D), (62, 33 - D), (60, 43 - D), (55, 51 - D), (47, 57 - D)],
                9.0, BANDS)
        fan = _fan(30, 19 - L - D, 1, [v + 0.4 * L for v in B_CROWN_LEN], B_CROWN_ANG)
        for i in (10, 9, 8, 7, 6):
            _crest_feather(p, fan[i][0], fan[i][1], 5.0, b_gold, b_white, b_bar, bias=0.08)
        body = p.blob(33.5, 43 - D, 11.4, 12, b_sl, group=1)
        p.blob(27.5, 37.5 - D, 9.2, 8.8, b_sl, group=1)
        p.limb([(31, 34 - D), (29, 25 - L - D)], 13, 11.4, b_sl, group=1)
        p.blob(27.5, 22.5 - L - D, 7.2, 6.6, b_sl, group=3)
        for i in (5, 4, 3, 2, 1, 0):
            _crest_feather(p, fan[i][0], fan[i][1], 5.0, b_gold, b_white, b_bar)
        p.limb(bez((21, 24 - L - D), (13, 24 - L - D), (5.5, 32 - L - D)), 3.6, 1.2, b_beak, group=30)
        _cloud(p, 32.5, 57, 1.15, D)
        if p.big:
            p.eye(22, 20 - L - D, 4, 4, iris="g1", shine="white", shine_at=(1, 0))
        else:
            p.pxs([(23, 21 - L - D), (24, 21 - L - D)], "ink")
        return

    if view == "back":
        # the hand-finished art replaces this
        p.blob(34, 66, 25, 22, b_sl, group=1)
        p.blob(42.5, 28, 8.4, 7.8, b_sl, group=3)
        _mantle(p, (33, 48), (9, 20), [(2, 30), (2, 40), (4, 49), (9, 56), (16, 61)], 9, BANDS)
        return

    if view in ("down", "up"):
        # follower: it rides its cloud, the mantle spread and the crown up;
        # the cloud drifts a pixel between steps
        D = phase
        if view == "up":
            _barred(p, (32, 40), (32, 54), 7, [(0.0, 0.3), (0.45, 0.62), (0.8, 1.0)], b_white, b_bar)
        _mantle(p, (27, 33 - D), (10, 20 - D), [(4, 32 - D), (5, 42 - D), (10, 50 - D), (18, 54 - D)], 8, BANDS)
        _mantle(p, (37, 33 - D), (54, 20 - D), [(60, 32 - D), (59, 42 - D), (54, 50 - D), (46, 54 - D)], 8, BANDS)
        p.blob(32, 38 - D, 9.6, 12.5, b_sl, group=1)
        if view == "up":
            p.blob(32, 21 - D, 7, 6.4, b_sl, group=3)
        fan = _fan(32, 17 - D, 1, [12, 14, 15.5, 16, 15.5, 14, 12], [170, 142, 116, 90, 64, 38, 10])
        for a, b in fan:
            _crest_feather(p, a, b, 5.0, b_gold, b_white, b_bar)
        if view == "down":
            p.blob(32, 21 - D, 7, 6.4, b_sl, group=3)
            p.limb(bez((32, 24 - D), (32.5, 30 - D), (31, 34 - D)), 3.2, 1.3, b_beak, group=30)
            p.eye(27, 19 - D, 3, 3, iris="g1", shine="white")
            p.eye(34, 19 - D, 3, 3, iris="g1", shine="white")
        _cloud(p, 32, 55, 1.0, D)
        return


MONS = [
    Mon("Epopoi", EPOPOI_COLORS, EPOPOI_SHINY, epopoi, foot="bird", icon_pal=3),
    Mon("Lophops", LOPHOPS_COLORS, LOPHOPS_SHINY, lophops, foot="bird", icon_pal=3),
    Mon("Basilops", BASILOPS_COLORS, BASILOPS_SHINY, basilops, foot="bird", icon_pal=3),
]
