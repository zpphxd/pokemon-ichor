"""Thyrsa's houses and town furniture (gTileset_Thyrsa).

The house kit: a terracotta roof (ridge and eaves rows), an upper storey and a
ground storey, each a strip of one-cell parts. A Thyrsan house is one or two
storeys of ochre stucco or limewash, its doors and shutters painted
wine-purple (ochre houses) or vine-green (limewashed ones), ivy up its walls,
and a mask over its door for the god's festival: a mask plaque on the upper
storey, or a mask hung from the eaves of a single-storey house. The lime parts
are the ochre parts' own tiles in the clay2 palette, so they cost nothing.

Also: Chthonia's house of huge rough stones (the oldest in the city), a
courtyard wall with a fig over it, the Agora under its striped awning, the
market's stalls, and the festival garlands strung across the streets.
"""
from __future__ import annotations

import emporion_lib as E
import thyrsa_lib as T
from thyrsa_lib import finish, struct

# ==========================================================================
# The house kit
# ==========================================================================


def roof_kit():
    s = struct("roof", "House roof: terracotta, two rows", 6, 2, walk=["XXXXXX", "XXXXXX"],
               ground="none", section="houses",
               notes="Row 0 is the ridge, row 1 the eaves with palmette antefixes. Columns: west "
                     "end, run (repeat it), east end, then a ridge with a clay chimney pot, a "
                     "ridge with doves on it, and, in the eaves row, (3) an eaves cell with a "
                     "festival mask hung under it (for a one-storey house: put it over the "
                     "door).")
    L = s.B
    E.roof(L, 0, 0, 48, 32)
    E.roof(L, 48, 0, 48, 32, ends=(False, False))
    for y in range(0, 32):
        L.px(1, y, "tc3")
        L.px(2, y, "tc2")
        L.px(46, y, "tc0")
        L.px(45, y, "tc1")
    # a chimney pot
    L.blit([" kkkk ", "kt22tk", "k1221k", "k1110k", "k1110k", "kk00kk", "k0000k", " kkkk "],
           {"k": "ink", "t": "tc3", "2": "tc2", "1": "tc1", "0": "tc0"}, 53, 3)
    L.px(55, 1, "w2")
    L.px(56, 0, "w2")
    # two doves on the ridge (Manto's roof)
    for x0 in (66, 73):
        L.blit([" kk  ", "kwwk ", "kwwwk", " kkk "], {"k": "ink", "w": "w0"}, x0, 0)
        L.px(x0 + 1, 1, "ink")
    # the eaves with a mask under the antefixes
    tmp = T.Layer(96, 32)
    T.mask(tmp, 52, 22, "comic")
    for yy in range(22, 29):
        for xx in range(52, 60):
            c = tmp.get(xx, yy)
            if c:
                L.px(xx, yy, {"rd": "tc2", "g0": "tc3"}.get(c, c))
    L.px(55, 21, "ink")
    L.px(56, 21, "ink")
    for x in range(52, 60, 2):
        L.px(x, 22, "iv2")
    s.names = {"W": (0, 0), "run": (1, 0), "E": (2, 0), "chimney": (3, 0), "doves": (4, 0),
               "eaves_W": (0, 1), "eaves_run": (1, 1), "eaves_E": (2, 1), "eaves_mask": (3, 1)}
    # (5, 0) and (5, 1) are plain runs, kept so the sheet packs evenly
    return finish(s)


def _upper_wall(L, x0, w, y0=0):
    """The upper storey: the eaves' shadow, a band of wine-purple dots, stucco,
    and the string course marking the floor."""
    E.stucco(L, x0, y0, w, 16)
    L.hline(x0, x0 + w - 1, y0, "oc0")
    L.hline(x0, x0 + w - 1, y0 + 1, "oc1")
    for x in range(x0, x0 + w):
        L.px(x, y0 + 2, "wn1" if x % 4 in (1, 2) else "oc3")
    L.hline(x0, x0 + w - 1, y0 + 15, "w2")


