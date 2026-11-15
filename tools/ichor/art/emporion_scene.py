#!/usr/bin/env python3
"""Mock scenes of Emporion and the Temple of Hermes, for judging the look.

The scenes are throwaway block data, not maps: a street of merchant houses, the
Agora, the port of Lechaion with the Diolkos, and the Temple of Hermes on its
height, each composed from the catalogs by structure key. The map team builds
the real maps once the Phase 2 script and geography land.

  --fast      composite straight from the drawn structures (no compile needed),
              for iterating on art
  (default)   write each scene's blockdata from build/<tileset>/catalog.json and
              render it with tools/ichor/render_map.py on the compiled tilesets,
              exactly as the game draws it

Writes design/phase2/img/emporion_scene_<name>.png (3x) and, with --pass N,
keeps a copy as emporion_scene_<name>_pass<N>.png.

Usage: /usr/bin/python3 tools/ichor/art/emporion_scene.py [--fast] [--pass N] [--only NAME]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_lib as E  # noqa: E402

ROOT = E.ROOT
IMG = ROOT / "design/phase2/img"
BUILD = ROOT / "build/emporion_scenes"

# aethos metatiles the scenes use
GRASS, PATH, SEA, SAND = 0x001, 0x1D9, 0x170, 0x124
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
PINE_TOP, PINE_BOT = (0x01E, 0x01F), (0x026, 0x027)
HERM, STELE = 0x01B, 0x003


class Canvas:
    """A grid of cells; each is ('a', aethos id) or (tileset, key, cx, cy)."""

    def __init__(self, w, h, tileset="emporion", fill=("a", GRASS)):
        self.w, self.h = w, h
        self.tileset = tileset
        self.g = [[fill for _ in range(w)] for _ in range(h)]

    def a(self, mid, x, y, w=1, h=1):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if 0 <= xx < self.w and 0 <= yy < self.h:
                    self.g[yy][xx] = ("a", mid)

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None, cat=None):
        cat = cat or CATS[self.tileset]
        s = cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                if 0 <= x + i < self.w and 0 <= y + j < self.h:
                    self.g[y + j][x + i] = (self.tileset, key, cx + i, cy + j)

    def cell(self, key, x, y, name=None, cx=0, cy=0):
        """One named (or (cx, cy)) cell of a structure."""
        s = CATS[self.tileset][key]
        if name is not None:
            cx, cy = s["names"][name]
        self.g[y][x] = (self.tileset, key, cx, cy)

    def fill(self, key, x, y, w, h, cx=0, cy=0):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.cell(key, xx, yy, cx=cx, cy=cy)

    def olive(self, x, y):
        self.a(OLIVE_TIP[0], x, y - 1)
        self.a(OLIVE_TIP[1], x + 1, y - 1)
        self.a(OLIVE_TOP[0], x, y)
        self.a(OLIVE_TOP[1], x + 1, y)
        self.a(OLIVE_BOT[0], x, y + 1)
        self.a(OLIVE_BOT[1], x + 1, y + 1)

    def cypress(self, x, y):
        self.a(CYPRESS_TOP, x, y)
        self.a(CYPRESS_BOT, x, y + 1)

    def pine(self, x, y):
        self.a(PINE_TOP[0], x, y)
        self.a(PINE_TOP[1], x + 1, y)
        self.a(PINE_BOT[0], x, y + 1)
        self.a(PINE_BOT[1], x + 1, y + 1)

    def solid(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return False
        c = self.g[y][x]
        if c[0] == "a":
            return False
        ts, key, cx, cy = c
        s = CATS[ts][key]
        walk = s.get("walk")
        # only buildings and walls cast a shadow a cell wide; small props don't
        return bool(walk) and walk[cy][cx] in "XD" and key not in ("paving", "pegasus_column") and \
            (s["h"] >= 3 or key in ("terrace_wall", "warehouse"))

    def auto_shade(self):
        """Lay the shaded flags where a building or wall to the north or west casts
        its shadow on plain paving (light from the top left)."""
        out = [row[:] for row in self.g]
        for y in range(self.h):
            for x in range(self.w):
                c = self.g[y][x]
                if c[0] == "a" or c[1] != "paving" or c[2] > 2:
                    continue
                n, w = self.solid(x, y - 1), self.solid(x - 1, y)
                if n or w:
                    out[y][x] = (c[0], "paving", 6 if (n and w) else 4 if n else 5, 0)
        self.g = out

    # -- rendering -------------------------------------------------------------

    def blockdata(self):
        out = []
        for row in self.g:
            for c in row:
                if c[0] == "a":
                    out.append(c[1])
                else:
                    ts, key, cx, cy = c
                    out.append(CATS[ts][key]["ids"][cy][cx])
        return np.array(out, "<u2")

    def render_fast(self, structs):
        img = np.zeros((self.h * 16, self.w * 16, 3), np.uint8)
        comp = {}
        for y, row in enumerate(self.g):
            for x, c in enumerate(row):
                if c[0] == "a":
                    t = E.aethos_metatile(c[1])
                else:
                    ts, key, cx, cy = c
                    if (ts, key) not in comp:
                        comp[(ts, key)] = E.composite(structs[(ts, key)])
                    t = comp[(ts, key)][cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = t
        return Image.fromarray(img)


CATS = {}


def load_catalogs():
    for ts in ("emporion", "isthmos", "temple_hermes"):
        p = ROOT / f"build/{ts}/catalog.json"
        if p.exists():
            CATS[ts] = {s["key"]: s for s in json.loads(p.read_text())}


def house(c, x, y, n):
    """House recipe n (1-8, TILES_emporion.md) with its top-left cell at (x, y).
    Returns its width."""
    import emporion_city as C
    rows = C.recipe_cells(C.RECIPES[n - 1])
    for j, row in enumerate(rows):
        for i, (key, name) in enumerate(row):
            c.cell(key, x + i, y + j, name)
    return len(rows[0])


def pave(c, x, y, w, h, seed=0):
    """Marble paving with its variants scattered, as a map builder would lay it."""
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            k = (xx * 7 + yy * 13 + seed) % 23
            c.cell("paving", xx, yy, cx=1 if k == 3 else 2 if k in (8, 15) else 0)


def kerb_box(c, x, y, w, h):
    """A paved area with its kerb against the grass around it."""
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            n = ("N" if yy == y else "S" if yy == y + h - 1 else "")
            n += ("W" if xx == x else "E" if xx == x + w - 1 else "")
            c.cell("kerb", xx, yy, {"": "C"}.get(n, n))


# --------------------------------------------------------------------------
# Scenes
# --------------------------------------------------------------------------

def scene_street():
    """Two terraces of merchant houses, all eight recipes, on marble streets."""
    c = Canvas(30, 15)
    pave(c, 0, 0, 30, 15)
    for x in range(30):
        c.a(GRASS, x, 0)
    for x in (2, 9, 16, 24):
        c.cypress(x, -1)
    # the north terrace (rows 1-4; the tall house rises a storey higher)
    x = 1
    for n in (1, 2, 5):
        x += house(c, x, 1, n) + (1 if n == 2 else 0)
    house(c, x + 1, 0, 8)
    # the south terrace
    x = 1
    for n in (3, 4, 6, 7):
        x += house(c, x, 8, n)
        if n == 4:
            x += 1
    # the street between: a herm, planters by the doors, an exedra
    c.put("great_herm", 13, 5)
    c.put("planter", 4, 5)
    c.put("planter", 21, 12)
    c.put("exedra", 26, 6)
    c.put("plaza_rose", 18, 5)
    return c


def scene_agora():
    """The great Agora: the stoa along its north side, the market in the square."""
    c = Canvas(26, 20)
    pave(c, 0, 0, 26, 20, seed=5)
    for x in range(26):
        c.a(GRASS, x, 0)
    for x in (1, 6, 19, 24):
        c.cypress(x, -1)
    # the stoa: west end, nine bays, east end
    x = 2
    c.put("stoa_end_w", x, 1)
    x += 1
    for key in ("stoa_bay", "stoa_bay_door", "stoa_bay_spice", "stoa_agora", "stoa_bay_cloth",
                "stoa_bay", "stoa_bay_pots", "stoa_bay_door", "stoa_bay"):
        c.put(key, x, 1)
        x += 2
    c.put("stoa_end_e", x, 1)
    # acroteria along the stoa's ridge (the house kit's, the same roof tiles)
    for xx in (5, 11, 15, 21):
        c.cell("roof", xx, 1, "acroterion")
    # its stylobate: one row of the broad steps
    c.cell("steps", 2, 6, cx=0, cy=1)
    for xx in range(3, x):
        c.cell("steps", xx, 6, cx=1, cy=1)
    c.cell("steps", x, 6, cx=2, cy=1)
    # the square
    c.put("plaza_rose", 12, 12)
    c.put("pegasus_column", 12, 9)
    for (key, x0, y0) in (("stall_spice", 3, 9), ("stall_bronze", 6, 9), ("stall_fish", 18, 9),
                          ("stall_wine", 21, 9), ("stall_pottery", 3, 14), ("stall_cloth", 7, 14),
                          ("stall_honey", 18, 14)):
        c.put(key, x0, y0)
    c.put("notice_board", 22, 14)
    c.put("exedra", 9, 17)
    c.put("exedra", 15, 17)
    c.put("great_herm", 15, 9)
    c.put("planter", 10, 9)
    # the square's south edge meets the grass
    for xx in range(26):
        c.cell("kerb", xx, 19, "S")
    return c


def scene_temple():
    """The Temple of Hermes on its terrace under Acrocorinth, with the Asclepeion,
    the Peirene, the Hephaisteion and the potters' quarter."""
    c = Canvas(32, 24)
    pave(c, 0, 0, 32, 24, seed=11)
    # Acrocorinth across the top
    seq = ["W", 1, 2, 1, 3, 2, 1, 2, 4, 1, 2, 1, 3, 1, 2, 1, 2, 1, 4, 2, 1, 2, 3, 1, 2, 1, 2, 1,
           2, 1, 2, "E"]
    for i, k in enumerate(seq):
        cx = {"W": 0, "E": 5}.get(k, k)
        for cy in range(3):
            c.cell("acrocorinth", i, cy, cx=cx, cy=cy)
    for x in range(32):
        c.a(GRASS, x, 3)
        c.a(GRASS, x, 4)
    for x in (1, 5, 26, 30):
        c.olive(x, 4)
    for x in (8, 22):
        c.cypress(x, 3)
    # the terrace: the temple, a herm and planters
    c.put("temple_hermes", 12, 4)
    for x in range(9, 22):
        c.cell("paving", x, 11)
    c.put("planter", 10, 9)
    c.put("planter", 20, 9)
    c.put("great_herm", 11, 9)
    # the terrace wall, its stair down to the street, and the cistern mouth
    row = ["W"] + ["run"] * 4 + ["stairs", "stairs", "stairs"] + ["run"] * 2 + \
          ["cistern", "cistern_sign"] + ["run", "E"]
    for i, n in enumerate(row):
        c.cell("terrace_wall", 9 + i, 12, n)
    # the Asclepeion to the east, the Hephaisteion to the west, on the upper level
    c.put("asclepeion", 25, 7)
    for x in range(24, 31):
        c.cell("steps", x, 12, cx=1, cy=1)
    c.cell("steps", 24, 12, cx=0, cy=1)
    c.cell("steps", 30, 12, cx=2, cy=1)
    c.put("hephaisteion", 3, 8)
    c.put("hephaisteion_lit", 4, 10)
    # the Peirene on the lower street, and the potters' quarter
    c.put("peirene", 13, 15)
    c.put("exedra", 18, 17)
    c.put("exedra", 11, 17)
    for x in range(0, 9):
        for y in range(15, 24):
            c.cell("yard", x, y)
    c.put("kiln", 1, 15)
    c.put("vase_rack", 4, 16)
    c.put("forge", 1, 19)
    c.put("smith_props", 4, 20)
    c.put("perfumer", 6, 18)
    house(c, 22, 15, 7)
    house(c, 25, 15, 4)
    return c


