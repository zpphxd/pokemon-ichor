"""Hexylla (#135), the Sheer Rock: Scylla of the strait.

Concept C, "The Sheer Rock". Homer's smooth, cloud-capped cliff (Odyssey
12.73-100) made one creature. Its body is a great barnacle crag hunched in
the surf: a heavy brow juts over the cave where Scylla lives, and two amber
eyes watch from inside it. The crag's wall plates part at the crown, and
the amber fire that runs in its fissures wells up there into six sea-hound
necks, the barnacle's cirri, that arch out of the crater like a fountain.
The rock's strata climb the necks as barnacle collars before they become
hide. Each head is its own: the lead hound lunges low with its jaws wide,
one snarls, one yelps at the sky, and the far three loom darker out of the
dark cloud that never leaves the peak. Foam breaks at its foot.
"""
import math

from mon_lib import Mat, Mon, bez, bez3, lerp, ellipse_pts, lens_pts, ribbon

COLORS = [
    ("ink", (32, 24, 24)),
    # the crag: barnacle limestone, wet
    ("r0", (64, 56, 72)), ("r1", (104, 96, 104)), ("r2", (152, 144, 144)), ("r3", (208, 200, 184)),
    # the hounds: slate-teal hide shading to a Dark-type indigo
    ("s0", (32, 40, 80)), ("s1", (40, 88, 120)), ("s2", (80, 136, 160)), ("s3", (152, 200, 200)),
    # the cloud on the peak, and the hounds' ear-fins
    ("v0", (64, 48, 104)), ("v1", (112, 96, 152)),
    # the signature glow: amber in the fissures, the eyes and the throats
    ("g0", (168, 64, 24)), ("g1", (232, 136, 32)), ("g2", (248, 224, 120)),
    # foam, wet sheen, fangs
    ("foam", (232, 248, 240)),
]
# The body turns cypress green and the heads turn marble white.
SHINY = {
    "r0": (24, 48, 40), "r1": (40, 88, 56), "r2": (80, 136, 88), "r3": (144, 184, 128),
    "s0": (96, 88, 104), "s1": (160, 152, 152), "s2": (208, 200, 192), "s3": (248, 248, 240),
}

rock = Mat(["r0", "r1", "r2", "r3"], line="r0", cuts=[0.2, 0.46, 0.72])
rock_d = Mat(["s0", "r0", "r1", "r2"], line="s0", cuts=[0.22, 0.5, 0.78])
cave = Mat(["ink", "s0"], line="ink", cuts=[0.6])
skin = Mat(["s0", "s1", "s2", "s3"], line="s0", cuts=[0.2, 0.46, 0.74])
skin_m = Mat(["s0", "s1", "s2"], line="s0", cuts=[0.34, 0.7])
skin_d = Mat(["s0", "s1", "s2"], line="s0", cuts=[0.4, 0.74])
pale = Mat(["s1", "s2", "s3"], line="s1", cuts=[0.4, 0.7])
mouth = Mat(["g0", "g1"], line="g0", cuts=[0.55])
fin = Mat(["v0", "v1"], line="v0", cuts=[0.5])
fin_d = Mat(["s0", "v0"], line="s0", cuts=[0.6])
cloud = Mat(["s0", "v0", "v1"], line="s0", cuts=[0.18, 0.7])
water = Mat(["s0", "s1", "s2", "s3"], line="s0", cuts=[0.2, 0.42, 0.66])
foam_m = Mat(["s2", "s3", "foam"], line="s2", cuts=[0.32, 0.6])
# the small views read better a step lighter
mini = Mat(["s1", "s2", "s3"], line="s0", cuts=[0.42, 0.72])
mini_d = Mat(["s0", "s1", "s2"], line="s0", cuts=[0.4, 0.72])


def path(*segs):
    out = []
    for s in segs:
        if out and s and out[-1] == s[0]:
            s = s[1:]
        out.extend(s)
    return out


# --------------------------------------------------------------------------
# A sea-hound's head, built from curves around the skull center (cx, cy):
# a round skull, a long muzzle tapering to a nose pad, a dropped jaw on a
# glowing throat, a tall pointed ear-fin and a gill-fin behind. f=-1 faces
# left; ang tilts the muzzle up; mouth opens the jaw (0..1).
# --------------------------------------------------------------------------

