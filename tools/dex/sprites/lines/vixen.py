"""Vixen line: Kerdovix (Dark/Fairy). The Teumessian vixen, fated never to be
caught, turned to stone mid-chase with the hound Laelaps. It is Skylaps's
mirror (lines/laelaps.py): the same frame in the same stride, its colors
swapped, so this module draws its body with the hound's stride."""
import importlib.util
import os

import math

from mon_lib import C, Mat, Mon, bez, bez3, ribbon

_spec = importlib.util.spec_from_file_location("_laelaps_stride", os.path.join(os.path.dirname(__file__), "laelaps.py"))
_hound = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hound)
LIGHT, DARK, GOLD, MARBLE, STONE = _hound.LIGHT, _hound.DARK, _hound.GOLD, _hound.MARBLE, _hound.STONE
stride_body = _hound.stride_body

INK = C.ink

KERDOVIX_COLORS = [
    ("ink", INK),
    # black-figure ink coat: the hound's shiny
    ("coat0", DARK[0]), ("coat1", DARK[1]), ("coat2", DARK[2]), ("coat3", DARK[3]),
    # the starlit tail, and the white of the muzzle
    ("star0", MARBLE[0]), ("star1", MARBLE[1]), ("star2", MARBLE[2]), ("snow", C.white),
    # Fairy-pink eyes and star glints
    ("pink0", (208, 88, 144)), ("pink1", (248, 176, 208)),
    # the fading afterimages of the tail
    ("ghost", (104, 96, 144)),
    ("stone0", STONE[0]), ("stone1", STONE[1]), ("stone2", STONE[2]),
]
KERDOVIX_SHINY = {
    # pale marble and Aegean with a sun-gold tail: the hound's colors
    "coat0": LIGHT[0], "coat1": LIGHT[1], "coat2": LIGHT[2], "coat3": LIGHT[3],
    "star0": GOLD[0], "star1": GOLD[1], "star2": GOLD[2],
    "ghost": (176, 136, 72),
}

v_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="ink", cuts=[0.12, 0.3, 0.56])
v_star = Mat(["star0", "star1", "star2"], line="star0", cuts=[0.26, 0.58])
v_snow = Mat(["coat3", "snow"], line="coat2", cuts=[0.5])
v_ghost1 = Mat(["ghost", "star0"], line="coat3", outline="coat2", cuts=[0.5])
v_ghost2 = Mat(["coat2", "ghost"], line="coat2", outline="coat1", cuts=[0.55])
v_stone = Mat(["stone0", "stone1", "stone2"], line="stone0", cuts=[0.3, 0.64])

# the brush, a thick fox tail sweeping up behind her, and its two fading
# afterimages swung further up, where it was a moment ago
TAIL = bez3((46.5, 28.5), (53, 28), (58.5, 23), (59.5, 14.5))


def _rot(path, ang, about):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    ox, oy = about
    return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in path]


def _brush_w(W):
    def w(t):
        if t < 0.55:
            return W * (0.42 + 0.58 * math.sin(math.pi / 2 * t / 0.55))
        return W * ((1 - t) / 0.45) ** 0.75
    return w


def _brush(p, path, W, mat, **kw):
    return p.poly(ribbon(path, _brush_w(W)), mat, **kw)