def scene_port():
    """The port of Lechaion (gTileset_Isthmos): quays, sheds, warehouses, the crane,
    the moored ship and, beyond, the Diolkos with a ship on her cradle."""
    c = Canvas(32, 22, tileset="isthmos", fill=("a", SEA))
    # the quay: rows 4-8, with its edges
    for y in range(4, 9):
        for x in range(0, 32):
            c.cell("quay", x, y, "N" if y == 4 else "C")
    c.put("ship", 2, 1)
    c.cell("bollards", 4, 4, cx=1)
    c.cell("bollards", 9, 4, cx=0)
    c.cell("bollards", 14, 4, cx=0)
    c.put("crane", 17, 4)
    c.put("harbor_goods", 11, 6)
    c.put("stall_fish", 22, 5)
    c.put("stall_wine", 25, 5)
    # warehouses with house-kit roofs; the hiring hall has the chalked board
    for x0, cells in ((1, ["W", "wall", "door_l", "door_r", "board", "E"]),
                      (8, ["W", "wall", "door_l", "door_r", "wall", "E"])):
        for i, n in enumerate(cells):
            part = "W" if i == 0 else "E" if i == len(cells) - 1 else "run"
            c.cell("roof", x0 + i, 9, part)
            c.cell("roof", x0 + i, 10, {"W": "eaves_W", "E": "eaves_E", "run": "eaves_run"}[part])
            c.cell("warehouse", x0 + i, 11, cx={"W": 0, "wall": 1, "door_l": 2, "door_r": 3,
                                                 "board": 4, "E": 5}[n])
    for y in range(9, 14):
        c.cell("quay", 0, y, "C")
        c.cell("quay", 7, y, "C")
        c.cell("quay", 14, y, "C")
    for x in range(0, 15):
        c.cell("quay", x, 12, "C")
        c.cell("quay", x, 13, "S")
    # the ship sheds on their basin
    c.cell("shed_end_w", 15, 9)
    c.cell("shed_end_w", 15, 10, cy=1)
    c.cell("shed_end_w", 15, 11, cy=2)
    for b in range(3):
        c.put("shed_bay", 16 + b * 2, 9)
    c.put("shed_end_e", 22, 9)
    for x in range(23, 32):
        for y in range(9, 12):
            c.cell("quay", x, y, "C")
    c.put("hull_stocks", 24, 9)
    c.put("timber", 28, 10)
    for x in range(15, 32):
        c.a(SEA, x, 12)
        c.a(SEA, x, 13)
    # the Isthmus beyond the harbor channel: grass, pines and the Diolkos
    for y in range(15, 22):
        for x in range(32):
            c.a(GRASS, x, y)
    for x in range(0, 32):
        c.cell("diolkos", x, 19, cx=0 if x == 0 else (2 if x % 7 == 3 else 1))
    c.put("ship_cradle", 12, 17)
    c.put("capstan", 20, 18)
    for x in (2, 6, 26):
        c.pine(x, 15)
    c.cypress(30, 15)
    c.put("wreath_post", 23, 15)
    return c


