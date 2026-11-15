#!/usr/bin/env python3
"""Mock scenes for the Kythera-family tilesets, rendered with render_map.py.

These are review scenes, not maps: they show how each kit's pieces fit
together. Pieces are placed by key and name from build/<dir>/catalog.json
(run kythera_build.py first), exactly as a map builder would place them, and
soft ground takes its shape keys from kythera_lib.blob_key.

Usage: /usr/bin/python3 tools/ichor/art/kythera_scene.py [scene ...]
Scenes: foam_beach (a 240x160 screen of the Foam Road at Aphrodite's rock),
foam_road (a wider stretch with the herm, the quarry and the spring stair),
spring (the Spring of Kallirhoe), harbor_street (a 240x160 screen of
Skandeia's quay), skandeia (the harbor town), and the paphia, neraida and
melos scenes once those tilesets exist.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_lib as K  # noqa: E402

ROOT = K.ROOT
IMG = ROOT / "design/phase4/img"

# aethos metatiles
GRASS, PATH, SAND, SEA, SHALLOW, FALL = 0x001, 0x1D9, 0x124, 0x170, 0x0D1, 0x0B3
TALL = 0x00D
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
CYP_TOP, CYP_BOT = 0x00E, 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
STELE, HERM = 0x003, 0x01B
PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
         "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
SAND_GRASS = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122,
              "BL": 0x128, "B": 0x129, "BR": 0x12A}
LEDGE = {"S": 0x087, "W": 0x085, "E": 0x086, "SW": 0x08D, "SE": 0x08E, "SL": 0x0D5, "SR": 0x0D6}
ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A}


class Scene:
    def __init__(self, tileset, w, h, fill=GRASS):
        self.dir = tileset
        cat = json.loads((ROOT / f"build/{tileset}/catalog.json").read_text())
        self.symbol = cat["tileset"]
        self.s = {d["key"]: d for d in cat["structures"]}
        self.fronts = cat.get("fronts", {})
        self.W, self.H = w, h
        self.m = np.full((h, w), fill, np.uint16)

    def ok(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def put(self, key, x, y, cells=None):
        d = self.s[key]
        for j in range(d["h"]):
            for i in range(d["w"]):
                if cells is not None and (i, j) not in cells:
                    continue
                if self.ok(x + i, y + j):
                    self.m[y + j, x + i] = d["ids"][j][i]

    def part(self, key, name, x, y, w, h):
        """A w x h block of a structure starting at its named cell."""
        d = self.s[key]
        cx, cy = d["names"][name]
        for j in range(h):
            for i in range(w):
                if self.ok(x + i, y + j):
                    self.m[y + j, x + i] = d["ids"][cy + j][cx + i]

    def piece(self, key, name, x, y):
        d = self.s[key]
        cx, cy = d["names"][name]
        if self.ok(x, y):
            self.m[y, x] = d["ids"][cy][cx]

    def front(self, key, x, y):
        for j, row in enumerate(self.fronts[key]["ids"]):
            for i, mid in enumerate(row):
                if mid is not None and self.ok(x + i, y + j):
                    self.m[y + j, x + i] = mid

    def rect(self, x0, y0, x1, y1, mid):
        self.m[max(0, y0):y1 + 1, max(0, x0):x1 + 1] = mid

    def blob(self, key, rows, ox, oy, ch="#"):
        region = [[c == ch for c in r] for r in rows]
        d = self.s[key]
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != ch:
                    continue
                k = K.blob_key(region, i, j)
                cx, cy = d["names"][k]
                if self.ok(ox + i, oy + j):
                    self.m[oy + j, ox + i] = d["ids"][cy][cx]

    def olive(self, x, y):
        for (dx, dy), mid in (((0, -1), OLIVE_TIP[0]), ((1, -1), OLIVE_TIP[1]),
                              ((0, 0), OLIVE_TOP[0]), ((1, 0), OLIVE_TOP[1]),
                              ((0, 1), OLIVE_BOT[0]), ((1, 1), OLIVE_BOT[1])):
            if self.ok(x + dx, y + dy):
                self.m[y + dy, x + dx] = mid

    def cypress(self, x, y):
        if self.ok(x, y):
            self.m[y, x] = CYP_TOP
        if self.ok(x, y + 1):
            self.m[y + 1, x] = CYP_BOT

    def path_patch(self, x0, y0, x1, y1, kit=PATCH):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                v = "T" if y == y0 else ("B" if y == y1 else "")
                h = "L" if x == x0 else ("R" if x == x1 else "")
                if self.ok(x, y):
                    self.m[y, x] = kit[(v + h) or "C"]

    def shore(self, rows, ox, oy, key="surf"):
        """Lay a coastline from a mask: '#' sand (aethos), '~' sea (aethos),
        and the waterline cells between them chosen from the surf kit by the
        sand around each sea cell."""
        H, Wd = len(rows), len(rows[0])

        def sand(i, j):
            if not (0 <= i < Wd and 0 <= j < H):
                return None
            return rows[j][i] == "#"
        for j in range(H):
            for i in range(Wd):
                c = rows[j][i]
                X, Y = ox + i, oy + j
                if not self.ok(X, Y) or c not in "#~":
                    continue
                if c == "#":
                    self.m[Y, X] = SAND
                    continue
                n, s_, e, w = sand(i, j - 1), sand(i, j + 1), sand(i + 1, j), sand(i - 1, j)
                ne, nw, se, sw = sand(i + 1, j - 1), sand(i - 1, j - 1), sand(i + 1, j + 1), sand(i - 1, j + 1)
                name = None
                if n and w:
                    name = "in_SE"
                elif n and e:
                    name = "in_SW"
                elif s_ and w:
                    name = "in_NE"
                elif s_ and e:
                    name = "in_NW"
                elif n:
                    name = "S"
                elif s_:
                    name = "N"
                elif w:
                    name = "E"
                elif e:
                    name = "W"
                elif nw:
                    name = "out_NW"
                elif ne:
                    name = "out_NE"
                elif sw:
                    name = "out_SW"
                elif se:
                    name = "out_SE"
                if name:
                    self.piece(key, name, X, Y)
                else:
                    self.m[Y, X] = SEA

    def render(self, out, scale=2):
        blk = ROOT / f"build/{self.dir}/scene.bin"
        blk.parent.mkdir(parents=True, exist_ok=True)
        self.m.astype("<u2").tofile(blk)
        prim = "oikos" if self.dir == "temple_aphrodite" else "aethos"
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata",
                        str(blk), "--width", str(self.W), "--primary", prim, "--secondary",
                        self.symbol, "--scale", str(scale), "-o", str(out)], check=True)
        print(Path(out).relative_to(ROOT) if str(out).startswith(str(ROOT)) else out)


# --------------------------------------------------------------------------
# kythera: the Foam Road
# --------------------------------------------------------------------------

def cliff_run(s, x0, x1, y, foot="sand"):
    """A south-facing pink cliff from x0 to x1: lip row y, face y+1, foot y+2."""
    for x in range(x0, x1 + 1):
        end = "_L" if x == x0 else ("_R" if x == x1 else "")
        s.piece("cliff", "lip" + end, x, y)
        s.piece("cliff", "face" + end, x, y + 1)
        if foot == "sea":
            s.piece("cliff", "foot_sea" + end, x, y + 2)
        elif foot == "sand" and not end:
            s.piece("cliff", "foot_sand", x, y + 2)
        elif foot == "grass" and not end:
            s.piece("cliff", "foot_grass", x, y + 2)


def hedge_run(s, x0, x1, y, key="myrtle"):
    for x in range(x0, x1 + 1):
        n = "L" if x == x0 else ("R" if x == x1 else ("M2" if (x - x0) % 3 == 2 and "M2" in s.s[key]["names"] else "M"))
        s.piece(key, n, x, y)


def foam_beach():
    """One screen (15 x 10) of the Foam Road at Aphrodite's rock."""
    s = Scene("kythera", 15, 10)
    # the ridge: myrtle over a band of sea-grass and thrift
    hedge_run(s, 0, 5, 0)
    s.piece("myrtle", "single", 6, 0)
    s.piece("flowers", "briar_L", 7, 0)
    s.piece("flowers", "briar_R", 8, 0)
    hedge_run(s, 9, 14, 0)
    s.blob("seagrass", ["..####...######",
                        ".#####..#######"], 0, 1)
    for (x, y) in ((1, 1), (7, 1)):
        s.piece("flowers", "thrift", x, y)
    # the low pink cliff the road runs under; the spring's seep and its basin
    cliff_run(s, 0, 14, 2, foot="sand")
    s.piece("cliff", "seep", 11, 3)
    # the road: sand, shingle near the water, the dig spot, the rock offshore
    s.rect(0, 4, 14, 5, SAND)
    for x in range(1, 14):
        s.piece("cliff", "foot_sand", x, 4)
    s.piece("cliff", "foot_sand_rocks", 4, 4)
    s.piece("falls", "basin", 11, 4)
    s.blob("shingle", ["###......",
                       "####....."], 0, 4)
    s.shore(["###############",
             "~~~~~~~~~~~~~~~",
             "~~~~~~~~~~~~~~~"], 0, 5)
    s.piece("sand_decor", "sherd_dig", 8, 5)
    s.piece("sand_decor", "shells", 13, 5)
    s.piece("sand_decor", "scallop", 5, 5)
    s.piece("sand_decor", "lace", 10, 5)
    s.piece("sand_decor", "lace", 11, 5)
    s.piece("sand_decor", "wrack", 6, 4)
    s.piece("sand_decor", "footprints", 9, 4)
    s.rect(0, 8, 14, 9, SEA)
    d = s.s["aphrodite_rock"]
    for j in range(3):
        for i in range(3):
            s.m[7 + j, 9 + i] = d["ids"][j][i]
    s.piece("rocks", "tide_rock", 3, 8)
    s.piece("rocks", "tide_rocks", 14, 8)
    return s