def _lower_wall(L, x0, w, y0=0):
    E.stucco(L, x0, y0, w, 16)
    L.hline(x0, x0 + w - 1, y0, "oc1")
    for x in range(x0, x0 + w):
        L.px(x, y0 + 11, "tc2")
        for y in range(y0 + 12, y0 + 14):
            L.px(x, y, "tc1")
        L.px(x, y0 + 14, "oc1")
        L.px(x, y0 + 15, "oc0")


def _pilasters(L, w, y0, h):
    for y in range(y0, y0 + h):
        L.px(0, y, "ink")
        L.px(1, y, "w0")
        L.px(2, y, "w2")
        L.px(w - 1, y, "ink")
        L.px(w - 2, y, "w0")
        L.px(w - 3, y, "w2")


def _half(L, cx, y0, y1):
    E.mirror_half(L, cx, 16, y0, y1)


def _window(L, cx, y0, kind):
    if kind == "shutter":
        L.rect(cx + 1, y0 + 4, 3, 10, "wn1")
        for yy in range(y0 + 5, y0 + 14, 2):
            L.px(cx + 2, yy, "wn0")
        E.outline_rect(L, cx + 1, y0 + 4, 3, 10)
        L.rect(cx + 4, y0 + 4, 4, 10, "w0")
        L.rect(cx + 5, y0 + 5, 3, 8, "ink")
        L.rect(cx + 5, y0 + 5, 3, 2, "tc0")
        L.hline(cx + 3, cx + 7, y0 + 13, "w0")
        L.hline(cx + 3, cx + 7, y0 + 14, "w2")
    elif kind == "grille":
        L.rect(cx + 3, y0 + 4, 5, 10, "w0")
        L.rect(cx + 4, y0 + 5, 4, 8, "ink")
        L.vline(cx + 5, y0 + 5, y0 + 12, "tc1")
        L.hline(cx + 4, cx + 7, y0 + 8, "tc1")
        L.hline(cx + 2, cx + 7, y0 + 13, "w0")
        L.hline(cx + 2, cx + 7, y0 + 14, "w2")
    elif kind == "arched":
        L.blit([" kkk ", "kwwwk", "kdddk", "kdddk", "kdddk", "kdddk", "kdddk", "kkkkk"],
               {"k": "ink", "w": "w0", "d": "tc0"}, cx + 2, y0 + 4)
        L.hline(cx + 1, cx + 7, y0 + 12, "w0")
        L.hline(cx + 1, cx + 7, y0 + 13, "w2")
    _half(L, cx, y0, y0 + 16)


def _mask_plaque(L, cx, y0, kind):
    """A festival mask on a round clay plaque wreathed in ivy, over a door."""
    L.blit(["   kkkk   ", "  k1111k  ", " k111111k ", " k111111k ", " k111111k ",
            " k111111k ", "  k1111k  ", "   kkkk   "], {"k": "ink", "1": "tc2"}, cx + 3, y0 + 3)
    tmp = T.Layer(16, 16)
    T.mask(tmp, 4, 4, kind)
    for yy in range(16):
        for xx in range(16):
            c = tmp.get(xx, yy)
            if c:
                L.px(cx + xx, y0 + yy, {"rd": "wn1", "g0": "oc3"}.get(c, c))
    for i, (xx, yy) in enumerate(((3, 4), (2, 6), (2, 8), (3, 10), (12, 4), (13, 6), (13, 8),
                                   (12, 10))):
        L.px(cx + xx, y0 + yy, "iv2" if i % 2 else "iv1")


def _ivy_wall(L, cx, y0):
    T.ivy_patch(L, cx, y0 + 2, 16, 13, density=0.75, seed=31, lit=False, dark="ink")


