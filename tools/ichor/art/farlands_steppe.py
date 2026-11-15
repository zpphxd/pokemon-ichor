"""gTileset_Steppe: the open land of the steppe family.

Thrace's Bistonian Plain and Diomedes's shore, the Thermodon Road, and, for
the Oikoumene, Scythia: the Steppe Road, Lake Maeotis and the Arimaspian
Heights. An ocean of grass under a huge sky, burial mounds and stone idols,
river banks and reed marsh, gold in the rock.

  ground   long golden grass and silver feather-grass (both encounter
           grass), dry turf and flowers, the dirt road and its joins onto
           aethos's limestone path, mudflats
  mounds   kurgans in two sizes (a dig-spot mound, a grave entrance), stone
           baba idols and the great waystone idol, race markers
  water    rivers and lakes with soft banks, reeds and reed marsh, fords
  land     willows and poplars by the water, a lone oak, horse-field fences,
           troughs and hay
  heights  the Arimaspian Heights: rock faces with gold veins, mine heads,
           fossil beds with mismatched bones
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
import farlands_ground as G
from farlands_lib import ground, put, struct

GROUPS = {
    # the long grasses, dry turf and flowers
    "gold": ["sg0", "sg1", "sg2", "sg3", "sg4", "t1", "w1", "w0", "dt1", "dt2", "dt3", "pp", "th2",
             "cf", "gd"],
    # the dirt road, its joins onto aethos's path, mudflats, dug earth
    "earth": ["g1", "g2", "g3", "gd", "l0", "l1", "rd0", "rd3", "p1", "p2", "p3", "md0", "md1",
              "md2", "sg2"],
    # river and lake banks, reeds, fords
    "river": ["b2", "b3", "b4", "w0", "g1", "g2", "g3", "gd", "md0", "md1", "md2", "t0", "t1",
              "t3", "rb1"],
    # field stone: babas, the waystone, race markers
    "stone": ["g1", "g2", "g3", "gd", "sn0", "sn1", "sn2", "sn3", "w1", "w0", "lc", "ink", "t0",
              "sg2", "fr2"],
    # the kurgans' grassy skins and their kerbs
    "mound": ["g1", "g2", "g3", "gd", "t0", "t1", "sg1", "sg2", "sg3", "l0", "l1", "sn1", "sn2",
              "sn3", "md0"],
    # the Arimaspian heights
    "heights": ["hr0", "hr1", "hr2", "hr3", "hr4", "au1", "au2", "bn1", "bn2", "ink", "g1", "g2",
                "gd", "tb1", "tb2"],
    # trees, fences, troughs, hay
    "grove": ["wl1", "wl2", "wl3", "wl4", "k1", "k2", "k3", "t0", "g1", "gd", "tb1", "tb2", "tb3",
              "b3", "sg3"],
}

SEC_G, SEC_M, SEC_W, SEC_L, SEC_H = "ground", "mounds", "water", "land", "heights"
GRASS = 0x001


# --------------------------------------------------------------------------
# Ground
# --------------------------------------------------------------------------

def _gold_tex():
    """aethos's barley, pixel for pixel, ripened to straw gold: the tall-grass
    field effect is cut from the same shapes."""
    return G.recolor_tex(0x00D, {"t0": "sg0", "t1": "sg1", "gd": "sg2", "t3": "sg3", "tg": "sg4"})


def _feather_tex():
    """The barley's shapes again, bleached to straw with silver awns."""
    t = G.recolor_tex(0x00D, {"t0": "sg0", "t1": "sg1", "gd": "dt2", "t3": "dt3", "tg": "w1"})
    for (x, y) in ((0, 0), (8, 0), (12, 8), (4, 8)):
        t[((x + 1) % 16, (y - 1) % 16)] = "w1"
    return t


def steppe_grass():
    return G.blob_set(
        "steppe_grass", "Long golden steppe grass (encounters)", SEC_G,
        G.grass_overlay(_gold_tex(), "sg0", "sg2", "sg4"), on="grass", walk="G",
        notes="Thrace's long grass: knee-high golden tufts with dark green feet, all 47 soft-edge "
              "shapes over borrowed aethos grass (`farlands_lib.blob_key` gives a cell's key from a "
              "region mask). Every cell is `MB_TALL_GRASS`. Blade tips lean out over the meadow "
              "along the top edge. Use it for the forced bands and the optional fields of the "
              "Bistonian Plain and the Thermodon Road.")


def feather():
    """Feather-grass as variants of the golden grass's full interior: set them
    inside a `steppe_grass` region (its edges stay golden) for silver streaks."""
    names = {"feather": (0, 0), "feather_b": (1, 0)}
    s = struct("feather", "Silver feather-grass (encounters)", 2, 1, SEC_G, walk=["GG"], names=names,
               oik=True,
               notes="The Pontic steppe's feather-grass (Stipa): straw tufts bleached silver, long "
                     "awns catching the wind. Two full-interior cells, `MB_TALL_GRASS`, to use in "
                     "place of `steppe_grass` `1|11111111` anywhere inside a grass region (its soft "
                     "edges stay golden). For the Oikoumene's Scythia, fill whole fields with them; "
                     "on a Thracian map, set a streak of them for the wind.")
    ground(s, "grass")
    tex = _feather_tex()
    for i in range(2):
        for y in range(16):
            for x in range(16):
                s.M.px(i * 16 + x, y, tex[((x + 8 * i) % 16, (y + 8 * i) % 16)] if i == 0 else
                       tex[((x + 4) % 16, y)])
    return s


def _road_px(X, Y):
    k = F.hp(X, Y, 17)
    c = "l1"
    if k % 7 == 0:
        c = "rd3"
    elif k % 11 == 0:
        c = "l0"
    # small pebbles: a lit pixel over a shadow
    x, y = X % 16, Y % 16
    for (px, py) in ((3, 4), (11, 2), (13, 11), (6, 13), (8, 8)):
        if (x, y) == (px, py):
            c = "p2"
        elif (x, y) == (px, py + 1):
            c = "l0"
    # hoof-prints: little dark crescents
    for (px, py) in ((2, 9), (9, 5), (14, 14)):
        if (x, y) in ((px, py), (px + 1, py), (px - 1, py + 1)):
            c = "rd0" if (x, y) == (px - 1, py + 1) else "l0"
    return c


