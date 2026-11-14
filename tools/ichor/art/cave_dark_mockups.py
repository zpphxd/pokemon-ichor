#!/usr/bin/env python3
"""Mock-up rooms for gTileset_CaveDark, rendered lit and in the dark.

Each room is composed from the catalog (data/tilesets/secondary/cave_dark/
catalog.json) the way a map builder would: a terrain grid the kit's
autotiler turns into rock, faces, floor, lit floor and water, then pieces
placed by name. The rooms are throwaway block data, not maps; the map batch
builds the real layouts.

Renders come from the compiled tileset through tools/ichor/render_map.py on
aethos, so they show exactly what the game will draw. For each room:

  design/phase2/img/cave_dark_<room>.png       at 2x, fully lit
  design/phase2/img/cave_dark_<room>_dark.png  at 2x, as a dark map shows it:
      black but for the torch's circle round the player (flash level 7 is
      24 px, Hecate's Torch 56 px: SYSTEMS.md §2) and the pools of light of
      lit braziers and lit zones

Usage: /usr/bin/python3 tools/ichor/art/cave_dark_mockups.py [ROOM ...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools/ichor"))
import cave_dark_kit as kit  # noqa: E402
import render_map as rm  # noqa: E402

CATALOG = ROOT / "data/tilesets/secondary/cave_dark/catalog.json"
TS = ROOT / "data/tilesets/secondary/cave_dark"
IMG = ROOT / "design/phase2/img"
SPRITES = ROOT / "graphics/object_events/pics/people"

TORCH_NONE, TORCH_HECATE = 24, 56     # flash radii, px (src/field_screen_effect.c)
HALO = 32                              # a lit brazier's pool (the 64x64 halo sprite, SYSTEMS.md §2)


class Catalog:
    def __init__(self):
        self.data = json.loads(CATALOG.read_text())
        self.pieces = {p["key"]: p for p in self.data["pieces"]}

    def kit_id(self, key, style=None):
        return kit.kit_id(self.data, key, style)


class Room:
    """A terrain grid plus placed pieces; style picks a wall look for a region."""

    def __init__(self, name, grid, style=None):
        self.name = name
        self.grid = [r for r in grid.strip("\n").splitlines()]
        w = max(len(r) for r in self.grid)
        self.grid = [r.ljust(w, "#") for r in self.grid]
        self.H, self.W = len(self.grid), w
        self.style = style
        self.places = []          # (key, x, y)
        self.actors = []          # (sprite path, frame, x, y)
        self.player = None
        self.halos = []           # (x, y) cell of a lit light source's center, px offset
        self.zones = []           # lit rectangles in cells (x0, y0, x1, y1)
        self.torch = TORCH_HECATE

    def put(self, key, x, y):
        self.places.append((key, x, y))
        return self

    def actor(self, path, x, y, frame=0):
        self.actors.append((path, frame, x, y))
        return self

    def blocks(self, cat):
        ids = np.array(kit.autotile(self.grid, cat.data, self.style), np.uint16)
        for key, x, y in self.places:
            if key.startswith("kit:"):
                ids[y, x] = cat.kit_id(key[4:], self.style)
                continue
            p = cat.pieces[key]
            for j in range(p["h"]):
                for i in range(p["w"]):
                    ids[y + j, x + i] = p["ids"][j][i]
        return ids


def renderer():
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                       rm.Tileset(rm.tileset_from_dir(TS)))


def sprite(path, frame=0):
    im = Image.open(path)
    pal = im.getpalette()
    a = np.array(im)
    fr = a[:, frame * 16:frame * 16 + 16]
    rgba = np.zeros((32, 16, 4), np.uint8)
    for y in range(32):
        for x in range(16):
            i = fr[y, x]
            if i:
                rgba[y, x, :3] = pal[i * 3:i * 3 + 3]
                rgba[y, x, 3] = 255
    return rgba


def paste(img, rgba, px, py):
    h, w = rgba.shape[:2]
    for y in range(h):
        for x in range(w):
            if rgba[y, x, 3] and 0 <= py + y < img.shape[0] and 0 <= px + x < img.shape[1]:
                img[py + y, px + x] = rgba[y, x, :3]


def render(room, cat, r):
    ids = room.blocks(cat)
    img = np.array(rm.render_blocks(r, ids.flatten(), room.W))
    for path, frame, x, y in room.actors:
        paste(img, sprite(path, frame), x * 16, y * 16 - 16)
    if room.player:
        px, py = room.player
        paste(img, sprite(SPRITES / "brendan/walking.png", 0), px * 16, py * 16 - 16)
    return img, ids


def glow_renderer():
    """A renderer with the glow copy loaded (SYSTEMS.md §2, dousing): flash
    level 0, every palette black but Hecate's chalk."""
    r = renderer()
    pals = [rm.load_pal(TS / "glow" / f"{i:02d}.pal") for i in range(16)]
    r.pals = np.stack([pals[i] for i in range(16)])
    r.backdrop = np.zeros(3, np.uint8)
    r.cache = {}
    return r


