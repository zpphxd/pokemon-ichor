#!/usr/bin/env python3
"""Compose and render mock-up scenes from gTileset_Skiron's catalog.

Not maps: four 30x20 scenes, built only from aethos and Skiron metatiles, to
prove the set before the Route 4 and Route 5 maps are laid out. Each scene is
written as code (ground regions, then pieces placed by catalog key), auto-tiled
like a map builder would (the paved road and tall grass by shape key), and
rendered at 2x to design/phase2/img/skiron_<scene>.png. Review copies go to
build/render/skiron/: collision tinted red over blocked cells, and the 15x10
GBA-screen crops a player would see.

Usage:
  /usr/bin/python3 tools/ichor/art/skiron_mockups.py            # render all scenes
  /usr/bin/python3 tools/ichor/art/skiron_mockups.py --shapes   # list the road and grass
                                                                # shapes they need
After --shapes changes tools/ichor/art/skiron_shapes.json, rebuild the tileset
(skiron_build.py) and render again.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map as rm  # noqa: E402
from skiron_ground import FULL, canon  # noqa: E402

CATALOG = ROOT / "build/skiron/catalog.json"
SHAPES = Path(__file__).resolve().parent / "skiron_shapes.json"
IMG = ROOT / "design/phase2/img"
REVIEW = ROOT / "build/render/skiron"

# aethos metatiles (TILES_aethos.md)
GRASS, TALL, FLOWERS, SEA = 0x001, 0x00D, 0x004, 0x170
HERM, SIGN, BOULDER = 0x01B, 0x003, 0x0E0
PATH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
        "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
OLIVE_TOP, OLIVE_BOTTOM = (0x1D4, 0x1D5), (0x1E4, 0x1E5)
OLIVE_TIP = {GRASS: (0x1CE, 0x1CF), TALL: (0x1C6, 0x1C7)}
CYPRESS_TOP = {GRASS: 0x00E, TALL: 0x025}
CYPRESS_BOTTOM = 0x016
STONE_PINE = (0x01E, 0x01F, 0x026, 0x027)
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def hashpct(x, y, salt):
    h = (x * 73856093 ^ y * 19349663 ^ salt * 83492791) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h >> 8) % 100


class Scene:
    def __init__(self, name, title, w=30, h=20, cat=None):
        self.name, self.title, self.w, self.h = name, title, w, h
        self.cat = cat
        self.ground = [["grass"] * w for _ in range(h)]   # grass / road / tall / path / sea
        self.mid = np.full((h, w), GRASS, int)
        self.walk = [["."] * w for _ in range(h)]
        self.fixed = np.zeros((h, w), bool)                # cells a piece has claimed
        self.road_floor = np.zeros((h, w), bool)           # pieces drawn on the road's floor
        self.path_floor = np.zeros((h, w), bool)           # pieces on borrowed aethos path
        self.missing = {"road": set(), "tall": set()}

    # ---- regions -------------------------------------------------------
    def fill(self, kind, x0, y0, x1, y1):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.ground[y][x] = kind

    def cells(self, kind, pts):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.ground[y][x] = kind

    # ---- pieces --------------------------------------------------------
    def piece(self, key, x, y, cells=None):
        """Place a catalog structure (or some of its cells) with its walk codes."""
        s = self.cat[key]
        for cy in range(s["h"]):
            for cx in range(s["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                X, Y = x + cx, y + cy
                if not (0 <= X < self.w and 0 <= Y < self.h):
                    continue
                self.mid[Y, X] = s["ids"][cy][cx]
                self.walk[Y][X] = s["walk"][cy][cx]
                self.fixed[Y, X] = True
                if s["ground"].get(f"{cx},{cy}") == "path":
                    self.path_floor[Y, X] = True
                if key in ("rubble", "rubble_cleared", "rubble_small", "rubble_small_cleared"):
                    self.road_floor[Y, X] = True

    def named(self, key, name, x, y):
        s = self.cat[key]
        cx, cy = s["names"][name]
        self.piece(key, x - cx, y - cy, cells={(cx, cy)})

    def put(self, mid, x, y, walk="X"):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.walk[y][x] = walk
            self.fixed[y, x] = True

    def olive(self, x, y):
        self.put(OLIVE_TOP[0], x, y)
        self.put(OLIVE_TOP[1], x + 1, y)
        self.put(OLIVE_BOTTOM[0], x, y + 1)
        self.put(OLIVE_BOTTOM[1], x + 1, y + 1)
        self.tips = getattr(self, "tips", []) + [(x, y - 1)]

    def cypress(self, x, y):
        self.cyp = getattr(self, "cyp", []) + [(x, y)]
        self.put(CYPRESS_BOTTOM, x, y + 1)
        self.fixed[y, x] = True
        self.walk[y][x] = "T"

    def stone_pine(self, x, y):
        for i, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            self.put(STONE_PINE[i], x + dx, y + dy)

    # ---- auto-tiling ---------------------------------------------------
    def region(self, kind):
        kinds = {"tall": ("tall", "meadow")}.get(kind, (kind,))
        m = np.array([[g in kinds for g in row] for row in self.ground])
        if kind == "road":
            m |= self.road_floor
        if kind == "path":
            m |= self.path_floor
        return m

    def key(self, m, x, y):
        nb = []
        for dx, dy in DIRS:
            X, Y = x + dx, y + dy
            inside = m[Y, X] if 0 <= X < self.w and 0 <= Y < self.h else m[min(max(Y, 0), self.h - 1), min(max(X, 0), self.w - 1)]
            nb.append("1" if inside else "0")
        return canon("1", nb)

    def autotile(self):
        road, tall = self.cat["road"], self.cat["tall"]
        rm_ = self.region("road")
        tm = self.region("tall")
        pm = self.region("path")
        for y in range(self.h):
            for x in range(self.w):
                if self.fixed[y, x]:
                    continue
                g = self.ground[y][x]
                if g == "road":
                    k = self.key(rm_, x, y)
                    if k == FULL:
                        r = hashpct(x, y, 3)
                        name = "mid3" if r < 8 else "mid2" if r < 22 else "mid"
                    else:
                        name = k
                    if name not in road["names"]:
                        self.missing["road"].add(k)
                        name = "mid"
                    cx, cy = road["names"][name]
                    self.mid[y, x] = road["ids"][cy][cx]
                elif g in ("tall", "meadow"):
                    k = self.key(tm, x, y)
                    self.walk[y][x] = "G"
                    if k == FULL:
                        thyme = g == "meadow" and hashpct(x, y, 9) < 70
                        if thyme:
                            th = self.cat["tall_thyme"]
                            self.mid[y, x] = th["ids"][0][0]
                        else:
                            self.mid[y, x] = TALL
                        continue
                    if k not in tall["names"]:
                        self.missing["tall"].add(k)
                        self.mid[y, x] = TALL
                        continue
                    cx, cy = tall["names"][k]
                    self.mid[y, x] = tall["ids"][cy][cx]
                elif g == "path":
                    n = lambda dx, dy: (not (0 <= y + dy < self.h and 0 <= x + dx < self.w)
                                        or pm[y + dy, x + dx])
                    v = ("T" if not n(0, -1) else "B" if not n(0, 1) else "")
                    hside = ("L" if not n(-1, 0) else "R" if not n(1, 0) else "")
                    self.mid[y, x] = PATH.get(v + hside, PATH.get(v or hside or "C", PATH["C"]))
                elif g == "sea":
                    self.mid[y, x] = SEA
                    self.walk[y][x] = "~"
                elif g == "flowers":
                    self.mid[y, x] = FLOWERS
                else:
                    self.mid[y, x] = GRASS
        # tree tops need to know what they stand over
        for (x, y) in getattr(self, "cyp", []):
            under = TALL if self.ground[y][x] == "tall" else GRASS
            self.mid[y, x] = CYPRESS_TOP[under]
        for (x, y) in getattr(self, "tips", []):
            if 0 <= y and not self.fixed[y, x] and not self.fixed[y, x + 1]:
                g = self.mid[y, x]
                if g in OLIVE_TIP:
                    self.mid[y, x], self.mid[y, x + 1] = OLIVE_TIP[g]
                    self.walk[y][x] = self.walk[y][x + 1] = "T"

    # ---- rendering -----------------------------------------------------
    def render(self, renderer, scale=2):
        img = np.zeros((self.h * 16, self.w * 16, 3), np.uint8)
        for y in range(self.h):
            for x in range(self.w):
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = renderer.metatile(int(self.mid[y, x]))[0]
        im = Image.fromarray(img)
        return im.resize((im.width * scale, im.height * scale), Image.NEAREST), im

    def walk_overlay(self, im):
        """Blocked cells tinted red, tall grass green, ledges blue, water cyan."""
        a = np.array(im).astype(np.float32)
        tint = {"X": (255, 0, 0), "J": (0, 80, 255), ">": (0, 80, 255), "<": (0, 80, 255),
                "G": (0, 200, 0), "~": (0, 220, 255)}
        for y in range(self.h):
            for x in range(self.w):
                c = tint.get(self.walk[y][x])
                if c:
                    sl = a[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
                    sl[:] = sl * 0.6 + np.array(c) * 0.4
        return Image.fromarray(a.astype(np.uint8))


# --------------------------------------------------------------------------
# The scenes
# --------------------------------------------------------------------------

def fv(x, y, salt=1):
    """A cliff face variant: mostly plain strata, a feature one cell in four."""
    r = hashpct(x, y, salt)
    return "B" if r < 12 else "C" if r < 25 else "A"


def foot(x, y):
    return "ABC"[hashpct(x, y, 5) % 3]


def plot(S, x0, y0, x1, y1, gate=None):
    """A walled family plot: front (south) wall on y1, back wall on y0, side
    walls on x0 and x1. gate: an x on the front wall left open."""
    for x in range(x0 + 1, x1):
        S.named("plot_wall", "EW", x, y0)
        if gate is not None and x == gate:
            continue
        if gate is not None and x == gate - 1:
            S.named("plot_wall", "W", x, y1)
        elif gate is not None and x == gate + 1:
            S.named("plot_wall", "E", x, y1)
        else:
            S.named("plot_wall", "EW", x, y1)
    for y in range(y0 + 1, y1):
        S.named("plot_wall", "NS", x0, y)
        S.named("plot_wall", "NS", x1, y)
    S.named("plot_wall", "ES", x0, y0)
    S.named("plot_wall", "SW", x1, y0)
    S.named("plot_wall", "NE", x0, y1)
    S.named("plot_wall", "NW", x1, y1)


def scene_road_tombs(cat):
    """Route 4 near the city: the old paved road coming out of the gate, the
    potters' kilns by it, the dead crowding both verges, and a forced band of
    grass where the paving has gone between two family plots."""
    S = Scene("road_tombs", "Route 4: the Isthmus road, kilns and tombs", cat=cat)
    # the road, 3 wide, from the city (east) running west; its paving gives
    # out between the two plots, where the grass has taken it
    S.fill("road", 0, 9, 29, 11)
    S.fill("road", 23, 8, 27, 8)                       # it widens into the kiln yard
    S.fill("tall", 12, 8, 14, 12)                      # the forced band
    # the north plot: the Kallias family, stelai and lekythoi inside
    plot(S, 2, 3, 15, 7)
    S.named("plot_wall", "EW2", 6, 7)
    S.piece("stele_family", 4, 4)
    S.piece("lekythos", 6, 4)
    S.piece("stele_palmette", 8, 4)
    S.piece("lekythos", 10, 4)
    S.piece("stele_family", 12, 4)
    S.piece("stele_low", 5, 6)
    S.piece("stele_low", 9, 6)
    S.piece("stele_low", 13, 6)
    S.cypress(3, 4)
    S.cypress(14, 4)
    S.fill("flowers", 7, 6, 7, 6)
    S.fill("flowers", 11, 6, 11, 6)
    # the south plot across the band, a gate in its wall
    plot(S, 10, 13, 20, 17)
    S.named("plot_wall", "EW2", 17, 13)
    S.piece("sarcophagus", 12, 14)
    S.piece("lekythos", 15, 14)
    S.piece("stele_family", 17, 14)
    S.piece("stele_low", 19, 15)
    S.piece("stele_low", 11, 16)
    S.piece("stele_palmette", 14, 15)
    S.cypress(16, 15)
    # tombs lining the verges outside the plots
    for x, key in ((0, "stele_low"), (1, "lekythos"), (16, "stele_palmette"), (17, "stele_low")):
        S.piece(key, x, 7 if key in ("lekythos", "stele_palmette") else 8)
    for x, key in ((1, "stele_low"), (3, "stele_family"), (6, "stele_low"), (8, "lekythos"),
                   (22, "stele_low"), (23, "stele_palmette")):
        S.piece(key, x, 12)
    S.cypress(5, 12)
    S.cypress(21, 12)
    # the old mound, older than the road, in its own long grass
    S.fill("tall", 0, 16, 7, 18)
    S.fill("tall", 1, 15, 2, 15)
    S.piece("mound", 2, 14)
    S.piece("stele_low", 6, 14)
    S.piece("rock", 8, 15)
    S.piece("oak", 9, 17)
    S.piece("oak", 0, 19)
    S.piece("boulders", 7, 18)
    # the potters' quarter by the gate: two kilns, the drying racks, the wasters
    S.piece("kiln", 19, 3)
    S.piece("kiln", 25, 2)
    S.piece("pot_rack", 21, 6)
    S.piece("pot_rack", 27, 5)
    S.piece("sherds", 23, 4)
    S.piece("sherds", 29, 3)
    S.piece("amphorae", 18, 6)
    S.piece("amphorae", 24, 6)
    S.piece("firewood", 21, 2)
    S.piece("pebbles", 23, 3)
    S.piece("pebbles", 26, 7)
    S.piece("pebbles", 20, 7)
    S.piece("dry_grass", 17, 4)
    S.piece("dry_grass", 28, 7)
    S.piece("dry_grass", 22, 5)
    S.piece("dry_grass", 25, 4)
    S.piece("pebbles", 27, 4)
    S.piece("dry_grass", 19, 7)
    S.piece("dry_grass", 20, 5)
    S.cypress(17, 1)
    S.piece("oak", 28, 0)
    # the hill behind: a terrace lip, Aleppo pines, scrub
    S.named("lip", "W", 0, 1)
    for x in range(1, 9):
        S.named("lip", "run", x, 1)
    S.named("lip", "E", 9, 1)
    S.piece("pine_young", 11, 0)
    S.piece("pine_tall", 13, -1)
    S.piece("oak", 15, 1)
    S.piece("rock", 10, 2)
    S.piece("thyme", 16, 2)
    # the hillside above the lip: scrub, rock and pines on the higher terrace
    for (key, x, y) in (("oak", 0, 0), ("pine_young", 2, -1), ("rock", 4, 0), ("oak", 5, 0),
                        ("boulders", 6, -1), ("dry_grass", 8, 0), ("oak", 9, 0)):
        S.piece(key, x, y)
    S.piece("thyme", 0, 2)
    S.piece("dry_grass", 1, 2)
    # south east: olives, a herm and a milestone where the road leaves the city
    S.olive(23, 15)
    S.olive(26, 14)
    S.olive(21, 18)
    S.olive(25, 18)
    S.olive(28, 17)
    S.cypress(28, 12)
    S.piece("milestone", 26, 12)
    S.put(HERM, 24, 12)
    S.put(SIGN, 29, 8)
    S.piece("dry_grass", 22, 14)
    S.piece("thyme", 29, 15)
    S.fill("flowers", 27, 13, 27, 13)
    return S


def scene_rockslide(cat):
    """Route 4 at the foot of the pass: the Titans' rockslide, a toppled tomb
    in three heaps across the road, the procession camped this side of it,
    and the terrace orchard behind its thicket."""
    S = Scene("rockslide_camp", "Route 4: the rockslide and the procession's camp", cat=cat)
    S.fill("road", 0, 10, 29, 12)
    # the cut bank north of the road, where the hill came down
    for x in range(0, 14):
        S.named("cliff_brink", "bite" if x in (4, 9) else ("B" if x % 4 == 1 else "A"), x, 6)
        S.named("cliff", "face_u_" + fv(x, 7), x, 7)
        S.named("bank_grass", "foot_" + "ABC"[x % 3], x, 8)
    S.named("bank_end_e", "brink", 14, 6)
    S.named("bank_end_e", "face_u", 14, 7)
    S.named("bank_end_grass", "foot_e", 14, 8)
    S.piece("rock", 15, 7)
    # the slope above: boulders and scree that came down with it, pines
    S.piece("boulders", 3, 4)
    S.piece("boulders", 8, 3)
    S.piece("rock", 6, 5)
    S.piece("rock", 11, 5)
    S.piece("rock", 1, 4)
    S.piece("pebbles", 5, 4)
    S.piece("pebbles", 12, 4)
    S.piece("pebbles", 7, 2)
    S.piece("pine_lean_w", 0, 0)
    S.piece("pine_young", 5, 1)
    S.piece("pine_tall", 10, -1)
    S.piece("oak", 13, 3)
    S.piece("dry_grass", 3, 2)
    # the rockslide across the road: three heaps, and boulders on the verges
    S.piece("rubble", 5, 10)
    S.piece("rubble_small", 5, 12)
    S.piece("rubble_small", 6, 12)
    S.piece("rubble", 7, 11)
    S.piece("rubble_small", 7, 10)
    S.piece("rubble_small", 8, 10)
    for (key, x, y) in (("rock", 4, 9), ("pebbles", 5, 9), ("rock", 6, 9), ("pebbles", 8, 9),
                        ("rock", 9, 9), ("pebbles", 10, 9), ("pebbles", 3, 9)):
        S.piece(key, x, y)
    S.piece("boulders", 5, 13)
    S.piece("rock", 8, 13)
    S.piece("drum", 7, 14)
    S.piece("pebbles", 4, 13)
    S.piece("pebbles", 9, 13)
    # the terrace orchard, up a wall north of the road: olives, and steps a
    # thicket has closed (Demeter's Sickle, the end of Act I)
    S.named("terrace_wall", "W", 15, 8)
    for x in range(16, 29):
        S.named("terrace_wall", "steps" if x == 21 else "run", x, 8)
    S.named("terrace_wall", "E", 29, 8)
    S.piece("oak", 21, 7)                              # where the Sickle's thicket will stand
    for (x, y) in ((16, 5), (19, 5), (23, 5), (26, 5), (17, 2), (21, 2), (25, 2)):
        S.olive(x, y)
    S.piece("dry_grass", 28, 2)
    S.piece("thyme", 15, 3)
    S.cypress(29, 4)
    S.cypress(15, 0)
    # the camp, south of the road, east of the slide: tents round a cookfire
    S.piece("cart", 10, 14)
    S.piece("milestone", 13, 13)
    S.piece("tent", 14, 13)
    S.piece("tent_b", 17, 13)
    S.piece("tent", 22, 13)
    S.piece("tent_b", 25, 14)
    S.piece("cookfire", 20, 15)
    S.piece("bedrolls", 19, 16)
    S.piece("bedrolls", 21, 16)
    S.piece("myrtle", 16, 15)
    S.piece("myrtle", 24, 16)
    S.piece("baskets", 23, 16)
    S.piece("baskets", 13, 16)
    S.piece("pebbles", 20, 14)
    S.piece("dry_grass", 18, 16)
    S.piece("dry_grass", 15, 16)
    S.piece("pebbles", 22, 15)
    S.piece("stele_low", 28, 13)
    S.cypress(28, 15)
    # south: the slope down, long grass and scrub
    S.fill("tall", 0, 15, 8, 18)
    S.fill("tall", 1, 14, 3, 14)
    S.fill("tall", 24, 18, 29, 19)
    S.piece("oak", 10, 17)
    S.piece("rock", 12, 18)
    S.piece("pine_lean", 13, 17)
    S.piece("oak", 9, 19)
    S.piece("rock", 22, 19)
    S.piece("thyme", 20, 19)
    return S


def scene_cliff_road(cat):
    """Route 5: the road cut along the Skironian cliffs. Pines and scrub on
    the mountain above, the cut bank with Aphrodite's niches, the railless
    edge with bites taken out of it, the rock seat on a narrow shoulder over
    the drop, and the sea far below."""
    S = Scene("cliff_road", "Route 5: the Skironian cliff road", cat=cat)
    # the mountainside: pines in staggered rows, scrub and rock between
    for (key, x, y) in (("pine_lean", 0, -1), ("pine_tall", 4, -1), ("pine_young", 7, 0),
                        ("pine_tall", 9, 0), ("pine_lean_w", 16, -1), ("pine_tall", 21, -1),
                        ("pine_young", 24, 0), ("pine_tall", 26, 0)):
        S.piece(key, x, y)
    for (key, x, y) in (("oak", 3, 2), ("rock", 6, 2), ("oak", 11, 0), ("boulders", 12, 1),
                        ("oak", 14, 3), ("thyme", 15, 2), ("dry_grass", 19, 2), ("oak", 20, 3),
                        ("rock", 23, 3), ("oak", 29, 3), ("dry_grass", 8, 3), ("thyme", 25, 3),
                        ("oak", 14, 0), ("rock", 19, 1), ("oak", 2, 3), ("pine_young", 13, -1),
                        ("oak", 7, 3), ("thyme", 10, 3), ("oak", 16, 3), ("dry_grass", 26, 3),
                        ("oak", 22, 3), ("rock", 28, 2)):
        S.piece(key, x, y)
    S.fill("tall", 17, 2, 18, 3)
    # the cut bank (brink, face, foot on the road)
    for x in range(30):
        S.named("cliff_brink", "B" if x % 5 == 2 else "A", x, 4)
        S.named("cliff", "face_u_" + fv(x, 5, 2), x, 5)
        S.named("bank", "foot_" + "ABC"[(x * 5) % 3], x, 6)
    S.piece("niches", 11, 4)
    # the road: the aethos path, three wide; the seat narrows it to one
    S.fill("path", 0, 7, 29, 9)
    S.piece("rock_seat_path", 21, 8)
    S.piece("rock_path", 20, 9)
    S.piece("rock_path", 23, 9)
    S.piece("pebbles_path", 19, 9)
    S.piece("pebbles_path", 5, 8)
    S.piece("milestone_path", 1, 7)
    S.piece("rock_path", 27, 7)
    S.put(HERM, 29, 7)
    # the railless edge, bitten into, and the drop
    for x in range(30):
        S.named("cliff_path", "bite" if x in (7, 16, 26) else ("B" if x % 6 == 3 else "A"), x, 10)
        S.named("cliff", "face_u_" + fv(x, 11), x, 11)
        S.named("cliff", "face_l_" + fv(x, 12, 3), x, 12)
        S.named("cliff", "face_u_" + fv(x, 13, 4), x, 13)
        S.named("cliff", "foot_" + foot(x, 14), x, 14)
    S.fill("sea", 0, 15, 29, 19)
    for (x, y, v) in ((3, 16, "A"), (11, 17, "B"), (17, 16, "A"), (25, 18, "B"), (28, 16, "A"),
                      (7, 19, "A"), (21, 19, "B")):
        S.named("surf_rock", v, x, y)
    return S


def scene_headland(cat):
    """Route 5 further on: the road leaves the edge for a thyme meadow and a
    beekeeper's hives; a ruined watchtower stands on the headland behind a
    fallen column drum, and the coast steps down to the east."""
    S = Scene("headland", "Route 5: the thyme meadow and the watchtower", cat=cat)
    S.fill("path", 0, 7, 29, 8)
    # the coast: the headland's cliff to x=11, the shore lower and further
    # south east of it (a side and an inner corner where it steps)
    for x in range(0, 12):
        S.named("cliff_brink", "B" if x % 4 == 1 else "A", x, 13)
        S.named("cliff", "face_u_" + fv(x, 14), x, 14)
        S.named("cliff", "face_l_" + fv(x, 15, 3), x, 15)
        S.named("cliff", "foot_" + foot(x, 16), x, 16)
    S.named("cliff_side", "in_sw", 12, 13)
    S.named("cliff_side", "side_w", 12, 14)
    for x in range(12, 30):
        S.named("cliff_brink", "bite" if x == 21 else ("B" if x % 4 == 0 else "A"), x, 15)
        S.named("cliff", "face_u_" + fv(x, 16), x, 16)
        S.named("cliff", "foot_" + foot(x, 17), x, 17)
    S.fill("sea", 0, 17, 11, 19)
    S.fill("sea", 12, 18, 29, 19)
    for (x, y, v) in ((4, 18, "A"), (9, 19, "B"), (16, 19, "A"), (26, 18, "B")):
        S.named("surf_rock", v, x, y)
    # the watchtower on the headland, a column drum across the way to it
    S.piece("watchtower", 3, 9)
    S.piece("drum", 6, 11)
    S.piece("rock", 7, 12)
    S.piece("rock", 5, 12)
    S.piece("pebbles", 2, 12)
    S.piece("dry_grass", 1, 10)
    S.piece("oak", 0, 12)
    S.piece("thyme", 8, 10)
    S.piece("dry_grass", 9, 12)
    S.piece("oak", 10, 11)
    # the cliff top east: a windbent pine, long grass, rocks
    S.piece("pine_lean", 14, 11)
    S.fill("tall", 20, 10, 27, 12)
    S.fill("tall", 22, 13, 26, 13)
    S.piece("rock", 18, 13)
    S.piece("thyme", 19, 11)
    S.piece("dry_grass", 28, 13)
    S.piece("oak", 29, 10)
    S.piece("pebbles", 17, 10)
    # north: the thyme meadow and the hives, the forest beyond
    S.fill("meadow", 11, 2, 19, 5)
    S.fill("meadow", 12, 1, 17, 1)
    S.fill("meadow", 10, 4, 10, 5)
    S.piece("hives", 21, 3)
    S.piece("hives", 21, 5)
    for (x, y) in ((20, 2), (24, 3), (23, 5), (20, 6), (25, 6), (9, 5), (19, 1), (24, 1)):
        S.piece("thyme", x, y)
    for (key, x, y) in (("pine_tall", 0, -1), ("pine_young", 3, 0), ("pine_lean_w", 5, -1),
                        ("pine_tall", 26, -1), ("pine_young", 29, 1), ("oak", 8, 2), ("rock", 9, 0),
                        ("oak", 2, 4), ("rock", 5, 4), ("dry_grass", 7, 5), ("oak", 28, 5),
                        ("oak", 22, 0), ("rock", 0, 5)):
        S.piece(key, x, y)
    S.put(SIGN, 19, 6)
    # flowers and scrub on the open slope between the road and the edge
    for (x0, y0, x1, y1) in ((8, 9, 9, 9), (23, 9, 24, 9), (1, 5, 1, 6)):
        S.fill("flowers", x0, y0, x1, y1)
    for (key, x, y) in (("thyme", 12, 10), ("dry_grass", 16, 9), ("oak", 11, 12), ("thyme", 14, 14),
                        ("rock", 28, 12), ("dry_grass", 7, 9), ("thyme", 27, 9), ("pebbles", 22, 14)):
        S.piece(key, x, y)
    return S


SCENES = [scene_road_tombs, scene_rockslide, scene_cliff_road, scene_headland]


def load_catalog():
    if not CATALOG.exists():
        sys.exit(f"{CATALOG} is missing: run /usr/bin/python3 tools/ichor/art/skiron_build.py")
    return {s["key"]: s for s in json.loads(CATALOG.read_text())}


def crops(im, scene, scale=2):
    """The 15x10 screens a player sees: the four quadrants and the middle."""
    tiles = [(0, 0), (15, 0), (0, 10), (15, 10), (7, 5)]
    pad = 6
    W, H = 15 * 16 * scale, 10 * 16 * scale
    out = Image.new("RGB", (2 * W + 3 * pad, 3 * H + 4 * pad), (24, 24, 28))
    for i, (x, y) in enumerate(tiles):
        c = im.crop((x * 16, y * 16, x * 16 + 240, y * 16 + 160)).resize((W, H), Image.NEAREST)
        out.paste(c, (pad + (i % 2) * (W + pad), pad + (i // 2) * (H + pad)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true", help="update skiron_shapes.json and stop")
    args = ap.parse_args()
    cat = load_catalog()
    scenes = [f(cat) for f in SCENES]
    for S in scenes:
        S.autotile()
    need = {"road": set(), "tall": set()}
    for S in scenes:
        for k in need:
            need[k] |= S.missing[k]
    if args.shapes:
        old = json.loads(SHAPES.read_text()) if SHAPES.exists() else {}
        new = {k: sorted(set(old.get(k, [])) | need[k]) for k in ("road", "tall")}
        SHAPES.write_text(json.dumps(new, indent=1) + "\n")
        print(f"{SHAPES}: road {len(new['road'])}, tall {len(new['tall'])} extra shapes")
        return
    if need["road"] or need["tall"]:
        print("missing shapes (run --shapes, rebuild, render again):", need)
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    r = rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                    rm.Tileset(rm.tileset_from_dir(ROOT / "data/tilesets/secondary/skiron")))
    IMG.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    for S in scenes:
        big, im = S.render(r)
        big.save(IMG / f"skiron_{S.name}.png")
        S.walk_overlay(im).resize(big.size, Image.NEAREST).save(REVIEW / f"{S.name}_walk.png")
        crops(im, S).save(REVIEW / f"{S.name}_screens.png")
        print(IMG / f"skiron_{S.name}.png")


if __name__ == "__main__":
    main()