def foam_road():
    """A wider stretch (30 x 20): the herm at the fork, the stair through the
    myrtle to the spring, the quarry spur, the cutting, the rock and the reef."""
    s = Scene("kythera", 30, 20)
    # north edge: the ridge with the spring stair
    hedge_run(s, 0, 9, 0)
    s.piece("myrtle", "gap_stair", 10, 0)
    hedge_run(s, 11, 18, 0)
    s.piece("myrtle", "single", 19, 0)
    s.olive(21, 1)
    s.cypress(24, 0)
    s.cypress(26, 0)
    hedge_run(s, 27, 29, 0)
    s.blob("seagrass", ["###....###.......####..",
                        "####..#####.....######.",
                        ".###...###.......###..."], 0, 1)
    # the herm at the fork, with the path to the stair
    s.rect(9, 1, 11, 3, PATH)
    s.path_patch(9, 1, 11, 4)
    s.piece("herm", "herm", 12, 3)
    s.piece("herm", "herm_base", 12, 4)
    s.m[4, 8] = STELE
    # the road east-west
    s.path_patch(0, 5, 29, 7)
    for x in (3, 15, 22):
        s.piece("flowers", "petals", x, 4)
    # the quarry spur to the south-west behind its drums
    for x in range(0, 6):
        s.piece("quarry", "cut_L" if x == 0 else ("cut_R" if x == 5 else "cut"), x, 8)
        s.piece("quarry", "face_L" if x == 0 else ("face_R" if x == 5 else "face"), x, 9)
    s.part("quarry", "gate_TL", 6, 8, 2, 2)
    s.rect(0, 10, 7, 11, PATH)
    for (x, y, n) in ((1, 10, "chips"), (3, 11, "block"), (5, 10, "drum_up"), (2, 11, "chips")):
        s.piece("quarry", n, x, y)
    s.piece("quarry", "drum_fallen", 4, 11)
    s.piece("quarry", "drum_fallen_R", 5, 11)
    # the cutting: a pink sea-cliff south of the road, the surf below it
    cliff_run(s, 8, 18, 8, foot="sea")
    s.rect(8, 11, 18, 19, SEA)
    s.piece("rocks", "tide_rock", 12, 13)
    # west of the cutting: the beach, Aphrodite's rock, the reef spit
    s.rect(19, 8, 29, 11, SAND)
    s.blob("shingle", ["..####", ".#####", "..###."], 22, 8)
    s.piece("sand_decor", "sherd_dig", 26, 10)
    s.piece("sand_decor", "lace", 20, 11)
    s.piece("sand_decor", "lace", 21, 11)
    s.shore(["###########",
             "~~~~~~~~~~~",
             "~~~~~~~~~~~"], 19, 11)
    s.rect(0, 12, 7, 19, SEA)
    s.shore(["########",
             "~~~~~~~~"], 0, 11)
    for x in range(0, 8):
        s.m[11, x] = SAND if x < 7 else s.m[11, x]
    s.rect(19, 14, 29, 19, SEA)
    d = s.s["aphrodite_rock"]
    for j in range(3):
        for i in range(3):
            s.m[14 + j, 24 + i] = d["ids"][j][i]
    for (x, n) in ((20, "spit_M"), (21, "spit_M"), (22, "spit_head")):
        s.piece("rocks", n, x, 13)
    s.piece("rocks", "tide_rocks", 28, 17)
    return s


