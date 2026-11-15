#!/usr/bin/env python3
"""Act III's outdoor maps around Kythera: the shared builder, and the driver.

The maps (design/phase4/SCRIPT.md, Part 2; design/MAP_DESIGN.md binds them):
  MAP_MELOS                        melos.py         aethos + melos
  MAP_ROUTE22_CRETAN_SEA           kythera_seas.py  aethos + melos
  MAP_ROUTE22_MYRTOAN_SEA          kythera_seas.py  aethos + melos
  MAP_ROUTE23_CRETAN_SEA           kythera_seas.py  aethos + melos
  MAP_KYTHERA_SKANDEIA             skandeia.py      aethos + skandeia
  MAP_TRIREME_EUPLOIA_DECK_SOUTH   euploia_south.py aethos + trireme

Each map module builds a Spec: a Grid of metatiles and collision, the header,
connections and events. This module writes the layout (map.bin, border.bin and
its layouts.json entry) and map.json, checks the result (warps on doors, people
and triggers reachable, bg events readable, the seam strips aethos-only) and
renders it:
  design/phase4/img/maps/<name>_1x.png and <name>_3x.png   the map, plain
  build/render/kythera/<name>_people.png                   with NPCs, 2x
  build/render/kythera/<name>_walk.png                     collision and events
  build/render/kythera/<name>_screens.png                  GBA-screen crops

  /usr/bin/python3 tools/ichor/maps/kythera_outdoor.py            # every map
  /usr/bin/python3 tools/ichor/maps/kythera_outdoor.py melos      # one module

Scripts are hand-written in data/maps/<Map>/scripts.pory; only map.json and
the layouts are generated here. Metatiles are placed by catalog key and name
(tools/ichor/maps/kythera_tiles.py), never by raw secondary id.
"""
from __future__ import annotations

import importlib
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
import kythera_tiles as KT  # noqa: E402
import render_map as RM  # noqa: E402

IMG = ROOT / "design/phase4/img/maps"
REVIEW = ROOT / "build/render/kythera"
LAYOUTS = ROOT / "data/layouts/layouts.json"

# ---------------------------------------------------------------------------
# aethos (General's numbering; design/phase1/TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS, GRASS_SHADE, TALL, FLOWERS, REEDS = 0x001, 0x01C, 0x00D, 0x004, 0x015
SEA = 0x170
STELE, HERM = 0x003, 0x01B
BOULDER = {"grass": 0x0E0, "rock": 0x0E1, "sand": 0x0E2}
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
SAND = 0x124
# sand set into grass (General's sand pit): its rim fades sand into the meadow
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}
TILLED = {"tl": 0x103, "t": 0x104, "tr": 0x105, "l": 0x10B, "c": 0x10C, "r": 0x10D,
          "bl": 0x113, "b": 0x114, "br": 0x115}
ASH = {"tl": 0x100, "t": 0x101, "tr": 0x102, "l": 0x108, "c": 0x109, "r": 0x10A,
       "bl": 0x110, "b": 0x111, "br": 0x112}
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
OLIVE_TIP_SEA = (0x1F6, 0x1F7)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
# sea stacks and reefs: pale stone standing in the sea (aethos 150-17F)
SEA_ROCK = 0x18C          # a lone boulder with a foam ring
SEA_ROCKS = (0x0C5, 0x0CD, 0x18C, 0x194)
ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]
# the farmhouse (General's route house): tiled roof, whitewash, door 021
FARMHOUSE = [[0x008, 0x009, 0x00A], [0x010, 0x011, 0x012],
             [0x018, 0x019, 0x01A], [0x020, 0x021, 0x022]]
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A, "w": 0x132, "e": 0x133}

SOLID, WATER_ELEV, GROUND_ELEV = 1 << 10, 1, 3

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER", "MB_WATERFALL", "MB_NO_SURFACING"}
DOOR_BEHAVIORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_SOUTH_ARROW_WARP", "MB_LADDER"}

SECONDARY_SYMBOL = {"melos": "gTileset_Melos", "skandeia": "gTileset_Skandeia",
                    "trireme": "gTileset_Trireme"}


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


