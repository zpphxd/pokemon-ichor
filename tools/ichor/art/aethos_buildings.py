"""Buildings: the Asclepeion (Pokemon Center) and the Agora stoa (Mart).

Both keep General's 4x4 footprints, doors and behaviors:

  Asclepeion  048 049 04A 04B / 050-053 / 058-05B / 060 061 062 063
  Agora       028 029 029 02B / 030-033 / 038-03B / 060 041 042 043
              (02A is unused; the Agora roof repeats 029 in the middle)

Both fronts share one rhythm, so they can share General's bottom-left corner
(060): an anta (pilaster) at each end and Doric columns at x = 16, 32, 48 of
the 64 px front. The door (061 / 041) opens between the first two columns.

  Asclepeion: a white marble temple front. Pediment with gold acroteria and a
    gilded rod of Asclepius in the tympanum, a painted frieze (blue
    triglyphs), fluted columns over a shadowed cella, three steps, an Aegean
    door, and a small marble plaque with the rod beside it.
  Agora: a market stoa. A long terracotta roof, a cream-and-clay striped
    awning, and goods between the columns: amphorae, baskets of olives and
    figs, a bolt of Aegean cloth. A painted pinax with an amphora hangs by
    the curtained door.

Drawn on 64x64 canvases with small helpers (columns, steps, tile courses)
and hand-drawn ASCII motifs, then cut into metatiles. Roof rows are on the
top layer over grass, as General's were.
"""
import numpy as np

from aethos_lib import art, rgba, over, B, M, T
from aethos_textures import TEX

LEG = dict(K="ink", H="mb_h", L="mb_l", C="lp_l", M="mb_m", D="mb_d", P="lp_d",
           T="tc_m", t="tc_l", R="tc_d", G="sg_l", g="sg_d",
           E="ae_m", e="ae_l", A="ae_d")


class Canvas:
    def __init__(self, w=64, h=64):
        self.a = np.zeros((h, w, 4), np.uint8)

    def px(self, x, y, c):
        if 0 <= y < self.a.shape[0] and 0 <= x < self.a.shape[1]:
            self.a[y, x] = rgba(LEG[c]) if c in LEG else rgba(c)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def blit(self, img, x, y):
        h, w = img.shape[:2]
        sub = self.a[y:y + h, x:x + w]
        over(sub, img[:sub.shape[0], :sub.shape[1]])


# --------------------------------------------------------------------------
# Shared parts
# --------------------------------------------------------------------------
COLUMNS = (16, 32, 48)
# A fluted Doric shaft, 7 px with its outline: lit from the left.
SHAFT = ["K", "H", "L", "L", "M", "D", "K"]

CAPITAL = art("""
    KKKKKKKKKK
    KHHHHHHHLK
    .KLLLLLMK.
    ..KMMMDK..
""", LEG)
COL_BASE = art("""
    .KHLLLMDK.
    KHHHHHHMDK
""", LEG)


def column(c, cx, y_cap, y_base):
    """Doric column centred on cx: capital at y_cap, base ending y_base."""
    x0 = cx - 3
    for y in range(y_cap + 4, y_base - 1):
        for i, col in enumerate(SHAFT):
            c.px(x0 + i, y, col)
        if (y - y_cap) % 2 == 0:       # flute shadows
            c.px(x0 + 2, y, "L")
            c.px(x0 + 4, y, "D")
    c.blit(CAPITAL, cx - 5, y_cap)
    c.blit(COL_BASE, cx - 5, y_base - 1)


def anta(c, x0, y0, y1, right=False):
    """A square pilaster closing the colonnade at one end."""
    cols = ["K", "H", "L", "M", "K"] if not right else ["K", "L", "M", "D", "K"]
    for y in range(y0, y1 + 1):
        for i, col in enumerate(cols):
            c.px(x0 + i, y, col)
    c.hline(x0 - 1, x0 + 5, y0, "K")
    c.hline(x0, x0 + 4, y0 + 1, "H")


def steps(c, y0):
    """Stylobate and two steps, the full width."""
    for y, col in ((y0, "H"), (y0 + 1, "L"), (y0 + 2, "D"),
                   (y0 + 3, "H"), (y0 + 4, "M"), (y0 + 5, "D"),
                   (y0 + 6, "L"), (y0 + 7, "M")):
        c.hline(0, 63, y, col)


