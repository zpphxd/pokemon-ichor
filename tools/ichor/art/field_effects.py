"""Field effects for the Kalliste slice, redrawn to sit on the aethos tiles.

Usage:
    python3 tools/ichor/art/field_effects.py [--write] [--preview DIR]

--write    rewrites the effect PNGs and the two shared effect palettes in
           graphics/field_effects/
--preview  writes DIR/field_effects.png: every redrawn effect at 6x, each over
           the aethos tile it plays on

What is here, and why it looks the way it does:

* The two shared effect palettes keep Emerald's index ROLES (greens stay
  greens, water stays water, sand stays sand), so the effects this file leaves
  alone (ash, bubbles, hot springs, bike tracks) still draw sensibly.
  - GENERAL_1 (grass and ripples) takes aethos's meadow and puddle colors.
  - GENERAL_0 (sand, splashes, dust, the Asclepeion glow) takes aethos's sand,
    sea and limestone, plus gold.
* Tall grass and reeds are cut from the aethos metatiles themselves
  (render_map.Renderer), so the tuft that hides the player's feet matches the
  barley tile pixel for pixel. The rustle adds bent stalks, gold grain and chaff.
* Ripples, splashes and ledge dust are native drawings in the old engine
  frame slots; the footprints are reshaped into sandal soles.
* The emotes ("!", "?", "!!", "X" in may.pal; the heart in npc_1.pal) are
  pottery shards with black-figure glyphs, after the pottery UI.
* The warp arrow is terracotta with an ink outline, blinking to saffron.
* The surf mount (surf_blob.png) is a Minoan dolphin: Aegean-blue back, a
  saffron flank stripe, a cream belly, after the Knossos fresco. The game draws
  it, and the warp arrow, in the current player's palette (brendan.pal or
  may.pal), so both use only slots the two palettes share: blue 5-6, straw
  10-11, terracotta 12-13, cream 14, ink 15. Riders: surf_poses.py.
* The Pokémon Center "monitor" is the Asclepeion's rod-of-Asclepius relief
  lighting up gold during the heal, drawn to the relief's pixels in
  design/phase1/rooms/akti_asclepeion.bin. The healed balls float in the spring.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, upscale  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "tools/ichor"))
import render_map as R  # noqa: E402

PICS = os.path.join(ROOT, "graphics/field_effects/pics")
PALS = os.path.join(ROOT, "graphics/field_effects/palettes")
OBJ_PALS = os.path.join(ROOT, "graphics/object_events/palettes")


# --------------------------------------------------------------------------
# Palettes
# --------------------------------------------------------------------------

class RawPal:
    """16 colors as given (no multiple-of-8 check: npc_1.pal is Emerald's)."""

    def __init__(self, colors):
        assert len(colors) == 16
        self.colors = [tuple(c) for c in colors]

    def flat(self):
        return [v for c in self.colors for v in c]

    def write_jasc(self, path):
        with open(path, "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n16\n")
            for c in self.colors:
                f.write("%d %d %d\n" % c)


def read_jasc(path):
    vals = open(path).read().split()[3:]
    return RawPal([tuple(int(v) for v in vals[i * 3:i * 3 + 3]) for i in range(16)])


# GENERAL_1: grass, reeds and ripples. Index roles follow Emerald.
GENERAL_1 = RawPal([
    (112, 192, 160),   # 0 transparent
    (160, 176, 80),    # 1 barley light       (Emerald: light green)
    (112, 128, 64),    # 2 barley mid
    (72, 88, 48),      # 3 barley shade
    (40, 56, 32),      # 4 barley dark
    (184, 184, 104),   # 5 meadow grass
    (88, 176, 200),    # 6 puddle water        (Emerald: ripple blues 6-9)
    (112, 168, 224),   # 7 sea-sky water
    (176, 216, 240),   # 8 water light
    (248, 240, 216),   # 9 foam
    (144, 128, 96),    # 10 ash, exact BGR555
    (176, 168, 144),   # 11 ash light, exact BGR555
    (240, 192, 64),    # 12 barley grain gold  (Emerald: teal greens 12-15)
    (200, 144, 40),    # 13 grain ochre
    (144, 152, 72),    # 14 meadow shade
    (208, 200, 128),   # 15 meadow light
])
G1 = {"a": 4, "c": 3, "e": 2, "d": 1, "b": 12, "o": 13, "g": 5, "h": 14, "G": 15,
      "w": 6, "s": 7, "l": 8, "F": 9}

# GENERAL_0: sand, splashes, dust, tracks and the Asclepeion glow.
GENERAL_0 = RawPal([
    (112, 192, 160),   # 0 transparent
    (248, 240, 216),   # 1 limestone dust light  (Emerald: impact dust 1-3)
    (232, 216, 176),   # 2 limestone dust
    (208, 184, 136),   # 3 limestone dust shade
    (248, 248, 240),   # 4 foam white            (Emerald: white)
    (176, 216, 240),   # 5 water light           (Emerald: splash blues 5-8)
    (112, 168, 224),   # 6 water
    (80, 136, 200),    # 7 sea
    (48, 104, 176),    # 8 deep sea
    (240, 192, 64),    # 9 gold glow             (Emerald: pink, unused here)
    (32, 24, 24),      # 10 ink
    (232, 208, 144),   # 11 sand                 (Emerald: sand 11-14)
    (216, 192, 128),   # 12 sand print rim
    (200, 168, 104),   # 13 sand print
    (176, 144, 96),    # 14 sand print deep
    (200, 144, 40),    # 15 ochre glow shade     (Emerald: black, unused here)
])
G0 = {"D": 1, "m": 2, "M": 3, "W": 4, "l": 5, "s": 6, "B": 7, "n": 8, "O": 9, "k": 10,
      "y": 11, "p": 12, "q": 13, "r": 14, "o": 15}

# may.pal (Ianthe's; it also colors the surf mount, the arrow and the emotes).
MAY = read_jasc(os.path.join(OBJ_PALS, "may.pal"))
MY = {"S": 1, "s": 2, "z": 3, "b": 4, "B": 5, "n": 6, "h": 7, "H": 8, "l": 9, "O": 10,
      "o": 11, "U": 12, "u": 13, "L": 14, "k": 15}

# npc_1.pal (Emerald's), which colors the heart emote.
NPC1 = read_jasc(os.path.join(OBJ_PALS, "npc_1.pal"))
N1 = {"P": 1, "U": 3, "u": 4, "r": 6, "R": 7, "L": 14, "k": 15}

BALL = read_jasc(os.path.join(PALS, "pokeball_glow.pal"))
BL = {"W": 1, "g": 2, "G": 3, "k": 4, "r": 5, "R": 6, "p": 7, "w": 8, "c": 12, "d": 13, "e": 15}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def ascii_frame(rows, legend, w=None, h=None):
    h = h or len(rows)
    w = w or len(rows[0])
    a = np.zeros((h, w), np.uint8)
    for y, row in enumerate(rows):
        if len(row) != w:
            raise ValueError(f"row {y} is {len(row)} wide, want {w}: {row!r}")
        for x, ch in enumerate(row):
            if ch in "._":
                continue
            if ch not in legend:
                raise ValueError(f"unknown char {ch!r} in {row!r}")
            a[y, x] = legend[ch]
    return a


def strip(frames):
    return np.hstack(frames)


def save(arr, pal, name):
    im = Image.fromarray(arr.astype(np.uint8), "P")
    im.putpalette(pal.flat())
    im.info["transparency"] = 0
    path = os.path.join(PICS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, bits=4, transparency=0)


_RENDERER = None


def aethos():
    global _RENDERER
    if _RENDERER is None:
        R.read_fieldmap_constants()
        syms = R.scan_tileset_symbols()
        _RENDERER = R.Renderer(R.Tileset(R.resolve_tileset("aethos", syms)),
                               R.Tileset(R.resolve_tileset("kalliste", syms)))
    return _RENDERER


def metatile_indices(mid, pal):
    """An aethos metatile as indices into `pal` (every color must be in it)."""
    rgb, _ = aethos().metatile(mid)
    lut = {c: i for i, c in enumerate(pal.colors) if i}
    out = np.zeros((16, 16), np.uint8)
    for y in range(16):
        for x in range(16):
            c = tuple(int(v) for v in rgb[y, x])
            if c not in lut:
                raise ValueError(f"metatile {mid:#x} color {c} is not in the effect palette")
            out[y, x] = lut[c]
    return out


def ripple_frames():
    frames = []
    for phase, (rx, ry) in enumerate(((2, 1), (4, 2), (5, 3), (6, 3), (7, 4))):
        im = Image.new("P", (16, 16), 0)
        d = ImageDraw.Draw(im)
        box = (8 - rx, 8 - ry, 8 + rx, 8 + ry)
        d.arc(box, 185, 345, fill=8)
        d.arc(box, 5, 165, fill=6 if phase == 4 else 7)
        if phase < 3:
            d.line((6, 8, 9, 8), fill=9)
        frames.append(np.array(im))
    return frames


def splash_frames(big=False, landing=False):
    """Hand-drawn fans of water, in the engine's existing frame slots."""
    count = 4 if big else 3 if landing else 2
    size = 16 if big else 8
    frames = []
    for phase in range(count):
        im = Image.new("P", (16, size), 0)
        d = ImageDraw.Draw(im)
        cx, floor = 8, size - 2
        rise = (5, 7, 4, 2)[phase] if big else (3, 4, 2)[phase]
        spread = phase + (3 if big else 1)
        d.polygon([(cx - spread - 1, floor), (cx - spread - 2, floor - rise),
                   (cx - 2, floor - 2), (cx - 1, floor - rise - 1),
                   (cx + 1, floor - 2), (cx + spread + 2, floor - rise + 1),
                   (cx + spread + 1, floor)], fill=7)
        d.arc((cx - spread - 1, floor - 2, cx + spread + 1, floor + 1), 0, 180, fill=8)
        d.line((cx - spread - 2, floor - rise, cx - spread, floor - 1), fill=5)
        d.line((cx + spread, floor - 1, cx + spread + 2, floor - rise + 1), fill=6)
        d.line((cx - 1, floor - 1, cx - 1, floor - rise - 1), fill=4)
        d.point((cx + spread + 2, floor - rise + 1), fill=5)
        d.point((cx - spread - 2, floor - rise), fill=4)
        if phase < count - 1:
            d.point((cx + spread + 1, floor - rise - 2), fill=5)
            d.point((cx - spread - 1, floor - rise - 1), fill=4)
        frames.append(np.array(im))
    return frames


def dust_frames():
    frames = []
    for phase in range(3):
        im = Image.new("P", (16, 8), 0)
        d = ImageDraw.Draw(im)
        for x, y, w in ((3 - phase, 5 - phase, 3), (7, 4 + phase, 4),
                        (11 + phase, 5 - phase, 3)):
            d.ellipse((x, y, x + w, y + 2), fill=3)
            d.line((x + 1, y, x + w - 1, y), fill=1)
            d.point((x + 1, y + 1), fill=2)
        frames.append(np.array(im))
    return frames


def overlay(base, rows, legend):
    out = base.copy()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "_":
                continue
            out[y, x] = 0 if ch == "." else legend[ch]
    return out


# --------------------------------------------------------------------------
# Tall grass: aethos barley (metatile 0x00D)
# --------------------------------------------------------------------------

TALL_GRASS = 0x00D
REEDS = 0x015


def tall_grass_frames():
    tile = metatile_indices(TALL_GRASS, GENERAL_1)
    shade = G1["c"]
    tuft = np.zeros((16, 16), np.uint8)
    tuft[10:16] = tile[10:16]
    # the top edge: keep only the blade strokes of row 9, so the tips stand up
    tuft[9] = np.where(tile[9] != shade, tile[9], 0)
    # frame 1: the stalks whip apart and lean out, grain flying off the heads
    f1 = overlay(tuft, [
        "................",
        "................",
        "...b........b...",
        "..bo.......ob...",
        "..ad.b..b..da...",
        "...ad.....da....",
        "...ead...dae....",
        "....eda.ade.....",
        "...a.ed.de.a....",
        "__aa_______aa___",
    ], G1)
    # frame 2: grain and chaff thrown high
    f2 = overlay(tuft, [
        "................",
        "..b.........o...",
        ".......d........",
        ".o..d......b....",
        "..........d..b..",
        "....b..o........",
        ".d.........d....",
        "......d..b......",
        "..b..........o..",
        "________________",
    ], G1)
    # frame 3: falling back
    f3 = overlay(tuft, [
        "................",
        "................",
        "................",
        "................",
        "..o..........b..",
        ".....d..........",
        "...........d....",
        "..b...o.........",
        ".......d.....b..",
        "________________",
    ], G1)
    # frame 4: the last grain settling into the tuft
    f4 = overlay(tuft, [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "....b...........",
        "...........o....",
        "......d.........",
        "________________",
    ], G1)
    return [tuft, f1, f2, f3, f4]


def jump_tall_grass_frames():
    """Landing in barley: stalks and grain burst out from under the feet (16x8)."""
    rows = [
        [
            "................",
            "................",
            "...b........b...",
            "...db......bd...",
            ".b..d......d..b.",
            ".db..........bd.",
            "..d..b....b..d..",
            "......d..d......",
        ],
        [
            "..b..........b..",
            "...b........b...",
            "b..d........d..b",
            ".b............b.",
            ".d..b......b..d.",
            ".....d....d.....",
            "................",
            "................",
        ],
        [
            "................",
            "................",
            "..bd........db..",
            "................",
            "bo............ob",
            "................",
            "....bd....db....",
            "................",
        ],
        [
            "................",
            "................",
            "................",
            "..oo........oo..",
            "................",
            "oo............oo",
            "................",
            "....oo....oo....",
        ],
    ]
    return [ascii_frame(r, G1) for r in rows]


# --------------------------------------------------------------------------
# Reeds: aethos long grass (metatile 0x015)
# --------------------------------------------------------------------------

def _part(tile, shifts):
    """The reed tile with its left half pushed left and right half pushed right
    by shifts[y] pixels, opening a gap down the middle."""
    out = np.zeros_like(tile)
    for y in range(16):
        s = shifts[y]
        if s >= 0:
            out[y, :8 - s] = tile[y, s:8]
            out[y, 8 + s:] = tile[y, 8:16 - s]
        else:
            s = -s
            out[y, s:8] = tile[y, :8 - s]
            out[y, 8:16 - s] = tile[y, 8 + s:]
    return out


def long_grass_frames():
    tile = metatile_indices(REEDS, GENERAL_1)
    rest = tile.copy()
    f1 = _part(tile, [2] * 4 + [2] * 4 + [1] * 4 + [0] * 4)
    f2 = _part(tile, [3] * 4 + [2] * 4 + [1] * 4 + [1] * 4)
    f3 = _part(tile, [-1] * 6 + [0] * 10)
    return [rest, f1, f2, f3]


def jump_long_grass_frames():
    tile = metatile_indices(REEDS, GENERAL_1)
    frames = [
        _part(tile, [4] * 6 + [3] * 4 + [2] * 3 + [1] * 3),
        _part(tile, [3] * 6 + [3] * 4 + [2] * 3 + [1] * 3),
        _part(tile, [2] * 8 + [1] * 8),
        _part(tile, [1] * 8 + [0] * 8),
        _part(tile, [-1] * 6 + [0] * 10),
        tile.copy(),
        tile.copy(),
    ]
    # a little chaff on the first frames
    frames[0] = overlay(frames[0], ["..d..........d..", ".b............b."], G1)
    frames[1] = overlay(frames[1], [".d............d."], G1)
    return frames


# --------------------------------------------------------------------------
# Native contact effects and sandal footprints
# --------------------------------------------------------------------------

def sandal_frames():
    """Sandal soles pressed into the sand: smooth ovals with a strap dent,
    instead of Hoenn's toed prints. Frame 0 north/south, frame 1 east/west."""
    rows = [
        [
            "................",
            "................",
            ".........pqp....",
            ".........qrq....",
            ".........qrq....",
            ".........prp....",
            ".........qrq....",
            ".........pqp....",
            "................",
            "................",
            "....pqp.........",
            "....qrq.........",
            "....qrq.........",
            "....prp.........",
            "....qrq.........",
            "....pqp.........",
        ],
        [
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "..........pqqqqp",
            "..........qrrprq",
            "................",
            "..pqqqqp........",
            "..qrprrq........",
        ],
    ]
    return [ascii_frame(r, G0) for r in rows]


# --------------------------------------------------------------------------
# Emotes: pottery shards with black-figure glyphs (16x16)
# --------------------------------------------------------------------------

_SHARD = [
    "................",
    "...kkkkk..kkk...",
    "..kLLUUUkkUUuk..",
    ".kLUUUUUUUUUUuk.",
    ".kLU########Uuk.",
    ".kUU########Uuk.",
    "..kU########Uuk.",
    "..kU########Uk..",
    ".kUU########Uk..",
    ".kUU########Uuk.",
    ".kUU########Uuk.",
    ".kuU########uuk.",
    "..kuuuuuuuuuuk..",
    "...kkkkkuukkk...",
    "........kuk.....",
    ".........k......",
]

GLYPHS = {
    "exclamation": [
        "...kkk..",
        "...kkk..",
        "...kkk..",
        "....k...",
        "....k...",
        "........",
        "...kk...",
        "...kk...",
    ],
    "question": [
        "..kkkk..",
        ".kk..kk.",
        ".....kk.",
        "....kk..",
        "...kk...",
        "........",
        "...kk...",
        "...kk...",
    ],
    "double_exclamation": [
        ".kk..kk.",
        ".kk..kk.",
        ".kk..kk.",
        "..k...k.",
        "..k...k.",
        "........",
        ".kk..kk.",
        ".kk..kk.",
    ],
    "x": [
        "........",
        ".kk..kk.",
        "..kkkk..",
        "...kk...",
        "..kkkk..",
        ".kk..kk.",
        "........",
        "........",
    ],
    "heart": [
        "........",
        ".kk..kk.",
        "kkkkkkkk",
        "kkkkkkkk",
        ".kkkkkk.",
        "..kkkk..",
        "...kk...",
        "........",
    ],
}


def shard(glyph, legend):
    rows = []
    g = GLYPHS[glyph]
    for y, row in enumerate(_SHARD):
        if "#" in row:
            i = row.index("#")
            line = g[y - 4]
            row = row[:i] + line.replace(".", "U") + row[i + 8:]
        rows.append(row)
    return ascii_frame(rows, legend)


# --------------------------------------------------------------------------
# Warp arrow: terracotta, ink outline; blinks to saffron (may.pal)
# --------------------------------------------------------------------------

def arrow_frames():
    van = load_vanilla("arrow.png")
    out = van.copy()
    # Emerald draws the arrow fill in index 14 (frames 0-3) and 10 (frames 4-7)
    # with an index-15 outline. Fill: terracotta, shaded on the lower right,
    # with a cream glint on the upper left; blink frames: saffron.
    for f in range(8):
        fr = out[:, f * 16:(f + 1) * 16]
        fill = fr != 0
        fill &= fr != MY["k"]
        ys, xs = np.nonzero(fill)
        if len(ys) == 0:
            continue
        cy, cx = ys.mean(), xs.mean()
        light, dark = (MY["U"], MY["u"]) if f < 4 else (MY["O"], MY["o"])
        for y, x in zip(ys, xs):
            fr[y, x] = dark if (y - cy) + (x - cx) > 2 else light
        # a glint on the first fill pixel from the top left
        y0, x0 = min(zip(ys, xs), key=lambda p: p[0] + p[1])
        fr[y0, x0] = MY["L"]
    return out


# --------------------------------------------------------------------------
# The surf mount: a Minoan dolphin (32x32, may.pal)
# --------------------------------------------------------------------------

DOLPHIN = {
    # facing south, toward the viewer: the rider sits on its back; its head
    # comes at us between the rider's shins, flippers out, foam at the sides
    "south": [
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "............kkkkkkkk............",
        "..........kknBBBBBnnkk..........",
        ".........knBBBBBBBBBnnnk........",
        "........knBBBBBBBBBBnnnnk.......",
        "........knBBBBBBBBBnnnnnk.......",
        "..kkk..knnBBBBBBBnnnnnnnk..kkk..",
        ".kBBnk.knnnBBBBnnnnnnnnnk.knnnk.",
        ".knnnnkknnnnnnnnnnnnnnnnkknnnnk.",
        "..kkkkkknnnnnBBBBBnnnnnnkkkkkk..",
        "LL.....knnnnBBBBBBBnnnnnk.....LL",
        ".LLL....knnnBBBBBBBnnnnk....LLL.",
        "...LLL...knkBnnnnnBknnk...LLL...",
        ".....LLL..knnnnnnnnnnk..LLL.....",
        ".......LLL.kLLLLLLLLk.LLL.......",
        ".........LLLkLllllLkLLL.........",
        "...........LLLkkkkLLL...........",
        "..............LLLL..............",
    ],
    # facing north, away: its back under the rider, the tail flukes toward us
    "north": [
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "............kkkkkkkk............",
        "..........kknBBBBBnnkk..........",
        ".........knBBBBBBBBBnnnk........",
        "........knBBBBBBBBBBnnnnk.......",
        "........knBBBBBBBBBnnnnnk.......",
        "..kkk..knnBBBBBBBnnnnnnnk..kkk..",
        ".kBBnkkknnnBBBBnnnnnnnnnkkknnnk.",
        "..kkkk.knnnnnnnnnnnnnnnnk.kkkk..",
        "LL......knnnnnnnnnnnnnnk......LL",
        ".LLL.....kknnnnnnnnnnkk.....LLL.",
        "...LLL.....knnnBnnnnk.....LLL...",
        ".....kkkk..knnBBnnnnk..kkkk.....",
        "....knBBBkkknnnnnnnnkkkBBBnk....",
        "....kknnnnnnnnkknnnnnnnnnkk.....",
        "......kkkkkkkk..kkkkkkkkk.......",
        ".......LLLLLLLLLLLLLLLLLL.......",
        "................................",
    ],
    # facing west: in profile, rostrum to the left, the dorsal fin behind the
    # rider, the saffron stripe down the flank, the tail fluke raised on the right
    "west": [
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "................................",
        "........................kk......",
        ".......................knnk.....",
        "......................knBnk.....",
        ".....................knBBnk.....",
        "...................kknBBBnk..kk.",
        ".........kkkkkkkkkknBBBBBnk.knBk",
        ".......kknBBBBBBBBBBBBBBBnkknnk.",
        ".....kknBBBBBBBBBBBBBBBBBBBnnk..",
        "...kknBkBBBBBBBBBBBBBBBnnnnnk...",
        ".kknBBBBnOOOOOOOOOOOOOOnnnnk....",
        "knnnnBnOOLLLLLLLLLLLLLLOOnk.....",
        "kLLLLLLLLLLLLLLLLLLLLLLLLk......",
        ".kkLLLLLLLlllllllllLLLkk........",
        "LL.kkkkkkkkkkkkkkkkkkkk.....LL..",
        ".LLLL......................LLLL.",
        "...LLLLLL...............LLLLL...",
        "......LLLLLLLLLLLLLLLLLLLL......",
        "...........LLLLLLLLLL...........",
        "................................",
        "................................",
        "................................",
    ],
}


def dolphin_frames():
    return [ascii_frame(DOLPHIN[d], MY) for d in ("south", "north", "west")]


# --------------------------------------------------------------------------
# The Asclepeion heal: the rod-of-Asclepius relief lights up (24x16, GENERAL_0)
# --------------------------------------------------------------------------
# The sprite covers map pixels x 112-135, y 8-23 of the Asclepeion room
# (ROOMS_civic.md): the relief's niche is columns 4-12. The serpent and rod
# below are traced from the relief's own pixels, so the glow lands on them.

RELIEF_GLOW = {
    "bright": [
        "........................",
        ".......WW...............",
        "......DOODD.O...........",
        ".......OOWWW............",
        ".....D.OWD..............",
        "......DOW...............",
        "......WOO...............",
        ".....WWOO...O...........",
        "......WOOD..............",
        ".......OWD..............",
        "....D..OOW..............",
        ".......OOWW.............",
        ".......OOW.D............",
        ".......OW...............",
        "......WOO...............",
        ".....WWOO...............",
    ],
    "dim": [
        "........................",
        ".......OO...............",
        ".......oOD..............",
        ".......ooOOO............",
        ".......oO...............",
        "......Doo...............",
        "......Ooo...............",
        ".....OOoo...............",
        "......Ooo...............",
        ".......oO...............",
        ".......ooO..............",
        ".......ooOO.............",
        ".......ooO..............",
        ".......oO...............",
        "......Ooo...............",
        ".....OOoo...............",
    ],
}


def monitor_frames():
    return [ascii_frame(RELIEF_GLOW[k], G0) for k in ("bright", "dim")]


def ball_frame():
    """A healed party member's ball floating in the spring, a ripple ring at its
    waterline. The ball's own slots (2, 3, 5, 6, 8) are the ones the heal
    flashes; the ring uses the palette's untouched blues (12, 13)."""
    return ascii_frame([
        "........",
        "...rr...",
        "..wpRr..",
        ".GpRRRr.",
        "cdGggGdc",
        ".cdgddc.",
        "..cccc..",
        "........",
    ], BL)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def build():
    """name -> (array, palette)"""
    out = {
        "tall_grass.png": (strip(tall_grass_frames()), GENERAL_1),
        "jump_tall_grass.png": (strip(jump_tall_grass_frames()), GENERAL_1),
        "long_grass.png": (strip(long_grass_frames()), GENERAL_1),
        "jump_long_grass.png": (strip(jump_long_grass_frames()), GENERAL_1),
        "sand_footprints.png": (strip(sandal_frames()), GENERAL_0),
        "emotion_exclamation.png": (shard("exclamation", MY), MAY),
        "emotion_question.png": (shard("question", MY), MAY),
        "emotion_double_exclamation.png": (shard("double_exclamation", MY), MAY),
        "emote_x.png": (shard("x", MY), MAY),
        "emotion_heart.png": (shard("heart", N1), NPC1),
        "arrow.png": (arrow_frames(), MAY),
        "surf_blob.png": (strip(dolphin_frames()), MAY),
        "pokecenter_monitor/0.png": (monitor_frames()[0], GENERAL_0),
        "pokecenter_monitor/1.png": (monitor_frames()[1], GENERAL_0),
        "pokeball_glow.png": (ball_frame(), BALL),
    }
    out.update({
        "ripple.png": (strip(ripple_frames()), GENERAL_1),
        "splash.png": (strip(splash_frames()), GENERAL_0),
        "jump_small_splash.png": (strip(splash_frames(landing=True)), GENERAL_0),
        "jump_big_splash.png": (strip(splash_frames(big=True)), GENERAL_0),
        "ground_impact_dust.png": (strip(dust_frames()), GENERAL_0),
    })
    return out


def to_rgba(arr, pal):
    rgba = np.zeros(arr.shape + (4,), np.uint8)
    for i, c in enumerate(pal.colors):
        m = arr == i
        rgba[m, :3] = c
        rgba[m, 3] = 0 if i == 0 else 255
    return Image.fromarray(rgba, "RGBA")


PREVIEW_GROUND = {
    "tall_grass.png": TALL_GRASS, "jump_tall_grass.png": 0x001, "long_grass.png": REEDS,
    "jump_long_grass.png": REEDS, "sand_footprints.png": 0x124, "ripple.png": 0x0D1,
    "splash.png": 0x0D1, "jump_small_splash.png": 0x0D1, "jump_big_splash.png": 0x170,
    "ground_impact_dust.png": 0x001, "surf_blob.png": 0x170, "arrow.png": 0x024,
}


def preview(effects, k=6):
    rows = []
    for name, (arr, pal) in effects.items():
        h = arr.shape[0]
        fw = {"surf_blob.png": 32, "pokecenter_monitor/0.png": 24, "pokecenter_monitor/1.png": 24,
              "pokeball_glow.png": 8}.get(name, 16)
        im = to_rgba(arr, pal)
        nf = arr.shape[1] // fw
        row = Image.new("RGBA", (nf * (fw + 2), h), (232, 224, 200, 255))
        for f in range(nf):
            bg = Image.new("RGBA", (fw, h), (184, 184, 104, 255))
            mid = PREVIEW_GROUND.get(name)
            if mid is not None:
                t = Image.fromarray(aethos().metatile(mid)[0])
                for ty in range(0, h, 16):
                    for tx in range(0, fw, 16):
                        bg.paste(t, (tx, ty))
            bg.alpha_composite(im.crop((f * fw, 0, (f + 1) * fw, h)))
            row.alpha_composite(bg, (f * (fw + 2), 0))
        rows.append((name, row))
    lw = 150
    W = max(r.width for _, r in rows) * k + lw
    H = sum((r.height + 4) * k for _, r in rows)
    out = Image.new("RGBA", (W, H), (232, 224, 200, 255))
    d = ImageDraw.Draw(out)
    y = 0
    for name, row in rows:
        d.text((4, y + 8), name, fill=(32, 24, 24, 255))
        out.alpha_composite(upscale(row, k), (lw, y))
        y += (row.height + 4) * k
    return out


def main():
    args = sys.argv[1:]
    effects = build()
    if "--write" in args:
        for name, (arr, pal) in effects.items():
            save(arr, pal, name)
        GENERAL_0.write_jasc(os.path.join(PALS, "general_0.pal"))
        GENERAL_1.write_jasc(os.path.join(PALS, "general_1.pal"))
    if "--preview" in args:
        d = args[args.index("--preview") + 1]
        os.makedirs(d, exist_ok=True)
        preview(effects).save(os.path.join(d, "field_effects.png"))


if __name__ == "__main__":
    main()
