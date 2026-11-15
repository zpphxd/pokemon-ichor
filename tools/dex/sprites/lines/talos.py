"""Talos line: Kolossette, Kolossard (Steel). Talos, the bronze giant of
Crete, and his single vein of ichor sealed by a bronze nail."""
from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Kolossette, the votive bronze figurine
# --------------------------------------------------------------------------

KOLOSSETTE_COLORS = [
    ("ink", INK),
    # cast bronze: ink-brown shadow through terracotta to sun-gold, and a
    # pale specular glint
    ("br0", (72, 40, 32)), ("br1", (128, 64, 40)), ("br2", (184, 104, 48)), ("br3", (224, 152, 64)),
    ("br4", (248, 200, 104)), ("spec", (248, 240, 200)),
    # the ichor: a molten-gold line and its white-hot core
    ("vein0", (248, 176, 32)), ("vein1", (248, 240, 152)),
    # the limestone plinth and the pebble it means to throw
    ("lime0", (144, 112, 80)), ("lime1", (192, 160, 112)), ("lime2", (224, 208, 168)), ("lime3", (248, 240, 216)),
    ("white", C.white),
]
KOLOSSETTE_SHINY = {
    # a cypress-green patina, and a marble-white vein
    "br0": (24, 48, 40), "br1": (40, 88, 64), "br2": (64, 128, 88), "br3": (104, 168, 120),
    "br4": (160, 208, 160), "spec": (224, 248, 224),
    "vein0": (200, 200, 192), "vein1": (248, 248, 240),
}

kb = Mat(["br0", "br1", "br2", "br3", "br4"], line="br0", cuts=[0.14, 0.32, 0.54, 0.76])
kb_dark = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.2, 0.46, 0.74])
k_lime = Mat(["lime0", "lime1", "lime2", "lime3"], line="lime0", cuts=[0.2, 0.44, 0.7])


def _plinth(p, x0, y0, w=17, d=4, h=5):
    """The square votive base in three-quarter view: the front face's top-left
    at (x0, y0), w wide, h tall, its top receding d px up and to the right."""
    top = [(x0, y0), (x0 + w, y0), (x0 + w + d, y0 - d + 0.5), (x0 + d, y0 - d + 0.5)]
    side = [(x0 + w, y0), (x0 + w + d, y0 - d + 0.5), (x0 + w + d, y0 + h - d + 0.5), (x0 + w, y0 + h)]
    front = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    p.poly(top, k_lime, flat=3, group=60)
    p.poly(front, k_lime, flat=1, group=61)
    p.poly(side, k_lime, flat=0, group=62)
    if p.big:
        # a cast moulding along the front face's top edge
        p.stroke([(x0 + 1, y0 + 1), (x0 + w - 1, y0 + 1)], "lime2")


kb_icon = Mat(["br1", "br2", "br3", "br4"], line="br1", cuts=[0.3, 0.52, 0.74])


def _kette_eyes(p, x, y, far=True):
    """Kolossette's round eyes glowing ichor-gold, the near one's top-left at
    (x, y); the far one sits 4 px to its left."""
    if p.big:
        legend = {"8": "vein0", "9": "vein1", "e": "white"}
        p.patch(x, y, [".88.", "89e8", "8998", "8998", ".88."], legend)
        if far:
            p.patch(x - 4, y, [".8.", "8e8", "898", ".8."], legend)
    else:
        # at icon size: a 2 px white glint per eye on the shadowed face
        p.px(x + 1.5, y + 1.5, "white")
        p.px(x + 1.5, y + 2.6, "white")
        if far:
            p.px(x - 3, y + 1.5, "white")


