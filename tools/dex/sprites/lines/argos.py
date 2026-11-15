"""Argos line: Nostail (#138, Normal), Odysseus's hound.

Concept C, "Swift and Shining". The Greek name Argos meant both "swift" and
"shining white", and this is the hound as it ran in its youth, or as it runs
still, home across twenty years: a white sighthound in a flying gallop, its
coat shaded with the blue of Ithaca's sea and sheened with pale gold, a gray
muzzle kept as the mark of the long wait, and sun-gold eyes that knew its
master at once. Its wag throws a comet's arc of gold light over its back, and
as the light fades it breaks into the Greek wave scroll, the pattern the vase
painters called the "running dog". It wears the old terracotta collar with a
black-figure meander.

The battle front (both frames) and back are hand-finished in
art/nostail_*.txt: the face, ear, collar, plumed tail, comet and scroll are
hand-placed there, and the coat is reshaded with sea-blue shadows, a gold
rim, sea light bounced under the belly and a row of wave crests along the
flank. This draft feeds the icon and the follower, and gives the art its
silhouettes.
"""
from mon_lib import C, Mat, Mon, Pen, bez, bez3

INK = C.ink

COLORS = [
    ("ink", INK),
    # the coat: Aegean-sea shadow up to white
    ("sea0", (24, 48, 112)), ("sea1", (56, 96, 168)), ("sea2", (112, 152, 208)),
    ("coat0", (176, 200, 232)), ("coat1", (224, 232, 248)), ("white", (248, 248, 248)),
    # pale-gold sheen on the lit rim; the white-gold core of the comet
    ("sheen", (248, 232, 160)),
    # the comet and the eyes
    ("gold0", (192, 112, 24)), ("gold1", (240, 184, 48)),
    # the old terracotta collar
    ("terra0", (136, 48, 24)), ("terra1", (208, 104, 56)),
    # the gray muzzle of age
    ("grey0", (96, 96, 112)), ("grey1", (160, 160, 176)),
    # sea light: Ithaca's water bounced up under the belly and the jaw
    ("foam", (96, 184, 200)),
]
# Shining silver-white: the sea leaves the shadows, which turn pewter and
# silver; the sun-gold eyes and comet stay.
SHINY = {
    "sea0": (48, 48, 72), "sea1": (96, 96, 120), "sea2": (144, 144, 168),
    "coat0": (192, 192, 208), "coat1": (232, 232, 240), "foam": (176, 184, 208),
}

coat = Mat(["sea0", "sea1", "sea2", "coat0", "coat1", "white"], line="sea1",
           cuts=[0.3, 0.44, 0.56, 0.68, 0.82])
far = Mat(["sea0", "sea1", "sea2", "coat0"], line="sea0", cuts=[0.4, 0.56, 0.74])
muzzle = Mat(["grey0", "grey1", "coat0"], line="grey0", cuts=[0.5, 0.75])
collar_m = Mat(["terra0", "terra1"], line="terra0", cuts=[0.6])
glow = Mat(["gold0", "gold1", "sheen", "white"], cuts=[0.25, 0.5, 0.75])


def _leg(p, pts, widths, mat, **kw):
    """A jointed leg: one tapering limb per segment, so elbow, wrist, stifle
    and hock read."""
    for i in range(len(pts) - 1):
        p.limb(pts[i:i + 2], widths[i], widths[i + 1], mat, **kw)


def comet(p, path, w0, w1, group=95):
    """A streak of gold light: amber edges, a gold body, a white-gold core,
    widest and hottest at the start (the tail tip), no ink outline."""
    kw = dict(nooutline=True, noline=True, group=group, cap=False)
    base = p.limb(path, w0, w1, glow, flat=0, **kw)
    if not base:
        return
    n = len(path)
    p.limb(path, w0 * 0.72, w1 * 0.5, glow, flat=1, clip=[base], **kw)
    if p.big:
        core = path[: int(n * 0.7)]
        p.limb(core, w0 * 0.42, 0.6, glow, flat=2, clip=[base], **kw)
        p.limb(path[: int(n * 0.25)], w0 * 0.22, 0.4, glow, flat=3, clip=[base], **kw)


