"""The Bull Road (LABYRINTH §2): the vineyard terraces, phrygana and thyme, the
beekeeper's round stone hut over its spring, hives in the yard, the labrys
door in the east cliff, Mount Ida's labrys-sealed gate, the vintner's sign.

The beekeeper's hut is a Cretan mitato, the shepherds' round corbelled hut of
dry stone. The labrys door has no handle, only a hollow shaped like a double
axe (SCRIPT.md III-3B); it opens after Ring III, as does Ida's gate.
"""
from __future__ import annotations

import math

import numpy as np

import knossa_lib as N
import knossa_town as T
from knossa_land import face_fill, lip_row, stone
from knossa_lib import anim_layer, ground, grid, struct

SEC = "road"


def foliage(L, mask, ramp, seed=0, outline="t0", clump=4.0, flowers=None, fl_rate=0,
            periodic=True):
    import kythera_land as KL
    KL.foliage(L, mask, ramp, seed=seed, outline=outline, clump=clump, flowers=flowers,
               fl_rate=fl_rate, periodic=periodic)


def mask_of(w, h_, fn):
    m = np.zeros((h_, w), bool)
    for y in range(h_):
        for x in range(w):
            m[y, x] = fn(x, y)
    return m


# --------------------------------------------------------------------------
# The vineyard
# --------------------------------------------------------------------------

