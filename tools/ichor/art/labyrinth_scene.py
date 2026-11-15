#!/usr/bin/env python3
"""Mock scenes of Daedalus's workshop, for judging the look (LABYRINTH.md §8).

The room is the hub at the end of Ring III, 24 x 18 (LABYRINTH.md §4), staged two
ways:

  workshop       scene D: lit and quiet. Rows of bronze automata, the half-polished
                 collar on the bench, the Icarus Shaft grated shut on its grey light,
                 the music box on its tripod. The player has just come in by the back
                 door. (There is no Daedalus overworld sprite yet, so he is left out.)
  workshop_dawn  scene L: the next morning. The lamps have burned out, the collar is
                 gone from the bench, the grate stands open and grey dawn light falls
                 down the shaft. Rendered with the dawn palette set (porytiles_bin/
                 dawn/), which the map loads over palettes 6-12 for this scene.

These are block data composed from build/labyrinth/catalog.json by structure key
and part name, not the map: world-act3 builds Knossa's maps from the tileset.

  --fast      composite straight from the drawn structures (no compile needed)
  (default)   write the blockdata and render it with tools/ichor/render_map.py on
              the compiled tileset and oikos, exactly as the game draws it

Writes design/phase4/img/labyrinth_scene_<name>.png (3x); with --pass N it also
keeps a copy as labyrinth_scene_<name>_passN.png.

Usage: /usr/bin/python3 tools/ichor/art/labyrinth_scene.py [--fast] [--pass N] [--only NAME]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import labyrinth_art as A  # noqa: E402

ROOT = A.K.ROOT
IMG = ROOT / "design/phase4/img"
BUILD = ROOT / "build/labyrinth_scenes"
TILESET = ROOT / "data/tilesets/secondary/labyrinth"
W, H = 24, 18

CAT = {}


class Room:
    """A grid of cells, each (key, cx, cy) into the catalog."""

    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.g = [[("floor", 1, 0) for _ in range(w)] for _ in range(h)]
        self.sprites = []

    def cell(self, key, x, y, name=None, cx=0, cy=0):
        if name is not None:
            cx, cy = CAT[key]["names"][name]
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = (key, cx, cy)

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        s = CAT[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.cell(key, x + i, y + j, cx=cx + i, cy=cy + j)

    def _src(self, key, x, y, cx, cy):
        """The catalog cell to use for cell (cx, cy) of `key` placed so that this
        cell lands on map (x, y): the odd twin's where the parity is odd and the
        twin covers that row."""
        odd = (x - cx + y - cy) % 2 == 1
        twin = CAT.get(key + "_odd")
        if odd and twin:
            r0 = (twin.get("twin_of") or [key, 0])[1]
            if r0 <= cy < r0 + twin["h"]:
                return key + "_odd", cx, cy - r0
        return key, cx, cy

    def floor_piece(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """A piece standing on the slab floor, drawn on the right floor parity."""
        s = CAT[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                k, ccx, ccy = self._src(key, x + i, y + j, cx + i, cy + j)
                self.cell(k, x + i, y + j, cx=ccx, cy=ccy)

    def floor_cell(self, key, x, y, name):
        """One named cell of a floor piece, on the right floor parity."""
        cx, cy = CAT[key]["names"][name]
        k, ccx, ccy = self._src(key, x, y, cx, cy)
        self.cell(k, x, y, cx=ccx, cy=ccy)

    def blockdata(self):
        return np.array([CAT[k]["ids"][cy][cx] for row in self.g for (k, cx, cy) in row], "<u2")

    def render_fast(self, structs):
        img = np.zeros((self.h * 16, self.w * 16, 3), np.uint8)
        comp = {}
        for y, row in enumerate(self.g):
            for x, (k, cx, cy) in enumerate(row):
                if k not in comp:
                    comp[k] = composite(structs[k])
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = \
                    comp[k][cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        return Image.fromarray(img)


def composite(s):
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        m = a[..., 3] > 0
        out[m] = a[..., :3][m]
    return out


# --------------------------------------------------------------------------
# The workshop
# --------------------------------------------------------------------------

def half(x, y):
    """The running bond: a slab's left half where x + y is even."""
    return "l" if (x + y) % 2 == 0 else "r"


