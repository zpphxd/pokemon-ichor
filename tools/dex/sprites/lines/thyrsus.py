"""Thyrsus line: Ampelix, Thyrsivy (Grass/Poison). Ampelos, the satyr boy
whose body became the first grapevine, and the maenads' ivy-wound staff
that struck wine from the rock."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Ampelix, the vine tendril
# --------------------------------------------------------------------------

AMPELIX_COLORS = [
    ("ink", INK),
    # the vine: olive, shaded down to cypress
    ("vine0", (40, 56, 24)), ("vine1", (88, 104, 40)), ("vine2", (136, 152, 64)), ("vine3", (192, 200, 112)),
    # the grape-leaf hood, a fresher green
    ("leaf0", (24, 72, 48)), ("leaf1", (40, 120, 64)), ("leaf2", (88, 168, 80)), ("leaf3", (160, 216, 120)),
    # wine-violet grapes
    ("wine0", (72, 32, 80)), ("wine1", (128, 64, 136)), ("wine2", (184, 128, 192)),
    ("white", C.white),
    # the root tuft
    ("root0", (88, 56, 40)), ("root1", (144, 104, 64)),
]
AMPELIX_SHINY = {
    # autumn terracotta leaf, sun-gold grapes
    "leaf0": (120, 48, 24), "leaf1": (184, 88, 48), "leaf2": (224, 136, 88), "leaf3": (248, 192, 136),
    "wine0": (152, 96, 24), "wine1": (208, 152, 48), "wine2": (248, 216, 112),
}

a_vine = Mat(["vine0", "vine1", "vine2", "vine3"], line="vine0", cuts=[0.2, 0.46, 0.74])
a_leaf = Mat(["leaf0", "leaf1", "leaf2", "leaf3"], line="leaf0", cuts=[0.2, 0.46, 0.74])
a_grape = Mat(["wine0", "wine1", "wine2"], line="wine0", cuts=[0.36, 0.7])
a_root = Mat(["root0", "root1"], line="root0", cuts=[0.5])


def helix(cx, yb, r0, r1, height, turns, th0, squash=0.4, n=None):
    """Points of a vine coiled like a spring, from the bottom up. Returns
    [(x, y, depth)], depth > 0 on the near side of the coil."""
    n = n or int(turns * 28)
    out = []
    for i in range(n + 1):
        t = i / n
        th = th0 + 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        out.append((cx + r * math.cos(th), yb - height * t + r * squash * math.sin(th), math.sin(th)))
    return out


def coil(p, pts, w0, w1, mat, near=True, far=True, group0=60, **kw):
    """Draws a helix as tube segments: the far halves of every turn first,
    then the near halves, each near half its own shading group so the turns
    read as stacked loops."""
    n = len(pts) - 1
    runs, cur = [], [0]
    for i in range(1, n + 1):
        if (pts[i][2] >= 0) == (pts[cur[-1]][2] >= 0):
            cur.append(i)
        else:
            cur.append(i)
            runs.append(cur)
            cur = [i]
    if len(cur) > 1:
        runs.append(cur)
    ids = []
    order = [r for r in runs if pts[r[len(r) // 2]][2] < 0] if far else []
    order += [r for r in runs if pts[r[len(r) // 2]][2] >= 0] if near else []
    for k, r in enumerate(order):
        t0, t1 = r[0] / n, r[-1] / n
        is_near = pts[r[len(r) // 2]][2] >= 0
        ids.append(p.limb([(pts[i][0], pts[i][1]) for i in r], w0 + (w1 - w0) * t0, w0 + (w1 - w0) * t1, mat,
                          group=group0 + k, bias=0.0 if is_near else 0.22, **kw))
    return ids


def _curl(p, x, y, r, mat, cw=True, w=2.0, **kw):
    """A tendril's spiral tip around (x, y)."""
    pts = []
    for i in range(19):
        t = i / 18
        a = (math.pi * 1.6 * t) * (1 if cw else -1) + math.pi
        rr = r * (1 - 0.65 * t)
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return p.limb(pts, w, w * 0.7, mat, **kw)


