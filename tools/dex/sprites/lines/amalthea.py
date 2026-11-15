"""Amalthea line: Eripip, Kerazap, Kerastorm (the region's mascot).

Amalthea, the goat who nursed the infant Zeus in the Diktaean cave. Her
broken horn became the cornucopia and her hide the aegis, the storm-cloud
Zeus shook to raise thunder (Ovid, Fasti 5; Hyginus, Astronomica 2.13).
The line grows from a static-charged puff of a kid, through a prancing
young goat with sparking horn buds, into the storm-fleeced nurse goat whose
snapped horn pours out fruit.
"""
from mon_lib import C, Mat, Mon, bez

INK = C.ink


def _zig(p, pts, core="gold1", edge=None):
    """A little zigzag spark: a 1 px bright line, optionally with a darker
    edge pixel under each bend."""
    p.stroke(pts, core)
    if edge and p.big:
        for x, y in pts[1:-1]:
            p.px(x, y + 1, edge)


# --------------------------------------------------------------------------
# Eripip, the static kid
# --------------------------------------------------------------------------

ERIPIP_COLORS = [
    ("ink", INK),
    # marble-white fleece shaded warm, toward limestone
    ("fl0", (160, 144, 120)), ("fl1", (200, 192, 168)), ("fl2", (232, 224, 208)), ("fl3", C.white),
    # limestone muzzle, inner ears and hooves
    ("lm0", (120, 88, 56)), ("lm1", C.limestone[0]), ("lm2", C.limestone[1]), ("lm3", C.limestone[2]),
    # sun-gold sparks with one pale Aegean highlight
    ("gold0", (200, 136, 32)), ("gold1", C.sungold[1]), ("gold2", (248, 240, 168)),
    ("sky", C.aegean[3]), ("iris", C.aegean[1]),
]
ERIPIP_SHINY = {
    # pale Aegean-blue fleece, marble-white sparks
    "fl0": (96, 128, 176), "fl1": (144, 184, 224), "fl2": (192, 224, 240), "fl3": (232, 248, 248),
    "gold0": (168, 160, 152), "gold1": (216, 208, 200), "gold2": (248, 248, 240),
    "sky": (248, 224, 120),
}

e_fleece = Mat(["fl0", "fl1", "fl2", "fl3"], line="fl0", cuts=[0.3, 0.56, 0.9])
e_face = Mat(["fl1", "fl2", "fl3"], line="fl0", cuts=[0.5, 0.8])
e_ear = Mat(["lm1", "lm2", "lm3"], line="lm0", cuts=[0.4, 0.66])
e_muzzle = Mat(["lm1", "lm2", "lm3"], line="lm0", cuts=[0.4, 0.62])
e_leg = Mat(["fl1", "fl2", "fl3"], line="fl0", cuts=[0.4, 0.66])
e_hoof = Mat(["lm0", "lm1"], line="ink", cuts=[0.5])
# at icon size the shared icon palettes turn fl1 gray, so keep the fleece light
e_fleece_s = Mat(["fl1", "fl2", "fl3"], line="fl1", cuts=[0.72, 0.95])
e_face_s = Mat(["fl2", "fl3"], line="fl1", cuts=[0.85])


def _ehoof(p, x, y, far=False):
    p.rect(x, y, x + 2, y + 1, e_hoof, bias=0.3 if far else 0)


def _cloud(p, puffs, mat, group, **kw):
    """Several circles as one shaded form (a scalloped fleece edge)."""
    from mon_lib import ellipse_pts
    polys = [ellipse_pts(x, y, r, r * k) for x, y, r, k in puffs]
    return p.polys(polys, mat, group=group, **kw)


