#!/usr/bin/env python3
"""Repaint aethos from General's sources (tools/ichor/art/base/aethos).

Every General color is mapped to a shade from the PLAN.md master palette, so
each metatile keeps its position and meaning. The same map is applied to the
animation key frames and frames, so Porytiles still finds the animated tiles.
Then run: porytiles compile-tileset gTileset_Aethos

Usage: /usr/bin/python3 tools/ichor/art/paint_aethos.py
"""
from pathlib import Path
import shutil
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "tools/ichor/art/base/aethos"
OUT = ROOT / "data/tilesets/primary/aethos/porytiles_src"

# General color -> Ichor color. Grouped by material. Distinct inputs stay
# distinct so animation key frames remain unique.
MAP = {
    # grass: sun-bleached sage
    (115, 197, 164): (200, 200, 128), (164, 213, 197): (208, 208, 144),
    (65, 180, 131): (144, 160, 72), (24, 164, 106): (120, 136, 64),
    # trees: olive canopy, silver highlights, cypress-dark shade
    (180, 255, 131): (192, 200, 160), (131, 197, 98): (136, 160, 88),
    (57, 139, 49): (72, 104, 40), (57, 82, 0): (24, 56, 40),
    # trunks and earth: gray-brown
    (222, 148, 115): (176, 144, 96), (106, 90, 90): (104, 88, 72),
    (164, 98, 90): (136, 112, 88), (65, 57, 49): (56, 48, 40),
    (255, 197, 148): (232, 216, 176),
    # flowers and roofs: terracotta
    (222, 106, 98): (224, 136, 88), (205, 65, 82): (184, 88, 48),
    (255, 189, 131): (240, 192, 64), (238, 148, 115): (200, 144, 40),
    # walls, metal, glass: marble
    (255, 255, 255): (248, 248, 240), (222, 230, 238): (232, 232, 216),
    (189, 205, 230): (216, 208, 192), (156, 180, 222): (192, 184, 168),
    (131, 131, 139): (168, 160, 152), (98, 98, 123): (128, 120, 112),
    (65, 74, 106): (88, 80, 80), (41, 49, 90): (32, 24, 24),
    (213, 213, 213): (224, 216, 200), (189, 189, 189): (200, 192, 176),
    (164, 164, 164): (176, 168, 160),
    # rocks and cliffs: pale limestone with warm shade
    (238, 213, 205): (240, 232, 208), (222, 180, 164): (216, 200, 160),
    (189, 148, 139): (192, 168, 120), (156, 115, 115): (160, 128, 88),
    (131, 90, 90): (128, 96, 64), (98, 65, 82): (96, 72, 48),
    (65, 49, 65): (64, 48, 40),
    # sand and paths: limestone
    (238, 230, 164): (248, 240, 216), (222, 205, 131): (240, 232, 200),
    (213, 180, 106): (200, 176, 120), (205, 156, 82): (176, 144, 96),
    # water: Aegean
    (115, 189, 246): (112, 168, 224), (98, 172, 238): (96, 152, 216),
    (98, 164, 222): (88, 144, 208), (82, 139, 197): (72, 128, 192),
    (74, 115, 172): (40, 80, 152), (172, 197, 230): (176, 216, 240),
    (139, 164, 222): (136, 192, 232), (106, 131, 213): (80, 136, 200),
    (82, 106, 213): (48, 104, 176), (65, 90, 189): (40, 88, 160),
    (57, 82, 156): (32, 72, 136), (41, 65, 139): (24, 56, 120),
    (156, 164, 189): (152, 200, 232),
}


def repaint(src, dst):
    im = np.array(Image.open(src).convert("RGBA"))
    out = im.copy()
    rgb = im[..., :3]
    for a, b in MAP.items():
        out[(rgb == a).all(-1), :3] = b
    Image.fromarray(out).save(dst)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(BASE, OUT)
    for png in OUT.rglob("*.png"):
        repaint(png, png)
    print("painted", OUT)


if __name__ == "__main__":
    main()
