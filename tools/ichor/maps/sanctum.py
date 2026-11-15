#!/usr/bin/env python3
"""The Mystery sanctum under Eleusa's Telesterion: three floors, built and checked.

design/phase2/SCRIPT.md, beat 23 and Part 5 ("The Mystery sanctum"); the plan is
design/phase2/MAPS_sanctum.md. Teach, test, payoff:

  B1F  the granaries (36x28): rock-cut halls of grain pits and great jars under the
       Telesterion. Dark; four braziers along the walls, each lighting its stretch
       (FLAG_ICHOR_BRAZIERS_START + 0x18..0x1B). The Anaktoron's stair comes down in
       the north-west, the Ploutonion's in the north-east. Chloe holds the stair.
  B2F  the Hall of the Kore (20x40): a long frescoed hall, its four panels read south
       to north, a chasm down the middle, grain pits crossed on Hecate's chalk in the
       near half, the iron-tasting spring halfway, Konis at the far stair.
  B3F  the deepest granary (18x18): a round vault, the bronze chest, the Titans'
       tunnel through the wall: Hyperion.

No tileset is drawn for it. The floors are built from two existing secondaries:
cave_dark's crypt style (TILES_cave_dark.md) for the granaries and the vault, and
temple_demeter (TILES_temple_demeter.md) for the Hall of the Kore, both on the oikos
primary. Each gets a derived tileset that shares its tiles and palettes and adds a
few metatiles composed from existing tiles: braziers, oikos's pithoi and lamps on the
crypt's flagstones; grain pits from the still-water pieces in the fire palette; the
spring basin on the hall's flagstones; and cave behaviour (wild encounters) on the
hall's floor. They are written here, to data/tilesets/secondary/eleusa_sanctum_rock/
and eleusa_sanctum_hall/: run this builder again after either base set is rebuilt.

Writes the three layouts, each map.json's events, the generated block of each
scripts.pory, the derived tilesets' metatiles and the METATILE_EleusaSanctum*
labels. Checks every floor; --render DIR writes the review images.

Usage: /usr/bin/python3 tools/ichor/maps/sanctum.py [--render DIR]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import cave_dark_kit as kit  # noqa: E402

CD_DIR = ROOT / "data/tilesets/secondary/cave_dark"
TD_DIR = ROOT / "data/tilesets/secondary/temple_demeter"
OIKOS_DIR = ROOT / "data/tilesets/primary/oikos"
ROCK_DIR = ROOT / "data/tilesets/secondary/eleusa_sanctum_rock"
HALL_DIR = ROOT / "data/tilesets/secondary/eleusa_sanctum_hall"
TD_CAT_PATH = ROOT / "build/temple_demeter/catalog.json"
LABELS_H = ROOT / "include/constants/metatile_labels.h"

SECONDARY = 0x200
FIRST_FREE = 0x3E0          # cave_dark fills 0x200-0x3DF; temple_demeter far less
LAST_ID = 0x3FF
MB_NORMAL, MB_CAVE = 0x00, 0x08
LAYER_COVERED = 1

# --- Reading the base sets ------------------------------------------------------------------

CD_CAT = json.loads((CD_DIR / "catalog.json").read_text())
CD_PIECE = {p["key"]: p for p in CD_CAT["pieces"]}


def load_bins(d):
    mt = np.fromfile(d / "porytiles_bin/metatiles.bin", "<u2").reshape(-1, 8).copy()
    at = np.fromfile(d / "porytiles_bin/metatile_attributes.bin", "<u2").copy()
    return mt, at


OIKOS_MT = np.fromfile(OIKOS_DIR / "porytiles_bin/metatiles.bin", "<u2").reshape(-1, 8)


def td_catalog():
    if not TD_CAT_PATH.exists():
        sys.exit(f"{TD_CAT_PATH} is missing; run /usr/bin/python3 tools/ichor/art/temple_demeter_build.py "
                 "--no-compile first")
    cat = json.loads(TD_CAT_PATH.read_text())
    ids, walk = {}, {}
    for s in cat["structures"]:
        names = {tuple(v): k for k, v in s.get("names", {}).items()}
        for j in range(s["h"]):
            for i in range(s["w"]):
                n = names.get((i, j), f"r{j}c{i}")
                ids[f"{s['key']}.{n}"] = s["ids"][j][i]
                walk[f"{s['key']}.{n}"] = s["walk"][j][i]
    return ids, walk


TD, TD_WALK = td_catalog()


# --- Derived tilesets -----------------------------------------------------------------------

class Derived:
    """A secondary that shares a base set's tiles and palettes: its metatiles are the
    base's, plus composed ones from FIRST_FREE up, with their own attributes."""

    def __init__(self, name, base_dir, label_prefix):
        self.name, self.label_prefix = name, label_prefix
        self.mt, self.at = load_bins(base_dir)
        self.base_count = len(self.mt)
        # composed metatiles start on the next row of 8 after the base set's
        self.first = SECONDARY + (self.base_count + 7) // 8 * 8
        if self.first > FIRST_FREE:
            sys.exit(f"sanctum: {base_dir.name} has grown to 0x{SECONDARY + self.base_count:03X}; "
                     "the derived set needs its composed metatiles moved")
        pad = self.first - SECONDARY - self.base_count
        self.mt = np.vstack([self.mt, np.zeros((pad, 8), np.uint16)])
        self.at = np.concatenate([self.at, np.zeros(pad, np.uint16)])
        self.made = {}           # key -> id
        self.labels = {}         # label -> id

    def entries(self, mid):
        """The 8 entries of a metatile id (primary oikos, or this set)."""
        if mid < SECONDARY:
            return [int(v) for v in OIKOS_MT[mid]]
        return [int(v) for v in self.mt[mid - SECONDARY]]

    def attr(self, mid):
        return int(self.at[mid - SECONDARY])

    def add(self, key, entries, behavior=MB_NORMAL, layer=LAYER_COVERED, label=None):
        if key in self.made:
            return self.made[key]
        mid = SECONDARY + len(self.mt)
        if mid > LAST_ID:
            sys.exit(f"sanctum: {self.name} is out of metatile slots at {key}")
        self.mt = np.vstack([self.mt, np.array(entries, np.uint16)[None, :]])
        self.at = np.concatenate([self.at, np.array([behavior | (layer << 12)], np.uint16)])
        self.made[key] = mid
        if label:
            self.labels[label] = mid
        return mid

    def over(self, key, ground, obj, label=None, behavior=None):
        """ground's bottom layer under obj's middle layer (an object on another floor)."""
        g, o = self.entries(ground), self.entries(obj)
        b = behavior if behavior is not None else MB_NORMAL
        return self.add(key, g[:4] + o[4:], b, LAYER_COVERED, label)

    def recolor(self, key, mid, pal_from, pal_to, behavior=MB_NORMAL, label=None):
        e = [((v & 0x0FFF) | (pal_to << 12)) if (v >> 12) == pal_from else v for v in self.entries(mid)]
        return self.add(key, e, behavior, (self.attr(mid) >> 12) & 0xF, label)

    def write(self, d):
        d.mkdir(parents=True, exist_ok=True)
        self.mt.astype("<u2").tofile(d / "metatiles.bin")
        self.at.astype("<u2").tofile(d / "metatile_attributes.bin")


# --- Small helpers ---------------------------------------------------------------------------

