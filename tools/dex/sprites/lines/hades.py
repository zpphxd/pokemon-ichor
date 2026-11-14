"""Nekranax (#151), the Shade Lord: Hades's lot of the murky dark.

Direction B, "The Elemental Titans". The Cyclopes forged one war-gear for
the three sons of Kronos: the same Corinthian helm and muscled cuirass. Inside
Nekranax's gear, bronze gone black as basalt, the body is the dark below.
Shadow fills the hulking shell and seeps violet from its joints, its arms are
smoke between the plates, its crest is a plume of shadow pouring up out of
the helm, and below the belt it sags into a ghost-tail of shadow tongues. Its
gauntlets are the bident: each ends in twin gold talons. It has no face, only
its lot's emblem, a bident, glowing ghost-violet in the T of the visor.
"""
from mon_lib import Mat, Mon, bez, bez3

COLORS = [
    ("ink", (16, 8, 24)),
    # the black war-shell: bronze gone dark as basalt, polished to a sheen
    ("k0", (32, 24, 48)), ("k1", (64, 56, 96)), ("k2", (112, 104, 152)), ("k3", (184, 176, 216)),
    # shadow, lit violet from within
    ("s0", (48, 32, 80)), ("s1", (88, 64, 136)), ("s2", (144, 112, 200)),
    # ghost-light, the signature glow
    ("v0", (168, 104, 248)), ("v1", (208, 168, 248)), ("v2", (248, 232, 248)),
    # the wealth under the earth, and red-figure trim
    ("g0", (168, 104, 40)), ("g1", (240, 184, 72)), ("g2", (248, 240, 176)),
    ("t0", (192, 80, 56)),
]
# The shell turns marble-white like a grave stele and the ghost-light turns
# sun-gold; the gold talons darken to old bronze so they still stand apart.
SHINY = {
    "k0": (104, 96, 104), "k1": (168, 160, 160), "k2": (216, 208, 200), "k3": (248, 248, 240),
    "v0": (200, 144, 40), "v1": (240, 192, 64), "v2": (248, 240, 176),
    "g0": (88, 48, 24), "g1": (152, 96, 40), "g2": (208, 160, 80),
}

shell = Mat(["k0", "k1", "k2", "k3"], line="ink", cuts=[0.26, 0.52, 0.8])
shell_hi = Mat(["k0", "k1", "k2", "k3"], line="ink", cuts=[0.2, 0.44, 0.72])
shade = Mat(["s0", "s1", "s2"], line="s0", outline="ink", cuts=[0.4, 0.74])
smoke = Mat(["s0", "s1", "s2"], line="s0", outline="ink", cuts=[0.34, 0.68])
gold = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.36, 0.7])
ghost = Mat(["v0", "v1"], line="v0", cuts=[0.5])


def path(*segs):
    out = []
    for s in segs:
        if out and s and out[-1] == s[0]:
            s = s[1:]
        out.extend(s)
    return out


# --------------------------------------------------------------------------
# The helm: the brothers' one Corinthian helm (see zeus.py), here black
# bronze with a gold bead, and the bident in the T.
# --------------------------------------------------------------------------

HELM = [
    "......#####.......",
    "....##44433##.....",
    "...#444443332#....",
    "..#34444333221#...",
    "..#33443333221#...",
    ".#bbbbbbbbbb3211#.",
    ".#vvvvvvvvvv2110#.",
    "#2vvvvvvvvvv21100#",
    "#3vvvvvvvvv221100#",
    "#23vvvvvvv3221100#",
    ".#23vvvv2b3211000#",
    ".#232vv2b32110000#",
    ".#232vv2b3211#000#",
    ".#122vv2b211#.#00#",
    "..#12vv2b210#..##.",
    "..#11#vv#b1#......",
    "...##..#.##.......",
]
# Hades's lot: a bident, two prongs over a crossbar and a shaft
BIDENT = [
    "", "", "", "", "", "",
    "...hc...ch",
    "...hc...ch",
    "....hccch",
    "......c",
    ".....hc",
    ".....hc",
    ".....hc",
    ".....hc",
    "......c",
]
HELM_LEGEND = {"#": "ink", "v": "ink", "0": "k0", "1": "k1", "2": "k2", "3": "k3", "4": "k3", "b": "g1",
               "c": "v2", "h": "v0"}

