"""Kairos line: Kairazor (#147), the Moment. Flying/Psychic legendary.

Round 2 concept A, "Adamant": Lugia's grace on Dialga's architecture, with a
Psychic twist. It hovers on Lugia's long neck with a raised wing-hand whose
fingers are razors, gold along the cutting edge and Aegean at the tips.
Aegean plates on the neck, shoulder and wing carry violet time-lines. It has
a diamond gem on its chest, a pink third eye, and a gold forelock that springs
from the brow and curls forward over a bare crown: seize it as it comes, for
there is nothing behind to hold. Its tail ends in two balance-pan fins on a
gold beam, and a dial of light turns around it.

It shares the violet time-glow ramp (vi0-vi2) with Kronolith, and its diamond
is Kronolith's hourglass turned inside out: the same two triangles. The battle
sprites are hand-finished in art/kairazor_*.txt.
"""
import math

from mon_lib import Mat, Mon, bez3

INK = (32, 24, 24)
VI0, VI1, VI2 = (72, 32, 120), (144, 80, 216), (216, 176, 248)

COLORS = [
    ("ink", INK),
    # marble body, cool and pale like Lugia's
    ("mb0", (128, 136, 176)), ("mb1", (176, 184, 216)), ("mb2", (216, 224, 240)), ("wh", (248, 248, 248)),
    # Aegean plates and finger tips
    ("ae0", (32, 48, 120)), ("ae1", (56, 96, 176)), ("ae2", (104, 160, 224)),
    # gold: the forelock, the razors' edges, the balance beam
    ("go0", (176, 120, 40)), ("go1", (232, 184, 72)), ("go2", (248, 232, 152)),
    # the shared time-glow, and the pink of the third eye
    ("vi0", VI0), ("vi1", VI1), ("vi2", VI2), ("pk", (240, 112, 184)),
]
# the forelock and edges turn silver, and the Aegean plates and tips sun-gold
SHINY = {
    "go0": (120, 128, 144), "go1": (184, 192, 208), "go2": (232, 240, 248),
    "ae0": (152, 96, 24), "ae1": (216, 160, 48), "ae2": (248, 216, 112),
}

marb = Mat(["mb0", "mb1", "mb2", "wh"], line="mb0", cuts=[0.2, 0.46, 0.74])
marb_d = Mat(["mb0", "mb1", "mb2"], line="mb0", cuts=[0.38, 0.7])
aeg = Mat(["ae0", "ae1", "ae2"], line="ae0", cuts=[0.34, 0.68])
gold = Mat(["go0", "go1", "go2"], line="go0", cuts=[0.3, 0.64])
gem = Mat(["vi0", "vi1", "vi2"], line="vi0", cuts=[0.3, 0.62])
pink = Mat(["vi1", "pk", "vi2"], line="vi0", cuts=[0.3, 0.62])

# part ids by name, for the hand-finishing scripts
PARTS = {}


def kairazor(p, view, phase):
    if view in ("front", "side", "icon"):
        _front(p, phase if view == "front" else 0)
    elif view == "back":
        _back(p)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)


# --------------------------------------------------------------------------
# front: hovering, 3/4 facing left, the near wing-hand raised
# --------------------------------------------------------------------------

# the head's offset from the hand-drawn head's frame (the art files draw it)
HX, HY = 1, 11
FINGERS = [((46.6, 14), (50.4, 1.6), 6.0), ((48.6, 14), (58.4, 1.8), 6.6), ((50, 16.6), (62.2, 7.6), 7.0),
           ((50.6, 20.6), (62.4, 17.8), 6.8), ((50, 25), (62, 28.6), 6.4), ((47.6, 29), (58.4, 37.6), 5.8)]
FAR_FINGERS = [((23, 15), (5.4, 4.6), 5.6), ((24.6, 12.6), (12.4, 1.6), 6.0), ((26.6, 11.6), (21.4, 1.4), 5.8),
               ((28.6, 12), (29.6, 1.6), 5.2)]
