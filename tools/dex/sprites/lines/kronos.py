"""Kronos line: Kronolith (#146), the Lord of Time. Ground/Psychic box legendary.

Round 2 concept A, "Adamant": the Devourer as a four-legged behemoth on
Doric-column legs. Its head is a bronze Corinthian helm grown into the skull,
and the maw opens onto a starry void, with fangs like broken marble columns.
One dorsal line runs from the helm's crest along the spine fins and up the
tail into the Harpe, the bronze sickle that arches over its back. The
stopped hourglass glows between its chest plates, and violet time-lines run
from it along the plate seams to the blade's edge.

It shares the violet time-glow ramp (vi0-vi2) with Kairazor, and its
hourglass is Kairazor's diamond turned inside out: the same two triangles.
The battle sprites are hand-finished in art/kronolith_*.txt.
"""
import math

from mon_lib import Mat, Mon, bez3

INK = (32, 24, 24)

# the time-glow ramp, identical in Kairazor's palette
VI0, VI1, VI2 = (72, 32, 120), (144, 80, 216), (216, 176, 248)

COLORS = [
    ("ink", INK),
    # slate hide: cold blue-gray stone plates
    ("sl0", (40, 40, 64)), ("sl1", (72, 72, 104)), ("sl2", (112, 112, 144)), ("sl3", (168, 168, 192)),
    # chased bronze: helm, Harpe, bands, frozen sand
    ("br0", (104, 56, 24)), ("br1", (176, 112, 40)), ("br2", (232, 168, 64)), ("br3", (248, 232, 144)),
    # broken-column marble: fangs and claws; white for stars and the edge
    ("mb", (192, 184, 168)), ("wh", (248, 240, 224)),
    # the starry void in the maw, and the time-glow
    ("vd", (24, 16, 40)), ("vi0", VI0), ("vi1", VI1), ("vi2", VI2),
]
# the bronze turns blackened iron, and its brightest tone, the frozen sand,
# turns marble silver
SHINY = {
    "br0": (32, 32, 40), "br1": (64, 64, 80), "br2": (128, 128, 144), "br3": (224, 224, 232),
}

stone = Mat(["sl0", "sl1", "sl2", "sl3"], line="sl0", cuts=[0.18, 0.44, 0.72])
stone_d = Mat(["sl0", "sl1", "sl2"], line="sl0", cuts=[0.4, 0.72])
fin_m = Mat(["vd", "sl0", "sl1", "sl2"], line="vd", cuts=[0.25, 0.5, 0.78])
bronze = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.16, 0.44, 0.8])
void = Mat(["vd", "vi0"], line="ink", cuts=[0.72])
marble = Mat(["mb", "wh"], line="sl1", cuts=[0.5])
blade_m = Mat(["br1", "br2", "br3"], line="br0", cuts=[0.3, 0.7])
glass = Mat(["vi0", "vi1", "vi2"], line="vi0", cuts=[0.3, 0.62])


def catmull(pts, n=8):
    """A smooth path through pts (Catmull-Rom)."""
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


def _fang(p, x, y, l, w=3.2, up=False, **kw):
    """A broken marble column: a capital at the gum, a shaft, a snapped tip."""
    s = -1 if up else 1
    pts = [(x - 0.5, y), (x + w + 0.5, y), (x + w, y + s * 1.2), (x + w - 0.2, y + s * (l - 0.6)),
           (x + w * 0.6, y + s * (l - 1.6)), (x + w * 0.3, y + s * l), (x + 0.1, y + s * (l - 0.8)), (x + 0.2, y + s * 1.2)]
    return p.poly(pts, marble, **kw)


def _plinth(p, x0, x1, y0, y1, mat, claws=3, **kw):
    """A column's square foot with marble claws along its front."""
    p.poly([(x0 + 0.6, y0), (x1 - 0.6, y0), (x1, y0 + 1.4), (x1, y1), (x0, y1), (x0, y0 + 1.4)], mat, **kw)
    if claws:
        span = (x1 - x0 - 1) / claws
        for i in range(claws):
            cx = x0 + 0.5 + span * i
            p.poly([(cx, y1 - 2.6), (cx + span - 0.8, y1 - 2.6), (cx + span - 1.2, y1), (cx - 0.4, y1)],
                   marble, group=kw.get("group", 0) + 100)


