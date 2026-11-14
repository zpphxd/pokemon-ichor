"""Cerberus line: Kynder, Dikyon, Pylakyon (Fire starter). Kerberos, the hound of Hades' gate."""
from mon_lib import C, Mat, Mon, lerp

INK = C.ink

# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------


def _flame(p, a, b, w, bend=0.0, hot=2, mat=None, **kw):
    """A flame tongue from base a to tip b: a red-edged orange tongue with a
    gold core toward the base (and a pale-yellow heart when hot is 3)."""
    mat = mat or FIRE
    p.lens(a, b, w, mat, bend=bend, fat=0.32, flat=1, **kw)
    kw.pop("group", None)
    kw.pop("under", None)
    m = lerp(a, b, 0.62)
    p.lens(a, m, w * 0.62, mat, bend=bend * 0.6, fat=0.3, flat=2, noline=True, nooutline=True, **kw)
    if hot >= 3 and p.big:
        m = lerp(a, b, 0.32)
        p.lens(a, m, w * 0.34, mat, bend=bend * 0.3, fat=0.3, flat=3, noline=True, nooutline=True, **kw)


FIRE = Mat(["fire0", "fire1", "fire2", "fire3"], line="fire0", outline="fire0")
GHOST = Mat(["blue0", "blue1", "blue2"], line="blue0", outline="blue0")


def _ghostflame(p, a, b, w, bend=0.0, **kw):
    """A sun-gold flame that cools to ghostly Aegean blue toward its tip."""
    m = lerp(a, b, 0.55)
    p.lens(m, b, w * 0.72, GHOST, bend=bend * 0.5, fat=0.25, flat=1, **kw)
    kw.pop("group", None)
    p.lens(lerp(a, b, 0.6), lerp(b, a, 0.12), w * 0.3, GHOST, fat=0.3, flat=2, noline=True, nooutline=True, **kw)
    _flame(p, a, lerp(a, b, 0.68), w, bend=bend * 0.6, hot=3, **kw)


def _head(p, cx, cy, face, mat, pale_mat, s=1.0, ears=True, eye=True, shine="white",
          iris=None, mouth=None, asleep=False, bias=0.0, group=None):
    """A hound's head facing left (face=-1) or right (face=1): cranium,
    pointed ears, a limestone muzzle and, at battle size, its face."""
    if ears:
        for ex, tx, ty in ((-2.6, -4.6, -13.5), (2.4, 1.6, -13)):
            ex, tx = ex * -face, tx * -face
            p.lens((cx + ex * s, cy - 3.5 * s), (cx + tx * s, cy + ty * s), 5 * s, mat,
                   bend=-0.6 * face * s, fat=0.28, bias=bias + 0.1)
    p.blob(cx, cy, 6.6 * s, 6 * s, mat, group=group, bias=bias)
    p.blob(cx + face * 8 * s, cy + 2.6 * s, 5.4 * s, 2.8 * s, pale_mat, ang=6 * face, group=group)
    if mouth:
        p.blob(cx + face * 7 * s, cy + 5.8 * s, 4.2 * s, 1.5 * s, pale_mat, group=group)
    if not p.big:
        if eye:
            p.px(cx + face * 2.5 * s, cy - 1 * s, "ink")
        return
    nx = cx + face * 12.6 * s
    p.pxs([(nx, cy + 1.2 * s), (nx - face, cy + 1.2 * s), (nx, cy + 2.2 * s)], "ink")
    if asleep:
        ex = cx + face * 2 * s
        p.stroke([(ex - 1.5, cy), (ex - 0.5, cy + 1), (ex + 0.5, cy + 1), (ex + 1.5, cy)], "ink")
    elif eye:
        p.eye(cx + face * 2.6 * s - 1, cy - 2 * s, 3, 3, iris=iris, shine=shine)
    if mouth:
        p.stroke([(cx + face * 3 * s, cy + 4 * s), (cx + face * 10.5 * s, cy + 4 * s)], "ink")
        p.stroke([(cx + face * 4 * s, cy + 5 * s), (cx + face * 9.5 * s, cy + 5 * s)], mouth)

# --------------------------------------------------------------------------
# Kynder, the hearth pup
# --------------------------------------------------------------------------

