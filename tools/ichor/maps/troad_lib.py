"""Shared tools for the Troad's outdoor maps (aethos + troas): the Hellespont,
Sestos and Ilion (tools/ichor/maps/hellespont.py, sestos.py, ilion.py).

A map is composed on a Grid from a ground Plan (one character a cell), then
structures from build/troas/catalog.json go on top. The builder also writes the
map's events (map.json), so every coordinate comes from the same code as the
layout, and then checks the result: warps on doors, people and triggers on
walkable ground, every sign and person readable, seams in aethos alone, sight
lines across the only path, and the current never carrying a surfer into rock.

Make the catalog with
  /usr/bin/python3 tools/ichor/art/troas_build.py --no-compile
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
SEC = "troas"

# ---------------------------------------------------------------------------
# aethos ids (General's numbering; TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
GRASS_SHADE = 0x01C
FLOWERS = 0x004
TALL = 0x00D             # barley: tall grass
LONG_GRASS = 0x015       # reeds: long grass
SEA = 0x170
DEEP = 0x14E             # rough, deep water
STELE = 0x003            # a marble stele: town and road signs
HERM = 0x01B             # a roadside herm
TRIPOD = (0x130, 0x131)
BOULDER = 0x0E0
SEA_ROCK = (0x18C, 0x194)
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A, "w": 0x132, "e": 0x133}
LEDGE = {"s": 0x087, "s_l": 0x0D5, "s_r": 0x0D6}
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
TILLED = {"tl": 0x103, "t": 0x104, "tr": 0x105, "l": 0x10B, "c": 0x10C, "r": 0x10D,
          "bl": 0x113, "b": 0x114, "br": 0x115}
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}
SAND = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "c": 0x124, "r": 0x125,
        "bl": 0x12B, "b": 0x12C, "br": 0x12D,
        "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}
ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER", "MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT",
                  "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT"}
DOOR_BEHAVIORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_SOUTH_ARROW_WARP"}
SOLID = 1 << 10


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


def attrs(path):
    return np.fromfile(ROOT / path, "<u2")


AETHOS_ATTR = attrs("data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin")
TROAS_ATTR = attrs("data/tilesets/secondary/troas/porytiles_bin/metatile_attributes.bin")


def behavior(mid):
    a = AETHOS_ATTR[mid] if mid < 0x200 else TROAS_ATTR[mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    """A stable pseudo-random number in [0, 1) for a map cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def catalog():
    path = ROOT / "build/troas/catalog.json"
    if not path.exists():
        sys.exit(f"{path} is missing; run tools/ichor/art/troas_build.py --no-compile")
    return {s["key"]: s for s in json.loads(path.read_text())}


# ---------------------------------------------------------------------------
# soft shapes (troas_land's fourteen): which piece a region cell needs
# ---------------------------------------------------------------------------

SHAPE_KEYS = {
    "11111111": "c", "00111110": "n", "11100011": "s", "11111000": "w", "10001111": "e",
    "00111000": "nw", "00001110": "ne", "11100000": "sw", "10000011": "se",
    "11111110": "in_nw", "10111111": "in_ne", "11111011": "in_sw", "11101111": "in_se",
    "00000000": "one",
}
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # N NE E SE S SW W NW


