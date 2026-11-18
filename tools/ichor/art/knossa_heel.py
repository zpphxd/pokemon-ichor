"""The Bronze Heel (LABYRINTH §2, seed 16; SCRIPT.md Part 2): Talos the giant's
bronze foot standing on the beach, green with age, a bronze nail hammered
into the vein in its heel; tide pools on the rocky shore; and the crumbling
fossil ledge by the tide line, with a skull and a dart in the rock.
"""
from __future__ import annotations

import math

import knossa_lib as N
from knossa_lib import ground, grid, struct

SEC = "heel"


def talos_foot():
    """5 x 4: a colossal right foot, toes to the east, broken off at the
    ankle; the statue was hollow, so the break shows the dark inside."""
    W, H = 5, 4
    names = {"ankle": (1, 0), "heel": (0, 3), "nail": (0, 2), "toes": (4, 3), "toe": (4, 2)}
    s = struct("talos_foot", "Talos's bronze foot", W, H, SEC,
               walk=["TTTTT", "XXXXX", "XXXXX", "XXXXX"], names=names,
               notes="A bronze foot taller than a house, on the Bronze Heel's beach (SCRIPT.md "
                     "Part 2): broken at the ankle, the hollow inside dark; verdigris over "
                     "everything but the toes, rubbed bright; a great bronze nail hammered into "
                     "the vein at the heel (`nail`). Place it whole, on borrowed sand. The top "
                     "row is drawn over the player, who can walk behind the ankle; the rest is "
                     "impassable. The foot is the bg event (`heel` or `nail`); the Big Pearl's "
                     "sealed jar stands on the ankle's break, and Glauke does handstands by the "
                     "`toes`.")
    ground(s, "sand")
    M, Tl = s.M, s.T
    Wp, Hp = W * 16, H * 16
    from PIL import Image, ImageDraw
    import numpy as np
    poly = [(6, 9), (12, 7), (18, 10), (23, 6), (28, 9), (33, 8), (34, 28), (38, 33),
            (46, 37), (55, 40), (62, 42), (66, 42), (70, 43), (74, 45), (77, 48), (79, 52),
            (79, 58), (76, 61), (70, 61), (60, 60), (52, 58), (40, 58), (30, 60), (18, 61),
            (9, 61), (4, 58), (2, 52), (2, 45), (5, 38), (7, 34), (5, 24)]
    im = Image.new("1", (Wp, Hp), 0)
    ImageDraw.Draw(im).polygon(poly, fill=1, outline=1)
    sol = np.array(im, bool)

    def solid(x, y):
        return 0 <= x < Wp and 0 <= y < Hp and bool(sol[y, x])

    def top_of(x):
        for y in range(Hp):
            if solid(x, y):
                return y
        return None

    def put(x, y, c):
        (Tl if y < 16 else M).px(x, y, c)

    for y in range(Hp):
        for x in range(Wp):
            if not solid(x, y):
                continue
            t = top_of(x)
            if x < 34:
                u = (x - 4) / 30.0
                c = "vg2" if u < 0.32 else ("vg1" if u < 0.78 else "vg0")
                if y > 52:
                    c = "vg1" if c == "vg2" else "vg0"
            else:
                d = y - t
                bot = 61 - y
                c = "vg2" if d < 3 else ("vg1" if bot > 4 else "vg0")
            put(x, y, c)
    # verdigris drips from the break, and the vein down the ankle to the heel
    for (dx, dl) in ((9, 9), (15, 14), (21, 7), (27, 11)):
        t = top_of(dx)
        for y in range(t + 5, t + 5 + dl):
            if solid(dx, y):
                put(dx, y, "vg2" if dx < 14 else "vg1")
    for y in range(16, 46):
        vx = 13 - (y - 16) // 4
        put(vx, y, "vg0")
        put(vx + 1, y, "vg2")
    # bronze showing where hands have rubbed: the ankle bone, the instep, the toes
    for (bx, by, r) in ((20, 38, 2.6), (44, 41, 2.0)):
        for y in range(by - 3, by + 4):
            for x in range(bx - 3, bx + 4):
                if solid(x, y) and math.hypot(x - bx, (y - by) * 1.3) < r:
                    put(x, y, "bz2" if (x - bx) + (y - by) < 0 else "bz1")
    for x in range(62, 79):
        t = top_of(x)
        if t is None:
            continue
        for y in range(t, min(t + 6, 61)):
            if solid(x, y):
                put(x, y, "bz3" if y - t < 2 else "bz2")
    # the toes: four rounded tips along the front, seen from above, each
    # rubbed bright, a crease between each; the big toe's nail
    toes = ((76, 49, 3.6), (73, 54, 3.0), (71, 58, 2.6), (66, 60, 2.2))
    for (tx, ty, r) in toes:
        for y in range(ty - 5, ty + 5):
            for x in range(tx - 5, tx + 5):
                if math.hypot(x - tx, (y - ty) * 1.15) < r and solid(x, y):
                    put(x, y, "bz3" if (x - tx) + (y - ty) < -1 else "bz2")
        for a in range(0, 360, 12):
            x = int(round(tx + math.cos(math.radians(a)) * r))
            y = int(round(ty + math.sin(math.radians(a)) * r / 1.15))
            if solid(x, y) and 90 < a < 300:
                put(x, y, "bz0")
    for y in range(50, 61):
        for x in range(62, 80):
            if solid(x, y) and not solid(x, y + 1):
                put(x, y, "bz0")
    grid(M, 76, 47, ["3.", "33"], {"3": "w0"})
    # outline
    for y in range(Hp):
        for x in range(Wp):
            if solid(x, y) and not (solid(x - 1, y) and solid(x + 1, y) and solid(x, y - 1)
                                    and solid(x, y + 1)):
                put(x, y, "ink")
    # the break: the hollow inside, ringed with bright bronze
    for y in range(4, 17):
        for x in range(4, 37):
            e = math.hypot((x - 19.5) / 14.0, (y - 10.0) / 4.2)
            if e < 0.78:
                put(x, y, "ink" if e < 0.6 else "bz0")
            elif e < 1.0 and solid(x, y):
                put(x, y, "bz3" if y < 10 else "bz2")
    # the nail, hammered into the heel's vein
    grid(M, 0, 43, [
        "..kkk....",
        ".k332k...",
        "k333221kk",
        "k3222111k",
        "k32211kkk",
        ".k2111k..",
        "..kkkk...",
    ], {"k": "ink", "3": "bz3", "2": "bz2", "1": "bz1"})
    # shadow on the sand under the arch and east of the toes
    for x in range(6, 80):
        for y in range(56, 64):
            if not solid(x, y) and M.get(x, y) is None and solid(x - 2, y - 1):
                M.px(x, y, "ks1")
    for x in range(30, 56):
        for y in range(58, 62):
            if not solid(x, y) and M.get(x, y) is None:
                M.px(x, y, "ks1")
    return s


