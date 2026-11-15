#!/usr/bin/env python3
"""Build Lebadeia and Route 9, the Split Road (design/phase3/SCRIPT.md beats 35B-36).

Each map is drawn below in code: a ground grid carved out of rock (the legend is
PMap's), stamped with gTileset_Parnassos's structures, then auto-tiled from
build/parnassos/catalog.json (tools/ichor/art/parnassos_build.py). It writes:

  data/layouts/<Map>/{map,border}.bin and the layouts' entries in layouts.json
  data/maps/<Map>/map.json: events, connections and music
  build/render/parnassos/<Map>.png, _review.png (collision and events) and
  _screens.png (15 x 10 GBA screens along the road)
  design/phase3/img/<Map>.png (2x), for the director

Usage:
  /usr/bin/python3 tools/ichor/maps/parnassos.py            # build both maps
  /usr/bin/python3 tools/ichor/maps/parnassos.py --shapes   # list the soft-ground
      shapes the maps use in tools/ichor/art/parnassos_shapes.json; then rebuild the
      tileset (tools/ichor/art/parnassos_build.py) and run this again
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_lib as L  # noqa: E402
from kithairon_lib import ROOT, item_ball, obj, sign, trigger, warp  # noqa: E402

# This builder's own tileset and catalog (kithairon_lib reads both from these).
L.CAT = ROOT / "build"
L.SETS["parnassos"] = ("gTileset_Parnassos", "parnassos")
L.RENDER = ROOT / "build/render/parnassos"
SHAPES = ROOT / "tools/ichor/art/parnassos_shapes.json"
SHAPE_SETS = ("tall", "path", "crag", "water", "pave", "gully")

IMG = ROOT / "design/phase3/img"
P = "OBJ_EVENT_GFX_ICHOR_"
LB = "Lebadeia_EventScript_"
R9 = "Route9_Schiste_EventScript_"
ROAD_MUSIC = "MUS_ICHOR_ROAD"    # SCRIPT.md Part 9: the road (630) for Lebadeia and Route 9

GRASS, TALL, SHADE = L.GRASS, L.TALL, L.SHADE
STELE, ANEMONE = 0x003, 0x004
OLIVE_TIP, OLIVE_TIP_TALL = (0x1CE, 0x1CF), (0x1C6, 0x1C7)
OLIVE_TOP, OLIVE_BOT, OLIVE_BOT_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1DC, 0x1DD)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
TILLED = {"TL": 0x103, "T": 0x104, "TR": 0x105, "L": 0x10B, "C": 0x10C, "R": 0x10D,
          "BL": 0x113, "B": 0x114, "BR": 0x115}

# Seams (design/phase3/BUILD.md, batch 2).
LEB_ROAD = 12          # Lebadeia's road: rows 12-13 on both its edges (verges 11, 14)
R9_EAST = 20           # Route 9's road meets its east edge on rows 20-21 (verges 19, 22)
R9_SOUTH = 9           # Route 9's road leaves its south edge at columns 9-10 (verges 8, 11)
KIRRHA_NORTH = 27      # ... Kirrha's at 27-28 (verges 26, 29): offset 9 - 27 = -18


class PMap(L.Map):
    """A map on gTileset_Parnassos. Ground characters:

      .  grass (aethos)         ,  tall grass (soft edges)     =  road (soft edges)
      #  crag (pale limestone, with a south face)              ~  the river (soft banks)
      p  paving (polygonal flags)                              g  a gully
      L  laurel woods           O  olive woods (aethos's olives, for seam strips)
      w  dry-stone wall (aethos) _  terrace ledge, jump south (aethos)
      T  a tilled garden (aethos)  s  scree (walkable)        b  a boulder
      @  under a stamp (set in code)

    Seam strips: `aethos_rows` and `aethos_cols` may use only aethos metatiles.
    """

    def __init__(self, name, w, h):
        super().__init__(name, w, h, "parnassos")
        self.aethos_cols = set()
        self.water_extra, self.gully_extra = set(), set()
        self.shapes_used = {k: set() for k in SHAPE_SETS}

    def seam(self, x, y):
        return y in self.aethos_rows or x in self.aethos_cols

    def open_grass(self, x, y):
        return (0 <= x < self.w and 0 <= y < self.h and self.ch[y][x] == "."
                and (x, y) not in self.stamped and self.mt[y][x] in (None, GRASS))

    def autotile(self):
        ch = self.ch
        tall = self.region(",")
        road = self.region("=p")
        pave = self.region("p=")
        crag = self.region("#")
        water = self.region("~", self.water_extra)
        gully = self.region("g", self.gully_extra)
        till = self.region("T")
        for y in range(self.h):
            for x in range(self.w):
                if self.mt[y][x] is not None:
                    continue
                c = ch[y][x]
                aeth = self.seam(x, y)
                if c in ".@":
                    self.set(x, y, GRASS, ".")
                elif c == ",":
                    if aeth:
                        self.set(x, y, TALL, "G")
                    else:
                        self.set(x, y, *self.shape("tall", L.blob_key(tall, x, y), x, y))
                elif c == "=":
                    if aeth:
                        self.set(x, y, self.patch(self.region("="), x, y), ".")
                    else:
                        self.set(x, y, *self.shape("path", L.blob_key(road, x, y), x, y))
                elif c == "p":
                    assert not aeth, (self.name, x, y, "paving in a seam strip")
                    self.set(x, y, *self.shape("pave", L.blob_key(pave, x, y), x, y))
                elif c == "#":
                    assert not aeth, (self.name, x, y, "crag in a seam strip")
                    k = L.blob_key(crag, x, y)
                    if k == "1|11111111" and L.hsh(x, y, self.seed) < 22:
                        name = ("crack", "juniper")[L.hsh(x, y, 5) % 2]
                        self.set(x, y, *self.cat.named("crag_detail", name))
                        self.shapes_used["crag"].add(k)
                    else:
                        self.set(x, y, *self.shape("crag", k, x, y))
                elif c == "~":
                    assert not aeth
                    self.set(x, y, *self.shape("water", L.blob_key(water, x, y), x, y))
                elif c == "g":
                    assert not aeth
                    self.set(x, y, *self.shape("gully", L.blob_key(gully, x, y), x, y))
                elif c == "w":
                    ns = (y > 0 and ch[y - 1][x] == "w") or (y + 1 < self.h and ch[y + 1][x] == "w")
                    we = x > 0 and ch[y][x - 1] == "w"
                    ea = x + 1 < self.w and ch[y][x + 1] == "w"
                    if ns and not (we or ea):
                        mid = L.WALL_NS
                    elif we and ea:
                        mid = L.WALL_EW
                    elif ea:
                        mid = L.WALL_W
                    elif we:
                        mid = L.WALL_E
                    else:
                        mid = L.WALL_EW
                    self.set(x, y, mid, "X")
                elif c == "_":
                    lft = x > 0 and ch[y][x - 1] == "_"
                    rgt = x + 1 < self.w and ch[y][x + 1] == "_"
                    mid = L.LEDGE if (lft and rgt) else (L.LEDGE_L if rgt else (L.LEDGE_R if lft else L.LEDGE))
                    self.set(x, y, mid, "J")
                elif c == "T":
                    self.set(x, y, self.tilled(till, x, y), ".")
                elif c == "s":
                    assert not aeth
                    self.set(x, y, *self.cat.named("markers", "scree"))
                elif c == "b":
                    if aeth:
                        self.set(x, y, 0x0E0, "X")
                    else:
                        self.set(x, y, *self.cat.named("markers", "boulder"))
                elif c in "LO":
                    pass
                else:
                    raise ValueError(f"{self.name}: unknown ground {c!r} at {x},{y}")
        self.laurels()
        self.olives()
        self.decorate()

    def tilled(self, inside, x, y):
        n, s_, w_, e = inside(x, y - 1), inside(x, y + 1), inside(x - 1, y), inside(x + 1, y)
        v = "T" if not n else ("B" if not s_ else "")
        hz = "L" if not w_ else ("R" if not e else "")
        return TILLED.get(v + hz or "C", TILLED["C"])

    # --- woods ---------------------------------------------------------------
    def _runs(self, ch, x):
        """Vertical runs of `ch` in the column pair (x, x+1)."""
        both = lambda y: self.ch[y][x] == ch and x + 1 < self.w and self.ch[y][x + 1] == ch \
            and self.mt[y][x] is None and self.mt[y][x + 1] is None
        y = 0
        while y < self.h:
            if not both(y):
                y += 1
                continue
            y0 = y
            while y < self.h and both(y):
                y += 1
            yield y0, y - 1

    def laurels(self):
        """Fill 'L' with laurel woods: column pairs of bay laurels, mixed with
        pairs of aethos's olives and cypresses so the woods aren't one tree in ranks."""
        cat = self.cat
        for x in range(0, self.w - 1, 2):
            for (y0, y1) in self._runs("L", x):
                for yy in range(y0, y1 + 1):
                    self.force_block |= {(x, yy), (x + 1, yy)}
                n = y1 - y0 + 1
                if n == 1:
                    self.set(x, y0, *cat.named("scrub", "oak"))
                    self.set(x + 1, y0, *cat.named("scrub", "laurel"))
                    continue
                if n == 2:
                    for xx in (x, x + 1):
                        k = L.hsh(xx, y0, self.seed + 11) % 3
                        if k == 0:
                            self.set(xx, y0, *cat.cell("laurel_young", 0, 0))
                            self.set(xx, y0 + 1, *cat.cell("laurel_young", 0, 1))
                        elif k == 1:
                            self.set(xx, y0, CYPRESS_TOP, "X")
                            self.set(xx, y0 + 1, CYPRESS_BOT, "X")
                        else:
                            self.set(xx, y0, *cat.named("scrub", "laurel"))
                            self.set(xx, y0 + 1, *cat.named("scrub", "oak"))
                    continue
                pick = L.hsh(x // 2, y0, self.seed + 3)
                if pick < 26:
                    self._olive_run(x, y0, y1, stagger=(x // 2) % 2 == 1)
                    continue
                if pick < 36:
                    for xx in (x, x + 1):
                        self._cypress_run(xx, y0, y1, offset=(xx % 2))
                    continue
                above = all(self.open_grass(xx, y0 - 1) and not self.seam(xx, y0 - 1) for xx in (x, x + 1))
                t = y0 - 1 if above else y0
                # stagger every other pair a row lower, so the woods don't stand in ranks
                if (x // 2) % 2 == 1 and t == y0 - 1 and n >= 4:
                    t = y0
                end = y1
                if (end - t) % 2 == 1:          # crown + (stack, crown)* + base: an even count below the top
                    self.set(x, end, *cat.named("scrub", "laurel"))
                    self.set(x + 1, end, *cat.named("scrub", "oak"))
                    end -= 1
                for yy in range(y0, t):
                    self.set(x, yy, *cat.named("scrub", "oak"))
                    self.set(x + 1, yy, *cat.named("scrub", "laurel"))
                for i, xx in enumerate((x, x + 1)):
                    self.set(xx, t, *cat.cell("laurel", i, 0))
                r = t + 1
                while r <= end:
                    for i, xx in enumerate((x, x + 1)):
                        if r == end:
                            self.set(xx, r, *cat.cell("laurel", i, 2))
                        elif (r - t) % 2 == 1:
                            self.set(xx, r, *cat.cell("laurel", i, 1))
                        else:
                            self.set(xx, r, *cat.cell("laurel_stack", i, 0))
                    r += 1
        # single columns left over: young laurels, cypresses and bushes
        for y in range(self.h):
            for x in range(self.w):
                if self.ch[y][x] != "L" or self.mt[y][x] is not None:
                    continue
                self.force_block.add((x, y))
                if y + 1 < self.h and self.ch[y + 1][x] == "L" and self.mt[y + 1][x] is None:
                    if L.hsh(x, y, 7) % 2:
                        self.set(x, y, *self.cat.cell("laurel_young", 0, 0))
                        self.set(x, y + 1, *self.cat.cell("laurel_young", 0, 1))
                    else:
                        self.set(x, y, CYPRESS_TOP, "X")
                        self.set(x, y + 1, CYPRESS_BOT, "X")
                    self.force_block.add((x, y + 1))
                else:
                    self.set(x, y, *self.cat.named("scrub", ("oak", "laurel")[L.hsh(x, y) % 2]))

    def _cypress_run(self, x, y0, y1, offset=0):
        y = y0
        if offset and y1 - y0 >= 2:
            self.set(x, y, *self.cat.named("scrub", "laurel"))
            y += 1
        while y + 1 <= y1:
            self.set(x, y, CYPRESS_TOP, "X")
            self.set(x, y + 1, CYPRESS_BOT, "X")
            y += 2
        if y == y1:
            self.filler(x, y)

    def _olive_run(self, x, y0, y1, stagger=False):
        """A column pair of aethos's olives: top, bottom-with-tip, top, ... bottom."""
        n = y1 - y0 + 1
        start = y0
        stagger = n % 2 == 1 and n >= 3
        if stagger:
            self.set(x, y0, OLIVE_TIP[0], "X"); self.set(x + 1, y0, OLIVE_TIP[1], "X")
            start = y0 + 1
        elif all(self.open_grass(xx, y0 - 1) for xx in (x, x + 1)):
            self.put(x, y0 - 1, OLIVE_TIP[0], "T"); self.put(x + 1, y0 - 1, OLIVE_TIP[1], "T")
        elif all(0 <= y0 - 1 and self.ch[y0 - 1][xx] == "," and self.mt[y0 - 1][xx] in (None, TALL)
                 and self.seam(xx, y0 - 1) for xx in (x, x + 1)):
            self.put(x, y0 - 1, OLIVE_TIP_TALL[0], "T"); self.put(x + 1, y0 - 1, OLIVE_TIP_TALL[1], "T")
        end = y1
        if (end - start + 1) % 2:
            for xx in (x, x + 1):
                self.filler(xx, end)
            end -= 1
        for yy in range(start, end + 1, 2):
            last = yy + 2 > end
            self.set(x, yy, OLIVE_TOP[0], "X"); self.set(x + 1, yy, OLIVE_TOP[1], "X")
            bot = OLIVE_BOT if last else OLIVE_BOT_TIP
            self.set(x, yy + 1, bot[0], "X"); self.set(x + 1, yy + 1, bot[1], "X")

    def olives(self):
        for x in range(0, self.w - 1, 2):
            for (y0, y1) in self._runs("O", x):
                for yy in range(y0, y1 + 1):
                    self.force_block |= {(x, yy), (x + 1, yy)}
                self._olive_run(x, y0, y1, stagger=(x // 2) % 2 == 1)
        for y in range(self.h):
            for x in range(self.w):
                if self.ch[y][x] != "O" or self.mt[y][x] is not None:
                    continue
                self.force_block.add((x, y))
                if y + 1 < self.h and self.ch[y + 1][x] == "O" and self.mt[y + 1][x] is None:
                    self.set(x, y, CYPRESS_TOP, "X")
                    self.set(x, y + 1, CYPRESS_BOT, "X")
                    self.force_block.add((x, y + 1))
                else:
                    self.filler(x, y)

    def filler(self, x, y):
        """One leftover cell in a wood: a bush, or (in a seam strip) a boulder."""
        if self.seam(x, y):
            self.set(x, y, 0x0E0, "X")
        else:
            self.set(x, y, *self.cat.named("scrub", ("oak", "laurel")[L.hsh(x, y, 9) % 2]))

    def decorate(self, rate=6):
        for y in range(self.h):
            for x in range(self.w):
                if self.mt[y][x] != GRASS or (x, y) in self.stamped or self.ch[y][x] != ".":
                    continue
                if (x, y) in self.no_decor or L.hsh(x, y, self.seed + 17) >= rate:
                    continue
                if self.seam(x, y):
                    self.set(x, y, ANEMONE, ".")
                    continue
                pick = L.hsh(x, y, 23) % 3
                if pick == 2:
                    self.set(x, y, ANEMONE, ".")
                else:
                    self.set(x, y, *self.cat.named("meadow", ("broom", "white")[pick]))

    # --- trees and stamps ----------------------------------------------------
    def laurel(self, x, y):
        """A bay laurel: (x, y) its crown's top-left (the walk-behind row)."""
        self.stamp("laurel", x, y)

    def plane(self, x, y):
        self.stamp("plane", x, y)

    def wild_olive(self, x, y):
        self.stamp("wild_olive", x, y)

    def olive(self, x, y):
        """An aethos olive, its crown tip poking into the row above."""
        if self.open_grass(x, y - 1) and self.open_grass(x + 1, y - 1):
            self.put(x, y - 1, OLIVE_TIP[0], "T")
            self.put(x + 1, y - 1, OLIVE_TIP[1], "T")
        self.put(x, y, OLIVE_TOP[0]); self.put(x + 1, y, OLIVE_TOP[1])
        self.put(x, y + 1, OLIVE_BOT[0]); self.put(x + 1, y + 1, OLIVE_BOT[1])

    def house(self, x, y, w, door_dx, windows=(), door="plank"):
        """An Eleusa-kit house front, w wide, its roof's top-left at (x, y)."""
        for i in range(w):
            side = "L" if i == 0 else ("R" if i == w - 1 else "M")
            self.named("roof_tile", f"R0_{side}", x + i, y)
            self.named("roof_tile", f"R1_{side}", x + i, y + 1)
            self.named("wall", f"W0_{side}", x + i, y + 2)
            self.named("wall", f"W1_{side}", x + i, y + 3)
        for dx, kind in windows:
            self.named("windows", kind, x + dx, y + 2)
        self.named("doors", door, x + door_dx, y + 3)
        return (x + door_dx, y + 3)

    def check_seams(self):
        errs = []
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                if self.seam(x, y) and m >= 0x200:
                    errs.append(f"{self.name} ({x},{y}): 0x{m:03X} in an aethos-only seam cell")
        return errs


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
            "quantity": 1, "underfoot": False}


def crag_border(cat):
    return [cat.named("crag", "1|11111111")[0]] * 4


# ===========================================================================
# Lebadeia (32 x 28): between the two springs (beat 35B)
# ===========================================================================

def lebadeia():
    m = PMap("Lebadeia", 32, 28)
    m.aethos_cols = set(range(24, 32))       # Route 8's seam (east): aethos only
    W, H = 32, 28
    # The gorge: the oracle's rock over the precinct, woods on the gorge's sides,
    # the road across the middle (rows 12-13), and the Herkyna winding down from
    # the springs to the south edge. Everything starts as woods.
    m.rect(0, 0, W - 1, H - 1, "L")
    m.rect(0, 0, 9, 2, "#")                  # the oracle's rock (face on row 2)
    m.rect(0, 3, 0, 6, "#")
    m.rect(10, 0, 11, 2, "#")
    m.rect(12, 3, 23, 4, "#")                # the band behind the hall (face on row 4)
    m.rect(12, 2, 13, 2, "#")
    # the precinct under the rock face, its steps on row 6
    m.rect(1, 3, 9, 5, "p")
    m.rect(1, 6, 9, 6, ".")                  # the steps (stamped)
    # the grove below the steps, down to the road
    m.rect(0, 7, 9, 11, ".")
    m.rect(0, 11, 23, 14, ".")
    m.rect(0, 12, W - 1, 13, "=")
    # east of the river: the pilgrims' hall under the band
    m.rect(12, 5, 23, 11, ".")
    # south of the road: Herkyna's house (west), the mason's house (east)
    m.rect(1, 14, 9, 21, ".")
    m.rect(12, 14, 23, 21, ".")
    # the Herkyna: from Mnemosyne's notch, winding to the south edge
    for (x, y0, y1) in ((10, 3, 9), (11, 10, 17), (10, 18, 21), (11, 22, H - 1)):
        m.rect(x, y0, x + 1, y1, "~")
    m.cells([(13, 22), (13, 23), (10, 24), (13, 25)], ".")
    # the east seam: aethos olives on the slopes, grass verges by the road
    m.rect(24, 0, W - 1, 10, "O")
    m.rect(24, 11, W - 1, 11, ".")
    m.rect(24, 14, W - 1, 14, ".")
    m.rect(24, 15, W - 1, H - 1, "O")
    m.rect(24, 5, 25, 10, ".")               # the slope opens behind the hall
    m.rect(0, 0, 9, 0, "L")                  # scrub on the oracle's rock
    # paths: from the steps down through the grove to the road; to the doors
    m.rect(3, 7, 4, 11, "=")
    m.rect(17, 10, 17, 11, "=")
    m.rect(21, 14, 21, 20, "=")
    m.rect(12, 20, 21, 20, "=")
    m.rect(5, 19, 9, 19, "=")
    # gardens
    m.rect(1, 20, 4, 21, "T")
    m.rect(1, 19, 4, 19, "w")
    m.rect(14, 18, 15, 19, "T")
    m.rect(13, 17, 15, 17, "w")

    # --- stamps ---------------------------------------------------------------
    # the rock face over the precinct: plain face cells, the grille, the spout, tablets
    for x in range(1, 10):
        m.named("face", "plain", x, 2)
    m.named("face", "tablets", 2, 2)
    m.named("face", "grille", 6, 2)
    m.named("face", "spout", 8, 2)
    m.named("face", "tablets", 4, 2)
    # the springs and the chair between them
    m.stamp("lethe", 3, 3)
    m.stamp("mnemosyne", 8, 3)
    m.named("pmarkers", "chair", 6, 3)
    m.water_extra |= {(8, 3), (9, 3), (8, 4), (9, 4)}
    # the pilgrims' steps
    m.named("steps", "L", 1, 6)
    for x in range(2, 9):
        m.named("steps", "M", x, 6)
    m.named("steps", "R", 9, 6)
    # the plane grove, and planes along the river
    m.plane(0, 8)
    m.plane(5, 7)
    m.plane(6, 15)
    m.plane(13, 14)
    # bridges over the Herkyna: the road's (rows 12-13), the footbridge (row 19)
    m.named("bridge", "N_L", 11, 12); m.named("bridge", "N_R", 12, 12)
    m.named("bridge", "S_L", 11, 13); m.named("bridge", "S_R", 12, 13)
    m.named("bridge", "F_L", 10, 19); m.named("bridge", "F_R", 11, 19)
    m.water_extra |= {(11, 12), (12, 12), (11, 13), (12, 13), (10, 19), (11, 19)}
    # the pilgrims' hall (warp 0), Herkyna's house (warp 1), the mason's (warp 2)
    hall = m.house(14, 6, 7, 3, windows=((1, "lattice"), (5, "lattice")), door="curtain")
    herk = m.house(1, 15, 5, 4, windows=((1, "shutters"),))
    mason = m.house(16, 16, 5, 2, windows=((4, "shutters"),))
    # the mason's yard: stones he's dressing
    m.named("markers", "drum", 22, 18)
    m.named("markers", "capital", 23, 17)
    m.named("markers", "rubble", 22, 19)
    # laurels about the hamlet
    m.laurel(12, 6)
    m.laurel(22, 7)
    # signs (aethos steles)
    m.put(28, 11, STELE)                      # the east gate
    m.put(1, 11, STELE)                       # the west way out
    m.named("markers", "dig", 8, 10)          # a daily dig spot under the planes (ICHOR_STUB_DIG)
    m.force_block |= {(0, 8), (0, 10)}        # the plane's crown at the west edge: no way off the map
    m.cells([(0, 7)], "L")

    E = {
        "connections": [
            {"map": "MAP_ROUTE8_KOPAIS", "offset": 0, "direction": "right"},
            {"map": "MAP_ROUTE9_SCHISTE", "offset": LEB_ROAD - R9_EAST, "direction": "left"},
        ],
        "object_events": [
            obj(P + "ALETHEA_RIM", 9, 5, LB + "Alethea", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_ALETHEA_LEBADEIA", local_id="LOCALID_LEBADEIA_ALETHEA"),
            obj(P + "SAON", 5, 3, LB + "Saon", "MOVEMENT_TYPE_FACE_DOWN",
                local_id="LOCALID_LEBADEIA_SAON"),
            obj(P + "TROPHONIAN_PRIEST", 7, 4, LB + "Priest", "MOVEMENT_TYPE_FACE_DOWN",
                local_id="LOCALID_LEBADEIA_PRIEST"),
            obj(P + "PILGRIM_BLANKET", 2, 6, LB + "Farmer", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "PILGRIM_BLANKET", 5, 6, LB + "Sailor", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "PILGRIM_BLANKET", 8, 6, LB + "OldWoman", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "ELDER_M", 2, 4, LB + "OldMan", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj(P + "MERCHANT", 14, 11, LB + "CakeSeller", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "KID_M", 9, 18, LB + "Child", "MOVEMENT_TYPE_FACE_RIGHT"),
            item_ball(13, 9, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_LEBADEIA_REVIVE"),
        ],
        "warp_events": [
            warp(*hall, "MAP_LEBADEIA_PILGRIMS_HALL", 0),
            warp(*herk, "MAP_LEBADEIA_HERKYNA_HOUSE", 0),
            warp(*mason, "MAP_LEBADEIA_MASONS_HOUSE", 0),
            warp(6, 2, "MAP_TROPHONIOS_CAVE_B1F", 0),
        ],
        "coord_events": [trigger(x, 6, LB + "SpringsTalk") for x in (1, 3, 4, 6, 7, 9)],
        "bg_events": [
            sign(28, 11, LB + "SignEast"),
            sign(1, 11, LB + "SignWest"),
            sign(6, 2, LB + "Grille", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(4, 4, LB + "Lethe"),
            sign(8, 4, LB + "Mnemosyne", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(7, 2, LB + "SignSprings", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(2, 2, LB + "Tablets", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(8, 10, LB + "DigSpot"),
            hidden(3, 4, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_LEBADEIA_BRONZE_OBOL"),
            hidden(18, 5, "ITEM_CALCIUM", "FLAG_ICHOR_HIDDEN_LEBADEIA_CALCIUM"),
            hidden(1, 10, "ITEM_HONEY", "FLAG_ICHOR_HIDDEN_LEBADEIA_HONEY"),
        ],
    }
    views = [(30, 12), (24, 12), (17, 12), (12, 12), (6, 12), (4, 8), (5, 4), (6, 3), (18, 7),
             (4, 19), (16, 20), (1, 12)]
    return m, E, views


# ===========================================================================
# Route 9, the Split Road (52 x 44): where three roads meet (beat 36)
# ===========================================================================

DRUMS = (15, 18)           # the treasury's push puzzle, its grid's top-left (7 x 6)
PUZZLE = [
    "###.###",             # (3,0) the ruin's way in
    "#g.3.##",             # D3 at (3,1); its lip (2,1), the gully (1,1)
    "####.##",
    "##..2.#",             # D2 at (4,3); the alcove (5,3) where it stops
    "##.####",
    "g.1....",             # D1 at (2,5); its lip (1,5), the gully (0,5); the corridor east
]


def route9():
    m = PMap("Route9_Schiste", 52, 44)
    m.aethos_rows = set(range(38, 44))       # Kirrha's seam (south): aethos only
    W, H = 52, 44
    # The mountain's flank: laurel woods, mixed with olives and cypresses, stepped
    # by bands of crag whose faces show to the south. Paths are carved below.
    m.rect(0, 0, W - 1, H - 1, "L")
    # rock steps: one row of crag is a low cliff, its face to the south
    m.rect(0, 9, 18, 9, "#")                 # under the lookout's shelf
    m.rect(0, 6, 0, 8, "#")
    m.rect(14, 6, 21, 6, "#")                # over the fork's last stretch
    m.rect(21, 9, 30, 9, "#")                # under the bridge's far bank
    m.rect(25, 0, 28, 1, "#")
    m.rect(28, 10, 36, 10, "#")              # the shoulder over the shrine
    m.rect(31, 7, 35, 7, "#")
    m.rect(10, 12, 18, 12, "#")              # behind the treasury
    m.rect(21, 13, 26, 13, "#")
    m.rect(19, 18, 21, 28, "#")              # the cutting's walls
    m.rect(24, 23, 25, 28, "#")
    m.rect(2, 14, 6, 16, "#")                # an outcrop in the western woods
    m.rect(1, 18, 4, 18, "#")
    m.rect(0, 24, 12, 24, "#")               # the step over the olive terraces
    m.rect(5, 21, 9, 21, "#")
    m.rect(10, 18, 12, 21, "#")
    m.rect(40, 14, W - 1, 14, "#")           # over the goats' slope
    m.rect(44, 11, 48, 11, "#")
    m.rect(39, 19, 43, 19, "#")              # over the east road
    m.rect(40, 16, 42, 16, "#")
    m.rect(34, 22, 47, 22, "#")              # under the east road
    m.rect(33, 23, W - 1, 37, "O")           # olive groves on the lower slopes
    m.rect(36, 30, W - 1, 30, "#")
    m.rect(40, 26, 47, 26, "#")
    m.rect(33, 35, 44, 35, "#")
    m.rect(24, 28, 33, 28, "#")              # under the olive grove
    m.rect(36, 18, 36, 21, "#")
    m.rect(35, 18, 35, 22, "#")
    m.rect(0, 38, W - 1, H - 1, "O")         # Kirrha's seam: aethos's olives only

    # --- the lookout (36B): the far side, the ravine, the lip, the shelf ------
    m.rect(0, 0, 15, 4, "@")                 # the far side (stamped below)
    m.rect(0, 5, 15, 5, "@")                 # the ravine
    m.rect(1, 6, 13, 6, "@")                 # the lip
    m.rect(1, 7, 13, 8, ".")                 # the shelf
    # the fork's last stretch (segment 4), west along rows 7-8; band F2
    m.rect(14, 7, 20, 8, "=")
    m.rect(15, 7, 17, 8, ",")
    # segment 3, north-south down from the corner
    m.rect(19, 9, 20, 10, "=")
    # segment 2, west-east (rows 11-12); band F1; Phayllos runs here
    m.rect(19, 11, 28, 12, "=")
    m.rect(21, 11, 23, 12, ",")
    # segment 1, down to the crossroads
    m.rect(27, 13, 28, 14, "=")
    # the broken bridge's branch: east from the corner, over the gully, the far bank
    m.rect(21, 7, 21, 8, "#")
    m.rect(21, 8, 21, 8, "=")
    m.rect(22, 1, 24, 9, "g")
    m.rect(25, 6, 27, 8, ".")
    m.rect(25, 2, 26, 5, "=")
    m.rect(26, 6, 27, 7, ",")
    # --- the crossroads: the paved triangle ----------------------------------
    for y, (x0, x1) in {15: (27, 28), 16: (26, 33), 17: (26, 33), 18: (25, 31), 19: (24, 29),
                        20: (24, 28), 21: (23, 27), 22: (22, 25)}.items():
        m.rect(x0, y, x1, y, "p")
    m.rect(29, 11, 31, 15, ".")              # grass round the herm and the shrine's laurel
    m.rect(32, 11, 35, 15, ".")
    m.rect(29, 11, 36, 11, "L")
    # --- the east road: Lebadeia to the crossroads ----------------------------
    m.rect(37, R9_EAST, W - 1, R9_EAST + 1, "=")
    m.rect(44, 15, W - 1, 19, ".")           # Koretas's slope
    m.rect(48, 22, W - 1, 22, ".")           # the south verge at the edge
    m.rect(45, 15, 49, 16, ",")              # optional grass on the goats' slope
    m.rect(44, 16, 44, 18, ",")
    m.rect(42, R9_EAST, 44, R9_EAST + 1, ",")      # band A1
    m.rect(39, R9_EAST, 40, R9_EAST + 1, ",")      # band A2
    # the cleft north to the crossroads; Onomarchos's notch on its west side
    m.rect(37, 16, 38, 21, "=")
    m.rect(34, 16, 36, 17, "=")
    m.cells([(36, 19)], ".")
    # the Sphinx's seat: a goat track up from the cleft's top to a flat rock
    m.rect(37, 12, 38, 15, ",")
    m.rect(37, 9, 42, 11, ".")
    m.rect(37, 8, 42, 8, "#")
    # --- the south-west road: the cutting, the terraces, Kirrha ---------------
    m.rect(22, 23, 23, 32, "=")              # down through the cutting (rows 23-28)
    m.rect(22, 29, 23, 32, ",")              # band B2, 4 deep, below the cutting
    m.rect(9, 33, 23, 34, "=")               # the terrace path
    m.rect(9, 35, 10, H - 1, "=")            # down to Kirrha
    m.rect(9, 35, 10, 37, ",")               # band B3 among the wild olives
    m.cells([(16, 35)], ".")                 # Lykoreus's place on the terrace's edge
    # the olive terraces west of the cutting: a loop up the west stair, ledges down
    m.rect(2, 25, 12, 26, ".")               # terrace 1
    m.rect(2, 27, 12, 27, "_")
    m.rect(2, 28, 18, 29, ".")               # terrace 2
    m.rect(2, 30, 18, 30, "_")
    m.rect(2, 31, 20, 31, ".")               # terrace 3
    m.rect(3, 32, 20, 32, "_")
    m.rect(1, 25, 1, 34, "=")                # the west stair, up from the terrace path
    m.rect(1, 33, 8, 34, "=")
    m.rect(2, 32, 2, 32, "=")
    m.rect(5, 25, 9, 26, ",")                # optional grass on terrace 1
    m.rect(11, 28, 15, 29, ",")              # ... and terrace 2
    m.rect(13, 25, 13, 27, "#")
    # the olive grove south-east of the crossroads (optional grass, a lure)
    m.rect(26, 23, 32, 27, ".")
    m.rect(27, 24, 31, 26, ",")
    m.cells([(26, 22), (27, 22)], "p")
    # the south: the road down to Kirrha between olive woods
    m.rect(8, 38, 8, H - 1, ".")
    m.rect(9, 38, 10, H - 1, "=")
    m.rect(11, 38, 11, H - 1, ".")

    # --- the route standard (MAP_DESIGN section 8): grass on every road ------
    m.rect(44, 17, 49, 19, ",")              # the goats' slope, down to the road
    m.rect(50, 15, W - 1, 18, "L")           # the east edge stays closed above the road
    m.rect(41, R9_EAST, 44, R9_EAST + 1, ",")      # band A1, 4 deep
    m.rect(37, 17, 38, 19, ",")              # the cleft's floor
    m.rect(21, 11, 25, 12, ",")              # band F1, 5 deep
    m.rect(14, 7, 18, 8, ",")                # band F2, 5 deep
    m.rect(19, 9, 20, 10, ",")               # the fork's corner
    m.rect(27, 13, 28, 14, ",")              # the fork's foot
    m.rect(11, 7, 13, 8, ",")                # the lookout's shelf, its east end
    m.rect(6, 8, 10, 8, ",")
    m.rect(25, 6, 27, 8, ",")                # the broken bridge's far bank
    m.rect(25, 2, 26, 5, ",")                # ... and the gully path
    m.rect(37, 9, 42, 11, ",")               # the Sphinx's seat
    m.rect(2, 25, 12, 26, ",")               # terrace 1
    m.rect(9, 28, 18, 29, ",")               # terrace 2
    m.rect(4, 31, 20, 31, ",")               # terrace 3
    m.rect(26, 24, 32, 27, ",")              # the grove below the crossroads
    m.rect(22, 28, 23, 32, ",")              # band B2, 5 deep below the cutting
    m.rect(18, 33, 20, 34, ",")              # band B2b on the terrace path
    m.rect(9, 35, 10, 38, ",")               # band B3 among the olives
    m.rect(8, 39, 8, 42, ",")                # the road's verges down to Kirrha
    m.rect(11, 39, 11, 42, ",")
    m.cells([(24, 25)], ".")                 # Phokos's place in the cutting's wall
    m.cells([(21, 30)], ".")                 # Daulis's place beside band B2

    # --- the treasury's ruin and its drums (36C) -----------------------------
    ox, oy = DRUMS
    for j, row in enumerate(PUZZLE):
        for i, c in enumerate(row):
            m.ch[oy + j][ox + i] = {"#": "#", "g": "g", ".": ".", "1": ".", "2": ".", "3": "."}[c]
    m.rect(13, 17, 14, 24, "g")              # the gully under the ruin, west of the drums
    m.cells([(15, 17), (16, 18), (15, 19), (15, 20), (15, 21), (15, 22), (16, 22)], "g")
    m.rect(11, 14, 19, 16, "p")              # the treasury's floor
    m.cells([(18, 17)], "p")                 # the doorway in its south wall
    # walls: north (row 13), west and east (columns 10 and 20), south (row 17)
    for x in range(10, 21):
        side = "W_L" if x == 10 else ("W_R" if x == 20 else ("W_low" if x in (13, 14, 16) else "W_M"))
        m.named("ruin", side, x, 13)
    for y in (14, 15, 16):
        m.named("ruin", "NS", 10, y)
        m.named("ruin", "NS", 20, y)
    for x in range(10, 21):
        if x == 18:
            continue
        side = "NS_end" if x in (10, 20) else ("W_stub" if x == 17 else ("W_low" if x in (11, 12, 15) else "W_M"))
        if x == 19:
            side = "door_L"
        m.named("ruin", side, x, 17)

    # --- stamps ---------------------------------------------------------------
    # the far side: cliff tops, faces with the gorge between the two cliffs, the
    # cliffs' foot, the slope with Delphoi's sanctuary, falling into the ravine
    far_rows = [
        ["top_a", "top_a"],
        ["face_a", "face_b"],
        ["face_b", "face_a"],
        ["foot", "foot"],
        ["slope", "slope"],
    ]
    for y in range(5):
        for x in range(16):
            m.named("far", far_rows[y][(x + y) % 2], x, y)
    m.named("far", "gorge_top", 7, 1)
    m.named("far", "gorge", 7, 2)
    m.named("far", "gorge_foot", 7, 3)
    m.named("far", "temple_L", 9, 4)
    m.named("far", "temple_R", 10, 4)
    m.named("far", "theater", 12, 4)
    m.named("far", "roofs", 11, 4)
    m.named("far", "roofs", 5, 4)
    m.named("far", "roofs", 3, 4)
    for x in range(16):
        m.named("far", "slope_foot", x, 5)
    for x in range(1, 14):
        m.named("ravine", "lip", x, 6)
    m.named("markers", "bench_L", 4, 7)
    m.named("markers", "bench_R", 5, 7)
    m.named("markers", "cairn", 9, 7)
    # the broken bridge over the gully (row 8)
    m.named("timber", "W", 22, 8); m.named("timber", "gap", 23, 8); m.named("timber", "E", 24, 8)
    m.gully_extra |= {(22, 8), (23, 8), (24, 8)}
    m.named("markers", "dig", 26, 2)                 # the gully path's fixed dig (ICHOR_STUB_DIG)
    # the crossroads: the boundary stone, the great herm, Apollo's laurel and altar
    m.stamp("pmarkers", 30, 17, names={(0, 0): "stone_top", (0, 1): "boundary"})
    m.named("markers", "herm_top", 30, 13)
    m.named("markers", "herm", 30, 14)
    m.laurel(33, 12)
    m.named("markers", "altar_top", 32, 14)
    m.named("markers", "altar_bad", 32, 15)
    # the Sphinx's seat: feathers on the flat rock
    for (x, y) in ((38, 10), (40, 9), (41, 11)):
        m.named("markers", "feathers", x, y)
    m.named("markers", "boulder", 42, 9)
    # wild olives on the terraces and in the grove
    for (x, y) in ((3, 28), (8, 28), (16, 28)):
        m.wild_olive(x, y)
    for (x, y) in ((26, 23), (30, 23)):
        m.wild_olive(x, y)
    # signs (aethos steles)
    m.put(48, 18, STELE)                    # the east end
    m.put(26, 14, STELE)                    # the north-west fork
    m.put(24, 23, STELE)                    # the cutting
    m.cells([(25, 17)], ".")
    m.put(25, 17, STELE)                    # the crossroads
    m.cells([(13, 38)], ".")
    m.put(12, 38, STELE)                    # the south-west end

    lx, ly = DRUMS
    E = {
        "connections": [
            {"map": "MAP_LEBADEIA", "offset": R9_EAST - LEB_ROAD, "direction": "right"},
            {"map": "MAP_KIRRHA", "offset": R9_SOUTH - KIRRHA_NORTH, "direction": "down"},
        ],
        "object_events": [
            # 36A: Alethea at the crossroads; 36B: her lookout self, for the scene
            obj(P + "ALETHEA", 32, 17, R9 + "Alethea", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_ALETHEA_ROUTE9", local_id="LOCALID_ROUTE9_ALETHEA"),
            obj(P + "ALETHEA", 13, 8, R9 + "AletheaLookout", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_TEMP_14", local_id="LOCALID_ROUTE9_ALETHEA_LOOKOUT"),
            # the east road: Koretas and his goats, Onomarchos in the cleft
            obj(P + "GOATHERD", 46, 18, R9 + "Koretas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
            obj("OBJ_EVENT_GFX_SPECIES(KERAZAP)", 44, 17, R9 + "Goat", "MOVEMENT_TYPE_WANDER_AROUND",
                rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(KERAZAP)", 48, 16, R9 + "Goat", "MOVEMENT_TYPE_WANDER_AROUND",
                rx=1, ry=1),
            obj(P + "MAN", 36, 19, R9 + "Onomarchos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=4),
            # the crossroads: Psephos at the shrine, the old man, the omen's Enigmaw
            obj(P + "TITAN_GRUNT", 32, 16, R9 + "Psephos", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1,
                flag="FLAG_ICHOR_HIDE_GRUNT_PSEPHOS", local_id="LOCALID_ROUTE9_PSEPHOS"),
            obj(P + "ELDER_M", 29, 18, R9 + "OldMan", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("OBJ_EVENT_GFX_SPECIES(ENIGMAW)", 30, 18, R9 + "Enigmaw", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_TEMP_15", local_id="LOCALID_ROUTE9_ENIGMAW"),
            # the fork: Phayllos on the switchbacks, Xenodike on the bench, the items
            obj(P + "YOUTH_M", 26, 11, R9 + "Phayllos", "MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT", trainer=True,
                sight=3, rx=1),
            obj(P + "XENODIKE", 4, 7, R9 + "Xenodike", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_XENODIKE_LOOKOUT", local_id="LOCALID_ROUTE9_XENODIKE"),
            item_ball(1, 7, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_ROUTE9_MAX_REVIVE"),
            item_ball(26, 8, "ITEM_PP_MAX", "FLAG_ICHOR_ITEM_ROUTE9_PP_MAX"),
            # the treasury: the drums (the Girdle) and its floor's finds
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", lx + 2, ly + 5, "EventScript_StrengthBoulder",
                flag="FLAG_TEMP_11", local_id="LOCALID_ROUTE9_DRUM_1"),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", lx + 4, ly + 3, "EventScript_StrengthBoulder",
                flag="FLAG_TEMP_12", local_id="LOCALID_ROUTE9_DRUM_2"),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", lx + 3, ly + 1, "EventScript_StrengthBoulder",
                flag="FLAG_TEMP_13", local_id="LOCALID_ROUTE9_DRUM_3"),
            # ICHOR_STUB_TMS: SCRIPT.md's TM Rock Slide isn't a TM in this build yet;
            # TM Rock Tomb stands in until the TM list is redone
            item_ball(13, 15, "ITEM_TM_ROCK_TOMB", "FLAG_ICHOR_ITEM_ROUTE9_TM_ROCK_SLIDE"),
            item_ball(17, 14, "ITEM_HARD_STONE", "FLAG_ICHOR_ITEM_ROUTE9_HARD_STONE"),
            # the route standard's four more: Phokos in the cutting and Daulis by band B2
            # (both across the road), Amphissa on terrace 2 and Mopsos on the Sphinx's seat
            obj(P + "HOPLITE", 24, 25, R9 + "Phokos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2),
            obj(P + "FOWLER_F", 21, 30, R9 + "Daulis", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=2),
            obj(P + "HARVESTER", 6, 29, R9 + "Amphissa", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
            obj(P + "AUGUR", 38, 11, R9 + "Mopsos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
            # the south-west road: Lykoreus on the terrace, the terrace end's potion
            obj(P + "SHEPHERD", 16, 35, R9 + "Lykoreus", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=4),
            item_ball(12, 25, "ITEM_SUPER_POTION", "FLAG_ICHOR_ITEM_ROUTE9_SUPER_POTION"),
            item_ball(31, 27, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_ROUTE9_ULTRA_BALL"),
        ],
        "warp_events": [],
        "coord_events": (
            [trigger(34, y, R9 + "Crossroads", "VAR_TEMP_1") for y in (16, 17)]
            + [trigger(11, y, R9 + "Lookout", "VAR_TEMP_6") for y in (7, 8)]
            + [trigger(lx + 2, ly + 5, R9 + "DrumRoll1", "VAR_TEMP_7"),
               trigger(lx + 3, ly + 1, R9 + "DrumRoll3", "VAR_TEMP_4")]
            + [trigger(x, 36, R9 + "TowardKirrha", "VAR_TEMP_5") for x in (9, 10)]
        ),
        "bg_events": [
            sign(48, 18, R9 + "SignEast"),
            sign(26, 14, R9 + "SignFork"),
            sign(24, 23, R9 + "SignCutting"),
            sign(12, 38, R9 + "SignSouthWest"),
            sign(30, 14, R9 + "GreatHerm"),
            sign(25, 17, R9 + "SignCrossroads"),
            sign(32, 15, R9 + "Shrine", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(34, 14, R9 + "LaurelTree", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(7, 5, R9 + "Falls", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(9, 7, R9 + "Cairn"),
            sign(42, 9, R9 + "SphinxSeat"),
            sign(15, 13, R9 + "TreasuryView", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(26, 2, R9 + "GullyDig"),
            hidden(10, 7, "ITEM_ETHER", "FLAG_ICHOR_HIDDEN_ROUTE9_ETHER"),
            hidden(40, 10, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_HIDDEN_ROUTE9_PRETTY_FEATHER"),
            hidden(12, 14, "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_ROUTE9_NUGGET"),
            hidden(3, 25, "ITEM_REVIVAL_HERB", "FLAG_ICHOR_HIDDEN_ROUTE9_REVIVAL_HERB"),
        ],
    }
    views = [(50, 20), (45, 20), (41, 20), (37, 18), (34, 16), (29, 17), (27, 12), (22, 11),
             (19, 8), (14, 7), (6, 7), (24, 7), (23, 22), (19, 23), (16, 20), (15, 15), (22, 28),
             (22, 32), (16, 33), (6, 29), (10, 36), (10, 41), (39, 11), (29, 25)]
    return m, E, views


# ===========================================================================

MAPS = {
    "lebadeia": ("LAYOUT_LEBADEIA", "Lebadeia", lebadeia, ROAD_MUSIC),
    "route9": ("LAYOUT_ROUTE9_SCHISTE", "Route9_Schiste", route9, ROAD_MUSIC),
}
ENTRIES = {"lebadeia": [(31, 12), (31, 13)], "route9": [(51, 20), (51, 21)]}
EXITS = {"lebadeia": [(0, 12), (0, 13)], "route9": [(9, 43), (10, 43)]}
UNREACHABLE_OK = {
    "lebadeia": set(),
    # the PP Max and the dig across the broken bridge (the Winged Talaria);
    # the treasury's finds behind the drums (the Girdle, pushed in play)
    "route9": {(26, 8), (26, 2), (13, 15), (17, 14), (12, 14), (15, 13),
               (19, 21), (18, 19), (17, 23)},
}
# Cells the drums' pushes open, for the reachability check.
OPENS = {"route9": set()}


def check(key, m, E):
    people = {(o["x"], o["y"]) for o in E.get("object_events", [])
              if o["script"] != "Common_EventScript_FindItem"}
    seen = L.reach(m, ENTRIES[key], blocked_extra=people)
    bad = []
    targets = [(o["x"], o["y"], o["script"].split("_")[-1]) for o in E.get("object_events", [])]
    targets += [(b["x"], b["y"], b.get("script", b.get("item", "?")).split("_")[-1])
                for b in E.get("bg_events", [])]
    for (x, y, what) in targets:
        near = {(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))} | {(x, y)}
        if not (near & seen) and (x, y) not in UNREACHABLE_OK.get(key, ()):
            bad.append(f"{what}@{x},{y}")
    for e in E.get("coord_events", []) + E.get("warp_events", []):
        if (e["x"], e["y"]) not in seen and not ({(e["x"], e["y"] + 1), (e["x"], e["y"] - 1)} & seen):
            bad.append(f"event@{e['x']},{e['y']}")
    print(f"  {m.name}: {len(seen)} cells reachable" + (f"; OUT OF REACH: {', '.join(bad)}" if bad else ""))
    if not (set(EXITS[key]) & seen):
        print(f"  {m.name}: THE FAR EXIT IS OUT OF REACH")
    if key != "route9":
        return
    grass = L.grass_cells(m)
    parts, left = [], set(grass)
    while left:
        c = left.pop()
        part, todo = {c}, [c]
        while todo:
            x, y = todo.pop()
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                n = (x + dx, y + dy)
                if n in left:
                    left.discard(n)
                    part.add(n)
                    todo.append(n)
        parts.append(part)
    forced = []
    for part in parts:
        r = L.reach(m, ENTRIES[key], blocked_extra=people | part)
        xs = sorted({x for x, _ in part}); ys = sorted({y for _, y in part})
        if not (set(EXITS[key]) & r):
            forced.append(f"x {xs[0]}-{xs[-1]}, y {ys[0]}-{ys[-1]}")
    print(f"  {m.name}: {len(grass)} grass cells in {len(parts)} patches; forced on the main "
          f"road: {'; '.join(forced) if forced else 'NONE'}")


def build(only=None, shapes_only=False, tag=""):
    missing = []
    built = {}
    for key, (layout, folder, fn, music) in MAPS.items():
        if only and key not in only:
            continue
        m, E, views = fn()
        m.missing = missing
        m.autotile()
        built[key] = (m, E, views, layout, folder, music)
    if shapes_only:
        data = {}
        for kind in SHAPE_SETS:
            used = set()
            for (m, *_rest) in built.values():
                used |= m.shapes_used[kind]
            data[kind] = sorted(used)
        SHAPES.write_text(json.dumps(data, indent=1) + "\n")
        print({k: len(v) for k, v in data.items()}, "->", SHAPES.relative_to(ROOT))
        return
    if missing:
        print(f"{len(missing)} shape cells drawn with stand-ins: run --shapes, rebuild the art")
        for mm in sorted(set(missing))[:12]:
            print("   ", mm)
    errs = []
    for (m, *_rest) in built.values():
        errs += m.check_seams()
    if errs:
        sys.exit("seam errors:\n  " + "\n  ".join(errs[:20]))
    for key, (m, E, views, layout, folder, music) in built.items():
        border = crag_border(m.cat)
        L.write_layout(layout, folder, m, border)
        L.write_events(folder, E, music)
        L.render(m, E, border, views, tag)
        IMG.mkdir(parents=True, exist_ok=True)
        shutil.copy2(L.RENDER / f"{m.name}{tag}.png", IMG / f"{folder}.png")
        print(f"{folder}: {m.w}x{m.h} -> {(IMG / f'{folder}.png').relative_to(ROOT)}")
        check(key, m, E)
    return built


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    build(args.only.split(",") if args.only else None, args.shapes, args.tag)


if __name__ == "__main__":
    main()
