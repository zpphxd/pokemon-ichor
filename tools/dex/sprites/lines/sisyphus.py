"""Sisyphus line: Bouldyphus (#131, Rock/Ghost), the king who cheated Death.

Concept A, "The Burden". The boulder has grown into its back. Its
shadow-flesh swells up round the stone's base and runs up into its lower
curve, its spine ridge carries on up over the stone as a row of stone spurs,
and the stone's meander cracks run down through the flesh into its stone
forearms, so ghost and boulder light up together. It hauls itself uphill on
two stone fists, shoulders straining under the weight, its legs smoke
streaming back down the slope. One wide gold eye, one screwed shut, and a
grin that is a jagged split glowing violet: it still thinks it got the better
deal.
"""
from mon_lib import Mat, Mon, bez, bez3

COLORS = [
    ("ink", (24, 16, 32)),
    # granite: four tones, a cold violet-gray
    ("s0", (56, 48, 72)), ("s1", (96, 88, 112)), ("s2", (144, 136, 152)), ("s3", (192, 184, 192)),
    # shadow-flesh
    ("k0", (32, 24, 56)), ("k1", (64, 48, 104)), ("k2", (104, 80, 152)), ("k3", (152, 128, 200)),
    # the meander's ghost-light; its core doubles as the stone's glint
    ("v0", (120, 56, 208)), ("v1", (184, 112, 248)), ("v2", (240, 216, 248)),
    # the one open eye: the life it stole back
    ("go0", (200, 136, 32)), ("go1", (248, 216, 88)),
    # lichen: the stone has been on its back a long time
    ("li", (136, 152, 104)),
]
# The boulder turns terracotta and the ghost pales to marble white.
SHINY = {
    "s0": (104, 40, 32), "s1": (152, 72, 40), "s2": (200, 112, 64), "s3": (232, 160, 112),
    "k0": (96, 88, 112), "k1": (152, 144, 160), "k2": (200, 192, 200), "k3": (240, 240, 232),
    "li": (120, 144, 96),
}

stone = Mat(["s0", "s1", "s2", "s3"], line="s0", cuts=[0.2, 0.44, 0.7])
stone_d = Mat(["s0", "s1", "s2"], line="s0", cuts=[0.4, 0.72])
flesh = Mat(["k0", "k1", "k2", "k3"], line="k0", cuts=[0.24, 0.5, 0.78])
smoke = Mat(["k0", "k1", "k2"], line="k0", cuts=[0.4, 0.7])
glow = Mat(["v0", "v1"], line="v0", cuts=[0.5])


def _spline(pts, n=8):
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


def _closed(pts, n=8):
    """A smooth closed outline through pts."""
    P = list(pts) + list(pts[:3])
    out = _spline(P, n)
    return out[n:n + n * len(pts)]


def _move(pts, dx=0.0, dy=0.0):
    return [(x + dx, y + dy) for x, y in pts]


# --------------------------------------------------------------------------
# Battle front: 3/4 view facing left, hauling itself uphill
# --------------------------------------------------------------------------

# the boulder: a craggy granite mass, not a ball. A flattened top ledge, a
# chipped facet at the back, and an overhang leaning forward with the climb.
BC = (40.2, 22.0)
BOULDER = [(28.6, 8.4), (33.0, 7.0), (41.0, 6.8), (47.4, 7.2), (51.6, 8.6), (53.2, 10.8), (56.6, 12.6),
           (58.4, 17.0), (59.0, 22.0), (57.0, 24.0), (58.0, 28.4), (55.4, 32.8), (50.6, 37.0), (44.4, 39.6),
           (36.0, 39.8), (29.4, 37.4), (25.6, 33.0), (23.6, 27.4), (21.2, 22.6), (19.8, 18.0), (21.0, 13.6),
           (24.4, 10.0)]
# the spine ridge: vertebrae of the same stone, running up out of the nape,
# over the arch and down the back, biggest at the front of the arch and
# tapering both ways; drawn back to front so each overlaps the next.
# (base, tip, width)
RIDGE = [((56.8, 13.4), (60.0, 11.6), 3.4), ((53.0, 9.8), (56.0, 6.8), 4.6), ((47.6, 7.8), (50.0, 3.6), 5.8),
         ((41.4, 7.2), (42.8, 2.8), 6.6), ((34.6, 7.6), (33.8, 2.2), 7.4), ((28.2, 9.6), (24.2, 4.0), 7.8),
         ((22.6, 13.8), (17.4, 10.6), 6.4)]


