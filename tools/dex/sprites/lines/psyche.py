"""Psyche line: Kampillar, Nymveil, Psychora (early Bug). Psyche, the soul
that is also a butterfly, and her bridal procession to the crag."""
import math

import numpy as np
from scipy import ndimage

from mon_lib import C, Mat, Mon, bez, ellipse_pts

INK = C.ink


def _ring(p, poly, inset):
    """The outer band of a polygon, `inset` design px wide, as a mask."""
    m = p.mask(poly)
    k = max(1, int(round(inset * p.s)))
    return m & ~ndimage.binary_erosion(m, iterations=k)


# --------------------------------------------------------------------------
# Kampillar, the soul caterpillar
# --------------------------------------------------------------------------

KAMPILLAR_COLORS = [
    ("ink", INK),
    ("ol0", (48, 72, 32)), ("ol1", (88, 120, 40)), ("ol2", (136, 168, 56)), ("ol3", (184, 208, 104)),
    ("sv0", (128, 152, 120)), ("sv1", (184, 200, 168)), ("sv2", (232, 240, 216)),
    ("marble", (208, 200, 184)), ("white", C.white),
    ("gl0", (96, 160, 168)), ("gl1", (168, 216, 232)), ("gl2", (232, 248, 248)),
    ("mouth", (104, 56, 48)),
]
KAMPILLAR_SHINY = {
    # a pale silver-leaf body with a sun-gold glow inside
    "ol0": (96, 112, 104), "ol1": (152, 168, 152), "ol2": (192, 208, 192), "ol3": (224, 232, 216),
    "sv0": (128, 136, 136), "sv1": (200, 208, 200), "sv2": (240, 240, 232),
    "gl0": (192, 144, 56), "gl1": (240, 200, 88), "gl2": (248, 240, 176),
}

k_body = Mat(["ol0", "ol1", "ol2", "ol3"], line="sv1", cuts=[0.16, 0.42, 0.7])
k_head = Mat(["ol0", "ol1", "ol2", "ol3"], line="ol0", cuts=[0.16, 0.42, 0.7])
k_band = Mat(["sv0", "sv1", "sv2"], line="sv0", cuts=[0.4, 0.7])
k_foot = Mat(["ol0", "ol1"], cuts=[0.5])
k_glow = Mat(["gl0", "gl1", "gl2"], cuts=[0.3, 0.6])


def _kband(p, x, y, h, ang, **kw):
    """A silver-leaf band at a segment joint: a thin upright lens."""
    a = math.radians(ang)
    dx, dy = math.sin(a) * h / 2, -math.cos(a) * h / 2
    return p.lens((x - dx, y - dy), (x + dx, y + dy), 1.7, k_band, **kw)