def vines():
    """Trellised vine rows (impassable) and the low vines between them, the
    vineyard's tall grass, as a soft-edged patch."""
    names = {"row_L": (0, 0), "row": (1, 0), "row_grapes": (2, 0), "row_R": (3, 0),
             "row_post": (4, 0), "sign": (5, 0),
             "NW": (0, 1), "N": (1, 1), "NE": (2, 1), "W": (0, 2), "C": (1, 2), "E": (2, 2),
             "SW": (0, 3), "S": (1, 3), "SE": (2, 3), "C_grapes": (3, 2), "C_b": (3, 1),
             "C_dig": (3, 3)}
    s = struct("vines", "The vineyard: trellised rows and low vines", 6, 4, "vineyard",
               walk=["XXXXXX", "GGGGXX", "GGGGXX", "GGGGXX"], names=names,
               notes="The vines of the house of Minos (SCRIPT.md Part 2, the vineyard terraces), "
                     "all on borrowed grass. **Trellised rows**, impassable, running west to "
                     "east: `row_L` `row` (`row_grapes`, `row_post` to vary it) `row_R`. **Low "
                     "vines**, the vineyard's tall grass (`MB_TALL_GRASS`; its own encounter "
                     "table, so it must look unlike the road's barley): a soft-edged patch, `NW` "
                     "`N` `NE` / `W` `C` `E` / `SW` `S` `SE`, with `C_b` and `C_grapes` to break "
                     "up the middle and `C_dig` for the vineyard's lowest-terrace sherd (turned "
                     "earth among the vines). Lay rows and low vines in alternating bands across "
                     "a terrace. `sign` is the old vintner's sign (impassable; bg event): "
                     "\"Vines of the house of Minos.\"")
    ground(s, "grass")
    M = s.M
    ramp = ["my1", "my2", "my3", "my4"]
    # trellised rows: posts and a wire, leaves heaped along it, grapes beneath
    for cx, kind in ((0, "L"), (1, "M"), (2, "G"), (3, "R"), (4, "P")):
        ox = cx * 16
        x0 = 4 if kind == "L" else 0
        x1 = 12 if kind == "R" else 16

        def inside(x, y, x0=x0, x1=x1, ox=ox):
            if not (x0 <= x - ox < x1):
                return False
            xx = x - ox
            top = 2 + (N.h(x, 1, 7) % 3 == 0) + (1 if xx in (x0, x1 - 1) else 0)
            bot = 11 - (N.h(x, 2, 7) % 4 == 0) - (1 if xx in (x0, x1 - 1) else 0)
            return top <= y < bot
        m = mask_of(80, 16, inside)
        sub = N.Layer(80, 16)
        foliage(sub, m, ramp, seed=11 + cx, flowers=None)
        for y in range(16):
            for x in range(ox, ox + 16):
                if sub.a[y, x, 3]:
                    M.a[y, x] = sub.a[y, x]
        # shadow on the ground under the row
        for x in range(ox + x0, ox + x1):
            for y in (11, 12):
                if M.get(x, y) is None:
                    M.px(x, y, "gd" if (x + y) % 2 else "g1")
        # posts at the ends and the wire's sag
        posts = [x0 + 1] if kind == "L" else ([x1 - 2] if kind == "R" else
                                              ([7] if kind == "P" else []))
        for px_ in posts:
            for y in range(1, 13):
                M.px(ox + px_, y, "kt1")
                M.px(ox + px_ + 1, y, "kt2" if y < 12 else "kt1")
            M.px(ox + px_, 0, "t0")
            M.px(ox + px_ + 1, 0, "t0")
        # grapes hanging under the leaves
        bunches = ((3, 9), (11, 8)) if kind in ("G",) else (((6, 9),) if kind == "M" else ())
        for (bx, by) in bunches:
            grid(M, ox + bx, by, [
                "kkkk",
                "k21k",
                "k12k",
                ".k1k",
                ".kk.",
            ], {"k": "gp0", "1": "gp1", "2": "th2"})
    # the vintner's sign: a weathered board on a post, a bunch painted on it
    ox = 80
    grid(M, ox + 1, 1, [
        ".tttttttttttt.",
        "t22222222222kt",
        "t2222pp22222kt",
        "t222pqpp2222kt",
        "t2222ppp2222kt",
        "t22222pp2222kt",
        "t222222p2222kt",
        "tkkkkkkkkkkkkt",
        ".tttttttttttt.",
        "......tk......",
        "......tk......",
        "......tk......",
        "......tk......",
        ".....ggggg....",
    ], {"t": "t0", "2": "kt2", "k": "kt1", "p": "gp0", "q": "gp1", "g": "gd"})
    # the low vines: a soft-edged patch of leaves sprawled over the ground
    def patch_inside(x, y, cx, cy):
        xx, yy = x - cx * 16, y - cy * 16
        n = cy == 1 and cx < 3
        sth = cy == 3 and cx < 3
        w_ = cx == 0
        e_ = cx == 2
        wob = (N.h(x, y, 9) % 3)
        if n and yy < 3 + wob:
            return False
        if sth and yy > 12 - wob:
            return False
        if w_ and xx < 3 + wob:
            return False
        if e_ and xx > 12 - wob:
            return False
        if (n or sth) and (w_ or e_):
            ax = xx - 3 if w_ else 12 - xx
            ay = yy - 3 if n else 12 - yy
            if ax < 4 and ay < 4 and math.hypot(4 - ax, 4 - ay) > 4.5:
                return False
        return True
    for cy in (1, 2, 3):
        for cx in range(4):
            if cx == 3 and cy not in (1, 2, 3):
                continue
            ox, oy = cx * 16, cy * 16
            m = mask_of(16, 16, lambda x, y, cx=cx, cy=cy: patch_inside(ox + x, oy + y, cx, cy))
            # low vines: leaf clumps sprawled over the ground, ground showing
            # between; clumps wrap at the cell's edges, so the middle tiles
            leaf = [
                "..ab..",
                ".abbc.",
                "abbbcc",
                ".bcbc.",
                "..kc..",
            ]
            lg = {"a": "my4", "b": "my3", "c": "my2", "k": "my1"}
            pts = [(1, 0), (8, 1), (13, 5), (4, 6), (10, 9), (0, 11), (6, 12), (14, 13)]
            if cx == 3 and cy == 1:
                pts = [(2, 1), (9, 0), (12, 6), (5, 5), (9, 10), (1, 12), (5, 11), (13, 13)]
            for (px_, py_) in pts:
                for j, row in enumerate(leaf):
                    for i, ch in enumerate(row):
                        if ch not in lg:
                            continue
                        x, y = (px_ + i) % 16, (py_ + j) % 16
                        if m[y, x]:
                            M.px(ox + x, oy + y, lg[ch])
                # the clump's shadow on the ground, one row below
                for i in range(1, 5):
                    x, y = (px_ + i) % 16, (py_ + 5) % 16
                    if m[y, x] and M.get(ox + x, oy + y) is None:
                        M.px(ox + x, oy + y, "gd")
            # runners between the clumps
            for (tx, ty) in ((6, 3), (7, 3), (11, 7), (3, 10), (12, 12), (13, 12)):
                if m[ty, tx] and M.get(ox + tx, oy + ty) is None:
                    M.px(ox + tx, oy + ty, "my1")
    for (bx, by) in ((50, 38), (57, 42)):
        grid(M, bx, by, ["kk", "21", "k1"], {"k": "gp0", "1": "gp1", "2": "th2"})
    # the dig: turned earth among the vines
    ox, oy = 48, 48
    for y in range(5, 12):
        for x in range(4, 12):
            if math.hypot(x - 7.5, (y - 8) * 1.3) < 4:
                M.px(ox + x, oy + y, "kt1" if (x + y) % 3 else "kt2")
    s.walk = ["XXXXXX", "GGGGXX", "GGGGXX", "GGGGXX"]
    for (x, y) in ((4, 1), (5, 1), (4, 2), (5, 2), (4, 3), (5, 3)):
        pass
    s.behaviors = {(x, y): "MB_TALL_GRASS" for y in (1, 2, 3) for x in range(4)}
    return N.pick(s, ["row_L", "row", "row_grapes", "row_post", "row_R", "sign",
                      "NW", "N", "NE", "C_b", "W", "C", "E", "C_grapes", "SW", "S", "SE",
                      "C_dig"], w=6, key="vines", notes=s.notes, section="vineyard")