def scene_temple_interior():
    """The Herald's Run (gTileset_TempleHermes on oikos): the entry porch, the
    switchback stoa, the upper colonnade and Kerykos's rostrum."""
    W, H = 21, 26
    c = Canvas(W, H, tileset="temple_hermes", fill=("temple_hermes", "floor", 1, 0))

    def t(name, x, y, key=None):
        k = key or {"f": "floor", "l": "lane", "w": "wall", "h": "herm", "b": "balustrade",
                    "r": "rostrum", "p": "props", "s": "turnstile", "c": "column",
                    "g": "pigeonholes", "t": "scroll_table"}[name[0]]
        c.cell(k, x, y, name[2:])

    # walls
    for x in range(W):
        t("w:cornice", x, 0)
        t("w:frieze", x, 1)
        t("w:lower", x, 2)
    motifs = ["frieze_wings", "frieze_caduceus", "frieze_petasos", "frieze_talaria", "frieze_lyre"]
    for i, x in enumerate(range(2, W - 2, 2)):
        t("w:" + motifs[i % 5], x, 1)
    t("w:frieze_runner_l", 9, 1)
    t("w:frieze_runner_r", 10, 1)
    t("w:frieze_wings", 11, 1)
    for x in (3, 17):
        t("w:lower_torch", x, 2)
    for x in (6, 14):
        t("w:lower_niche", x, 2)
    for y in range(0, H - 1):
        t("w:side_w", 0, y)
        t("w:side_e", W - 1, y)
    t("w:cornice_w", 1, 0)
    t("w:cornice_e", W - 2, 0)
    # pigeonholes in the wall either side of the rostrum
    for x0 in (2, 17):
        t("g:wall_tl", x0, 1)
        t("g:wall_tr", x0 + 1, 1)
        t("g:wall_bl", x0, 2)
        t("g:wall_br", x0 + 1, 2)
    # the upper colonnade and the rostrum (rows 3-7)
    for y in (3, 4, 5):
        for x in range(1, W - 1):
            t("r:dais", x, y)
    t("r:dais_roundel", 10, 3)
    t("r:lectern", 10, 4)
    for x in (8, 12):
        t("c:statue_top", x, 3)
        t("c:statue_mid", x, 4)
        t("c:statue_bot", x, 5)
    for x in (6, 14):
        t("p:torch_lit", x, 4)
        t("p:torch_stand", x, 5)
    t("h:head_oiled_s", 3, 4)
    t("h:shaft", 3, 5)
    t("h:head_oiled_s", 17, 4)
    t("h:shaft_scroll", 17, 5)
    for x in range(1, W - 1):
        t("r:dais_lip", x, 6)
        t("r:riser", x, 7)
    t("r:riser_w", 1, 7)
    t("r:riser_e", W - 2, 7)
    for x in (9, 10, 11):
        t("r:steps", x, 7)
    # the switchback stoa (rows 8-18): balustrades with gaps, turnstiles, herms
    for x in range(1, W - 1):
        for y in (8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18):
            t("f:slab", x, y)
    def wall_run(y, gap_x, gap_piece):
        for x in range(2, W - 2):
            if x == gap_x:
                continue
            arms = "EW"
            if x == 2:
                arms = "E"
            elif x == W - 3:
                arms = "W"
            elif x == gap_x - 1:
                arms = "W"
            elif x == gap_x + 1:
                arms = "E"
            t("b:" + arms, x, y)
    wall_run(10, 15, None)
    t("s:turn_n", 15, 10)
    wall_run(14, 5, None)
    t("s:turn_n", 5, 14)
    t("s:gate_h_shut", 9, 14)
    # the lanes of the run, inlaid along the path
    for x in range(6, 15):
        t("l:h", x, 12)
    t("l:wn", 15, 12)
    t("l:arrow_n", 15, 11)
    t("l:es", 5, 12)
    t("l:arrow_n", 5, 13)
    for x in range(6, 16):
        t("l:h", x, 9)
    t("l:start_h", 10, 9)
    # herms at the lanes' ends: anointed ones turned to point the way
    t("h:head_oiled_e", 2, 11)
    t("h:shaft", 2, 12)
    t("h:head_w", 18, 11)
    t("h:shaft", 18, 12)
    t("h:head_s", 2, 15)
    t("h:shaft_scroll", 2, 16)
    t("h:head_oiled_w", 18, 15)
    t("h:shaft", 18, 16)
    # columns down the sides
    for y in (8, 12, 16, 20):
        t("c:col_top", 1, y)
        t("c:col_bot", 1, y + 1)
        t("c:col_top", W - 2, y)
        t("c:col_bot", W - 2, y + 1)
    # the entry porch (rows 19-24): the scroll table, the step-glass, the oil, the first lane
    for x in range(2, W - 2):
        for y in range(19, 25):
            t("f:slab", x, y)
    t("t:full_l", 4, 20)
    t("t:full_r", 5, 20)
    t("p:glass_top", 15, 19)
    t("p:glass_stand", 15, 20)
    t("p:oil", 7, 20)
    t("p:basket_full", 13, 20)
    t("r:mosaic_tl", 9, 21)
    t("r:mosaic_tr", 10, 21)
    t("r:mosaic_bl", 9, 22)
    t("r:mosaic_br", 10, 22)
    t("f:wing", 12, 23)
    t("f:worn", 10, 24)
    t("f:vein_a", 6, 23)
    for x in range(3, 9):
        t("l:h", x, 17)
    t("l:post", 9, 17)
    # the doormat on the bottom row
    for x in range(W):
        t("f:void", x, H - 1)
    t("w:mat_l", 9, H - 1)
    t("w:mat_m", 10, H - 1)
    t("w:mat_r", 11, H - 1)
    return c


