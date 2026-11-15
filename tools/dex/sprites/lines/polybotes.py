"""Polybotes line: Kapnub, Gigantomb (Fire, then Fire/Rock). The giant
Polybotes, whom Poseidon buried under a piece of Kos that became the volcanic
island of Nisyros; its smoke is the giant's breath (Apollodorus 1.6.2;
Strabo 10.5.16)."""
import math

from mon_lib import C, Mat, Mon, bez3, ellipse_pts, lens_pts

INK = C.ink

# --------------------------------------------------------------------------
# Kapnub, the smoldering cinder
# --------------------------------------------------------------------------

KAPNUB_COLORS = [
    ("ink", INK),
    # dark gray crust, cooling
    ("crust0", (48, 40, 48)), ("crust1", (80, 72, 80)), ("crust2", (120, 112, 112)), ("crust3", (168, 160, 152)),
    # the glow in the cracks: terracotta to sun-gold to white heat
    ("glow0", (152, 48, 24)), ("glow1", (216, 96, 40)), ("glow2", (248, 168, 56)), ("glow3", (248, 232, 152)),
    # marble-gray smoke
    ("smoke0", (128, 120, 128)), ("smoke1", (184, 176, 176)), ("smoke2", (232, 232, 224)),
]
KAPNUB_SHINY = {
    # ash-pale crust, the glow turned blue
    "crust0": (112, 104, 112), "crust1": (160, 152, 152), "crust2": (200, 192, 192), "crust3": (232, 232, 224),
    "glow0": (40, 56, 136), "glow1": (64, 112, 200), "glow2": (120, 184, 248), "glow3": (208, 240, 248),
}

k_crust = Mat(["crust0", "crust1", "crust2", "crust3"], line="crust0", cuts=[0.24, 0.48, 0.74])
k_smoke = Mat(["smoke0", "smoke1", "smoke2"], line="smoke0", outline="smoke0", cuts=[0.36, 0.7])


def _curl(p, x, y, L=0, s=1.0):
    """The thin curl of smoke off the crown, base at (x, y)."""
    p.limb(bez3((x, y), (x - 2 * s, y - 4 * s), (x + 3 * s, y - 6 * s), (x + 1 * s, y - 10 * s + L)),
           2.0 * s, 1.4 * s, k_smoke, group=30)
    p.circle(x - 1.5 * s + L, y - 12 * s + L, 1.6 * s, k_smoke, group=31)


