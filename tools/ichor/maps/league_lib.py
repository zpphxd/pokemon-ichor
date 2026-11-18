#!/usr/bin/env python3
"""Shared pieces for the League's map builders (design/LEAGUE.md).

A Grid is one map: a plan of ground kinds, then structures from a tileset's
catalog placed by key and part name (never by raw id), then the soft ground
painted by shape. It writes map.bin/border.bin, the layout's size and tilesets,
and the map's events, and it can check reachability and render review images:
the whole map with its people, and every 15x10 screen along a route.

The Skiron helpers (banks, sea cliffs, woods) follow tools/ichor/maps/route5.py,
the reference builder for gTileset_Skiron (design/phase2/TILES_skiron.md).
"""
from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))

GFX = "OBJ_EVENT_GFX_ICHOR_"

# aethos primary ids (design/phase1/TILES_aethos.md)
A_GRASS, A_GRASS_SHADE, A_TALL, A_FLOWERS = 0x001, 0x002, 0x00D, 0x004
A_SIGN, A_HERM = 0x003, 0x01B
A_TRIPOD_TOP, A_TRIPOD_BASE = 0x130, 0x131
A_SEA = 0x170
A_BOULDER = 0x0E0
A_STEPS = (0x0AF, 0x0CF)
A_PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
          "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
