"""The map-building kit for the Kithairon crossing (tools/ichor/maps/kithairon.py).

A map is drawn as a grid of ground characters plus stamped structures, then
auto-tiled from the tilesets' catalogs (build/kithairon/<dir>/catalog.json):

  .  grass (aethos)         ,  tall grass (soft edges)      =  road (soft edges)
  #  crag (grey rock, with a south face)                    ~  water (pools, the Asopos)
  F  fir woods: filled with staggered firs (and the odd oak)
  w  dry-stone wall (aethos)  _  terrace ledge, jump south (aethos)
  v  a vine row on its trellis                              p  paving (aethos's patch)
  s  scree (walkable)       b  a boulder                    c  the fort's court
  k  the cave floor         @  under a stamp (set in code)

Seam rows: `aethos_rows` may use only aethos metatiles (a neighbor with
another secondary); `core_rows` only aethos or the core section shared by
gTileset_Kithairon and gTileset_Kronia. Both are enforced when a map is built.
"""
from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/kithairon"
LAYOUTS = ROOT / "data/layouts/layouts.json"
RENDER = ROOT / "build/render/kithairon"
SHAPES = ROOT / "tools/ichor/art/kithairon_shapes.json"

SETS = {"kithairon": ("gTileset_Kithairon", "kithairon"), "kronia": ("gTileset_Kronia", "kronia"),
        "cave": ("gTileset_KithaironCave", "kithairon_cave")}
CORE = {"tall", "path", "crag", "water", "fir", "fir_b", "fir_stack", "fir_stack_b", "fir_young",
        "oak", "crag_detail", "markers", "fir_shade", "fir_b_shade", "fir_stack_shade",
        "fir_stack_b_shade", "fir_young_shade", "oak_shade"}
SHAPE_SETS = ("tall", "path", "crag", "water", "cave")

# aethos metatiles (General's ids; design/phase1/TILES_aethos.md)
GRASS, TALL, SHADE = 0x001, 0x00D, 0x01C
PATCH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA,
         "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
LEDGE, LEDGE_L, LEDGE_R = 0x087, 0x0D5, 0x0D6
WALL_EW, WALL_W, WALL_E, WALL_NS = 0x149, 0x148, 0x14A, 0x132
STELE, HERM = 0x003, 0x01B
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
PINE_TOP, PINE_BOT = (0x01E, 0x01F), (0x026, 0x027)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016


def hsh(x, y, salt=0):
    h = (x * 73856093 ^ y * 19349663 ^ salt * 83492791) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h >> 8) % 100


NEIGH = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def blob_key(inside, x, y):
    b = [1 if inside(x + dx, y + dy) else 0 for dx, dy in NEIGH]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)


class Catalog:
    def __init__(self, setname, need_shapes=True):
        p = CAT / SETS[setname][1] / "catalog.json"
        if not p.exists():
            sys.exit(f"{p} is missing: run /usr/bin/python3 tools/ichor/art/kithairon_build.py")
        self.setname = setname
        self.s = {d["key"]: d for d in json.loads(p.read_text())["structures"]}
        self.core_ids = set()
        for k, d in self.s.items():
            if k in CORE:
                for row in d["ids"]:
                    self.core_ids.update(row)

    def has(self, key, name=None):
        return key in self.s and (name is None or name in self.s[key]["names"])

    def cell(self, key, cx, cy):
        d = self.s[key]
        return d["ids"][cy][cx], d["walk"][cy][cx]

    def named(self, key, name):
        cx, cy = self.s[key]["names"][name]
        return self.cell(key, cx, cy)


