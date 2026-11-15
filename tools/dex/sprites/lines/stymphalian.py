"""Stymphalian line: Chalkip, Belornis (Steel/Flying). Ares's bronze-beaked
birds of the Stymphalian marsh, which shot their feathers like arrows until
Herakles scared them up with Hephaestus's rattles (Apollodorus 2.5.6)."""
import math

from mon_lib import C, Mat, Mon, bez, bez3, lens_pts

INK = C.ink


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def _lit_left(a, b):
    """True when the +normal side of a->b faces the upper-left light."""
    return (b[1] - a[1]) - (b[0] - a[0]) > 0


def arrowhead(tip, back, L, W, sw=0.8):
    """A barbed arrowhead pointing at `tip`, coming from the direction of
    `back`: length L, barb span W, shaft width sw at the notch. Returns
    (whole polygon, lit half)."""
    ux, uy = _unit(back, tip)
    nx, ny = -uy, ux
    bx, by = tip[0] - ux * L, tip[1] - uy * L
    mx, my = tip[0] - ux * L * 0.6, tip[1] - uy * L * 0.6
    bl, br = (bx + nx * W / 2, by + ny * W / 2), (bx - nx * W / 2, by - ny * W / 2)
    nl, nr = (mx + nx * sw / 2, my + ny * sw / 2), (mx - nx * sw / 2, my - ny * sw / 2)
    whole = [tip, bl, nl, nr, br]
    lit = [tip, bl, nl, (mx, my)] if _lit_left(back, tip) else [tip, (mx, my), nr, br]
    return whole, lit


def blade(p, a, b, w, mat, lit, shade, fat=0.42, bend=0.0, sheen=None, **kw):
    """A flat-toned Gen 3 feather from a to b: the half facing the light at
    ramp level `lit`, the other at `shade`, split along the rachis; an
    optional sheen color just inside the lit edge."""
    pts = lens_pts(a, b, p._minw(w), bend, fat=fat)
    if not p.big:
        return p.poly(pts, mat, flat=lit, **kw)
    pid = p.poly(pts, mat, flat=shade, **kw)
    n = len(pts) // 2
    left, right = pts[:n], pts[n:][::-1]
    mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(left, right)]
    edge = left if _lit_left(a, b) else right
    kw.pop("group", None)
    kw.pop("bias", None)
    p.poly(edge + mid[::-1], mat, clip=[pid], flat=lit, noline=True, **kw)
    if sheen:
        for i in (int(n * 0.34), int(n * 0.5)):
            ex, ey = edge[i]
            mx, my = mid[i]
            d = math.hypot(mx - ex, my - ey) or 1
            k = min(1.4, d * 0.55) / d
            p.px(ex + (mx - ex) * k - 0.5, ey + (my - ey) * k - 0.5, sheen)
    return pid


def head_tip(p, tip, back, L, W, mat, lit, shade, sw=0.9, glint=None, **kw):
    """A barbed metal arrowhead, flat-toned in two halves."""
    whole, half = arrowhead(tip, back, L, W, sw)
    if not p.big:
        return p.poly(whole, mat, flat=lit, **kw)
    pid = p.poly(whole, mat, flat=shade, **kw)
    kw.pop("group", None)
    kw.pop("bias", None)
    p.poly(half, mat, clip=[pid], flat=lit, noline=True, **kw)
    if glint:
        ux, uy = _unit(back, tip)
        p.px(tip[0] - ux * 1.6 - 0.5, tip[1] - uy * 1.6 - 0.5, glint)
    return pid


def _tufts(p, cx, cy, rx, ry, angs, mat, ln=2.4, w=2.2, group=None, bias=0.0):
    """Down sticking out of an ellipse's rim at the given angles (degrees,
    0 = right, 90 = down); lengths vary so the fluff isn't stamped."""
    for i, a in enumerate(angs):
        r = math.radians(a)
        bx, by = cx + rx * 0.8 * math.cos(r), cy + ry * 0.8 * math.sin(r)
        l = ln * (0.7 + 0.3 * ((i * 5) % 3))
        tx, ty = cx + (rx + l) * math.cos(r + 0.22), cy + (ry + l) * math.sin(r + 0.22)
        p.lens((bx, by), (tx, ty), w, mat, group=group, bias=bias)


