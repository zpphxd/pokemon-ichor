#!/usr/bin/env python3
"""Pixel art for gTileset_ThyrsaRooms: the interiors of Thyrsa and Eleutherai.

The base of the set: its seven palettes, the drawing helpers, the floors, the
walls and the stamp registry. The furniture lives in three more modules, which
register their stamps here when imported:

  thyrsa_rooms_kithairon.py  Eleutherai: the watch-house, Oinoe's and Lysidike's
  thyrsa_rooms_civic.py      Thyrsa's Asclepeion, Agora and the Kantharos tavern
  thyrsa_rooms_homes.py      Thyrsa's seven households

Everything is drawn by hand as character grids, one character per color and
'.' for clear, in the style of oikia_art.py (whose floors and a few of whose
pieces are reused here as they are). Each 8x8 tile must take all its colors
from one palette; thyrsa_rooms_build.py checks that.

Two looks run through the set:
  Thyrsa      plastered walls with a wine-dark dado and an ochre wave scroll,
              ivy festooned along the beam; masks, grapes and wine everywhere.
  Eleutherai  a mountain border village: whitewash over rough stone, round log
              beams, packed-earth floors; the fort's barrack is bare ashlar.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import oikia_art as OA  # noqa: E402  (floors and a few pieces are reused as drawn)

# --------------------------------------------------------------------------
# Palettes. All values are multiples of 8, and none equals an aethos color, so
# Porytiles can only place these tiles in palettes 6-12 (the builder checks).
# --------------------------------------------------------------------------

INK = OA.INK  # (40, 24, 24)

PALETTES = {
    # Thyrsa's plaster walls: beam, whitewash, the wine-dark dado, windows
    "wall": {
        "k": INK,
        "1": (80, 48, 32),     # beam, dark
        "2": (120, 72, 40),    # beam
        "3": (160, 104, 56),   # beam, lit
        "w": (248, 240, 232),  # whitewash, lit
        "p": (232, 224, 208),  # whitewash
        "s": (208, 192, 176),  # whitewash, shade
        "S": (168, 152, 136),  # whitewash, deep shade
        "r": (184, 72, 96),    # wine dado, lit
        "R": (136, 40, 72),    # wine dado
        "D": (88, 24, 48),     # wine dado, dark
        "o": (224, 176, 96),   # ochre line
        "b": (56, 96, 160),    # shutter blue
        "B": (104, 152, 208),  # shutter blue, lit
        "a": (200, 224, 240),  # sky
    },
    # floors: oikia's terracotta, boards and limestone (packed earth is drawn
    # from the board and terracotta tones)
    "floor": dict(OA.PALETTES["floor"]),
    # furniture woods, linen, red and blue cloth, bronze fittings
    "wood": dict(OA.PALETTES["wood"]),
    # pottery, the hearth, stone, fire, soot, white slip; the black-figure frieze
    "clay": dict(OA.PALETTES["clay"]),
    # ivy, vines, grapes and wine, wicker, straw, rope, wool
    "nature": {
        "k": INK,
        "G": (40, 72, 48),     # leaf, dark
        "g": (72, 120, 56),    # leaf
        "v": (120, 168, 80),   # leaf, lit
        "V": (184, 216, 128),  # leaf, highlight
        "w": (248, 248, 232),  # bone, fleece, flower
        "S": (56, 24, 64),     # wine, darkest
        "p": (96, 56, 104),    # grape, dark
        "P": (136, 80, 144),   # grape
        "s": (184, 136, 192),  # grape, bloom
        "K": (120, 88, 48),    # wicker, dark
        "j": (176, 136, 72),   # wicker
        "J": (224, 192, 128),  # wicker, lit; straw
        "n": (208, 184, 144),  # rope, wool shade
        "d": (136, 56, 32),    # clay, dark
    },
    # bronze, flame, water, marble; masks and statues. oikia's, with its water
    # glint traded for an ivy green (glints use the marble white).
    "bronze": dict({k: v for k, v in OA.PALETTES["bronze"].items() if k != "a"}, g=(72, 120, 56)),
    # rough stone, dark flags, earth tones for the fort, the cellar, old houses
    "stone": {
        "k": INK,
        "1": (56, 48, 48),     # joint, deepest shadow
        "2": (88, 80, 72),     # stone, dark
        "3": (120, 112, 104),  # stone
        "4": (152, 144, 128),  # stone, lit
        "5": (184, 176, 160),  # stone, highlight
        "6": (224, 216, 200),  # stone, glint
        "e": (72, 56, 48),     # timber, dark; mortar
        "E": (112, 80, 56),    # timber
        "h": (152, 112, 72),   # timber, lit
        "m": (96, 104, 80),    # lichen
        "M": (136, 144, 104),  # lichen, lit
        "l": (232, 160, 72),   # lamp glow
        "L": (248, 216, 136),  # lamp glow, bright
    },
}

# The order the builder hands these to Porytiles as packing hints.
PALETTE_ORDER = ["wall", "floor", "wood", "clay", "nature", "bronze", "stone"]


def grid(pal, text, w=None, h=None):
    """Parse a character grid into an (h, w, 4) RGBA array ('.' or ' ' = clear)."""
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


def rows_to_grid(pal, rows):
    return grid(pal, "\n".join("".join(r) for r in rows))


def over(dst, src):
    out = dst.copy()
    m = src[..., 3] > 0
    out[m] = src[m]
    return out


def recolor(img, pal, mapping, pal_to=None):
    """Swap colors by character: {'a': 'b'} turns pal.a into (pal_to or pal).b."""
    src_cols, dst_cols = PALETTES[pal], PALETTES[pal_to or pal]
    out = img.copy()
    for a, b in mapping.items():
        m = (img[..., :3] == src_cols[a]).all(-1) & (img[..., 3] > 0)
        out[m, :3] = dst_cols[b]
    return out


def hflip(img):
    return img[:, ::-1].copy()


def blank(w, h):
    return np.zeros((h * 16, w * 16, 4), np.uint8)


def noise(x, y, seed=0):
    """A cheap deterministic hash in [0, 1)."""
    v = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((v ^ (v >> 16)) & 0xFFFF) / 65536.0


# --------------------------------------------------------------------------
# Floors: 16x16, opaque, bottom layer. Each has plain, top (under a wall),
# left (along a left edge) and corner variants, and may have an alternate
# plain sprinkled through empty floor.
# --------------------------------------------------------------------------

SHADE = {
    "terracotta": ("floor", {"T": "x", "t": "u", "x": "u", "u": "v", "v": "g"}),
    "boards": ("floor", {"W": "m", "m": "n", "n": "j"}),
    "flags": ("floor", {"L": "y", "l": "q", "y": "q", "q": "Q"}),
    "earth": ("floor", {"W": "m", "m": "n", "n": "j", "u": "v", "j": "g", "x": "u"}),
    "darkflags": ("stone", {"5": "4", "4": "3", "3": "2", "2": "1", "1": "k", "m": "2"}),
}


def _shade(img, material, mask):
    pal, m = SHADE[material]
    dark = recolor(img, pal, m)
    out = img.copy()
    out[mask] = dark[mask]
    return out


def floor_variants(material, base, alt=None, shade_as=None):
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    s = shade_as or material
    out = {"plain": base, "top": _shade(base, s, top), "left": _shade(base, s, left),
           "corner": _shade(base, s, top | left)}
    if alt is not None:
        out["alt"] = alt
    return out


def floor_earth():
    """Packed earth: board browns with a reddish cast, a few pebbles and cracks.
    Tiles seamlessly (the noise is periodic over 16)."""
    return _earth(3, [(3, 4), (11, 10), (13, 2)], [(5, 8), (6, 8), (7, 9), (8, 9)])


def _earth(seed, pebbles, crack):
    g = [["n"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            r = noise(x, y, seed)
            # soft patches: a dusty lighter tone where two neighbours agree
            if r < 0.10 and noise(x + 1, y, seed) < 0.5:
                g[y][x] = "m"
                if x + 1 < 16:
                    g[y][x + 1] = "m"
            elif r < 0.13:
                g[y][x] = "u"
            elif r < 0.15:
                g[y][x] = "j"
    for (x, y) in pebbles:
        g[y][x] = "W"
        g[y + 1][x] = "j"
    for (x, y) in crack:
        g[y][x] = "j"
    return rows_to_grid("floor", g)


def floor_earth_alt():
    return _earth(11, [(9, 5), (2, 12)], [])


def floor_darkflags(worn=False):
    """Dark grey flags for cellars and the Kadmeia's old houses: one big square
    slab per cell, a lit top-left bevel, a low bottom-right, dark joints."""
    g = [["3"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if x == 15 or y == 15:
                g[y][x] = "1"
            elif x == 14 or y == 14:
                g[y][x] = "2"
            elif x == 0 or y == 0:
                g[y][x] = "4"
    specks = [(4, 5, "2"), (5, 5, "2"), (10, 9, "4"), (9, 11, "2"), (3, 11, "4"), (12, 3, "2")]
    if worn:
        specks = [(6, 4, "2"), (11, 10, "2"), (12, 10, "2"), (4, 12, "4"), (8, 7, "m")]
    for (x, y, c) in specks:
        g[y][x] = c
    return rows_to_grid("stone", g)


def dapple(base, seed):
    """Limestone under a vine pergola: leaf shadows in soft blobs, a few sun
    flecks. Periodic over 16 so neighbours join."""
    yy, xx = np.mgrid[0:16, 0:16]
    blobs = [(3, 3, 3.2), (11, 2, 2.4), (7, 9, 3.6), (14, 12, 2.6), (1, 12, 2.2)]
    if seed:
        blobs = [(13, 4, 3.0), (5, 1, 2.2), (9, 10, 3.4), (2, 8, 2.6), (12, 14, 2.0)]
    m = np.zeros((16, 16), bool)
    for (bx, by, r) in blobs:
        dx = np.minimum(abs(xx - bx), 16 - abs(xx - bx))
        dy = np.minimum(abs(yy - by), 16 - abs(yy - by))
        d = np.sqrt(dx * dx + dy * dy * 1.3)
        m |= d < r + (noise(bx, by, seed) - 0.5)
    m &= ~((xx + yy) % 5 == 0)        # ragged edges
    out = _shade(base, "flags", m)
    for (x, y) in ([(9, 6), (2, 4)] if not seed else [(6, 13), (15, 6)]):
        out[y, x, :3] = PALETTES["floor"]["L"]
    return out


FLOORS = {
    "terracotta": OA.FLOORS["terracotta"],
    "boards": OA.FLOORS["boards"],
    "flags": OA.FLOORS["flags"],
    "earth": floor_variants("earth", floor_earth(), floor_earth_alt()),
    "darkflags": floor_variants("darkflags", floor_darkflags(), floor_darkflags(True)),
}
_d0, _d1 = dapple(OA.FLOORS["flags"]["plain"], 0), dapple(OA.FLOORS["flags"]["plain"], 1)
FLOORS["dappled"] = floor_variants("flags", _d0, _d1)

# --------------------------------------------------------------------------
# Walls. A style is a list of courses, top to bottom; each course is a list of
# 16x16 variants, picked by x. A wall n cells tall draws the style's last n
# courses (so a 2-tall wall skips a 3-course style's top).
# --------------------------------------------------------------------------

def _thyrsa_wall():
    """Thyrsa: a dark beam with rafter ends over lime plaster; a wine-dark dado
    carrying an ochre running-wave scroll between ochre lines."""
    rows = []
    rows.append("k" * 16)                       # 0 ceiling edge
    rows.append("2" * 16)                       # 1 beam
    rows.append("3" * 16)                       # 2 beam, lit
    rows.append("2" * 16)                       # 3
    rows.append("1" * 16)                       # 4 beam underside
    rows.append("s23321sss23321ss")             # 5 rafter ends
    rows.append("s12211sss12211ss")             # 6
    rows.append("ps1111spps1111sp")             # 7
    rows.append("pppssssppppssssp")             # 8
    for _ in range(9, 21):
        rows.append("p" * 16)                   # 9-20 plaster
    rows.append("s" * 16)                       # 21 shade under the moulding
    rows.append("o" * 16)                       # 22 ochre line
    WAVE = [                                    # 23-29: an 8-wide running wave
        "RRRRRRRR",
        "RRRooRRR",
        "RRoRRoRR",
        "RoRRoRoR",
        "oRRooRRo",
        "oooRRRoo",
        "oooooooo",
    ]
    for wr in WAVE:
        rows.append(wr * 2)
    rows.append("D" * 16)                       # 30
    rows.append("k" * 16)                       # 31 skirting
    rows = [list(r) for r in rows]
    for (x, y, c) in [(3, 11, "w"), (10, 13, "w"), (13, 17, "s"), (6, 18, "w"), (1, 16, "s"), (12, 10, "w")]:
        rows[y][x] = c
    img = rows_to_grid("wall", rows)
    return [[img[:16]], [img[16:]]]


def _eleu_wall():
    """Eleutherai: round log beams with their cut ends showing, whitewash
    rubbed thin, over a footing of rough fieldstone."""
    up = []
    up.append("k" * 16)
    up.append("1222222222222221")
    up.append("2333333333333332")
    up.append("2232323232323222")
    up.append("1111111111111111")
    up.append("sk22ksssssk22kss")               # 5-8 round log ends
    up.append("k2332kssssk2332k")
    up.append("k2132ksssk21232k"[:16])
    up.append("sk22kspppsk22ksp"[:16])
    for _ in range(9, 16):
        up.append("p" * 16)
    up = [list(r) for r in up]
    for (x, y, c) in [(4, 11, "s"), (12, 13, "w"), (8, 10, "s"), (1, 14, "w"), (14, 9, "s")]:
        up[y][x] = c
    upper = rows_to_grid("wall", up)
    lo = []
    for y in range(8):
        lo.append("p" * 16)
    lo = [list(r) for r in lo]
    for (x, y, c) in [(2, 1, "s"), (9, 3, "w"), (13, 2, "s"), (6, 6, "s"), (7, 7, "s"), (11, 7, "S")]:
        lo[y][x] = c
    top = rows_to_grid("wall", lo)
    # fieldstone footing, rows 8-15 of the lower cell (its own tiles, stone)
    st = [
        "1444451444445144",
        "4333351433335133",
        "3332212333221333",
        "1111111111111111",
        "5444451544441544",
        "3333213333321333",
        "2222212222212222",
        "kkkkkkkkkkkkkkkk",
    ]
    foot = grid("stone", "\n".join(st))
    lower = np.concatenate([top, foot], 0)
    return [[upper], [lower]]


def _ashlar(seed_rows):
    """Squared blocks in running bond, 8 px courses, for the fort."""
    rows = []
    for ci, off in enumerate(seed_rows):
        course = []
        for y in range(8):
            r = []
            for x in range(16):
                bx = (x + off) % 16
                if y == 7:
                    r.append("1")
                elif bx == 0:
                    r.append("1")
                elif y == 0:
                    r.append("5" if bx < 12 else "4")
                elif bx == 15 or y == 6:
                    r.append("2")
                elif bx == 1:
                    r.append("4")
                else:
                    v = noise(x, y + ci * 8, 7)
                    r.append("2" if v < 0.07 else ("4" if v > 0.93 else "3"))
            course.append(r)
        rows += course
    return rows


def _fort_wall():
    """The fort's barrack: a heavy timber plate, then ashlar of grey Kithairon
    limestone, darker toward the floor."""
    up = [list("k" * 16), list("eEEEEEEEEEEEEEEe"), list("EhhhhhhhhhhhhhhE"),
          list("eEEeEEEEEEeEEEEe"), list("1eeeeeeeeeeeeee1"), list("1" * 16)]
    body = _ashlar([0, 8, 0])[:10]
    upper = rows_to_grid("stone", up + body)
    lower_rows = _ashlar([8, 0])
    lower_rows[15] = list("k" * 16)
    for x in range(16):
        if lower_rows[14][x] == "3":
            lower_rows[14][x] = "2"
        if lower_rows[13][x] == "3" and noise(x, 13, 2) < 0.5:
            lower_rows[13][x] = "2"
    for (x, y) in [(4, 11), (12, 3)]:
        lower_rows[y][x] = "m"
    lower = rows_to_grid("stone", lower_rows)
    return [[upper], [lower]]


def _cyclopean():
    """Chthonia's house: huge rough polygonal boulders, the oldest walls in the
    city. A 48x32 field (three cells wide) so the stones don't repeat often."""
    W, H = 48, 32
    seeds = [(5, 6), (19, 4), (33, 7), (44, 3), (10, 20), (26, 19), (40, 22), (2, 28),
             (16, 30), (34, 29), (47, 27)]

    def owner(x, y):
        best, bi = None, 0
        for i, (sx, sy) in enumerate(seeds):
            dx = min(abs(x - sx), W - abs(x - sx))
            dy = abs(y - sy)
            d = dx * dx + dy * dy * 1.4
            if best is None or d < best:
                best, bi = d, i
        return bi
    own = [[owner(x, y) for x in range(W)] for y in range(H)]
    g = []
    for y in range(H):
        row = []
        for x in range(W):
            o = own[y][x]
            right = own[y][(x + 1) % W]
            down = own[y + 1][x] if y + 1 < H else o
            up = own[y - 1][x] if y > 0 else o
            left = own[y][(x - 1) % W]
            if o != right or o != down:
                row.append("1")
            elif o != up or o != left:
                row.append("5" if noise(x, y, o) < 0.7 else "4")
            else:
                # each boulder gets its own tone, shaded toward its lower right
                base = "3" if o % 3 else "4"
                n = noise(x, y, 17)
                if n < 0.08:
                    row.append("2")
                elif n > 0.95:
                    row.append("5")
                else:
                    row.append(base)
        g.append(row)
    # shade the lower-right inside edges of each stone
    for y in range(H - 1, 0, -1):
        for x in range(W):
            if g[y][x] == "1" and g[y - 1][x] in "34":
                g[y - 1][x] = "2"
    for (x, y) in [(7, 9), (8, 9), (8, 10), (30, 23), (31, 23), (21, 12), (41, 15), (42, 15)]:
        g[y][x] = "m"
    for (x, y) in [(8, 8), (31, 22), (42, 14)]:
        g[y][x] = "M"
    g[0] = list("k" * W)
    g[H - 1] = list("k" * W)
    img = rows_to_grid("stone", g)
    upper = [img[0:16, i * 16:(i + 1) * 16] for i in range(3)]
    lower = [img[16:32, i * 16:(i + 1) * 16] for i in range(3)]
    return [upper, lower]


