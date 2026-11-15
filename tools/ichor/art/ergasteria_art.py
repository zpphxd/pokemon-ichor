#!/usr/bin/env python3
"""Pixel art for the ergasteria tileset: Phase 2's working interiors.

ergasteria ("workshops") is the secondary for rooms where people work: the
inns, the mint, the forge, the potter's, the tavern. Batch 1 draws Aegina's
three homes (the inn, the mint and Aiakides's house); batch 2 adds Emporion's
workshops to the same set.

It is built the way oikia is (design/phase1/TILES_oikia.md): hand-drawn
character grids, one character per color, '.' for clear, in seven palettes of
at most 15 colors whose values appear in no aethos palette. The furniture a
working room shares with a home (tables, chairs, jars, the hearth, the mat) is
taken from oikia_art.py pixel for pixel, so the rooms match the slice exactly;
ergasteria's palettes hold every color those pieces use.

Palettes (design/phase2/TILES_ergasteria.md has the plan for batch 2):
  wall    oikia's: beams, whitewash, red and Aegean dados, shutters, sky
  floor   terracotta and limestone (oikia's), a dark pebble and three earth
          tones for pebble mosaics and beaten-earth workshop floors
  wood    oikia's: furniture woods, bronze fittings, linen, cloth
  clay    oikia's: pottery, hearth stone, fire, soot, slip
  iron    oikia's rug colors plus iron and silver, a lit wood: the anvils,
          dies and tongs; red, orange and yellow double as hot metal
  nature  oikia's: plants, wicker, fish, rope
  bronze  oikia's: bronze, flame, water, marble

ergasteria_build.py assembles the pieces into metatiles;
tools/ichor/maps/aegina_homes.py lays out the rooms.
"""
import copy
import math

import numpy as np

import oikia_art as O

INK = O.INK

PALETTES = copy.deepcopy(O.PALETTES)

# floor: oikia's boards go (no upper storeys here); in their place a dark
# pebble for mosaics and three earth tones for beaten-earth floors (batch 2).
for ch in ("W", "m", "n", "j"):
    del PALETTES["floor"][ch]
PALETTES["floor"].update({
    "K": (64, 48, 48),     # dark pebble
    "e": (160, 128, 88),   # beaten earth
    "E": (128, 96, 72),    # earth, low
    "h": (184, 152, 112),  # earth, lit
})

# iron: oikia's "cloth" palette keeps the two rugs' colors and gains iron,
# silver and a lit wood. The rug reds and saffron double as hot metal.
PALETTES["iron"] = {
    "k": INK,
    "R": (144, 40, 32),    # madder, dark / iron, red-hot core
    "r": (192, 64, 40),    # madder / red heat
    "o": (224, 168, 72),   # ochre / orange heat
    "y": (248, 208, 120),  # saffron / yellow heat
    "c": (240, 224, 184),  # undyed wool
    "i": (40, 56, 112),    # indigo
    "u": (72, 104, 168),   # blue
    "U": (128, 160, 208),  # blue, lit
    "n": (96, 64, 48),     # brown / wood, dark
    "N": (144, 104, 72),   # wood, lit
    "I": (64, 64, 80),     # iron, dark
    "s": (104, 104, 120),  # iron
    "S": (160, 160, 168),  # iron, lit
    "w": (216, 216, 224),  # silver
}
del PALETTES["cloth"]

PALETTE_ORDER = ["wall", "floor", "wood", "clay", "iron", "nature", "bronze"]


def grid(pal, text, w=None, h=None):
    """Parse a character grid into an (h, w, 4) RGBA array ('.' = clear)."""
    rows = [r.rstrip() for r in text.strip("\n").split("\n")]
    w = w or max(len(r) for r in rows)
    h = h or len(rows)
    assert len(rows) <= h, f"{len(rows)} rows > {h}"
    out = np.zeros((h, w, 4), np.uint8)
    colors = PALETTES[pal]
    for y, row in enumerate(rows):
        assert len(row) <= w, f"row {y} is {len(row)} wide > {w}: {row!r}"
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            if ch not in colors:
                raise ValueError(f"{pal}: unknown char {ch!r} at ({x},{y}) in {row!r}")
            out[y, x, :3] = colors[ch]
            out[y, x, 3] = 255
    return out


def rows_of(g):
    return "\n".join("".join(r) for r in g)


def mirror(half):
    """Rows drawn as left halves; return them mirrored to full width."""
    return [r + r[::-1] for r in half]


def outline(g, solid, ink="k"):
    """Draw `ink` on clear pixels that touch a solid one (4-neighbours)."""
    H, W = len(g), len(g[0])
    out = [row[:] for row in g]
    for y in range(H):
        for x in range(W):
            if solid(x, y):
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and solid(nx, ny):
                    out[y][x] = ink
                    break
    return out


def hflip(img):
    return img[:, ::-1].copy()


# --------------------------------------------------------------------------
# Floors, walls, void, rugs. oikia's terracotta and limestone flags are reused
# as they are; the strongroom's ashlar wall and the inn's gallery are new.
# --------------------------------------------------------------------------

FLOORS = {
    "terracotta": O.FLOORS["terracotta"],
    "flags": O.FLOORS["flags"],
}


def wall_stone():
    """Ashlar for the mint's strongroom: the ceiling beam, then three courses
    of squared limestone blocks with staggered joints, on a dark plinth."""
    rows = ["k" * 16, "2" * 16, "3" * 16, "2" * 16, "1" * 16, "S" * 16]
    joints = [4, 12, 6]
    for c, jx in enumerate(joints):
        top = 6 + c * 8
        for y in range(top, top + 8):
            r = y - top
            row = []
            for x in range(16):
                if r == 7:
                    ch = "S"                      # bed joint
                elif x == jx:
                    ch = "S"                      # head joint
                elif x == (jx + 1) % 16:
                    ch = "p"                      # lit edge right of the joint
                elif r == 0:
                    ch = "p"                      # lit top edge of the course
                elif r == 6:
                    ch = "S" if (x + c) % 5 == 0 else "s"
                else:
                    ch = "s"
                row.append(ch)
            rows.append("".join(row))
    # tooling marks and a few chips
    rows = [list(r) for r in rows]
    for (x, y, c) in [(9, 8, "p"), (2, 10, "S"), (14, 17, "p"), (7, 19, "S"), (11, 25, "p"), (1, 26, "S")]:
        rows[y][x] = c
    rows = rows[:30]
    rows.append(list("1" * 16))
    rows.append(list("k" * 16))
    return grid("wall", "\n".join("".join(r) for r in rows))


