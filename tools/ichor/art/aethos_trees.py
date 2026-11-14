"""Trees: gnarled olives, cypress spires and stone pines.

General has three tree styles and each keeps its footprint:

  * The big 2x2 tree (Route 101's forest edges) becomes an OLIVE: a split,
    twisted gray-brown trunk with a hollow, under a clumped silver-green
    crown. Its crown pokes 3 px into the row above (top layer), as General's
    did, so the player walks behind it.
  * The small 1x2 tree (towns, dense woods) becomes a CYPRESS spire. Its top
    half is on the top layer.
  * The secret-base tree becomes a STONE PINE, an umbrella crown on a tall
    bare trunk.

The ASCII below was drafted from clump shapes and finished by hand.
"""
import numpy as np

from aethos_lib import art, rgba, over, B, M, T
from aethos_textures import TEX

TREE_LEG = dict(k="ol_k", d="ol_d", m="ol_m", l="ol_l", s="ol_s",
                t="tr_k", u="tr_d", v="tr_m", w="tr_l")

# 32x35: rows 0-2 are the crown tip in the row above; rows 3-34 the 2x2.
OLIVE = art("""
    ..........kkkkk.................
    .........kllslsk...kkkk.........
    ........kslmmlmmkkklslmk........
    ........kslmmmmmddslmllmk.......
    ........kmmmdmmmddmmmmmmk.......
    ...kkkkkdmmmmmdddddlmmmmk.......
    ..klslmmmdmdddlslmmdmmdddkkkk...
    .klslmmlmmdddllllmmmdddsslsllk..
    .kmmmmmmddddddmmmdmdddddmmmmmmk.
    .kmmmmddssmmllddmddlssmmddmdmmk.
    ..kmmmdlmmmmmmmdddllmmmmmdmmmdk.
    ..kdddlmmlmmdmdddllmmmmmmmdddk..
    .kllmmdmdmmdddldddmmmmdmddddddk.
    klslmmmddmdsllllmmdmmmdddlslmmlk
    kmmmmmmdmddlmmmmmmddddddllmmmmmk
    kmmmmmddmddllmmmmddmdddsdddmmmmk
    .kmmddddddddddmmddddllmmmmmdmddk
    ..kkkdlmllmmdkdkkkkmllmdmmmmkkk.
    .....kmmmmmmk......kmmmmmddk....
    .....kkkkkkkkt.....tkkkdkkk.....
    ...........twvt...tvvut.........
    ...........twwvt.tvvut..........
    ............twwvtwvvut..........
    ............twwvvwvut...........
    ...........twwvvutwvut..........
    ...........twwvutttvut..........
    ..........twwvvutttwvut.........
    ..........twvvvuttwvvut.........
    ..........twwvvvutwvvut.........
    .........twwvwvvvvwvvvut........
    ........twwvvwvvvvvwvvvut.......
    .......ttwwvutttvvvttvvvutt.....
    .......twvut.....ttt...tvvut....
    ........ttt.............ttt.....
    ................................
""", TREE_LEG)

# Ground shadow under the olive (drawn on the grass, behind the trunk).
OLIVE_SHADOW = [  # (row, x0, x1) in sprite coords, inclusive
    (19, 6, 26), (20, 5, 27), (21, 6, 26), (22, 8, 25),
    (30, 7, 24), (31, 5, 27), (32, 5, 27), (33, 7, 25),
]

CY_LEG = dict(k="cy_k", d="cy_d", m="cy_m", l="cy_l",
              t="tr_k", u="tr_d", v="tr_m", w="tr_l")
# 16x32 cypress: rows 0-15 on the top layer, 16-31 on the middle layer.
CYPRESS = art("""
    .......kk.......
    ......kllk......
    ......kldk......
    .....kllmdk.....
    .....klmddk.....
    .....kllmdk.....
    ....klmmlddk....
    ....kllmdmdk....
    ....klmlmddk....
    ....kllmmdmk....
    ...klmmlmdmdk...
    ...kllmdmlddk...
    ...klmlmmdmdk...
    ...kllmdlmddk...
    ...klmmlmdmdk...
    ...kllmdmlddk...
    ..klmlmmlmdmdk..
    ..kllmdlmmdddk..
    ..klmlmmdlmdmk..
    ..kllmdmlmddmk..
    ..klmlmlmdmddk..
    ..kllmdmmlmdmk..
    ..klmlmdlmddmk..
    ..kllmmdmmdddk..
    ...klmdlmmddk...
    ...kllmmdmddk...
    ....kmmddmdk....
    .....kkddkk.....
    ......tuvt......
    ......tvwt......
    .....ttvutt.....
    ....t.tuut.t....
""", CY_LEG)
CYPRESS_SHADOW = [(27, 3, 12), (28, 3, 13), (29, 3, 13), (30, 4, 12), (31, 5, 11)]

