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

from mon_lib import Mat, Mon, bez, bez3, ribbon

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
    if view == "icon":
        _icon(p, phase)
    elif view in ("front", "side"):
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
# the near wing's four sickle-feathers and the far wing's three: (root,
# control, tip, width), curved quadratic spines that sweep back
# the near wing is one mass: the arm and its Aegean plate along the leading
# edge, four broad sickle-feathers fanned from the hand with only their tips
# free, and a broad trailing edge sweeping back toward the tail
FEATHERS = [((44, 18), (41.6, 7), (47, 1.6), 9.0), ((46.6, 17), (50.6, 4), (60.4, 1.6), 10.0),
            ((48, 20), (57.6, 9.6), (62.4, 11.6), 10.0), ((48, 24), (58, 20.4), (62.4, 28), 9.4)]
ARM = [(36.6, 36), (37.6, 29), (39.6, 22.6), (42.4, 16.6), (45.4, 12), (48.6, 10.4), (50.6, 13), (50, 19), (48, 25),
       (45, 31), (42, 36.6), (39, 38)]
ARM_PLATE = [(37.4, 34.6), (38.4, 28.6), (40.4, 22.4), (43, 16.6), (45.8, 12.4), (48, 11), (49, 12.6), (46.6, 16),
             (44, 21.4), (42, 27.4), (40.6, 34.6)]
TRAIL = [(46, 24), (55, 25), (62.4, 28), (60.6, 31), (56.6, 34), (51.6, 36.6), (46.6, 38.6), (42, 39.4), (40, 36)]
FAR_FEATHERS = [((33.6, 16.4), (30.6, 8.4), (33, 2.4), 5.8), ((36, 16), (37.6, 7.4), (42, 3.4), 6.2),
                ((38.4, 18.4), (42.6, 12.4), (46, 10), 5.4)]
LAYERS = ("far", "tail", "body", "near", "neck", "head")


def feather_poly(root, ctrl, tip, w, beat=0.0):
    """Outline of a sickle-feather along a curved spine: broad near the root,
    swelling a little, then tapering to a sharp tip."""
    tip = (tip[0] + beat * 0.6, max(1.6, tip[1] + beat))
    ctrl = (ctrl[0] + beat * 0.3, max(3.6, ctrl[1] + beat * 0.6))
    path = bez(root, ctrl, tip, n=16)
    return ribbon(path, lambda t: w * (0.9 + 0.2 * math.sin(math.pi * min(1, t * 1.6))) * (1 - t ** 2.2) + 0.5)


def _feather(p, root, ctrl, tip, w, far=False, beat=0.0, **kw):
    pts = feather_poly(root, ctrl, tip, w, beat)
    pid = p.poly(pts, marb_d if far else marb, bias=0.3 if far else 0.0, **kw)
    if p.big:
        t0 = bez(root, ctrl, (tip[0] + beat * 0.6, max(1.6, tip[1] + beat)), n=10)[7]
        p.lens(t0, (tip[0] + beat * 0.6, max(1.6, tip[1] + beat)), w * 0.6, aeg, fat=0.2, clip=[pid], noline=True,
               **kw)
    return pid


def _razor(p, a, b, w, far=False, **kw):
    """A straight-spined feather (follower views)."""
    c = ((a[0] + b[0]) / 2 - (b[1] - a[1]) * 0.12, (a[1] + b[1]) / 2 + (b[0] - a[0]) * 0.12)
    return _feather(p, a, c, b, w, far=far, **kw)


