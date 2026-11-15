"""Khalkotauros line: Kaminoo, Taurivet (Fire, then Fire/Steel). The
fire-breathing bronze bulls Hephaestus made for King Aeetes of Colchis, which
Jason yoked under Medea's balm (Apollonius, Argonautica 3)."""
from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# Kaminoo, the furnace calf
# --------------------------------------------------------------------------

KAMINOO_COLORS = [
    ("ink", INK),
    # terracotta hide, and the darker saddle over its back
    ("sad0", (72, 32, 24)), ("hide0", (120, 48, 24)), ("hide1", (168, 80, 40)), ("hide2", (208, 120, 64)),
    ("hide3", (232, 168, 112)),
    # pale limestone muzzle and horn nubs
    ("muz0", (176, 144, 96)), ("muz1", (232, 216, 176)),
    # the sun-gold nose ring, glowing like a coal
    ("gold0", (200, 120, 32)), ("gold1", (248, 208, 72)), ("glow", (248, 120, 40)),
    # marble-gray smoke
    ("smoke0", (152, 144, 144)), ("smoke1", (208, 200, 192)),
    ("white", C.white),
    ("hoof", (56, 40, 40)),
]
KAMINOO_SHINY = {
    # black-figure dark hide, the ring burning blue-white
    "sad0": (24, 24, 32), "hide0": (40, 40, 48), "hide1": (64, 64, 72), "hide2": (96, 96, 104), "hide3": (136, 136, 144),
    "gold0": (88, 136, 200), "gold1": (200, 232, 248), "glow": (120, 184, 248),
}

m_hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.2, 0.44, 0.7])
m_sad = Mat(["sad0", "hide0", "hide1"], line="sad0", cuts=[0.3, 0.62])
m_muz = Mat(["muz0", "muz1"], line="muz0", cuts=[0.55])
m_horn = Mat(["muz0", "muz1"], line="muz0", cuts=[0.5])
m_hoof = Mat(["hoof", "sad0"], line="hoof", cuts=[0.55])
m_gold = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])
m_smoke = Mat(["smoke0", "smoke1"], line="smoke0", outline="smoke0", cuts=[0.45])
m_ember = Mat(["glow", "gold1"], line="glow", cuts=[0.5])


def _ring(p, cx, cy, r, w=1.6):
    """The nose ring: a gold hoop, its far half behind the septum."""
    outer = ellipse_pts(cx, cy, r, r * 1.05)
    inner = ellipse_pts(cx, cy, r - w, (r - w) * 1.05)
    p.add(p.mask(outer) & ~p.mask(inner), m_gold, group=60)


