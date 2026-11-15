"""gTileset_FarWest: the sunset end of the world.

LABORS's Labor 10 (Erytheia, Geryon's pasture, the Strait of the Pillars, the
Ocean Stream) and, for the Oikoumene, the Atlantic shore and the country
round Tartessos. Red sunset light on everything: red earth, low maquis,
grass lit gold with violet shadows, red rock, a sea going pink and gold.

  ground   red earth (on grass and on sand), sunset-lit tall grass (on grass
           and on red earth), a river, maquis, boulders, slag
  coast    a sunset surf, Atlantic breakers, the sun's road on the water,
           sea stacks and tide pools
  rock     a red-rock crag kit: lips, faces, feet in the sea, ledges, a cave
           mouth, a mine head
  pillars  the Pillars of Herakles, standing and fallen, their sockets; the
           glow between them and the fog bank beyond
  places   the dock where Helios's cup moors, Eurytion's hut, the Ocean
           Stream's rocks of light and the edge of the world
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
import farlands_ground as G
import farlands_kits as K
from farlands_lib import anim_layer, ground, put, struct

GROUPS = {
    # red earth on grass and sand, and the river's banks
    "red": ["g1", "g2", "g3", "gd", "re0", "re1", "re2", "re3", "re4", "ks1", "ks2", "p3", "md0",
            "b2", "b4"],
    # sunset-lit grass, slag, the starry void past the edge of the world
    "dusk": ["dg0", "dg1", "dg2", "dg3", "dg4", "ev0", "ev1", "sl0", "sl1", "sl2", "ns0", "ns1",
             "ns2", "gl", "w0"],
    # the sea at sunset: surf, breakers, the sun's road, fog, the glow
    "sea": ["b1", "b2", "b3", "b4", "w0", "pk1", "pk2", "gl", "ks1", "ks2", "p3", "ev1", "ev2",
            "ev3", "ns1"],
    # red rock: crags, stacks, tide pools, the mine head
    "rock": ["rr0", "rr1", "rr2", "rr3", "rr4", "ev0", "ev1", "gd", "g1", "w0", "b3", "b4", "gl",
             "ink", "mq1"],
    # maquis
    "scrub": ["mq0", "mq1", "mq2", "mq3", "tg", "pk1", "w0", "gd", "g1", "dg2", "dg3", "re1",
              "rb1", "ev1"],
    # marble and gold: the Pillars, the cup's dock
    "marble": ["ml0", "ml1", "ml2", "ml3", "w0", "gl", "ev1", "ev2", "ink", "gd", "g1", "b3",
               "ap1", "ap2", "ap3"],
    # timber, thatch and field stone: Eurytion's hut
    "works": ["tb0", "tb1", "tb2", "tb3", "dg1", "dg2", "dg3", "rr1", "rr2", "rr3", "rr4", "ink",
              "gd", "g1", "ev1"],
}

SEC_G, SEC_C, SEC_R, SEC_P, SEC_X = "ground", "coast", "rock", "pillars", "places"
RR = ("rr0", "rr1", "rr2", "rr3", "rr4")


# --------------------------------------------------------------------------
# Ground
# --------------------------------------------------------------------------

def _red_px(X, Y):
    x, y = X % 16, Y % 16
    k = F.hp(x, y, 91)
    c = "re2"
    if k % 6 == 0:
        c = "re3"
    elif k % 9 == 0:
        c = "re1"
    for (px, py) in ((3, 4), (11, 2), (13, 11), (6, 13), (8, 8)):
        if (x, y) == (px, py):
            c = "re4"
        elif (x, y) == (px, py + 1):
            c = "re1"
        elif (x, y) == (px + 1, py + 1):
            c = "re0"
    # a dry crack
    if (x, y) in ((1, 9), (2, 9), (3, 10), (4, 10), (5, 11), (12, 6), (13, 5), (14, 5)):
        c = "re1"
    return c


RED_PAINT = dict(margin=2.5, radius=4.5, amp=2.0, seed=5.7)


def _red_painter():
    return G.earth_overlay(_red_px, "re1", None, **RED_PAINT)


def red_earth():
    return G.blob_set(
        "red_earth", "Red earth", SEC_G, _red_painter(), on="grass", walk=".",
        notes="Erytheia's ground: iron-red earth, cracked and pebbled, 47 soft-edge shapes over "
              "borrowed aethos grass. Walkable. Use it for the island's open ground, cattle tracks "
              "(a region one cell wide) and the trodden ground round the hut and the den; aethos "
              "grass shows between. Its edge fades onto aethos grass, so a seam strip can be grass.")


def red_earth_sand():
    s = G.blob_set(
        "red_earth_sand", "Red earth on sand", SEC_G, _red_painter(), on="sand", walk=".",
        notes="The same 47 shapes over borrowed aethos sand (the same tiles: only the ground "
              "differs), for where red earth runs down to a beach.")
    return s


def _dusk_tex():
    """aethos's barley, pixel for pixel, lit by the setting sun: gold blades,
    violet shadows."""
    return G.recolor_tex(0x00D, {"t0": "ev0", "t1": "dg1", "gd": "dg2", "t3": "dg3", "tg": "dg4"})


def _dusk_painter():
    return G.grass_overlay(_dusk_tex(), "ev0", "dg3", "dg4", seed=3.3)


def dusk_grass():
    return G.blob_set(
        "dusk_grass", "Sunset grass (encounters)", SEC_G, _dusk_painter(), on="grass", walk="G",
        notes="Tall grass lit by a sun that never quite sets: gold blades, violet shadows between "
              "them, 47 soft-edge shapes over borrowed aethos grass. `MB_TALL_GRASS`. The forced "
              "bands and the optional fields of Erytheia and the pasture.")


def dusk_grass_red():
    return G.blob_set(
        "dusk_grass_red", "Sunset grass on red earth (encounters)", SEC_G, _dusk_painter(),
        on=None, walk="G",
        base=lambda L, ox, oy: [L.px(ox + x, oy + y, _red_px(ox + x, oy + y))
                                for y in range(16) for x in range(16)],
        notes="The same grass growing out of red earth: its edges fade onto `red_earth`'s full "
              "interior. Lay it inside a red-earth region (a cell of it next to plain grass would "
              "show red earth there, so keep a cell of red earth round it).")


def river():
    paint = G.water_painter(lambda X, Y: F.grass_px(X, Y), ("re0", "re1", "g3"), "b2", "b4",
                            seed=6.3)
    return G.blob_set(
        "river", "A river", SEC_G, paint, on="sea", walk="P", oik=True,
        notes="Fresh water (`MB_POND_WATER`) over borrowed aethos sea, its banks cut in red earth: "
              "47 soft-edge shapes of the water, the land side of an edge cell drawn as aethos grass "
              "pixel for pixel. The Baetis below Tartessos's silver mines, and the brooks of Erytheia.")


def scrub():
    names = {"lentisk": (0, 0), "lentisk_b": (1, 0), "palm": (2, 0), "broom": (3, 0),
             "cistus": (4, 0), "thistle": (5, 0)}
    s = struct("scrub", "Maquis: lentisk, dwarf palm, broom, cistus", 6, 1, SEC_G,
               walk=["XXXX.."], names=names,
               notes="Low scrub on borrowed grass, lit from the west. Impassable: `lentisk` and "
                     "`lentisk_b`, dark glossy mastic bushes; `palm`, a dwarf fan-palm; `broom`, in "
                     "yellow flower. Walkable: `cistus`, a low rock-rose with pink flowers; "
                     "`thistle`, a few purple-headed thistles. Scatter them on grass and red earth's "
                     "edges; line a cattle track with them.")
    ground(s, "grass")
    M = s.M
    ramp = ("mq0", "mq1", "mq2", "mq3")
    for i, (cx, cy, rx, ry, seed) in enumerate(((8, 9, 7, 5.5, 1.0), (7.5, 9.5, 6.5, 5.0, 2.5))):
        m = F.blob(cx, cy, rx, ry, 16, 16, wobble=0.12, k=6, seed=seed)
        tmp = F.Layer(16, 16)
        F.foliage(tmp, m, ramp, seed=7 + i, outline="mq0", clump=3.0)
        for y, x in np.argwhere(m):
            M.px(i * 16 + x, y, tmp.get(x, y))
        for x in range(16):
            for y in range(1, 16):
                if not m[y, x] and m[y - 1, x]:
                    M.px(i * 16 + x, y, "gd")
                    if x + 1 < 16:
                        M.px(i * 16 + x + 1, y, "gd") if not m[y, min(15, x + 1)] else None
    # dwarf palm: fronds fanning from a short trunk
    for a in range(-80, 81, 20):
        r = 7
        ang = math.radians(a - 90)
        for j in range(r):
            x = 40 + int(round(math.cos(ang) * j))
            y = 10 + int(round(math.sin(ang) * j * 0.8))
            M.px(x, y, "mq3" if j > r - 3 else ("mq2" if a < 0 else "mq1"))
            M.px(x + 1, y, "mq1") if j > 2 else None
    for y in range(10, 14):
        M.px(40, y, "rb1")
        M.px(41, y, "re1")
    for x in range(37, 45):
        M.px(x, 14, "gd")
    # broom: a mound of green twigs dotted yellow
    m = F.blob(7.5, 9, 6.5, 5.5, 16, 16, wobble=0.1, k=7, seed=4.0)
    tmp = F.Layer(16, 16)
    F.foliage(tmp, m, ramp, seed=11, outline="mq0", clump=2.5, flowers=["tg", "dg3", "tg"], fl_rate=2)
    for y, x in np.argwhere(m):
        M.px(48 + x, y, tmp.get(x, y))
    for x in range(16):
        for y in range(1, 16):
            if not m[y, x] and m[y - 1, x]:
                M.px(48 + x, y, "gd")
    # cistus: low cushions, pink flowers
    for (cx, cy) in ((4, 5), (11, 9), (5, 12)):
        m = F.blob(cx, cy, 3.5, 2.6, 16, 16, wobble=0.1, k=5, seed=cx)
        for y, x in np.argwhere(m):
            M.px(64 + x, y, "mq2" if (x + y) % 3 else "mq1")
        M.px(64 + cx, cy - 1, "pk1")
        M.px(64 + cx - 1, cy, "w0")
        M.px(64 + cx + 1, cy, "pk1")
    # thistles
    for (x, y) in ((4, 4), (10, 7), (6, 11), (13, 12)):
        for j in range(4):
            M.px(80 + x, y + j, "mq1" if j else "ev1")
        M.px(80 + x - 1, y, "ev1")
        M.px(80 + x + 1, y, "ev1")
        M.px(80 + x, y - 1, "pk1")
        M.px(80 + x + 1, y + 2, "mq2")
    return s


def rocks():
    names = {"boulder": (0, 0), "boulders": (1, 0), "slag": (2, 0), "slag_b": (3, 0)}
    s = struct("rocks", "Red boulders and slag heaps", 4, 1, SEC_G, walk=["XXXX"], names=names,
               notes="On borrowed grass, impassable: `boulder` and `boulders`, red rock lit gold on "
                     "its western face, violet in shadow. `slag` and `slag_b`: heaps of glassy black "
                     "slag from the silver smelters round Tartessos (the Oikoumene's).")
    ground(s, "grass")
    M = s.M
    K.boulder(M, 0, 0, 7.5, 8.5, 6.5, 5.5, ("rr0", "rr1", "rr2", "rr3", "rr4"), "ev0", "ev1", seed=1)
    K.boulder(M, 16, 0, 5.0, 6.0, 4.5, 4.0, ("rr0", "rr1", "rr2", "rr3", "rr4"), "ev0", "ev1", seed=2)
    K.boulder(M, 16, 0, 11.0, 11.0, 4.0, 3.5, ("rr0", "rr1", "rr2", "rr3", "rr4"), "ev0", "ev1", seed=3)
    for i, seed in ((2, 1.5), (3, 4.1)):
        m = F.blob(7.5, 9.5, 7.0, 5.5 if i == 2 else 4.5, 16, 16, wobble=0.15, k=7, seed=seed)
        for y, x in np.argwhere(m):
            u = (x - 7.5) + (y - 9.5)
            k = F.h(x, y, i)
            c = "sl2" if u < -4 else ("sl1" if u < 3 else "sl0")
            if k % 7 == 0:
                c = "ns2" if u < 0 else "sl2"
            if k % 13 == 0:
                c = "gl"
            M.px(i * 16 + x, y, c)
        for x in range(16):
            for y in range(1, 16):
                if not m[y, x] and m[y - 1, x]:
                    M.px(i * 16 + x, y, "ev0")
    return s


# --------------------------------------------------------------------------
# Coast: the sunset surf, breakers, the sun's road
# --------------------------------------------------------------------------

def _wob(t, k=0):
    t = t % 16
    w = 1.0 * math.sin(2 * math.pi * t / 16 + 0.4) + 0.5 * math.sin(4 * math.pi * t / 16 + 1.3)
    if k:
        w += k * math.sin(math.pi * t / 16)
    return w


def _inter(a, b, r=4.0):
    if a < r and b < r:
        return r - math.hypot(max(r - a, 0), max(r - b, 0))
    return min(a, b)


def _union(a, b, r=4.0):
    return -_inter(-a, -b, r)


def _sd_S(x, y):
    return 7 + _wob(x) - y


def _sd_N(x, y):
    return y - (8 - _wob(x + 5))


def _sd_E(x, y):
    return 7 + _wob(y + 3) - x


def _sd_W(x, y):
    return x - (8 - _wob(y + 9))


SHORES = {
    "S": lambda x, y: _sd_S(x, y), "N": lambda x, y: _sd_N(x, y),
    "E": lambda x, y: _sd_E(x, y), "W": lambda x, y: _sd_W(x, y),
    "out_NW": lambda x, y: _inter(_sd_S(x, y), _sd_E(x, y)),
    "out_NE": lambda x, y: _inter(_sd_S(x, y), _sd_W(x, y)),
    "out_SW": lambda x, y: _inter(_sd_N(x, y), _sd_E(x, y)),
    "out_SE": lambda x, y: _inter(_sd_N(x, y), _sd_W(x, y)),
    "in_SE": lambda x, y: _union(_sd_S(x, y), _sd_E(x, y)),
    "in_SW": lambda x, y: _union(_sd_S(x, y), _sd_W(x, y)),
    "in_NE": lambda x, y: _union(_sd_N(x, y), _sd_E(x, y)),
    "in_NW": lambda x, y: _union(_sd_N(x, y), _sd_W(x, y)),
}
FRONT = (0.6, -1.4, 1.8)


def _bubbles(X, Y, f):
    x, y = (X + 3 * f) % 16, (Y + (f * 5) // 2) % 16
    v = (x * 5 + y * 7 + (x * y) % 5) % 13
    return v in (0, 3, 4, 8) or ((x + 2 * y) % 7 == 0)


def _surf_px(d, X, Y, f):
    """The sunset surf at signed distance d (sand > 0) in frame f: wet sand
    gone gold, foam lit pink."""
    F_ = FRONT[f]
    if d > F_:
        if d > 2.6:
            return F.sand_px(X, Y)
        if d > 0.0:
            if d > 1.9 and F.hp(X, Y, 3) % 2:
                return "ks2"
            return "gl" if F.hp(X, Y, 7) % 17 == 0 else "ks1"
        return "pk2" if d > -3.2 else ("b3" if (X + Y) % 2 else "pk2")
    if d > F_ - 1.1:
        return "w0"
    if d > F_ - 4.2:
        if _bubbles(X, Y, f):
            return "w0" if d > F_ - 2.6 else "pk2"
        if d > -3.6:
            return "b3" if (X + Y + f) % 3 == 0 else "b4"
        return "pk2" if (X * 3 + Y) % 5 == 0 else None
    if d > -3.6:
        return "b4"
    if d > -4.6:
        return "pk1" if (X + 2 * Y) % 3 == 0 else None
    return None


def surf():
    names_ = list(SHORES)
    w = 6
    cells = {n: (i % w, i // w) for i, n in enumerate(names_)}
    s = struct("surf", "The sunset surf", w, 2, SEC_C, walk=["WWWWWW", "WWWWWW"], names=cells,
               notes="Where sand meets the evening sea: each cell borrows aethos's animated sea and "
                     "draws the sand down to the waterline (aethos sand pixel for pixel, so it meets "
                     "plain aethos sand `0x124`), wet sand gone gold, and foam lit pink by the low "
                     "sun, washing up and back (the `surf` animation). Named by where the sea is: `S` "
                     "(sand north, sea south), `N`, `E`, `W`; `out_NW` is a sand spit's south-east "
                     "tip (sand to the north-west), and so on; `in_SE` is a cove's corner, sea only "
                     "to the south-east. Every cell is `MB_OCEAN_WATER`, as aethos's beach edges are. "
                     "Where a far-west beach meets a seam, end it with aethos's own sand and sea.")
    ground(s, "sea")
    frames = anim_layer(s, "surf", 3)
    for n, (cx, cy) in cells.items():
        for f, L in enumerate([s.M] + frames):
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, cy * 16 + y
                    c = _surf_px(SHORES[n](x, y), X, Y, f)
                    if c:
                        L.px(X, Y, c)
    return s


def sea_marks():
    """Breakers, the sun's road on the water."""
    names = {"breaker": (0, 0), "breaker_b": (1, 0), "sun_road": (2, 0), "sun_road_b": (3, 0)}
    s = struct("sea_marks", "Atlantic breakers and the sun's road", 4, 1, SEC_C, walk=["WWWW"],
               names=names, oik=True,
               notes="Over borrowed aethos sea, surfable. `breaker` and `breaker_b`: a big Atlantic "
                     "roller, a long crest of white water curling and spilling as it comes in (the "
                     "`breakers` animation); lay them in staggered rows two to four cells off a beach "
                     "for the Atlantic shore. `sun_road` and `sun_road_b`: the setting sun's glitter "
                     "on the water, pink and gold, twinkling (`twinkle`); lay a band of them due west "
                     "of a headland, toward the sunset.")
    ground(s, "sea")
    fr = anim_layer(s, "breakers", 4)
    allf = [s.M] + fr
    for i in range(2):
        for f, L in enumerate(allf):
            # the crest moves down the cell over the frames, steepening, then spilling
            cy = 4 + f * 2 + i
            for x in range(16):
                X = i * 16 + x
                yy = cy + int(round(1.2 * math.sin(2 * math.pi * (x + 4 * i) / 16)))
                if f == 3:
                    # spilling: a broad band of foam
                    for dy in range(0, 4):
                        c = "w0" if dy < 2 else ("pk2" if (x + dy) % 2 else "b4")
                        L.px(X, (yy + dy) % 16, c)
                else:
                    L.px(X, yy - 1, "b4")
                    L.px(X, yy, "w0")
                    L.px(X, yy + 1, "pk2" if (x + f) % 3 else "w0")
                    L.px(X, yy + 2, "b2")
                    if f == 2 and x % 3 == 0:
                        L.px(X, yy - 2, "w0")
            # the trough behind the wave
            for x in range(16):
                yy = cy + 4 + int(round(1.2 * math.sin(2 * math.pi * (x + 4 * i + 3) / 16)))
                if (x + f) % 2 == 0:
                    L.px(i * 16 + x, yy % 16, "b2")
    K_ = anim_layer(s, "twinkle", 3)
    for i in (2, 3):
        for f, L in enumerate([s.M] + K_):
            for (x, y) in ((2, 2), (7, 4), (12, 3), (4, 8), (10, 9), (14, 11), (1, 13), (8, 14)):
                xx, yy = (x + 5 * (i - 2)) % 16, (y + 3 * (i - 2)) % 16
                on = (x + y + f + i) % 3
                c = "gl" if on == 0 else ("pk2" if on == 1 else "pk1")
                L.px(i * 16 + xx, yy, c)
                L.px(i * 16 + (xx + 1) % 16, yy, "pk1" if on else "gl")
                if on == 0:
                    L.px(i * 16 + (xx + 2) % 16, yy, "pk2")
    # keep the two animations apart: each touches only its own cells
    F.settle(s, "breakers", [(0, 0), (1, 0)])
    F.settle(s, "twinkle", [(2, 0), (3, 0)])
    return s


