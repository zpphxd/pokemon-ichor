"""Python line: Pelython, Pythoros (Dragon, then Dragon / Ground).

When the flood drew back, the sun-warmed mud bred Python, the serpent that
guarded Gaia's oracle on Parnassus until Apollo shot it with a thousand
arrows (Ovid, Metamorphoses 1; Homeric Hymn to Apollo). Both stages carry
the knotted net carved on Delphoi's Omphalos down their backs. Pelython is
the hatchling, still threaded through the laurel root it hatched under;
Pythoros is the serpent grown vast, its coils stacked like the terraces of
Parnassus, a broken golden arrow lodged in an old pale scar.
"""
import math

from mon_lib import Mat, Mon, bez, bez3, lens_pts

INK = (32, 24, 24)


def arc(c, rx, ry, a0, a1, n=None):
    """Points on an ellipse around c from angle a0 to a1 (degrees, y down)."""
    n = n or max(6, int(abs(a1 - a0) / 9))
    return [(c[0] + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _shift(path, d, light=(-0.6, -0.8)):
    """The path moved d design px sideways, toward the light when d > 0."""
    out = []
    n = len(path)
    for i, (x, y) in enumerate(path):
        a, b = path[max(i - 1, 0)], path[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        if nx * light[0] + ny * light[1] < 0:
            nx, ny = -nx, -ny
        out.append((x + nx * d, y + ny * d))
    return out


def tube(p, path, w0, w1, mat, group, bands=((0.3, 0.26, 3), (-0.34, 0.3, 1)), base=2, **kw):
    """A body segment shaded in clean bands like hand-drawn Gen 3 scales: a
    midtone body, then for each (offset, width, level) a band along the
    path, offset toward the light (+) or away (-) as a fraction of the
    width. At icon size the bands are skipped."""
    pid = p.limb(path, w0, w1, mat, group=group, flat=base, **kw)
    if not pid or not p.big:
        return [pid]
    w = (w0 + w1) / 2
    pids = [pid]
    for off, bw, lvl in bands:
        pids.append(p.limb(_shift(path, off * w), max(1.0, bw * w), max(1.0, bw * w), mat, clip=[pid], flat=lvl,
                           noline=True, group=group))
    return pids


# --------------------------------------------------------------------------
# Pelython, the mud hatchling
# --------------------------------------------------------------------------

PELYTHON_COLORS = [
    ("ink", INK),
    # a dark mud-brown saddle over warm terracotta flanks, with a wet sheen
    ("mud0", (72, 32, 24)), ("mud1", (120, 64, 40)), ("mud2", (192, 104, 56)), ("mud3", (232, 152, 88)),
    ("sheen", (248, 232, 192)),
    # limestone belly, and the Omphalos net
    ("lime0", (168, 136, 96)), ("lime1", (208, 184, 136)), ("lime2", (240, 224, 184)),
    # heavy-lidded sun-gold eyes
    ("gold0", (216, 104, 24)), ("gold1", (248, 184, 56)),
    # the olive laurel root it hatched under
    ("root0", (48, 56, 32)), ("root1", (88, 104, 48)), ("root2", (144, 160, 72)),
    ("tongue", (192, 56, 64)),
]
PELYTHON_SHINY = {
    # olive-green scales with a marble belly
    "mud0": (40, 64, 32), "mud1": (80, 104, 48), "mud2": (128, 152, 64), "mud3": (176, 192, 104),
    "sheen": (240, 248, 216),
    "lime0": (160, 160, 152), "lime1": (208, 208, 200), "lime2": (240, 240, 232),
    # the root darkens to bark so it still parts from the green scales
    "root0": (64, 40, 32), "root1": (112, 72, 48), "root2": (160, 112, 72),
}

p_mud = Mat(["mud0", "mud1", "mud2", "mud3"], line="mud0", cuts=[0.2, 0.46, 0.72])
p_belly = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.36, 0.66])
p_root = Mat(["root0", "root1", "root2"], line="root0", cuts=[0.34, 0.66])
p_leaf = Mat(["root0", "root1", "root2"], line="root0", cuts=[0.3, 0.6])
p_tongue = Mat(["tongue"])
p_smear = Mat(["mud0", "mud1"], cuts=[0.5])


def _pleaf(p, a, b, w, **kw):
    pid = p.lens(a, b, w, p_leaf, **kw)
    if p.big:
        p.stroke([a, ((a[0] * 2 + b[0]) / 3, (a[1] * 2 + b[1]) / 3)], "root0")
    return pid


def _tongue(p, x, y, flick=0, right=False):
    """A forked tongue from the mouth at (x, y), pointing left (or right)."""
    s = 1 if right else -1
    p.stroke([(x, y), (x + 3 * s, y + flick)], "tongue")
    p.stroke([(x + 3 * s, y + flick), (x + 5 * s, y - 1 + flick)], "tongue")
    p.stroke([(x + 3 * s, y + flick), (x + 5 * s, y + 1 + flick)], "tongue")


P_BANDS = ((0.3, 0.3, 3), (-0.3, 0.28, 1), (-0.46, 0.1, 0))
PE_NECK_B = bez((42, 52), (46.5, 43), (41.5, 33))
PE_C1, PE_R1 = (34, 53), (10.5, 3.8)
PE_C2, PE_R2 = (34.5, 46.4), (8, 3.0)
PE_H, PE_HR = (48.5, 48.5), (5.6, 8)


def pelython(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0      # frame 2: head up, tongue out
        S = phase if view == "side" else 0       # slither: coils shift
        (C1, (RX1, RY1)), (C2, (RX2, RY2)), (H, (HX, HY)) = (PE_C1, PE_R1), (PE_C2, PE_R2), (PE_H, PE_HR)
        if view == "side":
            # the short smear of mud it leaves behind as it slithers
            p.blob(54 + 2 * S, 59.6, 7, 1.4, p_smear, group=40)

        # the laurel-root hoop the tail threads through: far half first
        p.limb(arc(H, HX, HY, 95, 265), 3.6, 3.6, p_root, bias=0.3, group=30)
        # the bottom loop's far half and the tail running out through the hoop
        tube(p, arc(C1, RX1, RY1, 185, 360), 8.4, 8.4, p_mud, 2, P_BANDS, bias=0.1)
        tail = bez3((C1[0] + RX1 - 1, C1[1] - 0.5), (C1[0] + RX1 + 6, C1[1] - 1.5), (53 - S, 51), (57 - S, 47 - S), n=12)
        tube(p, tail, 7.0, 3.0, p_mud, 3, P_BANDS)
        tube(p, bez((57 - S, 47.5 - S), (58.5 - S, 42.5 - S), (55.5 - S, 41.5 - S)), 3.0, 1.4, p_mud, 3, P_BANDS)
        # the hoop's near half, over the tail, sprouting laurel leaves
        p.limb(arc(H, HX, HY, 265, 455), 3.8, 3.8, p_root, group=31)
        _pleaf(p, (47.5, 41), (43.5 + F * 0.5, 34.5), 4.6, bend=0.9)
        _pleaf(p, (50, 41), (55.5, 36 - F * 0.5), 4.6, bend=-0.9)
        # the top loop's far half, the bottom loop's near half, the top loop's near half
        tube(p, arc(C2, RX2, RY2, 180, 360), 8, 8, p_mud, 7, P_BANDS, bias=0.06)
        coil = tube(p, arc(C1, RX1, RY1, 0, 180), 9, 9, p_mud, 1, P_BANDS)
        p.limb(arc(C1, RX1 - 0.5, RY1 + 3.4, 40, 140), 1.6, 1.6, p_belly, clip=coil, group=4)
        top = tube(p, arc(C2, RX2, RY2, 0, 180), 8.6, 8.6, p_mud, 8, P_BANDS)
        p.limb(arc(C2, RX2 - 0.5, RY2 + 3.2, 45, 135), 1.4, 1.4, p_belly, clip=top, group=9)
        # neck rising from the top loop's left side to the raised head
        npath = bez((28, 48), (23.5, 44.5), (23.5, 37 - F))
        neck = tube(p, npath, 10.4, 10, p_mud, 10, P_BANDS)
        p.limb(_shift(npath, 3.6, light=(-1, 0.2)), 3.2, 3.2, p_belly, clip=neck, group=11)
        # the head: a big round skull and a short, rounded snout
        hy = 31 - F
        p.blob(23, hy, 8.8, 7.8, p_mud, group=12)
        p.blob(15.5, hy + 2.4, 5.4, 4.8, p_mud, ang=8, group=12)
        p.blob(17.5, hy + 6.2, 6.4, 1.8, p_belly, ang=4, group=13)
        if p.big:
            _tongue(p, 10, hy + 5, flick=F, right=False)
            # heavy-lidded sun-gold eye
            p.patch(17, int(hy) - 3, [".11111.", "1222221", "1c1111c", "1ce11d1", ".1ddd1."],
                    {"1": "ink", "2": "mud1", "c": "gold0", "d": "gold1", "e": "sheen"})
            p.pxs([(11, hy + 1), (12, hy + 1)], "mud0")     # nostril
            p.stroke([(11, hy + 4.5), (18, hy + 5)], "mud0")  # mouth line
        else:
            p.px(19.5, hy - 0.5, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the coils' netted backs filling the
        # bottom of the frame, the neck rising at the right, the head turned
        # right in profile (the art file mirrors the front's head); the root
        # hoop on the tail at the left
        H, (HX, HY) = (12.5, 42), (6.4, 9.6)
        p.limb(arc(H, HX, HY, -85, 85), 4.2, 4.2, p_root, bias=0.3, group=30)
        tail = bez3((24, 52), (15, 50), (9, 47), (4.5, 40), n=12)
        tube(p, tail, 9, 3.6, p_mud, 3, P_BANDS)
        tube(p, bez((4.5, 40.5), (3, 35), (6.5, 33.5)), 3.6, 1.8, p_mud, 3, P_BANDS)
        p.limb(arc(H, HX, HY, 95, 265), 4.4, 4.4, p_root, group=31)
        _pleaf(p, (9, 33), (4, 26), 5.4, bend=1.0)
        _pleaf(p, (14, 32.5), (19, 25.5), 5.4, bend=-1.0)
        # the coils, cropped by the frame: the big near loop, the top loop on it
        tube(p, arc((32, 60), 22.5, 8.5, 185, 355), 13, 13, p_mud, 2, P_BANDS, bias=0.04)
        tube(p, arc((33, 50), 14, 6.4, 185, 355), 11, 11, p_mud, 7, P_BANDS)
        npath = PE_NECK_B
        neck = tube(p, npath, 12.4, 11.4, p_mud, 10, P_BANDS)
        p.limb(_shift(npath, 4.2, light=(1, 0.2)), 3.6, 3.4, p_belly, clip=neck, group=11)
        tube(p, arc((33, 50), 14, 6.4, -5, 185), 11.6, 11.6, p_mud, 8, P_BANDS)
        tube(p, arc((32, 60), 22.5, 8.5, -5, 185), 14, 14, p_mud, 1, P_BANDS)
        # head (the art file mirrors the front's hand-painted head)
        p.blob(42.5, 26, 10.2, 9, p_mud, group=12)
        p.blob(51.5, 29, 6.6, 5.6, p_mud, ang=-8, group=12)
        if p.big:
            p.eye(44, 23, 4, 4, iris="gold1", shine="sheen", shine_at=(2, 1))
        return

    if view in ("down", "up"):
        # follower, drawn the way the HGSS serpent followers are: a big round
        # head on top, the body curling down into a loop that trails to one
        # side, the tail through its root hoop on the other; walking away,
        # it leaves a short smear of mud behind it
        down = view == "down"
        sw = phase
        sg = 1 if down else -1
        if not down:
            p.blob(32 + sg * 2, 61, 8, 1.6, p_smear, group=40)
            p.blob(25 - sw * 2, 61.5, 3, 1, p_smear, group=40)
        C = (32 - 3 * sg, 52)
        tube(p, arc(C, 13, 4.6, 185, 355), 9, 9, p_mud, 2, P_BANDS, bias=0.06)
        tx = C[0] + 13 * sg
        tube(p, bez((C[0] + 7 * sg, 56), (tx + 5 * sg, 56), (tx + 7 * sg, 47 - sw)), 7, 3, p_mud, 5, P_BANDS)
        tube(p, bez((tx + 7 * sg, 47.5 - sw), (tx + 7.5 * sg, 43 - sw), (tx + 4.5 * sg, 43 - sw)), 3, 1.4, p_mud, 5, P_BANDS)
        H = (tx + 6 * sg, 53.5 - sw * 0.5)
        p.limb(arc(H, 3.2, 5, 0, 360, n=28), 3, 3, p_root, group=31)
        _pleaf(p, (H[0], H[1] - 5), (H[0] + 3 * sg, H[1] - 10), 4, bend=-0.8 * sg)
        npath = bez((C[0] - 9 * sg, 52), (32 - 13 * sg, 42), (32, 34))
        neck = tube(p, npath, 12, 12, p_mud, 10, P_BANDS)
        if down:
            p.limb(_shift(npath, 3, light=(-0.6 * sg, -0.3)), 5, 5, p_belly, clip=neck, group=11)
        low = tube(p, arc(C, 13, 4.6, -5, 185), 9.6, 9.6, p_mud, 3, P_BANDS)
        if down:
            p.limb(arc(C, 12.5, 8, 40, 140), 1.6, 1.6, p_belly, clip=low, group=4)
        hx, hy = 32 + (sw if down else -sw), 26
        p.blob(hx, hy, 13, 9.6, p_mud, group=12)
        if down:
            p.blob(hx, hy + 5.6, 8.6, 4.8, p_mud, group=12)
            p.blob(hx, hy + 9.4, 6.4, 1.6, p_belly, group=13)
            for ex, shine in ((hx - 10, 3), (hx + 5, 1)):
                p.patch(ex, hy - 2, ["11111", "1bb21", ".1dd1", "..11."], {"1": "ink", "b": "gold1", "d": "gold0", "2": "sheen"},
                        small=(ex + 2, hy - 1, ["1"]))
            p.pxs([(hx - 2, hy + 5), (hx + 1, hy + 5)], "mud0")
            p.stroke([(hx - 0.5, hy + 11), (hx - 0.5, hy + 13 + sw)], "tongue")
        elif p.big:
            for x, y in ((hx - 4, hy - 4), (hx + 4, hy - 4), (hx, hy), (hx - 4, hy + 4), (hx + 4, hy + 4)):
                p.px(x, y, "lime2")
        return


# --------------------------------------------------------------------------
# Pythoros, the serpent of Parnassus
# --------------------------------------------------------------------------

PYTHOROS_COLORS = [
    ("ink", INK),
    # terracotta scales, five tones for the grown serpent's heavier modeling
    ("ter0", (80, 32, 24)), ("ter1", (128, 56, 32)), ("ter2", (176, 88, 48)), ("ter3", (216, 128, 80)),
    ("ter4", (240, 176, 120)),
    # limestone belly plates and the pale scar; lime2 also lights fangs and eyes
    ("lime0", (160, 128, 88)), ("lime1", (208, 184, 136)), ("lime2", (240, 232, 200)),
    # olive moss and laurel in the folds of the coils
    ("moss0", (48, 64, 32)), ("moss1", (96, 112, 48)), ("moss2", (152, 168, 80)),
    # Apollo's sun-gold arrow, and the serpent's eye
    ("gold0", (176, 112, 24)), ("gold1", (240, 192, 64)),
    ("maw", (104, 32, 40)),
]
PYTHOROS_SHINY = {
    # olive and cypress-green scales, a silver arrow instead of gold
    "ter0": (24, 48, 32), "ter1": (40, 80, 48), "ter2": (72, 112, 56), "ter3": (120, 144, 72), "ter4": (176, 192, 112),
    "gold0": (120, 120, 136), "gold1": (208, 208, 216),
    "moss0": (72, 56, 32), "moss1": (128, 96, 48), "moss2": (184, 152, 80),
}

y_scale = Mat(["ter0", "ter1", "ter2", "ter3", "ter4"], line="ter0", cuts=[0.14, 0.36, 0.6, 0.8])
y_belly = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.36, 0.7])
y_moss = Mat(["moss0", "moss1", "moss2"], line="moss0", cuts=[0.3, 0.62])
y_gold = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])
y_maw = Mat(["maw"])