def kronolith(p, view, phase):
    if view == "icon":
        _icon(p, phase)
        return
    if view in ("front", "side"):
        _front(p, phase if view == "front" else 0)
        return
    if view == "back":
        _back(p)
        return
    if view == "down":
        _down(p, phase)
        return
    if view == "up":
        _up(p, phase)
        return


# --------------------------------------------------------------------------
# front: 3/4 facing left, the Harpe arched over its back
# --------------------------------------------------------------------------

# the Harpe follows the arch of the back, from the tail's guard to a hooked
# tip hanging over the crest
SPINE = [(61.6, 33), (62, 22), (59, 11.6), (52.6, 4.4), (43, 1.4), (33, 2.2), (25.6, 6.2), (21, 11.6), (19.6, 16)]
EDGE = [(19.6, 16), (23.4, 12.4), (29, 8.6), (36, 6.8), (43.4, 6.8), (50, 9), (54.6, 14), (56.4, 21.6), (56.4, 33)]
# legs: (elbow or knee, wrist or hock, toe) and their widths; columns that
# taper and bend into clawed feet
LEGS = {
    "ffore": ([(42.6, 40), (46.4, 52.6), (43, 57.6)], 8.0, 5.4),
    "fhind": ([(48.4, 43), (48, 52), (46, 57.4)], 7.6, 5.2),
    "nfore": ([(38, 41), (31.4, 52), (26.4, 58.4)], 9.4, 6.0),
    "nhind": ([(55.4, 40), (57.6, 50.4), (54.4, 58.6)], 9.0, 5.6),
}
# fins along the hump, raking back
FINS = [((27.6, 20.4), (32.4, 9.8), 7.4), ((34.4, 16.6), (40, 8.4), 7.8), ((41.6, 15.8), (47.2, 9.8), 7.4),
        ((48.4, 18.8), (52.8, 13.6), 5.8)]
# part ids by name, for the hand-finishing scripts
PARTS = {}


def _leg(p, key, far=False, group=10):
    (a, b, c), w0, w1 = LEGS[key]
    mat = stone_d if far else stone
    bias = 0.3 if far else 0.0
    PARTS[key] = p.limb([a, b], w0, w1, mat, bias=bias, group=group)
    # the clawed foot, bent forward from the column
    PARTS[key + "_foot"] = p.limb([b, c], w1 + 0.6, w1 + 1.4, mat, bias=bias, group=group + 1)
    if not far and p.big:
        for i in range(3):
            cx = c[0] - 2.4 + i * 2.2
            p.poly([(cx - 1, c[1] + 0.4), (cx + 1.2, c[1] + 0.4), (cx + 0.6, c[1] + 2.4), (cx - 1.4, c[1] + 2)], marble,
                   group=group + 2)


def _front(p, ph):
    J = 2.0 if ph else 0.0      # frame 2: the jaw drops wider
    H = -0.6 if ph else 0.0     # and the head lifts a touch

    # ---- far legs, in shade
    _leg(p, "ffore", far=True, group=10)
    _leg(p, "fhind", far=True, group=13)

    # ---- tail, rising from the low rump into the Harpe's guard
    PARTS["tail"] = p.limb(bez3((54, 36), (59, 37), (60.4, 34), (59.4, 30)), 9, 6.6, stone, bias=0.04, group=80)

    # ---- body: the hump arches high behind the head; the hindquarters sit low
    body = [(22, 33), (23.4, 24), (28.6, 16.4), (35.6, 12.4), (43, 12.2), (49, 15.4), (53.4, 20.6), (57, 27),
            (60.4, 33), (61, 39), (58.4, 44), (52, 46.6), (44, 47), (37, 45.6), (30, 43), (24.6, 39)]
    PARTS["body"] = p.poly(body, stone, group=1)
    p.blob(37, 26, 12.6, 13.4, stone, group=1)
    p.blob(54, 37, 7, 8, stone, group=1)
    PARTS["fins"] = []
    for i, (a, b, w) in enumerate(FINS):
        PARTS["fins"].append(p.lens(a, b, w, fin_m, fat=0.28, bend=-1.4, group=30 + i))
    # Dialga's pauldron in slate over the shoulder, and a plate on the haunch
    PARTS["pauldron"] = p.blob(37.6, 23.4, 7.6, 8.4, stone, ang=-20, bias=-0.14, group=61)
    PARTS["hplate"] = p.blob(53.6, 33, 5.6, 7, stone, ang=10, bias=-0.08, group=63)

    # ---- near legs, braced: the foreleg stepping forward, the hind leg crouched
    _leg(p, "nhind", group=16)
    _leg(p, "nfore", group=19)

    # ---- the chest under the neck, where the hourglass glows
    PARTS["chest"] = p.blob(32.6, 36.6, 6.4, 7.4, stone, bias=-0.06, group=45)

    _head(p, J, H)

    # ---- the Harpe: the tail's last plate is a bronze guard; the blade grows from it
    PARTS["blade"] = p.poly(catmull(SPINE, 6) + catmull(EDGE, 6), blade_m, group=81)
    PARTS["guard"] = p.limb([(56.4, 31.6), (61, 31.6)], 4.4, 4.4, bronze, group=82)

    if p.big:
        # the stopped hourglass between the chest plates
        p.patch(29, 31, [
            "167899871",
            "d1efffe1d",
            "d1e999e1d",
            "dd1e8e1dd",
            "2dd191dd2",
            "22d1f1d22",
            "2dd181dd2",
            "dd1ece1dd",
            "d1ecc9e1d",
            "d1e8998ed",
            "167899871",
            "111111111",
        ], {"1": "ink", "2": "sl0", "6": "br0", "7": "br1", "8": "br2", "9": "br3", "c": "vd", "d": "vi0",
            "e": "vi1", "f": "vi2"})
    else:
        p.rect(32, 33, 34, 40, glass)