def _front(p, phase):
    h = phase  # frame 2 heaves the stone up a step
    big = p.big
    ox0 = p.ox
    # the body sits 2 px back from the near fist, so the reach strains
    p.ox = ox0 + 2 * p.s

    # ---- smoke legs: thighs bent and pushing, dissolving into smoke that
    # streams back down the slope
    p.limb(_spline([(50, 38), (55.0, 44.6), (57.6, 50.0)]), 8.4, 5.4, smoke, group=2, bias=0.24)
    p.lens((55.4, 46.4), (59.6, 55.0 + h), 4.6, smoke, bend=-1.0, fat=0.3, group=2, bias=0.26)
    p.limb(_spline([(43, 41), (47.4, 48.6), (51.4, 52.6)]), 11.4, 7.4, smoke, group=3, bias=0.06)
    for k, (a, b, w, bend) in enumerate((((48.6, 51.4), (59.4, 59.6 + h), 6.4, -1.8),
                                         ((51.6, 50.0), (59.6, 53.0 + h), 4.4, -0.8),
                                         ((46.4, 54.2), (53.0, 61.0), 4.6, 1.2))):
        p.lens(a, b, w, smoke, bend=bend, fat=0.28, group=4 + k % 2, bias=0.06 * (k % 2))

    # ---- far arm, braced under the body: flesh shoulder, stone forearm, fist
    p.limb([(37.6, 40), (36.6, 47)], 8.4, 7.6, flesh, group=8, bias=0.26)
    p.limb([(36.8, 46), (35.8, 52.4)], 9.4, 10.4, stone_d, group=9, bias=0.16)
    p.blob(34.6, 56.4, 6.8, 4.4, stone_d, ang=-6, group=9, bias=0.16)

    # ---- the body under the stone: belly and hip, in the stone's shadow
    p.poly(_closed([(26, 35), (32, 40.6), (39, 44.6), (46, 45.0), (53, 40.0), (55, 32), (40, 30), (29, 30)]),
           flesh, group=12, bias=0.22)

    # ---- the boulder and the ridge of plates running over it
    for k, (a, b, w) in enumerate(RIDGE):
        p.lens(_move([a], dy=-h)[0], _move([b], dy=-h)[0], w, stone, fat=0.4, bend=-0.6, group=60 + k,
               bias=-0.08)
    p.poly(_move(BOULDER, dy=-h), stone, group=24)

    # ---- the flesh swelling up round the stone's base where they have fused,
    # with roots of it creeping up into the stone's lower curve
    collar = _spline([(24.0, 29.6), (29.6, 35.8), (37.6, 38.4), (45.6, 38.2), (52.6, 34.6), (57.6, 29.0)], 6)
    p.limb(_move(collar, dy=-h * 0.5), 7.4, 4.6, flesh, group=26, bias=0.04)
    for a, b, w in (((32.0, 36.0), (30.6, 30.0), 3.6), ((41.0, 37.6), (41.6, 31.6), 3.2), ((49.6, 36.0), (51.6, 31.0), 2.8)):
        p.lens(_move([a], dy=-h * 0.5)[0], _move([b], dy=-h)[0], w, flesh, fat=0.2, group=26)

    # ---- head: round, thrust forward and low under the stone's lip, two
    # stubs of the same stone breaking through its brow, swept back like the
    # plates of the ridge they lead into
    p.lens((8.6, 28.0), (5.0, 20.4), 5.0, stone, fat=0.32, bend=0.6, group=30, bias=0.06)
    p.lens((15.6, 27.0), (17.6, 18.6), 5.8, stone, fat=0.32, bend=-0.6, group=31)
    p.blob(22.6, 33.4, 6.8, 6.2, flesh, group=33)  # neck
    p.blob(12.6, 34.2, 10.0, 8.8, flesh, group=34, ang=-6)
    # the nape plate, where the ridge comes down off the stone onto the neck
    p.lens((24.6, 30.4), (20.6, 25.0), 4.6, stone, fat=0.36, bend=0.4, group=35)

    # ---- near shoulder, straining up into the stone's front curve
    p.blob(29.0, 36.4, 8.4, 7.4, flesh, group=36, ang=-24)
    # near arm: flesh upper arm, a forearm of the same stone, a fist as big as
    # its head, knuckles dug into the slope ahead
    p.limb([(28.0, 40), (21.6, 46.2)], 9.6, 8.6, flesh, group=38)
    p.ox = ox0
    p.limb([(24.0, 45.4), (15.0, 50.4)], 11.4, 10.2, stone, group=40)
    p.blob(10.6, 54.0, 8.8, 5.8, stone, ang=-12, group=41)
    for cx, cy, r in ((3.4, 53.8, 2.6), (5.4, 50.4, 2.6), (9.0, 48.6, 2.6), (13.0, 48.2, 2.4)):
        p.circle(cx, cy, r, stone, group=41)

    p.ox = ox0 + 2 * p.s
    if big:
        _front_details(p, phase)
    p.ox = ox0


