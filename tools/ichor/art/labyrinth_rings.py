"""The outer rings' fixtures, for gTileset_Labyrinth (LABYRINTH.md §5-§6).

  Ring I    the bronze braziers (2 x 2, cold and lit, their flames animated) and the
            threshold hearth, Hestia's, that never goes out
  Ring II   the sun and moon gates; Asterion's cracked walls, whole and broken
  Ring III  web anchors; Daedalus's glow-marks, painted in the latent glow color
  Ring V    the skylight pools by day and by night (MB_ICHOR_LIGHT_POOL, with
            their thread twins), the niches and a niche shrine, the fresco of the
            dance's steps 4-6
  all       the labrys seals, the doorways' jambs

Every passage these pieces open (a gate, a seal, a breach) opens onto plain ring
floor, `thread` `dark_l` / `dark_r` by parity, so the thread can be laid through
it: a threaded ring's walkable cells must all be registered floors.
"""
from __future__ import annotations

import math

import labyrinth_art as A
import labyrinth_kit as KIT
from labyrinth_art import Struct, blit

BZ = {"k": "ink", "0": "bz0", "1": "bz1", "2": "bz2", "3": "bz3", "4": "bz4"}
FI = {"k": "ink", "e": "fe0", "E": "fe1", "f": "ff0", "c": "ff1", "y": "ff2", "w": "ff3",
      "1": "fz0", "2": "fz1", "3": "fz2", "i": "fi0", "I": "fi1", "J": "fi2", "a": "fc0",
      "b": "fc1"}
ST = {"k": "lk", "1": "ls1", "2": "ls2", "3": "ls3", "4": "ls4", "5": "ls5", "6": "ls6",
      "j": "lj", "w": "lw1", "d": "ld0", "D": "ld1", "g": "lg"}


def lay(s, odd=False):
    """Lay the rings' floor under a piece (its floor_cells, default all). The
    piece itself goes in the middle layer, so its odd twin costs no tiles: no
    light or shadow is painted into the floor under it."""
    return KIT.on_ring_floor(s, getattr(s, "floor_cells", None), odd=odd,
                             kind=getattr(s, "floor_kind", "dark"))


def twins(s):
    return KIT.ring_twins(s)


# --------------------------------------------------------------------------
# Ring I: braziers and the threshold hearth
# --------------------------------------------------------------------------

def _brazier_body(M, x0, lit):
    """A Minoan bronze tripod brazier in a 32 x 32 box: a wide bowl with a
    beaded band, three splayed legs on lion's feet. Bronze tiles that touch fire
    use only bz1-bz3 (the fire palette's own bronze)."""
    # the bowl's body below the rim (y 16-22): pure bronze tiles
    rows = {16: (3, 28), 17: (4, 27), 18: (5, 26), 19: (6, 25), 20: (8, 23), 21: (10, 21),
            22: (12, 19)}
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            t = (x - a) / max(1, b - a)
            c = "bz4" if t < 0.12 else "bz3" if t < 0.35 else "bz2" if t < 0.7 else "bz1"
            if x in (a, b):
                c = "ink"
            M.px(x0 + x, y, c)
        if y == 22:
            for x in range(a, b + 1):
                M.px(x0 + x, y, "ink" if x in (a, b) else "bz1")
    # a beaded band round the bowl
    for x in range(6, 26, 3):
        M.px(x0 + x, 18, "bz4" if x < 14 else "bz3")
    for x in range(5, 27):
        M.px(x0 + x, 17, "bz0" if x not in (4, 27) else "ink")
    M.px(x0 + 4, 17, "ink")
    M.px(x0 + 27, 17, "ink")
    # the stem and three legs
    blit(M, ["......k21k......",
             ".....k2311k.....",
             "....k23k11k.....",
             "...k23k.k11k....",
             "..k23k..k21k....",
             ".k23k...k21k....",
             "k432k..k3221k...",
             "kkkk...kkkkkk..."], BZ, x0 + 6, 23)
    blit(M, ["k12k",
             ".k11k",
             "..k11k",
             "...k11k",
             "....k11k",
             "....k1110k",
             "....kkkkk"], BZ, x0 + 18, 23)
    # the bowl's rim, seen from a little above (y 11-15): fire-palette bronze
    for y in range(11, 16):
        for x in range(2, 30):
            dx = (x - 15.5) / 14.0
            dy = (y - 13.5) / 2.6
            r = dx * dx + dy * dy
            if r <= 1.0:
                inner = ((x - 15.5) / 11.5) ** 2 + ((y - 13.2) / 1.6) ** 2 <= 1.0
                if inner:
                    if lit:
                        c = "ff1" if (x * 3 + y) % 5 == 0 else "fe1" if (x + y) % 3 == 0 else "ff0"
                    else:
                        c = "fi1" if (x * 3 + y) % 4 == 0 else "fi0" if (x + y) % 3 else "fe0"
                else:
                    c = "fz2" if (x < 16 and y < 14) else "fz1" if y < 15 else "fz0"
                    if r > 0.82:
                        c = "ink"
                M.px(x0 + x, y, c)


