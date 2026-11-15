"""Lycaon line: Lykopup, Lykanax (Dark). King Lycaon of Arcadia, who served
Zeus a feast of human flesh and was turned into the first werewolf."""
from mon_lib import C, Mat, Mon, bez, bez3, ribbon

INK = C.ink

# --------------------------------------------------------------------------
# Shared fur: marble-gray coat shaded toward cypress, black-figure ink fur on
# the ruff and saddle, a limestone belly, moon-yellow eyes
# --------------------------------------------------------------------------

LYKOPUP_COLORS = [
    ("ink", INK),
    ("dk0", (40, 40, 48)), ("dk1", (72, 72, 80)),
    ("coat0", (80, 96, 96)), ("coat1", (136, 144, 144)), ("coat2", (184, 184, 184)), ("coat3", (224, 224, 216)),
    ("lime0", (176, 152, 112)), ("lime1", (216, 200, 160)),
    ("eye0", (200, 160, 48)), ("eye1", (248, 232, 128)),
    ("white", C.white),
    ("gum", (152, 56, 64)),
]
LYKOPUP_SHINY = {
    # moonlight on snow
    "dk0": (88, 96, 128), "dk1": (128, 136, 168),
    "coat0": (136, 152, 176), "coat1": (184, 192, 208), "coat2": (216, 224, 232), "coat3": (248, 248, 248),
    "lime0": (192, 192, 208), "lime1": (232, 232, 240),
}

p_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.18, 0.44, 0.7])
p_dark = Mat(["dk0", "dk1", "coat0"], line="ink", cuts=[0.26, 0.62])
p_pale = Mat(["lime0", "lime1"], line="coat1", cuts=[0.5])


def _tuft(p, base, tip, w, mat, **kw):
    """A pointed fur tuft from base to tip, bowed a little."""
    return p.lens(base, tip, w, mat, fat=0.3, **kw)