# --------------------------------------------------------------------------
# Phrygana: thyme, sage, spiny burnet, asphodel
# --------------------------------------------------------------------------

def phrygana():
    names = {"thyme": (0, 0), "sage": (1, 0), "burnet": (2, 0), "asphodel": (3, 0),
             "thyme_b": (4, 0)}
    s = struct("phrygana", "Phrygana: thyme, sage, spiny burnet, asphodel", 5, 1, "road",
               walk=[".XX.."], names=names,
               notes="Crete's low scrub on borrowed grass, between the terraces and on the "
                     "Bronze Heel's slope, where the bees work. Walkable: `thyme` and `thyme_b` "
                     "(flowering cushions), `asphodel` (white spikes). Impassable: `sage` "
                     "(Jerusalem sage, grey leaves), `burnet` (a spiny cushion).")
    ground(s, "grass")
    M = s.M
    for cx, (pts, seed) in ((0, ([(4, 8), (10, 10), (7, 4)], 1)), (4, ([(5, 6), (11, 9)], 4))):
        ox = cx * 16
        m = mask_of(16, 16, lambda x, y, pts=pts: any(math.hypot(x - a, (y - b) * 1.3) < 3.4
                                                     for (a, b) in pts))
        sub = N.Layer(16, 16)
        foliage(sub, m, ["my1", "my2", "my3", "my4"], seed=seed, clump=2.5, outline="t0")
        for y in range(16):
            for x in range(16):
                if sub.a[y, x, 3]:
                    M.a[y, ox + x] = sub.a[y, x]
                    # the cushion in flower: a haze of pink-lilac over its top
                    if sub.get(x, y) in ("my3", "my4", "my2") and N.hp(x, y, seed) % 3 == 0:
                        M.px(ox + x, y, "th2")
                    elif sub.get(x, y) == "my4" and N.hp(x, y, seed + 1) % 4 == 0:
                        M.px(ox + x, y, "w0")
    # sage: a grey-green dome, pale woolly leaves, yellow-green whorls
    ox = 16
    m = mask_of(16, 16, lambda x, y: math.hypot(x - 7.5, (y - 8) * 1.2) < 6.5)
    sub = N.Layer(16, 16)
    foliage(sub, m, ["my1", "my3", "my4", "w0"], seed=7, clump=3.0, flowers=["g3"], fl_rate=3)
    for y in range(16):
        for x in range(16):
            if sub.a[y, x, 3]:
                M.a[y, ox + x] = sub.a[y, x]
    for x in range(4, 13):
        if M.get(ox + x, 15) is None:
            M.px(ox + x, 15, "gd")
    # spiny burnet: a tight round cushion, dark and twiggy
    ox = 32
    m = mask_of(16, 16, lambda x, y: math.hypot(x - 7.5, (y - 9) * 1.15) < 5.5)
    sub = N.Layer(16, 16)
    foliage(sub, m, ["kt1", "my1", "my2", "my3"], seed=9, clump=2.0, flowers=["kt2"], fl_rate=3)
    for y in range(16):
        for x in range(16):
            if sub.a[y, x, 3]:
                M.a[y, ox + x] = sub.a[y, x]
    # asphodel: three spikes of white stars over a leafy base
    ox = 48
    for (sx, h_) in ((5, 9), (9, 11), (12, 7)):
        for y in range(15 - h_, 13):
            M.px(ox + sx, y, "my1")
        for y in range(15 - h_, 15 - h_ + 5):
            M.px(ox + sx - 1, y, "w0" if y % 2 else None)
            M.px(ox + sx + 1, y, "w0" if not y % 2 else None)
            M.px(ox + sx, y, "w0" if y == 15 - h_ else "my1")
    grid(M, ox + 3, 11, [".m.mm.m..", "mmmmmmmmm", ".mMmmMm.."], {"m": "my2", "M": "my3"})
    return s


