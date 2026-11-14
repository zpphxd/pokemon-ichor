"""Torpedo line: Narkeray (Water / Electric), a single stage. Meno's numbfish.

In Plato's Meno, Meno tells Socrates he is like the flat torpedo fish, the
narke, which numbs whoever touches it; Socrates answers that he numbs others
only because he is numb himself (Meno 80a-c). Narkeray is the ray of that
simile wearing the face it was compared to: its own eyes, a bald dome,
furrow ridges, a snub nose and a fringe of beard curls are marked on its
back, flanked by two glowing kidney-shaped electric organs.
"""
from mon_lib import C, Mat, Mon, bez3

INK = C.ink

NARKERAY_COLORS = [
    ("ink", INK),
    # limestone-sand back, dark to pale
    ("s0", (104, 80, 56)), ("s1", (152, 120, 80)), ("s2", (192, 160, 112)), ("s3", (224, 200, 152)),
    ("s4", (240, 232, 200)),
    # Aegean-blue fin rims
    ("b0", (24, 56, 120)), ("b1", (48, 104, 176)), ("b2", (112, 168, 224)),
    # the marble belly edge
    ("m0", (176, 168, 160)), ("m1", (224, 216, 208)), ("white", C.white),
    # the sun-gold glow of the electric organs
    ("g0", (200, 128, 32)), ("g1", (240, 192, 64)), ("g2", (248, 240, 168)),
]
NARKERAY_SHINY = {
    # the sandy back turns Aegean blue and the glow white; the rims take the sand
    "s0": (24, 40, 88), "s1": (40, 72, 136), "s2": (64, 112, 184), "s3": (104, 152, 216), "s4": (168, 208, 240),
    "b0": (104, 80, 56), "b1": (176, 144, 96), "b2": (224, 200, 152),
    "g0": (152, 168, 192), "g1": (216, 224, 232), "g2": (248, 248, 248),
}

sand = Mat(["s0", "s1", "s2", "s3"], line="s0", cuts=[0.16, 0.42, 0.72])
rimm = Mat(["b0", "b1", "b2"], line="b0", cuts=[0.4, 0.7])
belly = Mat(["m0", "m1", "white"], line="m0", cuts=[0.4, 0.7])
glow = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.45, 0.75])


def _wing_disc(F=0, k=1.0, ox=0.0, oy=0.0):
    """The disc outline in 3/4 view: a crescent, the body low in the middle
    and the round wings rising to curled tips. F lifts the tips."""
    top = bez3((3.5, 31 - F), (12, 17), (44, 10.6), (60, 17.4 - F), n=24)
    bot = bez3((60, 17.4 - F), (61.4, 38), (13, 58), (3.5, 31 - F), n=28)
    return [(ox + x * k, oy + y * k) for x, y in top + bot[1:-1]]


def _rim_band(F=0, k=1.0, ox=0.0, oy=0.0, t=2.2):
    """The blue rim along the leading (lower) edge."""
    outer = bez3((60, 17.4 - F), (61.4, 38), (13, 58), (3.5, 31 - F), n=28)
    inner = bez3((58.4, 20 - F), (58.4, 36.6 - t), (14.6, 55 - t), (5.2, 33 - F), n=28)
    return [(ox + x * k, oy + y * k) for x, y in outer + inner[::-1]]


def _front(p, F):
    """The battle front, also the side and icon: 3/4 facing left, gliding,
    the face markings hand-painted in the art files."""
    # the short thick tail behind, rising to the upper right, two small
    # dorsal fins and a paddle of a caudal fin
    tail = [(43, 21), (48, 14.6), (52, 9.6 - F)]
    p.lens((45.6, 17.6), (46.6, 11.6), 4, rimm, bend=0.8, group=31)
    p.lens((49.4, 13), (50.4, 7.8), 3.4, rimm, bend=0.8, group=32)
    p.limb(tail, 9.4, 6, sand, group=30, bias=0.06)
    p.lens((51, 11), (59.4, 4.4 - F), 6.4, rimm, bend=-1.6, group=33)
    p.lens((52.6, 10.6), (60, 12 - F), 4.6, rimm, bend=1.2, group=34)
    # the disc: sand back, blue leading edge, marble underside at the tips
    p.poly(_wing_disc(F), sand, group=1)
    p.poly(_rim_band(F), rimm, group=2)
    p.lens((4, 31.4 - F), (11.4, 44), 3.8, belly, bend=-1.4, group=3)
    p.lens((59.6, 18 - F), (58, 30), 3.2, belly, bend=1.2, group=4)
    if p.big:
        # the two kidney-shaped electric organs glowing under the skin
        p.blob(15, 34, 3.6, 5.2, glow, ang=-30, group=40, noline=True)
        p.blob(46.4, 28.6, 3.2, 4.6, glow, ang=20, group=41, noline=True)
        p.eye(24, 28, 3, 4, shine="white", shine_at=(1, 1))
        p.eye(33, 27, 3, 4, shine="white", shine_at=(1, 1))
    else:
        p.blob(15.6, 35.6, 2.6, 3.4, glow, noline=True)
        p.blob(45.4, 33.6, 2.4, 3.2, glow, noline=True)
        p.px(25, 30, "ink")
        p.px(34, 29, "ink")


