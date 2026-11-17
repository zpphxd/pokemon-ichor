#!/usr/bin/env python3
"""Mock scenes of the Labyrinth, for judging the look (LABYRINTH.md §6-§8).

These are block data composed from build/<tileset>/catalog.json by structure key
and part name, not maps: world-act3 builds Knossa's maps from the tilesets.

  labyrinth
    workshop       scene D: Daedalus's workshop, lit and quiet (24 x 18)
    workshop_dawn  scene L: the next morning, with the dawn palette set
    ring           a dark ring corridor (one 15 x 10 screen): the thread laid from
                   a bronze anchor ring, a brazier lit in its alcove, a stair down,
                   a cracked wall, webs; with the torch's radius and the lit
                   zone (ring_dark), and doused (ring_doused, the glow set)
  mychos
    forge          Ring VI's forge (scene G): the furnace, Hyperion's anvil
    choros         Ring VII: the mirrors' beam and the dancing floor, lit
    starry         the Starry Chamber (scene J): the lustral basin, the star-clock

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
import labyrinth_kit as KIT  # noqa: E402

ROOT = A.K.ROOT
IMG = ROOT / "design/phase4/img"
BUILD = ROOT / "build/labyrinth_scenes"
W, H = 24, 18

CATS = {}          # tileset -> {key: catalog entry}
STRUCTS = {}       # tileset -> {key: Struct} (--fast)


class Room:
    """A grid of cells, each (key, cx, cy) into a tileset's catalog."""

    def __init__(self, w=W, h=H, tileset="labyrinth", fill=("floor", 1, 0)):
        self.w, self.h = w, h
        self.tileset = tileset
        self.cat = CATS[tileset]
        self.g = [[fill for _ in range(w)] for _ in range(h)]
        self.sprites = []

    def cell(self, key, x, y, name=None, cx=0, cy=0):
        if name is not None:
            cx, cy = self.cat[key]["names"][name]
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = (key, cx, cy)

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        s = self.cat[key]
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
        twin = self.cat.get(key + "_odd")
        if odd and twin:
            r0 = (twin.get("twin_of") or [key, 0])[1]
            if r0 <= cy < r0 + twin["h"]:
                return key + "_odd", cx, cy - r0
        return key, cx, cy

    def floor_piece(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """A piece standing on the slab floor, drawn on the right floor parity."""
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                k, ccx, ccy = self._src(key, x + i, y + j, cx + i, cy + j)
                self.cell(k, x + i, y + j, cx=ccx, cy=ccy)

    def floor_cell(self, key, x, y, name):
        """One named cell of a floor piece, on the right floor parity."""
        cx, cy = self.cat[key]["names"][name]
        k, ccx, ccy = self._src(key, x, y, cx, cy)
        self.cell(k, x, y, cx=ccx, cy=ccy)

    # --- the rings ---------------------------------------------------------

    def dark(self, x, y):
        self.cell("thread", x, y, "dark_" + half(x, y))

    def walls(self, rows, floor="dark"):
        """Lay a wall/floor grid ('#' wall, anything else floor) with the kit."""
        grid = [[ch == "#" for ch in row] for row in rows]
        for y, row in enumerate(grid):
            for x, wall in enumerate(row):
                if wall:
                    self.cell("walls", x, y, KIT.classify(grid, x, y))
                elif floor == "dark":
                    self.dark(x, y)
                elif floor == "marble":
                    self.cell("marble", x, y, "marble")
        return grid

    def thread(self, path, kind="dark", from_anchor=False):
        """Lay Ariadne's thread along a path of cells (each next to the last),
        with the shapes the engine would draw. from_anchor: the path starts on a
        bronze ring, which the engine never draws thread over."""
        for i, (x, y) in enumerate(path):
            if from_anchor and i == 0:
                continue
            conn = set()
            for j in (i - 1, i + 1):
                if 0 <= j < len(path):
                    nx, ny = path[j]
                    conn.add({(0, -1): "n", (0, 1): "s", (-1, 0): "w", (1, 0): "e"}[(nx - x, ny - y)])
            shape = {frozenset("we"): "h", frozenset("ns"): "v", frozenset("ne"): "ne",
                     frozenset("nw"): "nw", frozenset("se"): "se", frozenset("sw"): "sw",
                     frozenset("n"): "cap_n", frozenset("s"): "cap_s", frozenset("w"): "cap_w",
                     frozenset("e"): "cap_e"}.get(frozenset(conn))
            if kind == "marble":
                self.cell("marble", x, y, f"marble_{shape}")
            else:
                key = "thread" if kind == "dark" else "pools"
                self.cell(key, x, y, f"{kind}_{half(x, y)}_{shape}")

    def blockdata(self):
        return np.array([self.cat[k]["ids"][cy][cx] for row in self.g for (k, cx, cy) in row], "<u2")

    def render_fast(self):
        structs = STRUCTS[self.tileset]
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


def half(x, y):
    """The running bond: a slab's left half where x + y is even."""
    return "l" if (x + y) % 2 == 0 else "r"


# --------------------------------------------------------------------------
# The workshop (labyrinth)
# --------------------------------------------------------------------------

def workshop(state="lit"):
    dawn = state == "dawn"
    r = Room()
    t = r.cell
    for y in range(3, H - 1):
        for x in range(1, W - 1):
            t("floor", x, y, "slab_" + half(x, y))
    for x in range(1, W - 1):
        t("floor", x, 3, "shade_" + half(x, 3))
    t("floor", 6, 14, "labrys")
    t("floor", 13, 14, "crack")
    t("floor", 15, 13, "crack")
    t("floor", 12, 10, "oil")
    for x in range(W):
        t("floor", x, H - 1, "void")
    t("edge", 11, H - 1, "sill_l")
    t("edge", 12, H - 1, "sill_r")
    for y in range(0, 3):
        t("arcade", 0, y, cx=5, cy=y)
        t("arcade", W - 1, y, cx=6, cy=y)
    for y in range(3, H - 1):
        t("edge", 0, y, "wall_w")
        t("edge", W - 1, y, "wall_e")
    for x in (9, 14, 22):
        r.put("arcade", x, 0, cx=0, cy=0, w=1)
    for x in (5, 18):
        if dawn:
            r.put("pier_cold", x, 0)
        else:
            r.put("arcade", x, 0, cx=7, cy=0, w=1)
    r.put("arcade", 1, 0, cx=4, cy=0, w=1)
    r.put("bay_wings", 2, 0)
    r.put("bay_shelves", 6, 0)
    r.put("shaft", 10, 0, cx=4 if dawn else 0, w=4)
    r.put("bay_plan", 15, 0)
    r.put("lift", 19, 0)
    if dawn:
        r.floor_piece("light_spill", 10, 4)
    lamp = "auto_lamp_cold" if dawn else "auto_lamp"
    r.floor_piece(lamp, 9, 4)
    r.floor_piece(lamp, 14, 4)
    rows = (("auto_kore", "auto_kouros", "plinth_three", "auto_hound", "auto_kouros",
             "auto_kore"),
            ("plinth_seven", "auto_kore", "plinth_nine", "auto_kouros", "auto_open",
             "auto_kore"),
            ("auto_kouros", "auto_kore", "auto_kouros", "auto_open", "auto_kore",
             "auto_kouros"))
    for y, row in zip((5, 9, 13), rows):
        for x, k in enumerate(row, 2):
            r.floor_piece(k, x, y)
    r.floor_piece("bench", 10, 8)
    if dawn:
        r.cell("bench_parts", 11, 8, "cloth_l")
        r.cell("bench_parts", 12, 8, "cloth_r")
    r.floor_piece("music_box", 15, 8)
    r.put("runner", 11, 10, cy=0, h=1)
    for y in range(11, H - 2):
        r.put("runner", 11, y, cy=1, h=1)
    r.put("runner", 11, H - 2, cy=2, h=1)
    r.floor_piece("drafting", 15, 4)
    r.floor_piece("kline", 21, 6)
    r.floor_piece("pithos", 21, 10)
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


# --------------------------------------------------------------------------
# A ring corridor (labyrinth): one screen
# --------------------------------------------------------------------------

RING = ["###############",
        "###############",
        "#.......####..#",
        "#.......####..#",
        "####.#####.....",
        "####.#####.....",
        "####...........",
        "####.######.###",
        "####.######.###",
        "####.#####...##"]


def ring(state="lit"):
    r = Room(15, 10, "labyrinth")
    r.walls(RING)
    # the brazier, lit, in the alcove at the west end of the north hall
    r.floor_piece("brazier", 1, 2, cx=2, w=2)
    # the stair down, in the north hall's wall
    r.cell("stairs", 5, 1, "down_l")
    r.cell("stairs", 6, 1, "down_r")
    # a cracked face, Asterion's way into the alcove beyond
    r.cell("cracked", 12, 1, "face")
    # webs where the east passage meets the hall
    r.cell("webs", 13, 1, "face_r")
    # glow-marks along the south passage's walls (by torchlight, the stone)
    r.cell("glow", 5, 8, "top_w")
    r.cell("glow", 3, 7, "top_e")
    # the anchor ring at the junction, and the thread laid from it: west along
    # the hall, down the passage, east along the corridor to the player
    r.floor_piece("anchor", 7, 3)
    path = [(7, 3), (6, 3), (5, 3), (4, 3), (4, 4), (4, 5), (4, 6), (5, 6), (6, 6), (7, 6),
            (8, 6), (9, 6), (10, 6), (11, 6)]
    r.thread(path, from_anchor=True)
    r.sprites.append((*PLAYER, FACING["east"], True, 11, 6))
    return r


HUNT = ["###############",
        "###############",
        "###############",
        "...............",
        "...............",
        "###.#####.###.#",
        "###############",
        "###############",
        "###############",
        "###############"]


def hunt(state="day"):
    """Ring V: the loop's north corridor, a skylight pool across it, niches to
    duck into, a cracked wall (Minos's tomb behind it), the fresco niche."""
    r = Room(15, 10, "labyrinth")
    grid = r.walls(HUNT)
    kind = "sun" if state == "day" else "moon"
    for y in (3, 4):
        for x in (6, 7, 8):
            r.cell("pools", x, y, f"{kind}_{half(x, y)}")
    # niches off the corridor's south side: their floor is ring floor, the
    # autotiled face behind them swapped for a niche back
    for x in (3, 9, 13):
        r.dark(x, 5)
        r.cell("niche", x, 6, "shrine" if x == 9 else "back")
    # walls fix-ups: the cells either side of each niche are faces with open
    # ends, which the autotile gives once the niche is floor
    g2 = [list(row) for row in HUNT]
    for x in (3, 9, 13):
        g2[5][x] = "."
    grid = [[ch == "#" for ch in row] for row in g2]
    for y in range(10):
        for x in range(15):
            if grid[y][x] and (x, y) not in ((3, 6), (9, 6), (13, 6)):
                r.cell("walls", x, y, KIT.classify(grid, x, y))
    # the fresco niche in the north wall: a bay of the arcade with steps 4-6
    for y in range(3):
        r.put("arcade", 0, y, cx=0, cy=y, w=1)
        r.put("arcade", 4, y, cx=0, cy=y, w=1)
    r.put("fresco_v", 1, 0)
    # %1, the cracked wall, at the corridor's east end... seen as a face here
    r.cell("cracked", 11, 2, "face")
    # the thread along the corridor, through the pool
    path = [(x, 4) for x in range(0, 12)]
    r.thread(path)
    for (x, y) in path:
        if 6 <= x <= 8:
            r.cell("pools", x, y, f"{kind}_{half(x, y)}_" + ("h" if x < 11 else "cap_w"))
    r.sprites.append((*PLAYER, FACING["east"], True, 11, 4))
    return r


def tomb():
    """Minos's tomb (scene F): low, painted pillars, dust, the bier and the cap."""
    r = Room(15, 10, "labyrinth")
    rows = ["###############",
            "###############",
            "##...........##",
            "##...........##",
            "##...........##",
            "##...........##",
            "##...........##",
            "##...........##",
            "##...........##",
            "######...######"]
    r.walls(rows)
    # the inscription over the bier, in the north face
    for i, n in enumerate("lmr"):
        r.cell("tomb_inscription", 6 + i, 1, n)
    r.floor_piece("tomb_bier", 6, 2, w=3)
    for x in (3, 11):
        r.floor_piece("tomb_pillar", x, 3)
        r.floor_piece("tomb_pillar", x, 6)
    r.floor_cell("tomb_goods", 5, 2, "labrys_top")
    r.floor_cell("tomb_goods", 5, 3, "labrys_base")
    r.floor_cell("tomb_goods", 9, 2, "labrys_top")
    r.floor_cell("tomb_goods", 9, 3, "labrys_base")
    r.floor_cell("tomb_goods", 2, 2, "jar")
    r.floor_cell("tomb_goods", 12, 2, "jar")
    for (x, y, n) in ((2, 3, "drift"), (12, 3, "drift"), (4, 5, "dust"), (9, 7, "dust"),
                      (7, 6, "prints"), (7, 8, "prints"), (2, 8, "dust"), (12, 6, "dust")):
        r.floor_cell("tomb_goods", x, y, n)
    # the breach the player came in by, Ring V's cracked wall broken
    r.dark(6, 9)
    r.dark(7, 9)
    r.dark(8, 9)
    r.sprites.append((*PLAYER, FACING["north"], False, 7, 7))
    return r


def shaft():
    """The top of the Icarus Shaft (scene L): ten wide, the light growing."""
    r = Room(10, 10, "labyrinth")
    rows = ["sky", "lip", "band4", "band4", "fade4", "band3", "band3", "fade3", "band2",
            "fade2"]
    for y, row in enumerate(rows):
        r.cell("icarus", 0, y, f"{row}_w")
        for x in range(1, 9):
            name = f"{row}_m"
            if row == "sky" and x in (3, 7):
                name = "sky_e"
            r.cell("icarus", x, y, name)
        r.cell("icarus", 9, y, f"{row}_e")
    return r


# --------------------------------------------------------------------------
# Mychos: Ring VI's forge, Ring VII's Choros, the Starry Chamber
# --------------------------------------------------------------------------

def arcade_wall(r, x0, x1, bays):
    """An arcade north wall (rows 0-2) from column x0 to x1: side walls at the
    ends, piers between bays; bays: [(key or None for a plain bay)]."""
    for y in range(3):
        r.cell("arcade", x0, y, cx=5, cy=y)
        r.cell("arcade", x1, y, cx=6, cy=y)
    x = x0 + 1
    for b in bays:
        r.put("arcade", x, 0, cx=0, w=1)
        if b is None:
            r.put("arcade", x + 1, 0, cx=1, w=3)
        else:
            r.put(b, x + 1, 0)
        x += 4
    r.put("arcade", x, 0, cx=0, w=1)


FORGE = ["###############",
          "###############",
          "###############",
          "#.............#",
          "#.............#",
          "#.............#",
          "#.............#",
          "#.............#",
          "#.............#",
          "#.............#"]


def forge_scene():
    r = Room(15, 10, "mychos")
    r.walls(FORGE)
    # the furnace in the north wall, sickle banners either side
    r.put("forge", 6, 0)
    for x in (2, 4, 10, 12):
        r.cell("banners", x, 2, "face")
    # Hyperion's anvil before the furnace, the bellows blowing into its flank
    r.floor_piece("anvil", 6, 4)
    r.floor_piece("forge_kit", 9, 3, cx=0, w=2)
    r.floor_piece("forge_kit", 4, 3, cx=2, w=1)        # the quench tub
    # a runnel of molten bronze from the furnace's foot to a mold
    r.floor_cell("forge_kit", 5, 3, "runnel_v")
    r.floor_cell("forge_kit", 5, 4, "runnel_v")
    r.floor_cell("forge_kit", 5, 5, "mold")
    r.floor_piece("forge_kit", 12, 6, cx=5, w=1)       # slag
    r.floor_piece("lamp_stand", 1, 3)
    r.floor_piece("lamp_stand", 13, 3)
    r.cell("grates", 10, 7, "floor")
    r.floor_piece("vault", 12, 8, cx=2, w=1)           # copper ingots, stacked
    r.sprites.append((*PLAYER, FACING["north"], False, 7, 8))
    return r


DANCE_GRID = ["SXWRL", "LRLWR", "RWSXL", "RWLWW", "WXWLX"]


def choros_scene():
    r = Room(15, 10, "mychos")
    for y in range(10):
        for x in range(15):
            r.cell("marble", x, y, "marble")
    for y in range(3, 10):
        r.cell("edge", 0, y, "wall_w")
        r.cell("edge", 14, y, "wall_e")
    arcade_wall(r, 0, 14, ["fresco_iv", "fresco_v", "fresco_vi"])
    # the dancing floor, revealed, the first four steps danced (E5, E4, E3, E2)
    lit = {(4, 4), (4, 3), (4, 2), (4, 1)}
    for j, row in enumerate(DANCE_GRID):
        for i, sym in enumerate(row):
            name = sym.lower() + ("_lit" if (i, j) in lit else "")
            r.cell("dance", 5 + i, 4 + j, name)
    # the beam: from the shaft's light, north, east along the wall, south, and
    # west into the crystal at the floor's edge
    r.cell("beam", 2, 9, "shaft_star")
    for y in range(4, 9):
        r.cell("beam", 2, y, "star_ns")
    r.cell("beam", 2, 3, "star_se")
    for x in range(3, 12):
        r.cell("beam", x, 3, "star_ew")
    r.cell("beam", 12, 3, "star_sw")
    for y in (4, 5):
        r.cell("beam", 12, y, "star_ns")
    r.cell("beam", 12, 6, "star_nw")
    r.cell("beam", 11, 6, "star_ew")
    r.cell("beam", 13, 8, "base")
    r.sprites.append((*PLAYER, FACING["north"], False, 9, 5))
    return r


STARRY = ["###############",
          "##.....ss....##",
          "#.............#",
          "...............",
          "...............",
          "...............",
          "...............",
          "...............",
          "#.............#",
          "##...........##"]


def starry_scene():
    r = Room(15, 10, "mychos")
    r.walls(STARRY, floor="marble")
    r.cell("stairs", 7, 1, "up_l")
    r.cell("stairs", 8, 1, "up_r")
    # the star-clock's ring round the basin
    x0, y0, x1, y1 = 2, 3, 12, 9
    for x in range(x0 + 1, x1):
        r.cell("clock", x, y0, "h_star" if (x - x0) % 3 == 0 else "h")
    for x in range(x0 + 1, x1):
        r.cell("clock", x, y1, "h_star" if (x - x0) % 3 == 0 else "h")
    r.cell("clock", x0, y0, "nw")
    r.cell("clock", x1, y0, "ne")
    r.cell("clock", x0, y1, "sw")
    r.cell("clock", x1, y1, "se")
    for y in range(y0 + 1, y1):
        r.cell("clock", x0, y, "v_star" if (y - y0) % 3 == 0 else "v")
        r.cell("clock", x1, y, "v_star" if (y - y0) % 3 == 0 else "v")
    # the basin inside it
    bx0, by0, bx1, by1 = 3, 4, 11, 8
    waters = ["water", "water_b", "water_c", "water_d", "water_e", "water_f", "water_g",
              "water_h"]
    for y in range(by0, by1 + 1):
        for x in range(bx0, bx1 + 1):
            n, s_, w, e = y == by0, y == by1, x == bx0, x == bx1
            name = ("n" if n else "s" if s_ else "") + ("w" if w else "e" if e else "")
            if not name:
                name = waters[(x * 3 + y * 5) % len(waters)]
            r.cell("basin", x, y, name)
    r.cell("basin", 7, by0, "steps_n")
    # the anvil at the far edge, the pillar of horns at the near
    r.cell("star_anvil", 9, 2, "l")
    r.cell("star_anvil", 10, 2, "r")
    r.put("horns", 13, 5)
    r.sprites.append((*PLAYER, FACING["north"], False, 7, 9))
    return r


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
FACING = {"south": 0, "north": 1, "west": 2, "east": 2}


def draw_sprites(img, sprites):
    a = np.array(img)
    for (path, pal, frame, flip, x, y) in sprites:
        s = load_sprite(path, pal, frame)
        if flip:
            s = s[:, ::-1]
        px, py = x * 16, y * 16 - 16
        h, w = s.shape[:2]
        reg = a[max(0, py):py + h, px:px + w]
        sub = s[max(0, -py):]
        m = sub[..., 3] > 0
        reg[m] = sub[..., :3][m]
    return Image.fromarray(a)


def render(room, palettes=None, primary_black=False):
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    prim = rm.Tileset(rm.resolve_tileset("oikos", syms))
    tdir = ROOT / f"data/tilesets/secondary/{room.tileset}"
    sec = rm.Tileset(rm.resolve_tileset(str(tdir.relative_to(ROOT)), syms))
    if palettes:
        sec.pals = [rm.load_pal(tdir / "porytiles_bin" / palettes / f"{i:02d}.pal")
                    if 6 <= i <= 12 else sec.pals[i] for i in range(16)]
    if primary_black:
        prim.pals = [np.zeros((16, 3), np.uint8) for _ in range(16)]
    r = rm.Renderer(prim, sec)
    return rm.render_blocks(r, room.blockdata(), room.w)


def darkness(img, holes, zones):
    """Black out all but the torch's circles and the lit zones (in pixels), as
    SYSTEMS.md §2's flash levels show a dark map."""
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


# name: (builder, tileset, palette set, post-process)
SCENES = {
    "workshop": (lambda: workshop("lit"), "labyrinth", None, None),
    "workshop_dawn": (lambda: workshop("dawn"), "labyrinth", "dawn", None),
    "ring": (ring, "labyrinth", None, None),
    # the torch's 3.5-tile radius round the player (flash level 3), and the
    # brazier's lit zone, the north hall
    "ring_dark": (ring, "labyrinth", None,
                  lambda img: darkness(img, [(11 * 16 + 8, 6 * 16 - 0, 56)],
                                       [(0, 0, 9 * 16, 4 * 16)])),
    "ring_doused": (ring, "labyrinth", "glow", "black"),
    "hunt": (lambda: hunt("day"), "labyrinth", None, None),
    "hunt_night": (lambda: hunt("night"), "labyrinth", None,
                   lambda img: darkness(img, [(11 * 16 + 8, 4 * 16, 56)],
                                        [(6 * 16, 3 * 16, 9 * 16, 5 * 16)])),
    "tomb": (tomb, "labyrinth", None, None),
    "shaft": (shaft, "labyrinth", "dawn", None),
    "forge": (forge_scene, "mychos", None, None),
    "choros": (choros_scene, "mychos", None, None),
    "starry": (starry_scene, "mychos", None, None),
}


def scene_names():
    return SCENES


def load_catalog(tileset, fast):
    if tileset in CATS:
        return
    if fast:
        secs = A.build(tileset)
        A.pack(secs)
        STRUCTS[tileset] = {}
        CATS[tileset] = {}
        for _, ss in secs:
            for s in ss:
                STRUCTS[tileset][s.key] = s
                CATS[tileset][s.key] = {
                    "key": s.key, "w": s.w, "h": s.h, "ids": s.ids, "walk": s.walk,
                    "names": {n: list(v) for n, v in s.names.items()},
                    "twin_of": list(getattr(s, "twin_of", None) or []) or None}
        return
    cat = ROOT / f"build/{tileset}/catalog.json"
    meta = ROOT / f"data/tilesets/secondary/{tileset}/porytiles_bin/metatiles.bin"
    if not meta.exists() or meta.stat().st_mtime < cat.stat().st_mtime:
        sys.exit(f"labyrinth_scene: the compiled {tileset} is older than its catalog; "
                 "run labyrinth_build.py (and let it finish) first")
    CATS[tileset] = {s["key"]: s for s in json.loads(cat.read_text())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pass", dest="pass_no", type=int)
    ap.add_argument("--only")
    ap.add_argument("--scale", type=int, default=3)
    args = ap.parse_args()
    IMG.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    for name, (fn, tileset, pals, post) in scene_names().items():
        if args.only and name not in args.only.split(","):
            continue
        load_catalog(tileset, args.fast)
        room = fn()
        if args.fast:
            img = room.render_fast()
        else:
            img = render(room, palettes=pals, primary_black=(post == "black"))
        if post not in (None, "black") and callable(post):
            img = draw_sprites(img, room.sprites)
            img = post(img)
        elif post != "black":
            img = draw_sprites(img, room.sprites)
        img = img.resize((img.width * args.scale, img.height * args.scale), Image.NEAREST)
        dst = (BUILD if args.fast else IMG) / f"labyrinth_scene_{name}.png"
        img.save(dst)
        print(dst)
        if args.pass_no is not None and not args.fast:
            p = IMG / f"labyrinth_scene_{name}_pass{args.pass_no}.png"
            img.save(p)
            print(p)


if __name__ == "__main__":
    main()
