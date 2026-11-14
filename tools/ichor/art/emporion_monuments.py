"""Emporion's monuments (gTileset_Emporion).

- The Temple of Hermes: an Ionic front in marble with a marble-tiled roof, a
  gold winged petasos on the apex, gilded wings at the corners, the caduceus on
  spread wings in a blue pediment, a frieze of golden wings, relay torches
  burning between the columns, and tall bronze doors. The city's crown: put it
  on a height at the end of the main street.
- The Asclepeion, Emporion's own: a Corinthian porch (Corinth's order) with the
  rod of Asclepius in its pediment and a blue door.
- The Peirene fountain house: an arcade of dark spring chambers over a drawing
  basin.
- The Hephaisteion above the Agora, with its forge cold or roaring.
- The great herm, garlanded and worn where hands have touched it.
- Street furniture: a marble exedra bench and a laurel planter.

Economy. The fronts are mirror-symmetric about a tile edge (Porytiles stores a
right-hand tile as its left-hand twin, flipped), and the temple, the Asclepeion
and the Hephaisteion share one porch kit: the same column cells and porch wall,
row for row, so their shafts and bases are the same tiles.
"""
from __future__ import annotations

import emporion_lib as E
from emporion_lib import Struct, finish

COLS = ("m4", "m3", "m2", "m1", "w0")
GOLD = {"k": "ink", "G": "g1", "g": "g0", "b": "br"}

# ==========================================================================
# Shared parts
# ==========================================================================


def _roof_planes(L, w, base):
    """A marble-tiled roof seen above a pediment: the ridge runs away from the
    viewer, so each plane shows its tiles in courses running east-west, each
    course lit along its lip. Symmetric about the middle."""
    for y in range(0, base):
        for x in range(w):
            Y = y % 4
            c = "w0" if Y == 0 else "m2" if Y == 3 else "m1"
            L.px(x, y, c)


def _pediment(L, w, top, base, tympanum=("b1", "b0"), cornice=("w0", "m1", "m2")):
    """Roof planes, raking cornices and tympanum over 0..w-1, apex at y=top,
    base at y=base. Symmetric."""
    cx = (w - 1) / 2

    def ytop(x):
        return int(round(top + (base - top) * abs(x - cx) / cx))
    _roof_planes(L, w, base)
    t0, t1 = tympanum
    for x in range(w):
        yt = ytop(x)
        L.px(x, yt - 1, "ink")
        L.px(x, yt, cornice[0])
        L.px(x, yt + 1, cornice[1])
        L.px(x, yt + 2, cornice[2])
        for y in range(yt + 3, base):
            L.px(x, y, t0)
        if yt + 3 < base:
            L.px(x, yt + 3, t1)
    return ytop


