"""Cyclops line: Monophant, Polyphant (Rock / Normal). The one-eyed giants.

Polyphemus kept his flocks in a cave on the Cyclopes' island (Odyssey 9).
Skulls of the Mediterranean dwarf elephants have one great hole in the
middle of the face where the trunk was, and they are a likely source of the
tale (Othenio Abel, 1914). Monophant is a dwarf elephant revived from such a
skull: its face is still bare bone, the trunk socket reads as one great eye
and its real eyes are small and set to the sides. Polyphant is the giant
shepherd, a fleece cloak on its shoulders and a boulder underfoot, the stone
it rolls across its cave door each night; deep in its socket a ring of light
stares like the Cyclops's one eye.

The battle front and back are hand-finished in tools/dex/sprites/art/; the
drafts here set their poses and still draw the icons and the followers.
"""
from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# An elephant's print: a round pad with the toenails along its front edge.
ELEPHANT_FOOT = [
    "................",
    "................",
    "................",
    ".....#..#..#....",
    "....##########..",
    "...############.",
    "...############.",
    "...############.",
    "...############.",
    "...############.",
    "....##########..",
    ".....########...",
    "................",
    "................",
    "................",
    "................",
]


# --------------------------------------------------------------------------
# Monophant, the revived skull
# --------------------------------------------------------------------------

MONOPHANT_COLORS = [
    ("ink", INK),
    # limestone bone fading to a marble highlight
    ("bone0", (136, 112, 80)), ("bone1", (184, 160, 120)), ("bone2", (224, 208, 168)), ("bone3", (248, 248, 232)),
    # earth-brown elephant hide
    ("hide0", (64, 40, 32)), ("hide1", (104, 64, 48)), ("hide2", (144, 96, 64)), ("hide3", (184, 136, 96)),
    # ginger terracotta wool
    ("wool0", (136, 56, 32)), ("wool1", (192, 104, 56)), ("wool2", (232, 160, 96)),
    ("void", (48, 24, 32)), ("rose", (208, 128, 112)),
]
MONOPHANT_SHINY = {
    # ash-gray wool and a sun-gold skull-plate
    "wool0": (72, 72, 80), "wool1": (120, 120, 128), "wool2": (184, 184, 192),
    "bone0": (152, 96, 32), "bone1": (208, 152, 48), "bone2": (240, 200, 96), "bone3": (248, 240, 184),
}

m_bone = Mat(["bone0", "bone1", "bone2", "bone3"], line="bone0", cuts=[0.28, 0.52, 0.76])
m_hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.2, 0.44, 0.7])
m_wool = Mat(["wool0", "wool1", "wool2"], line="wool0", cuts=[0.4, 0.66])
m_cave = Mat(["void", "hide0"], line="void")
m_ear = Mat(["hide1", "hide2", "rose"], line="hide0", cuts=[0.36, 0.62])
m_tusk = Mat(["bone1", "bone2", "bone3"], line="bone0", cuts=[0.34, 0.62])
m_rose = Mat(["hide1", "rose"], line="hide0", cuts=[0.5])


def _toes(p, x, y, n=3, far=False):
    """Elephant toenails along the front of a foot, left nail at (x, y)."""
    if not p.big:
        return
    for i in range(n):
        p.px(x + 2 * i, y, "bone1" if far else "bone2")


def _tusk(p, path, w, mat=None, **kw):
    """A stubby tusk: thick at the root, tapering to a blunt tip."""
    return p.limb(path, w, max(w * 0.45, 1.2), mat or m_tusk, **kw)


def _socket(p, cx, cy, r, group, **kw):
    """The great nasal socket: a round hole whose lower-right inner wall
    catches the light, so it reads as a hollow (and as one staring eye)."""
    hole = p.circle(cx, cy, r, m_cave, flat=1, group=group, **kw)
    p.circle(cx - 0.7, cy - 0.8, r - 1.0, m_cave, flat=0, clip=[hole], group=group, noline=True)
    return hole


