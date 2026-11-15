#!/usr/bin/env python3
"""Shared reader for Ichor's map tools: map_audit.py and tests/slice_map_audit.py.

Reads the data the game builds from: data/maps/<Map>/map.json, each layout's
map.bin (metatile id, collision and elevation per cell), each tileset's
metatile_attributes.bin (behaviors) and src/data/wild_encounters.json. It
works on any tree laid out like this repo, so it can read a branch export or
upstream's Emerald maps at the merge-base as well as the working tree.

Python 3 stdlib only.
"""
import json
import re
from collections import defaultdict, deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
NUM_PRIMARY = 512
SCREEN_W, SCREEN_H = 15, 10
# Engine maps the expansion still needs, which Ichor doesn't build or audit.
UPSTREAM_PREFIXES = ("BattleFrontier_", "BattlePyramidSquare", "TrainerHill_")

# Land encounter cells. Ash grass is Route 113's tall grass; the cycling-road
# slope grass is the same thing on a slope.
GRASS = {"MB_TALL_GRASS", "MB_LONG_GRASS", "MB_ASHGRASS", "MB_CYCLING_ROAD_PULL_DOWN_GRASS"}
OTHER_LAND_ENCOUNTER = {"MB_CAVE", "MB_INDOOR_ENCOUNTER", "MB_DEEP_SAND", "MB_FOOTPRINTS"}
# Water a surfer can cross (metatile_behavior.c's TILE_FLAG_SURFABLE, less waterfalls and dive-only water).
WATER = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_SOOTOPOLIS_DEEP_WATER",
         "MB_OCEAN_WATER", "MB_SEAWEED", "MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT",
         "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT", "MB_FAST_WATER", "MB_CYCLING_ROAD_WATER"}
NEVER_STAND = {"MB_WATERFALL", "MB_NO_SURFACING", "MB_SEAWEED_NO_SURFACING", "MB_ICHOR_GAP", "MISSING"}
# Objects a relic (or an HM) clears: rock smash rocks, cut trees, strength boulders.
OBSTACLE_GFX = ("BREAKABLE_ROCK", "CUTTABLE_TREE", "PUSHABLE_BOULDER")
TIMES = ("Morning", "Day", "Evening", "Night")
AREAS = ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons", "hidden_mons")
DIRS = ((0, -1, "NORTH"), (0, 1, "SOUTH"), (-1, 0, "WEST"), (1, 0, "EAST"))


class Repo:
    """One tree of map data: the working tree, a branch export or the upstream base."""

    def __init__(self, root=REPO):
        self.root = Path(root)
        self.mb = self._behaviors()
        lay = json.loads((self.root / "data/layouts/layouts.json").read_text())["layouts"]
        self.layouts = {l["id"]: l for l in lay if "id" in l}
        groups = json.loads((self.root / "data/maps/map_groups.json").read_text())
        self.names = [m for g in groups["group_order"] for m in groups[g]]
        self._json, self._maps, self._attrs, self._wild, self._ids = {}, {}, {}, None, None
        self._tilesets = self._tileset_paths()

    def _behaviors(self):
        text = (self.root / "include/constants/metatile_behaviors.h").read_text()
        names, n = {}, 0
        for line in text.splitlines():
            m = re.match(r"\s*(MB_[A-Z0-9_]+)\s*(?:=\s*(\w+))?\s*,", line)
            if m:
                if m.group(2):
                    n = int(m.group(2), 0)
                names[n] = m.group(1)
                n += 1
        return names

    def _tileset_paths(self):
        headers = (self.root / "src/data/tilesets/headers.h").read_text()
        incbins = dict(re.findall(r"(\w+)\[\]\s*=\s*INCBIN_U16\(\"([^\"]+)\"\)",
                                  (self.root / "src/data/tilesets/metatiles.h").read_text()))
        out = {}
        for sym, body in re.findall(r"const struct Tileset (\w+)\s*=\s*\{(.*?)\};", headers, re.S):
            m = re.search(r"\.metatileAttributes\s*=\s*(\w+)", body)
            if m and m.group(1) in incbins:
                out[sym] = incbins[m.group(1)]
        return out

    def attrs(self, symbol):
        if symbol not in self._attrs:
            data = (self.root / self._tilesets[symbol]).read_bytes()
            self._attrs[symbol] = [int.from_bytes(data[i:i + 2], "little") for i in range(0, len(data), 2)]
        return self._attrs[symbol]

    def map_json(self, name):
        if name not in self._json:
            self._json[name] = json.loads((self.root / f"data/maps/{name}/map.json").read_text())
        return self._json[name]

    def map(self, name):
        if name not in self._maps:
            self._maps[name] = Map(self, name)
        return self._maps[name]

    def name_of(self, map_id):
        if self._ids is None:
            self._ids = {self.map_json(n)["id"]: n for n in self.names}
        return self._ids.get(map_id)

    def script_text(self, name):
        name = self.map_json(name).get("shared_scripts_map") or name
        d = self.root / f"data/maps/{name}"
        return "".join(p.read_text(errors="replace") for p in (d / "scripts.pory", d / "scripts.inc") if p.exists())

    def wild(self):
        """map id -> time of day -> area ('land_mons', ...) -> the table's mons.

        A table's time comes from its label's suffix (_Morning, _Day, _Evening,
        _Night). An unsuffixed table is the fallback time, morning, as in Ichor's
        config (OW_TIME_OF_DAY_FALLBACK)."""
        if self._wild is None:
            self._wild = defaultdict(lambda: defaultdict(dict))
            data = json.loads((self.root / "src/data/wild_encounters.json").read_text())
            for group in data["wild_encounter_groups"]:
                if not group.get("for_maps"):
                    continue
                for e in group["encounters"]:
                    m = re.search(r"_(Morning|Day|Evening|Night)$", e.get("base_label", ""))
                    time = m.group(1) if m else "Morning"
                    for area in AREAS:
                        if area in e and e[area].get("mons"):
                            self._wild[e.get("map")][time][area] = e[area]["mons"]
        return self._wild