LAYERS = ("far", "tail", "body", "near", "neck", "head")


def _razor(p, a, b, w, far=False, **kw):
    """A razor finger: marble blade, its trailing edge gold, its tip Aegean."""
    pid = p.lens(a, b, w, marb_d if far else marb, fat=0.3, bend=-1.2, bias=0.3 if far else 0.0, **kw)
    if p.big:
        tip = (a[0] + (b[0] - a[0]) * 0.72, a[1] + (b[1] - a[1]) * 0.72)
        p.lens(tip, b, w * 0.62, aeg, fat=0.2, clip=[pid], noline=True, **kw)
    return pid


def _front(p, ph, layers=LAYERS):
    W = -3 if ph else 0   # frame 2: the wings beat up

    if "far" in layers:
        # ---- far wing, raised up and back behind the head, in shade
        PARTS["fhand"] = p.poly([(29.6, 31), (26, 26), (22.4, 20), (20.4, 15), (21, 11), (24.4, 9), (28.4, 10.6),
                                 (31.4, 15), (33.4, 21), (34.4, 27), (33.6, 31)], marb_d, bias=0.26, group=5)
        PARTS["far"] = []
        for i, (a, b, w) in reversed(list(enumerate(FAR_FINGERS))):
            PARTS["far"].append(_razor(p, a, (b[0], max(1.6, b[1] + W * 0.5)), w, far=True, group=6 + i))

    if "tail" in layers:
        # ---- tail: sweeping down and back to the balance
        PARTS["tail"] = p.limb(bez3((46, 46), (50, 54), (55.4, 53.6), (56, 46.4)), 8, 3.4, marb, group=8)
        PARTS["beam"] = p.limb([(49.6, 45.6), (61.6, 45.6)], 2.2, 2.2, gold, group=9)
        PARTS["pans"] = [p.poly([(46.6, 48), (53.4, 48), (52.4, 51.4), (50, 52.6), (47.6, 51.4)], aeg, group=10),
                         p.poly([(56.6, 48), (62.4, 48), (61.6, 51.4), (59.6, 52.6), (57.4, 51.4)], aeg, group=10)]
        PARTS["pivot"] = p.blob(56, 45.6, 1.7, 1.7, pink, group=11)

    if "body" in layers:
        # ---- body: round and full, Lugia's
        PARTS["body"] = p.blob(38.6, 41.6, 13, 10.4, marb, ang=-12, group=1)
        p.blob(31.4, 39, 7.6, 7.6, marb, group=1)
        # small legs tucked under, gold talons
        PARTS["legs"] = [p.limb([(35, 48.4), (34, 52.6)], 4.4, 3.4, marb, bias=0.2, group=12),
                         p.limb([(42.6, 48.6), (42.4, 53)], 4.6, 3.4, marb, group=13)]
        p.taper([(34.4, 52.4), (31.6, 55)], 2.6, gold, group=14)
        p.taper([(42.4, 52.6), (39.8, 55.2)], 2.6, gold, group=14)
        # chest plate and the diamond gem
        PARTS["chest"] = p.poly([(25.6, 38.4), (30, 33), (35, 34), (37, 40.4), (33, 47), (28, 44.4)], aeg, group=20)
        PARTS["gem"] = p.poly([(28.4, 40), (31.6, 35.4), (34.8, 40), (31.6, 45)], gem, group=21)

    if "near" in layers:
        # ---- near wing: one broad membrane from shoulder to hand, fanned into razors
        PARTS["hand"] = p.poly([(37.4, 35), (39, 27), (42, 19), (45.6, 13), (49, 10), (52, 12), (53.4, 17), (52.6, 24),
                                (50, 30), (45, 36), (41, 38.6)], marb, group=30)
        PARTS["fingers"] = []
        for i, (a, b, w) in reversed(list(enumerate(FINGERS))):
            b = (b[0] + (0.8 * W if i < 2 else 0), max(1.6, b[1] + W * (1 - i * 0.16)))
            PARTS["fingers"].append(_razor(p, a, b, w, group=32 + i))
        PARTS["wplate"] = p.poly([(38, 34), (39.6, 26.6), (42.6, 19), (46, 12.6), (49.4, 8.4), (51.4, 9.8),
                                  (48.6, 14.4), (45.6, 20.4), (43, 27.4), (41.6, 35)], aeg, group=40)
        PARTS["splate"] = p.poly([(38, 31.6), (43, 28.6), (47.6, 31), (48.6, 36.2), (44.6, 39.6), (39.6, 38.2)], aeg,
                                 group=42)

    if "neck" in layers:
        # ---- neck: Lugia's long curve, rising from the chest and bowing to the head
        PARTS["neck"] = p.limb(bez3((34, 38), (31.6, 26), (26, 21.6), (21, 27)), 10.6, 7.6, marb, group=50)
        PARTS["nplates"] = [p.lens(a, b, w, aeg, fat=0.3, group=51) for a, b, w in
                            (((32.6, 31), (36, 25.4), 4.0), ((29.6, 24.6), (33.4, 20), 3.8),
                             ((25.4, 22.6), (27.4, 17.4), 3.4))]

    if "head" in layers:
        _head(p, -1 if ph else 0)


