"""Verify complete OBJ/palette bytes and unobscured real-renderer pixels."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import model_cast as cast
from human_classes_render import locate


def tiles(image):
    a = np.array(image, dtype="uint8")
    height, width = a.shape
    pixels = a.reshape(height // 8, 8, width // 8, 8).transpose(0, 2, 1, 3).reshape(-1)
    return (pixels[::2] | (pixels[1::2] << 4)).tobytes()


def palette(image):
    rgb = np.array(image.getpalette()[:48]).reshape(16, 3)
    return struct.pack("<16H", *(int(r) // 8 | (int(g) // 8) << 5 | (int(b) // 8) << 10
                                for r, g, b in rgb))


def verify(directory, root):
    expected_names = set()
    captures = []
    for path in sorted(cast.OWNED):
        if path == cast.INTRO or path in (cast.FRONT / "sam.png", cast.FRONT / "cami.png"):
            continue
        image = Image.open(root / path)
        kind = "walk" if path.parent == cast.PEOPLE else "back" if path.parent == cast.BACK else "front"
        size = (16, 32) if kind == "walk" else (64, 64)
        count = image.width // size[0] * (image.height // size[1])
        for i in range(count):
            x, y = (i * size[0], 0) if kind == "walk" else (0, i * size[1])
            frame = image.crop((x, y, x + size[0], y + size[1]))
            label = f"{path.stem}_{kind}_frame{i}"
            expected_names.add(label)
            for suffix, expected in ((".4bpp", tiles(frame)), (".gbapal", palette(image))):
                actual = (directory / (label + suffix)).read_bytes()
                if actual != expected:
                    raise AssertionError(f"{label}{suffix}: real engine bytes differ from {path}")
            words = np.frombuffer(palette(image), dtype="<u2")
            rgb5 = np.array([(words >> shift) & 31 for shift in (0, 5, 10)]).T
            colors = ((rgb5 << 3) | (rgb5 >> 2)).astype(np.uint8)
            indices = np.array(frame)
            for mirror in (False, True) if kind == "walk" and i in (2, 7, 8) else (False,):
                shot_label = label + ("_east" if mirror else "")
                shots = list((directory / "shots").glob(f"*_{shot_label}.png"))
                if len(shots) != 1:
                    raise AssertionError(f"{shot_label}: expected exactly one actual-ROM capture")
                shot = shots[0]
                pixels, mask = colors[indices], indices != 0
                if mirror:
                    pixels, mask = pixels[:, ::-1], mask[:, ::-1]
                with Image.open(shot) as screen:
                    try:
                        bounds = locate(np.array(screen.convert("RGB")), pixels, mask)
                    except ValueError as error:
                        raise AssertionError(f"{shot_label}: {error}") from error
                captures.append({"shot": shot.name, "bounds": bounds,
                                 "opaque_pixels": int(mask.sum()),
                                 "sha256": hashlib.sha256(shot.read_bytes()).hexdigest()})
    for suffix in (".4bpp", ".gbapal"):
        actual_names = {p.stem for p in directory.glob("*" + suffix)}
        if actual_names != expected_names:
            raise AssertionError(f"{suffix}: missing/unexpected engine dumps")
    if {entry["shot"] for entry in captures} != {p.name for p in (directory / "shots").glob("*.png")}:
        raise AssertionError("missing/unexpected rendered named-cast states")
    (directory / "rendered.json").write_text(json.dumps({
        "kind": "TEST-ONLY forced real-loader gallery, not story/controller coverage",
        "check": "Every opaque native pixel equals the actual mGBA capture in RGB5-expanded colors.",
        "captures": captures,
    }, indent=2) + "\n")
    print(f"NAMED_CAST BYTES PASS: {len(expected_names)} complete OBJ frames and palettes; "
          "unrouted Sam/Cami busts and intro duplicate are separate source evidence")
    print(f"NAMED_CAST RENDER PASS: {len(captures)} complete, unobscured rendered states")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=Path("build/named_cast"))
    parser.add_argument("--root", type=Path, default=cast.ROOT)
    args = parser.parse_args()
    verify(args.directory, args.root)


if __name__ == "__main__":
    main()
