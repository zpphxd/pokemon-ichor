"""Theo's and Ianthe's overworld sheets: walking, running, fishing and field move.

They replace Brendan's and May's sheets in graphics/object_events/pics/people/
brendan/ and may/, and recolor graphics/object_events/palettes/brendan.pal and
may.pal by role (see design/phase1/SPRITES_player_ow.md).

Every frame is built from hand-edited ASCII parts: a petasos, a face per
facing and per character, and a body per pose. The parts use role letters,
which map to each character's palette indices, so one body serves both.

Usage:
    python3 tools/ichor/art/sprites_player_ow.py [--write [--sheets NAME ...]] [--preview OUT.png]

--write    writes the sheets (default: all four) for both characters, and the
           two palettes
--preview  writes every sheet for both characters at 4x to OUT.png
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, bresenham  # noqa: E402

PEOPLE = os.path.join(ROOT, "graphics/object_events/pics/people")
PALDIR = os.path.join(ROOT, "graphics/object_events/palettes")

# --------------------------------------------------------------------------
# Palettes, by role
# --------------------------------------------------------------------------
# brendan.pal and may.pal are shared with every player sheet (bike, surf,
# watering, ...) and the rival sprites, so each index keeps the role it had in
# Emerald and is recolored by role. The two palettes never had the same roles:
#
#   idx  brendan.pal (Theo)              may.pal (Ianthe)
#   1-4  skin, light -> outline          skin, light -> outline
#   5-8  navy, light -> dark             5 gray, 6 dark slate, 7-8 hair brown
#   9    light gray                      light gray
#   10-11 green                          green
#   12-13 red                            red
#   14   white                           white (also the "!" emote)
#   15   black                           black (also the "!" emote)

TRANSPARENT = (115, 197, 164)  # Emerald's value, kept as is

INK = (32, 24, 24)
SKIN = [(248, 208, 168), (232, 160, 112), (184, 112, 72), (104, 56, 40)]
AEGEAN = [(112, 168, 224), (48, 104, 176), (24, 56, 120)]
CREAM = [(248, 240, 208), (216, 192, 144)]
STRAW = [(240, 192, 64), (200, 144, 40)]
TERRA = [(224, 136, 88), (184, 88, 48)]

THEO_RGB = [TRANSPARENT,
            SKIN[0], SKIN[1], SKIN[2], SKIN[3],        # 1-4 skin
            AEGEAN[0], AEGEAN[1], AEGEAN[2],           # 5-7 navy -> chlamys
            (48, 48, 64),                              # 8 navy -> black hair sheen
            CREAM[1],                                  # 9 light gray -> chiton shade
            STRAW[0], STRAW[1],                        # 10-11 green -> petasos straw
            TERRA[0], TERRA[1],                        # 12-13 red -> satchel
            CREAM[0],                                  # 14 white -> chiton
            INK]                                       # 15 black -> ink

IANTHE_RGB = [TRANSPARENT,
              SKIN[0], SKIN[1], SKIN[2], SKIN[3],      # 1-4 skin
              AEGEAN[1], AEGEAN[2],                    # 5 gray, 6 slate -> chlamys
              (128, 80, 48), (72, 40, 32),             # 7-8 hair brown -> dark-brown braid
              CREAM[1],                                # 9 light gray -> chiton shade
              STRAW[0], STRAW[1],                      # 10-11 green -> petasos straw
              TERRA[0], TERRA[1],                      # 12-13 red -> satchel
              CREAM[0],                                # 14 white -> chiton
              INK]                                     # 15 black -> ink

# role letter -> palette index, per character
ROLE_THEO = {
    'k': 15, 's': 1, 'S': 2, 'd': 3, 'b': 4,
    'c': 5, 'C': 6, 'D': 7, 'h': 8, 'H': 15,
    'W': 9, 'y': 10, 'Y': 11, 't': 12, 'T': 13, 'w': 14,
}
ROLE_IANTHE = dict(ROLE_THEO, c=5, C=5, D=6, h=7, H=8)

# --------------------------------------------------------------------------
# Parts
# --------------------------------------------------------------------------
# k ink        s S d  skin light, mid, shadow   b brown (sandals, rod, band)
# c C D        chlamys light, mid, dark         h H  hair light, dark
# w W          chiton cream, shade              y Y  straw light, dark
# t T          satchel terracotta light, dark   .    transparent

HAT_FRONT = """
.....kkkkkk.....
..kkkywyyyYkkk..
.kyykyyyyYYkyYk.
kyyyybbbbbbyyYYk
kyyyyyyyyyyyyYYk
.kYYYYYYYYYYYYk.
"""
HAT_SIDE = """
......kkkkk.....
....kkywyyYkk...
.kkyykyyyYYkYkk.
kyyyyybbbbbyyyYk
kyyyyyyyyyyyyYYk
.kYYYYYYYYYYYYk.
"""

FACES = {
    'theo': {
        'down': """
