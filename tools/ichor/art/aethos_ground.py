"""Ground: dry grass, wild tall grass, red anemones, limestone paths, soil.

Metatiles (General ids):
  001        grass                      00D  tall grass (wild encounters)
  002        grass under a ledge lip     015  long grass (reeds)
  01C        grass in deep shade        004  red anemones (animated)
  1D0-1E2    limestone path patch, 3x3 set (TL T TR / L C R / BL B BR)
  103-115    tilled earth patch, 3x3 set; 10C/12E/12F/14C berry soil
  100-112    volcanic ash patch, 3x3 set
"""
import numpy as np

from aethos_lib import art, rgba, over, solid, B, M, T, join_tiles, split_tiles
from aethos_textures import TEX, GRASS, PATH, SOIL, ASH

# --------------------------------------------------------------------------
# Wild tall grass: dark blades with golden seed heads. It must read at a
# glance as "something lives in here".
# --------------------------------------------------------------------------
TG_LEG = dict(k="tg_k", d="tg_d", m="tg_m", l="tg_l", y="sg_l", o="sg_d", g="gr_d")
# Two staggered rows of tufts, each a V of blades with a darker heart, and a
# few ripe barley heads catching the sun.
TALL_GRASS = art("""
    kydddkdddkddykdd
    lkddkldddlkdkldd
    lkdklmkdklkklmkd
    mlkklmkdklmklmkd
    kllmlmkdkllmlmkd
    klmlmdkdklmlmdkd
    kmmmddkdkmmlmdkd
    kmdddkdddkmddkdd
    dkdddkdddkddkydd
    kldddlkdklddlkdd
    lmkdklkklmkdlkdk
    lmkdklmklmkdmlkk
    lmkdkllmlmkdkllm
    mdkdklmlmdkdklml
    ddkdkmmlmdkdkmmm
    dkdddkmddkddkmdd
""", TG_LEG)


def _tall_grass():
    return TALL_GRASS.copy()


# Reeds: taller, denser blades for the long-grass metatile.
LONG_GRASS = art("""
    kldkdlkdkldkdlkd
    kldklmkdklmkdlkd
    klmklmkdklmklmkd
    kllklmkdkllklmkd
    klmkllkdklmkllkd
    kllklmkdkllklmkd
    klmklmkdklmklmkd
    kmlkmlkdkmlkmlkd
    kmlkllkdkmlkllkd
    kllkmlkdkllkmlkd
    kmlkmmkdkmlkmmkd
    kmmkmlkdkmmkmlkd
    kmmkmmkdkmmkmmkd
    kdmkmdkdkdmkmdkd
    kddkddkdkddkddkd
    kkdkkdkkkkdkkdkk
""", TG_LEG)

# --------------------------------------------------------------------------
# Red anemones: three blooms with black hearts. Frames sway the heads.
# --------------------------------------------------------------------------
FL_LEG = dict(r="fl_m", d="fl_d", l="fl_l", c="ink", s="tg_m", t="tg_d", k="tg_k")
FLOWER_HEAD = art("""
    .lr.
    lrcr
    rcdr
    .dd.
""", FL_LEG)
FLOWER_LEAVES = art("""
    ................
    ................
    ................
    ................
    ....s...........
    ....t.......s...
    ...ts.......t...
    ..tst.s....st...
    ...k.stt..sts...
    ......kt..ktk...
    ..s...k.....t...
    ..ts.....s......
    .tsts...stk.....
    ..kt.k..ktt.....
    ...k.....k......
    ................
""", FL_LEG)
FLOWER_SPOTS = [(2, 2), (9, 4), (4, 9)]


def flower_frame(dx):
    img = FLOWER_LEAVES.copy()
    for i, (x, y) in enumerate(FLOWER_SPOTS):
        sway = dx if i != 1 else -dx
        over_at(img, FLOWER_HEAD, x + sway, y)
    return img


def over_at(dst, src, x, y):
    h, w = src.shape[:2]
    sub = dst[y:y + h, x:x + w]
    over(sub, src[:sub.shape[0], :sub.shape[1]])


def flower_frames():
    """[key, f0, f1, f2] for the 4-tile flower anim (16x16 each)."""
    f0, f1, f2 = flower_frame(0), flower_frame(1), flower_frame(-1)
    return [f0.copy(), f0, f1, f2]