def spring():
    s = Scene("kythera", 26, 22)
    # a round glade in the myrtle
    for x in range(26):
        s.piece("myrtle", "M" if x % 3 else "M2", x, 0)
        s.piece("myrtle", "M" if x % 4 else "M2", x, 21)
    for y in range(1, 21):
        s.piece("myrtle", "V", 0, y)
        s.piece("myrtle", "V", 25, y)
    s.piece("myrtle", "NW", 0, 0)
    s.piece("myrtle", "NE", 25, 0)
    s.piece("myrtle", "SW", 0, 21)
    s.piece("myrtle", "SE", 25, 21)
    # the rock lip and the thin fall feeding the pool
    cliff_run(s, 8, 17, 2, foot="grass")
    s.piece("cliff", "spring_lip", 12, 3)
    s.piece("falls", "thin_fall", 12, 4)
    s.put("spring_pool", 11, 5)
    # the rock stair down to Echo's caves, north-east
    s.piece("cave_stair", "cave_top", 20, 3)
    s.piece("cave_stair", "cave_stair", 20, 4)
    cliff_run(s, 18, 23, 2, foot="grass")
    s.piece("cave_stair", "cave_top", 20, 3)
    s.piece("cave_stair", "cave_stair", 20, 4)
    # the horseshoe of grass round the pool
    s.blob("seagrass", ["####..........####",
                        "#####........#####",
                        "#####........#####",
                        ".####........####.",
                        "..###########.###.",
                        "...##########..#.."], 4, 7)
    for (x, y) in ((10, 6), (16, 6), (10, 9), (16, 9), (11, 10), (15, 10), (13, 4)):
        s.piece("flowers", "narcissus" if (x + y) % 2 else "narcissus_b", x, y)
    s.path_patch(11, 15, 15, 20)
    return s