# --------------------------------------------------------------------------
# The beekeeper's hut: a mitato over its spring, and hives in the yard
# --------------------------------------------------------------------------

def mitato():
    names = {"top_L": (0, 0), "top": (1, 0), "top_R": (2, 0), "wall_L": (0, 1),
             "lintel": (1, 1), "wall_R": (2, 1), "foot_L": (0, 2), "door": (1, 2),
             "foot_R": (2, 2), "runnel": (3, 2), "hives": (3, 0), "skeps": (3, 1)}
    s = struct("mitato", "The beekeeper's hut, over its spring", 4, 3, "road",
               walk=["TTTX", "XXXX", "XDX."], names=names,
               notes="Bombylia's hut, the Bull Road's rest point (SCRIPT.md Part 2): a Cretan "
                     "mitato, a round hut of dry stone corbelled into a dome, built over a "
                     "spring. 3 x 3: the dome's crown (`top_*`, drawn over the player, who walks "
                     "behind it) over its walls over `foot_L` `door` `foot_R`. `door` is "
                     "`MB_NON_ANIMATED_DOOR` (the warp to `MAP_KNOSSA_BULL_ROAD_HUT`); the "
                     "spring's overflow runs out under it: lay `runnel` (walkable, a stone "
                     "channel of water) south of the door, as many cells as you like. `hives` "
                     "(clay tubes on a slab) and `skeps` stand in the yard, bees about them "
                     "(impassable). All on borrowed grass but the door.")
    ground(s, "grass", [(x, y) for y in range(3) for x in range(4) if (x, y) != (1, 2)])
    M, B, Tl = s.M, s.B, s.T
    cx0, cy0, R = 24, 30, 21.0

    def in_dome(x, y):
        # a dome on a short drum: round above y=30, straight sides below
        if y >= 30:
            return abs(x + 0.5 - cx0) <= 20.5 and y < 46
        return math.hypot((x + 0.5 - cx0) / 20.5, (y + 0.5 - cy0) / 26.0) <= 1.0
    for y in range(48):
        for x in range(48):
            if not in_dome(x, y):
                continue
            # corbelled courses: flat stones in rings, each course 3 px tall
            course = (y + 1) // 3
            off = (course * 5) % 7
            joint = (x + off) % 7 == 0
            row_top = (y + 1) % 3 == 0
            dx = (x + 0.5 - cx0) / 20.5
            lit = -dx * 0.8 + (30 - y) / 40
            if row_top:
                c = "cs1"
            elif joint:
                c = "cs1"
            else:
                c = "cs4" if lit > 0.55 else ("cs3" if lit > 0.05 else "cs2")
                if N.h(x, y, 2) % 13 == 0:
                    c = "cs5" if lit > 0.3 else "cs3"
            L = Tl if y < 16 else M
            L.px(x, y, c)
    # the dome's outline and a cap stone, a few weeds in the joints
    for y in range(48):
        for x in range(48):
            if in_dome(x, y) and (not in_dome(x - 1, y) or not in_dome(x + 1, y)
                                  or not in_dome(x, y - 1)):
                (Tl if y < 16 else M).px(x, y, "cs0")
    grid(Tl, 20, 2, ["..kkkk..", ".k5544k.", "kkkkkkkk"], {"k": "cs0", "5": "cs5", "4": "cs4"})
    for (wx, wy) in ((12, 14), (33, 9), (38, 22), (9, 26)):
        L = Tl if wy < 16 else M
        L.px(wx, wy, "my2")
        L.px(wx + 1, wy - 1, "my3")
    # the low doorway: a stone lintel, the dark inside, a worn threshold
    for y in range(32, 48):
        for x in range(16, 32):
            if in_dome(x, y):
                B.px(x, y, M.get(x, y) or "cs2")
            else:
                B.px(x, y, "g1")
    for y in range(32, 48):
        for x in range(16, 32):
            M.px(x, y, None)
    # copy the dome's stones into the door cell's bottom layer, then cut the door
    for y in range(32, 48):
        for x in range(16, 32):
            if in_dome(x, y):
                yy, xx = y, x
                course = (yy + 1) // 3
                off = (course * 5) % 7
                c = "cs1" if (yy + 1) % 3 == 0 or (xx + off) % 7 == 0 else "cs3"
                B.px(x, y, c)
    for x in range(16, 32):
        B.px(x, 46, "g1")
        B.px(x, 47, "g2" if x % 3 else "g1")
    for y in range(33, 46):
        for x in range(19, 29):
            B.px(x, y, "cv0" if 20 <= x <= 27 and y > 34 else "cs0")
    for x in range(17, 31):
        B.px(x, 32, "cs4")
        B.px(x, 33, "cs2")
        B.px(x, 34, "cs1")
    for x in range(19, 29):
        B.px(x, 45, "cs3")
        B.px(x, 46, "cs2")
    # the spring's overflow, out under the door (middle layer, the water's colors)
    for y in range(41, 48):
        for x in range(22, 26):
            M.px(x, y, "kq1" if (x + y) % 3 else "b4")
    M.px(22, 41, "kq2")
    # the runnel: a stone channel in the grass, water in it
    ox, oy = 48, 32
    for y in range(16):
        for x in range(5, 11):
            if x in (5, 10):
                M.px(ox + x, oy + y, "p1" if x == 5 else "l1")
            elif x == 6:
                M.px(ox + x, oy + y, "kq1")
            else:
                M.px(ox + x, oy + y, "b3" if (y + x) % 4 else "b4")
        if y % 5 == 2:
            M.px(ox + 8, oy + y, "w0")
    # yard hives and skeps, bees about them
    T.hive_tubes(M, 48, 0)
    T.skeps(M, 48, 16)
    frames = anim_layer(s, "bees", 3)
    allf = [M] + frames
    for f, pts in zip(allf, [[(3, 9), (13, 5), (8, 3)], [(1, 7), (14, 9), (10, 1)],
                             [(4, 4), (12, 3), (6, 10)]]):
        for (x, y) in pts:
            f.px(48 + x, y, "ink")
            f.px(48 + x, y - 1, "mg2")
    for f, pts in zip(allf, [[(4, 13), (13, 2), (8, 1)], [(2, 11), (14, 6), (11, 0)],
                             [(6, 12), (12, 11), (6, 1)]]):
        for (x, y) in pts:
            f.px(48 + x, 16 + y, "ink")
            f.px(48 + x, 16 + y - 1, "mg2")
    N.settle(s, "bees", [(3, 0), (3, 1)])
    return s