# --------------------------------------------------------------------------
# Battle front: the flying gallop, facing left, rising to the upper left
# --------------------------------------------------------------------------

STRIDES = {
    # extended suspension: forelegs reaching, hind legs thrown back
    0: dict(near_fore=[(20.5, 34), (17, 40), (10, 43.5), (5.5, 45)],
            far_fore=[(24.5, 36), (21.5, 42.5), (13.5, 47.5), (9.5, 49.5)],
            near_hind=[(48, 37), (51.5, 43), (55.5, 48), (59.6, 51)],
            far_hind=[(45, 38), (47.5, 45), (52, 51.5), (56, 56)]),
    # gathered suspension: forelegs folded back under the chest, hind legs
    # swung forward past them, the back arched
    1: dict(near_fore=[(21.5, 34), (20.5, 41), (23.5, 47), (28, 48.5)],
            far_fore=[(25, 36), (26.5, 42.5), (31, 46.5), (35, 46)],
            near_hind=[(46, 34), (41, 41.5), (44, 47.5), (37.5, 53)],
            far_hind=[(43, 35), (37.5, 42.5), (38.5, 49.5), (31.5, 55)]),
}

# the torso, a deep keel tucking up to a narrow waist (phase 0; phase 1
# arches the loin and draws the haunch forward)
TORSO = [(21, 24.5), (27, 22.2), (33, 21.6), (39, 22.2), (45, 24.2), (50, 27.4), (53, 31.5), (53.2, 36.4),
         (50.5, 40.4), (46.5, 41), (43.5, 38.4), (40.5, 35.6), (36.5, 37.8), (31.5, 40.6), (26.5, 42.4),
         (21.5, 41.8), (17.4, 38.2), (16.2, 32.6), (17.6, 27.4)]


def _torso(phase):
    if not phase:
        return TORSO
    out = []
    for x, y in TORSO:
        if x > 30:
            k = min(1.0, (x - 30) / 10) * (1 - max(0.0, (x - 44) / 12))
            y -= 3.0 * k                       # the loin arches up
            x -= 2.0 * min(1.0, (x - 30) / 14)  # the haunch draws forward
        out.append((x, y))
    return out


# a long sighthound head: a domed skull, a slight stop, a long muzzle
# tapering to the nose pad
HEAD = [(20.5, 9.8), (17.2, 7.8), (13.6, 8.2), (11.0, 10.0), (7.4, 12.2), (4.0, 14.2), (2.4, 15.3),
        (2.0, 16.6), (2.8, 17.8), (6.2, 18.4), (10.4, 18.8), (14.2, 19.0), (17.8, 19.0), (21.2, 17.4),
        (22.8, 13.4)]
# the near ear: a long silky pennant streaming back from the crown
EAR = [(16.2, 9.6), (19, 7.4), (23, 6.6), (27, 7.0), (30.5, 8.0), (32.6, 9.2), (31, 9.8), (33, 11.0),
       (30, 11.4), (31.4, 12.8), (27.6, 12.2), (23.6, 11.6), (20, 11.8), (17.6, 11.8)]