# --------------------------------------------------------------------------
# skandeia: the harbor town
# --------------------------------------------------------------------------

def quay_edge(s, x0, x1, y, side="S"):
    for x in range(x0, x1 + 1):
        s.piece("quay", side, x, y)


def harbor_street():
    """One screen (15 x 10) of Skandeia's quay: houses opening onto the
    harbor front, the Agora facing the water, the slips with the one boat the
    Titans left, the gear on the quay, fishing boats in the bay."""
    s = Scene("skandeia", 15, 10, fill=PATH)
    # the slope above: a terrace wall's top, myrtle
    for x in range(0, 10):
        s.piece("terrace", "top" if 0 < x < 9 else ("top_L" if x == 0 else "top_R"), x, 0)
    s.piece("myrtle", "bush", 4, 0)
    # houses on the harbor front, doors onto the quay
    s.front("cube_pot", 0, 1)
    s.front("cube", 5, 1)
    s.piece("house", "U_vine", 6, 2)
    s.piece("house", "door", 6, 3)
    s.m[1:4, 8] = PATH
    s.m[0, 8] = PATH
    s.piece("flowers", "briar", 9, 0)
    s.piece("flowers", "thrift", 9, 1)
    # the Agora, facing the water
    for j, row in enumerate(AGORA):
        for i, mid in enumerate(row):
            s.m[j, 10 + i] = mid
    s.m[0:4, 14] = PATH
    s.piece("flowers", "petals", 14, 2)
    # the harbor front: gear, the shrine at the quay's end
    s.piece("gear", "nets", 1, 5)
    s.piece("gear", "oars", 4, 5)
    s.piece("gear", "oars", 5, 5)
    s.piece("gear", "amphorae", 9, 4)
    s.piece("gear", "rope", 10, 6)
    s.piece("shrine", "shrine", 14, 4)
    s.piece("shrine", "shrine_base", 14, 5)
    # the slips going down into the bay: one empty, one with the leaky boat
    s.put("slips", 0, 6)
    # the quay's edge, a bollard, steps down to a boat
    quay_edge(s, 4, 14, 7)
    s.piece("quay", "ring_S", 7, 7)
    s.piece("quay", "S_plank", 11, 7)
    s.piece("gear", "bollard", 12, 6)
    s.piece("quay", "steps_S", 13, 7)
    s.rect(0, 8, 14, 9, SEA)
    s.put("slips", 0, 6)
    s.piece("gear", "crate", 7, 5)
    s.piece("gear", "rope", 2, 4)
    s.put("kaiki", 6, 8, cells=[(i, j) for i in range(3) for j in range(2)])
    d = s.s["kaiki"]
    for j in range(2):
        for i in range(3):
            s.m[8 + j, 10 + i] = d["ids"][j][i]
    return s


