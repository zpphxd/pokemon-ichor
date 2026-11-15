#!/usr/bin/env python3
"""Build the Gulf crossing (SCRIPT.md beat 37): Kirrha, the Gulf ferry's deck and
Aigion. Layouts, events, renders and checks.

Writes, for each of MAP_KIRRHA (36x30, aethos + kirrha), MAP_GULF_FERRY_DECK
(20x12, aethos + gulf_ferry) and MAP_AIGION (28x24, aethos + aigion):
  data/layouts/<Map>/map.bin, border.bin; the layout's entry in layouts.json
  data/maps/<Map>/map.json   (header, connections, people, warps, triggers, signs)

Kirrha is Delphoi's harbor at the head of the Krisaian gulf (SCRIPT.md Part 2,
"Kirrha"): the road from the Split Road comes in at the north-east and runs down
past Strophios's inn; the one street drops to the quay along the south, with the
fish market under the old fig and the Agora's shed at its head and Panopeus's
ferry at its east end; the muleteer and the old sweeper face each other across
the street; west, behind a low fence, Apollo's unploughed plain runs to the
gulf's shore; above everything the grey cliffs of Parnassos, and in the cleft of
the Phaidriades the sacred road climbs to Delphoi's roofs, shut by the pilgrims'
gate and the Pythia's guards.

Aigion is an Achaean port on a terrace across the gulf (Part 2, "Aigion"): the
quay along the north, Helike's roofs under the water off its west end, a steep
street climbing south past the old Achaean's and the goatherd's houses, the ring
of old planes round the altar of Zeus on the terrace above, and the road south
into the gorge (Route 11, batch 3).

The deck is Panopeus's ferry under way (Part 2, "The Gulf ferry"): reached only by
scripted warps from either quay.

Metatile ids come from build/<set>/catalog.json (design/phase3/TILES_kirrha.md).
Make them with  /usr/bin/python3 tools/ichor/art/kirrha_build.py all

Usage: /usr/bin/python3 tools/ichor/maps/harbors.py [--render DIR] [--no-check] [map ...]
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
# aethos ids (TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
GRASS_LEDGE = 0x002
GRASS_SHADE = 0x01C      # grass in deep shade: the closed ground under the trees
FLOWERS = 0x004
STELE = 0x003
HERM = 0x01B
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
BOULDER = 0x0E0
BOULDER_SAND = 0x0E2
SEA = 0x170
SAND = 0x124
SAND_EDGE = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "r": 0x125,
             "bl": 0x12B, "b": 0x12C, "br": 0x12D}
FALLS = 0x0BB
FALLS_FOAM = 0x0C1
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER", "MB_INTERIOR_DEEP_WATER",
                  "MB_WATERFALL"}
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
AETHOS_ATTR = np.fromfile(ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin", "<u2")


def hashed(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, tileset, w, h):
        self.ts = tileset
        self.W, self.H = w, h
        self.mid = np.full((h, w), GRASS, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.built = np.zeros((h, w), bool)
        self.cat = {s["key"]: s for s in json.loads((ROOT / f"build/{tileset}/catalog.json").read_text())}
        self.attr = np.fromfile(ROOT / f"data/tilesets/secondary/{tileset}/porytiles_bin/"
                                "metatile_attributes.bin", "<u2")

    def behavior(self, mid):
        if mid < 0x200:
            return MB.get(int(AETHOS_ATTR[mid]) & 0xFF, "?")
        return MB.get(int(self.attr[mid - 0x200]) & 0xFF, "?")

    def inside(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def set(self, x, y, mid, solid=False, built=True):
        if self.inside(x, y):
            self.mid[y, x] = mid
            self.solid[y, x] = solid
            if built:
                self.built[y, x] = True

    def part(self, key, name):
        s = self.cat[key]
        cx, cy = s["names"][name]
        return s["ids"][cy][cx], s["walk"][cy][cx]

    def put_part(self, key, name, x, y):
        mid, walk = self.part(key, name)
        self.set(x, y, mid, walk == "X")

    def cell(self, key, cx, cy, x, y):
        s = self.cat[key]
        self.set(x, y, s["ids"][cy][cx], s["walk"][cy][cx] == "X")

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.cell(key, cx + i, cy + j, x + i, y + j)

    def recipe(self, rows, x, y, kit="house", signs="house_signs"):
        for j, row in enumerate(rows):
            for i, part in enumerate(row):
                key = kit if part in self.cat[kit]["names"] else signs
                self.put_part(key, part, x + i, y + j)

    def free(self, x, y, w=1, h=1):
        return all(self.inside(x + i, y + j) and self.mid[y + j, x + i] in (GRASS, FLOWERS)
                   and not self.solid[y + j, x + i] and not self.built[y + j, x + i]
                   for j in range(h) for i in range(w))

    # -- aethos trees -------------------------------------------------------
    def olive(self, x, y):
        below = y + 2 < self.H and self.mid[y + 2, x] == OLIVE_TOP[0]
        for i in range(2):
            self.set(x + i, y, OLIVE_TOP[i], True)
            self.set(x + i, y + 1, (OLIVE_BOT_TIP if below else OLIVE_BOT)[i], True)
        if y > 0:
            above = (int(self.mid[y - 1, x]), int(self.mid[y - 1, x + 1]))
            if above == OLIVE_BOT:
                for i in range(2):
                    self.set(x + i, y - 1, OLIVE_BOT_TIP[i], True)
            elif all(m in (GRASS, FLOWERS) for m in above) and not self.built[y - 1, x] \
                    and not self.built[y - 1, x + 1]:
                for i in range(2):
                    self.set(x + i, y - 1, OLIVE_TIP_GRASS[i], bool(self.solid[y - 1, x + i]),
                             built=False)

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def pine(self, x, y):
        for j in range(2):
            for i in range(2):
                self.set(x + i, y + j, PINE[j][i], True)

    # -- the cliff kit ----------------------------------------------------
    def cliff(self, x0, x1, y_rim, faces, open_left=True, open_right=True, rim=True, foot=True):
        """A grey cliff band over columns x0..x1: the rim at y_rim (skipped when
        rim=False: the cliff runs on above the map), `faces` face rows A, B, A...
        below it, then the foot. open_left/right: draw the end flank (False when
        the band continues into another piece)."""
        y = y_rim
        rows = []
        if rim:
            rows.append("rim")
            y += 1
        for k in range(faces):
            rows.append("faceA" if k % 2 == 0 else "faceB")
        if foot:
            rows.append("footB" if faces % 2 == 0 else "footA")
        y = y_rim
        for row in rows:
            for x in range(x0, x1 + 1):
                if x == x0 and open_left:
                    col = "l"
                elif x == x1 and open_right:
                    col = "r"
                else:
                    col = "m0" if x % 2 == 0 else "m1"
                self.put_part("cliff", f"{row}_{col}", x, y)
            y += 1


def edge_key(n, s_, w_, e):
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
    return "c"


def lay_path(g, cells):
    """Aethos's path patch over a set of cells, edged where it meets grass."""
    for (x, y) in cells:
        n, s_, w_, e = [((xx, yy) not in cells) for (xx, yy) in
                        ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))]
        key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e)
        g.set(x, y, PATH.get(key, PATH["c"]), False, built=False)