def _head(p, H):
    """A streamlined skull and beak whose crown sweeps back bare, the gold
    forelock springing from the brow and curling forward over the face."""
    def hd(pts):
        return [(x + HX, y + H + HY) for x, y in pts]
    PARTS["skull"] = p.poly(hd([(1.4, 20), (4, 16.4), (8, 13), (13, 9.6), (18, 8), (23, 9.4), (26.6, 12.6),
                                (28, 15), (24, 16.4), (21, 20), (16, 23.4), (12, 25), (4, 25), (1.4, 22.6)]), marb,
                            group=60)
    PARTS["jaw"] = p.poly(hd([(2.4, 22.6), (9, 22.6), (15, 23.2), (12, 25.4), (4.4, 25)]), marb_d, group=61)
    # the forelock: a breaking wave of gold from the brow
    pts_o, pts_i = [], []
    for i in range(41):
        t = i / 40
        th = math.radians(15 - 243 * t)
        r = 5.6 if t < 0.62 else 5.6 - 2.2 * (t - 0.62) / 0.38
        w = 4.6 * (1 - t) ** 0.55 * (0.8 + 0.4 * math.sin(math.pi * min(1, t * 1.6))) + 0.7
        x, y = 9 + HX + r * math.cos(th), 9 + H + HY + r * math.sin(th)
        pts_o.append((x + math.cos(th) * w / 2, y + math.sin(th) * w / 2))
        pts_i.append((x - math.cos(th) * w / 2, y - math.sin(th) * w / 2))
    PARTS["lock"] = p.poly(pts_o + pts_i[::-1], gold, group=62)
    PARTS["third"] = p.poly(hd([(12.4, 11), (14, 9), (15.6, 11), (14, 13.6)]), pink, group=63)
    if p.big:
        p.patch(7 + HX, 14 + H + HY, ["..11111..", ".1111151.", "1edd111..", ".1edd1...", "..111...."],
                {"1": "ink", "5": "wh", "e": "vi2", "d": "vi1"})
    else:
        p.px(9 + HX, 17 + H + HY, "ink")


# --------------------------------------------------------------------------
# back, down, up
# --------------------------------------------------------------------------

BACK_FINGERS = [((16.4, 33.8), (2, 46.4), 7.0), ((16.2, 29.6), (1.6, 34.6), 7.6), ((16.2, 25.4), (1.6, 22), 8.0),
                ((16.4, 20.8), (2.4, 9.4), 8.0), ((19, 18), (9.6, 1.6), 7.8), ((22.4, 18), (19.4, 1.4), 7.4),
                ((25.4, 18.4), (28.4, 2), 6.6)]