def eripip(p, view, phase):
    # The battle front and back are hand-finished (art/eripip_*.txt); this
    # draft drives the icon and the follower, so it keeps the same design:
    # a white puffball kid, sideways ears, a limestone muzzle and hooves.
    if view in ("front", "side", "icon"):
        fleece, face = (e_fleece, e_face) if p.big or view == "side" else (e_fleece_s, e_face_s)
        walk = view == "side"
        hop = walk and phase == 1     # the follower pronks: all four legs tucked at once
        E = 1 if (phase == 1 and not walk) else 0     # ears flick up
        dy = -2 if hop else 0
        legs = [(32.5, 37.5), (40, 45)]
        for x, far in ((34, True), (40, True), (28, False), (45, False)):
            x0 = x + (0.8 if hop and x < 36 else -0.8 if hop else 0)
            p.limb([(x, 53 + dy), (x0, (57 if hop else 59) + (0 if far else 1))], 3.4 if far else 3.8,
                   3.0 if far else 3.4, e_leg, bias=0.3 if far else 0, group=10 + int(far))
            fy = (57 if hop else 59) + (0 if far else 1)
            p.rect(int(x0) - 1, int(fy), int(x0) + 1, int(fy) + 1, e_hoof, bias=0.3 if far else 0)
        p.lens((41.5, 39 + dy), (45, 33.5 + dy), 4, fleece, bend=-0.5, group=19)            # tail
        _cloud(p, [(36.5, 46.5 + dy, 9, 0.85), (42.6, 40.6 + dy, 3.8, 1),
                   (37.2, 38.8 + dy, 4.2, 1), (31.6, 40.2 + dy, 3.8, 1),
                   (45.2, 46.6 + dy, 3.6, 1), (41.2, 52.8 + dy, 3.6, 1),
                   (35, 53.8 + dy, 3.6, 1), (29.6, 52.4 + dy, 3.4, 1),
                   (28.6, 47 + dy, 4.3, 1)], fleece, 1)
        # ears stick out sideways (flicked up in frame 2)
        p.lens((17, 41 + dy), (11, 41.5 - 4 * E + dy), 3.4, e_ear, bend=0.3, bias=0.2, group=30)
        p.lens((30, 41 + dy), (37, 42 - 6 * E + dy), 3.6, e_ear, bend=-0.4, group=31)
        p.blob(24, 44.3 + dy, 7.4, 7, face, group=32)
        p.blob(18.2, 47.7 + dy, 3.8, 2.7, e_muzzle, ang=10, group=32)
        _cloud(p, [(24.6, 36.9 + dy, 3.4, 0.85), (29, 38.3 + dy, 2.8, 0.93), (20.6, 38.6 + dy, 2.2, 0.95)],
               fleece, 33)
        if p.big:
            p.eye(24, 40 + dy, 4, 6, iris="iris", shine="fl3", shine_at=(1, 1))
            p.eye(18, 41 + dy, 2, 4, shine="fl3", shine_at=(0, 1))
            p.pxs([(15, 45 + dy), (16, 45 + dy)], "ink")
            p.stroke([(17, 47 + dy), (19, 48 + dy)], "lm0")
            _zig(p, [(36, 33), (37, 31), (38, 31), (40, 29)], "gold1", "gold0")
            p.px(38, 31, "sky")
            _zig(p, [(46, 41), (49, 38), (47, 38), (50, 35 - E)], "gold2", "gold0")
            p.stroke([(33, 41 + dy), (35, 40 + dy), (38, 41 + dy)], "fl3")
            p.stroke([(38, 48 + dy), (40, 50 + dy), (42, 49 + dy)], "fl1")
        else:
            p.pxs([(19, 42 + dy), (24, 42 + dy)], "ink")
            p.px(37, 33, "gold1")
        return

    if view == "back":
        # (the hand-finished art replaces this) over the shoulder, the head
        # turned right in profile on the fleece
        p.lens((9, 40), (8, 35.5), 4.4, e_fleece, group=19)
        _cloud(p, [(28, 58, 19, 0.53), (12, 50, 5.4, 1), (19, 45, 6, 0.93), (28, 43, 6.2, 0.94),
                   (36.5, 45, 5.6, 0.96), (38.5, 41, 6, 0.9), (46, 46, 5.4, 1.04)], e_fleece, 1)
        p.lens((36, 31), (30, 34), 4.4, e_ear, bend=-0.5, group=30)
        p.blob(44, 33, 8.6, 8.2, e_face, group=32)
        p.blob(52.6, 37.6, 4.6, 3.3, e_muzzle, ang=-8, group=32)
        _cloud(p, [(42, 25, 4.2, 0.76), (37.3, 27, 2.8, 0.96), (46.8, 25.8, 2.8, 0.9)], e_fleece, 33)
        p.eye(44, 28, 4, 6, iris="iris", shine="fl3", shine_at=(1, 1))
        if p.big:
            p.px(56, 36, "ink")
            p.stroke([(51, 39), (54, 39)], "lm0")
            _zig(p, [(17, 40), (19, 37), (17, 37), (20, 34)], "gold1", "gold0")
            p.px(20, 34, "sky")
            p.stroke([(19, 48), (22, 46), (25, 47)], "fl3")
            p.stroke([(30, 52), (33, 54), (36, 53)], "fl1")
        return

    if view in ("down", "up"):
        # follower: facing the camera, or walking away; phase 1 bunches the
        # legs for a pronk
        s = phase
        for x, dx in ((27.5, -0.6), (36.5, 0.6)):
            x1 = x + dx * (1 - s) * 2
            p.limb([(x, 53), (x1, 59 - 2 * s)], 3.8, 3.4, e_leg, group=12)
            p.rect(int(x1) - 1, int(59 - 2 * s), int(x1) + 1, int(60 - 2 * s), e_hoof)
        if view == "up":
            p.lens((23, 41), (16, 41.5 - 2 * s), 3.6, e_ear, bias=0.1, group=30)
            p.lens((41, 41), (48, 41.5 - 2 * s), 3.6, e_ear, bias=0.1, group=31)
            p.blob(32, 40, 7, 6.2, e_face, group=32)
            _cloud(p, [(32, 35.5, 4.4, 0.8), (28, 36.6, 2.6, 1), (36, 36.6, 2.6, 1)], e_fleece, 33)
            _cloud(p, [(32, 50, 10, 0.75), (24, 47, 3.6, 1), (40, 47, 3.6, 1), (28, 44.5, 3.6, 1), (36, 44.5, 3.6, 1)],
                   e_fleece, 1)
            p.lens((32, 45.5), (33, 40), 4, e_fleece, group=2)
            return
        _cloud(p, [(32, 49, 10, 0.72), (24, 46, 3.5, 1), (40, 46, 3.5, 1), (25, 52, 3.5, 1), (39, 52, 3.5, 1)],
               e_fleece, 1)
        p.lens((25, 39), (17, 39.5 - 2 * s), 3.8, e_ear, group=30)
        p.lens((39, 39), (47, 39.5 - 2 * s), 3.8, e_ear, group=31)
        p.blob(32, 41, 7.4, 6.8, e_face, group=32)
        p.blob(32, 45.6, 3.8, 2.6, e_muzzle, group=32)
        _cloud(p, [(32, 35, 4.6, 0.75), (28, 36, 2.6, 1), (36, 36, 2.6, 1)], e_fleece, 33)
        p.eye(27, 39, 3, 4, iris="iris", shine="fl3")
        p.eye(35, 39, 3, 4, iris="iris", shine="fl3")
        p.pxs([(31, 45), (32, 45)], "ink")
        if p.big:
            _zig(p, [(43, 36), (44, 34), (45, 34), (46, 32)], "gold1", "gold0")
        return