def _kette_helmet(p, cx, cy, B, flip=False, **kw):
    """The big helmet: a fluted fan crest, the dome, a neck guard; the face
    plate is drawn by the caller. (cx, cy) is the dome's center."""
    sx = -1 if flip else 1
    X = lambda x: cx + sx * (x - 30.2)
    Y = lambda y: cy + (y - 32.6)
    outer = bez3((X(22.2), Y(29.0)), (X(21.0), Y(18.4)), (X(38.6), Y(16.0)), (X(39.8), Y(30.6)), n=20)
    inner = bez3((X(37.4), Y(31.0)), (X(36.6), Y(25.0)), (X(28.0), Y(25.0)), (X(24.6), Y(29.0)), n=20)
    p.poly([(X(34), Y(31)), (X(39.2), Y(32.4)), (X(39.6), Y(37.6)), (X(37.0), Y(40.4)), (X(33.0), Y(40.0))],
           B, bias=0.06, group=6, **kw.get("far", {}))
    p.poly(outer + inner, B, group=7, **kw.get("lit", kw.get("near", {})))
    return p.blob(cx, cy, 8.8, 8.2, B, bias=-0.1, group=8, **kw.get("near", {}))


def kolossette(p, view, phase):
    if view in ("front", "side", "icon"):
        # The battle front is hand-finished (art/kolossette_front*); this draft
        # gives the icon and the side follower the same figure.
        icon = view == "icon"
        B = kb_icon if icon else kb
        NEAR = {"flat": 2} if icon else {}
        FAR = {"flat": 1} if icon else {}
        LIT = {"flat": 3} if icon else {}
        hop = 1 if (view == "side" and phase == 1) else 0
        y = -hop
        _plinth(p, 19.5, 56.5 + y, w=18, d=5, h=5)
        # far arm cocked back with the pebble
        p.limb([(37.5, 42.5 + y), (42, 38.5 + y)], 4.4, 4.0, B, bias=0.14, group=20, **FAR)
        p.limb([(42, 38.5 + y), (43.6, 32.6 + y)], 4.0, 3.8, B, bias=0.06, group=20, **FAR)
        p.blob(44.4, 29.4 + y, 3.4, 3.1, k_lime, group=21)
        # far leg, body, belt, near leg
        p.limb([(33.6, 49 + y), (34.2, 54.6 + y)], 4.6, 4.2, B, bias=0.24, group=10, **FAR)
        p.blob(31.2, 45.4 + y, 6.8, 5.8, B, bias=-0.2, group=1, **NEAR)
        p.limb([(25.8, 48.6 + y), (36.4, 48.6 + y)], 2.6, 2.6, kb_dark if not icon else B, group=2, **FAR)
        p.limb([(28.2, 50 + y), (27.2, 54.4 + y)], 5.0, 4.6, B, group=12, **NEAR)
        p.poly([(22.6, 53.8 + y), (29.6, 53.6 + y), (30.4, 55.8 + y), (22.2, 55.8 + y)], B, group=13, **NEAR)
        # the big helmeted head and its face plate
        hd = _kette_helmet(p, 30.2, 32.6 + y, B, far=FAR, near=NEAR, lit=LIT)
        p.blob(29.6, 37.4 + y, 5.8, 4.4, B, bias=-0.1, group=8, **NEAR)        # the cheek-guards
        # the dark visor the eyes glow in, and the slit below it
        p.poly([(23.6, 32.4 + y), (32.6, 32.4 + y), (33.4, 35.0 + y), (32.4, 37.6 + y), (29.2, 37.8 + y),
                (28.6, 40.4 + y), (27.4, 40.4 + y), (27.0, 37.8 + y), (24.2, 37.6 + y), (23.2, 35.0 + y)],
               kb_dark if not icon else B, bias=0.5, group=9, **({"flat": 0} if icon else {}))
        # near arm, stiff at the side
        p.limb([(25.4, 43.4 + y), (24.4, 48.2 + y)], 3.8, 3.4, B, group=22, **LIT)
        p.blob(24.2, 49.0 + y, 2.2, 2.0, B, group=22, **LIT)
        if p.big:
            _kette_eyes(p, 28, 33 + y)
            p.stroke([(30, 42 + y), (29, 46 + y), (28, 50 + y), (27, 54 + y)], "vein1")
        else:
            _kette_eyes(p, 28, 33 + y)
            p.stroke([(30, 42 + y), (28, 50 + y)], "vein1")
        return

    if view == "back":
        # (the hand-finished art replaces this) the big helmet in right
        # profile, the pebble cocked over the left shoulder
        p.blob(30.5, 62.5, 17.5, 14.5, kb, group=1)
        p.limb([(20, 52), (12.6, 43.6), (13.2, 34.2)], 6.0, 5.2, kb, group=20)
        p.blob(13.6, 26.4, 4.4, 3.9, k_lime, group=21)
        _kette_helmet(p, 36.4, 38.2, kb, flip=True)
        p.patch(43, 37, [".88.", "8e98", "8998", ".88."], {"8": "vein0", "9": "vein1", "e": "white"})
        return

    if view in ("down", "up"):
        # follower: the statuette hopping along on its plinth
        hop = phase
        _plinth(p, 21.5, 58.5 - hop, w=17, d=4, h=4)
        y = -hop
        p.limb([(28.5, 49 + y), (28.5, 56 + y)], 4.6, 4.2, kb, group=12)
        p.limb([(35.5, 49 + y), (35.5, 56 + y)], 4.6, 4.2, kb, group=13)
        p.blob(32, 45.4 + y, 7.0, 5.8, kb, bias=-0.14, group=1)
        arm_r = (40.5, 33 + y) if view == "down" else (23.5, 33 + y)
        hang = (24.5, 48 + y) if view == "down" else (39.5, 48 + y)
        p.limb([(25.5 if view == "down" else 38.5, 42 + y), hang], 3.8, 3.4, kb, group=22)
        p.limb([(38.5 if view == "down" else 25.5, 42 + y), arm_r], 3.8, 3.4, kb, group=23)
        p.circle(arm_r[0], arm_r[1] - 3, 3.0, k_lime, group=21)
        p.limb([(32, 23.4 + y), (32, 28 + y)] if view == "down" else [(32, 23.4 + y), (32, 40 + y)],
               4.4, 3.4, kb, group=7)
        hd = p.blob(32, 33 + y, 9.4, 8.6, kb, bias=-0.1, group=8)
        if view == "down":
            p.blob(32, 36 + y, 6.6, 4.8, kb, clip=[hd], bias=0.16, group=9)
            p.stroke([(25, 30 + y), (39, 30 + y)], "br4")
            if p.big:
                legend = {"8": "vein0", "9": "vein1", "e": "white"}
                p.patch(26, 33 + y, [".88.", "89e8", "8998", ".88."], legend)
                p.patch(34, 33 + y, [".88.", "8e98", "8998", ".88."], legend)
            else:
                p.px(27.5, 34.5 + y, "vein1")
                p.px(35.5, 34.5 + y, "vein1")
            p.stroke([(30.5, 42 + y), (30, 48 + y), (28.5, 56 + y)], "vein1")
        else:
            p.stroke([(32, 42 + y), (32, 48 + y), (35.5, 56 + y)], "vein1")
        return