# --------------------------------------------------------------------------
# Chalkip, the bronze crane chick
# --------------------------------------------------------------------------

CHALKIP_COLORS = [
    ("ink", INK),
    # marble-gray down
    ("down0", (104, 104, 112)), ("down1", (152, 152, 160)), ("down2", (200, 200, 200)), ("down3", (240, 240, 232)),
    # terracotta-to-sun-gold bronze: beak and pin-feathers
    ("br0", (112, 48, 24)), ("br1", (176, 96, 40)), ("br2", (224, 160, 56)), ("br3", (248, 216, 112)),
    # cypress-dark legs
    ("leg0", (24, 56, 40)), ("leg1", (48, 96, 64)),
    ("red", (216, 48, 40)),
    # the reed tuft
    ("reed0", (64, 88, 32)), ("reed1", (112, 136, 56)), ("reed2", (168, 176, 96)),
]
CHALKIP_SHINY = {
    # olive verdigris bronze, limestone-tan down
    "br0": (32, 72, 56), "br1": (64, 128, 96), "br2": (112, 176, 128), "br3": (184, 224, 168),
    "down0": (136, 104, 72), "down1": (176, 144, 96), "down2": (208, 184, 136), "down3": (232, 216, 176),
}

c_down = Mat(["down0", "down1", "down2", "down3"], line="down0", cuts=[0.2, 0.46, 0.74])
c_bronze = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.2, 0.44, 0.72])
c_leg = Mat(["leg0", "leg1"], line="leg0", cuts=[0.55])
c_reed = Mat(["reed0", "reed1", "reed2"], line="reed0", cuts=[0.36, 0.7])


def _pin(p, base, tip, w=2.8, head=1.0, group=None, back=False):
    """A bronze pin-feather poking out of the down: a quill tipped with a
    barbed arrowhead. back=True tones it down for the far side."""
    ux, uy = _unit(base, tip)
    neck = (tip[0] - ux * 2.2 * head, tip[1] - uy * 2.2 * head)
    lit, shade = (1, 0) if back else (2, 1)
    blade(p, base, neck, w, c_bronze, lit, shade, fat=0.3, group=group)
    g = None if group is None else group + 200
    head_tip(p, tip, base, 3.2 * head, 3.6 * head, c_bronze, lit + 1, shade + 1, group=g)


def _reeds(p, x, y, front, sw=0):
    """The reed tuft the chick stands in. front=False draws the blades
    behind the leg, True the two in front."""
    if not front:
        for a, b, w, bend, lit in (((x + 4, y), (x + 9 + sw, y - 13), 2.8, -0.8, 1),
                                   ((x + 1, y), (x - 2 + sw, y - 11), 2.6, 0.6, 1),
                                   ((x + 7, y), (x + 14 + sw, y - 7), 2.6, -0.6, 1),
                                   ((x - 3, y), (x - 9 + sw, y - 6), 2.4, 0.5, 1)):
            blade(p, a, b, w, c_reed, lit, 0, bend=bend, fat=0.25)
    else:
        for a, b, w, bend in (((x - 1, y + 0.5), (x - 6 + sw, y - 8), 2.8, 0.7),
                              ((x + 3, y + 0.5), (x + 6 + sw, y - 5), 2.6, -0.5)):
            blade(p, a, b, w, c_reed, 2, 1, bend=bend, fat=0.25)


