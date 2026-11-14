#!/usr/bin/env python3
"""Draw Ichor's starter selection: Daphne's long table in the Akademia.

Three kraters stand on her white marble table, each painted for the Pokemon
inside, as in the room itself (TILES_civic.md): a cream serpent on a black
band for Snivy (it grows into Delphoi's python), flames for Cyndaquil, and a
white-ground krater with blue water and waves for Piplup. The selected krater
rocks as its Pokemon stirs. A black-figure hand points down at it, and the
chosen Pokemon rises on a painted tondo, the inside of a cup.

The screen keeps Emerald's flow (director ruling 11); only the art and the
positions change (src/starter_choose.c, marked Ichor).

  BG2 (behind)  the Akademia's wall: a meander frieze, ashlar, two pilasters
                and laurel festoons between them
  BG3           the long marble table, the kraters' shadows on it
  sprites       pokeball_selection.png: the three kraters (still, rocked left,
                rocked right) and the hand; starter_circle.png: the tondo

The sheet keeps Emerald's first frames where they were, because the Battle
Factory also loads its first 64 tiles: 0/16/32 Snivy's krater, 48 the hand,
then 64/80/96 Cyndaquil's and 112/128/144 Piplup's.

Writes graphics/starter_choose/: tiles.png, birch_grass.bin (the wall),
birch_bag.bin (the table), pokeball_selection.png, starter_circle.png; and a
preview in design/phase1/img/ui_starter_parts.png.

Usage: python3 tools/ichor/art/ui_starter_choose.py
"""
import math

import numpy as np

from ui_menus_lib import (ROOT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE, PARCHMENT,
                          PARCH_SHADE, PARCH_DARK, MARBLE_DARK, MARBLE, MARBLE_LIGHT, GOLD,
                          GOLD_DARK, GOLD_PALE, OLIVE, OLIVE_DARK, SILVER_LEAF, AEGEAN_DARK,
                          AEGEAN, AEGEAN_LIGHT, AEGEAN_PALE, TRANSPARENT, MEANDER, TileSet,
                          compile_map, write_tiles_png, write_indexed_png, render_map, save_rgb,
                          pal16)

OUT = ROOT / "graphics/starter_choose"
IMG = ROOT / "design/phase1/img"

# --- Background palettes: 0 the wall, 1 the table -----------------------------
WALL = pal16([
    TRANSPARENT, INK, CLAY_DARK, CLAY, CLAY_LIGHT,            # 1-4: the frieze
    (200, 176, 136), (224, 208, 168), PARCHMENT, (176, 152, 112),  # 5-8: ashlar, lit, mortar
    OLIVE_DARK, OLIVE, SILVER_LEAF,                            # 9-11: the laurel festoons
    MARBLE_DARK, MARBLE, MARBLE_LIGHT,                         # 12-14: the pilasters
    GOLD,                                                      # 15: the festoons' ties
])
TABLE = pal16([
    TRANSPARENT, INK, MARBLE_DARK, MARBLE, MARBLE_LIGHT, (248, 248, 248),   # 1-5: the slab
    (136, 128, 128), (104, 96, 96),                                       # 6-7: shadow on it
    AEGEAN_DARK, AEGEAN, CLAY_DARK, CLAY,                                  # 8-11: the apron's key
    (192, 184, 176),                                                       # 12: veining
])
W_ = {k: v for v, k in enumerate(["_", "ink", "clay_dk", "clay", "clay_lt", "stone", "stone_lt",
                                  "stone_pale", "mortar", "olive_dk", "olive", "silver",
                                  "marble_dk", "marble", "marble_lt", "gold"])}
T_ = {k: 16 + v for v, k in enumerate(["_", "ink", "marble_dk", "marble", "marble_lt", "white",
                                       "shadow", "shadow_dk", "aegean_dk", "aegean", "clay_dk",
                                       "clay", "vein"])}

KRATER_X = (60, 120, 180)     # sPokeballCoords: the kraters' centres
KRATER_Y = 80
TABLE_TOP = 88                # the slab's top face runs from here to its edge
TABLE_EDGE = 100


