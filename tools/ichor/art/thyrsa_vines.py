"""Thyrsa's vineyards (gTileset_Thyrsa).

Inside the west wall the city keeps its vineyards: rows of vines trained on
low trellises over furrowed earth. The rows are the city's tall grass
(MB_TALL_GRASS): wild Pokémon live among them. Also the old trellises in the
vineyards' corner (gnarled vines the god planted, they say), the old stone
wine press, jars and a barrel, and the marked ivy on the vineyards' old
terrace wall, which Dionysus's Thyrsus will one day climb.
"""
from __future__ import annotations

import random

import thyrsa_lib as T
from thyrsa_lib import finish, struct


def _vine_row(L, x0, y0, w, grapes=True, seed=1, posts=True):
    """A row of vines on a wire, 9 px of foliage at the top of the cell, the
    furrow below, a post at the cell's left."""
    rnd = random.Random(seed)
    for x in range(x0, x0 + w):
        X = x - x0
        top = y0 + 1 + (1 if (X * 7 + seed) % 5 == 0 else 0)
        for y in range(top, y0 + 10):
            c = "iv1"
            if y == top:
                c = "iv0"
            elif y == top + 1:
                c = "iv2" if X % 3 else "iv3"
            elif y >= y0 + 8:
                c = "iv0"
            elif (X + y) % 4 == 0:
                c = "iv2"
            L.px(x, y, c)
        L.px(x, y0 + 10, "e0")
    for _ in range(w // 3):
        L.px(x0 + rnd.randrange(w), y0 + 2 + rnd.randrange(4), "iv3")
    if grapes:
        for x in range(x0 + 3, x0 + w - 2, 8):
            gx = x + rnd.randint(0, 2)
            L.blit(["kk", "12", "21", " 1"], {"k": "vp0", "1": "vp1", "2": "vp2"}, gx, y0 + 5)
    if posts:
        L.vline(x0 + 1, y0, y0 + 11, "wd1")
        L.px(x0 + 1, y0, "wd3")
        L.px(x0 + 2, y0 + 11, "e0")


def vines():
    s = struct("vines", "Vine rows (the vineyards' tall grass)", 4, 1, walk=["...."],
               ground="earth", section="vines",
               notes="Rows of vines on low trellises over furrowed earth, one row to a cell, "
                     "so a block of them reads as striped rows. All are MB_TALL_GRASS: wild "
                     "encounters. (0) vines, (1) vines heavy with grapes (scatter it), (2) the "
                     "row's west end, a stout post with the wire tied off, (3) its east end.")
    L = s.B
    T.earth(L, 0, 0, 64, 16)
    _vine_row(L, 0, 0, 16, grapes=False, seed=3)
    _vine_row(L, 16, 0, 16, grapes=True, seed=3)
    _vine_row(L, 37, 0, 11, grapes=False, seed=4, posts=False)
    _vine_row(L, 48, 0, 11, grapes=False, seed=5, posts=False)
    for px in (35, 59):
        L.rect(px, 0, 2, 12, "wd2")
        L.vline(px, 0, 11, "wd1")
        L.hline(px, px + 1, 0, "wd3")
        L.hline(px - 1, px + 2, 12, "wd0")
    for i in range(4):
        s.behaviors[(i, 0)] = "MB_TALL_GRASS"
    s.names = {"row": (0, 0), "grapes": (1, 0), "W": (2, 0), "E": (3, 0)}
    return finish(s)


def old_trellis():
    s = struct("old_trellis", "The old trellises", 2, 2, walk=["XX", "XX"], ground="grass",
               section="vines",
               notes="In the vineyards' corner, vines older than anyone's grandmother: gnarled "
                     "black trunks under a pergola of grey poles, heavy with leaves. 'The god "
                     "planted these when he was a boy.' The rare-visitor omen puts a Thyrsivy "
                     "beside them. The top row draws over the player.")
    s.walk = ["TT", "XX"]
    Tl, M = s.T, s.M
    rnd = random.Random(11)
    # the pergola: poles and a canopy of leaves (top layer, row 0)
    # a canopy that repeats every 16 px, so both cells share it but for the grapes
    for _ in range(85):
        x, y = rnd.randrange(0, 16), rnd.randrange(1, 15)
        for ox in (0, 16):
            Tl.blit(["kk", "12"] if (x + y) % 2 else ["k1", "12"],
                    {"k": "iv0", "1": "iv1", "2": "iv2"}, x + ox, y)
    for _ in range(14):
        x, y = rnd.randrange(0, 16), rnd.randrange(1, 12)
        Tl.px(x, y, "iv3")
        Tl.px(x + 16, y, "iv3")
    Tl.a[:, 32:] = 0
    for (x, y) in ((6, 9), (19, 11), (26, 6)):
        Tl.blit(["kk", "12", "21", " 1"], {"k": "vp0", "1": "vp1", "2": "vp2"}, x, y)
    Tl.hline(0, 31, 0, "wd1")
    Tl.hline(0, 31, 1, "wd2")
    # row 1: the gnarled trunks and the pergola's posts
    for x0 in (5, 21):
        for y in range(16, 30):
            dx = int(round(1.5 * __import__("math").sin(y / 2.5 + x0)))
            M.rect(x0 + dx, y, 4, 1, "wd0")
            M.px(x0 + dx + 1, y, "wd1")
        M.hline(x0 - 2, x0 + 5, 30, "wd0")
    for x0 in (0, 30):
        M.vline(x0, 16, 30, "wd1")
        M.vline(x0 + 1, 16, 30, "wd2")
    for _ in range(25):
        M.blit(["k1"], {"k": "iv0", "1": "iv1"}, rnd.randrange(2, 28), rnd.randrange(16, 22))
    return finish(s)


def wine_press():
    s = struct("press", "The old wine press", 2, 2, walk=["XX", "XX"], ground="grass",
               section="vines",
               notes="A stone treading floor, purple-stained, under a great wooden beam press "
                     "on two posts, its spout over a stone vat. The Black Sludge lies beside "
                     "it.")
    M = s.M
    # the treading floor and the vat (row 1)
    for y in range(17, 31):
        for x in range(1, 31):
            c = "s3"
            if y in (17, 30) or x in (1, 30):
                c = "ink"
            elif y == 18 or x == 2:
                c = "s4"
            elif y == 29 or x == 29:
                c = "s1"
            elif y < 20 or x < 4 or x > 27 or y > 27:
                c = "s2"
            else:
                c = "tc0" if (x * 3 + y * 5) % 7 else "tc1"
            M.px(x, y, c)
    M.rect(19, 24, 9, 4, "s1")
    M.hline(19, 27, 24, "ink")
    M.rect(20, 25, 7, 2, "tc0")
    # the beam press over it (row 0 and the floor's top)
    for x0 in (3, 26):
        M.rect(x0, 2, 3, 17, "wd1")
        M.vline(x0, 2, 18, "wd0")
        M.vline(x0 + 2, 2, 18, "wd2")
    M.rect(1, 4, 30, 4, "wd2")
    M.hline(1, 30, 4, "wd3")
    M.hline(1, 30, 7, "wd0")
    M.vline(1, 4, 7, "ink")
    M.vline(30, 4, 7, "ink")
    M.rect(14, 8, 4, 10, "wd1")
    M.vline(14, 8, 17, "wd0")
    M.rect(10, 16, 12, 3, "wd2")
    M.hline(10, 21, 18, "wd0")
    return finish(s)


def ivy_marked():
    s = struct("ivy_mark", "Marked ivy on the old terrace wall", 1, 1, walk=["X"], ground="none",
               section="vines",
               notes="The vineyards' old terrace wall under a thick fall of ivy, a thyrsus (a "
                     "fennel staff tipped with a pinecone) scratched into a block behind it. "
                     "Dionysus's Thyrsus (rite gift II) climbs it; until then it is a bg "
                     "event. Lay it in a terrace wall run at an odd or even column.")
    L = s.B
    T.fill_masonry(L, 0, 0, 16, 16, "wall", ox=0, oy=-16)
    for x in range(16):
        L.px(x, 0, "cg5")
        L.px(x, 1, "cg4")
        L.px(x, 2, "cg2")
        L.px(x, 3, "cg0")
    T.ivy_patch(L, 0, 2, 16, 13, density=0.85, seed=51)
    # the thyrsus, scratched pale into the stone where the ivy parts
    L.rect(6, 4, 4, 11, "cg2")
    L.vline(7, 6, 14, "cg5")
    L.blit([" e ", "eee", "e2e", " e "], {"e": "e2", "2": "e1"}, 6, 3)
    return finish(s)


def jars():
    s = struct("jars", "Wine jars", 2, 1, walk=["XX"], ground="pave",
               section="vines",
               notes="(0) two amphorae of this year's wine leaning together, (1) a rack of "
                     "three: for the vintner's yard and the tavern's door. On the flags.")
    import emporion_lib as E
    M = s.M
    E.amphora(M, 1, 3, body="tc1", lit="tc2", shade="tc0", dark="tc0")
    E.amphora(M, 7, 4, body="tc2", lit="tc3", shade="tc1", dark="tc0")
    M.rect(17, 12, 14, 2, "wd1")
    M.hline(17, 30, 14, "wd0")
    for x0 in (17, 22, 26):
        E.amphora(M, x0, 4, body="tc1", lit="tc2", shade="tc0", dark="tc0", small=True)
    return finish(s)


def build():
    return [vines(), old_trellis(), wine_press(), ivy_marked(), jars()]