def kampillar(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        hump = 1 if (phase == 1 and view == "side") else 0
        # prolegs under the ground segments, true legs under the raised chest
        for x in (33.5, 39.5, 44.5):
            p.rect(x - 1, 58.5, x + 0.4, 59.5, k_foot, bias=0.25)
        p.rect(24.5, 49.5, 25.5, 50.5, k_foot, bias=0.25)
        # segments, tail first so each one overlaps the one behind it; the
        # joint lines are the silver-leaf bands
        segs = [
            (49.4, 52.4 - hump, 2.5, 2.6),
            (45.6, 54.6 - hump, 3.9, 4.0),
            (40.6, 54.4 - 2 * hump, 4.9, 5.1),
            (35.0, 53.6 - 2 * hump, 5.4, 5.7),
            (29.6, 50.8 - hump, 5.1, 5.3),
            (26.0, 45.6 - L, 4.6, 4.8),
        ]
        segpids = []
        for i, (x, y, rx, ry) in enumerate(segs):
            segpids.append(p.blob(x, y, rx, ry, k_body, group=10 + i))
        # the soul glowing through the middle of the body
        if p.big:
            p.blob(35.5, 54, 3.2, 2.8, k_glow, clip=segpids, group=30, nooutline=True, noline=True, bias=0.1)
        # the head, big and round, raised and curious, a small snout under it
        p.blob(17.5, 43.2 - L, 3.2, 2.4, k_head, group=21, bias=0.12)
        p.blob(21.2, 37.5 - L, 7.8, 7.4, k_head, group=20)
        if p.big:
            # eye-spots: marble rings with ink pupils
            p.patch(19, 35 - L, [
                ".mmmm.",
                "mm11mm",
                "m1a11m",
                "m1111m",
                "m1111m",
                ".m11m.",
                "..mm..",
            ], {"m": "marble", "1": "ink", "a": "white"})
            p.patch(14, 36 - L, [
                ".m",
                "m1",
                "m1",
                "m1",
                ".m",
            ], {"m": "marble", "1": "ink"})
            p.stroke([(16, 46 - L), (18, 47 - L)], "mouth")
        else:
            p.px(20, 38 - L, "ink")
            p.px(15, 38 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the raised chest and head from behind, head in
        # right profile, the glow showing through the back
        segs = [(8, 62, 10, 9), (20, 58, 10.5, 10), (31, 50, 9, 9.2)]
        pids = []
        for i, (x, y, rx, ry) in enumerate(segs):
            pids.append(p.blob(x, y, rx, ry, k_body, group=10 + i))
        p.blob(19, 57, 5, 4.4, k_glow, clip=pids, group=30, nooutline=True, noline=True, bias=0.1)
        p.blob(47.5, 45.5, 3.6, 3, k_head, group=21, bias=0.12)
        p.blob(40, 38, 10, 9.6, k_head, group=20)
        if p.big:
            p.patch(42, 32, [
                ".mmmmm.",
                "mm111mm",
                "m1111wm",
                "m11111m",
                "m11111m",
                "m11111m",
                ".m111m.",
                "..mmm..",
            ], {"m": "marble", "1": "ink", "w": "white"})
            p.stroke([(48, 47), (50, 46)], "mouth")
        return

    if view in ("down", "up"):
        # follower inching toward / away from the camera; the glow pulses
        hump = phase
        if view == "up":
            p.blob(32, 37 - hump, 7.6, 7, k_head, group=20)
            p.blob(32, 45 - hump, 6.6, 5.4 + hump, k_body, group=11)
            p.blob(32, 52, 6.6, 5.4, k_body, group=12)
            p.blob(32, 57, 4.4, 3.2, k_body, group=13)
            p.blob(32, 49 - hump, 3, 2.6 + hump, k_glow, group=30, nooutline=True, noline=True)
        else:
            p.blob(32, 42 - hump, 6.4, 5 + hump, k_body, group=11)
            p.blob(32, 48, 5.6, 4.2, k_body, group=12)
            p.blob(32, 43 - hump, 2.6, 2.4 + hump, k_glow, group=30, nooutline=True, noline=True)
            p.blob(32, 52, 8, 7, k_head, group=20)
            p.blob(32, 57.4, 3.4, 1.8, k_head, group=21, bias=0.15)
            p.patch(26, 49, ["mm", "m1", "11", "m1"], {"m": "marble", "1": "ink"},
                    small=(27, 50, ["1"]))
            p.patch(36, 49, ["mm", "1m", "11", "1m"], {"m": "marble", "1": "ink"},
                    small=(36, 50, ["1"]))
            if p.big:
                p.stroke([(31, 58), (33, 58)], "mouth")
        return


# --------------------------------------------------------------------------
# Nymveil, the veiled chrysalis
# --------------------------------------------------------------------------

NYMVEIL_COLORS = [
    ("ink", INK),
    ("sh0", (80, 96, 64)), ("sh1", (128, 144, 96)), ("sh2", (176, 192, 136)), ("sh3", (216, 224, 184)),
    ("v0", (96, 104, 152)), ("v1", (160, 168, 200)), ("v2", (216, 216, 216)), ("v3", (248, 248, 240)),
    ("gold0", C.sungold[0]), ("gold", C.sungold[1]),
    ("gl1", (168, 216, 232)),
]
NYMVEIL_SHINY = {
    # a sun-gold shell under a marble veil
    "sh0": (152, 96, 32), "sh1": (200, 144, 40), "sh2": (240, 192, 64), "sh3": (248, 232, 144),
    "gold0": (48, 104, 176), "gold": (112, 168, 224),
}

n_shell = Mat(["sh0", "sh1", "sh2", "sh3"], line="v0", cuts=[0.18, 0.44, 0.72])
n_veil = Mat(["v0", "v1", "v2", "v3"], line="v0", cuts=[0.2, 0.45, 0.72])


n_gold = Mat(["gold0", "gold"], cuts=[0.5])
n_face = Mat(["sh0", "sh1"], line="v0", cuts=[0.6])

NYM_OUTER = [(31, 9.6), (33, 11), (35.5, 13), (37.6, 16), (38.6, 20), (38.6, 24), (40, 28), (40.6, 31.5),
             (39.4, 34.5), (36.8, 37.6), (38.2, 40.5), (41, 45), (43.4, 49.5), (45, 53), (19.4, 53.4),
             (19.2, 51.4), (20.6, 47.5), (23, 43), (25.4, 38.8), (25.2, 36.2), (22.6, 32.5), (22.4, 28.5),
             (23.6, 24.5), (23.8, 19.5), (25.2, 15.5), (27.6, 12.4), (29.4, 10.6)]
NYM_GOWN = [(23, 25), (31, 25), (32, 30), (33, 36), (33, 41), (35, 48), (36, 50.4), (20.6, 50.4), (23, 43),
            (25.4, 38.8), (25.2, 36.2), (22.6, 32.5), (22.4, 28.5)]


def nymveil(p, view, phase):
    """The hand-finished battle art is the reference; this draft gives the
    icon and follower frames the same bride: hood and veil, gown, hem."""
    if view in ("front", "side", "icon"):
        sw = 1.0 if (phase == 1 and view != "icon") else 0.0
        p.stroke([(30, 1), (30, 9)], "v1")
        outer = [(x + (sw if y > 40 and x > 32 else 0), y) for x, y in NYM_OUTER]
        p.poly(outer, n_veil, group=3)
        p.poly(NYM_GOWN, n_shell, group=1)
        p.blob(28.6, 20, 3.4, 4.2, n_face, group=4)
        p.rect(20, 50, 44, 52, Mat(["v1", "v2", "v3"], cuts=[0.4, 0.7]), group=5)
        p.poly([(28.4, 52), (31.2, 52), (30, 56.6)], n_shell, group=6)
        if p.big:
            p.eye(27, 19, 2, 2, shine="gold", shine_at=(1, 1))
            p.eye(30, 19, 2, 2, shine="gold", shine_at=(1, 1))
            p.stroke([(27, 13), (30, 13), (32, 12)], "gold")
        else:
            p.px(28, 19, "gold")
            p.px(31, 19, "gold")
            p.stroke([(27, 13), (31, 13)], "gold")
        return

    if view == "back":
        p.stroke([(38, 1), (38, 8)], "v1")
        p.poly([(44, 26), (50, 28), (54, 34), (55.5, 44), (57, 56), (58, 64), (46, 64), (46, 40)], n_shell, group=1)
        p.poly([(36.5, 8.6), (40, 8.2), (44, 10), (47.5, 13.5), (49.4, 18), (49.6, 22), (48, 25.5), (50, 29),
                (51.5, 36), (52.4, 46), (53.6, 56), (54.4, 64), (16, 64), (18.4, 54), (21.6, 44), (25.4, 35),
                (29, 28.5), (30.4, 22), (31.4, 15.5), (33.6, 11)], n_veil, group=3)
        if p.big:
            p.eye(47, 17, 2, 2, shine="gold", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        hop = phase
        y = -2 * hop
        p.stroke([(32, 1), (32, 9 + y)], "v1")
        outer = [(32 + (x - 31) * 1.0, yy + y) for x, yy in NYM_OUTER]
        outer = [(x, yy) for x, yy in outer]
        sym = []
        for x, yy in NYM_OUTER:
            sym.append((32 - abs(x - 31.6) * 1.0 if x < 31.6 else 32 + abs(x - 31.6), yy + y))
        p.poly([(32, 9.6 + y), (36.5, 13 + y), (39, 20 + y), (39, 25 + y), (41, 31 + y), (37.4, 37.6 + y),
                (41, 45 + y), (44.6, 53 + y), (19.4, 53 + y), (23, 45 + y), (26.6, 37.6 + y), (23, 31 + y),
                (25, 25 + y), (25, 20 + y), (27.5, 13 + y)], n_veil, group=3)
        if view == "down":
            p.poly([(28, 25 + y), (36, 25 + y), (35, 36 + y), (37, 50 + y), (27, 50 + y), (29, 36 + y)], n_shell,
                   group=1)
            p.blob(32, 20 + y, 3.6, 4.2, n_face, group=4)
            p.eye(29.5, 19 + y, 2, 2, shine="gold", shine_at=(1, 1))
            p.eye(33.5, 19 + y, 2, 2, shine="gold", shine_at=(1, 1))
        p.rect(20, 50 + y, 44, 52 + y, Mat(["v1", "v2", "v3"], cuts=[0.4, 0.7]), group=5)
        p.stroke([(28, 13 + y), (36, 13 + y)], "gold")
        return


# --------------------------------------------------------------------------
# Psychora, the soul butterfly
# --------------------------------------------------------------------------

PSYCHORA_COLORS = [
    ("ink", INK),
    ("lm0", (128, 96, 64)), ("lm1", (176, 144, 96)), ("lm2", (208, 184, 136)), ("lm3", (232, 216, 176)),
    ("aeg0", (48, 104, 176)), ("aeg1", (112, 168, 224)), ("aeg2", (176, 216, 240)),
    ("wing", (216, 216, 208)), ("white", C.white), ("silver", (176, 192, 168)),
    ("gold0", C.sungold[0]), ("gold", C.sungold[1]), ("aegd", (24, 56, 120)), ("lmd", (88, 56, 40)),
]
PSYCHORA_SHINY = {
    # soft terracotta wings with Aegean-blue eye-spots
    "aeg0": (184, 88, 48), "aeg1": (224, 136, 88), "aeg2": (240, 184, 144), "aegd": (120, 48, 24),
    "wing": (248, 224, 200), "silver": (232, 184, 152),
    "gold0": (48, 104, 176), "gold": (112, 168, 224),
}

ps_body = Mat(["lm0", "lm1", "lm2", "lm3"], line="lm0", cuts=[0.16, 0.42, 0.7])
ps_wing = Mat(["silver", "wing", "white"], line="silver", cuts=[0.3, 0.62])
ps_edge = Mat(["aegd", "aeg0", "aeg1", "aeg2"], line="aeg0", cuts=[0.2, 0.42, 0.66])


def _wing(p, poly, edge=4.6, root=None, **kw):
    """A gauzy wing: marble inside, an Aegean margin away from the root."""
    pid = p.poly(poly, ps_wing, **kw)
    band = _ring(p, poly, edge)
    if root is not None:
        yy, xx = np.mgrid[0:p.H, 0:p.W]
        rx, ry = p.pt(*root)
        band &= np.hypot(xx + 0.5 - rx, yy + 0.5 - ry) > 9 * p.s
    p.add(band, ps_edge, clip=[pid], group=kw.get("group", pid), noline=True, bias=kw.get("bias", 0.0))
    return pid


def _eyespot(p, cx, cy, r):
    """A sun-gold eye-spot ringed in ink, with a dark pupil and a shine."""
    if not p.big:
        p.px(cx, cy, "gold")
        if p.s > 0.45:
            p.px(cx + 1, cy, "ink")
        return
    R = int(r) + 1
    for y in range(-R, R + 1):
        for x in range(-R, R + 1):
            d = math.hypot(x, y)
            if d <= r:
                c = "ink" if d > r - 1.1 else ("gold0" if (x + y) > 0.5 else "gold")
                if d <= 1.6:
                    c = "ink"
                p.px(cx + x, cy + y, c)
    p.px(cx - 1, cy - 1, "white")


# wing and body outlines shared by the draft views (the battle art matches)
PS_FW_HI = [(21, 25), (17, 17), (12, 11), (7, 7), (3.5, 8), (3, 12), (5, 17), (9, 21.5), (15, 25.5), (20, 27)]
PS_FW_LO = [(20.5, 29), (15, 31), (10, 35), (7.5, 39.5), (8.5, 43), (11, 43), (13, 47), (15.5, 43.5), (19, 36)]
PS_NW_LO = [(27, 31), (34, 31.5), (42, 33), (49, 36.5), (52.5, 41), (51.5, 45), (47.5, 46), (44.5, 50),
            (43, 55.5), (40, 56.5), (38, 52), (34.5, 46), (30, 39), (26.5, 33)]
PS_NW_HI = [(25.5, 28), (28, 19), (33, 12), (40, 6.5), (48, 4), (55, 4.5), (59.5, 7.5), (60, 13), (57.5, 20),
            (53, 26), (46, 30.5), (37, 32), (29, 31)]


def psychora(p, view, phase):
    if view in ("front", "side", "icon"):
        up = 2 if (phase == 1 and view != "icon") else 0
        lift = lambda poly: [(x, y - up if y < 20 else y) for x, y in poly]
        _wing(p, PS_FW_LO, root=(20, 31), group=40, bias=0.15)
        _wing(p, lift(PS_FW_HI), root=(21, 26), group=41, bias=0.15)
        _wing(p, PS_NW_LO, root=(27, 33), group=42)
        _wing(p, lift(PS_NW_HI), root=(26.5, 29), group=43)
        p.poly([(21.2, 33), (20.8, 39), (21.4, 45), (22.8, 50.5), (24.2, 53.6), (25.6, 50.5), (26.8, 45),
                (27.4, 39), (26.8, 33)], ps_body, group=1)
        p.blob(24, 29.6, 4.0, 4.4, ps_body, group=1)
        p.blob(22, 25.4, 6.4, 3.0, Mat(["wing", "white"], line="lm2", cuts=[0.5]), group=2, ang=-10)
        p.blob(18.4, 17.2 - phase, 6.8, 6.3, ps_body, group=3)
        if p.big:
            p.stroke([(16, 10), (13, 7), (10, 5), (9, 6), (10, 8)], "ink")
            p.stroke([(21, 10), (24, 7), (27, 5), (28, 6), (27, 8)], "ink")
            p.eye(17, 15, 4, 5, iris="aegd", shine="white", shine_at=(1, 1))
            p.eye(14, 15, 2, 4, shine="white", shine_at=(1, 1))
            _eyespot(p, 44, 17 - up, 5.4)
        else:
            p.px(17, 17 - phase, "ink")
            _eyespot(p, 44, 17 - up, 5.4)
        return

    if view == "back":
        _wing(p, [(44, 34), (47, 24), (52, 15), (57, 10), (60.5, 12), (60.5, 20), (57, 28), (50, 35)],
              root=(45, 36), group=40, bias=0.15)
        _wing(p, [(36, 44), (28, 45), (18, 48), (9, 53), (5, 58), (6, 64), (34, 64), (37, 52)], root=(36, 47),
              group=41)
        _wing(p, [(37, 38), (32, 30), (24, 20), (15, 11), (8, 5), (3.5, 5), (2.2, 10), (3, 19), (7, 28), (14, 36),
                  (24, 42), (34, 44)], root=(36, 40), group=42)
        p.poly([(34, 44), (33, 52), (33.4, 64), (44, 64), (44, 52), (43, 44)], ps_body, group=1)
        p.blob(39, 39, 6.2, 6.6, ps_body, group=1)
        p.blob(45, 22, 8.2, 7.6, ps_body, group=3)
        if p.big:
            p.eye(48, 17, 4, 5, iris="aegd", shine="white", shine_at=(1, 1))
            _eyespot(p, 16, 18, 6.2)
        return

    if view in ("down", "up"):
        flap = phase
        for sgn in (-1, 1):
            hi = [(32 + sgn * 2, 30), (32 + sgn * 9, 20 + 2 * flap), (32 + sgn * 18, 13 + 3 * flap),
                  (32 + sgn * 26, 16 + 3 * flap), (32 + sgn * 26, 26), (32 + sgn * 18, 33), (32 + sgn * 4, 35)]
            lo = [(32 + sgn * 3, 36), (32 + sgn * 12, 38), (32 + sgn * 18, 45), (32 + sgn * 14, 52),
                  (32 + sgn * 8, 50), (32 + sgn * 3, 42)]
            _wing(p, lo, root=(32, 37), group=42 + sgn)
            _wing(p, hi, root=(32, 32), group=44 + sgn)
            if view == "down":
                _eyespot(p, 32 + sgn * 17, 23 + 2 * flap, 4.2)
        p.limb([(32, 36), (32, 51)], 5, 2.4, ps_body, group=1)
        p.blob(32, 33, 3.8, 4, ps_body, group=1)
        p.blob(32, 25, 6, 5.4, ps_body, group=3)
        if p.big:
            p.stroke([(30, 20), (27, 13), (25, 12)], "ink")
            p.stroke([(34, 20), (37, 13), (39, 12)], "ink")
        if view == "down":
            p.eye(28, 23, 3, 4, iris="aegd", shine="white")
            p.eye(34, 23, 3, 4, iris="aegd", shine="white")
        return


MONS = [
    Mon("Kampillar", KAMPILLAR_COLORS, KAMPILLAR_SHINY, kampillar, foot="blank", icon_pal=5),
    Mon("Nymveil", NYMVEIL_COLORS, NYMVEIL_SHINY, nymveil, foot="blank", icon_pal=4),
    Mon("Psychora", PSYCHORA_COLORS, PSYCHORA_SHINY, psychora, foot="blank", icon_pal=4),
]