PINE_LEG = dict(k="cy_k", d="pn_d", m="pn_m", l="pn_l",
                t="tr_k", u="tr_d", v="tr_m", w="tr_l", h="ink")
# 32x32 stone pine: rows 0-15 top layer (01E/01F), 16-31 middle (026/027).
PINE = art("""
    ................................
    ............kkkkkkkk............
    ..........kkllllllmlkk..........
    ...kkkkkkkdddmmlmmldddkkkkkkk...
    ..kmllmmlmmlmdlmmldmlmmlmmlmmk..
    ..kmlmmlmdddmddddddmddmmlmmlmk..
    ..kdddlddlmmlmmddmlmmlmddmdddk..
    kklmmlddlmmlmmlmmlmmlmmlmdlmmlk.
    klmmlmmdmmlmmlmmlmmlmmlddlmmlmmk
    kmmlmdddmlmdddmlmmlddddddmmldddk
    kkddddkkkddddddkkddddddkkkddddk.
    ..kkkk...kkkkkk..kkkkkk...kkkk..
    ...........tut....tvt...........
    ............tvt..tvut...........
    .............tvttvut............
    ..............tvvut.............
    ..............tvwut.............
    ..............tvwut.............
    ..............tvwut.............
    ..............tvwut.............
    ..............tvwvt.............
    ..............tvwut.............
    ..............tvwut.............
    ..............tvwut.............
    ..............tvwvut............
    .............tvwvuut............
    .............tvwvuut............
    .............tvwvvut............
    ............tvwvvuuut...........
    ...........ttvvuttuutt..........
    ...........t.ttt..ttt.t.........
    ................................
""", PINE_LEG)
PINE_SHADOW = [(12, 4, 27), (13, 6, 25), (28, 9, 22), (29, 8, 23), (30, 9, 22)]
# Secret-base "open" variant: a dark hollow between the roots.
PINE_HOLLOW = [(26, 15, 17), (27, 14, 17), (28, 14, 18)]


def _shadowed(bg, shadow, row0, x0):
    """Darken bg rows covered by shadow spans (sprite coords offset)."""
    out = bg.copy()
    dark = {"gr_m": "gr_d", "gr_l": "gr_d", "gr_h": "gr_d", "gr_d": "gr_s"}
    from aethos_lib import PAL
    for r, a, b in shadow:
        y = r - row0
        if not 0 <= y < 16:
            continue
        for x in range(max(a - x0, 0), min(b - x0, 15) + 1):
            px = tuple(int(v) for v in out[y, x, :3])
            for k, v in dark.items():
                if px == PAL[k]:
                    out[y, x] = rgba(v)
                    break
    return out


def crop(sprite, row0, x0, h=16, w=16):
    """16x16 window of a sprite, transparent outside it."""
    out = np.zeros((16, 16, 4), np.uint8)
    H, W = sprite.shape[:2]
    for y in range(h):
        for x in range(w):
            sy, sx = row0 + y, x0 + x
            if 0 <= sy < H and 0 <= sx < W:
                out[y, x] = sprite[sy, sx]
    return out


def on(bg, sprite, row0, x0, shadow=None):
    img = bg.copy() if shadow is None else _shadowed(bg, shadow, row0, x0)
    return over(img, crop(sprite, row0, x0))


def tip(side):
    """The olive crown poking into the row above: sprite rows 0-2 at the
    bottom of a top-layer metatile."""
    x0 = 0 if side == "L" else 16
    out = np.zeros((16, 16, 4), np.uint8)
    out[13:16] = crop(OLIVE, 0, x0)[0:3]
    return out


