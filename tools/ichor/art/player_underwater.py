"""Canonical swimming source adapter; legacy --write is rejected.

Four 32x32 source frames: south, north, west and the retained spare east.
The engine aliases its nine walking image slots onto the first three.
"""
import argparse
from pathlib import Path

import numpy as np

import sprites_player_ow as player
import player_sources

PALETTE = Path(player.PALDIR) / "player_underwater.pal"
ROLES = {
    ".": 0, "k": 15, "s": 1, "S": 2, "d": 3, "b": 4,
    "c": 5, "C": 6, "D": 7, "h": 8, "H": 15,
    "W": 9, "y": 10, "Y": 11, "t": 12, "T": 13, "w": 14,
}

TORSO = {
    "down": """
...kcCkddkCDk...
..kcCCywwkCDDk..
...kCCwwwwCDDk..
...kCkwwwwkDk...
....kbbbbbbk....
....kwWWWwk.....
""",
    "up": """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
...kCCCDCCCDDk..
...kCCCDCCDDk...
....ktDDDDTk....
....kwWWWwk.....
""",
    "left": """
..kSdkcCDk......
...kSwwkcCDk....
....kwwkcCCDk...
.....kwwkCCDDk..
......kbbktTkDk.
.......kwWWkkDk.
""",
}

# Raised forearms return from wide elbows; the two kicking legs have
# separately placed knee/ankle bends rather than straight vertical shins.
ARM = """
..kSSk..
..kSsk..
.kSSdk..
kSSdkk..
ksdkkSsk
.kk..kSk
......kk
"""
KICK_LEFT = """
.....kSdk
...kkSSdk
.kkSSdkk.
kSSdkk...
kSdk.....
kbbkk....
.kbbk....
..kk.....
"""
KICK_RIGHT = """
kSdk.....
kSSdkk...
.kkSSdkk.
...kkSSdk
.....kSdk
....kkbbk
....kbbk.
.....kk..
"""
SIDE_ARM = """
...kSSk...
..kSSSk...
.kSddkk...
kSSdk..kk.
kSdkkkkSdk
.kkkkkSSdk
.....kkkk.
"""
SIDE_KICK = """
.kSSdkk.......
kSSSSSSdkk....
.kkkSSSSSSdk..
....kkkkSSSdk.
.......kSSdk..
.....kkSdkk...
....kbbbbk....
.....kkkk.....
"""
SIDE_REAR_KICK = """
..kSSdkk....
.kSSSSSSdk..
..kkkkSSSdk.
.....kSSdk..
...kkSdkk...
..kbbbbk....
...kkkk.....
"""


def part(source):
    return player.parse(source, width=None)


def palette():
    lines = PALETTE.read_text().splitlines()
    assert lines[:3] == ["JASC-PAL", "0100", "16"]
    # Preserve the existing file and its exact hardware colors, not expanded
    # 8-bit display values from the original upstream PNG.
    return [tuple(int(v) & 0xF8 for v in line.split()) for line in lines[3:19]]


def legacy_frames(who):
    result = []
    roles = dict(ROLES)
    if who == "ianthe":
        roles.update(h=4, H=8)
    for facing in ("down", "up", "left"):
        hat = player.HAT_SIDE if facing == "left" else player.HAT_FRONT
        if facing == "left":
            limbs = [
                (part(SIDE_REAR_KICK), 13, 19),
                (part(SIDE_KICK), 16, 20),
                (part(SIDE_ARM), 2, 13),
                (player.parse(TORSO[facing]), 10, 14),
            ]
            head_x = 6
        else:
            limbs = [
                (part(KICK_LEFT), 6, 21),
                (part(KICK_RIGHT), 17, 21),
                (part(ARM), 3, 13),
                ([row[::-1] for row in part(ARM)], 21, 13),
                (player.parse(TORSO[facing]), 8, 15),
            ]
            head_x = 8
        rows = player.compose(limbs + [
            (player.parse(hat), head_x, 4),
            (player.parse(player.FACES[who][facing]), head_x, 10),
        ], w=32, h=32)
        result.append(np.array([[roles[ch] for ch in row] for row in rows], dtype=np.uint8))
    result.append(np.fliplr(result[2]).copy())
    return result


def frames(who):
    return [frame.copy() for frame in np.hsplit(
        np.array(player_sources.source_image(who, "underwater")), 4)]


def assets():
    return {
        who: (Path(player.PEOPLE) / folder / "underwater.png", np.hstack(frames(who)))
        for who, folder in (("theo", "brendan"), ("ianthe", "may"))
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        for path, array in assets().values():
            player.save_sheet(array, palette(), path)


if __name__ == "__main__":
    main()