class Map:
    def __init__(self, name, w, h, setname, missing_shapes=None):
        self.name, self.w, self.h, self.setname = name, w, h, setname
        self.cat = Catalog(setname)
        self.ch = [["."] * w for _ in range(h)]
        self.mt = [[None] * w for _ in range(h)]
        self.walkc = [["."] * w for _ in range(h)]
        self.force_block = set()
        self.force_open = set()
        self.aethos_rows, self.core_rows = set(), set()
        self.pathlike = set()
        self.pavelike = set()
        self.shapes_used = {k: set() for k in SHAPE_SETS}
        self.missing = missing_shapes if missing_shapes is not None else []
        self.water_cells = set()
        self.stamped = set()
        self.seed = sum(map(ord, name))

    # --- drawing the ground grid -----------------------------------------
    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            for x in range(max(0, x0), min(self.w - 1, x1) + 1):
                self.ch[y][x] = c

    def cells(self, pts, c):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.ch[y][x] = c

    def rows(self, x0, y0, rows, legend=None):
        """Paint an ASCII block; ' ' leaves a cell as it is."""
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != " " and 0 <= x0 + i < self.w and 0 <= y0 + j < self.h:
                    self.ch[y0 + j][x0 + i] = (legend or {}).get(c, c)

    def grid(self, rows):
        assert len(rows) == self.h, (self.name, len(rows))
        for y, r in enumerate(rows):
            assert len(r) == self.w, (self.name, y, len(r))
            self.ch[y] = list(r)

    def at(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.ch[y][x]
        return None

    # --- stamps ------------------------------------------------------------
    def put(self, x, y, mid, walk="X"):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        self.mt[y][x] = mid
        self.walkc[y][x] = walk
        self.ch[y][x] = "@"
        self.stamped.add((x, y))

    def stamp(self, key, x, y, cells=None, names=None):
        """Place a catalog structure with its top-left cell at (x, y). `cells`
        limits it to some (cx, cy); `names` places named cells by offset."""
        d = self.cat.s[key]
        if names:
            for (dx, dy), n in names.items():
                mid, wk = self.cat.named(key, n)
                self.put(x + dx, y + dy, mid, wk)
            return
        for cy in range(d["h"]):
            for cx in range(d["w"]):
                if cells is not None and (cx, cy) not in cells:
                    continue
                mid, wk = self.cat.cell(key, cx, cy)
                self.put(x + cx, y + cy, mid, wk)

    def named(self, key, name, x, y):
        mid, wk = self.cat.named(key, name)
        self.put(x, y, mid, wk)

    def fir(self, x, y, kind="fir"):
        """A lone fir: (x, y) is its spire row's left cell."""
        self.stamp(kind, x, y)

    def oak(self, x, y):
        self.stamp("oak", x, y)

    def olive(self, x, y):
        """An aethos olive: (x, y) its top-left; draws the crown tip above on grass."""
        if self.at(x, y - 1) == "." and (x, y - 1) not in self.stamped:
            self.put(x, y - 1, OLIVE_TIP[0], "T")
            self.put(x + 1, y - 1, OLIVE_TIP[1], "T")
        self.put(x, y, OLIVE_TOP[0]); self.put(x + 1, y, OLIVE_TOP[1])
        self.put(x, y + 1, OLIVE_BOT[0]); self.put(x + 1, y + 1, OLIVE_BOT[1])

    def pine(self, x, y):
        self.put(x, y, PINE_TOP[0]); self.put(x + 1, y, PINE_TOP[1])
        self.put(x, y + 1, PINE_BOT[0]); self.put(x + 1, y + 1, PINE_BOT[1])

    def cypress(self, x, y):
        self.put(x, y, CYPRESS_TOP, "T")
        self.put(x, y + 1, CYPRESS_BOT)

    # --- auto-tiling -------------------------------------------------------
    def region(self, chars, extra=()):
        extra = set(extra)
        return lambda x, y: (not (0 <= x < self.w and 0 <= y < self.h)) or \
            self.ch[y][x] in chars or (x, y) in extra

    def shape(self, setkey, key, x, y):
        self.shapes_used[setkey].add(key)
        d = self.cat.s.get(setkey)
        if d and key in d["names"]:
            return self.cat.named(setkey, key)
        self.missing.append((self.name, setkey, key))
        # stand-in until the art is rebuilt with this shape
        return self.cat.named(setkey, "1|11111111") if d else (GRASS, ".")

    def patch(self, inside, x, y):
        n, s_, w_, e = inside(x, y - 1), inside(x, y + 1), inside(x - 1, y), inside(x + 1, y)
        v = "T" if not n else ("B" if not s_ else "")
        hz = "L" if not w_ else ("R" if not e else "")
        k = (v + hz) or "C"
        if k in ("T", "B") and not hz:
            k = v
        return PATCH.get(k, PATCH["C"])

    def autotile(self):
        ch = self.ch
        tall = self.region(",")
        road = self.region("=", self.pathlike)
        crag = self.region("#")
        water = self.region("~")
        cave = self.region("#")
        pave = self.region("p", self.pavelike)
        for y in range(self.h):
            for x in range(self.w):
                if self.mt[y][x] is not None:
                    continue
                c = ch[y][x]
                aeth = y in self.aethos_rows
                if c == ".":
                    self.set(x, y, GRASS, ".")
                elif c == ",":
                    if aeth:
                        self.set(x, y, TALL, "G")
                    else:
                        self.set(x, y, *self.shape("tall", blob_key(tall, x, y), x, y))
                elif c == "=":
                    if aeth:
                        self.set(x, y, self.patch(self.region("="), x, y), ".")
                    else:
                        self.set(x, y, *self.shape("path", blob_key(road, x, y), x, y))
                elif c == "p":
                    self.set(x, y, self.patch(pave, x, y), ".")
                elif c == "#":
                    assert not aeth, (self.name, x, y, "crag in an aethos-only row")
                    if self.setname == "cave":
                        self.set(x, y, *self.shape("cave", blob_key(cave, x, y), x, y))
                    else:
                        k = blob_key(crag, x, y)
                        if k == "1|11111111" and hsh(x, y, self.seed) < 16:
                            name = ("crack", "boulders", "tuft", "juniper", "ivy_top")[hsh(x, y, 5) % 5]
                            self.set(x, y, *self.cat.named("crag_detail", name))
                            self.shapes_used["crag"].add(k)
                        else:
                            self.set(x, y, *self.shape("crag", k, x, y))
                elif c == "~":
                    assert not aeth
                    self.set(x, y, *self.shape("water", blob_key(water, x, y), x, y))
                    self.water_cells.add((x, y))
                elif c == "w":
                    ns = ch[y - 1][x] == "w" if y > 0 else False
                    ss = ch[y + 1][x] == "w" if y + 1 < self.h else False
                    we = (x > 0 and ch[y][x - 1] == "w")
                    ea = (x + 1 < self.w and ch[y][x + 1] == "w")
                    if (ns or ss) and not (we or ea):
                        mid = WALL_NS
                    elif we and ea:
                        mid = WALL_EW
                    elif ea:
                        mid = WALL_W
                    elif we:
                        mid = WALL_E
                    else:
                        mid = WALL_EW
                    self.set(x, y, mid, "X")
                elif c == "_":
                    l = x > 0 and ch[y][x - 1] == "_"
                    r = x + 1 < self.w and ch[y][x + 1] == "_"
                    mid = LEDGE if (l and r) else (LEDGE_L if r else (LEDGE_R if l else LEDGE))
                    self.set(x, y, mid, "J")
                elif c == "v":
                    l = x > 0 and ch[y][x - 1] == "v"
                    r = x + 1 < self.w and ch[y][x + 1] == "v"
                    name = "M" if (l and r) else ("W" if r else ("E" if l else "M"))
                    if name == "M" and hsh(x, y, 9) < 40:
                        name = "grapes"
                    self.set(x, y, *self.cat.named("trellis", name))
                elif c == "s":
                    self.set(x, y, *self.cat.named("markers", "scree" if hsh(x, y) % 2 else "scree_b"))
                elif c == "b":
                    self.set(x, y, *self.cat.named("markers", "boulder"))
                elif c == "c":
                    self.set(x, y, *self.cat.named("fort", "court"))
                elif c == "k":
                    self.set(x, y, *self.cat.named("cave_floor",
                                                   "pebbles" if hsh(x, y, 3) < 12 else "plain"))
                elif c == "F":
                    pass   # woods: filled below
                elif c == "@":
                    self.set(x, y, GRASS, ".")
                else:
                    raise ValueError(f"{self.name}: unknown ground {c!r} at {x},{y}")
        self.woods()

    def set(self, x, y, mid, walk):
        self.mt[y][x] = mid
        self.walkc[y][x] = walk

    def woods(self):
        """Fill 'F' with firs, column pairs on even x, each pair's run of rows
        stacked: spire, crown, base-with-the-next-spire, ... base."""
        F = lambda x, y: 0 <= x < self.w and 0 <= y < self.h and self.ch[y][x] == "F"
        done = set()
        for x in range(0, self.w, 2):
            y = 0
            while y < self.h:
                if not (F(x, y) and F(x + 1, y)):
                    y += 1
                    continue
                y0 = y
                while F(x, y) and F(x + 1, y):
                    y += 1
                y1 = y - 1
                self._fir_run(x, y0, y1, done)
        # single columns left over: young firs, or a boulder in an odd cell
        for x in range(self.w):
            y = 0
            while y < self.h:
                if not F(x, y) or (x, y) in done:
                    y += 1
                    continue
                y0 = y
                while F(x, y) and (x, y) not in done:
                    y += 1
                n = y - y0
                yy = y0
                above = self._spire_ok(x, y0)
                if n % 2 and above and n > 1:
                    # a young fir whose top pokes onto the grass above the wood
                    self.set(x, y0 - 1, *self.cat.cell("fir_young", 0, 0))
                    self.set(x, y0, *self.cat.cell("fir_young_shade", 0, 1))
                    yy += 1
                elif n % 2:
                    self.set(x, yy, SHADE, "X")
                    yy += 1
                while yy + 1 < y:
                    self.set(x, yy, *self.cat.cell("fir_young_shade", 0, 0))
                    self.set(x, yy + 1, *self.cat.cell("fir_young_shade", 0, 1))
                    yy += 2
                for yy in range(y0, y):
                    done.add((x, yy))
        for (x, y) in done:
            self.force_block.add((x, y))

    def _spire_ok(self, x, y0, cols=1):
        """Can a tree's top poke onto the cells above (x..x+cols-1, y0-1)?"""
        if y0 <= 0 or (y0 - 1) in self.aethos_rows:
            return False
        return all(self.at(xx, y0 - 1) == "." and (xx, y0 - 1) not in self.stamped
                   and self.mt[y0 - 1][xx] in (None, GRASS) for xx in range(x, x + cols))

    def _fir_run(self, x, y0, y1, done):
        n = y1 - y0 + 1
        for yy in range(y0, y1 + 1):
            done.add((x, yy))
            done.add((x + 1, yy))
        if n == 1:
            for xx in (x, x + 1):
                self.set(xx, y0, SHADE, "X")
            return
        if n == 2:
            for cy in range(2):
                for i in range(2):
                    self.set(x + i, y0 + cy, *self.cat.cell("oak_shade", i, cy))
            return
        kind = "fir" if hsh(x, y0, self.seed + 1) < 62 else "fir_b"
        stack = "fir_stack" if kind == "fir" else "fir_stack_b"
        # the first spire goes on the grass above the woods when it can
        above_ok = self._spire_ok(x, y0, 2)
        t = y0 - 1 if (above_ok and (y1 - (y0 - 1)) % 2 == 0) else (y0 if (y1 - y0) % 2 == 0 else y0 + 1)
        for yy in range(y0, t):
            for xx in (x, x + 1):          # a leftover row on top: the woods' shade
                self.set(xx, yy, SHADE, "X")
        if t >= 0:
            for i, xx in enumerate((x, x + 1)):
                self.set(xx, t, *self.cat.cell(kind if t < y0 else kind + "_shade", i, 0))
        r = t + 1
        while r + 1 <= y1:
            for i, xx in enumerate((x, x + 1)):
                self.set(xx, r, *self.cat.cell(kind + "_shade", i, 1))
                last = r + 2 > y1 - 1
                if last:
                    self.set(xx, r + 1, *self.cat.cell(kind + "_shade", i, 2))
                else:
                    self.set(xx, r + 1, *self.cat.cell(stack + "_shade", i, 0))
            r += 2

    # --- output ------------------------------------------------------------
    def check_seams(self):
        errs = []
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                if y in self.aethos_rows and m >= 0x200:
                    errs.append(f"{self.name} ({x},{y}): 0x{m:03X} in an aethos-only seam row")
                if y in self.core_rows and m >= 0x200 and m not in self.cat.core_ids:
                    errs.append(f"{self.name} ({x},{y}): 0x{m:03X} is not core in a core-only seam row")
        return errs

    def collision(self, x, y):
        if (x, y) in self.force_open:
            return 0
        if (x, y) in self.force_block:
            return 1
        return 1 if self.walkc[y][x] in ("X", "J") else 0

    def blocks(self):
        b = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                assert m is not None, (self.name, x, y)
                if (x, y) in self.water_cells:
                    b[y, x] = m | (1 << 12)
                elif self.collision(x, y):
                    b[y, x] = m | (1 << 10)
                else:
                    b[y, x] = m | (3 << 12)
        return b


# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------

def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
        local_id=None, rx=0, ry=0, item=None):
    e = {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
         "movement_range_x": rx, "movement_range_y": ry,
         "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
         "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag}
    if local_id:
        e = {"local_id": local_id, **e}
    return e


def item_ball(x, y, item, flag):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag, item=item)


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def trigger(x, y, script, var="VAR_TEMP_1", value="0"):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": value,
            "script": script}


