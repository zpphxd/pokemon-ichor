"""Minotaur line: Asterlorn (Fighting/Dark). Asterion, the starry one, shut in
Daedalus's Labyrinth for other people's sins."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Asterlorn, the forlorn star-bull
# --------------------------------------------------------------------------

ASTERLORN_COLORS = [
    ("ink", INK),
    # dark limestone-brown hide
    ("hide0", (64, 40, 32)), ("hide1", (112, 72, 48)), ("hide2", (160, 112, 64)), ("hide3", (208, 160, 104)),
    # cypress-dark mane and shag
    ("mane0", (24, 40, 32)), ("mane1", (40, 72, 56)), ("mane2", (72, 104, 80)),
    # marble-white horns
    ("horn0", (144, 136, 120)), ("horn1", (208, 200, 184)), ("horn2", (248, 248, 240)),
    # the bronze shackle and nose ring
    ("gold0", (136, 80, 24)), ("gold1", (200, 144, 40)), ("gold2", (248, 208, 88)),
    # the star spots, for his name Asterion
    ("star", (232, 224, 192)),
]
ASTERLORN_SHINY = {
    # night-blue hide, the stars shining sun-gold
    "hide0": (32, 32, 64), "hide1": (56, 56, 104), "hide2": (88, 88, 144), "hide3": (128, 128, 184),
    "star": (248, 208, 72),
}

a_hide = Mat(["hide0", "hide1", "hide2", "hide3"], line="hide0", cuts=[0.18, 0.44, 0.72])
a_muzz = Mat(["hide1", "hide2", "hide3"], line="hide0", cuts=[0.3, 0.62])
a_mane = Mat(["mane0", "mane1", "mane2"], line="mane0", cuts=[0.36, 0.7])
a_horn = Mat(["horn0", "horn1", "horn2"], line="horn0", cuts=[0.32, 0.64])
a_gold = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.34, 0.68])
a_hoof = Mat(["mane0", "mane1"], line="mane0", cuts=[0.55])


def _horn(p, path, w, **kw):
    """A long bull horn: thick at the root, holding its girth for most of
    its length, then tapering to a point."""
    from mon_lib import ribbon, ellipse_pts
    a = p._minw(w)
    prof = lambda t: max(0.35, a * (1 - t ** 2.4) ** 0.8)
    return p.add(p.mask(ribbon(path, prof), ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12)),
                 a_horn, **kw)


def _shag_pts(cx, cy, rx, ry, a0, a1, n, depth, lean=0.0, seq=(1.0, 0.55, 0.85, 0.4, 0.95, 0.65)):
    """An ellipse whose rim between angles a0 and a1 (degrees, 0 = right,
    90 = down) is broken into n shaggy locks of varying length, each leaning
    by `lean` (degrees). The rest of the rim is smooth."""
    span = (a1 - a0) % 360 or 360
    out = []
    for j in range(n):
        u0, um = a0 + span * j / n, a0 + span * (j + 0.55) / n
        d = depth * seq[j % len(seq)]
        for a, rr in ((u0, 0.0), (um + lean, d)):
            r = math.radians(a)
            out.append((cx + (rx + rr) * math.cos(r), cy + (ry + rr) * math.sin(r)))
    r = math.radians(a0 + span)
    out.append((cx + rx * math.cos(r), cy + ry * math.sin(r)))
    # splice: smooth part runs from a1 back around to a0
    smooth = []
    for i in range(72):
        a = (a0 + span + (360 - span) * i / 71) % 360
        r = math.radians(a)
        smooth.append((cx + rx * math.cos(r), cy + ry * math.sin(r)))
    return out + smooth


def _star(p, x, y, big=False):
    if big:
        p.pxs([(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], "star")
    else:
        p.px(x, y, "star")


def _sub(p, k, cx, cy, dx=0.0, dy=0.0):
    """A pen drawing at k times p's scale about design point (cx, cy),
    moved by (dx, dy): for drawing one part bigger or smaller."""
    from mon_lib import Pen
    return Pen(p.fig, p.s * k, p.ox + p.s * (cx - cx * k + dx), p.oy + p.s * (cy - cy * k + dy), p.view, p.phase)


def _lock(p, root, tip, w, bend=-0.8, **kw):
    """A long tapered lock of mane swept back from its root."""
    return p.lens(root, tip, w, a_mane, bend=bend, fat=0.28, **kw)


def _stand(p, view, phase, chain=True):
    """The battle front: a bull-man on two digitigrade legs in three-quarter
    view facing left, hunched, the great shoulders rolled forward and the
    head lowered so the horns lead. Both arms hang heavy: the near one drags
    the snapped chain from its bronze cuff, the far fist is clenched at the
    hip. The near leg steps forward."""
    F = 1 if (phase == 1 and view == "front") else 0      # frame 2: the head tosses up
    walk = view == "side" and phase == 1
    L = F

    # ---- behind: the far horn, the tail, the far leg, the far arm ----
    _horn(p, bez3((19, 20.5 - L), (12, 18 - L), (6, 12 - L), (7, 3 - L)), 7.2, group=40, bias=0.1)
    tail = bez3((46, 41), (52, 44), (56, 41), (56, 34 - F))
    p.limb(tail, 2.6, 1.8, a_hide, group=8, bias=0.12)
    _lock(p, (56, 36 - F), (54.5, 28 - 2 * F), 4.4, bend=0.6, group=9)
    far = [(41, 43), (38, 48.5), (46, 54), (44, 58.5)] if not walk else [(41, 44), (41, 50), (46, 55), (46, 58.5)]
    p.limb(far[:2], 10, 7.4, a_hide, bias=0.22, group=11)
    p.limb(far[1:3], 5.4, 4.2, a_hide, bias=0.22, group=12)
    p.limb(far[2:], 4.0, 3.6, a_hide, bias=0.22, group=13)
    p.limb([(23, 32), (17, 39.5)], 7.8, 7, a_hide, group=21, bias=0.16)
    p.limb([(17, 39.5), (15.5, 45)], 7, 6.6, a_hide, group=22, bias=0.16)
    p.blob(15.5, 48.5, 5, 4.6, a_hide, group=23, bias=0.12)

    # ---- body: hunched over the hips, the back rising to the hump ----
    p.poly(bez3((24, 29), (19.5, 34), (21, 41), (27, 45.5))
           + bez3((27, 45.5), (31, 47.5), (37, 47.5), (41, 46.5))
           + bez3((41, 46.5), (46, 46), (48.5, 41), (48, 35))
           + bez3((48, 35), (47.5, 27), (45, 19), (40, 14))
           + bez3((40, 14), (35, 10), (28, 12), (25, 18)) + [(24, 29)], a_hide, group=1)
    _hump_locks(p, F, ox=-3, oy=-2)

    # ---- the near leg, stepping forward ----
    near = [(32, 43), (24, 48.5), (30.5, 54), (25.5, 58.5)] if not walk else [(32, 44), (29, 50), (33, 55), (31, 58.5)]
    p.limb(near[:2], 11, 7.8, a_hide, group=15)
    p.limb(near[1:3], 5.8, 4.4, a_hide, group=16)
    p.limb(near[2:], 4.2, 3.8, a_hide, group=17)
    for (hx, hy), bias, w in ((far[-1], 0.22, 3.4), (near[-1], 0.0, 3.8)):
        p.poly(_shag_pts(hx, hy - 0.8, w + 0.6, 2.2, 15, 165, 6, 1.8, lean=6), a_mane, bias=bias)
        p.rect(hx - w, hy + 0.6, hx + w - 0.6, hy + 2.6, a_hoof, bias=bias)
        if p.big:
            p.px(hx, hy + 2, "ink")

    # ---- the snapped chain, trailing from the cuff to the ground behind ----
    links = [(48, 50, 0), (50.5, 53.5, 1), (53, 57, 0), (56.5, 59.6, 1), (60, 60.3, 0)] if chain else []
    for i, (lx, ly, face) in enumerate(links):
        lx -= F * (i + 1) * 0.25
        if face:
            p.blob(lx, ly, 2.2, 1.9, a_gold, group=61 + i)
        else:
            p.blob(lx, ly, 1.4, 2.0, a_gold, group=61 + i)

    # ---- the near arm, hanging heavy: shoulder rolled forward, cuff, fist ----
    p.limb([(39, 29 - F), (43.5, 38)], 9.6, 8.4, a_hide, group=25)
    p.limb([(43.5, 38), (42.5, 46)], 8.4, 7.8, a_hide, group=26)
    p.blob(42.5, 50.5, 6.6, 5.6, a_hide, group=27)
    p.limb([(37.6, 45), (47.4, 46.2)], 4.4, 4.4, a_gold, cap=False, group=60)
    p.blob(36.5, 25 - F, 9, 8.4, a_hide, group=24)

    # ---- the head, lowered, horns leading, the eyes under the brow ----
    _charge_head(_sub(p, 0.86, 14, 36, dx=4, dy=-3), L,
                 near_horn=(p, bez3((29, 18.5 - L), (35, 13 - L), (37.5, 6 - L), (32.5, 2.5 - L))))
    if p.big:
        for x, y, b in ((35, 20, True), (40, 19, False), (42, 24, False), (38, 28, True), (33, 30, False),
                        (45, 29, True), (46, 35, False), (44, 39, False)):
            _star(p, x, y - (F if x < 43 else 0), b)


def _hump_locks(p, F=0, ox=0.0, oy=0.0):
    """The mane: four long locks swept back over the hump from the poll,
    each arching up off the neck and falling to a tapered point, the top
    ones overlapping the ones below. (Upper edge, lower edge, tip.)"""
    locks = [
        # lowest: lying along the back
        (bez3((35, 22), (42, 19.5), (50, 21), (54, 26)), bez3((35, 27), (43, 25), (50, 27), (54, 26)), (57, 32)),
        (bez3((32, 16), (40, 12.5), (49, 14), (54, 19)), bez3((33, 22), (41, 19), (49, 20), (54, 23)), (57, 26.5)),
        (bez3((29, 12), (36, 8), (45, 8.5), (50, 13)), bez3((31, 17), (38, 13.5), (46, 14), (50, 17)), (54, 19.5)),
        # top: rising off the poll
        (bez3((26, 10), (31, 5.5), (39, 5), (44, 8)), bez3((28, 14), (33, 10), (40, 9.5), (44, 11)), (48, 12.5)),
    ]
    for i, (top, bot, tip) in enumerate(locks):
        dy = (F if i >= 2 else 0) - oy
        top = [(x + ox, y - dy) for x, y in top] + [(tip[0] + ox, tip[1] - dy)]
        bot = [(x + ox, y - dy) for x, y in bot]
        p.poly(top + bot[::-1], a_mane, group=31 + i, bias=0.12 - 0.04 * i)


def _charge_head(p, L, near_horn=None):
    """The bowed head of the charging front view: the face turned down and
    left, half-lidded eyes, the ring through the nose, the beard. near_horn
    is (pen, path) to draw the near horn at full size over the head."""
    D = lambda pts: [(x, y - L) for x, y in pts]
    p.lens(*D([(12.5, 22.5), (4, 27)]), 4.4, a_hide, bend=-1.0, group=41, bias=0.1)        # far ear
    p.poly(D(_shag_pts(18, 40.5, 8.4, 2.8, 15, 165, 6, 4.2, lean=12)), a_mane, group=39)   # beard
    head = p.poly(D(bez3((12, 23), (15, 18.5), (24, 18), (27.5, 22))
                    + bez3((27.5, 22), (29.5, 27), (28, 33), (24, 37))
                    + bez3((24, 37), (19, 41), (11, 44.5), (5.5, 42))
                    + bez3((5.5, 42), (2.5, 39.5), (3.5, 34.5), (7, 31.5))
                    + bez3((7, 31.5), (10, 29.5), (10.5, 25.5), (12, 23))), a_hide, group=42)
    p.poly(D(bez3((3.6, 35), (6, 31.5), (13, 32), (15.5, 36))
             + bez3((15.5, 36), (16.5, 40), (12, 44), (7, 43.4))
             + bez3((7, 43.4), (3, 42.5), (2.6, 38.5), (3.6, 35))), a_muzz, clip=[head], group=43, noline=True)
    p.poly(D(_shag_pts(19, 19.5, 6, 2.4, 20, 175, 5, 3.6, lean=20)), a_mane, group=44)    # forelock
    p.lens(*D([(26.5, 23.5), (35, 29)]), 4.8, a_hide, bend=1.2, group=45)                  # near ear
    if near_horn:
        _horn(near_horn[0], near_horn[1], 8.2, group=46)
    else:
        _horn(p, D(bez3((23, 20), (29.5, 15.5), (31.5, 8), (26.5, 3))), 7.6, group=46)
    if p.big:
        p.eye(19, 25 - L, 4, 5, iris="gold0", shine="horn2", shine_at=(1, 1))
        p.eye(11, 27 - L, 2, 4, iris="gold0", shine="horn2", shine_at=(0, 1))
        p.pxs([(5, 37 - L), (6, 38 - L), (11, 38 - L), (12, 39 - L)], "ink")
    else:
        p.px(20, 27 - L, "ink")


def asterlorn(p, view, phase):
    if view == "icon":
        # party icon: the head big and the horns wide, so the face reads at
        # 32 px; the shoulders and fists below, the gold cuff on the left wrist
        b = phase
        _horn(p, bez3((22, 22 - b), (12, 20 - b), (5, 14 - b), (6, 5 - b)), 9, group=40)
        _horn(p, bez3((42, 22 - b), (52, 20 - b), (59, 14 - b), (58, 5 - b)), 9, group=46)
        p.poly(_shag_pts(32, 22 - b, 14, 8, 180, 360, 7, 4), a_mane, group=30)
        p.limb([(26, 50), (24, 61)], 9, 8, a_hide, group=11)
        p.limb([(38, 50), (40, 61)], 9, 8, a_hide, group=15)
        p.blob(32, 46, 17, 10, a_hide, group=1)
        for x in (12, 52):
            p.blob(x, 42, 8.6, 8.6, a_hide, group=20 + (x > 32))
            p.blob(x, 56, 6.4, 5.6, a_hide, group=22 + (x > 32))
        p.limb([(46, 51), (58, 51)], 4.4, 4.4, a_gold, cap=False, group=60)
        p.poly(_shag_pts(32, 38 - b, 13, 10, 20, 160, 9, 3.2), a_mane, group=39)
        p.blob(32, 30 - b, 11, 9, a_hide, group=42, bias=-0.2)
        p.blob(32, 41 - b, 9.4, 6.4, a_muzz, group=43, bias=-0.15)
        p.poly(_shag_pts(32, 22 - b, 8, 3, 10, 170, 5, 4), a_mane, group=44)
        p.eye(24, 29 - b, 3, 4, shine=None)
        p.eye(38, 29 - b, 3, 4, shine=None)
        p.pxs([(28, 42 - b), (36, 42 - b)], "ink")
        p.stroke([(30, 47 - b), (34, 47 - b)], "gold1")
        return
    if view in ("front", "side"):
        _stand(p, view, phase)
        return

    if view == "back":
        # over the shoulder at about 1.2x: the vast starry back under the
        # mane, the head turned right into profile, horns sweeping wide
        _horn(p, bez3((47, 14), (53, 11), (58, 6), (57, 1.5)), 7, group=40, bias=0.16)        # far horn
        p.blob(54, 44, 9, 9.5, a_hide, group=5, bias=0.14)                                    # far shoulder
        p.blob(31, 62, 30, 30, a_hide, group=1)                                               # back
        p.blob(13, 40, 12, 12, a_hide, group=2)                                               # near shoulder
        # the mane: long locks from the poll flowing down the neck and over the
        # hump toward the near shoulder, each overlapping the one below
        locks = [
            (bez3((42, 30), (34, 30), (25, 34), (17, 40)), bez3((42, 36), (34, 37), (25, 40), (19, 43)), (12, 45)),
            (bez3((43, 25), (35, 24), (26, 27), (19, 32)), bez3((43, 31), (35, 31), (27, 34), (21, 38)), (13, 38)),
            (bez3((44, 20), (37, 18), (29, 20), (22, 25)), bez3((44, 26), (37, 25), (30, 27), (24, 31)), (16, 30)),
            (bez3((45, 17), (40, 14), (33, 15), (28, 18)), bez3((45, 22), (40, 20), (34, 21), (30, 24)), (22, 21)),
        ]
        for i, (top, bot, tip) in enumerate(locks):
            p.poly(top + [tip] + bot[::-1], a_mane, group=31 + i, bias=0.1 - 0.03 * i)
        p.limb([(41, 33), (44, 26)], 13, 12, a_hide, group=4)                                  # neck
        p.lens((39.5, 21.5), (29, 31), 7.0, a_hide, bend=1.6, group=41, bias=-0.12)            # drooping ear
        p.poly(_shag_pts(50, 35, 7.2, 3.6, 20, 160, 5, 3.6, lean=-8), a_mane, group=39)        # beard
        p.blob(45, 21.5, 9.8, 9.2, a_hide, group=42)                                          # skull
        p.limb([(48, 24), (54.5, 29)], 13, 11.6, a_hide, group=42)                             # face
        p.blob(50, 30.5, 6.8, 5, a_hide, group=42)                                            # jaw
        p.blob(56, 31, 5.8, 5.4, a_muzz, group=43)                                            # muzzle
        p.poly(_shag_pts(43, 14, 7, 3, 190, 350, 5, 3.6, lean=-8), a_mane, group=44)           # forelock
        _horn(p, bez3((40, 15), (32, 12), (26, 8), (27, 1.5)), 8.2, group=46)                  # near horn
        if p.big:
            p.eye(47, 19, 4, 5, iris="gold0", shine="horn2", shine_at=(1, 1))
            p.pxs([(60, 29), (60, 30)], "ink")
            for x, y, b in ((8, 34, True), (14, 31, False), (16, 38, True), (6, 42, False), (20, 46, False),
                            (25, 52, True), (13, 50, False), (32, 49, False), (38, 55, True), (45, 48, False),
                            (51, 54, True), (55, 41, False), (9, 57, False), (28, 59, False), (44, 60, False)):
                _star(p, x, y, b)
        return

    if view in ("down", "up"):
        # follower: plodding slowly, the head low; the legs step in turn
        st = phase
        for sx, s0 in ((-1, st), (1, 1 - st)):
            X = lambda x: 32 + sx * (x - 32)
            p.limb([(X(27), 46), (X(26.5), 54), (X(26.5), 59 - 2 * s0)], 8.4, 6.6, a_hide, group=10 + (sx > 0))
            p.poly(_shag_pts(X(26.5), 58 - 2 * s0, 3.6, 2, 20, 160, 4, 1.4), a_mane)
            p.rect(X(26.5) - 3.2, 59.5 - 2 * s0, X(26.5) + 2.6, 61.4 - 2 * s0, a_hoof)
        if view == "up":
            # walking away: the tail hanging between the legs, and beyond the
            # hump the back of the head between the great horns
            p.limb(bez((32, 44), (33, 50), (35, 54)), 2.4, 2, a_hide)                         # tail
            p.lens((35, 53), (36, 59), 3.4, a_mane)
            _horn(p, bez3((27, 15), (17, 13), (9, 9), (10, 1.5)), 7.6, group=40)
            _horn(p, bez3((37, 15), (47, 13), (55, 9), (54, 1.5)), 7.6, group=46)
            p.lens((25, 18), (15, 24), 5, a_hide, bend=-1.0, group=41)
            p.lens((39, 18), (49, 24), 5, a_hide, bend=1.0, group=45)
            p.blob(32, 17, 8, 6.4, a_hide, group=42)
        p.poly(bez3((14, 30), (20, 20), (44, 20), (50, 30)) + bez3((50, 30), (48, 42), (40, 48), (32, 48))
               + bez3((32, 48), (24, 48), (16, 42), (14, 30)), a_hide, group=1)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            p.blob(X(15), 30, 6.6, 6.4, a_hide, group=20 + (sx > 0))
            p.limb([(X(13), 33), (X(10), 42), (X(11), 48)], 7.4, 6.6, a_hide, group=22 + (sx > 0))
            p.blob(X(11), 51, 4.8, 4.4, a_hide, group=24 + (sx > 0))
        # the cuff on the left wrist: on the right walking toward us, on the left walking away
        cx = 49 if view == "down" else 7
        p.limb([(cx, 47), (cx + 8, 47)], 3.6, 3.6, a_gold, cap=False)
        if view == "down":
            p.poly(_shag_pts(32, 21, 12, 8, 180, 360, 9, 3.4), a_mane, group=30)
            _horn(p, bez3((26, 15), (17, 13), (10, 9), (11, 2)), 7.0, group=40)
            _horn(p, bez3((38, 15), (47, 13), (54, 9), (53, 2)), 7.0, group=46)
            p.lens((24, 19), (14, 24), 4.6, a_hide, bend=-1.0)
            p.lens((40, 19), (50, 24), 4.6, a_hide, bend=1.0)
            p.blob(32, 20, 8.4, 6.6, a_hide, group=42)
            p.limb([(32, 23), (32, 32)], 13, 10, a_hide, group=42)
            p.blob(32, 35, 6.4, 4, a_muzz, group=43)
            p.poly(_shag_pts(32, 16.5, 7, 3, 10, 170, 6, 3.8), a_mane, group=44)
            p.eye(25, 21, 3, 5, iris="gold0", shine="horn2")
            p.eye(36, 21, 3, 5, iris="gold0", shine="horn2", shine_at=(0, 1))
            if p.big:
                p.pxs([(29, 35), (34, 35)], "ink")
                p.stroke([(30, 37), (30, 39), (33, 39), (33, 37)], "gold1")
        else:
            # the mane: a crest of long locks down the neck and over the hump,
            # the broad starry back left bare either side
            for a, b, w, bend in (((31, 15), (26, 31), 5.4, 1.2), ((33, 15), (38, 31), 5.4, -1.2),
                                  ((32, 15), (32, 35), 6.4, 0.0), ((30, 20), (24, 26), 4.0, 0.8),
                                  ((34, 20), (40, 26), 4.0, -0.8)):
                _lock(p, a, b, w, bend=bend, group=30)
            if p.big:
                for x, y, b in ((18, 31, True), (22, 38, False), (44, 34, True), (47, 29, False), (28, 42, False),
                                (37, 41, False), (14, 36, False), (50, 37, True)):
                    _star(p, x, y, b)
        return


MONS = [
    Mon("Asterlorn", ASTERLORN_COLORS, ASTERLORN_SHINY, asterlorn, foot="hoof"),
]