def monophant(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        flap = phase == 1 and view == "front"
        st = phase if view == "side" else 0

        # tail with a wool tassel
        p.limb(bez((53.5, 43), (56.5, 45), (57, 50)), 2.0, 1.6, m_hide, group=20)
        p.blob(57.2, 51.5 - L, 1.9, 2.6, m_wool, group=21)

        # far legs, in shade
        p.limb([(50, 50), (50.5, 60 - st)], 7.4, 7.0, m_hide, cap=False, bias=0.32, group=10)
        p.limb([(36, 50), (36, 60)], 7.2, 6.8, m_hide, cap=False, bias=0.32, group=11)

        # body: a round barrel, low and heavy
        p.blob(41.5, 47.5, 13.5, 8.6, m_hide, group=1)
        p.blob(49.5, 46, 6.5, 7.6, m_hide, group=1)
        # woolly back: a shaggy coat from the neck to the rump, its fringe
        # hanging in rounded locks
        wool = [(33, 38.5, 6, 5), (40, 37.5, 7, 5.5), (47, 38.5, 6.5, 5.2), (52.5, 41, 4.2, 4.4)]
        for x, y, rx, ry in wool:
            p.blob(x, y, rx, ry, m_wool, group=2)
        for x, y, r in ((30.5, 42.5, 2.6), (35, 43.5, 2.8), (40, 44, 3.0), (45, 44, 2.8), (49.5, 43.5, 2.6),
                        (53.5, 44.5, 2.2), (37.5, 33.5, 2.6), (43, 32.8, 2.8), (48.5, 34, 2.6), (52.5, 37, 2.2)):
            p.circle(x, y, r, m_wool, group=2)

        # the woolly crest, crown to back, like a young mammoth's hump
        for x, y, r in ((26, 21.5 - L, 3.4), (30, 20.5 - L, 3.6), (34, 21.5 - L, 3.6), (38, 23, 3.4), (42, 25, 3.2),
                        (45.5, 27.5, 3.0)):
            p.circle(x, y, r, m_wool, group=2)

        # near hind leg: haunch and column
        p.blob(48, 50, 6.2, 6.0, m_hide, group=13)
        p.limb([(47, 52), (46.5, 61 - st)], 8.0, 7.6, m_hide, cap=False, group=13)
        _toes(p, 44, 59 - st)

        # near ear: a broad fan behind the cheek, its inside showing
        tx = 3 if flap else 0
        ear = p.poly(bez3((28, 27 - L), (37 + tx, 23 - L), (44 + tx, 33), (39 + tx, 48)) +
                     bez((39 + tx, 48), (32, 49), (28, 42)), m_hide, group=5)
        p.poly(bez3((30, 30 - L), (36 + tx, 28 - L), (41 + tx, 35), (37 + tx, 45)) +
               bez((37 + tx, 45), (32, 45), (30, 40)), m_ear, clip=[ear], group=5, noline=True)

        # near front leg, under the cheek
        p.limb([(31, 50), (30.5, 61)], 8.2, 7.8, m_hide, cap=False, group=12)
        _toes(p, 27, 59)

        # head lowered: a hide skull behind the bony face-plate
        p.blob(23.5, 35.5 - L, 11, 10.5, m_hide, group=3)
        # wool forelock over the crown
        for x, y, r in ((24.5, 24.5 - L, 3.0), (28.5, 25.5 - L, 3.2), (31, 29 - L, 2.8)):
            p.circle(x, y, r, m_wool, group=4)
        # the face-plate: a domed brow, the socket in the middle of the face,
        # and two tusk-sheaths running down either side of the trunk
        p.poly(bez3((9.5, 34 - L), (9, 21.5 - L), (26, 19.5 - L), (29, 29 - L)) +
               bez3((29, 29 - L), (30.5, 36 - L), (28, 42 - L), (25, 46.5 - L)) +
               [(21.5, 47 - L), (19, 43 - L), (15.5, 43 - L)] +
               bez((15.5, 43 - L), (13.5, 47 - L), (11, 46 - L)) +
               bez((11, 46 - L), (9, 42 - L), (9.5, 34 - L)), m_bone, group=6, bias=-0.06)
        # far tusk, behind the trunk
        _tusk(p, bez((12.5, 44.5 - L), (9, 49.5 - L), (6.5, 46.5 - L)), 3.4, bias=0.22, group=8)
        # the short trunk curling out from under the socket's lower edge
        tip = (12.5, 48.5 - L) if not flap else (11.5, 43.5 - L)
        mid = (18, 51 - L) if not flap else (17, 50 - L)
        p.limb(bez((18, 40 - L), mid, tip), 5.0, 3.0, m_hide, group=9)
        p.circle(tip[0], tip[1], 1.5, m_rose, group=9)
        # the great socket, a whole round hole like one staring eye
        _socket(p, 18, 35.5 - L, 4.9, 7)
        # near tusk, stubby and curving up
        _tusk(p, bez((24, 45 - L), (23, 52.5 - L), (16.5, 51.5 - L)), 4.0, group=14)

        if p.big:
            # small dark eyes set to the sides
            p.eye(25, 32 - L, 2, 3, shine="bone3", shine_at=(1, 0))
            p.pxs([(11, 32 - L), (11, 33 - L)], "ink")
            # sutures across the dome
            p.stroke([(21, 24 - L), (22, 26 - L), (21, 28 - L)], "bone1")
            p.stroke([(13, 27 - L), (15, 28 - L)], "bone1")
        else:
            p.px(18, 35 - L, "void")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the woolly back cropped by the
        # frame, the ear fan seen from behind, the head turned right in
        # profile with the socket open at the front of the face
        p.blob(22, 63, 23, 15, m_hide, group=1)
        p.blob(37, 52, 12, 10, m_hide, group=1)
        for x, y, rx, ry in ((8, 56, 9, 8), (19, 52, 11, 8.4), (30, 49, 9.5, 7.4), (14, 61, 10, 5)):
            p.blob(x, y, rx, ry, m_wool, group=2)
        for x, y, r in ((2.5, 50, 2.6), (7.5, 47, 3.2), (14, 44.6, 3.4), (20.5, 43.4, 3.4), (27, 43, 3.2),
                        (33, 43.5, 3.0), (37.5, 45, 2.6)):
            p.circle(x, y, r, m_wool, group=2)
        # head: hide skull, then the ear fan over the shoulder
        p.blob(46, 29, 10.5, 10.5, m_hide, group=3)
        ear = p.poly(bez3((41, 18), (30, 13), (22, 24), (25, 36)) + bez3((25, 36), (27, 44), (35, 47), (40, 40)),
                     m_hide, group=5)
        for x, y, r in ((42, 17.5, 3.0), (46.5, 15.5, 3.2), (39, 21.5, 2.6)):
            p.circle(x, y, r, m_wool, group=4)
        # the face-plate in profile, the socket's rim standing out in front
        p.poly(bez3((47, 15), (52, 11), (59, 13), (60, 21)) +
               bez3((60, 21), (61.5, 28), (60, 36), (56.5, 41)) +
               [(52, 42), (49, 38)] + bez3((49, 38), (46.5, 33), (45.5, 23), (47, 15)), m_bone, group=6)
        # the trunk, hanging from the socket and curling forward
        p.limb(bez((57.5, 36), (58.5, 46), (61, 44.5)), 4.4, 2.8, m_hide, group=9)
        p.circle(60.8, 44.2, 1.4, m_rose, group=9)
        hole = p.blob(57.6, 29, 2.4, 4.6, m_cave, flat=0, group=7)
        p.blob(58.3, 30, 1.2, 3.0, m_cave, flat=1, clip=[hole], group=7, noline=True)
        _tusk(p, bez((53, 40), (55, 48), (59.5, 48)), 4.2, group=14)
        p.eye(52, 26, 2, 3, shine="bone3", shine_at=(0, 0))
        if p.big:
            p.stroke([(51, 15), (53, 17), (52, 19)], "bone1")
        return

    if view == "down":
        # follower walking toward the camera: the plate face-on, the socket
        # in the middle, an eye on each side; it turns its head to look
        # with one side at a time
        st = phase
        lk = phase  # the head turns a little toward the near eye
        for sx in (-1, 1):
            p.limb([(32 + 6.5 * sx, 48), (32 + 6.5 * sx, 61 - 1.5 * (st if sx < 0 else 1 - st))], 7.0, 6.6, m_hide, cap=False,
                   group=12 + (sx > 0))
        p.blob(32, 44, 12.5, 8.5, m_hide, group=1)
        for x, y, r in ((21.5, 42, 3.2), (42.5, 42, 3.2), (24, 37.5, 3.6), (40, 37.5, 3.6)):
            p.circle(x, y, r, m_wool, group=2)
        for sx in (-1, 1):
            p.poly([(32 + sx * 9, 26), (32 + sx * 19, 25), (32 + sx * 21, 36), (32 + sx * 16, 45), (32 + sx * 9, 40)],
                   m_hide, group=5 + (sx > 0) * 10)
            p.poly([(32 + sx * 11, 28), (32 + sx * 17.5, 28), (32 + sx * 19, 35), (32 + sx * 15.5, 41), (32 + sx * 11, 38)],
                   m_ear, group=5 + (sx > 0) * 10, noline=True)
        p.blob(32, 33, 10.5, 10, m_hide, group=3)
        for x, y, r in ((28, 23, 3.0), (32, 22, 3.2), (36, 23, 3.0)):
            p.circle(x, y, r, m_wool, group=4)
        p.poly(bez3((22, 32), (22, 21), (42, 21), (42, 32)) + [(40.5, 40), (36.5, 44.5), (34, 41), (30, 41),
                                                                  (27.5, 44.5), (23.5, 40)], m_bone, group=6)
        _tusk(p, bez((25.5, 42), (24, 47), (27, 49)), 3.2, group=14)
        _tusk(p, bez((38.5, 42), (40, 47), (37, 49)), 3.2, group=14)
        p.limb(bez((32 + lk, 37), (32 + lk, 46), (30 + lk, 49)), 4.6, 3.0, m_hide, group=9)
        p.circle(30 + lk, 49, 1.4, m_rose, group=9)
        _socket(p, 32 + lk, 32.5, 4.4, 7)
        p.eye(24 + lk, 30, 1, 2, shine=None)
        p.eye(39 + lk, 30, 1, 2, shine=None)
        return

    if view == "up":
        # follower walking away: the woolly back and the rump, the tail
        # with its tassel, the ears out to the sides
        st = phase
        for sx in (-1, 1):
            p.limb([(32 + 6.5 * sx, 50), (32 + 6.5 * sx, 61 - 1.5 * (st if sx < 0 else 1 - st))], 7.4, 7.0, m_hide, cap=False,
                   group=12 + (sx > 0))
        for sx in (-1, 1):
            p.poly([(32 + sx * 8, 27), (32 + sx * 19, 25), (32 + sx * 21, 36), (32 + sx * 15, 44), (32 + sx * 8, 38)],
                   m_hide, group=5 + (sx > 0) * 10, bias=0.1)
        p.blob(32, 31, 10, 9, m_hide, group=3)
        for x, y, r in ((27, 25, 3.4), (32, 23.5, 3.6), (37, 25, 3.4), (32, 28, 3.6)):
            p.circle(x, y, r, m_wool, group=4)
        p.blob(32, 46, 12.5, 10, m_hide, group=1)
        for x, y, r in ((24, 40, 4), (32, 38, 4.4), (40, 40, 4), (27, 45, 3.8), (37, 45, 3.8), (21.5, 46, 3), (42.5, 46, 3),
                        (32, 44, 4)):
            p.circle(x, y, r, m_wool, group=2)
        p.limb(bez((32, 50), (33, 54), (32.5 + st, 57)), 2.0, 1.6, m_hide, group=20)
        p.blob(32.5 + st, 58, 1.8, 2.2, m_wool, group=21)
        return


# --------------------------------------------------------------------------
# Polyphant, the giant shepherd
# --------------------------------------------------------------------------

POLYPHANT_COLORS = [
    ("ink", INK),
    ("bone0", (128, 104, 72)), ("bone1", (184, 152, 104)), ("bone2", (224, 200, 152)), ("white", C.white),
    # the fleece cloak, marble-white
    ("fleece0", (136, 128, 128)), ("fleece1", (208, 200, 184)),
    # earth-brown hide, a shade deeper than the calf's
    ("hide0", (56, 32, 32)), ("hide1", (96, 56, 40)), ("hide2", (144, 88, 56)), ("hide3", (200, 136, 104)),
    # the door-stone
    ("stone0", (72, 72, 80)), ("stone1", (120, 120, 128)),
    # the light deep in the socket
    ("glow0", (200, 128, 32)), ("glow1", (248, 208, 88)),
]
POLYPHANT_SHINY = {
    # ash-gray wool and a sun-gold skull-plate, like Monophant's
    "fleece0": (88, 88, 96), "fleece1": (152, 152, 160),
    "bone0": (144, 88, 24), "bone1": (208, 152, 48), "bone2": (240, 200, 96),
    "glow0": (48, 120, 184), "glow1": (152, 216, 248),
}

g_bone = Mat(["bone0", "bone1", "bone2", "white"], line="bone0", cuts=[0.26, 0.5, 0.74])
g_tusk = Mat(["bone1", "bone2", "white"], line="bone0", cuts=[0.36, 0.64])
g_hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.2, 0.44, 0.7])
g_ear = Mat(["hide1", "hide2", "hide3"], line="hide0", cuts=[0.36, 0.62])
g_fleece = Mat(["fleece0", "fleece1", "white"], line="fleece0", cuts=[0.42, 0.66])
g_stone = Mat(["stone0", "stone1", "fleece0"], line="stone0", cuts=[0.36, 0.64])
g_cave = Mat(["ink", "hide0"], line="ink")
g_glow = Mat(["glow0", "glow1"], line="glow0", cuts=[0.5])