def _head(p, J, H):
    """The Devourer's head, held low and thrust forward: a domed Corinthian
    helm sweeping back into the crest, the jaw dropped by J, lifted by H."""
    def jaw(pts):
        hx, hy = 24, 43
        a = math.radians(J * 2.4)
        ca, sa = math.cos(a), math.sin(a)
        return [(hx + (x - hx) * ca - (y - hy) * sa, hy + (x - hx) * sa + (y - hy) * ca + H) for x, y in pts]

    def hd(pts):
        return [(x, y + H) for x, y in pts]

    PARTS["jaw"] = p.poly(jaw([(26, 43), (26, 46), (22, 49.4), (16, 52.6), (9, 55), (3.6, 55.6), (1.6, 53),
                               (2.4, 49), (9, 47), (17, 44.6), (22.6, 43.4)]), stone, group=41)
    PARTS["void"] = p.poly(hd([(1.6, 38), (8, 38.6), (16, 40.6), (24, 43)]) +
                           jaw([(22, 44), (16, 45.6), (9, 47.6), (2.4, 49.4)]), void, group=42)
    PARTS["crest"] = p.poly(hd([(11.6, 21.4), (17, 19.6), (23, 17.6), (28.6, 15.6), (29.6, 22), (27, 27), (20, 22.6),
                                (14, 22.6)]), fin_m, group=46)
    PARTS["helm"] = p.poly(hd([(1.4, 35.6), (1.4, 32.4), (3, 29), (5.6, 26.4), (8.4, 23.6), (12, 22), (18, 21.6),
                               (24, 23), (27.6, 26.4), (30, 31), (30.6, 35), (27, 36), (24, 40), (20, 39.6),
                               (12, 37), (6, 36), (3, 36.4)]), bronze, group=44)
    for (x, y), l in (((2.6, 38), 6), ((8.6, 39), 5), ((14.6, 40.4), 3.6)):
        _fang(p, x, y + H, l, w=2.8, group=50)
    for (x, y), l in (((5.6, 48.6), 4.4), ((11.4, 47), 4), ((17.4, 45), 3)):
        pts = jaw([(x + 1.4, y)])[0]
        _fang(p, pts[0] - 1.4, pts[1], l, w=2.4, up=True, group=51)
    if p.big:
        p.patch(7, 26 + H, ["661111111", "61fbf1e1.", "1effe11..", ".1ee11..."],
                {"1": "ink", "6": "br0", "f": "vi2", "e": "vi1", "b": "wh"})
    else:
        p.px(9, 28 + H, "vi2")


# --------------------------------------------------------------------------
# back: over the shoulder, the head turned right in profile, the Harpe arched
# across the frame from the tail to above the head
# --------------------------------------------------------------------------

BACK_SPINE = [(2.6, 42), (1.8, 30), (4.2, 17), (10, 8), (18, 3), (27, 1.6), (33.4, 3.6), (37, 8.4)]
BACK_EDGE = [(37, 8.4), (32.4, 7.4), (26.4, 7.4), (19.6, 9.4), (14, 14), (10.6, 21), (9.6, 31), (10, 42)]