def _front(p, phase):
    st = STRIDES[phase]
    big = p.big
    hy = 0.0  # the head holds steady through the stride; the body moves under it

    def H(pts):
        return [(x, y + hy) for x, y in pts]

    # ---- the comet, thrown off the tail tip and arcing over the back --------
    if phase == 0:
        tip = (57.5, 14.5)
        arc = bez3(tip, (56.5, 4), (46, 1.8), (37, 5), n=30)
    else:
        tip = (56.5, 17)
        arc = bez3(tip, (59, 5.5), (48, 1.5), (38, 4.5), n=30)
    comet(p, arc, 4.0, 1.0)

    # ---- far ear, a dark sliver streaming back behind the head ---------------
    p.lens(*H([(19.5, 11.6), (31, 14.2)]), 3.6, far, bend=-1.0, fat=0.4, group=40)

    # ---- far legs, in Aegean shadow ------------------------------------------
    _leg(p, st["far_fore"], (7.0, 5.0, 3.6, 3.2), far, group=10, bias=0.06)
    ff = st["far_fore"][-1]
    p.blob(ff[0] - (0.6 if phase == 0 else -0.4), ff[1] + 0.3, 2.8, 1.7, far, group=10, bias=0.06)
    _leg(p, st["far_hind"], (8.0, 5.4, 3.8, 3.2), far, group=11, bias=0.06)
    fh = st["far_hind"][-1]
    p.blob(fh[0] + (0.5 if phase == 0 else -0.5), fh[1] + 0.2, 2.8, 1.7, far, group=11, bias=0.06)

    # ---- tail: a long feathered sweep up from the croup ------------------------
    if phase == 0:
        tail = bez3((51, 30), (58, 30), (60.2, 22.5), (57.5, 14.5), n=16)
    else:
        tail = bez3((49, 27.5), (56, 28.5), (59.8, 24), (56.5, 17), n=16)
    p.limb(tail, 5.0, 2.6, coat, group=5)

    # ---- body ------------------------------------------------------------------
    p.poly(_torso(phase), coat, group=1)
    if big:
        p.shade([(18, 37), (31, 36), (31, 43), (20, 43)], 0.12)              # under the keel
        p.shade([(31, 34), (44, 33), (44, 39), (31, 40)], 0.14)              # tucked belly

    # ---- near hind: a muscled thigh, the gaskin, the hock ----------------------
    nh = st["near_hind"]
    if phase == 0:
        p.blob(47.5, 33.5, 6.4, 7.6, coat, ang=-28, group=13, noline=True)
    else:
        p.blob(45, 32, 6.4, 7.6, coat, ang=22, group=13, noline=True)
    _leg(p, nh, (8.6, 5.8, 4.0, 3.4), coat, group=13)
    p.blob(nh[-1][0] + (0.6 if phase == 0 else -0.6), nh[-1][1] + 0.3, 3.0, 1.8, coat, group=13)

    # ---- neck, with a silky frill at the throat, and the head ----------------------
    neck = p.poly(H([(15, 18.5), (17.6, 11.8), (21.5, 11), (25.5, 16.4), (29.5, 22.4), (24, 27.5), (19, 31)]),
                  coat, group=2)
    p.lens(*H([(15.5, 22)]), (16.6, 33.5), 5.4, coat, bend=1.2, fat=0.35, group=2)
    hid = p.poly(H(HEAD), coat, group=3)
    p.circle(17.2, 13.0 + hy, 5.0, coat, group=3)                            # round skull
    # the gray muzzle of age
    p.limb(H(bez((11, 15.0), (7, 15.8), (2.6, 16.8))), 4.8, 2.8, muzzle, clip=[hid], noline=True, group=3)
    if big:
        p.shade(H([(8, 18.4), (22, 16.4), (22, 19.6), (8, 19.8)]), 0.15)     # under the jaw

    # ---- collar: terracotta across the neck ------------------------------------
    p.limb(H([(15.6, 24.2), (26, 16.8)]), 3.6, 3.6, collar_m, clip=[neck], group=7, cap=False)

    # ---- near ear: a feathered pennant streaming back ----------------------------
    p.poly(H(EAR), coat, group=41)

    # ---- near fore: the shoulder, the elbow, the reaching forearm ------------------
    nf = st["near_fore"]
    p.blob(23, 31.5, 5.4, 7.0, coat, ang=-20, group=12, noline=True)
    _leg(p, nf, (7.6, 5.4, 4.0, 3.4), coat, group=12)
    p.blob(nf[-1][0] - (0.8 if phase == 0 else -0.6), nf[-1][1] + 0.3, 3.1, 1.8, coat, group=12)

    # ---- face ------------------------------------------------------------------------
    if big:
        p.eye(12, 10.8 + hy, 3, 3, iris="gold1", shine="sheen", shine_at=(1, 0))
        p.pxs(H([(1.6, 15.4), (1.6, 16.4), (2.6, 15.4)]), "ink")                # nose pad
        p.stroke(H([(4.4, 17.4), (9.4, 17.6)]), "grey0")                        # mouth
    else:
        p.px(13, 12 + hy, "ink")