def shape_of(inside, x, y):
    """The fourteen-piece shape for region cell (x, y); inside(x, y) -> bool.
    Shapes outside the set (a one-wide neck, two inner corners) take the nearest."""
    b = [1 if inside(x + dx, y + dy) else 0 for dx, dy in DIRS]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    key = "".join(map(str, b))
    if key in SHAPE_KEYS:
        return SHAPE_KEYS[key]
    n, e, s_, w_ = b[0], b[2], b[4], b[6]
    if not n and not w_:
        return "nw"
    if not n and not e:
        return "ne"
    if not s_ and not w_:
        return "sw"
    if not s_ and not e:
        return "se"
    if not n:
        return "n"
    if not s_:
        return "s"
    if not w_:
        return "w"
    if not e:
        return "e"
    for d, name in ((7, "in_nw"), (1, "in_ne"), (5, "in_sw"), (3, "in_se")):
        if not b[d]:
            return name
    return "c"


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mid = np.full((h, w), GRASS, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.cat = catalog()

    def set(self, x, y, mid, solid=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def k(self, key, part=None, cx=0, cy=0):
        s = self.cat[key]
        if part is not None:
            cx, cy = s["names"][part]
        return s["ids"][cy][cx]

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place a structure (or part of one); collision follows its walk grid."""
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], s["walk"][cy + j][cx + i] == "X")

    def part(self, key, part, x, y, solid=None):
        s = self.cat[key]
        cx, cy = s["names"][part]
        code = s["walk"][cy][cx]
        self.set(x, y, s["ids"][cy][cx], code == "X" if solid is None else solid)

    def block(self, rows, x, y, solid=True):
        for j, r in enumerate(rows):
            for i, m in enumerate(r):
                if m is not None:
                    self.set(x + i, y + j, m, solid)

    def olive(self, x, y):
        below = y + 2 < self.h and self.mid[y + 2, x] == OLIVE_TOP[0]
        self.block([OLIVE_TOP, OLIVE_BOT_TIP if below else OLIVE_BOT], x, y)
        if y > 0:
            above = (int(self.mid[y - 1, x]), int(self.mid[y - 1, x + 1]))
            if above == OLIVE_BOT:
                self.block([OLIVE_BOT_TIP], x, y - 1)
            elif all(m in (GRASS, GRASS_SHADE, FLOWERS) for m in above):
                self.block([OLIVE_TIP_GRASS], x, y - 1, solid=bool(self.solid[y - 1, x]))

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def pine(self, x, y):
        self.block(PINE, x, y)

    def free(self, x, y, w=1, h=1):
        return all(0 <= x + i < self.w and 0 <= y + j < self.h
                   and self.mid[y + j, x + i] in (GRASS, GRASS_SHADE, FLOWERS)
                   and not self.solid[y + j, x + i]
                   for j in range(h) for i in range(w))

    def trees(self, olives=(), cypresses=(), pines=(), ida=(), oaks=(), young=(), elms=()):
        """Plant where the ground is still open grass, so a tree never lands on a road."""
        for (x, y) in ida:
            if self.free(x, y, 2, 3):
                self.put("ida_pine", x, y)
        for (x, y) in oaks:
            if self.free(x, y, 2, 2):
                self.put("oak", x, y)
        for (x, y) in pines:
            if self.free(x, y, 2, 2):
                self.pine(x, y)
        for (x, y) in olives:
            if self.free(x, y, 2, 2):
                self.olive(x, y)
        for (x, y) in young:
            if self.free(x, y, 1, 2):
                self.put("young_pine", x, y)
        for (x, y) in elms:
            if self.free(x, y, 1, 2):
                self.put("elm_withered", x, y)
        for (x, y) in cypresses:
            if self.free(x, y, 1, 2):
                self.cypress(x, y)

    def scatter(self, cells, part=None):
        """Flowers (aethos's anemones) or troas grass bits on open grass."""
        for i, (x, y) in enumerate(cells):
            if 0 <= x < self.w and 0 <= y < self.h and self.mid[y, x] == GRASS and not self.solid[y, x]:
                if part is None:
                    self.set(x, y, FLOWERS)
                else:
                    self.part("grass_bits", part if isinstance(part, str) else part[i % len(part)], x, y)

    def wall_we(self, x0, x1, y):
        for x in range(x0, x1 + 1):
            self.set(x, y, WALL["l"] if x == x0 else WALL["r"] if x == x1 else WALL["run"], True)

    def wall_ns(self, x, y0, y1, side="w"):
        for y in range(y0, y1 + 1):
            self.set(x, y, WALL[side], True)

    def forest(self, x0, y0, x1, y1, salt=0, open_cells=(), aethos=False):
        """Fill a box with a staggered mixed wood (Ida pines, stone pines, olives,
        cypresses, young pines), then close whatever grass is left in it with
        cypresses, so the edge never shows a gap. aethos: no troas trees (for a
        seam's aethos-only strip)."""
        cells = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
                 if (x, y) not in open_cells]
        # plant in a scrambled order, so the wood never settles into rows; the big
        # trees first, then the small ones in the gaps
        order = sorted(cells, key=lambda c: hashed(c[0], c[1], 77 + salt))
        for x, y in order:
            if not self.free(x, y):
                continue
            r = hashed(x, y, 31 + salt)
            fits2 = x + 1 <= x1 or x + 1 >= self.w
            if r < 0.22 and not aethos and self.free(x, y, 2, 3) and fits2 and y + 2 <= y1:
                self.put("ida_pine", x, y)
            elif r < 0.52 and self.free(x, y, 2, 2) and fits2 and y + 1 <= y1:
                self.olive(x, y)
            elif r < 0.64 and self.free(x, y, 2, 2) and fits2 and y + 1 <= y1:
                self.pine(x, y)
        for x, y in order:
            if not self.free(x, y):
                continue
            r = hashed(x, y, 41 + salt)
            if r < 0.4 and not aethos and self.free(x, y, 1, 2) and y + 1 <= y1:
                self.put("young_pine", x, y)
            elif self.free(x, y, 1, 2) and y + 1 <= y1:
                self.cypress(x, y)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x, y) in open_cells:
                    continue
                m = int(self.mid[y, x])
                edge = x in (0, self.w - 1) or y in (0, self.h - 1)
                if m in OLIVE_TIP_GRASS and edge:
                    self.solid[y, x] = True          # an olive's crown on the map's edge
                elif self.free(x, y) and edge:
                    # the map's edge must be shut; inside the wood a gap is a glade
                    if y == self.h - 1:
                        self.set(x, y, CYPRESS_TOP, True)        # a cypress cut by the map's edge
                    elif y == 0:
                        self.set(x, y, CYPRESS_BOT, True)        # its crown beyond the edge
                    elif self.free(x, y + 1):
                        self.cypress(x, y)
                    elif self.mid[y - 1, x] == CYPRESS_TOP:
                        self.set(x, y, CYPRESS_BOT, True)
                    else:
                        self.set(x, y, BOULDER, True)


def edge_key(n, s_, w_, e, nw, ne, sw, se):
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


def neighbours(plan, x, y, outside):
    h, w = len(plan), len(plan[0])

    def out(dx, dy):
        x2, y2 = x + dx, y + dy
        if not (0 <= x2 < w and 0 <= y2 < h):
            return False
        return plan[y2][x2] in outside
    return (out(0, -1), out(0, 1), out(-1, 0), out(1, 0), out(-1, -1), out(1, -1), out(-1, 1), out(1, 1))


QUAY_PART = {"tl": "NW", "t": "N", "tr": "NE", "l": "W", "r": "E", "bl": "SW", "b": "S", "br": "SE",
             "in_nw": "inNW", "in_ne": "inNE", "in_sw": "inSW", "in_se": "inSE"}
WATER = "~c"


def paint(g, plan):
    """Lay the plan's ground. Codes:
      g grass  p path  s sand  ~ sea  c the current  q quay  w wheat  T barley (tall grass)
      W wheat as a town's crop (impassable)  L reeds (long grass)  t tilled earth  B a building's footprint (left as grass; the
      building goes on top)"""
    P = plan
    h, w = len(P), len(P[0])
    for y in range(h):
        assert len(P[y]) == w, f"plan row {y} is {len(P[y])} wide, not {w}"
        for x in range(w):
            c = P[y][x]
            if c == "~":
                g.set(x, y, SEA)
            elif c == "c":
                g.part("current", f"v{int(hashed(x, y, 5) * 4)}", x, y)
            elif c == "q":
                key = edge_key(*neighbours(P, x, y, WATER))
                if key == "c":
                    r = hashed(x, y, 1)
                    part = "C2" if r < 0.16 else "C3" if r < 0.3 else "C"
                else:
                    part = QUAY_PART[key]
                g.part("quay", part, x, y, solid=False)
            elif c == "s":
                key = edge_key(*neighbours(P, x, y, WATER))
                if key == "c":
                    n, s_, w_, e, *_ = neighbours(P, x, y, "gTLwWtfB")
                    soft = edge_key(n, s_, w_, e, *[False] * 4)
                    g.set(x, y, SAND_GRASS[soft] if soft != "c" else SAND["c"])
                else:
                    g.set(x, y, SAND[key])
            elif c == "p":
                n, s_, w_, e, *_ = neighbours(P, x, y, "gtTwf")
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e, *[False] * 4)
                g.set(x, y, PATH.get(key, PATH["c"]))
            elif c in "wW":
                shape = shape_of(lambda a, b: 0 <= a < w and 0 <= b < h and P[b][a] == c, x, y)
                if shape == "c" and hashed(x, y, 9) < 0.2:
                    shape = "c2"
                g.part("wheat" if c == "w" else "wheat_crop", shape, x, y)
            elif c == "T":
                g.set(x, y, TALL)
            elif c == "L":
                g.set(x, y, LONG_GRASS)
            elif c == "t":
                n, s_, w_, e, *_ = neighbours(P, x, y, "gpsTw")
                g.set(x, y, TILLED[edge_key(n, s_, w_, e, *[False] * 4)])
            else:
                g.set(x, y, GRASS)