def wall_gallery():
    """The inn courtyard's back wall, three blocks tall: the eave beam and
    rafter ends, the whitewashed upper storey where the guest rooms open,
    then the shaded ground floor under the gallery with the inn's blue dado.
    The gallery's timber (posts, rail, doors) is drawn over it as stamps."""
    rows = []
    rows.append("k" * 16)
    rows.append("2" * 16)
    rows.append("3" * 16)
    rows.append("2" * 16)
    rows.append("1" * 16)
    rows.append("s23321sss23321ss"[:16])
    rows.append("s12211sss12211ss"[:16])
    rows.append("ps1111spps1111sp"[:16])
    rows.append("pppssssppppssssp"[:16])
    for y in range(9, 26):
        rows.append("p" * 16)
    for y in range(26, 32):
        rows.append("s" * 16)
    # ground floor, in the gallery's shadow
    rows.append("1" * 16)
    rows.append("S" * 16)
    for y in range(34, 39):
        rows.append("S" * 16)
    rows.append("s" * 16)
    rows.append("B" * 16)
    for y in range(6):
        rows.append("".join("B" if c == "#" else "b" for c in O.KEY8[y + 1] * 2))
    rows.append("k" * 16)
    rows = [list(r) for r in rows]
    for (x, y, c) in [(3, 11, "w"), (10, 14, "w"), (13, 20, "s"), (6, 22, "w"), (1, 17, "s"), (12, 10, "w"),
                      (5, 35, "s"), (12, 37, "s")]:
        rows[y][x] = c
    assert len(rows) == 48, len(rows)
    return grid("wall", "\n".join("".join(r) for r in rows))


WALLS = {
    "red": O.WALLS["red"],
    "blue": O.WALLS["blue"],
    "stone": wall_stone(),
    "gallery": wall_gallery(),
}

VOID = O.VOID
RUGS = {"red": O.RUGS["red"], "blue": O.RUGS["blue"]}

# --------------------------------------------------------------------------
# Stamps. Same contract as oikia's: w, h in metatiles; walk cells the player
# may stand on; behavior per cell; `top` art over the player; `flatten` puts
# the art in the bottom layer (it must then cover its cells opaquely or share
# the base's palette).
# --------------------------------------------------------------------------

STAMPS = {}

# Shared furniture, taken from oikia pixel for pixel.
SHARED = ["window", "niche", "herbs", "jar_shelf", "honey_shelf",
          "kline", "klismos_r", "klismos_l", "stool", "table", "table_round",
          "amphora", "amphora_plain", "pithos", "pots", "hearth", "soot",
          "myrtle", "fish_basket", "knucklebones", "lampstand", "column", "mat"]
for _name in SHARED:
    STAMPS[_name] = dict(O.STAMPS[_name], note=O.STAMPS[_name]["note"], source="oikia")


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note=""):
    """w, h in metatiles. walk: cells (cx, cy) the player may stand on.
    behavior: {(cx, cy): 'MB_...'}."""
    img = art if isinstance(art, np.ndarray) else grid(pal, art, w * 16, h * 16)
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    STAMPS[name] = {
        "pal": pal,
        "img": img,
        "top": grid(pal, top, w * 16, h * 16) if top else None,
        "w": w,
        "h": h,
        "walk": set(walk),
        "behavior": dict(behavior or {}),
        "flatten": flatten,
        "note": note,
        "source": "ergasteria",
    }


# ===========================================================================
# The inn
# ===========================================================================

def _cistern_art():
    """A marble well-head (puteal) over the courtyard's rain cistern, seen from
    above and in front: the rim's top ring, dark water inside it, a fluted
    drum, a rope over the lip."""
    W, H = 32, 32
    cx, cyt, cyb, rx, ry = 16.0, 10.5, 22.5, 13.5, 7.0
    g = [["." for _ in range(W)] for _ in range(H)]

    def ell(px, py, cy, a, b):
        return ((px - cx) / a) ** 2 + ((py - cy) / b) ** 2 <= 1.0

    def body(x, y):
        px, py = x + 0.5, y + 0.5
        if abs(px - cx) > rx:
            return False
        return ell(px, py, cyt, rx, ry) or ell(px, py, cyb, rx, ry) or cyt <= py <= cyb

    for y in range(H):
        for x in range(W):
            if not body(x, y):
                continue
            px, py = x + 0.5, y + 0.5
            t = (px - cx) / rx
            if ell(px, py, cyt, rx, ry):
                # the rim's top surface, the inner wall, the water
                if ell(px, py + 1.2, cyt, rx - 3.5, ry - 2.6):
                    g[y][x] = "u"
                elif ell(px, py, cyt, rx - 3.0, ry - 2.0):
                    g[y][x] = "n" if py < cyt else "m"
                else:
                    g[y][x] = "M" if py < cyt + 2 else "m"
            else:
                # the drum: lit left, shaded right, a moulding near the foot
                arc = cyb + ry * math.sqrt(max(0.0, 1 - t * t))
                if arc - 4.5 <= py <= arc - 3.5:
                    g[y][x] = "n"
                elif arc - 3.5 < py:
                    g[y][x] = "M" if t < -0.4 else ("m" if t < 0.35 else "n")
                else:
                    shade = "M" if t < -0.5 else ("m" if t < 0.3 else "n")
                    # flutes
                    if x % 3 == 0 and shade != "n":
                        shade = "m" if shade == "M" else "n"
                    g[y][x] = shade
    # water glints
    for (x, y, c) in [(11, 9, "U"), (12, 9, "a"), (13, 9, "U"), (16, 11, "U"), (19, 10, "U"), (20, 10, "a"),
                      (9, 10, "U"), (14, 12, "U"), (18, 12, "U"), (22, 11, "U")]:
        if g[y][x] == "u":
            g[y][x] = c
    g = outline(g, lambda x, y: g[y][x] != ".")
    # the bucket rope, looped over the near lip and hanging down the drum
    for (x, y, c) in [(23, 6, "z"), (23, 7, "z"), (24, 8, "z"), (24, 9, "b"), (24, 10, "z"),
                      (25, 11, "b"), (25, 12, "z"), (25, 13, "b"), (25, 14, "z"), (25, 15, "b"),
                      (25, 16, "z"), (25, 17, "b"), (25, 18, "z")]:
        g[y][x] = c
    # a bronze dipper hanging on the rope
    for (x, y, c) in [(24, 19, "k"), (25, 19, "k"), (26, 19, "k"), (23, 20, "k"), (24, 20, "y"), (25, 20, "b"),
                      (26, 20, "z"), (27, 20, "k"), (23, 21, "k"), (24, 21, "b"), (25, 21, "b"), (26, 21, "z"),
                      (27, 21, "k"), (24, 22, "k"), (25, 22, "k"), (26, 22, "k")]:
        g[y][x] = c
    return rows_of(g)


