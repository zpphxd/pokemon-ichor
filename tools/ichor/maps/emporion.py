#!/usr/bin/env python3
"""Build Emporion City (aethos + emporion), and the tools its harbor shares.

Writes data/layouts/EmporionCity/map.bin and border.bin (48x46), then checks
data/maps/EmporionCity/map.json against the blockdata: warps on doors, people
and triggers on walkable ground, every sign and person readable, the scripted
paths open, and the seams (see SEAMS below) drawn from aethos alone.

Emporion's metatiles come from build/emporion/catalog.json (TILES_emporion.md),
placed by structure key and part name. Make the catalog with
  /usr/bin/python3 tools/ichor/art/emporion_build.py emporion --no-compile

The harbor district, `MAP_EMPORION_HARBOR`, is built by emporion_harbor.py with
the Grid, painting, encoding, rendering and checking code in this file.

Usage: /usr/bin/python3 tools/ichor/maps/emporion.py [--render DIR]
  --render writes emporion_city.png (2x), emporion_city_walk.png (collision
  overlay with the events), screen-sized crops along the player's route and a
  sheet of them, into DIR.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------------------
# aethos ids (General's numbering; TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
GRASS_SHADE = 0x01C
FLOWERS = 0x004
SEA = 0x170
STELE = 0x003            # a marble stele: town and road signs
HERM = 0x01B             # a roadside herm
TRIPOD = (0x130, 0x131)  # a bronze tripod on a marble plinth (top layer, then base)
BOULDER = 0x0E0
TROUGH = (0x005, 0x006, 0x007)   # anemone troughs
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A, "w": 0x132, "e": 0x133}
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
TILLED = {"tl": 0x103, "t": 0x104, "tr": 0x105, "l": 0x10B, "c": 0x10C, "r": 0x10D,
          "bl": 0x113, "b": 0x114, "br": 0x115}
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}
SAND = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "c": 0x124, "r": 0x125,
        "bl": 0x12B, "b": 0x12C, "br": 0x12D,
        "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER"}
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
TILESET_ATTR = {
    s: attrs(f"data/tilesets/secondary/{s}/porytiles_bin/metatile_attributes.bin")
    for s in ("emporion", "isthmos")
}


def behavior(mid, secondary):
    a = AETHOS_ATTR[mid] if mid < 0x200 else TILESET_ATTR[secondary][mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    """A stable pseudo-random number in [0, 1) for a map cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def catalog(secondary):
    path = ROOT / f"build/{secondary}/catalog.json"
    if not path.exists():
        sys.exit(f"{path} is missing; run tools/ichor/art/emporion_build.py {secondary} --no-compile")
    return {s["key"]: s for s in json.loads(path.read_text())}


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, w, h, secondary):
        self.w, self.h, self.sec = w, h, secondary
        self.mid = np.full((h, w), GRASS, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.bldg = np.zeros((h, w), bool)     # tall fronts that shade the paving below
        self.cat = catalog(secondary)

    def set(self, x, y, mid, solid=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def k(self, key, part=None, cx=0, cy=0):
        s = self.cat[key]
        if part is not None:
            cx, cy = s["names"][part]
        return s["ids"][cy][cx]

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None, bldg=False):
        """Place a structure (or part of one); collision follows its walk grid."""
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                code = s["walk"][cy + j][cx + i]
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], code == "X")
                if bldg and code in "XD" and 0 <= x + i < self.w and 0 <= y + j < self.h:
                    self.bldg[y + j, x + i] = True

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
        """A 2x2 olive. Its crown pokes into the row above, drawn over the player;
        stacked olives use the bottom-with-tip piece, as TILES_aethos.md says."""
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
        """True if every cell is plain open grass."""
        return all(0 <= x + i < self.w and 0 <= y + j < self.h
                   and self.mid[y + j, x + i] in (GRASS, GRASS_SHADE, FLOWERS)
                   and not self.solid[y + j, x + i]
                   for j in range(h) for i in range(w))

    def wall_we(self, x0, x1, y):
        """A west-east dry-stone wall from x0 to x1 inclusive."""
        for x in range(x0, x1 + 1):
            self.set(x, y, WALL["l"] if x == x0 else WALL["r"] if x == x1 else WALL["run"], True)

    def wall_ns(self, x, y0, y1, side="w"):
        for y in range(y0, y1 + 1):
            self.set(x, y, WALL[side], True)

    def trees(self, olives=(), cypresses=(), pines=()):
        """Plant where the ground is still open grass, so a tree never lands on a road."""
        for (x, y) in pines:
            if self.free(x, y, 2, 2):
                self.pine(x, y)
        for (x, y) in olives:
            if self.free(x, y, 2, 2):
                self.olive(x, y)
        for (x, y) in cypresses:
            if self.free(x, y, 1, 2):
                self.cypress(x, y)

    def flowers(self, cells):
        for (x, y) in cells:
            if 0 <= x < self.w and 0 <= y < self.h and self.mid[y, x] == GRASS and not self.solid[y, x]:
                self.set(x, y, FLOWERS)

    def close_edge(self, row, keep_open, salt=0):
        """Shut a seam row everywhere but its road, with a mixed tree line (olives,
        stone pines and cypresses, by turns), so the only way across reads as the road.
        row is 0 (north edge) or h - 1 (south edge)."""
        top = row if row == 0 else row - 1
        x = 0
        while x < self.w:
            if x in keep_open or self.solid[row, x] or self.mid[row, x] not in (GRASS, GRASS_SHADE, FLOWERS):
                x += 1
                continue
            r = hashed(x, row, 7 + salt)
            two = x + 1 < self.w and x + 1 not in keep_open
            if two and r < 0.45 and self.free(x, top, 2, 2):
                self.olive(x, top)
                x += 2
            elif two and r < 0.6 and self.free(x, top, 2, 2):
                self.pine(x, top)
                x += 2
            elif self.free(x, top, 1, 2):
                self.cypress(x, top)
                x += 1
            else:
                # the row above is taken (a tree's crown, a wall): close the cell with a
                # cypress drawn over what it stands on
                self.set(x, row, CYPRESS_BOT if row != 0 else CYPRESS_TOP, True)
                x += 1
        # what's left open on the edge is an olive's crown poking into it: a tree,
        # so not a way across
        for x in range(self.w):
            if x not in keep_open and self.mid[row, x] in OLIVE_TIP_GRASS:
                self.solid[row, x] = True


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