HELM_SIDE = [
    "......######.......",
    "....##444333##.....",
    "...#4444443332#....",
    "..#344444333322#...",
    "..#334444333222#...",
    ".#23344433332221#..",
    ".#22333333332221#..",
    ".#122333333bbbbbb#.",
    ".#12233333#hcchcc#.",
    ".#1122333332#hch#..",
    ".#11223333332##21#.",
    ".#011222333221112#.",
    ".#0111222322111112#",
    ".#00111222#1211112#",
    ".#0011112#.#21111#.",
    "#00#0011#..#2111#..",
    "#0#.#00#...#2111#..",
    "##..##.....#b111#..",
    "...........#b11#...",
    "............#b1#...",
    ".............##....",
]


def helm_rows(glyph=BIDENT):
    rows = [list(r) for r in HELM]
    for j, r in enumerate(glyph):
        for i, ch in enumerate(r):
            if ch in "ch" and j < len(rows) and i < len(rows[j]) and rows[j][i] == "v":
                rows[j][i] = ch
    return ["".join(r) for r in rows]


def helm(p, x, y):
    if p.big:
        p.patch(x, y, helm_rows(), HELM_LEGEND)
        return
    p.poly([(x + 3, y + 3), (x + 9, y), (x + 15, y + 3), (x + 17, y + 13), (x + 13, y + 16), (x + 3, y + 16),
            (x + 0.5, y + 8)], shell, group=90)
    p.stroke([(x + 2, y + 7), (x + 10, y + 7)], "ink")
    p.stroke([(x + 5.5, y + 8), (x + 5.5, y + 15)], "ink")
    p.px(x + 4, y + 7, "v1")
    p.px(x + 8, y + 7, "v1")
    p.px(x + 6, y + 9, "v0")


def helm_side(p, x, y):
    if p.big:
        p.patch(x, y, HELM_SIDE, HELM_LEGEND)
        return
    p.poly([(x + 2, y + 15), (x + 2, y + 5), (x + 9, y), (x + 16, y + 4), (x + 18, y + 13), (x + 15, y + 20),
            (x + 12, y + 14), (x + 6, y + 17)], shell, group=200)
    p.px(x + 14, y + 8, "v1")


# --------------------------------------------------------------------------
# Shapes
# --------------------------------------------------------------------------

def tongue(p, a, b, w, mat, group, bend=0.0, fat=0.3, **kw):
    """A tongue of shadow or smoke: fat at its root, pointed at the tip."""
    return p.lens(a, b, w, mat, bend=bend, fat=fat, group=group, **kw)


def talon(p, a, b, w, group, bend=0.0):
    """One gold prong of the bident: a curved, tapering talon."""
    pts = bez(a, ((a[0] + b[0]) / 2 + bend, (a[1] + b[1]) / 2), b)
    return p.taper(pts, w, gold, group=group)


def gauntlet(p, cx, cy, r, group, phase=0, raised=False):
    """A great black gauntlet whose two gold talons are the bident's prongs:
    a gold cuff for the bident's crossbar, two long prongs curving to points."""
    sp = 0.5 * phase
    d = -1 if raised else 1
    for k, side in enumerate((-1, 1)):
        a = (cx + side * r * 0.45, cy + d * r * 0.55)
        b = (cx + side * (r * 0.62 + sp), cy + d * r * 2.35)
        talon(p, a, b, 4.2, group + 1 + k, bend=side * 1.0 * d)
    p.blob(cx, cy, r, r * 0.86, shell_hi, group=group)
    yb = cy + d * r * 0.5
    p.rect(cx - r * 0.86, min(yb, yb + d * 1.2), cx + r * 0.86, max(yb, yb + d * 1.2), gold, group=group + 3)


# --------------------------------------------------------------------------
# Battle front: 3/4 view facing left, sagging low into its ghost-tail
# --------------------------------------------------------------------------

HX, HY = 21, 16