# --------------------------------------------------------------------------
# The labrys door, and Ida's labrys-sealed gate
# --------------------------------------------------------------------------

def labrys(L, ox, oy, c, w=9):
    """A double axe: two blades either side of a haft (9 x 8)."""
    grid(L, ox, oy, [
        "c.......c",
        "cc.....cc",
        "ccc.c.ccc",
        "ccccccccc",
        "ccc.c.ccc",
        "cc..c..cc",
        "c...c...c",
        "....c....",
        "....c....",
    ], {"c": c})


def labrys_door():
    """3 x 2 in a two-row cliff face, closed and open (6 x 2)."""
    names = {"top_L": (0, 0), "top": (1, 0), "top_R": (2, 0), "foot_L": (0, 1), "door": (1, 1),
             "foot_R": (2, 1), "open_top_L": (3, 0), "open_top": (4, 0), "open_top_R": (5, 0),
             "open_foot_L": (3, 1), "open_door": (4, 1), "open_foot_R": (5, 1)}
    s = struct("labrys_door", "The labrys door in the east cliff", 6, 2, "road",
               walk=["XXXXXX", "XXXXDX"], names=names,
               notes="The Bull Road vault's door (LABYRINTH §2's relic gate), set in a two-row "
                     "stretch of the east cliff's face (stack two `cliff.face` rows either side, "
                     "a `cliff.lip` row above): a gypsum doorway under horns of consecration, "
                     "red-painted jambs, and a door with no handle, only a hollow the shape of a "
                     "double axe. Closed: `top_L` `top` `top_R` over `foot_L` `door` `foot_R` "
                     "(impassable; the bg event is on `door`). **Opened with the Labrys** after "
                     "Ring III: swap all six cells to `open_*`, the slab gone and a stair going "
                     "down into the dark; `open_door` is `MB_NON_ANIMATED_DOOR`, the warp to "
                     "`MAP_KNOSSA_BULL_ROAD_VAULT`.")
    B, M = s.B, s.M
    for ox in (0, 48):
        face_fill(B, ox, 0, 48, 32)
    for ox, open_ in ((0, False), (48, True)):
        # the gypsum doorway: lintel, jambs, horns above (middle layer, minoan)
        for y in range(6, 32):
            for x in range(12, 36):
                jamb = x < 16 or x >= 32
                lint = y < 11
                if jamb or lint:
                    if lint:
                        c = ("mg2", "mg1", "mg1", "mg0", "mb")[min(4, y - 6)]
                    else:
                        c = ("mr2", "mr1", "mr1", "mr0")[x - 12] if x < 16 else \
                            ("mr0", "mr1", "mr1", "mr0")[x - 32]
                    M.px(ox + x, y, c)
        # the horns of consecration on the lintel
        grid(M, ox + 16, 0, [
            "kk............kk",
            "k2k..........k1k",
            "k22k........k11k",
            "k222kkkkkkkk111k",
            "k22222222221110k",
            "kkkkkkkkkkkkkkkk",
        ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
        # double axes cut on the jambs' outer faces
        if not open_:
            for y in range(11, 32):
                for x in range(16, 32):
                    c = "mg1" if (x + y) % 9 else "mg0"
                    if x == 16:
                        c = "mg2"
                    if x == 31:
                        c = "mg0"
                    M.px(ox + x, y, c)
            # the hollow: a double axe sunk in the slab
            grid(M, ox + 19, 15, [
                "kk........kk",
                "kkk......kkk",
                "kkkk.kk.kkkk",
                "kkkkkkkkkkkk",
                "kkkk.kk.kkkk",
                "kkk..kk..kkk",
                "kk...kk...kk",
                ".....kk.....",
                ".....kk.....",
                ".....kk.....",
            ], {"k": "mb"})
            for y in range(15, 25):
                if M.get(ox + 19, y) == "mb":
                    M.px(ox + 19, y, "ink")
        else:
            for y in range(11, 32):
                for x in range(16, 32):
                    d = y - 11
                    c = "ink" if d < 10 else "mb"
                    if d >= 10 and (d - 10) % 4 == 0:
                        c = "mg0"
                    if d >= 10 and (d - 10) % 4 == 1:
                        c = "mg1"
                    M.px(ox + x, y, c)
    s.walk = ["XXXXXX", "XXXXDX"]
    s.behaviors = {(4, 1): "MB_NON_ANIMATED_DOOR"}
    return s


def ida_gate():
    """Mount Ida's gate: square limestone pillars and a timber gate sealed with
    a clay seal stamped with a double axe; and the gate opened."""
    names = {"pillar_L_top": (0, 0), "gate_top": (1, 0), "pillar_R_top": (2, 0),
             "pillar_L": (0, 1), "gate": (1, 1), "pillar_R": (2, 1),
             "open_top": (3, 0), "open": (3, 1)}
    s = struct("ida_gate", "Mount Ida's labrys-sealed gate", 4, 2, "road",
               walk=["TTTT", "XXX."], names=names,
               notes="The gate to the Ida path on the Bull Road's south-west (SCRIPT.md Part 2): "
                     "two square limestone pillars, each cut with a double axe, and between them "
                     "a timber gate bound shut, a fat clay seal stamped with a labrys over the "
                     "lock. Set it in a terrace or field wall: `pillar_L_top` `gate_top` "
                     "`pillar_R_top` (drawn over the player) over `pillar_L` `gate` `pillar_R` "
                     "(impassable; bg event on `gate`: the seal). **Opened with the Labrys** "
                     "after Ring III (`FLAG_ICHOR_IDA_GATE`): swap `gate_top` and `gate` to "
                     "`open_top` and `open`, the path running through (walkable). All on "
                     "borrowed grass.")
    ground(s, "grass")
    M, Tl = s.M, s.T
    for ox in (0, 32):
        for y in range(2, 30):
            for x in range(3, 13):
                c = stone(ox + x + 3, y)
                if x == 3:
                    c = "cs5"
                elif x == 12:
                    c = "cs0"
                elif x == 11:
                    c = {"cs4": "cs2", "cs5": "cs3", "cs3": "cs2"}.get(c, c)
                if y < 5:
                    c = ("cs0", "cs5", "cs4")[y - 2]
                (Tl if y < 16 else M).px(ox + x, y, c)
        for x in range(3, 13):
            M.px(ox + x, 30, "cs1")
            M.px(ox + x, 31, "g1" if x % 2 else "cs1")
        for y in range(2, 30):
            (Tl if y < 16 else M).px(ox + 2, y, "cs0")
            (Tl if y < 16 else M).px(ox + 13, y, "cs0")
        labrys(Tl, ox + 4, 7, "cs1")
    # the gate: planks between the pillars, bound with a bar, the seal on it
    for y in range(6, 30):
        for x in range(0, 16):
            X = 16 + x
            if y < 8:
                c = "wd0" if y == 6 else "wd1"
            else:
                pl = x % 4
                c = ("wd0", "wd2", "wd1", "wd1")[pl]
                if y in (12, 24):
                    c = "wd0"
            (Tl if y < 16 else M).px(X, y, c)
    for x in range(0, 16):
        M.px(16 + x, 29, "wd0")
    grid(M, 16 + 3, 16, [
        "..kkkkkk..",
        ".k221111k.",
        "k2211111tk",
        "k21k1k11tk",
        "k21kkk11tk",
        "k211k111tk",
        "k111k11ttk",
        ".k11k1ttk.",
        "..kkkkkk..",
    ], {"k": "tc0", "2": "tc3", "1": "tc2", "t": "tc1"})
    for (x, y) in ((16 + 2, 19), (16 + 13, 19), (16 + 1, 20), (16 + 14, 20)):
        M.px(x, y, "ink")
    # open: the gate gone, a worn path through between the pillar shadows
    for y in range(16):
        Tl.px(48, y, None)
    for y in range(16, 32):
        for x in range(48, 64):
            if (x + y) % 5 == 0:
                M.px(x, y, "g2")
    Tl.px(48 + 7, 15, "g2")
    for x in range(52, 60):
        M.px(x, 31, "gd")
    return s


def brow():
    """A terrace's edge seen from above and behind: the ground drops to the
    north, the wall's face hidden. A ledge you hop down northward."""
    names = {"L": (0, 0), "M": (1, 0), "M2": (2, 0), "R": (3, 0), "stair": (4, 0)}
    s = struct("brow", "Terrace brows: ledges down to the north", 5, 1, "road",
               walk=["^^^^."], names=names,
               notes="The Bull Road's terraces step down northward, so the trip back to Amnisos "
                     "is quick (LABYRINTH §2; MAP_DESIGN §1): from the road you see only each "
                     "terrace's coping, the drop beyond it to the north. `L` `M` (`M2`) `R` are "
                     "ledges you hop down northward (`MB_JUMP_NORTH`, walk code `^`); `stair` is "
                     "a flight of rough steps through the brow, the way back up (walkable). On "
                     "borrowed grass.")
    ground(s, "grass")
    M = s.M
    import kythera_coast as Co
    for cx, end in ((0, "L"), (1, None), (2, None), (3, "R"), (4, "S")):
        ox = cx * 16
        for x in range(16):
            if end == "L" and x < 3:
                continue
            if end == "R" and x > 12:
                continue
            e = 5 + int(round(Co.wob(x + 3 * cx, 0.7) * 0.6))
            if end == "S" and 4 <= x <= 11:
                continue
            for y in range(0, e - 2):
                M.px(ox + x, y, "g1" if (x + y) % 3 else "cs1")
            M.px(ox + x, e - 2, "cs0")
            M.px(ox + x, e - 1, "cs1" if (x + 2 * cx) % 5 else "cs0")
            M.px(ox + x, e, "cs5" if (x + cx) % 6 else "cs3")
            M.px(ox + x, e + 1, "cs4" if (x + cx) % 6 else "cs2")
            M.px(ox + x, e + 2, "cs3" if (x + cx) % 6 else "cs1")
            if (x * 3 + cx) % 7 == 0:
                M.px(ox + x, e + 3, "my3")
        if end == "S":
            for i, y0 in enumerate((0, 4, 8)):
                for x in range(4, 12):
                    M.px(ox + x, y0, "cs5")
                    M.px(ox + x, y0 + 1, "cs4")
                    M.px(ox + x, y0 + 2, "cs3")
                    M.px(ox + x, y0 + 3, "cs1")
                M.px(ox + 3, y0 + 2, "cs0")
                M.px(ox + 12, y0 + 2, "cs0")
    return s


def build():
    import kythera_town as KT
    herm = KT.herm_shrine()
    return [vines(), phrygana(), mitato(), labrys_door(), ida_gate(), brow(),
            N.pick(herm, ["herm", "herm_base"], w=1, key="herm", section="road",
                   notes="The great herm at the Bull Road's fork (SYSTEMS §4), which doubles as "
                         "the sign, \"East: the Bronze Heel. South: the palace.\": a tall marble "
                         "pillar with Hermes's bearded head on a plinth carved with the roads, "
                         "Kythera's great herm (on borrowed grass). `herm` (drawn over the "
                         "player) over `herm_base` (impassable; bg event here). A hidden item "
                         "waits behind it.")]