def road():
    return G.blob_set(
        "road", "Dirt road (and worn track)", SEC_G,
        G.earth_overlay(_road_px, "l0", None, seed=2.3, ring_rate=2, lit_c="rd3"),
        on="grass", walk=".",
        notes="Thrace's roads are beaten earth: hoof-prints, pebbles, a darker lip where the grass "
              "gives way. 47 soft-edge shapes over borrowed aethos grass; a region one cell wide "
              "reads as a worn track, two or three wide as a cart road. Lay roads as regions that "
              "bend diagonally in steps, and the soft corners make the curve. Walkable. Where a road "
              "crosses into a seam strip it must become aethos's limestone path: use `road_join`.")


def _road_base(L, ox, oy):
    L.texture(GRASS, ox, oy, 16, 16)


def road_join(road_struct):
    paint = G.earth_overlay(_road_px, "l0", None, seed=2.3, ring_rate=2, lit_c="rd3")
    return G.join_set(
        "road_join", "The road meets aethos's limestone path", SEC_G, paint, _road_base, "l1",
        notes="Where the dirt road becomes aethos's limestone path, so a road can run into a seam "
              "strip (MAP_DESIGN 5) or into a town's paving. Named `<side>_<cell>`, side being "
              "where the aethos path lies: `S_L` `S_C` `S_R` are the left, middle and right cells "
              "of a north-south road with the path to the south (below them put aethos `1D8` `1D9` "
              "`1DA`); `N_*` the same with the path to the north; `E_T` `E_C` `E_B` the top, middle "
              "and bottom cells of an east-west road with the path to the east (beside them put "
              "aethos `1D1` (top) `1D9` `1E1` (bottom)); `W_*` the same to the west. A two-wide road "
              "uses only `_L` `_R` (or `_T` `_B`). Walkable.")


def _turf_tex():
    t = {}
    for y in range(16):
        for x in range(16):
            k = F.hp(x, y, 23)
            t[(x, y)] = "dt2" if k % 5 else ("dt1" if k % 2 else "dt3")
    for (px, py) in ((2, 3), (9, 1), (13, 7), (5, 10), (11, 13), (1, 14)):
        put_v(t, px, py, "dt1", "dt3")
    return t


def put_v(t, x, y, dark, light):
    """A little 'v' tuft (as aethos's grass draws them)."""
    t[(x % 16, y % 16)] = dark
    t[((x + 2) % 16, y % 16)] = dark
    t[((x + 1) % 16, (y + 1) % 16)] = dark
    t[((x + 1) % 16, y % 16)] = light