BACK_FAR = [((45, 17), (42, 1.6), 5.8), ((47.6, 15), (50, 1.4), 6.0), ((50.4, 15.6), (57.6, 2.4), 5.8),
            ((52.4, 18.6), (61.6, 9), 5.4)]
# where the mirrored hand-drawn head sits in the back view
BHX, BHY = 63, 8


def _back(p, layers=LAYERS):
    """Over the shoulder: the vast wings spread in a V, the head turned right in
    profile so the bare back of its crown shows: nothing behind to hold."""
    if "far" in layers:
        PARTS["bfhand"] = p.poly([(38, 36), (40, 28), (43, 21.6), (46.4, 16.4), (50.4, 13.4), (54, 14.4), (55, 18.6),
                                  (53, 24.6), (49, 30.6), (43, 36)], marb_d, bias=0.26, group=5)
        PARTS["bfar"] = []
        for a, b, w in reversed(BACK_FAR):
            PARTS["bfar"].append(_razor(p, a, b, w, far=True, group=6))
    if "body" in layers:
        PARTS["bbody"] = p.blob(30, 53, 20.6, 17, marb, group=1)
        PARTS["bneck"] = p.limb([(40, 42), (42.6, 34), (44, 28)], 12, 10, marb, group=50)
        PARTS["bplates"] = [p.lens(a, b, w, aeg, fat=0.3, group=51) for a, b, w in
                            (((30, 56), (33, 47), 5.6), ((34, 46.4), (37.6, 39.4), 5.0), ((38.6, 38.6), (41.6, 32), 4.4))]
    if "near" in layers:
        PARTS["bhand"] = p.poly([(30, 44), (25, 41), (20, 37), (16.4, 32), (15.4, 26), (16.4, 20), (18.4, 15.4),
                                 (21.4, 12.6), (25, 13.4), (28, 18), (30.4, 27), (31.4, 37)], marb, group=30)
        PARTS["bfingers"] = []
        for a, b, w in reversed(BACK_FINGERS):
            PARTS["bfingers"].append(_razor(p, a, b, w, group=32))
        PARTS["bwplate"] = p.poly([(30.6, 40), (29.4, 31), (27, 22.6), (23.6, 15), (20.4, 11.4), (18, 11.4),
                                   (20.4, 16), (24, 24), (26.6, 32.6), (27.6, 41)], aeg, group=40)
        PARTS["bsplate"] = p.poly([(22, 44), (28, 40), (34, 42), (34, 48), (28, 50.6), (22.6, 49)], aeg, group=42)
    if "head" in layers:
        # the head, turned right
        p.poly([(60.6, 27), (58, 23), (53, 19.6), (48, 18), (43, 19), (38, 22), (35, 26), (38, 29), (42, 33),
                (47, 36), (55, 37), (61.6, 34)], marb, group=60)
        p.poly([(52, 18), (51, 12.6), (54, 9), (59, 9), (61.6, 13), (61, 18), (58, 16), (55, 15.4)], gold, group=62)
        if p.big:
            p.patch(51, 27, ["11111", "15111", "111dd", ".1dd1"], {"1": "ink", "5": "wh", "d": "vi1"})


def _wings_v(p, beat, far_side=False):
    """Both wings raised in a V, seen head-on or from behind."""
    for sx in (-1, 1):
        X = lambda x: 32 + sx * (x - 32)
        b = beat if sx < 0 else 1 - beat
        p.poly([(X(28), 36), (X(22), 30), (X(16), 22), (X(13), 15), (X(15), 11), (X(19), 12), (X(24), 19),
                (X(29), 28)], marb_d if far_side else marb, group=30 + (sx > 0))
        for (ax, ay), (bx, by), w in (((15, 14), (12, 2 - b), 5.4), ((14, 18), (5, 8 - b), 5.6),
                                      ((15, 23), (4, 21 - b), 5.4), ((18, 27), (8, 32 - b), 5.0)):
            _razor(p, (X(ax), ay), (X(bx), by), w, group=32 + (sx > 0))
        p.poly([(X(28), 34), (X(22.6), 28), (X(17), 20), (X(14.4), 14), (X(16), 13.4), (X(19.6), 19),
                (X(24.6), 26), (X(29.6), 32)], aeg, group=40 + (sx > 0))


