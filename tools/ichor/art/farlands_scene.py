#!/usr/bin/env python3
"""Showcase scenes for the far lands' tilesets, composed from the real
compiled metatiles (aethos plus one secondary each) and rendered the way the
game draws them. They are mock maps for judging the art, not game maps.

  thrace       the Bistonian Plain: a road, kurgans, a river and ford, a horse
               field in aethos's dry-stone walls (steppe)
  diomedes     Diomedes's yard: the stable, the palisade, the horse field (steppe_camp)
  themiskyra   Themiskyra's gate and practice ground on the Thermodon (steppe_camp)
  abdera       Abdera's harbor street (steppe_town)
  scythia      the Oikoumene's Scythia: feather-grass, a waystone, the
               Arimaspian heights, Lake Maeotis's marsh (steppe)
  erytheia     Erytheia's red pasture at sunset (far_west)
  pillars      the Pillars over the strait (far_west)
  garden       the Garden of the Hesperides under Atlas's ridge (hesperides)

Usage: /usr/bin/python3 tools/ichor/art/farlands_scene.py [scene|all] [--pass N]
Writes design/postgame/img/farlands_<scene>.png (2x) and _1x.png; with
--pass N also design/postgame/img/passes/farlands_<scene>_pass<N>.png and a
sheet of 15 x 10 views (_views.png) for the critique.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "maps"))
sys.path.insert(0, str(HERE.parent))
import farlands_lib as F  # noqa: E402
import render_map as rm  # noqa: E402

ROOT = F.ROOT
IMG = ROOT / "design/postgame/img"
PASSES = IMG / "passes"

SYMBOL = {"steppe": "gTileset_Steppe", "steppe_town": "gTileset_SteppeTown",
          "steppe_camp": "gTileset_SteppeCamp", "far_west": "gTileset_FarWest",
          "hesperides": "gTileset_Hesperides"}


def tiles_mod():
    import importlib
    import farlands_tiles
    importlib.reload(farlands_tiles)
    return farlands_tiles


# --------------------------------------------------------------------------
# Regions
# --------------------------------------------------------------------------

def ell(cx, cy, rx, ry, wob=0.18, seed=0.0, k=5):
    out = set()
    for y in range(int(cy - ry - 3), int(cy + ry + 4)):
        for x in range(int(cx - rx - 3), int(cx + rx + 4)):
            a = math.atan2(y - cy, x - cx)
            r = 1 + wob * math.sin(a * k + seed) + 0.5 * wob * math.sin(a * (k + 3) + 2 * seed)
            if math.hypot((x - cx) / rx, (y - cy) / ry) < r:
                out.add((x, y))
    return out


def line(pts, width=2.0):
    out = set()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for i in range(n + 1):
            u = i / n
            cx, cy = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            for y in range(int(cy - width), int(cy + width) + 2):
                for x in range(int(cx - width), int(cx + width) + 2):
                    if math.hypot(x + 0.5 - cx - 0.5, y + 0.5 - cy - 0.5) <= width / 2:
                        out.add((x, y))
    return out


def rect(x0, y0, x1, y1):
    return {(x, y) for y in range(y0, y1) for x in range(x0, x1)}


# --------------------------------------------------------------------------
# The scene
# --------------------------------------------------------------------------

class Scene:
    def __init__(self, name, tileset, w, h, base=0x001):
        self.name, self.ts, self.w, self.h = name, tileset, w, h
        self.ids = np.full((h, w), base, int)
        self.T = tiles_mod()

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def fill(self, cells, mid):
        for (x, y) in cells:
            if self.inside(x, y):
                self.ids[y, x] = mid

    def soft(self, key, cells, ts=None, keep=None):
        """Lay a soft-ground region: every cell gets its shape's metatile.
        keep: a set of cells to leave alone (already placed pieces)."""
        ts = ts or self.ts
        grid = [[(x, y) in cells for x in range(self.w)] for y in range(self.h)]
        for (x, y) in cells:
            if not self.inside(x, y) or (keep and (x, y) in keep):
                continue
            self.ids[y, x] = self.T.soft(ts, key, grid, x, y)
        return grid

    def interior(self, cells):
        grid = [[(x, y) in cells for x in range(self.w)] for y in range(self.h)]
        return {(x, y) for (x, y) in cells if self.inside(x, y)
                and self.T.shape(grid, x, y) == "1|11111111"}

    def put(self, key, x, y, ts=None, skip=()):
        s = self.T.TILESETS[ts or self.ts]["structures"][key]
        for j, row in enumerate(s["ids"]):
            for i, m in enumerate(row):
                if (i, j) in skip:
                    continue
                if self.inside(x + i, y + j):
                    self.ids[y + j, x + i] = m

    def put_rows(self, key, x, y, rows, ts=None):
        """Place named pieces of `key` as rows of names (None leaves a cell)."""
        for j, row in enumerate(rows):
            for i, n in enumerate(row):
                if n is not None:
                    self.piece(key, n, x + i, y + j, ts)

    def piece(self, key, name, x, y, ts=None):
        if self.inside(x, y):
            self.ids[y, x] = self.T.mid(ts or self.ts, key, name)

    def aethos(self, mid, x, y):
        if self.inside(x, y):
            self.ids[y, x] = mid

    def render(self):
        rm.read_fieldmap_constants()
        syms = rm.scan_tileset_symbols()
        r = rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                        rm.Tileset(rm.resolve_tileset(SYMBOL[self.ts], syms)))
        img = np.zeros((self.h * 16, self.w * 16, 3), np.uint8)
        for y in range(self.h):
            for x in range(self.w):
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = r.metatile(int(self.ids[y, x]))[0]
        return Image.fromarray(img)


def views(img, path, cols=3):
    """A sheet of 15 x 10 views (240 x 160 px, shown 2x) tiled over the scene."""
    W, H = img.size
    xs = list(range(0, max(1, W - 240 + 1), 240)) or [0]
    ys = list(range(0, max(1, H - 160 + 1), 160)) or [0]
    if xs[-1] + 240 < W:
        xs.append(W - 240)
    if ys[-1] + 160 < H:
        ys.append(H - 160)
    crops = [img.crop((x, y, x + 240, y + 160)).resize((480, 320), Image.NEAREST) for y in ys for x in xs]
    rows = (len(crops) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 488 + 8, rows * 328 + 8), (40, 40, 48))
    for i, c in enumerate(crops):
        sheet.paste(c, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
    sheet.save(path)


# --------------------------------------------------------------------------
# Scenes
# --------------------------------------------------------------------------

A_WALL = {"H_L": 0x148, "H": 0x149, "H_R": 0x14A, "V_W": 0x132, "V_E": 0x133}


def scatter(sc, key, names, cells, rate, seed=0):
    """Scatter single named pieces over plain cells, now and then."""
    for (x, y) in sorted(cells):
        if not sc.inside(x, y) or sc.ids[y, x] != 0x001:
            continue
        h = (x * 73 + y * 151 + seed * 37) % 97
        if h < rate:
            sc.piece(key, names[h % len(names)], x, y)


def thrace():
    sc = Scene("thrace", "steppe", 40, 30)
    W, H = sc.w, sc.h
    # the river, meandering down the east side, a ford where the road crosses
    river = set()
    for y in range(-1, H + 1):
        cx = 31.5 + 2.6 * math.sin(y / 4.2) + (1.5 if y > 18 else 0)
        wdt = 3 if y % 9 < 6 else 4
        for x in range(int(cx - wdt / 2), int(cx + wdt / 2) + 1):
            river.add((x, y))
    river |= ell(34, 25, 3.5, 2.5, 0.2, 1.0)
    # the road: in from the west, up through the fields, across the ford
    road = line([(-1, 22), (6, 21.5), (11, 19), (15, 17.5), (21, 16.5), (26, 15.5), (30, 15),
                 (34, 15.5), (41, 14.5)], 2.2)
    road |= line([(15, 17.5), (17, 12), (19, 8), (18, 4)], 1.4)
    # golden grass: a field north-west, a forced band across the road west,
    # a field by the kurgans, the meadow over the river
    gold = ell(8, 6, 7.5, 4.2, 0.22, 0.5) | ell(13, 9, 4, 2.5, 0.2, 2.0)
    gold |= ell(5, 24, 5, 4.5, 0.18, 1.3) | ell(9, 26, 3.5, 3, 0.2, 2.2)
    gold |= ell(25, 8, 4.5, 3.5, 0.2, 3.1)
    gold |= ell(37, 6, 3.5, 4, 0.2, 0.7) | ell(23, 23, 5, 3.5, 0.2, 4.2)
    gold -= road
    gold -= river
    marsh = ell(30, 26, 3, 2.6, 0.2, 2.5) - river
    mud = (ell(36.5, 21, 2.5, 2, 0.2, 1.8) - river) - marsh
    sc.soft("steppe_grass", gold)
    # feather streaks in the big field
    for (x, y) in sorted(sc.interior(gold)):
        if (x * 3 + y * 5) % 11 in (0, 1) and y < 10:
            sc.piece("feather", "feather" if (x + y) % 2 else "feather_b", x, y)
    sc.soft("reed_marsh", marsh)
    sc.soft("mudflat", mud)
    sc.soft("road", road)
    sc.soft("river", river)
    # the ford: gravel across the river on the road's line
    for (x, y) in sorted(river & road):
        sc.piece("reeds_ford", "ford_stones" if (x + y) % 3 == 0 else "ford", x, y)
    # kurgans
    sc.put("kurgan_large", 20, 1, skip={(x, 3) for x in range(4)})
    sc.piece("kurgan_large", "summit_idol", 21, 1)
    sc.put_rows("kurgan", 26, 12, [["small_TL", "small_TR"], ["small_BL", "small_BR"]])
    sc.put_rows("kurgan", 4, 12, [["low", "low_b", "low"]])
    sc.piece("kurgan", "dig", 8, 13)
    # idols at the ford and on the field's edge
    sc.put_rows("idols", 28, 16, [["horn_top"], ["horn"]])
    sc.put_rows("idols", 15, 4, [["woman_top"], ["woman"]])
    sc.put_rows("idols", 2, 17, [["worn_top"], ["worn"]])
    # the horse field: aethos's dry-stone walls
    for x in range(9, 15):
        sc.aethos(A_WALL["H"], x, 20 + 3)
    sc.aethos(A_WALL["H_L"], 8, 23)
    sc.aethos(A_WALL["H_R"], 15, 23)
    # trees along the river: willows on the bank, a line of poplars
    for (x, y) in ((27, 3), (35, 10), (27, 20)):
        sc.put_rows("trees", x, y, [["willow_TL", "willow_TR"], ["willow_BL", "willow_BR"]])
    for (x, y) in ((37, 17), (38, 19), (39, 21)):
        sc.put_rows("trees", x, y, [["poplar_top"], ["poplar"]])
    sc.put_rows("trees", 11, 14, [["oak_TL", "oak_TR"], ["oak_BL", "oak_BR"]])
    plain = {(x, y) for y in range(H) for x in range(W)}
    scatter(sc, "decor", ["poppies", "tussock", "salvia", "turf", "tussocks", "plumes"], plain, 9, 3)
    return sc


def scythia():
    sc = Scene("scythia", "steppe", 40, 30)
    W, H = sc.w, sc.h
    # an ocean of feather-grass with a track through it
    grass = ell(9, 9, 9, 6, 0.2, 0.4) | ell(20, 13, 8, 5, 0.2, 1.9) | ell(10, 22, 7, 5, 0.2, 3.3)
    track = line([(-1, 15.5), (8, 15), (14, 17.5), (22, 20.5), (30, 19.5), (41, 21)], 1.2)
    # the heights: a plateau to the north-east
    lake = ell(33, 26, 6, 3.5, 0.15, 0.6)
    marsh = (ell(27, 25, 3.5, 2.5, 0.2, 1.1) | ell(39, 23, 2.5, 2, 0.2, 3.0)) - lake
    grass -= track
    sc.soft("steppe_grass", grass)
    for (x, y) in sc.interior(grass):
        sc.piece("feather", "feather" if (x + y) % 2 else "feather_b", x, y)
    sc.soft("road", track)
    sc.soft("reed_marsh", marsh)
    sc.soft("river", lake)
    # the heights, built from the crag kit: plateau x 26..39, y 0..9
    px0, px1, fy = 26, 39, 7
    for x in range(px0, px1 + 1):
        n = "lip_L" if x == px0 else ("lip_R" if x == px1 else "lip")
        sc.piece("heights", n, x, fy)
        n = "face_L" if x == px0 else ("face_R" if x == px1 else "face")
        if x in (29, 33):
            n = "face_gold"
        if x == 35:
            n = "face_gold_b"
        if x == 31:
            n = "mine"
        sc.piece("heights", n, x, fy + 1)
        n = "foot_L" if x == px0 else ("foot_R" if x == px1 else "foot")
        sc.piece("heights", n, x, fy + 2)
    for y in range(0, fy):
        sc.piece("heights", "side_W", px0, y)
    sc.piece("heights", "cave", 37, fy + 1)
    sc.put("fossils", 28, 11)
    sc.put("waystone", 13, 13)
    sc.put("kurgan_large", 3, 2, skip={(x, 3) for x in range(4)})
    sc.piece("kurgan_large", "door", 4, 4)
    sc.put_rows("kurgan", 19, 3, [["small_TL", "small_TR"], ["small_BL", "small_BR"]])
    sc.put_rows("idols", 22, 24, [["marker_top"], ["marker"]])
    sc.put_rows("idols", 3, 18, [["cairn_top"], ["cairn"]])
    plain = {(x, y) for y in range(H) for x in range(W)}
    scatter(sc, "decor", ["plumes", "tussock", "turf", "salvia"], plain, 10, 5)
    return sc


def surf_pieces(sc, sea, sand):
    """Put the far west's surf on every sea cell that touches sand."""
    for (x, y) in sorted(sea):
        if not sc.inside(x, y):
            continue
        s = {d: ((x + dx, y + dy) in sand) for d, (dx, dy) in
             (("N", (0, -1)), ("S", (0, 1)), ("E", (1, 0)), ("W", (-1, 0)),
              ("NE", (1, -1)), ("NW", (-1, -1)), ("SE", (1, 1)), ("SW", (-1, 1)))}
        orth = [d for d in "NSEW" if s[d]]
        piece = None
        if len(orth) >= 3 or (s["N"] and s["S"]) or (s["E"] and s["W"]):
            sc.aethos(0x124, x, y)
            continue
        if s["N"] and s["W"]:
            piece = "in_SE"
        elif s["N"] and s["E"]:
            piece = "in_SW"
        elif s["S"] and s["W"]:
            piece = "in_NE"
        elif s["S"] and s["E"]:
            piece = "in_NW"
        elif s["N"]:
            piece = "S"
        elif s["S"]:
            piece = "N"
        elif s["E"]:
            piece = "W"
        elif s["W"]:
            piece = "E"
        elif s["NW"]:
            piece = "out_NW"
        elif s["NE"]:
            piece = "out_NE"
        elif s["SW"]:
            piece = "out_SW"
        elif s["SE"]:
            piece = "out_SE"
        if piece:
            sc.piece("surf", piece, x, y)


