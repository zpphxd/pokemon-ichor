"""Karkinos line: Karkipool, Karkitox (Water / Poison). The crab of Lerna.

While Herakles fought the Hydra at Lerna, Hera sent a great crab to bite his
foot; he crushed it, and she set it in the stars as Cancer (Apollodorus
2.5.2). Karkipool is the tide-pool crab that goes for ankles; Karkitox is
the marsh crab with one huge venom claw and Hera's peacock eye on its back.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink


def _leg(p, pts, w0, w1, mat, **kw):
    """A jointed crab leg: segments along pts, each a little narrower."""
    n = len(pts) - 1
    for i in range(n):
        a = w0 + (w1 - w0) * i / max(n, 1)
        b = w0 + (w1 - w0) * (i + 1) / max(n, 1)
        p.limb([pts[i], pts[i + 1]], a, b, mat, **kw)


# --------------------------------------------------------------------------
# Karkipool, the tide-pool crab
# --------------------------------------------------------------------------

KARKIPOOL_COLORS = [
    ("ink", INK),
    ("shell0", (112, 40, 24)), ("shell1", (168, 72, 40)), ("shell2", (216, 120, 72)), ("shell3", (240, 168, 120)),
    ("claw0", (128, 32, 32)), ("claw1", (192, 72, 48)), ("claw2", (232, 128, 88)),
    ("lime0", (168, 136, 88)), ("lime1", (208, 184, 136)), ("lime2", (240, 224, 184)),
    ("white", C.white), ("blue0", (40, 88, 160)), ("blue1", (112, 168, 224)), ("marble0", (160, 152, 144)),
]
KARKIPOOL_SHINY = {
    # a marble-white shell and Aegean-blue claws
    "shell0": (120, 112, 112), "shell1": (176, 168, 160), "shell2": (216, 208, 200), "shell3": (240, 240, 232),
    "claw0": (24, 56, 120), "claw1": (48, 104, 176), "claw2": (112, 168, 224),
}

p_shell = Mat(["shell0", "shell1", "shell2", "shell3"], line="shell0", cuts=[0.18, 0.44, 0.72])
p_claw = Mat(["claw0", "claw1", "claw2"], line="claw0", cuts=[0.34, 0.66])
p_under = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.4, 0.7])
p_tip = Mat(["marble0", "white"], line="marble0", cuts=[0.55])
p_limpet = Mat(["marble0", "lime1", "lime2"], line="lime0", cuts=[0.36, 0.66])


def _pincer(p, base, tip, w, gape, mat, tipmat, flip=False, palm=0.5, **kw):
    """A crab claw from base toward tip: a swollen palm, then the fixed
    finger and the moving finger curving toward each other with a gap of
    `gape` px between their tips. flip mirrors which side the dactyl is on.
    Returns the gap's centre (for venom drips and the like)."""
    bx, by = base
    tx, ty = tip
    dx, dy = tx - bx, ty - by
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    if flip:
        nx, ny = -nx, -ny
    pl = L * palm                              # palm length
    pc = (bx + ux * pl * 0.5, by + uy * pl * 0.5)
    p.blob(pc[0], pc[1], pl * 0.56, w / 2, mat, ang=math.degrees(math.atan2(dy, dx)), **kw)
    pe = (bx + ux * pl, by + uy * pl)          # the palm's distal end
    fl = L - pl                                # finger length
    out = []
    for side, wf in ((1, 0.46), (-1, 0.5)):
        s0 = (pe[0] + nx * side * w * 0.2 - ux * 1.2, pe[1] + ny * side * w * 0.2 - uy * 1.2)
        c = (pe[0] + ux * fl * 0.55 + nx * side * (w * 0.42 + gape * 0.3),
             pe[1] + uy * fl * 0.55 + ny * side * (w * 0.42 + gape * 0.3))
        t = (pe[0] + ux * fl + nx * side * gape * 0.5, pe[1] + uy * fl + ny * side * gape * 0.5)
        path = bez(s0, c, t, n=14)
        p.taper(path, w * wf, mat, **kw)
        out.append(path)
        if p.big and tipmat is not None:
            p.taper(path[9:], w * wf * 0.42, tipmat)
    gx = pe[0] + ux * fl * 0.55
    gy = pe[1] + uy * fl * 0.55
    return (gx, gy)