def _down(p, ph):
    """Follower toward the camera: the face under its forelock, the third eye
    above two eyes, both wings raised, the dial of light about its waist."""
    _wings_v(p, ph)
    # tail and balance hanging behind and below
    p.limb([(32, 48), (32, 55)], 4, 3, marb, group=8)
    p.limb([(25.6, 55), (38.4, 55)], 2, 2, gold, group=9)
    for cx in (25.6, 38.4):
        p.poly([(cx - 3, 57), (cx + 3, 57), (cx + 2, 59.6), (cx - 2, 59.6)], aeg, group=10)
    # body, chest plate, gem
    p.blob(32, 43, 9.6, 8.6, marb, group=1)
    p.poly([(27, 38), (32, 35), (37, 38), (35.6, 46), (32, 48.6), (28.4, 46)], aeg, group=20)
    p.poly([(29.6, 41), (32, 37.6), (34.4, 41), (32, 45)], gem, group=21)
    # neck and head
    p.limb([(32, 36), (32, 30)], 7, 6, marb, group=50)
    p.blob(32, 25, 8.6, 7.4, marb, group=60)
    p.poly([(29, 29), (35, 29), (33.6, 32.6), (30.4, 32.6)], marb, group=61)
    # the forelock arching up over the brow and curling forward
    p.poly(catmull_pts([(28.4, 19), (25, 12), (28, 6.4), (34, 5), (39, 8.6), (38.4, 14), (35, 15)]) +
           catmull_pts([(35, 15), (35.6, 11), (33, 9), (30, 10.4), (30, 15), (31, 19)]), gold, group=62)
    p.poly([(32, 17.4), (33.4, 19.6), (32, 21.6), (30.6, 19.6)], pink, group=63)
    if p.big:
        for ex, rows in ((25, ["111.", "1511", "1dd1", ".11."]), (35, [".111", "1151", "1dd1", ".11."])):
            p.patch(ex, 22, rows, {"1": "ink", "5": "wh", "d": "vi1"})
    else:
        p.px(28, 24, "ink")
        p.px(35, 24, "ink")


def _up(p, ph):
    """Follower walking away: wings raised in a V, the bare back of the head
    with only the forelock's curl showing over its brow, the balance below."""
    p.limb([(32, 48), (32, 55)], 4, 3, marb, group=8)
    p.limb([(25.6, 55), (38.4, 55)], 2, 2, gold, group=9)
    for cx in (25.6, 38.4):
        p.poly([(cx - 3, 57), (cx + 3, 57), (cx + 2, 59.6), (cx - 2, 59.6)], aeg, group=10)
    p.blob(32, 43, 10, 8.6, marb, group=1)
    _wings_v(p, ph)
    for a, b in (((32, 48), (32, 42)), ((32, 41), (32, 35))):
        p.lens(a, b, 4.6, aeg, group=51)
    p.limb([(32, 36), (32, 30)], 7, 6, marb, group=50)
    # the forelock's curl peeking over the crown, which is bare and polished
    p.poly([(28, 18), (27, 12.6), (30, 9), (35, 9), (37.4, 12.6), (36, 18)], gold, group=62)
    p.blob(32, 24, 8.4, 7.6, marb, group=60)
    if p.big:
        p.patch(28, 18, ["5555", ".55."], {"5": "wh"})


def catmull_pts(pts, n=6):
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


MONS = [
    # icon palette 0 keeps the marble white and the plates blue, as Lugia's icon does
    Mon("Kairazor", COLORS, SHINY, kairazor, foot="bird", icon_pal=0),
]