def erytheia():
    sc = Scene("erytheia", "far_west", 40, 30)
    W, H = sc.w, sc.h
    # the sea to the south and west, sand down to it, the sunset surf
    sea = set()
    for x in range(W):
        top = 22 + int(round(1.6 * math.sin(x / 4.0) + (2 if x < 8 else 0) + (0 if x < 30 else -2)))
        for y in range(top, H):
            sea.add((x, y))
    sea |= rect(0, 14, 4, 30) | ell(2, 17, 3, 3, 0.1, 1)
    land = {(x, y) for y in range(H) for x in range(W)} - sea
    # sand: a band along the shore
    sand = set()
    for (x, y) in land:
        if any((x + dx, y + dy) in sea for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)):
            sand.add((x, y))
    sc.fill(sand, 0x124)
    sc.fill(sea, 0x170)
    # the surf on the shore cells of the sea
    surf_pieces(sc, sea, sand)
    # the sun's road on the water, breakers further out
    for y in range(H):
        for x in range(W):
            if (x, y) in sea and sc.ids[y, x] == 0x170:
                if 5 <= x <= 12 and y >= 25 and (x + y) % 3 != 0:
                    sc.piece("sea_marks", "sun_road" if (x + y) % 2 else "sun_road_b", x, y)
                elif x > 18 and y == H - 2 and x % 5 < 3:
                    sc.piece("sea_marks", "breaker" if x % 2 else "breaker_b", x, y)
    sc.put_rows("stacks", 30, 26, [["stack_TL", "stack_TR"], ["stack_BL", "stack_BR"]])
    sc.put_rows("stacks", 1, 26, [["stack_small_top"], ["stack_small"]])
    # red earth: the pasture's tracks and trodden ground
    red = ell(16, 9, 9, 5.5, 0.22, 0.3) | line([(6, 21), (11, 16), (16, 12), (24, 10), (33, 5), (41, 3)], 2.0)
    red |= ell(32, 14, 4.5, 3, 0.2, 2.0)
    red -= sea
    red_on_sand = red & sand
    red_on_grass = red - sand
    sc.soft("red_earth", red_on_grass | red_on_sand)
    grid = [[(x, y) in red for x in range(W)] for y in range(H)]
    for (x, y) in red_on_sand:
        sc.ids[y, x] = T.mid("far_west", "red_earth_sand", T.shape(grid, x, y))
    # sunset grass: bands across the track, fields on the grass, grass growing
    # out of the red earth in the pasture's heart
    dusk = (ell(9, 6, 5.5, 3.5, 0.2, 1.4) | ell(25, 20, 6, 2.5, 0.2, 0.8) | ell(36, 9, 4, 3, 0.2, 2.6)
            | ell(21, 4, 4, 2, 0.2, 3.0)) - sea - sand - red
    sc.soft("dusk_grass", dusk)
    inner = sc.interior(red) - sand
    patch = {(x, y) for (x, y) in inner if math.hypot(x - 15, (y - 9) * 1.4) < 4.2}
    gridp = [[(x, y) in patch for x in range(W)] for y in range(H)]
    for (x, y) in patch:
        sc.ids[y, x] = T.mid("far_west", "dusk_grass_red", T.shape(gridp, x, y))
    # crags to the north: Geryon's crag, the den
    for x in range(26, 36):
        n = "lip_L" if x == 26 else ("lip_R" if x == 35 else "lip")
        sc.piece("crag", n, x, 0)
        n = "face_L" if x == 26 else ("face_R" if x == 35 else ("face_lit" if x in (28, 33) else "face"))
        if x == 31:
            n = "cave"
        sc.piece("crag", n, x, 1)
        sc.piece("crag", "foot_L" if x == 26 else ("foot_R" if x == 35 else "foot"), x, 2)
    sc.put("hut", 3, 9)
    # boulders and maquis
    for (x, y, n) in ((24, 13, "boulder"), (12, 19, "boulders"), (37, 17, "boulder"), (6, 3, "boulders")):
        if sc.ids[y, x] == 0x001:
            sc.piece("rocks", n, x, y)
    plain = {(x, y) for y in range(H) for x in range(W)}
    for (x, y) in sorted(plain):
        if sc.ids[y, x] == 0x001:
            h = (x * 73 + y * 151) % 97
            if h < 9:
                sc.piece("scrub", ["lentisk", "palm", "broom", "cistus", "thistle", "lentisk_b"][h % 6], x, y)
    # the cup at its landing
    sc.put_rows("dock", 14, 24, [["cup_TL", "cup_T", "cup_TR"], ["cup_BL", "cup_B", "cup_BR"]])
    return sc


