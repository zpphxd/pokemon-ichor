#!/usr/bin/env python3
"""Build Aegina Town: the island harbor where the Euploia puts in for the night.

Writes data/layouts/AeginaTown/map.bin and border.bin (30x24, aethos + aegina),
then checks the map against its map.json: the arrival tile and the doors, people
and signs on walkable ground, every bg event readable, the north gate the only
way off the island (its columns open on the seam, and shut on the voyage night),
and the scripted walks clear.

Aegina metatile ids come from build/aegina/catalog.json (TILES_aegina.md). Make it
with  /usr/bin/python3 tools/ichor/art/aegina_build.py --no-compile

Usage: /usr/bin/python3 tools/ichor/maps/aegina.py [--render DIR]
  --render writes aegina_town.png (2x), aegina_town_walk.png (collision and
  events) and aegina_screens.png (every 15x10 view along the player's route) into
  DIR, and each view on its own into build/aegina_render/. The renders in
  design/phase2/img/ come from --render design/phase2/img.
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
CAT = ROOT / "build/aegina/catalog.json"
LAYOUT = ROOT / "data/layouts/AeginaTown"
MAPJSON = ROOT / "data/maps/AeginaTown/map.json"
W, H = 30, 24

# The north gate: the walkable columns on the seam with the Aphaia Road (a map
# connection, up). Both maps share the aegina secondary, so the seam rows may use
# Aegina's pieces (MAP_DESIGN.md §5).
GATE_X = 23                 # the gate structure's left pier
GATE_COLS = (24, 25)        # its passage: the seam's walkable columns
GATE_Y = 1                  # the gate's top row; its passage runs rows 1-3
ARRIVAL = (12, 12)          # stepping off the Euploia's gangplank onto the quay

# ---------------------------------------------------------------------------
# aethos ids (TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
FLOWERS = 0x004
TALL = 0x00D
SEA = 0x170
STELE = 0x003
HERM = 0x01B
BOULDER = 0x0E0
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
UPINE = ((0x01E, 0x01F), (0x026, 0x027))     # aethos's umbrella pine, 2x2
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A, "w": 0x132, "e": 0x133}
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}
SAND = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "c": 0x124, "r": 0x125,
        "bl": 0x12B, "b": 0x12C, "br": 0x12D,
        "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER"}
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
AEGINA_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/aegina/porytiles_bin/metatile_attributes.bin", "<u2")


def behavior(mid):
    a = AETHOS_ATTR[mid] if mid < 0x200 else AEGINA_ATTR[mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    """A stable pseudo-random number in [0, 1) for a map cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def edge_key(n, s_, w_, e, nw=False, ne=False, sw=False, se=False):
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


