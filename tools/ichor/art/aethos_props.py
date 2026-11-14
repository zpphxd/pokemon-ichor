"""Edges and props: terrace ledges, dry-stone walls, steles, herms, boulders.

Ledges are dry-stone terrace lips: a pale capstone row over a face of laid
limestone and a dark foot, so they still read as "jump down". The lip sits
on the middle layer over the ground (grass, rock floor or sand, from the
terrain pass), so the three ledge families share every lip tile.

  ledge   S       W       E       SW      SE      S-end L  S-end R  inner
  grass   087     085     086     08D     08E     0D5      0D6      06E
  rock    08F     095     096     09D     09E     0DD      0DE
  sand    097     0A5     0A6     0AD     0AE     0E5      0E6
  also W/E: 0FE/0FF, 106/107 (grass), 10E/10F, 116/117 (rock), 11E/11F,
  126/127 (sand)

General's metal fence becomes a low dry-stone wall: 148/149/14A run west to
east (middle layer), 138/13A the same on the top layer, and the single posts
(132/133 middle, 139-142 top) become north-south wall runs.

Signs: 003 is a small marble stele with a pediment, 01B a roadside herm.
"""
import numpy as np

from aethos_lib import art, rgba, over, B, M, T
from aethos_textures import TEX

LP = dict(k="lp_k", d="lp_d", m="lp_m", l="lp_l", h="lp_h", i="ink")

# --------------------------------------------------------------------------
# Ledges
# --------------------------------------------------------------------------
# Rows 9-14 of a south-facing lip, 8 px repeat: capstones, two courses of
# laid stone, dark foot.
LEDGE_S_ROWS = art("""
    lhlllhll
    mmmkmmmm
    mmmkmmmm
    dddddddd
    dddddddk
    kkkkkkkk
""", LP)


def _ledge_s(x0=0, x1=16):
    out = np.zeros((16, 16, 4), np.uint8)
    for x in range(x0, x1):
        out[9:15, x] = LEDGE_S_ROWS[:, x % 8]
    return out


def _ledge_e(y0=0, y1=16):
    """Lip along the east side (x 10-15): the south lip turned on its side,
    capstones toward the upper terrace on the west."""
    out = np.zeros((16, 16, 4), np.uint8)
    rows = LEDGE_S_ROWS  # (6, 8)
    for y in range(y0, y1):
        out[y, 10:16] = rows[:, y % 8]
    return out


def ledge_pieces():
    s = _ledge_s()
    e = _ledge_e()
    w = e[:, ::-1].copy()
    # south-east corner: the south lip runs into the east lip
    se = _ledge_s(0, 10)
    over(se, _ledge_e(0, 15))
    se[14, 10:16] = rgba("lp_k")
    sw = se[:, ::-1].copy()
    # inner corner: the east lip starts at the cap line and runs down
    inner = _ledge_e(9, 16)
    inner[9, 10:16] = LEDGE_S_ROWS[0, 2:8]
    # south lip ends
    s_left = _ledge_s(3, 16)
    s_left[9:15, 3] = rgba("lp_k")
    s_left[9, 3] = 0
    s_left[10:14, 4] = rgba("lp_l")
    s_right = s_left[:, ::-1].copy()
    return dict(S=s, E=e, W=w, SE=se, SW=sw, IN=inner, SL=s_left, SR=s_right)


LEDGES = {
    "S": (0x087, 0x08F, 0x097),
    "W": (0x085, 0x095, 0x0A5, 0x0FE, 0x106, 0x10E, 0x116, 0x11E, 0x126),
    "E": (0x086, 0x096, 0x0A6, 0x0FF, 0x107, 0x10F, 0x117, 0x11F, 0x127),
    "SW": (0x08D, 0x09D, 0x0AD),
    "SE": (0x08E, 0x09E, 0x0AE),
    "SL": (0x0D5, 0x0DD, 0x0E5),
    "SR": (0x0D6, 0x0DE, 0x0E6),
    "IN": (0x06E,),
}

GRASS_LEDGES = {0x087, 0x085, 0x086, 0x08D, 0x08E, 0x0D5, 0x0D6, 0x06E,
                0x0FE, 0x0FF, 0x106, 0x107}

# --------------------------------------------------------------------------
# Dry-stone wall
# --------------------------------------------------------------------------
# Rows 3-13 of a west-east wall, 16 px repeat: rounded capstones, then two
# courses laid with offset joints. Drafted from stone rectangles, finished
# by hand.
WALL_ROWS = art("""
    .hlh..h..hl..hl.
    lmmlklmklmmklmmk
    ldddkldklddklddk
    kkkkkkkkkkkkkkkk
    lkmhlhkmhlkmhlhk
    dkldddklddkldddk
    kkkkkkkkkkkkkkkk
    mhkmhlhkmhkmhlhk
    lmkllmmklmkllmmk
    ldkldddkldkldddk
    kkkkkkkkkkkkkkkk
""", LP)

