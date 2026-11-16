"""Verify every opaque player trainer pixel in the forced real-loader gallery."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
from human_classes_render import locate
import player_sources as sources


BACK_ORDERS = ((3,), (0, 1, 2, 0, 3), (3, 0, 2, 2, 3))


def verify(directory, root):
    captures = []
    for who in ("theo", "ianthe"):
        for state in ("battle_front", "battle_back"):
            path, _ = sources.asset(who, state)
            with Image.open(root / path) as image:
                colors = np.array(image.getpalette()[:48]).reshape((16, 3)) >> 3
                colors = ((colors << 3) | (colors >> 2)).astype(np.uint8)
                cases = [(f"{who}_front", 0)] if state == "battle_front" else [
                    (f"{who}_back_anim{anim}_phase{phase + 1}", frame)
                    for anim, order in enumerate(BACK_ORDERS)
                    for phase, frame in enumerate(order)
                ]
                for label, frame in cases:
                    shots = list((directory / "shots").glob(f"*_{label}.png"))
                    if len(shots) != 1:
                        raise ValueError(f"{label}: expected exactly one real-ROM capture")
                    shot = shots[0]
                    indices = np.array(image.crop((0, frame * 64, 64, (frame + 1) * 64)))
                    mask = indices != 0
                    with Image.open(shot) as screen:
                        bounds = locate(np.array(screen.convert("RGB")), colors[indices], mask)
                    captures.append({
                        "shot": shot.name, "source": path, "frame": frame, "bounds": bounds,
                        "opaque_pixels": int(mask.sum()),
                        "sha256": hashlib.sha256(shot.read_bytes()).hexdigest(),
                    })
    if len(captures) != 24 or {case["shot"] for case in captures} != {
            shot.name for shot in (directory / "shots").glob("*.png")}:
        raise ValueError("Incomplete or unexpected rendered player battle states")
    (directory / "rendered.json").write_text(json.dumps({
        "kind": "TEST_ONLY forced real-loader/table gallery, not natural battle/controller coverage",
        "check": "Every opaque native pixel equals its RGB5-expanded mGBA display pixel.",
        "captures": captures,
    }, indent=2) + "\n")
    print("PLAYER_BATTLE_RENDER PASS: 24 complete, unobscured real-loader states")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("build/player_battle"))
    parser.add_argument("--root", type=Path, default=sources.ROOT)
    args = parser.parse_args()
    verify(args.directory, args.root)


if __name__ == "__main__":
    main()