...kHhhhhhhHk...
...khSssssShk...
...ksskssksSk...
...kssssssSdk...
....kSsssSdk....
""",
        'up': """
...kHhhhhhhHk...
...khhhhhhhHk...
...kHhhhhhHHk...
...kHHhhhHHHk...
....kkSddSkk....
""",
        'left': """
..kSShhhhhhhHk..
..ksssShhhhhHk..
..kskSdShhhhHk..
..kssssdShhHk...
...kSSSdkHHk....
""",
    },
    'ianthe': {
        'down': """
..kHhhhHHhhhHk..
..khSssssssShk..
..khsskssksSHk..
..khssssssSdHk..
..kHkSsssSdkHk..
""",
        'up': """
..kHhhhhhhhhHk..
..khhhhhhhhhHk..
..kHhhhhhhhHHk..
..kHHhhhhhHHHk..
...kHHhhhHHHk...
......khHk......
......kHhk......
......khHk......
......kHhk......
......ktTk......
.......kk.......
""",
        'left': """
..kSShhhhhhhHk..
..ksssShhhhhhHk.
..kskSdShhhhhHk.
..kssssdShhhHHk.
...kSSSdkhHHHk..
..........khHk..
..........kHhk..
..........khHk..
..........ktTk..
...........kk...
""",
    },
}

# Bodies start on the row under the chin. Walking frames bob down 1 px.
BODY = {
    'down': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCDDk.
.kskkbbbbbbkksk.
..kkwwwwwWtTkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'down_a': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCDDk.
.kskkbbbbbbkkDk.
..kkwwwwwWtTksk.
...kWwwwwWTTkk..
....kSdkkSdk....
....kbbkkSdk....
.....kk.kbbk....
""",
    'down_b': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCDDk.
.kCkkbbbbbbkksk.
.kskwwwwwWtTkk..
..kkWwwwwWTTk...
....kSdkkSdk....
....kSdkkbbk....
....kbbk.kk.....
""",
    'up': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
.ksCCCCDCCCDDsk.
..ktDDDDDDDDDk..
...kTkWwwwWWk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'up_a': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
.ksCCCCDCCCDDDk.
..ktDDDDDDDDDsk.
...kTkWwwwWWkk..
....kSdkkSdk....
....kbbkkSdk....
.....kk.kbbk....
""",
    'up_b': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
.kcCCCCDCCCDDsk.
.kstDDDDDDDDDk..
..kkTkWwwwWWk...
....kSdkkSdk....
....kSdkkbbk....
....kbbk.kk.....
""",
    'left': """
....kSdkcCDk....
...kwwwkcCCDk...
...kwwkcCCCDDk..
...kWwkCCDCDDDk.
...kbbksdtTkDDDk
...kwwWWTTkDDDk.
....kWWWkkDDk...
....kSdk........
....kSdk........
...kbbbk........
""",
    'left_a': """
....kSdkcCDk....
...kwwwkcCCDk...
...kwwkcCCCDDk..
..kkWwkCCDCDDDDk
.ksdbbbkTTkDDDk.
..kkwwWWTTkDDk..
...kWWWWWkkkk...
...kSdkkSdk.....
..kSdk...kdbk...
.kbbbk...kbbbk..
""",
    'left_b': """
....kSdkcCDk....
...kwwwkcCCDk...
...kwwkcCCCDDk..
...kWwkCCDCDDDDk
...kbbkCsdDDDDk.
...kwwWTTkDDDk..
...kWWWWWkkk....
...kdbkkSdk.....
..kdbk...kSdk...
.kbbbk...kbbbk..
""",
    # Running: crouched and leaning, fists pumping, the chlamys flaring out
    # behind, and the Talaria's little wings at the heels. 9 rows: the
    # standing pose sits 1 px lower than walking, the strides 2 px lower.
    'run_down': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCykwwkCCDDk.
.kCCksSwwSdkCDk.
kcCkkbbbbbbkkCDk
kCCkwwwwwWtTkDDk
.kkkWwwwwWTTkkk.
..wkSdk..kSdkw..
...kbbk..kbbk...
""",
    'run_down_a': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCykwwkCCDDk.