def upper_storey():
    s = struct("upper", "House upper storey, ochre", 8, 1, walk=["X" * 8], ground="none",
               section="houses",
               notes="One-cell parts for the upper storey, under the roof's eaves: (0) west "
                     "corner, (1) plain wall, (2) a window with wine-purple shutters, (3) a "
                     "window with a wooden grille, (4) a pair of small arched windows, (5) a "
                     "comic mask on an ivy-wreathed plaque and (6) a tragic one (put one over "
                     "the door), (7) east corner.")
    L = s.B
    _upper_wall(L, 0, 128)
    _pilasters(L, 128, 0, 16)
    _window(L, 32, 0, "shutter")
    _window(L, 48, 0, "grille")
    _window(L, 64, 0, "arched")
    _mask_plaque(L, 80, 0, "comic")
    _mask_plaque(L, 96, 0, "tragic")
    s.names = {"W": (0, 0), "wall": (1, 0), "shutters": (2, 0), "grille": (3, 0),
               "arched": (4, 0), "mask": (5, 0), "mask_tragic": (6, 0), "E": (7, 0)}
    return finish(s)


def upper_extras():
    s = struct("upper2", "House upper storey: trade signs, ochre", 4, 1,
               walk=["X" * 4], ground="none", section="houses",
               notes="Upper-storey cells with trade signs on iron brackets: (0) the tavern's "
                     "kantharos, (1) the mask-maker's mask, (2) the vintner's grapes, (3) the "
                     "poet's lyre.")
    L = s.B
    _upper_wall(L, 0, 64)
    SIGNS = {
        "tavern": ["         ", " kkkkkkk ", "kk11111kk", " k11111k ", "  k111k  ", "   k1k   ",
                   "  kkkkk  ", "         "],
        "mask": [" kkkkkk  ", "kwwwwwwk ", "kwkwwkwk ", "kwwwwwwk ", "kw1111wk ", " k1kk1k  ",
                 "  kkkk   ", "         "],
        "grapes": ["   gg    ", "  ggk    ", "  kk1k   ", " k1k1k   ", " k1k1k   ", "  k1k    ",
                   "   k     ", "         "],
        "lyre": [" k     k ", " kk   kk ", " k1kkk1k ", " k1 1 1k ", " k 1 1 k ", "  k1 1k  ",
                 "   kkk   ", "         "],
    }
    for i, (key, rows) in enumerate(SIGNS.items()):
        x0 = i * 16
        L.hline(x0 + 2, x0 + 13, 6, "ink")
        L.px(x0 + 2, 5, "ink")
        L.px(x0 + 2, 7, "ink")
        L.vline(x0 + 4, 7, 8, "ink")
        L.vline(x0 + 12, 7, 8, "ink")
        L.rect(x0 + 3, 8, 11, 7, "w0")
        E.outline_rect(L, x0 + 2, 8, 13, 8, "ink")
        key_map = {"k": "ink", "1": "tc1", "w": "w0", "g": "iv2"}
        if key == "grapes":
            key_map["1"] = "wn1"
        if key == "mask":
            key_map["1"] = "wn1"
        L.blit(rows, key_map, x0 + 4, 8)
    s.names = {"tavern": (0, 0), "mask_maker": (1, 0), "vintner": (2, 0), "poet": (3, 0)}
    return finish(s)