def _arc(c, r, a0, a1, n=None):
    n = n or max(6, int(abs(a1 - a0) / 10))
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _cclaw(p, c, r, w, open_at, gape, palm, mat, tipmat=None, **kw):
    """A round claw: a thick C around the gap centred at c, opening toward
    angle open_at (degrees, y down) by gape degrees, on a swollen palm."""
    p.blob(*palm, mat, **kw)
    a0 = open_at + gape / 2
    p.limb(_arc(c, r, a0, a0 + 360 - gape), w, w * 0.8, mat, **kw)
    if p.big and tipmat is not None:
        for a in (a0, a0 + 360 - gape):
            x, y = c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a))
            p.circle(x, y, w * 0.3, tipmat)


def lerp2(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def karkipool(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        S = 1 if (view == "side" and phase) else 0
        # far legs (its left side), behind the shell
        for i, (hx, hy) in enumerate(((41, 49), (42.5, 51.5), (42, 54))):
            k = (hx + 5, hy - 2 + i)
            _leg(p, [(hx, hy), k, (k[0] + 2, 60 - S * (i % 2))], 3, 1.6, p_claw, bias=0.22)
        # near legs
        for i, (hx, hy) in enumerate(((26, 50), (25, 52.5), (26, 55))):
            k = (hx - 5, hy - 2 + i)
            _leg(p, [(hx, hy), k, (k[0] - 2, 60 - S * ((i + 1) % 2))], 3.2, 1.7, p_claw, group=10 + i)
        # small claw, raised at the right
        p.limb([(42, 48), (46, 44), (47.5, 40)], 3.4, 3, p_claw, bias=0.12, group=20)
        _cclaw(p, (47, 33.5), 2.6, 2.6, 190, 50, (47.5, 36.5, 4.2, 3.4), p_claw, p_tip, group=21)
        # the shell: wider than tall, a pale limestone underside
        shell = p.blob(33.5, 47.5, 12, 7.4, p_shell, group=1)
        p.blob(33, 53.5, 10.5, 3, p_under, clip=[shell], group=2)
        # a limpet stuck to the back of the shell
        p.poly([(39.5, 42.5), (42.5, 37.5), (46, 43)], p_limpet)
        # eyestalks
        p.limb([(29, 43), (28, 36.5 - F)], 2.4, 2.2, p_claw, group=30)
        p.limb([(35, 42), (35.5, 36 - F)], 2.4, 2.2, p_claw, bias=0.15, group=31)
        p.circle(28, 35 - F, 2.4, p_claw, group=30)
        p.circle(35.5, 34.5 - F, 2.3, p_claw, bias=0.1, group=31)
        # the big right claw, raised and leading
        p.limb([(24, 49), (19.5, 45), (17.5, 40)], 4.4, 3.8, p_claw, group=40)
        _cclaw(p, (15.5, 31.5), 3.6, 3.4, -10, 50, (15.5, 35.5, 5.6, 4.4), p_claw, p_tip, group=41)
        if p.big:
            p.eye(27, 33.5 - F, 2, 3, shine="white")
            p.eye(34.5, 33 - F, 2, 3, shine="white")
        return

    if view == "back":
        # over the shoulder: the shell's back with its limpet, the big claw
        # raised at the right, the small one at the left, the eyestalks
        # turned to the right; cropped by the frame
        for hx, hy, kx, ky, fx, fy in ((10, 56, 4, 53, 3, 63), (50, 54, 57, 50, 59, 63)):
            _leg(p, [(hx, hy), (kx, ky), (fx, fy)], 4.6, 3, p_claw, bias=0.2)
        p.limb([(13, 51), (8, 44), (7.5, 37)], 5, 4.4, p_claw, group=40)
        _pincer(p, (7.5, 38), (6.5, 26), 9, 2.2, p_claw, p_tip, group=41)
        p.limb([(46, 50), (51, 41), (51.5, 33)], 6, 5.2, p_claw, group=20)
        _pincer(p, (51.5, 34), (52, 16), 13, 3, p_claw, p_tip, flip=True, group=21)
        shell = p.blob(30, 60, 24.5, 15.5, p_shell, group=1)
        p.limb([(35, 47), (36.5, 37)], 3.4, 3.2, p_claw, group=30)
        p.circle(37, 35.5, 3, p_claw, group=30)
        p.limb([(41, 48), (43, 39)], 3.2, 3.0, p_claw, bias=0.15, group=31)
        p.circle(43.5, 37.5, 2.8, p_claw, bias=0.1, group=31)
        p.poly([(16, 50), (23, 39), (30.5, 50)], p_limpet)
        if p.big:
            p.eye(37, 34, 2, 3, shine="white", shine_at=(1, 0))
            p.eye(43.5, 36, 2, 3, shine="white", shine_at=(1, 0))
        return

    if view == "down":
        # scuttling toward the camera: shell, both claws up, eyestalks
        s = phase
        for side in (-1, 1):
            for i in range(3):
                hx, hy = 32 + side * (6 + i * 1.5), 51 + i
                lift = 2 if (i + s + (side > 0)) % 2 else 0
                _leg(p, [(hx, hy), (hx + side * 5, hy - 2), (hx + side * 7, 60 - lift)], 3.2, 2.0, p_claw)
        shell = p.blob(32, 49, 11, 6.5, p_shell, group=1)
        p.blob(32, 54, 9, 2.4, p_under, clip=[shell], group=2)
        p.limb([(23, 47), (18, 42), (18, 38)], 3.6, 3, p_claw, group=40)
        _cclaw(p, (17.5, 31.5), 3.6, 3.4, -10, 50, (17.5, 35.5, 5.6, 4.4), p_claw, p_tip, group=41)
        p.limb([(41, 47), (46, 43), (46, 39)], 3.2, 2.8, p_claw, group=20)
        _cclaw(p, (46, 33), 2.6, 2.6, 190, 50, (46.5, 36, 4.2, 3.4), p_claw, p_tip, group=21)
        for x in (28.5, 35.5):
            p.limb([(x, 44), (x, 38)], 2.4, 2.2, p_claw, group=30)
            p.circle(x, 37, 2.2, p_claw, group=30)
        p.eye(27.5, 36, 2, 3, shine="white")
        p.eye(34.5, 36, 2, 3, shine="white")
        return

    if view == "up":
        # scuttling away: the shell's back and its limpet, claws up at the sides
        s = phase
        for side in (-1, 1):
            for i in range(3):
                hx, hy = 32 + side * (6 + i * 1.5), 52 + i
                lift = 2 if (i + s + (side > 0)) % 2 else 0
                _leg(p, [(hx, hy), (hx + side * 5, hy - 2), (hx + side * 7, 60 - lift)], 3.2, 2.0, p_claw)
        p.limb([(23, 47), (18, 42), (18, 38)], 3.6, 3, p_claw, group=40)
        _cclaw(p, (17.5, 31.5), 3.6, 3.4, -10, 50, (17.5, 35.5, 5.6, 4.4), p_claw, p_tip, group=41)
        p.limb([(41, 47), (46, 43), (46, 39)], 3.2, 2.8, p_claw, group=20)
        _cclaw(p, (46, 33), 2.6, 2.6, 190, 50, (46.5, 36, 4.2, 3.4), p_claw, p_tip, group=21)
        for x in (28.5, 35.5):
            p.limb([(x, 44), (x, 39)], 2.4, 2.2, p_claw, group=30)
            p.circle(x, 38, 2.2, p_claw, group=30)
        p.blob(32, 49, 11, 7, p_shell, group=1)
        p.poly([(33, 47), (36, 42), (39.5, 47)], p_limpet)
        return


# --------------------------------------------------------------------------
# Karkitox, the venom crab of Lerna
# --------------------------------------------------------------------------

KARKITOX_COLORS = [
    ("ink", INK),
    ("cyp0", (16, 40, 32)), ("cyp1", (32, 72, 48)), ("cyp2", (56, 112, 64)), ("cyp3", (112, 160, 96)),
    ("terra0", (112, 40, 24)), ("terra1", (176, 80, 40)), ("terra2", (224, 136, 88)),
    ("moss", (128, 144, 56)), ("reed", (208, 184, 136)),
    ("venom0", (104, 48, 136)), ("venom1", (192, 128, 224)),
    ("gold", C.sungold[1]), ("blue", (48, 104, 176)), ("white", C.white),
]
KARKITOX_SHINY = {
    # starlight sun-gold shell, an Aegean-blue eyespot
    "cyp0": (120, 72, 16), "cyp1": (184, 128, 32), "cyp2": (232, 184, 64), "cyp3": (248, 232, 152),
    "gold": (112, 168, 224), "blue": (24, 56, 120),
}

x_shell = Mat(["cyp0", "cyp1", "cyp2", "cyp3"], line="cyp0", cuts=[0.18, 0.44, 0.72])
x_claw = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.32, 0.64])
x_under = Mat(["terra0", "terra1", "reed"], line="terra0", cuts=[0.4, 0.7])
x_tip = Mat(["reed", "white"], line="terra0", cuts=[0.55])
x_venom = Mat(["venom0", "venom1"], line="venom0", cuts=[0.55])
x_moss = Mat(["cyp1", "moss"], line="cyp0", cuts=[0.5])