def paint(sheet, base):
    grass = TEX["grass"]
    ledge_grass = sheet.view(0x002, M).copy()
    tall = sheet.view(0x00D, M).copy()
    ash = sheet.view(0x109, M).copy()

    olive = {
        "TL": on(grass, OLIVE, 3, 0, OLIVE_SHADOW),
        "TR": on(grass, OLIVE, 3, 16, OLIVE_SHADOW),
        "BL": on(grass, OLIVE, 19, 0, OLIVE_SHADOW),
        "BR": on(grass, OLIVE, 19, 16, OLIVE_SHADOW),
    }
    tips = {"L": tip("L"), "R": tip("R")}

    def put(m, middle=None, top=None, bottom=None, keep=()):
        for l in (B, M, T):
            if l not in keep:
                sheet.view(m, l)[:] = 0
        if bottom is not None:
            sheet.set(m, B, bottom)
        if middle is not None:
            sheet.set(m, M, middle)
        if top is not None:
            sheet.set(m, T, top)

    # --- olive -------------------------------------------------------
    for m in (0x1D4, 0x1D6):
        put(m, olive["TL"])
    for m in (0x1D5, 0x1D7):
        put(m, olive["TR"])
    for m in (0x1DC, 0x1DE, 0x1F2):
        put(m, olive["BL"], tips["L"])
    for m in (0x1DD, 0x1DF, 0x1F3):
        put(m, olive["BR"], tips["R"])
    for m in (0x1E4, 0x1E6):
        put(m, olive["BL"])
    for m in (0x1E5, 0x1E7):
        put(m, olive["BR"])
    # the crown tip over other ground
    put(0x1CE, grass, tips["L"])
    put(0x1CF, grass, tips["R"])
    put(0x1C6, tall, tips["L"])
    put(0x1C7, tall, tips["R"])
    put(0x1E8, ledge_grass, tips["L"])
    put(0x1E9, ledge_grass, tips["R"])
    put(0x1EA, ash, tips["L"])
    put(0x1EB, ash, tips["R"])
    for m, s in ((0x1EE, "L"), (0x1EF, "R"), (0x1F0, "L"), (0x1F1, "R")):
        put(m, top=tips[s], keep=(B, M))         # over rock (terrain pass)
    for m, s in ((0x1F6, "L"), (0x1F7, "R"), (0x1FE, "L"), (0x1FF, "R")):
        put(m, top=tips[s], keep=(B, M))         # over sea / pond
    # olive crown's top half drawn over a ledge (top layer)
    put(0x1FC, ledge_grass, crop(OLIVE, 3, 0))
    put(0x1FD, ledge_grass, crop(OLIVE, 3, 16))

    # --- cypress -----------------------------------------------------
    cy_top = crop(CYPRESS, 0, 0)
    cy_bot = on(grass, CYPRESS, 16, 0, CYPRESS_SHADOW)
    for m in (0x00E, 0x00F, 0x0C6, 0x0C7):
        put(m, grass, cy_top)
    put(0x01D, ledge_grass, cy_top)
    put(0x025, tall, cy_top)
    for m in (0x02D, 0x035, 0x193, 0x0CE, 0x040):
        put(m, top=cy_top, keep=(B, M))           # over water / rock / fence
    for m in (0x016, 0x017):
        put(m, cy_bot)
    put(0x1EC, olive["BL"], cy_top)
    put(0x1ED, olive["BR"], cy_top)
    put(0x1F4, cy_bot, tips["L"])
    put(0x1F5, cy_bot, tips["R"])

    # --- stone pine (secret-base trees) --------------------------------
    for l_id, r_id in ((0x01E, 0x01F), (0x02E, 0x02F)):
        put(l_id, grass, crop(PINE, 0, 0))
        put(r_id, grass, crop(PINE, 0, 16))
    pine_bl = on(grass, PINE, 16, 0, PINE_SHADOW)
    pine_br = on(grass, PINE, 16, 16, PINE_SHADOW)
    put(0x026, pine_bl)
    put(0x027, pine_br)
    hollow = PINE.copy()
    for r, a, b in PINE_HOLLOW:
        hollow[r, a:b + 1] = rgba("ink")
    put(0x036, on(grass, hollow, 16, 0, PINE_SHADOW))
    put(0x037, on(grass, hollow, 16, 16, PINE_SHADOW))
