"""Review images for the Theoxenia's Sam and Cami (design/art/img/).

Usage:
    python3 tools/ichor/art/theoxenia_previews.py [sheets] [portraits] [scene] [--out DIR]
                                                  [--portraits-as NAME]

sheets      theoxenia_sam_cami_sheets.png: the four walkers' sheets at 4x,
            every frame including the strum, the seat and the rise, with
            vanilla Birch on top for scale
portraits   theoxenia_sam_cami_portraits.png: the two portraits at 3x
            (--portraits-as NAME writes NAME.png instead, for a pass's copy)
scene       theoxenia_sam_cami_scene.png: Cami on the seat stone by Eleusa's
            Maiden's Well, and Sam strumming in a field, at 3x. The ground is
            composed from gTileset_Eleusa and aethos with render_map.py, so
            run tools/ichor/art/eleusa_build.py --no-compile once first (it
            writes build/eleusa/catalog.json). Gods in disguise cast no
            shadow; the player's shadow is drawn, as the game draws it.

With no names, writes all three. Nothing here reads the reference photo.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, to_rgba, upscale  # noqa: E402
from sprites_npc import checker_bg, ref_rgba  # noqa: E402
import sprites_npc_theoxenia as T  # noqa: E402
import portraits_theoxenia as P  # noqa: E402

OUT = os.path.join(ROOT, "design/art/img")
INK = (48, 40, 40, 255)
PAPER = (240, 232, 208, 255)


def text(d, xy, s, fill=INK):
    d.text(xy, s, fill=fill)


# --------------------------------------------------------------------------
# Sheets
# --------------------------------------------------------------------------

FRAME_LABELS = ["down", "up", "left", "walk", "walk", "walk", "walk", "walk", "walk"]
EXTRA_LABELS = {"sam": ["strum hi", "strum lo", "strum joy"], "apollo": ["strum hi", "strum lo", "strum joy"],
                "cami": ["sit", "rise"], "demeter": []}


def sheets_image():
    k, pad, lab = 4, 4, 14
    rows = [("prof_birch (vanilla, for scale)", ref_rgba(), [])]
    for name in T.SPECS:
        rows.append((name, to_rgba(T.build(T.SPECS[name]), T.PAL), EXTRA_LABELS[name]))
    nmax = max(r[1].width // 16 for r in rows)
    w = 8 + nmax * (16 * k + pad)
    h = 8 + len(rows) * (32 * k + pad + 2 * lab)
    out = Image.new("RGBA", (w, h), PAPER)
    d = ImageDraw.Draw(out)
    y = 8
    for name, im, extra in rows:
        text(d, (8, y), name)
        y += lab
        for f in range(im.width // 16):
            tile = checker_bg(16, 32)
            tile.alpha_composite(im.crop((f * 16, 0, f * 16 + 16, 32)))
            x = 8 + f * (16 * k + pad)
            out.alpha_composite(upscale(tile, k), (x, y))
            if f >= 9:
                d.rectangle([x - 1, y - 1, x + 16 * k, y + 32 * k], outline=(200, 120, 40, 255))
                text(d, (x, y + 32 * k + 2), f"{f} {extra[f - 9]}")
        y += 32 * k + pad + lab
    return out


# --------------------------------------------------------------------------
# Portraits
# --------------------------------------------------------------------------

def portraits_image():
    k, pad = 3, 12
    names = list(P.PORTRAITS)
    w = pad + len(names) * (64 * k + pad)
    h = pad + 64 * k + 18
    out = Image.new("RGBA", (w, h), PAPER)
    d = ImageDraw.Draw(out)
    for i, name in enumerate(names):
        c, pal = P.PORTRAITS[name]()
        im = to_rgba(c.a, pal)
        bg = Image.new("RGBA", im.size, (200, 216, 200, 255))
        bg.alpha_composite(im)
        x = pad + i * (64 * k + pad)
        out.alpha_composite(upscale(bg, k), (x, pad))
        text(d, (x, pad + 64 * k + 4), name.capitalize())
    return out


# --------------------------------------------------------------------------
# Scene
# --------------------------------------------------------------------------

GRASS, PATH = 0x001, 0x1D9
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
CYP_TOP, CYP_BOT = 0x00E, 0x016
SW, SH = 26, 10            # the scene in metatiles: two vignettes side by side


def compose():
    sys.path.insert(0, os.path.dirname(__file__))
    import eleusa_scene as ES
    ES.W, ES.H = SW, SH
    s = ES.Scene()
    s.m[:] = GRASS
    # --- left: the well-yard at Eleusa. The Maiden's Well, the seat stone
    # south of it, wheat behind, poppies, a path coming up from the village.
    s.put("kallichoron", 5, 1)
    s.put("seat_stone", 6, 4)
    s.field(["#####.",
             "####..",
             "###...",
             "##....",
             "#....."], 0, 0)
    s.field([".####",
             "..###",
             "...##",
             "....#"], 8, 0)
    s.put("wheat_poppies", 1, 1)
    s.put("wheat_poppies", 10, 1)
    for x, y in ((1, 6), (10, 5), (3, 8)):
        s.piece("poppies", "scattered", x, y)
    s.piece("poppies", "dense", 9, 7)
    s.rect(6, 7, 6, 9, PATH)
    s.rect(5, 9, 7, 9, PATH)
    s.olive(11, 7)
    s.cypress(0, 5)
    s.put("sheaf_grass", 4, 5)
    # --- right: a pasture near Arkadia, where Sam plays for nobody
    x0 = 14
    s.field([".####.",
             "######",
             ".####."], x0 + 6, 6, key="stubble")
    s.put("stook", x0 + 8, 7)
    s.field(["####", "###."], x0 + 8, 0)
    s.olive(x0 + 1, 1)
    s.cypress(x0 + 11, 3)
    s.rect(x0 + 4, 0, x0 + 4, 9, PATH)
    for x, y in ((x0 + 2, 5), (x0 + 7, 3), (x0 + 1, 8)):
        s.piece("poppies", "scattered", x, y)
    return s


def render_ground(s, scale):
    blk = os.path.join(ROOT, "build/theoxenia/scene.bin")
    png = os.path.join(ROOT, "build/theoxenia/scene_ground.png")
    os.makedirs(os.path.dirname(blk), exist_ok=True)
    s.m.astype("<u2").tofile(blk)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools/ichor/render_map.py"), "--blockdata", blk,
                    "--width", str(SW), "--primary", "aethos", "--secondary", "gTileset_Eleusa",
                    "--scale", "1", "-o", png], check=True, stdout=subprocess.DEVNULL)
    return Image.open(png).convert("RGBA")


def frame(sheet, f):
    return sheet.crop((f * 16, 0, f * 16 + 16, 32))


def player_sheet():
    path = os.path.join(ROOT, "graphics/object_events/pics/people/brendan/walking.png")
    im = Image.open(path)
    idx = np.array(im)
    rgba = np.array(im.convert("RGBA"))
    rgba[idx == 0, 3] = 0
    return Image.fromarray(rgba, "RGBA")


def shadow():
    im = Image.open(os.path.join(ROOT, "graphics/field_effects/pics/shadow_medium.png"))
    idx = np.array(im)
    a = np.zeros(idx.shape + (4,), np.uint8)
    a[idx != 0] = (0, 0, 0, 64)      # OW_SHADOW_INTENSITY 4 of 16
    return Image.fromarray(a, "RGBA")


def place(img, spr, tx, ty, dy=0, with_shadow=False):
    """An object on metatile (tx, ty): its 16x32 frame stands on the tile."""
    x, y = tx * 16, ty * 16 - 16 + dy
    if with_shadow:
        img.alpha_composite(shadow(), (x, ty * 16 + 10))
    img.alpha_composite(spr, (x, y))


def scene_image():
    s = compose()
    ground = render_ground(s, 1)
    sheets = {n: to_rgba(T.build(T.SPECS[n]), T.PAL) for n in T.SPECS}
    pl = player_sheet()
    left, right = ground.copy(), ground.copy()
    # Cami on the seat stone, her back to us, facing the well; the player behind her
    place(left, frame(sheets["cami"], 9), 6, 4)
    place(left, frame(pl, 1), 6, 6, with_shadow=True)
    # Sam strumming in the pasture; the player coming up the path
    place(right, frame(sheets["sam"], 9), 20, 4)
    place(right, frame(pl, 2).transpose(Image.FLIP_LEFT_RIGHT), 18, 4, with_shadow=True)
    k = 3
    w = SW * 16
    out = Image.new("RGBA", (w * k, SH * 16 * k), PAPER)
    out.alpha_composite(upscale(left.crop((0, 0, 13 * 16, SH * 16)), k), (0, 0))
    out.alpha_composite(upscale(right.crop((13 * 16, 0, w, SH * 16)), k), (13 * 16 * k, 0))
    d = ImageDraw.Draw(out)
    d.line([(13 * 16 * k, 0), (13 * 16 * k, SH * 16 * k)], fill=PAPER, width=6)
    return out


def main():
    args = sys.argv[1:]
    out = OUT
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    pname = "theoxenia_sam_cami_portraits"
    if "--portraits-as" in args:
        i = args.index("--portraits-as")
        pname = args[i + 1]
        del args[i:i + 2]
    which = args or ["sheets", "portraits", "scene"]
    os.makedirs(out, exist_ok=True)
    if "sheets" in which:
        sheets_image().save(os.path.join(out, "theoxenia_sam_cami_sheets.png"))
    if "portraits" in which:
        portraits_image().save(os.path.join(out, pname + ".png"))
    if "scene" in which:
        scene_image().save(os.path.join(out, "theoxenia_sam_cami_scene.png"))


if __name__ == "__main__":
    main()
