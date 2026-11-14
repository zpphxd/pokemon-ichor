"""Cerberus line: Kynder, Dikyon, Pylakyon (Fire starter). Kerberos, the hound of Hades' gate.

Direction A, "Ember Dreams": the heads that are still asleep are flames. Kynder's
two sleeping heads are dozing flame faces curled up out of its ruff; on Dikyon
one has woken into flesh; on Pylakyon all three are flesh under a fire mane that
cools to ghost-blue at the tips.
"""
import math

from mon_lib import C, Mat, Mon, lerp, bez, bez3, ellipse_pts, lens_pts, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------

# a flame tongue: red rim, orange body, gold toward the base, a pale core
FLAME = Mat(["fire0", "fire1", "fire2", "fire3"], line="fire0", outline="fire0")
# a dozing flame face: lit like a head, pale core on the upper left
DREAM = Mat(["fire1", "fire2", "fire3"], line="fire0", outline="fire0", cuts=[0.40, 0.66])
# the same, a step deeper, for a face further back
DREAM_FAR = Mat(["fire0", "fire1", "fire2", "fire3"], line="fire0", outline="fire0", cuts=[0.22, 0.48, 0.80])


def _flame(p, a, b, w, bend=0.0, hot=3, mat=None, **kw):
    """A flame tongue from base a to tip b, layered rim to core."""
    mat = mat or FLAME
    p.lens(a, b, w, mat, bend=bend, fat=0.32, flat=1, **kw)
    kw.pop("group", None)
    kw.pop("under", None)
    p.lens(a, lerp(a, b, 0.6), w * 0.62, mat, bend=bend * 0.6, fat=0.3, flat=2, noline=True, nooutline=True, **kw)
    if hot >= 3 and p.big:
        p.lens(a, lerp(a, b, 0.3), w * 0.34, mat, bend=bend * 0.3, fat=0.3, flat=3, noline=True,
               nooutline=True, **kw)


def _dream(p, cx, cy, s=1.0, f=-1, g=60, licks=((2, -2, 9, -10, 5, -1.6), (4, 1, 11, -4, 4, -1.2)),
           mat=None, eye="coat0"):
    """A dozing flame face: a hound's head made of fire, eyes shut, its ears
    flame tongues and the back of its skull streaming into flame licks.
    f=-1 faces left. Returns nothing; the eye and nose are painted at
    battle size."""
    mat = mat or DREAM
    X = lambda d: cx + f * -d * s
    Y = lambda d: cy + d * s
    for x0, y0, x1, y1, w, bend in licks:
        _flame(p, (X(x0), Y(y0)), (X(x1), Y(y1)), w * s, bend=bend * s * -f, group=g, hot=2)
    p.lens((X(-3.2), Y(-2.5)), (X(-4.6), Y(-8.6)), 3.8 * s, mat, bend=0.6 * s * -f, fat=0.4, group=g + 1)
    p.lens((X(1.6), Y(-3)), (X(2.6), Y(-9.4)), 4.4 * s, mat, bend=-0.8 * s * -f, fat=0.4, group=g + 1)
    p.circle(X(0), Y(0), 4.6 * s, mat, group=g + 2)
    p.blob(X(-5.0), Y(1.8), 3.2 * s, 2.2 * s, mat, ang=8 * -f, group=g + 2)
    if p.big:
        ex, ey = X(-2.6), Y(-0.6)
        if f > 0:
            ex -= 3
        p.pxs([(ex, ey), (ex + 1, ey + 1), (ex + 2, ey + 1), (ex + 3, ey)], eye)
        p.pxs([(X(-8.0), Y(0.9)), (X(-7.0), Y(0.9))], eye)


def _meander(p, p0, p1, p2, xs, hi="fire2", base="bronze", phase=0, edges=True):
    """The black-figure meander band of the bronze collar, painted along the
    curve p0-p1-p2 for the columns xs: ink key marks over a gold-lit band."""
    if not p.big:
        return
    key = ["###.", "#.#.", "#.##"]
    pts = bez(p0, p1, p2, n=240)
    for i, x in enumerate(xs):
        yc = int(round(min(pts, key=lambda q: abs(q[0] - (x + 0.5)))[1] - 0.5))
        if edges:
            p.px(x, yc - 2, "ink")
            p.px(x, yc + 2, "ink")
        for j in range(3):
            ch = key[j][(i + phase) % 4]
            p.px(x, yc - 1 + j, "ink" if ch == "#" else (hi if j == 0 else base))


# --------------------------------------------------------------------------
# Kynder, the hearth pup
# --------------------------------------------------------------------------

KYNDER_COLORS = [
    ("ink", INK),
    ("coat0", (120, 48, 24)), ("coat1", (176, 80, 40)), ("coat2", (216, 128, 72)), ("coat3", (240, 176, 120)),
    ("pale1", (216, 184, 136)), ("pale2", (248, 232, 192)),
    ("fire0", (208, 64, 32)), ("fire1", (240, 136, 40)), ("fire2", (248, 200, 64)), ("fire3", (248, 240, 168)),
    ("bronze", (192, 128, 48)), ("white", C.white), ("tongue", (232, 96, 112)), ("pink", (248, 168, 160)),
]
KYNDER_SHINY = {
    "coat0": (72, 72, 80), "coat1": (120, 120, 128), "coat2": (168, 168, 168), "coat3": (208, 208, 200),
    "pale1": (200, 200, 192), "pale2": (240, 240, 232),
    "fire0": (40, 72, 160), "fire1": (64, 128, 216), "fire2": (128, 192, 240), "fire3": (216, 240, 248),
}
KL = {"#": "ink", "0": "coat0", "1": "coat1", "2": "coat2", "3": "coat3", "a": "pale1", "b": "pale2",
      "r": "fire0", "o": "fire1", "g": "fire2", "y": "fire3", "z": "bronze", "w": "white", "t": "tongue",
      "k": "pink", "_": "_"}

coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.7])
coatI = Mat(["coat0", "coat1", "coat2", "coat3"], line="ink", cuts=[0.16, 0.42, 0.7])
pale = Mat(["pale1", "pale2"], line="coat1", cuts=[0.55])
bronze = Mat(["coat0", "bronze", "fire2"], line="coat0", cuts=[0.3, 0.62])