def neighbours(plan, x, y, outside):
    h, w = len(plan), len(plan[0])

    def out(dx, dy):
        x2, y2 = x + dx, y + dy
        if not (0 <= x2 < w and 0 <= y2 < h):
            return False
        return plan[y2][x2] in outside
    return (out(0, -1), out(0, 1), out(-1, 0), out(1, 0), out(-1, -1), out(1, -1), out(-1, 1), out(1, 1))


KERB_PART = {"tl": "NW", "t": "N", "tr": "NE", "l": "W", "r": "E", "bl": "SW", "b": "S", "br": "SE",
             "in_nw": "inNW", "in_ne": "inNE", "in_sw": "inSW", "in_se": "inSE"}
QUAY_PART = KERB_PART


class Plan:
    """The ground plan, one character a cell:
      g grass   p aethos limestone path   f marble paving (kerbed against grass)
      y poros yard paving   q harbor quay (edged against the sea)   ~ sea
      s sand    t tilled earth (gardens, dig spots)
    Buildings go on top afterwards; the paving runs on under them."""

    def __init__(self, w, h, fill="g"):
        self.w, self.h = w, h
        self.rows = [[fill] * w for _ in range(h)]

    def fill(self, x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.rows[y][x] = ch

    def __getitem__(self, y):
        return self.rows[y]

    def __len__(self):
        return self.h

    def dump(self):
        return "\n".join("".join(r) for r in self.rows)


def paint(g, plan):
    """Lay the plan's ground into the grid."""
    P = plan
    for y in range(P.h):
        for x in range(P.w):
            c = P[y][x]
            if c == "~":
                g.set(x, y, SEA)
            elif c == "q":
                key = edge_key(*neighbours(P, x, y, "~"))
                if key == "c":
                    r = hashed(x, y, 1)
                    m = g.k("quay", "C2") if r < 0.14 else g.k("quay", "C")
                else:
                    m = g.k("quay", QUAY_PART[key])
                g.set(x, y, m)
            elif c == "s":
                key = edge_key(*neighbours(P, x, y, "~"))
                if key == "c":
                    n, s_, w_, e, *_ = neighbours(P, x, y, "g")
                    soft = edge_key(n, s_, w_, e, *[False] * 4)
                    g.set(x, y, SAND_GRASS[soft] if soft != "c" else SAND["c"])
                else:
                    g.set(x, y, SAND[key])
            elif c == "p":
                n, s_, w_, e, *_ = neighbours(P, x, y, "gt")
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e, *[False] * 4)
                g.set(x, y, PATH.get(key, PATH["c"]))
            elif c == "f":
                key = edge_key(*neighbours(P, x, y, "gpst~"))
                if key == "c":
                    r = hashed(x, y, 2)
                    part = ("flag_2" if r < 0.10 else "flag_4" if r < 0.17
                            else "drain" if r < 0.177 else "flag")
                    g.set(x, y, g.k("paving", part))
                else:
                    g.set(x, y, g.k("kerb", KERB_PART[key]))
            elif c == "y":
                if "yard" in g.cat:
                    g.set(x, y, g.k("yard"))
                else:
                    g.set(x, y, g.k("quay", "C"))
            elif c == "t":
                n, s_, w_, e, *_ = neighbours(P, x, y, "gpsfy")
                g.set(x, y, TILLED[edge_key(n, s_, w_, e, *[False] * 4)])
            else:
                g.set(x, y, GRASS)


