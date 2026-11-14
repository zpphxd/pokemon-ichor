#!/usr/bin/env python3
"""The berry tag (Bag > Berries > CHECK TAG), painted as a clay label.

Emerald's screen was a rounded paper tag on stripes. Ichor's is a terracotta
label tied on with twine, the kind a farmer hung on a jar of figs: a clay
tablet with a bored hole, a white-ground face ruled for the writing, a tondo
for the fruit, and a band of five seals naming the flavors. A gold ring marks
each flavor the fruit has. The backdrop is woven cloth, Aegean under Theo's
satchel and violet under Ianthe's, the trainer card's two colors.

How the engine draws it (src/berry_tag_screen.c, unchanged):
  - BG2 is the card (berry_tag.bin), BG0 the title band (berry_tag_title.bin),
    BG3 one tile, 0x42, repeated: palette 4 for Theo, 5 for Ianthe.
  - All four layers share charbase 0, and the text windows take tiles from 69
    up, so the art has tiles 0-68, with the backdrop fixed at 0x42 (66).
  - check_berry.pal holds palettes 0-5. The flavor rings (check_berry_circle.png)
    are sprites in palette 0, colors 12-14; each is centred 12 px left of the x
    the code gives it (64, 104, 144, 184, 224) and at y 100.
  - The windows print ink (2) with a parchment shadow (3) of berry_tag_screen.pal:
    the name at tile (11, 4), size and firmness at (11, 7), the description at
    (4, 14). The title prints at (2, 0) in 14 over a fill of 15.

Writes graphics/bag/: check_berry.png, check_berry.pal, berry_tag.bin,
berry_tag_title.bin, berry_tag_screen.pal; and design/phase1/img/ui_berry_tag.png.
It takes the palettes over from ui_menus_bag.py, which recolored the old card.

Usage: /usr/bin/python3 tools/ichor/art/ui_berry_tag.py
"""
import numpy as np

from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/bag"
IMG = ROOT / "design/phase1/img"
BG_TILE = 0x42
MAX_TILES = 69

TWINE = (216, 184, 120)
TWINE_DARK = (152, 112, 64)
AEGEAN_DARK2 = (16, 40, 96)
VIOLET = (104, 64, 144)
VIOLET_DARK = (72, 40, 104)
RING_EDGE = (216, 160, 72)

# Palette 0, the card. 12-14 color the flavor rings (sprites in this palette).
CARD = [TRANSPARENT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, (240, 176, 128), PARCHMENT, PARCH_SHADE,
        PARCH_DARK, PARCH_LIGHT, TWINE, TWINE_DARK, GOLD, GOLD_DARK, RING_EDGE, GLAZE]
(K, CD, CL, CLL, CP, PA, PS, PD, PL, TW, TD, RG1, RG2, RG3, GZ) = range(1, 16)
# Palettes 1-3 were Emerald's flavor colors; nothing on this screen uses them.
UNUSED = [TRANSPARENT] + [(0, 0, 0)] * 15
# Palettes 4 and 5: the woven backdrop (colors 12-13) and the title band.
THEO = [TRANSPARENT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, PARCHMENT, PARCH_SHADE, GLAZE,
        GOLD, GOLD_DARK, (0, 0, 0), (0, 0, 0), AEGEAN, AEGEAN_DARK2, (0, 0, 0), (0, 0, 0)]
IANTHE = list(THEO)
IANTHE[12], IANTHE[13] = VIOLET, VIOLET_DARK

FLAVORS = ["SPICY", "DRY", "SWEET", "BITTER", "SOUR"]
FLAVOR_X = [64 - 12, 104 - 12, 144 - 12, 184 - 12, 224 - 12]   # ring centres
FLAVOR_Y = 100


def backdrop_tile():
    """Woven cloth: two shades in a basket weave (colors 12 and 13)."""
    t = np.full((8, 8), 12, np.uint8)
    for y in range(8):
        for x in range(8):
            if (y < 4) == (x < 4):
                if y % 4 == 3:
                    t[y, x] = 13
            else:
                if x % 4 == 3:
                    t[y, x] = 13
    return t