FLAMES = [
    ["...........c....",
     "..........cc....",
     ".....c....cyc...",
     "....cc...cyyc...",
     "....cyc..cywc.c.",
     "...cyyc.cyywycc.",
     "..fcywyccywwyyc.",
     "..fcywwycywwwyf.",
     ".ffcywwwyywwwycf",
     ".fccywwwwwwwyycf",
     "ffccyyywwwwyyccf",
     "fEfccyyyyyyyccfE"],
    ["......c.........",
     "......cc.....c..",
     ".....cyc.....cc.",
     ".....cyyc...cyc.",
     "..c..cywc...cyc.",
     "..cc.cywyc.cyyc.",
     ".fcyccywwycyywcf",
     ".fcyycywwycywwcf",
     ".fcywyywwwywwycf",
     "ffcywwwwwwwwyycf",
     "fccyyywwwwwyyccf",
     "EfccyyyyyyyyccfE"],
    ["........c.......",
     ".......cc..c....",
     "...c...cyc.cc...",
     "...cc.cyyc.cyc..",
     "..cyc.cywycyyc..",
     "..cyc.cywwcywc..",
     ".fcyycywwyywwcf.",
     ".fcywyywwwwwycf.",
     "ffcywwwwwwwwyccf",
     "fccywwwwwwwwycff",
     "fccyyywwwwyyyccf",
     "EfccyyyyyyyyccfE"],
]


def _flames(M, x0, frame):
    blit(M, FLAMES[frame], FI, x0 + 8, 0)
    # embers spitting up
    for (x, y) in ((6, 4), (25, 2), (23, 7)) if frame == 1 else \
                  ((7, 2), (24, 5)) if frame == 2 else ((5, 6), (26, 3), (21, 1)):
        M.px(x0 + x, y, "ff2")


def braziers():
    """Ring I's five braziers and Ring III's: 2 x 2, cold and lit."""
    s = Struct("brazier", "Braziers: bronze tripods, cold and lit", 4, 2, walk=["XXXX", "XXXX"],
               notes="A Minoan bronze tripod brazier, 2 x 2: columns 0-1 **cold** (ash in "
                     "the bowl), columns 2-3 **lit** (coals glowing, its flames animated). "
                     "**Each lit cell is its cold cell + 2.** Swap all four cells together when "
                     "it lights (ENGINE_API.md §2, braziers) and keep them impassable; put the "
                     "brazier's bg event on its bottom row. On the odd parity use "
                     "`brazier_odd`.")
    lay(s)
    _brazier_body(s.M, 0, lit=False)
    _brazier_body(s.M, 32, lit=True)
    frames = A.anim_layer(s, "flame", 3)
    _flames(s.M, 32, 0)
    for i, f in enumerate(frames, 1):
        _flames(f, 32, i)
    s.names = {"cold_tl": (0, 0), "cold_tr": (1, 0), "cold_bl": (0, 1), "cold_br": (1, 1),
               "lit_tl": (2, 0), "lit_tr": (3, 0), "lit_bl": (2, 1), "lit_br": (3, 1)}
    return twins(s)


def hearth():
    """The threshold hearth (Ring I): Hestia's, the house's oldest fire, a low
    round hearth of clay, always burning."""
    s = Struct("hearth", "The threshold hearth", 2, 2, walk=["XX", "XX"],
               notes="Ring I's threshold hearth, the house's oldest fire (LABYRINTH.md §6, "
                     "Ring I): a low round hearth of fired clay ringed with stones, a bed of "
                     "embers, a steady flame (animated). It never goes out. Its bg event "
                     "relights the torch. `hearth_odd` on the odd parity.")
    lay(s)
    M = s.M
    # the clay ring, seen from a little above: y 14-30
    for y in range(13, 31):
        for x in range(1, 31):
            dx = (x - 15.5) / 15.0
            dy = (y - 22.0) / 8.5
            r = dx * dx + dy * dy
            if r > 1.0:
                continue
            inner = ((x - 15.5) / 11.0) ** 2 + ((y - 21.0) / 5.2) ** 2 <= 1.0
            if inner:
                c = "fe0"
                if (x * 7 + y * 3) % 5 == 0:
                    c = "fe1"
                if (x * 5 + y * 11) % 9 == 0:
                    c = "ff0"
            else:
                c = "fc1" if (y < 22 and x < 20) else "fc0"
                if y >= 27:
                    c = "fc0"
                if r > 0.86:
                    c = "ink"
                elif (x * 3 + y) % 7 == 0 and y > 20:
                    c = "fi1"       # a stone in the ring
            M.px(x, y, c)
    # two charred logs crossed in the embers
    blit(M, ["..kk.......kk..",
             ".kiiik...kiiik.",
             "..kiiikkkiiik..",
             "....kiiIiik....",
             "..kiiikkkiiik..",
             ".kiiik...kiiik.",
             "..kk.......kk.."], FI, 8, 16)

    frames = A.anim_layer(s, "flame", 3)
    blit(M, FLAMES[0], FI, 8, 8)
    for i, f in enumerate(frames, 1):
        blit(f, FLAMES[i], FI, 8, 8)
    s.names = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    return twins(s)