def noise(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 100


def reach(solid, start, w, h, blocked=frozenset()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < w and 0 <= p[1] < h and p not in seen and not solid[p[1]][p[0]] and p not in blocked:
                seen.add(p)
                q.append(p)
    return seen


def check_rows(name, rows, w, h):
    if len(rows) != h or any(len(r) != w for r in rows):
        bad = [(i, len(r)) for i, r in enumerate(rows) if len(r) != w]
        sys.exit(f"sanctum: {name}'s grid is {len(rows)} rows (want {h}); rows of the wrong width: {bad}")


# --- A floor --------------------------------------------------------------------------------

CRYPT_FLOOR = kit.kit_id(CD_CAT, "floor|..", "crypt")
CRYPT_FLOOR_V2 = kit.kit_id(CD_CAT, "floor|..|v2", "crypt")
CRYPT_FLOORS = {v for k, v in CD_CAT["styles"]["crypt"].items() if k.startswith("floor|")}
# oikos objects (TILES_oikos.md), drawn in their middle layer over a floor
OIKOS = {"pithos": [[0x034], [0x03C]], "amphora": [[0x043]], "lampstand": [[0x027], [0x02F]],
         "krater": [[0x084]], "chest": [[0x041]], "basin": [[0x04D, 0x04E]],
         "column3": [[0x032], [0x03A], [0x042]]}
# cave_dark pieces painted over the cave's floor, recomposed over the crypt's
ON_CAVE_FLOOR = {"brazier_cold", "brazier_lit", "hole_down", "stalagmite", "stalagmites", "boulder",
                 "rock_pile", "pebbles", "slab", "column", "stalagmite_tall", "bones"}


class Floor:
    def __init__(self, name, map_id, layout_id, w, h, derived, secondary):
        self.name, self.map_id, self.layout_id = name, map_id, layout_id
        self.w, self.h = w, h
        self.d = derived
        self.secondary = secondary
        self.ids = [[0] * w for _ in range(h)]
        self.solid = [[True] * w for _ in range(h)]
        self.kind = [[""] * w for _ in range(h)]        # what the cell is, for checks and renders
        self.border = [0, 0, 0, 0]
        self.objects, self.warps, self.coords, self.bgs = [], [], [], []

    def set(self, x, y, mid, solid, kind=""):
        self.ids[y][x] = mid
        self.solid[y][x] = solid
        if kind:
            self.kind[y][x] = kind

    # -- the rock floors (cave_dark, crypt style) ----------------------------------------
    def autotile(self, rows, style="crypt", region=None):
        """Terrain from a grid: '#' rock, '~' a grain pit (still water, recoloured),
        anything else floor. region(x, y): only those cells."""
        grid = ["".join("~" if c == "~" else "#" if c == "#" else "." for c in r) for r in rows]
        ids = kit.autotile(grid, CD_CAT, style=style)
        kinds = kit.classify(grid)
        for y in range(self.h):
            for x in range(self.w):
                if region and not region(x, y):
                    continue
                mid, k = ids[y][x], kinds[y][x]
                if k == "water":
                    key = kit.cell_key(grid, kinds, x, y, style)
                    mid = self.d.recolor("pit:" + key, mid, 12, 7)
                    self.set(x, y, mid, True, "pit")
                elif k in ("T", "ft", "fb"):
                    self.set(x, y, mid, True, "rock")
                else:
                    if mid == CRYPT_FLOOR_V2 and noise(x, y, 7) < 40:
                        mid = CRYPT_FLOOR
                    self.set(x, y, mid, False, "floor")

    def ground(self, x, y):
        """The floor a composed object stands on: plain crypt flagstones, or plain cave
        floor in the Titans' tunnel (None: the piece's own ground is right as drawn).
        Shadowed floor variants are not kept under objects: slots are few."""
        mid = self.ids[y][x]
        if mid in CRYPT_FLOORS:
            return CRYPT_FLOOR
        return None

    def piece(self, key, x, y, label=None, solid=None):
        """A cave_dark piece, or an oikos object (OIKOS), with its top-left at (x, y)."""
        if key in OIKOS:
            for j, row in enumerate(OIKOS[key]):
                for i, obj in enumerate(row):
                    g = self.ground(x + i, y + j) or kit.kit_id(CD_CAT, "floor|..")
                    mid = self.d.over(f"{key}{i}{j}@{g:03X}", g, obj,
                                      label=f"{label}_{i}{j}" if label else None)
                    self.set(x + i, y + j, mid, True if solid is None else solid, key)
            return
        p = CD_PIECE[key]
        for j, row in enumerate(p["ids"]):
            for i, pid in enumerate(row):
                walk = p["walk"][j][i]
                cx, cy = x + i, y + j
                lab = f"{label}_{i}{j}" if label else None
                g = self.ground(cx, cy) if key in ON_CAVE_FLOOR else None
                if g is not None:
                    beh = p.get("behaviors", {}).get(f"{i},{j}")
                    b = {"MB_NON_ANIMATED_DOOR": 0x60, "MB_CAVE": MB_CAVE}.get(beh, MB_NORMAL)
                    pid = self.d.over(f"{key}{i}{j}@{g:03X}", g, pid, label=lab, behavior=b)
                elif lab:
                    self.d.labels[lab] = pid
                self.set(cx, cy, pid, (walk == "X") if solid is None else solid, key)

    # -- events ---------------------------------------------------------------------------
    def person(self, lid, gfx, x, y, facing, script, flag="0", trainer=None, sight=0, movement=None):
        self.objects.append({
            "local_id": f"LOCALID_SANCTUM_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": movement or f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0,
            "movement_range_y": 0,
            "trainer_type": trainer or "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": str(sight),
            "script": f"{self.name}_EventScript_{script}", "flag": flag})

    def item(self, item, x, y, flag):
        self.objects.append({
            "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": item,
            "script": "Common_EventScript_FindItem", "flag": flag})

    def warp(self, x, y, dest, dest_id):
        self.warps.append({"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dest_id)})

    def trigger(self, x, y, var, value, script):
        self.coords.append({"type": "trigger", "x": x, "y": y, "elevation": 0, "var": var,
                            "var_value": str(value), "script": f"{self.name}_EventScript_{script}"})

    def sign(self, x, y, script, facing="ANY"):
        self.bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                         "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{facing}",
                         "script": f"{self.name}_EventScript_{script}"})

    def hidden(self, item, x, y, flag):
        self.bgs.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
                         "quantity": 1, "underfoot": False})

    # -- output ---------------------------------------------------------------------------
    def blockdata(self, ids=None):
        ids = ids or self.ids
        out = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                out[y, x] = ids[y][x] | (int(self.solid[y][x]) << 10) | (3 << 12)
        return out

    def write(self, tileset_symbol, music):
        lay_dir = ROOT / "data/layouts" / self.name
        lay_dir.mkdir(parents=True, exist_ok=True)
        self.blockdata().astype("<u2").tofile(lay_dir / "map.bin")
        np.array(self.border, np.uint16).astype("<u2").tofile(lay_dir / "border.bin")
        path = ROOT / "data/layouts/layouts.json"
        data = json.loads(path.read_text())
        for lay in data["layouts"]:
            if lay.get("id") == self.layout_id:
                lay["width"], lay["height"] = self.w, self.h
                lay["primary_tileset"], lay["secondary_tileset"] = "gTileset_Oikos", tileset_symbol
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        mpath = ROOT / "data/maps" / self.name / "map.json"
        m = json.loads(mpath.read_text())
        m.update({"music": music, "requires_flash": True, "map_type": "MAP_TYPE_UNDERGROUND",
                  "allow_cycling": False, "allow_escaping": True, "allow_running": True,
                  "show_map_name": False, "region_map_section": "MAPSEC_ELEUSA_VILLAGE",
                  "weather": "WEATHER_NONE", "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
                  "connections": None, "ichor_kind": "dungeon"})
        m["object_events"], m["warp_events"] = self.objects, self.warps
        m["coord_events"], m["bg_events"] = self.coords, self.bgs
        mpath.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
        return m


# ===========================================================================================
# B1F, the granaries (SCRIPT.md beat 23A; Part 5: "Teach")
# ===========================================================================================

