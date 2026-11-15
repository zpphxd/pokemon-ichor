"""Icarus line: Ikaroth (Bug/Flying). Icarus on the wings Daedalus made of
feathers set in wax, climbing too near the sun."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Ikaroth, the wax-winged moth
# --------------------------------------------------------------------------

IKAROTH_COLORS = [
    ("ink", INK),
    # the wing's limestone underlayer, then marble feathers
    ("fth0", (128, 104, 80)), ("fth1", (184, 168, 136)), ("fth2", (232, 224, 200)), ("fth3", (248, 248, 240)),
    # sun-gold wax
    ("wax0", (176, 104, 32)), ("wax1", (232, 168, 48)), ("wax2", (248, 224, 120)),
    # terracotta drips where the wax runs
    ("drip0", (136, 48, 32)), ("drip1", (208, 96, 56)),
    # olive body stripes
    ("olv0", (80, 88, 40)), ("olv1", (136, 144, 64)),
    # the dusk-brown wing margin and body shadow
    ("body0", (88, 64, 56)),
    # the amber ruff of the thorax
    ("ruf0", (168, 88, 40)), ("ruf1", (224, 144, 72)),
]
IKAROTH_SHINY = {
    # the wax turns Aegean blue, like the sea it falls into
    "wax0": (24, 56, 120), "wax1": (48, 104, 176), "wax2": (128, 184, 232),
    "drip0": (24, 40, 96), "drip1": (72, 128, 200),
}

k_under = Mat(["body0", "fth0"], line="body0", cuts=[0.6])
k_panel = Mat(["fth1", "fth2", "fth3"], line="body0", cuts=[0.42, 0.78])
k_panel_far = Mat(["fth0", "fth1", "fth2"], line="body0", cuts=[0.36, 0.8])
k_wax = Mat(["wax0", "wax1", "wax2"], line="wax0", cuts=[0.38, 0.7])
k_drip = Mat(["drip0", "drip1"], line="drip0", cuts=[0.55])
k_body = Mat(["body0", "fth0", "fth1", "fth2"], line="body0", cuts=[0.22, 0.48, 0.76])
k_ruff = Mat(["body0", "ruf0", "ruf1", "wax2"], line="body0", cuts=[0.2, 0.5, 0.84])
k_head = Mat(["body0", "fth0", "fth1", "fth2"], line="body0", cuts=[0.24, 0.5, 0.8])
k_leg = Mat(["olv0", "body0"], cuts=[0.5])


def _centroid(pts):
    return (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts))


def _inset(pts, d, scallop=None):
    """Pull a wing outline toward its middle by d design px, to leave the
    dark margin band; scallop=(i0, i1) frills the points between those
    indices like the tips of a row of feathers."""
    cx, cy = _centroid(pts)
    out = []
    for i, (x, y) in enumerate(pts):
        dx, dy = cx - x, cy - y
        n = math.hypot(dx, dy) or 1.0
        k = d
        if scallop and scallop[0] <= i <= scallop[1]:
            k = d + (1.3 if i % 2 else -0.5)
        out.append((x + dx / n * k, y + dy / n * k))
    return out


def _drip(p, x, y, ln, r=1.5, bias=0.0):
    """A run of melting wax from (x, y), ln long, its bead at the bottom
    gone terracotta with the heat."""
    p.limb([(x, y), (x, y + ln)], r * 1.3, r * 1.7, k_wax, bias=bias)
    p.blob(x, y + ln + r * 0.6, r * 1.05, r * 0.95, k_drip, bias=bias)


def _moth_wing(p, outline, veins, frame, rows=(), far=False, g=40, margin=3.0, scallop=None):
    """A moth's wing made the way Daedalus made his: a dusk-brown underlayer
    with a dark margin band, a panel of marble feathers laid in rows (the
    rows are texture inside the panel, not loose blades), and the wax: a
    gold frame along the leading edge and wax veins holding the panel."""
    wing = p.poly(outline, k_under, group=g, bias=0.25 if far else 0.0)
    panel = p.poly(_inset(outline, margin, scallop), k_panel_far if far else k_panel, clip=[wing], group=g + 1,
                   bias=0.1 if far else -0.05)
    if p.big:
        for row in rows:
            p.stroke(row, "fth0" if far else "fth1")
    for v in veins:
        p.limb(v, 1.8, 1.2, k_wax, group=g + 2, bias=0.2 if far else 0.0)
    p.limb(frame, 4.2 if not far else 3.4, 2.0, k_wax, group=g + 3, bias=0.2 if far else 0.0)
    return wing, panel


def _row(a, b, c, wave=0.6, n=10):
    """A row of feather tips across a panel: a gentle curve from a through b
    to c, rippled so it reads as the edges of overlapping feathers."""
    pts = bez(a, b, c, n=n)
    out = []
    for i, (x, y) in enumerate(pts):
        out.append((x, y + (wave if i % 2 else -wave * 0.3)))
    return out


def _antenna(p, root, tip, side=1, bias=0.0):
    """A feathery moth antenna: a curved shaft with short barbs."""
    mid = ((root[0] + tip[0]) / 2 + 2 * side, (root[1] + tip[1]) / 2)
    path = bez(root, mid, tip, n=10)
    p.limb(path, 1.6, 1.2, k_body, bias=bias)
    if p.big:
        for i in range(3, len(path) - 1, 2):
            (x0, y0), (x1, y1) = path[i - 1], path[i]
            dx, dy = x1 - x0, y1 - y0
            d = math.hypot(dx, dy) or 1
            nx, ny = -dy / d, dx / d
            p.stroke([(x1, y1), (x1 + nx * 2 - dx * 0.5, y1 + ny * 2 - dy * 0.5)], "ruf1")
            p.stroke([(x1, y1), (x1 - nx * 2 - dx * 0.5, y1 - ny * 2 - dy * 0.5)], "body0")


def _fuzz(cx, cy, rx, ry, n=14, depth=1.6):
    """An outline for a fluffy moth body: an ellipse with soft tufts."""
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        r = 1.0 if i % 2 else 1.0 + depth / max(rx, ry)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def _sub(p, k, cx, cy):
    """A pen drawing at k times p's scale about design point (cx, cy)."""
    from mon_lib import Pen
    return Pen(p.fig, p.s * k, p.ox + p.s * (cx - cx * k), p.oy + p.s * (cy - cy * k), p.view, p.phase)


