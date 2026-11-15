"""Triptolemus line: Stachyss, Stachypter (Grass, Grass/Dragon). The
serpents of Demeter's winged chariot, on which Triptolemus of Eleusis flew
over every land sowing grain."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink


def _body(p, pts, w0, w1, mat, n=18, **kw):
    """A serpent body along a smooth path through pts (Catmull-Rom),
    tapering linearly from w0 to w1. Returns the part id."""
    path = _spline(pts, n)
    return p.limb(path, w0, w1, mat, **kw)


def _spline(pts, n=10):
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


def _along(path, t):
    """Point and unit direction at fraction t along a polyline."""
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])]
    d = t * sum(lens)
    for (a, b), ln in zip(zip(path, path[1:]), lens):
        if d <= ln and ln:
            k = d / ln
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k), ((b[0] - a[0]) / ln, (b[1] - a[1]) / ln)
        d -= ln
    a, b = path[-2], path[-1]
    ln = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    return b, ((b[0] - a[0]) / ln, (b[1] - a[1]) / ln)


# --------------------------------------------------------------------------
# Stachyss, the wheat serpent
# --------------------------------------------------------------------------

STACHYSS_COLORS = [
    ("ink", INK),
    ("sc0", (48, 72, 32)), ("sc1", (88, 112, 40)), ("sc2", (136, 160, 64)), ("sc3", (184, 200, 104)),
    ("bl0", (176, 144, 96)), ("bl1", (216, 192, 144)), ("bl2", (240, 224, 184)),
    ("wh0", (168, 104, 24)), ("wh1", (216, 152, 40)), ("wh2", (248, 200, 72)), ("wh3", (248, 232, 152)),
    ("white", C.white), ("mouth", (176, 72, 56)),
]
STACHYSS_SHINY = {
    # terracotta scales, pale marble wheat
    "sc0": (112, 40, 24), "sc1": (168, 72, 40), "sc2": (208, 112, 64), "sc3": (232, 160, 112),
    "wh0": (152, 144, 136), "wh1": (200, 192, 184), "wh2": (232, 224, 216), "wh3": (248, 248, 240),
}

sy_scale = Mat(["sc0", "sc1", "sc2", "sc3"], line="sc0", cuts=[0.2, 0.46, 0.74])
sy_belly = Mat(["bl0", "bl1", "bl2"], line="bl0", cuts=[0.36, 0.7])
sy_wheat = Mat(["wh0", "wh1", "wh2", "wh3"], line="wh0", cuts=[0.2, 0.46, 0.76])


def _ear(p, base, d, ln, w, mat, **kw):
    """A wheat ear rising from base in direction d (unit), ln long."""
    tip = (base[0] + d[0] * ln, base[1] + d[1] * ln)
    return p.lens(base, tip, w, mat, fat=0.45, **kw)


def _crest(p, path, ts, ln, w, mat, side=1, lean=35, out=1.5, **kw):
    """Wheat ears along a body path, on its side `side`, leaning back by
    `lean` degrees. Draw it after the body with under=True so each ear sits
    behind the spine it grows from."""
    for t in ts:
        (x, y), (ux, uy) = _along(path, t)
        nx, ny = uy * side, -ux * side          # the normal on the chosen side
        a = math.radians(lean)
        dx, dy = nx * math.cos(a) + ux * math.sin(a), ny * math.cos(a) + uy * math.sin(a)
        _ear(p, (x + nx * out, y + ny * out), (dx, dy), ln, w, mat, **kw)


SY_BACK = [(22.5, 52), (31, 49.2), (42, 49.2), (51, 50.5), (56.5, 47.5), (58.5, 42.5), (56.5, 39)]
SY_FRONT = [(49, 55.5), (41, 59.2), (30, 59.2), (22.5, 56.5), (22, 52)]
SY_NECK = [(48, 57), (52.5, 51), (49.5, 44.5), (42, 41.5), (35.5, 40), (29.5, 35.5)]


def stachyss(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        back = _spline(SY_BACK)
        neck = _spline([(x, y - (L if y < 46 else 0)) for x, y in SY_NECK])
        p.limb(back, 7.4, 1.4, sy_scale, group=1, bias=0.12)
        _crest(p, back, (0.3, 0.46, 0.62), 7, 3.4, sy_wheat, side=1, lean=48, out=1.0, under=True, bias=0.15)
        p.limb(_spline(SY_FRONT), 7.6, 7.4, sy_scale, group=2)
        p.limb(_spline([(46, 59.6), (36, 60.4), (27, 59.4)]), 2.6, 2.4, sy_belly, group=2, noline=True)
        nk = p.limb(neck, 7.2, 5.6, sy_scale, group=3)
        # ears along the neck crest, behind the neck
        _crest(p, neck, (0.36, 0.52, 0.68, 0.84), 7.5, 3.6, sy_wheat, side=-1, lean=-46, out=1.0, under=True)
        p.limb(_spline([(47, 55), (49.6, 50), (47, 45.5)]), 2.6, 2.2, sy_belly, clip=[nk], group=3, noline=True)
        # head: a round skull, the snout tilted down, curious; two long awns
        # sweep back from the crown like a hood
        hx, hy = 24.5, 32.5 - L
        p.limb(bez((hx + 3, hy - 6), (hx + 10, hy - 11), (hx + 17.5, hy - 6)), 3.0, 2.2, sy_wheat, bias=0.15)
        p.limb(bez((hx + 5, hy - 3.5), (hx + 12, hy - 6.5), (hx + 16, hy - 1)), 3.0, 2.2, sy_wheat)
        p.blob(hx, hy, 7.6, 6.5, sy_scale, ang=-12, group=4)
        p.blob(hx - 6.4, hy + 2.6, 4.6, 3.4, sy_scale, ang=18, group=4)
        p.blob(hx - 3.8, hy + 5.0, 5.4, 1.8, sy_belly, ang=12, group=5)
        if p.big:
            p.eye(hx - 4.5, hy - 4.5, 5, 5, iris="wh1", shine="white", shine_at=(1, 1))
            p.pxs([(hx - 9.5, hy - 0.5)], "ink")
            p.stroke([(hx - 8.5, hy + 3.5), (hx - 3, hy + 3.5)], "sc0")
        else:
            p.px(hx - 3, hy - 1, "ink")
        return

    if view == "back":
        # over the shoulder: the raised neck and head in right profile, the
        # wheat crest running down the back, coils cropped by the frame
        p.limb(_spline([(6, 64), (12, 56), (24, 52), (38, 54), (50, 60), (54, 66)]), 11, 11, sy_scale, group=1,
               bias=0.08)
        neck = _spline([(26, 66), (24, 54), (28, 42), (35, 34), (40, 28)])
        _crest(p, neck, (0.25, 0.4, 0.55, 0.7, 0.85), 7.5, 4, sy_wheat, side=-1, lean=-40)
        p.limb(neck, 10, 7.5, sy_scale, group=2)
        hx, hy = 44, 25
        p.taper(bez((hx - 3, hy - 4), (hx - 12, hy - 9), (hx - 19, hy - 5)), 2.4, sy_wheat)
        p.blob(hx, hy, 7.8, 6.6, sy_scale, ang=12, group=4)
        p.blob(hx + 7, hy + 2.2, 4.8, 3.6, sy_scale, ang=-18, group=4)
        p.blob(hx + 4, hy + 5, 5.4, 1.8, sy_belly, ang=-12, group=5)
        if p.big:
            p.eye(hx + 3, hy - 3, 4, 4, iris="wh1", shine="white", shine_at=(2, 1))
        return

    if view in ("down", "up"):
        # follower: the head raised over a coil on the ground, the awns
        # spread like a hood; the walk sways the neck and rolls the coil
        S = 1 if phase else -1
        ring = [(32 + 15 * math.cos(t / 10 * 2 * math.pi), 53.5 + 5.5 * math.sin(t / 10 * 2 * math.pi)) for t in
                range(11)]
        p.limb(_spline(ring[:6]), 7, 7, sy_scale, group=1, bias=0.1)
        p.limb(_spline(ring[5:] + [ring[0]]), 7.4, 7.4, sy_scale, group=2)
        neck = _spline([(32 + 4 * S, 54), (32 + 3 * S, 45), (32 - S, 37), (32, 30)])
        nk = p.limb(neck, 8.6, 7.4, sy_scale, group=3)
        if view == "up":
            _crest(p, neck, (0.15, 0.35, 0.55, 0.75), 6, 3.6, sy_wheat, side=1, lean=0, out=0.5)
            _crest(p, neck, (0.25, 0.45, 0.65), 6, 3.6, sy_wheat, side=-1, lean=0, out=0.5)
        else:
            p.limb(_spline([(32 + 4 * S, 54), (32 + 3 * S, 45), (32 - S, 37), (32, 31)]), 3.4, 3.0, sy_belly,
                   clip=[nk], group=3, noline=True)
        for sg in (-1, 1):
            p.limb(bez((32 + sg * 4, 22), (32 + sg * 13, 17), (32 + sg * 15, 27 + (phase if sg > 0 else 1 - phase))),
                   3.0, 2.0, sy_wheat)
        p.blob(32, 25, 7.6, 6.6, sy_scale, group=4)
        if view == "down":
            p.blob(32, 30, 5, 3.4, sy_scale, group=4)
            p.blob(32, 32, 4, 1.6, sy_belly, group=5)
            p.eye(26, 23, 3, 4, iris="wh1", shine="white")
            p.eye(35, 23, 3, 4, iris="wh1", shine="white")
            if p.big:
                p.pxs([(30, 30), (33, 30)], "ink")
        return


# --------------------------------------------------------------------------
# Stachypter, the winged sower
# --------------------------------------------------------------------------

STACHYPTER_COLORS = [
    ("ink", INK),
    ("sc0", (24, 56, 40)), ("sc1", (48, 88, 48)), ("sc2", (96, 128, 56)), ("sc3", (152, 168, 80)),
    ("lf", (200, 208, 120)),
    ("bl0", (176, 144, 96)), ("bl1", (208, 184, 136)), ("bl2", (240, 224, 184)),
    ("wh0", (168, 104, 24)), ("wh1", (224, 160, 48)), ("wh2", (248, 216, 104)),
    ("tl0", (48, 136, 120)), ("tl1", (136, 208, 184)), ("white", C.white),
]
STACHYPTER_SHINY = {
    "sc0": (96, 32, 24), "sc1": (152, 64, 40), "sc2": (200, 104, 56), "sc3": (232, 152, 96), "lf": (248, 200, 152),
    "wh0": (152, 144, 136), "wh1": (208, 200, 192), "wh2": (248, 248, 240),
}

st_scale = Mat(["sc0", "sc1", "sc2", "sc3"], line="sc0", cuts=[0.2, 0.46, 0.74])
st_leaf = Mat(["sc1", "sc2", "sc3", "lf"], line="sc0", cuts=[0.22, 0.48, 0.76])
st_leaf_far = Mat(["sc0", "sc1", "sc2"], line="sc0", cuts=[0.34, 0.68])
st_belly = Mat(["bl0", "bl1", "bl2"], line="bl0", cuts=[0.36, 0.7])
st_wheat = Mat(["wh0", "wh1", "wh2"], line="wh0", cuts=[0.3, 0.66])


def _blade(p, a, b, w, mat, bend=0.0, vein=True, **kw):
    pid = p.lens(a, b, w, mat, bend=bend, fat=0.4, **kw)
    if vein and p.big:
        m = ((a[0] * 3 + b[0] * 2) / 5, (a[1] * 3 + b[1] * 2) / 5)
        p.stroke([a, m], "tl1")
    return pid


def _wing(p, root, elbow, wrist, blades, mat, w=3.2, **kw):
    """A leaf wing: an arm root-elbow-wrist and blades [(t, tip, width,
    bend)], t along the arm (0 root .. 2 wrist), drawn back to front."""
    for t, tip, bw, bend in blades:
        if t <= 1:
            base = (root[0] + (elbow[0] - root[0]) * t, root[1] + (elbow[1] - root[1]) * t)
        else:
            base = (elbow[0] + (wrist[0] - elbow[0]) * (t - 1), elbow[1] + (wrist[1] - elbow[1]) * (t - 1))
        _blade(p, base, tip, bw, mat, bend=bend, **kw)
    p.limb([root, elbow, wrist], w, w * 0.7, st_scale, **kw)


def _seed(p, x, y):
    if p.big:
        p.pxs([(x, y), (x, y + 1)], "wh1")
        p.px(x, y, "wh2")


ST_LOOP_BACK = [(55, 50), (53, 41), (45, 36.5), (34, 37), (24, 39.5), (16, 42), (10.5, 40), (10, 35.5)]
ST_LOOP_FRONT = [(27, 33), (22.5, 42), (24, 51.5), (33, 57.5), (45, 58.2), (53.5, 53.5), (55, 46)]
ST_NECK = [(27, 36), (28, 28), (25, 22), (20.5, 17)]


def stachypter(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        W = 2 if (phase == 1 and view != "icon") else 0
        # far wing rising behind the head
        _wing(p, (29, 29), (31, 19), (34, 11 - W),
              [(2.0, (30, 2 - W), 5.4, 0.6), (1.85, (38, 1.5 - W), 5.8, -0.2), (1.5, (45, 4 - W), 5.8, -0.6),
               (1.1, (48, 11 - W // 2), 5.0, -0.6)], st_leaf_far, w=3, bias=0.1)
        # the top of the loop and the tail, passing behind the neck to a
        # curl on the left with a wheat tuft
        back = _spline(ST_LOOP_BACK)
        p.limb(back, 10, 3, st_scale, group=1, bias=0.1)
        _crest(p, back, (0.12, 0.26, 0.4, 0.54), 7.5, 4.2, st_wheat, side=1, lean=-45, out=1.0, under=True,
               bias=0.1)
        tx, ty = ST_LOOP_BACK[-1]
        _ear(p, (tx + 0.5, ty + 0.5), (0.25, -1), 8, 4.2, st_wheat)
        # near wing: a leading edge to the wrist, leaf blades trailing back
        # from it like primaries, each upper blade over the next
        for a, b, w in (((35, 27), (44.5, 39.5), 6.6), ((38, 23.5), (50.5, 37), 7.4),
                        ((41, 20.5), (56, 32.5 - W // 2), 7.8), ((44, 16.5 - W // 2), (59.5, 26 - W), 8.0),
                        ((46.5, 13 - W), (61.5, 18.5 - W), 8.0), ((49, 10 - W), (62, 10.5 - W), 7.6),
                        ((51, 8 - W), (61.5, 2.5 - min(W, 1)), 7.0)):
            _blade(p, a, b, w, st_leaf, bend=0.6)
        p.limb([(32, 30), (42, 19 - W // 2), (51, 8 - W)], 4.4, 3.2, st_scale)
        # the near half of the loop and the chest, then neck and crest
        front = _spline(ST_LOOP_FRONT)
        fr = p.limb(front, 11.5, 10, st_scale, group=2)
        p.limb(_spline([(23, 44), (26.5, 53.5), (35, 58.5), (46, 59), (53, 54.5)]), 4, 3.4, st_belly,
               clip=[fr], group=2, noline=True)
        neck = _spline([(x, y - L) if y < 30 else (x, y) for x, y in ST_NECK])
        nk = p.limb(neck, 10.5, 8.0, st_scale, group=3)
        _crest(p, neck, (0.2, 0.42, 0.64), 8, 4.4, st_wheat, side=-1, lean=-40, out=1.0, under=True)
        p.limb(_spline([(23.5, 37), (24, 29), (21, 23)]), 3.6, 3, st_belly, clip=[nk], group=3, noline=True)
        # the long, wise head; awn horns swept back
        hx, hy = 16.5, 14 - L
        for a, b, w, bend in (((18.5, 11), (32, 1.5), 5.6, 2.2), ((21, 13), (37, 7), 5.2, 1.8),
                              ((21, 16), (35, 15.5), 4.4, 1.2)):
            p.lens((a[0], a[1] - L), (b[0], b[1] - L), w, st_wheat, bend=bend, fat=0.28)
        p.blob(hx, hy, 6.8, 5.6, st_scale, ang=-8, group=4)
        p.lens((hx + 2, hy + 1.5), (hx - 14, hy + 4), 7.0, st_scale, group=4, fat=0.3)
        p.lens((hx + 3, hy + 5.2), (hx - 11, hy + 6.0), 3.0, st_belly, group=5, fat=0.3)
        for x, y in ((61, 34), (60, 39), (62, 43), (58, 44), (60, 49), (62, 53), (57, 52)):
            _seed(p, x, y + L)
        if p.big:
            p.eye(hx - 4, hy - 2.5, 4, 3, iris="wh1", shine="white", shine_at=(1, 0))
            p.px(hx - 13, hy + 2.5, "ink")
        else:
            p.px(hx - 3, hy - 1, "ink")
        return

    if view == "back":
        # over the shoulder: the full wingspan, seed falling, the head in
        # right profile
        _wing(p, (42, 38), (50, 28), (56, 20),
              [(2.0, (62, 6), 6, 0.4), (1.7, (62, 17), 6, 0.2), (1.3, (62, 28), 5.6, 0)], st_leaf_far, w=3.6,
              bias=0.1)
        _wing(p, (34, 40), (24, 26), (14, 12),
              [(2.0, (2, 2), 7.4, -0.6), (1.85, (2, 14), 7.4, -0.4), (1.6, (3, 27), 7.0, -0.2),
               (1.3, (6, 38), 6.6, 0), (0.95, (12, 46), 6.0, 0.2)], st_leaf, w=4.4)
        p.limb(_spline([(14, 66), (24, 54), (38, 50), (52, 56), (58, 66)]), 15, 15, st_scale, group=1)
        neck = _spline([(36, 56), (39, 42), (43, 32), (48, 25)])
        nk = p.limb(neck, 12, 9, st_scale, group=2)
        _crest(p, neck, (0.15, 0.32, 0.5, 0.68), 8.5, 4.6, st_wheat, side=-1, lean=-40, out=1.0, under=True)
        hx, hy = 50, 20
        for a, b in (((47, 15), (34, 6)), ((46, 18), (33, 14))):
            p.limb(bez(a, ((a[0] + b[0]) / 2, a[1] - 5), b), 4, 1.8, st_wheat)
        p.blob(hx, hy, 7.4, 6, st_scale, ang=8, group=4)
        p.lens((hx - 2, hy + 1.5), (hx + 12, hy + 3.5), 6.6, st_scale, group=4, fat=0.35)
        if p.big:
            p.eye(hx + 3, hy - 3, 4, 3, iris="wh1", shine="white", shine_at=(2, 0))
            for x, y in ((4, 44), (7, 50), (3, 54), (10, 56), (6, 60)):
                _seed(p, x, y)
        return

    if view in ("down", "up"):
        # follower: wings spread to both sides, the head raised over the loop
        F = phase
        ring = [(32 + 14 * math.cos(t / 10 * 2 * math.pi), 52 + 6 * math.sin(t / 10 * 2 * math.pi)) for t in range(11)]
        p.limb(_spline(ring[:6]), 9, 9, st_scale, group=1, bias=0.1)
        for sg in (-1, 1):
            _wing(p, (32 + sg * 5, 34), (32 + sg * 13, 25), (32 + sg * 21, 17 + 2 * F),
                  [(2.0, (32 + sg * 31, 13 + 2 * F), 7.4, 0), (1.7, (32 + sg * 31, 24 + F), 7.6, 0),
                   (1.35, (32 + sg * 28, 34), 7.4, 0), (1.0, (32 + sg * 21, 41), 6.6, 0)], st_leaf, w=4.2)
        p.limb(_spline(ring[5:] + [ring[0]]), 9.6, 9.6, st_scale, group=2)
        neck = _spline([(32, 52), (32 + (1 if F else -1), 40), (32, 27)])
        nk = p.limb(neck, 11, 9, st_scale, group=3)
        if view == "up":
            _crest(p, neck, (0.15, 0.4, 0.65), 7, 4.2, st_wheat, side=1, lean=0, out=0.5)
            _crest(p, neck, (0.28, 0.53), 7, 4.2, st_wheat, side=-1, lean=0, out=0.5)
        else:
            p.limb(_spline([(32, 52), (32 + (1 if F else -1), 40), (32, 28)]), 4.2, 3.6, st_belly, clip=[nk],
                   group=3, noline=True)
        for sg in (-1, 1):
            p.limb(bez((32 + sg * 3, 14), (32 + sg * 9, 7), (32 + sg * 16, 6)), 4.6, 1.8, st_wheat)
        p.blob(32, 20, 7.6, 6.6, st_scale, group=4)
        if view == "down":
            p.blob(32, 27, 4.6, 4.4, st_scale, group=4)
            p.blob(32, 30, 3.4, 1.6, st_belly, group=5)
            p.eye(26, 18, 3, 3, iris="wh1", shine="white")
            p.eye(35, 18, 3, 3, iris="wh1", shine="white")
        return


MONS = [
    Mon("Stachyss", STACHYSS_COLORS, STACHYSS_SHINY, stachyss, foot="coil"),
    Mon("Stachypter", STACHYPTER_COLORS, STACHYPTER_SHINY, stachypter, foot="coil"),
]
