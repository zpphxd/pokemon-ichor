"""Smoliv's native opening redraw: an olive baby, not an Aethos dex entry.

SMOLIV is deliberately not exported in MONS: its species data remains upstream.
Build this drawing with tools/dex/sprites/smoliv.py.
"""
from mon_lib import C, Mat, Mon


COLORS = [
    ("ink", C.ink),
    ("body0", (96, 120, 40)), ("body1", (144, 168, 64)),
    ("body2", (192, 208, 96)), ("body3", (224, 232, 144)),
    ("leaf0", (32, 64, 32)), ("leaf1", (56, 104, 40)),
    ("leaf2", (96, 144, 56)), ("leaf3", (152, 184, 88)),
    ("fruit0", (96, 80, 32)), ("fruit1", (152, 136, 48)),
    ("fruit2", (192, 184, 72)), ("fruit3", (232, 216, 112)),
    ("white", C.white), ("oil", (248, 240, 176)),
]
SHINY = {
    "fruit0": (40, 32, 48), "fruit1": (64, 48, 72),
    "fruit2": (96, 80, 104), "fruit3": (152, 128, 152),
    "oil": (208, 184, 208),
}
BODY = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.2, 0.44, 0.72])
LEAF = Mat(["leaf0", "leaf1", "leaf2", "leaf3"], line="leaf0", cuts=[0.2, 0.44, 0.72])
FRUIT = Mat(["fruit0", "fruit1", "fruit2", "fruit3"], line="fruit0", cuts=[0.18, 0.42, 0.72])
FOOT = Mat(["body0", "body1", "body2"], line="body0", cuts=[0.3, 0.65])
FOOTPRINT = [
    "................", "................", "................", "................",
    "................", ".....##..##.....", "....###..###....", "....###..###....",
    "....###..###....", ".....##..##.....", "................", "................",
    "................", "................", "................", "................",
]


def leaf(p, a, b, width, bend, group=10, far=False):
    pid = p.lens(a, b, width, LEAF, bend=bend, group=group, bias=0.2 if far else 0)
    if p.big:
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        p.stroke([a, mid], "leaf0")
        p.px(mid[0] - 1, mid[1] - 1, "leaf3")
    return pid


def fruit(p, x, y, scale=1):
    p.blob(x, y, 5.4 * scale, 7.4 * scale, FRUIT, ang=-12, group=12)
    if p.big:
        p.stroke([(x - 2, y - 4), (x - 3, y - 2)], "oil")
        p.px(x, y - 6, "fruit3")


def smoliv(p, view, phase):
    if view in ("front", "side", "icon"):
        step = phase if view == "side" else 0
        sway = phase
        # Far foot, then the rounded seed-shaped body; no arms or muzzle.
        p.blob(36 + step, 49 - step, 2.8, 2.3, FOOT, group=3, bias=0.2)
        p.blob(32, 41, 10.4, 10.2, BODY, ang=-8, group=1)
        p.blob(31, 34, 7.6, 8.2, BODY, ang=-10, group=1)
        p.blob(27 - step, 49 - (1 - step), 3.2, 2.3, FOOT, group=2)
        fruit(p, 32 + sway, 20 - sway)
        leaf(p, (32, 29), (47, 24 + sway), 5.8, 1.2, far=True)
        leaf(p, (31, 29), (17, 23 - 2 * sway), 6.6, -1.4)
        leaf(p, (32, 30), (25 + sway, 33), 5, -0.6, group=11)
        if view == "side":
            p.eye(24, 38, 3, 4, shine="white")
        elif phase and view == "front" and p.big:
            p.stroke([(23, 39), (24, 40), (25, 39)], "ink")
            p.eye(33, 37, 4, 5, shine="white")
        else:
            p.eye(23, 38, 3, 4, shine="white")
            p.eye(33, 37, 4, 5, shine="white")
        if p.big:
            p.stroke([(27, 44), (28, 45), (29, 44), (30, 45), (31, 44)], "body0")
            p.stroke([(25, 34), (25, 35), (24, 36)], "body3")
            p.pxs([(24, 46), (25, 47)], "body2")
            p.pxs([(35, 45), (36, 44)], "body1")
        else:
            p.px(28, 44, "body0")
        return

    if view == "back":
        p.blob(33, 64, 20, 25, BODY, group=1)
        p.blob(39, 46, 12, 16, BODY, group=1)
        fruit(p, 41, 19, 1.15)
        leaf(p, (41, 30), (58, 25), 7.4, 1.2, far=True)
        leaf(p, (40, 31), (18, 24), 8.2, -1.6)
        leaf(p, (41, 32), (29, 38), 6.4, -1.0, group=11)
        p.eye(45, 42, 3, 5, shine="white", shine_at=(1, 1))
        if p.big:
            p.stroke([(45, 49), (46, 50), (47, 49)], "body0")
            p.stroke([(18, 51), (22, 48), (26, 49)], "body3")
            p.stroke([(35, 52), (37, 56), (36, 60)], "body1")
        return

    if view in ("down", "up"):
        back = view == "up"
        for x, st in ((27, phase), (37, 1 - phase)):
            p.blob(x, 51 - 2 * st, 3, 2.4, FOOT, group=2 if x < 32 else 3)
        p.blob(32, 41, 10.4, 10.4, BODY, group=1)
        p.blob(32, 34, 7, 7.6, BODY, group=1)
        fruit(p, 33 + phase if back else 32 - phase, 20, 0.95)
        leaf(p, (32, 29), (17, 23 + 2 * phase), 6.2, -1.1)
        leaf(p, (32, 29), (47, 25 - 2 * phase), 5.8, 1.1, far=True)
        leaf(p, (32, 30), (37, 34) if back else (27, 33), 4.6, 0.8, group=11)
        if not back:
            p.eye(25, 38, 3, 4, shine="white")
            p.eye(35, 38, 3, 4, shine="white")
            p.px(31, 44, "body0")
        return


SMOLIV = Mon("Smoliv", COLORS, SHINY, smoliv, foot=FOOTPRINT, icon_pal=1)
