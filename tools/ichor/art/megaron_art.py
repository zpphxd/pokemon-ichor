#!/usr/bin/env python3
"""Pixel art for the megaron tileset: the Troad's interiors, Sestos and Ilion.

megaron is the secondary for the Trojan rooms of the Oikoumene's first land
(design/OIKOUMENE.md §4.1 and §7; design/oikoumene/BUILD.md §5). It sits on the
oikos primary, as oikia and civic do, and like them works on any primary.

It is built the way oikia is (design/phase1/TILES_oikia.md): hand-drawn
character grids and small generators, one character per color, '.' clear, in
seven palettes of at most 15 colors whose values appear in no aethos palette.
The furniture a Trojan room shares with a Greek home (the couch, the stools,
the jars, the lampstand, the nets and oars) is taken from oikia_art.py pixel
for pixel; everything that makes the rooms Trojan is drawn here:

  - Troy's pale limestone ashlar with its timber lacing beam, Sestos's
    whitewash with a running-wave dado, and the palace's frescoed plaster;
  - the painted plaster floor of a Bronze Age megaron, squares ruled in red;
  - red Minoan columns, a round painted hearth, a throne and a horse frieze;
  - grey Trojan pottery; an Anatolian kilim;
  - and each household's own things: Hero's windy stair, slits and great lamp,
    the ferryman's wreath, the net rack, the mason's drums, the weaver's
    loom and dye vats, the stable's stalls, the Palladion.

Palettes:
  wall    oikia's: beams, whitewash, red ochre, ochre, Aegean blue, sky
  floor   oikia's limestone flags and boards; the megaron's painted plaster
          (cream ruled in red and ochre); beaten earth and straw
  wood    oikia's: furniture woods, bronze fittings, linen, red and blue cloth
  clay    oikia's: pottery, hearth stone (Trojan grey ware), fire, soot, slip
  cloth   oikia's rug colors and a Tyrian purple: kilims, bolts, dyes, skeins
  nature  oikia's: leaves, wicker and straw, fish, rope
  bronze  oikia's: bronze, flame, water, marble

megaron_build.py assembles the pieces into metatiles;
tools/ichor/maps/troad_rooms.py lays out the rooms.
"""
import copy
import math

import numpy as np

import oikia_art as O

INK = O.INK

PALETTES = copy.deepcopy(O.PALETTES)

# floor: oikia's terracotta goes (no Greek pavers in Troy). In its place the
# megaron's painted plaster, ruled in red and ochre over the limestone's
# cream, and beaten earth with straw for the stable and the ferry house.
for _ch in ("T", "t", "x", "u", "v", "g"):
    del PALETTES["floor"][_ch]
PALETTES["floor"].update({
    "r": (184, 72, 48),    # painted red line
    "o": (208, 160, 88),   # painted ochre
    "e": (160, 128, 88),   # beaten earth
    "E": (128, 96, 72),    # earth, low
    "h": (184, 152, 112),  # earth, lit
    "Y": (224, 192, 104),  # straw
})

# cloth: oikia's rug colors and a Tyrian purple for the peplos and the bolts.
PALETTES["cloth"].update({
    "p": (104, 48, 96),    # purple, dark
    "P": (152, 88, 144),   # purple
    "w": (248, 248, 224),  # bleached linen
})

PALETTE_ORDER = ["wall", "floor", "wood", "clay", "cloth", "nature", "bronze"]


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


def recolor(img, pal, mapping):
    colors = PALETTES[pal]
    out = img.copy()
    for a, b in mapping.items():
        m = (img[..., :3] == colors[a]).all(-1) & (img[..., 3] > 0)
        out[m, :3] = colors[b]
    return out


def hflip(img):
    return img[:, ::-1].copy()


# --- drawing helpers on character canvases ------------------------------------

def canvas(w, h, fill="."):
    return [[fill] * w for _ in range(h)]


def text(g):
    return "\n".join("".join(r) for r in g)


def put(g, x, y, c):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = c