# --------------------------------------------------------------------------
# Kolossard, the bronze giant
# --------------------------------------------------------------------------

KOLOSSARD_COLORS = [
    ("ink", INK),
    ("br0", (72, 32, 24)), ("br1", (128, 64, 32)), ("br2", (184, 104, 40)), ("br3", (224, 152, 56)),
    ("br4", (248, 200, 96)), ("spec", (248, 240, 200)),
    # the ichor vein: deep gold glow, molten gold, white-hot core
    ("vein0", (224, 120, 24)), ("vein1", (248, 192, 40)), ("vein2", (248, 248, 176)),
    ("lime0", (120, 96, 72)), ("lime1", (168, 144, 104)), ("lime2", (208, 192, 152)), ("lime3", (240, 232, 200)),
]
KOLOSSARD_SHINY = {
    "br0": (16, 40, 32), "br1": (32, 80, 56), "br2": (56, 120, 80), "br3": (96, 160, 112),
    "br4": (152, 200, 152), "spec": (224, 248, 224),
    "vein0": (152, 160, 160), "vein1": (216, 216, 208), "vein2": (248, 248, 240),
}

gb = Mat(["br0", "br1", "br2", "br3", "br4"], line="br0", cuts=[0.12, 0.3, 0.52, 0.74])
gb_dark = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.22, 0.48, 0.74])
g_lime = Mat(["lime0", "lime1", "lime2", "lime3"], line="lime0", cuts=[0.18, 0.42, 0.68])
gb_icon = Mat(["br1", "br2", "br3", "br4"], line="br1", cuts=[0.3, 0.52, 0.74])