def stacks():
    names = {"stack_TL": (0, 0), "stack_TR": (1, 0), "stack_BL": (0, 1), "stack_BR": (1, 1),
             "stack_small": (2, 1), "pool": (3, 1), "pool_b": (3, 0), "stack_small_top": (2, 0)}
    s = struct("stacks", "Sea stacks and tide pools", 4, 2, SEC_C, walk=["TTTX", "XXXX"],
               names=names, oik=True,
               notes="`stack` (2 x 2): a red sea stack standing out of the water, lit gold on its "
                     "western face, foam round its foot; its top row is drawn over the player. "
                     "`stack_small` (1 x 2, with `stack_small_top`): a lone pinnacle. Both stand on "
                     "borrowed sea, impassable. `pool` and `pool_b`: rock shelves with tide pools and "
                     "weed (on borrowed sand), impassable, for the Atlantic shore at low tide.")
    ground(s, "sea", [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (2, 1)])
    ground(s, "sand", [(3, 0), (3, 1)])
    M, T = s.M, s.T

    def stack(ox, oy, w, h_, rx, foot):
        m = F.mask_from(lambda x, y: abs(x - w / 2 + 0.5) < rx * (0.75 + 0.25 * (y / h_))
                        + 0.8 * math.sin(y * 0.7) and 2 <= y <= h_ - 3, w, h_)
        for y, x in np.argwhere(m):
            u = (x - w / 2) / rx
            c = K.rock_px(ox + x, oy + y, RR, 0 if u < 0.2 else 1, 4)
            if u < -0.5:
                c = "gl" if F.h(x, y, 2) % 4 == 0 else "rr4"
            (T if y < 16 else M).px(ox + x, oy + y, c)
        for y, x in np.argwhere(F.edge_of(m)):
            (T if y < 16 else M).px(ox + x, oy + y, "ev0")
        # the top
        for y, x in np.argwhere(m):
            if y < 4:
                (T if y < 16 else M).px(ox + x, oy + y, "rr3")
        # foam at the foot
        for x in range(w):
            for y in range(h_ - 5, h_):
                if not m[min(h_ - 1, y), x] and any(m[yy, xx] for yy in range(max(0, y - 2), min(h_, y + 1))
                                                    for xx in range(max(0, x - 2), min(w, x + 3))):
                    M.px(ox + x, oy + y, "w0" if (x + y) % 3 else "b4")
    stack(0, 0, 32, 32, 9, True)
    stack(32, 0, 16, 32, 4, True)
    # tide pools on rock shelves
    for i, oy in ((0, 16), (1, 0)):
        m = F.blob(7.5, 8, 7.0, 6.0, 16, 16, wobble=0.12, k=5, seed=i * 2.1 + 1)
        for y, x in np.argwhere(m):
            M.px(48 + x, oy + y, K.rock_px(48 + x, oy + y, RR, 0, 7))
        for y, x in np.argwhere(F.edge_of(m)):
            M.px(48 + x, oy + y, "ev0" if y > 7 else "rr2")
        for (px, py, r) in (((6, 7, 2.8), (10, 10, 2.0)) if i == 0 else ((8, 8, 3.2),)):
            for y in range(16):
                for x in range(16):
                    d = math.hypot(x - px, (y - py) * 1.3)
                    if d < r and m[y, x]:
                        M.px(48 + x, oy + y, "b3" if y < py else "b4")
                    elif d < r + 1 and m[y, x] and y >= py:
                        M.px(48 + x, oy + y, "mq1")
            M.px(48 + int(px) - 1, oy + int(py), "gl")
    return s


