#!/usr/bin/env python3
"""The Pithos's jars: the sixteen box wallpapers, painted as the walls of
storage jars.

Each jar is the engine's 20x18-tile wallpaper (graphics/pokemon_storage/
wallpapers/<slot>/): the top three rows are the jar's lip with a parchment
tag where the jar's name prints, the rest is the painted wall the Pokemon
icons sit on. The wall is shaded like a pot's body (lit on the left, falling
into shade on the right), banded at shoulder and foot, and painted with the
theme's motif in the gaps between the icon cells.

The engine slots keep their names (forest, city, ...) for easy upstream
merges; the themes are Ichor's:

  slot        theme               slot         theme
  forest      olive grove         beach        sea-foam (shells)
  city        Akropolis columns   seafloor     Atlantis
  desert      wheatfield          river        the wine-dark sea
  savanna     vineyard            sky          starry night
  crag        labyrinth meander   polkadot     red-figure amphora
  volcano     the forge           pokecenter   Asclepeion (the rod)
  snow        Olympus clouds      machine      black-figure frieze
  cave        the Underworld      plain        laurel

Files per slot: frame.png carries every tile in the lip's palette (the
tilemap's palette 1), bg.png a single blank tile in the wall's palette
(palette 2); the build concatenates them into tiles.4bpp. Tile 0 stays
transparent: the lip's corners show the clay behind.
"""
import math

import numpy as np

from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/pokemon_storage/wallpapers"
IMG = ROOT / "design/phase1/img"
W, H = 160, 144

# Lip palette (tilemap palette 1): the same clay lip on every jar.
LIP = [TRANSPARENT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, PARCHMENT, PARCH_SHADE, PARCH_LIGHT,
       PARCH_DARK, BRONZE, BRONZE_LIGHT, GOLD]
L_IK, L_CD, L_CL, L_CLL, L_PA, L_PS, L_PL, L_PD, L_BR, L_BL, L_GO = range(1, 12)

# Wall palette slots (tilemap palette 2).
B_IK, B_EDGE, B_MID, B_GROUND, B_LIGHT, B_D, B_M, B_L, B_A, B_BAND, B_BINK = range(1, 12)


def lip(c):
    """The jar's lip, x 16-143, y 0-23, with the name tag in the middle."""
    P = 16
    x0, x1 = 16, 144
    # A rolled rim: rounded ends, lit top, shaded underside.
    for y in range(2, 22):
        inset = {2: 4, 3: 2, 4: 1, 19: 1, 20: 2, 21: 4}.get(y, 0)
        c.hline(x0 + inset, y, x1 - x0 - 2 * inset, P + L_IK)
    for y in range(3, 21):
        inset = {3: 4, 4: 2, 5: 1, 18: 1, 19: 2, 20: 4}.get(y, 0)
        col = L_CLL if y < 7 else (L_CL if y < 16 else L_CD)
        c.hline(x0 + 1 + inset, y, x1 - x0 - 2 - 2 * inset, P + col)
    c.hline(x0 + 5, 4, x1 - x0 - 10, P + L_PL)
    # Meander strips along the rim, either side of the tag.
    for (mx, mw) in [(22, 24), (114, 24)]:
        c.meander(mx, 9, mw, P + L_IK)
    # The name tag: parchment with clipped corners, tied with bronze pegs.
    tx, tw = 47, 66
    c.rect(tx + 1, 4, tw - 2, 16, P + L_IK)
    c.rect(tx, 5, tw, 14, P + L_IK)
    c.rect(tx + 1, 5, tw - 2, 14, P + L_PA)
    c.hline(tx + 2, 5, tw - 4, P + L_PL)
    c.hline(tx + 2, 18, tw - 4, P + L_PS)
    for px in (tx - 3, tx + tw):
        c.rect(px, 10, 3, 4, P + L_IK)
        c.px(px + 1, 11, P + L_BL)
        c.px(px + 1, 12, P + L_BR)