SCENES = {"street": scene_street, "agora": scene_agora, "temple": scene_temple,
          "port": scene_port, "temple_interior": scene_temple_interior}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pass", dest="pass_no", type=int)
    ap.add_argument("--only")
    ap.add_argument("--scale", type=int, default=3)
    args = ap.parse_args()
    IMG.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    load_catalogs()
    structs = {}
    if args.fast:
        import importlib
        from kalliste_lib import pack
        for ts, mod in (("emporion", "emporion_art"), ("isthmos", "isthmos_art"),
                        ("temple_hermes", "temple_hermes")):
            sections = importlib.import_module(mod).build()
            pack(sections)
            CATS[ts] = {}
            for _, ss in sections:
                for s in ss:
                    structs[(ts, s.key)] = s
                    CATS[ts][s.key] = {"key": s.key, "w": s.w, "h": s.h, "ids": s.ids,
                                       "walk": s.walk,
                                       "names": {n: list(v) for n, v in
                                                 getattr(s, "names", {}).items()}}
    for name, fn in SCENES.items():
        if args.only and name != args.only:
            continue
        c = fn()
        if c.tileset != "temple_hermes":
            c.auto_shade()
        if args.fast:
            img = c.render_fast(structs)
        else:
            bd = BUILD / f"{name}.bin"
            c.blockdata().tofile(bd)
            prim = "oikos" if c.tileset == "temple_hermes" else "aethos"
            out = BUILD / f"{name}.png"
            subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata",
                            str(bd), "--width", str(c.w), "--primary", prim, "--secondary",
                            f"data/tilesets/secondary/{c.tileset}", "-o", str(out)],
                           check=True, capture_output=True)
            img = Image.open(out)
        img = img.resize((img.width * args.scale, img.height * args.scale), Image.NEAREST)
        dst = (BUILD if args.fast else IMG) / f"emporion_scene_{name}.png"
        img.save(dst)
        print(dst)
        if args.pass_no is not None:
            p = IMG / f"emporion_scene_{name}_pass{args.pass_no}.png"
            img.save(p)
            print(p)


if __name__ == "__main__":
    main()
