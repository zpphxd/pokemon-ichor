"""Thyrsa's public buildings and sacred places (gTileset_Thyrsa).

- The Temple of Dionysus: the city's crown. Its front is a theater's skene: a
  low pediment with the god's masks, comic and tragic, in gold on wine-red, a
  frieze of golden vines, and three painted doors (the comic door with ivy,
  the palace door with a crown, the satyr door with a goat). Only the palace
  door opens.
- Thyrsa's Asclepeion, a sibling of Act I's: a white pediment with the gold
  rod, a blue frieze, grey columns and a blue door; Thyrsa's ivy on it.
- The fountain house of Dirke: lion spouts over a long basin.
- Semele's chamber: a roofless ruin on the Kadmeia wrapped in ivy, smoke
  curling from a crack in its floor.
"""
from __future__ import annotations

import math

import emporion_lib as E
import thyrsa_lib as T
from thyrsa_lib import finish, struct

GOLD = {"k": "ink", "G": "g1", "g": "g0", "b": "br"}


def _pediment(L, w, top, base, tymp="rd0", tymp2="rd"):
    cx = (w - 1) / 2
    for y in range(0, base):
        for x in range(w):
            Y = y % 4
            L.px(x, y, "w0" if Y == 0 else "m2" if Y == 3 else "m1")
    for x in range(w):
        yt = int(round(top + (base - top) * abs(x - cx) / cx))
        L.px(x, yt - 1, "ink")
        L.px(x, yt, "w0")
        L.px(x, yt + 1, "m1")
        L.px(x, yt + 2, "m3")
        for y in range(yt + 3, base):
            L.px(x, y, tymp)
        if yt + 3 < base:
            L.px(x, yt + 3, tymp2)
    for x in range(w):
        L.px(x, base, "ink")


def _column(L, x, y0, y1):
    """A grey marble Doric column, 8 px wide, capital at y0, base at y1."""
    L.rect(x - 1, y0, 10, 3, "m1")
    L.hline(x - 1, x + 8, y0, "w0")
    L.hline(x - 1, x + 8, y0 + 2, "m3")
    L.vline(x - 1, y0, y0 + 2, "ink")
    L.vline(x + 8, y0, y0 + 2, "ink")
    for y in range(y0 + 3, y1 - 2):
        for i, c in enumerate(("ink", "m2", "w0", "m1", "m2", "m1", "m3", "ink")):
            L.px(x + i, y, c)
    L.rect(x - 1, y1 - 2, 10, 2, "m2")
    L.hline(x - 1, x + 8, y1 - 2, "w0")
    L.hline(x - 1, x + 8, y1 - 1, "m4")
    L.vline(x - 1, y1 - 2, y1 - 1, "ink")
    L.vline(x + 8, y1 - 2, y1 - 1, "ink")