KYNDER_COLORS = [
    ("ink", INK),
    ("coat0", (120, 48, 24)), ("coat1", (184, 88, 48)), ("coat2", (224, 136, 88)), ("coat3", (248, 184, 136)),
    ("pale0", (176, 144, 96)), ("pale1", (208, 184, 136)), ("pale2", (240, 224, 184)),
    ("fire0", (200, 56, 32)), ("fire1", (240, 128, 40)), ("fire2", (248, 192, 64)), ("fire3", (248, 240, 168)),
    ("white", C.white), ("tongue", (232, 104, 120)), ("pink", (248, 176, 168)),
]
KYNDER_SHINY = {
    "coat0": (80, 80, 88), "coat1": (128, 128, 136), "coat2": (176, 176, 176), "coat3": (216, 216, 208),
    "fire0": (40, 72, 160), "fire1": (64, 128, 216), "fire2": (128, 192, 240), "fire3": (216, 240, 248),
}

coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.44, 0.72])
head = Mat(["coat0", "coat1", "coat2", "coat3"], line="ink", cuts=[0.16, 0.44, 0.72])
pale = Mat(["pale0", "pale1", "pale2"], line="pale0", cuts=[0.4, 0.66])
ruff = Mat(["fire1", "fire2", "fire3"], line="fire1", cuts=[0.4, 0.66])


