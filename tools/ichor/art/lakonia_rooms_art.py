#!/usr/bin/env python3
"""Pixel art for Lakonia's rooms: Gytheion's five and Lakonia's ten.

Drawn the way limen is (hand-drawn character grids, char_canvas.Canvas for the
bigger pieces) in oikia's seven palettes, so every piece of the slice's
furniture (tables, stools, chests, jars, the loom, the hearth, the mat) can
stand in these rooms pixel for pixel. limen_art.py's palettes are used as they
are; its cloth palette already carries Tyrian purple for Gytheion's dye.

Lakonia's rooms are austere (STYLE §4.7: "austere, not grand"): bare lime
plaster over mudbrick, beaten earth floors, nothing on the walls that isn't
used. Gytheion's are a harbor's: whitewash, the sea in every window, and
purple on everything.

tools/ichor/maps/lakonia_rooms.py lays out the rooms and builds the three
secondaries (oikia_gytheion, oikia_lakonia, civic_lakonia) from this module.
"""
import copy

import numpy as np

import ergasteria_art as EA
import limen_art as L
import oikia_art as O
from char_canvas import Canvas

PALETTES = copy.deepcopy(L.PALETTES)
grid = L.grid
as_text = L.as_text
VOID = L.VOID
RUGS = {"red": O.RUGS["red"]}

STAMPS = {}
for _n in ("window", "niche", "kline", "stool", "table", "chest", "loom", "amphora", "amphora_plain",
           "pithos", "pots", "hearth", "soot", "myrtle", "kalathos", "fish_basket", "knucklebones",
           "lampstand", "column", "mat", "nets", "herbs", "jar_shelf", "table_round", "klismos_r",
           "klismos_l", "altar", "mortar", "scrolls", "desk", "oars"):
    STAMPS[_n] = dict(O.STAMPS[_n], source="oikia")
for _n in ("bench", "scales", "hearth_floor"):
    STAMPS[_n] = dict(EA.STAMPS[_n], source="ergasteria")
for _n in ("sea_window", "water_jar", "curtain_bed", "pallet", "sack", "louterion", "krater",
           "kline_side", "kline_side_r", "counter_plank"):
    STAMPS[_n] = dict(L.STAMPS[_n], source="limen")


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note=""):
    """oikia's contract: w, h in metatiles; walk cells the player may stand on;
    behavior per cell; top art drawn over the player; flatten into the floor."""
    if isinstance(art, Canvas):
        art = art.text()
    img = art if isinstance(art, np.ndarray) else grid(pal, art, w * 16, h * 16)
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    if isinstance(top, Canvas):
        top = top.text()
    STAMPS[name] = {
        "pal": pal, "img": img,
        "top": (top if isinstance(top, np.ndarray) else grid(pal, top, w * 16, h * 16)) if top is not None else None,
        "w": w, "h": h, "walk": set(walk), "behavior": dict(behavior or {}),
        "flatten": flatten, "note": note, "source": "lakonia_rooms",
    }


def layered(name, parts, w, h, walk=(), behavior=None, note="", flatten=False):
    """A piece drawn in several palettes: `parts` is [(pal, Canvas), ...], later
    over earlier. Every 8x8 tile must end up in one palette (the builder checks)."""
    img = np.zeros((h * 16, w * 16, 4), np.uint8)
    for pal, c in parts:
        a = c if isinstance(c, np.ndarray) else grid(pal, c.text() if isinstance(c, Canvas) else c, w * 16, h * 16)
        m = a[..., 3] > 0
        img[m] = a[m]
    stamp(name, parts[0][0], img, w, h, walk=walk, behavior=behavior, note=note, flatten=flatten)


def lower(img, pal, from_row=8):
    """A piece with its pixel rows above `from_row` cleared (for layered pieces
    whose upper 8x8 tiles are drawn in another palette)."""
    rows = as_text(img, pal)
    return grid(pal, "\n".join(["." * len(rows[0])] * from_row + rows[from_row:]))


def recolored(src, pal, mapping, region=None):
    """A copy of an RGBA piece with some characters swapped (region: x0,y0,x1,y1)."""
    rows = [list(r) for r in as_text(src, pal)]
    x0, y0, x1, y1 = region or (0, 0, len(rows[0]) - 1, len(rows) - 1)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if rows[y][x] in mapping:
                rows[y][x] = mapping[rows[y][x]]
    return grid(pal, "\n".join("".join(r) for r in rows))


# ===========================================================================
# Floors and walls
# ===========================================================================

FLOORS = {k: dict(v) for k, v in L.FLOORS.items() if k in ("terracotta", "boards", "flags")}


def _earth(variant):
    """Beaten earth: the floor of every Lakonian house. Packed brown with a
    speckle of grit that repeats every 8 pixels, shadowed under the wall."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            h = ((x % 8) * 37 + (y % 8) * 19 + (x % 8) * (y % 8) * 5) % 29
            c.put(x, y, "j" if h in (0, 13) else "y" if h == 7 else "n" if h in (20,) else "m")
    if variant in ("top", "corner"):
        c.hline(0, 15, 0, "g")
        c.hline(0, 15, 1, "j")
        for x in range(0, 16, 2):
            c.put(x, 2, "j")
    if variant in ("left", "corner"):
        c.vline(0, 0, 15, "g")
        c.vline(1, 0, 15, "j")
    if variant == "alt":
        for (x, y, ch) in [(3, 3, "q"), (4, 3, "y"), (11, 9, "j"), (12, 10, "q"), (6, 12, "y")]:
            c.put(x, y, ch)
    return grid("floor", c.text())


FLOORS["earth"] = {v: _earth(v) for v in ("plain", "alt", "top", "left", "corner")}


def _sand(variant):
    """The palaestra's wrestling pit: raked pale sand in a dark stone kerb (the
    kerb is the 'left'/'top' shading), ridged by the rake every 4 rows."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            h = ((x % 8) * 29 + (y % 8) * 13) % 23
            c.put(x, y, "l" if y % 4 == 3 and (x + y) % 3 else ("y" if h in (0, 9) else "L"))
    if variant in ("top", "corner"):
        c.hline(0, 15, 0, "j")
        c.hline(0, 15, 1, "Q")
        c.hline(0, 15, 2, "q")
    if variant in ("left", "corner"):
        c.vline(0, 0, 15, "j")
        c.vline(1, 0, 15, "Q")
        c.vline(2, 0, 15, "q")
    return grid("floor", c.text())