def wisp(p, pts, w0, w1, group, bias=0.0):
    """A curling wisp of shadow along a cubic path, tapering from w0 to w1."""
    return p.limb(bez3(*pts, n=20), w0, w1, smoke, group=group, bias=bias)


# The brothers' crest, here a plume of shadow: the same Corinthian arc as
# Olympanax's lightning and Pontanax's fin, with smoke tongues pouring up
# off its crown.
CREST = path(bez3((21.5, 19), (21, 13), (26, 11.4), (32, 11.4)), bez3((32, 11.4), (40, 11.6), (47, 16), (50, 26)),
             [(47.5, 27)], bez3((47.5, 27), (44, 21), (39, 17.5), (32, 16.5)), [(25, 18.5)])
PLUME = [((24.5, 13), (21, 4.4), 4.6, 1.2), ((29.5, 11.8), (29.6, 2.4), 5.4, -1.2), ((35.5, 12), (39.4, 2.6), 5.6, -1.8),
         ((41, 14.2), (47.6, 5.2), 5.4, -1.8), ((45.6, 18.4), (54, 11.6), 4.8, -1.6), ((48.4, 23), (57.6, 19.6), 4.0, -1.2)]


FLAMES = [((24, 13.4), (21, 9), (20, 5), (23, 3.4)), ((29, 12), (27.6, 7), (29, 3), (33, 2.6)),
          ((35, 12.2), (35.6, 7), (39, 3.6), (43, 4.2)), ((41, 14.4), (43.6, 9.6), (48, 7), (52, 8.4)),
          ((45.6, 18.6), (49.6, 15), (54, 13.6), (57.6, 15.6)), ((48.4, 23.4), (52.6, 21.6), (56.6, 21.6), (59.6, 24))]


def _front_plume(p, phase):
    """The plume of shadow: the crest's arc, with tongues of smoke pouring
    up off it, each curling back over at its tip."""
    s = phase
    for k, (a, b, c, d) in enumerate(FLAMES):
        dd = s if k % 2 else -s
        p.limb(bez3(a, (b[0], b[1] + dd * 0.5), (c[0] + dd * 0.6, c[1] + dd), (d[0] + dd, d[1] + dd), n=20),
               5.6, 2.4, smoke, group=5 + k, bias=0.04 * (k % 2))
    p.poly(CREST, smoke, group=12, bias=-0.06)


def _front_tail(p, phase):
    """Below the belt the shell gives out: shadow tongues sagging into a
    ghost-tail that sweeps back and curls."""
    sw = phase
    p.poly(path(bez3((18, 44), (19, 52), (26, 57), (34, 58)), bez3((34, 58), (41, 59), (47, 57), (47, 53 - sw)),
                bez3((47, 53 - sw), (47, 50), (44, 50), (43, 53)), bez3((43, 53), (41, 55), (37, 54), (40, 44))),
           smoke, group=20)
    for k, (x, ln, bend) in enumerate(((19, 11, -1.4), (24, 13, 1.2), (29, 14, -1.0), (34, 12, 1.4), (39, 9, -1.2))):
        tongue(p, (x, 44), (x + bend * 1.2, 44 + ln + (sw if k % 2 else 0)), 5.6, smoke, group=21 + k % 2,
               bend=bend * 1.2, bias=0.06 * (k % 2))


