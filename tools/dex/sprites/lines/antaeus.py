"""Antaeus: Geogrip (Fighting/Ground). The giant son of Gaia who wrestled
every traveler and rose stronger from each fall, until Herakles lifted him
off the earth (Apollodorus 2.5.11)."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

GEOGRIP_COLORS = [
    ("ink", INK),
    # clay-red skin, oiled like a palaestra wrestler
    ("k0", (96, 32, 24)), ("k1", (152, 64, 40)), ("k2", (200, 104, 64)), ("k3", (232, 152, 104)),
    ("sheen", (248, 208, 168)),
    # limestone sand and dust
    ("s0", (152, 120, 80)), ("s1", (200, 176, 128)), ("s2", (232, 216, 176)),
    # olive root-toes
    ("o0", (48, 64, 32)), ("o1", (88, 104, 48)), ("o2", (136, 152, 72)),
    # the dry-grass topknot
    ("straw0", (152, 112, 48)), ("straw1", (216, 176, 88)),
    ("white", C.white),
]
GEOGRIP_SHINY = {
    # marble-pale skin and cypress roots: a statue of a wrestler
    "k0": (112, 104, 104), "k1": (160, 152, 152), "k2": (208, 200, 192), "k3": (232, 232, 224),
    "sheen": (248, 248, 240),
    "o0": (24, 48, 40), "o1": (40, 88, 56), "o2": (72, 128, 88),
}

g_skin = Mat(["k0", "k1", "k2", "k3"], line="k0", cuts=[0.2, 0.44, 0.7])
g_sand = Mat(["s0", "s1", "s2"], line="s0", cuts=[0.36, 0.7])
g_root = Mat(["o0", "o1", "o2"], line="o0", cuts=[0.36, 0.68])
g_straw = Mat(["straw0", "straw1"], line="straw0", cuts=[0.5])
# cracked earth caked on the forearms
g_mud = Mat(["s0", "s1", "s2"], line="s0", cuts=[0.4, 0.7])


def _roots(p, x, y, spread, far=False):
    """Root-toes digging from a foot's front edge at (x, y) into the sand."""
    for i, (dx, dy) in enumerate(spread):
        p.taper(bez((x + i * 2.4, y), (x + i * 2.4 + dx * 0.4, y + dy * 0.8), (x + i * 2.4 + dx, y + dy)), 2.8,
                g_root, bias=0.25 if far else 0)


def _hand(p, x, y, sx=1, far=False, L=0):
    """An open hand, palm toward the foe, fingers spread; sx flips it."""
    b = 0.25 if far else 0.0
    p.blob(x, y, 3.8, 3.4, g_skin, bias=b, group=None)
    for i, (dx, dy) in enumerate(((-3.5, -4.5 - L), (-1, -5.5 - L), (1.5, -5 - L), (3.6, -3.5 - L))):
        p.limb([(x + sx * dx * 0.4, y - 1), (x + sx * dx, y + dy)], 2.2, 1.9, g_skin, bias=b)
    p.limb([(x - sx * 3, y + 0.5), (x - sx * 5.2, y - 1.5)], 2.2, 1.9, g_skin, bias=b)


def _palm(p, x, y, far=False, L=0):
    """An open hand raised with its palm to the foe, fingers splayed up."""
    b = 0.25 if far else 0.0
    for dx, dy in ((-3.6, -5.5), (-1, -7), (1.8, -6.5), (3.8, -3.8)):
        p.limb([(x + dx * 0.4, y - 1), (x + dx, y + dy - L)], 3.6, 3.0, g_skin, bias=b)
    p.blob(x, y, 5.4, 4.6, g_skin, bias=b)
    p.limb([(x - 4, y + 1.5), (x - 6.5, y - 1)], 3.4, 3.0, g_skin, bias=b)


