"""Theo and Ianthe riding the dolphin (Poseidon's Conch), 32x32 surfing sheets.

Usage:
    python3 tools/ichor/art/surf_poses.py [--write]

--write    retired; rejects protected player PNG writes

Six frames, Emerald's layout: 0 south sitting, 1 south hopping on or off,
2 north sitting, 3 north hopping, 4 west sitting, 5 west hopping (east is west
mirrored in game). The rider sits astride the surf mount (field_effects.py
draws the dolphin under it), shins down its flanks.

build() reads the canonical model-led sprites. The historical drawing parts
remain reference helpers, not the current art producer.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import sprites_player_ow as P  # noqa: E402
import player_sources  # noqa: E402

# Seated bodies, in sprites_player_ow role letters (k ink, s S d skin, c C D
# chlamys, w W chiton, y Y straw, t T terracotta, b brown). They start on the
# row under the chin.
SEAT = {
    'down': """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCDDk.
.kskkbbbbbbkksk.
..kkwwwwwwwWkk..
.kSdkwwwwwWkSdk.
.kSdkkkkkkkkSdk.
.kSdk......kSdk.
.kbbk......kbbk.
""",
    'up': """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDDk.
.ksCCCCDCCCDDsk.
..ktDDDDDDDDDk..
.kSdkWwwwwWkSdk.
.kSdkkkkkkkkSdk.
.kSdk......kSdk.
.kbbk......kbbk.
""",
    'left': """
....kSdkcCDk....
...kwwwkcCCDk...
..kSwwkcCCCDDk..
.kSdwwkCCDCDDDk.
.kskbbksdtTkDDk.
...kwwwwwWkDDk..
...kSSSSSdkkk...
....kkkkSdk.....
.......kSdk.....
.......kbbk.....
""",
}

# Hopping on or off: knees drawn up, hands out for balance.
HOP = {
    'down': """
...kcCkddkCDk...
.kkcCCkwwkCCDkk.
ksSkcCyCwwCCDksk
kskCCkwwwwkCDDkk
.kkkkbbbbbbkkkk.
..kkwwwwwwwWkk..
..kSdwwwwwWSdk..
..kbbkkkkkkbbk..
""",
    'up': """
...kcCCCCCCDk...
.kkcCCCCCCCDDkk.
ksScCCCCDCCCDDsk
kskcCCCCDCCCDDkk
.kkDDDDDDDDDDkk.
..ktDDDDDDDDDk..
..kSdWwwwwWSdk..
..kbbkkkkkkbbk..
""",
    'left': """
....kSdkcCDk....
.kSkwwwkcCCDk...
.ksdwwkcCCCDDk..
..kkwwkCCDCDDDk.
...kbbksdtTkDDk.
..kSSSSSdkDDk...
..kbbkkSdkk.....
.......kbbk.....
""",
}

HAT_Y, FACE_Y, BODY_Y = 5, 11, 16
X0 = 8


def rider(who, facing, hop=False):
    body = (HOP if hop else SEAT)[facing]
    dy = -2 if hop else 0
    hat = P.HAT_SIDE if facing == 'left' else P.HAT_FRONT
    return P.compose([(P.parse(body), X0, BODY_Y + dy),
                      (P.parse(hat), X0, HAT_Y + dy),
                      (P.parse(P.FACES[who][facing]), X0, FACE_Y + dy)], w=32, h=32)


def frames(who):
    return [rider(who, f, hop) for f in ('down', 'up', 'left') for hop in (False, True)]


def build(sheet):
    """sheet: 'brendan' (Theo) or 'may' (Ianthe) -> 32x192 index array."""
    who = {'brendan': 'theo', 'may': 'ianthe'}[sheet]
    return np.array(player_sources.source_image(who, "surfing"))


def main():
    if '--write' in sys.argv:
        for sheet, who in (('brendan', 'theo'), ('may', 'ianthe')):
            _, rgb, roles = P.CHARS[who]
            arr = P.to_index(frames(who), roles)
            P.save_sheet(arr.astype(np.uint8), rgb, os.path.join(P.PEOPLE, sheet, 'surfing.png'))


if __name__ == '__main__':
    main()