def _front(p, ph, layers=LAYERS):
    W = -3 if ph else 0   # frame 2: the wings beat up

    if "far" in layers:
        # ---- far wing: small and in shadow, rising behind the neck
        PARTS["fhand"] = p.poly([(31, 30), (30.4, 22), (31.6, 16), (34.4, 12.6), (38, 12.4), (40.4, 15), (40, 21),
                                 (37.6, 28)], marb_d, bias=0.3, group=5)
        PARTS["far"] = []
        for i, (r, c, t, w) in reversed(list(enumerate(FAR_FEATHERS))):
            PARTS["far"].append(_feather(p, r, c, t, w, far=True, beat=W * 0.5, group=6 + i))

    if "tail" in layers:
        # ---- tail: sweeping down, back and up into a plate, the balance's
        # pivot; the gold beam grows from the plate, its pans hung from its ends
        PARTS["tail"] = p.limb(bez3((47, 47), (51.4, 55.4), (55.4, 53.4), (55, 46)), 8.4, 3.4, marb, group=8)

    if "body" in layers:
        # ---- body: a deep breast flowing back into a long, tapering body
        PARTS["body"] = p.blob(40, 42.6, 14, 9.6, marb, ang=-6, group=1)
        p.blob(30.4, 41.6, 9.4, 9.4, marb, group=1)
        # small legs tucked under, gold talons
        PARTS["legs"] = [p.limb([(35, 49.6), (34, 53)], 4.4, 3.4, marb, bias=0.2, group=12),
                         p.limb([(43, 49.4), (42.6, 53.4)], 4.6, 3.4, marb, group=13)]
        p.taper([(34.4, 52.8), (31.6, 55.4)], 2.6, gold, group=14)
        p.taper([(42.6, 53), (40, 55.6)], 2.6, gold, group=14)
        # chest plate and the diamond gem, low on the deep breast
        PARTS["chest"] = p.poly([(25, 41.6), (30.4, 34.6), (35.8, 41.6), (30.4, 49)], aeg, group=20)
        PARTS["gem"] = p.poly([(27.4, 41.6), (30.4, 37.4), (33.4, 41.6), (30.4, 46.4)], gem, group=21)

    if "tail" in layers:
        # the balance in front: the tail's tip rises into a plate, the pivot,
        # and the gold beam grows out of it with the pans hung from its ends
        PARTS["beam"] = p.limb([(48, 41), (62, 41)], 2.4, 2.4, gold, group=9)
        PARTS["pivot"] = p.poly([(55.4, 36.6), (59, 41), (55.4, 45.6), (51.8, 41)], aeg, group=11)
        PARTS["pans"] = [p.poly([(46, 47), (53, 47), (52.4, 49), (51, 50.6), (48, 50.6), (46.6, 49)], aeg, group=10),
                         p.poly([(57, 47), (62.4, 47), (62.2, 49), (61.2, 50.6), (58.6, 50.6), (57.4, 49)], aeg,
                                group=10)]

    if "near" in layers:
        # ---- near wing: the arm rising from the shoulder into a hand of four
        # sickle-feathers, gold along their cutting edges
        PARTS["fingers"] = []
        for i, (r, c, t, w) in reversed(list(enumerate(FEATHERS))):
            PARTS["fingers"].append(_feather(p, r, c, t, w, beat=W * (1 - i * 0.2), group=32 + i))
        PARTS["trail"] = p.poly(TRAIL, marb, group=31)
        PARTS["hand"] = p.poly(ARM, marb, group=30)
        PARTS["wplate"] = p.poly(ARM_PLATE, aeg, group=40)
        PARTS["splate"] = p.poly([(38.4, 32), (43, 29.6), (47, 31.6), (47.6, 35.6), (44.4, 38.6), (40, 37.6)], aeg,
                                 group=42)

    if "neck" in layers:
        # ---- neck: one smooth S, rising from the chest and bowing to the head
        PARTS["neck"] = p.limb(bez3((34, 39), (32.4, 27), (26.4, 20.4), (20.6, 27)), 9.6, 8.0, marb, group=50)

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

# the back view's wings: the near one vast, four sickle-feathers sweeping up
# and back to the left; the far one small and dark behind the head
BACK_FEATHERS = [((22.4, 18), (24.4, 7.2), (17, 1.6), 8.6), ((19.2, 17.6), (15.4, 4.2), (3.8, 2.6), 9.4),
                 ((18, 21.8), (8.2, 12.6), (2.4, 19.8), 9.4), ((18.8, 27.2), (8.2, 25), (4.2, 36.6), 8.4)]
BACK_FAR = [((45, 17), (44, 9), (46.4, 3), 5.0), ((47.4, 16), (50, 9), (54, 4.4), 5.2),
            ((49, 18.6), (54, 14), (58, 11.6), 4.6)]
# where the mirrored hand-drawn head sits in the back view
BHX, BHY = 63, 8


def _back(p, layers=LAYERS):
    """Over the shoulder: the vast wings spread in a V, the head turned right in
    profile so the bare back of its crown shows: nothing behind to hold."""
    if "far" in layers:
        PARTS["bfhand"] = p.poly([(38, 36), (40, 28), (43, 21.6), (46.4, 16.4), (50.4, 13.4), (54, 14.4), (55, 18.6),
                                  (53, 24.6), (49, 30.6), (43, 36)], marb_d, bias=0.26, group=5)
        PARTS["bfar"] = []
        for r, c, t, w in reversed(BACK_FAR):
            PARTS["bfar"].append(_feather(p, r, c, t, w, far=True, group=6))
    if "body" in layers:
        PARTS["bbody"] = p.blob(30, 53, 20.6, 17, marb, group=1)
        PARTS["bneck"] = p.limb([(40, 42), (42.6, 34), (44, 28)], 12, 10, marb, group=50)
    if "near" in layers:
        PARTS["bhand"] = p.poly([(30, 44), (25, 41), (20, 37), (16.4, 32), (15.4, 26), (16.4, 20), (18.4, 15.4),
                                 (21.4, 12.6), (25, 13.4), (28, 18), (30.4, 27), (31.4, 37)], marb, group=30)
        PARTS["bfingers"] = []
        for r, c, t, w in reversed(BACK_FEATHERS):
            PARTS["bfingers"].append(_feather(p, r, c, t, w, group=32))
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


