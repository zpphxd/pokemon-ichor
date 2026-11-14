#!/usr/bin/env python3
"""Paint the battle's small sprites as pottery: the ability pop-up, the
last-used-ball and move-info windows, the Apotheosis trigger and its mark.

* The ability pop-up is a clay plaque like the healthboxes: a black-glaze
  band carries the Pokemon's name in parchment, a parchment band carries the
  ability (or item) in ink, between two meander strips. The game prints the
  name at (8 or 16, 0) with color 7 and shadow 1, the ability at y 12 with
  color 9 and shadow 1, and restores the area under the ability from this art.
* The last-used-ball window (R) and the move-info window (L) share the
  pop-up's palette. ArrowsChangeColorLastBallCycle hides the cycle arrows by
  copying index 13 (the body) into 8 and 9, and shows them by copying 11 and
  10, so those slots keep their roles.
* Mega Evolution is Apotheosis in Ichor, and its key stone is the Omphalos,
  Delphi's navel stone with its net of knotted wool. The trigger shows the
  stone dim (frame 1) or lit with golden ichor (frame 2). The mega mark beside
  the level is a little omphalos too. Z-Move, Dynamax, Tera and Ultra Burst
  triggers are untouched: those gimmicks are off in Ichor.

Usage: python3 tools/ichor/art/ui_battle_sprites.py
"""
from ui_battle_lib import (
    BI, CLAY, CLAY_DARK, CLAY_LIGHT, GLAZE, GOLD, GOLD_DARK, INK, MARBLE, MARBLE_DARK,
    MARBLE_LIGHT, PARCHMENT, PARCH_SHADE, TRANSPARENT, IdxCanvas, meander_v, text_3x5,
    write_jasc,
)

POP = {"shadow": 1, "incised": 2, "clay": 3, "light": 4, "glaze": 5, "parch": 7,
       "arrow_edge": 8, "ink": 9, "key": 10, "outline": 11, "gold": 12, "body": 13,
       "rim": 14, "shade": 15}
POPUP_PAL = [
    (0, 176, 88),    # 0  transparent
    CLAY,            # 1  text shadow (both bands)
    CLAY_DARK,       # 2  incised lines
    CLAY,            # 3  plaque clay
    CLAY_LIGHT,      # 4
    INK,             # 5  name band (black glaze); MOVE INFO letters
    GLAZE,           # 6
    PARCHMENT,       # 7  name text, ability band, key caps
    INK,             # 8  cycle arrow edge
    INK,             # 9  ability text, cycle arrow
    CLAY_DARK,       # 10 key letters; arrow edge when shown
    INK,             # 11 window outline; arrow when shown
    GOLD,            # 12
    CLAY_LIGHT,      # 13 window body (arrows hidden in this color)
    CLAY,            # 14 window rim
    PARCH_SHADE,     # 15
]


# --- Ability pop-up (128x32: two 64x32 sprites) -----------------------------
def ability_popup():
    c = IdxCanvas(128, 32)
    x0, x1, y0, y1 = 0, 103, 0, 27
    clay, inc = POP["clay"], POP["incised"]
    c.rect(x0, y0, x1, y1, clay)
    c.rect(x0 + 6, y0 + 2, x1 - 6, y1 - 2, inc)
    c.rect(x0 + 7, 3, x1 - 7, 12, POP["glaze"])     # name band
    c.rect(x0 + 7, 14, x1 - 7, y1 - 3, POP["parch"])  # ability band
    meander_v(c, x0 + 1, y0 + 1, y1 - 1, POP["ink"], clay, phase=6)
    meander_v(c, x1 - 5, y0 + 1, y1 - 1, POP["ink"], clay, phase=6, mirror=True)
    for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        c.set(x, y, 0)
    return c


# --- Small windows: R (last ball) and L (move info) --------------------------
def window(c, x0, y0, x1, y1):
    """A clay tablet: ink outline, clay rim, incised line, light-clay body."""
    c.rect(x0 + 1, y0, x1 - 1, y1, POP["outline"])
    c.rect(x0, y0 + 1, x1, y1 - 1, POP["outline"])
    c.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, POP["rim"])
    c.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, POP["key"])
    c.rect(x0 + 3, y0 + 3, x1 - 3, y1 - 3, POP["body"])


def key_cap(c, cx, y, letter):
    """A parchment key with its letter, 10x8, centered on cx."""
    x0 = cx - 5
    c.rect(x0 + 1, y, x0 + 8, y + 7, POP["parch"])
    c.rect(x0, y + 1, x0 + 9, y + 6, POP["parch"])
    c.hline(x0 + 1, x0 + 8, y + 7, POP["shade"])
    text_3x5(c, cx - 1, y + 1, letter, POP["key"])


def last_ball_window(letter, cycle):
    c = IdxCanvas(32, 64 if cycle else 32)
    top = 16 if cycle else 0
    bottom = top + (35 if cycle else 30)
    window(c, 0, top, 25, bottom)
    key_cap(c, 13, top + 2, letter)
    if cycle:
        # Left and right arrows either side of the ball, for cycling balls.
        arrows = {"a": POP["arrow_edge"], "b": POP["ink"]}
        c.blit(6, bottom - 5, ["..ab", ".abb", "..ab"], arrows)
        c.blit(16, bottom - 5, ["ba..", "bba.", "ba.."], arrows)
    return c