B1F_W, B1F_H = 36, 28
B1F_ROWS = [
    "####################################",  # 0
    "####################################",  # 1
    "####################################",  # 2   the stairs cut up through the faces
    "####################################",  # 3
    "##.........##...#...#...##........##",  # 4   the stair hall | bays A B C | the Ploutonion landing
    "##.........##...#...#...##........##",  # 5
    "##.........##...#...#...##........##",  # 6
    "##.........##...#...#...##........##",  # 7
    "##................................##",  # 8   the upper gallery
    "##................................##",  # 9
    "##......####################......##",  # 10  the west and east galleries round the core
    "##~~....####################....~~##",  # 11
    "##~~....#..~~..#####..~~...#....~~##",  # 12  Bolos's side pit | the sealed granary
    "##.........~~..#####..~~..........##",  # 13
    "##.............#####............~~##",  # 14
    "##~~....####################....~~##",  # 15
    "##~~....####################......##",  # 16
    "##................................##",  # 17  the lower gallery
    "##................................##",  # 18
    "##................................##",  # 19
    "##.......................####.######",  # 20  the pit field | the narrow way down
    "##..~~~..~~..~~..~~..~~..####.######",  # 21
    "##..~~~..~~..~~..~~..~~..#.......###",  # 22  | the apse and the steps down
    "##.....~~......~~........#.......###",  # 23
    "###....~~......~~.......##.......###",  # 24
    "####################################",  # 25
    "####################################",  # 26
    "####################################",  # 27
]
B1F_TELESTERION_STAIR = (5, 2)       # crypt_stair, 2x2: its bottom row is the warp
B1F_PLOUTONION_STAIR = (29, 2)
B1F_HOLE = (31, 23)                  # the steps down to the Hall of the Kore
B1F_COLUMNS = [(4, 4), (7, 4)]       # oikos Doric columns, 1x3, flanking the Anaktoron's stair
B1F_BRAZIERS = [(9, 5), (21, 4), (26, 5), (26, 22)]   # top-left of each 2x2; flags +0x18..0x1B
B1F_PITHOI = [(2, 4), (3, 4), (13, 4), (14, 4), (15, 4), (17, 6), (23, 4), (32, 4), (33, 4),
              (2, 13), (26, 12), (33, 18), (11, 17), (17, 17), (23, 17), (2, 22), (32, 22)]
B1F_AMPHORAE = [(3, 6), (31, 4), (28, 10), (7, 16), (24, 21), (14, 12), (20, 12)]
B1F_DIG = (17, 5)                    # the Persephone sherd, behind the great jar in bay B


def build_b1f(d):
    f = Floor("EleusaSanctum_B1F", "MAP_ELEUSA_SANCTUM_B1F", "LAYOUT_ELEUSA_SANCTUM_B1F", B1F_W, B1F_H, d, "rock")
    check_rows("B1F", B1F_ROWS, B1F_W, B1F_H)
    f.autotile(B1F_ROWS)
    f.border = [kit.kit_id(CD_CAT, "T|...", "crypt")] * 4
    f.piece("crypt_stair", *B1F_TELESTERION_STAIR)
    f.piece("crypt_stair", *B1F_PLOUTONION_STAIR)
    for (x, y) in B1F_COLUMNS:
        f.piece("column3", x, y)
    for n, (x, y) in enumerate(B1F_BRAZIERS):
        f.piece("brazier_cold", x, y, label="EleusaSanctumRock_BrazierCold")
    for (x, y) in B1F_PITHOI:
        f.piece("pithos", x, y)
    for (x, y) in B1F_AMPHORAE:
        f.piece("amphora", x, y)
    f.piece("dig_crypt", *B1F_DIG)
    f.piece("hole_down", *B1F_HOLE)
    # the lit braziers, for the scripts' swaps (composed now so their ids are fixed)
    for (x, y) in B1F_BRAZIERS[:1]:
        lit = Floor("lit", "", "", B1F_W, B1F_H, d, "rock")
        lit.ids = [r[:] for r in f.ids]
        lit.ids[y][x] = lit.ids[y][x + 1] = lit.ids[y + 1][x] = lit.ids[y + 1][x + 1] = CRYPT_FLOOR
        lit.piece("brazier_lit", x, y, label="EleusaSanctumRock_BrazierLit")
    b1f_events(f)
    return f


GFX = "OBJ_EVENT_GFX_ICHOR_"
B1F_ZONES = [(2, 3, 10, 7), (13, 4, 23, 9), (26, 3, 33, 16), (26, 22, 32, 24)]   # each brazier's stretch
B1F_FADE_TRIGGERS = [(x, 10) for x in range(2, 8)] + [(14, 8), (14, 9)]   # out of sight of Alethea's fight


def b1f_events(f):
    S = "FLAG_ICHOR_HIDE_HYPERION_SANCTUM"      # the grunts are gone once the theft is over
    f.person("CHLOE", GFX + "PRIESTESS", 6, 3, "DOWN", "Chloe", "FLAG_ICHOR_GOT_DEMETERS_SICKLE")
    f.person("ALETHEA", GFX + "ALETHEA", 6, 4, "DOWN", "Alethea", "FLAG_ICHOR_SANCTUM_ARRIVED")
    f.person("LAMP_GRUNT", GFX + "TITAN_GRUNT", 6, 9, "UP", "LampGrunt", "FLAG_ICHOR_SANCTUM_ARRIVED")
    f.person("KROKALOS", GFX + "TITAN_GRUNT", 28, 22, "RIGHT", "Krokalos", S, "TRAINER_TYPE_NORMAL", 3)
    f.person("BOLOS", GFX + "TITAN_GRUNT", 9, 13, "LEFT", "Bolos", S, "TRAINER_TYPE_NORMAL", 3)
    f.item("ITEM_HYPER_POTION", 14, 14, "FLAG_ICHOR_ITEM_SANCTUM_B1F_HYPER_POTION")
    f.hidden("ITEM_MIRACLE_SEED", 20, 14, "FLAG_ICHOR_HIDDEN_SANCTUM_B1F_MIRACLE_SEED")
    tx, ty = B1F_TELESTERION_STAIR
    px, py = B1F_PLOUTONION_STAIR
    f.warp(tx, ty + 1, "MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER", 3)      # 0: the Anaktoron's stair
    f.warp(tx + 1, ty + 1, "MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER", 3)  # 1
    f.warp(px, py + 1, "MAP_ELEUSA_VILLAGE", 9)                         # 2: the Ploutonion's stair
    f.warp(px + 1, py + 1, "MAP_ELEUSA_VILLAGE", 10)                    # 3
    f.warp(*B1F_HOLE, "MAP_ELEUSA_SANCTUM_B2F", 0)                      # 4: down to the Hall of the Kore
    for n, (x, y) in enumerate(B1F_BRAZIERS):      # read from below or beside its legs
        for dx in (0, 1):
            f.sign(x + dx, y + 1, f"Brazier{n}")
    f.sign(*B1F_DIG, "DigSpot")
    zone_triggers(f, B1F_ZONES)
    for (x, y) in B1F_FADE_TRIGGERS:
        f.trigger(x, y, "VAR_TEMP_B", 1, "AletheaOutOfSight")


def zone_of(zones, x, y):
    for n, (x0, y0, x1, y1) in enumerate(zones):
        if x0 <= x <= x1 and y0 <= y <= y1:
            return n
    return None


