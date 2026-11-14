#!/usr/bin/env python3
"""Paint Ichor's battle interface as pottery: healthboxes, bars and tokens.

The healthboxes become terracotta plaques: a light-clay lettering panel
(names and numbers in black-figure ink) framed by two vertical meander strips,
the same running key as the dialogue box. The HP and EXP bars are ink-drawn
tubes. Party "balls" become little kraters standing on a painted ground line.

Engine facts this art must respect (src/battle_interface.c):
* Two OBJ palettes. The healthbox palette (from ball_status_bar.png) colors
  the boxes, the EXP bar, the status badges, the summary ground line and the
  enemy shadows. Its index 1 is the text ink, 2 the lettering ground
  (HEALTHBOX_BG_INDEX, used to erase text), 3 the text shadow, 10 and 11 the
  female and male signs (DYNAMIC_COLOR1/2) and 12-15 the badge color of
  battlers 0-3, written at run time from sStatusIconColors.
  The healthbar palette (from ball_display.png) colors the HP bar sprite and
  the party tokens.
* The HP bar is its own sprite laid over the box: "HP" (2 tiles), then six
  bar tiles. Its right end cap belongs to the box art. When a badge shows in
  the opponent's or a doubles box, the "HP" tiles become a blank tile and
  misc_frameend.png (the bar's left cap).
* Text is printed by the game: name at (8 or 16, 3), level right-aligned at
  x 88 or 96, the player's HP numbers under the bar. Every area it erases
  is filled with index 2, so those areas must be plain ground in the art.

Writes, in graphics/battle_interface/: the healthbox PNGs, hpbar*, expbar,
misc*, status1-4, *_frameend*, ball_display, ball_caught_indicator,
ball_status_bar and the enemy shadows.

Usage: python3 tools/ichor/art/ui_battle.py
"""
from ui_battle_lib import (
    AEGEAN, AEGEAN_DARK, AEGEAN_LIGHT, BI, CLAY, CLAY_DARK, CLAY_LIGHT, GLAZE, GOLD,
    GOLD_DARK, INK, PARCHMENT, RED, TRANSPARENT, IdxCanvas, meander_v, text_3x5,
)

# --- Palettes --------------------------------------------------------------
# Status badge colors. The game writes them into healthbox palette slots
# 12-15 (one per battler); src/battle_interface.c's sStatusIconColors holds the
# same values. Dark enough that parchment letters read on them.
STATUS_COLORS = {
    "PSN": (128, 56, 144),   # nightshade purple
    "PAR": (176, 120, 0),    # amber
    "SLP": (104, 96, 88),    # river stone
    "FRZ": AEGEAN,           # sea ice
    "BRN": RED,              # fire red
}

FEMALE = (152, 32, 72)       # added purple-red, the black-figure painters' accent
MALE = AEGEAN_DARK

HB = {"ink": 1, "ground": 2, "shadow": 3, "incised": 4, "letter": 5, "gold": 6,
      "trough": 7, "exp_hi": 8, "exp": 9, "female": 10, "male": 11, "badge": 12}
HEALTHBOX_PAL = [
    TRANSPARENT,
    INK,            # 1  text ink, outlines, meander
    CLAY_LIGHT,     # 2  lettering ground (HEALTHBOX_BG_INDEX)
    CLAY,           # 3  text shadow, plaque band
    CLAY_DARK,      # 4  incised lines
    PARCHMENT,      # 5  badge letters
    GOLD,           # 6  spare
    GLAZE,          # 7  empty EXP trough
    AEGEAN_LIGHT,   # 8  EXP fill, light
    AEGEAN,         # 9  EXP fill
    FEMALE,         # 10 female sign (DYNAMIC_COLOR1)
    MALE,           # 11 male sign (DYNAMIC_COLOR2)
    STATUS_COLORS["PSN"], STATUS_COLORS["PAR"], STATUS_COLORS["SLP"], STATUS_COLORS["FRZ"],
]

# HP fill colors: laurel green (healthy), sun-gold (caution), fire red (danger).
GREEN = [(168, 216, 104), (104, 168, 64), (56, 112, 40)]
YELLOW = [(248, 224, 120), GOLD, GOLD_DARK]
REDS = [(240, 120, 88), (208, 56, 40), (136, 32, 24)]
BAR = {"ink": 1, "trough": 2, "green": 3, "yellow": 6, "red": 9,
       "tok_light": 12, "tok": 13, "tok_dark": 14, "parch": 15}
