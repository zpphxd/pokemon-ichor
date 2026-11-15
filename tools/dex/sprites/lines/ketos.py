"""Ketos line: Ketofry, Kynoketos (Water / Dragon). The sea monster.

Poseidon's ketos came for Andromeda at Ethiopia and for Hesione at Troy
(Apollodorus 2.4.3, 2.5.9). Kynoketos is the ketos as the vase painters drew
it: a hound's head with pricked ears and a beard of fins, on the coils of a
sea serpent whose tail ends in a tight spiral fin.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink


def spiral(center, start, r0, r1, turns=1.0, n=24, cw=True):
    """A curl from `start` around `center`, its radius shrinking from r0 to r1
    over `turns` turns (clockwise on screen unless cw is False)."""
    cx, cy = center
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    sgn = 1 if cw else -1
    pts = [start]
    for i in range(1, n + 1):
        t = i / n
        a = a0 + sgn * 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# --------------------------------------------------------------------------
# Ketofry, the ketos fry
# --------------------------------------------------------------------------

KETOFRY_COLORS = [
    ("ink", INK),
    ("blue0", (24, 56, 120)), ("blue1", (48, 104, 176)), ("blue2", (96, 152, 216)), ("blue3", (168, 208, 240)),
    ("marble0", (176, 168, 152)), ("marble1", (224, 216, 200)), ("white", C.white),
    ("terra0", (120, 48, 24)), ("terra1", (184, 88, 48)), ("terra2", (232, 144, 96)),
    ("maw", (88, 24, 40)), ("gum", (184, 80, 96)),
]
KETOFRY_SHINY = {
    # sun-gold, like a coin in the shallows
    "blue0": (128, 72, 16), "blue1": (200, 136, 32), "blue2": (240, 192, 64), "blue3": (248, 232, 152),
}

f_hide = Mat(["blue0", "blue1", "blue2", "blue3"], line="blue0", cuts=[0.18, 0.44, 0.72])
f_belly = Mat(["marble0", "marble1", "white"], line="marble0", cuts=[0.38, 0.66])
f_fin = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.34, 0.66])
f_maw = Mat(["maw", "gum"], line="maw", cuts=[0.55])
f_eye = Mat(["marble1", "white"], cuts=[0.6])


def ketofry(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        y = -1 if (view == "side" and phase) else 0
        # tail stalk curling up behind, its fan fin flopped over the back
        tip = (44 + 0.5 * F, 39.5 - F + y)
        p.limb(bez((40, 51 + y), (47.5, 47 + y), tip), 5.6, 4.2, f_hide, bias=0.08, group=5)
        p.lens(tip, (35.5 + F, 33.5 - F + y), 5.8, f_fin, bend=1.4, fat=0.62)
        p.lens(tip, (48.5 + F, 32 - 2 * F + y), 5.2, f_fin, bend=-1.1, fat=0.62, bias=0.12)
        # far eye, bulging over the brow
        p.circle(31.5, 38.5 + y, 3, f_eye, bias=0.2)
        # ragged stub of a dorsal fin
        p.lens((35, 44.5 + y), (38, 39 + y), 3.8, f_fin, bend=-0.6, bias=0.1)
        # dumpy body: a big round head, the body tapering to the tail
        body = p.blob(25, 50 + y, 9.5, 8.5, f_hide, group=1)
        b2 = p.blob(36.5, 49.5 + y, 9, 6.2, f_hide, ang=-22, group=1)
        p.blob(28, 57.5 + y, 11, 4.2, f_belly, ang=-6, clip=[body, b2], group=2)
        # near pectoral fin, drooping
        p.lens((31, 52 + y), (37, 58 + y), 4.4, f_fin, bend=-0.9)
        # the enormous gape, ringed by thick lips
        p.blob(20.5, 50.5 + y, 4.6, 7.2, f_hide, ang=4, group=3)
        p.blob(21.3, 50.2 + y, 3.0 - 0.3 * F, 5.6 + 0.5 * F, f_maw, ang=4)
        # near eye, bulging high on the head
        p.circle(26, 40 + y, 3.5, f_eye)
        # barbels hanging from the chin
        p.limb(bez((18, 57 + y), (16.5, 59 + y), (16 - F, 61 + y)), 1.6, 1.2, f_fin, cap=False)
        p.limb(bez((23, 58 + y), (24, 60 + y), (24.5 + F, 61 + y)), 1.6, 1.2, f_fin, cap=False)
        if p.big:
            p.pxs([(25, 39 + y), (26, 39 + y), (25, 40 + y), (26, 40 + y)], "ink")   # pupil
            p.pxs([(31, 38 + y), (32, 38 + y)], "ink")
        else:
            p.px(25, 40 + y, "ink")
        return

    if view == "back":
        # over the shoulder from behind: the curled tail near us at left, the
        # goggle eye on top and the gape in right profile
        p.limb(bez((16, 54), (6, 46), (12, 33)), 9.5, 7, f_hide, group=5)
        p.lens((12, 34), (3.5, 17), 9.4, f_fin, bend=1.6, fat=0.6)
        p.lens((12, 34), (25, 19), 8.4, f_fin, bend=-1.6, fat=0.6, bias=0.12)
        p.circle(50.5, 29, 3.6, f_eye, bias=0.2)                     # far eye
        p.lens((30, 42), (34, 33), 6, f_fin, bend=-1.0, bias=0.1)       # dorsal stub
        body = p.blob(28, 59, 24, 17, f_hide, group=1)
        head = p.blob(44, 45, 13, 12, f_hide, group=1)
        p.blob(36, 64, 20, 5, f_belly, clip=[body, head], group=2)
        p.blob(49, 57, 8, 4, f_belly, clip=[body, head], group=2)
        p.blob(54.5, 46, 5.4, 8.6, f_hide, group=3)                  # lips
        p.blob(56.4, 46, 3.2, 6.8, f_maw)                            # gape
        p.lens((34, 53), (23, 62), 8, f_fin, bend=1.4)                 # pectoral fin
        p.circle(42, 31, 5.4, f_eye)                                  # near eye
        p.limb(bez((53, 55), (55, 58), (54, 62)), 2.2, 1.6, f_fin, cap=False)
        if p.big:
            p.pxs([(44, 30), (45, 30), (44, 31), (45, 31), (44, 32), (45, 32)], "ink")
            p.pxs([(51, 28), (51, 29)], "ink")
        return

    if view == "down":
        # flopping toward the camera: the gape, both goggle eyes, the tail up
        y = -2 * phase
        p.lens((32, 40 + y), (24 - phase, 27 + y), 7.4, f_fin, bend=1.4, fat=0.62)
        p.lens((32, 40 + y), (40 + phase, 27 + y), 7.4, f_fin, bend=-1.4, fat=0.62)
        p.limb([(32, 44 + y), (32, 37 + y)], 6, 4.4, f_hide, group=5)
        body = p.blob(32, 49 + y, 12.5, 10, f_hide, group=1)
        p.blob(32, 55.5 + y, 10, 4.4, f_belly, clip=[body], group=2)
        p.lens((21, 52 + y), (14, 57 + y - phase), 5.4, f_fin, bend=1)
        p.lens((43, 52 + y), (50, 57 + y - phase), 5.4, f_fin, bend=-1)
        p.blob(32, 51 + y, 6.4, 7.4, f_belly, group=3)
        p.blob(32, 51.5 + y, 4.4, 5.6 + phase, f_maw)
        p.circle(25.5, 40.5 + y, 4.2, f_eye)
        p.circle(38.5, 40.5 + y, 4.2, f_eye)
        p.limb([(28.5, 58 + y), (27.5, 61)], 1.6, 1.4, f_fin, cap=False)
        p.limb([(35.5, 58 + y), (36.5, 61)], 1.6, 1.4, f_fin, cap=False)
        if p.big:
            p.pxs([(26, 41 + y), (27, 41 + y), (37, 41 + y), (38, 41 + y)], "ink")
            p.pxs([(30, 47 + y), (32, 47 + y), (34, 47 + y), (31, 56 + y), (33, 56 + y)], "white")
        else:
            p.pxs([(26, 41 + y), (38, 41 + y)], "ink")
        return

    if view == "up":
        # flopping away: the round back, the curled tail and its fan, the
        # goggle eyes peeking over the brow
        y = -2 * phase
        p.circle(25.5, 39.5 + y, 4, f_eye)
        p.circle(38.5, 39.5 + y, 4, f_eye)
        body = p.blob(32, 49 + y, 12.5, 10, f_hide, group=1)
        p.lens((21, 52 + y), (14, 57 + y - phase), 5.4, f_fin, bend=1)
        p.lens((43, 52 + y), (50, 57 + y - phase), 5.4, f_fin, bend=-1)
        p.lens((32, 44 + y), (32, 38.5 + y), 4, f_fin)
        p.limb(bez((32, 56 + y), (31, 47 + y), (32, 41 + y)), 6.4, 4.6, f_hide, group=5)
        p.lens((32, 42 + y), (23 - phase, 33 + y), 7.4, f_fin, bend=1.4, fat=0.62)
        p.lens((32, 42 + y), (41 + phase, 33 + y), 7.4, f_fin, bend=-1.4, fat=0.62)
        return


# --------------------------------------------------------------------------
# Kynoketos, the sea monster
# --------------------------------------------------------------------------

KYNOKETOS_COLORS = [
    ("ink", INK),
    ("blue0", (16, 40, 96)), ("blue1", (32, 80, 152)), ("blue2", (64, 128, 200)), ("blue3", (136, 192, 232)),
    ("marble0", (160, 152, 144)), ("marble1", (208, 200, 184)), ("white", C.white),
    ("terra0", (120, 48, 24)), ("terra1", (184, 88, 48)), ("terra2", (232, 144, 96)),
    ("gold0", (200, 144, 40)), ("gold1", (248, 208, 72)),
    ("maw", (88, 24, 40)), ("gum", (176, 72, 88)),
]
KYNOKETOS_SHINY = {
    # a red-figure monster: terracotta hide, ink-black markings
    "blue0": (40, 24, 24), "blue1": (152, 64, 32), "blue2": (208, 112, 64), "blue3": (240, 176, 128),
}

k_hide = Mat(["blue0", "blue1", "blue2", "blue3"], line="blue0", cuts=[0.2, 0.5, 0.78])
k_belly = Mat(["marble0", "marble1", "white"], line="marble0", cuts=[0.36, 0.66])
k_fin = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.32, 0.64])
k_maw = Mat(["maw", "gum"], line="maw", cuts=[0.55])
k_tooth = Mat(["marble1", "white"], cuts=[0.5])


def arc(c, r, a0, a1, n=None):
    """Points on a circle around c from angle a0 to a1 (degrees, y down)."""
    n = n or max(6, int(abs(a1 - a0) / 10))
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


# the two loops of the front view: centers and centerline radii
KY_C1, KY_R1 = (32, 49), 8.6     # the near loop, low
KY_C2, KY_R2 = (49, 30), 8       # the far loop, behind and higher


def kynoketos(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        C1, R1, C2, R2 = KY_C1, KY_R1, KY_C2, KY_R2
        # ---- the tail: out of the far loop, up the right side, curling into a
        # tight spiral edged with fin, as the vase painters drew it
        tail = bez3((56, 39), (62, 31), (61, 18), (55, 13 - F), n=16)
        p.limb(tail, 6.6, 4.4, k_hide, group=8)
        sp = spiral((50.5 - F * 0.5, 9.5 - F), (55, 13 - F), 4.8, 1.0, turns=1.05, n=26, cw=False)
        p.limb(sp, 6.4, 3.0, k_fin, group=9)
        p.limb(sp[:20], 3.0, 1.4, k_hide, group=10, noline=True)
        # crest along the top of the far loop, rooted behind it
        for a, ln in ((-160, 7), (-122, 9.5), (-86, 10), (-52, 6.4), (-22, 4.2)):
            r0, r1 = R2 + 1.5, R2 + 1.5 + ln
            x, y = C2[0] + r0 * math.cos(math.radians(a)), C2[1] + r0 * math.sin(math.radians(a))
            x2, y2 = C2[0] + r1 * math.cos(math.radians(a + 20)), C2[1] + r1 * math.sin(math.radians(a + 20))
            p.lens((x, y), (x2, y2), 5.4, k_fin, bend=-1.0, fat=0.3, bias=0.12)
        # ---- the far loop (counterclockwise from its bottom), behind everything
        p.limb(arc(C2, R2, 95, -205), 8.4, 7.6, k_hide, group=6, bias=0.1)
        p.limb(bez((C2[0] - 6.5, C2[1] + 5), (C2[0] + 1, C2[1] + 10.5), (56, 39)), 7.8, 6.6, k_hide, group=7, bias=0.06)
        # ---- the near loop's back half and the run up to the far loop
        p.limb(arc(C1, R1, -90, 25), 9.6, 9, k_hide, group=4, bias=0.05)
        p.limb(bez((C1[0], C1[1] - R1), (39, 38.5), (C2[0] - 6.5, C2[1] + 5)), 9, 8.2, k_hide, group=5, bias=0.06)
        # far flipper, peeking past the neck
        p.lens((30, 31), (39, 35), 4.6, k_fin, bend=-0.8, fat=0.6, bias=0.15)
        # ---- the near loop's front half, clockwise from the right side
        coil = p.limb(arc(C1, R1, 18, 272), 9.6, 9.6, k_hide, group=1)
        p.limb(arc(C1, R1 - 3.2, 28, 258), 3.8, 3.8, k_belly, clip=[coil], group=2)
        # ---- neck rising from the near loop to the head
        neck = p.limb(bez((C1[0] + 1, C1[1] - R1 + 1), (27, 34), (24, 22)), 11, 9.6, k_hide, group=1)
        p.limb(bez((27.5, 42), (22.5, 34), (19.5, 25)), 4.4, 3.6, k_belly, clip=[neck], group=2)
        # crest down the back of the neck
        for a, b in (((28, 12), (35, 5.5)), ((29.5, 18), (38.5, 13)), ((30.5, 24), (39.5, 21)), ((31, 29.5), (39, 29))):
            p.lens(a, b, 5.2, k_fin, bend=-0.8, fat=0.3, bias=0.15, under=True)
        # ---- the hound's head
        p.lens((26, 13 - F), (31, 2 - F), 5, k_hide, bend=-0.5, bias=0.22, group=10)   # far ear
        p.blob(22, 17 - F, 7.6, 6.8, k_hide, group=3)                                 # skull
        p.limb([(18, 16 - F), (5, 18 - F)], 7.6, 5.6, k_hide, group=3)                 # muzzle
        drop = 2 * F
        p.limb([(21, 24 - F), (7, 27 + drop - F)], 5.6, 4.0, k_hide, group=4)          # lower jaw
        p.poly([(6, 20.5 - F), (19, 21 - F), (21, 24 - F), (8, 25.5 + drop - F)], k_maw)
        p.lens((24, 12 - F), (21, 1 - F), 5.4, k_hide, bend=0.6, group=11)            # near ear
        # frilled beard under the jaw
        for a, b in (((10, 26 + drop - F), (7, 33 + drop)), ((13.5, 26 + drop - F), (12, 35 + drop)),
                     ((17, 26 + drop - F), (17, 35 + drop)), ((20.5, 25 - F), (22, 33))):
            p.lens(a, b, 3.6, k_fin, bend=0.6)
        # near flipper, sweeping down and forward from behind the jaw
        p.lens((25, 29), (11, 40), 7.2, k_fin, bend=-1.6, fat=0.62)
        if p.big:
            p.eye(17, 14 - F, 3, 3, iris="gold1", shine="white", shine_at=(1, 0))
        else:
            p.px(18, 15, "ink")
        return

    if view == "back":
        # over the shoulder: a great coil close to us, cropped by the frame;
        # the neck rearing away to the right, the head in profile with the
        # jaws agape; the spiral tail raised at the left
        tail = bez3((14, 50), (1, 40), (2, 21), (11, 15), n=18)
        p.limb(tail, 8.6, 5.4, k_hide, group=8)
        sp = spiral((14.5, 9.5), (11, 15), 5.4, 1.2, turns=1.05, n=26, cw=True)
        p.limb(sp, 7, 3.2, k_fin, group=9)
        p.limb(sp[:20], 3.4, 1.6, k_hide, group=10, noline=True)
        # crest down the back of the neck, rooted behind it
        for a, b in (((40, 17), (31, 9)), ((38.5, 23), (28.5, 18)), ((37.5, 30), (27.5, 27)), ((37.5, 37), (28, 36.5))):
            p.lens(a, b, 6, k_fin, bend=0.9, fat=0.3, bias=0.12)
        # far flipper
        p.lens((47, 36), (57, 44), 6, k_fin, bend=1.0, fat=0.6, bias=0.15)
        # the neck rising out of the coil
        neck = p.limb(bez((36, 56), (42, 44), (42, 28)), 14, 11.5, k_hide, group=1)
        p.limb(bez((43.5, 54), (48, 42), (48, 30)), 4.4, 3.6, k_belly, clip=[neck], group=2)
        # the great near coil, a loop with daylight through it
        C, R = (21, 52), 11.5
        coil = p.limb(arc(C, R, -10, 330, n=40), 13, 13, k_hide, group=3)
        p.limb(arc(C, R - 4.4, 200, 330, n=16), 3.6, 3.6, k_belly, clip=[coil], group=4)
        # the hound's head in right profile (groups 50+; the battle back's
        # head is the front's hand-finished head, mirrored)
        p.lens((41, 14), (38, 3), 5.6, k_hide, bend=0.6, bias=0.22, group=50)   # far ear
        p.blob(45, 19, 8, 7.2, k_hide, group=51)
        p.limb([(49, 18), (61, 20.5)], 8, 5.6, k_hide, group=51)
        p.limb([(46, 27), (59, 31.5)], 5.8, 4.2, k_hide, group=52)
        p.poly([(60, 23.5), (49, 24), (46, 27), (58, 29)], k_maw, group=53)
        p.lens((44, 13), (45, 2.5), 6, k_hide, bend=-0.6, group=54)       # near ear
        for a, b in (((56, 33), (59, 39)), ((52.5, 33), (54, 41)), ((49, 32), (49, 40)), ((46, 30.5), (44, 37))):
            p.lens(a, b, 3.8, k_fin, bend=-0.6, fat=0.35, group=55)
        # near flipper, sweeping back from behind the jaw
        p.lens((40, 33), (25, 41), 8.4, k_fin, bend=1.8, fat=0.55)
        if p.big:
            p.eye(49, 16, 3, 3, iris="gold1", shine="white", shine_at=(1, 0))
        return

    if view in ("down", "up"):
        # follower: the head reared over a coiled body; phase sways the
        # coils and flicks the spiral tail
        y = -phase
        down = view == "down"
        tx = 50 if down else 14
        p.limb(bez((tx - 8 * (1 if down else -1), 56), (tx + (2 if down else -2), 50), (tx, 38 + y)), 6.4, 4.2, k_hide, group=6)
        p.limb(spiral((tx - (3 if down else -3), 33.5 + y), (tx, 38 + y), 4, 1.2, turns=0.95, cw=not down), 4.4, 2.2,
               k_fin, group=8)
        coil = p.limb(arc((32, 54), 10, 0, 360, n=36), 7.4, 7.4, k_hide, group=1)
        if down:
            p.limb(arc((32, 54), 7.8, 200, 340, n=12), 2.6, 2.6, k_belly, clip=[coil], group=2)
        p.lens((25, 41 + y), (13, 46 - y), 7, k_fin, bend=-1.2)
        p.lens((39, 41 + y), (51, 46 - y), 7, k_fin, bend=1.2)
        neck = p.limb([(32, 52), (32, 36 + y)], 10.5, 9.6, k_hide, group=3)
        if down:
            p.limb([(32, 50), (32, 39 + y)], 4, 3.4, k_belly, clip=[neck], group=4)
        p.lens((27, 27 + y), (22.5, 15 + y), 5.4, k_hide, bend=0.4, group=9)
        p.lens((37, 27 + y), (41.5, 15 + y), 5.4, k_hide, bend=-0.4, group=9)
        p.blob(32, 30 + y, 7.6, 6.6, k_hide, group=10)
        if down:
            p.blob(32, 36.5 + y, 5, 3.6, k_hide, group=10)
            p.blob(32, 38 + y, 3.4, 2 + phase, k_maw)
            for a, b in (((28.5, 40 + y), (26.5, 46 + y)), ((32, 41 + y), (32, 47.5 + y)), ((35.5, 40 + y), (37.5, 46 + y))):
                p.lens(a, b, 3.6, k_fin)
            p.eye(27, 28 + y, 2, 3, iris="gold1", shine="white")
            p.eye(35, 28 + y, 2, 3, iris="gold1", shine="white")
            p.pxs([(31, 34 + y), (32, 34 + y)], "ink")
        else:
            for a, b in (((32, 26 + y), (32, 19 + y)), ((32, 33 + y), (36, 27 + y)), ((32, 40 + y), (37, 35 + y))):
                p.lens(a, b, 3.6, k_fin, bend=-0.5)
        return


MONS = [
    Mon("Ketofry", KETOFRY_COLORS, KETOFRY_SHINY, ketofry, foot="blank"),
    Mon("Kynoketos", KYNOKETOS_COLORS, KYNOKETOS_SHINY, kynoketos, foot="blank"),
]