def _ashlar_wall(L, x0, y0, w, h):
    """The porch's back wall: grey ashlar, each cell mirror-symmetric."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - x0) % 16, y - y0
            c = "m4"
            if Y % 8 == 7 or (X in (7, 8) if (Y // 8) % 2 else X in (0, 15)):
                c = "m5"
            elif Y % 8 == 0:
                c = "m3"
            L.px(x, y, c)


# ==========================================================================
# The Temple of Dionysus
# ==========================================================================

MASK_GOLD_COMIC = [
    "  kkkkkkkk  ",
    " kGGGGGGGGk ",
    "kGGGGGGGGGGk",
    "kGkkGGGGkkGk",
    "kGGGGGGGGGGk",
    "kGGgGGGGgGGk",
    "kGgrrrrrrgGk",
    " kgrkkkkrgk ",
    "  kgrrrrgk  ",
    "   kkkkkk   ",
]
MASK_GOLD_TRAGIC = [
    "  kkkkkkkk  ",
    " kGGGGGGGGk ",
    "kGGkGGGGkGGk",
    "kGkkkGGkkkGk",
    "kGGGGGGGGGGk",
    "kGGgGGGGgGGk",
    "kGGGgkkgGGGk",
    " kGGkrrkGGk ",
    "  kGgkkgGk  ",
    "   kkkkkk   ",
]


def temple():
    s = struct("temple", "Temple of Dionysus, the skene front", 8, 4,
               walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXDDXXX"], ground="none",
               section="civic",
               notes="The crown of Thyrsa, at the head of the main street on the Kadmeia: a "
                     "temple whose front is a theater's skene. A low pediment with the god's "
                     "masks, comic and tragic, in gold on wine-red; a frieze of golden vines "
                     "on red; and three painted doors between grey columns: the comic door "
                     "(ivy), the palace door (a gold crown on purple, double, the real door) "
                     "and the satyr door (a goat). Doors: bottom row, columns 3-4 "
                     "(MB_NON_ANIMATED_DOOR); give both the temple's warp. Lay the broad steps "
                     "below it, eight cells wide.")
    L = s.B
    W = 128
    _pediment(L, W, 2, 15)
    # the frieze: golden vine scrolls on red, between dentils
    for x in range(W):
        L.px(x, 16, "w0")
        L.px(x, 17, "m3" if x % 4 in (1, 2) else "w0")
        L.px(x, 18, "m4")
        for y in range(19, 28):
            L.px(x, y, "rd0")
        L.px(x, 28, "m4")
        L.px(x, 29, "w0")
        L.px(x, 30, "m2")
        L.px(x, 31, "m4")
    for x in range(W):
        X = x % 16
        yv = 23 + int(round(2.5 * __import__("math").sin(X / 16 * 6.283)))
        L.px(x, yv, "g1")
        L.px(x, yv + 1, "g0")
        if X in (4, 12):
            L.blit([" G ", "GgG", " g "], GOLD, x - 1, 19 if X == 4 else 25)
        if X == 8:
            L.blit(["g", "G"], GOLD, x, 21)
    # the skene wall and its columns
    _ashlar_wall(L, 0, 32, W, 32)
    for x in (2, 36, 84, 118):
        _column(L, x, 32, 64)
    L.vline(0, 16, 63, "ink")
    E.mirror_half(L, 0, W, 0, 64)
    L.vline(W - 1, 16, 63, "ink")
    # the masks in the tympanum, after mirroring: comic left, tragic right
    L.blit(MASK_GOLD_COMIC, {**GOLD, "r": "rd"}, 51, 4)
    L.blit(MASK_GOLD_TRAGIC, {**GOLD, "r": "rd"}, 65, 4)
    # little gold masks on the corner acroteria
    for x0 in (2, 118):
        L.blit([" kkkk ", "kGGGGk", "kGkGkk", "kgggGk", " kkkk "], GOLD, x0, 9)
    # the three painted doors, in the festival's colors, whole cells
    D = s.B
    # door cells: (1) ivy, (3)-(4) the palace, (6) goat; rows 2-3
    def door(x0, w, body, deco):
        D.rect(x0, 32, w, 32, "w0")
        D.rect(x0 + 1, 33, w - 2, 31, "ink")
        D.rect(x0 + 2, 34, w - 4, 30, body)
        D.hline(x0 + 2, x0 + w - 3, 34, "w0")
        for y in range(36, 64, 9):
            D.hline(x0 + 3, x0 + w - 4, y, "ink")
        deco(x0, w)

    def ivy(x0, w):
        # an ivy wreath round a comic mask on the upper panel
        D.blit([" 2121 ", "2kkkk1", "1wwww2", "kwkwkk", "2wrrw1", " kkkk ", " 1  2 "],
               {"k": "ink", "w": "w0", "r": "rd", "1": "iv2", "2": "iv3"}, x0 + 5, 38)

    def goat(x0, w):
        D.blit(["k    k", "kk  kk", " kwwk ", "kwkwkk", " kwwk ", "  kk  ", "  w   "],
               {"k": "ink", "w": "w0"}, x0 + 5, 38)

    def palace(x0, w):
        D.blit(["k  k  k", "kGkGkGk", "kGGGGGk", "kgggggk", "kkkkkkk"], {"k": "ink", "G": "g1", "g": "g0"},
               x0 + w // 2 - 3, 39)
        for y in range(36, 63):
            D.px(x0 + w // 2 - 1, y, "ink")
            D.px(x0 + w // 2, y, "ink")
        for (xx, yy) in ((x0 + 8, 50), (x0 + w - 9, 50), (x0 + 8, 57), (x0 + w - 9, 57)):
            D.px(xx, yy, "g1")

    door(16, 16, "vp0", ivy)
    door(48, 32, "vp1", palace)
    door(96, 16, "vp0", goat)
    s.names = {"door": (3, 3), "door_r": (4, 3)}
    return finish(s)


# ==========================================================================
# The Asclepeion and the fountain of Dirke
# ==========================================================================

ROD = ["  kk ", " kGgk", " kbk ", "kGk  ", "kgGk ", " kbGk", "  kgk", " kbk ", "  kk "]


def asclepeion():
    s = struct("asclepeion", "Thyrsa's Asclepeion", 5, 4,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXDXX"], ground="none", section="civic",
               notes="Thyrsa's healing house, a sibling of Act I's Asclepeion (aethos 0x048): "
                     "a white pediment with the gold rod at its apex, a blue triglyph frieze, "
                     "grey Doric columns, the rod of Asclepius on a gold plaque "
                     "and a tall blue door. Door: bottom row, middle (MB_NON_ANIMATED_DOOR). "
                     "The fountain house of Dirke stands in front of it. Its top row stands "
                     "on the flags.")
    s.ground_rows(["ppppp", "nnnnn", "nnnnn", "nnnnn"])
    L = s.B
    W = 80
    # pediment: white, with the rod in gold at the apex
    cx = (W - 1) / 2
    for y in range(0, 16):
        for x in range(W):
            L.px(x, y, "w0" if y % 4 == 0 else ("m1" if y % 4 != 3 else "m2"))
    for x in range(W):
        yt = int(round(3 + 11 * abs(x - cx) / cx))
        for y in range(0, yt):
            L.a[y, x] = 0
        L.px(x, yt, "ink")
        L.px(x, yt + 1, "rd")
        L.px(x, yt + 2, "w0")
    # the frieze: blue triglyphs and white metopes
    for x in range(W):
        X = x % 16
        L.px(x, 16, "ink")
        L.px(x, 17, "w0")
        for y in range(18, 26):
            L.px(x, y, ("b1" if X in (1, 3) else "b0") if X < 5 else "w0")
        L.px(x, 26, "m2")
        L.px(x, 27, "m4")
    # porch
    _ashlar_wall(L, 0, 28, W, 36)
    for x in (4, 20):
        _column(L, x, 28, 64)
    # the door
    L.rect(29, 34, 22, 30, "w0")
    E.outline_rect(L, 28, 33, 24, 31, "ink")
    L.rect(32, 37, 16, 27, "b1")
    L.vline(39, 37, 63, "ink")
    L.vline(40, 37, 63, "ink")
    for y in range(41, 63, 6):
        L.px(35, y, "g1")
        L.px(44, y, "g1")
    L.hline(32, 47, 37, "b2")
    L.vline(0, 0, 63, "ink")
    E.mirror_half(L, 0, W, 0, 64)
    # the rod at the apex and on a plaque by the door (after mirroring)
    L.blit(ROD, GOLD, 37, 4)
    L.blit(["kkkkkkk", "kGGGGGk", "kG   Gk", "kG   Gk", "kG   Gk", "kG   Gk", "kGGGGGk", "kkkkkkk"],
           GOLD, 55, 40)
    L.blit(ROD, GOLD, 56, 39)
    for yy in range(41, 47):
        for xx in range(57, 61):
            if L.get(xx, yy) is None:
                L.px(xx, yy, "w0")
    s.names = {"door": (2, 3)}
    return finish(s)


def fountain():
    s = struct("dirke", "The fountain house of Dirke", 3, 2, walk=["XXX", "XXX"], ground="pave",
               section="civic",
               notes="The spring of Dirke's fountain house, before the Asclepeion: a white "
                     "entablature on two short columns, two bronze lion heads pouring into "
                     "a long marble basin. Give the basin a bg event (the Heart Scale is "
                     "hidden here).")
    L = s.M
    W = 48
    for x in range(W):
        L.px(x, 0, "ink")
        L.px(x, 1, "w0")
        L.px(x, 2, "m1")
        for y in range(3, 7):
            L.px(x, y, "b0" if x % 8 < 2 else "w0")
        L.px(x, 7, "m3")
        L.px(x, 8, "ink")
    # the spring chambers, dark, with lion spouts
    for x in range(1, W - 1):
        for y in range(9, 22):
            L.px(x, y, "m5")
    for x0 in (1, W - 6):
        L.rect(x0, 9, 5, 13, "m1")
        L.vline(x0, 9, 21, "ink")
        L.vline(x0 + 4, 9, 21, "ink")
        L.vline(x0 + 1, 9, 21, "w0")
    for x0 in (13, 30):
        L.blit([" kkk ", "kGgGk", "kgkgk", " kGk ", "  k  "], GOLD, x0, 11)
        for y in range(16, 23):
            L.px(x0 + 2, y, "b2" if y % 2 else "w0")
    L.vline(0, 0, 21, "ink")
    L.vline(W - 1, 0, 21, "ink")
    # the basin
    L.rect(0, 22, W, 10, "m1")
    L.hline(0, W - 1, 22, "ink")
    L.hline(1, W - 2, 23, "w0")
    L.rect(2, 24, W - 4, 4, "b1")
    for x in range(3, W // 2, 6):
        L.px(x, 25, "b2")
        L.px(x + 1, 25, "w0")
    L.hline(1, W - 2, 28, "m2")
    L.hline(1, W - 2, 30, "m3")
    L.hline(0, W - 1, 31, "ink")
    L.vline(0, 22, 31, "ink")
    E.mirror_half(L, 0, W, 0, 32)
    s.names = {"basin": (1, 1)}
    return finish(s)


# ==========================================================================
# Semele's chamber
# ==========================================================================

# Semele's smoke: two wisps curling up from the crack, over the back wall (top layer).
# The tileset animates it (SCRIPT.md Part 10: a 2-frame smoke): frame 1 is the same
# wisps risen two pixels, so the pair loops as a slow climb. The animated tiles are the
# smoke's own (SMOKE_BOX, in the struct's pixels); thyrsa_build.py moves them to fixed
# tile slots and writes the frames for src/tileset_anims.c.
SMOKE_BOX = (16, 0, 32, 24)      # x0, y0, x1, y1: the top layer's tiles the smoke lives in
SMOKE_FRAMES = 2


def smoke(L, frame=0):
    rise = 2 * frame
    for x0, ph in ((22, 0), (26, 3)):
        for y in range(1, 22):
            x = x0 + int(round(1.6 * math.sin((y + ph + rise) / 3.0)))
            L.px(x, y, "w0" if (y + rise) % 4 else "cg5")
            if (y + rise) % 3 == 0:
                L.px(x + 1, y, "cg5")


def semele(frame=0):
    s = struct("semele", "Semele's chamber", 3, 2, walk=["XXX", "XXX"], ground="none",
               section="civic",
               notes="On the Kadmeia: the room where Zeus came to Semele as lightning, a "
                     "roofless ruin of the city's Cyclopean stones, wrapped in ivy, open to "
                     "the south. Smoke curls from a crack in its floor (row 1, middle: give it "
                     "the crack's bg event, read from the flags below). Its stones are the "
                     "wall's masonry: place it at an even map column with its top row on an "
                     "even map row.")
    import math
    import random
    L, Tl = s.B, s.T
    W = 48
    T.paving(L, 0, 0, W, 32)
    # the back wall, its top broken and ragged
    T.fill_masonry(L, 0, 0, W, 14, "wall", ox=0, oy=16)
    rnd = random.Random(7)
    for x in range(W):
        top = rnd.choice((0, 0, 1, 2, 3, 4)) if 6 < x < W - 6 else 0
        for y in range(0, top):
            L.px(x, y, "cg2")
        L.px(x, 13, "cg0")
    # the side walls, tops lit, broken low toward the front
    for x0, x1 in ((0, 9), (39, 48)):
        T.fill_masonry(L, x0, 14, x1 - x0, 18, "wall", ox=0, oy=16)
        for x in range(x0, x1):
            L.px(x, 14, "cg5")
        L.vline(x1 if x0 == 0 else x0 - 1, 14, 31, "cg0")
    # scorched flags round the crack
    for y in range(14, 32):
        for x in range(9, 39):
            if (x - 24) ** 2 * 0.7 + (y - 23) ** 2 < 40:
                c = L.get(x, y)
                L.px(x, y, {"cg5": "cg3", "cg4": "cg2", "cg3": "cg2"}.get(c, c))
    crack = [(24, 17), (23, 18), (23, 19), (24, 20), (25, 21), (25, 22), (24, 23), (23, 24),
             (23, 25), (24, 26), (25, 27), (25, 28)]
    for (x, y) in crack:
        L.px(x, y, "ink")
        L.px(x + 1, y, "cg0")
        L.px(x - 1, y, "e1")
    # smoke, rising over the back wall (top layer); animated in two frames
    smoke(Tl, frame)
    # ivy over the back wall's corners
    T.ivy_drape(Tl, 0, 0, 13, 20, seed=17, top_full=5)
    T.ivy_drape(Tl, W - 12, 0, 12, 12, seed=19, top_full=4)
    Tl.a[16:32, 0:16] = 0
    s.names = {"crack": (1, 1)}
    return finish(s)


def build():
    return [temple(), asclepeion(), fountain(), semele()]
