#!/usr/bin/env python3
"""Draw Ichor's boot sequence: the cards, the studio mark, the frieze and the loom.

The intro is one painted pot turning under the light. A clay band (BG3) stays
put, lit like the title's amphora, while the black-figure frieze (BG2) scrolls
across it, so the figures move under a fixed highlight as a turning pot's do.
The white thread of mortal lives (BG1) and the hero's golden thread (BG0)
scroll with it. See design/phase1/INTRO.md for the scenes and the frame sheet.

Writes:
  graphics/intro/copyright.png/.bin             the copyright card (BG0)
  graphics/expansion_intro/*                    the "powered by" card
  graphics/intro/studio_*                       the studio mark and its sprites
  graphics/intro/clay*, frieze*, thread_*       the frieze scene
  graphics/intro/loom*                          the loom scene
  graphics/intro/sprites_*.png, *.pal           the sprites and palettes
  src/data/intro_ichor_layout.h                 positions intro.c needs

Usage: python3 tools/ichor/art/intro_screen.py [--preview] [--capture]
  --preview   composites key frames like the GBA into build/intro_preview/
  --capture   boots the built ROM headlessly and writes the contact sheets and
              stills into design/phase1/img/intro_*.png (run make first, and
              tools/ichor/smoke_test.sh once to build the runner)
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import intro_cards as CARDS
import intro_figures as F
import intro_lib as L
import title_screen as TS

ROOT = L.ROOT
GFX = ROOT / "graphics/intro"
EXP = ROOT / "graphics/expansion_intro"
LAYOUT_H = ROOT / "src/data/intro_ichor_layout.h"
PREVIEW = ROOT / "build/intro_preview"

W, H = 240, 160

# --------------------------------------------------------------------------
# Screen geometry: the frieze band, framed like the title's panel
# --------------------------------------------------------------------------
TOP_BAND_Y = 22          # 13 rows: clay, 2x meander, clay, ink rule
PANEL_Y0 = TOP_BAND_Y + 13
GROUND_Y = 130           # feet stand on this row
BOTTOM_BAND_Y = 131      # ink ground line, clay, 2x meander, clay
FOOT_Y = BOTTOM_BAND_Y + 13

FRIEZE_W = 1464
CAM_END = FRIEZE_W - W   # the pan stops with Olympus in frame

# --------------------------------------------------------------------------
# Palettes
# --------------------------------------------------------------------------
# BG palette rows (both painted scenes)
PAL_PAINT, PAL_CLAY, PAL_WHITE, PAL_GOLD = 0, 1, 2, 3
PAINT_PAL = [L.INK, L.INK, L.WHITE, L.RED]                       # BG2; color 0 is the backdrop
CLAY_PAL = [L.BLACK] + L.CLAY_RAMP + [L.INK]                      # BG3
WHITE_PAL = [L.BLACK, L.WHITE, L.CLAY_HI]                         # BG1
GOLD_PAL = [L.BLACK, L.THREAD_UNDER, L.THREAD_BODY, L.THREAD_BRIGHT] + [L.BLACK] * 11 + [L.GOLD_GLINT]
GOLD_GLINT = 15                                                  # intro.c pulses it

# OBJ palettes
OBJ_FIGURE = [L.BLACK, L.INK, L.WHITE, L.RED]                    # black-figure sprites
OBJ_GOLD = [L.BLACK, L.GOLD_DEEP, L.GOLD_SHADOW, L.GOLD_MID, L.GOLD_LIT, L.GOLD_GLINT, (248, 248, 232)]


# --------------------------------------------------------------------------
# The clay band (BG3): static, lit like the amphora's belly
# --------------------------------------------------------------------------
LIGHT_KEYS = [(0, 0.7), (12, 1.0), (28, 2.0), (52, 2.0), (66, 3.0), (84, 3.0), (100, 2.0), (196, 2.0),
              (214, 1.0), (239, 0.7)]


def clay_level(x):
    for (xa, a), (xb, b) in zip(LIGHT_KEYS, LIGHT_KEYS[1:]):
        if xa <= x <= xb:
            return a + (b - a) * (x - xa) / (xb - xa)
    return LIGHT_KEYS[-1][1]


def clay_at(x, y, bright=0.0):
    lv = clay_level(x) + bright
    base = int(math.floor(lv))
    if lv - base > L.BAYER[y % 4][x % 4]:
        base += 1
    return 1 + min(4, max(0, base))       # CLAY_PAL indices 1..5


def build_clay():
    img = np.zeros((H, W), int)
    for y in range(TOP_BAND_Y, FOOT_Y):
        for x in range(W):
            img[y, x] = clay_at(x, y)
    for x in range(W):
        img[TOP_BAND_Y + 12, x] = 6        # ink rule under the top band
        img[BOTTOM_BAND_Y, x] = 6          # the ground line
    return img


# --------------------------------------------------------------------------
# The frieze (BG2), the threads (BG1, BG0) and the sprite anchors
# --------------------------------------------------------------------------
def meander_bands(img):
    w = img.shape[1]
    for x in range(w):
        for r in range(10):
            if TS.meander_row(r, x + 4):
                img[TOP_BAND_Y + 1 + r, x] = F.K
                img[BOTTOM_BAND_Y + 2 + r, x] = F.K


def put(img, arr, x, y):
    F.stamp(img, arr, x, y)


def on_ground(arr, x, img, ground=GROUND_Y):
    put(img, arr, x, ground - arr.shape[0] + 1)


def put_label(img, text, x, y):
    put(img, F.label(text), x, y)


class Frieze:
    def __init__(self):
        self.img = np.zeros((H, FRIEZE_W), int)
        self.white = np.zeros((H, FRIEZE_W), int)
        self.gold = np.zeros((H, FRIEZE_W), int)
        self.pos = {}
        self.build()

    def build(self):
        img = self.img
        meander_bands(img)
        # --- Clotho spinning, her wool basket behind her
        on_ground(F.grid_arr(F.KALATHOS), 6, img)
        cl = F.clotho_static()
        cx, cy = 26, GROUND_Y - cl.shape[0] + 1
        put(img, cl, cx, cy)
        put_label(img, "ΚΛΩΘΩ", 12, cy - 9)
        hx, hy = cx + F.CLOTHO_HAND[0], cy + F.CLOTHO_HAND[1]
        self.pos["CLOTHO_HAND"] = (hx, hy)
        self.pos["SPINDLE"] = (cx + F.SPINDLE_ORIGIN[0], cy + F.SPINDLE_ORIGIN[1])

        # --- the olive grove of Elaia, where the golden thread begins
        tree_a = F.olive_tree(1, lean=-0.4)
        tree_b, boughs_b = F.olive_tree(2, lean=0.3, with_boughs=True)
        tree_c = F.olive_tree(5, lean=0.6)
        ta, tb, tc = 112, 228, 344
        on_ground(tree_a, ta, img)
        on_ground(tree_b, tb, img)
        on_ground(tree_c, tc, img)
        on_ground(F.mareep(), 172, img)
        on_ground(F.flip_arr(F.mareep()), 296, img)
        # Athena's owl on tree B's highest bough
        bx, by = min(boughs_b, key=lambda p: p[1])
        tb_y = GROUND_Y - tree_b.shape[0] + 1
        owl = F.grid_arr(F.NOCTOWL)
        put(img, owl, int(tb + bx) - owl.shape[1] // 2, int(tb_y + by) - owl.shape[0] - 4)
        put_label(img, "ΕΛΑΙΑ", 190, PANEL_Y0 + 4)
        # the hero's thread rises from the roots of the third olive
        self.pos["GOLD_ORIGIN"] = (tc + 40, GROUND_Y - 1)

        # --- the sea: a rocky shore, the trireme, the ketos and the waves
        sea_x0, sea_x1 = 420, 852
        ship = F.trireme()
        put(img, ship, 470, 118 - 60)
        ket = F.ketos()
        put(img, ket, 690, 118 - (ket.shape[0] - 8))
        sea = F.sea_band(sea_x1 - sea_x0)
        put(img, sea, sea_x0, GROUND_Y - sea.shape[0] + 1)
        for x, seed in ((sea_x0 - 16, 9), (sea_x1 - 12, 4)):
            on_ground(F.rocks(30, 17, seed), x, img)
        self.pos["FINIZEN_A"] = (606, 114, 648, 28)   # leap from x0 to x1 at the waterline, height
        self.pos["FINIZEN_B"] = (798, 114, 838, 24)
        put_label(img, "ΘΑΛΑΣΣΑ", 560, PANEL_Y0 + 4)

        # --- the temple of the Twelve, its altar fire, and Xatu on the roof
        tpl = F.temple()
        tx = 880
        on_ground(tpl, tx, img)
        t_top = GROUND_Y - tpl.shape[0] + 1
        xatu = F.grid_arr(F.XATU)
        put(img, xatu, tx + tpl.shape[1] - 14, t_top + 13 - xatu.shape[0] + 2)
        altar = F.grid_arr(F.TRIPOD_FIRE)
        ax = tx + tpl.shape[1] + 14
        on_ground(altar, ax, img)
        self.pos["FLAME"] = (ax - 1, GROUND_Y - altar.shape[0] - 15)
        put_label(img, "ΝΑΟΣ", tx + 80, PANEL_Y0 + 2)

        # --- cypresses on the road up, then Olympus in the clouds
        on_ground(F.cypress(52, 3), 1150, img)
        on_ground(F.cypress(60, 4), 1172, img)
        on_ground(F.cypress(46, 5), 1196, img)
        oly = F.olympus()
        ox = 1234
        on_ground(oly, ox, img)
        zap = F.zapdos()
        zx, zy = 1262, PANEL_Y0 + 2
        put(img, zap, zx, zy)
        self.pos["ZAPDOS"] = (zx, zy)
        self.pos["BOLTS"] = [(zx + 50, zy + 22), (zx + 4, zy + 30), (zx + 64, zy + 4)]
        put_label(img, "ΟΛΥΜΠΟΣ", 1392, PANEL_Y0 + 4)

        # --- the threads
        self.draw_white_thread(hx, hy)
        self.draw_gold_thread(*self.pos["GOLD_ORIGIN"])

    def draw_white_thread(self, hx, hy):
        """One added-white thread from Clotho's hand to the end of the frieze,
        sagging and rising gently."""
        prev = hy
        for x in range(hx, FRIEZE_W):
            y = int(round(hy + 2.5 * math.sin(2 * math.pi * (x - hx) / 192 - 0.0)))
            lo, hi = min(prev, y), max(prev, y)
            for yy in range(lo, hi + 1):
                self.white[yy, x] = 1
            prev = y

    def gold_y(self, x):
        return 95 + 3.0 * math.sin(2 * math.pi * x / 128)

    def draw_gold_thread(self, ox, oy):
        """The hero's thread: it rises from the olive's roots, unspun, and runs on
        above the white one. A 2 px cord like the title's (core, body, lip),
        with glints in the pulsing color."""
        g = self.gold
        rise_x1 = ox + 24
        y1 = self.gold_y(rise_x1)
        # the rise: a curve from the root up to the running height
        for i in range(0, 41):
            t = i / 40
            x = ox + (rise_x1 - ox) * (1 - (1 - t) ** 2)
            y = oy + (y1 - oy) * t
            xi, yi = int(round(x)), int(round(y))
            g[yi, xi] = 3
            if g[yi, xi + 1] == 0:
                g[yi, xi + 1] = 2
        for x in range(rise_x1, FRIEZE_W):
            y = self.gold_y(x)
            yc = int(round(y))
            g[yc, x] = GOLD_GLINT if (x % 32) in (5, 6, 21) else 3
            g[yc + 1, x] = 2
            frac = y - yc
            if abs(frac) > 0.3:
                ny = yc - 1 if frac < 0 else yc + 2
                if g[ny, x] == 0:
                    g[ny, x] = 1
        g[oy, ox] = GOLD_GLINT


F.flip_arr = lambda a: a[:, ::-1].copy()


# --------------------------------------------------------------------------
# The loom (BG2 painting, BG0 gold thread) and its sprites
# --------------------------------------------------------------------------
LOOM_THREADS_X = [48, 72, 96, 120, 144, 168, 192]
LOOM_GOLD = 3                         # index of the golden thread
LOOM_KNOT_Y = [76, 96, 68, 0, 88, 104, 80]
LOOM_CUT = [6, 5, 4]                  # Atropos cuts these, right to left, then reaches the gold
BEAM_Y = 40
CLOTH_Y0, CLOTH_Y1 = 48, 58           # the woven band under the beam
WEIGHT_TOP = 113
GOLD_END_Y = 110
SEG_W, SEG_H = 32, 64                 # sprite for a thread's lower part and its weight


def build_loom():
    """The warp-weighted loom of the Fates: two posts and a beam, a band of
    woven cloth, and the warp hanging in front of it, each thread pulled taut
    by a clay weight. The golden thread hangs among them with no weight."""
    img = np.zeros((H, W), int)
    meander_bands(img)
    # posts
    for x0 in (20, 214):
        for y in range(BEAM_Y - 2, GROUND_Y + 1):
            for x in range(x0, x0 + 6):
                img[y, x] = F.K
        for y in range(BEAM_Y + 12, GROUND_Y - 4, 9):
            img[y, x0 + 2] = 0
            img[y + 1, x0 + 3] = 0
    # beam with a red band and incised grain, ends past the posts
    for y in range(BEAM_Y, BEAM_Y + 8):
        for x in range(12, 229):
            img[y, x] = F.K
    for x in range(14, 227):
        img[BEAM_Y + 3, x] = F.R
    for x in range(16, 226, 6):
        img[BEAM_Y + 1, x] = 0
        img[BEAM_Y + 6, x + 3] = 0
    # the woven band: a meander in added white on black, red edges
    for y in range(CLOTH_Y0, CLOTH_Y1 + 1):
        for x in range(36, 205):
            img[y, x] = F.K
    for x in range(36, 205):
        img[CLOTH_Y0 + 1, x] = F.R
        img[CLOTH_Y1 - 1, x] = F.R
        for r in range(5):
            if CARDS.MEANDER[r][(x - 36) % 8] == "#":
                img[CLOTH_Y0 + 3 + r, x] = F.Wt
    # fringe below the cloth
    for x in range(36, 205, 2):
        img[CLOTH_Y1 + 1, x] = F.K
    # the white warp threads and their weights; the cut ones stop at the knot
    weight = F.rim(F.pad(F.grid_arr(F.LOOM_WEIGHT), 1, 1, 0, 0)) if False else F.grid_arr(F.LOOM_WEIGHT)
    for i, x in enumerate(LOOM_THREADS_X):
        if i == LOOM_GOLD:
            continue
        y_end = LOOM_KNOT_Y[i] - 1 if i in LOOM_CUT else WEIGHT_TOP
        for y in range(CLOTH_Y1 + 2, y_end + 1):
            img[y, x] = F.Wt
        if i not in LOOM_CUT:
            put(img, weight, x - 3, WEIGHT_TOP)
    put_label(img, "ΛΑΧΕΣΙΣ", 28, GROUND_Y - 6)
    put_label(img, "ΑΤΡΟΠΟΣ", 176, GROUND_Y - 6)
    return img


def build_loom_gold():
    """The golden warp thread: from the beam down past the cloth (it is not
    woven in), loose at the end, a few strands frayed apart. intro.c sways it
    with a per-scanline offset that grows toward its free end."""
    g = np.zeros((H, W), int)
    x = LOOM_THREADS_X[LOOM_GOLD]
    for y in range(BEAM_Y + 8, GOLD_END_Y):
        g[y, x] = GOLD_GLINT if y % 23 in (3, 4) else 3
        g[y, x + 1] = 2
    for k, (dx, ln) in enumerate(((-2, 5), (0, 7), (2, 5), (1, 4))):
        for j in range(ln):
            yy = GOLD_END_Y + j
            xx = x + int(round(dx * j / ln))
            g[yy, xx] = 2 if j < ln - 2 else 1
    return g


def loom_segment(i):
    """32x64 sprite: thread i from its knot down, with its weight."""
    f = np.zeros((SEG_H, SEG_W), int)
    top = LOOM_KNOT_Y[i]
    cx = 16
    for y in range(0, WEIGHT_TOP - top):
        f[y, cx] = F.Wt
    wgt = F.grid_arr(F.LOOM_WEIGHT)
    F.stamp(f, wgt, cx - 3, WEIGHT_TOP - top)
    return f


def sparkle_frames():
    """16x16 gold twinkle: a point, a small star, a large star, a small star."""
    frames = []
    for size in (1, 3, 5, 3):
        f = np.zeros((16, 16), int)
        c = 7
        for d in range(-size, size + 1):
            v = 6 if abs(d) <= 1 else (5 if abs(d) <= 3 else 4)
            f[c + d, c] = max(f[c + d, c], v)
            f[c, c + d] = max(f[c, c + d], v)
        if size >= 3:
            for d in (-1, 1):
                f[c + d, c + d] = 4
                f[c + d, c - d] = 4
        frames.append(f)
    return frames


# --------------------------------------------------------------------------
# Writing files
# --------------------------------------------------------------------------
def long_maps(layers):
    """layers: [(img, tileset, pal_row)] each H x FRIEZE_W. Returns their
    column-major tilemaps (cols, 20) so intro.c can stream a column at once."""
    out = []
    for img, ts, pal in layers:
        m = L.tilemap(img, ts, pal)          # (20, cols)
        out.append(np.ascontiguousarray(m.T))
    return out


def write_pal(name, colors):
    L.write_jasc(GFX / f"{name}.pal", L.pad16(colors))


def write_sprites(name, frames, w, h, palette):
    sheet = L.sprite_sheet(frames, w, h)
    L.save_indexed(sheet, L.pad16(palette), GFX / f"{name}.png")


def write_cards():
    cp = CARDS.build_copyright()
    ts = L.TileSet(np.zeros((8, 8), int), allow_flip=True)
    m = L.tilemap(cp, ts, 0)
    assert len(ts) < 0x3800 // 32
    L.save_tiles(ts.tiles, L.pad16(CARDS.COPYRIGHT_PAL), GFX / "copyright.png")
    L.write_map(GFX / "copyright.bin", L.map_to_screen(m))

    bg3, bg2 = CARDS.build_powered_by()
    ts3 = L.TileSet(np.zeros((8, 8), int))
    m3 = L.tilemap(bg3, ts3, 0)
    L.save_tiles(ts3.tiles, L.pad16(CARDS.POWERED_PAL), EXP / "powered_by.png")
    L.write_map(EXP / "powered_by.bin", L.map_to_screen(m3))
    ts2 = L.TileSet(np.zeros((8, 8), int))
    m2 = L.tilemap(bg2, ts2, 0)
    pal256 = list(CARDS.POWERED_PAL) + [L.BLACK] * (256 - len(CARDS.POWERED_PAL))
    L.save_tiles(ts2.tiles, pal256, EXP / "rhh_credits.png")
    # 8bpp tiles: the tilemap entries carry no palette bits
    L.write_map(EXP / "rhh_credits.bin", L.map_to_screen(m2 & 0x0FFF))
    L.write_jasc(EXP / "credits.pal", pal256)

    st = CARDS.build_studio()
    tss = L.TileSet(np.zeros((8, 8), int))
    ms = L.tilemap(st, tss, 0)
    L.save_tiles(tss.tiles, L.pad16(CARDS.STUDIO_PAL), GFX / "studio_mark.png")
    L.write_map(GFX / "studio_mark.bin", L.map_to_screen(ms))
    write_pal("studio_mark", CARDS.STUDIO_PAL)
    write_sprites("studio_drop", CARDS.build_drop_frames(), 16, 32, CARDS.STUDIO_OBJ_PAL)
    write_sprites("studio_ripple", CARDS.build_ripple_frames(), 64, 64, CARDS.STUDIO_OBJ_PAL)
    write_pal("studio_obj", CARDS.STUDIO_OBJ_PAL)
    return {"copyright": len(ts), "powered_bg3": len(ts3), "powered_bg2": len(ts2), "studio": len(tss)}


def write_frieze(fz):
    clay = build_clay()
    paint_ts = L.TileSet(np.zeros((8, 8), int))
    aux_ts = L.TileSet(np.zeros((8, 8), int))
    m_paint, m_white, m_gold = long_maps([(fz.img, paint_ts, PAL_PAINT), (fz.white, aux_ts, PAL_WHITE),
                                          (fz.gold, aux_ts, PAL_GOLD)])
    m_clay = L.tilemap(clay, aux_ts, PAL_CLAY)
    assert len(paint_ts) <= 1024, f"frieze: {len(paint_ts)} tiles > 1024"
    assert len(aux_ts) <= 512, f"frieze aux: {len(aux_ts)} tiles > 512"
    L.save_tiles(paint_ts.tiles, L.pad16(PAINT_PAL), GFX / "frieze.png")
    L.save_tiles(aux_ts.tiles, L.pad16(CLAY_PAL), GFX / "frieze_aux.png")
    L.write_map(GFX / "frieze.bin", m_paint)
    L.write_map(GFX / "frieze_white.bin", m_white)
    L.write_map(GFX / "frieze_gold.bin", m_gold)
    L.write_map(GFX / "clay.bin", L.map_to_screen(m_clay))
    write_pal("paint", PAINT_PAL)
    write_pal("clay", CLAY_PAL)
    write_pal("thread_white", WHITE_PAL)
    write_pal("thread_gold", GOLD_PAL)
    write_pal("obj_figure", OBJ_FIGURE)
    write_pal("obj_gold", OBJ_GOLD)
    write_sprites("sprites_spindle", F.spindle_frames(), 8, 16, OBJ_FIGURE)
    write_sprites("sprites_finizen", F.finizen_frames(), 32, 16, OBJ_FIGURE)
    write_sprites("sprites_flame", F.flame_frames(), 16, 16, OBJ_FIGURE)
    write_sprites("sprites_bolt", F.bolt_frames(), 16, 32, OBJ_FIGURE)
    write_sprites("sprites_sparkle", sparkle_frames(), 16, 16, OBJ_GOLD)
    return {"frieze": len(paint_ts), "frieze_aux": len(aux_ts)}, clay


def write_loom():
    loom = build_loom()
    gold = build_loom_gold()
    clay = build_clay()
    paint_ts = L.TileSet(np.zeros((8, 8), int))
    aux_ts = L.TileSet(np.zeros((8, 8), int))
    m_paint = L.tilemap(loom, paint_ts, PAL_PAINT)
    m_gold = L.tilemap(gold, aux_ts, PAL_GOLD)
    m_clay = L.tilemap(clay, aux_ts, PAL_CLAY)
    assert len(paint_ts) <= 1024 and len(aux_ts) <= 512
    L.save_tiles(paint_ts.tiles, L.pad16(PAINT_PAL), GFX / "loom.png")
    L.save_tiles(aux_ts.tiles, L.pad16(CLAY_PAL), GFX / "loom_aux.png")
    L.write_map(GFX / "loom.bin", L.map_to_screen(m_paint))
    L.write_map(GFX / "loom_gold.bin", L.map_to_screen(m_gold))
    L.write_map(GFX / "loom_clay.bin", L.map_to_screen(m_clay))
    write_sprites("sprites_segments", [loom_segment(i) for i in LOOM_CUT], SEG_W, SEG_H, OBJ_FIGURE)
    rod = F.grid_arr(F.ROD)
    rod_img = np.zeros((64, 8), int)
    F.stamp(rod_img, rod, 1, 64 - rod.shape[0])
    write_sprites("sprites_rod", [rod_img], 8, 64, OBJ_FIGURE)
    write_sprites("sprites_rod_hand", [F.rod_hand()], 16, 16, OBJ_FIGURE)
    write_sprites("sprites_shears", F.shears_frames(), 64, 32, OBJ_FIGURE)
    write_sprites("sprites_arm", F.arm_frames(), 64, 32, OBJ_FIGURE)
    write_sprites("sprites_knot", [F.knot()], 8, 8, OBJ_FIGURE)
    return {"loom": len(paint_ts), "loom_aux": len(aux_ts)}, loom, gold


def write_layout(fz):
    p = fz.pos
    lines = [
        "// Generated by tools/ichor/art/intro_screen.py: positions in the intro's art.",
        "// Frieze coordinates: x along the frieze (0 at its left end), y on screen.",
        "#ifndef GUARD_INTRO_ICHOR_LAYOUT_H",
        "#define GUARD_INTRO_ICHOR_LAYOUT_H",
        "",
        f"#define FRIEZE_WIDTH          {FRIEZE_W}",
        f"#define FRIEZE_COLS           {FRIEZE_W // 8}",
        f"#define FRIEZE_CAM_END        {CAM_END}",
        f"#define FRIEZE_HAND_X         {p['CLOTHO_HAND'][0]}",
        f"#define FRIEZE_HAND_Y         {p['CLOTHO_HAND'][1]}",
        f"#define FRIEZE_SPINDLE_X      {p['SPINDLE'][0]}",
        f"#define FRIEZE_SPINDLE_Y      {p['SPINDLE'][1]}",
        f"#define FRIEZE_GOLD_X         {p['GOLD_ORIGIN'][0]}",
        f"#define FRIEZE_GOLD_Y         {p['GOLD_ORIGIN'][1]}",
        f"#define FRIEZE_FLAME_X        {p['FLAME'][0]}",
        f"#define FRIEZE_FLAME_Y        {p['FLAME'][1]}",
        "// Finizen leaps: x0, waterline y, x1, height",
        "#define FRIEZE_FINIZEN_A      {%d, %d, %d, %d}" % p["FINIZEN_A"],
        "#define FRIEZE_FINIZEN_B      {%d, %d, %d, %d}" % p["FINIZEN_B"],
        "// lightning around Zapdos: top-left of each 16x32 bolt",
        "#define FRIEZE_BOLTS          {" + ", ".join("{%d, %d}" % b for b in p["BOLTS"]) + "}",
        f"#define FRIEZE_GOLD_GLINT     {GOLD_GLINT}",
        "",
        "// The loom",
        "#define LOOM_THREAD_X         {" + ", ".join(map(str, LOOM_THREADS_X)) + "}",
        "#define LOOM_KNOT_Y           {" + ", ".join(map(str, LOOM_KNOT_Y)) + "}",
        "#define LOOM_CUT              {" + ", ".join(map(str, LOOM_CUT)) + "}",
        f"#define LOOM_GOLD             {LOOM_GOLD}",
        f"#define LOOM_BEAM_BOTTOM      {BEAM_Y + 8}",
        f"#define LOOM_GOLD_END_Y       {GOLD_END_Y}",
        f"#define LOOM_WEIGHT_TOP       {WEIGHT_TOP}",
        f"#define LOOM_SHEARS_CUT_X     {F.SHEARS_CUT[0]}",
        f"#define LOOM_SHEARS_CUT_Y     {F.SHEARS_CUT[1]}",
        "",
        "#endif // GUARD_INTRO_ICHOR_LAYOUT_H",
        "",
    ]
    LAYOUT_H.write_text("\n".join(lines))


def write_all():
    GFX.mkdir(parents=True, exist_ok=True)
    counts = write_cards()
    fz = Frieze()
    c, clay = write_frieze(fz)
    counts.update(c)
    c, loom, lgold = write_loom()
    counts.update(c)
    write_layout(fz)
    print("tiles:", ", ".join(f"{k} {v}" for k, v in counts.items()))
    return fz, clay, loom, lgold


# --------------------------------------------------------------------------
# Preview: composite frames the way the GBA layers them
# --------------------------------------------------------------------------
def blend(a, b, eva, evb):
    a5, b5 = np.asarray(a, int) >> 3, np.asarray(b, int) >> 3
    return np.minimum(31, (a5 * eva + b5 * evb) >> 4) << 3


def frieze_frame(fz, clay, cam, white_to=W, gold_to=W, show_gold=True):
    out = L.rgb(clay, CLAY_PAL)
    out[clay == 0] = L.INK
    seg = fz.img[:, cam:cam + W]
    pal = np.array(PAINT_PAL, np.uint8)
    m = seg > 0
    out[m] = pal[seg[m]]
    wseg = fz.white[:, cam:cam + W].copy()
    wseg[:, white_to:] = 0
    m = wseg > 0
    out[m] = np.array(WHITE_PAL, np.uint8)[wseg[m]]
    if show_gold:
        gseg = fz.gold[:, cam:cam + W].copy()
        gseg[:, gold_to:] = 0
        m = gseg > 0
        gp = np.array(GOLD_PAL, np.uint8)[gseg[m]]
        out[m] = blend(gp, out[m], 12, 8)
    return out


def preview(fz, clay, loom, lgold):
    PREVIEW.mkdir(parents=True, exist_ok=True)
    shots = []
    hx = fz.pos["CLOTHO_HAND"][0]
    shots.append(frieze_frame(fz, clay, 0, white_to=hx + 90, show_gold=False))
    for cam in range(0, CAM_END + 1, 120):
        shots.append(frieze_frame(fz, clay, cam))
    shots.append(frieze_frame(fz, clay, CAM_END))
    lo = L.rgb(clay, CLAY_PAL)
    lo[clay == 0] = L.INK
    m = loom > 0
    lo[m] = np.array(PAINT_PAL, np.uint8)[loom[m]]
    m = lgold > 0
    lo[m] = blend(np.array(GOLD_PAL, np.uint8)[lgold[m]], lo[m], 12, 8)
    shots.append(lo)
    for i, s in enumerate(shots):
        L.upscale(s, 3).save(PREVIEW / f"f{i:02d}.png")
    contact(shots, PREVIEW / "sheet.png", cols=4)
    strip = np.zeros((H, FRIEZE_W, 3), np.uint8)
    for cam in range(0, FRIEZE_W, W):
        w = min(W, FRIEZE_W - cam)
        strip[:, cam:cam + w] = frieze_frame(fz, clay, min(cam, CAM_END))[:, (cam - min(cam, CAM_END)):][:, :w]
    Image.fromarray(strip).save(PREVIEW / "frieze_strip.png")
    print(f"preview in {PREVIEW}")


def contact(frames, path, cols=4, labels=None, k=1):
    rows = (len(frames) + cols - 1) // cols
    lab = 12 if labels else 0
    sheet = Image.new("RGB", (cols * W * k + (cols + 1) * 4, rows * (H * k + lab) + (rows + 1) * 4), (24, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(frames):
        x = 4 + (i % cols) * (W * k + 4)
        y = 4 + (i // cols) * (H * k + lab + 4)
        im = Image.fromarray(np.asarray(f, np.uint8)) if not isinstance(f, Image.Image) else f
        im = im.convert("RGB").resize((W * k, H * k), Image.NEAREST)
        sheet.paste(im, (x, y + lab))
        if labels:
            d.text((x + 1, y), labels[i], fill=(232, 216, 176))
    sheet.save(path)


# --------------------------------------------------------------------------
# In-game capture
# --------------------------------------------------------------------------
RUNNER = ROOT / "build/tools/ichor-mgba-headless"
CAPTURE = ROOT / "build/intro_capture"
IMG = ROOT / "design/phase1/img"


def capture():
    import intro_capture
    intro_capture.capture()


if __name__ == "__main__":
    layers = write_all()
    if "--preview" in sys.argv:
        preview(*layers)
    if "--capture" in sys.argv:
        capture()