def kynder(p, view, phase):
    if view in ("front", "side"):
        # matches the hand-finished front: a sitting pup, its head up and
        # panting, a gold ruff with a sleeping head on each shoulder
        pant = 1 if (phase == 1 and view == "front") else 0
        step = phase if view == "side" else 0
        for a, b, w in (((36, 34), (38, 12), 7), ((41, 35), (45, 17), 6.5), ((45, 36), (51, 22), 6),
                        ((48, 38), (56, 29), 5)):
            _flame(p, a, b, w, bend=-1.0, hot=3)
        _flame(p, (55, 50), (58, 38 - pant), 6, bend=-0.8, hot=3)
        p.limb([(50, 55), (53.5, 53), (55, 50)], 4.6, 3.8, coat, group=9)
        far = [(34, 44), (34, 52), (34, 56)] if not step else [(34, 44), (36, 52), (37, 56)]
        p.limb(far, 5.4, 5, coat, bias=0.25, group=10)
        p.blob(far[-1][0], 57.8, 4.2, 2, coat, bias=0.25, group=10)
        p.blob(44, 52, 8, 7.5, coat, group=1)
        p.blob(44, 58, 6, 2.4, coat, group=11, bias=0.1)
        p.blob(30, 47, 8, 6, pale, group=2)
        p.blob(30, 39.5, 17, 5.5, ruff, group=5)
        for a, b in (((18, 42), (17, 46)), ((24, 43), (24, 47)), ((30, 43), (31, 47)),
                     ((36, 43), (37, 47)), ((42, 42), (44, 46))):
            p.lens(a, b, 4, ruff, fat=0.3, group=5)
        _head(p, 48, 37, 1, head, pale, s=0.75, asleep=True, ears=False, group=7)
        near = [(22, 44), (22, 52), (21.5, 56)] if not step else [(22, 44), (20, 51), (18.5, 55.5)]
        p.limb(near, 7, 6.6, coat, group=12)
        p.blob(near[-1][0] - 0.5, near[-1][1] + 2, 6.4, 2.8, coat, group=12)
        _head(p, 26, 22 - pant, -1, head, pale, s=1.3, iris="fire2", mouth="tongue")
        _head(p, 12, 40, -1, head, pale, s=0.75, asleep=True, ears=False, group=6)
        return

    if view == "back":
        # over the shoulder: the back and ruff cropped by the frame, the
        # awake head turned right in profile, a sleeping head on each shoulder
        _flame(p, (6, 52), (3.5, 38), 6.5, bend=0.8, hot=3)
        p.limb([(9, 62), (7, 57), (6, 52)], 5.5, 4.5, coat, group=9)
        for a, b, w in (((22, 38), (16, 25), 6.5), ((27, 35), (24, 21), 7), ((47, 34), (52, 22), 6),
                        ((50, 37), (58, 29), 5.5)):
            _flame(p, a, b, w, bend=0.9 if a[0] < 40 else -0.9, hot=3)
        p.blob(26, 61, 23, 13, coat, group=1)
        p.limb([(33, 50), (38, 38), (42, 30)], 13, 11, coat, group=1)
        p.blob(33, 42, 17, 8, ruff, group=5)
        for a, b in (((18, 46), (15, 51)), ((25, 48), (24, 53)), ((32, 49), (32, 54)),
                     ((39, 48), (41, 53)), ((46, 46), (49, 50))):
            p.lens(a, b, 4.4, ruff, fat=0.3, group=5)
        # far ear, head, near ear
        p.lens((46, 15), (49.5, 3.5), 8.5, coat, bend=-1.0, fat=0.32, bias=0.2)
        p.blob(43, 21.5, 9.5, 9, head, group=3)
        p.blob(53.5, 25.5, 5.6, 3.4, pale, ang=-4, group=4)
        p.blob(52.5, 29.6, 4, 1.6, pale, group=4)
        p.lens((38.5, 15), (34.5, 3.5), 8.5, coat, bend=1.0, fat=0.32)
        # sleeping heads on the shoulders
        p.blob(14, 41, 6.2, 5.4, head, group=6)
        p.blob(8, 44, 2.8, 2, pale, group=6)
        p.lens((17, 36.5), (20, 34), 4, coat, bias=0.1)
        p.blob(51.5, 43, 6, 5.2, head, group=7)
        p.blob(57.6, 45.4, 2.8, 2, pale, group=8)
        p.lens((48.5, 38.5), (46, 36), 4, coat, bias=0.15)
        p.eye(46, 17, 4, 6, iris="fire2", shine_at=(1, 1))
        if p.big:
            p.pxs([(59, 23), (59, 24), (60, 24)], "ink")
            p.stroke([(53, 28), (58, 28)], "ink")
            p.stroke([(10, 40), (11, 41), (12, 41), (13, 40)], "ink")
            p.pxs([(5, 43), (5, 44)], "ink")
            p.stroke([(52, 42), (53, 43), (54, 43), (55, 42)], "ink")
            p.pxs([(60, 45), (60, 44)], "ink")
        return

    if view == "icon":
        # party icon: the pup's big head over its burning ruff
        bob = phase
        _flame(p, (45, 38), (49, 26 - bob), 5.4, bend=-1, hot=3)
        p.blob(32, 46, 10, 5, coat, group=1)
        p.blob(25, 50, 4, 2.4, coat, group=12)
        p.blob(38, 50, 4, 2.4, coat, group=13)
        for a, b in (((22, 38), (17, 30)), ((42, 37), (47, 29)), ((37, 36), (39, 27))):
            _flame(p, a, b, 5.5, hot=3)
        p.blob(32, 40, 13, 5.5, ruff, group=5)
        _head(p, 20.5, 41.5, -1, head, pale, s=0.55, asleep=True, ears=False, group=6)
        _head(p, 43.5, 40.5, 1, head, pale, s=0.55, asleep=True, ears=False, group=7)
        _head(p, 31, 27 - bob, -1, head, pale, s=1.35, iris="fire2", mouth="tongue")
        return

    if view == "down":
        # follower walking toward the camera
        step = phase
        p.blob(32, 50, 9.5, 6, coat, group=1)
        p.limb([(27.5, 53), (27.5, 58.5 - 1.5 * step)], 5, 4.6, coat, group=12)
        p.limb([(36.5, 53), (36.5, 58.5 - 1.5 * (1 - step))], 5, 4.6, coat, group=13)
        p.blob(27.5, 59.4 - 1.5 * step, 3.4, 1.9, coat, group=12)
        p.blob(36.5, 59.4 - 1.5 * (1 - step), 3.4, 1.9, coat, group=13)
        for a, b in (((23, 42), (19, 34)), ((41, 42), (45, 34))):
            _flame(p, a, b, 4.4, hot=3)
        p.blob(32, 44, 11.5, 4.6, ruff, group=5)
        _head(p, 22.5, 44, -1, head, pale, s=0.5, asleep=True, ears=False, group=6)
        _head(p, 41.5, 44, 1, head, pale, s=0.5, asleep=True, ears=False, group=7)
        p.lens((26.5, 28), (23.5, 16 + step), 6.4, coat, bend=0.5, fat=0.3)
        p.lens((37.5, 28), (40.5, 16 + step), 6.4, coat, bend=-0.5, fat=0.3)
        if p.big:
            p.lens((27, 27), (24.5, 18 + step), 2.4, Mat(["pink"]), fat=0.3, noline=True, nooutline=True)
            p.lens((37, 27), (39.5, 18 + step), 2.4, Mat(["pink"]), fat=0.3, noline=True, nooutline=True)
        p.blob(32, 33, 7.5, 6.6, head, group=3)
        p.blob(32, 38, 5, 3.4, pale, group=4)
        p.eye(27.5, 30, 2, 3, iris="fire2", shine_at=(1, 0))
        p.eye(34.5, 30, 2, 3, iris="fire2", shine_at=(0, 0))
        p.pxs([(31.5, 35.5), (32.5, 35.5), (32, 36.5)], "ink")
        if p.big:
            p.stroke([(30, 39), (32, 38), (34, 39)], "ink")
            p.pxs([(31.5, 40), (32.5, 40), (32, 41)], "tongue")
        return

    if view == "up":
        # follower walking away: the whole pup from behind
        step = phase
        p.limb([(27.5, 53), (27.5, 58.5 - 1.5 * step)], 5, 4.6, coat, group=12, bias=0.15)
        p.limb([(36.5, 53), (36.5, 58.5 - 1.5 * (1 - step))], 5, 4.6, coat, group=13, bias=0.15)
        p.blob(27.5, 59.4 - 1.5 * step, 3.4, 1.9, coat, group=12, bias=0.15)
        p.blob(36.5, 59.4 - 1.5 * (1 - step), 3.4, 1.9, coat, group=13, bias=0.15)
        p.blob(32, 49, 9.5, 6.5, coat, group=1)
        p.limb([(32, 53), (34, 48), (35, 45)], 3.4, 3, coat, group=9)
        _flame(p, (35, 45), (36.5, 38 + step), 4.6, hot=3)
        for a, b in (((23, 41), (19, 32)), ((41, 41), (45, 32)), ((29, 39), (28, 31)), ((35, 39), (36, 31))):
            _flame(p, a, b, 4.4, hot=3)
        p.blob(32, 42, 11.5, 4.6, ruff, group=5)
        p.blob(22.5, 42, 3.6, 3.2, head, group=6)
        p.blob(41.5, 42, 3.6, 3.2, head, group=7)
        p.lens((26.5, 28), (23.5, 16 + step), 6.4, coat, bend=0.5, fat=0.3)
        p.lens((37.5, 28), (40.5, 16 + step), 6.4, coat, bend=-0.5, fat=0.3)
        p.blob(32, 33, 7.5, 6.6, head, group=3)
        return


