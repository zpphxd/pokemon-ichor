"""Melissa line: Melibee, Melisseer (Bug, Bug/Psychic). The Melissai, the
bee nymphs who fed the infant Zeus on honey in a Cretan cave, and the
Pythia, "the Delphic Bee", in the temple the bees built of wax and feathers."""
import math

from mon_lib import C, Mat, Mon, bez, lens_pts

INK = C.ink


def _net(p, pid, cell, color, knot=None, off=(0.0, 0.0), ang=0.0):
    """A honeycomb net over the visible interior of part pid, painted after
    render: 1 px lines on the edges of a hex lattice of spacing cell
    (canvas px), optionally with a darker knot pixel where three cells meet.
    Call it last, once every part that can cover the wing is drawn."""
    if not p.big or not pid:
        return
    import numpy as np
    m = p.fig.pid == pid
    inner = m.copy()
    inner[1:, :] &= m[:-1, :]
    inner[:-1, :] &= m[1:, :]
    inner[:, 1:] &= m[:, :-1]
    inner[:, :-1] &= m[:, 1:]
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    rows = cell * 0.866
    for Y, X in zip(*np.nonzero(inner)):
        x0, y0 = X + 0.5 - off[0], Y + 0.5 - off[1]
        x, y = x0 * ca + y0 * sa, -x0 * sa + y0 * ca
        j0 = int(math.floor(y / rows))
        ds = []
        for j in range(j0 - 1, j0 + 3):
            sh = cell / 2 if j % 2 else 0.0
            i0 = int(math.floor((x - sh) / cell))
            for i in range(i0 - 1, i0 + 3):
                cx, cy = i * cell + sh, j * rows
                ds.append(math.hypot(x - cx, y - cy))
        ds.sort()
        if ds[1] - ds[0] < 0.95:
            c = knot if (knot and ds[2] - ds[0] < 1.6) else color
            p.fig.px(int(X), int(Y), c)


def _curl(p, x, y, sgn, color):
    """A 3 px curled antenna tip opening downward; sgn -1 curls left."""
    p.pxs([(x, y), (x + sgn, y - 1), (x + 2 * sgn, y), (x + 2 * sgn, y + 1)], color)


# --------------------------------------------------------------------------
# Melibee, the honey worker
# --------------------------------------------------------------------------

MELIBEE_COLORS = [
    ("ink", INK),
    # sun-gold fuzz, warm amber in the shadows
    ("fz0", (144, 80, 24)), ("fz1", (208, 136, 32)), ("fz2", (240, 192, 64)), ("fz3", (248, 232, 136)),
    # black-figure stripes with a soft fuzz sheen
    ("st1", (72, 56, 56)), ("st2", (120, 104, 96)),
    # marble face
    ("mb0", (200, 184, 160)), ("mb1", (240, 232, 208)), ("white", C.white),
    # clear wings with Aegean glints
    ("wg0", (64, 120, 192)), ("wg1", (168, 208, 240)), ("wg2", (232, 248, 248)),
    ("honey", (224, 120, 32)), ("cheek", (240, 160, 144)),
]
MELIBEE_SHINY = {
    # olive bands, silver wings
    "fz0": (56, 80, 32), "fz1": (104, 128, 48), "fz2": (152, 176, 72), "fz3": (200, 216, 136),
    "wg0": (112, 112, 128), "wg1": (200, 200, 208), "wg2": (240, 240, 240),
}

mb_fuzz = Mat(["fz0", "fz1", "fz2", "fz3"], line="fz0", cuts=[0.2, 0.44, 0.72])
mb_stripe = Mat(["ink", "st1", "st2"], line="ink", cuts=[0.32, 0.66])
mb_face = Mat(["mb0", "mb1", "white"], line="mb0", cuts=[0.34, 0.7])
mb_wing = Mat(["wg1", "wg2"], line="wg1", outline="wg0", cuts=[0.6])
mb_leg = Mat(["ink", "st1"], cuts=[0.6])
mb_honey = Mat(["fz0", "honey", "fz2"], line="fz0", cuts=[0.3, 0.7])


def _mb_wing(p, a, b, w, bend=0.0, **kw):
    return p.lens(a, b, w, mb_wing, bend=bend, fat=0.62, **kw)