def pillars():
    sc = Scene("pillars", "far_west", 40, 30, base=0x170)
    W, H = sc.w, sc.h
    # two headlands, north and south, the strait between them running west
    north = ell(26, 2, 15, 6.5, 0.12, 0.4) | rect(14, 0, 40, 4)
    south = ell(26, 28, 15, 6, 0.12, 2.0) | rect(14, 26, 40, 30)
    for land, face_row in ((north, None), (south, None)):
        sc.fill(land, 0x001)
    T = sc.T
    # north headland: its south edge is a cliff with its foot in the sea
    for x in range(W):
        ys = [y for y in range(H) if (x, y) in north]
        if not ys:
            continue
        b = max(ys)
        if b < 2:
            continue
        sc.piece("crag", "foot_sea_L" if (x - 1, b) not in north else
                 ("foot_sea_R" if (x + 1, b) not in north else "foot_sea"), x, b + 1)
        sc.piece("crag", "face_lit" if x % 4 == 0 else "face", x, b)
        sc.piece("crag", "lip", x, b - 1)
    # south headland: its north edge is the crag's back, then grass
    for x in range(W):
        ys = [y for y in range(H) if (x, y) in south]
        if not ys:
            continue
        t = min(ys)
        sc.piece("crag", "back", x, t)
    # the pillars: west ends of the headlands
    sc.put("pillars", 22, 1, skip={(x, y) for y in range(6) for x in range(2, 6)})
    sc.put_rows("pillars", 22, 23, [[f"E{x}{y}" for x in range(2)] for y in range(6)])
    # the glow across the strait between them, the fog to the west
    for y in range(9, 19):
        for x in range(20, 27):
            if sc.ids[y, x] == 0x170:
                sc.piece("strait", "glow" if (x + y) % 2 else "glow_b", x, y)
    for y in range(H):
        for x in range(0, 9):
            if sc.ids[y, x] == 0x170:
                sc.piece("strait", "fog", x, y)
        if sc.ids[y, 9] == 0x170:
            sc.piece("strait", "fog_E", 9, y)
    sc.piece("strait", "fog_shape", 3, 13)
    sc.piece("strait", "fog_shape_b", 4, 13)
    # the second headland's fallen column, not yet raised (the set piece's start)
    sc.put_rows("pillars", 33, 23, [["fallen00", "fallen10", "fallen20", "fallen30"],
                                    ["fallen01", "fallen11", "fallen21", "fallen31"]])
    sc.put_rows("pillars", 30, 25, [["socket_L", "socket_R"]])
    for (x, y) in ((35, 2), (18, 27), (37, 26)):
        sc.piece("scrub", "lentisk", x, y)
    for x in range(30, 40, 3):
        sc.piece("sea_marks", "breaker", x, 14)
    sc.put_rows("stacks", 14, 7, [["stack_small_top"], ["stack_small"]])
    return sc


