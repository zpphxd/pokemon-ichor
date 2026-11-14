#!/usr/bin/env python3
"""Static checks over the slice's maps: what the playthrough can't see by walking.

Reads the same data the game builds from: data/maps/<Map>/map.json, the
layout's map.bin (metatile id, collision and elevation per cell) and each
tileset's metatile_attributes.bin (behaviors). For every slice map it checks:

  REACH     every NPC, item ball, sign, hidden item and story trigger can be
            reached (a trigger stood on, the rest faced from an open tile),
            walking from the map's warps and connected edges
  WARP      every warp's destination exists, and the player lands somewhere
            they can step off (a door's tile below is open)
  EDGE      walking off a connected edge lands on an open tile of the next map,
            and the reverse
  MIXED     a metatile used both as open and as solid ground in one map: either
            a wall you can walk through or a path you can't (listed for a look)
  ONSOLID   an NPC or item standing on a solid cell (fine behind a counter)

  tools/ichor/tests/slice_map_audit.py            (prints findings; exit 0)
"""
import json
import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAPS = ["ElaiaVillage", "ElaiaVillage_PlayersHouse_1F", "ElaiaVillage_PlayersHouse_2F", "ElaiaVillage_NeighborsHouse",
        "ElaiaVillage_Akademia", "KallisteRoute1", "KallisteRoute1_KronionHill", "AktiTown", "AktiTown_Asclepeion",
        "AktiTown_Agora", "AktiTown_FishersHouse", "AktiTown_TempleOfHestia"]
NUM_PRIMARY = 512


def behaviors():
    text = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    names, n = {}, 0
    for line in text.splitlines():
        m = re.match(r"\s*(MB_[A-Z0-9_]+)\s*(?:=\s*(\w+))?\s*,", line)
        if m:
            if m.group(2):
                n = int(m.group(2), 0)
            names[n] = m.group(1)
            n += 1
    return names


def tileset_dir(symbol):
    text = (ROOT / "src/data/tilesets/headers.h").read_text()
    m = re.search(r"const struct Tileset " + re.escape(symbol) + r"\s*=\s*\{(.*?)\};", text, re.S)
    attrs = re.search(r"\.metatileAttributes\s*=\s*(\w+)", m.group(1)).group(1)
    mt = (ROOT / "src/data/tilesets/metatiles.h").read_text()
    path = re.search(re.escape(attrs) + r"\[\]\s*=\s*INCBIN_U16\(\"([^\"]+)\"\)", mt).group(1)
    data = (ROOT / path).read_bytes()
    return [int.from_bytes(data[i:i + 2], "little") for i in range(0, len(data), 2)]