def is_obstacle(o):
    return any(k in o.get("graphics_id", "") for k in OBSTACLE_GFX)


def is_item_ball(o):
    return "ITEM_BALL" in o.get("graphics_id", "") or o.get("script") == "Common_EventScript_FindItem"


def is_trainer(o):
    return o.get("trainer_type") not in (None, "", "0", 0, "TRAINER_TYPE_NONE")


def is_berry_tree(o):
    return o.get("movement_type") == "MOVEMENT_TYPE_BERRY_TREE_GROWTH" or o.get("graphics_id") == "OBJ_EVENT_GFX_BERRY_TREE"


class Map:
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name
        self.json = repo.map_json(name)
        lay = repo.layouts[self.json["layout"]]
        self.w, self.h = lay["width"], lay["height"]
        raw = (repo.root / lay["blockdata_filepath"]).read_bytes()
        self.cells = [int.from_bytes(raw[i:i + 2], "little") for i in range(0, len(raw), 2)]
        self.prim = repo.attrs(lay["primary_tileset"])
        self.sec = repo.attrs(lay["secondary_tileset"])
        self.mb = repo.mb
        ev = repo.map_json(self.json["shared_events_map"]) if self.json.get("shared_events_map") else self.json
        # clones are another map's objects drawn across a seam
        self.objects = [o for o in ev.get("object_events") or [] if o.get("type") != "clone"]
        self.bgs = ev.get("bg_events") or []
        self.warps = ev.get("warp_events") or []
        self.coords = ev.get("coord_events") or []
        self.connections = self.json.get("connections") or []

    def cell(self, x, y):
        """(metatile id, collision, elevation), or None off the map."""
        if not (0 <= x < self.w and 0 <= y < self.h):
            return None
        v = self.cells[x + y * self.w]
        return v & 0x3FF, (v >> 10) & 3, v >> 12

    def behavior(self, mid):
        attrs = self.prim if mid < NUM_PRIMARY else self.sec
        i = mid if mid < NUM_PRIMARY else mid - NUM_PRIMARY
        return self.mb.get(attrs[i] & 0xFF, "?") if i < len(attrs) else "MISSING"

    def behavior_at(self, x, y):
        c = self.cell(x, y)
        return self.behavior(c[0]) if c else None

    def is_water(self, x, y):
        return self.behavior_at(x, y) in WATER

    def open(self, x, y):
        """Walkable ground, before objects (the slice audit's old test, kept for slice_grid)."""
        c = self.cell(x, y)
        if c is None or c[1]:
            return False
        b = self.behavior(c[0])
        return b not in WATER and b not in NEVER_STAND and not b.startswith("MB_JUMP")

    def people(self):
        """Objects who are always in the way. An object with a hide flag comes and
        goes, and one that wanders steps aside."""
        return {(o["x"], o["y"]) for o in self.objects if o.get("flag") in (None, "0", 0, "")
                and not int(o.get("movement_range_x") or 0) and not int(o.get("movement_range_y") or 0)}

    def obstacles(self):
        return {(o["x"], o["y"]) for o in self.objects if is_obstacle(o)}

    def edge_tiles(self, c):
        """The cells along the edge a connection leaves from: where it overlaps the neighbour."""
        d, off = c["direction"], int(c.get("offset") or 0)
        oname = self.repo.name_of(c["map"])
        ow, oh = (self.repo.map(oname).w, self.repo.map(oname).h) if oname else (1 << 20, 1 << 20)
        if d == "up":
            return [(x, 0) for x in range(self.w) if 0 <= x - off < ow]
        if d == "down":
            return [(x, self.h - 1) for x in range(self.w) if 0 <= x - off < ow]
        if d == "left":
            return [(0, y) for y in range(self.h) if 0 <= y - off < oh]
        if d == "right":
            return [(self.w - 1, y) for y in range(self.h) if 0 <= y - off < oh]
        return []  # dive and emerge connections have no edge


