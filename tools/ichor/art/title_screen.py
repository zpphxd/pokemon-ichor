#!/usr/bin/env python3
"""Draw Ichor's title screen: the three Fates on a black-figure amphora.

The screen is the belly of a panel amphora. A reserved clay panel, framed top
and bottom by a meander, shows Clotho spinning, Lachesis measuring and Atropos
cutting a white thread. One golden thread runs free past them all: the
player, whose fate was never spun. The neck and foot are black gloss; the
neck carries the gilded ICHOR inscription, the foot carries PRESS START.

It reuses Emerald's title-screen layers, so the file names stay Emerald's:

  rayquaza.png/.bin     BG0, the painted panel (4bpp, palette 13)
  clouds.png/.bin       BG1, the golden thread (4bpp, palette 14), drifted
                        sideways and waved by title_screen.c
  pokemon_logo.png      BG2, the ICHOR inscription (8bpp, affine, shines)
  pokemon_logo.pal      BG palettes 0-13: row 0 the gold, row 13 the painting
  rayquaza_and_clouds.pal  BG palette 14: the thread; color 15 shimmers
  emerald_version.png   the version-banner sprite pair: POKEMON
  press_start.png       PRESS START and the fan-work line (sprites)

pokemon_logo.bin (the identity tilemap) and logo_shine.png are kept as they
are. The figures live in title_fates.py, the letters in title_lettering.py.
See design/phase1/TITLE.md for the layers and effects.

Usage: python3 tools/ichor/art/title_screen.py [--preview] [--capture | --capture-all]
  --preview      also writes build/title_preview/*.png, composited like the GBA
                 (BG1 blend and wave, sprites), for review at 3x.
  --capture      boots the built ROM headlessly and saves the SHOTS frames to
                 design/phase1/img/title_*.png (run make first, and
                 tools/ichor/smoke_test.sh once to build the runner).
  --capture-all  saves every 2nd title frame to build/title_capture/.
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import title_fates as FATES
import title_lettering as LET

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/title_screen"
PREVIEW = ROOT / "build/title_preview"

W, H = 240, 160

# --------------------------------------------------------------------------
# Palettes. Master palette from design/phase1/PLAN.md; every value is a
# multiple of 8 so it maps exactly to BGR555.
# --------------------------------------------------------------------------
INK = (32, 24, 24)

# BG row 0, used by the 8bpp ICHOR inscription. Index 0 is the backdrop.
GOLD = [
    INK,              # 0 backdrop
    (120, 72, 16),    # 1 d  deep edge
    (168, 112, 32),   # 2 s  shadow wall
    (200, 144, 40),   # 3 m  turning wall
    (240, 192, 64),   # 4 l  lit wall
    (248, 232, 152),  # 5 g  glint
]
GOLD_KEY = {".": 0, "d": 1, "s": 2, "m": 3, "l": 4, "g": 5}

# BG row 13, the painted panel (BG0).
PAINT_ROW = 13
PAINT = [
    INK,              # 0 (unused: BG0 is opaque)
    INK,              # 1 black gloss
    (56, 48, 48),     # 2 gloss sheen
    (120, 48, 24),    # 3 clay, deep
    (152, 64, 32),    # 4 clay, shade
    (184, 88, 48),    # 5 clay
    (208, 112, 64),   # 6 clay, light
    (224, 136, 88),   # 7 clay, highlight
    (232, 216, 176),  # 8 added white
    (128, 40, 40),    # 9 added red
]
P_INK, P_SHEEN, P_WHITE, P_RED = 1, 2, 8, 9
CLAY_LEVELS = [3, 4, 5, 6, 7]

# BG row 14, the golden thread (BG1). title_screen.c pulses color 15.
THREAD_ROW = 14
THREAD = [(0, 0, 0)] * 16
THREAD[1] = (136, 80, 16)    # underside
THREAD[2] = (232, 176, 48)   # body
THREAD[3] = (248, 216, 104)  # bright
THREAD[15] = (248, 232, 152)  # glint (animated)

# OBJ palettes.
BANNER = GOLD[:]              # POKEMON: same golds, index 0 transparent
PRESS_PAL = [
    (0, 0, 0),
    (120, 72, 16),    # 1 shadow
    (200, 144, 40),   # 2 mid
    (240, 192, 64),   # 3 lit
    (248, 232, 152),  # 4 glint
    (152, 64, 32),    # 5 fan line, clay shade
    (224, 136, 88),   # 6 fan line, clay light
]

# --------------------------------------------------------------------------
# Layout (screen pixels).
# --------------------------------------------------------------------------
PANEL_X0, PANEL_X1 = 8, 231          # reserved panel inside the black body
TOP_BAND_Y = 52                      # 13 rows: meander over the panel
PANEL_Y0 = TOP_BAND_Y + 13           # 65
GROUND_Y = 128                       # last row of the figures' feet
BOTTOM_BAND_Y = GROUND_Y + 1         # 13 rows: ground line + meander
FOOT_Y = BOTTOM_BAND_Y + 13          # 142: black foot with PRESS START

ICHOR_TOP = 17                       # final screen row of the inscription
BG2_X_OFFSET = 29                    # title_screen.c: BG2X = -29
ICHOR_GAP = 9

# Figures: (grid, left x). Feet stand on GROUND_Y.
FIGURES = [
    ("clotho", FATES.CLOTHO, 24),
    ("lachesis", FATES.LACHESIS, 96),
    ("atropos", FATES.ATROPOS, 158),
]
# Name labels painted in the field above them: (text, left x, top y).
LABELS = [
    ("ΚΛΩΘΩ", 14, 68),
    ("ΛΑΧΕΣΙΣ", 92, 68),
    ("ΑΤΡΟΠΟΣ", 168, 68),
]

# Banner sprite pair (title_screen.c VERSION_BANNER_*): left half centered on
# BANNER_LEFT_X, 64 px apart; BANNER_Y_GOAL is the sprite center at rest.
BANNER_LEFT_X, BANNER_Y_GOAL = 88, 16
BANNER_TEXT_TOP = 2                  # row in the 128x32 sprite

# PRESS START / fan line sprites (title_screen.c CreatePressStartBanner etc.)
START_BANNER_X = 120
PRESS_Y, FAN_Y = 147, 155            # sprite centers

# The golden thread (BG1): a slow wave across the panel at knee height.
THREAD_Y = 110
THREAD_AMP = 3.0
THREAD_PERIOD = 128

# Bayer 4x4 for the few dithered transitions.
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


# --------------------------------------------------------------------------
# The pot's surface
# --------------------------------------------------------------------------
def clay_level(x):
    """Clay level across the panel (1 shade, 2 clay, 3 light): the belly's
    curve lit from the top left. Flat fields, with stippled ramps between."""
    # Ramps fall in open field, never right behind a figure's contour.
    keys = [(8, 1.0), (10, 1.0), (24, 2.0), (52, 2.0), (64, 3.0), (82, 3.0),
            (98, 2.0), (198, 2.0), (214, 1.0), (231, 1.0)]
    for (xa, a), (xb, b) in zip(keys, keys[1:]):
        if xa <= x <= xb:
            return a + (b - a) * (x - xa) / (xb - xa)
    return keys[-1][1]


def clay_at(x, y):
    lv = clay_level(x)
    base = int(math.floor(lv))
    if lv - base > BAYER[y % 4][x % 4]:
        base += 1
    return CLAY_LEVELS[min(4, max(0, base))]


def gloss_at(x, y):
    """Black gloss."""
    return P_INK


# Greek key: the pottery UI's meander (graphics/text_window) drawn at twice the
# size, so the title and the dialogue box share one motif.
MEANDER_UNIT = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]


def meander_row(r, x):
    """Pixel of the 2x meander at band row r (0..9) and absolute x."""
    unit = MEANDER_UNIT[r // 2]
    return unit[(x // 2) % len(unit)] == "#"


def paint_bands(img):
    # Top band: clay, meander, clay, ink rule under it.
    for r in range(13):
        y = TOP_BAND_Y + r
        for x in range(PANEL_X0, PANEL_X1 + 1):
            if r == 12:
                img[y, x] = P_INK
            elif 1 <= r <= 10 and meander_row(r - 1, x - PANEL_X0 + 4):
                img[y, x] = P_INK
            else:
                img[y, x] = clay_at(x, y)
    # Bottom band: the ground line, clay, meander, clay.
    for r in range(13):
        y = BOTTOM_BAND_Y + r
        for x in range(PANEL_X0, PANEL_X1 + 1):
            if r == 0:
                img[y, x] = P_INK
            elif 2 <= r <= 11 and meander_row(r - 2, x - PANEL_X0 + 4):
                img[y, x] = P_INK
            else:
                img[y, x] = clay_at(x, y)


FIG_KEY = {"#": P_INK, "w": P_WHITE, "r": P_RED}


def paint_figure(img, grid, x0):
    check_glyph(grid, "figure")
    h = len(grid)
    y0 = GROUND_Y - h + 1
    for dy, row in enumerate(grid):
        for dx, ch in enumerate(row):
            x, y = x0 + dx, y0 + dy
            if ch == "." or not (0 <= x < W and 0 <= y < H):
                continue
            img[y, x] = clay_at(x, y) if ch == "i" else FIG_KEY[ch]
    return y0


def grid_point(grid, x0, pt):
    return x0 + pt[0], GROUND_Y - len(grid) + 1 + pt[1]


def paint_thread(img, pts):
    """The mortal thread: added white, sagging slightly between hands."""
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        span = xb - xa
        for x in range(xa, xb + 1):
            t = (x - xa) / span if span else 0
            sag = 2.0 * math.sin(math.pi * t) if span > 24 else 0
            y = round(ya + (yb - ya) * t + sag)
            img[y, x] = P_WHITE


def build_painting():
    img = np.zeros((H, W), int)
    for y in range(H):
        for x in range(W):
            img[y, x] = gloss_at(x, y)
    for y in range(PANEL_Y0, GROUND_Y + 1):
        for x in range(PANEL_X0, PANEL_X1 + 1):
            img[y, x] = clay_at(x, y)
    paint_bands(img)
    fig = {}
    for name, grid, x0 in FIGURES:
        paint_figure(img, grid, x0)
        fig[name] = (grid, x0)
    # The white thread: Clotho's hand -> along Lachesis' rod -> Atropos' jaws.
    hand = grid_point(*fig["clotho"], FATES.CLOTHO_HAND)
    lx0, lx1, ly = FATES.LACHESIS_ROD
    rod0 = grid_point(*fig["lachesis"], (lx0, ly))
    rod1 = grid_point(*fig["lachesis"], (lx1, ly))
    jaws = grid_point(*fig["atropos"], FATES.ATROPOS_JAWS)
    paint_thread(img, [hand, rod0, rod1, jaws])
    for text, x, y in LABELS:
        for gy, row in enumerate(set_word(LET.GREEK, text, 1, 5)):
            for gx, ch in enumerate(row):
                if ch == "#":
                    img[y + gy, x + gx] = P_INK
    return img


# --------------------------------------------------------------------------
# The golden thread (BG1, 256x256, wraps horizontally as it drifts)
# --------------------------------------------------------------------------
def thread_y(x):
    return THREAD_Y + THREAD_AMP * math.sin(2 * math.pi * x / THREAD_PERIOD)


def build_thread():
    """A 2 px cord: a bright core over a gold body, with a dark gold lip where
    the curve steps so the line reads smooth instead of stair-stepped. A few
    core pixels use color 15, which title_screen.c pulses, so glints travel
    along the thread as it drifts."""
    img = np.zeros((256, 256), int)
    for x in range(256):
        y = thread_y(x)
        yc = int(round(y))
        img[yc, x] = 15 if (x % 32) in (5, 6, 21) else 3
        img[yc + 1, x] = 2
        frac = y - yc
        if abs(frac) > 0.3:
            ny = yc - 1 if frac < 0 else yc + 2
            if img[ny, x] == 0:
                img[ny, x] = 1
    return img


# --------------------------------------------------------------------------
# Lettering
# --------------------------------------------------------------------------
def check_glyph(rows, name):
    assert len({len(r) for r in rows}) == 1, f"ragged glyph {name}"


def shade_thin(mask_rows):
    """Cut a V into a 2 px stroke: top/left pixels in shadow, the rest lit."""
    h, w = len(mask_rows), len(mask_rows[0])
    on = lambda x, y: 0 <= x < w and 0 <= y < h and mask_rows[y][x] == "#"
    out = []
    for y in range(h):
        row = ""
        for x in range(w):
            if not on(x, y):
                row += "."
            elif not on(x - 1, y) or not on(x, y - 1):
                row += "s"
            else:
                row += "l"
        out.append(row)
    return out


def set_word(glyphs, word, gap, h):
    rows = [""] * h
    for i, ch in enumerate(word):
        g = glyphs[ch]
        check_glyph(g, ch)
        for y in range(h):
            rows[y] += g[y] + ("." * gap if i < len(word) - 1 else "")
    return rows


def build_logo():
    """256x64, 8bpp indices into BG row 0. Screen x = texture x + 29."""
    word = set_word(LET.ICHOR, "ICHOR", ICHOR_GAP, 32)
    w = len(word[0])
    img = np.zeros((64, 256), int)
    x0 = 120 - BG2_X_OFFSET - w // 2
    for y, row in enumerate(word):
        for x, ch in enumerate(row):
            img[ICHOR_TOP + y, x0 + x] = GOLD_KEY[ch]
    assert not img[:8, :8].any(), "tile 0 must stay blank"
    return img


def build_banner():
    """128x32 sprite pair: POKEMON with the acute over the E."""
    glyphs = {k: shade_thin(v) for k, v in LET.POKEMON.items()}
    word = set_word(glyphs, "POKEMON", 4, 9)
    w = len(word[0])
    img = np.zeros((32, 128), int)
    x0 = 64 - w // 2
    top = BANNER_TEXT_TOP + 3
    for y, row in enumerate(word):
        for x, ch in enumerate(row):
            img[top + y, x0 + x] = GOLD_KEY[ch]
    # acute over the E (4th letter)
    ex = x0 + sum(len(LET.POKEMON[c][0]) + 4 for c in "POK")
    for y, row in enumerate(shade_thin(LET.ACUTE)):
        for x, ch in enumerate(row):
            if ch != ".":
                img[BANNER_TEXT_TOP + y, ex + 2 + x] = GOLD_KEY[ch]
    return img


def build_press_start():
    """160x24, 4bpp. Row 0 tiles 1-19: PRESS START; row 1 tiles 1-19: the
    fan-work line. title_screen.c shows tiles 1-20 and 21-40 as five 32x8
    sprites each, so image x maps to screen x - 32 (START_BANNER_X 120)."""
    img = np.zeros((24, 160), int)
    center = START_BANNER_X - 32  # image x that lands on the screen center
    press = set_word({k: shade_thin(v) if k != " " else v for k, v in LET.PRESS.items()},
                     "PRESS · START", 1, 7)
    w = len(press[0])
    x0 = center - w // 2
    pk = {".": 0, "s": 2, "l": 3}
    for y, row in enumerate(press):
        for x, ch in enumerate(row):
            img[0 + y, x0 + x] = pk[ch]
    fan = set_word(LET.SMALL, "A FAN WORK · 2026", 1, 5)
    w = len(fan[0])
    x0 = center - w // 2
    for y, row in enumerate(fan):
        for x, ch in enumerate(row):
            if ch == "#":
                img[8 + 1 + y, x0 + x] = 6
    assert x0 >= 8 and not img[:, :8].any(), "tile 0 of each row must stay blank"
    return img


# --------------------------------------------------------------------------
# Tiles and files
# --------------------------------------------------------------------------
def tileize(img, palette_row, first_tile=None, max_tiles=None, map_w=32, map_h=32):
    """Dedupe 8x8 tiles (with flips). Returns (tiles, tilemap u16 array)."""
    h, w = img.shape
    tiles, index = [], {}

    def add(t):
        key = t.tobytes()
        if key in index:
            return index[key]
        for flip, ft in ((1, t[:, ::-1]), (2, t[::-1, :]), (3, t[::-1, ::-1])):
            k = ft.tobytes()
            if k in index:
                return index[k][0], flip
        index[key] = (len(tiles), 0)
        tiles.append(t)
        return index[key]

    if first_tile is not None:
        add(first_tile)
    tmap = np.zeros((map_h, map_w), np.uint16)
    for ty in range(h // 8):
        for tx in range(w // 8):
            t = img[ty * 8:(ty + 1) * 8, tx * 8:(tx + 1) * 8].copy()
            n, flip = add(t)
            tmap[ty, tx] = n | ((flip & 1) << 10) | ((flip >> 1) << 11) | (palette_row << 12)
    for ty in range(map_h):
        for tx in range(map_w):
            if ty >= h // 8 or tx >= w // 8:
                tmap[ty, tx] = palette_row << 12
    if max_tiles:
        assert len(tiles) <= max_tiles, f"{len(tiles)} tiles > {max_tiles}"
    return tiles, tmap


def save_indexed(arr, palette, path):
    im = Image.fromarray(np.asarray(arr, np.uint8), "P")
    flat = []
    for c in palette:
        flat.extend(c)
    flat += [0] * (768 - len(flat))
    im.putpalette(flat)
    im.save(path, optimize=False)


def save_tilesheet(tiles, palette, path, per_row=16):
    rows = (len(tiles) + per_row - 1) // per_row
    sheet = np.zeros((rows * 8, per_row * 8), int)
    for i, t in enumerate(tiles):
        sheet[(i // per_row) * 8:(i // per_row) * 8 + 8, (i % per_row) * 8:(i % per_row) * 8 + 8] = t
    save_indexed(sheet, palette, path)


def write_jasc(path, colors):
    with open(path, "w", newline="\r\n") as f:
        f.write(f"JASC-PAL\n0100\n{len(colors)}\n")
        for c in colors:
            f.write("%d %d %d\n" % c)


def pad16(colors):
    return list(colors) + [(0, 0, 0)] * (16 - len(colors))


def write_all():
    painting = build_painting()
    solid_ink = np.full((8, 8), P_INK, int)
    p_tiles, p_map = tileize(painting, PAINT_ROW, first_tile=solid_ink, max_tiles=512)
    save_tilesheet(p_tiles, pad16(PAINT), OUT / "rayquaza.png")
    (OUT / "rayquaza.bin").write_bytes(p_map.astype("<u2").tobytes())

    thread = build_thread()
    t_tiles, t_map = tileize(thread, THREAD_ROW, first_tile=np.zeros((8, 8), int), max_tiles=128)
    save_tilesheet(t_tiles, THREAD, OUT / "clouds.png")
    (OUT / "clouds.bin").write_bytes(t_map.astype("<u2").tobytes())

    logo = build_logo()
    pal256 = [(0, 0, 0)] * 256
    pal256[:len(GOLD)] = GOLD
    pal256[PAINT_ROW * 16:PAINT_ROW * 16 + len(PAINT)] = PAINT
    save_indexed(logo, pal256, OUT / "pokemon_logo.png")
    write_jasc(OUT / "pokemon_logo.pal", pal256)
    write_jasc(OUT / "rayquaza_and_clouds.pal", THREAD)

    save_indexed(build_banner(), pad16(BANNER), OUT / "emerald_version.png")
    save_indexed(build_press_start(), pad16(PRESS_PAL), OUT / "press_start.png")
    print(f"painting: {len(p_tiles)} tiles, thread: {len(t_tiles)} tiles")
    return painting, thread, logo


# --------------------------------------------------------------------------
# Preview: composite the screen the way the GBA does
# --------------------------------------------------------------------------
def rgb5(c):
    return tuple(v >> 3 for v in c)


def blend(a, b, eva, evb):
    return tuple(min(31, (x * eva + y * evb) >> 4) << 3 for x, y in zip(rgb5(a), rgb5(b)))


def composite(painting, thread, logo, t=0, eva=16, evb=0, amp=4, drift=0.25,
              glint=None, show_bgs=True, logo_dy=0, banner_y=BANNER_Y_GOAL,
              press=True):
    """t: frames into the final phase. Returns an RGB array."""
    banner = build_banner()
    ps = build_press_start()
    out = np.zeros((H, W, 3), np.uint8)
    thread_pal = list(THREAD)
    if glint is not None:
        thread_pal[15] = glint
    bg1x = -int(t * drift)
    for y in range(H):
        wave = int(amp * math.sin(2 * math.pi * ((y + t) % 64) / 64))
        for x in range(W):
            c = INK
            if show_bgs:
                c = PAINT[painting[y, x]]
                tx = (x + wave + bg1x) % 256
                ti = thread[y % 256, tx]
                if ti:
                    c = blend(thread_pal[ti], c, eva, evb) if (eva, evb) != (16, 0) else thread_pal[ti]
            lx, ly = x - BG2_X_OFFSET, y + logo_dy
            if 0 <= lx < 256 and 0 <= ly < 64 and logo[ly, lx]:
                c = GOLD[logo[ly, lx]]
            out[y, x] = c
    # sprites: banner
    top = banner_y - 16
    left = BANNER_LEFT_X - 32
    for yy in range(32):
        for xx in range(128):
            v = banner[yy, xx]
            if v and 0 <= top + yy < H and 0 <= left + xx < W:
                out[top + yy, left + xx] = BANNER[v]
    if press:
        for row, cy in ((0, PRESS_Y), (1, FAN_Y)):
            for yy in range(8):
                for xx in range(8, 160):
                    v = ps[row * 8 + yy, xx]
                    sx, sy = xx + START_BANNER_X - 88, cy - 4 + yy
                    if v and 0 <= sx < W and 0 <= sy < H:
                        out[sy, sx] = PRESS_PAL[v]
    return out


def save_preview(arr, name, k=3):
    PREVIEW.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).resize((W * k, H * k), Image.NEAREST).save(PREVIEW / name)


def preview(painting, thread, logo):
    # BLDALPHA(12, 8), as title_screen.c sets it, so the thread glows.
    save_preview(composite(painting, thread, logo, eva=12, evb=8), "final.png")
    save_preview(composite(painting, thread, logo, t=40, eva=12, evb=8,
                           glint=(248, 248, 216)), "final_t40.png")
    save_preview(composite(painting, thread, logo, show_bgs=False, logo_dy=-32,
                           banner_y=-60, press=False), "phase1.png")
    rgb = np.array([PAINT[v] for v in painting.ravel()], np.uint8).reshape(H, W, 3)
    Image.fromarray(rgb).save(PREVIEW / "painting_1x.png")


# --------------------------------------------------------------------------
# In-game capture: boot the built ROM headlessly and screenshot the title
# --------------------------------------------------------------------------
CAPTURE = ROOT / "build/title_capture"
RUNNER = ROOT / "build/tools/ichor-mgba-headless"  # built by tools/ichor/smoke_test.sh
# Review shots for design/phase1/img, by frame (START at 500 skips the intro;
# timing is stable for a given ROM, re-pick if the intro or title changes).
SHOTS = {
    "title_1_glint": 568,   # the first shine crosses ICHOR on black gloss
    "title_2_flash": 640,   # the double shine; the backdrop warms to clay
    "title_3_rise": 862,    # POKEMON slides in as ICHOR rises
    "title_4_final": 1000,  # the amphora: PRESS START blinking
    "title_5_drift": 1500,  # later: the golden thread has drifted on
}
CAPTURE_LUA = """-- Written by tools/ichor/art/title_screen.py --capture
local K = C.GBA_KEY
local OAM_BUF = 0x03006700  -- gMain.oamBuffer (pokeemerald.map: gMain + 0x38)
local FRAMES = {%s}
local want, held, releaseAt, last = {}, nil, 0, 0
for _, f in ipairs(FRAMES) do want[f] = true; if f > last then last = f end end
callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  if f == 500 then emu:addKey(K.START); held = K.START; releaseAt = f + 6 end
  -- Hide the dev-only Quickstart HUD (top right) so shots show the art alone.
  for i = 0, 127 do
    local a0 = emu:read16(OAM_BUF + i * 8)
    local a1 = emu:read16(OAM_BUF + i * 8 + 2)
    local y, x = a0 & 0xFF, a1 & 0x1FF
    if x >= 168 and x < 240 and y < 24 then emu:write16(OAM_BUF + i * 8, (a0 & 0xFF00) | 160) end
  end
  if want[f] then emu:screenshot(string.format("%s/f%%04d.png", f)) end
  if f == last + 1 then console:log("TITLE done") end