# --------------------------------------------------------------------------
# Dikyon, the twin hound (Orthros)
# --------------------------------------------------------------------------

DIKYON_COLORS = [
    ("ink", INK), ("soot", (72, 32, 24)),
    ("coat0", (120, 48, 24)), ("coat1", (176, 80, 40)), ("coat2", (216, 128, 80)), ("coat3", (240, 176, 128)),
    ("pale0", (176, 144, 96)), ("pale1", (208, 184, 136)), ("pale2", (240, 224, 184)),
    ("fire0", (200, 56, 32)), ("fire1", (240, 128, 40)), ("fire2", (248, 192, 64)), ("fire3", (248, 240, 168)),
    ("white", C.white), ("tongue", (232, 104, 120)),
]
DIKYON_SHINY = {
    "soot": (48, 48, 56),
    "coat0": (80, 80, 88), "coat1": (120, 120, 128), "coat2": (168, 168, 168), "coat3": (208, 208, 200),
    "fire0": (40, 72, 160), "fire1": (64, 128, 216), "fire2": (128, 192, 240), "fire3": (216, 240, 248),
}


dcoat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.44, 0.72])
dleg = Mat(["soot", "coat0", "coat1", "coat2"], line="soot", cuts=[0.2, 0.46, 0.72], wy=0.6)
dhead = Mat(["coat0", "coat1", "coat2", "coat3"], line="ink", cuts=[0.16, 0.44, 0.72])
dpale = Mat(["pale0", "pale1", "pale2"], line="pale0", cuts=[0.4, 0.66])


