"""Hydra line: Lernip, Trilerna, Lernathan (Dragon/Poison pseudo-legendary).
The Lernaean Hydra, raised by Hera in the marsh of Lerna: cut off one head
and two grow back, and the middle head can never die.

Concept C, "The Branching": an upright marsh dragon whose single neck forks
like a tree and forks again. Every fork is a healed cut, sealed with a seam of
violet regrowth-light. Lernip has one head, a forked bud at the root of its
neck and a gold freckle on its brow (the immortal head, not yet awake);
Trilerna's trunk splits into three, the middle head budding gold; on
Lernathan the trunk splits, splits again, and the golden immortal head rises
crowned above four green ones.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3, lerp, ellipse_pts, lens_pts, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# One palette family for the whole line: five marsh greens (cypress shadow to
# a wet olive sheen), a limestone belly, venom violet, sun-gold, white.
# --------------------------------------------------------------------------

GREENS = [("g0", (16, 48, 48)), ("g1", (32, 88, 64)), ("g2", (64, 136, 72)), ("g3", (128, 184, 80)),
          ("g4", (200, 224, 136))]
BELLY = [("b0", (176, 152, 104)), ("b1", (232, 216, 160))]
VIOLET = [("v0", (72, 24, 96)), ("v1", (152, 64, 192)), ("v2", (224, 160, 248))]
GOLD = [("o0", (168, 104, 24)), ("o1", (232, 176, 48)), ("o2", (248, 232, 136))]
COLORS = [("ink", INK)] + GREENS + BELLY + VIOLET + GOLD + [("white", (248, 248, 232))]

# legend for hand-placed patches
HL = {"#": "ink", "0": "g0", "1": "g1", "2": "g2", "3": "g3", "4": "g4", "b": "b0", "B": "b1",
      "v": "v0", "V": "v1", "u": "v2", "o": "o0", "y": "o1", "Y": "o2", "w": "white", "_": "_"}

# Hand-drawn heads, facing left (mirrored to face right). The patch
# legend is HL; _stamp darkens a head for depth and mirrors it. GHEAD is the
# immortal head: a crowned dragon, its horns radiating from brow and skull
# like a diadem, a lit brow, a glowing violet eye.
GHEAD = [
    ".............#............",
    "............#Y#...........",
    "...#........#Yw#.....##...",
    "..#Y#.......#YY#....#Yw#..",
    "..#Yw#......#Yyo#..#YYy#..",
    "...#YY#.....#Yyo#.#YYyo#..",
    "....#YY#...#YYyo##YYyo#.##",
    ".....#YY#..#YYyo#YYyo#.#Yw",
    "......#YY##YYyyoYYyo#.#YYy",
    "..###..#YYYYYyyyyyo##YYyo#",
    ".#YYY###YYYYYYyyyyyYYyoo#.",
    "#YwwwwYYYYwwYYYyyyyyyoo#..",
    "#YYYYYYYYYY##YYYyyyyoooo#.",
    "#YYYYYYYY##uw#YYyyyyoooo#.",
    "#YYYYYYYYY#Vuu#yyyyyooooo#",
    "#Y#YYYYyyyy###yyyyyyooooo#",
    "#yyyyyyyyyyyyyyyyyyyoooo#.",
    "#o###############yyyooooo#",
    ".#w#oyyyyyyyyyyy#oyyoooo#.",
    "..##oooooooooooo#oyyyoo#..",
    "....############YYyyyoo#..",
]
HEAD_MC = [
    "..............###..",
    "...........###uVV#.",
    "........####VVVv#..",
    "......##344#Vvv#...",
    "....##3443333#v##..",
    "...#3443###22##Vv#.",
    "..#3433#Y#y#222#v#.",
    ".#3333#3y#o#2211#..",
    "#3#33333###221100#.",
    "#33############100#",
    ".#BwBBBBbbbbb#000#.",
    "..############.##..",
]
HEAD_MO = [
    "..............###..",
    "...........###uVV#.",
    "........####VVVv#..",
    "......##344#Vvv#...",
    "....##3443333#v##..",
    "...#3443###22##Vv#.",
    "..#3433#Y#y#222#v#.",
    ".#3333#3y#o#2211#..",
    "#3#33333#w##21100#.",
    "#33####w#vvvv#1100#",
    ".##vvvvvVVV#11100#.",
    "...#w#Bbbbb##000#..",
    "..#BBBBBbb#0000#...",
    "...########.###....",
]
HEAD_SC = [
    "...........###...",
    ".........##uV#...",
    "......####VVv#...",
    "....##344#Vv##...",
    "..##34433###v#...",
    ".#3443##Y#y#2#V#.",
    "#3433#3#y#o#210#.",
    "#3#3333###221100#",
    "#33###########10#",
    ".#BwBBBbbbbbb#0#.",
    "..############.#.",
]
HEAD_SO = [
    "...........###...",
    ".........##uV#...",
    "......####VVv#...",
    "....##344#Vv##...",
    "..##34433###v#...",
    ".#3443##Y#y#2#V#.",
    "#3433#3#y#o#210#.",
    "#3#3333#w##21100#",
    "#33###w#vvvv#110#",
    ".##vvvvvVVV#1100#",
    "...#w#Bbbbb#000#.",
    "..#BBBBbb##000#..",
    "...########.##...",
]
HEAD_SR = [
    ".........###.....",
    ".......##uV#.....",
    "...###.#VVv#.....",
    "..#344#Vv##......",
    ".#3443333#v#.....",
    ".#443#yY#22#V#...",
    "#3433#Yy#2221#...",
    "#33#3###22211#...",
    "#3##w#22221100#..",
    "#3#vvv#222110#...",
    ".#vvVV#22110#....",
    ".#wvvVV#2100#....",
    "..#BBbbb#100#....",
    "...#BBb##00#.....",
    "....###.###......",
]
HEAD_RO = [
    "..##...........",
    ".#34#..........",
    "#3443##........",
    "#34433###......",
    ".#34443333##.##",
    ".#w#3333#y#uV#.",
    "#vv##333yY#Vv#.",
    "#Vvv##333#2#v#.",
    ".#vVv#22222#V#.",
    "#w#vV#222211#..",
    "#BB#v#2221100#.",
    ".#BB##2211100#.",
    "..#BBb#11100#..",
    "...##bb#000#...",
    ".....####0#....",
    ".........#.....",
]
HEAD_TC = [
    "..............###..",
    ".......##..###uVV#.",
    "......#Yw#####VVv#.",
    "......#Yyo#4#Vvv#..",
    "....##3#oo#333#v##.",
    "...#3443###22##Vv#.",
    "..#3433#Y#y#222#v#.",
    ".#3333#3y#o#2211#..",
    "#3#33333###221100#.",
    "#33############100#",
    ".#BwBBBBbbbbb#000#.",
    "..############.##..",
]
HEAD_TO = [
    "..............###..",
    ".......##..###uVV#.",
    "......#Yw#####VVv#.",
    "......#Yyo#4#Vvv#..",
    "....##3#oo#333#v##.",
    "...#3443###22##Vv#.",
    "..#3433#Y#y#222#v#.",
    ".#3333#3y#o#2211#..",
    "#3#33333#w##21100#.",
    "#33####w#vvvv#1100#",
    ".##vvvvvVVV#11100#.",
    "...#w#Bbbbb##000#..",
    "..#BBBBBbb#0000#...",
    "...########.###....",
]
HEAD_C = [
    ".............#....",
    "............#u#.#.",
    "........###.#V##V#",
    "......##443#VVvV#.",
    "....##3443333#Vv#.",
    "...#344333###3#v#.",
    "..#34433##Yy#2221#",
    ".#3#3333#yY##22110#",
    "#33333333###222110#",
    "#3############1100#",
    ".#BwBBBBBBbbbb#000#",
    "..##############.##",
]
HEAD_O = [
    ".............#....",
    "............#u#.#.",
    "........###.#V##V#",
    "......##443#VVvV#.",
    "....##3443333#Vv#.",
    "...#344333###3#v#.",
    "..#34433##Yy#2221#",
    ".#3#3333#yY##22110#",
    "#3333333##w#222110#",
    "#3####w#vvvv#11100#",
    ".###vvvvVVv#11000#.",
    "..#w#BBbbb##0000#..",
    ".#BBBBBb###0000#...",
    "..######.#####.....",
]
LHEAD_C = [
    "...........#######....",
    ".........##wwwwwBb#...",
    "........#wwwwwwwwBb#..",
    ".......#BwwwwwwwwwBb#.",
    ".....###w#ww#ww#w#bb#.",
    "....#34433#3#3#3#2#b#.",
    "...#3443Yo3333332221#.",
    "..#34433oo3333322221#.",
    "..#34433##33332222111#",
    ".#34433#w##3322221110#",
    ".#34433####3222221110#",
    "##4433#yYy#2222211100#",
    "#4#333#yyy#2222111100#",
    "#433333###22221111000#",
    "#33333333222211110000#",
    ".#3#############10000#",
    "..#BBwBBBbbbbb#1000#..",
    "...#BBBBbbbbb##000#...",
    "....###########.##....",
]
LHEAD_O = [
    "...........#######....",
    ".........##wwwwwBb#...",
    "........#wwwwwwwwBb#..",
    ".......#BwwwwwwwwwBb#.",
    ".....###w#ww#ww#w#bb#.",
    "....#34433#3#3#3#2#b#.",
    "...#3443Yo3333332221#.",
    "..#34433oo3333322221#.",
    "..#34433##33332222111#",
    ".#34433#w##3322221110#",
    ".#34433####3222221110#",
    "##4433#yYy#2222211100#",
    "#4#333#yyy#2222111100#",
    "#433333###22221111000#",
    "#33333333222211110000#",
    ".#3##########110000#..",
    "..#w#vvvvVVV#10000#...",
    "...#BvvvvVV#1000#.....",
    "....#BBBbbb#000#......",
    ".....#######.##.......",
]
DARK = {"4": "2", "3": "2", "2": "1", "1": "0", "B": "b", "u": "V", "Y": "y"}
DARKER = {"4": "1", "3": "1", "2": "1", "1": "0", "B": "b", "b": "1", "u": "V", "V": "v", "Y": "y"}


def _stamp(p, x, y, rows, flip=False, remap=None):
    """Paint a hand-drawn head with its top-left at (x, y), at battle size."""
    rows = [r[::-1] for r in rows] if flip else rows
    if remap:
        rows = ["".join(remap.get(c, c) for c in r) for r in rows]
    p.patch(x, y, rows, HL)


scale = Mat(["g0", "g1", "g2", "g3", "g4"], line="g0", cuts=[0.13, 0.36, 0.62, 0.9])
scaleM = Mat(["g0", "g1", "g2", "g3"], line="g0", cuts=[0.2, 0.46, 0.76])
scaleD = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.36, 0.72])
belly = Mat(["b0", "b1"], line="g1", cuts=[0.52])
bellyD = Mat(["g1", "b0"], line="g0", cuts=[0.5])
violet = Mat(["v0", "v1", "v2"], line="v0", cuts=[0.3, 0.68])
violetD = Mat(["v0", "v1"], line="v0", cuts=[0.5])
gold = Mat(["o0", "o1", "o2", "white"], line="o0", cuts=[0.2, 0.5, 0.82])
goldN = Mat(["o0", "o1", "o2"], line="o0", cuts=[0.3, 0.7])
claw = Mat(["b0", "b1", "white"], line="b0", cuts=[0.4, 0.75])
mouthM = Mat(["v0"], line="v0")
shell = Mat(["b0", "b1", "white"], line="b0", cuts=[0.3, 0.62])


# --------------------------------------------------------------------------
# Heads. Local coordinates face left with the origin at the skull's center;
# ang > 0 tips the snout up, f = 1 mirrors the head to face right.
# --------------------------------------------------------------------------

def _xf(cx, cy, s, f, ang):
    th = math.radians(ang)
    c, sn = math.cos(th), math.sin(th)

    def T(lx, ly):
        lx, ly = lx * s, ly * s
        rx, ry = c * lx - sn * ly, sn * lx + c * ly
        return (cx + (rx if f < 0 else -rx), cy + ry)
    return T


def _ip(T, lx, ly):
    x, y = T(lx, ly)
    return int(math.floor(x)), int(math.floor(y))


def _head(p, cx, cy, s=1.0, f=-1, ang=0.0, mouth=0.0, mat=None, jaw=None, crest=None, g=100, bias=0.0,
          ncrest=3, eye="o1", shine="o2", fang=True, drip=False, face=True):
    """A hydra head: a serpent-dragon skull with a brow ridge over a slit eye,
    a tapering muzzle with a nostril, a pale jaw, fangs at the corner of the
    mouth and violet crest spines swept back."""
    mat = mat or scaleM
    jaw = jaw or belly
    crest = crest or violet
    T = _xf(cx, cy, s, f, ang)

    def TP(pts):
        return [T(x, y) for x, y in pts]
    spines = [((-2.4, -3.0), (4.4, -9.4), 2.8, 0.9), ((0.8, -2.8), (8.4, -6.2), 2.6, 0.7),
              ((2.6, -0.4), (9.0, 0.4), 2.2, 0.4)]
    for i, (a, b, w, bd) in enumerate(spines[:ncrest]):
        p.poly(TP(lens_pts(a, b, w, bend=bd * -1, fat=0.3)), crest, group=g + i, bias=bias + 0.05 * i)
    m = mouth
    if m > 0:
        p.poly(TP([(-0.5, 0.8), (-11.4, 0.6), (-10.4, 2.0 + 3.0 * m), (-5, 3.0 + 1.6 * m), (-0.5, 3.6)]),
               mouthM, group=g + 5, flat=0)
    p.poly(TP(ribbon(bez((0.8, 3.0), (-5, 3.4 + 1.2 * m), (-10.2, 2.2 + 3.0 * m), n=10), lambda t: 3.0 - 1.4 * t)),
           jaw, group=g + 6, bias=bias)
    p.poly(TP(ellipse_pts(-10.0, 2.4 + 3.0 * m, 1.2, 1.0)), jaw, group=g + 6, bias=bias)
    p.poly(TP(ellipse_pts(0, 0, 4.8, 4.2)), mat, group=g + 7, bias=bias)
    p.poly(TP(ellipse_pts(1.2, 1.8, 3.8, 2.8)), mat, group=g + 7, bias=bias)
    p.poly(TP(ribbon(bez((-2, -0.6), (-6.5, -1.8), (-10.8, -0.2), n=12), lambda t: 6.2 - 2.6 * t)), mat,
           group=g + 7, bias=bias)
    p.poly(TP(ellipse_pts(-10.8, 0.1, 1.9, 1.8)), mat, group=g + 7, bias=bias)
    p.poly(TP(lens_pts((-7.2, -2.0), (1.4, -4.0), 2.4, bend=0.5, fat=0.55)), mat, group=g + 8, bias=bias - 0.05)
    if not face:
        return T
    if not p.big:
        x, y = _ip(T, -4.4, -1.2)
        p.fig.px(x, y, "ink")
        return T
    d = -1 if f < 0 else 1
    ex, ey = _ip(T, -4.4, -1.4)
    # slit eye: a gold iris split by a dark pupil, under the brow
    for dx, c in ((-1, eye), (0, "ink"), (1, eye)):
        p.fig.px(ex + dx * -d, ey, c)
    p.fig.px(ex + d, ey, shine)
    for dx in (-1, 0, 1):
        p.fig.px(ex + dx, ey - 1, "ink")
    p.fig.px(ex + 2 * -d, ey, "ink")
    nx, ny = _ip(T, -10.6, -1.2)
    p.fig.px(nx, ny, "ink")
    if fang:
        fx, fy = _ip(T, -8.2, 2.2 + 1.6 * m)
        p.fig.px(fx, fy, "white")
        p.fig.px(fx, fy + 1, "white")
    if drip:
        dx_, dy_ = _ip(T, -9.4, 4.6 + 3.0 * m)
        p.fig.px(dx_, dy_, "v2")
        p.fig.px(dx_, dy_ + 1, "v1")
    return T


def _ghead(p, cx, cy, s=1.0, f=-1, ang=0.0, mouth=0.0, g=300, face=True):
    """The immortal head: a crowned dragon. Two great horns sweep back off a
    lit brow plate with a circlet of short spikes between them, the muzzle is
    deep with a nose horn, the jaw heavy, and the eye burns with the violet
    regrowth-light."""
    T = _xf(cx, cy, s, f, ang)

    def TP(pts):
        return [T(x, y) for x, y in pts]
    # the far horn, behind the skull, then the circlet, then the near horn
    p.poly(TP(lens_pts((2.0, -2.6), (11.6, -9.6), 3.0, bend=-1.4, fat=0.26)), gold, group=g, bias=0.25)
    for i, (a, b, w) in enumerate((((-4.6, -3.6), (-5.4, -8.0), 2.2), ((-2.4, -4.4), (-1.6, -9.2), 2.4),
                                   ((-0.2, -4.6), (1.8, -9.0), 2.2))):
        p.poly(TP(lens_pts(a, b, w, bend=0.0, fat=0.3)), gold, group=g + 1 + i, bias=0.05 * i)
    m = mouth
    if m > 0:
        p.poly(TP([(-0.5, 1.2), (-10.0, 1.4), (-9.0, 2.8 + 3.0 * m), (-4, 3.8 + 1.6 * m), (-0.5, 4.2)]),
               mouthM, group=g + 6, flat=0)
    p.poly(TP(ribbon(bez((1.4, 3.6), (-4.2, 4.2 + 1.2 * m), (-8.6, 3.0 + 3.0 * m), n=10), lambda t: 3.8 - 1.6 * t)),
           goldN, group=g + 7, bias=0.14)
    p.poly(TP(ellipse_pts(0, 0, 5.2, 4.8)), gold, group=g + 8)
    p.poly(TP(ellipse_pts(1.6, 2.4, 4.2, 3.2)), gold, group=g + 8)
    p.poly(TP(ribbon(bez((-2, -0.6), (-5.8, -1.4), (-9.0, 0.4), n=12), lambda t: 7.6 - 2.6 * t)), gold,
           group=g + 8)
    p.poly(TP(ellipse_pts(-9.2, 0.8, 2.4, 2.3)), gold, group=g + 8)
    # nose horn
    p.poly(TP(lens_pts((-8.6, -1.2), (-10.4, -4.4), 2.2, bend=0.5, fat=0.3)), gold, group=g + 9)
    # the lit brow plate
    p.poly(TP(lens_pts((-7.2, -2.6), (2.4, -4.0), 3.2, bend=0.8, fat=0.5)), gold, group=g + 10, bias=-0.12)
    # the near horn, sweeping back over the skull
    p.poly(TP(lens_pts((-0.6, -3.4), (10.4, -6.0), 3.4, bend=-1.6, fat=0.24)), gold, group=g + 11, bias=-0.04)
    if not face:
        return T
    if not p.big:
        x, y = _ip(T, -4.0, -1.0)
        p.fig.px(x, y, "v1")
        return T
    d = -1 if f < 0 else 1
    ex, ey = _ip(T, -4.0, -1.0)
    p.fig.px(ex, ey, "white")
    p.fig.px(ex - d, ey, "v2")
    p.fig.px(ex + d, ey, "v1")
    p.fig.px(ex, ey + 1, "v1")
    for dx in (-1, 0, 1, 2):
        p.fig.px(ex + dx * -d, ey - 1, "o0")
    nx, ny = _ip(T, -9.6, -0.4)
    p.fig.px(nx, ny, "o0")
    fx, fy = _ip(T, -6.8, 3.4 + 1.6 * m)
    p.fig.px(fx, fy, "white")
    p.fig.px(fx, fy + 1, "white")
    return T


def _seam(p, a, b, w=2.2, clip=None, glow=1):
    """A violet regrowth seam across a fork: a lens of glowing scar tissue
    from a to b, its core lit brighter."""
    kw = {"clip": clip} if clip else {}
    p.poly(lens_pts(a, b, w, fat=0.5), violet, flat=1, noline=True, nooutline=True, group=900, **kw)
    if p.big and glow:
        p.stroke([lerp(a, b, 0.3), lerp(a, b, 0.7)], "v2")


def _spines(p, pts, size=2.6, mat=None, g=950, bias=0.0, out=1):
    """Violet dorsal spines along a path, each pointing away (out=1 to the
    right of the direction of travel)."""
    mat = mat or violet
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d * out, dx / d * out
        L = size * (1.0 - 0.15 * (i % 2))
        tip = (x0 + nx * L + dx / d * L * 0.7, y0 + ny * L + dy / d * L * 0.7)
        p.poly(lens_pts((x0 - nx * 0.6, y0 - ny * 0.6), tip, size * 0.85, fat=0.3), mat, group=g + i, bias=bias)


def _fhead(p, cx, cy, s=1.0, mat=None, crest=None, eye="o1", goldh=False, g=600):
    """A head seen from the front, for the follower walking toward the
    camera: a round skull over a broad snout, two eyes, crest spines (or the
    gold head's horns) swept out to both sides."""
    mat = mat or scaleM
    crest = crest or violet
    if goldh:
        for sx in (-1, 1):
            p.lens((cx + sx * 2.5 * s, cy - 2.5 * s), (cx + sx * 8 * s, cy - 8 * s), 2.6 * s, gold, fat=0.3, group=g)
        p.lens((cx, cy - 3 * s), (cx, cy - 8.5 * s), 2.6 * s, gold, fat=0.3, group=g + 1)
    else:
        for sx in (-1, 1):
            p.lens((cx + sx * 2.5 * s, cy - 2 * s), (cx + sx * 7 * s, cy - 6 * s), 2.4 * s, crest, fat=0.3, group=g)
    p.blob(cx, cy, 4.4 * s, 4 * s, mat, group=g + 2)
    p.blob(cx, cy + 3.6 * s, 3.4 * s, 2.6 * s, mat, group=g + 2)
    p.blob(cx, cy + 5.2 * s, 2.6 * s, 1.2 * s, belly if not goldh else goldN, group=g + 3)
    ec = "v2" if goldh else eye
    for sx in (-1, 1):
        p.px(cx + sx * 2.2 * s - 0.5, cy - 0.2 * s, ec)
        p.px(cx + sx * 2.2 * s - 0.5, cy - 1.2 * s, "ink")
    p.px(cx - 1, cy + 3.2 * s, "ink")
    p.px(cx + 0.2, cy + 3.2 * s, "ink")


# Icons and followers are drawn small, where the shared icon palettes have
# only two greens: keep their forms bold and their tones light.
iconG = Mat(["g1", "g2", "g3"], line="g1", cuts=[0.35, 0.7])
iconD = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.4, 0.75])