def shade(g, plan):
    """Shadow the paving along the foot of tall fronts (TILES_emporion.md: paving)."""
    plain = {g.k("paving", p) for p in ("flag", "flag_2", "flag_4", "drain")}
    for y in range(1, g.h):
        for x in range(g.w):
            if int(g.mid[y, x]) not in plain or g.solid[y, x]:
                continue
            n = g.bldg[y - 1, x]
            w_ = x > 0 and g.bldg[y, x - 1]
            if n and w_:
                g.set(x, y, g.k("paving", "shade_nw"))
            elif n:
                g.set(x, y, g.k("paving", "shade_n"))
            elif w_:
                g.set(x, y, g.k("paving", "shade_w"))


def encode(g):
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mid[y, x])
            water = behavior(mid, g.sec) in SURF_BEHAVIORS
            elev = 1 if water else 3
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | (elev << 12)
    return out


def write_layout(g, name, border):
    d = ROOT / "data/layouts" / name
    d.mkdir(parents=True, exist_ok=True)
    encode(g).astype("<u2").tofile(d / "map.bin")
    np.array(border, np.uint16).astype("<u2").tofile(d / "border.bin")


def set_layout_size(layout_id, w, h):
    """Keep layouts.json's width and height in step with the builder."""
    path = ROOT / "data/layouts/layouts.json"
    text = path.read_text()
    pat = re.compile(r'("id": "%s",\s*"name": "[^"]+",\s*"width": )\d+(,\s*"height": )\d+' % layout_id)
    new, n = pat.subn(lambda m: f"{m.group(1)}{w}{m.group(2)}{h}", text)
    assert n == 1, f"{layout_id} not found in layouts.json"
    if new != text:
        path.write_text(new)


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def render(layout_id, map_name, w, h, secondary, out_dir, stem, screens):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / f"{stem}.png"
    subprocess.run(rm + [layout_id, "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    overlay(png, ROOT / f"data/layouts/{map_name}/map.bin", w, map_name, out_dir / f"{stem}_walk.png", 2)
    crops(map_name, w, h, secondary, out_dir, stem, screens)


def crops(map_name, w, h, secondary, out_dir, stem, screens, margin=8):
    """Crop GBA-screen views (15x10 tiles, the player on the 8th column and 5th row)
    from the map padded with its border, at 2x, and tile them into one sheet."""
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
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", secondary,
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    out = []
    for name, (px, py) in screens.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        crop.save(out_dir / f"{stem}_screen_{name}.png")
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
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5],
                  outline=(255, 255, 0, 255), width=2)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=2)
    for t in ev["coord_events"]:
        d.rectangle([t["x"] * c + 6, t["y"] * c + 6, t["x"] * c + c - 7, t["y"] * c + c - 7],
                    fill=(255, 0, 255, 160))
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


FLYERS = ("WINGULL",)
# People who stand on solid cells on purpose: sellers behind a counter, the
# snatcher on its awning, the statue on its plinth, the augur on the wall.
PERCHED = ("PERCH",)