def encode(g):
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mid[y, x])
            water = behavior(mid) in SURF_BEHAVIORS
            elev = 1 if water else 3
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | (elev << 12)
    return out


def write_layout(g, name, border):
    d = ROOT / "data/layouts" / name
    d.mkdir(parents=True, exist_ok=True)
    encode(g).astype("<u2").tofile(d / "map.bin")
    np.array(border, np.uint16).astype("<u2").tofile(d / "border.bin")


def set_layout(layout_id, w, h, secondary="gTileset_Troas"):
    """Keep layouts.json's size and tilesets in step with the builder."""
    path = ROOT / "data/layouts/layouts.json"
    text = path.read_text()
    pat = re.compile(r'("id": "%s",\s*"name": "[^"]+",\s*"width": )\d+(,\s*"height": )\d+'
                     r'(,\s*"primary_tileset": "[^"]+",\s*"secondary_tileset": ")[^"]+"' % layout_id)
    new, n = pat.subn(lambda m: f"{m.group(1)}{w}{m.group(2)}{h}{m.group(3)}{secondary}\"", text)
    assert n == 1, f"{layout_id} not found in layouts.json"
    if new != text:
        path.write_text(new)


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def obj(gfx, x, y, script="0x0", local_id=None, move="MOVEMENT_TYPE_FACE_DOWN", rx=0, ry=0,
        trainer="TRAINER_TYPE_NONE", sight="0", flag="0", elevation=3):
    o = {"graphics_id": gfx, "x": x, "y": y, "elevation": elevation, "movement_type": move,
         "movement_range_x": rx, "movement_range_y": ry, "trainer_type": trainer,
         "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}
    if local_id:
        o = {"local_id": local_id, **o}
    return o


def item_ball(x, y, item, flag):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", sight=item, flag=flag)


def warp(x, y, dest, dest_id):
    return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dest_id)}


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def hidden(x, y, item, flag, elevation=3):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": elevation, "item": item, "flag": flag}


