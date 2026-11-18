"""Ichor's Poke Balls: the in-battle ball sprites (graphics/balls) and the
24x24 bag icons, themed on the figure each ball is named for.

Usage:
    /usr/bin/python3 tools/ichor/art/balls.py [--write] [--check] [--preview DIR]

--write    writes graphics/balls/<ball>.png (three 16x16 frames and the
           ball's palette) and graphics/balls/open.png. The icons are written
           by items.py, which registers them from here (items.py --write).
--check    checks the battle sprites on disk match what this file draws
--preview  writes DIR/balls_sheet.png: every ball's icon and its three battle
           frames at 1x and 4x, with the old art beside it

Every ball keeps the Gen 3 silhouette, so the throw, the wobble and the
open-and-close still read: a sphere split at the equator by a band, a boss
where the two halves meet. The theme lives in the colors and in one mark on
the cap: Poseidon's trident, Daedalus's labyrinth key, Selene's crescent.
The plain Poke Ball keeps its name (TERMS.md) and its red-over-white look,
in terracotta and marble with a black-glaze band.

All the ball sprites share one palette layout, because the engine copies
graphics/balls/open.png (the lid tipped back, seen from inside) over frame 3
of the classic balls at load time (LoadBallGfx in src/pokeball.c): that
frame takes its colors from each ball's own palette by index.

  index  1-4 cap ramp, dark to highlight    9-10 band, dark and light
         5-6 base, light and mid             11-12 the mark, dark and light
         7   ink outline                     13   the boss
         8   the dark inside the ball        14   a third mark color
                                             15   base, dark

Light comes from the top left. Colors are multiples of 8 (GBA-exact).
"""
from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from items_lib import ROOT, Icon, centred, save_indexed, to_rgb, upscale  # noqa: E402

BALLS_DIR = os.path.join(ROOT, "graphics/balls")
BASE_REV = "abc930a004"     # main when this file was written: the "before" art

INK = (32, 24, 24)
INSIDE = (56, 40, 48)
MARBLE = [(168, 160, 152), (208, 200, 184), (248, 248, 240)]
BRONZE = [(152, 96, 40), (232, 176, 72)]
GOLD = [(200, 144, 40), (248, 216, 104)]
SILVER = [(120, 128, 144), (200, 208, 216)]
BOSS_GOLD = (248, 224, 136)
BOSS_MARBLE = (248, 248, 240)

# --------------------------------------------------------------------------
# The battle frames. Letters are palette roles; the motif rows overlay the
# closed frame's cap (rows 3-7) and, one row lower, the opening frame's.
# --------------------------------------------------------------------------
ROLE_INDEX = {"1": 1, "2": 2, "3": 3, "4": 4, "w": 5, "b": 6, "K": 7, "i": 8,
              "n": 9, "N": 10, "m": 11, "M": 12, "o": 13, "x": 14, "B": 15}

FRAME_CLOSED = [
    "................",
    "................",
    "......KKKK......",
    "....KK3322KK....",
    "...K34433221K...",
    "...K34333221K...",
    "..K3333322211K..",
    "..K3332KK2211K..",
    "..KNNNKooKnnnK..",
    "..KwwwwKKwwbbK..",
    "...KwwwwwbbbK...",
    "...KwwwbbbbBK...",
    "....KKbbbBKK....",
    "......KKKK......",
    "................",
    "................",
]

# The lid lifts one pixel and the dark inside shows between the halves.
FRAME_OPENING = [
    "................",
    "................",
    "................",
    "......KKKK......",
    "....KK3322KK....",
    "...K34433221K...",
    "...K34333221K...",
    "..K3333322211K..",
    "..K3332KK2211K..",
    "..KNNNKooKnnnK..",
    "...KniiiiiinK...",
    "..KwiiiiiiiibK..",
    "...KwwiiiiwbK...",
    "...KwwwwbbbBK...",
    "....KKbbbBKK....",
    "......KKKK......",
]

# The lid tipped right back: its inside above, the open bowl below. This is
# also graphics/balls/open.png.
FRAME_OPEN = [
    "......KKKK......",
    "....KK3333KK....",
    "...K33222233K...",
    "...K21111112K...",
    "..K2111111112K..",
    "..K2111111111K..",
    "..K3211111121K..",
    "...K33211233K...",
    "....KKNNnnKK....",
    "...KniiiiiinK...",
    "..KwiiiiiiiibK..",
    "..KwiiiiiiiibK..",
    "...KwwiiiiwbK...",
    "...KwwwwbbbBK...",
    "....KKbbbBKK....",
    "......KKKK......",
]

