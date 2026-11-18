#!/usr/bin/env python3
"""The reference sheet for Oros's snow and ice: Emerald's own Shoal Cave ice rooms
(rendered from the layouts cut in aae327b35e, read back out of git) beside
Ichor's new snow and ice, at 1x and 3x (design/maps/img/oros_vs_shoal.png).

Usage: /usr/bin/python3 tools/ichor/art/oros_compare.py
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map as R  # noqa: E402

CUT = "aae327b35e^"
ROOMS = [("ShoalCave_LowTideIceRoom", 31), ("ShoalCave_LowTideLowerRoom", 20)]


def shoal(name, w):
    raw = subprocess.run(["git", "show", f"{CUT}:data/layouts/{name}/map.bin"], cwd=ROOT,
                         capture_output=True, check=True).stdout
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    r = R.Renderer(R.Tileset(R.tileset_from_dir(ROOT / "data/tilesets/primary/general")),
                   R.Tileset(R.tileset_from_dir(ROOT / "data/tilesets/secondary/cave")))
    return R.render_blocks(r, np.frombuffer(raw, "<u2"), w).convert("RGB")


def crop(path, box):
    im = Image.open(path).convert("RGB")
    im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)   # the review renders are 2x
    return im.crop(box)


def main():
    a = shoal(*ROOMS[0])
    b = shoal(*ROOMS[1])
    snow = crop(ROOT / "build/oros_r/Ascent_Snowfield.png", (96, 256, 96 + 240, 256 + 160))
    lake = crop(ROOT / "build/oros_r/Ascent_Glacier.png", (176, 528, 176 + 240, 528 + 160))
    pieces = [("Emerald: Shoal Cave ice room, west", a.crop((0, 0, 240, 160))),
              ("Emerald: Shoal Cave ice room, east", a.crop((256, 0, 496, 160))),
              ("Ichor: the Leuke snowfield", snow), ("Ichor: the Glacier's frozen lake", lake)]
    W = 4 * 248 + 8
    H = 24 + 168 + 24 + 3 * 160 + 16
    sheet = Image.new("RGB", (max(W, 2 * 3 * 240 + 24), H + 24 + 3 * 160), (24, 24, 30))
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(pieces):
        x = 8 + i * 248
        d.text((x, 6), label + " (1x)", fill=(230, 220, 180))
        sheet.paste(im, (x, 22))
    y = 22 + 168
    for i, (label, im) in enumerate(pieces):
        x = 8 + (i % 2) * (3 * 240 + 8)
        yy = y + 18 + (i // 2) * (3 * 160 + 24)
        d.text((x, yy - 14), label + " (3x)", fill=(230, 220, 180))
        sheet.paste(im.resize((720, 480), Image.NEAREST), (x, yy))
    out = ROOT / "design/maps/img/oros_vs_shoal.png"
    sheet = sheet.crop((0, 0, sheet.width, y + 18 + 2 * (3 * 160 + 24)))
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