def _cellar_vault():
    """The Kantharos's barrel vault, seen end on: voussoirs curving away into
    the dark at the top of the wall. Course 0 of the cellar style."""
    g = []
    for y in range(16):
        row = []
        for x in range(16):
            band = (y + (x // 4) % 2 * 2) // 4          # staggered voussoirs
            if y < 3:
                row.append("k" if y < 2 else "1")
            elif (x + band * 2) % 8 == 0 or y % 4 == 3:
                row.append("1")
            else:
                n = noise(x, y, 23)
                row.append("2" if n < 0.6 else "3")
        g.append(row)
    return rows_to_grid("stone", g)


def _cellar_base():
    """Rough cellar wall under the frieze, lamp-warmed at the top."""
    rows = _ashlar([4, 12])
    for x in range(16):
        rows[15][x] = "k"
        if rows[14][x] == "3":
            rows[14][x] = "2"
    return rows_to_grid("stone", rows)


# The satyrs-and-maenads frieze, black figure on a terracotta ground (clay).
# Four cells; the maenads are winning. Each figure stands on the ground line.
FRIEZE = {
    "satyr_run": """
kkkkkkkkkkkkkkkk
dddddddddddddddd
mmmmmmmmmmmmmmmm
mmmmmmkkmmmmmmmm
mmmmmkkkkmmmmmmm
mmmmkkmkkmkmmmmm
mmmmmmkkkkkmmmmm
mmmmmmkkkmmkmmmm
mmmmmmkkkmmmkmmm
mmmmmkkmkkmmmmmm
mmmmkkmmmkkmmmmm
mmmkkmmmmmkkmmmm
mmkkmmmmmmmkkmmm
mmmmmmmmmmmmmmmm
dddddddddddddddd
kkkkkkkkkkkkkkkk
""",
    "maenad_thyrsus": """
kkkkkkkkkkkkkkkk
dddddddddddddddd
mmmmmmmmmlmmmmmm
mmmmmmmmlklmmmmm
mmmmkkmmmkmmmmmm
mmmkkkkmmkmmmmmm
mmmmkkmmkkmmmmmm
mmmkkkkkkmmmmmmm
mmkmkkkmmkmmmmmm
mmmmkkkkmkmmmmmm
mmmkkkkkkmmmmmmm
mmkkkkkkkkmmmmmm
mmmkmmmmkmmmmmmm
mmmmmmmmmmmmmmmm
dddddddddddddddd
kkkkkkkkkkkkkkkk
""",
    "satyr_fall": """
kkkkkkkkkkkkkkkk
dddddddddddddddd
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmkkmmmmmmmmmmm
mmkkkkmmmmmmmmmm
mmkmkkkkmmmmmmmm
mmmmmkkkkkkmmmmm
mmmmkkkkkkkkkmmm
mmmkkmmmmkkmmkmm
mmkkmmmmmmkkmmmm
mmmmmmmmmmmkkmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
dddddddddddddddd
kkkkkkkkkkkkkkkk
""",
    "maenad_dance": """
kkkkkkkkkkkkkkkk
dddddddddddddddd
mmmmmmmmmmmmmmmm
mmmmmmmmkkmmmmmm
mmmmmmmkkkkmmmmm
mmmmkmmmkkmmmkmm
mmmmmkkkkkkkkmmm
mmmmmmmkkkkmmmmm
mmmmmmkkkkkkmmmm
mmmmmkkkkkkkkmmm
mmmmkkkkkkkkkkmm
mmmmmmmkmmkmmmmm
mmmmmmkkmmkkmmmm
mmmmmmmmmmmmmmmm
dddddddddddddddd
kkkkkkkkkkkkkkkk
""",
}


def _frieze_cells():
    out = []
    for name in ("satyr_run", "maenad_thyrsus", "satyr_fall", "maenad_dance"):
        img = grid("clay", FRIEZE[name])
        # incised details and highlights: a lighter clay rim on the figures
        out.append(img)
    return out


WALLS = {
    "thyrsa": _thyrsa_wall(),
    "eleu": _eleu_wall(),
    "fort": _fort_wall(),
    "cyclopean": _cyclopean(),
    "cellar": [[_cellar_vault()], _frieze_cells(), [_cellar_base()]],
}

VOID = grid("wall", "\n".join(["k" * 16] * 16))

# --------------------------------------------------------------------------
# The ivy festoon Thyrsa hangs along its beams: nature, middle layer, laid by
# the builder over bare upper-wall cells in rooms that ask for it.
# --------------------------------------------------------------------------

IVY = [grid("nature", """
................
................
................
G..............G
gGG..........GGg
.vgGG......GGgv.
..VgggG..GGggV..
...kgvgggggvgk..
....kgVggVgGk...
.....GkgggkG....
......kGPGk.....
.......pPp......
.......kpk......
................
................
................
"""), grid("nature", """
................
................
................
G..............G
gG...........GGg
.gGG.......GGgv.
..vggGG..GGgg...
...kVgggggVgk...
....kGgvgGgk....
.....kGgggk.....
......kGgk......
.......kk.......
................
................
................
................
""")]

# --------------------------------------------------------------------------
# Stamps. A stamp is a whole number of cells. Its art goes on the middle layer
# (drawn under walkers), its `top` art on the top layer (over walkers), and its
# `flat` art into the bottom layer over the floor or wall (the flat art and the
# base must share a palette in every 8x8 tile).
# --------------------------------------------------------------------------

STAMPS = {}


def _art(parts, w, h):
    """parts: a grid string, an RGBA array, or a list of (palette, grid) or
    arrays overlaid in order."""
    if parts is None:
        return None
    if isinstance(parts, np.ndarray):
        assert parts.shape[:2] == (h * 16, w * 16), (parts.shape, w, h)
        return parts
    out = blank(w, h)
    for p in parts:
        if isinstance(p, np.ndarray):
            img = p
        else:
            pal, text = p
            img = grid(pal, text, w * 16, h * 16)
        assert img.shape[:2] == (h * 16, w * 16), (img.shape, w, h)
        out = over(out, img)
    return out


def stamp(name, w, h, art=None, top=None, flat=None, walk=(), behavior=None, note="", pal=""):
    """w, h in cells. art/top/flat: see _art. walk: cells (cx, cy) a walker may
    stand on. behavior: {(cx, cy): 'MB_...'}."""
    assert name not in STAMPS, f"stamp {name} defined twice"
    STAMPS[name] = {
        "w": w, "h": h,
        "img": _art(art, w, h) if art is not None else blank(w, h),
        "top": _art(top, w, h),
        "flat": _art(flat, w, h),
        "walk": set(walk),
        "behavior": dict(behavior or {}),
        "note": note,
        "pal": pal,
    }
    return STAMPS[name]


def reuse(name, oikia_name=None, note=None, **kw):
    """Register one of oikia's pieces as it is drawn (its colors are in these
    palettes)."""
    src = OA.STAMPS[oikia_name or name]
    s = stamp(name, src["w"], src["h"], art=src["img"].copy(),
              top=None if src["top"] is None else src["top"].copy(),
              walk=kw.get("walk", src["walk"]), behavior=kw.get("behavior", src["behavior"]),
              note=note or src["note"] + " (oikia)", pal=src["pal"])
    return s


# Pieces shared with oikia, unchanged.
for _n in ("window", "kline", "klismos_r", "klismos_l", "stool", "table", "table_round", "desk",
           "amphora", "amphora_plain", "pithos", "pots", "mortar", "hearth", "soot", "kalathos",
           "lampstand", "chest", "herbs"):
    reuse(_n)
reuse("mat", walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"})
