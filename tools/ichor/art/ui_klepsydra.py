#!/usr/bin/env python3
"""Draw the klepsydra: the water clock in the hero's room, which opens
Emerald's wall-clock screen (special StartWallClock / ViewWallClock).

Water drips from a bronze bowl into a tall bronze vessel. Its sight window
shows the water rising past twelve hour lines, empty at midnight and noon and
full twelve hours later; a bronze dial beside it, the kind Ktesibios's float
turned, carries the minute hand, and a slot at its foot shows AM or PM. The
D-pad turns the hand as in Emerald, and the water follows.

How the engine draws it (src/wallclock.c, where the Ichor edits are):
  BG3       this picture, palette 0 (male.pal for Theo, female.pal for Ianthe)
  sprites   hand.png in male.pal: the minute hand (frame 0) and the hour hand
            (frame 64, left blank: the water tells the hour), AM (128) and PM
            (132), and the water: its surface (136) and body (168), 32x64 each
  The water and the AM/PM tablets are drawn behind BG3 (OAM priority 3), so
  they show only through the window and the slot, which are holes in it.
  Color 0 of palette 0 is the backdrop seen through the holes: the vessel's
  dark, empty inside.
  BG2       the CONFIRM / CANCEL label, palette 12 (text_prompt.pal), over a
            parchment plaque painted here

Writes graphics/wallclock/: clock.png, clock_start.bin, clock_view.bin,
male.pal, female.pal, text_prompt.pal, hand.png; and design/phase1/img/ui_klepsydra*.png.

Usage: python3 tools/ichor/art/ui_klepsydra.py
"""
import math

import numpy as np

from ui_menus_lib import (ROOT, INK, CLAY, PARCHMENT, PARCH_SHADE, GOLD, MARBLE_LIGHT,
                          AEGEAN_DARK, AEGEAN, AEGEAN_LIGHT, MEANDER, TileSet, compile_map,
                          write_tiles_png, write_indexed_png, write_jasc, render_map, save_rgb,
                          pal16)
from ui_menus_summary import GLYPHS, letter

OUT = ROOT / "graphics/wallclock"
IMG = ROOT / "design/phase1/img"

BASE = [
    (56, 40, 32),     # 0  the backdrop: the vessel's empty inside, seen through the holes
    INK,              # 1
    (112, 64, 32),    # 2  bronze, dark
    (176, 112, 48),   # 3  bronze
    (232, 176, 104),  # 4  bronze, lit
    GOLD,             # 5
    PARCHMENT,        # 6  the dial's face; the plaques
    PARCH_SHADE,      # 7
    AEGEAN_DARK,      # 8  water, deep
    AEGEAN,           # 9  water
    AEGEAN_LIGHT,     # 10 water, lit
    MARBLE_LIGHT,     # 11 foam and glints
    None, None, None,  # 12-14 the wall: the hero's color
    CLAY,             # 15 the frieze
]
WALL_THEO = [(32, 80, 88), (64, 128, 136), (120, 184, 184)]       # a Minoan teal fresco
WALL_IANTHE = [(80, 56, 120), (128, 96, 168), (184, 160, 208)]    # violet, her name's flower


def palette(wall):
    p = list(BASE)
    p[12:15] = wall
    return pal16(p)


MALE, FEMALE = palette(WALL_THEO), palette(WALL_IANTHE)
PROMPT = [(0, 0, 0), PARCHMENT, (56, 40, 32), PARCH_SHADE]

K = dict(hole=0, ink=1, br_dk=2, br=3, br_lt=4, gold=5, parch=6, parch_sh=7, w_dk=8, w=9,
         w_lt=10, foam=11, wall_dk=12, wall=13, wall_lt=14, clay=15)
# A tilemap entry of 0 must not be a hole: tile 0 is solid wall here, and the
# holes are pixels of index 0 inside the vessel and dial tiles.

# --- Geometry -------------------------------------------------------------------
VX0, VX1 = 38, 90                 # the vessel's body
VY0, VY1 = 44, 126
WIN_X0, WIN_X1 = 54, 74           # the sight window (holes): the water sprite's x is 64
WIN_Y0, WIN_Y1 = 47, 119          # 72 px: six per hour; the level is WIN_Y1 at 0:00
DIAL_X, DIAL_Y, DIAL_R = 172, 70, 42
SLOT_R = 30                       # the AM/PM tablets circle the hand's pivot at 30 px


