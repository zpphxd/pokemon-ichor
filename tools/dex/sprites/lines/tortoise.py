"""Tortoise line: Chelonet, Chelyra (Ground, then Ground / Fairy). Hermes' lyre.

On the day he was born, Hermes found a mountain tortoise at the mouth of his
cave on Kyllene, hollowed its shell and strung it with seven strings: the
first lyre. That night he stole Apollo's cattle, and paid for them with the
lyre's song (Homeric Hymn to Hermes). Chelonet is the hatchling whose hollow
shell hums in the wind; Chelyra's shell has become the instrument, two horns
rising from its front rim with a crossbar and seven strings.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts, ribbon

INK = C.ink


def _note(p, x, y, color="ink"):
    """A small eighth note, head at the bottom-left (x, y)."""
    p.pxs([(x, y), (x + 1, y), (x, y - 1), (x + 1, y - 1)], color)
    p.pxs([(x + 1, y - 2), (x + 1, y - 3), (x + 1, y - 4), (x + 2, y - 4), (x + 3, y - 3)], color)


# --------------------------------------------------------------------------
# Chelonet, the humming hatchling
# --------------------------------------------------------------------------

CHELONET_COLORS = [
    ("ink", INK),
    # a smooth terracotta dome, like an unglazed pot
    ("t0", (120, 48, 32)), ("t1", (176, 88, 48)), ("t2", (216, 128, 80)), ("t3", (240, 176, 120)),
    # limestone rim and sound-hole ring
    ("l0", (168, 136, 88)), ("l1", (208, 184, 136)), ("l2", (240, 224, 184)),
    # olive skin
    ("o0", (56, 72, 32)), ("o1", (96, 120, 48)), ("o2", (144, 168, 72)), ("o3", (192, 200, 120)),
    # marble belly plate
    ("m0", (160, 152, 144)), ("m1", (216, 208, 192)), ("white", C.white),
]
CHELONET_SHINY = {
    # the shell turns pale marble with sun-gold rims
    "t0": (136, 128, 128), "t1": (184, 176, 168), "t2": (216, 208, 200), "t3": (240, 240, 232),
    "l0": (184, 120, 32), "l1": (232, 168, 48), "l2": (248, 216, 104),
}

n_shell = Mat(["t0", "t1", "t2", "t3"], line="t0", cuts=[0.2, 0.46, 0.72])
n_rim = Mat(["l0", "l1", "l2"], line="l0", cuts=[0.4, 0.68])
n_skin = Mat(["o0", "o1", "o2", "o3"], line="o0", cuts=[0.2, 0.5, 0.82])
n_mouth = Mat(["t0", "t1"], line="t0", cuts=[0.6])
n_belly = Mat(["m0", "m1", "white"], line="m0", cuts=[0.42, 0.7])
n_nub = Mat(["m0", "m1", "white"], line="m0", cuts=[0.4, 0.66])

# a tortoise's print: a round pad with four blunt nails
TORTOISE_FOOT = [
    "", "", "",
    "....#.#.#.#.....",
    "....#.#.#.#.....",
    "...#########....",
    "..###########...",
    "..###########...",
    "..###########...",
    "...#########....",
    "....#######.....",
]
TORTOISE_FOOT = [r.ljust(16, ".") for r in TORTOISE_FOOT] + ["." * 16] * (16 - len(TORTOISE_FOOT))


def _soundhole(p, cx, cy, r):
    """The round sound-hole on the shell's flank: a limestone ring with the
    dark hollow inside."""
    ring = p.blob(cx, cy, r + 1.2, r + 1.0, n_rim, ang=-10)
    p.blob(cx + 0.2, cy + 0.2, r, r * 0.9, Mat(["t0"]), ang=-10, clip=[ring], noline=True)


def chelonet(p, view, phase):
    if view in ("front", "side", "icon"):
        hum = 1 if (phase == 1 and view == "front") else 0
        step = view == "side" and phase == 1
        H = hum
        # far legs, behind the shell
        p.limb([(33, 55), (33.5, 59.5)], 4.6, 4.2, n_skin, bias=0.3, group=10)
        p.limb([(47, 54.5), (48, 59.2)], 4.2, 3.8, n_skin, bias=0.35, group=11)
        # tail
        p.taper([(47.5, 53), (50.5, 54.4), (52, 55.6)], 2.8, n_skin, bias=0.25, group=11)
        # the shell: a limestone rim under a smooth terracotta dome
        p.blob(39.5, 53, 11.4, 4.2, n_rim, group=2)
        p.blob(39.5, 48.6, 10, 7.6, n_shell, group=1)
        # the hatchling's two nubs on the front rim, where the horns will grow
        p.blob(31.4, 44, 1.4, 1.8, n_nub, ang=-30, group=5)
        p.blob(35.4, 41.4, 1.3, 1.6, n_nub, ang=-10, group=6, bias=0.1)
        _soundhole(p, 41.5, 49.5, 2.4)
        # belly plate showing under the front of the shell
        p.blob(33, 56.8, 4.6, 1.6, n_belly, group=3)
        # near legs, stubby
        p.limb([(29, 55), (27.5, 59.5)] if not step else [(29, 55), (30, 59.5)], 5.4, 5.0, n_skin, group=12)
        p.limb([(44, 55.5), (44.5, 59.5)] if not step else [(44, 55.5), (42.5, 59.5)], 5.2, 4.8, n_skin, group=13)
        # neck stretched up, and the big round head tipped back to hum
        p.limb([(32, 53.5), (29, 49), (26.5, 45 - H)], 6.4, 6.0, n_skin, group=4)
        # the open mouth, behind the beak and jaw
        p.poly([(15.5, 41 - H), (22, 42 - H), (16.5, 45 - H * 0.5)], n_mouth, group=9)
        p.blob(24, 39.6 - H, 7.2, 6.6, n_skin, ang=-8, group=7)
        # upper beak pointing up and out, the lower jaw dropped open
        p.blob(18, 39.6 - H, 3.8, 2.6, n_skin, ang=-22, group=7)
        p.blob(19.4, 44.6 - H * 0.5, 3.6, 1.6, n_skin, ang=10, group=8, bias=0.1)
        if p.big:
            p.eye(21, 35 - H, 4, 5, shine="white", shine_at=(2, 1))
            p.px(16, 38 - H, "o0")                          # nostril
            for x in (25.5, 28.5, 42, 45):
                p.px(x, 59, "l2")                           # nails
            if hum:
                _note(p, 11, 35)
        else:
            p.px(22, 38 - H, "ink")
        return

    if view == "back":
        # over the shoulder, about 1.2x: the dome and its sound-hole cropped
        # by the frame, the neck stretched up and the head turned right,
        # humming
        p.limb([(7, 59), (5, 64)], 7, 7, n_skin, bias=0.15, group=10)      # near hind leg
        p.blob(25, 61.5, 23.5, 6.5, n_rim, group=2)
        p.blob(24.5, 53.5, 21.5, 14.5, n_shell, group=1)
        _soundhole(p, 16.5, 50, 3.2)
        p.blob(36.5, 39.6, 1.8, 2.2, n_nub, ang=20, group=5)
        p.limb(bez((39, 52), (43.5, 44), (44.5, 35)), 10, 8.8, n_skin, group=4)
        p.blob(50.6, 39.6, 1.7, 2.0, n_nub, ang=-20, group=6, bias=0.1)
        p.poly([(52, 28.5), (59.5, 26.5), (56, 32)], n_mouth, group=9)
        p.blob(46.5, 26, 8.2, 7.4, n_skin, ang=8, group=7)
        p.blob(55, 26.6, 4.2, 2.8, n_skin, ang=18, group=7)
        p.blob(53.8, 31.6, 3.8, 1.8, n_skin, ang=-8, group=8, bias=0.1)
        if p.big:
            p.eye(48, 21, 4, 6, shine="white", shine_at=(2, 1))
            p.px(57, 25, "o0")
        return

    if view == "down":
        # follower walking toward the camera: the dome rising behind the
        # big head, the nubs either side of the neck
        step = phase
        p.limb([(21.5, 50), (21, 59 - step)], 5.4, 5, n_skin, group=12)
        p.limb([(42.5, 50), (43, 59 - (1 - step))], 5.4, 5, n_skin, group=13)
        p.blob(32, 47.5, 13.6, 5.4, n_rim, group=2)
        p.blob(32, 43, 12.6, 9.4, n_shell, group=1)
        p.blob(24.6, 40.6, 1.6, 2, n_nub, group=5)
        p.blob(39.4, 40.6, 1.6, 2, n_nub, group=6)
        p.limb([(32, 54), (32, 49)], 6, 6, n_skin, group=4)
        p.blob(32, 47, 7, 6.4, n_skin, group=7)
        p.blob(32, 51.6, 3.6, 2, n_skin, group=7)
        p.eye(27, 45, 3, 4, shine="white", shine_at=(1, 1))
        p.eye(34, 45, 3, 4, shine="white", shine_at=(1, 1))
        p.pxs([(31, 52), (32, 52)], "t0")
        if p.big:
            p.pxs([(31, 50), (33, 50)], "o0")
        return

    if view == "up":
        # follower walking away: the dome from behind with its plates, the
        # head stretched up over the front rim
        step = phase
        p.blob(32, 30, 5.6, 5, n_skin, group=7)
        p.limb([(32, 35), (32, 39)], 5, 5, n_skin, group=7)
        p.blob(25, 36.4, 1.6, 2, n_nub, group=5)
        p.blob(39, 36.4, 1.6, 2, n_nub, group=6)
        p.limb([(23, 51), (22.5, 59 - step)], 5.4, 5, n_skin, group=12)
        p.limb([(41, 51), (41.5, 59 - (1 - step))], 5.4, 5, n_skin, group=13)
        p.blob(32, 50, 13.4, 6, n_rim, group=2)
        p.blob(32, 45, 12.6, 9.4, n_shell, group=1)
        p.taper([(32, 55), (32, 58.5)], 2.8, n_skin, group=11)
        if p.big:
            for pts in (((27, 37), (26, 45), (27, 53)), ((37, 37), (38, 45), (37, 53)), ((26, 45), (38, 45))):
                p.stroke(list(pts), "t1")
        return


# --------------------------------------------------------------------------
# Chelyra, the lyre tortoise
# --------------------------------------------------------------------------

CHELYRA_COLORS = [
    ("ink", INK),
    ("t0", (112, 40, 24)), ("t1", (168, 72, 40)), ("t2", (216, 120, 72)), ("t3", (240, 168, 120)),
    ("l1", (200, 176, 128)), ("l2", (232, 216, 176)),
    ("o0", (48, 64, 32)), ("o1", (96, 112, 48)), ("o2", (144, 160, 80)),
    ("m0", (144, 136, 136)), ("m1", (208, 200, 192)), ("white", C.white),
    ("pink0", (216, 96, 144)), ("pink1", (248, 184, 208)),
]
CHELYRA_SHINY = {
    # the shell turns marble white and the horns sun-gold
    "t0": (128, 120, 120), "t1": (176, 168, 168), "t2": (216, 208, 200), "t3": (240, 240, 232),
    "m0": (176, 112, 24), "m1": (232, 176, 56), "white": (248, 232, 152),
}

y_shell = Mat(["t0", "t1", "t2", "t3"], line="t0", cuts=[0.18, 0.42, 0.7])
y_band = Mat(["m0", "l1", "l2"], line="t0", cuts=[0.4, 0.72])
y_under = Mat(["m0", "l1", "l2"], line="m0", cuts=[0.45, 0.75])
y_skin = Mat(["o0", "o1", "o2", "l1"], line="o0", cuts=[0.2, 0.48, 0.82])
y_horn = Mat(["m0", "m1", "white"], line="m0", cuts=[0.36, 0.7])
y_nail = Mat(["m0", "m1"], line="m0", cuts=[0.5])

# the lyre in design coordinates (front view): horn control points (an S
# curve: out, in at the yoke, and a flick out at the tip), the crossbar, and
# the seven strings fanning in from the yoke to the tailpiece on the dome
LYRE_NEAR = [(26.5, 31), (19.5, 25), (18, 17.5), (21.6, 12.6), (19.6, 6.4), (15.4, 2.6)]
LYRE_FAR = [(45.5, 29), (52, 23.5), (53.4, 17), (50.6, 12.2), (52.6, 6), (56.4, 2.2)]
YOKE = ((21.6, 13.8), (50.6, 13.2))
STRING_TOP = [(25.4 + 3.3 * i, 15.6 - 0.1 * i) for i in range(7)]
STRING_BOT = [(29.6 + 2 * i, 28.4 - 0.15 * i) for i in range(7)]
TAILPIECE = ((28.4, 29.4), (43.8, 28.4))


def _path(pts):
    return bez3(pts[0], pts[1], pts[2], pts[3], n=14)[:-1] + bez3(pts[3], pts[4], pts[4], pts[5], n=8)


def _horn(p, pts, w0, mat=None, **kw):
    """A thick horn spine: full width for most of its length, tapering at
    the tip."""
    path = _path(pts)
    w0 = p._minw(w0)

    def wf(t):
        return w0 * (1 - 0.45 * t) if t < 0.72 else w0 * 0.55 * (1 - (t - 0.72) / 0.28) + 0.6
    polys = [ribbon(path, wf), ellipse_pts(path[0][0], path[0][1], w0 / 2, w0 / 2, n=12)]
    return p.add(p.mask(*polys), mat or y_horn, **kw)


def _strings(p, top, bot, F=0, glints=()):
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(top, bot)):
        p.stroke([(x0, y0 - F), (x1, y1)], "l2")
    for i, t in glints:
        (x0, y0), (x1, y1) = top[i], bot[i]
        p.px(x0 + (x1 - x0) * t, y0 - F + (y1 - y0 + F) * t, "pink1")


def _chelyra_lyre(p, F=0, far_bias=0.12, k=1.0, ox=0.0, oy=0.0, swap=False):
    """Horns, crossbar and strings; F lifts the tips. k, ox, oy place a
    scaled copy (the back and follower views); swap shades the left horn
    as the far one (seen from behind)."""
    def T(pts):
        return [(ox + x * k, oy + y * k) for x, y in pts]
    near = T([(x, y - (F if i > 1 else 0)) for i, (x, y) in enumerate(LYRE_NEAR)])
    far = T([(x, y - (F if i > 1 else 0)) for i, (x, y) in enumerate(LYRE_FAR)])
    if swap:
        _horn(p, near, 7.2 * k, bias=far_bias, group=60)
        _horn(p, far, 6.6 * k, group=61)
    else:
        _horn(p, far, 6.4 * k, bias=far_bias, group=61)
        _horn(p, near, 7.2 * k, group=60)
    (ax, ay), (bx, by) = T(YOKE)
    p.limb([(ax, ay - F * k), (bx, by - F * k)], 3.2 * k, 3.0 * k, y_horn, group=62)
    p.limb(T(TAILPIECE), 2.6 * k, 2.4 * k, y_band, group=63)
    top, bot = T(STRING_TOP), T(STRING_BOT)
    if p.big:
        _strings(p, top, bot, F * k, glints=((1, 0.3), (4, 0.55), (6, 0.2)) if not F else ((2, 0.45), (5, 0.3)))
    else:
        _strings(p, top[1::2], bot[1::2])


def _dome_poly(cx, cy, rx, ry_top, ry_bot, n=40):
    """A shell seen in 3/4: the upper half of a tall ellipse over the lower
    half of a flat one (the shell's equator)."""
    pts = [(cx + rx * math.cos(math.pi + math.pi * i / n), cy + ry_top * math.sin(math.pi + math.pi * i / n))
           for i in range(n + 1)]
    pts += [(cx + rx * math.cos(math.pi * i / n), cy + ry_bot * math.sin(math.pi * i / n)) for i in range(1, n)]
    return pts


def _band_poly(cx, cy, rx, ry_bot, h, n=40):
    """The marginal band hanging h px below the shell's equator."""
    arc = [(cx + rx * math.cos(math.pi * i / n), cy + ry_bot * math.sin(math.pi * i / n)) for i in range(n + 1)]
    return arc[::-1] + [(x, y + h) for x, y in arc]


def chelyra(p, view, phase):
    if view in ("front", "side", "icon"):
        F = 1 if (phase == 1 and view == "front") else 0
        step = view == "side" and phase == 1
        # far legs and the tail
        p.limb([(34, 53), (34.5, 57.4)], 6.6, 6.4, y_skin, bias=0.3, group=10)
        p.limb([(54.5, 49), (56, 56.6)], 6.4, 6, y_skin, bias=0.36, group=11)
        p.taper([(55.5, 48), (59.5, 50), (61, 52.5)], 3.6, y_skin, bias=0.3, group=11)
        # the lyre, rising from the front of the shell
        _chelyra_lyre(p, F)
        # the shell: the meander band (painted by hand) under a high dome
        p.blob(36, 54.4, 9, 2, y_under, group=3)
        p.poly(_band_poly(39, 43, 19, 5.5, 5), y_band, group=2)
        p.poly(_dome_poly(39, 43, 19, 15.5, 5.5), y_shell, group=1)
        # near legs, short elephantine columns
        p.limb([(25, 52), (24, 56.4)] if not step else [(25, 52), (26.5, 56.4)], 9.4, 9, y_skin, group=12)
        p.limb([(49, 53), (49.5, 56.4)] if not step else [(49, 53), (47.5, 56.4)], 9, 8.6, y_skin, group=13)
        # neck rising, head lifted, eyes half-closed as it plays
        p.limb(bez((27.5, 46), (20, 42), (16.5, 31 - F)), 8.8, 7.8, y_skin, group=4)
        p.blob(12.6, 25 - F, 7.6, 6.8, y_skin, ang=-10, group=7)
        p.blob(6.4, 27.6 - F, 3.8, 3.2, y_skin, ang=-14, group=7)
        if p.big:
            p.stroke([(9, 24 - F), (12, 23 - F), (15, 24 - F)], "ink")
            p.stroke([(4, 30 - F), (8, 31 - F)], "o0")
        else:
            p.px(12, 24 - F, "ink")
        return

    if view == "back":
        # over the shoulder, about 1.2x: the dome and its meander band
        # cropped below, the lyre rising from the shell's front (seen from
        # behind), the head lifted in right profile, eyes closed in song
        p.limb([(5, 58), (3.5, 64)], 8, 8, y_skin, bias=0.2, group=10)        # near hind leg
        # the lyre stands on the shell's far (front) rim, so the dome's crest
        # hides the horn roots and the tailpiece
        _chelyra_lyre(p, k=1.0, ox=-8, oy=5, swap=True)
        p.poly(_band_poly(24, 51, 22, 7, 6), y_band, group=2)
        p.poly(_dome_poly(24, 51, 22, 18.5, 7), y_shell, group=1)
        p.limb(bez((40, 53), (49, 45), (51, 34)), 11, 9.4, y_skin, group=4)
        p.blob(53.4, 26.4, 8.2, 7.2, y_skin, ang=10, group=7)
        p.blob(59.6, 29, 3.6, 3, y_skin, ang=16, group=7)
        if p.big:
            p.stroke([(52, 24), (54, 25), (56, 24)], "ink")
            p.stroke([(58, 31), (61, 30)], "o0")
        return

    if view == "down":
        # follower walking toward the camera: the lyre faces us over the
        # dome, the head in front, the strings shimmering as it walks
        step = phase
        _chelyra_lyre(p, F=step, k=0.82, ox=2.6, oy=7.4)
        p.limb([(19.5, 50), (19, 58.4 - step)], 7.4, 7, y_skin, group=12)
        p.limb([(44.5, 50), (45, 58.4 - (1 - step))], 7.4, 7, y_skin, group=13)
        p.poly(_band_poly(32, 45, 16, 4, 4), y_band, group=2)
        p.poly(_dome_poly(32, 45, 16, 12.5, 4), y_shell, group=1)
        p.limb([(32, 54), (32, 47)], 7.6, 7.6, y_skin, group=4)
        p.blob(32, 45.6, 7.2, 6.4, y_skin, group=7)
        p.blob(32, 50.4, 4, 2.4, y_skin, group=7)
        p.stroke([(27, 44), (28, 45), (29, 44)], "ink")
        p.stroke([(35, 44), (36, 45), (37, 44)], "ink")
        p.pxs([(31, 51), (32, 51)], "o0")
        if p.big:
            p.pxs([(30, 49), (34, 49)], "o0")
        return

    if view == "up":
        # follower walking away: the dome and its meander band from behind,
        # the lyre rising beyond the crest, the tail
        step = phase
        _chelyra_lyre(p, F=step, k=0.82, ox=2.6, oy=7.4, swap=True)
        p.limb([(20, 50), (19.5, 58.4 - step)], 7.4, 7, y_skin, group=12)
        p.limb([(44, 50), (44.5, 58.4 - (1 - step))], 7.4, 7, y_skin, group=13)
        p.poly(_band_poly(32, 46, 16.4, 4.4, 4.4), y_band, group=2)
        p.poly(_dome_poly(32, 46, 16.4, 14, 4.4), y_shell, group=1)
        p.taper([(32, 54), (32, 58)], 3.4, y_skin, group=11)
        if p.big:
            for pts in (((27, 35), (26, 43), (27, 50)), ((37, 35), (38, 43), (37, 50)), ((26, 43), (38, 43))):
                p.stroke(list(pts), "t0")
        return


MONS = [
    Mon("Chelonet", CHELONET_COLORS, CHELONET_SHINY, chelonet, foot=TORTOISE_FOOT),
    Mon("Chelyra", CHELYRA_COLORS, CHELYRA_SHINY, chelyra, foot=TORTOISE_FOOT),
]