def _attrs(kind, name):
    return np.fromfile(ROOT / f"data/tilesets/{kind}/{name}/porytiles_bin/metatile_attributes.bin", "<u2")


AETHOS_ATTR = _attrs("primary", "aethos")
SEC_ATTR = {name: _attrs("secondary", name) for name in SECONDARY_SYMBOL}


def behavior(mid, sec):
    a = AETHOS_ATTR[mid] if mid < 0x200 else SEC_ATTR[sec][mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    """A stable pseudo-random number in [0, 1) for a cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------

class Grid:
    """Metatile ids and collision for one layout on aethos + `sec`."""

    def __init__(self, w, h, sec, fill=GRASS):
        self.w, self.h, self.sec = w, h, sec
        self.mid = np.full((h, w), fill, np.uint16)
        self.solid = np.zeros((h, w), bool)

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def set(self, x, y, mid, solid=False):
        if self.inside(x, y):
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def get(self, x, y):
        return int(self.mid[y, x]) if self.inside(x, y) else None

    # --- secondary pieces, by catalog key and name -------------------------
    def m(self, key, name=None, cx=0, cy=0):
        return KT.mid(self.sec, key, name, cx, cy)

    def piece(self, key, name, x, y):
        """One named cell; collision from its walk code."""
        self.set(x, y, KT.mid(self.sec, key, name), KT.walk(self.sec, key, name) == "X")

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """A whole structure (or part of one) with its top-left at (x, y)."""
        s = KT.TILESETS[self.sec]["structures"][key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], s["walk"][cy + j][cx + i] == "X")

    def front(self, name, x, y):
        """A house front from the catalog's fronts (every cell solid but its door)."""
        f = KT.TILESETS[self.sec]["fronts"][name]
        for j, row in enumerate(f["ids"]):
            for i, mid in enumerate(row):
                self.set(x + i, y + j, mid, behavior(mid, self.sec) not in DOOR_BEHAVIORS)

    def block(self, rows, x, y, solid=True):
        for j, r in enumerate(rows):
            for i, mid in enumerate(r):
                if mid is not None:
                    self.set(x + i, y + j, mid, solid)

    # --- aethos trees ---------------------------------------------------------
    def olive(self, x, y):
        """A 2x2 olive; its crown pokes into the row above (TILES_aethos.md)."""
        below = y + 2 < self.h and self.get(x, y + 2) == OLIVE_TOP[0]
        self.block([OLIVE_TOP, OLIVE_BOT_TIP if below else OLIVE_BOT], x, y)
        if y > 0:
            above = (self.get(x, y - 1), self.get(x + 1, y - 1))
            if above == OLIVE_BOT:
                self.block([OLIVE_BOT_TIP], x, y - 1)
            elif all(m in (GRASS, GRASS_SHADE, FLOWERS) for m in above):
                self.block([OLIVE_TIP_GRASS], x, y - 1, solid=bool(self.solid[y - 1, x]))

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def pine(self, x, y):
        self.block(PINE, x, y)

    def orchard(self, cells, seed=0, period=3):
        """An olive grove: olives planted in staggered rows on a `period` grid,
        the grass between them solid (a grove is walled and tended, not a
        path), a cypress where a row ends short."""
        cells = set(cells)
        xs = [x for x, _ in cells]
        ys = [y for _, y in cells]
        x0, y0 = min(xs), min(ys)
        for (x, y) in sorted(cells, key=lambda p: (p[1], p[0])):
            j = (y - y0)
            if j % period != 1 or not self.free(x, y):
                continue
            off = (j // period) % 2 * (period // 2 + 1)
            if (x - x0 - off) % period == 0:
                if all((x + i, y + k) in cells and self.free(x + i, y + k) for i in (0, 1) for k in (0, 1)):
                    self.olive(x, y)
                elif all((x, y + k) in cells and self.free(x, y + k) for k in (0, 1)):
                    self.cypress(x, y)
        for (x, y) in cells:
            if self.get(x, y) in (GRASS, GRASS_SHADE, FLOWERS):
                self.set(x, y, FLOWERS if hashed(x, y, seed) < 0.06 else GRASS, True)
            self.solid[y, x] = True

    def wall_h(self, x0, x1, y):
        """A west-east dry-stone wall (aethos), x0..x1 inclusive."""
        for x in range(x0, x1 + 1):
            self.set(x, y, WALL["l"] if x == x0 else WALL["r"] if x == x1 else WALL["run"], True)

    def wall_v(self, x, y0, y1, side="e"):
        """A north-south dry-stone wall (aethos) on the cells' east or west side."""
        for y in range(y0, y1 + 1):
            self.set(x, y, WALL[side], True)

    def free(self, x, y, w=1, h=1, ok=(GRASS, GRASS_SHADE, FLOWERS)):
        return all(self.inside(x + i, y + j) and self.get(x + i, y + j) in ok
                   and not self.solid[y + j, x + i] for j in range(h) for i in range(w))

    def woods(self, cells, seed=0, pines=0.22, cypresses=0.5, boulders=0.0, skip=0.42, shrubs=None,
              glades=True):
        """Fill a set of (x, y) cells with a staggered mix of olives, stone pines
        and cypresses, so a tree line never settles into rows (MAP_DESIGN §7).
        Trees go top-down so crowns stack; each 2x2 spot is skipped with
        probability `skip` so the next row's trees fall between this row's, and
        the trees' sizes and kinds vary by a hash. A second pass puts cypresses
        in the narrow gaps and `shrubs(x, y)` (a myrtle, a briar) in some single
        cells; open patches left inside become small glades with flowers. Every
        cell ends solid."""
        cells = set(cells)
        order = sorted(cells, key=lambda p: (p[1], p[0]))
        for (x, y) in order:
            if not self.free(x, y):
                continue
            fits2 = all((x + i, y + j) in cells and self.free(x + i, y + j) for i in (0, 1) for j in (0, 1))
            if not fits2 or hashed(x, y, seed + 11) < skip:
                continue
            r = hashed(x, y, seed)
            if r < pines:
                self.pine(x, y)
            else:
                self.olive(x, y)
        for (x, y) in order:
            if not self.free(x, y):
                continue
            fits_c = all((x, y + j) in cells and self.free(x, y + j) for j in (0, 1))
            r = hashed(x, y, seed + 3)
            if fits_c and r < cypresses:
                self.cypress(x, y)
            elif shrubs and r < cypresses + 0.25:
                shrubs(x, y)
            elif boulders and hashed(x, y, seed + 5) < boulders:
                self.set(x, y, BOULDER["grass"], True)
        def edge(x, y):
            return any((x + dx, y + dy) not in cells and self.inside(x + dx, y + dy)
                       and not self.solid[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        for (x, y) in cells:
            if self.get(x, y) not in (GRASS, GRASS_SHADE, FLOWERS):
                continue
            if edge(x, y):
                # the wood's rim never shows open grass that won't let you in: a
                # cypress, a shrub or a boulder closes it
                if (x, y + 1) in cells and self.free(x, y + 1):
                    self.cypress(x, y)
                elif shrubs:
                    shrubs(x, y)
                if self.get(x, y) in (GRASS, GRASS_SHADE, FLOWERS):
                    self.set(x, y, BOULDER["grass"], True)
        for (x, y) in cells:
            if self.get(x, y) in (GRASS, GRASS_SHADE, FLOWERS):
                # the understory between the trunks; now and then a glade's anemones
                self.set(x, y, FLOWERS if glades and hashed(x, y, seed + 7) < 0.08 else GRASS_SHADE, True)
            self.solid[y, x] = True          # crown tips inside the woods too


def edge_key(n, s, w, e, nw, ne, sw, se):
    """Where a region cell's outside lies: tl t tr l c r bl b br or in_*."""
    if n and w:
        return "tl"
    if n and e:
        return "tr"
    if s and w:
        return "bl"
    if s and e:
        return "br"
    if n:
        return "t"
    if s:
        return "b"
    if w:
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


NEIGH = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]  # n s w e nw ne sw se


def around(plan, x, y, chars, off_map=False):
    h, w = len(plan), len(plan[0])
    out = []
    for dx, dy in NEIGH:
        i, j = x + dx, y + dy
        out.append(plan[j][i] in chars if 0 <= i < w and 0 <= j < h else off_map)
    return out


def surf_piece(n, s, w, e, nw, ne, sw, se):
    """The kythera-family surf piece for a sea cell, from which neighbours are
    sand: pieces are named by where the sea is (TILES_melos.md)."""
    if n and w:
        return "in_SE"
    if n and e:
        return "in_SW"
    if s and w:
        return "in_NE"
    if s and e:
        return "in_NW"
    if n:
        return "S"
    if s:
        return "N"
    if w:
        return "E"
    if e:
        return "W"
    if nw:
        return "out_NW"
    if ne:
        return "out_NE"
    if sw:
        return "out_SW"
    if se:
        return "out_SE"
    return None


def blob_key(region, x, y):
    """kythera_lib.blob_key: the soft-edge shape key of a region cell."""
    hh, ww = len(region), len(region[0])

    def at(i, j):
        if not (0 <= i < ww and 0 <= j < hh):
            return 1
        return 1 if region[j][i] else 0
    order = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # N NE E SE S SW W NW
    b = [at(x + dx, y + dy) for dx, dy in order]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)


def lay_ground(g, plan, legend):
    """Ground from an ASCII plan. legend maps a character to a ground kind:
    'sea', 'sand', 'grass', 'tall', 'path', 'flowers', 'shade', 'ash', or a
    callable(g, x, y). Sea next to sand gets the secondary's foam surf; sand next
    to grass a soft rim; paths fade into grass. Returns nothing; structures go on
    top afterwards."""
    sandish = {c for c, k in legend.items() if k == "sand"}
    seaish = {c for c, k in legend.items() if k == "sea"}
    grassish = {c for c, k in legend.items() if k in ("grass", "tall", "flowers", "shade", "woods")}
    pathish = {c for c, k in legend.items() if k == "path"}
    for y, row in enumerate(plan):
        assert len(row) == g.w, f"plan row {y} is {len(row)} wide, not {g.w}"
        for x, c in enumerate(row):
            kind = legend.get(c, "grass")
            if callable(kind):
                kind(g, x, y)
            elif kind == "sea":
                key = surf_piece(*around(plan, x, y, sandish))
                g.set(x, y, g.m("surf", key) if key else SEA)
            elif kind == "sand":
                n, s, w_, e, *_ = around(plan, x, y, grassish)
                k = edge_key(n, s, w_, e, False, False, False, False)
                g.set(x, y, SAND_GRASS[k] if k != "c" else SAND)
            elif kind == "path":
                n, s, w_, e, *_ = around(plan, x, y, grassish)
                k = "c" if (n and s) or (w_ and e) else edge_key(n, s, w_, e, False, False, False, False)
                g.set(x, y, PATH.get(k, PATH["c"]))
            elif kind == "tilled":
                tilled = {ch for ch, k in legend.items() if k == "tilled"}
                n, s, w_, e, *_ = (not v for v in around(plan, x, y, tilled, off_map=True))
                g.set(x, y, TILLED[edge_key(n, s, w_, e, False, False, False, False)])
            elif kind == "tall":
                g.set(x, y, TALL)
            elif kind == "flowers":
                g.set(x, y, FLOWERS)
            elif kind == "shade":
                g.set(x, y, GRASS_SHADE)
            else:
                g.set(x, y, GRASS)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

FACE_MOVE = {"down": "MOVEMENT_TYPE_FACE_DOWN", "up": "MOVEMENT_TYPE_FACE_UP",
             "left": "MOVEMENT_TYPE_FACE_LEFT", "right": "MOVEMENT_TYPE_FACE_RIGHT",
             "look": "MOVEMENT_TYPE_LOOK_AROUND", "wander": "MOVEMENT_TYPE_WANDER_AROUND",
             "updown": "MOVEMENT_TYPE_WALK_UP_AND_DOWN", "leftright": "MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT"}
FACING = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
          "east": "BG_EVENT_PLAYER_FACING_EAST", "west": "BG_EVENT_PLAYER_FACING_WEST",
          "any": "BG_EVENT_PLAYER_FACING_ANY"}


def obj(gfx, x, y, face, script, local_id=None, flag="0", rng=(0, 0), trainer=0, item=None, solid_ok=False):
    """An object event. gfx is OBJ_EVENT_GFX_<gfx> (or a full constant).
    trainer: sight range for a trainer. item: the ITEM_ constant of an item ball.
    solid_ok: it may stand on an impassable cell (a statue in a niche, a boat)."""
    if not gfx.startswith("OBJ_EVENT_GFX_"):
        gfx = "OBJ_EVENT_GFX_" + gfx
    return {"gfx": gfx, "x": x, "y": y, "face": face, "script": script, "local_id": local_id,
            "flag": flag, "range": rng, "trainer": trainer, "item": item, "solid_ok": solid_ok}


def item_ball(x, y, item, flag):
    return obj("ITEM_BALL", x, y, "down", "Common_EventScript_FindItem", flag=flag, item=item)


def warp(x, y, dest_map, dest_warp, elevation=0):
    return {"x": x, "y": y, "map": dest_map, "warp": dest_warp, "elevation": elevation}


def trigger(x, y, script, var="VAR_TEMP_0", value=0, elevation=3):
    return {"x": x, "y": y, "script": script, "var": var, "value": value, "elevation": elevation}


def sign(x, y, script, facing="any"):
    return {"type": "sign", "x": x, "y": y, "script": script, "facing": facing}


def hidden(x, y, item, flag):
    """A hidden item. Elevation 0, so it answers from land or from the sea
    (a surfer's elevation is the water's). Its flag must be a vanilla flag at
    or above FLAG_HIDDEN_ITEMS_START (tools/ichor/claim_ranges.md)."""
    return {"type": "hidden_item", "x": x, "y": y, "item": item, "flag": flag, "facing": "any"}


class Spec:
    def __init__(self, name, grid, **kw):
        self.name = name
        self.grid = grid
        self.map_id = kw.get("map_id") or "MAP_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()
        self.layout_id = "LAYOUT_" + self.map_id[4:]
        self.music = kw["music"]
        self.mapsec = kw["mapsec"]
        self.map_type = kw.get("map_type", "MAP_TYPE_ROUTE")
        self.weather = kw.get("weather", "WEATHER_SUNNY")
        self.show_name = kw.get("show_name", True)
        self.border = kw.get("border", [SEA] * 4)
        self.connections = kw.get("connections", [])
        self.objects = kw.get("objects", [])
        self.warps = kw.get("warps", [])
        self.coords = kw.get("coords", [])
        self.bgs = kw.get("bgs", [])
        self.seams = kw.get("seams", {})        # side -> width of the aethos-only strip
        self.start = kw.get("start")            # a walkable tile every check reaches from
        self.allow_cycling = kw.get("allow_cycling", True)
        self.screens = kw.get("screens", {})    # review crops: name -> (x, y)
        self.blocks = kw.get("blocks")          # precomposed map.bin (the deck), else from grid
        self.extra_reach = kw.get("extra_reach", ())  # cells counted reachable (surf landings)


def encode(g):
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mid[y, x])
            elev = WATER_ELEV if behavior(mid, g.sec) in SURF_BEHAVIORS else GROUND_ELEV
            out[y, x] = mid | (SOLID if g.solid[y, x] else 0) | (elev << 12)
    return out


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def bg_json(b):
    if b.get("type") == "hidden_item":
        return {"type": "hidden_item", "x": b["x"], "y": b["y"], "elevation": 0,
                "item": b["item"], "flag": b["flag"]}
    return {"type": "sign", "x": b["x"], "y": b["y"], "elevation": 0,
            "player_facing_dir": FACING[b["facing"]], "script": b["script"]}


