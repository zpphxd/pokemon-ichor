"""Laelaps line: Skylaps (Electric). The storm-wind hound fated to catch
whatever it chased, set on the Teumessian vixen that could never be caught,
both turned to stone mid-chase. Kerdovix (lines/vixen.py) is its mirror: the
same frame in the same stride, with the coat colors swapped."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

# The paradox pair swap colors: the hound's coat is the vixen's shiny and the
# vixen's coat is the hound's shiny (lines/vixen.py uses the same values).
LIGHT = [(88, 104, 136), (136, 152, 184), (184, 200, 224), (232, 240, 248)]
DARK = [(48, 40, 48), (64, 56, 72), (88, 80, 104), (136, 128, 160)]
GOLD = [(192, 128, 32), (240, 192, 64), (248, 240, 168)]
MARBLE = [(160, 152, 168), (208, 200, 216), (248, 248, 240)]
STONE = [(96, 88, 80), (144, 136, 128), (192, 184, 168)]

SKYLAPS_COLORS = [
    ("ink", INK),
    ("coat0", LIGHT[0]), ("coat1", LIGHT[1]), ("coat2", LIGHT[2]), ("coat3", LIGHT[3]),
    # thundercloud ears, deep Aegean blue
    ("cloud0", (24, 48, 112)), ("cloud1", (48, 96, 168)), ("cloud2", (112, 160, 216)),
    # the bolt down its spine
    ("bolt0", GOLD[0]), ("bolt1", GOLD[1]), ("bolt2", GOLD[2]),
    # hind paws turning to stone
    ("stone0", STONE[0]), ("stone1", STONE[1]), ("stone2", STONE[2]),
]
SKYLAPS_SHINY = {
    # black-figure ink with marble-white lightning: the vixen's colors
    "coat0": DARK[0], "coat1": DARK[1], "coat2": DARK[2], "coat3": DARK[3],
    "bolt0": MARBLE[0], "bolt1": MARBLE[1], "bolt2": MARBLE[2],
}

s_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.7])
s_cloud = Mat(["cloud0", "cloud1", "cloud2"], line="cloud0", cuts=[0.3, 0.62])
s_bolt = Mat(["bolt0", "bolt1", "bolt2"], line="bolt0", cuts=[0.3, 0.62])
s_stone = Mat(["stone0", "stone1", "stone2"], line="stone0", cuts=[0.3, 0.64])

# The shared stride (vixen.py repeats these): a long-legged courser stretched
# mid-gallop, facing left. Legs are (hip, joint, ..., paw).
# The two phases of the gallop: the reach (phase 0, the near foreleg
# stretched forward, the near hind leg pushing off) and the gather (phase 1,
# the forelegs planted and folding, the hind legs swinging under).
STRIDES = {
    0: dict(near_fore=[(21.5, 35), (19, 43.5), (12.5, 51), (7.5, 55.5)],
            far_fore=[(26, 36), (27.5, 44.5), (25.5, 52), (23, 58.5)],
            near_hind=[(46, 33), (51, 40.5), (56, 48.5), (58, 58.5)],
            far_hind=[(43, 34), (39.5, 41), (44, 49), (40.5, 56)]),
    1: dict(near_fore=[(21.5, 35), (21, 43.5), (17, 51), (14, 58.5)],
            far_fore=[(26, 36), (30, 43), (32.5, 50), (30.5, 54)],
            near_hind=[(46, 33), (46.5, 41), (51, 49.5), (50, 58.5)],
            far_hind=[(43, 34), (38.5, 40.5), (40, 48.5), (35.5, 54.5)]),
}
NEAR_FORE, FAR_FORE = STRIDES[0]["near_fore"], STRIDES[0]["far_fore"]
NEAR_HIND, FAR_HIND = STRIDES[0]["near_hind"], STRIDES[0]["far_hind"]


def _leg(p, pts, widths, coat, stone=None, stone_from=None, **kw):
    """A jointed leg: one limb per segment, each tapering, so the joints
    (elbow, wrist, stifle, hock) read; segments from stone_from on are stone."""
    for i in range(len(pts) - 1):
        mat = stone if (stone_from is not None and i >= stone_from) else coat
        g = kw.get("group", 0) + (10 if mat is stone else 0)
        p.limb(pts[i:i + 2], widths[i], widths[i + 1], mat, **{**kw, "group": g})


def stride_body(p, coat, stone, phase=0):
    """The courser's legs and body, its lower hind legs turned to stone: a
    deep chest, a tucked waist, a muscled haunch, legs with real joints."""
    st = STRIDES[phase]
    fb = 0.3
    # far legs, in shade
    _leg(p, st["far_fore"], (7.0, 5.0, 3.8, 3.4), coat, bias=fb, group=10)
    p.blob(st["far_fore"][-1][0] - 1, st["far_fore"][-1][1] + 0.4, 3.0, 1.7, coat, bias=fb, group=10)
    _leg(p, st["far_hind"], (8.6, 5.6, 4.2, 3.6), coat, stone, stone_from=2, bias=fb, group=11)
    p.blob(st["far_hind"][-1][0] - 0.8, st["far_hind"][-1][1] + 0.5, 3.0, 1.7, stone, bias=fb, group=21)

    # body: a deep keel of a chest standing well off the ground, the waist
    # tucked up under an arched loin, clear air under the belly
    p.blob(22, 33.5, 8.4, 9.0, coat, group=1)
    p.limb(bez((26, 30.5), (35, 29), (43, 29.5)), 11.0, 8.6, coat, group=1)
    p.blob(35, 27.8, 6.6, 3.2, coat, group=1)
    p.blob(46, 31, 7.0, 6.6, coat, group=1)

    # near hind: a muscled thigh, the gaskin, then stone from the hock down
    p.blob(47.5, 34, 6.4, 7.2, coat, ang=-30, group=13)
    _leg(p, [(46, 32)] + st["near_hind"][1:], (9.0, 6.0, 4.6, 4.0), coat, stone, stone_from=2, group=13)
    p.blob(st["near_hind"][-1][0] + 0.2, st["near_hind"][-1][1] + 0.6, 3.2, 1.8, stone, group=25)
    # near fore: a muscled shoulder, the elbow, the reaching forearm
    p.blob(21, 35, 5.8, 6.2, coat, group=12)
    _leg(p, st["near_fore"], (8.4, 5.6, 4.2, 3.8), coat, group=12)
    nf = st["near_fore"][-1]
    p.blob(nf[0] - 1, nf[1] + 0.5, 3.3, 1.9, coat, group=12)


def _cloud(p, path, r0, r1, mat, group, bias=0.0):
    """A thundercloud tuft: puffs shrinking along path, each its own lobe."""
    n = len(path)
    for i, (x, y) in enumerate(path):
        t = i / max(n - 1, 1)
        p.circle(x, y, r0 + (r1 - r0) * t, mat, group=group + i, bias=bias)


# a lightning-bolt tail: a zigzag from the rump to a point
BOLT_TAIL = [(47.5, 27), (51, 22.4), (49.5, 21.4), (54.5, 17), (53, 16), (58, 11)]


def skylaps(p, view, phase):
    # the battle front and back are hand-finished in the art files (the head,
    # the cloud ears, the bolt and the stone redrawn there); this draft feeds
    # the icon and the follower
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        # the tail, a bolt of storm-gray fur
        p.limb(BOLT_TAIL, 5.6, 2.0, s_coat, group=20, cap=False)
        stride_body(p, s_coat, s_stone, phase if view == "front" else 0)
        # far ear, a thundercloud standing up and back
        p.lens((19.5, 14 - L), (24.5, 3.5 - L), 4.2, s_cloud, bend=-0.6, fat=0.35, group=40, bias=0.22)
        # the neck rising from the shoulders, the head held above the back
        p.limb(bez((25, 31), (21, 24), (17.5, 20 - L)), 9.4, 7.4, s_coat, group=2)
        p.blob(16.5, 19 - L, 5.4, 4.8, s_coat, group=3)
        p.limb(bez((12, 21 - L), (8, 21.8 - L), (3.5, 22.4 - L)), 5.4, 3.6, s_coat, group=3)
        # near ear
        p.lens((16.5, 15 - L), (19.5, 3 - L), 4.8, s_cloud, bend=-0.6, fat=0.35, group=50)
        # the bolt down the spine to the tail's tip
        p.stroke([(25, 27), (29, 26), (31, 27), (35, 26), (37, 27), (41, 26), (43, 27), (46, 26), (49, 25),
                  (51, 22), (52, 21), (55, 17), (56, 16), (58, 12)], "bolt1")
        if p.big:
            p.eye(13, 17 - L, 3, 3, shine="coat3", shine_at=(0, 0))
            p.pxs([(2, 22 - L), (2, 23 - L)], "ink")
            p.stroke([(4, 24 - L), (9, 24 - L)], "coat0")
        else:
            p.px(14, 18 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the long back with the bolt down its spine, the
        # bolt tail rising at the left, the head low and turned right in
        # profile along the trail, the cloud ears streaming back
        p.limb([(13, 54), (8, 47), (11.5, 44), (6.5, 37), (10, 34), (6, 27)], 7.6, 2.6, s_coat, group=20, cap=False)
        _cloud(p, [(47, 31), (42.5, 27), (38, 24.5), (34, 23.5)], 3.0, 1.6, s_cloud, 40, bias=0.24)
        p.blob(30, 61, 24, 11, s_coat, group=1)
        p.limb(bez((26, 56), (38, 50), (47, 44)), 17, 12, s_coat, group=1)
        p.limb(bez((45, 46), (49.5, 41), (51.5, 38)), 11.5, 9.0, s_coat, group=2)
        p.blob(52, 36.5, 6.6, 5.4, s_coat, group=3)
        p.limb(bez((55.5, 38), (59, 39.5), (62, 41)), 6.0, 4.0, s_coat, group=3)
        _cloud(p, [(49, 33.5), (44, 31), (39, 30), (34, 30.5), (30, 32)], 3.6, 1.6, s_cloud, 50)
        if p.big:
            p.patch(53, 34, ["111", "151", "1a1", ".1."], {"1": "ink", "5": "coat3", "a": "bolt1"})
            p.pxs([(62, 40), (62, 41)], "ink")
        return

    if view in ("down", "up"):
        # follower: the hound loping toward or away from the camera, its
        # cloud ears swept up and back
        st = phase
        if view == "up":
            p.limb([(32, 46), (35, 41.5), (32, 39.5), (35, 33.5)], 4.6, 1.8, s_coat, group=20, cap=False)
        p.blob(32, 47, 7.0, 8, s_coat, group=1)
        p.limb([(28, 50), (27.5, 59 - 2 * st)], 4.2, 3.4, s_coat, group=12)
        p.limb([(36, 50), (36.5, 59 - 2 * (1 - st))], 4.2, 3.4, s_coat, group=13)
        p.blob(27.5, 59.5 - 2 * st, 2.8, 1.8, s_coat if view == "down" else s_stone, group=12)
        p.blob(36.5, 59.5 - 2 * (1 - st), 2.8, 1.8, s_coat if view == "down" else s_stone, group=13)
        if view == "down":
            p.lens((28, 35), (21, 24 + st), 4.6, s_cloud, bend=0.6, fat=0.35, group=40)
            p.lens((36, 35), (43, 24 + (1 - st)), 4.6, s_cloud, bend=-0.6, fat=0.35, group=41)
            p.blob(32, 38.5, 6.0, 5.6, s_coat, group=3)
            p.limb([(32, 41), (32, 47)], 5.4, 3.6, s_coat, group=4)
            p.eye(27, 37, 2, 3, shine="coat3", shine_at=(0, 0))
            p.eye(35, 37, 2, 3, shine="coat3", shine_at=(1, 0))
            p.pxs([(31, 47), (32, 47)], "ink")
            p.stroke([(32, 33), (31, 35), (33, 36)], "bolt1")
        else:
            p.blob(32, 38, 6.0, 5.6, s_coat, group=3)
            p.lens((28, 36), (21, 25 + st), 4.6, s_cloud, bend=0.6, fat=0.35, group=40)
            p.lens((36, 36), (43, 25 + (1 - st)), 4.6, s_cloud, bend=-0.6, fat=0.35, group=41)
            p.stroke([(32, 41), (31, 44), (33, 46), (31, 49), (32, 52)], "bolt1")
            p.stroke([(32, 46), (35, 41), (32, 39), (34, 34)], "bolt1")
        return


MONS = [
    Mon("Skylaps", SKYLAPS_COLORS, SKYLAPS_SHINY, skylaps, foot="paw"),
]