# --------------------------------------------------------------------------
# The balls. cap: 4 colors, dark to highlight; base: 3, dark to light; band:
# dark, light; mark: m, M (and x). The marks themselves (motif16 on the
# battle sprite, motif24 on the icon) are drawn in ball_motifs.py.
# --------------------------------------------------------------------------
BALLS = []


def ball(key, item, name, cap, mark, base=MARBLE, band=BRONZE, boss=BOSS_GOLD, x=None,
         motif16=(), motif24=(), note=""):
    BALLS.append(dict(key=key, item=item, name=name, cap=cap, mark=mark, base=base,
                      band=band, boss=boss, x=x or mark[0], motif16=dict(motif16),
                      motif24=dict(motif24), note=note))


def battle_palette(b):
    c = b["cap"]
    cols = [(0, 0, 0)] * 16
    cols[0] = (112, 192, 160)
    cols[1:5] = c
    cols[5] = b["base"][2]
    cols[6] = b["base"][1]
    cols[7] = INK
    cols[8] = INSIDE
    cols[9], cols[10] = b["band"]
    cols[11], cols[12] = b["mark"]
    cols[13] = b["boss"]
    cols[14] = b["x"]
    cols[15] = b["base"][0]
    for col in cols:
        assert all(v % 8 == 0 and 0 <= v <= 248 for v in col), (b["key"], col)
    return cols


def frame_array(rows):
    a = np.zeros((16, 16), np.int32)
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x_, ch in enumerate(row):
            if ch != ".":
                a[y, x_] = ROLE_INDEX[ch]
    return a


CAP_INDICES = (1, 2, 3, 4)


def overlay(a, motif, dy):
    """Paint the mark {(x, y): role} dy rows down, on cap pixels only, so a
    mark can never eat the outline, the band or the boss."""
    for (x_, y_), ch in motif.items():
        if a[y_ + dy, x_] in CAP_INDICES:
            a[y_ + dy, x_] = ROLE_INDEX[ch]


def battle_frames(b):
    f0 = frame_array(FRAME_CLOSED)
    overlay(f0, b["motif16"], 0)
    f1 = frame_array(FRAME_OPENING)
    overlay(f1, b["motif16"], 1)
    f2 = frame_array(FRAME_OPEN)
    return np.vstack([f0, f1, f2])


# --------------------------------------------------------------------------
# Icons (24x24), registered into items.py
# --------------------------------------------------------------------------
ICON_ROLES = "K c1 c2 c3 c4 b1 b2 b3 n N o m M x"
ICON_CX = ICON_CY = 12.0
ICON_R = 9.5


def draw_icon(b):
    ic = Icon(ICON_ROLES)
    ball_m = ic.ellipse(ICON_CX, ICON_CY, ICON_R, ICON_R)
    y, x = np.mgrid[0:24, 0:24]
    cap = ball_m & (y <= 10)
    band = ball_m & (y >= 11) & (y <= 12)
    base = ball_m & (y >= 13)
    ic.shade(cap, ["c1", "c2", "c3", "c4"], center=(ICON_CX, ICON_CY), radius=(ICON_R, ICON_R),
             cuts=[0.42, 0.78, 0.97])
    ic.shade(base, ["b1", "b2", "b3"], center=(ICON_CX, ICON_CY), radius=(ICON_R, ICON_R),
             cuts=[0.3, 0.62], bias=0.25)
    ic.fill(band & (x <= 9), "N")
    ic.fill(band & (x >= 10), "n")
    ic.fill(band & (y == 11) & (x <= 6), "N")
    ic.outline(ball_m)
    # the boss: a ring of ink round a metal stud, lit at its top left
    ic.patch(9, 9, [
        ".KKKK.",
        "KooooK",
        "KoNooK",
        "KooooK",
        "KooooK",
        ".KKKK.",
    ], {"o": "o", "N": "c4"})
    cap_idx = {ic.idx[r] for r in ("c1", "c2", "c3", "c4")}
    for (x_, y_), ch in b["motif24"].items():
        if ic.a[y_, x_] in cap_idx:
            ic.px(x_, y_, {"1": "c1", "2": "c2", "3": "c3", "4": "c4"}.get(ch, ch))
    return ic