def kaminoo(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        walk = view == "side" and phase == 1

        # tail: up from the rump, the tuft tipped with an ember
        p.limb(bez((48, 42), (51.5, 40.5), (51.5, 35.5 - L)), 2.2, 1.8, m_hide, group=20)
        p.lens((51.5, 36.5 - L), (52.5 - L, 30 - L), 3.8, m_sad, bend=-0.6, group=21)
        p.lens((52.3 - L, 32 - L), (53 - L, 28 - L), 2.8, m_ember, group=22)

        # far legs, in shade
        p.limb([(34, 50), (33.5 + walk, 55), (33.5 + walk, 58)], 4.8, 4.0, m_hide, bias=0.36, group=10)
        p.rect(31.5 + walk, 58, 35.5 + walk, 59, m_hoof, bias=0.3, group=10)
        p.limb([(41.5, 49), (41 - walk, 54), (41.5 - walk, 58)], 4.8, 4.0, m_hide, bias=0.36, group=11)
        p.rect(39.5 - walk, 58, 43.5 - walk, 59, m_hoof, bias=0.3, group=11)

        # body: stocky barrel, deep chest, round rump
        body = p.blob(38.5, 46.5, 8.5, 6.4, m_hide, ang=-4, group=1)
        p.blob(31.5, 47, 6.2, 6.8, m_hide, group=1)
        p.blob(45.5, 45.5, 5.8, 6.4, m_hide, group=1)
        # the darker saddle over the back
        p.blob(40, 41.5, 7.5, 3.6, m_sad, ang=-8, clip=[body], group=2)

        # near hind leg: the round haunch over a short shank
        p.blob(46, 47, 5.2, 6.2, m_hide, group=13)
        p.limb([(47, 50), (48.5, 54), (48 - walk, 58)], 5.4, 4.4, m_hide, group=13)
        p.rect(45.5 - walk, 58, 50.5 - walk, 59, m_hoof, group=13)

        # near foreleg, braced forward, the hoof planted
        p.blob(29.5, 50, 4.8, 5.2, m_hide, group=12)
        p.limb([(28.5, 52), (26.5 - walk, 55), (26 - walk, 58)], 5.4, 4.4, m_hide, group=12)
        p.rect(23.5 - walk, 58, 28.5 - walk, 59, m_hoof, group=12)

        # head, lowered to butt and turned to the foe: the big round skull,
        # the broad muzzle, both eyes glaring up from under the poll
        far_ear = p.lens((12.5, 38 - L), (4.5, 35.5 - 2 * L), 4.8, m_hide, bend=0.6, fat=0.4, bias=0.2, group=5)
        p.lens((11.5, 37.6 - L), (6.5, 36.2 - 2 * L), 1.8, Mat(["hide3"]), clip=[far_ear], group=5)
        p.lens((15, 34 - L), (13, 29.5 - L), 3.2, m_horn, fat=0.3, bias=0.15, group=8)
        p.blob(20, 41 - L, 9, 8.2, m_hide, group=3)
        p.blob(20.5, 46 - L, 7.6, 4.6, m_hide, group=3)
        p.blob(16.5, 49.5 - L, 6.2, 4.2, m_muz, group=4)
        p.lens((23.5, 34 - L), (25, 29 - L), 3.8, m_horn, fat=0.3, group=7)
        ear = p.lens((27, 38.5 - L), (35, 36 - 2 * L), 5.2, m_hide, bend=-0.6, fat=0.4, group=6)
        p.lens((28, 38 - L), (33, 36.6 - 2 * L), 1.8, Mat(["hide3"]), clip=[ear], group=6)

        # the nose ring
        _ring(p, 16.5, 54.5 - L, 3.1, 1.9)

        # a puff of smoke from the nostrils
        if view == "front":
            p.blob(8.5, 47 - L, 2.8, 2.3, m_smoke, group=30)
            p.blob(5.5, 43 - 2 * L, 2.2, 2.0, m_smoke, group=31)
            p.blob(7, 39 - 2 * L, 1.5, 1.4, m_smoke, group=32)

        if p.big:
            p.eye(20, 38 - L, 4, 6, shine="white", shine_at=(2, 1))
            p.eye(12, 38 - L, 3, 5, shine="white", shine_at=(1, 1))
            p.pxs([(14, 50 - L), (19, 50 - L)], "ink")
        else:
            p.pxs([(21, 40 - L), (13, 40 - L)], "ink")
        return

    if view == "back":
        # over the shoulder: the saddled back and round rump close at the
        # lower left, the head turned right in profile; cropped below
        p.limb(bez((9, 48), (3.5, 44), (4.5, 36.5)), 3.2, 2.6, m_hide, group=20)
        p.lens((4.5, 37.5), (6.5, 28), 5.4, m_sad, bend=0.6, group=21)
        p.lens((6.3, 31.5), (7.6, 25.5), 3.6, m_ember, group=22)
        p.lens((49.5, 22), (50, 16), 3.4, m_horn, fat=0.3, bias=0.15, group=8)
        body = p.blob(25, 57, 24, 18, m_hide, group=1)
        p.blob(38, 45, 12.5, 10.5, m_hide, group=1)
        p.blob(23, 46.5, 17, 6.6, m_sad, ang=-8, clip=[body], group=2)
        p.blob(45, 31, 10, 9.5, m_hide, group=3)
        p.limb([(50, 35), (55, 37.5)], 11, 10, m_hide, group=3)
        p.blob(56.5, 38, 5.6, 5, m_muz, ang=10, group=4)
        p.lens((44.5, 22.5), (42.5, 16), 4.2, m_horn, fat=0.3, group=7)
        ear = p.lens((41, 28), (31, 28.5), 6.4, m_hide, bend=0.7, fat=0.4, group=6)
        p.lens((40, 28), (33.5, 28.4), 2.2, Mat(["hide3"]), clip=[ear], group=6)
        _ring(p, 57.5, 46, 3.5, 2.1)
        p.eye(48, 26, 4, 6, shine="white", shine_at=(1, 1))
        if p.big:
            p.pxs([(60, 36), (61, 36)], "ink")
        return

    if view == "down":
        # follower trotting toward the camera, snorting sparks
        st = phase
        for sx in (-1, 1):
            k = st if sx < 0 else 1 - st
            p.limb([(32 + 5 * sx, 50), (32 + 5.5 * sx, 59 - 2 * k)], 4.6, 4.2, m_hide, group=12 + (sx > 0))
            p.rect(32 + 5.5 * sx - 2, 58 - 2 * k, 32 + 5.5 * sx + 2, 59 - 2 * k, m_hoof, group=14 + (sx > 0))
        p.blob(32, 48, 9.5, 7, m_hide, group=1)
        p.blob(32, 43, 7, 3, m_sad, group=2)
        for sx in (-1, 1):
            p.lens((32 + 6 * sx, 37), (32 + 12 * sx, 35 - st * (sx > 0)), 4.4, m_hide, bend=0.5 * sx, group=5 + sx)
            p.lens((32 + 3.5 * sx, 33), (32 + 4.5 * sx, 29), 2.8, m_horn, fat=0.3, group=8 + sx)
        p.blob(32, 39, 7.6, 7, m_hide, group=3)
        p.blob(32, 45, 5, 3.6, m_muz, group=4)
        _ring(p, 32, 49.5, 2.2, 1.4)
        if p.big:
            p.eye(27, 37, 2, 3, shine="white")
            p.eye(35, 37, 2, 3, shine="white")
            p.pxs([(30, 45), (33, 45)], "ink")
            p.pxs([(26 - st, 47 - st), (39 + st, 48 - st)], "gold1")
        return

    if view == "up":
        # follower trotting away: rump, saddle, tail with its ember
        st = phase
        for sx in (-1, 1):
            k = st if sx < 0 else 1 - st
            p.limb([(32 + 5.5 * sx, 50), (32 + 6 * sx, 59 - 2 * k)], 5, 4.4, m_hide, group=12 + (sx > 0))
            p.rect(32 + 6 * sx - 2, 58 - 2 * k, 32 + 6 * sx + 2, 59 - 2 * k, m_hoof, group=14 + (sx > 0))
        for sx in (-1, 1):
            p.lens((32 + 5 * sx, 34), (32 + 11 * sx, 32 - st * (sx > 0)), 4.4, m_hide, bend=0.5 * sx, group=5 + sx)
            p.lens((32 + 3.5 * sx, 31), (32 + 4.5 * sx, 27), 2.8, m_horn, fat=0.3, group=8 + sx)
        p.blob(32, 36, 7, 6, m_hide, group=3)
        p.blob(32, 47, 10, 8.4, m_hide, group=1)
        p.blob(32, 42, 7.5, 4, m_sad, group=2)
        p.limb(bez((32, 48), (33, 44), (32 + st, 41)), 2, 1.6, m_hide, group=20)
        p.lens((32 + st, 42), (32 + 2 * st, 36), 3.4, m_sad, group=21)
        p.lens((32 + 2 * st, 38), (32.5 + 2 * st, 34.5), 2.4, m_ember, group=22)
        return


# --------------------------------------------------------------------------
# Taurivet, the bronze bull
# --------------------------------------------------------------------------

TAURIVET_COLORS = [
    ("ink", INK),
    # terracotta bronze: the hide between the plates
    ("cu0", (80, 32, 24)), ("cu1", (128, 56, 32)), ("cu2", (176, 96, 48)), ("cu3", (216, 144, 88)),
    # sun-gold bronze: the riveted plates, horns and hooves
    ("au0", (136, 80, 24)), ("au1", (192, 128, 40)), ("au2", (232, 184, 72)), ("au3", (248, 232, 152)),
    ("marble", C.white),
    # the furnace: one hot orange accent
    ("fire0", (200, 48, 24)), ("fire1", (248, 120, 32)), ("fire2", (248, 184, 56)),
    # exhaust
    ("smoke0", (88, 80, 88)), ("smoke1", (144, 136, 136)),
]
TAURIVET_SHINY = {
    # black iron, the furnace burning blue-white
    "cu0": (32, 32, 40), "cu1": (56, 56, 64), "cu2": (88, 88, 96), "cu3": (128, 128, 144),
    "au0": (64, 64, 80), "au1": (104, 104, 120), "au2": (152, 152, 168), "au3": (208, 216, 232),
    "fire0": (40, 72, 184), "fire1": (72, 136, 240), "fire2": (136, 200, 248),
}

t_hide = Mat(["cu0", "cu1", "cu2", "cu3"], line="cu0", cuts=[0.22, 0.46, 0.72])
t_plate = Mat(["au0", "au1", "au2", "au3"], line="cu0", cuts=[0.2, 0.44, 0.7])
t_horn = Mat(["au0", "au1", "au2", "au3"], line="au0", cuts=[0.2, 0.46, 0.74])
t_hoof = Mat(["au0", "au1", "au2"], line="cu0", cuts=[0.34, 0.66])
t_fire = Mat(["fire0", "fire1", "fire2", "au3"], line="fire0", outline="ink", cuts=[0.2, 0.42, 0.66])
t_flame = Mat(["fire1", "fire2", "au3", "marble"], line="fire1", outline="fire0", cuts=[0.24, 0.5, 0.76])
t_smoke = Mat(["smoke0", "smoke1"], line="smoke0", outline="smoke0", cuts=[0.5])
t_grate = Mat(["ink"])


def _horn(p, path, w, **kw):
    """A great bronze horn along path, thick at the root, curling to a point."""
    a = p._minw(w)
    poly = ribbon(path, lambda t: a * (1 - t ** 1.6) + 0.5 * t)
    return p.add(p.mask(poly, ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12)), t_horn, **kw)