# --------------------------------------------------------------------------
# Walls with something in them
# --------------------------------------------------------------------------

def face(L, x0, y0, l="cont", r="cont"):
    KIT.draw_face(L, x0, y0, l, r)


def top(L, x0, y0, **k):
    KIT.draw_top(L, x0, y0, **k)


def crack(L, x0, y0, pts, branch=(), chip=()):
    """A crack: a polyline in the darkest stone, its lower lip lit."""
    def seg(a, b):
        (xa, ya), (xb, yb) = a, b
        n = max(abs(xb - xa), abs(yb - ya))
        out = []
        for i in range(n + 1):
            out.append((round(xa + (xb - xa) * i / max(1, n)), round(ya + (yb - ya) * i / max(1, n))))
        return out
    px = []
    for path in [pts] + list(branch):
        for a, b in zip(path, path[1:]):
            px += seg(a, b)
    for (x, y) in px:
        L.px(x0 + x, y0 + y, "lk")
    for (x, y) in px:
        if L.get(x0 + x + 1, y0 + y + 1) not in (None, "lk"):
            L.px(x0 + x + 1, y0 + y + 1, "ls5")
    for (x, y) in chip:
        L.px(x0 + x, y0 + y, "lk")


def cracked():
    """Asterion's cracked walls (LABYRINTH.md §5.3): whole, cracked so they read
    as weak from across a corridor; register each with Ichor_AddCrackedWall and
    give it a floor cell as its broken metatile."""
    s = Struct("cracked", "Cracked walls, and the breach a charge leaves", 7, 1,
               walk=["XXXXXXX"],
               notes="Walls Asterion's charge can break (LABYRINTH.md §5.3), one cell thick. "
                     "(0) `face`: a cracked face, for a charge from the south; (1) `top_we`: a "
                     "cracked one-cell wall seen from above, for a charge from the east or "
                     "west; (2) `top_n`, (3) `top_w`, (4) `top_e`: a cracked wall top's rim, "
                     "for a charge from the north, west or east into a thicker wall's side. "
                     "Register each with `Ichor_AddCrackedWall` and give it the ring floor "
                     "for its parity (`thread` `dark_l` or `dark_r`) as its broken metatile, so "
                     "the thread can be laid through the breach. Then, in ON_LOAD when its "
                     "flag is set, swap the faces either side of a breach in a row of faces for "
                     "its broken edges: (5) `breach_r` west of it, (6) `breach_l` east of it (a "
                     "breach in a one-cell wall of tops needs nothing more: autotile it). All "
                     "block.")
    L, M = s.B, s.M
    # the cracks are overlays in three shared tiles, laid over the plain kit
    face(L, 0, 0)
    _crack_tile(M, 8, 0, CRACK_V1)
    _crack_tile(M, 8, 8, CRACK_V2)
    _crack_tile(M, 0, 8, CRACK_D)
    top(L, 16, 0, w=True, e=True)
    _crack_tile(M, 16, 0, CRACK_V1)
    _crack_tile(M, 16, 8, CRACK_V2)
    top(L, 32, 0, n=True)
    _crack_tile(M, 32, 0, CRACK_V1)
    _crack_tile(M, 32, 8, CRACK_V2)
    top(L, 48, 0, w=True)
    _crack_tile(M, 48, 0, CRACK_D)
    _crack_tile(M, 48, 8, CRACK_V2)
    top(L, 64, 0, e=True)
    _crack_tile(M, 72, 0, CRACK_D, hflip=True)
    _crack_tile(M, 72, 8, CRACK_V2, hflip=True)
    # the breach's edges
    face(L, 80, 0, "cont", "open")
    _broken_end(L, 80, "r")
    face(L, 96, 0, "open", "cont")
    _broken_end(L, 96, "l")
    s.names = {"face": (0, 0), "top_we": (1, 0), "top_n": (2, 0), "top_w": (3, 0),
               "top_e": (4, 0), "breach_r": (5, 0), "breach_l": (6, 0)}
    return s


CRACK_V1 = ["...k....",
            "...kl...",
            "..k.l...",
            "..kl..k.",
            "...k.kl.",
            "...kkl..",
            "....k...",
            "....kl.."]
