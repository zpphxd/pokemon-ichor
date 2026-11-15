"""Salmoneus line: Lebetron (Steel/Electric), a single stage. King
Salmoneus, who dragged bronze kettles behind his chariot to fake Zeus's
thunder and threw torches for lightning, until Zeus struck him down."""

from mon_lib import C, Mat, Mon

INK = C.ink


def _spline(pts, n=8):
    """A smooth path through pts (Catmull-Rom)."""
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


def _closed(pts, n=8):
    """A smooth closed outline through pts."""
    P = list(pts) + list(pts[:3])
    out = _spline(P, n)
    return out[n:n + n * len(pts)]


# --------------------------------------------------------------------------
# Lebetron, the thunder-faker
# --------------------------------------------------------------------------

LEBETRON_COLORS = [
    ("ink", INK),
    # terracotta bronze, hammered and polished
    ("br0", (88, 40, 24)), ("br1", (144, 72, 40)), ("br2", (192, 112, 56)), ("br3", (232, 160, 80)),
    ("br4", (248, 216, 144)),
    # the sun-gold crown and the torch flame
    ("gold0", (152, 104, 16)), ("gold1", (232, 184, 40)), ("gold2", (248, 240, 152)),
    ("fire", (232, 88, 32)),
    # the real spark: white and Aegean blue
    ("white", C.white), ("blue0", (48, 104, 176)), ("blue1", (136, 192, 240)),
    # verdigris on the old dragged kettles
    ("pat0", (40, 96, 88)), ("pat1", (88, 152, 128)),
]
LEBETRON_SHINY = {
    # silver-gray tin kettles under a gold crown
    "br0": (56, 56, 72), "br1": (104, 104, 120), "br2": (152, 152, 168), "br3": (200, 200, 208),
    "br4": (240, 240, 240),
    "pat0": (72, 72, 104), "pat1": (120, 128, 160),
}

l_br = Mat(["br0", "br1", "br2", "br3", "br4"], line="br0", cuts=[0.14, 0.34, 0.58, 0.8])
l_head = Mat(["br0", "br1", "br2", "br3", "br4"], line="br0", cuts=[0.12, 0.3, 0.54, 0.78])
l_old = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.24, 0.5, 0.76])
l_rim = Mat(["br1", "br2", "br3", "br4"], line="br0", cuts=[0.26, 0.52, 0.76])
l_dark = Mat(["br0", "br1"], line="br0", cuts=[0.5])
l_gold = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.36, 0.7])
l_fire = Mat(["fire", "gold1", "gold2"], line="fire", cuts=[0.3, 0.66])
l_rod = Mat(["br0", "br2", "br4"], line="br0", cuts=[0.4, 0.7])


def _kettle(p, cx, cy, r, tilt=0.0, bias=0.0, group=None):
    """A dented, dragged kettle: round belly, a lighter rim round a dark
    mouth, and verdigris on its belly."""
    p.blob(cx, cy, r, r * 0.86, l_old, ang=tilt, bias=bias, group=group)
    rim = p.blob(cx + 0.3, cy - r * 0.62, r * 0.7, r * 0.3, l_rim, ang=tilt, bias=bias - 0.06, group=group + 1)
    p.blob(cx + 0.3, cy - r * 0.66, r * 0.42, r * 0.16, Mat(["br0"]), ang=tilt, clip=[rim], group=group + 2)
    if p.big:
        p.pxs([(cx - r * 0.5, cy + r * 0.4), (cx - r * 0.3, cy + r * 0.55)], "pat1")
        p.px(cx - r * 0.5, cy + r * 0.55, "pat0")