def _back(p):
    """Over the shoulder at about 1.2x: the head turned right in profile, the
    spine's fins climbing to the nape, the Harpe arched over everything."""
    # the back and shoulders, cropped by the frame
    PARTS["bbody"] = p.poly([(1, 64), (1.4, 46), (8, 36), (18, 28), (28, 22), (36, 20), (40, 26), (42, 40),
                             (40, 52), (36, 64)], stone, group=1)
    # the tail rising at the left into the guard
    PARTS["btail"] = p.limb([(6, 64), (5.4, 52), (6.4, 44)], 10, 8, stone, bias=0.06, group=80)
    # fins along the spine, raking back
    PARTS["bfins"] = []
    for i, (a, b, w) in enumerate((((31, 23), (25, 13.4), 8), ((24, 28), (17, 18.6), 8.4), ((17, 34), (10, 25), 8),
                                   ((11, 40), (6, 32.4), 6.4))):
        PARTS["bfins"].append(p.lens(a, b, w, fin_m, fat=0.28, bend=1.4, group=30 + i))
    # the pauldron, huge and near
    PARTS["bpauldron"] = p.blob(22, 52, 15, 13.6, stone, ang=-20, bias=-0.12, group=61)
    # the head, turned right
    p.poly([(26, 20), (30, 12), (40, 8), (52, 10), (60, 18), (62.4, 24), (61, 30), (52, 32), (40, 36),
            (34, 40), (28, 34)], bronze, group=44)
    p.poly([(36, 36), (48, 40), (60, 44), (61.6, 50), (52, 52), (40, 48), (32, 44)], stone, group=41)
    p.poly([(40, 34), (52, 32), (61, 30), (60.4, 43), (48, 39)], void, group=42)
    PARTS["bblade"] = p.poly(catmull(BACK_SPINE, 6) + catmull(BACK_EDGE, 6), blade_m, group=81)
    PARTS["bguard"] = p.limb([(2.4, 42), (10.6, 42)], 4.4, 4.4, bronze, group=82)
    if p.big:
        p.patch(48, 18, ["11111", "1ffb1", "1eef1", ".111."], {"1": "ink", "f": "vi2", "e": "vi1", "b": "wh"})


def _icon(p, ph):
    """Party icon: the Devourer boiled down for 32 px. A big gold helm over a
    violet maw, the hump, four stubby columns, the Harpe arched over all."""
    J = 1.6 if ph else 0.0
    p.poly(catmull([(60, 40), (61, 24), (55, 10), (44, 4), (32, 5), (24, 11), (21, 18)], 4) +
           catmull([(21, 18), (27, 14), (35, 11), (44, 11), (51, 15.6), (54, 25), (54, 40)], 4), blade_m, group=81)
    for x, far in ((33, True), (50, True)):
        p.rect(x, 46, x + 6, 57, stone_d, bias=0.3, group=10)
    p.blob(41, 36, 17, 13, stone, group=1)
    for (x0, y0), (x1, y1), w in (((30, 18), (33, 9), 8), ((40, 16), (44, 8), 8), ((49, 19), (53, 12), 7)):
        p.lens((x0, y0), (x1, y1), w, fin_m, fat=0.3, group=30)
    for x in (27, 45):
        p.rect(x, 46, x + 8, 58, stone, group=14)
        p.rect(x - 1, 44, x + 9, 46, bronze, group=18)
    # the head: helm dome, the maw dropped open, the lower jaw
    p.poly([(4, 38), (16, 41), (26, 42), (24, 50 + J), (14, 54 + J), (5, 55 + J), (2, 51 + J)], stone, group=41)
    p.poly([(4, 37), (16, 39.6), (25, 42), (14, 47 + J), (4, 50 + J)], void, group=42)
    p.poly([(2, 36), (3, 29), (8, 22), (16, 18.6), (25, 20), (31, 26), (32, 33), (28, 40), (16, 39), (6, 38)],
           bronze, group=44)
    p.poly([(14, 20), (22, 15.6), (30, 15), (32, 22), (25, 21)], fin_m, group=46)
    p.rect(9, 27, 13, 29, glass, group=47)
    p.rect(35, 30, 37, 36, glass, group=48)


