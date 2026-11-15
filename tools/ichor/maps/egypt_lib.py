"""Shared code for Egypt's outdoor maps in the Oikoumene (aethos + kemet):
naukratis.py, pharos.py, delta_reeds.py and memphis.py.

- Grid: metatile ids and collision per cell; kemet pieces placed by catalog key and
  part name (build/kemet/catalog.json, from tools/ichor/art/kemet_build.py).
- paint(): lays a map's ASCII ground plan (see PLAN_KEY), choosing every edge piece
  from its neighbours, as the slice's builders do.
- Events: obj(), sign(), hidden(), item_ball(), trainer(); map.json writing.
- Checks: warps on doors, people on walkable ground, everyone and every sign
  reachable and readable, seam strips aethos-only, and for routes the forced grass
  bands and the mandatory trainers' sight lines (Walk, from route1.py's method).
- Rendering: 2x renders, a collision-and-events overlay, and GBA-screen crops.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/kemet/catalog.json"
SECONDARY = "kemet"

# ---------------------------------------------------------------------------
# aethos ids (TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
GRASS_SHADE = 0x01C
TALL_GRASS = 0x00D
FLOWERS = 0x004
SEA = 0x170
STELE = 0x003
BOULDER = 0x0E0
BOULDER_SAND = 0x0E2
SEA_ROCKS = (0x0C5, 0x0CD, 0x18C, 0x194)
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}
SAND = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "c": 0x124, "r": 0x125,
        "bl": 0x12B, "b": 0x12C, "br": 0x12D,
        "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER"}
DOOR_BEHAVIORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_SOUTH_ARROW_WARP"}
SOLID = 1 << 10
SEAM_ROWS, SEAM_COLS = 6, 8           # MAP_DESIGN.md §5


def behavior_names():
    txt = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    out, v = {}, 0
    for name, val in re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", txt, re.M):
        if val:
            v = int(val, 0)
        out[v] = name
        v += 1
    return out


MB = behavior_names()
AETHOS_ATTR = np.fromfile(ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin", "<u2")
KEMET_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/kemet/porytiles_bin/metatile_attributes.bin", "<u2")


def behavior(mid):
    a = AETHOS_ATTR[mid] if mid < 0x200 else (KEMET_ATTR[mid - 0x200] if mid - 0x200 < len(KEMET_ATTR) else 0)
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    """A stable pseudo-random number in [0, 1) for a map cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def catalog():
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run tools/ichor/art/kemet_build.py --no-compile")
    return {s["key"]: s for s in json.loads(CAT.read_text())}


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, w, h, name):
        self.w, self.h, self.name = w, h, name
        self.mid = np.full((h, w), GRASS, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.cat = catalog()
        self.plan = None

    def set(self, x, y, mid, solid=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def k(self, key, part=None, cx=0, cy=0):
        s = self.cat[key]
        if part is not None:
            cx, cy = s["names"][part]
        return s["ids"][cy][cx]

    def part(self, key, part, x, y, solid=None):
        s = self.cat[key]
        cx, cy = s["names"][part]
        code = s["walk"][cy][cx]
        self.set(x, y, s["ids"][cy][cx], code == "X" if solid is None else solid)

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place a kemet structure (or part of one); collision follows its walk grid."""
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                code = s["walk"][cy + j][cx + i]
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], code == "X")

    def block(self, rows, x, y, solid=True):
        for j, r in enumerate(rows):
            for i, m in enumerate(r):
                if m is not None:
                    self.set(x + i, y + j, m, solid)

    def house(self, x, y, recipe):
        """Lay a house from the kit: three rows of part names (None to skip)."""
        for j, row in enumerate(recipe):
            for i, n in enumerate(row):
                if n is not None:
                    self.part("house", n, x + i, y + j)

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def ground_at(self, x, y):
        return self.plan[y][x] if self.plan and 0 <= y < len(self.plan) and 0 <= x < len(self.plan[0]) else None

    def palm(self, x, y, young=False):
        """A date palm on whatever the plan has there (grass, sand or mud)."""
        foot = self.ground_at(x, y + (1 if young else 2))
        kind = {"s": "_sand", "d": "_sand", "m": "_mud", "r": "_mud"}.get(foot, "")
        if young:
            self.put("palm_young" + ("_sand" if kind == "_sand" else ""), x, y)
        else:
            self.put("palm" + kind, x, y)

    def reach_from(self, start, extra=()):
        return reachable(encode(self), start, extra)


class Plan:
    """A ground plan, one character a cell (PLAN_KEY), filled by rectangles."""

    def __init__(self, w, h, fill="g"):
        self.w, self.h = w, h
        self.rows = [[fill] * w for _ in range(h)]

    def fill(self, x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.rows[y][x] = ch

    def cells(self, cells, ch):
        for (x, y) in cells:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.rows[y][x] = ch

    def __getitem__(self, y):
        return self.rows[y]

    def __len__(self):
        return self.h

    def dump(self):
        return "\n".join("".join(r) for r in self.rows)


def wall(g, cells, skip_faces=()):
    """White Walls: a top on every cell, joined to its neighbours, and a face south
    of every top that has no wall below (unless listed in skip_faces)."""
    S = set(cells)
    for (x, y) in S:
        n, s_, w, e = ((x, y - 1) in S, (x, y + 1) in S, (x - 1, y) in S, (x + 1, y) in S)
        g.part("wall", "top_%d%d%d%d" % (n, s_, w, e), x, y, solid=True)
    faces = {(x, y + 1) for (x, y) in S if (x, y + 1) not in S} - set(skip_faces)
    face_row(g, faces)


def face_row(g, faces):
    F = set(faces)
    for (x, y) in F:
        g.part("wall", "face_%d%d" % ((x - 1, y) in F, (x + 1, y) in F), x, y, solid=True)


def edge_key(n, s_, w_, e, nw, ne, sw, se):
    """Which edge piece a region cell needs, from which neighbours lie outside it."""
    if n and w_:
        return "tl"
    if n and e:
        return "tr"
    if s_ and w_:
        return "bl"
    if s_ and e:
        return "br"
    if n:
        return "t"
    if s_:
        return "b"
    if w_:
        return "l"
    if e:
        return "r"
    if nw:
        return "in_nw"
    if ne:
        return "in_ne"
    if sw:
        return "in_sw"
    if se:
        return "in_se"
    return "c"


def neighbours(plan, x, y, outside, edge_outside=False):
    h, w = len(plan), len(plan[0])

    def out(dx, dy):
        x2, y2 = x + dx, y + dy
        if not (0 <= x2 < w and 0 <= y2 < h):
            return edge_outside
        return plan[y2][x2] in outside
    return (out(0, -1), out(0, 1), out(-1, 0), out(1, 0), out(-1, -1), out(1, -1), out(-1, 1), out(1, 1))


# ---------------------------------------------------------------------------
# painting a plan
# ---------------------------------------------------------------------------
#
#   g meadow          G aethos tall grass (barley; not used in Egypt's routes)
#   r papyrus reeds (encounters) on mud      R papyrus reeds on the meadow
#   d dune grass on sand (encounters)        m black mud
#   P papyrus thicket (solid)                ~ open water       w water with lotus
#   s sand            p limestone path       q quay             f flowers
#   B buildings and pieces placed afterwards: painted as meadow, then covered
#   o open water that must stay aethos-only (the seam strips): plain sea
PLAN_KEY = "gGrRdmP~wspqfBo"
WATER = "~wo"
MUDLIKE = "mrP"


def paint(g, plan):
    plan = [list(r) for r in plan]
    g.plan = plan
    H, W = len(plan), len(plan[0])
    assert H == g.h and W == g.w, (g.name, H, W, g.h, g.w)
    for y in range(H):
        assert len(plan[y]) == W, f"{g.name} plan row {y} is {len(plan[y])} wide"
        for x in range(W):
            c = plan[y][x]
            assert c in PLAN_KEY, (g.name, x, y, c)
            if c in "~o":
                g.set(x, y, SEA)
            elif c == "w":
                g.set(x, y, g.k("lotus", "a" if hashed(x, y, 3) < 0.5 else "b"))
            elif c == "q":
                key = edge_key(*neighbours(plan, x, y, WATER))
                if key == "c":
                    g.set(x, y, g.k("quay", "c"))
                else:
                    g.set(x, y, g.k("quay", key))
            elif c == "m":
                key = edge_key(*neighbours(plan, x, y, WATER))
                if key != "c":
                    g.set(x, y, g.k("bank", key))
                    continue
                key = edge_key(*neighbours(plan, x, y, "gGRfpsBd"))
                if key != "c":
                    g.set(x, y, g.k("mud_grass", key))
                    continue
                r = hashed(x, y, 5)
                g.set(x, y, g.k("mud", "c2" if r < 0.06 else "c4" if r < 0.12 else "c"))
            elif c == "r":
                g.set(x, y, g.k("reeds", "a" if (x + y) % 2 else "b"))
            elif c == "R":
                g.set(x, y, g.k("reeds", "g"))
            elif c == "d":
                g.set(x, y, g.k("dune_grass", "a" if (x + y) % 2 else "b"))
            elif c == "P":
                n, s_, w_, e, *_ = neighbours(plan, x, y, PLAN_KEY.replace("P", ""))
                key = {(1, 0, 1, 0): "nw", (1, 0, 0, 0): "n", (1, 0, 0, 1): "ne",
                       (0, 0, 1, 0): "w", (0, 0, 0, 0): "c", (0, 0, 0, 1): "e",
                       (0, 1, 1, 0): "sw", (0, 1, 0, 0): "s", (0, 1, 0, 1): "se"}.get(
                    (int(n), int(s_), int(w_), int(e)))
                assert key, f"{g.name}: thicket at ({x},{y}) is under 2 cells thick"
                if key == "c" and hashed(x, y, 8) < 0.4:
                    key = "c2"
                g.set(x, y, g.k("thicket", key), True)
            elif c == "s":
                key = edge_key(*neighbours(plan, x, y, WATER))
                if key == "c":
                    n, s_, w_, e, *_ = neighbours(plan, x, y, "gGRfB")
                    soft = edge_key(n, s_, w_, e, *[False] * 4)
                    g.set(x, y, SAND_GRASS[soft] if soft != "c" else SAND["c"])
                else:
                    g.set(x, y, SAND[key])
            elif c == "p":
                n, s_, w_, e, *_ = neighbours(plan, x, y, "gGRf")
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e, *[False] * 4)
                g.set(x, y, PATH.get(key, PATH["c"]))
            elif c == "f":
                g.set(x, y, FLOWERS)
            elif c == "G":
                g.set(x, y, TALL_GRASS)
            else:
                g.set(x, y, GRASS)
    # thicket fringes: the top rank's umbels over the cell north of every north edge
    for y in range(1, H):
        for x in range(W):
            if plan[y][x] == "P" and plan[y - 1][x] != "P":
                above = plan[y - 1][x]
                if above == "m":
                    if int(g.mid[y - 1, x]) == g.k("mud", "c") or int(g.mid[y - 1, x]) in (
                            g.k("mud", "c2"), g.k("mud", "c4")):
                        g.set(x, y - 1, g.k("thicket", "fringe_mud" if x % 2 else "fringe_mud2"))
                elif above in "gB" and int(g.mid[y - 1, x]) == GRASS:
                    g.set(x, y - 1, g.k("thicket", "fringe_grass"))


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
        local_id=None, rx=0, ry=0, item=None):
    e = {
        "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
        "movement_range_x": rx, "movement_range_y": ry,
        "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag,
    }
    if local_id:
        e = {"local_id": local_id, **e}
    return e


def item_ball(x, y, item, flag):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag, item=item)


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag}


def warp(x, y, dest_map, dest_warp):
    return {"x": x, "y": y, "elevation": 0, "dest_map": dest_map, "dest_warp_id": str(dest_warp)}


def trigger(x, y, script, var="VAR_TEMP_1", value="0"):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": value,
            "script": script}


def write_map_json(name, events, connections=None, **fields):
    path = ROOT / "data/maps" / name / "map.json"
    m = json.loads(path.read_text())
    m.update(fields)
    m["connections"] = connections or None
    for k in ("object_events", "warp_events", "coord_events", "bg_events"):
        m[k] = events.get(k, [])
    path.write_text(json.dumps(m, indent=2) + "\n")


# ---------------------------------------------------------------------------
# layouts
# ---------------------------------------------------------------------------

def encode(g):
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mid[y, x])
            water = behavior(mid) in SURF_BEHAVIORS
            elev = 1 if water else 3
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | (elev << 12)
    return out


def write_layout(g, folder, layout_id, border):
    d = ROOT / "data/layouts" / folder
    d.mkdir(parents=True, exist_ok=True)
    encode(g).astype("<u2").tofile(d / "map.bin")
    np.array(border, np.uint16).astype("<u2").tofile(d / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    text = path.read_text()
    pat = re.compile(r'("id": "%s",\s*"name": "[^"]+",\s*"width": )\d+(,\s*"height": )\d+'
                     r'(,\s*"primary_tileset": "[^"]+",\s*"secondary_tileset": ")[^"]+"' % layout_id)
    new, n = pat.subn(lambda m: f'{m.group(1)}{g.w}{m.group(2)}{g.h}{m.group(3)}gTileset_Kemet"', text)
    assert n == 1, f"{layout_id} not found in layouts.json"
    if new != text:
        path.write_text(new)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 != 1


def reachable(blocks, start, extra_open=()):
    seen, q = {start}, deque([start])
    h, w = blocks.shape
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in seen and (walkable(blocks, *p) or p in extra_open):
                seen.add(p)
                q.append(p)
    return seen


FLYERS = ("WINGULL", "SPECIES(WINGULL)", "SPECIES(PELIPPER)")


def check_map(name, start, events, seams=(), water_ok=()):
    """The common checks. seams: (kind, cells, why): kind 'rows' or 'cols', the rows or
    columns that must use aethos only. water_ok: object locals allowed on water."""
    errors = []
    lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    layout = json.loads((ROOT / "data/maps" / name / "map.json").read_text())["layout"]
    entry = next(l for l in lay["layouts"] if l.get("id") == layout)
    w = entry["width"]
    blocks = np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, w)
    ev = events
    warps = [(w_["x"], w_["y"]) for w_ in ev["warp_events"]]
    starts = start if isinstance(start, list) else [start]
    reach = set()
    for s in starts:
        reach |= reachable(blocks, s, extra_open=set(warps))
    hh, ww = blocks.shape
    for (x, y) in warps:
        b = behavior(int(blocks[y, x]) & 0x3FF)
        if b not in DOOR_BEHAVIORS:
            errors.append(f"{name}: warp at ({x},{y}) is on {b}, not a door")
        if (x, y) not in reach:
            errors.append(f"{name}: warp at ({x},{y}) is unreachable")
    for y in range(hh):
        for x in range(ww):
            m = int(blocks[y, x]) & 0x3FF
            if behavior(m) in DOOR_BEHAVIORS and not (blocks[y, x] >> 10 & 3) and (x, y) not in warps:
                errors.append(f"{name}: door metatile at ({x},{y}) has no warp")
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if any(f in o["graphics_id"] for f in FLYERS) or o.get("local_id") in water_ok:
            continue
        if not walkable(blocks, x, y):
            errors.append(f"{name}: object {o.get('local_id', o['graphics_id'])} at ({x},{y}) stands on a solid cell")
    for t in ev["coord_events"]:
        if (t["x"], t["y"]) not in reach:
            errors.append(f"{name}: coord event at ({t['x']},{t['y']}) is unreachable")
    still = blocks.copy()
    for o in ev["object_events"]:
        if o["movement_type"] != "MOVEMENT_TYPE_WANDER_AROUND" and 0 <= o["y"] < hh and 0 <= o["x"] < ww:
            still[o["y"], o["x"]] |= SOLID
    reach_still = set()
    for s in starts:
        reach_still |= reachable(still, s, extra_open=set(warps))
    targets = [(b["x"], b["y"], f"{b['type']} event") for b in ev["bg_events"]]
    targets += [(o["x"], o["y"], o.get("local_id", o["graphics_id"])) for o in ev["object_events"]
                if not any(f in o["graphics_id"] for f in FLYERS) and o["script"] not in ("0x0", "0")]
    for (x, y, what) in targets:
        if what.startswith("hidden_item") and (x, y) in reach_still:
            continue
        fronts = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0))]
        if not any(p in reach_still for p in fronts):
            errors.append(f"{name}: the {what} at ({x},{y}) can't be reached past the people standing still")
    for (kind, cells, why) in seams:
        for c in cells:
            rng = [(x, c) for x in range(ww)] if kind == "rows" else [(c, y) for y in range(hh)]
            for (x, y) in rng:
                m = int(blocks[y, x]) & 0x3FF
                if m >= 0x200:
                    errors.append(f"{name}: ({x},{y}) is kemet metatile 0x{m:03X}, within the {why} "
                                  f"seam's band; use aethos there")
    return errors, reach, blocks


def seam_open(blocks, edge, cells, water=False):
    """The cells of one edge that a walker (or a surfer, water=True) can cross."""
    h, w = blocks.shape
    out = []
    for i in cells:
        x, y = {"n": (i, 0), "s": (i, h - 1), "w": (0, i), "e": (w - 1, i)}[edge]
        v = int(blocks[y, x])
        if v >> 10 & 3:
            continue
        if water and v >> 12 == 1:
            out.append(i)
        elif not water and v >> 12 != 1:
            out.append(i)
    return out


# ---------------------------------------------------------------------------
# routes: forced grass and sight lines (route1.py's Walk)
# ---------------------------------------------------------------------------

STEPS = ((0, -1), (1, 0), (0, 1), (-1, 0))
FACING = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0),
          "MOVEMENT_TYPE_FACE_UP": (0, -1), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0),
          "MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_LEFT": (-1, 0)}


class Walk:
    """Each cell of a built map: 'solid', 'grass' (tall grass), 'water' or 'open'.
    Walkers don't surf: the routes must work on foot."""

    def __init__(self, blocks):
        self.blocks, (self.h, self.w) = blocks, blocks.shape
        self.kind = {}
        for y in range(self.h):
            for x in range(self.w):
                v = int(blocks[y, x])
                b = behavior(v & 0x3FF)
                if v >> 10 & 3:
                    k = "solid"
                elif v >> 12 == 1:
                    k = "water"
                elif b == "MB_TALL_GRASS":
                    k = "grass"
                else:
                    k = "open"
                self.kind[(x, y)] = k

    def cost(self, starts, goals, avoid=frozenset(), weight=None):
        weight = weight or (lambda c: 1 if self.kind[c] == "grass" else 0)
        ok = lambda c: c in self.kind and self.kind[c] in ("open", "grass") and c not in avoid
        dist, dq = {}, deque()
        for s in starts:
            if ok(s):
                dist[s] = weight(s)
                dq.append(s)
        dq = deque(sorted(dq, key=lambda c: dist[c]))
        while dq:
            c = dq.popleft()
            for dx, dy in STEPS:
                n = (c[0] + dx, c[1] + dy)
                if not ok(n):
                    continue
                w = weight(n)
                if n not in dist or dist[c] + w < dist[n]:
                    dist[n] = dist[c] + w
                    (dq.appendleft if w == 0 else dq.append)(n)
        best = [dist[g] for g in goals if g in dist]
        self.dist = dist
        return min(best) if best else None

    def grass_parts(self):
        seen, parts = set(), []
        for c, k in self.kind.items():
            if k != "grass" or c in seen:
                continue
            part, todo = set(), [c]
            seen.add(c)
            while todo:
                x, y = todo.pop()
                part.add((x, y))
                for dx, dy in STEPS:
                    n = (x + dx, y + dy)
                    if self.kind.get(n) == "grass" and n not in seen:
                        seen.add(n)
                        todo.append(n)
            parts.append(part)
        return parts

    def forced_bands(self, starts, goals):
        bands = []
        for part in self.grass_parts():
            if self.cost(starts, goals, avoid=part) is None:
                depth = self.cost(starts, goals, weight=lambda c, p=part: 1 if c in p else 0)
                bands.append((part, depth))
        return sorted(bands, key=lambda b: min(y for _, y in b[0]))

    def sight(self, x, y, facing, reach):
        dx, dy = FACING[facing]
        cells = []
        for i in range(1, reach + 1):
            c = (x + dx * i, y + dy * i)
            if self.kind.get(c) not in ("open", "grass"):
                break
            cells.append(c)
        return cells


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def render(layout_id, name, w, h, out_png, scale=2):
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), layout_id, "--scale",
                    str(scale), "-o", str(out_png)], check=True, stdout=subprocess.DEVNULL)
    return out_png