CRACK_V2 = ["....k...",
            "...kl...",
            "...k....",
            "..kl....",
            "..k..k..",
            ".kl.k...",
            ".k.kl...",
            "k..k...."]
CRACK_D = ["........",
           "kk......",
           ".lkk....",
           "...lk.k.",
           "....kk..",
           ".....lk.",
           ".......k",
           "........"]


def _crack_tile(M, x0, y0, rows, hflip=False):
    blit(M, [r[::-1] for r in rows] if hflip else rows, {"k": "lk", "l": "ls5"}, x0, y0)


def _broken_end(L, x0, side):
    """Knock the end off a face: blocks gone in a jagged line, rubble at its foot."""
    X = (lambda v: v) if side == "l" else (lambda v: 15 - v)
    edge = [3, 4, 2, 5, 6, 4, 3, 5, 7, 6, 4, 5, 6, 8, 7, 9]    # how deep it's broken, per row
    for y in range(2, 15):
        d = edge[y]
        for i in range(d):
            L.px(x0 + X(i), y, "lk" if i < d - 1 else "ls1")
        L.px(x0 + X(d), y, "ls5" if side == "r" else "ls4")
    # rubble at the foot
    for (x, y, c) in ((1, 13, "ls4"), (2, 12, "ls5"), (3, 14, "ls3"), (0, 14, "ls4"),
                      (4, 13, "ls2"), (2, 14, "ls5")):
        L.px(x0 + X(x), y, c)


# --- doorways: jambs, the labrys seal, the sun and moon gates --------------

def _jamb(L, x0, side, emblem=None):
    """A face whose door side (side: 'r' if the doorway is east of it) has a
    dressed doorpost; emblem: 'sun' or 'moon' carved high on the post."""
    face(L, x0, 0, "cont" if side == "r" else "inner", "inner" if side == "r" else "cont")
    X = (lambda v: 15 - v) if side == "r" else (lambda v: v)
    for y in range(2, 16):
        for i, c in enumerate(("ls1", "ls5", "ls6", "ls4", "ls2") if side == "l" else
                              ("ls1", "ls3", "ls4", "ls5", "ls2")):
            if y >= 4 or i >= 3:
                L.px(x0 + X(i), y, c)
    for y in range(2, 4):
        for i in range(5):
            L.px(x0 + X(i), y, ("ls6", "ls6", "ls5", "ls4", "ls4")[i] if y == 3 else "ls5")
    if emblem == "sun":
        blit(L, [".w.w.", "wwwww", ".www.", "wwwww", ".w.w."], {"w": "lw1"}, x0 + X(0) + (-5 if side == "r" else 1), 6)
        L.px(x0 + X(0) + (-3 if side == "r" else 3), 8, "lj")
    elif emblem == "moon":
        blit(L, [".DDD.", "DD...", "D....", "DD...", ".DDD."], {"D": "ld1"}, x0 + X(0) + (-5 if side == "r" else 1), 6)


def doorways(gates=True):
    """Jambs for every doorway in a face row, and the closed doors that go
    between them: the labrys seal, a bronze grate, and (Ring II) the sun and
    moon gates."""
    names = ["jamb_l", "jamb_r", "seal", "grate"] + (["sun", "moon"] if gates else [])
    s = Struct("doorways", "Doorways: jambs, the labrys seal, a grate" +
               (", the sun and moon gates" if gates else ""), len(names), 1,
               walk=["X" * len(names)],
               notes="Doorways in a face row, one cell wide: lay `jamb_l`, the door, `jamb_r`. "
                     "(0, 1) the jambs, dressed doorposts; (2) `seal`: a bronze door with a "
                     "labrys-shaped socket (the Labrys opens it: EventScript_IchorLabrysSeal; "
                     "swap it for the ring floor, or stand the seal object on the floor between "
                     "the jambs instead); (3) `grate`: a bronze grille in a doorway, for a view "
                     "through (Ring II's lattice) or a locked way." +
                     (" (4) `sun`: the sun gate's stone door, carved with a rayed disc, open "
                      "06:00-19:59; (5) `moon`: the moon gate's, carved with a crescent, open "
                      "20:00-05:59 (gettimeofday in ON_LOAD, LABYRINTH.md §5.5)." if gates else "")
                     + " Open, a door is the ring floor for its parity, between its jambs.")
    L = s.B
    _jamb(L, 0, "r")
    _jamb(L, 16, "l")
    # the labrys seal: a bronze door in a dark doorway
    face(L, 32, 0, "inner", "inner")
    L.rect(32 + 1, 5, 14, 11, "lk")
    blit(s.M, ["kkkkkkkkkkkkkk",
               "k443333333332k",
               "k4kkkkkkkkkk1k",
               "k3k22222222k1k",
               "k3k2k2222k2k1k",
               "k3k2kk22kk2k1k",
               "k3k2k4kk4k2k1k",
               "k3k2kk22kk2k1k",
               "k3k2k2222k2k1k",
               "k3k22222222k1k",
               "k2kkkkkkkkkk0k"], BZ, 33, 5)
    # the double axe in the middle, raised
    blit(s.M, ["4...3", "44.33", "44k33", "44.33", "4...3"], BZ, 38, 7)
    for (x, y) in ((35, 7), (44, 7), (35, 13), (44, 13)):
        s.M.px(x, y, "bz4")
    # a bronze grate in a doorway
    face(L, 48, 0, "inner", "inner")
    L.rect(49, 5, 14, 11, "lk")
    for y in range(5, 16):
        for x in range(49, 63):
            if (x - 49) % 3 == 1:
                s.M.px(x, y, "bz2" if y % 4 else "bz3")
            if (y - 5) % 5 == 0:
                s.M.px(x, y, "bz1")
    for x in range(49, 63):
        s.M.px(x, 5, "bz3")
    if gates:
        _stone_door(L, 64, "sun")
        _stone_door(L, 80, "moon")
    s.names = {n: (i, 0) for i, n in enumerate(names)}
    return [s]