def _braced_legs(p, st, y0, far=False):
    """Two column legs braced wide and angled out, stepping in turn."""
    for sx in (-1, 1):
        X = lambda x: 32 + sx * (x - 32)
        lift = (st if sx < 0 else 1 - st) * 2
        top, foot = (X(24), y0), (X(17.4), 58.6 - lift)
        mat = stone_d if far else stone
        p.limb([top, foot], 7.4, 5.4, mat, bias=0.3 if far else 0.0, group=10 + (sx > 0) + (4 if not far else 0))
        if not far:
            p.limb([(X(25.6), y0 - 0.6), (X(22.4), y0 - 0.6)], 4, 4, bronze, group=18 + (sx > 0))
            p.poly([(X(14), 58.4 - lift), (X(21), 58.4 - lift), (X(21.4), 61 - lift), (X(13.6), 61 - lift)], marble,
                   group=20 + (sx > 0))


def _down(p, ph):
    """Follower toward the camera: the helmed head held low and thrust at
    you, the hump rising behind it under the Harpe, forelegs braced wide."""
    st = ph
    # the Harpe, rising from behind the hump and curling forward over it
    p.poly(catmull([(42, 40), (48, 30), (49, 18), (44, 9), (35, 5), (26, 6.6), (20.6, 12)], 6) +
           catmull([(20.6, 12), (27, 10.4), (34, 10.4), (40, 13.4), (42.4, 20), (41.4, 30), (37.4, 39)], 6),
           blade_m, group=81)
    _braced_legs(p, 1 - st, 44, far=True)
    # the hump, its fins up the middle
    p.blob(32, 34, 15, 11, stone, group=1)
    for i, (x, y) in enumerate(((27, 26), (32, 23.4), (37, 26))):
        p.lens((x, y + 5), (x + 1.4, y - 3), 5, fin_m, fat=0.3, group=30 + i)
    _braced_legs(p, st, 45)
    # the head, low and forward: a Corinthian helm head-on, its T-opening
    # holding two slanted eyes either side of the nose-guard, the maw below
    p.blob(32, 49, 11, 5.6, stone, group=41)
    p.blob(32, 47, 8.6, 3.6, void, group=42)
    p.blob(32, 39, 12, 8, bronze, group=44)
    p.poly([(30.4, 34), (33.6, 34), (33, 44), (31, 44)], bronze, group=45)
    for x in (25.6, 29, 35, 38.4):
        p.rect(x, 44.6, x + 1, 46.4, marble, group=50)
    if p.big:
        for ex, rows in ((24, ["1111..", "1ffb11", ".1eef1", "..111."]), (34, ["..1111", "11bff1", "1fee1.", ".111.."])):
            p.patch(ex, 37, rows, {"1": "ink", "f": "vi2", "e": "vi1", "b": "wh"})
    else:
        p.px(26, 39, "vi2")
        p.px(37, 39, "vi2")


def _up(p, ph):
    """Follower walking away: the hump and its fins from behind, the tail
    rising into the Harpe arched forward over the back, hind legs braced."""
    st = ph
    # the helm beyond the hump
    p.blob(32, 18, 9, 6, bronze, group=44)
    p.poly([(29.6, 14), (32, 7), (34.4, 14)], fin_m, group=46)
    _braced_legs(p, 1 - st, 40, far=True)
    p.blob(32, 33, 16, 13, stone, group=1)
    for i, y in enumerate((21, 27, 33)):
        p.lens((31, y + 5), (33.4, y - 3), 5.4, fin_m, fat=0.3, group=30 + i)
    _braced_legs(p, st, 44)
    # the tail rising at the near end, the Harpe arched forward over the back
    p.limb([(32, 49), (32, 43)], 8, 6, stone, group=80)
    p.poly(catmull([(28.6, 44), (25.4, 33), (25, 21), (28.6, 11.4), (35, 6.4), (42, 7), (45.4, 11)], 6) +
           catmull([(45.4, 11), (40.4, 11.4), (35.4, 13), (32, 19), (31.4, 29), (33, 38), (35.4, 44)], 6),
           blade_m, group=81)
    p.rect(27, 42, 37, 45, bronze, group=82)


MONS = [
    # icon palette 0 keeps the violet maw and the gold helm apart from the slate
    Mon("Kronolith", COLORS, SHINY, kronolith, foot="bigpaw", icon_pal=0),
]
