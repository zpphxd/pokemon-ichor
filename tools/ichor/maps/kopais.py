#!/usr/bin/env python3
"""Build Route 7 (the Kronia grounds), Route 8 (the Kopais road), the Kopais
katavothres, and Lebadeia with its Trophoneion and the honey-baker's house:
layouts, events, scripts, wild tables, trainer parties for the new trainers,
checks and review renders.

The three outdoor maps were placeholders from thyrsa.py (Route 7) and
arkadia.py (Route 8, Lebadeia): straight roads past open grass with every
trainer avoidable, and Lebadeia a bare yard with an outdoor healer. Those
scripts now skip them; thyrsa.py and arkadia.py still write the parties of the
trainers they named (HAGES..MANTO, R8_PANOS..R8_THYONE). design/maps/Lebadeia.md
and design/maps/Route8_KopaisRoad.md are the briefs and the hooks for later.

Route 7, the Kronia grounds (Skiron, like Kithairon below it). *Off Kithairon's
col, through pine and scree, into the festival field outside Thyrsa's south gate
where the Titanborn masters serve bread at the Kronia.*
  - The col's foot: pines, the first band, Manto in a niche.
  - The cut stair up the scree band: Euxenos at its head; a ledge home.
  - The scree meadow: the second band, Doris on the narrow road.
  - The camp gate: Hages in it. The Kronia field: tents, the bread tables, the
    baker (a heal and Barley Cakes), the Kronist, Myrton and Philiskos.
  - Kronos's stone in the west pocket, behind marble rubble (the Hammer).
  - The old vineyard east, behind vines (the Sickle); a column drum on its stair
    to the upper terrace (the Girdle, won just north in Thyrsa: a return).
  - Olives and the last band up to the gate.
  - East along the lane under the olives, just outside the gate: the Nursery
    of Nysa, a farmhouse where the nymphs who raised Dionysus raise travelers'
    Pokemon (the day care, Route7_NurseryOfNysa, kapeleia_rooms.py), and its
    glade below the wall where the two Pokemon left there roam; Aristaios the
    beekeeper keeps the gate and hands over the Eggs.

Route 8, the Kopais road (Stymphalia's marsh pieces on the aethos primary). *A
Mycenaean dike carries the road across Lake Kopais's reeds from Thyrsa to the
mountain's foot, where the lake drains into the katavothres; through them, the
Herkyna's valley climbs to Lebadeia.*
  - Thyrsa's olives (an aethos strip at the seam) and the first band.
  - The dike: two reed bars to wade (bands two and three), Enchelys the
    eel-fisher and Panos on its landings. Gla's island fortress across the
    water to the north (Poseidon's Conch: a return).
  - The south shore: a sand bank, the fisher's gift, a boardwalk into the reeds
    behind a reed thicket (the Sickle) to an islet's jar.
  - The katavothra: the road enters the mountain (KopaisKatavothres).
  - West of the ridge: the Herkyna's valley, plane trees, a wayside shrine of
    Trophonios, the last band, Lebadeia.

The katavothres (cave_dark, dark: the Torch). The lake's water pours into the
rock and runs west under the ridge. A drain passage with a lit brazier hall in
the middle, the black channel (fish it; Poseidon's Conch for the rock in it),
a side gallery behind rubble (the Hammer), and a cliff with old handholds (the
climbing relic).

Lebadeia (Stymphalia). *A pilgrims' stop in the gorge where the Herkyna leaves
the rock: Trophonios's temple, a rest-house for travelers, on its terrace above
the springs of Lethe and Mnemosyne, and the oracle's sealed mouth in the cliff.*

Usage: /usr/bin/python3 tools/ichor/maps/kopais.py [--render DIR] [--walk]
  --render DIR  <map>.png (2x, with people), <map>_walk.png (collision, grass,
                water, sight lines) and 15x10 views along the road
  --walk        prints each walk map (# solid, ~ water, , grass, v ledge)
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import route5 as R5  # noqa: E402  (aethos ids, noise, behaviors, sprites)
import kithairon as K  # noqa: E402  (the Skiron painter, for Route 7)
import lakonia_tiles as LT  # noqa: E402  (Stymphalia's pieces)
import water_tables as WT  # noqa: E402
import plan_hook  # noqa: E402  (tools/ichor/wild_plan.py)

noise = R5.noise
GFX = "OBJ_EVENT_GFX_ICHOR_"
FACE = {"LEFT": (-1, 0), "RIGHT": (1, 0), "UP": (0, -1), "DOWN": (0, 1)}
STYM_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/stymphalia/porytiles_bin/metatile_attributes.bin", "<u2")
CAVE_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/cave_dark/porytiles_bin/metatile_attributes.bin", "<u2")
CIVIC = "gTileset_Civic"

R7, R8, CAVE, LEB = "Route7_KroniaGrounds", "Route8_KopaisRoad", "KopaisKatavothres", "Lebadeia"
TEMPLE, HOUSE = "Lebadeia_Trophoneion", "Lebadeia_HoneyHouse"


def const(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


def behavior_of(mid, secondary):
    if mid < 0x200:
        a = R5.AETHOS_ATTR[mid]
    else:
        a = {"gTileset_Stymphalia": STYM_ATTR, "gTileset_CaveDark": CAVE_ATTR,
             "gTileset_Skiron": R5.SKIRON_ATTR}[secondary][mid - 0x200]
    return R5.MB.get(int(a) & 0xFF, "?")


# ---------------------------------------------------------------------------
# Events, shared by every map here
# ---------------------------------------------------------------------------

def obj(lid, gfx, x, y, facing, script, flag="0", sight=0, trainer=False, move=None):
    return {"local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": move or (f"MOVEMENT_TYPE_FACE_{facing}" if facing else "MOVEMENT_TYPE_NONE"),
            "movement_range_x": 1 if move and "WANDER" in move else 0,
            "movement_range_y": 1 if move and "WANDER" in move else 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}


class Spec:
    """One map's events and scripts: trainers (mandatory or optional), people,
    relic obstacles, items, hidden items, signs, warps, connections."""

    def __init__(self, name):
        self.name = name
        self.px = name + "_EventScript_"
        self.lid = "LOCALID_" + const(name) + "_"
        self.trainers, self.people, self.gates = [], [], []
        self.items, self.hidden, self.signs, self.scripts = [], [], [], []
        self.warps, self.coords, self.connections = [], [], []

    def trainer(self, const_name, gfx, x, y, facing, sight, intro, defeat, after=None, mandatory=True):
        self.trainers.append(dict(name=const_name, gfx=GFX + gfx, x=x, y=y, facing=facing, sight=sight,
                                  intro=intro, defeat=defeat, after=after or defeat, mandatory=mandatory))

    def person(self, name, gfx, x, y, facing="DOWN", flag="0", move=None):
        self.people.append((name, gfx, x, y, facing, flag, move))

    def gate(self, name, kind, x, y, flag="0"):
        """kind: thicket (the Sickle), rubble (the Hammer), drum (the Girdle)."""
        self.gates.append((name, kind, x, y, flag))

    def item(self, item, x, y, flag):
        self.items.append((item, x, y, flag))

    def hide(self, item, x, y, flag):
        self.hidden.append((item, x, y, flag))

    def sign(self, x, y, script, facing="ANY", text=None):
        self.signs.append((x, y, facing, script))
        if text is not None:
            self.scripts.append(f'''script {self.px}{script} {{
    msgbox(format("{text}"), MSGBOX_SIGN)
    end
}}''')

    def objects(self):
        out = []
        for t in self.trainers:
            short = t["name"].replace("R8_", "").replace("KOPAIS_", "")
            out.append(obj(self.lid + short, t["gfx"], t["x"], t["y"], t["facing"], self.px + short,
                           sight=t["sight"], trainer=True))
        for name, gfx, x, y, facing, flag, move in self.people:
            g = gfx if gfx.startswith("OBJ_") else GFX + gfx
            out.append(obj(self.lid + const(name), g, x, y, facing, self.px + name, flag, move=move))
        gfx = {"thicket": "OBJ_EVENT_GFX_CUTTABLE_TREE", "rubble": "OBJ_EVENT_GFX_BREAKABLE_ROCK",
               "drum": "OBJ_EVENT_GFX_PUSHABLE_BOULDER"}
        script = {"thicket": "EventScript_CutTree", "rubble": "EventScript_RockSmash",
                  "drum": "EventScript_StrengthBoulder"}
        for name, kind, x, y, flag in self.gates:
            out.append(obj(self.lid + const(name), gfx[kind], x, y, None, script[kind], flag))
        for item, x, y, flag in self.items:
            o = obj(None, "OBJ_EVENT_GFX_ITEM_BALL", x, y, "DOWN", "Common_EventScript_FindItem", flag)
            o.pop("local_id")
            o["trainer_sight_or_berry_tree_id"] = item
            out.append(o)
        return out

    def bgs(self):
        out = [{"type": "sign", "x": x, "y": y, "elevation": 0,
                "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": self.px + s}
               for x, y, f, s in self.signs]
        out += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
                 "quantity": 1, "underfoot": False} for item, x, y, flag in self.hidden]
        return out


def write_events(spec, music, map_type, header=None, extra=None):
    path = ROOT / f"data/maps/{spec.name}/map.json"
    m = json.loads(path.read_text())
    m["music"] = music
    m["map_type"] = map_type
    m["connections"] = spec.connections or None
    m["object_events"] = spec.objects()
    m["warp_events"] = spec.warps
    m["coord_events"] = spec.coords
    m["bg_events"] = spec.bgs()
    if extra:
        m.update(extra)
    path.write_text(json.dumps(m, indent=2) + "\n")
    scripts = [header or f"mapscripts {spec.name}_MapScripts {{}}",
               "// Generated by tools/ichor/maps/kopais.py; edit the builder, not this file."]
    for t in spec.trainers:
        short = t["name"].replace("R8_", "").replace("KOPAIS_", "")
        scripts.append(f'''script {spec.px}{short} {{
    trainerbattle_single(TRAINER_ICHOR_{t["name"]}, format("{t["intro"]}"), format("{t["defeat"]}"))
    msgbox(format("{t["after"]}"), MSGBOX_AUTOCLOSE)
    end
}}''')
    scripts += spec.scripts
    (ROOT / f"data/maps/{spec.name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")


def warp(x, y, dest, index):
    return {"x": x, "y": y, "elevation": 0, "dest_map": "MAP_" + const(dest), "dest_warp_id": str(index)}


def write_layout(name, blocks, border, primary, secondary):
    """blocks: (h, w) uint16 in map.bin form; border: four map.bin blocks."""
    d = ROOT / f"data/layouts/{name}"
    d.mkdir(parents=True, exist_ok=True)
    blocks.astype("<u2").tofile(d / "map.bin")
    np.array(border, np.uint16).astype("<u2").tofile(d / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    lid = "LAYOUT_" + const(name)
    for lay in data["layouts"]:
        if lay.get("id") == lid:
            h, w = blocks.shape
            want = (w, h, primary, secondary)
            if (lay["width"], lay["height"], lay["primary_tileset"], lay["secondary_tileset"]) != want:
                lay["width"], lay["height"], lay["primary_tileset"], lay["secondary_tileset"] = want
                path.write_text(json.dumps(data, indent=2) + "\n")
            return
    raise SystemExit(f"no layout {lid}")


# ---------------------------------------------------------------------------
# A map as walked: blocks, behaviors, events. Checks and renders work on this.
# ---------------------------------------------------------------------------

class Walked:
    WATER = {"MB_POND_WATER", "MB_OCEAN_WATER", "MB_DEEP_WATER", "MB_INTERIOR_DEEP_WATER"}
    JUMP = {"MB_JUMP_SOUTH": (0, 1), "MB_JUMP_WEST": (-1, 0), "MB_JUMP_EAST": (1, 0), "MB_JUMP_NORTH": (0, -1)}

    def __init__(self, name, blocks, secondary, spec, primary="gTileset_Aethos"):
        self.name, self.blocks, self.secondary, self.spec, self.primary = name, blocks, secondary, spec, primary
        self.h, self.w = blocks.shape
        self.mid = blocks & 0x3FF
        self.solid = (blocks & 0xC00) != 0
        self.elev = blocks >> 12
        self.beh = np.array([[behavior_of(int(self.mid[y, x]), secondary) if primary == "gTileset_Aethos" else "?"
                              for x in range(self.w)] for y in range(self.h)], object)

    def water(self, x, y):
        return self.beh[y, x] in self.WATER

    def grass(self, x, y):
        return self.beh[y, x] in ("MB_TALL_GRASS", "MB_LONG_GRASS")

    def open(self, x, y, blocked=frozenset(), surf=False):
        return (0 <= x < self.w and 0 <= y < self.h and not self.solid[y, x]
                and (surf or not self.water(x, y)) and (x, y) not in blocked)

    def steps(self, x, y, blocked=frozenset(), surf=False):
        for dx, dy in FACE.values():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.w and 0 <= ny < self.h):
                continue
            j = self.JUMP.get(self.beh[ny, nx])
            if j is not None:
                if j == (dx, dy) and self.open(nx + dx, ny + dy, blocked):
                    yield nx + dx, ny + dy
                continue
            if self.open(nx, ny, blocked, surf):
                yield nx, ny

    def reach(self, starts, blocked=frozenset(), surf=False):
        seen = {s for s in starts if self.open(*s, blocked)}
        q = deque(seen)
        while q:
            c = q.popleft()
            for n in self.steps(*c, blocked, surf):
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        return seen

    def grass_cost(self, starts, goals, blocked=frozenset()):
        cost = {s: int(self.grass(*s)) for s in starts if self.open(*s, blocked)}
        dq = deque(sorted(cost, key=cost.get))
        while dq:
            c = dq.popleft()
            for n in self.steps(*c, blocked):
                v = cost[c] + int(self.grass(*n))
                if v < cost.get(n, 1 << 30):
                    cost[n] = v
                    (dq.append if v > cost[c] else dq.appendleft)(n)
        got = [cost[t] for t in goals if t in cost]
        return min(got) if got else None

    def sight(self, t):
        dx, dy = FACE[t["facing"]]
        out, x, y = [], t["x"], t["y"]
        for _ in range(t["sight"]):
            x, y = x + dx, y + dy
            if not self.open(x, y):
                break
            out.append((x, y))
        return out


def check(m, segments, forced_min=8, ends_all=None):
    """segments: [(label, start cells, goal cells)], each a stretch of the main
    road a first-time walker must cross (no relics; people are walls). Returns
    problems, the names of trainers that cut a segment, and forced grass per
    segment."""
    problems = []
    objs = m.spec.objects()
    gate_gfx = ("OBJ_EVENT_GFX_CUTTABLE_TREE", "OBJ_EVENT_GFX_BREAKABLE_ROCK", "OBJ_EVENT_GFX_PUSHABLE_BOULDER")
    gates = {(o["x"], o["y"]) for o in objs if o["graphics_id"] in gate_gfx}
    people = {(o["x"], o["y"]) for o in objs} - gates
    for o in objs:
        if m.solid[o["y"], o["x"]] or m.water(o["x"], o["y"]):
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} on a solid or water cell")
    ends = ends_all or [c for _, a, b in segments for c in a + b]
    # with relics (gates open) everything is reachable and readable
    allr = m.reach(ends, frozenset(people), surf=True)     # every relic, the Conch included
    for o in objs:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in allr for dx, dy in FACE.values()):
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} at ({x},{y}) can't be reached")
    for b in m.spec.bgs():
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and not m.solid[y, x]:
            problems.append(f"sign {b['script']} at ({x},{y}) is on walkable ground")
        f = b.get("player_facing_dir", "")
        spots = [(x, y + 1)] if f.endswith("NORTH") else [(x, y - 1)] if f.endswith("SOUTH") else \
            [(x + dx, y + dy) for dx, dy in FACE.values()]
        if b["type"] == "hidden_item":
            spots.append((x, y))
        if not any(p in allr for p in spots):
            problems.append(f"{b.get('script', b.get('item'))} at ({x},{y}) can't be read")
    for wv in m.spec.warps:
        x, y = wv["x"], wv["y"]
        if (x, y) not in allr and not any((x + dx, y + dy) in allr for dx, dy in FACE.values()):
            problems.append(f"warp at ({x},{y}) can't be reached")
    pockets = [(x, y) for y in range(m.h) for x in range(m.w) if m.open(x, y) and (x, y) not in allr
               and (x, y) not in people | gates and m.beh[y, x] not in m.JUMP]
    if pockets:
        problems.append(f"walkable but cut off: {pockets[:8]}")
    for c in sorted(m.reach(ends, frozenset(people))):      # on foot, before the Conch
        if not set(ends) & m.reach([c], frozenset(people)):
            problems.append(f"trap at {c}")
            break
    mand, forced = [], []
    for label, a, b in segments:
        if not set(b) & m.reach(a, frozenset(people | gates)):
            problems.append(f"{label}: no way through without relics past the people")
            forced.append(None)
            continue
        forced.append(m.grass_cost(a, b, frozenset(people | gates)))
        for t in m.spec.trainers:
            cells = set(m.sight(t))
            if not set(b) & m.reach(a, frozenset(people | gates | cells)):
                mand.append(t["name"])
                for stop in m.sight(t)[:-1]:
                    if not set(b) & m.reach(a, frozenset((people - {(t["x"], t["y"])}) | gates | {stop})):
                        problems.append(f"{t['name']} could stop at {stop} and block {label}")
    for t in m.spec.trainers:
        if t["mandatory"] and t["name"] not in mand:
            problems.append(f"{t['name']}'s sight can be walked round")
        if len(m.sight(t)) < t["sight"]:
            problems.append(f"{t['name']} sees {len(m.sight(t))} of {t['sight']} cells (blocked)")
    if forced_min and max([f or 0 for f in forced] or [0]) < forced_min:
        problems.append(f"forced grass {forced} < {forced_min}")
    stacked = {}
    for t in m.spec.trainers:
        for c in m.sight(t):
            stacked[c] = stacked.get(c, 0) + 1
    if any(v >= 3 for v in stacked.values()):
        problems.append("three sight lines on one cell")
    return problems, sorted(set(mand)), forced


def walk_text(m):
    objs = {(o["x"], o["y"]): o for o in m.spec.objects()}
    sights = {c for t in m.spec.trainers for c in m.sight(t)}
    rows = ["    " + "".join(str(x % 10) for x in range(m.w))]
    for y in range(m.h):
        line = ""
        for x in range(m.w):
            o, b = objs.get((x, y)), m.beh[y, x]
            if o is not None:
                g = o["graphics_id"]
                line += "T" if o["trainer_type"] != "TRAINER_TYPE_NONE" else "*" if "CUTTABLE" in g else \
                    "R" if "BREAKABLE" in g else "B" if "BOULDER" in g else "o" if "ITEM_BALL" in g else "@"
            elif b in m.JUMP:
                line += {"MB_JUMP_SOUTH": "v", "MB_JUMP_WEST": "<", "MB_JUMP_EAST": ">"}.get(b, "^")
            elif m.water(x, y):
                line += "~"
            elif m.solid[y, x]:
                line += "#"
            elif (x, y) in sights:
                line += "!"
            elif m.grass(x, y):
                line += ","
            else:
                line += "."
        rows.append(f"{y:3d} {line}")
    return "\n".join(rows)


def render(m, out_dir, stem, views, scale=2):
    from PIL import Image, ImageDraw
    import render_map as RM
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset(m.primary, syms)),
                    RM.Tileset(RM.resolve_tileset(m.secondary, syms)))
    flat = RM.render_blocks(r, m.blocks.reshape(-1), m.w).convert("RGBA")
    for o in m.spec.objects():
        gfx = o["graphics_id"]
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE" in o["movement_type"] else "DOWN"
        try:
            if gfx == "OBJ_EVENT_GFX_ITEM_BALL":
                spr = Image.open(ROOT / "graphics/object_events/pics/misc/ball_poke.png").convert("RGBA")
                spr = spr.crop((0, 0, 16, 16))
                px = spr.load()
                key = px[0, 0]
                for j in range(16):
                    for i in range(16):
                        if px[i, j] == key:
                            px[i, j] = (0, 0, 0, 0)
                fw, fh = 16, 16
            else:
                spr, fw, fh = R5.sprite(gfx, facing)
        except (FileNotFoundError, KeyError):
            continue
        flat.paste(spr, (o["x"] * 16 + 8 - fw // 2, o["y"] * 16 + 16 - fh), spr)
    big = (m.w * 16 * scale, m.h * 16 * scale)
    flat.convert("RGB").resize(big, Image.NEAREST).save(out_dir / f"{stem}.png")
    im = flat.resize(big, Image.NEAREST)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, c = ImageDraw.Draw(ov), 16 * scale
    for y in range(m.h):
        for x in range(m.w):
            b = m.beh[y, x]
            box = [x * c, y * c, x * c + c - 1, y * c + c - 1]
            if b in m.JUMP:
                d.rectangle(box, fill=(0, 120, 255, 90))
            elif m.water(x, y):
                d.rectangle(box, fill=(0, 200, 255, 50))
            elif m.solid[y, x]:
                d.rectangle(box, fill=(255, 0, 0, 60))
            elif m.grass(x, y):
                d.rectangle(box, fill=(0, 255, 0, 45))
    for t in m.spec.trainers:
        col = (255, 160, 0, 255) if t["mandatory"] else (255, 255, 120, 255)
        for (sx, sy) in m.sight(t):
            d.rectangle([sx * c + 6, sy * c + 6, sx * c + c - 7, sy * c + c - 7], outline=col, width=3)
    Image.alpha_composite(im, ov).convert("RGB").save(out_dir / f"{stem}_walk.png")
    if not views:
        return
    shots = []
    for name, px, py in views:
        x0 = min(max(px - 7, 0), max(m.w - 15, 0)) * 16
        y0 = min(max(py - 5, 0), max(m.h - 10, 0)) * 16
        shots.append((name, flat.crop((x0, y0, x0 + 240, y0 + 160)).convert("RGB")))
    cols = 3
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 248 + 8, rows * 178 + 8), (24, 24, 32))
    sd = ImageDraw.Draw(sheet)
    for i, (name, v) in enumerate(shots):
        x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
        sheet.paste(v, (x, y + 10))
        sd.text((x, y - 2), name, fill=(230, 230, 200))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / f"{stem}_views.png")


# ---------------------------------------------------------------------------
# Route 7, the Kronia grounds (30x36, Skiron). Kithairon's col is south (its
# north edge is open at x 10-13); Thyrsa's south gate is north (its x 26-29 at
# offset 16, so ours 10-13). The top six rows draw from Thyrsa's side too, so
# they keep to aethos (K.Grid's strip).
# ---------------------------------------------------------------------------

R7_W = 44                       # 30 columns of the Kronia grounds, 14 more east for the nursery
NURSERY_DOOR = (35, 3)          # the farmhouse's door (its warp 0)
NURSERY_HOUSE = (32, 0)         # the farmhouse's 7x4 front, top-left
YARD = (31, 7, 41, 11)          # the glade the Pokemon left at the nursery roam
YARD_GATE = (37, 6)
YARD_MONS = [(34, 9), (38, 9)]  # the two roamers' home cells (wander range 2)
ARISTAIOS = (39, 5)
# aethos's farmhouse (Route 5's inn) widened to seven, the door in the middle
NURSERY = [[0x008] + [0x009] * 5 + [0x00A],
           [0x010] + [0x011] * 5 + [0x012],
           [0x018, 0x01A, 0x019, 0x01A, 0x019, 0x01A, 0x01A],
           [0x020, 0x019, 0x019, 0x021, 0x019, 0x019, 0x022]]


def plan_route7():
    W, H = 30, 36                                   # the Kronia grounds' own columns
    g = K.Grid(R7, R7_W, H, strip_top=True)
    # --- the col's foot (rows 30-35): pines, the road up from Kithairon ---------
    g.rect("#", 0, 30, W - 1, H - 1)
    g.rect("p", 10, 34, 13, H - 1)
    g.rect("p", 11, 30, 12, 33)
    g.rect(",", 10, 31, 13, 32)                     # band 1, walled by pines
    g.rect(".", 6, 31, 9, 33)                       # Manto's hollow, off the road
    g.rect(",", 6, 31, 8, 32)
    g.put(".", (5, 32))
    g.rect(".", 14, 33, 15, 34)                     # the sign's verge
    g.put("k", (15, 34))
    # --- the scree band (rows 27-29): the cut stair, a ledge home --------------
    for y, ch in ((27, "b"), (28, "u"), (29, "f")):
        g.rect(ch, 0, y, W - 1, y)
        g.rect("s" if ch == "u" else "p", 11, y, 12, y)
    g.rect(".", 19, 27, 22, 27)
    g.rect("v", 19, 28, 22, 28)
    g.rect(".", 19, 29, 22, 29)
    g.rect(",", 18, 30, 23, 31)                     # under the ledge: long grass
    g.rect(".", 14, 32, 22, 32)                     # ...and back to the road's verge
    # --- the scree meadow (rows 20-26): band 2, Doris on the narrow road --------
    g.rect("^", 0, 20, W - 1, 26)
    g.rect("p", 11, 20, 12, 26)
    g.put(".", (10, 26))                            # Euxenos at the stair's head
    g.rect(",", 10, 22, 13, 24)                     # band 2
    g.put(".", (13, 21))                            # Doris's niche
    g.rect(".", 15, 20, 24, 26)                     # the east meadow, down to the ledge
    g.rect(",", 16, 22, 23, 25)
    g.rect(".", 13, 25, 14, 25)                     # off the road above the stair
    g.put("^", (15, 20), (24, 20), (24, 26), (15, 26), (19, 23), (20, 23))
    g.rect(".", 3, 21, 8, 25)                       # a scree pocket west: the climb face
    g.rect(",", 4, 22, 7, 24)
    g.rect(".", 9, 25, 9, 25)
    g.put(".", (9, 24))
    # --- the camp wall (row 19): Hages in its gate -----------------------------
    g.rect("w", 0, 19, W - 1, 19)
    g.rect("p", 11, 19, 12, 19)
    g.put(".", (10, 18))
    # --- the Kronia field (rows 7-18) ------------------------------------------
    g.rect("#", 0, 7, W - 1, 18)
    g.rect(".", 8, 7, 21, 18)                       # the festival ground
    g.rect("p", 11, 7, 12, 18)
    g.rect("p", 8, 13, 21, 14)                      # the cross path between the tables
    g.rect("k", 13, 9, 16, 10)                      # the long tables: carts and baskets
    g.rect("k", 7, 9, 10, 10)                       # the tents
    g.rect("k", 17, 16, 20, 17)
    # Kronos's stone, west: through rubble (the Hammer)
    g.rect(".", 2, 11, 6, 16)
    g.rect("p", 7, 13, 7, 14)
    g.rect("k", 2, 11, 4, 12)                       # the mound
    g.rect(",", 2, 15, 3, 16)
    # the old vineyard, east: through vines (the Sickle), then a drum (the Girdle)
    g.rect(".", 22, 13, 27, 17)
    g.rect(",", 23, 15, 26, 17)
    g.rect("w", 22, 12, 28, 12)
    g.put("s", (25, 12))
    g.rect(".", 23, 8, 27, 11)                      # the upper terrace
    g.rect(",", 23, 8, 24, 9)
    # --- the field's north wall and the olives to the gate (rows 0-6) ----------
    g.rect("w", 0, 6, W - 1, 6)
    g.rect("s", 11, 6, 12, 6)
    g.rect("o", 0, 0, W - 1, 5)
    g.rect("p", 10, 0, 13, 0)
    g.rect("p", 11, 1, 12, 5)
    g.rect(",", 10, 2, 13, 4)                       # band 3, in the olives
    g.rect(".", 13, 4, 15, 5)
    g.put("k", (14, 4))
    # --- the Nursery of Nysa, east of the gate (x 30-43) -----------------------
    # the lane under the olives: a verge on row 4, the path on row 5
    g.rect("o", 30, 0, R7_W - 1, 5)
    g.rect(".", 16, 4, 38, 4)
    g.rect("p", 16, 5, 38, 5)
    hx, hy = NURSERY_HOUSE
    g.rect("k", hx, hy, hx + 6, hy + 3)               # the farmhouse
    g.put("k", (31, 4))                               # its sign
    g.put(".", ARISTAIOS)                             # the lane's end, over the glade
    g.rect("#", 39, 0, 39, 4)                         # a cypress or two by the farmhouse
    # the glade below the wall, in the pines: in through the wall's steps
    g.rect("w", 31, 6, 42, 6)
    g.put("#", (30, 6))                               # a pine between the field wall and the glade's
    g.put("s", YARD_GATE)
    x0, y0, x1, y1 = YARD
    g.rect(".", x0, y0, x1, y1)
    g.put("#", (x0, y0), (x1, y0), (x0, y1))
    # below the glade, the long grass where the nymphs' bees forage (wild, like the road)
    g.rect(",", 32, 12, 42, 15)
    g.rect(",", 34, 16, 40, 16)
    g.put("#", (32, 15), (42, 12), (42, 15))
    g.rect("k", 32, 7, 33, 7)                         # the hives
    g.put("k", (40, 8), (31, 10))
    return g


def props_route7(g):
    g.set(15, 34, R5.SIGN, True, "sign")
    g.set(14, 4, R5.SIGN, True, "sign")
    # the camp: tents, the bread carts and baskets, cookfires, bedrolls
    g.piece("tent", 7, 9)
    g.piece("tent_b", 9, 9)
    g.piece("cart", 13, 9)
    g.piece("baskets", 16, 9)
    g.piece("amphorae", 16, 10)
    g.piece("tent", 17, 16)
    g.piece("tent_b", 19, 16)
    g.piece("cookfire", 15, 15)
    g.piece("bedrolls", 8, 18)
    g.piece("bedrolls", 8, 16)
    g.piece("firewood", 19, 11)
    g.piece("hives", 9, 7)
    # Kronos's stone: the old mound with its stele
    g.piece("mound", 2, 11)
    g.piece("stele_family", 5, 11)
    # the old vineyard: a press's sherds and amphorae, a kiln on the terrace
    g.piece("kiln", 26, 8)
    g.piece("sherds", 27, 14)
    g.piece("amphorae", 22, 16)
    # the scree meadow: boulders, the climb face's stele
    g.piece("boulders", 19, 23)
    g.piece("stele_low", 3, 21)
    # the Nursery of Nysa: the farmhouse, a sign, the beekeeper's hives in the glade
    hx, hy = NURSERY_HOUSE
    for j, row in enumerate(NURSERY):
        for i, mid in enumerate(row):
            door = (hx + i, hy + j) == NURSERY_DOOR
            g.set(hx + i, hy + j, mid, not door, "door" if door else "house")
    g.set(31, 4, R5.SIGN, True, "sign")
    g.piece("hives", 32, 7)
    g.piece("baskets", 40, 8)
    g.piece("myrtle", 31, 10)
    for c in ((34, 7), (35, 8), (39, 7), (38, 10), (32, 9), (36, 11), (40, 10), (35, 10), (33, 11)):
        g.set(*c, R5.FLOWERS, False, "flowers")            # the glade's flowers


def spec_route7():
    s = Spec(R7)
    s.connections = [{"direction": "down", "map": "MAP_MT_KITHAIRON", "offset": 0},
                     {"direction": "up", "map": "MAP_THYRSA_CITY", "offset": -16}]
    # Trainer ids, flags, items and texts are thyrsa.py's originals.
    s.trainer("EUXENOS", "HOPLITE", 10, 26, "RIGHT", 2,
              "They said I'd come home from the war.", "That's all I wanted.")
    s.trainer("DORIS", "PILGRIM", 13, 21, "LEFT", 2,
              "A better reading. Free bread. What's the catch?", "I keep asking.")
    s.trainer("HAGES", "TITAN_GRUNT", 10, 18, "RIGHT", 2,
              "No toll. Battle for fun?", "Still no toll.")
    s.trainer("MANTO", "MANTO", 6, 33, "RIGHT", 2,
              "A true reading doesn't need a sales pitch.", "Remember that.", mandatory=False)
    s.trainer("MYRTON", "HARVESTER", 18, 13, "DOWN", 2,
              "They fed me. Nobody asked my name.", "Funny thing to be grateful for.", mandatory=False)
    s.trainer("PHILISKOS", "ACOLYTE_M", 20, 9, "LEFT", 2,
              "Even masters serve at the Kronia.", "Your turn to sit.", mandatory=False)
    s.person("Baker", "WOMAN", 14, 11, "DOWN")
    s.person("Kronist", "PILGRIM", 17, 8, "DOWN")
    s.person("Feaster", "MAN", 20, 15, "LEFT")
    s.gate("ShrineRubble", "rubble", 7, 13)
    s.gate("Vines", "thicket", 22, 14, "FLAG_ICHOR_R7_VINES_CUT")
    s.gate("Drum", "drum", 25, 13)
    s.item("ITEM_SUPER_POTION", 4, 22, "FLAG_ICHOR_ITEM_R7_HEAL")         # the scree pocket
    s.item("ITEM_GREAT_BALL", 26, 16, "FLAG_ICHOR_ITEM_R7_BALL")          # the old vineyard
    s.item("ITEM_ETHER", 19, 32, "FLAG_ICHOR_ITEM_R7_ETHER")              # under the ledge
    s.item("ITEM_HARD_STONE", 3, 14, "FLAG_ICHOR_ITEM_R7_SHRINE")         # Kronos's stone
    s.item("ITEM_PP_UP", 25, 9, "FLAG_ICHOR_ITEM_R7_TERRACE")             # the upper terrace
    s.hide("ITEM_HONEY", 9, 7, "FLAG_ICHOR_HIDDEN_ITEM_R7_HONEY")         # the camp's hives
    s.hide("ITEM_REVIVE", 27, 14, "FLAG_ICHOR_HIDDEN_ITEM_R7_REVIVE")     # the press's sherds
    s.hide("ITEM_SUPER_REPEL", 6, 31, "FLAG_ICHOR_HIDDEN_ITEM_R7_REPEL")  # Manto's hollow
    s.hide("ITEM_STARDUST", 4, 12, "FLAG_ICHOR_HIDDEN_ITEM_R7_SHRINE")    # under the stone
    s.warps = [warp(*NURSERY_DOOR, "Route7_NurseryOfNysa", 0)]
    # the two Pokemon left at the nursery, roaming the glade (VAR_OBJ_GFX_ID_0/1, set on entry)
    for i, (x, y) in enumerate(YARD_MONS):
        s.person(f"YardMon{i}", f"OBJ_EVENT_GFX_VAR_{i}", x, y, "DOWN", f"FLAG_TEMP_{i + 1}",
                 move="MOVEMENT_TYPE_WANDER_AROUND")
    s.person("Aristaios", "SHEPHERD", *ARISTAIOS, "DOWN")
    s.sign(31, 4, "NurserySign", text="THE NURSERY OF NYSA. The nymphs raise travelers' Pokémon.\\n"
           "Leave two with Makris inside. Eggs from Aristaios at the glade.")
    s.sign(15, 34, "SouthSign", text="Route 7, the Kronia grounds.\\nSouth: Mt. Kithairon. North: Thyrsa.")
    s.sign(14, 4, "NorthSign", text="Thyrsa, the south gate.\\nSouth: the Kronia grounds and Mt. Kithairon.")
    s.sign(5, 11, "Stone", text="An old stele on a grassy mound. A sickle and a swaddled stone are cut into it.\\p"
           "Under them: HE SWALLOWED IT, AND WAS FOOLED.")
    s.sign(3, 21, "Handholds", text="Old handholds climb the scree face here, worn smooth.\\p"
           "Someone with the knack could climb up to the ledge.")
    s.scripts += NURSERY_SCRIPTS
    s.scripts += [
        f'''script {s.px}Baker {{
    lock
    faceplayer
    msgbox(format("Sit. Masters carry the bread today. Hungry people eat it."))
    special(HealPlayerParty)
    if (!flag(FLAG_ICHOR_KRONIA_BREAD)) {{
        giveitem(ITEM_BARLEY_CAKE, 2)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_KRONIA_BREAD)
        }}
    }}
    msgbox(format("No oath. No payment. Take your time."))
    release
}}''',
        f'''script {s.px}Kronist {{
    lock
    faceplayer
    msgbox(format("The old readers sell you an ending. We offer a beginning.\\p"
                  "May your thread never be cut."))
    release
}}''',
        f'''script {s.px}Feaster {{
    lock
    faceplayer
    msgbox(format("At the Kronia the masters wait on the servants. One day a year.\\p"
                  "The Titanborn say it could be every day. The bread is good, anyway."))
    release
}}''',
    ]
    return s


# Route 7's ON_TRANSITION: the two Pokemon left at the nursery roam its glade
# (src/ichor_nursery.c puts their sprites in VAR_OBJ_GFX_ID_0/1); an empty
# slot's roamer hides on FLAG_TEMP_1 or _2 (VAR_0x8004/5 say which hold one).
R7_HEADER = f'''mapscripts {R7}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        special(Ichor_SetNurseryYardMons)
        if (var(VAR_0x8004) == FALSE) {{
            setflag(FLAG_TEMP_1)
        }}
        if (var(VAR_0x8005) == FALSE) {{
            setflag(FLAG_TEMP_2)
        }}
    }}
}}'''

# Aristaios, who carried the infant Dionysus to the nymphs of Nysa, keeps the
# glade and hands over the Eggs: the day-care man's script (data/scripts/
# day_care.inc's Route117_EventScript_DaycareMan) in Ichor's words.
_PX7 = R7 + "_EventScript_"
NURSERY_SCRIPTS = [
    f'''text {_PX7}Text_NameAristaios {{ "ARISTAIOS" }}''',
    f'''script {_PX7}Aristaios {{
    lock
    faceplayer
    special(GetDaycareMonNicknames)
    specialvar(VAR_RESULT, GetDaycareState)
    if (var(VAR_RESULT) == DAYCARE_EGG_WAITING) {{
        setspeaker({_PX7}Text_NameAristaios)
        msgbox(format("Ah, there you are. Your two left something in the hay this morning.\\p"
                      "An Egg. The nymphs say it's yours by right. Will you take it?"), MSGBOX_YESNO)
        if (var(VAR_RESULT) == NO) {{
            setspeaker({_PX7}Text_NameAristaios)
            msgbox(format("You're sure? Makris will raise it if you don't.\\nWill you take it after all?"), MSGBOX_YESNO)
            if (var(VAR_RESULT) == NO) {{
                setspeaker({_PX7}Text_NameAristaios)
                msgbox(format("Then it stays with the nymphs. They have raised stranger things."))
                special(RejectEggFromDayCare)
                release
                end
            }}
        }}
        specialvar(VAR_RESULT, CalculatePlayerPartyCount)
        if (var(VAR_RESULT) == PARTY_SIZE) {{
            setspeaker({_PX7}Text_NameAristaios)
            msgbox(format("Your arms are full. Make room in your party, and I'll keep it warm."))
            release
            end
        }}
        message(format("{{PLAYER}} received the Egg from Aristaios."))
        playfanfare(MUS_LEVEL_UP)
        waitfanfare
        waitbuttonpress
        setspeaker({_PX7}Text_NameAristaios)
        msgbox(format("Keep it close and keep walking. It hatches on the road."))
        special(GiveEggFromDaycare)
        release
        end
    }}
    if (var(VAR_RESULT) == DAYCARE_ONE_MON) {{
        setspeaker({_PX7}Text_NameAristaios)
        msgbox(format("Your {{STR_VAR_1}} is out in the glade with the bees and me. Doing fine."))
        release
        end
    }}
    if (var(VAR_RESULT) == DAYCARE_TWO_MONS) {{
        setspeaker({_PX7}Text_NameAristaios)
        msgbox(format("Your {{STR_VAR_1}} and {{STR_VAR_2}} are out in the glade. Doing fine."))
        special(SetDaycareCompatibilityString)
        special(ShowFieldMessageStringVar4)
        waitmessage
        waitbuttonpress
        release
        end
    }}
    setspeaker({_PX7}Text_NameAristaios)
    msgbox(format("I carried a god up this hill once, wrapped in a fawn skin, to the nymphs inside.\\p"
                  "They raised him. Leave two Pokémon with Makris and they'll raise yours.\\p"
                  "Two that get along may leave you an Egg. I watch the glade for them."))
    release
}}''',
    f'''script {_PX7}YardMon0 {{
    lock
    special(GetDaycareMonNicknames)
    msgbox(format("{{STR_VAR_1}} is rolling in the thyme. It looks happy."))
    release
}}''',
    f'''script {_PX7}YardMon1 {{
    lock
    special(GetDaycareMonNicknames)
    msgbox(format("{{STR_VAR_2}} is nosing around the hives. It looks happy."))
    release
}}''',
]

VIEWS7 = [("1 the col's foot", 11, 32), ("2 the cut stair", 12, 26), ("3 the scree meadow", 12, 22),
          ("4 the camp gate", 11, 16), ("5 the Kronia field", 14, 11), ("6 Kronos's stone", 6, 13),
          ("7 the old vineyard", 23, 12), ("8 the gate", 12, 3), ("9 the Nursery of Nysa", 36, 5),
          ("10 the nursery's glade", 36, 8)]


def build_route7():
    g = plan_route7()
    K.notch(g)
    K.bands(g)
    props_route7(g)
    K.trees(g)
    K.olives(g)
    K.ground(g)
    blocks = K.write_layout(g, "pine_tall")
    spec = spec_route7()
    write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE", header=R7_HEADER)
    m = Walked(R7, blocks, "gTileset_Skiron", spec)
    segs = [("Kithairon to Thyrsa", [(x, 35) for x in range(10, 14)], [(x, 0) for x in range(10, 14)])]
    return m, segs, VIEWS7, "route7", g.missing


# ---------------------------------------------------------------------------
# The Stymphalia painter: Route 8 and Lebadeia. Stymphalia's marsh, reeds,
# causeway, boardwalks, river, trees and Taygetos rock on aethos's grass, paths,
# sand, olives, cypresses and buildings. Plan kinds, one character per cell:
#   ~  marsh water (fishable)        r  reeds in the water (tall grass)
#   R  reed curtain (impassable)     c  the dike's deck   C  its south face
#   b  boardwalk                     =  river water        f  a ford
#   .  grass   ,  tall grass   ;  long grass   p  path   s  sand   q  scree
#   #  woods   o  olives   ^  rock (Taygetos)   k  under a placed piece
# ---------------------------------------------------------------------------

STYM = "gTileset_Stymphalia"
WALK = set(".,;psqcbfk")
WATERY = set("~rRcCb")


def smid(key, name=None, x=0, y=0):
    return LT.mid("stymphalia", key, name, x, y)


class SGrid:
    def __init__(self, name, w, h, strip=()):
        self.name, self.w, self.h = name, w, h
        self.g = [["#"] * w for _ in range(h)]
        self.mt = np.full((h, w), R5.GRASS, np.int32)
        self.solid = np.zeros((h, w), bool)
        self.wet = np.zeros((h, w), bool)
        self.fixed = np.zeros((h, w), bool)
        self.strip = set(strip)          # cells drawn only from aethos (a seam to another tileset)

    def rect(self, k, x0, y0, x1, y1):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.g[y][x] = k

    def put(self, k, *cells):
        for x, y in cells:
            self.g[y][x] = k

    def at(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def set(self, x, y, mid, solid, wet=False):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        if (x, y) in self.strip and mid >= 0x200:
            raise ValueError(f"{self.name}: Stymphalia metatile 0x{mid:03X} at ({x},{y}) in a seam strip")
        self.mt[y, x], self.solid[y, x], self.wet[y, x], self.fixed[y, x] = mid, solid, wet, True

    def stamp(self, x, y, rows, solid=True):
        for j, row in enumerate(rows):
            for i, mid in enumerate(row):
                if mid is not None:
                    self.set(x + i, y + j, mid, solid if not callable(solid) else solid(i, j))

    def spiece(self, key, x, y, names=None, solid=None):
        """A Stymphalia structure (or some of its named cells, as (name, dx, dy))."""
        s = LT.TILESETS["stymphalia"]["structures"][key]
        if names is None:
            for j in range(s["h"]):
                for i in range(s["w"]):
                    code = s["walk"][j][i]
                    self.set(x + i, y + j, s["ids"][j][i], code in "XT" if solid is None else solid)
        else:
            for name, dx, dy in names:
                cx, cy = s["names"][name]
                code = s["walk"][cy][cx]
                self.set(x + dx, y + dy, s["ids"][cy][cx], code in "XT" if solid is None else solid)

    def room(self, x, y, w, h, kinds):
        for cy in range(y, y + h):
            for cx in range(x, x + w):
                if not (0 <= cx < self.w and 0 <= cy < self.h):
                    return False
                if self.g[cy][cx] not in kinds or self.fixed[cy, cx]:
                    return False
        return True

    def mask(self, kinds):
        return [[self.g[y][x] in kinds for x in range(self.w)] for y in range(self.h)]

    def blocks(self):
        out = np.zeros((self.h, self.w), np.uint16)
        for y in range(self.h):
            for x in range(self.w):
                mid = int(self.mt[y, x]) & 0x3FF
                if self.wet[y, x]:
                    out[y, x] = mid | (1 << 12)          # water: elevation 1, no collision
                elif self.solid[y, x]:
                    out[y, x] = mid | (1 << 10)
                else:
                    out[y, x] = mid | (3 << 12)
        return out


def paint_water(g):
    marsh, reeds, curtain = g.mask(WATERY), g.mask("r"), g.mask("R")
    river = g.mask("=f")
    S = LT.TILESETS["stymphalia"]["structures"]
    for y in range(g.h):
        for x in range(g.w):
            if g.fixed[y, x]:
                continue
            k = g.g[y][x]
            if k == "~":
                g.set(x, y, smid("marsh", LT.blob_key(marsh, x, y)), False, wet=True)
            elif k == "r":
                g.set(x, y, smid("marsh_reeds", LT.blob_key(reeds, x, y)), False)
            elif k == "R":
                g.set(x, y, smid("curtain", LT.blob_key(curtain, x, y)), True)
            elif k == "=":
                g.set(x, y, smid("river", LT.blob_key(river, x, y)), False, wet=True)
            elif k == "f":
                g.set(x, y, smid("river", "ford"), False)
            elif k == "c":
                w, e = g.at(x - 1, y) == "c", g.at(x + 1, y) == "c"
                n, s = g.at(x, y - 1) == "c", g.at(x, y + 1) == "c"
                if (n or s) and not (w or e):
                    name = "V" if n and s else ("V_N" if s else "V_S")
                elif n and not s and (w or e):
                    name = "H"
                else:
                    name = "H" if w and e else ("H_W" if e else "H_E") if (w or e) else "H"
                g.set(x, y, smid("causeway", name), False)
            elif k == "C":
                w, e = g.at(x - 1, y) == "C", g.at(x + 1, y) == "C"
                g.set(x, y, smid("causeway", "face" if w and e else ("face_W" if e else "face_E")), True)
            elif k == "b":
                nb = {d: g.at(x + dx, y + dy) in WALK and g.at(x + dx, y + dy) not in ("k",)
                      for d, (dx, dy) in (("N", (0, -1)), ("S", (0, 1)), ("W", (-1, 0)), ("E", (1, 0)))}
                n, s, w, e = nb["N"], nb["S"], nb["W"], nb["E"]
                cnt = n + s + w + e
                if cnt >= 4:
                    name = "cross"
                elif cnt == 3:
                    name = {"N": "T_S", "S": "T_N", "W": "T_E", "E": "T_W"}[[d for d in "NSWE" if not nb[d]][0]]
                    # T_E has a branch east: the missing side is west
                elif n and s:
                    name = "V"
                elif w and e:
                    name = "H"
                elif n and e:
                    name = "NE"
                elif n and w:
                    name = "NW"
                elif s and e:
                    name = "SE"
                elif s and w:
                    name = "SW"
                elif n:
                    name = "end_S"
                elif s:
                    name = "end_N"
                elif w:
                    name = "end_E"
                else:
                    name = "end_W"
                g.set(x, y, smid("boardwalk", name), False)


def paint_rock(g):
    """Taygetos rock for '^': lip over face over foot on a south-facing wall,
    flanks east and west, a rim where the rock's top meets ground to the north."""
    def rock(x, y):
        k = g.at(x, y)
        return k is None or k == "^"
    for y in range(g.h):
        for x in range(g.w):
            if g.g[y][x] != "^" or g.fixed[y, x]:
                continue
            n, w, e = rock(x, y - 1), rock(x - 1, y), rock(x + 1, y)
            if not rock(x, y + 1):
                name = "foot" if w and e else ("foot_L" if not w else "foot_R")
                if not w and rock(x, y - 1) and not rock(x - 1, y - 1) and rock(x, y - 2):
                    name = "side_W_foot"
                if not e and rock(x, y - 1) and not rock(x + 1, y - 1) and rock(x, y - 2):
                    name = "side_E_foot"
                if name == "foot" and noise(x, y, 51) < 30:
                    name = "foot_b"
            elif not rock(x, y + 2):
                name = "face" if w and e else ("face_L" if not w else "face_R")
                if name == "face" and noise(x, y, 52) < 35:
                    name = "face_b"
            elif not rock(x, y + 3):
                name = "lip" if w and e else ("lip_L" if not w else "lip_R")
                if name == "lip" and noise(x, y, 53) < 30:
                    name = "lip_b"
            elif not n:
                name = "back" if w and e else ("back_NW" if not w else "back_NE")
            elif not w:
                name = "side_W"
            elif not e:
                name = "side_E"
            else:
                name = ("mass_00", "mass_10", "mass_01", "mass_11")[(x % 2) + 2 * (y % 2)]
            g.set(x, y, smid("taygetos", name), True)