def zone_triggers(f, zones):
    """Lit zones (ENGINE_API.md §2): an enter trigger on each zone cell that borders
    open ground outside it, a leave trigger on each outside cell that borders a zone.
    VAR_TEMP_8 is 1 while the player stands in a lit zone."""
    taken = {(c["x"], c["y"]) for c in f.coords}

    def open_(x, y):
        return 0 <= x < f.w and 0 <= y < f.h and not f.solid[y][x] and not f.kind[y][x].startswith("crypt_stair")
    leave = set()
    for y in range(f.h):
        for x in range(f.w):
            z = zone_of(zones, x, y)
            if z is None or not open_(x, y):
                continue
            outside = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                       if open_(x + dx, y + dy) and zone_of(zones, x + dx, y + dy) != z]
            if outside and (x, y) not in taken:
                f.trigger(x, y, "VAR_TEMP_8", 0, f"EnterZone{z}")
            for p in outside:
                if zone_of(zones, *p) is None:
                    leave.add(p)
    for (x, y) in sorted(leave, key=lambda p: (p[1], p[0])):
        if (x, y) not in taken:
            f.trigger(x, y, "VAR_TEMP_8", 1, "LeaveLitZone")


# ===========================================================================================
# B2F, the Hall of the Kore (beat 23B; Part 5: "Test")
# ===========================================================================================

B2F_W, B2F_H = 20, 40
# '<' '>' corners, 'T' wall top, 'F' frieze, 'L' lower wall, '[' ']' side walls, 'v' the chasm,
# 'p' a grain pit (walkable: it drops you), 'c' Hecate's chalk (the safe way), '=' a bridge
# over the chasm, 'P' the partition (its doorway placed below), '.' flagstones, 'x' void.
B2F_ROWS = [
    "<TTTTTTTTTTTTTTTTTT>",  # 0   the north wall: the fourth panel over the stair down
    "[FFFFFFFFFFFFFFFFFF]",  # 1
    "[LLLLLLLLLLLLLLLLLL]",  # 2
    "[..................]",  # 3   the far end: the stair down, the sentinels
    "[..................]",  # 4
    "[..................]",  # 5
    "[........vvPPPPPPPP]",  # 6   Konis's doorway in the low wall
    "[........vv........]",  # 7   west: Gaios's fresco alcove
    "[........vv........]",  # 8
    "[........vv........]",  # 9
    "[........vv........]",  # 10
    "[........vv........]",  # 11
    "[........vv........]",  # 12
    "[TTTTTTTTvv........]",  # 13  the third panel (west)
    "[FFFFFFFFvv........]",  # 14
    "[LLLLLLLLvv........]",  # 15
    "[........vv........]",  # 16
    "[........==........]",  # 17  the far bridge
    "[........vv........]",  # 18
    "[........vv........]",  # 19  west: the iron-tasting spring
    "[........vvTTTTTTTT]",  # 20  the second panel (east)
    "[........vvFFFFFFFF]",  # 21
    "[........vvLLLLLLLL]",  # 22
    "[........==........]",  # 23  the near bridge
    "[ppppppppvvccpppppp]",  # 24  the near half: grain pits, and the chalk across them (east)
    "[ppppppppvvpcpppppp]",  # 25
    "[ppppppppvvpccccppp]",  # 26
    "[ppppppppvvppppcppp]",  # 27
    "[ppppppppvvpppccppp]",  # 28
    "[ppppppppvvpppcpppp]",  # 29
    "[ppppppppvvpcccpppp]",  # 30
    "[TTTTTTTTvv.c......]",  # 31  the first panel (west)
    "[FFFFFFFFvv.c......]",  # 32
    "[LLLLLLLLvv.c......]",  # 33
    "[..................]",  # 34  the court at the stair's foot
    "[..................]",  # 35
    "[..................]",  # 36
    "[..................]",  # 37
    "[..................]",  # 38
    "xxxxxxxxxSSxxxxxxxxx",  # 39  the stair up to the granaries
]
B2F_PANELS = {   # row of a frieze -> {x: frieze piece}; the rest of the row is bands
    1: {14: "hermes", 15: "return"},
    14: {3: "search", 4: "hecate"},
    21: {15: "seized"},
    32: {3: "maiden", 4: "horses"},
}
# where each panel is read from (the lower wall under it), south to north
B2F_FRESCOES = [(32, (3, 4)), (21, (14, 15, 16)), (14, (3, 4)), (1, (14, 15))]
B2F_DOOR = (13, 6)             # Konis's doorway through the low wall
B2F_STAIR_DOWN = [(9, 3), (10, 3)]
B2F_SENTINELS = [(8, 3), (11, 3)]
B2F_BASIN = (2, 19)            # 2x1, the spring
B2F_COLUMNS = [(1, 9), (7, 9), (12, 9), (17, 9), (12, 14), (17, 14), (1, 35), (18, 35)]   # 1x2
B2F_SCONCES = [(2, 2), (6, 2), (12, 2), (17, 2), (6, 15), (17, 22), (6, 33)]
B2F_LAMPS = [(14, 4), (5, 10), (16, 36)]     # the grunts' lamps, and one left on the court's flags
B2F_THINGS = [("vessels.kistai", 1, 4), ("vessels.liknon", 7, 4), ("vessels.kernos", 1, 12),
              ("vessels.kiste_smashed", 3, 37), ("overturned.r0c0", 13, 38), ("overturned.r0c1", 14, 38),
              ("vessels.kylikes", 18, 16), ("vessels.kykeon", 11, 19)]
B2F_BOOTS = [(10, 38), (10, 37), (11, 36), (11, 35), (12, 34)]   # the Titans' bootprints from the stair


def hall_set():
    d = Derived("gTileset_EleusaSanctumHall", TD_DIR, "EleusaSanctumHall")
    # cave behaviour on the hall's flagstones: the deeper table's encounters
    for key, mid in TD.items():
        if TD_WALK[key] == "." and (key.startswith("floor.") or key.startswith("glow.")) \
                and key not in ("floor.void", "floor.rubble", "floor.floor_inlay"):
            d.at[mid - SECONDARY] = (d.at[mid - SECONDARY] & 0xFF00) | MB_CAVE
    return d


def build_b2f(d):
    f = Floor("EleusaSanctum_B2F", "MAP_ELEUSA_SANCTUM_B2F", "LAYOUT_ELEUSA_SANCTUM_B2F", B2F_W, B2F_H, d, "hall")
    rows = B2F_ROWS
    check_rows("B2F", rows, B2F_W, B2F_H)
    f.border = [TD["floor.void"]] * 4
    plain = ("floor.floor", "floor.floor_b", "floor.floor_c", "floor.floor_cracked")
    chalk = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "c"]
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == "<":
                f.set(x, y, TD["wall.corner_l"], True, "wall")
            elif c == ">":
                f.set(x, y, TD["wall.corner_r"], True, "wall")
            elif c == "T":
                f.set(x, y, TD["wall.top"], True, "wall")
            elif c == "F":
                piece = B2F_PANELS.get(y, {}).get(x) or ("key" if x % 4 == 0 else "wheat")
                f.set(x, y, TD["frieze." + piece], True, "panel" if x in B2F_PANELS.get(y, {}) else "wall")
            elif c == "L":
                f.set(x, y, TD["wall.lower"], True, "wall")
            elif c == "[":
                f.set(x, y, TD["wall.side_l"], True, "wall")
            elif c == "]":
                f.set(x, y, TD["wall.side_r"], True, "wall")
            elif c in "vx":
                f.set(x, y, TD["floor.void"], True, "chasm" if c == "v" else "void")
            elif c == "p":
                f.set(x, y, TD["floor.void"], False, "pit")
            elif c == "c":
                k = chalk.index((x, y))
                prev = chalk[k - 1] if k else None
                f.set(x, y, TD["floor.bootprints"] if k % 2 else TD["floor.chalk_fork"], False, "chalk")
            elif c == "=":
                f.set(x, y, TD["floor.floor_cracked"], False, "bridge")
            elif c == "P":
                end = "W" if x == 11 else "E" if x == 18 else "M"
                f.set(x, y, TD["partition." + end], True, "wall")
            elif c == "S":
                f.set(x, y, TD["stairs.up_L" if x == 9 else "stairs.up_R"], False, "stair")
            else:
                n = noise(x, y, 3)
                name = "floor.floor_b" if n < 14 else "floor.floor_c" if n < 22 else \
                    "floor.floor_cracked" if n < 25 else "floor.floor"
                f.set(x, y, TD[name], False, "floor")
    f.set(*B2F_DOOR, TD["partition.door_draught"], False, "door")
    for (x, y) in B2F_STAIR_DOWN:
        f.set(x, y, TD["stairs.crypt"], False, "stair")
    for (x, y) in B2F_SENTINELS:
        f.set(x, y, TD["sentinel.r0c0"], True, "sentinel")
        f.set(x, y + 1, TD["sentinel.r1c0"], True, "sentinel")
    for (x, y) in B2F_COLUMNS:
        f.set(x, y, TD["columns.top"], True, "column")
        f.set(x, y + 1, TD["columns.bottom" if noise(x, y) < 60 else "columns.bottom_b"], True, "column")
    for (x, y) in B2F_SCONCES:
        f.set(x, y, TD["wall_lights.sconce_lit"], True, "wall")
    for (x, y) in B2F_LAMPS:
        f.set(x, y, TD["vessels.lamp_lit"], True, "lamp")
    for key, x, y in B2F_THINGS:
        f.set(x, y, TD[key], True, "thing")
    for (x, y) in B2F_BOOTS:
        f.set(x, y, TD["floor.bootprints"], False, "floor")
    bx, by = B2F_BASIN
    for i, obj in enumerate(OIKOS["basin"][0]):
        mid = d.over(f"basin{i}", TD["floor.floor"], obj, label=f"EleusaSanctumHall_Basin_{i}")
        f.set(bx + i, by, mid, True, "basin")
    hall_holes(f)
    b2f_events(f)
    return f


