"""Below the Euploia's deck, refitted: MAP_EUPLOIA_BELOW as one 20x10 scene.

World-act1's hold was the rowers' deck, three tiers of benches. The refit
moved the oarsmen up to benches on deck and turned the hull into the crew's
quarters (ODYSSEY §2's diagram), bow to the east like the deck:

  the port wall (rows 1-2), stern to bow: the bunk; Iaso's staff and chest;
  the trophy shelf, seven keepsakes and the ship's own plaque; the ladder up
  to the hatch, daylight falling down it; Lampon's hearth, its clay hood and
  pot; the mess rack; the Pithos, Kydon's hold; Kydon's stall under a
  striped awning, its counter across the floor; jars in the bow
  the floor (rows 3-8): the mess table and its stool, Diktys's nets heaped
  against the stern bulkhead
  the beams overhead (row 0) and the starboard side's edge (row 9)

draw() returns the scene with the hearth lit and the shelf empty. Variants
for setmetatile (euploia_build.py diffs them against the base):

  hearth_cold         Lampon not aboard: ash, a cold pot, no glow
  keepsake_<name>     each of the seven keepsakes on its spot

Every texture repeats on a 16 or 32 px grid, so repeated cells share one
metatile. Pixel coordinates are absolute (x 0-319, y 0-159).
"""
from __future__ import annotations

from euploia_lib import CELL, Scene, h

W, H = 20, 10
PW, PH = W * CELL, H * CELL

BUNK = (1, 3)             # 2 wide; its frame rises into the wall
CHEST = (3, 3)            # Iaso's chest; her staff leans on the wall above
SHELF = (4, 1)            # the trophy shelf: 4 wide, 2 tiers (rows 1-2)
LADDER = (8, 3)           # the ladder's foot: warp 0, MB_LADDER
HEARTH = (9, 3)           # 2 wide; the hood rises above it
MESS = (11, 1)            # the mess rack on the wall, 2 wide
TABLE = (11, 6)           # the mess table, 2 wide; its stool at (10,6)
STOOL = (10, 6)
PITHOS = (13, 2)          # 2 wide, 2 tall
STALL = (15, 1)           # 3 wide: shelves on the wall, the awning above
COUNTER = 4               # the stall's counter row (MB_COUNTER), x 15-17
NETS = (1, 7)             # 2x2
JARS = (18, 3)
LAMPS = (18,)             # a hanging lamp (columns)
RUG = (9 * CELL + 4, 5 * CELL + 2, 14 * CELL - 4, 8 * CELL - 2)    # px: x0, y0, x1, y1
CHESTS = ((6, 8), (16, 8))   # the crew's sea chests along the starboard side
COIL = (17, 7)
WATER_JAR = (18, 6)

# The seven keepsakes and their spots on the shelf (ODYSSEY §2's order),
# and the ship's own plaque, always there.
KEEPSAKES = [
    ("fleece", "the ram's fleece", (4, 1)),
    ("lotus", "a lotus", (5, 1)),
    ("cord", "the bag's silver cord", (6, 1)),
    ("feather", "a Siren's feather", (7, 1)),
    ("tooth", "Scylla's tooth", (4, 2)),
    ("cup", "Circe's cup", (5, 2)),
    ("oar", "a Phaeacian oar", (6, 2)),
]
PLAQUE = (7, 2)


# ---------------------------------------------------------------------------
# The room: beams, the port wall, the floor, the bulkheads, the edge
# ---------------------------------------------------------------------------

