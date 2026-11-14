"""Diogenes line: Pithound (Dark / Psychic), a single stage. The Cynic in his jar.

Diogenes slept in a pithos in the Agora, walked it with a lamp lit in broad
daylight looking for an honest man, and asked Alexander to stand out of his
sun (Diogenes Laertius 6). The Cynics were the "dog-like" philosophers.
Pithound is a scruffy, bearded dog lying half out of a cracked jar tipped on
its side, chin on its paws, one brow tuft raised; its tail comes up through
the crack and holds a little clay lamp over its head, lit at noon.
"""
import math

from mon_lib import C, Mat, Mon, bez3

INK = C.ink

PITHOUND_COLORS = [
    ("ink", INK),
    # the jar: unglazed terracotta
    ("t0", (104, 40, 24)), ("t1", (160, 72, 40)), ("t2", (208, 112, 64)), ("t3", (232, 160, 112)),
    # black-figure paint on the jar (its own slot, so the shiny can invert it)
    ("fig", (48, 32, 32)),
    # limestone-gray fur
    ("f0", (80, 72, 80)), ("f1", (128, 120, 120)), ("f2", (176, 168, 160)), ("f3", (216, 208, 200)),
    # the lamp's sun-gold flame
    ("gold", (240, 176, 48)), ("flame", (248, 232, 136)),
    # dusky violet: the jar's dark inside and the glint in its eyes
    ("v0", (64, 40, 88)), ("v1", (152, 104, 192)),
    ("white", C.white),
]
PITHOUND_SHINY = {
    # a black jar with terracotta figures, like red-figure pottery
    "t0": (24, 24, 32), "t1": (48, 48, 56), "t2": (80, 72, 80), "t3": (120, 112, 120),
    "fig": (216, 120, 64),
}

jar = Mat(["t0", "t1", "t2", "t3"], line="t0", cuts=[0.2, 0.46, 0.74])
rim = Mat(["t1", "t2", "t3"], line="t0", cuts=[0.36, 0.7])
inside = Mat(["v0", "t0"], line="v0", cuts=[0.7])
fur = Mat(["f0", "f1", "f2", "f3"], line="f0", cuts=[0.12, 0.32, 0.72])
pale = Mat(["f1", "f2", "f3"], line="f0", cuts=[0.56, 0.86])
lamp = Mat(["t0", "t1", "t2"], line="t0", cuts=[0.4, 0.7])
flame = Mat(["gold", "flame"], line="gold", cuts=[0.5])


