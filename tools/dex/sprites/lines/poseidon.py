"""Pontanax (#150), the Sea Lord: Poseidon's lot of the gray sea.

Direction B, "The Elemental Titans". The Cyclopes forged one war-gear for
the three sons of Kronos: the same Corinthian helm and muscled cuirass.
Inside Pontanax's gear, gone green with the sea's patina, the body is the sea.
Water fills the verdigris cuirass and spills from its joints, its arms are
water between bronze-bound plates, and below the belt it is a swell that
rises behind it into a great curling wave breaking over its head. The crest
of its helm is a fin of water. Its raised far hand is the trident: past the
vambrace the hand is three tines of water, foam glowing at their points.
It has no face, only its lot's emblem, a trident, glowing sea-cyan in the T
of the visor.
"""
from mon_lib import Mat, Mon, bez, bez3

COLORS = [
    ("ink", (16, 24, 48)),
    # the sea, from the abyss in the curl to the lit face of the wave
    ("abyss", (8, 24, 72)), ("w0", (16, 48, 120)), ("w1", (32, 88, 168)), ("w2", (64, 144, 216)),
    ("w3", (136, 200, 240)), ("foam", (240, 248, 248)),
    # verdigris: the bronze gone green
    ("v0", (24, 64, 72)), ("v1", (40, 112, 104)), ("v2", (88, 168, 136)), ("v3", (160, 216, 176)),
    # bare bronze where the patina wears
    ("b0", (128, 72, 32)), ("b1", (216, 160, 72)),
    # the glassy green of thin water at the top of the wave
    ("glass", (80, 184, 200)),
    # the signature glow
    ("glow", (104, 240, 224)),
]
# The patina is scoured off: bright new bronze in sun-gold, the glow gone to
# white-gold.
SHINY = {
    "v0": (112, 64, 24), "v1": (184, 120, 40), "v2": (232, 176, 64), "v3": (248, 224, 136),
    "b0": (88, 48, 24), "b1": (152, 96, 40), "glow": (248, 240, 168),
}

water = Mat(["w0", "w1", "w2", "w3"], line="w0", cuts=[0.24, 0.5, 0.76])
water_d = Mat(["abyss", "w0", "w1", "w2"], line="abyss", cuts=[0.3, 0.56, 0.8])
foam_m = Mat(["w3", "foam"], line="w2", cuts=[0.5])
verd = Mat(["v0", "v1", "v2", "v3"], line="v0", cuts=[0.2, 0.44, 0.7])
verd_hi = Mat(["v0", "v1", "v2", "v3", "foam"], line="v0", cuts=[0.16, 0.38, 0.6, 0.86])
bronze = Mat(["b0", "b1"], line="b0", cuts=[0.5])
tine_m = Mat(["w2", "w3", "foam"], line="w1", cuts=[0.4, 0.7])


def path(*segs):
    out = []
    for s in segs:
        if out and s and out[-1] == s[0]:
            s = s[1:]
        out.extend(s)
    return out


# --------------------------------------------------------------------------
# The helm: the brothers' one Corinthian helm (see zeus.py), here verdigris,
# with the trident in the T.
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
# Poseidon's lot: a trident, three tines over a crossbar and a shaft
TRIDENT = [
    "", "", "", "", "", "",
    "..hc..c..ch",
    "...c..c..c",
    "....c.c.c",
    ".....ccc",
    "......c",
    ".....hc",
    "......c",
    ".....hc",
    "......c",
]
HELM_LEGEND = {"#": "ink", "v": "ink", "0": "v0", "1": "v1", "2": "v2", "3": "v3", "4": "v3", "b": "b1",
               "c": "foam", "h": "glow"}

HELM_SIDE = [
    "......######.......",
    "....##444333##.....",
    "...#4444443332#....",
    "..#344444333322#...",
    "..#334444333222#...",
    ".#23344433332221#..",
    ".#22333333332221#..",
    ".#122333333bbbbbb#.",
    ".#12233333#hchchc#.",
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


def helm_rows(glyph=TRIDENT):
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
            (x + 0.5, y + 8)], verd, group=90)
    p.stroke([(x + 2, y + 7), (x + 10, y + 7)], "ink")
    p.stroke([(x + 5.5, y + 8), (x + 5.5, y + 15)], "ink")
    p.px(x + 6, y + 7, "glow")
    p.px(x + 6, y + 9, "glow")


