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
    if view in ("front", "side", "icon"):
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

SPINE = [(61, 23), (61.8, 13), (59, 5), (51.5, 1.2), (41, 1), (32.4, 2.8), (27.4, 5.8), (24.6, 9.6)]
EDGE = [(24.6, 9.6), (28, 8.4), (33.4, 7.6), (41, 7.4), (48, 8.4), (52.8, 11.6), (54.8, 16.6), (55.2, 23)]
# part ids by name, for the hand-finishing scripts
PARTS = {}


def _front(p, ph):
    J = 1.6 if ph else 0.0      # frame 2: the jaw drops wider
    H = -0.6 if ph else 0.0     # and the head lifts a touch

    # ---- far legs, in shade: Doric columns on square feet
    PARTS["ffleg"] = p.poly([(18.6, 40), (27, 40), (26.4, 55), (19, 55)], stone, bias=0.3, group=10)
    _plinth(p, 16.6, 28.4, 54, 59.6, stone_d, claws=0, bias=0.26, group=12)
    PARTS["frleg"] = p.poly([(43, 41), (50.6, 41), (50.2, 55), (43.4, 55)], stone, bias=0.34, group=11)
    _plinth(p, 41.6, 51.6, 54, 59.6, stone_d, claws=0, bias=0.3, group=13)

    # ---- tail, rising behind the haunch into the Harpe's guard
    PARTS["tail"] = p.limb(bez3((53, 32), (57.6, 32), (58.4, 27), (58, 21)), 10, 7, stone, bias=0.04, group=80)

    # ---- body: shoulder hump, barrel and haunch as one mass
    body = [(26, 25), (30, 18), (36, 15), (43, 15.4), (50, 20), (56, 25), (60.5, 31), (60.5, 40), (56, 45),
            (46, 46.5), (38, 46), (30, 43), (25, 34)]
    PARTS["body"] = p.poly(body, stone, group=1)
    p.blob(38, 29, 12, 13.4, stone, group=1)
    p.blob(55, 35, 6.6, 8.4, stone, group=1)
    PARTS["belly"] = p.blob(45, 44.6, 7.6, 2.2, stone_d, ang=-3, bias=-0.1, group=2)
    # ---- dorsal fins: the crest's line carried down the spine, raking back
    fins = [((32, 18), (37.6, 9.8), 7.4), ((38.6, 16.6), (44.6, 10), 7.2), ((45, 19), (50.4, 12.6), 6.4),
            ((50.6, 22.4), (54.8, 16.6), 5.2)]
    PARTS["fins"] = []
    for i, (a, b, w) in enumerate(fins):
        PARTS["fins"].append(p.lens(a, b, w, fin_m, fat=0.28, bend=-1.4, group=30 + i))

    # Dialga's pauldron in slate over the shoulder, and a plate on the haunch
    PARTS["pauldron"] = p.poly([(36.4, 22.6), (44, 18.8), (51, 21.4), (52.4, 29), (48, 36), (41, 36.6),
                                (37, 29.6)], stone, bias=-0.14, group=61)
    PARTS["hplate"] = p.poly([(52, 28.6), (56.6, 27), (60.6, 32.4), (59.4, 39.6), (54, 39.4), (51.4, 34)], stone,
                             bias=-0.08, group=63)

    # ---- near legs: Doric columns, a capital at the shoulder, square feet
    PARTS["nfleg"] = p.poly([(30, 42), (40.6, 42), (40, 54), (30.6, 54)], stone, group=14)
    PARTS["nrleg"] = p.poly([(52.6, 38), (60.6, 38), (60.2, 54), (53, 54)], stone, group=15)
    PARTS["nrcap"] = p.poly([(51.6, 40.4), (61.6, 40.4), (61.2, 43.6), (52, 43.6)], bronze, group=19)
    _plinth(p, 28.4, 42.4, 53.4, 61, stone_d, claws=3, group=16)
    _plinth(p, 51.4, 61.6, 53.4, 61, stone_d, claws=2, group=17)

    # ---- neck and chest plates parting around the hourglass
    p.limb([(37, 26), (30, 27.4)], 16, 15, stone, group=40)
    PARTS["chestl"] = p.poly([(27, 30.4), (32.6, 29.4), (33, 42.6), (29, 43.4), (26.6, 37)], stone, bias=-0.1,
                             group=45)
    PARTS["chestr"] = p.poly([(37.4, 29.2), (43, 30), (44.4, 37), (42.6, 43.4), (37.6, 42.6)], stone, bias=-0.04,
                             group=46)
    PARTS["nfcap"] = p.poly([(28.6, 42.6), (42.4, 42.6), (42, 45.8), (29, 45.8)], bronze, group=18)

    _head(p, J, H)

    # ---- the Harpe: the tail's last plate is a bronze guard; the blade grows from it
    PARTS["blade"] = p.poly(catmull(SPINE, 6) + catmull(EDGE, 6), blade_m, group=81)
    PARTS["guard"] = p.limb([(56, 22.6), (60, 21.6)], 4.2, 4.2, bronze, group=82)

    if p.big:
        # the stopped hourglass between the chest plates
        p.patch(31, 30, [
            ".1111111.",
            "1qqqqqqq1",
            "1pdddddp1",
            "1pSsssSp1",
            ".1sSSSs1.",
            "..1sSs1..",
            "...1S1...",
            "..1dSd1..",
            ".1pd.dp1.",
            "1pdddSdp1",
            "1pddddqp1",
            "1psSsssp1",
            ".1111111.",
        ], {"1": "sl0", "q": "vi2", "p": "vi1", "d": "vd", "s": "br2", "S": "br3"})
    else:
        p.rect(34, 32, 35, 40, glass)


