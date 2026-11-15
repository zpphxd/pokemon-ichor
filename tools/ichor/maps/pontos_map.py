#!/usr/bin/env python3
"""Shared tools for the Black Sea's maps on aethos + pontos (bosporus.py,
salmydessos.py, pontic_coast.py, aia.py).

A map is a ground plan, one character a cell, painted into a Grid, with
structures placed on top in code. The plan's letters:

  ~  the Pontic sea (pontos's psea: aethos's water in palette 12)
  b  aethos's own blue sea (the Hellespont seam's eight columns)
  R  rough water in the Pontic sea (currents), surfable
  c  chalk land: white cliffs where it meets the sea, aethos grass inside
  k  kyanean land: the Clashing Rocks' blue-black rock, solid
  q  a quay: dressed stone, walkable to its edge, an ashlar face on its south side
  s  sand: aethos's beach; where it meets the sea, aethos's beach edges (Pontic
     or blue to match the water)
  .  aethos grass        ,  aethos tall grass (wild encounters)     p  aethos path
  r  kyanean rocks awash (solid, in the sea)    w  chalk rocks awash (solid)
  W  a whirlpool (solid)  #  placed in code (left as grass until something goes there)

Coast cells take the pontos autotile for their 3x3 neighbourhood (land = any
letter but ~ b R and the rocks in the sea). Every map builder can list the
neighbourhoods it needs (`--shapes`), which pontos_build.py draws.

Checks know about the sea: the player walks on land and surfs on water, and
gets on and off the water anywhere land meets it.
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
CATALOG = ROOT / "build/pontos/catalog.json"
COAST_INDEX = ROOT / "build/pontos/coast_index.json"
SHAPES = ROOT / "tools/ichor/art/pontos_shapes.json"
PRIMARY, SECONDARY = "gTileset_Aethos", "gTileset_Pontos"

# --- aethos metatiles (General's ids; design/phase1/TILES_aethos.md) ---------------
GRASS, TALL, FLOWERS, SHADE = 0x001, 0x00D, 0x004, 0x01C
SEA, ROUGH_BLUE = 0x170, 0x14E
STELE, HERM = 0x003, 0x01B
TRIPOD = (0x130, 0x131)
BOULDER, BOULDER_SAND = 0x0E0, 0x0E2
OLIVE_TOP, OLIVE_BOT, OLIVE_BOT_TIP, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1DC, 0x1DD), (0x1CE, 0x1CF)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
SAND = 0x124
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]   # door 0x061 (1,3)
AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]        # door 0x041 (1,3)
# aethos's sand island in the sea (aethos's semantics: the island's top edge and
# inner corners are sand cells; its sides, bottom and outer corners are water cells)
BEACH = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "r": 0x125, "bl": 0x12B, "b": 0x12C,
         "br": 0x12D, "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}

WATER_CH = set("~bRW")         # water letters (W is a whirlpool: water underneath)
SEA_ROCK_CH = set("rw")        # solid rocks standing in the sea
WATER_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                   "MB_SOOTOPOLIS_DEEP_WATER", "MB_NO_SURFACING"}
DOOR_BEHAVIORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR"}


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


def _attrs(path):
    p = ROOT / path
    return np.fromfile(p, "<u2") if p.exists() else np.zeros(0, "<u2")


AETHOS_ATTR = _attrs("data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin")
PONTOS_ATTR = _attrs("data/tilesets/secondary/pontos/porytiles_bin/metatile_attributes.bin")


def behavior(mid):
    if mid < 0x200:
        a = AETHOS_ATTR[mid]
    else:
        i = mid - 0x200
        a = PONTOS_ATTR[i] if i < len(PONTOS_ATTR) else 0
    return MB.get(int(a) & 0xFF, "?")


def is_water(mid):
    return behavior(mid) in WATER_BEHAVIORS


def hashed(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def load_catalog():
    if not CATALOG.exists():
        sys.exit(f"{CATALOG} is missing; run tools/ichor/art/pontos_build.py")
    cat = {s["key"]: s for s in json.loads(CATALOG.read_text())}
    index = json.loads(COAST_INDEX.read_text()) if COAST_INDEX.exists() else {}
    return cat, index


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, name, plan, shapes_only=False):
        self.name = name
        self.plan = [list(r) for r in plan]
        self.h, self.w = len(plan), len(plan[0])
        assert all(len(r) == self.w for r in plan), [len(r) for r in plan]
        self.mid = np.full((self.h, self.w), GRASS, np.uint16)
        self.solid = np.zeros((self.h, self.w), bool)
        self.needs = {"chalk": set(), "kyanean": set(), "quay": set()}
        self.shapes_only = shapes_only
        if not shapes_only:
            self.cat, self.index = load_catalog()

    # --- the plan ------------------------------------------------------------
    def ch(self, x, y):
        x = min(self.w - 1, max(0, x))
        y = min(self.h - 1, max(0, y))
        return self.plan[y][x]

    def land(self, x, y):
        return self.ch(x, y) not in WATER_CH and self.ch(x, y) not in SEA_ROCK_CH

    def key(self, x, y):
        return "".join("1" if self.land(x + dx, y + dy) else "0" for dy in (-1, 0, 1) for dx in (-1, 0, 1))

    def k(self, key, cx=0, cy=0):
        return self.cat[key]["ids"][cy][cx]

    # --- painting -------------------------------------------------------------
    def set(self, x, y, mid, solid=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def coast(self, style, x, y):
        key = self.key(x, y)
        self.needs[style].add(key)
        if self.shapes_only:
            return
        sk = self.index.get(style, {}).get(key)
        if sk == "GRASS":
            self.set(x, y, GRASS)
            return
        if sk is None:
            sys.exit(f"{self.name}: no {style} coast piece for {key} at ({x},{y}); run with --shapes, "
                     f"then tools/ichor/art/pontos_build.py")
        s = self.cat[sk]
        self.set(x, y, s["ids"][0][0], s["walk"][0] == "X")

    def paint(self):
        for y in range(self.h):
            for x in range(self.w):
                c = self.plan[y][x]
                if c == "b":
                    self.set(x, y, SEA)
                elif c in "~":
                    self.set(x, y, self.k("psea") if not self.shapes_only else 0)
                elif c == "R":
                    self.set(x, y, self.k("psea_rough") if not self.shapes_only else 0)
                elif c == "W":
                    self.set(x, y, self.k("whirlpool") if not self.shapes_only else 0, True)
                elif c == "r":
                    self.set(x, y, self.k("kyrocks") if not self.shapes_only else 0, True)
                elif c == "w":
                    self.set(x, y, self.k("rocks") if not self.shapes_only else 0, True)
                elif c in "ckq":
                    style = {"c": "chalk", "k": "kyanean", "q": "quay"}[c]
                    key = self.key(x, y)
                    if style == "chalk" and key == "1" * 9:
                        self.set(x, y, GRASS)
                    else:
                        self.coast(style, x, y)
                elif c == "s":
                    self.sand(x, y)
                elif c == ",":
                    self.set(x, y, TALL)
                elif c == "%":
                    self.set(x, y, GRASS)
                elif c == "p":
                    self.path(x, y)
                else:
                    self.set(x, y, GRASS)
        # water cells round a beach take aethos's beach edges; water cells by a
        # cliff, a rock or a quay take that coast's piece (its face, its foam)
        for y in range(self.h):
            for x in range(self.w):
                c = self.plan[y][x]
                if c in "~bR":
                    style = self.coast_style_near(x, y)
                    if style:
                        if c == "b":
                            sys.exit(f"{self.name}: blue water at ({x},{y}) touches a pontos coast")
                        self.coast(style, x, y)
                    else:
                        self.beach_water(x, y)
                elif c in ".,p" and any(self.ch(x + dx, y + dy) in WATER_CH
                                        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                    print(f"WARNING {self.name}: '{c}' at ({x},{y}) meets the water with no edge")

    def coast_style_near(self, x, y):
        """The coast a water cell belongs to: its north neighbour's, else any
        neighbour's (a face hangs from the north; foam rings everything)."""
        order = [(0, -1), (-1, 0), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        for i, (dx, dy) in enumerate(order):
            if i == 4 and any(self._sandy(x + ex, y + ey) for ex, ey in order[:4]):
                return None      # a beach's edge, not a cliff's
            if i == 4 and any(self._sandy(x + ex, y + ey) for ex, ey in order[4:]):
                return None
            xx, yy = x + dx, y + dy
            if not (0 <= xx < self.w and 0 <= yy < self.h):
                continue
            c = self.plan[yy][xx]
            if c in "ckq":
                return {"c": "chalk", "k": "kyanean", "q": "quay"}[c]
        return None

    def _sandy(self, x, y):
        return self.ch(x, y) == "s"

    def _water(self, x, y):
        return self.ch(x, y) in "~bR"

    def sand(self, x, y):
        """A sand cell: its top edge has the surf if the sea is north of it; its
        inner corners where the sea cuts in diagonally (aethos's semantics)."""
        n, w_, e = self._water(x, y - 1), self._water(x - 1, y), self._water(x + 1, y)
        nw, ne = self._water(x - 1, y - 1), self._water(x + 1, y - 1)
        part = None
        if n:
            part = "t"
        elif nw and not w_:
            part = "in_nw"
        elif ne and not e:
            part = "in_ne"
        if part is None:
            self.set(x, y, SAND)
            return
        self._beach_piece(x, y, part, self._blue_near(x, y))

    def _blue_near(self, x, y):
        return any(self.ch(x + dx, y + dy) == "b" for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    def _beach_piece(self, x, y, part, blue):
        if blue or self.shapes_only:
            self.set(x, y, BEACH[part])
        else:
            self.set(x, y, self.k(f"beach_{part}"))

    def beach_water(self, x, y):
        s = self._sandy
        n, so, w_, e = s(x, y - 1), s(x, y + 1), s(x - 1, y), s(x + 1, y)
        nw, ne, sw, se = s(x - 1, y - 1), s(x + 1, y - 1), s(x - 1, y + 1), s(x + 1, y + 1)
        part = None
        if n and e:
            part = "in_sw"
        elif n and w_:
            part = "in_se"
        elif e:
            part = "l"
        elif w_:
            part = "r"
        elif n:
            part = "b"
        elif so:
            part = None           # the sand cell below carries the surf
        elif se:
            part = "tl"
        elif sw:
            part = "tr"
        elif ne:
            part = "bl"
        elif nw:
            part = "br"
        if part:
            self._beach_piece(x, y, part, self.plan[y][x] == "b")

    def path(self, x, y):
        g = lambda xx, yy: self.ch(xx, yy) != "p"
        n, s_, w_, e = g(x, y - 1), g(x, y + 1), g(x - 1, y), g(x + 1, y)
        if (n and s_) or (w_ and e):
            key = "c"
        elif n and w_:
            key = "tl"
        elif n and e:
            key = "tr"
        elif s_ and w_:
            key = "bl"
        elif s_ and e:
            key = "br"
        elif n:
            key = "t"
        elif s_:
            key = "b"
        elif w_:
            key = "l"
        elif e:
            key = "r"
        else:
            key = "c"
        self.set(x, y, PATH[key])

    # --- structures -------------------------------------------------------------
    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place a pontos structure (or part); collision follows its walk grid."""
        if self.shapes_only:
            return
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

    def olive(self, x, y):
        below = y + 2 < self.h and self.mid[y + 2, x] == OLIVE_TOP[0]
        self.block([OLIVE_TOP, OLIVE_BOT_TIP if below else OLIVE_BOT], x, y)
        if y > 0 and all(int(m) in (GRASS, SHADE, FLOWERS) for m in self.mid[y - 1, x:x + 2]):
            self.block([OLIVE_TIP], x, y - 1, solid=bool(self.solid[y - 1, x]))

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def pine(self, x, y):
        self.block(PINE, x, y)

    def free(self, x, y, w=1, h=1):
        return all(0 <= x + i < self.w and 0 <= y + j < self.h
                   and int(self.mid[y + j, x + i]) in (GRASS, FLOWERS, SHADE)
                   and not self.solid[y + j, x + i]
                   for j in range(h) for i in range(w))

    def trees(self, olives=(), cypresses=(), pines=(), oaks=(), hazels=()):
        for (x, y) in oaks:
            if self.free(x, y, 2, 2):
                self.put("oak", x, y)
        for (x, y) in pines:
            if self.free(x, y, 2, 2):
                self.pine(x, y)
        for (x, y) in olives:
            if self.free(x, y, 2, 2):
                self.olive(x, y)
        for (x, y) in cypresses:
            if self.free(x, y, 1, 2):
                self.cypress(x, y)
        for (x, y) in hazels:
            if self.free(x, y):
                self.put("hazel", x, y)

    def woods(self, salt=0, kinds=("oak", "oak", "pine", "hazel", "oak", "cypress", "hazel")):
        """Fill the plan's '%' cells with a staggered mix of Pontic woods: oaks,
        stone pines, hazel and cypress, never in rows."""
        if self.shapes_only:
            return
        cells = [(x, y) for y in range(self.h) for x in range(self.w) if self.plan[y][x] == "%"]
        for (x, y) in cells:
            if not self.free(x, y):
                continue
            r = hashed(x, y, 31 + salt)
            kind = kinds[int(r * len(kinds)) % len(kinds)]
            two = all(self.plan[y + j][x + i] == "%" for i in (0, 1) for j in (0, 1)
                      if 0 <= y + j < self.h and 0 <= x + i < self.w) and x + 1 < self.w and y + 1 < self.h
            if kind == "oak" and two and self.free(x, y, 2, 2):
                self.put("oak", x, y)
            elif kind == "pine" and two and self.free(x, y, 2, 2):
                self.pine(x, y)
            elif kind == "cypress" and y + 1 < self.h and self.plan[y + 1][x] == "%" and self.free(x, y, 1, 2):
                self.cypress(x, y)
            else:
                self.put("hazel", x, y)
        # the woods are a wall: nothing left open inside them
        for (x, y) in cells:
            if self.free(x, y):
                self.put("hazel", x, y)

    def flowers(self, cells):
        for (x, y) in cells:
            if 0 <= x < self.w and 0 <= y < self.h and int(self.mid[y, x]) == GRASS and not self.solid[y, x]:
                self.set(x, y, FLOWERS)

    def house(self, x, y, roof, walls, upper=None):
        """A thatched house from the kit: `roof` one key per column (each 1 x 2),
        then an optional upper floor, then the ground floor (one key per column).
        Returns the ground floor's row."""
        for i, k in enumerate(roof):
            self.put(k, x + i, y)
        row = y + 2
        if upper:
            for i, k in enumerate(upper):
                self.put(k, x + i, row)
            row += 1
        for i, k in enumerate(walls):
            self.put(k, x + i, row)
        return row

    # --- output -----------------------------------------------------------------
    def encode(self):
        out = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                mid = int(self.mid[y, x])
                water = is_water(mid)
                elev = 1 if water else 3
                out[y, x] = mid | (int(self.solid[y, x]) << 10) | (elev << 12)
        return out


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

def write_layout(layout_id, folder, g, border):
    d = ROOT / "data/layouts" / folder
    d.mkdir(parents=True, exist_ok=True)
    g.encode().astype("<u2").tofile(d / "map.bin")
    np.array(border, "<u2").tofile(d / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    text = path.read_text()
    pat = re.compile(r'(\{\s*"id": "%s",.*?"blockdata_filepath": "[^"]+",\s*"layout_version": "[^"]+"\s*\})'
                     % layout_id, re.S)
    m = pat.search(text)
    assert m, f"{layout_id} not in layouts.json"
    entry = json.loads(m.group(1))
    entry.update({"width": g.w, "height": g.h, "primary_tileset": PRIMARY, "secondary_tileset": SECONDARY})
    ind = re.search(r"\n(\s*)\{\s*\"id\": \"%s\"" % layout_id, text).group(1)
    new = json.dumps(entry, indent=2).replace("\n", "\n" + ind)
    text = text[:m.start()] + new + text[m.end():]
    path.write_text(text)


def write_events(folder, events, **header):
    path = ROOT / "data/maps" / folder / "map.json"
    m = json.loads(path.read_text())
    m.update(header)
    m.update(events)
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def write_shapes(*grids):
    data = json.loads(SHAPES.read_text()) if SHAPES.exists() else {}
    for g in grids:
        for style, keys in g.needs.items():
            data.setdefault(style, [])
            data[style] = sorted(set(data[style]) | set(keys))
    SHAPES.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
    print(f"{SHAPES}: " + ", ".join(f"{s} {len(v)}" for s, v in sorted(data.items())))


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
        local_id=None, rx=0, ry=0, item=None, elevation=3):
    e = {"graphics_id": gfx, "x": x, "y": y, "elevation": elevation, "movement_type": move,
         "movement_range_x": rx, "movement_range_y": ry,
         "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
         "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag}
    if local_id:
        e = {"local_id": local_id, **e}
    return e


def swimmer(gfx, x, y, script, move, sight, local_id=None):
    """A trainer in the water: elevation 1, so the engine lets them see and swim to a
    surfing player."""
    return obj(gfx, x, y, script, move, trainer=True, sight=sight, local_id=local_id, elevation=1)


def item_ball(x, y, item, flag, water=False):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag, item=item,
               elevation=1 if water else 3)


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
            "quantity": 1, "underfoot": False}


def warp(x, y, dest, dest_id):
    return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dest_id)}


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def load_blocks(name):
    lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    layout = json.loads((ROOT / "data/maps" / name / "map.json").read_text())["layout"]
    entry = next(l for l in lay["layouts"] if l.get("id") == layout)
    return np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, entry["width"])