B2F_FALL_TO = (12, 34)          # a pit drops you back in the court, at the chalk's first mark
B2F_VOICE_ROW = 36              # the hall's head: Hyperion's voice comes up from the far stair


def b2f_events(f):
    S = "FLAG_ICHOR_HIDE_HYPERION_SANCTUM"
    f.person("KONIS", GFX + "TITAN_GRUNT", 14, 5, "LEFT", "Konis", S, "TRAINER_TYPE_NORMAL", 3)
    f.person("GAIOS", GFX + "TITAN_GRUNT", 4, 10, "UP", "Gaios", S, "TRAINER_TYPE_NORMAL", 3)
    f.item("ITEM_TM28", 2, 12, "FLAG_ICHOR_ITEM_SANCTUM_B2F_TM_DIG")
    f.item("ITEM_SUPER_POTION", 18, 23, "FLAG_ICHOR_ITEM_SANCTUM_B2F_SUPER_POTION")
    f.hidden("ITEM_ETHER", 4, 19, "FLAG_ICHOR_HIDDEN_SANCTUM_B2F_ETHER")
    f.warp(9, 39, "MAP_ELEUSA_SANCTUM_B1F", 4)       # 0: up to the granaries
    f.warp(10, 39, "MAP_ELEUSA_SANCTUM_B1F", 4)      # 1
    f.warp(9, 3, "MAP_ELEUSA_SANCTUM_B3F", 0)        # 2: down to the deepest granary
    f.warp(10, 3, "MAP_ELEUSA_SANCTUM_B3F", 1)       # 3
    for n, (row, xs) in enumerate(B2F_FRESCOES):
        for x in xs:
            f.sign(x, row + 1, f"Fresco{n + 1}", "NORTH")
    bx, by = B2F_BASIN
    f.sign(bx, by, "Spring")
    f.sign(bx + 1, by, "Spring")
    for x in range(1, 19):
        if not f.solid[B2F_VOICE_ROW][x]:
            f.trigger(x, B2F_VOICE_ROW, "VAR_TEMP_A", 0, "Voice")
    for y in range(f.h):
        for x in range(f.w):
            if f.kind[y][x] == "pit":
                f.trigger(x, y, "VAR_TEMP_9", 0, "Pit")


# The hall's holes: grain pits and the chasm, rimmed where they meet the floor. Each is
# composed quadrant by quadrant from the hall's own 8x8 tiles: the wall top's lit lip
# (flipped for a far edge), the side walls' rims, and the void; the chasm's bottom is the
# hall's flagstones in the fire palette, glowing faintly red far below.
def hall_holes(f):
    d = f.d
    tile = lambda key, k: d.entries(TD[key])[k]          # noqa: E731
    void = tile("floor.void", 0)
    lip = (tile("wall.top", 2), tile("wall.top", 3))     # lip along the tile's bottom edge
    rim_w = tile("wall.side_r", 0)                       # a rim on the tile's left edge
    rim_e = tile("wall.side_l", 1)                       # a rim on the tile's right edge
    ember = [(e & 0x0FFF) | (7 << 12) for e in d.entries(TD["floor.floor_cracked"])[:4]]
    vflip = lambda e: e ^ (1 << 11)                       # noqa: E731
    holes = ("pit", "chasm")
    edge = ("floor", "chalk", "bridge", "door", "stair")

    def at(x, y):
        return f.kind[y][x] if 0 <= x < f.w and 0 <= y < f.h else ""
    for y in range(f.h):
        for x in range(f.w):
            k = at(x, y)
            if k not in holes:
                continue
            n, s, w, e = (at(x, y - 1) in edge, at(x, y + 1) in edge, at(x - 1, y) in edge, at(x + 1, y) in edge)
            glow = k == "chasm" and not (n or s) and noise(x, y, 5) < 45
            inner = ember if glow else [void] * 4
            q = [vflip(lip[0]) if n else rim_w if w else inner[0],
                 vflip(lip[1]) if n else rim_e if e else inner[1],
                 lip[0] if s else rim_w if w else inner[2],
                 lip[1] if s else rim_e if e else inner[3]]
            key = f"{k}:{'N' * n}{'S' * s}{'W' * w}{'E' * e}{'g' * glow}"
            mid = d.add(key, q + [0, 0, 0, 0], MB_NORMAL, LAYER_COVERED)
            f.set(x, y, mid, f.solid[y][x], k)


# ===========================================================================================
# B3F, the deepest granary (beat 23C; Part 5: "Payoff")
# ===========================================================================================

B3F_W, B3F_H = 18, 18
B3F_ROWS = [
    "##################",  # 0
    "##################",  # 1
    "##################",  # 2   the stair up cuts through the face
    "##################",  # 3
    "######......######",  # 4   the landing at the stair's foot
    "####..........####",  # 5   the scene's line, five steps from the chest
    "###............###",  # 6
    "##..............##",  # 7
    "##..............##",  # 8
    "#..............###",  # 9
    "#.................",  # 10  the Titans' tunnel, east through the wall
    "#.................",  # 11
    "##.............###",  # 12
    "##..............##",  # 13
    "###............###",  # 14
    "####..........####",  # 15
    "######......######",  # 16
    "##################",  # 17
]
B3F_STAIR = (8, 2)              # crypt_stair: warps at (8,3), (9,3)
B3F_CHEST = (7, 10)             # the sarcophagus stands in for the great bronze chest (3x2)
B3F_TUNNEL_X = 15               # natural rock from here east: the tunnel the Titans dug
B3F_TUNNEL = [(x, y) for x in range(15, 18) for y in (10, 11)]
B3F_LINE = [(x, 5) for x in range(4, 14)]   # the scene's coord triggers
B3F_SICKLE = (6, 4)             # thrown aside in the dust by the stair's foot (solid: a heap of spoil)
B3F_DIG = (14, 12)              # Daedalus's page II, where the tunnel bared the old foundations
B3F_PITHOI = [(3, 7), (13, 7), (2, 12)]
B3F_AMPHORAE = [(5, 6), (12, 6), (3, 12)]
B3F_SPOIL = [(14, 8), (12, 13)]             # spoil heaps from the Titans' dig
B3F_PITS = [(4, 14), (11, 14)]              # the oldest granary's own pits (2x2)