def decor():
    """Single cells on borrowed grass: dry turf, tussocks, flowers."""
    names = {"turf": (0, 0), "tussock": (2, 0), "tussocks": (3, 0),
             "poppies": (4, 0), "salvia": (6, 0), "plumes": (7, 0)}
    s = struct("decor", "Dry turf, tussocks and steppe flowers", 8, 1, SEC_G, walk=["........"],
               names=names, oik=False,
               notes="On borrowed aethos grass, walkable, to scatter through the meadow so it isn't one "
                     "flat green: `turf`, a patch of grazed dry turf (the steppe's short grass); "
                     "`tussock` and `tussocks`, clumps of last year's straw; `poppies` and `salvia` "
                     "(violet sage), the steppe's flowers in early summer; `plumes`, a few "
                     "feather-grass awns standing out of the meadow. None has encounters.")
    ground(s, "grass")
    M = s.M
    tt = _turf_tex()
    for i, seed in ((0, 1.7), (1, 5.3)):
        vis = G.soft_mask("1|00000000", margin=1.0, radius=4.0, amp=1.8, seed=seed)
        for y, x in np.argwhere(vis):
            M.px(i * 16 + x, y, tt[(x, y)])
        for y, x in np.argwhere(G.ring(vis)):
            if (x + y) % 2:
                M.px(i * 16 + x, y, "dt1")
    # tussocks: tufts of last year's straw, blades fanning from a dark foot
    def tussock(ox, cx, cy, r):
        blades = [(-r, 0.55), (-r * 0.6, 0.85), (-r * 0.25, 1.0), (0.1, 0.95), (r * 0.4, 0.9),
                  (r * 0.75, 0.7), (r, 0.45)]
        for (dx, hgt) in blades:
            ht = r * 1.3 * hgt
            n = int(ht) + 1
            for j in range(n + 1):
                u = j / n
                x = int(round(cx + dx * u * (0.6 + 0.4 * u)))
                y = int(round(cy - ht * u))
                c = "sg1" if u < 0.3 else ("sg2" if u < 0.65 else ("sg3" if dx < 0.5 else "sg2"))
                if j == n:
                    c = "sg4" if dx < 0 else "sg3"
                M.px(ox + x, y, c)
        for dx in range(-int(r * 0.6), int(r * 0.6) + 1):
            M.px(ox + int(cx) + dx, int(cy) + 1, "gd")
        M.px(ox + int(cx), int(cy), "sg0")
        M.px(ox + int(cx) - 1, int(cy), "t1")
    # flowers: tiny heads on green stalks, scattered
    def flowers(ox, head, centre, pts):
        for (x, y) in pts:
            M.px(ox + x, y + 1, "gd")
            M.px(ox + x, y, head)
            if centre:
                M.px(ox + x + 1, y, head)
                M.px(ox + x, y - 1, head)
    flowers(64, "pp", False, [(2, 3), (7, 2), (12, 5), (4, 9), (10, 10), (14, 12), (6, 13)])
    for (x, y) in [(2, 3), (7, 2), (12, 5), (4, 9), (10, 10), (14, 12), (6, 13)]:
        M.px(64 + x + 1, y, "pp")
        M.px(64 + x, y - 1, "sg0") if (x + y) % 3 == 0 else None
    flowers(80, "cf", False, [(3, 4), (9, 3), (13, 8), (5, 11), (11, 13)])
    for (x, y) in [(3, 4), (9, 3), (13, 8), (5, 11), (11, 13)]:
        M.px(80 + x + 1, y, "cf")
        M.px(80 + x, y - 1, "cf")
    for (x, y) in [(3, 5), (10, 4), (7, 10), (13, 12)]:
        for j in range(4):
            M.px(96 + x, y + j, "th2" if j < 3 else "gd")
        M.px(96 + x - 1, y + 1, "th2")
        M.px(96 + x + 1, y + 2, "th2")
    for (x, y) in [(4, 12), (10, 10), (13, 14)]:
        for j in range(6):
            M.px(112 + x - (j // 3), y - j, "dt3" if j < 3 else "w0")
        M.px(112 + x - 3, y - 6, "w1")
        M.px(112 + x, y + 1, "gd")
    return F.pick(s, ["turf", "tussock", "tussocks", "poppies", "salvia", "plumes"])


MUD_SEEDS = [(2, 3), (9, 1), (14, 6), (6, 9), (12, 13), (3, 14), (8, 5), (0, 9)]


def _mud_px(X, Y):
    """Drying mud: plates split by a net of cracks (a 16 px periodic Voronoi),
    a puddle glint here and there."""
    x, y = X % 16, Y % 16
    ds = []
    for (sx, sy) in MUD_SEEDS:
        best = min(math.hypot(x - sx - dx, y - sy - dy) for dx in (-16, 0, 16) for dy in (-16, 0, 16))
        ds.append(best)
    ds.sort()
    if ds[1] - ds[0] < 1.0:
        return "md0" if F.hp(x, y, 5) % 3 == 0 else "md1"
    if ds[1] - ds[0] < 1.8 and F.hp(x, y, 7) % 2:
        return "md1"
    if (x, y) in ((9, 3), (10, 3), (2, 12), (14, 7)):
        return "b4" if (x + y) % 2 else "b3"
    return "md2"


def mudflat():
    return G.blob_set(
        "mudflat", "Mudflats", SEC_W,
        G.earth_overlay(_mud_px, "md1", None, seed=6.1, lit_c="g3"),
        on="grass", walk="M", oik=True,
        notes="Lake Maeotis's shore: cracked grey-brown mud with standing water in the hoof-holes, "
              "47 soft-edge shapes over borrowed grass, walkable (`MB_PUDDLE`, so feet splash). Lay "
              "it between the meadow and the water's edge (`river` banks are muddy too).")


def river():
    paint = G.water_painter(lambda X, Y: F.grass_px(X, Y), ("md1", "md2", "g3"), "b2", "b4")
    return G.blob_set(
        "river", "Rivers and lakes, with soft banks", SEC_W, paint, on="sea", walk="P",
        notes="Fresh water (`MB_POND_WATER`, surfable; fish here) over borrowed aethos sea, so it "
              "moves. The 47 soft-edge shapes are of the water: an edge cell draws the grassy "
              "bank over the land side, aethos grass pixel for pixel, with a muddy lip, a pale "
              "fringe of shallows and a ripple line, and now and then a few reeds. The Thermodon, "
              "the Nestos, the Borysthenes, Lake Maeotis. One cell wide is a brook.")


# --------------------------------------------------------------------------
# Reeds and fords
# --------------------------------------------------------------------------

def _reed_tex():
    """aethos's reeds (0x015), pixel for pixel, with cattail heads."""
    t = G.recolor_tex(0x015, {})
    for (x, y) in ((2, 0), (10, 0), (6, 8), (14, 8)):
        t[(x, y)] = "rb1"
        t[(x, (y + 1) % 16)] = "rb1"
    return t


def _reed_tex_old():
    t = {}
    for y in range(16):
        for x in range(16):
            t[(x, y)] = "rg1" if F.hp(x, y, 41) % 3 else "md1"
    for i, bx in enumerate((1, 4, 6, 9, 12, 14)):
        for row in (0, 8):
            by = row + 7 + (i % 2)
            ht = 6 + (i + row) % 3
            for j in range(ht + 1):
                u = j / ht
                c = "rg1" if u < 0.25 else ("rg2" if u < 0.7 else "rg3")
                if bx % 3 == 0 and u > 0.5:
                    c = "rg2"
                t[(bx % 16, (by - j) % 16)] = c
            if (i + row) % 3 == 0:
                t[(bx % 16, (by - ht) % 16)] = "rb1"
                t[(bx % 16, (by - ht + 1) % 16)] = "rb1"
    return t


def reed_marsh():
    tex = _reed_tex()
    return G.blob_set(
        "reed_marsh", "Reed marsh (encounters)", SEC_W,
        G.grass_overlay(tex, "t0", "t1", "t3", margin=1.0, radius=4.5, amp=2.2, seed=8.3),
        on="grass", walk="L", oik=True,
        notes="A bed of reeds and cattails taller than you, 47 soft-edge shapes over borrowed grass. "
              "`MB_LONG_GRASS`: wild encounters, and the reeds part round you. For Lake Maeotis's "
              "marsh and the Thermodon's backwaters.")


def reeds_ford():
    names = {"reeds_water": (0, 0), "reeds_water_b": (1, 0), "reeds_bank": (2, 0),
             "ford": (3, 0), "ford_stones": (4, 0), "stones": (5, 0)}
    s = struct("reeds_ford", "Reeds in the water, fords and stepping stones", 6, 1, SEC_W,
               walk=["XX.HH."], names=names,
               notes="`reeds_water` and `reeds_water_b`: a clump of reeds standing in the river "
                     "(borrowed sea; impassable, surf round it). `reeds_bank`: reeds on dry ground "
                     "(borrowed grass; impassable). `ford`: a gravel bar under a skin of water, "
                     "walkable (`MB_SHALLOW_WATER`): lay a line of them across a river, inside the "
                     "water region, to make a ford; `ford_stones` is the same with stepping stones. "
                     "`stones`: three flat stones in the grass by a ford (walkable).")
    ground(s, "sea", [(0, 0), (1, 0)])
    ground(s, "grass", [(2, 0), (5, 0)])
    M, B = s.M, s.B
    cols = ("t0", "t1", "t3", "rb1")
    for (cx, pts) in ((0, [(4, 13), (8, 11), (12, 14), (6, 7)]), (1, [(3, 9), (9, 14), (12, 8)])):
        for (x, y) in pts:
            G.reed_clump(M, cx * 16 + x, y, cols)
            for dx in (-2, -1, 0, 1, 2):
                M.px(cx * 16 + x + dx, y + 1, "b4" if (dx + y) % 2 else "b3")
    for (x, y) in [(3, 13), (9, 14), (13, 10), (6, 8)]:
        G.reed_clump(M, 32 + x, y, cols)
        M.px(32 + x - 1, y + 1, "gd")
        M.px(32 + x, y + 1, "gd")
    # the ford: gravel seen through clear water, the current's ripples
    for i in (3, 4):
        for y in range(16):
            for x in range(16):
                k = F.hp(x, y, 51)
                c = "b3"
                if k % 5 == 0:
                    c = "md2"
                elif k % 7 == 0:
                    c = "b4"
                B.px(i * 16 + x, y, c)
        for (ry, ph) in ((3, 0), (10, 5)):
            for x in range(16):
                if (x + ph) % 8 < 4:
                    B.px(i * 16 + x, ry + ((x + ph) % 8 == 2), "w0" if (x + ph) % 8 == 1 else "b4")
    for (x, y, r) in ((4, 5, 2.6), (11, 9, 3.0), (5, 13, 2.2)):
        for yy in range(16):
            for xx in range(16):
                d = math.hypot(xx - x, (yy - y) * 1.3)
                if d < r:
                    B.px(64 + xx, yy, "md2" if yy < y else "md1")
                elif d < r + 1 and yy >= y:
                    B.px(64 + xx, yy, "md0")
                elif d < r + 1.6 and yy >= y and (xx + yy) % 2:
                    B.px(64 + xx, yy, "w0")
    for (x, y) in ((3, 4), (10, 7), (6, 12)):
        put(M, 80 + x - 2, y - 1, [".aaa.", "abbbm", ".mmm."], {"a": "g3", "b": "md2", "m": "md1"})
    return s


# --------------------------------------------------------------------------
# Kurgans
# --------------------------------------------------------------------------

def _dome(L, ox, oy, w, h_, cx, cy, rx, ry, seed=0, tufts=True):
    """A grassy burial mound lit from the top left, over aethos grass pixels:
    draws the whole box (grass outside the mound), so it fills a bottom layer."""
    for y in range(h_):
        for x in range(w):
            L.px(ox + x, oy + y, F.grass_px(ox + x, oy + y))
    m = F.blob(cx, cy, rx, ry, w, h_, wobble=0.03, k=7, seed=seed)
    # the mound's shadow on the meadow, bottom right
    sh = F.blob(cx + 3, cy + 3, rx, ry, w, h_, wobble=0.03, k=7, seed=seed)
    for y, x in np.argwhere(sh & ~m):
        L.px(ox + x, oy + y, "gd" if (x + y) % 2 == 0 else "g1")
    ramp = ["t1", "gd", "g1", "g2", "g3"]
    for y, x in np.argwhere(m):
        u = (x - cx) / rx
        v = (y - cy) / ry
        # a dome's normal, lit from the top left
        z = max(0.0, 1 - u * u - v * v) ** 0.5
        lit = (-0.55 * u - 0.6 * v + 0.6 * z)
        i = 4 if lit > 0.62 else (3 if lit > 0.35 else (2 if lit > 0.05 else (1 if lit > -0.25 else 0)))
        k = F.h(x, y, 13 + seed)
        if k % 6 == 0:
            i = max(0, i - 1)
        L.px(ox + x, oy + y, ramp[i])
    if tufts:
        # dry tufts on the dome, catching the sun
        for y, x in np.argwhere(m):
            if F.h(x, y, 77 + seed) % 23 == 0 and m[max(0, y - 2), x]:
                L.px(ox + x, oy + y, "sg2")
                L.px(ox + x, oy + y - 1, "sg3")
                L.px(ox + x + 1, oy + y, "sg1")
    for y, x in np.argwhere(F.edge_of(m)):
        if y > cy:
            L.px(ox + x, oy + y, "t1")
    return m


def _kerb(L, ox, oy, m, cx, cy, rx, ry, step=5, start=0.15):
    """Grey kerb stones half-buried round the foot of a mound (lower half)."""
    for i in range(0, 64):
        a = math.pi * (start + (1 - 2 * start) * i / 63)
        x = cx + rx * 0.98 * math.cos(a)
        y = cy + ry * 0.92 * math.sin(a)
        if i % step:
            continue
        X, Y = int(round(x)), int(round(y))
        put(L, ox + X - 2, oy + Y - 1, [".33.", "3221", "2110"],
            {"3": "sn3", "2": "sn2", "1": "sn1", "0": "sn0"})


def kurgans():
    names = {"small_TL": (0, 0), "small_TR": (1, 0), "small_BL": (0, 1), "small_BR": (1, 1),
             "dig": (2, 0), "dug": (3, 0), "low": (2, 1), "low_b": (3, 1)}
    s = struct("kurgan", "Kurgans: a small mound, a dig-spot mound", 4, 2, SEC_M,
               walk=["XXXX", "XXXX"], names=names, oik=True,
               notes="Burial mounds of the horse-lords, grassy domes ringed with half-buried kerb "
                     "stones. `small` is 2 x 2 (its cells `small_TL` `small_TR` / `small_BL` "
                     "`small_BR`), impassable. `low` and `low_b` are low barrows one cell across, for "
                     "a line of them along a ridge. `dig` is a low mound with fresh cracks in its turf: "
                     "a dig spot (`EventScript_IchorDigSpot` on it); swap it for `dug`, the opened pit, "
                     "once dug. All drawn whole (grass round them is aethos's own pixels).")
    B, M = s.B, s.M
    m = _dome(B, 0, 0, 32, 32, 15.5, 18, 14.5, 10.5, seed=1)
    _kerb(M, 0, 0, m, 15.5, 18, 14.5, 10.5, step=6)
    # dig spot: a low hump split by cracks of bare earth
    m2 = _dome(B, 32, 0, 16, 16, 7.5, 9, 7, 5, seed=2, tufts=False)
    for (x, y) in ((5, 7), (6, 8), (7, 8), (8, 9), (9, 9), (10, 10), (7, 10), (6, 11)):
        M.px(32 + x, y, "l0")
        M.px(32 + x, y - 1, "l1")
    # dug: an opened pit with its spoil
    _dome(B, 48, 0, 16, 16, 7.5, 9, 7, 5, seed=2, tufts=False)
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 7.5) / 5.0, (y - 9) / 3.6)
            if d < 1:
                M.px(48 + x, y, "md0" if d < 0.6 else ("rd0" if y > 9 else "l0"))
            elif d < 1.3 and y < 9:
                M.px(48 + x, y, "l1" if (x + y) % 2 else "rd3")
    for (x, y) in ((1, 12), (2, 13), (13, 13), (14, 12), (12, 14)):
        M.px(48 + x, y, "l1")
    # low barrows
    for i, seed in ((2, 5), (3, 6)):
        mm = _dome(B, i * 16, 16, 16, 16, 7.5, 9.5, 7.2, 5.5, seed=seed)
        _kerb(M, i * 16, 16, mm, 7.5, 9.5, 7.2, 5.5, step=9)
    return s