def _ihead(p, cx, cy, s=1.0, f=-1, mat=None, crest=None, mouth=0, g=700, goldh=False):
    """A bold small head for icons and followers: a round skull, a snout,
    a crest fin swept back (or the gold head's horns), one eye, a mouth."""
    mat = mat or iconG
    crest = crest or violet
    X = lambda d: cx - f * -d * s if False else cx + f * d * s
    Y = lambda d: cy + d * s
    if goldh:
        for (ax, ay), (bx, by) in (((-1.5, -3.5), (-3.5, -10)), ((1, -4), (2.5, -10.5)), ((3.5, -2.5), (9, -7)),
                                   ((4, 0), (9.5, -1.5))):
            p.lens((X(ax), Y(ay)), (X(bx), Y(by)), 2.6 * s, gold, fat=0.3, group=g)
    else:
        p.lens((X(2), Y(-3)), (X(8.5), Y(-6.5)), 3.2 * s, crest, fat=0.3, group=g)
        p.lens((X(3.5), Y(-0.5)), (X(8.5), Y(0.5)), 2.6 * s, crest, fat=0.3, group=g)
    p.blob(X(0.5), Y(0), 4.6 * s, 4.2 * s, mat, group=g + 1)
    p.limb([(X(-1), Y(0.6)), (X(-8.5), Y(1.2))], 5.6 * s, 4.2 * s, mat, group=g + 1)
    if mouth:
        p.limb([(X(-1), Y(3.4)), (X(-7.5), Y(4.6 + mouth))], 2.6 * s, 1.8 * s, mouthM, group=g + 2)
    p.px(X(-3), Y(-1.2), "v2" if goldh else "ink")
    if not mouth:
        p.stroke([(X(-8), Y(2.6)), (X(-2.5), Y(2.8))], "o0" if goldh else "g0")


