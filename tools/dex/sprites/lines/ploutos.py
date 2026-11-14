"""Ploutos line: Spalunk, Plouteras (Ground). Ploutos, wealth, Demeter's
son: blind, so riches fall on whoever he stumbles into."""
from mon_lib import C, Mat, Mon, bez, bez3, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# Spalunk, the blind mole
# --------------------------------------------------------------------------

SPALUNK_COLORS = [
    ("ink", INK),
    # velvety cypress-dark fur
    ("fur0", (32, 48, 48)), ("fur1", (48, 80, 72)), ("fur2", (80, 120, 96)), ("fur3", (128, 168, 136)),
    # limestone belly
    ("belly0", (176, 144, 96)), ("belly1", (224, 200, 152)),
    # terracotta paws and snout
    ("terra0", (128, 56, 32)), ("terra1", (192, 96, 64)), ("terra2", (232, 152, 112)),
    # the sun-gold coin
    ("gold0", (200, 136, 32)), ("gold1", (248, 208, 72)), ("white", C.white),
    # turned earth
    ("earth0", (88, 56, 32)), ("earth1", (136, 96, 56)),
]
SPALUNK_SHINY = {
    # pale sun-gold fur
    "fur0": (152, 112, 40), "fur1": (200, 160, 64), "fur2": (232, 200, 104), "fur3": (248, 232, 160),
}

s_fur = Mat(["fur0", "fur1", "fur2", "fur3"], line="fur0", cuts=[0.24, 0.5, 0.78])
s_belly = Mat(["belly0", "belly1"], line="fur1", cuts=[0.55])
s_terra = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.66])
s_gold = Mat(["gold0", "gold1"], line="gold0", cuts=[0.55])
s_earth = Mat(["earth0", "earth1"], line="earth0", cuts=[0.5])


def _paw(p, cx, cy, ang, mat, claw_mat, n=4, r=3.6, ln=2.6, **kw):
    """A broad digging paw: a round palm with n stout claws fanning out
    along ang (degrees, 0 = right, -90 = up)."""
    import math
    pid = p.blob(cx, cy, r, r * 0.9, mat, ang=ang + 90, **kw)
    a0 = math.radians(ang)
    for i in range(n):
        da = math.radians((i - (n - 1) / 2) * 26)
        ux, uy = math.cos(a0 + da), math.sin(a0 + da)
        root = (cx + ux * (r - 0.8), cy + uy * (r - 0.8))
        p.taper([root, (root[0] + ux * ln, root[1] + uy * ln)], 1.7, claw_mat, **kw)
    return pid


