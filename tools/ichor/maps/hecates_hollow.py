#!/usr/bin/env python3
"""Hecate's Hollow: layout, events, scripts, checks and renders.

The cave under the pass of Mount Aigaleos, where the Sacred Way runs from Route 4
(the Isthmus) to Route 5 (the Skironian cliffs): beat 18 and Part 5's "Three
Roads" in design/phase2/SCRIPT.md, drawn with gTileset_CaveDark
(design/phase2/TILES_cave_dark.md) on aethos. It is dark ("cave": true): a tile
and a half of light without Hecate's Torch, three and a half with it.

  the east mouth   daylight from Route 4; the old woman and her covered dish; a
                   cobweb over a side tunnel (the shortcut, burnt on the way back)
  the dark road    three forks, each heard before it is seen: the dog barks left,
                   then right, then straight ahead. Fork 1's right is a loop past a
                   hidden Escape Rope; fork 2's left a dead end with the Bronze
                   Obol and a lost pilgrim; fork 3's left and right loop back
  the Hekataion    the round chamber where the three roads meet, lit faintly from
                   above: the three-faced pillar, its spring (the midpoint rest),
                   Hecate's supper in a niche. The payoff: the Torch
  the road west    behind a cobweb: two cold braziers (each lights its hall for
                   good), Hekabe by the first, Kallias in the dark of a side
                   passage, the web chamber behind a second cobweb, and the west
                   mouth's daylight with Battos and his goats
  the way back     from the Hekataion east, the shortcut tunnel to the east mouth
                   (its cobweb burns from the inside)

Lighting is a small state machine (SYSTEMS.md §2's lit zones): VAR_TEMP_2 holds
the region the player stands in (REGIONS below; 0 is the dark). Every cell on a
region's edge carries a trigger for each neighbouring region, so stepping across
an edge runs the new region's Enter script once, which sets the light: the
daylight full, the Hekataion faint (flash 2) until the Torch and full after, a
brazier's hall full once its brazier burns, the dark the Torch's own radius.

Writes:
  data/layouts/HecatesHollow/map.bin, border.bin   (48x40, aethos + cave_dark)
  data/maps/HecatesHollow/map.json                 its events, from the tables below
  data/maps/HecatesHollow/scripts.pory             the generated block between the markers
Checks: the forks lead only where SCRIPT.md says; before the Torch the cobwebs
shut the road west and the shortcut; every open cell reachable once they burn;
people, items and signs placed and reachable; Hekabe's sight cuts the only way
west; triggers on open cells; every setmetatile on the piece it swaps.
Renders, into --render DIR: hecates_hollow.png (2x, as first found, with people),
hecates_hollow_lit.png (cleared: webs burnt, braziers and torches lit),
hecates_hollow_dark.png (no Torch: the light the player sees on the dark road),
hecates_hollow_dark_torch.png (with the Torch, one brazier lit), and
hecates_hollow_events.png (collision, triggers, regions; for review).

Usage: /usr/bin/python3 tools/ichor/maps/hecates_hollow.py [--render DIR]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import cave_dark_kit as kit  # noqa: E402

CATALOG = ROOT / "data/tilesets/secondary/cave_dark/catalog.json"
NAME = "HecatesHollow"
MAP_ID = "MAP_HECATES_HOLLOW"
LAYOUT_ID = "LAYOUT_HECATES_HOLLOW"
MAP_DIR = ROOT / "data/maps" / NAME
LAYOUT_DIR = ROOT / "data/layouts" / NAME
PX = "HecatesHollow_EventScript_"

# ---------------------------------------------------------------------------
# The terrain, carved from shapes: '#' rock, '.' cave floor (MB_CAVE, with
# encounters), ',' lit floor (daylight at the mouths and the Hekataion's
# skylight: MB_NORMAL, no encounters). Chambers are ellipses whose radius wavers
# with the angle; passages are bands that bulge a cell here and there. Cells set
# last (FIX) pin what the scripts need: the cobwebs' one-wide necks, the mouths,
# the fork pillars and the ledge.
# ---------------------------------------------------------------------------
W, H = 48, 40


def _wave(t, s):
    """A smooth wobble in -1..1: two sines with their own phases."""
    import math
    return 0.6 * math.sin(3 * t + s) + 0.4 * math.sin(5 * t + 2.1 * s)


def _ellipse(g, cx, cy, rx, ry, ch=".", wob=0.10, s=0.0):
    import math
    for y in range(H):
        for x in range(W):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            r = 1 + wob * _wave(math.atan2(dy, dx), s)
            if dx * dx + dy * dy <= r * r:
                g[y][x] = ch


def _band(g, pts, w=2, ch=".", bulge=(), s=0.0):
    """Axis-aligned segments through pts, w cells wide (the band's top or left
    edge on the point). bulge: cells along the way that widen by one, given as
    (x, y) of the extra cell."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                for j in range(w):
                    g[y0 + j][x] = ch
        else:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for i in range(w):
                    g[y][x0 + i] = ch
    for (x, y) in bulge:
        g[y][x] = ch


def _roughen(g, s=0.0, keep=()):
    """Break up straight walls: a rock cell on a floor's edge opens where a slow
    noise runs high, if the two cells beyond it are rock (so passages never merge
    and every wall keeps its two-cell face). keep: rects (x0, y0, x1, y1) left alone."""
    import math

    def kept(x, y):
        return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in keep)
    opened = []
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            if g[y][x] != "#" or kept(x, y):
                continue
            n = math.sin(0.83 * x + 1.31 * y + s) * math.sin(0.61 * y - 0.47 * x + 2.0 * s)
            if n < 0.42:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if g[y + dy][x + dx] != "#":
                    bx, by = x - dx, y - dy
                    cx, cy = x - 2 * dx, y - 2 * dy
                    side = [(x - dy, y - dx), (x + dy, y + dx)]
                    if (0 <= cx < W and 0 <= cy < H and g[by][bx] == "#" and g[cy][cx] == "#"
                            and all(g[sy][sx] == "#" or (sx, sy) == (x + dx, y + dy) or g[sy][sx] != "#"
                                    for sx, sy in side)):
                        opened.append((x, y))
                    break
    for x, y in opened:
        g[y][x] = "."


