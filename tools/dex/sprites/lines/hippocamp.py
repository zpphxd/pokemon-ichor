"""Hippocamp line: Hipling, Thalamare, Seismare (Water starter).

Poseidon's sea-horses: a horse's forequarters and a fish's tail, with the
bronze hooves and golden manes of the Iliad's team (13.23-30). Seismare is
the Earth-shaker's steed, the horse that sprang from the struck rock.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Hipling, the sea foal
# --------------------------------------------------------------------------

HIPLING_COLORS = [
    ("ink", INK),
    ("hide0", C.aegean[0]), ("hide1", (64, 120, 192)), ("hide2", C.aegean[2]), ("hide3", C.aegean[3]),
    ("cream0", C.limestone[1]), ("cream1", C.limestone[2]), ("white", C.white),
    ("gold0", (152, 96, 32)), ("gold1", C.sungold[0]), ("gold2", C.sungold[1]), ("gold3", (248, 232, 136)),
    ("fin0", C.marble[0]), ("sheen", (200, 240, 248)),
    ("iris", (40, 144, 160)),
]
HIPLING_SHINY = {
    # wet-sand limestone hide, Aegean-blue mane
    "hide0": (104, 80, 56), "hide1": (160, 128, 88), "hide2": (200, 176, 128), "hide3": (232, 216, 176),
    "cream0": (216, 200, 168), "cream1": (240, 232, 208),
    "gold0": (24, 48, 112), "gold1": (40, 88, 168), "gold2": (80, 144, 216), "gold3": (160, 208, 240),
    "iris": (48, 104, 176), "sheen": (248, 248, 232),
}

hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.16, 0.44, 0.72])
cream = Mat(["cream0", "cream1", "white"], line="hide0", cuts=[0.42, 0.7])
mane = Mat(["gold0", "gold1", "gold2", "gold3"], line="gold0", cuts=[0.16, 0.44, 0.74])
fin = Mat(["fin0", "cream1", "white"], line="fin0", cuts=[0.4, 0.7])
bronze = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])


def spiral(center, start, r0, r1, turns=1.0, n=24):
    """A clockwise curl: from `start` into a spiral around `center` whose
    radius shrinks from r0 to r1 over `turns` turns."""
    cx, cy = center
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    pts = [start]
    for i in range(1, n + 1):
        t = i / n
        a = a0 + 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _hoof(p, x, y, far=False):
    """A bronze hoof whose top-left is at (x, y)."""
    p.rect(x, y, x + 2, y + 1, bronze, bias=0.3 if far else 0)


def hipling(p, view, phase):
    if view in ("front", "side", "icon"):
        walk = view == "side"
        L = 1 if (phase == 1 and not walk) else 0

        if walk and phase:
            far_leg = [(30, 47), (31, 53), (30.5, 57.5)]
            near_leg = [(24, 47), (25.5, 53), (25, 57.5)]
        elif walk:
            far_leg = [(30, 47), (29, 53), (28, 57.5)]
            near_leg = [(24, 47), (21.5, 52.5), (20, 57)]
        else:
            far_leg = [(30.5, 47), (31, 53), (30.5, 57.5)]
            # the near foreleg kicks: knee forward, hoof tucked under
            near_leg = [(24, 47), (19, 51.5), (21, 55.5 - L)]

        # Split caudal fan at the tip of a supporting U-coil.
        p.lens((52, 40), (51 - phase, 29), 6.4, fin, bend=1.1)
        p.lens((53, 40), (60, 34 - phase), 5.8, fin, bend=-1.1, bias=0.1)

        # far foreleg
        p.limb(far_leg, 4, 3, hide, bias=0.35, group=10)
        _hoof(p, int(far_leg[-1][0]) - 1, 58, far=True)
        p.lens((far_leg[-1][0] + 1, 56.5), (far_leg[-1][0] + 4, 54), 2.4, fin, bias=0.3)

        # tail: back from the rump and down, curling like a seahorse's into
        # a spiral that props the foal up
        tail = bez3((36, 44.5), (43, 59), (53, 60), (53, 39), n=24)
        p.limb(tail, 8, 3.2, hide, group=5)

        # body: a round foal's chest and a short barrel
        body = p.blob(28.5, 45, 7.6, 6, hide, group=1)
        p.blob(35.5, 44.5, 5.2, 4.8, hide, group=1)
        neck = p.limb([(29.5, 43), (28.5, 38), (27, 34)], 8.4, 8, hide, group=1)
        # pale underside from the throat down the chest to the belly
        p.limb([(23, 38), (22.5, 44), (27, 50.5), (34, 50)], 5, 3.4, cream, clip=[body, neck], group=2)

        # mane, far side: frilly gold fins along the crest
        p.lens((28, 23.5 - L), (37, 26.5 - L), 5.6, mane, bend=-1)
        p.lens((30.5, 28 - L), (38.5, 33), 5.4, mane, bend=-0.8)
        p.lens((32, 33), (38, 40), 4.8, mane, bend=-0.6)

        # far ear
        p.lens((29, 26 - L), (32, 17.5 - L), 4.4, hide, bend=-0.3, bias=0.15)

        # head: a big foal's cranium and a short soft muzzle
        p.blob(25, 29.5 - L, 7.4, 7.4, hide, group=3)
        p.blob(18.5, 33.5 - L, 4.8, 3.4, hide, ang=10, group=3)
        p.blob(16.5, 36 - L, 4.4, 2.6, cream, ang=10, group=4, bias=-0.2)

        # near ear and forelock
        p.lens((24, 24.5 - L), (21, 16 - L), 4.8, hide, bend=0.5)
        p.lens((23.5, 23 - L), (21.5, 18 - L), 2, cream, bend=0.3, bias=0.1)
        p.lens((28, 22.5 - L), (21, 20.5 - L), 3.8, mane, bend=0.8)

        # near foreleg
        p.limb(near_leg, 4.4, 3.2, hide, group=12)
        fx, fy = near_leg[-1]
        _hoof(p, int(fx) - 1, 58 if walk else int(fy) + 1)
        p.lens((fx + 1, fy - 1), (fx + 4, fy - 3.5), 2.4, fin)

        # face
        p.eye(22, 26 - L, 4, 6, iris="iris", shine="white")
        if p.big:
            p.px(14, 33 - L, "hide0")
            p.stroke([(14, 37 - L), (17, 37 - L)], "hide0")
            p.stroke([(51, 37), (50 - phase, 32)], "hide1")
            p.stroke([(54, 38), (58, 35 - phase)], "hide1")
            p.pxs([(35, 43), (36, 44), (39, 47), (40, 48)], "sheen")
        return

    if view == "back":
        p.lens((12, 46), (6, 34), 7, fin, bend=1.2, under=False)
        p.lens((12.5, 46), (19, 33), 6, fin, bend=-1, under=False)
        p.blob(22, 60, 19, 13, hide, group=1)
        p.limb(bez((8, 62), (6, 52), (12, 46), n=10), 9, 5, hide, group=5)
        p.limb([(32, 50), (36, 41), (40, 33)], 12, 10.5, hide, group=1)
        p.lens((30, 30), (38, 14), 8, mane, bend=1.2)
        p.lens((30, 40), (34, 24), 7, mane, bend=1.2)
        p.blob(43, 26, 9, 8.4, hide, group=3)
        p.blob(52, 30, 6, 4.2, hide, ang=-6, group=3)
        p.blob(52.5, 32.4, 4.6, 2.2, cream, ang=-6, group=4)
        p.lens((40, 19), (37, 9), 5.4, hide, bend=0.5)
        p.lens((42, 19), (47, 10), 5, hide, bend=-0.4)
        p.eye(46, 22, 4, 6, iris="iris", shine="white", shine_at=(1, 1))
        if p.big:
            p.px(58, 30, "hide0")
            p.stroke([(53, 34), (56, 34)], "hide0")
        return

    if view == "up":
        # walking away: rump and coiled tail nearest us, mane down the neck, ears
        p.limb([(22, 45), (21, 52), (21, 57 - 2 * phase)], 5, 4, hide, bias=0.35, group=10)
        p.limb([(42, 45), (43, 52), (43, 57 - 2 * (1 - phase))], 5, 4, hide, bias=0.35, group=11)
        p.lens((26.5, 22), (20, 12), 6, hide, bend=0.5)
        p.lens((37.5, 22), (44, 12), 6, hide, bend=-0.5)
        p.blob(32, 25, 9.8, 7.6, hide, group=3)
        p.limb([(32, 29), (32, 37)], 13, 16, hide, group=1)
        p.blob(32, 43.5, 14.5, 9, hide, group=1)
        for i, (y, dx) in enumerate(((20, -1), (26, 1), (32, -1), (38, 1))):
            p.lens((32, y), (32 + 6.5 * dx, y + 4), 5.4, mane, bend=-dx * 0.8)
        p.limb([(32, 19), (32, 41)], 4, 3.4, mane)
        p.limb(bez3((32, 48.5), (30, 60), (48, 62), (47, 40), n=20), 7.4, 3, hide, group=5)
        p.lens((47, 41), (42 - phase, 30), 6, fin, bend=1.0)
        p.lens((48, 41), (55, 34 + phase), 5.4, fin, bend=-0.8)
        return

    if view == "down":
        # walking toward us: big head, both eyes, cream muzzle and chest
        step = phase
        p.limb(bez3((36, 50), (42, 62), (48, 59), (47, 42), n=18), 5, 2.4, hide, bias=0.2, group=5)
        p.lens((47, 43), (44 - step, 33), 5.4, fin, bend=0.8)
        p.lens((48, 43), (55, 37 + step), 4.8, fin, bend=-0.8)
        p.blob(32, 47, 8, 7, hide, group=1)
        p.blob(32, 47, 4.6, 5.4, cream, group=1)
        p.limb([(28, 50), (27.5, 60 - 2 * step)], 4, 3.4, hide, group=12)
        p.limb([(36, 50), (36.5, 60 - 2 * (1 - step))], 4, 3.4, hide, group=13)
        p.rect(26, 59 - 2 * step, 29, 60 - 2 * step, bronze)
        p.rect(35, 59 - 2 * (1 - step), 38, 60 - 2 * (1 - step), bronze)
        p.lens((25, 27), (20, 15), 5.6, hide, bend=0.5)
        p.lens((39, 27), (44, 15), 5.6, hide, bend=-0.5)
        p.blob(32, 30, 9.6, 8.6, hide, group=3)
        p.lens((32, 20), (32, 27), 5.4, mane)
        p.blob(32, 37.5, 5.4, 3.6, cream, group=4)
        p.eye(25, 28, 4, 5, iris="iris", shine="white")
        p.eye(35, 28, 4, 5, iris="iris", shine="white", shine_at=(1, 1))
        p.pxs([(30, 38), (34, 38)], "hide0")
        return


# --------------------------------------------------------------------------
# Thalamare, the hippocamp
# --------------------------------------------------------------------------

THALAMARE_COLORS = [
    ("ink", INK),
    ("hide0", C.aegean[0]), ("hide1", (64, 120, 192)), ("hide2", C.aegean[2]), ("hide3", C.aegean[3]),
    ("marble0", C.marble[0]), ("marble1", C.marble[1]), ("white", C.white),
    ("gold0", (152, 96, 32)), ("gold1", C.sungold[0]), ("gold2", C.sungold[1]), ("gold3", (248, 232, 136)),
    ("iris", (40, 144, 160)), ("sheen", (200, 240, 248)),
]
THALAMARE_SHINY = {
    # pale marble hide, deep Aegean-blue mane
    "hide0": (88, 88, 104), "hide1": (144, 144, 152), "hide2": (200, 200, 200), "hide3": (240, 240, 232),
    "marble0": (176, 160, 136), "marble1": (224, 216, 192),
    "gold0": (16, 32, 88), "gold1": (24, 64, 136), "gold2": (48, 104, 176), "gold3": (112, 168, 224),
    "iris": (200, 144, 40), "sheen": (248, 248, 248),
}

belly = Mat(["marble0", "marble1", "white"], line="hide0", cuts=[0.42, 0.7])
tfin = Mat(["hide2", "marble1", "white"], line="hide1", cuts=[0.35, 0.68])


THAL_TAIL = bez3((35, 39), (42, 46), (38, 58), (46, 58.5), n=14) + \
    bez3((46, 58.5), (55, 59), (57, 49), (51, 44), n=12)[1:] + \
    bez3((51, 44), (47, 40), (48, 33), (54, 29.5), n=10)[1:]


def thalamare_parts(p, phase=0):
    """The rearing hippocamp, facing left. Returns {name: part id(s)}."""
    L = phase
    R = {}
    # caudal fin, forked, at the top of the S
    # in frame 2 the fin flares wider
    R["cfin"] = [p.lens((53, 30), (46 - L, 15 - L), 8 + L, tfin, bend=1.4, group=40),
                 p.lens((54.5, 30.5), (60, 21 - L), 7 + L, tfin, bend=-1.2, group=41)]
    # far foreleg, raised: knee forward, cannon hanging, a webbed flipper
    R["fleg"] = [p.limb([(23, 29.5), (11, 28.5)], 7.2, 6.4, hide, bias=0.3, group=10),
                 p.limb([(10.5, 29), (9, 35)], 5.8, 4.8, hide, bias=0.3, group=11)]
    R["fhoof"] = p.blob(8.8, 36.4, 3.3, 2, bronze, bias=0.2, group=12)
    if p.big:
        R["fweb"] = p.lens((7.8, 36), (3, 41.5), 6, belly, bend=0.4, bias=0.2, group=13)
    # fin mane: a gold fin from the brow over the poll and down the crest,
    # its trailing edge scalloped into lobes
    mane_poly = [(15, 11), (19, 7.5), (24, 6.5), (29, 7), (35, 6.5), (32, 11.5), (40, 14),
                 (35.5, 18), (43, 22), (37.5, 25.5), (44, 30.5), (37.5, 33), (41, 37.5),
                 (34, 37), (31, 30), (28, 22), (25, 15), (20, 11)]
    # in frame 2 the head lifts and the lobe tips flick back
    tips = {(35, 6.5), (40, 14), (43, 22), (44, 30.5), (41, 37.5)}
    R["mane"] = p.poly([(x + (1.2 * L if (x, y) in tips else 0), y - (L if y < 20 else 0) - (0.8 * L if (x, y) in tips else 0))
                        for x, y in mane_poly], mane, group=31)
    # far ear fin
    R["fear"] = p.lens((21.5, 11 - L), (26.5, 2.5 - L), 5, mane, bend=-0.6, bias=0.2, group=35)
    # tail: the S-coil, thick at the hips and down to the ground, then up
    s_path = THAL_TAIL
    k = 14
    R["tail"] = p.limb(s_path[:k + 1], 13, 7.4, hide, group=1)
    R["tail2"] = p.limb(s_path[k:], 7.4, 3.6, hide, group=5)
    # body: chest and a short barrel that becomes the tail
    R["body"] = [p.blob(25, 32.5, 9, 8, hide, group=1),
                 p.blob(32, 37.5, 7.6, 6.6, hide, ang=30, group=1)]
    R["neck"] = p.limb([(26, 31), (24.5, 24), (21, 18 - L)], 12, 10, hide, group=1)
    R["belly"] = p.limb(bez3((15, 24 - L), (17, 33), (26, 43), (39, 49), n=12), 5, 5.6, belly,
                        clip=R["body"] + [R["neck"], R["tail"]], group=1)
    # head: cranium and a long sleek muzzle, nose down
    R["head"] = [p.blob(19.5, 16.5 - L, 7.2, 6.8, hide, group=3),
                 p.limb(bez((16, 19 - L), (12, 20 - L), (9, 23 - L)), 7, 5, hide, group=3)]
    R["muzzle"] = p.blob(9.5, 23.6 - L, 4.6, 2.2, belly, ang=30, group=3, clip=R["head"])
    # near ear fin
    R["ear"] = p.lens((17, 11.5 - L), (12, 3 - L), 5.6, mane, bend=0.7, group=36)
    # near foreleg, raised higher, webbed flipper forward
    R["leg"] = [p.limb([(27, 37), (14, 38)], 8.4, 7.2, hide, group=14),
                p.limb([(13.5, 38.5), (14, 45)], 6.4, 5.4, hide, group=15)]
    R["hoof"] = p.blob(13.8, 47, 3.6, 2.1, bronze, group=16)
    if p.big:
        R["web"] = p.lens((12, 46.5), (5.5, 52.5), 7, belly, bend=0.5, group=17)
    if p.big:
        # rays through the webbing
        for a, b in (((12, 47), (6.5, 51.5)), ((13.5, 48), (9.5, 53)), ((7.5, 37), (3.5, 40.5))):
            p.stroke([a, b], "gold0")
    return R


def thalamare(p, view, phase):
    if view in ("front", "side", "icon"):
        L = phase
        thalamare_parts(p, L)
        p.eye(16, 14 - L, 4, 5, iris="iris", shine="white")
        if p.big:
            p.px(6, 21 - L, "hide0")
            p.stroke([(8, 25 - L), (11, 25 - L)], "hide0")
            p.stroke([(50, 26), (47 - L, 18 - L)], "hide1")
            p.stroke([(55, 28), (58, 23 - L)], "hide1")
            p.pxs([(28, 29), (29, 30), (34, 38), (35, 39)], "sheen")
        return

    if view == "back":
        # tail fin spread wide behind, head turned right in profile
        p.lens((14, 50), (2, 34), 9, tfin, bend=1.6)
        p.lens((15, 50), (14, 30), 8, tfin, bend=0.4)
        p.lens((17, 50), (26, 34), 8, tfin, bend=-1.4)
        p.blob(24, 61, 21, 14, hide, group=1)
        p.limb([(14, 62), (14, 54), (15, 50)], 10, 6, hide, group=5)
        p.limb([(34, 50), (38, 38), (42, 28)], 13, 11, hide, group=1)
        p.lens((34, 30), (24, 22), 9, mane, bend=1.4)
        p.lens((36, 38), (25, 36), 8, mane, bend=1.2)
        p.lens((38, 22), (30, 10), 8, mane, bend=1.4)
        p.blob(45, 22, 8, 7.4, hide, group=3)
        p.blob(54, 27, 6.4, 4, hide, ang=22, group=3)
        p.blob(55, 29.5, 4.6, 2, belly, ang=22, group=4)
        p.lens((42, 16), (40, 5), 5.4, mane, bend=0.6)
        p.lens((46, 16), (50, 6), 5, mane, bend=-0.6)
        p.eye(48, 18, 3, 5, iris="iris", shine="white", shine_at=(1, 1))
        if p.big:
            p.px(60, 27, "hide0")
        return

    if view == "up":
        # swimming away: ear fins, the fin mane down the neck, hips and the
        # tail fin spread wide nearest us
        p.blob(20.5, 45.5, 3, 2, bronze)
        p.blob(43.5, 45.5, 3, 2, bronze)
        p.lens((26, 18), (18, 8), 6, mane, bend=0.5)
        p.lens((38, 18), (46, 8), 6, mane, bend=-0.5)
        p.blob(32, 22, 9.6, 7.6, hide, group=3)
        p.limb([(32, 26), (32, 34)], 13, 16, hide, group=1)
        p.blob(32, 40, 14.5, 9, hide, group=1)
        p.poly([(32, 13), (35, 17), (34, 23), (35.5, 30), (34, 38), (32, 42), (30, 38), (28.5, 30), (30, 23), (29, 17)], mane)
        p.limb([(32, 45), (32, 51)], 8, 5.6, hide, group=5)
        p.lens((32, 51), (16, 56 - 2 * phase), 8.6, tfin, bend=-1.2)
        p.lens((32, 51), (48, 54 + 2 * phase), 8.6, tfin, bend=1.2)
        p.lens((32, 51), (32 + 2 * phase, 61), 6, tfin)
        return

    if view == "down":
        # rearing toward us: forelegs kicking in turn, ear fins, marble muzzle
        step = phase
        p.limb([(32, 46), (35, 54), (41, 57)], 8, 4, hide, bias=0.2, group=5)
        p.lens((41, 57), (49.5, 50), 6.4, tfin, bend=-1)
        p.lens((41.5, 57.5), (51, 60), 5.4, tfin, bend=0.6)
        p.blob(32, 41, 10.4, 8.6, hide, group=1)
        p.blob(32, 43, 5.4, 6, belly, group=1)
        p.limb([(26.5, 45), (24, 50 - 3 * step), (25, 54 - 3 * step)], 5, 4, hide, group=12)
        p.limb([(37.5, 45), (40, 50 - 3 * (1 - step)), (39, 54 - 3 * (1 - step))], 5, 4, hide, group=13)
        p.blob(25, 55.5 - 3 * step, 3, 2, bronze)
        p.blob(39, 55.5 - 3 * (1 - step), 3, 2, bronze)
        p.lens((25, 20), (19, 7), 5.8, mane, bend=0.6)
        p.lens((39, 20), (45, 7), 5.8, mane, bend=-0.6)
        p.lens((32, 9), (32, 20), 6, mane)
        p.blob(32, 24, 9.6, 8.4, hide, group=3)
        p.blob(32, 31.5, 5.6, 3.6, belly, group=4)
        p.eye(25, 21, 4, 5, iris="iris", shine="white")
        p.eye(35, 21, 4, 5, iris="iris", shine="white", shine_at=(1, 1))
        p.pxs([(30, 32), (34, 32)], "hide0")
        return


# --------------------------------------------------------------------------
# Seismare, the Earth-shaker's steed
# --------------------------------------------------------------------------

SEISMARE_COLORS = [
    ("ink", INK),
    ("hide0", C.aegean[0]), ("hide1", (64, 120, 192)), ("hide2", C.aegean[2]), ("hide3", C.aegean[3]),
    ("wave0", (16, 48, 112)), ("wave1", (32, 96, 176)), ("wave2", (96, 168, 224)),
    ("foam", C.marble[1]), ("white", C.white), ("gold", (232, 176, 56)),
    ("stone0", C.limestone[0]), ("stone1", C.limestone[1]), ("wave3", (176, 224, 240)),
    ("terra", C.terracotta[1]),
]
SEISMARE_SHINY = {
    # sandy limestone hide, deep Aegean-blue mane
    "hide0": (112, 80, 48), "hide1": (168, 128, 80), "hide2": (208, 176, 120), "hide3": (240, 224, 176),
    "wave0": (16, 40, 104), "wave1": (32, 80, 160), "wave2": (88, 144, 208), "wave3": (160, 200, 240),
}

wave = Mat(["wave0", "wave1", "wave2", "wave3"], line="wave0", cuts=[0.2, 0.45, 0.72])
foam = Mat(["foam", "white"], line="wave0", cuts=[0.5])
stone = Mat(["stone0", "stone1", "foam"], line="stone0", cuts=[0.34, 0.66])
shin = Mat(["hide0", "hide1", "hide2"], line="hide0", cuts=[0.3, 0.62])
sfin = Mat(["wave0", "wave1", "wave2"], line="wave0", cuts=[0.3, 0.62])


SEIS_TAIL = bez3((37, 40), (45, 43), (48, 49), (50.5, 54.5), n=12)


def seismare_parts(p, phase=0):
    """The rearing Earth-shaker, facing left. Returns {name: part id(s)}."""
    L = phase
    R = {}
    # the stone it stands on, cracked under the planted fin
    R["stone"] = [p.poly([(27, 58.5), (33, 54.5), (45, 55), (53, 53.5), (62.5, 55), (62.5, 58), (28, 60)],
                         stone, group=50),
                  p.poly([(27, 58.5), (62.5, 57.5), (62.5, 61), (58.5, 62.5), (31, 62.5), (27.5, 61)],
                         stone, bias=0.45, group=51)]
    # the wave mane, curling forward over the head, behind everything
    wave_poly = [(39, 35), (44.5, 26), (47.5, 16), (46, 8), (41, 3.5), (34, 2), (27.5, 3), (23.5, 6),
                 (24, 10), (27, 9.5), (30, 7.5), (34, 8), (36.5, 12), (34.5, 17), (32, 23), (32, 30)]
    if L:
        # frame 2: the wave's lip curls further over and down
        wave_poly[7:9] = [(22, 6.5), (22.5, 11)]
    R["wave"] = p.poly([(x, y - L) for x, y in wave_poly], wave, group=31)
    p.limb(bez3((24, 7 - L), (30, 0.5), (42, 2), (45, 12), n=18), 4, 2, foam, group=32)
    p.limb(bez3((44, 15), (37, 11), (35, 21), (43, 23), n=16), 3, 2, foam, group=32)
    p.limb(bez3((43, 24), (38, 21), (36, 28), (39, 31), n=12), 3, 1.6, foam, group=32)
    p.limb(bez3((43, 7), (49, 15), (45, 26), (41, 34), n=18), 2, 1.4, Mat(["gold"]), group=33)
    # far foreleg, raised high to strike
    R["fleg"] = [p.limb([(25, 29), (14, 25.5 - L)], 8, 7, hide, bias=0.3, group=10),
                 p.limb([(14, 25.5 - L), (9, 30 - L)], 6.4, 5.6, shin, bias=0.3, group=11)]
    R["fhoof"] = p.poly([(4.5, 29.5 - L), (9, 27.5 - L), (12, 31 - L), (8.5, 34.5 - L), (4.5, 33.5 - L)],
                        stone, bias=0.2, group=12)
    # the thick, muscled fish tail down to the split fin on the stone
    tpath = SEIS_TAIL
    R["tail"] = p.limb(tpath, 16, 8, hide, group=1)
    R["sfin"] = [p.lens((50, 54.5), (38.5, 57.5), 7.4, sfin, bend=-1.2, group=40),
                 p.lens((51.5, 54.5), (62, 53), 7, sfin, bend=1.2, group=41)]
    # body: deep chest, short barrel
    R["body"] = [p.blob(26, 35, 11.4, 10.4, hide, group=1),
                 p.blob(36, 40, 9.4, 8.2, hide, ang=25, group=1)]
    R["neck"] = p.limb([(29, 32), (26, 24), (21.5, 17 - L)], 16, 13, hide, group=1)
    R["belly"] = p.limb(bez3((15.5, 25 - L), (16, 38), (27, 47), (42, 49), n=12), 5, 6, foam,
                        clip=R["body"] + [R["neck"], R["tail"]], group=1)
    # head: heavy, nose down, nostrils flared
    R["head"] = [p.blob(20, 14.5 - L, 7.8, 7.4, hide, group=3),
                 p.limb(bez((17, 17 - L), (12, 19 - L), (8, 22 - L)), 8, 5.4, hide, group=3)]
    p.blob(9, 24 - L, 4.2, 1.6, foam, clip=R["head"], group=3)
    R["ear"] = p.lens((23, 8 - L), (26, 2.5 - L), 5, hide, bend=-0.6, group=36)
    # near foreleg: forearm thrust forward, heavy stone hoof
    R["leg"] = [p.limb([(27, 38), (14.5, 37)], 9, 7.6, hide, group=14),
                p.limb([(14.5, 37), (11, 44)], 7, 6, shin, group=15)]
    R["hoof"] = p.poly([(5.5, 44), (11, 42), (15, 45.5), (11.5, 49.5), (6, 48.5)], stone, group=16)
    return R


def seismare(p, view, phase):
    if view in ("front", "side", "icon"):
        L = phase
        seismare_parts(p, L)
        p.eye(17, 12 - L, 4, 5, iris="gold", shine="white")
        if p.big:
            p.pxs([(5, 20 - L), (6, 21 - L)], "ink")
            p.stroke([(7, 25 - L), (11, 25 - L)], "hide0")
            for a, b in (((6, 32 - L), (9, 30 - L)), ((8, 45), (11, 47)), ((34, 59), (41, 57)),
                         ((46, 60), (49, 57)), ((56, 57), (59, 59))):
                p.stroke([a, b], "terra")
        return

    if view == "back":
        p.poly([(2, 64), (7, 54), (18, 52), (26, 57), (30, 64)], stone)
        p.lens((14, 54), (4, 51), 7, sfin, bend=1)
        p.lens((15, 54), (27, 51), 8, sfin, bend=-1)
        p.poly([(14, 46), (18, 26), (24, 10), (34, 4), (44, 6), (40, 10), (34, 14), (30, 30), (28, 44)], wave)
        p.limb(bez((24, 12), (30, 3), (42, 7)), 3.6, 2, foam)
        p.limb(bez3((31, 18), (24, 16), (23, 25), (29, 26)), 3, 2, foam)
        p.blob(28, 62, 24, 16, hide, group=1)
        p.limb([(14, 64), (15, 55)], 12, 9, hide, group=5)
        p.limb([(36, 52), (40, 38), (45, 26)], 17, 14, hide, group=1)
        p.blob(46, 18, 9, 8, hide, group=3)
        p.blob(56, 24, 7, 5, hide, ang=25, group=3)
        p.lens((44, 11), (40, 2), 5, hide, bend=0.5)
        p.eye(48, 15, 4, 4, iris="gold", shine="white", shine_at=(1, 1))
        if p.big:
            p.px(61, 23, "ink")
        return

    if view == "up":
        # walking away: the wave towers off the back of the neck, ears either
        # side of it, broad hips, the thick tail down to its fin on stone
        p.poly([(13, 62.5), (18, 57.5), (46, 57.5), (51, 62.5)], stone)
        p.limb([(20.5, 44), (19.5, 52 - 2 * phase)], 6.6, 5.6, shin, bias=0.3, group=10)
        p.limb([(43.5, 44), (44.5, 52 - 2 * (1 - phase))], 6.6, 5.6, shin, bias=0.3, group=11)
        p.lens((25, 22), (18.5, 12), 5.6, hide, bend=0.5)
        p.lens((39, 22), (45.5, 12), 5.6, hide, bend=-0.5)
        p.blob(32, 25, 10.4, 7.8, hide, group=3)
        p.limb([(32, 29), (32, 36)], 15, 18, hide, group=1)
        p.blob(32, 42, 16, 9.8, hide, group=1)
        p.poly([(25, 42), (23, 28), (25, 16), (32, 8), (39, 13), (37.5, 10.5), (41.5, 16), (41, 28), (39, 42), (32, 45)], wave)
        p.poly([(25, 16), (32, 8), (39, 13), (35.5, 12.5), (32, 11.5), (28, 14)], foam)
        p.limb([(32, 48), (32, 55)], 14, 8, hide, group=5)
        p.lens((32, 57), (18, 55), 7.6, sfin, bend=1)
        p.lens((32, 57), (46, 55), 7.6, sfin, bend=-1)
        p.circle(17 + phase * 2, 59, 1.5, stone, noline=True)
        p.circle(48 - phase * 2, 60 - phase * 2, 1.4, stone, noline=True)
        return

    if view == "down":
        # stamping toward us: a long horse face, the wave rising behind on its
        # right and breaking over the top of the head to the left
        step = phase
        p.poly([(37, 36), (44, 27), (46, 17), (42, 8), (35, 4.5), (27, 5), (21.5, 8.5), (19.5, 13.5), (22, 17.5),
                (24.5, 12.5), (29, 9.5), (35, 10.5), (38.5, 16), (38, 26)], wave)
        p.poly([(21.5, 8.5), (27, 5), (35, 4.5), (42, 8), (37.5, 8), (30, 7.5), (24, 10.5), (20.5, 13)], foam)
        p.limb(bez((42, 10), (48, 22), (39, 34)), 2, 1.4, Mat(["gold"]), group=32)
        p.blob(32, 42, 12, 9, hide, group=1)
        p.blob(32, 44, 6, 6.4, foam, group=1)
        p.limb([(26, 47), (25.5, 56 - 2 * step)], 6.4, 5.6, shin, group=12)
        p.limb([(38, 47), (38.5, 56 - 2 * (1 - step))], 6.4, 5.6, shin, group=13)
        p.blob(25.5, 58 - 2 * step, 4, 2.6, stone)
        p.blob(38.5, 58 - 2 * (1 - step), 4, 2.6, stone)
        p.lens((26.5, 17), (23.5, 9.5), 4.6, hide, bend=0.5)
        p.lens((37.5, 17), (40.5, 9.5), 4.6, hide, bend=-0.5)
        p.blob(32, 21.5, 8, 6.4, hide, group=3)
        p.limb([(32, 24), (32, 33)], 11, 8, hide, group=3)
        p.blob(32, 33, 5, 3.4, hide, group=4)
        p.eye(25, 20, 3, 3, iris="gold", shine="white")
        p.eye(36, 20, 3, 3, iris="gold", shine="white", shine_at=(1, 0))
        p.pxs([(30, 34), (34, 34)], "ink")
        p.circle(20 + step * 2, 60 - step * 2, 1.6, stone, noline=True)
        p.circle(44 - step * 2, 60, 1.4, stone, noline=True)
        return


MONS = [
    Mon("Hipling", HIPLING_COLORS, HIPLING_SHINY, hipling, foot="hoof", icon_pal=3),
    Mon("Thalamare", THALAMARE_COLORS, THALAMARE_SHINY, thalamare, foot="hoof", icon_pal=3),
    Mon("Seismare", SEISMARE_COLORS, SEISMARE_SHINY, seismare, foot="hoof", icon_pal=3),
]
