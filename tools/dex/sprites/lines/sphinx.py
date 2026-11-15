"""Sphinx line: Enigmaw (Psychic/Fighting). The Sphinx on her rock outside
Thebes, who asked every traveler a riddle and strangled those who failed;
her name comes from sphingo, "to squeeze"."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

ENIGMAW_COLORS = [
    ("ink", INK),
    # limestone-tan coat with sun-gold highlights
    ("c0", (120, 80, 48)), ("c1", (176, 128, 72)), ("c2", (216, 176, 112)), ("c3", (240, 208, 128)),
    # eagle wings
    ("w0", (96, 64, 48)), ("w1", (152, 112, 72)), ("w2", (208, 168, 112)),
    # terracotta: the bars on the wings and the braided hair
    ("t0", (128, 48, 32)), ("t1", (192, 96, 56)),
    # pale limestone: the rock, and the marble of her face
    ("s0", (136, 120, 112)), ("s1", (184, 168, 152)), ("s2", (224, 208, 184)), ("s3", (248, 240, 224)),
    # the knowing, Psychic-violet eyes
    ("eye", (128, 72, 176)),
]
ENIGMAW_SHINY = {
    # a marble-white coat and black-figure wings
    "c0": (144, 136, 136), "c1": (192, 184, 176), "c2": (224, 216, 208), "c3": (248, 248, 240),
    "w0": (32, 32, 40), "w1": (64, 56, 64), "w2": (104, 96, 104),
}

coat = Mat(["c0", "c1", "c2", "c3"], line="c0", cuts=[0.18, 0.44, 0.72])
belly = Mat(["c1", "c2", "c3"], line="c0", cuts=[0.36, 0.66])
wing = Mat(["w0", "w1", "w2"], line="w0", cuts=[0.26, 0.56])
hair = Mat(["t0", "t1"], line="t0", cuts=[0.5])
bar = Mat(["t0", "t1"], line="t0", cuts=[0.45])
face = Mat(["s1", "s2", "s3"], line="s0", cuts=[0.3, 0.62])
rock = Mat(["s0", "s1", "s2", "s3"], line="s0", cuts=[0.2, 0.46, 0.74])
gold = Mat(["c2", "c3"], line="c1", cuts=[0.55])
muzzle = Mat(["s1", "s2", "s3"], line="c1", cuts=[0.3, 0.62])
claw = Mat(["s0", "s1"], line="s0", cuts=[0.5])


def _braid(p, top, bot, w=2.6, n=None, **kw):
    """A beaded braid hanging from top to bot: a chain of small rounded
    terracotta segments, the archaic Greek way of drawing hair."""
    dx, dy = bot[0] - top[0], bot[1] - top[1]
    d = math.hypot(dx, dy)
    n = n or max(2, int(d / 2.4))
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        a = (top[0] + dx * t0, top[1] + dy * t0)
        b = (top[0] + dx * t1, top[1] + dy * t1)
        p.lens(a, b, w, hair, fat=0.5, **kw)


def _lion_head(p, x, y, L=0):
    """Her head, 3/4 facing left, its skull centred on (x, y): a lioness's
    face - short muzzle, nose pad, cat mouth, almond eyes - framed by the
    archaic banded tresses worn as a mane-headdress under a gold fillet, the
    way the Naxian Sphinx wears her hair."""
    Y = y - L
    # the tresses falling behind the neck to the shoulders, and the mane
    # massed behind the head
    _braid(p, (x + 7, Y + 3), (x + 11.5, Y + 19), 3.6, group=7, bias=0.25)
    _braid(p, (x + 5, Y + 5), (x + 8.5, Y + 20), 3.6, group=7, bias=0.18)
    p.blob(x + 3.5, Y + 1.5, 9, 9.4, hair, group=8)
    # rounded ears standing out of the mane
    p.lens((x - 4, Y - 4), (x - 6, Y - 9.5), 4.6, coat, bend=0.6, bias=0.22, group=14)
    p.lens((x + 3.5, Y - 4.5), (x + 6, Y - 10.5), 5.2, coat, bend=-0.6, group=13)
    # skull and cheeks, then the short muzzle and chin
    p.blob(x, Y, 7, 6.4, coat, group=9)
    p.blob(x - 1, Y + 4.5, 6.2, 4, coat, group=9)
    p.blob(x - 6, Y + 4, 4.4, 3.1, muzzle, ang=8, group=10)
    p.blob(x - 5.5, Y + 7, 2.8, 1.6, muzzle, group=10)
    # the gold fillet across her brow, between the ears
    p.limb(bez((x - 7.5, Y - 2.5), (x - 1, Y - 6.5), (x + 7.5, Y - 4.5)), 2.2, 2.0, gold, group=12)
    # a tress falling in front of the near shoulder
    _braid(p, (x + 3.5, Y + 7.5), (x + 5, Y + 19), 3.0, group=11)
    if p.big:
        leg = {"1": "ink", "f": "eye", "w": "s3", "n": "t0", "m": "t1", "d": "c0"}
        # almond cat eyes, violet, with slit pupils
        p.patch(int(x - 1), int(Y), [" 1111 ", "1wf1f1", "1ff1f1", " 1111 "], leg)
        p.patch(int(x - 7), int(Y), [" 111", "1f1f", "1f11", " 11 "], leg)
        # the nose pad, and a cat's mouth curving into the archaic smile
        p.patch(int(x - 10), int(Y + 2), ["1mn1", " 11 ", "  d ", "  d  d", "   dd "], leg)
    else:
        leg = {"1": "ink", "f": "eye", "n": "t0"}
        p.patch(0, 0, [], leg, small=(x - 6, Y, ["1f"]))
        p.patch(0, 0, [], leg, small=(x + 0.5, Y, ["1f1"]))
        p.patch(0, 0, [], leg, small=(x - 9.5, Y + 2.5, ["n"]))


def _taper_braid(p, top, bot, w, **kw):
    """A tress hanging from top and tapering to a point at bot: beaded
    segments that narrow as they fall."""
    dx, dy = bot[0] - top[0], bot[1] - top[1]
    n = max(3, int(math.hypot(dx, dy) / 2.6))
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        ww = w * (1 - 0.7 * t0)
        p.lens((top[0] + dx * t0, top[1] + dy * t0), (top[0] + dx * t1, top[1] + dy * t1), ww, hair, fat=0.5, **kw)


def _lion_profile(p, x, y, k=1.0):
    """Her head in right profile, skull centred on (x, y), scaled by k: the
    lioness's muzzle, nose and ear, the gold fillet and the mane-headdress
    behind."""
    def q(dx, dy):
        return (x + dx * k, y + dy * k)
    p.blob(*q(-4, 2), 7.5 * k, 8.5 * k, hair, group=8)
    p.lens(q(-1, -4.5), q(-2.5, -10.5), 5.2 * k, coat, bend=0.6, group=13)
    p.blob(*q(1, 0), 6.6 * k, 6.2 * k, coat, group=9)
    p.blob(*q(1.5, 4.6), 5.4 * k, 3.6 * k, coat, group=9)
    p.blob(*q(7, 3.6), 3.8 * k, 2.8 * k, muzzle, ang=-6, group=10)
    p.blob(*q(6, 6.6), 2.6 * k, 1.6 * k, muzzle, group=10)
    p.limb(bez(q(-6, -1), q(-1, -5.5), q(6, -4)), 2.4 * k, 2.2 * k, gold, group=12)
    if p.big:
        leg = {"1": "ink", "f": "eye", "w": "s3", "n": "t0", "m": "t1", "d": "c0"}
        ex, ey = q(2, -1)
        p.patch(int(ex), int(ey), [" 1111", "1f1ffw", "1f1ff1", " 1111"], leg)
        nx, ny = q(9.5, 2)
        p.patch(int(nx), int(ny), [" 11", "1mn", " 1d", "  d", " dd"], leg)


def _paw(p, x, y, w=4.2, far=False):
    """A lion's forepaw resting on the rock, toes toward the viewer."""
    p.blob(x, y, w / 2 + 0.6, 1.9, coat, bias=0.3 if far else 0.0)
    if p.big:
        for i in range(3):
            p.px(x - w / 2 + 1.2 + i * (w - 1.4) / 2, y + 0.6, "c0")