# Kynder's awake head, hand-drawn: a round skull, short soft-pointed ears,
# a cream muzzle with a nose pad, a cream cheek under a big eye with a
# two-pixel shine and a gold glint, and a panting tongue.
KHEAD = [
    "..........................",
    ".....##...........###.....",
    "....#33#.........#332#....",
    "....#332#.......#3322#....",
    "....#3321#.....#322k20#...",
    "....#33211#####322kk10#...",
    ".....#3211333332#2kkk0#...",
    ".....#3#11333333#22kk0#...",
    "......#3333333332#22k0#...",
    "......#33333333322#2210#..",
    "......#3333333322222221#..",
    "......#3333333222222221#..",
    ".....#333332##222222211#..",
    ".....#33222#ww#22222111#..",
    ".....#22222#w##22221110#..",
    "...##222222####22211110#..",
    ".###bbbbb22##g#22111100#..",
    ".####bbbba22##22111100#...",
    ".###bbbbaabaa2111110000#..",
    "..###bbaaabbaa1111000000#.",
    "..######aabbbaa100000000#.",
    "....##tt#aabbbaa000000##..",
    ".....##t####aaaa00000#....",
    ".......##...######000#....",
]


# Kynder's head turned right in profile for the back view, at 1.25x.
KBACKHEAD = [
    "......##..........##...........",
    ".....#33#........#22#..........",
    "....#3332#......#3221#.........",
    "....#3332#......#32k1#.........",
    "...#33322#.....#322k10#........",
    "...#33322#.....#32kk10#........",
    "...#33221#######2kkk10#........",
    "..#3332213333333#2kk10#........",
    "..#3332133333333322kk0#........",
    "..#33333333333333222k0#........",
    ".#3333333333333332222100#......",
    ".#33333333333333222222210#.....",
    ".#3333333333333322222221110#...",
    ".#3333333333332222##2221111#...",
    "#3333333333222222#ww#221110#...",
    "#2333333332222222#w##221110#...",
    "#2233333222222222####111111###.",
    "#2222222222222222##g#211100####",
    "#22222222222222222##211bbbb####",
    "#11222222222222222222bbbbbbb###",
    "#1111222222222222221bbbbbbbbb##",
    ".#1111122222222aaaaabbbbbbbbb#.",
    ".#011111122222abbbbbbbbbbbbbb#.",
    ".#00111111222abbbbbbbbbbaaaa##.",
    "..#00011111aabbbbbbaa########..",
    "..#000001111aaaaaaaa##ttkt#....",
    "...#0000011111aaaa##.#tttt#....",
    "....#00000011111###...#tt#.....",
    ".....##000000000#......##......",
    "......#########................",
]

# The dozing flame faces, hand-drawn: a hound's head made of fire, its ears
# flame tongues, its eye shut in a little arc, a nose pip at the snout. The
# far one curls the other way and looks back over the shoulder in its sleep.
KDREAM_FAR = [
    "...r.....r......",
    "..rgr...rgr.....",
    "..rgyr.rggor....",
    ".rgyygrggggor...",
    ".rgyyygggggor...",
    "rgyyygggggggor..",
    "rgyyggg0gg0ggor.",
    "rggygggg00ggggor",
    "roggggggggggg00r",
    "roogggggoooooor.",
    ".rooogggoooorr..",
    "..rrroooooor....",
    "....rrrrrrr.....",
]
KDREAM_NEAR = [
    "......r.....r.....",
    ".....ryr...rgr....",
    "....ryygr.rggor...",
    "...ryyyygrggggor..",
    "...ryyyyyyggggoor.",
    "..rgyyyyyggggggor.",
    ".rggy0yy0ggggggor.",
    "rggyyy00ggggggoor.",
    "r00yygggggggggoor.",
    ".roggggggggggooor.",
    "..rroogggggooorr..",
    "....rrroooooor....",
    ".......rrrrrrr....",
]


def _khead(p, cx, cy, s=1.0, f=-1, face=True, g=40, tongue=True):
    """Kynder's head as shapes around the skull center (cx, cy), facing
    left (f=-1) or right (f=1): the shapes behind KHEAD, for the back view,
    icons and followers. At battle size the face is painted on."""
    X = lambda d: cx - f * d * s
    Y = lambda d: cy + d * s
    p.lens((X(-4.0), Y(-5.6)), (X(-8.0), Y(-13.0)), 6.2 * s, coatI, bend=0.8 * s * -f, fat=0.36,
           group=g, bias=0.12)
    p.circle(X(0), Y(0), 9.2 * s, coatI, group=g + 1)
    for (ax, ay), (bx, by) in (((5.5, 4.4), (10.6, 7.4)), ((3, 6.4), (6.2, 10.6))):
        p.lens((X(ax), Y(ay)), (X(bx), Y(by)), 4.4 * s, coatI, bend=0.6 * s * f, fat=0.35, group=g + 1)
    p.blob(X(-8.3), Y(3.8), 5.2 * s, 3.5 * s, pale, ang=10 * -f, group=g + 2)
    p.blob(X(-6.5), Y(7.0), 3.7 * s, 1.9 * s, pale, group=g + 2)
    p.lens((X(2.8), Y(-6.4)), (X(6.0), Y(-13.6)), 7.0 * s, coatI, bend=-0.9 * s * -f, fat=0.36, group=g + 3)
    if not face:
        return
    if not p.big:
        p.px(X(-3.2), Y(-0.6), "ink")
        p.px(X(-13), Y(1.6), "ink")
        return
    # the big eye with its shine and gold glint, the nose pad, the smile
    ex = int(round(X(-3.2) - 2))
    ey = int(round(Y(-2.6)))
    p.eye(ex, ey, 4, 6, iris="fire2", shine_at=(1 if f < 0 else 2, 1))
    p.px(ex + (1 if f < 0 else 2), ey + 2, "white")
    nx = int(round(X(-13.2)))
    ny = int(round(Y(1.2)))
    p.pxs([(nx, ny), (nx + 1, ny), (nx, ny + 1), (nx + 1, ny + 1), (nx - f, ny - 1)], "ink")
    p.stroke([(X(-12.2), Y(5.0)), (X(-6.5), Y(5.6))], "ink")
    if tongue:
        tx = int(round(X(-9.5)))
        p.pxs([(tx, int(Y(6.6))), (tx - f, int(Y(6.6))), (tx, int(Y(6.6)) + 1)], "tongue")