def dikyon(p, view, phase):
    if view in ("front", "side"):
        snap = phase if view == "front" else 0
        walk = phase if view == "side" else 0
        # tail with an ember at the tip
        _flame(p, (57.5, 28), (59, 14 - snap), 6, bend=-1.0, hot=3)
        p.limb([(52, 34), (56, 32), (57.5, 28)], 4.4, 3.4, dcoat, group=9)
        # far legs (darkening toward the paws)
        ff = [(32, 43), (33.5, 51), (35, 57)] if not walk else [(32, 43), (30.5, 51), (29, 57)]
        fh = [(45, 42), (44.5, 51), (42, 57)] if not walk else [(45, 42), (47, 51), (48, 57)]
        for path in (ff, fh):
            p.limb(path, 5.2, 3.8, dleg, bias=0.15, group=10)
            p.blob(path[-1][0] + 0.5, 58.7, 3.5, 1.9, dleg, bias=0.15, group=10)
        # chest, barrel and rump
        p.blob(37.5, 37.5, 14, 6.5, dcoat, group=1)
        p.blob(28.5, 38, 8.5, 8, dcoat, group=1)
        p.blob(48.5, 36.5, 7, 7, dcoat, group=1)
        # near legs
        nf = [(26, 42), (21, 50), (17, 56.5)] if not walk else [(26, 42), (25, 50), (25, 56.5)]
        nh = [(50, 40), (55.5, 49), (53.5, 57)] if not walk else [(50, 40), (50, 49), (47.5, 57)]
        p.limb(nf, 6.4, 4.4, dleg, group=12)
        p.blob(nf[-1][0] - 1, 58.4, 4.2, 2.1, dleg, group=12)
        p.limb(nh, 7, 4.2, dleg, group=13)
        p.blob(nh[-1][0] - 0.5, 58.9, 4, 2, dleg, group=13)
        # the forked neck and the flaming mane
        p.limb([(30, 36), (25.5, 30), (21, 25)], 9, 8, dcoat, group=1)
        p.limb([(33, 35), (35, 27), (36, 18)], 9, 8, dcoat, group=1)
        for a, b, w, bend in (((27, 36), (20, 24), 6.5, 1.2), ((31, 33), (29, 16), 7, 0.6),
                              ((39, 33), (44, 19), 7, -1.0), ((43, 36), (50, 25), 6.5, -1.0)):
            _flame(p, a, b, w, bend=bend, hot=3)
        # the third head, asleep in the mane
        _head(p, 34, 31, -1, dhead, dpale, s=0.62, asleep=True, bias=0.1)
        # one head barks back over the shoulder, one snaps ahead
        _head(p, 38, 14 - snap, 1, dhead, dpale, s=1.0, mouth="tongue", iris="fire2")
        _head(p, 20, 25, -1, dhead, dpale, s=1.0, mouth="tongue", iris="fire2")
        return

    if view == "icon":
        bob = phase
        _flame(p, (47, 38), (52, 27 - bob), 5, bend=-1, hot=3)
        for x in (24, 30, 36, 41):
            p.limb([(x, 44), (x, 53)], 3.6, 3.2, dleg, group=12)
        p.blob(33, 42, 12, 5, dcoat, group=1)
        for a, b, w in (((27, 38), (24, 28), 5.5), ((33, 37), (33, 27), 5.5), ((39, 38), (42, 28), 5.5)):
            _flame(p, a, b, w, hot=3)
        _head(p, 33, 37, -1, dhead, dpale, s=0.55, asleep=True, ears=False)
        _head(p, 42, 27 - bob, 1, dhead, dpale, s=1.0, mouth="tongue", iris="fire2")
        _head(p, 22, 29, -1, dhead, dpale, s=1.0, mouth="tongue", iris="fire2")
        return

    if view == "back":
        _flame(p, (6, 52), (4, 37), 6.5, bend=1.0, hot=3)
        p.blob(27, 68, 25, 19, dcoat, group=1)
        p.blob(35, 52, 19, 14, dcoat, group=1)
        p.limb([(29, 46), (24, 36), (19, 27)], 12, 10, dcoat, group=1)
        p.limb([(37, 46), (42, 35), (45, 25)], 12, 10, dcoat, group=1)
        for a, b, w, bend in (((20, 46), (13, 33), 7, 1.3), ((26, 42), (25, 27), 7.5, 0.8),
                              ((33, 41), (33, 25), 7, 0.0), ((40, 42), (42, 27), 7.5, -0.8),
                              ((46, 46), (54, 34), 7, -1.3)):
            _flame(p, a, b, w, bend=bend, hot=3)
        _head(p, 33, 38, -1, dhead, dpale, s=0.7, asleep=True)
        _head(p, 15, 22, -1, dhead, dpale, s=1.2, mouth="tongue", iris="fire2")
        _head(p, 48, 20, 1, dhead, dpale, s=1.2, mouth="tongue", iris="fire2")
        return

    if view in ("down", "up"):
        step = phase
        back = view == "up"
        p.limb([(27.5, 48), (27.5, 60 - 2 * step)], 4, 3.4, dleg, group=12)
        p.limb([(36.5, 48), (36.5, 60 - 2 * (1 - step))], 4, 3.4, dleg, group=13)
        p.blob(27.5, 60.5 - 2 * step, 2.8, 1.6, dleg, group=12)
        p.blob(36.5, 60.5 - 2 * (1 - step), 2.8, 1.6, dleg, group=13)
        p.blob(32, 45, 9, 7, dcoat, group=1)
        if back:
            p.limb([(32, 48), (34, 42), (35, 37)], 3.4, 3, dcoat, group=9)
            _flame(p, (35, 37), (36, 30 + step), 4.4, hot=3)
        for a, b in (((26, 40), (22, 30)), ((38, 40), (42, 30)), ((32, 38), (32, 28))):
            _flame(p, a, b, 5, hot=3)
        _head(p, 32, 37, -1, dhead, dpale, s=0.55, asleep=True, ears=False)
        for cx, face in ((23, -1), (41, 1)):
            p.lens((cx - 2.4, 25), (cx - 5, 14 + step), 5.4, dcoat, bend=0.4, fat=0.3)
            p.lens((cx + 2.4, 25), (cx + 5, 14 + step), 5.4, dcoat, bend=-0.4, fat=0.3)
            p.blob(cx, 28.5, 6.2, 5.6, dhead, group=3 if face < 0 else 4)
            if not back:
                p.blob(cx, 33.5, 4, 3.6, dpale, group=3 if face < 0 else 4)
                p.eye(cx - 3.5, 26, 2, 3, iris="fire1", shine_at=(0, 0))
                p.eye(cx + 2, 26, 2, 3, iris="fire1", shine_at=(0, 0))
                p.pxs([(cx - 0.5, 31), (cx + 0.5, 31), (cx, 32)], "ink")
                if p.big:
                    p.pxs([(cx - 1, 35), (cx, 35), (cx + 1, 35)], "tongue")
        return