def garden():
    sc = Scene("garden", "hesperides", 40, 30)
    W, H = sc.w, sc.h
    # Atlas's ridge across the top: the low sky, the summit's snow, the crag
    for x in range(W):
        sc.piece("low_sky", "sky" if x % 2 else "sky_b", x, 0)
        sc.piece("low_sky", "rim" if x % 3 else "rim_b", x, 1)
    snow = rect(0, 2, W, 4) | ell(8, 4, 5, 1.5, 0.2, 1) | ell(31, 4, 6, 1.6, 0.2, 2)
    sc.soft("snowline", snow)
    for x in range(W):
        sc.piece("crag", "lip" if 0 < x < W - 1 else ("lip_L" if x == 0 else "lip_R"), x, 5)
        sc.piece("crag", "face" if x % 5 else "face_ice", x, 6)
        sc.piece("crag", "foot", x, 7)
    sc.piece("crag", "cave", 33, 6)
    # the garden: a walled lawn, the tree on its rise, Ladon round its foot
    for x in range(3, 37):
        n = "H" if x not in (19, 20) else None
        if x == 3:
            n = "H_L"
        if x == 36:
            n = "H_R"
        if x in (11, 27):
            n = "H_roses"
        if x == 18:
            n = "gate_L"
        if x == 21:
            n = "gate_R"
        if n:
            sc.piece("walls", n, x, 27)
    for y in range(10, 27):
        sc.piece("walls", "V" if y % 4 else "V_ivy", 3, y)
        sc.piece("walls", "V" if y % 4 else "V_ivy", 36, y)
    sc.piece("walls", "NW", 3, 9)
    sc.piece("walls", "NE", 36, 9)
    for x in range(4, 36):
        sc.piece("walls", "H", x, 9)
    sc.aethos(0x1D9, 19, 27)
    sc.aethos(0x1D9, 20, 27)
    # paths: aethos limestone
    for y in range(20, 30):
        for x in (19, 20):
            if sc.ids[y, x] == 0x001:
                sc.aethos(0x1D9, x, y)
    sc.put("apple_tree", 18, 12)
    sc.put_rows("ladon", 17, 14, [["W_top"], ["W"]])
    sc.put_rows("ladon", 22, 14, [["E_top"], ["E"]])
    sc.put_rows("ladon", 17, 16, [["head", "coil", "loop", "coil_b", "loop_b", "tail"]])
    sc.put("fountain", 9, 21)
    sc.put("bower", 5, 11)
    sc.put("bower", 31, 11)
    sc.put("bower", 30, 20)
    sc.put_rows("fountain", 27, 17, [["spring_TL", "spring_TR"], ["spring_BL", "spring_BR"]])
    grass = (ell(10, 17, 4.5, 2.2, 0.2, 1.0) | ell(28, 24, 3, 1.5, 0.2, 2.0) | ell(24, 21, 3, 1.8, 0.2, 2.7))
    grass = {c for c in grass if sc.ids[c[1], c[0]] == 0x001} if all(sc.inside(*c) for c in grass) else \
        {c for c in grass if sc.inside(*c) and sc.ids[c[1], c[0]] == 0x001}
    sc.soft("garden_grass", grass)
    for (x, y) in ((12, 13), (8, 18), (14, 24), (25, 12), (16, 21), (23, 24), (6, 25), (33, 16)):
        if sc.ids[y, x] == 0x001:
            sc.piece("decor", ["lilies", "asphodel", "petals", "windfalls"][(x + y) % 4], x, y)
    for x in range(5, 17):
        if sc.ids[19, x] == 0x001:
            sc.piece("decor", "myrtle" if 5 < x < 16 else ("myrtle_L" if x == 5 else "myrtle_R"), x, 19)
    for (x, y) in ((15, 11), (25, 18), (6, 15), (33, 25)):
        if sc.ids[y, x] == 0x001:
            sc.piece("decor", "roses", x, y)
    # outside the wall: cold scrub on the slope under the crag
    for (x, y) in ((1, 9), (38, 10), (0, 14), (39, 20), (1, 24)):
        sc.piece("cold", "cold_scrub" if (x + y) % 2 else "cold_scrub_b", x, y)
    return sc