.kCCksSwwkCCkDk.
kcCkkbbbbbbkkCDk
kCCkwwwwwWtTkDDk
.kkkWwwwwWTTkkk.
..wkbbk..kSdk...
...kkk...kbbkw..
""",
    'run_down_b': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCykwwkCCDDk.
.kDkCCkwwSdkCDk.
kcCkkbbbbbbkkCDk
kCCkwwwwwWtTkDDk
.kkkWwwwwWTTkkk.
...kSdk..kbbkw..
..wkbbk...kkk...
""",
    'run_up': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
kcCCCCCDCCCCCDDk
kCtTDDDDDDDDDDDk
.kTkkWwwwwWWkkk.
..wkSdk..kSdkw..
...kbbk..kbbk...
""",
    'run_up_a': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
kcCCCCCDCCCCCDDk
kCtTDDDDDDDDDDDk
.kTkkWwwwwWWkkk.
..wkbbk..kSdk...
...kkk...kbbkw..
""",
    'run_up_b': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
kcCCCCCDCCCCCDDk
kCtTDDDDDDDDDDDk
.kTkkWwwwwWWkkk.
...kSdk..kbbkw..
..wkbbk...kkk...
""",
    'run_left': """
.....kSdkcCDk...
....kwwwkcCCDDk.
...ksdwwkcCCCDDk
...kkWwkCCDDCDDk
....kbbkdtTkCDDk
....kwwWWTTk.kk.
...kWWWWWWk.....
..wkSdkkSdk.....
..kbbbkkbbbk....
""",
    'run_left_a': """
.....kSdkcCDk...
....kwwwkcCCDDk.
..kskwwwkcCCCDDk
..kdkWwkCCDDCDDk
....kbbkdtTkCDDk
...kkwwWWTTk.kk.
..kSdWWWWkSdk...
.kSdk....kSdkw..
kbbbk.....kbbk..
""",
    'run_left_b': """
.....kSdkcCDk...
....kwwwkcCCDDk.
...kwwwkCcCCCDDk
...kWwkCsdDDCDDk
....kbbkkTTkCDDk
...kkwwWWTTk.kk.
..kdbWWWWkSdk...
.kdbk....kSdkw..
kbbbk.....kbbk..
""",
    # Fishing: both hands on the rod.
    'fish_left': """
....kSdkcCDk....
...kwwwkcCCDk...
.ksSSSkcCCCDDk..
.kdkkkwkCDCDDDk.
...kbbkCtTkDDDDk
...kwwWWTTkDDDk.
....kWWWkkDDk...
....kSdk........
....kSdk........
...kbbbk........
""",
    'fish_left_cast': """
....kSdkcCDk....
...kwwwkcCCDk...
kssSSkwkcCCDDk..
kdkkkwwkCDCDDDk.
...kbbkCtTkDDDDk
...kwwWWTTkDDDk.
....kWWWkkDDk...
....kSdk........
....kSdk........
...kbbbk........
""",
    'fish_up': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
.kcCCCCDCCCDDDk.
..ktDDDDDDDDDk..
...kTkWwwwWWk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'fish_up_side': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
.kcCCCCDCCCDDsk.
..ktDDDDDDDDDdk.
...kTkWwwwWWk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'fish_down_side': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.ksdCyCwwCCCDDk.
.kdkCkwwwwkCDDk.
..kkkbbbbbbkksk.
..kkwwwwwWtTkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'fish_down_front': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCksSSdkCDDk.
..kCkbbbbbbkDk..
..kkwwwwwWtTkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    # Field move: reach into the satchel, bring out the relic, raise it.
    'fm_reach': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCDDk.
.kskkbbbbbbkCDk.
..kkwwwwwWsdkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'fm_reach_in': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCDDk.
.kskkbbbbbbkCDk.
..kkwwwwwWtkDk..
...kWwwwwWskk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'fm_hold': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCykkkkCCDDk.
.kCCksywYkkCDDk.
.kCCksYYbkbkksk.
..kkwkkkkWtTkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    'fm_raise': """
...kcCkddkCDk...
..kwwCkwwkCCDk..
..kwCyCwwCCCDDk.
..kkCkwwwwkCDDk.
...kkbbbbbbkksk.
..kkwwwwwWtTkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
}