def b3f_rows():
    rows = [list(r) for r in B3F_ROWS]
    for (x, y) in B3F_PITS:
        for dx in (0, 1):
            for dy in (0, 1):
                rows[y + dy][x + dx] = "~"
    return ["".join(r) for r in rows]


def build_b3f(d):
    f = Floor("EleusaSanctum_B3F", "MAP_ELEUSA_SANCTUM_B3F", "LAYOUT_ELEUSA_SANCTUM_B3F", B3F_W, B3F_H, d, "rock")
    rows = b3f_rows()
    check_rows("B3F", rows, B3F_W, B3F_H)
    f.autotile(rows, "crypt")
    # the tunnel: the Titans' rough dig through living rock, beyond the vault's wall
    near = {(x + dx, y + dy) for (x, y) in B3F_TUNNEL for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    f.autotile(rows, None, region=lambda x, y: (x, y) in near and x >= B3F_TUNNEL_X)
    f.border = [kit.kit_id(CD_CAT, "T|...", "crypt")] * 4
    f.piece("crypt_stair", *B3F_STAIR)
    f.piece("sarcophagus", *B3F_CHEST)
    for (x, y) in B3F_PITHOI:
        f.piece("pithos", x, y)
    for (x, y) in B3F_AMPHORAE:
        f.piece("amphora", x, y)
    f.piece("rock_pile", *B3F_SICKLE)
    for (x, y) in B3F_SPOIL:
        f.piece("rock_pile" if (x + y) % 2 else "boulder", x, y)
    # the collapse's rubble (cave pieces on the tunnel's cave floor: no composing), and the
    # dig the cave-in bares among the old foundations
    f.collapsed = [(x, y, CD_PIECE["rock_pile" if (x + y) % 3 == 1 else "boulder"]["ids"][0][0])
                   for (x, y) in B3F_TUNNEL]
    d.labels["EleusaSanctumRock_Boulder"] = CD_PIECE["boulder"]["ids"][0][0]
    d.labels["EleusaSanctumRock_RockPile"] = CD_PIECE["rock_pile"]["ids"][0][0]
    d.labels["EleusaSanctumRock_DigCrypt"] = CD_PIECE["dig_crypt"]["ids"][0][0]
    b3f_events(f)
    return f


def b3f_collapsed(f):
    """The ids once the tunnel has caved in (Hyperion's Pebblith, beat 23C)."""
    ids = [row[:] for row in f.ids]
    for (x, y, mid) in f.collapsed:
        ids[y][x] = mid
    return ids


def b3f_events(f):
    H = "FLAG_ICHOR_HIDE_HYPERION_SANCTUM"
    f.person("HYPERION", GFX + "KEDALION", 11, 10, "LEFT", "Hyperion", H)    # ICHOR_STUB_ART: his walker
    f.person("PETROS", GFX + "TITAN_GRUNT", 7, 9, "DOWN", "Crew", "FLAG_ICHOR_FRAGMENT_STOLEN")
    f.person("AMATHOS", GFX + "TITAN_GRUNT", 9, 9, "DOWN", "Crew", "FLAG_ICHOR_FRAGMENT_STOLEN")
    f.person("KAPNUB_W", "OBJ_EVENT_GFX_SPECIES(KAPNUB)", 4, 9, "DOWN", "Kapnub", H)
    f.person("KAPNUB_E", "OBJ_EVENT_GFX_SPECIES(KAPNUB)", 12, 12, "DOWN", "Kapnub", H)
    f.person("CHLOE_B3F", GFX + "PRIESTESS", 8, 3, "DOWN", "Nobody", "FLAG_TEMP_1")
    f.person("ALETHEA_B3F", GFX + "ALETHEA", 9, 3, "DOWN", "Nobody", "FLAG_TEMP_2")
    f.item("ITEM_SOFT_SAND", 14, 9, "FLAG_ICHOR_ITEM_SANCTUM_B3F_SOFT_SAND")
    f.hidden("ITEM_RELIC_COPPER", 2, 10, "FLAG_ICHOR_HIDDEN_SANCTUM_B3F_BRONZE_OBOL")
    sx, sy = B3F_STAIR
    f.warp(sx, sy + 1, "MAP_ELEUSA_SANCTUM_B2F", 2)          # 0: up to the Hall of the Kore
    f.warp(sx + 1, sy + 1, "MAP_ELEUSA_SANCTUM_B2F", 3)      # 1
    f.sign(*B3F_SICKLE, "Sickle")
    for (x, y) in B3F_TUNNEL[:2]:
        f.sign(x, y, "Tunnel")
    f.sign(*B3F_DIG, "DigSpot")
    for (x, y) in B3F_LINE:
        f.trigger(x, y, "VAR_TEMP_A", 0, "Theft")


# ===========================================================================================
# Generated scripts and labels
# ===========================================================================================

SCRIPT_BEGIN = "// --- Generated by tools/ichor/maps/sanctum.py from the layout. Do not edit. ---"
SCRIPT_END = "// --- End of the generated block. ---"
BRAZIER_FLAG = "FLAG_ICHOR_BRAZIERS_START + 0x{:02X}"
B1F_BRAZIER_BASE = 0x18


def b1f_script(f):
    px = "EleusaSanctum_B1F_EventScript_"
    o = [SCRIPT_BEGIN, "",
         "// The four braziers (FLAG_ICHOR_BRAZIERS_START + 0x18..0x1B), each lighting its stretch",
         "// of the granaries: a lit zone (ENGINE_API.md §2). VAR_TEMP_8 is 1 while the player",
         "// stands in a lit zone."]
    o.append(f"script {px}DrawBraziers {{")
    for n in range(len(B1F_BRAZIERS)):
        o += [f"    if (flag({BRAZIER_FLAG.format(B1F_BRAZIER_BASE + n)})) {{", f"        call({px}Light{n})", "    }"]
    o += ["    return", "}"]
    for n, (x, y) in enumerate(B1F_BRAZIERS):
        o += ["", f"script {px}Light{n} {{"]
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            o.append(f"    setmetatile({x + dx}, {y + dy}, METATILE_EleusaSanctumRock_BrazierLit_{dx}{dy}, TRUE)")
        o += ["    return", "}"]
        o += ["", f"script {px}Brazier{n} {{",
              f"    setvar(VAR_0x8004, {BRAZIER_FLAG.format(B1F_BRAZIER_BASE + n)})",
              "    setvar(VAR_0x8005, TRUE)      // the brazier stands in its own stretch",
              "    call(EventScript_IchorBrazier)",
              "    if (var(VAR_RESULT) == TRUE) {",
              f"        call({px}Light{n})",
              "        special(DrawWholeMapView)",
              "        setvar(VAR_TEMP_8, 1)",
              "    }",
              "    releaseall",
              "}"]
        # (a trigger's script locks and releases: releaseall clears the player's finished
        # step, or the trigger would fire again on the next frame)
        o += ["", f"script {px}EnterZone{n} {{",
              "    lockall",
              f"    setvar(VAR_0x8004, {BRAZIER_FLAG.format(B1F_BRAZIER_BASE + n)})",
              "    call(EventScript_IchorEnterLitZone)",
              f"    if (flag({BRAZIER_FLAG.format(B1F_BRAZIER_BASE + n)})) {{",
              "        setvar(VAR_TEMP_8, 1)",
              "    }",
              "    releaseall",
              "}"]
    o += ["", f"script {px}LeaveLitZone {{",
          "    lockall",
          "    call(EventScript_IchorLeaveLitZone)",
          "    setvar(VAR_TEMP_8, 0)",
          "    releaseall",
          "}", "",
          "// On arrival in a lit stretch (the stair hall, the Ploutonion's landing, the apse):",
          "// full light at once, as ENGINE_API.md §2 asks of ON_TRANSITION.",
          f"script {px}LightOnArrival {{",
          "    getplayerxy(VAR_TEMP_C, VAR_TEMP_D)"]
    for n, (x0, y0, x1, y1) in enumerate(B1F_ZONES):
        o += [f"    if (flag({BRAZIER_FLAG.format(B1F_BRAZIER_BASE + n)}) && var(VAR_TEMP_C) >= {x0} && "
              f"var(VAR_TEMP_C) <= {x1} && var(VAR_TEMP_D) >= {y0} && var(VAR_TEMP_D) <= {y1}) {{",
              "        setflashlevel(0)",
              "        setvar(VAR_TEMP_8, 1)",
              "    }"]
    o += ["    return", "}", "", SCRIPT_END]
    return "\n".join(o)


def b3f_script(f):
    px = "EleusaSanctum_B3F_EventScript_"
    o = [SCRIPT_BEGIN, "",
         "// The Titans' tunnel, caved in behind Hyperion (beat 23C), and the dig it bared.",
         f"script {px}DrawCollapse {{"]
    names = {CD_PIECE["boulder"]["ids"][0][0]: "Boulder", CD_PIECE["rock_pile"]["ids"][0][0]: "RockPile"}
    for (x, y, mid) in f.collapsed:
        o.append(f"    setmetatile({x}, {y}, METATILE_EleusaSanctumRock_{names[mid]}, TRUE)")
    o.append(f"    setmetatile({B3F_DIG[0]}, {B3F_DIG[1]}, METATILE_EleusaSanctumRock_DigCrypt, FALSE)")
    o += ["    return", "}", "", SCRIPT_END]
    return "\n".join(o)


def splice(name, block):
    path = ROOT / "data/maps" / name / "scripts.pory"
    text = path.read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"sanctum: {path} needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    new = text[:a] + block + text[b + len(SCRIPT_END):]
    if new != text:
        path.write_text(new)


LABELS_BEGIN = "// --- EleusaSanctum: written by tools/ichor/maps/sanctum.py ---"
LABELS_END = "// --- EleusaSanctum: end ---"


def write_labels(*sets):
    lines = [LABELS_BEGIN]
    for d in sets:
        for label, mid in sorted(d.labels.items(), key=lambda kv: (kv[1], kv[0])):
            lines.append(f"#define METATILE_{label:<44} 0x{mid:03X}")
    lines.append(LABELS_END)
    block = "\n".join(lines)
    text = LABELS_H.read_text()
    a, b = text.find(LABELS_BEGIN), text.find(LABELS_END)
    if a >= 0 and b >= 0:
        text = text[:a] + block + text[b + len(LABELS_END):]
    else:
        end = text.rfind("#endif")
        text = text[:end] + block + "\n\n" + text[end:]
    LABELS_H.write_text(text)


# ===========================================================================================
# Checks
# ===========================================================================================

def check(f, m, starts, extra_reach=()):
    """Every open cell reachable from the floor's arrival; people, items and triggers on open
    ground; bg events faceable; warps on stairs or the hole."""
    errors = []
    solid = [row[:] for row in f.solid]
    every = set()
    for s in starts:
        every |= reach(solid, s, f.w, f.h)
    open_cells = {(x, y) for y in range(f.h) for x in range(f.w) if not solid[y][x]}
    stranded = sorted(open_cells - every - set(extra_reach))
    if stranded:
        errors.append(f"{f.name}: open but unreachable: {stranded[:12]}")
    for o in m["object_events"]:
        if solid[o["y"]][o["x"]] and not o.get("flag", "").startswith("FLAG_TEMP"):
            errors.append(f"{f.name}: {o.get('local_id', o['script'])} stands on a solid cell ({o['x']},{o['y']})")
    for b in m["bg_events"]:
        bx, by = b["x"], b["y"]
        if not any((bx + dx, by + dy) in every for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) \
                and (bx, by) not in every:
            errors.append(f"{f.name}: bg event ({bx},{by}) can't be faced")
    for c in m["coord_events"]:
        if solid[c["y"]][c["x"]]:
            errors.append(f"{f.name}: trigger ({c['x']},{c['y']}) on a solid cell")
    cells = [(c["x"], c["y"]) for c in m["coord_events"]]
    if len(set(cells)) != len(cells):
        errors.append(f"{f.name}: two triggers share a cell")
    for w in m["warp_events"]:
        k = f.kind[w["y"]][w["x"]]
        if k not in ("crypt_stair", "hole_down", "stair"):
            errors.append(f"{f.name}: warp ({w['x']},{w['y']}) is on {k}")
    return errors


# ===========================================================================================
# Renders
# ===========================================================================================

GFX_PNG = {"OBJ_EVENT_GFX_ICHOR_PRIESTESS": "people/ichor/priestess.png",
           "OBJ_EVENT_GFX_ICHOR_ALETHEA": "people/ichor/alethea.png",
           "OBJ_EVENT_GFX_ICHOR_TITAN_GRUNT": "people/ichor/titan_grunt.png",
           "OBJ_EVENT_GFX_ICHOR_KEDALION": "people/ichor/kedalion.png",
           "OBJ_EVENT_GFX_ITEM_BALL": "misc/ichor_item_jar.png"}


def renderer(base_symbol, derived_dir):
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    sec = dict(R.resolve_tileset(base_symbol, syms))
    sec["metatiles"] = derived_dir / "metatiles.bin"
    return R, R.Renderer(R.Tileset(R.resolve_tileset("gTileset_Oikos", syms)), R.Tileset(sec))


def sprite(gfx, facing):
    from PIL import Image
    rel = GFX_PNG.get(gfx)
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
        sp = gfx[len("OBJ_EVENT_GFX_SPECIES("):-1].lower()
        stub = {"kapnub": "slugma", "kaminoo": "ponyta"}.get(sp, sp)
        path = ROOT / f"graphics/pokemon/{stub}/overworld.png"
        size = (32, 32)
    elif rel:
        path = ROOT / "graphics/object_events/pics" / rel
        size = (16, 16) if "item" in rel else (16, 32)
    else:
        return None
    if not path.exists():
        return None
    sheet = Image.open(path)
    frame = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}.get(facing, 0)
    if size[0] * (frame + 1) > sheet.width:
        frame = 0
    crop = sheet.crop((frame * size[0], 0, frame * size[0] + size[0], size[1]))
    spr = crop.convert("RGBA")
    if sheet.mode == "P":
        idx, px = crop.load(), spr.load()
        for j in range(size[1]):
            for i in range(size[0]):
                if idx[i, j] == 0:
                    px[i, j] = (0, 0, 0, 0)
    if facing == "RIGHT":
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    return spr


