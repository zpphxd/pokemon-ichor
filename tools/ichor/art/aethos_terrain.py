"""Terrain pass: rebuild every metatile from General's material map.

This is the first pass of the build and the floor under everything else. It
reads each of General's pixels only as a *material* (grass, sand, sea, rock,
marble...) and a shade, then paints that spot with aethos textures: tufted dry
grass, rippled sand, the Aegean, and pale limestone laid in strata with block
joints. Flat areas take the texture, not General's pattern.

Later passes (ground, trees, coast, props, buildings) redraw whole metatiles
by hand on top of this.
"""
import numpy as np

from aethos_lib import rgba, tile_index, quad, flip
from aethos_textures import TEX8
from aethos_water import sea_texture

# General color -> (material, shade)
GEN = {
    (115, 197, 164): ("grass", "m"), (164, 213, 197): ("path", "m"),
    (65, 180, 131): ("grass", "d"), (24, 164, 106): ("grass", "s"),
    (180, 255, 131): ("leaf", "s"), (131, 197, 98): ("leaf", "l"),
    (57, 139, 49): ("leaf", "m"), (57, 82, 0): ("leaf", "d"),
    (65, 57, 49): ("earth", "k"), (106, 90, 90): ("earth", "d"),
    (164, 98, 90): ("earth", "m"), (222, 148, 115): ("earth", "l"),
    (238, 213, 205): ("rock", "h"), (222, 180, 164): ("rock", "l"),
    (189, 148, 139): ("rock", "m"), (156, 115, 115): ("rock", "n"),
    (131, 90, 90): ("rock", "d"), (98, 65, 82): ("rock", "k"),
    (65, 49, 65): ("rock", "x"),
    (238, 230, 164): ("sand", "h"), (222, 205, 131): ("sand", "m"),
    (213, 180, 106): ("sand", "d"), (205, 156, 82): ("sand", "x"),
    (115, 189, 246): ("pond", "m"), (74, 115, 172): ("pond", "d"),
    (172, 197, 230): ("sea", "h"), (139, 164, 222): ("sea", "l"),
    (106, 131, 213): ("sea", "n"), (82, 106, 213): ("sea", "m"),
    (65, 90, 189): ("sea", "m2"), (57, 82, 156): ("sea", "d"),
    (41, 65, 139): ("sea", "k"), (156, 164, 189): ("sea", "floor"),
    (255, 255, 255): ("white", "h"), (222, 230, 238): ("white", "l"),
    (189, 205, 230): ("white", "m"), (156, 180, 222): ("white", "n"),
    (131, 131, 139): ("metal", "m"), (98, 98, 123): ("metal", "d"),
    (65, 74, 106): ("metal", "k"), (41, 49, 90): ("metal", "x"),
    (213, 213, 213): ("gray", "l"), (189, 189, 189): ("gray", "m"),
    (164, 164, 164): ("gray", "d"),
    (222, 106, 98): ("red", "l"), (205, 65, 82): ("red", "m"),
    (238, 148, 115): ("roof", "m"), (255, 189, 131): ("roof", "l"),
    (255, 197, 148): ("roof", "h"),
    (98, 172, 238): ("glass", "l"), (98, 164, 222): ("glass", "m"),
    (82, 139, 197): ("glass", "d"),
}

# (material, shade) -> PAL name, or a texture name prefixed with '@'
MAP = {
    ("grass", "m"): "@grass", ("grass", "d"): "gr_d", ("grass", "s"): "tg_d",
    ("path", "m"): "@path",
    ("leaf", "s"): "ol_s", ("leaf", "l"): "ol_l", ("leaf", "m"): "ol_m", ("leaf", "d"): "ol_d",
    ("earth", "k"): "tr_k", ("earth", "d"): "tr_d", ("earth", "m"): "dt_m", ("earth", "l"): "tc_l",
    ("rock", "h"): "lp_h", ("rock", "l"): "lp_l", ("rock", "m"): "lp_m", ("rock", "n"): "lp_m",
    ("rock", "d"): "lp_d", ("rock", "k"): "lp_k", ("rock", "x"): "ink",
    ("sand", "h"): "sd_l", ("sand", "m"): "@sand", ("sand", "d"): "sd_d", ("sand", "x"): "lp_d",
    ("pond", "m"): "@shallow", ("pond", "d"): "ae_d",
    ("sea", "h"): "ae_h", ("sea", "l"): "ae_l", ("sea", "n"): "ae_n", ("sea", "m"): "@sea",
    ("sea", "m2"): "ae_m", ("sea", "d"): "ae_d", ("sea", "k"): "ae_k", ("sea", "floor"): "@shallow",
    ("white", "h"): "mb_h", ("white", "l"): "mb_l", ("white", "m"): "mb_l", ("white", "n"): "mb_m",
    ("metal", "m"): "mb_m", ("metal", "d"): "mb_d", ("metal", "k"): "rk_k", ("metal", "x"): "ink",
    ("gray", "l"): "mb_l", ("gray", "m"): "mb_m", ("gray", "d"): "mb_d",
    ("red", "l"): "tc_l", ("red", "m"): "tc_m",
    ("roof", "m"): "tc_l", ("roof", "l"): "sg_l", ("roof", "h"): "lp_h",
    ("glass", "l"): "ae_l", ("glass", "m"): "ae_n", ("glass", "d"): "ae_m",
}