class Walker:
    """Moves the player one step at a time, the way the overworld does.

    It follows collision, ledges (a hop of two cells) and the elevation rule:
    a step is blocked when the player's elevation and the cell's differ and
    neither is 0 or 15, and the player takes the cell's elevation unless the
    cell, or the one they leave, is 15 (a bridge end). Surf ignores the step
    between water and the shore. Objects who are always there block the way.

      surf    the player can surf
      relics  rocks, cut trees and boulders are cleared, and Talaria gaps leapt
    """

    def __init__(self, m, surf=False, relics=False):
        self.m, self.surf, self.relics = m, surf, relics
        self.block = m.people() - (m.obstacles() if relics else set())

    def stand(self, x, y):
        c = self.m.cell(x, y)
        if c is None or c[1] or (x, y) in self.block:
            return False
        b = self.m.behavior(c[0])
        if b in WATER:
            return self.surf
        return b not in NEVER_STAND and not b.startswith("MB_JUMP")

    def starts(self, tiles):
        return [(x, y, self.m.cell(x, y)[2]) for x, y in tiles if self.stand(x, y)]

    def steps(self, x, y, e):
        m = self.m
        here = m.cell(x, y)
        for dx, dy, d in DIRS:
            nx, ny = x + dx, y + dy
            b = m.behavior_at(nx, ny)
            if b is None:
                continue
            if b == "MB_JUMP_" + d or (self.relics and b == "MB_ICHOR_GAP"):
                nx, ny = nx + dx, ny + dy
            if not self.stand(nx, ny):
                continue
            te = m.cell(nx, ny)[2]
            if m.is_water(x, y) != m.is_water(nx, ny):
                ne = te
            else:
                if e not in (0, 15) and te not in (0, 15) and te != e:
                    continue
                ne = e if (te == 15 or here[2] == 15) else te
            yield nx, ny, ne

    def reach(self, starts):
        """Every (x, y, elevation) state reachable from the start states."""
        seen = set(starts)
        q = deque(seen)
        while q:
            s = q.popleft()
            for t in self.steps(*s):
                if t not in seen:
                    seen.add(t)
                    q.append(t)
        return seen

    def graph(self, starts):
        """The step graph over every state reachable from the starts: state -> next states."""
        adj, q = {}, deque(set(starts))
        seen = set(q)
        while q:
            s = q.popleft()
            adj[s] = list(self.steps(*s))
            for t in adj[s]:
                if t not in seen:
                    seen.add(t)
                    q.append(t)
        return adj


def bfs(adj, sources):
    dist = {s: 0 for s in sources if s in adj}
    q = deque(dist)
    while q:
        s = q.popleft()
        for t in adj[s]:
            if t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)
    return dist


def reverse(adj):
    r = defaultdict(list)
    for s, nb in adj.items():
        r.setdefault(s, [])
        for t in nb:
            r[t].append(s)
    return r


def entries(m):
    """Where a player arrives: each warp (and the cell below a door) and each connected edge.
    Returns [(label, [cells])]."""
    out = []
    for i, w in enumerate(m.warps):
        out.append((f"warp {i} to {w.get('dest_map')}", [(w["x"], w["y"]), (w["x"], w["y"] + 1)]))
    for c in m.connections:
        tiles = m.edge_tiles(c)
        if tiles:
            out.append((f"{c['direction']} edge to {c['map']}", tiles))
    return out