def hline(g, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        put(g, x, y, c)


def vline(g, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        put(g, x, y, c)


def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        hline(g, x0, x1, y, c)


def paste(g, rows, x, y):
    """Lay a small character piece over g at (x, y); '.' stays clear."""
    for j, line in enumerate(rows):
        for i, ch in enumerate(line):
            if ch != ".":
                put(g, x + i, y + j, ch)


def mirror(half):
    """Rows drawn as left halves; return them mirrored to full width."""
    return [r + r[::-1] for r in half]


def outline(g, ink="k"):
    """Ink every clear pixel that touches a drawn one (4-neighbours)."""
    H, W = len(g), len(g[0])
    out = [row[:] for row in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != ".":
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and g[ny][nx] not in (".", ink):
                    out[y][x] = ink
                    break
    return out


def jar(w, h, cx, top, profile, body, lit, dark, rim=None):
    """A turned vessel: profile[i] is the half-width of row top+i."""
    g = canvas(w, h)
    for i, hw in enumerate(profile):
        y = top + i
        for x in range(cx - hw, cx + hw):
            rel = (x - (cx - hw)) / max(1, 2 * hw - 1)
            c = lit if rel < 0.3 else dark if rel > 0.78 else body
            put(g, x, y, c)
    if rim:
        hline(g, cx - profile[0], cx + profile[0] - 1, top, rim)
    return g


# --------------------------------------------------------------------------
# Floors (16x16, opaque, bottom layer).
# --------------------------------------------------------------------------

def floor_plaster(alt=False):
    """The megaron's painted floor: squares of cream plaster with soft ruled
    joints, red where four meet, and here and there a painted rosette (Pylos,
    the throne room). Mirror-symmetric both ways: the quadrants are one tile."""
    g = canvas(16, 16, "L")
    for i in range(16):                 # a soft ruled joint, red only where four squares meet
        for (x, y) in ((i, 0), (i, 15), (0, i), (15, i)):
            g[y][x] = "y"
    for (x, y) in ((0, 0), (15, 0), (0, 15), (15, 15)):
        g[y][x] = "r"
    for (x, y) in ((1, 0), (0, 1), (14, 0), (15, 1), (0, 14), (1, 15), (15, 14), (14, 15)):
        g[y][x] = "o"
    if alt:   # a rosette of ochre petals
        for (x, y, c) in [(7, 4, "o"), (8, 4, "o"), (6, 5, "o"), (9, 5, "o"), (7, 5, "r"), (8, 5, "r"),
                          (4, 7, "o"), (4, 8, "o"), (5, 6, "o"), (5, 9, "o"), (5, 7, "r"), (5, 8, "r"),
                          (6, 6, "y"), (9, 6, "y"), (6, 9, "y"), (9, 9, "y")]:
            for (mx, my) in ((x, y), (15 - x, y), (x, 15 - y), (15 - x, 15 - y)):
                g[my][mx] = c
        for (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8)):
            g[y][x] = "r"
    return grid("floor", text(g))


def floor_earth(straw=False):
    """Beaten earth, 8-pixel periodic: one tile; the alternate has straw."""
    t = [
        "eeheeeEe",
        "eeeeEeee",
        "heeeeeeh",
        "eeEeeeee",
        "eeeeehee",
        "Eeeeeeee",
        "eeehEeee",
        "eeeeeeeE",
    ]
    if straw:
        t = [list(r) for r in t]
        for (x, y) in [(1, 1), (2, 1), (3, 2), (5, 5), (6, 5), (6, 4)]:
            t[y][x] = "Y"
        t = ["".join(r) for r in t]
    rows = [r + r for r in t] * 2
    return grid("floor", "\n".join(rows))


FLOOR_SHADE = {
    "flags": {"L": "y", "l": "q", "y": "q", "q": "Q"},
    "boards": {"W": "m", "m": "n", "n": "j"},
    "plaster": {"L": "l", "l": "y", "y": "q", "o": "h", "r": "E"},
    "earth": {"h": "e", "e": "E", "E": "j", "Y": "o"},
}


def shade(img, material, mask):
    dark = recolor(img, "floor", FLOOR_SHADE[material])
    out = img.copy()
    out[mask] = dark[mask]
    return out


def floor_variants(material, base, alt=None):
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    out = {
        "plain": base,
        "top": shade(base, material, top),
        "left": shade(base, material, left),
        "corner": shade(base, material, top | left),
    }
    if alt is not None:
        out["alt"] = alt
    return out


FLOORS = {
    "flags": O.FLOORS["flags"],
    "boards": O.FLOORS["boards"],
    "plaster": floor_variants("plaster", floor_plaster(), floor_plaster(alt=True)),
    "earth": floor_variants("earth", floor_earth(), floor_earth(straw=True)),
}

# --------------------------------------------------------------------------
# Walls (16x32: rows 0 and 1 of a room).
# --------------------------------------------------------------------------

# A running spiral (the "wave" of Aegean painting), one period in 8x8.
SPIRAL8 = [
    "..####..",
    ".#....#.",
    "#..##..#",
    "#.#..#.#",
    "#.#.##.#",
    "#..#...#",
    ".#....#.",
    "#.####..",
]


def _ceiling(rows):
    rows.append("k" * 16)                       # 0 ceiling edge
    rows.append("2" * 16)                       # 1 beam
    rows.append("3" * 16)                       # 2 beam, lit
    rows.append("2" * 16)                       # 3
    rows.append("1" * 16)                       # 4 beam underside
    rows.append("s23321sss23321ss")             # 5 rafter ends
    rows.append("s12211sss12211ss")             # 6
    rows.append("ps1111spps1111sp")             # 7 shadow under rafters
    rows.append("pppssssppppssssp")             # 8


def wall_sea():
    """Sestos: whitewashed plaster over a dado of blue running waves, the
    harbor's colors."""
    rows = []
    _ceiling(rows)
    for y in range(9, 20):
        rows.append("p" * 16)
    rows.append("s" * 16)                       # 20 shade line
    rows.append("B" * 16)                       # 21
    rows.append("b" * 16)                       # 22
    for y in range(8):                          # 23-30 the wave band
        rows.append("".join("w" if c == "#" else "b" for c in SPIRAL8[y] * 2))
    rows.append("k" * 16)                       # 31
    rows = [list(r) for r in rows]
    for (x, y, c) in [(3, 11, "w"), (10, 13, "w"), (13, 16, "s"), (6, 17, "w"), (1, 15, "s")]:
        rows[y][x] = c
    return grid("wall", text(rows))


def wall_ashlar():
    """Ilion: Troy's pale limestone, squared and laid in courses, with the
    timber lacing beam the Trojans ran through their walls, on a dark plinth."""
    rows = []
    _ceiling(rows)
    joints = [3, 11, 7]
    for c, jx in enumerate(joints):             # 9-29: three courses of 7 rows
        top = 9 + c * 7
        for y in range(top, top + 7):
            r = y - top
            row = []
            for x in range(16):
                if r == 6:
                    ch = "S"
                elif x == jx:
                    ch = "S"
                elif x == (jx + 1) % 16 or r == 0:
                    ch = "w"
                elif r == 5:
                    ch = "s"
                else:
                    ch = "p"
                row.append(ch)
            rows.append("".join(row))
    rows = rows[:23]                            # rows 0-22
    rows.append("1" * 16)                       # 23 the lacing beam
    rows.append("3" * 16)
    rows.append("2" * 16)
    rows.append("2" * 16)
    rows.append("1" * 16)
    rows.append("S" * 16)                       # 28 plinth
    rows.append("s" * 16)
    rows.append("S" * 16)
    rows.append("k" * 16)                       # 31
    rows = [list(r) for r in rows]
    for (x, y, c) in [(5, 11, "s"), (13, 18, "w"), (9, 20, "s"), (1, 13, "w"), (14, 25, "1"), (6, 24, "2")]:
        rows[y][x] = c
    return grid("wall", text(rows))


def wall_fresco():
    """The palace's plaster: a frieze of red and blue spirals at eye height,
    and a dado painted as red-veined stone panels."""
    rows = []
    _ceiling(rows)
    for y in range(9, 13):
        rows.append("p" * 16)                   # 9-12 plaster
    rows.append("o" * 16)                       # 13
    rows.append("r" * 16)                       # 14
    for y in range(8):                          # 15-22 the spiral frieze
        rows.append("".join(("r" if (y < 4) else "b") if c == "#" else "w" for c in SPIRAL8[y] * 2))
    rows.append("r" * 16)                       # 23
    rows.append("o" * 16)                       # 24
    panel = [
        "RRRRRRRDRRRRRRRD",
        "RrRRRRRDRRRrRRRD",
        "RRrrRRRDRRRRrRRD",
        "RRRRrRRDRrRRRRRD",
        "RRRRRrRDRRrrRRRD",
        "DDDDDDDDDDDDDDDD",
    ]
    rows.extend(panel)                          # 25-30 the stone-painted dado
    rows.append("k" * 16)                       # 31
    return grid("wall", text(rows))


WALLS = {
    "sea": wall_sea(),
    "ashlar": wall_ashlar(),
    "fresco": wall_fresco(),
}

VOID = O.VOID

# --------------------------------------------------------------------------
# Rugs: 9-slices on the bottom layer, cut from a 48x48 grid.
# --------------------------------------------------------------------------


def rug_kilim():
    """An Anatolian kilim: madder field, a border of ram's-horn hooks in wool
    between saffron lines, and a column of indigo hooked lozenges. Built to be
    symmetric and 8-pixel periodic along its edges, so it costs few tiles."""
    g = [["r"] * 48 for _ in range(48)]
    for y in range(48):
        for x in range(48):
            d = min(x, y, 47 - x, 47 - y)
            if d == 0:
                g[y][x] = "n"
            elif d == 1:
                g[y][x] = "y"
            elif d in (2, 3, 4, 5, 6):
                g[y][x] = "R"
            elif d == 7:
                g[y][x] = "y"
    HOOK = [  # 8-wide period, 5 tall: a ram's-horn hook in wool
        "c......c",
        "cc.cc.cc",
        ".ccc.cc.",
        "cc.cc.cc",
        "c......c",
    ]
    for i in range(48):
        for k in range(5):
            c = HOOK[k][i % 8]
            if c == "." or not (8 <= i <= 39):
                continue
            for (x, y) in ((i, 2 + k), (i, 45 - k), (2 + k, i), (45 - k, i)):
                g[y][x] = c
    # corners: a saffron square knot
    for (cx, cy) in ((4, 4), (43, 4), (4, 43), (43, 43)):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                g[cy + dy][cx + dx] = "y" if max(abs(dx), abs(dy)) == 2 else ("i" if dx == dy == 0 else "R")
    # field: a lattice of hooked lozenges every 16 pixels, centered on 16k+8
    LOZ = [
        "...i...",
        "..iui..",
        ".iuyui.",
        "iuyRyui",
        ".iuyui.",
        "..iui..",
        "...i...",
    ]
    for cy in (8, 24, 40):
        for cx in (8, 24, 40):
            if 12 <= cx <= 36 and 12 <= cy <= 36:
                for j, line in enumerate(LOZ):
                    for i, c in enumerate(line):
                        if c != ".":
                            g[cy - 3 + j][cx - 3 + i] = c
                for (dx, dy) in ((-5, 0), (5, 0), (0, -5), (0, 5)):
                    g[cy + dy][cx + dx] = "c"
    return grid("cloth", text(g))


RUGS = {"kilim": rug_kilim()}

# --------------------------------------------------------------------------
# Stamps. oikia's contract: w, h in metatiles; walk cells the player may stand
# on; behavior per cell; `top` art over the player; `flatten` into the bottom.
# --------------------------------------------------------------------------

STAMPS = {}

SHARED = ["window", "kline", "klismos_r", "klismos_l", "stool", "table",
          "pithos", "lampstand", "kalathos", "fish_basket", "knucklebones", "nets", "oars"]
for _name in SHARED:
    STAMPS[_name] = dict(O.STAMPS[_name], source="oikia")


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note=""):
    img = art if isinstance(art, np.ndarray) else grid(pal, art, w * 16, h * 16)
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    tp = None
    if top is not None:
        tp = top if isinstance(top, np.ndarray) else grid(pal, top, w * 16, h * 16)
    STAMPS[name] = {
        "pal": pal, "img": img, "top": tp, "w": w, "h": h,
        "walk": set(walk), "behavior": dict(behavior or {}),
        "flatten": flatten, "note": note, "source": "megaron",
    }


from megaron_pieces import define_pieces  # noqa: E402  (the stamps, in their own file)

define_pieces(globals())