# --------------------------------------------------------------------------
# Red rock
# --------------------------------------------------------------------------

def crag():
    def foot_sea(s, M, ox, oy):
        # repaint as a face whose foot stands in the sea, foam at the base
        for y in range(16):
            for x in range(16):
                M.px(ox + x, oy + y, None)
        for x in range(16):
            bot = 6 + int(round(1.2 * math.sin(2 * math.pi * (x + 7) / 16)))
            for y in range(0, bot):
                M.px(ox + x, oy + y, K.rock_px(ox + x, oy + y, RR, 1 if y >= bot - 2 else 0, 1))
            M.px(ox + x, oy + bot, "w0")
            M.px(ox + x, oy + bot + 1, "w0" if x % 3 else "b4")
            if x % 2:
                M.px(ox + x, oy + bot + 2, "b4")

    def mine(s, M, ox, oy):
        K.adit(M, ox, oy, ("rr0", "rr1", "rr2"), ("rr0", "ink"), "rr4", spoil="rr2")

    def cave(s, M, ox, oy):
        K.cave_mouth(M, ox, oy, ("ev0", "ink"), "rr1")

    def lit(s, M, ox, oy):
        # the face catching the last of the sun
        for y in range(16):
            for x in range(16):
                c = K.rock_px(ox + x + 3, oy + y + 7, RR, -1, 1)
                if F.hp(x, y, 4) % 9 == 0:
                    c = "gl"
                M.px(ox + x, oy + y, c)

    s = K.cliff_kit("crag", "Red crags", SEC_R, RR, "ev0", "ev1",
                    notes=K.CLIFF_NOTES + " Red rock lit from the west, its shadows violet. Extra "
                    "pieces: `face_lit`, a face the sunset strikes full on; `foot_sea_L` `foot_sea` "
                    "`foot_sea_R`, a face whose foot stands in the sea (borrowed sea, foam at the "
                    "base; surfable), for Erytheia's and the Atlantic's sea cliffs and the Strait's "
                    "headlands; `cave`, a cave mouth (Orthros's den, the Atlas range's caves); "
                    "`mine`, a timber-framed mine head (Tartessos's silver mines, the Oikoumene's). "
                    "`cave` and `mine` are `MB_NON_ANIMATED_DOOR`.",
                    seed=1, extra_faces=[("face_lit", lit), ("foot_sea_L", foot_sea),
                                         ("foot_sea", foot_sea), ("foot_sea_R", foot_sea),
                                         ("cave", cave), ("mine", mine)])
    # the sea feet sit on borrowed sea
    for n in ("foot_sea_L", "foot_sea", "foot_sea_R"):
        cx, cy = s.names[n]
        s.ground[(cx, cy)] = "sea"
    # trim the _L/_R sea feet's ends
    for n, end in (("foot_sea_L", "L"), ("foot_sea_R", "R")):
        cx, cy = s.names[n]
        for y in range(16):
            for x in range(16):
                if (end == "L" and x < 3) or (end == "R" and x > 12):
                    if s.M.get(cx * 16 + x, cy * 16 + y) not in ("w0", "b4"):
                        s.M.px(cx * 16 + x, cy * 16 + y, None)
    F.set_walk(s, ["XXXX", "XXXX", "XXXX", "XXXX", "....", "XWWW", "DDXX"])
    return s


