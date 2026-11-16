"""Source-exact mount/underwater contracts and complete native comparisons."""
import argparse
from pathlib import Path
import re

import numpy as np
from PIL import Image, ImageDraw

import field_effects as field
import player_underwater as water
import sprites_player_ow as player
import surf_poses as riders


def assets():
    result = {"dolphin": (Path(field.PICS) / "surf_blob.png",
                          np.hstack(field.dolphin_frames()), field.MAY.flat())}
    result.update({name: (path, array, [v for c in water.palette() for v in c])
                   for name, (path, array) in water.assets().items()})
    return result


def check():
    for name, (path, array, palette) in assets().items():
        image = Image.open(path)
        assert image.size == ((96, 32) if name == "dolphin" else (128, 32)), name
        assert image.mode == "P" and image.info.get("transparency") == 0, name
        assert path.read_bytes()[24] == 4, (name, "4bpp")
        assert np.array_equal(np.array(image), array), (name, "source pixels")
        assert image.getpalette()[:48] == palette, (name, "hardware palette")
        assert all(v % 8 == 0 for v in palette), name
        frames = [array[:, x:x + 32] for x in range(0, array.shape[1], 32)]
        assert len({frame.tobytes() for frame in frames}) == len(frames), name
        assert all(np.any(frame) and np.any(frame == 0) for frame in frames), name
        if name == "dolphin":
            assert set(array.flat) <= {0, 5, 6, 9, 10, 14, 15}, "shared mount palette roles"
            assert all(np.any(frame == 10) for frame in frames), "saffron flank in every view"
        else:
            # Pose review belongs to the reviewed master, not the old ASCII
            # painter's particular arm/knee coordinates.
            assert len(frames) == 4, "south/north/west plus retained dormant east"
    for folder in ("brendan", "may"):
        actual = np.array(Image.open(Path(player.PEOPLE) / folder / "surfing.png"))
        assert np.array_equal(actual, riders.build(folder)), "reviewed rider source"
    print("PASS: 3 source-exact sheets, 11 distinct frames, reviewed riders and unchanged dolphin")


def display(array, palette):
    image = Image.fromarray(array)
    image.putpalette(palette)
    image = image.convert("RGBA")
    image.putalpha(Image.fromarray(np.where(array == 0, 0, 255).astype(np.uint8)))
    return image


def compare(before, output):
    entries = []
    for name, (_, array, palette) in assets().items():
        old = np.array(Image.open(before / (name + ".png")))
        palettes = [("underwater", palette)]
        if name == "dolphin":
            palettes = [("Theo", [v for c in player.THEO_RGB for v in c]),
                        ("Ianthe", [v for c in player.IANTHE_RGB for v in c])]
        for label, colors in palettes:
            entries.append((name + " / " + label, old, array, colors))
    output.mkdir(parents=True, exist_ok=True)
    for scale in (1, 4):
        sheet = Image.new("RGB", (180 + 2 * 136 * scale, 28 + len(entries) * 40 * scale),
                          (232, 224, 200))
        draw = ImageDraw.Draw(sheet)
        draw.text((180, 6), "BEFORE", fill="black")
        draw.text((180 + 136 * scale, 6), "AFTER", fill="black")
        for row, (label, old, array, palette) in enumerate(entries):
            y = 28 + row * 40 * scale
            draw.text((4, y + 8), label, fill="black")
            for col, pixels in enumerate((old, array)):
                image = display(pixels, palette)
                image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
                sheet.paste(image, (180 + col * 136 * scale, y), image)
        sheet.save(output / f"water-native-before-after-{scale}x.png")


def engine_compare(before, after, output):
    before_paths = {path.name: path for path in before.glob("*.png")}
    after_paths = {path.name: path for path in after.glob("*.png")}
    assert before_paths.keys() == after_paths.keys(), "matched capture filenames"
    assert len(before_paths) == 320, "complete 64-state capture set"
    pattern = re.compile(r"engine_(mount|underwater)_(theo|ianthe)_anim(\d+)_image(\d+)_bob(-?\d+)")
    groups = {}
    for filename in sorted(before_paths):
        match = pattern.search(filename)
        assert match is not None, filename
        mode, who, anim, image, bob = match.groups()
        groups.setdefault((mode, who), {}).setdefault(int(anim), []).append(
            (filename, f"i{image}\ny2={bob}"))
    assert set(groups) == {(mode, who) for mode in ("mount", "underwater")
                          for who in ("theo", "ianthe")}, "both characters and state groups"
    for (mode, _), animations in groups.items():
        expected = set(range(8)) | set(range(20, 24)) if mode == "mount" else set(range(20))
        assert set(animations) == expected, "complete requested state animations"
    output.mkdir(parents=True, exist_ok=True)
    for (mode, who), animations in groups.items():
        columns = max(map(len, animations.values()))
        for scale in (1, 4):
            row_height = 96 * scale
            column_width = 56 * scale
            half = columns * column_width + 12
            sheet = Image.new("RGB", (100 + 2 * half, 32 + len(animations) * row_height),
                              (232, 224, 200))
            draw = ImageDraw.Draw(sheet)
            draw.text((100, 6), "BASELINE: FIXTURE", fill="black")
            draw.text((100 + half, 6), "AFTER: FIXTURE", fill="black")
            for row, (anim, entries) in enumerate(sorted(animations.items())):
                y = 32 + row * row_height
                draw.text((4, y + 8), f"{who} {mode}\nanim {anim}", fill="black")
                for column, (filename, label) in enumerate(entries):
                    for side, paths in enumerate((before_paths, after_paths)):
                        x = 100 + side * half + column * column_width
                        image = Image.open(paths[filename]).convert("RGB")
                        image = image.crop((64, 48, 112, 112))
                        image = image.resize((48 * scale, 64 * scale), Image.Resampling.NEAREST)
                        sheet.paste(image, (x, y))
                        draw.text((x, y + 64 * scale), label, fill="black")
            sheet.save(output / f"water-engine-{mode}-{who}-{scale}x.png")
    print(f"PASS: matched complete engine comparisons, {len(before_paths)} captures per ROM")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--engine-before", type=Path)
    parser.add_argument("--engine-after", type=Path)
    args = parser.parse_args()
    if bool(args.engine_before) != bool(args.engine_after):
        parser.error("--engine-before and --engine-after must be supplied together")
    if bool(args.before or args.engine_before) != bool(args.output):
        parser.error("comparisons require a before source and --output")
    check()
    if args.before:
        compare(args.before, args.output)
    if args.engine_before:
        engine_compare(args.engine_before, args.engine_after, args.output)


if __name__ == "__main__":
    main()
