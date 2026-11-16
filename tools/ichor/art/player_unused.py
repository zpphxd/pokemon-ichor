"""Canonical watering/decorating source adapter and historical drawing parts.

--check validates the four PNGs. Legacy --write is rejected; shared palettes
and unused-system eligibility remain untouched.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import sprites_player_ow as player
import player_sources


WATER_BODY = {
    "down": """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kccCyCwwCCCDDk.
.kCCCkwwwwkCsk..
.kskkbbbbbbkSsk.
..kkwwwwwWtTkk..
...kWwwwwWTTk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    "up": """
...kcCCCCCCDk...
..kcCCCCCCCDDk..
.kcCCCCDCCCCDDk.
.kcCCCCDCCCCDsk.
.ksCCCCDCCCDDsk.
..ktDDDDDDDDDk..
...kTkWwwwWWk...
....kSdkkSdk....
....kSdkkSdk....
....kbbkkbbk....
""",
    "left": """
....kSdkcCDk....
...kwwwkcCCDk...
...kwwkcCCCDDk..
..ksSwkCCDCDDDDk
.ksdbbbkTTkDDDk.
..kkwwWWTTkDDk..
....kWWWkkDDk...
....kSdk........
....kSdk........
...kbbbk........
""",
}

JUG = (
    """
..kkk...
.kwtTk..
.kttTTk.
kktTTTk.
.ktTTTk.
..kTTk..
...kk...
""",
    """
...kk...
..kwTk..
.kttTTkk
kktTTTtk
.ktTTTk.
..kTTk..
...kk...
""",
)

CROUCH = """
...kcCkddkCDk...
..kcCCkwwkCCDk..
.kCCksSwwSdkCDk.
..kCCkttTkCCDk..
...kkkTTTkkkk...
..kwWkbbbkWWk...
...kbbk..kbbk...
"""


def watering(who):
    frames = []
    for facing in ("down", "up", "left"):
        for phase in (0, 1):
            hat = player.HAT_SIDE if facing == "left" else player.HAT_FRONT
            jug = player.parse(JUG[phase], 8)
            if facing == "left":
                jug = [row[::-1] for row in jug]
            x = 0 if facing == "left" else 23
            parts = [
                (player.parse(WATER_BODY[facing]), 8, 21),
                (player.parse(hat), 8, 10),
                (player.parse(player.FACES[who][facing]), 8, 16),
                (jug, x, 22),
            ]
            frame = player.compose(parts, w=32)
            if facing == "left":
                frame[25][8] = "s"
                frame[25][9] = "S"
                drops = [(0, 28), (1, 30)] if phase else [(0, 29)]
            elif facing == "up":
                frame[24][22] = "s"
                drops = [(30, 28), (29, 30)] if phase else [(30, 29)]
            else:
                frame[24][22] = "s"
                drops = [(30, 28), (29, 30)] if phase else [(30, 29)]
            for dx, dy in drops:
                frame[dy][dx] = "c"
                frame[dy + 1][dx] = "C"
            frames.append(frame)
    return frames


def decorating(who):
    return [player.compose([
        (player.parse(CROUCH), 0, 24),
        (player.parse(player.HAT_FRONT), 0, 13),
        (player.parse(player.FACES[who]["down"]), 0, 19),
    ])]


SHEETS = {"watering": watering, "decorating": decorating}


def build():
    return {
        (who, name): np.array(player_sources.source_image(who, name))
        for who in player.CHARS
        for name in SHEETS
    }


def check(built, written=False):
    for (who, name), arr in built.items():
        folder, rgb, _ = player.CHARS[who]
        expected = (32, 192 if name == "watering" else 16)
        assert arr.shape == expected, (who, name, arr.shape)
        assert arr.max() <= 15 and np.any(arr == 0), (who, name, "indices")
        if name == "watering":
            frames = np.hsplit(arr, 6)
            assert all(np.count_nonzero(frames[i] != frames[i + 1])
                       for i in (0, 2, 4)), (who, "duplicate pouring phases")
        if written:
            path = Path(player.PEOPLE) / folder / (name + ".png")
            with Image.open(path) as im:
                assert im.mode == "P" and im.info["transparency"] == 0, path
                assert np.array_equal(np.array(im), arr), (path, "source mismatch")
                assert im.getpalette()[:48] == [v for c in rgb for v in c], path
            assert path.read_bytes()[24] == 4, (path, "native bit depth")


def comparison(built, before, out):
    cards = []
    for (who, name), arr in built.items():
        folder, rgb, _ = player.CHARS[who]
        with Image.open(before / folder / (name + ".png")) as im:
            old = np.array(im)
        assert old.shape == arr.shape, (who, name, "before dimensions")
        images = [player.rgba(a, rgb) for a in (old, arr)]
        for scale in (1, 4):
            gap, pad, label = 12, 8, 20
            titles = [f"{who} / {name} / {title} / {scale}x"
                      for title in ("BEFORE", "NATIVE AFTER")]
            measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            columns = [max(arr.shape[1] * scale, measure.textbbox((0, 0), title)[2])
                       for title in titles]
            width = sum(columns) + gap + 2 * pad
            card = Image.new("RGBA", (width, 32 * scale + label + 2 * pad),
                             (232, 224, 200, 255))
            draw = ImageDraw.Draw(card)
            x = pad
            for image, title, column in zip(images, titles, columns):
                draw.text((x, pad), title, fill=(40, 32, 24, 255))
                image = image.resize((image.width * scale, image.height * scale),
                                     Image.Resampling.NEAREST)
                card.alpha_composite(image, (x, pad + label))
                x += column + gap
            cards.append(card)
    result = Image.new("RGBA", (max(c.width for c in cards),
                                sum(c.height for c in cards)), (232, 224, 200, 255))
    y = 0
    for card in cards:
        result.alpha_composite(card, (0, y))
        y += card.height
    out.parent.mkdir(parents=True, exist_ok=True)
    result.convert("RGB").save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--before", type=Path)
    ap.add_argument("--comparison", type=Path)
    args = ap.parse_args()
    if bool(args.before) != bool(args.comparison):
        ap.error("--before and --comparison must be supplied together")
    built = build()
    check(built)
    if args.write:
        for (who, name), arr in built.items():
            folder, rgb, _ = player.CHARS[who]
            player.save_sheet(arr, rgb, str(Path(player.PEOPLE) / folder / (name + ".png")))
    if args.check or args.write:
        check(built, written=True)
        print("PASS: four source-exact native player sheets; pouring phases distinct")
    if args.comparison:
        comparison(built, args.before, args.comparison)


if __name__ == "__main__":
    main()