def _icon(p):
    """Party icon: the strut, the crown, the torch and one kettle, chunky
    enough to read at 32 px."""
    flat = lambda m, f: dict(flat=f)
    _kettle(p, 46, 52, 6.0, tilt=-12, bias=0.08, group=60)
    p.limb([(37, 50), (41, 47.5)], 2.4, 2.4, l_dark, group=66)
    p.limb([(26, 54), (25, 60)], 6.4, 6, l_br, group=11)
    p.limb([(34, 54), (35, 60)], 6.4, 6, l_br, bias=0.2, group=12)
    p.blob(30, 46, 11.6, 9.6, l_br, group=1)
    p.blob(31, 37.4, 9, 2.6, l_rim, group=2)
    p.blob(29, 28.5, 8.6, 8, l_head, group=3)
    p.poly([(22, 26), (16.5, 26), (15.5, 29), (22, 31.5)], l_head, group=4)
    p.limb([(20, 40), (15.6, 34), (14.6, 27)], 5.4, 5, l_br, group=13)
    p.limb([(14.6, 27), (13.6, 19)], 2.8, 2.6, l_dark, group=14)
    p.poly([(10.4, 19.5), (17.4, 19.5), (17.6, 15), (15, 14), (17, 9.5), (13, 6.5), (13, 10.5), (10, 12), (12, 15.5),
            (10, 16.5)], l_fire, group=16)
    p.blob(30, 20.6, 8.4, 2.4, l_gold, group=20, flat=1)
    for bx in (24.5, 30, 35.5):
        p.limb([(bx, 20), (bx + (bx - 30) * 0.15, 14.5)], 3.4, 3.2, l_gold, group=21, flat=1)
    p.px(24, 26, "ink")
    p.px(25, 26, "ink")
    p.px(30, 12, "white")
    p.px(30, 11, "blue1")