def _stone_door(L, x0, kind):
    face(L, x0, 0, "inner", "inner")
    for y in range(5, 16):
        for x in range(1, 15):
            c = "ls4"
            if x == 1 or y == 5:
                c = "ls5"
            elif x == 14 or y == 15:
                c = "ls2"
            L.px(x0 + x, y, c)
    if kind == "sun":
        # a rayed disc in raised relief, gilded
        blit(L, ["......6......",
                 "..6...6...6..",
                 "...6.....6...",
                 ".....jjj.....",
                 "....jwwwj....",
                 "666.jwwwj.666",
                 "....jwwwj....",
                 ".....jjj.....",
                 "...3.....3...",
                 "..3...3...3..",
                 "......3......"], ST, x0 + 1, 5)
    else:
        for y in range(5, 16):
            for x in range(1, 15):
                d1 = math.hypot(x - 7.5, y - 10.0)
                d2 = math.hypot(x - 9.5, y - 9.0)
                if d1 <= 4.4 and d2 > 3.6:
                    L.px(x0 + x, y, "ld1" if x < 7 else "ld0")
                elif d1 <= 5.2 and d2 > 4.4 and x < 8:
                    L.px(x0 + x, y, "ls6")
        for (x, y) in ((11, 6), (12, 13), (3, 6)):
            L.px(x0 + x, y, "ld1")


# --- webs (Ring III) --------------------------------------------------------

def _web(M, x0, ox, oy, rays, rings, reach=15):
    """Radial strands from an anchor point (ox, oy), joined by sagging rings."""
    pts = {}
    for k, ang in enumerate(rays):
        for t in range(1, reach + 1):
            x = round(ox + math.cos(ang) * t)
            y = round(oy + math.sin(ang) * t)
            if 0 <= x < 16 and 0 <= y < 16:
                pts[(x, y)] = "ls6"
    for r in rings:
        for a0, a1 in zip(rays, rays[1:]):
            for i in range(9):
                a = a0 + (a1 - a0) * i / 8
                sag = 0.5 * math.sin(math.pi * i / 8)
                x = round(ox + math.cos(a) * (r + sag))
                y = round(oy + math.sin(a) * (r + sag))
                if 0 <= x < 16 and 0 <= y < 16:
                    pts.setdefault((x, y), "ls5")
    for (x, y), c in pts.items():
        M.px(x0 + x, y, c)