def kurgan_large():
    names = {f"c{x}{y}": (x, y) for y in range(3) for x in range(4)}
    names.update({"door": (1, 3), "summit_idol": (2, 3)})
    s = struct("kurgan_large", "The great kurgan, with a grave door and a summit idol", 4, 4, SEC_M,
               walk=["XXXX", "XXXX", "XXXX", "XDXX"], names=names, oik=True,
               notes="A royal barrow, 4 x 3 (`c00` to `c32`, column then row), impassable: a broad "
                     "dome lit from the west, dry tufts on its flanks, kerb stones round its foot. "
                     "Two swaps: `door` replaces `c12` (the bottom row's second cell) with the grave "
                     "entrance, a passage lined with upright slabs (`MB_NON_ANIMATED_DOOR`: warp to the "
                     "barrow's chamber; the Oikoumene's barrow-keeper, Spiritomb's lair); "
                     "`summit_idol` replaces `c10` (the top row's second cell) with a stone baba "
                     "standing on the crown. The extra row's last two cells are fillers.")
    B, M = s.B, s.M
    m = _dome(B, 0, 0, 64, 48, 31.5, 30, 30.5, 18.0, seed=3)
    _kerb(M, 0, 0, m, 31.5, 30, 30.5, 18.0, step=4, start=0.08)
    # the door: a copy of c12 with the passage cut into it
    B.a[48:64, 16:32] = B.a[32:48, 16:32]
    M.a[48:64, 16:32] = M.a[32:48, 16:32]
    put(M, 16 + 2, 48 + 1, [
        "..00000000..",
        ".0322222210.",
        "032000000210",
        "03200..00210",
        "0320....0210",
        "0320....0210",
        "0320....0210",
        "0320....0210",
        "0320....0210",
        "0320....0210",
        "032000000210",
        "0211111111100",
    ], {"0": "sn0", "1": "sn1", "2": "sn2", "3": "sn3"})
    for y in range(52, 62):
        for x in range(22, 26):
            M.px(x, y, "ink" if y > 54 else "sn0")
    # the summit idol: a copy of c10 with a baba on the crown
    B.a[48:64, 32:48] = B.a[0:16, 16:32]
    M.a[48:64, 32:48] = M.a[0:16, 16:32]
    _baba_small(M, 32 + 9, 48 + 1)
    # filler
    B.a[48:64, 0:16] = B.a[32:48, 0:16]
    M.a[48:64, 0:16] = M.a[32:48, 0:16]
    B.a[48:64, 48:64] = B.a[32:48, 48:64]
    M.a[48:64, 48:64] = M.a[32:48, 48:64]
    F.set_walk(s, ["XXXX", "XXXX", "XXXX", "XDXX"])
    return s