# --------------------------------------------------------------------------
# Kerazap, the spark goat
# --------------------------------------------------------------------------

KERAZAP_COLORS = [
    ("ink", INK),
    # marble-white fleece with marble-gray cloud shading
    ("fl0", (120, 120, 128)), ("fl1", (168, 168, 168)), ("fl2", (216, 208, 200)), ("fl3", C.white),
    # limestone face, coat and legs
    ("lm0", (112, 80, 48)), ("lm1", (168, 136, 88)), ("lm2", (208, 176, 128)), ("lm3", (232, 216, 176)),
    # sun-gold horn tips and sparks
    ("gold0", (200, 136, 32)), ("gold1", C.sungold[1]), ("gold2", (248, 240, 168)),
    ("sky", C.aegean[3]), ("iris", C.aegean[1]),
    ("hoof", (80, 56, 40)),
]
KERAZAP_SHINY = {
    # pale Aegean-blue fleece, marble-white horn sparks
    "fl0": (72, 104, 152), "fl1": (128, 168, 216), "fl2": (184, 216, 240), "fl3": (232, 248, 248),
    "gold0": (168, 160, 152), "gold1": (216, 208, 200), "gold2": (248, 248, 240),
    "sky": (248, 224, 120),
}

z_fleece = Mat(["fl0", "fl1", "fl2", "fl3"], line="fl0", cuts=[0.34, 0.6, 0.92])
z_fleece_s = Mat(["fl1", "fl2", "fl3"], line="fl1", cuts=[0.7, 0.95])
z_coat = Mat(["lm0", "lm1", "lm2", "lm3"], line="lm0", cuts=[0.18, 0.42, 0.7])
z_leg = Mat(["lm0", "lm1", "lm2"], line="lm0", cuts=[0.3, 0.6])
z_horn = Mat(["hoof", "lm1", "lm2"], line="hoof", cuts=[0.34, 0.66])
z_tip = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.3, 0.62])
z_hoof = Mat(["hoof", "lm0"], line="ink", cuts=[0.5])