def lykopup(p, view, phase):
    # the battle front and back are hand-finished in the art files (the ruff's
    # five points redrawn there); this draft feeds the icon and the follower
    if view in ("front", "side", "icon"):
        walk = view == "side" and phase == 1
        L = 1 if (phase == 1 and view == "front") else 0

        # tail, tucked low behind the hind legs
        p.limb(bez3((46, 49), (51.5, 50), (53, 55), (50.5, 59)), 5.6, 3.2, p_coat, bias=0.3, group=9)

        # far legs, in shade
        ff = [(31, 53), (29.5, 57), (29, 59.5)] if not walk else [(31, 53), (31.5, 57), (31.5, 59.5)]
        fh = [(46, 52), (48.5, 56), (47.5, 59.5)] if not walk else [(46, 52), (45, 56), (44, 59.5)]
        p.limb(ff, 4.6, 4.0, p_coat, bias=0.35, group=10)
        p.blob(ff[-1][0] - 0.6, 59.8, 2.8, 1.6, p_coat, bias=0.35, group=10)
        p.limb(fh, 4.8, 3.8, p_coat, bias=0.35, group=11)
        p.blob(fh[-1][0] - 0.6, 59.8, 2.8, 1.6, p_coat, bias=0.35, group=11)

        # body, crouched low with the rump a little higher
        body = p.blob(39.5, 51.5, 9.0, 5.6, p_coat, ang=-6, group=1)
        p.blob(45, 50.5, 4.4, 4.4, p_coat, group=1)
        p.blob(38.5, 55.6, 7.0, 2.0, p_pale, clip=[body], group=2)

        # the ruff: a shaggy collar of black-figure fur, far too big for the
        # pup, sitting up in five points behind the lowered head
        p.blob(34, 45, 8.4, 8.0, p_dark, group=5)
        for base, tip, w, bend in (((29.5, 41), (27.5, 30.5 - L), 7.0, 0.8), ((33, 40), (34, 28.5 - L), 7.6, 0.6),
                                   ((36.5, 41), (41, 29.5 - L), 7.4, 0.4), ((39, 43), (46, 34 - L), 7.0, 0.2),
                                   ((40.5, 46.5), (48.5, 40.5 - L), 6.0, -0.2)):
            _tuft(p, base, tip, w, p_dark, bend=bend, group=5)

        # near hind leg: haunch, hock, paw
        nh = [(44.5, 52), (46.5, 56), (45, 59.5)] if not walk else [(44.5, 52), (42, 56), (40.5, 59.5)]
        p.blob(44, 51.5, 5.0, 4.8, p_coat, group=13)
        p.limb(nh, 5.0, 4.0, p_coat, group=13)
        p.blob(nh[-1][0] - 1, 59.6, 3.4, 2.0, p_coat, group=13)

        # far ear, behind the head
        p.poly(bez3((26.5, 38 - L), (27.5, 33 - L), (29.5, 31 - L), (31.5, 30.5 - L)) + [(31, 36 - L), (29.5, 39 - L)],
               p_coat, group=6, bias=0.2)
        # head: low, big and round, with a short tapering muzzle
        p.blob(24.5, 43.5 - L, 8.6, 7.8, p_coat, group=3, bias=-0.1)
        p.limb(bez((19, 46.5 - L), (16.5, 47.5 - L), (14, 47.5 - L)), 7.2, 4.8, p_coat, group=3, bias=-0.1)
        p.blob(18.5, 50 - L, 4.0, 1.8, p_pale, group=4)
        # cheek fluff under the jaw
        _tuft(p, (24, 48.5 - L), (21.5, 53.5 - L), 5.0, p_pale, group=8)
        _tuft(p, (27.5, 48 - L), (27, 54 - L), 5.2, p_pale, group=8)
        # near ear, pricked
        p.poly(bez3((17.5, 39 - L), (17, 34 - L), (18.5, 31 - L), (20.5, 29.5 - L)) + bez((20.5, 29.5 - L), (23.5, 32 - L), (25, 37 - L)),
               p_coat, group=7)

        # near front leg, crouched forward
        nf = [(26.5, 52), (23.5, 56), (22, 59.5)] if not walk else [(26.5, 52), (26.5, 56), (26.5, 59.5)]
        p.limb(nf, 5.4, 4.4, p_coat, group=12)
        p.blob(nf[-1][0] - 1.2, 59.6, 3.6, 2.0, p_coat, group=12)

        if p.big:
            # eye: moon-yellow under a heavy brow
            p.patch(16, 40 - L, ["222222", "1111111", "1ffe11", "1eff1.", ".e1f1.", "..11.."],
                    {"1": "ink", "2": "coat0", "e": "eye0", "f": "eye1"})
            p.px(17, 42 - L, "white")
            p.pxs([(12, 46 - L), (13, 46 - L), (12, 47 - L)], "ink")       # nose
            p.stroke([(14, 49 - L), (18, 49 - L)], "coat0")             # mouth
            p.pxs([(19, 34 - L), (20, 35 - L), (20, 36 - L)], "dk0")     # inner ear
        else:
            p.px(17.5, 42.5 - L, "eye1")
            p.px(12.5, 46.5 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the pup's hunched back, the ruff from behind
        # sitting up in its five points, the head turned right in profile,
        # staring; the tail tucked low
        p.limb(bez3((14, 66), (5, 62), (4, 54), (8, 49)), 8.0, 5.0, p_coat, group=20)
        _tuft(p, (7, 51), (6.5, 44.5), 5.0, p_dark, bend=-0.6, group=20)
        p.blob(28, 61, 22, 12, p_coat, group=1)
        p.blob(36, 50, 12, 9, p_coat, group=1)
        # the far side of the ruff, behind the head
        for base, tip, w, bend in (((46, 40), (55, 29), 7.6, -0.8), ((47, 45), (58, 40), 7.0, -0.4)):
            _tuft(p, base, tip, w, p_dark, bend=bend, group=4)
        # the head in right profile, low and staring
        p.poly(bez3((43, 32), (44, 24), (47, 20.5), (50, 19.5)) + [(52.5, 26), (51, 31)], p_coat, group=5, bias=0.12)
        p.blob(46.5, 37, 9.4, 8.6, p_coat, group=3, bias=-0.08)
        p.limb(bez((51, 40), (55, 41.5), (59.5, 41.5)), 8.4, 5.6, p_coat, group=3, bias=-0.08)
        p.blob(54, 45, 4.8, 2.0, p_pale, group=6)
        _tuft(p, (45, 44), (49, 50), 5.6, p_pale, group=6)
        if p.big:
            p.patch(48, 33, ["222222", ".1111111", "..1cb1b1", "..1bb1a1", "...1aa1.", "....11.."],
                    {"1": "ink", "2": "coat0", "b": "eye1", "a": "eye0", "c": "white"})
            p.pxs([(60, 40), (61, 40), (61, 41)], "ink")
            p.stroke([(55, 44), (59, 44)], "coat0")
        return

    if view in ("down", "up"):
        # follower: the pup slinking toward or away from the camera, the
        # ruff standing round its head like a little crown
        st = phase
        p.limb([(27, 52), (26.5, 59.5 - 2 * st)], 5.0, 4.4, p_coat, group=12, bias=0.1 if view == "up" else 0)
        p.limb([(37, 52), (37.5, 59.5 - 2 * (1 - st))], 5.0, 4.4, p_coat, group=13, bias=0.1 if view == "up" else 0)
        p.blob(26.5, 60 - 2 * st, 3.2, 2.0, p_coat, group=12)
        p.blob(37.5, 60 - 2 * (1 - st), 3.2, 2.0, p_coat, group=13)
        p.blob(32, 50, 9.2, 8.0, p_coat, group=1)
        if view == "down":
            p.blob(32, 54, 4.6, 4.0, p_pale, group=2)
            # the ruff, five points standing round the head
            p.blob(32, 41, 11, 7, p_dark, group=5)
            for tip, w in (((19, 33), 6.4), ((24, 28.5), 7.0), ((32, 27), 7.4), ((40, 28.5), 7.0), ((45, 33), 6.4)):
                _tuft(p, (32 + (tip[0] - 32) * 0.35, 38), tip, w, p_dark, group=5)
            p.poly([(23, 36), (21, 26), (28.5, 31)], p_coat, group=6)
            p.poly([(41, 36), (43, 26), (35.5, 31)], p_coat, group=6)
            p.blob(32, 38, 8.6, 7.4, p_coat, group=3)
            p.blob(32, 43, 4.2, 3.4, p_coat, group=4)
            p.blob(32, 45, 3.2, 1.6, p_pale, group=4)
            p.eye(26, 37, 3, 4, iris="eye1", shine="white", shine_at=(0, 1))
            p.eye(35, 37, 3, 4, iris="eye1", shine="white", shine_at=(2, 1))
            if p.big:
                p.pxs([(26, 36), (27, 36), (28, 36), (35, 36), (36, 36), (37, 36)], "coat0")
                p.pxs([(22, 29), (23, 31), (42, 29), (41, 31)], "dk0")
            p.pxs([(31, 42), (32, 42)], "ink")
        else:
            # from behind: the tail hanging low, hackles down the back, the
            # ruff's points round the back of the head, the ears above
            p.limb(bez3((32, 50), (34, 55), (34.5, 59), (32, 62)), 5.4, 3.0, p_coat, group=20)
            for tip in ((26, 50), (32, 53), (38, 50)):
                _tuft(p, (32 + (tip[0] - 32) * 0.3, 44), tip, 4.6, p_dark, group=7)
            for tip, w in (((18.5, 36), 6.4), ((22.5, 30.5), 7.0), ((41.5, 30.5), 7.0), ((45.5, 36), 6.4)):
                _tuft(p, (32 + (tip[0] - 32) * 0.4, 43), tip, w, p_dark, group=5)
            p.poly([(23, 36), (21, 26), (28.5, 31)], p_coat, group=6, bias=0.1)
            p.poly([(41, 36), (43, 26), (35.5, 31)], p_coat, group=6, bias=0.1)
            p.blob(32, 37, 8.0, 7.0, p_coat, group=3)
            p.blob(32, 45.5, 10, 4.6, p_dark, group=7)
            _tuft(p, (32, 44), (32, 37.5), 6.0, p_dark, group=7)
        return

# --------------------------------------------------------------------------
# Lykanax, the wolf-king
# --------------------------------------------------------------------------

LYKANAX_COLORS = [
    ("ink", INK),
    ("dk0", (40, 40, 48)), ("dk1", (72, 72, 80)),
    ("coat0", (80, 96, 96)), ("coat1", (136, 144, 144)), ("coat2", (184, 184, 184)), ("coat3", (224, 224, 216)),
    # the torn royal cloak, terracotta
    ("cloak0", (112, 40, 24)), ("cloak1", (176, 80, 48)), ("cloak2", (224, 136, 88)),
    # moon-yellow eyes and the gold of the cloak's clasp
    ("gold0", (192, 136, 40)), ("gold1", (248, 224, 112)),
    ("lime", (216, 200, 160)),
    ("white", C.white),
    ("gum", (152, 56, 64)),
]
LYKANAX_SHINY = {
    # moon-white fur and a sun-gold cloak
    "dk0": (88, 96, 128), "dk1": (128, 136, 168),
    "coat0": (136, 152, 176), "coat1": (184, 192, 208), "coat2": (216, 224, 232), "coat3": (248, 248, 248),
    "cloak0": (144, 88, 24), "cloak1": (216, 160, 48), "cloak2": (248, 216, 112),
    "lime": (232, 232, 240),
}

x_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.18, 0.44, 0.7])
x_dark = Mat(["dk0", "dk1", "coat0"], line="ink", cuts=[0.38, 0.78])
x_pale = Mat(["coat2", "lime"], line="coat1", cuts=[0.5])
x_ruff = Mat(["coat1", "coat2", "coat3", "lime"], line="coat1", cuts=[0.2, 0.42, 0.66])
x_cloak = Mat(["cloak0", "cloak1", "cloak2"], line="cloak0", cuts=[0.3, 0.66])
x_gold = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])