def paint_woods(g):
    """Fill woods ('#') top down so the edge staggers: holm-oaks, black pines,
    walnuts and planes; aethos stone pines and cypresses in seam strips."""
    T = "trees"
    for y in range(g.h):
        for x in range(g.w):
            if g.fixed[y, x] or g.g[y][x] != "#":
                continue
            n = noise(x, y, 61 + len(g.name))
            strip = any((x + i, y + j) in g.strip for i in range(3) for j in range(3))
            if strip:
                if n < 30 and g.room(x, y, 2, 2, "#"):
                    g.stamp(x, y, R5.STONE_PINE)
                elif g.room(x, y, 1, 2, "#"):
                    g.set(x, y, R5.CYPRESS_TOP, True)
                    g.set(x, y + 1, R5.CYPRESS_BOT, True)
                continue
            pine = g.pines if hasattr(g, "pines") else 75
            if n < 30 and g.room(x, y, 2, 2, "#"):
                g.spiece(T, x, y, [("holm_TL", 0, 0), ("holm_TR", 1, 0), ("holm_BL", 0, 1), ("holm_BR", 1, 1)], True)
            elif n < pine and g.room(x, y, 2, 3, "#"):
                g.spiece(T, x, y, [("pine_TL", 0, 0), ("pine_TR", 1, 0), ("pine_ML", 0, 1), ("pine_MR", 1, 1),
                                   ("pine_BL", 0, 2), ("pine_BR", 1, 2)], True)
            elif n < pine + 10 and g.room(x, y, 3, 3, "#"):
                g.spiece(T, x, y, [(f"walnut_{i}{j}", i, j) for i in range(3) for j in range(3)], True)
            elif n < pine + 18 and g.room(x, y, 3, 3, "#"):
                g.spiece("plane", x, y, [(f"plane_{i}{j}", i, j) for i in range(3) for j in range(3)], True)
    for y in range(g.h):
        for x in range(g.w):
            if g.fixed[y, x] or g.g[y][x] != "#":
                continue
            if (x, y) in g.strip:
                if g.room(x, y, 1, 2, "#"):
                    g.set(x, y, R5.CYPRESS_TOP, True)
                    g.set(x, y + 1, R5.CYPRESS_BOT, True)
                else:
                    g.set(x, y, R5.BOULDER, True)
                continue
            if noise(x, y, 63) < 55 and g.room(x, y, 1, 2, "#"):
                g.set(x, y, R5.CYPRESS_TOP, True)       # cypress spires break up the gaps
                g.set(x, y + 1, R5.CYPRESS_BOT, True)
                continue
            g.spiece(T, x, y, [("holm_small" if noise(x, y, 62) < 60 else "shrub", 0, 0)], True)