def check_map(name, secondary, start, seams=(), scripted=None, still_people=True):
    """The common checks. seams: (kind, cells, rule) where kind 'rows'/'cols' lists
    the rows or columns that must use aethos only."""
    errors = []
    lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    layout = json.loads((ROOT / "data/maps" / name / "map.json").read_text())["layout"]
    entry = next(l for l in lay["layouts"] if l.get("id") == layout)
    w = entry["width"]
    blocks = np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, w)
    ev = json.loads((ROOT / "data/maps" / name / "map.json").read_text())
    warps = [(w_["x"], w_["y"]) for w_ in ev["warp_events"]]
    objects = {(o["x"], o["y"]) for o in ev["object_events"]}
    reach = reachable(blocks, start, extra_open=set(warps))
    for (x, y) in warps:
        b = behavior(int(blocks[y, x]) & 0x3FF, secondary)
        if b not in DOOR_BEHAVIORS:
            errors.append(f"{name}: warp at ({x},{y}) is on {b}, not a door")
        if (x, y) not in reach:
            errors.append(f"{name}: warp at ({x},{y}) is unreachable")
    # every door metatile has a warp: no barred doors (MAP_DESIGN.md §2)
    hh, ww = blocks.shape
    for y in range(hh):
        for x in range(ww):
            m = int(blocks[y, x]) & 0x3FF
            if behavior(m, secondary) in DOOR_BEHAVIORS and not (blocks[y, x] >> 10 & 3) and (x, y) not in warps:
                errors.append(f"{name}: door metatile at ({x},{y}) has no warp")
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if any(f in o["graphics_id"] for f in FLYERS) or any(p in o.get("local_id", "") for p in PERCHED):
            continue
        if not walkable(blocks, x, y):
            errors.append(f"{name}: object {o.get('local_id', o['graphics_id'])} at ({x},{y}) stands on a solid cell")
    for t in ev["coord_events"]:
        if (t["x"], t["y"]) not in reach:
            errors.append(f"{name}: coord event at ({t['x']},{t['y']}) is unreachable")
    # nobody may wall off a thing to read or a person to talk to, counting the
    # people who stand still as obstacles
    still = blocks.copy()
    for o in ev["object_events"]:
        if o["movement_type"] not in ("MOVEMENT_TYPE_WANDER_AROUND",) and 0 <= o["y"] < hh and 0 <= o["x"] < ww:
            still[o["y"], o["x"]] |= SOLID
    reach_still = reachable(still, start, extra_open=set(warps))
    targets = [(b["x"], b["y"], f"{b['type']} event") for b in ev["bg_events"]]
    targets += [(o["x"], o["y"], o.get("local_id", o["graphics_id"])) for o in ev["object_events"]
                if not any(f in o["graphics_id"] for f in FLYERS) and o["script"] not in ("0x0", "0")]
    for (x, y, what) in targets:
        fronts = []
        for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            fx, fy = x + dx, y + dy
            fronts.append((fx, fy))
            if 0 <= fx < ww and 0 <= fy < hh and behavior(int(blocks[fy, fx]) & 0x3FF, secondary) == "MB_COUNTER":
                fronts.append((fx + dx, fy + dy))      # talked to across a counter
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
                    errors.append(f"{name}: ({x},{y}) is {secondary} metatile 0x{m:03X}, within the {why} "
                                  f"seam's band; use aethos there")
    for who, cells in (scripted or {}).items():
        for (x, y) in cells:
            if not walkable(blocks, x, y):
                errors.append(f"{name}: {who}'s scripted path crosses solid ({x},{y})")
    return errors, reach, blocks


# ---------------------------------------------------------------------------
# Emporion City
# ---------------------------------------------------------------------------
#
# Corinth in its prime on a planned grid, south to north (SCRIPT.md, "Layout"):
#   the harbor road (an aethos band: the harbor district joins on the south seam),
#   the harbor quarter with the Asclepeion and the Deigma, the Agora with its stoa,
#   stalls, Pegasus and the tavern, the Temple of Hermes on its raised terrace at
#   the top of the main street, and the wooded slope of the crag behind it (an
#   aethos band, for Route 4 on the north seam). The Hephaisteion stands on its
#   hill above the Agora's west side, the potters' lane below it; the Isthmus road
#   runs up the west side to the Isthmus Gate, past the runners' house; the
#   households and the Peirene are in the grid streets east of the Agora; the
#   Nemea road (Route 14, Act II) leaves west from the harbor road, shut.

W, H = 48, 46
LAYOUT = "LAYOUT_EMPORION_CITY"
NAME = "EmporionCity"
MAIN = range(21, 26)           # the main street, quay to temple
ISTHMUS_SEAM = range(7, 10)    # the Isthmus Gate's road on the north seam (Route 4)
HARBOR_SEAM = MAIN             # the harbor road on the south seam (MAP_EMPORION_HARBOR)
SEAM_ROWS = 6                  # MAP_DESIGN.md §5
NEMEA_ROW = 41                 # the Nemea road (Route 14) on the west edge, shut in Act I