def diomedes():
    sc = Scene("diomedes", "steppe_camp", 40, 30)
    W, H = sc.w, sc.h
    # the shore to the south
    for x in range(W):
        top = 26 + int(round(1.2 * math.sin(x / 3.5)))
        for y in range(top, H):
            sc.aethos(0x170, x, y)
        sc.aethos(0x124, x, top - 1)
        sc.aethos(0x124, x, top - 2)
    # the yard: a palisade round the stable
    x0, x1, y0, y1 = 4, 30, 3, 21
    for x in range(x0 + 1, x1):
        if x in (16, 17):
            continue
        sc.piece("palisade", "top", x, y0)
        sc.piece("palisade", "base", x, y0 + 1)
        if x not in (16, 17, 18):
            sc.piece("palisade", "top", x, y1 - 1)
            sc.piece("palisade", "base", x, y1)
    for y in range(y0 + 2, y1):
        sc.piece("palisade", "V", x0, y)
        sc.piece("palisade", "V", x1, y)
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1 - 1), (x1, y1 - 1)):
        sc.piece("palisade", "tower_top", x, y)
        sc.piece("palisade", "tower", x, y + 1)
    sc.put("gate", 16, y1 - 2)
    sc.put("stable", 8, 6)
    road = line([(17.5, 21), (17.5, 25)], 2.0) | line([(17.5, 12), (17.5, 19)], 2.0) | ell(17, 15, 6, 3, 0.2, 1.0)
    sc.soft("road", road, keep={(x, y) for y in range(H) for x in range(W) if sc.ids[y, x] != 0x001})
    # the horse field with its fence, a trough, hay
    fx0, fx1, fy0, fy1 = 32, 38, 4, 12
    for x in range(fx0 + 1, fx1):
        sc.piece("fence", "H" if x != 35 else "gate", x, fy0)
        sc.piece("fence", "H", x, fy1)
    for y in range(fy0 + 1, fy1):
        sc.piece("fence", "V", fx0, y)
        sc.piece("fence", "V", fx1, y)
    sc.piece("fence", "NW", fx0, fy0)
    sc.piece("fence", "NE", fx1, fy0)
    sc.piece("fence", "SW", fx0, fy1)
    sc.piece("fence", "SE", fx1, fy1)
    sc.put_rows("troughs", 34, 9, [["trough_L", "trough_R", "hay"]])
    sc.put_rows("yard", 23, 13, [["horse_TL", "horse_TR"], ["horse_BL", "horse_BR"]])
    sc.piece("yard", "hearth", 10, 16)
    sc.piece("yard", "cauldron", 25, 8)
    plain = {(x, y) for y in range(H) for x in range(W)}
    scatter(sc, "decor", ["tussock", "turf", "poppies"], plain, 7, 2)
    return sc


