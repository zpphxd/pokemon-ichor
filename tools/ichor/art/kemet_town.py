"""Kemet's towns and marsh: mud-brick houses plastered white (each a household of
its own, every one with a door and a roof that says who lives there), granaries,
market stalls, Naukratis's Greek pottery, the delta's gnat-towers, reed fences,
nets, a shaduf, boats, and the seal-herders' shelter on Pharos.

A house is three rows seen from above and in front: the flat roof with what
people keep on it, then the roof's edge over the upper wall with its beam ends
and high windows, then the ground floor with the door.
"""
from __future__ import annotations

import math

import numpy as np

import kemet_lib as L
from kemet_lib import Layer, Struct, finish


# --------------------------------------------------------------------------
# House painters
# --------------------------------------------------------------------------

WHITE = {"hi": "w0", "lit": "pl2", "base": "pl1", "shade": "pl0", "dark": "mb1"}
RAW = {"hi": "pl2", "lit": "mb2", "base": "mb1", "shade": "mb0", "dark": "wd0"}


def plaster(Ly, x0, y0, w, h, pal, ox=0, oy=0):
    """Whitewashed mud brick: a flat wash with faint brick courses showing through."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 8, (y - oy) % 8
            c = pal["base"]
            if Y == 7 and (X + (y - oy) // 8 * 4) % 8 in (2, 3, 4):
                c = pal["shade"]
            elif (X, Y) in ((1, 2), (6, 5)):
                c = pal["lit"]
            Ly.px(x, y, c)


def bricks(Ly, x0, y0, w, h, ox=0, oy=0):
    """Bare mud brick: 8x4 bricks in a running bond."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = x - ox, y - oy
            row = Y // 4
            bx = (X + (4 if row % 2 else 0)) % 8
            by = Y % 4
            c = "mb1"
            if by == 3 or bx == 7:
                c = "mb0"
            elif by == 0:
                c = "mb2"
            Ly.px(x, y, c)


def roof(Ly, x0, y0, w, pal):
    """The flat roof (16 px tall) and its back parapet, outlined."""
    for y in range(y0, y0 + 16):
        for x in range(x0, x0 + w):
            c = pal["lit"]
            if ((x - x0) % 8, (y - y0) % 8) in ((3, 5), (6, 2)):
                c = pal["base"]
            Ly.px(x, y, c)
    Ly.hline(x0, x0 + w - 1, y0, "ink")
    Ly.hline(x0 + 1, x0 + w - 2, y0 + 1, pal["hi"])
    Ly.hline(x0 + 1, x0 + w - 2, y0 + 2, pal["base"])
    Ly.hline(x0 + 1, x0 + w - 2, y0 + 3, pal["shade"])
    Ly.vline(x0, y0, y0 + 15, "ink")
    Ly.vline(x0 + w - 1, y0, y0 + 15, "ink")
    Ly.vline(x0 + 1, y0 + 1, y0 + 15, pal["hi"])
    Ly.vline(x0 + w - 2, y0 + 1, y0 + 15, pal["shade"])


def front(Ly, x0, y0, w, pal, beams=True, raw=False):
    """Row 1 and row 2 of the house: the roof edge, the wall, beam ends (32 px)."""
    # the front parapet's coping and the roof's edge
    Ly.hline(x0, x0 + w - 1, y0, pal["hi"])
    Ly.hline(x0, x0 + w - 1, y0 + 1, pal["lit"])
    Ly.hline(x0, x0 + w - 1, y0 + 2, pal["base"])
    Ly.hline(x0, x0 + w - 1, y0 + 3, "ink")
    if raw:
        bricks(Ly, x0, y0 + 4, w, 28, ox=x0, oy=y0)
    else:
        plaster(Ly, x0, y0 + 4, w, 28, pal, ox=x0, oy=y0)
    Ly.vline(x0, y0, y0 + 31, "ink")
    Ly.vline(x0 + w - 1, y0, y0 + 31, "ink")
    Ly.vline(x0 + 1, y0 + 4, y0 + 30, pal["hi"] if not raw else "mb2")
    # shade under the eaves
    Ly.hline(x0 + 1, x0 + w - 2, y0 + 4, pal["shade"] if not raw else "mb0")
    if beams:
        for x in range(x0 + 4, x0 + w - 3, 8):
            Ly.blit(["kk", "dw"], {"k": "ink", "d": "wd0", "w": "wd2"}, x, y0 + 5)
    # the plinth: splashed mud at the foot
    for x in range(x0 + 1, x0 + w - 1):
        Ly.px(x, y0 + 30, "mb1" if x % 4 == 1 else "mb0")
        Ly.px(x, y0 + 31, "ink")