def tide_pools():
    names = {"pool": (0, 0), "pool_b": (1, 0), "pool_dig": (2, 0), "urchins": (3, 0),
             "ledge_skull": (0, 1), "ledge_dart": (1, 1), "ledge_gone_L": (2, 1),
             "ledge_gone_R": (3, 1)}
    s = struct("tide_pools", "Tide pools, and the fossil ledge", 4, 2, SEC,
               walk=["XX.X", "XX.."], names=names,
               notes="On borrowed sand by the water. Tide pools in wet rock: `pool` and `pool_b` "
                     "(an anemone, a crab; impassable), `urchins` (black urchins in a shallow "
                     "pool; impassable), `pool_dig` (a pool's sandy edge stirred up: the daily "
                     "dig spot, walkable). **The fossil ledge** by the tide line (SCRIPT.md Part "
                     "6, the fixed dig): `ledge_skull` `ledge_dart`, a low shelf of soft rock "
                     "with a great one-eyed skull and a stone dart showing in it (impassable; the "
                     "dig's bg events). When the player chooses one, it crumbles into the sea: "
                     "swap both cells to `ledge_gone_L` `ledge_gone_R` (rubble and wet sand, "
                     "walkable). `FLAG_ICHOR_FOSSIL_DUG`.")
    ground(s, "sand")
    M = s.M
    # rock pools: a ring of wet grey rock round a pool of clear water
    def pool(ox, oy, seed, extra=None):
        cx0, cy0 = 7.5 + (seed % 2) * 0.5, 7.5
        for y in range(16):
            for x in range(16):
                ang = math.atan2(y - cy0, x - cx0)
                wob = 0.09 * math.sin(3 * ang + seed) + 0.06 * math.sin(5 * ang + 2 * seed)
                d = math.hypot((x - cx0) / 7.6, (y - cy0) / 7.0) + wob
                pd = math.hypot((x - cx0 - 0.5) / 5.2, (y - cy0 - 0.5) / 3.8) - wob
                if pd < 0.8:
                    c = "kq1" if (x + y + seed) % 5 else "kq2"
                    if y - cy0 < -1.5 and pd > 0.5:
                        c = "b3"
                elif pd < 1.0:
                    c = "kr0" if y < cy0 else "kr1"
                elif d < 0.86:
                    c = "kr2" if (x * 3 + y * 5 + seed) % 7 else "kr3"
                    if y > cy0 + 2:
                        c = "kr1"
                    if N.h(x, y, seed) % 11 == 0:
                        c = "l1"
                elif d < 1.0:
                    c = "kr0"
                else:
                    continue
                M.px(ox + x, oy + y, c)
        if extra:
            extra(ox, oy)
    pool(0, 0, 1, lambda ox, oy: grid(M, ox + 6, oy + 6, [".w.w.", "wwkww", ".www.", "w.w.w"],
                                      {"w": "p3", "k": "kr0"}))
    pool(16, 0, 2, lambda ox, oy: grid(M, ox + 6, oy + 7, ["k.k", ".k.", "kkk", "k.k"],
                                       {"k": "kr0"}))
    pool(48, 0, 3, lambda ox, oy: [grid(M, ox + x, oy + y, [".k.", "kkk", ".k."], {"k": "kr0"})
                                   for (x, y) in ((5, 6), (9, 8), (7, 10))])
    # pool_dig: the pool's sandy lip stirred up
    ox = 32
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 8) / 6.0, (y - 10) / 4.5)
            if d < 0.55:
                M.px(ox + x, y, "kq1" if (x + y) % 4 else "kq2")
            elif d < 0.75:
                M.px(ox + x, y, "kr1")
            elif d < 1.0 and y < 10:
                M.px(ox + x, y, "kr2")
    for (x, y) in ((3, 3), (12, 2), (5, 14), (11, 13), (2, 9), (14, 8)):
        grid(M, ox + x - 1, y - 1, [".s.", "sSs", ".s."], {"s": "ks1", "S": "p1"})
    # the fossil ledge: a low shelf of buff rock, the skull and the dart in it
    for cx in (0, 1):
        ox, oy = cx * 16, 16
        for y in range(16):
            for x in range(16):
                top = 3 + (N.h(x + cx * 16, 0, 2) % 2)
                if cx == 0 and x < 2:
                    top += 2 - x
                if cx == 1 and x > 13:
                    top += x - 13
                if y < top:
                    continue
                if y == top:
                    c = "p3"
                elif y == top + 1:
                    c = "p2"
                elif y < 13:
                    band = (y + (x // 5)) % 4
                    c = ("p2", "p1", "p1", "l1")[band]
                    if N.h(x + cx * 16, y, 6) % 17 == 0:
                        c = "kr1"
                elif y < 15:
                    c = "l1" if (x + y) % 2 else "kr0"
                else:
                    c = "kq2" if (x + cx) % 2 else None
                if c:
                    M.px(ox + x, oy + y, c)
    # the skull: a great dome with one eye socket in the middle
    grid(M, 3, 16 + 5, [
        "..kkkkkk..",
        ".k333333k.",
        "k33kkkk33k",
        "k3kk..kk3k",
        "k33kkkk33k",
        ".k3k33k3k.",
        "..kkkkkk..",
    ], {"k": "kr0", "3": "p3"})
    # the dart: a belemnite's long point
    grid(M, 16 + 2, 16 + 7, [
        "kkkk.........",
        "k333kkkk.....",
        "k3333333kkkk.",
        "k333kkkk....k",
        "kkkk.........",
    ], {"k": "kr0", "3": "p3"})
    # gone: wet sand and rubble where the ledge fell into the sea
    for cx in (2, 3):
        ox, oy = cx * 16, 16
        for (x, y) in ((2, 4), (7, 6), (11, 3), (4, 10), (12, 9), (8, 12)):
            grid(M, ox + x, oy + y, [".pp", "plk", ".kk"], {"p": "p2", "l": "l1", "k": "kr0"})
        for y in range(13, 16):
            for x in range(16):
                if (x + y) % 2:
                    M.px(ox + x, oy + y, "ks1")
    s.walk = ["XX.X", "XX.."]
    return s


def build():
    return [talos_foot(), tide_pools()]