def wall():
    a = np.zeros((160, 256), np.uint8)
    # ashlar: courses 16 tall, blocks 32 wide, alternate courses offset
    for y in range(160):
        for x in range(256):
            course = (y - 16) // 16
            u = (x + (16 if course % 2 else 0)) % 32
            v = (y - 16) % 16
            if v == 15 or u == 31:
                c = "mortar"
            elif v == 0 or u == 0:
                c = "stone_pale"
            else:
                c = "stone_lt" if (u + v) % 11 else "stone"
            a[y, x] = W_[c]
    # the frieze along the top: clay with the meander, banded in ink
    for y in range(0, 16):
        for x in range(256):
            a[y, x] = W_["clay"]
    a[0, :] = W_["ink"]
    a[1, :] = W_["clay_dk"]
    for j, row in enumerate(MEANDER):
        for x in range(256):
            if row[x % 8] == "#":
                a[5 + j, x] = W_["ink"]
    a[3, :] = W_["clay_lt"]
    a[12, :] = W_["clay_dk"]
    a[13, :] = W_["ink"]
    a[14, :] = W_["clay_dk"]
    a[15, :] = W_["mortar"]
    # two Doric pilasters at the edges, fluted
    for px0 in (0, 224):
        for y in range(16, 160):
            for x in range(px0, px0 + 16):
                u = x - px0
                if u in (0, 15):
                    c = "marble_dk"
                elif u % 4 == 1:
                    c = "marble_lt"
                elif u % 4 == 3:
                    c = "marble_dk"
                else:
                    c = "marble"
                a[y, x] = W_[c]
        for y in range(16, 22):      # the capital
            for x in range(px0, px0 + 16):
                a[y, x] = W_["marble_lt"] if y < 18 else W_["marble"]
        a[22, px0:px0 + 16] = W_["marble_dk"]
    # a black fresco band under the frieze, where the starter's name shows
    # (the engine darkens the wall behind the label; on black, its pale
    # letters stand out), with laurel festoons swagged across it
    for y in range(16, 44):
        for x in range(16, 224):
            a[y, x] = W_["ink"]
    a[16, 16:224] = W_["clay_dk"]
    a[42, 16:224] = W_["clay_lt"]
    a[43, 16:224] = W_["clay_dk"]
    nails = [16, 72, 128, 184, 240]
    for x0, x1 in zip(nails, nails[1:]):
        for x in range(x0, x1 + 1):
            t = (x - x0) / (x1 - x0)
            y = 20 + int(round(14 * math.sin(math.pi * t)))
            for dy in range(-2, 3):
                ok = abs(dy) <= 2 - (1 if (x % 3 == 0) else 0)
                if ok:
                    c = "olive_dk" if dy == 2 else ("silver" if dy == -2 else "olive")
                    if (x + dy) % 4 == 0 and dy == 0:
                        c = "olive_dk"
                    a[y + dy, x] = W_[c]
        for x in (x0, x1):
            for (dx, dy) in [(0, 16), (0, 17), (-1, 18), (1, 18), (0, 18), (0, 19)]:
                a[dy, x + dx] = W_["gold"]
        # a ribbon hanging from each nail
        for x in (x0,):
            for dy in range(19, 30):
                a[dy, x + (1 if dy % 4 < 2 else 0)] = W_["gold"]
    return a


def table():
    a = np.zeros((160, 256), np.uint8)
    for y in range(TABLE_TOP, 160):
        for x in range(256):
            if y == TABLE_TOP:
                c = "ink"
            elif y < TABLE_TOP + 3:
                c = "white"
            elif y < TABLE_EDGE:
                c = "marble_lt"
                if (x * 3 + y * 7) % 37 == 0:
                    c = "vein"
            elif y == TABLE_EDGE:
                c = "marble_dk"
            elif y < TABLE_EDGE + 4:
                c = "marble"            # the slab's front edge
            elif y == TABLE_EDGE + 4:
                c = "ink"
            elif y < TABLE_EDGE + 13:
                c = "marble_dk"         # the apron, with a key in Aegean blue
            else:
                c = "ink" if y == TABLE_EDGE + 13 else "marble_dk"
            a[y, x] = T_[c]
    for j, row in enumerate(MEANDER):
        for x in range(256):
            if row[x % 8] == "#":
                a[TABLE_EDGE + 6 + j, x] = T_["aegean"]
    # the kraters' shadows on the slab
    for kx in KRATER_X:
        for y in range(TABLE_TOP + 1, TABLE_EDGE):
            for x in range(kx - 14, kx + 15):
                if ((x - kx + 0.5) / 12) ** 2 + ((y - 95) / 3.2) ** 2 <= 1:
                    a[y, x] = T_["shadow"]
    return a


