"""Ploutos line: Spalunk, Plouteras (Ground). Ploutos, wealth, Demeter's
son: blind, so riches fall on whoever he stumbles into."""
from mon_lib import C, Mat, Mon, bez, bez3, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# Spalunk, the blind mole
# --------------------------------------------------------------------------

SPALUNK_COLORS = [
    ("ink", INK),
    # velvety cypress-dark fur, warm olive midtones and a pale sheen
    ("fur0", (32, 48, 48)), ("fur1", (56, 88, 72)), ("fur2", (96, 128, 88)), ("fur3", (152, 176, 128)),
    # limestone underside, and the long pale claws
    ("belly0", (176, 144, 96)), ("belly1", (232, 216, 184)),
    # rosy terracotta snout and palms
    ("terra0", (144, 64, 56)), ("terra1", (208, 112, 104)), ("terra2", (240, 168, 152)),
    # the sun-gold coin
    ("gold0", (200, 136, 32)), ("gold1", (248, 208, 72)), ("white", C.white),
    # turned earth
    ("earth0", (80, 56, 40)), ("earth1", (136, 96, 64)),
]
SPALUNK_SHINY = {
    # pale sun-gold fur
    "fur0": (160, 112, 48), "fur1": (208, 160, 72), "fur2": (232, 200, 112), "fur3": (248, 232, 168),
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
    claw = Mat(["belly0", "belly1"], line="ink", cuts=[0.5])
    if view == "down":
        # follower shuffling toward the camera: low and wide, the snout
        # pointed at us, the great spade paws paddling either side
        st = phase
        p.blob(32, 50, 13, 8, s_fur, group=1)
        p.blob(32, 47, 8.4, 7, s_fur, group=3)
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            _paw(p, 32 + 12 * sx, 56 - up, 90 - 35 * sx, s_terra, claw, n=4, r=3.8, ln=3.0, group=10 + (sx > 0))
        p.limb([(32, 50), (32, 54.5)], 5.4, 3.6, s_terra, group=4)
        p.blob(32, 55, 2.4, 1.9, s_terra, group=4)
        if p.big:
            p.pxs([(27, 46), (28, 46), (36, 46), (37, 46)], "fur0")
            p.pxs([(31, 55), (33, 55)], "terra0")
        return

    if view == "up":
        # follower shuffling away: the hunched velvet back, the spade paws
        # out to the sides, a stub of tail
        st = phase
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            _paw(p, 32 + 12.5 * sx, 55 - up, 90 - 40 * sx, s_terra, claw, n=4, r=3.6, ln=2.8, group=10 + (sx > 0))
        p.blob(32, 49, 13, 10, s_fur, group=1)
        p.limb([(32, 57), (32, 60)], 2.4, 1.6, s_terra, group=20)
        return

    if view in ("front", "icon", "side"):
        # the draft of the hand-finished battle front (icon and walking
        # side draw from it): low, wide and hunched, crawling out of its
        # burrow, the long pink snout out front, enormous spade paws turned
        # out with long pale claws, a coin pinched in them
        L = 1 if (phase == 1 and view == "front") else 0
        st = phase if view == "side" else 0
        if view != "side":
            p.blob(43, 55.5, 9, 5, s_earth, bias=0.15, group=30)
        _paw(p, 30.5 - st, 57.5, 180, s_terra, claw, n=3, r=3.6, ln=3.4, bias=0.12, group=10)
        p.blob(32, 47 - 0.5 * L, 11.5, 9, s_fur, group=1)
        p.blob(19.5, 47.5 - L, 7.4, 6.6, s_fur, group=1)
        p.limb(bez((14, 49 - L), (9, 49 - L), (4.5, 50 - 2 * L)), 5.6, 3.2, s_terra, group=4)
        if view != "side":
            p.poly([(30, 61), (33, 57.5), (40, 57), (48, 57.5), (53, 55), (54, 61)], s_earth, group=31)
        _paw(p, 14 + st, 56, 180, s_terra, claw, n=4, r=4.6, ln=4.4, group=13)
        if view != "side":
            p.circle(3.5, 54 - L, 2.4, s_gold, group=14)
        if p.big:
            p.pxs([(16, 45 - L), (17, 45 - L), (18, 45 - L)], "fur0")
        else:
            p.px(17, 46, "fur0")
        return

    if view == "back":
        # draft of the hand-finished back: the hunched velvet back out of
        # the hole, the head turned right, the paws and the coin
        _paw(p, 9.5, 55, 160, s_terra, claw, n=3, r=3.4, ln=3.0, bias=0.1, group=10)
        p.blob(28, 55, 17.5, 15, s_fur, group=1)
        p.blob(45, 50.5, 8, 7, s_fur, group=3)
        p.limb(bez((51, 51.5), (56, 52.5), (60.5, 54.5)), 5.8, 3.2, s_terra, group=4)
        _paw(p, 47.5, 58.5, 0, s_terra, claw, n=3, r=4.2, ln=3.6, group=11)
        p.circle(58.5, 58.5, 2.4, s_gold, group=12)
        p.poly([(1, 64), (2, 60), (14, 59.5), (28, 60.5), (44, 60), (46, 64)], s_earth, group=31)
        return
    return


# --------------------------------------------------------------------------
# Plouteras, wealth with the horn of plenty
# --------------------------------------------------------------------------

PLOUTERAS_COLORS = [
    ("ink", INK),
    # velvety cypress-dark fur, warm olive midtones and a pale sheen
    ("fur0", (32, 48, 48)), ("fur1", (56, 88, 72)), ("fur2", (96, 128, 88)), ("fur3", (152, 176, 128)),
    # limestone horn and claws
    ("lime0", (168, 136, 88)), ("lime1", (216, 192, 144)), ("lime2", (248, 240, 208)),
    # rosy terracotta snout, star and palms
    ("terra0", (144, 64, 56)), ("terra1", (208, 112, 104)), ("terra2", (240, 168, 152)),
    # sun-gold bands, circlet, wheat and coins
    ("gold0", (192, 128, 32)), ("gold1", (248, 208, 72)),
    # olive figs
    ("fig0", (72, 88, 40)), ("fig1", (128, 144, 64)),
]
PLOUTERAS_SHINY = {
    # sun-gold fur, a marble horn
    "fur0": (152, 104, 32), "fur1": (200, 152, 56), "fur2": (232, 192, 96), "fur3": (248, 224, 152),
    "lime0": (176, 176, 176), "lime1": (224, 224, 216), "lime2": (248, 248, 240),
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


def _star(p, cx, cy, r, a0, a1, n, **kw):
    """The fleshy star of feelers round the nose: n short pink rays fanning
    from angle a0 to a1 (degrees) about (cx, cy)."""
    import math
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * k / max(n - 1, 1))
        p.taper([(cx, cy), (cx + math.cos(a) * r, cy + math.sin(a) * r)], 2.0, pl_terra, **kw)
    p.circle(cx, cy, 1.8, pl_terra, **kw)


def _circlet(p, cx, cy, w, L=0):
    """The gold circlet half-buried in the velvet of the brow, leaves up."""
    p.limb(bez((cx - w, cy + 1.5 - L), (cx, cy - 2.5 - L), (cx + w, cy + 1.5 - L)), 1.8, 1.8, pl_gold, group=40)
    for dx in (-w * 0.6, -w * 0.2, w * 0.2, w * 0.6):
        p.lens((cx + dx, cy - 1 - L), (cx + dx * 1.2, cy - 4 - L), 2.2, pl_gold, group=41)


def plouteras(p, view, phase):
    claw = Mat(["lime1", "lime2"], line="ink", cuts=[0.5])
    if view == "down":
        # follower waddling toward the camera: the broad hump, the crowned
        # head low, the star nose, the horn hugged across the front between
        # great spade paws
        st = phase
        p.blob(32, 45, 15, 12, pl_fur, group=1)
        p.blob(32, 42, 9, 8, pl_fur, group=3)
        _circlet(p, 32, 36, 6.5)
        _horn(p, bez3((22, 54), (28, 57), (38, 56), (43, 51)), 9, pl_horn, bands=(0.2, 0.4, 0.6, 0.78), band_mat=pl_gold, group=20)
        p.blob(22, 54, 2.2, 4.4, pl_gold, group=21)
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            _paw(p, 32 + 12 * sx, 55 - up, 90 - 35 * sx, pl_terra, claw, n=4, r=4.0, ln=3.2, group=10 + (sx > 0))
        _star(p, 32, 49, 3.2, -180, 0, 7, group=4)
        p.limb([(32, 45), (32, 48)], 4.4, 3.4, pl_terra, group=4)
        if p.big:
            p.pxs([(27, 41), (28, 41), (36, 41), (37, 41)], "fur0")
        return

    if view == "up":
        # follower waddling away: the great hunched back, the circlet's
        # leaves over the crown, paws out to the sides, the horn's tip
        st = phase
        for sx in (-1, 1):
            up = 2 * (st if sx < 0 else 1 - st)
            _paw(p, 32 + 13.5 * sx, 55 - up, 90 - 40 * sx, pl_terra, claw, n=4, r=3.8, ln=3.0, group=10 + (sx > 0))
        _circlet(p, 32, 33, 6)
        p.blob(32, 47, 15, 13, pl_fur, group=1)
        _horn(p, bez3((44, 58), (49, 57), (50, 52), (47, 50)), 5, pl_horn, bands=(0.35, 0.7), band_mat=pl_gold, group=20)
        return

    if view in ("front", "icon", "side"):
        # the draft of the hand-finished battle front (icon and walking
        # side draw from it): a massive mole hunched over its hoard, the
        # crowned head low, the star nose, the horn of plenty on the gold
        # with its tip gripped in a great clawed paw
        L = 1 if (phase == 1 and view == "front") else 0
        st = phase if view == "side" else 0
        full = view == "front"
        if full:
            p.blob(26, 64, 23, 9.5, pl_gold, group=50)
        p.blob(56.5, 58.5, 5.2, 2.6, pl_terra, bias=0.1, group=11)
        p.blob(42, 33, 19.5, 16.5, pl_fur, group=1)
        p.blob(52, 47.5, 9.5, 9, pl_fur, group=1)
        p.blob(29, 38.5 - 0.5 * L, 8.5, 8.5, pl_fur, group=1)
        p.blob(18.5, 38 - L, 10.2, 9.2, pl_fur, group=3)
        _circlet(p, 18.5, 31, 8, L)
        _paw(p, 46 - st, 53.5, 180, pl_terra, claw, n=3, r=4.6, ln=4.6, bias=0.12, group=12)
        _horn(p, bez3((11.5, 53), (17, 56), (26, 56), (33, 51)) + bez3((33, 51), (37.5, 47.5), (37, 43), (33.5, 44.5))[1:],
              13, pl_horn, bands=(0.1, 0.22, 0.34, 0.46, 0.58, 0.69, 0.79), band_mat=pl_gold, group=20)
        p.blob(11.5, 53, 2.8, 6.6, pl_gold, ang=20, group=21)
        p.blob(11.2, 53, 1.5, 5.0, Mat(["fur0"]), ang=20, group=22)
        if full and p.big:
            for b_, t_ in (((10, 55), (3.5, 57.5 + L)), ((12.5, 50), (12, 43 - L))):
                _wheat(p, b_, t_, {"group": 23})
            _fig(p, 6, 59 - L, 2.3, ang=-30, group=24)
            _fig(p, 17.5, 58.4, 2.2, ang=20, group=25)
        _paw(p, 36 + st, 44.5 - 0.5 * L, 200, pl_terra, claw, n=3, r=5.0, ln=4.4, group=13)
        p.limb(bez3((11, 42 - L), (8.5, 43 - L), (7, 45 - L), (6.5, 46.5 - 2 * L)), 6.2, 4.0, pl_terra, group=4)
        _star(p, 6.6, 48 - 2 * L, 4.4, 90, 270, 9, group=4)
        if p.big:
            p.pxs([(12, 37 - L), (13, 37 - L), (14, 37 - L)], "fur0")
        else:
            p.px(13, 37, "fur0")
        return

    if view == "back":
        # draft of the hand-finished back: the hunched velvet back, the
        # crowned head turned right with its star nose, a great paw on the
        # horn of plenty, the hoard glinting at the left
        p.blob(10, 66, 13, 10, pl_gold, group=50)
        _paw(p, 9.5, 52, 160, pl_terra, claw, n=3, r=4.0, ln=3.6, bias=0.1, group=10)
        p.blob(26, 55, 23, 24, pl_fur, group=1)
        p.blob(40, 45, 11, 10, pl_fur, group=1)
        p.blob(49.5, 42, 9.6, 8.6, pl_fur, group=3)
        _circlet(p, 49, 36, 7.5)
        _horn(p, bez3((58, 58.5), (52, 61), (43, 61), (36, 57)), 11, pl_horn, bands=(0.15, 0.35, 0.55, 0.75), band_mat=pl_gold, group=20)
        _paw(p, 47, 54, 0, pl_terra, claw, n=3, r=5.0, ln=4.4, group=11)
        p.limb(bez3((55, 45), (57.5, 46), (59, 48), (59.5, 49.5)), 6, 4, pl_terra, group=4)
        _star(p, 59.5, 51.2, 3.0, -60, 100, 7, group=4)
        return
    return


MONS = [
    # icon palette 1 keeps the velvet green and the rosy snout
    Mon("Spalunk", SPALUNK_COLORS, SPALUNK_SHINY, spalunk, foot="claw", icon_pal=1),
    Mon("Plouteras", PLOUTERAS_COLORS, PLOUTERAS_SHINY, plouteras, foot="claw", icon_pal=1),
]