def lay_quay(g, cells, sea):
    """The grey quay over a set of cells, its edges and corners chosen by where the
    sea lies around it (the quay's edge pieces show coping or the wet face)."""
    Q = {"nw": (0, 0), "n": (1, 0), "ne": (2, 0), "in_nw": (3, 0), "in_ne": (4, 0),
         "w": (0, 1), "c": (1, 1), "e": (2, 1), "in_sw": (3, 1), "in_se": (4, 1),
         "sw": (0, 2), "s": (1, 2), "se": (2, 2), "c2": (3, 2), "c3": (4, 2)}
    for (x, y) in cells:
        def w(dx, dy):
            return (x + dx, y + dy) in sea
        n, s_, wst, e = w(0, -1), w(0, 1), w(-1, 0), w(1, 0)
        if n and wst:
            k = "nw"
        elif n and e:
            k = "ne"
        elif s_ and wst:
            k = "sw"
        elif s_ and e:
            k = "se"
        elif n:
            k = "n"
        elif s_:
            k = "s"
        elif wst:
            k = "w"
        elif e:
            k = "e"
        elif w(-1, -1):
            k = "in_nw"
        elif w(1, -1):
            k = "in_ne"
        elif w(-1, 1):
            k = "in_sw"
        elif w(1, 1):
            k = "in_se"
        else:
            r = hashed(x, y, 41)
            k = "c2" if r < 0.06 else ("c3" if r < 0.1 else "c")
        g.cell("quay", *Q[k], x, y)


