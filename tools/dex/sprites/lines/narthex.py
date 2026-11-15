"""Narthex line: Narthip, Promethex (Grass, then Grass/Fire). Prometheus hid
the stolen fire in a hollow fennel stalk, the narthex, and gave it to
mortals."""
import math

from mon_lib import C, Mat, Mon, bez, lerp

INK = C.ink


def _along(path):
    """Arc-length lookup along a polyline: returns (total, at), where at(d)
    gives the point and direction d design px along it."""
    acc = [0.0]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        acc.append(acc[-1] + math.hypot(x1 - x0, y1 - y0))
    total = acc[-1] or 1.0

    def at(d):
        for i in range(len(path) - 1):
            if acc[i + 1] >= d:
                u = (d - acc[i]) / ((acc[i + 1] - acc[i]) or 1)
                (x0, y0), (x1, y1) = path[i], path[i + 1]
                return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, x1 - x0, y1 - y0
        (x0, y0), (x1, y1) = path[-2], path[-1]
        return x1, y1, x1 - x0, y1 - y0
    return total, at


def _frond(p, path, w, mat, r0=None, step=None, bias=0.0, **kw):
    """A feathery fennel frond: little leaflet tufts bunched along a curved
    rachis (use bez), alternating side to side and shrinking toward the tip.
    Each tuft is its own part, drawn tip first, so the ones nearer the stem
    overlap the next with a fine line: the silhouette scallops and the
    inside reads as layered leaflets. w is the plume's full width."""
    kw.pop("group", None)
    r0 = r0 or max(1.6, w * 0.32)
    step = step or max(1.3, r0 * 0.72)
    total, at = _along(path)
    ds, d = [], 0.0
    while d <= total:
        ds.append(d)
        d += step
    first = None
    for k, d in reversed(list(enumerate(ds))):
        x, y, dx, dy = at(d)
        dd = math.hypot(dx, dy) or 1
        dx, dy = dx / dd, dy / dd
        t = d / total
        side = 1 if k % 2 == 0 else -1
        off = max(0.0, w / 2 - r0) * (1 - 0.7 * t) * side
        r = max(0.9, r0 * (1 - 0.5 * t))
        pid = p.circle(x - dy * off + dx * r * 0.4, y + dx * off + dy * r * 0.4, r, mat,
                       bias=bias + (0.08 if side < 0 else -0.04), **kw)
        first = first or pid
    return first


# --------------------------------------------------------------------------
# Narthip, the fennel sprout
# --------------------------------------------------------------------------

NARTHIP_COLORS = [
    ("ink", INK),
    # the limestone stalk
    ("st0", (144, 112, 72)), ("st1", (184, 152, 104)), ("st2", (216, 192, 144)), ("st3", (240, 224, 184)),
    # olive fronds with a silver-leaf sheen
    ("ol0", (48, 72, 32)), ("ol1", (88, 112, 40)), ("ol2", (136, 160, 64)), ("silver", (184, 200, 144)),
    # the umbel of sun-gold buds
    ("gold0", (200, 136, 32)), ("gold1", (240, 192, 64)), ("gold2", (248, 232, 144)),
    # the dark hollow inside the stalk, the root, the eye shine
    ("hollow", (64, 40, 32)), ("root", (120, 88, 56)), ("white", C.white),
]
NARTHIP_SHINY = {
    "ol0": (104, 32, 16), "ol1": (160, 64, 24), "ol2": (208, 104, 48), "silver": (240, 168, 112),
    "gold0": (168, 168, 160), "gold1": (224, 224, 216), "gold2": (248, 248, 248),
}

stalk = Mat(["st0", "st1", "st2", "st3"], line="st0", cuts=[0.2, 0.46, 0.74])
frond = Mat(["ol0", "ol1", "ol2", "silver"], line="ol0", cuts=[0.16, 0.4, 0.68])
buds = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.38, 0.7])
hollow = Mat(["hollow", "root"], line="hollow", cuts=[0.6])
rootm = Mat(["root", "st0"], line="root", cuts=[0.55])


