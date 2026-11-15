"""Trainer front pics for Act II, batch 2 (beats 35-37): the Fowler class.

FOWLER is the bird-catchers of the Kopais marsh (SCRIPT.md Part 3): a lean man
or woman in a short undyed tunic and a broad straw hat, a folded net over one
shoulder, a reed decoy-pipe at the lips, and a little wicker quail cage at the
hip. Two pics, `Pic: Fowler M` (Gorgidas) and `Pic: Fowler F` (Timoxena), each
a 64x64, 16-color Gen 3 trainer pic in the slice's house style
(sprites_classes.py): a 3/4 view facing the player's side (screen left), lit
from the top left, the palette embedded in the PNG. See design/phase3/SPRITES.md.

Usage: python3 tools/ichor/art/sprites_act2_b2_classes.py [NAME ...] [--write] [--preview DIR]

--write   writes the indexed PNGs to graphics/trainers/front_pics/ and, when no
          NAME is given, the portrait sheet design/phase3/img/portraits_batch2.png
--preview writes the 3x sheet, 6x singles and pixel grids to DIR
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, Mat, Fig, save_indexed, to_rgba, upscale, palette_report, grid_preview  # noqa: E402,E501
from sprites_classes import INK, SKIN_SUN, render, skin_mat, load_pic, battle_tile, FRONT  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402


def _palette(band, lin):
    return Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("hair", (80, 48, 32)),
        ("straw_l", (248, 216, 112)), ("straw_m", (216, 160, 64)), ("straw_d", (144, 96, 40)),
        ("lin_l", lin[0]), ("lin_m", lin[1]), ("lin_d", lin[2]),
        ("twine", (112, 96, 80)),
        ("band", band),
        ("reed_l", (176, 184, 96)), ("reed_d", (96, 112, 48)),
    ])


def _net_mesh(f, pid):
    """A diamond mesh of dark twine over the folded net, inside its edge."""
    m = f.pid == pid
    pts = []
    for y in range(1, f.h - 1):
        for x in range(1, f.w - 1):
            if not m[y, x] or not (m[y - 1, x] and m[y + 1, x] and m[y, x - 1] and m[y, x + 1]):
                continue
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                pts.append((x, y))
    f.pxs(pts, "twine")


# The quail cage: a domed wicker cage, three gold ribs in front of a plump
# brown quail (speckled, facing you, its eye a dot), the wicker's shadowed back
# wall behind it, a woven base, hung by a cord loop. Legend: k ink, S/s/d
# straw, q quail, Q speckle.
_CAGE = [
    "....kkk....",
    "...k...k...",
    "..kkkkkkk..",
    ".kSsSsSsSk.",
    "kSdddSdddSk",
    "kSdqdSdddSk",
    "kSqkqSqqdSk",
    "kSqqQSqQqSk",
    "kSdqqSqqdSk",
    "kSsSsSsSsSk",
    ".kkkkkkkkk.",
]
_CAGE_LEGEND = {"k": "ink", "S": "straw_l", "s": "straw_m", "d": "straw_d", "q": "hair", "Q": "lin_l"}


def fowler(female=False):
    pal = _palette((88, 144, 200) if female else (184, 72, 48),
                   [(240, 232, 208), (208, 192, 152), (152, 136, 104)] if female
                   else [(224, 208, 168), (184, 160, 120), (128, 112, 80)])
    skin = skin_mat("hair")
    straw = Mat(["straw_d", "straw_m", "straw_l"], outline="hair", wx=0.8, wy=0.35, cuts=[0.3, 0.7])
    tunic = Mat(["lin_d", "lin_m", "lin_l"], outline="hair", wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    net = Mat(["lin_d", "lin_m"], outline="hair", wx=0.7, wy=0.4, cuts=[0.6])
    hairm = Mat(["hair"], outline="ink")
    lea = Mat(["hair"])
    band = Mat(["band"])
    f = Fig(pal)

    # legs: lean, the near one forward, sandals
    hem = 47 if female else 44
    f.poly([(27, hem), (31, hem), (30, 50), (29, 57), (25, 57), (26, 50)], skin, group=100)
    f.poly([(35, hem), (39, hem), (40, 50), (41, 57), (38, 57), (36, 50)], skin, group=101)
    f.poly([(23, 57), (30, 57), (30, 61), (22, 61)], lea)
    f.poly([(37, 57), (43, 57), (44, 61), (37, 61)], lea)
    if female:
        # her hair, long behind her under the hat
        f.poly([(35, 12), (42, 12), (44, 18), (43, 24), (39, 23), (36, 19)], hairm, group=30)
    f.rect(29, 17, 34, 25, skin, group=400)
    # the short undyed tunic, belted
    body = f.poly([(26, 24), (39, 24), (41, 33), (42, hem), (35, hem + 1), (24, hem), (25, 33)], tunic)
    f.rect(23, 33, 44, 34, band, clip=body, noline=True)
    f.shade_poly([(31, 36), (32, 36), (32, hem), (31, hem)], 0.45)
    f.shade_poly([(37, 36), (38, 36), (40, hem), (39, hem)], 0.45)
    f.shade_poly([(25, 35), (28, 35), (27, hem), (24, hem)], -0.3)
    # the net, folded over the far shoulder and hanging down the back
    net_id = f.poly([(34, 22), (41, 21), (46, 25), (48, 32), (48, 40), (46, 45), (43, 42), (41, 46),
                     (39, 41), (38, 34), (36, 28)], net, group=70)
    if female:
        # far arm up, holding the decoy quail's cage out to show you
        f.thick_line([(39, 25), (45, 29), (49, 24)], 4, skin, group=300)
    else:
        # far arm down at his side, hand on the net's fold
        f.thick_line([(39, 25), (42, 32), (43, 39)], 4, skin, group=300)
    # near arm raised, the hand at the pipe
    f.thick_line([(27, 25), (21, 31)], 5, skin, group=200)
    f.thick_line([(21, 31), (23, 24)], 4, skin, group=201)
    # the broad straw hat with a peaked crown (Boeotia's tholia, the hat of the
    # Tanagra figurines; the player's petasos is domed): a brim wider than the
    # shoulders, a band at the crown's foot
    f.ellipse((13, 5, 51, 11), straw, group=800)
    f.poly([(24, 7), (29, 2), (32, 0), (34, 0), (37, 2), (42, 7)], straw, group=810)
    f.rect(24, 5, 42, 6, band, clip=810, noline=True)

    _net_mesh(f, net_id)
    # straw weave on the brim and crown
    for x in range(16, 49, 3):
        f.px(x, 8 if x % 2 else 9, "straw_m")
    for x in (30, 33, 36):
        f.px(x, 3, "straw_m")
    # head: in the brim's shadow, eyes on the reeds; the pipe at the lips
    if female:
        f.patch(24, 11, [
            ".kHHHHHHHHHHHHk...",
            "kHHHHHHHHHHhhHHk..",
            "kHkkkLLLLkkkMhHHk.",
            "kLLWkLLLLkWLMDhHk.",
            "kLLLLLLLLLLLMDhHk.",
            "kLLLLLDLLLLMMhHHk.",
            ".kLLLDDLLLMMMhHk..",
            ".kLLLLLLLLMMhHHk..",
            "..kLLLLLLMMkhHk...",
            "...kkLLLMMkkhk....",
            ".....kkkkk..k.....",
        ], {"k": "ink", "H": "hair", "h": "straw_d", "L": "skin_l", "M": "skin_m", "D": "skin_d",
            "W": "lin_l"})
    else:
        f.patch(24, 11, [
            ".kHHHHHHHHHHHHk...",
            "kHHHHHHHHHHHHHHk..",
            "kHkkkLLLkkkMHHHk..",
            "kLLWkLLLkWLMDHHk..",
            "kLLLLLLLLLLMDHk...",
            "kLLLLDLLLLMMMHk...",
            ".kLLDDLLLMMMDk....",
            ".kLLLLLLLLMMk.....",
            "..kLLLLLLMMk......",
            "...kLLLLMMk.......",
            "....kkkkkk........",
        ], {"k": "ink", "H": "hair", "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": "lin_l"})
    # the reed decoy-pipe from the lips down to the near hand
    f.patch(18, 16, [
        ".......kk",
        "......kGk",
        ".....kGgk",
        "....kGgk.",
        "...kGgk..",
        "..kGgk...",
        ".kGgk....",
        "kGgk.....",
        "kkk......",
    ], {"k": "ink", "G": "reed_l", "g": "reed_d"})
    f.patch(19, 20, [".bbbb.", "bLLLLb", "bLbLMb", "bLLMMb", ".bbbb."],
            {"b": "hair", "L": "skin_l", "M": "skin_m"})
    if female:
        # her braid over the near shoulder, tied with the band's color
        f.patch(25, 20, [
            ".kk.",
            "kHhk",
            "khHk",
            "kHhk",
            "khHk",
            "kHhk",
            "khHk",
            ".kBk",
            ".kBk",
            "kHhk",
            ".kk.",
        ], {"k": "ink", "H": "hair", "h": "straw_d", "B": "band"})
        # the cage held up in the far hand
        f.patch(44, 13, _CAGE, _CAGE_LEGEND)
        f.patch(46, 22, [".kkk.", "kLLMk", "kLMMk", ".kkk."], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    else:
        f.patch(41, 38, [".kkk.", "kLLMk", "kLMMk", ".kkk."], {"k": "hair", "L": "skin_l", "M": "skin_m"})
        # the quail cage hung at the near hip from the belt
        f.patch(15, 33, _CAGE, _CAGE_LEGEND)
        f.line([(24, 34), (21, 34)], "band")
    return f, pal


CLASSES = {
    "fowler_m": lambda: fowler(False),
    "fowler_f": lambda: fowler(True),
}

SHEET = os.path.join(ROOT, "design/phase3/img/portraits_batch2.png")
REFS = ("shepherd", "harvester", "goatherd", "vintner", "maenad")


def tiles_sheet(images, cols):
    tiles = [battle_tile(im) for im in images]
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGBA", (96 * cols, 72 * rows), (232, 224, 200, 255))
    for i, t in enumerate(tiles):
        out.alpha_composite(t, (96 * (i % cols), 72 * (i // cols)))
    return out


def contact_sheet(figs, k=3):
    """Four Act I and batch 1 portraits on the top row for scale and style,
    then the batch's two, on the grass battle background, labelled."""
    refs = [load_pic(os.path.join(FRONT, n + ".png")) for n in REFS]
    news = [to_rgba(arr, pal) for arr, pal in figs.values()]
    cols = len(REFS)
    pad = [Image.new("RGBA", (64, 64))] * (-len(refs) % cols)
    big = upscale(tiles_sheet(refs + pad + news, cols), k)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.load_default(size=16)
    except TypeError:
        font = ImageFont.load_default()
    names = list(REFS) + [""] * len(pad) + list(figs)
    for i, n in enumerate(names):
        if n:
            label = n + (" (ref)" if n in REFS else "")
            d.text((96 * k * (i % cols) + 6, 72 * k * (i // cols) + 4), label, fill=(32, 24, 24, 255), font=font)
    return big


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in CLASSES]
    figs = {}
    for name, fn in CLASSES.items():
        if only and name not in only:
            continue
        f, pal = fn()
        arr = render(f)
        palette_report(arr, pal, name)
        figs[name] = (arr, pal)
        if write:
            save_indexed(arr, pal, os.path.join(FRONT, name + ".png"))
    if write and not only:
        os.makedirs(os.path.dirname(SHEET), exist_ok=True)
        contact_sheet(figs, 2).save(SHEET)
    if pv:
        os.makedirs(pv, exist_ok=True)
        contact_sheet(figs).save(os.path.join(pv, "portraits.png"))
        for name, (arr, pal) in figs.items():
            upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
            grid_preview(to_rgba(arr, pal), 12, 4, 0, 60, 64).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