def _jar_poly(cx, cy, r, bx, by, br, n=36):
    """A pithos lying on its side: the round shoulder (circle at cx, cy)
    tapering to a narrow base (circle at bx, by)."""
    d = math.hypot(bx - cx, by - cy)
    a = math.atan2(by - cy, bx - cx)
    t = math.acos((r - br) / d)
    pts = []
    for i in range(n + 1):
        ang = a + t + (2 * math.pi - 2 * t) * i / n
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    for i in range(n // 3 + 1):
        ang = a - t + 2 * t * i / (n // 3)
        pts.append((bx + br * math.cos(ang), by + br * math.sin(ang)))
    return pts


def _lamp(p, x, y, F=0):
    """A small clay oil lamp hanging by its handle at (x, y): a round squat
    body, the nozzle to the left, lit with a sun-gold flame."""
    p.blob(x - 1, y + 4.6, 4.2, 2.6, lamp)
    p.limb([(x - 3.6, y + 4.2), (x - 7, y + 3.4)], 2.6, 2, lamp)
    p.drop((x - 8.4 - F * 0.5, y - 2.4), x - 8, y + 1.6, 1.8, flame)


def pithound(p, view, phase):
    if view in ("front", "icon"):
        F = 1 if (phase == 1 and view == "front") else 0
        # the tail, up through the crack, curling over to hold the lamp
        tail = bez3((41, 39), (42, 25), (33, 15.5 - F), (28.5, 20 - F), n=18)
        p.limb(tail, 4.4, 3.2, fur, group=40, bias=0.1)
        _lamp(p, 28, 21 - F, F)
        # the jar, tipped on its side, mouth to the left
        p.poly(_jar_poly(38.5, 48.5, 11.2, 47, 47.6, 8.6), jar, group=1)
        p.blob(54.6, 47.6, 1.8, 6, rim, group=2)                       # the foot
        p.blob(29.6, 48.6, 3.4, 9.6, rim, group=3)                     # the rolled rim
        p.blob(28.8, 48.6, 2.4, 7.6, inside, group=4, noline=True)     # the dark inside
        # the dog: shaggy shoulders filling the mouth of the jar
        p.blob(28, 48.5, 4.6, 8.6, fur, group=10, bias=0.12)
        # the head, turned toward us, resting on its paws: lop ears, a short
        # muzzle with a big nose pad, bushy brows and a beard
        p.lens((15.5, 40), (10, 51.5), 5.6, fur, bend=1.4, group=13, bias=0.3)     # far ear
        p.blob(20, 45.2, 8, 7, fur, group=14, bias=-0.1)
        p.lens((25.6, 40), (29.4, 52.6), 6.4, fur, bend=-1.6, group=15, bias=0.22)  # near ear
        p.blob(14.6, 50.2, 6.4, 4.4, pale, ang=-6, group=16)                        # muzzle
        p.lens((16.5, 53), (14, 59.4), 9.6, pale, bend=-0.6, group=17)             # beard
        p.lens((10.6, 52.6), (8.4, 57.6), 4.4, pale, bend=-0.4, group=18)
        p.lens((18.2, 43.4), (25.4, 39.4), 4, pale, bend=1.0, group=19)            # raised brow
        p.lens((10.4, 44.6), (16, 44), 3.4, pale, bend=0.6, group=20)              # low brow
        # paws, side by side on the ground under the beard
        p.limb([(26, 58.2), (19.5, 58.4)], 4.6, 4.4, fur, group=11, bias=0.08)
        p.limb([(12, 58.2), (6.8, 58.4)], 4.6, 4.4, fur, group=12)
        if p.big:
            p.eye(18, 44, 4, 4, iris="v1", shine="white", shine_at=(1, 2))
            p.eye(11.6, 45, 3, 3, iris="v1", shine=None)
            p.patch(9, 46, [".11.", "1f11", "1111", ".11."], {"1": "ink", "f": "f2"})
        else:
            p.px(19, 46, "ink")
        return

    if view == "side":
        # follower: trudging left with the jar on its back like a shell
        st = phase
        for x, d in ((19, st), (24, -st), (36, -st), (41, st)):
            p.limb([(x, 50), (x - 1 + d, 59)], 3.8, 3.4, fur, group=10 + x)
        p.limb(bez3((40, 38), (41, 28), (33, 22), (28, 25.6), n=14), 3.6, 2.8, fur, group=40)
        _lamp(p, 28, 26.4)
        p.poly(_jar_poly(33, 42, 10, 46, 40.4, 3.6), jar, group=1)
        p.blob(23.6, 42.4, 3.2, 9.2, rim, group=3)
        p.blob(22.8, 42.4, 2.2, 7.2, inside, group=4, noline=True)
        p.blob(20, 45, 5.2, 5.6, fur, group=12)
        p.blob(15.4, 42, 5.4, 5, fur, group=13)
        p.limb([(13, 44), (8, 44.6)], 4.6, 3.6, fur, group=13)
        p.lens((17.5, 38.5), (17.5, 46.5), 4, fur, bend=-1, group=14)
        p.lens((12.5, 45.6), (9.5, 49.4), 3.6, pale, group=16)
        if p.big:
            p.eye(11, 40, 2, 2, iris=None, shine=None)
            p.px(6, 44, "ink")
        return

    if view == "back":
        # over the shoulder, about 1.2x: the jar's base and cracked belly
        # toward us (cropped below), the tail up through the crack holding
        # the lamp high, the dog's head out of the far mouth in right
        # profile, chin on its paws
        tail = bez3((22, 40), (19, 22), (30, 11), (40, 15.5), n=20)
        p.limb(tail, 5.6, 4.2, fur, group=40, bias=0.1)
        p.blob(44.6, 21.6, 5, 3, lamp)
        p.limb([(49, 21), (53, 19.6)], 3, 2.4, lamp)
        p.drop((55.6, 13), 54.6, 17.4, 2.2, flame)
        p.poly(_jar_poly(27, 52, 15, 8, 55, 10), jar, group=1)
        p.blob(4.6, 55, 2.6, 8.6, rim, group=2)                       # the foot
        p.blob(41, 51, 4, 13, rim, group=3)                           # the far rim
        p.blob(41.8, 51, 2.8, 11, inside, group=4, noline=True)
        p.blob(43, 52, 5, 9.6, fur, group=10, bias=0.12)
        p.limb([(41, 60.4), (59, 60.6)], 5.6, 5.2, fur, group=11)
        p.lens((45.6, 39.4), (41.6, 52), 6.4, fur, bend=1.6, group=13, bias=0.22)  # far ear
        p.blob(49.6, 46, 7.6, 6.6, fur, group=14, bias=-0.1)
        p.limb([(53, 49.6), (60, 50.4)], 7, 6, pale, group=16)                     # muzzle
        p.lens((53.6, 52.6), (57, 59), 7, pale, bend=0.6, group=17)               # beard
        p.lens((47, 42.6), (54.4, 40.6), 3.6, pale, bend=-0.6, group=19)          # brow
        if p.big:
            p.eye(52, 44, 4, 3, iris="v1", shine="white", shine_at=(2, 1))
            p.patch(59, 47, ["11.", "111", "11."], {"1": "ink"})
        return

    if view == "down":
        # follower walking toward us: the jar's mouth framing the head
        st = phase
        p.limb([(26, 50), (25.5, 59 - st)], 4.4, 4, fur, group=11)
        p.limb([(38, 50), (38.5, 59 - (1 - st))], 4.4, 4, fur, group=12)
        p.blob(32, 40, 13, 11, jar, group=1)
        p.blob(32, 42, 10.4, 9.6, rim, group=3)
        p.blob(32, 42.6, 8.6, 7.8, inside, group=4, noline=True)
        p.blob(32, 46, 7, 6, fur, group=10)
        p.blob(32, 41, 6.4, 5.6, fur, group=13)
        p.blob(32, 45.6, 3.6, 3, pale, group=16)
        p.lens((27, 38), (24.5, 46), 3.6, fur, bend=1, group=14)
        p.lens((37, 38), (39.5, 46), 3.6, fur, bend=-1, group=15)
        p.limb(bez3((40, 30), (44, 20), (36, 16), (33, 20), n=12), 3.2, 2.6, fur, group=40)
        _lamp(p, 33, 20.4)
        p.eye(28, 40, 2, 2, shine=None)
        p.eye(34, 40, 2, 2, shine=None)
        p.pxs([(31, 43), (32, 43)], "ink")
        return

    if view == "up":
        # follower walking away: the jar's base and belly on its back
        st = phase
        p.limb([(26, 50), (25.5, 59 - st)], 4.4, 4, fur, group=11)
        p.limb([(38, 50), (38.5, 59 - (1 - st))], 4.4, 4, fur, group=12)
        p.blob(32, 41, 12.6, 11, jar, group=1)
        p.blob(32, 41, 4.6, 4.6, rim, group=2)
        p.limb(bez3((33, 32), (36, 20), (28, 15), (25, 19), n=12), 3.2, 2.6, fur, group=40)
        _lamp(p, 25, 19.4)
        if p.big:
            p.stroke([(36, 33), (38, 37), (36, 40), (39, 45)], "t0")
        return


MONS = [
    Mon("Pithound", PITHOUND_COLORS, PITHOUND_SHINY, pithound, foot="paw"),
]