def _front_details(p, phase):
    """Draft placement of the glow and the face; the battle art is finished
    by hand in art/bouldyphus_front*.txt."""
    h = phase
    # the meander round the stone's girth
    pts = bez3((22.4, 24 - h), (30, 31 - h), (46, 31 - h), (58, 22 - h), n=40)
    p.stroke(pts, "v1")
    # the crack that runs down from the stone through the shoulder and arm
    p.stroke([(36, 12 - h), (36, 16 - h), (32, 16 - h), (32, 21 - h), (29, 21 - h), (29, 27 - h)], "v0")
    p.stroke([(27, 33), (25, 37), (22, 41), (18, 46), (14, 50)], "v0")
    # face: the gold eye, the screwed eye, the grin
    p.eye(7, 29, 5, 5, iris="go1", shine="v2")
    p.stroke([(15, 31), (17, 32), (19, 31)], "ink")
    p.stroke([(6, 37), (9, 38), (12, 37), (15, 38), (18, 36)], "v1")


# --------------------------------------------------------------------------
# Battle back: over the shoulder, the stone huge on its back
# --------------------------------------------------------------------------

BBOULDER = [(22, 5.2), (30, 4.4), (40, 4.6), (46, 6.2), (49.6, 9.4), (53.2, 13.6), (55.0, 19.6), (53.6, 22.0),
            (55.2, 28.0), (51.4, 38.6), (43, 45.6), (32, 47.6), (20, 45.6), (11.4, 39.4), (7.6, 30), (8.4, 22.6),
            (6.8, 17.6), (10.4, 11.4), (15.0, 7.4)]
BBC = (31.2, 25.6)
# ridge plates seen from behind: down the stone's crown toward the nape at right
BRIDGE = [(205, 2.6, 4.6), (228, 3.6, 5.8), (252, 4.6, 7.0), (277, 5.0, 7.4), (302, 4.6, 7.0), (326, 3.8, 6.0),
          (350, 3.0, 5.0)]


def _back(p, phase):
    import math
    h = phase
    # smoke legs streaming back and down out of the frame at the left
    p.limb(_spline([(16, 46), (11, 54), (8, 64)]), 12, 9, smoke, group=2, bias=0.16)
    p.lens((12, 52), (2.6, 58), 5.0, smoke, bend=1.0, fat=0.3, group=3, bias=0.2)
    # the back and shoulders, cropped by the frame
    p.poly([(10, 64), (12, 51), (18, 43), (32, 41), (46, 43), (56, 50), (58, 64)], flesh, group=10, bias=0.12)
    # shoulder blades straining under the weight
    p.blob(20, 51, 9.0, 7.4, flesh, group=11, ang=14)
    p.blob(41, 52, 8.4, 7.0, flesh, group=12, ang=-14, bias=0.06)
    # the near arm reaching forward right: flesh upper arm, stone forearm, fist
    p.limb([(46, 53), (53, 47)], 11, 10, flesh, group=13)
    p.limb([(52, 48), (57, 55)], 11, 11, stone, group=14)
    p.blob(57.6, 59.6, 5.4, 5.0, stone, group=15)
    # the boulder, huge, its ridge running down to the nape
    for k, (ang, ln, w) in enumerate(BRIDGE):
        t = math.radians(ang)
        bx, by = BBC[0] + 23.2 * math.cos(t), BBC[1] + 21.6 * math.sin(t) - h
        nx, ny = math.cos(t), math.sin(t)
        tx, ty = ny, -nx
        p.lens((bx - nx * 1.6, by - ny * 1.6), (bx + nx * ln + tx * ln * 0.45, by + ny * ln + ty * ln * 0.45), w,
               stone, fat=0.42, bend=0.8, group=19 + k % 2, bias=-0.1 + 0.03 * k)
    p.poly(_move(BBOULDER, dy=-h), stone, group=24)
    # flesh swelling up round the stone's base
    p.limb(_spline([(10, 40), (18, 46), (32, 49), (46, 46), (54, 39)], 6), 8, 6, flesh, group=26)
    # the head turned right in profile, low and forward under the stone's lip
    p.lens((51, 37), (49.6, 29.6), 5.0, stone, fat=0.32, bend=0.6, group=30)
    p.blob(53.0, 42.4, 8.6, 7.4, flesh, group=34)
    if p.big:
        p.eye(55, 38, 4, 5, iris="go1", shine="v2")
        p.stroke([(52, 46), (55, 47), (58, 46), (60, 44)], "v1")