def parse(s, width=16):
    rows = s.strip('\n').split('\n')
    for r in rows:
        assert width is None or len(r) == width, (len(r), r)
    return rows


def compose(parts, w=16, h=32):
    """Layers in drawing order: (rows, x, y) blocks or callables on the grid."""
    a = [['.'] * w for _ in range(h)]
    for part in parts:
        if callable(part):
            part(a)
            continue
        rows, x0, y0 = part
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.':
                    y, x = y0 + j, x0 + i
                    assert 0 <= y < h and 0 <= x < w, (x, y)
                    a[y][x] = ch
    return a


def rod(p0, p1, over=False):
    """The Old Rod: a cane line from the grip p0 to the tip p1, brown with a
    straw-gold highlight on its lit side and a terracotta float at the tip.
    The highlight fills only empty pixels unless `over` (a rod crossing the
    body needs both pixels to read)."""
    def draw(a):
        pts = bresenham(*p0, *p1)
        steep = abs(p1[1] - p0[1]) >= abs(p1[0] - p0[0])
        for x, y in pts:
            a[y][x] = 'b'
        for x, y in pts[:-1]:
            hx, hy = (x - 1, y) if steep else (x, y - 1)
            if 0 <= hx < len(a[0]) and 0 <= hy < len(a) and (a[hy][hx] == '.' or over and (hx, hy) not in pts):
                a[hy][hx] = 'Y'
        x, y = pts[-1]
        a[y][x] = 't'
    return draw


def figure(who, facing, body, dy=0, hx=0, hy=0, bx=0, x0=0, w=16):
    """One standing/walking/running figure; x0 places it in a wider frame."""
    hat = HAT_SIDE if facing == 'left' else HAT_FRONT
    return [(parse(BODY[body]), x0 + bx, 21 + dy),
            (parse(hat), x0 + hx, 10 + dy + hy),
            (parse(FACES[who][facing]), x0 + hx, 16 + dy + hy)]


def walking(who):
    f = lambda *a, **k: compose(figure(who, *a, **k))  # noqa: E731
    return [
        f('down', 'down'), f('up', 'up'), f('left', 'left'),
        f('down', 'down_a', dy=1), f('down', 'down_b', dy=1),
        f('up', 'up_a', dy=1), f('up', 'up_b', dy=1),
        f('left', 'left_a', dy=1), f('left', 'left_b', dy=1),
    ]


def running(who):
    f = lambda *a, **k: compose(figure(who, *a, **k))  # noqa: E731
    return [
        f('down', 'run_down', dy=1), f('up', 'run_up', dy=1), f('left', 'run_left', dy=1),
        f('down', 'run_down_a', dy=2), f('down', 'run_down_b', dy=2),
        f('up', 'run_up_a', dy=2), f('up', 'run_up_b', dy=2),
        f('left', 'run_left_a', dy=2), f('left', 'run_left_b', dy=2),
    ]


# Fishing and the field move use 32x32 frames with the figure centered (x+8).
# Fishing: 0-3 west (rod over the shoulder, raised, cast, out), 4-7 north,
# 8-11 south. A bite alternates frames 2/3, 6/7 or 10/11.

def fishing(who):
    def f(facing, body, before=(), after=(), **k):
        return compose(list(before) + figure(who, facing, body, x0=8, **k) + list(after), w=32)
    return [
        f('left', 'fish_left', before=[rod((10, 22), (31, 4))]),
        f('left', 'fish_left', before=[rod((10, 22), (22, 0))]),
        f('left', 'fish_left_cast', hx=-1, hy=1, after=[rod((8, 23), (1, 9))]),
        f('left', 'fish_left_cast', hx=-1, hy=1, after=[rod((8, 23), (0, 19))]),
        f('up', 'fish_up_side', after=[rod((22, 21), (22, 31))]),
        f('up', 'fish_up_side', after=[rod((22, 21), (25, 31))]),
        f('up', 'fish_up_side', after=[rod((22, 22), (26, 5))]),
        f('up', 'fish_up', before=[rod((15, 22), (15, 1))]),
        f('down', 'fish_down_side', before=[rod((10, 27), (10, 1))]),
        f('down', 'fish_down_side', after=[rod((9, 22), (3, 6))]),
        f('down', 'fish_down_front', after=[rod((14, 25), (6, 31), over=True)]),
        f('down', 'fish_down_front', after=[rod((15, 25), (15, 31), over=True)]),
    ]