FLOORS["sand"] = {v: _sand(v) for v in ("plain", "top", "left", "corner")}


def _court(variant):
    """Orthia's court: worn limestone flags with marsh grass in the joints."""
    base = as_text(L.FLOORS["flags"][variant if variant in L.FLOORS["flags"] else "plain"], "floor")
    rows = [list(r) for r in base]
    for (x, y) in ((0, 7), (1, 7), (7, 0), (7, 1), (8, 15), (15, 8), (14, 8)):
        if rows[y][x] in "qQy":
            rows[y][x] = "j"
    return grid("floor", "\n".join("".join(r) for r in rows))


FLOORS["court"] = {v: _court(v) for v in ("plain", "top", "left", "corner")}

WALLS = {"red": O.WALLS["red"], "blue": O.WALLS["blue"], "stone": EA.WALLS["stone"]}


def _wall_lakon():
    """A Lakonian wall: a plain timber beam, tan lime plaster over mudbrick,
    worn through in places to the brick, on a rubble footing. No dado, no
    paint: Lykourgos said a house should be built with an axe and a saw."""
    rows = ["k" * 16, "1" * 16, "2" * 16, "3" * 16, "1" * 16, "k" * 16]
    for y in range(6, 27):
        row = []
        for x in range(16):
            h = (x * 7 + y * 13 + x * y) % 17
            row.append("S" if h == 0 else ("s" if h in (4, 9, 12) else "p"))
        rows.append("".join(row))
    rows += ["S" * 16, "SsSSsSSSsSSSsSsS", "s" * 16, "S" * 16, "k" * 16]
    assert len(rows) == 32, len(rows)
    return grid("wall", "\n".join(rows))


def _wall_smoke():
    """The syssition's wall: no windows, fifteen men's soot. The plaster is
    black at the top and only browns toward the footing."""
    rows = as_text(_wall_lakon(), "wall")
    out = []
    for y, r in enumerate(rows):
        r = list(r)
        for x in range(16):
            if 6 <= y < 27 and r[x] in "psSRD":
                h = (x * 5 + y * 3) % 7
                if y < 20:
                    r[x] = "1" if h else "k"
                else:
                    r[x] = "2" if h else "1"
        out.append("".join(r))
    return grid("wall", "\n".join(out))


def _wall_sayings():
    """Chilon's wall: the plaster scratched floor to ceiling with sayings of one
    or two words each, in a hundred hands."""
    rows = [list(r) for r in as_text(_wall_lakon(), "wall")]
    for y in range(6, 27):
        for x in range(16):
            if rows[y][x] in "RD":
                rows[y][x] = "p"
    marks = [(7, 1, 4), (7, 7, 3), (10, 3, 5), (10, 11, 3), (13, 0, 3), (13, 6, 6), (16, 2, 4),
             (16, 9, 5), (19, 1, 3), (19, 6, 2), (22, 3, 6), (22, 11, 4), (25, 0, 2), (25, 8, 5)]
    for (y, x0, n) in marks:
        for i in range(n):
            x = x0 + i
            if x < 16:
                rows[y][x] = "S" if (x * 3 + y) % 4 else "1"
                if (x + y) % 3 == 0 and y + 1 < 27:
                    rows[y + 1][x] = "S"
    return grid("wall", "\n".join("".join(r) for r in rows))


def _wall_white():
    """Kranai's shrine: whitewash all the way down, a pink wash at the foot for
    the goddess, the beam painted blue."""
    rows = ["k" * 16, "b" * 16, "B" * 16, "b" * 16, "k" * 16, "S" * 16]
    for y in range(6, 27):
        rows.append("".join("p" if (x * 11 + y * 5) % 23 == 0 else "w" for x in range(16)))
    rows += ["o" * 16, "r" * 16, "r" * 16, "R" * 16, "k" * 16]
    return grid("wall", "\n".join(rows))


WALLS["lakon"] = _wall_lakon()
WALLS["smoke"] = _wall_smoke()
WALLS["sayings"] = _wall_sayings()
WALLS["white"] = _wall_white()


# ===========================================================================
# Lampito's kitchen
# ===========================================================================

def _stele(kind):
    """A grave-stele painted on the plaster: a pale slab with a little pediment.
    AGIS (in war, so his name is on it) or a swallow, painted small."""
    c = Canvas(16, 32)
    c.paste(["......kk......",
             ".....kssk.....",
             "....kswwsk....",
             "...kswwwwsk...",
             "..kkkkkkkkkk.."], 1, 3)
    c.box(3, 8, 12, 27, "w")
    c.vline(11, 9, 26, "s")
    c.hline(4, 11, 26, "s")
    c.hline(2, 13, 28, "S")
    c.hline(2, 13, 29, "k")
    if kind == "agis":
        # A G I S in three-pixel letters, red ochre, and a small spear under it
        c.paste(["R.RR", "RRR.", "R.RR"], 4, 11)       # "A" and half a "G", squeezed
        c.paste(["RR.R.RR", "R..R.R.", "RR.R..R"], 4, 15)
        c.vline(7, 19, 25, "1")
        c.put(7, 18, "k")
        c.put(6, 19, "1")
        c.put(8, 19, "1")
    else:
        # a swallow, wings back, forked tail
        c.paste([".b....b.",
                 "bbb..bbb",
                 ".bBBBBb.",
                 "..bBBb..",
                 "...bb...",
                 "..b..b.."], 4, 14)
        c.put(7, 16, "w")
    return c


stamp("stele_agis", "wall", _stele("agis"), 1, 2,
      note="a grave-stele painted on the plaster: AGIS, IN WAR (only the war dead get names)")
stamp("stele_swallow", "wall", _stele("swallow"), 1, 2,
      note="a grave-stele painted on the plaster, with no name: a small swallow")


def _loom_cloak():
    """oikia's loom with a small red cloak on it, nearly finished."""
    img = recolored(O.STAMPS["loom"]["img"], "wood", {"u": "R", "U": "r", "c": "r", "C": "R"},
                    region=(5, 10, 26, 34))
    return img