def kynder(p, view, phase):
    if view in ("front", "side"):
        pant = 1 if (phase == 1 and view == "front") else 0
        walk = phase if view == "side" else 0
        HX, HY = 9, 22
        # stubby tail out behind the haunch, an ember at the tip
        _flame(p, (47.5, 56), (51, 49.5 - pant), 4.8, bend=-0.8)
        p.limb([(42, 59), (45.5, 58), (47.5, 56)], 4.4, 3.8, coat, group=20)
        # haunch and hind foot
        p.blob(38.5, 55.5, 6.8, 5.6, coat, group=21)
        p.blob(35, 59.8, 4.6, 2.0, coat, group=22, bias=0.05)
        # the ruff of fire the two faces doze in, rising behind them
        _flame(p, (45.5, 49), (46.5, 34 + pant), 5.6, bend=-1.4, hot=2)
        # far shoulder: a flame face curled the other way, looking back over
        # the shoulder in its sleep (the head that wakes first, on Dikyon)
        if not p.big:
            _dream(p, 39.5, 29.5 + pant, 1.0, f=1, g=60, licks=(), mat=DREAM_FAR)
        # far front leg and the shoulder
        far = [(29.5, 53), (30, 56), (30.5, 58.5)] if not walk else [(29.5, 53), (31.5, 56), (32.5, 58.5)]
        p.limb(far, 5.2, 4.8, coat, group=23, bias=0.25)
        p.blob(far[-1][0] + 0.5, 59.6, 3.8, 2.0, coat, group=23, bias=0.2)
        p.blob(34, 50.5, 7.5, 5, coat, group=26)
        # near shoulder: a flame face dozing with its chin on the collar
        if not p.big:
            _dream(p, 39.5, 44, 1.1, g=70, licks=())
        # chest bib, scalloped
        p.blob(24.5, 51.5, 7, 5.2, pale, group=24)
        for a, b in (((19, 51), (18.5, 55.5)), ((23, 53), (23, 57)), ((27.5, 53), (28, 57))):
            p.lens(a, b, 4.6, pale, fat=0.3, group=24)
        # near front leg and its big paw
        near = [(21.5, 55), (21.5, 57), (21.5, 58.5)] if not walk else [(21.5, 55), (19.5, 57), (18, 58.5)]
        p.limb(near, 6.4, 6.4, coat, group=25)
        p.blob(near[-1][0] - 0.5, 59.4, 4.8, 2.5, coat, group=25)
        # the bronze collar
        p.limb(bez((16.5, 47.5), (24, 51.5), (31.5, 48)), 3.6, 3.4, bronze, group=34)
        if p.big:
            p.patch(33, 23 + pant, KDREAM_FAR, KL)
            p.patch(HX, HY, KHEAD, KL)
            _meander(p, (16.5, 47.5), (24, 51.5), (31.5, 48), range(17, 31))
            p.patch(31, 37, KDREAM_NEAR, KL)
        else:
            _khead(p, HX + 14.5, HY + 13.5)
        return

    if view == "back":
        # over the shoulder at 1.25x: the back cropped by the frame, the awake
        # head turned right in profile, a flame face dozing on each shoulder
        _flame(p, (6, 56), (3, 45), 6, bend=1.0)
        p.limb([(9, 64), (7, 60), (6, 56)], 6, 5, coat, group=9)
        p.blob(28, 66, 26, 15, coat, group=1)
        p.blob(17, 61, 12, 8, coat, group=1)
        p.blob(36, 54, 15, 10, coat, group=1)
        _dream(p, 20, 43.5, 1.4, f=-1, g=60, licks=((3, 1, 8, -5, 5, -1.0),), mat=DREAM_FAR)
        p.limb([(38, 56), (40, 46), (41, 40)], 18, 16, coat, group=1)
        p.limb(bez((27, 45), (39, 51.5), (51, 44.5)), 4.4, 4.2, bronze, group=34)
        if p.big:
            p.patch(27, 9, KBACKHEAD, KL)
        else:
            _khead(p, 41.5, 25, 1.25, f=1)
        _dream(p, 50.5, 53, 1.35, f=1, g=70, licks=((3, 1, 7.5, -4.5, 4.6, -1.0),))
        _meander(p, (27, 45), (39, 51.5), (51, 44.5), range(28, 49))
        return

    if view == "icon":
        # party icon: the pup's big head, a flame face on each shoulder
        bob = phase
        _flame(p, (44, 52), (47, 44 - bob), 5, bend=-1)
        p.blob(34, 53, 9, 6, coat, group=1)
        p.blob(26, 58, 4.2, 2.4, coat, group=12)
        p.blob(36, 58.5, 4.2, 2.4, coat, group=13)
        _dream(p, 40, 38 - bob, 1.0, f=1, g=60, licks=(), mat=DREAM_FAR)
        _dream(p, 41, 48, 1.0, g=70, licks=())
        p.limb(bez((19, 48), (26, 52), (33, 48)), 3.4, 3.2, bronze, group=34)
        _khead(p, 24, 35 + bob)
        return

    if view in ("down", "up"):
        # follower: toward the camera (down) or walking away (up)
        step = phase
        back = view == "up"
        p.blob(32, 51, 9.5, 6.5, coat, group=1)
        for x, st in ((27.5, step), (36.5, 1 - step)):
            p.limb([(x, 54), (x, 58.5 - 1.5 * st)], 5, 4.6, coat, group=12 if x < 32 else 13)
            p.blob(x, 59.4 - 1.5 * st, 3.4, 1.9, coat, group=12 if x < 32 else 13)
        if back:
            p.limb([(32, 55), (34, 50), (35, 47)], 3.4, 3, coat, group=9)
            _flame(p, (35, 47), (36.5, 40 + step), 4.6)
        # a flame face dozing on each shoulder, curled outward
        _dream(p, 20.5, 46, 0.8, f=-1, g=60, licks=())
        _dream(p, 43.5, 46, 0.8, f=1, g=70, licks=())
        # the head, front-on (down) or from behind (up)
        p.lens((27, 29), (24.5, 20 + step), 6.8, coatI, bend=0.4, fat=0.45)
        p.lens((37, 29), (39.5, 20 + step), 6.8, coatI, bend=-0.4, fat=0.45)
        if p.big and not back:
            p.lens((27.2, 28), (25.4, 22 + step), 2.6, Mat(["pink"]), fat=0.45, noline=True, nooutline=True)
            p.lens((36.8, 28), (38.6, 22 + step), 2.6, Mat(["pink"]), fat=0.45, noline=True, nooutline=True)
        p.blob(32, 34, 8.6, 7.4, coatI, group=3)
        p.limb(bez((24.5, 42.5), (32, 46), (39.5, 42.5)), 3.2, 3.2, bronze, group=34)
        if not back:
            p.blob(32, 39, 5, 3.4, pale, group=4)
            p.blob(25, 38, 2.6, 2, pale, group=4)
            p.blob(39, 38, 2.6, 2, pale, group=4)
            p.eye(26.5, 31, 3, 4, iris="fire2", shine_at=(1, 0))
            p.eye(34.5, 31, 3, 4, iris="fire2", shine_at=(1, 0))
            p.pxs([(31.5, 36.5), (32.5, 36.5), (32, 37.5)], "ink")
            if p.big:
                p.stroke([(30, 40), (32, 39), (34, 40)], "ink")
                p.pxs([(31.5, 41), (32.5, 41), (32, 42)], "tongue")
        return