def _rivets(p, pts):
    """Marble-headed rivets, each with a shadow pixel below right."""
    if not p.big:
        return
    for x, y in pts:
        p.px(x + 1, y + 1, "au0")
        p.px(x, y, "marble")


NEAR_HORN = bez3((8, 31), (3.5, 31.5), (2.5, 23), (5.5, 15))
FAR_HORN = bez3((19.5, 29.5), (27, 28.5), (30, 20), (27.5, 9.5))


def taurivet(p, view, phase):
    if view in ("front", "side", "icon"):
        # mid-charge, head lowered, the lyre of horns forward; the battle
        # sprites are hand-finished from this (art/taurivet_*.txt)
        L = 1 if (phase == 1 and view == "front") else 0
        walk = view == "side" and phase == 1
        big = p.big

        # tail lashing up, a flame for a tuft
        p.limb(bez3((56, 27), (61.5, 25), (62, 18), (59.5, 14)), 2.8, 2.2, t_hide, group=20)
        p.lens((59.5, 15.5), (57, 3.5), 6.0, t_flame, bend=1.0, fat=0.42, group=21)

        # far legs, in shade: the far foreleg folded mid-stride
        p.limb([(47.5, 42), (47.5, 50), (45 + walk, 56.5)], 9.4, 6.4, t_hide, bias=0.34, group=10)
        p.poly([(41 + walk, 56), (48.5 + walk, 56), (49 + walk, 60.5), (40.5 + walk, 60.5)], t_hoof, bias=0.3, group=10)
        p.limb([(36, 42.5), (39.5, 48.5), (36.5, 53)], 9, 6.6, t_hide, bias=0.34, group=11)
        p.poly([(31.5, 51.5), (37, 50.5), (39, 55.5), (33, 57)], t_hoof, bias=0.3, group=11)

        # body: the shoulder hump, the barrel, the haunch
        hump = p.blob(30.5, 26.5, 14, 14, t_hide, group=1)
        barrel = p.blob(42, 35, 14, 11, t_hide, ang=6, group=1)
        rump = p.blob(53, 33.5, 8, 10, t_hide, group=1)
        chest = p.blob(26.5, 37.5, 9.5, 10, t_hide, group=1)
        p.blob(40, 44.5, 12, 2.6, t_hide, bias=0.3, clip=[barrel, chest], group=1)
        body = [hump, barrel, rump, chest]
        # riveted plates: the lame and pauldron over the hump, the flank barding
        p.blob(31.5, 23, 15.5, 14, t_plate, clip=body, group=2)
        p.blob(31.5, 20.5, 14, 11.5, t_plate, clip=body, group=3)
        p.poly([(39, 27), (51.5, 25), (51, 41.5), (41, 43)], t_plate, clip=[barrel, rump], group=4)
        if big:
            # the furnace grate in the chest
            p.blob(30, 40.5, 4.6, 4, t_fire, clip=[chest], group=50)
            for gx in (27, 29, 31, 33):
                p.rect(gx, 38, gx, 43, t_grate, clip=[chest], group=50, flat=0)

        # near hind leg driving back, its thigh plated
        thigh = p.blob(53, 39.5, 7.5, 8.6, t_hide, group=13)
        p.limb([(55, 45), (59.5 - walk, 50.5), (59 - walk, 56.5)], 9, 6, t_hide, group=13)
        p.blob(54, 37, 6.4, 7.4, t_plate, clip=[thigh], group=14)
        p.poly([(55.5 - walk, 56), (62 - walk, 56), (62.2 - walk, 60.5), (55 - walk, 60.5)], t_hoof, group=13)

        # the far horn sweeps out and up behind the head
        p.taper(FAR_HORN, 8.4, t_horn, group=40)
        # the head, lowered and turned to the foe, a chanfron down its face
        p.blob(14.5, 35.5 - L, 10.5, 9.5, t_hide, group=5)
        p.blob(14.5, 31.5 - L, 11, 5, t_hide, group=5)
        p.limb([(14.5, 40 - L), (14.5, 47 - L)], 15, 13, t_hide, group=5)
        p.blob(14.5, 48.5 - L, 7.2, 4.6, t_hide, group=5)
        p.lens((14.5, 26 - L), (14, 46 - L), 8.6, t_plate, fat=0.34, group=6)
        p.taper(NEAR_HORN, 7.8, t_horn, group=41)

        # near foreleg planted forward, its knee plated
        nf = [(27, 51), (24, 54), (22, 56.5)] if not walk else [(27, 51), (26, 54), (26.5, 56.5)]
        p.blob(28, 49.5, 6.4, 5.8, t_hide, group=12)
        p.limb(nf, 8.8, 6.4, t_hide, group=12)
        p.blob(nf[1][0] + 1, 53.5, 3.6, 2.8, t_plate, group=15)
        hx = nf[-1][0] - 5
        p.poly([(hx, 56), (hx + 9, 56), (hx + 9, 60.5), (hx - 1, 60.5)], t_hoof, group=12)

        # the heavy nose ring, red-hot
        outer = ellipse_pts(14.5, 55.5 - L, 4.5, 4.6)
        inner = ellipse_pts(14.5, 55.5 - L, 2.0, 2.1)
        p.add(p.mask(outer) & ~p.mask(inner), t_horn, group=60)

        if view == "front":
            # flame snorted from the nostril, curling up at the tip
            p.lens((8.5, 48 - L), (3.5, 57), 5.6, t_flame, bend=-1.4, fat=0.55, group=70)
            p.lens((3.5, 56), (3.5, 48.5 - L), 4.0, t_flame, bend=-0.8, group=71)
            # a curl of smoke off the flame's tip
            p.circle(3.5, 43.5 - 2 * L, 1.6, t_smoke, group=72)
            p.circle(4.5, 40 - 2 * L, 1.1, t_smoke, group=73)

        if big:
            # furnace eyes either side of the chanfron, flared nostrils
            p.patch(9, 33 - L, ["11..", "1da1"], {"1": "ink", "d": "fire2", "a": "marble"})
            p.patch(19, 33 - L, [".111", "1ad1"], {"1": "ink", "d": "fire2", "a": "marble"})
            p.pxs([(10, 46 - L), (17, 46 - L)], "fire1")
            _rivets(p, [(22, 18), (30, 21), (38, 20), (23, 28), (31, 30), (39, 29), (45, 38), (49, 36)])
        else:
            p.pxs([(10, 34 - L), (19, 34 - L)], "fire2")
        return

    if view == "back":
        # over the shoulder: the riveted spine running up the great hump,
        # the head turned right in profile, flame from the nostril
        p.limb(bez((8, 54), (2.5, 50), (3, 42)), 3.4, 2.6, t_hide, group=20)
        p.lens((3, 43), (6, 33), 5.4, t_flame, bend=-0.8, group=21)
        _horn(p, bez3((45, 23), (49, 16), (55, 14), (58, 8)), 5.6, bias=0.2, group=40)
        back = p.blob(26, 62, 24, 20, t_hide, group=1)
        sh = p.blob(36, 40, 16, 15, t_hide, group=1)
        p.blob(22, 50, 14, 10, t_plate, ang=-25, clip=[back], group=2)
        p.blob(36, 36, 12, 10, t_plate, ang=-20, clip=[sh], group=3)
        # spine plates
        for i, (x, y) in enumerate(((8, 52), (14, 46.5), (20, 42), (26, 37.5), (32, 33.5), (38, 30))):
            p.blob(x, y, 3.2, 2.4, t_plate, ang=-35, group=30 + i)
        p.blob(47, 31, 9.5, 9.5, t_hide, group=5)
        p.limb([(50, 35), (57, 41)], 11.5, 8.5, t_hide, group=5)
        p.blob(58, 42, 4.6, 4.2, t_hide, group=5)
        p.lens((42, 26), (55, 36), 7, t_plate, bend=1.0, group=6)
        _horn(p, bez3((44, 27), (50, 24), (56, 22), (59, 15)), 6.2, group=41)
        outer = ellipse_pts(59, 47.5, 3.4, 3.6)
        inner = ellipse_pts(59, 47.5, 1.4, 1.6)
        p.add(p.mask(outer) & ~p.mask(inner), t_horn, group=60)
        p.lens((60.5, 42), (63, 34), 4, t_flame, bend=0.6, group=70)
        if p.big:
            p.patch(48, 29, [".111.", "1ddc1", ".111."], {"1": "ink", "c": "fire2", "d": "au3"})
        return

    if view == "down":
        # follower charging toward the camera: horns wide, ring swinging
        st = phase
        for sx in (-1, 1):
            k = st if sx < 0 else 1 - st
            p.limb([(32 + 8 * sx, 48), (32 + 8.5 * sx, 59 - 2 * k)], 6.6, 5, t_hide, group=12 + (sx > 0))
            p.rect(32 + 8.5 * sx - 3, 57 - 2 * k, 32 + 8.5 * sx + 2.5, 59 - 2 * k, t_hoof, group=14 + (sx > 0))
        p.blob(32, 42, 14, 11, t_hide, group=1)
        p.blob(32, 37, 12, 6, t_plate, group=2)
        for sx in (-1, 1):
            _horn(p, bez3((32 + 6 * sx, 32), (32 + 14 * sx, 33), (32 + 18 * sx, 29), (32 + 17 * sx, 22)), 5.4,
                  group=40 + (sx > 0))
        p.blob(32, 38, 8.6, 8, t_hide, group=3)
        p.lens((32, 30), (32, 41), 6.4, t_plate, group=4)
        p.blob(32, 46, 6.4, 4.4, t_hide, bias=-0.1, group=5)
        outer = ellipse_pts(32, 51, 3.4, 3.4)
        inner = ellipse_pts(32, 51, 1.4, 1.4)
        p.add(p.mask(outer) & ~p.mask(inner), t_horn, group=60)
        if p.big:
            for ex in (25, 36):
                p.patch(ex, 37, [".11.", "1cd1", ".11."], {"1": "ink", "c": "fire2", "d": "au3"})
            p.pxs([(29, 46), (34, 46)], "ink")
            p.pxs([(27 - st, 49 + st), (37 + st, 49 + st)], "fire1")
        return

    if view == "up":
        # follower charging away: the riveted spine, the haunches, the tail
        st = phase
        for sx in (-1, 1):
            k = st if sx < 0 else 1 - st
            p.limb([(32 + 8.5 * sx, 48), (32 + 9 * sx, 59 - 2 * k)], 7, 5.2, t_hide, group=12 + (sx > 0))
            p.rect(32 + 9 * sx - 3, 57 - 2 * k, 32 + 9 * sx + 2.5, 59 - 2 * k, t_hoof, group=14 + (sx > 0))
        for sx in (-1, 1):
            _horn(p, bez3((32 + 6 * sx, 27), (32 + 14 * sx, 28), (32 + 18 * sx, 24), (32 + 17 * sx, 17)), 5.4,
                  group=40 + (sx > 0))
        p.blob(32, 30, 11, 7, t_hide, group=3)
        p.blob(32, 42, 15, 12, t_hide, group=1)
        p.blob(23, 44, 6, 7, t_plate, group=2)
        p.blob(41, 44, 6, 7, t_plate, group=3)
        for i, y in enumerate((31, 35, 39, 43)):
            p.blob(32, y, 2.6, 1.8, t_plate, group=30 + i)
        p.limb(bez((32, 49), (34, 46), (33 + st, 40)), 2.4, 2, t_hide, group=20)
        p.lens((33 + st, 41), (34 + 2 * st, 33), 4.2, t_flame, group=21)
        return


# --------------------------------------------------------------------------

MONS = [
    Mon("Kaminoo", KAMINOO_COLORS, KAMINOO_SHINY, kaminoo, foot="hoof"),
    Mon("Taurivet", TAURIVET_COLORS, TAURIVET_SHINY, taurivet, foot="hoof"),
]
