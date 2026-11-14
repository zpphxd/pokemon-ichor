#!/usr/bin/env python3
"""Lay out the civic slice rooms as layout blockdata, and render them.

Writes design/phase1/rooms/<room>.bin (u16 per block: metatile id, collision
in bits 10-11, elevation in bits 12-15, as in data/layouts/*/map.bin) and
renders design/phase1/img/rooms_<room>.png at 3x. Every room is rendered over
two different primaries and the renders must match exactly, which proves civic
draws nothing from the primary.

Each room below is a grid of metatile names from civic_tiles.py. Objects that
span several cells are placed with put(), which names each cell
prefix_X_Y. Walkable cells get elevation 3 and solid ones collision 1, the
convention of Emerald's interiors.

Usage: /usr/bin/python3 tools/ichor/art/civic_rooms.py
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import civic_tiles as ct  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
ROOMS = ROOT / "design/phase1/rooms"
IMG = ROOT / "design/phase1/img"
RENDER = ROOT / "tools/ichor/render_map.py"


class Room:
    def __init__(self, name, w, h, fill):
        self.name, self.w, self.h = name, w, h
        self.grid = [[fill(x, y) for x in range(w)] for y in range(h)]
        self.solid_override = {}

    def set(self, x, y, name):
        if name not in ct.BY_NAME:
            raise KeyError(f"{self.name}: no metatile {name}")
        self.grid[y][x] = name

    def row(self, y, x0, names):
        for i, n in enumerate(names):
            self.set(x0 + i, y, n)

    def put(self, prefix, x, y, w, h):
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, f"{prefix}_{i}_{j}")

    def blocks(self):
        out = np.zeros(self.w * self.h, np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                n = self.grid[y][x]
                mid = ct.FIRST_ID + ct.BY_NAME[n]
                solid = self.solid_override.get((x, y), ct.METATILES[ct.BY_NAME[n]]["solid"])
                out[y * self.w + x] = mid | (0x0400 if solid else 0x3000)
        return out


def checker(a, b):
    return lambda x, y: a if (x + y) % 2 == 0 else b


# --- the Akti Asclepeion -----------------------------------------------------

def asclepeion():
    r = Room("akti_asclepeion", 15, 11, checker("asc_floor_a", "asc_floor_b"))
    # Back wall.
    r.row(0, 0, ["asc_wall_top_l"] + ["asc_wall_top"] * 13 + ["asc_wall_top_r"])
    r.row(1, 0, ["asc_wall_l"] + ["asc_wall"] * 13 + ["asc_wall_r"])
    r.row(2, 0, [("asc_floor_a_sh" if x % 2 == 0 else "asc_floor_b_sh") for x in range(15)])
    # Stairs up in the back-left corner, Asclepius in his niche beside them.
    r.put("asc_stairs", 0, 0, 2, 3)
    r.put("asc_statue", 2, 0, 1, 3)
    # The healer's counter: spring basin, the healer, the votives.
    r.put("asc_relief", 7, 0, 1, 2)
    r.put("asc_basin", 5, 1, 2, 2)
    r.put("asc_votive_wall", 8, 1, 2, 1)
    r.set(4, 2, "asc_counter_l")
    r.set(7, 2, "asc_counter_staff")
    r.put("asc_votive_counter", 8, 2, 2, 1)
    r.set(10, 2, "asc_counter_r")
    r.row(3, 4, ["asc_counter_front_l"] + ["asc_counter_front_m"] * 5 + ["asc_counter_front_r"])
    # The Pithos corner.
    r.put("asc_jar", 11, 1, 1, 2)
    r.put("asc_pithos", 12, 0, 2, 3)
    r.put("asc_jar", 14, 1, 1, 2)
    # Colonnade and the couches' alcove.
    for x in (2, 12):
        r.put("asc_column", x, 3, 1, 3)
        r.put("asc_column", x, 7, 1, 3)
    r.put("asc_kline", 0, 4, 2, 2)
    r.put("asc_kline", 0, 7, 2, 2)
    r.set(1, 9, "asc_snake_0_0")
    # The floor mosaic between two braziers, a bench by the door, the threshold.
    r.put("asc_mosaic", 6, 5, 3, 3)
    r.put("asc_brazier", 4, 5, 1, 2)
    r.put("asc_brazier", 10, 5, 1, 2)
    r.put("asc_bench", 13, 9, 2, 1)
    r.set(7, 10, "asc_mat")
    return r


# --- the Akti Agora ----------------------------------------------------------

def agora():
    r = Room("akti_agora", 13, 9, lambda x, y: "ago_floor")
    r.row(0, 0, ["ago_wall_top_l"] + ["ago_wall_top"] * 11 + ["ago_wall_top_r"])
    r.row(1, 0, ["ago_wall_l"] + ["ago_wall"] * 11 + ["ago_wall_r"])
    r.row(2, 0, ["ago_floor_sh"] * 13)
    # Cloth and herbs hang from the beam; pottery shelves on the right.
    r.put("ago_cloth_purple", 1, 0, 1, 2)
    r.put("ago_cloth_blue", 5, 0, 1, 2)
    r.put("ago_herbs", 6, 0, 1, 2)
    r.put("ago_herbs", 7, 0, 1, 2)
    r.put("ago_cloth_saffron", 8, 0, 1, 2)
    for x in (9, 10, 11):
        r.put("ago_shelf", x, 0, 1, 3)
    # Demeas's stall: the awning, the counter with the scale, its front.
    r.put("ago_awning", 2, 0, 3, 2)
    r.row(2, 2, ["ago_counter_l", "ago_counter_staff", "ago_counter_r"])
    r.row(3, 2, ["ago_counter_front_l", "ago_counter_front_m", "ago_counter_front_r"])
    # The stoa's inner colonnade, the money-changer's table behind it.
    for x in (1, 4, 8, 11):
        r.put("ago_column", x, 5, 1, 3)
    r.put("ago_trapeza", 6, 4, 2, 2)
    # Goods on the floor and jars.
    r.set(0, 3, "ago_basket_grain")
    r.set(0, 4, "ago_basket_olives")
    r.set(10, 3, "ago_basket_figs")
    r.set(11, 3, "ago_basket_pomegranates")
    r.put("ago_amphora", 12, 3, 1, 2)
    r.put("ago_jar", 0, 7, 1, 2)
    r.put("ago_jar", 12, 7, 1, 2)
    r.set(6, 8, "ago_mat")
    return r


# --- the Elaia Akademia ------------------------------------------------------

def akademia():
    def fill(x, y):
        if x < 4:
            return "aka_grass"
        if x == 4:
            return "aka_stylobate"
        return "aka_floor" if (x * 7 + y * 3) % 5 else "aka_floor_b"
    r = Room("elaia_akademia", 16, 13, fill)
    # The grove on the left behind its hedge, opening through a colonnade.
    r.row(0, 0, ["aka_hedge_top"] * 4)
    r.row(1, 0, ["aka_hedge"] * 4)
    r.row(2, 0, ["aka_grass_sh"] * 4)
    for x, y in ((0, 8), (3, 5), (2, 11), (1, 3), (3, 12)):
        r.set(x, y, "aka_grass_flowers")
    r.put("aka_laurel", 1, 3, 2, 3)
    r.put("aka_bench", 1, 9, 2, 1)
    r.set(4, 2, "aka_stylobate_sh")
    for y in (2, 6, 10):
        r.put("aka_column", 4, y, 1, 3)
    r.set(4, 2, "aka_column_cap_sh")
    # The hall's back wall.
    r.row(0, 4, ["aka_wall_top_l"] + ["aka_wall_top"] * 10 + ["aka_wall_top_r"])
    r.row(1, 4, ["aka_wall_l"] + ["aka_wall"] * 10 + ["aka_wall_r"])
    for x in range(5, 16):
        r.set(x, 2, "aka_floor_sh" if x % 3 else "aka_floor_b_sh")
    r.put("aka_specimens", 5, 1, 1, 2)
    r.put("aka_map", 6, 0, 2, 2)
    r.put("aka_scrolls", 12, 0, 2, 3)
    r.put("aka_scrolls", 14, 0, 2, 3)
    # Daphne's table with the three kraters; the armillary sphere beside it.
    r.row(3, 8, ["aka_table_l", "aka_krater_snivy", "aka_krater_cyndaquil",
                 "aka_krater_piplup", "aka_table_r"])
    r.row(4, 8, ["aka_table_front_0_0"] + ["aka_table_front_1_0"] * 3 + ["aka_table_front_2_0"])
    r.put("aka_armillary", 6, 3, 1, 2)
    # Two writing desks with stools.
    for x in (6, 11):
        r.put("aka_desk", x, 7, 2, 2)
        r.set(x, 9, "aka_stool")
    # Alethea's corner of finds.
    r.put("aka_worktable", 13, 10, 2, 2)
    r.set(15, 9, "aka_crate")
    r.put("aka_amphora", 15, 10, 1, 2)
    r.set(12, 11, "aka_head")
    r.set(15, 12, "aka_tools")
    r.set(10, 12, "aka_mat")
    return r


ALL = [asclepeion, agora, akademia]


def render(blockfile, width, primary, out):
    subprocess.run(["/usr/bin/python3", str(RENDER), "--blockdata", str(blockfile), "--width", str(width),
                    "--primary", primary, "--secondary", "civic", "--scale", "3", "-o", str(out)],
                   cwd=ROOT, check=True, capture_output=True)


def main():
    ct.define()
    ROOMS.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "build/render"
    tmp.mkdir(parents=True, exist_ok=True)
    for make in ALL:
        room = make()
        f = ROOMS / f"{room.name}.bin"
        room.blocks().tofile(f)
        out = IMG / f"rooms_{room.name}.png"
        render(f, room.w, "aethos", out)
        render(f, room.w, "building", tmp / f"{room.name}_building.png")
        a = np.array(Image.open(out))
        b = np.array(Image.open(tmp / f"{room.name}_building.png"))
        same = a.shape == b.shape and (a == b).all()
        print(f"{room.name}: {room.w}x{room.h} -> {f.relative_to(ROOT)}; "
              f"aethos vs building renders {'identical' if same else 'DIFFER'}")
        if not same:
            sys.exit(1)


if __name__ == "__main__":
    main()