def _baba_small(L, ox, oy):
    put(L, ox, oy, [
        ".0000.",
        "033210",
        "031310",
        "032210",
        ".0220.",
        "032210",
        "033110",
        "0r3r10",
        "032210",
        "032210",
        "033210",
        "032110",
        "0000000",
    ], {"0": "sn0", "1": "sn1", "2": "sn2", "3": "sn3", "r": "sn0"})


# --------------------------------------------------------------------------
# Stone idols and markers
# --------------------------------------------------------------------------

BABA = {
    # a man with a drinking horn held at his belly
    "horn": [
        "....00000...",
        "...0333220..",
        "..033333210.",
        "..0300302010",
        "..032333210.",
        "..0300000210",
        "...0322210..",
        "..033322210.",
        ".03333222110",
        ".03023221010",
        ".0302wwww010",
        ".0322w22w210",
        ".03222ww2210",
        ".03322222110",
        ".03322222110",
        ".03332222110",
        ".03322221110",
        ".03322221110",
        ".03322221110",
        ".03332222110",
        ".03322221110",
        "..033222110.",
        "..033222110.",
        ".00000000000",
    ],
    # a woman, hands folded on her belly, a tall headdress
    "woman": [
        "...000000...",
        "...033220...",
        "..03333210..",
        "..03333210..",
        "..03003010..",
        "..03323210..",
        "..03200210..",
        "...032220...",
        "..03333220..",
        ".0333332210.",
        ".0332222110.",
        ".0303333010.",
        ".0302222010.",
        ".0333222110.",
        ".0332222110.",
        ".0332222110.",
        ".0333222110.",
        ".0332222110.",
        ".0332222110.",
        ".0332222110.",
        "..03322110..",
        "..03322110..",
        "..03322110..",
        ".0000000000.",
    ],
}