def webs():
    """Web anchors (Ring III, Ariados country): webbing on the walls either side
    of a web curtain (the curtain itself is an object, EventScript_IchorCobweb)."""
    s = Struct("webs", "Webs anchored on the walls", 6, 1, walk=["XXXXXX"],
               notes="Webbing anchored on Ring III's walls, either side of a web curtain (the "
                     "curtain is an object on the floor between them, burned with the Torch: "
                     "EventScript_IchorCobweb). (0) `face`: on a face, webbing hung from its "
                     "coping, for a curtain south of it; (1) `top_n`: on a wall top's north "
                     "rim, for a curtain north of it; (2) `top_e`: on a top's east rim, for a "
                     "curtain east of it; (3) `top_w`: west; (4) `face_l`, (5) `face_r`: a "
                     "face's corner thick with old web, for dead ends. All block.")
    L, M = s.B, s.M
    face(L, 0, 0)
    _web(M, 0, 8, 3, [math.radians(a) for a in (20, 55, 90, 125, 160)], [4, 8], reach=12)
    top(L, 16, 0, n=True)
    _web(M, 16, 8, 2, [math.radians(a) for a in (-160, -125, -90, -55, -20)], [3, 6], reach=4)
    for x in (2, 5, 8, 11, 14):
        M.px(16 + x, 0, "ls6")
        M.px(16 + x, 1, "ls5")
    top(L, 32, 0, e=True)
    _web(M, 32, 13, 8, [math.radians(a) for a in (-60, -30, 0, 30, 60)], [3, 6], reach=4)
    top(L, 48, 0, w=True)
    _web(M, 48, 2, 8, [math.radians(a) for a in (120, 150, 180, 210, 240)], [3, 6], reach=4)
    face(L, 64, 0, "inner", "cont")
    _web(M, 64, 0, 4, [math.radians(a) for a in (-10, 15, 40, 65, 90)], [4, 8, 12])
    face(L, 80, 0, "cont", "inner")
    _web(M, 80, 15, 4, [math.radians(a) for a in (90, 115, 140, 165, 190)], [4, 8, 12])
    s.names = {"face": (0, 0), "top_n": (1, 0), "top_e": (2, 0), "top_w": (3, 0),
               "face_l": (4, 0), "face_r": (5, 0)}
    return s


# --- glow-marks (Ring III's back way) ---------------------------------------

LABRYS_MARK = [".......",
               "g.....g",
               "gg.g.gg",
               "ggggggg",
               "gg.g.gg",
               "g..g..g",
               "...g..."]
ARROW_MARK = ["...g...",
              "..ggg..",
              ".g.g.g.",
              "g..g..g",
              "...g...",
              "...g...",
              "...g..."]


def glow_marks():
    """Daedalus's private marks, painted on the wall tops in the latent glow
    paint `lg`: by torchlight the very stone they're on (palettes as drawn), and
    the only thing on screen when the torch is doused (the glow set)."""
    s = Struct("glow", "Glow-marks: Daedalus's labrys signs", 8, 1, walk=["XXXXXXXX"],
               notes="Daedalus's marks for his own way through Ring III (LABYRINTH.md §6, the "
                     "back way): labrys signs and arrows painted on the wall tops in the latent "
                     "glow paint, invisible by torchlight and bright in the doused `glow/` "
                     "palettes. Use them in place of the plain kit top of the same name: "
                     "(0) `top`, (1) `top_n`, (2) `top_w`, (3) `top_e`, (4) `top_we` (on a "
                     "one-cell wall); (5-7) `arrow_n`, `arrow_w`, `arrow_e` on a `top`, "
                     "pointing the way (an arrow south is `arrow_n` turned: use `top` there). "
                     "All block.")
    L, M = s.B, s.M
    # each mark sits inside one 8 x 8 tile, clear of the rims, so every mark is
    # the same tile wherever it's painted
    cells = [("top", {}, (5, 5)), ("top_n", {"n": True}, (1, 9)), ("top_w", {"w": True}, (9, 1)),
             ("top_e", {"e": True}, (1, 1))]
    for i, (nm, k, (mx, my)) in enumerate(cells):
        top(L, i * 16, 0, **k)
        blit(M, LABRYS_MARK, {"g": "lg"}, i * 16 + mx - (4 if nm == "top" else 0),
             my - (4 if nm == "top" else 0))
    # a thin wall's top has room only for a stroke down its middle
    top(L, 64, 0, w=True, e=True)
    for y in (1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14):
        M.px(64 + 7, y, "lg")
    for y in (2, 6, 10, 14):
        M.px(64 + 6, y, "lg")
        M.px(64 + 8, y, "lg")
    top(L, 80, 0)
    blit(M, ARROW_MARK, {"g": "lg"}, 80 + 1, 1)
    top(L, 96, 0)
    blit(M, [r[::-1] for r in _rot(ARROW_MARK)], {"g": "lg"}, 96 + 1, 1)
    top(L, 112, 0)
    blit(M, _rot(ARROW_MARK), {"g": "lg"}, 112 + 1, 1)
    s.names = {"top": (0, 0), "top_n": (1, 0), "top_w": (2, 0), "top_e": (3, 0),
               "top_we": (4, 0), "arrow_n": (5, 0), "arrow_w": (6, 0), "arrow_e": (7, 0)}
    return s


def _rot(rows):
    """Rotate an ASCII grid 90 degrees clockwise."""
    return ["".join(rows[len(rows) - 1 - j][i] for j in range(len(rows))) for i in range(len(rows[0]))]


# --- niches (Ring V) ----------------------------------------------------------