def lay_sand(g, cells):
    """Aethos's beach: sand inside, and round it the sand-edge tiles, which are
    water (surfable) with the sand's rim curving into them."""
    for (x, y) in cells:
        g.set(x, y, SAND, False, built=False)


def sand_rim(g, rim):
    """rim: {(x, y): key} with key in SAND_EDGE: the water cells round a beach."""
    for (x, y), k in rim.items():
        g.set(x, y, SAND_EDGE[k], False, built=False)


def fill_trees(g, zone, salt=21, pines=0.12, olives=0.62):
    """Fill a zone of free grass with aethos's olives, pines and cypresses, mixed in
    uneven depth; what's left is scrub and rock, closed."""
    cands = sorted(zone, key=lambda c: hashed(c[0], c[1], salt))
    zs = set(zone)
    for (x, y) in cands:
        r = hashed(x, y, salt + 2)
        two = all((x + i, y + j) in zs for i in (0, 1) for j in (0, 1)) and g.free(x, y, 2, 2)
        if r < olives and two:
            g.olive(x, y)
        elif r < olives + pines and two:
            g.pine(x, y)
    for (x, y) in cands:
        if (x, y + 1) in zs and g.free(x, y, 1, 2) and hashed(x, y, salt + 5) < 0.75:
            g.cypress(x, y)
    # what's left: a rock where the grove meets open ground (so a gap never reads as
    # a way in), open grass inside it, sealed off by the trees and rocks round it
    for (x, y) in cands:
        if not g.free(x, y):
            continue
        rim = any(not g.inside(x + dx, y + dy) or ((x + dx, y + dy) not in zs and
                                                   not g.solid[y + dy, x + dx])
                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if rim:
            g.set(x, y, BOULDER, True)
        else:
            g.set(x, y, GRASS, False)


def encode(g):
    out = np.zeros((g.H, g.W), np.uint16)
    for y in range(g.H):
        for x in range(g.W):
            mid = int(g.mid[y, x])
            water = g.behavior(mid) in SURF_BEHAVIORS
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | ((1 if water else 3) << 12)
    return out


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def obj(local_id, gfx, x, y, script, flag="0", move="MOVEMENT_TYPE_FACE_DOWN", trainer=False,
        sight=0, rx=0, ry=0, item=None):
    return {
        "local_id": local_id, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": move, "movement_range_x": rx, "movement_range_y": ry,
        "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": item if item else str(sight),
        "script": script, "flag": flag,
    }


def item_ball(local_id, x, y, item, flag):
    return obj(local_id, "OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag,
               item=item)


def sign(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
            "quantity": 1, "underfoot": False}


def trigger(x, y, var, value, script):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": str(value),
            "script": script}


# ---------------------------------------------------------------------------
# writing
# ---------------------------------------------------------------------------