def neighbours(plan, x, y, outside, edge_out=False):
    h, w = len(plan), len(plan[0])

    def out(dx, dy):
        x2, y2 = x + dx, y + dy
        if not (0 <= x2 < w and 0 <= y2 < h):
            return edge_out
        return plan[y2][x2] in outside
    return (out(0, -1), out(0, 1), out(-1, 0), out(1, 0), out(-1, -1), out(1, -1), out(-1, 1), out(1, 1))


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mid = np.full((h, w), SEA, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.cat = {s["key"]: s for s in json.loads(CAT.read_text())}

    def set(self, x, y, mid, solid=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def k(self, key, cx=0, cy=0):
        return self.cat[key]["ids"][cy][cx]

    def put(self, key, x, y):
        """Place an aegina structure; collision follows its walk grid ('X' solid),
        and '-' cells are left as they are."""
        s = self.cat[key]
        for j in range(s["h"]):
            for i in range(s["w"]):
                if s["walk"][j][i] == "-":
                    continue
                self.set(x + i, y + j, s["ids"][j][i], s["walk"][j][i] == "X")

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
            elif all(m in (GRASS, FLOWERS) for m in above):
                self.block([OLIVE_TIP_GRASS], x, y - 1, solid=bool(self.solid[y - 1, x]))

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def upine(self, x, y):
        self.block(UPINE, x, y)

    def free(self, x, y, w=1, h=1, ok=None):
        ok = ok or (GRASS,)
        return all(0 <= x + i < self.w and 0 <= y + j < self.h
                   and self.mid[y + j, x + i] in ok and not self.solid[y + j, x + i]
                   for j in range(h) for i in range(w))


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------
#
# An island town round a round harbor. The Euploia lies in the basin against the
# waterfront quay; two moles close the basin to the north, a beacon on each head,
# with the harbor mouth between them and the open sea beyond. To the west the
# Kolona headland rises in dry grass to the old column, the first thing a ship
# sees. The waterfront runs east past the inn to the mint's square and its
# turtle mosaic; a lane climbs north-east through the ant hills to Aiakides's
# house and the gate to the Aphaia Road. South of town, pistachios, then the beach.
#
#   ~ sea   s sand   g grass   d dry grass   p limestone path   q quay
#   B a structure's footprint (its ground doesn't matter)
#
# Columns 0..29; the sea runs round the whole island, so the border is sea.

PLAN = [
    #         1111111111222222222
    # 234567890123456789012345678 9
    "~~~~~~~~~~~~~~~~~~~~~sddppdgg~",  # 0   the road north, beyond the gate
    "~~sss~~~~~~~~~~~~~~~~sdppppdg~",  # 1
    "~sddds~~~~~~~~~~~~~~sgdppppdg~",  # 2
    "~sddddqqqqqq~~qqqqqqgggppppgg~",  # 3   the moles; the town wall and gate
    "~sddddqqqqqq~~qqqqqqggddppdgs~",  # 4
    "~sddddq~~~~~~~~~~~~qggddppdds~",  # 5   the round basin
    "~sddddq~~~~~~~~~~~~qgdddppggg~",  # 6
    "~sddddq~~~~~~~~~~~~qgdddppggg~",  # 7   Kolona's foot
    "~sddpdq~~~~~~~~~~~~qgdddppggg~",  # 8
    "~sgdpgq~~~~~~~~~~~~qgdddpppps~",  # 9
    "~sggpgq~~~~~~~~~~~~qggddppdds~",  # 10
    "~sggppqqqqqqqqqqqqqqpppppppps~",  # 11  the waterfront
    "~sgggpqqqqqqqqqqqqqqpppppppps~",  # 12
    "~~sggppppppppBBBBBppBBBpggggs~",  # 13  the inn, the mint
    "~~sgggggggpggBBBBBppBBBpgdds~~",  # 14
    "~~sgggggggpggBBBBBppBBBpdddgs~",  # 15
    "~ssgggggggpggBBBBBppBBBpddggs~",  # 16
    "~sgggggggppppppppppppppppgggs~",  # 17  the lane from the inn to the square
    "~sgggggggpggggggggppppppggss~~",  # 18  the mint's square
    "~~sgggggspgggggggsppppppgss~~~",  # 19
    "~~~sssssssssssss~ssssssssss~~~",  # 20  the beach
    "~~~~~sssssss~~~~~~ssssss~~~~~~",  # 21
    "~~~~~~~sss~~~~~~~~~~~~~~~~~~~~",  # 22
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",  # 23
]


def plan_rows():
    for i, r in enumerate(PLAN):
        assert len(r) == W, f"plan row {i} is {len(r)} wide"
    assert len(PLAN) == H
    return PLAN


# ---------------------------------------------------------------------------
# ground
# ---------------------------------------------------------------------------

def ground(g, plan):
    q = lambda cx, cy: g.k("quay", cx, cy)
    quay_pieces = {"tl": q(0, 0), "t": q(1, 0), "tr": q(2, 0), "l": q(0, 1), "r": q(2, 1),
                   "bl": q(0, 2), "b": q(1, 2), "br": q(2, 2),
                   "in_nw": q(3, 0), "in_ne": q(4, 0), "in_sw": q(3, 1), "in_se": q(4, 1)}
    dg = lambda cx, cy: g.k("dry_grass", cx, cy)
    dry_pieces = {"tl": dg(0, 0), "t": dg(1, 0), "tr": dg(2, 0), "l": dg(0, 1), "c": dg(1, 1),
                  "r": dg(2, 1), "bl": dg(0, 2), "b": dg(1, 2), "br": dg(2, 2),
                  "in_nw": dg(3, 0), "in_ne": dg(4, 0), "in_sw": dg(3, 1), "in_se": dg(4, 1)}
    for y, row in enumerate(plan):
        for x, c in enumerate(row):
            if c == "~":
                g.set(x, y, SEA)
            elif c == "q":
                key = edge_key(*neighbours(plan, x, y, "~"))
                if key == "c":
                    g.set(x, y, q(1, 1) if hashed(x, y, 1) > 0.3 else q(3 + (x % 2), 2))
                else:
                    g.set(x, y, quay_pieces[key])
            elif c == "s":
                key = edge_key(*neighbours(plan, x, y, "~", edge_out=True))
                if key == "c":
                    n, s_, w_, e, *_ = neighbours(plan, x, y, "gdp")
                    soft = edge_key(n, s_, w_, e)
                    g.set(x, y, SAND_GRASS[soft] if soft != "c" else SAND["c"])
                else:
                    g.set(x, y, SAND[key])
            elif c == "d":
                key = edge_key(*neighbours(plan, x, y, "gps"))
                if key == "c" and hashed(x, y, 3) < 0.15:
                    g.set(x, y, dg(3 + (x % 2), 2))      # a pebble
                else:
                    g.set(x, y, dry_pieces[key])
            elif c == "p":
                n, s_, w_, e, *_ = neighbours(plan, x, y, "gd")
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e)
                g.set(x, y, PATH.get(key, PATH["c"]))
            else:
                g.set(x, y, GRASS)


def wall_run(g, x0, x1, y):
    for x in range(x0, x1 + 1):
        g.set(x, y, WALL["l"] if x == x0 else WALL["r"] if x == x1 else WALL["run"], True)


def compose(gate_shut=False):
    plan = plan_rows()
    g = Grid(W, H)
    ground(g, plan)

    # ---- the round harbor ---------------------------------------------------
    g.put("basin_nw", 6, 4)
    g.put("basin_ne", 17, 4)
    g.put("basin_sw", 6, 9)
    g.put("basin_se", 17, 9)
    g.put("mole_head_e", 10, 3)                  # the west mole's head, its beacon
    g.put("mole_head_w", 14, 3)                  # the east mole's head
    # the north rim between the corners and the heads is a mole two cells thick:
    # coping on the open sea (row 3), the wall face over the basin (row 4)
    for x in (6, 7, 8, 9, 16, 17, 18, 19):
        g.set(x, 3, g.k("quay", 1, 0))
    for x in (9, 16):
        g.set(x, 4, g.k("quay", 1, 2))
    g.set(19, 3, g.k("quay", 2, 0))              # the mole's corner on the open sea
    g.set(6, 3, g.k("quay", 0, 0))
    # the Euploia at her berth, her gangplank down to the quay; kaikia in the basin
    g.put("trireme", 9, 8)
    g.set(12, 11, g.k("quay_gangplank"))
    g.put("boat_kaiki", 8, 5)
    g.put("boat_kaiki_left", 14, 6)
    g.set(10, 11, g.k("bollard_line"), True)     # the Euploia's stern and bow lines
    g.set(15, 11, g.k("bollard_line"), True)
    # harbor goods at the quay's west end
    g.put("amphora_stack", 6, 12)
    g.set(8, 12, g.k("rope_coil"), True)
    g.set(10, 12, STELE, True)                   # AIGINA, by the gangplank

    # ---- Kolona's headland ---------------------------------------------------
    g.put("kolona", 2, 3)
    for (x, y) in ((2, 3), (2, 4), (2, 5), (2, 6), (4, 3), (4, 4), (4, 5), (4, 6)):
        g.set(x, y, g.k("dry_grass", 1, 1))       # dry grass beside the shaft
    g.put("kolona_ruins", 2, 9)
    for (x, y) in ((0, 4), (5, 0), (6, 1), (0, 12), (1, 14), (18, 1), (29, 15), (27, 20)):
        g.set(x, y, g.k("sea_rocks"), True)       # rocks awash round the island

    # ---- the waterfront and the town --------------------------------------------
    g.put("inn", 13, 13)
    g.put("mint", 20, 13)
    g.put("turtle_mosaic", 20, 17)

    # ---- the hills: the gate, the lane, Aiakides's house, the ant hills -----------
    g.put("gate", GATE_X, GATE_Y)
    if gate_shut:
        sh = g.cat["gate_shut"]
        for i, x in enumerate(GATE_COLS):
            g.set(x, GATE_Y + 2, sh["ids"][0][i], True)
    wall_run(g, 20, 22, GATE_Y + 2)
    wall_run(g, 27, 28, GATE_Y + 2)
    g.put("house_aiakides", 26, 6)
    ant = lambda x, y: g.set(x, y, g.k("anthills", 0, 0), True)
    trail = lambda x, y: g.set(x, y, g.k("anthills", 1, 0))
    for (x, y) in ((22, 6), (23, 9), (21, 8)):
        ant(x, y)
    for (x, y) in ((22, 7), (22, 8), (23, 8)):
        trail(x, y)
    for (x, y) in ((26, 10), (27, 5)):
        g.set(x, y, g.k("scrub", 0, 0), True)

    # ---- greenery -------------------------------------------------------------------
    # beyond the wall, the pines of the Aphaia Road begin; the road between them is
    # the only way on (the seam is open at GATE_COLS alone)
    g.put("pine", 21, 0)
    g.put("pine", 27, 0)
    for x in (21, 22, 27, 28):
        g.solid[0, x] = True                     # the pines' crowns meet the seam
    g.set(23, 0, g.k("scrub", 0, 0), True)
    g.set(26, 0, g.k("scrub", 1, 0), True)
    # Kolona: scrub in the dry grass
    g.set(5, 4, g.k("scrub", 0, 0), True)
    g.set(5, 5, g.k("scrub", 1, 0), True)
    # the pistachio orchard south-west of the waterfront
    for (x, y) in ((3, 14), (6, 14), (3, 17), (6, 17), (8, 15)):
        if g.free(x, y, 2, 2):
            g.put("pistachio", x, y)
    g.upine(2, 10)                               # an umbrella pine at Kolona's foot
    # shade in the square, and trees along the lane
    for (x, y) in ((25, 14), (11, 14), (11, 18)):
        if g.free(x, y, 2, 2):
            g.put("pistachio", x, y)
    for (x, y) in ((24, 18), (16, 18), (12, 16)):
        if g.free(x, y, 1, 2):
            g.cypress(x, y)
    for (x, y) in ((3, 12), (7, 19), (14, 18), (26, 17), (2, 19), (17, 19)):
        if g.mid[y, x] == GRASS and not g.solid[y, x]:
            g.set(x, y, FLOWERS)
    g.put("boat_kaiki", 13, 21)                  # a fishing boat in the beach's inlet
    g.put("boat_beached", 7, 20)                 # and one hauled up on the sand
    g.put("pistachio", 22, 18)                   # shade in the mint's square

    return g, plan


def border():
    return np.full(4, SEA, np.uint16)


def encode(g):
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mid[y, x])
            water = behavior(mid) in SURF_BEHAVIORS
            elev = 1 if water else 3
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | (elev << 12)
    return out