# --------------------------------------------------------------------------
# Dikyon, the twin hound (Orthros)
# --------------------------------------------------------------------------

DIKYON_COLORS = [
    ("ink", INK), ("dusk", (72, 32, 24)),
    ("coat0", (120, 48, 24)), ("coat1", (176, 80, 40)), ("coat2", (216, 128, 72)), ("coat3", (240, 176, 120)),
    ("pale1", (216, 184, 136)), ("pale2", (248, 232, 192)),
    ("fire0", (208, 64, 32)), ("fire1", (240, 136, 40)), ("fire2", (248, 200, 64)), ("fire3", (248, 240, 168)),
    ("bronze", (192, 128, 48)), ("white", C.white), ("tongue", (232, 96, 112)),
]
DIKYON_SHINY = {
    "dusk": (48, 48, 56),
    "coat0": (72, 72, 80), "coat1": (120, 120, 128), "coat2": (168, 168, 168), "coat3": (208, 208, 200),
    "pale1": (200, 200, 192), "pale2": (240, 240, 232),
    "fire0": (40, 72, 160), "fire1": (64, 128, 216), "fire2": (128, 192, 240), "fire3": (216, 240, 248),
}
DL = dict(KL)
DL.update({"d": "dusk", "k": "coat3"})

dleg = Mat(["dusk", "coat0", "coat1", "coat2"], line="dusk", cuts=[0.22, 0.46, 0.72], wy=0.55)

# Dikyon's heads, hand-drawn: a lean Cretan hound with tall ears, a bright
# almond eye under a brow, a long cream muzzle and an open jaw. The second
# head is the same face turned back over the shoulder, barking.
DHEAD = [
    "........#.......#......",
    ".......#3#.....#2#.....",
    ".......#32#...#3k1#....",
    "......#332#..#3kk10#...",
    "......#3321#.#32k10#...",
    ".....#333001132k210#...",
    ".....#33333##332110#...",
    "....#33333#ww#32110#...",
    "...#333333#w1#32211#...",
    "..#3333333#1g#222111#..",
    ".#233333333##22221110#.",
    "#1#3333332222222111100#",
    "#11#bbbbbb222221111100#",
    "#1#bbbbbbbbaa2211111#..",
    ".##11111bbbbaa21100#...",
    "..#dtkt#1bbaa22100#....",
    "...#wtt#1aaaa2100#.....",
    "....#aaaaaaa#0000#.....",
    ".....#######.####......",
]
DHEAD_BACK = [
    "......#.......#........",
    ".....#3#.....#2#.......",
    "....#3k3#...#22#.......",
    "...#33kk3#..#222#......",
    "...#33k33#.#3222#......",
    "...#333k331100222#.....",
    "...#333333##22222#.....",
    "...#33333#ww#22221#....",
    "...#33333#w1#222111#...",
    "..#333322#1g#2211110#..",
    ".#33222222##221111000#.",
    "#2222222222221111000#0#",
    "#222222222211bbbbbb#00#",
    "..#2222221aabbbbbbbb#0#",
    "...#00112aabbbb11111##.",
    "....#00122aabb1#tktd#..",
    ".....#0012aaaa1#ttw#...",
    ".....#0000#aaaaaaa#....",
    "......####.#######.....",
]

# the forward head turned right in profile for the back view, at 1.25x
DBACKHEAD = [
    "........#.........#...........",
    ".......#3#.......#2#..........",
    "......#3k3#.....#32#..........",
    "......#3kk3#...#3221#.........",
    ".....#33kk3#...#3221#.........",
    ".....#33kk32#.#32210#.........",
    ".....#333k33211322210#........",
    "....#33333333332222210#.......",
    "....#333333300112222110#......",
    "...#33333333333##222111#......",
    "...#3333333333#ww#221111#.....",
    "..#33333333332#w1#2211110#....",
    ".#333333322222#1g##21111000#..",
    ".#3333222222222##2211110000#..",
    "#2222222222222222211110000###.",
    "#22222222222222211bbbbbbbb#11#",
    ".##2222222221aaabbbbbbbbbbb#1#",
    "...#000111222aabbbbbb111111##.",
    "....#00122222aabbbb#dttkd#....",
    ".....#00122aaaaaab#ttwd#......",
    "......#0000#aaaaaaaa##........",
    ".......####.########..........",
]

