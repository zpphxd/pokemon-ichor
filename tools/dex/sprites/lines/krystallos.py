"""Krystallos line: Pagoshard, Krystolos (Ice, then Ice/Rock). Krystallos is
the Greek word for ice: rock crystal was thought to be ice frozen so hard,
high in the coldest peaks, that it could never thaw (Pliny 37.9).

The code drafts below give the icons and follower frames. The battle sprites
are hand-finished in tools/dex/sprites/art/. Krystolos's were cut like a gem:
its living, hunched silhouette (round hump, shoulders, fists) was split into
flat crystal facets, each toned by which way its plane faces the light, so
the body reads as clear crystal without turning boxy; the spires, the face,
the frosted core and the glints were then laid by hand."""
import math

from mon_lib import C, Mat, Mon, bez3

INK = C.ink


def _at(cx, cy, r, ang, sx=1.0):
    a = math.radians(ang)
    return (cx + sx * r * math.cos(a), cy - r * math.sin(a))


def _hexagon(cx, cy, r, ang=90.0, sx=1.0, sy=1.0):
    return [(cx + sx * r * math.cos(math.radians(ang + 60 * i)), cy - sy * r * math.sin(math.radians(ang + 60 * i)))
            for i in range(6)]


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _crystal(p, base, tip, w, mat, tones=(3, 2, 1), ridge=0.42, group=None, bias=0.0, cap=0.34, clip=None):
    """A hexagonal crystal point from base to tip, seen in 3/4: a lit face,
    a front face and a shaded face running up the prism, meeting at a
    pyramidal tip. tones are flat ramp levels (lit, front, shade)."""
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    nx, ny = -uy, ux                       # left of the base->tip direction
    h = w / 2
    shoulder = _lerp(base, tip, 1 - cap)
    left = [(base[0] + nx * h, base[1] + ny * h), (shoulder[0] + nx * h, shoulder[1] + ny * h)]
    right = [(shoulder[0] - nx * h, shoulder[1] - ny * h), (base[0] - nx * h, base[1] - ny * h)]
    pts = left + [tip] + right
    kw = {"group": group, "bias": bias}
    if clip is not None:
        kw["clip"] = clip
    pid = p.poly(pts, mat, flat=tones[1], **kw)
    if not pid or not p.big:
        return pid
    # which side faces the upper-left light
    lit_left = (nx * -0.6 + ny * -0.8) > 0
    a = ridge if lit_left else 1 - ridge
    # the two ridges running up the prism into the tip
    r1b = (base[0] + nx * h * (1 - 2 * a * 0.6), base[1] + ny * h * (1 - 2 * a * 0.6))
    r2b = (base[0] - nx * h * (1 - 2 * (1 - a) * 0.6), base[1] - ny * h * (1 - 2 * (1 - a) * 0.6))
    r1s = (r1b[0] + ux * d * (1 - cap), r1b[1] + uy * d * (1 - cap))
    r2s = (r2b[0] + ux * d * (1 - cap), r2b[1] + uy * d * (1 - cap))
    litface = [left[0], left[1], tip, r1s, r1b] if lit_left else [right[1], right[0], tip, r2s, r2b]
    shadeface = [right[1], right[0], tip, r2s, r2b] if lit_left else [left[0], left[1], tip, r1s, r1b]
    p.poly(litface, mat, clip=[pid], flat=tones[0], noline=True)
    p.poly(shadeface, mat, clip=[pid], flat=tones[2], noline=True)
    return pid


# --------------------------------------------------------------------------
# Pagoshard, the ice shard
# --------------------------------------------------------------------------

PAGOSHARD_COLORS = [
    ("ink", INK),
    # ice: darker Aegean-blue facet edges up to marble white
    ("ice0", (40, 72, 152)), ("ice1", (88, 144, 216)), ("ice2", (152, 208, 248)), ("ice3", (208, 232, 248)),
    ("white", (248, 248, 248)),
    # the quartz heart, lilac where the ice is thickest
    ("violet", (96, 88, 176)), ("quartz", (168, 160, 232)), ("qlight", (224, 216, 248)),
    # the limestone-gray rock it grows from
    ("rock0", (80, 72, 72)), ("rock1", (120, 112, 104)), ("rock2", (160, 152, 136)), ("rock3", (200, 192, 176)),
]
PAGOSHARD_SHINY = {
    # smoky sun-gold quartz, like citrine
    "ice0": (120, 72, 24), "ice1": (184, 120, 40), "ice2": (232, 176, 72), "ice3": (248, 224, 152),
    "white": (248, 248, 224),
    "violet": (104, 64, 48), "quartz": (168, 112, 72), "qlight": (224, 184, 128),
}