def hound(p, cx, cy, s=1.0, f=-1, ang=0.0, mouth_open=0.8, mat=None, jaw=None, finm=None, g=80,
          eye=True, ear=1.0, depth=0):
    mat = mat or skin
    jaw = jaw or pale
    finm = finm or fin
    th = math.radians(ang if f < 0 else -ang)
    ca, sa = math.cos(th), math.sin(th)

    def T(lx, ly):
        lx, ly = lx * s, ly * s
        rx, ry = lx * ca - ly * sa, lx * sa + ly * ca
        return (cx + (rx if f < 0 else -rx), cy + ry)

    def TP(pts):
        return [T(x, y) for x, y in pts]
    m = mouth_open
    # gill-fin behind the skull, then the tall ear-fin
    p.poly(TP(lens_pts((3.6, -1.6), (11.0, -6.4 * ear), 4.2, bend=1.0, fat=0.3)), finm, group=g)
    p.poly(TP(lens_pts((0.6, -3.4), (4.6, -15.0 * ear), 5.8, bend=-1.4, fat=0.3)), finm, group=g + 1)
    # the open mouth: a glowing throat between muzzle and jaw
    p.poly(TP([(-1.0, 2.6), (-12.6, 2.4), (-11.6, 4.0 + 3.6 * m), (-6.0, 5.8 + 2.4 * m), (-1.0, 6.0)]), mouth,
           group=g + 2)
    # the lower jaw
    p.poly(TP(ribbon(bez((-2.0, 5.8 + 0.4 * m), (-6.6, 7.0 + 1.8 * m), (-11.4, 5.6 + 3.6 * m), n=10),
                     lambda t: 3.4 - 1.6 * t)), jaw, group=g + 3)
    # skull and cheek
    p.poly(TP(ellipse_pts(0.6, -0.2, 6.0, 5.4)), mat, group=g + 4)
    p.poly(TP(ellipse_pts(2.6, 3.0, 4.4, 3.6)), mat, group=g + 4)
    # the muzzle, tapering along a curved top line to the nose pad
    p.poly(TP(ribbon(bez((-2.2, 0.4), (-8.0, -0.8), (-13.0, 0.8), n=12), lambda t: 7.0 - 3.2 * t)), mat,
           group=g + 5)
    p.poly(TP(ellipse_pts(-13.0, 1.1, 1.9, 1.8)), mat, group=g + 5)
    # pale upper lip along the muzzle's underside
    p.poly(TP(ribbon(bez((-3.6, 2.8), (-8.6, 3.2), (-12.8, 2.4), n=8), lambda t: 1.8 - 0.6 * t)), jaw,
           group=g + 5, noline=True, nooutline=True)
    if not p.big:
        if eye:
            X, Y = T(-4.4, -1.6)
            p.px(X, Y, "g2")
        return

    def at(lx, ly):
        X, Y = T(lx, ly)
        return int(math.floor(X)), int(math.floor(Y))
    d = 1 if f < 0 else -1
    # nose pad
    nx, ny = at(-14.0, 0.2)
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        p.fig.px(nx + dx * d, ny + dy, "ink")
    # fangs, two up and two down, no rows of teeth
    fx, fy = at(-10.6, 3.0)
    p.fig.px(fx, fy, "foam")
    p.fig.px(fx, fy + 1, "foam")
    lx, ly = at(-9.6, 5.4 + 3.0 * m)
    p.fig.px(lx, ly, "foam")
    p.fig.px(lx, ly - 1, "foam")
    # the throat's hot core
    tx, ty = at(-3.0, 4.2 + 0.8 * m)
    p.fig.px(tx, ty, "g2")
    if eye:
        ex, ey = at(-4.6, -1.6)
        rows = ["11...", ".1221", "..11."] if depth < 2 else ["11..", ".121", "..1."]
        for j, r in enumerate(rows):
            r = r if f < 0 else r[::-1]
            for i, c in enumerate(r):
                if c != ".":
                    p.fig.px(ex - 2 + i, ey - 1 + j, {"1": "ink", "2": "g2"}[c])


# --------------------------------------------------------------------------
# The six hounds, hand-pixeled, each its own drawing. Legend: '#' ink,
# '0'-'3' hide dark to light, 'v'/'V' ear-fin, 'm'/'g'/'G' the glowing
# throat, 'w' fang or shine. The far hounds are drawn a step darker.
# --------------------------------------------------------------------------