def _door(L, cx, y0, kind):
    if kind == "double":
        L.rect(cx + 2, y0 + 1, 6, 14, "w0")
        L.hline(cx + 1, cx + 7, y0 + 1, "w0")
        L.hline(cx + 1, cx + 7, y0 + 2, "w2")
        L.rect(cx + 4, y0 + 3, 4, 12, "wn1")
        L.vline(cx + 7, y0 + 3, y0 + 14, "ink")
        E.outline_rect(L, cx + 4, y0 + 4, 3, 4, "wn0")
        E.outline_rect(L, cx + 4, y0 + 9, 3, 4, "wn0")
        L.px(cx + 6, y0 + 8, "oc3")
        L.vline(cx + 3, y0 + 3, y0 + 14, "w2")
        L.hline(cx + 2, cx + 7, y0 + 15, "w2")
        L.hline(cx + 1, cx + 7, y0, "ink")
    elif kind == "arched":
        rows = ["   kkkk", "  kwwww", " kwkkkk", " kwk111", "kwk1000", "kwk1000", "kwk1o00",
                "kwk1000", "kwk1000", "kwk1000", "kwk1000", "kwk1o00", "kwk1000", "kwkkkkk",
                "kwwwwww"]
        L.blit(rows, {"k": "ink", "w": "w0", "1": "tc1", "0": "tc0", "o": "oc3"}, cx + 1, y0 + 1)
    elif kind == "shop":
        # an open workshop front: masks drying on a rail over a counter
        L.rect(cx + 1, y0 + 2, 7, 13, "ink")
        L.rect(cx + 2, y0 + 3, 6, 6, "tc0")
        L.hline(cx + 2, cx + 7, y0 + 3, "tc1")
        L.blit(["kwwk", "kwkk", " kk "], {"k": "ink", "w": "w0"}, cx + 3, y0 + 4)
        L.rect(cx + 1, y0 + 9, 7, 6, "tc1")
        L.hline(cx + 1, cx + 7, y0 + 9, "oc3")
        L.hline(cx + 1, cx + 7, y0 + 10, "oc2")
        L.hline(cx + 1, cx + 7, y0 + 14, "tc0")
        L.hline(cx, cx + 7, y0 + 1, "w0")
        E.outline_rect(L, cx, y0 + 1, 16, 15, "ink")
    elif kind == "window_low":
        L.rect(cx + 3, y0 + 2, 5, 6, "w0")
        L.rect(cx + 4, y0 + 3, 4, 4, "ink")
        L.vline(cx + 5, y0 + 3, y0 + 6, "tc1")
        L.hline(cx + 2, cx + 7, y0 + 8, "w2")
    elif kind == "jar":
        L.rect(cx + 1, y0 + 11, 7, 3, "w2")
        L.hline(cx + 1, cx + 7, y0 + 11, "w0")
        L.hline(cx, cx + 7, y0 + 14, "ink")
        E.amphora(L, cx + 4, y0 - 1, body="tc2", lit="tc3", shade="tc1")
        return
    _half(L, cx, y0, y0 + 16)


def ground_storey():
    s = struct("lower", "House ground storey, ochre", 8, 1, walk=["XDDDXXXX"], ground="none",
               section="houses",
               notes="One-cell parts for the ground storey: (0) west corner, (1) a double door "
                     "painted wine-purple, (2) an arched wooden door, (3) an open workshop "
                     "front, masks drying over its counter (a door too), (4) plain wall, (5) a "
                     "low barred window, (6) a stone bench with an amphora, (7) east corner. "
                     "(1)-(3) are MB_NON_ANIMATED_DOOR: put the warp there.")
    L = s.B
    _lower_wall(L, 0, 128)
    _pilasters(L, 128, 0, 16)
    _door(L, 16, 0, "double")
    _door(L, 32, 0, "arched")
    _door(L, 48, 0, "shop")
    _door(L, 80, 0, "window_low")
    _door(L, 96, 0, "jar")
    # ivy climbing the corners
    for x0 in (0, 112):
        for yy in range(3, 15, 2):
            L.px(x0 + (3 if x0 == 0 else 12), yy, "iv1")
            L.px(x0 + (4 if x0 == 0 else 11), yy + 1, "iv2")
    s.names = {"W": (0, 0), "door": (1, 0), "door_arched": (2, 0), "shop": (3, 0),
               "wall": (4, 0), "window": (5, 0), "bench": (6, 0), "E": (7, 0)}
    return finish(s)


def lime(s, key, title):
    notes = (s.notes.replace("ochre", "limewashed").replace("wine-purple", "vine-green")
             + " The limewashed parts are the ochre parts' own tiles in the clay2 palette.")
    return T.recolor(s, T.LIME, key=key, title=title, notes=notes)