def trigger(x, y, var, value, script, elevation=3):
    return {"type": "trigger", "x": x, "y": y, "elevation": elevation, "var": var, "var_value": str(value),
            "script": script}


def write_events(name, objects, warps, coords, bgs, connections=None, **header):
    path = ROOT / "data/maps" / name / "map.json"
    m = json.loads(path.read_text())
    m.update(header)
    m["connections"] = connections or None
    m["object_events"] = objects
    m["warp_events"] = warps
    m["coord_events"] = coords
    m["bg_events"] = bgs
    path.write_text(json.dumps(m, indent=2) + "\n")


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def render(layout_id, map_name, w, h, out_dir, stem, screens):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / f"{stem}.png"
    subprocess.run(rm + [layout_id, "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    overlay(png, ROOT / f"data/layouts/{map_name}/map.bin", w, map_name, out_dir / f"{stem}_walk.png", 2)
    if screens:
        crops(map_name, w, h, out_dir, stem, screens)
    return png


def crops(map_name, w, h, out_dir, stem, screens, margin=8):
    """GBA-screen views (15x10 tiles, the player on the 8th column and 5th row)
    from the map padded with its border, at 2x, tiled into one sheet."""
    from PIL import Image
    blocks = np.fromfile(ROOT / f"data/layouts/{map_name}/map.bin", "<u2").reshape(h, w)
    bord = np.fromfile(ROOT / f"data/layouts/{map_name}/border.bin", "<u2").reshape(2, 2)
    big = np.empty((h + 2 * margin, w + 2 * margin), np.uint16)
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            big[y, x] = bord[y % 2, x % 2]
    big[margin:margin + h, margin:margin + w] = blocks
    tmp = out_dir / f"{stem}_padded.bin"
    big.astype("<u2").tofile(tmp)
    png = out_dir / f"{stem}_padded.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", SEC,
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    out = []
    for name, (px, py) in screens.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        out.append(crop)
    cols = 2
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(out) // cols) * (10 * c + 8) - 8),
                      (24, 24, 32))
    for i, crop in enumerate(out):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out_dir / f"{stem}_screens.png")
    tmp.unlink()
    png.unlink()


