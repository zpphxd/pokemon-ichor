#!/usr/bin/env python3
"""Compose a mock Kalliste scene from aethos ground and kalliste structures,
then render it with tools/ichor/render_map.py --blockdata.

The scene is a review image, not a map: Elaia's houses, shrine and festival
square, Akti's quay, boats and Temple of Hestia, and Kronion Hill's ruins.
It reads metatile ids from build/kalliste/catalog.json (kalliste_build.py).

Usage: /usr/bin/python3 tools/ichor/art/kalliste_scene.py [--scale 2] [-o out.png]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/kalliste/catalog.json"

# aethos ground (General's ids, repainted)
GRASS = 0x001
GRASS_ALT = [0x001, 0x001, 0x001, 0x002, 0x001, 0x001, 0x003]
SAND = 0x121
WATER = 0x170
TALL_GRASS = 0x00D


class Scene:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = np.full((h, w), GRASS, np.uint16)
        self.cat = {s["key"]: s for s in json.loads(CAT.read_text())}

    def fill(self, x, y, w, h, mid):
        self.g[y:y + h, x:x + w] = mid

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place a structure (or a sub-rectangle of it) with its top-left at (x, y)."""
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                if 0 <= x + i < self.w and 0 <= y + j < self.h:
                    self.g[y + j, x + i] = s["ids"][cy + j][cx + i]

    def id(self, key, cx, cy):
        return self.cat[key]["ids"][cy][cx]

    def save(self, path):
        self.g.astype("<u2").tofile(path)


def pave(sc, x, y, w, h, key="paving"):
    """A rectangle of festival paving with its curb."""
    I = lambda cx, cy: sc.id(key, cx, cy)
    for j in range(h):
        for i in range(w):
            top, bot, lef, rig = j == 0, j == h - 1, i == 0, i == w - 1
            if top and lef:
                m = I(0, 0)
            elif top and rig:
                m = I(2, 0)
            elif bot and lef:
                m = I(0, 2)
            elif bot and rig:
                m = I(2, 2)
            elif top:
                m = I(1, 0)
            elif bot:
                m = I(1, 2)
            elif lef:
                m = I(0, 1)
            elif rig:
                m = I(2, 1)
            else:
                m = I(1, 1) if (i * 7 + j * 3) % 5 == 0 else I(3, 0)
            sc.g[y + j, x + i] = m


def compose():
    sc = Scene(40, 30)
    # ---- Elaia (west half) ----
    sc.put("house_small", 1, 1)
    sc.put("house_large", 6, 0)
    sc.put("shrine_dome", 12, 0)
    pave(sc, 1, 6, 17, 9)
    sc.put("altar_square", 8, 9)
    # garland posts along the square's north side
    for i, x in enumerate(range(3, 16, 2)):
        sc.g[7, x] = sc.id("klotheia_posts", 0, 0)
        sc.g[8, x] = sc.id("klotheia_posts", 0, 1)
        if x + 1 < 16:
            sc.g[7, x + 1] = sc.id("klotheia_posts", 1, 0)
    sc.put("olive_press", 1, 16)
    # dry-stone wall run and a terrace
    sc.put("wall_drystone", 5, 18, 0, 0, 1, 1)
    for x in range(6, 11):
        sc.put("wall_drystone", x, 18, 1 + (x % 2), 0, 1, 1)
    sc.put("wall_drystone", 11, 18, 3, 0, 1, 1)
    sc.put("terrace", 5, 22, 0, 0, 1, 1)
    for x in range(6, 12):
        sc.put("terrace", x, 22, 1 + (x % 2), 0, 1, 1)
    sc.put("terrace", 12, 22, 3, 0, 1, 1)
    sc.put("terrace", 13, 22, 4, 0, 1, 1)
    return sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("-o", "--out", default=str(ROOT / "design/phase1/img/kalliste_scene.png"))
    args = ap.parse_args()
    sc = compose()
    bin_path = ROOT / "build/kalliste/scene.bin"
    sc.save(bin_path)
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(bin_path),
                    "--width", str(sc.w), "--primary", "aethos", "--secondary", "kalliste",
                    "--scale", str(args.scale), "-o", args.out], check=True)


if __name__ == "__main__":
    main()