def chalkip(p, view, phase):
    if view in ("front", "side", "icon"):
        F = 1 if (phase == 1 and view == "front") else 0   # panicked flap
        hop = 1 if (phase == 1 and view == "side") else 0

        _reeds(p, 36, 61, False, sw=F)
        # crown pins, behind the head
        _pin(p, (31, 22 - F), (35, 15 - 2 * F), group=30, back=True)
        # far wing stub, raised a little behind the body
        p.lens((38, 35), (45, 30 - 3 * F), 5.6, c_down, bend=1.0, bias=0.3, group=9)
        # the stilt leg: thigh, backward knee, shank
        p.limb([(37, 47 - hop), (38.5, 53 - hop)], 2.8, 2.4, c_leg, group=12)
        p.limb([(38.5, 53 - hop), (36.5, 59.5 - hop)], 2.4, 2.1, c_leg, group=12)
        for dx, dy in ((-5, 0.8), (-3.4, 1.7), (2.8, 0.6)):
            p.limb([(36.5, 59.8 - hop), (36.5 + dx, 59.8 + dy - hop)], 1.6, 1.3, c_leg, group=12)
        # the tucked leg, folded up under the down
        p.limb([(41, 46), (44.5, 49), (41.5, 50.5)], 2.2, 1.8, c_leg, bias=0.2, group=13)
        # tail fluff
        p.lens((44, 38.5), (50.5, 36 - F), 5.2, c_down, bend=-0.6, bias=0.1, group=1)
        # body: a round ball of down
        p.blob(38, 41, 9, 7.8, c_down, group=1)
        # neck and big round head
        p.limb([(33.5, 37), (31, 32)], 8, 7.6, c_down, group=1)
        p.blob(29.5, 27.5 - F, 7.6, 7, c_down, group=3)
        # the near crown pins, in front
        _pin(p, (26.5, 21.5 - F), (24.5, 14 - 2 * F), group=33)
        _pin(p, (29, 21 - F), (29.5, 13 - 2 * F), group=35)
        # the long straight beak; open in the panic frame
        if F:
            p.poly([(23.5, 24.5), (11.5, 23.2), (11.5, 24.4), (23.5, 27.5)], c_bronze, group=5)
            p.poly([(23.5, 29), (13, 30.6), (13, 31.6), (23.5, 31)], c_bronze, group=6, bias=0.2)
        else:
            p.poly([(23.5, 26.5), (17, 27.6), (11, 29.2), (11, 30.2), (17, 30.6), (23.5, 31)], c_bronze, group=5)
        # near wing stub
        if F:
            p.lens((36, 38), (45.5, 31.5), 6.4, c_down, bend=1.6, group=10)
        else:
            p.lens((35.5, 37.5), (45.5, 41.5), 6.6, c_down, bend=-1.8, group=10)
        _reeds(p, 36, 61, True, sw=F)

        if p.big:
            p.eye(25, 24 - F, 3, 4, iris="red", shine="down3")
        else:
            p.px(26, 26 - F, "ink")
        return

    if view == "back":
        # over the shoulder: the round down back with the wing stubs and
        # pins, the head turned right in profile
        p.blob(28, 62, 22, 16, c_down, group=1)
        _tufts(p, 28, 62, 22, 16, (-170, -150, -130, -110), c_down, ln=2.6, w=3, group=1)
        p.limb([(36, 48), (40, 38)], 11, 10, c_down, group=1)
        _pin(p, (40, 22), (36.5, 12), w=3.2, head=1.2, group=30, back=True)
        p.blob(43, 30, 8.6, 8.2, c_down, group=3)
        _tufts(p, 43, 30, 8.6, 8.2, (-150, -120, 180, 160), c_down, ln=2.0, w=2.6, group=3)
        _pin(p, (44, 22.5), (45, 13), w=3.2, head=1.2, group=31)
        p.poly([(50, 29), (62, 31), (62, 32.2), (50, 34)], c_bronze, group=5)
        # the near wing stub, its pins fanned up the back
        for a, b in (((12, 45), (5, 37)), ((15, 44), (11, 35)), ((10, 48), (2.5, 44))):
            _pin(p, a, b, w=3.2, head=1.2, group=34)
        p.lens((22, 50), (8, 44), 9, c_down, bend=1.6, group=10)
        _reeds(p, 50, 64, True)
        if p.big:
            p.eye(48, 26, 3, 4, iris="red", shine="down3", shine_at=(0, 1))
        return

    if view in ("down", "up"):
        # follower: hopping and flapping, never lifting off
        hop = phase
        _reeds(p, 32, 62, False)
        for x in (29.5, 34.5):
            p.limb([(x, 48 - hop), (x, 58 - hop)], 2.4, 2.0, c_leg, group=12)
            p.limb([(x, 58.5 - hop), (x - 2, 60 - hop)], 1.6, 1.3, c_leg)
            p.limb([(x, 58.5 - hop), (x + 2, 60 - hop)], 1.6, 1.3, c_leg)
        p.blob(32, 42 - hop, 8.6, 7.6, c_down, group=1)
        _tufts(p, 32, 42 - hop, 8.6, 7.6, (60, 90, 120), c_down, ln=2, w=2.4, group=1)
        up = 4 * hop
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            _pin(p, (X(43), 38.5 - up), (X(49), 35 - up), group=20 + sx)
            p.lens((X(37), 40 - hop), (X(45), 38 - up), 5.4, c_down, bend=-sx, group=10 + sx)
        p.blob(32, 30 - hop, 7, 6.6, c_down, group=3)
        _pin(p, (31, 25 - hop), (29.5, 17.5 - hop), group=30)
        _pin(p, (33, 25 - hop), (35, 18 - hop), group=31)
        if view == "down":
            p.blob(32, 45 - hop, 5, 4, c_down, bias=-0.2, group=2)
            p.eye(28, 28 - hop, 2, 3, iris="red", shine="down3")
            p.eye(34, 28 - hop, 2, 3, iris="red", shine="down3")
            p.limb([(32, 32 - hop), (32, 38 - hop)], 2.8, 1.4, c_bronze, group=5)
        _reeds(p, 32, 62, True)
        return


