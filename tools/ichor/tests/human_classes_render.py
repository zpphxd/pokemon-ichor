#!/usr/bin/env python3
"""Verify whole, unobscured native sprites in the test-only mGBA captures."""
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import human_classes as humans


def locate(screen, pixels, mask):
    colors, indices = np.unique(pixels[mask], axis=0, return_index=True)
    positions = [np.argwhere(np.all(screen == color, axis=2)) for color in colors]
    choice = min(range(len(colors)), key=lambda i: len(positions[i]))
    y, x = np.argwhere(mask)[indices[choice]]
    height, width = mask.shape
    bounds = []
    for row, column in positions[choice]:
        left, top = int(column - x), int(row - y)
        if left < 0 or top < 0 or left + width > screen.shape[1] or top + height > screen.shape[0]:
            continue
        crop = screen[top:top + height, left:left + width]
        if np.array_equal(crop[mask], pixels[mask]):
            bounds.append([left, top, left + width, top + height])
    if len(bounds) != 1:
        raise ValueError(f"expected one complete, unobscured rendered sprite; found {len(bounds)}")
    return bounds[0]


def main():
    out = Path(sys.argv[1])
    reference = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None
    expected = set()
    for entry in humans.ASSETS:
        name, kind = entry["name"], entry["kind"]
        if kind == "portraits":
            expected.add((kind, name, "Front", 0))
        else:
            for direction, frames in (("Down", (0, 3, 4)), ("Up", (1, 5, 6)),
                                      ("Left", (2, 7, 8)), ("Right", (2, 7, 8))):
                expected.update((kind, name, direction, frame) for frame in frames)
            if name == "healer":
                expected.add((kind, name, "Bow", 9))
    captures = []
    seen = set()
    for shot in sorted((out / "shots").glob("*_TEST_ONLY_*.png")):
        label = shot.stem.split("_TEST_ONLY_", 1)[1]
        if label.startswith("front_"):
            kind, name, direction, frame, width = "portraits", label[6:], "Front", 0, 64
        else:
            match = re.fullmatch(r"(.+)_(Down|Up|Left|Right|Bow)_(\d+)", label)
            if not match:
                raise ValueError(f"{shot}: unrecognized capture label")
            name, direction, frame = match[1], match[2], int(match[3])
            kind, width = "walkers", 16
        key = (kind, name, direction, frame)
        if key not in expected or key in seen:
            raise ValueError(f"{shot}: unexpected or repeated native state {key}")
        entry = humans.BY_KEY[kind, name]
        source = reference / entry["source"] if reference else humans.ROOT / entry["target"]
        with Image.open(source) as image:
            indices = np.array(image)[:, frame * width:(frame + 1) * width]
        words = np.frombuffer((out / "native" / f"{kind}_{name}.gbapal").read_bytes(), dtype="<u2")
        rgb5 = np.array([(words >> shift) & 31 for shift in (0, 5, 10)]).T
        palette = ((rgb5 << 3) | (rgb5 >> 2)).astype(np.uint8)
        pixels, mask = palette[indices], indices != 0
        if direction == "Right":
            pixels, mask = pixels[:, ::-1], mask[:, ::-1]
        with Image.open(shot) as image:
            screen = np.array(image.convert("RGB"))
        bounds = locate(screen, pixels, mask)
        captures.append({"shot": shot.name, "kind": kind, "name": name, "direction": direction,
                         "frame": frame, "bounds": bounds, "opaque_pixels": int(mask.sum()),
                         "sha256": hashlib.sha256(shot.read_bytes()).hexdigest()})
        seen.add(key)
    if seen != expected:
        raise ValueError(f"missing complete rendered native states: {sorted(expected - seen)}")
    (out / "rendered.json").write_text(json.dumps({
        "kind": "TEST-ONLY stage, background display layers hidden; not story footage",
        "check": "Every opaque native pixel equals the actual mGBA PNG in GBA RGB5-expanded colors.",
        "captures": captures,
    }, indent=2) + "\n")
    print(f"HUMANS RENDER PASS: {len(captures)} complete rendered states, including all199 frames and ten fronts")


if __name__ == "__main__":
    main()