def emit(spec):
    """Write the layout, its layouts.json entry and map.json."""
    g = spec.grid
    blocks = spec.blocks if spec.blocks is not None else encode(g)
    d = ROOT / "data/layouts" / spec.name
    d.mkdir(parents=True, exist_ok=True)
    blocks.astype("<u2").tofile(d / "map.bin")
    np.array(spec.border, "<u2").tofile(d / "border.bin")

    layouts = json.loads(LAYOUTS.read_text())
    for lay in layouts["layouts"]:
        if lay.get("id") == spec.layout_id:
            lay["width"], lay["height"] = g.w, g.h
            lay["primary_tileset"] = "gTileset_Aethos"
            lay["secondary_tileset"] = SECONDARY_SYMBOL[g.sec]
            break
    else:
        raise SystemExit(f"{spec.layout_id} isn't in layouts.json (run new_map.py first)")
    write_json(LAYOUTS, layouts)

    objects = []
    for o in spec.objects:
        ev = {}
        if o["local_id"]:
            ev["local_id"] = o["local_id"]
        rx, ry = o["range"]
        ev.update({
            "graphics_id": o["gfx"], "x": o["x"], "y": o["y"], "elevation": 3,
            "movement_type": FACE_MOVE.get(o["face"], o["face"]),
            "movement_range_x": rx, "movement_range_y": ry,
            "trainer_type": "TRAINER_TYPE_NORMAL" if o["trainer"] else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": o["item"] or str(o["trainer"]),
            "script": o["script"], "flag": o["flag"],
        })
        objects.append(ev)
    data = {
        "id": spec.map_id, "name": spec.name, "layout": spec.layout_id, "music": spec.music,
        "region": "REGION_HOENN", "region_map_section": spec.mapsec, "requires_flash": False,
        "weather": spec.weather, "map_type": spec.map_type, "allow_cycling": spec.allow_cycling,
        "allow_escaping": False, "allow_running": True, "show_map_name": spec.show_name,
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
        "connections": [{"map": m, "offset": off, "direction": side} for (side, m, off) in spec.connections] or None,
        "object_events": objects,
        "warp_events": [{"x": w["x"], "y": w["y"], "elevation": w["elevation"], "dest_map": w["map"],
                         "dest_warp_id": str(w["warp"])} for w in spec.warps],
        "coord_events": [{"type": "trigger", "x": c["x"], "y": c["y"], "elevation": c["elevation"],
                          "var": c["var"], "var_value": str(c["value"]), "script": c["script"]}
                         for c in spec.coords],
        "bg_events": [bg_json(b) for b in spec.bgs],
    }
    write_json(ROOT / "data/maps" / spec.name / "map.json", data)
    return blocks


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y, surf=False):
    h, w = blocks.shape
    if not (0 <= x < w and 0 <= y < h):
        return False
    b = int(blocks[y, x])
    if b & SOLID:
        return False
    return surf or (b >> 12) != WATER_ELEV