def niches():
    """The back wall of a niche: a one-cell alcove off a corridor where the player
    can duck out of Asterion's line (LABYRINTH.md §5.3)."""
    s = Struct("niche", "Niches: the back of an alcove, plain and a shrine", 3, 1, walk=["XXX"],
               notes="A niche is one cell cut into a wall at least two cells thick: its floor "
                     "is ring floor (walkable, threaded), and the cell north of it, which the "
                     "autotile makes `face_ii`, is the niche's back: put one of these there. "
                     "(0) `back`: an arched recess in shadow; (1) `shrine`: a clay lamp, lit, "
                     "and a little Minoan goddess, arms raised, on a ledge (Ring V's niche "
                     "shrine, a landmark); (2) `lamp_out`: the same, its lamp burned out.")
    L, M = s.B, s.M
    for i in range(3):
        x0 = i * 16
        face(L, x0, 0, "inner", "inner")
        # the alcove's back, in shadow under its arch
        for y in range(2, 16):
            for x in range(1, 15):
                ax = abs(x - 7.5)
                if y < 2 + max(0, ax - 3.5) * 0.9 and ax > 3.5:
                    continue
                c = L.get(x0 + x, y)
                darker = {"ls4": "ls3", "ls3": "ls2", "ls6": "ls4", "ls2": "ls1", "ls1": "lk"}
                L.px(x0 + x, y, darker.get(c, c))
        # the arch's rim
        for x in range(1, 15):
            ax = abs(x - 7.5)
            y = round(2 + max(0, ax - 3.5) * 0.9)
            L.px(x0 + x, y, "ls5" if x < 8 else "ls4")
        if i:
            # a ledge with a lamp and a figurine
            for x in range(3, 13):
                L.px(x0 + x, 11, "ls5")
                L.px(x0 + x, 12, "ls3")
            blit(M, ["..k..", ".kak.", "kbbak", ".kak.", "kbbbk", "kbaak", ".kkk."],
                 {"k": "ink", "a": "fc0", "b": "fc1"}, x0 + 3, 4)
    # the goddess (terracotta) and the lamp
    for x0, lit in ((16, True), (32, False)):
        blit(M, ["k...k", "bk.kb", ".bkb.", "..b..", ".kbk.", "kbabk", "kaaak"],
             {"k": "ink", "a": "fc0", "b": "fc1"}, x0 + 3, 4)
        blit(M, [".kkkk..", "kbbbbak", ".kaaak."], {"k": "ink", "a": "fc0", "b": "fc1"},
             x0 + 8, 8)
        if lit:
            blit(M, ["..c", ".cy", ".yw", "cyc"], FI, x0 + 11, 4)
    s.names = {"back": (0, 0), "shrine": (1, 0), "lamp_out": (2, 0)}
    return s


# --------------------------------------------------------------------------
# Ring V: skylight pools
# --------------------------------------------------------------------------

def pools():
    return KIT.thread_block(
        "pools", "Skylight pools (sun and moon) and the herald plate, with their thread twins",
        [("sun_l", "sun", "l", "MB_ICHOR_LIGHT_POOL"), ("sun_r", "sun", "r", "MB_ICHOR_LIGHT_POOL"),
         ("moon_l", "moon", "l", "MB_ICHOR_LIGHT_POOL"), ("moon_r", "moon", "r", "MB_ICHOR_LIGHT_POOL"),
         ("plate", _plate, None, None)],
        section="rings",
        notes="Ring V's four skylight pools (LABYRINTH.md §5.2): the ring floor where a "
              "square of sky falls on it, each cell `MB_ICHOR_LIGHT_POOL` (Asterion sees 7 "
              "tiles into it by day, 5 by night), twins and all. By day lay `sun_l` / "
              "`sun_r` (x + y even / odd), by night `moon_l` / `moon_r`: in ON_LOAD, "
              "gettimeofday picks which set the pool's cells get, and registers that pair "
              "beside `dark_l` and `dark_r`: `Ichor_AddThreadFloor(sun_l, sun_l + 1)` and so "
              "on (four floors: the engine's limit). A pool is a rectangle of whole cells, "
              "the shape of the skylight. " + PLATE_NOTE)


# --------------------------------------------------------------------------
# Ring II: the herald plates
# --------------------------------------------------------------------------

def _plate(L, x0, y0):
    """A herald gate's bronze plate, set flush in the floor, a herald's staff
    engraved on it (Hermes's ring)."""
    blit(L, ["kkkkkkkkkkkkkkkk",
             "k43333333333332k",
             "k32222222222221k",
             "k32422222222421k",
             "k32222k0k222221k",
             "k3222k030k22221k",
             "k32222k0k222221k",
             "k3220k000k02221k",
             "k32220202022221k",
             "k32222202222221k",
             "k32222202222221k",
             "k32222202222221k",
             "k32422202222421k",
             "k32222222222221k",
             "k21111111111110k",
             "kkkkkkkkkkkkkkkk"], BZ, x0, y0)