def skandeia():
    """A wider look at Skandeia (30 x 22): houses climbing the slope in
    terraces, the Asclepeion and Agora on the harbor front, the quay, the
    slips at its north end, the Euploia at the gangplank, the shrine."""
    s = Scene("skandeia", 30, 22, fill=GRASS)
    # the sea: north bay across the top right, east bay down the east side
    s.rect(20, 0, 29, 21, SEA)
    s.rect(14, 0, 19, 4, SEA)
    # the Euploia moored in the north bay, her plank onto the quay
    d = s.s["trireme"]
    for j in range(d["h"]):
        for i in range(d["w"]):
            s.m[1 + j, 14 + i] = d["ids"][j][i]
    # the quay: north edge under the ship, east edge down the side
    s.rect(10, 4, 19, 21, PATH)
    for x in range(10, 20):
        s.piece("quay", "N", x, 4)
    s.piece("quay", "N_plank", 17, 4)
    for y in range(5, 22):
        s.piece("quay", "E", 20, y)
    s.piece("quay", "out_NE", 20, 4)
    s.piece("quay", "steps_E", 20, 12)
    s.rect(21, 4, 29, 21, SEA)
    # slips at the north end, before the ship
    s.put("slips", 10, 2)
    s.rect(10, 0, 13, 1, SEA)
    # the harbor front: the Asclepeion and the Agora face the water
    for j, row in enumerate(ASCLEPEION):
        for i, mid in enumerate(row):
            s.m[7 + j, 15 + i] = mid
    for j, row in enumerate(AGORA):
        for i, mid in enumerate(row):
            s.m[13 + j, 15 + i] = mid
    s.piece("gear", "oars", 12, 6)
    s.piece("gear", "nets", 11, 9)
    s.piece("gear", "amphorae", 13, 11)
    s.piece("gear", "bollard", 19, 8)
    s.piece("gear", "bollard", 19, 16)
    s.piece("shrine", "shrine", 19, 19)
    s.piece("shrine", "shrine_base", 19, 20)
    # the houses climb the slope west of the harbor in terraces
    for (fx, fy, f) in ((1, 1, "cube_pot"), (6, 1, "cube"), (1, 7, "long_house"),
                        (6, 13, "stair_house"), (1, 13, "cube"), (2, 18, "cube_pot")):
        s.front(f, fx, fy)
    for x in range(0, 10):
        s.piece("terrace", "M" if 0 < x < 9 else ("L" if x == 0 else "R"), x, 5)
        s.piece("terrace", "top" if 0 < x < 9 else ("top_L" if x == 0 else "top_R"), x, 4)
        s.piece("terrace", "M" if 0 < x < 9 else ("L" if x == 0 else "R"), x, 11)
        s.piece("terrace", "top" if 0 < x < 9 else ("top_L" if x == 0 else "top_R"), x, 10)
    s.piece("terrace", "steps", 8, 5)
    s.piece("terrace", "top_steps", 8, 4)
    s.piece("terrace", "steps", 4, 11)
    s.piece("terrace", "top_steps", 4, 10)
    s.rect(0, 6, 9, 6, PATH)
    s.rect(0, 12, 9, 12, PATH)
    s.rect(0, 16, 9, 17, PATH)
    s.olive(7, 8)
    s.cypress(0, 8)
    s.piece("myrtle", "single", 9, 1)
    s.piece("myrtle", "bush", 9, 7)
    s.piece("flowers", "briar", 5, 8)
    s.m[6, 0] = STELE
    return s


# --------------------------------------------------------------------------
# paphia, neraida, melos, the temple
# --------------------------------------------------------------------------