def _tidy(g):
    """Smooth the carve: a lone rock cell in open floor opens up, and a floor stub
    poking into rock (open on one side only) fills in."""
    for _ in range(3):
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                n = sum(g[y + dy][x + dx] != "#" for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if g[y][x] == "#" and n >= 3:
                    g[y][x] = "."
                elif g[y][x] != "#" and n <= 1:
                    g[y][x] = "#"


def carve():
    g = [["#"] * W for _ in range(H)]
    # -- the Hekataion: the round chamber where the three roads meet --------------
    _ellipse(g, 25.0, 7.3, 9.8, 5.0, s=0.7)
    _ellipse(g, 25.0, 7.0, 5.4, 3.7, ch=",", wob=0.08, s=1.9)        # the skylight
    _band(g, [(24, 11), (24, 14)])                                    # south: the dark road
    _band(g, [(13, 8), (17, 8)])                                      # west: the road on
    _band(g, [(33, 6), (41, 6)], bulge=[(36, 8), (37, 8)])            # east: the shortcut
    # -- the road west: neck A, Hekabe's hall in two lobes, the stair to hall 2 ----
    _band(g, [(13, 10), (13, 12)], w=1)                               # neck A
    _ellipse(g, 12.3, 14.8, 2.6, 2.6, s=2.3)                          # the east lobe (entry)
    _ellipse(g, 4.3, 14.0, 3.2, 2.7, s=4.1)                           # the west lobe (brazier 1)
    _band(g, [(7, 14), (10, 14)], w=1)                                # the waist Hekabe watches
    _band(g, [(3, 16), (3, 21)], bulge=[(2, 19)])                     # down to hall 2
    _ellipse(g, 5.8, 5.2, 4.4, 2.3, s=3.3)                            # the web chamber
    _band(g, [(5, 8), (5, 11)], w=1)                                  # neck B
    # -- hall 2 (brazier 2), the west mouth, Kallias's pocket ------------------------
    _ellipse(g, 6.2, 26.2, 5.3, 4.2, s=5.2)
    _band(g, [(0, 25), (3, 25)], w=4)                                 # the west mouth
    _band(g, [(7, 30), (7, 32)])                                      # down to the pocket
    _ellipse(g, 7.6, 34.6, 4.4, 1.7, s=0.4)
    # -- fork 3 below the Hekataion: a round junction; the side ways are narrow loops
    #    that come back down to its approach --------------------------------------
    _ellipse(g, 24.6, 16.2, 3.4, 1.6, s=1.4)
    _band(g, [(19, 16), (21, 16)], w=1)
    _band(g, [(19, 16), (19, 21)], w=1)
    _band(g, [(19, 21), (24, 21)], w=1)
    _band(g, [(28, 16), (30, 16)], w=1)
    _band(g, [(30, 16), (30, 21)], w=1)
    _band(g, [(25, 21), (30, 21)], w=1)
    _band(g, [(24, 14), (24, 26)])                                    # the approach, ahead
    # -- fork 2: right is the way on, left a dead end -------------------------------
    _ellipse(g, 19.0, 26.0, 2.2, 1.5, s=1.1)                          # the junction
    _band(g, [(20, 26), (24, 26)])                                    # right, to fork 3's approach
    _band(g, [(15, 25), (17, 25)])                                    # left, to the dead end
    _ellipse(g, 15.4, 23.4, 2.0, 2.4, s=2.7)                          # the dead end
    _band(g, [(18, 27), (18, 32)])                                    # its approach, from fork 1
    # -- fork 1: left is the way on, right a loop round a pillar ---------------------
    _ellipse(g, 26.5, 32.3, 2.3, 1.5, s=3.9)                          # the junction
    _band(g, [(18, 32), (25, 32)])                                    # left, to fork 2's approach
    _band(g, [(28, 32), (33, 32)])                                    # right, to the loop
    _ellipse(g, 32.2, 29.2, 3.4, 2.8, s=0.2)                          # the loop
    _band(g, [(26, 33), (26, 36)])                                    # its approach, from the mouth
    # -- the east mouth: the corridor in, the hall, daylight --------------------------
    _band(g, [(26, 36), (33, 36)], bulge=[(29, 38), (30, 38)])
    _band(g, [(33, 35), (40, 35)], bulge=[(35, 37), (36, 37)])
    _ellipse(g, 42.4, 34.0, 5.6, 3.3, s=4.4)
    # -- the shortcut tunnel: web C, the ledge, the jog down to the hall ------------
    _band(g, [(40, 7), (40, 16)])
    _band(g, [(40, 17), (40, 19)])
    _band(g, [(38, 19), (39, 19)])
    _band(g, [(38, 19), (38, 26)], bulge=[(37, 23)])
    _band(g, [(38, 26), (40, 26)])
    _band(g, [(40, 26), (40, 31)])
    _roughen(g, s=0.9, keep=[(6, 12, 11, 16), (11, 8, 15, 13), (3, 7, 7, 12), (38, 7, 42, 11),
                             (0, 22, 2, 31), (45, 30, 47, 38), (18, 14, 31, 22), (38, 15, 42, 19)])
    _tidy(g)
    # -- pin what the scripts and the checks rely on --------------------------------
    for y in range(H):
        for x in range(W):
            if x >= 41 and 32 <= y <= 36 and g[y][x] != "#":
                g[y][x] = ","                                         # daylight, east
            if x <= 3 and 24 <= y <= 30 and g[y][x] != "#":
                g[y][x] = ","                                         # daylight, west
    FIX = {
        # the mouths reach the edges on three rows each, and nowhere else
        **{(46, y): "," for y in (33, 34, 35)}, **{(47, y): "," for y in (33, 34, 35)},
        **{(47, y): "#" for y in (31, 32, 36, 37)}, **{(46, y): "#" for y in (31, 37)},
        **{(0, y): "," for y in (26, 27, 28)}, **{(0, y): "#" for y in (23, 24, 25, 29, 30, 31)},
        # the cobwebs' necks, one wide, rock either side
        (13, 10): ".", (13, 11): ".", (12, 10): "#", (12, 11): "#", (14, 10): "#", (14, 11): "#",
        (5, 8): ".", (5, 9): ".", (4, 8): "#", (4, 9): "#", (6, 8): "#", (6, 9): "#",
        (40, 9): ".", (40, 10): ".", (41, 9): "#", (41, 10): "#", (39, 9): "#", (39, 10): "#",
        # fork 3's pillars
        # pass 2: break up the straight walls the bands left
        (23, 20): ".", (26, 20): ".", (20, 20): ".", (10, 5): ".", (3, 7): ".",
        # the shortcut tunnel's walls: a bend and a pinch, so the long shaft reads
        (42, 13): ".", (42, 14): ".", (39, 12): ".", (39, 13): ".",
        # the loop's pillar at fork 1
        **{(x, y): "#" for x in (32, 33) for y in (28, 29, 30)}, (33, 35): "#",
    }
    for (x, y), ch in FIX.items():
        g[y][x] = ch
    return ["".join(r) for r in g]


ROWS = carve()

# ---------------------------------------------------------------------------
# What stands in the cave. Positions the scripts use are named here; the
# pieces below are placed from them.
# ---------------------------------------------------------------------------
HEKATAION = (24, 5)            # 3x4: the torches on row 0, the altar ledge at (+1, +3)
ALTAR = (25, 8)                # the ledge where the barley cake sits; faced from (25, 9)
NICHE = (27, 1)                # Hecate's supper, cut in the chamber's north face
WEBS = {"West": (13, 10), "Chamber": (5, 8), "Shortcut": (40, 9)}    # web_1 on (x, y) and (x, y + 1)
WEB_FLAG = {"West": "FLAG_ICHOR_HIDE_HOLLOW_WEB_WEST", "Chamber": "FLAG_ICHOR_HIDE_HOLLOW_WEB_CHAMBER",
            "Shortcut": "FLAG_ICHOR_HIDE_HOLLOW_WEB_SHORTCUT"}
BRAZIERS = {"1": (3, 12), "2": (6, 22)}    # 2x2, top-left
BRAZIER_FLAG = {"1": 0x14, "2": 0x15}      # FLAG_ICHOR_BRAZIERS_START + n (world-act1's block, BUILD.md)
LEDGE = (40, 17)               # the shortcut's one-way drop toward the east mouth (2 wide)
MOUTH_E = [(47, 33), (47, 34), (47, 35)]   # warp cells; the middle is warp 0
MOUTH_W = [(0, 26), (0, 27), (0, 28)]      # the middle is warp 3
STELE_E, STELE_W = (42, 31), (4, 25)

# Pieces from the catalog, by key: (key, x, y) for the piece's top-left cell.
PIECES = [
    *[("daylight_e", x - 1, y) for x, y in MOUTH_E],
    *[("daylight_w", x, y) for x, y in MOUTH_W],
    ("hekataion", *HEKATAION),
    ("niche_supper", *NICHE),
    ("chalk_wheel", 22, 1),
    ("chalk_triangle_lit", 25, 10),
    *[("web_1", x, y) for x, y in WEBS.values()],
    *[("brazier_cold", x, y) for x, y in BRAZIERS.values()],
    ("ledge_w", *LEDGE), ("ledge_e", LEDGE[0] + 1, LEDGE[1]),
    ("stele", *STELE_E), ("stele", *STELE_W),
    ("dish_covered", 39, 33),
    ("niche_empty", 16, 20),       # a supper someone ate, over fork 2's dead end
    ("slab", 22, 33),              # a slab fallen from the roof in fork 1's hall
    ("seep", 38, 17),              # the spring weeping into the shortcut tunnel
]
# Scatter: stone and bones, and Hecate's faint chalk on the true road.
SCATTER = [
    # the true road's chalk: into the dark, then at each fork her triangle and the right way
    ("chalk_triangle", 27, 32), ("chalk_triangle", 18, 26), ("chalk_triangle", 25, 16),
    ("chalk_arrow_w", 36, 37), ("chalk_arrow_w", 25, 33), ("chalk_arrow_e", 21, 26),
    ("chalk_arrow_n", 25, 22), ("chalk_arrow_n", 24, 12),
    # the east mouth and the corridor in
    ("stalagmites", 45, 31), ("pebbles", 38, 36), ("rock_pile", 45, 37), ("boulder", 30, 37),
    ("pebbles", 33, 36),
    # fork 1 and its loop
    ("stalagmite", 28, 33), ("pebbles", 21, 33), ("stalagmites", 29, 27), ("pebbles", 30, 30),
    ("pebbles", 30, 28),
    # fork 2 and its dead end
    ("stalagmite", 22, 26), ("rock_pile", 17, 22), ("pebbles", 15, 24),
    # fork 3
    ("stalagmite", 23, 15), ("pebbles", 25, 17), ("pebbles", 30, 19),
    # the Hekataion
    ("bones", 28, 3), ("stalagmites", 18, 5), ("stalagmite", 33, 7), ("pebbles", 16, 9),
    # the shortcut tunnel
    ("column", 41, 12), ("pebbles", 40, 15), ("stalagmites", 39, 24), ("pebbles", 41, 29),
    # Hekabe's hall and the web chamber
    ("stalagmite_tall", 14, 15), ("pebbles", 13, 16), ("stalagmites", 2, 15), ("pebbles", 5, 16),
    ("web_corner_w", 2, 4), ("web_corner_e", 9, 4), ("bones", 7, 6), ("pebbles", 3, 6),
    # hall 2 and Kallias's pocket
    ("pebbles", 10, 25), ("stalagmite", 11, 27), ("boulder", 10, 29),
    ("rock_pile", 4, 34), ("pebbles", 9, 36), ("stalagmites", 11, 34),
]

# ---------------------------------------------------------------------------
# The catalog
# ---------------------------------------------------------------------------
CAT = json.loads(CATALOG.read_text())
PIECE = {p["key"]: p for p in CAT["pieces"]}
WALK_OPEN = set(".T^v[]")          # walkable walk codes (J/>/< are ledges, X blocks)


def terrain_ids():
    return np.array(kit.autotile(ROWS, CAT, None), np.int32)


def kinds():
    return kit.classify(ROWS)


def placed():
    """(key, x, y) for every piece, the big ones first."""
    return PIECES + SCATTER


def build_ids_and_walk(state="cold"):
    """Metatile ids and walkability. state: 'cold' (as first found) or 'lit'
    (webs burnt, braziers and the Hekataion's torches lit)."""
    ids = terrain_ids()
    k = kinds()
    walk = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            walk[y, x] = k[y][x] in ("floor", "lit")
    for key, x, y in placed():
        p = PIECE[key]
        for j in range(p["h"]):
            for i in range(p["w"]):
                ids[y + j, x + i] = p["ids"][j][i]
                walk[y + j, x + i] = p["walk"][j][i] in WALK_OPEN
    if state in ("lit", "torch"):
        for (x, y) in WEBS.values():
            ids[y, x], ids[y + 1, x] = PIECE["torn_1"]["ids"][0][0], PIECE["torn_1"]["ids"][1][0]
            walk[y, x] = walk[y + 1, x] = True
        for n, (x, y) in BRAZIERS.items():
            if state == "torch" and n != "1":
                continue
            lit = PIECE["brazier_lit"]["ids"]
            for j in range(2):
                for i in range(2):
                    ids[y + j, x + i] = lit[j][i]
        hx, hy = HEKATAION
        ids[hy, hx] = PIECE["hekataion_torch_w_lit"]["ids"][0][0]
        ids[hy, hx + 1] = PIECE["hekataion_torch_s_gone"]["ids"][0][0]
        ids[hy, hx + 2] = PIECE["hekataion_torch_e_lit"]["ids"][0][0]
        ids[hy + 3, hx + 1] = PIECE["hekataion_no_cake"]["ids"][0][0]
        nx, ny = NICHE
        ids[ny + 1, nx] = PIECE["niche_empty"]["ids"][1][0]
    return ids, walk


def blockdata(ids, walk):
    """map.bin cells: metatile | collision << 10 | elevation << 12. As on Route 1,
    open ground is elevation 3; rock, solid pieces and ledges are collision 1 at 0."""
    out = np.zeros((H, W), np.uint16)
    webs = {(x, y + j) for x, y in WEBS.values() for j in (0, 1)}
    for y in range(H):
        for x in range(W):
            if walk[y, x]:
                out[y, x] = (int(ids[y, x]) & 0x3FF) | (3 << 12)
            else:   # a web's cells keep the ground's elevation, for when they burn
                out[y, x] = (int(ids[y, x]) & 0x3FF) | (1 << 10) | ((3 << 12) if (x, y) in webs else 0)
    return out


def write_if_changed(path, data):
    """Write only when the content differs, so make doesn't rebuild for nothing."""
    old = path.read_bytes() if path.exists() else None
    new = data.encode() if isinstance(data, str) else data
    if old != new:
        path.write_bytes(new)


def write_layout(ids, walk):
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    write_if_changed(LAYOUT_DIR / "map.bin", blockdata(ids, walk).astype("<u2").tobytes())
    rock = CAT["kit"]["T|..."]
    write_if_changed(LAYOUT_DIR / "border.bin", np.full(4, rock | (1 << 10), np.uint16).astype("<u2").tobytes())
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    for l in data["layouts"]:
        if l.get("id") == LAYOUT_ID:
            want = {"width": W, "height": H, "primary_tileset": "gTileset_Aethos",
                    "secondary_tileset": "gTileset_CaveDark"}
            if any(l.get(k) != v for k, v in want.items()):
                l.update(want)
                path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# The light: regions (VAR_TEMP_2), each a rect of open cells; the first rect
# that holds a cell names its region. 0, everywhere else, is the dark.
# ---------------------------------------------------------------------------
REGIONS = [
    # id, name, rect (x0, y0, x1, y1)
    (1, "DaylightEast", (41, 32, 47, 36)),
    (2, "Hekataion", (16, 2, 33, 12)),
    (3, "Brazier1", (1, 12, 14, 17)),
    (5, "DaylightWest", (0, 24, 3, 29)),
    (4, "Brazier2", (3, 22, 12, 32)),
]
REGION_NAME = {0: "Dark", **{i: n for i, n, _ in REGIONS}}


def region_of(x, y):
    for i, _, (x0, y0, x1, y1) in REGIONS:
        if x0 <= x <= x1 and y0 <= y <= y1:
            return i
    return 0


def region_triggers(walk):
    """(x, y, from_region, to_region) for every open cell on a region's edge, one
    per neighbouring region: stepping in from that region runs this one's Enter."""
    out = []
    for y in range(H):
        for x in range(W):
            if not walk[y, x]:
                continue
            here = region_of(x, y)
            seen = set()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and walk[ny, nx]:
                    there = region_of(nx, ny)
                    if there != here and there not in seen:
                        seen.add(there)
                        out.append((x, y, there, here))
    return out


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
GFX = "OBJ_EVENT_GFX_ICHOR_"
NIGHT_HOUNDS = {"HOUND": (24, 9), "HOUND_W": (23, 7), "HOUND_E": (27, 7)}
# local id, gfx, x, y, movement, trainer (sight or 0), script, hide flag
OBJECTS = [
    ("OLD_WOMAN", GFX + "ELDER_F", 40, 33, "FACE_RIGHT", 0, "OldWoman", "0"),
    ("HEKABE", GFX + "PILGRIM", 6, 14, "FACE_RIGHT", 3, "Hekabe", "0"),
    ("KALLIAS", GFX + "ACOLYTE_M", 8, 34, "FACE_UP", 2, "Kallias", "0"),       # ICHOR_STUB_SPRITE: an initiate
    ("PHAINO", GFX + "PILGRIM", 16, 23, "FACE_DOWN", 2, "Phaino", "0"),
    ("BATTOS", GFX + "GOATHERD", 3, 25, "FACE_LEFT", 2, "Battos", "0"),
    ("HOUND", "OBJ_EVENT_GFX_SPECIES(LYKOPUP)", *NIGHT_HOUNDS["HOUND"], "FACE_DOWN", 0, "Hound", "FLAG_TEMP_2"),
    ("HOUND_W", "OBJ_EVENT_GFX_SPECIES(LYKOPUP)", *NIGHT_HOUNDS["HOUND_W"], "FACE_LEFT", 0, "HoundFading", "FLAG_TEMP_3"),
    ("HOUND_E", "OBJ_EVENT_GFX_SPECIES(LYKOPUP)", *NIGHT_HOUNDS["HOUND_E"], "FACE_RIGHT", 0, "HoundFading", "FLAG_TEMP_4"),
    ("RAKNIT", "OBJ_EVENT_GFX_SPECIES(RAKNIT)", 7, 4, "FACE_DOWN", 0, "Raknit", "FLAG_TEMP_1"),
]
# The cobwebs: two invisible objects each, on the web's two cells, sharing its flag.
for _name, (_x, _y) in WEBS.items():
    for _k in (0, 1):
        OBJECTS.append((f"WEB_{_name.upper()}_{_k + 1}", "OBJ_EVENT_GFX_BREAKABLE_ROCK", _x, _y + _k, "INVISIBLE", 0,
                        "Web", WEB_FLAG[_name]))
# Items: (item, x, y, flag)
ITEMS = [
    ("ITEM_RELIC_COPPER", 14, 22, "FLAG_ICHOR_ITEM_HOLLOW_BRONZE_OBOL"),    # the Bronze Obol (ICHOR_STUB_COINS)
    ("ITEM_SILK_SCARF", 4, 5, "FLAG_ICHOR_ITEM_HOLLOW_SILK_SCARF"),
    ("ITEM_ETHER", 8, 23, "FLAG_ICHOR_ITEM_HOLLOW_ETHER"),
    ("ITEM_DUSK_BALL", 40, 18, "FLAG_ICHOR_ITEM_HOLLOW_DUSK_BALL"),
    ("ITEM_REVIVE", 12, 35, "FLAG_ICHOR_ITEM_HOLLOW_REVIVE"),
]
HIDDEN = [
    ("ITEM_ESCAPE_ROPE", 35, 29, "FLAG_ICHOR_HIDDEN_HOLLOW_ESCAPE_ROPE"),   # fork 1's loop
    ("ITEM_HONEY", NICHE[0], NICHE[1] + 1, "FLAG_ICHOR_HIDDEN_HOLLOW_HONEY"),  # Hecate's supper niche
    ("ITEM_STARDUST", 19, 18, "FLAG_ICHOR_HIDDEN_HOLLOW_STARDUST"),       # fork 3's left loop
    ("ITEM_HARD_STONE", 38, 22, "FLAG_ICHOR_HIDDEN_HOLLOW_HARD_STONE"),   # the shortcut tunnel
]
# Warps: the east mouth (0-2, to Route 4) and the west mouth (3-5, to Route 5).
ROUTE4, ROUTE5 = "MAP_ROUTE4_ISTHMUS", "MAP_ROUTE5_SKIRONIAN_CLIFFS"
ROUTE4_MOUTH_WARP = 0          # PLACEHOLDER: the Route 4 agent's mouth tile's warp id
ROUTE5_MOUTH_WARP = 0          # PLACEHOLDER: the Route 5 agent's mouth tile's warp id
# Bark triggers: (cells, temp var, which way)
BARKS = [
    ([(25, 35), (26, 35), (27, 35)], "VAR_TEMP_5", "Left"),
    ([(18, 29), (19, 29), (20, 29)], "VAR_TEMP_6", "Right"),
    ([(24, 23), (25, 23)], "VAR_TEMP_7", "Ahead"),
]


def map_exists(map_id):
    return any(f'"id": "{map_id}"' in p.read_text() for p in (ROOT / "data/maps").glob("*/map.json"))


def warps():
    """The mouths' warps. Until Route 4 and Route 5 are registered on this branch,
    each mouth leads to the other one (the build needs a map that exists): rerun
    this builder after merging them and the warps point at the routes."""
    east = (ROUTE4, ROUTE4_MOUTH_WARP) if map_exists(ROUTE4) else (MAP_ID, 3)
    west = (ROUTE5, ROUTE5_MOUTH_WARP) if map_exists(ROUTE5) else (MAP_ID, 0)
    out = []
    for cells, (dest, wid) in ((MOUTH_E, east), (MOUTH_W, west)):
        mid = cells[1]
        for x, y in [mid] + [c for c in cells if c != mid]:
            out.append({"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)})
    return out


def bg_events(walk):
    def faceable(x, y):
        return any(0 <= x + dx < W and 0 <= y + dy < H and walk[y + dy, x + dx]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    out = [(*STELE_E, "ANY", "SignEast"), (*STELE_W, "ANY", "SignWest"),
           (ALTAR[0], ALTAR[1], "NORTH", "Hekataion")]
    hx, hy = HEKATAION
    # the pillar's sides, from any side: its spring. (One event to a cell: the game reads
    # only the first event on a cell, and refuses it if the facing is wrong.)
    for y in range(hy + 1, hy + 4):
        out += [(hx, y, "ANY", "Spring"), (hx + 2, y, "ANY", "Spring")]
    for n, (bx, by) in BRAZIERS.items():
        out += [(bx + i, by + j, "ANY", "Brazier" + n) for j in range(2) for i in range(2)
                if faceable(bx + i, by + j)]
    out += [(22, 2, "NORTH", "ChalkWheel"), (7, 3, "NORTH", "WebPictures")]
    return out


def write_events(walk):
    m = json.loads((MAP_DIR / "map.json").read_text())
    m.update({"music": "MUS_ICHOR_HOLLOW", "region_map_section": "MAPSEC_HECATES_HOLLOW",
              "requires_flash": True, "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_UNDERGROUND",
              "allow_cycling": False, "allow_escaping": True, "allow_running": True, "show_map_name": True,
              "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None})
    objs = []
    for lid, gfx, x, y, move, sight, script, flag in OBJECTS:
        objs.append({"local_id": f"LOCALID_HOLLOW_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
                     "movement_type": f"MOVEMENT_TYPE_{move}", "movement_range_x": 0, "movement_range_y": 0,
                     "trainer_type": "TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
                     "trainer_sight_or_berry_tree_id": str(sight), "script": PX + script, "flag": flag})
    for item, x, y, flag in ITEMS:
        objs.append({"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
                     "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0, "movement_range_y": 0,
                     "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": item,
                     "script": "Common_EventScript_FindItem", "flag": flag})
    m["object_events"] = objs
    m["warp_events"] = warps()
    coords = []
    for cells, var, way in BARKS:
        coords += [{"type": "trigger", "x": x, "y": y, "elevation": 0, "var": var, "var_value": "0",
                    "script": PX + "Bark" + way} for x, y in cells]
    for x, y, frm, to in region_triggers(walk):
        coords.append({"type": "trigger", "x": x, "y": y, "elevation": 0, "var": "VAR_TEMP_2",
                       "var_value": str(frm), "script": PX + "Enter" + REGION_NAME[to]})
    m["coord_events"] = coords
    bgs = [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}",
            "script": PX + s} for x, y, f, s in bg_events(walk)]
    bgs += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag, "quantity": 1,
             "underfoot": False} for item, x, y, flag in HIDDEN]
    m["bg_events"] = bgs
    write_if_changed(MAP_DIR / "map.json", json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    return m


# ---------------------------------------------------------------------------
# The generated block of scripts.pory: drawing the cave from its state, and
# finding the light where the player arrives.
# ---------------------------------------------------------------------------
SCRIPT_BEGIN = "// --- Generated by tools/ichor/maps/hecates_hollow.py from its tables. Do not edit. ---"
SCRIPT_END = "// --- End of the generated block. ---"


def label(key, i=0, j=0):
    """The METATILE_CaveDark_* label for a piece's cell, where the build wrote one."""
    names = {
        ("brazier_cold", 0, 0): "Brazier_Cold_00", ("brazier_cold", 1, 0): "Brazier_Cold_10",
        ("brazier_cold", 0, 1): "Brazier_Cold_01", ("brazier_cold", 1, 1): "Brazier_Cold_11",
        ("brazier_lit", 0, 0): "Brazier_Lit_00", ("brazier_lit", 1, 0): "Brazier_Lit_10",
        ("brazier_lit", 0, 1): "Brazier_Lit_01", ("brazier_lit", 1, 1): "Brazier_Lit_11",
        ("web_1", 0, 0): "Web1_0", ("web_1", 0, 1): "Web1_1",
        ("torn_1", 0, 0): "Web1_Torn_0", ("torn_1", 0, 1): "Web1_Torn_1",
        ("hekataion_torch_w_lit", 0, 0): "Hekataion_TorchW_Lit", ("hekataion_torch_e_lit", 0, 0): "Hekataion_TorchE_Lit",
        ("hekataion_torch_s_lit", 0, 0): "Hekataion_TorchS_Lit", ("hekataion_torch_s_gone", 0, 0): "Hekataion_TorchS_Gone",
        ("hekataion_no_cake", 0, 0): "Hekataion_NoCake",
        ("niche_empty", 0, 1): "Niche_Empty_1",
    }
    return "METATILE_CaveDark_" + names[(key, i, j)]


def script_block():
    o = [SCRIPT_BEGIN, ""]
    hx, hy = HEKATAION
    nx, ny = NICHE
    o.append("// The cave as the story has left it: the Hekataion once the Torch is taken,")
    o.append("// the lit braziers, the burnt webs. ON_LOAD calls it before the map is drawn.")
    o.append(f"script {PX}DrawCave {{")
    o.append("    if (flag(FLAG_ICHOR_GOT_HECATES_TORCH)) {")
    o.append(f"        call({PX}DrawHekataionLit)")
    o.append("    }")
    for n in BRAZIERS:
        o.append(f"    if (flag(FLAG_ICHOR_BRAZIERS_START + 0x{BRAZIER_FLAG[n]:02X})) {{")
        o.append(f"        call({PX}DrawBrazier{n}Lit)")
        o.append("    }")
    o.append(f"    call({PX}DrawWebs)")
    o.append("    return")
    o.append("}")
    o.append("")
    o.append(f"script {PX}DrawHekataionLit {{")
    o.append(f"    setmetatile({hx}, {hy}, {label('hekataion_torch_w_lit')}, FALSE)")
    o.append(f"    setmetatile({hx + 1}, {hy}, {label('hekataion_torch_s_gone')}, FALSE)")
    o.append(f"    setmetatile({hx + 2}, {hy}, {label('hekataion_torch_e_lit')}, FALSE)")
    o.append(f"    setmetatile({hx + 1}, {hy + 3}, {label('hekataion_no_cake')}, TRUE)")
    o.append(f"    setmetatile({nx}, {ny + 1}, {label('niche_empty', 0, 1)}, TRUE)")
    o.append("    return")
    o.append("}")
    for side, key, dx in (("W", "hekataion_torch_w_lit", 0), ("E", "hekataion_torch_e_lit", 2),
                          ("S", "hekataion_torch_s_lit", 1)):
        o.append("")
        o.append(f"script {PX}LightTorch{side} {{")
        o.append(f"    setmetatile({hx + dx}, {hy}, {label(key)}, FALSE)")
        o.append("    special(DrawWholeMapView)")
        o.append("    playse(SE_M_FLAME_WHEEL)")
        o.append("    return")
        o.append("}")
    o.append("")
    o.append("// The middle face's torch comes away in the player's hand; the cake is gone.")
    o.append(f"script {PX}TakeTorch {{")
    o.append(f"    setmetatile({hx + 1}, {hy}, {label('hekataion_torch_s_gone')}, FALSE)")
    o.append(f"    setmetatile({hx + 1}, {hy + 3}, {label('hekataion_no_cake')}, TRUE)")
    o.append(f"    setmetatile({nx}, {ny + 1}, {label('niche_empty', 0, 1)}, TRUE)")
    o.append("    special(DrawWholeMapView)")
    o.append("    return")
    o.append("}")
    for n, (bx, by) in BRAZIERS.items():
        o.append("")
        o.append(f"script {PX}DrawBrazier{n}Lit {{")
        for j in range(2):
            for i in range(2):
                o.append(f"    setmetatile({bx + i}, {by + j}, {label('brazier_lit', i, j)}, TRUE)")
        o.append("    return")
        o.append("}")
    o.append("")
    o.append("// Burnt webs: torn shreds you can walk through. Each web's second object shares")
    o.append("// its flag, so it goes too.")
    o.append(f"script {PX}DrawWebs {{")
    for n, (x, y) in WEBS.items():
        o.append(f"    if (flag({WEB_FLAG[n]})) {{")
        o.append(f"        setmetatile({x}, {y}, {label('torn_1', 0, 0)}, FALSE)")
        o.append(f"        setmetatile({x}, {y + 1}, {label('torn_1', 0, 1)}, FALSE)")
        o.append(f"        removeobject(LOCALID_HOLLOW_WEB_{n.upper()}_1)")
        o.append(f"        removeobject(LOCALID_HOLLOW_WEB_{n.upper()}_2)")
        o.append("    }")
    o.append("    return")
    o.append("}")
    o.append("")
    o.append("// ON_TRANSITION: the region the player arrives in (VAR_TEMP_2) and its light.")
    o.append(f"script {PX}FindRegion {{")
    o.append("    getplayerxy(VAR_TEMP_0, VAR_TEMP_1)")
    o.append("    setvar(VAR_TEMP_2, 0)")
    for k, (i, name, (x0, y0, x1, y1)) in enumerate(REGIONS):
        kw = "if" if k == 0 else "elif"
        o.append(f"    {kw} (var(VAR_TEMP_0) >= {x0} && var(VAR_TEMP_0) <= {x1} && "
                 f"var(VAR_TEMP_1) >= {y0} && var(VAR_TEMP_1) <= {y1}) {{")
        o.append(f"        setvar(VAR_TEMP_2, {i})")
        o.append(f"        call({PX}Light{name})")
        o.append("    }")
    o.append("    return")
    o.append("}")
    o.append("")
    o.append(SCRIPT_END)
    return "\n".join(o)


def splice_script():
    path = MAP_DIR / "scripts.pory"
    text = path.read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"hecates_hollow: {path} needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    new = text[:a] + script_block() + text[b + len(SCRIPT_END):]
    if new != text:
        path.write_text(new)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
LEDGE_CELLS = {(LEDGE[0], LEDGE[1]), (LEDGE[0] + 1, LEDGE[1])}


def reach(walk, start, blocked=frozenset()):
    """Open cells reachable from start; a ledge is crossed southward only."""
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in LEDGE_CELLS:
                if dy == 1:
                    p = (x, y + 2)
                else:
                    continue
            if 0 <= p[0] < W and 0 <= p[1] < H and p not in seen and walk[p[1], p[0]] and p not in blocked:
                seen.add(p)
                q.append(p)
    return seen


def labels():
    text = (ROOT / "include/constants/metatile_labels.h").read_text()
    return {k: int(v, 16) for k, v in re.findall(r"#define (METATILE_CaveDark_\w+)\s+(0x[0-9A-Fa-f]+)", text)}


def check(m, cold, lit):
    errors = []
    ids_cold, walk_cold = cold
    ids_lit, walk_lit = lit
    east, west = MOUTH_E[1], MOUTH_W[1]
    people = {(o["x"], o["y"]) for o in m["object_events"] if o.get("flag") in ("0",) or "ITEM" in o["trainer_sight_or_berry_tree_id"]}
    # every scatter piece and placed piece on open ground (pieces that are rock-face pieces excepted)
    on_face = {"niche_supper", "niche_empty", "chalk_wheel", "seep"}
    for key, x, y in placed():
        if key in on_face or key.startswith("daylight"):
            continue
        if ROWS[y][x] == "#":
            errors.append(f"{key} at ({x},{y}) stands on rock")
    for key, x, y in placed():
        if key in on_face:
            k = kinds()
            if not (k[y][x] == "ft" and k[y + 1][x] == "fb"):
                errors.append(f"{key} at ({x},{y}) isn't on a face (ft over fb)")
    # thin rock: a rock cell with open floor above and below draws as half a wall
    for y in range(1, H - 1):
        for x in range(W):
            if ROWS[y][x] == "#" and ROWS[y - 1][x] != "#" and ROWS[y + 1][x] != "#":
                errors.append(f"rock one cell thick at ({x},{y})")
    # before the Torch: the webs shut the road west, the web chamber and the shortcut
    before = reach(walk_cold, east)
    if west in before:
        errors.append("the west mouth is reachable before the webs burn")
    for name, cell in (("the Hekataion's altar", (ALTAR[0], ALTAR[1] + 1)), ("fork 2's dead end", (14, 23))):
        if cell not in before:
            errors.append(f"{name} {cell} isn't reachable from the east mouth before the Torch")
    for name, cell in (("Hekabe's hall", (10, 15)), ("the web chamber", (6, 5)), ("the shortcut's upper tunnel", (40, 13))):
        if cell in before:
            errors.append(f"{name} {cell} is reachable before the Torch")
    # the forks: the right way is the only way to the Hekataion
    goal = (ALTAR[0], ALTAR[1] + 1)
    for name, cut in (("fork 1's left", {(22, y) for y in range(29, 34)}),
                      ("fork 2's right", {(22, y) for y in range(24, 28)}),
                      ("fork 3's approach", {(x, 24) for x in range(23, 28)})):
        if goal in reach(walk_cold, east, frozenset(cut)):
            errors.append(f"the Hekataion is reachable without {name}")
    # after: everything open, and the ledge one way
    after = reach(walk_lit, east)
    stranded = sorted({(x, y) for y in range(H) for x in range(W) if walk_lit[y, x]} - after)
    if stranded:
        errors.append(f"open but unreachable once the webs burn: {stranded[:12]}")
    web_c = frozenset({WEBS["Shortcut"], (WEBS["Shortcut"][0], WEBS["Shortcut"][1] + 1)})
    if (40, 13) in reach(walk_lit, (LEDGE[0], LEDGE[1] + 1), web_c):
        errors.append("the shortcut's ledge can be climbed from below")
    # Hekabe: her sight cuts the only way west
    hek = next(o for o in m["object_events"] if o.get("local_id") == "LOCALID_HOLLOW_HEKABE")
    sight = {(hek["x"] + k, hek["y"]) for k in range(0, int(hek["trainer_sight_or_berry_tree_id"]) + 1)}
    if west in reach(walk_lit, (13, 13), frozenset(sight)):
        errors.append("the road west gets past Hekabe without crossing her sight")
    # people, items and signs
    for o in m["object_events"]:
        if not walk_lit[o["y"], o["x"]] and o["movement_type"] != "MOVEMENT_TYPE_INVISIBLE":
            errors.append(f"{o.get('local_id', o['trainer_sight_or_berry_tree_id'])} stands on a solid cell")
        if (o["x"], o["y"]) not in after and o["movement_type"] != "MOVEMENT_TYPE_INVISIBLE":
            errors.append(f"{o.get('local_id', o['trainer_sight_or_berry_tree_id'])} can't be reached")
    for b in m["bg_events"]:
        if not any((b["x"] + dx, b["y"] + dy) in after for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            errors.append(f"bg event ({b['x']},{b['y']}) can't be faced")
    cells = [(b["x"], b["y"]) for b in m["bg_events"]]
    for c in sorted({c for c in cells if cells.count(c) > 1}):
        errors.append(f"two bg events on {c}: the game only ever reads the first")
    for c in m["coord_events"]:
        if not walk_lit[c["y"], c["x"]]:
            errors.append(f"trigger ({c['x']},{c['y']}) is on a solid cell")
    for w in m["warp_events"]:
        if not walk_lit[w["y"], w["x"]]:
            errors.append(f"warp ({w['x']},{w['y']}) is on a solid cell")
    # every setmetatile lands on the piece it swaps
    lab = labels()
    allowed = {}
    hx, hy = HEKATAION
    for key, x, y in [("hekataion_torch_w_lit", hx, hy), ("hekataion_torch_s_lit", hx + 1, hy),
                      ("hekataion_torch_s_gone", hx + 1, hy), ("hekataion_torch_e_lit", hx + 2, hy),
                      ("hekataion_no_cake", hx + 1, hy + 3)]:
        allowed.setdefault((x, y), set()).add(PIECE[key]["ids"][0][0])
    allowed.setdefault((NICHE[0], NICHE[1] + 1), set()).add(PIECE["niche_empty"]["ids"][1][0])
    for bx, by in BRAZIERS.values():
        for j in range(2):
            for i in range(2):
                allowed.setdefault((bx + i, by + j), set()).add(PIECE["brazier_lit"]["ids"][j][i])
    for x, y in WEBS.values():
        for j in range(2):
            allowed.setdefault((x, y + j), set()).add(PIECE["torn_1"]["ids"][j][0])
    script = (MAP_DIR / "scripts.pory").read_text()
    for x, y, lname in re.findall(r"setmetatile\((\d+),\s*(\d+),\s*(METATILE_\w+)", script):
        x, y = int(x), int(y)
        if lab.get(lname) not in allowed.get((x, y), set()):
            errors.append(f"setmetatile({x}, {y}, {lname}) isn't one of that cell's swaps")
    _ = people
    return errors


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------
def renderer():
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R, R.Renderer(R.Tileset(R.resolve_tileset("gTileset_Aethos", syms)),
                         R.Tileset(R.resolve_tileset("gTileset_CaveDark", syms)))


def sprite(gfx, facing):
    from PIL import Image
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
        species = {"LYKOPUP": "poochyena", "RAKNIT": "spinarak"}[gfx[len("OBJ_EVENT_GFX_SPECIES("):-1]]
        sheet = Image.open(ROOT / f"graphics/pokemon/{species}/overworld.png")
        w = h = 32
    elif gfx == "OBJ_EVENT_GFX_ITEM_BALL":
        sheet = Image.open(ROOT / "graphics/object_events/pics/misc/ichor_item_jar.png")
        w = h = 16
    else:
        sheet = Image.open(ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png")
        w, h = 16, 32
    frame = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}.get(facing, 0)
    crop = sheet.crop((frame * w, 0, frame * w + w, h))
    spr = crop.convert("RGBA")
    if sheet.mode == "P":
        idx, px = crop.load(), spr.load()
        for j in range(h):
            for i in range(w):
                if idx[i, j] == 0:
                    px[i, j] = (0, 0, 0, 0)
    if facing == "RIGHT":
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    return spr, w, h


def people(im, m, scale=2, night=False):
    for o in m["object_events"]:
        if o["movement_type"] == "MOVEMENT_TYPE_INVISIBLE":
            continue
        flag = o.get("flag", "0")
        if flag.startswith("FLAG_TEMP") and not (night and "HOUND" in o.get("local_id", "")):
            continue
        facing = o["movement_type"].replace("MOVEMENT_TYPE_FACE_", "").replace("MOVEMENT_TYPE_LOOK_AROUND", "DOWN")
        spr, w, h = sprite(o["graphics_id"], facing)
        from PIL import Image
        spr = spr.resize((w * scale, h * scale), Image.NEAREST)
        x = (o["x"] * 16 + 8 - w // 2) * scale
        y = (o["y"] * 16 + 16 - h) * scale
        im.paste(spr, (x, y), spr)
    return im


def darkness(img, lit_regions, lights, walk, scale=2):
    """Black out what a dark map hides. A lit region (flash level 0) shows its open
    cells and the walls two cells round them, as its screen would; the circles of
    light, (cx, cy, r) in map pixels, are the flash radius round the player."""
    a = np.array(img).astype(np.float32)
    Hp, Wp = a.shape[:2]
    yy, xx = np.mgrid[0:Hp, 0:Wp]
    mask = np.zeros((Hp, Wp), bool)
    cells = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            if walk[y, x] and region_of(x, y) in lit_regions:
                cells[max(0, y - 2):y + 2, max(0, x - 1):x + 2] = True
    for y in range(H):
        for x in range(W):
            if cells[y, x]:
                mask[y * 16 * scale:(y + 1) * 16 * scale, x * 16 * scale:(x + 1) * 16 * scale] = True
    for cx, cy, r in lights:
        mask |= (xx - cx * scale) ** 2 + (yy - cy * scale) ** 2 <= (r * scale) ** 2
    a[~mask] = 0
    from PIL import Image
    return Image.fromarray(a.astype(np.uint8))


def region_cells_rects():
    return {i: rect for i, _, rect in REGIONS}


def render(m, cold, lit, out):
    from PIL import Image, ImageDraw
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    R, r = renderer()
    s = 2

    def img(state):
        ids, walk = state
        return R.render_blocks(r, blockdata(ids, walk).reshape(-1), W).convert("RGBA").resize(
            (W * 16 * s, H * 16 * s), Image.NEAREST)
    first = people(img(cold), m, s)
    first.convert("RGB").save(out / "hecates_hollow.png")
    cleared = people(img(lit), m, s, night=True)
    cleared.convert("RGB").save(out / "hecates_hollow_lit.png")
    # without the Torch: the daylight at both mouths, the skylight's faint circle in the
    # Hekataion, and the 1.5-tile circle at stops along the dark road
    road = [(44, 34), (36, 36), (27, 35), (26, 31), (19, 30), (19, 26), (24, 24), (24, 19), (25, 14)]
    lights = [(x * 16 + 8, y * 16 + 8, 24) for x, y in road] + [(25 * 16 + 8, 9 * 16 + 8, 64)]
    darkness(first.convert("RGB"), {1, 5}, lights, lit[1], s).save(out / "hecates_hollow_dark.png")
    # with the Torch: the Hekataion and brazier 1's hall lit, the 3.5-tile circle on the
    # road west, down the shortcut, and through hall 2 (its brazier still cold)
    road = [(13, 11), (4, 19), (8, 26), (8, 33), (36, 7), (40, 12), (39, 22), (41, 29), (27, 34), (19, 29)]
    lights = [(x * 16 + 8, y * 16 + 8, 56) for x, y in road]
    torch = people(img(build_ids_and_walk("torch")), m, s)
    darkness(torch.convert("RGB"), {1, 2, 3, 5}, lights, lit[1], s).save(out / "hecates_hollow_dark_torch.png")
    # events, for review
    ev = img(cold)
    ov = Image.new("RGBA", ev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = 16 * s
    walk = cold[1]
    tint = {0: None, 1: (255, 240, 120, 50), 2: (120, 200, 255, 50), 3: (255, 150, 60, 50),
            4: (255, 110, 60, 50), 5: (255, 240, 120, 50)}
    for y in range(H):
        for x in range(W):
            if not walk[y, x]:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 40))
            elif tint[region_of(x, y)]:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=tint[region_of(x, y)])
    for e in m["coord_events"]:
        col = (255, 255, 255, 140) if e["var"] == "VAR_TEMP_2" else (255, 60, 200, 200)
        d.rectangle([e["x"] * c + 10, e["y"] * c + 10, e["x"] * c + c - 11, e["y"] * c + c - 11], fill=col)
    for b in m["bg_events"]:
        d.rectangle([b["x"] * c + 2, b["y"] * c + 2, b["x"] * c + c - 3, b["y"] * c + c - 3],
                    outline=(80, 160, 255, 255), width=2)
    for w in m["warp_events"]:
        d.rectangle([w["x"] * c + 6, w["y"] * c + 6, w["x"] * c + c - 7, w["y"] * c + c - 7],
                    outline=(255, 60, 200, 255), width=3)
    for o in m["object_events"]:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5],
                  outline=(40, 255, 90, 255), width=3)
    Image.alpha_composite(ev, ov).convert("RGB").save(out / "hecates_hollow_events.png")
    # screens along the road (15x10 tiles each), for the critique passes
    stops = [("east_mouth", 42, 34), ("fork1", 26, 32), ("fork2", 19, 26), ("fork3", 25, 18),
             ("hekataion", 25, 7), ("hekabe", 7, 15), ("hall2", 6, 26), ("tunnel", 40, 18)]
    full = first.convert("RGB")
    tiles = []
    for name, x, y in stops:
        x0 = max(0, min(W - 15, x - 7)) * c
        y0 = max(0, min(H - 10, y - 5)) * c
        tiles.append(full.crop((x0, y0, x0 + 15 * c, y0 + 10 * c)))
    sheet = Image.new("RGB", (2 * 15 * c + c, 4 * 10 * c + 3 * c // 2), (20, 20, 28))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % 2) * (15 * c + c), (k // 2) * (10 * c + c // 2)))
    sheet.save(out / "hecates_hollow_screens.png")


def ascii_map(walk):
    out = []
    for y in range(H):
        out.append("".join(ROWS[y][x] if walk[y, x] or ROWS[y][x] == "#" else "X" for x in range(W)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--ascii", action="store_true", help="print the terrain grid")
    args = ap.parse_args()
    cold = build_ids_and_walk("cold")
    lit = build_ids_and_walk("lit")
    write_layout(*cold)
    m = write_events(lit[1])
    splice_script()
    errors = check(m, cold, lit)
    if args.ascii:
        for y, row in enumerate(ascii_map(cold[1])):
            print(f"{y:3d} {row}")
    if args.render:
        render(m, cold, lit, args.render)
    for e in errors:
        print("PROBLEM:", e)
    if not map_exists(ROUTE4) or not map_exists(ROUTE5):
        print("NOTE: Route 4 or Route 5 isn't registered here yet: the mouths lead to each other until "
              "they are (rerun this builder after merging them)")
    print(f"hecates_hollow: {W}x{H}, {len(m['object_events'])} objects, {len(m['warp_events'])} warps, "
          f"{len(m['coord_events'])} triggers, {len(m['bg_events'])} bg events, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
