#!/usr/bin/env python3
"""The follower's emotion bubbles and the balls it rides in, as pottery.

Usage:
    /usr/bin/python3 tools/ichor/art/follower_icons.py [--write] [--preview DIR]

--write    rewrites graphics/misc/emotes.png and emotes.pal, and the 28 follower
           ball sheets graphics/object_events/pics/misc/ball_*.png
--preview  writes DIR/follower_icons.png: every emote frame and ball frame at 6x

Emotes (graphics/misc/emotes.png, src/trainer_see.c sSpriteImageTable_Emotes).
  Talking to the follower pops one of eleven emotions over it, each a pair of
  16x16 frames shown A, B, A. They were HGSS's white speech bubbles. Now they
  are the field's own pottery shards (field_effects.py: the trainer "!", "?")
  in the same terracotta, cream chip and broken top, with the face or glyph in
  black-figure ink. The poisoned shard is fired olive, like sickly glaze.
  emotes.pal is the emotes' own palette (OBJ_EVENT_PAL_TAG_EMOTES).

Follower balls (graphics/object_events/pics/misc/ball_*.png).
  The follower goes into its ball at doors and comes out of it after. Each
  sheet is five 16x32 frames (closed, closed and rocking, cracking open, open
  with light rising, a column of light); the expansion's sheets also carry two
  unused frames, kept blank here. Every ball is the party menu's black-figure
  ball (ui_menus_party.py): a glazed cap with a lit edge, a clay band, a gold
  button and a buff lower half, with an ichor-gold light. The other 27 balls
  keep their colors as painted caps and marks, so a Great Ball still reads blue
  with red bands.
  - ball_poke.png is drawn in the townsfolk palette (ichor_folk.pal), and
    gObjectEventGraphicsInfo_PokeBall now loads that palette instead of
    Emerald's npc_3 (src/data/object_events/object_event_graphics_info.h). On
    maps with folk walkers it costs no extra slot, as the item jar doesn't.
  - Every other sheet carries its own 16-color palette, as the expansion's do.
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT  # noqa: E402

MISC = os.path.join(ROOT, "graphics/misc")
BALL_DIR = os.path.join(ROOT, "graphics/object_events/pics/misc")
FOLK_PAL = os.path.join(ROOT, "graphics/object_events/palettes/ichor_folk.pal")

TRANSPARENT = (115, 197, 164)
INK = (32, 24, 24)


def read_jasc(path):
    v = open(path).read().split()
    n = int(v[2])
    nums = list(map(int, v[3:3 + 3 * n]))
    return [tuple(nums[i:i + 3]) for i in range(0, 3 * n, 3)]


def write_jasc(path, colors):
    lines = ["JASC-PAL", "0100", str(len(colors))] + ["%d %d %d" % tuple(c) for c in colors]
    with open(path, "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def save_png(path, a, pal):
    flat = [v for c in pal for v in c]
    im = Image.fromarray(a.astype(np.uint8), "P")
    im.putpalette(flat)
    im.save(path, bits=4, transparency=0)


def grid(rows, key):
    a = np.zeros((len(rows), len(rows[0])), np.uint8)
    for y, row in enumerate(rows):
        assert len(row) == len(rows[0]), (row, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                a[y, x] = key[ch]
    return a


# --------------------------------------------------------------------------
# Emotes: pottery shards with black-figure faces (16x16 frames)
# --------------------------------------------------------------------------

# emotes.pal. U/u/L are the shard's terracotta, shade and cream chip, as in
# may.pal's 12-14; P/p/l the poisoned shard's olive glaze.
EMOTE_PAL = [
    TRANSPARENT,
    INK,                 # 1 k  ink
    (224, 136, 88),      # 2 U  terracotta
    (184, 88, 48),       # 3 u  terracotta shade
    (248, 240, 208),     # 4 L  cream chip, a white highlight
    (168, 40, 32),       # 5 r  added red (mouths, hearts, the anger vein)
    (176, 216, 240),     # 6 w  tear water
    (144, 160, 72),      # 7 P  olive glaze
    (96, 112, 48),       # 8 p  olive shade
    (200, 208, 152),     # 9 l  olive chip
    (240, 192, 64),      # 10 g gold (the note's shine)
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
]
EK = {"k": 1, "U": 2, "u": 3, "L": 4, "r": 5, "w": 6, "P": 7, "p": 8, "l": 9, "g": 10}

# The field's shard (field_effects.py _SHARD): '#' is the 8x8 glyph field.
SHARD = [
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

# Each emotion: two 8x8 glyphs, A and B. '.' is the shard's own clay.
FACES = {
    "happy": ([
        "........",
        ".k....k.",
        "k.k..k.k",
        "........",
        "k......k",
        ".k....k.",
        "..kkkk..",
        "........",
    ], [
        "........",
        ".k....k.",
        "k.k..k.k",
        "........",
        ".kkkkkk.",
        ".krrrrk.",
        "..kkkk..",
        "........",
    ]),
    "neutral": ([
        "........",
        "..k..k..",
        "..k..k..",
        "........",
        "........",
        "..kkkk..",
        "........",
        "........",
    ], [
        "........",
        "..k..k..",
        "..k..k..",
        "........",
        ".k....k.",
        "..kkkk..",
        "........",
        "........",
    ]),
    "sad": ([
        "........",
        ".kk..kk.",
        "........",
        "..k..k..",
        "..k..k..",
        "........",
        "..kkkk..",
        ".k....k.",
    ], [
        "........",
        ".kk..kk.",
        "........",
        "..k..k..",
        "..k..k..",
        "..w.....",
        "..kkkk..",
        ".k....k.",
    ]),
    "upset": ([
        ".k....k.",
        "..k..k..",
        "........",
        "..k..k..",
        "..k..k..",
        "........",
        "..kkkk..",
        ".k....k.",
    ], [
        ".k....kw",
        "..k..k.w",
        "........",
        "..k..k..",
        "..k..k..",
        "........",
        ".kkkkkk.",
        "........",
    ]),
    "angry": ([
        "k......k",
        ".kk..kk.",
        "...kk...",
        "..k..k..",
        "........",
        "..kkkk..",
        ".k....k.",
        "........",
    ], [
        "k.....rr",
        ".kk..kr.",
        "...kk...",
        "..k..k..",
        "........",
        ".kkkkkk.",
        ".krrrrk.",
        "........",
    ]),
    "pensive": ([
        "........",
        "........",
        "........",
        "........",
        "kk..kk..",
        "kk..kk..",
        "........",
        "........",
    ], [
        "........",
        "........",
        "........",
        "........",
        "kk.kk.kk",
        "kk.kk.kk",
        "........",
        "........",
    ]),
    "love": ([
        "........",
        "........",
        "..k..k..",
        ".kkkkkk.",
        ".kkkkkk.",
        "..kkkk..",
        "...kk...",
        "........",
    ], [
        "........",
        ".kk..kk.",
        "krrkkrrk",
        "krrrrrrk",
        ".krrrrk.",
        "..krrk..",
        "...kk...",
        "........",
    ]),
    "surprise": ([
        "...kkk..",
        "...kkk..",
        "...kkk..",
        "....k...",
        "....k...",
        "........",
        "...kk...",
        "...kk...",
    ], [
        "..kkkk..",
        "..kkkk..",
        "..kkkk..",
        "...kk...",
        "...kk...",
        "........",
        "...kk...",
        "...kk...",
    ]),
    "curious": ([
        "..kkkk..",
        ".kk..kk.",
        ".....kk.",
        "....kk..",
        "...kk...",
        "........",
        "...kk...",
        "...kk...",
    ], [
        "...kkkk.",
        "..kk..kk",
        "......kk",
        ".....kk.",
        "....kk..",
        "........",
        "....kk..",
        "....kk..",
    ]),
    "music": ([
        "....kk..",
        "....kkk.",
        "....k.kk",
        "....k...",
        "....k...",
        ".kkkk...",
        "kgkkk...",
        ".kkk....",
    ], [
        "...kk...",
        "...kkk..",
        "...k.kk.",
        "...k....",
        ".kkk....",
        "kgkk....",
        ".kk.....",
        "........",
    ]),
    "poisoned": ([
        "........",
        "....kk..",
        "...k..k.",
        "...k..k.",
        "....kk..",
        ".kk.....",
        "k..k....",
        ".kk.....",
    ], [
        "...kk...",
        "..k..k..",
        "..k..k..",
        "...kk...",
        "......k.",
        ".....k.k",
        ".kk...k.",
        "k..k....",
    ]),
}
ORDER = ["happy", "neutral", "sad", "upset", "angry", "pensive", "love",
         "surprise", "curious", "music", "poisoned"]


def shard(glyph, olive=False):
    rows = []
    for y, row in enumerate(SHARD):
        if "#" in row:
            i = row.index("#")
            row = row[:i] + glyph[y - 4].replace(".", "U") + row[i + 8:]
        if olive:
            row = row.replace("U", "P").replace("u", "p").replace("L", "l")
        rows.append(row)
    return grid(rows, EK)


def emote_frames():
    frames = []
    for name in ORDER:
        a, b = FACES[name]
        frames += [shard(a, name == "poisoned"), shard(b, name == "poisoned")]
    frames.append(shard(FACES["surprise"][0]))   # frame 22, Emerald's spare "!"
    return frames


# --------------------------------------------------------------------------
# Follower balls (16x32 frames)
# --------------------------------------------------------------------------

# The party menu's small black-figure ball (ui_menus_party.py), on a 16x32
# frame: C cap, H the cap's lit edge, M a mark painted on the cap, k ink,
# B the clay band, b its shade, G/g/Y the gold button, W/w/v the lower half.
BALL_CLOSED = [
    ".....kkkkkk.....",
    "...kkCCCCCCkk...",
    "..kCHCCMMCCCCk..",
    "..kCHCCMMkkkCk..",
    ".kkkkkkkGgGkkkk.",
    ".kBBBBBkGYGkBbk.",
    "..kWWWWWkGkWWk..",
    "..kWWWWWWWWWwk..",
    "...kWwwwwwwwvk..",
    "....kkvvvvkk....",
    "......kkkk......",
]
# Rocking: the light has moved round the cap, the seam tilts a pixel.
BALL_ROCK = [
    ".....kkkkkk.....",
    "...kkCCCCCCkk...",
    "..kCCCCMMCCHCk..",
    "..kkkCCMMCCCHk..",
    ".kkkkkkGgGkkkkk.",
    ".kbBBBkGYGkBBBk.",
    "..kWWkWGkWWWWk..",
    "..kwWWWWWWWWWk..",
    "...kvwwwwwwwWk..",
    "....kkvvvvkk....",
    "......kkkk......",
]
# The cap lifts on its hinge and the light shows in the seam.
BALL_CRACK = [
    "......kkkk......",
    "....kkCCCCkk....",
    "...kCHCMMCCCk...",
    "..kkkkkkkkkkkk..",
    "..kOOOOOYOOOOk..",
    ".kBBBBBkGYGkBbk.",
    "..kWWWWWkGkWWk..",
    "..kWWWWWWWWWwk..",
    "...kWwwwwwwwvk..",
    "....kkvvvvkk....",
    "......kkkk......",
]
BALL_OPEN = [
    ".......Y........",
    "......YOY.......",
    "...kkkYOYkkk....",
    "..kCHkOYOkCCk...",
    ".kkkkOYYYOkkkk..",
    ".kBkOYYYYYOkBk..",
    "..kWOYYYYYOWWk..",
    "..kWWOOOOOWWwk..",
    "...kWwwwwwwwvk..",
    "....kkvvvvkk....",
    "......kkkk......",
]


def beam(rows_above):
    """A column of ichor light rising rows_above pixels from the open ball."""
    out = []
    for y in range(rows_above):
        if y % 4 == 0:
            out.append(".......Y........")
        elif y % 4 == 1:
            out.append("......YO........")
        elif y % 4 == 2:
            out.append(".......OY.......")
        else:
            out.append("......YO........")
    return out


def frame(rows, top):
    """Place rows on a 16x32 frame with its first row at y = top."""
    full = ["." * 16] * top + rows
    full += ["." * 16] * (32 - len(full))
    return full[:32]


def ball_frames():
    return [
        frame(BALL_CLOSED, 12),
        frame(BALL_ROCK, 12),
        frame(BALL_CRACK, 12),
        frame(BALL_OPEN, 10),
        frame(beam(10) + BALL_OPEN, 0),
    ]


# Each ball: (cap, cap light, mark, band, band shade, lower, lower shade,
# lower dark); None for a mark means none is painted.
CLAY_BAND = ((120, 48, 24), (88, 40, 24))
BUFF = ((248, 240, 216), (216, 200, 160), (176, 152, 112))
GOLD_LOWER = ((240, 192, 64), (200, 144, 40), (152, 96, 40))
BALL_SPECS = {
    "master":  ((104, 48, 104), (160, 96, 152), (232, 136, 184), CLAY_BAND, BUFF),
    "ultra":   ((48, 40, 40), (96, 80, 72), (240, 192, 64), CLAY_BAND, BUFF),
    "great":   ((48, 104, 176), (112, 168, 224), (184, 72, 48), CLAY_BAND, BUFF),
    "safari":  ((96, 112, 48), (144, 160, 72), (56, 72, 32), CLAY_BAND, ((216, 200, 144), (184, 160, 104), (136, 112, 72))),
    "net":     ((24, 56, 120), (48, 104, 176), (32, 24, 24), CLAY_BAND, BUFF),
    "dive":    ((48, 104, 176), (112, 168, 224), (248, 240, 216), CLAY_BAND, BUFF),
    "nest":    ((120, 136, 56), (168, 184, 96), (64, 80, 32), CLAY_BAND, GOLD_LOWER),
    "repeat":  ((184, 72, 48), (224, 136, 88), (240, 192, 64), CLAY_BAND, GOLD_LOWER),
    "timer":   ((232, 216, 176), (248, 248, 232), (184, 72, 48), ((32, 24, 24), (32, 24, 24)), BUFF),
    "luxury":  ((48, 40, 40), (96, 80, 72), (184, 72, 48), ((200, 144, 40), (152, 96, 40)), ((88, 72, 64), (64, 48, 40), (40, 32, 32))),
    "premier": ((248, 240, 216), (255, 255, 248), None, ((184, 72, 48), (120, 48, 24)), BUFF),
    "dusk":    ((56, 72, 32), (96, 112, 48), (184, 72, 48), CLAY_BAND, ((64, 56, 48), (48, 40, 32), (32, 24, 24))),
    "heal":    ((224, 136, 136), (248, 192, 184), (248, 240, 216), ((248, 240, 216), (216, 200, 160)), BUFF),
    "quick":   ((48, 104, 176), (112, 168, 224), (240, 192, 64), CLAY_BAND, GOLD_LOWER),
    "cherish": ((152, 32, 40), (200, 72, 64), (240, 192, 64), ((88, 24, 24), (64, 16, 16)), ((184, 72, 48), (152, 48, 40), (104, 32, 24))),
    "park":    ((240, 192, 64), (248, 224, 136), (48, 104, 176), CLAY_BAND, ((112, 168, 224), (48, 104, 176), (24, 56, 120))),
    "fast":    ((240, 192, 64), (248, 224, 136), (184, 72, 48), CLAY_BAND, BUFF),
    "level":   ((184, 72, 48), (224, 136, 88), (240, 192, 64), CLAY_BAND, BUFF),
    "lure":    ((48, 104, 176), (112, 168, 224), (184, 72, 48), CLAY_BAND, BUFF),
    "heavy":   ((112, 112, 120), (160, 160, 168), (32, 24, 24), CLAY_BAND, BUFF),
    "love":    ((224, 120, 152), (248, 176, 192), (248, 240, 216), CLAY_BAND, BUFF),
    "friend":  ((120, 136, 56), (168, 184, 96), (184, 72, 48), CLAY_BAND, BUFF),
    "moon":    ((24, 56, 120), (48, 104, 176), (240, 192, 64), CLAY_BAND, BUFF),
    "sport":   ((200, 144, 40), (240, 192, 64), (184, 72, 48), CLAY_BAND, BUFF),
    "dream":   ((200, 120, 168), (232, 168, 200), (248, 240, 216), CLAY_BAND, BUFF),
    "beast":   ((24, 56, 120), (48, 104, 176), (240, 192, 64), ((240, 192, 64), (200, 144, 40)), BUFF),
    "strange": ((112, 168, 224), (176, 216, 240), (120, 136, 56), CLAY_BAND, BUFF),
}

# A generic ball palette: one index per role, shared by every non-folk sheet.
GEN_KEY = {"k": 1, "C": 2, "H": 3, "M": 4, "B": 5, "b": 6, "W": 7, "w": 8, "v": 9,
           "G": 10, "g": 11, "Y": 12, "O": 13}
GOLD_BTN = ((240, 192, 64), (200, 144, 40), (248, 240, 200), (240, 192, 64))


def gen_palette(spec):
    cap, light, mark, band, lower = spec
    pal = [TRANSPARENT, INK, cap, light, mark or cap, band[0], band[1],
           lower[0], lower[1], lower[2]] + list(GOLD_BTN) + [(0, 0, 0)] * 2
    return pal


def folk_key():
    """ball_poke.png in ichor_folk.pal's fixed order (sprites_folk.py)."""
    # 1 ink, 2 brown, 3 terra, 4 ochre, 5 gold, 6 skin_d, 7 skin_l,
    # 8 linen_d, 9 linen_l, 10 gray
    return {"k": 1, "C": 2, "H": 6, "M": 2, "B": 3, "b": 2, "W": 9, "w": 8, "v": 10,
            "G": 5, "g": 4, "Y": 9, "O": 5}