def wall(c, theme):
    """The jar's painted body, y 24-143."""
    P = 32
    y0, y1 = 24, 144
    for x in range(W):
        if x == 0 or x == W - 1:
            col = B_IK
        elif x <= 2:
            col = B_MID
        elif x <= 6:
            col = B_LIGHT
        elif x >= W - 3:
            col = B_EDGE
        elif x >= W - 7:
            col = B_MID
        else:
            col = B_GROUND
        c.vline(x, y0, y1 - y0, P + col)
    theme["paint"](c, P)
    band(c, P, 24, theme["top"])
    band(c, P, 136, theme["foot"])
    # Reshade the bands' ends so the body still reads as round.
    for y in list(range(24, 32)) + list(range(136, 144)):
        c.px(0, y, P + B_IK)
        c.px(W - 1, y, P + B_IK)


def band(c, P, y, kind):
    x0, w = 1, W - 2
    if kind == "meander":
        c.hline(x0, y, w, P + B_BINK)
        c.rect(x0, y + 1, w, 6, P + B_BAND)
        c.meander(x0, y + 2, w, P + B_BINK)
        c.hline(x0, y + 7, w, P + B_BINK)
    elif kind == "rays":
        rays_band(c, x0, y, w, P + B_BINK, P + B_BAND)
    elif kind == "tongues":
        c.rect(x0, y, w, 8, P + B_BAND)
        c.hline(x0, y, w, P + B_BINK)
        for x in range(x0, x0 + w, 6):
            for j, half in enumerate([2, 2, 2, 1, 1, 0]):
                c.hline(x + 2 - half, y + 1 + j, 2 * half + 1, P + B_BINK)
        c.hline(x0, y + 7, w, P + B_BINK)
    elif kind == "waves":
        c.rect(x0, y, w, 8, P + B_BAND)
        for x in range(x0, x0 + w):
            k = (x - x0) % 16
            h = [6, 5, 4, 3, 2, 2, 1, 1, 1, 2, 3, 3, 4, 5, 6, 6][k]
            c.vline(x, y + h, 7 - h, P + B_BINK)
        c.hline(x0, y + 7, w, P + B_BINK)
    elif kind == "dots":
        c.rect(x0, y, w, 8, P + B_BAND)
        c.hline(x0, y + 1, w, P + B_BINK)
        c.hline(x0, y + 6, w, P + B_BINK)
        for x in range(x0 + 2, x0 + w, 6):
            c.rect(x, y + 3, 2, 2, P + B_BINK)
    elif kind == "triglyph":
        c.rect(x0, y, w, 8, P + B_BAND)
        c.hline(x0, y, w, P + B_BINK)
        for x in range(x0 + 2, x0 + w, 12):
            for dx in (0, 2, 4):
                c.vline(x + dx, y + 1, 6, P + B_BINK)
        c.hline(x0, y + 7, w, P + B_BINK)
    elif kind == "laurel":
        c.rect(x0, y, w, 8, P + B_BAND)
        c.hline(x0, y + 4, w, P + B_D)
        for x in range(x0, x0 + w, 6):
            c.px(x + 1, y + 2, P + B_M)
            c.px(x + 2, y + 3, P + B_M)
            c.px(x + 4, y + 6, P + B_M)
            c.px(x + 3, y + 5, P + B_M)
        c.hline(x0, y, w, P + B_BINK)
        c.hline(x0, y + 7, w, P + B_BINK)


# Motifs sit in the gaps between the icon cells: icons are centered at
# (20 + 24c, 28 + 24r) on the wallpaper, so the gaps meet at (32 + 24c, 40 + 24r).
GAPS = [(32 + 24 * cx, 40 + 24 * cy) for cy in range(4) for cx in range(5)]
KEY = {"k": B_IK, "d": B_D, "m": B_M, "l": B_L, "a": B_A, "g": B_GROUND, "h": B_LIGHT}