def _front_body(p, phase):
    ph = phase
    big = p.big
    # ---- shadow arms hanging from under the pauldrons, the great gauntlets
    p.limb([(11, 30), (9, 40)], 7.8, 7.4, shade, group=40)
    gauntlet(p, 9, 45.5, 6.2, 41, ph)
    p.limb([(51, 31), (53.5, 40)], 7.8, 7.4, shade, group=50, bias=0.06)
    gauntlet(p, 53.5, 45.5, 6.4, 51, ph)
    # ---- shadow seeping at the neck
    p.blob(29.5, 33, 7.0, 3.6, shade, group=60)
    # ---- the cuirass: a black muscled shell
    p.poly(path(bez3((18, 34), (22, 31.5), (36, 31.5), (42, 34)), bez3((42, 34), (45, 39), (43, 43), (42, 47)),
                bez((42, 47), (30, 49.5), (18, 47)), bez3((18, 47), (17.5, 43), (15, 38.5), (18, 34))),
           shell_hi, group=100, bias=0.04)
    if big:
        p.blob(23, 36.8, 4.6, 3.6, shell_hi, group=101, noline=True, bias=-0.04)
        p.blob(33, 37, 6.2, 4.0, shell_hi, group=102, noline=True, bias=-0.02)
        for k, (cx, cy, rx, ry) in enumerate(((25, 42.2, 2.4, 1.6), (31.4, 42.4, 3.0, 1.6))):
            p.blob(cx, cy, rx, ry, shell_hi, group=103 + k, noline=True)
        p.shade([(37, 31), (45, 35), (45, 48), (37, 48)], 0.08)
    p.poly(path(bez((17.6, 44.8), (30, 47.4), (42.4, 44.8)), [(42.6, 47.6)], bez((42.6, 47.6), (30, 50.2), (17.4, 47.6))),
           shell, group=112, bias=0.12)
    # ---- the pauldrons: huge, the helm sunk low between them
    p.poly(path(bez3((38, 32), (38, 22), (46, 18.5), (53, 19.5)), bez3((53, 19.5), (61, 21), (62, 29), (58, 33)),
                [(47, 34.5)]), shell_hi, group=130, bias=0.04)
    p.poly(path(bez3((23, 32), (23, 23), (16, 20), (10.5, 21)), bez3((10.5, 21), (3.6, 22.5), (3.4, 29.5), (6.5, 33)),
                [(15, 34.5)]), shell_hi, group=131, bias=0.02)
    # ---- the helm
    helm(p, HX, HY - ph)


def _front(p, phase):
    _front_plume(p, phase)
    _front_tail(p, phase)
    _front_body(p, phase)


# --------------------------------------------------------------------------
# Battle back: over the shoulder, helm in profile, a gauntlet raised
# --------------------------------------------------------------------------

BCREST = path(bez3((43.5, 21.5), (44, 13), (38, 10.6), (33, 11)), bez3((33, 11), (26, 11.6), (22, 17), (20, 27)),
              [(23, 28)], bez3((23, 28), (25, 21), (29, 17.5), (35, 18)), [(41, 22)])
BFLAMES = [((42, 14), (43, 9), (41, 5), (37, 4)), ((37, 11.4), (36.6, 6), (33, 2.6), (28.6, 3)),
           ((31, 11.8), (28, 7), (23, 5), (19, 6.6)), ((26, 13.6), (22, 10.4), (17, 10), (13.6, 12.4)),
           ((22.6, 18), (18, 16.6), (13, 17.6), (10, 20.4)), ((20.6, 23.6), (16, 23.4), (11.6, 25.6), (9, 28.6))]


def _back_plume(p, phase):
    s = phase
    for k, (a, b, c, d) in enumerate(BFLAMES):
        dd = s if k % 2 else -s
        p.limb(bez3(a, (b[0], b[1] + dd * 0.5), (c[0] - dd * 0.6, c[1] + dd), (d[0] - dd, d[1] + dd), n=20),
               6.0, 2.6, smoke, group=5 + k, bias=0.04 * (k % 2))
    p.poly(BCREST, smoke, group=12, bias=-0.06)


def _back_body(p, phase):
    # the shadow below, filling the frame's foot
    p.poly([(4, 64), (6, 54), (16, 50), (48, 50), (58, 54), (60, 64)], smoke, group=20)
    # far arm hanging (left), shadow and gauntlet cropped by the frame
    p.limb([(10, 46), (8, 58)], 8.4, 7.6, shade, group=30)
    p.blob(8, 61, 6.0, 5.0, shell_hi, group=31)
    # back plate
    p.poly(path(bez3((14, 54), (17, 47), (25, 45), (32, 45)), bez3((32, 45), (39, 45), (47, 47), (49, 54)),
                [(48, 64), (15, 64)]), shell_hi, group=40)
    if p.big:
        p.blob(25, 52, 6.6, 5.4, shell_hi, group=41, noline=True, bias=-0.02)
        p.blob(39, 52, 6.2, 5.2, shell_hi, group=42, noline=True, bias=0.04)
    p.limb([(37, 38), (33, 45)], 8.4, 10.4, shade, group=43)
    # pauldrons
    p.poly(path(bez3((24, 50), (24, 41), (16, 37.5), (10, 38.5)), bez3((10, 38.5), (2.6, 40), (2.6, 48), (6, 52)),
                [(16, 53)]), shell_hi, group=44)
    p.poly(path(bez3((38, 50), (38, 42), (45, 38.5), (51, 39.5)), bez3((51, 39.5), (58, 41), (58.6, 48), (55, 52)),
                [(46, 53)]), shell, group=45)
    # the gauntlet raised, talons up
    p.limb([(52, 46), (55.5, 33)], 8.0, 7.2, shade, group=50)
    gauntlet(p, 55.5, 28, 6.0, 51, phase, raised=True)
    helm_side(p, 29, 20 - phase)


