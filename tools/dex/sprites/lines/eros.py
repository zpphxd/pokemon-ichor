"""Eros line: Erosie, Himerow (Fairy, then Fairy/Flying). The Erotes, Eros
and his two arrows, gold to kindle love and lead to drive it off."""
from mon_lib import C, Mat, Mon, bez, bez3, ribbon, _fp

INK = C.ink

# --------------------------------------------------------------------------
# Erosie, the little love
# --------------------------------------------------------------------------

EROSIE_COLORS = [
    ("ink", INK),
    # rosy fairy-pink body, after Cleffa: a Pokemon, not a human baby
    ("sk0", (168, 72, 104)), ("sk1", (224, 120, 152)), ("sk2", (248, 168, 184)), ("sk3", (248, 216, 224)),
    # marble-white wings with cool shadows
    ("wg0", (144, 144, 168)), ("wg1", (200, 200, 216)), ("wg2", (248, 248, 240)),
    # sun-gold curls, bowstring and gilded bow
    ("gd0", (160, 96, 32)), ("gd1", (216, 152, 48)), ("gd2", (248, 200, 80)), ("gd3", (248, 240, 160)),
    # the cheeks' deeper rose
    ("pink", (224, 64, 112)),
    ("tw0", (104, 64, 48)),
]
EROSIE_SHINY = {
    # curls and bow lead-gray instead of gold
    "gd0": (72, 72, 88), "gd1": (120, 120, 136), "gd2": (168, 168, 184), "gd3": (216, 216, 224),
    "tw0": (48, 48, 56),
}

e_skin = Mat(["sk0", "sk1", "sk2", "sk3"], line="sk0", cuts=[0.2, 0.46, 0.72])
e_wing = Mat(["wg0", "wg1", "wg2"], line="wg0", cuts=[0.42, 0.7])
e_gold = Mat(["gd0", "gd1", "gd2", "gd3"], line="gd0", cuts=[0.22, 0.48, 0.74])
e_bow = Mat(["tw0", "gd0", "gd1"], line="tw0", cuts=[0.4, 0.7])
e_quiv = Mat(["tw0", "gd0"], line="tw0", cuts=[0.55])


def wing_poly(S, T, B, bulge, n=4, sc=1.3, droop=0.0, taper=0.15):
    """A wing outline: a smooth leading edge from the shoulder S to the tip
    T, bowed out by `bulge`, then a trailing edge of n scalloped feather
    tips from T back to B, where the last feather meets the body. Returns
    (polygon, feather junctions on the trailing edge, their inner ends)."""
    import math
    mx, my = (S[0] + T[0]) / 2, (S[1] + T[1]) / 2
    dx, dy = T[0] - S[0], T[1] - S[1]
    d = math.hypot(dx, dy) or 1.0
    # the leading edge bows away from B
    nx, ny = dy / d, -dx / d
    if (B[0] - mx) * nx + (B[1] - my) * ny > 0:
        nx, ny = -nx, -ny
    lead = bez(S, (mx + nx * bulge, my + ny * bulge), T, n=14)
    tx, ty = B[0] - T[0], B[1] - T[1]
    td = math.hypot(tx, ty) or 1.0
    ox, oy = ty / td, -tx / td                    # outward from the trailing edge
    if (S[0] - T[0]) * ox + (S[1] - T[1]) * oy > 0:
        ox, oy = -ox, -oy
    base = bez(T, ((T[0] + B[0]) / 2 + ox * droop, (T[1] + B[1]) / 2 + oy * droop), B, n=n * 6)
    trail, joints, inner = [], [], []
    for i in range(n):
        seg = base[i * 6:(i + 1) * 6 + 1]
        k = sc * (1.0 - taper * i)
        for j, q in enumerate(seg):
            t = j / (len(seg) - 1)
            bump = math.sin(math.pi * t) ** 0.7 * k
            trail.append((q[0] + ox * bump, q[1] + oy * bump))
        if i:
            a = seg[0]
            joints.append(a)
            inner.append((a[0] + (S[0] - a[0]) * 0.45, a[1] + (S[1] - a[1]) * 0.45))
    return lead + trail, joints, inner