def stamp(c, P, rows, cx, cy, flip=False):
    if flip:
        rows = [r[::-1] for r in rows]
    h, w = len(rows), len(rows[0])
    c.grid(cx - w // 2, cy - h // 2, rows, {k: P + v for k, v in KEY.items()}, transparent=".")


def motif_painter(rows, alt=None, gaps=GAPS):
    def paint(c, P):
        for i, (x, y) in enumerate(gaps):
            r = alt if (alt is not None and (i + (i // 5)) % 2) else rows
            stamp(c, P, r, x, y, flip=bool(alt is None and i % 2))
    return paint


OLIVE_SPRIG = [
    "......dd..",
    "....dmml..",
    "..d.mmd...",
    ".dmd.d..dm",
    "dmlm.d.dml",
    ".dd..dmm..",
    "....kdd...",
    "...kak....",
    "...kk.....",
]
WHEAT = [
    "....a....",
    "...mam...",
    "..dmlmd..",
    "...mam...",
    "..dmlmd..",
    "...mam...",
    "..dmlmd..",
    "....d....",
    "....d....",
    "...d.....",
]
GRAPES = [
    "....dmm...",
    "...dmlmd..",
    "..aa.ddm..",
    ".alakaa...",
    ".aakalaa..",
    "..aaaaka..",
    "...akaa...",
    "....aa....",
    ".....a....",
]
IVY = [
    "...m.....",
    "..mlm....",
    ".mlmlm.m.",
    "dmmlmmdlm",
    ".dmmmd.d.",
    "..dmd....",
    "...d.....",
]
BOLT = [
    "....aa",
    "...aa.",
    "..aa..",
    ".aaaa.",
    "...aa.",
    "..aa..",
    ".aa...",
    ".a....",
]
ASPHODEL = [
    "...l.l...",
    "..llmll..",
    ".l.mam.l.",
    "..llmll..",
    "...ldl...",
    "....d....",
    "...dd....",
    "....d....",
]
SHELL = [
    "..kkkkk..",
    ".klmlmlk.",
    "kmlmlmlmk",
    "klmlmlmlk",
    ".kmlmlmk.",
    "..kdddk..",
    "...kdk...",
]
CORAL = [
    "..a...a..",
    "..a.a.a..",
    "a.aaa.a.a",
    ".aa.aaaa.",
    "...aaa...",
    "....a....",
    "...aaa...",
]
BUBBLES = [
    ".ll..",
    "l..l.",
    ".ll..",
    "...l.",
    "..l.l",
    "...l.",
]
MOON = [
    "..aaa...",
    ".aa.....",
    "aa......",
    "aa......",
    "aa......",
    ".aa.....",
    "..aaa...",
]
STAR = [
    "...a...",
    "...a...",
    ".a.a.a.",
    "..aaa..",
    "aaala.a",
    "..aaa..",
    ".a.a.a.",
    "...a...",
]
AMPHORA = [
    "..mm.mm..",
    "...mmm...",
    ".mm.m.mm.",
    "m..mmm..m",
    ".mmmmmmm.",
    "mmmkkkmmm",
    "mmmmmmmmm",
    ".mmkkkmm.",
    "..mmmmm..",
    "...mmm...",
    "..mmmmm..",
]
ROD = [
    "....k....",
    "...kak...",
    "..mkkd...",
    ".m.k..d..",
    "..dkmm...",
    "...k..m..",
    "..mkdd...",
    ".d.k.....",
    "..mkm....",
    "...k.....",
    "...k.....",
]
HORSE = [
    ".......kk...",
    "......kkkk..",
    "kk...kkk.k..",
    ".kkkkkkk....",
    "..kkkkkk....",
    "..kkkkkk....",
    "..k.k..k.k..",
    ".k..k...k.k.",
    "k...k...k..k",
]
WREATH = [
    "...m.m...",
    "..m...m..",
    ".m.....m.",
    "dm.....md",
    ".m.....m.",
    "..m...m..",
    "...dad...",
    "....a....",
]
EMBER = [
    "..a..",
    ".ala.",
    "aamaa",
    ".ama.",
    "..a..",
]


def paint_columns(c, P):
    """Fluted marble: column drums, each flute a lit and a shaded line."""
    for x in range(8, W - 8):
        k = (x - 8) % 8
        if k == 0:
            c.vline(x, 32, 104, P + B_D)
        elif k == 1:
            c.vline(x, 32, 104, P + B_L)
    for y in range(56, 136, 48):
        c.hline(8, y, W - 16, P + B_M)


def paint_labyrinth(c, P):
    """A big meander key across the wall, the labyrinth's walls."""
    key = [
        "##########......",
        "#........#......",
        "#.######.#......",
        "#.#....#.#......",
        "#.#.##.#.#......",
        "#.#.#..#.#......",
        "#.#.####.#......",
        "#.#......#......",
        "#.########......",
        "#...............",
        "################",
    ]
    for y0 in range(36, 132, 24):
        for x0 in range(8, W - 8, 16):
            for j, row in enumerate(key):
                for i, ch in enumerate(row):
                    if ch == "#" and y0 + j < 134:
                        c.px(x0 + i, y0 + j, P + B_D)


def paint_scatter(rows_list, n=34, seed=7, extra=None):
    def paint(c, P):
        if extra:
            extra(c, P)
        rnd = np.random.default_rng(seed)
        pts = []
        while len(pts) < n:
            x, y = int(rnd.integers(10, W - 10)), int(rnd.integers(36, 132))
            if all(abs(x - a) + abs(y - b) > 14 for a, b in pts):
                pts.append((x, y))
        for i, (x, y) in enumerate(pts):
            stamp(c, P, rows_list[i % len(rows_list)], x, y)
    return paint


def paint_clouds(c, P):
    rnd = np.random.default_rng(3)
    for k in range(9):
        cx, cy = int(rnd.integers(16, W - 16)), int(rnd.integers(40, 128))
        for (dx, dy, r) in [(-6, 2, 5), (0, 0, 7), (7, 2, 5)]:
            for y in range(cy + dy - r, cy + dy + r + 1):
                for x in range(cx + dx - r, cx + dx + r + 1):
                    if (x - cx - dx) ** 2 + (y - cy - dy) ** 2 <= r * r and 30 < y < 134 and 6 < x < W - 6:
                        lit = (y - cy - dy) < -r // 2
                        c.px(x, y, P + (B_L if lit else B_M))
        for x in range(cx - 11, cx + 13):
            if 6 < x < W - 6:
                c.px(x, cy + 7, P + B_D)
    for (x, y) in GAPS[1::4]:
        stamp(c, P, BOLT, x, y)


def paint_wavesea(c, P):
    """The wine-dark sea: rows of running waves."""
    for y0 in range(40, 132, 16):
        for x in range(8, W - 8):
            k = (x + (y0 // 16) * 8) % 16
            h = [6, 5, 4, 3, 2, 2, 1, 1, 1, 2, 3, 3, 4, 5, 6, 6][k]
            c.vline(x, y0 + h, 1, P + B_L)
            c.vline(x, y0 + h + 1, 1, P + B_M)


def paint_forge(c, P):
    rnd = np.random.default_rng(11)
    # Basalt cracks.
    for k in range(10):
        x, y = int(rnd.integers(10, W - 10)), int(rnd.integers(36, 130))
        for s in range(8):
            c.px(x, y, P + B_D)
            x += int(rnd.integers(-1, 2))
            y += 1
    for (x, y) in GAPS:
        stamp(c, P, EMBER, x + int(rnd.integers(-3, 4)), y + int(rnd.integers(-3, 4)))


def paint_plainclay(c, P):
    for y in range(32, 136):
        if y % 8 == 7:
            c.hline(8, y, W - 16, P + B_M)


THEMES = {
    # slot: name, wall colors (ground, light, mid, edge, motif d/m/l, accent, band, band ink), bands, painter
    "forest": dict(name="olive grove", colors=[(208, 200, 152), (232, 224, 184), (176, 168, 120), (136, 128, 88),
                                               OLIVE_DARK, OLIVE, SILVER_LEAF, INK, CLAY, INK],
                   top="meander", foot="rays", paint=motif_painter(OLIVE_SPRIG)),
    "city": dict(name="Akropolis", colors=[MARBLE, MARBLE_LIGHT, MARBLE_DARK, (128, 120, 112),
                                          (152, 144, 128), (192, 184, 168), MARBLE_LIGHT, GOLD, MARBLE_DARK, INK],
                 top="triglyph", foot="dots", paint=paint_columns),
    "desert": dict(name="wheatfield", colors=[(232, 200, 128), (248, 224, 160), (208, 168, 96), (168, 128, 64),
                                             BRONZE, GOLD_DARK, GOLD_PALE, GOLD, BRONZE, INK],
                   top="tongues", foot="rays", paint=motif_painter(WHEAT)),
    "savanna": dict(name="vineyard", colors=[(216, 184, 136), (232, 208, 168), (184, 152, 104), (144, 112, 72),
                                            OLIVE_DARK, OLIVE, OLIVE_LIGHT, (104, 48, 96), (104, 48, 96), PARCH_LIGHT],
                    top="laurel", foot="rays", paint=motif_painter(GRAPES, IVY)),
    "crag": dict(name="labyrinth", colors=[(184, 168, 144), (208, 192, 168), (152, 136, 112), (112, 96, 80),
                                          (128, 112, 88), (152, 136, 112), (208, 192, 168), INK, CLAY, INK],
                 top="meander", foot="meander", paint=paint_labyrinth),
    "volcano": dict(name="the forge", colors=[(56, 48, 48), (80, 72, 64), (40, 32, 32), (24, 16, 16),
                                             (24, 16, 16), (232, 120, 40), GOLD_PALE, (200, 56, 24), (200, 56, 24), INK],
                    top="rays", foot="rays", paint=paint_forge),
    "snow": dict(name="Olympus", colors=[AEGEAN_PALE, (208, 232, 248), AEGEAN_LIGHT, AEGEAN,
                                        AEGEAN_LIGHT, MARBLE_LIGHT, MARBLE_LIGHT, GOLD, MARBLE, AEGEAN_DARK],
                 top="meander", foot="dots", paint=paint_clouds),
    "cave": dict(name="the Underworld", colors=[(112, 104, 112), (136, 128, 136), (88, 80, 88), (56, 48, 56),
                                               (64, 88, 64), (200, 192, 176), MARBLE_LIGHT, (184, 168, 96), (80, 72, 80), (40, 32, 40)],
                 top="meander", foot="rays", paint=motif_painter(ASPHODEL)),
    "beach": dict(name="sea-foam", colors=[(232, 216, 176), (248, 240, 216), (208, 184, 136), (168, 144, 96),
                                          (200, 120, 104), (232, 168, 152), (248, 224, 216), AEGEAN_LIGHT, AEGEAN_LIGHT, AEGEAN_DARK],
                  top="waves", foot="waves", paint=motif_painter(SHELL)),
    "seafloor": dict(name="Atlantis", colors=[AEGEAN_DARK, (40, 80, 152), (16, 40, 96), (8, 24, 64),
                                             (8, 24, 64), AEGEAN_LIGHT, AEGEAN_PALE, (224, 120, 104), AEGEAN, (8, 24, 64)],
                     top="waves", foot="rays", paint=motif_painter(CORAL, BUBBLES)),
    "river": dict(name="the wine-dark sea", colors=[(72, 40, 88), (96, 56, 112), (56, 32, 72), (32, 16, 48),
                                                   (32, 16, 48), (128, 88, 152), (176, 144, 200), GOLD, (128, 88, 152), (32, 16, 48)],
                  top="waves", foot="waves", paint=paint_wavesea),
    "sky": dict(name="starry night", colors=[(24, 32, 72), (40, 48, 96), (16, 24, 56), (8, 8, 32),
                                            (8, 8, 32), (48, 56, 104), PARCH_LIGHT, GOLD_PALE, (40, 48, 96), GOLD],
                top="dots", foot="dots", paint=paint_scatter([STAR, ["a"], ["a"], ["a"], [".a.", "aaa", ".a."]], n=30,
                                                          extra=lambda c, P: stamp(c, P, MOON, 128, 50))),
    "polkadot": dict(name="red-figure", colors=[GLAZE, (88, 56, 40), (48, 32, 24), INK,
                                               INK, CLAY, CLAY_LIGHT, CLAY, CLAY, INK],
                     top="meander", foot="rays", paint=motif_painter(AMPHORA)),
    "pokecenter": dict(name="Asclepeion", colors=[(232, 224, 200), MARBLE_LIGHT, (200, 192, 168), (160, 152, 128),
                                                 OLIVE_DARK, OLIVE, OLIVE_LIGHT, BRONZE, CLAY, INK],
                       top="meander", foot="dots", paint=motif_painter(ROD)),
    "machine": dict(name="black-figure", colors=[CLAY, CLAY_LIGHT, (160, 72, 40), CLAY_DARK,
                                                INK, INK, INK, PARCHMENT, CLAY, INK],
                    top="tongues", foot="rays", paint=motif_painter(HORSE)),
    "plain": dict(name="laurel", colors=[CLAY, CLAY_LIGHT, (160, 72, 40), CLAY_DARK,
                                        BRONZE, GOLD, GOLD_PALE, GOLD_PALE, CLAY, INK],
                  top="meander", foot="laurel", paint=motif_painter(WREATH)),
}
ORDER = ["forest", "city", "desert", "savanna", "crag", "volcano", "snow", "cave",
         "beach", "seafloor", "river", "sky", "polkadot", "pokecenter", "machine", "plain"]


def wall_palette(colors):
    ground, light, mid, edge, d, m, l, a, bandg, bink = colors
    return pal16([TRANSPARENT, INK, edge, mid, ground, light, d, m, l, a, bandg, bink])


def build(slot):
    t = THEMES[slot]
    c = Canvas(W, H)
    lip(c)
    wall(c, t)
    ts = TileSet(reserved=1)
    m = compile_map(c, ts, 20, 18)
    check_tiles(len(ts), 256, f"wallpapers/{slot}")
    return c, ts, m, [pal16(LIP), wall_palette(t["colors"])]


def write(slot):
    c, ts, m, pals = build(slot)
    d = OUT / slot
    write_tiles_png(d / "frame.png", ts.tiles, [pals[0]], tiles_wide=16)
    write_indexed_png(d / "bg.png", np.zeros((8, 8), np.uint8), [pals[1]])
    write_tilemap(d / "tilemap.bin", m)
    return c, pals


# The seventeenth wallpaper, WALLPAPER_FRIENDS, is Walda's gift in Emerald:
# sixteen patterns the player tints with two colors of their own. Nothing in
# Aethos gives it yet, but the engine still loads it, so its art is fired in
# the same clay: every color moves to the nearest step of a clay-and-parchment
# ramp by brightness. Nearest-step mapping leaves ramp colors where they are,
# so running this twice changes nothing.
FRIENDS = ["zigzagoon", "screen", "horizontal", "diagonal", "block", "ribbon", "pokecenter2",
           "frame", "blank", "circles", "azumarill", "pikachu", "legendary", "dusclops",
           "ludicolo", "whiscash"]
RAMP = sorted([INK, GLAZE, CLAY_DARK, RING, CLAY, PARCH_DARK, CLAY_LIGHT, PARCH_SHADE, PARCHMENT,
               PARCH_LIGHT], key=lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2])


def fire(c):
    lum = 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
    return min(RAMP, key=lambda r: abs(0.3 * r[0] + 0.59 * r[1] + 0.11 * r[2] - lum))


def write_friends():
    paths = [OUT / "friends_frame1.png", OUT / "friends_frame2.png"]
    paths += [OUT / s / "bg.png" for s in FRIENDS if (OUT / s / "bg.png").exists()]
    for p in paths:
        im = Image.open(p)
        a = np.array(im)
        pal = png_palette(p)[:16]
        new = [gba(pal[0])] + [fire(c) for c in pal[1:16]]
        write_indexed_png(p, a, [new])
    ribbon = OUT / "ribbon" / "frame.pal"
    if ribbon.exists():
        cols = read_jasc(ribbon)
        write_jasc(ribbon, [gba(cols[0])] + [fire(c) for c in cols[1:]])


def preview(results, out):
    sheet = np.zeros((2 * (H + 16) + 0, 8 * (W + 8), 3), np.uint8)
    sheet[:] = (40, 40, 40)
    for i, (slot, (c, pals)) in enumerate(results):
        rgb = canvas_rgb(c, [[TRANSPARENT] * 16] + pals)
        x, y = (i % 8) * (W + 8), (i // 8) * (H + 16)
        sheet[y:y + H, x:x + W] = rgb
    save_rgb(out, sheet, 2)


if __name__ == "__main__":
    results = [(s, write(s)) for s in ORDER]
    preview(results, IMG / "ui_codex_jars.png")
    write_friends()
