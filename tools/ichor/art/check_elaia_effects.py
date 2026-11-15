#!/usr/bin/env python3
"""Check source-exact native Elaia effects; optionally render a comparison."""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import field_effects as field
import follower_icons as follower

TARGETS = (
    "tall_grass.png", "jump_tall_grass.png", "long_grass.png",
    "jump_long_grass.png", "sand_footprints.png", "emotion_exclamation.png",
    "emotion_question.png", "emotion_double_exclamation.png", "emote_x.png",
    "emotion_heart.png", "arrow.png", "shadow_small.png", "shadow_medium.png",
    "shadow_large.png", "shadow_extra_large.png",
)
SIZES = {
    "tall_grass.png": (80, 16), "jump_tall_grass.png": (64, 8),
    "long_grass.png": (64, 16), "jump_long_grass.png": (112, 16),
    "sand_footprints.png": (32, 16), "arrow.png": (128, 16),
    "shadow_small.png": (8, 8), "shadow_medium.png": (16, 8),
    "shadow_large.png": (32, 8), "shadow_extra_large.png": (64, 32),
}


def check():
    effects = field.build()
    for name in TARGETS:
        array, palette = effects[name]
        image = Image.open(Path(field.PICS) / name)
        assert image.size == SIZES.get(name, (16, 16)), (name, "engine dimensions")
        assert image.mode == "P" and image.info.get("transparency") == 0, name
        assert (Path(field.PICS) / name).read_bytes()[24] == 4, (name, "4bpp PNG")
        assert np.array_equal(np.array(image), array), (name, "source pixels")
        assert image.getpalette()[:48] == palette.flat(), (name, "source palette")
        assert max(image.getdata()) < 16, name
        assert all(value % 8 == 0 for value in palette.flat()), name
        width = field.SHADOW_SIZES[name[7:-4]][0] if name.startswith("shadow_") else 16
        frames = [array[:, x:x + width].tobytes() for x in range(0, array.shape[1], width)]
        assert len(set(frames)) == len(frames), (name, "duplicate motion frames")
        if name.startswith("shadow_"):
            assert set(image.getdata()) == {0, 9}, (name, "weather shadow role")
    frames = follower.emote_frames()
    image = Image.open(Path(follower.MISC) / "emotes.png")
    assert image.size == (368, 16) and image.mode == "P", "emote frame contract"
    assert image.info.get("transparency") == 0
    assert (Path(follower.MISC) / "emotes.png").read_bytes()[24] == 4, "4bpp emotions"
    assert np.array_equal(np.array(image), np.hstack(frames)), "emotion source pixels"
    assert image.getpalette()[:48] == [v for c in follower.EMOTE_PAL for v in c]
    assert follower.read_jasc(Path(follower.MISC) / "emotes.pal") == follower.EMOTE_PAL
    assert all(v % 8 == 0 for c in follower.EMOTE_PAL for v in c)
    assert all(not np.array_equal(frames[i], frames[i + 1]) for i in range(0, 22, 2))
    assert np.array_equal(frames[22], frames[14]), "spare exclamation contract"
    print("PASS: 16 source-exact native sheets; all motion/emotion pairs distinct; palette roles intact")


def rgba(path):
    image = Image.open(path)
    array = np.array(image)
    result = image.convert("RGBA")
    result.putalpha(Image.fromarray(np.where(array == 0, 0, 255).astype(np.uint8)))
    return result


def compare(before, out):
    out.mkdir(parents=True, exist_ok=True)
    entries = [(name, Path(field.PICS) / name) for name in TARGETS]
    entries.append(("emotes.png", Path(follower.MISC) / "emotes.png"))
    for scale in (1, 4):
        width = 180 + 2 * (368 + 8) * scale
        height = sum((max(16, rgba(path).height) + 8) * scale for _, path in entries) + 28
        sheet = Image.new("RGBA", (width, height), (232, 224, 200, 255))
        draw = ImageDraw.Draw(sheet)
        draw.text((180, 8), "BEFORE", fill="black")
        draw.text((180 + 376 * scale, 8), "AFTER", fill="black")
        y = 28
        for name, path in entries:
            draw.text((4, y + 4), name, fill="black")
            for col, image_path in enumerate((before / name, path)):
                image = rgba(image_path)
                image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
                sheet.alpha_composite(image, (180 + col * 376 * scale, y))
            y += (max(16, rgba(path).height) + 8) * scale
        sheet.convert("RGB").save(out / f"native-before-after-{scale}x.png")


def engine_compare(before, after, out):
    groups = {
        "engine-effects-before-after": [
            ("GAMEPLAY: Route1 grass", "*gameplay_tall_grass_frame2_2.png"),
            ("API: field question", "*engine_field_question_frame1_1.png"),
            ("API: Nebrel happy", "*engine_follower_emotion_happy_frame1_2.png"),
            ("API: Nebrel poisoned", "*engine_follower_emotion_poisoned_frame21_2.png"),
            ("API: north arrow blink", "*engine_warp_direction2_frame4_2.png"),
            ("API: medium shadow", "*engine_shadow_size1.png"),
            ("API: sandal prints", "*engine_sandal_direction0_frame0_1.png"),
            ("API: barley landing", "*engine_jump_tall_frame1_2.png"),
            ("RAM: reed rustle", "*engine_RAM_reed_rustle_frame2_2.png"),
        ],
        "engine-states-before-after": [
            ("STATE: Theo cast", "*engine_theo_fish0_frame10_3.png"),
            ("STATE: Ianthe rod north", "*engine_ianthe_fish1_frame6_3.png"),
            ("STATE: Theo seated surf", "*engine_theo_surf0_frame0_1.png"),
            ("STATE: Ianthe surf hop", "*engine_ianthe_surf22_frame11_1.png"),
            ("STATE: Theo relic", "*engine_theo_relic_frame4_5.png"),
            ("STATE: Ianthe relic", "*engine_ianthe_relic_frame4_5.png"),
        ],
    }
    out.mkdir(parents=True, exist_ok=True)
    for name, entries in groups.items():
        sheet = Image.new("RGB", (924, 32 + len(entries) * 364), (232, 224, 200))
        draw = ImageDraw.Draw(sheet)
        draw.text((156, 8), "POST-POKEMON BASELINE", fill="black")
        draw.text((540, 8), "EFFECT CHECKPOINT", fill="black")
        for row, (label, pattern) in enumerate(entries):
            y = 32 + row * 364
            draw.text((4, y + 8), label, fill="black")
            for col, folder in enumerate((before, after)):
                paths = list(folder.glob(pattern))
                assert len(paths) == 1, (folder, pattern, paths)
                image = Image.open(paths[0]).convert("RGB")
                # Keep the actual terrain and owners around the reviewed sprite.
                image = image.crop((52, 24, 172, 140)).resize((360, 348), Image.Resampling.NEAREST)
                sheet.paste(image, (156 + col * 384, y))
        sheet.save(out / f"{name}.png")


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
        parser.error("comparisons require --output and a before source")
    check()
    if args.before:
        compare(args.before, args.output)
    if args.engine_before:
        engine_compare(args.engine_before, args.engine_after, args.output)


if __name__ == "__main__":
    main()