def _head(p, J, H):
    """The Devourer's head, jaw dropped by J and lifted by H."""
    # ---- the head: helm and snout over a maw dropped wide, held low
    def jaw(pts):
        # rotate the lower jaw down about the hinge
        hx, hy = 27, 32
        a = math.radians(J * 2.4)
        ca, sa = math.cos(a), math.sin(a)
        return [(hx + (x - hx) * ca - (y - hy) * sa, hy + (x - hx) * sa + (y - hy) * ca + H) for x, y in pts]

    def hd(pts):
        return [(x, y + H) for x, y in pts]

    PARTS["jaw"] = p.poly(jaw([(28, 31), (30, 37), (25, 42.5), (16, 47.4), (6.4, 51), (2, 49.8), (2.4, 46),
                               (10, 42), (18, 38), (24, 33.6)]), stone, group=41)
    PARTS["void"] = p.poly(hd([(1.4, 25), (10, 27.4), (19, 30), (27, 32.4)]) +
                           jaw([(27, 35.6), (18, 38.4), (10, 42.4), (2.6, 46.4)]), void, group=42)
    PARTS["skull"] = p.poly(hd([(1.4, 21), (3, 17.4), (11, 14.4), (21, 13), (28.5, 15.4), (32, 21.4), (30.4, 30.4),
                                (18, 30), (9, 28), (1.4, 25.4)]), stone, group=43)
    # the crest: the helm's plume grown into a living fin, brow to nape
    PARTS["crest"] = p.poly(hd([(8.4, 14.6), (9.6, 11), (11.6, 8.2), (14.4, 5.8), (17.4, 4.8), (19.4, 6.4),
                                (21.4, 8.8), (25, 11.2), (29, 12.8), (33.6, 15.2), (33, 17.4), (24, 14.4),
                                (14, 15)]), fin_m, group=46)
    # the helm: a Corinthian bronze skull, nose-guard down the snout, flared nape
    PARTS["helm"] = p.poly(hd([(1.6, 19.8), (3, 17.8), (6, 16.2), (8.4, 14.8), (11, 13.2), (15, 12.2), (21, 12),
                               (27, 12.8), (31.4, 15), (34.4, 18.2), (35.8, 22.4), (36.8, 27), (37.2, 30.6),
                               (34.4, 30.2), (32, 31.4), (30.4, 30), (28, 26), (24, 22.6), (18, 21.4), (10, 22),
                               (4, 22), (1.4, 22.6)]), bronze, group=44)
    # the cheek-guard, sweeping down past the eye to a point at the hinge
    PARTS["cheek"] = p.poly(hd([(15.6, 21.2), (22, 21.6), (27, 24.8), (30, 29.6), (29.4, 34.6), (25.6, 30.6),
                                (21.4, 26.6), (17.6, 23.6)]), bronze, group=47)
    for (x, y), l in (((2.2, 24.8), 6.8), ((8.8, 27), 7.4), ((15.4, 29), 5.6), ((21.4, 30.8), 3.6)):
        _fang(p, x, y + H, l, group=50)
    for (x, y), l in (((3.6, 47), 7), ((10.4, 43), 5.8), ((17, 39.4), 3.8)):
        pts = jaw([(x + 1.6, y)])[0]
        _fang(p, pts[0] - 1.6, pts[1], l, up=True, group=51)

    if p.big:
        # the eye, glowing violet in the helm's cut-out
        p.patch(7, 15 + H, [".1111111.", "1qqw1qp11", "1qqq1pp1.", ".1pp1p11.", "..1111..."],
                {"1": "ink", "q": "vi2", "p": "vi1", "w": "wh"})
        p.pxs([(2, 20 + H), (3, 20 + H)], "ink")
    else:
        p.px(10, 17 + H, "vi2")


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