def cella(c, y0, y1):
    """The shadowed wall behind the columns."""
    c.rect(0, y0, 63, y1, "D")
    c.hline(0, 63, y0, "K")
    c.hline(0, 63, y0 + 1, "K")
    for y in range(y0 + 5, y1 + 1, 5):   # ashlar courses catching a little light
        c.hline(0, 63, y, "M")


# --------------------------------------------------------------------------
# Asclepeion
# --------------------------------------------------------------------------
# Gilded rod of Asclepius for the tympanum (staff with a coiled serpent).
ROD = art("""
    ..gG...
    ..GKg..
    ...Kg..
    .gGK...
    G..KGg.
    .gGK..g
    ...KGg.
    ..gK...
    ...K...
""", LEG)
ACRO = art("""
    .G.
    GgG
    .g.
""", LEG)
# The plaque beside the door: a small stele with the rod, on the cella wall.
PLAQUE = art("""
    ..KKKKK..
    .KHHHHLK.
    KHLLGLLMK
    KHLLGgLMK
    KHLGgLLMK
    KHLLGgLMK
    KHLGLLLMK
    KHLLGLLMK
    KHLLLLLMK
    KKKKKKKKK
""", LEG)
DOOR = art("""
    KKKKKKKKKKK
    KHHHHHHHHMK
    KHKKKKKKKMK
    KHKeEEEeKMK
    KHKEEgEEKMK
    KHKeEEEeKMK
    KHKEEEEEKMK
    KHKeEEEeKMK
    KHKEEgEEKMK
    KHKeEEEeKMK
    KHKEEEEEKMK
    KHKEEEEEKMK
    KHKAAAAAKMK
""", LEG)


def asclepeion():
    c = Canvas()
    # pediment, y 0-15: a low triangle, apex at x 31-32
    for x in range(64):
        d = min(x, 63 - x)               # distance from the nearer corner
        top = 14 - d * 12 // 31          # roof line
        c.px(x, top, "t")
        c.px(x, top + 1, "T")
        c.px(x, top + 2, "R")
        for y in range(top + 3, 14):
            c.px(x, y, "L")
        if top + 3 < 14:
            c.px(x, 13, "M")
    c.hline(0, 63, 14, "H")
    c.hline(0, 63, 15, "D")
    c.blit(ROD, 29, 4)
    c.blit(ACRO, 30, 0)
    c.blit(ACRO, 0, 10)
    c.blit(ACRO, 61, 10)
    # entablature, y 16-26
    c.hline(0, 63, 16, "K")
    c.hline(0, 63, 17, "H")
    c.hline(0, 63, 18, "M")
    for x in range(64):                  # frieze: blue triglyphs, marble metopes
        k = x % 8
        for y in range(19, 24):
            if k in (0, 1, 2, 3):
                col = "A" if k in (0, 2) else "E"
            else:
                col = "L" if k != 7 else "M"
            c.px(x, y, col)
    c.hline(0, 63, 24, "K")
    c.hline(0, 63, 25, "L")
    c.hline(0, 63, 26, "M")
    c.hline(0, 63, 27, "D")
    # cella and colonnade, y 28-55
    cella(c, 28, 55)
    c.blit(DOOR, 19, 43)
    c.blit(PLAQUE, 36, 40)
    for cx in COLUMNS:
        column(c, cx, 28, 56)
    anta(c, 0, 28, 55)
    anta(c, 59, 28, 55, right=True)
    # steps, y 56-63
    steps(c, 56)
    return c.a


# --------------------------------------------------------------------------
# Agora
# --------------------------------------------------------------------------
AMPHORA = art("""
    ..KKK..
    .KtRK..
    KKTTTKK
    KtTTTRK
    KtTTTRK
    .KtTRK.
    ..KTK..
    ..KRK..
""", LEG)
BASKET = art("""
    .EgEgEg.
    KgggGggK
    KgGgGgRK
    KRgRgRRK
    .KKKKKK.
""", dict(LEG, E="ink"))
FIGS = art("""
    .tRtR.
    KgggGK
    KRgRgK
    .KKKK.
""", LEG)
CLOTH = art("""
    KKKK
    KeEK
    KeEK
    KEAK
    KeEK
    KEAK
    KKKK
""", LEG)
PINAX = art("""
    ...K...
    ..K.K..
    KKKKKKK
    KCCCCCK
    KCRTRCK
    KCRTTCK
    KCCRCCK
    KKKKKKK
""", LEG)
CURTAIN = art("""
    KKKKKKKKKK
    KeEeEeEeEK
    KeEeEeEeEK
    KeEAEeEAEK
    KeEAEeEAEK
    KeEAEeEAEK
    KEEAEEEAEK
    KEAAEEAAEK
    KEAAEEAAEK
    KEAAEEAAEK
    KEAAEEAAEK
    KAAAAAAAAK
""", LEG)