def spalunk(p, view, phase):
    claw = Mat(["belly0", "belly1"], line="terra0", cuts=[0.5])
    if view == "down":
        # follower shuffling toward the camera: snout first, paws paddling
        st = phase
        p.blob(32, 50, 10.5, 9, s_fur, group=1)
        p.blob(32, 52, 5.4, 5, s_belly, group=2)
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            _paw(p, 32 + 10 * sx, 56 - up, -90 + 30 * sx, s_terra, claw, n=4, r=3.4, ln=2.2, group=10 + (sx > 0))
        p.blob(32, 40, 9, 8.4, s_fur, group=3)
        p.limb([(32, 43), (32, 46.5)], 6.0, 4.4, s_terra, group=4)
        p.blob(32, 47, 2.8, 2.2, s_terra, group=4)
        if p.big:
            for ex in (26, 35):
                p.pxs([(ex, 38), (ex + 1, 38), (ex + 2, 38)], "fur3")
                p.pxs([(ex, 39), (ex + 1, 40), (ex + 2, 39)], "fur0")
            p.pxs([(31, 47), (33, 47)], "terra0")
        return

    if view == "up":
        # follower shuffling away: the round velvet back, the paws out to
        # the sides, a stub of tail
        st = phase
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            _paw(p, 32 + 10.5 * sx, 50 - up, -90 + 40 * sx, s_terra, claw, n=4, r=3.2, ln=2.0, group=10 + (sx > 0))
        p.blob(32, 47, 11, 11, s_fur, group=1)
        p.blob(32, 36.5, 7.4, 6, s_fur, group=3)
        p.limb([(32, 55), (32, 58)], 2.4, 1.6, s_terra, group=20)
        return

    if view == "side":
        # follower trundling left: snout out, a paw reaching to dig
        st = phase
        p.limb([(42, 50), (46, 52)], 2.0, 1.4, s_terra, group=20)
        _paw(p, 38 - 2 * st, 57.5, 0, s_terra, claw, n=3, r=2.6, ln=1.6, bias=0.2, group=10)
        p.blob(33, 49, 11, 8, s_fur, group=1)
        p.blob(29, 53, 6, 3.4, s_belly, group=2)
        p.limb(bez((24, 48), (20, 48), (17, 46)), 5.4, 3.0, s_terra, group=4)
        p.blob(16.6, 45.8, 1.9, 1.8, s_terra, group=4)
        _paw(p, 24 + 2 * st, 57, -160, s_terra, claw, n=4, r=3.2, ln=2.2, group=11)
        if p.big:
            p.pxs([(25, 44), (26, 45), (27, 45), (28, 44)], "fur0")
        return

    if view in ("front", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0

        # far paw raised at the right side, palm out
        p.limb([(37, 49), (41, 45)], 4.4, 4.0, s_fur, bias=0.25, group=10)
        _paw(p, 43, 42.5 - L, -55, s_terra, claw, n=4, r=3.4, ln=2.4, bias=0.12, group=11)

        # the burrow's back rim
        p.blob(32, 56.5, 15.5, 4.4, s_earth, bias=0.25, group=30)
        # body half out of the ground, under a big round velvet head
        p.blob(31.5, 52, 10, 7, s_fur, group=1)
        p.blob(30.5, 40.5 - L, 9.4, 9, s_fur, group=1)
        p.blob(28, 51.5, 5, 4.6, s_belly, group=2)
        # the long pink snout, sniffing up
        p.limb(bez((23.5, 43 - L), (18.5, 42.5 - L), (14.5, 39.5 - 2 * L)), 6.0, 3.0, s_terra, group=4)
        p.blob(14, 39.2 - 2 * L, 1.9, 1.8, s_terra, group=4)
        # the burrow's front rim of turned earth, lumpy with clods
        p.poly([(15, 61), (17, 57.5), (22, 56), (28, 57.5), (34, 56.5), (40, 57.5), (46, 56), (49.5, 58.5), (50.5, 61)],
               s_earth, group=31)
        for x, y, r in ((19.5, 56.5, 2.3), (25.5, 57.5, 2.2), (32, 57, 2.0), (39.5, 57.5, 2.3), (46, 56.5, 2.1)):
            p.circle(x, y, r, s_earth, group=31)
        # near paw raised at the chest, a coin pinched up in its claws
        p.limb([(25, 51), (21, 48.5)], 4.4, 4.0, s_fur, group=12)
        _paw(p, 19, 47 - L, -125, s_terra, claw, n=4, r=3.8, ln=2.6, group=13)
        p.circle(14.6, 42 - 2 * L, 2.4, s_gold, group=14)

        if p.big:
            # the closed eye: a seam in the fur, a lit lid above it
            p.pxs([(25, 37 - L), (26, 38 - L), (27, 38 - L), (28, 37 - L)], "fur0")
            p.pxs([(25, 36 - L), (26, 36 - L), (27, 36 - L)], "fur3")
            p.px(12, 38 - 2 * L, "terra0")
            # the coin's glint
            p.pxs([(14, 41 - 2 * L), (13, 42 - 2 * L)], "white")
        else:
            p.px(26, 38, "fur0")
        return

    if view == "back":
        # draft of the hand-finished back: the round velvet shoulders out of
        # the hole, the head turned right, both paws raised, the coin held up
        _paw(p, 10.5, 46, -120, s_terra, claw, n=3, r=3.4, ln=2.0, bias=0.1, group=10)
        p.blob(28, 51, 17, 16.5, s_fur, group=1)
        p.blob(34, 44, 9, 8, s_fur, group=1)
        p.blob(40, 38, 9, 8.4, s_fur, group=1)
        p.limb(bez((47, 40), (52, 40), (56, 36.5)), 5.6, 3.0, s_terra, group=4)
        _paw(p, 51, 48.5, -60, s_terra, claw, n=3, r=3.4, ln=2.0, group=11)
        p.circle(54, 45, 2.2, s_gold, group=12)
        p.poly([(3, 64), (4, 59), (16, 58), (28, 59), (40, 58.5), (52, 60), (54, 64)], s_earth, group=31)
        if p.big:
            p.pxs([(34, 42), (35, 43), (36, 43), (37, 42)], "fur0")
        return
    return


# --------------------------------------------------------------------------
# Plouteras, wealth with the horn of plenty
# --------------------------------------------------------------------------

PLOUTERAS_COLORS = [
    ("ink", INK),
    # cypress-dark fur
    ("fur0", (32, 48, 48)), ("fur1", (48, 80, 72)), ("fur2", (80, 120, 96)), ("fur3", (128, 168, 136)),
    # limestone belly and horn
    ("lime0", (168, 136, 88)), ("lime1", (208, 184, 136)), ("lime2", (240, 224, 184)),
    # terracotta paws and snout
    ("terra0", (128, 56, 32)), ("terra1", (192, 96, 64)), ("terra2", (232, 152, 112)),
    # sun-gold bands, wheat and coins
    ("gold0", (192, 128, 32)), ("gold1", (248, 208, 72)),
    # olive figs
    ("fig0", (72, 88, 32)), ("fig1", (128, 144, 64)),
]
PLOUTERAS_SHINY = {
    # sun-gold fur, a marble horn
    "fur0": (152, 104, 32), "fur1": (200, 152, 56), "fur2": (232, 192, 96), "fur3": (248, 224, 152),
    "lime0": (192, 184, 176), "lime1": (224, 224, 216), "lime2": (248, 248, 240),
}

pl_fur = Mat(["fur0", "fur1", "fur2", "fur3"], line="fur0", cuts=[0.24, 0.5, 0.78])
pl_belly = Mat(["lime0", "lime1", "lime2"], line="fur1", cuts=[0.36, 0.7])
pl_horn = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.3, 0.66])
pl_terra = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.66])
pl_gold = Mat(["gold0", "gold1"], line="gold0", cuts=[0.55])
pl_fig = Mat(["fig0", "fig1"], line="fig0", cuts=[0.55])