def icon_colors(b):
    c = b["cap"]
    return dict(K=INK, c1=c[0], c2=c[1], c3=c[2], c4=c[3], b1=b["base"][0], b2=b["base"][1],
                b3=b["base"][2], n=b["band"][0], N=b["band"][1], o=b["boss"],
                m=b["mark"][0], M=b["mark"][1], x=b["x"])


def register(icon, pal, ramp_roles, C, Icon_):
    for b in BALLS:
        def make(b=b):
            @icon(b["item"], {b["item"]: icon_colors(b)}, labels={b["item"]: b["name"]})
            def _ball():
                return draw_icon(b)
        make()


# --------------------------------------------------------------------------
# Files, checks and the sheet
# --------------------------------------------------------------------------

def write_battle():
    for b in BALLS:
        save_indexed(battle_frames(b), battle_palette(b), os.path.join(BALLS_DIR, b["key"] + ".png"))
    # open.png carries the Poke Ball's palette; the engine uses only its tiles
    save_indexed(frame_array(FRAME_OPEN), battle_palette(BALLS[0]), os.path.join(BALLS_DIR, "open.png"))
    print(f"balls.py: wrote {len(BALLS)} ball sprites and open.png")


def read_png(path):
    im = Image.open(path)
    pal = list(im.getpalette() or [])
    pal += [0] * (48 - len(pal))
    return np.array(im), [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]


def check_battle():
    ok = True
    for b in BALLS:
        a, cols = read_png(os.path.join(BALLS_DIR, b["key"] + ".png"))
        if a.shape != (48, 16) or not np.array_equal(a, battle_frames(b)) or cols[1:] != battle_palette(b)[1:]:
            print(f"balls.py: graphics/balls/{b['key']}.png is not what balls.py draws; run balls.py --write")
            ok = False
    a, _ = read_png(os.path.join(BALLS_DIR, "open.png"))
    if not np.array_equal(a, frame_array(FRAME_OPEN)):
        print("balls.py: graphics/balls/open.png is stale; run balls.py --write")
        ok = False
    return ok