def city_plan():
    P = Plan(W, H)
    # the north band: the wooded slope, and the Isthmus road up through the gate
    P.fill(7, 0, 9, 5, "p")
    # the upper city: the Isthmus road, the Hephaisteion's forecourt, the terrace
    P.fill(7, 6, 9, 31, "f")
    P.fill(1, 12, 6, 13, "f")              # the Hephaisteion's forecourt
    P.fill(0, 8, 1, 10, "t")               # its garden
    P.fill(10, 10, 34, 13, "f")            # the temple terrace
    P.fill(20, 6, 26, 9, "f")              # under the temple
    P.fill(27, 8, 34, 9, "f")
    P.fill(11, 6, 15, 9, "f")              # under the runners' house
    P.fill(0, 14, 6, 14, "f")              # the Hephaisteion's terrace wall
    P.fill(10, 14, 34, 14, "f")            # the temple terrace wall
    P.fill(35, 6, 47, 8, "f")              # under the crag of Acrocorinth
    # the potters' lane under the hill
    P.fill(0, 15, 6, 23, "y")
    # the lane behind the stoa, the Agora, the grid east of it
    P.fill(7, 15, 34, 31, "f")
    P.fill(35, 17, 47, 31, "f")
    P.fill(35, 13, 37, 16, "f")            # the stair down from the east slope
    # the harbor quarter
    P.fill(8, 32, 47, 39, "f")
    # the south band: the harbor road and the Nemea road
    P.fill(MAIN.start, 40, MAIN.stop - 1, H - 1, "p")
    P.fill(0, NEMEA_ROW, MAIN.start - 1, NEMEA_ROW, "p")
    # gardens inside the grid
    P.fill(42, 17, 47, 21, "g")            # Philoxenos's garden
    P.fill(37, 24, 42, 31, "g")            # the neighbourhood garden
    P.fill(8, 33, 12, 38, "g")             # the Asclepeion's herb garden
    P.fill(9, 34, 11, 36, "t")
    P.fill(40, 33, 47, 38, "g")            # the cypress court east of the Deigma
    return P


def stoa(g, x, y, bays, bldg=True):
    g.put("stoa_end_w", x, y, bldg=bldg)
    cx = x + 1
    for b in bays:
        g.put(b, cx, y, bldg=bldg)
        cx += 2
    g.put("stoa_end_e", cx, y, bldg=bldg)
    return cx + 1


def house(g, x, y, recipe):
    """Lay a house from the kit: recipe rows of (key, part) or None."""
    for j, row in enumerate(recipe):
        for i, cell in enumerate(row):
            if cell is None:
                continue
            key, part = cell
            g.part(key, part, x + i, y + j)
            g.bldg[y + j, x + i] = True


def roof(width, chimney=None, acroterion=None):
    top = [("roof", "W")] + [("roof", "run")] * (width - 2) + [("roof", "E")]
    if chimney is not None:
        top[chimney] = ("roof", "chimney")
    if acroterion is not None:
        top[acroterion] = ("roof", "acroterion")
    eaves = [("roof", "eaves_W")] + [("roof", "eaves_run")] * (width - 2) + [("roof", "eaves_E")]
    return [top, eaves]


def storey(kind, parts):
    return [(kind, p) for p in parts]


def terrace_run(g, x0, x1, y, stairs=(), cistern=None):
    for x in range(x0, x1 + 1):
        if x in stairs:
            g.part("terrace_wall", "stairs", x, y)
        elif cistern is not None and x == cistern:
            g.part("terrace_wall", "cistern", x, y)
        elif cistern is not None and x == cistern + 1:
            g.part("terrace_wall", "cistern_sign", x, y)
        else:
            g.part("terrace_wall", "W" if x == x0 else "E" if x == x1 else "run", x, y)


