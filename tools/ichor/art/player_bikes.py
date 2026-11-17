"""Source adapters for the player's riding sheets; the Acro Bike stays unavailable.

For the Acro Bike's rider-only redraws, the original contact planes and
VEHICLE_EXTRAS remain exact, including transparent pixels. The Mach Bike's sheet
is now the chariot (walker_paint.py draws it: a pony and a two-wheeled car), so
it keeps only the atlas, palette and ground-anchor checks; no bicycle is retained.
"""
import argparse
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import sprites_player_ow as player
import player_sources

BASE = Path(__file__).parent / "base/player_bikes"
FOLDERS = {"theo": "brendan", "ianthe": "may"}
# (facing, bicycle plane, pedal phase, torso lean)
NORMAL = [
    ("down", 23, 0, 0), ("up", 23, 0, 0), ("left", 25, 0, 0),
    ("down", 23, 1, 0), ("down", 23, 2, 0),
    ("up", 23, 1, 0), ("up", 23, 2, 0),
    ("left", 25, 1, 0), ("left", 25, 2, 0),
]
ACRO = NORMAL + [
    ("down", 23, 0, -1), ("down", 18, 0, -1),
    ("down", 24, 0, 1), ("down", 24, 1, 1),
    ("up", 23, 0, -1), ("up", 20, 0, -1),
    ("up", 25, 0, 1), ("up", 25, 1, 1),
    ("left", 25, 0, -1), ("left", 21, 0, -1),
    ("left", 25, 0, -2), ("left", 25, 1, -3),
    ("down", 18, 1, -1), ("down", 18, 2, -1),
    ("up", 20, 1, -1), ("up", 20, 2, -1),
    ("left", 21, 1, -1), ("left", 21, 2, -1),
]
# Raised wheel/handlebar rectangles above the contact plane. Coordinates are
# native source pixels; the rider never replaces these existing vehicle parts.
VEHICLE_EXTRAS = {
    2: [(8, 20, 10, 23)],
    7: [(8, 20, 10, 23)],
    8: [(8, 20, 10, 23)],
    11: [(15, 12, 17, 13)],
    12: [(15, 10, 17, 13)],
    17: [(8, 20, 10, 23)],
    19: [(18, 23, 32, 25)],
    20: [(20, 21, 32, 25)],
}
BODY = {
    "down": """
...kcCywwkCDk...
..kcCCwwwwCDDk..
.kSdkCwwwwDkSdk.
.kSSkbbbbbbkSSk.
..kkkwWWWwkkk...
...kSdWWWSdk....
...kSdkkkSdk....
...kbbk.kbbk....
""",
    "up": """
...kcCCCCCCDk...
..kcCCCDCCCDDk..
.kSdkCCDCDDkSdk.
.kSSkDDDDDDkSSk.
..kkktWWWwkkk...
...kSdWWWSdk....
...kSdkkkSdk....
...kbbk.kbbk....
""",
    "left": """
....kcCCCDk.....
...kwwkCCCDDk...
..kSSkwwkCCDDk..
.kSdkkbbktTkDk..
.kbkkwWWWkDDk...
....kSSWWkkk....
....kSddkSdk....
....kbbk.kbbk...
""",
}


def path(who, bike):
    return Path(player.PEOPLE) / FOLDERS[who] / (bike + ".png")


def palette(who):
    return player.CHARS[who][1]


def vehicle(who, bike):
    image = np.array(Image.open(BASE / f"{who}_{bike}.png"))
    specs = NORMAL if bike == "mach_bike" else ACRO
    result = []
    for i, (_, plane, _, _) in enumerate(specs):
        original = image[:, i * 32:(i + 1) * 32]
        frame = original.copy()
        frame[:plane] = 0
        for x0, y0, x1, y1 in VEHICLE_EXTRAS.get(i, []):
            frame[y0:y1, x0:x1] = original[y0:y1, x0:x1]
        result.append(frame)
    return result