def reachable(blocks, start, sec, surf=False, extra=()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in seen:
                continue
            if walkable(blocks, *p, surf=surf) or p in extra:
                seen.add(p)
                q.append(p)
    return seen


def check(spec, blocks):
    errors = []
    g = spec.grid
    sec = g.sec
    walk_reach = reachable(blocks, spec.start, sec, surf=False, extra={(w["x"], w["y"]) for w in spec.warps})
    surf_reach = reachable(blocks, spec.start, sec, surf=True, extra={(w["x"], w["y"]) for w in spec.warps})
    reach = surf_reach
    for w in spec.warps:
        b = behavior(int(blocks[w["y"], w["x"]]) & 0x3FF, sec)
        if b not in DOOR_BEHAVIORS and not w.get("any_tile"):
            errors.append(f"{spec.name}: warp at ({w['x']},{w['y']}) is on {b}, not a door")
        if (w["x"], w["y"]) not in reach:
            errors.append(f"{spec.name}: warp at ({w['x']},{w['y']}) is unreachable")
    for o in spec.objects:
        x, y = o["x"], o["y"]
        if not o["solid_ok"] and not walkable(blocks, x, y, surf=True):
            errors.append(f"{spec.name}: object {o['local_id'] or o['script']} at ({x},{y}) stands on a solid cell")
        fronts = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))]
        if not any(p in reach for p in fronts) and (x, y) not in reach:
            errors.append(f"{spec.name}: object {o['local_id'] or o['script']} at ({x},{y}) can't be reached")
    for c in spec.coords:
        if (c["x"], c["y"]) not in reach:
            errors.append(f"{spec.name}: trigger at ({c['x']},{c['y']}) is unreachable")
    seen_bg = {}
    taken = {(o["x"], o["y"]) for o in spec.objects}
    for b in spec.bgs:
        x, y = b["x"], b["y"]
        fronts = {"north": [(x, y + 1)], "south": [(x, y - 1)], "east": [(x - 1, y)], "west": [(x + 1, y)]}
        cand = fronts.get(b["facing"], [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
                          + ([] if b.get("type") == "hidden_item" else [(x, y)]))
        if not any(p in reach for p in cand):
            errors.append(f"{spec.name}: bg event at ({x},{y}) can't be read")
        # the first bg event on a cell wins, and a taken hidden item answers nothing
        if (x, y) in seen_bg:
            errors.append(f"{spec.name}: two bg events share ({x},{y})")
        seen_bg[(x, y)] = b
        if b.get("type") == "hidden_item" and (x, y) in taken:
            errors.append(f"{spec.name}: hidden item at ({x},{y}) is under an object")
    mids = blocks & 0x3FF
    for side, width in spec.seams.items():
        if side == "west":
            cells = [(x, y) for x in range(width) for y in range(g.h)]
        elif side == "east":
            cells = [(x, y) for x in range(g.w - width, g.w) for y in range(g.h)]
        elif side == "north":
            cells = [(x, y) for x in range(g.w) for y in range(width)]
        else:
            cells = [(x, y) for x in range(g.w) for y in range(g.h - width, g.h)]
        bad = [(x, y) for (x, y) in cells if int(mids[y, x]) >= 0x200]
        if bad:
            errors.append(f"{spec.name}: {len(bad)} {sec} metatiles in the {side} seam strip, e.g. {bad[:4]}")
    spec.walk_reach, spec.surf_reach = walk_reach, surf_reach
    return errors


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_R = {}


def renderer(sec):
    if sec not in _R:
        RM.read_fieldmap_constants()
        syms = RM.scan_tileset_symbols()
        _R[sec] = RM.Renderer(RM.Tileset(RM.resolve_tileset("gTileset_Aethos", syms)),
                              RM.Tileset(RM.resolve_tileset(SECONDARY_SYMBOL[sec], syms)))
    return _R[sec]


def render_array(sec, blocks):
    h, w = blocks.shape
    return RM.render_blocks(renderer(sec), blocks.reshape(-1), w).convert("RGB")


SPRITES = ROOT / "graphics/object_events/pics/people/ichor"
FRAME = {"down": 0, "up": 1, "left": 2, "right": 2}


def sprite(gfx, face):
    g = gfx.replace("OBJ_EVENT_GFX_ICHOR_", "").lower()
    p = SPRITES / f"{g}.png"
    if p.exists():
        sheet = Image.open(p)
        pal = sheet.getpalette()
        arr = np.array(sheet)
        f = FRAME.get(face, 0)
        fr = arr[:, f * 16:(f + 1) * 16]
        rgba = np.zeros((fr.shape[0], 16, 4), np.uint8)
        for j in range(fr.shape[0]):
            for i in range(16):
                v = fr[j, i]
                if v:
                    rgba[j, i] = (*pal[v * 3:v * 3 + 3], 255)
        spr = Image.fromarray(rgba)
        if face == "right":
            spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
        return spr
    misc = {"OBJ_EVENT_GFX_ITEM_BALL": ROOT / "graphics/object_events/pics/misc/ichor_item_jar.png"}.get(
        gfx, ROOT / f"graphics/object_events/pics/misc/{gfx.replace('OBJ_EVENT_GFX_ICHOR_', '').lower()}.png")
    if misc and misc.exists():
        im = Image.open(misc).convert("RGBA")
        arr = np.array(im)
        pal0 = np.array(Image.open(misc).convert("RGB"))[0, 0]
        arr[(arr[..., :3] == pal0).all(-1)] = 0
        return Image.fromarray(arr[:16, :16])
    return None


def with_people(im, spec):
    out = im.convert("RGBA")
    for o in sorted(spec.objects, key=lambda o: o["y"]):
        x, y = o["x"] * 16, o["y"] * 16
        spr = sprite(o["gfx"], o["face"])
        if spr is None:
            out.alpha_composite(Image.new("RGBA", (10, 10), (240, 60, 160, 255)), (x + 3, y + 3))
        else:
            out.alpha_composite(spr, (x, y + 16 - spr.height))
    return out.convert("RGB")


def overlay(im, spec, blocks):
    out = im.convert("RGBA")
    lay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16
    for y in range(blocks.shape[0]):
        for x in range(blocks.shape[1]):
            b = int(blocks[y, x])
            if b & SOLID:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif b >> 12 == WATER_ELEV:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 80, 255, 40))
    for o in spec.objects:
        d.ellipse([o["x"] * c + 2, o["y"] * c + 2, o["x"] * c + c - 3, o["y"] * c + c - 3],
                  outline=(255, 255, 0, 255), width=2)
    for w in spec.warps:
        d.rectangle([w["x"] * c + 1, w["y"] * c + 1, w["x"] * c + c - 2, w["y"] * c + c - 2],
                    outline=(0, 255, 255, 255), width=2)
    for t in spec.coords:
        d.rectangle([t["x"] * c + 5, t["y"] * c + 5, t["x"] * c + c - 6, t["y"] * c + c - 6], fill=(255, 0, 255, 170))
    for b in spec.bgs:
        col = (0, 230, 120, 255) if b.get("type") == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4], fill=col, width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4], fill=col, width=2)
    for x in range(0, out.size[0], c * 5):
        d.line([x, 0, x, out.size[1]], fill=(255, 255, 255, 40))
    for y in range(0, out.size[1], c * 5):
        d.line([0, y, out.size[0], y], fill=(255, 255, 255, 40))
    return Image.alpha_composite(out, lay).convert("RGB")