def _cap(p, cx, cy, tilt=0.0, scale=1.0):
    """The umbel cap: a tipped dome of sun-gold bud clusters on short rays
    springing from behind the chimney rim at (cx, cy)."""
    ca, sa = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))

    def rot(dx, dy):
        return cx + (dx * ca - dy * sa) * scale, cy + (dx * sa + dy * ca) * scale
    tops = [rot(-7.5, -4.5), rot(-4, -8), rot(0.5, -9.2), rot(5, -8), rot(8, -4.5)]
    for t in tops:
        p.limb([(cx, cy), t], 1.3, 1.1, frond)
    for i, (x, y) in enumerate(tops):
        p.circle(x, y, (2.4 if i in (0, 4) else 2.8) * scale, buds)


def narthip(p, view, phase):
    if view in ("front", "side", "icon"):
        # the bulb is its head: a round fennel bulb leaning forward on its
        # root, the hollow stalk on top tipping its bud cap back
        hop = 1 if (phase == 1 and view == "side") else 0
        wave = phase == 1 and view == "front"
        L = 1 if wave else 0

        # near frond-arm raised high and waving
        tip = (50, 33) if wave else (47.5, 29)
        _frond(p, bez((38, 45), (44, 42), tip), 7.6, frond, bias=0.12)
        # the root foot and its rootlets
        p.blob(32, 57.5 - hop, 5, 2.8, rootm, group=10)
        for path in ([(29, 58), (25.5, 60.6)], [(32.5, 59), (32.5, 61)], [(35.5, 58), (39, 60.6)]):
            p.limb([(x, y - hop) for x, y in path], 1.8, 1.1, rootm, group=11)
        # the neck of hollow stalk, leaning back, its open top a chimney
        p.limb(bez((34, 39), (36, 33), (38.5, 28.5 - L)), 8, 6.6, stalk, group=2)
        _cap(p, 40, 27.5 - L, tilt=18 + 6 * L, scale=0.92)
        p.blob(38.7, 28.3 - L, 3.6, 1.6, stalk, ang=20, group=6, flat=3)
        p.blob(38.6, 28.5 - L, 2.4, 0.9, hollow, ang=20, group=7, flat=0)
        # the bulb
        p.blob(30.5, 46, 11.4, 10.4, stalk, ang=-10, group=1)
        # far frond-arm held out in front
        _frond(p, bez((22, 48), (17, 50), (12, 47.5 - L)), 7, frond)

        if p.big:
            # big round eyes, the near one larger; a small open smile
            p.eye(29, 40, 5, 6, shine="white", shine_at=(1, 1))
            p.eye(23, 41, 3, 5, shine="white", shine_at=(0, 1))
            p.pxs([(26, 48), (27, 49), (28, 48)], "ink")
        else:
            p.px(31, 42, "ink")
            p.px(24, 43, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the round bulb-head turned right,
        # one eye and the smile in profile, the stalk leaning back with its
        # tipped cap, the fronds spread unevenly
        _frond(p, bez((22, 46), (13, 40), (7, 29)), 9, frond, bias=0.15)
        p.limb(bez((33, 36), (31, 27), (28, 20)), 10, 8, stalk, group=2)
        _cap(p, 27, 19, tilt=-20, scale=1.15)
        p.blob(28.2, 19.8, 4.4, 1.9, stalk, ang=-20, group=6, flat=3)
        p.blob(28.2, 20, 3, 1.1, hollow, ang=-20, group=7, flat=0)
        p.blob(34, 52, 18, 15, stalk, ang=8, group=1)
        _frond(p, bez((44, 57), (52, 56), (58, 49)), 8.4, frond)
        if p.big:
            p.eye(46, 41, 4, 6, shine="white", shine_at=(1, 1))
            p.pxs([(51, 50), (52, 51)], "ink")
        return

    if view in ("down", "up"):
        # follower: hopping on its root, both fronds swinging in turn
        step = phase
        p.blob(32, 58.5 - step, 4.6, 2.4, rootm, group=10)
        for path in ([(29, 58.5), (25.5, 60.6)], [(35, 58.5), (38.5, 60.6)]):
            p.limb([(x, y - step) for x, y in path], 1.8, 1.1, rootm, group=11)
        _frond(p, bez((24, 46), (18, 44), (14.5, 37 + step)), 7, frond)
        _frond(p, bez((40, 46), (46, 44), (49.5, 37 + (1 - step))), 7, frond)
        p.limb([(32, 38), (32, 29)], 7.6, 6.4, stalk, group=2)
        _cap(p, 32, 28, tilt=8, scale=0.92)
        if view == "down":
            p.blob(32, 28.6, 3.4, 1.5, stalk, group=6, flat=3)
            p.blob(32, 28.8, 2.2, 0.8, hollow, group=7, flat=0)
        p.blob(32, 47, 10.4, 10, stalk, group=1)
        if view == "down":
            p.eye(26, 42, 4, 5, shine="white", shine_at=(1, 1))
            p.eye(34, 42, 4, 5, shine="white", shine_at=(1, 1))
            p.pxs([(31, 50), (32, 50)], "ink")
        return


# --------------------------------------------------------------------------
# Promethex, the firebearer
# --------------------------------------------------------------------------

PROMETHEX_COLORS = [
    ("ink", INK),
    ("st0", (128, 96, 64)), ("st1", (184, 152, 104)), ("st2", (216, 192, 144)), ("st3", (240, 224, 184)),
    ("ol0", (40, 64, 32)), ("ol1", (80, 104, 40)), ("ol2", (136, 160, 64)), ("silver", (184, 200, 144)),
    ("gold0", (200, 136, 32)), ("gold1", (240, 192, 64)), ("gold2", (248, 240, 168)),
    # the stolen ember: terracotta heat with one orange accent
    ("emb0", (120, 48, 24)), ("emb1", (192, 88, 40)), ("orange", (248, 152, 48)),
]
PROMETHEX_SHINY = {
    "ol0": (96, 32, 16), "ol1": (152, 56, 24), "ol2": (208, 104, 48), "silver": (240, 168, 112),
    "emb0": (24, 48, 128), "emb1": (56, 112, 208), "orange": (128, 200, 248),
}

x_stalk = Mat(["st0", "st1", "st2", "st3"], line="st0", cuts=[0.2, 0.46, 0.74])
x_frond = Mat(["ol0", "ol1", "ol2", "silver"], line="ol0", cuts=[0.16, 0.4, 0.68])
x_buds = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.36, 0.68])
x_ember = Mat(["emb0", "emb1", "orange", "gold2"], line="emb0", cuts=[0.3, 0.55, 0.8])
x_fire = Mat(["emb1", "orange", "gold1", "gold2"], line="emb1", outline="emb0", cuts=[0.3, 0.55, 0.8])