# House recipes for the catalog: (title, lime?, uppers, ground, ridge variants, eaves variants)
RECIPES = [
    ("The Kantharos, a tavern", False, [["arched", "x:tavern", "shutters"]],
     ["window", "door", "bench"], [None, "chimney", None], None),
    ("A one-storey house with a mask under its eaves", True, [], ["window", "door_arched", "bench"],
     [None, "chimney", None], [None, "eaves_mask", None]),
    ("The mask-maker's workshop", False, [["x:mask_maker", "grille"]], ["shop", "door"],
     [None, None], None),
    ("A limewashed house with a mask over the door", True, [["shutters", "mask", "grille"]],
     ["window", "door", "wall"], [None, None, "chimney"], None),
]


def recipe_cells(recipe):
    title, is_lime, uppers, lower, ridge, eaves = recipe
    up, lo, ex = ("upper_lime", "lower_lime", "upper2_lime") if is_lime else ("upper", "lower", "upper2")
    n = len(lower)
    eaves = eaves or [None] * n
    rows = [[("roof", "W")] + [("roof", r or "run") for r in ridge] + [("roof", "E")],
            [("roof", "eaves_W")] + [("roof", e or "eaves_run") for e in eaves] + [("roof", "eaves_E")]]
    for upper in uppers:
        rows.append([(up, "W")] + [((ex, p[2:]) if p.startswith("x:") else (up, p)) for p in upper]
                    + [(up, "E")])
    rows.append([(lo, "W")] + [(lo, p) for p in lower] + [(lo, "E")])
    return rows


# ==========================================================================
# Special houses and yards
# ==========================================================================

def sown_house():
    s = struct("sown_house", "Chthonia's house, of huge rough stones", 3, 3,
               walk=["XXX", "XXX", "XDX"], ground="none", section="houses",
               notes="The oldest house in the city, on the Kadmeia: walls of huge rough stones "
                     "under a flat roof of beaten earth edged with slabs, a squat doorway "
                     "under one enormous lintel, and five clay figures of armed men set in a "
                     "niche beside it. The family of the Sown Men lives here. Door: bottom row, "
                     "middle. Its walls are the city wall's masonry: place it at an even map "
                     "column with its roof on an even map row.")
    L = s.B
    W = 48
    # the flat roof: beaten earth, a kerb of slabs, grass tufts
    for x in range(W):
        for y in range(0, 12):
            c = "e1" if (x % 8, y % 4) not in ((2, 1), (6, 3)) else "e2"
            if y < 2:
                c = "cg0" if y == 0 else "cg4"
            L.px(x, y, c)
        L.px(x, 10, "cg4")
        L.px(x, 11, "cg2")
    L.blit([" 3 ", "323"], {"2": "iv2", "3": "iv3"}, 30, 5)
    T.fill_masonry(L, 0, 12, W, 36, "wall", ox=0, oy=16)
    L.vline(0, 0, 47, "ink")
    L.vline(W - 1, 0, 47, "ink")
    for y in range(12, 48):
        L.px(1, y, "cg4")
        L.px(W - 2, y, "cg1")
    # the doorway under one enormous lintel
    L.rect(15, 26, 18, 4, "cg5")
    L.hline(15, 32, 29, "cg2")
    E.outline_rect(L, 14, 25, 20, 6, "cg0")
    L.rect(18, 31, 12, 17, "ink")
    L.rect(19, 32, 10, 16, "cg0")
    # a niche with five clay figures
    L.rect(36, 18, 8, 6, "cg0")
    for k in range(4):
        L.vline(37 + k * 2, 20, 23, "e2")
        L.px(37 + k * 2, 19, "e1")
    s.names = {"door": (1, 2)}
    return finish(s)