def _ewing(p, S, T, B, bulge, far=False, g=60, n=4, sc=1.3, droop=0.0, mat=None, lines=0.5):
    """A cherub wing; its feather divisions are drawn in the shadow tone."""
    mat = mat or e_wing
    poly, joints, inner = wing_poly(S, T, B, bulge, n=n, sc=sc, droop=droop)
    pid = p.poly(poly, mat, bias=0.2 if far else -0.05, group=g)
    if p.big and lines:
        for a, b in zip(joints, inner):
            p.stroke([a, (a[0] + (b[0] - a[0]) * lines, a[1] + (b[1] - a[1]) * lines)], mat.ramp[0])
    return pid


def feather(p, mat, a, b, w, tone=1, lit=None, bend=0.0, fat=0.42, tip=None, tipfrac=0.34, group=None, **kw):
    """One flat-toned feather from its root a to its tip b, after the laurel
    line's leaves: the half facing the upper-left light is a step lighter,
    and `tip` (a Mat and a tone) dips its end in another color."""
    import math
    from mon_lib import lens_pts
    lit = tone + 1 if lit is None else lit
    pts = lens_pts(a, b, p._minw(w), bend, fat=fat)
    pid = p.poly(pts, mat, flat=tone, group=group, **kw)
    n = len(pts) // 2
    left, right = pts[:n], pts[n:][::-1]
    mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(left, right)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    edge = left if dy - dx > 0 else right
    if p.big and lit != tone and w * p.s >= 2.5:
        p.poly(edge + mid[::-1], mat, clip=[pid], flat=min(lit, len(mat.ramp) - 1), noline=True, **kw)
    if tip is not None:
        tmat, ttone = tip
        k = int(n * (1 - tipfrac))
        p.poly(left[k:] + right[k:][::-1], tmat, clip=[pid], flat=ttone, noline=True, **kw)
        if p.big and w * p.s >= 2.5:
            p.poly(edge[k:] + mid[k:][::-1], tmat, clip=[pid], flat=min(ttone + 1, len(tmat.ramp) - 1), noline=True, **kw)
    return pid


def fan(S, W, T, trail, k_prim):
    """Roots and tips of a wing's flight feathers: `trail` lists the
    trailing-edge tips from the wingtip T inward; the first k_prim are
    primaries rooted near the wrist W, the rest secondaries rooted along
    the arm from W back to the shoulder S."""
    out = []
    n = len(trail)
    for i, q in enumerate(trail):
        if i < k_prim:
            t = i / max(k_prim, 1)
            r = (W[0] + (T[0] - W[0]) * (0.25 - 0.2 * t), W[1] + (T[1] - W[1]) * (0.25 - 0.2 * t) + 1.5)
        else:
            t = (i - k_prim + 1) / max(n - k_prim, 1)
            r = (W[0] + (S[0] - W[0]) * t * 0.85, W[1] + (S[1] - W[1]) * t * 0.85 + 1.0)
        out.append((r, q))
    return out