def overlay(png, bin_path, width, map_name, out, scale):
    """Tint impassable cells red and water blue, and draw the map's events."""
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    blocks = np.fromfile(bin_path, "<u2").reshape(-1, width)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16 * scale
    for y, row in enumerate(blocks):
        for x, b in enumerate(row):
            if b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif b >> 12 == 1:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 80, 255, 50))
    ev = json.loads((ROOT / f"data/maps/{map_name}/map.json").read_text())
    for o in ev["object_events"]:
        col = (255, 120, 0, 255) if o["trainer_type"] != "TRAINER_TYPE_NONE" else (255, 255, 0, 255)
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=col, width=2)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=2)
    for t in ev["coord_events"]:
        d.rectangle([t["x"] * c + 6, t["y"] * c + 6, t["x"] * c + c - 7, t["y"] * c + c - 7], fill=(255, 0, 255, 160))
    for b in ev["bg_events"]:
        col = (120, 255, 120, 255) if b["type"] == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4], fill=col, width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4], fill=col, width=2)
    Image.alpha_composite(im, lay).save(out)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 != 1


def surfable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 == 1


def reachable(blocks, start, extra_open=(), surf=False):
    """Cells reachable on foot (or, with surf, on foot and on the water)."""
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            ok = walkable(blocks, *p) or (surf and surfable(blocks, *p))
            if p not in seen and (ok or p in extra_open):
                seen.add(p)
                q.append(p)
    return seen


FLYERS = ("WINGULL",)


def load(name):
    lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    ev = json.loads((ROOT / "data/maps" / name / "map.json").read_text())
    entry = next(l for l in lay["layouts"] if l.get("id") == ev["layout"])
    blocks = np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, entry["width"])
    return blocks, ev