def _horn(p, path, w0, mat, bands=(), band_mat=None, **kw):
    """The horn of plenty along path: a flared mouth at path[0] tapering to
    a curled tip, with gold bands at the fractions in `bands`."""
    import math
    a = p._minw(w0)

    def width(t):
        return a * (1 - t) ** 0.85 + 0.6 * t
    poly = ribbon(path, width)
    pid = p.add(p.mask(poly), mat, **kw)
    if bands and p.big:
        acc = [0.0]
        for u, v in zip(path, path[1:]):
            acc.append(acc[-1] + math.hypot(v[0] - u[0], v[1] - u[1]))
        tot = acc[-1]
        kw2 = {k: v for k, v in kw.items() if k not in ("group",)}
        for t in bands:
            d = t * tot
            i = max(j for j in range(len(acc)) if acc[j] <= d)
            i = min(i, len(path) - 2)
            u, v = path[i], path[i + 1]
            k = (d - acc[i]) / ((acc[i + 1] - acc[i]) or 1)
            cx, cy = u[0] + (v[0] - u[0]) * k, u[1] + (v[1] - u[1]) * k
            dx, dy = v[0] - u[0], v[1] - u[1]
            n = math.hypot(dx, dy) or 1
            nx, ny = -dy / n, dx / n
            h = width(t) / 2 + 1
            bw = max(1.6, width(t) * 0.16)
            p.lens((cx + nx * h, cy + ny * h), (cx - nx * h, cy - ny * h), bw, band_mat or mat,
                   bend=-width(t) * 0.12, clip=[pid], group=kw.get("group"), **kw2)
    return pid


def _wheat(p, base, tip, kw=None):
    """A wheat ear: a stalk from base to tip, the grain head on the last
    third, in sun-gold."""
    mid = (base[0] + (tip[0] - base[0]) * 0.45, base[1] + (tip[1] - base[1]) * 0.45)
    p.limb([base, mid], 1.3, 1.2, pl_gold, **(kw or {}))
    return p.lens(mid, tip, 3.0, pl_gold, fat=0.45, **(kw or {}))


def _fig(p, x, y, r, ang=-30.0, **kw):
    """A fig: round, with a short pointed stem end."""
    import math
    a = math.radians(ang - 90)
    tip = (x + math.cos(a) * r * 1.7, y + math.sin(a) * r * 1.7)
    return p.drop(tip, x, y, r, pl_fig, **kw)