def _stripes(p, mat, ab, cx, cy, ang, offs, w=2.4, half=8.0, bend=1.4, group=2):
    """Curved bands across a body part ab, perpendicular to its long axis
    (angle ang, degrees, pointing to the tail); offs are positions along the
    axis. bend > 0 bows them toward the tail, as rings on a body turned away."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    out = []
    for o in offs:
        x, y = cx + ux * o, cy + uy * o
        out.append(p.lens((x - uy * half, y + ux * half), (x + uy * half, y - ux * half), w, mat, bend=bend,
                          clip=[ab], group=group, noline=True))
    return out


def melibee(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0     # the bob
        F = phase if view != "icon" else 0                  # wingbeat
        wings = []
        # far wing, behind everything
        wings.append(_mb_wing(p, (34, 35 - L), (40 + 2 * F, 21.5 - L + F), 7.4, bend=1.2, bias=0.18, group=40))
        # far legs
        p.limb([(36, 46 - L), (37.5, 48.5 - L), (37, 51 - L)], 1.6, 1.2, mb_leg, bias=0.3)
        # abdomen: plump, tipped down to the stinger
        ab = p.blob(40.5, 43.6 - L, 8.0, 7.2, mb_fuzz, ang=24, group=1)
        _stripes(p, mb_stripe, ab, 40.5, 43.6 - L, 24, (-1.0, 3.6), w=2.6, half=8.5, bend=1.2)
        p.taper([(47, 48.5 - L), (49.5, 51 - L)], 2.2, mb_stripe)
        # thorax: a fuzzy collar
        p.blob(33.5, 41 - L, 5.4, 5.4, mb_fuzz, group=1)
        # head, big and round, the pale face
        head = p.blob(25.5, 36 - L, 7.8, 7.4, mb_fuzz, group=3)
        p.blob(22.6, 39.4 - L, 6.0, 4.6, mb_face, clip=[head], group=4, ang=-10)
        # near wings, over the back
        wings.append(_mb_wing(p, (36, 36 - L), (48.5 + F, 23 - L + 2 * F), 8.8, bend=-1.4, group=41))
        wings.append(_mb_wing(p, (37.5, 38 - L), (51, 33.5 - L + F), 5.8, bend=-0.8, group=42, bias=0.06))
        # antennae, short and curled
        p.limb(bez((23, 30 - L), (21.5, 27.5 - L), (19, 26 - L)), 1.3, 1.2, mb_leg)
        p.limb(bez((28.5, 29.5 - L), (29.5, 27 - L), (31.5, 25.5 - L)), 1.3, 1.2, mb_leg, bias=0.2)
        # near legs dangling, clasping the honey drop
        p.limb([(31, 45 - L), (29, 47.5 - L), (27.5, 50 - L)], 1.7, 1.3, mb_leg)
        p.limb([(33.5, 46 - L), (33.5, 49 - L), (32, 51 - L)], 1.7, 1.3, mb_leg)
        p.drop((29.8, 47.2 - L), 29.8, 52 - L, 3.0, mb_honey)
        if p.big:
            for w in wings:
                _net(p, w, 4.2, "wg1", off=(1, 2))
            _curl(p, 18, 26 - L, -1, "ink")
            _curl(p, 32, 25 - L, 1, "ink")
            p.eye(23, 34 - L, 4, 5, shine="white", shine_at=(1, 1))
            p.eye(18.5, 34 - L, 2, 4, shine="white", shine_at=(0, 1))
            p.stroke([(20, 41 - L), (22, 41 - L)], "fz0")
            p.px(19, 40 - L, "fz0")
            p.px(26, 40 - L, "cheek")
            p.px(28.5, 50.5 - L, "fz3")
        else:
            p.px(24, 36 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: sitting low so the round striped
        # abdomen is cropped by the frame, wings up, the head turned right
        wings = []
        wings.append(_mb_wing(p, (40, 40), (50, 20), 8.4, bend=-1.0, bias=0.2, group=40))
        ab = p.blob(26.5, 57, 11, 9.8, mb_fuzz, ang=-35, group=1)
        _stripes(p, mb_stripe, ab, 35, 46, 127, (9, 16), w=3.2, half=12, bend=-2.0)
        p.blob(35.5, 46, 6.8, 6.6, mb_fuzz, group=1)
        head = p.blob(42.5, 34, 9.2, 8.8, mb_fuzz, group=3)
        p.blob(48.5, 38, 5.6, 5.2, mb_face, clip=[head], group=4, ang=10)
        wings.append(_mb_wing(p, (34, 42), (13, 22), 10.5, bend=1.6, group=41))
        wings.append(_mb_wing(p, (33, 46), (13, 40), 7.0, bend=0.8, group=42, bias=0.06))
        p.limb(bez((45, 26), (45.5, 22.5), (48.5, 20.5)), 1.6, 1.4, mb_leg)
        p.limb(bez((40, 26.5), (38.5, 22.5), (36.5, 20.5)), 1.6, 1.4, mb_leg, bias=0.2)
        if p.big:
            for w in wings:
                _net(p, w, 5.0, "wg1", off=(2, 1))
            _curl(p, 49, 20, 1, "ink")
            _curl(p, 36, 20, -1, "ink")
            p.eye(48, 32, 4, 5, shine="white", shine_at=(2, 1))
        return

    if view in ("down", "up"):
        F = phase
        for s in (-1, 1):
            _mb_wing(p, (32 + s * 4, 33), (32 + s * 16, 21 + 2 * F), 8, bend=-s * 1.2, group=40 + s)
            _mb_wing(p, (32 + s * 4, 36), (32 + s * 14, 33 + F), 5, bend=-s * 0.6, group=43 + s)
        if view == "up":
            ab = p.blob(32, 43, 8.2, 8.4, mb_fuzz, group=1)
            for y in (40.5, 46.5):
                p.lens((23, y), (41, y), 2.8, mb_stripe, bend=-1.2, clip=[ab], group=2, noline=True)
            p.taper([(32, 50.5), (32, 54.5)], 2.2, mb_stripe)
            p.blob(32, 30, 7.6, 7, mb_fuzz, group=3)
            p.limb(bez((29, 24.5), (27, 21), (25, 20)), 1.3, 1.2, mb_leg)
            p.limb(bez((35, 24.5), (37, 21), (39, 20)), 1.3, 1.2, mb_leg)
            return
        p.blob(32, 43, 5, 4.6, mb_fuzz, group=1)
        p.limb([(29.5, 45), (29, 49.5 - F)], 1.7, 1.3, mb_leg)
        p.limb([(34.5, 45), (35, 49.5 - (1 - F))], 1.7, 1.3, mb_leg)
        p.drop((32, 47), 32, 51.5, 3.0, mb_honey)
        head = p.blob(32, 34, 8, 7.4, mb_fuzz, group=3)
        p.blob(32, 37.4, 6.4, 4.6, mb_face, clip=[head], group=4)
        p.limb(bez((29, 28), (27, 25), (25, 24)), 1.3, 1.2, mb_leg)
        p.limb(bez((35, 28), (37, 25), (39, 24)), 1.3, 1.2, mb_leg)
        p.eye(27.5, 32, 3, 4, shine="white")
        p.eye(33.5, 32, 3, 4, shine="white")
        if p.big:
            p.stroke([(31, 39), (32, 39)], "fz0")
        return


# --------------------------------------------------------------------------
# Melisseer, the Delphic bee
# --------------------------------------------------------------------------

MELISSEER_COLORS = [
    ("ink", INK),
    ("gd0", (152, 88, 24)), ("gd1", (208, 144, 40)), ("gd2", (240, 192, 64)), ("gd3", (248, 232, 144)),
    ("st1", (64, 48, 64)),
    ("mr0", (160, 152, 152)), ("mr1", (208, 200, 192)), ("mr2", (248, 248, 240)),
    # wings: pale gauze with the violet Omphalos net
    ("vi0", (104, 64, 136)), ("vi1", (168, 128, 200)), ("wg", (216, 216, 232)),
    ("lf0", (56, 72, 32)), ("lf1", (96, 120, 48)), ("lf2", (152, 168, 72)),
]
MELISSEER_SHINY = {
    # pale silver bands, an Aegean net
    "gd0": (120, 120, 128), "gd1": (168, 168, 176), "gd2": (208, 208, 216), "gd3": (240, 240, 240),
    "vi0": (24, 72, 152), "vi1": (96, 152, 216),
}

ms_gold = Mat(["gd0", "gd1", "gd2", "gd3"], line="gd0", cuts=[0.2, 0.44, 0.72])
ms_band = Mat(["ink", "st1"], line="ink", cuts=[0.5])
ms_robe = Mat(["mr0", "mr1", "mr2"], line="mr0", cuts=[0.34, 0.68])
ms_wing = Mat(["wg", "mr2"], line="vi1", outline="vi0", cuts=[0.62])
ms_leaf = Mat(["lf0", "lf1", "lf2"], line="lf0", cuts=[0.3, 0.64])
ms_leg = Mat(["ink", "st1"], cuts=[0.6])


def _wreath(p, x, y, L=0, n=5, span=12):
    """A laurel crown from (x, y) back along the brow: small leaves rising."""
    for i in range(n):
        t = i / (n - 1)
        bx, by = x + span * t, y + 1.2 * math.sin(math.pi * t) * -1
        ang = math.radians(-120 + 70 * t)
        ln = 3.6
        p.lens((bx, by - L), (bx + math.cos(ang) * ln, by + math.sin(ang) * ln - L), 2.6, ms_leaf, bend=0.4,
               bias=0.12 if t > 0.6 else 0)


def _ms_hand(p, x, y, L=0):
    """A raised forefoot: a gold fuzz cuff and a three-clawed tarsus."""
    p.blob(x, y - L, 2.0, 1.8, ms_gold)


def melisseer(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        wings = []
        # four wings fanned behind like a halo: the far pair first
        wings.append(p.lens((32, 23), (44, 1.5 - L), 9.4, ms_wing, bend=2.2, fat=0.6, bias=0.16, group=40))
        wings.append(p.lens((34, 31), (50, 52 + L), 8.4, ms_wing, bend=-2.0, fat=0.6, bias=0.16, group=41))
        # far foreleg raised beside the head
        p.limb([(31, 25), (36.5, 21.5), (36, 14 - L)], 2.8, 2.2, ms_leg, bias=0.3)
        _ms_hand(p, 36, 12.5, L)
        # abdomen hanging like a gown, banded, full at the hip
        ab = p.poly(lens_pts((28, 30), (33.5, 57.5), 19.5, bend=-1.8, fat=0.36), ms_gold, group=1)
        _stripes(p, ms_band, ab, 31, 43, 80, (-1.5, 4.0, 9.0), w=2.0, half=11, bend=1.4)
        # near wings
        wings.append(p.lens((33, 24), (61.5, 9 - 2 * L), 10.6, ms_wing, bend=-1.0, fat=0.58, group=42))
        wings.append(p.lens((34, 28), (61, 34 + L), 9.0, ms_wing, bend=-1.6, fat=0.58, group=43))
        # thorax: the marble robe, a bell from the ruff to a scalloped hem
        p.poly([(21.5, 23), (32, 22.5), (34.8, 27), (36, 33), (37, 38.2), (34.2, 37.2), (31.4, 39), (28.2, 37.4),
                (25, 39), (21.8, 37.4), (19.4, 38.2), (19.4, 32), (20.4, 27)], ms_robe, group=3)
        p.blob(26.5, 22.2, 6.0, 2.9, ms_gold, group=4)
        # head: gold fuzz, a pale marble face plate low in front, small
        # mandibles; big compound eyes, lidded and calm
        head = p.blob(22, 15.5, 6.2, 6.0, ms_gold, group=5)
        p.blob(17.6, 19.4, 3.0, 2.4, ms_robe, clip=[head], group=6, ang=-20)
        _wreath(p, 17, 11, n=5, span=11)
        p.limb(bez((20, 10), (17, 5.5), (13.5, 3)), 1.4, 1.2, ms_leg)
        p.limb(bez((25, 9.5), (27, 5), (30, 3)), 1.4, 1.2, ms_leg, bias=0.2)
        # lower legs folded down the front like the folds of a robe
        p.limb([(21.5, 37), (19, 42), (22.5, 47)], 2.1, 1.9, ms_leg)
        # near foreleg raised before the face, as if speaking
        p.limb([(23.5, 26), (16.5, 30), (12, 24 - L)], 3.0, 2.4, ms_leg)
        _ms_hand(p, 11.5, 22, L)
        if p.big:
            for w in wings:
                _net(p, w, 4.6, "vi1", knot="vi0", off=(1, 0), ang=-20)
            _curl(p, 13, 3, -1, "ink")
            _curl(p, 30, 3, 1, "ink")
            # the near compound eye, lidded halfway: calm, in trance
            p.patch(18, 12, [".gg.", "1111", "1155", "1ee1", ".11."], {"1": "ink", "e": "vi1", "5": "mr2",
                                                                     "g": "gd1"})
            p.patch(15, 14, ["1", "1", "e"], {"1": "ink", "e": "vi0"})
            p.pxs([(15, 21), (16, 22), (18, 22)], "ink")      # mandibles
        else:
            p.px(19, 15, "ink")
        return

    if view == "back":
        wings = []
        wings.append(p.lens((40, 30), (58, 4), 9, ms_wing, bend=-1.2, fat=0.62, group=39, bias=0.2))
        wings.append(p.lens((32, 34), (8, 3), 12, ms_wing, bend=1.6, fat=0.62, group=40, bias=0.1))
        wings.append(p.lens((32, 40), (3, 34), 10, ms_wing, bend=-1, fat=0.62, group=41, bias=0.1))
        ab = p.poly(lens_pts((33, 38), (35, 78), 21, bend=-1, fat=0.4), ms_gold, group=1)
        _stripes(p, ms_band, ab, 34, 52, 95, (0, 9), w=3.4, half=13, bend=-1.6)
        p.blob(38, 34, 9, 9.4, ms_robe, group=3)
        p.blob(42, 26, 8, 3.8, ms_gold, group=4)
        head = p.blob(45, 18, 7.6, 7.4, ms_gold, group=5)
        p.blob(50, 21, 4.4, 4, ms_robe, clip=[head], group=6)
        wings.append(p.lens((35, 32), (14, 8), 12, ms_wing, bend=1.4, fat=0.6, group=42))
        wings.append(p.lens((35, 38), (8, 47), 10, ms_wing, bend=-1.4, fat=0.6, group=43))
        p.limb(bez((46, 11), (47, 6), (51, 3)), 1.6, 1.4, ms_leg)
        p.limb(bez((41, 12), (39, 7), (36, 4)), 1.6, 1.4, ms_leg, bias=0.2)
        for a, b in (((40, 13), (37, 9.5)), ((43, 11), (42.5, 7)), ((46.5, 11), (48.5, 7.5)), ((49.5, 12.5), (52.5, 10))):
            p.lens(a, b, 2.8, ms_leaf, bend=0.4)
        if p.big:
            for w in wings:
                _net(p, w, 5.6, "vi1", knot="vi0", off=(2, 1), ang=20)
            _curl(p, 51, 3, 1, "ink")
            _curl(p, 36, 4, -1, "ink")
            p.patch(48, 17, ["111", "51e", ".11"], {"1": "ink", "e": "vi1", "5": "mr2"})
        return

    if view in ("down", "up"):
        F = phase
        for s in (-1, 1):
            p.lens((32 + s * 4, 26), (32 + s * 20, 6 + 2 * F), 9, ms_wing, bend=-s * 1.4, fat=0.6, group=40 + s)
            p.lens((32 + s * 4, 31), (32 + s * 20, 38 - 2 * F), 7, ms_wing, bend=s * 1.4, fat=0.6, group=43 + s)
        ab = p.poly(lens_pts((32, 32), (32, 56), 13, fat=0.42), ms_gold, group=1)
        for y0 in (40, 46, 51):
            p.lens((22, y0 + 1), (42, y0 + 1), 2.4, ms_band, bend=-1, clip=[ab], group=2, noline=True)
        p.blob(32, 28, 6.4, 6.4, ms_robe, group=3)
        p.blob(32, 17, 6.4, 6.2, ms_gold, group=5)
        for s in (-1, 1):
            p.limb(bez((32 + s * 2.5, 12), (32 + s * 5, 7), (32 + s * 9, 4)), 1.4, 1.2, ms_leg)
        if view == "down":
            p.blob(32, 20, 4.4, 3.4, ms_robe, group=6)
            p.limb([(27, 26), (22, 22), (22, 16)], 2.4, 2, ms_leg)
            p.limb([(37, 26), (42, 22), (42, 16)], 2.4, 2, ms_leg)
            p.patch(27, 16, ["111..111", "1e5..5e1", ".11..11."], {"1": "ink", "e": "vi1", "5": "mr2"})
        for a, b in (((28, 12), (25, 9)), ((32, 11), (32, 7.5)), ((36, 12), (39, 9))):
            p.lens(a, b, 2.8, ms_leaf, bend=0.4)
        return


MONS = [
    # icon palette 4 keeps the gold fuzz gold rather than orange
    Mon("Melibee", MELIBEE_COLORS, MELIBEE_SHINY, melibee, foot="blank", icon_pal=4),
    Mon("Melisseer", MELISSEER_COLORS, MELISSEER_SHINY, melisseer, foot="blank", icon_pal=5),
]
