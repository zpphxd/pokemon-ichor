"""Hierophant Kerykos, the Herald of Hermes: his battle portrait and his walker.

Kerykos is round and cheerful, middle-aged, with a short graying beard and a grin
that is always halfway through a sentence. He wears a winged petasos, a traveling
chlamys in Aegean blue with a gold border and deep pockets stuffed with scrolls, and
carries the herald's staff, the kerykeion: gold, wound with two snakes, winged at the
top. Drawn in the slice's style (sprites_trainers.py, sprites_classes.py for the
portrait; sprites_npc.py for the walker), see design/phase2/SPRITES.md.

  TRAINER_PIC_HIEROPHANT_KERYKOS   graphics/trainers/front_pics/hierophant_kerykos.png
  OBJ_EVENT_GFX_ICHOR_KERYKOS      graphics/object_events/pics/people/ichor/kerykos.png
                                   (the cast palette, OBJ_EVENT_PAL_TAG_ICHOR_CAST)

Usage: python3 tools/ichor/art/sprites_kerykos.py [--write] [--preview DIR]

--write    writes both PNGs and the contact sheet design/phase2/img/sprites_kerykos.png
--preview  writes DIR/kerykos_sheet.png (the contact sheet), a 6x portrait, a 4x walker
           strip and pixel grids for editing
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba, battle_bg,  # noqa: E402
                         upscale, palette_report, grid_preview)
from sprites_classes import INK, render, load_pic  # noqa: E402
from sprites_npc import CAST_PAL, CAST_LEGEND, build_sheet, checker_bg, W, H  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

FRONT = os.path.join(ROOT, "graphics/trainers/front_pics/hierophant_kerykos.png")
WALKER = os.path.join(ROOT, "graphics/object_events/pics/people/ichor/kerykos.png")
SHEET = os.path.join(ROOT, "design/phase2/img/sprites_kerykos.png")


# --------------------------------------------------------------------------
# The portrait: 64 x 64, facing the player's side (screen left), lit from the
# top left. The kerykeion in his near hand, his far hand up as if to say
# "Hear ye!", the petasos pushed back.
# --------------------------------------------------------------------------

def portrait():
    pal = Palette([
        ("ink", INK),
        ("skin_l", (248, 200, 152)), ("skin_m", (216, 144, 104)), ("skin_d", (160, 96, 64)),
        ("gray_d", (96, 80, 72)), ("gray_l", (168, 160, 152)),
        ("hat_l", (184, 120, 72)), ("hat_d", (112, 64, 40)),
        ("lin_l", (248, 240, 216)), ("lin_d", (200, 184, 152)),
        ("blue_l", (208, 88, 112)), ("blue_m", (152, 48, 80)), ("blue_d", (88, 24, 56)),
        ("gold_l", (248, 216, 112)), ("gold_m", (208, 144, 48)),
    ])
    skin = Mat(["skin_d", "skin_m", "skin_l"], outline="gray_d", cuts=[0.5, 0.86])
    linen = Mat(["lin_d", "lin_l"], outline="gray_d", wx=0.8, wy=0.3, cuts=[0.6])
    cloak = Mat(["blue_d", "blue_m", "blue_l"], wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    lea = Mat(["gray_d"])
    f = Fig(pal)

    # the cloak behind him, falling from the far shoulder to the knee
    back = f.poly([(34, 23), (42, 23), (47, 28), (50, 36), (51, 46), (49, 52), (44, 53), (40, 50)], cloak, group=40)
    # stout legs and sandals
    f.poly([(25, 51), (30, 51), (30, 57), (25, 57)], skin, group=100)
    f.poly([(35, 51), (40, 51), (40, 57), (35, 57)], skin, group=101)
    f.poly([(22, 57), (30, 57), (30, 61), (21, 61)], lea)
    f.poly([(35, 57), (42, 57), (44, 61), (35, 61)], lea)
    # the chiton over a round belly, to the knee
    body = f.poly([(25, 23), (39, 23), (43, 28), (46, 35), (46, 45), (43, 50), (37, 53), (27, 53), (21, 50),
                   (18, 44), (18, 35), (21, 28)], linen, group=110)
    for x in (28, 33):
        f.shade_poly([(x, 46), (x + 1, 46), (x + 1, 52), (x, 52)], 0.5)
    f.shade_poly([(18, 35), (22, 35), (22, 48), (19, 48)], -0.25)
    # a leather belt riding under the belly
    f.poly([(19, 42), (45, 41), (45, 43), (19, 44)], lea, clip=body, noline=True)
    f.rect(29, 19, 35, 25, skin, group=400)
    # the chlamys over the far shoulder and down his side, its front edge gold
    f.poly([(33, 23), (41, 23), (46, 29), (48, 38), (47, 46), (43, 51), (38, 52), (38, 44), (40, 36),
            (38, 29)], cloak, group=130)
    f.shade_poly([(44, 31), (45, 31), (46, 47), (45, 47)], 0.4)
    # the deep pocket on the cloak, scrolls sticking out
    f.poly([(40, 39), (47, 39), (47, 47), (40, 47)], cloak, group=500, bias=0.35)
    # near arm: the forearm reaching down to the kerykeion
    f.poly([(21, 23), (28, 23), (27, 29), (22, 30), (19, 27)], linen, group=210)
    f.thick_line([(22, 28), (18, 32), (15, 35)], 5, skin, group=200)
    # far arm raised, one finger up: "Hear ye!"
    f.thick_line([(42, 26), (48, 22), (50, 17)], 5, skin, group=300)
    f.poly([(38, 23), (43, 23), (46, 27), (42, 29)], cloak, group=310)

    # gold border down the chlamys's front edge and the brooch at the shoulder
    f.line([(38, 29), (40, 36), (38, 44), (38, 51)], "gold_m")
    f.pxs([(39, 30), (40, 35)], "gold_l")
    f.patch(36, 22, [
        ".kk.",
        "kOok",
        "kook",
        ".kk.",
    ], {"k": "ink", "O": "gold_l", "o": "gold_m"})
    # the pocket's seam, and two sealed scrolls poking out of it
    f.patch(39, 35, [
        ".kkk.kkk.",
        "kWWwkWWwk",
        "kwWwkkwWk",
        ".kRk.kRk.",
        "kkkkkkkkk",
    ], {"k": "ink", "W": "lin_l", "w": "lin_d", "R": "hat_d"})
    # belt buckle
    f.patch(31, 41, ["kOk", "kok"], {"k": "ink", "O": "gold_l", "o": "gold_m"})
    # sandal straps, knees
    f.line([(25, 54), (29, 54)], "gray_d")
    f.line([(36, 54), (39, 54)], "gray_d")
    f.pxs([(26, 51), (37, 51)], "skin_m")

    # the kerykeion: a cedar staff, two gold snakes wound up it, white wings and a gold
    # knob on top
    for y in range(9, 62):
        f.px(12, y, "ink")
        f.px(13, y, "hat_l" if y % 5 == 0 else "hat_d")
        f.px(14, y, "ink")
    f.patch(7, 2, [
        ".....kkk.....",
        "kk..kOOok..kk",
        "kWWkkOook.kWk",
        ".kWWkkokkWWk.",
        "..kWWWkWWWk..",
        "...kkk.kkk...",
    ], {"k": "ink", "W": "lin_l", "w": "lin_d", "O": "gold_l", "o": "gold_m"})
    f.patch(9, 8, [
        ".kk...kk.",
        "kOOk.kOOk",
        ".kOOkOOk.",
        "..koOok..",
        ".kOkhkOk.",
        "kOk.h.kOk",
        "kok.h.kok",
        ".kOkhkOk.",
        "..koOok..",
        ".kOkhkOk.",
        "kOk.h.kOk",
        ".kokhkok.",
        "..koOok..",
        "...kok...",
        "....h....",
    ], {"k": "ink", "O": "gold_l", "o": "gold_m", "h": "hat_d"})
    # his fist round the staff
    f.patch(10, 33, [
        ".kkkkk.",
        "kLLLLMk",
        "kLkLkMk",
        "kLLLMMk",
        ".kkkkk.",
    ], {"k": "gray_d", "L": "skin_l", "M": "skin_m"})
    # the raised hand, index finger up
    f.patch(47, 7, [
        "...kk..",
        "..kLk..",
        "..kLk..",
        "..kLkk.",
        ".kkLLLk",
        "kLkLLMk",
        "kLLLLMk",
        ".kLLMMk",
        "..kMMk.",
        "...kk..",
    ], {"k": "gray_d", "L": "skin_l", "M": "skin_m"})
    # head: the petasos pushed back, its little wings; a round face, graying beard,
    # bushy brows and a grin mid-sentence
    f.patch(18, 0, [
        "..........kkkkkkkk.....kk....",
        ".........kHHHHHhhhk...kWWk...",
        "........kHHHHHHhhhhk.kWWWk...",
        ".......kHHHHHHHhhhhhkWWwk....",
        "......kHHHHHHHHhhhhhkWwk.....",
        ".....kHHHHHHHHhhhhhhkwk......",
        "....kkHHHHHHHHHhhhhhhkk......",
        ".kkkkkkkkkkkkkkkkkkkkkkkkk...",
        "kHHHHHHHHHHHHhhhhhhhhhhhhhk..",
        ".kkhhhhhhhhhhhhhhhhhhhhhkk...",
        "...kkkkkkkkkkkkkkkkkkkkk.....",
        "....kgLLLLLLLLLLLLMMgk.......",
        "....kgGGgLLLLLgGGgMMgk.......",
        "....kLkkkLLLLLkkkLMDMk.......",
        "...kLLkWkLLLLLkWkLMDMk.......",
        "...kLLMMLLLLDLLMMMMDk........",
        "...kLMMMLLLDDLLMMMMDk........",
        "....kgLLkkkkkkkLMMgk.........",
        "....kggkWWWWWWkgMggk.........",
        "....kgggkWWWWkggggk..........",
        ".....kggggkkkggggk...........",
        "......kkgggggggkk............",
        "........kkkkkkk..............",
    ], {"k": "ink", "H": "hat_l", "h": "hat_d", "W": "lin_l", "w": "lin_d", "L": "skin_l",
        "M": "skin_m", "D": "skin_d", "g": "gray_l", "G": "gray_d"})
    return f, pal


# --------------------------------------------------------------------------
# The walker: the cast palette (sprites_npc.CAST_PAL), so he needs no new OBJ
# palette slot. A dark felt petasos (umber and brown) with linen wings and a
# porphyry chlamys (crimson and red_d) over a linen chiton and a round belly, the
# kerykeion in his right hand (screen left facing down), bronze with leaf-green
# snakes. The player wears a straw petasos and Aegean blue, so he must not.
#   k ink  b brown  u umber  o bronze  O bronze_l  s skin_d  S skin_l
#   l linen_d  L linen_l  c crimson  r red_d  g leaf  t slate (gray hair)
# --------------------------------------------------------------------------

_HAT_DOWN = [
    "...kk.kkkk.kk...",
    "..kLLkuuuuukLLk.",
    "..kLkuuuuuuukLk.",
    ".kkuuuuuuuuuubkk",
    "kbbbbbbbbbbbbbbk",
    ".kkkkkkkkkkkkkk.",
]
_FACE_DOWN = [
    "..ktSSSSSSSStk..",
    "..kSkSSSSSSkSk..",
    "..ksSSSSSSSSsk..",
    "..klSSkkkkSSlk..",
    "...kllkLLklk....",
    "....kllllllk....",
]
_HAT_UP = [
    "...kk.kkkk.kk...",
    "..kLLkuuuuukLLk.",
    "..kLkuuuuuuukLk.",
    ".kkuuuuuuuuuubkk",
    "kbbbbbbbbbbbbbbk",
    ".kkkkkkkkkkkkkk.",
]
_HEAD_UP = [
    "..kttttttttttk..",
    "..ktttttttttsk..",
    "..ksttttttttsk..",
    "...kssssssssk...",
    "....kSSSSSSk....",
    "....kkkkkkkk....",
]
_HAT_LEFT = [
    "....kk.kkkk.....",
    "...kLLkuuuuuk...",
    "...kLkuuuuuuuk..",
    "..kkuuuuuuuubk..",
    ".kbbbbbbbbbbbbk.",
    "..kkkkkkkkkkkk..",
]
_FACE_LEFT = [
    "...kSSSSSStttk..",
    "...kSkSSSSSttk..",
    "..kSSSSSSSsttk..",
    "..kkkkSSSlltk...",
    "...klLklllltk...",
    "....kllllllk....",
]

# Bodies: a round belly in linen, the blue chlamys over the shoulders, the staff
# in his right hand. The staff column: O gold, g snake, k outline.
_BODY_DOWN = [
    "kgk.kcLLLLcrrk..",
    "kOkkccLLLLLcrck.",
    "kgSkcLLLLLLLLrck",
    "kOkkLLLLLLLLLLrk",
    "kgk.kLLLLLLLLLrk",
    "kuk.kbbbobbbbbrk",
    "kuk.kLLLLLLLLLk.",
    "kuk..kLLLLLLLk..",
]
_BODY_UP = [
    "..krccccccccrkgk",
    ".krccccccccccrOk",
    ".krccccccccccrSk",
    ".krccccccccccrkk",
    ".krccccccccccrkg",
    ".krrbbbbbbbbrrku",
    "..kLLLLLLLLLLk.u",
    "...kLLLLLLLLk..u",
]
_BODY_LEFT = [
    "..kgkLLLLLcrk...",
    "..kOkLLLLLLcrk..",
    "..kgSkLLLLLLrk..",
    ".kkOkLLLLLLLrk..",
    ".kLkgLLLLLLLrk..",
    ".kbkObbobbbbrk..",
    "..kkuLLLLLLLk...",
    "...kukLLLLLk....",
]


def walker_spec():
    stand_d = _BODY_DOWN + [".k...kbbkbbk...."]
    walk_d0 = _BODY_DOWN[:-1] + ["kuk..kLLLLLLLk..", ".k...kbbk......."]
    walk_d1 = _BODY_DOWN[:-1] + ["kuk..kLLLLLLLk..", ".k........kbbk.."]
    stand_u = _BODY_UP + ["....kbbkbbk...k."]
    walk_u0 = _BODY_UP[:-1] + ["...kLLLLLLLLk..u", "....kbbk.......k"]
    walk_u1 = _BODY_UP[:-1] + ["...kLLLLLLLLk..u", "........kbbk...k"]
    stand_l = _BODY_LEFT + ["....kbbkbk......"]
    walk_l0 = _BODY_LEFT[:-1] + ["...kukLLLLLk....", "...kbbk.kbk....."]
    walk_l1 = _BODY_LEFT[:-1] + ["...kukLLLLLk....", "....k.kbbbk....."]
    return dict(
        name="kerykos",
        y0=10,
        down=dict(top=_HAT_DOWN + _FACE_DOWN, stand=stand_d, walk=[walk_d0, walk_d1]),
        up=dict(top=_HAT_UP + _HEAD_UP, stand=stand_u, walk=[walk_u0, walk_u1]),
        left=dict(top=_HAT_LEFT + _FACE_LEFT, stand=stand_l, walk=[walk_l0, walk_l1]),
    )


def walker():
    return build_sheet(walker_spec(), CAST_LEGEND, CAST_PAL)


# --------------------------------------------------------------------------
# Previews
# --------------------------------------------------------------------------

def battle_tile(im):
    tile = battle_bg().crop((240 - 96, 40, 240, 112)).copy()
    tile.alpha_composite(im, (16, 4))
    return tile


def walker_strip(arr, k=4, ref=None):
    rows = ([ref] if ref is not None else []) + [to_rgba(arr, CAST_PAL)]
    pad = 4
    out = Image.new("RGBA", (W * 9 + pad * 8, (H + pad) * len(rows) - pad), (232, 224, 200, 255))
    for i, im in enumerate(rows):
        for fr in range(9):
            tile = checker_bg(W, H)
            tile.alpha_composite(im.crop((fr * W, 0, (fr + 1) * W, H)))
            out.alpha_composite(tile, (fr * (W + pad), i * (H + pad)))
    return upscale(out, k)


def ref_walker(name):
    p = os.path.join(ROOT, "graphics/object_events/pics/people/ichor", name + ".png")
    im = Image.open(p)
    idx = np.array(im)
    rgba = np.array(im.convert("RGBA"))
    rgba[idx == 0, 3] = 0
    return Image.fromarray(rgba, "RGBA")


def contact_sheet(parr, ppal, warr):
    """The portrait on the battle background beside Ione's and the merchant's, at 3x;
    under it his walker's nine frames beside Ione's, at 4x."""
    refs = [load_pic(os.path.join(ROOT, "graphics/trainers/front_pics", n + ".png"))
            for n in ("hierophant_ione", "merchant")]
    tiles = [battle_tile(r) for r in refs] + [battle_tile(to_rgba(parr, ppal))]
    top = Image.new("RGBA", (96 * len(tiles), 72))
    for i, t in enumerate(tiles):
        top.alpha_composite(t, (96 * i, 0))
    top = upscale(top, 3)
    strip = walker_strip(warr, 4, ref_walker("hierophant_ione"))
    out = Image.new("RGBA", (max(top.width, strip.width) + 16, top.height + strip.height + 48), (40, 40, 48, 255))
    out.alpha_composite(top, (8, 24))
    out.alpha_composite(strip, (8, top.height + 40))
    d = ImageDraw.Draw(out)
    fnt = ImageFont.load_default(size=14)
    d.text((8, 4), "Ione, the merchant, Kerykos (3x, battle background)", fill=(230, 230, 200), font=fnt)
    d.text((8, top.height + 24), "Ione's walker, then Kerykos's (4x)", fill=(230, 230, 200), font=fnt)
    return out


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    f, pal = portrait()
    parr = render(f)
    palette_report(parr, pal, "hierophant_kerykos")
    warr = walker()
    if write:
        save_indexed(parr, pal, FRONT)
        save_indexed(warr, CAST_PAL, WALKER)
        os.makedirs(os.path.dirname(SHEET), exist_ok=True)
        contact_sheet(parr, pal, warr).save(SHEET)
    if pv:
        os.makedirs(pv, exist_ok=True)
        contact_sheet(parr, pal, warr).save(os.path.join(pv, "kerykos_sheet.png"))
        bg = Image.new("RGBA", (64, 64), (168, 200, 120, 255))
        bg.alpha_composite(to_rgba(parr, pal))
        upscale(bg, 6).save(os.path.join(pv, "kerykos_portrait6x.png"))
        grid_preview(to_rgba(parr, pal), 12, 0, 0, 64, 64).save(os.path.join(pv, "kerykos_portrait_grid.png"))
        grid_preview(to_rgba(warr, CAST_PAL), 10).save(os.path.join(pv, "kerykos_walker_grid.png"))


if __name__ == "__main__":
    main()