def ball_sheet(key, frames_wide):
    sheet = np.zeros((32, 16 * frames_wide), np.uint8)
    for i, rows in enumerate(ball_frames()):
        sheet[:, i * 16:(i + 1) * 16] = grid(rows, key)
    return sheet


# --------------------------------------------------------------------------
# Write and preview
# --------------------------------------------------------------------------

def write():
    frames = emote_frames()
    assert len(frames) == 23
    save_png(os.path.join(MISC, "emotes.png"), np.hstack(frames), EMOTE_PAL)
    write_jasc(os.path.join(MISC, "emotes.pal"), EMOTE_PAL)
    print("wrote graphics/misc/emotes.png, emotes.pal")

    folk = read_jasc(FOLK_PAL)
    assert folk[1] == INK and folk[9] == (248, 240, 216), "ichor_folk.pal changed order"
    save_png(os.path.join(BALL_DIR, "ball_poke.png"), ball_sheet(folk_key(), 5), folk)
    for name, spec in BALL_SPECS.items():
        save_png(os.path.join(BALL_DIR, f"ball_{name}.png"), ball_sheet(GEN_KEY, 7), gen_palette(spec))
    print(f"wrote graphics/object_events/pics/misc/ball_*.png ({1 + len(BALL_SPECS)} sheets)")