def _coin(p, x, y, r=1.8, **kw):
    return p.blob(x, y, r, r * 1.05, pl_gold, **kw)


def plouteras(p, view, phase):
    if view == "down":
        # follower waddling toward the camera, the horn hugged up to its
        # chest, wheat standing out of the mouth
        st = phase
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            p.blob(32 + 7.5 * sx, 59 - up, 4.4, 2.4, pl_terra, group=12 + (sx > 0))
        p.blob(32, 46, 13, 12.5, pl_fur, group=1)
        p.blob(32, 30, 9.4, 8.6, pl_fur, group=3)
        for bx, tx, ty in ((29, 18.5, 31), (35, 45.5, 31)):
            _wheat(p, (bx, 39), (tx, ty), {"group": 18})
        _horn(p, bez3((32, 40), (28, 48), (31, 54), (38, 54)), 11, pl_horn, bands=(0.2, 0.4, 0.6, 0.78), band_mat=pl_gold, group=20)
        p.blob(32, 40, 5.6, 2.2, pl_gold, group=21)
        p.blob(32, 39.8, 4.2, 1.2, Mat(["fur0"]), group=22)
        p.blob(24, 45, 3.6, 3, pl_terra, group=23)
        p.blob(40, 45, 3.6, 3, pl_terra, group=24)
        p.limb([(32, 32), (32, 35)], 5.6, 4.2, pl_terra, group=4)
        p.blob(32, 35.5, 2.6, 2, pl_terra, group=4)
        if p.big:
            for ex in (26, 35):
                p.pxs([(ex, 28), (ex + 1, 28), (ex + 2, 28)], "fur3")
                p.pxs([(ex, 29), (ex + 1, 30), (ex + 2, 29)], "fur0")
        return

    if view == "up":
        # follower waddling away: the round back, wheat over its shoulder,
        # the horn's curled tip at its side
        st = phase
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            p.blob(32 + 7.5 * sx, 59 - up, 4.4, 2.4, pl_terra, group=12 + (sx > 0))
        for bx, tx, ty in ((40, 44, 22), (42, 48, 26)):
            _wheat(p, (bx, 36), (tx, ty), {"group": 18})
        p.blob(32, 46, 13.5, 13, pl_fur, group=1)
        p.blob(32, 31, 9.4, 8.6, pl_fur, group=3)
        _horn(p, bez3((26, 52), (19, 53), (17, 47), (20, 44)), 6, pl_horn, bands=(0.3, 0.6), band_mat=pl_gold, group=20)
        return

    if view == "side":
        # follower waddling left, the horn hugged before it, a grain dropping
        st = phase
        p.blob(40, 58.5 - 2 * st, 4.6, 2.4, pl_terra, bias=0.2, group=10)
        p.blob(36, 46, 13, 12.5, pl_fur, group=1)
        p.blob(28, 33, 8.6, 8, pl_fur, group=1)
        p.limb(bez((22, 35), (16, 35.5), (12, 32)), 5.6, 3.0, pl_terra, group=4)
        p.blob(11.6, 31.8, 2, 1.8, pl_terra, group=4)
        for b_, t_ in (((19, 41), (12, 33)), ((21, 40), (19, 31))):
            _wheat(p, b_, t_, {"group": 18})
        _horn(p, bez3((20, 43), (24, 55), (38, 57), (44, 50)), 11, pl_horn, bands=(0.15, 0.32, 0.5, 0.68, 0.84), band_mat=pl_gold, group=20)
        p.blob(20, 43, 5.6, 2.2, pl_gold, ang=-60, group=21)
        p.blob(30, 46, 3.8, 3, pl_terra, group=22)
        p.blob(32, 59 - 2 * (1 - st), 4.6, 2.4, pl_terra, group=14)
        if st:
            _coin(p, 50, 56, 1.6, group=25)
        if p.big:
            p.pxs([(25, 30), (26, 31), (27, 31), (28, 30)], "fur0")
        return

    if view in ("front", "icon"):
        # the draft of the hand-finished battle front (the icon draws from
        # it): a great round mole sitting back, hugging a banded horn of
        # plenty whose mouth spills wheat, figs and coins
        L = 1 if (phase == 1 and view == "front") else 0
        p.blob(49.5, 58.5, 5.2, 2.6, pl_terra, bias=0.15, group=11)
        body = p.blob(37.5, 44.5, 16.5, 15.5, pl_fur, group=1)
        p.blob(48.5, 52, 6.5, 6.5, pl_fur, group=1)
        p.blob(32.5, 26 - L, 10.2, 9.6, pl_fur, group=1)
        p.blob(27, 31 - L, 6, 5, pl_fur, group=1)
        p.blob(35.5, 39.5, 6.5, 7.5, Mat(["lime0", "lime1"], line="fur1", cuts=[0.5]), clip=[body], group=2)
        p.blob(29, 58.6, 6.4, 2.8, pl_terra, group=14)
        horn = bez3((16.5, 37), (23, 47), (35, 55.5), (46, 55)) + bez3((46, 55), (52.5, 54.5), (54.5, 48), (50.5, 46))[1:]
        _horn(p, horn, 15, pl_horn, bands=(0.1, 0.22, 0.34, 0.46, 0.57, 0.67, 0.76, 0.85), band_mat=pl_gold, group=20)
        p.blob(17, 37, 8.2, 3.4, pl_gold, ang=-68, group=21)
        p.blob(16.6, 36.6, 6.4, 1.9, Mat(["fur0"]), ang=-68, group=22)
        for b_, t_ in (((15, 34), (5.5, 21 - L)), ((18, 33), (16, 18 - L)), ((13, 36), (4, 30.5 - L)), ((20.5, 33), (25, 21 - L))):
            _wheat(p, b_, t_, {"group": 23})
        if p.big:
            _fig(p, 10.5, 39.5, 2.6, ang=-45, group=24)
            _fig(p, 14.5, 43.5 + L, 2.4, ang=0, group=25)
            _fig(p, 9.5, 47 + 2 * L, 2.5, ang=45, group=26)
            for x, y in ((7.5, 54 + L), (12, 58.5), (17.5, 59.5), (6.5, 59.3), (13.5, 52 + 2 * L)):
                _coin(p, x, y, group=27)
        p.blob(27.5, 44, 5.4, 3.8, pl_terra, ang=25, group=15)
        p.blob(45.5, 47, 4.6, 3.6, pl_terra, ang=-20, group=16)
        p.limb(bez3((25, 29.5 - L), (19, 30 - L), (14, 28 - L), (10.5, 24 - 2 * L)), 8.0, 3.2, pl_terra, group=4)
        if p.big:
            p.pxs([(27, 23 - L), (28, 24 - L), (29, 24 - L), (30, 23 - L)], "fur0")
            p.pxs([(20, 33 - L), (21, 34 - L), (22, 34 - L), (23, 33 - L)], "terra0")
        else:
            p.px(28, 24, "fur0")
        return

    if view == "back":
        # draft of the hand-finished back: the round back cropped below, the
        # head turned right, wheat standing up out of the horn beyond it, the
        # horn's curled tip at the left
        for b_, t_ in (((52, 40), (51, 17)), ((55, 40), (58.5, 18.5)), ((57.5, 41), (62, 27))):
            _wheat(p, b_, t_, {"group": 18})
        p.blob(26, 57, 21, 20, pl_fur, group=1)
        p.blob(36, 41, 11, 9, pl_fur, group=1)
        p.blob(41, 32, 10.4, 9.8, pl_fur, group=1)
        _horn(p, bez3((14, 60), (6, 60), (2.5, 54), (5, 48.5)), 7, pl_horn, bands=(0.25, 0.55, 0.8), band_mat=pl_gold, group=20)
        p.limb(bez3((47, 35), (52, 35.5), (56, 34), (59.5, 30)), 8, 3.2, pl_terra, group=4)
        p.blob(50.5, 44, 4.6, 3.6, pl_terra, ang=-25, group=15)
        _coin(p, 46, 41, group=16)
        if p.big:
            p.pxs([(43, 30), (44, 31), (45, 31), (46, 30)], "fur0")
        return
    return


MONS = [
    Mon("Spalunk", SPALUNK_COLORS, SPALUNK_SHINY, spalunk, foot="claw"),
    Mon("Plouteras", PLOUTERAS_COLORS, PLOUTERAS_SHINY, plouteras, foot="claw"),
]