# --------------------------------------------------------------------------
# Lernathan, the Lernaean Hydra
# --------------------------------------------------------------------------

LERNATHAN_COLORS = COLORS
LERNATHAN_SHINY = {
    # deep Aegean scales, and the golden head turns marble white
    "g0": (16, 24, 72), "g1": (24, 56, 120), "g2": (48, 96, 168), "g3": (96, 144, 208), "g4": (176, 208, 240),
    "o0": (152, 144, 144), "o1": (208, 200, 192), "o2": (240, 240, 232),
}


def lernathan(p, view, phase):
    if view in ("icon", "side"):
        # the icon doubles as the side follower: compact and bold, legs
        # swapping as it walks
        walk = phase if view == "side" else -1
        # party icon: the crowned gold head over four green ones, on a squat
        # body, compact so the heads stay big; frame 2 the heads snap
        b = phase if view == "icon" else 0
        p.limb(bez3((38, 54), (45, 58), (50, 55), (49, 49)), 6, 2.2, iconG, group=1)
        p.blob(33, 52, 8.5, 7, iconG, group=2)
        p.blob(30, 54, 4, 5, belly, group=3)
        for i, x in enumerate((28, 37)):
            lift = 1.5 if walk == i else 0
            p.blob(x - (2 if walk == i else 0), 59.5 - lift, 3.6, 2.2, iconG, group=4)
        p.limb([(33, 47), (33, 40)], 8, 7, iconG, group=5)
        for hx, hy in ((19, 31 + b), (47, 31 - b)):
            p.limb(bez((33, 43), (hx + (33 - hx) * 0.4, 42), (hx, hy + 3)), 5, 4.4, iconG, group=6)
        for hx, hy in ((22, 41 - b), (45, 41 + b)):
            p.limb(bez((33, 45), (hx + (33 - hx) * 0.4, 46), (hx, hy + 2)), 5, 4.4, iconG, group=7)
        _ihead(p, 47, 30 - b, 1.2, f=1, mat=iconD, g=700)
        _ihead(p, 46, 41 + b, 1.15, f=1, mat=iconD, mouth=1, g=710)
        _ihead(p, 19, 30 + b, 1.25, f=-1, mouth=1.5, g=720)
        _ihead(p, 21, 41 - b, 1.2, f=-1, g=730)
        p.limb([(33, 41), (32, 32)], 6.4, 6, gold, group=8)
        _ihead(p, 32, 27, 1.55, f=-1, mat=gold, goldh=True, g=740)
        p.limb(bez((28.5, 42), (33, 44), (37.5, 42)), 2.4, 2.4, violet, group=9)
        return

    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        big = p.big
        # ---- tail, sweeping back and curling up --------------------------
        tail = bez3((44, 50), (56, 60), (64, 54), (59, 41 - 2 * F))
        _spines(p, [tail[i] for i in (5, 8, 11, 14)], 3.2, out=-1, g=960)
        p.limb(tail, 11.5, 2.2, scale, group=5)
        # ---- far leg, far arm ---------------------------------------------
        p.limb([(44, 47), (48, 53), (46, 58)], 9, 6, scaleD, group=6)
        p.blob(45, 59.6, 5.2, 2.2, scaleD, group=6)
        p.limb([(35, 43), (28, 50), (22, 50)], 6, 5, scaleD, group=7)
        p.blob(20.5, 50.5, 2.8, 2.4, scaleD, group=7)
        # ---- far branch: forks right into two dark heads facing back ------
        p.limb(bez((36, 30), (43, 30), (46, 25)), 8, 6.8, scaleD, group=40)
        p.limb(bez3((46, 26), (45, 20), (49, 19), (51, 15)), 5.6, 5.0, scaleD, group=41)
        p.limb(bez((46, 26), (50, 28), (53, 28)), 5.6, 5.0, scaleD, group=42)
        if not big:
            _head(p, 55, 9, 0.66, f=1, ang=24, mouth=0.9, mat=scaleD, jaw=bellyD, crest=violetD, g=400, ncrest=2)
            _head(p, 56, 24, 0.64, f=1, ang=-8, mat=scaleD, jaw=bellyD, crest=violetD, g=420, ncrest=2)
        # ---- body ----------------------------------------------------------
        _spines(p, [(41, 33), (44.5, 37), (47.5, 41.5), (49.5, 46)], 3.4, out=-1, g=952)
        p.blob(40, 49, 9.5, 8, scale, group=1)            # hips
        p.blob(31.5, 44, 10.5, 9.5, scale, group=1)       # chest
        p.blob(34, 37, 9.5, 5.5, scale, group=1)          # shoulders
        p.poly(bez3((25, 35), (20, 44), (26, 54), (36, 57)) + bez3((36, 57), (31, 48), (29, 41), (30, 34)),
               belly, group=2)
        # ---- trunk neck and the gold stem --------------------------------
        p.limb(bez((34, 40), (33, 34), (33, 28)), 13.5, 11.5, scale, group=10)
        p.limb(bez3((33, 31), (38, 27), (34, 24), (35, 18)), 9.4, 8.4, gold, group=11)
        if not big:
            _ghead(p, 31, 11, 1.0, f=-1, ang=12, g=300)
        # ---- near branch: forks left into two light heads ------------------
        p.limb(bez((31, 31), (25, 31), (22, 27)), 8.4, 7.4, scale, group=20)
        nu = p.limb(bez3((22, 28), (21, 21), (15, 21), (11, 16)), 6.4, 5.6, scale, group=21)
        p.limb(bez3((20.4, 27), (19.4, 23), (14, 23), (10, 18)), 1.8, 1.6, belly, clip=[nu], group=23)
        nl = p.limb(bez3((21, 28), (19, 30), (18, 32), (14, 32)), 6.4, 5.8, scale, group=22)
        p.limb(bez3((20, 30.4), (19, 32), (17, 34), (14, 34.4)), 1.8, 1.6, belly, clip=[nl], group=24)
        if not big:
            _head(p, 9, 16, 0.74, f=-1, ang=8, g=200, ncrest=2)
            _head(p, 10, 31, 0.76, f=-1, ang=-6, mouth=1.0, g=220, ncrest=2)
        # ---- seams at the forks -------------------------------------------
        _seam(p, (28, 30), (38, 29))
        _seam(p, (19, 28), (24, 24))
        _seam(p, (44, 27), (49, 23))
        # ---- near leg, near arm ---------------------------------------------
        p.limb([(36, 48), (29, 54), (31, 59)], 11.5, 7, scale, group=60)
        p.blob(28, 59.6, 6, 2.4, scale, group=60)
        p.limb([(27, 40), (22, 47), (16, 45)], 7.4, 5.6, scale, group=70)
        p.blob(15, 44.5, 2.8, 2.8, scale, group=70)
        if big:
            # frame 2: the heads strike in turn, the near one snapping shut
            # as the far one opens to hiss
            _stamp(p, 46, 6, HEAD_SO if F else HEAD_SC, flip=True, remap=DARKER)
            _stamp(p, 46, 20 + F, HEAD_SC if F else HEAD_SO, flip=True, remap=DARK)
            _stamp(p, 16, 1, GHEAD)
            _stamp(p, 1, 3 - F, HEAD_RO)
            _stamp(p, 1, 25 + F, HEAD_SC if F else HEAD_SO)
        return

    if view == "back":
        # over the shoulder at about 1.2x: the broad spined back cropped by
        # the frame, the trunk rising from it and forking twice, the golden
        # head in right profile leading, the green heads watching every way
        big = p.big
        tail = bez3((15, 64), (4, 60), (2, 50), (7, 42))
        _spines(p, [tail[i] for i in (6, 9, 12)], 3.4, out=1, g=960)
        p.limb(tail, 11, 3, scale, group=5)
        # left branch, behind: two heads looking away to the left
        p.limb(bez((28, 39), (20, 38), (17, 33)), 10, 9, scaleD, group=30)
        p.limb(bez3((17, 34), (17, 27), (14, 22), (12, 17)), 7, 6.4, scaleD, group=31)
        p.limb(bez3((17, 34), (13, 35), (11, 33), (9, 31)), 7, 6.4, scaleD, group=32)
        # right branch: one head turned right to hiss
        p.limb(bez((37, 39), (45, 39), (48, 35)), 10, 9, scaleM, group=33)
        p.limb(bez3((48, 36), (51, 34), (51, 31), (53, 29)), 7.4, 6.6, scaleM, group=34)
        # the back, the spine ridge and the trunk
        _spines(p, [(29, 63), (28.5, 58), (28.5, 53)], 4.0, out=1, g=952)
        p.blob(32, 70, 29.5, 21, scale, group=1)
        p.blob(17, 55, 12, 9, scale, group=1)
        p.blob(46, 55, 12, 9, scale, group=1)
        p.limb(bez((32, 58), (33, 46), (33, 37)), 19, 16, scale, group=10)
        _spines(p, [(25, 50), (25.5, 45), (26.5, 40)], 3.4, out=1, g=970)
        p.limb(bez3((33, 39), (39, 34), (35, 30), (39, 24)), 11, 9.6, gold, group=11)
        _seam(p, (26, 38), (41, 38))
        _seam(p, (13, 35), (20, 31))
        _seam(p, (45, 38), (51, 33))
        if big:
            _stamp(p, 1, 9, HEAD_SC, remap=DARKER)
            _stamp(p, 1, 25, HEAD_SC, remap=DARK)
            _stamp(p, 46, 22, HEAD_SO, flip=True)
            _stamp(p, 33, 4, GHEAD, flip=True)
        else:
            _ghead(p, 44, 12, 1.2, f=1, ang=8, g=300)
        return

    if view in ("down", "up"):
        # follower: the five heads fanned over a squat body, toward the camera
        # (down) or seen from behind (up), the legs stepping in turn
        step = phase
        back = view == "up"
        if back:
            p.limb(bez3((32, 54), (40, 62), (50, 60), (52, 50 - step)), 9, 2.6, iconG, group=5)
            p.blob(51.5, 48.5 - step, 2.6, 2.4, violet, group=5)
        for x, st in ((24, step), (40, 1 - step)):
            p.limb([(x, 50), (x, 59 - 2 * st)], 9, 8, iconG, group=12 if x < 32 else 13)
            p.blob(x, 60 - 2 * st, 5, 2.4, iconG, group=12 if x < 32 else 13)
        p.blob(32, 48, 14, 11, iconG, group=1)
        if not back:
            p.blob(32, 50, 7, 8, belly, group=2)
            for sx in (-1, 1):
                p.limb([(32 + sx * 12, 44), (32 + sx * 15, 51)], 6, 5, iconG, group=20 + sx)
        p.limb([(32, 44), (32, 33)], 13, 12, iconG, group=3)
        for sx in (-1, 1):
            p.limb(bez((32 + sx * 4, 36), (32 + sx * 14, 35), (32 + sx * 18, 26)), 8, 7, iconG, group=30 + sx)
            p.limb(bez((32 + sx * 4, 40), (32 + sx * 15, 41), (32 + sx * 19, 37)), 8, 7, iconG, group=32 + sx)
        p.limb([(32, 34), (32, 22)], 9, 8, gold, group=4)
        p.limb(bez((25, 36), (32, 39), (39, 36)), 3, 3, violet, group=6)
        if back:
            for sx in (-1, 1):
                for hx, hy in ((32 + sx * 17, 20), (32 + sx * 20, 33)):
                    p.blob(hx, hy, 5.6, 5.2, iconD, group=40 + sx)
                    p.lens((hx, hy - 3), (hx + sx * 6, hy - 9), 3.4, violet, fat=0.3, group=41 + sx)
            p.blob(32, 17, 6.4, 6, gold, group=44)
            for sx in (-1, 0, 1):
                p.lens((32 + sx * 3, 13), (32 + sx * 7, 3 + abs(sx) * 3), 3.2, gold, fat=0.3, group=45)
        else:
            for sx in (-1, 1):
                _ihead(p, 32 + sx * 17, 20, 1.4, f=sx, mat=iconD if sx > 0 else iconG, mouth=1.4 if sx < 0 else 0,
                       g=400 + 20 * (sx > 0))
                _ihead(p, 32 + sx * 20, 33, 1.35, f=sx, mat=iconG if sx > 0 else iconD, mouth=1.4 if sx > 0 else 0,
                       g=440 + 20 * (sx > 0))
            _fhead(p, 32, 16, 1.5, goldh=True, mat=gold, g=600)
        return