def _tail(p, L=0, sq=0.0):
    """The tail rising from the rump and curling into a question-mark hook;
    sq tightens the coil."""
    path = bez3((51, 47), (61, 45), (61 - sq, 31), (57.5 - sq, 24.5 - L)) + \
        bez3((57.5 - sq, 24.5 - L), (55 - sq, 20.5 - L), (50.5 + sq, 22.5 - L), (51.5 + sq, 27.5 - L))[1:]
    p.limb(path, 4.2, 3.0, coat, group=25)
    # the tuft at its tip, hanging in the hook
    p.drop((52 + sq, 34 - L), 52 + sq, 30 - L, 2.6, Mat(["c0", "c1"], line="c0", cuts=[0.55]), group=26)


def _wing(p, L=0, near=True):
    """The archaic sickle wing, as on the Naxian Sphinx at Delphi: rising
    from the shoulder behind the back and curling forward at its tip. Four
    bold groups: a pale band of coverts along the leading edge with a
    terracotta stripe behind it, the plain inner wing, and three broad
    primaries fanning out behind with one terracotta bar across them."""
    up = L
    # the primaries, behind the wing, their shaped tips fanning out
    prim = []
    for i, (a, b, w) in enumerate((((40, 11 - up), (50.5, 13 - up), 6.2), ((41, 19), (52.5, 23.5), 6.6),
                                   ((40.5, 27), (50, 34), 6.2))):
        prim.append(p.lens(a, b, w, wing, bend=-0.8, fat=0.32, group=50 + i, bias=0.04 * i - 0.06))
    if p.big:
        p.limb(bez3((45.5, 10 - up), (49, 17), (48.5, 26), (45.5, 33)), 2.4, 2.2, bar, clip=prim, group=60, noline=True)
    lead = bez3((29.5, 32), (30, 21), (35, 10 - up), (42, 5.5 - up))
    curl = bez((42, 5.5 - up), (40, 2.6 - up), (37, 4.4 - up), n=6)
    trail = bez3((44, 8 - up), (46.5, 15), (47, 26), (44, 35))
    body = lead + curl[1:] + [(40.5, 7 - up)] + trail + [(40, 37), (33, 36)]
    pid = p.poly(body, wing, group=20, bias=-0.05 if near else 0.3)
    if p.big:
        # the covert band along the leading edge and the stripe behind it
        band = bez3((31.5, 32), (32, 22), (36, 12 - up), (41, 8 - up))
        p.limb(band, 4.6, 3.4, wing, clip=[pid], group=21, bias=-0.32)
        stripe = [(x + 3.8, y + 0.6) for x, y in band]
        p.limb(stripe, 2.4, 1.8, bar, clip=[pid], group=22, noline=True)
    return pid