HEALTHBAR_PAL = [TRANSPARENT, INK, GLAZE] + GREEN + YELLOW + REDS + [CLAY_LIGHT, CLAY, CLAY_DARK, PARCHMENT]


# --- The plaque ------------------------------------------------------------
def plaque(c, x0, x1, y0, y1):
    """A terracotta plaque from (x0, y0) to (x1, y1), inclusive.

    Clay rim, an incised line around a light-clay panel, and a vertical
    meander strip at each end, as on the panels of a painted vase.
    """
    g, ink, clay, inc = HB["ground"], HB["ink"], HB["shadow"], HB["incised"]
    c.rect(x0, y0, x1, y1, clay)
    c.rect(x0 + 6, y0 + 2, x1 - 6, y1 - 2, inc)
    c.rect(x0 + 7, y0 + 3, x1 - 7, y1 - 3, g)
    # The strips: the key runs from rim to rim, its outer stroke on the outside.
    meander_v(c, x0 + 1, y0 + 1, y1 - 1, ink, clay, phase=6)
    meander_v(c, x1 - 5, y0 + 1, y1 - 1, ink, clay, phase=6, mirror=True)
    # Soften the corners.
    for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        c.set(x, y, 0)


def bar_end_cap(c, x, y):
    """Right end of the HP bar tube, at column x of the box (bar row y = top)."""
    c.vline(x, y + 2, y + 5, HB["ink"])


def healthbox_opponent(doubles):
    c = IdxCanvas(128, 32)
    plaque(c, 0, 103, 2, 26)
    bar_end_cap(c, 88, 16)
    return c


def healthbox_player(singles):
    c = IdxCanvas(128, 64 if singles else 32)
    if singles:
        plaque(c, 8, 111, 2, 39)
        bar_end_cap(c, 96, 16)
        # EXP row: label, then the tube from x 31 to x 96 (the game fills
        # x 32..95 with expbar tiles; their bottom rows carry the rim).
        text_3x5(c, 17, 32, "EXP", HB["ink"])
        exp_tube_caps(c, 31, 96, 33)
    else:
        plaque(c, 8, 111, 2, 26)
        bar_end_cap(c, 96, 16)
    return c


def exp_tube_caps(c, xl, xr, y):
    c.vline(xl, y + 1, y + 2, HB["ink"])
    c.vline(xr, y + 1, y + 2, HB["ink"])


def healthbox_safari():
    c = IdxCanvas(128, 64)
    plaque(c, 8, 111, 2, 34)
    return c


# --- HP bar (healthbar palette) ---------------------------------------------
def hp_bar_tile(color, n):
    """One 8x8 slice of the bar tube with n of 8 pixels filled."""
    t = IdxCanvas(8, 8)
    t.hline(0, 7, 1, BAR["ink"])
    t.hline(0, 7, 6, BAR["ink"])
    t.rect(0, 2, 7, 5, BAR["trough"])
    if n:
        base = BAR[color]
        t.hline(0, n - 1, 2, base)          # highlight
        t.rect(0, 3, n - 1, 4, base + 1)
        t.hline(0, n - 1, 5, base + 2)      # shade
    return t


def hp_label():
    """'HP' in ink with the tube's left end, 16x8 (two tiles)."""
    t = IdxCanvas(16, 8)
    text_3x5(t, 4, 2, "HP", BAR["ink"])
    t.vline(15, 2, 5, BAR["ink"])
    return t


def bar_left_cap():
    t = IdxCanvas(8, 8)
    t.vline(7, 2, 5, BAR["ink"])
    return t


def hpbar_png():
    # Tile 0 blank (shown under a badge), 1-2 the label, 3-11 green 0..8 px.
    c = IdxCanvas(96, 8)
    c.paste(hp_label(), 8, 0)
    for n in range(9):
        c.paste(hp_bar_tile("green", n), 24 + 8 * n, 0)
    return c


def hpbar_anim_png():
    c = IdxCanvas(144, 8)
    for n in range(9):
        c.paste(hp_bar_tile("yellow", n), 8 * n, 0)
        c.paste(hp_bar_tile("red", n), 72 + 8 * n, 0)
    return c