def _icon(p, ph):
    """Party icon: Kairazor boiled down for 32 px. A big head under its gold
    forelock, one wing of three broad sickle-feathers, the balance below."""
    W = -3 if ph else 0
    p.limb(bez3((44, 46), (50, 56), (55, 54), (55, 45)), 8, 4, marb, group=8)
    p.blob(39, 42, 13, 11, marb, group=1)
    p.poly([(28, 40), (32, 34), (36, 40), (32, 46)], gem, group=21)
    for (r, c, t, w) in (((44, 17), (42, 7), (48, 1.6), 9), ((47, 17), (53, 6), (61.4, 6), 10),
                         ((48, 22), (57, 18), (61, 29), 9)):
        _feather(p, r, c, t, w, beat=W)
    p.poly([(34, 40), (36, 30), (40, 21), (44, 14), (48, 12.6), (51, 17), (50, 25), (46, 32), (41, 38)], marb, group=30)
    p.poly([(35, 38), (37, 30), (40.6, 22), (44.6, 15), (47, 14.4), (44, 21), (41, 29), (38.6, 38)], aeg, group=40)
    p.limb(bez3((35, 39), (33, 28), (28, 24), (23, 28)), 10, 9, marb, group=50)
    # the balance: the tail rises into a plate, the gold beam grows from it
    p.limb([(46.6, 40), (62, 40)], 3.4, 3.4, gold, group=70)
    p.poly([(55, 34.6), (59.4, 40), (55, 45.6), (50.6, 40)], aeg, group=71)
    for cx in (48.6, 60):
        p.limb([(cx, 41), (cx, 45)], 1.6, 1.6, gold, group=72)
        p.poly([(cx - 3.6, 45), (cx + 2.6 if cx > 55 else cx + 3.6, 45), (cx + 2.2, 49.6), (cx - 2.6, 49.6)], aeg,
               group=73)
    # the head, big; the bare crown sweeping back; the mask round a narrow eye
    p.poly([(2, 31), (5, 27), (10, 23.4), (16, 21.4), (22, 21.6), (27.4, 24.4), (29.4, 28), (25, 30), (20, 33.6),
            (14, 35.6), (7, 35.6), (2, 33.6)], marb, group=60)
    p.poly([(8.6, 27), (14, 25.6), (21, 27), (15, 29.6), (10, 29.6)], aeg, group=61)
    pts_o, pts_i = [], []
    for i in range(31):
        t = i / 30
        th = math.radians(25 - 250 * t)
        r = 6.4 if t < 0.62 else 6.4 - 2.4 * (t - 0.62) / 0.38
        w = 6.0 * (1 - t) ** 0.55 + 1.8
        x, y = 10.6 + r * math.cos(th), 17.6 + r * math.sin(th)
        pts_o.append((x + math.cos(th) * w / 2, y + math.sin(th) * w / 2))
        pts_i.append((x - math.cos(th) * w / 2, y - math.sin(th) * w / 2))
    p.poly(pts_o + pts_i[::-1], gold, group=62)
    p.poly([(13.6, 22.6), (15.4, 20.4), (17.2, 22.6), (15.4, 25)], pink, group=63)
    p.rect(11, 27, 14, 28, gem, group=64)


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
    # the forelock springing from the brow and curling forward toward you
    p.lens((32, 19.4), (30, 7.4), 6.4, gold, bend=1.4, fat=0.4, group=62)
    p.blob(28.6, 9.4, 2.6, 2.6, gold, group=62)
    p.poly([(32, 17.4), (33.4, 19.6), (32, 21.6), (30.6, 19.6)], pink, group=63)
    # Lugia's mask round two narrow eyes
    for sx in (-1, 1):
        X = lambda x: 32 + sx * (x - 32)
        p.poly([(X(25), 24), (X(29), 22.6), (X(30.4), 25.4), (X(26), 26.4)], aeg, group=64 + (sx > 0))
    if p.big:
        for ex, rows in ((26, ["111", "1d1"]), (35, ["111", "1d1"])):
            p.patch(ex, 23, rows, {"1": "ink", "d": "vi1"})
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
