"""Small field objects for Ichor (16x16, one frame), drawn in the cast palette.

Usage:
    python3 tools/ichor/art/sprites_objects.py [--write] [--preview DIR]

--write    writes graphics/object_events/pics/misc/ichor/<name>.png (16x16,
           4bpp indexed, the ichor_cast palette embedded)
--preview  writes DIR/sprites_objects.png (each object at 4x on the summit's
           grass and slab colors) and an 8x pixel grid per object

The objects load under OBJ_EVENT_PAL_TAG_ICHOR_CAST, the palette the cast
walkers already use, so placing one costs no extra OBJ palette slot on a map
that already shows the cast. Registration follows design/phase1/SPRITES_npc.md,
with the 16x16 inanimate settings of the vanilla Fossil object.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from sprites_npc import CAST_PAL, CAST_LEGEND  # noqa: E402
from PIL import Image  # noqa: E402

W = H = 16
OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/misc/ichor")

# The Titanborn's clay tablet, dropped face up on the grass below the
# stylobate (Kronion Hill, beat 5). Unfired terracotta lit from the top left:
# skin_l on the lit rim, skin_d for the face, umber and red_d for the shaded
# side and the slab's thickness. The sickle (the Harpe) is pressed into the
# top left corner in brown; the scratched list of places runs beside and
# under it in red_d, one line struck through (Kalliste, crossed out). The
# bottom right corner is chipped.
TABLET = [
    "................",
    "................",
    "................",
    ".....bbbbbbb....",
    "...bSSSSSSSSsb..",
    "..bSssbbsssssb..",
    "..bSsbssbssrsb..",
    "..bSsbssssrssb..",
    "..bSssbbssssub..",
    "..bSsssrrrrsub..",
    "..bSsssssssuub..",
    "..bsrsrrrssub...",
    "...buuuuuuuub...",
    "....brrrrrrb....",
    ".....bbbbbb.....",
    "................",
]

# A town's travel herm (design/SYSTEMS.md §4), 16x32, stood by every town's
# main entrance. It has to read at a glance as "not a signpost": Hermes's
# winged cap in bright bronze on top, a bearded marble head, a laurel garland
# with a crimson ribbon, and a bronze caduceus down the pillar's face, on a
# plinth. Lit from the top left like the cast (linen_l lit, linen_d and slate
# in shade).
GREAT_HERM = [
    "................",
    "......kkkk......",
    ".kk..kOOOOk..kk.",
    "kLLk.kOOOOk.kLLk",
    ".kLlkkoooookLlk.",
    "..kkkkoooookkk..",
    "...kkkkkkkkkk...",
    "....kLLLLLLk....",
    "....kLkLLkLk....",
    "....kLLLLLlk....",
    "....kLlkklLk....",
    "....kllllllk....",
    "....ktlllltk....",
    "...kgkklllkgk...",
    "..kggcgkkkgcggk.",
    "...kgggLLLgggk..",
    "....kLgggggLk...",
    "....kLLLcLLlk...",
    "....kLLLcLLlk...",
    "....kLLoOoLlk...",
    "....kLLLoLLlk...",
    "....kLLoLoLlk...",
    "....kLLLoLLlk...",
    "....kLLoLoLlk...",
    "....kLLLoLLlk...",
    "....kLLLLLLtk...",
    "....kLLLLLltk...",
    "...kkkkkkkkkkk..",
    "...kLLLLLLLLtk..",
    "...kllllllllttk.",
    "....kkkkkkkkkk..",
    "................",
]

# The herm's little plaque: a marble board in a bronze frame on a wooden post,
# with three lines of lettering. Its sign names the herm a travel
# stop (data/scripts/ichor_herms.pory).
HERM_PLAQUE = [
    "................",
    "................",
    "...kkkkkkkkkk...",
    "...koOOOOOOok...",
    "...kLLLLLLLLk...",
    "...kLtLttLtLk...",
    "...kLLLLLLLLk...",
    "...kLttLtttLk...",
    "...kLLLLLLLLk...",
    "...kLtttLttlk...",
    "...kllllllllk...",
    "...kkkkkkkkkk...",
    "......kbbk......",
    "......kbbk......",
    ".....kkbbkk.....",
    "................",
]

OBJECTS = {
    "tablet": TABLET,
    "great_herm": GREAT_HERM,
    "herm_plaque": HERM_PLAQUE,
}


def build(rows):
    H = len(rows)
    assert H in (16, 32), f"{len(rows)} rows"
    arr = np.zeros((H, W), np.int32)
    for y, row in enumerate(rows):
        assert len(row) == W, f"row {y} is {len(row)} px: {row!r}"
        for x, ch in enumerate(row):
            if ch != ".":
                arr[y, x] = CAST_PAL[CAST_LEGEND[ch]]
    return arr


def preview(arrs, k=4):
    """Each object on the summit's grass and on a pale slab, upscaled."""
    grounds = [(144, 152, 72), (216, 200, 160)]
    tall = max(a.shape[0] for a in arrs.values())
    out = Image.new("RGBA", (len(arrs) * (W * len(grounds) + 4), tall), (232, 224, 200, 255))
    x = 0
    for arr in arrs.values():
        for g in grounds:
            tile = Image.new("RGBA", (W, arr.shape[0]), g + (255,))
            tile.alpha_composite(to_rgba(arr, CAST_PAL))
            out.alpha_composite(tile, (x, 0))
            x += W
        x += 4
    return upscale(out, k)


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    arrs = {name: build(rows) for name, rows in OBJECTS.items()}
    if "--write" in args:
        for name, arr in arrs.items():
            save_indexed(arr, CAST_PAL, os.path.join(OUT_DIR, name + ".png"))
    if pv:
        os.makedirs(pv, exist_ok=True)
        preview(arrs).save(os.path.join(pv, "sprites_objects.png"))
        for name, arr in arrs.items():
            grid_preview(to_rgba(arr, CAST_PAL), 8).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