def narkeray(p, view, phase):
    if view in ("front", "icon", "side"):
        F = 1 if (phase == 1 and view in ("front", "side")) else 0
        p.oy += 8 * p.s        # it glides low, its lowest point near row 51
        _front(p, F)
        p.oy -= 8 * p.s
        return

    if view == "back":
        # over the shoulder, about 1.2x: banking away into a turn to the
        # right, so the wings tilt across the frame and the two organs sit
        # at different heights (level, they read as a skull's eyes); the
        # thick tail sweeps toward us off the lower left, cropped. The art
        # file paints the raised body, the bald pate and its furrows.
        far = bez3((3, 13), (24, 1.6), (58, 8), (61.6, 33), n=28)
        near = bez3((61.6, 33), (63, 58), (16, 60), (3, 13), n=30)
        p.poly(far + near[1:-1], rimm, group=1)
        inner_far = bez3((5, 14.4), (24.6, 4.4), (56.4, 10), (59.6, 33), n=28)
        inner_near = bez3((59.6, 33), (60.6, 55.6), (17.6, 57.6), (5, 14.4), n=30)
        p.poly(inner_far + inner_near[1:-1], sand, group=1, noline=True)
        p.lens((3.6, 13.6), (5, 26.6), 3.8, belly, bend=-1.4, group=3)
        p.lens((61.2, 33.6), (59.6, 44), 3.4, belly, bend=1.4, group=4)
        # the thick tail sweeping toward us off the lower left, with its fins
        p.limb([(28, 50), (20, 57), (12, 66)], 12, 10, sand, group=30)
        p.lens((24.6, 52.4), (17, 47.6), 5, rimm, bend=-1, group=31)
        p.lens((17.6, 58.6), (8.6, 55.4), 5, rimm, bend=-1, group=32)
        if p.big:
            p.blob(15, 23, 3.6, 5, glow, ang=-55, group=40, noline=True)
            p.blob(51.4, 40, 3.6, 5, glow, ang=-10, group=41, noline=True)
        return

    if view in ("down", "up"):
        # follower: gliding toward us (down) or away (up), the fin tips
        # beating; it floats a hand's breadth off the ground
        F = 2 * phase
        top = bez3((5, 31 - F), (14, 18), (50, 18), (59, 31 - F), n=24)
        bot = bez3((59, 31 - F), (61, 49), (3, 49), (5, 31 - F), n=24)
        if view == "up":
            p.limb([(32, 44), (32, 55)], 8, 5, sand, group=30)
            p.lens((32, 54), (26.4, 59.4), 4.6, rimm, bend=0.8, group=31)
            p.lens((32, 54), (37.6, 59.4), 4.6, rimm, bend=-0.8, group=32)
        p.poly(top + bot[1:-1], rimm, group=1)
        top_i = bez3((6.6, 32 - F), (15, 20.4), (49, 20.4), (57.4, 32 - F), n=24)
        bot_i = bez3((57.4, 32 - F), (58.4, 46.4), (5.6, 46.4), (6.6, 32 - F), n=24)
        p.poly(top_i + bot_i[1:-1], sand, group=1, noline=True)
        p.lens((5.4, 31.4 - F), (9.6, 41), 3.4, belly, bend=-1.2, group=3)
        p.lens((58.6, 31.4 - F), (54.4, 41), 3.4, belly, bend=1.2, group=4)
        p.blob(32, 33.4, 9, 6.4, sand, group=5, bias=-0.22, noline=True)
        p.blob(16.6, 35.6, 2.8, 4, glow, ang=-20, noline=True, group=40)
        p.blob(47.4, 35.6, 2.8, 4, glow, ang=20, noline=True, group=41)
        if view == "down":
            p.eye(26.6, 32, 3, 4, shine="white", shine_at=(1, 1))
            p.eye(34.4, 32, 3, 4, shine="white", shine_at=(1, 1))
            p.blob(32, 42, 6.6, 2.6, sand, group=6, bias=0.3, noline=True)     # the beard
        return


MONS = [
    Mon("Narkeray", NARKERAY_COLORS, NARKERAY_SHINY, narkeray, foot="blank"),
]