# Field move: Aethos has no HM Pokemon; field powers come from relics (the
# Labrys, the Bronze Hammer, Hecate's Torch...). The player reaches into the
# satchel, brings out the relic and raises it, glinting.
ARM_MID = """
.kkk.....
kwyYk....
kyYYk....
kYYbk....
.ksdk....
.kSdk....
.kSdk....
.kSdk....
.kSSkkkk.
..kSSwwWk
...kkkwWk
"""
ARM_HIGH = """
....y.......
.w..w..w....
..y...y.....
....kkk.....
wy.kwyYk.yw.
...kyYYk....
...kYYbk....
..y.kkk.y...
.w..ksk..w..
....kSdk....
....kSdk....
.....kSdk...
.....kSdk...
......kSdk..
......kwWk..
.......kwWk.
.......kwWk.
........kwWk
........kwWk
.........kwk
"""


def field_move(who):
    def f(body, after=()):
        return compose(figure(who, 'down', body, x0=8) + list(after), w=32)
    return [
        f('fm_reach'),
        f('fm_reach_in'),
        f('fm_hold'),
        f('fm_raise', after=[(parse(ARM_MID, None), 2, 10)]),
        f('fm_raise', after=[(parse(ARM_HIGH, None), 0, 1)]),
    ]


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def to_index(frames, roles):
    w = sum(len(f[0]) for f in frames)
    out = np.zeros((32, w), np.uint8)
    x = 0
    for f in frames:
        for y, row in enumerate(f):
            for i, ch in enumerate(row):
                if ch != '.':
                    out[y, x + i] = roles[ch]
        x += len(f[0])
    return out


def save_sheet(arr, rgb, path):
    im = Image.fromarray(arr, "P")
    flat = []
    for c in rgb:
        flat.extend(c)
    im.putpalette(flat)
    im.save(path, bits=4, transparency=0)


def write_pal(rgb, path):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in rgb:
            f.write("%d %d %d\n" % c)


def rgba(arr, rgb):
    h, w = arr.shape
    out = np.zeros((h, w, 4), np.uint8)
    for i, c in enumerate(rgb):
        m = arr == i
        out[m, :3] = c
        out[m, 3] = 0 if i == 0 else 255
    return Image.fromarray(out, "RGBA")


CHARS = {
    'theo': ('brendan', THEO_RGB, ROLE_THEO),
    'ianthe': ('may', IANTHE_RGB, ROLE_IANTHE),
}
SHEETS = {'walking': walking, 'running': running, 'fishing': fishing, 'field_move': field_move}


def build(who):
    _, rgb, roles = CHARS[who]
    return {name: to_index(fn(who), roles) for name, fn in SHEETS.items()}


def preview(path, built, k=4):
    """Every sheet for both characters at k x, on a pale-grass ground, with a
    tick between frames."""
    bg, ink = (168, 200, 120, 255), (40, 40, 48)
    lab, pad = 16, 6
    rows = [(f"{who.capitalize()}: {name.replace('_', ' ')}", rgba(arr, CHARS[who][1]), name)
            for who, sheets in built.items() for name, arr in sheets.items()]
    width = max(im.width for _, im, _ in rows) * k + 2 * pad
    out = Image.new("RGB", (width, sum(lab + 32 * k + pad for _ in rows) + pad), (232, 228, 216))
    d = ImageDraw.Draw(out)
    y = pad
    for label, im, name in rows:
        d.text((pad, y + 2), label, fill=ink)
        y += lab
        base = Image.new("RGBA", im.size, bg)
        base.alpha_composite(im)
        out.paste(base.resize((im.width * k, im.height * k), Image.NEAREST), (pad, y))
        fw = 16 if name in ('walking', 'running') else 32
        for x in range(fw, im.width, fw):
            d.line([(pad + x * k, y), (pad + x * k, y + 5)], fill=ink)
        y += 32 * k + pad
    out.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sheets", nargs="+", choices=list(SHEETS), default=list(SHEETS),
                    help="which sheets --write writes (default: all)")
    ap.add_argument("--preview")
    args = ap.parse_args()
    built = {who: build(who) for who in CHARS}
    if args.write:
        for who, sheets in built.items():
            folder, rgb, _ = CHARS[who]
            for name in args.sheets:
                save_sheet(sheets[name], rgb, os.path.join(PEOPLE, folder, name + ".png"))
            write_pal(rgb, os.path.join(PALDIR, folder + ".pal"))
    if args.preview:
        preview(args.preview, built)


if __name__ == "__main__":
    main()