# --------------------------------------------------------------------------
# Battle back: over the shoulder
# --------------------------------------------------------------------------

BACK_DY = 3  # the back view's head sits this far below the front's


def _back(p):
    """Over the left shoulder, at about 1.2x: the tail rising at the left with
    the comet arching over the top and breaking into the wave scroll, the
    long back sloping down to the haunch, the shoulder blades, the neck
    rising at the right and the head turned into right profile, its ear
    streaming back. The hand-finished art mirrors the front's head."""
    def hd(pts):  # the front's head, mirrored to face right
        return [(63 - x, y + BACK_DY) for x, y in pts]

    comet(p, bez3((9.5, 17), (8.0, 3.5), (14, 1.6), (19.5, 2.6), n=30), 4.2, 1.2)
    tail = bez3((13, 48), (2.4, 42), (2.4, 27), (9.5, 17), n=18)
    p.limb(tail, 6.0, 3.0, coat, group=5)
    p.blob(14.5, 61, 13.5, 13, coat, group=8)                              # haunch, cropped
    back = [(8, 48), (14, 44), (21, 40.5), (27, 37.5), (32, 34.5), (36, 31), (42, 29.5), (50, 32), (56, 39),
            (59.5, 50), (61, 64), (3, 64), (3, 57)]
    p.poly(back, coat, group=1)                                            # the long back
    p.blob(44, 45, 11, 12, coat, ang=20, group=9, noline=True)            # near shoulder blade
    neck = p.poly([(32, 34), (35.5, 27), (38.5, 20), (40.5, 14.5), (48, 14.5), (52.5, 20), (54.5, 28),
                   (56, 38), (46, 38)], coat, group=2)
    p.limb([(35, 28.5), (54.5, 23)], 4.2, 4.2, collar_m, clip=[neck], group=7, cap=False)
    hid = p.poly(hd(HEAD), coat, group=3)
    p.circle(*hd([(17.2, 13.0)])[0], 5.0, coat, group=3)
    p.limb(hd(bez((11, 15.0), (7, 15.8), (2.6, 16.8))), 4.8, 2.8, muzzle, clip=[hid], noline=True, group=3)
    p.poly(hd(EAR), coat, group=41)
    if p.big:
        x, y = hd([(12, 10.8)])[0]
        p.eye(x - 3, y, 3, 3, iris="gold1", shine="sheen", shine_at=(1, 0))


# --------------------------------------------------------------------------
# Follower and icon
# --------------------------------------------------------------------------

def _grow(p, k=1.25):
    """The follower views are drawn a size up: the flying gallop's wide frame
    would otherwise shrink a walking hound too far."""
    return Pen(p.fig, p.s * k, p.ox + p.s * 32 * (1 - k), p.oy + p.s * 62 * (1 - k), p.view, p.phase)


# lighter ramps for the small follower shapes, so the white coat stays white
fcoat = Mat(["sea1", "sea2", "coat0", "coat1", "white"], line="sea1", cuts=[0.55, 0.66, 0.76, 0.86])
ffar = Mat(["sea0", "sea1", "sea2", "coat0"], line="sea0", cuts=[0.5, 0.66, 0.82])