def move_info_window(letter):
    c = IdxCanvas(32, 32)
    window(c, 0, 0, 31, 26)
    key_cap(c, 16, 2, letter)
    text_3x5(c, 8, 11, "MOVE", POP["glaze"])
    text_3x5(c, 8, 17, "INFO", POP["glaze"])
    return c


# --- The Omphalos ------------------------------------------------------------
# A beehive stone wrapped in a net of knotted fillets, on a low plinth.
OMPHALOS = [
    "....#####....",
    "...#hhsss#...",
    "..#hsnsnss#..",
    ".#hsnsssnss#.",
    ".#snsnsnsns#.",
    "#hsssnsnsss##",
    "#snsnsssnsns#",
    "#ssnsssssnss#",
    "#############",
    ".#ppppppppp#.",
    ".###########.",
]

TRIGGER_OFF = {"bg": (0, 0, 0), "ink": INK, "rim": CLAY_DARK, "tab": CLAY, "tab_hi": CLAY_LIGHT,
               "h": MARBLE_LIGHT, "s": MARBLE, "n": MARBLE_DARK, "p": CLAY_DARK, "glow": CLAY_LIGHT}
TRIGGER_ON = {"bg": (0, 0, 0), "ink": INK, "rim": CLAY_DARK, "tab": GOLD_DARK, "tab_hi": GOLD,
              "h": (248, 240, 192), "s": GOLD, "n": GOLD_DARK, "p": CLAY_DARK, "glow": (248, 232, 160)}
TRIG_IDX = {"ink": 1, "rim": 2, "tab": 3, "tab_hi": 4, "h": 5, "s": 6, "n": 7, "p": 8, "glow": 9}


def trigger_frame(lit):
    """32x32. The plaque tucks under the healthbox's left end; its left side
    slants like the vanilla tab so it reads as a button pointing at the box."""
    c = IdxCanvas(32, 32)
    top, bottom = 3, 16
    for y in range(top, bottom + 1):
        left = 1 + (bottom - y) // 2           # slanted leading edge
        c.hline(left, 26, y, TRIG_IDX["tab"])
        c.set(left, y, TRIG_IDX["ink"])
    c.hline(1 + (bottom - top) // 2, 26, top, TRIG_IDX["ink"])
    c.hline(1, 26, bottom, TRIG_IDX["ink"])
    c.hline(2 + (bottom - top) // 2, 25, top + 1, TRIG_IDX["tab_hi"])
    # The healthbox covers the plaque from x 22, so the stone sits left of it.
    c.blit(6, 4, OMPHALOS, {"#": TRIG_IDX["ink"], "h": TRIG_IDX["h"], "s": TRIG_IDX["s"],
                            "n": TRIG_IDX["n"], "p": TRIG_IDX["p"]})
    if lit:
        for x, y in ((4, 1), (12, 0), (20, 1), (3, 6), (21, 6)):
            c.set(x, y, TRIG_IDX["glow"])
    return c


def trigger_palette(colors):
    pal = [(0, 0, 0)] * 16
    pal[0] = TRANSPARENT
    for name, i in TRIG_IDX.items():
        pal[i] = colors[name]
    return pal


def mega_trigger():
    """Frame 1 (tiles 0-15) is the dim stone, frame 2 (16-31) the lit one.
    One palette serves both, so the two frames use separate slots."""
    off, on = trigger_frame(False), trigger_frame(True)
    lit = ["tab", "tab_hi", "h", "s", "n", "glow"]       # own slots 9-14 when lit
    on_shift = {TRIG_IDX[name]: 9 + k for k, name in enumerate(lit)}
    for row in on.px:
        for x, v in enumerate(row):
            row[x] = on_shift.get(v, v)
    c = IdxCanvas(32, 64)
    c.paste(off, 0, 0)
    c.paste(on, 0, 32)
    pal = trigger_palette(TRIGGER_OFF)
    for name in lit:
        pal[on_shift[TRIG_IDX[name]]] = TRIGGER_ON[name]
    return c, pal


OMPHALOS_SMALL = [
    "..###..",
    ".#hss#.",
    "#hnsns#",
    "#snsns#",
    "#######",
    ".#ppp#.",
    ".#####.",
]


def mega_indicator():
    c = IdxCanvas(8, 16)
    c.blit(0, 8, OMPHALOS_SMALL, {"#": 1, "h": 2, "s": 3, "n": 4, "p": 5})
    pal = [TRANSPARENT, INK, (248, 240, 192), GOLD, GOLD_DARK, CLAY_DARK] + [(0, 0, 0)] * 10
    return c, pal


def main():
    pop = POPUP_PAL
    write_jasc(BI / "ability_pop_up.pal", pop)
    ability_popup().save(BI / "ability_pop_up.png", pop)
    for side in ("l", "r"):
        letter = side.upper()
        last_ball_window(letter, False).save(BI / f"last_used_ball_{side}.png", pop)
        last_ball_window(letter, True).save(BI / f"last_used_ball_{side}_cycle.png", pop)
        move_info_window(letter).save(BI / f"move_info_window_{side}.png", pop)
    c, pal = mega_trigger()
    c.save(BI / "mega_trigger.png", pal)
    c, pal = mega_indicator()
    c.save(BI / "mega_indicator.png", pal)


if __name__ == "__main__":
    main()