def dikyon(p, view, phase):
    if view in ("front", "side"):
        snap = phase if view == "front" else 0
        walk = phase if view == "side" else 0
        # the tail, an ember at its tip
        _flame(p, (54.5, 37.5), (57, 29.5 - snap), 5.4, bend=-1.0)
        p.limb(bez((50, 41.5), (54, 41.5), (54.5, 37.5)), 4.2, 3.4, coat, group=9)
        # far legs, darkening to dusk at the paws
        fh = [(45, 45), (43, 51), (45.5, 55.5), (43.5, 59)] if not walk else [(45, 45), (46, 51), (48.5, 55.5), (47, 59)]
        ff = [(31, 47), (32, 53), (33.5, 58.5)] if not walk else [(31, 47), (29, 53), (27.5, 58.5)]
        p.limb(fh, 7.6, 4.4, dleg, bias=0.18, group=10)
        p.blob(fh[-1][0] - 0.5, 59.6, 4.0, 2.1, dleg, bias=0.18, group=10)
        p.limb(ff, 7.0, 4.4, dleg, bias=0.18, group=11)
        p.blob(ff[-1][0] - 0.5, 59.6, 4.0, 2.1, dleg, bias=0.18, group=11)
        # deep chest, tucked waist, hips
        p.blob(47, 42.5, 6.5, 6.5, coat, group=1)
        p.limb(bez((28, 45), (38, 47), (46, 43)), 11, 8, coat, group=1)
        p.blob(27.5, 44.5, 8, 7.5, coat, group=1)
        p.blob(22.5, 47.5, 4.6, 5, pale, group=2)
        for a, b in (((20.5, 49), (19.5, 53.5)), ((24, 51), (24, 55))):
            p.lens(a, b, 4.2, pale, fat=0.3, group=2)
        # near legs: the hind leg thrust back with its hock, the foreleg reaching
        nh = [(48, 44), (52, 50), (55.5, 55), (54, 59)] if not walk else [(48, 44), (50, 50), (51, 55), (49, 59)]
        nf = [(25, 48), (21, 53), (17.5, 57.5)] if not walk else [(25, 48), (25, 53), (24.5, 57.5)]
        p.limb(nh, 9.6, 4.8, dleg, group=12)
        p.blob(nh[-1][0] - 1, 59.6, 4.6, 2.3, dleg, group=12)
        p.limb(nf, 8.6, 5.0, dleg, group=13)
        p.blob(nf[-1][0] - 1, 59.4, 4.8, 2.4, dleg, group=13)
        # two necks: one forward, one turned back over the shoulder
        p.limb(bez((34, 42), (36, 36), (38, 29)), 9, 7.5, coat, group=20)
        p.limb(bez((29, 43), (26, 38), (22, 33)), 10, 8.5, coat, group=21)
        # the flame mane, behind the second neck at the withers, leaving the
        # dozing flame face its own place on the shoulder
        for a, b, w, bd in (((47.5, 42), (50, 32), 5.4, -1.2),):
            _flame(p, a, b, w, bend=bd, group=30)
        if not p.big:
            _dream(p, 33, 36, 1.0, f=-1, g=60, licks=())
        p.limb(bez((19, 39.5), (24.5, 43), (30.5, 39.5)), 3.8, 3.6, bronze, group=34)
        if p.big:
            p.patch(32, 13 - snap, DHEAD_BACK, DL)
            p.patch(26, 30, KDREAM_NEAR, DL)
            p.patch(7, 21, DHEAD, DL)
            _meander(p, (19, 39.5), (24.5, 43), (30.5, 39.5), range(19, 31))
        else:
            _khead(p, 42, 22 - snap, 0.9, f=1, face=True)
            _khead(p, 18, 29, 0.9, f=-1, face=True)
        return

    if view == "back":
        # over the shoulder at 1.25x: the forward head turned right in profile,
        # the second head on the far neck looking back, the third still a
        # flame face dozing between the shoulders
        _flame(p, (7, 57), (3, 44), 6.5, bend=1.0)
        p.limb([(11, 64), (8, 61), (7, 57)], 6, 5, coat, group=9)
        p.blob(31, 69, 31, 21, coat, group=1)
        p.blob(40, 55, 16, 11, coat, group=1)
        p.limb(bez((26, 52), (20, 44), (15, 36)), 13, 10, coat, group=2)
        p.limb(bez((41, 54), (43, 44), (44, 33)), 18, 15, coat, group=3)
        for a, b, w, bd in (((22, 48), (27, 33), 7, -1.2), ((30, 50), (33, 36), 7.5, -0.8),
                            ((48, 50), (56, 39), 7, -1.4), ((15, 47), (8, 37), 6, 1.2)):
            _flame(p, a, b, w, bend=bd, group=30)
        p.limb(bez((33, 39.5), (43, 46), (54, 39)), 4.6, 4.4, bronze, group=34)
        if p.big:
            p.patch(3, 17, DHEAD, DL)
            p.patch(19, 33, KDREAM_NEAR, DL)
            p.patch(32, 11, DBACKHEAD, DL)
            _meander(p, (33, 39.5), (43, 46), (54, 39), range(34, 53))
        else:
            _khead(p, 15, 24, 0.9, f=-1)
            _dream(p, 28, 38, 1.0, g=60, licks=())
            _khead(p, 46, 20, 1.15, f=1)
        return

    if view == "icon":
        bob = phase
        _flame(p, (47, 44), (50, 36 - bob), 5, bend=-1)
        for x in (24, 30, 37, 43):
            p.limb([(x, 48), (x - 1, 56)], 3.6, 3.2, dleg, group=12)
        p.blob(34, 46, 12, 5.5, coat, group=1)
        _dream(p, 33, 38, 0.9, g=60, licks=())
        _khead(p, 42, 27 - bob, 0.95, f=1)
        _khead(p, 21, 31, 0.95, f=-1)
        return

    if view in ("down", "up"):
        step = phase
        back = view == "up"
        p.blob(32, 48, 9, 7, coat, group=1)
        for x, st in ((27.5, step), (36.5, 1 - step)):
            p.limb([(x, 50), (x, 59.5 - 2 * st)], 4, 3.4, dleg, group=12 if x < 32 else 13)
            p.blob(x, 60 - 2 * st, 2.8, 1.6, dleg, group=12 if x < 32 else 13)
        if back:
            p.limb([(32, 50), (34, 44), (35, 39)], 3.4, 3, coat, group=9)
            _flame(p, (35, 39), (36, 32 + step), 4.4)
        for a, b in (((26, 42), (22, 33)), ((38, 42), (42, 33))):
            _flame(p, a, b, 5)
        _dream(p, 32, 41, 0.8, f=-1, g=60, licks=())
        for cx, face in ((22.5, -1), (41.5, 1)):
            p.lens((cx - 3, 26), (cx - 4.6, 18 + step), 5.4, coatI, bend=0.4, fat=0.4)
            p.lens((cx + 3, 26), (cx + 4.6, 18 + step), 5.4, coatI, bend=-0.4, fat=0.4)
            p.blob(cx, 29.5, 6.4, 6, coatI, group=3 if face < 0 else 4)
            if not back:
                p.blob(cx, 34.5, 4, 3.4, pale, group=3 if face < 0 else 4)
                p.eye(cx - 4, 27, 2, 3, iris="fire2", shine_at=(0, 0))
                p.eye(cx + 2, 27, 2, 3, iris="fire2", shine_at=(0, 0))
                p.pxs([(cx - 0.5, 32), (cx + 0.5, 32), (cx, 33)], "ink")
                if p.big:
                    p.pxs([(cx - 1, 36), (cx, 36)], "tongue")
            p.limb(bez((cx - 5, 36), (cx, 38.5), (cx + 5, 36)), 2.6, 2.6, bronze)
        return


# --------------------------------------------------------------------------
# Pylakyon, the gatehound (Kerberos)
# --------------------------------------------------------------------------

PYLAKYON_COLORS = [
    ("ink", INK), ("dusk", (64, 32, 32)),
    ("coat0", (112, 40, 24)), ("coat1", (168, 72, 40)), ("coat2", (208, 120, 72)), ("coat3", (240, 168, 120)),
    ("pale1", (216, 184, 136)), ("pale2", (248, 232, 192)),
    ("fire0", (208, 64, 32)), ("fire1", (240, 136, 40)), ("fire2", (248, 200, 64)),
    ("blue0", (40, 72, 152)), ("blue1", (80, 144, 216)), ("blue2", (168, 216, 248)),
    ("bronze", (192, 128, 48)),
]
PYLAKYON_SHINY = {
    "dusk": (40, 40, 48),
    "coat0": (72, 72, 80), "coat1": (112, 112, 120), "coat2": (160, 160, 168), "coat3": (200, 200, 200),
    "pale1": (192, 192, 192), "pale2": (232, 232, 232),
    "fire0": (24, 56, 120), "fire1": (48, 104, 176), "fire2": (112, 168, 224),
    "blue0": (64, 96, 160), "blue1": (136, 176, 224), "blue2": (216, 240, 248),
}
PL = {"#": "ink", "d": "dusk", "0": "coat0", "1": "coat1", "2": "coat2", "3": "coat3", "a": "pale1",
      "b": "pale2", "r": "fire0", "o": "fire1", "g": "fire2", "B": "blue0", "m": "blue1", "E": "blue2",
      "z": "bronze", "_": "_"}