def structural_checks(m):
    """The slice audit's checks for one map. Returns [(kind, message)].

      REACH    every NPC, item ball, sign, hidden item and story trigger can be
               reached (a trigger stood on, the rest faced from an open cell),
               walking or surfing from the map's warps and connected edges, with
               relic obstacles cleared
      WARP     every warp's destination exists, and the player lands somewhere
               they can step off (a door's cell below is open)
      EDGE     walking off a connected edge lands on an open cell of the next map
      MIXED    a metatile used both as open and as solid ground in one map: either
               a wall you can walk through or a path you can't (listed for a look)
      ONSOLID  an item ball standing on a solid cell (fine behind a counter)
    """
    repo, out = m.repo, []
    walker = Walker(m, surf=True, relics=True)
    starts = walker.starts([t for _, tiles in entries(m) for t in tiles])
    seen = {(x, y) for x, y, _ in walker.reach(starts)}

    def faceable(x, y):
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (x + dx, y + dy) in seen:
                return True
            # talked to across a counter (or a dais step that works like one)
            if m.behavior_at(x + dx, y + dy) == "MB_COUNTER" and (x + 2 * dx, y + 2 * dy) in seen:
                return True
        return False

    for o in m.objects:
        what = f"{o.get('local_id') or o.get('graphics_id')} at ({o['x']},{o['y']})"
        if o.get("script") and o["script"] != "0" and not faceable(o["x"], o["y"]):
            out.append(("REACH", f"can't stand next to {what} ({o['script']})"))
        c = m.cell(o["x"], o["y"])
        if c and c[1] and is_item_ball(o):
            out.append(("ONSOLID", f"item ball {what} sits on a solid cell"))
    for b in m.bgs:
        what = f"{b.get('type')} at ({b['x']},{b['y']}) {b.get('script') or b.get('item')}"
        if not faceable(b["x"], b["y"]) and (b["x"], b["y"]) not in seen:
            out.append(("REACH", f"can't face {what}"))
    for c in m.coords:
        if (c["x"], c["y"]) not in seen:
            out.append(("REACH", f"trigger at ({c['x']},{c['y']}) {c.get('script')} can't be stood on"))

    for w in m.warps:
        dest_id = w.get("dest_map")
        if dest_id in (None, "MAP_DYNAMIC", "MAP_UNDEFINED"):
            continue
        dname = repo.name_of(dest_id)
        if not dname:
            out.append(("WARP", f"warp at ({w['x']},{w['y']}) leads to {dest_id}, which isn't in map_groups.json"))
            continue
        dest = repo.map(dname)
        try:
            wid = int(w["dest_warp_id"])
        except (TypeError, ValueError):
            continue
        if wid >= len(dest.warps):
            out.append(("WARP", f"warp at ({w['x']},{w['y']}) names {dname} warp {wid}, which has {len(dest.warps)}"))
            continue
        dw = dest.warps[wid]
        c = dest.cell(dw["x"], dw["y"])
        b = dest.behavior(c[0]) if c else "?"
        if "DOOR" in b:
            if not dest.open(dw["x"], dw["y"] + 1):
                out.append(("WARP", f"door into {dname} ({dw['x']},{dw['y']}) has no open cell below it"))
        elif c and c[1]:
            out.append(("WARP", f"arrival in {dname} at ({dw['x']},{dw['y']}) is a solid cell ({b})"))
        elif not any(dest.open(dw["x"] + dx, dw["y"] + dy) or dest.is_water(dw["x"] + dx, dw["y"] + dy)
                     for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            out.append(("WARP", f"arrival in {dname} at ({dw['x']},{dw['y']}) is boxed in"))

    for c in m.connections:
        oname = repo.name_of(c["map"])
        if not oname:
            out.append(("EDGE", f"connects {c['direction']} to {c['map']}, which isn't in map_groups.json"))
            continue
        other, d = repo.map(oname), c["direction"]
        off = int(c.get("offset", 0))
        pairs = []
        if d in ("up", "down"):
            for x in range(m.w):
                ox = x - off
                if 0 <= ox < other.w:
                    pairs.append(((x, 0 if d == "up" else m.h - 1), (ox, other.h - 1 if d == "up" else 0)))
        elif d in ("left", "right"):
            for y in range(m.h):
                oy = y - off
                if 0 <= oy < other.h:
                    pairs.append(((0 if d == "left" else m.w - 1, y), (other.w - 1 if d == "left" else 0, oy)))
        # one line per run of neighbouring bad cells; only cells a player can reach count
        bad = [(a, b) for a, b in pairs if a in seen and m.open(*a) and not other.open(*b)]
        runs = []
        for a, b in bad:
            if runs and abs(a[0] - runs[-1][1][0][0]) + abs(a[1] - runs[-1][1][0][1]) == 1:
                runs[-1][1] = (a, b)
            else:
                runs.append([(a, b), (a, b)])
        for (a0, b0), (a1, b1) in runs:
            if a0 == a1:
                out.append(("EDGE", f"open edge cell {a0} walks {d} into solid {oname} {b0}"))
            else:
                out.append(("EDGE", f"open edge cells {a0}-{a1} walk {d} into solid {oname} {b0}-{b1}"))

    uses = {}
    for y in range(m.h):
        for x in range(m.w):
            mid, col, _ = m.cell(x, y)
            uses.setdefault(mid, [[], []])[1 if col else 0].append((x, y))
    for mid, (op, so) in sorted(uses.items()):
        if op and so:
            b = m.behavior(mid)
            minority, kind = (op, "open") if len(op) < len(so) else (so, "solid")
            out.append(("MIXED", f"metatile 0x{mid:03X} ({b}) is open {len(op)}x and solid {len(so)}x; "
                                 f"the {kind} ones: {minority[:6]}{' ...' if len(minority) > 6 else ''}"))
    return out