def workshop(state="lit"):
    dawn = state == "dawn"
    r = Room()
    t = r.cell
    # the floor
    for y in range(3, H - 1):
        for x in range(1, W - 1):
            t("floor", x, y, "slab_" + half(x, y))
    for x in range(1, W - 1):
        t("floor", x, 3, "shade_" + half(x, 3))
    t("floor", 6, 14, "labrys")       # (6 + 14) even: a left half
    t("floor", 13, 14, "crack")
    t("floor", 15, 13, "crack")
    t("floor", 12, 10, "oil")
    # the bottom edge and the threshold down to Ring III
    for x in range(W):
        t("floor", x, H - 1, "void")
    t("edge", 11, H - 1, "sill_l")
    t("edge", 12, H - 1, "sill_r")
    # side walls
    for y in range(0, 3):
        t("arcade", 0, y, cx=5, cy=y)
        t("arcade", W - 1, y, cx=6, cy=y)
    for y in range(3, H - 1):
        t("edge", 0, y, "wall_w")
        t("edge", W - 1, y, "wall_e")
    # the arcade: piers at 1, 5, 9, 14, 18, 22; bays 2-4, 6-8, 10-13, 15-17, 19-21
    for x in (9, 14, 22):
        r.put("arcade", x, 0, cx=0, cy=0, w=1)
    for x in (5, 18):
        if dawn:
            r.put("pier_cold", x, 0)
        else:
            r.put("arcade", x, 0, cx=7, cy=0, w=1)
    r.put("arcade", 1, 0, cx=4, cy=0, w=1)            # the back door
    r.put("bay_wings", 2, 0)
    r.put("bay_shelves", 6, 0)
    r.put("shaft", 10, 0, cx=4 if dawn else 0, w=4)    # with its sill on row 3
    r.put("bay_plan", 15, 0)
    r.put("lift", 19, 0)
    if dawn:
        r.floor_piece("light_spill", 10, 4)
    # the lamp-bearers flanking the shaft
    lamp = "auto_lamp_cold" if dawn else "auto_lamp"
    r.floor_piece(lamp, 9, 4)
    r.floor_piece(lamp, 14, 4)
    # rows of bronze automata, west: Number One to Eighteen, three still with
    # empty plinths (Three and Seven are out in the maze; Nine walked off)
    rows = (("auto_kore", "auto_kouros", "plinth_three", "auto_hound", "auto_kouros",
             "auto_kore"),
            ("plinth_seven", "auto_kore", "plinth_nine", "auto_kouros", "auto_open",
             "auto_kore"),
            ("auto_kouros", "auto_kore", "auto_kouros", "auto_open", "auto_kore",
             "auto_kouros"))
    for y, row in zip((5, 9, 13), rows):
        for x, k in enumerate(row, 2):
            r.floor_piece(k, x, y)
    # Daedalus's bench under the shaft, the collar on it (gone at dawn)
    r.floor_piece("bench", 10, 8)
    if dawn:
        r.cell("bench_parts", 11, 8, "cloth_l")
        r.cell("bench_parts", 12, 8, "cloth_r")
    r.floor_piece("music_box", 15, 8)
    # a runner from the threshold to the bench
    r.put("runner", 11, 10, cy=0, h=1)
    for y in range(11, H - 2):
        r.put("runner", 11, y, cy=1, h=1)
    r.put("runner", 11, H - 2, cy=2, h=1)
    # the drafting tables before the plan; the bed and the Pithos on the east wall
    r.floor_piece("drafting", 15, 4)
    r.floor_piece("kline", 21, 6)
    r.floor_piece("pithos", 21, 10)
    # the tool bench
    r.floor_cell("bench", 15, 12, "tools")
    for x, n in ((16, "vise"), (17, "top")):
        r.floor_cell("bench_parts", x, 12, n)
    r.floor_cell("bench", 18, 12, "top_r")
    for x, n in ((15, "front_l"), (16, "front"), (17, "front"), (18, "front_r")):
        r.floor_cell("bench_parts", x, 13, n)
    if not dawn:
        r.sprites.append((*PLAYER, FACING["west"], True, 9, 8))
    else:
        r.sprites.append((*PLAYER, FACING["north"], False, 11, 6))
    return r


SCENES = {"workshop": lambda: workshop("lit"), "workshop_dawn": lambda: workshop("dawn")}