def helm_side(p, x, y):
    if p.big:
        p.patch(x, y, HELM_SIDE, HELM_LEGEND)
        return
    p.poly([(x + 2, y + 15), (x + 2, y + 5), (x + 9, y), (x + 16, y + 4), (x + 18, y + 13), (x + 15, y + 20),
            (x + 12, y + 14), (x + 6, y + 17)], verd, group=200)
    p.px(x + 14, y + 8, "glow")


# --------------------------------------------------------------------------
# Shapes
# --------------------------------------------------------------------------

def tongue(p, a, b, w, mat, group, bend=0.0, **kw):
    """A tongue of water: a lens fat at its root, pointed at the tip."""
    return p.lens(a, b, w, mat, bend=bend, fat=0.3, group=group, **kw)


def trident(p, x, y, phase=0, s=1.0):
    """The hand that is a trident of water, rising from (x, y): a shaft and
    three barbed tines, foam at the points."""
    sh = 0.4 * phase
    p.limb([(x, y), (x, y - 9 * s)], 2.6 * s, 2.2 * s, tine_m, group=150)
    p.limb(bez((x, y - 7 * s), (x - 5 * s, y - 7.5 * s), (x - 5.4 * s, y - 14.6 * s - sh)), 2.2 * s, 1.6 * s,
           tine_m, group=151)
    p.limb(bez((x, y - 7 * s), (x + 5 * s, y - 7.5 * s), (x + 5.4 * s, y - 14.6 * s + sh)), 2.2 * s, 1.6 * s,
           tine_m, group=152, bias=0.06)
    p.limb([(x, y - 8 * s), (x, y - 16.6 * s - sh)], 2.4 * s, 1.6 * s, tine_m, group=153)
    for tx, ty in ((x - 5.4 * s, y - 15.4 * s - sh), (x, y - 17.4 * s - sh), (x + 5.4 * s, y - 15.4 * s + sh)):
        p.drop((tx, ty - 1.4 * s), tx, ty + 0.4 * s, 1.0 * s, foam_m, group=154)


# --------------------------------------------------------------------------
# Battle front: 3/4 view facing left, rising out of its curling wave
# --------------------------------------------------------------------------

HX, HY = 19, 13

WAVE = path([(3, 61.5), (61.5, 61.5), (61.6, 30)], bez3((61.6, 30), (62, 14), (58, 4), (48, 2.4)),
            bez3((48, 2.4), (40, 1.8), (33, 5), (31, 11)), bez3((31, 11), (35, 8.4), (41, 9), (45, 14)),
            bez3((45, 14), (49, 21), (49, 33), (46, 42)), [(40, 50), (24, 53), (10, 55), (4, 57)])


def _front_wave(p, phase):
    # the great wave: a swell along the base rising behind into a curl over the head
    p.poly(WAVE, water, group=10, bias=0.04)
    # the curl's shadowed underside
    p.poly(path(bez3((31, 11), (35, 8.4), (41, 9), (45, 14)), bez3((45, 14), (47, 18), (48, 24), (48, 30)),
                [(44.5, 30)], bez3((44.5, 30), (44.5, 22), (40, 14), (32, 12.5))), water_d, group=11)
    # the foam lip rolling over
    p.limb(bez3((31.4, 10.4), (32, 4), (40, 1.8), (50, 2.6)), 3.0, 2.2, foam_m, group=12)
    for k, (tip, cx, cy, r) in enumerate((((29.6, 14.6), 31.6, 11.4, 1.6), ((33.4, 14.0), 34.6, 10.6, 1.3))):
        p.drop(tip, cx, cy, r, foam_m, group=13 + k)