class Map:
    def __init__(self, name, layouts, mb):
        self.name = name
        self.json = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
        lay = layouts[self.json["layout"]]
        self.w, self.h = lay["width"], lay["height"]
        raw = (ROOT / lay["blockdata_filepath"]).read_bytes()
        self.cells = [int.from_bytes(raw[i:i + 2], "little") for i in range(0, len(raw), 2)]
        self.prim = tileset_dir(lay["primary_tileset"])
        self.sec = tileset_dir(lay["secondary_tileset"])
        self.mb = mb

    def cell(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return None
        v = self.cells[x + y * self.w]
        return v & 0x3FF, (v >> 10) & 3, v >> 12

    def behavior(self, mid):
        attrs = self.prim if mid < NUM_PRIMARY else self.sec
        i = mid if mid < NUM_PRIMARY else mid - NUM_PRIMARY
        return self.mb.get(attrs[i] & 0xFF, "?") if i < len(attrs) else "MISSING"

    def open(self, x, y):
        c = self.cell(x, y)
        if c is None or c[1]:
            return False
        b = self.behavior(c[0])
        return not ("WATER" in b or b.startswith("MB_JUMP") or b in ("MB_WATERFALL", "MB_NO_SURFACING", "MISSING"))

    def people(self):
        # people who are always there: an object with a hide flag comes and goes
        return {(o["x"], o["y"]) for o in self.json.get("object_events", []) if o.get("flag") in (None, "0", 0)}


def main():
    mb = behaviors()
    layouts = {l["id"]: l for l in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"] if "id" in l}
    maps = {n: Map(n, layouts, mb) for n in MAPS}
    by_id = {m.json["id"]: m for m in maps.values()}
    findings = 0

    def say(kind, m, msg):
        nonlocal findings
        findings += 1
        print(f"{kind:8s} {m.name}: {msg}")

    for m in maps.values():
        people = m.people()
        # where a player can enter: warps (and the tile below a door), connected edges
        starts = []
        for w in m.json.get("warp_events", []):
            starts.append((w["x"], w["y"]))
            starts.append((w["x"], w["y"] + 1))
        for c in m.json.get("connections") or []:
            d = c["direction"]
            if d == "up":
                starts += [(x, 0) for x in range(m.w)]
            elif d == "down":
                starts += [(x, m.h - 1) for x in range(m.w)]
            elif d == "left":
                starts += [(0, y) for y in range(m.h)]
            elif d == "right":
                starts += [(m.w - 1, y) for y in range(m.h)]
        seen = set()
        q = deque()
        for s in starts:
            if m.open(*s) and s not in people:
                seen.add(s)
                q.append(s)
        while q:
            x, y = q.popleft()
            for dx, dy, jump in ((0, -1, "MB_JUMP_NORTH"), (0, 1, "MB_JUMP_SOUTH"), (-1, 0, "MB_JUMP_WEST"),
                                 (1, 0, "MB_JUMP_EAST")):
                nx, ny = x + dx, y + dy
                c = m.cell(nx, ny)
                if c and m.behavior(c[0]) == jump:
                    nx, ny = nx + dx, ny + dy
                if (nx, ny) not in seen and m.open(nx, ny) and (nx, ny) not in people:
                    seen.add((nx, ny))
                    q.append((nx, ny))

        def faceable(x, y):
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (x + dx, y + dy) in seen:
                    return True
                # talked to across a counter (or a dais step that works like one)
                c = m.cell(x + dx, y + dy)
                if c and m.behavior(c[0]) == "MB_COUNTER" and (x + 2 * dx, y + 2 * dy) in seen:
                    return True
            return False

        for o in m.json.get("object_events", []):
            what = f"{o.get('local_id') or o['graphics_id']} at ({o['x']},{o['y']})"
            if o.get("script") and o["script"] != "0" and not faceable(o["x"], o["y"]):
                say("REACH", m, f"can't stand next to {what} ({o['script']})")
            c = m.cell(o["x"], o["y"])
            if c and c[1] and "ITEM_BALL" in o["graphics_id"]:
                say("ONSOLID", m, f"item ball {what} sits on a solid cell")
        for b in m.json.get("bg_events", []):
            what = f"{b['type']} at ({b['x']},{b['y']}) {b.get('script') or b.get('item')}"
            if not faceable(b["x"], b["y"]) and (b["x"], b["y"]) not in seen:
                say("REACH", m, f"can't face {what}")
        for c in m.json.get("coord_events", []):
            if (c["x"], c["y"]) not in seen:
                say("REACH", m, f"trigger at ({c['x']},{c['y']}) {c.get('script')} can't be stood on")

        for w in m.json.get("warp_events", []):
            dest = by_id.get(w["dest_map"])
            if not dest:
                say("WARP", m, f"warp at ({w['x']},{w['y']}) leaves the slice for {w['dest_map']}")
                continue
            dws = dest.json.get("warp_events", [])
            if int(w["dest_warp_id"]) >= len(dws):
                say("WARP", m, f"warp at ({w['x']},{w['y']}) names {w['dest_map']} warp {w['dest_warp_id']}, "
                               f"which has {len(dws)}")
                continue
            dw = dws[int(w["dest_warp_id"])]
            c = dest.cell(dw["x"], dw["y"])
            b = dest.behavior(c[0]) if c else "?"
            if "DOOR" in b:
                if not dest.open(dw["x"], dw["y"] + 1):
                    say("WARP", m, f"door into {dest.name} ({dw['x']},{dw['y']}) has no open tile below it")
            elif c and c[1]:
                say("WARP", m, f"arrival in {dest.name} at ({dw['x']},{dw['y']}) is a solid cell ({b})")
            elif not any(dest.open(dw["x"] + dx, dw["y"] + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                say("WARP", m, f"arrival in {dest.name} at ({dw['x']},{dw['y']}) is boxed in")

        for c in m.json.get("connections") or []:
            other = by_id.get(c["map"])
            if not other:
                say("EDGE", m, f"connects {c['direction']} to {c['map']}, outside the slice")
                continue
            off, d = c["offset"], c["direction"]
            pairs = []
            if d in ("up", "down"):
                for x in range(m.w):
                    ox = x - off
                    if 0 <= ox < other.w:
                        pairs.append(((x, 0 if d == "up" else m.h - 1), (ox, other.h - 1 if d == "up" else 0)))
            else:
                for y in range(m.h):
                    oy = y - off
                    if 0 <= oy < other.h:
                        pairs.append(((0 if d == "left" else m.w - 1, y), (other.w - 1 if d == "left" else 0, oy)))
            for a, b in pairs:
                if m.open(*a) and not other.open(*b):
                    say("EDGE", m, f"open edge tile {a} walks {d} into solid {other.name} {b}")

        # the same metatile both open and solid in one map
        uses = {}
        for y in range(m.h):
            for x in range(m.w):
                mid, col, _ = m.cell(x, y)
                u = uses.setdefault(mid, [[], []])
                u[1 if col else 0].append((x, y))
        for mid, (op, so) in sorted(uses.items()):
            if op and so:
                b = m.behavior(mid)
                minority, kind = (op, "open") if len(op) < len(so) else (so, "solid")
                say("MIXED", m, f"metatile 0x{mid:03X} ({b}) is open {len(op)}x and solid {len(so)}x; "
                                f"the {kind} ones: {minority[:6]}{' ...' if len(minority) > 6 else ''}")
    print(f"{findings} finding(s)")


if __name__ == "__main__":
    main()