def _yleaf(p, a, b, w, **kw):
    pid = p.lens(a, b, w, y_moss, **kw)
    if p.big:
        p.stroke([a, ((a[0] * 2 + b[0]) / 3, (a[1] * 2 + b[1]) / 3)], "moss0")
    return pid


def _moss(p, x, y, w=6, sprig=0):
    """A tuft of moss in a fold, with an optional laurel sprig (sprig = -1
    leans left, 1 right)."""
    p.blob(x, y, w / 2, 1.6, y_moss, group=60 + int(x))
    if sprig:
        _yleaf(p, (x, y - 0.5), (x + 3.5 * sprig, y - 5.5), 3.2, bend=0.6 * sprig)
        _yleaf(p, (x + sprig, y - 0.5), (x + 5.5 * sprig, y - 2), 3.0, bend=-0.5 * sprig)


def _arrow(p, base, tip, broken=True):
    """Apollo's golden arrow, its head buried at base, snapped off at tip."""
    p.limb([base, tip], 2.2, 2.0, y_gold)
    if p.big and broken:
        dx, dy = tip[0] - base[0], tip[1] - base[1]
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        # splinters at the snapped end
        p.stroke([tip, (tip[0] + ux * 2 - uy * 1.2, tip[1] + uy * 2 + ux * 1.2)], "gold1")
        p.stroke([tip, (tip[0] + ux * 1.5 + uy * 1.2, tip[1] + uy * 1.5 - ux * 1.2)], "gold0")