def _spike(p, base, tip, w, mat, **kw):
    """A stiff crown point: a lens fat at its base, straight to the tip."""
    return p.lens(base, tip, w, mat, fat=0.22, **kw)


def lykanax(p, view, phase):
    # the battle front and back are hand-finished in the art files (the crown,
    # the meander border, the clasp and the hanging paws); this draft feeds
    # the icon and the follower
    if view in ("front", "side", "icon"):
        sw = 1 if phase == 1 else 0     # frame 2: the swipe follows through, the cloak billows

        # tail, low behind the legs, out under the cloak's hem
        p.limb(bez3((40, 44), (48, 49), (53, 57), (59, 56 - 2 * sw)), 8.4, 4.0, x_coat, bias=0.25, group=9)
        # the cloak, hanging from hunched shoulders and billowing behind,
        # torn at the hem into long tatters
        b = 1.5 * sw
        hem = [(60 + b, 51 - b), (56.5 + b, 47 - b), (55 + b, 56 - b), (52 + b, 48.5 - b), (49 + b, 55 - b),
               (46.5, 48.5), (44, 53), (41.5, 46)]
        p.poly(bez3((33, 15), (43, 14), (51, 20), (55, 31)) + bez((55, 31), (58, 42), (60 + b, 51 - b))[1:] + hem
               + [(38, 34)], x_cloak, group=8)
        for path in (bez((45, 22), (49, 34), (51, 48)), bez((49.5, 24), (54, 36), (56.5, 47))):
            p.shade(ribbon(path, lambda t: 1.4 + t), 0.3)

        # far arm, braced low with its claws spread
        fw = [(35, 23), (31, 33.5), (20, 40 - 2 * sw)]
        p.limb(fw, 7.2, 5.6, x_coat, bias=0.3, group=20)
        p.blob(17.5, 41.5 - 2 * sw, 3.6, 3.0, x_coat, bias=0.3, group=20)
        for tip in ((12.5, 44 - 2 * sw), (14.5, 46.5 - 2 * sw), (17.5, 47 - 2 * sw)):
            p.taper([(17, 42 - 2 * sw), tip], 2.0, x_coat, bias=0.3, group=20)
        # far hind leg, braced back
        fl = [(39, 42), (41, 48.5), (45, 54), (43, 59.8)]
        p.limb(fl[:2], 9.4, 6.6, x_coat, bias=0.3, group=10)
        p.limb(fl[1:], 5.8, 4.4, x_coat, bias=0.3, group=10)
        p.blob(41.5, 59.9, 4.4, 1.8, x_coat, bias=0.3, group=10)

        # torso: a barrel chest thrown forward over a narrow waist
        body = p.limb(bez((28, 28), (32, 36), (36, 41)), 17, 12, x_coat, group=1)
        p.blob(26.5, 29, 11, 10, x_coat, group=1)
        p.blob(36, 41, 6.4, 6.0, x_coat, group=1)
        p.limb(bez((19, 30), (23, 37), (30, 41.5)), 7.0, 5.4, x_pale, clip=[body], group=2)
        # the black-figure mantle over broad, hunched shoulders, its fur
        # spilling onto the chest and over the cloak's edge in tufts
        p.poly(bez3((19, 20), (27, 13), (40, 14), (45, 23)) + [(44, 28)], x_dark, group=1)
        for base, tip, w in (((41, 21), (45.5, 28.5), 5.0), ((43, 24), (46.5, 32), 4.4), ((38, 23), (40.5, 30), 4.6),
                             ((22, 21), (19.5, 26), 4.6)):
            _tuft(p, base, tip, w, x_dark, group=1)

        # near hind leg, bearing the weight: a heavy thigh, the knee thrust
        # forward, the hock back, a long clawed paw
        nl = [(30, 44), (22.5, 50.5), (27.5, 55.5), (21, 60)]
        p.blob(30, 45, 8.6, 7.6, x_coat, group=11)
        p.limb(nl[:2], 11, 7.4, x_coat, group=11)
        p.limb(nl[1:], 6.4, 4.6, x_coat, group=11)
        p.blob(19.5, 60.1, 5.2, 1.9, x_coat, group=11)

        # a shaggy pale ruff spilling down the barrel chest
        for base, tip, w, bend in (((22, 23), (18.5, 32), 5.6, 0.8), ((25.5, 23), (23.5, 34), 6.0, 0.5),
                                   ((29, 24), (28.5, 34.5), 6.0, 0.0), ((32.5, 25), (34, 33), 5.2, -0.4)):
            _tuft(p, base, tip, w, x_ruff, bend=bend, group=14)
        # fur jutting from the back of the thigh, the belly and the knee
        _tuft(p, (35, 42), (40.5, 51), 5.4, x_coat, bend=-0.6, group=11)
        _tuft(p, (32, 46), (36.5, 53.5), 4.8, x_coat, bend=-0.4, group=11)
        _tuft(p, (24, 48), (19.5, 47), 4.4, x_coat, bend=0.6, group=11)
        _tuft(p, (21, 37), (17, 41.5), 4.4, x_coat, bend=0.4, group=1)

        # the crown-ruff: five stiff points of black-figure fur standing up
        # round the neck; the four behind the head first
        for base, tip, w in (((32.5, 16), (35, 2), 6.6), ((36.5, 16), (41.5, 2.5), 7.0),
                             ((39.5, 17.5), (47, 6.5 - sw), 6.8), ((41, 20.5), (50, 13.5 - sw), 6.0)):
            _spike(p, base, tip, w, x_dark, group=5)
        p.blob(34, 19.5, 8.6, 5.4, x_dark, group=5)

        # head thrown back mid-howl: the jaws open to the sky
        p.limb(bez((29, 23), (27, 18), (25.5, 14.5)), 9.6, 8.4, x_coat, group=3)
        p.poly([(22, 13), (15.5, 3.5), (12.5, 11.5 - sw)], Mat(["gum"]), group=30)
        p.blob(25.5, 12, 6.6, 5.8, x_coat, group=3)
        p.limb(bez((22, 9.5), (18.5, 5.5), (16, 2.5)), 6.8, 4.4, x_coat, group=3)
        p.limb(bez((22, 15.5), (17, 13.5 + sw / 2), (12.5, 11.5 + sw)), 4.8, 2.8, x_pale, group=4)
        # the ear laid back
        p.poly(bez3((26.5, 7.5), (28, 4.5), (30.5, 3), (33.5, 3)) + [(31, 9)], x_coat, group=7)
        # the fifth point, in front of the throat
        _spike(p, (26.5, 19.5), (18, 17), 6.4, x_dark, group=12)
        _tuft(p, (28, 22.5), (21.5, 22.5), 5.0, x_dark, group=12)

        # near arm raised mid-swipe: the elbow out, the claws fanned; in frame
        # 2 the swipe comes down across the body
        if sw:
            nw, pc, claws = [(23, 23), (13.5, 30), (7, 27)], (5.5, 28.5), ((1.5, 31), (2.5, 34.5), (5.5, 36))
        else:
            nw, pc, claws = [(23, 23), (13, 27.5), (7.5, 20)], (6, 17.5), ((2, 12), (5, 11), (8.5, 12))
        p.blob(21.5, 23.5, 6.8, 5.8, x_coat, group=21)
        p.limb(nw, 8.0, 6.0, x_coat, group=21)
        p.blob(pc[0], pc[1], 3.8, 3.4, x_coat, group=21)
        for tip in claws:
            p.taper([pc, tip], 2.4, x_coat, group=21)
        _tuft(p, (14, 29 + 2 * sw), (12, 34.5 + 2 * sw), 4.4, x_coat, bend=0.4, group=21)

        # the cloak drawn over the near shoulder, pinned with a gold clasp
        p.poly(bez3((26, 20), (30, 16), (36, 16), (39, 20)) + [(37, 24.5), (30.5, 24)], x_cloak, group=22)
        p.circle(28.5, 22.5, 2.2, x_gold, group=23)

        if p.big:
            p.patch(21, 8, ["2222", "11111", "1ff1.", ".11.."], {"1": "ink", "2": "coat0", "f": "gold1"})
            p.pxs([(15, 2), (16, 2)], "ink")
        else:
            p.px(22.5, 9.5, "gold1")
        return

    if view == "back":
        # over the shoulder: the broad back under the torn cloak, the crown
        # standing round the neck as a ring of points, the head turned right
        # in profile and thrown back to howl
        # the crown's points on the far side, behind the head
        for base, tip, w in (((43, 27), (46, 9.5), 7.0), ((46.5, 29.5), (55.5, 23), 6.6)):
            _spike(p, base, tip, w, x_dark, group=4)
        # neck, head, jaws open to the sky
        p.limb(bez((38, 38), (41, 30), (44, 23)), 13, 11, x_coat, group=3)
        p.poly([(49, 19), (58.5, 5.5), (60.5, 13)], Mat(["gum"]), group=30)
        p.blob(46, 19, 7.6, 7.0, x_coat, group=3)
        p.limb(bez((49.5, 15.5), (53.5, 10.5), (57, 5)), 8.4, 5.6, x_coat, group=3)
        p.limb(bez((50.5, 21.5), (56, 17), (61, 13)), 5.4, 3.2, x_pale, group=6)
        p.poly(bez3((43, 13), (41, 9), (38, 8), (35, 9)) + [(39, 14), (42.5, 16.5)], x_coat, group=7, bias=0.1)
        # shoulders and back, cropped by the frame
        p.blob(30, 60, 26, 18, x_coat, group=1)
        p.blob(20, 45, 12, 10, x_coat, group=1)
        # the near arm, the elbow out at the left
        p.limb(bez((14, 44), (6, 51), (5.5, 62)), 12, 10, x_coat, group=21)
        # the cloak hanging square from the shoulders, torn at both edges
        p.poly([(11, 43), (17, 37), (26, 34), (36, 33.5), (45, 35), (51, 39), (54, 46), (52, 49.5), (56, 52.5),
                (55, 57), (58, 61), (57, 66), (13, 66), (14.5, 61), (10, 58.5), (13.5, 55), (9, 51.5), (12.5, 48)],
               x_cloak, group=8)
        # the black-figure mantle over the shoulders, its fur spilling onto
        # the cloak in tufts
        p.poly(bez3((13, 43), (20, 34), (34, 31), (46, 35)) + [(49, 39)], x_dark, group=9)
        for base, tip, w in (((17, 40), (15.5, 46), 4.6), ((22, 38), (21, 45.5), 5.0), ((28, 37), (28, 44.5), 5.0),
                             ((34, 37), (35, 44), 5.0), ((40, 37.5), (42.5, 43.5), 4.6), ((45, 38), (48.5, 42.5), 4.0)):
            _tuft(p, base, tip, w, x_dark, group=9)
        # the near side of the crown: three points rising round the neck
        for base, tip, w in (((27, 34), (21, 17), 7.6), ((32, 32), (28.5, 11), 8.0), ((37.5, 31), (36.5, 8), 7.8)):
            _spike(p, base, tip, w, x_dark, group=10)
        p.blob(35, 34, 11.5, 5.0, x_dark, group=10)
        if p.big:
            p.patch(46, 15, ["2222", "11111", ".1ff1", "..11."], {"1": "ink", "2": "coat0", "f": "gold1"})
            p.pxs([(58, 4), (59, 4)], "ink")
        return

    if view in ("down", "up"):
        # follower: the wolf-king on two legs, the cloak at his back, the
        # crown-ruff standing round his head
        st = phase
        p.limb([(28, 47), (27, 54), (27.5, 60 - 2 * st)], 6.0, 4.4, x_coat, group=12)
        p.limb([(36, 47), (37, 54), (36.5, 60 - 2 * (1 - st))], 6.0, 4.4, x_coat, group=13)
        p.blob(26.5, 60.4 - 2 * st, 3.4, 1.8, x_coat, group=12)
        p.blob(37.5, 60.4 - 2 * (1 - st), 3.4, 1.8, x_coat, group=13)
        if view == "down":
            p.poly([(22, 30), (42, 30), (47, 52 + st), (43, 50), (40, 53), (32, 51), (24, 53), (21, 50), (17, 52 + (1 - st))],
                   x_cloak, group=8)
            p.blob(32, 40, 8.6, 10, x_coat, group=1)
            p.blob(32, 42, 4.6, 7, x_pale, group=2)
            p.limb([(24, 33), (21, 41), (24, 45)], 5.2, 4.2, x_coat, group=20)
            p.limb([(40, 33), (43, 41), (40, 45)], 5.2, 4.2, x_coat, group=21)
            for tip, w in (((17, 22), 6.4), ((23, 15), 7.0), ((32, 12.5), 7.4), ((41, 15), 7.0), ((47, 22), 6.4)):
                _spike(p, (32 + (tip[0] - 32) * 0.4, 28), tip, w, x_dark, group=5)
            p.blob(32, 29, 11, 5, x_dark, group=5)
            p.poly([(24, 24), (22, 13), (29, 19)], x_coat, group=6)
            p.poly([(40, 24), (42, 13), (35, 19)], x_coat, group=6)
            p.blob(32, 23, 7.6, 7, x_coat, group=3)
            p.blob(32, 28, 4.0, 3.6, x_coat, group=4)
            p.blob(32, 30, 3.0, 1.6, x_pale, group=4)
            p.eye(26, 22, 3, 4, iris="gold1", shine="white", shine_at=(0, 1))
            p.eye(35, 22, 3, 4, iris="gold1", shine="white", shine_at=(2, 1))
            p.pxs([(31, 27), (32, 27)], "ink")
            p.circle(32, 33, 1.8, x_gold, group=23)
        else:
            p.limb(bez3((32, 48), (35, 53), (35, 58), (32, 61)), 6.0, 3.4, x_coat, group=20)
            p.limb([(24, 33), (21, 41), (23, 45)], 5.2, 4.2, x_coat, group=20)
            p.limb([(40, 33), (43, 41), (41, 45)], 5.2, 4.2, x_coat, group=21)
            p.poly(bez3((23, 29), (28, 27), (36, 27), (41, 29)) + [(43, 40), (45, 50 + st), (41, 48), (38, 51.5), (34.5, 48.5),
                                                                  (30, 51.5), (26, 48.5), (22.5, 50.5), (19, 50 + (1 - st)), (21, 40)],
                   x_cloak, group=8)
            for tip, w in (((17, 22), 6.4), ((23, 15), 7.0), ((41, 15), 7.0), ((47, 22), 6.4)):
                _spike(p, (32 + (tip[0] - 32) * 0.4, 28), tip, w, x_dark, group=5)
            p.poly([(24, 24), (22, 13), (29, 19)], x_coat, group=6, bias=0.1)
            p.poly([(40, 24), (42, 13), (35, 19)], x_coat, group=6, bias=0.1)
            p.blob(32, 22, 7.2, 6.6, x_coat, group=3)
            p.blob(32, 29.5, 10.5, 4.6, x_dark, group=9)
            _spike(p, (32, 28), (32, 17), 7.0, x_dark, group=9)
        return


MONS = [
    Mon("Lykopup", LYKOPUP_COLORS, LYKOPUP_SHINY, lykopup, foot="paw"),
    Mon("Lykanax", LYKANAX_COLORS, LYKANAX_SHINY, lykanax, foot="bigpaw"),
]