def _grapes(p, x, y, s=1.0, far=False):
    """Three grapes hanging from a short stalk at (x, y)."""
    b = 0.2 if far else 0.0
    p.limb([(x, y), (x + 0.3, y + 2.2 * s)], 1.2, 1.0, a_vine, bias=b)
    r = 2.1 * s
    for gx, gy in ((x - 1.5 * s, y + 3.6 * s), (x + 1.9 * s, y + 3.7 * s), (x + 0.2 * s, y + 6.6 * s)):
        p.circle(gx, gy, r, a_grape, bias=b)
        if p.big:
            p.px(gx - 0.9 * s, gy - 0.9 * s, "white")


# the hood leaf's outline in the battle front, design coordinates: five
# toothed lobes, the brow lobe over the eyes, the petiole notch at the back
HOOD = [(16.5, 35.5), (18.5, 32.5), (17.8, 31.6), (20, 30.6), (19.2, 28.6), (18.6, 27.8), (20.5, 25.4),
        (22.6, 27), (23.7, 26.5), (24.6, 28.4), (26.4, 26), (26.2, 25), (30, 23.4), (32.6, 25),
        (33.8, 24.8), (34.6, 27), (36.5, 28.4), (38.6, 27.6), (39.6, 26.8), (43.6, 29.2), (41.4, 31),
        (42.4, 32.2), (39.6, 32.6), (41.6, 34.6), (40.2, 37.6), (37.4, 35.6), (35.6, 35.2),
        (30, 34.2), (24, 34.3), (20.6, 35.2), (18.6, 36.3)]
# the same leaf seen face-on, for the follower walking toward the camera
HOOD_FRONT = [(32, 22.5), (34.5, 25.5), (35.6, 25), (37, 27.5), (40.5, 25.5), (40.6, 26.6), (43.5, 26.5),
              (41.8, 29.5), (42.8, 30.2), (40.8, 31.5), (42.2, 35.5), (39, 34.2), (36, 33.6), (32, 33.2),
              (28, 33.6), (25, 34.2), (21.8, 35.5), (23.2, 31.5), (21.2, 30.2), (22.2, 29.5), (20.5, 26.5),
              (23.4, 26.6), (23.5, 25.5), (27, 27.5), (28.4, 25), (29.5, 25.5)]


def _hood(p, dx=0.0, dy=0.0, front=False, mirror=None, s=1.0, ox=0.0, oy=0.0):
    pts = HOOD_FRONT if front else HOOD
    if mirror is not None:
        pts = [(mirror - (x - 27.3) * s, oy + (y - 38.6) * s) for x, y in pts]
    return p.poly([(x + dx, y + dy) for x, y in pts], a_leaf, group=80)


def _hood_veins(p, o, tips):
    if not p.big:
        return
    for t in tips:
        p.stroke([o, t], "leaf0")