def _figure(L, ox, oy, rows, lichen=0, lean=0):
    legend = {"0": "sn0", "1": "sn1", "2": "sn2", "3": "sn3", "w": "w1"}
    for j, row in enumerate(rows):
        dx = (lean * (len(rows) - j)) // len(rows) if lean else 0
        for i, ch in enumerate(row):
            if ch in legend:
                c = legend[ch]
                if lichen and ch in "23" and F.h(i, j, lichen) % 7 == 0:
                    c = "lc"
                L.px(ox + i + dx, oy + j, c)


def idols():
    names = {"horn_top": (0, 0), "horn": (0, 1), "woman_top": (1, 0), "woman": (1, 1),
             "worn_top": (2, 0), "worn": (2, 1), "marker_top": (3, 0), "marker": (3, 1),
             "cairn": (4, 1), "cairn_top": (4, 0)}
    s = struct("idols", "Stone babas, race markers, a cairn", 5, 2, SEC_M,
               walk=["TTTT.", "XXXXX"], names=names, oik=True,
               notes="Stone idols (`baba`) on borrowed grass, each 1 x 2: the top cell (`*_top`) is "
                     "drawn over the player, the bottom one impassable (put a bg event here: they "
                     "stand on kurgans and at fords, and travellers leave them a cup of milk). "
                     "`horn`: a man holding a drinking horn at his belly; `woman`: hands folded, a "
                     "tall headdress; `worn`: weathered faceless and leaning, crusted with lichen. "
                     "`marker` (with `marker_top`): a race marker, a stone post banded in red ochre, "
                     "for the Wagon Camp's races and the steppe's boundary lines. `cairn`: a heap of "
                     "stones with a red rag tied to a stick, the turning post of a race course "
                     "(`cairn_top` is plain grass to go above it).")
    ground(s, "grass")
    M = s.M
    for i, (k, lich, lean) in enumerate((("horn", 0, 0), ("woman", 0, 0), ("horn", 29, 2))):
        rows = BABA[k]
        ox = i * 16 + 2
        oy = 32 - len(rows) - 1
        if i == 2:
            rows = [r.replace("w", "2").replace("00302", "02302") for r in rows]
        _figure(M, ox, oy, rows, lichen=lich, lean=lean)
        # shadow on the grass
        for x in range(ox + 3, ox + 13):
            M.px(x, 31, "gd") if M.get(x, 31) is None else None
            M.px(x + 1, 30, "gd") if M.get(x + 1, 30) is None else None
    # race marker: a squared post banded with red ochre
    for y in range(6, 31):
        for x in range(52, 59):
            c = "sn3" if x == 52 else ("sn1" if x >= 57 else "sn2")
            if 10 <= y <= 13 or 20 <= y <= 23:
                c = "fr2" if x < 57 else "sn1"
            if F.h(x, y, 3) % 11 == 0 and c == "sn2":
                c = "sn1"
            M.px(x, y, c)
        M.px(51, y, "sn0")
        M.px(59, y, "sn0")
    for x in range(51, 60):
        M.px(x, 5, "sn0")
        M.px(x, 31, "sn0")
    for x in range(56, 62):
        M.px(x, 30, "gd")
    # the cairn
    for (x, y, r) in ((70, 26, 4.5), (75, 27, 4.0), (72, 22, 4.0), (67, 28, 3.0), (77, 23, 2.5)):
        for yy in range(16, 32):
            for xx in range(64, 80):
                d = math.hypot(xx - x, (yy - y) * 1.2)
                if d < r:
                    u = (xx - x) + (yy - y)
                    M.px(xx, yy, "sn3" if u < -2 else ("sn2" if u < 2 else "sn1"))
                elif d < r + 0.8 and M.get(xx, yy) is None:
                    M.px(xx, yy, "sn0")
    for y in range(17, 24):
        M.px(72, y, "sn0")
    for (x, y) in ((73, 17), (74, 18), (75, 18), (73, 18), (76, 19)):
        M.px(x, y, "fr2")
    return s


def waystone():
    names = {f"c{x}{y}": (x, y) for y in range(3) for x in range(2)}
    s = struct("waystone", "The great idol: a route's waystone", 2, 3, SEC_M,
               walk=["TT", "XX", "XX"], names=names, oik=True,
               notes="A great stone idol twice a man's height, four-square, with a pointed cap, a "
                     "drinking horn and a short sword at its belt, on a plinth cut with the roads it "
                     "watches; red ribbons and a heap of offering-stones at its foot. 2 x 3 on "
                     "borrowed grass: the top row is drawn over the player, the rest impassable. Put "
                     "the route sign's bg event on its plinth (`c01` or `c11`, bottom row is `c02` "
                     "`c12`).")
    ground(s, "grass")
    M = s.M
    rows = [
        "......0000......",
        ".....033200.....",
        "....03333210....",
        "...0333332210...",
        "...0000000000...",
        "...0333322210...",
        "...0300230010...",
        "...0333322210...",
        "...0322002210...",
        "...0320000210...",
        "....03222210....",
        "...033322221....",
        "..03333222211...",
        "..03023322101...",
        "..03023wwww01...",
        "..030232w2w01...",
        "..03322www2110..",
        "..03322222211...",
        "..000000000000..",
        "..03r3r3r3r3r1..",
        "..000000000000..",
        "..03322222211...",
        "..03322201211...",
        "..03322201211...",
        "..03322201211...",
        "..03322202211...",
        "..03322222211...",
        "..03332222111...",
        "..03322222111...",
        "..03322222111...",
        "..03322222111...",
        "..03332222111...",
        "..03322222111...",
        ".0000000000000..",
        ".0333333222211..",
        ".0322222222110..",
        ".0320303022110..",
        ".0322232222110..",
        ".0303022322110..",
        ".0322222222110..",
        ".00000000000000.",
    ]
    _figure(M, 0, 47 - len(rows), [r.replace("r", "2") for r in rows])
    # red ochre on the belt
    for x in range(5, 12, 2):
        M.px(x, 47 - len(rows) + 19, "fr2")
    # offerings: stones and ribbons at the foot
    for (x, y) in ((1, 43), (3, 45), (14, 44), (16, 45), (19, 43), (12, 46), (21, 45)):
        put(M, x, y, ["32", "21"], {"3": "sn3", "2": "sn2", "1": "sn1"})
    for (x, y) in ((17, 36), (18, 37), (18, 38), (19, 39), (2, 30), (1, 31), (1, 32)):
        M.px(x, y, "fr2")
    for x in range(3, 18):
        if M.get(x, 47) is None:
            M.px(x, 47, "gd")
    return s