# --------------------------------------------------------------------------
# Pylakyon, the gatehound (Kerberos)
# --------------------------------------------------------------------------

PYLAKYON_COLORS = [
    ("ink", INK), ("soot", (64, 32, 32)),
    ("coat0", (112, 40, 24)), ("coat1", (168, 72, 40)), ("coat2", (208, 120, 72)), ("coat3", (240, 168, 120)),
    ("pale0", (192, 160, 112)), ("pale1", (240, 224, 184)),
    ("fire0", (200, 56, 32)), ("fire1", (240, 128, 40)), ("fire2", (248, 192, 64)), ("fire3", (248, 240, 168)),
    ("blue0", (48, 104, 176)), ("blue1", (112, 168, 224)), ("blue2", (200, 232, 248)),
]
PYLAKYON_SHINY = {
    "soot": (40, 40, 48),
    "coat0": (72, 72, 80), "coat1": (112, 112, 120), "coat2": (160, 160, 160), "coat3": (200, 200, 192),
    "fire0": (24, 56, 120), "fire1": (48, 104, 176), "fire2": (112, 168, 224), "fire3": (176, 216, 240),
    "blue0": (136, 168, 216), "blue1": (192, 216, 240), "blue2": (232, 248, 248),
}


pcoat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.44, 0.72])
pleg = Mat(["ink", "soot", "coat0", "coat1", "coat2"], line="soot", cuts=[0.1, 0.28, 0.5, 0.74], wy=0.7)
phead = Mat(["coat0", "coat1", "coat2", "coat3"], line="ink", cuts=[0.16, 0.44, 0.72])
ppale = Mat(["pale0", "pale1"], line="pale0", cuts=[0.55])
serpent = Mat(["soot", "coat0", "coat1"], line="soot", cuts=[0.4, 0.66])


