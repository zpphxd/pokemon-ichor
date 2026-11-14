#!/usr/bin/env python3
"""Shared painters for Ichor's "reading" screens: the Pokedex codex, the
Pithos, the naming tablet, options and save.

They extend ui_menus_lib.py (the master palette, the indexed Canvas, tile
cutting) with what these screens add:
  - the game's own fonts, so lettering baked into art (tab labels, menu
    entries) matches the text the engine prints beside it
  - codex pieces: bronze corner caps, parchment leaves, ink cartouches
"""
import re
from pathlib import Path

import numpy as np
from PIL import Image

from ui_menus_lib import *  # noqa: F401,F403  (re-exported for the screen scripts)
from ui_menus_lib import ROOT, Canvas, MEANDER

# Bronze, for the codex's corner caps and clasps (multiples of 8).
BRONZE_DARK = (96, 56, 24)
BRONZE = (152, 96, 40)
BRONZE_LIGHT = (208, 152, 72)
BRONZE_GLINT = (248, 216, 136)
GLAZE = (64, 40, 32)            # black glaze, not quite ink
RING = (160, 72, 40)            # the throwing ring on the clay field
PARCH_LIGHT = (248, 240, 216)   # the lit edge of a leaf, and light text


# --- The game's fonts --------------------------------------------------------
_FONT_ARRAYS = {
    "normal": ("latin_normal", "gFontNormalLatinGlyphWidths"),
    "small": ("latin_small", "gFontSmallLatinGlyphWidths"),
    "short": ("latin_short", "gFontShortLatinGlyphWidths"),
    "narrow": ("latin_narrow", "gFontNarrowLatinGlyphWidths"),
}
_font_cache = {}
_charmap = None


def _load_charmap():
    global _charmap
    if _charmap is None:
        _charmap = {}
        for line in (ROOT / "charmap.txt").read_text(encoding="utf-8").splitlines():
            line = line.split("@")[0].rstrip()
            m = re.match(r"^'(\\?.)'\s*=\s*([0-9A-Fa-f]{2})$", line)
            if m:
                _charmap.setdefault(m.group(1).replace("\\'", "'"), int(m.group(2), 16))
    return _charmap


def _load_font(name):
    if name not in _font_cache:
        png, array = _FONT_ARRAYS[name]
        img = np.array(Image.open(ROOT / f"graphics/fonts/{png}.png"))
        src = (ROOT / "src/fonts.c").read_text(encoding="utf-8")
        m = re.search(re.escape(array) + r"\[\]\s*=\s*\{(.*?)\};", src, re.S)
        widths = [int(x) for x in re.findall(r"\d+", m.group(1))]
        _font_cache[name] = (img, widths)
    return _font_cache[name]


def text_width(s, font="normal"):
    img, widths = _load_font(font)
    cm = _load_charmap()
    return sum(widths[cm[ch]] for ch in s)


def draw_text(c, x, y, s, fg, shadow=None, font="normal"):
    """Letter s onto canvas c with the game's font. The glyph cell's top-left
    goes at (x, y), as the engine places a printed string. fg and shadow are
    canvas values; shadow None leaves the shadow pixels unpainted."""
    img, widths = _load_font(font)
    cm = _load_charmap()
    for ch in s:
        code = cm[ch]
        cell = img[(code // 16) * 16:(code // 16) * 16 + 16, (code % 16) * 16:(code % 16) * 16 + 16]
        w = widths[code]
        for gy in range(16):
            for gx in range(w):
                v = cell[gy, gx]
                if v == 1:
                    c.px(x + gx, y + gy, fg)
                elif v == 2 and shadow is not None:
                    c.px(x + gx, y + gy, shadow)
        x += w
    return x


# --- Painters -----------------------------------------------------------------
def clay_field(c, x, y, w, h, clay, ring, period=8):
    """Terracotta with a throwing ring on the last row of every tile."""
    c.rect(x, y, w, h, clay)
    for yy in range(y, y + h):
        if yy % period == period - 1:
            c.hline(x, yy, w, ring)


def meander_band(c, x, y, w, ink, ground, rule_top=None, rule_bottom=None):
    """A 7 px band: a rule, the 5 px meander, a rule."""
    c.hline(x, y, w, rule_top if rule_top is not None else ink)
    c.rect(x, y + 1, w, 5, ground)
    c.meander(x, y + 1, w, ink)
    c.hline(x, y + 6, w, rule_bottom if rule_bottom is not None else ink)


def rays_band(c, x, y, w, ink, ground):
    """The foot of a vase: black rays rising from an ink rule, 8 px tall."""
    c.rect(x, y, w, 8, ground)
    c.hline(x, y, w, ink)
    for x0 in range(x, x + w, 8):
        for j, half in enumerate([0, 0, 1, 1, 2, 3]):
            c.hline(x0 + 4 - half, y + 2 + j, 2 * half + 1, ink)
    c.hline(x, y + 7, w, ink)


def bevel_rect(c, x, y, w, h, face, light, shade, outline=None):
    """A flat face lit from the top left: light on the top and left edges,
    shade on the bottom and right, an optional outline round it all."""
    if outline is not None:
        c.frame(x, y, w, h, outline)
        x, y, w, h = x + 1, y + 1, w - 2, h - 2
    c.rect(x, y, w, h, face)
    c.hline(x, y, w, light)
    c.vline(x, y, h, light)
    c.hline(x, y + h - 1, w, shade)
    c.vline(x + w - 1, y, h, shade)


# A bronze corner cap: an 8x8 angle bracket riveted to a codex board, lit from
# the top left. 'o' outline, 'd' dark bronze, 'b' bronze, 'l' light, 'g' glint,
# 'r' the rivet's shadow. Drawn for the top-left corner; flip it for the rest.
BRONZE_CORNER = [
    "oooooooo",
    "ogllllld",
    "olbbbbbd",
    "olbrbddo",
    "olbbdo  ",
    "olbdo   ",
    "olbo    ",
    "oddo    ",
]


def bronze_corner(c, x, y, key, flip_h=False, flip_v=False):
    rows = BRONZE_CORNER
    if flip_v:
        rows = rows[::-1]
    if flip_h:
        rows = [r[::-1] for r in rows]
    # Light always comes from the top left, so a flipped cap swaps its lit
    # and shaded strokes back.
    k = dict(key)
    if flip_h or flip_v:
        lit, dark = k["l"], k["d"]
        if flip_h and flip_v:
            k["l"], k["d"] = dark, lit
            k["g"] = k["b"]
    c.grid(x, y, rows, k)


def cartouche(c, x, y, w, h, ink, face=None):
    """An ink cartouche with clipped corners (the summary's section labels)."""
    c.rect(x + 1, y, w - 2, h, ink)
    c.rect(x, y + 1, w, h - 2, ink)
    if face is not None:
        c.rect(x + 1, y + 1, w - 2, h - 2, face)


def check_tiles(n, limit, what):
    assert n <= limit, f"{what}: {n} tiles, the engine loads {limit}"
    print(f"{what}: {n}/{limit} tiles")