A_CYPRESS = (0x00E, 0x016)
A_STONE_PINE = ((0x01E, 0x01F), (0x026, 0x027))
# the palaestra (General's gym, 6x5), door 0x1CD: the Pantheon's propylaia front
A_PALAESTRA = [[0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
               [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
               [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
               [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
               [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]]
A_PALAESTRA_DOOR = (3, 4)

DIRS8 = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def const(name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name).upper()


def noise(x, y, salt=0):
    """A stable 0..99 per cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 100


def canon(neigh):
    """Skiron's soft-ground shape key: diagonals count only when both sides are in."""
    b = list(neigh)
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] == "1" and b[c] == "1"):
            b[d] = "0"
    return "1|" + "".join(b)


def catalog(name):
    path = ROOT / f"build/{name}/catalog.json"
    if not path.exists():
        builders = {"skiron": "skiron_build.py", "aegina": "aegina_build.py",
                    "labyrinth": "labyrinth_build.py", "temple_demeter": "temple_demeter_build.py"}
        sys.exit(f"{path} is missing; run /usr/bin/python3 tools/ichor/art/{builders.get(name, '?')} --no-compile")
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        data = data.get("pieces") or data.get("structures") or []
    return {s["key"]: s for s in data}


def behavior_names():
    txt = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    out, v = {}, 0
    for name, val in re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", txt, re.M):
        if val:
            v = int(val, 0)
        out[v] = name
        v += 1
    return out


class Grid:
    """One map's cells. kinds: the plan; mt/solid/water: what gets written."""

    def __init__(self, name, w, h, primary="gTileset_Aethos", secondary="gTileset_Skiron",
                 cat="skiron", base=A_GRASS, base_kind="grass"):
        self.name, self.W, self.H = name, w, h
        self.primary, self.secondary = primary, secondary
        self.cat = catalog(cat) if cat else {}
        self.g = [[base_kind] * w for _ in range(h)]
        self.mt = np.full((h, w), base, np.int32)
        self.solid = np.zeros((h, w), bool)
        self.water = np.zeros((h, w), bool)
        self.fixed = np.zeros((h, w), bool)
        self.kind = np.full((h, w), "", object)
        self.missing = set()
        self.events = dict(object_events=[], warp_events=[], coord_events=[], bg_events=[])
        self.prefix = name + "_EventScript_"

    # --- the plan ---------------------------------------------------------------
    def fill(self, kind, x0, y0, x1, y1):
        for y in range(max(0, y0), min(self.H, y1 + 1)):
            for x in range(max(0, x0), min(self.W, x1 + 1)):
                self.g[y][x] = kind

    def rows(self, kind, ox, oy, rows):
        """A mask of '#' cells, top-left at (ox, oy)."""
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c == "#" and 0 <= oy + j < self.H and 0 <= ox + i < self.W:
                    self.g[oy + j][ox + i] = kind

    def at(self, x, y):
        return self.g[y][x] if 0 <= x < self.W and 0 <= y < self.H else None

    def inside(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    # --- cells and pieces -------------------------------------------------------------
    def set(self, x, y, mid, solid, kind="", water=False):
        if self.inside(x, y):
            self.mt[y, x] = mid
            self.solid[y, x] = solid
            self.water[y, x] = water
            self.fixed[y, x] = True
            self.kind[y, x] = kind

    def piece(self, key, x, y, cells=None, kind=None, block_t=False, solid_all=False):
        """A catalog structure, top-left at (x, y). Walk codes: X and S block
        (S is a stair the scripts handle), D is a door, '.' 'G' 'J' are open
        (J is a ledge: solid, as vanilla), T walks behind unless block_t, '-'
        keeps the ground."""
        s = self.cat[key]
        for cy in range(s["h"]):
            for cx in range(s["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                X, Y = x + cx, y + cy
                if not self.inside(X, Y):
                    continue
                code = s["walk"][cy][cx]
                if code == "-":
                    continue
                solid = solid_all or code in ("X", "J", "S") or (code == "T" and block_t)
                sea = s.get("ground", {}).get(f"{cx},{cy}") == "sea"
                self.set(X, Y, s["ids"][cy][cx], solid, kind or key, water=sea and not solid)

    def named(self, key, name, x, y, kind=None, solid=None):
        s = self.cat[key]
        cx, cy = s["names"][name]
        self.piece(key, x - cx, y - cy, cells={(cx, cy)}, kind=kind)
        if solid is not None:
            self.solid[y, x] = solid

    def stamp(self, x, y, rows, solid=True, kind="stamp"):
        for dy, row in enumerate(rows):
            for dx, mid in enumerate(row):
                if mid is not None:
                    self.set(x + dx, y + dy, mid, solid if not isinstance(solid, list) else solid[dy][dx], kind)

    def free(self, x, y, w=1, h=1, kinds=("wood",)):
        return all(self.inside(x + i, y + j) and self.g[y + j][x + i] in kinds
                   and not self.fixed[y + j, x + i] for j in range(h) for i in range(w))

    def region(self, kinds):
        return np.array([[self.g[y][x] in kinds for x in range(self.W)] for y in range(self.H)])

    def shape_key(self, m, x, y):
        nb = []
        for dx, dy in DIRS8:
            X, Y = min(max(x + dx, 0), self.W - 1), min(max(y + dy, 0), self.H - 1)
            nb.append("1" if m[Y, X] else "0")
        return canon(nb)

    # --- events -----------------------------------------------------------------------
    def person(self, lid, gfx, x, y, script, facing="DOWN", sight=0, flag="0", movement=None,
               trainer=False, rx=0, ry=0):
        self.events["object_events"].append(dict(
            local_id=f"LOCALID_{const(self.name)}_{lid}",
            graphics_id=gfx if gfx.startswith("OBJ_EVENT_GFX_") else GFX + gfx,
            x=x, y=y, elevation=3,
            movement_type=movement or f"MOVEMENT_TYPE_FACE_{facing}",
            movement_range_x=rx, movement_range_y=ry,
            trainer_type="TRAINER_TYPE_NORMAL" if (sight or trainer) else "TRAINER_TYPE_NONE",
            trainer_sight_or_berry_tree_id=str(sight),
            script=script if (script.startswith(("EventScript_", "Common_")) or "_EventScript_" in script)
            else self.prefix + script,
            flag=flag))

    def item(self, item, x, y, flag):
        self.events["object_events"].append(dict(
            graphics_id="OBJ_EVENT_GFX_ITEM_BALL", x=x, y=y, elevation=3,
            movement_type="MOVEMENT_TYPE_LOOK_AROUND", movement_range_x=0, movement_range_y=0,
            trainer_type="TRAINER_TYPE_NONE", trainer_sight_or_berry_tree_id=item,
            script="Common_EventScript_FindItem", flag=flag))

    def obstacle(self, lid, kind, x, y, flag="0"):
        gfx, script = {"drum": ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "EventScript_StrengthBoulder"),
                       "rubble": ("OBJ_EVENT_GFX_BREAKABLE_ROCK", "EventScript_RockSmash")}[kind]
        self.person(lid, gfx, x, y, script, movement="MOVEMENT_TYPE_NONE", flag=flag)

    def hidden(self, item, x, y, flag):
        self.events["bg_events"].append(dict(type="hidden_item", x=x, y=y, elevation=3, item=item,
                                             flag=flag, quantity=1, underfoot=False))

    def sign(self, x, y, script, facing="ANY"):
        self.events["bg_events"].append(dict(
            type="sign", x=x, y=y, elevation=0, player_facing_dir=f"BG_EVENT_PLAYER_FACING_{facing}",
            script=script if "_EventScript_" in script or script.startswith("EventScript_") else self.prefix + script))

    def warp(self, x, y, dest, dest_id):
        self.events["warp_events"].append(dict(x=x, y=y, elevation=0, dest_map="MAP_" + const(dest),
                                               dest_warp_id=str(dest_id)))

    def trigger(self, x, y, script, var="VAR_TEMP_1", value="0"):
        self.events["coord_events"].append(dict(type="trigger", x=x, y=y, elevation=3, var=var,
                                                var_value=str(value), script=self.prefix + script))

    # --- output -----------------------------------------------------------------------
    def blockdata(self):
        out = np.zeros((self.H, self.W), np.uint16)
        for y in range(self.H):
            for x in range(self.W):
                mid = int(self.mt[y, x]) & 0x3FF
                if self.solid[y, x]:
                    out[y, x] = mid | (1 << 10)
                elif self.water[y, x]:
                    out[y, x] = mid | (1 << 12)
                else:
                    out[y, x] = mid | (3 << 12)
        return out

    def save(self, border, map_fields=None, connections=None):
        lay_dir = ROOT / "data/layouts" / self.name
        lay_dir.mkdir(parents=True, exist_ok=True)
        self.blockdata().astype("<u2").tofile(lay_dir / "map.bin")
        np.array(border, np.uint16).astype("<u2").tofile(lay_dir / "border.bin")
        path = ROOT / "data/layouts/layouts.json"
        data = json.loads(path.read_text())
        lid = "LAYOUT_" + const(self.name)
        lay = next(l for l in data["layouts"] if l.get("id") == lid)
        want = dict(width=self.W, height=self.H, primary_tileset=self.primary, secondary_tileset=self.secondary)
        if any(lay.get(k) != v for k, v in want.items()):
            lay.update(want)
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        mpath = ROOT / f"data/maps/{self.name}/map.json"
        m = json.loads(mpath.read_text())
        m.update(map_fields or {})
        m["connections"] = connections
        m.update(self.events)
        mpath.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")

    # --- checks -----------------------------------------------------------------------
    def walkable(self, blocked=()):
        ok = ~self.solid & ~self.water
        people = {(o["x"], o["y"]) for o in self.events["object_events"]
                  if o["graphics_id"] not in ("OBJ_EVENT_GFX_ITEM_BALL",)}
        for x, y in set(people) | set(blocked):
            if self.inside(x, y):
                ok[y, x] = False
        return ok

    def reach(self, start, blocked=()):
        ok = self.walkable(blocked)
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if self.inside(X, Y) and (X, Y) not in seen:
                    beh = BEH(self, X, Y)
                    jump = {"MB_JUMP_SOUTH": (0, 1), "MB_JUMP_EAST": (1, 0), "MB_JUMP_WEST": (-1, 0),
                            "MB_JUMP_NORTH": (0, -1)}.get(beh)
                    if jump:
                        if (dx, dy) == jump and self.inside(X + dx, Y + dy) and ok[Y + dy, X + dx]:
                            seen.add((X + dx, Y + dy))
                            q.append((X + dx, Y + dy))
                        continue
                    if ok[Y, X]:
                        seen.add((X, Y))
                        q.append((X, Y))
        return seen

    def check(self, start, must_reach, blocked=()):
        """Fail loudly when anything the player must reach is cut off."""
        seen = self.reach(start, blocked)
        bad = []
        for label, (x, y) in must_reach:
            if not any((x + dx, y + dy) in seen for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))):
                bad.append(f"{label} at {x},{y}")
        if bad:
            raise SystemExit(f"{self.name}: unreachable: " + "; ".join(bad))
        return seen

    def walk_text(self, seen):
        rows = []
        for y in range(self.H):
            r = ""
            for x in range(self.W):
                if (x, y) in seen:
                    r += "," if BEH(self, x, y) == "MB_TALL_GRASS" else "."
                elif self.water[y, x]:
                    r += "~"
                elif self.solid[y, x]:
                    r += "#"
                else:
                    r += "?"
            rows.append(r)
        return "\n".join(rows)


_MB = None
_ATTR = {}


def attrs(tileset):
    if tileset not in _ATTR:
        d = {"gTileset_Aethos": "primary/aethos", "gTileset_Oikos": "primary/oikos"}.get(tileset)
        if d is None:
            d = "secondary/" + re.sub(r"(?<=[a-z])(?=[A-Z])", "_", tileset[len("gTileset_"):]).lower()
        p = ROOT / f"data/tilesets/{d}/porytiles_bin/metatile_attributes.bin"
        if not p.exists():
            p = ROOT / f"data/tilesets/{d}/metatile_attributes.bin"
        _ATTR[tileset] = np.fromfile(p, "<u2")
    return _ATTR[tileset]


def BEH(g, x, y):
    global _MB
    if _MB is None:
        _MB = behavior_names()
    mid = int(g.mt[y, x]) & 0x3FF
    a = attrs(g.primary)[mid] if mid < 0x200 else attrs(g.secondary)[mid - 0x200]
    return _MB.get(int(a) & 0xFF, "?")


# ---------------------------------------------------------------------------
# Skiron: banks, cliffs, woods and the soft ground
# ---------------------------------------------------------------------------

def fv(x, y, salt=1):
    r = noise(x, y, salt)
    return "B" if r < 14 else "C" if r < 18 else "A"


def foot(x, y):
    return "ABC"[noise(x, y, 5) % 3]


def bank_run(g, x0, x1, y, ends=(False, False), tall=False):
    """A cut bank from y: brink, face (and a second face if tall), foot on
    the ground below. ends=(west, east) close the run with its end pieces."""
    rows = 4 if tall else 3
    for x in range(x0, x1 + 1):
        below = g.at(x, y + rows)
        on_path = below in ("path", "road", "scree")
        if (ends[0] and x == x0) or (ends[1] and x == x1):
            side = "bank_end_w" if (ends[0] and x == x0) else "bank_end_e"
            g.named(side, "brink", x, y)
            g.named(side, "face_u", x, y + 1)
            if tall:
                g.named(side, "face_u", x, y + 2)
            g.named("bank_end" if on_path else "bank_end_grass", "foot_w" if side == "bank_end_w" else "foot_e",
                    x, y + rows - 1)
            continue
        g.named("cliff_brink", "bite" if noise(x, y, 9) < 8 else ("B" if noise(x, y, 4) < 22 else "A"), x, y)
        g.named("cliff", "face_u_" + fv(x, y + 1, 2), x, y + 1)
        if tall:
            g.named("cliff", "face_l_" + ("C" if noise(x, y, 3) < 20 else "A"), x, y + 2)
        g.named("bank" if on_path else "bank_grass", "foot_" + foot(x, y + rows - 1), x, y + rows - 1)


def sea_cliff(g, x0, x1, y, faces=2, path_above=()):
    """A sea cliff from y: brink (or the path's brink), faces, foot in the sea."""
    for x in range(x0, x1 + 1):
        key = "cliff_path" if g.at(x, y - 1) in ("path", "road") or x in path_above else "cliff_brink"
        g.named(key, "bite" if noise(x, y, 13) < 7 else ("B" if noise(x, y, 6) < 20 else "A"), x, y)
        for i in range(faces):
            v = fv(x, y + 1 + i, 7 + i)
            if i % 2 == 1 and v == "B" and noise(x, y, 77) < 70:
                v = "A"
            g.named("cliff", ("face_u_" if i % 2 == 0 else "face_l_") + v, x, y + 1 + i)
        g.named("cliff", "foot_" + foot(x, y + 1 + faces), x, y + 1 + faces)


def woods(g, mix=(34, 42, 60, 64), xmax=None):
    """Fill 'wood' with pines, kermes oak, rock and boulders, top down, so the
    tree line staggers; every woods cell is solid."""
    W, H = g.W, g.H
    xmax = W if xmax is None else xmax

    def room(x, y, w, h):
        if x < 0 or x + w > xmax:
            return False
        return all(g.g[cy][cx] == "wood" and not g.fixed[cy, cx]
                   for cy in range(max(y, 0), min(y + h, H)) for cx in range(x, x + w)) and y + h - 1 >= 0

    for y in range(-2, H):
        for x in range(0, W):
            if 0 <= y and (g.fixed[y, x] or g.g[y][x] != "wood"):
                continue
            n = noise(x, y, 21)
            if n < mix[0] and room(x, y, 2, 3):
                g.piece("pine_tall", x, y, block_t=True, kind="woods")
            elif n < mix[1] and room(x, y, 3, 3):
                g.piece("pine_lean" if noise(x, y, 3) < 50 else "pine_lean_w", x, y, block_t=True, kind="woods")
            elif y >= 0 and n < mix[2] and room(x, y, 1, 2):
                g.piece("pine_young", x, y, block_t=True, kind="woods")
            elif y >= 0 and n < mix[3] and room(x, y, 2, 2):
                g.piece("boulders", x, y, kind="woods")
    for y in range(H):
        for x in range(W):
            if g.fixed[y, x] or g.g[y][x] != "wood":
                continue
            n = noise(x, y, 22)
            if n < 30 and y + 1 < H and g.g[y + 1][x] == "wood" and not g.fixed[y + 1, x] and x < xmax:
                g.piece("pine_young", x, y, block_t=True, kind="woods")
                g.solid[y + 1, x] = True
            else:
                g.piece("oak" if n < 78 else "rock", x, y, kind="woods")
            g.solid[y, x] = True


def massif(g, kind="mass"):
    """Bare rock in bulk: every column of 'mass' becomes a cliff in strata,
    a brink on top, faces down its height and a scree foot at the bottom, so
    big rock reads as one wall of limestone and not as scattered stones. A
    mass's open sides take Skiron's side pieces."""
    W, H = g.W, g.H

    def m(x, y):
        return 0 <= x < W and 0 <= y < H and g.g[y][x] == kind

    for x in range(W):
        y = 0
        while y < H:
            if not m(x, y) or g.fixed[y, x]:
                y += 1
                continue
            y0 = y
            while y < H and m(x, y) and not g.fixed[y, x]:
                y += 1
            y1 = y - 1
            for yy in range(y0, y1 + 1):
                top = yy == y0 and y0 > 0
                bottom = yy == y1 and y1 < H - 1
                open_w, open_e = not m(x - 1, yy) and x > 0, not m(x + 1, yy) and x < W - 1
                if top:
                    g.named("cliff_brink", "B" if noise(x, yy, 4) < 22 else "A", x, yy)
                elif bottom:
                    below = g.at(x, yy + 1)
                    g.named("bank" if below in ("path", "road", "scree") else "bank_grass",
                            "foot_" + foot(x, yy), x, yy)
                elif open_w and not open_e:
                    g.named("cliff_side", "side_w", x, yy)
                elif open_e and not open_w:
                    g.named("cliff_side", "side_e", x, yy)
                else:
                    face = "face_u_" if (yy - y0) % 2 else "face_l_"
                    n = noise(x, yy, 11)
                    var = ("B" if n < 16 else "C" if n < 30 else "A") if face == "face_u_" else ("C" if n < 20 else "A")
                    g.named("cliff", face + var, x, yy)
                g.solid[yy, x] = True


def rockland(g, kind="crag"):
    """Fill bare-rock ground ('crag') with boulders and rocks, all solid: the
    timberline's scree and outcrops."""
    W, H = g.W, g.H
    for y in range(H):
        for x in range(W):
            if g.fixed[y, x] or g.g[y][x] != kind:
                continue
            if noise(x, y, 41) < 30 and g.free(x, y, 2, 2, (kind,)):
                g.piece("boulders", x, y, kind="crag")
                for j in range(2):
                    for i in range(2):
                        g.solid[y + j, x + i] = True
    for y in range(H):
        for x in range(W):
            if g.fixed[y, x] or g.g[y][x] != kind:
                continue
            n = noise(x, y, 42)
            g.piece("rock" if n < 65 else "oak", x, y, kind="crag")
            g.solid[y, x] = True


def ground(g, thyme=0):
    """Paint the open ground by shape: the paved road (Skiron's), the aethos
    path patch, tall grass with Skiron's soft edges, scree, grass."""
    road = g.cat["road"]
    tall = g.cat["tall"]
    thyme_id = g.cat["tall_thyme"]["ids"][0][0]
    roadm = g.region(("road",))
    tallm = g.region(("tall",))
    for y in range(g.H):
        for x in range(g.W):
            if g.fixed[y, x]:
                continue
            k = g.g[y][x]
            if k == "road":
                key = g.shape_key(roadm, x, y)
                full = "1|11111111"
                if key == full:
                    n = noise(x, y, 17)
                    name = "mid2" if n < 14 else "mid3" if n < 24 else "mid"
                elif key in road["names"]:
                    name = key
                else:
                    g.missing.add(f"road {key}@{x},{y}")
                    name = "mid"
                cx, cy = road["names"][name]
                g.set(x, y, road["ids"][cy][cx], False, "road")
                g.fixed[y, x] = False
            elif k == "path":
                def out(dx, dy):
                    X, Y = x + dx, y + dy
                    return g.inside(X, Y) and g.g[Y][X] in ("grass", "tall", "flowers")
                n, s, w, e = out(0, -1), out(0, 1), out(-1, 0), out(1, 0)
                v = "t" if n and not s else "b" if s and not n else ""
                h = "l" if w and not e else "r" if e and not w else ""
                g.set(x, y, A_PATH[(v + h) or "c"], False, "path")
                g.fixed[y, x] = False
            elif k == "tall":
                key = g.shape_key(tallm, x, y)
                if key == "1|11111111":
                    mid = thyme_id if thyme and noise(x, y, 9) < thyme else A_TALL
                elif key in tall["names"]:
                    cx, cy = tall["names"][key]
                    mid = tall["ids"][cy][cx]
                else:
                    g.missing.add(f"tall {key}@{x},{y}")
                    mid = A_TALL
                g.set(x, y, mid, False, "tall")
                g.fixed[y, x] = False
            elif k == "scree":
                n = noise(x, y, 31)
                if n < 30:
                    g.piece("pebbles", x, y, kind="scree")
                else:
                    g.set(x, y, A_GRASS, False, "grass")
                g.fixed[y, x] = False
                g.solid[y, x] = False
            elif k == "sea":
                g.set(x, y, A_SEA, False, "sea", water=True)
            elif k in ("grass", "flowers", "dry"):
                n = noise(x, y, 51)
                if k == "flowers" and n < 40:
                    g.set(x, y, A_FLOWERS, False, "grass")
                elif k == "dry" and n < 12:
                    g.piece("dry_grass", x, y, kind="grass")
                    g.solid[y, x] = False
                elif k != "flowers" and n < 4:
                    g.piece("thyme", x, y, kind="grass")
                    g.solid[y, x] = False
                else:
                    g.set(x, y, A_GRASS, False, "grass")
                g.fixed[y, x] = False


# ---------------------------------------------------------------------------
# Review renders
# ---------------------------------------------------------------------------

def _renderer(primary, secondary):
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R.Renderer(R.Tileset(R.resolve_tileset(primary, syms)), R.Tileset(R.resolve_tileset(secondary, syms)))


def _sprite(gfx, facing):
    from PIL import Image
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
        name = gfx[len("OBJ_EVENT_GFX_SPECIES("):-1].lower()
        p = ROOT / f"graphics/pokemon/{name}/overworld.png"
        sheet, fw = Image.open(p), None
        fw = sheet.height
    elif gfx == "OBJ_EVENT_GFX_ITEM_BALL":
        jar = ROOT / "graphics/object_events/pics/misc/ichor_item_jar.png"
        sheet, fw = Image.open(jar if jar.exists() else ROOT / "graphics/object_events/pics/misc/item_ball.png"), 16
    elif gfx in ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "OBJ_EVENT_GFX_BREAKABLE_ROCK"):
        sheet = Image.open(ROOT / f"graphics/object_events/pics/misc/{gfx[len('OBJ_EVENT_GFX_'):].lower()}.png")
        fw, facing = 16, "DOWN"
    elif gfx.startswith(GFX):
        p = ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png"
        if not p.exists():
            p = ROOT / f"graphics/object_events/pics/misc/ichor/{gfx[len(GFX):].lower()}.png"
        sheet = Image.open(p)
        fw = 16 if sheet.width >= 32 else sheet.width
        if gfx[len(GFX):].startswith("STATUE_"):
            fw = sheet.width                  # the statues of the Twelve: one 32x64 frame
    else:
        raise FileNotFoundError(gfx)
    frame = 0 if gfx == "OBJ_EVENT_GFX_ITEM_BALL" else {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}.get(facing, 0)
    if (frame + 1) * fw > sheet.width:
        frame = 0
    fh = sheet.height
    crop = sheet.crop((frame * fw, 0, frame * fw + fw, fh))
    spr = crop.convert("RGBA")
    if sheet.mode == "P":
        idx, px = crop.load(), spr.load()
        for j in range(fh):
            for i in range(fw):
                if idx[i, j] == 0:
                    px[i, j] = (0, 0, 0, 0)
    if facing == "RIGHT":
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    return spr, fw, fh


def render(g, out_dir, views=(), tag=""):
    """Write <name><tag>.png (2x, people on), and one native 240x160 image per
    15x10 view (player at the view's center), plus a contact sheet."""
    from PIL import Image, ImageDraw
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    r = _renderer(g.primary, g.secondary)
    import render_map as R
    img = R.render_blocks(r, g.blockdata().ravel(), g.W).convert("RGBA")
    for o in g.events["object_events"]:
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE_" in o["movement_type"] else "DOWN"
        try:
            spr, fw, fh = _sprite(o["graphics_id"], facing)
        except (FileNotFoundError, OSError):
            continue
        img.alpha_composite(spr, (o["x"] * 16 + 8 - fw // 2, o["y"] * 16 + 16 - fh))
    img.convert("RGB").resize((img.width * 2, img.height * 2), Image.NEAREST).save(out_dir / f"{g.name}{tag}.png")
    shots = []
    for label, cx, cy in views:
        x0 = min(max(cx - 7, 0), max(g.W - 15, 0)) * 16
        y0 = min(max(cy - 5, 0), max(g.H - 10, 0)) * 16
        crop = img.crop((x0, y0, x0 + 240, y0 + 160)).convert("RGB")
        crop.save(out_dir / f"{g.name}{tag}_{label}.png")
        shots.append((label, crop))
    if shots:
        cols = 3
        rows = (len(shots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 248, rows * 176), (24, 24, 30))
        d = ImageDraw.Draw(sheet)
        for i, (label, crop) in enumerate(shots):
            x, y = (i % cols) * 248 + 4, (i // cols) * 176 + 14
            sheet.paste(crop, (x, y))
            d.text((x, y - 12), label, fill=(230, 220, 180))
        sheet.save(out_dir / f"{g.name}{tag}_screens.png")
    return out_dir / f"{g.name}{tag}.png"