PLATE_NOTE = ("Last, Ring II's **herald plate** (LABYRINTH.md §6, Ring II): `plate`, a bronze "
              "plate set flush in the floor, a herald's staff engraved on it, and its ten "
              "twins. Step on it and its gate opens for ten steps (a coord event; the gate is "
              "`doorways` `grate` between jambs, open = ring floor). The player runs from the "
              "plate through the gate, so the plate takes thread: register "
              "`Ichor_AddThreadFloor(plate, plate + 1)` beside `dark_l` and `dark_r`. It "
              "covers its cell, so it has no parity. The last cell is void.")


# --------------------------------------------------------------------------
# Frescoes: the dance's steps (Rings IV-VII)
# --------------------------------------------------------------------------

FR = {"k": "ink", "w": "fw", "0": "fb0", "1": "fb1", "2": "fb2", "3": "fb3", "y": "fy0",
      "Y": "fy1", "r": "fr", "s": "fs", "c": "fcr", "q": "fq", "p": "fp", "g": "fg0", "G": "fg1"}

# the five symbols of the dancing floor (LABYRINTH.md §5.7), 7 x 6, held aloft
SYMBOLS = {
    "X": [".......", "Y.....Y", "YY.k.YY", "YYYkYYY", "YY.k.YY", "Y..k..Y"],   # double axe
    "W": [".www...", "w...w..", "w.ww.w.", "w..w..w", ".w....3", "..www3."],   # a curling wave
    "L": ["...w...", ".w.w.w.", ".wwwww.", "..www..", "...g...", "...g..."],   # lily
    "R": ["..rrr..", ".rYYYr.", "rYyrYYr", "rYrYrYr", ".rYYYr.", "..rrr.."],   # rosette
    "S": ["...Y...", "...Y...", "YYYwYYY", "...Y...", "...Y...", "......."],   # star
}
# a Minoan dancer, arms raised: 9 rows tall
DANCER = ["k.....k",
          "s.kk..s",
          ".skks.s",
          "..ss.s.",
          "..rr...",
          ".rYYr..",
          ".ryyrr.",
          "rYYYYYr",
          "..s.s.."]


def fresco_panel(L, x0, y0, sym, faded=False):
    """One step of the dance as a 16 x 16 fresco panel: a dancer holding the
    step's symbol overhead, on a blue ground between dark bands."""
    for y in range(16):
        for x in range(16):
            if faded:
                c = "fcr" if (x * 3 + y * 7) % 11 else "fq"
            else:
                c = "fb1" if y < 14 else "fb0"
            if y == 0 or y == 15:
                c = "fb0" if not faded else "fq"
            L.px(x0 + x, y0 + y, c)
    if faded:
        # a silhouette, flaking: the ghost of a dancer and a blot over her head
        blit(L, ["..qqq..", ".q...q.", "..qqq.."], {"q": "fq"}, x0 + 5, y0 + 2)
        blit(L, DANCER, {"k": "fq", "s": "fq", "r": "fq", "Y": "fq", "y": "fq"}, x0 + 5, y0 + 6)
        for (x, y) in ((2, 4), (12, 9), (3, 11), (13, 3), (9, 13)):
            L.px(x0 + x, y0 + y, "fw")
        return
    blit(L, SYMBOLS[sym], FR, x0 + 5, y0 + 1)
    blit(L, DANCER, FR, x0 + 4, y0 + 6)
    # the ground's border: a row of white dots
    for x in range(1, 16, 3):
        L.px(x0 + x, y0 + 14, "fw")


def fresco_bay(key, title, steps, notes, faded=False, section="rings"):
    """An arcade bay (3 x 3, as `arcade` `bay_l` `bay_m` `bay_r`) whose recess is
    painted with three steps of the dance."""
    s = Struct(key, title, 3, 3, walk=["XXX"] * 3, section=section, notes=notes)
    ins = A.arch(s.B, 0, 48)
    A.recess(s.B, 0, 48, ins)
    for i, sym in enumerate(steps):
        fresco_panel(s.B, i * 16, 24, sym, faded=faded)
    s.names = {f"{c}{r}": (i, r) for r in range(3) for i, c in enumerate("lmr")}
    return s


def fresco_v():
    return fresco_bay(
        "fresco_v", "Fresco: the dance's steps 4-6 (Ring V)", "RWL",
        "Ring V's fresco niche (LABYRINTH.md §5.7): three dancers holding up the dance's "
        "steps 4-6, rosette, wave, lily, in a three-cell bay of the arcade (lay it between "
        "piers as `arcade`'s bay). Each step is one bay column, so the order reads left to "
        "right.")


# --------------------------------------------------------------------------

def build():
    out = []
    out += braziers()
    out += hearth()
    out.append(pools())
    out.append(cracked())
    out += doorways()
    out.append(webs())
    out.append(glow_marks())
    out.append(niches())
    out.append(fresco_v())
    return out
