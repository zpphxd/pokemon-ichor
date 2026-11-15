"""The boot cards: the copyright notice, the "powered by" card and the studio mark.

All three are black gloss with terracotta and gold, framed by the meander the
title and the dialogue box use. intro_screen.py writes them; see
design/phase1/INTRO.md.
"""
import math

import numpy as np

import intro_lib as L

W, H = 240, 160

# The 1x meander, as on the dialogue frames (graphics/text_window); the title
# draws it at 2x.
MEANDER = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]


def meander_rule(img, x0, x1, y, clay, ink):
    """A 7-row clay rule with an ink meander, x0..x1 inclusive (period 8)."""
    for r in range(7):
        for x in range(x0, x1 + 1):
            on = 1 <= r <= 5 and MEANDER[r - 1][(x - x0) % 8] == "#"
            img[y + r, x] = ink if on else clay
    # close the key at the right end so it does not stop mid-hook
    for r in range(1, 6):
        img[y + r, x1] = clay


def center_text(img, rows, y, v, cx=W // 2):
    w = len(rows[0])
    x0 = cx - w // 2
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == "#":
                img[y + dy, x0 + dx] = v
    return x0, w


# --------------------------------------------------------------------------
# 1. Copyright card (graphics/intro/copyright.png, BG0, palette 0)
# --------------------------------------------------------------------------
# credits.c's "THE END" screen reuses this palette: its letters use colors 9,
# 13 and 15 on 0/1, so those stay a mid, a light and the brightest color.
COPYRIGHT_PAL = [
    L.INK,          # 0 backdrop
    L.INK,          # 1 ink
    L.SHEEN,        # 2
    L.CLAY_DEEP,    # 3
    L.CLAY_SHADE,   # 4
    L.GOLD_DEEP,    # 5
    L.GOLD_SHADOW,  # 6
    L.GOLD_MID,     # 7
    L.GOLD_LIT,     # 8
    L.CLAY,         # 9   THE END: shade
    L.GOLD_GLINT,   # 10
    L.CLAY_LIGHT,   # 11
    L.RED,          # 12
    L.CLAY_HI,      # 13  THE END: light
    L.CLAY_LIGHT,   # 14
    L.WHITE,        # 15  THE END: letters
]

DROP_SMALL = [
    "..g..",
    "..g..",
    ".gl#.",
    ".lmm#",
    "glmms",
    ".mms.",
    "..s..",
]
DROP_SMALL_KEY = {"g": 10, "l": 8, "m": 7, "s": 6, "#": 5}

COPYRIGHT_LINES = [
    # (text, color, y)
    ("POKÉMON © NINTENDO / CREATURES / GAME FREAK", 15, 58),
    ("ICHOR IS A FAN-MADE GAME,", 13, 88),
    ("NOT AFFILIATED WITH THEM.", 13, 99),
]


def build_copyright():
    img = np.zeros((H, W), int)
    meander_rule(img, 48, 191, 40, 9, 1)
    meander_rule(img, 48, 191, 116, 9, 1)
    for text, v, y in COPYRIGHT_LINES:
        rows = L.set_text7(text)
        assert len(rows[0]) <= 228, (text, len(rows[0]))
        center_text(img, rows, y - 2, v)
    L.paste(img, DROP_SMALL, W // 2 - 2, 73, DROP_SMALL_KEY)
    return img


# --------------------------------------------------------------------------
# 2. Powered by (graphics/expansion_intro/: BG3 4bpp + BG2 8bpp, credits.pal)
# --------------------------------------------------------------------------
POWERED_PAL = [
    L.INK,          # 0 backdrop
    L.CLAY,         # 1 rule clay
    L.INK,          # 2 rule ink
    L.CLAY_HI,      # 3 small text
    L.GOLD_DEEP,    # 4 d
    L.GOLD_SHADOW,  # 5 s
    L.GOLD_MID,     # 6 m
    L.GOLD_LIT,     # 7 l
    L.GOLD_GLINT,   # 8 g
    L.WHITE,        # 9 captions
    L.CLAY_SHADE,   # 10
]
VCUT_KEY = {".": 0, "d": 4, "s": 5, "m": 6, "l": 7, "g": 8}


def scale_rows(rows, k):
    out = []
    for r in rows:
        line = "".join(ch * k for ch in r)
        out += [line] * k
    return out


def build_powered_by():
    """Returns (bg3, bg2): the frame and 'POWERED BY' on BG3, the gilded
    PRET x RHH mark and its captions on BG2 (which fades in over BG3)."""
    bg3 = np.zeros((H, W), int)
    meander_rule(bg3, 48, 191, 30, 1, 2)
    meander_rule(bg3, 48, 191, 124, 1, 2)
    center_text(bg3, L.set_text7("POWERED BY"), 44, 3)

    bg2 = np.zeros((H, W), int)
    mark = L.set_rows(L.F9, "PRET × RHH", 2, 9)
    mark = scale_rows(mark, 2)
    shaded = L.vcut(mark)
    w = len(shaded[0])
    x0 = W // 2 - w // 2
    y0 = 66
    for dy, row in enumerate(shaded):
        for dx, ch in enumerate(row):
            if ch != ".":
                bg2[y0 + dy, x0 + dx] = VCUT_KEY[ch]
    # captions under each half, as upstream's card has them
    left_w = len(scale_rows(L.set_rows(L.F9, "PRET", 2, 9), 2)[0])
    right_w = len(scale_rows(L.set_rows(L.F9, "RHH", 2, 9), 2)[0])
    center_text(bg2, L.set_text7("POKEEMERALD"), y0 + 21, 9, cx=x0 + left_w // 2)
    center_text(bg2, L.set_text7("EXPANSION"), y0 + 21, 9, cx=x0 + w - right_w // 2)
    return bg3, bg2


# --------------------------------------------------------------------------
# 3. The studio mark: a drop of ichor ringed by the Twelve, over ΙΧΩΡ
# --------------------------------------------------------------------------
# BG palette for the mark. Each group has its own colors so intro.c can light
# them one after another: the drop, the ring of twelve, the letters.
STUDIO_PAL = [
    L.INK,          # 0 backdrop
    L.GOLD_DEEP,    # 1 drop: d
    L.GOLD_SHADOW,  # 2 drop: s
    L.GOLD_MID,     # 3 drop: m
    L.GOLD_LIT,     # 4 drop: l
    L.GOLD_GLINT,   # 5 drop: g
    L.GOLD_MID,     # 6 ring: dot
    L.GOLD_GLINT,   # 7 ring: dot highlight
    L.GOLD_DEEP,    # 8 letters: d
    L.GOLD_SHADOW,  # 9 letters: s
    L.GOLD_MID,     # 10 letters: m
    L.GOLD_LIT,     # 11 letters: l
    L.GOLD_GLINT,   # 12 letters: g
    L.GOLD_SHADOW,  # 13 credit: shadow wall
    L.GOLD_LIT,     # 14 credit: lit wall
    L.GOLD_MID,     # 15 credit: "A GAME BY"
]
STUDIO_DROP = (1, 6)      # palette ranges [a, b) intro.c fades separately
STUDIO_RING = (6, 8)
STUDIO_LETTERS = (8, 13)
STUDIO_CREDIT = (13, 16)

MARK_CX, MARK_CY = 120, 54   # ring center (screen)
RING_R = 31
DROP_TOP = 36                # the big drop: tip row
LETTERS_Y = 94
CREDIT_BY_Y = 123            # "A GAME BY", 7 px plain capitals
CREDIT_NAME_Y = 133          # "ZACH POWERS", 11 px gilded capitals

# The credit's name, 11 px capitals with 2 px stems: the title's POKEMON
# banner style (title_lettering.POKEMON) a size up, cut with the same
# shadow-left, lit-right V (shade2) so it pairs with ΙΧΩΡ as POKEMON does with
# ICHOR on the title.
CREDIT11 = {
    "Z": ["########", "......##", ".....##.", ".....##.", "....##..", "...##...", "..##....",
          ".##.....", ".##.....", "##......", "########"],
    "A": ["....#....", "...###...", "...###...", "..##.##..", "..##.##..", ".##...##.", ".#######.",
          ".##...##.", "##.....##", "##.....##", "##.....##"],
    "C": ["..#####.", ".##...##", "##......", "##......", "##......", "##......", "##......",
          "##......", "##......", ".##...##", "..#####."],
    "H": ["##....##"] * 5 + ["########"] + ["##....##"] * 5,
    "P": ["######..", "##...##.", "##....##", "##....##", "##...##.", "######..", "##......",
          "##......", "##......", "##......", "##......"],
    "O": ["..#####..", ".##...##.", "##.....##", "##.....##", "##.....##", "##.....##", "##.....##",
          "##.....##", "##.....##", ".##...##.", "..#####.."],
    "W": ["##........##", "##........##", "##........##", "##...##...##", "##...##...##",
          "##..####..##", "##..#..#..##", "##.##..##.##", "####....####", "###......###",
          "##........##"],
    "E": ["#######", "##.....", "##.....", "##.....", "##.....", "######.", "##.....", "##.....",
          "##.....", "##.....", "#######"],
    "R": ["######..", "##...##.", "##....##", "##....##", "##...##.", "######..", "##.##...",
          "##..##..", "##...##.", "##....##", "##....##"],
    "S": [".######.", "##....##", "##......", "##......", ".##.....", "..####..", ".....##.",
          "......##", "......##", "##....##", ".######."],
    " ": ["....."] * 11,
}
CREDIT_KEY = {".": 0, "s": 13, "l": 14}
CREDIT_NAME = "ZACH POWERS"
CREDIT_BY = "A GAME BY"

# Greek capitals for ΙΧΩΡ, 20 px, 3 px strokes, with wedge apices.
GREEK20 = {
    "Ι": [
        "#######",
        ".#####.",
        "..###..",
    ] + ["..###.."] * 14 + [
        "..###..",
        ".#####.",
        "#######",
    ],
    "Χ": [
        "####.......####",
        ".###.......###.",
        ".###.......###.",
        "..###.....###..",
        "..###.....###..",
        "...###...###...",
        "...###...###...",
        "....###.###....",
        ".....#####.....",
        "......###......",
        "......###......",
        ".....#####.....",
        "....###.###....",
        "...###...###...",
        "...###...###...",
        "..###.....###..",
        "..###.....###..",
        ".###.......###.",
        ".###.......###.",
        "####.......####",
    ],
    "Ω": [
        ".....#######.....",
        "...###########...",
        "..####.....####..",
        ".###.........###.",
        ".###.........###.",
        "###...........###",
        "###...........###",
        "###...........###",
        "###...........###",
        "###...........###",
        "###...........###",
        ".###.........###.",
        ".###.........###.",
        "..###.......###..",
        "...###.....###...",
        "....###...###....",
        ".....##...##.....",
        "#######...#######",
        "#######...#######",
        "#######...#######",
    ],
    "Ρ": [
        "###########...",
        ".###########..",
        "..###....####.",
        "..###.....###.",
        "..###.....###.",
        "..###.....###.",
        "..###....####.",
        "..###########.",
        "..##########..",
        "..###.........",
        "..###.........",
        "..###.........",
        "..###.........",
        "..###.........",
        "..###.........",
        "..###.........",
        "..###.........",
        "..###.........",
        ".#####........",
        "#######.......",
    ],
}
LETTER_KEY = {".": 0, "d": 8, "s": 9, "m": 10, "l": 11, "g": 12}


def drop_mask(w, h, tip=0.38):
    """A falling drop: round belly, tapering to a point at the top."""
    m = np.zeros((h, w), bool)
    r = w / 2
    cy = h - r
    for y in range(h):
        for x in range(w):
            px, py = x + 0.5 - w / 2, y + 0.5
            if py >= cy:
                inside = px * px + (py - cy) ** 2 <= r * r
            else:
                # the taper: width grows as a curve from the tip to the belly
                t = py / cy
                half = r * (t ** tip) * math.sqrt(max(0.0, 1 - (1 - t) ** 2)) if t > 0 else 0
                inside = abs(px) <= half
            m[y, x] = inside
    return m


def shade_drop(m, key, glint=True):
    """Gold drop lit from the top left. Each row is treated as a slice of a
    rounded body: the normal leans out toward the row's edges and up along the
    taper, Lambert-lit, quantized to the gold ramp, with a deep rim on the
    lower right and a glint high on the left of the belly."""
    h, w = m.shape
    out = np.zeros((h, w), int)
    ys, xs = np.nonzero(m)
    r = w / 2
    belly_cy = h - r
    lx, ly, lz = -0.55, -0.6, 0.58
    n = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / n, ly / n, lz / n
    levels = ["d", "s", "m", "l", "l"]
    for y, x in zip(ys, xs):
        row = np.nonzero(m[y])[0]
        c = (row.min() + row.max() + 1) / 2
        half = max(0.5, (row.max() + 1 - row.min()) / 2)
        nx = (x + 0.5 - c) / (half + 0.4)
        if y + 0.5 >= belly_cy:
            ny = (y + 0.5 - belly_cy) / (r + 0.4)
        else:
            ny = -0.35
        nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
        i = max(0.0, nx * lx + ny * ly + nz * lz)
        v = levels[min(4, int(i * 4.6))]
        edge_r = not (x + 1 < w and m[y, x + 1])
        edge_b = not (y + 1 < h and m[y + 1, x])
        if (edge_r or edge_b) and nx > -0.2:
            v = "d"
        out[y, x] = key[v]
    if glint and w >= 7:
        gy = int(round(belly_cy - r * 0.25))
        gx = int(round(w / 2 - r * 0.45))
        for dx, dy in ((0, 0), (0, 1), (0, -1)):
            if 0 <= gy + dy < h and m[gy + dy, gx + dx]:
                out[gy + dy, gx + dx] = key["g"]
    return out


def build_studio():
    img = np.zeros((H, W), int)
    # the drop of ichor
    dm = drop_mask(19, 30)
    drop = shade_drop(dm, {"d": 1, "s": 2, "m": 3, "l": 4, "g": 5})
    x0 = MARK_CX - 19 // 2
    for y in range(30):
        for x in range(19):
            if drop[y, x]:
                img[DROP_TOP + y, x0 + x] = drop[y, x]
    # the Twelve: twelve dots on a ring, one at the top
    for k in range(12):
        a = -math.pi / 2 + k * 2 * math.pi / 12
        cx = int(round(MARK_CX + RING_R * math.cos(a)))
        cy = int(round(MARK_CY + RING_R * math.sin(a)))
        L.paste(img, [".6.", "676", ".6."], cx - 1, cy - 1, {"6": 6, "7": 7})
    # ΙΧΩΡ
    word = L.set_rows(GREEK20, "ΙΧΩΡ", 6, 20)
    shaded = L.vcut(word)
    w = len(shaded[0])
    x0 = W // 2 - w // 2
    for dy, row in enumerate(shaded):
        for dx, ch in enumerate(row):
            if ch != ".":
                img[LETTERS_Y + dy, x0 + dx] = LETTER_KEY[ch]
    # the credit: "A GAME BY" over the name, in the gold of the mark
    center_text(img, L.set_text7(CREDIT_BY, gap=2), CREDIT_BY_Y - 2, 15)
    name = L.shade2(L.set_rows(CREDIT11, CREDIT_NAME, 2, 11))
    x0 = W // 2 - len(name[0]) // 2
    for dy, row in enumerate(name):
        for dx, ch in enumerate(row):
            if ch != ".":
                img[CREDIT_NAME_Y + dy, x0 + dx] = CREDIT_KEY[ch]
    return img


# Sprites for the studio card (OBJ palette: STUDIO_OBJ_PAL)
STUDIO_OBJ_PAL = [
    (0, 0, 0),
    L.GOLD_DEEP,     # 1
    L.GOLD_SHADOW,   # 2
    L.GOLD_MID,      # 3
    L.GOLD_LIT,      # 4
    L.GOLD_GLINT,    # 5
    (248, 248, 232), # 6 white-hot
]


def build_drop_frames():
    """16x32 frames: 0-3 the bead forming and hanging, 4 falling (stretched),
    5 a round drop. The bead hangs from the top edge of the sprite."""
    frames = []
    key = {"d": 1, "s": 2, "m": 3, "l": 4, "g": 5}
    for (w, h, tip) in ((3, 3, 1.0), (5, 6, 0.6), (7, 10, 0.45), (8, 14, 0.38), (7, 18, 0.30), (9, 11, 0.8)):
        f = np.zeros((32, 16), int)
        dm = drop_mask(w, h, tip)
        d = shade_drop(dm, key) if w >= 5 else np.where(dm, 4, 0)
        x0 = 8 - (w + 1) // 2 + (1 if w % 2 == 0 else 0)
        y0 = 2      # every frame hangs from the same point, so the fall is continuous
        f[y0:y0 + h, x0:x0 + w] = np.where(d > 0, d, f[y0:y0 + h, x0:x0 + w])
        frames.append(f)
    return frames


def build_ripple_frames():
    """64x64 rings expanding to the ring of the Twelve (radius 31)."""
    frames = []
    for i, r in enumerate((5, 10, 16, 22, 27, 31)):
        f = np.zeros((64, 64), int)
        col = [6, 5, 4, 4, 3, 2][i]
        for y in range(64):
            for x in range(64):
                d = math.hypot(x + 0.5 - 32, y + 0.5 - 32)
                if abs(d - r) < 0.75:
                    f[y, x] = col
                elif abs(d - r) < 1.3 and i < 3:
                    f[y, x] = 3
        frames.append(f)
    return frames
