#!/usr/bin/env python3
"""Build Trophonios's cave: MAP_TROPHONIOS_CAVE_B1F and _B2F (SCRIPT.md Part 5).

Each floor is an ASCII grid, auto-tiled from gTileset_Trophonios's catalog
(build/trophonios/catalog.json, written by tools/ichor/art/trophonios_build.py):

  #  rock: the cap above, a face along every south edge (2 tall, 1 where the
     rock is only 2 deep)                          %  cliff rock: a free face, as
     tall as the run (the upper chamber's drop)    .  floor   ,  damp floor
  p  the priests' paving                           ~  the stream (blocked)
  =  the ford (shallow, walkable)                  _  a ledge, hopped south
  ^  a stalagmite    !  two    b  a boulder        s  scree (walkable)
  @  under a stamp (set in code)

Writes each floor's layout (map.bin, border.bin, layouts.json's entry), its
map.json events, and renders to build/render/trophonios/: the plain 2x map
(also copied to design/phase3/img/<Map>.png), a review with collision and
events, screens along the route, and dark screens with the torch's circle.

Usage: /usr/bin/python3 tools/ichor/maps/trophonios.py [--shapes] [--no-write]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/trophonios/catalog.json"
SHAPES = ROOT / "tools/ichor/art/trophonios_shapes.json"
LAYOUTS = ROOT / "data/layouts/layouts.json"
RENDER = ROOT / "build/render/trophonios"
IMG = ROOT / "design/phase3/img"
SYMBOL = "gTileset_Trophonios"

NEIGH = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
ROCK = set("#%")


def hsh(x, y, salt=0):
    h = (x * 73856093 ^ y * 19349663 ^ salt * 83492791) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h >> 8) % 100


def blob_key(inside, x, y):
    b = [1 if inside(x + dx, y + dy) else 0 for dx, dy in NEIGH]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)


class Catalog:
    def __init__(self):
        if not CAT.exists():
            sys.exit(f"{CAT} is missing: run /usr/bin/python3 tools/ichor/art/trophonios_build.py")
        self.s = {d["key"]: d for d in json.loads(CAT.read_text())["structures"]}

    def cell(self, key, cx, cy):
        d = self.s[key]
        return d["ids"][cy][cx], d["walk"][cy][cx]

    def named(self, key, name):
        d = self.s[key]
        if name not in d["names"]:
            return None
        cx, cy = d["names"][name]
        return self.cell(key, cx, cy)


class Floor:
    def __init__(self, name, rows, cat=None):
        self.name = name
        self.h, self.w = len(rows), len(rows[0])
        for y, r in enumerate(rows):
            assert len(r) == self.w, (name, y, len(r))
        self.ch = [list(r) for r in rows]
        self.cat = cat
        self.mt = [[None] * self.w for _ in range(self.h)]
        self.walk = [["."] * self.w for _ in range(self.h)]
        self.beh = {}
        self.water = set()
        self.stamped = set()
        self.decor = {}          # (x, y) -> (key, name): named pieces put after auto-tiling
        self.face_info = {}      # (x, y) -> (H, r, top, end)
        self.used = {"cap": set(), "face": set(), "water": set()}
        self.missing = []
        self.extra_water = set()  # cells that count as water for the banks (outlets, sinks)

    # --- grid ---------------------------------------------------------------
    def at(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.ch[y][x]
        return "#"

    def rock(self, x, y):
        return self.at(x, y) in ROCK

    # --- the walls ------------------------------------------------------------
    def classify(self):
        """Face or cap for every rock cell: (H, r, top, end) for faces."""
        for x in range(self.w):
            y = 0
            while y < self.h:
                if not self.rock(x, y):
                    y += 1
                    continue
                y0 = y
                while y < self.h and self.rock(x, y):
                    y += 1
                y1 = y - 1                       # last rock cell of the run
                if y1 == self.h - 1:
                    continue                     # runs off the bottom edge: all cap
                run = y1 - y0 + 1
                cliff = self.at(x, y1) == "%"
                free_above = y0 > 0 and not self.rock(x, y0 - 1)
                if cliff:
                    H, top = min(run, 3), "f"
                elif run >= 3 or (y0 == 0 and run >= 2):
                    H, top = 2, "c"
                elif run == 2:
                    H, top = (1, "c")
                else:
                    H, top = 1, "f"
                if cliff and run > 3:
                    top = "c"
                if not cliff and run == 2 and not free_above:
                    H, top = 2, "c"
                for r in range(H):
                    yy = y1 - (H - 1) + r
                    self.face_info[(x, yy)] = [H, r, top, None]
        for (x, y), info in self.face_info.items():
            wv = self.rock(x - 1, y)
            ev = self.rock(x + 1, y)
            info[3] = "M" if (wv and ev) else ("E" if wv else ("W" if ev else "B"))

    # --- auto-tiling -------------------------------------------------------------
    def shape(self, kind, key, variant=0):
        self.used[kind].add(key)
        if self.cat is None:
            return 0x200, "X"
        got = self.cat.named(kind, f"{key}~{variant}") if variant else None
        got = got or self.cat.named(kind, key)
        if got is None:
            self.missing.append((self.name, kind, key))
            got = self.cat.named(kind, "1|11111111" if kind != "face" else "20cM") or (0x200, "X")
        return got

    def autotile(self):
        self.classify()
        rock = lambda x, y: self.rock(x, y)
        water = lambda x, y: self.at(x, y) in "~=" or (x, y) in self.extra_water
        pave = lambda x, y: self.at(x, y) == "p"
        for y in range(self.h):
            for x in range(self.w):
                c = self.ch[y][x]
                if c in ROCK:
                    if (x, y) in self.face_info:
                        H, r, top, end = self.face_info[(x, y)]
                        self.set(x, y, *self.shape("face", f"{H}{r}{top}{end}",
                                                   hsh(x, 0, 21) % 3 if end == "M" else 0))
                    else:
                        k = blob_key(rock, x, y)
                        self.set(x, y, *self.shape("cap", k, hsh(x, y, 13) % 3 if k == "1|11111111" else 0))
                elif c == "~":
                    self.set(x, y, *self.shape("water", blob_key(water, x, y)))
                    self.water.add((x, y))
                elif c == "=":
                    n, s_ = water(x, y - 1), water(x, y + 1)
                    name = "one" if not (n or s_) else ("top" if not n else ("bot" if not s_ else "stones"))
                    self.set(x, y, *self.named("ford", name))
                elif c == "p":
                    n, s_, w_, e = pave(x, y - 1), pave(x, y + 1), pave(x - 1, y), pave(x + 1, y)
                    v = "t" if not n else ("b" if not s_ else "")
                    hz = "l" if not w_ else ("r" if not e else "")
                    k = (v + hz) or ("c" if hsh(x, y, 4) < 70 else ("c2" if hsh(x, y, 5) < 60 else "c3"))
                    self.set(x, y, *self.named("pave", k))
                elif c in ".,s@O":
                    self.floor(x, y, c)
                elif c == "_":
                    l, r_ = self.at(x - 1, y) == "_", self.at(x + 1, y) == "_"
                    self.set(x, y, *self.named("ledge", "M" if (l and r_) else ("W" if r_ else ("E" if l else "M"))))
                elif c in "^!b":
                    self.set(x, y, *self.named("rocks", {"^": "stal", "!": "stal_pair", "b": "boulder"}[c]))
                else:
                    raise ValueError(f"{self.name}: unknown ground {c!r} at {x},{y}")
        for (x, y), (key, name) in self.decor.items():
            self.set(x, y, *self.named(key, name))

    def floor(self, x, y, c):
        above = self.face_info.get((x, y - 1))
        if above and above[1] == above[0] - 1 and self.rock(x, y - 1):
            end = above[3]
            if end == "M":
                name = ("sh", "sh_b", "sh_c")[hsh(x, y, 3) % 3]
            else:
                name = {"W": "shW", "E": "shE", "B": "shB"}[end]
            self.set(x, y, *self.named("floor", name))
            return
        if c == ",":
            self.set(x, y, *self.named("floor", "damp"))
        elif c == "s":
            self.set(x, y, *self.named("rocks", "scree"))
        else:
            h = hsh(x, y, 7)
            pick = [(8, "pebbles"), (12, "crack"), (17, "gravel"), (21, "flat"), (55, "plain_b"),
                    (78, "plain_c"), (101, "plain")]
            self.set(x, y, *self.named("floor", next(n for lim, n in pick if h < lim)))

    def named(self, key, name):
        if self.cat is None:
            return 0x200, "."
        got = self.cat.named(key, name)
        assert got is not None, (self.name, key, name)
        return got

    def set(self, x, y, mid, walk):
        self.mt[y][x] = mid
        self.walk[y][x] = walk

    def put(self, x, y, key, name):
        """A named piece, placed after the auto-tiler (it wins over the ground)."""
        self.decor[(x, y)] = (key, name)
        self.stamped.add((x, y))

    def stamp(self, key, x, y):
        d = self.cat.s[key] if self.cat else None
        if d is None:
            return
        for cy in range(d["h"]):
            for cx in range(d["w"]):
                inv = {tuple(v): k for k, v in d["names"].items()}
                self.put(x + cx, y + cy, key, inv[(cx, cy)])

    def face_at(self, x, y):
        return self.face_info.get((x, y))

    # --- output ----------------------------------------------------------------
    def collision(self, x, y):
        return 1 if self.walk[y][x] in ("X",) else 0

    def blocks(self):
        b = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                m = self.mt[y][x]
                assert m is not None, (self.name, x, y)
                if self.walk[y][x] == "X":
                    b[y, x] = m | (1 << 10) | (3 << 12)
                else:
                    b[y, x] = m | (3 << 12)
        return b


def renderer():
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    sec = rm.resolve_tileset(SYMBOL, syms) if SYMBOL in syms else rm.resolve_tileset("trophonios", syms)
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)), rm.Tileset(sec))


def render(m, events, views, tag=""):
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer()
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
            if m.collision(x, y):
                d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=(255, 0, 0, 45))
    colors = {"sign": (255, 220, 0), "hidden_item": (0, 220, 120), "trigger": (255, 0, 255)}
    for e in events.get("object_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 4, y * cell + 4, x * cell + cell - 5, y * cell + cell - 5], outline=(40, 80, 255), width=3)
        label = e["script"].split("_")[-1] if e["script"] != "Common_EventScript_FindItem" \
            else e["trainer_sight_or_berry_tree_id"][5:]
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
    # 15 x 10 screens along the route, lit and by torchlight (radius 56 px)
    pad = 8
    W, H = m.w + 2 * pad, m.h + 2 * pad
    border = border_ids(m)
    big = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            big[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
    big[pad:pad + m.h, pad:pad + m.w] = blocks & 0x3FF
    full = rm.render_blocks(r, big.ravel(), W)
    shots, darks = [], []
    yy, xx = np.mgrid[0:160, 0:240]
    circle = ((xx - 120 + 0.5) ** 2 + (yy - 80 - 8 + 0.5) ** 2) <= 56 ** 2
    for (px, py) in views:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16 + 8
        sh = full.crop((x0, y0, x0 + 240, y0 + 160))
        shots.append(sh.resize((480, 320), Image.NEAREST))
        a = np.array(sh.convert("RGB"))
        a[~circle] = 0
        darks.append(Image.fromarray(a).resize((480, 320), Image.NEAREST))
    for name, lst in (("screens", shots), ("dark", darks)):
        if not lst:
            continue
        cols = 3
        nrows = (len(lst) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 488 + 8, nrows * 328 + 8), (24, 24, 32))
        for i, sh in enumerate(lst):
            sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
        sheet.save(RENDER / f"{m.name}{tag}_{name}.png")
    return plain


def border_ids(m):
    mid = m.cat.named("cap", "1|11111111")[0]
    return [mid, mid, mid, mid]


def reach(m, starts, blocked=()):
    blocked = set(blocked)
    ok = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and not m.collision(x, y) and (x, y) not in blocked
    seen = set(s for s in starts if ok(*s))
    dq = deque(seen)
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < m.w and 0 <= ny < m.h and m.walk[ny][nx] == "J" and dy == 1:
                ny += 1
            if ok(nx, ny) and (nx, ny) not in seen:
                seen.add((nx, ny))
                dq.append((nx, ny))
    return seen




# --------------------------------------------------------------------------
# The floors, carved out of solid rock
# --------------------------------------------------------------------------

def grid(w, h):
    return [["#"] * w for _ in range(h)]


def carve(g, x0, y0, x1, y1, c="."):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[y][x] = c


def cells(g, pts, c):
    for (x, y) in pts:
        g[y][x] = c


P = "OBJ_EVENT_GFX_ICHOR_"
B1 = "TrophoniosCave_B1F_EventScript_"
B2 = "TrophoniosCave_B2F_EventScript_"

# Fixed points the scripts and the test share (scripts.pory and the test repeat them).
B1F_GRILLE = (9, 3)          # warp 0: the steps under the grille, out to Lebadeia's warp 3
B1F_THRONE = (12, 5)         # the seat of the throne of Mnemosyne (beat 35C)
B1F_STAIR = (27, 21)         # warp 1: down to B2F
B1F_LADDER_X = 9
B1F_BRAZIER = (14, 13)       # its top cell; the tripod below
B2F_STAIR = (3, 2)           # warp 0: up to B1F
B2F_CLEFT = (20, 11)
B2F_BRAZIER = (10, 14)
B2F_HOLE = (6, 16)           # top-left of the 2 x 2 hole


def b1f_grid():
    g = grid(30, 24)
    # the upper chamber inside the grille: paved, lit by the day through the bars
    carve(g, 5, 4, 13, 4)
    carve(g, 4, 5, 14, 6)
    carve(g, 5, 7, 13, 7)
    carve(g, 6, 8, 12, 8)
    carve(g, 6, 5, 11, 7, "p")
    # the cliff it stands on, three tall (the ladder at x 9)
    carve(g, 6, 9, 12, 11, "%")
    # the stream chamber: the north bank
    carve(g, 2, 12, 24, 14)
    cells(g, [(1, 13), (25, 14), (16, 11), (17, 11)], ".")
    # the underground Herkyna, from its outlet in the east wall to its sink in the west
    carve(g, 2, 15, 26, 16, "~")
    carve(g, 23, 14, 25, 14, "~")          # wider where it comes out of the rock
    # the north wall bulges into the bank here and there
    cells(g, [(2, 12), (21, 12), (22, 12)], "#")
    cells(g, [(1, 15)], "~")
    carve(g, 19, 15, 20, 16, "=")
    # the south bank, and a deep pool where the stream bends below the brazier
    carve(g, 4, 17, 25, 17)
    carve(g, 10, 17, 13, 17, "~")
    # west: the rubble passage to the Max Repel's nook
    carve(g, 4, 18, 4, 19)
    carve(g, 2, 20, 4, 21)
    # south of the pool: a room round an outcrop, open to the bank on both sides
    carve(g, 7, 18, 16, 21)
    carve(g, 10, 19, 12, 20, "#")
    # east: down to Philomelos's corridor and the stair
    carve(g, 22, 18, 23, 20)
    carve(g, 20, 21, 27, 21)
    # texture: stalagmites, scree, damp
    cells(g, [(3, 12), (23, 12), (8, 21), (15, 19)], "^")
    cells(g, [(17, 12), (14, 21)], "!")
    cells(g, [(6, 13)], "b")               # a block fallen from the cliff, by the ladder's foot
    cells(g, [(24, 17), (2, 14), (3, 20), (7, 19), (5, 12), (7, 12), (19, 13), (20, 13)], "s")
    cells(g, [(10, 14), (16, 14), (21, 17), (9, 18), (13, 18)], ",")
    return g


def b2f_grid():
    g = grid(26, 22)
    # the stair up, the spring, the long passage east: forks A (7) and B (17)
    carve(g, 2, 3, 24, 4)
    cells(g, [(13, 3), (21, 3)], "#")      # the north wall juts into the passage
    # fork A's wrong branch: a loop round a pillar, back to the start
    carve(g, 2, 5, 2, 8)
    carve(g, 7, 5, 7, 8)
    carve(g, 2, 8, 7, 8)
    # fork B: east to a dead end (the Max Ether); south is the way on
    carve(g, 22, 5, 24, 6)
    carve(g, 17, 5, 17, 10)
    # the web den, west of the way on, behind its curtain (16, 8)
    carve(g, 10, 7, 15, 9)
    cells(g, [(16, 8)], ".")
    # fork C: ahead to a dead end (the Hyper Potion); left past the snake's cleft
    carve(g, 17, 11, 19, 11)
    carve(g, 17, 12, 17, 13)
    cells(g, [B2F_CLEFT], ".")
    # the black pool's round chamber
    carve(g, 21, 10, 22, 10)
    carve(g, 21, 11, 24, 11)
    carve(g, 20, 12, 24, 15)
    carve(g, 21, 12, 23, 14, "O")
    # the great boulder's niche, west of the pool, and the dig behind it
    cells(g, [(19, 14), (18, 14)], ".")
    # down to the oracle's chamber
    carve(g, 22, 16, 23, 16)
    carve(g, 12, 17, 23, 17)
    # the oracle's chamber: round, at the very bottom; the ledge with the TM
    carve(g, 5, 13, 9, 13)                 # the shelf, a step up, with the TM
    carve(g, 4, 14, 10, 14)
    carve(g, 5, 14, 8, 14, "_")
    carve(g, 3, 15, 11, 17)
    carve(g, 4, 18, 10, 18)
    carve(g, 5, 19, 9, 19)
    # texture
    cells(g, [(13, 9), (24, 3)], "^")
    cells(g, [(11, 3), (22, 10)], "!")
    cells(g, [(5, 8), (14, 17), (11, 4), (15, 3), (23, 5)], "s")
    cells(g, [(19, 4), (3, 7), (22, 15)], ",")
    return g


def as_rows(g):
    return ["".join(r) for r in g]


# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------

def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", trainer=False, sight=0,
        local_id=None, item=None):
    e = {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
         "movement_range_x": 0, "movement_range_y": 0,
         "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
         "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag}
    if local_id:
        e = {"local_id": local_id, **e}
    return e


def item_ball(x, y, item, flag):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag, item=item)


def sign(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag}


def trigger(x, y, script, var="VAR_TEMP_9", value="0"):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": value,
            "script": script}


def warp(x, y, dest, dest_warp):
    return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dest_warp)}


def build_b1f(cat):
    m = Floor("TrophoniosCave_B1F", as_rows(b1f_grid()), cat)
    m.extra_water |= {(26, 14)}
    # the north wall of the upper chamber: tablets, lamps, the grille
    gx, gy = B1F_GRILLE
    m.put(gx, gy - 1, "grille", "arch")
    m.put(gx, gy, "grille", "steps")
    m.put(6, 3, "tablets", "a")
    m.put(7, 3, "lamp", "lamp")
    m.put(11, 3, "lamp", "lamp")
    m.put(13, 3, "tablets", "b")
    tx, ty = B1F_THRONE
    m.put(tx, ty - 1, "throne", "back")
    m.put(tx, ty, "throne", "seat")
    m.put(5, 4, "offerings", "bread")
    m.put(4, 5, "offerings", "cakes")
    m.put(13, 6, "offerings", "crumbs")
    # the ladder down the cliff
    lx = B1F_LADDER_X
    m.put(lx, 8, "ladder", "stakes")
    m.put(lx, 9, "ladder", "top")
    m.put(lx, 10, "ladder", "mid")
    m.put(lx, 11, "ladder", "foot")
    # brazier 1 by the stream; the first chalk hand on the wall past it
    bx, by = B1F_BRAZIER
    m.put(bx, by, "brazier", "cold_top")
    m.put(bx, by + 1, "brazier", "cold")
    m.put(18, 11, "prints", "E")
    # the stream's ends
    m.put(26, 14, "outlet", "outlet")
    m.put(1, 15, "sink", "sink")
    # the stair down
    m.put(*B1F_STAIR, "stairs", "down")
    m.put(4, 21, "lair", "bones")
    events = {
        "object_events": [
            obj(P + "MAN", 20, 21, B1 + "Philomelos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3,
                local_id="LOCALID_TROPHONIOS_PHILOMELOS"),
            # ICHOR_STUB_AETHOS_DEX: the Halcyling's sprite is its stand-in species' until the dex lands
            obj("OBJ_EVENT_GFX_SPECIES(HALCYLING)", 15, 15, B1 + "Goose", "MOVEMENT_TYPE_LOOK_AROUND",
                flag="FLAG_ICHOR_FOUND_HERKYNAS_GOOSE", local_id="LOCALID_TROPHONIOS_GOOSE"),
            obj("OBJ_EVENT_GFX_BREAKABLE_ROCK", 4, 19, "EventScript_RockSmash", flag="FLAG_TEMP_12",
                local_id="LOCALID_TROPHONIOS_RUBBLE"),
            item_ball(8, 13, "ITEM_ESCAPE_ROPE", "FLAG_ICHOR_ITEM_TROPHONIOS_B1F_ESCAPE_ROPE"),
            item_ball(2, 21, "ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_TROPHONIOS_B1F_MAX_REPEL"),
            # the reading (beat 35C): hidden by FLAG_TEMP_11 unless the player comes up on the throne
            obj(P + "SAON", 12, 7, B1 + "Saon", "MOVEMENT_TYPE_FACE_UP", flag="FLAG_TEMP_11",
                local_id="LOCALID_TROPHONIOS_SAON"),
            obj(P + "TROPHONIAN_PRIEST", 11, 7, B1 + "Priest", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_TEMP_11", local_id="LOCALID_TROPHONIOS_PRIEST"),
            obj(P + "ALETHEA", 14, 6, B1 + "Alethea", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_TEMP_11",
                local_id="LOCALID_TROPHONIOS_ALETHEA"),
        ],
        "warp_events": [
            warp(*B1F_GRILLE, "MAP_LEBADEIA", 3),
            warp(*B1F_STAIR, "MAP_TROPHONIOS_CAVE_B2F", 0),
        ],
        "coord_events": [
            trigger(lx, 12, B1 + "LadderFoot", "VAR_TEMP_1", "0"),
            # the lit zone: the stream chamber (brazier 1)
            trigger(lx, 9, B1 + "LeaveStream"),
            trigger(lx, 10, B1 + "EnterStream"),
            trigger(4, 17, B1 + "EnterStream"),
            trigger(4, 18, B1 + "LeaveStream"),
            trigger(22, 17, B1 + "EnterStream"),
            trigger(23, 17, B1 + "EnterStream"),
            trigger(22, 18, B1 + "LeaveStream"),
            trigger(23, 18, B1 + "LeaveStream"),
        ],
        "bg_events": [
            sign(6, 3, B1 + "Tablets"), sign(13, 3, B1 + "Tablets"),
            sign(7, 3, B1 + "Lamp"), sign(11, 3, B1 + "Lamp"),
            sign(tx, ty - 1, B1 + "Throne"),
            sign(5, 4, B1 + "Bread"), sign(4, 5, B1 + "Cakes"),
            sign(bx, by, B1 + "Brazier"), sign(bx, by + 1, B1 + "Brazier"),
            sign(18, 11, B1 + "Handprint"),
            hidden(8, 16, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_TROPHONIOS_B1F_BRONZE_OBOL"),
            hidden(13, 4, "ITEM_HONEY", "FLAG_ICHOR_HIDDEN_TROPHONIOS_B1F_HONEY"),
        ],
    }
    return m, events


def build_b2f(cat):
    m = Floor("TrophoniosCave_B2F", as_rows(b2f_grid()), cat)
    sx, sy = B2F_STAIR
    m.put(sx, sy - 1, "stairs", "up_arch")
    m.put(sx, sy, "stairs", "up")
    m.put(5, 2, "spring", "seep")
    m.put(5, 3, "spring", "basin")
    # the forks' chalk hands, on the right way, and the floor's
    m.put(9, 2, "prints", "E")
    m.put(17, 2, "prints", "S")
    m.put(18, 10, "prints", "E")
    m.put(8, 4, "prints", "fE")
    m.put(17, 6, "prints", "fS")
    # the web den
    m.put(15, 6, "lair", "web_face")
    m.put(10, 6, "lair", "web_face")
    m.put(12, 8, "lair", "strands")
    m.put(14, 9, "lair", "bones")
    # the snake's cleft
    m.put(*B2F_CLEFT, "cleft", "coils")
    # the black pool
    for yy in range(3):
        for xx in range(3):
            m.put(21 + xx, 12 + yy, "pool", f"{xx}{yy}")
    # the dig behind the great boulder
    m.put(18, 14, "dig", "dig")
    # the oracle's chamber: brazier 2, the hole, offerings by it
    bx, by = B2F_BRAZIER
    m.put(bx, by, "brazier", "cold_top")
    m.put(bx, by + 1, "brazier", "cold")
    hx, hy = B2F_HOLE
    for (dx, dy, n) in ((0, 0, "tl"), (1, 0, "tr"), (0, 1, "bl"), (1, 1, "br")):
        m.put(hx + dx, hy + dy, "hole", n)
    m.put(9, 18, "offerings", "cakes")
    m.put(4, 18, "offerings", "bread")
    pool = [sign(21 + xx, 12 + yy, B2 + "BlackPool") for yy in range(3) for xx in range(3)]
    events = {
        "object_events": [
            obj(P + "AUGUR", 20, 12, B2 + "Melampos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3,
                local_id="LOCALID_TROPHONIOS_MELAMPOS"),
            obj(P + "AUGUR", B2F_CLEFT[0], B2F_CLEFT[1], B2 + "Snake", "MOVEMENT_TYPE_INVISIBLE",
                flag="FLAG_ICHOR_TROPHONIOS_SNAKE_FED", local_id="LOCALID_TROPHONIOS_SNAKE"),
            obj(P + "COBWEB", 16, 8, "EventScript_IchorCobweb", flag="FLAG_TEMP_13", local_id="LOCALID_TROPHONIOS_COBWEB"),
            obj(P + "GREAT_BOULDER", 19, 14, "EventScript_IchorGreatBoulder",
                flag="FLAG_ICHOR_HIDE_TROPHONIOS_GREAT_BOULDER", local_id="LOCALID_TROPHONIOS_GREAT_BOULDER"),
            item_ball(24, 6, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_TROPHONIOS_B2F_MAX_ETHER"),
            item_ball(11, 8, "ITEM_SPELL_TAG", "FLAG_ICHOR_ITEM_TROPHONIOS_B2F_SPELL_TAG"),
            item_ball(17, 13, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_TROPHONIOS_B2F_HYPER_POTION"),
            # ICHOR_STUB_TMS: Future Sight has no TM number yet; Skill Swap stands in
            item_ball(5, 13, "ITEM_TM_SKILL_SWAP", "FLAG_ICHOR_ITEM_TROPHONIOS_B2F_TM_FUTURE_SIGHT"),
        ],
        "warp_events": [
            warp(sx, sy, "MAP_TROPHONIOS_CAVE_B1F", 1),
        ],
        "coord_events": [
            trigger(11, 17, B2 + "EnterOracle"),
            trigger(12, 17, B2 + "LeaveOracle"),
        ],
        "bg_events": [
            sign(5, 2, B2 + "Spring"), sign(5, 3, B2 + "Spring"),
            sign(9, 2, B2 + "HandprintA"), sign(17, 2, B2 + "HandprintB"), sign(18, 10, B2 + "HandprintC"),
            *pool,
            sign(18, 14, B2 + "DigSpot"),
            sign(bx, by, B2 + "Brazier"), sign(bx, by + 1, B2 + "Brazier"),
            *[sign(hx + dx, hy + dy, B2 + "Hole") for dy in range(2) for dx in range(2)],
            sign(9, 18, B2 + "Cakes"), sign(4, 18, B2 + "Bread"),
            hidden(2, 8, "ITEM_ETHER", "FLAG_ICHOR_HIDDEN_TROPHONIOS_B2F_ETHER"),
            hidden(24, 13, "ITEM_DUSK_STONE", "FLAG_ICHOR_HIDDEN_TROPHONIOS_B2F_DUSK_STONE"),
        ],
    }
    return m, events


# --------------------------------------------------------------------------
# Writing, rendering, checking
# --------------------------------------------------------------------------

FLOORS = {
    "TrophoniosCave_B1F": ("LAYOUT_TROPHONIOS_CAVE_B1F", build_b1f,
                           [(9, 4), (12, 6), (9, 13), (15, 13), (20, 17), (24, 21), (5, 19)]),
    "TrophoniosCave_B2F": ("LAYOUT_TROPHONIOS_CAVE_B2F", build_b2f,
                           [(4, 4), (12, 5), (17, 8), (13, 8), (21, 13), (8, 16)]),
}


def write_shapes():
    used = {"cap": set(), "face": set(), "water": set()}
    for name, (_, build, _) in FLOORS.items():
        m, _ = build(None)
        m.autotile()
        for k in used:
            used[k] |= m.used[k]
    SHAPES.write_text(json.dumps({k: sorted(v) for k, v in used.items()}, indent=1) + "\n")
    print(SHAPES.relative_to(ROOT), {k: len(v) for k, v in used.items()})


def write_layout(layout_id, folder, m):
    d = ROOT / "data/layouts" / folder
    d.mkdir(parents=True, exist_ok=True)
    m.blocks().tofile(d / "map.bin")
    border = border_ids(m)
    np.array([b | (1 << 10) | (3 << 12) for b in border], "<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == layout_id:
            lay.update({"width": m.w, "height": m.h, "primary_tileset": "gTileset_Aethos",
                        "secondary_tileset": SYMBOL})
            break
    else:
        sys.exit(f"no layout {layout_id}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_events(folder, events):
    path = ROOT / "data/maps" / folder / "map.json"
    mp = json.loads(path.read_text())
    mp["music"] = "MUS_ICHOR_HOLLOW"       # ICHOR_STUB_MUSIC (scripts.pory says so too)
    mp["requires_flash"] = True
    mp["map_type"] = "MAP_TYPE_UNDERGROUND"
    mp["allow_escaping"] = True
    mp["show_map_name"] = False          # the section is Lebadeia's: no popup on the way down
    mp["battle_scene"] = "MAP_BATTLE_SCENE_NORMAL"
    for k in ("object_events", "warp_events", "coord_events", "bg_events"):
        mp[k] = events.get(k, [])
    path.write_text(json.dumps(mp, indent=2, ensure_ascii=False) + "\n")


def check(m, events, starts, must_reach, blocked=()):
    """Every listed cell reachable from the starts; returns the problems."""
    cleared = ("EventScript_RockSmash", "EventScript_IchorCobweb", B2 + "Snake")   # once the player clears them
    objs = {(e["x"], e["y"]) for e in events.get("object_events", [])
            if e["flag"] != "FLAG_TEMP_11" and e["graphics_id"] != "OBJ_EVENT_GFX_ITEM_BALL"
            and e["script"] not in cleared}
    seen = reach(m, starts, set(blocked) | objs)
    probs = []
    for name, cell in must_reach.items():
        adj = [(cell[0] + dx, cell[1] + dy) for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0))]
        if not any(a in seen for a in adj):
            probs.append(f"{m.name}: can't reach {name} at {cell}")
    return probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true", help="write the shapes the maps use, then stop")
    ap.add_argument("--no-write", action="store_true", help="render only")
    ap.add_argument("--tag", default="", help="suffix for the render files (a pass's name)")
    args = ap.parse_args()
    if args.shapes:
        write_shapes()
        return
    cat = Catalog()
    probs = []
    for folder, (layout, build, views) in FLOORS.items():
        m, events = build(cat)
        m.autotile()
        if m.missing:
            probs.append(f"missing shapes (rerun --shapes and the art build): {sorted(set(m.missing))[:12]}")
        if not args.no_write:
            write_layout(layout, folder, m)
            write_events(folder, events)
        plain = render(m, events, views, args.tag)
        if not args.no_write and not args.tag:
            plain.save(IMG / f"{folder}.png")
        if folder.endswith("B1F"):
            # snake-free: the reachability the player has with the Hammer (rubble gone)
            probs += check(m, events, [B1F_GRILLE], {
                "the ladder's foot": (9, 12), "the Escape Rope": (8, 13), "the brazier": (14, 14),
                "the goose (from the bank)": (15, 14), "the ford's far side": (19, 17),
                "Philomelos's sight": (22, 21), "the stair down": B1F_STAIR,
                "the Max Repel (Hammer)": (2, 21), "the throne": (12, 6), "the hidden honey": (13, 5)},
                blocked=[])
        else:
            probs += check(m, events, [(3, 3)], {
                "the spring": (5, 4), "fork B's Max Ether": (24, 6), "the web den (Torch)": (11, 8),
                "fork C's Hyper Potion": (17, 13), "the cleft": (19, 11),
                "the black pool's far rim": (24, 13), "the oracle's chamber": (6, 15),
                "the TM": (4, 13), "the hole": (6, 15), "fork A's loop": (2, 8)},
                blocked=[])
        print(m.name, f"{m.w}x{m.h}", "written" if not args.no_write else "rendered")
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)


if __name__ == "__main__":
    main()