# --------------------------------------------------------------------------
# Trilerna, the three-headed (stub)
# --------------------------------------------------------------------------

TRILERNA_COLORS = COLORS
TRILERNA_SHINY = {
    "g0": (16, 40, 88), "g1": (24, 72, 136), "g2": (48, 112, 184), "g3": (112, 168, 224), "g4": (184, 216, 240),
    "o0": (152, 144, 144), "o1": (208, 200, 192), "o2": (240, 240, 232),
}


def trilerna(p, view, phase):
    if view in ("icon", "side"):
        # the icon doubles as the side follower: compact and bold, legs
        # swapping as it walks
        b = phase if view == "icon" else 0
        walk = phase if view == "side" else -1
        p.limb(bez3((38, 54), (46, 58), (51, 55), (50, 48)), 6.4, 2.2, iconG, group=1)
        p.blob(33, 52, 8.5, 7.5, iconG, group=2)
        p.blob(30, 54, 4, 5, belly, group=3)
        for i, x in enumerate((28, 37)):
            lift = 1.5 if walk == i else 0
            p.blob(x - (2 if walk == i else 0), 59.5 - lift, 3.6, 2.2, iconG, group=4)
        p.limb([(33, 47), (33, 41)], 7.4, 6.6, iconG, group=5)
        p.limb(bez((33, 44), (40, 43), (44, 38)), 5.4, 4.6, iconD, group=6)
        p.limb(bez((33, 45), (26, 45), (22, 41)), 5.4, 4.6, iconG, group=7)
        p.limb(bez((33, 42), (33, 37), (32, 32)), 6, 5.4, iconG, group=8)
        _ihead(p, 46, 35 - b, 1.25, f=1, mat=iconD, g=700)
        _ihead(p, 19, 39 + b, 1.3, f=-1, mouth=1.5, g=710)
        _ihead(p, 31, 28 - b, 1.5, f=-1, g=720)
        p.blob(28, 22.5 - b, 1.9, 1.7, gold, group=730)
        p.limb(bez((29, 43), (33, 45), (37, 43)), 2.2, 2.2, violet, group=9)
        return

    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        big = p.big
        # tail, long and whipping back
        tail = bez3((43, 50), (53, 58), (62, 55), (59, 44 - 2 * F))
        _spines(p, [tail[i] for i in (5, 8, 11, 14)], 2.8, out=-1, g=960)
        p.limb(tail, 9.5, 2.2, scale, group=5)
        # far leg, far arm
        p.limb([(42, 48), (45, 54), (44, 58.5)], 7.6, 5, scaleD, group=6)
        p.blob(43.5, 59.8, 4.4, 2.0, scaleD, group=6)
        p.limb([(35, 42), (30, 48), (25, 48)], 4.8, 4.2, scaleD, group=7)
        p.blob(24, 48.4, 2.2, 2.0, scaleD, group=7)
        # far neck and head, turned back over the shoulder
        p.limb(bez3((36, 32), (41, 30), (43, 26), (47, 23)), 6.4, 5.8, scaleD, group=40)
        if not big:
            _head(p, 49, 19, 0.74, f=1, ang=10, mat=scaleD, jaw=bellyD, crest=violetD, g=400, ncrest=2)
        # the cut stump between the necks, sealed, two tiny heads budding
        p.limb(bez((36, 31), (38, 28), (38.5, 25.5)), 4.6, 4.2, scaleM, group=45)
        p.blob(37, 24.6, 1.9, 1.7, scaleM, group=46)
        p.blob(40.2, 25.2, 1.7, 1.6, scaleM, group=47)
        # body
        _spines(p, [(40, 34), (43, 38.5), (45.5, 43)], 2.8, out=-1, g=952)
        p.blob(38.5, 48.5, 7.8, 7.2, scale, group=1)
        p.blob(32, 43, 8.4, 8.4, scale, group=1)
        p.blob(34, 36.5, 7.4, 4.8, scale, group=1)
        p.poly(bez3((27, 35), (23, 43), (28, 52), (36, 55)) + bez3((36, 55), (32, 47), (31, 41), (31, 34)),
               belly, group=2)
        # trunk neck and the middle neck
        p.limb(bez((34, 39), (33, 34), (33, 30)), 10.4, 9.4, scale, group=10)
        p.limb(bez3((33, 31), (37, 26), (32, 21), (33, 15)), 7.6, 6.8, scale, group=11)
        if not big:
            _head(p, 27, 11, 0.92, f=-1, ang=8, g=300, ncrest=3)
        # near neck and head, lowered and hissing
        nn = p.limb(bez3((31, 32), (26, 27), (21, 25), (16, 27)), 7, 6.2, scale, group=20)
        p.limb(bez3((30, 34.5), (25, 29.5), (20, 27.5), (15, 29.5)), 1.8, 1.6, belly, clip=[nn], group=21)
        if not big:
            _head(p, 10, 25, 0.8, f=-1, ang=-6, mouth=1.0, g=200, ncrest=2)
        _seam(p, (28, 32), (38, 31))
        _seam(p, (37, 26.5), (40, 27))
        # near leg, near arm
        p.limb([(35, 48), (30, 53), (31, 58.5)], 9, 5.8, scale, group=60)
        p.blob(28.5, 59.8, 5.2, 2.2, scale, group=60)
        p.limb([(28, 39), (24, 46), (19, 45)], 5.6, 4.6, scale, group=70)
        p.blob(18, 44.6, 2.3, 2.3, scale, group=70)
        if big:
            _stamp(p, 42, 14 - F, HEAD_SO if F else HEAD_SC, flip=True, remap=DARK)
            _stamp(p, 18, 5 - F, HEAD_TO if F else HEAD_TC)
            _stamp(p, 2, 20 + F, HEAD_SC if F else HEAD_SO)
        return

    if view == "back":
        # over the shoulder: the trunk splitting into three, the middle head
        # in right profile with its gold bud, the others turning away
        big = p.big
        tail = bez3((14, 64), (5, 60), (3, 52), (8, 45))
        _spines(p, [tail[i] for i in (6, 9, 12)], 2.8, out=1, g=960)
        p.limb(tail, 10, 2.6, scale, group=5)
        p.limb(bez3((29, 41), (24, 33), (20, 28), (15, 25)), 9, 7.6, scaleD, group=30)
        p.limb(bez3((37, 41), (42, 34), (44, 33), (48, 31)), 9, 7.6, scaleM, group=33)
        _spines(p, [(30, 63), (29.5, 58), (29.5, 53)], 3.4, out=1, g=952)
        p.blob(32, 69, 27, 18, scale, group=1)
        p.blob(19, 57, 10, 7, scale, group=1)
        p.blob(45, 57, 10, 7, scale, group=1)
        p.limb(bez((32, 60), (33, 50), (33, 40)), 15, 12.5, scale, group=10)
        _spines(p, [(27, 52), (27, 47), (28, 42)], 2.8, out=1, g=970)
        p.limb(bez3((33, 42), (38, 35), (33, 29), (36, 22)), 9.4, 8, scale, group=11)
        _seam(p, (26, 41), (40, 41))
        if big:
            _stamp(p, 1, 16, HEAD_MC, remap=DARKER)
            _stamp(p, 44, 23, HEAD_MO, flip=True, remap=DARK)
            _stamp(p, 27, 12, HEAD_TC, flip=True)
        else:
            _head(p, 40, 18, 1.1, f=1, g=300)
        return

    if view in ("down", "up"):
        step = phase
        back = view == "up"
        if back:
            p.limb(bez3((32, 54), (40, 62), (49, 60), (51, 50 - step)), 8, 2.4, iconG, group=5)
            p.blob(50.5, 48.5 - step, 2.4, 2.2, violet, group=5)
        for x, st in ((25, step), (39, 1 - step)):
            p.limb([(x, 50), (x, 59 - 2 * st)], 8, 7, iconG, group=12 if x < 32 else 13)
            p.blob(x, 60 - 2 * st, 4.4, 2.2, iconG, group=12 if x < 32 else 13)
        p.blob(32, 48, 12.5, 10, iconG, group=1)
        if not back:
            p.blob(32, 50, 6, 7.5, belly, group=2)
            for sx in (-1, 1):
                p.limb([(32 + sx * 11, 44), (32 + sx * 14, 50)], 5, 4.4, iconG, group=20 + sx)
        p.limb([(32, 44), (32, 33)], 11, 10, iconG, group=3)
        for sx in (-1, 1):
            p.limb(bez((32 + sx * 3, 37), (32 + sx * 13, 36), (32 + sx * 17, 29)), 8, 7, iconG, group=30 + sx)
        p.limb([(32, 34), (32, 23)], 8, 7.4, iconG, group=4)
        p.limb(bez((26, 37), (32, 40), (38, 37)), 2.8, 2.8, violet, group=6)
        if back:
            for sx in (-1, 1):
                p.blob(32 + sx * 18, 25, 5.6, 5.2, iconD, group=40 + sx)
                p.lens((32 + sx * 18, 22), (32 + sx * 24, 16), 3.4, violet, fat=0.3, group=41 + sx)
            p.blob(32, 18, 6.2, 5.8, iconG, group=44)
            for sx in (-1, 1):
                p.lens((32 + sx * 3, 14), (32 + sx * 7, 7), 3.2, violet, fat=0.3, group=45)
        else:
            for sx in (-1, 1):
                _ihead(p, 32 + sx * 19, 25, 1.5, f=sx, mat=iconD if sx > 0 else iconG, mouth=1.4 if sx < 0 else 0,
                       g=400 + 20 * (sx > 0))
            _fhead(p, 32, 18, 1.45, mat=iconG, g=600)
            p.blob(32, 12.5, 1.6, 1.4, gold, group=650)
        return