end)
"""


def capture(frames, shots=None):
    import shutil
    import subprocess
    assert RUNNER.exists(), "run tools/ichor/smoke_test.sh once to build the headless runner"
    CAPTURE.mkdir(parents=True, exist_ok=True)
    for old in CAPTURE.glob("f*.png"):
        old.unlink()
    lua = CAPTURE / "capture.lua"
    lua.write_text(CAPTURE_LUA % (", ".join(map(str, frames)), CAPTURE))
    subprocess.run([str(RUNNER), "--script", str(lua), "--frames", str(max(frames) + 100),
                    "--until", "TITLE done", str(ROOT / "pokeemerald.gba")],
                   check=True, capture_output=True, cwd=ROOT)
    for name, f in (shots or {}).items():
        shutil.copy(CAPTURE / f"f{f:04d}.png", ROOT / "design/phase1/img" / f"{name}.png")
    print(f"captured {len(frames)} frames in {CAPTURE}")


if __name__ == "__main__":
    layers = write_all()
    if "--preview" in sys.argv:
        preview(*layers)
        print(f"preview in {PREVIEW}")
    if "--capture-all" in sys.argv:   # every 2nd frame of the title, for picking SHOTS
        capture(list(range(520, 1100, 2)) + list(range(1100, 1700, 20)))
    elif "--capture" in sys.argv:     # the review shots, into design/phase1/img
        capture(sorted(SHOTS.values()), SHOTS)