def overlay(png, name, w, out, scale=2, events=None, marks=()):
    """Tint impassable cells red and water blue, and draw the map's events."""
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    blocks = np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, w)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16 * scale
    for y, row in enumerate(blocks):
        for x, b in enumerate(row):
            if b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif b >> 12 == 1:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 80, 255, 50))
            elif behavior(int(b) & 0x3FF) == "MB_TALL_GRASS":
                d.rectangle([x * c + 2, y * c + 2, x * c + c - 3, y * c + c - 3], outline=(0, 255, 0, 160))
    ev = events or json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
    for o in ev["object_events"]:
        col = (255, 0, 255, 255) if o["trainer_type"] != "TRAINER_TYPE_NONE" else (255, 255, 0, 255)
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=col, width=2)
        if o["trainer_type"] != "TRAINER_TYPE_NONE":
            dx, dy = FACING[o["movement_type"]]
            n = int(o["trainer_sight_or_berry_tree_id"])
            x0, y0 = o["x"] * c + c // 2, o["y"] * c + c // 2
            d.line([x0, y0, x0 + dx * n * c, y0 + dy * n * c], fill=(255, 0, 255, 200), width=3)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=2)
    for t in ev["coord_events"]:
        d.rectangle([t["x"] * c + 6, t["y"] * c + 6, t["x"] * c + c - 7, t["y"] * c + c - 7], fill=(255, 0, 255, 160))
    for b in ev["bg_events"]:
        col = (120, 255, 120, 255) if b["type"] == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4], fill=col, width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4], fill=col, width=2)
    for (x, y, col) in marks:
        d.rectangle([x * c + 1, y * c + 1, x * c + c - 2, y * c + c - 2], outline=col, width=3)
    Image.alpha_composite(im, lay).save(out)