def karkitox(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0
        S = 1 if (view == "side" and phase) else 0
        # right legs (its left side), splayed wide behind the shell
        for i, (hx, hy, kx, ky, fx) in enumerate(((54, 39, 59, 35, 62), (55, 43, 61, 43, 62),
                                                  (54, 47, 59, 49, 60.5), (50, 50, 55, 54, 56.5))):
            _leg(p, [(hx, hy), (kx, ky), (fx, 60 - S * (i % 2))], 4.2 - i * 0.2, 1.6, x_claw, bias=0.22 + 0.05 * i)
        # left legs, under the great claw
        for i, (hx, hy, kx, ky, fx) in enumerate(((25, 46, 15, 46, 8.5), (26, 49, 18, 52, 12.5), (29, 51, 23, 55, 18.5))):
            _leg(p, [(hx, hy), (kx, ky), (fx, 60 - S * ((i + 1) % 2))], 4.2 - i * 0.2, 1.6, x_claw,
                 bias=0.1 * i, group=12 + i)
        # the underside, below the front margin
        p.blob(38.5, 50, 13, 4.6, x_under, group=3)
        # the carapace: broad and armored; a terracotta rim curves round the
        # cypress-dark top
        shell = p.blob(40, 37.5, 20.5, 11.4, x_claw, group=2)
        p.blob(40.5, 35.6, 19.6, 10, x_shell, clip=[shell], group=1)
        # the small claw, tucked under the front at its left
        p.limb([(50, 46), (51, 51)], 4.4, 4, x_claw, group=25)
        _pincer(p, (51, 52.5), (40, 55.5 - F * 0.5), 8, 1.2, x_claw, x_tip, flip=True, group=26)
        # eyestalks on the front margin
        p.limb([(32, 35), (30.5, 26 - F)], 3.2, 2.8, x_claw, group=30)
        p.limb([(38.5, 34), (39, 25 - F)], 3.2, 2.8, x_claw, bias=0.12, group=31)
        p.circle(30.5, 24.5 - F, 3, x_claw, group=30)
        p.circle(39, 24 - F, 2.9, x_claw, bias=0.1, group=31)
        # the great venom claw, raised high and thrust forward: a swollen
        # palm, the fixed finger below, the hooked dactyl above, agape
        p.limb([(25, 44), (18.5, 40), (18.5, 34)], 10, 9, x_claw, group=40)
        _cclaw(p, (11, 11 - F), 7.2, 6.2, 185, 34 + 12 * F, (19, 23, 9.6, 10.4), x_claw, x_tip, group=41)
        if p.big:
            p.eye(29, 22.5 - F, 3, 4, shine="white")
            p.eye(37.5, 22 - F, 3, 4, shine="white")
        else:
            p.pxs([(30, 24), (39, 23)], "ink")
        return

    if view == "back":
        # over the shoulder: the great armored back with Hera's eye centered
        # on it, the venom claw raised high at the right, the small claw at
        # the left, the eyestalks turned to the right; cropped by the frame
        for hx, hy, kx, ky, fx, fy in ((10, 54, 5, 50, 4, 63), (13, 58, 7.5, 57, 6.5, 64), (52, 52, 58.5, 48, 60.5, 63)):
            _leg(p, [(hx, hy), (kx, ky), (fx, fy)], 5.6, 3.4, x_claw, bias=0.2)
        p.limb([(13, 47), (7, 41), (7, 35)], 6.4, 5.6, x_claw, group=25)
        _pincer(p, (7, 36), (5, 23), 10.5, 2.4, x_claw, x_tip, group=26)
        # the great claw (groups 40+; the battle back's claw is the front's
        # hand-finished claw, mirrored)
        p.limb([(49, 46), (47, 38), (44, 31)], 11, 10, x_claw, group=40)
        p.taper(bez((49, 12), (56, 3), (60, 8), n=16), 6.4, x_claw, group=42)               # dactyl
        p.taper(bez((54, 22), (62, 19), (58.5, 13), n=16), 6.8, x_claw, group=41)          # fixed finger
        p.blob(47, 19.5, 10, 11.6, x_claw, ang=38, group=41)                              # palm
        shell = p.blob(29, 58, 28, 20, x_claw, group=2)
        p.blob(29.5, 60, 26, 18, x_shell, clip=[shell], group=1)
        p.limb([(28, 42), (28.5, 33)], 4.4, 4, x_claw, group=30)
        p.circle(29, 31.5, 3.6, x_claw, group=30)
        p.limb([(35, 42), (37, 35)], 4, 3.6, x_claw, bias=0.15, group=31)
        p.circle(37.5, 33.5, 3.4, x_claw, bias=0.1, group=31)
        if p.big:
            p.eye(29.5, 29.5, 3, 4, shine="white", shine_at=(2, 1))
            p.eye(38, 31.5, 3, 4, shine="white", shine_at=(2, 1))
        return

    if view == "down":
        s = phase
        for side in (-1, 1):
            for i in range(3):
                hx, hy = 32 + side * (8 + i * 2), 50 + i
                lift = 2 if (i + s + (side > 0)) % 2 else 0
                _leg(p, [(hx, hy), (hx + side * 6, hy - 3), (hx + side * 9, 60 - lift)], 4, 2.4, x_claw)
        shell = p.blob(32, 47, 14, 8, x_shell, group=1)
        p.blob(32, 53, 12, 3, x_under, clip=[shell], group=2)
        p.limb([(22, 46), (15, 40), (14, 34)], 6, 5, x_claw, group=40)
        _cclaw(p, (11, 18), 6, 5.4, 185, 40, (16, 27, 7.6, 8.4), x_claw, x_tip, group=41)
        p.limb([(42, 50), (46, 54)], 3.6, 3.2, x_claw, group=25)
        for x in (28, 36):
            p.limb([(x, 41), (x, 35)], 2.6, 2.4, x_claw, group=30)
            p.circle(x, 34, 2.4, x_claw, group=30)
        p.eye(27, 33, 2, 3, shine="white")
        p.eye(35, 33, 2, 3, shine="white")
        return

    if view == "up":
        s = phase
        for side in (-1, 1):
            for i in range(3):
                hx, hy = 32 + side * (8 + i * 2), 50 + i
                lift = 2 if (i + s + (side > 0)) % 2 else 0
                _leg(p, [(hx, hy), (hx + side * 6, hy - 3), (hx + side * 9, 60 - lift)], 4, 2.4, x_claw)
        p.limb([(42, 46), (49, 40), (50, 34)], 6, 5, x_claw, group=40)
        _cclaw(p, (53, 18), 6, 5.4, -5, 40, (48, 27, 7.6, 8.4), x_claw, x_tip, group=41)
        for x in (28, 36):
            p.limb([(x, 41), (x, 36)], 2.6, 2.4, x_claw, group=30)
            p.circle(x, 35, 2.4, x_claw, group=30)
        p.blob(32, 47, 14, 8.6, x_shell, group=1)
        p.blob(32, 45, 4.4, 3, Mat(["gold"]), flat=0)
        p.blob(32, 45, 3, 2, Mat(["blue"]), flat=0)
        return


MONS = [
    Mon("Karkipool", KARKIPOOL_COLORS, KARKIPOOL_SHINY, karkipool, foot="claw"),
    Mon("Karkitox", KARKITOX_COLORS, KARKITOX_SHINY, karkitox, foot="claw"),
]
