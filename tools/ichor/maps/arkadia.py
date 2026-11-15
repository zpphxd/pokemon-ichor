#!/usr/bin/env python3
"""Build Arkadia, the Cypress Wood and the Pool of Mnemosyne: layouts, events, checks.

  MAP_ARKADIA               (Arkadia, 50x44, aethos + arkadia): beat 41 and the town
  MAP_ARKADIA_CYPRESS_WOOD  (Arkadia_CypressWood, 36x30, aethos + arkadia_wood): beats 42-43
  MAP_POOL_OF_MNEMOSYNE     (PoolOfMnemosyne, 24x20, aethos + arkadia_wood): the dead end

The ground comes from tools/ichor/maps/arkadia_plan.py; the structures are stamped
from build/arkadia/<set>/catalog.json (make it with tools/ichor/art/arkadia_build.py).
Scripts are data/maps/<Map>/scripts.pory. Renders go to build/render/arkadia/ and,
with --publish, the final 2x renders to design/phase3/img/<Map>.png.

Usage: /usr/bin/python3 tools/ichor/maps/arkadia.py [--render] [--publish] [--no-check]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arkadia_plan as P  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/arkadia"
LAYOUTS = ROOT / "data/layouts/layouts.json"
RENDER = ROOT / "build/render/arkadia"
IMG = ROOT / "design/phase3/img"

# aethos ids (design/phase1/TILES_aethos.md)
GRASS, FLOWERS, SHADE, TALL = 0x001, 0x004, 0x01C, 0x00D
STELE, HERM, BOULDER = 0x003, 0x01B, 0x0E0
PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
         "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
CYP_TOP, CYP_BOT, CYP_TOP_POND = 0x00E, 0x016, 0x02D
PINE = ((0x01E, 0x01F), (0x026, 0x027))
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
FALLS_L, FALLS_R = 0x0BB, 0x0BC
POND = {"TL": 0x0B0, "T": 0x0B1, "TR": 0x0B2, "L": 0x0B8, "R": 0x0BA, "IN": 0x170,
        "FALL_IN": 0x0B9, "FOAM": 0x0C1}

SETS = {"arkadia": ("gTileset_Arkadia", "arkadia"), "wood": ("gTileset_ArkadiaWood", "arkadia_wood")}


def hsh(x, y, salt=0):
    h = (x * 73856093 ^ y * 19349663 ^ salt * 83492791) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h >> 8) % 100


class Catalog:
    def __init__(self, setname):
        p = CAT / SETS[setname][1] / "catalog.json"
        if not p.exists():
            sys.exit(f"{p} is missing: run /usr/bin/python3 tools/ichor/art/arkadia_build.py")
        self.s = {d["key"]: d for d in json.loads(p.read_text())["structures"]}

    def cell(self, key, cx, cy):
        d = self.s[key]
        return d["ids"][cy][cx], d["walk"][cy][cx]

    def named(self, key, name):
        d = self.s[key]
        if name not in d["names"]:
            return None
        cx, cy = d["names"][name]
        return self.cell(key, cx, cy)


class Map:
    def __init__(self, name, folder, layout, plan, setname):
        self.name, self.folder, self.layout = name, folder, layout
        self.plan = plan
        self.w, self.h = plan.w, plan.h
        self.cat = Catalog(setname)
        self.setname = setname
        self.mt = [[None] * self.w for _ in range(self.h)]
        self.walk = [["."] * self.w for _ in range(self.h)]
        self.water = set()
        self.stamped = set()
        self.missing = []

    def ch(self, x, y):
        return self.plan.at(x, y)

    def put(self, x, y, mid, walk="X"):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mt[y][x] = mid
            self.walk[y][x] = walk
            self.stamped.add((x, y))

    def stamp(self, key, x, y, cols=None):
        d = self.cat.s[key]
        for cy in range(d["h"]):
            for cx in range(d["w"]):
                if cols is not None and cx not in cols:
                    continue
                if d["ids"][cy][cx] is None:
                    continue
                mid, wk = self.cat.cell(key, cx, cy)
                self.put(x + (cx - (min(cols) if cols else 0)), y + cy, mid, wk)

    def part(self, key, name, x, y):
        r = self.cat.named(key, name)
        assert r, (key, name)
        self.put(x, y, *r)

    def shape(self, key, blob, x, y):
        r = self.cat.named(key, blob)
        if r is None:
            self.missing.append((self.name, key, blob, x, y))
            r = self.cat.named(key, "1|11111111")
        self.mt[y][x], self.walk[y][x] = r

    def region(self, chars, outside=False):
        return lambda x, y: (outside if not (0 <= x < self.w and 0 <= y < self.h)
                             else self.plan.g[y][x] in chars)

    def blocked(self, x, y):
        return self.walk[y][x] in ("X", "J") or (x, y) in self.water

    def blocks(self):
        b = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                assert m is not None, (self.name, x, y)
                if (x, y) in self.water:
                    b[y, x] = m | (1 << 10) | (1 << 12) if m in (FALLS_L, FALLS_R) else m | (1 << 12)
                elif self.walk[y][x] == "X":
                    b[y, x] = m | (1 << 10)
                else:
                    b[y, x] = m | (3 << 12)
        return b


# --------------------------------------------------------------------------
# Ground
# --------------------------------------------------------------------------

def patch_piece(inside, x, y):
    n, s_, w_, e = inside(x, y - 1), inside(x, y + 1), inside(x - 1, y), inside(x + 1, y)
    v = "T" if not n else ("B" if not s_ else "")
    hz = "L" if not w_ else ("R" if not e else "")
    k = (v + hz) or "C"
    return PATCH.get(k, PATCH["C"])


def aethos_woods(m, chars="A"):
    """Fill the woods: cypress spires above all (Arkadia's), stone pines, a few
    olives, deep-shade grass in the gaps. Everything blocks."""
    A = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and m.plan.g[y][x] in chars and \
        m.mt[y][x] is None
    for y in range(m.h):
        for x in range(m.w):
            if not A(x, y):
                continue
            h = hsh(x, y, 5)
            if h < 18 and A(x + 1, y) and A(x, y + 1) and A(x + 1, y + 1):
                (t, b) = PINE
                m.put(x, y, t[0]); m.put(x + 1, y, t[1])
                m.put(x, y + 1, b[0]); m.put(x + 1, y + 1, b[1])
            elif h < 22 and A(x + 1, y) and A(x, y + 1) and A(x + 1, y + 1):
                m.put(x, y, OLIVE_TOP[0]); m.put(x + 1, y, OLIVE_TOP[1])
                m.put(x, y + 1, OLIVE_BOT[0]); m.put(x + 1, y + 1, OLIVE_BOT[1])
            elif A(x, y + 1) and h < 92:
                m.put(x, y, CYP_TOP)
                m.put(x, y + 1, CYP_BOT)
            else:
                m.put(x, y, SHADE)


def ground(m):
    """Auto-tile the plan's ground characters."""
    path = m.region("=")
    for y in range(m.h):
        for x in range(m.w):
            if m.mt[y][x] is not None:
                continue
            c = m.plan.g[y][x]
            if c == ".":
                m.mt[y][x], m.walk[y][x] = GRASS, "."
            elif c == "=":
                m.mt[y][x], m.walk[y][x] = patch_piece(path, x, y), "."
            elif c == "K":
                key = P.blob_key(m.region("K", outside=m.setname == "wood"), x, y)
                m.shape("canopy_grass" if m.name == "PoolOfMnemosyne" else "canopy", key, x, y)
            elif c == "R":
                m.shape("rock", P.blob_key(m.region("Rf"), x, y), x, y)
            elif c == "f":
                kind = "top" if m.ch(x, y - 1) != "f" else ("foot" if m.ch(x, y + 1) != "f" else "mid")
                side = "W" if m.ch(x - 1, y) not in ("f",) else ("E" if m.ch(x + 1, y) != "f" else "")
                r = m.cat.named("face", kind + side)
                m.mt[y][x], m.walk[y][x] = r
            elif c == ":":
                h = hsh(x, y, 11)
                name = "roots" if h < 7 else ("needles" if h < 15 else "plain")
                m.mt[y][x], m.walk[y][x] = m.cat.named("floor", name)
            elif c == ",":
                m.mt[y][x], m.walk[y][x] = m.cat.named("ferns", "ab"[(x + y) % 2])
            elif c == "s":
                m.mt[y][x], m.walk[y][x] = m.cat.named("floor", "lit2" if hsh(x, y, 3) < 30 else "lit")
            elif c == "v":
                m.mt[y][x], m.walk[y][x] = m.cat.named("asphodel", "ab"[(x + y) % 2])
            elif c in ("A", "~"):
                pass
            else:
                raise ValueError(f"{m.name}: unknown ground {c!r} at {x},{y}")


def decorate(m, rate=6, avoid=()):
    """Red anemones here and there in open grass."""
    for y in range(m.h):
        for x in range(m.w):
            if m.mt[y][x] == GRASS and (x, y) not in m.stamped and (x, y) not in avoid:
                if hsh(x, y, 17) < rate:
                    m.mt[y][x] = FLOWERS


# --------------------------------------------------------------------------
# Arkadia
# --------------------------------------------------------------------------

LAMP_TREES = [(20, 6), (26, 6), (20, 13), (26, 13), (13, 14), (31, 13)]
CYPRESSES = [("cypress_twin", 32, 6), ("cypress_spire", 18, 8), ("cypress_broad", 20, 17),
             ("cypress_old", 11, 23), ("cypress_spire", 11, 27), ("cypress_broad", 38, 13),
             ("cypress_spire", 38, 17)]
SMALL_CYPRESSES = [(16, 36), (18, 36), (22, 36), (25, 36), (27, 36)]
STELES = {"SignForestGate": (22, 7), "SignTemple": (22, 34), "SignWoodGate": (11, 17),
          "SignEastRoad": (39, 22), "SignAlpheios": (8, 35)}
# boulders on the verges where the closed roads are guarded, so nobody walks round
VERGE_STONES = [(43, 22), (43, 25), (5, 35), (5, 38), (12, 40), (15, 40)]

# Arkadia's fixed door warps (BUILD.md), and the Wood's gate
ARKADIA_DOORS = [
    (15, 11, "MAP_ARKADIA_ASCLEPEION"),
    (29, 11, "MAP_ARKADIA_AGORA"),
    (29, 20, "MAP_ARKADIA_NYKTIMOS_HALL"),
    (37, 11, "MAP_ARKADIA_KLYMENE_HOUSE"),
    (11, 21, "MAP_ARKADIA_CHARCOAL_HUT"),
    (38, 29, "MAP_ARKADIA_GOATHERD_HOUSE"),
    (20, 30, "MAP_ARKADIA_TEMPLE_OF_ARTEMIS"),
    (9, 17, "MAP_ARKADIA_CYPRESS_WOOD"),
]
TEMPLE_STAIR_FOOT = [(19, 33), (20, 33), (21, 33)]


def house(m, x, y, w, upper=None, ground_row=None, roof_extra=None):
    """A kit house: two roof rows, an optional upper storey, a ground storey."""
    m.part("house", "ridgeW", x, y)
    for i in range(1, w - 1):
        m.part("house", (roof_extra or {}).get(i, "ridge"), x + i, y)
    m.part("house", "ridgeE", x + w - 1, y)
    m.part("house", "eaveW", x, y + 1)
    for i in range(1, w - 1):
        m.part("house", "eave", x + i, y + 1)
    m.part("house", "eaveE", x + w - 1, y + 1)
    row = y + 2
    if upper:
        for i, n in enumerate(upper):
            m.part("house", n, x + i, row)
        row += 1
    for i, n in enumerate(ground_row):
        m.part("house", n, x + i, row)


def lamp_tree(m, x, y):
    m.stamp("lamptree", x, y)


def arkadia():
    plan = P.arkadia()
    m = Map("Arkadia", "Arkadia", "LAYOUT_ARKADIA", plan, "arkadia")
    # --- structures -----------------------------------------------------
    m.stamp("asclepeion", 13, 8)
    m.part("grotto", "L", 10, 12)
    m.part("grotto", "R", 11, 12)
    m.part("spring", "spout", 12, 12)
    m.part("spring", "basin", 12, 13)
    # the upper terrace's wall, stairs at the doors, the road and the east end
    m.part("terrace", "W", 13, 12)
    for x in range(14, 34):
        m.part("terrace", "stair" if x in (15, 23, 24, 29, 33) else "run", x, 12)
    m.part("terrace", "E", 34, 12)
    for (x, y) in LAMP_TREES:
        lamp_tree(m, x, y)
    for (k, x, y) in CYPRESSES:
        m.stamp(k, x, y)
    m.stamp("agora", 28, 6)
    house(m, 35, 8, 5, upper=["upW", "up", "upRibbon", "up", "upE"],
          ground_row=["wallW", "wallWin", "door", "wallWin", "wallE"])
    m.stamp("woodgate", 8, 14)
    m.stamp("hut", 9, 19)
    m.stamp("kiln", 13, 18)
    m.part("oldwall", "W", 17, 19)
    m.part("oldwall", "E", 18, 19)
    house(m, 26, 18, 7, ground_row=["wallW", "wallWin", "wall", "doorWolf", "wall", "wallWin", "wallE"],
          roof_extra={2: "louvre"})
    # the temple hill
    m.stamp("temple", 18, 25)
    m.stamp("precinct", 17, 29)
    m.stamp("precinct_e", 21, 29, cols=[1, 2, 3])
    m.stamp("stair", 19, 31)
    for y in range(28, 34):
        m.put(30, y, FALLS_L)
        m.put(31, y, FALLS_R)
        m.water |= {(30, y), (31, y)}
    m.stamp("cliff_cave", 29, 30)
    pond = [["TL", "FALL_IN", "FALL_IN", "T", "TR"],
            ["L", "FOAM", "FOAM", "IN", "R"],
            ["L", "IN", "IN", "IN", "R"],
            ["L", "IN", "IN", "IN", "R"]]
    for j, row in enumerate(pond):
        for i, k in enumerate(row):
            m.put(29 + i, 34 + j, POND[k], ".")
            m.water.add((29 + i, 34 + j))
    # Krotos's byre, house and pasture
    m.stamp("byre", 34, 27)
    house(m, 36, 27, 5, ground_row=["wallW", "wall", "doorPan", "wallWin", "wallE"])
    for x in range(36, 40):
        m.part("fence", "gate" if x == 38 else "h", x, 31)
        m.part("fence", "h", x, 36)
    for y in range(32, 36):
        m.part("fence", "v", 35, y)
        m.part("fence", "v", 40, y)
    m.part("fence", "nw", 35, 31)
    m.part("fence", "ne", 40, 31)
    m.part("fence", "sw", 35, 36)
    m.part("fence", "se", 40, 36)
    # the old racecourse, and its finishing post
    for y in range(12, 21):
        m.part("track", "W", 36, y)
        m.part("track", "E", 37, y)
    m.part("track", "post", 35, 20)
    # small aethos cypresses below the hill (rows 36-37, so nothing crosses the strip)
    for (x, y) in SMALL_CYPRESSES:
        m.put(x, y, CYP_TOP)
        m.put(x, y + 1, CYP_BOT)
    # signs and markers
    for (x, y) in STELES.values():
        m.put(x, y, STELE)
    for (x, y) in VERGE_STONES:
        m.put(x, y, BOULDER)
    m.put(14, 40, HERM)
    # --- ground ----------------------------------------------------------
    aethos_woods(m)
    ground(m)
    decorate(m, avoid={(x, y) for y in range(m.h) for x in range(m.w) if m.ch(x, y) == "="})
    return m


def arkadia_events():
    obj, warp, sign, trig, hidden = [], [], [], [], []

    def o(lid, gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False,
          sight=0, item=None, rx=0, ry=0):
        obj.append({"local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
                    "movement_type": move, "movement_range_x": rx, "movement_range_y": ry,
                    "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
                    "trainer_sight_or_berry_tree_id": item or str(sight), "script": script,
                    "flag": flag})

    S = "Arkadia_EventScript_"
    o("LOCALID_ARKADIA_ALETHEA", "OBJ_EVENT_GFX_ICHOR_ALETHEA", 22, 9, S + "Alethea",
      "MOVEMENT_TYPE_FACE_DOWN", "FLAG_ICHOR_KLEON_JOINED_TITANS")
    o("LOCALID_ARKADIA_LAMPLIGHTER", "OBJ_EVENT_GFX_ICHOR_LAMPLIGHTER", 25, 11, S + "Lamplighter",
      "MOVEMENT_TYPE_WANDER_UP_AND_DOWN", ry=1)
    o("LOCALID_ARKADIA_HUNTRESS_1", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 21, 19, S + "Huntress1",
      "MOVEMENT_TYPE_FACE_RIGHT")
    o("LOCALID_ARKADIA_HUNTRESS_2", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 22, 19, S + "Huntress2",
      "MOVEMENT_TYPE_FACE_LEFT")
    o("LOCALID_ARKADIA_TEMPLE_GUARD", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 20, 31, S + "TempleClosed",
      "MOVEMENT_TYPE_FACE_DOWN", "FLAG_ICHOR_KLEON_JOINED_TITANS")
    o("LOCALID_ARKADIA_IAMOS", "OBJ_EVENT_GFX_ICHOR_AUGUR", 17, 18, S + "Iamos",
      "MOVEMENT_TYPE_FACE_DOWN")
    o("LOCALID_ARKADIA_KRONIST", "OBJ_EVENT_GFX_ICHOR_KRONIST", 28, 14, S + "Kronist",
      "MOVEMENT_TYPE_FACE_DOWN")
    o("LOCALID_ARKADIA_HUNTER", "OBJ_EVENT_GFX_ICHOR_MAN", 28, 16, S + "Hunter",
      "MOVEMENT_TYPE_FACE_UP")
    o("LOCALID_ARKADIA_CHILD_1", "OBJ_EVENT_GFX_ICHOR_KID_M", 16, 15, S + "Child1",
      "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1)
    o("LOCALID_ARKADIA_CHILD_2", "OBJ_EVENT_GFX_ICHOR_KID_F", 15, 17, S + "Child2",
      "MOVEMENT_TYPE_FACE_RIGHT")
    o("LOCALID_ARKADIA_LOST_GIRL", "OBJ_EVENT_GFX_ICHOR_KID_F", 23, 35, S + "LostGirl",
      "MOVEMENT_TYPE_FACE_UP", "FLAG_ICHOR_THEOXENIA_START+0x25")
    o("LOCALID_ARKADIA_CORDON_1", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 43, 23, S + "Cordon",
      "MOVEMENT_TYPE_FACE_LEFT", "FLAG_BADGE05_GET")
    o("LOCALID_ARKADIA_CORDON_2", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 43, 24, S + "Cordon",
      "MOVEMENT_TYPE_FACE_LEFT", "FLAG_BADGE05_GET")
    o("LOCALID_ARKADIA_HOPLITE", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 13, 40, S + "Hoplite",
      "MOVEMENT_TYPE_FACE_UP")
    o("LOCALID_ARKADIA_WEST_GUARD_1", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 5, 36, S + "WestGuard",
      "MOVEMENT_TYPE_FACE_RIGHT", "FLAG_ICHOR_POSTGAME")
    o("LOCALID_ARKADIA_WEST_GUARD_2", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 5, 37, S + "WestGuard",
      "MOVEMENT_TYPE_FACE_RIGHT", "FLAG_ICHOR_POSTGAME")
    o("LOCALID_ARKADIA_KID_1", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 19, 6, S + "Kid1",
      "MOVEMENT_TYPE_FACE_DOWN", "FLAG_ICHOR_KROTOS_KID_1")
    o("LOCALID_ARKADIA_KID_2", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 21, 32, S + "Kid2",
      "MOVEMENT_TYPE_FACE_DOWN", "FLAG_ICHOR_KROTOS_KID_2")
    o("LOCALID_ARKADIA_KID_3", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 11, 13, S + "Kid3",
      "MOVEMENT_TYPE_FACE_UP", "FLAG_ICHOR_KROTOS_KID_3")
    o("LOCALID_ARKADIA_GRAZER", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 37, 34, S + "Grazer",
      "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1)
    o("LOCALID_ARKADIA_MAX_REPEL", "OBJ_EVENT_GFX_ITEM_BALL", 34, 26, "Common_EventScript_FindItem",
      "MOVEMENT_TYPE_LOOK_AROUND", "FLAG_ICHOR_ITEM_ARKADIA_MAX_REPEL", item="ITEM_MAX_REPEL")

    for i, (x, y, dest) in enumerate(ARKADIA_DOORS):
        warp.append({"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": "0"})

    def b(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
        sign.append({"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing,
                     "script": script})

    for name, (x, y) in STELES.items():
        b(x, y, S + name)
    b(12, 13, S + "SignAsclepeion")
    b(11, 12, S + "PansGrotto")
    for (x, y) in ((29, 34), (33, 34), (29, 35), (33, 35)):
        b(x, y, S + "Waterfall")
    b(34, 35, S + "DigSpot")
    b(34, 20, S + "TurnedEarth")
    for (x, y, item, flag) in ((21, 9, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ARKADIA_REVIVE"),
                               (31, 10, "ITEM_SILVER_POWDER", "FLAG_ICHOR_HIDDEN_ARKADIA_SILVER_POWDER")):
        hidden.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item,
                       "flag": flag})
    return {"object_events": obj, "warp_events": warp, "coord_events": trig,
            "bg_events": sign + hidden}


# --------------------------------------------------------------------------
# The Cypress Wood and the Pool
# --------------------------------------------------------------------------

def wood():
    m = Map("Arkadia_CypressWood", "Arkadia_CypressWood", "LAYOUT_ARKADIA_CYPRESS_WOOD", P.wood(), "wood")
    m.stamp("tomb", 2, 21)
    m.stamp("kiln_wood", 12, 2)
    for (x, y) in ((18, 20), (20, 20), (8, 20), (1, 20), (1, 24)):
        m.stamp("great_trunk", x, y)
    m.stamp("stump", 15, 13)
    for (x, y) in WOOD_STELES.values():
        m.stamp("stele", x, y)
    m.part("floor", "mats", 32, 29)
    m.part("floor", "mats", 33, 29)
    m.part("floor", "dig", 7, 24)
    ground(m)
    return m


WOOD_STELES = {"SignGate": (34, 28), "SignTomb": (5, 17), "SignPool": (4, 12)}


def wood_events():
    obj, warp, sign, trig = [], [], [], []
    S = "Arkadia_CypressWood_EventScript_"

    def o(lid, gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False,
          sight=0, item=None):
        obj.append({"local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
                    "movement_type": move, "movement_range_x": 0, "movement_range_y": 0,
                    "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
                    "trainer_sight_or_berry_tree_id": item or str(sight), "script": script,
                    "flag": flag})

    # Kleon on the stump: his look is a var (stump, then standing); MOVEMENT_TYPE_NONE
    # keeps the seated pose (SPRITES.md, batch 3). His balls run away from him.
    o("LOCALID_WOOD_KLEON", "OBJ_EVENT_GFX_VAR_0", 15, 13, S + "Kleon",
      "MOVEMENT_TYPE_NONE", "FLAG_ICHOR_KLEON_JOINED_TITANS")
    o("LOCALID_WOOD_BALLS", "OBJ_EVENT_GFX_ICHOR_KLEON_BALLS", 16, 13, S + "Kleon",
      "MOVEMENT_TYPE_FACE_RIGHT", "FLAG_ICHOR_KLEON_JOINED_TITANS")
    o("LOCALID_WOOD_IAPETOS", "OBJ_EVENT_GFX_ICHOR_CHORUS_LEADER", 20, 10, S + "Nothing",
      "MOVEMENT_TYPE_FACE_LEFT", "FLAG_TEMP_11")
    o("LOCALID_WOOD_ALETHEA", "OBJ_EVENT_GFX_VAR_1", 19, 21, S + "Nothing",
      "MOVEMENT_TYPE_FACE_UP", "FLAG_TEMP_12")
    o("LOCALID_WOOD_SKYLAPS", "OBJ_EVENT_GFX_SPECIES(SKYLAPS)", 11, 14, S + "Nothing",
      "MOVEMENT_TYPE_FACE_RIGHT", "FLAG_TEMP_13")
    o("LOCALID_WOOD_KERDOVIX", "OBJ_EVENT_GFX_SPECIES(KERDOVIX)", 11, 13, S + "Nothing",
      "MOVEMENT_TYPE_FACE_RIGHT", "FLAG_TEMP_14")
    o("LOCALID_WOOD_EUADNE", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 18, 21, S + "Euadne",
      "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=4)
    o("LOCALID_WOOD_AGAPENOR", "OBJ_EVENT_GFX_ICHOR_CHARCOALER", 14, 4, S + "Agapenor",
      "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2)
    o("LOCALID_WOOD_HEKAERGE", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 30, 9, S + "Hekaerge",
      "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3)
    o("LOCALID_WOOD_MAINALOS", "OBJ_EVENT_GFX_ICHOR_CHARCOALER", 26, 26, S + "Mainalos",
      "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3)
    o("LOCALID_WOOD_LYSIPPE", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 3, 12, S + "Lysippe",
      "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3)
    o("LOCALID_WOOD_MELANIPPE", "OBJ_EVENT_GFX_ICHOR_HUNTRESS", 7, 19, S + "Melanippe",
      "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4)
    o("LOCALID_WOOD_DUSK_BALLS", "OBJ_EVENT_GFX_ITEM_BALL", 17, 3, S + "DuskBalls",
      "MOVEMENT_TYPE_LOOK_AROUND", "FLAG_ICHOR_ITEM_CYPRESS_WOOD_DUSK_BALLS", item="ITEM_DUSK_BALL")
    o("LOCALID_WOOD_DUSK_STONE", "OBJ_EVENT_GFX_ITEM_BALL", 33, 12, "Common_EventScript_FindItem",
      "MOVEMENT_TYPE_LOOK_AROUND", "FLAG_ICHOR_ITEM_CYPRESS_WOOD_DUSK_STONE", item="ITEM_DUSK_STONE")
    o("LOCALID_WOOD_HYPER_POTION", "OBJ_EVENT_GFX_ITEM_BALL", 21, 27, "Common_EventScript_FindItem",
      "MOVEMENT_TYPE_LOOK_AROUND", "FLAG_ICHOR_ITEM_CYPRESS_WOOD_HYPER_POTION", item="ITEM_HYPER_POTION")
    o("LOCALID_WOOD_HEDGE", "OBJ_EVENT_GFX_CUTTABLE_TREE", 19, 3, S + "Hedge",
      "MOVEMENT_TYPE_FACE_DOWN", "FLAG_BADGE05_GET")
    o("LOCALID_WOOD_VIXEN", "OBJ_EVENT_GFX_SPECIES(KERDOVIX)", 22, 2, S + "SleepingVixen",
      "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_15")

    for x in (32, 33):
        warp.append({"x": x, "y": 29, "elevation": 0, "dest_map": "MAP_ARKADIA", "dest_warp_id": "7"})
    trig.append({"type": "trigger", "x": 19, "y": 18, "elevation": 3, "var": "VAR_TEMP_1",
                 "var_value": "0", "script": S + "NewMoon"})

    def b(x, y, script):
        sign.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                     "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script})

    for name, (x, y) in WOOD_STELES.items():
        b(x, y, S + name)
    b(15, 13, S + "Stump")
    b(4, 22, "EventScript_IchorAltar_Artemis")
    b(4, 23, S + "TabletEarth")
    b(7, 24, S + "DigSpot")
    for (x, y, item, flag) in ((13, 3, "ITEM_CHARCOAL", "FLAG_ICHOR_HIDDEN_CYPRESS_WOOD_CHARCOAL"),
                               (24, 7, "ITEM_BIG_MUSHROOM", "FLAG_ICHOR_HIDDEN_CYPRESS_WOOD_BIG_MUSHROOM"),
                               (3, 22, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_CYPRESS_WOOD_STAR_PIECE")):
        sign.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag})
    return {"object_events": obj, "warp_events": warp, "coord_events": trig, "bg_events": sign}


POPLARS = [("poplar", 5, 3), ("poplar_b", 10, 3), ("poplar", 15, 4), ("poplar_b", 17, 12),
           ("poplar", 11, 13), ("poplar_b", 5, 12), ("poplar", 3, 7)]


def pool():
    m = Map("PoolOfMnemosyne", "PoolOfMnemosyne", "LAYOUT_POOL_OF_MNEMOSYNE", P.pool(), "wood")
    m.stamp("pool", 10, 8)
    m.part("seat", "seat", 7, 9)
    m.part("seat", "dig", 6, 6)
    m.part("seat", "dig", 15, 8)
    for (k, x, y) in POPLARS:
        m.stamp(k, x, y)
    m.put(21, 8, STELE)
    ground(m)
    return m


def pool_events():
    S = "PoolOfMnemosyne_EventScript_"
    obj = [{"local_id": "LOCALID_POOL_MNASEAS", "graphics_id": "OBJ_EVENT_GFX_ICHOR_ELDER_M", "x": 7,
            "y": 9, "elevation": 3, "movement_type": "MOVEMENT_TYPE_FACE_RIGHT", "movement_range_x": 0,
            "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0", "script": S + "Mnaseas", "flag": "0"}]
    for (lid, x, y, item, flag) in (("LOCALID_POOL_ULTRA_BALL", 3, 11, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_POOL_ULTRA_BALL"),
                                    ("LOCALID_POOL_PP_UP", 19, 15, "ITEM_PP_UP", "FLAG_ICHOR_ITEM_POOL_PP_UP"),
                                    ("LOCALID_POOL_ETHER", 13, 2, "ITEM_ETHER", "FLAG_ICHOR_ITEM_POOL_ETHER")):
        obj.append({"local_id": lid, "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y,
                    "elevation": 3, "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0,
                    "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
                    "trainer_sight_or_berry_tree_id": item, "script": "Common_EventScript_FindItem",
                    "flag": flag})
    bg = []
    for (x, y) in ((10, 9), (13, 9), (11, 8), (12, 8), (11, 10), (12, 10), (10, 10), (13, 10)):
        bg.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                   "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": S + "Pool"})
    for (x, y, s) in ((21, 8, "Sign"), (6, 6, "OldPoplar"), (15, 8, "DigSpot")):
        bg.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                   "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": S + s})
    bg.append({"type": "hidden_item", "x": 9, "y": 10, "elevation": 3, "item": "ITEM_MOON_STONE",
               "flag": "FLAG_ICHOR_HIDDEN_POOL_MOON_STONE"})
    bg.append({"type": "hidden_item", "x": 14, "y": 10, "elevation": 3, "item": "ITEM_STARDUST",
               "flag": "FLAG_ICHOR_HIDDEN_POOL_STARDUST"})
    bg.append({"type": "hidden_item", "x": 4, "y": 15, "elevation": 3, "item": "ITEM_PRETTY_FEATHER",
               "flag": "FLAG_ICHOR_HIDDEN_POOL_PRETTY_FEATHER"})
    return {"object_events": obj, "warp_events": [], "coord_events": [], "bg_events": bg}


# --------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------

BORDERS = {}


def write(m, events, music, connections, map_type="MAP_TYPE_ROUTE", border=None):
    d = ROOT / "data/layouts" / m.folder
    d.mkdir(parents=True, exist_ok=True)
    m.blocks().tofile(d / "map.bin")
    np.array(border, "<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == m.layout:
            lay.update({"width": m.w, "height": m.h, "primary_tileset": "gTileset_Aethos",
                        "secondary_tileset": SETS[m.setname][0]})
            break
    else:
        sys.exit(f"no layout {m.layout}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    path = ROOT / "data/maps" / m.folder / "map.json"
    mp = json.loads(path.read_text())
    mp["music"] = music
    mp["map_type"] = map_type
    mp["connections"] = connections or None
    mp.update(events)
    path.write_text(json.dumps(mp, indent=2, ensure_ascii=False) + "\n")


def renderer(secondary):
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                           rm.Tileset(rm.resolve_tileset(secondary, syms)))


def render(m, events, border, tag="", publish=False, views=()):
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer(SETS[m.setname][0])
    RENDER.mkdir(parents=True, exist_ok=True)
    img = rm.render_blocks(r, m.blocks().ravel(), m.w)
    plain = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
    plain.save(RENDER / f"{m.name}{tag}.png")
    if publish:
        plain.save(IMG / f"{m.name}.png")
    s = 3
    rev = img.resize((img.width * s, img.height * s), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", rev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    font = ImageFont.load_default(size=11)
    cell = 16 * s
    for y in range(m.h):
        for x in range(m.w):
            if m.walk[y][x] == "X" and (x, y) not in m.water:
                d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=(255, 0, 0, 45))
    for e in events.get("object_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 4, y * cell + 4, x * cell + cell - 5, y * cell + cell - 5],
                    outline=(40, 80, 255), width=3)
        label = e["script"].split("_")[-1]
        d.text((x * cell + 2, y * cell + 2), label[:8], fill=(255, 255, 255, 255), font=font,
               stroke_width=2, stroke_fill=(0, 0, 0, 255))
    colors = {"sign": (255, 220, 0), "hidden_item": (0, 220, 120), "trigger": (255, 0, 255)}
    for e in events.get("bg_events", []) + events.get("coord_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 10, y * cell + 10, x * cell + cell - 11, y * cell + cell - 11],
                    outline=colors[e["type"]], width=3)
    for e in events.get("warp_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 14, y * cell + 14, x * cell + cell - 15, y * cell + cell - 15],
                    outline=(0, 255, 255), width=4)
    for i in range(max(m.w, m.h)):
        if i < m.w:
            d.text((i * cell + cell // 2 - 6, 0), str(i), fill=(255, 255, 255, 255), font=font,
                   stroke_width=2, stroke_fill=(0, 0, 0, 255))
        if i < m.h:
            d.text((2, i * cell + cell // 2 - 6), str(i), fill=(255, 255, 255, 255), font=font,
                   stroke_width=2, stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(rev, over).convert("RGB").save(RENDER / f"{m.name}{tag}_review.png")
    if views:
        pad = 8
        W, H = m.w + 2 * pad, m.h + 2 * pad
        big = np.zeros((H, W), np.uint16)
        for y in range(H):
            for x in range(W):
                big[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
        big[pad:pad + m.h, pad:pad + m.w] = m.blocks() & 0x3FF
        full = rm.render_blocks(r, big.ravel(), W)
        shots = []
        for (px, py) in views:
            x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16 + 8
            shots.append(full.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
        cols = 3
        nrows = (len(shots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 488 + 8, nrows * 328 + 8), (24, 24, 32))
        for i, sh in enumerate(shots):
            sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
        sheet.save(RENDER / f"{m.name}{tag}_screens.png")


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def reach(m, starts, blocked_extra=(), people=()):
    blocked_extra = set(blocked_extra) | set(people)
    ok = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and not m.blocked(x, y) and \
        (x, y) not in blocked_extra
    seen = {s for s in starts if ok(*s)}
    dq = deque(seen)
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < m.w and 0 <= ny < m.h and m.walk[ny][nx] == "J" and dy == 1:
                ny += 1
            if ok(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                dq.append((nx, ny))
    return seen


def faceable(cells, x, y):
    return any((x + dx, y + dy) in cells for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)))


def check_common(m, events, starts, errs):
    seen = reach(m, starts)
    for e in events["object_events"]:
        x, y = e["x"], e["y"]
        if "FLAG_TEMP" in e["flag"] or e["local_id"] in ("LOCALID_WOOD_VIXEN",):
            continue
        if not faceable(seen, x, y) and (x, y) not in seen:
            errs.append(f"{m.name}: {e['local_id']} at ({x},{y}) can't be reached")
    for e in events["bg_events"]:
        x, y = e["x"], e["y"]
        if not faceable(seen, x, y) and (x, y) not in seen:
            errs.append(f"{m.name}: bg {e.get('script', e.get('item'))} at ({x},{y}) can't be reached")
    for e in events["warp_events"]:
        x, y = e["x"], e["y"]
        if not faceable(seen, x, y):
            errs.append(f"{m.name}: warp to {e['dest_map']} at ({x},{y}) can't be reached")
    return seen


def check(maps):
    errs = []
    a, ae, w, we, p, pe = maps
    # Arkadia: the strips are aethos-only
    for y in range(a.h):
        for x in range(a.w):
            if (y in P.STRIP_ROWS or x in P.STRIP_COLS) and a.mt[y][x] >= 0x200:
                errs.append(f"Arkadia ({x},{y}): 0x{a.mt[y][x]:03X} in an aethos-only seam strip")
    # the north edge open exactly on the road and its verges
    for x in range(a.w):
        open_ = not a.blocked(x, 0)
        if open_ != (x in (22, 23, 24, 25)):
            errs.append(f"Arkadia: north edge at column {x} {'open' if open_ else 'closed'}")
    for (x, y) in ((49, P.EAST_ROAD[0]), (49, P.EAST_ROAD[1]), (0, P.WEST_ROAD[0]), (0, P.WEST_ROAD[1]),
                   (P.SOUTH_ROAD[0], 43), (P.SOUTH_ROAD[1], 43)):
        if a.blocked(x, y):
            errs.append(f"Arkadia: the road at the edge ({x},{y}) is blocked")
    people = {(e["x"], e["y"]) for e in ae["object_events"]
              if e["local_id"] not in ("LOCALID_ARKADIA_LAMPLIGHTER", "LOCALID_ARKADIA_CHILD_1")}
    seen = check_common(a, ae, [(23, 0)], errs)
    # with the cordon, the hoplite and the guards standing, the town is closed but north
    inside = reach(a, [(23, 0)], people=people)
    for (x, y, what) in ((49, P.EAST_ROAD[0], "the east road"), (0, P.WEST_ROAD[0], "the west road"),
                         (P.SOUTH_ROAD[0], 43, "the south road")):
        if (x, y) in inside:
            errs.append(f"Arkadia: {what} is open past its guards")
    for (x, y, dest) in ARKADIA_DOORS:
        if a.walk[y][x] == "X":
            errs.append(f"Arkadia: the door to {dest} at ({x},{y}) is on a blocking cell")
    # the Wood: band 1 is forced, Euadne's line is forced, band 2 is forced
    ferns = {(x, y) for y in range(w.h) for x in range(w.w) if w.plan.g[y][x] == ","}
    seenw = check_common(w, we, [(32, 29)], errs)
    if (19, 22) in reach(w, [(32, 29)], blocked_extra=ferns):
        errs.append("Wood: band 1 can be walked round")
    if (19, 18) in reach(w, [(32, 29)], blocked_extra={(19, 21)}):
        errs.append("Wood: the clearing can be reached without passing Euadne's line")
    if (0, 14) in reach(w, [(15, 15)], blocked_extra=ferns):
        errs.append("Wood: band 2 can be walked round")
    if (4, 22) not in seenw and not faceable(seenw, 4, 22):
        errs.append("Wood: the shrine can't be reached")
    for x in range(w.w):
        for y in (0, w.h - 1):
            if not w.blocked(x, y) and not (y == w.h - 1 and x in (32, 33)):
                errs.append(f"Wood: edge open at ({x},{y})")
    for y in range(w.h):
        if not w.blocked(0, y) != (y in P.WOOD_WEST_ROWS):
            errs.append(f"Wood: west edge row {y} {'open' if not w.blocked(0, y) else 'closed'}")
        if not w.blocked(w.w - 1, y):
            errs.append(f"Wood: east edge open at row {y}")
    for y in range(p.h):
        if not p.blocked(p.w - 1, y) != (y in P.POOL_EAST_ROWS):
            errs.append(f"Pool: east edge row {y} {'open' if not p.blocked(p.w - 1, y) else 'closed'}")
    check_common(p, pe, [(23, 10)], errs)
    for mm in (a, w, p):
        for (name, key, blob, x, y) in mm.missing:
            errs.append(f"{name}: no {key} piece for {blob} at ({x},{y}): rebuild the tiles")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    a, ae = arkadia(), arkadia_events()
    w, we = wood(), wood_events()
    p, pe = pool(), pool_events()
    canopy_w = w.cat.named("canopy", "1|11111111")[0]
    canopy_g = p.cat.named("canopy_grass", "1|11111111")[0]
    borders = {"Arkadia": [CYP_TOP, CYP_TOP, CYP_BOT, CYP_BOT],
               "Arkadia_CypressWood": [canopy_w] * 4, "PoolOfMnemosyne": [canopy_g] * 4}
    errs = [] if args.no_check else check((a, ae, w, we, p, pe))
    for e in errs:
        print("CHECK:", e)
    # ICHOR_STUB_MUSIC: Arkadia's cues aren't composed; the road's day and night forms stand in
    write(a, ae, "MUS_ICHOR_ROAD", [{"map": "MAP_ROUTE12_CYPRESS_ROAD", "offset": -6, "direction": "up"}],
          "MAP_TYPE_TOWN", borders["Arkadia"])
    write(w, we, "MUS_ICHOR_ROAD_NIGHT", [{"map": "MAP_POOL_OF_MNEMOSYNE",
                                           "offset": P.WOOD_TO_POOL_OFFSET, "direction": "left"}],
          "MAP_TYPE_ROUTE", borders["Arkadia_CypressWood"])
    write(p, pe, "MUS_ICHOR_HOLLOW", [{"map": "MAP_ARKADIA_CYPRESS_WOOD",
                                       "offset": -P.WOOD_TO_POOL_OFFSET, "direction": "right"}],
          "MAP_TYPE_ROUTE", borders["PoolOfMnemosyne"])
    if args.render or args.publish:
        render(a, ae, borders["Arkadia"], args.tag, args.publish,
               views=[(23, 3), (23, 9), (15, 13), (28, 17), (14, 22), (20, 33), (31, 32), (37, 16),
                      (40, 24), (8, 36), (13, 38), (36, 30)])
        render(w, we, borders["Arkadia_CypressWood"], args.tag, args.publish,
               views=[(32, 27), (31, 22), (21, 22), (16, 14), (14, 5), (6, 14), (5, 24), (21, 3)])
        render(p, pe, borders["PoolOfMnemosyne"], args.tag, args.publish,
               views=[(20, 10), (11, 6), (11, 13)])
    print(f"built Arkadia, the Cypress Wood and the Pool ({len(errs)} check problems)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
