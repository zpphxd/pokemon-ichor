"""Pontos's towns: Thracian Salmydessos and Colchian Aia.

Houses share one thatch-roof kit. Their walls tell them apart:
  - Salmydessos (Thrace) builds in wattle and daub on a timber frame;
  - Aia (Colchis) builds the way Vitruvius saw it (2.1.4): whole trees laid flat
    and crossed at the corners, raised into towers, roofed in reed thatch.
Aietes's palace is Hephaestus's bronze (Argonautica 3.215-248), with the court
of his four fountains, of milk, wine, oil and water, under vines.
"""
from __future__ import annotations

import pontos_lib as P
from pontos_lib import Struct, finish, logs, mirror, thatch


# --------------------------------------------------------------------------
# The thatch roof kit
# --------------------------------------------------------------------------

def _roof(L, x0, y0, w, h, slant_l=False, slant_r=False, ridge=True, hem=True):
    """Reed thatch seen from the front, h px tall: a log ridge pole on top, thatch
    combed down, a ragged hem of reed ends along the eaves casting a shadow."""
    thatch(L, x0, y0, w, h)
    if ridge:
        L.hline(x0, x0 + w - 1, y0 + 1, "ink")
        L.hline(x0, x0 + w - 1, y0 + 2, "wd3")
        L.hline(x0, x0 + w - 1, y0 + 3, "wd2")
        L.hline(x0, x0 + w - 1, y0 + 4, "wd1")
        L.hline(x0, x0 + w - 1, y0 + 5, "th0")
        for x in range(x0 + 3, x0 + w, 8):          # pegs through the ridge
            L.px(x, y0 + 2, "wd4")
            L.px(x, y0 + 3, "wd1")
        L.hline(x0, x0 + w - 1, y0, None)
    if hem:
        yh = y0 + h - 4
        for x in range(x0, x0 + w):
            X = (x - x0) % 4
            L.px(x, yh, "th2" if X in (1, 2) else "th1")
            L.px(x, yh + 1, "th1" if X != 3 else "th0")
            L.px(x, yh + 2, "th0" if X in (0, 3) else "th1")
            L.px(x, yh + 3, "ink" if X in (0, 3) else "th0")
    # hipped ends: the slope cut away at the sides, top narrower than bottom
    for side, on in (("l", slant_l), ("r", slant_r)):
        if not on:
            continue
        for y in range(y0, y0 + h):
            cut = max(0, (h - (y - y0)) // 3 - 1)
            for i in range(cut):
                x = x0 + i if side == "l" else x0 + w - 1 - i
                L.px(x, y, None)
            xe = x0 + cut if side == "l" else x0 + w - 1 - cut
            L.px(xe, y, "ink")
            xi = xe + (1 if side == "l" else -1)
            if L.get(xi, y) not in (None, "ink"):
                L.px(xi, y, "th0" if side == "r" else "th2")


def roof_kit():
    """Two rows of thatch: W end, run, E end (mirrored), plus Phineus's run with
    the Harpies' claw marks and the patch over the hole they tore."""
    out = []
    for key, title, slant in (("roof_w", "Thatch roof, west end", True),
                              ("roof_run", "Thatch roof, run", False)):
        s = Struct(key, title, 1, 2, walk=["X", "X"], ground="grass",
                   notes="Two rows: the ridge row and the eaves row. Lay W end, runs, E end.")
        _roof(s.M, 0, 2, 16, 30, slant_l=slant)
        out.append(finish(s))
    out.append(mirror(out[0], "roof_e", "Thatch roof, east end"))
    # Phineus's roof: three long claw rakes across the thatch, and a square patch
    s = Struct("roof_claws", "Thatch roof, run, raked by Harpies", 1, 2, walk=["X", "X"],
               ground="grass", notes="Phineus's roof: claw marks, and fresh reed over the hole.")
    _roof(s.M, 0, 2, 16, 30)
    for i, x in enumerate((3, 7, 11)):
        for k in range(9):
            s.M.px(x + k // 3, 8 + k + i, "th0")
            s.M.px(x + k // 3 + 1, 8 + k + i, "ink" if k % 3 else "th0")
    for y in range(18, 26):
        for x in range(5, 12):
            s.M.px(x, y, "th2" if (x + y) % 3 else "rp")
    P.outline_box(s.M, 5, 18, 7, 8, "th0")
    out.append(finish(s))
    return out


# --------------------------------------------------------------------------
# Walls
# --------------------------------------------------------------------------

def _daub(L, x0, y0, w, h):
    """Wattle and daub: a clay wash, the wattle showing through in faint courses."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = "cl1"
            if (y - y0) % 5 == 2 and (x * 3 + y) % 4 != 0:
                c = "cl0" if ((x % 8) + (y % 8)) % 7 == 0 else "cl1"
            if ((x % 8) * 5 + (y % 8) * 3) % 17 == 0:
                c = "cl0"
            L.px(x, y, c)


def _wall_base(L, y0, top=0):
    """Eave shadow along the wall's top, a footing of dark stones at its foot."""
    L.hline(0, 15, top, "sh")
    L.hline(0, 15, top + 1, "wd0")
    for x in range(16):
        L.px(x, 14, "wd1" if x % 5 else "sh")
        L.px(x, 15, "sh" if x % 4 == 0 else "wd0")


def _door(L, x0, kind="plank", frame="wd1"):
    """A doorway 8 px wide from x0: a dark opening with a plank door ajar."""
    L.rect(x0, 3, 9, 12, frame)
    L.rect(x0 + 1, 4, 7, 11, "sh")
    if kind == "plank":
        for y in range(5, 15):
            for x in range(x0 + 1, x0 + 5):
                L.px(x, y, "wd2" if (x - x0) % 2 else "wd1")
        L.px(x0 + 3, 9, "rp")
    L.hline(x0, x0 + 8, 3, "wd0")
    L.hline(x0 - 1, x0 + 9, 2, "wd3")


def _window(L, x0, y0=5):
    L.rect(x0, y0, 6, 5, "wd0")
    L.rect(x0 + 1, y0 + 1, 4, 3, "sh")
    L.hline(x0, x0 + 5, y0 + 5, "wd3")
    L.px(x0 + 2, y0 + 1, "wd1")


def daub_walls():
    """Salmydessos's houses: W end, wall, window, door, E end (one row)."""
    out = []

    def wall(key, title, walk="X", door=False, window=False, end=None):
        s = Struct(key, title, 1, 1, walk=[walk], ground="none",
                   notes="Wattle and daub on a timber frame, the eave's shadow along the top.")
        _daub(s.M, 0, 0, 16, 16)
        _wall_base(s.M, 0)
        if end == "w":
            s.M.rect(0, 0, 3, 16, "wd1")
            s.M.vline(0, 0, 15, "ink")
            s.M.vline(2, 2, 13, "wd0")
        if window:
            _window(s.M, 5)
        if door:
            _door(s.M, 4)
        return finish(s)

    w = wall("daub_w", "Daub wall, west end", end="w")
    out += [w, wall("daub", "Daub wall"), wall("daub_window", "Daub wall, window", window=True),
            wall("daub_door", "Daub wall, door (warp here)", walk="D", door=True),
            mirror(w, "daub_e", "Daub wall, east end")]
    return out


def log_walls():
    """Aia's log towers (Vitruvius 2.1.4): ground floor and upper floor rows, with
    crossed log ends at the corners."""
    out = []

    def wall(key, title, walk="X", door=False, window=False, end=None, upper=False, plaque=None):
        s = Struct(key, title, 1, 1, walk=[walk], ground="none",
                   notes="Whole logs laid flat, four px a course, crossed at the corners.")
        logs(s.M, 0, 0, 16, 16)
        if not upper:
            for x in range(16):
                s.M.px(x, 15, "sh" if x % 4 == 0 else "wd0")
        else:
            s.M.hline(0, 15, 0, "sh")
        if end == "w":
            for y in range(0, 16, 4):
                s.M.blit(["eeee", "dccd", "kddk", "kkkk"][:4], {"e": "wd4", "c": "wd3", "d": "wd2", "k": "wd0"}, 0, y)
            s.M.vline(0, 0, 15, "ink")
        if window:
            _window(s.M, 5, 4 if upper else 5)
            if upper:          # a gallery rail under the upper window
                s.M.hline(3, 12, 11, "wd3")
                for x in (3, 6, 9, 12):
                    s.M.vline(x, 11, 13, "wd1")
        if door:
            _door(s.M, 4, frame="wd0")
            if plaque == "ram":          # Phrixos's golden ram over the door
                s.M.blit([" ggg ", "gGGgg", " g g "], {"g": "wd3", "G": "wd4"}, 5, 0)
        return finish(s)

    w = wall("log_w", "Log wall, west corner", end="w")
    wu = wall("log_up_w", "Log wall, upper floor, west corner", end="w", upper=True)
    out += [w, wall("log", "Log wall"), wall("log_window", "Log wall, window", window=True),
            wall("log_door", "Log wall, door (warp here)", walk="D", door=True),
            wall("log_door_ram", "Log wall, door under a carved ram (Phrixos's sons)", walk="D",
                 door=True, plaque="ram"),
            mirror(w, "log_e", "Log wall, east corner"),
            wu, wall("log_up", "Log wall, upper floor", upper=True),
            wall("log_up_window", "Log wall, upper floor, window and gallery", upper=True, window=True),
            mirror(wu, "log_up_e", "Log wall, upper floor, east corner")]
    return out


# --------------------------------------------------------------------------
# Aietes's palace: Hephaestus's bronze
# --------------------------------------------------------------------------

def _bronze_shaft(L, x, y, w, h):
    ramp = ["ink", "bz3", "bz4", "bz3", "bz2", "bz2", "bz1", "bz0", "ink"]
    for yy in range(y, y + h):
        for i in range(w):
            j = int(i * (len(ramp) - 1) / max(1, w - 1))
            L.px(x + i, yy, ramp[j])
    for yy in range(y + 2, y + h, 5):          # bands round the shaft
        L.hline(x + 1, x + w - 2, yy, "bz1")


def palace():
    """Aietes's palace front, 8 x 6, left half drawn and mirrored: a gilded roof
    with Helios's sun disc at the peak (Aietes is his son), a frieze of bulls'
    heads, bronze columns, the great bronze doors and the steps."""
    W, H = 8, 6
    s = Struct("palace", "Aietes's bronze palace", W, H,
               walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "........"],
               ground="none",
               notes="The crown of Aia. Rows 0-1 roof, 2 frieze, 3-4 colonnade with the great "
                     "doors at x 3-4 (a hall door, locked until batch 2: no door behavior), 5 the "
                     "steps, walkable. ICHOR_STUB_HALL.")
    M = s.M
    w = W * 16
    # the roof's top row and hipped ends stand against grass
    s.set_ground("grass", [(x, y) for x in range(W) for y in (0, 1)])
    # roof: bronze tiles in courses, gilded ridge, raking edges
    for y in range(4, 32):
        for x in range(0, w):
            X, Y = x % 8, (y - 4) % 4
            c = "bz2"
            if X == 6:
                c = "bz3"
            elif X == 7:
                c = "bz1"
            elif Y == 0:
                c = "bz3"
            elif Y == 3:
                c = "bz1"
            M.px(x, y, c)
    for y in range(4, 32):                     # the roof's hipped ends
        cut = max(0, (32 - y) // 2 - 2)
        for i in range(cut):
            M.px(i, y, None)
        M.px(cut, y, "ink")
    M.hline(0, w - 1, 31, "ink")
    for x in range(0, w, 8):
        M.px(x + 6, 30, "bz4")
    # the ridge and the sun disc of Helios at the peak
    M.hline(14, w - 1, 4, "ink")
    M.hline(14, w - 1, 5, "bz4")
    M.hline(14, w - 1, 6, "bz3")
    c = w // 2                                # the disc straddles the middle
    M.ellipse(c - 7, 0, c + 6, 13, "bz1")
    M.ellipse(c - 6, 1, c + 5, 12, "oil")
    M.ellipse(c - 4, 3, c + 3, 10, "bz4")
    M.px(c - 3, 4, "w0")
    for (x0, y0, x1, y1) in ((c - 8, 6, c - 12, 6), (c - 7, 2, c - 10, 0), (c - 7, 10, c - 10, 12)):
        M.line(x0, y0, x1, y1, "oil")          # rays
    # frieze (row 2): a band with bulls' heads, Hephaestus's bronze bulls
    M.rect(0, 32, w, 16, "bz1")
    M.hline(0, w - 1, 32, "bz4")
    M.hline(0, w - 1, 33, "bz3")
    M.hline(0, w - 1, 46, "bz0")
    M.hline(0, w - 1, 47, "ink")
    for cx in (8, 24, 40):
        M.blit(["h      h",
                "hh    hh",
                " hbbbbh ",
                "  bBBb  ",
                "  bkBb  ",
                "  bBBb  ",
                "   bb   ",
                "   ff   "], {"h": "bz4", "b": "bz2", "B": "bz3", "k": "ink", "f": "fire"}, cx - 4, 36)
    # colonnade (rows 3-4): bronze columns before a dark porch
    M.rect(0, 48, w, 32, "bz0")
    for y in range(48, 80, 8):          # the porch's shadowed courses
        M.hline(0, w - 1, y + 7, "ink")
    for cx in (2, 18, 34):
        M.rect(cx - 1, 48, 12, 3, "bz3")
        M.hline(cx - 1, cx + 10, 48, "bz4")
        _bronze_shaft(M, cx, 51, 10, 29)
    # the great doors at the middle: bronze leaves with bosses, shut
    for y in range(52, 80):
        for x in range(50, 64):
            c = "bz2" if (x - 50) % 7 else "bz1"
            if (y - 52) % 8 == 0:
                c = "bz1"
            M.px(x, y, c)
    for y in range(56, 80, 8):
        for x in range(53, 64, 7):
            M.px(x, y, "bz4")
            M.px(x + 1, y + 1, "bz0")
    M.vline(63, 52, 79, "ink")
    M.hline(50, 63, 51, "bz4")
    M.vline(49, 51, 79, "bz4")
    # steps (row 5), walkable: three stone treads with a bronze nosing
    for y in range(80, 96):
        for x in range(w):
            k = (y - 80) % 5
            M.px(x, y, "bz3" if k == 0 else ("bz1" if k == 4 else "mk"))
    P.mirror_half(M, 0, w, 0, 96)
    return [finish(s)]


def fountain(liquid):
    """One of Hephaestus's four fountains (Argonautica 3.220-227): a bronze basin
    with a bull's head spout, running with milk, wine, oil or water. 2 x 2; the
    basin is solid, the cells in front of it walkable."""
    col = {"milk": ("mk", "w0", "mk"), "wine": ("wn0", "wn1", "wn0"), "oil": ("bz3", "oil", "bz4"),
           "water": ("wa", "w0", "wa")}[liquid]
    s = Struct(f"fountain_{liquid}", f"Fountain of {liquid}", 2, 2, walk=["XX", "XX"], ground="grass",
               notes=f"Hephaestus's fountain of {liquid}: read it (a bg sign) for its line.")
    M = s.M
    deep, glint, mid = col
    # basin: a wide bronze bowl, its rim lit
    M.ellipse(2, 13, 29, 30, "bz1")
    M.ellipse(3, 13, 28, 27, "bz2")
    M.ellipse(5, 15, 26, 25, deep)
    for x in range(8, 24, 4):
        M.px(x, 19, glint)
        M.px(x + 1, 21, mid)
    M.hline(6, 25, 13, "bz4")
    M.hline(4, 27, 14, "bz3")
    M.ellipse(10, 27, 21, 31, "bz0")         # its foot
    # the spout pillar and a bull's head
    M.rect(13, 3, 6, 13, "bz2")
    M.vline(13, 3, 15, "bz3")
    M.vline(18, 3, 15, "bz0")
    M.blit(["h    h", "hbbbbh", " bkkb ", " bbbb ", "  bb  "], {"h": "bz4", "b": "bz3", "k": "bz0"},
           13, 0)
    # the stream from its mouth into the bowl
    for y in range(5, 16):
        M.px(15 + (y > 10), y, glint if y % 3 else mid)
        M.px(16 + (y > 10), y, mid)
    P.mirror_half(M, 0, 32, 0, 32)
    return finish(s)


def vine_post():
    """A trellis post hung with grapevine, between the fountains (the lofty vines
    over them, Argonautica 3.220)."""
    s = Struct("vine_post", "Vine on a trellis post", 1, 2, walk=["T", "X"], ground="grass",
               notes="Top half drawn over the player.")
    M, T = s.M, s.T
    leaves = P.Layer(16, 32)
    leaves.rect(6, 16, 4, 16, "tr1")
    leaves.vline(6, 16, 31, "tr0")
    leaves.vline(9, 16, 31, "tr0")
    for (x, y, r) in ((8, 6, 7), (3, 12, 4), (13, 13, 4), (8, 18, 4)):
        leaves.ellipse(x - r, y - r, x + r, y + r, "fg1")
        leaves.ellipse(x - r + 1, y - r + 1, x + r - 2, y + r - 2, "fg2")
        leaves.px(x - 1, y - 2, "fg3")
    for (x, y) in ((5, 14), (11, 9), (7, 4), (12, 16), (3, 9)):
        leaves.blit(["bb", "bbb", " b"], {"b": "bry"}, x, y)
    T.a[0:16] = leaves.a[0:16]       # the crown over the player
    M.a[16:32] = leaves.a[16:32]     # the post and the lower leaves
    return finish(s)


def ram_post():
    """The waystone: a log post with a bronze ram's head, for the ram that carried
    Phrixos here. Travellers touch it for luck. ICHOR_STUB_HERM."""
    s = Struct("ram_post", "Ram post, Aia's waystone", 1, 2, walk=["X", "X"], ground="grass")
    M = s.M
    M.rect(5, 12, 6, 20, "bz1")
    M.vline(5, 12, 31, "bz2")
    M.vline(10, 12, 31, "bz0")
    for y in range(14, 32, 4):
        M.hline(5, 10, y, "bz0")
    M.blit(["  hhhh   ",
            " hBBBBh  ",
            "hBbbbbBh ",
            "hBbkbbbBh",
            " hbbbbbh ",
            "  bbbbh  ",
            "   bbb   ",
            "  hh hh  ",
            " h      h"], {"h": "bz4", "B": "bz3", "b": "bz2", "k": "ink"}, 3, 3)
    return finish(s)


# --------------------------------------------------------------------------
# Harbors: piers, boats, the ship at her mooring
# --------------------------------------------------------------------------

def _planks(L, x0, y0, w, h, across=True):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            k = (y - y0) % 4 if across else (x - x0) % 4
            c = "wd3" if k == 0 else ("wd1" if k == 3 else "wd2")
            if ((x % 8) * 7 + (y % 8) * 3) % 23 == 0:
                c = "wd1"
            L.px(x, y, c)


def pier():
    """A plank pier on posts over the sea, one cell wide, running north from the
    shore: root, run, tip. Walkable; surf off its tip or sides."""
    out = []
    for key, title, posts in (("pier_root", "Pier, root at the shore", "s"),
                              ("pier_run", "Pier, run", ""), ("pier_tip", "Pier, tip with posts", "n")):
        s = Struct(key, title, 1, 1, walk=["."], ground="psea")
        M = s.M
        _planks(M, 2, 0, 12, 16)
        M.vline(1, 0, 15, "wd0")
        M.vline(14, 0, 15, "wd0")
        for y in (3, 11):                      # the posts under the deck
            M.px(0, y, "wd1")
            M.px(15, y, "wd1")
            M.px(0, y + 1, "wd0")
            M.px(15, y + 1, "wd0")
        if posts == "n":
            M.hline(2, 13, 0, "wd0")
            for x in (2, 12):
                M.rect(x, 0, 2, 3, "wd3")
                M.px(x, 0, "wd4")
            M.hline(4, 11, 1, "rp")            # a rope between the posts
        out.append(finish(s))
    return out


def boat():
    """A Thracian fishing boat moored on the sea, bow east: 2 x 1, solid."""
    s = Struct("boat", "Fishing boat, moored", 2, 1, walk=["XX"], ground="psea")
    M = s.M
    M.poly([(2, 7), (27, 7), (31, 9), (28, 13), (4, 13), (1, 10)], "wd1")
    M.poly([(3, 7), (26, 7), (29, 9), (4, 9)], "wd2")
    M.hline(2, 28, 7, "wd3")
    M.hline(4, 27, 13, "ink")
    M.rect(6, 8, 18, 2, "wd0")                  # the hold
    M.rect(10, 8, 3, 2, "rp")                   # coiled net
    M.vline(15, 1, 8, "wd0")                    # the stubby mast
    M.hline(13, 17, 2, "wd2")
    M.hline(4, 26, 14, "w0")                    # foam where it sits
    M.px(30, 12, "w0")
    M.blit(["rr"], {"r": "rd"}, 27, 8)          # a red eye at the bow
    return finish(s)


def ship():
    """The Euploia at her mooring, stern to the quay: 3 x 2 on the sea, her
    gangplank down onto the quay cell below the middle (that cell is where
    Nausikles waits). ICHOR_STUB_SHIP."""
    s = Struct("ship", "The Euploia, moored stern-to", 3, 2, walk=["XXX", "XXX"], ground="psea",
               notes="Moor her with the gangplank's foot (row 1, x 1) on the quay's water edge: "
                     "the cell below it is the gangplank tile.")
    M, T = s.M, s.T
    # hull, seen from astern and a little above: a broad dark stern, the deck
    M.poly([(3, 12), (44, 12), (46, 18), (42, 30), (6, 30), (1, 18)], "wd1")
    M.poly([(6, 13), (41, 13), (43, 18), (5, 18)], "wd2")
    M.hline(3, 44, 12, "ink")
    M.hline(6, 42, 30, "ink")
    for y in (20, 24, 27):
        M.hline(4, 44, y, "wd0")
    M.blit(["kkk", "kek", "kkk"], {"k": "wd0", "e": "w0"}, 8, 21)       # the painted eyes
    M.blit(["kkk", "kek", "kkk"], {"k": "wd0", "e": "w0"}, 36, 21)
    M.hline(2, 45, 31, "w0")
    # the curled stern-post and the mast with its furled sail
    M.poly([(20, 12), (27, 12), (25, 4), (27, 1), (23, 0), (21, 3)], "wd2")
    M.line(23, 0, 21, 3, "wd0")
    M.vline(14, 0, 12, "wd0")
    M.rect(9, 3, 11, 3, "rp")
    M.hline(9, 19, 6, "wd1")
    # oars shipped along the sides
    for y in (15, 17):
        M.hline(0, 4, y, "wd3")
        M.hline(43, 47, y, "wd3")
    # the gangplank down to the quay
    _planks(M, 18, 18, 12, 14, across=True)
    M.vline(18, 18, 31, "wd0")
    M.vline(29, 18, 31, "wd0")
    return finish(s)


def nets():
    """Nets drying between two poles, cork floats along the head rope: 2 x 1."""
    s = Struct("nets", "Nets drying on poles", 2, 1, walk=["XX"], ground="grass")
    M = s.M
    for x in (2, 28):
        M.rect(x, 0, 2, 16, "wd1")
        M.vline(x, 0, 15, "wd2")
    for y in range(3, 14):
        for x in range(4, 28):
            if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                M.px(x, y, "rp" if y > 4 else "wd3")
    for x in range(5, 28, 4):
        M.rect(x, 2, 2, 2, "rd")
    return finish(s)


def wreck():
    """Timbers of a wreck on the sand, ribs up. Salmydessos lived off wrecks, and set
    boundary stones along the beach to divide what washed up (Xenophon, Anabasis
    7.5.12-13): 2 x 1 on sand."""
    s = Struct("wreck", "Wreck timbers", 2, 1, walk=["XX"], ground="sand")
    M = s.M
    M.rect(2, 10, 28, 3, "wd1")
    M.hline(2, 29, 10, "wd2")
    M.hline(2, 29, 13, "wd0")
    for x in (5, 11, 17, 23):
        M.line(x, 10, x - 2, 2, "wd2")
        M.line(x + 1, 10, x - 1, 2, "wd1")
        M.px(x - 2, 1, "wd3")
    M.hline(0, 31, 14, "sh")
    return finish(s)


def boundary_stone():
    """A hóros: a rough upright stone marking whose stretch of beach is whose."""
    s = Struct("horos", "Boundary stone on the beach", 1, 1, walk=["X"], ground="sand")
    M = s.M
    M.poly([(5, 2), (10, 1), (11, 13), (4, 13)], "wd2")
    M.vline(5, 3, 13, "wd3")
    M.vline(10, 2, 13, "wd0")
    M.hline(4, 11, 14, "sh")
    for (x, y) in ((7, 5), (8, 6), (7, 7), (8, 8)):     # a cut mark
        M.px(x, y, "wd0")
    return finish(s)


def table():
    """Phineus's table outside his door, set with bread and a cup: the meals the
    Harpies used to snatch (Argonautica 2.178-193). 2 x 1."""
    s = Struct("table", "Phineus's table", 2, 1, walk=["XX"], ground="grass")
    M = s.M
    M.rect(2, 4, 28, 6, "wd2")
    M.hline(2, 29, 4, "wd3")
    M.hline(2, 29, 9, "wd0")
    for x in (3, 27):
        M.rect(x, 10, 2, 5, "wd1")
    M.ellipse(6, 1, 12, 6, "wd4")              # bread
    M.ellipse(15, 2, 19, 5, "rp")              # a bowl of curds
    M.rect(23, 1, 3, 4, "cl1")                 # a cup
    M.hline(0, 31, 15, "sh")
    return finish(s)


def dovecote():
    """The bird-catcher's dovecote: a wicker cote on a post, a dove at its door."""
    s = Struct("dovecote", "Dovecote", 1, 2, walk=["T", "X"], ground="grass",
               notes="Top row drawn over the player.")
    M, T = s.M, s.T
    T.poly([(1, 6), (8, 0), (15, 6)], "th1")
    T.line(1, 6, 8, 0, "ink")
    T.line(8, 0, 15, 6, "ink")
    T.hline(1, 15, 6, "th0")
    for y in range(7, 16):
        for x in range(2, 14):
            T.px(x, y, "wd2" if (x + y) % 2 else "wd3")
    T.rect(6, 9, 4, 4, "sh")
    T.blit(["ww", "ww"], {"w": "w0"}, 6, 10)
    for y in range(16, 19):
        for x in range(2, 14):
            M.px(x, y, "wd2" if (x + y) % 2 else "wd3")
    M.hline(2, 13, 19, "wd0")
    M.rect(7, 20, 3, 12, "wd1")
    M.vline(7, 20, 31, "wd2")
    M.hline(4, 11, 31, "sh")
    return finish(s)


def cages():
    """Wicker cages of birds by the bird-catcher's door, and his lime-twigs."""
    s = Struct("cages", "Bird cages", 1, 1, walk=["X"], ground="grass")
    M = s.M
    for (x0, y0) in ((1, 4), (8, 2)):
        M.ellipse(x0, y0, x0 + 6, y0 + 10, "wd2")
        for y in range(y0 + 1, y0 + 10):
            for x in range(x0 + 1, x0 + 6):
                if (x - x0) % 2 == 1:
                    M.px(x, y, "wd0")
        M.px(x0 + 3, y0 + 6, "w0")
        M.px(x0 + 2, y0 + 6, "w0")
    M.hline(0, 15, 15, "sh")
    return finish(s)


def sea_mark():
    """A sea-mark: a tarred post in the sea with a painted board, read from the
    water. The lanes' signs. Solid."""
    s = Struct("sea_mark", "Sea-mark post with a board", 1, 1, walk=["X"], ground="psea")
    M = s.M
    M.rect(7, 4, 2, 11, "wd0")
    M.rect(2, 1, 12, 6, "wd2")
    P.outline_box(M, 2, 1, 12, 6, "wd0")
    M.hline(4, 11, 3, "rd")
    M.hline(4, 9, 4, "w0")
    M.hline(5, 11, 15, "w0")
    M.px(4, 14, "w0")
    M.px(12, 14, "w0")
    return finish(s)


def build_salmydessos():
    return (roof_kit() + daub_walls() + pier() + [boat(), nets(), wreck(), boundary_stone(), table(),
                                                 dovecote(), cages(), sea_mark()])


def build_aia():
    return (log_walls() + palace() + [fountain(k) for k in ("milk", "wine", "oil", "water")]
            + [vine_post(), ram_post(), ship()])