def compose_city():
    g = Grid(W, H, "emporion")
    plan = city_plan()
    paint(g, plan)

    # ---- the north band: the crag's wooded slope and the Isthmus Gate -----------
    # The city wall runs across the slope; the gate is the gap where the road
    # climbs through it. Rows 0-5 sit on Route 4's seam: aethos only.
    g.wall_we(0, 6, 3)
    g.wall_we(10, W - 1, 3)
    g.set(5, 5, STELE, True)                           # THE ISTHMUS GATE
    g.trees(pines=((0, 0), (12, 0), (19, 1), (30, 0), (41, 1), (25, 1), (36, 0)),
            olives=((3, 0), (15, 1), (22, 0), (33, 1), (38, 1), (44, 0), (46, 1)),
            cypresses=((2, 1), (11, 1), (17, 0), (21, 1), (28, 0), (29, 1), (35, 1), (43, 1), (14, 0)))
    for (x, y) in ((5, 1), (27, 2), (40, 2), (18, 2)):
        if g.free(x, y):
            g.set(x, y, BOULDER, True)
    # cypresses stand behind the temple's roof and along the wall's inner side
    g.trees(cypresses=((18, 4), (28, 4), (13, 4), (31, 4), (36, 4), (42, 4)),
            olives=((0, 4), (2, 4), (15, 4), (33, 4), (38, 4), (41, 4), (46, 4)))

    # ---- the runners' house, beside the gate ---------------------------------
    # Dromokleia's day-runners: SCRIPT.md, the runners' house. Door (12,9).
    house(g, 11, 6, roof(5, chimney=3) + [
        storey("upper", ["W", "shutters", "wall", "grille", "E"]),
        storey("lower", ["W", "door", "wall", "window", "E"])])

    # ---- the Hephaisteion on its hill, the potters' lane below -----------------
    g.put("hephaisteion", 2, 8, bldg=True)            # doors (3,11), (4,11)
    terrace_run(g, 0, 6, 14)
    g.trees(olives=((0, 6), (4, 6)), cypresses=((6, 8), (2, 6)))
    g.cypress(6, 10)
    # Euphronios's workshop: the potter's narrow house, door (3,19), with his
    # kiln and pots drying in the yard
    house(g, 2, 16, roof(3, chimney=1) + [
        [("upper", "W"), ("signs", "potter"), ("upper", "E")],
        storey("lower", ["W", "door_arched", "E"])])
    g.put("kiln", 5, 16)
    g.put("vase_rack", 0, 21)
    g.put("vase_rack", 4, 21)
    g.put("kiln", 0, 16)

    # ---- the temple of Hermes on its terrace: the crown ------------------------
    g.put("temple_hermes", 20, 6, bldg=True)          # door (23,11), its steps row 12
    for x in (17, 19):
        g.put("planter", x, 11)
    for x in (27, 29):
        g.put("planter", x, 11)
    g.trees(cypresses=((16, 6), (18, 6), (27, 6), (34, 6)), olives=((32, 6),))
    g.put("peirene", 29, 8, bldg=True)
    terrace_run(g, 10, 34, 14, stairs=MAIN, cistern=31)
    g.put("steps", 21, 15, w=1, h=2)
    for x in range(22, 25):
        g.put("steps", x, 15, cx=1, w=1, h=2)
    g.put("steps", 25, 15, cx=2, w=1, h=2)

    # ---- the Agora --------------------------------------------------------------
    # the stoa on the square's north-west side, its counters and portico
    stoa(g, 10, 17, ["stoa_bay_pots", "stoa_bay_spice", "stoa_bay_cloth", "stoa_bay"])
    for x in range(10, 20):                             # its stylobate
        g.put("steps", x, 22, cx=0 if x == 10 else 2 if x == 19 else 1, cy=1, w=1, h=1)
    # the tavern, the Dolphin, on the square's north-east side; door (30,21)
    house(g, 28, 18, roof(5, acroterion=2) + [
        storey("upper", ["W", "arched"]) + [("signs", "tavern")] + storey("upper", ["arched", "E"]),
        storey("lower", ["W", "window", "door", "bench", "E"])])
    g.put("planter", 27, 20)
    g.put("planter", 33, 20)
    # the pithoi by the stoa (Pithound's jars): six jars on three racks
    for x in (10, 12, 14):
        g.put("vase_rack", x, 24)
    # the main street, quay to temple, is an avenue of laurels in great pots
    for y in (24, 28, 33):
        g.put("planter", 20, y)
        g.put("planter", 26, y)
    g.put("pegasus_column", 14, 25)
    g.put("plaza_rose", 22, 27)
    # the west market: two rows of stalls
    g.put("stall_fish", 10, 25)
    g.put("stall_pottery", 17, 25)        # the general stall, facing the main street
    g.put("stall_bronze", 10, 28)         # Pasion's table
    g.put("stall_wine", 13, 28)           # the offerings stall
    g.put("stall_honey", 16, 28)          # Kydon
    # the east market
    g.put("notice_board", 27, 22)         # THE AGORA
    g.put("stall_spice", 28, 25)          # Sykeas's figs
    g.put("stall_fish", 31, 25)
    g.put("stall_cloth", 28, 28)
    g.put("stall_wine", 31, 28)
    g.put("great_herm", 26, 30)           # the crossroads herm
    g.put("exedra", 31, 22)
    g.set(34, 23, TRIPOD[1], True)        # Number Nine's plinth
    g.put("exedra", 11, 31)
    g.put("exedra", 15, 31)
    # the Isthmus road down the Agora's west side is an avenue of laurels too
    for y in (17, 21, 25, 29):
        g.put("planter", 7, y)

    # ---- the crag of Acrocorinth over the east grid ------------------------------
    for i, x in enumerate(range(35, W)):
        col = 0 if x == 35 else 5 if x == W - 1 else 3 if x == 41 else 4 if x == 44 else 1 + i % 2
        g.put("acrocorinth", x, 6, cx=col, w=1)
    # ---- the east slope under it: olives, a shrine, the stair down -------------
    g.trees(olives=((38, 9), (45, 9), (36, 12), (42, 12), (40, 14), (46, 14)),
            cypresses=((40, 9), (47, 11), (39, 11), (44, 11), (38, 14), (43, 14)))
    g.block([[TRIPOD[0]], [TRIPOD[1]]], 42, 10)      # Hermes's tripod on the slope
    g.solid[10, 42] = False

    # ---- the grid east of the Agora --------------------------------------------
    # Philoxenos's house, three storeys tall; door (39,21)
    house(g, 37, 17, roof(5, chimney=2) + [
        storey("upper_rose", ["W", "arched", "shutters", "arched", "E"]),
        storey("upper_rose", ["W", "grille", "balcony_l", "balcony_r", "E"]),
        storey("lower_rose", ["W", "window", "door", "window", "E"])])
    # his garden, walled
    g.wall_we(42, 47, 22)
    g.trees(olives=((43, 17), (46, 19)), cypresses=((42, 18), (45, 17)))
    g.put("planter", 36, 20)
    # the widow's house, Penelopeia's, with a balcony; door (45,27)
    house(g, 43, 24, roof(4, chimney=1) + [
        storey("upper_rose", ["W", "balcony_l", "balcony_r", "E"]),
        storey("lower_rose", ["W", "bench", "door_arched", "E"])])
    # the neighbourhood's garden: walled, with Apollo's tripod among the olives,
    # its gate on the street at (40,24)
    g.wall_we(37, 39, 24)
    g.wall_we(41, 42, 24)
    g.trees(olives=((37, 25), (40, 28)), cypresses=((42, 25), (37, 29), (42, 29), (39, 30)))
    g.block([[TRIPOD[0]], [TRIPOD[1]]], 40, 26)
    g.solid[26, 40] = False
    g.put("exedra", 35, 28)
    g.put("planter", 44, 29)
    g.put("planter", 46, 29)

    # ---- the harbor quarter ---------------------------------------------------
    g.put("asclepeion", 14, 32, bldg=True)            # door (16,36)
    g.put("steps", 15, 37)
    stoa(g, 28, 32, ["stoa_bay", "stoa_bay_door", "stoa_bay", "stoa_bay"])   # the Deigma, door (32,36)
    for x in range(28, 38):
        g.put("steps", x, 37, cx=0 if x == 28 else 2 if x == 37 else 1, cy=1, w=1, h=1)
    g.trees(cypresses=((9, 32), (11, 32)))
    g.trees(cypresses=((40, 33), (42, 33), (44, 33), (46, 33), (41, 36), (45, 36)),
            olives=((43, 36),))
    g.put("planter", 13, 35)
    g.put("planter", 19, 35)
    g.put("planter", 38, 35)
    g.put("exedra", 29, 38)
    g.put("exedra", 34, 38)

    # ---- the south band: the harbor road, and the Nemea road (Route 14) -------
    # Rows 40-45 sit on the harbor's seam: aethos only.
    g.wall_we(0, 2, NEMEA_ROW - 1)
    g.wall_we(0, 2, NEMEA_ROW + 1)
    g.set(3, NEMEA_ROW - 1, STELE, True)               # THE NEMEA GATE
    g.set(20, 42, STELE, True)                         # the fork
    # the road out to the harbor is lined with cypresses; the gardens either side
    # are olives and stone pines, never in rows
    g.trees(cypresses=((20, 43), (26, 40), (26, 43), (19, 40), (27, 42), (18, 43)),
            pines=((9, 42), (33, 41), (44, 42)),
            olives=((4, 42), (13, 42), (15, 44), (29, 40), (37, 42), (40, 40), (46, 40),
                    (1, 44), (6, 44), (11, 44), (30, 44), (39, 44), (42, 44)))
    # the garden below the Asclepeion: Asclepius's tripod among the olives
    g.block([[TRIPOD[0]], [TRIPOD[1]]], 5, 34)
    g.solid[34, 5] = False
    g.trees(olives=((0, 32), (2, 34), (5, 37), (0, 38)),
            pines=((1, 36),),
            cypresses=((6, 32), (3, 32), (7, 35), (3, 37)))
    g.trees(olives=((0, 25), (3, 26), (1, 29), (5, 29)), pines=((3, 28),),
            cypresses=((5, 24), (6, 26), (2, 24), (0, 27)))

    g.flowers([(1, 5), (4, 4), (14, 5), (25, 4), (37, 5), (42, 5), (12, 43), (7, 45), (18, 45),
               (29, 43), (35, 45), (45, 40), (3, 31), (6, 30), (0, 28), (9, 39), (44, 39),
               (38, 12), (46, 11), (36, 15), (43, 20), (47, 21)])
    g.close_edge(0, ISTHMUS_SEAM)
    g.close_edge(H - 1, HARBOR_SEAM)
    shade(g, plan)
    return g