# --------------------------------------------------------------------------
# Belornis, the Stymphalian bird
# --------------------------------------------------------------------------

BELORNIS_COLORS = [
    ("ink", INK),
    # marble-gray plumage
    ("pl0", (88, 88, 104)), ("pl1", (136, 136, 144)), ("pl2", (184, 184, 184)), ("pl3", (224, 224, 216)),
    ("white", C.white),
    # terracotta-to-sun-gold bronze, with a hot glint
    ("br0", (96, 40, 24)), ("br1", (160, 80, 40)), ("br2", (208, 136, 48)), ("br3", (240, 192, 72)),
    ("br4", (248, 232, 152)),
    # cypress-dark legs
    ("leg0", (24, 48, 40)), ("leg1", (56, 96, 72)),
    # the red eye and crown patch
    ("red0", (136, 24, 32)), ("red1", (216, 56, 48)),
]
BELORNIS_SHINY = {
    # olive verdigris bronze, charcoal plumage: bronze long buried
    "br0": (32, 56, 48), "br1": (56, 104, 72), "br2": (96, 144, 96), "br3": (144, 184, 120), "br4": (200, 224, 168),
    "pl0": (40, 40, 48), "pl1": (72, 72, 80), "pl2": (104, 104, 112), "pl3": (152, 152, 160),
}

b_plume = Mat(["pl0", "pl1", "pl2", "pl3"], line="pl0", cuts=[0.2, 0.44, 0.7])
b_bronze = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.18, 0.4, 0.66])
b_metal = Mat(["br1", "br2", "br3", "br4"], line="br0", cuts=[0.2, 0.42, 0.66])
b_leg = Mat(["leg0", "leg1"], line="leg0", cuts=[0.55])
b_red = Mat(["red0", "red1"], line="red0", cuts=[0.5])