# --------------------------------------------------------------------------
# Sprites and rendering
# --------------------------------------------------------------------------

def load_sprite(path, pal, frame):
    im = Image.open(path)
    a = np.array(im, np.uint8)
    vals = [int(v) for v in Path(pal).read_text().split()[3:3 + 48]]
    cols = np.array(vals, np.uint8).reshape(16, 3)
    f = a[:, frame * 16:frame * 16 + 16] % 16
    rgba = np.zeros(f.shape + (4,), np.uint8)
    rgba[..., :3] = cols[f]
    rgba[..., 3] = np.where(f == 0, 0, 255)
    return rgba


PLAYER = (ROOT / "graphics/object_events/pics/people/brendan/walking.png",
          ROOT / "graphics/object_events/palettes/brendan.pal")
FACING = {"south": 0, "north": 1, "west": 2}


def draw_sprites(img, sprites):
    a = np.array(img)
    for (path, pal, frame, flip, x, y) in sprites:
        s = load_sprite(path, pal, frame)
        if flip:
            s = s[:, ::-1]
        px, py = x * 16, y * 16 - 16
        h, w = s.shape[:2]
        reg = a[py:py + h, px:px + w]
        m = s[..., 3] > 0
        reg[m] = s[..., :3][m]
    return Image.fromarray(a)


def render(room, palettes=None):
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    prim = rm.Tileset(rm.resolve_tileset("oikos", syms))
    sec = rm.Tileset(rm.resolve_tileset(str(TILESET.relative_to(ROOT)), syms))
    if palettes:
        sec.pals = [rm.load_pal(TILESET / "porytiles_bin" / palettes / f"{i:02d}.pal")
                    if 6 <= i <= 12 else sec.pals[i] for i in range(16)]
    r = rm.Renderer(prim, sec)
    return rm.render_blocks(r, room.blockdata(), room.w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pass", dest="pass_no", type=int)
    ap.add_argument("--only")
    ap.add_argument("--scale", type=int, default=3)
    args = ap.parse_args()
    IMG.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    structs = {}
    if args.fast:
        sections = A.build()
        A.pack(sections)
        for _, ss in sections:
            for s in ss:
                structs[s.key] = s
                CAT[s.key] = {"key": s.key, "w": s.w, "h": s.h, "ids": s.ids, "walk": s.walk,
                              "names": {n: list(v) for n, v in s.names.items()},
                              "twin_of": list(getattr(s, "twin_of", None) or []) or None}
    else:
        cat = ROOT / "build/labyrinth/catalog.json"
        meta = TILESET / "porytiles_bin/metatiles.bin"
        if not meta.exists() or meta.stat().st_mtime < cat.stat().st_mtime:
            sys.exit("labyrinth_scene: the compiled tileset is older than the catalog; "
                     "run labyrinth_build.py (and let it finish) first")
        for s in json.loads(cat.read_text()):
            CAT[s["key"]] = s
    for name, fn in SCENES.items():
        if args.only and name != args.only:
            continue
        room = fn()
        if args.fast:
            img = room.render_fast(structs)
            if name.endswith("dawn"):
                img = fake_dawn(img)
        else:
            img = render(room, palettes="dawn" if name.endswith("dawn") else None)
        img = draw_sprites(img, room.sprites)
        img = img.resize((img.width * args.scale, img.height * args.scale), Image.NEAREST)
        dst = (BUILD if args.fast else IMG) / f"labyrinth_scene_{name}.png"
        img.save(dst)
        print(dst)
        if args.pass_no is not None and not args.fast:
            p = IMG / f"labyrinth_scene_{name}_pass{args.pass_no}.png"
            img.save(p)
            print(p)


def fake_dawn(img):
    """--fast only: apply the dawn transform to every color but the dawn light."""
    a = np.array(img)
    keep = {A.C[n] for n in A.DAWN_KEEP}
    out = a.copy()
    flat = a.reshape(-1, 3)
    o = out.reshape(-1, 3)
    cache = {}
    for i, c in enumerate(map(tuple, flat)):
        if c in keep:
            continue
        if c not in cache:
            cache[c] = A.dawn_color(c)
        o[i] = cache[c]
    return Image.fromarray(out)


if __name__ == "__main__":
    main()