def legacy_frames(who, bike):
    specs = NORMAL if bike == "mach_bike" else ACRO
    result = []
    roles = player.CHARS[who][2]
    for retained, (facing, plane, phase, lean) in zip(vehicle(who, bike), specs):
        body = [list(row) for row in player.parse(BODY[facing])]
        # Alternate bent knees/ankles while the bicycle frame remains fixed.
        if phase:
            x = 4 if phase == 1 else 9
            body[5][x:x + 3] = list("SSk")
            body[6][x:x + 3] = list("bbk")
            body[7][x:x + 3] = list("...")
        body = ["".join(row) for row in body]
        hat_y = max(0, plane - 19)
        face_y = hat_y + 6
        body_y = hat_y + 11
        head_x = 8 + (lean if facing == "left" else 0)
        head = player.HAT_SIDE if facing == "left" else player.HAT_FRONT
        rows = player.compose([
            (body, 8, body_y),
            (player.parse(head), head_x, hat_y),
            (player.parse(player.FACES[who][facing]), head_x, face_y),
        ], w=32, h=32)
        rider = np.array([[0 if ch == "." else roles[ch] for ch in row] for row in rows],
                         dtype=np.uint8)
        # Retained vehicle pixels are foreground at the documented contact plane.
        rider[plane:] = retained[plane:]
        exposed = (rider == 0) & (retained != 0)
        rider[exposed] = retained[exposed]
        result.append(rider)
    return result


def frames(who, bike):
    count = 9 if bike == "mach_bike" else 27
    return [frame.copy() for frame in np.hsplit(
        np.array(player_sources.source_image(who, bike)), count)]