def _flying_dart(p, tail, tip, group):
    """A loosed dart hanging in the air: fletching, shaft and barbed head."""
    ux, uy = _unit(tail, tip)
    neck = (tip[0] - ux * 3.6, tip[1] - uy * 3.6)
    p.limb([tail, neck], 1.6, 1.6, b_bronze, group=group, flat=1, cap=False)
    blade(p, tail, (tail[0] + ux * 5.5, tail[1] + uy * 5.5), 3.6, b_bronze, 2, 1, fat=0.35, group=group + 1)
    head_tip(p, tip, tail, 4.6, 4.6, b_metal, 2, 1, sw=1.4, glint="br4", group=group + 2)


def _bfoot(p, x, y, spread, far=False):
    b = 0.3 if far else 0.0
    for a in spread:
        r = math.radians(a)
        ln = 4.6 if a < 90 else 2.6
        p.limb([(x, y), (x - ln * math.cos(r), y + ln * math.sin(r))], 2.0, 1.4, b_leg, bias=b)


def _sdart(p, base, tip, w, group, bright=True):
    """A dart-primary simplified for the code draft: a two-toned vane and a
    wide barbed head; drawn fatter at follower and icon size."""
    k = 1.0 if p.big else 1.5
    ux, uy = _unit(base, tip)
    neck = (tip[0] - ux * 3.6, tip[1] - uy * 3.6)
    blade(p, base, neck, w * k, b_bronze, 2 if bright else 1, 1 if bright else 0, fat=0.5, group=group)
    head_tip(p, tip, base, 5.6, 6.4 * k, b_metal, 3 if bright else 2, 2 if bright else 1, sw=1.8, group=group + 100)