NEAR = {"#": "ink", "0": "s0", "1": "s1", "2": "s2", "3": "s3", "v": "v0", "V": "v1",
        "m": "g0", "g": "g1", "G": "g2", "w": "foam", "_": "_"}
FAR = NEAR

# the lead hound, lunging at the foe with its jaws wide
LEAD = [
    "...............#......",
    "..............#V#.....",
    ".............#3V#.....",
    ".............#3Vv#....",
    "............#32Vv#....",
    "........####322Vvv#...",
    "......##3333322Vv11#..",
    "....##333332222211110#",
    ".###333322##2222111100#",
    "#33322222#Gg#222111100#",
    "##2222222##222211111100#",
    "##222222222222211111100#",
    ".#11111111111111111100#",
    ".#w#########m#1111100#.",
    "..#w#mmmgggmm#111100#..",
    "...##mggGGgg#1111000#..",
    "...#w##mmmmm#111000#...",
    "...#33w####221100#.....",
    "....##333222211#0#.....",
    "......##########.......",
]
# a sister snarling forward, jaws half open
SNARL = [
    "..........#......",
    ".........#V#.....",
    "........#3Vv#....",
    ".......#32Vv#....",
    "....####32Vv1#...",
    "..##33333221110#.",
    ".#3332##2221110#.",
    "##322#Gg#2211100#",
    "##22222###2111100#",
    ".#1111111111111100#",
    ".#w#######m#11100#",
    "..#mgggGgm#11100#.",
    "..#w#####111100#..",
    "...##3322221100#..",
    ".....#########....",
]
# a sister thrown back, yelping at the sky
HOWL = [
    "..##............",
    ".#33#...........",
    ".#323#..........",
    "#w#323#....###..",
    "#mm#3222#.#VVV#.",
    ".#gm#3222#3VvV#.",
    ".#wGg#3222#2Vv#.",
    "..#mGgm#2#G#2vv#",
    "..#3mgg##222211#",
    "...#3mmg#2221110#",
    "...#32##22221110#",
    "....#322222111100#",
    ".....##322211100#",
    ".......##2211100#",
    ".........######.",
]
# far: peering out between its sisters
PEER = [
    "......#...",
    ".....#V#..",
    "....#2Vv#.",
    "..##22vv#.",
    ".#222#G#1#",
    "#1#2111110#",
    "##111110000#",
    ".#w##0000#.",
    "..##00000#.",
    "....####..",
]
# far: turned back over the shoulder (faces right)
BACKH = [
    "....#.......",
    "...#V#......",
    "..#vV2#.....",
    "..#vv22##...",
    ".#01122222#.",
    "#0011#G#22##",
    "#00111###11#",
    "#0011111111#",
    ".#00#m####w#",
    "..#00#mm#w#.",
    "...#00000#..",
    "....#####...",
]
# far: snapping down out of the cloud (faces right)
SNAP = [
    "..#.........",
    ".#V#........",
    ".#vV##......",
    "#vv2222#....",
    "#0112##2#...",
    "#0011#G#2#..",
    ".#0011###2#.",
    ".#00111111#.",
    "..#0011##w#.",
    "..#001#gm#..",
    "...#00#Gm#..",
    "...#0#w#m#..",
    "....##.##...",
]

# Each hound: its drawing, where the patch sits, where the neck enters the
# skull, the neck's path from the crater and its widths, and its depth
# (0 lead, 1 near, 2 far).
HEADS = [
    dict(rows=LEAD, at=(1, 30), d=0, path=((32, 31), (30, 20), (21, 20), (19, 36)), w=(8.0, 7.2)),
    dict(rows=SNARL, at=(2, 12), d=1, path=((36, 30), (34, 11), (24, 8), (16, 18)), w=(6.8, 5.6)),
    dict(rows=HOWL, at=(30, 1), d=1, path=((42, 30), (43, 24), (43, 18), (42, 13)), w=(6.6, 5.8)),
    dict(rows=PEER, at=(44, 9), d=2, path=((45, 30), (48, 24), (51, 19), (52, 15)), w=(5.2, 4.2)),
    dict(rows=BACKH, at=(49, 1), d=2, path=((47, 30), (50, 20), (50, 12), (50, 8)), w=(5.4, 4.4)),
    dict(rows=SNAP, at=(51, 16), d=2, path=((49, 30), (52, 28), (52, 24), (52, 21)), w=(6.0, 5.0)),
]