pcoat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.7])
pcoatI = Mat(["coat0", "coat1", "coat2", "coat3"], line="ink", cuts=[0.16, 0.42, 0.7])
pdark = Mat(["dusk", "coat0", "coat1", "coat2"], line="dusk", cuts=[0.2, 0.46, 0.74])
pleg = Mat(["ink", "dusk", "coat0", "coat1", "coat2"], line="dusk", cuts=[0.12, 0.3, 0.52, 0.76], wy=0.75)
ppale = Mat(["pale1", "pale2"], line="pale1", cuts=[0.55])
pbronze = Mat(["coat0", "bronze", "fire2"], line="coat0", cuts=[0.3, 0.62])
serpent = Mat(["dusk", "coat0", "bronze", "fire2"], line="dusk", cuts=[0.24, 0.5, 0.8])
PFIRE = Mat(["fire0", "fire1", "fire2", "pale2"], line="fire0", outline="fire0")
PGHOST = Mat(["blue0", "blue1", "blue2"], line="blue0", outline="blue0")


def _gflame(p, a, b, w, bend=0.0, cool=0.52, **kw):
    """A flame of the underworld river: gold at the root, cooling to ghost-blue
    at the tip."""
    m = lerp(a, b, cool)
    p.lens(m, b, w * 0.78, PGHOST, bend=bend * 0.5, fat=0.25, flat=0, **kw)
    g = kw.pop("group", None)
    p.lens(lerp(a, b, cool + 0.06), lerp(b, a, 0.14), w * 0.34, PGHOST, fat=0.3, flat=1, noline=True,
           nooutline=True, **kw)
    e = lerp(a, b, cool + 0.14)
    p.lens(a, e, w, PFIRE, bend=bend * 0.6, fat=0.32, flat=1, group=g, **kw)
    p.lens(a, lerp(a, e, 0.66), w * 0.62, PFIRE, bend=bend * 0.4, fat=0.3, flat=2, noline=True,
           nooutline=True, **kw)
    if p.big:
        p.lens(a, lerp(a, e, 0.34), w * 0.3, PFIRE, bend=bend * 0.2, fat=0.3, flat=3, noline=True,
               nooutline=True, **kw)


# Pylakyon's three heads, hand-drawn hounds, all awake and snarling with open
# jaws: the near one lowered over the braced foreleg, biggest and brightest,
# its ears swept back; the middle one raised, muzzle up; the far one reared
# back and turned the other way, a step darker. Ghost-light eyes with dark
# pupils, limestone fangs, a red tongue.
PHEAD_NEAR = [
    ".................#......#...",
    "................#3#....#2#..",
    "...............#332#..#321#.",
    "...............#3321##3221#.",
    "..............#33321#32210#.",
    ".............#3333222322110#",
    "............#333332222221110#",
    "...........#3333322222211110#",
    "..........#33000112222111100#",
    "........##33#mE##222211111000#",
    "......##3333#E#B#22221111100#.",
    "....##333333111#222211111000#.",
    "..##333333222222222111110000#.",
    "##333322222222222211111000d#..",
    "#1#3222222222211111111000dd#..",
    "##1##111111111#1111100000d#...",
    ".#b#ddddddddd#a11110000dd#....",
    ".#ddrrrdddbd#aa1110000d#......",
    "..#dddddddb#aaa110000d#.......",
    "...#aaaaaaaa#aa10000d#........",
    "....#aaaaaa#.#0dddd#..........",
    ".....##aa##...####............",
    ".......##.....................",
]
PHEAD_MID = [
    "..................#....#.",
    ".................#3#..#2#",
    "................#332##321#",
    "..###..........#3332#3221#",
    ".#1#3#........#333322221#.",
    "#11#333#......#33332222110#",
    "##1#33333###.#333322221110#",
    ".#b#33333333##3330022211100#",
    "..#bdd2222333333#mE##211100#",
    "..#ddrdd122222333#E#B#21110#",
    "...#dddrdd1112222###2211100#",
    "...#bdddddb#111222222111000#",
    "....#aabbb#a11112221111000#.",
    ".....#aaa#aa11111111100dd#..",
    "......###aaa111110000dd#....",
    ".........#aaa100000dd#......",
    "..........#aa#0dddd#........",
    "...........###.####.........",
]
PHEAD_FAR = [
    "....#....#..................",
    "...#2#..#2#.................",
    "..#222##222#................",
    "..#2222#2222#..........###..",
    "...#222222222#........#1#0#.",
    ".#22222222222#......#111#00#",
    ".#222222222222#.###11111#0##",
    "#2222222222222##21111111#b#.",
    "#222222##Em#2222111111ddb#..",
    "#11111#B#E#222111111ddrdd#..",
    "#1111112###2111111ddrddd#...",
    "#111111111111111#bdddddb#...",
    ".#11111111111111a#bbbaa#....",
    "..#dddd000000000aa#aaa#.....",
    "....#dddddd00000aaa###......",
    "......#ddddddd0aaa#.........",
    "........#ddddd#aa#..........",
    ".........####.###...........",
]

# the near head turned right in profile, for the back view
PHEAD_BACK = [
    ".....#......#.................",
    "....#3#....#3#................",
    "...#333#..#333#...............",
    "...#3333##3333#...............",
    "...#33333#33333#..............",
    "..#3333333333333#.............",
    ".#333333333333333#............",
    ".#3333333333333333#...........",
    ".#33333333333333332#..........",
    "#333333333333##Em#22##........",
    ".#22333333333#B#E#2222##......",
    ".#223333333333#222222221##....",
    ".#222333333222222222221111##..",
    "..#d222222222222222211111000##",
    "..#dd2222222222222211111100#0#",
    "...#d2222222222#211111110##0##",
    "....#dd00001111a#ddddddddd#b#.",
    "......#d0000111aa#dbdddrrrdd#.",
    ".......#d000011aaa#bddddddd#..",
    "........#d00001aa#aaaaaaaa#...",
    "..........#dddd0#.#aaaaaa#....",
    "............####...##aa##.....",
    ".....................##.......",
]


