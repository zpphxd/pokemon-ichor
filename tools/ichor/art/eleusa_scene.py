#!/usr/bin/env python3
"""Compose a mock scene of Eleusa from gTileset_Eleusa + aethos and render it
with tools/ichor/render_map.py: the village on the Sacred Way, wheat and
stubble fields, a farm compound, the threshing floor, and the sanctuary of the
Mysteries behind the Greater Propylaea.

This is a review scene, not a map: it shows how the kit's pieces fit
together. Pieces are placed by key and name from build/eleusa/catalog.json
(run eleusa_build.py first), and the fields' soft edges come from
eleusa_lib.blob_key, exactly as a map builder would use them.

Usage: /usr/bin/python3 tools/ichor/art/eleusa_scene.py [-o design/phase2/img/eleusa_scene.png]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eleusa_lib as E  # noqa: E402

ROOT = E.ROOT
CAT = ROOT / "build/eleusa/catalog.json"
OUT = ROOT / "design/phase2/img/eleusa_scene.png"

W, H = 50, 40

# aethos metatiles
GRASS, PATH, SEA = 0x001, 0x1D9, 0x170
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
CYP_TOP, CYP_BOT = 0x00E, 0x016
PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
         "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}


class Scene:
    def __init__(self):
        cat = json.loads(CAT.read_text())
        self.s = {d["key"]: d for d in cat["structures"]}
        self.fronts = cat["fronts"]
        self.m = np.full((H, W), GRASS, np.uint16)

    def put(self, key, x, y, cells=None):
        d = self.s[key]
        for j in range(d["h"]):
            for i in range(d["w"]):
                if cells is not None and (i, j) not in cells:
                    continue
                if 0 <= y + j < H and 0 <= x + i < W:
                    self.m[y + j, x + i] = d["ids"][j][i]

    def piece(self, key, name, x, y):
        d = self.s[key]
        cx, cy = d["names"][name]
        self.m[y, x] = d["ids"][cy][cx]

    def front(self, key, x, y):
        f = self.fronts[key]
        for j, row in enumerate(f["ids"]):
            for i, mid in enumerate(row):
                if mid is not None:
                    self.m[y + j, x + i] = mid

    def rect(self, x0, y0, x1, y1, mid):
        self.m[y0:y1 + 1, x0:x1 + 1] = mid

    def path_patch(self, x0, y0, x1, y1):
        """An aethos limestone patch with its own edges."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                v = "T" if y == y0 else ("B" if y == y1 else "")
                h = "L" if x == x0 else ("R" if x == x1 else "")
                self.m[y, x] = PATCH[(v + h) or "C"]

    def field(self, rows, ox, oy, key="wheat", inner=None):
        """A soft-edged field from a character mask ('#' in the field)."""
        region = [[c == "#" for c in r] for r in rows]
        d = self.s[key]
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != "#":
                    continue
                k = E.blob_key(region, i, j)
                cx, cy = d["names"][k]
                self.m[oy + j, ox + i] = d["ids"][cy][cx]
                if inner and k == "1|11111111" and (i * 7 + j * 3) % inner[1] == 0:
                    self.piece(*inner[0], ox + i, oy + j)

    def olive(self, x, y):
        self.m[y - 1, x], self.m[y - 1, x + 1] = OLIVE_TIP
        self.m[y, x], self.m[y, x + 1] = OLIVE_TOP
        self.m[y + 1, x], self.m[y + 1, x + 1] = OLIVE_BOT

    def cypress(self, x, y):
        self.m[y, x] = CYP_TOP
        self.m[y + 1, x] = CYP_BOT

    def way(self, x, y0, y1, ends=True):
        """The Sacred Way running north-south, three cells wide."""
        for y in range(y0, y1 + 1):
            row = ("NW", "N", "NE") if (ends and y == y0) else \
                  (("SW", "S", "SE") if (ends and y == y1) else ("W", "C", "E"))
            for i, n in enumerate(row):
                self.piece("sacred_way", n, x + i, y)

    def pave(self, x0, y0, x1, y1, ruts_x=None):
        """A patch of the Sacred Way's slabs, kerbed all round."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                n = ("N" if y == y0 else ("S" if y == y1 else "")) + \
                    ("W" if x == x0 else ("E" if x == x1 else ""))
                self.piece("sacred_way", n or "C", x, y)

    def pool(self, x, y, w, h):
        for j in range(h):
            for i in range(w):
                n = ("N" if j == 0 else ("S" if j == h - 1 else "")) + \
                    ("W" if i == 0 else ("E" if i == w - 1 else ""))
                if n:
                    self.piece("rheitoi", n, x + i, y + j)
                else:
                    self.m[y + j, x + i] = SEA


def compose():
    s = Scene()
    # ------------------------------------------------------------ the sanctuary
    # the precinct's court, paved with the Sacred Way's slabs
    s.pave(9, 6, 43, 16)
    s.put("telesterion", 20, 0)
    s.put("plutonion", 13, 3)
    s.put("seat_stone", 17, 5)
    s.put("temple_demeter", 33, 0)
    s.put("grain_shrine", 31, 4)
    s.put("pomegranate", 10, 3)
    s.put("pomegranate", 41, 3)
    for x, y in ((18, 8), (30, 8), (18, 12), (30, 12)):
        s.piece("torch_post_path", "top_lit", x, y)
        s.piece("torch_post_path", "foot", x, y + 1)
    s.put("grain_shrine_path", 12, 11)
    s.put("grain_shrine_path", 39, 11)
    s.put("sheaf_path", 13, 12)
    s.put("sheaf_path", 38, 12)
    s.put("pithos_path", 36, 7)
    s.put("pithos_path", 37, 7)
    # the precinct wall and its gate, the Greater Propylaea
    for x in range(8, 45):
        if not 21 <= x <= 27:
            s.m[17, x] = 0x149
    s.m[17, 8], s.m[17, 44] = 0x148, 0x14A
    s.put("propylaea", 21, 12)
    # the Kallichoron, just outside the gate, where Demeter sat grieving
    s.put("kallichoron", 16, 19)
    s.put("seat_stone", 19, 20)
    # ------------------------------------------------------------ the road
    s.way(23, 18, 39, ends=False)
    for y in (21, 26, 31, 36):
        for x in (21, 27):
            s.piece("torch_post", "top_lit" if y < 31 else "top_cold", x, y)
            s.piece("torch_post", "foot", x, y + 1)
    # the Rheitoi beside the road
    s.pool(33, 33, 6, 4)
    s.cypress(32, 32)
    s.cypress(39, 32)
    # ------------------------------------------------------------ the village
    # west: a farm compound (the longhouse in its walled yard), the Asclepeion
    s.front("longhouse", 8, 20)
    s.rect(8, 24, 12, 25, PATH)
    for y in (23, 24, 25):
        s.piece("court_wall", "NS", 7, y)
        s.piece("court_wall", "NS", 13, y)
    s.piece("court_wall", "NE", 7, 26)
    s.piece("court_wall", "NW", 13, 26)
    for x in range(8, 13):
        s.piece("court_wall", "gate" if x == 10 else "EW", x, 26)
    s.put("pithos_sunk", 11, 24)
    s.put("asclepeion", 16, 24)
    s.rect(4, 28, 22, 28, PATH)
    s.rect(10, 27, 10, 28, PATH)
    s.front("cottage", 3, 29)
    s.front("gable_house", 11, 30)
    s.rect(4, 33, 4, 33, PATH)
    s.rect(12, 34, 12, 34, PATH)
    # east: the Agora on the road, the porch house, the tower farm, the granary
    s.put("agora", 28, 20)
    s.rect(26, 24, 46, 24, PATH)
    s.front("porch_house", 35, 20)
    s.front("tower_farm", 41, 18)
    s.front("thatch_cottage", 29, 26)
    s.rect(31, 30, 31, 31, PATH)
    s.rect(26, 31, 31, 31, PATH)
    s.front("granary", 43, 26)
    s.rect(44, 30, 45, 31, PATH)
    s.put("pithos", 42, 28)
    s.put("pithos", 47, 28)
    s.put("oven", 39, 27)
    # the threshing floor and the winnowing
    s.put("alonia", 42, 33)
    s.put("alonia_work", 43, 34)
    s.put("winnowing", 46, 37)
    s.put("sheaf_grass", 41, 37)
    # ------------------------------------------------------------ the fields
    s.field(["..####..",
             ".#######",
             "########",
             "#######.",
             "######..",
             ".#####..",
             "..###..."], 0, 6)
    s.put("wheat_poppies", 3, 8)
    s.put("wheat_poppies", 2, 10)
    s.put("wheat_poppies", 5, 9)
    s.field([".####",
             "#####",
             "#####",
             "####.",
             "###..",
             "##..."], 45, 6)
    s.put("wheat_poppies", 47, 8)
    s.field(["######",
             "######",
             "#####.",
             ".###.."], 0, 35, key="stubble")
    s.put("stook", 2, 36)
    s.put("stook", 4, 37)
    s.put("reaper", 1, 37)
    s.field([".###..",
             "####..",
             "###...",
             "##...."], 0, 18)
    s.field(["..####",
             ".#####",
             "######",
             "######"], 14, 36)
    s.put("wheat_poppies", 17, 38)
    s.field(["#####",
             "#####",
             "####."], 28, 37 - 0)
    s.field(["##", "##", "##"], 47, 32)
    for x, y in ((3, 23), (5, 22), (1, 24), (6, 24)):
        s.piece("poppies", "scattered", x, y)
    s.piece("poppies", "dense", 4, 24)
    s.piece("poppies", "dense", 5, 23)
    s.piece("poppies", "dense", 2, 23)
    for x, y in ((14, 18), (20, 22), (8, 18)):
        s.piece("poppies", "scattered", x, y)
    # ------------------------------------------------------------ trees
    for x, y in ((1, 1), (5, 0), (45, 0), (8, 33), (19, 33), (40, 38)):
        s.olive(x, y)
    for x, y in ((7, 2), (47, 2), (1, 27), (48, 18), (6, 30), (15, 30), (40, 30)):
        s.cypress(x, y)
    return s


def render(s, out, scale=2):
    blk = ROOT / "build/eleusa/scene.bin"
    blk.parent.mkdir(parents=True, exist_ok=True)
    s.m.astype("<u2").tofile(blk)
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(blk),
                    "--width", str(W), "--primary", "aethos", "--secondary", "gTileset_Eleusa",
                    "--scale", str(scale), "-o", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(OUT))
    ap.add_argument("--scale", type=int, default=2)
    args = ap.parse_args()
    render(compose(), Path(args.out), args.scale)


if __name__ == "__main__":
    main()