def check_map(name, start, seams=(), scripted=None, surf=False):
    """The common checks. seams: (kind, cells, why): kind 'rows' or 'cols' lists
    the rows or columns that must use aethos only."""
    errors = []
    blocks, ev = load(name)
    hh, ww = blocks.shape
    warps = [(w_["x"], w_["y"]) for w_ in ev["warp_events"]]
    reach = reachable(blocks, start, extra_open=set(warps), surf=surf)
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
        if any(f in o["graphics_id"] for f in FLYERS):
            continue
        ok = walkable(blocks, x, y) or (o["elevation"] == 1 and surfable(blocks, x, y))
        if not ok:
            errors.append(f"{name}: object {o.get('local_id', o['graphics_id'])} at ({x},{y}) stands on a solid cell")
        if (x, y) not in reach:
            errors.append(f"{name}: object {o.get('local_id', o['graphics_id'])} at ({x},{y}) is unreachable")
    for t in ev["coord_events"]:
        if (t["x"], t["y"]) not in reach:
            errors.append(f"{name}: coord event at ({t['x']},{t['y']}) is unreachable")
    still = blocks.copy()
    for o in ev["object_events"]:
        if o["movement_type"] not in ("MOVEMENT_TYPE_WANDER_AROUND",) and 0 <= o["y"] < hh and 0 <= o["x"] < ww:
            still[o["y"], o["x"]] |= SOLID
    reach_still = reachable(still, start, extra_open=set(warps), surf=surf)
    targets = [(b["x"], b["y"], f"{b['type']} event") for b in ev["bg_events"]]
    targets += [(o["x"], o["y"], o.get("local_id", o["graphics_id"])) for o in ev["object_events"]
                if not any(f in o["graphics_id"] for f in FLYERS) and o["script"] not in ("0x0", "0")]
    for (x, y, what) in targets:
        fronts = []
        for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            fx, fy = x + dx, y + dy
            fronts.append((fx, fy))
            if 0 <= fx < ww and 0 <= fy < hh and behavior(int(blocks[fy, fx]) & 0x3FF) == "MB_COUNTER":
                fronts.append((fx + dx, fy + dy))
        if (x, y) in reach_still and what.startswith("hidden_item"):
            continue
        if not any(p in reach_still for p in fronts):
            errors.append(f"{name}: the {what} at ({x},{y}) can't be reached past the people standing still")
    for (kind, cells, why) in seams:
        for c in cells:
            rng = [(x, c) for x in range(ww)] if kind == "rows" else [(c, y) for y in range(hh)]
            for (x, y) in rng:
                m = int(blocks[y, x]) & 0x3FF
                if m >= 0x200:
                    errors.append(f"{name}: ({x},{y}) is troas metatile 0x{m:03X}, within the {why} "
                                  f"seam's band; use aethos there")
    for who, cells in (scripted or {}).items():
        for (x, y) in cells:
            if not walkable(blocks, x, y):
                errors.append(f"{name}: {who}'s scripted path crosses solid ({x},{y})")
    return errors, reach, blocks, ev


def check_edge(name, blocks, side, open_cells, walk=True):
    """An edge's open cells are exactly open_cells: walkable (or surfable)."""
    errors = []
    hh, ww = blocks.shape
    if side == "top":
        cells = [(x, 0) for x in range(ww)]
    elif side == "bottom":
        cells = [(x, hh - 1) for x in range(ww)]
    elif side == "left":
        cells = [(0, y) for y in range(hh)]
    else:
        cells = [(ww - 1, y) for y in range(hh)]
    for (x, y) in cells:
        ok = walkable(blocks, x, y) or surfable(blocks, x, y)
        want = (x if side in ("top", "bottom") else y) in open_cells
        if ok != want:
            errors.append(f"{name}: {side} edge cell ({x},{y}) is {'open' if ok else 'closed'}")
    return errors


def check_current(name, blocks):
    """A surfer riding the current must always be carried onto water: the cell
    east of every current cell is current or calm, surfable water."""
    errors = []
    hh, ww = blocks.shape
    for y in range(hh):
        for x in range(ww):
            if behavior(int(blocks[y, x]) & 0x3FF) != "MB_EASTWARD_CURRENT":
                continue
            if not surfable(blocks, x + 1, y):
                errors.append(f"{name}: the current at ({x},{y}) carries a surfer into ({x + 1},{y}), "
                              f"which is not open water")
    return errors


def sight_cells(o):
    """The cells a trainer watches, from its facing and range."""
    rng = int(o["trainer_sight_or_berry_tree_id"])
    d = {"MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_UP": (0, -1),
         "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}.get(o["movement_type"])
    if not d:
        return []
    return [(o["x"] + d[0] * k, o["y"] + d[1] * k) for k in range(1, rng + 1)]


def blocks_path(blocks, ev, local_id, start, goal, surf=False):
    """True if the trainer's sight line cuts every way from start to goal."""
    o = next(o for o in ev["object_events"] if o.get("local_id") == local_id)
    cut = blocks.copy()
    for (x, y) in sight_cells(o) + [(o["x"], o["y"])]:
        if 0 <= y < cut.shape[0] and 0 <= x < cut.shape[1]:
            cut[y, x] |= SOLID
    return goal not in reachable(cut, start, surf=surf)