def _boulder(p, cx, cy, r, **kw):
    """A rough limestone boulder: a lumpy round outline."""
    import math
    lumps = [1.0, 0.94, 1.02, 0.97, 0.9, 1.0, 1.04, 0.95, 0.99, 0.92, 1.03, 0.96]
    pts = []
    n = 36
    for i in range(n):
        t = 2 * math.pi * i / n
        k = lumps[int(i / n * len(lumps))]
        pts.append((cx + r * k * math.cos(t), cy + r * k * 0.94 * math.sin(t)))
    return p.poly(pts, g_lime, **kw)


def kolossard(p, view, phase):
    if view in ("front", "side", "icon"):
        # The battle front is hand-finished (art/kolossard_front*); this draft
        # gives the icon and the side follower the same design: mid-stride,
        # a boulder cocked over the far shoulder, a fluted crest, the vein
        # running down to the nail at the near ankle.
        R = 2 if (phase == 1 and view == "front") else 0
        stride = view == "side" and phase == 1
        icon = view == "icon"
        B = gb_icon if icon else gb   # the icon keeps to the warm tones
        NEAR = {"flat": 2} if icon else {}   # flat tones read best at 32 px
        FAR = {"flat": 1} if icon else {}
        LIT = {"flat": 3} if icon else {}
        _boulder(p, 50, 12.6 - R, 9.4, group=40)
        # far arm under the boulder
        p.blob(44.5, 25.5, 5.4, 5.2, B, bias=0.12, group=20, **FAR)
        p.limb([(46, 25.5), (55, 27.5 - R / 2)], 7.2, 6.6, B, bias=0.1, group=20, **FAR)
        p.limb([(55, 27.5 - R / 2), (55.5, 20 - R)], 6.6, 6.2, B, bias=0.04, group=24, **FAR)
        p.blob(54.2, 18.4 - R, 4.6, 3.4, B, ang=-10, group=25, **FAR)
        # far leg, pushing off behind
        far = [(41, 45), (47.5, 51), (50.5, 57.2), (52, 59.6)]
        if stride:
            far = [(41, 45), (41.5, 51), (40, 57.2), (38, 59.6)]
        p.limb(far[:2], 9.4, 7.6, B, bias=0.2, group=10, **FAR)
        p.limb(far[1:3], 7.0, 5.8, B, bias=0.22, group=11, **FAR)
        p.blob(far[3][0], far[3][1], 4.6, 2.0, B, bias=0.24, group=11, **FAR)
        # torso
        p.blob(38.5, 45.5, 7.6, 4.4, B, group=2, **FAR)
        p.blob(37.2, 38.6, 8.0, 5.8, B, bias=-0.1, group=3, **NEAR)
        chest = p.blob(34.5, 29.6, 11.8, 9.2, B, ang=-12, bias=-0.12, group=1, **NEAR)
        p.blob(30.2, 29.8, 6.6, 5.2, B, ang=-14, clip=[chest], bias=-0.16, group=30, **LIT)
        p.limb([(31, 42.6), (45.5, 42.2)], 3.8, 3.8, gb_dark if not icon else B, group=4, **FAR)
        p.limb([(29.5, 20), (32, 25)], 7.6, 8.2, B, group=5, **NEAR)
        # near leg, planted forward, the nail at its ankle
        near = [(33.5, 45), (25.8, 50.6), (23.4, 56.6), (20.5, 59.4)]
        if stride:
            near = [(33.5, 45), (33, 51), (33.4, 56.6), (30, 59.4)]
        p.limb(near[:2], 10.6, 8.6, B, bias=-0.08, group=12, **NEAR)
        p.limb(near[1:3], 8.6, 8.0, B, group=13, **NEAR)
        p.blob(near[3][0], near[3][1], 6.6, 2.2, B, group=14, **NEAR)
        # the helm: a fluted crest fan on a round domed Corinthian helm whose
        # cheek-guards close over the face, a dark visor slot in front
        crest = bez3((20.4, 9.6), (19.4, -1.4), (40.5, -3.6), (42.0, 17.4), n=24)
        inner = bez3((37.6, 17.0), (37.8, 8.4), (29.0, 8.6), (23.6, 10.4), n=24)
        p.poly(crest + inner, B, group=7, **LIT)
        p.blob(32.8, 20.0, 4.4, 4.2, B, ang=20, bias=0.12, group=5, **FAR)
        p.blob(26.4, 14.8, 8.6, 7.4, B, ang=-28, bias=-0.1, group=6, **NEAR)
        p.blob(25.0, 19.6, 5.6, 5.0, B, bias=-0.1, group=6, **NEAR)
        p.poly([(20.4, 14.4), (30.6, 14.0), (30.4, 17.4), (26.2, 17.6), (25.8, 21.6), (23.6, 21.6), (23.2, 17.6), (20.6, 17.6)],
               gb_dark if not icon else B, bias=0.5, group=8, **({"flat": 0} if icon else {}))
        # near arm swung forward, a great fist
        p.blob(23.2, 27.2, 6.4, 6.0, B, bias=-0.08, group=21, **LIT)
        p.limb([(21.5, 29.5), (14.8, 35.2)], 7.2, 6.6, B, group=21, **NEAR)
        p.limb([(14.6, 35.4), (11.6, 41)], 6.8, 6.4, B, group=22, **NEAR)
        p.blob(10.6, 44.2, 5.0, 4.6, B, group=23, **NEAR)
        if p.big:
            p.patch(20, 14, ["1111111111", "19a12219aa91", "1891221a9a81"][:1] + ["9a12219aa9", "891221a9a8"],
                    {"1": "ink", "2": "br0", "8": "vein0", "a": "vein2", "9": "vein1"})
            p.stroke([(29, 21), (31, 27), (32, 31), (33, 38), (33, 43), (31, 46), (27, 50), (24, 54)], "vein2")
            p.patch(21, 54, [".111.", "16751", "15641", ".111."], {"1": "ink", "4": "br2", "5": "br3", "6": "br4", "7": "spec"})
        else:
            p.px(21.5, 15.5, "spec")
            p.px(27.5, 15.5, "spec")
            p.stroke([(30, 23), (32, 32), (33, 42), (28, 49), (24, 55)], "vein1")
        return

    if view == "back":
        # over the shoulder at 1.2x: the broad back with the vein down the
        # spine, the boulder raised over the left shoulder, the helmet in
        # right profile
        _boulder(p, 14, 13, 11, group=40)
        p.limb([(18, 46), (11, 36), (12, 25)], 11, 9, gb, bias=0.1, group=20)
        p.blob(32, 64, 30, 20, gb, group=1)
        p.blob(20, 44, 10, 9, gb, group=2)
        p.blob(46, 44, 10, 9, gb, group=3)
        p.limb([(37, 44), (40, 34)], 10, 10, gb, group=5)
        hd = p.blob(41, 26, 10, 9.6, gb, group=6)
        p.poly([(46, 22), (51, 24), (51.5, 31), (47, 35), (42, 33)], gb, group=6)
        p.limb(bez((33, 20), (38, 10), (50, 16)), 6.4, 5, gb, group=7)
        p.limb(bez((33, 20), (29, 24), (30, 32)), 5, 3, gb, group=7)
        p.blob(47.5, 28, 4, 4.6, gb_dark, clip=[hd], bias=0.5, group=8)
        if p.big:
            p.patch(47, 26, ["111", "1ab", ".11"], {"1": "ink", "a": "vein2", "b": "vein1"})
            p.stroke([(36, 38), (33, 46), (32, 54), (32, 63)], "vein1")
        return

    if view in ("down", "up"):
        step = phase
        p.limb([(27, 44), (26, 51), (26, 59 - 2 * step)], 7.0, 6.0, gb, bias=-0.16, group=12)
        p.limb([(37, 44), (38, 51), (38, 59 - 2 * (1 - step))], 7.0, 6.0, gb, bias=-0.16, group=13)
        p.blob(32, 43, 8, 4.4, gb, bias=-0.16, group=2)
        p.blob(32, 32, 11.4, 9.4, gb, bias=-0.16, group=1)
        p.limb([(31, 41.5), (33, 41.5)], 13, 3.4, gb_dark, bias=-0.1, group=4)
        if view == "down":
            p.limb([(21, 28), (17, 36), (16.5, 44)], 6.6, 6, gb, bias=-0.16, group=21)
            p.blob(16.5, 46, 4, 3.6, gb, bias=-0.16, group=21)
            p.limb([(43, 28), (47, 22), (47, 14)], 6.6, 6, gb, bias=-0.16, group=22)
            _boulder(p, 47, 9, 6, group=40)
        else:
            p.limb([(43, 28), (47, 36), (47.5, 44)], 6.6, 6, gb, bias=-0.16, group=21)
            p.blob(47.5, 46, 4, 3.6, gb, bias=-0.16, group=21)
            p.limb([(21, 28), (17, 22), (17, 14)], 6.6, 6, gb, bias=-0.16, group=22)
            _boulder(p, 17, 9, 6, group=40)
        hd = p.blob(32, 18, 7.4, 7.2, gb, bias=-0.16, group=6)
        if view == "down":
            p.limb(bez((32, 12), (32, 6), (32, 8)), 4.4, 3.6, gb, bias=-0.16, group=7)
            p.blob(32, 20.5, 5, 4.4, gb_dark, clip=[hd], bias=0.2, group=8)
            p.patch(28, 19, ["11.11", "ab.ab"], {"1": "ink", "a": "vein2", "b": "vein1"},
                    small=(29, 19, ["a.a"]))
            p.stroke([(30, 26), (31, 34), (28, 44), (26, 57)], "vein1")
        else:
            p.limb([(32, 8), (32, 26)], 4.4, 3.4, gb, bias=-0.16, group=7)
            p.stroke([(32, 27), (32, 40), (27, 46), (26, 57)], "vein1")
        return


# Kolossette walks on its votive plinth, so it leaves the plinth's square
KOLOSSETTE_FOOT = [
    "................",
    "................",
    "................",
    "...##########...",
    "...##########...",
    "...##......##...",
    "...##......##...",
    "...##......##...",
    "...##......##...",
    "...##......##...",
    "...##......##...",
    "...##########...",
    "...##########...",
    "................",
    "................",
    "................",
]
# Kolossard: a giant's broad bare sole, five toes
KOLOSSARD_FOOT = [
    "................",
    "....#.##.##.#...",
    "...##.##.##.##..",
    "................",
    "....#########...",
    "...##########...",
    "...##########...",
    "...#########....",
    "....########....",
    "....#######.....",
    "....#######.....",
    "....########....",
    "....########....",
    ".....######.....",
    "................",
    "................",
]

MONS = [
    Mon("Kolossette", KOLOSSETTE_COLORS, KOLOSSETTE_SHINY, kolossette, foot=KOLOSSETTE_FOOT),
    Mon("Kolossard", KOLOSSARD_COLORS, KOLOSSARD_SHINY, kolossard, foot=KOLOSSARD_FOOT),
]