def check():
    for who in FOLDERS:
        for bike, count in (("mach_bike", 9), ("acro_bike", 27)):
            expected = np.hstack(frames(who, bike))
            image = Image.open(path(who, bike))
            assert image.size == (count * 32, 32), (who, bike, "atlas")
            assert image.mode == "P" and image.info.get("transparency") == 0
            assert path(who, bike).read_bytes()[24] == 4
            assert np.array_equal(np.array(image), expected), "native source"
            assert image.getpalette()[:48] == [v for c in palette(who) for v in c]
            assert all(v % 8 == 0 for c in palette(who) for v in c)
            palfile = Path(player.PALDIR) / (FOLDERS[who] + ".pal")
            hardware = [[int(v) // 8 * 8 for v in line.split()]
                        for line in palfile.read_text().splitlines()[3:]]
            assert hardware == [list(c) for c in palette(who)], "existing hardware palette identity"
            _, contract = player_sources.asset(who, bike)
            original = np.array(Image.open(BASE / f"{who}_{bike}.png"))
            specs = NORMAL if bike == "mach_bike" else ACRO
            for index, (frame, bounds, (_, plane, _, _)) in enumerate(zip(
                    frames(who, bike), contract["prior_source_frame_bounds"], specs)):
                assert np.nonzero(frame)[0].max() + 1 == bounds[3], "original ground anchor"
                assert np.any(frame == 0)
                if bike == "mach_bike":
                    continue  # the chariot replaces the bicycle: no vehicle plane to keep
                retained = original[:, index * 32:(index + 1) * 32]
                assert np.array_equal(frame[plane:], retained[plane:]), (
                    who, bike, index, "retained vehicle contact plane")
                for x0, y0, x1, y1 in VEHICLE_EXTRAS.get(index, []):
                    assert np.array_equal(frame[y0:y1, x0:x1], retained[y0:y1, x0:x1]), (
                        who, bike, index, "retained VEHICLE_EXTRAS", (x0, y0, x1, y1))
    print("PASS: four source-exact indexed atlases, 72 frames; Acro vehicle planes/extras exact")


def rgba(array, colors):
    image = Image.fromarray(array)
    image.putpalette([v for c in colors for v in c])
    image = image.convert("RGBA")
    image.putalpha(Image.fromarray(np.where(array == 0, 0, 255).astype(np.uint8)))
    return image


def compare(output):
    output.mkdir(parents=True, exist_ok=True)
    for who in FOLDERS:
        for bike in ("mach_bike", "acro_bike"):
            original = np.array(Image.open(BASE / f"{who}_{bike}.png"))
            current = frames(who, bike)
            for scale in (1, 4):
                width = 80 + 8 * 40 * scale
                height = 28 + ((len(current) + 7) // 8) * 88 * scale
                sheet = Image.new("RGB", (width, height), (232, 224, 200))
                draw = ImageDraw.Draw(sheet)
                draw.text((4, 4), f"{who} {bike}: original above / native below", fill="black")
                for i, frame in enumerate(current):
                    x, y = 80 + (i % 8) * 40 * scale, 28 + (i // 8) * 88 * scale
                    draw.text((x, y), str(i), fill="black")
                    for row, pixels in enumerate((original[:, i * 32:(i + 1) * 32], frame)):
                        image = rgba(pixels, palette(who))
                        image = image.resize((32 * scale, 32 * scale), Image.Resampling.NEAREST)
                        sheet.paste(image, (x, y + 12 + row * 36 * scale), image)
                sheet.save(output / f"{who}-{bike}-{scale}x.png")


def engine_compare(before, after, output):
    """Pair every verified phase, using OAM bounds reported by the actual ROM."""
    groups = {}
    old = sorted((before / "shots").glob("*.png"))
    new = sorted((after / "shots").glob("*.png"))
    assert len(old) == len(new) == 736
    assert [p.name for p in old] == [p.name for p in new], "matched phase filenames"
    pattern = r"NOTE capture (\S+) (\d+) (\d+)"
    positions = dict((label, (int(x), int(y)))
                     for label, x, y in re.findall(pattern, (after / "run.log").read_text()))
    original_positions = dict((label, (int(x), int(y)))
                              for label, x, y in re.findall(pattern, (before / "run.log").read_text()))
    assert positions == original_positions and len(positions) == 736, "matching OAM anchors"
    for baseline, current in zip(old, new):
        label = current.stem.split("_boot_", 1)[1]
        case = label.split("_phase", 1)[0]
        x, y = positions[label]
        images = [Image.open(p).convert("RGB") for p in (baseline, current)]
        assert images[0].size == images[1].size == (240, 160)
        pixels = [np.array(image) for image in images]
        differences = np.any(pixels[0] != pixels[1], axis=2)
        assert np.any(differences[y:y + 32, x:x + 32]), label
        differences[y:y + 32, x:x + 32] = False
        assert not np.any(differences), (label, "change outside forced bike sprite")
        crops = [image.crop((x, y, x + 32, y + 32)) for image in images]
        groups.setdefault(case, []).append((label.split("_phase", 1)[1], crops))
    assert len(groups) == 240
    output.mkdir(parents=True, exist_ok=True)
    for case, phases in groups.items():
        for scale in (1, 4):
            sheet = Image.new("RGB", (max(240, len(phases) * 52 * scale), 40 + 72 * scale),
                              (232, 224, 200))
            draw = ImageDraw.Draw(sheet)
            draw.text((4, 4), f"{case}: forced ROM before / after", fill="black")
            for index, (phase, images) in enumerate(phases):
                x = index * 52 * scale
                draw.text((x, 20), phase, fill="black")
                for row, image in enumerate(images):
                    sheet.paste(image.resize((32 * scale, 32 * scale), Image.Resampling.NEAREST),
                                (x, 36 + row * 36 * scale))
            sheet.save(output / f"{case}-{scale}x.png")
    print("PASS: 736 matched actual-ROM phases, 240 cases, identical anchors/backgrounds")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--engine-before", type=Path)
    parser.add_argument("--engine-after", type=Path)
    args = parser.parse_args()
    if args.write:
        for who in FOLDERS:
            for bike in ("mach_bike", "acro_bike"):
                player.save_sheet(np.hstack(frames(who, bike)), palette(who), path(who, bike))
    if args.check:
        check()
    if args.preview:
        compare(args.preview)
    if args.engine_before or args.engine_after:
        if not (args.engine_before and args.engine_after and args.preview):
            parser.error("engine comparison needs --engine-before, --engine-after and --preview")
        engine_compare(args.engine_before, args.engine_after, args.preview / "engine")


if __name__ == "__main__":
    main()
