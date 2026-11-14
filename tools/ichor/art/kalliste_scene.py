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


TREE = [[0x1D4, 0x1D5], [0x1DC, 0x1DD]]
FLOWERS = 0x004


def tree(sc, x, y):
    for j in range(2):
        for i in range(2):
            sc.g[y + j, x + i] = TREE[j][i]


def slab_field(sc, x, y, w, h, variants=()):
    """Kronion's stylobate: edges, corners and a few worn variants."""
    I = lambda cx, cy: sc.id("stylobate", cx, cy)
    for j in range(h):
        for i in range(w):
            top, bot, lef, rig = j == 0, j == h - 1, i == 0, i == w - 1
            cx = 0 if lef else 2 if rig else 1
            cy = 0 if top else 2 if bot else 1
            sc.g[y + j, x + i] = I(cx, cy)
    for (i, j, v) in variants:
        sc.g[y + j, x + i] = I(3, v)


def quay_field(sc, x, y, w, h):
    for j in range(h):
        for i in range(w):
            sc.g[y + j, x + i] = sc.id("quay", 1, 1)


def compose():
    sc = Scene(46, 36)
    q = lambda cx, cy: sc.id("quay", cx, cy)

    # ---------------- Elaia ----------------
    sc.put("house_small", 1, 1)
    sc.put("house_large", 6, 0)
    sc.put("shrine_dome", 12, 0)
    tree(sc, 18, 0)
    tree(sc, 18, 3)
    pave(sc, 1, 5, 19, 9)
    # Klotheia posts strung across the square's north side
    posts = list(range(3, 18, 2))
    for x in posts:
        top = (3, 0) if x == posts[0] else (2, 0) if x == posts[-1] else (0, 0)
        sc.g[6, x] = sc.id("klotheia_posts", *top)
        sc.g[7, x] = sc.id("klotheia_posts", 0, 1)
        if x != posts[-1]:
            sc.g[6, x + 1] = sc.id("klotheia_posts", 1, 0)
    sc.put("altar_square", 9, 9)
    sc.put("olive_press", 1, 15)
    tree(sc, 5, 15)
    sc.g[17, 7] = FLOWERS
    sc.g[17, 8] = FLOWERS
    # a field wall with a corner, then the terraces below the village
    sc.put("wall_drystone", 10, 15, 2, 1, 1, 1)   # NW corner
    sc.put("wall_drystone", 10, 16, 0, 1, 1, 1)   # north-south run
    sc.put("wall_drystone", 10, 17, 0, 0, 1, 1)   # its foot: west end of the east-west run
    for x in range(11, 19):
        sc.put("wall_drystone", x, 17, 1 + (x % 2), 0, 1, 1)
    sc.put("wall_drystone", 19, 17, 3, 0, 1, 1)
    for x in range(11, 19, 3):
        tree(sc, x, 15) if x + 1 < 19 else None
    sc.put("terrace", 0, 20, 1, 0, 1, 1)
    for x in range(1, 21):
        sc.put("terrace", x, 20, 1 + (x % 2), 1 if 4 <= x <= 7 else 0, 1, 1)
    sc.put("terrace", 9, 20, 3, 0, 1, 1)
    sc.put("terrace", 21, 20, 4, 0, 1, 1)
    for (x, y) in ((1, 22), (5, 23), (9, 22), (13, 24), (17, 22), (3, 27), (11, 28), (16, 27)):
        tree(sc, x, y)
    sc.put("terrace", 0, 26, 1, 0, 1, 1)
    for x in range(1, 21):
        sc.put("terrace", x, 26, 1 + (x % 2), 0, 1, 1)
    sc.put("terrace", 7, 26, 3, 0, 1, 1)
    sc.put("terrace", 21, 26, 4, 0, 1, 1)
    for x in range(0, 21):
        for y in (30, 31):
            sc.g[y, x] = TALL_GRASS if (x * 5 + y) % 3 else GRASS

    # ---------------- Kronion Hill ----------------
    slab_field(sc, 25, 1, 16, 8, variants=((5, 3, 0), (12, 5, 1), (3, 5, 2), (14, 2, 1)))
    for x in (26, 29, 35):
        sc.put("ruin_columns", x, 1, 0, 0, 1, 3)
    sc.put("ruin_columns", 32, 1, 1, 0, 1, 3)       # snapped at mid height
    sc.put("ruin_columns", 38, 3, 2, 2, 1, 1)       # stump
    sc.put("ruin_columns", 39, 6, 3, 2, 1, 1)       # two-drum stump
    sc.put("ruin_drums", 26, 6, 0, 0, 2, 1)
    sc.put("ruin_drums", 28, 7, 2, 0, 1, 1)
    sc.put("ruin_drums", 37, 6, 3, 0, 1, 1)
    sc.put("altar_broken", 32, 3)
    sc.put("dig_site", 32, 5, 0, 0, 2, 2)
    sc.put("dig_site", 34, 5, 2, 0, 1, 1)
    sc.put("dig_site", 34, 6, 2, 1, 1, 1)
    sc.put("dig_site", 31, 5, 3, 0, 1, 1)
    sc.put("dig_site", 30, 6, 3, 1, 1, 1)
    tree(sc, 23, 0)
    tree(sc, 42, 1)
    tree(sc, 43, 5)
    sc.put("terrace", 23, 10, 0, 0, 1, 1)
    for x in range(24, 45):
        sc.put("terrace", x, 10, 1 + (x % 2), 0, 1, 1)
    sc.put("terrace", 32, 10, 3, 0, 1, 1)
    sc.put("terrace", 45, 10, 4, 0, 1, 1)

    # ---------------- Akti ----------------
    sc.put("temple_hestia", 23, 12)
    sc.put("shrine_poseidon", 31, 15)
    tree(sc, 34, 13)
    tree(sc, 41, 12)
    tree(sc, 37, 15)
    pave(sc, 22, 18, 24, 3)           # the temple forecourt and harbor street
    quay_field(sc, 22, 21, 24, 4)
    quay_field(sc, 22, 25, 8, 11)
    # north side of the basin: the quay's south face, with steps cut into it
    for x in range(30, 46):
        sc.g[25, x] = q(1, 2)
    sc.g[25, 29] = q(4, 1)
    sc.g[25, 36] = sc.id("quay_steps", 1, 0)
    # west side of the basin
    for y in range(26, 34):
        sc.g[y, 29] = q(2, 1)
    # breakwater on the south side: north-facing coping, bollards and steps
    for x in range(30, 46):
        sc.g[34, x] = q(1, 0)
        sc.g[35, x] = q(1, 1)
    sc.g[34, 29] = q(4, 0)
    for x in (33, 39, 44):
        sc.g[34, x] = sc.id("quay_steps", 2, 0)
    sc.g[34, 41] = sc.id("quay_steps", 0, 0)
    sc.fill(30, 26, 16, 8, WATER)
    sc.put("boat_kaiki", 31, 26)
    sc.put("boat_kaiki_left", 39, 26)
    sc.put("boat_kaiki", 33, 31)
    # goods on the quay
    sc.put("quay_nets", 33, 22, 0, 0, 3, 1)
    sc.put("quay_nets", 38, 22, 0, 1, 2, 1)
    sc.put("quay_nets", 40, 22, 2, 1, 2, 1)
    sc.put("quay_nets", 24, 27, 0, 1, 3, 1)
    sc.put("quay_nets", 25, 31, 0, 0, 2, 1)
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