def enigmaw(p, view, phase):
    if view in ("front", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        onrock = view == "front"

        if onrock:
            # the pale limestone rock she sits on, cracked and weathered
            # three weathered boulders: a big one under her, a low one in
            # front, one behind the haunch
            p.blob(50.5, 55, 8.5, 7.5, rock, group=41, bias=0.15)
            p.blob(33, 56.5, 20, 6.6, rock, group=40)
            p.poly([(5.5, 61.5), (6.5, 57), (10, 54.5), (17, 54), (22, 56.5), (23, 61.5)], rock, group=42, bias=-0.05)
            p.rect(13, 59, 52, 61, rock, group=40)
            if p.big:
                p.stroke([(20, 54), (22, 56), (21, 59)], "s0")
                p.stroke([(46, 53), (44, 56), (46, 59)], "s0")
                p.stroke([(33, 57), (36, 59)], "s1")
                p.stroke([(10, 58), (13, 59)], "s1")

        # the wing behind
        _wing(p, L)
        # the tail curled into a question mark
        _tail(p, L, sq=0.8 * L)

        # body: the haunch folded on the rock, the barrel, the chest held high
        p.blob(43.5, 42.5, 10, 8.4, coat, group=1)
        p.blob(34, 40, 11, 7.6, coat, ang=-12, group=1)
        p.blob(25, 35.5, 7.6, 9, coat, group=1)
        p.blob(26.5, 42, 6.5, 5, belly, group=2)
        # the hind paw tucked under the haunch
        p.blob(40, 50, 5.4, 2.2, coat, group=3)
        # forelegs straight, paws together on the rock's edge
        p.limb([(28.5, 39), (28, 46), (27.5, 50)], 6.2, 5, coat, bias=0.25, group=4)
        _paw(p, 28, 50.8, w=5, far=True)
        p.limb([(22, 38), (21, 46), (20.5, 50)], 6.8, 5.4, coat, group=5)
        _paw(p, 20, 51, w=5.2)

        # the neck, and her head held high
        p.limb([(25.5, 33), (21.5, 23)], 9, 7.4, coat, group=6)
        _lion_head(p, 18.5, 15, L)
        return

    if view == "side":
        # follower walking: she pads along, wings folded, tail still curled
        step = phase
        p.limb([(50, 40), (58, 34), (57, 25), (52, 23), (50, 27)], 3.2, 2.4, coat)
        p.lens((30, 34), (52, 26), 9, wing, bend=-1.5)
        p.limb([(44, 44), (46 - 3 * step, 52), (45 - 3 * step, 58)], 5, 4, coat, bias=0.3)
        p.limb([(26, 44), (24 + 3 * step, 52), (24 + 3 * step, 58)], 5, 4, coat, bias=0.3)
        p.blob(36, 41, 13, 7, coat, group=1)
        p.limb([(44, 44), (42 + 3 * step, 52), (43 + 3 * step, 58)], 5.4, 4.4, coat)
        p.limb([(26, 44), (28 - 3 * step, 52), (27 - 3 * step, 58)], 5.4, 4.4, coat)
        p.limb([(26, 38), (21, 28)], 8, 6.5, coat)
        _lion_head(p, 18.5, 20)
        return

    if view == "back":
        # over the shoulder at about 1.2x: the lioness's back and shoulder,
        # the sickle wing rising from it and curling forward at the tip, the
        # question-mark tail behind the haunch, the banded hair falling down
        # her neck, the head turned right in profile
        tail = bez3((14, 60), (2, 56), (2, 40), (8, 34)) + bez((8, 34), (13, 31), (14.5, 37), n=6)[1:]
        p.limb(tail, 4.6, 3.4, coat, group=25, bias=0.15)
        p.drop((14, 42.5), 14, 38.5, 2.8, Mat(["c0", "c1"], line="c0", cuts=[0.55]), group=26)
        # the body from behind the shoulder: haunch, rib barrel, shoulder
        p.blob(12, 57, 10.5, 9, coat, group=1, bias=0.12)
        p.blob(27, 58, 14, 8.5, coat, group=2)
        p.blob(40.5, 51, 10.5, 10, coat, group=3)
        # the wing
        # three broad primaries fanning from the wing's trailing (left) edge,
        # behind it, one terracotta bar across them
        prim = []
        for i, (a_, b_, w_) in enumerate((((28, 11), (14, 15), 8.2), ((28, 20), (12.5, 26.5), 8.8),
                                          ((31, 29), (16.5, 38.5), 8.4))):
            prim.append(p.lens(a_, b_, w_, wing, bend=1.0, fat=0.3, group=50 + i, bias=0.05 * i))
        if p.big:
            p.limb(bez3((20, 11), (17, 19), (17.5, 28), (21.5, 36)), 2.4, 2.2, bar, clip=prim, group=60, noline=True)
        lead = bez3((34, 46), (24, 37), (21, 22), (24, 8))
        curl = bez((24, 8), (27.5, 3.5), (31.5, 6.5), n=6)
        trail = bez3((29, 9), (31, 22), (37, 33), (44, 41))
        pid = p.poly(lead + curl[1:] + trail, wing, group=20)
        if p.big:
            band = bez3((33, 44), (26, 35), (24, 22), (26.5, 11))
            p.limb(band, 4.6, 3.4, wing, clip=[pid], group=21, bias=-0.3)
            p.limb([(x - 3.6, y + 0.4) for x, y in band], 2.2, 1.6, bar, clip=[pid], group=22, noline=True)
        # the neck, the tresses hanging down it and tapering, and her head
        # turned right in profile
        p.limb([(41, 48), (45, 30)], 12, 9, coat, group=5)
        _lion_profile(p, 46.5, 19.5, k=1.2)
        # the tresses of the mane hang down the back of her neck, tapering
        for i, (top, bot, w) in enumerate((((38.5, 24), (35, 48), 5.0), ((41.5, 27), (39.5, 44), 4.4),
                                           ((36, 21), (31.5, 38), 4.4))):
            _taper_braid(p, top, bot, w, group=70 + i, bias=0.08 * i)
        return

    if view in ("down", "up"):
        step = phase
        if view == "up":
            # walking away: the haunches, the wings raised over the back, the
            # question-mark tail
            p.lens((30, 36), (12, 25), 8, wing, bend=2.4)
            p.lens((34, 36), (52, 25), 8, wing, bend=-2.4)
            p.limb([(26, 48), (26, 59 - 2 * step)], 4.6, 4, coat)
            p.limb([(38, 48), (38, 59 - 2 * (1 - step))], 4.6, 4, coat)
            p.blob(32, 44, 10, 9, coat, group=1)
            p.limb([(32, 47), (40, 42), (40, 33), (35, 30), (33, 34)], 3, 2.4, coat)
            # her head from behind: ears out of the mane, the tresses hanging
            p.lens((28.5, 24), (26.5, 17.5), 4.6, coat, bend=0.5)
            p.lens((35.5, 24), (37.5, 17.5), 4.6, coat, bend=-0.5)
            p.blob(32, 27, 7.4, 7, hair)
            p.limb(bez((25, 24), (32, 21.5), (39, 24)), 2.0, 1.8, gold)
            _taper_braid(p, (29, 30), (28, 42), 3.4)
            _taper_braid(p, (35, 30), (36, 42), 3.4)
            _taper_braid(p, (32, 31), (32, 44), 3.4)
            return
        # walking toward the camera: a lioness's face framed by the mane,
        # the forelegs, the sickle wings spread low behind the shoulders
        p.lens((29, 37), (11, 27), 8, wing, bend=2.4, bias=0.2)
        p.lens((35, 37), (53, 27), 8, wing, bend=-2.4, bias=0.2)
        p.blob(32, 43, 9, 9, coat, group=1)
        p.limb([(28, 46), (27.5, 59 - 2 * step)], 4.6, 4, coat)
        p.limb([(36, 46), (36.5, 59 - 2 * (1 - step))], 4.6, 4, coat)
        _taper_braid(p, (24.5, 31), (25, 44), 3.4, group=7)
        _taper_braid(p, (39.5, 31), (39, 44), 3.4, group=7)
        p.blob(32, 29, 9.5, 9, hair, group=8)
        p.lens((26.5, 24), (24, 17), 5, coat, bend=0.6, group=13)
        p.lens((37.5, 24), (40, 17), 5, coat, bend=-0.6, group=13)
        p.blob(32, 29, 6.6, 6, coat, group=9)
        p.blob(32, 33.5, 3.8, 2.8, muzzle, group=10)
        p.limb(bez((25.5, 25), (32, 22), (38.5, 25)), 2.0, 1.8, gold, group=12)
        leg = {"1": "ink", "f": "eye", "w": "s3", "n": "t0", "m": "t1", "d": "c0"}
        if p.big:
            p.patch(27, 28, ["111", "1f1", "f1w"], leg)
            p.patch(34, 28, ["111", "1f1", "w1f"], leg)
            p.patch(31, 32, ["mn", "11", "dd"], leg)
        else:
            p.px(29, 29.5, "ink")
            p.px(35, 29.5, "ink")
            p.px(32, 32.5, "t0")
        return


MONS = [
    # icon palette 2 keeps the tan coat and the terracotta hair apart
    Mon("Enigmaw", ENIGMAW_COLORS, ENIGMAW_SHINY, enigmaw, foot="bigpaw", icon_pal=2),
]
