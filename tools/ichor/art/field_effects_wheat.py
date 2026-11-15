#!/usr/bin/env python3
"""The wheat rustle: Eleusa's tall-grass field effect, in gold.

Eleusa's standing wheat (gTileset_Eleusa's `wheat`) is MB_TALL_GRASS, so the
player rustles through it with the tall-grass effect. The slice's effect is cut
from aethos's green barley (field_effects.py); this one is cut the same way from
the wheat's own full-interior metatile (0x22E, shape key 1|11111111), so the
tuft over the player's feet matches the field pixel for pixel, and it plays the
slice's rustle (the stalks whip apart, grain and chaff fly up and settle) in the
wheat's five golds.

FldEff_TallGrass (src/field_effect_helpers.c) picks it on any map whose
secondary tileset is gTileset_Eleusa, with its own palette (FLDEFF_PAL_TAG_WHEAT).

Writes, with --write:
  graphics/field_effects/pics/tall_grass_wheat.png   5 frames of 16x16, as tall_grass.png
  graphics/field_effects/palettes/wheat.pal
and with --preview PATH, every frame at 6x over the wheat it plays on.

Usage: /usr/bin/python3 tools/ichor/art/field_effects_wheat.py [--write] [--preview PATH]
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import field_effects as F  # noqa: E402
from sprites_lib import upscale  # noqa: E402

WHEAT_TILE = 0x22E

# The wheat's five colors (eleusa_lib's field group, as the compiled tileset draws
# them), lightest first, then the chaff. Index roles mirror GENERAL_1's barley so the
# slice's rustle frames (letters a c e d b o) read the same.
WHEAT = F.RawPal([
    (112, 192, 160),   # 0 transparent
    (248, 224, 136),   # 1 straw light (the ear's highlight)
    (240, 192, 64),    # 2 wheat gold
    (200, 144, 40),    # 3 ochre
    (160, 104, 32),    # 4 stalk brown
    (96, 56, 24),      # 5 dark between the stalks
    (248, 240, 216),   # 6 chaff, pale
    (248, 224, 136), (248, 224, 136), (248, 224, 136), (248, 224, 136), (248, 224, 136),
    (248, 224, 136), (248, 224, 136), (248, 224, 136), (248, 224, 136),
])
# letters in field_effects.tall_grass_frames: a dark, c shade, e mid, d light (the
# blades), b grain, o grain ochre. Over gold the thrown grain must still read, so it
# flies as pale chaff and dark husks.
LEGEND = {"a": 5, "c": 4, "e": 3, "d": 1, "b": 6, "o": 5, "g": 2, "h": 4, "G": 1,
          "w": 6, "s": 6, "l": 6, "F": 6}


def eleusa_renderer():
    R = F.R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R.Renderer(R.Tileset(R.resolve_tileset("aethos", syms)),
                      R.Tileset(R.resolve_tileset("gTileset_Eleusa", syms)))


def frames():
    """The slice's five tall-grass frames, cut from the wheat instead of the barley."""
    saved = (F._RENDERER, F.GENERAL_1, F.G1, F.TALL_GRASS)
    try:
        F._RENDERER = eleusa_renderer()
        F.GENERAL_1, F.G1, F.TALL_GRASS = WHEAT, LEGEND, WHEAT_TILE
        return F.tall_grass_frames()
    finally:
        F._RENDERER, F.GENERAL_1, F.G1, F.TALL_GRASS = saved


def preview(arr, path, k=6):
    r = eleusa_renderer()
    ground = Image.fromarray(r.metatile(WHEAT_TILE)[0]).convert("RGBA")
    im = F.to_rgba(arr, WHEAT)
    n = arr.shape[1] // 16
    out = Image.new("RGBA", (n * 18, 16), (232, 224, 200, 255))
    for f in range(n):
        bg = ground.copy()
        bg.alpha_composite(im.crop((f * 16, 0, f * 16 + 16, 16)))
        out.alpha_composite(bg, (f * 18, 0))
    upscale(out, k).save(path)


def main():
    args = sys.argv[1:]
    arr = F.strip(frames())
    if "--write" in args:
        F.save(arr, WHEAT, "tall_grass_wheat.png")
        WHEAT.write_jasc(os.path.join(F.PALS, "wheat.pal"))
        print("graphics/field_effects/pics/tall_grass_wheat.png, graphics/field_effects/palettes/wheat.pal")
    if "--preview" in args:
        p = args[args.index("--preview") + 1]
        preview(arr, p)
        print(p)


if __name__ == "__main__":
    main()