def _polar(c, ang, r):
    a = math.radians(ang)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def _scallop(a, b, n, amp):
    """A trailing edge from a to b broken into n feather tips."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = dy / d, -dx / d
    out = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        bump = amp * abs(math.sin(math.pi * t * n))
        out.append((a[0] + dx * t + nx * bump, a[1] + dy * t + ny * bump))
    return out


def _bwing(p, lead, w0, w1, prim, secs, group, bright=True):
    """A raised wing: dart primaries trailing from the hand, a gray
    secondary mass with a scalloped edge, then the arm band whose outer side
    is the curved leading edge."""
    for i, (b, ang, L) in reversed(list(enumerate(prim))):
        _sdart(p, b, _polar(b, ang, L), 3.6, group + i, bright=bright and i % 2 == 0)
    bias = 0 if bright else 0.3
    p.poly(secs, b_plume, bias=bias, group=group + 20)
    p.limb(lead, w0, w1, b_plume, bias=bias - 0.1, group=group + 21)


def belornis(p, view, phase):
    if view in ("front", "side", "icon"):
        # the code draft of the hand-finished front: a raptor-crane mantling
        # both gray wings, its dart primaries fanned like blades, one dart
        # loosed in front of it
        F = 1 if (phase == 1 and view == "front") else 0
        stride = 1 if (phase == 1 and view == "side") else 0
        _bwing(p, bez3((34, 37), (33, 28), (29.5, 19), (24, 12.5 - F)), 8.5, 3.6,
               (((24.5, 12.5 - F), -96, 10.5), ((24.5, 14 - F), -121, 14), ((26, 17.5 - F), -146, 12.5), ((28, 21), -168, 8.5)),
               [(35.5, 37), (31.5, 26), (29, 20)] + _scallop((29, 20), (37.5, 23.5), 2, 1.2) + _scallop((37.5, 23.5), (39, 34), 2, 1.2),
               100, bright=False)
        for i, (a, b2) in enumerate((((47, 45), (60, 51)), ((46, 47), (56, 56)), ((48, 43), (61, 44.5)))):
            blade(p, a, b2, 3.4, b_plume, 2, 1, bend=-1.0, fat=0.45, group=30 + i)
        p.limb([(43, 47), (47, 52)], 6.4, 4.4, b_plume, bias=0.25, group=20)
        p.limb([(47, 52), (48.5 - 3 * stride, 55), (50 - 4 * stride, 58.5)], 2.8, 2.4, b_leg, group=21)
        _bfoot(p, 50 - 4 * stride, 59, (8, 35, 155), far=True)
        p.blob(39.5, 43, 10.5, 7.4, b_plume, ang=-12, group=1)
        p.blob(32, 41.5, 7.6, 7.6, b_plume, group=1)
        p.limb([(35, 46.5), (31, 52)], 6.8, 4.6, b_plume, group=22)
        p.limb([(31, 52), (28.5 + 3 * stride, 55), (26 + 4 * stride, 58.5)], 2.8, 2.4, b_leg, group=23)
        _bfoot(p, 26 + 4 * stride, 59, (2, 28, 160))
        p.limb(bez3((31.5, 41.5), (23.5, 40), (26.5, 34 + F), (20, 31 + F)), 9.4, 6.4, b_plume, group=2)
        for i, (b, t) in enumerate((((21, 26.5 + F), (28.5, 24)), ((22, 28 + F), (29.5, 27.5)), ((20, 26 + F), (26, 21.5)))):
            blade(p, b, t, 3.0, b_bronze, 3, 1, bend=-0.5, fat=0.22, group=50 + i)
        p.poly(bez3((12, 29 + F), (13, 25.8 + F), (18, 24.8 + F), (22, 26.4 + F)) +
               bez3((22, 26.4 + F), (25, 28.4 + F), (23.5, 33.4 + F), (19, 33.9 + F)) +
               bez((19, 33.9 + F), (14.5, 34.2 + F), (12, 32.9 + F), n=6), b_plume, group=3)
        p.blob(18.5, 25.4 + F, 2.6, 1.3, b_red, group=4)
        # the spearhead beak: lit culmen above, dark bronze below the gape
        p.poly([(13, 27.8 + F), (8, 29 + F), (4, 31 + F), (0.8, 33.6 + F), (13, 31 + F)], b_metal, flat=1, group=5)
        p.poly([(13, 31 + F), (0.8, 33.6 + F), (3.5, 34.3 + F), (8, 33.9 + F), (13, 33 + F)], b_bronze, flat=1, group=6)
        _bwing(p, bez3((38.5, 39), (38, 30), (40, 21), (44.5, 13.5 - F)), 9.4, 4.2,
               (((44.5, 14 - F), -66 - 2 * F, 13.5 - 2 * F), ((44, 17 - F), -48 - 2 * F, 19), ((43.5, 20.5), -30 - F, 15.5),
                ((43, 24), -13, 18.5), ((42.5, 27.5), 4, 15), ((42, 31), 20, 11)),
               [(39.5, 38), (40, 28), (43, 23)] + _scallop((43, 23), (49, 30), 2, 1.4) + _scallop((49, 30), (45, 40.5), 2, 1.4),
               120)
        _flying_dart(p, (21 - 2 * F, 46 + F), (5 - 2 * F, 51 + F), 90)
        if p.big:
            p.patch(14, 27 + F, ["11111", "1f1f1", "1eee1", ".111."], {"1": "ink", "f": "red1", "e": "red0"})
        else:
            p.px(15, 28 + F, "red1")
        return

    if view == "back":
        # over the shoulder (the hand-finished art replaces this): both wings
        # raised, their darts bristling like a full quiver, the neck curving
        # up to a raptor head in right profile
        _bwing(p, bez3((44, 52), (52, 43), (57, 31), (57, 17)), 9.0, 4.0,
               (((57, 17.5), -90, 13), ((56.2, 21), -108, 15.5), ((55.4, 25), -126, 14), ((54.5, 29), -144, 10)),
               [(43, 50), (49, 38), (54, 30)] + _scallop((54, 30), (48, 36), 2, 1.3) + _scallop((48, 36), (44, 46), 2, 1.3),
               100, bright=False)
        _bwing(p, bez3((24, 54), (12, 49), (6.5, 38), (9.5, 22.5)), 11, 5.0,
               (((9.5, 23), -100, 16), ((10, 26), -82, 20.5), ((11, 29.5), -64, 22.5), ((12.5, 33), -47, 20.5),
                ((14.5, 36.5), -30, 17), ((17, 40), -14, 12)),
               [(22, 53), (13, 44), (12, 33), (15, 36)] + _scallop((15, 36), (24, 42), 2, 1.5) + _scallop((24, 42), (32, 48), 2, 1.5),
               120)
        p.blob(31, 68, 29.5, 21, b_plume, group=1)
        p.limb(bez3((42, 62), (52, 51), (37, 44), (43, 34)), 12.5, 7, b_plume, group=2)
        p.poly(bez3((53.5, 29.5), (52.5, 24.5), (45.5, 22.6), (40, 25)) + bez3((40, 25), (36.5, 28), (37.5, 34.5), (43, 35.2)) +
               bez((43, 35.2), (49.5, 35.6), (53.5, 34), n=6), b_plume, group=3)
        p.poly([(52.5, 26.2), (56.5, 27.8), (59.8, 30.8), (61.4, 34.4), (59.8, 35.3), (56, 35.2), (52.5, 34)], b_metal, flat=1, group=5)
        p.patch(45, 26, ["2111111", ".1f161.", ".1eee12", "..111.."],
                {"1": "ink", "2": "pl0", "f": "red1", "e": "red0", "6": "white"})
        return

    if view in ("down", "up"):
        # follower: stalking on long legs, both wings mantled with their darts
        step = phase
        for x, sd in ((28.5, step), (35.5, 1 - step)):
            p.limb([(x, 46), (x, 59 - 2 * sd)], 2.8, 2.4, b_leg, group=12)
            p.limb([(x, 59.5 - 2 * sd), (x - 2.5, 61 - 2 * sd)], 1.8, 1.4, b_leg, group=12)
            p.limb([(x, 59.5 - 2 * sd), (x + 2.5, 61 - 2 * sd)], 1.8, 1.4, b_leg, group=12)
        for sx in (-1, 1):
            def X(x, sx=sx):
                return 32 + sx * (x - 32)
            for i, (b, ang, L) in enumerate((((X(50), 22), -90 + sx * 12, 12), ((X(51), 24), -90 + sx * 38, 14),
                                             ((X(51.5), 26.5), -90 + sx * 64, 11.5))):
                _sdart(p, b, _polar(b, ang, L), 4.0, 40 + i + (10 if sx > 0 else 0), bright=i != 1)
            p.poly([(X(36), 42), (X(38), 33), (X(46), 27)] + _scallop((X(46), 27), (X(47), 36), 2, 1.2), b_plume, bias=0.15,
                   group=24 + sx)
            p.limb(bez3((X(35), 38), (X(40), 32), (X(46), 27), (X(51), 23)), 7.6, 3.6, b_plume, group=20 + sx)
        p.blob(32, 40, 9, 9, b_plume, group=1)
        if view == "up":
            for i, (a, b2) in enumerate((((30, 46), (26, 55)), ((34, 46), (38, 55)))):
                blade(p, a, b2, 4, b_plume, 2, 1, fat=0.45, group=30 + i)
        p.limb([(32, 34), (32, 25)], 7, 5.6, b_plume, group=2)
        p.blob(32, 21, 6.2, 5, b_plume, group=3)
        for i, (b, t) in enumerate((((30.5, 18), (26, 12)), ((33.5, 18), (38, 12)))):
            blade(p, b, t, 2.8, b_bronze, 3, 1, fat=0.22, group=50 + i)
        p.blob(32, 16.8, 3, 1.4, b_red, group=4)
        if view == "down":
            p.poly([(30, 23), (34, 23), (32, 33.5)], b_metal, flat=1, group=5)
            p.eye(28, 20, 2, 2, iris="red1", shine=None)
            p.eye(34, 20, 2, 2, iris="red1", shine=None)
        return


MONS = [
    Mon("Chalkip", CHALKIP_COLORS, CHALKIP_SHINY, chalkip, foot="bird"),
    Mon("Belornis", BELORNIS_COLORS, BELORNIS_SHINY, belornis, foot="bird"),
]