def wall():
    a = np.full((160, 256), K["wall"], np.uint8)
    # a fresco of lighter panels, edged dark
    for (x0, y0, x1, y1) in [(8, 16, 112, 118), (124, 16, 232, 118)]:
        for y in range(y0, y1):
            for x in range(x0, x1):
                edge = x in (x0, x1 - 1) or y in (y0, y1 - 1)
                inner = x in (x0 + 3, x1 - 4) or y in (y0 + 3, y1 - 4)
                a[y, x] = K["wall_dk"] if edge else (K["wall_lt"] if inner else K["wall"])
    # the frieze along the top
    a[0:11, :] = K["clay"]
    a[0, :] = K["ink"]
    for j, row in enumerate(MEANDER):
        for x in range(256):
            if row[x % 8] == "#":
                a[3 + j, x] = K["ink"]
    a[10, :] = K["ink"]
    # the dado
    a[126:160, :] = K["wall_dk"]
    a[126, :] = K["ink"]
    a[127, :] = K["clay"]
    return a


def disc(a, cx, cy, r, color):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if math.hypot(x - cx + 0.5, y - cy + 0.5) <= r:
                a[y, x] = color


def vessel(a):
    """The receiving vessel: a tall bronze situla with a flared rim, a foot,
    and a sight window in its front where the water shows."""
    for y in range(VY0, VY1 + 1):
        # the body tapers a little toward its foot
        inset = max(0, (y - 100) // 8)
        x0, x1 = VX0 + inset, VX1 - inset
        for x in range(x0, x1 + 1):
            if x in (x0, x1) or y == VY1:
                a[y, x] = K["ink"]
            else:
                u = (x - x0) / (x1 - x0)
                a[y, x] = K["br_lt"] if u < 0.18 else (K["br"] if u < 0.72 else K["br_dk"])
    # the rim, flared, and the foot
    for y in range(VY0 - 4, VY0 + 1):
        for x in range(VX0 - 4, VX1 + 5):
            edge = y in (VY0 - 4, VY0) or x in (VX0 - 4, VX1 + 4)
            a[y, x] = K["ink"] if edge else (K["br_lt"] if y == VY0 - 3 else K["br"])
    for y in range(VY1 - 2, VY1 + 2):
        for x in range(VX0 + 2, VX1 - 1):
            a[y, x] = K["ink"] if y in (VY1 - 2, VY1 + 1) or x in (VX0 + 2, VX1 - 2) else K["br_dk"]
    # a band of gold dots under the rim
    for x in range(VX0 + 3, VX1 - 2, 4):
        a[VY0 + 3, x] = K["gold"]
    # ring handles on its shoulders
    for side in (-1, 1):
        hx = VX0 - 3 if side < 0 else VX1 + 3
        for y in range(VY0 + 4, VY0 + 18):
            for x in range(hx - 5, hx + 6):
                d = math.hypot((x - hx) / 5.0, (y - (VY0 + 11)) / 6.5)
                if 0.62 < d <= 1 and side * (x - hx) >= -1:
                    a[y, x] = K["ink"] if d > 0.88 or d < 0.72 else K["br"]
    # the sight window: a hole, framed in lit bronze and ink
    for y in range(WIN_Y0 - 2, WIN_Y1 + 3):
        for x in range(WIN_X0 - 2, WIN_X1 + 2):
            if WIN_Y0 <= y <= WIN_Y1 and WIN_X0 <= x < WIN_X1:
                a[y, x] = K["hole"]
            elif y in (WIN_Y0 - 2, WIN_Y1 + 2) or x in (WIN_X0 - 2, WIN_X1 + 1):
                a[y, x] = K["ink"]
            else:
                a[y, x] = K["br_lt"]
    # the hour lines, painted inside: ticks every hour, a dotted line every
    # three, opaque so they read over water and empty vessel alike
    for h in range(1, 12):
        y = WIN_Y1 - 6 * h
        for x in range(WIN_X0, WIN_X1):
            if h % 3 == 0:
                if x % 2 == 0:
                    a[y, x] = K["foam"]
            elif x < WIN_X0 + 3 or x >= WIN_X1 - 3:
                a[y, x] = K["foam"]
    # Greek numerals beside the window: 3, 6, 9 and 12 (gamma, digamma, theta, iota-beta)
    numerals = {3: "G3", 6: "S6", 9: "TH", 12: "IB"}
    glyphs = {
        "G3": ["###", "#..", "#..", "#..", "#.."],          # gamma
        "S6": ["###", "#..", "##.", "#..", "#.."],          # digamma
        "TH": [".#.", "#.#", "###", "#.#", ".#."],          # theta
        "IB": ["#.##.", "#.#.#", "#.##.", "#.#.#", "#.##."],  # iota beta
    }
    for h, key in numerals.items():
        g = glyphs[key]
        y = WIN_Y1 - 6 * h - 2
        x = WIN_X0 - 4 - len(g[0])
        for j, row in enumerate(g):
            for i, ch in enumerate(row):
                if ch == "#":
                    a[y + j, x + i] = K["ink"]


def reservoir(a):
    """The bowl the water drips from, on a bronze bracket from the wall."""
    cx = (WIN_X0 + WIN_X1) // 2
    # the bracket
    for x in range(12, cx - 10):
        a[30, x] = K["ink"]
        a[31, x] = K["br_dk"]
        a[32, x] = K["ink"]
    for y in range(18, 34):
        a[y, 12] = K["ink"]
        a[y, 13] = K["br"]
        a[y, 14] = K["ink"]
    # the bowl: a bronze hemisphere with a lit rim and water at its brim
    for y in range(14, 33):
        for x in range(cx - 22, cx + 23):
            r = math.hypot((x - cx + 0.5) / 22, (y - 14) / 18)
            if y == 14 or y == 15:
                if abs(x - cx + 0.5) < 22:
                    a[y, x] = K["ink"] if y == 14 or abs(x - cx + 0.5) > 20.5 else K["w_lt"]
            elif r <= 1:
                edge = r > 0.92
                u = (x - (cx - 22)) / 44
                a[y, x] = K["ink"] if edge else (K["br_lt"] if u < 0.25 else K["br"] if u < 0.7 else K["br_dk"])
    for x in range(cx - 20, cx + 21, 5):
        a[18, x] = K["gold"]
    # the spout and the drops falling from it into the vessel's mouth
    for y in range(32, 36):
        a[y, cx - 1] = K["ink"]
        a[y, cx] = K["br_lt"]
        a[y, cx + 1] = K["ink"]
    for (y, c) in [(37, "w_lt"), (38, "w"), (40, "foam"), (41, "w_lt")]:
        a[y, cx] = K[c]


def dial(a):
    """The bronze dial: a parchment face with five-minute marks, gold at the
    quarters, and a slot at its foot for the AM/PM tablet."""
    cx, cy, R = DIAL_X, DIAL_Y, DIAL_R
    for y in range(cy - R - 2, cy + R + 3):
        for x in range(cx - R - 2, cx + R + 3):
            d = math.hypot(x - cx + 0.5, y - cy + 0.5)
            if d > R:
                continue
            if d > R - 1 or (R - 6 < d <= R - 5):
                a[y, x] = K["ink"]
            elif d > R - 5:
                lit = -((x - cx) + (y - cy)) / R
                a[y, x] = K["br_lt"] if lit > 0.3 else (K["br"] if lit > -0.4 else K["br_dk"])
            else:
                a[y, x] = K["parch"] if d < R - 8 or (x + y) % 2 else K["parch_sh"]
    for m in range(12):
        t = math.radians(m * 30 - 90)
        major = m % 3 == 0
        if m == 6:
            continue            # the slot takes the half-hour's place
        r0 = R - 13 if major else R - 10
        for k in range(int(r0 * 4), int((R - 7) * 4)):
            r = k / 4
            x, y = cx + r * math.cos(t), cy + r * math.sin(t)
            a[int(math.floor(y)), int(math.floor(x))] = K["gold"] if major else K["ink"]
    # the slot: a 16x16 hole at the tablets' circle, framed in bronze
    sx, sy = cx - 8, cy + SLOT_R - 8
    for y in range(sy - 2, sy + 18):
        for x in range(sx - 2, sx + 18):
            if sy <= y < sy + 16 and sx <= x < sx + 16:
                a[y, x] = K["hole"]
            elif y in (sy - 2, sy + 17) or x in (sx - 2, sx + 17):
                a[y, x] = K["ink"]
            else:
                a[y, x] = K["br"]
    # the boss under the hand's pivot
    disc(a, cx, cy, 3.5, K["ink"])
    disc(a, cx, cy, 2.5, K["br_lt"])


def plaque(a, x0, y0, x1, y1):
    for y in range(y0, y1):
        for x in range(x0, x1):
            edge = y in (y0, y1 - 1) or x in (x0, x1 - 1)
            rim = y in (y0 + 1, y1 - 2) or x in (x0 + 1, x1 - 2)
            a[y, x] = K["ink"] if edge else (K["br"] if rim else K["parch"])


def a_coin(a, x0, y0):
    """The A button, as the summary screen strikes it: a gold coin, ink A."""
    rows = [" #### ", "#gggg#", "#g#gg#", "##g#g#", "#g###g", "#g#g#g", " #### "]
    rows = [" ##### ", "#ggggg#", "#gg#gg#", "#g#g#g#", "#g###g#", "#g#g#g#", " ##### "]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == "#":
                a[y0 + j, x0 + i] = K["ink"]
            elif ch == "g":
                a[y0 + j, x0 + i] = K["gold"]


def dpad_hint(a):
    """In the set screen only: left and right arrows on a plaque, to turn the hand."""
    plaque(a, 12, 128, 52, 146)
    for (x0, d) in [(20, -1), (38, 1)]:
        for k in range(5):
            for j in range(-k, k + 1):
                x = x0 + (4 - k if d > 0 else k)
                a[137 + j, x] = K["ink"]


def picture(start):
    a = wall()
    reservoir(a)
    vessel(a)
    dial(a)
    # the label's plaque: the window prints at tiles (24, 16) 6x2
    plaque(a, 178, 126, 238, 146)
    a_coin(a, 182, 131)
    if start:
        dpad_hint(a)
    return a


# --- Sprites: hand.png, 64 wide, 256 tiles, 1D-mapped -----------------------------
def put_sprite(sheet, tile0, img):
    """Lay a w x h sprite into the sheet at tile0, in the order 1D mapping reads it."""
    h, w = img.shape
    t = tile0
    for ty in range(h // 8):
        for tx in range(w // 8):
            sy, sx = (t // 8) * 8, (t % 8) * 8
            sheet[sy:sy + 8, sx:sx + 8] = img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            t += 1


def minute_hand():
    """The hand pivots 24 px below the 64x64 frame's centre (sClockHandCoords),
    so it is drawn upward from (32, 56): a bronze pointer with a gold tip."""
    a = np.zeros((64, 64), np.uint8)
    L = 29
    for d in range(L + 1):
        y = 56 - d
        half = 1 if d < L - 6 else (1 if d < L - 2 else 0)
        for x in range(32 - half - 1, 32 + half + 1):
            a[y, x] = K["ink"]
        if half:
            a[y, 32 - half] = K["br_lt"]
            a[y, 31 + half] = K["br"] if d < L - 6 else K["gold"]
    a[56 - L - 1, 31] = K["ink"]
    # the counterweight and the pivot ring
    for y in range(55, 61):
        for x in range(29, 35):
            if math.hypot(x - 31.5, y - 57.5) <= 2.8:
                a[y, x] = K["ink"] if math.hypot(x - 31.5, y - 57.5) > 1.6 else K["gold"]
    return a


def tablet(text):
    a = np.zeros((16, 16), np.uint8)
    for y in range(16):
        for x in range(16):
            a[y, x] = K["parch"]
    a[0, :] = a[15, :] = K["br_dk"]

    class C:
        def px(self, x, y, c):
            a[y, x] = c
    w = sum(len(GLYPHS[ch][0]) + 1 for ch in text) - 1
    letter(C(), (16 - w) // 2, 5, text, K["ink"])
    return a


def water(surface):
    """32x64: the water as the window frames it. The surface sprite carries
    a lit meniscus on its top rows; the body sprite below it is deep water."""
    a = np.zeros((64, 32), np.uint8)
    for y in range(64):
        for x in range(32):
            if surface and y == 0:
                c = "foam"
            elif surface and y == 1:
                c = "w_lt"
            elif surface and y < 5:
                c = "w_lt" if (x + y) % 3 else "w"
            else:
                c = "w" if (x // 3 + y // 7) % 5 else "w_dk"
                if x in (13, 14) and y % 9 < 5:
                    c = "w_lt"      # a glint through the glassy water
            a[y, x] = K[c]
    return a


def sheet():
    s = np.zeros((256, 64), np.uint8)
    put_sprite(s, 0, minute_hand())
    put_sprite(s, 64, np.zeros((64, 64), np.uint8))   # the hour hand: the water tells the hour
    put_sprite(s, 128, tablet("AM"))
    put_sprite(s, 132, tablet("PM"))
    put_sprite(s, 136, water(True))
    put_sprite(s, 168, water(False))
    write_indexed_png(OUT / "hand.png", s, [MALE])
    return s


def write():
    start, view = picture(True), picture(False)
    ts = TileSet()
    ts.tiles, ts.lookup = [], {}

    class Cv:
        def __init__(self, a):
            self.a = a
            self.w, self.h = a.shape[1], a.shape[0]
    m_start = compile_map(Cv(start), ts, 32, 20, region=(0, 0, 32, 20))
    m_view = compile_map(Cv(view), ts, 32, 20, region=(0, 0, 32, 20))
    n = len(ts.tiles)
    assert n <= 448, n
    print(f"klepsydra: {n} tiles")
    write_tiles_png(OUT / "clock.png", ts.tiles, [MALE], tiles_wide=16)
    (OUT / "clock_start.bin").write_bytes(m_start.astype("<u2").tobytes())
    (OUT / "clock_view.bin").write_bytes(m_view.astype("<u2").tobytes())
    print("wrote graphics/wallclock/clock_start.bin, clock_view.bin")
    write_jasc(OUT / "male.pal", MALE)
    write_jasc(OUT / "female.pal", FEMALE)
    write_jasc(OUT / "text_prompt.pal", PROMPT)
    s = sheet()
    preview(ts.tiles, m_start, s)


def preview(tiles, m, s):
    """The set screen at 7:42, as the engine would compose it."""
    out = []
    for pal in (MALE, FEMALE):
        p = np.array(pal, np.uint8)
        rgb = render_map(m, tiles, [pal], 30, 20)
        holes = np.zeros((160, 240), bool)
        for ty in range(20):
            for tx in range(30):
                e = int(m[ty, tx])
                t = np.asarray(tiles[e & 0x3FF]) & 15
                if e & 0x400:
                    t = t[:, ::-1]
                if e & 0x800:
                    t = t[::-1]
                holes[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = t == 0
        under = np.zeros_like(rgb)
        under[:] = BASE[0]
        level = WIN_Y1 - (7 * 60 + 42) * 72 // 720
        surf = np.zeros((64, 32), np.uint8)
        for t in range(32):
            sy, sx = ((136 + t) // 8) * 8, ((136 + t) % 8) * 8
            ty, tx = t // 4, t % 4
            surf[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = s[sy:sy + 8, sx:sx + 8]
        y0 = level
        for y in range(64):
            if y0 + y < 160:
                under[y0 + y, 48:80] = p[surf[y]]
        for y in range(y0 + 64, 160):
            under[y, 48:80] = p[K["w"]]
        tab = np.zeros((16, 16), np.uint8)
        for t in range(4):
            sy, sx = ((128 + t) // 8) * 8, ((128 + t) % 8) * 8
            tab[(t // 2) * 8:(t // 2) * 8 + 8, (t % 2) * 8:(t % 2) * 8 + 8] = s[sy:sy + 8, sx:sx + 8]
        under[DIAL_Y + SLOT_R - 8:DIAL_Y + SLOT_R + 8, DIAL_X - 8:DIAL_X + 8] = p[tab]
        rgb[holes] = under[holes]
        # the minute hand at 42 minutes
        hand = np.zeros((64, 64), np.uint8)
        for t in range(64):
            sy, sx = (t // 8) * 8, (t % 8) * 8
            hand[(t // 8) * 8:(t // 8) * 8 + 8, (t % 8) * 8:(t % 8) * 8 + 8] = s[sy:sy + 8, sx:sx + 8]
        ang = math.radians(42 * 6)
        for y in range(64):
            for x in range(64):
                if hand[y, x]:
                    dx, dy = x - 32, y - 56
                    rx = dx * math.cos(ang) - dy * math.sin(ang)
                    ry = dx * math.sin(ang) + dy * math.cos(ang)
                    X, Y = int(round(DIAL_X + rx)), int(round(DIAL_Y + ry))
                    rgb[Y, X] = p[hand[y, x]]
        out.append(rgb)
    save_rgb(IMG / "ui_klepsydra_parts.png", np.hstack(out), 2)


if __name__ == "__main__":
    write()
