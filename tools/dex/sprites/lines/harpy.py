"""Harpy line: Harpeck, Harpelle (Dark/Flying). The Harpies, "the
snatchers", storm-wind spirits that stole blind Phineus's every meal."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Harpeck, the snatcher fledgling
# --------------------------------------------------------------------------

HARPECK_COLORS = [
    ("ink", INK),
    # ragged marble-gray down
    ("down0", (104, 96, 104)), ("down1", (152, 144, 152)), ("down2", (200, 192, 192)), ("down3", (240, 232, 232)),
    # the black-figure hood, talons and legs
    ("hood0", (40, 40, 56)), ("hood1", (64, 64, 88)), ("hood2", (104, 104, 128)),
    # horn beak
    ("beak0", (144, 120, 88)), ("beak1", (208, 184, 136)),
    # sun-gold eyes
    ("gold0", (200, 144, 40)), ("gold1", (248, 208, 72)),
    # the stolen olive
    ("olive0", (56, 72, 32)), ("olive1", (104, 128, 48)), ("olive2", (168, 184, 96)),
]
HARPECK_SHINY = {
    # sandy limestone down, terracotta eyes
    "down0": (144, 112, 72), "down1": (176, 144, 96), "down2": (208, 184, 136), "down3": (232, 216, 176),
    "gold0": (184, 88, 48), "gold1": (232, 144, 96),
}

k_down = Mat(["down0", "down1", "down2", "down3"], line="down0", cuts=[0.18, 0.44, 0.72])
k_hood = Mat(["hood0", "hood1", "hood2"], line="hood0", cuts=[0.34, 0.68])
k_beak = Mat(["beak0", "beak1"], line="beak0", cuts=[0.5])
k_olive = Mat(["olive0", "olive1", "olive2"], line="olive0", cuts=[0.3, 0.7])
k_claw = Mat(["hood0", "hood1"], cuts=[0.6])


def _tufts(p, cx, cy, rx, ry, angs, mat, ln=2.6, w=2.2, group=None, bias=0.0):
    """Ragged down sticking out of an ellipse's rim at the given angles
    (degrees, 0 = right, 90 = down)."""
    for i, a in enumerate(angs):
        r = math.radians(a)
        bx, by = cx + rx * 0.82 * math.cos(r), cy + ry * 0.82 * math.sin(r)
        l = ln * (0.75 + 0.5 * ((i * 7) % 3) / 2)
        tx, ty = cx + (rx + l) * math.cos(r + 0.25), cy + (ry + l) * math.sin(r + 0.25)
        p.lens((bx, by), (tx, ty), w, mat, group=group, bias=bias)


def _talon_foot(p, x, y, spread, mat, claw, big=1.0, bias=0.0):
    """A hooked bird foot, the ankle at (x, y). spread: list of toe angles
    (degrees, 0 = left, 90 = down); each toe ends in a hooked claw."""
    for a in spread:
        r = math.radians(a)
        ln = 3.6 * big
        tx, ty = x - ln * math.cos(r), y + ln * math.sin(r)
        p.limb([(x, y), (tx, ty)], 2.0 * big, 1.6 * big, mat, bias=bias)
        # the hooked claw curling down from the toe tip
        cx, cy = tx - 1.6 * big * math.cos(r - 0.9), ty + 1.6 * big * math.sin(r - 0.9) + 0.4
        p.taper(bez((tx, ty), (tx - 1.2 * math.cos(r), ty + 1.2 * math.sin(r) - 0.6), (cx, cy + 0.8)),
                1.6 * big, claw, bias=bias)


def harpeck(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        hop = phase if view == "side" else 0

        # far wing, a ragged stub raised behind the back
        p.lens((38, 44), (47.5, 36 - 2 * L), 6.6, k_down, bend=-1.2, bias=0.32, group=20)
        p.lens((44, 40 - L), (49, 35.5 - 2 * L), 2.6, k_down, bias=0.32, group=20)
        # tail, a short ragged tuft
        p.lens((41, 51), (49.5, 48), 4.8, k_down, bend=0.8, bias=0.12, group=21)
        p.lens((41, 53), (48.5, 53.5), 3.8, k_down, bias=0.22, group=21)

        # far leg, planted, its foot gripping the ground
        p.limb([(37.5, 55), (38, 58.5)], 3.0, 2.6, k_hood, bias=0.25, group=11)
        _talon_foot(p, 38, 58.5, (5, 35), k_hood, Mat(["ink"]), big=0.9, bias=0.25)

        # body: a round, scruffy ball of down
        body = p.blob(34.5, 49, 9.6, 8.6, k_down, ang=-10, group=1)
        for a, b_, w in (((26.5, 47), (23.5, 49.5), 3.0), ((27.5, 51), (25, 54.5), 2.8),
                         ((33, 56), (31.5, 59.5), 3.0), ((40.5, 41.5), (43, 39), 2.8)):
            p.lens(a, b_, w, k_down, group=1)

        # the big head under its dark hood
        head = p.blob(29, 36 - L, 8.8, 8.2, k_down, group=3)
        # the hood: a cowl over the crown and nape, ragged where it ends
        p.poly(bez3((20.5, 36 - L), (20, 27 - L), (32, 24 - L), (37.5, 30 - L)) +
               [(38.8, 37 - L), (38.5, 42 - L), (36.5, 44.5 - L), (35.5, 40.5 - L), (33.5, 42.5 - L),
                (32.5, 39 - L), (30, 40 - L), (29, 36.5 - L), (26.5, 34.5 - L), (21.5, 37.5 - L)],
               k_hood, group=4)
        # scruffy hood feathers standing up off the crown
        p.lens((30, 28.5 - L), (31.5, 23.5 - L), 3.2, k_hood, bend=-0.4, group=4)
        p.lens((33.5, 28.5 - L), (37.5, 25 - L), 3.0, k_hood, bend=-0.4, group=4)

        # the hooked beak, the stolen olive clamped at its tip
        p.blob(16.8, 41.6 - L, 2.6, 2.3, k_olive, ang=-20)
        p.poly(bez((23, 35.5 - L), (17, 34 - L), (15, 39.5 - L)) +
               [(16, 40.5 - L), (17.5, 39 - L), (22.5, 39.5 - L)], k_beak)
        p.poly([(22.5, 39.6 - L), (18.5, 39.8 - L), (19, 41.8 - L), (22.5, 41.6 - L)], k_beak, bias=0.3)

        # near wing, a stubby ragged fan held up for balance
        p.lens((34, 45 - L), (44.5, 41 - 2 * L), 6.8, k_down, bend=1.4, group=22)
        for a, b_ in (((40, 44 - L), (46, 44.5 - 2 * L)), ((38.5, 46.5 - L), (44, 48 - L))):
            p.lens(a, b_, 2.8, k_down, group=22)

        # near leg thrust forward to snatch, the oversized hooked foot
        p.blob(30, 55.5, 3.6, 3.0, k_down, group=12)
        p.limb([(29, 56.5), (24, 56.5 - hop)], 3.2, 2.8, k_hood, group=13)
        _talon_foot(p, 23.5, 56.5 - hop, (-30, 12, 52), k_hood, Mat(["ink"]), big=1.3)

        if p.big:
            p.eye(23, 34 - L, 4, 4, iris="gold1", shine="down3", shine_at=(1, 1))
        else:
            p.px(24, 35 - L, "gold1")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the scruffy round back under the
        # ragged hood, a stub wing raised, the hooded head turned right in
        # profile with the stolen olive in its beak
        p.lens((20, 46), (8, 34), 7.6, k_down, bend=1.4, bias=0.2, group=20)
        p.lens((15, 40), (6, 37), 3.2, k_down, bias=0.2, group=20)
        p.lens((17, 43), (7, 42.5), 3.0, k_down, bias=0.2, group=20)
        body = p.blob(29, 60, 21, 17, k_down, group=1)
        for a_, b_, w in (((9, 52), (4, 50), 3.4), ((10, 57), (4.5, 57), 3.2), ((48, 52), (53, 49), 3.2),
                          ((49, 58), (55, 57), 3.0)):
            p.lens(a_, b_, w, k_down, group=1)
        # the hood's ragged cape over the shoulders
        p.poly(bez3((30, 40), (24, 42), (22, 47), (21, 50)) +
               [(24, 48), (26, 52), (29, 49), (32, 53), (35, 49), (38, 52), (40, 48), (43, 50), (44, 45)] +
               bez((44, 45), (42, 41), (38, 39)), k_hood, group=4)
        p.blob(40, 31, 9.5, 9, k_down, group=3)
        p.blob(39, 27, 9, 7, k_hood, group=4)
        p.lens((40, 21), (42, 14), 3.4, k_hood, group=4)
        p.lens((36, 22), (31, 16), 3.2, k_hood, group=4)
        p.poly(bez((46, 28), (54, 27), (57, 33)) + [(55.5, 34), (54, 32.5), (47, 33)], k_beak)
        p.blob(56.5, 36, 2.8, 2.4, k_olive)
        p.eye(43, 27, 4, 4, iris="gold1", shine="down3", shine_at=(2, 1))
        return

    if view in ("down", "up"):
        # follower: the hooded chick hopping toward (down) or away (up)
        st = phase
        for x, s_ in ((28, st), (36, 1 - st)):
            p.limb([(x, 52), (x, 58 - s_)], 3, 2.6, k_hood)
            for dx in (-2.5, 0, 2.5):
                p.limb([(x, 58 - s_), (x + dx, 60.5 - s_)], 1.8, 1.4, Mat(["ink"]))
        p.lens((26, 45), (16.5, 40 - st), 5.6, k_down, bend=-1.0)
        p.lens((38, 45), (47.5, 40 - (1 - st)), 5.6, k_down, bend=1.0)
        p.blob(32, 47, 8.4, 7.4, k_down, group=1)
        p.blob(32, 34, 8.4, 7.8, k_down, group=3)
        if view == "down":
            p.poly(bez3((23.5, 36), (22.5, 26), (41.5, 26), (40.5, 36)) +
                   [(38, 33), (35, 31.5), (32, 33), (29, 31.5), (26, 33)], k_hood, group=4)
            p.lens((32, 28), (32, 21.5), 3.2, k_hood, group=4)
            p.poly([(29, 35), (35, 35), (33.5, 40), (32, 41.5), (30.5, 40)], k_beak)
            p.circle(32, 42, 2.2, k_olive)
            p.eye(26, 32, 3, 4, iris="gold1", shine="down3", shine_at=(1, 1))
            p.eye(35, 32, 3, 4, iris="gold1", shine="down3", shine_at=(1, 1))
        else:
            p.poly(bez3((23.5, 38), (22.5, 26), (41.5, 26), (40.5, 38)) +
                   [(38, 43), (35, 40), (32, 44), (29, 40), (26, 43)], k_hood, group=4)
            p.lens((32, 28), (32, 21.5), 3.2, k_hood, group=4)
            p.lens((32, 52), (32 + st, 58), 4.4, k_down)
        return


# --------------------------------------------------------------------------
# Harpelle, the harpy
# --------------------------------------------------------------------------

HARPELLE_COLORS = [
    ("ink", INK),
    # marble-gray feathers, barred in black-figure ink
    ("f0", (80, 80, 96)), ("f1", (128, 128, 144)), ("f2", (184, 184, 192)), ("f3", (232, 232, 224)),
    # the dark hood and beak
    ("hood0", (40, 40, 56)), ("hood1", (72, 72, 96)),
    # sun-gold eyes, cere and scaled feet
    ("gold0", (200, 144, 40)), ("gold1", (248, 208, 72)),
    # Aegean-blue storm wisps
    ("aeg0", (48, 96, 168)), ("aeg1", (112, 160, 216)), ("aeg2", (184, 216, 240)),
    # the stolen terracotta loaf
    ("terra0", (120, 56, 32)), ("terra1", (184, 104, 56)), ("terra2", (232, 160, 96)),
]
HARPELLE_SHINY = {
    # sandy limestone feathers, sun-gold storm wisps
    "f0": (128, 96, 64), "f1": (176, 144, 96), "f2": (208, 184, 136), "f3": (240, 224, 184),
    "aeg0": (184, 120, 32), "aeg1": (232, 176, 56), "aeg2": (248, 224, 136),
}

h_feat = Mat(["f0", "f1", "f2", "f3"], line="f0", cuts=[0.18, 0.44, 0.72])
h_wing = Mat(["hood0", "f0", "f1", "f2"], line="hood0", cuts=[0.2, 0.46, 0.74])
h_hood = Mat(["hood0", "hood1", "f0"], line="hood0", cuts=[0.4, 0.78])
h_gold = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])
h_storm = Mat(["aeg0", "aeg1", "aeg2"], line="aeg0", outline="aeg0", cuts=[0.3, 0.62])
h_loaf = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.62])


def _feather_fan(p, root, tips, w, mat, bias=0.0, group=None, bars=True):
    """Long flight feathers from a common root region out to each tip,
    back ones first (darker), each a lens with a slight bend."""
    pids = []
    for i, (tx, ty, bend) in enumerate(tips):
        rx, ry = root(i) if callable(root) else root
        pids.append(p.lens((rx, ry), (tx, ty), w, mat, bend=bend, fat=0.36, bias=bias, group=group))
    return pids


def _wisp(p, path, w, **kw):
    """A trailing curl of storm cloud along a path, tapering to a point."""
    return p.taper(path, w, h_storm, **kw)


def _cloud(p, x, y, r, tail, **kw):
    """A puff of storm cloud: a few overlapping round lobes at (x, y) and a
    tapering wisp streaming off along `tail` (a path starting at the puff)."""
    p.circle(x, y, r, h_storm, **kw)
    p.circle(x + r * 0.9, y + r * 0.35, r * 0.75, h_storm, **kw)
    p.circle(x - r * 0.7, y + r * 0.45, r * 0.65, h_storm, **kw)
    if tail:
        p.taper(tail, r * 1.1, h_storm, **kw)


def _wing(p, lead, tips, notches, inner, mat, **kw):
    """One wing as a single silhouette: the leading edge `lead` (shoulder to
    wrist), then the primaries as pointed fingers (tips, with notches
    between them), then the `inner` edge back to the body."""
    edge = list(lead)
    for i, t in enumerate(tips):
        edge.append(t)
        if i < len(notches):
            edge.append(notches[i])
    return p.poly(edge + list(inner), mat, **kw)


def _feather_lines(p, roots, tips, color="f0", frac=0.72):
    """Shaft lines down the middle of each flight feather, root to most of
    the way to its tip."""
    for (rx, ry), (tx, ty) in zip(roots, tips):
        p.stroke([(rx, ry), (rx + (tx - rx) * frac, ry + (ty - ry) * frac)], color)


def harpelle(p, view, phase):
    if view in ("front", "side", "icon"):
        F = 1 if (phase == 1 and view == "front") else 0   # wings lift, crest flicks

        # far wing, arched up and back behind the body, its fingered
        # primaries trailing storm cloud
        if p.big:
            _cloud(p, 58.5, 16.5 - F, 2.2, bez((58.5, 16.5 - F), (61.5, 20.5), (60, 25)))
            _cloud(p, 56.5, 30.5 - F, 2.0, bez((56.5, 30.5 - F), (60, 33.5), (58, 38)))
        ftips = [(58.5, 10 - F), (60, 17.5 - F), (58.5, 25 - F), (55.5, 31.5 - F), (50.5, 37)]
        fnot = [(55, 14 - F), (55.5, 21 - F), (53.5, 27 - F), (50, 32)]
        _wing(p, [(36, 31), (37, 21), (43, 12 - F), (50, 7.5 - F), (54, 8.5 - F)], ftips, fnot,
              [(44, 35), (38, 35)], h_feat, bias=0.28, group=30)
        if p.big:
            _feather_lines(p, [(51, 12), (51.5, 17.5), (50, 23), (48, 28), (45, 31.5)], ftips, "f0")

        # tail, a long barred fan low behind
        _wing(p, [(39, 43), (47, 44)], [(56, 48), (55, 52.5), (51, 56)], [(51.5, 49.5), (50, 53)],
              [(42, 51)], h_feat, bias=0.22, group=32)

        # the stolen loaf, round, scored and well browned
        p.blob(28, 57, 10.5, 4.4, h_loaf, group=40)
        # far leg, its foot clamped on the loaf
        p.limb([(36, 47), (36, 52)], 4.4, 3.4, h_gold, bias=0.2, group=41)
        _talon_grip(p, 36, 52, bias=0.2)

        # body: a lean barred breast hunched over the prey
        p.blob(31, 39, 8.4, 10.5, h_feat, ang=22, group=1)
        p.blob(36, 45, 6.8, 5.6, h_feat, group=1)
        p.blob(35.5, 47, 4, 3.6, h_feat, group=2, bias=0.1)

        # near wing, mantled forward and down over the prey like a cloak:
        # the arm arched from the shoulder to the wrist, the primaries
        # hanging in splayed fingers, storm streaming off their tips
        if p.big:
            _cloud(p, 5, 50.5, 2.2, bez((5, 50.5), (2, 54.5), (4.5, 58.5)))
            _cloud(p, 13.5, 56.5, 1.9, bez((13.5, 56.5), (10.5, 59.5), (14.5, 61)))
        ntips = [(4, 48 + F), (8, 53 + F), (13, 55 + F), (18.5, 53), (23.5, 50.5), (28.5, 48.5)]
        nnot = [(7, 44 + F), (11, 48 + F), (16, 49), (21, 47), (25.5, 46)]
        _wing(p, [(35, 31), (28, 27), (17, 26), (10, 28.5 + F), (6.5, 33 + F)], ntips, nnot,
              [(33, 42)], h_feat, group=20)
        if p.big:
            _feather_lines(p, [(8, 37), (11, 40), (15, 42), (19, 42), (23, 42), (27, 42)], ntips, "f0", 0.8)
        # near leg and foot, clutching the loaf
        p.limb([(27, 48), (25, 53)], 4.6, 3.6, h_gold, group=42)
        _talon_grip(p, 25, 53)

        # head low and forward, crest streaming back in the wind
        for a_, b_, w in (((23, 16), (39, 4 - 2 * F), 4.0), ((25, 17), (46, 9 - 2 * F), 4.4),
                          ((26, 19.5), (48, 16 - F), 4.0), ((26, 22), (43, 23 - F), 3.4)):
            p.lens(a_, b_, w, h_hood, bend=-0.9, fat=0.28, group=50)
        head = p.blob(21, 22, 8, 7.4, h_hood, group=3)
        # a pale facial disc framed by the dark hood
        p.blob(18.5, 24.5, 4.6, 4.4, h_feat, clip=[head], group=4)
        # the hooked beak, a gold cere at its base
        p.poly(bez((16, 21), (10, 20.5), (9.5, 27.5)) + [(11, 26.5), (12.5, 25.5), (15.5, 26)], h_hood,
               group=5)
        p.blob(15.5, 21.6, 1.8, 1.5, h_gold, group=6)

        if p.big:
            p.eye(15, 20, 4, 4, iris="gold1", shine="f3", shine_at=(1, 1))
        else:
            p.px(16, 21, "gold1")
        return

    if view == "back":
        # over the shoulder at about 1.2x, the wings flung fully open and the
        # storm streaming off them; the hooded head turned right in profile
        if p.big:
            _cloud(p, 4, 12, 2.2, bez((4, 12), (1.5, 8), (4, 4)))
            _cloud(p, 3.5, 30, 2.0, bez((3.5, 30), (1.5, 34), (4, 37)))
            _cloud(p, 59.5, 4.5, 1.9, bez((59.5, 4.5), (62, 8), (60, 11)))
        # far (right) wing, up behind the head
        rt = [(57, 4), (61, 9.5), (61.5, 17), (60, 24), (56.5, 30)]
        _wing(p, [(40, 44), (44, 28), (49, 15), (53, 7)], rt, [(56.5, 9), (57.5, 14.5), (57, 21), (54.5, 26)],
              [(50, 35), (46, 44)], h_feat, bias=0.28, group=30)
        if p.big:
            _feather_lines(p, [(52, 11), (53.5, 15), (53.5, 20.5), (52.5, 25), (50.5, 29.5)], rt, "f0", 0.75)
        # near (left) wing, flung wide across the frame
        lt = [(3, 8), (2, 17), (3, 25.5), (5.5, 33), (9.5, 40), (15, 45.5)]
        _wing(p, [(30, 47), (22, 32), (14, 18), (7, 8)], lt,
              [(6, 13), (5.5, 21.5), (7, 29), (9.5, 35.5), (13.5, 41)], [(22, 50)], h_feat, group=20)
        if p.big:
            _feather_lines(p, [(9, 13), (8.5, 19.5), (9.5, 26.5), (11.5, 32.5), (14.5, 38), (18, 43)], lt, "f0", 0.75)
        # back and shoulders, cropped by the bottom of the frame
        p.blob(33, 62, 17, 12, h_feat, group=1)
        p.blob(36, 50, 10, 9, h_feat, group=1)
        # head turned right, crest streaming back
        for a_, b_, w in (((40, 22), (24, 12), 4.4), ((39, 25), (23, 21), 4.0), ((42, 20), (31, 7), 4.0)):
            p.lens(a_, b_, w, h_hood, bend=0.8, fat=0.3, group=50)
        head = p.blob(44, 28, 8.4, 8, h_hood, group=3)
        p.blob(48, 31.5, 4.6, 4.4, h_feat, clip=[head], group=4)
        p.poly(bez((50, 27), (57, 26.5), (57.5, 34)) + [(56, 33), (54.5, 31.5), (50.5, 32)], h_hood, group=5)
        p.blob(50.6, 27.6, 1.9, 1.6, h_gold, group=6)
        p.eye(46, 25, 4, 4, iris="gold1", shine="f3", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: the harpy stalking toward (down) or away (up), wings
        # half mantled, crest up, storm curling off the wingtips
        st = phase
        back = view == "up"
        for x, s_ in ((28.5, st), (35.5, 1 - st)):
            p.limb([(x, 50), (x, 57.5 - s_)], 3.4, 3.0, h_gold)
            for dx in (-2.5, 0, 2.5):
                p.limb([(x, 57.5 - s_), (x + dx, 60 - s_)], 1.8, 1.4, Mat(["ink"]))
        # wings: arched from the shoulders, fingered primaries hanging
        lt = [(7, 45 + st), (10, 50 + st), (14, 51), (18, 48)]
        _wing(p, [(27, 31), (18, 27), (10, 29 + st), (6, 36 + st)], lt, [(9, 43 + st), (12, 46), (16, 45)],
              [(25, 44)], h_feat, group=20)
        rt = [(57, 45 + 1 - st), (54, 50 + 1 - st), (50, 51), (46, 48)]
        _wing(p, [(37, 31), (46, 27), (54, 29 + 1 - st), (58, 36 + 1 - st)], rt,
              [(55, 43 + 1 - st), (52, 46), (48, 45)], [(39, 44)], h_feat, group=21)
        if p.big:
            _feather_lines(p, [(10, 38), (13, 40), (16, 41), (19, 41)], lt, "f0", 0.7)
            _feather_lines(p, [(54, 38), (51, 40), (48, 41), (45, 41)], rt, "f0", 0.7)
        if back:
            _wing(p, [(28, 46), (36, 46)], [(37, 56), (32, 58), (27, 56)], [(34, 53), (30, 53)], [], h_feat)
        p.blob(32, 40, 8, 11, h_feat, group=1)
        # crest
        for a_, b_ in (((28.5, 19), (23, 8 + st)), ((32, 18), (32, 6)), ((35.5, 19), (41, 8 + 1 - st))):
            p.lens(a_, b_, 4, h_hood, fat=0.3, group=50)
        p.blob(32, 24.5, 8, 7.4, h_hood, group=3)
        if not back:
            # the face-like disc, two gold eyes, the hooked beak between
            p.blob(32, 27, 5.6, 5, h_feat, group=4)
            p.poly([(30.5, 24), (33.5, 24), (33, 30), (32, 31.5), (31, 30)], h_hood, group=5)
            p.eye(27, 23, 3, 3, iris="gold1", shine="f3", shine_at=(0, 0))
            p.eye(34, 23, 3, 3, iris="gold1", shine="f3", shine_at=(0, 0))
        return


def _talon_grip(p, x, y, bias=0.0):
    """A raptor's foot closed over the loaf: gold toes and ink hooks."""
    for dx, dy in ((-3.5, 1.5), (-1, 2.5), (2.5, 1.8)):
        p.limb([(x, y), (x + dx, y + dy)], 2.2, 1.8, h_gold, bias=bias)
        p.taper(bez((x + dx, y + dy), (x + dx * 1.3, y + dy + 1), (x + dx * 1.1, y + dy + 2.4)), 1.8,
                Mat(["ink"]), bias=bias)


MONS = [
    Mon("Harpeck", HARPECK_COLORS, HARPECK_SHINY, harpeck, foot="bird"),
    Mon("Harpelle", HARPELLE_COLORS, HARPELLE_SHINY, harpelle, foot="bird"),
]