stamp("cistern", "bronze", _cistern_art(), 2, 2,
      note="the courtyard's rain cistern: a fluted marble well-head over dark water, a dipper on its rope")


def _turtle_mosaic():
    """A pebble mosaic of a sea turtle, Aegina's coin, in a frame of white
    beads: dark pebbles outline it, terracotta pebbles make its shell and a row
    of white ones runs down its spine, as on the island's staters. Symmetric
    left to right, so half its tiles are flips."""
    W, H = 64, 48
    c = W / 2

    def hsh(x, y):
        # A speckle that repeats every 8 pixels and mirrors left to right,
        # so the plain field costs one tile, flipped.
        x = min(x, W - 1 - x) % 8
        y = y % 8
        return (x * 73 + y * 151 + (x * y) * 7) % 23

    def rot_ell(px, py, ex, ey, a, b, ang):
        ca, sa = math.cos(ang), math.sin(ang)
        dx, dy = px - ex, py - ey
        u = dx * ca + dy * sa
        v = -dx * sa + dy * ca
        return (u / a) ** 2 + (v / b) ** 2

    def part(px, py):
        """Which part of the turtle a pixel centre falls in, or None."""
        mx = c - abs(px - c)             # fold onto the left half
        if rot_ell(mx, py, c, 25.0, 10.5, 12.5, 0) <= 1:
            return "shell"
        if rot_ell(mx, py, c, 10.0, 3.8, 4.4, 0) <= 1:
            return "head"
        if abs(mx - c) <= 2.6 and 12.5 <= py <= 15.0:
            return "neck"
        if rot_ell(mx, py, c - 12.0, 17.5, 9.0, 3.2, math.radians(-28)) <= 1:
            return "flipper"
        if rot_ell(mx, py, c - 9.0, 36.0, 4.6, 2.4, math.radians(35)) <= 1:
            return "rear"
        if abs(mx - c) <= max(0.0, (41.5 - py) * 0.7) and 37.0 <= py <= 41.5:
            return "tail"
        return None

    g = [["l"] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            d = min(x, y, W - 1 - x, H - 1 - y)
            h = hsh(x, y)
            if d == 0:
                g[y][x] = "K"
            elif d == 1:
                g[y][x] = "v"
            elif d == 2:
                g[y][x] = "L" if ((min(x, W - 1 - x) + min(y, H - 1 - y)) % 2 == 0) else "v"
            elif d == 3:
                g[y][x] = "v"
            elif d == 4:
                g[y][x] = "K"
            else:
                g[y][x] = "L" if h == 0 else ("y" if h in (5, 11, 17) else ("q" if h == 9 else "l"))
    inside = [[part(x + 0.5, y + 0.5) for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            p = inside[y][x]
            if p is None:
                continue
            mx = min(x, W - 1 - x)          # the left half
            if p == "shell":
                nx = (mx + 0.5 - c) / 10.5
                ny = (y + 0.5 - 25.0) / 12.5
                r = math.hypot(nx, ny)
                if r > 0.86:
                    g[y][x] = "v"                       # marginal ring
                elif mx >= c - 3:                        # vertebral plates
                    g[y][x] = "v" if y in (17, 22, 27, 32) else "x"
                else:                                    # costal plates
                    if mx == c - 4 or y in (20, 26, 31) and mx < c - 4:
                        g[y][x] = "v"
                    else:
                        g[y][x] = "u" if (y + mx) % 7 else "t"
            elif p in ("head", "neck"):
                g[y][x] = "x"
            elif p == "flipper":
                g[y][x] = "x" if (mx + y) % 5 else "t"
            elif p == "rear":
                g[y][x] = "x"
            elif p == "tail":
                g[y][x] = "u"
    g = outline(g, lambda x, y: inside[y][x] is not None, ink="K")
    # the white beads down the spine, the eyes, a highlight on the head
    for y in (16, 19, 21, 24, 26, 29, 31, 34):
        g[y][int(c) - 1] = "L"
        g[y][int(c)] = "L"
    ci = int(c)
    for (x, y, ch) in [(ci - 3, 8, "K"), (ci + 2, 8, "K"), (ci - 1, 7, "T"), (ci, 7, "T"),
                       (ci - 1, 11, "u"), (ci, 11, "u")]:
        g[y][x] = ch
    return rows_of(g)


stamp("mosaic_turtle", "floor", _turtle_mosaic(), 4, 3,
      walk={(x, y) for x in range(4) for y in range(3)}, flatten=True,
      note="pebble mosaic of a sea turtle, Aegina's coin: terracotta shell, white beads down the spine")


def _gallery(door=False, post=True, blanket=None, lamp=False):
    """One bay of the inn's timber gallery, 1x3 over the 'gallery' wall:
    a post, the guest-room door (or bare wall) behind the balustrade, the
    gallery floor's beam, and the post running down to the courtyard."""
    W, H = 16, 48
    g = [["."] * W for _ in range(H)]

    def put(x, y, ch):
        if 0 <= x < W and 0 <= y < H:
            g[y][x] = ch
    if door:
        # a plank door with a bronze ring, under a lintel
        for y in range(9, 27):
            for x in range(5, 14):
                if y == 9:
                    put(x, y, "k")
                elif y == 10:
                    put(x, y, "d")
                elif x in (5, 13):
                    put(x, y, "k")
                elif x in (6,):
                    put(x, y, "l")
                elif x in (9,):
                    put(x, y, "d")
                elif x == 12:
                    put(x, y, "d")
                else:
                    put(x, y, "m")
        for (x, y, ch) in [(11, 17, "k"), (10, 18, "y"), (12, 18, "z"), (11, 19, "z"), (8, 13, "l"), (7, 21, "l")]:
            put(x, y, ch)
    # balustrade: top rail, balusters, bottom rail
    for x in range(W):
        put(x, 20, "k")
        put(x, 21, "h")
        put(x, 22, "l")
        put(x, 23, "d")
        for y in range(24, 27):
            if x % 4 == 1:
                put(x, y, "k")
            elif x % 4 == 2:
                put(x, y, "l")
            elif x % 4 == 3:
                put(x, y, "d")
        put(x, 27, "k")
        # the gallery floor's beam, joist ends
        put(x, 28, "h")
        put(x, 29, "l")
        put(x, 30, "m")
        put(x, 31, "k")
        put(x, 32, "d")
        put(x, 33, "k")
    for x in (3, 11):
        for y in (29, 30):
            put(x, y, "d")
    if blanket:
        a, b = ("u", "U") if blanket == "blue" else ("r", "R")
        for y in range(19, 31):
            for x in range(4, 13):
                if y == 19 or x in (4, 12):
                    put(x, y, "k")
                elif y < 22:
                    put(x, y, b if y == 20 else a)
                else:
                    put(x, y, "c" if (y % 4 == 1) else a)
        for x in range(4, 13):
            put(x, 31, "k" if x % 2 else ".")
    if post:
        for y in range(5, H):
            put(0, y, "k")
            put(1, y, "h" if y >= 34 else "l")
            put(2, y, "m")
            put(3, y, "k")
        for (x, y, ch) in [(0, 4, "k"), (1, 4, "k"), (2, 4, "k"), (3, 4, "k"), (4, 33, "k"), (4, 34, "d"),
                           (4, 35, "k"), (1, 47, "d"), (2, 47, "d")]:
            put(x, y, ch)
    if lamp:
        # a clay lamp hung from the beam on a cord
        for (x, y, ch) in [(9, 34, "z"), (9, 35, "z"), (9, 36, "z"), (8, 37, "k"), (9, 37, "k"), (10, 37, "k"),
                           (7, 38, "k"), (8, 38, "y"), (9, 38, "b"), (10, 38, "z"), (11, 38, "k"),
                           (8, 39, "k"), (9, 39, "k"), (10, 39, "k"), (11, 37, "y")]:
            put(x, y, ch)
    return rows_of(g)


stamp("gallery_door", "wood", _gallery(door=True), 1, 3,
      note="the inn's timber gallery: a post, a guest-room door behind the balustrade")
stamp("gallery_rail", "wood", _gallery(post=False), 1, 3,
      note="the gallery's balustrade over bare wall")
stamp("gallery_blanket", "wood", _gallery(post=False, blanket="blue"), 1, 3,
      note="a blue blanket airing over the gallery rail")
stamp("gallery_lamp", "wood", _gallery(post=False, lamp=True), 1, 3,
      note="the balustrade, with a clay lamp hung under the gallery")


def _ladder():
    """A timber ladder leaning on the gallery: its tops stand above the rail,
    its foot on the courtyard floor (1x3: gallery, ground floor, floor)."""
    W, H = 16, 48
    g = [["."] * W for _ in range(H)]
    for y in range(12, 44):
        for x in (3, 4, 11, 12):
            g[y][x] = "l" if x in (3, 11) else "m"
        g[y][2] = "k"
        g[y][5] = "k"
        g[y][10] = "k"
        g[y][13] = "k"
    for y in range(15, 43, 5):
        for x in range(6, 10):
            g[y][x] = "k"
            g[y + 1][x] = "h"
            g[y + 2][x] = "d"
            g[y + 3][x] = "k"
    for x in (2, 3, 4, 5, 10, 11, 12, 13):
        g[11][x] = "k"
        g[44][x] = "k"
    g[43][3] = g[43][11] = "d"
    return rows_of(g)


stamp("ladder", "wood", _ladder(), 1, 3,
      note="a timber ladder up to the guest gallery (the loft); its foot stands in the courtyard")

stamp("hearth_floor", "clay", """
................................
................................
..............kk................
.............kYFk...............
............kFYYFk..kk..........
.......kk..kFYYYFk.kFk..........
......kFFk.kFYcYFkkFYFk.........
.....kFYYFkkFYcYYFkFYYFk........
.....kfFYYFkFYYYYFkFYFfk........
....kkfFYYYFFYYYYFFYFfkkk.......
...ktttfFFYYYYYYYYYFffttttk.....
..kttttfFFFYYYYYYYFFfttttttk....
..ktSSaafFFFYYYYYFFFfaaSSSttk...
..ktSaaaddfFFFFFFFFddaaaaSStk...
..ktSaaaFddddfffffddddFaaaSStk..
..ktSafFfFdddddddddddFfFaaSStk..
..ktSaaFfaFfaFFaFfFaaFfaaaSStk..
..ktSaaaaaaaaaaaaaaaaaaaaaSStk..
..ktttttttttttttttttttttttttSk..
..ktSSSSSStSSSSSSStSSSSSSSSSSk..
..kSSSSSSsSSSSSSSsSSSSSSSsSSSk..
..kSSSSSSsSSSSSSSsSSSSSSSsSSSk..
..kssssssssssssssssssssssssssk..
..ktSSstSSSSSstSSSSSSstSSSSStk..
..kSSSsSSSSSSsSSSSSSSsSSSSSSsk..
..kssssssssssssssssssssssssssk..
...kkkkkkkkkkkkkkkkkkkkkkkkkk...
................................
................................
................................
................................
................................
""", 2, 2, note="the common room's hearth: an open fire in a raised stone curb, where the inn eats")


stamp("bench", "wood", """
................................
................................
................................
................................
................................
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
.khhhhhhhhhhhhhhhhhhhhhhhhhhhhk.
.khlllllllllllllllllllllllllllk.
.kmmmmmmmmmmmmmmmmmmmmmmmmmmmdk.
.kddddddddddddddddddddddddddddk.
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
...kmdk..................kmdk...
...kmdk..................kmdk...
...kmdk..................kmdk...
...kkkk..................kkkk...
................................
""", 2, 1, note="a long wooden bench")


# ===========================================================================
# The mint
# ===========================================================================

stamp("anvil", "iron", """
................
.......kk.......
......kwwk......
..kkkkkSSkkkkk..
.kwwwwwwwwwwwSk.
.kSSSSSSSSSSssk.
..ksSSSSSSSsIk..
...kIssssssIk...
....kIsssIIk....
..kkkkkkkkkkkk..
.kNNNNNNNNNNnnk.
.knNNnNNNNNnnnk.
.knNNNNNnNNnnnk.
.knNnNNNNNNnnnk.
.knnnnnnnnnnnnk.
..kkkkkkkkkkkk..
""", 1, 1, note="a coin anvil: an iron block with the lower die in it, on an oak stump; a blank on the die")


def _coin_table():
    """A counting table: stacks of silver staters and a purse on top (iron
    palette, the top 8x8 row), an oak table under them (wood palette)."""
    top = """
................................
................................
........kkk.....................
...kkk.kwwwk.......kk...........
..kwwwkkSSsk..kkk.kNNk..kkkkk...
..kSSskkwwwk.kwwwkknNNk.kwwwwk..
..kwwwkkSSsk.kSSskknNnNkkSSsSk..
..kSSskkSssk.kSssk.knnk.kkkkkk..
"""
    bottom = """
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.khhhhhhhhhhhhhhhhhhhhhhhhhhhhk.
.khlllllllllllllllllllllllllllk.
.kmmmmmmmmmmmmmmmmmmmmmmmmmmmmk.
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
..kmdk....................kmdk..
..kmdk....................kmdk..
..kkkk....................kkkk..
"""
    return np.vstack([grid("iron", top, 32, 8), grid("wood", bottom, 32, 8)])


stamp("coin_table", "wood", _coin_table(), 2, 1,
      note="a counting table: stacks of silver staters, a purse, blanks waiting their turn")


stamp("die_rack", "iron", """
................................
................................
................................
................................
................................
................................
................................
................................
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
.kNNNNNNNNNNNNNNNNNNNNNNNNNNNNk.
.knnnnnnnnnnnnnnnnnnnnnnnnnnnnk.
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
...kk...kk...kk....kk.....kk....
...kk...kk...kk....kk.....kk....
..kSsk.kSsk.kSsk..kNNk...kSk....
..kSsk.kSsk.kSsk..kNnk..kSsIk...
..kSsk.kSsk.kSsk..kNnk..kSsIk...
..kSsk.kSsk.kSsk..kNnk..kSskIk..
..kSsk.kSsk.kSsk..kNnk..kSk.kIk.
..kSsk.kSsk.kSsk..kNnk..kSk.kIk.
..kSsk.kSsk.kSsk.kkSskk.kSk.kIk.
.kSSsIkSSsIkSSsIkkSSssIkkSk.kIk.
.kSwsIkSwsIkSwsIkkSSssIkkSk.kIk.
.kIIIIkIIIIkIIIIk.kIIIk..kk..kk.
..kkkk.kkkk.kkkk...kkk..........
................................
................................
................................
................................
................................
................................
................................
""", 2, 2, note="the moneyer's rack: three upper dies, a hammer and tongs on pegs")


stamp("brazier_small", "bronze", """
................
.....e..e.......
....eFeeFe..e...
....FfFFfFeeFe..
...kkkkkkkkkkkk.
..kYyyyyyyyyyzk.
..kzMkfMkFkMzk..
...kbkMfkMfkzk..
....kbbbbbbzk...
.....kkzzkkk....
.....kzkkzk.....
....kzk..kzk....
...kzk....kzk...
...kk......kk...
................
................
""", 1, 1, note="a small bronze brazier, silver blanks heating on its coals")


stamp("scales", "bronze", """
................
.......kk.......
......kYyk......
.kkkkkkyykkkkkk.
.kYyyyyyyyyyyzk.
..kkkkkbbkkkkk..
..k....kbk...k..
..k....kbk...k..
..k....kbk...k..
.k.k...kbk..k.k.
k...k..kbk.k...k
kMMMk..kbk.kkkkk
kkkkk..kbk.kYyzk
.......kbk..kkk.
.......kbk......
.......kbk......
.......kbk......
.......kbk......
.......kbk......
.......kbk......
.......kbk......
.......kbk......
.......kbk......
......kkbkk.....
.....kyyybzk....
....kYyyyybzk...
...kyyyyyybbzk..
...kzzzzzzzzzk..
....kkkkkkkkk...
................
................
................
""", 1, 2, note="a moneyer's balance: silver in one pan, a bronze weight in the other")


def paste(rows, piece, x, y):
    """Paste a grid (list of strings, '.' clear) into rows at (x, y)."""
    rows = [list(r) for r in rows]
    for j, prow in enumerate(piece):
        for i, ch in enumerate(prow):
            if ch != ".":
                rows[y + j][x + i] = ch
    return ["".join(r) for r in rows]


def _turtle_chest():
    body = [
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
        ".kbhhhhhhhhhhhhhhhhhhhhhhhhhhbk.",
        ".kyhhhhhhhhhhhhhhhhhhhhhhhhhhzk.",
        ".khllllllllllllllllllllllllllldk",
        ".khllllllllllllllllllllllllllldk",
        ".khllllllllllllllllllllllllllldk",
        ".khllllllllllllllllllllllllllldk",
        ".khllllllllllllllllllllllllllldk",
        ".khllllllllllllllllllllllllllldk",
        ".khllllllllllllllllllllllllllldk",
        ".kbllllllllllllllllllllllllllzk.",
        ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
        ".kbdddddddddddddddddddddddddzbk.",
        ".kybmmmmmmmmmkkkkkkmmmmmmmmmbzk.",
        ".kbbmlmmmmmmkyyyybzkmmmmmmlmbzk.",
        ".kybmlmmmmmmkybkkbzkmmmmmmlmbzk.",
        ".kbbmlmmmmmmkybkkbzkmmmmmmlmbzk.",
        ".kybmlmmmmmmkyybbbzkmmmmmmlmbzk.",
        ".kbbmmmmmmmmmkkkkkkmmmmmmmmmbzk.",
        ".kybmmmmmmmmmmmmmmmmmmmmmmmmbzk.",
        ".kybdddddddddddddddddddddddddzk.",
        ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
        "..kdk......................kdk..",
        "..kkk......................kkk..",
        "................................",
    ]
    turtle = [
        "....kkk....",
        "....kyk....",
        "kk.kybbk.kk",
        "kykybbbzkzk",
        ".kkbybzbkk.",
        ".kkbbbbzkk.",
        "kykkbbzkkzk",
        "kk..kzk..kk",
        ".....k.....",
    ]
    body = paste(body, turtle, 10, 9)
    return "\n".join(body)


stamp("turtle_chest", "wood", _turtle_chest(), 2, 2,
      note="the mint's strongbox: oak bound in bronze, a sea turtle stamped on its lid")


stamp("vault_door", "wood", """
................
................
................
................
................
................
.kkkkkkkkkkkkkk.
.kdddddddddddddk
.kdlllllllllldk.
.kdkkkkkkkkkkdk.
.kdkmlmmdmlmkdk.
.kdkmlmmdmlmkdk.
.kdkyybbybbzkdk.
.kdkzzzzzzzzkdk.
.kdkmlmmdmlmkdk.
.kdkmlmmdmlmkdk.
.kdkmlkkkkkmkdk.
.kdkmkzzzzzkkdk.
.kdkmkkkkkkkkdk.
.kdkmlbyybmmkdk.
.kdkmlmmdmlmkdk.
.kdkmlmmdmyykdk.
.kdkmlmmdmybkdk.
.kdkmlmmdmlmkdk.
.kdkmlmmdmlmkdk.
.kdkyybbybbzkdk.
.kdkzzzzzzzzkdk.
.kdkmlmmdmlmkdk.
.kdkmlmmdmlmkdk.
.kdkmlmmdmlmkdk.
.kdkkkkkkkkkkdk.
.kkkkkkkkkkkkkk.
""", 1, 2, note="the strongroom's inner door: oak bound in bronze, with a slot that lets coins out and nothing in")


# ===========================================================================
# Aiakides's house
# ===========================================================================

def _shield_spear():
    """A bronze hoplite shield hung on the wall with an ant for its blazon, and
    the spear behind it, butt to the floor."""
    W, H = 32, 32
    g = [["."] * W for _ in range(H)]
    cx, cy, R = 15.5, 18.5, 10.6
    # the spear, from the head at the top right to the butt at the bottom left
    for i in range(0, 30):
        x = 27 - i * 0.8
        y = 1 + i
        xi = int(round(x))
        if 0 <= xi < W and 0 <= y < H:
            ch = "y" if i < 6 else "z"
            g[y][xi] = ch
            if xi + 1 < W and i >= 6:
                g[y][xi + 1] = "b"
    for (x, y, ch) in [(28, 0, "Y"), (27, 1, "Y"), (28, 1, "y"), (26, 2, "y"), (27, 2, "y"), (28, 2, "b"),
                       (26, 3, "Y"), (27, 3, "b"), (25, 4, "y"), (26, 4, "z")]:
        g[y][x] = ch
    spear = {(x, y) for y in range(H) for x in range(W) if g[y][x] != "."}
    # the shield
    for y in range(H):
        for x in range(W):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= R:
                if d > R - 1.6:
                    g[y][x] = "z" if (x + 0.5 - cx) + (y + 0.5 - cy) > 0 else "b"   # the rim
                elif d > R - 2.4:
                    g[y][x] = "k"
                else:
                    t = ((x + 0.5 - cx) * -0.7 + (y + 0.5 - cy) * -0.7) / R
                    g[y][x] = "Y" if t > 0.45 else ("y" if t > -0.2 else "b")

    def solid(x, y):
        return g[y][x] != "." and g[y][x] != "k"
    g = outline(g, lambda x, y: g[y][x] != ".")
    for (x, y) in spear:
        pass
    # the blazon: a black ant, head up
    ant = [
        "...k.k...",
        "....k....",
        "...kkk...",
        "k..kkk..k",
        ".k..k..k.",
        "..kkkkk..",
        "....k....",
        ".kkkkkkk.",
        "k.kkkkk.k",
        "..kkkkk..",
        "...kkk...",
    ]
    for j, row in enumerate(ant):
        for i, ch in enumerate(row):
            if ch == "k":
                g[13 + j][11 + i] = "k"
    # the peg it hangs from
    g[7][15] = g[7][16] = "k"
    return rows_of(g)


stamp("shield_spear", "bronze", _shield_spear(), 2, 2,
      note="Aiakides's bronze shield, an ant for its blazon, and his spear, hung on the wall")


stamp("ant_shrine", "clay", """
................
.k..k...........
..kk............
.kllk...........
kmlmdkk..kkkkk..
kmmmdklk.kllllk.
.kddkmmdkkmlllmk
..k.kddk.kmmmmdk
.k.k.k.kk.kmmddk
k..k..k..k.kddk.
kkkkkkkkkkkkkkkk
khttttttttttttsk
kSSSSSSSSSSSSSsk
.kkkkkkkkkkkkkk.
..ktttttttttsk..
..ktSSSSSSSSsk..
..ktSkkkkkkSsk..
..ktkaaaFaakSk..
..ktkaaYYaakSk..
..ktkacccakkSk..
..ktkkkkkkkkSk..
..ktSSSSSSSSsk..
..ktSSsSSSSSsk..
..ktSSSSSSsSsk..
..ktSSSSSSSSsk..
..ktSSSSSSSSsk..
.kkkkkkkkkkkkkk.
.khttttttttttsk.
.kSSSSSSSSSSSsk.
.kkkkkkkkkkkkkk.
................
................
""", 1, 2, note="a little stone shrine with a clay ant on it and a lamp in its niche: Aiakides's ancestors")


stamp("anthill_pot", "clay", """
................
................
................
................
................
......k.........
.....kak..k.....
....kasak.......
...kaSasak..k...
..kasaksaak.....
..kaSaasaSak....
.kaasakasaSak...
.kaSaasaahaak...
kaasaSaasaaSak..
kkkkkkkkkkkkkkk.
khhhhhhhhhhhhlk.
kmlllllllllllmk.
.kddddddddddddk.
..klmmmmmmmmdk..
.klhmmmmmmmmmdk.
.klhmmmmmmmmmdk.
kllkmmmmmmmmmmdk
klhmmmmmmmmmmmdk
klhmmkmmmmmmmmdk
klhmmmmmmmmmmmdk
klhmmmmmmkmmmmdk
.klmmmmmmmmmmdk.
.klmmmmmmmmmmdk.
..klmmmmmmmmdk..
...kddddddddk...
....kkkkkkkk....
................
""", 1, 2, note="a big pot full of earth, a living anthill heaped in it; ants on the rim")


stamp("ant_trail", "clay", """
................
...........k.k..
..........kkdk..
...........k.k..
................
.......k.k......
......kkdk......
.......k.k......
................
...k.k..........
..kkdk..........
...k.k..........
................
k.k.............
kdk.............
k.k.............
""", 1, 1, walk={(0, 0)}, note="a line of ants across the floor, marching for the crumbs")


# ===========================================================================
# Batch 2: Emporion's Hephaisteion (tools/ichor/maps/emporion_rooms.py)
#
# A forge built into the temple's courtyard, under a smoke-black roof: the
# great forge and its hood, cold or lit, the goatskin bellows, the smith's
# horned anvil on an oak stump, the quenching trough, the tongs rack, a
# basket of charcoal, and the shelf of bronze votives Kedalion sells once the
# fire is back. The floor is beaten earth (the floor palette's earth tones,
# saved for this), the wall smoke-blackened plaster.
# ===========================================================================

from char_canvas import Canvas  # noqa: E402


def _earth(variant):
    """Beaten earth, swept but sooty: a speckle that repeats every 8 pixels so
    the plain floor costs one tile; a shadow under the wall or along the left
    edge, as oikia's floors have; the alt cell has a few cinders in it."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            h = ((x % 8) * 37 + (y % 8) * 91 + (x % 8) * (y % 8) * 13) % 29
            c.put(x, y, "h" if h in (0, 11) else "E" if h in (4, 17, 23) else "e")
    if variant in ("top", "corner"):
        for x in range(16):
            c.put(x, 0, "K")
            c.put(x, 1, "E")
            c.put(x, 2, "E")
            c.put(x, 3, "E" if x % 2 == 0 else "e")
    if variant in ("left", "corner"):
        for y in range(16):
            c.put(0, y, "K")
            c.put(1, y, "E")
            if y % 2 == 0:
                c.put(2, y, "E")
    if variant == "alt":
        for (x, y, ch) in [(4, 5, "K"), (5, 5, "E"), (11, 9, "K"), (10, 10, "K"), (11, 10, "E"),
                           (6, 12, "K"), (13, 3, "E"), (2, 13, "E")]:
            c.put(x, y, ch)
    return grid("floor", c.text())


FLOORS["earth"] = {v: _earth(v) for v in ("plain", "alt", "top", "left", "corner")}


def wall_smoke():
    """The forge's back wall: the ceiling beam black with soot, the plaster
    under it smoked from black at the top to stone-gray at the plinth. The
    soot streaks repeat every 8 pixels, so the wall costs four tiles."""
    rows = ["k" * 16, "2" * 16, "1" * 16, "1" * 16, "k" * 16]
    # Soot hangs in streaks from the beam: each column of the 8-pixel repeat
    # has its own depth, so the black comes down in a ragged fringe.
    depth = [14, 9, 17, 11, 7, 15, 12, 18]
    for y in range(5, 28):
        row = []
        for x in range(16):
            d = depth[x % 8]
            if y < 7:
                ch = "k"
            elif y < 5 + d:
                ch = "k" if (y + x) % 5 == 0 else "1"
            elif y < 5 + d + 3:
                ch = "2"
            elif y < 24:
                ch = "S" if (x % 8 + y) % 6 else "2"
            else:
                ch = "S"
            row.append(ch)
        rows.append("".join(row))
    rows += ["2" * 16, "1" * 16, "1" * 16, "k" * 16]
    assert len(rows) == 32, len(rows)
    return grid("wall", "\n".join(rows))


WALLS["smoke"] = wall_smoke()


def _forge_hood(lit):
    """The forge's stone hood, 3x2 against the back wall: a flue rising
    through the roof, the hood flaring over the hearth, its lintel, and in the
    middle the empty iron hook where the Bronze Hammer hung, a clean hammer
    shape left in the soot behind it. Lit, the fire glows on the lintel and
    up inside the hood."""
    c = Canvas(48, 32)
    # the flue, up through the ceiling: dark stone, black with soot
    c.box(14, 0, 33, 11, "s")
    c.vline(15, 0, 10, "S")
    c.vline(32, 0, 10, "a")
    for y in (3, 7):
        c.hline(15, 32, y, "a")
    for x in (20, 27):
        c.vline(x, 0, 2, "a")
        c.vline(x + 3, 4, 6, "a")
        c.vline(x, 8, 10, "a")
    # the hood: a trapezoid flaring from the flue to the lintel
    for y in range(11, 25):
        half = 10 + (y - 11) * 14 // 13
        x0, x1 = 24 - half, 23 + half
        c.hline(x0, x1, y, "s")
        c.put(x0, y, "k")
        c.put(x1, y, "k")
        c.put(x0 + 1, y, "S")
        c.put(x1 - 1, y, "a")
    c.hline(10, 37, 11, "k")
    # soot thick up the hood's middle
    for y in range(12, 25):
        for x in range(12, 36):
            if c.get(x, y) == "s" and (x * 7 + y * 5) % 7 < 3:
                c.put(x, y, "a")
    # the lintel: a stone beam across the front of the hood
    c.box(0, 24, 47, 31, "S")
    c.hline(1, 46, 25, "t")
    c.hline(1, 46, 29, "s")
    c.hline(1, 46, 30, "s")
    for x in (12, 24, 36):
        c.vline(x, 25, 29, "s")
    # the empty hook, and the hammer's clean shape in the soot behind it
    c.rect(19, 13, 28, 16, "S")          # the head's shadow
    c.rect(22, 17, 25, 22, "S")          # the haft's shadow
    c.hline(20, 27, 14, "t")
    c.vline(23, 17, 22, "t")
    c.vline(23, 12, 15, "k")
    c.vline(24, 12, 15, "k")
    c.put(22, 15, "k")
    c.put(22, 16, "k")
    c.put(23, 16, "k")
    c.put(25, 13, "c")
    if lit:
        # firelight on the lintel and up the hood's throat
        c.hline(1, 46, 29, "F")
        c.hline(1, 46, 30, "f")
        c.hline(1, 46, 31, "f")
        for x in range(2, 46, 3):
            c.put(x, 28, "F")
        for y in range(16, 24):
            for x in range(8, 40):
                if c.get(x, y) in ("a", "s") and (x * 3 + y) % 4 == 0:
                    c.put(x, y, "f" if y < 21 else "F")
        for (x, y) in ((17, 23), (21, 22), (27, 23), (31, 22), (12, 23), (36, 23)):
            c.put(x, y, "Y")
    return c.text()


stamp("forge_hood", "clay", _forge_hood(False), 3, 2,
      note="the forge's stone hood and flue, black with soot; the empty hook where the Bronze Hammer hung")
stamp("forge_hood_lit", "clay", _forge_hood(True), 3, 2,
      note="the hood with the forge lit: firelight on the lintel and up its throat")


def _forge(lit):
    """The hearth itself, 3x1: a raised bed of stone with the fire on it and
    the bellows' clay nozzle let into its right end. Cold, the bed is gray ash
    and dead charcoal; lit, the coals glow and flames lick up at the hood."""
    c = Canvas(48, 16)
    # the stone curb, its top rim lit, its face in courses
    c.box(1, 2, 46, 15, "S")
    c.hline(2, 45, 3, "t")
    c.hline(2, 45, 8, "k")
    c.hline(2, 45, 9, "t")
    c.hline(2, 45, 14, "s")
    c.hline(2, 45, 12, "s")
    for x in (9, 20, 31, 42):
        c.vline(x, 10, 11, "s")
    for x in (4, 15, 26, 37):
        c.vline(x, 13, 14, "s")
    # the clay tuyere at the right end, where the bellows blow in
    c.box(41, 10, 46, 13, "m")
    c.put(42, 11, "l")
    c.put(43, 11, "l")
    c.put(45, 12, "k")
    # the bed of the fire
    for y in range(4, 8):
        for x in range(3, 45):
            n = (x * 13 + y * 7) % 11
            if lit:
                c.put(x, y, "Y" if n == 0 else "F" if n < 5 else "f" if n < 9 else "d")
            else:
                c.put(x, y, "a" if n < 4 else "s" if n < 8 else "t" if n == 8 else "k")
    if lit:
        # flames licking up off the coals
        for (x0, hgt) in ((8, 3), (14, 4), (20, 2), (25, 4), (31, 3), (37, 4)):
            c.vline(x0, 4 - hgt, 3, "F")
            c.put(x0, 4 - hgt, "Y")
            c.put(x0 - 1, 3, "f")
            c.put(x0 + 1, 3, "f")
        c.hline(2, 45, 3, "F")
    else:
        for (x, y) in ((10, 5), (11, 5), (22, 6), (23, 5), (33, 6), (34, 6), (17, 4)):
            c.put(x, y, "k")
    return c.text()


stamp("forge_cold", "clay", _forge(False), 3, 1,
      note="the forge's hearth, cold: gray ash and dead charcoal on a stone bed")
stamp("forge_lit", "clay", _forge(True), 3, 1,
      note="the forge's hearth, lit from Hestia's coal: glowing coals, flames licking at the hood")

stamp("bellows", "iron", """
................
................
....kkk..kkk....
...kNNNkkNNNk...
..kNNnNNkNnNNk..
..kNnnnNkNnnNk..
..knnnnnkknnnk..
..knnnnnkknnnk..
..kNnnnnkNnnnk..
...knnnkkknnk...
...kknkkSkknk...
kkkkkkkSSSkkk...
kIssssssSSk.....
kkkkkkkkkkk.....
...kNNNNNNNNk...
...kkkkkkkkkk...
""", 1, 1, note="the bellows: two goatskins on a plank, their iron nozzle run into the hearth")

stamp("smith_anvil", "iron", """
................
................
................
....kkkkkkkk....
.kkkwwwwwwwSk...
kSSSSSSSSSSSsk..
.kkkssssssssk...
....kIssssIk....
.....kIssIk.....
....kkkkkkkk....
...kNNNNNNNNk...
...knNNNNNNnk...
...knnNnnNnnk...
...knnnNNnnnk...
...knnnnnnnnk...
....kkkkkkkk....
""", 1, 1, note="the smith's anvil: a horned iron anvil on an oak stump")

stamp("quench_trough", "bronze", """
................................
................................
................................
................................
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
.kMMMMMMMMMMMMMMMMMMMMMMMMMMMMk.
.kMmkkkkkkkkkkkkkkkkkkkkkkkkmmk.
.kMkuuuuUuuuuuuuuuuuaUuuuuuukmk.
.kMkuuUuuuuukkuuuuuuuuuUuuuukmk.
.kMkuuuuuuukzkkkkkuuuuuuuuuukmk.
.kmmkkkkkkkkkkkkkkkkkkkkkkkkmnk.
.knmmmmmmmmmmmmmmmmmmmmmmmmmmnk.
.knnmnnmnnnmnnmnnnmnnmnnnmnnnnk.
.knnnnnnnnnnnnnnnnnnnnnnnnnnnnk.
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
................................
""", 2, 1, note="the quenching trough: a stone trough of dark water, tongs left in it")

stamp("tongs_rack", "iron", """
................................
....k.......k..........k........
...kSk.....kSk........kSk.......
...kSk.....kSk.......kSSk..kkk..
...kSk.....kSk......kSsk..kSSSk.
...kSk.....kSk......kSk...kIIsk.
...kSkk...kkSk.....kSk.....kkk..
...kSkSk.kSkSk.....kNk......kNk.
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
kNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNk
knnnnknnnnnnknnnnnnknnnnnnknnnnk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
..kSk..kSk.........kNk......kNk.
..kSk..kSk.........kNk......kNk.
..ksk..ksk.........kNk......kNk.
...k....k...........k........k..
""", 2, 1, note="the tongs rack: a pegged plank of tongs and hammers")

stamp("votive_shelf", "bronze", """
................................
................................
.....k.....................k....
....kyk.......kkk.........kyk...
....kbk......kyybk..kk....kbk...
...kybk.....kybbbkkybk...kybbk..
...kbbzk....kbbbbbbbzk...kbbbk..
....kbk.....kbk.kbkk.....kbbzk..
....kzk.....kzk.kzk.......kzk...
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
kyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyk
kbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk
kzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
..kzk......................kzk..
..kkk......................kkk..
""", 2, 1, note="a low shelf of bronze votives for sale: a little smith, a bull, an owl")

stamp("workbench", "wood", """
................................
................................
................................
..........kkkkk.................
.........kybbbbk.......kk.......
..kkk...kyybbbzzk.....kbbk......
.kbbbk..kybbkkkzk.kkkkbbbkk.kk..
.kzzzzk.kkkkkkkkkkkkkkkkkkkkkkk.
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
khlllllllllllllllllllllllllllllk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
.kmdk......................kmdk.
.kmdk......................kmdk.
.kkkk......................kkkk.
""", 2, 1, note="the smith's bench: an ingot, a half-beaten bronze helmet, a hammer and a file")

stamp("charcoal_basket", "nature", """
................
................
................
................
....kkk.kk......
..kkSkkkSkkk....
.kkSkkSkkkSkk...
.kJJJJJJJJJJJk..
.kjJjJjJjJjJjk..
..kjjjjjjjjjk...
..kKjKjKjKjKk...
..kjjjjjjjjjk...
...kKjKjKjKk....
...kjjjjjjjk....
....kkkkkkk.....
................
""", 1, 1, note="a wicker basket heaped with charcoal")
