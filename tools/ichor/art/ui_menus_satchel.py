#!/usr/bin/env python3
"""Draw the traveler's satchel shown in the bag screen, one 64x64 frame per
pocket, for Theo (bag_male.png) and Ianthe (bag_female.png).

The satchel is a pera, the leather shoulder bag of Greek travelers and of
Hermes. Each pocket opens the flap on what it holds, the way the Hoenn bag
opened a different pocket:

  frame 0  closed (shown while the pocket changes)
  frame 1  ITEMS       clay flasks of medicine
  frame 2  KEY ITEMS   a bronze key and a laurel sprig
  frame 3  POKE BALLS  balls
  frame 4  TMs & HMs   rolled scrolls with gold caps
  frame 5  BERRIES     berries and olive leaves

(The order is fixed by sSpriteAnim_Bag_* in src/item_menu_icons.c.) Theo's
satchel closes with a bronze disc; Ianthe's has a pointed flap embroidered
with a gold meander and a tassel. Both share graphics/bag/bag.pal.

Usage: python3 tools/ichor/art/ui_menus_satchel.py
"""
import numpy as np

from ui_menus_lib import *

OUT = ROOT / "graphics/bag"
IMG = ROOT / "design/phase1/img"

PAL = pal16([
    TRANSPARENT,       # 0
    INK,               # 1  outline
    (64, 40, 32),      # 2  leather, deepest (inside the bag)
    (112, 72, 40),     # 3  leather, shadow
    (160, 112, 64),    # 4  leather (buff, so it parts from the clay field)
    (200, 152, 96),    # 5  leather, lit
    (232, 200, 144),   # 6  leather, highlight / stitching
    GOLD_DARK,         # 7  bronze, shade
    GOLD,              # 8  bronze
    PARCHMENT,         # 9  scrolls, ball white
    PARCH_SHADE,       # 10 scroll shade
    (216, 64, 48),     # 11 ball red
    CLAY,              # 12 clay flasks
    CLAY_LIGHT,        # 13 clay, lit
    OLIVE_LIGHT,       # 14 leaves
    (128, 48, 96),     # 15 berries
])
OUTL, L0, L1, L2, L3, L4, BR0, BR1, PA, PAS, RED, CL, CLH, LEAF, BERRY = range(1, 16)

N = 64


def mask_from(fn):
    m = np.zeros((N, N), bool)
    for y in range(N):
        for x in range(N):
            m[y, x] = fn(x, y)
    return m


def shade(a, m, base, hi, lit, dark, deep=None, outline=OUTL):
    """Fill mask m with leather lit from the top left, with an ink outline."""
    inside = m.copy()
    edge = inside & ~(np.roll(inside, 1, 0) & np.roll(inside, -1, 0) & np.roll(inside, 1, 1) & np.roll(inside, -1, 1))
    a[inside] = base

    def off(dx, dy):
        return np.roll(np.roll(inside, dy, 0), dx, 1)

    # Highlights where the shape ends above or to the left.
    tl1 = inside & ~(off(1, 0) & off(0, 1))
    tl2 = inside & ~(off(2, 0) & off(0, 2)) & ~tl1
    br1 = inside & ~(off(-1, 0) & off(0, -1))
    br2 = inside & ~(off(-2, 0) & off(0, -2)) & ~br1
    br3 = inside & ~(off(-3, 0) & off(0, -3)) & ~br1 & ~br2
    a[br3] = dark if deep is None else base
    a[br2] = dark
    a[br1] = deep if deep is not None else dark
    a[tl2] = lit
    a[tl1] = hi
    a[edge] = outline
    return edge


def ellipse(cx, cy, rx, ry):
    return lambda x, y: ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0


def rounded_rect(x0, y0, x1, y1, rt, rb):
    def f(x, y):
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            return False
        r = rt if y < (y0 + y1) / 2 else rb
        cy = y0 + r if y < (y0 + y1) / 2 else y1 - r
        for cx in (x0 + r, x1 - r):
            if (x < x0 + r and cx == x0 + r) or (x > x1 - r and cx == x1 - r):
                if (y < y0 + r and r == rt) or (y > y1 - r and r == rb):
                    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r + r * 0.6
        return True
    return f


