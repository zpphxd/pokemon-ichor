#!/usr/bin/env python3
"""Render a sample of the Lesser Mysteries from gTileset_TempleDemeter on oikos,
with tools/ichor/render_map.py: the vestibule (teach), the hall of columns
(test) and the Anaktoron behind the draughty doorway (master).

Four images in design/phase2/img/:
  temple_demeter_lit.png     every light lit, the glow rings round them
  temple_demeter_dark.png    the start of the rite in the dark: only the torch's
                             3.5-tile radius round the player and the lit
                             vestibule zone show (SYSTEMS.md §2's flash levels)
  temple_demeter_doused.png  the torch doused: the glow/ palettes, so only the
                             seeds, the chalk and the flames show
  temple_demeter_raid.png    the robbed Telesterion: one lamp lit on the steps

It is a review sample, not the map. Pieces are placed by key and name from
build/temple_demeter/catalog.json (run temple_demeter_build.py first).

Usage: /usr/bin/python3 tools/ichor/art/temple_demeter_scene.py [--out DIR]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/temple_demeter/catalog.json"
OUTDIR = ROOT / "design/phase2/img"
GLOW = ROOT / "data/tilesets/secondary/temple_demeter/porytiles_bin/glow"
W, H = 21, 30
SCALE = 2


class Room:
    def __init__(self):
        cat = json.loads(CAT.read_text())["structures"]
        self.s = {d["key"]: d for d in cat}
        self.m = np.zeros((H, W), np.uint16)

    def id(self, key, name=None):
        d = self.s[key]
        if name is None:
            return d["ids"][0][0]
        cx, cy = d["names"][name]
        return d["ids"][cy][cx]

    def set(self, x, y, key, name=None):
        self.m[y, x] = self.id(key, name)

    def put(self, key, x, y):
        d = self.s[key]
        for j in range(d["h"]):
            for i in range(d["w"]):
                self.m[y + j, x + i] = d["ids"][j][i]

    def light(self, x, y, top, legs, lit):
        """A 1 x 2 light (top over legs) at (x, y); lit adds its glow ring."""
        self.m[y, x] = top + (1 if lit else 0)
        self.m[y + 1, x] = legs + (1 if lit else 0)
        if lit:
            ring = {(-1, 0): "l0", (1, 0): "r0", (-1, 1): "l1", (1, 1): "r1",
                    (-1, 2): "bl", (0, 2): "b", (1, 2): "br"}
            plain = {self.id("floor", n) for n in ("floor", "floor_b", "floor_c")}
            for (dx, dy), n in ring.items():
                if self.m[y + dy, x + dx] in plain:
                    self.set(x + dx, y + dy, "glow", n)


def compose(state):
    """state: 'lit', 'cold' (start of the rite) or 'raid'."""
    r = Room()
    lit = state == "lit"
    F = r.id("floor", "floor")
    Fb, Fc = r.id("floor", "floor_b"), r.id("floor", "floor_c")
    for y in range(H):
        for x in range(W):
            r.m[y, x] = (F, Fb, Fc)[(x * 7 + y * 3) % 5 % 3]
    # walls: top row, frieze, lower wall; side walls down both edges
    for x in range(1, W - 1):
        r.set(x, 0, "wall", "top")
        r.set(x, 2, "wall", "lower")
    r.set(0, 0, "wall", "corner_l")
    r.set(W - 1, 0, "wall", "corner_r")
    for y in range(1, H - 1):
        r.set(0, y, "wall", "side_l")
        r.set(W - 1, y, "wall", "side_r")
    story = ["maiden", "horses", "seized", "search", "hecate", "grief", "hermes", "return"]
    row = ["key"] + sum(([m, "wheat"] for m in story[:4]), []) + ["key"] + \
        sum(([m, "wheat"] for m in story[4:]), [])[:-1] + ["key"]
    for x in range(1, W - 1):
        r.set(x, 1, "frieze", row[(x - 1) % len(row)])
    # the north wall's sconces and the painted door
    for x in (3, 17):
        r.m[2, x] = r.id("wall_lights", "sconce_cold") + (1 if lit else 0)
        if lit:
            r.set(x, 3, "wall_lights", "floor_sconce")
    r.set(5, 1, "wall_lights", "door_top_open" if lit else "door_top_painted")
    r.set(5, 2, "wall_lights", "door_bottom_open" if lit else "door_bottom_painted")
    r.set(14, 2, "wall", "lower_chalk")
    # ---------------------------------------------------- master: the Anaktoron
    r.put("anaktoron", 8, 3)
    r.put("throne", 13, 4)
    r.set(6, 5, "vessels", "kykeon")
    r.set(15, 5, "vessels", "kistai")
    r.set(4, 5, "vessels", "kernos")
    r.set(16, 4, "vessels", "liknon")
    r.set(10, 6, "floor", "floor_inlay")
    r.set(10, 7, "floor", "chalk_trail_v")
    r.set(7, 7, "floor", "chalk_fork")
    r.set(13, 6, "floor", "seed")
    # the partition and its draughty doorway
    for x in range(1, W - 1):
        r.set(x, 8, "partition", "W" if x == 1 else ("E" if x == W - 2 else "M"))
    r.set(10, 8, "partition", "door_draught")
    r.set(9, 8, "partition", "E")
    r.set(11, 8, "partition", "W")
    r.set(10, 9, "floor", "draught")
    # ---------------------------------------------------- test: the hall
    for x in range(1, W - 1):
        if 9 <= x <= 11:
            continue
        side = "L" if x in (1, 12) else ("R" if x in (8, W - 2) else "M")
        for j, tier in enumerate(("top", "mid", "low")):
            r.set(x, 9 + j, "tiers", f"{tier}_{side}")
    cols = [(4, 13), (8, 13), (12, 13), (16, 13), (4, 17), (8, 17), (12, 17), (16, 17)]
    torches = {(8, 13), (12, 17)}
    for (x, y) in cols:
        if (x, y) in torches:
            r.light(x, y, r.id("columns", "torch_cold"), r.id("columns", "bottom"), False)
            if True:     # the two acolytes' column torches are always lit
                r.m[y, x] = r.id("columns", "torch_cold") + 1
                r.set(x, y + 1, "columns", "bottom_lit")
                for (dx, dy), n in {(-1, 0): "l0", (1, 0): "r0", (-1, 1): "l1",
                                    (1, 1): "r1", (-1, 2): "bl", (0, 2): "b", (1, 2): "br"}.items():
                    r.set(x + dx, y + dy, "glow", n)
        else:
            r.set(x, y, "columns", "top")
            r.set(x, y + 1, "columns", "bottom")
    seasons = [("spring", 2, 12), ("summer", 18, 12), ("autumn", 2, 19), ("winter", 18, 19)]
    seed_at = [(3, 15), (17, 15), (3, 18), (17, 21)]
    for (season, x, y), (sx, sy) in zip(seasons, seed_at):
        r.set(sx, sy, "floor", "seed" if season != "winter" else "seeds")
        if state == "raid":
            continue
        r.light(x, y, r.id("braziers", "top_cold"), r.id("braziers", f"{season}_cold"), lit)
    r.set(10, 15, "floor", "chalk_fork")
    r.set(10, 16, "floor", "chalk_trail_v")
    r.set(10, 20, "floor", "chalk_trail_v")
    # the vestibule's wall, open in the middle
    for x in range(1, W - 1):
        if 9 <= x <= 11:
            continue
        r.set(x, 22, "partition", "W" if x in (1, 12) else ("E" if x in (8, W - 2) else "M"))
    # ---------------------------------------------------- teach: the vestibule
    r.light(13, 24, r.id("braziers", "top_cold"), r.id("braziers", "vestibule_cold"), True)
    r.set(9, 26, "floor", "seed")
    r.set(6, 24, "vessels", "kylikes")
    r.put("sentinel", 2, 24)
    r.put("sentinel", 4, 24)
    r.set(3, 25, "stairs", "crypt")
    r.set(3, 24, "floor", "floor")
    # the stair up to the temple, on the bottom row; void beside it
    for x in range(W):
        r.set(x, H - 1, "floor", "void")
    r.set(9, H - 1, "stairs", "up_L")
    r.set(10, H - 1, "stairs", "up_M")
    r.set(11, H - 1, "stairs", "up_R")
    r.set(0, H - 1, "floor", "void")
    if state == "raid":
        for (season, x, y) in seasons:
            r.put("overturned", x - (1 if x > 10 else 0), y + 1)
        for (x, y) in ((10, 12), (9, 18), (11, 21), (7, 10), (13, 6)):
            r.set(x, y, "floor", "bootprints")
        r.set(6, 15, "floor", "rubble")
        r.set(14, 19, "floor", "rubble")
        r.set(15, 5, "vessels", "kiste_smashed")
        r.set(16, 13, "columns", "broken_top")
        r.set(16, 14, "columns", "broken_bottom")
        r.set(15, 15, "columns", "drum")
        r.set(13, 10, "vessels", "lamp_lit")
        r.set(13, 24, "braziers", "top_cold")
        r.set(13, 25, "braziers", "vestibule_cold")
    return r


def render(room, out):
    blk = ROOT / "build/temple_demeter/scene.bin"
    blk.parent.mkdir(parents=True, exist_ok=True)
    room.m.astype("<u2").tofile(blk)
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata",
                    str(blk), "--width", str(W), "--primary", "oikos", "--secondary",
                    "gTileset_TempleDemeter", "--scale", "1", "-o", str(out)], check=True,
                   capture_output=True)
    return Image.open(out).convert("RGB")


def render_doused(room):
    """The same blocks with the glow palettes over slots 6-12, the primary black."""
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    prim = rm.Tileset(rm.resolve_tileset("oikos", syms))
    sec = rm.Tileset(rm.resolve_tileset("gTileset_TempleDemeter", syms))
    sec.pals = [rm.load_pal(GLOW / f"{i:02d}.pal") for i in range(16)]
    prim.pals = [np.zeros((16, 3), np.uint8) for _ in range(16)]
    r = rm.Renderer(prim, sec)
    return rm.render_blocks(r, room.m.ravel(), W)


def darkness(img, holes, zones):
    """Black out all but the torch's circles and the lit zones (in pixels)."""
    a = np.array(img).astype(np.int32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    keep = np.zeros((h, w), bool)
    for (cx, cy, rad) in holes:
        keep |= (xx - cx) ** 2 + (yy - cy) ** 2 <= rad * rad
    for (x0, y0, x1, y1) in zones:
        keep[y0:y1, x0:x1] = True
    a[~keep] = 0
    return Image.fromarray(a.astype(np.uint8))


def big(img):
    return img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUTDIR))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "build/temple_demeter"
    lit = render(compose("lit"), tmp / "lit.png")
    cold_room = compose("cold")
    cold = render(cold_room, tmp / "cold.png")
    raid_room = compose("raid")
    raid = render(raid_room, tmp / "raid.png")
    big(lit).save(out / "temple_demeter_lit.png")
    # the player stands in the vestibule, torch lit: 56 px radius (flash level 3);
    # the vestibule brazier has lit its zone for good
    big(darkness(cold, [(10 * 16 + 8, 21 * 16 + 8, 56)],
                 [(16, 23 * 16, 20 * 16, 29 * 16)])).save(out / "temple_demeter_dark.png")
    big(render_doused(cold_room)).save(out / "temple_demeter_doused.png")
    big(darkness(raid, [(13 * 16 + 8, 10 * 16 + 8, 40), (10 * 16 + 8, 13 * 16 + 8, 56)], []))\
        .save(out / "temple_demeter_raid.png")
    for n in ("lit", "dark", "doused", "raid"):
        print(out / f"temple_demeter_{n}.png")


if __name__ == "__main__":
    main()
