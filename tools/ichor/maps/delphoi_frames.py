#!/usr/bin/env python3
"""Crop Delphoi's arrival frames (15 x 10 metatiles, the GBA screen) out of the
full render, for the arrival's before/after record in design/maps/img/.

  /usr/bin/python3 tools/ichor/maps/delphoi_frames.py <render.png> <tag>

Frames: `step_in`, the screen as you step onto the arrival trigger (39, 39);
`terrace`, where the arrival's camera pan stops (13 left, 31 up of it), the
temple terrace under the Phaedriades; `lookout`, the belvedere at the lane's
west end over the olive sea."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
W, H = 52, 46
FRAMES = {"step_in": (39, 39), "terrace": (26, 8), "lookout": (8, 37)}


def frame(img, cx, cy):
    t = img.width // W
    x0 = min(max(cx - 7, 0), W - 15)
    y0 = min(max(cy - 4, 0), H - 10)
    return img.crop((x0 * t, y0 * t, (x0 + 15) * t, (y0 + 10) * t))


if __name__ == "__main__":
    img = Image.open(sys.argv[1]).convert("RGB")
    tag = sys.argv[2]
    for name, (cx, cy) in FRAMES.items():
        out = ROOT / f"design/maps/img/delphoi_arrival_{name}_{tag}.png"
        frame(img, cx, cy).save(out)
        print(out)