# --- The satchel ------------------------------------------------------------
BODY = rounded_rect(11, 24, 52, 58, 3, 9)


def strap(a):
    """The shoulder strap, an arch behind the bag, with a bronze ring at each
    end where it meets the body."""
    m = np.zeros((N, N), bool)
    for x in range(8, 56):
        t = (x - 31.5) / 22.0
        yc = 27 - 21 * (1 - t * t)
        for y in range(int(yc) - 2, int(yc) + 2):
            if 0 <= y < N:
                m[y, x] = True
    # thin at the very ends so it tucks behind the body
    shade(a, m, L2, L4, L3, L1)


def ring(a, cx, cy):
    for (x, y) in [(cx - 1, cy - 2), (cx, cy - 2), (cx - 2, cy - 1), (cx + 1, cy - 1),
                   (cx - 2, cy), (cx + 1, cy), (cx - 1, cy + 1), (cx, cy + 1)]:
        a[y, x] = BR1 if y < cy else BR0
    a[cy - 2, cx - 1] = PA


def body(a):
    m = mask_from(BODY)
    shade(a, m, L2, L4, L3, L1, deep=L1)
    # a seam and a row of stitches round the lower body
    for x in range(15, 49):
        if x % 3 == 0:
            a[54, x] = L4
    for y in range(32, 53):
        if y % 3 == 0:
            a[y, 14] = L3
            a[y, 49] = L1
    return m


def opening(a):
    """The open mouth of the bag: a dark oval under the raised flap."""
    m = mask_from(ellipse(32, 29, 19, 3))
    a[m] = L0
    rim = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    a[rim] = OUTL
    # lit front lip
    for x in range(14, 50):
        y = 31
        if a[y, x] in (L2, L3, L4, L1):
            a[y, x] = L4
    return m


def flap_closed_theo(a):
    def f(x, y):
        if not (9 <= x <= 54 and 21 <= y):
            return False
        t = (x - 31.5) / 23.0
        return y <= 38 + 7 * (1 - t * t)
    m = mask_from(f)
    shade(a, m, L3, L4, L4, L2, deep=L2)
    # stitching along the curved edge
    for x in range(12, 52, 2):
        t = (x - 31.5) / 23.0
        y = int(38 + 7 * (1 - t * t)) - 2
        a[y, x] = L4
    # bronze disc clasp
    disc = [
        " 1111 ",
        "188871",
        "188771",
        "187771",
        "177771",
        " 1111 ",
    ]
    stamp(a, 29, 41, disc, {"1": OUTL, "8": BR1, "7": BR0})
    a[42, 31] = PA


def flap_closed_ianthe(a):
    def f(x, y):
        if not (9 <= x <= 54 and 21 <= y):
            return False
        return y <= 33 + 13 * (1 - abs(x - 31.5) / 23.0)
    m = mask_from(f)
    shade(a, m, L3, L4, L4, L2, deep=L2)
    # an embroidered gold meander across the flap, on a dark leather band
    for y in range(26, 33):
        for x in range(12, 52):
            if m[y, x] and a[y, x] != OUTL:
                a[y, x] = L1
    for i, row in enumerate(MEANDER):
        for x in range(14, 50):
            if row[(x - 14) % 8] == "#" and m[27 + i, x]:
                a[27 + i, x] = BR1 if i < 2 else BR0
    for x in range(12, 52):
        if m[25, x] and a[25, x] != OUTL:
            a[25, x] = L4
        if m[33, x] and a[33, x] != OUTL:
            a[33, x] = L0
    # tassel from the point of the flap
    tassel = [
        " 11 ",
        "1871",
        " 11 ",
        "1871",
        "1871",
        "1877",
        "1771",
        " 7 7",
    ]
    stamp(a, 30, 45, tassel, {"1": OUTL, "8": BR1, "7": BR0})