def geogrip(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0   # sinks deeper, hands flex

        # the patch of sand
        p.blob(32, 59.5, 28, 3.4, g_sand, group=90)
        # far arm: elbow out wide, forearm up, palm raised to the foe
        p.limb([(47, 23 + L), (56.5, 32 + L)], 10, 8.6, g_skin, bias=0.25, group=20)
        p.limb([(56.5, 32 + L), (56, 22 + L)], 8.6, 7.4, g_mud, bias=0.15, group=21)
        _palm(p, 56, 18 + L, far=True, L=L)
        # far leg, bent, the foot planted wide
        p.limb([(40, 42 + L), (49, 48), (49, 56)], 10, 8, g_skin, bias=0.25, group=22)
        p.blob(50, 57.4, 6, 2.6, g_skin, bias=0.25, group=23)
        _roots(p, 45, 58.5, ((-1, 3), (0, 3.5), (1.5, 3), (2.6, 2.5)), far=True)
        # torso: huge chest, broad shoulders, a wrestler's belly
        p.blob(32, 30 + L, 15.5, 12, g_skin, group=1)
        p.blob(33, 40 + L, 11, 7, g_skin, group=1)
        # head, low between the shoulders, and the topknot of dry grass
        for a, b, w in (((29, 8.5 + L), (24, 2 + L), 3), ((30, 8 + L), (30.5, 1.5 + L), 3.2),
                        ((31, 8.5 + L), (36, 3 + L), 3)):
            p.lens(a, b, w, g_straw)
        p.blob(30, 9.5 + L, 3.2, 2.2, g_straw, group=8)
        p.blob(27, 17 + 2 * L, 7.4, 6.8, g_skin, group=3)
        # near leg, bent wide, foot flat with root-toes
        p.limb([(26, 43 + L), (16, 49), (16, 56)], 11, 8.6, g_skin, group=24)
        p.blob(15, 57.4, 6.6, 2.8, g_skin, group=25)
        _roots(p, 9, 58.5, ((-2, 3), (-1, 3.6), (0.5, 3.4), (2, 3)))
        # near arm: elbow out wide, forearm up, palm raised to the foe
        p.limb([(17, 24 + L), (7, 33 + L)], 10.6, 8.8, g_skin, group=26)
        p.limb([(7, 33 + L), (7.5, 22.5 + L)], 8.8, 7.8, g_mud, group=27)
        _palm(p, 7.5, 19.5 + L, L=L)
        if p.big:
            p.eye(21, 15 + 2 * L, 3, 4, shine="white", shine_at=(1, 1))
            p.eye(27, 15 + 2 * L, 3, 4, shine="white", shine_at=(1, 1))
        else:
            p.pxs([(22, 16 + 2 * L), (27, 16 + 2 * L)], "ink")
        return

    if view == "back":
        p.blob(32, 66, 30, 22, g_skin, group=1)
        p.limb([(12, 52), (5, 40), (8, 30)], 12, 9, g_skin, group=26)
        _hand(p, 9, 25, sx=1)
        p.blob(44, 30, 10, 9, g_skin, group=3)
        for a, b, w in (((44, 22), (40, 13), 3.6), ((45, 21.5), (46, 12), 3.8), ((46, 22), (51, 14), 3.6)):
            p.lens(a, b, w, g_straw)
        p.blob(45, 23, 3.8, 2.6, g_straw, group=8)
        if p.big:
            p.eye(50, 27, 3, 4, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: a flat-footed shuffle, never a hop; the roots drag
        sh = phase
        p.blob(32, 59.5, 15, 2.8, g_sand, group=90)
        for x, sd in ((25, sh), (39, 1 - sh)):
            p.limb([(x, 44), (x - 1 + 2 * sd, 55)], 8, 7, g_skin, group=20)
            p.blob(x - 1 + 2 * sd, 57, 5, 2.4, g_skin, group=21)
            for dx in (-3, 0, 3):
                p.taper([(x - 1 + 2 * sd + dx, 58), (x - 1 + 2 * sd + dx * 1.4, 61.5)], 2.6, g_root)
        for sx in (-1, 1):
            X = lambda x, sx=sx: 32 + sx * (x - 32)
            p.limb([(X(42), 29), (X(50), 36), (X(50), 45)], 7.4, 6.4, g_skin, group=22 + sx)
            for i, dx in enumerate((-2.4, 0, 2.4)):
                p.limb([(X(50) + dx, 47), (X(50) + dx * 1.4, 51)], 2.4, 2.0, g_skin, group=22 + sx)
            p.blob(X(50), 47, 3.4, 3, g_skin, group=22 + sx)
        p.blob(32, 35, 13, 11, g_skin, group=1)
        p.blob(32, 43, 9, 5, g_skin, group=1)
        for a, b, w in (((31, 16), (25, 8), 3.4), ((32, 15.5), (32, 7), 3.6), ((33, 16), (39, 8), 3.4)):
            p.lens(a, b, w * (1 if p.big else 1.25), g_straw)
        p.blob(32, 16.5, 3.4, 2.2, g_straw, group=8)
        p.blob(32, 23, 7.4, 6.8, g_skin, group=3)
        if view == "down":
            p.patch(26, 21, ["33333333333", "11112221111", "1w11...1w11", "1111...1111", ".......", "....222...."],
                    {"1": "ink", "w": "white", "2": "k0", "3": "k3"},
                    small=(26, 22, ["1w1...1w1", ".........", "...222..."]))
        else:
            if p.big:
                p.stroke([(32, 30), (32, 44)], "k0")
                p.stroke([(25, 31), (29, 34)], "k1")
                p.stroke([(39, 31), (35, 34)], "k1")
            else:
                p.stroke([(32, 31), (32, 43)], "k0")
        return


MONS = [
    Mon("Geogrip", GEOGRIP_COLORS, GEOGRIP_SHINY, geogrip, foot="root"),
]