def erosie(p, view, phase):
    if view in ("front", "icon", "side"):
        fr = view == "front"
        L = 1 if (phase == 1 and fr) else 0       # body bob
        fl = 3 if phase == 1 else 0               # wings beat down
        # the twig bow held up over its head, its tips in the two fists
        p.limb(bez3((16, 22 - L), (16.5, 11 - L), (45.5, 9.5 - L), (46, 21 - L)), 2.6, 2.4, e_bow, group=30)
        # wings on its back, far then near
        _ewing(p, (37, 33 - L), (47, 15 - L + 3 * fl), (52, 27 - L + 2 * fl), 2.6, far=True, g=60, n=3, sc=1.3)
        # far arm, raised up the right side of the head
        p.limb(bez((39, 39 - L), (46.5, 35 - L), (44.5, 23 - L)), 4.6, 4.0, e_skin, bias=0.22, group=20)
        p.circle(44.4, 21.6 - L, 2.6, e_skin, bias=0.22, group=20)
        # quiver at its hip, one blunt arrow standing in it
        p.limb([(46, 42 - L), (47.6, 37.5 - L)], 1.3, 1.3, e_gold)
        p.circle(47.9, 36.5 - L, 1.5, e_skin)
        p.limb([(43.5, 50 - L), (46.4, 42 - L)], 3.8, 3.2, e_quiv)
        _ewing(p, (39, 39 - L), (54, 21 - L + 3 * fl), (51, 46 - L + fl), 3.0, g=70, n=4, sc=1.5)
        # body: a round belly, legs tucked up
        p.blob(35, 44.5 - L, 7.2, 6.2, e_skin, group=1)
        p.blob(40.5, 50.4 - L, 3.4, 2.4, e_skin, ang=-15, bias=0.2, group=2)
        p.blob(32, 51 - L, 4.2, 2.8, e_skin, ang=-18, group=3)
        # big round head with full cheeks
        p.blob(30.5, 30 - L, 9.6, 9.2, e_skin, group=5)
        p.blob(25.5, 33.5 - L, 5.0, 4.0, e_skin, group=5)
        # the one big sun-gold curl, springing from the crown and curling
        # forward over the brow (the art file hand-paints it)
        p.limb(bez((32, 22 - L), (32, 15 - L), (27, 16 - L)), 3.0, 2.4, e_gold, group=7)
        p.circle(26.2, 18 - L, 1.6, e_gold, group=7)
        p.circle(38.6, 27 - L, 1.6, e_gold, group=8)
        # near arm, raised up the left side of the head
        p.limb(bez((28, 40 - L), (15.5, 38 - L), (17.5, 24 - L)), 4.8, 4.2, e_skin, group=21)
        p.circle(17.6, 22.4 - L, 2.7, e_skin, group=21)
        if p.big:
            p.stroke([(17, 21 - L), (45, 20 - L)], "gd2")
            # face: big dark eyes with a shine, a tiny mouth, pink cheeks
            p.eye(28, 26 - L, 4, 6, shine="wg2")
            p.eye(22.5, 26 - L, 3, 6, shine="wg2", shine_at=(1, 1))
            p.pxs([(25, 34 - L), (26, 35 - L)], "sk0")
            p.pxs([(30, 33 - L), (31, 33 - L), (21, 33 - L)], "pink")
        else:
            p.px(29, 28 - L, "ink")
            p.px(23, 28 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the bow held up overhead, both
        # wings spread from its back, the quiver between them with its one
        # blunt arrow, the head turned right in profile
        p.limb(bez3((18, 19), (19, 7), (51, 5), (55.5, 17)), 3.0, 2.8, e_bow, group=30)
        _ewing(p, (45, 45), (61, 27), (60, 50), 3.2, far=True, g=60, n=4, sc=1.6)
        p.limb(bez((44, 47), (57, 41), (54, 21)), 5.6, 4.8, e_skin, bias=0.18, group=20)
        p.circle(54.2, 19, 3.1, e_skin, bias=0.18, group=20)
        p.blob(33, 60, 14.5, 11.5, e_skin, group=1)
        _ewing(p, (30, 47), (4, 30), (9, 61), 3.8, g=70, n=5, sc=1.9)
        p.limb([(35, 64), (29.5, 50)], 4.8, 4.4, e_quiv)
        p.limb([(29.5, 50), (27.6, 45.5)], 1.8, 1.8, e_gold)
        p.circle(27.3, 44.5, 1.9, e_skin)
        p.blob(39, 32, 11, 10.2, e_skin, group=5)
        p.blob(45.5, 37.5, 5.4, 4.2, e_skin, group=5)
        for cx, cy, r in ((31, 28, 3.6), (34, 23.5, 3.6), (39.5, 22, 3.4), (29.5, 34, 3.2), (33, 32, 3.0), (44, 22.6, 2.6)):
            p.circle(cx, cy, r, e_gold, group=6)
        p.limb(bez((43, 22), (46, 15), (50.5, 19)), 3.8, 2.4, e_gold, group=7)
        p.limb(bez((29, 47), (14, 42), (20, 23)), 6.0, 5.0, e_skin, group=21)
        p.circle(20.4, 20.5, 3.3, e_skin, group=21)
        if p.big:
            p.stroke([(19, 19), (54.5, 17)], "gd2")
            p.eye(45, 28, 3, 6, shine="wg2", shine_at=(1, 1))
            p.pxs([(48, 37), (49, 37)], "pink")
            p.px(50, 35, "sk0")
        return

    if view in ("down", "up"):
        # follower: hovering toward or away from the camera, the bow held up
        # overhead in both fists, the stubby wings beating in turn
        st = phase
        dn = view == "down"
        p.limb(bez3((17.5, 22 + st), (18, 10 + st), (46, 10 + st), (46.5, 22 + st)), 2.6, 2.4, e_bow, group=30)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            _ewing(p, (X(37), 40 + st), (X(52), 27 + st + 4 * st), (X(48), 48 + st), 2.6,
                   far=not dn, g=60 + (sx > 0), n=3, sc=1.3, lines=0.5)
        p.blob(32, 44 + st, 6.6, 6.0, e_skin, group=1)
        p.blob(28.5, 50.5 + st, 3.2, 2.4, e_skin, group=2)
        p.blob(35.5, 50.5 + st, 3.2, 2.4, e_skin, group=3)
        if not dn:
            p.limb([(37, 52 + st), (33.5, 42 + st)], 3.4, 3.0, e_quiv)
            p.circle(33, 40.6 + st, 1.6, e_quiv)
        p.blob(32, 31 + st, 9.0, 8.4, e_skin, group=5)
        # the one big curl on the crown
        p.limb(bez((32.5, 23.5 + st), (33.5, 17 + st), (29, 17.5 + st)), 3.4, 2.4, e_gold, group=7)
        p.circle(28.6, 19 + st, 1.8, e_gold, group=7)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            p.limb(bez((X(26.5), 39 + st), (X(18.5), 35 + st), (X(19.5), 24 + st)), 4.4, 3.8, e_skin, group=20 + (sx > 0))
            p.circle(X(19.5), 22.4 + st, 2.6, e_skin, group=20 + (sx > 0))
        if dn:
            p.eye(26.5, 28 + st, 3, 6, shine="wg2")
            p.eye(34.5, 28 + st, 3, 6, shine="wg2")
            p.pxs([(24, 35 + st), (39, 35 + st)], "pink")
            p.pxs([(31, 36 + st), (32, 36 + st)], "sk0")
        else:
            for cx, cy in ((28, 36), (32, 37), (36, 36)):
                p.circle(cx, cy + st, 1.6, e_gold, group=8)
        p.stroke([(19, 21 + st), (45, 21 + st)], "gd2")
        return


# --------------------------------------------------------------------------
# Himerow, the love archer
# --------------------------------------------------------------------------

HIMEROW_COLORS = [
    ("ink", INK),
    # body colour: a pale blush white, the face and slender limbs (no skin)
    ("bd0", (176, 104, 136)), ("bd1", (232, 176, 192)), ("bd2", (248, 232, 232)),
    # swan feathers, marble-white over cool shadow
    ("fw0", (112, 120, 152)), ("fw1", (168, 176, 200)), ("fw2", (216, 216, 232)), ("fw3", (248, 248, 240)),
    # sun-gold: bow, curl, the gold wingtip
    ("gd0", (160, 96, 32)), ("gd1", (232, 168, 48)), ("gd2", (248, 224, 120)),
    # lead: the lead arrows and the lead wingtip
    ("ld0", (64, 64, 88)), ("ld1", (128, 128, 152)),
    # the gold arrows (a color of their own, so the shiny can turn them to lead)
    ("ag", (240, 192, 56)),
    ("pink", (240, 120, 160)),
]
HIMEROW_SHINY = {
    "fw0": (176, 96, 128), "fw1": (224, 152, 176), "fw2": (240, 200, 216), "fw3": (248, 232, 232),
    "ag": (152, 152, 176),
}

h_skin = Mat(["bd0", "bd1", "bd2"], line="bd0", cuts=[0.3, 0.64])
h_fth = Mat(["fw0", "fw1", "fw2", "fw3"], line="fw0", cuts=[0.2, 0.44, 0.7])
h_gold = Mat(["gd0", "gd1", "gd2"], line="gd0", cuts=[0.34, 0.66])
h_lead = Mat(["ld0", "ld1"], line="ld0", cuts=[0.5])
h_quiv = Mat(["ld0", "ld1"], line="ld0", cuts=[0.45])


def _swan(p, S, T, B, bulge, tipmat, far=False, g=60, n=6, sc=1.7, droop=1.0, cov=0.5, tipk=3, flap=0):
    """A swan wing in flat bands, the way Gen 3 draws a bird's wing: the
    flight feathers with scalloped tips (the primaries dipped in `tipmat`,
    gold or lead), a lighter band of coverts, and the bright leading edge."""
    import numpy as np
    T = (T[0], T[1] + flap)
    B = (B[0], B[1] + flap * 0.4)
    o = 0 if far else 1
    poly, joints, inner = wing_poly(S, T, B, bulge, n=n, sc=sc, droop=droop, taper=0.06)
    w = p.poly(poly, h_fth, flat=o + 0, group=g)
    # the primaries' tips, the outer feathers' ends
    tips = [T] + joints[:tipk]
    m = np.zeros_like(p.fig.pid, bool)
    for q in tips:
        inner_q = (q[0] + (S[0] - q[0]) * 0.3, q[1] + (S[1] - q[1]) * 0.3)
        m |= p.mask(ribbon([q, inner_q], lambda t: 2 * sc + 2.5))
    m &= p.fig.pid == w
    p.add(m, tipmat, flat=len(tipmat.ramp) - 1 if not far else 0, group=g + 1, noline=True)
    # coverts: the leading part of the wing, scalloped too
    Bc = (S[0] + (B[0] - S[0]) * cov + (T[0] - S[0]) * cov * 0.5, S[1] + (B[1] - S[1]) * cov + (T[1] - S[1]) * cov * 0.5)
    Tc = (S[0] + (T[0] - S[0]) * 0.72, S[1] + (T[1] - S[1]) * 0.72)
    cpoly, cj, _ = wing_poly(S, Tc, Bc, bulge * 0.9, n=max(3, n - 2), sc=sc * 0.8, droop=0.5)
    p.poly(cpoly, h_fth, flat=o + 1, group=g + 2)
    # the leading edge
    lead = bez(S, ((S[0] + T[0]) / 2, (S[1] + T[1]) / 2), T, n=10)
    import math
    dx, dy = T[0] - S[0], T[1] - S[1]
    d = math.hypot(dx, dy)
    nx, ny = dy / d, -dx / d
    if (B[0] - S[0]) * nx + (B[1] - S[1]) * ny > 0:
        nx, ny = -nx, -ny
    arc = [(x + nx * bulge * 4 * t * (1 - t), y + ny * bulge * 4 * t * (1 - t)) for (x, y), t in
           zip(lead, [i / 10 for i in range(11)])]
    p.limb(arc[:9], 3.4, 2.0, h_fth, flat=o + 2, group=g + 3)
    if p.big:
        for a, b in zip(joints, inner):
            p.stroke([a, (a[0] + (b[0] - a[0]) * 0.3, a[1] + (b[1] - a[1]) * 0.3)], "fw0")
    return w


def _plume(p, x, y, sway=0.0, g=40):
    """The lower body: a long gown of swan feathers from the waist (x, y),
    tapering to a point and sweeping a little back."""
    for k, (a, b, w, bend, tone) in enumerate((
            ((x + 4, y), (x + 13 + sway, y + 19), 6.4, -1.4, 0),
            ((x + 1.5, y), (x + 7 + sway, y + 22), 8.0, -1.0, 1),
            ((x - 1, y - 1), (x + 0.5 + sway, y + 18), 7.4, 0.2, 2))):
        feather(p, h_fth, a, b, w, tone=tone, bend=bend, fat=0.3, group=g + k)


def _swan_fan(p, root, tips, tipmat, g, lead_tip, w=6.0, far=False):
    """A swan wing for the follower and the icon: long feathers fanned from
    the shoulder, the outer two dipped in gold or lead, under a bright
    leading edge."""
    rx, ry = root
    for k, (tx, ty) in enumerate(tips[::-1]):
        kk = len(tips) - 1 - k
        a = (rx + (tx - rx) * 0.2, ry + (ty - ry) * 0.2)
        pid = p.lens(a, (tx, ty), w, h_fth, fat=0.55, flat=2 if kk < 2 else 1, group=g + k)
        if kk < 2:
            p.lens(((a[0] + tx * 2) / 3, (a[1] + ty * 2) / 3), (tx, ty), w * 0.9, tipmat, fat=0.4,
                   flat=len(tipmat.ramp) - 1, clip=[pid], group=g + k, noline=True)
    p.limb([root, ((rx + lead_tip[0]) / 2, (ry + lead_tip[1]) / 2 - 2), lead_tip], 3.6, 2.4, h_fth, flat=3, group=g + 20)


def himerow(p, view, phase):
    if view in ("front", "side"):
        # the battle sprites are hand-finished in art/himerow_*.txt; this
        # draft gives the side follower and the art's starting shapes
        fr = view == "front"
        L = 1 if (phase == 1 and fr) else 0
        dw = 2 if (phase == 1) else 0            # wings beat down a little
        # far wing: a simple lead-tipped fan behind the head
        for k, tip in enumerate(((49, 9 + dw), (45.4, 5.2 + dw))):
            pid = p.lens((37.6, 24 - L), tip, 6.8, h_fth, fat=0.55, flat=1, group=100 + k)
            p.lens(((37.6 + tip[0] * 4) / 5, (24 - L + tip[1] * 4) / 5), tip, 6.0, h_lead, fat=0.4, flat=1,
                   clip=[pid], group=100 + k, noline=True)
        # near wing, sweeping up and back, gold-tipped
        _swan(p, (38, 31), (60, 9), (50, 45), 5.0, h_gold, g=150, n=6, sc=1.8, tipk=3, flap=dw)
        # the bow: a tall gold recurve, held out to the left
        p.limb(bez3((13.6, 11 - L), (6, 17 - L), (6, 37 - L), (13.6, 43 - L)), 2.6, 2.6, h_gold, group=30)
        # lower body: the swan-feather gown
        _plume(p, 32, 39 - L, sway=L)
        # quiver at the hip, gold and lead arrows standing in it
        for x0, c in ((41.4, "ag"), (43, "ld"), (44.6, "ag")):
            p.limb([(x0 - 1.4, 39 - L), (x0 + 0.6, 33.4 - L)], 1.3, 1.3, Mat(["ag"]) if c == "ag" else h_lead)
        p.limb([(38.6, 46.5 - L), (42.6, 37.2 - L)], 3.8, 4.0, h_quiv, group=35)
        # torso: swan-down plumage, white over a blush belly
        p.blob(31.4, 30.4 - L, 6.6, 6.8, h_fth, group=1)
        p.limb([(31.6, 33 - L), (32.4, 39.4 - L)], 9.0, 6.4, h_fth, group=1)
        # far arm, the bow arm: slender, straight out to the grip
        p.limb([(27.6, 28.4 - L), (18, 27.4 - L), (10.4, 27 - L)], 2.8, 2.4, h_skin, bias=0.15, group=20)
        p.circle(9.4, 27 - L, 2.0, h_skin, bias=0.15, group=20)
        # near arm drawing the string back under the chin, elbow high
        p.limb([(35.4, 28.4 - L), (42, 21.6 - L)], 3.2, 2.8, h_skin, group=21)
        p.limb([(42, 21.6 - L), (34, 24.6 - L), (28.6, 26.6 - L)], 2.8, 2.4, h_skin, group=21)
        # the big round head, gold hair swept back into one great curl
        p.blob(27, 13.4 - L, 9.8, 9.6, h_skin, group=5)
        p.poly([(16.4, 13.8), (18.2, 10.2), (21.4, 9.4), (26.6, 9.6), (31, 12.4), (32.4, 18), (33.8, 21.4),
                (36.8, 18), (37.4, 11), (35.8, 6), (32, 3.2), (27, 2.4), (21.6, 3.2), (18, 6), (16.2, 9.6)],
               h_gold, group=6)
        p.limb(bez((34, 6 - L), (37, 0.6 - L), (41.6, 4 - L)), 3.6, 2.4, h_gold, group=7)
        # the string, and the gold arrow nocked on it
        if p.big:
            p.stroke([(14, 12 - L), (16, 15 - L)], "gd2")
            p.stroke([(27, 28 - L), (14, 42 - L)], "gd2")
            p.stroke([(26, 27 - L), (5, 27 - L)], "ag")
            p.pxs([(3, 27 - L), (4, 26 - L), (4, 28 - L), (5, 25 - L), (5, 29 - L)], "ag")
            p.pxs([(26, 26 - L), (26, 28 - L)], "pink")
            p.eye(19, 12 - L, 4, 6, iris="gd1", shine="fw3")
            p.eye(25, 12 - L, 5, 6, iris="gd1", shine="fw3")
        else:
            p.stroke([(26, 27 - L), (5, 27 - L)], "ag")
            p.px(20.5, 14 - L, "ink")
            p.px(26.5, 14 - L, "ink")
        return

    if view == "back":
        # (the hand-finished art replaces this) over the shoulder: a mound of
        # swan-down where the wings are rooted, the big head in profile
        p.limb([(47, 37), (53, 34.6), (56.6, 34)], 3.2, 2.8, h_skin, group=20)
        _swan(p, (32, 42), (5, 17), (21, 62), 6.0, h_gold, g=150, n=7, sc=2.0, tipk=3)
        p.blob(39.4, 54, 14.6, 17.4, h_fth, group=1)
        p.blob(40, 41, 10.4, 7.4, h_fth, group=1)
        p.limb([(33, 64), (26.4, 50)], 6.0, 6.4, h_quiv, group=35)
        p.limb([(34, 38.4), (25.6, 32), (37, 30.6), (48.6, 29.8)], 3.6, 2.8, h_skin, group=21)
        p.blob(44, 16.4, 11.0, 10.6, h_skin, group=5)
        p.poly([(33, 19), (33.4, 11), (36.6, 6.4), (42, 4.6), (47.6, 5), (52, 7.6), (54.4, 11.4), (46.4, 10.8),
                (44.4, 14.4), (43.8, 19), (44.6, 24.6), (41, 26.6), (37, 25.4)], h_gold, group=6)
        p.limb(bez((38.6, 8), (33.4, 0.8), (27.6, 5.4)), 4.6, 3.0, h_gold, group=7)
        p.limb(bez3((54, 10), (61, 18), (61, 44), (54, 52)), 3.0, 3.0, h_gold, group=30)
        if p.big:
            p.eye(49, 13, 4, 6, iris="gd1", shine="fw3")
        return

    if view in ("down", "up"):
        # follower: hovering toward or away from the camera on its swan-feather
        # gown, both wings raised (gold-tipped and lead-tipped), the bow in
        # one hand; the wings beat in turn
        st = phase
        dn = view == "down"
        for sx, tipm in ((-1, h_gold), (1, h_lead)):
            X = lambda x: 32 + sx * (x - 32)
            f = 3 * st if sx < 0 else 3 * (1 - st)
            _swan_fan(p, (X(36), 27), [(X(54), 2 + f), (X(58), 9 + f), (X(57), 17 + f), (X(53), 25 + f), (X(46), 32)],
                      tipm, 100 + 60 * (sx > 0), (X(51), 1.5 + f), w=6.6)
        for k, (a, b, w) in enumerate((((30, 38), (25, 58), 7.0), ((34, 38), (39, 58), 7.0), ((32, 37), (32, 61), 8.4))):
            feather(p, h_fth, a, b, w, tone=1 + (k == 2), bend=0.0, fat=0.3, group=40 + k)
        p.limb([(32, 24), (32, 38)], 9.4, 6.8, h_fth, group=1)
        if not dn:
            for x0, c in ((34, "ag"), (36, "ld"), (38, "ag")):
                p.limb([(x0 - 1, 40), (x0 + 1, 33)], 1.4, 1.4, Mat(["ag"]) if c == "ag" else h_lead)
            p.limb([(32, 46), (36, 37)], 4.2, 4.2, h_quiv, group=35)
        p.limb([(27.5, 25), (23.6, 32), (22.4, 39)], 2.6, 2.2, h_skin, group=20)
        p.limb([(36.5, 25), (40.4, 32), (41.6, 39)], 2.6, 2.2, h_skin, group=21)
        p.limb(bez3((19, 28), (14.6, 35), (14.6, 47), (19, 54)), 2.6, 2.6, h_gold, group=30)
        if dn:
            p.blob(32, 15, 9.0, 8.8, h_skin, group=5)
            p.poly([(24.4, 15), (25, 10), (29, 7), (35, 7), (39, 10), (39.6, 15), (37.4, 12), (32, 10.6), (26.6, 12)],
                   h_gold, group=6)
            p.limb(bez((34, 8), (37, 1), (42, 5)), 3.6, 2.2, h_gold, group=7)
            p.eye(26.5, 13, 4, 6, iris="gd1", shine="fw3")
            p.eye(33.5, 13, 4, 6, iris="gd1", shine="fw3")
        else:
            p.blob(32, 15, 9.0, 8.8, h_gold, group=5)
            p.limb(bez((34, 10), (37, 2), (42, 6)), 3.6, 2.2, h_gold, group=7)
        return

    if view == "icon":
        # party icon: a big head with its gold curl, both wings raised behind
        # (gold-tipped and lead-tipped), the bow before it
        _swan_fan(p, (38, 31), [(54, 3), (60, 11), (59, 21), (54, 30), (47, 37)], h_gold, 100, (50, 2), w=8)
        _swan_fan(p, (26, 31), [(10, 3), (4, 11), (5, 21), (10, 30), (17, 37)], h_lead, 160, (14, 2), w=8)
        for k, (a, b, w) in enumerate((((30, 44), (27, 60), 8.0), ((34, 44), (38, 60), 8.0))):
            feather(p, h_fth, a, b, w, tone=2, fat=0.3, group=40 + k)
        p.limb([(32, 32), (32, 46)], 11, 8.6, h_fth, group=1)
        p.blob(31, 22, 10.4, 10, h_skin, group=5)
        p.poly([(20.6, 20), (21.4, 13.6), (26, 9.6), (33, 9), (39.6, 12), (42, 18), (41.4, 26), (38.4, 24.4),
                (37, 18), (31, 15.4), (24.6, 16.6), (22, 21)], h_gold, group=6)
        p.limb(bez((36, 11), (41, 1), (48, 6)), 5, 3, h_gold, group=7)
        p.limb(bez3((16, 26), (8, 34), (8, 48), (16, 56)), 3.2, 3.2, h_gold, group=30)
        p.stroke([(16, 27), (28, 41), (16, 55)], "gd2")
        p.eye(23.5, 19, 3, 5, iris="gd1", shine="fw3")
        p.eye(30, 19, 4, 5, iris="gd1", shine="fw3")
        return


# --------------------------------------------------------------------------

# a chubby infant's foot: five round toes over a plump sole
EROSIE_FOOT = [
    "", "", "",
    ".....#.#.#.#....",
    "................",
    ".....########...",
    "....##########..",
    "....##########..",
    ".....########...",
    ".....#######....",
    "......#####.....",
]

MONS = [
    Mon("Erosie", EROSIE_COLORS, EROSIE_SHINY, erosie, foot=_fp(EROSIE_FOOT), icon_pal=0),
    Mon("Himerow", HIMEROW_COLORS, HIMEROW_SHINY, himerow, foot="blank", icon_pal=1),
]