# --------------------------------------------------------------------------
# Follower views
# --------------------------------------------------------------------------

def _down(p, phase):
    """Walking toward the camera: head low and forward between the two
    fists, the boulder looming over its back."""
    st = 1 if phase else -1
    # smoke trailing behind
    p.lens((24, 46), (16, 58), 5.0, smoke, group=2, bias=0.2)
    p.lens((40, 46), (48, 58), 5.0, smoke, group=2, bias=0.2)
    # boulder with its ridge
    for k, (a, b, w) in enumerate((((32, 6), (32, 1.4), 5.0), ((25, 8), (22, 4), 4.0), ((39, 8), (42, 4), 4.0))):
        p.lens(a, b, w, stone, fat=0.24, group=4 + k % 2)
    p.blob(32, 22, 18, 16.5, stone, group=6)
    p.limb(_spline([(14, 30), (22, 37), (32, 39), (42, 37), (50, 30)]), 7, 7, flesh, group=7)
    # shoulders and arms, fists planted either side
    for side in (-1, 1):
        sx = 32 + side * 13
        p.blob(sx, 38, 7.0, 6.0, flesh, group=10 + side)
        p.limb([(sx + side * 2, 41), (sx + side * 4, 49 + st * side * 0.6)], 7.6, 8.4, stone, group=12 + side)
        p.blob(sx + side * 4.6, 53 + st * side * 0.8, 6.4, 4.6, stone, group=14 + side)
    # the head
    for side in (-1, 1):
        p.lens((32 + side * 4, 35), (32 + side * 7.4, 29.4), 4.2, stone, fat=0.26, group=17 + side)
    p.blob(32, 42, 8.8, 7.8, flesh, group=20)
    if p.big:
        p.eye(26, 39, 4, 5, iris="go1", shine="v2")
        p.stroke([(35, 41), (37, 42), (39, 41)], "ink")
        p.stroke([(26, 46), (29, 47), (32, 46), (35, 47), (38, 45)], "v1")
        p.stroke(bez3((14.4, 24), (22, 30), (42, 30), (49.6, 24), n=30), "v1")
    else:
        p.px(27.5, 41, "go1")


def _up(p, phase):
    """Walking away: the boulder and its ridge, the smoke legs below."""
    st = 1 if phase else -1
    p.lens((26, 44), (20 + st, 58), 6.0, smoke, group=2, bias=0.1)
    p.lens((38, 44), (44 + st, 58), 6.0, smoke, group=3, bias=0.1)
    for side in (-1, 1):
        p.blob(32 + side * 17, 47 + st * side * 0.8, 6.0, 4.6, stone, group=5 + side)
    p.poly([(16, 50), (18, 40), (46, 40), (48, 50), (32, 53)], flesh, group=8)
    for k, (a, b, w) in enumerate((((32, 5), (32, 0.6), 5.4), ((32, 13), (26, 8), 0), ((32, 13), (38, 8), 0))):
        if w:
            p.lens(a, b, w, stone, fat=0.24, group=9)
    p.blob(32, 24, 18.5, 18.0, stone, group=10)
    p.limb(_spline([(14, 34), (22, 42), (32, 44), (42, 42), (50, 34)]), 7, 7, flesh, group=11)
    if p.big:
        p.stroke(bez3((14, 28), (22, 36), (42, 36), (50, 28), n=30), "v1")
        p.stroke([(32, 6), (32, 20)], "s0")


# --------------------------------------------------------------------------

def bouldyphus(p, view, phase):
    if view in ("front", "side", "icon"):
        _front(p, phase if view != "side" else 0)
    elif view == "back":
        _back(p, phase)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)


MONS = [
    Mon("Bouldyphus", COLORS, SHINY, bouldyphus, foot="blank"),
]