def _front(p, view, fl):
    """Battle front: three-quarter view facing left, climbing, the great
    near forewing raised toward the sun and sagging as its wax runs."""
    B = -fl if view == "front" else 0     # the body bobs up as the wings beat down
    W = 2 * fl                            # how far the wings sweep down

    # ---- far wings, behind the body: a value step darker ----
    far_fore = (bez3((25, 25 + B), (18, 17 + B), (11, 11 + W), (5, 8 + W))
                + bez3((5, 8 + W), (1.5, 9 + W), (1.5, 15 + W), (3, 18 + W))
                + bez3((3, 18 + W), (4, 25 + W), (8, 30 + W), (14, 33 + W))
                + bez3((14, 33 + W), (19, 33 + B), (23, 30 + B), (25, 27 + B)))
    _moth_wing(p, far_fore, [bez((24, 26 + B), (14, 20 + W), (6, 22 + W))],
               bez((25, 25 + B), (16, 16 + W), (5, 8 + W)),
               rows=[_row((20, 27 + B), (12, 26 + W), (8, 28 + W)), _row((19, 21 + B), (12, 17 + W), (7, 14 + W))],
               far=True, g=40, margin=2.6, scallop=(18, 34))
    far_hind = (bez3((26, 31 + B), (21, 32 + B), (17, 37 + fl), (18, 41 + fl))
                + bez3((18, 41 + fl), (20, 45 + fl), (25, 44 + fl), (27, 38 + B)))
    _moth_wing(p, far_hind, [], bez((26, 31 + B), (21, 33 + B), (18, 40 + fl)), far=True, g=50, margin=2.2)
    _drip(p, 8, 31 + W, 3.4, bias=0.2)

    # ---- the abdomen, banded, hanging below ----
    abd = bez((27, 33 + B), (29, 40 + B), (31, 47 + B))
    p.limb(abd, 6.8, 2.6, k_body, group=10)
    if p.big:
        for t, w in ((0.3, 6), (0.55, 5), (0.78, 3.8)):
            i = int(t * (len(abd) - 1))
            x, y = abd[i]
            p.stroke([(x - w / 2, y + 0.4), (x + w / 2, y - 0.6)], "olv1")
            p.stroke([(x - w / 2 + 0.3, y + 1.3), (x + w / 2 + 0.3, y + 0.3)], "olv0")
    for (x0, y0), (x1, y1) in (((23, 31 + B), (19, 36 + B)), ((25, 32 + B), (23, 38 + B))):
        p.limb([(x0, y0), (x1, y1)], 1.5, 1.2, k_leg, bias=0.1)

    # ---- near hind wing ----
    hind = (bez3((32, 31 + B), (40, 30 + B), (48, 32 + W - fl), (51, 37 + W - fl))
            + bez3((51, 37 + W - fl), (53, 43 + W), (47, 49 + W), (41, 48 + W))
            + bez3((41, 48 + W), (35, 46 + B), (31, 40 + B), (32, 31 + B)))
    _moth_wing(p, hind, [bez((33, 33 + B), (40, 37 + B), (46, 45 + W))],
               bez((31, 32 + B), (41, 30 + B), (51, 36 + W - fl)),
               rows=[_row((36, 41 + B), (42, 44 + W), (48, 42 + W)), _row((38, 35 + B), (44, 36 + W), (49, 38 + W))],
               g=60, margin=2.8, scallop=(16, 30))

    # ---- near fore wing: raised toward the sun, its tip sagging as the wax runs ----
    fore = (bez3((30, 26 + B), (37, 15 + B), (44, 7 + W), (51, 5 + W))
            + bez3((51, 5 + W), (57, 4.5 + W), (61.5, 10 + W), (61, 18 + W))
            + bez3((61, 18 + W), (60, 24 + W), (58, 29 + W), (54, 32 + W))
            + bez3((54, 32 + W), (47, 35 + W), (39, 34 + B), (32, 30 + B)))
    _moth_wing(p, fore, [bez((32, 28 + B), (45, 24 + W), (57, 25 + W))],
               bez((29, 27 + B), (39, 14 + B), (51, 5 + W)),
               rows=[_row((37, 31 + B), (47, 32 + W), (55, 30 + W)), _row((39, 22 + B), (49, 18 + W), (58, 19 + W)),
                     _row((42, 15 + B), (50, 10 + W), (57, 11 + W))],
               g=70, margin=3.0, scallop=(30, 52))
    # the melt: wax running thick off the sagging tip and the outer edge
    if p.big:
        # wax running down the sagging tip in gold streaks
        for x0, y0, x1, y1 in ((51, 7, 50, 15), (55, 7, 55, 19), (59, 11, 59.5, 20)):
            p.stroke([(x0, y0 + W), (x1, y1 + W)], "wax1")
            p.stroke([(x0 - 1, y0 + 1 + W), (x1 - 1, y1 + W)], "wax0")
    for x, y, ln in ((59.5, 22 + W, 6 + fl), (56, 29 + W, 7 + fl), (50, 33 + W, 5), (44, 46 + W, 3)):
        _drip(p, x, y, ln, r=1.8)

    # ---- the amber ruff, the head, the feathery antennae ----
    p.poly(_fuzz(26, 27 + B, 7.2, 6.6, 11, 2.2), k_ruff, group=11)
    _antenna(p, (23, 14 + B), (31, 2 + B), side=-1, bias=0.15)
    p.poly(_fuzz(21, 18.5 + B, 5.8, 5.4, 9, 1.2), k_head, group=12)
    _antenna(p, (19, 14 + B), (15, 1 + B), side=-1)
    if not p.big:
        p.px(18, 19 + B, "wax2")