def _back(p, phase):
    _back_plume(p, phase)
    _back_body(p, phase)


# --------------------------------------------------------------------------
# Follower views
# --------------------------------------------------------------------------

def _follow_body(p, bob, back=False):
    # ghost-tail
    p.poly([(22, 44 + bob), (42, 44 + bob), (40, 52 + bob), (34, 56), (30, 60), (27, 54), (22, 50 + bob)], smoke,
           group=10)
    p.poly(path(bez3((19, 30 + bob), (25, 27 + bob), (39, 27 + bob), (45, 30 + bob)),
                bez3((45, 30 + bob), (47, 37 + bob), (43, 42 + bob), (43, 46 + bob)),
                bez((43, 46 + bob), (32, 49 + bob), (21, 46 + bob)),
                bez3((21, 46 + bob), (21, 42 + bob), (17, 37 + bob), (19, 30 + bob))), shell_hi, group=60)
    p.rect(20, 43 + bob, 43, 45 + bob, shell, group=61)
    if back and p.big:
        p.stroke([(32, 31 + bob), (32, 42 + bob)], "ink")
    p.blob(15, 28 + bob, 7.6, 6, shell_hi, group=62)
    p.blob(49, 28 + bob, 7.6, 6, shell_hi, group=63)
    for side, gx in ((-1, 11), (1, 53)):
        p.limb([(gx - side * 2, 32 + bob), (gx, 44 + bob)], 6, 5.4, shade, group=64 + side)
        talon(p, (gx - 2, 47 + bob), (gx - 3, 57), 3.8, 70 + side)
        talon(p, (gx + 2, 47 + bob), (gx + 3, 57), 3.8, 72 + side)
        p.blob(gx, 46 + bob, 4.4, 3.8, shell_hi, group=74 + side)
    # ghost-light under the pauldrons and the hem
    p.stroke([(9, 33 + bob), (20, 33 + bob)], "v0")
    p.stroke([(44, 33 + bob), (55, 33 + bob)], "v0")
    p.stroke([(22, 46 + bob), (41, 46 + bob)], "v1")
    p.stroke([(30, 49 + bob), (32, 55)], "v0")


def _down(p, phase):
    bob = phase
    for k, (a, b, w, bend) in enumerate((((30, 17 + bob), (25, 5 + bob), 6.0, 1.2), ((32, 16 + bob), (36, 3 + bob), 7.0, -1.6),
                                         ((34, 17 + bob), (44, 8 + bob), 6.0, -1.6))):
        tongue(p, a, b, w, smoke, group=5 + k, fat=0.34, bend=bend)
    _follow_body(p, bob)
    p.poly([(23, 18 + bob), (26, 12 + bob), (32, 10 + bob), (38, 12 + bob), (41, 18 + bob), (41, 27 + bob),
            (35, 30 + bob), (29, 30 + bob), (23, 27 + bob)], shell_hi, group=71)
    p.rect(25, 17 + bob, 38, 19 + bob, Mat(["ink"]), group=72, flat=0, noline=True)
    p.rect(31, 20 + bob, 33, 29 + bob, Mat(["ink"]), group=73, flat=0, noline=True)
    p.pxs([(28, 17 + bob), (36, 17 + bob)], "v1")
    p.stroke([(28, 18 + bob), (36, 18 + bob)], "v0")
    p.stroke([(32, 19 + bob), (32, 27 + bob)], "v1")