def _pyhead(p, ox=0.0, oy=0.0, F=0, right=False, s=1.0, W=44.0):
    """Pythoros's head in profile, facing left (or right), built from curves:
    a broad wedge of a skull tapering along a curved top line to a rounded
    snout, a heavy brow ledge jutting over the eye, a deep cheek, and a lower
    jaw with a curved underside (dropped F px at its front). In head-local
    coordinates the snout tip is near (2.4, 15.5) and the jaw's underside
    near y 28; (ox, oy) and s place it, and right mirrors it about x = W/2.
    Returns the transform, for painting the eye and lips by hand."""
    T = (lambda u, v: (ox + s * (W - u), oy + s * v)) if right else (lambda u, v: (ox + s * u, oy + s * v))
    M = lambda pts: [T(u, v) for u, v in pts]
    hinge = (37.0, 22.0)

    def drop(pts):
        if not F:
            return pts
        return [(u, v + F * max(0.0, (hinge[0] - u) / (hinge[0] - 4.0)) * 2.0) for u, v in pts]
    # the cranium, cheek and upper jaw
    upper = (bez3((2.4, 15.5), (2.6, 11.0), (7.0, 8.8), (12.5, 8.0)) +
             bez3((12.5, 8.0), (17.0, 5.6), (25.0, 5.0), (30.0, 5.4)) +
             bez3((30.0, 5.4), (36.0, 5.0), (41.0, 7.6), (42.0, 12.0)) +
             bez3((42.0, 12.0), (42.8, 17.0), (41.4, 22.0), (37.6, 24.8)) +
             bez3((37.6, 24.8), (31.0, 24.8), (21.0, 22.0), (12.0, 20.6)) +
             bez3((12.0, 20.6), (8.0, 20.0), (4.6, 19.8), (3.0, 18.4)))
    p.poly(M(upper), y_scale, group=12)
    p.blob(*T(32.6, 15.6), 8.4 * s, 8.2 * s, y_scale, group=12)
    # the lower jaw, its underside curved, dropping open at the front
    lower = drop(bez3((33.0, 25.0), (24.0, 24.6), (14.0, 23.8), (7.0, 22.6)) +
                 bez3((7.0, 22.6), (4.6, 23.0), (4.2, 25.2), (6.6, 26.4)) +
                 bez3((6.6, 26.4), (14.0, 28.8), (25.0, 29.4), (33.0, 28.2)) +
                 bez3((33.0, 28.2), (37.0, 27.4), (39.6, 25.6), (38.6, 23.6)))
    jaw = p.poly(M(lower), y_scale, group=13)
    p.limb(M(drop([(8.2, 26.2), (17.0, 28.0), (26.0, 28.4), (33.6, 27.2)])), 2.6 * s, 2.0 * s, y_belly,
           clip=[jaw], group=15)
    # the mouth between the lips, wide at the front and closing toward the corner
    mouth = (bez3((4.6, 19.6), (12.0, 20.4), (22.0, 22.2), (33.0, 24.8)) +
             list(reversed(drop(bez3((6.0, 22.6), (14.0, 23.8), (24.0, 24.8), (33.0, 25.4))))))
    p.poly(M(mouth), y_maw, group=14)
    # the heavy brow ledge, jutting forward over the eye
    p.poly(M(lens_pts((10.0, 11.4), (28.0, 4.6), 7.0, bend=2.6 if not right else -2.6, fat=0.34)), y_scale, group=17)
    return T