# --- EXP bar (healthbox palette) --------------------------------------------
def expbar_png():
    """Nine tiles, 0..8 px filled. Rows 0-4 the tube, 5-7 the box's bottom rim."""
    c = IdxCanvas(72, 8)
    for n in range(9):
        x = 8 * n
        c.rect(x, 0, x + 7, 0, HB["ground"])
        c.hline(x, x + 7, 1, HB["ink"])
        c.rect(x, 2, x + 7, 3, HB["trough"])
        if n:
            c.hline(x, x + n - 1, 2, HB["exp_hi"])
            c.hline(x, x + n - 1, 3, HB["exp"])
        c.hline(x, x + 7, 4, HB["ink"])
        c.hline(x, x + 7, 5, HB["incised"])
        c.rect(x, 6, x + 7, 7, HB["shadow"])
    return c


# --- Misc tiles (healthbox palette) -----------------------------------------
def misc_png():
    """11 tiles. Only tile 3 is used by the game (it erases the badge area),
    so it must be plain ground; the rest stay as their vanilla roles."""
    c = IdxCanvas(88, 8)
    for t in (3, 4, 5, 6, 10):
        c.rect(8 * t, 0, 8 * t + 7, 7, HB["ground"])
    for t in (7, 8, 9):
        c.rect(8 * t, 0, 8 * t + 7, 7, HB["ground"])
        c.hline(8 * t, 8 * t + 7, 2, HB["incised"])
    return c


def frame_end(with_bar):
    t = IdxCanvas(8, 8)
    t.rect(0, 0, 7, 7, HB["ground"])
    if with_bar:
        t.vline(0, 2, 5, HB["ink"])
    return t


# --- Status badges (healthbox palette) --------------------------------------
# Letterforms from Emerald's badges, which read well at this size.
STATUS_LETTERS = {
    "PSN": ["...###...##..#..#..",
            "...#..#.#..#.##.#..",
            "...#..#..#...#.##..",
            "...###....#..#..#..",
            "...#....#..#.#..#..",
            "...#.....##..#..#.."],
    "PAR": ["...###...##..###...",
            "...#..#.#..#.#..#..",
            "...#..#.#..#.#..#..",
            "...###..####.###...",
            "...#....#..#.#.#...",
            "...#....#..#.#..#.."],
    "SLP": ["....##..#....###...",
            "...#..#.#....#..#..",
            "....#...#....#..#..",
            ".....#..#....###...",
            "...#..#.#....#.....",
            "....##..####.#....."],
    "FRZ": ["...####.###..####..",
            "...#....#..#....#..",
            "...#....#..#...#...",
            "...###..###...#....",
            "...#....#.#..#.....",
            "...#....#..#.####.."],
    "BRN": ["...###..###..#..#..",
            "...#..#.#..#.##.#..",
            "...###..#..#.#.##..",
            "...#..#.###..#..#..",
            "...#..#.#.#..#..#..",
            "...###..#..#.#..#.."],
    "FRB": ["...####.###..###...",
            "...#....#..#.#..#..",
            "...#....#..#.###...",
            "...###..###..#..#..",
            "...#....#.#..#..#..",
            "...#....#..#.###..."],
}
STATUS_ORDER = ["PSN", "PAR", "SLP", "FRZ", "BRN", "FRB"]  # rows of status.png


def status_png(battler):
    """24x48: one badge per row, filled with the battler's palette slot."""
    c = IdxCanvas(24, 48, HB["ground"])
    fill = HB["badge"] + battler
    for row, name in enumerate(STATUS_ORDER):
        y = row * 8
        c.rect(1, y, 19, y + 7, HB["ink"])
        c.rect(1, y + 1, 18, y + 6, fill)
        c.vline(0, y + 1, y + 6, HB["ink"])
        c.set(1, y, HB["ground"])
        c.set(1, y + 7, HB["ground"])
        c.set(19, y, HB["ground"])
        c.set(19, y + 7, HB["ground"])
        c.blit(0, y + 1, STATUS_LETTERS[name], {"#": HB["letter"]})
    return c


# --- Party tokens: little kraters (healthbar palette) ------------------------
KRATER = [
    ".#####..",
    "##lll##.",
    "#.ccc.#.",
    "##ccc##.",
    ".#ccc#..",
    "..###...",
    "...#....",
    "..###...",
]


def krater(body_light, body, rim=BAR["ink"]):
    t = IdxCanvas(8, 8)
    t.blit(0, 0, KRATER, {"#": rim, "l": body_light, "c": body})
    return t