HJAW = Mat(["pale1", "pale2"], line="pale1", cuts=[0.5])
HMOUTH = Mat(["dusk"], line="dusk")


def _hound(p, cx, cy, s=1.0, f=-1, ang=0.0, mouth=0.8, mat=None, g=80, pinned=0.0, eye="blue2"):
    """A mastiff's head built from curves around the skull center (cx, cy):
    a round skull and heavy cheek, a long muzzle tapering along a curved top
    line, an open jaw with a tongue and fangs, swept ears (pinned flat back
    as pinned goes to 1). f=-1 faces left; ang tilts the muzzle up. At battle
    size it gets a nose pad, fangs and an awake, fierce ghost-light eye."""
    mat = mat or pcoatI
    th = math.radians(ang if f < 0 else -ang)
    ca, sa = math.cos(th), math.sin(th)

    def T(lx, ly):
        lx, ly = lx * s, ly * s
        rx, ry = lx * ca - ly * sa, lx * sa + ly * ca
        return (cx + (rx if f < 0 else -rx), cy + ry)

    def TP(pts):
        return [T(x, y) for x, y in pts]
    m = mouth
    ex1 = lerp((6.6, -14.0), (12.0, -6.5), pinned)
    ex2 = lerp((0.4, -15.0), (8.0, -9.5), pinned)
    p.poly(TP(lens_pts((1.0, -3.0), ex1, 5.4, bend=-1.2, fat=0.32)), mat, group=g, bias=0.2)
    p.poly(TP([(-1.5, 3.2), (-13.5, 3.0), (-12.5, 5.0 + 3.4 * m), (-6, 6.8 + 1.6 * m), (-1.5, 6.4)]), HMOUTH,
           group=g + 1, flat=0)
    p.poly(TP(ribbon(bez((-3, 6.0 + 0.6 * m), (-7, 7.4 + 1.4 * m), (-11.8, 6.4 + 3.2 * m), n=10),
                     lambda t: 3.8 - 1.6 * t)), HJAW, group=g + 2)
    p.poly(TP(ellipse_pts(0, 0, 6.6, 6.0)), mat, group=g + 3)
    p.poly(TP(ellipse_pts(2.4, 3.6, 4.8, 4.0)), mat, group=g + 3)
    p.poly(TP(ribbon(bez((-2.5, 0.6), (-8.5, -0.8), (-14.0, 1.2), n=12), lambda t: 7.8 - 3.6 * t)), mat,
           group=g + 4)
    p.poly(TP(ellipse_pts(-13.6, 1.5, 2.0, 1.9)), mat, group=g + 4)
    p.poly(TP(ribbon(bez((-4, 3.0), (-9, 3.3), (-13.4, 2.8), n=8), lambda t: 2.4 - 0.8 * t)), HJAW,
           group=g + 4, noline=True, nooutline=True)
    p.poly(TP(lens_pts((-2.4, -3.6), ex2, 6.0, bend=-1.4, fat=0.32)), mat, group=g + 5)
    if not p.big:
        X, Y = T(-4.6, -1.5)
        p.px(X, Y, eye)
        return

    def at(lx, ly):
        X, Y = T(lx, ly)
        return int(math.floor(X)), int(math.floor(Y))
    d = 1 if f < 0 else -1
    nx, ny = at(-14.4, 0.4)
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 1)):
        p.fig.px(nx + dx * d, ny + dy, "ink")
    fx, fy = at(-10.6, 3.9)
    p.fig.px(fx, fy, "pale2")
    p.fig.px(fx, fy + 1, "pale2")
    lx, ly = at(-9.4, 6.2 + 2.6 * m)
    p.fig.px(lx, ly, "pale2")
    p.fig.px(lx, ly - 1, "pale2")
    tx, ty = at(-6.5, 5.6 + 1.2 * m)
    p.fig.px(tx, ty, "fire0")
    p.fig.px(tx - d, ty, "fire0")
    ex, ey = at(-4.6, -2.2)
    rows = ["..111", "11ee1", "1e8e1", ".111."]
    for j, r in enumerate(rows):
        r = r if f < 0 else r[::-1]
        for i, c in enumerate(r):
            if c != ".":
                p.fig.px(ex - 2 + i, ey - 1 + j, {"1": "ink", "e": eye, "8": "pale2"}[c])