def kapnub(p, view, phase):
    if view in ("front", "side", "icon"):
        L = phase if view == "front" else 0
        roll = phase if view == "side" else 0
        # far nub arm, behind; the battle sprites are hand-finished from
        # this as crust plates split by glowing seams (art/kapnub_*.txt)
        p.blob(45.5, 47 - L - roll, 3.4, 2.8, k_crust, ang=-30, bias=0.3, group=10)
        # the cinder: a domed crown over a flat base, a dark face plate in front
        top = [pt for pt in ellipse_pts(31, 47 - 0.5 * L, 13.5, 12.5 + 0.5 * L, n=48) if pt[1] <= 52]
        top.sort(key=lambda pt: math.atan2(pt[1] - 47, pt[0] - 31))
        base = [(43.6, 51), (44.6, 54), (43.2, 57.4), (18.8, 57.4), (17.4, 54), (18.4, 51)]
        dome = p.polys([top, base], k_crust, group=1)
        p.blob(25, 45.5 - 0.5 * L, 7, 6.5, k_crust, bias=0.2, clip=[dome], group=1)
        # cracks glowing through the crust
        if p.big:
            for path in ([(32, 37), (33, 43), (31, 47), (32, 52), (30, 57)], [(33, 43), (38, 44), (43, 43)],
                         [(32, 52), (38, 50), (44, 52)], [(21, 51), (26, 52), (31, 52)], [(38, 50), (40, 57)]):
                p.stroke(path, "glow1")
        # near nub arm
        p.blob(17.5, 54 + L - roll, 3.8, 3.0, k_crust, ang=20, group=11)
        _curl(p, 32, 35 - L, L)
        if p.big:
            # two glowing eye-slits and a little glowing mouth
            p.patch(20, 41 - L, [".11...1111.", "1891.178871", "1981.189981", "1871.178871", ".11...1111."],
                    {"1": "ink", "7": "glow1", "8": "glow2", "9": "glow3"})
            p.patch(23, 48 - L, ["1....1", ".1871.", "..11.."], {"1": "ink", "7": "glow1", "8": "glow2"})
        else:
            p.pxs([(21, 43 - L), (28, 43 - L)], "glow3")
        return

    if view == "back":
        # over the shoulder: the cracked crown, the smoke curl, the
        # eye-slits turned right in profile
        p.blob(30, 54, 21, 16, k_crust, ang=-10, group=1)
        p.blob(36, 42, 14, 10, k_crust, group=1)
        p.blob(53, 47, 4, 3.4, k_crust, ang=-20, group=11)
        if p.big:
            for path in (([16, 50], [22, 53], [24, 58]), ([22, 53], [27, 51]), ([31, 44], [36, 47], [41, 45]),
                         ([12, 58], [16, 61]), ([36, 56], [40, 60], [46, 59])):
                p.stroke(path, "glow1")
            p.patch(44, 43, ["1111", "1cd1", ".11."], {"1": "ink", "c": "glow2", "d": "glow3"})
        _curl(p, 36, 33, 0, 1.4)
        return

    if view in ("down", "up"):
        # follower: rolling after the player, trailing smoke
        L = phase
        p.blob(32, 50, 9.5, 8.5 - 0.5 * L, k_crust, ang=12 * L, group=1)
        p.blob(22.5, 52, 2.4, 2.2, k_crust, group=11)
        p.blob(41.5, 52, 2.4, 2.2, k_crust, group=12)
        _curl(p, 32 + L, 42, L, 0.9)
        if view == "down":
            p.patch(26, 47, ["111..111", "1dc..cd1"], {"1": "ink", "c": "glow2", "d": "glow3"})
            p.stroke([(31, 53), (33, 53)], "glow1")
        else:
            p.stroke([(27, 49), (31, 52), (34, 51), (37, 54)], "glow1")
        return


# --------------------------------------------------------------------------
# Gigantomb, the buried giant
# --------------------------------------------------------------------------

GIGANTOMB_COLORS = [
    ("ink", INK),
    # dark basalt skin, ink to marble-gray
    ("bas0", (48, 40, 56)), ("bas1", (80, 72, 88)), ("bas2", (120, 112, 120)), ("bas3", (168, 160, 160)),
    # furnace cracks: terracotta, sun-gold, white heat
    ("lava0", (184, 64, 32)), ("lava1", (240, 152, 48)), ("lava2", (248, 232, 152)),
    # the island on its back: limestone, marble whitewash, olive, Aegean blue
    ("lime0", (152, 120, 80)), ("lime1", (200, 176, 128)), ("lime2", (232, 216, 176)),
    ("white", C.white),
    ("olive0", (64, 80, 40)), ("olive1", (120, 144, 64)),
    ("aegean", (48, 104, 176)),
]
GIGANTOMB_SHINY = {
    # ash-white skin, blue cracks, a terracotta door
    "bas0": (104, 96, 112), "bas1": (152, 144, 152), "bas2": (192, 184, 192), "bas3": (232, 232, 232),
    "lava0": (40, 64, 168), "lava1": (88, 152, 240), "lava2": (200, 232, 248),
    "aegean": (184, 88, 48),
}

g_bas = Mat(["bas0", "bas1", "bas2", "bas3"], line="bas0", cuts=[0.22, 0.46, 0.72])
g_dark = Mat(["ink", "bas0", "bas1", "bas2"], line="ink", cuts=[0.22, 0.5, 0.78])
g_lime = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.34, 0.66])
g_wall = Mat(["lime1", "lime2", "white"], line="lime0", cuts=[0.3, 0.6])
g_olive = Mat(["olive0", "olive1"], line="olive0", cuts=[0.5])
g_trunk = Mat(["bas0", "lime0"], line="bas0", cuts=[0.5])
g_smoke = Mat(["bas2", "bas3", "white"], line="bas2", outline="bas1", cuts=[0.34, 0.68])
g_lava = Mat(["lava0", "lava1", "lava2"], line="lava0", outline="ink", cuts=[0.3, 0.62])
g_door = Mat(["aegean"])