def _front_body(p, phase):
    ph = phase
    big = p.big
    # ---- near arm (right of frame): water arm sweeping back into the wave
    p.limb([(44, 37), (49.5, 41.5)], 6.6, 6.0, water, group=40)
    p.limb([(49.5, 41.5), (53, 36.5)], 6.0, 5.4, verd, group=41)
    p.limb([(49.0, 42.4), (50.4, 40.6)], 6.8, 6.8, verd_hi, group=42)
    tongue(p, (53, 36.5), (57.5, 30), 5.4, water, group=43, bend=-1.0)
    # ---- far arm (left of frame) raised: water arm, vambrace, and the hand is the trident
    p.limb([(15, 36), (9.5, 29)], 6.6, 6.0, water, group=50)
    p.limb([(9.5, 29), (9.2, 22.4)], 5.8, 5.2, verd, group=51)
    p.limb([(9.6, 29.6), (9.4, 28.2)], 6.8, 6.8, verd_hi, group=52)
    trident(p, 9.2, 21.6, ph)
    # ---- water spilling from the neck
    p.blob(27, 29.5, 6.6, 3.4, water, group=60)
    # ---- the sea churning below the hem
    p.poly([(17, 48), (41, 47), (46, 52), (40, 56), (26, 57), (14, 54)], water, group=61, bias=-0.04)
    # ---- the cuirass: verdigris muscle plate
    p.poly(path(bez3((18.5, 31.5), (22, 29.5), (32, 29.5), (38.5, 31.5)), bez3((38.5, 31.5), (41, 36), (39, 41), (38.5, 47)),
                bez((38.5, 47), (28, 49.5), (18.5, 47)), bez3((18.5, 47), (18.5, 42), (16, 36.5), (18.5, 31.5))),
           verd_hi, group=100, bias=0.08)
    if big:
        p.blob(22.4, 34.6, 4.2, 3.4, verd_hi, group=101, noline=True, bias=-0.04)
        p.blob(30.6, 34.8, 5.6, 3.8, verd_hi, group=102, noline=True, bias=-0.02)
        for k, (cx, cy, rx, ry) in enumerate(((24.2, 40.6, 2.2, 1.8), (29.8, 40.8, 2.8, 1.8), (24.6, 43.6, 2.0, 1.4),
                                              (29.8, 43.8, 2.6, 1.4))):
            p.blob(cx, cy, rx, ry, verd_hi, group=103 + k, noline=True)
        p.shade([(35, 29), (41, 33), (41, 48), (35, 48)], 0.1)
    p.poly(path(bez((18.2, 45.6), (28, 48.2), (37.8, 45.6)), [(38, 48)], bez((38, 48), (28, 50.6), (18, 48))),
           bronze, group=112)
    # ---- pauldrons, coral growing on the near one
    p.blob(44, 37.6, 3.6, 2.2, verd, ang=36, group=130)
    p.blob(42.4, 35.2, 4.6, 2.6, verd, ang=30, group=131)
    p.blob(40.2, 31.8, 5.6, 3.8, verd_hi, ang=20, group=132)
    p.blob(14.8, 34.8, 3.8, 2.2, verd, ang=-32, group=133, bias=0.06)
    p.blob(16.6, 31.8, 4.6, 3.4, verd_hi, ang=-20, group=134, bias=0.04)
    # ---- the crest: a fin of water swept back over the helm
    crest = path(bez3((19.5, 16), (19, 10), (24, 8.4), (30, 8.4)), bez3((30, 8.4), (38, 8.6), (45, 13), (48, 23)),
                 [(45.5, 24)], bez3((45.5, 24), (42, 18), (37, 14.5), (30, 13.5)), [(23, 15.5)])
    p.poly(crest, water, group=140, bias=-0.1)
    helm(p, HX, HY - ph)


def _front(p, phase):
    _front_wave(p, phase)
    _front_body(p, phase)


# --------------------------------------------------------------------------
# Battle back: over the shoulder, helm in profile, the trident raised and the
# wave rising beyond it toward the foe
# --------------------------------------------------------------------------

BWAVE = path([(1.5, 63.5), (1.4, 40)], bez3((1.4, 40), (1, 22), (6, 8), (18, 3.4)), bez3((18, 3.4), (28, 0.6), (40, 3), (44, 9)),
             bez3((44, 9), (38, 7.4), (31, 9), (27, 14)), bez3((27, 14), (22, 21), (21, 32), (24, 42)), [(26, 63.5)])


def _back_wave(p, phase):
    p.poly(BWAVE, water, group=10, bias=0.04)
    p.poly(path(bez3((44, 9), (38, 7.4), (31, 9), (27, 14)), bez3((27, 14), (24, 18), (23, 24), (23, 30)),
                [(27, 30)], bez3((27, 30), (27, 22), (32, 14), (40, 11))), water_d, group=11)
    p.limb(bez3((17, 3.6), (28, 0.8), (38, 2.6), (44.4, 8.6)), 3.2, 2.4, foam_m, group=12)
    for k, (tip, cx, cy, r) in enumerate((((45.6, 13.6), 43.6, 10, 1.6), ((41.4, 13.0), 40.4, 9.6, 1.3))):
        p.drop(tip, cx, cy, r, foam_m, group=13 + k)