# --------------------------------------------------------------------------
# Trees, fences, troughs, hay
# --------------------------------------------------------------------------

WILLOW = ("wl1", "wl2", "wl3", "wl4")


def trees():
    names = {"willow_TL": (0, 0), "willow_TR": (1, 0), "willow_BL": (0, 1), "willow_BR": (1, 1),
             "poplar_top": (2, 0), "poplar": (2, 1),
             "oak_TL": (3, 0), "oak_TR": (4, 0), "oak_BL": (3, 1), "oak_BR": (4, 1)}
    s = struct("trees", "Willow, poplar and a lone oak", 5, 2, SEC_L, walk=["TTTTT", "XXXXX"],
               names=names,
               notes="On borrowed grass; each tree's top row is drawn over the player, its bottom row "
                     "impassable. `willow` (2 x 2): a white willow on a river bank, its fronds hanging "
                     "to the grass. `poplar` (1 x 2, with `poplar_top`): a black poplar, tall and "
                     "narrow; plant them in lines along a river. `oak` (2 x 2): a lone wind-bent oak, "
                     "the only shade for a day's ride; set a rest point under it.")
    ground(s, "grass")
    M, T = s.M, s.T

    def place(mask, ox, oy, split=16):
        tmp = F.Layer(s.w * 16, s.h * 16)
        F.foliage(tmp, mask, WILLOW, seed=ox, outline="t0", clump=3.5)
        for y, x in np.argwhere(mask):
            c = tmp.get(int(x), int(y))
            if c:
                (T if y < split else M).px(int(x), int(y), c)

    def trunk(x0, y0, y1, w=3):
        for y in range(y0, y1):
            for i in range(w):
                c = "k3" if i == 0 else ("k2" if i < w - 1 else "k1")
                M.px(x0 + i, y, c)
        for x in range(x0 - 3, x0 + w + 5):
            if M.get(x, y1) is None:
                M.px(x, y1, "gd")
            if M.get(x + 1, y1 + 1) is None and x % 2:
                M.px(x + 1, y1 + 1, "gd")

    W, H = s.w * 16, s.h * 16
    # willow: a round crown with fronds hanging down
    trunk(14, 18, 28, 4)
    crown = F.mask_from(lambda x, y: math.hypot((x - 16) / 14.5, (y - 12) / 10.5) < 1
                        + 0.06 * math.sin(math.atan2(y - 12, x - 16) * 7), W, H)
    for fx in range(4, 29, 3):
        ln = 8 + (fx * 7) % 5
        for y in range(12, 12 + ln):
            if 0 <= y < H and math.hypot((fx - 16) / 14.5, 0) < 1:
                crown[y, fx] = True
                if fx % 2:
                    crown[y, fx + 1] = True
    place(crown, 0, 0)
    for fx in range(4, 29, 3):
        y = 12 + 8 + (fx * 7) % 5
        if y < 32:
            M.px(fx, y, "wl4") if M.get(fx, y) else None
    # poplar: a tall column
    trunk(39, 26, 30, 2)
    col = F.mask_from(lambda x, y: abs(x - 40) < 6.2 * math.sin(math.pi * min(1, max(0, (y - 1) / 27.0))) ** 0.7
                      and 1 <= y <= 28, W, H)
    place(col, 32, 0)
    # oak: a broad crown pushed east by the wind
    trunk(60, 19, 29, 4)
    for (x, y) in ((63, 21), (64, 20), (65, 19)):
        M.px(x, y, "k2")
    oak = F.mask_from(lambda x, y: math.hypot((x - 66) / 15, (y - 11) / 10) < 1
                      + 0.09 * math.sin(math.atan2(y - 11, x - 66) * 5 + 1), W, H)
    place(oak, 48, 0)
    return s


def fence():
    from farlands_kits import FENCE_NOTES, fence_kit
    return fence_kit("fence", "Horse-field fence", SEC_L, ("k1", "tb1", "tb2", "tb3"), "gd",
                     notes=FENCE_NOTES + " For horse fields on the plain and the Thermodon road.")


def troughs():
    names = {"trough_L": (0, 0), "trough_R": (1, 0), "hay": (2, 0), "hay_TL": (3, 0)}
    s = struct("troughs", "A trough and hay", 3, 1, SEC_L, walk=["XXX"],
               names={"trough_L": (0, 0), "trough_R": (1, 0), "hay": (2, 0)},
               notes="On borrowed grass, impassable: `trough_L` `trough_R`, a hollowed-log water "
                     "trough two cells long; `hay`, a stack of hay on a pole, eaten at the bottom.")
    ground(s, "grass")
    M = s.M
    for y in range(5, 13):
        for x in range(2, 30):
            if y in (5, 12) or x in (2, 29):
                c = "k1"
            elif y == 6:
                c = "tb3"
            elif y < 9:
                c = "b3" if (x + y) % 5 else "wl4"
            else:
                c = "tb2" if y < 11 else "tb1"
            M.px(x, y, c)
    for x in range(3, 31):
        M.px(x, 13, "gd")
    for x in (4, 27):
        for y in range(12, 15):
            M.px(x, y, "k1")
    # hay
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 7.5) / 6.5, (y - 8) / 7.5)
            if d < 1 and y < 14:
                u = (x - 7.5) + (y - 8)
                c = "sg3"
                if u > 3:
                    c = "tb2"
                if u > 7:
                    c = "tb1"
                if F.h(x, y, 5) % 5 == 0:
                    c = "tb3"
                M.px(32 + x, y, c)
    for y in range(0, 3):
        M.px(32 + 7, y, "tb1")
    for x in range(34, 47):
        M.px(x, 14, "gd")
    s.names = {"trough_L": (0, 0), "trough_R": (1, 0), "hay": (2, 0)}
    return s