def paste_people(im, objects, hide=()):
    for o in objects:
        if o.get("local_id") in hide:
            continue
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE_" in o["movement_type"] else "DOWN"
        spr = sprite(o["graphics_id"], facing)
        if spr is None:
            continue
        x = o["x"] * 16 + 8 - spr.width // 2
        y = o["y"] * 16 + 16 - spr.height
        im.paste(spr, (x, y), spr)
    return im


def render_floor(f, base_symbol, derived_dir, ids=None):
    R, r = renderer(base_symbol, derived_dir)
    return R.render_blocks(r, f.blockdata(ids).reshape(-1), f.w).convert("RGBA")


def darken(im, player, zones=(), lights=(), radius=56):
    """The torch's radius round the player; lit zones (x0, y0, x1, y1) fully lit; extra
    light pools (x, y, r) round lamps."""
    from PIL import Image
    arr = np.array(im).astype(np.float32)
    H, W = arr.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    px, py = player[0] * 16 + 8, player[1] * 16 + 8
    mask = (xx - px) ** 2 + (yy - py) ** 2 <= radius ** 2
    for (x0, y0, x1, y1) in zones:
        mask |= (xx >= x0 * 16) & (xx < (x1 + 1) * 16) & (yy >= y0 * 16) & (yy < (y1 + 1) * 16)
    for (lx, ly, lr) in lights:
        mask |= (xx - (lx * 16 + 8)) ** 2 + (yy - (ly * 16 + 8)) ** 2 <= lr ** 2
    arr[..., :3][~mask] *= 0.06
    return Image.fromarray(arr.astype(np.uint8))