def write_layout(name, layout_id, g, border, secondary):
    laydir = ROOT / f"data/layouts/{name}"
    laydir.mkdir(parents=True, exist_ok=True)
    encode(g).astype("<u2").tofile(laydir / "map.bin")
    np.array(border, np.uint16).astype("<u2").tofile(laydir / "border.bin")
    lj = ROOT / "data/layouts/layouts.json"
    t = lj.read_text()
    new = (f'"id": "{layout_id}",\n      "name": "{name}_Layout",\n      "width": {g.W},\n'
           f'      "height": {g.H},\n      "primary_tileset": "gTileset_Aethos",\n'
           f'      "secondary_tileset": "{secondary}",')
    t2 = re.sub(rf'"id": "{layout_id}",\s*"name": "{name}_Layout",\s*"width": \d+,\s*'
                r'"height": \d+,\s*"primary_tileset": "\w+",\s*"secondary_tileset": "\w+",', new, t)
    assert f'"secondary_tileset": "{secondary}"' in t2, layout_id
    if t2 != t:
        lj.write_text(t2)


def write_map_json(name, header, objects, warps, coords, bgs):
    path = ROOT / f"data/maps/{name}/map.json"
    d = json.loads(path.read_text())
    d.update(header)
    d.update({"object_events": objects, "warp_events": warps, "coord_events": coords,
              "bg_events": bgs})
    path.write_text(json.dumps(d, indent=2) + "\n")


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 != 1