stamp("loom_cloak", "wood", _loom_cloak(), 2, 3,
      note="a loom with a small red cloak on it. Too small for anyone in this house")


def _hearth_cold():
    """The hearth_floor stone, cold: grey ash and a few black brands."""
    return recolored(EA.STAMPS["hearth_floor"]["img"], "clay",
                     {"Y": "t", "F": "S", "f": "s", "c": "t", "d": "a"})


stamp("hearth_cold", "clay", _hearth_cold(), 2, 2,
      note="a hearth of stones, cold: ash, and nobody's lit it in a long time")
stamp("hearth_lit", "clay", EA.STAMPS["hearth_floor"]["img"], 2, 2,
      note="the same hearth, lit: someone's home")


# ===========================================================================
# Gylippos: a strap, a mat, a stool, and twelve identical staffs
# ===========================================================================

def _staff_rack():
    """Twelve scytale staffs of exactly the same thickness on wall pegs, each
    with a name burned in; the elders' staffs, read only by their twins."""
    c = Canvas(48, 32)
    c.hline(0, 47, 3, "k")
    c.hline(0, 47, 4, "d")
    c.hline(0, 47, 5, "k")
    for i in range(12):
        x = 2 + i * 4
        c.vline(x, 6, 29, "k")
        c.vline(x + 1, 6, 29, "m")
        c.vline(x + 2, 6, 29, "d")
        c.put(x + 1, 6, "l")
        for y in range(10 + (i % 3) * 3, 24, 5):
            c.put(x + 1, y, "k")
        c.hline(x, x + 2, 30, "k")
    return c


stamp("staff_rack", "wood", _staff_rack(), 3, 2,
      note="the elders' scytale staffs on pegs: a dozen, all exactly as thick, a name burned into each")