def kerdovix(p, view, phase):
    # the battle front and back are hand-finished in the art files (the head,
    # the starlit brush and its afterimages redrawn there); this draft feeds
    # the icon and the follower
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        fl = 1 if phase == 1 else 0
        # the afterimages, fading, then the brush itself
        _brush(p, _rot(TAIL, -44 - 4 * fl, TAIL[0]), 10.0, v_ghost2, group=22)
        _brush(p, _rot(TAIL, -22 - 2 * fl, TAIL[0]), 10.5, v_ghost1, group=21)
        _brush(p, TAIL, 11.0, v_star, group=20)
        stride_body(p, v_coat, v_stone)
        # neck twisting up and back, the head turned over her shoulder
        p.limb(bez((23, 32), (21, 26), (22.5, 22 - L)), 9.0, 8.0, v_coat, group=2)
        # far ear, tall and pricked
        p.poly(bez3((17.5, 19 - L), (16.5, 13 - L), (17, 9.5 - L), (17.5, 7 - L)) + [(23.5, 15.5 - L)], v_coat, group=4,
               bias=0.2)
        p.blob(23, 19.5 - L, 6.4, 5.6, v_coat, group=3)
        # the white muzzle and cheek, pointing back at the hound
        p.limb(bez((26.5, 22 - L), (30, 23 - L), (33.5, 24.5 - L)), 5.6, 3.0, v_snow, group=5)
        p.blob(24.5, 24 - L, 4.8, 2.8, v_snow, group=5)
        # near ear, tall and pricked
        p.poly(bez3((23.5, 15.5 - L), (24.5, 10 - L), (26.5, 6 - L), (28, 5 - L)) + [(29, 11 - L), (29.5, 17 - L)],
               v_coat, group=6)
        if p.big:
            p.eye(25, 19 - L, 3, 3, iris="pink1", shine="snow", shine_at=(2, 0))
            p.pxs([(33, 23 - L), (34, 23 - L), (34, 24 - L)], "ink")
            for x, y in ((53, 22), (57, 19), (51, 26), (56, 25)):
                p.px(x, y, "pink1")
        else:
            p.px(26, 20 - L, "pink1")
        return

    if view == "back":
        # over the shoulder: the black back, the starlit brush and its
        # afterimages at the left, the head turned right in profile
        base = (16, 54)
        tail = bez3(base, (8, 50), (4, 40), (8, 26))
        _brush(p, _rot(tail, 34, base), 14, v_ghost2, group=22)
        _brush(p, _rot(tail, 17, base), 14.5, v_ghost1, group=21)
        _brush(p, tail, 15, v_star, group=20)
        p.blob(30, 61, 22, 12, v_coat, group=1)
        p.limb(bez((28, 54), (38, 48), (44, 40)), 17, 13, v_coat, group=1)
        p.poly([(40, 30), (40.5, 17), (47, 26)], v_coat, group=4, bias=0.2)
        p.limb(bez((42, 44), (46, 38), (48, 34)), 12, 10, v_coat, group=2)
        p.blob(49, 31, 7.2, 6.4, v_coat, group=3)
        p.limb(bez((53, 33), (57, 34.5), (61, 36)), 6.4, 3.6, v_snow, group=5)
        p.blob(51.5, 36, 5.0, 3.0, v_snow, group=5)
        p.poly([(45.5, 27), (49.5, 13.5), (53, 26.5)], v_coat, group=6)
        if p.big:
            p.eye(51, 29, 3, 3, iris="pink1", shine="snow", shine_at=(2, 0))
            p.pxs([(61, 35), (62, 35)], "ink")
            for x, y in ((9, 36), (12, 44), (7, 30), (14, 50)):
                p.px(x, y, "pink1")
        return

    if view in ("down", "up"):
        # follower: the vixen toward or away from the camera, her brush
        # swaying behind her
        st = phase
        if view == "down":
            _brush(p, bez3((34, 46), (42, 44), (45, 36), (44 + 2 * st, 27)), 8.0, v_star, group=20)
        p.blob(32, 47, 7.0, 7.6, v_coat, group=1)
        p.limb([(28, 50), (27.5, 59 - 2 * st)], 4.0, 3.2, v_coat, group=12)
        p.limb([(36, 50), (36.5, 59 - 2 * (1 - st))], 4.0, 3.2, v_coat, group=13)
        p.blob(27.5, 59.5 - 2 * st, 2.8, 1.8, v_coat if view == "down" else v_stone, group=12)
        p.blob(36.5, 59.5 - 2 * (1 - st), 2.8, 1.8, v_coat if view == "down" else v_stone, group=13)
        p.poly([(23, 36), (21.5, 24), (29, 32)], v_coat, group=4)
        p.poly([(41, 36), (42.5, 24), (35, 32)], v_coat, group=4)
        p.blob(32, 37, 7.0, 6.2, v_coat, group=3)
        if view == "down":
            p.blob(32, 42, 4.2, 3.4, v_snow, group=5)
            p.eye(27, 36, 2, 3, iris="pink1", shine="snow", shine_at=(0, 0))
            p.eye(35, 36, 2, 3, iris="pink1", shine="snow", shine_at=(1, 0))
            p.pxs([(31, 43), (32, 43)], "ink")
        else:
            _brush(p, _rot(bez3((32, 48), (33, 52), (36, 56), (40, 57)), -40 - 6 * st, (32, 48)), 8.0, v_ghost1, group=21)
            _brush(p, bez3((32, 48), (31, 53), (27, 57), (22 + st, 58)), 8.4, v_star, group=20)
        return


MONS = [
    Mon("Kerdovix", KERDOVIX_COLORS, KERDOVIX_SHINY, kerdovix, foot="paw"),
]