def scale(im, s=2):
    from PIL import Image
    return im.resize((im.width * s, im.height * s), Image.NEAREST)


def events_overlay(im, f):
    from PIL import Image, ImageDraw
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = im.width // f.w
    for y in range(f.h):
        for x in range(f.w):
            if f.solid[y][x]:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 45))
    for e in f.coords:
        col = (255, 255, 255, 90) if "Leave" in e["script"] else (255, 200, 0, 120) if "Enter" in e["script"] \
            else (40, 120, 255, 150)
        d.rectangle([e["x"] * c + 4, e["y"] * c + 4, e["x"] * c + c - 5, e["y"] * c + c - 5], fill=col)
    for b in f.bgs:
        col = (255, 120, 220, 255) if b["type"] == "hidden_item" else (80, 160, 255, 255)
        d.rectangle([b["x"] * c + 2, b["y"] * c + 2, b["x"] * c + c - 3, b["y"] * c + c - 3], outline=col, width=2)
    for w in f.warps:
        d.rectangle([w["x"] * c + 6, w["y"] * c + 6, w["x"] * c + c - 7, w["y"] * c + c - 7],
                    outline=(0, 255, 255, 255), width=3)
    for o in f.objects:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5],
                  outline=(40, 255, 90, 255), width=3)
    return Image.alpha_composite(im.convert("RGBA"), ov)


def b1f_lit_ids(f, which):
    ids = [row[:] for row in f.ids]
    lit = {k: v for k, v in f.d.labels.items() if k.startswith("EleusaSanctumRock_BrazierLit_")}
    for n in which:
        x, y = B1F_BRAZIERS[n]
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            ids[y + dy][x + dx] = lit[f"EleusaSanctumRock_BrazierLit_{dx}{dy}"]
    return ids


def label(im, text):
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 8 * len(text) + 10, 18], fill=(0, 0, 0))
    d.text((5, 4), text, fill=(240, 220, 170))
    return im


def render_all(out, b1, b2, b3):
    """The review images: each floor as first found (with its people), lit or after
    the story, in the dark as the Torch shows it, and its events; then a gallery."""
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    hide_first = {"LOCALID_SANCTUM_CHLOE_B3F", "LOCALID_SANCTUM_ALETHEA_B3F"}
    shown = {}
    # B1F
    cold = render_floor(b1, "gTileset_CaveDark", ROCK_DIR)
    lit = render_floor(b1, "gTileset_CaveDark", ROCK_DIR, b1f_lit_ids(b1, range(4)))
    first = scale(paste_people(cold.copy(), b1.objects)).convert("RGB")
    first.save(out / "sanctum_b1f.png")
    scale(paste_people(lit.copy(), b1.objects)).convert("RGB").save(out / "sanctum_b1f_lit.png")
    one = render_floor(b1, "gTileset_CaveDark", ROCK_DIR, b1f_lit_ids(b1, [0]))
    scale(darken(paste_people(one, b1.objects), (5, 9), zones=[B1F_ZONES[0]])).convert("RGB") \
        .save(out / "sanctum_b1f_dark.png")
    events_overlay(scale(cold), b1).convert("RGB").save(out / "sanctum_b1f_events.png")
    shown["B1F, the granaries"] = scale(paste_people(lit.copy(), b1.objects), 1)
    # B2F
    hall = render_floor(b2, "gTileset_TempleDemeter", HALL_DIR)
    scale(paste_people(hall.copy(), b2.objects)).convert("RGB").save(out / "sanctum_b2f.png")
    scale(darken(paste_people(hall.copy(), b2.objects), (3, 21))).convert("RGB").save(out / "sanctum_b2f_dark.png")
    events_overlay(scale(hall), b2).convert("RGB").save(out / "sanctum_b2f_events.png")
    shown["B2F, the Hall of the Kore"] = paste_people(hall.copy(), b2.objects)
    # B3F
    vault = render_floor(b3, "gTileset_CaveDark", ROCK_DIR)
    after = render_floor(b3, "gTileset_CaveDark", ROCK_DIR, b3f_collapsed(b3))
    people = [o for o in b3.objects if o.get("local_id") not in hide_first]
    scale(paste_people(vault.copy(), people)).convert("RGB").save(out / "sanctum_b3f.png")
    stayed = [o for o in b3.objects if o.get("graphics_id") == "OBJ_EVENT_GFX_ITEM_BALL"]
    scale(paste_people(after.copy(), stayed)).convert("RGB").save(out / "sanctum_b3f_after.png")
    scale(darken(paste_people(vault.copy(), people), (10, 6))).convert("RGB").save(out / "sanctum_b3f_dark.png")
    events_overlay(scale(vault), b3).convert("RGB").save(out / "sanctum_b3f_events.png")
    shown["B3F, the deepest granary"] = paste_people(vault.copy(), people)
    shown["B3F, after the theft"] = paste_people(after.copy(), stayed)
    # the gallery: every floor at 1x, side by side
    ims = [label(im.convert("RGB"), name) for name, im in shown.items()]
    gap = 8
    w = sum(i.width for i in ims) + gap * (len(ims) + 1)
    h = max(i.height for i in ims) + 2 * gap
    sheet = Image.new("RGB", (w, h), (24, 20, 24))
    x = gap
    for im in ims:
        sheet.paste(im, (x, gap))
        x += im.width + gap
    scale(sheet).save(out / "sanctum_gallery.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    args = ap.parse_args()
    rock = Derived("gTileset_EleusaSanctumRock", CD_DIR, "EleusaSanctumRock")
    hall = hall_set()
    b1 = build_b1f(rock)
    b2 = build_b2f(hall)
    b3 = build_b3f(rock)
    rock.write(ROCK_DIR)
    hall.write(HALL_DIR)
    write_labels(rock, hall)
    music = "MUS_ICHOR_TEMPLE_DEMETER"
    m1 = b1.write("gTileset_EleusaSanctumRock", music)
    m2 = b2.write("gTileset_EleusaSanctumHall", music)
    m3 = b3.write("gTileset_EleusaSanctumRock", music)
    splice(b1.name, b1f_script(b1))
    splice(b3.name, b3f_script(b3))
    errors = check(b1, m1, [(5, 4)]) + check(b2, m2, [(9, 38)]) + check(b3, m3, [(8, 4)])
    # B2F: the far half is reached only along the chalk; B3F's tunnel only once it's open
    pits = {(x, y) for y in range(b2.h) for x in range(b2.w) if b2.kind[y][x] == "pit"}
    across = reach(b2.solid, (9, 38), b2.w, b2.h, frozenset(pits))
    if (11, 23) not in across:
        errors.append("B2F: the chalk doesn't cross the pits to the near bridge")
    if args.render:
        render_all(Path(args.render), b1, b2, b3)
    for e in errors:
        print("PROBLEM:", e)
    print(f"sanctum: B1F {B1F_W}x{B1F_H}, B2F {B2F_W}x{B2F_H}, B3F {B3F_W}x{B3F_H}; "
          f"composed metatiles: rock {len(rock.made)}/{LAST_ID + 1 - rock.first}, "
          f"hall {len(hall.made)}/{LAST_ID + 1 - hall.first}; {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