def ball_display_png():
    # full (a healthy mon), empty slot, fainted, statused
    c = IdxCanvas(32, 8)
    c.paste(krater(BAR["tok_light"], BAR["tok"]), 0, 0)
    empty = IdxCanvas(8, 8)
    empty.blit(0, 0, KRATER, {"#": BAR["tok_dark"]})
    c.paste(empty, 8, 0)
    broken = krater(BAR["trough"], BAR["ink"])
    broken.set(3, 3, BAR["tok_dark"])  # a crack through the glaze
    broken.set(4, 2, BAR["tok_dark"])
    broken.set(3, 4, BAR["tok_dark"])
    c.paste(broken, 16, 0)
    c.paste(krater(BAR["yellow"], BAR["yellow"] + 2), 24, 0)
    return c


def ball_caught_png():
    return krater(BAR["tok_light"], BAR["tok"])


def ball_status_bar_png():
    """The ground line the kraters stand on: an ink line over a clay one,
    rising to a point at the leading end and fading out at the tail."""
    c = IdxCanvas(128, 8)
    ink, clay = HB["ink"], HB["shadow"]
    c.blit(0, 0, ["......#.",
                  "....##..",
                  "..##....",
                  "##......"], {"#": ink})
    c.hline(2, 55, 2, ink)
    c.hline(0, 55, 3, clay)
    c.hline(4, 55, 3, clay)
    for x in range(56, 104):
        # thin to a dotted tail, like a painter lifting the brush
        k = (x - 56) // 12
        if k == 0 or (k == 1 and x % 2 == 0) or (k == 2 and x % 4 == 0) or (k == 3 and x % 8 == 0):
            c.set(x, 2, ink)
            c.set(x, 3, clay)
    return c


# --- Enemy shadows (healthbox palette) --------------------------------------
def shadow_ellipse(c, cx, cy, rx, ry):
    """A glaze core with a dithered rim, so the platform shows through."""
    for y in range(c.h):
        for x in range(c.w):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            d = dx * dx + dy * dy
            if d <= 0.45:
                c.set(x, y, HB["trough"])
            elif d <= 1.0 and (x + y) % 2 == 0:
                c.set(x, y, HB["ink"])


def enemy_shadow_png():
    c = IdxCanvas(32, 8)
    shadow_ellipse(c, 16, 4, 16, 4)
    return c


def enemy_shadows_sized_png():
    # Four 64x8 bands, small to extra large, as in vanilla.
    c = IdxCanvas(64, 32)
    for band, (rx, ry) in enumerate(((14, 3.5), (21, 4), (25, 4), (30, 4))):
        b = IdxCanvas(64, 8)
        shadow_ellipse(b, 32, 4, rx, ry)
        c.paste(b, 0, band * 8)
    return c


# --- Output ------------------------------------------------------------------
def main():
    hb, bar = HEALTHBOX_PAL, HEALTHBAR_PAL
    healthbox_player(True).save(BI / "healthbox_singles_player.png", hb)
    healthbox_player(False).save(BI / "healthbox_doubles_player.png", hb)
    healthbox_opponent(False).save(BI / "healthbox_singles_opponent.png", hb)
    healthbox_opponent(True).save(BI / "healthbox_doubles_opponent.png", hb)
    healthbox_safari().save(BI / "healthbox_safari.png", hb)
    # B_HP_PERCENTAGE_DISPLAY's taller opponent box: the player's shape.
    big = IdxCanvas(128, 64)
    big.paste(healthbox_opponent(False), 0, 0)
    big.save(BI / "healthbox_singles_opponent_large.png", hb)
    expbar_png().save(BI / "expbar.png", hb)
    misc_png().save(BI / "misc.png", hb)
    for i, name in enumerate(["status", "status2", "status3", "status4"]):
        status_png(i).save(BI / f"{name}.png", hb)
    frame_end(False).save(BI / "healthbox_doubles_player_frameend.png", hb)
    frame_end(True).save(BI / "healthbox_doubles_player_frameend_bar.png", hb)
    frame_end(False).save(BI / "healthbox_doubles_opponent_frameend.png", hb)
    frame_end(True).save(BI / "healthbox_doubles_opponent_frameend_bar.png", hb)
    ball_status_bar_png().save(BI / "ball_status_bar.png", hb)
    enemy_shadow_png().save(BI / "enemy_mon_shadow.png", hb)
    enemy_shadows_sized_png().save(BI / "enemy_mon_shadows_sized.png", hb)

    hpbar_png().save(BI / "hpbar.png", bar)
    hpbar_anim_png().save(BI / "hpbar_anim.png", bar)
    bar_left_cap().save(BI / "misc_frameend.png", bar)
    ball_display_png().save(BI / "ball_display.png", bar)
    ball_caught_png().save(BI / "ball_caught_indicator.png", bar)


if __name__ == "__main__":
    main()