def _porch(L, w, y0, rows, columns, capital="ionic"):
    """The shaded porch behind a colonnade, `rows` cell-rows from y0, with
    columns centered on the given cells. Every porch is drawn by this, row for
    row, so the column cells of every building are the same tiles."""
    for y in range(y0, y0 + rows * 16):
        for x in range(w):
            X, Y = x % 16, y - y0
            c = "m4"
            # ashlar courses, each cell mirror-symmetric so a mirrored front's
            # column cells stay the same tiles
            if Y % 8 == 7 or (X in (7, 8) if (Y // 8) % 2 else X in (0, 15)):
                c = "m5"
            L.px(x, y, c)
    L.hline(0, w - 1, y0, "ink")
    L.hline(0, w - 1, y0 + 1, "m5")
    L.hline(0, w - 1, y0 + 2, "m5")


def _columns(L, y0, rows, cells, capital="ionic"):
    bot = y0 + rows * 16
    for c in cells:
        x = c * 16 + 4
        E.shaft(L, x, y0 + 6, 9, bot - 4 - (y0 + 6), ramp=COLS)
        if capital == "ionic":
            E.ionic_capital(L, x, y0 + 1, 9, gold=True)
        elif capital == "corinthian":
            E.corinthian_capital(L, x + 1, y0, 7)
            E.shaft(L, x, y0 + 7, 9, 1, ramp=COLS)
        else:
            E.doric_capital(L, x + 1, y0 + 1, 7)
        # Ionic base: two tori on a plinth
        L.rect(x - 1, bot - 4, 11, 1, "m1")
        L.rect(x - 2, bot - 3, 13, 1, "w0")
        L.rect(x - 2, bot - 2, 13, 2, "m2")
        L.hline(x - 2, x + 10, bot - 1, "m4")
        L.vline(x - 2, bot - 3, bot - 1, "ink")
        L.vline(x + 10, bot - 3, bot - 1, "ink")
        L.px(x - 1, bot - 4, "ink")
        L.px(x + 9, bot - 4, "ink")


def _door(L, cx, y_lintel, y_bot, leaf=("g1", "g0", "br"), studs="g1"):
    """A tall double door centered on cx under a marble lintel, symmetric."""
    hi, body, dark = leaf
    L.rect(cx - 11, y_lintel, 22, 4, "w0")
    L.hline(cx - 11, cx + 10, y_lintel + 3, "m2")
    E.outline_rect(L, cx - 12, y_lintel - 1, 24, 5, "ink")
    y = y_lintel + 4
    L.rect(cx - 10, y, 20, y_bot - y + 1, "w0")
    L.vline(cx - 9, y, y_bot, "m2")
    L.vline(cx + 8, y, y_bot, "m2")
    L.rect(cx - 8, y, 16, y_bot - y + 1, "ink")
    for side in (-1, 1):
        x0 = cx - 7 if side < 0 else cx + 1
        for yy in range(y + 1, y_bot):
            for xx in range(x0, x0 + 6):
                c = body
                if xx == x0 and side < 0 or xx == x0 + 5 and side > 0:
                    c = hi
                if (yy - y) % 9 in (0, 8):
                    c = dark
                L.px(xx, yy, c)
        for yy in range(y + 4, y_bot, 9):
            L.px(x0 + (1 if side < 0 else 4), yy, studs)
            L.px(x0 + (4 if side < 0 else 1), yy, studs)


def _steps(L, w, y0, n=3):
    for k in range(n):
        y = y0 + k * 5
        L.rect(0, y, w, 5, "m1")
        L.hline(0, w - 1, y, "w0")
        L.hline(0, w - 1, y + 3, "m2")
        L.hline(0, w - 1, y + 4, "m4")
    L.hline(0, w - 1, y0 + 15, "m3")


CADUCEUS = [
    "  kGk  ",
    "kGkgkGk",
    "kgGgGgk",
    " kkgkk ",
    "  kgk  ",
    " kGgGk ",
    "kGkgkGk",
    "kgkgkgk",
    " kGgGk ",
    "  kgk  ",
    " kGgGk ",
    "kGkgkGk",
    " kkgkk ",
    "  kgk  ",
    "  kgk  ",
    "  kbk  ",
]
PETASOS = [
    "kk    kkkk    kk",
    "kGk  kGGggk  kGk",
    "kGGkkGGggggkkGGk",
    " kGgGGggggggGgk ",
    "  kGgkkkkkkgGk  ",
    " kGGGGGGggggggk ",
    "  kkkkkkkkkkkk  ",
]
TORCH = [
    "  f  ",
    " fcf ",
    "fcycf",
    "fcycf",
    "kGGGk",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    " kgk ",
    "kkgkk",
    "kgggk",
    "kkkkk",
]

# ==========================================================================
# The Temple of Hermes
# ==========================================================================


def temple_hermes():
    s = Struct("temple_hermes", "Temple of Hermes, exterior", 7, 7,
               walk=["XXXXXXX"] * 5 + ["XXXDXXX", "......."], ground="none",
               notes="The city's crown. A tetrastyle Ionic front in marble under a marble-tiled "
                     "roof: a gold winged petasos on the apex, gilded wings at the corners, the "
                     "caduceus on spread wings in a blue pediment, a dentil cornice over a "
                     "frieze of golden wings, relay torches burning in the side bays, and tall "
                     "bronze doors. Door: row 5, middle column (MB_NON_ANIMATED_DOOR). The step "
                     "row is walkable. Raise it on a terrace at the end of the main street.")
    L = s.B
    W = 112
    _pediment(L, W, 9, 33)
    # spread wings behind the caduceus, filling the tympanum
    for i in range(22):
        h = 1 + (i * 5) // 22
        for j in range(h):
            L.px(55 - i, 27 - j - (22 - i) // 4, "g1" if j < h - 1 else "g0")
        L.px(55 - i, 28 - (22 - i) // 4, "ink")
    L.blit(CADUCEUS, GOLD, 52, 14)
    # the corner acroteria: gilded wings
    L.blit(["       kk", "     kkGk", "   kkGGgk", " kkGGggk ", "kGGggkk  ", "kkkkk    "], GOLD, 0, 26)
    # the apex acroterion: the winged petasos
    L.blit(PETASOS, GOLD, 48, 1)
    # the horizontal cornice with dentils (y 33-37)
    L.hline(0, W - 1, 33, "ink")
    L.hline(0, W - 1, 34, "w0")
    L.hline(0, W - 1, 35, "m1")
    for x in range(W):
        L.px(x, 36, "m3" if x % 4 in (1, 2) else "w0")
    L.hline(0, W - 1, 37, "m4")
    # the winged frieze (y 38-43): golden wings on deep blue, symmetric every 16 px
    WINGS = [
        "bGbbbbbbbbbbbbGb",
        "bGGbbbbbbbbbbGGb",
        "bbGGGbbbbbbGGGbb",
        "bbbGGGGggGGGGbbb",
        "bbbbgggGGgggbbbb",
        "bbbbbbbggbbbbbbb",
    ]
    for y, row in enumerate(WINGS):
        for x in range(W):
            L.px(x, 38 + y, {"b": "b0", "G": "g1", "g": "g0"}[row[x % 16]])
    L.hline(0, W - 1, 44, "w0")
    L.hline(0, W - 1, 45, "m1")
    L.hline(0, W - 1, 46, "m2")
    L.hline(0, W - 1, 47, "m4")
    # the porch, three rows; the bronze doors in cell 3; relay torches in cells 1 and 5
    _porch(L, W, 48, 3, (0, 2, 4, 6))
    _door(L, 56, 58, 95)
    L.blit(TORCH, {**GOLD, "f": "rd", "c": "g1", "y": "w0"}, 22, 75)
    L.blit(["m m", " m "], {"m": "m3"}, 23, 72)
    # the edges
    L.vline(0, 33, 95, "ink")
    E.mirror_half(L, 0, W, 0, 96)
    _columns(L, 48, 3, (0, 2, 4, 6))
    _steps(L, W, 96)
    L.vline(0, 96, 111, "m3")
    L.vline(W - 1, 96, 111, "m3")
    return finish(s)


def asclepeion():
    s = Struct("asclepeion", "Emporion's Asclepeion", 5, 5,
               walk=["XXXXX"] * 4 + ["XXDXX"], ground="none",
               notes="Emporion's healing temple, a sibling of aethos's Asclepeion (0x048): a "
                     "Corinthian porch (Corinth's own order), the rod of Asclepius in gold in a "
                     "blue pediment, a frieze of white rosettes on red, and a tall blue door "
                     "with gold studs. Door: bottom row, middle (MB_NON_ANIMATED_DOOR). Lay the "
                     "broad steps in front of it. Its column cells are the Temple of Hermes's "
                     "own tiles below the capitals.")
    L = s.B
    W = 80
    _pediment(L, W, 1, 16, cornice=("w0", "m1", "rd"))
    L.hline(0, W - 1, 16, "ink")
    L.hline(0, W - 1, 17, "w0")
    L.hline(0, W - 1, 18, "m1")
    L.hline(0, W - 1, 19, "m3")
    for x in range(W):
        X = x % 8
        for y in range(20, 26):
            L.px(x, y, "rd")
        if X in (3, 4):
            L.px(x, 22, "w0")
            L.px(x, 23, "w0")
        if X in (2, 5):
            L.px(x, 22, "m1")
            L.px(x, 23, "m1")
        if X in (3, 4):
            L.px(x, 21, "m1")
            L.px(x, 24, "m1")
    L.hline(0, W - 1, 26, "w0")
    L.hline(0, W - 1, 27, "m1")
    L.hline(0, W - 1, 28, "m2")
    L.hline(0, W - 1, 29, "m2")
    L.hline(0, W - 1, 30, "m3")
    L.hline(0, W - 1, 31, "m4")
    _porch(L, W, 32, 3, (0, 1, 3, 4))
    _door(L, 40, 42, 79, leaf=("b2", "b1", "b0"), studs="g1")
    L.vline(0, 16, 79, "ink")
    E.mirror_half(L, 0, W, 0, 80)
    # the rod of Asclepius: one serpent, so it is drawn after the mirroring
    rod = ["  kk ", " kGgk", " kbk ", "kGk  ", "kgGk ", " kbGk", "  kgk", " kbk ", "  kk "]
    L.blit(rod, GOLD, 37, 5)
    _columns(L, 32, 3, (0, 1, 3, 4), capital="corinthian")
    return finish(s)


def hephaisteion():
    s = Struct("hephaisteion", "The Hephaisteion above the Agora (forge cold)", 4, 4,
               walk=["XXXX", "XXXX", "XXXX", "XDDX"], ground="none",
               notes="Hephaestus's small temple above the Agora (SYSTEMS.md §1, 'The Cold "
                     "Forge'): a red pediment with the god's hammer and tongs in gold, a "
                     "triglyph frieze, and the cella's great doorway, dark while the forge is "
                     "cold. Doors: bottom row, middle two cells. When Kedalion relights the "
                     "forge, swap hephaisteion_lit's four cells over rows 2-3, columns 1-2. "
                     "Its back stair (stair_up) can be blocked by column drums as object "
                     "events for the Girdle gate.")
    L = s.B
    W = 64
    _pediment(L, W, 3, 17, tympanum=("rd", "rd"))
    L.hline(0, W - 1, 17, "ink")
    L.hline(0, W - 1, 18, "w0")
    L.hline(0, W - 1, 19, "m2")
    for x in range(W):
        X = x % 16
        for y in range(20, 25):
            if X in (6, 7, 8, 9):
                L.px(x, y, "br" if X in (7, 8) else "g0")
            else:
                L.px(x, y, "m1")
    L.hline(0, W - 1, 25, "w0")
    L.hline(0, W - 1, 26, "m2")
    L.hline(0, W - 1, 27, "m4")
    for y in range(28, 32):
        L.hline(0, W - 1, y, "m5" if y > 28 else "ink")
    _porch(L, W, 32, 2, (0, 3))
    # the great doorway: dark, the cold forge only a shape inside
    L.rect(19, 36, 13, 28, "ink")
    L.hline(18, 31, 35, "w0")
    L.vline(18, 35, 63, "w0")
    L.vline(19, 36, 63, "m2")
    L.blit(["    kkk", "   km55", "  km555", " kkkkkk"], {"k": "m5", "m": "m4", "5": "m5"}, 25, 54)
    L.vline(0, 17, 63, "ink")
    E.mirror_half(L, 0, W, 0, 64)
    # the hammer and the tongs, drawn after the mirroring
    L.blit(["kkkkk", "kGggk", "kkgkk", "  gk ", "  gk ", "  bk "], GOLD, 24, 8)
    L.blit(["k   k", "kG kG", " kGk ", " kgk ", "kg gk", "b   b"], GOLD, 34, 8)
    _columns(L, 32, 2, (0, 3), capital="doric")
    return finish(s)


def hephaisteion_lit():
    s = Struct("hephaisteion_lit", "The Hephaisteion's doorway with the forge roaring", 2, 2,
               walk=["XX", "DD"], ground="none",
               notes="Swap these over hephaisteion's cells (1,2), (2,2), (1,3) and (2,3) once "
                     "the forge is lit: firelight fills the doorway and the anvil stands black "
                     "against it. Keep the bottom row MB_NON_ANIMATED_DOOR.")
    L = s.B
    base = hephaisteion()
    L.a[:] = base.B.a[32:64, 16:48]
    # the dark cella, the hearth burning at its back: a low glow round the fire,
    # its light on the floor and the jambs, sparks rising; symmetric
    for y in range(4, 32):
        for x in range(3, 16):
            r = ((x - 15.5) ** 2 / 2.2 + (y - 27) ** 2) ** 0.5
            c = "ink"
            if r < 3:
                c = "w0"
            elif r < 5:
                c = "g1"
            elif r < 7.5:
                c = "g0"
            elif r < 10:
                c = "rd"
            elif r < 12 and (x + y) % 2:
                c = "br"
            L.px(x, y, c)
    for (x, y) in ((12, 14), (14, 11), (10, 17), (13, 8)):
        L.px(x, y, "g1")
    # the light on the jambs
    for y in range(18, 32):
        L.px(3, y, "rd" if y % 2 else "br")
    # the anvil, black against the fire
    L.blit(["kkkkkkkkkk", " kkkkkkkkk", "     kkkk ", "    kkkkkk"], {"k": "ink"}, 6, 21)
    E.mirror_half(L, 0, 32, 0, 32)
    return finish(s)


def peirene():
    s = Struct("peirene", "The Peirene fountain house", 5, 3, walk=["XXXXX"] * 3, ground="none",
               notes="Corinth's sacred spring, where Bellerophon caught Pegasus: an Ionic "
                     "entablature with a frieze of waves over an arcade of dark spring "
                     "chambers, each with a bronze spout, over a marble drawing basin. The "
                     "middle three cells are the same tiles, so it can be made longer or "
                     "shorter. Give the basin a bg event: 'The water is cold and very sweet.'")
    L = s.B
    W = 80
    L.rect(0, 0, W, 16, "m1")
    L.hline(0, W - 1, 0, "ink")
    L.hline(0, W - 1, 1, "w0")
    L.hline(0, W - 1, 2, "m2")
    for x in range(W):
        X = x % 8
        wave = [3, 2, 2, 3, 4, 5, 5, 4][X]
        for y in range(3, 9):
            L.px(x, y, "b1" if y - 3 >= wave - 2 else "w0")
        L.px(x, 3 + wave - 2, "b2")
    L.hline(0, W - 1, 9, "m3")
    L.hline(0, W - 1, 10, "w0")
    L.hline(0, W - 1, 11, "m2")
    for c in range(5):
        x0 = c * 16
        for y in range(12, 32):
            for x in range(x0 + 4, x0 + 16):
                dx = x - (x0 + 9.5)
                top = 18 - (36 - dx ** 2) ** 0.5 if abs(dx) <= 6 else 99
                if y >= top:
                    L.px(x, y, "ink")
        for x in range(x0 + 3, x0 + 17):
            dx = x - (x0 + 9.5)
            if abs(dx) <= 7:
                y = int(round(18 - (49 - dx ** 2) ** 0.5))
                L.px(x, y, "m3")
                L.px(x, y - 1, "w0")
        for x in range(x0 + 5, x0 + 15):
            L.px(x, 28, "b0")
            L.px(x, 29, "b1" if x % 3 else "b2")
            L.px(x, 30, "b0")
        L.blit(["gGg", " g ", " b "], {"g": "g0", "G": "g1", "b": "b2"}, x0 + 8, 21)
        L.vline(x0 + 9, 24, 27, "b2")
        L.rect(x0, 12, 4, 20, "m2")
        L.vline(x0, 12, 31, "ink")
        L.vline(x0 + 1, 13, 31, "w0")
        L.vline(x0 + 3, 12, 31, "m4")
    L.rect(W - 4, 12, 4, 20, "m3")
    L.vline(W - 1, 12, 31, "ink")
    L.vline(W - 3, 13, 31, "m2")
    L.vline(W - 4, 12, 31, "ink")
    for x in range(W):
        for y in range(32, 38):
            L.px(x, y, "b1")
        X = x % 16
        if X in (3, 4):
            L.px(x, 33, "b3" if X == 3 else "b2")
        if X == 11:
            L.px(x, 35, "b2")
    L.hline(0, W - 1, 32, "b0")
    L.hline(0, W - 1, 38, "w0")
    L.hline(0, W - 1, 39, "m1")
    for y in range(40, 47):
        for x in range(W):
            X = x % 16
            c = "m2"
            if 2 <= X <= 13 and y in (41, 45):
                c = "m3"
            if X in (2, 13) and 41 <= y <= 45:
                c = "m3"
            if X == 0:
                c = "m4"
            L.px(x, y, c)
    L.hline(0, W - 1, 47, "m5")
    L.vline(0, 0, 47, "ink")
    L.vline(W - 1, 0, 47, "ink")
    return finish(s)


def great_herm(ground="pave"):
    key = "great_herm" if ground == "pave" else "great_herm_grass"
    s = Struct(key, "Great herm" + ("" if ground == "pave" else ", on grass"), 1, 2,
               walk=["T", "X"], ground=ground,
               notes="A garlanded pillar with Hermes's bearded head, darker where hands have "
                     "touched it (SYSTEMS.md §4). Kerykos teaches anointing at this one. The "
                     "top cell draws over the player; give the bottom cell the bg event."
                     + (" On aethos grass; its tiles are great_herm's." if ground == "grass"
                        else " On paving."))
    T, M = s.T, s.M
    # a bearded head, its marble darkened by hands (so it stands out on the paving)
    head = [
        "   kkkkkk   ",
        "  k333333k  ",
        " k32222223k ",
        " k2kk22kk2k ",
        " k22222222k ",
        " k32211223k ",
        "  k333333k  ",
        "  k343343k  ",
        "   k3443k   ",
        "    k44k    ",
    ]
    T.blit(head, {"k": "ink", "2": "m1", "1": "m2", "3": "m3", "4": "m4"}, 2, 6)
    for y in range(16, 30):
        M.hline(4, 11, y, "m2")
        M.px(4, y, "ink")
        M.px(11, y, "ink")
        M.px(5, y, "m1")
        M.px(10, y, "m3")
        M.px(9, y, "m3")
    for (x, y) in ((7, 20), (8, 20), (7, 21), (8, 22), (6, 22)):
        M.px(x, y, "m3")
    for x in range(4, 12):
        y = 17 + (1 if 5 <= x <= 10 else 0) + (1 if 6 <= x <= 9 else 0)
        M.px(x, y, "rd" if x % 2 else "g1")
    M.vline(3, 17, 20, "rd")
    M.vline(12, 17, 20, "rd")
    M.rect(3, 29, 10, 3, "m2")
    M.hline(3, 12, 29, "w0")
    M.hline(2, 13, 31, "ink")
    M.px(2, 30, "ink")
    M.px(13, 30, "ink")
    return finish(s)


def street_furniture():
    s = Struct("exedra", "Marble exedra bench", 2, 1, walk=["XX"],
               notes="A curved marble bench with lion's-foot ends, for squares and the "
                     "Peirene's court. Sit townsfolk beside it.")
    M = s.M
    M.rect(1, 4, 30, 6, "m1")
    M.hline(1, 30, 4, "w0")
    M.hline(1, 30, 9, "m3")
    M.rect(1, 10, 30, 2, "m2")
    M.hline(0, 31, 3, "ink")
    M.hline(0, 31, 12, "ink")
    M.vline(0, 3, 12, "ink")
    M.vline(31, 3, 12, "ink")
    for x in (2, 27):
        M.rect(x, 10, 3, 4, "m3")
        M.hline(x - 1, x + 3, 14, "ink")
    M.hline(3, 28, 13, "m4")
    E.mirror_half(M, 0, 32, 0, 16)
    return [finish(s)]


def planter():
    s = Struct("planter", "A clipped laurel in a great terracotta pot", 1, 2,
               walk=["T", "X"],
               notes="For squares, doorways and the temple's terrace. One cell wide, two tall; "
                     "the laurel's head draws over the player.")
    T, M = s.T, s.M
    m = E.ellipse_mask(13, 12)
    E.fill_mask(T, m, 1, 4, "c2")
    for y in range(4, 16):
        for x in range(1, 14):
            if T.get(x, y) == "c2":
                if (x + y) % 5 == 0:
                    T.px(x, y, "c3")
                if x > 8 and y > 10:
                    T.px(x, y, "c1")
                if x < 6 and y < 9 and (x + y) % 2 == 0:
                    T.px(x, y, "ov3")
    E.silhouette_outline(T, (0, 0, 16, 16), "ink")
    M.vline(7, 16, 18, "tk0")
    M.blit(["kkkkkkkkkkkk", "k2222222211k", " k22222211k ", " k22222211k ", " k22222111k ",
            "  k221111k  ", "  kkkkkkkk  "], {"k": "ink", "2": "tc2", "1": "tc1"}, 2, 19)
    M.hline(3, 12, 20, "tk0")
    return finish(s)


def build():
    # ordered so the shelf packer fills the columns beside the big fronts
    return ([temple_hermes(), great_herm("pave"), asclepeion()] + street_furniture()
            + [planter(), hephaisteion(), hephaisteion_lit(), great_herm("grass"), peirene()])