def ikaroth(p, view, phase):
    if view in ("front", "side", "icon"):
        fl = 1 if phase == 1 else 0
        _front(_sub(p, 0.86, 32, 27), view, fl)
        return

    if view == "back":
        # over the shoulder at about 1.2x: both wings spread wide from behind,
        # the amber ruff and the head turned right with its great gold eye
        far = (bez3((38, 40), (45, 28), (51, 18), (56, 9))
               + bez3((56, 9), (60, 8), (62, 13), (61, 18))
               + bez3((61, 18), (62, 30), (59, 42), (52, 50))
               + bez3((52, 50), (46, 52), (41, 48), (38, 42)))
        _moth_wing(p, far, [bez((39, 42), (50, 36), (60, 30))], bez((37, 41), (47, 26), (56, 9)),
                   rows=[_row((43, 46), (51, 44), (57, 40)), _row((44, 34), (52, 28), (58, 22))],
                   far=True, g=40, margin=3.0, scallop=(18, 34))
        near = (bez3((28, 44), (20, 30), (13, 18), (7, 8))
                + bez3((7, 8), (2.5, 7), (1, 13), (2, 19))
                + bez3((2, 19), (1, 34), (3, 48), (10, 58))
                + bez3((10, 58), (18, 62), (26, 56), (28, 46)))
        _moth_wing(p, near, [bez((27, 46), (16, 42), (4, 38)), bez((27, 44), (15, 30), (3, 22))],
                   bez((29, 44), (19, 26), (7, 8)),
                   rows=[_row((24, 54), (14, 52), (6, 46)), _row((22, 40), (12, 36), (5, 30)), _row((20, 28), (11, 22), (5, 16))],
                   g=60, margin=3.4, scallop=(18, 36))
        # the wax running in long streaks down the backs of the wings,
        # beading and dropping off their lower edges
        for x, y, ln in ((9, 12, 13), (16, 22, 11), (22, 32, 9), (55, 13, 10), (59, 21, 10), (52, 49, 5)):
            _drip(p, x, y, ln, r=1.7)
        # the body: a banded abdomen dropping out of frame, the amber ruff, the head
        p.limb(bez((33, 52), (34, 60), (32, 68)), 13, 10, k_body, group=10)
        p.poly(_fuzz(32, 45, 11, 10, 12, 2.6), k_ruff, group=11)
        _antenna(p, (41, 27), (34, 8), side=1, bias=0.12)
        p.poly(_fuzz(45, 33, 8, 7.4, 10, 1.4), k_head, group=12)
        _antenna(p, (45, 27), (52, 8), side=1)
        if p.big:
            for i, y in enumerate((57, 61)):
                p.stroke([(27 + i * 0.4, y + 1), (39 - i * 0.6, y - 1.2)], "olv1")
                p.stroke([(27 + i * 0.4, y + 2), (39 - i * 0.6, y - 0.2)], "olv0")
        return

    if view in ("down", "up"):
        # follower: hovering, wings spread; the wingbeat lifts and lowers them
        fl = phase
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            fore = [(X(30), 27), (X(22), 18), (X(14), 12 + fl), (X(7), 10 + fl), (X(4), 14 + fl), (X(4), 22 + fl),
                    (X(9), 31 + fl), (X(18), 34), (X(28), 32)]
            hind = [(X(29), 33), (X(22), 35), (X(17), 40 - fl), (X(19), 46 - fl), (X(26), 45), (X(30), 38)]
            _moth_wing(p, hind, [], [(X(29), 33), (X(18), 39 - fl)], g=40 if sx < 0 else 60, margin=2.4)
            _moth_wing(p, fore, [[(X(28), 29), (X(8), 22 + fl)]], [(X(30), 27), (X(14), 12 + fl), (X(7), 10 + fl)],
                       g=44 if sx < 0 else 64, margin=2.8)
            _drip(p, X(10), 31 + fl, 3)
        p.limb([(32, 34), (32, 47)], 5.4, 2.6, k_body, group=10)
        p.poly(_fuzz(32, 30, 6, 5.4, 10, 1.6), k_ruff, group=11)
        if view == "down":
            _antenna(p, (30, 20), (25, 9), side=-1)
            _antenna(p, (34, 20), (39, 9), side=1)
            p.poly(_fuzz(32, 23, 5.2, 4.8, 9, 1.0), k_head, group=12)
            p.eye(28, 21, 3, 4, iris="wax1", shine="fth3")
            p.eye(33, 21, 3, 4, iris="wax1", shine="fth3", shine_at=(0, 1))
        else:
            p.poly(_fuzz(32, 23, 5.2, 4.8, 9, 1.0), k_head, group=12)
            _antenna(p, (30, 20), (25, 9), side=-1)
            _antenna(p, (34, 20), (39, 9), side=1)
        return


MONS = [
    # icon palette 1 keeps the wax gold and the feathers pale
    Mon("Ikaroth", IKAROTH_COLORS, IKAROTH_SHINY, ikaroth, foot="blank", icon_pal=1),
]