def flap_open(a, ianthe):
    """The flap thrown back over the top of the bag, seen from inside."""
    def f(x, y):
        if not (10 <= x <= 53):
            return False
        t = (x - 31.5) / 22.0
        top = 13 + 6 * t * t if not ianthe else 10 + 13 * abs(t)
        return top <= y <= 24
    m = mask_from(f)
    shade(a, m, L3, L4, L4, L2)
    if ianthe:
        for x in range(16, 48, 3):
            t = (x - 31.5) / 22.0
            y = int(10 + 13 * abs(t)) + 2
            if m[y, x]:
                a[y, x] = BR1
    else:
        for x in range(13, 51, 2):
            t = (x - 31.5) / 22.0
            y = int(13 + 6 * t * t) + 2
            if m[y, x]:
                a[y, x] = L4


def stamp(a, x0, y0, rows, key):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != " ":
                a[y0 + j, x0 + i] = key[ch]


# --- Contents ---------------------------------------------------------------
# Everything is drawn rising out of the bag's mouth; the front of the bag is
# repainted afterwards, so anything below row 30 is hidden inside.
FLASK = [
    "  111  ",
    "  1d1  ",
    "  1c1  ",
    "  1c1  ",
    " 1cc1  ",
    "1hccc1 ",
    "1hccc11",
    "1hccc1c",
    "111111c",
    "1hccc11",
    "1hccc1 ",
    "1hccc1 ",
    "1hccc1 ",
    "1hccc1 ",
    "1hccc1 ",
    "1hccc1 ",
]


def contents_items(a):
    k = {"1": OUTL, "c": CL, "h": CLH, "d": PA}
    stamp(a, 17, 16, FLASK, k)
    stamp(a, 38, 15, FLASK, k)
    stamp(a, 27, 11, FLASK, k)
    # a bundle of herbs tucked between them
    for (x, y) in [(24, 22), (25, 21), (25, 23), (24, 24), (26, 20), (35, 21), (36, 20), (36, 22), (37, 23)]:
        a[y, x] = LEAF


BALL = [
    "  1111  ",
    " 1rrrr1 ",
    "1rhrrrr1",
    "1rrrrrr1",
    "11111111",
    "1ww11ww1",
    "1wwwwww1",
    " 1wwww1 ",
    "  1111  ",
]


def contents_balls(a):
    k = {"1": OUTL, "r": RED, "h": CLH, "w": PA}
    stamp(a, 15, 22, BALL, k)
    stamp(a, 41, 22, BALL, k)
    stamp(a, 22, 19, BALL, k)
    stamp(a, 34, 19, BALL, k)
    stamp(a, 28, 22, BALL, k)


def contents_scrolls(a):
    # Rolled papyri leaning out of the bag, each with a gold cap and a tie.
    for (x0, y0, x1, y1) in [(17, 30, 25, 10), (27, 30, 33, 8), (38, 30, 46, 12)]:
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n)
            y = round(y0 + (y1 - y0) * i / n)
            a[y, x - 2] = OUTL
            a[y, x - 1] = PA
            a[y, x] = PA
            a[y, x + 1] = PAS
            a[y, x + 2] = OUTL
        for d in range(-1, 2):
            a[y1, x1 + d] = BR1
            a[y1 + 1, x1 + d] = BR0
        a[y1 - 1, x1 - 1:x1 + 2] = OUTL
        ty = (y0 + y1) // 2 + 3
        tx = round(x0 + (x1 - x0) * (ty - y0) / (y1 - y0))
        a[ty, tx - 1:tx + 2] = CL