Y_BANDS = ((0.3, 0.3, 3), (0.42, 0.1, 4), (-0.28, 0.26, 1), (-0.44, 0.12, 0))


# the front view's terraces (centers and centerline radii) and neck
PY_C1, PY_R1 = (31, 51.5), (23, 4.2)
PY_C2, PY_R2 = (33, 42.2), (17, 3.8)
PY_C3, PY_R3 = (36, 35), (10, 3.0)


def py_neck(F=0):
    return bez3((43, 39.5), (57, 28), (55, 3.5), (38, 8.5 - F), n=24)


PYB_C1, PYB_R1 = (32, 55), (22.5, 9)
PYB_C2, PYB_R2 = (37, 45), (17, 3.6)


def py_neck_back():
    return bez3((26, 52), (2.5, 37), (5, 5), (24, 10.5), n=24)


def pythoros(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase if view == "front" else 0     # frame 2: head rears, jaw drops
        (C1, (R1x, R1y)), (C2, (R2x, R2y)), (C3, (R3x, R3y)) = (PY_C1, PY_R1), (PY_C2, PY_R2), (PY_C3, PY_R3)

        # ---- the tail, curling up at the right behind the lowest terrace
        tube(p, bez3((47, 54), (59, 54), (61.5, 45), (57, 41 - F), n=14), 9, 3.4, y_scale, 5, Y_BANDS)
        tube(p, bez((57, 41.5 - F), (54, 38 - F), (51.5, 41 - F)), 3.4, 1.6, y_scale, 5, Y_BANDS)
        # ---- the terraces, each a loop: far half, then near half
        tube(p, arc(C1, R1x, R1y, 185, 355), 11.4, 11.4, y_scale, 2, Y_BANDS, bias=0.1)
        low = tube(p, arc(C1, R1x, R1y, -5, 185), 12.2, 12.2, y_scale, 3, Y_BANDS)
        p.limb(arc(C1, R1x - 0.5, R1y + 4.9, 38, 142), 1.8, 1.8, y_belly, clip=low, group=4, flat=1)
        tube(p, arc(C2, R2x, R2y, 185, 355), 10.6, 10.6, y_scale, 6, Y_BANDS)
        mid = tube(p, arc(C2, R2x, R2y, -5, 185), 11.4, 11.4, y_scale, 7, Y_BANDS)
        p.limb(arc(C2, R2x - 0.5, R2y + 4.6, 42, 138), 1.6, 1.6, y_belly, clip=mid, group=8, flat=1)
        # ---- the neck, rising at the back and arching over toward the foe
        npath = py_neck(F)
        neck = tube(p, npath, 15.6, 12, y_scale, 10, Y_BANDS)
        p.limb(_shift(npath, 5.4, light=(-0.7, 0.7)), 5.4, 4.2, y_belly, clip=neck, group=11)
        # the top terrace, wrapping the neck's base
        tube(p, arc(C3, R3x, R3y, 185, 355), 9.6, 9.6, y_scale, 20, Y_BANDS)
        tube(p, arc(C3, R3x, R3y, -5, 185), 10.2, 10.2, y_scale, 21, Y_BANDS)
        # moss and laurel in the folds
        _moss(p, 9, 46.4, 7, sprig=-1)
        _moss(p, 30, 47.8, 6)
        _moss(p, 52, 46.2, 5, sprig=1)
        _moss(p, 22, 38.4, 5)
        # ---- the scar and the broken golden arrow, high on the neck's side
        p.blob(52.3, 18, 3.4, 2.6, y_belly, ang=-60, group=9)
        _arrow(p, (52.3, 18), (59.5, 10.5 - F))
        # ---- the head
        T = _pyhead(p, 0, -2.5 - F, F)
        if p.big:
            p.eye(*[v - 0.5 for v in T(17.5, 11.6)], 6, 3, iris="gold1", shine="lime2", shine_at=(2, 0))
        else:
            p.px(*T(20, 12.5), "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the coils close to us and cropped
        # by the frame, the Omphalos net down their backs; the neck rising at
        # the left and arching over to the right, the head in right profile
        # under its heavy brow (the art file mirrors the front's head); the
        # arrow still lodged in the neck's flank
        tube(p, bez3((47, 52), (59, 50), (62, 40), (57, 35)), 9, 3.4, y_scale, 5, Y_BANDS)
        tube(p, bez((57, 35.5), (54, 32), (51.5, 35)), 3.4, 1.6, y_scale, 5, Y_BANDS)
        # the neck rising from behind the great near loop, which is cropped by
        # the frame: its far half, a sliver of shadow through the ring, and
        # its near half across the bottom
        npath = py_neck_back()
        neck = tube(p, npath, 18, 13, y_scale, 10, Y_BANDS)
        p.limb(_shift(npath, 6.0, light=(0.7, 0.7)), 5, 4, y_belly, clip=neck, group=11)
        tube(p, arc(PYB_C1, *PYB_R1, 185, 355), 15, 15, y_scale, 2, Y_BANDS)
        tube(p, arc(PYB_C1, *PYB_R1, -5, 185), 16, 16, y_scale, 3, Y_BANDS)
        _moss(p, 50, 43, 7, sprig=1)
        _moss(p, 36, 59.6, 7)
        p.blob(8, 24, 3.4, 2.6, y_belly, ang=60, group=9)
        _arrow(p, (8, 24), (2.5, 16.5))
        T = _pyhead(p, 19, -2.5, 0, right=True)
        if p.big:
            p.eye(*[v - 0.5 for v in T(23.5, 11.6)], 6, 3, iris="gold1", shine="lime2", shine_at=(3, 0))
        return

    if view == "side":
        # follower, walking left: only the reared head and the first coil
        F = 0
        C1, (R1x, R1y) = PY_C1, PY_R1
        tube(p, bez3((47, 54), (59, 54), (61.5, 45), (57, 41 - phase), n=14), 9, 3.4, y_scale, 5, Y_BANDS)
        npath = py_neck(0)
        tube(p, arc(C1, R1x, R1y, 185, 355), 11.4, 11.4, y_scale, 2, Y_BANDS, bias=0.1)
        neck = tube(p, npath, 15.6, 12, y_scale, 10, Y_BANDS)
        p.limb(_shift(npath, 5.4, light=(-0.7, 0.7)), 5.4, 4.2, y_belly, clip=neck, group=11)
        low = tube(p, arc(C1, R1x, R1y, -5, 185), 12.2, 12.2, y_scale, 3, Y_BANDS)
        p.limb(arc(C1, R1x - 0.5, R1y + 4.9, 38, 142), 1.8, 1.8, y_belly, clip=low, group=4, flat=1)
        _moss(p, 22, 44.6, 7, sprig=-1)
        p.blob(52.3, 18, 3.4, 2.6, y_belly, ang=-60, group=9)
        _arrow(p, (52.3, 18), (59.5, 10.5))
        T = _pyhead(p, 0, -2.5 - phase, phase)
        p.eye(*[v - 0.5 for v in T(17.5, 11.6)], 6, 3, iris="gold1", shine="lime2", shine_at=(2, 0))
        return

    if view in ("down", "up"):
        # follower: only the reared head and the first coil, drawn the way
        # the HGSS serpent followers are: a big head on top, the thick neck
        # curving down into one loop that trails to the side, the tail tip
        # flicking out on the other
        down = view == "down"
        sw = phase
        sg = 1 if down else -1
        C = (32 + 3 * sg, 52)
        tube(p, arc(C, 17, 5.6, 185, 355), 12, 12, y_scale, 2, Y_BANDS, bias=0.06)
        tx = C[0] + 17 * sg
        tube(p, bez((C[0] + 9 * sg, 57.5), (tx + 4 * sg, 57), (tx + 6 * sg, 47 - sw)), 8, 3, y_scale, 5, Y_BANDS)
        tube(p, bez((tx + 6 * sg, 47.5 - sw), (tx + 6.5 * sg, 43 - sw), (tx + 3.5 * sg, 43.5 - sw)), 3, 1.4, y_scale, 5, Y_BANDS)
        npath = bez3((C[0] - 13 * sg, 53), (32 - 20 * sg, 44), (32 - 8 * sg, 34), (32, 26))
        neck = tube(p, npath, 17, 18, y_scale, 10, Y_BANDS)
        if down:
            p.limb(_shift(npath, 4, light=(-0.5 * sg, -0.3)), 7, 7, y_belly, clip=neck, group=11)
        low = tube(p, arc(C, 17, 5.6, -5, 185), 13, 13, y_scale, 3, Y_BANDS)
        if down:
            p.limb(arc(C, 16.5, 10.4, 40, 140), 2, 2, y_belly, clip=low, group=4)
        else:
            _moss(p, C[0] + 6, 46.8, 7, sprig=1)
        hx, hy = 32 + (sw if down else -sw), 17
        # the brow ledges, jutting out over the eyes
        p.lens((hx - 4, hy - 8), (hx - 18, hy - 5), 6, y_scale, bend=1.4, fat=0.3, group=16)
        p.lens((hx + 4, hy - 8), (hx + 18, hy - 5), 6, y_scale, bend=-1.4, fat=0.3, group=16)
        # the skull: broad at the temples, tapering to a blunt snout
        tall = 14 if down else 10
        head = bez3((hx - 15, hy - 2), (hx - 16, hy - 14), (hx + 16, hy - 14), (hx + 15, hy - 2)) + \
            bez3((hx + 15, hy - 2), (hx + 14, hy + tall / 2), (hx + 8, hy + tall), (hx, hy + tall)) + \
            bez3((hx, hy + tall), (hx - 8, hy + tall), (hx - 14, hy + tall / 2), (hx - 15, hy - 2))
        p.poly(head, y_scale, group=12)
        if down:
            p.blob(hx, hy + 11.5, 6, 2 + 0.7 * sw, y_maw, group=14)
            p.eye(hx - 11, hy - 4, 5, 4, iris="gold1", shine="lime2", shine_at=(1, 1))
            p.eye(hx + 6, hy - 4, 5, 4, iris="gold1", shine="lime2", shine_at=(3, 1))
            p.pxs([(hx - 4, hy + 10), (hx - 4, hy + 11), (hx + 3, hy + 10), (hx + 3, hy + 11)], "lime2")
            p.pxs([(hx - 2, hy + 6), (hx + 1, hy + 6)], "ter0")
        else:
            # the net down the back of the head and neck
            if p.big:
                for x, y in ((24, 36), (31, 36), (28, 40), (22, 42), (30, 44), (26, 48), (36, 30), (30, 30),
                             (32, 12), (26, 16), (38, 16), (32, 20)):
                    p.px(x, y, "lime1")
        return


MONS = [
    Mon("Pelython", PELYTHON_COLORS, PELYTHON_SHINY, pelython, foot="coil"),
    Mon("Pythoros", PYTHOROS_COLORS, PYTHOROS_SHINY, pythoros, foot="coil"),
]