# --- Sprites ----------------------------------------------------------------
SPR = pal16([
    TRANSPARENT, INK, (56, 40, 40),                  # 1 ink, 2 glaze
    CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE,          # 3-6 clay
    PARCHMENT,                                       # 7 the serpent's cream
    (232, 64, 32), GOLD,                             # 8 flame red, 9 flame gold
    MARBLE_LIGHT, MARBLE_DARK,                       # 10 white ground, 11 its shade
    AEGEAN, AEGEAN_LIGHT, AEGEAN_DARK,               # 12-14 water
    (248, 248, 248),                                 # 15 glints
])
SK = {" ": 0, "#": 1, "k": 2, "d": 3, "c": 4, "l": 5, "p": 6, "'": 7, "r": 8, "g": 9, "G": 3,
      "w": 10, "W": 11, "b": 12, "B": 13, "n": 14, "*": 15}

# A bell krater, 26 wide: lip, neck band, the painted band, the body, the foot.
# '@' marks the painted band's two rows; 'i' the mouth's interior.
KRATER = [
    "                          ",
    "  ######################  ",
    " #pllllllllllllllllllccd# ",
    " #iiiiiiiiiiiiiiiiiiiiii# ",
    "  #iiiiiiiiiiiiiiiiiiii#  ",
    "  #llcccccccccccccccccd#  ",
    "###kkkkkkkkkkkkkkkkkkkk###",
    "#c#@@@@@@@@@@@@@@@@@@@@#c#",
    "#d#@@@@@@@@@@@@@@@@@@@@#d#",
    "###@@@@@@@@@@@@@@@@@@@@###",
    "  #@@@@@@@@@@@@@@@@@@@@#  ",
    "  #kkkkkkkkkkkkkkkkkkkk#  ",
    "  #plcccccccccccccccccd#  ",
    "   #lcccccccccccccccdd#   ",
    "   #lccccccccccccccddd#   ",
    "    #lccccccccccccddd#    ",
    "     #llcccccccccdd#      ",
    "      ##kkkkkkkkkk##      ",
    "        #lcccccd#         ",
    "        #lcccdd#          ",
    "       #kkkkkkkkk#        ",
    "      #plcccccccdd#       ",
    "      ############        ",
]