def border_city():
    return [OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]]


# Where the player stands for each screen-sized review crop, along the route.
SCREENS = {
    "1_harbor_road": (23, 42), "2_asclepeion": (17, 37), "3_deigma": (31, 37),
    "4_agora_south": (21, 29), "5_agora_north": (16, 23), "6_tavern": (30, 23),
    "7_temple": (23, 13), "8_gate": (9, 6), "9_hephaisteion": (4, 13),
    "10_potters": (3, 20), "11_east_grid": (40, 25), "12_nemea": (5, 41),
}

# Cells the scenes walk people across: they must stay open.
SCRIPTED_PATHS = {
    # beat 14: Kleon from the temple door (23,12) down the steps, then west along
    # the lane under the terrace, out of sight
    "Kleon (beat 14)": [(23, y) for y in range(12, 16)] + [(x, 15) for x in range(14, 24)],
    # beat 16: Kleon from the gateway (8,3) up the Isthmus road and off the north edge
    "Kleon (beat 16)": [(8, y) for y in range(0, 4)],
    # the player, drawn to the middle of the temple stair and of the gate's road
    "Player": [(x, 16) for x in range(21, 26)] + [(x, 4) for x in range(7, 10)],
    # Number Nine steps off his plinth (34,23): north past the tavern, or east
    "Number Nine": [(34, y) for y in range(16, 23)] + [(x, 23) for x in range(35, W)],
}