def lebetron(p, view, phase):
    if view == "icon":
        _icon(p)
        return
    if view in ("front", "side"):
        H = 1 if (phase == 1 and view == "front") else 0   # frame 2: chin higher, torch shaken
        walk = view == "side"
        B = phase if walk else 0                            # kettles bouncing on the walk

        # the train of kettles dragged behind, receding up and to the right
        _kettle(p, 57.5, 44.5 - B, 3.4, tilt=-24, bias=0.16, group=60)
        _kettle(p, 52, 49.6 - 2 * (1 - B) * walk, 4.0, tilt=16, bias=0.1, group=62)
        _kettle(p, 45, 55.2 - 2 * B, 4.6, tilt=-12, bias=0.04, group=64)
        # the chain from its back to the kettles' handles
        p.limb(_spline([(37, 47), (41.5, 50), (45, 50.4), (48.5, 47.5), (52, 45.4), (55, 42.5), (57.5, 40.8)], 4),
               1.4, 1.4, l_dark, group=66)

        # far arm, fist planted on the hip
        p.limb([(35, 39), (41.5, 41.5), (38.5, 47)], 4.4, 4.0, l_br, bias=0.2, group=10)
        # far leg
        fx = (35 if phase else 29) if walk else 32
        p.limb([(31, 53), (fx, 58.5)], 5.6, 5.0, l_br, bias=0.22, group=11)
        p.blob(fx + 0.5, 59.2, 3.6, 1.6, l_br, bias=0.2, group=11)

        # the cauldron body, chest puffed out, and its rim for a collar
        body = p.blob(27, 46, 11.5, 10.2, l_br, group=1)
        p.blob(22, 45, 7, 7.6, l_br, bias=-0.04, group=1)
        p.blob(27.5, 36.4, 9.2, 2.8, l_rim, ang=-6, group=2)
        # the chain slung across the chest like a sash
        p.limb(_spline([(34.5, 37.5), (27, 44), (19, 51), (17, 53)], 4), 1.8, 1.8, l_dark, clip=[body], group=5)

        # the head: a round bronze dome tipped back, with a short hooked beak
        p.blob(24.5, 28 - H, 8.4, 7.8, l_head, ang=-10, group=3)
        p.poly(_closed([(18.5, 25 - H), (15.5, 24.4 - H), (13.6, 25.6 - H), (13.6, 28 - H), (15.6, 28.6 - H),
                        (18, 30 - H)], 4), l_head, group=4)

        # the lopsided crown of bent kettle handles, tipped back
        p.blob(26, 20.8 - H, 6.6, 2.0, l_gold, ang=14, group=20)
        for (bx, by), (tx, ty), w in (((20.5, 19.5), (19, 14.5), 3.0), ((25, 20), (25, 13.5), 3.0),
                                      ((29.5, 21.5), (31.5, 16), 3.0)):
            p.limb(_spline([(bx, by - H), ((bx + tx) / 2 - 1.2, (by + ty) / 2 - H), (tx, ty - H)], 4),
                   w, w * 0.8, l_gold, group=21)
        # the lightning rod through the crown, a real spark at its tip
        p.limb([(27, 20 - H), (28, 8.5 - H)], 1.6, 1.2, l_rod, group=22)
        p.circle(28, 8 - H, 1.3, l_rod, group=23)

        # near leg, stout, on a lion's-paw foot like a tripod cauldron's
        nx = (17 if phase else 23) if walk else 20.5
        p.limb([(21, 54), (nx, 58.5)], 6, 5.4, l_br, group=12)
        p.blob(nx - 1.5, 59.4, 4.2, 1.8, l_br, group=12)

        # near arm, raising the torch high like a thunderbolt
        p.limb(_spline([(17, 40), (10.5, 36), (9, 27.5 - H)], 4), 4.8, 4.2, l_br, group=13)
        p.blob(9, 26 - H, 2.8, 2.6, l_br, group=13)
        p.limb([(9.5, 28.5 - H), (8, 17 - H)], 2.2, 2.0, l_dark, group=14)
        p.blob(8, 16.5 - H, 2.6, 1.6, l_br, group=15)
        # the flame, jagged like a lightning bolt
        p.poly([(5.5, 16 - H), (10.5, 16 - H), (11, 12.5 - H), (8.5, 11.5 - H), (11.5, 7 - H), (7.5, 3.5 - H),
                (7.5, 7 - H), (5, 8 - H), (6.5, 11.5 - H), (4.5, 13 - H)], l_fire, group=16)

        if p.big:
            # spark crackling at the rod's tip
            p.stroke([(25, 5 - H), (26.5, 6.5 - H), (25.5, 8 - H)], "blue1")
            p.stroke([(30.5, 4.5 - H), (29.5, 6.5 - H), (31, 8 - H)], "blue1")
            p.pxs([(27, 7 - H), (28, 6 - H)], "white")
            # face: a big haughty eye, half-lidded, gazing up past its beak
            p.patch(17, 23 - H, [".1111.", "122221", "1b1111", "1b1w11", ".1111."],
                    {"1": "ink", "2": "br1", "b": "blue0", "w": "white"})
            p.pxs([(24, 24 - H), (24, 25 - H)], "ink")
            p.stroke([(13.5, 28.5 - H), (16, 30 - H)], "br0")
        else:
            p.px(19, 25, "ink")
        return

    if view == "back":
        # over the shoulder at 1.2x: the cauldron's broad back with the chain
        # slung over it, the head turned right in profile, the crown askew,
        # the rod sparking and the torch held high
        p.limb(_spline([(46, 46), (53, 40), (55.5, 31)], 4), 6.4, 5.4, l_br, bias=0.1, group=13)
        p.blob(55.5, 29.5, 3.6, 3.4, l_br, bias=0.1, group=13)
        p.limb([(56, 32), (57.5, 15)], 2.6, 2.4, l_dark, group=14)
        p.blob(57.5, 14.5, 3.2, 2, l_br, group=15)
        p.poly([(54.5, 14), (60.5, 14), (61, 10), (58.5, 9), (61.5, 4), (57.5, 1), (57.5, 5), (55, 6), (56.5, 10),
                (54, 11)], l_fire, group=16)
        body = p.blob(28, 64, 27, 22, l_br, group=1)
        p.blob(29, 43.5, 19, 4.4, l_rim, ang=-3, group=2)
        p.blob(31, 30, 10.4, 9.8, l_head, ang=8, group=3)
        p.poly(_closed([(39, 27.5), (44, 25.5), (48, 26.5), (48.5, 29.5), (46, 30), (41, 34)], 4), l_head, group=4)
        p.blob(30, 20.5, 8, 2.4, l_gold, ang=-12, group=20)
        for (bx, by), (tx, ty) in (((24, 21.5), (22.5, 15)), ((29, 20.5), (28.5, 13)), ((35, 19), (37, 12.5))):
            p.limb(_spline([(bx, by), ((bx + tx) / 2 + 1.2, (by + ty) / 2), (tx, ty)], 4), 3.4, 2.8, l_gold,
                   group=21)
        p.limb([(31.5, 19), (33, 6)], 1.8, 1.4, l_rod, group=22)
        p.circle(33, 5.5, 1.5, l_rod, group=23)
        # the chain over the shoulder and down the back
        p.limb(_spline([(44, 44), (34, 50), (22, 56), (12, 64)], 4), 2.2, 2.2, l_dark, clip=[body], group=5)
        if p.big:
            p.stroke([(29, 2), (30.5, 4), (29.5, 6)], "blue1")
            p.stroke([(36.5, 2), (35.5, 4), (37, 6)], "blue1")
            p.pxs([(32, 4), (33, 3)], "white")
            p.patch(37, 24, [".111.", "12221", "1w1b1", ".111."], {"1": "ink", "2": "br1", "b": "blue0", "w": "white"})
        return

    if view in ("down", "up"):
        # follower: strutting toward or away from the camera, torch high,
        # the kettles bouncing along behind
        st = phase
        down = view == "down"
        tx = 14 if down else 50                 # the torch hand: its right hand
        hx = 50 if down else 14                 # the other fist, on the hip
        if down:
            # kettles peeking out behind, bouncing in turn
            _kettle(p, 51, 52 - 2 * st, 4.6, tilt=10, bias=0.12, group=60)
        p.limb([(25, 52), (25, 59 - 2 * st)], 6, 5.4, l_br, group=11)
        p.limb([(39, 52), (39, 59 - 2 * (1 - st))], 6, 5.4, l_br, group=12)
        p.blob(25, 59.4 - 2 * st, 4.2, 1.8, l_br, group=11)
        p.blob(39, 59.4 - 2 * (1 - st), 4.2, 1.8, l_br, group=12)
        p.limb([(42 if down else 22, 40), (hx, 42), (46 if down else 18, 48)], 4.6, 4.2, l_br, bias=0.1, group=13)
        p.limb(_spline([(22 if down else 42, 39), (tx + (2 if down else -2), 33), (tx, 25)], 4), 4.8, 4.2, l_br,
               group=14)
        p.blob(tx, 24, 3, 2.8, l_br, group=14)
        p.limb([(tx, 26), (tx - 1, 13)], 2.4, 2.2, l_dark, group=15)
        p.poly([(tx - 3.5, 13), (tx + 2, 13), (tx + 2.5, 9), (tx, 8), (tx + 3, 3.5), (tx - 1, 0.5 + 1), (tx - 1, 4),
                (tx - 4, 5), (tx - 2.5, 9), (tx - 4.5, 10.5)], l_fire, group=16)
        body = p.blob(32, 45, 12, 10.6, l_br, group=1)
        p.blob(32, 35.6, 9.6, 2.8, l_rim, group=2)
        p.blob(32, 27, 8.6, 8, l_head, group=3)
        p.blob(32, 19.6, 6.6, 2.0, l_gold, ang=-8 if down else 8, group=20)
        for bx, tx2 in ((27, 25.5), (32, 32), (37, 38.5)):
            p.limb([(bx, 19.5), (tx2, 13.5)], 3.0, 2.6, l_gold, group=21)
        p.limb([(33, 19), (33.5, 7.5)], 1.6, 1.2, l_rod, group=22)
        p.circle(33.5, 7, 1.4, l_rod, group=23)
        if down:
            p.limb(_spline([(40, 36.5), (32, 44), (24, 52)], 4), 1.8, 1.8, l_dark, clip=[body], group=5)
            p.poly([(29.5, 29), (34.5, 29), (32, 33.5)], l_head, group=4)
            p.eye(26.5, 24, 3, 4, shine="white")
            p.eye(34.5, 24, 3, 4, shine="white")
        else:
            p.limb(_spline([(24, 36.5), (34, 44), (42, 52), (44, 58)], 4), 1.8, 1.8, l_dark, group=5)
            _kettle(p, 46, 58 - 2 * st, 4.4, tilt=-10, bias=0.04, group=60)
        return

MONS = [
    # icon palette 3 keeps the bronze warm and the crown gold
    Mon("Lebetron", LEBETRON_COLORS, LEBETRON_SHINY, lebetron, foot="paw", icon_pal=3),
]