def crops(name, w, h, out_dir, stem, screens, margin=8, scale=2):
    """GBA-screen views (15x10 tiles, the player on the 8th column, 5th row) from the
    map padded with its border, tiled into one sheet."""
    from PIL import Image
    out_dir = Path(out_dir)
    blocks = np.fromfile(ROOT / f"data/layouts/{name}/map.bin", "<u2").reshape(h, w)
    bord = np.fromfile(ROOT / f"data/layouts/{name}/border.bin", "<u2").reshape(2, 2)
    big = np.empty((h + 2 * margin, w + 2 * margin), np.uint16)
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            big[y, x] = bord[y % 2, x % 2]
    big[margin:margin + h, margin:margin + w] = blocks
    tmp = out_dir / f"{stem}_padded.bin"
    big.astype("<u2").tofile(tmp)
    png = out_dir / f"{stem}_padded.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", SECONDARY,
                    "--scale", str(scale), "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 16 * scale
    out = []
    for nm, (px, py) in screens.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        out.append(im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c)))
    cols = 2
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(out) // cols) * (10 * c + 8) - 8),
                      (24, 24, 32))
    for i, crop in enumerate(out):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out_dir / f"{stem}_screens.png")
    tmp.unlink()
    png.unlink()


def report(errors, label):
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(f"{label}: {len(errors)} check(s) failed")
    print(f"{label}: layout written, checks pass")