def check_city():
    errors, reach, blocks = check_map(
        NAME, "emporion", start=(23, H - 1),
        seams=(("rows", range(0, SEAM_ROWS), "Route 4 (north)"),
               ("rows", range(H - SEAM_ROWS, H), "harbor (south)"),
               ("cols", range(0, 8), "Route 14 (west)")),
        scripted=SCRIPTED_PATHS)
    # the west-seam rule only binds the rows a player on Route 14 would see
    errors = [e for e in errors if "Route 14" not in e or int(re.search(r",(\d+)\)", e).group(1)) >= 32]
    # The Deigma's door is the stoa's door bay, which the tileset doesn't mark
    # MB_NON_ANIMATED_DOOR: a coord trigger on it does the warp (DeigmaDoor).
    errors = [e for e in errors if "(32,36) is on MB_NORMAL" not in e]
    for x in range(W):
        top, bot = walkable(blocks, x, 0), walkable(blocks, x, H - 1)
        if top != (x in ISTHMUS_SEAM):
            errors.append(f"{NAME}: north seam column {x} is {'open' if top else 'closed'}")
        if bot != (x in HARBOR_SEAM):
            errors.append(f"{NAME}: south seam column {x} is {'open' if bot else 'closed'}")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR", help="also render the map into DIR")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--plan", action="store_true", help="print the ground plan")
    args = ap.parse_args()
    if args.plan:
        print(city_plan().dump())
    g = compose_city()
    set_layout_size(LAYOUT, W, H)
    write_layout(g, NAME, border_city())
    if args.render:
        render(LAYOUT, NAME, W, H, "emporion", args.render, "emporion_city", SCREENS)
    if not args.no_check:
        errors = check_city()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("emporion: layout written, checks pass")


if __name__ == "__main__":
    main()
