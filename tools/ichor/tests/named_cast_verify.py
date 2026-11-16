"""Compare real engine OBJ/palette dumps with the indexed production PNGs."""
import argparse
from pathlib import Path
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import model_cast as cast


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
    for suffix in (".4bpp", ".gbapal"):
        actual_names = {p.stem for p in directory.glob("*" + suffix)}
        if actual_names != expected_names:
            raise AssertionError(f"{suffix}: missing/unexpected engine dumps")
    print(f"NAMED_CAST BYTES PASS: {len(expected_names)} complete OBJ frames and palettes; "
          "unrouted Sam/Cami busts and intro duplicate are separate source evidence")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=Path("build/named_cast"))
    parser.add_argument("--root", type=Path, default=cast.ROOT)
    args = parser.parse_args()
    verify(args.directory, args.root)


if __name__ == "__main__":
    main()