def court_wall():
    s = struct("court_wall", "A courtyard wall", 3, 1, walk=["XXX"], ground="none",
               section="houses",
               notes="A stucco yard wall under a tiled coping, one cell tall: (0) west end, (1) "
                     "run (repeat it), (2) east end. Behind Eudora's house, with an aethos "
                     "olive's crown over it.")
    L = s.B
    W = 48
    E.stucco(L, 0, 0, W, 16)
    for x in range(W):
        L.px(x, 0, "ink")
        L.px(x, 1, "tc3" if x % 6 == 0 else "tc2")
        L.px(x, 2, "tc1")
        L.px(x, 3, "tc0")
        L.px(x, 14, "oc1")
        L.px(x, 15, "oc0")
    for x in (0, W - 1):
        L.vline(x, 0, 15, "ink")
    for x in (1, W - 2):
        L.vline(x, 4, 14, "w0" if x == 1 else "w2")
    s.names = {"W": (0, 0), "run": (1, 0), "E": (2, 0)}
    return finish(s)


def fig():
    s = struct("fig", "An old fig over a yard wall", 2, 1, walk=["XX"], ground="grass",
               section="houses",
               notes="The crown of an old fig growing in a walled yard, its broad dark leaves "
                     "and purple figs spilling over the wall: lay it on the yard's grass in "
                     "the row behind court_wall. Drawn over the player.")
    import math
    import random
    Tl = s.T
    rnd = random.Random(5)
    cx, cy = 16, 9
    for _ in range(130):
        a = rnd.uniform(0, 6.28)
        r = rnd.uniform(0, 1) ** 0.5
        x = int(cx + r * 14 * math.cos(a))
        y = int(cy + r * 7 * math.sin(a))
        Tl.blit(["kk ", "122", " 2 "] if rnd.random() < 0.5 else [" kk", "221", " 1 "],
                {"k": "iv0", "1": "iv1", "2": "iv2"}, x - 1, y - 1)
    for _ in range(16):
        Tl.px(cx + rnd.randint(-11, 11), cy + rnd.randint(-6, 2), "iv3")
    for (x, y) in ((10, 6), (20, 10), (14, 12), (23, 4)):
        Tl.px(x, y, "vp0")
        Tl.px(x + 1, y, "vp1")
    Tl.a[:, :1] = 0
    Tl.a[:, 31:] = 0
    return finish(s)


# ==========================================================================
# The Agora, the market and the festival
# ==========================================================================