def contents_berries(a):
    berry = [" 11 ", "1bh1", "1bb1", " 11 "]
    k = {"1": OUTL, "b": BERRY, "h": CLH}
    for (x, y) in [(15, 25), (19, 23), (23, 25), (27, 21), (31, 24), (35, 22), (39, 25), (43, 23),
                   (23, 20), (31, 19), (39, 20), (19, 27), (35, 27), (45, 27), (27, 26)]:
        stamp(a, x, y, berry, k)
    leaf = ["  11 ", " 1ll1", "1lll1", "1ll1 ", " 11  "]
    for (x, y) in [(26, 14), (35, 15), (16, 18), (44, 17)]:
        stamp(a, x, y, leaf, {"1": OUTL, "l": LEAF})


def contents_key(a):
    key = [
        "  1111            ",
        " 188871           ",
        "188  871111111111 ",
        "18    78888888871 ",
        "188  8777777777771",
        " 187771 1871 1871 ",
        "  1111   11   11  ",
    ]
    stamp(a, 14, 19, key, {"1": OUTL, "8": BR1, "7": BR0})
    # a laurel sprig standing beside it
    stem = [(42, 29), (42, 28), (43, 27), (43, 26), (43, 25), (44, 24), (44, 23), (44, 22),
            (45, 21), (45, 20), (45, 19), (46, 18)]
    for (x, y) in stem:
        a[y, x] = OUTL
    leaf = [" 1 ", "1l1", "1l1", " 1 "]
    for (x, y) in [(39, 24), (45, 22), (40, 19), (46, 16), (42, 14)]:
        stamp(a, x, y, leaf, {"1": OUTL, "l": LEAF})


CONTENTS = {1: contents_items, 2: contents_key, 3: contents_balls, 4: contents_scrolls, 5: contents_berries}


def frame(n, ianthe):
    a = np.zeros((N, N), np.uint8)
    strap(a)
    ring(a, 12, 26)
    ring(a, 52, 26)
    body(a)
    if n == 0:
        (flap_closed_ianthe if ianthe else flap_closed_theo)(a)
    else:
        flap_open(a, ianthe)
        opening(a)
        CONTENTS[n](a)
        # the front of the bag hides the bottom of whatever sticks out
        m = mask_from(BODY) & (np.arange(N)[:, None] >= 30)
        front = np.zeros((N, N), np.uint8)
        shade(front, mask_from(BODY), L2, L4, L3, L1, deep=L1)
        a[m] = front[m]
        for x in range(14, 50):
            a[30, x] = OUTL
            a[31, x] = L4
        # a small front pocket, marked like the closed flap: Theo's with a
        # bronze disc, Ianthe's with a band of gold meander
        pocket = rounded_rect(20, 38, 43, 52, 2, 5)
        pm = mask_from(pocket)
        shade(a, pm, L3, L4, L4, L1, deep=L1)
        if ianthe:
            for y in range(41, 48):
                for x in range(21, 43):
                    if pm[y, x] and a[y, x] != OUTL:
                        a[y, x] = L1
            for i, row in enumerate(MEANDER):
                for x in range(22, 42):
                    if row[(x - 22) % 8] == "#":
                        a[42 + i, x] = BR1 if i < 2 else BR0
        else:
            disc = [" 1111 ", "188871", "187771", " 1111 "]
            stamp(a, 29, 43, disc, {"1": OUTL, "8": BR1, "7": BR0})
    return a


def write():
    for name, ianthe in (("bag_male.png", False), ("bag_female.png", True)):
        frames = [frame(n, ianthe) for n in range(6)]
        sheet = np.vstack(frames)
        write_indexed_png(OUT / name, sheet, [PAL])
    write_jasc(OUT / "bag.pal", PAL)
    # Review sheet: both satchels, every pocket, at 3x on the bag's field.
    rows = []
    for name in ("bag_male.png", "bag_female.png"):
        from PIL import Image
        a = np.array(Image.open(OUT / name))
        rgb = np.array(PAL, np.uint8)[a]
        rgb[a == 0] = CLAY
        rows.append(np.hstack([rgb[i * 64:(i + 1) * 64] for i in range(6)]))
    save_rgb(IMG / "ui_bag_satchel.png", np.vstack(rows), 3)


if __name__ == "__main__":
    write()