def paphia():
    """Paphia's crown (24 x 18): the temple at the top of the great stair, the
    terraces of houses with mirrors and doves, a dovecote, the sculptors."""
    s = Scene("paphia", 24, 18, fill=GRASS)
    s.put("temple_front", 8, 0)
    # the great stair down the hill's spine
    for y in range(5, 18):
        s.piece("great_stair", "L", 10, y)
        s.piece("great_stair", "M", 11, y)
        s.piece("great_stair", "M", 12, y)
        s.piece("great_stair", "R", 13, y)
    for y in (9, 14):
        for x, n in ((10, "land_L"), (11, "land"), (12, "land"), (13, "land_R")):
            s.piece("great_stair", n, x, y)
    # terraces either side, a pink retaining wall between them
    for x in range(0, 10):
        s.piece("terrace", "top" if 0 < x < 9 else ("top_L" if x == 0 else "top_R"), x, 8)
        s.piece("terrace", "M" if 0 < x < 9 else ("L" if x == 0 else "R"), x, 9)
    for x in range(14, 24):
        s.piece("terrace", "top" if 14 < x < 23 else ("top_L" if x == 14 else "top_R"), x, 8)
        s.piece("terrace", "M" if 14 < x < 23 else ("L" if x == 14 else "R"), x, 9)
    s.rect(0, 10, 9, 17, PATH)
    s.rect(14, 10, 23, 17, PATH)
    s.front("paphia_house", 1, 5)
    s.front("paphia_narrow", 4, 11)
    s.front("chapel_house", 15, 5)
    s.front("paphia_house", 18, 11)
    s.put("dovecote", 20, 4)
    s.put("sculptors", 0, 15, cells=[(i, 0) for i in range(5)])
    s.piece("sculptors", "hoist_foot", 2, 16)
    for (x, y) in ((8, 6), (14, 6), (9, 12), (14, 15)):
        s.piece("flowers", "petals", x, y)
    s.piece("myrtle", "single", 0, 1)
    s.piece("myrtle", "bush", 6, 2)
    s.cypress(7, 2)
    s.cypress(16, 1)
    s.piece("flowers", "briar", 18, 2)
    d = s.s["apple"]
    for j in range(2):
        for i in range(2):
            s.m[1 + j, 2 + i] = d["ids"][j][i]
    s.olive(21, 15)
    return s


def neraida():
    """The Neraida ravine (22 x 20): the double falls into a plunge pool and its
    shrine, the river below in pools and weirs, stepping stones, the plank
    bridge, Myles's mill turning, a plane tree, the vault door in the cliff."""
    s = Scene("neraida", 22, 20, fill=GRASS)
    # the cliff across the top, the falls cutting it at x=10-11
    for y, row in ((0, "lip"), (1, "face"), (2, "face")):
        for x in range(0, 22):
            if x in (10, 11):
                continue
            end = "_L" if x == 0 else ("_R" if x == 21 else "")
            if row == "lip":
                s.piece("cliff", "lip" + end, x, y)
            else:
                s.piece("cliff", "face" + end, x, y)
    s.piece("falls", "face_fall_L", 9, 1)
    s.piece("falls", "face_fall_R", 12, 1)
    s.piece("falls", "face_fall_L", 9, 2)
    s.piece("falls", "face_fall_R", 12, 2)
    s.piece("falls", "lip_L", 10, 0)
    s.piece("falls", "lip_R", 11, 0)
    s.rect(10, 1, 11, 2, FALL)
    s.part("vault", "vault_TL", 15, 1, 2, 2)
    # the plunge pool and its kerbs, the shrine beside it
    s.piece("falls", "foot_face_L", 9, 3)
    s.piece("falls", "foot_face_R", 12, 3)
    s.piece("falls", "foot_L", 10, 3)
    s.piece("falls", "foot_R", 11, 3)
    for x in range(8, 14):
        for y in (4, 5):
            s.m[y, x] = SHALLOW
    s.piece("kerb", "E", 7, 4)
    s.piece("kerb", "E", 7, 5)
    s.piece("kerb", "W", 14, 4)
    s.piece("kerb", "W", 14, 5)
    s.piece("kerb", "SW", 7, 6)
    s.piece("kerb", "SE", 14, 6)
    for x in range(8, 14):
        if x not in (10, 11):
            s.piece("kerb", "N", x, 6)
    s.piece("kerb", "in_SW", 9, 6)
    s.piece("kerb", "in_SE", 12, 6)
    s.m[6, 10] = s.m[6, 11] = SHALLOW
    s.piece("naiad_altar", "horn", 5, 4)
    # the river runs south from the pool: weir, stones, the bridge
    for y in range(7, 20):
        for x in (10, 11):
            s.m[y, x] = SHALLOW
        s.piece("kerb", "E", 9, y)
        s.piece("kerb", "W", 12, y)
    s.piece("bridge_weir", "weir_W", 9, 8)
    s.piece("bridge_weir", "weir", 10, 8)
    s.piece("bridge_weir", "weir", 11, 8)
    s.piece("bridge_weir", "weir_E", 12, 8)
    s.piece("kerb", "stones", 10, 11)
    s.piece("kerb", "stones_b", 11, 12)
    s.piece("kerb", "reeds", 10, 14)
    for x, n in ((9, "bridge_W"), (10, "bridge"), (11, "bridge"), (12, "bridge_E")):
        s.piece("bridge_weir", n, x, 16)
    # the mill on the east bank, its wheel in the river
    s.put("mill", 13, 10, cells=[(i, j) for i in range(3) for j in range(3)])
    d = s.s["mill"]
    for j in range(2):
        for i in range(2):
            s.m[11 + j, 11 + i] = d["ids"][1 + j][3 + i]
    s.put("plane", 2, 9)
    s.piece("flowers", "oleander", 6, 8)
    s.piece("flowers", "oleander", 16, 7)
    s.blob("seagrass", ["####..", "#####.", ".####."], 1, 14)
    s.piece("myrtle", "single", 19, 4)
    s.piece("myrtle", "bush", 20, 15)
    s.cypress(18, 16)
    s.path_patch(13, 17, 21, 19)
    return s