def band(name, w, h):
    """The krater's painted band, w x h: each starter's own motif."""
    b = [[" "] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if name == "snivy":
                # a cream serpent winding across black glaze
                yy = 1.5 + 1.4 * math.sin(x * math.pi / 5.0)
                b[y][x] = "'" if abs(y - yy) < 0.75 else "k"
                if x == w - 3 and y == round(1.5 + 1.4 * math.sin((w - 3) * math.pi / 5.0)):
                    b[y][x] = "r"           # the serpent's tongue... its eye
            elif name == "cyndaquil":
                # flames licking up from the band's foot
                phase = (x % 5)
                hgt = [3, 4, 2, 4, 3][phase]
                if y >= h - hgt:
                    b[y][x] = "g" if (y == h - 1 or phase in (1, 3) and y >= h - 2) else "r"
                else:
                    b[y][x] = "k"
            else:
                # running waves in blue on white ground
                yy = 1.5 - 1.5 * math.cos(x * math.pi / 3.0)
                b[y][x] = "b" if abs(y - (h - 1 - yy * 0.66)) < 0.8 or y == h - 1 else "w"
    return b


def krater(name):
    rows = [list(r) for r in KRATER]
    h = sum(1 for r in KRATER if "@" in r)
    w = KRATER[7].count("@")
    b = band(name, w, h)
    j = 0
    for y, r in enumerate(rows):
        if "@" in r:
            x0 = r.index("@")
            for i in range(w):
                r[x0 + i] = b[j][i]
            j += 1
    white = name == "piplup"
    for r in rows:
        for i, ch in enumerate(r):
            if ch == "i":
                r[i] = "b" if white else "k"      # the mouth: water, or dark wine
            elif white and ch in "cl":
                r[i] = "w" if ch == "l" else "w"
            elif white and ch == "d":
                r[i] = "W"
            elif white and ch == "p":
                r[i] = "*"
    if white:
        # the water's surface catches the light
        for i, ch in enumerate(rows[3]):
            if ch == "b" and i % 5 == 2:
                rows[3][i] = "B"
    out = np.zeros((32, 32), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            out[y + 8, x + 3] = SK[ch]
    return out


def rocked(f, d):
    """The krater rocking: its upper rows shift by up to two pixels."""
    out = np.zeros_like(f)
    for y in range(32):
        s = int(round(d * max(0, (24 - y)) / 12.0))
        s = max(-2, min(2, s))
        row = f[y]
        out[y] = np.roll(row, s)
    return out


HAND = [   # a red-figure hand pointing down: clay, outlined in ink, its
           # fingers incised, a gold cuff, the index finger lit at its tip
    "    ######    ",
    "    #gGgg#    ",
    "    ######    ",
    "   #llllll#   ",
    "  #llllllll#  ",
    " #lllllllll#  ",
    " #ll#llllll#  ",
    " #ll#ldldll#  ",
    "  ##lldldll#  ",
    "    #lllll#   ",
    "    #ll####   ",
    "    #ll#      ",
    "    #ll#      ",
    "    #ll#      ",
    "    #ll#      ",
    "    #lp#      ",
    "     ##       ",
]


def hand():
    out = np.zeros((32, 32), np.uint8)
    for y, r in enumerate(HAND):
        for x, ch in enumerate(r):
            if ch != " ":
                out[y + 8, x + 10] = SK[ch]
    return out


def sprites():
    frames = {}
    for name in ("snivy", "cyndaquil", "piplup"):
        f = krater(name)
        frames[name] = [f, rocked(f, -1), rocked(f, 1)]
    order = frames["snivy"] + [hand()] + frames["cyndaquil"] + frames["piplup"]
    sheet = np.vstack(order)
    write_indexed_png(OUT / "pokeball_selection.png", sheet, [SPR])
    return sheet


CIRCLE = pal16([TRANSPARENT, INK, (56, 40, 40), CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE,
                PARCHMENT, GOLD])


def tondo():
    """The disc the chosen Pokemon rises on: a cup's tondo, clay inside a
    glaze band set with clay dots, the ground line at its foot."""
    a = np.zeros((64, 64), np.uint8)
    cx = cy = 31.5
    for y in range(64):
        for x in range(64):
            r = math.hypot(x - cx, y - cy)
            if r > 31:
                continue
            if r > 30:
                a[y, x] = 1
            elif r > 26:
                a[y, x] = 2
            elif r > 25:
                a[y, x] = 1
            else:
                a[y, x] = 7 if y < cy + 14 else (1 if y < cy + 15 else 3)
    for k in range(24):
        t = 2 * math.pi * k / 24
        x, y = cx + 28 * math.cos(t), cy + 28 * math.sin(t)
        a[int(round(y)), int(round(x))] = 5
    write_indexed_png(OUT / "starter_circle.png", a, [CIRCLE])
    return a


def write():
    wall_a, table_a = wall(), table()
    ts = TileSet(reserved=1)     # tile 0 stays blank: BG3 shows the wall where it is 0
    m_wall = compile_map(Canvas_(wall_a), ts, 32, 32, region=(0, 0, 32, 20))
    m_table = compile_map(Canvas_(table_a), ts, 32, 20, region=(0, 0, 32, 20))
    n = len(ts.tiles)
    assert n <= 384, n
    print(f"starter screen: {n} tiles")
    write_tiles_png(OUT / "tiles.png", ts.tiles, [WALL, TABLE], tiles_wide=16)
    (OUT / "birch_grass.bin").write_bytes(m_wall.astype("<u2").tobytes())
    (OUT / "birch_bag.bin").write_bytes(m_table.astype("<u2").tobytes())
    print("wrote graphics/starter_choose/birch_grass.bin, birch_bag.bin")
    sheet = sprites()
    circ = tondo()
    preview(ts.tiles, m_wall, m_table, sheet, circ)


class Canvas_:
    """compile_map wants .a, .w and .h."""

    def __init__(self, a):
        self.a = a

    @property
    def w(self):
        return self.a.shape[1]

    @property
    def h(self):
        return self.a.shape[0]


def preview(tiles, m_wall, m_table, sheet, circ):
    pals = [WALL, TABLE]
    bg = render_map(m_wall, tiles, pals, 30, 20)
    tb = render_map(m_table, tiles, pals, 30, 20, transparent=(255, 0, 255))
    m = (tb == (255, 0, 255)).all(axis=2)
    img = tb.copy()
    img[m] = bg[m]
    spr = np.array(SPR, np.uint8)
    for i, kx in enumerate(KRATER_X):
        row = (0, 128, 224)[i]      # frames 0, 4 and 7: each still krater
        f = sheet[row:row + 32]
        sub = img[KRATER_Y - 16:KRATER_Y + 16, kx - 16:kx + 16]
        sub[f != 0] = spr[f[f != 0]]
    hf = sheet[96:128]
    sub = img[46 - 16:46 + 16, 120 - 16:120 + 16]
    sub[hf != 0] = spr[hf[hf != 0]]
    cp = np.array(CIRCLE, np.uint8)
    big = cp[circ]
    big[circ == 0] = (40, 24, 32)
    save_rgb(IMG / "ui_starter_parts.png", img, 3)
    save_rgb(IMG / "ui_starter_tondo.png", big, 3)


if __name__ == "__main__":
    write()