def window(Ly, x, y, w=4, h=3, grille=True):
    """A small high window with a palm-log sill."""
    Ly.rect(x, y, w, h, "door")
    Ly.hline(x - 1, x + w, y - 1, "ink")
    Ly.hline(x - 1, x + w, y + h, "wd1")
    Ly.px(x - 1, y + h, "wd0")
    if grille and w >= 4:
        Ly.vline(x + w // 2, y, y + h - 1, "wd1")


def doorway(Ly, x, y, frame=None, w=10, h=13, lintel=True):
    """A doorway at (x, y): dark opening, palm-log lintel, painted jambs."""
    Ly.rect(x, y, w, h, "door")
    Ly.vline(x - 1, y, y + h - 1, "ink")
    Ly.vline(x + w, y, y + h - 1, "ink")
    if frame:
        Ly.vline(x - 2, y, y + h - 1, frame)
        Ly.vline(x + w + 1, y, y + h - 1, frame)
    if lintel:
        Ly.hline(x - 3, x + w + 2, y - 2, "ink")
        Ly.hline(x - 2, x + w + 1, y - 1, "wd2")
        Ly.hline(x - 2, x + w + 1, y, "wd1")
        Ly.px(x - 3, y - 1, "ink")
        Ly.px(x + w + 2, y - 1, "ink")
    # a threshold step
    Ly.hline(x - 1, x + w, y + h, "pl2")
    # a hint of the room inside
    Ly.hline(x, x + w - 1, y + 1, "ink")


def jar(Ly, x, y, big=False):
    """An unglazed storage jar (brick group browns)."""
    rows = [" kk ", "k21k", "k221k", "k2211k", "k2211k", " k21k", "  kk "] if big else \
           [" kk ", "k21k", "k221k", "k221k", " kk "]
    Ly.blit(rows, {"k": "ink", "2": "mb2", "1": "mb1"}, x, y)


# roof furniture --------------------------------------------------------------

def roof_jars(x, y, n=3):
    def f(B):
        for i in range(n):
            jar(B, x + i * 6, y)
    return f


def roof_shade(x, y, w=20):
    """A palm-mat shade on four poles, the household's cool corner."""
    def f(B):
        for px in (x, x + w - 1):
            B.vline(px, y + 2, y + 10, "wd0")
        for yy in range(y, y + 4):
            for xx in range(x - 1, x + w + 1):
                B.px(xx, yy, "wd2" if (xx + yy) % 2 else "wd1")
        B.hline(x - 1, x + w, y - 1, "ink")
        B.hline(x - 1, x + w, y + 4, "ink")
        B.vline(x - 2, y, y + 4, "ink")
        B.vline(x + w + 1, y, y + 4, "ink")
        for xx in range(x, x + w):
            B.px(xx, y + 5, "pl0")
    return f


def roof_malqaf(x, y):
    """A wind-catcher: a slanted hood facing the north wind."""
    def f(B):
        B.blit(["kkkkkkk",
                "k22222k",
                "k21112k",
                "k1ddd1k",
                "k1ddd1k",
                "k11111k",
                "kkkkkkk"], {"k": "ink", "2": "pl2", "1": "pl1", "d": "door"}, x, y)
    return f


def roof_dovecote(x, y):
    """A pigeon tower: a white cone pocked with nest holes."""
    def f(B):
        rows = ["   kk   ",
                "  k22k  ",
                "  k2d2k ",
                " k22222k",
                " k2d2d2k",
                "k2222222k",
                "k2d22d22k",
                "k2222222k",
                "kkkkkkkkk"]
        B.blit(rows, {"k": "ink", "2": "pl2", "d": "door"}, x, y)
    return f


def roof_linen(x, y, w=24):
    """Linen strips drying on a line: the embalmer's."""
    def f(B):
        B.hline(x, x + w, y, "wd0")
        B.vline(x, y, y + 8, "wd0")
        B.vline(x + w, y, y + 8, "wd0")
        for i, xx in enumerate(range(x + 2, x + w - 2, 4)):
            ln = 5 + (i % 3)
            B.vline(xx, y + 1, y + ln, "w0")
            B.vline(xx + 1, y + 1, y + ln - 1, "pl2")
    return f


def roof_domes(x, y, n=3):
    """Beehive oven domes with smoke holes: the egg-ovens."""
    def f(B):
        for i in range(n):
            ox = x + i * 12
            B.blit(["  kkkkk  ",
                    " k22222k ",
                    "k2222211k",
                    "k22d2211k",
                    "k2222111k",
                    "kkkkkkkkk"], {"k": "ink", "2": "mb2", "1": "mb1", "d": "door"}, ox, y)
            B.px(ox + 4, y - 1, "net")
            B.px(ox + 5, y - 2, "pl0")
    return f


def roof_pots(x, y, n=4):
    """Pots drying in the sun: the potter's roof."""
    def f(B):
        for i in range(n):
            ox = x + i * 7
            B.blit([" kkk ", "k2r1k", "k2r1k", " k1k "], {"k": "ink", "2": "mb2", "1": "mb1",
                                                         "r": "rd1"}, ox, y + (i % 2))
    return f


def roof_nets(x, y, w=26):
    """Fishing nets heaped and hung over a pole: the net-loft."""
    def f(B):
        B.hline(x, x + w, y, "wd1")
        B.hline(x, x + w, y - 1, "ink")
        for xx in range(x + 1, x + w):
            for yy in range(y + 1, y + 7 - (xx % 3 == 0)):
                if (xx + yy) % 2 == 0:
                    B.px(xx, yy, "net")
        for xx in range(x + 2, x + w - 2, 6):
            B.px(xx, y + 7, "w0")      # floats
    return f


def roof_scrolls(x, y):
    """A scribe's table under the sun: papyrus rolls and a palette."""
    def f(B):
        B.rect(x, y + 3, 18, 5, "wd2")
        B.hline(x, x + 17, y + 2, "ink")
        B.hline(x, x + 17, y + 8, "ink")
        B.vline(x - 1, y + 3, y + 7, "ink")
        B.vline(x + 18, y + 3, y + 7, "ink")
        for i in range(3):
            B.hline(x + 2 + i * 5, x + 4 + i * 5, y + 4, "pl2")
            B.hline(x + 2 + i * 5, x + 4 + i * 5, y + 5, "pl1")
        B.px(x + 15, y + 6, "rd1")
        B.px(x + 16, y + 6, "door")
    return f


def roof_room(x, y, w=22):
    """An upper room on the roof: the field station's loggia, two columns and a shade."""
    def f(B):
        B.rect(x, y, w, 12, "pl1")
        B.hline(x, x + w - 1, y, "ink")
        B.hline(x + 1, x + w - 2, y + 1, "w0")
        B.vline(x, y, y + 11, "ink")
        B.vline(x + w - 1, y, y + 11, "ink")
        B.rect(x + 3, y + 4, w - 6, 7, "door")
        for cx in (x + 3 + (w - 6) // 3, x + 3 + 2 * (w - 6) // 3):
            B.vline(cx, y + 4, y + 10, "pl2")
            B.vline(cx + 1, y + 4, y + 10, "pl0")
        B.hline(x + 1, x + w - 2, y + 11, "pl0")
        B.hline(x, x + w - 1, y + 12, "ink")
    return f


def awning(x, y, w, stripes=("lp1", "pl2")):
    """A striped awning over a door, on two poles."""
    def f(B):
        for xx in range(x, x + w):
            for yy in range(y, y + 4):
                B.px(xx, yy, stripes[(xx - x) // 3 % 2])
        B.hline(x - 1, x + w, y - 1, "ink")
        B.hline(x - 1, x + w, y + 4, "ink")
        for xx in range(x, x + w, 3):
            B.px(xx, y + 5, stripes[(xx - x) // 3 % 2])
        for px in (x, x + w - 1):
            B.vline(px, y + 5, y + 13, "wd0")
    return f


def bench_jars(x, y):
    def f(B):
        jar(B, x, y, big=True)
        jar(B, x + 7, y + 2)
    return f


def lintel_ibis(x, y):
    """A painted ibis over the scribe's door: Thoth's bird."""
    def f(B):
        B.blit(["  kk     ",
                " kwwk    ",
                "  kwwwwk ",
                "   kwwwkk",
                "    k  k ",
                "    k  k "], {"k": "ink", "w": "w0"}, x, y)
        B.px(x + 1, y + 2, "ink")
        B.px(x, y + 3, "ink")
    return f


def stable_door(x, y):
    """The Apis byre's wide door, with horns over it."""
    def f(B):
        B.blit(["k        k",
                "kk      kk",
                " kk    kk ",
                "  kkkkkk  "], {"k": "ink"}, x, y)
        B.blit(["2        2",
                " 2      2 ",
                "  2    2  "], {"2": "pl2"}, x, y + 1)
    return f


def house_kit():
    """Houses built from one-cell parts, three rows tall: a roof row (ends, a plain
    run and the roof furniture that says who lives there), an upper wall (beam ends
    and high windows) and a ground floor with the door. Walls come whitewashed
    (`up_*`, `lo_*`) or as bare mud brick (`rup_*`, `rlo_*`); the roof is the same
    for both. Map builders lay recipes of part names (see naukratis.py)."""
    roof_parts = ["W", "run", "E", "jars", "pots", "dome", "malqaf", "dovecote",
                  "scrolls", "shade_l", "shade_r", "nets_l", "nets_r", "linen_l", "linen_r",
                  "loggia_l", "loggia_r"]
    white = ["up_W", "up", "up_win", "up_E", "up_ibis", "lo_W", "lo", "lo_win", "lo_E",
             "lo_door", "lo_door_blue", "lo_door_red", "lo_door_awning", "lo_jars"]
    raw = ["rup_W", "rup", "rup_E", "rlo_W", "rlo", "rlo_E", "rlo_door", "rlo_door_red",
           "rlo_door_wide"]
    names = ["roof_" + n for n in roof_parts] + white + raw
    W = 8
    H = -(-len(names) // W)
    walk = []
    for r in range(H):
        row = ""
        for i in range(W):
            k = r * W + i
            n = names[k] if k < len(names) else None
            row += "D" if n and "door" in n else "X" if n else "."
        walk.append(row)
    s = Struct("house", "House kit: mud brick, whitewashed or bare", W, H, walk=walk,
               ground="none",
               notes="Every house in Naukratis and Memphis is a recipe of these parts, three "
                     "rows tall: `roof_*` (W, run, E, then furniture: jars, pots, dome, malqaf, "
                     "dovecote, scrolls, and the pairs shade, nets, linen, loggia), the upper "
                     "wall (`up_*` whitewashed, `rup_*` bare brick: W, run, win, E, and up_ibis "
                     "painted with Thoth's bird) and the ground floor (`lo_*`, `rlo_*`: W, run, "
                     "win, E, jars, and the doors). Door parts are MB_NON_ANIMATED_DOOR.")
    B = s.B
    for k, n in enumerate(names):
        cx, cy = k % W, k // W
        ox, oy = cx * 16, cy * 16
        s.names[n] = (cx, cy)
        if n.startswith("roof_"):
            part = n[5:]
            roof_cell(B, ox, oy, part)
        else:
            raw_ = n.startswith("r")
            pal = RAW if raw_ else WHITE
            part = n[1:] if raw_ else n
            if part.startswith("up"):
                upper_cell(B, ox, oy, part[3:] or "run", pal, raw_)
            else:
                lower_cell(B, ox, oy, part[3:] or "run", pal, raw_)
    return finish(s)


def roof_cell(B, ox, oy, part):
    pal = WHITE
    for y in range(16):
        for x in range(16):
            c = pal["lit"]
            if (x % 8, y % 8) in ((3, 5), (6, 2)):
                c = pal["base"]
            B.px(ox + x, oy + y, c)
    B.hline(ox, ox + 15, oy, "ink")
    B.hline(ox, ox + 15, oy + 1, pal["hi"])
    B.hline(ox, ox + 15, oy + 2, pal["base"])
    B.hline(ox, ox + 15, oy + 3, pal["shade"])
    if part == "W":
        B.vline(ox, oy, oy + 15, "ink")
        B.vline(ox + 1, oy + 1, oy + 15, pal["hi"])
    elif part == "E":
        B.vline(ox + 15, oy, oy + 15, "ink")
        B.vline(ox + 14, oy + 1, oy + 15, pal["shade"])
    elif part == "jars":
        for x in (1, 9):
            jar(B, ox + x, oy + 7)
    elif part == "pots":
        for x in (2, 10):
            B.blit([" kkk ", "k2r1k", "k2r1k", " k1k "], {"k": "ink", "2": "mb2", "1": "mb1",
                                                         "r": "rd1"}, ox + x, oy + 8)
    elif part == "dome":
        roof_domes(ox + 3, oy + 7, 1)(B)
    elif part == "malqaf":
        roof_malqaf(ox + 4, oy + 5)(B)
    elif part == "dovecote":
        roof_dovecote(ox + 3, oy + 5)(B)
    elif part == "scrolls":
        B.rect(ox + 2, oy + 8, 12, 4, "wd2")
        B.hline(ox + 2, ox + 13, oy + 7, "ink")
        B.hline(ox + 2, ox + 13, oy + 12, "ink")
        B.vline(ox + 1, oy + 8, oy + 11, "ink")
        B.vline(ox + 14, oy + 8, oy + 11, "ink")
        for i in range(2):
            B.hline(ox + 3 + i * 5, ox + 5 + i * 5, oy + 9, "pl2")
            B.hline(ox + 3 + i * 5, ox + 5 + i * 5, oy + 10, "pl1")
        B.px(ox + 12, oy + 10, "rd1")
    elif part in ("shade_l", "shade_r"):
        x0 = 3 if part == "shade_l" else 0
        x1 = 15 if part == "shade_l" else 12
        for y in range(6, 10):
            for x in range(x0, x1 + 1):
                B.px(ox + x, oy + y, "wd2" if (x + y) % 2 else "wd1")
        B.hline(ox + x0, ox + x1, oy + 5, "ink")
        B.hline(ox + x0, ox + x1, oy + 10, "ink")
        edge = x0 if part == "shade_l" else x1
        B.vline(ox + edge, oy + 5, oy + 10, "ink")
        B.vline(ox + (x0 + 1 if part == "shade_l" else x1 - 1), oy + 11, oy + 14, "wd0")
        for x in range(x0 + 1, x1):
            B.px(ox + x, oy + 11, pal["shade"])
    elif part in ("nets_l", "nets_r"):
        x0 = 3 if part == "nets_l" else 0
        x1 = 15 if part == "nets_l" else 12
        B.hline(ox + x0, ox + x1, oy + 6, "wd1")
        B.hline(ox + x0, ox + x1, oy + 5, "ink")
        for x in range(x0, x1 + 1):
            for y in range(7, 13 - (x % 4 == 0)):
                if (x + y) % 2 == 0:
                    B.px(ox + x, oy + y, "net")
        for x in range(x0 + 2, x1, 4):
            B.px(ox + x, oy + 13, "w0")
    elif part in ("linen_l", "linen_r"):
        x0 = 3 if part == "linen_l" else 0
        x1 = 15 if part == "linen_l" else 12
        B.hline(ox + x0, ox + x1, oy + 5, "wd0")
        post = x0 if part == "linen_l" else x1
        B.vline(ox + post, oy + 5, oy + 13, "wd0")
        for i, x in enumerate(range(x0 + 2, x1 - 1, 4)):
            ln = 5 + (i % 2) * 2
            B.vline(ox + x, oy + 6, oy + 5 + ln, "w0")
            B.vline(ox + x + 1, oy + 6, oy + 4 + ln, "pl1")
    elif part in ("loggia_l", "loggia_r"):
        x0 = 3 if part == "loggia_l" else 0
        x1 = 15 if part == "loggia_l" else 12
        B.rect(ox + x0, oy + 4, x1 - x0 + 1, 10, "pl1")
        B.hline(ox + x0, ox + x1, oy + 4, "ink")
        B.hline(ox + x0, ox + x1, oy + 5, "w0")
        B.rect(ox + x0 + (2 if part == "loggia_l" else 0), oy + 8,
               x1 - x0 - 1, 5, "door")
        col = ox + (9 if part == "loggia_l" else 6)
        B.vline(col, oy + 8, oy + 12, "pl2")
        B.vline(col + 1, oy + 8, oy + 12, "pl0")
        B.hline(ox + x0, ox + x1, oy + 13, "pl0")
        B.hline(ox + x0, ox + x1, oy + 14, "ink")
        edge = x0 if part == "loggia_l" else x1
        B.vline(ox + edge, oy + 4, oy + 14, "ink")


def wall_fill(B, ox, oy, pal, raw_, y0, y1):
    if raw_:
        bricks(B, ox, oy + y0, 16, y1 - y0, ox=ox, oy=oy)
    else:
        plaster(B, ox, oy + y0, 16, y1 - y0, pal, ox=ox, oy=oy)


def edges(B, ox, oy, part, pal, raw_, y0=0):
    if part == "W":
        B.vline(ox, oy + y0, oy + 15, "ink")
        B.vline(ox + 1, oy + y0, oy + 15, pal["hi"] if not raw_ else "mb2")
    elif part == "E":
        B.vline(ox + 15, oy + y0, oy + 15, "ink")
        B.vline(ox + 14, oy + y0, oy + 15, pal["shade"])


def upper_cell(B, ox, oy, part, pal, raw_):
    wall_fill(B, ox, oy, pal, raw_, 4, 16)
    B.hline(ox, ox + 15, oy, pal["hi"] if not raw_ else "pl2")
    B.hline(ox, ox + 15, oy + 1, pal["lit"] if not raw_ else "pl1")
    B.hline(ox, ox + 15, oy + 2, pal["base"] if not raw_ else "pl0")
    B.hline(ox, ox + 15, oy + 3, "ink")
    B.hline(ox, ox + 15, oy + 4, pal["shade"] if not raw_ else "mb0")
    for x in (4, 12):
        B.blit(["kk", "dw"], {"k": "ink", "d": "wd0", "w": "wd2"}, ox + x, oy + 5)
    if part == "win":
        window(B, ox + 6, oy + 10)
    elif part == "ibis":
        lintel_ibis(ox + 3, oy + 8)(B)
    edges(B, ox, oy, part, pal, raw_)


def lower_cell(B, ox, oy, part, pal, raw_):
    wall_fill(B, ox, oy, pal, raw_, 0, 14)
    for x in range(16):
        B.px(ox + x, oy + 14, "mb1" if x % 4 == 1 else "mb0")
        B.px(ox + x, oy + 15, "ink")
    if part == "win":
        window(B, ox + 6, oy + 4)
    elif part == "jars":
        jar(B, ox + 2, oy + 7, big=True)
        jar(B, ox + 9, oy + 9)
    elif part.startswith("door"):
        frame = {"door": None, "door_blue": "lp1", "door_red": "rd1", "door_awning": "lp1",
                 "door_wide": None}[part]
        w = 12 if part == "door_wide" else 10
        top = 4 if part in ("door_awning", "door_wide") else 3
        doorway(B, ox + (16 - w) // 2, oy + top, frame=frame, w=w, h=14 - top - 1)
        if part == "door_awning":
            for x in range(16):
                for y in range(0, 3):
                    B.px(ox + x, oy + y, ("lp1", "pl2")[x // 3 % 2])
            B.hline(ox, ox + 15, oy + 3, "ink")
        if part == "door_wide":
            B.blit(["k          k", "kk        kk", " kkkkkkkkkk "], {"k": "ink"}, ox + 2, oy)
    edges(B, ox, oy, part, pal, raw_)


# --------------------------------------------------------------------------
# Yards, market and marsh
# --------------------------------------------------------------------------

def granary():
    s = Struct("granary", "Granary dome", 1, 2, walk=["T", "X"], ground="grass",
               notes="A beehive grain silo with its filling hole and a ladder: Egypt's bread. "
                     "Its dome is drawn over the player.")
    cnv = Layer(16, 32)
    cx, w, top = 8, 14, 3
    for y in range(top, 31):
        t = (y - top) / (31 - top)
        half = round(w / 2 * min(1, 0.45 + t * 1.4))
        for x in range(cx - half, cx + half):
            c = "pl2" if x < cx - half // 3 else "pl1" if x < cx + half // 2 else "pl0"
            cnv.px(x, y, c)
    cnv.rect(cx - 2, top + 13, 4, 4, "door")
    a = cnv.a[..., 3] > 0
    pad = np.pad(a, 1)
    ring = ~a & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(ring)):
        cnv.px(x, y, "ink")
    cnv.px(cx - 1, top, "door")
    cnv.px(cx, top, "door")
    for y in range(32):
        for x in range(16):
            if cnv.a[y, x, 3]:
                (s.T if y < 16 else s.M).a[y, x] = cnv.a[y, x]
    return finish(s)


def stall(kind):
    s = Struct(f"stall_{kind}", f"Market stall: {kind}", 2, 2, walk=["XX", "XX"], ground="grass",
               notes="A market table under a linen awning on poles.")
    T = Layer(32, 32)
    # awning
    for y in range(2, 10):
        for x in range(1, 31):
            T.px(x, y, "ln1" if (x // 4) % 2 == 0 else "st1")
    T.hline(1, 30, 1, "ink")
    T.hline(1, 30, 10, "ink")
    T.vline(0, 1, 10, "ink")
    T.vline(31, 1, 10, "ink")
    for x in range(1, 31, 4):
        T.px(x, 11, "ln0")
        T.px(x + 1, 11, "ln0")
    for px in (3, 28):
        T.vline(px, 11, 29, "wd0")
    # table
    T.rect(2, 18, 28, 4, "wd2")
    T.hline(2, 29, 17, "ink")
    T.hline(2, 29, 22, "wd0")
    T.rect(4, 23, 24, 6, "wd1")
    T.hline(4, 27, 29, "ink")
    goods = {
        "bread": lambda: [T.blit([" kk ", "k11k", "k21k"], {"k": "ink", "1": "st1", "2": "st2"},
                                 4 + i * 6, 13) for i in range(4)],
        "fish": lambda: [T.blit(["k  kkkk ", "kk1111rk", "k  kkkk "], {"k": "ink", "1": "ln0", "r": "rp"},
                                3 + i * 9, 13 + (i % 2)) for i in range(3)],
        "pots": lambda: [T.blit([" kk ", "k12k", "k12k", " kk "], {"k": "ink", "1": "tc2", "2": "tc1"},
                                4 + i * 6, 13) for i in range(4)],
        "baskets": lambda: [T.blit(["kkkkk", "k121k", " kkk "], {"k": "ink", "1": "st0", "2": "st2"},
                                   3 + i * 7, 14) for i in range(4)],
    }
    goods[kind]()
    for y in range(32):
        for x in range(32):
            if T.a[y, x, 3]:
                s.M.a[y, x] = T.a[y, x]
    return finish(s)


def amphorae():
    s = Struct("amphorae", "Greek amphorae (Naukratis ware)", 2, 1, walk=["XX"], ground="grass",
               notes="Naukratis's own pottery, black-figure on orange clay, waiting for a ship.")
    M = s.M
    for i, x in enumerate((1, 9, 17, 24)):
        rows = ["  kkk  ",
                "  k2k  ",
                "kkk2kkk",
                " k222k ",
                "k21112k",
                "k2kkk2k",
                "k21112k",
                " k221k ",
                "  k2k  ",
                "  kkk  "]
        M.blit(rows, {"k": "ink", "2": "tc2", "1": "tc1"}, x, 4 + (i % 2))
    return finish(s)


def gnat_tower():
    """Herodotus 2.95: in the marsh people sleep up towers, above the gnats."""
    s = Struct("gnat_tower", "Gnat-tower", 2, 4, walk=["TT", "XX", "XX", "XX"], ground="mud",
               notes="A mud-brick tower in the marsh; at night the family sleeps on top under "
                     "a net, above the gnats (Herodotus 2.95). The top row is drawn over the "
                     "player. Solid below.")
    cnv = Layer(32, 64)
    # the tower, tapering
    for y in range(14, 63):
        half = 10
        for x in range(16 - half, 16 + half):
            if x == 16 - half or x == 16 + half - 1:
                c = "ink"
            else:
                X, Y = x - (16 - half), y
                row = Y // 4
                bx = (X + (4 if row % 2 else 0)) % 8
                c = "mb0" if (Y % 4 == 3 or bx == 7) else ("mb2" if x < 14 else "mb1")
            cnv.px(x, y, c)
    # platform and net canopy
    cnv.rect(4, 11, 24, 4, "wd1")
    cnv.hline(4, 27, 10, "ink")
    cnv.hline(4, 27, 15, "ink")
    cnv.hline(5, 26, 11, "wd2")
    for x in (6, 25):
        cnv.vline(x, 1, 10, "wd0")
    for y in range(2, 10):
        for x in range(7, 25):
            if (x + y) % 2 == 0:
                cnv.px(x, y, "net" if y > 2 else "w0")
    cnv.hline(6, 25, 1, "ink")
    cnv.blit(["  kk      ", " kppkwwwww", "  kk wwwww"], {"k": "ink", "p": "mb2", "w": "w0"}, 10, 6)
    # the ladder
    for y in range(16, 62):
        cnv.px(22, y, "wd0")
        cnv.px(25, y, "wd0")
        if y % 4 == 0:
            cnv.hline(22, 25, y, "wd1")
    # a door-less arched niche for storage at the foot
    cnv.rect(10, 50, 6, 10, "door")
    cnv.hline(10, 15, 49, "ink")
    for y in range(64):
        for x in range(32):
            if cnv.a[y, x, 3]:
                (s.T if y < 16 else s.M).a[y, x] = cnv.a[y, x]
    return finish(s)


def fence():
    s = Struct("fence", "Reed fence", 3, 1, walk=["XXX"], ground="grass",
               notes="Bundled reeds lashed to stakes. Parts: run (west-east), v (north-"
                     "south), gate (a closed gate with a papyrus finial, for the Papyrus "
                     "Shallows Nursery until it opens).")
    M = s.M
    for cx, kind in enumerate(("run", "v", "gate")):
        ox = cx * 16
        if kind in ("l", "run", "r"):
            x0 = 6 if kind == "l" else 0
            x1 = 9 if kind == "r" else 15
            for x in range(x0, x1 + 1):
                M.px(ox + x, 6, "ink")
                M.px(ox + x, 7, "st2")
                M.px(ox + x, 8, "st1")
                M.px(ox + x, 9, "st0")
                M.px(ox + x, 10, "ink")
            for x in (x0 + (2 if kind == "l" else 4), 12 if kind != "r" else 7):
                if x0 <= x <= x1:
                    M.vline(ox + x, 3, 13, "wd1")
                    M.px(ox + x, 3, "ink")
                    M.px(ox + x, 13, "ink")
            for x in range(x0, x1 + 1, 4):
                M.px(ox + x, 8, "rp")
        elif kind == "v":
            for y in range(16):
                M.px(ox + 6, y, "ink")
                M.px(ox + 7, y, "st2")
                M.px(ox + 8, y, "st1")
                M.px(ox + 9, y, "ink")
            for y in (4, 12):
                M.hline(ox + 5, ox + 10, y, "rp")
        else:
            for x in range(0, 16):
                M.vline(ox + x, 4, 12, "st1" if x % 2 else "st2")
                M.px(ox + x, 3, "ink")
                M.px(ox + x, 13, "ink")
            M.hline(ox, ox + 15, 6, "wd1")
            M.hline(ox, ox + 15, 10, "wd1")
            M.blit([" k ", "kwk", " k "], {"k": "ink", "w": "st0"}, ox + 6, 7)
            M.blit(["k k k", " kkk ", "  k  "], {"k": "ink"}, ox + 5, 0)
        s.names[kind] = (cx, 0)
    return finish(s)


def nets():
    s = Struct("nets", "Nets drying on poles", 2, 1, walk=["XX"], ground="sand",
               notes="A fisher's nets hung to dry, on sand (Pharos, the harbor's beach).")
    M = s.M
    for x in (2, 29):
        M.vline(x, 1, 15, "wd0")
        M.px(x, 0, "ink")
    M.hline(2, 29, 2, "rp")
    for y in range(3, 13):
        for x in range(3, 29):
            sag = round(2 * math.sin((x - 3) / 26 * math.pi))
            if y > 3 + sag and (x + y) % 2 == 0:
                M.px(x, y, "net")
    for x in range(5, 28, 5):
        M.px(x, 12, "w0")
    return finish(s)


def shaduf():
    s = Struct("shaduf", "Shaduf", 2, 2, walk=["XX", "XX"], ground="mud",
               notes="A water-lift: a pole on a forked post, a bucket at one end and a mud "
                     "counterweight at the other. Stands on the bank.")
    T = Layer(32, 32)
    T.vline(14, 10, 30, "wd0")
    T.vline(15, 10, 30, "wd1")
    T.blit(["k  k", " kk "], {"k": "wd0"}, 13, 8)
    T.line(3, 4, 30, 16, "wd1")
    T.line(3, 5, 30, 17, "wd0")
    T.blit([" kkk ", "k111k", "k111k", " kkk "], {"k": "ink", "1": "wd0"}, 26, 16)  # weight
    T.vline(3, 5, 18, "rp")
    T.blit(["kkk", "k1k", "kkk"], {"k": "ink", "1": "wd2"}, 2, 18)
    for y in range(32):
        for x in range(32):
            if T.a[y, x, 3]:
                s.M.a[y, x] = T.a[y, x]
    return finish(s)


def skiff():
    s = Struct("skiff", "Papyrus skiff", 3, 1, walk=["XXX"], ground="sea",
               notes="A light boat of bound papyrus, moored. Solid.")
    M = s.M
    for x in range(2, 46):
        t = (x - 2) / 43
        lift = round(4 * (abs(t - 0.5) * 2) ** 3)
        y0 = 6 - lift
        M.vline(x, y0, 11, "st1")
        M.px(x, y0, "st2")
        M.px(x, 11, "st0")
        if x % 5 == 0:
            M.vline(x, y0, 11, "rp")
        M.px(x, 12, "ink")
        M.px(x, y0 - 1, "ink")
    M.line(30, 10, 44, 2, "wd0")     # the pole
    M.hline(4, 44, 13, "net")
    return finish(s)


def nile_boat():
    s = Struct("nile_boat", "Nile boat", 4, 3, walk=["XXXX", "XXXX", "XXXX"], ground="sea",
               notes="A cargo boat with a tall linen sail, moored at the quay. Solid.")
    cnv = Layer(64, 48)
    # hull
    for x in range(2, 62):
        t = (x - 2) / 59
        lift = round(7 * (abs(t - 0.5) * 2) ** 2.5)
        top = 32 - lift
        for y in range(top, 41):
            c = "wd2" if y == top + 1 else "wd1" if y < 38 else "wd0"
            cnv.px(x, y, c)
        cnv.px(x, top, "ink")
        cnv.px(x, 41, "ink")
        if x % 8 == 0:
            cnv.vline(x, top + 2, 38, "wd0")
    cnv.hline(6, 56, 35, "rp")
    # mast and sail
    cnv.vline(31, 3, 33, "wd0")
    cnv.vline(32, 3, 33, "wd1")
    for y in range(5, 27):
        for x in range(17, 47):
            c = "ln0" if x % 8 == 0 or y % 8 == 0 else "ln1"
            cnv.px(x, y, c)
    cnv.hline(15, 48, 4, "wd1")
    cnv.hline(15, 48, 27, "wd1")
    cnv.hline(15, 48, 3, "ink")
    cnv.hline(15, 48, 28, "ink")
    cnv.vline(16, 4, 27, "ink")
    cnv.vline(47, 4, 27, "ink")
    # steering oar and cabin
    cnv.line(4, 24, 10, 40, "wd0")
    cnv.rect(44, 28, 10, 5, "st1")
    cnv.hline(44, 53, 27, "ink")
    cnv.hline(44, 53, 33, "ink")
    for y in range(48):
        for x in range(64):
            if cnv.a[y, x, 3]:
                s.M.a[y, x] = cnv.a[y, x]
    return finish(s)


def shelter():
    s = Struct("shelter", "Seal-herders' shelter", 2, 2, walk=["XX", "XX"], ground="sand",
               notes="A reed lean-to on Pharos where the pharaoh's seal-herders keep out of the "
                     "sun. Open-fronted; no door.")
    T = Layer(32, 32)
    for y in range(3, 14):
        for x in range(2, 30):
            T.px(x, y, "st1" if (x + y // 2) % 4 else "st0")
    T.hline(2, 29, 2, "ink")
    T.hline(2, 29, 14, "ink")
    T.vline(1, 2, 14, "ink")
    T.vline(30, 2, 14, "ink")
    for x in range(3, 29, 2):
        T.px(x, 3, "st2")
    T.rect(3, 15, 26, 12, "net")
    for x in (4, 27):
        T.vline(x, 15, 29, "wd0")
    T.blit(["kkkkk", "k1212k", "k1212k", " kkkk "], {"k": "ink", "1": "st0", "2": "st2"}, 8, 22)
    T.blit([" kk ", "k12k", "k12k", " kk "], {"k": "ink", "1": "tc2", "2": "tc1"}, 19, 23)
    T.hline(3, 28, 29, "st0")
    for y in range(32):
        for x in range(32):
            if T.a[y, x, 3]:
                s.M.a[y, x] = T.a[y, x]
    return finish(s)


def regrounded(s, ground, key):
    """A copy of a structure drawn on borrowed grass, standing on other ground (the
    same art tiles; only the ground under them changes)."""
    import copy
    t = copy.deepcopy(s)
    t.key, t.title = key, s.title + f" (on {ground})"
    for c in list(t.ground):
        t.ground[c] = ground
    return finish(t)


def build():
    out = [house_kit(), granary()]
    for s in (stall("bread"), stall("pots"), amphorae()):
        out += [s, regrounded(s, "path", s.key + "_path"), regrounded(s, "quay", s.key + "_quay")]
    return out + [gnat_tower(), fence(), nets(), shaduf(), nile_boat(), shelter()]