def write_layouts():
    LAYOUT.mkdir(parents=True, exist_ok=True)
    g, _ = compose()
    encode(g).astype("<u2").tofile(LAYOUT / "map.bin")
    border().astype("<u2").tofile(LAYOUT / "border.bin")
    return g


def gate_shut_ids():
    """The metatile values ON_TRANSITION writes over the gate's passage on the
    voyage night (setmetatile), for scripts.pory."""
    g, _ = compose(gate_shut=True)
    return [(x, GATE_Y + 2, int(g.mid[GATE_Y + 2, x])) for x in GATE_COLS]


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

# Where the player stands for each screen-sized review crop, along their route:
# off the gangplank, west to Kolona and out on the moles, then round the town,
# up the lane to the ant hills and the gate, and down to the beach.
SCREENS = {
    "1_arrival": ARRIVAL, "2_waterfront_west": (7, 12), "3_kolona": (4, 8),
    "4_headland": (3, 4), "5_west_mole": (8, 4), "6_east_mole": (17, 4),
    "7_inn": (15, 17), "8_square": (21, 18), "9_east_street": (25, 12),
    "10_ant_hills": (22, 10), "11_aiakides": (27, 9), "12_gate": (24, 5),
    "13_orchard": (5, 16), "14_beach": (10, 19), "15_south": (18, 19),
}


