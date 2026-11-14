"""Ground textures for aethos, drawn by hand as 8x8 tiles.

The primary holds only 512 tiles, so a texture is one or two 8x8 tiles laid
in a checker (like General's grass) rather than a 16x16 picture. TEX8 holds
the single tile the terrain pass paints mixed tiles with; TEX holds the
16x16 metatile built from the pair.
"""
import numpy as np

from aethos_lib import art

GL = dict(a="gr_m", b="gr_d", c="gr_l", d="gr_h", s="gr_s")

GRASS_A = art("""
    aaaaaaaa
    aaaaaaaa
    aacaaaaa
    abaabaaa
    aabbaaaa
    aaaaaaaa
    aaaaaaaa
    aaaaaaaa
""", GL)
GRASS_B = art("""
    aaaaaaaa
    aaaaaaaa
    aaaaaaca
    adaaabaa
    aaaaaabb
    aaaaaaaa
    aaaaaaaa
    aaaaaaaa
""", GL)
GRASS_SHADE_A = art("""
    bbbbbbbb
    bbbbbbbb
    bbabbbbb
    bsbbsbbb
    bbssbbbb
    bbbbbbbb
    bbbbbbbb
    bbbbbbbb
""", GL)

PL = dict(a="lp_l", b="lp_m", c="lp_h", d="lp_d")
PATH_A = art("""
    aaaaaaaa
    aaaaaaca
    aacbaaab
    aaabaaaa
    aaaaaaaa
    aaaaaaaa
    acaaaaaa
    aabaaaaa
""", PL)
PATH_B = art("""
    aaaaaaaa
    aaaaaaaa
    aaaaacaa
    aaaaaaba
    abaaaaaa
    aaaacaaa
    aaaaabaa
    aaaaaaaa
""", PL)

SL = dict(a="sd_m", b="sd_d", c="sd_l")
SAND_A = art("""
    aaaaaaaa
    aaaaacaa
    abaaaaaa
    aaaaaaaa
    aaaaaaab
    aaccaaaa
    aaaaaaaa
    aaaaaaaa
""", SL)
SAND_B = art("""
    aaaaaaaa
    aaaaaaaa
    aaaaabaa
    acaaaaaa
    aaaaaaaa
    aaaaaacc
    aaabaaaa
    aaaaaaaa
""", SL)

# Tilled red earth: furrows run across the tile.
SOIL_A = art("""
    aaaaaaaa
    bbbbbbbb
    aacaaaaa
    aaaaaaaa
    aaaaaaaa
    bbbbbbbb
    aaaaacaa
    aaaaaaaa
""", dict(a="dt_m", b="dt_d", c="lp_l"))

# Volcanic ash: pale gray dust with cinders.
ASH_A = art("""
    aaaaaaaa
    aaaaacaa
    abaaaaaa
    aaaaaaaa
    aaaaaaba
    aacaaaaa
    aaaaaaaa
    aaaaaaaa
""", dict(a="mb_l", b="mb_m", c="mb_h"))


def checker(a, b):
    """[a b / b a] as a 16x16 metatile."""
    top = np.concatenate([a, b], axis=1)
    bot = np.concatenate([b, a], axis=1)
    return np.concatenate([top, bot], axis=0)


TEX8 = dict(grass=GRASS_A, path=PATH_A, sand=SAND_A, soil=SOIL_A, ash=ASH_A,
            grass_shade=GRASS_SHADE_A)
TEX = dict(grass=checker(GRASS_A, GRASS_B), path=checker(PATH_A, PATH_B),
           sand=checker(SAND_A, SAND_B), soil=checker(SOIL_A, SOIL_A),
           ash=checker(ASH_A, ASH_A[:, ::-1]),
           grass_shade=checker(GRASS_SHADE_A, GRASS_SHADE_A[:, ::-1]))

# Back-compat names used by painters
GRASS, PATH, SAND, SOIL, ASH = TEX["grass"], TEX["path"], TEX["sand"], TEX["soil"], TEX["ash"]


def tex(name):
    return TEX[name].copy()