# --------------------------------------------------------------------------
# Lernip, the hatchling (stub)
# --------------------------------------------------------------------------

LERNIP_COLORS = COLORS
LERNIP_SHINY = {
    # Aegean blue scales, and the violet spots turn sun-gold
    "g0": (16, 40, 88), "g1": (24, 72, 136), "g2": (48, 112, 184), "g3": (112, 168, 224), "g4": (184, 216, 240),
    "v0": (120, 72, 24), "v1": (216, 160, 48), "v2": (248, 224, 120),
}


def lernip(p, view, phase):
    if view in ("icon", "side"):
        # the icon doubles as the side follower: compact and bold, legs
        # swapping as it walks
        b = phase if view == "icon" else 0
        walk = phase if view == "side" else -1
        p.limb(bez3((40, 54), (50, 59), (57, 55), (55, 47)), 7, 2.2, iconG, group=1)
        p.blob(35, 51, 9, 9, iconG, group=2)
        p.blob(31, 53, 4.6, 6, belly, group=3)
        for i, x in enumerate((30, 40)):
            lift = 1.5 if walk == i else 0
            p.blob(x - (2 if walk == i else 0), 60 - lift, 4, 2.4, iconG, group=4)
        p.blob(42, 42, 3, 2.8, iconG, group=5)
        p.blob(26, 32 + b, 14, 12.5, iconG, group=6)
        p.blob(14, 37 + b, 7.5, 6, iconG, group=6)
        p.limb([(10, 41 + b), (22, 43 + b)], 3, 2.4, mouthM, group=7)
        p.poly([(14, 26 + b), (17, 20 + b), (24, 17 + b), (32, 17 + b), (39, 21 + b), (41, 27 + b), (37, 25 + b),
                (34, 28 + b), (31, 25 + b), (28, 28 + b), (25, 25 + b), (22, 28 + b), (19, 25 + b)], shell, group=8)
        p.rect(19, 30 + b, 21, 34 + b, Mat(["ink"]), group=9)
        p.rect(19, 33 + b, 21, 34 + b, Mat(["o1"]), group=10)
        p.blob(16.5, 27 + b, 1.4, 1.3, gold, group=11)
        return

    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        big = p.big
        # tail curling up behind, a violet tip
        tail = bez3((39, 55), (47, 60), (54, 57), (53, 49 - F))
        p.limb(tail, 7, 2.0, scale, group=5)
        # far leg, far arm
        p.limb([(38, 54), (40, 58.5)], 5.4, 4.6, scaleD, group=6)
        p.blob(40, 60, 3.4, 1.8, scaleD, group=6)
        # the forked bud at the root of the neck: two knobs waiting to wake
        p.blob(40.5, 42.5, 2.6, 2.4, scaleM, group=45)
        p.blob(43, 45.5, 2.4, 2.2, scaleM, group=46)
        # body: a chubby hatchling, belly forward
        p.blob(35, 51, 7, 7.5, scale, group=1)
        p.blob(33, 45, 5.5, 4.5, scale, group=1)
        p.poly(bez3((29, 44), (27, 50), (30, 57), (36, 58)) + bez3((36, 58), (33, 52), (32, 47), (32, 43)),
               belly, group=2)
        # near leg, stubby arm
        p.limb([(33, 55), (31, 58.5)], 6, 5, scale, group=60)
        p.blob(30, 60, 4, 2, scale, group=60)
        p.limb([(30, 47), (27, 50), (25.5, 49)], 3.6, 3.0, scale, group=70)
        if big:
            _stamp(p, 13, 24 - F, LHEAD_O if not F else LHEAD_C)
        else:
            _head(p, 26, 34, 1.1, f=-1, g=200, ncrest=2)
        return

    if view == "back":
        # over the shoulder: the round back and tail, the forked bud on the
        # neck, the big head turned right in profile under its eggshell cap
        big = p.big
        tail = bez3((17, 64), (7, 62), (4, 54), (9, 47))
        p.limb(tail, 9, 2.4, scale, group=5)
        p.blob(32, 70, 23, 17, scale, group=1)
        p.limb(bez((33, 60), (34, 50), (36, 43)), 15, 12, scale, group=10)
        p.blob(26, 47.5, 3.6, 3.4, scaleM, group=45)
        p.blob(23.5, 52, 3.4, 3.2, scaleM, group=46)
        if big:
            _stamp(p, 26, 22, LHEAD_C, flip=True)
        else:
            _head(p, 40, 36, 1.3, f=1, g=300)
        return

    if view in ("down", "up"):
        step = phase
        back = view == "up"
        if back:
            p.limb(bez3((32, 56), (38, 61), (44, 59), (45, 53 - step)), 5, 1.8, scale, group=5)
        for x, st in ((28, step), (36, 1 - step)):
            p.limb([(x, 54), (x, 59.5 - 1.5 * st)], 5, 4.4, scale, group=12 if x < 32 else 13)
            p.blob(x, 60 - 1.5 * st, 3, 1.6, scale, group=12 if x < 32 else 13)
        p.blob(32, 51, 7, 7, scale, group=1)
        if not back:
            p.blob(32, 52, 4, 5, belly, group=2)
            for sx in (-1, 1):
                p.limb([(32 + sx * 6, 48), (32 + sx * 8, 51)], 3, 2.6, scale, group=20 + sx)
        p.blob(32, 36, 9.5, 9, scale, group=3)
        p.blob(32, 30, 8, 5, shell, group=4)
        if p.big:
            p.patch(24, 32, ["#.#.#.#.#.#.#.#.#"[:17]], HL)
        if not back:
            p.blob(32, 41, 5.5, 3.6, scaleM, group=5)
            p.blob(32, 43.5, 3.6, 1.4, belly, group=6)
            for sx in (-1, 1):
                p.eye(32 + sx * 4.5 - 1, 35, 2, 3, iris="o1", shine="white")
            p.px(31.5, 33, "o1")
            p.pxs([(30.5, 40), (32.5, 40)], "ink")
        return



MONS = [
    Mon("Lernip", LERNIP_COLORS, LERNIP_SHINY, lernip, foot="claw"),
    Mon("Trilerna", TRILERNA_COLORS, TRILERNA_SHINY, trilerna, foot="claw"),
    Mon("Lernathan", LERNATHAN_COLORS, LERNATHAN_SHINY, lernathan, foot="claw"),
]