def cell_kind(blocks, x, y):
    """'land' (walkable), 'water' (surfable) or 'solid'."""
    h, w = blocks.shape
    if not (0 <= x < w and 0 <= y < h):
        return "out"
    b = int(blocks[y, x])
    if b >> 10 & 3:
        return "solid"
    beh = behavior(b & 0x3FF)
    if beh in WATER_BEHAVIORS:
        return "water"
    if beh.startswith("MB_JUMP"):
        return "ledge"
    return "land"


def reach(blocks, starts, blocked=frozenset(), surf=True):
    """Every cell reachable from the starts, walking and surfing, and how: dist."""
    seen = {}
    q = deque()
    for s in starts:
        if cell_kind(blocks, *s) in ("land", "water") and s not in blocked:
            seen[s] = 0
            q.append(s)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in seen or p in blocked:
                continue
            k = cell_kind(blocks, *p)
            if k == "land" or (k == "water" and surf):
                seen[p] = seen[(x, y)] + 1
                q.append(p)
    return seen


def check_map(name, starts, seams=(), still_people=True, perched=(), locked=()):
    """The common checks: warps on doors and reachable, door cells all warped, people
    standing where they can, every sign and person reachable past the people who
    stand still, seam bands primary-only. Returns (errors, reach, blocks)."""
    errors = []
    blocks = load_blocks(name)
    hh, ww = blocks.shape
    ev = json.loads((ROOT / "data/maps" / name / "map.json").read_text())
    warps = {(w_["x"], w_["y"]) for w_ in ev["warp_events"]}
    still = set()
    for o in ev["object_events"]:
        if o["movement_type"] != "MOVEMENT_TYPE_WANDER_AROUND":
            still.add((o["x"], o["y"]))
    r_all = reach(blocks, starts)
    r = reach(blocks, starts, blocked=still)
    for (x, y) in warps:
        b = behavior(int(blocks[y, x]) & 0x3FF)
        if b not in DOOR_BEHAVIORS:
            errors.append(f"{name}: warp at ({x},{y}) is on {b}, not a door")
        if not any((x + dx, y + dy) in r for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))) and (x, y) not in r:
            errors.append(f"{name}: warp at ({x},{y}) is unreachable")
    for y in range(hh):
        for x in range(ww):
            b = behavior(int(blocks[y, x]) & 0x3FF)
            if b in DOOR_BEHAVIORS and (x, y) not in warps:
                errors.append(f"{name}: door metatile at ({x},{y}) has no warp")
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        k = cell_kind(blocks, x, y)
        lid = o.get("local_id", o["graphics_id"])
        if lid in perched or o["script"].split("_")[-1] in perched:
            continue
        want = "water" if o["elevation"] == 1 else "land"
        if k != want:
            errors.append(f"{name}: object {lid} at ({x},{y}) (elevation {o['elevation']}) stands on {k}")
    targets = [(b["x"], b["y"], f"{b['type']} {b.get('script', b.get('item'))}") for b in ev["bg_events"]]
    targets += [(o["x"], o["y"], o.get("local_id", o["script"])) for o in ev["object_events"]
                if o["script"] not in ("0x0", "0")]
    for (x, y, what) in targets:
        fronts = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0))]
        # talked to across a counter
        for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            fx, fy = x + dx, y + dy
            if 0 <= fx < ww and 0 <= fy < hh and behavior(int(blocks[fy, fx]) & 0x3FF) == "MB_COUNTER":
                fronts.append((fx + dx, fy + dy))
        if what.startswith("hidden_item") and (x, y) in r:
            continue
        if (x, y) in locked:          # behind a relic gate on purpose
            continue
        if not any(p in r for p in fronts):
            errors.append(f"{name}: the {what} at ({x},{y}) can't be reached past the people standing still")
    for (kind, cells, why) in seams:
        for c in cells:
            rng = [(x, c) for x in range(ww)] if kind == "rows" else [(c, y) for y in range(hh)]
            for (x, y) in rng:
                m = int(blocks[y, x]) & 0x3FF
                if m >= 0x200:
                    errors.append(f"{name}: ({x},{y}) is pontos metatile 0x{m:03X} within the {why} seam's "
                                  f"band; use aethos there")
    return errors, r_all, blocks