def melos():
    """Klima on Melos (24 x 18): boathouses at the waterline with painted sea
    doors, the jetty, the well, the terraces and the niche, the obsidian slope,
    the white pumice cliffs."""
    s = Scene("melos", 24, 18, fill=GRASS)
    # the obsidian slope across the top
    s.blob("obsidian", ["..########......########",
                        ".##########....##########",
                        "..########......#######..",
                        "....####..........###...."], 0, 0)
    s.piece("obsidian_bits", "pit", 4, 1)
    s.piece("obsidian_bits", "flakes", 7, 2)
    s.piece("obsidian_bits", "sacks", 18, 1)
    # the terraces: tuff walls, the niche
    for x in range(0, 24):
        n = "top" if 0 < x < 23 else ("top_L" if x == 0 else "top_R")
        s.piece("village", n, x, 4)
        w = "wall" if 0 < x < 23 else ("wall_L" if x == 0 else "wall_R")
        s.piece("village", w, x, 5)
    s.piece("village", "niche", 6, 5)
    s.piece("village", "top_niche", 6, 4) if "top_niche" in s.s["village"]["names"] else None
    s.piece("village", "wall_steps", 12, 5)
    s.piece("village", "top_steps", 12, 4)
    for x in (2, 3, 4, 15, 16, 17, 18, 19):
        s.piece("village", "vine", x, 6) if x != 19 else s.piece("village", "vine_end", x, 6)
    s.m[6:8, 0:24][s.m[6:8, 0:24] == GRASS] = TALL
    s.m[7, 0:24] = TALL
    # the houses, the well, the path down
    s.rect(0, 8, 23, 10, PATH)
    s.front("cube_pot", 1, 8)
    s.front("cube", 17, 8)
    s.piece("village", "well", 9, 10)
    s.piece("village", "trough", 10, 10)
    # the boathouses at the waterline, the jetty, the bay
    s.rect(0, 11, 23, 12, SAND)
    for i, col in enumerate(("red", "blue", "green")):
        x = 1 + i * 4
        for j, row in enumerate((("R_L", "R_M", "R_R"), ("U_L", "U_balcony" if col == "red" else
                                                         f"U_balcony_{col}", "U_R"))):
            for k, n in enumerate(row):
                s.piece("boathouse", n, x + k, 11 + j)
        s.piece("boathouse", "land_door", x, 13)
        s.piece("boathouse", f"sea_{col}_L", x + 1, 13)
        s.piece("boathouse", f"sea_{col}_R", x + 2, 13)
        s.piece("boathouse", "slip_L", x + 1, 14)
        s.piece("boathouse", "slip_R", x + 2, 14)
    s.shore(["############", "~~~~~~~~~~~~", "~~~~~~~~~~~~", "~~~~~~~~~~~~"], 12, 13)
    s.rect(0, 14, 0, 17, SEA)
    s.rect(4, 14, 4, 17, SEA)
    s.rect(8, 14, 8, 17, SEA)
    s.rect(0, 15, 11, 17, SEA)
    for x in range(1, 12):
        if (x - 1) % 4 in (1, 2):
            pass
    # the pumice cliffs at the bay's end
    for x, n in ((19, "top_L"), (20, "top"), (21, "top"), (22, "top"), (23, "top_R")):
        s.piece("pumice", n, x, 13)
    for x, n in ((19, "foot_L"), (20, "foot"), (21, "foot"), (22, "foot"), (23, "foot_R")):
        s.piece("pumice", n, x, 14)
    s.rect(19, 15, 23, 17, SEA)
    s.piece("pumice", "hollow", 21, 13)
    s.piece("rocks", "tide_rock", 15, 16)
    return s