# --------------------------------------------------------------------------
# Patches: a 3x3 set of a material inside grass along a ragged edge. Built
# from four edge tiles plus flips, so a whole set costs ~6 tiles.
# Mask codes: 0 grass, 1 inside, 2 rim (inside, darker), 3 grass shadow.
# --------------------------------------------------------------------------
def _mask(text):
    rows = [r.strip() for r in text.strip().split("\n")]
    return np.array([[int(c) for c in r] for r in rows], np.uint8)


EDGE_TOP = _mask("""
    00000000
    00000000
    00000000
    00000000
    00000300
    30003230
    23332123
    12221112
""")
CORNER = _mask("""
    00000000
    00000000
    00000000
    00000000
    00000000
    00000003
    00000032
    00000321
""")
EDGE_LEFT = EDGE_TOP.T.copy()


def _fill(mask, grass, inside, rim, shadow):
    out = grass.copy()
    out[mask == 1] = inside[mask == 1]
    out[mask == 2] = rgba(rim)
    out[mask == 3] = rgba(shadow)
    return out


def _quad4(tl, tr, bl, br):
    return np.concatenate([np.concatenate([tl, tr], 1), np.concatenate([bl, br], 1)], 0)


def patch_set(inside_a, inside_b, rim, shadow="gr_d", grass_a=None):
    """{key: 16x16} for TL T TR L C R BL B BR."""
    from aethos_textures import GRASS_A
    g = GRASS_A if grass_a is None else grass_a
    et = _fill(EDGE_TOP, g, inside_a, rim, shadow)
    el = _fill(EDGE_LEFT, g, inside_a, rim, shadow)
    k = _fill(CORNER, g, inside_a, rim, shadow)
    a, b = inside_a, inside_b
    tl = _quad4(k, et, el, a)
    t = _quad4(et, et[:, ::-1], b, a)
    l = _quad4(el, a, el[::-1], b)
    c = _quad4(a, b, b, a)
    out = dict(TL=tl, T=t, L=l, C=c)
    out["TR"] = tl[:, ::-1]
    out["R"] = l[:, ::-1]
    out["BL"] = tl[::-1]
    out["B"] = t[::-1]
    out["BR"] = tl[::-1, ::-1]
    return out


PATCH_IDS = {
    "path": dict(TL=0x1D0, T=0x1D1, TR=0x1D2, L=0x1D8, C=0x1D9, R=0x1DA,
                 BL=0x1E0, B=0x1E1, BR=0x1E2),
    "soil": dict(TL=0x103, T=0x104, TR=0x105, L=0x10B, C=0x10C, R=0x10D,
                 BL=0x113, B=0x114, BR=0x115),
    "ash": dict(TL=0x100, T=0x101, TR=0x102, L=0x108, C=0x109, R=0x10A,
                BL=0x110, B=0x111, BR=0x112),
}


def paint(sheet, base):
    grass = TEX["grass"]
    # 001 grass, 01C deep-shade grass
    sheet.clear(0x001)
    sheet.set(0x001, M, grass)
    sheet.clear(0x01C)
    sheet.set(0x01C, M, TEX["grass_shade"])
    # 002: grass meeting a ledge lip above (thin shadow line at the top)
    g = grass.copy()
    g[0] = rgba("gr_s")
    g[1, ::3] = rgba("gr_d")
    sheet.clear(0x002)
    sheet.set(0x002, M, g)

    # tall grass and long grass
    sheet.clear(0x00D)
    sheet.set(0x00D, M, _tall_grass())
    sheet.clear(0x015)
    sheet.set(0x015, M, LONG_GRASS)

    # anemones: grass on bottom, the animated flower tiles on middle
    sheet.clear(0x004)
    sheet.set(0x004, B, grass)
    sheet.set(0x004, M, flower_frame(0))

    # patches
    from aethos_textures import PATH_A, PATH_B, SOIL_A, ASH_A
    sets = {
        "path": patch_set(PATH_A, PATH_B, "lp_m"),
        "soil": patch_set(SOIL_A, SOIL_A[:, ::-1], "dt_k", shadow="gr_s"),
        "ash": patch_set(ASH_A, ASH_A[:, ::-1], "mb_m"),
    }
    for kind, ids in PATCH_IDS.items():
        for k, m in ids.items():
            sheet.clear(m)
            sheet.set(m, M, sets[kind][k])
    # 14B/14C/14D: the top edge of a tilled plot (corner, edge, corner)
    soil = sets["soil"]
    for m, k in ((0x14B, "TL"), (0x14C, "T"), (0x14D, "TR")):
        sheet.clear(m)
        sheet.set(m, M, soil[k])