def ledges():
    names = {"S_L": (0, 0), "S": (1, 0), "S_R": (2, 0), "W": (3, 0), "E": (4, 0)}
    s = struct("ledges", "Red-rock ledges", 5, 1, SEC_R, walk=["JJJ<>"], names=names, oik=True,
               notes="One-way drops in red rock on borrowed grass: `S_L` `S` `S_R` jump south (a run "
                     "and its ends), `W` jumps west, `E` east. For Erytheia's gully, the Atlas "
                     "foothills' steep slopes and the Oikoumene's red uplands.")
    ground(s, "grass")
    M = s.M
    for i in range(3):
        for x in range(16):
            if i == 0 and x < 3 or i == 2 and x > 12:
                continue
            top = 8 + int(round(_wob(x + 3 * i) * 0.6))
            for y in range(top, top + 5):
                c = "rr4" if y == top else ("rr3" if y == top + 1 else ("rr2" if y < top + 4 else "rr1"))
                M.px(i * 16 + x, y, c)
            M.px(i * 16 + x, top + 5, "ev1")
            M.px(i * 16 + x, top - 1, "rr1") if x % 4 == 0 else None
    for i, side in ((3, "W"), (4, "E")):
        for y in range(16):
            for k in range(5):
                x = 6 + k if side == "W" else 9 - k
                c = "rr4" if k == 0 else ("rr3" if k == 1 else ("rr2" if k < 4 else "rr1"))
                M.px(i * 16 + x, y, c)
            M.px(i * 16 + (5 if side == "W" else 10), y, "ev1")
    return s