def reachable(blocks, start, blocked=()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in seen and p not in blocked and walkable(blocks, *p):
                seen.add(p)
                q.append(p)
    return seen


def common_checks(g, name, start, extra_blocked=(), unreachable_ok=(), solid_ok=()):
    """Warps sit on doors reached from their doorsteps; every person, item, trigger
    and sign can be reached; returns (errors, reach)."""
    errors = []
    blocks = np.fromfile(ROOT / f"data/layouts/{name}/map.bin", "<u2").reshape(g.H, g.W)
    ev = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
    reach = reachable(blocks, start, blocked=set(extra_blocked))
    objects = {(o["x"], o["y"]) for o in ev["object_events"]}
    for w_ in ev["warp_events"]:
        x, y = w_["x"], w_["y"]
        b = g.behavior(int(blocks[y, x]) & 0x3FF)
        if b not in DOOR_BEHAVIORS:
            errors.append(f"{name}: warp at ({x},{y}) to {w_['dest_map']} is on {b}, not a door")
        if (x, y + 1) not in reach:
            errors.append(f"{name}: warp at ({x},{y}) can't be reached from its doorstep")
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if o["local_id"] in solid_ok:
            continue
        if not walkable(blocks, x, y):
            errors.append(f"{name}: object {o['local_id']} at ({x},{y}) stands on a solid cell")
            continue
        if o["local_id"] in unreachable_ok:
            continue
        near = [(x, y)] + [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if not any(p in reach for p in near):
            errors.append(f"{name}: object {o['local_id']} at ({x},{y}) is unreachable")
    for t in ev["coord_events"]:
        if (t["x"], t["y"]) not in reach:
            errors.append(f"{name}: coord event at ({t['x']},{t['y']}) is unreachable")
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        if b["type"] == "hidden_item" and (x, y) in unreachable_ok:
            continue
        fronts = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y), (x, y)]
        if not any(p in reach and p not in objects for p in fronts):
            errors.append(f"{name}: bg event at ({x},{y}) can't be read from a walkable tile")
    return errors, reach, blocks


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def render(name, layout_id, out_dir, secondary_dir, screens=None, margin=8):
    from PIL import Image, ImageDraw
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / f"{name}.png"
    subprocess.run(rm + [layout_id, "--scale", "2", "-o", str(png)], check=True,
                   stdout=subprocess.DEVNULL)
    ev = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
    # people and events overlay
    im = Image.open(png).convert("RGBA")
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 32
    blocks = np.fromfile(ROOT / f"data/layouts/{name}/map.bin", "<u2")
    W = im.size[0] // c
    blocks = blocks.reshape(-1, W)
    for y, row in enumerate(blocks):
        for x, b in enumerate(row):
            if b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 60))
            elif b >> 12 == 1:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 80, 255, 50))
    for o in ev["object_events"]:
        x, y = o["x"] * c, o["y"] * c
        col = (250, 210, 60, 255) if "ITEM" in o["graphics_id"] else \
            (230, 80, 80, 255) if o["trainer_type"] != "TRAINER_TYPE_NONE" else (90, 170, 255, 255)
        d.ellipse([x + 8, y + 2, x + 23, y + 13], fill=col, outline=(20, 20, 20, 255))
        d.rectangle([x + 10, y + 13, x + 21, y + 29], fill=col, outline=(20, 20, 20, 255))
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=2)
    for t in ev["coord_events"]:
        d.rectangle([t["x"] * c + 8, t["y"] * c + 8, t["x"] * c + c - 9, t["y"] * c + c - 9],
                    fill=(255, 0, 255, 170))
    for b in ev["bg_events"]:
        col = (255, 255, 255, 255) if b["type"] == "sign" else (255, 160, 0, 255)
        d.line([b["x"] * c + 4, b["y"] * c + 4, b["x"] * c + c - 5, b["y"] * c + c - 5], fill=col, width=2)
        d.line([b["x"] * c + c - 5, b["y"] * c + 4, b["x"] * c + 4, b["y"] * c + c - 5], fill=col, width=2)
    Image.alpha_composite(im, lay).save(out_dir / f"{name}_events.png")
    # 15x10 screens, with the border round the map
    if screens:
        H = blocks.shape[0]
        bord = np.fromfile(ROOT / f"data/layouts/{name}/border.bin", "<u2").reshape(2, 2)
        big = np.empty((H + 2 * margin, W + 2 * margin), np.uint16)
        for y in range(big.shape[0]):
            for x in range(big.shape[1]):
                big[y, x] = bord[y % 2, x % 2]
        big[margin:margin + H, margin:margin + W] = blocks
        tmp = out_dir / f"{name}_padded.bin"
        big.astype("<u2").tofile(tmp)
        pad = out_dir / f"{name}_padded.png"
        subprocess.run(rm + ["--blockdata", str(tmp), "--width", str(big.shape[1]), "--primary",
                             "aethos", "--secondary", secondary_dir, "--scale", "2", "-o", str(pad)],
                       check=True, stdout=subprocess.DEVNULL)
        pim = Image.open(pad)
        crops = []
        for sname, (px, py) in screens.items():
            x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
            crops.append(pim.crop((x0, y0, x0 + 15 * c, y0 + 10 * c)))
        cols = 2
        sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8,
                                  -(-len(crops) // cols) * (10 * c + 8) - 8), (24, 24, 32))
        for i, crop in enumerate(crops):
            sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
        sheet.save(out_dir / f"{name}_screens.png")
        tmp.unlink()
        pad.unlink()
    return png


# ---------------------------------------------------------------------------
# the three maps live in their own modules
# ---------------------------------------------------------------------------

def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import harbors_kirrha
    import harbors_deck
    import harbors_aigion
    mods = {"kirrha": harbors_kirrha, "deck": harbors_deck, "aigion": harbors_aigion}
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("maps", nargs="*", default=list(mods))
    ap.add_argument("--render", metavar="DIR", help="also render the maps into DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    errors = []
    for m in args.maps:
        mod = mods[m]
        g = mod.build()
        if args.render:
            print(mod.render(args.render))
        if not args.no_check:
            errors += mod.check(g)
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(1)
    if not args.no_check:
        print("harbors: layouts and events written, checks pass")


if __name__ == "__main__":
    main()