p_ice = Mat(["ice0", "ice1", "ice2", "ice3", "white"], line="ice0", cuts=[0.14, 0.34, 0.58, 0.8])
p_quartz = Mat(["violet", "quartz", "qlight"], line="violet", cuts=[0.36, 0.66])
p_rock = Mat(["rock0", "rock1", "rock2", "rock3"], line="rock0", cuts=[0.3, 0.52, 0.74])


def pagoshard(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        T = 2 * phase if view == "front" else 0     # the tip bends forward

        # a crystal jutting from its back, behind the body
        _crystal(p, (36, 42), (45.5, 29.5 - L), 7.0, p_ice, tones=(3, 2, 1), group=20, bias=0.1, cap=0.42)
        _crystal(p, (33.6, 33), (38.6, 24.6 - L), 4.6, p_ice, tones=(4, 3, 1), group=21, cap=0.45)
        # the rock it grows from: rounded limestone, two stubby feet
        p.blob(32, 54.6, 11, 4.4, p_rock, group=1)
        p.blob(24.8, 58.2, 4.8, 3.0, p_rock, group=2)
        p.blob(38.4, 58.4, 4.6, 2.8, p_rock, group=3, bias=0.12)
        p.blob(44.6, 55.2, 3.2, 2.6, p_rock, group=4, bias=0.2)

        # the shard: a round crystal belly rising into a jagged point that
        # curls forward like a hood
        tip = (21.6 - T, 22 - L + T * 0.4)
        body = (bez3((21.6, 54), (15.4, 48), (16.4, 38.6), (21.6, 34)) +
                bez3((21.6, 34), (23.6, 31.6), (23, 26.4), tip) +
                bez3(tip, (29, 23.2), (35, 28), (38.4, 34.4)) +
                bez3((38.4, 34.4), (45, 40), (45.4, 49.4), (41.4, 54.2)))
        bid = p.poly(body, p_ice, group=10, flat=2)
        if p.big:
            # curved facets: the lit left plane, the front, the shaded right
            lit = bez3((14, 56), (12, 44), (18, 34), tip) + bez3(tip, (24.4, 31), (21.6, 42), (24, 56))
            shade = bez3((36.4, 56), (38.6, 44), (35, 33), tip) + bez3(tip, (34, 24), (47, 36), (47, 56))
            p.poly(lit, p_ice, clip=[bid], flat=3, noline=True)
            p.poly(shade, p_ice, clip=[bid], flat=1, noline=True)
            p.stroke(bez3(tip, (24.4, 31), (21.6, 42), (24, 53)), "ice2")
            p.stroke(bez3(tip, (33, 25), (38.6, 37), (36.4, 53)), "ice0")
        # the quartz heart, a hexagon showing through the ice
        p.poly(_hexagon(29.4, 35.4 - L, 3.6, 90, 0.92), p_quartz, group=12)
        if p.big:
            p.pxs([(28, 33 - L), (29, 33 - L)], "qlight")
            p.px(29, 34 - L, "white")
        # frost crystals studding its sides
        _crystal(p, (20.4, 46.4), (14.6, 42.2), 3.8, p_ice, tones=(3, 2, 1), group=30)
        _crystal(p, (21.6, 51.6), (16.6, 51.2), 3.0, p_ice, tones=(3, 2, 1), group=31)
        _crystal(p, (42.2, 47.6), (47, 44.4), 3.4, p_ice, tones=(2, 1, 0), group=32)

        if p.big:
            # two small square eyes set in the front facets, a small mouth
            p.patch(23, 40 - L, ["1111...1111", "1w11...1w11", "1111...1111", "1111...1111"], {"1": "ink", "w": "white"})
            p.stroke([(28, 46 - L), (30, 46 - L)], "ice0")
        else:
            p.pxs([(26, 42), (31, 42)], "ink")
        return

    if view == "back":
        # over the shoulder at about 1.3x, cropped by the frame: the back
        # crystal jutting toward us and catching the light, the hooded tip
        # curling forward to the right, one square eye in profile
        k = 0.78

        def S(x, y):
            return (32 + (x - 32) * k, 66 + (y - 66) * k)

        def SS(pts):
            return [S(x, y) for x, y in pts]
        _crystal(p, S(26, 44), S(8, 26), 10 * k, p_ice, tones=(4, 3, 1), group=20, cap=0.42)
        _crystal(p, S(30, 34), S(24, 20), 6.4 * k, p_ice, tones=(4, 3, 2), group=21, cap=0.45)
        tip = S(46, 13)
        body = SS(bez3((16, 66), (10, 54), (12, 42), (22, 34)) + bez3((22, 34), (30, 26), (37, 18), (46, 13)) +
                  bez3((46, 13), (47.6, 20), (46, 25), (48, 30)) + bez3((48, 30), (56, 38), (58, 50), (55, 66)))
        bid = p.poly(body, p_ice, group=10, flat=2)
        if p.big:
            lit = SS(bez3((8, 68), (6, 48), (18, 30), (46, 13)) + bez3((46, 13), (36, 30), (30, 46), (33, 68)))
            shade = SS(bez3((47, 68), (50, 50), (47, 36), (46, 13)) + bez3((46, 13), (52, 26), (62, 40), (62, 68)))
            p.poly(lit, p_ice, clip=[bid], flat=3, noline=True)
            p.poly(shade, p_ice, clip=[bid], flat=1, noline=True)
            p.stroke(SS(bez3((46, 13), (36, 30), (30, 46), (33, 64))), "ice2")
            p.stroke(SS(bez3((46, 13), (46, 30), (50, 48), (47, 64))), "ice0")
        # the quartz heart, seen through the ice
        p.poly(_hexagon(*S(38.6, 33), 4.6 * k, 90, 0.92), p_quartz, group=12)
        # frost crystals studding its flanks
        _crystal(p, S(54, 46), S(61, 41.6), 4.4 * k, p_ice, tones=(2, 1, 0), group=30)
        _crystal(p, S(13, 52), S(5, 50), 4.0 * k, p_ice, tones=(3, 2, 1), group=31)
        _crystal(p, S(15, 60), S(8, 60), 3.6 * k, p_ice, tones=(3, 2, 1), group=32)
        if p.big:
            qx, qy = S(38.6, 33)
            p.pxs([(qx - 1.5, qy - 2), (qx - 0.5, qy - 2)], "qlight")
            p.px(qx - 1.5, qy - 1, "white")
            ex, ey = S(49.6, 37)
            p.patch(int(ex), int(ey), ["1111", "1w11", "1111", "1111"], {"1": "ink", "w": "white"})
        return

    if view in ("down", "up"):
        # follower: waddling on its stubby rock feet, the round crystal
        # belly rising to its point, frost crystals at its sides
        step = phase
        p.blob(32, 55.6, 10.6, 4.2, p_rock, group=1)
        p.blob(26.6, 58.6 - step, 4.4, 2.8, p_rock, group=2)
        p.blob(37.4, 58.6 - (1 - step), 4.4, 2.8, p_rock, group=3)
        if view == "up":
            _crystal(p, (32, 40), (32, 25), 7.4, p_ice, tones=(4, 3, 1), group=20, cap=0.42)
        body = (bez3((24, 54.4), (18.6, 48), (19, 38), (25, 31)) + bez3((25, 31), (28.4, 27), (30.6, 24), (32, 20)) +
                bez3((32, 20), (33.4, 24), (35.6, 27), (39, 31)) + bez3((39, 31), (45, 38), (45.4, 48), (40, 54.4)))
        bid = p.poly(body, p_ice, group=10, flat=2)
        if p.big:
            p.poly(bez3((16, 56), (15, 44), (22, 32), (32, 20)) + bez3((32, 20), (28, 32), (26, 44), (27, 56)), p_ice,
                   clip=[bid], flat=3, noline=True)
            p.poly(bez3((37, 56), (38, 44), (36, 32), (32, 20)) + bez3((32, 20), (42, 32), (49, 44), (48, 56)), p_ice,
                   clip=[bid], flat=1, noline=True)
        _crystal(p, (20.4, 46), (14.4, 42), 3.8, p_ice, tones=(3, 2, 1), group=30)
        _crystal(p, (43.6, 46), (49.6, 42), 3.8, p_ice, tones=(2, 1, 0), group=31)
        if view == "down":
            p.poly(_hexagon(32, 34, 3.4, 90, 0.92), p_quartz, group=12)
            p.patch(26, 40, ["1111..1111", "1w11..1w11", "1111..1111", "1111..1111"], {"1": "ink", "w": "white"},
                    small=(27, 41, ["11..11"]))
        return


# --------------------------------------------------------------------------
# Krystolos, everlasting ice
# --------------------------------------------------------------------------

KRYSTOLOS_COLORS = [
    ("ink", INK),
    # clear crystal: darker Aegean-blue edges up to marble-white glints
    ("ice0", (32, 56, 128)), ("ice1", (64, 104, 184)), ("ice2", (104, 160, 224)), ("ice3", (160, 208, 240)),
    ("ice4", (216, 240, 248)), ("white", (248, 248, 248)),
    # lilac in the deepest crystal, where the ice is thickest
    ("violet0", (64, 56, 136)), ("violet1", (120, 112, 200)),
    # cold eyes and the glow round the frosted core
    ("glow", (168, 248, 248)),
    # the limestone-gray rock at its feet
    ("rock0", (72, 64, 64)), ("rock1", (112, 104, 96)), ("rock2", (152, 144, 128)), ("rock3", (192, 184, 168)),
]
KRYSTOLOS_SHINY = {
    # smoky sun-gold citrine
    "ice0": (104, 56, 24), "ice1": (160, 96, 32), "ice2": (208, 144, 56), "ice3": (240, 192, 104),
    "ice4": (248, 232, 168), "white": (248, 248, 224),
    "violet0": (88, 48, 40), "violet1": (144, 88, 64),
    "glow": (248, 240, 168),
}

k_ice = Mat(["ice0", "ice1", "ice2", "ice3", "ice4"], line="ice0", cuts=[0.14, 0.34, 0.56, 0.78])
k_deep = Mat(["violet0", "violet1", "ice2"], line="violet0", cuts=[0.34, 0.66])
k_rock = Mat(["rock0", "rock1", "rock2", "rock3"], line="rock0", cuts=[0.18, 0.44, 0.72])
k_core = Mat(["ice3", "ice4", "white"], line="ice2", cuts=[0.4, 0.7])
k_body = Mat(["ice1", "ice2", "ice3", "ice4"], line="ice0", cuts=[0.22, 0.46, 0.7])


def _column(p, a, b, w, mat=k_ice, tones=(3, 2, 1), group=None, bias=0.0):
    """A thick hexagonal crystal column from a to b (an arm or leg), seen
    in 3/4: lit face, front face and shaded face in long flat strips, with
    the hexagonal end facet at b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    nx, ny = -uy, ux
    h = w / 2
    pts = [(a[0] + nx * h, a[1] + ny * h), (b[0] + nx * h, b[1] + ny * h),
           (b[0] - nx * h, b[1] - ny * h), (a[0] - nx * h, a[1] - ny * h)]
    pid = p.poly(pts, mat, flat=tones[1], group=group, bias=bias)
    if not pid or not p.big:
        return pid
    lit_left = (nx * -0.6 + ny * -0.8) > 0
    s1, s2 = (0.62, 0.25) if lit_left else (-0.25, -0.62)

    def strip(o0, o1):
        return [(a[0] + nx * h * o0, a[1] + ny * h * o0), (b[0] + nx * h * o0, b[1] + ny * h * o0),
                (b[0] + nx * h * o1, b[1] + ny * h * o1), (a[0] + nx * h * o1, a[1] + ny * h * o1)]
    if lit_left:
        p.poly(strip(1.2, 0.3), mat, clip=[pid], flat=tones[0], noline=True)
        p.poly(strip(-0.42, -1.2), mat, clip=[pid], flat=tones[2], noline=True)
    else:
        p.poly(strip(-1.2, -0.3), mat, clip=[pid], flat=tones[0], noline=True)
        p.poly(strip(0.42, 1.2), mat, clip=[pid], flat=tones[2], noline=True)
    return pid


def krystolos(p, view, phase):
    if view in ("front", "side", "icon"):
        # Regigigas-heavy: the head sunk low between crystal shoulders, both
        # massive fists planted on the ground, a ridge of spires down the
        # hump of its back, the frosted core shining in its chest. The
        # hand-finished art cuts every mass into crystal facets.
        L = 1 if (phase == 1 and view == "front") else 0     # shoulders heave up
        H = 2 * phase if view == "front" else 0              # the head lifts

        spires = (((54, 31), (62.2, 21), 5.6, (3, 2, 1)), ((50, 25), (58.4, 10.4), 7.6, (3, 2, 1)),
                  ((39.4, 22), (39.4, 5.6), 7.6, (4, 3, 2)), ((44.6, 21), (48.6, 1.6), 10, (4, 3, 2)))
        if not p.big:
            spires = spires[1:]        # fewer, bolder spires at icon size
        for base, tip, w, tones in spires:
            _crystal(p, (base[0], base[1] - L), (tip[0], tip[1] - L), w, k_ice, tones=tones, group=60, cap=0.4)
        p.blob(36, 37 - L, 15.4, 13, k_body, group=1)
        p.blob(44, 27.6 - L, 11.4, 9, k_body, group=1)
        p.limb([(39.6, 45), (40, 56)], 11.6, 11.6, k_body, group=1, bias=0.15)
        p.limb([(28.6, 45), (28.2, 56)], 11.6, 11.6, k_body, group=1, bias=0.1)
        p.poly([(19, 62), (19.6, 58.4), (23, 55.6), (28, 54.6), (33, 55.4), (38, 54), (44, 54.6), (47, 57), (48, 62)],
               k_rock, group=30)
        # the far shoulder's crystals, the far arm and fist (screen left)
        if p.big:
            _crystal(p, (13, 25.6 - L), (5.4, 14.6 - L), 5.6, k_ice, tones=(4, 3, 2), group=41, cap=0.42)
            _crystal(p, (17, 23 - L), (12.6, 11.6 - L), 4.4, k_ice, tones=(4, 3, 2), group=42, cap=0.42)
        p.blob(15, 28.6 - L, 7.6, 6.8, k_body, group=10)
        p.limb([(14, 31 - L), (11.4, 42), (10.4, 49)], 12, 13.4, k_body, group=10)
        p.blob(10, 53.6, 9, 6.8, k_body, group=11)
        # the head, low between the shoulders, and its crest
        p.blob(22.4, 23.6 - H, 8.2, 7.0, k_body, group=50)
        p.blob(19, 27.4 - H, 5.6, 3.8, k_body, ang=-10, group=50)
        _crystal(p, (25.4, 18.4 - H), (19.4, 4.6 - H), 6.4, k_ice, tones=(4, 3, 2), group=51, cap=0.5)
        # the near arm and fist (screen right), in front of the flank
        p.blob(46.6, 32 - L, 8, 7, k_body, group=20)
        p.limb([(47, 35 - L), (50.6, 44), (51.6, 49)], 12.4, 13.6, k_body, group=20)
        p.blob(52.4, 54, 9, 6.8, k_body, group=21)
        # the frosted core
        p.poly(_hexagon(30, 37 - L, 5.0, 90, 0.86), k_deep, group=8, flat=0, noline=True)
        p.poly(_hexagon(30, 37 - L, 3.6, 90, 0.86), k_core, group=9, noline=True)
        if p.big:
            p.patch(15, 21 - H, ["11111.1111", "1aa11.1aa1", ".111...11"], {"1": "ink", "a": "glow"})
        else:
            p.pxs([(17, 22), (22, 22)], "ink")
        return

    if view == "back":
        krystolos_back(p)
        return

    if view in ("down", "up"):
        # follower: knuckle-walking toward or away from the camera, the
        # fists swinging in turn
        st = phase
        for k, x in enumerate((24, 40)):
            _crystal(p, (x, 22), (x + (-6 if k == 0 else 6), 6), 7.4, k_ice, tones=(4, 3, 2), group=60 + k, cap=0.4)
        _crystal(p, (32, 20), (32, 2), 8.6, k_ice, tones=(4, 3, 2), group=62, cap=0.36)
        p.poly([(18, 62), (20, 56.6), (44, 56.6), (46, 62)], k_rock, group=30)
        _column(p, (27, 46), (27, 57), 9, tones=(4, 3, 2), group=31)
        _column(p, (37, 46), (37, 57), 9, tones=(3, 2, 1), group=32)
        p.blob(32, 37, 14, 12, k_body, group=1)
        if view == "down":
            p.poly(_hexagon(32, 39, 5, 90), k_deep, group=8, flat=1, noline=True)
            p.poly(_hexagon(32, 39, 3.4, 90), k_core, group=9, noline=True)
        for k, (sx, fy) in enumerate(((-1, 56 - 2 * st), (1, 56 - 2 * (1 - st)))):
            X = lambda x: 32 + sx * (x - 32)
            _column(p, (X(19), 30), (X(13), 48), 10, tones=(4, 3, 2) if sx < 0 else (3, 2, 1), group=10 + k)
            p.poly(_hexagon(X(12.6), fy, 7, 0, 1.0, 0.8), k_ice, group=12 + k, flat=3 if sx < 0 else 2)
        if view == "down":
            p.poly([(24, 22), (26, 16), (32, 14), (38, 16), (40, 22), (38, 29), (32, 31), (26, 29)], k_body, group=50)
            p.patch(25, 21, ["11111111111111", ".1gg111111gg1.", "..11......11"], {"1": "ink", "g": "glow"},
                    small=(26, 21, ["1g1..1g1"]))
        else:
            p.blob(32, 26, 9, 7, k_body, group=50)
        return

def krystolos_back(p):
    """Battle back, over the shoulder at about 1.2x: the hump of its back
    and the cluster of crystal spires catching the light, the faceted head
    turned right in profile, the near arm a column cropped by the frame."""
    # spires rising up and back from the hump
    _crystal(p, (14, 40), (3, 20), 8.6, k_ice, tones=(3, 2, 1), group=60, cap=0.4)
    _crystal(p, (22, 36), (13, 6), 11, k_ice, tones=(4, 3, 1), group=61, cap=0.36)
    _crystal(p, (31, 34), (29.6, 3), 11.6, k_ice, tones=(4, 3, 1), group=62, cap=0.34)
    _crystal(p, (38, 36), (43, 15), 8.4, k_ice, tones=(3, 2, 1), group=63, cap=0.4)
    _crystal(p, (26, 40), (22, 22), 6.6, k_ice, tones=(4, 3, 2), group=64, cap=0.45)
    # the back: a broad hunched mass, cropped
    bid = p.poly(bez3((0, 64), (0, 46), (10, 36), (24, 34)) + bez3((24, 34), (38, 32), (50, 36), (56, 46)) +
                 [(60, 54), (62, 64)], k_ice, group=1)
    if p.big:
        p.poly([(0, 44), (10, 36), (24, 34), (38, 33), (46, 36), (34, 41), (20, 42), (8, 47)], k_ice, clip=[bid],
               flat=3, noline=True, group=1)
        p.poly([(40, 44), (50, 38), (60, 48), (64, 64), (44, 64)], k_ice, clip=[bid], flat=1, noline=True, group=1)
        p.stroke([(8, 47), (20, 42), (34, 41), (46, 36)], "ice4")
        p.stroke([(30, 41), (32, 52), (30, 63)], "ice3")
        p.stroke([(34, 41), (40, 44), (44, 63)], "ice1")
    # the far shoulder and the head in profile, low and forward
    p.blob(48, 41, 9.6, 8.6, k_ice, group=40)
    _crystal(p, (46, 36), (51, 25), 6, k_ice, tones=(4, 3, 1), group=41, cap=0.45)
    hid = p.blob(54.6, 37, 7.4, 7, k_ice, group=50)
    p.blob(58.4, 41.4, 4, 2.8, k_ice, group=50)
    if p.big:
        p.poly([(49, 32), (56, 29.6), (62, 32.6), (58, 35), (51, 35.6)], k_ice, clip=[hid], flat=4, noline=True,
               group=50)
        p.patch(55, 35, ["111111", "11gg1", ".11"], {"1": "ink", "g": "glow"})
    # the near arm, a column down out of frame
    _column(p, (10, 44), (6, 64), 13, tones=(3, 2, 1), group=10)
    if p.big:
        for x, y in ((12, 10), (28, 7), (5, 24), (40, 19), (22, 25)):
            p.px(x, y, "white")


# footprints: the six-sided cross-section of a crystal column
PAGOSHARD_FOOT = ["................", "................", "................", "................",
                  "................", "......####......", ".....######.....", "....###..###....",
                  "....###..###....", ".....######.....", "......####......", "................",
                  "................", "................", "................", "................"]
KRYSTOLOS_FOOT = ["................", "................", ".....######.....", "....########....",
                  "...###....###...", "..###......###..", ".###...##...###.", ".###..####..###.",
                  ".###..####..###.", ".###...##...###.", "..###......###..", "...###....###...",
                  "....########....", ".....######.....", "................", "................"]

MONS = [
    # icon palette 4 keeps the ice blue
    Mon("Pagoshard", PAGOSHARD_COLORS, PAGOSHARD_SHINY, pagoshard, foot=PAGOSHARD_FOOT, icon_pal=4),
    Mon("Krystolos", KRYSTOLOS_COLORS, KRYSTOLOS_SHINY, krystolos, foot=KRYSTOLOS_FOOT, icon_pal=4),
]