def render(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / "aegina_town.png"
    subprocess.run(rm + ["LAYOUT_AEGINA_TOWN", "--scale", "2", "-o", str(png)], check=True,
                   stdout=subprocess.DEVNULL)
    overlay(png, LAYOUT / "map.bin", W, out_dir / "aegina_town_walk.png", 2)
    screens(out_dir)


def screens(out_dir, margin=8):
    """Crop GBA-screen views (15x10 tiles, the player on the 8th column and 5th row)
    from the map padded with its border, at 2x, and tile them into one sheet."""
    from PIL import Image
    if not SCREENS:
        return
    blocks = np.fromfile(LAYOUT / "map.bin", "<u2").reshape(H, W)
    bord = np.fromfile(LAYOUT / "border.bin", "<u2").reshape(2, 2)
    big = np.empty((H + 2 * margin, W + 2 * margin), np.uint16)
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            big[y, x] = bord[y % 2, x % 2]
    big[margin:margin + H, margin:margin + W] = blocks
    tmp = out_dir / "padded.bin"
    big.astype("<u2").tofile(tmp)
    png = out_dir / "padded.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", "aegina",
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    crops = []
    crops_dir = ROOT / "build/aegina_render"           # one file per screen, for review
    crops_dir.mkdir(parents=True, exist_ok=True)
    for name, (px, py) in SCREENS.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        crop.save(crops_dir / f"aegina_screen_{name}.png")
        crops.append(crop)
    cols = 2
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(crops) // cols) * (10 * c + 8) - 8),
                      (24, 24, 32))
    for i, crop in enumerate(crops):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out_dir / "aegina_screens.png")
    tmp.unlink()
    png.unlink()