def _up(p, phase):
    bob = phase
    for k, (a, b, w, bend) in enumerate((((30, 17 + bob), (25, 5 + bob), 6.0, 1.2), ((32, 16 + bob), (36, 3 + bob), 7.0, -1.6),
                                         ((34, 17 + bob), (44, 8 + bob), 6.0, -1.6))):
        tongue(p, a, b, w, smoke, group=5 + k, fat=0.34, bend=bend)
    _follow_body(p, bob, back=True)
    p.poly([(23, 18 + bob), (26, 12 + bob), (32, 10 + bob), (38, 12 + bob), (41, 18 + bob), (43, 28 + bob),
            (37, 29 + bob), (27, 29 + bob), (21, 28 + bob)], shell_hi, group=71)
    if p.big:
        p.stroke([(25, 17 + bob), (39, 17 + bob)], "g1")


def _icon(p, phase):
    """Party icon: the helm sunk between the great pauldrons, the plume above,
    the gold talons below."""
    ox, oy = 17, 18
    up = phase
    for k, (a, b, w, bend) in enumerate((((ox + 12, oy + 7), (ox + 9, oy + 0.6 - up), 4.4, 0.8),
                                         ((ox + 14, oy + 7), (ox + 17, oy + 0.4), 5.0, -1.2),
                                         ((ox + 16, oy + 8), (ox + 25, oy + 2.4 + up), 5.0, -1.6),
                                         ((ox + 17, oy + 10), (ox + 30, oy + 9), 4.4, -1.2))):
        tongue(p, a, b, w, smoke, group=5 + k % 2, fat=0.34, bend=bend)
    p.poly([(ox + 9, oy + 24), (ox + 21, oy + 24), (ox + 18, oy + 28), (ox + 12, oy + 28)], smoke, group=8)
    for side, gx in ((-1, ox + 3.4), (1, ox + 26.6)):
        talon(p, (gx - 1.4, oy + 23), (gx - 2.0, oy + 28), 2.4, 10 + side)
        talon(p, (gx + 1.4, oy + 23), (gx + 2.0, oy + 28), 2.4, 12 + side)
        p.blob(gx, oy + 21.4, 3.2, 2.8, shell_hi, group=14 + side)
        p.rect(gx - 2.4, oy + 23, gx + 2.4, oy + 23.6, gold, group=16 + side)
    p.poly([(ox + 8, oy + 18), (ox + 22, oy + 18), (ox + 21, oy + 25), (ox + 9, oy + 25)], shell_hi, group=30)
    p.blob(ox + 5, oy + 15.5, 5.4, 4.2, shell_hi, group=31)
    p.blob(ox + 25, oy + 15.5, 5.4, 4.2, shell_hi, group=32)
    helm(p, ox + 6, oy + 6 - up)


# At follower size the black shell turns to a silhouette, so the follower and
# side views draw it a step lighter, the smoke lit violet from within.
LIGHT = {
    "shell_hi": Mat(["k1", "k2", "k3"], line="ink", cuts=[0.34, 0.68]),
    "shell": Mat(["k1", "k2"], line="ink", cuts=[0.5]),
    "smoke": Mat(["s1", "s2", "v0"], line="s0", outline="ink", cuts=[0.4, 0.8]),
    "shade": Mat(["s1", "s2"], line="s0", outline="ink", cuts=[0.5]),
}


def nekranax(p, view, phase):
    if not p.big and view != "icon":
        g = globals()
        saved = {k: g[k] for k in LIGHT}
        g.update(LIGHT)
        try:
            _draw(p, view, phase)
        finally:
            g.update(saved)
        return
    _draw(p, view, phase)


def _draw(p, view, phase):
    if view == "icon":
        _icon(p, phase)
    elif view in ("front", "side"):
        _front(p, phase)
    elif view == "back":
        _back(p, phase)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)


MONS = [
    # icon palette 2 keeps the shell gray-violet and the plume purple
    Mon("Nekranax", COLORS, SHINY, nekranax, foot="blank", icon_pal=2),
]