def preview(out_dir):
    S = 6
    rows = []
    # Emotes on a sand-colored ground, A and B frames.
    em = np.hstack(emote_frames())
    pal = np.array(EMOTE_PAL, np.uint8)
    rgb = pal[em]
    rgb[em == 0] = (232, 216, 176)
    rows.append(rgb)
    folk = read_jasc(FOLK_PAL)
    for name, key, width, p in [("poke", folk_key(), 5, folk)] + \
            [(n, GEN_KEY, 5, gen_palette(s)) for n, s in BALL_SPECS.items()]:
        a = ball_sheet(key, width)[:, :80]
        c = np.array(p, np.uint8)[a]
        c[a == 0] = (232, 216, 176)
        rows.append(c)
    w = max(r.shape[1] for r in rows)
    sheet = np.full((sum(r.shape[0] + 2 for r in rows[:1]) + 34 * ((len(rows) - 1 + 5) // 6), w * 0 + 6 * 82, 3), 40, np.uint8)
    y = 0
    sheet[0:16, 0:min(368, sheet.shape[1])] = rows[0][:, :min(368, sheet.shape[1])]
    y = 18
    for i, r in enumerate(rows[1:]):
        x = (i % 6) * 82
        yy = y + (i // 6) * 34
        sheet[yy:yy + 32, x:x + 80] = r
    im = Image.fromarray(sheet, "RGB").resize((sheet.shape[1] * S, sheet.shape[0] * S), Image.NEAREST)
    path = os.path.join(out_dir, "follower_icons.png")
    im.save(path)
    print("wrote", path)


if __name__ == "__main__":
    if "--write" in sys.argv:
        write()
    if "--preview" in sys.argv:
        preview(sys.argv[sys.argv.index("--preview") + 1])