def git_png(rel):
    try:
        data = subprocess.run(["git", "-C", ROOT, "show", f"{BASE_REV}:{rel}"],
                              capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    im = Image.open(io.BytesIO(data))
    pal = list(im.getpalette() or [])
    pal += [0] * (48 - len(pal))
    return np.array(im) % 16, [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]


GRASS = (144, 184, 104)
PARCH = (232, 216, 176)


def rgb_on(a, cols, bg):
    return to_rgb(a, cols, bg)[..., :3]


def preview(outdir):
    from items_lib import palette_colors
    os.makedirs(outdir, exist_ok=True)
    k = 4
    cell_w = 24 * k + 16 * k * 3 + 24 + 16 * 3 + 24 * 2 + 70
    cell_h = 24 * k + 22
    cols_n = 3
    rows_n = (len(BALLS) + cols_n - 1) // cols_n
    sheet = Image.new("RGB", (cols_n * cell_w + 8, rows_n * cell_h + 26), (64, 40, 32))
    d = ImageDraw.Draw(sheet)
    d.text((6, 6), "icon 4x on the bag plate | battle frames 4x on grass (closed, opening, open) | "
                   "1x: icon, frames | before (1x)", fill=(248, 224, 136))
    for n, b in enumerate(BALLS):
        r, c = divmod(n, cols_n)
        x0, y0 = c * cell_w + 8, r * cell_h + 26
        d.text((x0, y0), f"{b['name'].replace('é', 'e')}  ({b['key']})", fill=(248, 240, 216))
        y = y0 + 14
        ic = draw_icon(b)
        icon_rgb = rgb_on(centred(ic.a), palette_colors(ic.roles, icon_colors(b)), PARCH)
        sheet.paste(Image.fromarray(upscale(icon_rgb, k)), (x0, y))
        fr = rgb_on(battle_frames(b), battle_palette(b), GRASS)
        x = x0 + 24 * k + 8
        for f in range(3):
            sheet.paste(Image.fromarray(upscale(fr[f * 16:(f + 1) * 16], k)), (x, y + 24))
            x += 16 * k + 4
        x += 8
        sheet.paste(Image.fromarray(icon_rgb), (x, y))
        for f in range(3):
            sheet.paste(Image.fromarray(fr[f * 16:(f + 1) * 16]), (x + 28 + f * 18, y + 4))
        old = git_png(f"graphics/balls/{b['key']}.png")
        oi = git_png(f"graphics/items/icons/{b['item']}.png")
        if old is not None:
            ofr = rgb_on(old[0], old[1], GRASS)
            for f in range(3):
                sheet.paste(Image.fromarray(ofr[f * 16:(f + 1) * 16]), (x + 28 + f * 18, y + 30))
        if oi is not None:
            pal_path = f"graphics/items/icon_palettes/{b['item']}.pal"
            try:
                data = subprocess.run(["git", "-C", ROOT, "show", f"{BASE_REV}:{pal_path}"],
                                      capture_output=True, check=True).stdout.decode().split()[3:]
                ocols = [tuple(int(v) for v in data[i * 3:i * 3 + 3]) for i in range(16)]
            except subprocess.CalledProcessError:
                ocols = oi[1]
            sheet.paste(Image.fromarray(rgb_on(oi[0], ocols, PARCH)), (x, y + 30))
    path = os.path.join(outdir, "balls_sheet.png")
    sheet.save(path)
    print(f"balls.py: preview in {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--preview")
    args = ap.parse_args()
    if args.write:
        write_battle()
    if args.preview:
        preview(args.preview)
    if args.check or args.write:
        if not check_battle():
            sys.exit(1)
        print(f"balls.py: {len(BALLS)} ball sprites match")


# ==========================================================================
# The balls, in item order. Names: design/TERMS.md.
# ==========================================================================
ball("strange", "strange_ball", "Aion Ball",
     cap=[(64, 112, 112), (112, 168, 160), (168, 216, 200), (224, 248, 240)], mark=GOLD,
     band=SILVER, boss=BOSS_MARBLE)
ball("poke", "poke_ball", "Poké Ball",
     cap=[(120, 40, 24), (184, 64, 40), (224, 112, 72), (248, 176, 128)], mark=[INK, (88, 72, 64)],
     band=[INK, (88, 72, 64)], boss=BOSS_MARBLE)
ball("great", "great_ball", "Theseus Ball",
     cap=[(24, 56, 120), (48, 104, 176), (96, 152, 216), (176, 216, 240)],
     mark=[(168, 56, 32), (232, 120, 80)])
ball("ultra", "ultra_ball", "Herakles Ball",
     cap=[(112, 64, 24), (176, 112, 40), (224, 160, 64), (248, 216, 128)],
     mark=[(64, 40, 24), (112, 72, 40)], band=[INK, (88, 72, 64)])
ball("master", "master_ball", "Daedalus Ball",
     cap=[(88, 56, 24), (152, 96, 40), (208, 144, 56), (248, 208, 112)],
     mark=[(48, 32, 24), (104, 64, 32)], band=[(80, 40, 112), (144, 88, 184)])
ball("premier", "premier_ball", "Xenia Ball",
     cap=[(168, 160, 152), (208, 200, 184), (232, 224, 208), (248, 248, 240)],
     mark=[(160, 32, 32), (224, 88, 64)], band=[(144, 32, 24), (208, 72, 48)], boss=BOSS_MARBLE)
ball("heal", "heal_ball", "Asclepius Ball",
     cap=[(168, 88, 104), (216, 136, 152), (240, 184, 192), (248, 224, 224)],
     mark=[(104, 64, 32), (48, 120, 64)], x=(128, 192, 104))
ball("net", "net_ball", "Arachne Ball",
     cap=[(24, 72, 72), (40, 112, 104), (72, 152, 136), (136, 200, 176)],
     mark=[(160, 200, 184), (232, 240, 232)], band=SILVER, boss=BOSS_MARBLE)
ball("nest", "nest_ball", "Alcyone Ball",
     cap=[(16, 80, 112), (32, 128, 160), (64, 176, 200), (152, 224, 232)],
     mark=[(192, 88, 32), (240, 152, 64)], band=[(152, 112, 48), (224, 192, 104)])
ball("dive", "dive_ball", "Poseidon Ball",
     cap=[(16, 40, 104), (32, 80, 160), (64, 128, 208), (144, 200, 240)], mark=GOLD,
     base=[(96, 152, 200), (176, 216, 232), (232, 248, 248)])
ball("dusk", "dusk_ball", "Nyx Ball",
     cap=[(24, 16, 48), (48, 32, 88), (80, 64, 128), (128, 112, 176)],
     mark=[(176, 168, 208), (248, 240, 200)], base=[(72, 72, 88), (112, 112, 128), (160, 160, 176)],
     band=[(64, 64, 80), (144, 144, 160)], boss=(216, 208, 232))
ball("timer", "timer_ball", "Chronos Ball",
     cap=[(144, 112, 64), (192, 160, 104), (224, 200, 144), (248, 240, 200)],
     mark=[(72, 48, 32), (232, 160, 40)], band=[(152, 64, 32), (216, 112, 64)])
ball("quick", "quick_ball", "Hermes Ball",
     cap=[(176, 112, 24), (224, 160, 40), (248, 200, 72), (248, 240, 160)],
     mark=[(160, 168, 192), (248, 248, 240)], band=[(40, 88, 160), (112, 168, 224)], boss=BOSS_MARBLE)
ball("repeat", "repeat_ball", "Mnemosyne Ball",
     cap=[(40, 32, 96), (72, 64, 144), (112, 104, 192), (176, 168, 224)],
     mark=[(168, 176, 224), (232, 240, 248)], band=SILVER, boss=BOSS_MARBLE)
ball("luxury", "luxury_ball", "Plutus Ball",
     cap=[(88, 16, 32), (136, 32, 48), (184, 64, 72), (224, 128, 120)], mark=GOLD,
     base=[(40, 32, 40), (72, 64, 72), (112, 104, 112)], band=GOLD)
ball("level", "level_ball", "Arete Ball",
     cap=[(32, 24, 32), (64, 48, 56), (104, 88, 96), (152, 136, 144)],
     mark=[(216, 152, 40), (248, 216, 104)])
ball("lure", "lure_ball", "Glaucus Ball",
     cap=[(24, 80, 64), (40, 128, 96), (80, 176, 136), (160, 216, 184)],
     mark=[(88, 136, 184), (192, 216, 232)])
ball("moon", "moon_ball", "Selene Ball",
     cap=[(16, 24, 64), (32, 48, 104), (56, 80, 144), (104, 128, 192)],
     mark=[(200, 200, 184), (248, 248, 224)], band=SILVER, boss=BOSS_MARBLE)
ball("friend", "friend_ball", "Philia Ball",
     cap=[(56, 72, 32), (96, 112, 48), (144, 160, 72), (192, 208, 128)], mark=GOLD)
ball("love", "love_ball", "Eros Ball",
     cap=[(176, 64, 104), (224, 112, 152), (240, 160, 192), (248, 208, 224)],
     mark=[(160, 24, 48), (224, 64, 80)])
ball("fast", "fast_ball", "Atalanta Ball",
     cap=[(144, 64, 24), (200, 104, 40), (232, 152, 72), (248, 200, 136)],
     mark=[(216, 160, 24), (248, 232, 128)], x=(56, 128, 48))
ball("heavy", "heavy_ball", "Atlas Ball",
     cap=[(72, 72, 80), (112, 112, 120), (160, 160, 168), (208, 208, 208)],
     mark=[(40, 72, 136), (112, 160, 216)])
ball("dream", "dream_ball", "Hypnos Ball",
     cap=[(88, 64, 120), (136, 104, 168), (184, 152, 208), (224, 208, 240)],
     mark=[(184, 32, 40), (240, 96, 80)], band=SILVER, boss=BOSS_MARBLE)
ball("safari", "safari_ball", "Pan Ball",
     cap=[(24, 56, 32), (48, 96, 48), (88, 136, 64), (144, 184, 104)],
     mark=[(176, 128, 56), (232, 192, 104)], band=[(152, 112, 48), (224, 192, 104)])
ball("sport", "sport_ball", "Agon Ball",
     cap=[(136, 88, 24), (192, 136, 40), (232, 184, 72), (248, 224, 144)],
     mark=[INK, (232, 224, 208)], band=[(152, 64, 32), (216, 112, 64)], boss=BOSS_MARBLE)
ball("park", "park_ball", "Elysium Ball",
     cap=[(104, 128, 48), (152, 176, 80), (200, 216, 128), (240, 240, 192)],
     mark=[(216, 192, 104), (248, 248, 240)], band=GOLD)
ball("beast", "beast_ball", "Typhon Ball",
     cap=[(16, 24, 48), (32, 48, 96), (56, 72, 136), (96, 112, 176)],
     mark=[(224, 112, 24), (248, 200, 64)], band=GOLD)
ball("cherish", "cherish_ball", "Charis Ball",
     cap=[(128, 24, 32), (176, 40, 40), (216, 80, 64), (248, 152, 128)], mark=GOLD,
     base=[(40, 32, 40), (72, 64, 72), (112, 104, 112)], band=GOLD)

import ball_motifs  # noqa: E402  (fills in each ball's motif16 and motif24)
ball_motifs.apply(BALLS)

if __name__ == "__main__":
    main()