def _zhoof(p, x, y, far=False, w=3):
    p.rect(x, y, x + w - 1, y + 1, z_hoof, bias=0.3 if far else 0)
    if p.big:
        p.px(x + w // 2, y + 1, "ink")


def _horn_bud(p, base, tip, w, bias=0.0):
    """A stubby horn bud whose top third is a sun-gold spark tip."""
    mid = (base[0] + (tip[0] - base[0]) * 0.5, base[1] + (tip[1] - base[1]) * 0.5)
    p.limb([base, mid], w, w * 0.85, z_horn, bias=bias)
    p.limb([mid, tip], w * 0.85, w * 0.45, z_tip, bias=bias)


def kerazap(p, view, phase):
    if view in ("front", "side", "icon"):
        fleece = z_fleece if p.big or view == "side" else z_fleece_s
        walk = view == "side"
        L = 1 if (phase == 1 and view == "front") else 0
        # legs: (hip, knee or hock, foot)
        if walk and phase:
            near_front = [(25, 44), (24, 51), (22.5, 58)]
            far_front = [(29, 45), (31, 51), (32.5, 58)]
            near_hind = [(47.5, 43), (48.5, 50.5), (46.5, 58.5)]
            far_hind = [(43, 45), (46.5, 51.5), (47, 58)]
        elif walk:
            near_front = [(25, 44), (21.5, 49.5), (19.5, 55.5)]
            far_front = [(29, 45), (29, 51.5), (28.5, 58)]
            near_hind = [(47.5, 43), (51, 50), (51.5, 58.5)]
            far_hind = [(43, 45), (44.5, 51.5), (42, 58)]
        else:
            # mid-prance: the near forehoof raised, knee forward
            near_front = [(25, 44), (20.5, 48.5 - L), (22, 53.5 - L)]
            far_front = [(29, 45), (29.5, 52), (29, 58.5)]
            near_hind = [(47.5, 43), (50.5, 50), (48.5, 59.5)]
            far_hind = [(43, 45), (45.5, 51.5), (43.5, 58.5)]
        p.limb(far_front, 3.8, 3.0, z_leg, bias=0.35, group=10)
        p.limb(far_hind, 4.6, 3.0, z_leg, bias=0.35, group=11)
        _zhoof(p, int(far_front[-1][0]) - 1, int(far_front[-1][1]), far=True)
        _zhoof(p, int(far_hind[-1][0]) - 1, int(far_hind[-1][1]), far=True)

        # tail, a white puff flicked up
        p.lens((49, 37.5), (52.5, 32 - L), 4, fleece, bend=-0.6, group=19)
        # far ear and far horn bud, behind the head
        p.lens((17, 20.5 - L), (10, 19.5 - 2 * L), 3.4, z_coat, bend=-0.5, bias=0.3, group=20)
        _horn_bud(p, (20, 19 - L), (20, 13.5 - L), 3.8, bias=0.2)

        # barrel and rump: short limestone coat
        p.blob(41, 41, 8.6, 5.4, z_coat, group=1)
        p.blob(46.5, 39.6, 4.6, 5, z_coat, group=1)
        p.blob(40, 44.6, 6.4, 1.8, z_coat, bias=-0.2, group=1)
        # neck rising out of the ruff
        p.limb([(28, 36), (24, 27)], 8, 7, z_coat, group=2)

        # the cloud-puff ruff over chest and shoulders
        g = 3
        for x, y, r in ((34.5, 36.5, 5.0), (30, 31.5, 5.2), (26.5, 39.5, 5.2), (32, 42.5, 4.4),
                        (23.5, 33.5, 5.4), (20.8, 38.8, 4.2)):
            p.circle(x, y, r, fleece, group=g, bias=-0.12)
            g += 1

        # head, lifted and alert
        p.blob(22.5, 24 - L, 6.8, 6.2, z_coat, group=12)
        p.blob(15.8, 28.4 - L, 4.2, 2.9, z_coat, ang=22, group=12)
        # goatee that crackles
        p.lens((16, 31 - L), (16.5, 37 - L), 3.2, fleece, bend=0.4, group=13)
        # near horn bud and ear
        _horn_bud(p, (24.5, 19.5 - L), (26.5, 13.5 - L), 4.2)
        p.lens((27.5, 21.5 - L), (35, 21 - 3 * L), 3.8, z_coat, bend=0.6, group=14)

        # near legs, over the body
        p.limb(near_front, 4.2, 3.4, z_leg, group=15)
        p.limb([(46, 41)] + near_hind, 6.8, 3.4, z_leg, group=16)
        fx, fy = near_front[-1]
        _zhoof(p, int(fx) - 1, int(fy))
        _zhoof(p, int(near_hind[-1][0]) - 1, int(near_hind[-1][1]))

        if p.big:
            p.eye(19, 21 - L, 4, 5, iris="iris", shine="fl3", shine_at=(1, 1))
            p.pxs([(12, 27 - L), (12, 28 - L)], "ink")             # nose
            p.stroke([(14, 30 - L), (16, 30 - L)], "lm0")         # mouth
            _zig(p, [(14, 36), (15, 38), (16, 38), (17, 40)], "gold1", "gold0")   # goatee crackle
            _zig(p, [(27, 11), (28, 9), (29, 9), (30, 7)], "gold1", "gold0")      # horn sparks
            p.px(29, 9, "sky")
        else:
            p.px(20, 22 - L, "ink")
        return

    if view == "back":
        # over the shoulder, head turned right: ruff, horn buds, coat
        p.blob(22, 62, 22, 12, z_coat, group=1)
        p.blob(12, 52, 6, 6, z_coat, group=1)
        p.lens((6, 47), (3, 40), 5, z_fleece, bend=0.6, group=19)
        g = 3
        for x, y, r in ((32, 52, 7), (40, 46, 7), (30, 42, 6.6), (46, 54, 6.6), (37, 58, 6.6), (24, 50, 6)):
            p.circle(x, y, r, z_fleece, group=g)
            g += 1
        p.limb([(40, 44), (44, 33)], 10, 9, z_coat, group=10)
        p.blob(45, 27, 8, 7.4, z_coat, group=12)
        p.blob(53.5, 31, 5, 3.4, z_coat, ang=-15, group=12)
        p.lens((54, 34), (54.5, 41), 3.8, z_fleece, group=13)
        _horn_bud(p, (41, 21), (38.5, 13), 4.4)
        _horn_bud(p, (46, 20.5), (46.5, 13), 4.0, bias=0.2)
        p.lens((39, 25), (31, 25.5), 4.4, z_coat, bend=-0.5, group=14)
        p.eye(48, 23, 4, 5, iris="iris", shine="fl3", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        s = phase
        for x, k in ((27.5, 0), (36.5, 1)):
            st = (s + k) % 2
            p.limb([(x, 46), (x, 59 - 2 * st)], 3.6, 3.0, z_leg, group=12)
            _zhoof(p, int(x) - 1, int(59 - 2 * st))
        p.blob(32, 44, 7.4, 6, z_coat, group=1)
        if view == "up":
            p.lens((32, 48), (33, 41), 4, z_fleece, group=2)
            _cloud(p, [(32, 37, 7.4, 0.7), (26, 36, 4, 1), (38, 36, 4, 1)], z_fleece, 3)
            p.lens((26, 25), (18, 23.5 - s), 3.6, z_coat, group=4)
            p.lens((38, 25), (46, 23.5 - (1 - s)), 3.6, z_coat, group=4)
            p.blob(32, 27, 6.4, 6, z_coat, group=5)
            _horn_bud(p, (29.5, 22), (28, 15), 3.6)
            _horn_bud(p, (34.5, 22), (36, 15), 3.6)
            return
        _cloud(p, [(32, 38, 8, 0.75), (25.5, 37, 4, 1), (38.5, 37, 4, 1), (32, 42, 5, 0.8)], z_fleece, 3)
        p.lens((26, 25), (18, 23.5 - s), 3.6, z_coat, group=4)
        p.lens((38, 25), (46, 23.5 - (1 - s)), 3.6, z_coat, group=4)
        _horn_bud(p, (29.5, 21.5), (28, 14.5), 3.6)
        _horn_bud(p, (34.5, 21.5), (36, 14.5), 3.6)
        p.blob(32, 27, 6.6, 6, z_coat, group=5)
        p.blob(32, 31.5, 3.8, 2.6, z_coat, bias=-0.1, group=5)
        p.lens((32, 33.5), (32, 38.5), 3, z_fleece, group=6)
        p.eye(27, 25, 3, 4, iris="iris", shine="fl3")
        p.eye(35, 25, 3, 4, iris="iris", shine="fl3")
        p.pxs([(31, 31), (32, 31)], "ink")
        return


# --------------------------------------------------------------------------
# Kerastorm, the storm-goat: Amalthea grown, the aegis and the cornucopia
# --------------------------------------------------------------------------

KERASTORM_COLORS = [
    ("ink", INK),
    # the thundercloud fleece: marble gray with Aegean-blue shadows
    ("cl0", (40, 56, 104)), ("cl1", (96, 112, 160)), ("cl2", (160, 168, 192)), ("cl3", (216, 216, 224)),
    ("cl4", C.white),
    # limestone face, legs and the great horn, warming to bronze in the shadows
    ("lm0", (88, 48, 32)), ("lm1", (192, 128, 72)), ("lm2", (232, 192, 128)),
    # sun-gold lightning
    ("gold0", (216, 144, 32)), ("gold1", (248, 224, 96)),
    # the horn of plenty: olive grapes and figs, a terracotta pomegranate, one Fairy-pink accent
    ("ol0", (72, 96, 32)), ("ol1", (144, 168, 64)), ("terra", (152, 80, 48)), ("pink", (240, 152, 168)),
]
KERASTORM_SHINY = {
    # a sunset sun-gold thundercloud with Aegean-blue lightning
    "cl0": (128, 56, 32), "cl1": (200, 104, 48), "cl2": (232, 160, 72), "cl3": (248, 208, 128),
    "cl4": (248, 240, 208),
    "gold0": (48, 104, 176), "gold1": (152, 208, 248),
}

s_cloud = Mat(["cl0", "cl1", "cl2", "cl3", "cl4"], line="cl1", cuts=[0.3, 0.48, 0.64, 0.84])
s_cloud_s = Mat(["cl2", "cl3", "cl4"], line="cl2", cuts=[0.62, 0.9])
s_coat = Mat(["lm0", "terra", "lm1", "lm2"], line="lm0", cuts=[0.24, 0.44, 0.7])
s_horn = Mat(["lm0", "lm1", "lm2"], line="lm0", cuts=[0.3, 0.6])
s_hoof = Mat(["ink", "lm0"], line="ink", cuts=[0.5])
s_grape = Mat(["ol0", "ol1"], line="ol0", cuts=[0.55])
s_pom = Mat(["lm0", "terra", "pink"], line="lm0", cuts=[0.3, 0.8])
s_bolt = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])