def _pneck_path(h):
    sx, sy = h["c"]
    back = 4.6 * h["s"]
    end = (sx + back, sy + 1.2) if h["f"] < 0 else (sx - back, sy + 1.2)
    return bez3(h["root"], h["c1"], h["c2"], end, n=28)


def _pneck(p, k, h, mats):
    """A neck for the parametric (small-view) hounds."""
    pts = _pneck_path(h)
    mat = mats[h["d"]]
    p.limb(pts, h["w"][0], h["w"][1], mat, group=200 + k)
    p.limb(pts[:7], h["w"][0] + 1.6, h["w"][0] + 0.4, rock if h["d"] <= 1 else rock_d, group=260 + k)


def _side(pts, off):
    """The path pushed `off` px toward its lit (upper-left) side."""
    out = []
    for n in range(len(pts)):
        a, b = pts[max(n - 1, 0)], pts[min(n + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        if nx + ny > 0:
            nx, ny = -nx, -ny
        out.append((pts[n][0] + nx * off, pts[n][1] + ny * off))
    return out


def _span(pts, l0, l1):
    """The stretch of a path from l0 to l1 px along it."""
    out, acc = [], 0.0
    for n, q in enumerate(pts):
        if n:
            acc += math.hypot(q[0] - pts[n - 1][0], q[1] - pts[n - 1][1])
        if l0 <= acc <= l1:
            out.append(q)
    return out if len(out) >= 2 else pts[:2]


def _neck(p, h, k, dy=0):
    a, b, c, e = h["path"]
    e = (e[0], e[1] + dy)
    pts = bez3(a, b, c, e, n=28)
    near = h["d"] <= 1
    w0, w1 = h["w"]
    g = 200 + 10 * k
    if near:
        p.limb(pts, w0, w1, Mat(["s0", "s1"], line="s0", cuts=[0.62]), group=g)
        # a tube: lit flank, rim light and a dark underside
        p.limb(_side(pts, w0 * 0.16), w0 * 0.46, w1 * 0.46, Mat(["s2"]), group=g, noline=True, nooutline=True)
        p.limb(_side(pts, w0 * 0.3 - 0.5), 1.0, 1.0, Mat(["s3"]), group=g, noline=True, nooutline=True)
    else:
        p.limb(pts, w0, w1, skin_d, group=g)
    # the crag's wall plates climb the neck as barnacle collars
    p.limb(_span(pts, 0, 2.6), w0 + 0.6, w0 + 0.2, rock if near else rock_d, group=g + 1)
    return pts


def _head(p, h, dx=0, dy=0, rows=None):
    x, y = h["at"]
    p.patch(x + dx, y + dy, rows or h["rows"], NEAR if h["d"] <= 1 else FAR)


# the body: a crag hunched in the surf that narrows upward into the necks
CRAG = path([(16, 60.5)], bez3((16, 60.5), (20, 56), (22.5, 50), (23, 46)),
            bez3((23, 46), (21.6, 43), (22, 40), (24.5, 37)),
            bez3((24.5, 37), (26, 33), (29, 29.5), (33, 28)),
            [(47, 27)],
            bez3((47, 27), (51, 24.6), (56, 24.6), (58.6, 29)),
            bez3((58.6, 29), (61, 34), (61.4, 46), (62.5, 60.5)))
# the wall plates meet at sutures that glow
SUTURE_A = bez3((33, 29), (29, 36), (27.4, 44), (27, 60.5), n=20)
SUTURE_B = bez3((43, 28.4), (42, 37), (44.6, 47), (45.4, 60.5), n=20)
SUTURE_C = bez3((50, 26.4), (53.6, 34), (55.4, 46), (56.6, 60.5), n=20)
PLATES = [
    ([(15, 61)] + SUTURE_A[::-1] + [(30, 27), (24, 33), (21, 44)], -0.1, rock),
    (SUTURE_A + SUTURE_B[::-1], -0.02, rock),
    (SUTURE_B + SUTURE_C[::-1], 0.08, rock),
    (SUTURE_C + [(63, 61), (63, 40), (56, 30)], 0.12, rock_d),
]


def _front(p, phase):
    ph = phase
    big = p.big

    # ---- the far hounds' necks, lost in the cloud that never leaves the peak
    for k in (3, 4, 5):
        _neck(p, HEADS[k], k)
    for cx, cy, rx, ry in ((52, 12, 7.0, 4.5), (58.4, 9.6, 4.0, 3.5), (59.2, 19, 3.6, 5.0), (46.4, 16.4, 3.6, 3.4),
                           (51, 24, 7.4, 4.4), (57.4, 27, 4.0, 2.6)):
        p.blob(cx, cy, rx, ry, cloud, group=2)

    # ---- the crag
    p.poly(CRAG, rock, group=10)
    for k, (pts, bias, mat) in enumerate(PLATES):
        p.add(p.mask(pts) & p.mask(CRAG), mat, group=11 + k, bias=bias, noline=True)
    # the brow jutting over the cave where Scylla lives, and the cave beneath it
    p.blob(30.4, 38.6, 6.2, 1.9, rock, ang=-8, group=16, bias=-0.2)
    p.poly([(25.6, 41.4), (29, 40.4), (34, 40.6), (35.6, 42.6), (33, 45.4), (28.4, 45.8), (25.6, 44.4)], cave,
           group=17)

    # ---- the near hounds rise out of the crown
    for k in (2, 1, 0):
        _neck(p, HEADS[k], k)

    # ---- the crag's wall plates rise between them like the teeth of a crown
    for k, (a, b, w, mat) in enumerate((((27.4, 31.6), (25, 25.4), 3.6, rock), ((34.4, 30.6), (34, 23.6), 3.0, rock),
                                         ((39.4, 30), (39.4, 23.4), 3.0, rock), ((45.6, 30.4), (46.6, 25), 3.2, rock))):
        p.lens(a, b, w, mat, group=300 + k, fat=0.36)

    # ---- the sea at its foot: a surge of foam and spray
    p.poly([(7, 61.6), (10, 57.4), (18, 56), (26, 57.6), (36, 56.6), (46, 57.6), (55, 55.6), (62.6, 56.6),
            (62.6, 61.6)], water, group=400)
    p.limb(bez3((8, 59.6), (10, 54 - ph), (16, 52 - ph), (22, 55.4)), 3.0, 2.0, foam_m, group=401)
    p.limb(bez3((24, 57), (30, 55.4), (36, 56.6), (42, 55.8)), 2.2, 1.8, foam_m, group=402)
    p.limb(bez3((47, 56.4), (52, 53 + ph), (57, 52.4), (62, 54.6)), 2.6, 2.0, foam_m, group=403)
    for k, (cx, cy, r) in enumerate(((7.4, 52.6 - ph, 1.2), (12, 49.4 - ph, 1.0), (60, 49.6 + ph, 1.1))):
        p.circle(cx, cy, r, foam_m, group=410 + k)

    if not big:
        return
    # ---- the heads, hand-pixeled
    for k in (3, 4, 5, 2, 1, 0):
        _head(p, HEADS[k])
    # ---- sutures of amber fire between the plates
    glow = "g2" if ph else "g1"
    for sut, hot in ((SUTURE_A, True), (SUTURE_B, True), (SUTURE_C, False)):
        p.stroke(sut[:-1], "g0")
        if hot:
            p.stroke(sut[3:13], glow)
    # the eyes in the cave
    p.px(27, 42, "g1"); p.px(28, 42, "g2")
    p.px(31, 42, "g2"); p.px(32, 42, "g1")


# --------------------------------------------------------------------------
# Battle back: over the crag's shoulder toward the foe on the right; the
# necks arch over and the lead hound turns into right profile
# --------------------------------------------------------------------------

def _back(p, phase):
    ph = phase
    p.blob(14, 14, 10, 6, cloud, group=2)
    p.blob(6, 22, 5, 4.6, cloud, group=2)
    # far necks
    far = [
        dict(c=(22, 6), s=0.6, f=-1, ang=10, m=0.5, d=2, root=(30, 34), c1=(28, 18), c2=(26, 8), w=(6.0, 5.0)),
        dict(c=(40, 5), s=0.6, f=1, ang=20, m=0.7, d=2, root=(34, 33), c1=(34, 16), c2=(36, 6), w=(6.0, 5.0)),
        dict(c=(8, 30), s=0.6, f=-1, ang=-10, m=0.6, d=2, root=(26, 38), c1=(18, 28), c2=(12, 26), w=(6.0, 5.0)),
    ]
    for k, h in enumerate(far):
        _pneck(p, k + 3, h, {2: skin_d})
        hound(p, *h["c"], s=h["s"], f=h["f"], ang=h["ang"], mouth_open=h["m"], mat=skin_d, jaw=skin_m,
              finm=fin_d, g=100 + 10 * k, depth=2)
    # the crag's back, cropped by the frame
    p.poly(path([(4, 64.5)], bez3((4, 64.5), (6, 52), (12, 42), (22, 37)), [(40, 34)],
                bez3((40, 34), (50, 36), (56, 46), (58, 64.5))), rock, group=10)
    p.poly([(12, 64.5), (16, 48), (26, 39), (30, 40), (24, 52), (24, 64.5)], rock, group=11, noline=True, bias=-0.06)
    near = [
        dict(c=(50, 30), s=0.8, f=1, ang=0, m=0.8, d=1, root=(38, 36), c1=(44, 20), c2=(54, 18), w=(7.6, 6.4)),
        dict(c=(51, 11), s=0.7, f=1, ang=10, m=0.6, d=1, root=(36, 35), c1=(38, 18), c2=(44, 8), w=(6.6, 5.6)),
    ]
    for k, h in enumerate(near):
        _pneck(p, k, h, {1: skin})
        hound(p, *h["c"], s=h["s"], f=h["f"], ang=h["ang"], mouth_open=h["m"], mat=skin, jaw=pale, finm=fin,
              g=140 + 10 * k, depth=1)
    p.poly([(28, 64.5), (30, 50), (36, 40), (44, 42), (50, 54), (52, 64.5)], rock_d, group=12, noline=True)


# --------------------------------------------------------------------------
# Follower views (drawn at the front's scale; the build shrinks them)
# --------------------------------------------------------------------------

def _mini_head(p, cx, cy, s=1.0, f=-1, ang=0.0, mat=None, finm=None, eye=True, mouth_open=True, g=100):
    """A hound's head for the small views: skull, muzzle, ear-fin, a glowing
    throat and one bright eye pixel. f=-1 faces left; ang tilts the muzzle up."""
    mat = mat or skin
    finm = finm or fin
    th = math.radians(ang if f < 0 else -ang)
    ca, sa = math.cos(th), math.sin(th)

    def T(lx, ly):
        lx, ly = lx * s, ly * s
        rx, ry = lx * ca - ly * sa, lx * sa + ly * ca
        return (cx + (rx if f < 0 else -rx), cy + ry)
    p.poly([T(*q) for q in lens_pts((0.6, -2.0), (2.6, -9.0), 3.2, bend=-0.6, fat=0.3)], finm, group=g)
    if mouth_open:
        p.poly([T(*q) for q in lens_pts((-1.6, 2.4), (-7.4, 3.4), 2.4, fat=0.3)], mouth, group=g + 1, flat=1)
    p.poly([T(*q) for q in ellipse_pts(0.4, 0.2, 3.8, 3.4)], mat, group=g + 2)
    p.poly([T(*q) for q in lens_pts((-1.0, 0.6), (-8.6, 1.4), 4.4, fat=0.2)], mat, group=g + 2)
    if eye:
        X, Y = T(-2.0, -1.0)
        p.px(X, Y, "g2")


MINI_FRONT = [
    # (neck root, ctrl, head center, scale, facing, tilt)
    ((34, 36), (26, 24), (15, 41), 1.6, -1, -8),
    ((37, 33), (31, 16), (14, 21), 1.35, -1, 6),
    ((40, 32), (40, 20), (34, 11), 1.3, -1, 36),
    ((36, 33), (30, 18), (23, 9), 1.1, -1, 14),
    ((45, 32), (48, 20), (50, 11), 1.15, 1, 14),
    ((47, 33), (54, 32), (55, 23), 1.2, 1, -14),
]


def _mini(p, phase):
    """Icon and side view: the front, simplified for 32 px."""
    bob = phase
    p.blob(53, 18, 8.4, 6.4, cloud, group=2)
    heads = MINI_FRONT
    for k in (3, 4, 5):
        root, c, hd, sc, f, ang = heads[k]
        hd = (hd[0], hd[1] + (bob if k % 2 else -bob))
        p.limb(bez(root, c, hd, n=14), 6.0, 5.0, mini_d, group=200 + k)
        _mini_head(p, *hd, s=sc, f=f, ang=ang, mat=mini_d, finm=fin_d, g=300 + 10 * k)
    p.poly([(15, 60.5), (19, 48), (24, 39), (30, 33), (46, 31.4), (53, 35), (58, 45), (61.5, 60.5)], rock, group=10)
    p.poly([(27, 41.4), (36, 40.6), (36.6, 46), (28, 46.6)], cave, group=11)
    p.px(29.5, 43.4, "g2")
    p.px(33.5, 43.4, "g2")
    p.stroke([(40, 34), (41, 44), (40, 56)], "g1")
    for k in (2, 1, 0):
        root, c, hd, sc, f, ang = heads[k]
        hd = (hd[0], hd[1] + (bob if k % 2 == 0 else -bob))
        p.limb(bez(root, c, hd, n=14), 8.4 if k == 0 else 7.0, 6.0, mini, group=200 + k)
        _mini_head(p, *hd, s=sc, f=f, ang=ang, mat=mini, g=300 + 10 * k)
    p.poly([(9, 62.5), (12, 56.6), (22, 55), (34, 56.4), (46, 55.4), (56, 54.4), (62.6, 56), (62.6, 62.5)], water,
           group=400)
    p.limb(bez((10, 58.6), (34, 53.6 + bob), (61, 56.6)), 3.0, 2.4, foam_m, group=401)


def _follow(p, phase, back=False):
    """Follower views, drawn at the front's scale: the crag on its surf with the
    six hounds fanned round its crown like a fountain, bobbing in turn."""
    eye = not back
    cx, cy, r = 32.0, 41.0, 21.0
    p.blob(32, 31, 7, 3.6, cloud, group=2)
    fan = [(168, -1, -10), (132, -1, 8), (102, -1, 30), (78, 1, 30), (48, 1, 8), (12, 1, -10)]
    pos = []
    for k, (deg, f, ang) in enumerate(fan):
        a = math.radians(deg)
        dy = (1.4 if (k + phase) % 2 else -1.4)
        pos.append((cx + r * math.cos(a), cy - r * math.sin(a) + dy, f, ang))
    for k in (2, 3, 1, 4, 0, 5):
        hx, hy, f, ang = pos[k]
        far = False
        root = (cx + (k - 2.5) * 1.6, cy - 4)
        mid = ((root[0] + hx) / 2, min(root[1], hy) - 3)
        p.limb(bez(root, mid, (hx, hy), n=14), 7.0, 5.6, mini_d if far else mini, group=200 + k)
        _mini_head(p, hx, hy, s=1.25, f=f, ang=ang, mat=mini_d if far else mini, finm=fin_d if far else fin,
                   eye=eye, mouth_open=eye, g=300 + 10 * k)
    p.poly([(16, 60), (20, 48), (25, 40), (32, 36.4), (39, 40), (44, 48), (48, 60)], rock_d if back else rock,
           group=10)
    if not back:
        p.poly([(27.4, 45), (36.6, 45), (35.6, 49.6), (28.4, 49.6)], cave, group=11)
        p.px(29.6, 47, "g2")
        p.px(33.4, 47, "g2")
    else:
        p.stroke([(32, 38), (31, 48), (32, 58)], "g1")
    w = 1 if phase else 0
    p.poly([(10, 62.5), (14, 57), (32, 58.4 + w), (50, 57), (54, 62.5)], water, group=400)
    p.limb(bez((12, 59.4), (32, 55.4 + w), (52, 59.4)), 2.6, 2.2, foam_m, group=401)


def hexylla(p, view, phase):
    if view == "front":
        _front(p, phase)
    elif view == "back":
        _back(p, phase)
    elif view in ("down", "up"):
        _follow(p, phase, back=view == "up")
    elif view in ("side", "icon"):
        _mini(p, phase)


MONS = [
    Mon("Hexylla", COLORS, SHINY, hexylla, foot="blank"),
]