def _down(p, phase):
    """Trotting toward the camera: the long head foreshortened, the gray
    muzzle pointing at you, the rose ears flying out, the collar, a deep
    narrow chest; the tail and its comet rise behind."""
    st = phase
    p = _grow(p)
    comet(p, bez((42, 30), (46.5, 19), (37, 16), n=14), 3.4, 1.2)
    p.limb(bez((38, 44), (44, 40), (42, 30)), 4.4, 3.2, fcoat, flat=3, group=5)        # tail behind
    p.limb([(26.5, 47), (26, 60 - 2 * st)], 4.2, 3.2, ffar, flat=2, group=10)        # hind legs between
    p.limb([(37.5, 47), (38, 60 - 2 * (1 - st))], 4.2, 3.2, ffar, flat=2, group=11)
    p.blob(32, 44, 8.0, 8.6, fcoat, group=1)                                          # chest
    p.limb([(28.5, 46), (28.5, 60 - 2 * (1 - st))], 5.0, 4.0, fcoat, group=12)
    p.limb([(35.5, 46), (35.5, 60 - 2 * st)], 5.0, 4.0, fcoat, group=13)
    p.blob(28.5, 60.5 - 2 * (1 - st), 3.0, 1.8, fcoat, group=12)
    p.blob(35.5, 60.5 - 2 * st, 3.0, 1.8, fcoat, group=13)
    p.limb([(32, 39), (32, 29)], 11.0, 9.0, fcoat, group=2)                            # neck
    p.limb([(26, 35.5), (38, 35.5)], 3.6, 3.6, collar_m, flat=1, group=7, cap=False)
    p.lens((27, 22.5), (15.5, 28.5 + st), 5.6, fcoat, bend=-1.0, fat=0.35, group=40)  # ears flying out
    p.lens((37, 22.5), (48.5, 28.5 + (1 - st)), 5.6, fcoat, bend=1.0, fat=0.35, group=41)
    p.blob(32, 24, 6.4, 5.6, fcoat, group=3)                                           # skull
    p.limb([(32, 27), (32, 34.5)], 6.0, 4.0, muzzle, group=4)                         # muzzle
    if p.big:
        p.eye(27, 23, 3, 3, iris="gold1", shine="sheen", shine_at=(1, 0))
        p.eye(34, 23, 3, 3, iris="gold1", shine="sheen", shine_at=(1, 0))
    else:
        p.pxs([(28, 24), (35, 24)], "ink")
        p.pxs([(28, 25), (35, 25)], "gold1")
    p.pxs([(31, 35), (32, 35)], "ink")


def _up(p, phase):
    """Trotting away: the haunches and the long back, the plumed tail raised
    with its comet arcing over, the head and flying ears beyond."""
    st = phase
    p = _grow(p)
    p.lens((28, 19), (16, 23 + st), 5.4, fcoat, bend=-1.0, fat=0.35, group=40)        # ears
    p.lens((36, 19), (48, 23 + (1 - st)), 5.4, fcoat, bend=1.0, fat=0.35, group=41)
    p.blob(32, 19, 6.0, 5.2, fcoat, group=3)                                           # the back of the head
    p.limb([(32, 34), (32, 23)], 10.0, 8.5, fcoat, group=2)                            # neck
    p.limb([(26.5, 28), (37.5, 28)], 3.6, 3.6, collar_m, flat=1, group=7, cap=False)
    p.limb([(27.5, 50), (27, 60 - 2 * st)], 5.0, 4.0, fcoat, group=12)                # hind legs
    p.limb([(36.5, 50), (37, 60 - 2 * (1 - st))], 5.0, 4.0, fcoat, group=13)
    p.blob(27, 60.5 - 2 * st, 3.0, 1.8, fcoat, group=12)
    p.blob(37, 60.5 - 2 * (1 - st), 3.0, 1.8, fcoat, group=13)
    p.blob(32, 39, 8.0, 9.0, fcoat, group=1)                                           # back
    p.blob(27, 47, 6.4, 6.8, fcoat, group=8)                                           # haunches
    p.blob(37, 47, 6.4, 6.8, fcoat, group=9)
    p.limb(bez((32, 44), (33, 34), (38 + 2 * st, 27)), 5.0, 3.4, fcoat, group=5)      # tail
    comet(p, bez((38 + 2 * st, 27), (45, 17.5), (28, 16), n=16), 3.4, 1.2)


def nostail(p, view, phase):
    if view in ("front", "side", "icon"):
        _front(p, phase if view != "icon" else 0)
    elif view == "back":
        _back(p)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)


MONS = [
    # icon palette 3 keeps the coat white, the shadows sea-blue and the comet gold
    Mon("Nostail", COLORS, SHINY, nostail, foot="paw", icon_pal=3),
]