def douse(room, cat):
    """The room as the torch-doused player sees it: the chalk alone, glowing.
    Sprites keep their own palettes, so the player still shows."""
    ids = room.blocks(cat)
    img = np.array(rm.render_blocks(glow_renderer(), ids.flatten(), room.W))
    if room.player:
        px, py = room.player
        paste(img, sprite(SPRITES / "brendan/walking.png", 0), px * 16, py * 16 - 16)
    return img


def darken(room, img):
    """What a dark map shows: the flash circle round the player, plus lit zones
    and the halos of lit braziers. Everything else is the black backdrop."""
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    lit = np.zeros((H, W), bool)
    if room.player:
        cx, cy = room.player[0] * 16 + 8, room.player[1] * 16 + 8
        lit |= (xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= room.torch ** 2
    for halo in room.halos:
        hx, hy = halo[:2]
        r = halo[2] if len(halo) > 2 else HALO
        lit |= (xx + 0.5 - hx) ** 2 + (yy + 0.5 - hy) ** 2 <= r ** 2
    for x0, y0, x1, y1 in room.zones:
        lit[y0 * 16:y1 * 16, x0 * 16:x1 * 16] = True
    if getattr(room, "lit_cells", False):
        for y, row in enumerate(room.grid):
            for x, ch in enumerate(row):
                if ch == ",":
                    lit[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = True
    out = img.copy()
    out[~lit] = 0
    return out


def save(img, path, scale=2):
    Image.fromarray(img).resize((img.shape[1] * scale, img.shape[0] * scale), Image.NEAREST).save(path)


def screen(room, img):
    """A 15x10 GBA screen round the player."""
    if not room.player:
        return img
    px, py = room.player
    x0 = max(0, min(room.W * 16 - 240, px * 16 + 8 - 120))
    y0 = max(0, min(room.H * 16 - 160, py * 16 + 8 - 80))
    return img[y0:y0 + 160, x0:x0 + 240]


# --------------------------------------------------------------------------
# The rooms
# --------------------------------------------------------------------------

ELDER = SPRITES / "ichor/elder_f.png"
HOPLITE = SPRITES / "ichor/hoplite.png"


def entrance():
    """The Hollow's east mouth: daylight from Route 2, the old woman and her
    covered dish, and the passage west where the dark begins (beat 18)."""
    rm_ = Room("entrance", """
##########################
##########################
##########################
####......################
###........###############
###.........######....####
###..........####......###
####...........#......,,..
####..................,,..
#####.................,,..
######..........#......###
######.........###.....###
#######.......#####....###
#######.......#####...####
##########################
##########################
""")
    for y in (7, 8, 9):
        rm_.put("daylight_e", 24, y)
    rm_.put("stalagmite_tall", 5, 6).put("stalagmites", 13, 11).put("rock_pile", 7, 12)
    rm_.put("pebbles", 12, 10).put("pebbles", 19, 9).put("boulder", 20, 12)
    rm_.put("ledge_w", 6, 8).put("ledge_a", 7, 8).put("ledge_b", 8, 8).put("ledge_a", 9, 8)
    rm_.put("ledge_e", 10, 8)
    rm_.put("stele", 21, 6).put("dish_covered", 21, 9).put("chalk_arrow_w", 9, 10)
    rm_.put("column", 16, 6)
    rm_.actor(ELDER, 22, 9)
    rm_.player = (18, 8)
    rm_.torch = TORCH_NONE
    rm_.halos = [(26 * 16, 8 * 16 + 8, 52)]
    return rm_


def three_roads():
    """The Three Roads: the round chamber where the forks meet, lit faintly
    from above, the Hekataion at its heart and Hecate's supper in a niche."""
    rm_ = Room("three_roads", """
#########################
#########################
##..######################
##...#####################
###...####.......#########
####.......,,,,.......####
####......,,,,,,..........
###......,,,,,,,,.........
###.....,,,,,,,,,,........
###.....,,,,,,,,,,.....###
####....,,,,,,,,,,.....###
####.....,,,,,,,,......###
#####.....,,,,,,......####
######......,,.......#####
########............######
##########.......#########
##########.......#########
##########.......#########
""")
    rm_.put("hekataion", 11, 6)
    rm_.put("niche_supper", 14, 2)
    rm_.put("bones", 15, 4)
    rm_.put("chalk_triangle_lit", 12, 11)
    rm_.put("chalk_wheel", 8, 2)
    # Hecate's chalk marks the way out west; it shows best with the torch doused
    rm_.put("chalk_arrow_w", 6, 6).put("chalk_arrow_n", 4, 4).put("chalk_arrow_n", 12, 15)
    rm_.doused = True
    rm_.put("stalagmite", 5, 9).put("stalagmites", 19, 12).put("pebbles", 6, 11)
    rm_.player = (12, 14)
    rm_.torch = TORCH_NONE
    rm_.halos = [(12 * 16 + 8, 8 * 16 + 8, 64)]     # the faint light from above
    return rm_


def web_passage():
    """A side passage curtained with cobweb (the Arachne lead, SCRIPT.md), and
    beside it one already burnt through with Hecate's Torch."""
    rm_ = Room("web_passage", """
########################
########################
###......###############
##........######......##
##........######......##
###......########....###
#####..#############..##
#####..#############..##
#####..#############..##
####....##########.....#
##.......................
##.......................
##......................#
###.....####.......######
########################
########################
""")
    rm_.put("web_2", 5, 7).put("torn_2", 20, 7)
    rm_.put("web_corner_w", 2, 10).put("web_corner_e", 7, 9).put("web_corner_w", 4, 4)
    rm_.put("web_corner_e", 9, 4).put("pebbles", 12, 11).put("stalagmite", 15, 12)
    rm_.put("bones", 6, 3).put("rock_pile", 3, 11)
    rm_.player = (6, 10)
    return rm_


def brazier_room():
    """A chamber on the way out west: two bronze braziers, one lit, its light
    a landmark for the walk back; stone, a ledge and a column."""
    rm_ = Room("brazier_room", """
##########################
##########################
##########################
####.....~~~~#############
###......~~~~.######.....#
###.......~~...####......#
##.......................#
##........................
##.......................#
###......................#
####.........#####.......#
####........#######.....##
#####......#########...###
#####......#########...###
##########################
##########################
""")
    rm_.put("seep", 11, 1)
    rm_.put("brazier_lit", 5, 4).put("brazier_cold", 19, 6)
    rm_.put("stalagmite_tall", 15, 7).put("stalagmites", 3, 9)
    rm_.put("ledge_w", 3, 7).put("ledge_a", 4, 7).put("ledge_b", 5, 7).put("ledge_a", 6, 7)
    rm_.put("ledge_e", 7, 7)
    rm_.put("rock_pile", 23, 9).put("pebbles", 8, 11).put("slab", 21, 11)
    rm_.player = (17, 8)
    rm_.halos = [(5 * 16 + 16, 4 * 16 + 14)]
    rm_.actor(HOPLITE, 9, 7)
    return rm_


def rooms():
    out = [entrance(), three_roads(), web_passage(), brazier_room()]
    try:
        import cave_dark_places
        out += cave_dark_places.mockups(Room, SPRITES)
    except (ImportError, AttributeError):
        pass
    return out


def main():
    cat = Catalog()
    r = renderer()
    want = sys.argv[1:]
    IMG.mkdir(parents=True, exist_ok=True)
    for room in rooms():
        if want and room.name not in want:
            continue
        img, _ = render(room, cat, r)
        save(img, IMG / f"cave_dark_{room.name}.png")
        save(darken(room, img), IMG / f"cave_dark_{room.name}_dark.png")
        if getattr(room, "doused", False):
            save(douse(room, cat), IMG / f"cave_dark_{room.name}_doused.png")
        print(IMG / f"cave_dark_{room.name}.png")


if __name__ == "__main__":
    main()