# A north-south wall run, 5 px wide: stones stacked with a lit west edge.
WALL_V_ROWS = art("""
    klhlk
    kmmlk
    kdmmk
    kkkkk
    khlmk
    klmmk
    kddmk
    kkkkk
""", LP)


def wall_h(x0=0, x1=16):
    out = np.zeros((16, 16, 4), np.uint8)
    for x in range(x0, x1):
        out[3:14, x] = WALL_ROWS[:, x % 16]
    return out


def wall_end(side):
    """Wall run ending inside this metatile, with a squared end stone."""
    if side == "L":
        out = wall_h(2, 16)
        out[4:14, 2] = rgba("lp_k")
        out[4:13, 3] = rgba("lp_l")
        out[3, 2:4] = 0
        out[3, 3] = rgba("lp_h")
        return out
    return wall_end("L")[:, ::-1].copy()


def wall_v(x0):
    out = np.zeros((16, 16, 4), np.uint8)
    for y in range(16):
        out[y, x0:x0 + 5] = WALL_V_ROWS[y % 8]
    return out


# --------------------------------------------------------------------------
# Steles, herm, tripod plinth
# --------------------------------------------------------------------------
MB = dict(k="ink", d="mb_d", m="mb_m", l="mb_l", h="mb_h", g="gm", t="tc_m",
          y="sg_l", o="sg_d", e="tc_d")

# A marble stele: pediment top with a gold acroterion, an inscription band,
# standing on a plinth, with its shadow on the grass.
STELE = art("""
    ................
    .......kk.......
    ......khhk......
    .....khllmk.....
    ....kkkkkkkk....
    ....khhhhhlk....
    ....khkkkkmk....
    ....khlllllk....
    ....khkkkkmk....
    ....khlllllk....
    ....khkkkmmk....
    ....khlllmmk....
    ...kkkkkkkkkk...
    ...kmmmmmmmdkg..
    ....kkkkkkkkgg..
    ................
""", MB)

# A herm: a square stone pillar topped with a bearded head, the old
# boundary marker of Greek roads.
HERM = art("""
    ......kkkk......
    .....kmhhmk.....
    .....khlkmk.....
    .....kmlmmk.....
    .....kkdmdk.....
    ......kddk......
    .....kkkkkk.....
    .....khllmk.....
    .....khlmmk.....
    .....khlmmk.....
    .....khlmmk.....
    .....khlmdk.....
    .....khmmdk.....
    ....kkkkkkkk....
    ....kmmmmmdkgg..
    .....kkkkkkkgg..
""", MB)

# 130/131: the palaestra's marker, a bronze tripod on a marble plinth
# (top half on the top layer, plinth on the middle layer).
TRIPOD = art("""
    ................
    ................
    ................
    ................
    ................
    ................
    ...kkkkkkkkkk...
    ..kyyyyyyyyyyk..
    ..koyoooooooyk..
    ...koooooooook..
    ....kkoooookk...
    .....kkkkkkk....
    ....ko.ko.ok....
    ....ko.ko.ok....
    ...ko..ko..ok...
    ...ko..ko..ok...
    ..ko...ko...ok..
    ..kkkkkkkkkkkk..
    ..khhhhhhhhhlk..
    ..khkkkkkkkkmk..
    ..khkyoyyoykmk..
    ..khkkkkkkkkmk..
    ..khllllllllmk..
    ..khlllllllmmk..
    ..khllllllmmmk..
    ..khlllllmmmdk..
    .kkkkkkkkkkkkkk.
    .kmmmmmmmmmmmdkg
    ..kkkkkkkkkkkkgg
    ................
    ................
    ................
""", MB)

# --------------------------------------------------------------------------
# Boulders, steps, pebble mosaic, planters
# --------------------------------------------------------------------------
BOULDER = art("""
    ................
    ................
    .....kkkkk......
    ...kkhhllmkk....
    ..khhllllmmdk...
    ..khllmlmmmdk...
    .khlllmkmmmddk..
    .khllmkmmmmddk..
    .klllmmmmmdddk..
    .kllmmmmmmdddk..
    .kmlmmmmmdddkk..
    ..kmmmmmdddkk...
    ..kkdddddkkk....
    ....kkkkkk......
    ................
    ................
""", LP)
SEA_BOULDER = art("""
    ................
    ................
    .....kkkkk......
    ...kkhhllmkk....
    ..khhllllmmdk...
    ..khllmlmmmdk...
    .khlllmkmmmddk..
    .khllmkmmmmddk..
    .klllmmmmmdddk..
    .kllmmmmmmdddk..
    fkmlmmmmmdddkkf.
    .fkmmmmmdddkkf..
    ..fkkkkkkkkff...
    ...ffffffff.....
    ................
    ................
""", dict(k="ink", d="mb_d", m="mb_m", l="mb_l", h="mb_h", f="foam"))

STEPS = art("""
    hhhhhhhhhhhhhhhh
    llllllllllllllll
    llllllllllllllll
    mmmmmmmmmmmmmmmm
    dddddddddddddddd
    hhhhhhhhhhhhhhhh
    llllllllllllllll
    llllllllllllllll
    mmmmmmmmmmmmmmmm
    dddddddddddddddd
    hhhhhhhhhhhhhhhh
    llllllllllllllll
    llllllllllllllll
    mmmmmmmmmmmmmmmm
    dddddddddddddddd
    hhhhhhhhhhhhhhhh
""", MB)