def _flame(p, a, b, w, bend=0.0, **kw):
    """A flame tongue: an orange tongue rimmed with ember red, a gold heart
    and a pale-gold core at its base."""
    pid = p.lens(a, b, w, x_fire, bend=bend, fat=0.3, flat=1, **kw)
    kw.pop("group", None)
    p.lens(a, lerp(a, b, 0.62), w * 0.62, x_fire, bend=bend * 0.6, fat=0.3, flat=2, noline=True,
           nooutline=True, clip=[pid], **kw)
    if p.big:
        p.lens(a, lerp(a, b, 0.32), w * 0.34, x_fire, bend=bend * 0.3, fat=0.3, flat=3, noline=True,
               nooutline=True, clip=[pid], **kw)
    return pid


def _crown(p, hub, tops, r=3.4, **kw):
    """The great umbel: one bold tier of sun-gold umbellets, each on its own
    ray from the hub on the crown of the head."""
    for t in tops:
        p.limb([hub, t], 1.6, 1.2, x_frond, **kw)
    for i, (x, y) in enumerate(tops):
        p.circle(x, y, r * (0.86 if i in (0, len(tops) - 1) else 1.0), x_buds, **kw)


def _torch(p, base, top, flame_h, w=11, sway=0.0):
    """The stolen fire: a hollow fennel stalk, a node ring below its open
    mouth, and a great flame pouring up out of it."""
    p.limb([base, top], 3.6, 3.4, x_stalk)
    p.blob(lerp(base, top, 0.45)[0], lerp(base, top, 0.45)[1], 2.6, 1.3, x_frond, flat=1)
    tx, ty = top
    for a, b, ww in (((tx - 1.5, ty + 1), (tx - 7.5 + sway, ty - flame_h * 0.58), w * 0.52),
                     ((tx + 1.5, ty + 1), (tx + 6.5 + sway, ty - flame_h * 0.66), w * 0.52)):
        _flame(p, a, b, ww, bend=0.9 if b[0] < tx else -0.9)
    _flame(p, (tx, ty + 2), (tx - 2 + sway, ty - flame_h), w, bend=0.7)