def _g_socket(p, cx, cy, r, group, gaze=(0, 0)):
    """The giant's socket: a deep round hollow with a ring of light far
    inside it, so it stares like one great eye."""
    hole = p.circle(cx, cy, r, g_cave, flat=1, group=group)
    inner = p.circle(cx - 0.8, cy - 0.8, r - 1.2, g_cave, flat=0, clip=[hole], group=group, noline=True)
    if p.big:
        gx, gy = cx + gaze[0], cy + gaze[1]
        ring = p.circle(gx, gy, r * 0.5, g_glow, flat=0, clip=[hole, inner], group=group, noline=True)
        lit = p.circle(gx + 0.5, gy + 0.5, r * 0.5 - 0.9, g_glow, flat=1, clip=[ring], group=group, noline=True)
        p.circle(gx, gy, r * 0.22, g_cave, flat=0, clip=[ring, lit], group=group, noline=True)
    return hole


def _fleece(p, locks, **kw):
    """Curly fleece: a mat of round locks [(x, y, r), ...]."""
    for x, y, r in locks:
        p.circle(x, y, r, g_fleece, **kw)


def polyphant(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        st = phase if view == "side" else 0

        walk = view == "side"
        # the door-stone under the raised forefoot (the follower walks
        # without it)
        if not walk:
            p.poly([(2, 57), (3.5, 51.5), (8, 48), (15, 47), (21.5, 48.5), (24.5, 53), (24, 58.5), (19, 61.2), (6, 61.2)],
                   g_stone, group=40)

        # tail
        p.limb(bez((59, 40), (61.5, 43), (61, 48)), 2.2, 1.8, g_hide, group=20)
        p.blob(61, 49.5, 1.6, 2.4, g_fleece, group=21)

        # far legs in shade: the hind column and the planted foreleg
        p.limb([(56.5, 46), (57, 60 - st)], 8.6, 8.0, g_hide, cap=False, bias=0.34, group=10)
        p.limb([(34, 44), (33, 60)], 9.4, 8.8, g_hide, cap=False, bias=0.34, group=11)

        # body: a huge barrel, the forequarters raised, the rump rounding off
        p.blob(43, 40, 17, 13, g_hide, ang=-15, group=1)
        p.blob(53, 44.5, 8.2, 9.2, g_hide, group=1)

        # near hind leg: the great haunch and its column
        p.blob(50.5, 46.5, 8.4, 8.6, g_hide, group=13)
        p.limb([(50, 50), (49.5, 61 - st)], 10.8, 10.4, g_hide, cap=False, group=13)

        # near ear, under the fleece's edge
        ear = p.poly(bez3((27, 12 - L), (37, 11 - L), (42, 22), (38, 35)) + bez((38, 35), (32, 38), (28, 31)), g_hide, group=5)
        p.poly(bez3((29, 15 - L), (35.5, 14.5 - L), (39, 22), (36, 31)) + bez((36, 31), (32, 34), (30, 29)),
               g_ear, clip=[ear], group=5, noline=True)

        # near foreleg raised, the foot set on the boulder; walking, it
        # swings forward and back in step
        p.blob(31, 40, 7, 6.5, g_hide, group=12)
        if walk:
            p.limb([(29.5, 43), (27 - 3 * st, 61)], 10.4, 9.8, g_hide, cap=False, group=12)
        else:
            p.limb([(30, 42), (23.5, 45), (18, 47)], 10.4, 9.4, g_hide, group=12)
            p.blob(16.5, 47, 4.6, 3.2, g_hide, group=12)

        # the fleece cloak over the shoulders and neck, hanging in locks
        _fleece(p, [(36, 18, 6.5), (42.5, 21, 7), (48.5, 26, 6.4), (53, 31.5, 5), (31, 25, 4.5),
                    (38, 26.5, 6.4), (45, 31, 6), (40, 35, 5.4)], group=2)
        _fleece(p, [(28.5, 33.5, 3.4), (33.5, 36.5, 3.8), (39, 39.5, 3.8), (44.5, 38.5, 3.6), (49.5, 37, 3.4),
                    (54, 36, 3.0), (57, 35.5, 2.4)], group=22, bias=0.06)

        # the head: hide skull behind the domed face-plate, the fleece
        # pulled over the crown like a hood
        p.blob(22, 20 - L, 12, 11.5, g_hide, group=3)
        _fleece(p, [(27, 7.5 - L, 3.8), (32, 9 - L, 4.2), (35.5, 13 - L, 4.0), (37, 9.5, 3.4)], group=4)
        p.poly(bez3((5, 22 - L), (4, 4 - L), (26, 0.8 - L), (29.5, 14 - L)) +
               bez3((29.5, 14 - L), (31, 21 - L), (29, 27 - L), (25.5, 31 - L)) +
               [(21.5, 32 - L), (19.5, 27 - L), (13.5, 27 - L)] +
               bez((13.5, 27 - L), (11, 32 - L), (8, 31 - L)) +
               bez((8, 31 - L), (5.5, 27 - L), (5, 22 - L)), g_bone, group=6, bias=-0.04)

        # far tusk, sweeping out behind the trunk
        _g_tusk(p, bez3((10, 29 - L), (4.5, 37 - L), (1.4, 31 - L), (3, 23 - L)), 5.6, bias=0.2, group=8)
        # the long trunk, hanging from the socket and curling at the tip
        p.limb(bez3((16.5, 22 - L), (16.5, 33 - L), (12, 39), (12, 44 + L)), 6.8, 4.4, g_hide, group=9)
        p.limb(bez((12, 44 + L), (12.5, 47.5 + L), (16, 46.5 + L)), 4.4, 3.2, g_hide, group=9)
        _g_socket(p, 16.5, 16 - L, 6.4, 7)
        # near tusk: a great curve forward and up, framing the trunk
        _g_tusk(p, bez3((24, 29 - L), (23.5, 42 - L), (10, 44 - L), (5.5, 32 - L)), 8.4, group=14)

        if p.big:
            p.eye(25.5, 14 - L, 2, 3, shine="white", shine_at=(1, 0))
            p.pxs([(6, 14 - L), (6, 15 - L)], "ink")
            p.stroke([(18, 5 - L), (20, 7 - L), (19, 9 - L)], "bone1")
            for x in (45, 47, 49, 51):
                p.px(x, 60 - st, "white")
            for x in (30, 32, 34):
                p.px(x, 59, "bone1")
        else:
            p.px(16, 16 - L, "glow1")
        return

    if view == "back":
        # over the shoulder: the fleece cloak across a broad back and drawn
        # up over the crown like a hood, the head turned right in profile
        # with the socket's light at the front of the face, the great tusk
        # sweeping forward under it
        p.blob(30, 66, 30, 18, g_hide, group=1)
        p.blob(44, 50, 10, 12, g_hide, group=1)
        # ear lobe hanging below the hood
        p.poly(bez3((38, 30), (34, 34), (35, 44), (41, 47)) + bez((41, 47), (46, 44), (45, 34)), g_hide, group=5)
        # the head
        p.blob(44, 24, 9, 12, g_hide, group=3)
        # the fleece: the cloak on the back and the hood over the crown
        _fleece(p, [(8, 50, 9), (20, 46, 10), (31, 44, 9), (4, 60, 7), (16, 58, 9), (28, 57, 9), (38, 56, 7),
                    (14, 38, 6), (25, 34, 7), (33, 26, 7.4), (38, 17, 7), (44, 11, 6), (37, 34, 5.5)], group=2)
        _fleece(p, [(2, 42, 3.4), (8, 38.5, 4.2), (16, 33, 4.4), (23, 27.5, 4.6), (29, 20, 4.8), (33, 13, 4.6),
                    (38, 8.5, 4.4), (44.5, 5.8, 3.8), (49, 7, 3)], group=22, bias=-0.04)
        p.poly(bez3((45, 14), (48, 7), (56, 6.4), (59.4, 12)) +
               bez3((59.4, 12), (61.4, 18), (61.4, 28), (59.6, 34)) +
               [(56.5, 39.5), (51, 41), (47.5, 37)] + bez3((47.5, 37), (45.5, 31), (44.4, 22), (45, 14)), g_bone, group=6)
        p.limb(bez3((57.5, 31), (60.5, 40), (57, 46), (58.5, 51)), 5.6, 3.6, g_hide, group=9)
        p.limb(bez((58.5, 51), (60, 54), (61.5, 51)), 3.6, 2.8, g_hide, group=9)
        hole = p.blob(57, 23, 2.8, 6.2, g_cave, flat=0, group=7)
        if p.big:
            ring = p.blob(57.8, 23.6, 1.8, 3.8, g_glow, flat=0, clip=[hole], group=7, noline=True)
            p.blob(58.2, 24, 0.9, 2.6, g_glow, flat=1, clip=[ring], group=7, noline=True)
        _g_tusk(p, bez3((50.5, 39), (49, 53), (58, 57), (61.5, 45)), 7.0, group=14)
        p.eye(49, 20, 2, 3, shine="white", shine_at=(0, 0))
        if p.big:
            p.stroke([(51, 9), (53, 11), (52, 13)], "bone1")
        return

    if view == "down":
        # follower walking toward the camera
        st = phase
        for sx in (-1, 1):
            p.limb([(32 + 7.5 * sx, 47), (32 + 7.5 * sx, 61 - 1.5 * (st if sx < 0 else 1 - st))], 8.6, 8.0, g_hide, cap=False,
                   group=12 + (sx > 0))
        p.blob(32, 44, 14, 9.5, g_hide, group=1)
        for sx in (-1, 1):
            p.poly([(32 + sx * 10, 22), (32 + sx * 22, 21), (32 + sx * 24, 33), (32 + sx * 18, 43), (32 + sx * 10, 38)],
                   g_hide, group=5 + (sx > 0) * 10)
            p.poly([(32 + sx * 12, 24.5), (32 + sx * 20, 24.5), (32 + sx * 21.5, 32), (32 + sx * 17.5, 39), (32 + sx * 12, 36)],
                   g_ear, group=5 + (sx > 0) * 10, noline=True)
        _fleece(p, [(20, 40, 4.6), (44, 40, 4.6), (22.5, 34, 5), (41.5, 34, 5), (32, 41, 5)], group=2)
        p.blob(32, 29, 12, 11, g_hide, group=3)
        _fleece(p, [(27, 18, 3.6), (32, 16.5, 4), (37, 18, 3.6)], group=4)
        p.poly(bez3((21, 29), (20, 15), (44, 15), (43, 29)) + [(41.5, 37), (37, 42), (34.5, 37.5), (29.5, 37.5),
                                                                (27, 42), (22.5, 37)], g_bone, group=6)
        _g_tusk(p, bez3((25, 39), (19, 47), (17, 42), (18.5, 36)), 4.2, group=14)
        _g_tusk(p, bez3((39, 39), (45, 47), (47, 42), (45.5, 36)), 4.2, group=15)
        p.limb(bez3((32, 33), (32.5, 42), (30, 47), (32.5 + st, 52)), 5.4, 3.4, g_hide, group=9)
        _g_socket(p, 32, 28, 5.0, 7)
        p.eye(23, 26, 1, 2, shine=None)
        p.eye(40, 26, 1, 2, shine=None)
        return

    if view == "up":
        # follower walking away: the fleece over its back, the rump, the
        # tail, the ears and the tusk tips showing past the head
        st = phase
        for sx in (-1, 1):
            p.limb([(32 + 7.5 * sx, 49), (32 + 7.5 * sx, 61 - 1.5 * (st if sx < 0 else 1 - st))], 9.0, 8.4, g_hide, cap=False,
                   group=12 + (sx > 0))
        _g_tusk(p, bez((22, 33), (17, 34), (17.5, 27)), 3.6, group=30)
        _g_tusk(p, bez((42, 33), (47, 34), (46.5, 27)), 3.6, group=31)
        for sx in (-1, 1):
            p.poly([(32 + sx * 9, 21), (32 + sx * 21, 20), (32 + sx * 23, 31), (32 + sx * 17, 41), (32 + sx * 9, 36)],
                   g_hide, group=5 + (sx > 0) * 10, bias=0.08)
        p.blob(32, 27, 11, 10, g_hide, group=3)
        p.blob(32, 46, 14, 11, g_hide, group=1)
        _fleece(p, [(26, 21, 4), (32, 19.5, 4.4), (38, 21, 4), (32, 25, 4.4), (23, 36, 5.4), (32, 34, 6), (41, 36, 5.4),
                    (25, 43, 4.6), (32, 42, 5), (39, 43, 4.6)], group=2)
        p.limb(bez((32, 50), (33, 54), (32.5 + st, 57)), 2.4, 1.8, g_hide, group=20)
        p.blob(32.5 + st, 58, 1.8, 2.2, g_fleece, group=21)
        return


def _g_tusk(p, path, w, **kw):
    """A great curved tusk, tapering to a blunt point."""
    return p.limb(path, w, max(w * 0.38, 1.4), g_tusk, **kw)


MONS = [
    Mon("Monophant", MONOPHANT_COLORS, MONOPHANT_SHINY, monophant, foot=ELEPHANT_FOOT),
    Mon("Polyphant", POLYPHANT_COLORS, POLYPHANT_SHINY, polyphant, foot=ELEPHANT_FOOT),
]