def pylakyon(p, view, phase):
    if view in ("front", "side"):
        turn = phase if view == "front" else 0
        walk = phase if view == "side" else 0
        # serpent tail curling up behind, its own head hissing
        p.limb([(54, 45), (58.5, 43.5), (60.5, 38), (59.5, 32)], 5.4, 4.2, serpent, group=9)
        p.blob(56.5, 28.5 - turn, 4.4, 3, serpent, group=9)
        if p.big:
            p.pxs([(54, 27 - turn), (55, 27 - turn)], "blue2")
            p.pxs([(51, 30 - turn), (50, 31 - turn), (51, 32 - turn)], "fire0")
        # far legs
        for path in ([(31, 48), (31, 53.5), (31, 57)], [(44, 48), (43.5, 53.5), (43, 57)]):
            if walk:
                path = [path[0], (path[1][0] + 2, path[1][1]), (path[2][0] + 3, path[2][1])]
            p.limb(path, 6.4, 5.6, pleg, bias=0.12, group=10)
            p.blob(path[-1][0], 58.4, 4.2, 2.1, pleg, bias=0.12, group=10)
        # chest, barrel and rump
        p.blob(37, 41, 15, 8.5, pcoat, group=1)
        p.blob(25.5, 42, 9.5, 10, pcoat, group=1)
        p.blob(49, 40, 8.5, 9, pcoat, group=1)
        # near legs, fading to ink at the paws
        for path in ([(23, 47), (21.5, 53.5), (21, 57.5)], [(52, 46), (54, 52.5), (53, 57.5)]):
            if walk:
                path = [path[0], (path[1][0] - 2, path[1][1]), (path[2][0] - 3, path[2][1])]
            p.limb(path, 8, 6.8, pleg, group=12)
            p.blob(path[-1][0] - 0.5, 58.8, 5.2, 2.3, pleg, group=12)
        # three thick necks
        p.limb([(29, 38), (28, 29), (28, 19)], 12, 11, pcoat, group=1)
        p.limb([(24, 40), (18, 34), (14, 30)], 11, 10, pcoat, group=1)
        p.limb([(34, 37), (39, 27), (42, 16)], 11, 10, pcoat, group=1)
        # the mane of rolling fire
        for a, b, w, bend in (((31, 37), (30, 17), 7.5, 1.4), ((36, 37), (39, 18), 7, -1.6),
                              ((41, 38), (48, 20), 8, -2.2), ((46, 39), (54, 26), 7, -1.8),
                              ((50, 40), (58, 33), 6, -1.4), ((24, 39), (15, 29), 6, 1.4)):
            _ghostflame(p, a, b, w, bend=bend)
        # a corona of ghost-fire behind the heads
        for a, b, w in (((24, 20), (18, 6), 6), ((30, 18), (29, 3), 7), ((37, 18), (39, 3), 7), ((44, 20), (50, 6), 6)):
            _ghostflame(p, a, b, w, bend=-0.6)
        # far head snarls outward, near head snarls outward, the middle stares ahead
        _head(p, 49, 20, 1, phead, ppale, s=0.95, mouth="fire0", shine="blue2", iris="blue2", bias=0.1)
        _head(p, 17, 29 - turn, -1, phead, ppale, s=1.15, mouth="fire0", shine="blue2", iris="blue2")
        p.lens((22, 9 + turn), (19, 4 + turn), 5.6, phead, fat=0.3)
        p.lens((40, 9 + turn), (43, 4 + turn), 5.6, phead, fat=0.3)
        p.blob(31, 14 + turn, 11, 9, phead, group=3)
        p.blob(31, 19 + turn, 6, 4.2, ppale, group=3)
        if p.big:
            for ex in (24, 36):
                p.pxs([(ex, 12 + turn), (ex + 1, 12 + turn)], "blue2")
            p.pxs([(30, 16 + turn), (31, 16 + turn), (32, 16 + turn), (31, 17 + turn)], "ink")
            p.stroke([(27, 21 + turn), (35, 21 + turn)], "ink")
        else:
            p.px(31, 16 + turn, "ink")
        return

    if view == "icon":
        bob = phase
        p.limb([(44, 46), (49, 44), (50, 38)], 3.6, 3, serpent, group=9)
        p.blob(49.5, 36 - bob, 3, 2.2, serpent, group=9)
        for x in (24, 30, 36, 42):
            p.limb([(x, 46), (x, 54)], 4.6, 4.2, pleg, group=12)
        p.blob(33, 43, 13, 6, pcoat, group=1)
        for a, b in (((25, 40), (21, 30)), ((33, 39), (33, 28)), ((41, 40), (45, 30))):
            _ghostflame(p, a, b, 6)
        _head(p, 19, 34, -1, phead, ppale, s=0.85, mouth="fire0", shine="blue2", iris="blue2")
        _head(p, 46, 31, 1, phead, ppale, s=0.85, mouth="fire0", shine="blue2", iris="blue2")
        p.lens((29, 22 - bob), (27.5, 15 - bob), 4.8, phead, fat=0.3)
        p.lens((37, 22 - bob), (38.5, 15 - bob), 4.8, phead, fat=0.3)
        p.blob(33, 26 - bob, 7.6, 7, phead, group=3)
        p.blob(32.5, 29.5 - bob, 4, 2.8, ppale, group=3)
        p.pxs([(29, 25 - bob), (35, 25 - bob)], "blue2")
        p.px(32, 28 - bob, "ink")
        return

    if view == "back":
        p.blob(30, 69, 27, 19, pcoat, group=1)
        p.blob(36, 52, 21, 14, pcoat, group=1)
        p.limb([(26, 46), (19, 36), (14, 29)], 13, 11, pcoat, group=1)
        p.limb([(33, 44), (33, 30), (32, 16)], 13, 11, pcoat, group=1)
        p.limb([(42, 46), (48, 36), (51, 28)], 13, 11, pcoat, group=1)
        for a, b, w, bend in (((22, 47), (14, 33), 8, 1.4), ((28, 44), (25, 24), 8.5, 1.0),
                              ((35, 44), (39, 22), 8.5, -1.2), ((41, 47), (50, 34), 8, -1.4),
                              ((30, 50), (31, 36), 7, 0.6)):
            _ghostflame(p, a, b, w, bend=bend)
        p.limb([(14, 62), (8, 57), (6, 49), (8, 43)], 6, 4.6, serpent, group=9)
        p.blob(8, 39, 4.4, 3, serpent, group=9)
        _head(p, 14, 25, -1, phead, ppale, s=1.15, mouth="fire0", shine="blue2", iris="blue2")
        _head(p, 34, 11, 1, phead, ppale, s=1.15, mouth="fire0", shine="blue2", iris="blue2")
        _head(p, 51, 24, 1, phead, ppale, s=1.15, mouth="fire0", shine="blue2", iris="blue2")
        return

    if view in ("down", "up"):
        step = phase
        back = view == "up"
        for x, st in ((25.5, step), (38.5, 1 - step)):
            p.limb([(x, 48), (x, 60 - 2 * st)], 5.6, 5, pleg, group=12)
            p.blob(x, 60.5 - 2 * st, 3.6, 1.8, pleg, group=12)
        p.blob(32, 45, 12, 8, pcoat, group=1)
        if back:
            p.limb([(32, 49), (35, 43), (36, 37)], 4, 3.4, serpent, group=9)
            p.blob(36.5, 35 + step, 3, 2.4, serpent, group=9)
        for a, b in (((22, 40), (17, 29)), ((42, 40), (47, 29)), ((28, 38), (26, 26)), ((36, 38), (38, 26))):
            _ghostflame(p, a, b, 5.5)
        for cx, cy in ((18, 31), (32, 25), (46, 31)):
            p.lens((cx - 2.6, cy - 3), (cx - 5.2, cy - 13 + step), 5.4, pcoat, bend=0.4, fat=0.3)
            p.lens((cx + 2.6, cy - 3), (cx + 5.2, cy - 13 + step), 5.4, pcoat, bend=-0.4, fat=0.3)
            p.blob(cx, cy, 6.2, 5.8, phead, group=3)
            if not back:
                p.blob(cx, cy + 3.8, 4.6, 3.4, ppale, group=3)
                p.pxs([(cx - 3, cy - 1), (cx - 2, cy - 1), (cx + 2, cy - 1), (cx + 3, cy - 1)], "blue2")
                p.pxs([(cx - 1, cy + 2), (cx, cy + 2), (cx + 1, cy + 2), (cx, cy + 3)], "ink")
        return


MONS = [
    Mon("Kynder", KYNDER_COLORS, KYNDER_SHINY, kynder, foot="paw", icon_pal=3),
    Mon("Dikyon", DIKYON_COLORS, DIKYON_SHINY, dikyon, foot="paw", icon_pal=3),
    Mon("Pylakyon", PYLAKYON_COLORS, PYLAKYON_SHINY, pylakyon, foot="bigpaw", icon_pal=3),
]