# A pebble mosaic threshold: white and black river pebbles laid as a
# meander band around a rosette.
MOSAIC = art("""
    kkkkkkkkkkkkkkkk
    khhhhhhhhhhhhhhk
    khkkkkhhkkkkkhhk
    khkhhkhhkhhhkhhk
    khkhhkkkkhkhkhhk
    khhhhhhhhhkhhhhk
    khhhhhtthhhhhhhk
    khhhhtyytthhhhhk
    khhhhtyytthhhhhk
    khhhhhtthhhhhhhk
    khhhhkhhhhhhhhhk
    khhkhkhkkkkhkhhk
    khhkhhhkhhkhhkhk
    khhkkkkkhhkkkkhk
    khhhhhhhhhhhhhhk
    kkkkkkkkkkkkkkkk
""", MB)

# A limestone trough of anemones (General's flower boxes).
PLANTER = art("""
    ..ff..ff..ff..f.
    .frrf.frf.frrf..
    .frcrfrcrffrcrf.
    ..ffs.ffs..ffs..
    kkkkkkkkkkkkkkkk
    khhhhhhhhhhhhhhk
    klllllllllllllck
    kkkkkkkkkkkkkkkk
    ..ff..ff..ff..f.
    .frrf.frf.frrf..
    .frcrfrcrffrcrf.
    ..ffs.ffs..ffs..
    kkkkkkkkkkkkkkkk
    khhhhhhhhhhhhhhk
    klllllllllllllck
    kkkkkkkkkkkkkkkk
""", dict(k="ink", h="lp_h", l="lp_l", f="fl_d", r="fl_m", c="ink", s="gm"))


def on_grass(sprite):
    g = TEX["grass"].copy()
    return over(g, sprite)


def paint(sheet, base):
    # ledges: keep the terrain pass's ground on the bottom layer
    pieces = ledge_pieces()
    for kind, ids in LEDGES.items():
        for m in ids:
            sheet.view(m, M)[:] = 0
            sheet.view(m, T)[:] = 0
            sheet.set(m, M, pieces[kind])
    # Grass ledges: plain grass underneath, and the lip's shadow on the lower
    # ground below south-facing runs.
    shade = {"S": (0, 16), "SL": (3, 16), "SR": (0, 13), "SE": (0, 10), "SW": (6, 16)}
    for kind, ids in LEDGES.items():
        for m in ids:
            if m not in GRASS_LEDGES:
                continue
            g = TEX["grass"].copy()
            if kind in shade:
                a, b = shade[kind]
                g[15, a:b] = rgba("gm")
            sheet.set(m, B, g)

    grass = TEX["grass"]

    def put(m, layer, img, ground=True):
        sheet.clear(m)
        lower = B if layer == M else M
        if ground:
            sheet.set(m, lower, grass)
        sheet.set(m, layer, img)

    # dry-stone walls
    put(0x149, M, wall_h())
    put(0x148, M, wall_end("L"))
    put(0x14A, M, wall_end("R"))
    put(0x138, T, wall_end("L"))
    put(0x13A, T, wall_end("R"))
    put(0x134, M, wall_h())
    put(0x132, M, wall_v(2))
    put(0x133, M, wall_v(9))
    for m in (0x139, 0x140):
        put(m, T, wall_v(2))
    for m in (0x141, 0x142):
        put(m, T, wall_v(9))

    # stele (003 is one layer: grass under the stone in the same tiles)
    sheet.clear(0x003)
    sheet.set(0x003, M, on_grass(STELE))
    put(0x01B, M, HERM)
    # palaestra marker: tripod (top layer) over its plinth (middle layer)
    sheet.clear(0x130)
    sheet.set(0x130, M, grass)
    sheet.set(0x130, T, TRIPOD[0:16].copy())
    put(0x131, M, TRIPOD[16:32].copy())

    # boulders: land boulders over the terrain's ground, sea boulders over water
    for m in (0x0E0, 0x0E1, 0x0E2):
        sheet.view(m, M)[:] = 0
        sheet.set(m, M, BOULDER)
    for m in (0x0C5, 0x0CD, 0x18C, 0x194):
        sheet.view(m, M)[:] = 0
        sheet.view(m, T)[:] = 0
        sheet.set(m, M, SEA_BOULDER)
    sheet.view(0x0BD, T)[:] = 0
    sheet.set(0x0BD, T, SEA_BOULDER)

    # marble steps, mosaic threshold, planters
    for m in (0x0AF, 0x0CF):
        sheet.clear(m)
        sheet.set(m, M, STEPS)
    sheet.clear(0x024)
    sheet.set(0x024, M, MOSAIC)
    for m in (0x005, 0x006, 0x007):
        sheet.clear(m)
        sheet.set(m, M, PLANTER)