def _back_body(p, phase):
    # the sea at the waist
    p.poly([(8, 64), (8, 56), (20, 52), (40, 52), (56, 55), (58, 64)], water, group=20)
    # far arm, hanging into the sea
    p.limb([(13, 50), (10, 60)], 7.4, 6.8, water, group=30)
    # back plate
    p.poly(path(bez3((15, 54), (18, 47), (25, 45), (32, 45)), bez3((32, 45), (39, 45), (46, 47), (48, 54)),
                [(47, 64), (16, 64)]), verd_hi, group=40)
    if p.big:
        p.blob(25, 52, 6.6, 5.4, verd_hi, group=41, noline=True, bias=-0.02)
        p.blob(39, 52, 6.2, 5.2, verd_hi, group=42, noline=True, bias=0.04)
    p.limb([(37, 37), (33, 44)], 8.4, 10.4, water, group=43)      # a neck of sea under the helm
    p.blob(16.5, 49, 5.8, 4.0, verd_hi, ang=-24, group=44)
    p.blob(47, 48.5, 5.4, 3.8, verd, ang=24, group=45)
    # the trident arm raised: water, vambrace, the trident
    p.limb([(50, 46), (55, 37)], 7.0, 6.4, water, group=50)
    p.limb([(55, 37), (56.4, 29)], 6.2, 5.6, verd, group=51)
    p.limb([(55.2, 37.8), (55.4, 36.2)], 7.2, 7.2, verd_hi, group=52)
    trident(p, 56.4, 28.4, phase, s=1.4)
    # the crest and the helm in profile
    p.poly(path(bez3((44.5, 21.5), (45, 13), (39, 10.6), (34, 11)), bez3((34, 11), (27, 11.6), (23, 17), (21, 27)),
                [(24, 28)], bez3((24, 28), (26, 21), (30, 17.5), (36, 18)), [(42, 22)]), water, group=60, bias=-0.1)
    helm_side(p, 29, 20 - phase)


def _back(p, phase):
    _back_wave(p, phase)
    _back_body(p, phase)


# --------------------------------------------------------------------------
# Follower views
# --------------------------------------------------------------------------

def _follow_body(p, bob, back=False):
    p.poly(path(bez3((20, 28 + bob), (26, 25 + bob), (38, 25 + bob), (44, 28 + bob)),
                bez3((44, 28 + bob), (46, 36 + bob), (42, 42 + bob), (42, 45 + bob)),
                bez((42, 45 + bob), (32, 48 + bob), (22, 45 + bob)),
                bez3((22, 45 + bob), (22, 42 + bob), (18, 36 + bob), (20, 28 + bob))), verd_hi, group=60)
    p.rect(21, 42 + bob, 42, 44 + bob, bronze, group=61)
    if back and p.big:
        p.stroke([(32, 29 + bob), (32, 41 + bob)], "v0")
    p.blob(18, 29 + bob, 5, 4, verd_hi, group=62)
    p.blob(46, 29 + bob, 5, 4, verd_hi, group=63)


def _follow_wave(p, phase, back=False):
    sw = phase
    # the swell it rides on, and a wave rising behind one shoulder
    p.poly([(8, 58), (14, 50 + sw), (24, 47), (40, 47), (50, 50 - sw), (56, 58), (32, 60)], water, group=10)
    p.poly(path(bez3((40, 50), (52, 40), (56, 26), (50, 12 - sw)), bez3((50, 12 - sw), (47, 16), (46, 30), (36, 48))),
           water, group=11, bias=0.06)
    p.limb(bez((50, 12.5 - sw), (53, 11), (55, 14)), 2.6, 2.0, foam_m, group=12)
    p.stroke([(14, 52), (24, 49), (40, 49), (50, 52)], "foam")