def _down(p, ph):
    """Follower walking toward the camera: the helmed head and its starry maw
    head-on, the Harpe arched up behind, column legs stepping in turn."""
    st = ph
    # the Harpe, rising behind the back and curling forward over the head
    p.poly(catmull([(40, 40), (47, 30), (49, 18), (45, 8), (36, 3), (27, 4), (21, 9)], 6) +
           catmull([(21, 9), (28, 8.4), (35, 8.4), (41, 12), (43, 19), (41, 29), (36, 38)], 6), blade_m, group=81)
    # rear legs, behind
    for sx in (-1, 1):
        X = lambda x: 32 + sx * (x - 32)
        p.rect(min(X(18), X(23)), 50, max(X(18), X(23)), 57 - (st if sx < 0 else 1 - st), stone_d, bias=0.3, group=10)
    # body
    p.blob(32, 44, 17, 11, stone, group=1)
    # front legs, stepping in turn
    for sx in (-1, 1):
        X = lambda x: 32 + sx * (x - 32)
        lift = st if sx < 0 else 1 - st
        p.rect(min(X(20), X(28)), 48, max(X(20), X(28)), 58 - lift, stone, group=14 if sx < 0 else 15)
        p.rect(min(X(19), X(29)), 47, max(X(19), X(29)), 49, bronze, group=18 if sx < 0 else 19)
        p.rect(min(X(19), X(29)), 58 - lift, max(X(19), X(29)), 61 - lift, stone_d, group=16 if sx < 0 else 17)
    # the head: a Corinthian helm seen head-on, its T-shaped opening holding
    # two slanted eyes either side of the nose-guard and the starry maw below
    p.blob(32, 25, 14.6, 11, bronze, group=44)
    p.poly([(28.6, 15), (32, 4.6), (35.4, 15)], fin_m, group=46)
    p.poly([(21, 26), (43, 26), (40, 38), (32, 40.6), (24, 38)], void, group=42)
    p.poly([(30.4, 20), (33.6, 20), (33, 30), (31, 30)], bronze, group=45)
    for x in (23.4, 27, 35.4, 39):
        p.rect(x, 27, x + 1.4, 30, marble, group=50)
    for x in (26.4, 30.4, 34.4):
        p.rect(x, 35, x + 1.4, 37.6, marble, group=51)
    if p.big:
        for ex, rows in ((22, ["1111..", "1ffb11", ".1eef1", "..111."]), (36, ["..1111", "11bff1", "1fee1.", ".111.."])):
            p.patch(ex, 20, rows, {"1": "ink", "f": "vi2", "e": "vi1", "b": "wh"})
        p.patch(30, 44, ["1e1", "1f1", "1e1"], {"1": "ink", "e": "vi1", "f": "vi2"})
    else:
        p.px(24, 22, "vi2")
        p.px(39, 22, "vi2")


def _up(p, ph):
    """Follower walking away: the broad back, its fins down the spine, the tail
    rising into the Harpe arched over toward the head."""
    st = ph
    # the helm and crest beyond the shoulders
    p.blob(32, 20, 11, 7, bronze, group=44)
    p.poly([(29.6, 14), (32, 6), (34.4, 14)], fin_m, group=46)
    # front legs beyond, rear legs near
    for sx in (-1, 1):
        X = lambda x: 32 + sx * (x - 32)
        lift = st if sx < 0 else 1 - st
        p.rect(min(X(20), X(26)), 46, max(X(20), X(26)), 56 - (1 - lift), stone_d, bias=0.3, group=10)
        p.rect(min(X(17), X(27)), 49, max(X(17), X(27)), 59 - lift, stone, group=14 if sx < 0 else 15)
        p.rect(min(X(16), X(28)), 49, max(X(16), X(28)), 51, bronze, group=18 if sx < 0 else 19)
        p.rect(min(X(16), X(28)), 58 - lift, max(X(16), X(28)), 61 - lift, stone_d, group=16 if sx < 0 else 17)
    # the back
    p.blob(32, 38, 17, 14, stone, group=1)
    p.blob(23, 33, 7, 7, stone, bias=-0.12, group=61)
    p.blob(41, 33, 7, 7, stone, bias=-0.12, group=62)
    for i, y in enumerate((24, 30, 36)):
        p.lens((32, y + 5), (32, y - 2), 5.4, fin_m, group=30 + i)
    # the tail rising at the back into the Harpe, arched over toward the head
    p.limb([(32, 50), (32, 44)], 9, 7, stone, group=80)
    p.poly(catmull([(29, 44), (26, 34), (25, 22), (28, 12), (34, 6), (41, 6), (45, 10)], 6) +
           catmull([(45, 10), (40, 10.4), (35, 12), (32, 18), (31.4, 28), (33, 38), (35, 44)], 6), blade_m, group=81)
    p.rect(27, 43, 37, 46, bronze, group=82)


MONS = [
    # icon palette 0 keeps the violet maw and the gold helm apart from the slate
    Mon("Kronolith", COLORS, SHINY, kronolith, foot="bigpaw", icon_pal=0),
]