def overlay(png, bin_path, width, out, scale):
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
    ev = json.loads(MAPJSON.read_text())
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
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4],
               fill=(255, 255, 255, 255), width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4],
               fill=(255, 255, 255, 255), width=2)
    Image.alpha_composite(im, lay).save(out)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 != 1


def reachable(blocks, start, extra_open=()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in seen and (walkable(blocks, *p) or p in extra_open):
                seen.add(p)
                q.append(p)
    return seen


FLYERS = ("WINGULL",)
# Cells the arrival walks people across: Alethea and Kleon go east along the quay
# from (14,12) and (13,12), eight steps each.
SCRIPTED_PATHS = {
    "Alethea": [(x, 12) for x in range(15, 23)],
    "Kleon": [(x, 12) for x in range(14, 22)],
}


def check():
    errors = []
    blocks = np.fromfile(LAYOUT / "map.bin", "<u2").reshape(H, W)
    bord = np.fromfile(LAYOUT / "border.bin", "<u2")
    ev = json.loads(MAPJSON.read_text())
    if any(int(b) & 0x3FF != SEA for b in bord):
        errors.append("the border should be open sea all round")
    warps = [(w_["x"], w_["y"]) for w_ in ev["warp_events"]]
    if warps[0] != ARRIVAL:
        errors.append(f"warp 0 should be the arrival tile {ARRIVAL} (the ferry lands there)")
    objects = {(o["x"], o["y"]) for o in ev["object_events"]}
    reach = reachable(blocks, ARRIVAL, extra_open=set(warps))
    for i, (x, y) in enumerate(warps):
        b = behavior(int(blocks[y, x]) & 0x3FF)
        if i == 0:
            if not walkable(blocks, x, y) or b in DOOR_BEHAVIORS:
                errors.append(f"warp 0 at ({x},{y}) must be plain walkable quay, not {b}")
        elif b not in DOOR_BEHAVIORS:
            errors.append(f"warp {i} at ({x},{y}) is on {b}, not a door")
        if (x, y) not in reach:
            errors.append(f"warp {i} at ({x},{y}) is unreachable from the quay")
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if any(f in o["graphics_id"] for f in FLYERS):
            continue
        if not walkable(blocks, x, y):
            errors.append(f"object {o['local_id']} at ({x},{y}) stands on a solid cell")
        elif (x, y) not in reach:
            errors.append(f"object {o['local_id']} at ({x},{y}) can't be reached")
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        if b["type"] == "hidden_item" and (x, y) in reach:
            continue
        fronts = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
        if b.get("player_facing_dir") == "BG_EVENT_PLAYER_FACING_NORTH":
            fronts = [(x, y + 1)]
        if not any(p in reach and p not in objects for p in fronts):
            errors.append(f"bg event at ({x},{y}) can't be read from any walkable tile")
    # the north seam: open exactly at the gate's columns
    for x in range(W):
        ok = walkable(blocks, x, 0)
        if ok != (x in GATE_COLS):
            errors.append(f"north seam column {x} is {'open' if ok else 'closed'}")
    for x in GATE_COLS:
        if (x, 0) not in reach:
            errors.append(f"the road north at ({x},0) can't be reached from the quay")
    # every other edge is sea: nobody walks off the island but through the gate
    for (x, y) in reach:
        if (x in (0, W - 1) or y == H - 1) and (x, y) not in warps:
            errors.append(f"({x},{y}) on the map's edge is walkable")
    # the voyage night: with the leaves shut and the gatekeeper in the gate, the
    # road north is out of reach
    g_shut, _ = compose(gate_shut=True)
    shut = encode(g_shut)
    keeper = next(o for o in ev["object_events"] if o["local_id"] == "LOCALID_AEGINA_GATEKEEPER")
    shut[keeper["y"], keeper["x"]] |= 1 << 10
    night = reachable(shut, ARRIVAL)
    if any((x, 0) in night for x in GATE_COLS):
        errors.append("the road north is reachable on the voyage night")
    # scripts.pory's setmetatile ids must be gate_shut's
    pory = (ROOT / "data/maps/AeginaTown/scripts.pory").read_text()
    for (x, y, mid) in gate_shut_ids():
        if f"setmetatile({x}, {y}, 0x{mid:03X}, TRUE)" not in pory:
            errors.append(f"scripts.pory should shut the gate with setmetatile({x}, {y}, 0x{mid:03X}, TRUE)")
    # (the two walk off together, Kleon a step behind Alethea)
    others = {(o["x"], o["y"]) for o in ev["object_events"]
              if o["local_id"] not in ("LOCALID_AEGINA_KLEON", "LOCALID_AEGINA_ALETHEA")}
    for who, cells in SCRIPTED_PATHS.items():
        for (x, y) in cells:
            if not walkable(blocks, x, y) or (x, y) in others:
                errors.append(f"{who}'s walk off the quay crosses a blocked cell ({x},{y})")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR", help="also render the map into DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run tools/ichor/art/aegina_build.py --no-compile first")
    write_layouts()
    if args.render:
        render(args.render)
    if not args.no_check:
        errors = check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("aegina: layout written, checks pass")


if __name__ == "__main__":
    main()