def paint_olives(g):
    """Aethos olives in 2x2 blocks, cypress pairs among them, boulders in the gaps."""
    def free(x, y):
        return 0 <= x < g.w and 0 <= y < g.h and g.g[y][x] == "o" and not g.fixed[y, x]
    for y in range(0, g.h, 2):
        for x in range(0, g.w, 2):
            cells = [(x + i, y + j) for j in range(2) for i in range(2)]
            if not all(free(cx, cy) for cx, cy in cells):
                continue
            cyp = noise(x, y, 71) < 18
            for i in range(2):
                if cyp:
                    g.set(x + i, y, R5.CYPRESS_TOP, True)
                    g.set(x + i, y + 1, R5.CYPRESS_BOT, True)
                else:
                    g.set(x + i, y, R5.OLIVE_TOP[i], True)
                    g.set(x + i, y + 1, R5.OLIVE_BOT[i], True)
    for y in range(g.h):
        for x in range(g.w):
            if free(x, y):
                if y + 1 < g.h and free(x, y + 1):
                    g.set(x, y, R5.CYPRESS_TOP, True)
                    g.set(x, y + 1, R5.CYPRESS_BOT, True)
                else:
                    g.set(x, y, R5.BOULDER, True)


def paint_ground(g, decorate=True):
    def nine(kind, table):
        m = np.array([[g.g[y][x] in kind for x in range(g.w)] for y in range(g.h)])
        for y in range(g.h):
            for x in range(g.w):
                if g.fixed[y, x] or not m[y, x]:
                    continue

                def out(dx, dy):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < g.w and 0 <= Y < g.h):
                        return False
                    return not m[Y, X] and g.g[Y][X] in ".,;#^ok~="
                n, s, w, e = out(0, -1), out(0, 1), out(-1, 0), out(1, 0)
                key = "c" if (n and s) or (w and e) else R5.edge9(n, s, w, e)
                g.set(x, y, table[key], False)
    nine("p", R5.PATH)
    nine("s", R5.SAND)
    for y in range(g.h):
        for x in range(g.w):
            if g.fixed[y, x]:
                continue
            k = g.g[y][x]
            if k == ",":
                g.set(x, y, R5.TALL, False)
            elif k == ";":
                g.set(x, y, 0x015, False)
            elif k == "v":                           # aethos's dry-stone ledge on grass: hop south
                w, e = g.at(x - 1, y) == "v", g.at(x + 1, y) == "v"
                g.set(x, y, 0x087 if w and e else 0x0D5 if e else 0x0D6 if w else 0x087, False)
            elif k == "q":
                g.set(x, y, smid("taygetos", "scree"), False)
            elif k in ".k":
                g.set(x, y, R5.GRASS, False)
                if decorate and k == "." and (x, y) not in g.strip:
                    # flowers in beds: a bed is a 3x2 patch, and a third of a bed flowers
                    if noise(x // 3, y // 2, 81 + len(g.name)) < 10 and noise(x, y, 82) < 45:
                        g.set(x, y, R5.FLOWERS, False)
            elif k == "#":
                g.set(x, y, R5.BOULDER, True)


def paint(g, props):
    paint_water(g)
    paint_rock(g)
    props(g)
    paint_woods(g)
    paint_olives(g)
    paint_ground(g)


# ---------------------------------------------------------------------------
# Route 8, the Kopais road (72x26). Thyrsa's west gate is east (its rows 23-24
# at offset 12: ours 11-12); Lebadeia is west (our rows 17-18). The eight
# columns at the Thyrsa seam keep to aethos.
# ---------------------------------------------------------------------------
R8_W, R8_H = 72, 26
EAST_MOUTH, WEST_MOUTH = (22, 20), (8, 7)     # door cells in the ridge's south faces


def plan_route8():
    W, H = R8_W, R8_H
    g = SGrid(R8, W, H, strip={(x, y) for x in range(W - 8, W) for y in range(H)})
    # --- the lake: north shore woods, open water, Gla's island ------------------
    g.rect("~", 26, 2, 63, 17)
    g.rect("#", 26, 0, 63, 1)
    g.rect("R", 30, 2, 41, 2)                       # reed curtains along the north shore
    g.rect("R", 52, 2, 60, 2)
    g.rect("R", 62, 3, 63, 6)
    g.rect(".", 42, 3, 49, 7)                       # Gla: the island fortress
    g.rect("#", 42, 3, 43, 4)
    g.put("~", (42, 7), (49, 7), (49, 3))
    g.rect("k", 46, 3, 47, 5)                       # its tower
    g.rect("r", 33, 5, 37, 7)                       # reed islets
    g.rect("r", 55, 5, 58, 7)
    g.put("r", (34, 4), (56, 4), (36, 8))
    # --- the dike: deck rows 10-11, face row 12, two reed bars ------------------
    g.rect("c", 30, 10, 59, 11)
    g.rect("C", 30, 12, 59, 12)
    g.rect("r", 49, 9, 51, 12)                      # band 2
    g.rect("r", 37, 9, 39, 12)                      # band 3
    g.put("c", (55, 9), (44, 9))                    # landings for Enchelys and Panos
    # --- Thyrsa's olives at the seam (x 60-71) --------------------------------
    g.rect("o", 60, 0, W - 1, 9)
    g.rect("o", 60, 14, W - 1, 25)
    g.rect(".", 63, 10, W - 1, 13)                  # the verges either side of the road
    g.rect("#", 58, 13, 62, 13)
    g.put("#", (W - 1, 10), (W - 1, 13))
    g.rect("p", 60, 11, W - 1, 12)
    g.rect("p", 60, 10, 63, 10)
    g.rect(",", 60, 10, 62, 13)                     # band 1, between the olives
    g.put("k", (66, 13))                            # the east sign
    # --- the south shore (a side area): sand, the fisher, a boardwalk ----------
    g.rect("#", 29, 18, 63, 25)
    g.rect("s", 30, 18, 52, 19)                     # the sand bank
    g.rect(".", 30, 20, 52, 21)
    g.rect(";", 31, 20, 38, 23)                     # long reeds on the bank
    g.rect(",", 41, 21, 52, 23)                     # the water-meadow below the bank's step
    g.rect("v", 41, 20, 45, 20)
    g.rect(".", 53, 18, 56, 20)
    g.rect("r", 31, 14, 35, 16)                     # more reed beds in the shallows
    g.rect("r", 52, 14, 57, 15)
    g.rect("r", 50, 3, 51, 4)
    g.rect("b", 47, 13, 47, 17)                     # the boardwalk out into the reeds
    g.rect("b", 44, 14, 46, 14)
    g.rect("r", 41, 13, 43, 15)                     # its islet
    g.put(".", (47, 18))
    # --- a ragged shore: no long straight edge of water --------------------------
    for y in list(range(3, 10)) + list(range(13, 18)):
        for x, salt, cut in ((30, 91, 45), (31, 92, 18), (63, 93, 50), (62, 94, 20)):
            if g.at(x, y) == "~" and noise(x, y, salt) < cut and (x in (30, 63) or g.at(x + (1 if x == 62 else -1), y) == "#"):
                g.g[y][x] = "#"
    for x in range(31, 59):
        if g.at(x, 17) == "~" and noise(x, 17, 95) < 30:
            g.g[17][x] = "s"
    for x in range(31, 62):
        if g.at(x, 2) == "~" and noise(x, 2, 96) < 30:
            g.g[2][x] = "#"
    # --- the ridge (Mt. Ptoon's spur): pine woods over two south faces ---------
    g.rect("#", 0, 0, 29, 25)
    g.rect("^", 14, 19, 25, 21)                     # the east face, the katavothra in it
    g.rect("^", 0, 6, 13, 8)                        # the west face, the way out
    g.rect("^", 14, 11, 24, 13)                     # the spur steps up: two more faces
    g.rect("^", 15, 3, 25, 5)
    g.rect("^", 0, 0, 9, 2)
    # --- the west landing and the shore road down to the katavothra -----------
    g.rect(".", 26, 9, 29, 21)
    g.rect("p", 27, 10, 29, 11)
    g.rect("p", 27, 12, 28, 23)
    g.rect(",", 26, 16, 29, 18)                     # long grass on the shore road
    g.put("#", (26, 20), (26, 21))
    g.rect("p", 20, 22, 28, 23)
    g.rect(".", 20, 21, 25, 21)
    g.put("p", (EAST_MOUTH[0], 21))
    g.put("k", (24, 21))                            # the katavothra's stele
    g.put("#", (20, 21))
    # --- west of the ridge: the Herkyna's valley to Lebadeia --------------------
    wx = WEST_MOUTH[0]
    g.rect(".", 5, 9, 6, 11)                        # the Herkyna's pool under the face
    g.rect("=", 1, 9, 4, 11)
    g.rect("=", 2, 12, 3, 16)                       # its stream down the valley
    g.rect("f", 2, 17, 3, 18)                       # the ford where the road crosses
    g.rect("=", 2, 19, 3, 19)
    g.rect("=", 1, 20, 4, 21)
    g.rect("p", wx - 1, 9, wx, 18)                  # the road down from the mouth
    g.put("p", (wx, 8))
    g.rect(",", wx - 1, 14, wx, 16)                 # band 4, in the pines
    g.rect("p", 0, 17, wx, 18)
    g.rect(",", 4, 17, 5, 18)                       # band 5, at the ford
    g.put(".", (5, 16))                             # Thyone's niche
    g.put(".", (wx + 1, 12))                        # Meda's niche
    g.rect(".", wx + 1, 9, 12, 11)                  # the wayside shrine's clearing
    g.rect("k", 10, 9, 11, 9)
    g.rect(".", 5, 19, 12, 21)                      # a meadow below the road
    g.rect(",", 7, 20, 11, 21)
    g.put(".", (6, 19))
    g.put("k", (1, 16))                             # the west sign
    return g


def props_route8(g):
    # the mouths in the ridge's faces: aethos's cave arch over its door
    for x, y in (EAST_MOUTH, WEST_MOUTH):
        g.set(x, y - 1, R5.CAVE_TOP, True)
        g.set(x, y, R5.CAVE_DOOR, False)          # a door: walkable, the warp is on it
    g.set(66, 13, R5.SIGN, True)
    g.set(1, 16, R5.SIGN, True)
    g.spiece("tower", 46, 3, solid=True)        # its door stays shut (a hook)
    g.spiece("odds", 45, 5, [("rubble", 0, 0)], False)
    g.spiece("odds", 48, 4, [("stele", 0, 0)])
    g.spiece("phoibaion", 10, 9)
    g.spiece("odds", 12, 9, [("stele", 0, 0)])
    g.spiece("odds", 24, 21, [("stele", 0, 0)])
    g.spiece("marsh", 59, 15, [("stump", 0, 0)], True)
    g.spiece("marsh", 37, 15, [("rock", 0, 0)], True)
    g.spiece("river", 3, 20, [("tuft", 0, 0)], True)
    g.spiece("taygetos", 20, 21, [("boulders", 0, 0)])
    g.spiece("taygetos", 25, 13, [("boulder", 0, 0)])


def spec_route8():
    s = Spec(R8)
    s.connections = [{"direction": "right", "map": "MAP_THYRSA_CITY", "offset": -12},
                     {"direction": "left", "map": "MAP_LEBADEIA", "offset": 0}]
    s.warps = [warp(*EAST_MOUTH, CAVE, 0), warp(*WEST_MOUTH, CAVE, 1)]
    s.trainer("R8_ENCHELYS", "FISHER", 55, 9, "DOWN", 2,
              "Kopais eels! Best in Greece. Hold still, I'm counting the bucket.",
              "There goes my count.", "The fat ones hide under the dike. The thin ones bite.")
    s.trainer("R8_PANOS", "HOPLITE", 44, 9, "DOWN", 2,
              "The old kings built this dike. I just stand on it.", "Worth the walk.",
              "The katavothres drink the lake. The road goes in after it.")
    s.trainer("R8_SCHOINIS", "HARVESTER", 26, 15, "RIGHT", 3,
              "Reeds for roofs, reeds for flutes, reeds for you.", "Cut short.",
              "Cut a reed, three grow back. Like trainers.")
    s.trainer("R8_AMPELIS", "HARVESTER", 40, 20, "LEFT", 3,
              "The bank is soft. My footing isn't.", "Sunk.", mandatory=False)
    s.trainer("R8_KEPHALOS", "PILGRIM", 53, 18, "LEFT", 2,
              "I walked the dike to see Gla. You can't get there from here.", "Not from here, no.",
              "Someone who rides the water could reach the island.", mandatory=False)
    s.trainer("R8_MEDA", "ACOLYTE_F", 9, 12, "LEFT", 2,
              "Out of the dark already? The god's cave is darker.", "Bright enough.",
              "Lebadeia's temple takes in every traveler. Go and rest.")
    s.trainer("R8_THYONE", "AUGUR", 5, 16, "DOWN", 2,
              "The birds over Kopais all fly west tonight.", "They were right.",
              "West is Lebadeia. Follow the birds.")
    s.trainer("R8_MELAS", "SHEPHERD", 11, 19, "LEFT", 2,
              "My goats drink from the Herkyna. Nobody else may.", "Fine. One sip.", mandatory=False)
    s.person("Fisher", "FISHER", 36, 18, "UP")
    s.gate("Reeds", "thicket", 47, 17, "FLAG_ICHOR_R8_REEDS_CUT")
    s.item("ITEM_HYPER_POTION", 29, 9, "FLAG_ICHOR_ITEM_R8_HEAL")          # the landing
    s.item("ITEM_ULTRA_BALL", 44, 14, "FLAG_ICHOR_ITEM_R8_BALL")           # the boardwalk's end
    s.item("ITEM_ETHER", 12, 21, "FLAG_ICHOR_ITEM_R8_ETHER")               # the valley's corner
    s.item("ITEM_BIG_PEARL", 48, 6, "FLAG_ICHOR_ITEM_R8_GLA")              # Gla (the Conch)
    s.item("ITEM_MYSTIC_WATER", 55, 19, "FLAG_ICHOR_ITEM_R8_ISLET")        # the bank's east end
    s.hide("ITEM_HONEY", 5, 9, "FLAG_ICHOR_HIDDEN_ITEM_R8_HONEY")          # by the Herkyna's pool
    s.hide("ITEM_REVIVE", 30, 21, "FLAG_ICHOR_HIDDEN_ITEM_R8_REVIVE")      # the bank's west end
    s.hide("ITEM_SUPER_REPEL", 26, 9, "FLAG_ICHOR_HIDDEN_ITEM_R8_REPEL")   # the landing's corner
    s.sign(66, 13, "EastSign", text="Route 8, the Kopais road.\\nEast: Thyrsa. West: the dike, and Lebadeia.")
    s.sign(1, 16, "WestSign", text="Route 8, the Kopais road.\\nWest: Lebadeia. East: the katavothres and Thyrsa.")
    s.sign(10, 9, "Shrine", text="A wayside altar. Two honey cakes sit on it, untouched.\\p"
           "THE ONE WHO GOES DOWN TO TROPHONIOS RETURNS, BUT DOES NOT LAUGH.")
    s.sign(24, 21, "Katavothra", text="A katavothra. Kopais drains into the rock here.\\p"
           "The road follows the water through.")
    s.sign(47, 5, "Gla", "NORTH", text="The tower of Gla. Its door is bricked up, and the bricks are newer than the tower.")
    s.scripts.append(f'''script {s.px}Fisher {{
    lock
    faceplayer
    if (!flag(FLAG_ICHOR_R8_FISHER_GIFT)) {{
        msgbox(format("Eels, all day. The lake gives and the rock takes.\\p"
                      "You fish? Take these. They like the water."))
        giveitem(ITEM_NET_BALL, 3)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_R8_FISHER_GIFT)
        }}
        release
        end
    }}
    msgbox(format("Cast off the boardwalk. The Kopais eels feed in the reeds."))
    release
}}''')
    return s


VIEWS8 = [("1 Thyrsa's olives", 64, 11), ("2 the dike, east", 54, 10), ("3 Gla", 46, 6),
          ("4 the dike, west", 38, 11), ("5 the south bank", 44, 19), ("6 the landing", 27, 12),
          ("7 the katavothra", 23, 20), ("8 out of the rock", 8, 9), ("9 the Herkyna", 5, 16)]


def build_route8():
    g = plan_route8()
    paint(g, props_route8)
    blocks = g.blocks()
    border = [smid("trees", "holm_BL") | (1 << 10)] * 4
    write_layout(R8, blocks, border, "gTileset_Aethos", STYM)
    spec = spec_route8()
    write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE")
    m = Walked(R8, blocks, STYM, spec)
    east = [(R8_W - 1, y) for y in (11, 12)]
    segs = [("Thyrsa to the katavothra", east, [(EAST_MOUTH[0], EAST_MOUTH[1] + 1)]),
            ("the katavothra to Lebadeia", [(WEST_MOUTH[0], WEST_MOUTH[1] + 1)], [(0, 17), (0, 18)])]
    return m, segs, VIEWS8, "route8", set()


# ---------------------------------------------------------------------------
# The Kopais katavothres (40x22, cave_dark, dark). Both mouths open south onto
# Route 8: the east one by the lake, the west one into the Herkyna's valley.
# ---------------------------------------------------------------------------
CAVE_W, CAVE_H = 40, 22
CAVE_E, CAVE_W_MOUTH = (34, 20), (5, 20)        # daylight_s: lit floor over the arrow warp
CAVE_BRAZIER = (21, 7)                          # brazier_cold, 2x2
CAVE_BRAZIER_FLAG = "FLAG_ICHOR_BRAZIERS_START + 0x5A"


def plan_cave():
    W, H = CAVE_W, CAVE_H
    g = [["#"] * W for _ in range(H)]

    def rect(ch, x0, y0, x1, y1):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch
    # the east mouth: lit floor up from the daylight, then the corridor
    rect(".", 33, 13, 35, 19)
    rect(",", 33, 17, 35, 19)
    rect(".", 33, 14, 34, 16)
    rect("#", 35, 14, 35, 17)
    g[16][35] = "."                                  # Dipsas's niche
    # the sink hall, where the lake falls in, and the channel west under the ridge
    rect(".", 24, 8, 37, 12)
    rect("~", 26, 2, 37, 6)                          # the sink pool
    rect("~", 6, 3, 25, 5)                           # the channel
    rect("~", 6, 6, 14, 6)
    rect(".", 18, 3, 19, 4)                          # a rock in the channel (the Conch)
    rect(".", 26, 7, 36, 7)                          # the bank
    # the brazier hall
    rect(".", 15, 6, 25, 12)
    rect(".", 14, 7, 14, 9)
    # the drain passage west, Agamedes in a niche
    rect(".", 8, 7, 14, 8)
    g[9][11] = "."
    rect(".", 6, 7, 8, 9)
    # down to the west mouth
    rect(".", 5, 9, 7, 16)
    rect(",", 4, 16, 6, 19)
    rect(".", 7, 11, 8, 14)                          # a shelf under the handholds
    # the side gallery south of the hall, behind rubble (the Hammer)
    g[13][20] = "."
    rect(".", 16, 14, 25, 18)
    rect("#", 16, 17, 17, 18)
    rect("~", 22, 16, 25, 18)                        # a still pool in the gallery
    rect(".", 10, 15, 14, 18)                        # ...and a crawl on to the old bones
    rect(".", 14, 15, 15, 16)
    rect("#", 28, 10, 31, 12)                        # rock islands break the halls up
    rect("#", 17, 10, 18, 12)
    return g


def build_cave():
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import cave_dark_kit as kit
    cat = json.loads((ROOT / "data/tilesets/secondary/cave_dark/catalog.json").read_text())
    pieces = {p["key"]: p["ids"] for p in cat["pieces"]}
    g = plan_cave()
    W, H = CAVE_W, CAVE_H
    tiles = kit.autotile(["".join(r) for r in g], cat, "wet")
    blocks = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            t = tiles[y][x] & 0x3FF
            blocks[y, x] = t | (0x400 if g[y][x] == "#" else 0x1000 if g[y][x] == "~" else 0x3000)

    def put(x, y, ids, solid=True):
        for j, row in enumerate(ids):
            for i, mid in enumerate(row):
                blocks[y + j, x + i] = mid | (0x400 if solid else 0x3000)
    for x, y in (CAVE_E, CAVE_W_MOUTH):
        put(x, y, pieces["daylight_s"], solid=False)
    put(*CAVE_BRAZIER, pieces["brazier_cold"])
    put(36, 1, pieces["seep"])                       # the lake pouring in
    put(29, 1, pieces["seep"])
    put(8, 10, pieces["chalk_arrow_s"])              # handholds' chalk marks
    put(12, 18, pieces["bones"])
    put(5, 12, pieces["ledge_w"], solid=False)       # a rock step down toward the west mouth
    put(6, 12, pieces["ledge_e"], solid=False)
    put(33, 12, pieces["stalagmite"])
    put(15, 11, pieces["column"])
    put(24, 12, pieces["stalagmites"])
    put(36, 12, pieces["rock_pile"])
    put(32, 13, pieces["stele"])
    put(6, 15, pieces["stele"])
    put(10, 7, pieces["pebbles"], solid=False)
    put(28, 9, pieces["pebbles"], solid=False)
    write_layout(CAVE, blocks, [kit.kit_id(cat, "T|...", "wet") | 0x3400] * 4, "gTileset_Aethos", "gTileset_CaveDark")
    s = Spec(CAVE)
    s.warps = [warp(CAVE_E[0], CAVE_E[1] + 1, R8, 0), warp(CAVE_W_MOUTH[0], CAVE_W_MOUTH[1] + 1, R8, 1)]
    s.trainer("KOPAIS_DIPSAS", "TITAN_GRUNT", 35, 16, "LEFT", 2,
              "Every drain mapped, every drop counted. You're a drop.",
              "Uncounted.", "Kronos wants to know where all the water goes. So do I, now.")
    s.trainer("KOPAIS_AGAMEDES", "PILGRIM", 11, 9, "UP", 2,
              "Trophonios built Apollo's temple with his brother. Then the earth took him.",
              "It takes everyone eventually.", "Lebadeia's just beyond the light. Mind the water.")
    s.gate("GalleryRubble", "rubble", 20, 13)
    s.item("ITEM_FULL_HEAL", 14, 7, "FLAG_ICHOR_ITEM_KATAVOTHRA_PASSAGE")
    s.item("ITEM_NUGGET", 18, 15, "FLAG_ICHOR_ITEM_KATAVOTHRA_GALLERY")
    s.item("ITEM_DEEP_SEA_SCALE", 18, 3, "FLAG_ICHOR_ITEM_KATAVOTHRA_ISLET")
    s.hide("ITEM_HEART_SCALE", 36, 7, "FLAG_ICHOR_HIDDEN_ITEM_KATAVOTHRA_SEEP")
    s.hide("ITEM_RARE_BONE", 11, 18, "FLAG_ICHOR_HIDDEN_ITEM_KATAVOTHRA_BONES")
    s.sign(32, 13, "EastStele", text="THE KATAVOTHRES.\\nHere Kopais goes under the mountain.")
    s.sign(6, 15, "WestStele", text="THE KATAVOTHRES.\\nOut to the Herkyna and Lebadeia.")
    s.sign(8, 10, "Handholds", text="Chalk marks and old handholds climb the wet rock.\\p"
           "A draught comes down from somewhere above.")
    s.sign(CAVE_BRAZIER[0], CAVE_BRAZIER[1] + 1, "Brazier", "NORTH")
    s.sign(CAVE_BRAZIER[0] + 1, CAVE_BRAZIER[1] + 1, "Brazier", "NORTH")
    bx, by = CAVE_BRAZIER
    lit = pieces["brazier_lit"]
    swap = "\n".join(f"    setmetatile({bx + i}, {by + j}, 0x{lit[j][i]:03X}, TRUE)"
                     for j in range(2) for i in range(2))
    header = f'''const KV_BRAZIER = {CAVE_BRAZIER_FLAG}
mapscripts {CAVE}_MapScripts {{
    MAP_SCRIPT_ON_LOAD {{
        if (flag(KV_BRAZIER)) {{
            call({s.px}Lit)
        }}
    }}
    MAP_SCRIPT_ON_TRANSITION {{
        if (flag(KV_BRAZIER)) {{
            setflashlevel(0)
        }}
    }}
}}'''
    s.scripts += [
        f'''script {s.px}Brazier {{
    setvar(VAR_0x8004, KV_BRAZIER)
    setvar(VAR_0x8005, TRUE)
    call(EventScript_IchorBrazier)
    if (flag(KV_BRAZIER)) {{
        call({s.px}Lit)
        special(DrawWholeMapView)
    }}
    releaseall
}}''',
        f'''script {s.px}Lit {{
{swap}
    return
}}''']
    write_events(s, "MUS_ICHOR_HOLLOW", "MAP_TYPE_UNDERGROUND", header=header,
                 extra={"requires_flash": True, "allow_cycling": False, "allow_escaping": True,
                        "show_map_name": True, "weather": "WEATHER_NONE"})
    m = Walked(CAVE, blocks, "gTileset_CaveDark", s)
    east, west = [(CAVE_E[0], CAVE_E[1])], [(CAVE_W_MOUTH[0], CAVE_W_MOUTH[1])]
    return m, [("east mouth to west mouth", east, west)], [("1 east mouth", 34, 17), ("2 the sink", 30, 7),
                                                          ("3 the brazier hall", 20, 9), ("4 the drain", 9, 9),
                                                          ("5 the gallery", 18, 16), ("6 west mouth", 5, 16)], "cave", set()


# ---------------------------------------------------------------------------
# Lebadeia (36x30, Stymphalia). Route 8 is east (our rows 17-18, offset 0);
# Route 9 is south (its top is open at x 10-13, offset 0). The six rows at the
# Route 9 seam keep to aethos.
# ---------------------------------------------------------------------------
LEB_W, LEB_H = 36, 30
TEMPLE_AT = (12, 10)                             # aethos's palaestra, 6x5: its door at (+3, +4)
TEMPLE_DOOR = (TEMPLE_AT[0] + 3, TEMPLE_AT[1] + 4)
HOUSE_AT = (4, 12)                               # aethos's farmhouse, 3x4: its door at (+1, +3)
HOUSE_DOOR = (HOUSE_AT[0] + 1, HOUSE_AT[1] + 3)
ORACLE = (17, 4)                                 # the sealed mouth in the gorge wall
PALAESTRA = [[0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
             [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
             [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
             [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
             [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]]
FARMHOUSE = [[0x008, 0x009, 0x00A], [0x010, 0x011, 0x012], [0x018, 0x019, 0x01A], [0x020, 0x021, 0x022]]


def plan_lebadeia():
    W, H = LEB_W, LEB_H
    g = SGrid(LEB, W, H, strip={(x, y) for x in range(W) for y in range(H - 6, H)})
    g.pines = 70
    # --- the gorge wall, the oracle's mouth, the springs' grove ---------------
    g.rect("^", 0, 3, W - 1, 5)
    g.rect(".", 6, 6, 25, 9)
    g.rect("k", 13, 6, 14, 7)                       # the spring of Lethe
    g.rect("k", 20, 6, 21, 7)                       # the spring of Mnemosyne
    g.rect("p", ORACLE[0], 5, ORACLE[0], 8)
    g.rect("p", ORACLE[0], 8, 19, 8)
    g.rect("k", 7, 6, 9, 8)                         # a plane over the grove
    g.rect("k", 23, 6, 25, 8)
    # --- the Herkyna, out of the rock and down past the town ----------------
    g.rect("=", 27, 6, 28, 18)
    g.rect("=", 26, 9, 29, 12)                      # a pool where the springs' water gathers
    g.put("=", (25, 10), (25, 11), (30, 11))
    g.rect("=", 26, 19, 30, 22)
    g.put("=", (25, 20), (25, 21), (31, 20))
    g.rect("k", 27, 17, 28, 18)                     # the footbridge
    # --- the temple on its terrace, the temenos wall, the court --------------
    g.rect(".", 9, 9, 21, 15)
    g.rect("k", TEMPLE_AT[0], TEMPLE_AT[1], TEMPLE_AT[0] + 5, TEMPLE_AT[1] + 4)
    g.rect("p", 10, 15, 20, 15)
    g.rect("p", 19, 9, 19, 14)
    g.rect("k", 9, 16, 21, 16)                      # the temenos's front wall
    g.rect("p", 14, 16, 16, 16)                     # ...and its gate
    g.rect("k", 12, 15, 13, 15)                     # the altar before the door
    g.put("k", (11, 15))                            # the temple's sign
    # --- the honey-baker's house, west ---------------------------------------
    g.rect(".", 2, 10, 8, 16)
    g.rect("k", HOUSE_AT[0], HOUSE_AT[1], HOUSE_AT[0] + 2, HOUSE_AT[1] + 3)
    g.rect("p", HOUSE_DOOR[0], HOUSE_DOOR[1] + 1, HOUSE_DOOR[0], 16)
    g.rect("k", 2, 11, 3, 11)                       # her hives
    # --- the roads: east to Route 8, south to Route 9 --------------------------
    g.rect("p", 4, 17, W - 1, 18)
    g.rect("p", 10, 17, 13, H - 1)
    g.rect(".", 22, 9, 26, 16)                      # the meadow by the river
    g.rect(".", 29, 9, 33, 16)
    g.rect("#", 32, 9, 35, 11)                      # holm-oaks over the far bank
    g.rect("k", 30, 13, 32, 15)                     # a plane where travelers sit
    g.rect(".", 14, 19, 23, 23)                     # the town green, south of the road
    g.rect("v", 15, 21, 21, 21)                     # ...stepping down south
    g.rect(".", 4, 19, 9, 19)
    g.put("k", (14, 19))                            # the town sign
    g.rect("o", 0, 20, 9, H - 1)
    g.rect("o", 14, 24, W - 1, H - 1)
    g.rect("o", 32, 20, W - 1, 23)
    return g


def props_lebadeia(g):
    g.set(ORACLE[0], ORACLE[1] - 1, R5.CAVE_TOP, True)
    g.set(ORACLE[0], ORACLE[1], R5.CAVE_DOOR, True)     # sealed: no warp, and solid
    g.spiece("spring", 13, 6)
    g.spiece("spring", 20, 6)
    g.spiece("plane", 7, 6)
    g.spiece("plane", 23, 6)
    g.spiece("plane", 30, 13)
    g.spiece("bridge", 27, 17, [("foot_H", 0, 0), ("foot_H", 1, 0), ("foot_H", 0, 1), ("foot_H", 1, 1)], False)
    g.stamp(*TEMPLE_AT, PALAESTRA, solid=lambda i, j: not (i == 3 and j == 4))
    g.stamp(*HOUSE_AT, FARMHOUSE, solid=lambda i, j: not (i == 1 and j == 3))
    g.set(9, 16, 0x148, True)                           # the temenos wall, its gate at x 14-16
    for x in list(range(10, 14)) + list(range(17, 21)):
        g.set(x, 16, 0x149, True)
    g.set(21, 16, 0x14A, True)
    g.spiece("phoibaion", 12, 15)
    g.set(11, 15, R5.SIGN, True)
    g.set(14, 19, R5.SIGN, True)
    g.spiece("odds", 2, 11, [("post", 0, 0)])
    g.set(3, 11, smid("trees", "shrub"), True)
    g.spiece("river", 29, 21, [("tuft", 0, 0)], True)


def spec_lebadeia():
    s = Spec(LEB)
    s.connections = [{"direction": "right", "map": "MAP_ROUTE8_KOPAIS_ROAD", "offset": 0},
                     {"direction": "down", "map": "MAP_ROUTE9_PARNASSOS_CROSSROADS", "offset": 0}]
    s.warps = [warp(*TEMPLE_DOOR, TEMPLE, 0), warp(*HOUSE_DOOR, HOUSE, 0)]
    s.person("Pilgrim", "PILGRIM", 16, 7, "DOWN")
    s.person("Traveler", "MAN", 24, 15, "LEFT")
    s.person("Child", "KID_F", 17, 19, "DOWN", move="MOVEMENT_TYPE_WANDER_AROUND")
    s.item("ITEM_SITRUS_BERRY", 24, 9, "FLAG_ICHOR_ITEM_LEBADEIA")
    s.hide("ITEM_PEARL", 12, 7, "FLAG_ICHOR_HIDDEN_ITEM_LEBADEIA_SPRING")
    s.hide("ITEM_STARDUST", 20, 15, "FLAG_ICHOR_HIDDEN_ITEM_LEBADEIA_TEMENOS")
    s.sign(14, 19, "Sign", text="LEBADEIA\\nThe Trophoneion takes in travelers.\\nEast: Thyrsa. South: Kirrha.")
    s.sign(11, 15, "TempleSign", text="THE TROPHONEION\\nRest, healing and provisions for every traveler.")
    s.sign(ORACLE[0], ORACLE[1], "Oracle", "NORTH",
           text="A dark mouth in the rock, closed with a bronze grille. Cold air breathes through it.\\p"
                "A tablet: THE DESCENT IS CLOSED BY ORDER OF THE KEEPER.")
    for x in (13, 14):
        s.sign(x, 7, "Lethe", "NORTH")
    for x in (20, 21):
        s.sign(x, 7, "Mnemosyne", "NORTH")
    s.scripts += [
        f'''script {s.px}Lethe {{
    msgbox(format("LETHE. The water of forgetting.\\p"
                  "Those who went down drank here first, to forget what they had been."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Mnemosyne {{
    msgbox(format("MNEMOSYNE. The water of memory.\\p"
                  "And here, to remember what they would see below."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Pilgrim {{
    lock
    faceplayer
    msgbox(format("I came all the way from Euboia to go down to Trophonios.\\p"
                  "The keeper says the descent is closed. Something is wrong down there.\\p"
                  "So I sit by the springs and wait. Forgetting, remembering. Mostly waiting."))
    release
}}''',
        f'''script {s.px}Traveler {{
    lock
    faceplayer
    msgbox(format("Came in through the katavothres? Then you've seen where the lake goes.\\p"
                  "The temple keeps beds for travelers. Nobody pays. Lebadeia's always been that way."))
    release
}}''',
        f'''script {s.px}Child {{
    lock
    faceplayer
    msgbox(format("My grandma says people came back from the cave and never laughed again.\\p"
                  "I laugh all the time. So I'm not going."))
    release
}}''',
    ]
    return s


def build_lebadeia():
    g = plan_lebadeia()
    paint(g, props_lebadeia)
    blocks = g.blocks()
    border = [smid("trees", "holm_BL") | (1 << 10)] * 4
    write_layout(LEB, blocks, border, "gTileset_Aethos", STYM)
    spec = spec_lebadeia()
    header = f'''mapscripts {LEB}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        setrespawn(HEAL_LOCATION_LEBADEIA)
    }}
}}'''
    write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_TOWN", header=header)
    m = Walked(LEB, blocks, STYM, spec)
    segs = [("Route 8 to Route 9", [(LEB_W - 1, 17), (LEB_W - 1, 18)], [(x, LEB_H - 1) for x in range(10, 14)])]
    views = [("1 the road in", 30, 17), ("2 the Trophoneion", 15, 12), ("3 the springs", 17, 6),
             ("4 the honey house", 6, 14), ("5 the road south", 12, 24), ("6 the Herkyna", 28, 12)]
    return m, segs, views, "lebadeia", set()


# ---------------------------------------------------------------------------
# The Trophoneion (17x13, Civic): Trophonios's temple and Lebadeia's
# Asclepeion and rest-house in one hall. The healer's station and the Pithos
# against the back wall; the god in his niche beside the stair down to the
# oracle, roped off and kept; couches for sleeping pilgrims; a stall; the
# god's snakes; the descent's mosaic in the floor.
# ---------------------------------------------------------------------------
TEMPLE_W, TEMPLE_H = 17, 13
HEALER = (10, 2)


def build_temple():
    import civic_tiles as ct
    import civic_rooms as CR
    ct.define()
    r = CR.Room(TEMPLE, TEMPLE_W, TEMPLE_H, CR.checker("asc_floor_a", "asc_floor_b"))
    W = TEMPLE_W
    r.row(0, 0, ["asc_wall_top_l"] + ["asc_wall_top"] * (W - 2) + ["asc_wall_top_r"])
    r.row(1, 0, ["asc_wall_l"] + ["asc_wall"] * (W - 2) + ["asc_wall_r"])
    r.row(2, 0, [("asc_floor_a_sh" if x % 2 == 0 else "asc_floor_b_sh") for x in range(W)])
    r.put("asc_stairs", 0, 0, 2, 3)                 # the stair down to the oracle, kept shut
    r.put("asc_statue", 2, 0, 1, 3)                 # Trophonios in his niche
    r.put("asc_herbs", 4, 0, 1, 2)
    r.put("asc_jar", 5, 0, 1, 2)
    CR.healer_station(r, *HEALER)
    CR.pithos(r, 15)
    # the pilgrims' couches along the west wall, under a colonnade
    r.put_checkered("asc_kline", 0, 5, 2, 2)
    r.put_checkered("asc_kline", 0, 8, 2, 2)
    r.put_checkered("asc_column", 3, 4, 1, 3)
    r.put_checkered("asc_column", 3, 8, 1, 3)
    r.put_checkered("asc_snake", 1, 11)
    # the descent's mosaic between braziers, Trophonios's snakes beside it
    r.put("asc_mosaic", 6, 6, 3, 3)
    r.put_checkered("asc_brazier", 5, 5, 1, 2)
    r.put_checkered("asc_brazier", 9, 5, 1, 2)
    r.put_checkered("asc_snake", 5, 8)
    r.put_checkered("asc_snake", 9, 8)
    # the stall: awning, counter, the stallkeeper behind it
    r.put("ago_awning", 14, 5, 3, 2)
    r.row(7, 14, ["ago_counter_l", "ago_counter_staff", "ago_counter_r"])
    r.row(8, 14, ["ago_counter_front_l", "ago_counter_front_m", "ago_counter_front_r"])
    r.put("asc_jar", 13, 6, 1, 2)
    r.put_checkered("asc_basket_grain", 16, 10, single=True)
    r.put_checkered("asc_bench", 12, 12, 2, 1)
    r.put_checkered("asc_column", 14, 9, 1, 3)
    r.put_checkered("asc_mat", 8, 12, single=True)
    r.solid_override.update({(0, 2): True, (1, 2): True})    # the stair is roped off
    blocks = r.blocks().reshape(TEMPLE_H, W)
    write_layout(TEMPLE, blocks, [CR.block_of("void")] * 4, "gTileset_Aethos", CIVIC)
    s = Spec(TEMPLE)
    s.warps = [warp(8, 12, LEB, 0)]
    s.person("Healer", "HEALER", HEALER[0], HEALER[1], "DOWN")
    s.person("Merchant", "MERCHANT", 15, 7, "DOWN")
    s.person("Keeper", "PRIESTESS", 1, 3, "DOWN")
    s.person("Sleeper", "PILGRIM", 2, 9, "LEFT")
    s.person("Acolyte", "ACOLYTE_M", 11, 9, "LEFT")
    for x in (15, 16):
        s.sign(x, 2, "Pithos")
    s.sign(0, 2, "Descent", "NORTH")                    # the keeper stands below the other half
    s.sign(7, 7, "Mosaic", text="A floor mosaic: a man going down a dark shaft feet first,\\n"
           "a honey cake in each hand, two snakes waiting below.")
    s.sign(2, 2, "Statue", "NORTH", text="TROPHONIOS. He built Apollo's temple at Delphoi with his brother.\\p"
           "The god paid them with sleep. The earth opened for him here.")
    header = f'''mapscripts {TEMPLE}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        setrespawn(HEAL_LOCATION_LEBADEIA)
    }}
}}'''
    s.scripts += [
        f'''script {s.px}Healer {{
    setvar(VAR_0x800B, LOCALID_LEBADEIA_TROPHONEION_HEALER)
    call(Ichor_EventScript_AsclepeionHealer)
    waitmessage
    waitbuttonpress
    release
}}''',
        f'''script {s.px}Pithos {{
    lockall
    setvar(VAR_0x8004, PC_LOCATION_OTHER)
    msgbox(Ichor_Text_PithosLook)
    call(Ichor_EventScript_PithosLiftLid)
    goto({s.px}PithosMenu)
}}''',
        f'''script {s.px}PithosMenu {{
    message(Ichor_Text_PithosReach)
    waitmessage
    dynmultichoice(0, 0, FALSE, 3, 0, DYN_MULTICHOICE_CB_NONE,
        Ichor_Text_PithosOptionPokemon, Ichor_Text_PithosOptionThings, Ichor_Text_PithosOptionClose)
    switch (var(VAR_RESULT)) {{
        case 0:
            msgbox(format("The Pithos of Lebadeia opened."))
            msgbox(Ichor_Text_PithosPokemonRest)
            special(ShowPokemonStorageSystemPC)
            goto({s.px}PithosMenu)
        case 1:
            msgbox(Ichor_Text_PithosThings)
            special(PlayerPC)
            goto({s.px}PithosMenu)
    }}
    msgbox(Ichor_Text_PithosClose)
    releaseall
}}''',
        # Kirrha, Aigion and Arkadia's stalls jump here too (arkadia.py's hamlets).
        f'''script ArkadiaApproach_EventScript_Merchant {{
    lock
    faceplayer
    message(format("Stock up before the next pass."))
    waitmessage
    pokemart(ThyrsaCity_Agora_Stock)
    release
}}''',
        f'''script {s.px}Merchant {{
    goto(ArkadiaApproach_EventScript_Merchant)
}}''',
        f'''script {s.px}Keeper {{
    lock
    faceplayer
    if (!flag(FLAG_ICHOR_LEBADEIA_KEEPER_TALK)) {{
        msgbox(format("Welcome to the Trophoneion. Eat, sleep, heal. Nobody here asks for coin.\\p"
                      "That stair? It goes down to Trophonios. Once, anyone could ask him a question.\\p"
                      "You drank from Lethe, then Mnemosyne, took a honey cake in each hand,\\n"
                      "and went down feet first. Into the dark.\\p"
                      "I closed it this spring. The water below runs the wrong way now,\\n"
                      "and something answers before the god does.\\p"
                      "Here. Every traveler gets bread for the road."))
        giveitem(ITEM_BARLEY_CAKE, 2)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_LEBADEIA_KEEPER_TALK)
        }}
        release
        end
    }}
    msgbox(format("The descent stays closed. When it's safe, I'll want someone who isn't afraid of the dark."))
    release
}}''',
        f'''script {s.px}Descent {{
    msgbox(format("A narrow stair goes down into the rock, roped off with red wool.\\p"
                  "Far below, water runs. It sounds like someone whispering."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Sleeper {{
    lock
    msgbox(format("Zzz... The god... came in a dream... He said... the road is long..."))
    release
}}''',
        f'''script {s.px}Acolyte {{
    lock
    faceplayer
    msgbox(format("The snakes are Trophonios's. They take the honey cakes.\\p"
                  "Don't worry. They're fed. Mostly."))
    release
}}''',
    ]
    write_events(s, "MUS_ICHOR_ASCLEPEION", "MAP_TYPE_INDOOR", header=header,
                 extra={"allow_cycling": False, "show_map_name": False, "weather": "WEATHER_NONE"})
    return s


# ---------------------------------------------------------------------------
# Euanthe's house (10x7, Oikia): the honey-baker who makes the cakes pilgrims
# carry down to Trophonios. Bring her Honey and she bakes for you.
# ---------------------------------------------------------------------------
HOME = {
    "title": "Euanthe's house, Lebadeia", "map": "MAP_LEBADEIA_HONEY_HOUSE", "layout": HOUSE,
    "floor": "terracotta", "wall": "red",
    "grid": [
        "WWWWWWWWWW",
        "WWWWWWWWWW",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
    ],
    "rugs": [],
    "stamps": [("soot", 1, 0), ("hearth", 1, 2), ("window", 3, 0), ("honey_shelf", 4, 0), ("herbs", 6, 0),
               ("jar_shelf", 7, 0), ("mortar", 3, 4), ("table", 4, 4), ("stool", 6, 4), ("pithos", 9, 3),
               ("amphora", 0, 5), ("kline", 8, 5), ("mat", 4, 6)],
    "spots": [("warp", "door to Lebadeia (south-arrow mat)", [(4, 6), (5, 6)]),
              ("npc", "Euanthe, at her table", (5, 3), "south")],
}


def build_house():
    import oikia_art as A
    import oikia_build as B
    import oikia_rooms as RR
    base = dict(RR.ROOMS)
    base.update(RR.catalog(A.STAMPS))
    composed = {n: B.compose(sp) for n, sp in base.items()}
    order0, _ = B.collect(composed)
    composed[HOUSE] = B.compose(HOME)
    order, ids = B.collect(composed)
    if len(order) != len(order0):
        raise SystemExit(f"kopais: Euanthe's house needs {len(order) - len(order0)} cells gTileset_Oikia doesn't have")
    B.check_spots(HOUSE, HOME, composed[HOUSE])
    cells = composed[HOUSE]
    h, w = len(cells), len(cells[0])
    blocks = B.blockdata(cells, ids[HOUSE]).reshape(h, w)
    write_layout(HOUSE, blocks, [0x0210] * 4, "gTileset_Aethos", "gTileset_Oikia")
    s = Spec(HOUSE)
    s.warps = [warp(4, 6, LEB, 1), warp(5, 6, LEB, 1)]
    s.person("Euanthe", "WOMAN", 5, 3, "DOWN")
    s.scripts.append(f'''script {s.px}Euanthe {{
    lock
    faceplayer
    if (flag(FLAG_ICHOR_LEBADEIA_HONEY_TRADE)) {{
        msgbox(format("When the keeper opens the descent, come to me first.\\n"
                      "Nobody goes down to Trophonios without two of my cakes."))
        release
        end
    }}
    msgbox(format("Honey cakes for the snakes below, one in each hand. I've baked them all my life.\\p"
                  "But my bees are sulking, and the jar is empty."))
    checkitem(ITEM_HONEY)
    if (var(VAR_RESULT) == FALSE) {{
        msgbox(format("If you find wild honey on the road, bring it here. I'll make it worth your while."))
        release
        end
    }}
    msgbox(format("Is that honey? Real Kopais honey? Will you give it to me?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == NO) {{
        msgbox(format("Ah. Keep it close, then. Bees are jealous."))
        release
        end
    }}
    removeitem(ITEM_HONEY)
    msgbox(format("Bless you. Here, from my own stores. Berries keep a traveler on her feet."))
    giveitem(ITEM_SITRUS_BERRY, 3)
    if (var(VAR_RESULT) == TRUE) {{
        setflag(FLAG_ICHOR_LEBADEIA_HONEY_TRADE)
    }}
    release
}}''')
    write_events(s, "MUS_ICHOR_ROAD", "MAP_TYPE_INDOOR",
                 extra={"allow_cycling": False, "show_map_name": False, "weather": "WEATHER_NONE"})
    return s


# ---------------------------------------------------------------------------
# Wild tables, the new trainers' parties, the heal location
# ---------------------------------------------------------------------------
# Land slots run 20 20 10 10 10 10 5 5 4 4 1 1 percent. Levels per BALANCE.md:
# Route 7 closes Thyrsa's stage (wild 21-28), Route 8 and the katavothres open
# Arkadia's (26-33). Evolved forms only at or past their evolution level.
WILD = {
    R7: ("MAP_ROUTE7_KRONIA_GROUNDS", 24, 28, {
        "Morning": ["AMPELIX", "GELASABLE", "LOPHOPS", "MELIBEE", "KERAZAP", "ONOTIS",
                    "STACHYSS", "GALEKIT", "PEBBLITH", "CAIRNOLITH", "NEMECUB", "BOTRYKIT"],
        "Day": ["AMPELIX", "GELASABLE", "ONOTIS", "LOPHOPS", "MELIBEE", "KERAZAP",
                "STACHYSS", "HARPECK", "PEBBLITH", "CAIRNOLITH", "NEMECUB", "AMPELIX"],
        "Evening": ["GELASABLE", "BOTRYKIT", "AMPELIX", "ONOTIS", "LOPHOPS", "PROSOMIME",
                    "LYKOPUP", "PEBBLITH", "CAIRNOLITH", "KERAZAP", "NEMECUB", "BOTRYKIT"],
        "Night": ["BOTRYKIT", "GELASABLE", "LYKOPUP", "PROSOMIME", "PEBBLITH", "AMPELIX",
                  "SPALUNK", "CAIRNOLITH", "LYKOPUP", "BOTRYKIT", "PROSOMIME", "NEMECUB"],
    }),
    R8: ("MAP_ROUTE8_KOPAIS_ROAD", 27, 31, {
        "Morning": ["MELIBEE", "LOPHOPS", "KARKIPOOL", "GALENYON", "CHELONET", "ONOTIS",
                    "KARKITOX", "AMPELIX", "SPALUNK", "KERAZAP", "STACHYSS", "KARKITOX"],
        "Day": ["MELIBEE", "LOPHOPS", "CHELONET", "GALENYON", "KARKIPOOL", "ONOTIS",
                "AMPELIX", "KARKITOX", "KERAZAP", "SPALUNK", "STACHYSS", "KARKITOX"],
        "Evening": ["KARKIPOOL", "GALENYON", "LOPHOPS", "GELASABLE", "KARKITOX", "CHELONET",
                    "PROSOMIME", "MELIBEE", "LYKOPUP", "SPALUNK", "KARKITOX", "AMNOZE"],
        "Night": ["KARKIPOOL", "LYKOPUP", "GELASABLE", "PROSOMIME", "KARKITOX", "SPALUNK",
                  "CHELONET", "LYKOPUP", "KARKITOX", "GELASABLE", "AMNOZE", "PROSOMIME"],
    }),
    CAVE: ("MAP_KOPAIS_KATAVOTHRES", 28, 31, {
        "Morning": ["SPALUNK", "PEBBLITH", "RAKNIT", "CHELONET", "CAIRNOLITH", "SPALUNK",
                    "KARKIPOOL", "RAKNIT", "CAIRNOLITH", "PEBBLITH", "KARKITOX", "OBOLORN"],
        "Night": ["SPALUNK", "RAKNIT", "PEBBLITH", "OBOLORN", "CAIRNOLITH", "RAKNIT",
                  "KARKIPOOL", "CHELONET", "OBOLORN", "SPALUNK", "KARKITOX", "CAIRNOLITH"],
    }),
}
MIN_LEVEL = {"CAIRNOLITH": 25, "GALENYON": 24, "KARKITOX": 28}
MAX_LEVEL = {"KARKIPOOL": 27, "RAKNIT": 28, "OBOLORN": 29, "SPALUNK": 31}


def write_wild():
    path = ROOT / "src/data/wild_encounters.json"
    data = json.loads(path.read_text())
    group = next(gr for gr in data["wild_encounter_groups"] if gr.get("for_maps"))
    ids = {v[0] for v in WILD.values()} | {"MAP_LEBADEIA"}
    at = next((i for i, e in enumerate(group["encounters"]) if e.get("map") in ids), len(group["encounters"]))
    before = [e for e in group["encounters"][:at] if e.get("map") not in ids]
    after = [e for e in group["encounters"][at:] if e.get("map") not in ids]
    new = []
    for name, (mapid, lo, hi, tables) in WILD.items():
        for time, species in tables.items():
            mons = []
            for i, sp in enumerate(species):
                a = max(lo, MIN_LEVEL.get(sp, lo))
                b = min(hi, MAX_LEVEL.get(sp, hi))
                b = max(a, b if i % 3 else b - 1)
                a = min(a, b)
                mons.append({"min_level": a, "max_level": b, "species": "SPECIES_" + sp})
            e = {"map": mapid, "base_label": f"g{name}_{time}",
                 "land_mons": {"encounter_rate": 10 if name == CAVE else 25, "mons": mons}}
            if name == R8:
                e.update(json.loads(json.dumps(WT.lake(27))))          # Lake Kopais (water_tables.py)
            elif name == CAVE:
                e.update(json.loads(json.dumps(WT.pond(28))))          # the black channel
            if name == CAVE:
                e["rock_smash_mons"] = {"encounter_rate": 20, "mons": [
                    {"min_level": 28, "max_level": 30, "species": "SPECIES_PEBBLITH"},
                    {"min_level": 28, "max_level": 31, "species": "SPECIES_CAIRNOLITH"},
                    {"min_level": 28, "max_level": 30, "species": "SPECIES_SPALUNK"},
                    {"min_level": 28, "max_level": 30, "species": "SPECIES_CHELONET"},
                    {"min_level": 30, "max_level": 31, "species": "SPECIES_CAIRNOLITH"}]}
            elif name == R7 and time in ("Morning", "Night"):
                e["rock_smash_mons"] = {"encounter_rate": 20, "mons": [
                    {"min_level": 24, "max_level": 27, "species": "SPECIES_PEBBLITH"},
                    {"min_level": 25, "max_level": 28, "species": "SPECIES_CAIRNOLITH"},
                    {"min_level": 24, "max_level": 26, "species": "SPECIES_SPALUNK"},
                    {"min_level": 24, "max_level": 27, "species": "SPECIES_CHELONET"},
                    {"min_level": 26, "max_level": 28, "species": "SPECIES_CAIRNOLITH"}]}
            new.append(e)
    leb = {"map": "MAP_LEBADEIA", "base_label": "gLebadeia_Morning"}       # the Herkyna's pool
    leb.update(json.loads(json.dumps(WT.pond(28))))
    new.append(leb)
    group["encounters"] = before + new + after
    plan_hook.apply(group["encounters"])  # the distribution pass has the last word (design/DISTRIBUTION.md)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


TEAMS = [  # (trainer, name, class, pic, gender, [(species, level)])
    ("R8_ENCHELYS", "ENCHELYS", "Fisher", "Fisherman", "Male", [("Karkipool", 30), ("Galenyon", 31)]),
    ("R8_SCHOINIS", "SCHOINIS", "Harvester", "Harvester", "Female", [("Ampelix", 30), ("Stachyss", 30), ("Karkitox", 31)]),
    ("KOPAIS_AGAMEDES", "AGAMEDES", "Pilgrim", "Pilgrim", "Male", [("Chelonet", 31), ("Cairnolith", 32)]),
    ("KOPAIS_DIPSAS", "DIPSAS", "Titanborn", "Titan Grunt", "Male", [("Raknit", 30), ("Spalunk", 31), ("Prosomime", 32)]),
]


def write_teams():
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Kopais road teams: generated by tools/ichor/maps/kopais.py. */", "/* End Kopais road teams. */"
    text = path.read_text()
    if start in text:
        before, _, old = text.partition(start)
        after = old.partition(end)[2]
    else:
        before, after = text, "\n"
    out = before.rstrip() + "\n\n" + start + "\n"
    for tid, name, cls, pic, gender, mons in TEAMS:
        out += f"\n=== TRAINER_ICHOR_{tid} ===\nName: {name}\nClass: {cls}\nPic: {pic}\nGender: {gender}\n"
        out += f"Music: {gender}\nAI: Basic Trainer\n"
        for sp, lv in mons:
            out += f"\n{sp}\nLevel: {lv}\nIVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    path.write_text(out + "\n" + end + after)


def write_heal():
    path = ROOT / "src/data/heal_locations.json"
    data = json.loads(path.read_text())
    items = data["heal_locations"] if isinstance(data, dict) else data
    for h in items:
        if h["id"] == "HEAL_LOCATION_LEBADEIA":
            h.update(map="MAP_LEBADEIA", x=TEMPLE_DOOR[0], y=TEMPLE_DOOR[1] + 1,
                     respawn_map="MAP_LEBADEIA_TROPHONEION", respawn_npc="LOCALID_LEBADEIA_TROPHONEION_HEALER",
                     respawn_x=HEALER[0], respawn_y=HEALER[1] + 3)
    path.write_text(json.dumps(data, indent=2) + "\n")


# MAIN_MARKER


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--only", help="comma-separated stems: route7,route8,cave,lebadeia")
    args = ap.parse_args()
    if not K.CAT.exists():
        sys.exit(f"{K.CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    builders = [build_route7, build_route8, build_cave, build_lebadeia]
    build_temple()
    build_house()
    write_wild()
    write_teams()
    write_heal()
    if args.render:
        import render_map as RM
        for lay, stem in ((TEMPLE, "lebadeia_trophoneion"), (HOUSE, "lebadeia_honey_house")):
            out = Path(args.render) / f"{stem}.png"
            img = RM.main.__globals__  # noqa: F841  (render_map's CLI does the work)
            import subprocess
            subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "LAYOUT_" + const(lay),
                            "--scale", "3", "-o", str(out)], check=True, capture_output=True)
    bad = 0
    for b in builders:
        m, segs, views, stem, missing = b()
        if args.only and stem not in args.only.split(","):
            continue
        problems, mand, forced = check(m, segs, 8 if stem.startswith("route") else 0)
        if args.walk:
            print(walk_text(m))
        if args.render:
            render(m, args.render, stem, views)
        for p in problems:
            print(f"PROBLEM {m.name}: {p}")
        if missing:
            print(f"NOTE {m.name}: missing tall-grass shapes {sorted(missing)}")
        print(f"{m.name}: {m.w}x{m.h}, forced grass {forced}, {len(m.spec.trainers)} trainers, "
              f"{len(mand)} on the road ({', '.join(mand)}), {len(problems)} problems")
        bad += len(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