def agora():
    c = Canvas()
    # roof, y 4-15: terracotta courses with cover-tile ridges every 4 px; the
    # end bays slope down to the corners.
    for x in range(64):
        d = min(x, 63 - x)
        top = 4 if d >= 8 else 4 + (8 - d)
        c.px(x, top, "R")
        for y in range(top + 1, 15):
            k = x % 4
            col = "t" if k == 0 else ("T" if k in (1, 2) else "R")
            if (y - top) % 4 == 0:
                col = "R"
            c.px(x, y, col)
    c.hline(0, 63, 15, "K")
    # eaves with palmette antefixes, y 16-18
    c.hline(0, 63, 16, "H")
    c.hline(0, 63, 17, "M")
    c.hline(0, 63, 18, "D")
    for x in range(1, 64, 4):
        c.px(x, 17, "H")
        c.px(x + 1, 17, "G")
        c.px(x, 18, "M")
    # striped awning, y 18-29, scalloped hem
    for x in range(64):
        stripe = (x // 4) % 2
        for y in range(19, 28):
            c.px(x, y, ("C" if stripe else "T") if y > 19 else "R")
        hem = 28 + (1 if x % 4 in (1, 2) else 0)
        for y in range(28, hem + 1):
            c.px(x, y, "C" if stripe else "T")
        c.px(x, hem + 1, "K")
    # shade under the awning, then the colonnade
    cella(c, 30, 55)
    c.hline(0, 63, 30, "K")
    # goods between the columns (bays at x 4-12, 35-44, 51-58)
    c.blit(BASKET, 4, 35)
    c.blit(AMPHORA, 5, 40)
    c.blit(FIGS, 37, 49)
    c.blit(AMPHORA, 38, 41)
    c.blit(CLOTH, 41, 46)
    c.blit(BASKET, 51, 50)
    c.blit(AMPHORA, 52, 41)
    c.blit(CURTAIN, 19, 43)
    c.blit(PINAX, 37, 33)
    for cx in COLUMNS:
        column(c, cx, 31, 56)
    anta(c, 0, 31, 55)
    anta(c, 59, 31, 55, right=True)
    steps(c, 56)
    return c.a


def cut(img, r, col):
    return img[r * 16:r * 16 + 16, col * 16:col * 16 + 16].copy()


def paint(sheet, base):
    grass = TEX["grass"]

    def place(m, layer, tile, ground=None):
        sheet.clear(m)
        if ground is not None:
            sheet.set(m, ground, grass)
        sheet.set(m, layer, tile)

    a = asclepeion()
    ids = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
           [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
    for r, row in enumerate(ids):
        for col, m in enumerate(row):
            t = cut(a, r, col)
            if r == 0:
                place(m, T, t, ground=M)          # roof over grass
            elif r < 3:
                place(m, M, over(grass.copy(), t) if not t[..., 3].all() else t)
            elif m == 0x061:
                place(m, B, t)                    # door: bottom layer, as General
            elif m == 0x062:
                place(m, B, t)
            else:
                place(m, M, t, ground=B)

    g = agora()
    ids = [[0x028, 0x029, None, 0x02B], [0x030, 0x031, 0x032, 0x033],
           [0x038, 0x039, 0x03A, 0x03B], [None, 0x041, 0x042, 0x043]]
    for r, row in enumerate(ids):
        for col, m in enumerate(row):
            if m is None:
                continue
            t = cut(g, r, col)
            if r == 0:
                place(m, T, t, ground=M)
            elif r < 3:
                place(m, M, over(grass.copy(), t) if not t[..., 3].all() else t)
            elif m == 0x041:
                place(m, B, t)
            elif m == 0x042:
                place(m, B, t)
            else:
                place(m, M, t, ground=B)
    # 02A: General's unused roof slot, kept as a plain roof bay
    sheet.clear(0x02A)