def kerastorm(p, view, phase):
    big = p.big
    cloud = s_cloud if big and view != "side" else s_cloud_s
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        # hind legs planted, the forequarters rearing
        p.limb([(43, 44), (45, 51), (42.5, 58.5)], 6, 3.4, s_coat, bias=0.3, group=10)
        p.rect(41, 58, 44, 59, s_hoof, bias=0.3)
        # tail, a curl of cloud
        p.circle(58, 34 - L, 3.6, cloud, group=11)
        # far foreleg, tucked high
        p.limb([(32, 30), (25, 25 - L), (22, 31 - L)], 5, 3.4, s_coat, bias=0.3, group=12)
        p.rect(20, 31 - L, 23, 32 - L, s_hoof, bias=0.3)
        # torso rising to the chest, belly in limestone
        p.blob(40, 37, 13, 8, s_coat, ang=-30, group=1)
        p.blob(30, 31, 7.5, 8, s_coat, group=1)
        # the thundercloud along the back and neck
        g = 20
        for x, y, r in ((53, 40, 5.6), (48.5, 33, 6.4), (41.5, 28, 7), (35, 23.5, 6), (31.5, 17, 5.4),
                        (45, 39, 6), (37.5, 33, 6.4), (30, 28, 4.8)):
            p.circle(x, y - (L if y < 30 else 0), r, cloud, group=g)
            g += 1
        # neck and lifted head
        p.limb([(29, 31), (25, 21 - L)], 9.5, 8.5, s_coat, group=2)
        p.blob(24, 15 - L, 6.6, 6.2, s_coat, group=3)
        p.blob(16.6, 19 - L, 4.8, 3.2, s_coat, ang=26, group=3)
        p.lens((16.8, 22.5 - L), (16.4, 30 - L), 4, cloud, bend=0.6, group=4)     # goatee
        # the great horn, sweeping back
        p.limb(bez((27, 12.5 - L), (31, 5 - L), (43, 6 - L), n=10) + [(50, 8.5 - L), (54, 13 - L), (55, 18 - L),
               (53.5, 22 - L)], 8.4, 2.6, s_horn, group=5)
        # the broken horn, the horn of plenty, and its fruit
        p.limb([(20.5, 10 - L), (17, 5 - L)], 5.6, 6.2, s_horn, group=6)
        for x, y in ((13, 6.5), (11.5, 9), (14, 9.5), (10, 11.5), (12.5, 12), (11, 14.5)):
            p.circle(x, y - L, 1.6, s_grape, group=7)
        p.circle(7.5, 19 - L, 3.2, s_pom, group=8)
        p.drop((5.5, 9.5 - L), 6.5, 13 - L, 2.4, s_grape, group=9)
        # near ear
        p.lens((29.5, 15 - L), (36.5, 17.5 - L), 3.6, s_coat, bend=0.6, group=13)
        # near foreleg, raised and bent
        p.limb([(31, 35), (22, 34 - L), (18.5, 40 - L)], 6, 3.8, s_coat, group=14)
        p.rect(16, 40 - L, 20, 41 - L, s_hoof)
        # near hind leg, the thrust of the rear
        p.limb([(49, 40), (53, 49), (50, 59.5)], 8.4, 3.8, s_coat, group=15)
        p.rect(48, 59, 52, 60, s_hoof)
        if big:
            p.eye(20, 12 - L, 4, 5, shine="cl4", shine_at=(1, 1))
            p.px(21, 16 - L, "gold0")
            p.pxs([(12, 18 - L), (12, 19 - L)], "ink")
            p.stroke([(14, 21 - L), (17, 21 - L)], "lm0")
        else:
            p.px(21, 13 - L, "ink")
        return

    if view == "back":
        p.circle(6, 40, 4, s_cloud, group=11)
        g = 20
        for x, y, r in ((14, 54, 9), (26, 46, 9), (38, 44, 8.5), (46, 52, 8), (30, 58, 9), (20, 62, 9),
                        (42, 60, 7)):
            p.circle(x, y, r, s_cloud, group=g)
            g += 1
        p.limb([(42, 42), (45, 30)], 10, 9, s_coat, group=2)
        p.blob(46, 24, 8, 7.4, s_coat, group=3)
        p.blob(55, 28, 5, 3.4, s_coat, ang=-15, group=3)
        p.limb(bez((43, 18), (36, 4), (24, 8), n=10) + [(19, 14)], 7, 2.6, s_horn, group=5)
        p.limb([(49, 18), (51, 12)], 5.6, 6, s_horn, group=6)
        p.eye(49, 21, 4, 5, shine="cl4", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: a sturdy goat under a storm-cloud fleece, the great horn
        # sweeping out to her left, the horn of plenty on her right
        s = phase
        down = view == "down"
        hx = 1 if down else -1          # which side of the screen the great horn is on
        for x, k in ((25.5, 0), (38.5, 1)):
            st = (s + k) % 2
            p.limb([(x, 46), (x, 58 - 2 * st)], 6, 5, s_coat, bias=0.1, group=12 + k)
            p.rect(int(x) - 2, int(58 - 2 * st), int(x) + 2, int(59 - 2 * st), s_hoof)
        if not down:
            p.circle(32, 50, 3.6, cloud, group=9)                     # tail puff
        g = 1
        for x, y, r in ((21, 38, 6), (43, 38, 6), (32, 35, 7.4), (24, 45, 6), (40, 45, 6), (32, 46, 6.4)):
            p.circle(x, y, r, cloud, group=g)
            g += 1
        # the great horn: a wide ridged crescent out to one side
        cx = 32 + hx * 4
        p.limb(bez((cx, 22), (cx + hx * 8, 6), (cx + hx * 18, 10), n=10) + [(cx + hx * 21, 17), (cx + hx * 19, 22)],
               6.4, 2.4, s_horn, group=20)
        # the broken horn on the other side, grapes spilling from it
        sx = 32 - hx * 4
        p.limb([(sx, 22), (sx - hx * 3, 16)], 5, 6, s_horn, group=21)
        for dx, dy in ((-1, 14.5), (-3.5, 16), (-1.5, 18), (-4, 19.5)):
            p.circle(sx - hx * 3 + hx * dx, dy, 1.7, s_grape, group=22)
        p.blob(32, 26, 7.6, 7.2, s_coat, group=23)
        if down:
            p.blob(32, 32, 4.6, 3.6, s_coat, group=23)
            p.lens((32, 34), (32, 41), 4, cloud, group=24)            # goatee
            if big:
                p.eye(26, 24, 4, 4, shine="cl4", shine_at=(1, 1))
                p.eye(34, 24, 4, 4, shine="cl4", shine_at=(2, 1))
                p.pxs([(27, 27), (36, 27)], "gold0")
                p.pxs([(31, 32), (32, 32)], "ink")
            else:
                p.pxs([(27, 25), (36, 25)], "ink")
        return


MONS = [
    Mon("Eripip", ERIPIP_COLORS, ERIPIP_SHINY, eripip, foot="hoof"),
    Mon("Kerazap", KERAZAP_COLORS, KERAZAP_SHINY, kerazap, foot="hoof"),
    Mon("Kerastorm", KERASTORM_COLORS, KERASTORM_SHINY, kerastorm, foot="hoof", icon_pal=3),
]