def edge_kinds(blocks, side):
    """The cells along one edge, as 'open' (land or water you can cross) or 'shut'."""
    h, w = blocks.shape
    cells = {"left": [(0, y) for y in range(h)], "right": [(w - 1, y) for y in range(h)],
             "up": [(x, 0) for x in range(w)], "down": [(x, h - 1) for x in range(w)]}[side]
    return [cell_kind(blocks, *c) for c in cells]


def check_seam(a, b, direction, offset):
    """Map a's edge `direction` meets map b, offset as in map.json. Along the cells
    they share, both sides must agree: water against water, land against land."""
    A, B = load_blocks(a), load_blocks(b)
    opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}[direction]
    ea, eb = edge_kinds(A, direction), edge_kinds(B, opposite)
    errors = []
    for i, ka in enumerate(ea):
        j = i - offset
        if 0 <= j < len(eb):
            kb = eb[j]
            if (ka == "water") != (kb == "water"):
                errors.append(f"{a} {direction} edge cell {i} is {ka}; {b}'s cell {j} is {kb}")
    return errors


def sight_cells(blocks, x, y, facing, reach_n):
    d = {"MOVEMENT_TYPE_FACE_UP": (0, -1), "MOVEMENT_TYPE_FACE_DOWN": (0, 1),
         "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}[facing]
    out = []
    for i in range(1, reach_n + 1):
        c = (x + d[0] * i, y + d[1] * i)
        if cell_kind(blocks, *c) not in ("land", "water"):
            break
        out.append(c)
    return out


def check_checkpoint(name, blocks, trainer, starts, goals):
    """A mandatory trainer: no walk or surf from the starts to the goals skirts
    their sight line."""
    x, y, facing, n = trainer["x"], trainer["y"], trainer["movement_type"], int(trainer["trainer_sight_or_berry_tree_id"])
    line = sight_cells(blocks, x, y, facing, n)
    r = reach(blocks, starts, blocked=set(line) | {(x, y)})
    ok = not any(g in r for g in goals)
    whole = reach(blocks, starts)
    return ok and any(g in whole for g in goals), line


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(layout_id, name, out_dir, stem, screens, scale=2):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / f"{stem}.png"
    subprocess.run(rm + [layout_id, "--scale", str(scale), "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    overlay(png, name, out_dir / f"{stem}_walk.png", scale)
    crops(name, out_dir, stem, screens)
    return png


def crops(name, out_dir, stem, screens, margin=8):
    from PIL import Image
    blocks = load_blocks(name)
    h, w = blocks.shape
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
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", "pontos",
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    out = []
    for nm, (px, py) in screens.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        crop.save(out_dir / f"{stem}_screen_{nm}.png")
        out.append(crop)
    cols = 2
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(out) // cols) * (10 * c + 8) - 8), (24, 24, 32))
    for i, crop in enumerate(out):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out_dir / f"{stem}_screens.png")
    tmp.unlink()
    png.unlink()


def overlay(png, name, out, scale):
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    blocks = load_blocks(name)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16 * scale
    for y, row in enumerate(blocks):
        for x, b in enumerate(row):
            if b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 60))
    ev = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
    for o in ev["object_events"]:
        col = (255, 128, 0, 255) if o["trainer_type"] != "TRAINER_TYPE_NONE" else (255, 255, 0, 255)
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=col, width=2)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=2)
    for b in ev["bg_events"]:
        col = (120, 255, 120, 255) if b["type"] == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4], fill=col, width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4], fill=col, width=2)
    Image.alpha_composite(im, lay).save(out)