def _down(p, phase):
    bob = phase
    _follow_wave(p, phase)
    _follow_body(p, bob)
    # trident arm raised on the left of frame, the other arm on the right
    p.limb([(16, 33 + bob), (12, 24 + bob)], 6, 5.4, water, group=64)
    p.limb([(12, 24 + bob), (12, 18 + bob)], 5.4, 5.0, verd, group=65)
    trident(p, 12, 17 + bob, phase, s=0.8)
    p.limb([(48, 33 + bob), (50, 41 + bob)], 6, 5.4, water, group=66)
    # helm face-on with the fin crest
    p.poly([(30, 12 + bob), (32, 3 + bob), (34, 12 + bob)], water, group=70)
    p.poly([(23, 16 + bob), (26, 10 + bob), (32, 8 + bob), (38, 10 + bob), (41, 16 + bob), (41, 25 + bob),
            (35, 28 + bob), (29, 28 + bob), (23, 25 + bob)], verd_hi, group=71)
    p.rect(25, 15 + bob, 38, 17 + bob, Mat(["ink"]), group=72, flat=0, noline=True)
    p.rect(31, 18 + bob, 33, 27 + bob, Mat(["ink"]), group=73, flat=0, noline=True)
    p.pxs([(28, 15 + bob), (32, 15 + bob), (36, 15 + bob)], "glow")
    p.stroke([(28, 16 + bob), (36, 16 + bob)], "glow")
    p.stroke([(32, 17 + bob), (32, 25 + bob)], "foam")


def _up(p, phase):
    bob = phase
    _follow_wave(p, phase, back=True)
    _follow_body(p, bob, back=True)
    p.limb([(16, 33 + bob), (14, 41 + bob)], 6, 5.4, water, group=64)
    p.limb([(48, 33 + bob), (52, 24 + bob)], 6, 5.4, water, group=66)
    p.limb([(52, 24 + bob), (52, 18 + bob)], 5.4, 5.0, verd, group=65)
    trident(p, 52, 17 + bob, phase, s=0.8)
    p.poly([(23, 16 + bob), (26, 10 + bob), (32, 8 + bob), (38, 10 + bob), (41, 16 + bob), (43, 26 + bob),
            (37, 27 + bob), (27, 27 + bob), (21, 26 + bob)], verd_hi, group=71)
    p.limb([(32, 4 + bob), (32, 22 + bob)], 4.0, 2.4, water, group=72)


def _icon(p, phase):
    """Party icon: a compact bust rising from the wave, the trident raised."""
    ox, oy = 17, 18
    up = phase
    p.poly(path(bez3((ox + 20, oy + 28), (ox + 30, oy + 22), (ox + 31, oy + 6), (ox + 24, oy + 1)),
                bez3((ox + 24, oy + 1), (ox + 21, oy + 0.4), (ox + 18, oy + 2), (ox + 17.4, oy + 5)),
                bez3((ox + 17.4, oy + 5), (ox + 21, oy + 3.6), (ox + 25, oy + 8), (ox + 22, oy + 22))),
           water, group=10)
    p.limb(bez((ox + 17.6, oy + 4.6), (ox + 19, oy + 1), (ox + 24, oy + 1.2)), 1.8, 1.4, foam_m, group=11)
    p.poly([(ox + 2, oy + 27.6), (ox + 4, oy + 24), (ox + 26, oy + 24), (ox + 30, oy + 27.6)], water, group=12)
    p.poly([(ox + 8, oy + 20), (ox + 22, oy + 20), (ox + 21, oy + 26), (ox + 9, oy + 26)], verd_hi, group=30)
    p.blob(ox + 7.5, oy + 21, 3.6, 3.0, verd_hi, group=31)
    p.blob(ox + 22.5, oy + 21, 3.6, 3.0, verd_hi, group=32)
    p.limb([(ox + 6, oy + 20), (ox + 4, oy + 14)], 3.4, 3.0, water, group=33)
    trident(p, ox + 4, oy + 13.6 - up, 0, s=0.74)
    p.poly([(ox + 9, oy + 9), (ox + 10, oy + 3), (ox + 16, oy + 2.4), (ox + 22, oy + 6), (ox + 23, oy + 11),
            (ox + 19, oy + 8)], water, group=34)
    helm(p, ox + 6, oy + 6 - up)


def pontanax(p, view, phase):
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
    # icon palette 0 keeps the verdigris green against the wave's blue
    Mon("Pontanax", COLORS, SHINY, pontanax, foot="blank", icon_pal=0),
]