def pylakyon(p, view, phase):
    if view in ("front", "side"):
        # weight thrown forward over a braced near foreleg: the near head
        # lowered and snarling, the middle head raised, the far head reared back
        rear = phase if view == "front" else 0
        walk = phase if view == "side" else 0
        # the burning mane behind the heads, streaming back and cooling to blue
        for a, b, w, bd in (((22, 32), (8, 12 - rear), 8, 2.4), ((40, 24), (42, 2 + rear), 8, -1.2),
                            ((44, 30), (56, 26), 6, -2.0)):
            _gflame(p, a, b, w, bend=bd, group=20)
        # the serpent tail rising in an S behind the body, its head reared to hiss
        p.limb(bez3((52, 40), (66, 35), (50, 28), (59, 20.5 - rear)), 7.4, 4.4, serpent, group=9)
        p.blob(58.5, 19 - rear, 4.2, 3.0, serpent, ang=-15, group=9)
        # far legs, darker, under the body
        fh = [(46, 45), (43, 51), (48, 55), (46, 59)]
        ff = [(31, 45), (32, 51), (30, 56), (29, 59)]
        if walk:
            fh = [(46, 45), (46, 51), (51, 55), (49, 59)]
            ff = [(31, 45), (29, 51), (26, 56), (24, 59)]
        p.limb(fh, 9, 4.6, pleg, bias=0.22, group=10)
        p.blob(fh[-1][0] - 1, 59.6, 4.6, 2.2, pleg, bias=0.22, group=10)
        p.limb(ff, 8.4, 4.6, pleg, bias=0.22, group=11)
        p.blob(ff[-1][0] - 1, 59.6, 4.6, 2.2, pleg, bias=0.22, group=11)
        # arched back, deep curved chest, tucked belly, rounded haunch
        p.limb(bez((30, 40), (42, 30), (54, 38)), 12, 11, pcoat, group=1)
        p.limb(bez((27, 45), (38, 48.5), (48, 44)), 15, 12, pcoat, group=1)
        p.blob(25, 43.5, 10.5, 10, pcoat, group=1)
        p.blob(50, 42.5, 8.5, 8.5, pcoat, group=2)
        # near hind leg driving back: stifle, hock, a big paw
        nh = [(51, 45), (50, 51), (56.5, 55), (55, 59)] if not walk else [(51, 45), (48, 51), (52, 55), (50, 59)]
        p.limb(nh, 11, 5.2, pleg, group=12)
        p.blob(nh[-1][0] - 1, 59.2, 5.6, 2.6, pleg, group=12)
        # the muscled shoulder and the braced near foreleg: elbow, wrist, big paw
        nf = [(24, 43), (22, 50), (16, 55.5), (12, 58.5)] if not walk else [(24, 43), (24, 50), (21, 55.5), (19, 58.5)]
        p.limb(nf, 12, 6, pleg, group=13)
        p.blob(nf[-1][0] - 1.5, 59.2, 6.4, 2.8, pleg, group=13)
        p.blob(26, 40, 7.5, 7, pcoat, group=14)
        # three necks rising from the shoulders
        p.limb(bez((41, 35), (47, 26), (50, 17)), 10, 7.5, pdark, group=21)
        p.limb(bez((32, 37), (32, 29), (32, 22)), 12, 9, pcoat, group=22)
        p.limb(bez((28, 41), (25, 38), (22, 35)), 13, 11, pcoat, group=23)
        # the fire mane at the root of the necks
        for a, b, w, bd in (((30, 38), (27, 26), 7, 1.4), ((37, 36), (39, 24), 7, -1.0),
                            ((44, 34), (50, 24), 6.5, -1.6)):
            _gflame(p, a, b, w, bend=bd, group=59, cool=0.62)
        # the bronze gorget across the chest
        p.limb(bez((14, 41), (25, 50), (36, 41)), 5, 5, pbronze, group=60, cap=False)
        # the heads: far reared back, middle raised, near lowered over the paw
        if p.big:
            p.patch(33, 1, PHEAD_FAR, PL)
            p.patch(12, 7 - rear, PHEAD_MID, PL)
            _meander(p, (14, 41), (25, 50), (36, 41), range(15, 36))
            p.patch(1, 27 + rear, PHEAD_NEAR, PL)
        else:
            _hound(p, 51, 13.5 - rear, 0.78, f=1, ang=26, mouth=0.9, mat=pdark, g=80)
            _hound(p, 31, 18 - rear, 1.0, f=-1, ang=12, mouth=1.0, g=90)
            _hound(p, 20, 37, 1.16, f=-1, ang=-10, mouth=0.9, g=100, pinned=0.85)
        return

    if view == "back":
        # over the shoulder at 1.25x: a broad muscled back with its spine and
        # shoulder blades, three necks rising from it into their heads, the
        # mane burning along the neck bases. The near head turns right in
        # profile, the middle one rears up behind it, the far one looks back.
        p.limb(bez3((11, 64), (2, 58), (10, 51), (4.5, 44)), 6.4, 4, serpent, group=9)
        p.blob(5, 42, 3.8, 2.8, serpent, ang=20, group=9)
        p.blob(31.5, 71, 30, 25, pcoat, group=1)
        p.blob(18, 53, 12, 9, pcoat, group=2)
        p.blob(46, 53, 13.5, 9.5, pcoat, group=3)
        # the necks, thick at the shoulders and running up into each head
        p.limb(bez((30, 48), (29, 31), (22, 13)), 13, 9, pdark, group=5)
        p.limb(bez((16, 50), (17, 42), (19, 34)), 15, 11, pcoat, group=4)
        p.limb(bez((45, 51), (45, 40), (41, 28)), 18, 13, pcoat, group=6)
        for a, b, w, bd in (((10, 47), (4, 36), 8, 1.4), ((29, 46), (33, 30), 9, -0.6),
                            ((54, 47), (59, 36), 8, -1.4)):
            _gflame(p, a, b, w, bend=bd, group=30, cool=0.6)
        p.limb(bez((8, 47), (31, 55), (56, 46)), 5, 5, pbronze, group=34)
        if p.big:
            p.patch(12, 1, PHEAD_FAR, PL)
            p.patch(1, 22, PHEAD_MID, PL)
            p.patch(33, 9, PHEAD_BACK, PL)
            _meander(p, (8, 47), (31, 55), (56, 46), range(9, 56))
        else:
            _hound(p, 22, 10, 0.8, f=1, ang=26, mat=pdark)
            _hound(p, 16, 26, 0.9, f=-1, ang=12)
            _hound(p, 46, 20, 1.1, f=1, ang=-8, pinned=0.85)
        return

    if view in ("down", "up"):
        step = phase
        back = view == "up"
        for x, st in ((25.5, step), (38.5, 1 - step)):
            p.limb([(x, 48), (x, 60 - 2 * st)], 5.6, 5, pleg, group=12)
            p.blob(x, 60.5 - 2 * st, 3.6, 1.8, pleg, group=12)
        p.blob(32, 45, 12, 8, pcoat, group=1)
        if back:
            p.limb([(32, 49), (35, 43), (36, 37)], 4, 3.4, serpent, group=9)
            p.blob(36.5, 35 + step, 3, 2.4, serpent, group=9)
        for a, b in (((22, 40), (16, 27)), ((42, 40), (48, 27)), ((28, 38), (26, 24)), ((36, 38), (38, 24))):
            _gflame(p, a, b, 6)
        for cx, cy, mat in ((18, 32, pcoatI), (46, 32, pdark), (32, 27, pcoatI)):
            p.lens((cx - 3, cy - 3), (cx - 5, cy - 11 + step), 5, mat, bend=0.4, fat=0.4)
            p.lens((cx + 3, cy - 3), (cx + 5, cy - 11 + step), 5, mat, bend=-0.4, fat=0.4)
            p.blob(cx, cy, 6.4, 6, mat, group=3)
            if not back:
                p.blob(cx, cy + 3.8, 4.4, 3.2, ppale, group=3)
                p.pxs([(cx - 3, cy - 1), (cx - 2, cy - 1), (cx + 2, cy - 1), (cx + 3, cy - 1)], "blue2")
                p.pxs([(cx - 1, cy + 2), (cx, cy + 2), (cx + 1, cy + 2)], "ink")
        p.limb(bez((19, 40), (32, 45), (45, 40)), 3.4, 3.4, pbronze, group=34)
        return


MONS = [
    Mon("Kynder", KYNDER_COLORS, KYNDER_SHINY, kynder, foot="paw", icon_pal=3),
    Mon("Dikyon", DIKYON_COLORS, DIKYON_SHINY, dikyon, foot="paw", icon_pal=3),
    Mon("Pylakyon", PYLAKYON_COLORS, PYLAKYON_SHINY, pylakyon, foot="bigpaw", icon_pal=3),
]