def paint_card():
    c = Canvas(256, 160, 0)
    # The tablet, cols 2-29 and rows 3-18: a one-tile clay rim, lit from the
    # top left, round a white-ground face. Tile-aligned, so the rim repeats.
    x0, y0, x1, y1 = 16, 24, 240, 152
    c.rect(x0 + 1, y0, x1 - x0 - 2, y1 - y0, K)
    c.rect(x0, y0 + 1, x1 - x0, y1 - y0 - 2, K)
    c.rect(x0 + 1, y0 + 1, x1 - x0 - 2, y1 - y0 - 2, CL)
    c.hline(x0 + 2, y0 + 1, x1 - x0 - 4, CLL)
    c.vline(x0 + 1, y0 + 2, y1 - y0 - 4, CLL)
    c.hline(x0 + 2, y1 - 2, x1 - x0 - 4, CD)
    c.vline(x1 - 2, y0 + 2, y1 - y0 - 4, CD)
    c.frame(x0 + 6, y0 + 6, x1 - x0 - 12, y1 - y0 - 12, CD)
    c.rect(x0 + 8, y0 + 8, x1 - x0 - 16, y1 - y0 - 16, PA)
    # The bored hole in the rim and the twine hanging from it.
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if dx * dx + dy * dy <= 5:
                c.px(19 + dx, 84 + dy, K if dx * dx + dy * dy >= 3 else GZ)
    for x, y in [(17, 83), (15, 82), (13, 82), (11, 83), (10, 85), (10, 87), (11, 89),
                 (12, 91), (12, 93), (11, 95), (10, 97), (10, 99)]:
        c.px(x, y, TW)
        c.px(x + 1, y + 1, TD)
    # The tondo for the fruit (the sprite is centred at (56, 64)): an ink ring,
    # a clay band, a shaded ground. Symmetric about a tile corner, so its
    # quarters share tiles.
    for y in range(32, 96):
        for x in range(24, 88):
            r = ((x + 0.5 - 56) ** 2 + (y + 0.5 - 64) ** 2) ** 0.5
            if r <= 27:
                c.px(x, y, K)
            if r <= 26:
                c.px(x, y, CL if r > 23 else PS)
            if 22 < r <= 23:
                c.px(x, y, K)
    # Ruled lines under the writing: the name, size and firmness, the description.
    for y, x, w in [(47, 88, 64), (71, 88, 136), (87, 88, 136), (127, 32, 192), (143, 32, 192)]:
        c.hline(x, y, w, PD)
    # The band of flavor seals, on clay, with the five names in parchment.
    c.rect(24, 92, 208, 16, CL)
    c.hline(24, 91, 208, K)
    c.hline(24, 108, 208, K)
    for name, cx in zip(FLAVORS, FLAVOR_X):
        w = text_width(name, "small")
        draw_text(c, cx - w // 2, FLAVOR_Y - 8, name, PL, font="small")
    return c


def paint_title():
    """The title band across rows 0-1: black glaze, a gold rule, and a clay
    plaque where the code prints BERRY TAG (tiles 2-9)."""
    c = Canvas(256, 16, 0)
    c.rect(0, 0, 256, 14, 4 * 16 + 7)       # glaze, palette 4
    c.hline(0, 14, 256, 4 * 16 + 9)          # gold rule
    c.hline(0, 15, 256, 4 * 16 + 1)
    c.rect(16, 0, 64, 16, 4 * 16 + 3)       # the plaque the title prints on (fill 15 = clay)
    c.hline(16, 14, 64, 4 * 16 + 2)
    c.vline(15, 0, 15, 4 * 16 + 1)
    c.vline(80, 0, 15, 4 * 16 + 1)
    c.hline(15, 15, 66, 4 * 16 + 1)
    return c


def write():
    card = paint_card()
    title = paint_title()
    ts = TileSet(reserved=1)
    card_map = compile_map(card, ts, 32, 32, region=(0, 0, 32, 20))
    title_map = compile_map(title, ts, 32, 32, region=(0, 0, 32, 2))
    tiles = ts.tiles
    n = len(tiles)
    # The backdrop must be tile 0x42.
    bd = backdrop_tile()
    if n <= BG_TILE:
        tiles = tiles + [np.zeros((8, 8), np.uint8)] * (BG_TILE - n) + [bd]
    else:
        moved = tiles[BG_TILE]
        tiles = tiles[:BG_TILE] + [bd] + tiles[BG_TILE + 1:] + [moved]
        for m in (card_map, title_map):
            hit = (m & 0x3FF) == BG_TILE
            m[hit] = (m[hit] & 0xFC00) | (len(tiles) - 1)
    assert len(tiles) <= MAX_TILES, f"berry tag: {len(tiles)} tiles, the windows start at {MAX_TILES}"
    print(f"berry tag: {len(tiles)}/{MAX_TILES} tiles")
    write_tiles_png(OUT / "check_berry.png", tiles, [CARD], tiles_wide=10, min_tiles=70)
    write_tilemap(OUT / "berry_tag.bin", card_map)
    write_tilemap(OUT / "berry_tag_title.bin", title_map)
    write_jasc(OUT / "check_berry.pal", CARD + UNUSED + UNUSED + UNUSED + THEO + IANTHE)
    # Window text (palette 15): ink on the card; the title in ink on the clay plaque.
    z = (0, 0, 0)
    write_jasc(OUT / "berry_tag_screen.pal", [
        (248, 240, 216), (248, 240, 216), INK_TEXT, PARCH_SHADE, (192, 48, 32), (224, 160, 120), (56, 120, 32),
        (176, 200, 120), (40, 88, 176), (168, 184, 208), z, z, z, CLAY_DARK, PARCH_LIGHT, CLAY])
    preview(tiles, card_map, title_map)


def preview(tiles, card_map, title_map):
    pals = [CARD, UNUSED, UNUSED, UNUSED, THEO, IANTHE]
    shots = []
    for back in (4, 5):
        bg = np.zeros((32, 32), np.uint16) | (back << 12) | BG_TILE
        out = render_map(bg, tiles, pals, w=30, h=20)
        card = render_map(card_map, tiles, pals, w=30, h=20, transparent=(1, 2, 3))
        m = np.all(card == (1, 2, 3), axis=2)
        out[~m] = card[~m]
        top = render_map(title_map, tiles, pals, w=30, h=2, transparent=(1, 2, 3))
        tm = np.all(top == (1, 2, 3), axis=2)
        out[:16][~tm] = top[~tm]
        shots.append(out)
    save_rgb(IMG / "ui_berry_tag.png", np.hstack(shots), 2)


if __name__ == "__main__":
    write()