def themiskyra():
    sc = Scene("themiskyra", "steppe_camp", 40, 30)
    W, H = sc.w, sc.h
    river = set()
    for y in range(-1, H + 1):
        cx = 35.5 + 1.8 * math.sin(y / 3.6)
        for x in range(int(cx - 2), int(cx + 2) + 1):
            river.add((x, y))
    sc.soft("river", river)
    # the palisade, the gate on the road from the river
    x0, x1, y0, y1 = 1, 29, 1, 25
    for x in range(x0 + 1, x1):
        sc.piece("palisade", "top", x, y0)
        sc.piece("palisade", "base", x, y0 + 1)
    for y in range(y0 + 2, y1 + 1):
        sc.piece("palisade", "V", x0, y)
        if not (14 <= y <= 16):
            sc.piece("palisade", "V", x1, y)
    for (x, y) in ((x0, y0), (x1, y0)):
        sc.piece("palisade", "tower_top", x, y)
        sc.piece("palisade", "tower", x, y + 1)
    for x in range(x0 + 1, x1):
        sc.piece("palisade", "top", x, y1 - 1)
        sc.piece("palisade", "base", x, y1)
    for (x, y) in ((x0, y1 - 1), (x1, y1 - 1)):
        sc.piece("palisade", "tower_top", x, y)
        sc.piece("palisade", "tower", x, y + 1)
    sc.put("gate", 12, y1 - 2)
    for x in (13, 14):
        sc.aethos(0x001, x, y1 + 1)
    # inside: the hall, tents, the practice ground, hearths
    sc.put("hall", 17, 4)
    sc.put_rows("tents", 4, 4, [[f"red{x}{y}" for x in range(3)] for y in range(3)])
    sc.put_rows("tents", 9, 4, [[f"red{x}{y}" for x in range(3)] for y in range(3)])
    sc.piece("tents", "agora_door", 10, 6)
    sc.put_rows("tents", 4, 15, [[f"cream{x}{y}" for x in range(3)] for y in range(3)])
    sc.piece("tents", "ascl_door", 5, 17)
    sc.put_rows("tents", 23, 15, [[f"cream{x}{y}" for x in range(3)] for y in range(3)])
    yard_ = ell(17, 15, 5.5, 3.2, 0.2, 1.4)
    road = line([(13.5, 23), (14, 18), (17, 12), (19, 9)], 2.0) | line([(14, 26), (14, 31)], 2.0)
    road |= line([(29, 15.5), (33, 15.5)], 2.0)
    occupied = {(x, y) for y in range(H) for x in range(W) if sc.ids[y, x] != 0x001} - river
    sc.soft("road", (road | yard_) - river, keep=occupied)
    for (x, y) in ((14, 13), (18, 13), (21, 14)):
        sc.put_rows("yard", x, y, [["target_top"], ["target"]])
    sc.put_rows("yard", 15, 16, [["rack_L", "rack_R"]])
    sc.piece("yard", "post", 20, 17)
    sc.put_rows("yard", 11, 12, [["standard_top"], ["standard"]])
    sc.piece("yard", "hearth", 8, 10)
    sc.piece("yard", "cauldron", 20, 10)
    sc.piece("yard", "well", 9, 20)
    sc.piece("yard", "shields", 25, 10)
    # the horse field across the river road
    sc.put_rows("yard", 31, 3, [["horse_TL", "horse_TR"], ["horse_BL", "horse_BR"]])
    for x in range(30, 34):
        sc.piece("fence", "H", x, 6)
    sc.piece("fence", "H_L", 30, 6)
    sc.put_rows("troughs", 31, 8, [["trough_L", "trough_R"]])
    plain = {(x, y) for y in range(H) for x in range(W)}
    scatter(sc, "decor", ["tussock", "turf", "poppies", "salvia"], plain, 6, 4)
    return sc