def beams(s: Scene):
    """Row 0: the underside of the deck, dark, its beams every 32 px, and the
    heavy shelf of the deck clamp at the top of the wall."""
    B = s.B
    for x in range(PW):
        for y in range(0, 16):
            c = "hd0" if (y // 3) % 2 else "ink"
            if y >= 12:
                c = {12: "wd1", 13: "wd0", 14: "wd0", 15: "ink"}[y]
            elif x % 32 in (10, 11, 12, 13, 14, 15):
                c = {10: "ink", 11: "wd0", 12: "wd1", 13: "wd0", 14: "wd0", 15: "ink"}[x % 32]
            B.px(x, y, c)


def wall(s: Scene):
    """Rows 1-2: the port hull from inside: strakes, frames every 32 px, the
    oar ports shuttered now, a little daylight round their edges."""
    B = s.B
    for x in range(PW):
        for y in range(16, 48):
            k = (y - 16) % 8
            c = "wd1" if k == 0 else "wd0" if k < 5 else "hd0"
            fx = x % 32
            if fx in (10, 11, 12, 13):
                c = {10: "ink", 11: "pk1", 12: "wd1", 13: "ink"}[fx]
            if y >= 45:
                c = "hd0" if y < 47 else "ink"                    # the wall's foot
            B.px(x, y, c)
    for x0 in range(26, PW, 32):                                  # the shutters
        B.blit(["kkkkkkk", "kfwwwfk", "kwdddwk", "kwdddwk", "kfwwwfk", "kkkkkkk"],
               {"k": "ink", "f": "lt1", "w": "wd1", "d": "wd0"}, x0, 32)


def plank(x, y):
    """The quarters' floor: planks fore and aft, 4 px wide, on a 16 px repeat."""
    r = (y // 4) % 4
    yy = y % 4
    joint = (r * 5 + 3) % 16
    if yy == 3 or (x - joint) % 16 == 0:
        return "wd1"
    if yy == 0:
        return "pk2"
    g = h(x, y, 5, 16)
    return "pk2" if g > 0.9 else "pk1"


def floor(s: Scene):
    B = s.B
    for x in range(PW):
        for y in range(48, 144):
            c = plank(x, y)
            if y == 48:
                c = "ink"
            elif y in (49, 50):
                c = "wd0"                                         # shadow under the wall
            B.px(x, y, c)


def edge(s: Scene):
    """Row 9: the starboard side's top edge, and the dark beyond it."""
    B = s.B
    for x in range(PW):
        for y in range(144, 160):
            k = y - 144
            c = {0: "ink", 1: "pk2", 2: "wd1", 3: "wd0"}.get(k, "hd0" if k < 12 else "ink")
            if k >= 4 and x % 32 in (10, 11):
                c = "wd0" if x % 32 == 10 else "ink"
            B.px(x, y, c)


def bulkheads(s: Scene):
    """The stern and bow ends: dark timber, frames converging."""
    B = s.B
    for cx in (0, W - 1):
        for x in range(cx * CELL, cx * CELL + CELL):
            for y in range(0, PH):
                inner = (x - cx * CELL) if cx == 0 else (cx * CELL + 15 - x)
                c = "hd0" if inner < 12 else "wd0"
                if inner in (12, 13):
                    c = "ink" if inner == 13 else "wd1"
                if inner == 6 and y % 8 < 6:
                    c = "wd0"
                B.px(x, y, c)


# ---------------------------------------------------------------------------
# The furniture
# ---------------------------------------------------------------------------

def draw_bunk(s: Scene):
    """The Archon's bunk against the stern: a box bed, a fleece over it and a
    linen pillow, a red blanket folded at the foot; above it a second shelf
    with a rolled fleece and a kitbag."""
    M = s.M
    x0, y0 = BUNK[0] * CELL, BUNK[1] * CELL - 32          # 16, 16
    # the recess behind the bed, in shadow
    for x in range(x0 + 2, x0 + 30):
        for y in range(y0 + 2, y0 + 33):
            M.px(x, y, "hd0" if (y - y0) % 8 else "ink")
    # corner posts
    for px_ in (x0, x0 + 29):
        for y in range(y0, y0 + 48):
            for dx, c in ((0, "ink"), (1, "pk1"), (2, "wd1")):
                M.px(px_ + dx, y, c)
    for x in range(x0, x0 + 32):
        M.px(x, y0, "ink")
        M.px(x, y0 + 1, "wd1")
    # the upper shelf with a rolled fleece and a kitbag
    for x in range(x0 + 2, x0 + 30):
        M.px(x, y0 + 12, "pk2")
        M.px(x, y0 + 13, "wd1")
        M.px(x, y0 + 14, "ink")
    M.blit([" kkkkkkkkkk ", "kwwrwwwrwwwk", "kwrwwwrwwrrk", "krrrwrrrrrrk", " kkkkkkkkkk "],
           {"k": "ink", "w": "w0", "r": "rp"}, x0 + 4, y0 + 7)
    M.blit(["  kk  ", " kbbk ", "kbBBbk", "kbBbbk", " kkkk "], {"k": "ink", "b": "b1", "B": "b0"},
           x0 + 19, y0 + 7)
    # the bed: a plump pillow, the red blanket with the sheet turned down, a
    # fleece thrown over the foot
    yb = y0 + 32
    for x in range(x0 + 3, x0 + 29):
        for y in range(yb + 1, yb + 10):
            k = x - x0
            if k < 12:
                c = "w0" if y < yb + 8 else "rp"
            elif k < 14:
                c = "w0" if k == 12 else "rp"                    # the sheet, turned down
            else:
                c = "rd" if (y - yb) < 7 else "rd0"
                if (k + y) % 7 == 0 and y < yb + 7:
                    c = "rd0"                                     # folds
            M.px(x, y, c)
        M.px(x, yb, "ink")
    M.blit([" kkkkkkk ", "kwwwwwwwk", "kwwwwwwrk", "krwwwwrrk", " kkkkkkk "], {"k": "ink", "w": "w0", "r": "rp"},
           x0 + 3, yb + 1)
    M.blit(["  kkkkkk", " kwwrwwk", "kwrwwwrk", "kwwwrwwk", "kkkkkkkk"], {"k": "ink", "w": "w0", "r": "rp"},
           x0 + 22, yb + 4)
    # the front board and its feet
    for x in range(x0 + 1, x0 + 31):
        M.px(x, yb + 10, "pk3")
        M.px(x, yb + 11, "pk2")
        M.px(x, yb + 12, "wd1")
        M.px(x, yb + 13, "ink")
    for fx in (x0 + 2, x0 + 3, x0 + 28, x0 + 29):
        M.px(fx, yb + 14, "wd0")
        M.px(fx, yb + 15, "ink")


def draw_iaso(s: Scene):
    """Iaso's chest by the bunk, its lid open on herbs and linen, a snake
    painted on its front; her staff with its snake leaning on the wall."""
    M = s.M
    x0, y0 = CHEST[0] * CELL, CHEST[1] * CELL
    # the staff of Asclepius
    for y in range(y0 - 30, y0):
        M.px(x0 + 11, y, "ink")
        M.px(x0 + 12, y, "pk2")
        M.px(x0 + 13, y, "wd1")
        M.px(x0 + 14, y, "ink")
    for i, y in enumerate(range(y0 - 27, y0 - 4)):
        sx = x0 + 10 + (2 if (i // 3) % 2 else 4)
        M.px(sx, y, "ol2" if i % 3 else "ol1")
        M.px(sx + 1, y, "ol1")
    M.blit([" kk", "kooo", " kk"], {"k": "ink", "o": "ol2"}, x0 + 13, y0 - 29)
    # the open lid, leaning on the wall
    M.blit([
        " kkkkkkkkkkk ",
        "kpPPPPPPPPPpk",
        "kpwwwwwwwwwpk",
        "kpwwwwwwwwwpk",
        "kpppppppppppk",
        " kkkkkkkkkkk ",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1"}, x0 + 1, y0 - 6)
    # the chest: herbs and linen rolls inside, the painted snake on the front
    M.blit([
        "kkkkkkkkkkkkk ",
        "kgGgLLwLLtTgkk",
        "kGggLwwwLtttgk",
        "kkkkkkkkkkkkkk",
        "kPPPPPPPPPPPPk",
        "kpppoppppppppk",
        "kppopoppppopwk",
        "kpopppopppopwk",
        "kppppppoppoppk",
        "kwwwwwwwwwwwwk",
        "kkkkkkkkkkkkkk",
        " kk        kk ",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1", "g": "ol1", "G": "ol2", "L": "rp", "o": "ol1",
        "t": "tc1", "T": "tc2"}, x0 + 1, y0 + 3)


def draw_shelf(s: Scene, filled=()):
    """The trophy shelf: two tiers between side boards, a cap above. Each of
    the seven keepsakes sits on its own 16 px spot; `filled` names the ones
    drawn. The eighth spot holds the ship's own painted plaque."""
    M = s.M
    x0, y0 = SHELF[0] * CELL, SHELF[1] * CELL            # 64, 16
    x1 = x0 + 4 * CELL - 1                                # 127
    # the niche's back, painted Aegean blue, so the keepsakes stand out
    for x in range(x0 + 2, x1 - 1):
        for y in range(y0 + 3, y0 + 29):
            c = "b1" if (x - x0) % 16 else "ink"
            if y in (y0 + 3, y0 + 16):
                c = "ink"
            elif y in (y0 + 4, y0 + 17):
                c = "b2"
            M.px(x, y, c)
    for x in range(x0, x1 + 1):
        M.px(x, y0, "ink")
        M.px(x, y0 + 1, "g0")                             # a gilded cap
        M.px(x, y0 + 2, "br")
        for yp in (y0 + 13, y0 + 29):                     # the two tiers
            M.px(x, yp, "wd1")
            M.px(x, yp + 1, "br")
            M.px(x, yp + 2, "ink")
    for px_ in (x0, x1 - 1):
        for y in range(y0, y0 + 32):
            M.px(px_, y, "ink" if px_ == x0 else "br")
            M.px(px_ + 1, y, "wd1" if px_ == x0 else "ink")
    # brackets under each tier
    for bx in (x0 + 14, x0 + 46):
        for yp in (y0 + 16, y0 + 32):
            if yp < y0 + 32:
                M.blit(["kwk", " k "], {"k": "ink", "w": "wd0"}, bx, yp)
    for name, _, (cx, cy) in KEEPSAKES:
        if name in filled:
            KEEPSAKE_ART[name](M, cx * CELL, cy * CELL)
    plaque(M, PLAQUE[0] * CELL, PLAQUE[1] * CELL)


# Each keepsake is drawn in its 16x16 spot (sx, sy), resting on the tier's
# plank at sy + 13. Shrine colors.

def fleece(M, sx, sy):
    """The great ram's fleece from the Cyclops's island, folded over the edge."""
    M.blit([
        "    kkkkkk    ",
        "  kkwmwwmwkk  ",
        " kwwmwwwmwwmk ",
        "kwmwwwmwwwmwwk",
        "kwwwmwwmwwwmwk",
        "kmwwwwmwwmwwMk",
        "kwmwmwwwmwwMMk",
        " kMwwMwwMwMMk ",
        " kwMkkMMkMMkk ",
        "  kk  kk  kk  ",
    ], {"k": "ink", "w": "w0", "m": "m2", "M": "m3"}, sx + 1, sy + 4)


def lotus(M, sx, sy):
    """A lotus from the island where nobody wants to leave, in a bronze bowl."""
    M.blit([
        "     kk     ",
        "    kppk    ",
        "  kkpPPpkk  ",
        " kppkPPkppk ",
        " kpPpwwpPpk ",
        "  kpPwwPpk  ",
        " o kkppkk o ",
        "oook    kooo",
        " kggggggggk ",
        "  kGggggbk  ",
        "   kkkkkk   ",
    ], {"k": "ink", "p": "pn1", "P": "pn2", "w": "w0", "o": "ol2", "g": "g0", "G": "g1",
        "b": "br"}, sx + 2, sy + 2)


def cord(M, sx, sy):
    """The silver cord that tied Aeolus's bag of winds, coiled, its knot."""
    M.blit([
        "    kkkkk     ",
        "  kkwmwmwkk   ",
        " kwmkkkkkmwk  ",
        "kwmk kkk kmwk ",
        "kmwkkwmwkkwmk ",
        " kmwmwkwmwmk  ",
        "  kkkkkkkkwmk ",
        "     kGgk kmwk",
        "    kGggk  kmk",
        "    kgggk   k ",
        "     kkk      ",
    ], {"k": "ink", "w": "w0", "m": "m2", "G": "g1", "g": "g0"}, sx + 1, sy + 2)


def feather(M, sx, sy):
    """A Siren's feather, long and white, barred blue, standing in a holder."""
    M.blit([
        "       kkk   ",
        "     kkwwwk  ",
        "    kwwbwwwk ",
        "   kwbwwbwmk ",
        "   kwwbwwwmk ",
        "  kwbwwbwmk  ",
        "  kwwwbwmk   ",
        " kwbwwwmk    ",
        " kwwbwmk     ",
        " kwwmkk      ",
        "kmmkk        ",
        "kk           ",
    ], {"k": "ink", "w": "w0", "b": "b2", "m": "m2"}, sx + 1, sy + 1)


def tooth(M, sx, sy):
    """Scylla's tooth: a long curved fang on a small wooden stand."""
    M.blit([
        "    kk      ",
        "   kwmk     ",
        "   kwmk     ",
        "  kwwmk     ",
        "  kwwmMk    ",
        "  kwwwmk    ",
        "   kwwmMk   ",
        "   kwwwmMk  ",
        "    kwwwmMk ",
        "     kkkkkk ",
        "   kdddddddk",
        "   kkkkkkkkk",
    ], {"k": "ink", "w": "w0", "m": "m2", "M": "m3", "d": "wd0"}, sx + 2, sy + 1)


def cup(M, sx, sy):
    """Circe's cup: a golden kylix, wide and shallow, two handles, one foot."""
    M.blit([
        "kk  kkkkkkk  kk",
        "k kkGGGGGGgkk k",
        "kkgGgggggggggkk",
        " kkgggggggggbk ",
        "   kbbbbbbbbk  ",
        "     kkbkk     ",
        "      kbk      ",
        "    kkgggbk    ",
        "    kkkkkkk    ",
    ], {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, sx, sy + 4)


def oar(M, sx, sy):
    """A Phaeacian oar, a votive model: the ships that sail by thought."""
    for i in range(11):
        x, y = sx + 2 + i, sy + 11 - i
        M.px(x, y, "ink")
        M.px(x, y - 1, "wd1")
        M.px(x + 1, y - 1, "ink")
    M.blit([
        "   kkk",
        "  kbBk",
        " kbBbk",
        "kbBbk ",
        "kggk  ",
        " kk   ",
    ], {"k": "ink", "b": "b1", "B": "b2", "g": "g1"}, sx + 9, sy + 1)


def plaque(M, sx, sy):
    """The ship's own pinax: the Euploia painted in black on a blue sea."""
    M.blit([
        " kkkkkkkkkkkk ",
        "kmmmmmmmmmmmmk",
        "kmwwwwwwwwwwMk",
        "kmwwwwkwwwwwMk",
        "kmwwwkkkwwwwMk",
        "kmkkkkkkkkkkMk",
        "kmbkkkkkkkkbMk",
        "kmbbbBbbBbbbMk",
        "kmBbbbbBbbbBMk",
        "kMMMMMMMMMMMMk",
        " kkkkkkkkkkkk ",
    ], {"k": "ink", "m": "m2", "M": "m3", "w": "w0", "b": "b1", "B": "b2"}, sx + 1, sy + 2)


KEEPSAKE_ART = {"fleece": fleece, "lotus": lotus, "cord": cord, "feather": feather,
                "tooth": tooth, "cup": cup, "oar": oar}


def draw_ladder(s: Scene):
    """The ladder up to the hatch against the wall, daylight falling down it
    onto the floor at its foot (bottom layer: the player stands in front)."""
    B = s.B
    x0 = LADDER[0] * CELL
    for y in range(0, 48):
        for x in range(x0, x0 + 16):
            c = "lt1" if (x + y) % 2 else "pk3"
            if y < 6:
                c = "fc"
            B.px(x, y, c)
    for y in range(48, 80):
        for x in range(x0, x0 + 16):
            c = B.get(x, y)
            edge = x < x0 + 2 or x > x0 + 13 or y > 74
            if c == "pk1":
                B.px(x, y, "pk2" if edge else "pk3")
            elif c == "pk2":
                B.px(x, y, "pk3" if edge else "lt1")
            elif c == "wd1" and not edge:
                B.px(x, y, "pk2")
    for y in range(0, 55):
        for x in (x0 + 2, x0 + 12):
            B.px(x, y, "ink")
            B.px(x + 1, y, "pk3")
            B.px(x + 2, y, "wd1")
        if y % 8 == 3:
            for x in range(x0 + 4, x0 + 12):
                B.px(x, y, "pk2")
                B.px(x, y + 1, "wd0")
    for x in (x0 + 2, x0 + 3, x0 + 4, x0 + 12, x0 + 13, x0 + 14):
        B.px(x, 55, "ink")


# The flames in four phases: euploia_build.py turns phases 1-3 into the frames
# src/tileset_anims.c copies over phase 0's tiles, so Hestia's fire flickers.
FLAMES = [
    ["     f    f     g     f   ",
     "    fg   fgf   fgf   fg   ",
     "   fgGf fgGgf fgGgf fgGf  ",
     "  fgGcgffgGcgfgGcGgffgcgf ",
     "  fgcccgfgcccgfgcccgfgccgf"],
    ["    f     g    f     f    ",
     "    gf   fgf   fg   fgf   ",
     "   fgGf fgGgf fGgf  fGgf  ",
     "  fgcGgffgcGgfgGcGgffgGcf ",
     "  fgcccgfgcccgfgcccgfgccgf"],
    ["      f   f      f    g   ",
     "     fg  fgf    fgf  fgf  ",
     "   fgGf fgGgf  fgGgffgGf  ",
     "  fgGcgffgGcgffgGcGgfgcgf ",
     "  fgcccgfgcccgfgcccgfgccgf"],
    ["   g      f    g      f   ",
     "   fgf   fg   fgf    fg   ",
     "   fgGf fgGf  fgGgf fgGf  ",
     "  fgGcgfgGcgffgGcGgffgcgf ",
     "  fgcccgfgcccgfgcccgfgccgf"],
]


def draw_hearth(s: Scene, lit=True, phase=0):
    """Lampon's hearth, Hestia's fire aboard: a raised clay hearth, a cooking
    pot on three stones over the flames, a clay hood and flue up through the
    deck. Cold, it's ash and a dark pot. `phase` picks the flames' frame."""
    M = s.M
    x0, y0 = HEARTH[0] * CELL, HEARTH[1] * CELL          # 144, 48
    # the flue through the beams and the hood over the hearth
    for y in range(0, 46):
        if y < 22:
            a, b = x0 + 8, x0 + 23
        else:
            t = (y - 22) / 23
            a, b = int(x0 + 8 - 7 * t), int(x0 + 23 + 7 * t)
        for x in range(a, b + 1):
            k = x - a
            # dark clay, sooted, warmer toward the fire
            warm = y > 34
            c = "tc1" if k < 2 else "hd0" if k > (b - a) - 3 else "tc0"
            if warm and 2 <= k <= (b - a) - 3:
                c = "tc1" if (x + y) % 3 else "tc0"
            if y % 8 == 7:
                c = "hd0" if not warm else "tc0"
            if x in (a, b):
                c = "ink"
            M.px(x, y, c)
    for x in range(x0 + 1, x0 + 31):                       # the hood's rim
        M.px(x, 44, "tc2")
        M.px(x, 45, "lt1" if lit else "tc0")
        M.px(x, 46, "ink")
    # the hearth: a raised clay box, its rim, the bricks of its front
    for x in range(x0 + 1, x0 + 31):
        for y in range(y0 + 4, y0 + 16):
            k = y - y0
            if k < 6:
                c = "tc2" if k == 4 else "tc1"
            else:
                c = "tc0" if (y % 4 == 1 or (x + (y // 4) * 4) % 8 == 0) else "tc1"
            M.px(x, y, c)
        M.px(x, y0 + 3, "ink")
        M.px(x, y0 + 15, "ink")
    for y in range(y0 + 3, y0 + 16):
        M.px(x0, y, "ink")
        M.px(x0 + 31, y, "ink")
    M.blit(["kkkkkkkk", "kHHHHHHk", "kHkkkkHk"], {"k": "ink", "H": "hd0"}, x0 + 12, y0 + 9)   # the ash door
    if lit:
        for x in range(x0 + 13, x0 + 19):
            M.px(x, y0 + 10, "fl" if (x + phase) % 2 else "g1")
            M.px(x, y0 + 11, "fl")
    # the fire bed, with the flames or the ash
    for x in range(x0 + 4, x0 + 28):
        M.px(x, y0 + 5, "hd0")
        M.px(x, y0 + 6, "fl" if lit and (x + phase) % 3 else "hd0" if lit else "wd0")
    if lit:
        M.blit(FLAMES[phase % len(FLAMES)], {"f": "fl", "g": "g1", "G": "fc", "c": "fc"}, x0 + 3, y0 - 1)
    else:
        M.blit(["  w  ww  w   ww  w  ww  ", " wHwwHHwwHw wHHwwHwwHHw "], {"w": "wd0", "H": "hd0"},
               x0 + 4, y0 + 2)
    # the cooking pot on its stones
    pot = [
        "   kkkkkkkk   ",
        "  kRRRRRRRRk  ",
        " kkkkkkkkkkkk ",
        " kTTttttttttk ",
        "kTTtttttttttak",
        "kTtttttttttaak",
        "kTtttttttttaak",
        " kttttttttaak ",
        "  kkkkkkkkkk  ",
    ]
    if lit:
        M.blit(pot, {"k": "ink", "R": "tc2", "T": "tc2", "t": "tc1", "a": "tc0"}, x0 + 9, y0 - 8)
        M.blit(["  l    l ", " l  l  l", "  l  l "], {"l": "rp"}, x0 + 12, y0 - 12)   # steam
    else:
        M.blit(pot, {"k": "ink", "R": "tc0", "T": "tc0", "t": "hd0", "a": "ink"}, x0 + 9, y0 - 8)
    for sx in (x0 + 8, x0 + 21):
        M.blit(["kpk", "kwk"], {"k": "ink", "p": "pk2", "w": "wd0"}, sx, y0 + 1)


def draw_mess(s: Scene):
    """The mess: a rack on the wall with bowls, cups and a jug, a ladle and a
    string of onions; the table with its stool, bowls and a loaf."""
    M = s.M
    x0, y0 = MESS[0] * CELL, MESS[1] * CELL               # 176, 16
    for x in range(x0 + 1, x0 + 31):
        for yp in (y0 + 13, y0 + 26):
            M.px(x, yp, "pk2")
            M.px(x, yp + 1, "wd1")
            M.px(x, yp + 2, "ink")
    bowl = [" kkkkk ", "k22222k", " k111k ", "  kkk  "]
    for bx in (x0 + 2, x0 + 9):
        M.blit(bowl, {"k": "ink", "2": "tc2", "1": "tc1"}, bx, y0 + 9)
        M.blit(bowl, {"k": "ink", "2": "tc2", "1": "tc1"}, bx, y0 + 7)
    M.blit(["  kk  ", " k3 k ", "k3322k", "k3221k", "k2211k", " k11k ", "  kk  "],
           {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"}, x0 + 18, y0 + 6)        # the jug
    for cx in (x0 + 25,):
        M.blit(["kkkk", "k33k", "k22k", " kk "], {"k": "ink", "3": "tc3", "2": "tc2"}, cx, y0 + 9)
    # the lower shelf: cups and a jar of oil
    for cx in (x0 + 2, x0 + 7):
        M.blit(["kkkk", "k33k", "k22k", " kk "], {"k": "ink", "3": "tc3", "2": "tc2"}, cx, y0 + 22)
    M.blit([" kk ", "kook", "kOok", "kOOk", " kk "], {"k": "ink", "o": "ol2", "O": "ol1"}, x0 + 13, y0 + 21)
    # the ladle on its hook, and the onions hanging
    for y in range(y0 + 29, y0 + 32):
        M.px(x0 + 20, y, "wd1")
    M.blit(["kk", "kw", "kw", "kw", "kw", "kkk", "kwwk", " kk"], {"k": "ink", "w": "wd1"}, x0 + 19, y0 + 15)
    for i, oy in enumerate(range(y0 + 16, y0 + 25, 3)):
        M.blit([" kk ", "krrk", "kRrk", " kk "], {"k": "ink", "r": "rp", "R": "pk3"},
               x0 + 26 + (i % 2), oy)
    for y in range(y0 + 15, y0 + 17):
        M.px(x0 + 27, y, "rp1")


def draw_table(s: Scene):
    M = s.M
    x0, y0 = TABLE[0] * CELL, TABLE[1] * CELL
    for x in range(x0 + 1, x0 + 31):
        for y in range(y0 + 2, y0 + 9):
            M.px(x, y, "pk3" if (y - y0) % 3 else "pk2")
        M.px(x, y0 + 1, "ink")
        M.px(x, y0 + 9, "wd1")
        M.px(x, y0 + 10, "wd0")
        M.px(x, y0 + 11, "ink")
    for y in range(y0 + 1, y0 + 12):
        M.px(x0, y, "ink")
        M.px(x0 + 31, y, "ink")
    for lx in (x0 + 2, x0 + 3, x0 + 28, x0 + 29):
        for y in range(y0 + 12, y0 + 16):
            M.px(lx, y, "wd0" if lx in (x0 + 3, x0 + 29) else "ink")
    bowl = [" kkkkk ", "k22222k", " k111k ", "  kkk  "]
    M.blit(bowl, {"k": "ink", "2": "tc2", "1": "tc1"}, x0 + 4, y0 + 3)
    M.blit(bowl, {"k": "ink", "2": "tc2", "1": "tc1"}, x0 + 20, y0 + 4)
    M.blit([" kkkkk ", "kpPPPpk", "kppPppk", " kkkkk "], {"k": "ink", "p": "pk2", "P": "rp"}, x0 + 12, y0 + 3)
    M.blit([" kk ", "k32k", "k21k", " kk "], {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"},
           x0 + 26, y0 + 1)
    # the stool
    x0, y0 = STOOL[0] * CELL, STOOL[1] * CELL
    M.blit([
        "   kkkkkkkk   ",
        "  kPPPPPPPPk  ",
        "  kppppppppk  ",
        "   kwwwwwwk   ",
        "   kw kk wk   ",
        "  kw  kk  wk  ",
        "  kw  kk  wk  ",
        " kkk  kk  kkk ",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1"}, x0 + 1, y0 + 6)


def draw_pithos(s: Scene):
    """The Pithos, Kydon's hold: a great storage jar taller than a child, its
    lid roped down, relief bands, and a black-figure ship sailing round it."""
    M = s.M
    x0, y0 = PITHOS[0] * CELL, PITHOS[1] * CELL          # 208, 32
    cx = x0 + 15.5
    for y in range(y0 + 3, y0 + 31):
        t = y - y0
        if t < 6:
            hw = 8
        elif t < 11:
            hw = 8 + (t - 6) * 1.4
        elif t < 22:
            hw = 14
        else:
            hw = 14 - (t - 22) * 0.9
        a, b = int(round(cx - hw)), int(round(cx + hw))
        for x in range(a, b + 1):
            f = (x - a) / max(1, b - a)
            c = "tc3" if f < 0.18 else "tc2" if f < 0.55 else "tc1" if f < 0.85 else "tc0"
            if t in (6, 14, 25):
                c = "tc0" if f > 0.5 else "tc1"                 # relief bands
            if t in (7, 15, 26) and f < 0.6:
                c = "tc3"
            if 17 <= t <= 22 and 0.12 < f < 0.88:
                c = "tc2"                                       # the frieze's ground
            if x in (a, b):
                c = "ink"
            M.px(x, y, c)
    # the black-figure frieze: a ship with its oars, a dolphin
    M.blit([
        "        k            ",
        "  k    kk   k k     k",
        "kkkkkkkkkkkkk  kk  kk",
        " kkkkkkkkkkk    kkkk ",
        " k k k k k k     k   ",
    ], {"k": "ink"}, x0 + 5, y0 + 17)
    # the rim, the wooden lid, the rope
    M.blit([
        "     kkkkkkkkkkkkkkkkkkkk     ",
        "    kPPPPPPPPPPPPPPPPPPPPpk    ",
        "    kppppppppppppppppppppwk    ",
        "     kkkkkkkkkkkkkkkkkkkk     ",
        "      k3222222222222221k      ",
        "      kkkkkkkkkkkkkkkkkk      ",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1", "3": "tc3", "2": "tc2", "1": "tc1"},
        x0 + 1, y0 - 2)
    for x in range(x0 + 7, x0 + 25, 5):
        M.px(x, y0 - 1, "rp")
        M.px(x, y0, "rp1")
    # its shadow on the floor
    for x in range(x0 + 4, x0 + 28):
        M.px(x, y0 + 31, "wd0")


def draw_stall(s: Scene):
    """Kydon's stall: shelves on the wall with Poké Balls, potions, berries and
    the six offerings; a striped awning from the beam; the counter across."""
    M = s.M
    x0, y0 = STALL[0] * CELL, STALL[1] * CELL             # 240, 16
    x1 = x0 + 48
    # uprights and shelves
    for px_ in (x0 + 1, x1 - 3):
        for y in range(y0 + 4, y0 + 32):
            M.px(px_, y, "ink")
            M.px(px_ + 1, y, "wd1")
            M.px(px_ + 2, y, "ink")
    for yp in (y0 + 15, y0 + 28):
        for x in range(x0 + 1, x1 - 1):
            M.px(x, yp, "pk2")
            M.px(x, yp + 1, "wd1")
            M.px(x, yp + 2, "ink")
    ball = [" kkk ", "krrrk", "kkwkk", "kwwwk", " kkk "]
    for bx in (x0 + 5, x0 + 10):
        M.blit(ball, {"k": "ink", "r": "rd", "w": "w0"}, bx, y0 + 10)
    lek = [" k ", "k3k", "k2k", "k21k", " kk"]
    for bx in (x0 + 17, x0 + 21, x0 + 25):
        M.blit(lek, {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"}, bx, y0 + 10)
    M.blit(["  kk  ", " krrk ", "krrrrk", "kRrrRk", " kkkk "], {"k": "ink", "r": "rd", "R": "tc0"},
           x0 + 31, y0 + 10)                                                     # wine
    M.blit([" kkkk ", "kOooOk", "kooooO", "kOooOk", " kkkk "], {"k": "ink", "o": "ol2", "O": "ol1"},
           x0 + 38, y0 + 10)                                                     # olive oil
    # the lower shelf: a basket of berries, barley cakes, laurel, incense
    M.blit(["krkokrk", "korkrok", "kwwwwwk", " kwwwk "], {"k": "ink", "r": "rd", "o": "ol2", "w": "wd1"},
           x0 + 4, y0 + 24)
    M.blit([" kkkkk ", "kpPPPpk", "kpPPPpk", "kpPPPpk"], {"k": "ink", "p": "pk3", "P": "rp"}, x0 + 13, y0 + 24)
    M.blit(["o o o", " ooo ", "o o o", "  k  "], {"o": "ol2", "k": "ol1"}, x0 + 23, y0 + 23)
    M.blit([" kkk ", "kwrwk", "kwwrk", " kkk "], {"k": "ink", "w": "w0", "r": "rp"}, x0 + 31, y0 + 24)
    M.blit(["  kk  ", " k32k ", "k3221k", " kkkk "], {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"},
           x0 + 38, y0 + 24)
    # the awning, striped, scalloped, hanging from the beam
    for x in range(x0, x1):
        for y in range(10, 20):
            c = "rd" if (x // 4) % 2 else "w0"
            if y == 10:
                c = "ink"
            M.px(x, y, c)
        sc = (x - x0) % 8
        drop = 20 + (2 if 2 <= sc <= 5 else 1 if sc in (1, 6) else 0)
        for y in range(20, drop):
            M.px(x, y, "rd" if (x // 4) % 2 else "w0")
        M.px(x, drop, "ink")
    # behind the counter: a sack and a basket either side of Kydon
    M.blit([
        "   kk  kk   ",
        "  kssk ksk  ",
        "  kSsskssk  ",
        " kSSsssssk  ",
        "kSSssssssrk ",
        "kSsssssssrk ",
        "kSssssssrrk ",
        "kssssssrrrk ",
        " kssssrrrk  ",
        "  kkkkkkk   ",
    ], {"k": "ink", "S": "rp", "s": "rp1", "r": "wd1"}, x0 + 2, y0 + 37)
    M.blit([
        " kkkkkkkkkk ",
        "kokrkokrkook",
        "kwwwwwwwwwwk",
        "kwdwdwdwdwdk",
        "kdwdwdwdwdwk",
        "kwdwdwdwdwdk",
        " kkkkkkkkkk ",
    ], {"k": "ink", "o": "ol2", "r": "rd", "w": "wd1", "d": "wd0"}, x0 + 34, y0 + 40)
    # the counter
    yc = COUNTER * CELL
    for x in range(x0, x1):
        M.px(x, yc + 1, "ink")
        for y in range(yc + 2, yc + 5):
            M.px(x, y, "pk3" if y < yc + 4 else "pk2")
        M.px(x, yc + 5, "ink")
        for y in range(yc + 6, yc + 15):
            c = "wd1" if (x - x0) % 8 else "wd0"
            if y == yc + 6:
                c = "pk2"
            M.px(x, y, c)
        M.px(x, yc + 15, "ink")
    for y in range(yc + 1, yc + 16):
        M.px(x0, y, "ink")
        M.px(x1 - 1, y, "ink")
    # on the counter: a basket of berries, a stack of balls, a tally board
    M.blit([" kkkkk ", "krorork", "kwwwwwk", " kwwwk "], {"k": "ink", "r": "rd", "o": "ol2", "w": "wd1"},
           x0 + 4, yc - 1)
    M.blit([" kkk  kkk ", "krrrkkrrrk", "kkwkkkkwkk", "kwwwkkwwwk", " kkk  kkk "], {"k": "ink", "r": "rd", "w": "w0"},
           x0 + 34, yc - 1)
    M.blit(["kkkkkkkk", "kpkpkkpk", "kkkkkkkk"], {"k": "ink", "p": "pk3"}, x0 + 18, yc + 1)


def draw_nets(s: Scene):
    """Diktys's nets, heaped against the stern bulkhead: the mesh, a line of
    cork floats along the head rope, lead weights, a mending needle."""
    M = s.M
    x0, y0 = NETS[0] * CELL, NETS[1] * CELL              # 16, 112
    w, hgt = 32, 32
    import math
    for x in range(x0, x0 + w):
        top = y0 + 6 + 4 * math.sin((x - x0) / 32 * math.pi * 1.3) ** 2 - 6 * math.sin((x - x0) / 32 * math.pi)
        for y in range(int(top), y0 + hgt - 1):
            u, v = (x + y) % 5, (x - y) % 5
            c = "rp1" if (u == 0 or v == 0) else "wd0" if (x * 7 + y) % 3 else "wd1"
            if y > y0 + hgt - 6 and c == "wd1":
                c = "wd0"
            M.px(x, y, c)
        M.px(x, int(top) - 1, "ink")
        M.px(x, y0 + hgt - 1, "ink")
    for (fx, fy) in ((x0 + 3, y0 + 4), (x0 + 10, y0 + 1), (x0 + 17, y0 + 2), (x0 + 24, y0 + 6),
                     (x0 + 6, y0 + 16), (x0 + 20, y0 + 18)):
        M.blit([" kk ", "kotk", "kttk", " kk "], {"k": "ink", "o": "tc3", "t": "tc1"}, fx, fy)
    for (lx, ly) in ((x0 + 13, y0 + 26), (x0 + 27, y0 + 24)):
        M.blit(["kk", "kk"], {"k": "ink"}, lx, ly)
    M.blit(["k", "w", "w", "w", "k"], {"k": "ink", "w": "pk3"}, x0 + 28, y0 + 10)


def draw_jars(s: Scene):
    M = s.M
    x0, y0 = JARS[0] * CELL, JARS[1] * CELL
    jar = [
        "  kkkk  ",
        "  k33k  ",
        " kk22kk ",
        "k3222211",
        "k3222211",
        "k3222211",
        "k3222111",
        " k22111k",
        "  k211k ",
        "  k11k  ",
        "   kk   ",
    ]
    M.blit(jar, {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}, x0 + 1, y0 + 4)
    M.blit(jar, {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}, x0 + 7, y0 + 3)


def draw_rug(s: Scene):
    """A woven rug under the mess table: a red field, a blue key border
    (bottom layer, on the floor; it repeats on 8 px so its cells share tiles)."""
    B = s.B
    x0, y0, x1, y1 = RUG
    for x in range(x0, x1):
        for y in range(y0, y1):
            ex = min(x - x0, x1 - 1 - x)
            ey = min(y - y0, y1 - 1 - y)
            e = min(ex, ey)
            if e == 0:
                c = "ink"
            elif e == 1:
                c = "rd0"
            elif e < 5:
                # the border: cream with a blue stripe
                c = "b0" if e == 3 else "rp"
            elif e == 5:
                c = "rd0"
            else:
                c = "rd"
                if (x - x0) % 8 == 4 and (y - y0) % 8 == 4:
                    c = "w0"
                elif (x - x0) % 8 in (3, 5) and (y - y0) % 8 == 4 or \
                        (x - x0) % 8 == 4 and (y - y0) % 8 in (3, 5):
                    c = "rd0"
            B.px(x, y, c)


def sea_chest(M, x, y):
    """A crewman's sea chest, roped shut."""
    M.blit([
        " kkkkkkkkkkkk ",
        "kPPPPPPPPPPPPk",
        "kppppppppppppk",
        "kkkkkkkkkkkkkk",
        "kwwrwwwwwwrwwk",
        "kwwrwwwwwwrwwk",
        "kdwrwwddwwrwdk",
        "kwwrwwwwwwrwwk",
        "kkkkkkkkkkkkkk",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1", "d": "wd0", "r": "rp"}, x + 1, y + 5)


def draw_chests(s: Scene):
    for (cx, cy) in CHESTS:
        sea_chest(s.M, cx * CELL, cy * CELL)
    # the deck's own rope coil and water jar, stowed in the bow: the same art,
    # so the same tiles
    import euploia_deck
    euploia_deck.rope_coil(s.M, *COIL)
    euploia_deck.water_jar(s.M, *WATER_JAR)


def draw_lamps(s: Scene):
    """Oil lamps hung from the beams, warm on the wall."""
    M = s.M
    for col in LAMPS:
        x0 = col * CELL + 4
        for y in range(12, 22):
            M.px(x0 + 3, y, "ink")
        M.blit([
            "   k    ",
            "  kfk   ",
            " kfFfk  ",
            "kppppppk",
            " kpppk  ",
            "  kkk   ",
        ], {"k": "ink", "f": "lt1", "F": "fc", "p": "pk2"}, x0, 20)


# ---------------------------------------------------------------------------
# Assembling
# ---------------------------------------------------------------------------

VARIANTS = ["hearth_cold"] + [f"keepsake_{k}" for k, _, _ in KEEPSAKES]


def draw(variant="base", phase=0):
    s = Scene("below" if variant == "base" else "below_" + variant, W, H)
    beams(s)
    wall(s)
    floor(s)
    edge(s)
    bulkheads(s)
    draw_rug(s)
    draw_ladder(s)
    draw_lamps(s)
    draw_bunk(s)
    draw_iaso(s)
    filled = (variant[len("keepsake_"):],) if variant.startswith("keepsake_") else ()
    if variant == "full_shelf":                       # previews only: every keepsake home
        filled = tuple(k for k, _, _ in KEEPSAKES)
    draw_shelf(s, filled)
    draw_hearth(s, lit=variant != "hearth_cold", phase=phase)
    draw_mess(s)
    draw_table(s)
    draw_pithos(s)
    draw_stall(s)
    draw_nets(s)
    draw_jars(s)
    draw_chests(s)
    s.flatten()
    walkability(s)
    return s


def void():
    """The dark outside the quarters' walls: its layout's border."""
    s = Scene("void", 1, 1)
    s.B.rect(0, 0, CELL, CELL, "ink")
    s.piece("void", "The dark beyond the quarters", 0, 0, 1, 1, "Below deck's border.")
    return s


SOLID = [BUNK, (BUNK[0] + 1, BUNK[1]), CHEST, HEARTH, (HEARTH[0] + 1, HEARTH[1]),
         (PITHOS[0], PITHOS[1] + 1), (PITHOS[0] + 1, PITHOS[1] + 1), (15, 3), (17, 3), JARS,
         TABLE, (TABLE[0] + 1, TABLE[1]), STOOL,
         NETS, (NETS[0] + 1, NETS[1]), (NETS[0], NETS[1] + 1), (NETS[0] + 1, NETS[1] + 1),
         COIL, WATER_JAR] + list(CHESTS)


def walkability(s: Scene):
    for y in range(H):
        for x in range(W):
            s.walk[y][x] = "X"
    for y in range(3, 9):
        for x in range(1, 19):
            s.walk[y][x] = "."
    for (x, y) in SOLID:
        s.walk[y][x] = "X"
    for x in range(15, 18):
        s.set_walk(x, COUNTER, "c", "MB_COUNTER")
    s.set_walk(*LADDER, "w", "MB_LADDER")
    s.piece("bunk", "The bunk", BUNK[0], BUNK[1] - 2, 2, 3,
            "A box bed against the stern, a fleece over it, a linen pillow and a red blanket "
            "folded at the foot; a shelf above with a rolled fleece and a kitbag. The bed (row 3) "
            "is solid; its bg events rest the party, read from row 4.")
    s.piece("iaso_chest", "Iaso's chest and staff", CHEST[0], CHEST[1] - 2, 1, 3,
            "Her chest, open on herbs, linen and a little jar, a snake painted on its front; the "
            "staff of Asclepius leaning on the wall above. The chest (3,3) is solid.")
    s.piece("trophy_shelf", "The trophy shelf", SHELF[0], SHELF[1], 4, 2,
            "Two tiers between side boards: seven keepsake spots, drawn empty (the keepsake_* "
            "variants fill them), and the ship's own painted plaque at (7,2). Bg events on row 2, "
            "read from row 3.")
    s.piece("ladder", "The ladder up to the hatch", LADDER[0], 0, 1, 4,
            "Daylight down the ladder's column and onto the floor at its foot. The foot (8,3) is "
            "MB_LADDER: warp 0, up to the deck's hatch.")
    s.piece("hearth", "Lampon's hearth", HEARTH[0], 0, 2, 4,
            "A raised clay hearth with a cooking pot on three stones over the flames, a clay hood "
            "and flue up through the beams. The hearth (row 3) is solid. Variant hearth_cold: ash "
            "and a dark pot.")
    s.piece("mess", "The mess rack", MESS[0], MESS[1], 2, 2,
            "Bowls, cups and a jug on two shelves, a jar of oil, a ladle on its hook, a string of "
            "onions. On the wall.")
    s.piece("mess_table", "The mess table and stool", STOOL[0], STOOL[1], 3, 1,
            "Bowls, a loaf and a cup on the table; a three-legged stool. Solid.")
    s.piece("pithos", "The Pithos", PITHOS[0], PITHOS[1] - 1, 2, 3,
            "A great storage jar, its lid roped down, relief bands and a black-figure ship sailing "
            "round it. Its two floor cells (row 3) are solid and carry the Pithos's bg events.")
    s.piece("stall", "Kydon's stall", STALL[0], 0, 3, 5,
            "A striped awning from the beam; shelves of Poké Balls, potions, wine, olive oil, "
            "berries, barley cakes, laurel and incense; a sack and a basket either side of Kydon "
            "at (16,3); the counter (row 4, MB_COUNTER) across.")
    s.piece("nets", "Diktys's nets", NETS[0], NETS[1], 2, 2,
            "Heaped against the stern bulkhead: the mesh, cork floats, lead weights, a mending "
            "needle. Solid.")
    s.piece("jars", "Stores in the bow", JARS[0], JARS[1], 1, 1, "Two jars. Solid.")