# --------------------------------------------------------------------------
# The Arimaspian Heights
# --------------------------------------------------------------------------

HR = ("hr0", "hr1", "hr2", "hr3", "hr4")


def heights():
    import farlands_kits as K

    def gold(s, M, ox, oy):
        for y in range(16):
            for x in range(16):
                M.px(ox + x, oy + y, K.rock_px(ox + x, oy + y, HR, 0, 3, vein=("au1", "au2")))

    def gold_b(s, M, ox, oy):
        for y in range(16):
            for x in range(16):
                M.px(ox + x, oy + y, K.rock_px(ox + x + 7, oy + y + 5, HR, 0, 5, vein=("au1", "au2")))

    def mine(s, M, ox, oy):
        K.adit(M, ox, oy, ("tb1", "tb1", "tb2"), ("hr0", "ink"), "hr4", spoil="hr2")

    def cave(s, M, ox, oy):
        K.cave_mouth(M, ox, oy, ("hr0", "ink"), "hr1")

    s = K.cliff_kit("heights", "The Arimaspian heights: rock faces", SEC_H, HR, "hr0", "gd",
                    notes=K.CLIFF_NOTES + " Extra faces: `face_gold` and `face_gold_b`, the face "
                    "threaded with veins of gold the one-eyed Arimaspians dig (Herodotus 3.116); "
                    "`mine`, a timber-framed mine head; `cave`, a natural cave mouth. Both are "
                    "`MB_NON_ANIMATED_DOOR` (put the warp there).",
                    oik=True, seed=2,
                    extra_faces=[("face_gold", gold), ("face_gold_b", gold_b), ("mine", mine),
                                 ("cave", cave)])
    F.set_walk(s, ["XXXX", "XXXX", "XXXX", "XXXX", "....", "XXDD"])
    return s


def fossils():
    names = {"bed": (0, 0), "skull": (1, 0), "jaw": (2, 0), "ribs": (3, 0)}
    s = struct("fossils", "Fossil beds of mismatched bones", 4, 1, SEC_H, walk=["XXXX"],
               names=names, oik=True,
               notes="On borrowed grass, impassable: shelves of pale rock weathering out of the "
                     "turf, where the 'gold-guardians' lie (Adrienne Mayor: griffin tales from "
                     "fossils). `bed`, bare rock; `skull`, a beaked skull too big for any bird; "
                     "`jaw`, a toothed jaw beside a wing-bone; `ribs`, ribs and a clawed foot that "
                     "don't belong together. Dig spots: the Oikoumene's mismatched fossils (Dracozolt "
                     "and kin) come out of these.")
    ground(s, "grass")
    M = s.M
    for i in range(4):
        m = F.blob(7.5, 8.5, 7.0, 6.0, 16, 16, wobble=0.1, k=5, seed=i * 1.7)
        for y, x in np.argwhere(m):
            u = (x - 7.5) + (y - 8.5)
            c = "hr4" if u < -4 else ("hr3" if u < 3 else "hr2")
            if F.h(x, y, i) % 9 == 0:
                c = "hr2"
            M.px(i * 16 + x, y, c)
        for y, x in np.argwhere(F.edge_of(m)):
            M.px(i * 16 + x, y, "hr1" if y > 7 else "hr2")
        for x in range(16):
            for y in range(16):
                if not m[y, x] and y > 0 and m[y - 1, x]:
                    M.px(i * 16 + x, y, "gd")
    put(M, 16 + 2, 4, [
        "..0000.....",
        ".0bbbb00...",
        "0bb0bbbb00.",
        "0bbbbbbbbb0",
        ".0bbbbb0000",
        "..0b0b0....",
    ], {"0": "hr1", "b": "bn2"})
    put(M, 32 + 2, 5, [
        "0b0b0b0b0..",
        "bbbbbbbbb0.",
        ".000000bb0.",
        "......0bb0.",
        ".bbbbbb00..",
        "..0000.....",
    ], {"0": "hr1", "b": "bn1"})
    put(M, 48 + 2, 3, [
        "b0b0b0b0b..",
        "b0b0b0b0b..",
        "bbbbbbbbbb0",
        "..........b",
        "....b..b.b.",
        ".....bbbb..",
    ], {"0": "hr2", "b": "bn2"})
    return s


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build():
    out = {}
    for s in (steppe_grass(), feather(), road(), decor(), mudflat(), river(), reed_marsh(),
              reeds_ford(), kurgans(), kurgan_large(), idols(), waystone(), trees(), heights(),
              fossils()):
        out[s.key] = s
    out["road_join"] = road_join(out["road"])
    return out


SPEC = {
    "symbol": "gTileset_Steppe", "dir": "steppe", "label": "Steppe",
    "title": "the steppe: Thrace, the Thermodon and Scythia",
    "doc": "TILES_steppe.md",
    "limit": 504,
    "sections": [
        ("ground", ["steppe_grass", "feather", "road", "road_join", "decor"]),
        ("water", ["river", "reed_marsh", "mudflat", "reeds_ford"]),
        ("mounds", ["kurgan", "kurgan_large", "idols", "waystone"]),
        ("land", ["trees"]),
        ("heights", ["heights", "fossils"]),
    ],
    "rows": {"ground": 0, "water": 17, "mounds": 37, "land": 47, "heights": 50},
    "labels": [("kurgan", [("dig", "DigMound"), ("dug", "DigMound_Dug")]),
               ("kurgan_large", [("c12", "Kurgan_Door_Shut"), ("door", "Kurgan_Door"),
                                 ("c10", "Kurgan_Crown"), ("summit_idol", "Kurgan_Crown_Idol")])],
}