def abdera():
    sc = Scene("abdera", "steppe_town", 40, 30)
    W, H = sc.w, sc.h
    T = sc.T
    # the harbor: sea to the south, the quay along it
    for y in range(22, H):
        for x in range(W):
            sc.aethos(0x170, x, y)
    for x in range(4, 36):
        sc.piece("quay", "deck", x, 20)
        sc.piece("quay", "edge_S" if x not in (12,) else "gangplank", x, 21)
    sc.piece("quay", "corner_SW", 3, 21)
    sc.piece("quay", "corner_SE", 36, 21)
    sc.piece("quay", "edge_W", 3, 20)
    sc.piece("quay", "edge_E", 36, 20)
    for x in (8, 18, 28):
        sc.piece("quay", "post", x, 20)
    sc.piece("quay", "nets", 31, 20)
    sc.put_rows("quay", 20, 23, [["boat_L", "boat_R"]])
    # the limestone street (aethos) along the harbor, the road inland
    for x in range(0, W):
        for y in (18, 19):
            sc.aethos(0x1D9, x, y)
    for x in range(0, W):
        sc.aethos(0x1D1, x, 17)
        if sc.ids[20, x] == 0x001:
            sc.aethos(0x1E1, x, 20)
    road = line([(20, 17), (20, 11), (24, 6), (28, 2), (30, -1)], 2.0)
    sc.soft("road", road)
    # houses along the street
    fronts = T.TILESETS["steppe_town"].get("fronts", {})

    def front(name, x, y):
        rows = __import__("farlands_steppe_town").FRONTS[name]
        sc.put_rows("house", x, y, rows)
    front("brick_house", 1, 14)
    front("long_house", 5, 14)
    front("timber_house", 26, 14)
    front("cottage", 30, 14)
    front("wide_house", 1, 4)
    # the Asclepeion and the Agora
    sc.put_rows("house", 10, 14, [["tile_A_L", "tile_A_M", None, "tile_A_M", "tile_A_R"],
                                  ["tile_B_L", "tile_B_M", "tile_B_M", "tile_B_M", "tile_B_R"],
                                  ["brick_L", None, None, None, "brick_R"]])
    sc.piece("civic", "ascl_ped", 12, 14)
    sc.piece("civic", "ascl_col", 11, 16)
    sc.piece("civic", "ascl_door", 12, 16)
    sc.piece("civic", "ascl_col", 13, 16)
    sc.put_rows("house", 21, 14, [["thatch_A_L", "thatch_A_M", None, "thatch_A_M", "thatch_A_R"],
                                  ["thatch_B_L", "thatch_B_M", "thatch_B_M", "thatch_B_M", "thatch_B_R"],
                                  ["timber_L", None, None, None, "timber_R"]])
    sc.piece("civic", "agora_ped", 23, 14)
    sc.piece("civic", "agora_awning", 22, 16)
    sc.piece("civic", "agora_door", 23, 16)
    sc.piece("civic", "agora_awning", 24, 16)
    sc.put("temple", 9, 3)
    sc.put("market", 31, 5)
    for x in range(31, 37):
        pass
    sc.put_rows("market", 27, 8, [["cart_L", "cart_R"]])
    # the horse market
    px0, px1, py0, py1 = 30, 38, 9, 12
    for x in range(px0 + 1, px1):
        sc.piece("pen", "H" if x != 34 else "gate", x, py0)
        sc.piece("pen", "H", x, py1)
    for y in range(py0 + 1, py1):
        sc.piece("pen", "V", px0, y)
        sc.piece("pen", "V", px1, y)
    sc.piece("pen", "NW", px0, py0)
    sc.piece("pen", "NE", px1, py0)
    sc.piece("pen", "SW", px0, py1)
    sc.piece("pen", "SE", px1, py1)
    return sc


SCENES = {"thrace": thrace, "diomedes": diomedes, "themiskyra": themiskyra, "abdera": abdera,
          "scythia": scythia, "erytheia": erytheia, "pillars": pillars, "garden": garden}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene", nargs="?", default="all")
    ap.add_argument("--pass", dest="pass_", type=int, default=0)
    args = ap.parse_args()
    names = list(SCENES) if args.scene == "all" else [args.scene]
    IMG.mkdir(parents=True, exist_ok=True)
    for n in names:
        sc = SCENES[n]()
        img = sc.render()
        img.save(IMG / f"farlands_{n}_1x.png")
        img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(IMG / f"farlands_{n}.png")
        if args.pass_:
            PASSES.mkdir(parents=True, exist_ok=True)
            img.save(PASSES / f"farlands_{n}_pass{args.pass_}.png")
            views(img, PASSES / f"farlands_{n}_pass{args.pass_}_views.png")
        print(f"design/postgame/img/farlands_{n}.png")


if __name__ == "__main__":
    main()