def _sleeping_mat():
    c = Canvas(16, 32)
    c.box(2, 3, 13, 29, "J")
    for y in range(4, 29):
        for x in range(3, 13):
            c.put(x, y, "j" if (y + (x // 3)) % 4 == 0 else "J")
    c.hline(3, 12, 6, "K")
    return c


stamp("sleeping_mat", "nature", _sleeping_mat(), 1, 2,
      note="a sleeping mat of cut reeds on the bare floor")


def _stool_strap():
    img = O.STAMPS["stool"]["img"].copy()
    c = Canvas(16, 16)
    c.paste([".kkkk.",
             "kdmmdk",
             "kmkkmk",
             "kdmmdk",
             ".kkkk."], 5, 2)
    a = grid("wood", c.text())
    m = a[..., 3] > 0
    img[m] = a[m]
    return img


stamp("stool_strap", "wood", _stool_strap(), 1, 1,
      note="Gylippos's stool, a leather strap coiled on it")


# ===========================================================================
# Chilon: the IF shard
# ===========================================================================

def _if_shelf():
    c = Canvas(16, 32)
    c.hline(1, 14, 20, "k")
    c.hline(1, 14, 21, "l")
    c.hline(1, 14, 22, "m")
    c.hline(1, 14, 23, "k")
    c.put(2, 24, "k")
    c.put(13, 24, "k")
    c.paste(["..kkkk..",
             ".kmllmk.",
             "kmlkhkhk",
             "kmlkhkhk",
             "kmlkhkk.",
             ".kkkkk.."], 4, 14)
    return c


stamp("if_shelf", "clay", _if_shelf(), 1, 2,
      note="a pottery shard on a shelf with one word on it: IF")


# ===========================================================================
# Lichas: cushions, an Olympic tripod with someone else's name on it, figs
# ===========================================================================

def _cushions():
    c = Canvas(32, 16)
    for (x, y, f, s) in ((1, 6, "r", "R"), (10, 4, "o", "R"), (19, 6, "u", "i"), (8, 9, "y", "o")):
        c.box(x, y, x + 11, y + 6, f)
        c.hline(x + 1, x + 10, y + 5, s)
        c.put(x + 1, y + 1, "c")
    return c


stamp("cushions", "cloth", _cushions(), 2, 1,
      note="a heap of cushions. The only cushions in Lakonia; the neighbors find them suspicious")


def _tripod():
    c = Canvas(16, 32)
    c.paste(["...kk......kk...",
             "..kyyk....kyyk..",
             "..kbbk....kbbk..",
             ".kkkkkkkkkkkkkk.",
             "kbyyyyyyyyyyyybk",
             "kzbbbbbbbbbbbbzk",
             ".kzbbbbbbbbbbzk.",
             "..kkkkkkkkkkkk.."], 0, 4)
    for x in (3, 7, 12):
        c.vline(x, 12, 27, "k")
        c.vline(x + 1, 12, 27, "b")
    c.hline(2, 14, 20, "z")
    c.hline(2, 14, 28, "k")
    c.put(6, 8, "Y")
    c.put(9, 8, "Y")
    return c


stamp("tripod", "bronze", _tripod(), 1, 2,
      note="a bronze tripod from Olympia, with someone else's name on it")


def _figs():
    c = Canvas(16, 16)
    c.paste(["....pkp.pkp.....",
             "...pVpppVpp.....",
             "..kppppppppk....",
             ".kJjJjJjJjJjk...",
             ".kjJjJjJjJjJk...",
             "..kKKKKKKKKk....",
             "...kkkkkkkk....."], 1, 7)
    return c


stamp("figs", "nature", _figs(), 1, 1, note="a basket of figs")


# ===========================================================================
# The syssition: the long table, cups on pegs, the black cauldron, barley
# ===========================================================================

def _plank(part):
    """The mess table: one long plank on trestles, a clay cup at every place."""
    c = Canvas(16, 16)
    c.hline(0, 15, 5, "k")
    c.hline(0, 15, 6, "h")
    c.hline(0, 15, 7, "l")
    c.hline(0, 15, 8, "m")
    c.hline(0, 15, 9, "k")
    if part == "L":
        for y in range(5, 10):
            c.put(0, y, "k")
        c.paste(["kmdk", "kmdk", "kkkk"], 1, 10)
    if part == "R":
        for y in range(5, 10):
            c.put(15, y, "k")
        c.paste(["kmdk", "kmdk", "kkkk"], 11, 10)
    if part == "M":
        c.paste(["kmdk", "kmdk", "kkkk"], 6, 10)
    return c


for _p in ("L", "M", "R"):
    stamp(f"plank_{_p}", "wood", _plank(_p), 1, 1, note="the mess table: one long plank on trestles")


def _cup_pegs():
    """Fifteen men's places, each with its own clay cup on a peg above it."""
    c = Canvas(32, 16)
    c.hline(0, 31, 4, "k")
    c.hline(0, 31, 5, "d")
    for i in range(3):
        x = 1 + i * 11
        c.put(x + 3, 6, "k")
        c.paste([".kkkkk.", "kmllhlk", "kmllllkk", "kmlllmkmk", "kdmmmdkk", ".kdddk..", "..kkk..."], x, 7)
    return c


stamp("cup_pegs", "clay", _cup_pegs(), 2, 1, note="clay cups on pegs, one for every man's place")


def _cauldron():
    """The black cauldron on its fire: black broth. Pork, blood, salt, vinegar."""
    c = Canvas(32, 32)
    c.ellipse(16, 13, 13, 5, "k")
    c.ellipse(16, 13, 11, 3.5, "a")
    c.ellipse(16, 13, 9, 2.5, "k")
    c.rect(4, 13, 27, 22, "a")
    c.ellipse(16, 22, 12, 5, "a")
    for y in range(13, 25):
        c.put(4, y, "k")
        c.put(27, y, "k")
        c.put(6, y, "s")
    c.hline(5, 26, 13, "S")
    c.paste(["k.k", ".k."], 2, 12)
    c.paste(["k.k", ".k."], 27, 12)
    # the fire under it
    for (x, ch) in ((7, "f"), (10, "F"), (13, "Y"), (16, "F"), (19, "Y"), (22, "F"), (25, "f")):
        c.vline(x, 25, 28, ch)
        c.put(x, 24, "F" if ch == "Y" else "f")
    c.hline(3, 28, 29, "S")
    c.hline(3, 28, 30, "k")
    # steam
    for (x, y) in ((12, 3), (13, 2), (18, 4), (19, 3), (20, 2), (15, 6)):
        c.put(x, y, "t")
    return c


stamp("cauldron", "clay", _cauldron(), 2, 2, note="the black cauldron over the fire: black broth, the worst soup in the world")


def _barley_barrel():
    c = Canvas(16, 32)
    c.box(2, 6, 13, 29, "m")
    for y in range(7, 29):
        c.put(4, y, "l")
        c.put(11, y, "d")
    for y in (10, 18, 26):
        c.hline(3, 12, y, "k")
    c.ellipse(8, 6, 6, 2, "J" if False else "h")
    c.hline(4, 11, 6, "y")
    return c


stamp("barley", "wood", _barley_barrel(), 1, 2, note="a barrel of barley")


# ===========================================================================
# The agoge: reed mats, the spear rack, cloaks on pegs, the herd's names
# ===========================================================================

def _reed_mat():
    c = Canvas(16, 16)
    c.box(1, 2, 14, 14, "J")
    for y in range(3, 14):
        for x in range(2, 14):
            c.put(x, y, "j" if (x + y // 2) % 3 == 0 else "J")
    c.hline(2, 13, 4, "K")
    return c


stamp("reed_mat", "nature", _reed_mat(), 1, 1, walk={(0, 0)},
      note="a sleeping mat of reeds cut barehanded from the Eurotas. No knives")


def _spear_rack():
    c = Canvas(32, 32)
    c.hline(1, 30, 26, "k")
    c.hline(1, 30, 27, "m")
    c.hline(1, 30, 28, "d")
    c.hline(1, 30, 29, "k")
    c.hline(1, 30, 10, "k")
    c.hline(1, 30, 11, "d")
    for i in range(6):
        x = 3 + i * 5
        c.vline(x, 1, 26, "k")
        c.vline(x + 1, 1, 26, "l")
        c.vline(x + 2, 3, 26, "k")
        c.paste([".k.", "kmk"], x, 0)
    c.vline(1, 10, 29, "k")
    c.vline(30, 10, 29, "k")
    return c


stamp("spear_rack", "wood", _spear_rack(), 2, 2, note="a rack of wooden practice spears, blunted")


def _cloak_pegs():
    c = Canvas(32, 32)
    c.hline(0, 31, 4, "k")
    c.hline(0, 31, 5, "d")
    for i in range(3):
        x = 1 + i * 10
        c.put(x + 4, 6, "k")
        c.paste(["...kkk...",
                 "..krrRk..",
                 ".krrrrRk.",
                 ".krrrrRk.",
                 "krrrrrrRk",
                 "krrrrrrRk",
                 "krrrrrrRk",
                 "krrrrrRRk",
                 "kRrrrrrRk",
                 "kRrrrrRRk",
                 "kRRrrRRRk",
                 "kkkkkkkkk"], x, 7)
    return c


stamp("cloak_pegs", "wood", _cloak_pegs(), 2, 2,
      note="red cloaks on pegs. One cloak a year; you make it last")


def _names_list():
    """The herd's names painted by the door, some struck through: gone north."""
    c = Canvas(32, 32)
    c.box(2, 3, 29, 28, "w")
    for i, y in enumerate(range(6, 27, 3)):
        n = 6 + (i * 5) % 9
        c.hline(5, 5 + n, y, "1")
        c.hline(17, 17 + (n + 3) % 9, y, "1")
        if i in (2, 5):
            c.hline(4, 6 + n, y, "R")
        if i == 4:
            c.hline(16, 19 + (n + 3) % 9, y, "R")
    return c


stamp("names_list", "wall", _names_list(), 2, 2,
      note="the herd's names painted on the plaster; some are struck through")


# ===========================================================================
# The palaestra: flasks and scrapers, six olive crowns, folded cloaks
# ===========================================================================

def _oil_hooks():
    c = Canvas(32, 16)
    c.hline(0, 31, 2, "k")
    c.hline(0, 31, 3, "z")
    for i in range(4):
        x = 2 + i * 8
        c.put(x + 2, 4, "k")
        if i % 2 == 0:       # an aryballos: a round oil flask
            c.paste([".kk.", "kbyk", "kbyyk"[:4], ".kbbk", "kbbyk", "kbbbk", ".kkk."], x, 5)
        else:                # a strigil: the bronze scraper
            c.paste(["kk..", "kbk.", ".kbk", ".kbk", "..kbk", "..kbk", "...kk"], x, 5)
    return c


stamp("oil_hooks", "bronze", _oil_hooks(), 2, 1,
      note="oil flasks and bronze scrapers on hooks")


def _crowns():
    """Six olive crowns from Olympia, dried brown, nailed above the door."""
    c = Canvas(48, 16)
    for i in range(6):
        x = 1 + i * 8
        c.paste(["..KjK..",
                 ".j...j.",
                 "K.....K",
                 "j.....j",
                 ".K...K.",
                 "..jKj.."], x, 4)
        c.put(x + 3, 3, "k")
    return c


stamp("crowns", "nature", _crowns(), 3, 1,
      note="six olive crowns, dried brown, nailed above the door. Olympia, six times")


def _cloak_bench():
    c = Canvas(32, 16)
    for (x, f, s) in ((2, "r", "R"), (11, "C", "n"), (20, "r", "R")):
        c.box(x, 2, x + 9, 7, f)
        c.hline(x + 1, x + 8, 6, s)
    return c


layered("cloak_bench", [("wood", lower(EA.STAMPS["bench"]["img"], "wood")),
                        ("cloth", _cloak_bench())], 2, 1, note="a bench of folded cloaks")


# ===========================================================================
# Artemis Orthia: the willows, the long altar of cheeses, the wooden image
# ===========================================================================

def _willow():
    c = Canvas(32, 48)
    c.ellipse(16, 15, 14, 13, "G")
    c.ellipse(15, 13, 11, 10, "g")
    c.ellipse(13, 10, 6, 5, "v")
    for x in range(3, 30, 2):
        top = 14 if abs(x - 16) > 10 else 20
        c.vline(x, top, 33 + (x * 7) % 5, "G" if x % 4 else "g")
        c.put(x, 34 + (x * 7) % 5, "v")
    c.rect(14, 28, 17, 43, "K")
    c.vline(14, 28, 43, "k")
    c.vline(17, 28, 43, "k")
    c.hline(11, 20, 44, "k")
    c.put(12, 43, "K")
    c.put(19, 43, "K")
    return c


stamp("willow", "nature", _willow(), 2, 3,
      note="a willow. The goddess's image was found in a willow thicket, bound upright")


def _cheese_altar(part):
    """The long stone altar set with round cheeses (the old rite: boys stole
    them while others stood guard)."""
    c = Canvas(16, 16)
    c.rect(0, 6, 15, 13, "t")
    c.hline(0, 15, 5, "k")
    c.hline(0, 15, 14, "k")
    c.hline(0, 15, 12, "S")
    c.hline(0, 15, 13, "s")
    if part == "L":
        c.vline(0, 5, 14, "k")
    if part == "R":
        c.vline(15, 5, 14, "k")
    return c


for _p in ("L", "M", "R"):
    stamp(f"altar_{_p}", "clay", _cheese_altar(_p), 1, 1,
          note="the long stone altar of Artemis Orthia")


def _xoanon():
    """The goddess's wooden image, small and heavy, bound upright in willow."""
    c = Canvas(16, 32)
    c.box(5, 4, 10, 27, "m")
    c.box(6, 4, 9, 8, "h")
    c.put(7, 6, "k")
    c.put(8, 6, "k")
    for y in (12, 16, 20, 24):
        c.hline(4, 11, y, "o")
    c.hline(3, 12, 28, "k")
    c.hline(3, 12, 29, "d")
    return c


stamp("xoanon", "wood", _xoanon(), 1, 2,
      note="Orthia: the goddess's wooden image, small and heavy, bound upright in willow withies")


# ===========================================================================
# Lakonia's Asclepeion and Agora
# ===========================================================================

def _stone_counter(part):
    """A plank laid on two stones: the counter. A bowl of cold water on it."""
    wood = Canvas(16, 16)
    wood.hline(0, 15, 4, "k")
    wood.hline(0, 15, 5, "h")
    wood.hline(0, 15, 6, "l")
    wood.hline(0, 15, 7, "k")
    if part == "L":
        wood.vline(0, 4, 7, "k")
    if part == "R":
        wood.vline(15, 4, 7, "k")
    if part == "M":
        wood.paste([".kkkkkk.", "kuUUUUuk"], 4, 2)
    clay = Canvas(16, 16)
    if part in ("L", "R"):
        clay.paste([".kkkkkk.",
                    "kStttSSk",
                    "kSttSSsk",
                    "kSSSSssk",
                    "kssssssk",
                    ".kkkkkk."], 4, 8)
    return wood, clay


for _p in ("L", "M", "R"):
    _w, _c = _stone_counter(_p)
    layered(f"stone_counter_{_p}", [("wood", _w), ("clay", _c)], 1, 1,
            behavior={(0, 0): "MB_COUNTER"},
            note="Lakonia's counter: a plank on two stones, a bowl of cold water on it")

def _basin_stone():
    """A low marble trough of cold spring water against the wall, fed by a
    spout in the plaster: the Asclepeion's spring. The healer lays the
    Pokemon's balls in the water (the heal animation lands here)."""
    c = Canvas(32, 32)
    # the spout: a lion's-head plaque on the wall above
    c.paste([".kkkk.", "kmMMmk", "kMkkMk", "kmMMmk", ".kuuk.", "..uu..", "..uU..", "..uu.."], 13, 2)
    # the trough, seen from the front and a little above
    c.box(1, 14, 30, 29, "m")
    c.hline(2, 29, 15, "M")
    c.box(3, 16, 28, 22, "n")
    c.rect(4, 17, 27, 21, "u")
    c.hline(4, 27, 17, "U")
    for (x, y) in ((8, 19), (9, 19), (20, 20), (21, 20), (15, 18), (16, 18)):
        c.put(x, y, "a")
    c.hline(2, 29, 25, "n")
    c.vline(10, 23, 28, "n")
    c.vline(21, 23, 28, "n")
    c.hline(1, 30, 30, "k")
    return c


stamp("basin_stone", "bronze", _basin_stone(), 2, 2,
      note="a stone basin of cold spring water. Nothing else")


def _iron_bars():
    """Lakonia's money: iron bars, stacked by the door like firewood."""
    c = Canvas(32, 16)
    for row, y in enumerate((11, 7, 3)):
        for i in range(4 - row):
            x = 2 + row * 3 + i * 7
            c.box(x, y, x + 6, y + 3, "a")
            c.hline(x + 1, x + 5, y + 1, "S")
    return c


stamp("iron_bars", "clay", _iron_bars(), 2, 1,
      note="iron bars stacked like firewood. You can't hide one up your sleeve")


def _great_scales():
    c = Canvas(32, 32)
    c.vline(15, 3, 27, "k")
    c.vline(16, 3, 27, "b")
    c.hline(3, 28, 5, "k")
    c.hline(3, 28, 6, "y")
    c.hline(3, 28, 7, "k")
    for x0 in (2, 22):
        c.line(x0 + 1, 8, x0 + 4, 15, "z")
        c.line(x0 + 7, 8, x0 + 4, 15, "z")
        c.paste(["kkkkkkkkk", "kbyyyyybk", ".kbbbbbk."], x0, 15)
    c.box(11, 27, 20, 30, "z")
    c.put(15, 2, "Y")
    return c


stamp("great_scales", "bronze", _great_scales(), 2, 2,
      note="a great set of scales: everything in Lakonia is weighed")


def _stall_counter(part):
    wood = Canvas(16, 16)
    wood.rect(0, 3, 15, 15, "m")
    wood.hline(0, 15, 2, "k")
    wood.hline(0, 15, 3, "h")
    wood.hline(0, 15, 4, "l")
    wood.hline(0, 15, 15, "k")
    for x in range(2, 16, 5):
        wood.vline(x, 6, 14, "d")
    if part == "L":
        wood.vline(0, 2, 15, "k")
    if part == "R":
        wood.vline(15, 2, 15, "k")
    return wood


for _p in ("L", "M", "R"):
    stamp(f"stall_{_p}", "wood", _stall_counter(_p), 1, 1, behavior={(0, 0): "MB_COUNTER"},
          note="a plank stall counter")


# ===========================================================================
# Gytheion: the stage-building, the dye-works, the harbor-master, the baker,
# the shrine
# ===========================================================================

def _flat(kind):
    """A painted scenery flat leaning on the wall: a palace, or a sea."""
    c = Canvas(32, 32)
    c.box(1, 2, 30, 30, "o")
    c.rect(2, 3, 29, 29, "a")
    if kind == "palace":
        c.paste([".....kkkkkkkkkkkkkkkk.....",
                 "...kkwwwwwwwwwwwwwwwwkk...",
                 ".kkwwwwwwwwwwwwwwwwwwwwkk.",
                 "kkkkkkkkkkkkkkkkkkkkkkkkkk"], 3, 7)
        for x in (5, 10, 15, 20, 25):
            c.rect(x, 11, x + 1, 26, "w")
            c.vline(x + 2, 11, 26, "s")
        c.hline(3, 28, 27, "S")
        c.hline(3, 28, 28, "s")
    else:
        for y in range(3, 30):
            for x in range(2, 30):
                c.put(x, y, "B" if y < 14 else "b")
        for y in (16, 20, 24, 28):
            for x in range(2, 30):
                if (x + y) % 6 in (0, 1):
                    c.put(x, y, "a")
        c.paste(["....k.....",
                 "...kwk....",
                 "..kwwwk...",
                 ".kwwwwwk..",
                 "....k.....",
                 "kRRRRRRRRk",
                 ".kRRRRRRk."], 10, 6)
    return c


stamp("flat_palace", "wall", _flat("palace"), 2, 2, note="a painted scenery flat: a palace")
stamp("flat_sea", "wall", _flat("sea"), 2, 2, note="a painted scenery flat: the sea, and a ship on it")


def _theater_window():
    """The window over the front rows, where patients sit in the sun."""
    c = Canvas(32, 32)
    c.box(1, 6, 30, 29, "k")
    c.rect(2, 7, 29, 28, "a")
    for i, y in enumerate((14, 19, 24)):
        c.rect(2, y, 29, y + 3, "s")
        c.hline(2, 29, y, "w")
        c.hline(2, 29, y + 4, "S")
    c.paste(["kk", "rr", "RR"], 8, 17)
    c.paste(["kk", "bb", "bb"], 20, 22)
    c.hline(0, 31, 30, "w")
    c.hline(1, 30, 31, "S")
    return c


stamp("theater_window", "wall", _theater_window(), 2, 2,
      note="a window over the theater's front rows, where patients sit in the sun")


def _tickets(part):
    """The counter where the actors once sold tickets: bone tokens in a dish."""
    c = Canvas(16, 16)
    c.rect(0, 5, 15, 15, "m")
    c.hline(0, 15, 4, "k")
    c.hline(0, 15, 5, "h")
    c.hline(0, 15, 6, "l")
    c.hline(0, 15, 15, "k")
    for x in range(3, 16, 6):
        c.vline(x, 8, 14, "d")
    if part == "L":
        c.vline(0, 4, 15, "k")
    if part == "R":
        c.vline(15, 4, 15, "k")
    if part == "M":
        c.paste([".kkkkk.", "kcCcCck"], 5, 2)
    return c


for _p in ("L", "M", "R"):
    stamp(f"tickets_{_p}", "wood", _tickets(_p), 1, 1, behavior={(0, 0): "MB_COUNTER"},
          note="the old ticket counter; the healer's counter now")


def _vat():
    """A great lead vat steaming over a low fire, purple to the brim."""
    c = Canvas(32, 32)
    c.ellipse(16, 11, 14, 5, "k")
    c.ellipse(16, 11, 12, 4, "U")
    c.ellipse(16, 11, 10, 3, "p")
    c.ellipse(15, 10, 6, 1.5, "P")
    c.put(13, 10, "q")
    c.rect(3, 12, 28, 24, "u")
    c.ellipse(16, 24, 13, 4, "u")
    for y in range(12, 26):
        c.put(2, y, "k")
        c.put(29, y, "k")
        c.put(5, y, "U")
        c.put(26, y, "i")
    c.hline(3, 28, 12, "U")
    c.hline(4, 27, 18, "i")
    for x in (8, 12, 16, 20, 24):
        c.vline(x, 27, 29, "r")
        c.put(x, 26, "o")
        c.put(x + 1, 28, "y")
    c.hline(2, 29, 30, "k")
    for (x, y) in ((10, 3), (11, 2), (17, 4), (18, 3), (22, 2)):
        c.put(x, y, "c")
    return c


stamp("vat", "cloth", _vat(), 2, 2,
      note="a lead dye vat steaming over a low fire, purple to the brim")


def _shell_heap():
    """Crushed murex: the heap in the corner, gray-white and purple."""
    c = Canvas(32, 32)
    c.ellipse(16, 22, 15, 9, "C")
    c.ellipse(15, 19, 11, 7, "c")
    for y in range(10, 31):
        for x in range(1, 31):
            if c.get(x, y) in "cC":
                h = (x * 7 + y * 11 + x * y) % 13
                if h == 0:
                    c.put(x, y, "p")
                elif h == 5:
                    c.put(x, y, "q")
                elif h in (8, 9):
                    c.put(x, y, "n")
    c.outline("k")
    return c


stamp("shell_heap", "cloth", _shell_heap(), 2, 2,
      note="a heap of crushed murex shells: ten thousand snails for one cloak")


def _skeins():
    """Wool hanging from the rafters in every shade from pink to near-black."""
    c = Canvas(32, 32)
    c.hline(0, 31, 1, "k")
    c.hline(0, 31, 2, "n")
    c.hline(0, 31, 3, "k")
    for i, (a, b) in enumerate((("q", "P"), ("P", "p"), ("r", "R"), ("q", "P"), ("p", "k"), ("P", "p"))):
        x = 1 + i * 5
        n = 18 + (i * 5) % 9
        for y in range(4, 4 + n):
            c.put(x, y, "k")
            c.put(x + 1, y, a)
            c.put(x + 2, y, b if y % 3 else a)
            c.put(x + 3, y, "k")
        c.hline(x, x + 3, 4 + n, "k")
    return c


stamp("skeins", "cloth", _skeins(), 2, 2,
      note="skeins of wool hanging from the rafters, pink to nearly black")


def _hank_cloth():
    c = Canvas(16, 16)
    c.paste(["...kkkkkkkk...",
             "..kcCcCcCcCk..",
             ".kCcCpPpcCcCk.",
             "kcCcCcCcCcCcCk",
             "kCcCcCcCcCcCck",
             "kkkkkkkkkkkkkk"], 1, 2)
    return c


layered("hank_stool", [("wood", lower(O.STAMPS["stool"]["img"], "wood")), ("cloth", _hank_cloth())], 1, 1,
      note="a stool with one finished hank of true purple on it, under a cloth")


def _gulf_map():
    """Lysandros's map of the gulf, scratched straight into the plaster: every
    rock and current, Malea's cape, Kythera, Kranai."""
    c = Canvas(48, 32)
    c.rect(0, 2, 47, 29, "p")
    # coast: the gulf's two arms and Kythera below
    pts = [(2, 4), (6, 9), (8, 16), (13, 20), (17, 18), (20, 12), (24, 10), (27, 15), (31, 21),
           (35, 22), (40, 17), (44, 9), (46, 4)]
    for (a, b) in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], "1")
    c.ellipse(36, 26, 4, 2, "S")
    c.outline("1", solid=lambda ch: ch == "S")
    c.put(20, 9, "R")
    for (x, y) in ((12, 24), (16, 25), (24, 22), (28, 26)):
        c.paste(["S.S", ".S."], x, y)
    c.line(26, 20, 34, 13, "s")
    c.line(34, 13, 38, 14, "s")
    return c


stamp("gulf_map", "wall", _gulf_map(), 3, 2,
      note="a map of the gulf scratched into the plaster, every rock and current marked")


def _trireme_shelf():
    c = Canvas(32, 32)
    c.hline(0, 31, 22, "k")
    c.hline(0, 31, 23, "l")
    c.hline(0, 31, 24, "m")
    c.hline(0, 31, 25, "k")
    c.put(2, 26, "k")
    c.put(29, 26, "k")
    for (x, y) in ((1, 16), (11, 15), (21, 16)):
        c.paste(["k.......k",
                 "kdmmmmmdk",
                 ".kllllk..",
                 "..kkkk..."], x, y + 2)
        c.vline(x + 4, y - 4, y + 2, "k")
        c.rect(x + 1, y - 3, x + 3, y, "c")
    return c


stamp("trireme_shelf", "wood", _trireme_shelf(), 2, 2, note="three model triremes on a shelf")


def _ram():
    c = Canvas(16, 16)
    c.paste(["..........kk....",
             "......kkkkzbk...",
             "...kkkbbbbbbyk..",
             "kkkbbbbbbbbbbyk.",
             "kzzzzzzzzzzbbyk.",
             ".kkkzzzzzzzzbk..",
             "....kkkkkkkkk..."], 0, 7)
    return c


stamp("ram", "bronze", _ram(), 1, 1, note="a bronze ship's ram, used as a doorstop")


def _bread_oven():
    """A domed bread oven built into the corner, the fire's mouth glowing."""
    c = Canvas(32, 32)
    c.ellipse(16, 18, 14, 13, "m")
    c.ellipse(13, 13, 7, 6, "l")
    c.rect(2, 18, 29, 29, "m")
    c.outline("k")
    c.ellipse(16, 23, 6, 5, "k")
    c.ellipse(16, 24, 4.5, 3.5, "f")
    c.ellipse(16, 25, 3, 2, "F")
    c.put(16, 26, "Y")
    c.hline(2, 29, 30, "k")
    c.hline(3, 28, 29, "d")
    return c


stamp("bread_oven", "clay", _bread_oven(), 2, 2, note="a bread oven built into the corner, warm")


def _toy_spear():
    c = Canvas(16, 32)
    c.line(4, 2, 11, 29, "m")
    c.line(5, 2, 12, 29, "d")
    c.paste([".k.", "kmk", "kmk"], 3, 0)
    c.put(11, 30, "k")
    c.put(12, 30, "k")
    return c


stamp("toy_spear", "wood", _toy_spear(), 1, 2, note="a child's wooden spear propped behind the door")


def _cake_table():
    cloth = Canvas(32, 16)
    cloth.paste(["......kkkkkk......",
                 "....kkcCcCcCkk....",
                 "...kcCcCcCcCcCk...",
                 "..kCcCcCcCcCcCck..",
                 ".kcCcCcCcCcCcCcCk.",
                 "kkkkkkkkkkkkkkkkkk"], 7, 2)
    cloth.hline(1, 30, 7, "k")
    return cloth


layered("cake_table", [("wood", lower(O.STAMPS["table"]["img"], "wood")),
                       ("cloth", _cake_table())], 2, 1,
        note="the table, and on it a cloth over something fig-shaped")


def _bench_nets():
    nets = Canvas(32, 16)
    for (x, w) in ((2, 13), (16, 13)):
        nets.box(x, 1, x + w, 7, "J")
        for xx in range(x + 1, x + w, 2):
            nets.vline(xx, 2, 6, "j")
    return nets


layered("bench_nets", [("wood", lower(EA.STAMPS["bench"]["img"], "wood")),
                       ("nature", _bench_nets())], 2, 1,
        note="nets mended and folded on a bench")


def _dove_niche():
    c = Canvas(16, 32)
    c.paste(["...kkkkkkkkkk...",
             "..kssssssssssk..",
             ".kssSSSSSSSSssk."], 0, 6)
    c.rect(2, 9, 13, 25, "S")
    c.vline(1, 9, 25, "k")
    c.vline(14, 9, 25, "k")
    c.hline(1, 14, 26, "k")
    c.hline(1, 14, 27, "s")
    for x in (3, 8):
        c.paste([".kk..",
                 "kwwk.",
                 ".kwwk",
                 "kwwwk",
                 "kkkk."], x, 20)
        c.put(x + 1, 21, "k")
    return c


stamp("dove_niche", "wall", _dove_niche(), 1, 2, note="a niche with two clay doves in it")


def _sandal_strings(kind):
    """Tiny votive sandals on strings from the ceiling, left by couples who came
    here to run away together."""
    c = Canvas(32, 32)
    for i in range(4):
        x = 2 + i * 8 + (kind % 2) * 2
        n = 8 + ((i + kind) * 7) % 11
        c.vline(x + 2, 0, n, "S")
        c.paste([".kk.", "k23k", "k22k", "k23k", ".kk."], x + 1, n + 1)
        if (i + kind) % 2:
            c.paste([".kk.", "k22k", "k32k", ".kk."], x + 1, n + 7)
            c.vline(x + 2, n + 6, n + 6, "S")
    return c


stamp("sandals_a", "wall", _sandal_strings(0), 2, 2, note="a hundred tiny votive sandals on strings")
stamp("sandals_b", "wall", _sandal_strings(1), 2, 2, note="votive sandals on strings, left by runaways")


# ===========================================================================
# Small extras
# ===========================================================================

FLOORS["sea"] = L.FLOORS["sea"]

# a stool you can sit on: the scene's people stand on it
stamp("stool_seat", "wood", O.STAMPS["stool"]["img"], 1, 1, walk={(0, 0)},
      note="a stool (walkable: whoever stands on it sits)")


def _cheese_on(part):
    c = _cheese_altar(part)
    c.paste(["..kkkkkk..",
             ".khhhhhhk.",
             "khhcchhhhk",
             "kmhhhhhhmk",
             ".kmmmmmmk."], 3, 1)
    return c


for _p in ("L", "M", "R"):
    stamp(f"altar_cheese_{_p}", "clay", _cheese_on(_p), 1, 1,
          note="the long altar with a round cheese on it")


def _wall_worn():
    """Where the plaster has fallen off the mudbrick: a patch of brick showing."""
    c = Canvas(16, 16)
    c.paste(["..SSSSS...",
             ".SRDRRDS..",
             "SRRDRRRDS.",
             "SDRRDRRRS.",
             ".SRRRDRS..",
             "..SSSSS..."], 3, 3)
    return c


stamp("wall_worn", "wall", _wall_worn(), 1, 1, note="plaster fallen off the brick")


def _mask_pegs():
    """Old theater masks on pegs: comic, tragic, a king's."""
    c = Canvas(32, 16)
    c.hline(0, 31, 2, "k")
    c.hline(0, 31, 3, "1")
    for i, mouth in enumerate(("up", "down", "flat")):
        x = 2 + i * 10
        c.put(x + 3, 4, "k")
        c.paste([".kkkkk.", "kwwwwwk", "kwkwkwk", "kwwwwwk", "kwwwwwk", ".kwwwk.", "..kkk.."], x, 5)
        if mouth == "up":
            c.paste(["k...k", ".kkk."], x + 1, 8)
        elif mouth == "down":
            c.paste([".kkk.", "k...k"], x + 1, 8)
        else:
            c.hline(x + 2, x + 4, 9, "k")
            c.hline(x + 1, x + 5, 4, "o")
    return c


stamp("mask_pegs", "wall", _mask_pegs(), 2, 1, note="old theater masks on pegs: comic, tragic, a king's")


def _reeds():
    c = Canvas(16, 16)
    for x in (2, 4, 6, 9, 11, 13):
        top = 2 + (x * 5) % 5
        c.vline(x, top, 14, "g")
        c.vline(x + 1, top + 2, 14, "G")
        c.put(x, top - 1, "K")
        c.put(x, max(top - 2, 0), "K")
    c.hline(1, 14, 15, "G")
    return c


stamp("reeds", "nature", _reeds(), 1, 1, note="marsh reeds growing up through the court's flags")


def _reed_mat_b():
    c = _reed_mat()
    c.hline(2, 13, 4, "J")
    c.hline(2, 13, 11, "K")
    return c


stamp("reed_mat_b", "nature", _reed_mat_b(), 1, 1, walk={(0, 0)}, note="a sleeping mat of reeds")