def warp(x, y, dest, dest_warp):
    return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dest_warp)}


# --------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------

def write_layout(layout_id, folder, m, border, primary="gTileset_Aethos"):
    d = ROOT / "data/layouts" / folder
    d.mkdir(parents=True, exist_ok=True)
    m.blocks().tofile(d / "map.bin")
    np.array(border, "<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == layout_id:
            lay.update({"width": m.w, "height": m.h, "primary_tileset": primary,
                        "secondary_tileset": SETS[m.setname][0]})
            break
    else:
        sys.exit(f"no layout {layout_id}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_events(folder, events, music=None, extra=None):
    path = ROOT / "data/maps" / folder / "map.json"
    mp = json.loads(path.read_text())
    if music:
        mp["music"] = music
    mp.update(events)
    if extra:
        mp.update(extra)
    path.write_text(json.dumps(mp, indent=2, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# Rendering and checks
# --------------------------------------------------------------------------

def renderer(secondary):
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                           rm.Tileset(rm.resolve_tileset(secondary, syms)))


def render(m, events, border, views, tag=""):
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer(SETS[m.setname][0])
    RENDER.mkdir(parents=True, exist_ok=True)
    blocks = m.blocks()
    img = rm.render_blocks(r, blocks.ravel(), m.w)
    plain = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
    plain.save(RENDER / f"{m.name}{tag}.png")
    s = 3
    rev = img.resize((img.width * s, img.height * s), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", rev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    font = ImageFont.load_default(size=11)
    cell = 16 * s
    for y in range(m.h):
        for x in range(m.w):
            if (x, y) in m.water_cells:
                continue
            if m.collision(x, y):
                d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=(255, 0, 0, 55))
    colors = {"sign": (255, 220, 0), "hidden_item": (0, 220, 120), "trigger": (255, 0, 255)}
    for e in events.get("object_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 4, y * cell + 4, x * cell + cell - 5, y * cell + cell - 5], outline=(40, 80, 255), width=3)
        label = e["script"].split("_")[-1] if e["script"] != "Common_EventScript_FindItem" else e["trainer_sight_or_berry_tree_id"][5:]
        d.text((x * cell + 2, y * cell + 2), label[:8], fill=(255, 255, 255, 255), font=font, stroke_width=2,
               stroke_fill=(0, 0, 0, 255))
    for e in events.get("bg_events", []) + events.get("coord_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 10, y * cell + 10, x * cell + cell - 11, y * cell + cell - 11],
                    outline=colors[e["type"]], width=3)
    for e in events.get("warp_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 14, y * cell + 14, x * cell + cell - 15, y * cell + cell - 15],
                    outline=(0, 255, 255), width=4)
    for i in range(max(m.w, m.h)):
        if i < m.w:
            d.text((i * cell + cell // 2 - 6, 0), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2,
                   stroke_fill=(0, 0, 0, 255))
        if i < m.h:
            d.text((2, i * cell + cell // 2 - 6), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2,
                   stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(rev, over).convert("RGB").save(RENDER / f"{m.name}{tag}_review.png")
    # 15 x 10 screens at the given player positions, the border past the edges
    pad = 8
    W, H = m.w + 2 * pad, m.h + 2 * pad
    big = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            big[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
    big[pad:pad + m.h, pad:pad + m.w] = blocks & 0x3FF
    full = rm.render_blocks(r, big.ravel(), W)
    shots = []
    for (px, py) in views:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16 + 8
        shots.append(full.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
    if shots:
        cols = 3
        nrows = (len(shots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 488 + 8, nrows * 328 + 8), (24, 24, 32))
        for i, sh in enumerate(shots):
            sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
        sheet.save(RENDER / f"{m.name}{tag}_screens.png")
    return plain


def reach(m, starts, blocked_extra=()):
    """Cells reachable on foot from the starts (ledges hop south)."""
    blocked_extra = set(blocked_extra)
    ok = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and not m.collision(x, y) and \
        (x, y) not in m.water_cells and (x, y) not in blocked_extra
    seen = set(s for s in starts if ok(*s))
    dq = deque(seen)
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < m.w and 0 <= ny < m.h and m.walkc[ny][nx] == "J" and dy == 1:
                ny += 1
            if ok(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                dq.append((nx, ny))
    return seen


def grass_cells(m):
    return {(x, y) for y in range(m.h) for x in range(m.w) if m.walkc[y][x] == "G"}
