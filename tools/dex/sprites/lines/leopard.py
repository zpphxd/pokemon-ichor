"""Leopard line: Botrykit, Oinopard (Poison, Poison/Dark). The wine-loving
leopards that nursed Dionysus and drew his chariot home from the east."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Botrykit, the vine cub
# --------------------------------------------------------------------------

BOTRYKIT_COLORS = [
    ("ink", INK),
    # sun-gold coat
    ("gold0", (152, 88, 32)), ("gold1", (208, 144, 48)), ("gold2", (240, 192, 72)), ("gold3", (248, 224, 136)),
    # limestone belly and muzzle
    ("cream0", (208, 184, 136)), ("cream1", (240, 232, 200)),
    # wine-violet grape spots
    ("wine0", (80, 32, 88)), ("wine1", (136, 72, 152)), ("wine2", (192, 136, 208)),
    # olive ivy collar
    ("ivy0", (40, 72, 32)), ("ivy1", (88, 120, 48)), ("ivy2", (144, 168, 72)),
    ("white", C.white),
    ("rose", (216, 128, 144)),
]
BOTRYKIT_SHINY = {
    # a marble coat, and spots of unripe green fruit
    "gold0": (136, 128, 128), "gold1": (184, 176, 168), "gold2": (216, 208, 200), "gold3": (240, 240, 232),
    "wine0": (56, 80, 32), "wine1": (104, 136, 48), "wine2": (160, 192, 88),
}

k_fur = Mat(["gold0", "gold1", "gold2", "gold3"], line="gold0", cuts=[0.22, 0.48, 0.76])
k_cream = Mat(["cream0", "cream1"], line="gold1", cuts=[0.5])
k_ivy = Mat(["ivy0", "ivy1", "ivy2"], line="ivy0", cuts=[0.34, 0.68])
k_grape = Mat(["wine0", "wine1", "wine2"], line="wine0", cuts=[0.36, 0.7])
k_rose = Mat(["rose"])


def grape_spot(p, x, y, c0="wine0", c1="wine1", c2="wine2", big=False):
    """A grape-cluster spot: a little bunch of berries, darkest at the
    bottom, with a shine on the top berry."""
    if big:
        p.patch(x, y, [".ab.", "abba", "aab.", ".a.."], {"a": c0, "b": c1})
        p.px(x + 1, y, c2)
    else:
        p.patch(x, y, ["ab", "aa", ".a"], {"a": c0, "b": c1})


def ivy_leaf(a, b, w, bend=0.0):
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d, dx / d

    def at(t, side):
        off = bend * math.sin(math.pi * t)
        return (a[0] + dx * t + nx * (side + off), a[1] + dy * t + ny * (side + off))
    h = w / 2
    return [at(0.0, 0), at(-0.05, h * 0.55), at(0.12, h * 1.0), at(0.34, h * 0.95), at(0.42, h * 0.62),
            at(0.7, h * 0.42), at(1.0, 0), at(0.7, -h * 0.42), at(0.42, -h * 0.62), at(0.34, -h * 0.95),
            at(0.12, -h * 1.0), at(-0.05, -h * 0.55)]


def _collar(p, cx, cy, rx, ry, mat, n=7, ln=4.6, w=4.2, front=True, L=0, group=60, far_bias=0.24):
    """A ring of ivy leaves around a neck centered at (cx, cy): leaves on the
    far side first (darker), then the near ones, tips pointing down and out."""
    ids = []
    leaves = []
    for i in range(n):
        a = math.pi * (0.05 + 0.9 * i / (n - 1))       # 0 = right, pi = left, along the near arc
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a) - L
        ox, oy = math.cos(a) * 0.55, 0.85
        d = math.hypot(ox, oy)
        leaves.append(((x, y), (x + ox / d * ln, y + oy / d * ln)))
    for k, (a, b) in enumerate(leaves):
        ids.append(p.poly(ivy_leaf(a, b, w, bend=0.4 * (1 if k % 2 else -1)), mat, group=group + k))
    return ids


def botrykit(p, view, phase):
    if view in ("front", "side", "icon"):
        # the battle front is hand-finished in the art files; this draft
        # matches it for the icon and the follower
        L = 1 if (phase == 1 and view == "front") else 0
        B = 2 if (phase == 1 and view != "side") else 0
        hop = 1 if (phase == 1 and view == "side") else 0
        p.limb(bez3((44, 57), (54, 58), (55, 47), (50.5, 42.5)), 4.0, 3.2, k_fur, group=20)
        p.limb(bez3((50.5, 42.5), (48, 40.5), (46, 42.5), (48, 44.5)), 3.2, 2.8, k_fur, group=20)
        p.poly(bez3((30.5, 33 - L), (31, 28.5 - L), (34.5, 26 - L), (36.8, 32.5 - L)) + [(34, 35 - L)], k_fur,
               group=5, bias=0.12)
        p.blob(40.5, 53.5 - hop, 7.4, 6.6, k_fur, group=1)
        body = p.blob(30.5, 51.5 - hop, 7.2, 8.2, k_fur, group=1)
        p.blob(28.5, 54.5 - hop, 4.0, 5.0, k_cream, clip=[body], group=2)
        p.limb([(33.5, 51), (34, 58)], 5.2, 4.8, k_fur, group=10, bias=0.2)
        p.blob(34.5, 59.3, 3.3, 1.9, k_fur, group=10, bias=0.2)
        p.blob(42.5, 59.4, 4.8, 1.9, k_fur, group=11)
        p.blob(26.5, 37.8 - L, 9.8, 8.2, k_fur, group=3)
        p.blob(35, 42.5 - L, 2.8, 2.6, k_fur, group=3)
        p.blob(19, 43 - L, 3.0, 2.4, k_fur, group=3)
        p.blob(18.2, 41.5 - L, 5.0, 3.3, k_cream, group=4)
        p.poly(bez3((16.5, 33.5 - L), (15.5, 29 - L), (17.5, 26 - L), (20, 26.5 - L)) + [(24.5, 31.5 - L), (21, 34 - L)],
               k_fur, group=6)
        for a, b, w in (((35.5, 46.2), (38.5, 51.5), 5.8), ((32, 47), (33.5, 52.8), 6.0), ((28.5, 47), (28, 53), 6.0),
                        ((25, 46.4), (22.5, 51.6), 5.8)):
            p.poly(ivy_leaf(a, b, w, 0.4), k_ivy, group=60)
        p.limb(bez3((27.5, 49), (24.5, 53), (21, 52.5 - B / 2), (18.5, 49.5 - B)), 5.6, 5.0, k_fur, group=12)
        p.blob(16.6, 48.2 - B, 3.4, 3.1, k_fur, group=12)
        if p.big:
            p.eye(19, 35 - L, 4, 6, iris="wine1", shine="white", shine_at=(2, 1))
            p.eye(27, 35 - L, 3, 6, iris="wine1", shine="white", shine_at=(1, 1))
            p.pxs([(13, 39 - L), (14, 39 - L), (13, 40 - L), (14, 40 - L)], "rose")
            for x, y, b in ((38, 48, True), (42, 52, True), (36, 54, False), (45, 49, False)):
                grape_spot(p, x, y, big=b)
        else:
            p.pxs([(20, 37 - L), (28, 37 - L)], "ink")
            p.px(13, 39 - L, "rose")
            p.pxs([(40, 50), (43, 54)], "wine1")
        return

    if view == "back":
        # over the shoulder: the cub from behind, sitting, head turned right
        p.limb(bez3((30, 66), (8, 64), (6, 50), (12, 44)), 4.4, 3.4, k_fur, group=20)
        p.limb([(12, 44), (15, 42), (17, 45), (14.5, 46.5)], 3.4, 2.8, k_fur, group=20)
        p.blob(30, 64, 19, 14, k_fur, group=1)
        p.blob(34, 48, 12, 10, k_fur, group=1)
        p.poly([(29, 27), (30, 17), (37, 25)], k_fur, group=5, bias=0.12)
        p.blob(39.5, 33, 11.4, 10, k_fur, group=3)
        p.blob(49, 37.5, 5.4, 4.0, k_cream, group=4)
        p.poly([(42, 24), (48, 16.5), (50, 26)], k_fur, group=6)
        _collar(p, 37, 42, 11, 3.4, k_ivy, n=8, ln=5.6, w=5.4)
        if p.big:
            p.pxs([(47, 19), (47, 20), (48, 21), (46, 21), (47, 22)], "rose")
            p.eye(44, 30, 3, 5, iris="wine1", shine="white", shine_at=(1, 1))
            p.pxs([(53, 35), (54, 35), (53, 36)], "rose")
            p.pxs([(51, 38), (52, 39)], "gold0")
            for x, y, b in ((20, 50, True), (27, 47, False), (25, 55, True), (36, 52, True), (16, 58, False),
                            (31, 59, False), (42, 56, False)):
                grape_spot(p, x, y, big=b)
        return

    if view in ("down", "up"):
        st = phase
        if view == "up":
            p.limb(bez3((32, 54), (40, 56), (44, 46), (40, 41 - st)), 3.2, 2.6, k_fur, group=20)
        p.blob(32, 50, 8.4, 8.4, k_fur, group=1)
        if view == "down":
            p.blob(32, 52, 4.6, 5.6, k_cream, group=2)
        p.limb([(28, 52), (27.5, 59 - 2 * st)], 4.6, 4.4, k_fur, group=12)
        p.limb([(36, 52), (36.5, 59 - 2 * (1 - st))], 4.6, 4.4, k_fur, group=13)
        p.blob(27.5, 59.6 - 2 * st, 3.2, 2.0, k_fur, group=12)
        p.blob(36.5, 59.6 - 2 * (1 - st), 3.2, 2.0, k_fur, group=13)
        p.poly(bez3((21, 32), (20, 26), (22.5, 23.5), (25, 24.5)) + [(28.5, 29)], k_fur, group=5)
        p.poly(bez3((43, 32), (44, 26), (41.5, 23.5), (39, 24.5)) + [(35.5, 29)], k_fur, group=6)
        p.blob(32, 35, 10.5, 8.4, k_fur, group=3)
        _collar(p, 32, 42.5, 7.6, 2.2, k_ivy, n=7)
        if view == "down":
            p.blob(32, 39.5, 4.4, 3.0, k_cream, group=4)
            p.eye(25, 32, 3, 5, iris="wine1", shine="white", shine_at=(1, 1))
            p.eye(36, 32, 3, 5, iris="wine1", shine="white", shine_at=(1, 1))
            p.pxs([(31, 38), (32, 38), (31.5, 39)], "rose")
            p.pxs([(23, 26), (23, 27), (24, 28), (40, 26), (40, 27), (39, 28)], "rose")
        else:
            for x, y in ((27, 46), (34, 48), (30, 53)):
                grape_spot(p, x, y, big=True)
        return


# --------------------------------------------------------------------------
# Oinopard, the panther of Dionysus
# --------------------------------------------------------------------------

OINOPARD_COLORS = [
    ("ink", INK),
    # black-figure coat with a violet sheen
    ("coat0", (40, 32, 56)), ("coat1", (56, 48, 80)), ("coat2", (80, 72, 112)), ("coat3", (128, 120, 168)),
    # sun-gold grape-cluster rosettes
    ("ros0", (184, 128, 40)), ("ros1", (240, 192, 72)),
    # half-lidded gold eyes
    ("eye", (248, 224, 104)),
    ("ivy0", (32, 64, 32)), ("ivy1", (72, 112, 48)), ("ivy2", (136, 168, 72)),
    ("wine0", (88, 32, 96)), ("wine1", (152, 72, 160)), ("wine2", (208, 144, 224)),
    ("white", C.white),
]
OINOPARD_SHINY = {
    # a sun-gold coat with ink-black rosettes, like a vase painting
    "coat0": (144, 80, 32), "coat1": (200, 128, 48), "coat2": (232, 176, 72), "coat3": (248, 224, 144),
    "ros0": (40, 32, 32), "ros1": (80, 64, 56),
}

o_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.12, 0.36, 0.64])
o_ivy = Mat(["ivy0", "ivy1", "ivy2"], line="ivy0", cuts=[0.34, 0.68])
o_vine = Mat(["ivy0", "ivy1"], line="ivy0", cuts=[0.5])
o_grape = Mat(["wine0", "wine1", "wine2"], line="wine0", cuts=[0.36, 0.7])


def rosette(p, x, y, big=True):
    """A grape-cluster rosette: a ring of gold berries round a dark heart."""
    if big:
        p.patch(x, y, [".ab.", "b..a", "a..a", ".aa."], {"a": "ros0", "b": "ros1"})
    else:
        p.patch(x, y, ["ba", "a."], {"a": "ros0", "b": "ros1"})


def _bunch(p, x, y, s=1.0, far=False):
    """A bunch of grapes hanging from (x, y)."""
    b = 0.2 if far else 0.0
    p.limb([(x, y), (x + 0.5, y + 2.4 * s)], 1.4, 1.2, o_vine, bias=b)
    r = 1.9 * s
    for gx, gy in ((x - 1.8, y + 3.8), (x + 1.9, y + 4.0), (x + 0.1, y + 5.4), (x - 1.6, y + 7.2),
                   (x + 1.9, y + 7.4), (x + 0.2, y + 10.0)):
        p.circle(x + (gx - x) * s, y + (gy - y) * s, r, o_grape, bias=b)
        if p.big:
            p.px(x + (gx - x) * s - 0.8, y + (gy - y) * s - 0.8, "white")


def _garland(p, path, leaves, far=False, group=70):
    """A thick ivy garland: a cord along path covered by overlapping leaves
    [(t, side, length, width, angle)]."""
    p.limb(path, 3.0, 3.0, o_vine, group=group, bias=0.2 if far else 0.0)
    lens = [math.hypot(q[0] - o[0], q[1] - o[1]) for o, q in zip(path, path[1:])]
    tot = sum(lens)
    for k, (t, side, ln, w, ang) in enumerate(leaves):
        dd = t * tot
        for (o, q), l in zip(zip(path, path[1:]), lens):
            if dd <= l or l == lens[-1]:
                kk = min(1.0, dd / l) if l else 0
                bx, by = o[0] + (q[0] - o[0]) * kk, o[1] + (q[1] - o[1]) * kk
                ux, uy = (q[0] - o[0]) / l, (q[1] - o[1]) / l
                break
            dd -= l
        r = math.radians(ang) * side
        vx, vy = ux * math.cos(r) - uy * math.sin(r), ux * math.sin(r) + uy * math.cos(r)
        p.poly(ivy_leaf((bx, by), (bx + vx * ln, by + vy * ln), w, bend=0.4 * side), o_ivy,
               group=group + 1 + k, bias=0.2 if far else 0.0)


def oinopard(p, view, phase):
    if view in ("front", "side", "icon"):
        # the battle front is hand-finished in the art files; this draft
        # matches it for the icon and the follower: a prowl, head low,
        # tail raised in an S with its grapes
        L = 1 if (phase == 1 and view == "front") else 0
        sw = 1 if phase == 1 else 0
        walk = view == "side" and phase == 1
        p.limb(bez3((54, 30), (61, 26), (61, 15), (55, 12 - sw)), 5.2, 3.4, o_coat, group=20)
        p.limb(bez3((55, 12 - sw), (52, 10.5 - sw), (49.5, 11.5 - sw), (49, 14.5 - sw)), 3.4, 3.0, o_coat, group=20)
        _bunch(p, 49, 15.5 - sw)
        ff = (bez3((29, 39), (30, 45), (30.5, 51), (30.5, 58)) if walk else bez3((29, 39), (32.5, 45), (34, 51), (35, 58)))
        fh = (bez3((45, 37), (45, 44), (45, 51), (45.5, 58)) if walk else bez3((45, 37), (42.5, 44), (41.5, 51), (41, 58)))
        for k, path in enumerate((ff, fh)):
            p.limb(path, 7.2, 4.4, o_coat, group=10 + k, bias=0.25)
            p.blob(path[-1][0] + 1, 59.3, 3.2, 1.7, o_coat, group=10 + k, bias=0.25)
        outline = (bez3((20, 30), (23, 24), (30, 24), (34, 28)) + bez3((34, 28), (39, 30.5), (44, 25), (50, 25.5))[1:]
                   + bez3((50, 25.5), (56, 26), (58, 34), (55, 40))[1:] + bez3((55, 40), (51, 43), (46, 42), (42, 41))[1:]
                   + bez3((42, 41), (36, 42.5), (30, 45.5), (24, 44))[1:] + bez3((24, 44), (18, 42.5), (17, 35), (20, 30))[1:])
        p.poly(outline, o_coat, group=1)
        p.poly(bez3((24, 27.5 - L), (19, 28 - L), (15, 30 - L), (13, 32 - L)) + bez3((14, 41 - L), (18, 43), (21, 44), (24, 42)),
               o_coat, group=2)
        p.blob(12.5, 34.5 - L, 8.0, 7.2, o_coat, group=3)
        p.blob(12, 38.5 - L, 7.0, 4.2, o_coat, group=3)
        p.poly(bez3((8.5, 34 - L), (5.5, 34 - L), (3, 35.5 - L), (3, 37.5 - L))
               + bez3((3, 37.5 - L), (3.3, 40.5 - L), (7, 41.5 - L), (10, 40.5 - L)) + [(10, 36 - L)], o_coat, group=3)
        p.poly(bez3((7, 30.5 - L), (5.5, 22 - L), (10.5, 19.5 - L), (14, 28 - L)), o_coat, group=4)
        p.poly(bez3((14.5, 28.5 - L), (15, 21 - L), (20.5, 21 - L), (20, 30 - L)), o_coat, group=4, bias=0.15)
        nf = (bez3((23.5, 35), (23.5, 42), (23.5, 50), (24, 58)) if walk else bez3((23.5, 35), (21, 44), (19, 51), (17.8, 58)))
        p.limb(nf, 9.0, 5.4, o_coat, group=12)
        p.blob(nf[-1][0] - 1.5, 59.2, 4.8, 2.2, o_coat, group=12)
        p.poly(bez3((46, 31), (50, 26.5), (57.5, 30), (57, 39)) + bez3((57, 39), (56.5, 43), (54.5, 45), (52.5, 44)) + [(47, 39)],
               o_coat, group=13)
        nh = (bez3((54, 43), (53, 48), (52.5, 53), (52.5, 58.5)) if walk else bez3((54, 43), (55.5, 49), (55.5, 54), (59.5, 58.6)))
        p.limb(nh, 5.6, 3.8, o_coat, group=13)
        _garland(p, bez3((30, 24.5 - L), (28.5, 37), (22.5, 44.5), (14.5, 41 - L)),
                 [(0.0, -1, 7, 6.4, 55), (0.17, 1, 7, 6.4, 55), (0.33, -1, 7, 6.4, 55), (0.5, 1, 7, 6.4, 55),
                  (0.67, -1, 7, 6.4, 55), (0.83, 1, 7, 6.4, 55), (1.0, -1, 7, 6.4, 55)])
        if p.big:
            p.patch(7, 31 - L, ["...111..11", ".11281.181", "1288811881", "18811...11", ".11......."],
                    {"1": "ink", "8": "eye", "2": "coat0"})
            for x, y in ((32, 27), (39, 30), (45, 27), (36, 35), (49, 31), (53, 36)):
                p.patch(x, y, [".7.", "6.6", ".6."], {"6": "ros0", "7": "ros1"})
        else:
            p.pxs([(9, 33 - L), (16, 33 - L)], "eye")
            p.pxs([(36, 29), (44, 28), (48, 33)], "ros1")
        return

    if view == "back":
        # over the shoulder: the panther's back and haunch, cropped by the
        # frame; the garland slung over the shoulders, the tail swinging up
        # with its grapes, the head turned right in profile, low
        p.limb(bez3((14, 54), (3, 48), (3, 32), (11, 25)), 6.2, 4.2, o_coat, group=20)
        p.limb(bez((11, 25), (15, 22), (17, 26)), 4.2, 3.4, o_coat, group=20)
        p.limb(bez3((4, 40), (1.5, 34), (5, 29), (9, 30)), 1.6, 1.4, o_vine, group=21)
        _bunch(p, 17, 26, s=1.2)
        p.blob(28, 62, 24, 15, o_coat, group=1)
        p.blob(40, 46, 13, 10, o_coat, group=1)
        p.blob(33, 41, 8, 6, o_coat, group=1)
        p.limb(bez((42, 42), (47, 38), (49, 34)), 12, 10.5, o_coat, group=2)
        p.blob(50, 31, 8.6, 7.6, o_coat, group=3)
        p.blob(51.5, 35, 7.0, 4.6, o_coat, group=3)
        p.blob(57.5, 34.5, 4.2, 3.4, o_coat, group=3, bias=-0.05)
        p.poly(bez3((43.5, 27), (42.5, 21.5), (47, 21), (48.5, 26)), o_coat, group=4, bias=0.18)
        p.poly(bez3((49, 25.5), (50, 20.5), (54.5, 21), (54, 27)), o_coat, group=4)
        _garland(p, bez3((30, 40), (35, 50), (44, 55), (54, 49)),
                 [(0.0, 1, 6, 5.6, 65), (0.12, -1, 7, 6.2, 80), (0.25, 1, 7, 6.2, 65), (0.38, -1, 7, 6.2, 80),
                  (0.5, 1, 7, 6.2, 65), (0.62, -1, 7, 6.2, 80), (0.75, 1, 7, 6.2, 65), (0.88, -1, 6.5, 5.8, 75),
                  (1.0, 1, 6, 5.4, 30)])
        if p.big:
            p.patch(52, 29, ["1111", "1ee1", ".11."], {"1": "ink", "e": "eye"})
            p.pxs([(61, 33), (61, 34), (60, 33)], "ink")
            for x, y, b in ((14, 50, True), (21, 45, True), (26, 53, True), (19, 58, True), (36, 39, True),
                            (42, 41, False), (32, 59, True), (10, 59, False), (41, 61, True), (28, 46, False),
                            (7, 52, False)):
                rosette(p, x, y, big=b)
        return

    if view in ("down", "up"):
        # follower: prowling toward or away from the camera, the garland
        # across the chest, the tail raised with its grapes
        st = phase
        if view == "up":
            p.limb(bez3((32, 48), (42, 48), (45, 36), (39, 29 - st)), 4.4, 3.2, o_coat, group=20)
            _bunch(p, 38, 29.5 - st)
        p.blob(32, 47, 8.6, 9, o_coat, group=1)
        p.limb([(27.5, 50), (27, 59 - 2 * st)], 6.4, 5.2, o_coat, group=12)
        p.limb([(36.5, 50), (37, 59 - 2 * (1 - st))], 6.4, 5.2, o_coat, group=13)
        p.blob(27, 59.6 - 2 * st, 3.6, 2.1, o_coat, group=12)
        p.blob(37, 59.6 - 2 * (1 - st), 3.6, 2.1, o_coat, group=13)
        p.poly(bez3((24.5, 34), (22, 28.5), (26, 27), (29, 31)), o_coat, group=5)
        p.poly(bez3((35, 31), (38, 27), (42, 28.5), (39.5, 34)), o_coat, group=5)
        p.blob(32, 36.5, 9, 7.6, o_coat, group=3)
        if view == "down":
            p.blob(32, 41, 4.6, 3.4, o_coat, group=4, bias=-0.1)
            _garland(p, bez((23, 43), (32, 52), (41, 43)),
                     [(0.0, 1, 5.5, 5.0, 70), (0.25, -1, 6, 5.4, 80), (0.5, 1, 6, 5.4, 90), (0.75, -1, 6, 5.4, 80),
                      (1.0, 1, 5.5, 5.0, 70)])
            p.patch(26, 34, ["111...111", "181...181"], {"1": "ink", "8": "eye"})
            p.pxs([(31, 40), (32, 40)], "ink")
        else:
            _garland(p, bez((23, 41), (32, 46), (41, 41)),
                     [(0.0, 1, 5, 4.6, 70), (0.5, -1, 5.5, 5.0, 90), (1.0, 1, 5, 4.6, 70)])
            for x, y in ((27, 46), (34, 48), (30, 52)):
                rosette(p, x, y)
        return


MONS = [
    # icon palette 3 keeps the coat sun-gold rather than orange or olive
    Mon("Botrykit", BOTRYKIT_COLORS, BOTRYKIT_SHINY, botrykit, foot="paw", icon_pal=3),
    # icon palette 0 keeps the grapes violet on the black coat
    Mon("Oinopard", OINOPARD_COLORS, OINOPARD_SHINY, oinopard, foot="bigpaw", icon_pal=0),
]