def promethex(p, view, phase):
    if view in ("front", "side", "icon"):
        # Prometheus making off with the fire: a long stride, the stem leaning
        # into it, the fennel torch thrust high and forward
        L = 1 if (phase == 1 and view == "front") else 0
        stride = view == "side" and phase == 1

        # near frond-arm swept back for balance, its fronds trailing
        for path, w in ((bez((40, 31), (48, 31), (57, 26 - L)), 8.4), (bez((40, 33.5), (49, 38), (57, 37 + L)), 7.6),
                        (bez((39, 36), (45, 43), (51, 47)), 6.4)):
            _frond(p, path, w, x_frond, bias=0.14)

        # the back leg pushing off, the front leg reaching: roots for feet
        back = bez((37, 46.5), (43, 52.5), (48.5, 59.5)) if not stride else bez((36, 47), (37, 53), (36, 59.5))
        front = [(31, 46.5), (24.5, 51.5), (21.5, 59.5)] if not stride else [(32, 47), (29, 53), (27, 59.5)]
        p.limb(back, 7.6, 5.2, x_stalk, bias=0.18, group=11)
        for d in ((3, 1.5), (4.5, 0.2)):
            p.limb([back[-1], (back[-1][0] + d[0], back[-1][1] + d[1])], 2.2, 1.2, x_stalk, bias=0.18, group=11)
        p.limb(front, 8, 5.6, x_stalk, group=12)
        for d in ((-4, 1.2), (-2, 1.8), (1.5, 1.2)):
            p.limb([front[-1], (front[-1][0] + d[0], front[-1][1] + d[1])], 2.4, 1.2, x_stalk, group=12)
        # leaf sheaths flaring at the hip
        for a, b, bend in (((31, 46.5), (24, 52), 0.8), ((37, 46.5), (44, 51.5), -0.8)):
            _frond(p, bez(a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 0.5 * abs(bend)), b), 5.6, x_frond, bias=0.1)

        # the jointed stem: the swollen heart leaning forward, the neck, the head
        p.blob(34.5, 37.5, 9.6, 10, x_stalk, ang=-18, group=1)
        p.limb(bez((34, 47), (34, 44), (34.5, 42)), 8, 9, x_stalk, group=1)
        p.blob(34, 46.5, 5.2, 1.8, x_frond, group=5, flat=1)
        p.limb(bez((31.5, 30), (30, 26), (28.5, 22 - L)), 8.4, 8, x_stalk, group=2)
        p.blob(31, 27.8, 5.4, 1.8, x_frond, ang=-20, group=5, flat=1)
        p.blob(27.5, 17 - L, 7.4, 6.6, x_stalk, group=3)
        # the ember in the split of the swollen stem
        p.lens((33, 30), (35.5, 45), 7.6, x_ember, bend=0.8, fat=0.5, group=8)

        # the crown: one bold tier of umbellets fanned over the head
        hub = (30, 13 - L)
        _crown(p, hub, [(19.8, 11.6 - L), (22.2, 7.2 - L), (26.6, 4.6 - L), (32, 4.2 - L), (37.2, 5.4 - L),
                        (41.2, 8.2 - L), (43.2, 12.2 - L)], r=3.2)

        # far frond-arm thrusting the fennel torch high and forward
        p.limb(bez((29, 31), (23, 31), (18.5, 25)), 5.6, 4.4, x_frond, group=21)
        _frond(p, bez((28, 32.5), (22, 35), (16, 33)), 5.4, x_frond)
        _torch(p, (18.5, 28), (13, 17), 16, w=13, sway=-L)
        p.blob(18, 25.2, 2.8, 2.6, x_frond, group=21)

        if p.big:
            p.eye(22, 15 - L, 3, 4, iris="orange", shine="gold2", shine_at=(1, 1))
            p.eye(27, 15 - L, 3, 4, iris="orange", shine="gold2", shine_at=(1, 1))
            p.stroke([(24, 20 - L), (25, 20 - L)], "st0")
        else:
            p.px(23, 16 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x, the stride's lean carried on: the
        # swollen stem cropped by the frame with the ember showing through a
        # crack in its back, the head turned right under the crown, the torch
        # thrust high and forward on the right, the near fronds trailing
        for path, w in ((bez((26, 40), (14, 37), (5, 27)), 10), (bez((25, 44), (13, 46), (4, 41)), 9.4)):
            _frond(p, path, w, x_frond, bias=0.12)
        p.blob(31, 56, 17, 14, x_stalk, ang=-10, group=1)
        p.limb(bez((35, 45), (38, 36), (41.5, 28)), 13, 11, x_stalk, group=2)
        p.blob(36.5, 39, 6.6, 2.1, x_frond, ang=-30, group=5, flat=1)
        p.blob(43, 22, 8.4, 7.6, x_stalk, group=3)
        p.lens((37, 46), (40.5, 63), 6.4, x_ember, bend=-0.6, group=8)
        # fronds falling from the shoulder across the back like a cloak
        for path, w in ((bez((31, 41), (21, 47), (13, 59)), 10), (bez((33, 43), (27, 53), (24, 63)), 8)):
            _frond(p, path, w, x_frond, bias=0.06)
        _crown(p, (41, 17), [(27.5, 14.5), (30.5, 10), (35.5, 7), (41.5, 6), (47, 7.4), (51, 11)], r=3.8)
        p.limb(bez((40, 36), (48, 38), (52, 31)), 6.2, 5, x_frond, group=21)
        _torch(p, (52, 32), (56, 20), 17, w=11)
        p.blob(51.5, 31.5, 3, 2.8, x_frond, group=21)
        if p.big:
            p.eye(47, 20, 3, 4, iris="orange", shine="gold2", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        step = phase
        p.limb(bez((30, 48), (27, 54), (25, 61 - step)), 5.6, 4, x_stalk, group=10)
        p.limb(bez((34, 48), (37, 54), (39, 61 - (1 - step))), 5.6, 4, x_stalk, group=10)
        if view == "up":
            for path, w in ((bez((27, 31), (19, 30), (13, 24)), 8), (bez((37, 31), (45, 30), (51, 24)), 8)):
                _frond(p, path, w, x_frond)
            p.blob(32, 39, 9.6, 9.6, x_stalk, group=1)
            p.limb([(32, 31), (32, 21)], 7.6, 7, x_stalk, group=2)
            p.blob(32, 17, 6.6, 6, x_stalk, group=3)
            p.blob(32, 29, 5.2, 1.7, x_frond, group=5, flat=1)
            _crown(p, (32, 11), [(21, 10), (24.5, 5.5), (29.5, 3.5), (34.5, 3.5), (39.5, 5.5), (43, 10)])
            _torch(p, (45, 30), (47, 20), 12, w=9)
            return
        _frond(p, bez((37, 31), (45, 32), (51, 27 + step)), 7.4, x_frond)
        p.blob(32, 39, 9.6, 9.6, x_stalk, group=1)
        p.lens((32, 31), (32, 46), 6.4, x_ember, group=8)
        p.limb([(32, 31), (32, 21)], 7.6, 7, x_stalk, group=2)
        p.blob(32, 29, 5.2, 1.7, x_frond, group=5, flat=1)
        p.blob(32, 17, 6.6, 6, x_stalk, group=3)
        _crown(p, (32, 11), [(21, 10), (24.5, 5.5), (29.5, 3.5), (34.5, 3.5), (39.5, 5.5), (43, 10)])
        p.limb(bez((27, 31), (20, 30), (16, 25)), 5, 4, x_frond, group=21)
        _torch(p, (16, 27), (14, 18), 12, w=9, sway=step)
        p.eye(28, 15, 3, 4, iris="orange", shine="gold2", shine_at=(1, 1))
        p.eye(33, 15, 3, 4, iris="orange", shine="gold2", shine_at=(1, 1))
        return


MONS = [
    # icon palette 5 keeps the tan stalk and the green fronds apart
    Mon("Narthip", NARTHIP_COLORS, NARTHIP_SHINY, narthip, foot="root", icon_pal=5),
    Mon("Promethex", PROMETHEX_COLORS, PROMETHEX_SHINY, promethex, foot="root"),
]