def ampelix(p, view, phase):
    if view in ("front", "side", "icon"):
        # the battle front is hand-finished in the art files; this draft
        # matches it for the icon and the follower
        L = 1 if (phase == 1 and view == "front") else 0
        hop = 1 if (phase == 1 and view == "side") else 0
        for path in (((21, 58), (18.5, 60.5)), ((26, 59), (25.5, 61)), ((32, 59), (32.5, 61.5)),
                     ((40, 59), (40.5, 61)), ((45, 57.5), (48, 60.5))):
            p.limb(list(path), 2.4, 1.4, a_root, group=5)
        # far tendril arm, raised behind on the right
        p.limb(bez3((35, 45 - L), (38, 44), (39, 42), (41, 41 - L)), 2.0, 1.8, a_vine, bias=0.25, group=40)
        _curl(p, 43, 40.5 - L, 2.2, a_vine, cw=False, w=1.8, bias=0.25, group=40)
        # the coil
        pts = helix(32.3, 53.6 - hop, 12.4, 8.2, 7.6, 1.75, math.pi * 0.62, squash=0.42)
        coil(p, pts, 6.6, 5.2, a_vine)
        # near tendril arm, curling forward from under the chin
        p.limb(bez3((25, 43.5 - L), (22, 44.5), (20, 43), (18.5, 42 - L)), 2.0, 1.8, a_vine, group=41)
        _curl(p, 16.5, 41.5 - L, 2.2, a_vine, cw=True, w=1.8, group=41)
        # neck and head
        p.limb([(32.5, 41 - L), (32.5, 46.5)], 6.0, 6.4, a_vine, group=70)
        p.blob(27.3, 38.6 - L, 8.2, 6.3, a_vine, ang=-6, group=71, bias=-0.06)
        # petiole and hood
        p.limb(bez((37, 28 - L), (39.5, 24 - L), (37, 22.5 - L)), 1.6, 1.3, a_vine, group=79)
        _hood(p, dy=-L)
        _hood_veins(p, (36, 29 - L), [(22, 27 - L), (30, 25 - L), (19, 34 - L), (41, 30 - L), (39, 35 - L)])
        _grapes(p, 44, 50 + hop)
        if p.big:
            p.eye(21, 37 - L, 4, 5, shine="white")
            p.eye(28, 37 - L, 3, 5, shine="white", shine_at=(1, 1))
            p.stroke([(24, 43 - L), (25, 44 - L), (26, 44 - L), (27, 43 - L)], "vine0")
        else:
            p.pxs([(22, 39 - L), (29, 39 - L)], "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x (the hand-finished art replaces
        # this): the top turn of the coil from behind, cropped by the frame,
        # the head turned right in profile under its leaf hood
        pts = helix(29, 69, 19, 13, 16, 1.3, math.pi * 1.05, squash=0.42)
        coil(p, pts, 8.8, 7.2, a_vine)
        p.limb([(35, 42), (35, 50)], 9.0, 9.4, a_vine, group=70)
        p.blob(39, 37.5, 9.8, 7.6, a_vine, ang=6, group=71, bias=-0.06)
        p.limb(bez((27, 27), (24, 23), (26.5, 20.5)), 1.9, 1.6, a_vine, group=79)
        _hood(p, mirror=39, oy=37.5, s=1.2)
        p.limb(bez3((42, 46), (48, 48), (52, 44), (55, 46)), 2.6, 2.2, a_vine, group=41)
        _curl(p, 57, 44, 3.0, a_vine, cw=False, w=2.2, group=41)
        _grapes(p, 12.5, 44, s=1.2)
        if p.big:
            p.eye(42, 35, 4, 5, shine="white", shine_at=(2, 1))
            p.stroke([(44, 42), (46, 41)], "vine0")
        return

    if view in ("down", "up"):
        st = phase
        for path in (((25, 57), (21.5, 60.5)), ((31, 58), (30.5, 61.5)), ((38, 57), (42, 60.5))):
            p.limb(list(path), 2.4, 1.4, a_root, group=5)
        if view == "up":
            _grapes(p, 41, 47 - st)
        pts = helix(32, 54 - st, 10.5, 7, 8 - st, 1.75, math.pi * (0.5 if view == "down" else 1.5), squash=0.42)
        coil(p, pts, 6.0, 4.8, a_vine)
        p.limb(bez3((28, 45 - st), (23, 45), (21, 42), (19.5, 40 - st)), 2.0, 1.8, a_vine, group=41)
        p.limb(bez3((36, 45 - st), (41, 45), (43, 42), (44.5, 40 - (1 - st))), 2.0, 1.8, a_vine, group=42)
        p.limb([(32, 46 - st), (32, 40 - st)], 5.6, 6.0, a_vine, group=70)
        p.blob(32, 37.5 - st, 7.6, 6.2, a_vine, group=71)
        if view == "up":
            p.limb(bez((32, 28 - st), (35, 24 - st), (32.5, 21.5 - st)), 1.6, 1.3, a_vine, group=79)
        _hood(p, dy=1.5 - st, front=True)
        if view == "down":
            p.eye(27, 36 - st, 3, 5, shine="white", shine_at=(1, 1))
            p.eye(34, 36 - st, 3, 5, shine="white", shine_at=(1, 1))
            p.stroke([(31, 42 - st), (32, 42 - st)], "vine0")
        return


# --------------------------------------------------------------------------
# Thyrsivy, the walking thyrsus
# --------------------------------------------------------------------------

THYRSIVY_COLORS = [
    ("ink", INK),
    # pine cone, terracotta-brown; its darkest also shades the stalk
    ("brown0", (72, 40, 32)), ("cone1", (120, 64, 32)), ("cone2", (168, 96, 48)), ("cone3", (216, 144, 72)),
    # fennel stalk, limestone tan
    ("stalk1", (160, 128, 80)), ("stalk2", (208, 184, 128)), ("stalk3", (240, 224, 176)),
    # ivy, olive and cypress
    ("ivy0", (24, 56, 40)), ("ivy1", (48, 96, 48)), ("ivy2", (96, 144, 64)), ("ivy3", (160, 192, 96)),
    # dark wine
    ("wine0", (80, 32, 88)), ("wine1", (144, 72, 152)), ("wine2", (200, 136, 216)),
]
THYRSIVY_SHINY = {
    # sun-gold ivy, and wine running pale marble-white, like milk
    "ivy0": (120, 72, 24), "ivy1": (184, 128, 32), "ivy2": (232, 184, 56), "ivy3": (248, 224, 128),
    "wine0": (152, 144, 152), "wine1": (208, 200, 200), "wine2": (248, 248, 240),
}

t_cone = Mat(["brown0", "cone1", "cone2", "cone3"], line="brown0", cuts=[0.22, 0.48, 0.74])
t_stalk = Mat(["brown0", "stalk1", "stalk2", "stalk3"], line="brown0", cuts=[0.16, 0.44, 0.74])
t_root = Mat(["brown0", "cone1", "stalk1"], line="brown0", cuts=[0.34, 0.66])
t_ivy = Mat(["ivy0", "ivy1", "ivy2", "ivy3"], line="ivy0", cuts=[0.2, 0.46, 0.76])
t_vine = Mat(["ivy0", "ivy1"], line="ivy0", cuts=[0.5])
t_wine = Mat(["wine0", "wine1", "wine2"], line="wine0", cuts=[0.34, 0.66])


def ivy_leaf(a, b, w, bend=0.0):
    """A three-lobed ivy leaf from stalk a to tip b: a broad heart-shaped
    base with two short side lobes and a long pointed middle lobe."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    nx, ny = -uy, ux

    def at(t, side):
        off = bend * math.sin(math.pi * t)
        return (a[0] + dx * t + nx * (side + off), a[1] + dy * t + ny * (side + off))
    h = w / 2
    pts = [at(0.0, 0), at(-0.05, h * 0.55), at(0.12, h * 1.0), at(0.34, h * 0.95), at(0.42, h * 0.62),
           at(0.7, h * 0.42), at(1.0, 0), at(0.7, -h * 0.42), at(0.42, -h * 0.62), at(0.34, -h * 0.95),
           at(0.12, -h * 1.0), at(-0.05, -h * 0.55)]
    return pts


def _ivy(p, a, b, w, bend=0.0, far=False, vein=True, **kw):
    # at icon and follower size the ivy is drawn lighter so it stays green
    lift = 0.0 if p.big else -0.3
    pid = p.poly(ivy_leaf(a, b, p._minw(w), bend), t_ivy, bias=(0.24 if far else kw.pop("bias", 0.0)) + lift, **kw)
    if vein and p.big:
        p.stroke([a, ((a[0] * 3 + b[0] * 2) / 5, (a[1] * 3 + b[1] * 2) / 5)], "ivy0")
    return pid


def _ivy_rope(p, path, w0, w1, leaves, far=False, group=None):
    """An ivy runner along path carrying leaves [(t, side, length, width, angle)]."""
    p.limb(path, w0, w1, t_vine, bias=(0.25 if far else 0.0) + (0.0 if p.big else -0.3), group=group)
    lens = [math.hypot(q[0] - o[0], q[1] - o[1]) for o, q in zip(path, path[1:])]
    tot = sum(lens)
    for t, side, ln, w, ang in leaves:
        dd = t * tot
        for (o, q), l in zip(zip(path, path[1:]), lens):
            if dd <= l or l == lens[-1]:
                k = min(1.0, dd / l) if l else 0
                bx, by = o[0] + (q[0] - o[0]) * k, o[1] + (q[1] - o[1]) * k
                ux, uy = (q[0] - o[0]) / l, (q[1] - o[1]) / l
                break
            dd -= l
        r = math.radians(ang) * side
        vx, vy = ux * math.cos(r) - uy * math.sin(r), ux * math.sin(r) + uy * math.cos(r)
        _ivy(p, (bx, by), (bx + vx * ln, by + vy * ln), w, far=far)


def cone_pts(cx, cy, w, h, rot=0.0, n=44):
    """A pine cone, broad and round at the base, tapering to a blunt tip;
    rot tilts it (degrees, negative leans the tip left)."""
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = math.cos(t), math.sin(t)
        k = 1.0 if y > 0 else (1 - 0.45 * (-y) ** 1.25)
        x, y = x * w / 2 * k, y * h / 2 * (0.92 if y > 0 else 1.08)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def _inside(pts, x, y):
    c = False
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def _scales(p, cx, cy, w, h, rot=0.0, rows=7, per=9, L=0):
    """Paints the shingled scale lattice over a cone_pts cone: rows of
    rounded scales, staggered, foreshortened toward the sides, each with a
    dark lower lip and a lit upper-left edge."""
    if not p.big:
        return
    poly = cone_pts(cx, cy - L, w, h, rot)
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for r in range(rows):
        v = (r + 0.7) / (rows + 0.2)                     # 0 top .. 1 base
        ly = -h / 2 * 1.08 + v * h * 1.0
        yy = ly / (h / 2 * (0.92 if ly > 0 else 1.08))
        half = w / 2 * (1.0 if yy > 0 else (1 - 0.45 * (-yy) ** 1.25)) * math.sqrt(max(0.0, 1 - min(1, yy * yy) * 0.6))
        for c in range(per):
            ph = (c + (0.5 if r % 2 else 0.0)) / per * math.pi * 2 - math.pi
            if math.cos(ph) < 0.15:
                continue
            lx = half * math.sin(ph)
            sw = max(1, round(2.3 * math.cos(ph) ** 0.7 * (0.6 + 0.4 * v)))
            x, y = cx + lx * ca - ly * sa, cy - L + lx * sa + ly * ca
            lip = [(x + i, y + (1 if abs(i) < sw else 0)) for i in range(-sw, sw + 1)]
            if all(_inside(poly, q[0] + 0.5, q[1] + 0.5) for q in lip):
                p.pxs(lip, "brown0")
                if _inside(poly, x - 1.5, y - 1.5):
                    p.px(x - sw + 1, y - 1, "cone3")


def thyrsivy(p, view, phase):
    if view in ("front", "side", "icon") and not p.big:
        # icon and follower size: the same pose in a few broad shapes, so
        # the ivy stays green instead of turning to outline
        L = 1 if (phase == 1 and view == "front") else 0
        sw = 1 if phase == 1 else 0
        st = view == "side" and phase == 1
        p.blob(33.5, 59.8, 14.5, 2.4, t_wine, group=2)
        p.limb(bez3((37, 29), (46, 29), (47, 18), (51, 10 - sw)), 4.0, 3.0, t_ivy, group=30, bias=-0.1)
        p.lens((47, 22), (55, 12 - sw), 8.0, t_ivy, bend=1.0, group=30, bias=-0.1)
        for path, w0 in ((((31, 53), (26, 56), (17, 59.5)), 5.6), (((37, 53), (44, 56.5), (50, 58.5)), 5.6)):
            p.limb(list(path), w0, 2.6, t_root, group=10)
        p.blob(34.2, 53.4, 6.2, 4.4, t_root, group=10)
        p.limb(bez3((34.5, 54 - st), (35, 47), (33.5, 39), (31.5, 31 - L)), 11.0, 9.4, t_stalk, group=20)
        p.blob(31.5, 34 - L, 10.5, 6.0, t_ivy, group=25, bias=-0.25)
        p.poly(cone_pts(29.5, 17 - L, 25, 26.5, rot=-8), t_cone, group=40)
        p.limb(bez3((25, 31 - L), (15, 32 - L), (9, 30), (9, 23 - sw)), 4.4, 3.6, t_ivy, group=31, bias=-0.25)
        p.lens((9, 27 - sw), (7, 14 - sw), 9.0, t_ivy, bend=0.6, group=31, bias=-0.25)
        p.pxs([(21, 18 - L), (30, 18 - L)], "ivy3")
        return

    if view in ("front", "side", "icon"):
        # the battle front is hand-finished in the art files; this draft
        # matches it for the icon and the follower: both ivy arms flung up
        # in the revel, the cone tipped forward
        L = 1 if (phase == 1 and view == "front") else 0
        sw = 1 if phase == 1 else 0
        st = view == "side" and phase == 1
        p.blob(33.5, 59.8, 14.5, 2.0, t_wine, group=2)
        # far ivy arm raised high behind
        _ivy_rope(p, bez3((37, 29), (46, 29), (47, 18), (51, 10 - sw)), 3.0, 2.4,
                  [(0.15, -1, 7, 6.0, 58, ), (0.4, 1, 7, 6.0, 58), (0.65, -1, 7, 6.0, 58), (0.88, 1, 6.5, 5.6, 58),
                   (1.0, 1, 6.5, 5.6, 10)], far=True, group=30)
        for path, w0 in ((((31, 53), (26, 56), (17, 59.5)), 5.0), (((32, 55), (29, 58.5), (26.5, 60.5)), 4.6),
                         (((36, 55), (39, 58.5), (41.5, 60.5)), 4.6), (((37, 53), (44, 56.5), (50, 58.5)), 5.0)):
            p.limb(list(path), w0, 2.0, t_root, group=10)
        p.blob(34.2, 53.4, 5.6, 3.8, t_root, group=10)
        stalk = p.limb(bez3((34.5, 54 - st), (35, 47), (33.5, 39), (31.5, 31 - L)), 10.0, 8.6, t_stalk, group=20)
        for k, y0 in enumerate((52, 45.5, 39)):
            p.limb([(39.5, y0 - 2.6), (34, y0 + 0.2), (29.5, y0 + 2.4)], 2.6, 2.6, t_vine, group=21 + k, clip=[stalk])
        _ivy(p, (38.5, 49), (45, 46), 5.6, bend=0.6)
        _ivy(p, (29.5, 47.5), (23.5, 50), 5.2, bend=-0.6)
        for (a, b, w, bend, far) in (((38, 28.5), (46.5, 32), 7.4, -0.6, True), ((23.5, 29), (15.5, 32.5), 7.2, 0.6, True),
                                     ((36, 30), (42.5, 37.5), 7.6, -0.8, False), ((26.5, 30), (21, 38), 7.6, 0.8, False),
                                     ((31.5, 31), (31.5, 41.5), 8.0, 0.2, False)):
            _ivy(p, (a[0], a[1] - L), (b[0], b[1] - L), w, bend=bend, far=far)
        p.poly(cone_pts(29.5, 17 - L, 25, 26.5, rot=-8), t_cone, group=40)
        _scales(p, 29.5, 17, 25, 26.5, rot=-8, L=L)
        # near ivy arm flung forward and up, a hand of leaves at its end
        _ivy_rope(p, bez3((25, 31 - L), (15, 32 - L), (9, 30), (9, 23 - sw)), 3.4, 2.8,
                  [(0.25, 1, 7, 6.2, 62), (0.5, -1, 7, 6.2, 62), (0.75, 1, 7, 6.2, 62)], group=31)
        for a, b, w in (((9, 23 - sw), (4.5, 18.5 - sw), 6.4), ((9, 23 - sw), (14.5, 19 - sw), 6.0),
                        ((9, 23 - sw), (8.5, 15.5 - sw), 6.8)):
            _ivy(p, a, b, w)
        for x, y, ln in ((21, 27, 3.5), (37, 30, 2.5)):
            p.drop((x, y - L), x, y + ln - L, 1.5, t_wine, group=50)
        if p.big:
            p.patch(18, 14 - L, ["11.......", ".111...11", ".18111.111", ".11111..181", "..1cc1..1cc1",
                                 "..1cb1...1c1", "...11.....1"], {"1": "ink", "c": "ivy3", "b": "ivy2", "8": "stalk3"})
        else:
            p.pxs([(21, 18 - L), (30, 18 - L)], "ivy3")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the stalk cropped by the frame,
        # the ivy ruff from behind, the cone turned right with one leaf-eye
        _ivy_rope(p, bez3((24, 33), (14, 31), (9, 22), (5, 12)), 3.2, 2.4,
                  [(0.2, 1, 7, 6.0, 75), (0.45, -1, 7, 6.0, 80), (0.7, 1, 6.5, 5.6, 70), (0.9, -1, 6, 5.4, 70),
                   (1.0, -1, 6, 5.4, 10)], far=True, group=30)
        stalk = p.limb(bez((27, 68), (28, 52), (31, 34)), 13.0, 11.0, t_stalk, group=20)
        for k in range(3):
            y0 = 60 - k * 9
            p.limb([(20 + k * 0.6, y0 - 2), (35 + k * 0.6, y0 + 3)], 3.2, 3.2, t_vine, group=21 + k, clip=[stalk])
        _ivy(p, (21.5, 55), (14.5, 52), 6.4, bend=-0.6)
        _ivy(p, (34, 47), (41, 45), 6.0, bend=0.6)
        for (a, b, w, bend, far) in (((26, 32), (16, 37), 7.6, 0.6, True), ((40, 31), (49, 36), 7.4, -0.6, True),
                                     ((29, 33), (24, 44), 8.0, 0.8, False), ((37, 33), (42, 43), 7.8, -0.8, False),
                                     ((33, 33), (33, 45), 8.0, 0.0, False)):
            _ivy(p, a, b, w, bend=bend, far=far)
        p.poly(cone_pts(34, 17, 29, 29, rot=10), t_cone, group=40)
        _scales(p, 34, 17, 29, 29, rot=10, rows=8)
        _ivy_rope(p, bez3((41, 32), (51, 33), (55, 41), (52, 50)), 3.2, 2.6,
                  [(0.2, -1, 7, 6.0, 80), (0.45, 1, 7, 6.0, 75), (0.72, -1, 6.5, 5.8, 70)], group=31)
        for a, b, w in (((52, 50), (48, 56), 6.4), ((52, 50), (55.5, 57), 6.4)):
            _ivy(p, a, b, w)
        for x, y, ln in ((26, 30, 3.5), (42.5, 29.5, 4.5)):
            p.drop((x, y), x, y + ln, 1.7, t_wine, group=50)
        if p.big:
            p.patch(42, 15, ["..1111.", ".1aaaa1", "1aa11f1", ".1a11a1", "..1111."], {"1": "ink", "a": "ivy3", "f": "stalk3"})
        return

    if view in ("down", "up"):
        # follower: thumping along on its roots, both ivy arms raised in a V
        st = phase
        p.blob(32, 60.6, 12, 1.8, t_wine, group=2)
        for path in (((30, 55), (24, 59), (20, 61)), ((32, 57), (32, 61.5)), ((34, 55), (40, 59), (44, 61))):
            p.limb(list(path), 4.4, 2.0, t_root, group=10)
        p.blob(32, 55, 5.4, 3.6, t_root, group=10)
        stalk = p.limb([(32, 55), (32, 30 - st)], 9.4, 8.4, t_stalk, group=20)
        for k in range(3):
            y0 = 51 - k * 7
            p.limb([(37, y0 - 2 - st * 0.5), (27, y0 + 2 - st * 0.5)], 2.6, 2.6, t_vine, group=21 + k, clip=[stalk])
        _ivy_rope(p, bez3((27, 30 - st), (18, 30), (14, 24), (14, 16 - st)), 3.0, 2.4,
                  [(0.3, 1, 6.5, 5.8, 62), (0.6, -1, 6.5, 5.8, 62), (1.0, 1, 6.5, 5.8, 10)], group=31)
        _ivy_rope(p, bez3((37, 30 - st), (46, 30), (50, 24), (50, 16 - (1 - st))), 3.0, 2.4,
                  [(0.3, -1, 6.5, 5.8, 62), (0.6, 1, 6.5, 5.8, 62), (1.0, -1, 6.5, 5.8, 10)], group=32)
        for (a, b, w, bend) in (((28, 29), (19.5, 33), 7.0, 0.6), ((36, 29), (44.5, 33), 7.0, -0.6),
                                ((30, 30), (26.5, 39), 7.2, 0.6), ((34, 30), (37.5, 39), 7.2, -0.6),
                                ((32, 30.5), (32, 41), 7.4, 0.0)):
            _ivy(p, (a[0], a[1] - st), (b[0], b[1] - st), w, bend=bend)
        p.poly(cone_pts(32, 17 - st, 23, 25), t_cone, group=40)
        _scales(p, 32, 17, 23, 25, L=st)
        if view == "down":
            p.pxs([(27, 18 - st), (36, 18 - st)], "ivy3")
            p.pxs([(27, 17 - st), (36, 17 - st), (28, 18 - st), (35, 18 - st)], "ink")
        return


MONS = [
    Mon("Ampelix", AMPELIX_COLORS, AMPELIX_SHINY, ampelix, foot="root"),
    # icon palette 5 keeps the cone brown and the ivy green
    Mon("Thyrsivy", THYRSIVY_COLORS, THYRSIVY_SHINY, thyrsivy, foot="root", icon_pal=5),
]