def _olive(p, x, y, s=1.0, **kw):
    """A small gnarled olive tree, trunk foot at (x, y)."""
    p.limb([(x, y), (x - 0.6 * s, y - 3 * s)], 1.6 * s, 1.2 * s, g_trunk, **kw)
    p.blob(x - 0.8 * s, y - 4.6 * s, 3.4 * s, 2.6 * s, g_olive, **kw)
    p.blob(x + 1.6 * s, y - 3.6 * s, 2.0 * s, 1.8 * s, g_olive, **kw)


def _hut(p, x, y, door=True):
    """The whitewashed hut, its top-left corner at (x, y): 7 wide, 6 tall,
    a flat roof and an Aegean-blue door."""
    p.rect(x, y, x + 6, y + 5, g_wall, group=90)
    if door:
        p.rect(x + 2, y + 2, x + 3, y + 5, g_door, group=91, noline=True)


def gigantomb(p, view, phase):
    if view in ("front", "side", "icon"):
        # the giant heaving out of the ground, arms braced either side, the
        # island riding its back; the battle sprites are hand-finished from
        # this (art/gigantomb_*.txt)
        L = phase if view == "front" else 0
        sw = phase if view == "side" else 0
        big = p.big
        # the back sloping away into the ground at the right
        p.blob(53, 40, 10, 19, g_bas, bias=0.12, group=1)
        p.blob(46, 30, 13, 9, g_bas, bias=0.12, group=1)
        # the island on its back: a limestone hill, a whitewashed hut with an
        # Aegean-blue door, two olive trees and a smoking vent
        p.blob(46, 21, 16, 6.5, g_lime, group=60)
        p.blob(47.5, 14.5, 10, 7.5, g_lime, group=60)
        p.blob(37, 19.5, 6, 4, g_lime, group=60)
        _olive(p, 34, 20, 1.3, group=62)
        _hut(p, 42, 4)
        _olive(p, 58, 18, 1.3, group=63)
        if view == "front":
            p.blob(37, 6 - L, 2.4, 2.2, g_smoke, group=80)
            p.blob(38.5, 10 - L, 1.6, 1.6, g_smoke, group=80)
        # far arm (the giant's right) braced at the left
        p.blob(9, 35, 7.5, 7.5, g_bas, bias=0.15, group=11)
        p.limb([(8.5, 39), (6, 47), (7.5, 53)], 9.5, 8, g_bas, bias=0.18, group=11)
        p.blob(8.5, 55.5 + sw, 7.2, 4, g_bas, bias=0.18, group=12)
        # the chest heaving out of the rubble
        p.blob(25, 47, 13, 10.5, g_bas, group=2)
        # near shoulder and arm (the giant's left) braced at the right
        p.blob(41, 33, 11.5, 11, g_bas, group=3)
        p.limb([(42.5, 40), (44, 48), (42, 53)], 12, 10, g_bas, group=4)
        p.blob(40.5, 55.5 - sw, 9.6, 4.8, g_bas, group=5)
        # the head, a crag thrust forward between the shoulders: crown crags
        # sweeping back, a rounded brow shelf jutting forward, a heavy jaw
        crag = lambda pts: [(x, y - L) for x, y in pts]
        p.polys([crag([(9.5, 19), (11.5, 13.5), (14.4, 8.6), (15.6, 9.2), (16.4, 12.5), (17.2, 19)]),
                 crag([(16.5, 19), (19.5, 12.5), (24.4, 4.6), (25.8, 5.2), (26.2, 8.6), (27.6, 9.6), (27, 13),
                       (27.6, 19)]),
                 crag([(24.5, 20), (26.6, 15.8), (28.6, 12.4), (29.6, 13.4), (29.8, 20)])], g_bas, group=6)
        p.blob(18.5, 27.5 - L, 9.5, 9.5, g_bas, group=7)
        p.blob(14.5, 29.5 - L, 8.5, 5.5, g_bas, group=7)
        p.blob(13.5, 36, 9, 4.6, g_bas, ang=6, group=8)
        p.blob(7.5, 36.5, 3.8, 3.4, g_bas, group=8)
        p.blob(14, 21.5 - L, 9.8, 3.9, g_bas, ang=-5, bias=-0.15, group=9)
        p.blob(22, 20.5 - L, 6.5, 3.4, g_bas, bias=-0.1, group=9)
        # the furnace maw: one glowing opening in a dark rim
        rim = p.poly(lens_pts((5.5, 32.2 - L * 0.5), (20.5, 32.2 - L * 0.5), 4.6 + L, fat=0.4), g_dark, group=10, flat=0)
        p.poly(lens_pts((7.5, 32.4 - L * 0.5), (19, 32.4 - L * 0.5), 3.0 + L, fat=0.4), g_lava, clip=[rim], group=11,
               noline=True)
        # rubble heaved up around it
        for pts in ([(15, 62.5), (17, 57.5), (22, 56), (25.5, 58.5), (24.5, 62.5)],
                    [(48, 62.5), (50, 58.5), (55, 57.5), (58, 59.5), (57, 62.5)]):
            p.poly(pts, g_dark, group=20)
        if view == "front":
            # one plume of smoke pouring from the maw, curling back over the crown
            for k, (cx, cy, r) in enumerate(((3.5, 30.5, 2.4), (2.6, 24, 2.2), (4, 16, 3.4), (7, 8.5, 4.0),
                                             (12, 5.2, 3.2), (15.5, 6.5, 1.8))):
                p.blob(cx, cy - L, r, r * 0.9, g_smoke, group=81 + k)
        if big:
            p.patch(16, 26 - L, ["..1111", ".1c871", "188761", "17611."], {"1": "ink", "6": "lava0", "7": "lava1", "8": "lava2", "c": "white"})
            p.patch(9, 26 - L, ["111.", "1c81", "1871", ".161"], {"1": "ink", "6": "lava0", "7": "lava1", "8": "lava2", "c": "white"})
            for path in ([(14, 46), (18, 44), (22, 47), (26, 45), (30, 48), (34, 46)], [(34, 26), (37, 30), (35, 34), (39, 37)],
                         [(56, 29), (58, 35), (55, 41), (58, 47)], [(23, 8), (21, 13), (18, 18), (15, 20)]):
                p.stroke(path, "lava1")
        else:
            p.pxs([(10, 27 - L), (18, 27 - L)], "lava2")
        return

    if view == "back":
        # over the shoulder: the island close up on the giant's back, the
        # hut's chimney smoking, the head turned right in profile
        p.blob(17, 5, 3, 2.6, g_smoke, group=80)
        p.blob(20, 10, 2.4, 2.2, g_smoke, group=80)
        p.blob(28, 62, 30, 20, g_bas, group=1)
        p.blob(44, 40, 14, 14, g_bas, group=1)
        p.blob(24, 40, 20, 8, g_lime, group=60)
        p.blob(24, 33, 13, 8, g_lime, group=60)
        p.rect(20, 12, 21, 18, g_wall, group=92)
        _hut(p, 17, 19, door=False)
        p.rect(19, 21, 20, 24, g_door, group=91, noline=True)
        _olive(p, 9, 36, 1.6, group=62)
        _olive(p, 35, 32, 1.4, group=63)
        p.blob(50, 30, 10, 10, g_bas, group=3)
        p.blob(54, 39, 7.6, 5, g_bas, group=3)
        p.lens((40, 24), (60, 27), 6.6, g_bas, bend=-1.2, group=4)
        p.blob(57, 40, 4, 2.4, g_lava, group=5)
        p.blob(60, 36, 2.4, 2.2, g_smoke, group=81)
        if p.big:
            p.patch(53, 28, ["1111", "1dd1", ".11."], {"1": "ink", "d": "lava2"})
            for path in ([(6, 50), (12, 54), (16, 52)], [(30, 50), (36, 46), (42, 49)], [(46, 54), (52, 58)]):
                p.stroke(path, "lava1")
        return

    if view == "down":
        # follower: the giant hauling itself toward the player on its arms,
        # the crag head between its shoulders, the hut riding behind
        st = phase
        p.blob(46, 17, 10, 5, g_lime, group=60)
        _hut(p, 45, 6)
        _olive(p, 54, 16, 1.4, group=61)
        for sx in (-1, 1):
            k = st if sx < 0 else 1 - st
            p.blob(32 + 17 * sx, 32, 10, 9.5, g_bas, group=10 + (sx > 0))
            p.limb([(32 + 19 * sx, 36), (32 + 23 * sx, 46), (32 + 22 * sx, 53 - 2 * k)], 11, 9, g_bas,
                   group=12 + (sx > 0))
            p.blob(32 + 22 * sx, 56 - 2 * k, 8, 4, g_bas, group=14 + (sx > 0))
        p.blob(32, 47, 13, 9, g_bas, group=2)
        for a2, b2, w in (((25, 20), (20, 8), 5.6), ((32, 18), (32, 5), 6.4), ((39, 20), (44, 8), 5.6)):
            p.lens(a2, b2, w, g_bas, fat=0.28, group=4)
        p.blob(32, 27, 11.5, 10, g_bas, group=5)
        p.blob(32, 37, 10, 4.6, g_bas, group=6)
        p.blob(32, 22.5, 13, 4, g_bas, group=7)
        # the furnace maw: a dark-rimmed opening with one glowing interior
        rim = p.poly(lens_pts((23.5, 33), (40.5, 33), 6.0, fat=0.5), g_dark, group=8, flat=0)
        p.poly(lens_pts((25, 33.2), (39, 33.2), 4.0, fat=0.5), g_lava, clip=[rim], group=9, noline=True)
        p.poly([(12, 62), (17, 58.5), (47, 58.5), (52, 62)], g_dark, group=20)
        if p.big:
            p.patch(23, 26, [".1111.", "1c8871", ".1111."], {"1": "ink", "7": "lava1", "8": "lava2", "c": "white"})
            p.patch(35, 26, [".1111.", "1788c1", ".1111."], {"1": "ink", "7": "lava1", "8": "lava2", "c": "white"})
            for path in ([(24, 46), (29, 49), (34, 46), (40, 49)], [(32, 16), (31, 21)]):
                p.stroke(path, "lava1")
        else:
            p.pxs([(26, 27), (37, 27)], "lava2")
        return

    if view == "up":
        # follower walking away: the island on its back, hut and olives and
        # the smoking chimney, the crags of its head beyond
        st = phase
        for a2, b2, w in (((28, 34), (26, 27), 3.6), ((32, 33), (32, 26), 4.2), ((36, 34), (38, 27), 3.6)):
            p.lens(a2, b2, w, g_bas, fat=0.3, group=4)
        p.blob(32, 37, 8, 5, g_bas, group=3)
        p.blob(32, 50, 16, 9, g_bas, group=1)
        for sx in (-1, 1):
            k = st if sx < 0 else 1 - st
            p.blob(32 + 15 * sx, 56 - k, 4.6, 2.8, g_bas, group=12 + (sx > 0))
        p.blob(32, 45, 12.5, 6, g_lime, group=60)
        p.blob(32, 40.5, 8, 4.5, g_lime, group=60)
        _hut(p, 29, 33)
        _olive(p, 22, 46, 1.4, group=62)
        _olive(p, 42, 45, 1.4, group=63)
        p.blob(34 + st, 29 - st, 1.8, 1.6, g_smoke, group=80)
        p.poly([(15, 61), (19, 57), (45, 57), (49, 61)], g_dark, group=20)
        if p.big:
            for path in ([(20, 52), (26, 55), (31, 53)], [(36, 54), (42, 52), (46, 55)]):
                p.stroke(path, "lava1")
        return


MONS = [
    Mon("Kapnub", KAPNUB_COLORS, KAPNUB_SHINY, kapnub, foot="blank"),
    Mon("Gigantomb", GIGANTOMB_COLORS, GIGANTOMB_SHINY, gigantomb, foot="hand"),
]