DARKER = {"lp_h": "lp_l", "lp_l": "lp_m", "lp_m": "lp_d", "lp_d": "lp_k", "lp_k": "lp_k"}

# 8x8 textures: the terrain pass works per tile, so a texture must tile on
# the 8 px grid and survive the flips General placed its tiles with.
TEXTURES = {
    "grass": TEX8["grass"], "path": TEX8["path"], "sand": TEX8["sand"],
    "sea": sea_texture("sea")[0:8, 0:8], "shallow": sea_texture("shallow")[0:8, 0:8],
}


def strata(name, x, y):
    """Limestone bedding: a seam on the tile's last row, one block joint."""
    if name not in ("lp_m", "lp_l"):
        return name
    if y == 7 or x == 5 and y < 7:
        return DARKER[name]
    return name


def material_of(px):
    return GEN.get(tuple(int(v) for v in px[:3]))


# Rock standing in the sea is pale gray stone, washed clean; rock on land is
# warm limestone.
MARINE_ROCK = {"lp_h": "mb_h", "lp_l": "mb_l", "lp_m": "mb_m", "lp_d": "mb_d", "lp_k": "mb_d"}
# Sea stacks and reefs: every rock metatile in this block stands in water,
# even the all-rock interiors.
MARINE_IDS = set(range(0x150, 0x1C0)) | {0x0BD, 0x0C5, 0x0CD, 0x02C, 0x034, 0x03C}
MARINE_DARKER = {"mb_h": "mb_l", "mb_l": "mb_m", "mb_m": "mb_d", "mb_d": "ink", "ink": "ink"}


def render_tile(src, marine=False):
    """Re-render one 8x8 General tile by material."""
    out = np.zeros_like(src)
    for y in range(8):
        for x in range(8):
            if not src[y, x, 3]:
                continue
            mat = material_of(src[y, x])
            if mat is None:
                raise SystemExit(f"aethos_terrain: unmapped General color {tuple(src[y, x, :3])}")
            target = MAP[mat]
            if target.startswith("@"):
                out[y, x] = TEXTURES[target[1:]][y, x]
                continue
            if mat[0] == "rock":
                if marine:
                    target = MARINE_ROCK.get(target, target)
                    if target == "mb_m" and (x + 2 * y) % 9 == 0:
                        target = MARINE_DARKER[target]
                else:
                    target = strata(target, x, y)
            out[y, x] = rgba(target)
    return out


def marine_metatiles(base):
    """Metatiles whose General art contains sea or pond water."""
    wet = set()
    for m in range(512):
        for l in base.layers(m):
            a = base.get(m, l)
            for px in a[a[..., 3] > 0][:, :3]:
                mat = GEN.get(tuple(int(v) for v in px))
                if mat and mat[0] in ("sea", "pond"):
                    wet.add(m)
                    break
            if m in wet:
                break
    return wet


def paint(sheet, base):
    tiles, uses = tile_index(base.get)
    wet = marine_metatiles(base) | MARINE_IDS
    marine = {ci for m, l, q, ci, hf, vf in uses if m in wet}
    rendered = [render_tile(t, ci in marine) for ci, t in enumerate(tiles)]
    for m, l, q, ci, hf, vf in uses:
        quad(sheet.view(m, l), q)[:] = flip(rendered[ci], hf, vf)