# --------------------------------------------------------------------------
# The Pillars of Herakles
# --------------------------------------------------------------------------

LETTERS = {
    "N": ["1..1", "11.1", "1.11", "1..1", "1..1"],
    "E": ["111", "1..", "11.", "1..", "111"],
    "P": ["11.", "1.1", "11.", "1..", "1.."],
    "L": ["1..", "1..", "1..", "1..", "111"],
    "U": ["1.1", "1.1", "1.1", "1.1", "111"],
    "S": [".11", "1..", ".1.", "..1", "11."],
    "T": ["111", ".1.", ".1.", ".1.", ".1."],
    "R": ["11.", "1.1", "11.", "1.1", "1.1"],
    "A": [".1.", "1.1", "111", "1.1", "1.1"],
}


def _carve(L, x, y, word):
    for ch in word:
        g = LETTERS[ch]
        for j, row in enumerate(g):
            for i, c in enumerate(row):
                if c == "1":
                    L.px(x + i, y + j, "ap2")
                    L.px(x + i + 1, y + j + 1, "ml0") if L.get(x + i + 1, y + j + 1) not in ("ap2",) else None
        x += len(g[0]) + 1


def _column(L, T, ox, oy, words, lit_west=True):
    """A 2 x 6 column: capital, shaft with words carved and gilded, base."""
    W, H = 32, 96
    # shaft: fluted, lit from the west
    for y in range(18, 86):
        for x in range(5, 27):
            fl = (x - 5) % 4
            u = (x - 5) / 21
            i = 3 if u < 0.25 else (2 if u < 0.6 else (1 if u < 0.85 else 0))
            if fl == 0:
                i = max(0, i - 1)
            c = ("ml0", "ml1", "ml2", "ml3")[i]
            if u < 0.12 and fl and F.h(x, y, 2) % 5 == 0:
                c = "w0"
            (T if y < 32 else L).px(ox + x, oy + y, c)
        (T if y < 32 else L).px(ox + 4, oy + y, "ink")
        (T if y < 32 else L).px(ox + 27, oy + y, "ink")
    # capital: echinus and abacus
    for y in range(4, 18):
        for x in range(0, 32):
            if y < 9:
                ok = 0 <= x < 32
                c = "ml3" if y == 4 else ("ml2" if x < 18 else "ml1")
            else:
                half = 13 - (y - 9) * 0.9
                ok = abs(x - 15.5) <= half + 1
                c = "ml2" if x < 14 else "ml1"
                if y == 9:
                    c = "ml0"
            if ok:
                T.px(ox + x, oy + y, c)
        for x in range(0, 32):
            if T.get(ox + x, oy + y):
                pass
    for x in range(0, 32):
        T.px(ox + x, oy + 3, "ink")
        T.px(ox + x, oy + 8, "ml0")
    for y in range(3, 9):
        T.px(ox, oy + y, "ink")
        T.px(ox + 31, oy + y, "ink")
    # gold band under the capital
    for x in range(5, 27):
        T.px(ox + x, oy + 17, "ap1")
        T.px(ox + x, oy + 18, "ap2" if x < 16 else "ap1")
    # base: a square plinth
    for y in range(86, 96):
        for x in range(1, 31):
            c = "ml2" if y < 88 else ("ml1" if x < 20 else "ml0")
            if y == 86:
                c = "ml3"
            L.px(ox + x, oy + y, c)
        L.px(ox + 1, oy + y, "ink")
        L.px(ox + 30, oy + y, "ink")
    for x in range(1, 31):
        L.px(ox + x, oy + 95, "ink")
        L.px(ox + x, oy + 85, "ink")
    # the inscription
    yy = oy + 40
    for word in words:
        wpx = sum(len(LETTERS[c][0]) + 1 for c in word) - 1
        _carve(L, ox + 16 - wpx // 2, yy, word)
        yy += 9
    # the evening shadow east of the column
    for y in range(90, 96):
        for x in range(31, 32):
            L.px(ox + x, oy + y, "ev1")


def pillars():
    names = {}
    for side, x0 in (("W", 0), ("E", 2)):
        for y in range(6):
            for x in range(2):
                names[f"{side}{x}{y}"] = (x0 + x, y)
    names.update({"socket_L": (4, 5), "socket_R": (5, 5)})
    for x in range(4):
        for y in range(2):
            names[f"fallen{x}{y}"] = (4 + (x % 2), 1 + y + 2 * (x // 2))
    s = struct("pillars", "The Pillars of Herakles", 6, 6, SEC_P,
               walk=["TTTTTT", "TTTTXX", "XXXXXX", "XXXXXX", "XXXXXX", "XXXXXX"], names=names,
               notes="The two Pillars, 2 x 6 each, on borrowed grass: `W00` to `W15` (column then "
                     "row) carries NE PLUS carved and gilded on its shaft, `E00` to `E15` ULTRA. Their "
                     "top two rows (the capital and the shaft's top) are drawn over the player; the "
                     "rest is impassable. The set piece (LABORS 10, step 3): each headland starts with "
                     "a fallen column, `fallen00` to `fallen31` (4 x 2, lying west-east, the capital "
                     "at its east end; impassable), beside an empty `socket_L` `socket_R` (2 x 1, the "
                     "plinth's cut). When the Girdle pushes it upright, swap the fallen cells to grass "
                     "and the socket and the 2 x 5 above it to the standing pillar (the socket becomes "
                     "the pillar's base row, `W05` `W15`). The labels below name each swap.")
    ground(s, "grass")
    M, T = s.M, s.T
    # standing pillars: draw into a tall scratch, then split cells (top two rows: T)
    for side, x0, words in (("W", 0, ["NE", "PLUS"]), ("E", 32, ["ULTRA"])):
        tmpM = F.Layer(32, 96)
        tmpT = F.Layer(32, 96)
        _column(tmpM, tmpT, 0, 0, words)
        for y in range(96):
            for x in range(32):
                c = tmpT.get(x, y) or tmpM.get(x, y)
                if c:
                    (T if y < 32 else M).px(x0 + x, y, c)
    # the empty socket
    for y in range(4, 16):
        for x in range(1, 31):
            c = "ml2" if y < 6 else ("ml1" if x < 20 else "ml0")
            if y == 4:
                c = "ml3"
            M.px(64 + x, 80 + y, c)
        M.px(64 + 1, 80 + y, "ink")
        M.px(64 + 30, 80 + y, "ink")
    for x in range(1, 31):
        M.px(64 + x, 80 + 3, "ink")
        M.px(64 + x, 80 + 15, "ink")
    for y in range(6, 12):
        for x in range(6, 26):
            M.px(64 + x, 80 + y, "ml0" if y < 8 else "ev1")
    # the fallen column: lying west-east across a 4 x 2 footprint, in two
    # 2 x 2 halves stacked in the sheet (fallen00-11 west, fallen20-31 east)
    lay = F.Layer(64, 32)
    for x in range(2, 50):
        for y in range(8, 26):
            v = (y - 8) / 17
            i = 3 if v < 0.25 else (2 if v < 0.6 else (1 if v < 0.85 else 0))
            if (y - 8) % 4 == 0:
                i = max(0, i - 1)
            lay.px(x, y, ("ml0", "ml1", "ml2", "ml3")[i])
        lay.px(x, 7, "ink")
        lay.px(x, 26, "ink")
    for x in range(50, 62):
        half = 10 + (x - 50) * 0.5
        for y in range(int(17 - half), int(17 + half) + 1):
            if 0 <= y < 32:
                lay.px(x, y, "ml2" if y < 17 else "ml1")
    for y in range(4, 31):
        lay.px(62, y, "ink")
    for x in range(2, 62):
        if lay.get(x, 27) is None:
            lay.px(x, 27, "ev1")
            lay.px(x, 28, "gd") if x % 2 else None
    for x in range(48, 50):
        for y in range(8, 26):
            lay.px(x, y, "ap1")
    _carve(lay, 12, 14, "NE")
    for (hx, hy) in ((0, 0), (32, 0)):
        for y in range(32):
            for x in range(32):
                c = lay.get(hx + x, y)
                if c:
                    dx, dy = (64, 16) if hx == 0 else (64, 48)
                    M.px(dx + x, dy + y, c)
    return s


def strait():
    names = {"glow": (0, 0), "glow_b": (1, 0), "fog_E": (2, 0), "fog": (3, 0), "fog_shape": (4, 0),
             "fog_shape_b": (5, 0)}
    s = struct("strait", "The glow between the Pillars, the fog bank beyond", 6, 1, SEC_P,
               walk=["WWWWWW"], names=names,
               notes="Over borrowed sea, surfable. `glow` and `glow_b`: the sea between the Pillars "
                     "once both stand, lit from below, pulsing gold (`glow`); swap them in across the "
                     "strait in the set piece. The fog bank west of the strait: `fog_E` its eastern "
                     "edge (fog to the west), `fog` its body, and `fog_shape` `fog_shape_b` a dark "
                     "shape on the horizon in the fog, a seed for Atlantis (POSTGAME 3). Aeolus's "
                     "Bag parts the fog (the Oikoumene's waters of the Strait).")
    ground(s, "sea")
    fr = anim_layer(s, "glow", 3)
    for i in (0, 1):
        for f, L in enumerate([s.M] + fr):
            for y in range(16):
                for x in range(16):
                    v = (x + 2 * y + 5 * i + 3 * f) % 7
                    if v == 0:
                        L.px(i * 16 + x, y, "gl")
                    elif v == 3 and (x + f) % 2:
                        L.px(i * 16 + x, y, "pk2" if f != 1 else "gl")
                    elif v == 5 and f == 2:
                        L.px(i * 16 + x, y, "b4")
    M = s.M
    # fog: a dithered bank of violet-white mist, denser westward
    for i in (2, 3, 4, 5):
        for y in range(16):
            for x in range(16):
                X = i * 16 + x
                dens = 1.0 if i != 2 else max(0.0, (10 - x) / 10 + 0.15 * math.sin(y * 0.8))
                k = F.hp(x, y, 33)
                if dens >= 1.0:
                    c = "ev3" if (x + y) % 2 else ("w0" if k % 3 else "ev2")
                    M.px(X, y, c)
                elif dens > 0.0 and (k % 10) / 10 < dens:
                    M.px(X, y, "ev3" if (x + y) % 2 else "ev2")
    for i, (cx, w) in ((4, (9, 7)), (5, (0, 8))):
        pass
    # the dark shape: a low silhouette of something built, rings and a spire
    sil = [
        "................................",
        "...............1................",
        "..............111...............",
        "..............111...............",
        ".............11111..............",
        "...........111111111............",
        ".......1111111111111111.........",
        "...1111111111111111111111111....",
        ".111111111111111111111111111111.",
    ]
    for j, row in enumerate(sil):
        for x, ch in enumerate(row):
            if ch == "1":
                M.px(64 + x, 5 + j, "ns1" if (x + j) % 3 else "ev1")
    F.settle(s, "glow", [(0, 0), (1, 0)])
    return s


# --------------------------------------------------------------------------
# Places
# --------------------------------------------------------------------------

def dock():
    names = {"quay_L": (0, 0), "quay": (1, 0), "quay_R": (2, 0), "steps": (3, 0), "bollard": (4, 0),
             "cup_TL": (0, 1), "cup_T": (1, 1), "cup_TR": (2, 1), "cup_BL": (0, 2), "cup_B": (1, 2),
             "cup_BR": (2, 2), "sundisc": (3, 1), "sundisc_b": (4, 1)}
    s = struct("dock", "Where Helios's cup moors", 5, 3, SEC_X,
               walk=["XXX.X", "WWW..", "WWWXX"], names=names,
               notes="The cup's landing: a marble quay whose face drops into the sea (`quay_L` "
                     "`quay` `quay_R`, the quay's south edge over borrowed sea; walk on the paving "
                     "above them, which is aethos limestone path), `steps` going down into the water, "
                     "a gilded `bollard` to moor to (impassable), and a sun-disc set in the paving "
                     "(`sundisc`, walkable; `sundisc_b` impassable as a plinth). The cup itself, "
                     "`cup_TL` to `cup_BR` (3 x 2 on borrowed sea): a great golden bowl the size of a "
                     "house rocking in the shallows, full of light. It is there at sunset only: put "
                     "it in with a script (the labels below) and take it out after. For the Western "
                     "Cape (pair the cape's map with this set) and Erytheia's landing.")
    ground(s, "sea", [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)])
    ground(s, "path", [(4, 0), (3, 1), (4, 1), (3, 2), (4, 2)])
    M = s.M
    for i in range(3):
        for y in range(0, 11):
            for x in range(16):
                if i == 0 and x < 2 or i == 2 and x > 13:
                    continue
                c = "ml2" if y < 2 else ("ml1" if (x + (y // 4) * 8) % 16 else "ml0")
                if y in (5, 10):
                    c = "ml0"
                if y == 0:
                    c = "ml3"
                M.px(i * 16 + x, y, c)
        for x in range(16):
            if not (i == 0 and x < 2 or i == 2 and x > 13):
                M.px(i * 16 + x, 11, "w0" if x % 3 else "b3")
                if x % 2:
                    M.px(i * 16 + x, 12, "b3")
        if i == 1:
            for (x, y) in ((7, 6), (8, 6)):
                M.px(x + 16, y, "ap2")
                M.px(x + 16, y + 1, "ap1")
    # steps down into the sea
    for j in range(5):
        for x in range(2, 14):
            y = j * 3
            M.px(48 + x, y, "ml3")
            M.px(48 + x, y + 1, "ml1")
            M.px(48 + x, y + 2, "ml0" if j < 4 else "b3")
    # bollard
    put(M, 64 + 4, 2, [
        "..0000..",
        ".032210.",
        "03322210",
        ".032210.",
        "..0220..",
        "..0320..",
        "..0320..",
        ".032210.",
        "03332210",
        "00000000",
    ], {"0": "ink", "1": "ap1", "2": "ap2", "3": "ap3"})
    for x in range(68, 77):
        M.px(x, 12, "ev1")
    # sun discs in the paving
    for (ox, plinth) in ((48, False), (64, True)):
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - 7.5, y - 7.5)
                if d < 6:
                    M.px(ox + x, 16 + y, "ap2" if d < 3.5 else ("ap3" if (x + y) % 2 else "ap1"))
                elif d < 7.2 and (int(math.degrees(math.atan2(y - 7.5, x - 7.5))) // 30) % 2 == 0:
                    M.px(ox + x, 16 + y, "ap1")
        if plinth:
            for x in range(1, 15):
                M.px(ox + x, 16 + 14, "ml0")
                M.px(ox + x, 16 + 15, "ev1")
    # the cup: a golden bowl, 48 x 32, rocking in the shallows
    cup = F.Layer(48, 32)
    for y in range(32):
        for x in range(48):
            # the rim is an ellipse; the bowl below it
            rim = math.hypot((x - 23.5) / 22.5, (y - 9) / 7.0)
            body = math.hypot((x - 23.5) / 22.5, (y - 9) / 19.0) < 1 and y >= 9
            if rim < 1:
                inner = rim < 0.82
                if inner:
                    c = "ap3" if (x + y) % 5 else "w0"
                    if y > 9:
                        c = "ap2"
                else:
                    c = "ap3" if x < 24 else "ap2"
                cup.px(x, y, c)
            elif body and y < 27:
                u = (x - 23.5) / 22.5
                c = "ap3" if u < -0.5 else ("ap2" if u < 0.3 else "ap1")
                if (x + y * 3) % 11 == 0:
                    c = "gl"
                cup.px(x, y, c)
    m = cup.a[..., 3] > 0
    for y, x in np.argwhere(F.edge_of(m)):
        cup.px(int(x), int(y), "ap1" if y < 10 else "ink")
    for x in range(48):
        for y in range(24, 32):
            if not m[y, x] and m[y - 1, x] if y > 0 else False:
                cup.px(x, y, "w0")
                cup.px(x, min(31, y + 1), "b3") if x % 2 else None
    for y in range(32):
        for x in range(48):
            c = cup.get(x, y)
            if c:
                M.px(x, 16 + y, c)
    return s


def hut():
    names = {f"c{x}{y}": (x, y) for y in range(3) for x in range(3)}
    names["door"] = (1, 2)
    s = struct("hut", "Eurytion's hut", 3, 3, SEC_X, walk=["TTT", "XXX", "XDX"], names=names,
               notes="The herdsman's hut on Erytheia, 3 x 3 on borrowed grass: walls of red field "
                     "stone, a steep thatched roof gone gold in the sunset, a smoke-hole, a crooked "
                     "door (`door`, `MB_NON_ANIMATED_DOOR`). The roof's top row is drawn over the "
                     "player. For any herders' or fishers' huts in the far west.")
    ground(s, "grass")
    M, T = s.M, s.T
    # walls
    for y in range(26, 47):
        for x in range(3, 45):
            k = F.h(x // 4 + (y // 3) * 3, y // 3, 9)
            row = y // 3
            c = ("rr2", "rr3", "rr2", "rr1")[k % 4]
            if (x + (row % 2) * 2) % 6 == 0 or y % 3 == 2:
                c = "rr1"
            if x < 6:
                c = "rr3" if c != "rr1" else "rr2"
            M.px(x, y, c)
        M.px(2, y, "ink")
        M.px(45, y, "ink")
    for x in range(3, 45):
        M.px(x, 46, "ink")
        M.px(x + 2, 47, "ev1") if x < 44 else None
    # roof: thatch, a long ridge, eaves overhanging the wall
    for y in range(4, 30):
        half = 7 + (y - 4) * 0.75
        for x in range(48):
            if abs(x - 23.5) <= min(23.5, half + 10) and y >= 4:
                u = (x - 23.5) / 24
                k = F.hp(x, y, 21)
                c = "dg3" if u < -0.2 else ("dg2" if u < 0.35 else "dg1")
                if k % 5 == 0:
                    c = "dg1" if c != "dg1" else "tb1"
                if (y + x // 3) % 4 == 0 and k % 2:
                    c = "dg2" if c == "dg3" else c
                if y >= 28:
                    c = "tb1" if y == 29 else "dg1"
                (T if y < 16 else M).px(x, y, c)
    for x in range(48):
        for y in range(4, 30):
            L = T if y < 16 else M
            if L.get(x, y) and (y == 4 or not (T if y - 1 < 16 else M).get(x, y - 1)):
                L.px(x, y, "ink")
                break
    # smoke-hole
    for x in range(20, 27):
        T.px(x, 6, "tb0")
        T.px(x, 7, "tb0")
    # door
    for y in range(34, 47):
        for x in range(20, 28):
            c = "tb2" if x < 24 else "tb1"
            if y == 34 or x in (20, 27):
                c = "tb0"
            M.px(x, y, c)
    M.px(26, 41, "rr4")
    return s


def stream():
    names = {"light_rock": (0, 0), "light_rocks": (1, 0), "rim_W": (2, 0), "rim_E": (3, 0),
             "void": (4, 0), "void_b": (5, 0)}
    s = struct("stream", "The Ocean Stream: rocks of light, the edge of the world", 6, 1, SEC_X,
               walk=["XXXXXX"], names=names,
               notes="For the Ocean Stream (LABORS 10): the cup sails west round the edge of the world "
                     "at night. `light_rock` and `light_rocks`: floating rocks of light, the "
                     "obstacles you steer round, glowing (`glow`; borrowed sea). `rim_W`: the world's "
                     "western edge, the sea spilling over a lip of foam into the void (sea to the "
                     "east); `rim_E` the same with the void to the east. `void` and `void_b`: the "
                     "starry dark beyond, impassable. Use the void for the map's border, too.")
    ground(s, "sea", [(0, 0), (1, 0), (2, 0), (3, 0)])
    fr = anim_layer(s, "glow", 3)
    allf = [s.M] + fr
    for i, pts in ((0, [(7.5, 8, 5.5)]), (1, [(5, 6, 3.5), (11, 11, 3.0)])):
        for f, L in enumerate(allf):
            for (cx, cy, r) in pts:
                for y in range(16):
                    for x in range(16):
                        d = math.hypot(x - cx, (y - cy) * 1.2)
                        if d < r:
                            u = (x - cx) + (y - cy)
                            c = "gl" if u < -1 else ("pk2" if u < 2 else "pk1")
                            L.px(i * 16 + x, y, c)
                        elif d < r + 1 + (f % 3) * 0.7 and (x + y + f) % 2 == 0:
                            L.px(i * 16 + x, y, "gl" if f == 1 else "pk2")
    M, B = s.M, s.B
    # the void: stars on deep night
    for i in (4, 5):
        for y in range(16):
            for x in range(16):
                k = F.hp(x + 5 * i, y, 47)
                c = "ns0"
                if k % 31 == 0:
                    c = "w0"
                elif k % 17 == 0:
                    c = "ns1"
                elif k % 23 == 0:
                    c = "ns2"
                B.px(i * 16 + x, y, c)
    for (x, y) in ((4, 4), (12, 10)):
        B.px(64 + x, y, "gl")
        B.px(80 + x - 2, y + 3, "w0")
    # the rims: the sea pours off a lip of foam into the stars
    for i, side in ((2, "W"), (3, "E")):
        for y in range(16):
            edge = 7 + int(round(_wob(y + 2) * 0.8))
            for x in range(16):
                xx = x if side == "W" else 15 - x
                if xx < edge - 2:
                    k = F.hp(x, y + i, 47)
                    c = "ns1" if k % 13 else "w0"
                    if xx > edge - 6 and (y + xx) % 2:
                        c = "ev1"
                    M.px(i * 16 + x, y, c)
                elif xx < edge:
                    M.px(i * 16 + x, y, "w0" if (y + xx) % 3 else "ev3")
                elif xx < edge + 2 and (y + x) % 2:
                    M.px(i * 16 + x, y, "b4")
    F.settle(s, "glow", [(0, 0), (1, 0)])
    return s


# --------------------------------------------------------------------------

def build():
    out = {}
    for s in (red_earth(), red_earth_sand(), dusk_grass(), dusk_grass_red(), river(), scrub(),
              rocks(), surf(), sea_marks(), stacks(), crag(), ledges(), pillars(), strait(), dock(),
              hut(), stream()):
        out[s.key] = s
    return out


SPEC = {
    "symbol": "gTileset_FarWest", "dir": "far_west", "label": "FarWest",
    "title": "the far west: Erytheia, the Pillars, the Ocean Stream",
    "doc": "TILES_far_west.md",
    "limit": 504,
    "sections": [
        ("ground", ["red_earth", "red_earth_sand", "dusk_grass", "dusk_grass_red", "river", "scrub",
                    "rocks"]),
        ("coast", ["surf", "sea_marks", "stacks"]),
        ("rock", ["crag", "ledges"]),
        ("pillars", ["pillars", "strait"]),
        ("places", ["dock", "hut", "stream"]),
    ],
    "rows": {"ground": 0, "coast": 32, "rock": 37, "pillars": 46, "places": 54},
}
