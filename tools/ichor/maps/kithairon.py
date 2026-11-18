#!/usr/bin/env python3
"""Build Route 6 (the Eleutherai road) and Mt. Kithairon: layouts, events,
scripts, wild tables, checks and review renders.

Both maps were placeholders from tools/ichor/maps/thyrsa.py (a straight road
past open grass, every trainer avoidable). This builder replaces their layouts,
events and wild tables; thyrsa.py still writes the trainers' parties.

Route 6, the Eleutherai road. *The old road out of Eleusa climbs terraced
vineyards gone wild to the fort of Eleutherai, whose towers hold the pass under
Kithairon.*
  - Eleusa's olives at the seam, the first forced band between them.
  - The lower terrace: Sostratos the shepherd in plain view, the vines over the
    terrace stair (Demeter's Sickle; Kleon went over the wall), an old press
    choked with vines (the Sickle again, for a Super Potion).
  - The middle terrace: Phano at the stair's head, the vine-dresser's gift,
    Melanippe and the second band, a long meadow east (Lysis, a Great Ball)
    with ledges back down.
  - The fort: two square towers astride the road, Damon in the gate. A postern
    choked with vines leads to the augur's knoll (Theognis, an Ether).
  - Fir and pine above the fort, the third band, and the mountain.

Mt. Kithairon. *A switchback climb up four cliff tiers to Dionysus's altar on
the summit, then a hop down off the peak into the col toward the Kronia
grounds.*
  - T0, the foot: Aktaios guards the first cleft stair.
  - T1: Bromios on the ledge road, a ledge back down, a Great Ball.
  - T2: the maenads' camp (a spring keeper's heal, a gift of Wine), Nysa.
  - The great cliff: a four-row face with a long cut stair.
  - T3: Kleito watches the high meadow (an Ether); the band below the peak.
  - The summit: the altar, Charinos before it, the pine Pentheus climbed, the
    lookout (the summit reward), and a ledge off the peak's west side.
  - The col: Euphron, the last band, and the road down to the Kronia grounds.

Every tier is woods or crag except its road, so the trainers at the narrow
points can't be walked round; ledges only drop south, so the way back is
quick and the way up is earned.

Pieces come from build/skiron/catalog.json (design/phase2/TILES_skiron.md;
make it with /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile).

Usage: /usr/bin/python3 tools/ichor/maps/kithairon.py [--render DIR] [--walk]
  --render DIR  <map>.png (2x, with people), <map>_walk.png (collision, grass,
                sight lines) and 15x10 views along the road
  --walk        prints each walk map (# solid, . open, , grass, v ledge)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
import route5 as R5  # noqa: E402  (aethos ids, noise, behaviors, sprites)

CAT = ROOT / "build/skiron/catalog.json"
GFX = "OBJ_EVENT_GFX_ICHOR_"
noise, behavior = R5.noise, R5.behavior
GRASS, TALL, BOULDER, SIGN = R5.GRASS, R5.TALL, R5.BOULDER, R5.SIGN
TRIPOD_TOP, TRIPOD_BASE = 0x130, 0x131
STONE_PINE, CYPRESS_TOP, CYPRESS_BOT = R5.STONE_PINE, R5.CYPRESS_TOP, R5.CYPRESS_BOT
FACE = {"LEFT": (-1, 0), "RIGHT": (1, 0), "UP": (0, -1), "DOWN": (0, 1)}
SEAM_ROWS = 6       # rows nearest an up/down seam to a non-Skiron map: aethos only


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------
# Plan kinds, one character per cell:
#   #  woods: pines, kermes oak and boulders      ^  crag: boulders, rock, scrub
#   o  olive grove (aethos olives)                .  grass       ,  tall grass
#   p  the path                                   k  under a placed piece
#   b u l f   a cliff band: brink, upper face, lower face, foot (ends are found)
#   s  stone steps cut in a cleft or wall         w  a terrace or fort wall
#   v  a ledge, jump south     <  a ledge, jump west      [ ]  a cliff's side
WALKABLE_KINDS = set(".,ps")


class Grid:
    def __init__(self, name, w, h, strip_top=False, strip_bottom=False):
        self.name, self.w, self.h = name, w, h
        self.cat = {s["key"]: s for s in json.loads(CAT.read_text())}
        self.g = [["#"] * w for _ in range(h)]
        self.mt = np.full((h, w), GRASS, np.int32)
        self.solid = np.zeros((h, w), bool)
        self.fixed = np.zeros((h, w), bool)
        self.kind = np.full((h, w), "", object)
        self.missing = set()
        self.strip = set()
        if strip_top:
            self.strip |= set(range(SEAM_ROWS))
        if strip_bottom:
            self.strip |= set(range(h - SEAM_ROWS, h))

    # --- the plan -----------------------------------------------------------------
    def rect(self, k, x0, y0, x1, y1):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.g[y][x] = k

    def put(self, k, *cells):
        for x, y in cells:
            self.g[y][x] = k

    def at(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    # --- cells and pieces ----------------------------------------------------------
    def set(self, x, y, mid, solid, kind=""):
        if 0 <= x < self.w and 0 <= y < self.h:
            if y in self.strip and mid >= 0x200:
                raise ValueError(f"{self.name}: Skiron metatile 0x{mid:03X} at ({x},{y}) in a seam strip")
            self.mt[y, x], self.solid[y, x], self.fixed[y, x], self.kind[y, x] = mid, solid, True, kind

    def piece(self, key, x, y, cells=None, kind=None, block_t=True):
        s = self.cat[key]
        for cy in range(s["h"]):
            for cx in range(s["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                code = s["walk"][cy][cx]
                solid = code in "XJ" or (code == "T" and block_t) or (code == "." and kind in ("woods", "crag"))
                self.set(x + cx, y + cy, s["ids"][cy][cx], solid, kind or key)

    def named(self, key, name, x, y):
        cx, cy = self.cat[key]["names"][name]
        self.piece(key, x - cx, y - cy, cells={(cx, cy)})

    def room(self, x, y, w, h, kinds, strip_ok=False):
        for cy in range(y, y + h):
            for cx in range(x, x + w):
                if not (0 <= cx < self.w and 0 <= cy < self.h):
                    return False
                if self.g[cy][cx] not in kinds or self.fixed[cy, cx]:
                    return False
                if cy in self.strip and not strip_ok:
                    return False
        return True


# ---------------------------------------------------------------------------
# Painting: bands, walls and ledges, then trees, then the ground
# ---------------------------------------------------------------------------

def runs(g, y, ch):
    """(x0, x1) runs of plan character ch along row y."""
    out, x = [], 0
    while x < g.w:
        if g.g[y][x] == ch:
            x0 = x
            while x < g.w and g.g[y][x] == ch:
                x += 1
            out.append((x0, x - 1))
        else:
            x += 1
    return out


def notch(g, every=6, fill=","):
    """Break long straight tree lines along the road (STYLE.md 4.2: a step or a
    notch every 6 or so): a one-cell bay of long grass in the woods or crag,
    open only to the cell it was cut from."""
    walk = set(".,ps")

    def bay(x, y, fx, fy):
        if g.at(x, y) not in ("#", "^") or y in g.strip:
            return False
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) != (fx, fy) and g.at(nx, ny) in walk | set("v<>sk"):
                return False
        return True
    for d in (-1, 1):
        for y in range(g.h):
            run = 0
            for x in range(g.w):
                if g.at(x, y) in walk and g.at(x, y + d) not in walk | {None}:
                    run += 1
                    if run >= every and bay(x, y + d, x, y):
                        g.g[y + d][x] = fill
                        run = 0
                else:
                    run = 0
        for x in range(g.w):
            run = 0
            for y in range(g.h):
                if g.at(x, y) in walk and g.at(x + d, y) not in walk | {None}:
                    run += 1
                    if run >= every and bay(x + d, y, x, y):
                        g.g[y][x + d] = fill
                        run = 0
                else:
                    run = 0


def face(x, y, salt):
    r = noise(x, y, salt)
    return "B" if r < 12 else "C" if r < 25 else "A"


def bands(g):
    for y in range(g.h):
        for ch in "bulf":
            for x0, x1 in runs(g, y, ch):
                for x in range(x0, x1 + 1):
                    west = x == x0 and x0 > 0
                    east = x == x1 and x1 < g.w - 1
                    below = g.at(x, y + 1)
                    on_path = below in ("p", "s")
                    if ch == "b":
                        if west or east:
                            g.named("bank_end_w" if west else "bank_end_e", "brink", x, y)
                        else:
                            r = noise(x, y, 9)
                            g.named("cliff_brink", "bite" if r < 7 else "B" if r < 25 else "A", x, y)
                    elif ch == "u":
                        if west or east:
                            g.named("bank_end_w" if west else "bank_end_e", "face_u", x, y)
                        else:
                            g.named("cliff", "face_u_" + face(x, y, 2), x, y)
                    elif ch == "l":
                        g.named("cliff", "face_l_" + ("B" if noise(x, y, 3) < 6 else "A"), x, y)
                    else:
                        if west or east:
                            g.named("bank_end" if on_path else "bank_end_grass",
                                    "foot_w" if west else "foot_e", x, y)
                        else:
                            g.named("bank" if on_path else "bank_grass", "foot_" + "ABC"[noise(x, y, 5) % 3], x, y)
        for x0, x1 in runs(g, y, "v"):
            for x in range(x0, x1 + 1):
                name = "W" if x == x0 and x0 > 0 and x1 > x0 else "E" if x == x1 and x1 < g.w - 1 and x1 > x0 else "run"
                g.named("lip", name, x, y)
        for x0, x1 in runs(g, y, "w"):
            for x in range(x0, x1 + 1):
                name = "W" if x == x0 and x0 > 0 else "E" if x == x1 and x1 < g.w - 1 else "run"
                g.named("terrace_wall", name, x, y)
        for x in range(g.w):
            ch = g.g[y][x]
            if ch == "s":
                g.named("terrace_wall", "steps", x, y)
            elif ch in "<>":
                key = "lip_west" if ch == "<" else "lip_east"
                up, down = g.at(x, y - 1) == ch, g.at(x, y + 1) == ch
                g.named(key, "run" if up and down else "S" if up else "N" if down else "run", x, y)
                # a sideways ledge carries its jump, but is solid like any ledge
                g.solid[y, x] = True
            elif ch in "[]":
                g.named("cliff_side", "side_e" if ch == "[" else "side_w", x, y)


def trees(g):
    """Fill woods and crag top down so the tree line staggers. Seam strips get
    aethos's stone pines, cypresses and boulders; the rest Skiron's pines, oak,
    rock and boulders. Every woods and crag cell is solid."""
    woods, crag = ("#",), ("^",)
    for y in range(-2, g.h):
        for x in range(g.w):
            if 0 <= y and (g.fixed[y, x] or g.g[y][x] not in "#^"):
                continue
            n = noise(x, y, 21 + len(g.name))
            here = g.at(x, max(y, 0))
            if y in g.strip and here in "#^":
                # seam rows: cypress stands, a few stone pines
                if y + 1 in g.strip and n < 22 and g.room(x, y, 2, 2, ("#", "^"), strip_ok=True):
                    for j in range(2):
                        for i in range(2):
                            g.set(x + i, y + j, STONE_PINE[j][i], True, "woods")
                elif g.room(x, y, 1, 2, ("#", "^"), strip_ok=True):
                    g.set(x, y, CYPRESS_TOP, True, "woods")
                    g.set(x, y + 1, CYPRESS_BOT, True, "woods")
                continue
            if here == "#":
                if y < 0:
                    continue
                if n < 34 and g.room(x, y, 2, 3, woods):
                    g.piece("pine_tall", x, y, kind="woods")
                elif n < 42 and g.room(x, y, 3, 3, woods):
                    g.piece("pine_lean" if noise(x, y, 3) < 50 else "pine_lean_w", x, y, kind="woods")
                elif n < 58 and g.room(x, y, 1, 2, woods):
                    g.piece("pine_young", x, y, kind="woods")
                elif n < 64 and g.room(x, y, 2, 2, woods):
                    g.piece("boulders", x, y, kind="woods")
            elif here == "^" and y >= 0:
                # crag masses: boulder heaps and wind-bent pines, rocks between
                if n < 26 and g.room(x, y, 2, 2, crag):
                    g.piece("boulders", x, y, kind="crag")
                elif n < 44 and g.room(x, y, 2, 3, crag):
                    g.piece("pine_tall", x, y, kind="crag")
                elif n < 50 and g.room(x, y, 3, 3, crag):
                    g.piece("pine_lean" if noise(x, y, 3) < 50 else "pine_lean_w", x, y, kind="crag")
                elif n < 66 and g.room(x, y, 1, 2, crag):
                    g.piece("pine_young", x, y, kind="crag")
    for y in range(g.h):
        for x in range(g.w):
            if g.fixed[y, x] or g.g[y][x] not in "#^":
                continue
            if y in g.strip:
                if g.room(x, y, 1, 2, ("#", "^"), strip_ok=True) and noise(x, y, 23) < 85:
                    g.set(x, y, CYPRESS_TOP, True, "woods")
                    g.set(x, y + 1, CYPRESS_BOT, True, "woods")
                else:
                    g.set(x, y, BOULDER, True, "woods")
                continue
            n = noise(x, y, 22)
            if g.g[y][x] == "^":
                g.piece("rock" if n < 55 else "oak", x, y, kind="crag")
            else:
                g.piece("oak" if n < 86 else "rock", x, y, kind="woods")


def olives(g):
    """Aethos olives in 2x2 blocks on even columns and even rows, in step with
    Eleusa's grove across the seam (its y = ours - 40, its x = ours + 34), with
    cypress pairs breaking them up."""
    def free(x, y):
        return 0 <= x < g.w and 0 <= y < g.h and g.g[y][x] == "o" and not g.fixed[y, x]
    for y in range(0, g.h, 2):
        for x in range(0, g.w, 2):
            cells = [(x + i, y + j) for j in range(2) for i in range(2) if 0 <= y + j < g.h]
            if not cells or not all(free(cx, cy) for cx, cy in cells):
                continue
            cyp = noise(x, y, 31) < 16 and 0 <= y and y + 1 < g.h
            for i in range(2):
                if cyp:
                    g.set(x + i, y, CYPRESS_TOP, True, "cypress_top")
                    g.set(x + i, y + 1, CYPRESS_BOT, True, "cypress_bot")
                    continue
                if y >= 0:
                    g.set(x + i, y, R5.OLIVE_TOP[i], True, "olive_top")
                if y + 1 < g.h:
                    g.set(x + i, y + 1, R5.OLIVE_BOT[i], True, "olive_bot")
    for y in range(g.h):
        for x in range(g.w):
            if free(x, y):
                g.set(x, y, BOULDER, True, "olive")
    for y in range(1, g.h):
        for x in range(g.w):
            if g.kind[y, x] != "olive_top":
                continue
            i = 0 if g.mt[y, x] == R5.OLIVE_TOP[0] else 1
            k = g.kind[y - 1, x]
            if k == "olive_bot":
                g.mt[y - 1, x] = R5.OLIVE_BOT_TIP[i]
            elif k == "cypress_bot":
                g.mt[y - 1, x] = R5.CYPRESS_BOT_UNDER_TIP[i]
            elif not g.fixed[y - 1, x] and g.g[y - 1][x] == ".":
                g.set(x, y - 1, R5.OLIVE_TIP_GRASS[i], False, "tip")


def ground(g, decorate=True):
    tall = g.cat["tall"]
    pathm = np.array([[g.g[y][x] == "p" for x in range(g.w)] for y in range(g.h)])
    tallm = np.array([[g.g[y][x] == "," for x in range(g.w)] for y in range(g.h)])
    for y in range(g.h):
        for x in range(g.w):
            if g.fixed[y, x]:
                continue
            k = g.g[y][x]
            if k == "p":
                def out(dx, dy):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < g.w and 0 <= Y < g.h):
                        return False
                    return not pathm[Y, X] and g.g[Y][X] in ".,#^ok"
                n, s, w, e = out(0, -1), out(0, 1), out(-1, 0), out(1, 0)
                key = "c" if (n and s) or (w and e) else R5.edge9(n, s, w, e)
                g.set(x, y, R5.PATH[key], False, "path")
                g.fixed[y, x] = False
            elif k == ",":
                nb = []
                for dx, dy in R5.DIRS8:
                    X, Y = min(max(x + dx, 0), g.w - 1), min(max(y + dy, 0), g.h - 1)
                    nb.append("1" if tallm[Y, X] else "0")
                key = R5.canon("1", nb)
                if key == R5.FULL or y in g.strip:
                    mid = TALL
                elif key in tall["names"]:
                    cx, cy = tall["names"][key]
                    mid = tall["ids"][cy][cx]
                else:
                    g.missing.add(key)
                    mid = TALL
                g.set(x, y, mid, False, "tall")
                g.fixed[y, x] = False
            elif k in ".k":
                g.set(x, y, GRASS, False, "grass")
                g.fixed[y, x] = False
                if decorate and y not in g.strip and k == ".":
                    r = noise(x, y, 41 + len(g.name))
                    if r < 6:
                        g.piece("thyme", x, y)
                    elif r < 11:
                        g.piece("dry_grass", x, y)
                    elif r < 14:
                        g.piece("pebbles", x, y)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def obj(lid, gfx, x, y, facing, script, flag="0", sight=0, trainer=False):
    return {"local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}" if facing else "MOVEMENT_TYPE_NONE",
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}


class Spec:
    """One map's events: trainers (mandatory or not), people, thickets, items,
    hidden items and signs, plus its scripts and connections."""

    def __init__(self, name, map_id, tag):
        self.name, self.map_id, self.tag = name, map_id, tag
        self.px = name + "_EventScript_"
        self.trainers, self.people, self.thickets = [], [], []
        self.items, self.hidden, self.signs, self.scripts = [], [], [], []
        self.connections = []

    def trainer(self, name, gfx, x, y, facing, sight, intro, defeat, mandatory=True):
        self.trainers.append(dict(name=name, gfx=GFX + gfx, x=x, y=y, facing=facing, sight=sight,
                                  intro=intro, defeat=defeat, mandatory=mandatory))

    def objects(self):
        lid = "LOCALID_" + R5.re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", self.name).upper() + "_"
        out = []
        for t in self.trainers:
            out.append(obj(lid + t["name"], t["gfx"], t["x"], t["y"], t["facing"], self.px + t["name"],
                           sight=t["sight"], trainer=True))
        for name, gfx, x, y, facing, flag in self.people:
            out.append(obj(lid + name.upper(), gfx if gfx.startswith("OBJ_") else GFX + gfx, x, y, facing,
                           self.px + name, flag))
        for name, x, y, flag in self.thickets:
            out.append(obj(lid + name.upper(), "OBJ_EVENT_GFX_CUTTABLE_TREE", x, y, None,
                           "EventScript_CutTree", flag))
        for item, x, y, flag in self.items:
            o = obj(None, "OBJ_EVENT_GFX_ITEM_BALL", x, y, "DOWN", "Common_EventScript_FindItem", flag)
            o.pop("local_id")
            o["trainer_sight_or_berry_tree_id"] = item
            out.append(o)
        return out

    def bgs(self):
        out = [{"type": "sign", "x": x, "y": y, "elevation": 0,
                "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": self.px + s}
               for x, y, f, s in self.signs]
        out += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
                 "quantity": 1, "underfoot": False} for item, x, y, flag in self.hidden]
        return out


def write_events(g, spec):
    path = ROOT / f"data/maps/{spec.name}/map.json"
    m = json.loads(path.read_text())
    m["music"] = "MUS_ICHOR_ROAD"
    m["map_type"] = "MAP_TYPE_ROUTE"
    m["connections"] = spec.connections
    m["object_events"] = spec.objects()
    m["warp_events"] = []
    m["coord_events"] = []
    m["bg_events"] = spec.bgs()
    path.write_text(json.dumps(m, indent=2) + "\n")
    scripts = [f"mapscripts {spec.name}_MapScripts {{}}",
               f"// Generated by tools/ichor/maps/kithairon.py; edit the builder, not this file."]
    for t in spec.trainers:
        scripts.append(f'''script {spec.px}{t["name"]} {{
    trainerbattle_single(TRAINER_ICHOR_{t["name"]}, format("{t["intro"]}"), format("{t["defeat"]}"))
    msgbox(format("{t["defeat"]}"), MSGBOX_AUTOCLOSE)
    end
}}''')
    scripts += spec.scripts
    (ROOT / f"data/maps/{spec.name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")


def write_layout(g, border_key):
    lay_dir = ROOT / f"data/layouts/{g.name}"
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mt[y, x]) & 0x3FF
            out[y, x] = mid | (1 << 10) if g.solid[y, x] else mid | (3 << 12)
    out.astype("<u2").tofile(lay_dir / "map.bin")
    s = g.cat[border_key]
    border = np.array([s["ids"][1][0], s["ids"][1][1], s["ids"][2][0], s["ids"][2][1]], np.uint16) | (1 << 10)
    border.astype("<u2").tofile(lay_dir / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    lid = "LAYOUT_" + R5.re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", g.name).upper()
    for l in data["layouts"]:
        if l.get("id") == lid:
            want = (g.w, g.h, "gTileset_Aethos", "gTileset_Skiron")
            if (l["width"], l["height"], l["primary_tileset"], l["secondary_tileset"]) != want:
                l["width"], l["height"], l["primary_tileset"], l["secondary_tileset"] = want
                path.write_text(json.dumps(data, indent=2) + "\n")
            return out
    raise SystemExit(f"no layout {lid}")


# ---------------------------------------------------------------------------
# Route 6, the Eleutherai road (28x40)
# ---------------------------------------------------------------------------
R6 = "Route6_EleutheraiRoad"
KITH = "MtKithairon"
SOUTH_COLS_R6 = (10, 13)   # Eleusa's north edge is open at its x 44-47 (our 10-13, offset -34)
GATE = (12, 13)             # the road between the fort's towers; Kithairon's foot is on these columns


def plan_route6():
    W, H = 28, 40
    g = Grid(R6, W, H, strip_bottom=True)
    # --- Eleusa's olives at the seam (rows 31-39): the road between them -------------
    g.rect("o", 0, 32, W - 1, H - 1)
    g.rect(".", 10, 31, 13, H - 1)
    g.rect("p", 11, 29, 12, H - 1)
    g.rect(",", 10, 34, 13, 35)                     # band 1, walled by the olives
    g.put("k", (13, 38))                            # the south sign
    g.rect("#", 0, 31, 9, 31)
    g.rect("#", 14, 31, W - 1, 31)
    # --- the lower terrace (rows 28-30): west to the terrace stair -------------------
    g.rect("#", 0, 28, W - 1, 30)
    g.rect("p", 5, 29, 12, 30)
    g.rect(".", 3, 28, 4, 30)
    g.put("p", (5, 28))                             # the stair's foot
    g.rect(",", 9, 29, 10, 30)                      # band 2
    g.put(".", (8, 28))                             # Sostratos, in plain view
    # the old press east of the road: a meadow, then a yard behind vines
    g.rect(",", 13, 28, 20, 30)
    g.rect(".", 13, 29, 13, 30)
    g.put(".", (21, 29))                            # the press gate (its vines)
    g.rect(".", 22, 28, 25, 30)
    # --- the terrace wall: the vines on its stair, ledges down from the meadow -------
    g.rect("w", 0, 27, W - 1, 27)
    g.put("s", (5, 27))
    g.rect("v", 17, 27, 20, 27)
    # --- the middle terrace (rows 15-26) ------------------------------------------
    g.rect("#", 0, 15, W - 1, 26)
    g.rect("p", 4, 21, 5, 26)                       # up from the stair
    g.rect("p", 4, 21, 13, 22)                      # east along the terrace
    g.rect("p", 12, 15, 13, 22)                     # north to the fort
    g.put(".", (6, 24))                             # Phano's niche
    g.put(".", (3, 26))                             # the vine-dresser's corner
    g.put("k", (3, 25), (6, 26), (7, 26))           # his baskets and firewood
    g.put(".", (9, 20))                             # Melanippe's niche
    g.rect(",", 10, 21, 12, 22)                     # band 3, after Melanippe
    # the long meadow east, with ledges back down to the press
    g.rect(",", 15, 17, 25, 25)
    g.rect(".", 14, 21, 14, 22)
    g.rect(".", 17, 26, 20, 26)
    g.rect(".", 15, 23, 17, 25)
    g.rect(".", 22, 18, 24, 19)
    g.put("^", (25, 17), (25, 18), (15, 17), (24, 25), (25, 25), (15, 25), (20, 20), (21, 20))
    g.rect("^", 15, 15, 20, 16)
    g.rect("^", 24, 15, 26, 16)
    # --- the fort of Eleutherai: two towers astride the road, a wall each side -------
    g.rect("^", 0, 9, W - 1, 13)
    g.rect("w", 0, 14, W - 1, 14)
    g.rect("k", 10, 11, 11, 14)                     # the west tower
    g.rect("k", 14, 11, 15, 14)                     # the east tower
    g.rect("p", 12, 9, 13, 14)
    g.put(".", (11, 10))                            # Damon's post
    g.put("k", (14, 10))                            # the north sign
    g.put("s", (22, 14))                            # the postern (vines)
    g.rect(".", 21, 15, 23, 16)                     # under the postern, from the meadow
    # the augur's knoll behind the postern: a dead end, not a way round the gate
    g.rect(".", 18, 9, 25, 13)
    g.rect(",", 19, 9, 22, 11)
    g.put("^", (18, 9), (25, 9), (18, 13), (25, 13))
    # --- fir and pine up to the mountain; the last band ----------------------------
    g.rect("#", 0, 0, W - 1, 8)
    g.rect("#", 0, 9, 8, 13)
    g.rect("#", 16, 9, 17, 13)
    g.rect("#", 26, 9, W - 1, 13)
    g.rect("p", 12, 0, 13, 8)
    for y, ch in ((1, "b"), (2, "u"), (3, "f")):    # the mountain's first rock
        g.rect(ch, 0, y, W - 1, y)
        g.rect("s" if ch == "u" else "p", 12, y, 13, y)
    g.rect(",", 11, 5, 14, 7)                       # band 4, under the firs
    g.put(".", (11, 4), (14, 8))
    return g


def props_route6(g):
    # the fort's towers, the signs
    g.piece("watchtower", 10, 11)
    g.piece("watchtower", 14, 11)
    g.set(14, 10, SIGN, True, "sign")
    g.set(13, 38, SIGN, True, "sign")
    # the press: amphorae and sherds by its gate; the vine-dresser's baskets
    g.piece("amphorae", 23, 28)
    g.piece("sherds", 25, 28)
    g.piece("baskets", 3, 25)
    g.piece("firewood", 6, 26)
    # the knoll's augur stone and a young pine
    g.piece("stele_low", 24, 10)
    g.piece("pine_young", 18, 11)
    # the meadow: a lone pine and a rock
    g.piece("pine_tall", 22, 21)
    g.piece("rock", 18, 18)


def spec_route6():
    s = Spec(R6, "MAP_ROUTE6_ELEUTHERAI_ROAD", "R6")
    s.connections = [{"direction": "down", "map": "MAP_ELEUSA_VILLAGE", "offset": -34},
                     {"direction": "up", "map": "MAP_MT_KITHAIRON", "offset": 0}]
    s.trainer("SOSTRATOS", "SHEPHERD", 8, 28, "DOWN", 2,
              "My flock won't climb without an audience.", "They liked that.")
    s.trainer("PHANO", "HARVESTER", 6, 24, "LEFT", 2,
              "The vines have ears. Mine have partners.", "All right. You can pass the grapes.")
    s.trainer("MELANIPPE", "ACOLYTE_F", 9, 20, "DOWN", 2,
              "The mountain is the god's other theater.", "A very steep stage.")
    s.trainer("DAMON", "HOPLITE", 11, 10, "RIGHT", 2,
              "The road goes up. Your guard must too.", "Good. Keep your footing.")
    s.trainer("LYSIS", "PILGRIM", 16, 23, "UP", 3,
              "Do you trust the next step?", "That one, apparently.", mandatory=False)
    s.trainer("THEOGNIS", "AUGUR", 21, 12, "UP", 3,
              "My reading promised a quiet walk.", "It left that part out.", mandatory=False)
    s.people.append(("VineDresser", "VINTNER", 3, 26, "RIGHT", "0"))
    s.thickets += [("StairVines", 5, 27, "FLAG_ICHOR_R6_VINES_CUT"),
                   ("PressVines", 21, 29, "FLAG_ICHOR_R6_PRESS_VINES_CUT"),
                   ("PosternVines", 22, 14, "FLAG_ICHOR_R6_POSTERN_VINES_CUT")]
    s.items += [("ITEM_SUPER_POTION", 24, 30, "FLAG_ICHOR_ITEM_R6_HEAL"),
                ("ITEM_GREAT_BALL", 23, 18, "FLAG_ICHOR_ITEM_R6_BALL"),
                ("ITEM_ETHER", 25, 10, "FLAG_ICHOR_ITEM_R6_ETHER")]
    s.hidden += [("ITEM_HONEY", 18, 12, "FLAG_ICHOR_HIDDEN_ITEM_R6_HONEY"),        # the knoll's young pine
                 ("ITEM_REVIVE", 25, 28, "FLAG_ICHOR_HIDDEN_ITEM_R6_REVIVE"),      # in the press's sherds
                 ("ITEM_SUPER_REPEL", 9, 36, "FLAG_ICHOR_HIDDEN_ITEM_R6_REPEL")]   # in the olives by band 1
    s.signs += [(13, 38, "ANY", "SouthSign"), (14, 10, "ANY", "NorthSign"),
                (4, 27, "NORTH", "KleonWall"), (11, 14, "ANY", "FortSign"),
                (24, 10, "ANY", "AugurStone")]
    s.scripts += [
        f'''script {s.px}SouthSign {{
    msgbox(format("Route 6, the Eleutherai road.\\nSouth: Eleusa. North: Mt. Kithairon."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}NorthSign {{
    msgbox(format("Mt. Kithairon. Keep to the road. The mountain keeps the rest."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}KleonWall {{
    msgbox(format("Fresh boot prints go straight up the terrace wall.\\pSomeone didn't wait for the stair."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}FortSign {{
    msgbox(format("Eleutherai. The free town's towers still watch the pass."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}AugurStone {{
    msgbox(format("An augur's stone. Someone scratched a bird on it, flying north."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}VineDresser {{
    lock
    faceplayer
    if (!flag(FLAG_ICHOR_R6_VINEDRESSER_GIFT)) {{
        if (flag(FLAG_ICHOR_R6_VINES_CUT)) {{
            msgbox(format("You cut my old vines? Good. Cut back, they come back sweeter.\\pHere. Plant it somewhere that needs it."))
            giveitem(ITEM_MIRACLE_SEED)
            if (var(VAR_RESULT) == TRUE) {{
                setflag(FLAG_ICHOR_R6_VINEDRESSER_GIFT)
            }}
            release
            end
        }}
    }}
    msgbox(format("These terraces fed the fort once. Now the vines feed themselves."))
    release
}}''',
    ]
    return s


# ---------------------------------------------------------------------------
# Mt. Kithairon (28x52)
# ---------------------------------------------------------------------------

def plan_kithairon():
    W, H = 28, 52
    g = Grid(KITH, W, H, strip_top=True)
    # --- the col and the road down to the Kronia grounds (rows 0-12) -----------------
    g.rect("p", 10, 0, 13, 1)
    g.rect(",", 10, 2, 13, 4)                       # the last band
    g.rect("p", 10, 5, 11, 12)
    g.put(".", (12, 5), (9, 6))                     # Euphron's spot
    g.rect("^", 0, 6, 8, 12)
    g.put("^", (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12))
    g.rect("v", 10, 13, 11, 13)                     # the col drops back to the high meadow
    # --- the summit (rows 6-12, x 13-26) ---------------------------------------------
    g.rect("^", 13, 6, 26, 6)
    g.rect("p", 13, 7, 26, 12)                      # bare limestone above the trees
    g.rect(".", 15, 7, 19, 8)
    g.rect("p", 22, 12, 23, 12)
    g.put("k", (17, 7), (17, 8))                    # the altar
    g.rect("k", 20, 6, 21, 8)                       # Pentheus's pine
    g.rect(",", 13, 12, 20, 12)
    g.rect(",", 24, 7, 26, 9)
    g.put("^", (26, 12), (13, 7), (14, 7))
    for y in range(6, 13):
        g.put("<" if 8 <= y <= 10 else "[", (12, y))
    g.rect("^", 27, 0, 27, 51)
    # the band under the summit, its stair at x 22-23
    for y, ch in ((13, "b"), (14, "u"), (15, "f")):
        g.rect(ch, 12, y, 26, y)
        g.rect("s" if ch == "u" else "p", 22, y, 23, y)
    # --- T3, the high meadow (rows 14-20) ------------------------------------------
    g.rect("^", 0, 13, 9, 20)
    g.rect("^", 10, 16, 26, 20)
    g.rect(",", 5, 14, 11, 16)                      # the meadow under the col
    g.rect(".", 10, 14, 11, 15)
    g.rect("p", 3, 17, 23, 18)
    g.rect("p", 22, 16, 23, 16)
    g.rect("p", 3, 19, 4, 20)
    g.rect(",", 13, 17, 16, 18)                     # band T3
    g.put(".", (4, 15))                             # Kleito's spot
    g.put("^", (5, 14), (11, 16))
    # --- the great cliff (rows 21-24), its long stair at x 3-4 ----------------------
    for y, ch in ((21, "b"), (22, "u"), (23, "l"), (24, "f")):
        g.rect(ch, 0, y, 26, y)
        g.rect("s" if ch in "ul" else "p", 3, y, 4, y)
    # --- T2, the maenads' camp (rows 25-31) -----------------------------------------
    g.rect("^", 0, 25, 26, 31)
    g.rect("p", 3, 25, 4, 29)
    g.rect("p", 3, 28, 23, 29)
    g.rect("p", 22, 28, 23, 31)
    g.rect(".", 6, 25, 11, 27)                      # the camp
    g.put(".", (12, 27))                            # Nysa's spot
    g.rect(",", 15, 28, 17, 29)                     # band T2
    g.rect(",", 14, 30, 20, 31)                     # a hollow below the road
    g.rect(".", 7, 30, 10, 31)                      # down to the ledge
    g.rect(",", 8, 30, 10, 31)
    # --- band B (rows 32-34): the stair east, a ledge west -----------------------------
    for y, ch in ((32, "b"), (33, "u"), (34, "f")):
        g.rect(ch, 0, y, 26, y)
        g.rect("s" if ch == "u" else "p", 22, y, 23, y)
        g.rect("." if ch != "u" else "v", 7, y, 10, y)
    # --- T1, the ledge road (rows 35-41) --------------------------------------------
    g.rect("^", 0, 35, 26, 41)
    g.rect("p", 22, 35, 23, 38)
    g.rect("p", 3, 37, 23, 38)
    g.rect("p", 3, 39, 4, 41)
    g.rect(",", 7, 34, 10, 36)                      # under the ledge, a Great Ball
    g.put(".", (14, 36))                            # Bromios's spot
    g.rect(",", 16, 37, 18, 38)                     # band T1
    g.rect(",", 6, 39, 12, 40)                      # long grass under the road
    g.rect(",", 17, 39, 20, 41)                     # to the ledge down
    g.put(".", (17, 39))
    # --- band A (rows 42-44): the cleft stair west, a ledge east ----------------------
    for y, ch in ((42, "b"), (43, "u"), (44, "f")):
        g.rect(ch, 0, y, 26, y)
        g.rect("s" if ch == "u" else "p", 3, y, 4, y)
        g.rect("." if ch != "u" else "v", 17, y, 20, y)
    # --- T0, the foot (rows 45-51) ---------------------------------------------------
    g.rect("#", 0, 45, 26, H - 1)
    g.rect("p", 3, 45, 4, 47)
    g.rect("p", 3, 46, 13, 47)
    g.rect("p", 12, 46, 13, H - 1)
    g.put(".", (5, 45))                             # Aktaios's spot
    g.rect(",", 7, 46, 9, 47)                       # band T0
    g.rect(",", 4, 48, 9, 49)                       # bracken under the pines
    g.rect(",", 14, 45, 20, 47)                     # the meadow under the ledge
    g.rect(".", 17, 44, 20, 44)
    g.put("^", (14, 45), (15, 45))
    g.put(".", (14, 48))
    g.put("k", (14, 49), (14, 1))                   # the signs
    return g


def props_kithairon(g):
    # the summit: Dionysus's altar (a bronze tripod), the pine Pentheus climbed,
    # the lookout's cairn
    g.set(14, 49, SIGN, True, "sign")
    g.set(14, 1, SIGN, True, "sign")
    g.set(17, 7, TRIPOD_TOP, True, "altar")
    g.set(17, 8, TRIPOD_BASE, True, "altar")
    g.piece("pine_tall", 20, 6)
    g.piece("amphorae", 16, 8)
    g.piece("thyme", 18, 8)
    g.piece("stele_low", 26, 10)
    for x, y in ((15, 9), (19, 10), (21, 9), (25, 10), (14, 11)):
        g.piece("pebbles_path", x, y)                   # scree on the bare top
    g.piece("rock_path", 24, 10)
    # the maenads' camp: a fire, bedrolls, myrtle staves (thyrsoi), baskets
    g.piece("cookfire", 8, 25)
    g.piece("bedrolls", 6, 25)
    g.piece("bedrolls", 11, 25)
    g.piece("myrtle", 7, 25)
    g.piece("baskets", 10, 25)
    g.piece("amphorae", 11, 26)
    # the herdsman's cairn at the foot
    g.piece("stele_low", 15, 48)
    g.piece("pine_young", 18, 45)


def spec_kithairon():
    s = Spec(KITH, "MAP_MT_KITHAIRON", "KITHAIRON")
    s.connections = [{"direction": "down", "map": "MAP_ROUTE6_ELEUTHERAI_ROAD", "offset": 0},
                     {"direction": "up", "map": "MAP_ROUTE7_KRONIA_GROUNDS", "offset": 0}]
    s.trainer("AKTAIOS", "HOPLITE", 5, 45, "LEFT", 2,
              "At the pass, even a whisper carries.", "So does a defeat.")
    s.trainer("BROMIOS", "ACOLYTE_M", 14, 36, "DOWN", 2,
              "The mountain answers a shout.", "It answered yours.")
    s.trainer("NYSA", "ACOLYTE_F", 12, 27, "DOWN", 2,
              "Don't pick the ivy. It picks back.", "You've met it before.")
    s.trainer("KLEITO", "HARVESTER", 4, 15, "RIGHT", 4,
              "Up here the wine needs no water.", "I need some, though.", mandatory=False)
    s.trainer("CHARINOS", "PILGRIM", 17, 9, "DOWN", 3,
              "The god came here dressed as a stranger.", "I'd have offered him a seat.")
    s.trainer("EUPHRON", "SHEPHERD", 9, 6, "RIGHT", 2,
              "Thyrsa's just beyond the next ridge.", "A ridge and a battle.")
    s.people += [("Spring", "ELDER_F", 10, 26, "DOWN", "0"),
                 ("Maenad", "ACOLYTE_F", 7, 26, "RIGHT", "0")]
    s.items += [("ITEM_SUPER_POTION", 26, 11, "FLAG_ICHOR_ITEM_KITHAIRON"),
                ("ITEM_GREAT_BALL", 8, 35, "FLAG_ICHOR_ITEM_KITHAIRON_BALL"),
                ("ITEM_ETHER", 6, 14, "FLAG_ICHOR_ITEM_KITHAIRON_ETHER")]
    s.hidden += [("ITEM_HONEY", 10, 25, "FLAG_ICHOR_HIDDEN_ITEM_KITHAIRON_HONEY"),     # the maenads' baskets
                 ("ITEM_REVIVE", 13, 7, "FLAG_ICHOR_HIDDEN_ITEM_KITHAIRON_REVIVE"),    # a rock by the peak
                 ("ITEM_SUPER_REPEL", 14, 45, "FLAG_ICHOR_HIDDEN_ITEM_KITHAIRON_REPEL")]  # under the ledge
    s.signs += [(14, 49, "ANY", "SouthSign"), (14, 1, "ANY", "NorthSign"),
                (17, 8, "ANY", "Altar"), (20, 8, "ANY", "Pine"), (21, 8, "ANY", "Pine"),
                (15, 48, "ANY", "Cairn"), (26, 10, "ANY", "Lookout")]
    s.scripts += [
        f'''script {s.px}SouthSign {{
    msgbox(format("Mt. Kithairon.\\nSouth: the Eleutherai road."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}NorthSign {{
    msgbox(format("Mt. Kithairon.\\nNorth: down to the Kronia grounds."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Altar {{
    msgbox(format("A bronze tripod, wound with ivy. The bowl smells of fresh wine."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Pine {{
    msgbox(format("A lone pine on the brink. Its top is snapped off.\\pAs if someone climbed it once to watch something he shouldn't."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Cairn {{
    msgbox(format("A herdsman's cairn. A baby's sandal is tied to it, far too small to walk in."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Lookout {{
    msgbox(format("The whole road lies below: Eleusa's fields, the fort, the sea beyond."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Spring {{
    lock
    faceplayer
    msgbox(format("Water first. The god can wait."))
    special(HealPlayerParty)
    release
}}''',
        f'''script {s.px}Maenad {{
    lock
    faceplayer
    if (!flag(FLAG_ICHOR_KITHAIRON_WINE_GIFT)) {{
        msgbox(format("Going down to Thyrsa? Then carry this for us.\\pPour it at his altar. He notices who brings it."))
        giveitem(ITEM_WINE)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_KITHAIRON_WINE_GIFT)
        }}
        release
        end
    }}
    msgbox(format("We dance up here so the city can sleep down there."))
    release
}}''',
    ]
    return s


# ---------------------------------------------------------------------------
# Wild tables
# ---------------------------------------------------------------------------
# Land slots run 20 20 10 10 10 10 5 5 4 4 1 1 percent. Species fit the place:
# Thyrsa's vines and Dionysus's panther cubs, hill goats and hoopoes, stoneborn
# on the mountain road (Cairnolith from 25 up, its evolution level), wolves and
# masks at night. Levels per design/BALANCE.md (Thyrsa: wild 21-28).

WILD = {
    R6: (21, 24, {
        "Morning": ["AMPELIX", "LOPHOPS", "MELIBEE", "ONOTIS", "KERAZAP", "GALEKIT",
                    "PEBBLITH", "STACHYSS", "AMPELIX", "HARPECK", "NEMECUB", "GELASABLE"],
        "Day": ["AMPELIX", "LOPHOPS", "MELIBEE", "ONOTIS", "KERAZAP", "HARPECK",
                "PEBBLITH", "GALEKIT", "STACHYSS", "AMPELIX", "NEMECUB", "GELASABLE"],
        "Evening": ["AMPELIX", "GELASABLE", "ONOTIS", "KERAZAP", "PEBBLITH", "BOTRYKIT",
                    "LOPHOPS", "GALEKIT", "MELIBEE", "NEMECUB", "LYKOPUP", "PROSOMIME"],
        "Night": ["GELASABLE", "BOTRYKIT", "GALEKIT", "PEBBLITH", "LYKOPUP", "AMPELIX",
                  "ONOTIS", "SPALUNK", "GELASABLE", "BOTRYKIT", "PROSOMIME", "NEMECUB"],
    }),
    KITH: (23, 27, {
        "Morning": ["PEBBLITH", "KERAZAP", "LOPHOPS", "HARPECK", "AMPELIX", "MELIBEE",
                    "GALEKIT", "CAIRNOLITH", "NEMECUB", "GELASABLE", "BOTRYKIT", "CAIRNOLITH"],
        "Day": ["PEBBLITH", "KERAZAP", "HARPECK", "LOPHOPS", "AMPELIX", "MELIBEE",
                "NEMECUB", "CAIRNOLITH", "GALEKIT", "GELASABLE", "BOTRYKIT", "CAIRNOLITH"],
        "Evening": ["BOTRYKIT", "PEBBLITH", "CAIRNOLITH", "KERAZAP", "AMPELIX", "GELASABLE",
                    "HARPECK", "LYKOPUP", "NEMECUB", "PROSOMIME", "CAIRNOLITH", "PROSOMIME"],
        "Night": ["BOTRYKIT", "LYKOPUP", "GELASABLE", "PEBBLITH", "PROSOMIME", "CAIRNOLITH",
                  "BOTRYKIT", "GALEKIT", "AMPELIX", "LYKOPUP", "PROSOMIME", "CAIRNOLITH"],
    }),
}
MIN_LEVEL = {"CAIRNOLITH": 25}   # its evolution level: never earlier in the wild


def write_wild():
    path = ROOT / "src/data/wild_encounters.json"
    data = json.loads(path.read_text())
    group = next(gr for gr in data["wild_encounter_groups"] if gr.get("for_maps"))
    ids = {R6: "MAP_ROUTE6_ELEUTHERAI_ROAD", KITH: "MAP_MT_KITHAIRON"}
    keep = [e for e in group["encounters"] if e.get("map") not in ids.values()]
    # put the new tables where the old ones were, so the diff stays small
    at = next(i for i, e in enumerate(group["encounters"]) if e.get("map") in ids.values())
    new = []
    for name, (lo, hi, tables) in WILD.items():
        for time, species in tables.items():
            mons = []
            for i, sp in enumerate(species):
                a = max(lo, MIN_LEVEL.get(sp, lo))
                b = hi if i % 3 else max(a, hi - 1)
                mons.append({"min_level": a, "max_level": b, "species": "SPECIES_" + sp})
            new.append({"map": ids[name], "base_label": f"g{name}_{time}",
                        "land_mons": {"encounter_rate": 25, "mons": mons}})
    before = [e for e in group["encounters"][:at] if e.get("map") not in ids.values()]
    group["encounters"] = before + new + keep[len(before):]
    path.write_text(json.dumps(data, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def walk_graph(g, blocked=frozenset()):
    """step(x, y) -> cells, following collision and ledges (a ledge cell is
    jumped in its own direction only)."""
    jumps = {"MB_JUMP_SOUTH": (0, 1), "MB_JUMP_WEST": (-1, 0), "MB_JUMP_EAST": (1, 0), "MB_JUMP_NORTH": (0, -1)}

    def ok(x, y):
        return 0 <= x < g.w and 0 <= y < g.h and not g.solid[y, x] and (x, y) not in blocked

    def steps(x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < g.w and 0 <= ny < g.h):
                continue
            j = jumps.get(behavior(int(g.mt[ny, nx])))
            if j is not None:
                if j == (dx, dy) and ok(nx + dx, ny + dy):
                    yield nx + dx, ny + dy
                continue
            if ok(nx, ny):
                yield nx, ny
    return steps


def reach(g, starts, blocked=frozenset()):
    steps = walk_graph(g, blocked)
    seen = {s for s in starts if not g.solid[s[1], s[0]] and s not in blocked}
    q = deque(seen)
    while q:
        c = q.popleft()
        for n in steps(*c):
            if n not in seen:
                seen.add(n)
                q.append(n)
    return seen


def grass_cost(g, starts, goals, blocked=frozenset()):
    steps = walk_graph(g, blocked)
    tall = lambda x, y: behavior(int(g.mt[y, x])) == "MB_TALL_GRASS"
    cost = {s: int(tall(*s)) for s in starts if not g.solid[s[1], s[0]]}
    dq = deque(sorted(cost, key=cost.get))
    while dq:
        c = dq.popleft()
        for n in steps(*c):
            v = cost[c] + int(tall(*n))
            if v < cost.get(n, 1 << 30):
                cost[n] = v
                (dq.append if v > cost[c] else dq.appendleft)(n)
    got = [cost[t] for t in goals if t in cost]
    return min(got) if got else None


def sight(g, t):
    dx, dy = FACE[t["facing"]]
    out, x, y = [], t["x"], t["y"]
    for _ in range(t["sight"]):
        x, y = x + dx, y + dy
        if not (0 <= x < g.w and 0 <= y < g.h) or g.solid[y, x]:
            break
        out.append((x, y))
    return out


def check(g, spec, south, north):
    problems = []
    objs = spec.objects()
    gates = {(o["x"], o["y"]) for o in objs if o["graphics_id"] == "OBJ_EVENT_GFX_CUTTABLE_TREE"}
    people = {(o["x"], o["y"]) for o in objs} - gates
    for o in objs:
        if g.solid[o["y"], o["x"]]:
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} on a solid cell")
    # the edges: open where the neighbours are, and joined (Sickle in hand)
    for y, cols, label in ((g.h - 1, south, "south"), (0, north, "north")):
        open_ = {x for x in range(g.w) if not g.solid[y, x]}
        if open_ != set(cols):
            problems.append(f"{label} edge is open at {sorted(open_)}, wanted {sorted(cols)}")
    s_cells = [(x, g.h - 1) for x in south]
    n_cells = [(x, 0) for x in north]
    for a, b, label in ((s_cells, n_cells, "north"), (n_cells, s_cells, "south")):
        if not set(b) & reach(g, a, frozenset(people)):
            problems.append(f"can't walk {label} across the map past the people")
    if set(n_cells) & reach(g, s_cells, frozenset(people | gates)):
        if spec.name == R6:
            problems.append("the vines don't close the road: Route 6 can be walked without the Sickle")
    # everything reachable and readable
    allr = reach(g, s_cells + n_cells, frozenset(people))
    for o in objs:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in allr for dx, dy in FACE.values()):
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} at ({x},{y}) can't be reached")
    for b in spec.bgs():
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and not g.solid[y, x]:
            problems.append(f"sign {b['script']} at ({x},{y}) is on walkable ground")
        spots = [(x, y + 1)] if b.get("player_facing_dir", "").endswith("NORTH") else \
            [(x + dx, y + dy) for dx, dy in FACE.values()]
        if not any(p in allr for p in spots):
            problems.append(f"{b.get('script', b.get('item'))} at ({x},{y}) can't be read")
    pockets = [(x, y) for y in range(g.h) for x in range(g.w) if not g.solid[y, x] and (x, y) not in allr
               and (x, y) not in people | gates]
    if pockets:
        problems.append(f"walkable but cut off: {pockets[:10]}")
    # traps: cells you can reach but not leave (people count as walls)
    for c in sorted(allr):
        if not set(s_cells + n_cells) & reach(g, [c], frozenset(people)):
            problems.append(f"trap at {c}")
            break
    # forced grass, northbound and southbound
    fg = grass_cost(g, s_cells, n_cells, frozenset(people))
    if fg is None or fg < 8:
        problems.append(f"forced grass northbound is {fg} < 8")
    # trainers: the mandatory ones cut the road; nobody ends up blocking it
    mand = []
    for t in spec.trainers:
        cells = set(sight(g, t))
        cut = not set(n_cells) & reach(g, s_cells, frozenset(people | cells))
        if t["mandatory"] and not cut:
            problems.append(f"{t['name']}'s sight can be walked round")
        if cut:
            mand.append(t["name"])
        if len(cells) < t["sight"]:
            problems.append(f"{t['name']} sees {len(cells)} of {t['sight']} cells (blocked)")
        for stop in sight(g, t)[:-1]:
            if not set(n_cells) & reach(g, s_cells, frozenset((people - {(t['x'], t['y'])}) | {stop})):
                problems.append(f"{t['name']} could stop at {stop} and block the road")
    stacked = {}
    for t in spec.trainers:
        for c in sight(g, t):
            stacked[c] = stacked.get(c, 0) + 1
    if any(v >= 3 for v in stacked.values()):
        problems.append("three sight lines on one cell")
    return problems, mand, fg


def walk_text(g, spec):
    objs = {(o["x"], o["y"]): o for o in spec.objects()}
    sights = {c for t in spec.trainers for c in sight(g, t)}
    rows = ["    " + "".join(str(x % 10) for x in range(g.w))]
    for y in range(g.h):
        line = ""
        for x in range(g.w):
            o = objs.get((x, y))
            b = behavior(int(g.mt[y, x]))
            if o is not None:
                line += "T" if o["trainer_type"] != "TRAINER_TYPE_NONE" else \
                        "*" if o["graphics_id"].endswith("CUTTABLE_TREE") else \
                        "o" if o["graphics_id"].endswith("ITEM_BALL") else "@"
            elif b.startswith("MB_JUMP"):
                line += {"MB_JUMP_SOUTH": "v", "MB_JUMP_WEST": "<", "MB_JUMP_EAST": ">"}.get(b, "j")
            elif g.solid[y, x]:
                line += "#"
            elif (x, y) in sights:
                line += "!"
            elif b == "MB_TALL_GRASS":
                line += ","
            else:
                line += "."
        rows.append(f"{y:3d} {line}")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

def render(g, spec, blocks, out_dir, views):
    from PIL import Image, ImageDraw
    import render_map as RM
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset("gTileset_Aethos", syms)),
                    RM.Tileset(RM.resolve_tileset("gTileset_Skiron", syms)))
    flat = RM.render_blocks(r, blocks.reshape(-1), g.w).convert("RGBA")
    for o in spec.objects():
        gfx = o["graphics_id"]
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE" in o["movement_type"] else "DOWN"
        try:
            spr, fw, fh = R5.sprite(gfx, facing)
        except (FileNotFoundError, KeyError):
            continue
        flat.paste(spr, (o["x"] * 16 + 8 - fw // 2, o["y"] * 16 + 16 - fh), spr)
    stem = {R6: "route6", KITH: "kithairon"}[spec.name]
    flat.convert("RGB").resize((g.w * 32, g.h * 32), Image.NEAREST).save(out_dir / f"{stem}.png")
    im = flat.resize((g.w * 32, g.h * 32), Image.NEAREST)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, c = ImageDraw.Draw(ov), 32
    for y in range(g.h):
        for x in range(g.w):
            b = behavior(int(g.mt[y, x]))
            if b.startswith("MB_JUMP"):
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 120, 255, 90))
            elif g.solid[y, x]:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 60))
            elif b == "MB_TALL_GRASS":
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 255, 0, 45))
    for t in spec.trainers:
        col = (255, 160, 0, 255) if t["mandatory"] else (255, 255, 120, 255)
        for (sx, sy) in sight(g, t):
            d.rectangle([sx * c + 6, sy * c + 6, sx * c + c - 7, sy * c + c - 7], outline=col, width=3)
    Image.alpha_composite(im, ov).convert("RGB").save(out_dir / f"{stem}_walk.png")
    shots = []
    for name, px, py in views:
        x0 = min(max(px - 7, 0), g.w - 15) * 16
        y0 = min(max(py - 5, 0), g.h - 10) * 16
        shots.append((name, flat.crop((x0, y0, x0 + 240, y0 + 160)).convert("RGB")))
    cols = 3
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 248 + 8, rows * 178 + 8), (24, 24, 32))
    sd = ImageDraw.Draw(sheet)
    for i, (name, v) in enumerate(shots):
        x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
        sheet.paste(v, (x, y + 10))
        sd.text((x, y - 2), name, fill=(230, 230, 200))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / f"{stem}_views.png")


VIEWS = {
    R6: [("1 Eleusa's olives", 12, 35), ("2 the lower terrace", 7, 29), ("3 the stair's head", 6, 22),
         ("4 the long meadow", 19, 21), ("5 the fort gate", 13, 12), ("6 to the mountain", 13, 4)],
    KITH: [("1 the foot", 8, 46), ("2 the ledge road", 13, 37), ("3 the maenads' camp", 11, 28),
           ("4 the great cliff", 7, 21), ("5 the high meadow", 14, 17), ("6 the summit", 19, 9),
           ("7 the col", 11, 5)],
}


def build(plan, props, specf, border_key, south, north):
    g = plan()
    notch(g)
    bands(g)
    props(g)
    trees(g)
    olives(g)
    ground(g)
    spec = specf()
    blocks = write_layout(g, border_key)
    write_events(g, spec)
    return g, spec, blocks, south, north


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    built = [build(plan_route6, props_route6, spec_route6, "pine_tall", range(10, 14), range(12, 14)),
             build(plan_kithairon, props_kithairon, spec_kithairon, "pine_tall", range(12, 14), range(10, 14))]
    write_wild()
    bad = 0
    for g, spec, blocks, south, north in built:
        problems, mand, fg = check(g, spec, south, north)
        if args.walk:
            print(walk_text(g, spec))
        if args.render:
            render(g, spec, blocks, args.render, VIEWS[spec.name])
        for p in problems:
            print(f"PROBLEM {spec.name}: {p}")
        print(f"{spec.name}: {g.w}x{g.h}, forced grass {fg}, {len(spec.trainers)} trainers, "
              f"{len(mand)} on the only road ({', '.join(mand)}), {len(problems)} problems")
        bad += len(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