def agora():
    s = struct("agora", "Thyrsa's Agora", 5, 4, walk=["XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               ground="none", section="civic",
               notes="The market hall off the square, a sibling of aethos's Agora (0x028): "
                     "terracotta roof, a long awning striped red and white over the front, the "
                     "Agora's painted jar on a pinax over the door, and counters either side "
                     "stacked with wine jars and baskets. Door: bottom row, middle "
                     "(MB_NON_ANIMATED_DOOR).")
    L = s.B
    W = 80
    E.roof(L, 0, 0, W, 32)
    for y in range(0, 32):
        L.px(1, y, "tc3")
        L.px(2, y, "tc2")
    # the awning: red and white stripes, scalloped hem (fest group)
    for y in range(32, 48):
        for x in range(W):
            X = x % 8
            L.px(x, y, "rd" if X in (2, 3, 4, 5) else "w0")
    for x in range(W):
        L.px(x, 32, "ink")
        L.px(x, 33, "rd0" if x % 8 in (2, 3, 4, 5) else "w0")
        L.px(x, 44, "rd0" if x % 8 in (2, 3, 4, 5) else "g0")
        X = x % 4
        L.px(x, 46, "ink" if X in (0, 3) else ("rd" if x % 8 in (2, 3, 4, 5) else "w0"))
        L.px(x, 47, "ink")
    L.vline(0, 32, 47, "ink")
    # the ground storey: stucco, counters with jars, the door
    _lower_wall(L, 0, W, 48)
    _pilasters(L, W, 48, 16)
    for x0 in (4, 20):
        L.rect(x0, 56, 12, 6, "tc1")
        L.hline(x0, x0 + 11, 56, "oc3")
        L.hline(x0, x0 + 11, 61, "ink")
        E.amphora(L, x0 + 1, 48, small=True)
        E.amphora(L, x0 + 6, 48, small=True, body="oc2", lit="oc3", shade="oc1", dark="oc0")
    _door(L, 32, 48, "double")
    E.mirror_half(L, 0, W, 0, 64)
    # the pinax over the door: the Agora's jar (fest group, in the awning row)
    L.rect(33, 35, 14, 10, "w0")
    E.outline_rect(L, 32, 34, 16, 12, "ink")
    E.amphora(L, 36, 35, body="rd", lit="w0", shade="rd0", dark="rd0", ink="ink", small=True)
    s.names = {"door": (2, 3)}
    return finish(s)


def _stall_awning(L, c1, edge):
    for y in range(1, 14):
        for x in range(32):
            L.px(x, y, c1 if x % 8 in (2, 3, 4, 5) else "w0")
    L.hline(0, 31, 1, "ink")
    L.vline(0, 1, 13, "ink")
    L.vline(31, 1, 13, "ink")
    L.hline(1, 30, 11, edge)
    for x in range(32):
        X = x % 4
        L.px(x, 13, "ink" if X in (0, 3) else (c1 if x % 8 in (2, 3, 4, 5) else "w0"))
        if X in (0, 3):
            L.px(x, 12, edge)
    L.hline(0, 31, 14, "ink")
    for x in (1, 2, 29, 30):
        L.px(x, 15, "wd0")


def _stall_frame(L):
    for x in (1, 30):
        L.vline(x, 16, 30, "ink")
    for x in (2, 29):
        L.vline(x, 16, 30, "wd1")
    L.rect(1, 22, 30, 8, "wd2")
    L.hline(1, 30, 22, "wd1")
    L.hline(1, 30, 29, "ink")
    L.vline(0, 22, 29, "ink")
    L.vline(31, 22, 29, "ink")
    for x in (7, 8, 15, 16, 23, 24):
        L.vline(x, 24, 28, "wd1")
    L.hline(2, 29, 30, "ink")


def stalls():
    wine = struct("stall_wine", "Market stall: wine", 2, 2, walk=["XX", "XX"], ground="pave",
                  section="civic",
                  notes="Under a purple-and-white awning: a krater, jugs and a rack of amphorae "
                        "of new wine. Free-standing on the flags; the seller stands beside it.")
    M = wine.M
    _stall_awning(M, "vp1", "vp0")
    _stall_frame(M)
    for x0 in (4, 11, 18):
        E.amphora(M, x0, 16, body="tc1", lit="tc2", shade="tc0", dark="tc0", small=True)
    M.blit([" kkkkk ", "k22222k", " k222k ", "  k2k  ", " kkkkk "],
           {"k": "ink", "2": "tc2"}, 23, 17)
    masks = struct("stall_masks", "Market stall: festival masks", 2, 2, walk=["XX", "XX"],
                   ground="pave", section="civic",
                   notes="The mask-seller's stall for the Dionysia, under a green-and-white "
                         "awning: comic, tragic and satyr masks on pegs and on the counter. "
                         "Free-standing on the flags.")
    M = masks.M
    _stall_awning(M, "iv2", "iv1")
    _stall_frame(M)
    for i, x0 in enumerate((3, 12, 21)):
        M.blit([" kkkkk ", "kwwwwwk", "kwkwkwk", "kwwwwwk", " k3k3k ", "  kkk  "],
               {"k": "ink", "w": "w0" if i != 1 else "wd3", "3": "tc1"}, x0, 16)
    return [finish(wine)]


def garland():
    s = struct("garland", "A festival garland across the street", 3, 1, walk=["XTX"],
               ground="pave", section="civic",
               notes="Ivy ropes and red ribbons strung between two ribboned poles, sagging "
                     "over the street: (0) the west pole, (1) the swag (repeat it), (2) the "
                     "east pole. The swags draw over the player, who walks under them.")
    M, Tl = s.M, s.T
    for x0 in (0, 32):
        M.rect(x0 + 6, 2, 4, 14, "wd1")
        M.vline(x0 + 6, 2, 15, "wd0")
        M.vline(x0 + 9, 2, 15, "wd0")
        M.vline(x0 + 7, 2, 15, "wd2")
        M.blit([" gg ", "gkkg"], {"g": "g1", "k": "ink"}, x0 + 6, 0)
        for y in (5, 9):
            M.hline(x0 + 5, x0 + 10, y, "rd")
        M.px(x0 + 11, 6, "rd")
        M.px(x0 + 4, 10, "rd")
        M.rect(x0 + 5, 14, 6, 2, "wd0")
    for x in range(8, 40):
        X = (x - 8) % 16
        sag = int(round(4 * (1 - ((X - 8) / 8) ** 2)))
        y = 3 + sag
        # over the street the swag is on the top layer; at the poles, beside it
        def D(xx):
            return Tl if 16 <= xx < 32 else M
        D(x).px(x, y, "iv1")
        D(x).px(x, y + 1, "iv2" if x % 3 else "iv3")
        if x % 2:
            D(x).px(x, y + 2, "iv1")
        if X == 8:
            D(x).vline(x, y + 2, y + 5, "rd")
            D(x - 1).px(x - 1, y + 5, "rd0")
    s.names = {"post_W": (0, 0), "swag": (1, 0), "post_E": (2, 0)}
    return finish(s)


def statue():
    s = struct("statue", "The god in bronze", 1, 2, walk=["T", "X"], ground="pave", section="civic",
               notes="Dionysus in bronze on a marble plinth in the Agora square: young, ivy-crowned, "
                     "a thyrsus (a fennel staff tipped with a pinecone) in his raised hand. The "
                     "top cell draws over the player; give the bottom cell a bg event.")
    Tl, M = s.T, s.M
    BR = {"k": "ink", "b": "br", "g": "g0", "G": "g1", "m": "m3"}
    # the upper body, the head and the thyrsus (top cell)
    Tl.blit([
        "           G    ",
        "          GgG   ",
        "           g    ",
        "     kkk   b    ",
        "    kGgGk  b    ",
        "    kgbgk  b    ",
        "     kbk   b    ",
        "    kkbbkkkb    ",
        "   kbgbbbbgk    ",
        "   kbgbbbbk     ",
        "   kb kbbbk     ",
        "   kk kbgbk     ",
        "      kbgbk     ",
        "      kbbbk     ",
        "      kbgbk     ",
        "      kbbbk     ",
    ], BR, 0, 0)
    # the ivy crown: two greens are not in the marble group, so the crown is gold
    Tl.px(4, 4, "g1")
    Tl.px(8, 4, "g1")
    # the legs and the plinth (bottom cell)
    M.blit([
        "      kbgbk     ",
        "      kb kbk    ",
        "      kb  kbk   ",
        "     kbk  kbk   ",
        "     kkk  kkk   ",
        "  kkkkkkkkkkkk  ",
        "  k1111111111k  ",
        "  k2222222222k  ",
        "  kkkkkkkkkkkk  ",
        "   k33333333k   ",
        "   k33333333k   ",
        "   k34433443k   ",
        "   k33333333k   ",
        "  kkkkkkkkkkkk  ",
        "  k4444444444k  ",
        "  kkkkkkkkkkkk  ",
    ], {"k": "ink", "b": "br", "g": "g0", "1": "w0", "2": "m2", "3": "m1", "4": "m3"}, 0, 16)
    return finish(s)


def build_houses():
    roof = roof_kit()
    up, ex, lo = upper_storey(), upper_extras(), ground_storey()
    return [roof, up, lime(up, "upper_lime", "House upper storey, limewashed"),
            ex, lime(ex, "upper2_lime", "House upper storey: trade signs, limewashed"),
            lo, lime(lo, "lower_lime", "House ground storey, limewashed"),
            sown_house(), court_wall()]


def build_market():
    return [agora()] + stalls() + [garland(), statue()]