def temple():
    """The gallery of the Temple of Aphrodite (16 x 14): its back wall with the
    frieze, wall mirrors, columns with roses, plinths, rose petals; a doorway
    through to the rose court, with its beds and Galatea's dais beyond."""
    s = Scene("temple_aphrodite", 16, 14, fill=0)
    fl = s.s["floor"]
    s.rect(0, 0, 15, 13, fl["ids"][0][7])
    # the rose court above
    for x in range(1, 15):
        s.piece("walls", "top", x, 0)
    s.piece("walls", "top_L", 1, 0)
    s.piece("walls", "top_R", 14, 0)
    for x in range(1, 15):
        s.piece("court", "gravel", x, 1)
        s.piece("court", "gravel", x, 2)
        s.piece("court", "gravel", x, 3)
    s.put("dais", 6, 0)
    for (x, y, n) in ((2, 2, "bed_NW"), (3, 2, "bed_NE"), (2, 3, "bed_SW"), (3, 3, "bed_SE"),
                      (12, 2, "bed_NW"), (13, 2, "bed_NE"), (12, 3, "bed_SW"), (13, 3, "bed_SE")):
        s.piece("court", n, x, y)
    s.piece("court", "urn", 5, 3)
    s.piece("court", "urn", 10, 3)
    s.piece("court", "gravel_petals", 7, 3)
    for y in range(0, 14):
        s.piece("walls", "side_L", 0, y)
        s.piece("walls", "side_R", 15, y)
    # the partition between the court and the gallery, its doorway
    for x in range(1, 15):
        s.piece("walls", "part", x, 4)
        s.piece("walls", "lower", x, 5)
    s.piece("walls", "door_top", 12, 4)
    s.piece("walls", "door", 12, 5)
    s.piece("mirrors", "mirror_N", 3, 5)
    s.piece("walls", "fresco", 6, 5)
    s.piece("walls", "lower_niche", 8, 5)
    # the gallery floor, columns, plinths, petals
    for y in range(6, 13):
        for x in range(1, 15):
            s.piece("floor", "floor" if (x + y) % 3 else "floor_b", x, y)
    for x in (2, 6, 10, 13):
        s.piece("gallery", "col_top", x, 7)
        s.piece("gallery", "col_base", x, 8)
        s.piece("gallery", "col_top", x, 10)
        s.piece("gallery", "col_base", x, 11)
    for (x, y) in ((4, 8), (8, 8), (4, 11), (11, 11)):
        s.piece("gallery", "plinth" if (x + y) % 2 else "plinth_rose", x, y)
    for (x, y) in ((5, 6), (9, 9), (12, 12), (3, 12)):
        s.piece("floor", "petals" if x % 2 else "petals_b", x, y)
    s.piece("mirrors", "mirror_E", 14, 9)
    s.piece("floor", "threshold", 2, 13)
    s.piece("floor", "exit", 3, 13)
    s.piece("gallery", "altar", 8, 12)
    return s


SCENES = {
    "paphia": (paphia, "paphia_town.png", 2),
    "neraida": (neraida, "neraida_falls.png", 2),
    "melos": (melos, "melos_klima.png", 2),
    "temple": (temple, "temple_aphrodite_gallery.png", 2),
    "harbor_street": (harbor_street, "skandeia_harbor_street.png", 3),
    "skandeia": (skandeia, "skandeia_town.png", 2),
    "foam_beach": (foam_beach, "kythera_foam_beach.png", 3),
    "foam_road": (foam_road, "kythera_foam_road.png", 2),
    "spring": (spring, "kythera_spring.png", 2),
}


ONE_X = {"foam_beach", "harbor_street"}     # the 240 x 160 screens get a 1x copy too


def main(names):
    IMG.mkdir(parents=True, exist_ok=True)
    for n in names or list(SCENES):
        fn, out, sc = SCENES[n]
        s = fn()
        s.render(IMG / out, scale=sc)
        if n in ONE_X:
            s.render(IMG / out.replace(".png", "_1x.png"), scale=1)


if __name__ == "__main__":
    main(sys.argv[1:])