def screens(spec, blocks, people_im, margin=8):
    """GBA-screen crops (15x10 tiles, the player on the 8th column and 5th row)
    around each review point, from the map padded with its border, at 2x."""
    if not spec.screens:
        return
    h, w = blocks.shape
    bord = np.array(spec.border, np.uint16).reshape(2, 2)
    big = np.empty((h + 2 * margin, w + 2 * margin), np.uint16)
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            big[y, x] = bord[y % 2, x % 2]
    big[margin:margin + h, margin:margin + w] = blocks
    im = render_array(spec.grid.sec, big)
    im.paste(people_im, (margin * 16, margin * 16))
    crops = []
    for name, (px, py) in spec.screens.items():
        x0, y0 = (px - 7 + margin) * 16, (py - 4 + margin) * 16
        crops.append(im.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
    cols = 2
    sheet = Image.new("RGB", (cols * 480 + 8, -(-len(crops) // cols) * 328 - 8), (24, 24, 32))
    for i, crop in enumerate(crops):
        sheet.paste(crop, ((i % cols) * 488, (i // cols) * 328))
    sheet.save(REVIEW / f"{spec.name}_screens.png")


def render(spec, blocks):
    IMG.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    im = render_array(spec.grid.sec, blocks)
    base = spec.name.lower()
    im.save(IMG / f"{base}_1x.png")
    im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(IMG / f"{base}_3x.png")
    ppl = with_people(im, spec)
    ppl.resize((ppl.width * 2, ppl.height * 2), Image.NEAREST).save(REVIEW / f"{spec.name}_people.png")
    ov = overlay(ppl, spec, blocks)
    ov.resize((ov.width * 2, ov.height * 2), Image.NEAREST).save(REVIEW / f"{spec.name}_walk.png")
    screens(spec, blocks, ppl)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

MODULES = ("euploia_south", "melos", "kythera_seas", "skandeia")


def build_module(name):
    mod = importlib.import_module(name)
    errors = []
    for spec in mod.specs():
        blocks = emit(spec)
        errors += check(spec, blocks)
        render(spec, blocks)
        print(f"kythera_outdoor: {spec.name} {spec.grid.w}x{spec.grid.h} written")
    return errors


def main():
    names = sys.argv[1:] or MODULES
    errors = []
    for n in names:
        errors += build_module(n)
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(1)
    print("kythera_outdoor: checks pass")


if __name__ == "__main__":
    main()
