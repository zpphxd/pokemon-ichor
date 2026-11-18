#!/usr/bin/env python3
"""Build the road north out of Lakonia: Route 26 (the Skiritis), Lake Stymphalia,
Route 27 (the Arkadian hills) and the Skiritai cave, with their events, scripts,
wild tables, trainer parties, herms, checks and review renders. This file owns
those maps. It also writes its two seams into the neighbours it joins: Lakonia's
north road (lakonia_town.py keeps its top rows aethos-only and roped by a cadet
until III-5J) and Arkadia's south road (the Karneia hoplite steps aside).

Design: design/phase4/SCRIPT.md Part 2 ("Route 26", "Lake Stymphalia",
"Route 27"), Part 3 (their trainers) and Part 4 (their tables); AETHOS_MAP.md;
WORLD_EXPLORATION.md §5.8 (D4, D5); LABORS.md (Labors 2 and 6). Each map's
finds and its hooks for later are in design/maps/<Map>.md.

Story. After III-5J (FLAG_ICHOR_LAKONIA_PARTED) Rhea tells the player to take
the road and make noise: the road is the story's way to Delphoi (Route 26, the
lake, Route 27, Arkadia, then Routes 12 and 11, the ferry and Route 28). The
Wings still work, so it is the long way on purpose, not a wall.

Route 26, the Skiritis (32x48). *North past the battle school's grounds.* The
running track by the upper Eurotas, the practice field (band 1), the
Platanistas in its moat (Herakles's and Lykourgos's bridges, Anaxandros on
the first), the fork with the great herm, the Phoibaion behind a cracked rock
(the Hammer), the west terrace that hops home (and its thicket, the Sickle),
the Titan columns marching on the road below the east ridge, Dienekes in the
gap between the Skiritis's walls and band 2 behind him, and the reeds.

Lake Stymphalia (42x36). *The marsh of the bronze-feathered birds.* The old
causeway from the south shore, Akanthis's stilt hut (the rest stop and its
travel herm), the long boardwalk Borboros sits on, the islets and their reed
bands, the nests' curtain and the augur, the deep reeds' side walk (Lernip's
rainy pool, a hook), the roost on the north shore (Labor 6), the reed wall that
grows back in the south-east (Labor 2), the far rock (the Conch), and the
flock that rises over the causeway the first time you cross.

Route 27, the Arkadian hills (44x36). *Over the hills into Arkadia.* Tityos's
goats, a hollow (band 1), the ravine and Othryades on its one bridge (band 2),
the Titans' lower road, the Karyai spring under walnuts (heal, berries, the
herm), the lookout's sill plates and drums (the Girdle) and the watchtower, a
cascade (the Horn), a crack with an anchor ring (the Thread), an updraft to an
eyrie (the Wings), a Titan cache under a watchman's eye (the Helm), the cave's
two mouths, Sthenelaidas at the top of the pass (band 3), and Arkadia.

The Skiritai cave (30x20, cave_dark, dark: the Torch). The scouts' climb from
the hollow up to the lookout terrace: a brazier, rubble (the Hammer), bronze
chains over the scouts' store (the Labrys), and the stair up to the high mouth.

Usage: /usr/bin/python3 tools/ichor/maps/stymphalia.py [--render DIR] [--walk] [--only STEMS]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import route5 as R5  # noqa: E402
import kopais as KP  # noqa: E402  (the Stymphalia painter, Spec, Walked, renders)
import lakonia_tiles as LT  # noqa: E402

noise = R5.noise
GFX = "OBJ_EVENT_GFX_ICHOR_"
STYM = "gTileset_Stymphalia"
FACE = KP.FACE
smid = KP.smid
const = KP.const

R26, LAKE, R27, CAVE = "Route26_Skiritis", "LakeStymphalia", "Route27_ArkadianHills", "Route27_SkiritaiCave"
MAP = {R26: "MAP_ROUTE26_SKIRITIS", LAKE: "MAP_LAKE_STYMPHALIA", R27: "MAP_ROUTE27_ARKADIAN_HILLS",
       CAVE: "MAP_ROUTE27_SKIRITAI_CAVE"}

# --- the seams -----------------------------------------------------------------------------
# Lakonia's north road is its x 24-26; Route 26 sits on Lakonia's top at offset 9.
LAKONIA_OFFSET = 9
# Route 26's top road (x 15-17) meets the lake's causeway shore (x 20-22).
LAKE_OVER_R26 = 5
# The lake's west shore (rows 11-13) meets Route 27's east end (rows 27-29).
R27_EAST_ROWS = (27, 28, 29)
LAKE_WEST_ROWS = (11, 12, 13)
R27_OFFSET = LAKE_WEST_ROWS[0] - R27_EAST_ROWS[0]      # Route 27's y 0 at the lake's y -16
# Arkadia's south road is its x 13-14; Route 27's top road is x 6-7.
ARKADIA_OFFSET = 7

FLAG_PARTED = "FLAG_ICHOR_LAKONIA_PARTED"
FLAG_AFTER = "FLAG_ICHOR_ACT3_COMPLETE"       # the Titan columns are gone after the climax

# Aethos metatiles
GRASS, TALL, SIGN, HERM, BOULDER = R5.GRASS, R5.TALL, R5.SIGN, R5.HERM, R5.BOULDER
LEDGE_S, LEDGE_W, LEDGE_E = 0x087, 0x085, 0x086
STAIR = 0x0AF                     # cut stone steps through a face (walkable)
FALL, FALL_FOOT = 0x0BB, 0x0C1    # a cascade and its splash (MB_WATERFALL; climbed by script)
BERRY_SOIL = 0x10C


# ---------------------------------------------------------------------------
# Flags: every name this file uses, claimed from world-act3's bank range
# (tools/ichor/claim_ranges.md, "Route 26, Lake Stymphalia and Route 27").
# ---------------------------------------------------------------------------
BANK_RANGE = "0x640-0x6BF"
FLAG_NOTES = {}


def flag(name, note):
    FLAG_NOTES[name] = note
    return name


def claim_flags():
    """Claim each flag this file names that flags.h doesn't define yet."""
    text = (ROOT / "include/constants/flags.h").read_text()
    for name, note in FLAG_NOTES.items():
        if re.search(rf"#define {name}\b", text):
            continue
        kind = "hiddenitem" if name.startswith("FLAG_ICHOR_HIDDEN_ITEM_") else "bankflag"
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/claim.py"), "--range", BANK_RANGE, kind, name,
                        "Stymphalia road: " + note], check=True, capture_output=True)
        text = (ROOT / "include/constants/flags.h").read_text()


# ---------------------------------------------------------------------------
# A grid on the Stymphalia painter, with a few more plan kinds:
#   v < >  aethos ledges (hop south, west, east)    S  cut stone stairs
#   X      a ravine (lip, chasm, foot by its rows)   B  a plank bridge over it
#   F      a cascade (aethos's fall)                 P  a sill plate (a drum's seat)
#   t      the Titans' lower road (path, never reached)
# ---------------------------------------------------------------------------

class Grid(KP.SGrid):
    def __init__(self, name, w, h, strip=()):
        super().__init__(name, w, h, strip)
        self.links = []          # (a, b): scripted moves between cells (Wings, Thread, Horn)
        self.exempt = set()      # walkable cells nobody reaches on purpose (the Titans' road)

    def blob(self, k, cx, cy, rx, ry, salt=0, rough=0.25, only=None):
        for y in range(cy - ry - 1, cy + ry + 2):
            for x in range(cx - rx - 1, cx + rx + 2):
                if not (0 <= x < self.w and 0 <= y < self.h):
                    continue
                d = ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2
                if d <= 1.0 + rough * (noise(x, y, salt) / 50.0 - 1.0):
                    if only is None or self.g[y][x] in only:
                        self.g[y][x] = k


def paint_extras(g):
    """The kinds KP's painters don't know; run before them (they skip fixed cells)."""
    for y in range(g.h):
        for x in range(g.w):
            k = g.g[y][x]
            if k == "v":
                w, e = g.at(x - 1, y) == "v", g.at(x + 1, y) == "v"
                g.set(x, y, LEDGE_S if w and e else 0x0D5 if e else 0x0D6 if w else LEDGE_S, False)
            elif k == "<":
                g.set(x, y, LEDGE_W, False)
            elif k == ">":
                g.set(x, y, LEDGE_E, False)
            elif k == "S":
                g.set(x, y, STAIR, False)
            elif k == "F":
                below = g.at(x, y + 1)
                g.set(x, y, FALL if below == "F" else FALL_FOOT, True)
            elif k == "P":
                g.spiece("odds", x, y, [("start", 0, 0)], False)
            elif k == "t":
                g.set(x, y, R5.PATH["c"], False)
            elif k in "XB":
                top = g.at(x, y - 1) not in ("X", "B")
                bot = g.at(x, y + 1) not in ("X", "B")
                if k == "B":
                    name = "bridge_N" if top else "bridge_S" if bot else "bridge"
                    g.spiece("ravine", x, y, [(name, 0, 0)], False)
                else:
                    base = "lip" if top else "foot" if bot else "chasm"
                    if noise(x, y, 41) < 35:
                        base += "_b"
                    g.spiece("ravine", x, y, [(base, 0, 0)], True)


def paint(g, props):
    paint_extras(g)
    KP.paint_water(g)
    KP.paint_rock(g)
    props(g)
    KP.paint_woods(g)
    KP.paint_olives(g)
    KP.paint_ground(g)


# ---------------------------------------------------------------------------
# Events. KP.Spec, plus people with scripts, relic signs and triggers.
# ---------------------------------------------------------------------------

class Spec(KP.Spec):
    def talker(self, name, gfx, x, y, text, facing="DOWN", flag="0", move=None):
        self.person(name, gfx, x, y, facing, flag, move)
        self.scripts.append(f'''script {self.px}{name} {{
    lock
    faceplayer
    msgbox(format("{text}"))
    release
}}''')

    def script(self, name, body):
        self.scripts.append(f"script {self.px}{name} {{\n{body}\n}}")

    def trigger(self, x, y, script, var="VAR_TEMP_1", value="0"):
        self.coords.append({"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var,
                            "var_value": value, "script": self.px + script})


def trainer_party(tid, name, cls, pic, gender, mons, music=None, iv=14, items=None):
    out = f"=== TRAINER_ICHOR_{tid} ===\nName: {name}\nClass: {cls}\nPic: {pic}\nGender: {gender}\n"
    out += f"Music: {music or gender}\n"
    if items:
        out += f"Items: {items}\n"
    out += "AI: Basic Trainer\n"
    for sp, lv in mons:
        out += f"\n{sp}\nLevel: {lv}\nIVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe\n"
    return out


TEAMS = []   # (tid, party text)


def team(tid, name, cls, pic, gender, mons, **kw):
    TEAMS.append((tid, trainer_party(tid, name, cls, pic, gender, mons, **kw)))
    return tid


# ---------------------------------------------------------------------------
# Checks: KP.check's rules, with scripted links (relics) and exempt cells
# ---------------------------------------------------------------------------

class Walk(KP.Walked):
    def __init__(self, name, blocks, secondary, spec, grid):
        super().__init__(name, blocks, secondary, spec)
        self.links = grid.links
        self.exempt = grid.exempt

    def reach(self, starts, blocked=frozenset(), surf=False, links=False):
        seen = {s for s in starts if self.open(*s, blocked)}
        q = deque(seen)
        while q:
            c = q.popleft()
            nxt = list(self.steps(*c, blocked, surf))
            if links:
                nxt += [b for a, b in self.links if a == c] + [a for a, b in self.links if b == c]
            for n in nxt:
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        return seen


def check(m, segments, forced_min=8, ends=None, floats=()):
    problems = []
    objs = m.spec.objects()
    gate_gfx = ("OBJ_EVENT_GFX_CUTTABLE_TREE", "OBJ_EVENT_GFX_BREAKABLE_ROCK", "OBJ_EVENT_GFX_PUSHABLE_BOULDER")
    gates = {(o["x"], o["y"]) for o in objs if o["graphics_id"] in gate_gfx}
    people = {(o["x"], o["y"]) for o in objs} - gates
    for o in objs:
        xy = (o["x"], o["y"])
        if (m.solid[o["y"], o["x"]] or m.water(*xy)) and xy not in m.exempt and xy not in floats:
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} on a solid or water cell {xy}")
    ends = ends or [c for _, a, b in segments for c in a + b]
    allr = m.reach(ends, frozenset(people), surf=True, links=True)
    for o in objs:
        x, y = o["x"], o["y"]
        if (x, y) in m.exempt or (x, y) in floats:
            continue
        if not any((x + dx, y + dy) in allr for dx, dy in FACE.values()):
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} at ({x},{y}) can't be reached")
    for b in m.spec.bgs():
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and not m.solid[y, x] and not m.water(x, y):
            problems.append(f"sign {b['script']} at ({x},{y}) is on walkable ground")
        f = b.get("player_facing_dir", "")
        spots = [(x, y + 1)] if f.endswith("NORTH") else [(x, y - 1)] if f.endswith("SOUTH") else \
            [(x + 1, y)] if f.endswith("WEST") else [(x - 1, y)] if f.endswith("EAST") else \
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
               and (x, y) not in people | gates and m.beh[y, x] not in m.JUMP and (x, y) not in m.exempt]
    if pockets:
        problems.append(f"walkable but cut off: {pockets[:8]}")
    foot = m.reach(ends, frozenset(people))
    for c in sorted(foot):
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


def write_events(spec, music, map_type, header=None, extra=None):
    """KP.write_events, with this file's name in the scripts' banner. A " / " in a
    trainer's line is a page break (SCRIPT.md's convention)."""
    for t in spec.trainers:
        for k in ("intro", "defeat", "after"):
            t[k] = t[k].replace(" / ", "\\p")
    KP.write_events(spec, music, map_type, header=header, extra=extra)
    p = ROOT / f"data/maps/{spec.name}/scripts.pory"
    p.write_text(p.read_text().replace("tools/ichor/maps/kopais.py", "tools/ichor/maps/stymphalia.py"))


def item_flag(mapkey, what, note):
    return flag(f"FLAG_ICHOR_ITEM_{mapkey}_{what}", note)


def hidden_flag(mapkey, what, note):
    return flag(f"FLAG_ICHOR_HIDDEN_ITEM_{mapkey}_{what}", note)


# ---------------------------------------------------------------------------
# Route 26, the Skiritis (32x48). Lakonia is south (its x 24-26 = our 15-17);
# the lake is north (our x 15-17 = its 20-22). The six rows at Lakonia's seam
# keep to aethos (MAP_DESIGN §5; TILES_lakonia.md's seam table).
# ---------------------------------------------------------------------------
R26_W, R26_H = 32, 48
R26_HERM = (12, 14)                  # land (12, 15)
R26_SIGN_S, R26_SIGN_FORK = (13, 44), (13, 16)


def plan_r26():
    W, H = R26_W, R26_H
    g = Grid(R26, W, H, strip={(x, y) for x in range(W) for y in range(H - 6, H)})
    # --- the strip at Lakonia's seam: a sunken road between stone pines --------------
    g.rect("#", 0, 42, W - 1, H - 1)
    g.rect("p", 15, 42, 17, H - 1)
    g.put(".", (14, 44), (18, 44), (14, 43), (18, 45))
    g.put("k", R26_SIGN_S)
    # --- the running track by the upper Eurotas (rows 35-41) ---------------------------
    g.rect("#", 0, 35, 23, 41)
    g.rect(".", 6, 35, 22, 41)
    g.rect("p", 7, 35, 21, 35)                      # the oval: north straight
    g.rect("p", 7, 40, 21, 40)                      # south straight
    g.rect("p", 7, 35, 8, 40)                       # the turns
    g.rect("p", 20, 35, 21, 40)
    g.rect("p", 15, 40, 17, 41)                     # the road comes up onto the track
    g.rect(";", 10, 37, 18, 38)                     # long grass in the infield
    g.put("k", (9, 37), (19, 37))                   # the turning posts
    g.put(".", (6, 41), (22, 41))
    # --- band 1: the practice field (rows 31-34), moat north, woods west, river east --
    g.rect(",", 6, 31, 22, 34)
    g.rect("#", 23, 31, 23, 41)
    g.put(".", (6, 34), (22, 34))
    # --- the upper Eurotas: down the east side, then off east to the valley --------------
    g.rect("#", 24, 17, W - 1, 41)
    g.rect("=", 24, 17, 26, 39)
    g.rect("=", 27, 36, W - 1, 39)
    g.rect("=", 23, 23, 23, 24)                     # the channel that feeds the moat
    g.put("#", (24, 17), (26, 39))
    # --- the Platanistas: a moat ring round an island (rows 18-30) -----------------------
    g.rect("=", 6, 18, 22, 30)
    g.rect(".", 8, 20, 20, 28)
    g.put("=", (8, 20), (20, 20), (8, 28), (20, 28))   # round the island's corners
    g.rect("p", 15, 20, 15, 28)                     # the island's path between the bridges
    g.rect("p", 13, 24, 17, 24)
    g.rect("s", 10, 23, 12, 25)                     # the wrestling sands at the water's edge
    g.rect("s", 18, 23, 19, 25)
    g.rect(",", 12, 20, 14, 22)                     # long grass under the planes
    g.rect(",", 16, 26, 18, 28)
    g.rect(",", 7, 13, 9, 13)
    g.put("k", (15, 18), (15, 19), (15, 29), (15, 30))  # the two bridges
    g.put(".", (7, 29))                             # the moat's islet (the Conch)
    # --- the fork (rows 13-17): the herm, Lykourgos, the spur east ---------------------
    g.rect("#", 0, 13, 23, 17)
    g.rect(".", 6, 13, 22, 17)
    g.rect("p", 14, 13, 16, 17)
    g.rect("p", 6, 15, 22, 15)
    g.put("k", R26_HERM, R26_SIGN_FORK, (16, 16), (17, 16), (16, 17), (17, 17))
    g.put(".", (12, 15))
    # the east spur: the Phoibaion in its pocket behind a cracked rock, a brook below it
    g.rect(".", 18, 12, 22, 14)
    g.rect("#", 17, 12, 17, 14)
    g.put("k", (20, 12), (21, 12))
    g.rect("=", 19, 15, 23, 17)
    g.put(".", (18, 16), (18, 17))
    g.rect("p", 6, 15, 18, 15)
    # --- the west terrace: a ledged slope that hops home (rows 13-41) ------------------
    g.rect(".", 1, 13, 4, 41)
    g.rect("#", 5, 16, 5, 41)
    g.rect(",", 1, 17, 3, 19)
    g.rect("v", 1, 21, 4, 21)
    g.rect(",", 2, 23, 4, 25)
    g.rect("v", 1, 27, 4, 27)
    g.put("#", (1, 29), (1, 30))
    g.rect("v", 1, 33, 4, 33)
    g.rect(",", 1, 35, 3, 37)
    g.rect(".", 4, 40, 6, 41)
    g.put("#", (4, 13), (1, 13))
    g.rect(".", 0, 24, 0, 25)                       # the thicket's pocket, west of the slope
    g.put("#", (1, 24), (1, 26), (0, 26))
    g.put(".", (1, 25), (5, 15))
    # --- the Skiritis (rows 5-12): two rock walls and the gap between them -------------
    g.rect("^", 0, 5, 13, 12)
    g.rect("^", 17, 5, 22, 11)
    g.rect(".", 14, 5, 16, 12)
    g.rect(",", 14, 6, 16, 9)                       # band 2, in the scrub behind Dienekes
    g.put(".", (13, 11))                            # Dienekes's niche
    # --- the Titans' lower road, below the east ridge (never reached) -----------------
    g.rect("^", 23, 0, 26, 16)
    g.rect("t", 27, 0, 29, 16)
    g.rect("#", 30, 0, W - 1, 16)
    g.exempt |= {(x, y) for x in range(27, 30) for y in range(0, 17)}
    # --- the last rise (rows 0-4): the north-west clearing, reeds over the lake ------------
    g.rect("#", 0, 0, 22, 4)
    g.rect("p", 15, 0, 17, 4)
    g.rect(".", 3, 1, 14, 3)
    g.rect("p", 9, 2, 14, 2)
    g.rect(",", 4, 1, 8, 3)                         # optional grass, the shepherd's meadow
    g.rect("~", 18, 0, 21, 2)                       # the lake's reeds show over the rise
    g.rect("r", 19, 1, 21, 2)
    g.rect(".", 18, 3, 22, 4)                       # the ridge's edge: the columns in view
    return g


def props_r26(g):
    g.set(*R26_SIGN_S, SIGN, True)
    g.set(*R26_SIGN_FORK, SIGN, True)
    g.set(*R26_HERM, HERM, True)
    for x in (9, 19):                                # the track's turning posts
        g.spiece("odds", x, 37, [("post", 0, 0)])
    g.spiece("odds", 16, 39, [("start", 0, 0)], False)   # the starting sill
    for y in (18, 19):                               # Lykourgos's bridge (north), Herakles's (south)
        g.spiece("bridge", 15, y, [("foot_V_N" if y == 18 else "foot_V_S", 0, 0)], False)
    for y in (29, 30):
        g.spiece("bridge", 15, y, [("foot_V_N" if y == 29 else "foot_V_S", 0, 0)], False)
    g.spiece("statues", 16, 16, [("lykourgos", 0, 0), ("lykourgos_base", 0, 1)])
    g.set(16, 16, smid("statues", "lykourgos"), False)
    g.set(17, 16, GRASS, False)
    g.set(17, 17, GRASS, False)
    g.spiece("statues", 13, 31, [("herakles", 0, 0), ("herakles_base", 0, 1)])
    g.set(13, 31, smid("statues", "herakles"), False)
    g.spiece("phoibaion", 20, 12)
    # the island's plane trees: one at each corner, the biggest north-east
    for x, y in ((9, 21), (17, 21), (9, 25), (17, 25)):
        g.spiece("plane", x, y, [(f"plane_{i}{j}", i, j) for i in range(3) for j in range(3)])
    g.spiece("marsh", 20, 1, [("stump", 0, 0)], True)
    g.spiece("taygetos", 2, 39, [("boulders", 0, 0)])
    g.spiece("taygetos", 22, 12, [("boulder", 0, 0)])


def spec_r26():
    s = Spec(R26)
    s.connections = [{"direction": "down", "map": "MAP_LAKONIA", "offset": -LAKONIA_OFFSET},
                     {"direction": "up", "map": MAP[LAKE], "offset": -LAKE_OVER_R26}]
    L = "Lakonian"
    # --- trainers (SCRIPT Part 3's three, and six more for MAP_DESIGN §8's late density) --
    s.trainer("ANAXILAS", "CADET", 12, 40, "RIGHT", 3,
              "Lap forty! Or forty-one. Battle me while I count.",
              "Now I've lost the count AND the battle.",
              "The island's past the field. Two bridges. Pick one and don't fall in.", mandatory=False)
    team("ANAXILAS", "ANAXILAS", L, "Camper", "Male", [("Hoplomex", 50), ("Gelasable", 50)])
    s.trainer("R26_DROMAS", "CADET_F", 21, 37, "DOWN", 2,
              "Out of my lane! …Fine. In it, then. Battle!",
              "I'd have won if it was a race.",
              "Cadets run the track barefoot, in winter. It's character. Apparently.", mandatory=False)
    team("R26_DROMAS", "DROMAS", L, "Picnicker", "Female", [("Harpelle", 50), ("Kerazap", 50)])
    s.trainer("ANAXANDROS", "CADET", 15, 27, "DOWN", 1,
              "Herakles's bridge is my team's. Cross it and you're on my side. Or in the moat.",
              "…Fine. You're on my side. Welcome to the team. We lost.",
              "Out by Lykourgos's bridge. Nobody ever says thank you to Lykourgos.")
    team("ANAXANDROS", "ANAXANDROS", L, "Camper", "Male", [("Dorydrake", 50), ("Geogrip", 51), ("Hoplektor", 51)])
    s.trainer("R26_PALAISTES", "CADET", 11, 24, "LEFT", 2,
              "You're on the island, so you're in the fight. Those are the rules.",
              "Thrown in. Spiritually.",
              "Last team standing on the island wins. I'm standing. Sort of.", mandatory=False)
    team("R26_PALAISTES", "PALAISTES", L, "Camper", "Male", [("Hoplomex", 50), ("Cairnolith", 51)])
    s.trainer("R26_ARGEIOS", "TITAN_GRUNT", 19, 13, "DOWN", 1,
              "I fell out of the column. On purpose. Don't tell them.",
              "They'll never notice. That's the sad part.",
              "The altar's older than the school. The boys still leave it honey.", mandatory=False)
    team("R26_ARGEIOS", "ARGEIOS", "Titanborn", "Titan Grunt", "Male", [("Kolossard", 50), ("Plouteras", 51)])
    s.trainer("R26_PHRYNON", "AUGUR", 9, 14, "DOWN", 2,
              "The birds over the ridge fly north with the columns. I'm counting both.",
              "Counted out.",
              "Every column that goes north, nothing comes back south. Not even birds.", mandatory=False)
    team("R26_PHRYNON", "PHRYNON", "Augur", "Augur", "Male", [("Sophowl", 50), ("Belornis", 51)])
    s.trainer("R26_KRYPTIS", "CADET_F", 2, 30, "DOWN", 2,
              "Skiritai scouts learn the terrace first. Down's easy. Up's the lesson.",
              "Lesson learned. By me.",
              "Hop the walls to get home quick. Climbing back is your problem.", mandatory=False)
    team("R26_KRYPTIS", "KRYPTIS", L, "Picnicker", "Female", [("Nemeleon", 50), ("Gelasable", 51)])
    s.trainer("DIENEKES", "HOPLITE", 13, 11, "RIGHT", 3,
              "Seen you coming for a mile. That's the job. Now, the other job.",
              "Should've seen that coming too.",
              "They say the Titans' arrows will blot out the sun. / Good. We'll fight in the shade.")
    team("DIENEKES", "DIENEKES", L, "Hoplite", "Male", [("Cairnolith", 51), ("Harpelle", 51)])
    s.trainer("R26_AIPOLOS", "SHEPHERD", 6, 2, "DOWN", 1,
              "My goats graze the scouts' meadow. The scouts graze my goats.",
              "Even the goats saw that.",
              "From the rise you can see the lake. Don't look at the birds too long.", mandatory=False)
    team("R26_AIPOLOS", "AIPOLOS", "Shepherd", "Shepherd", "Male", [("Kerazap", 50), ("Chelonet", 51)])
    # --- people and set pieces --------------------------------------------------------------
    s.talker("Runner", "CADET", 7, 37, "Run. Turn at the post. Run. That's the whole agoge, really.",
             move="MOVEMENT_TYPE_WALK_UP_AND_DOWN")
    s.talker("Wrestler", "CADET", 18, 24,
             "Two teams. One island. Last team standing on it wins.\\p"
             "I've been thrown in four times this morning.\\pI'm winning, though. Spiritually.", facing="LEFT")
    s.person("WrestlerTwo", "CADET_F", 12, 25, "RIGHT")
    gift = flag("FLAG_ICHOR_GOT_R26_WRESTLERS_BAND", "the island's wrestler gave her headband")
    s.script("WrestlerTwo", f'''    lock
    faceplayer
    if (flag({gift})) {{
        msgbox(format("Herakles's side always loses. Don't tell Anaxandros."))
        release
        end
    }}
    msgbox(format("You came over Herakles's bridge and you're still dry? Respect.\\p"
                  "Here. The team's headband. We lost anyway."))
    giveitem(ITEM_MUSCLE_BAND)
    if (var(VAR_RESULT) == TRUE) {{
        setflag({gift})
    }}
    release''')
    for i, y in enumerate((2, 5, 8, 11, 14)):
        s.person(f"Column{i + 1}", "TITAN_GRUNT", 28, y, "UP", FLAG_AFTER, move="MOVEMENT_TYPE_WALK_IN_PLACE_UP")
        s.scripts.append(f"script {s.px}Column{i + 1} {{\n    end\n}}")
    # --- relic gates and finds ----------------------------------------------------------------
    s.gate("PhoibaionRock", "rubble", 18, 15, flag("FLAG_ICHOR_HIDE_R26_PHOIBAION_ROCK", "the Phoibaion's rock broken"))
    s.gate("TerraceThicket", "thicket", 1, 25, flag("FLAG_ICHOR_HIDE_R26_THICKET", "the terrace thicket cut"))
    s.item("ITEM_HONEY", 20, 13, item_flag("R26", "PHOIBAION", "the honey on the Phoibaion's step"))
    s.item("ITEM_RARE_CANDY", 0, 24, item_flag("R26", "THICKET", "behind the terrace thicket"))
    s.item("ITEM_BIG_PEARL", 7, 29, item_flag("R26", "MOAT", "the moat's islet (the Conch)"))
    s.item("ITEM_ULTRA_BALL", 3, 1, item_flag("R26", "MEADOW", "the scouts' meadow"))
    s.item("ITEM_HYPER_POTION", 4, 41, item_flag("R26", "TERRACE", "the terrace's foot"))
    s.hide("ITEM_STAR_PIECE", 19, 24, hidden_flag("R26", "PLANE", "under the island's biggest plane"))
    s.hide("ITEM_PEARL", 22, 14, hidden_flag("R26", "BROOK", "the brook below the Phoibaion"))
    s.hide("ITEM_PP_UP", 16, 39, hidden_flag("R26", "SILL", "the track's starting sill"))
    s.hide("ITEM_ESCAPE_ROPE", 13, 10, hidden_flag("R26", "NICHE", "Dienekes's rock"))
    s.hide("ITEM_REVIVE", 12, 13, hidden_flag("R26", "HERM", "behind the herm"))
    # --- signs ----------------------------------------------------------------------------------
    s.sign(*R26_SIGN_S, "SouthSign", text="ROUTE 26\\nNorth past the training grounds to Lake Stymphalia.")
    s.sign(*R26_SIGN_FORK, "ForkSign", text="SOUTH: LAKONIA. NORTH: STYMPHALIA.\\nEAST: the old altar.")
    s.sign(*R26_HERM, "Herm", text=None)
    s.script("Herm", '''    lockall
    msgbox(format("SOUTH: LAKONIA. NORTH: STYMPHALIA.\\pA herm of Hermes, at the crossing of the boys' road and the scouts'."))
    call(EventScript_IchorAnointHerm)
    releaseall''')
    s.sign(13, 32, "Herakles", text="A bridge onto the island, with a statue of Herakles at its head.\\p"
           "The other bridge has Lykourgos. You choose your bridge, and then you fight.")
    s.sign(16, 17, "Lykourgos", text="Lykourgos the lawgiver, bearded, with his staff.\\p"
           "Under him: NO WALLS. THE WALLS OF LAKONIA ARE ITS MEN.")
    s.sign(20, 12, "Phoibaion", text="The Phoibaion. Two teams made their offering here before the fight.\\p"
           "A puppy for the war god, in the old days. Now it's honey.")
    s.sign(21, 12, "Phoibaion")
    s.sign(23, 3, "Columns", "EAST")
    s.script("Columns", '''    lockall
    if (flag(FLAG_ICHOR_ACT3_COMPLETE)) {
        msgbox(format("The road below is empty. A helmet lies in the dust, upside down, full of rain."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("Below the ridge, a line of bronze helmets marches north. It doesn't end.\\p"
                      "Some of them are singing. Some of them are boys."), MSGBOX_DEFAULT)
    }
    releaseall''')
    s.sign(9, 37, "Post", text="The turning post. Cadets round it a hundred times a day.\\p"
           "The stone's worn smooth on one side only.")
    return s


VIEWS26 = [("1 Lakonia's north road", 16, 44), ("2 the running track", 14, 37), ("3 the practice field", 14, 32),
           ("4 Herakles's bridge", 15, 28), ("5 the Platanistas", 14, 23), ("6 the fork and the herm", 14, 15),
           ("7 the Phoibaion", 20, 13), ("8 the west terrace", 3, 27), ("9 Dienekes's gap", 15, 9),
           ("10 the Titans' road", 26, 6), ("11 the last rise", 14, 2)]


def build_r26():
    g = plan_r26()
    paint(g, props_r26)
    blocks = g.blocks()
    border = [smid("trees", "holm_BL") | (1 << 10)] * 4
    KP.write_layout(R26, blocks, border, "gTileset_Aethos", STYM)
    spec = spec_r26()
    write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE")
    m = Walk(R26, blocks, STYM, spec, g)
    south = [(x, R26_H - 1) for x in range(15, 18)]
    north = [(x, 0) for x in range(15, 18)]
    return m, [("Lakonia to the lake", south, north)], VIEWS26, "route26", set()


# ---------------------------------------------------------------------------
# Lake Stymphalia (42x36). Route 26 is south (our x 20-22 = its 15-17); Route 27
# is west (our rows 11-13 = its 27-29). One tileset on all three: no strips.
# ---------------------------------------------------------------------------
LAKE_W, LAKE_H = 42, 36
HUT = (22, 26)                     # stilt_hut 3x3: roof row 26, door (23,27), porch row 28
AKANTHIS = (24, 28)
LAKE_HERM, LAKE_PLAQUE, LAKE_LAND = (19, 32), (18, 32), (20, 32)
LAKE_SIGN_S, LAKE_SIGN_W = (23, 33), (1, 9)
FLOCK = [(17, 3), (19, 2), (21, 3), (23, 2), (25, 3), (27, 2)]   # perched on the roost's reeds


def plan_lake():
    W, H = LAKE_W, LAKE_H
    g = Grid(LAKE, W, H)
    g.rect("~", 0, 0, W - 1, H - 1)
    # --- the shores ----------------------------------------------------------------------
    g.rect("#", 0, 0, W - 1, 0)
    g.rect("#", 0, 33, W - 1, H - 1)
    g.rect(".", 6, 31, 29, 32)                      # the south shore
    g.rect("s", 9, 31, 28, 31)
    g.rect("p", 20, 31, 22, H - 1)
    g.rect(";", 7, 32, 12, 33)                      # long reeds on the bank
    g.put(".", (23, 33), (18, 33), (19, 33))
    g.put("k", LAKE_SIGN_S)
    g.rect("#", 0, 18, 4, 35)
    g.rect("#", 5, 30, 5, 35)
    g.rect(".", 0, 9, 4, 17)                        # the west shore
    g.rect("p", 0, 11, 4, 13)
    g.rect("s", 4, 9, 4, 16)
    g.rect(",", 1, 14, 3, 16)
    g.rect("v", 1, 10, 3, 10)                       # the bank's step down to the shore path
    g.put("#", (0, 9), (0, 10), (0, 14), (0, 15), (0, 16), (0, 17))   # the shore meets Route 27 only on its road
    g.put("k", LAKE_SIGN_W)
    g.rect("#", 0, 0, 1, 8)
    # --- the causeway and the long boardwalk ---------------------------------------------
    g.rect("c", 21, 24, 21, 30)
    g.rect("b", 21, 18, 21, 23)
    g.put("b", (22, 20))                            # Borboros's seat at the edge
    # Akanthis's stilt hut, off the causeway
    # islet 1, west of the causeway: Kyknos's boardwalk
    g.blob("r", 15, 28, 2, 2, salt=3)
    g.rect("b", 18, 28, 20, 28)
    # --- islet 2: band one, right behind Borboros (rows 14-17) ----------------------------
    g.rect("r", 17, 14, 25, 17)
    g.put("~", (17, 14), (25, 14), (25, 17), (17, 17))
    # the side boardwalk east to the deep reeds
    g.rect("b", 26, 15, 32, 15)
    # the stub north to the roost (a dead end that pays)
    g.rect("b", 21, 5, 21, 13)
    # --- the boardwalk west to islet 3 and Tenagos's notch ------------------------------------
    g.rect("b", 11, 15, 16, 15)
    g.put("b", (13, 14))
    # islet 3: band two (rows 11-16), Donax cutting reeds
    g.rect("r", 5, 11, 10, 16)
    g.put("~", (5, 16), (10, 11), (10, 16))
    g.rect("b", 4, 12, 4, 12) if False else None
    # the north walk from islet 3 to the nests' curtain
    g.rect("b", 7, 8, 7, 10)
    g.put("b", (8, 9))                              # Melampous's notch
    # --- the reed-bed nests, behind their curtain (north-west) ------------------------------
    g.rect("R", 2, 1, 13, 7)
    g.rect("~", 4, 2, 11, 6)
    g.blob("r", 7, 4, 3, 1, salt=5)
    g.put("r", (7, 6), (7, 7))                      # the gap, choked with reeds (the Sickle)
    # --- the north roost: curtains, the roost's reeds, the stub's end ------------------------
    g.rect("R", 14, 1, 34, 3)
    g.rect("R", 16, 4, 27, 4)
    g.put("~", (14, 4), (15, 4))
    g.rect("R", 35, 1, W - 1, 4)                    # the fog bank's reeds, north-east (Aeolus's Bag)
    # --- the deep reeds: a dead-end pool at the far east end --------------------------------
    g.rect("R", 33, 9, W - 1, 21)
    g.rect("~", 34, 11, 40, 19)
    g.blob("r", 37, 15, 3, 3, salt=7, only="~")
    g.rect("b", 33, 15, 38, 15)
    g.put("~", (37, 12), (37, 18))
    # --- the far rock (Poseidon's Conch) ------------------------------------------------------
    g.rect(".", 29, 6, 30, 7)
    # --- the south-east shore: the reed wall that grows back, the eight pools ---------------
    g.rect(".", 23, 31, 29, 32)
    g.rect("R", 30, 27, 30, 32)                     # the wall
    g.rect(".", 31, 27, W - 1, 32)
    g.rect("#", 31, 26, W - 1, 26)
    for cx, cy in ((32, 28), (35, 27), (38, 28), (32, 31), (38, 31), (33, 32), (37, 32), (35, 32)):
        g.put("~", (cx, cy), (cx + 1, cy))
    g.rect("~", 35, 29, 36, 30)                     # the ninth, in the middle
    g.rect("#", 30, 33, W - 1, H - 1)
    # rocks and stumps in the open water
    g.exempt |= {(x, y) for x in range(31, W) for y in range(27, 33)}   # behind the wall: Labor 2
    # reed beds and curtains in the open water, so no view is empty
    g.blob("R", 9, 21, 2, 1, salt=11, only="~")
    g.blob("r", 13, 23, 1, 1, salt=12, only="~")
    g.blob("R", 27, 21, 2, 2, salt=13, only="~")
    g.blob("r", 29, 25, 1, 1, salt=14, only="~")
    g.blob("R", 13, 9, 1, 1, salt=15, only="~")
    g.blob("r", 25, 8, 1, 1, salt=16, only="~")
    return g


def props_lake(g):
    g.set(*LAKE_SIGN_S, SIGN, True)
    g.set(*LAKE_SIGN_W, SIGN, True)
    g.spiece("stilt_hut", *HUT)
    g.spiece("stilt_hut", HUT[0] + 1, HUT[1] + 1, [("door", 0, 0)], True)   # the nets hang across it
    # the roost's run along the curtain's front: L M ... R, bronze glints
    for x in range(16, 28):
        name = "L" if x == 16 else "R" if x == 27 else ("M_b" if x % 3 == 0 else "M")
        g.spiece("roost", x, 4, [(name, 0, 0)], True)
    # the reed wall that grows back, with the eight pools behind it
    for y in range(27, 33):
        g.spiece("regrow", 30, y, [("wall_b" if y % 2 else "wall", 0, 0)], True)
    g.spiece("marsh", 31, 6, [("rock", 0, 0)], True)
    for i, (x, y) in enumerate(((12, 21), (27, 9), (8, 25), (30, 22), (15, 9))):
        g.spiece("marsh", x, y, [("stump" if i % 2 else "rock", 0, 0)], True)
    # Borboros's seat: the boardwalk's gap at its edge
    g.spiece("boardwalk", 21, 20, [("V_sit", 0, 0)], False)


def spec_lake():
    s = Spec(LAKE)
    s.connections = [{"direction": "down", "map": MAP[R26], "offset": LAKE_OVER_R26},
                     {"direction": "left", "map": MAP[R27], "offset": R27_OFFSET}]
    # --- trainers ------------------------------------------------------------------------------
    s.trainer("KYKNOS", "FISHER", 19, 28, "LEFT", 1,
              "The birds here drop feathers like knives. / I fish in a helmet. Battle me in one.",
              "A feather went down my collar. I'm blaming you.",
              "Akanthis in the stilt hut says there's a monster in the deep reeds. / She says that about everything.",
              mandatory=False)
    team("KYKNOS", "KYKNOS", "Fisher", "Fisherman", "Male", [("Karkitox", 51), ("Galenyon", 51)], music="Hiker")
    s.trainer("STYM_HALIA", "FISHER", 10, 31, "RIGHT", 2,
              "Shh. The eels come up when the birds go quiet.",
              "Well, now nothing's quiet.",
              "Fish off the sand at dusk. The Karkitox come in to the reeds to feed.", mandatory=False)
    team("STYM_HALIA", "HALIA", "Fisher", "Fisherman", "Female", [("Karkitox", 51), ("Chelonet", 51)], music="Hiker")
    s.trainer("TITANBORN_BORBOROS", "TITAN_GRUNT", 22, 20, "LEFT", 1,
              "In the golden age, do we still get to eat? / I've asked three times. Nobody answers.",
              "Nobody answers that either.",
              "The column won't wait. It never waits. / I'm going to sit here a while. You can step over me.")
    team("TITANBORN_BORBOROS", "BORBOROS", "Titanborn", "Titan Grunt", "Male", [("Kolossard", 51), ("Plouteras", 52)],
         music="Aqua")
    s.trainer("STYM_TENAGOS", "TITAN_GRUNT", 13, 14, "DOWN", 1,
              "Borboros sat down. I'm standing up. That's the difference between us.",
              "…Maybe I'll sit down too.",
              "They march us past the lake so the birds can count us. Or so the birds don't eat us.")
    team("STYM_TENAGOS", "TENAGOS", "Titanborn", "Titan Grunt", "Male", [("Laolith", 51), ("Kalyptor", 52)], music="Aqua")
    s.trainer("MELAMPOUS", "AUGUR", 8, 9, "LEFT", 1,
              "Bronze birds. They read nothing. I read them. Battle?",
              "The birds saw that coming. I didn't.",
              "The little ones nest in there, in the shallows. / Mornings and evenings. Wade in quiet.", mandatory=False)
    team("MELAMPOUS", "MELAMPOUS", "Augur", "Augur", "Male", [("Belornis", 52), ("Sophowl", 52), ("Galenyon", 52)],
         music="Hiker")
    s.trainer("DONAX", "HARVESTER", 6, 13, "UP", 2,
              "Reeds for roofs. Reeds for pipes. Reeds for the cadets' beds. Reeds for you!",
              "I'll cut you a pipe to cry into.",
              "The south reeds grow back while you watch. / I don't cut there. Nobody cuts there.", mandatory=False)
    team("DONAX", "DONAX", "Harvester", "Harvester", "Male", [("Karkitox", 51), ("Chelonet", 52), ("Cairnolith", 52)],
         music="Hiker")
    s.trainer("STYM_ORNITHE", "HARVESTER", 35, 15, "RIGHT", 2,
              "I lime the reeds for birds. Small ones. The big ones lime me.",
              "Stuck. Again.",
              "Akanthis taught me. Forty years in these reeds and she still has both eyes.", mandatory=False)
    team("STYM_ORNITHE", "ORNITHE", "Harvester", "Harvester", "Female", [("Belornis", 51), ("Karkitox", 52)],
         music="Hiker")
    s.trainer("STYM_SKIRITES", "CADET", 2, 15, "UP", 2,
              "Skiritai watch the west shore. I watch the Skiritai watch it.",
              "Watched that. Didn't like it.",
              "The road climbs west into the hills. Scouts on every height, so mind your manners.", mandatory=False)
    team("STYM_SKIRITES", "SKIRITES", "Lakonian", "Camper", "Male", [("Dorydrake", 51), ("Kerazap", 52)])
    s.trainer("STYM_LIMNAIA", "CADET_F", 27, 31, "LEFT", 2,
              "The reed wall moved. I swear it moved. Battle me so I stop thinking about it.",
              "Thinking about it again.",
              "Cut it and it grows back before you've put the sickle down. / Eight pools behind it. I counted through the stems.",
              mandatory=False)
    team("STYM_LIMNAIA", "LIMNAIA", "Lakonian", "Picnicker", "Female", [("Gelasable", 51), ("Harpelle", 52)])
    # --- Akanthis: the rest stop -------------------------------------------------------------------
    s.person("Akanthis", "ELDER_F", *AKANTHIS, "DOWN")
    s.script("Akanthis", f'''    lock
    faceplayer
    msgbox(format("Sit. By the fire. Everyone who crosses gets a sit. Them's the rules."))
    closemessage
    fadescreen(FADE_TO_BLACK)
    special(HealPlayerParty)
    playfanfare(MUS_HEAL)
    waitfanfare
    fadescreen(FADE_FROM_BLACK)
    // the hut is the road's rest stop: its herm on the shore goes live (MAP_DESIGN §2)
    setvar(VAR_0x8004, TOWN_HERM_STYMPHALIA)
    special(Ichor_RegisterTownHerm)
    if (flag({flag("FLAG_ICHOR_HEARD_LERNIP_RUMOR", "Akanthis told the deep reeds' rumor (SCRIPT Part 4)")})) {{
        msgbox(format("Sit. Fire's still going."))
        release
        end
    }}
    msgbox(format("Forty years I've limed birds in these reeds. Bronze ones, now. Mind your eyes.\\p"
                  "There's a thing in the deep reeds. East, down the side boards.\\p"
                  "Only in the rain. Swims up when the water's all rings.\\p"
                  "Small. Green. Too many heads for a small green thing.\\p"
                  "Three times in forty years, I've seen it. You've got young eyes.\\p"
                  "Come back when it rains. The augur'll tell you when."))
    setflag(FLAG_ICHOR_HEARD_LERNIP_RUMOR)
    release''')
    # --- the flock: perched on the roost, and the first crossing's scene ------------------------------
    for i, (x, y) in enumerate(FLOCK):
        s.person(f"Bird{i + 1}", "OBJ_EVENT_GFX_SPECIES(BELORNIS)", x, y, "DOWN")
        s.scripts.append(f"script {s.px}Bird{i + 1} {{\n    end\n}}")
    seen = flag("FLAG_ICHOR_STYMPHALIA_FLOCK_ROSE", "the bronze flock rose over the causeway")
    for x in (21,):
        s.trigger(x, 25, "Flock", "VAR_TEMP_1", "0")
    rise = "\n".join(f"    applymovement({s.lid}BIRD{i + 1}, {s.name}_Movement_Rise{i % 3})" for i in range(len(FLOCK)))
    land = "\n".join(f"    applymovement({s.lid}BIRD{i + 1}, {s.name}_Movement_Settle{i % 3})" for i in range(len(FLOCK)))
    s.script("Flock", f'''    lockall
    setvar(VAR_TEMP_1, 1)
    setflag({seen})
    applymovement(OBJ_EVENT_ID_PLAYER, Common_Movement_FaceUp)
    waitmovement(0)
    special(SpawnCameraObject)
    applymovement(OBJ_EVENT_ID_CAMERA, {s.name}_Movement_CameraNorth)
    waitmovement(0)
    playse(SE_M_HARDEN)
    msgbox(format("Clink. Clink-clink. The reeds on the north shore shift like coins in a purse."))
    closemessage
    playmoncry(SPECIES_BELORNIS, CRY_MODE_ENCOUNTER)
{rise}
    waitmovement(0)
    waitmoncry
    msgbox(format("A hundred bronze birds lift out of the reeds at once.\\p"
                  "The light off their wings turns the whole marsh the color of a shield."))
    closemessage
{land}
    waitmovement(0)
    msgbox(format("They circle once, and settle. Every bronze head is turned toward the causeway.\\pToward you."))
    closemessage
    applymovement(OBJ_EVENT_ID_CAMERA, {s.name}_Movement_CameraSouth)
    waitmovement(0)
    special(RemoveCameraObject)
    releaseall''')
    s.scripts.append(f'''movement {s.name}_Movement_CameraNorth {{ walk_up * 16 }}
movement {s.name}_Movement_CameraSouth {{ walk_down * 16 }}
movement {s.name}_Movement_Rise0 {{ fly_up walk_fast_left * 2 walk_fast_up walk_fast_right * 3 }}
movement {s.name}_Movement_Rise1 {{ fly_up walk_fast_right * 2 walk_fast_up walk_fast_left * 3 }}
movement {s.name}_Movement_Rise2 {{ fly_up walk_fast_up walk_fast_left walk_fast_right * 2 }}
movement {s.name}_Movement_Settle0 {{ walk_fast_left walk_fast_down fly_down }}
movement {s.name}_Movement_Settle1 {{ walk_fast_right walk_fast_down fly_down }}
movement {s.name}_Movement_Settle2 {{ walk_fast_left walk_fast_down fly_down }}''')
    # --- relic gates and finds ------------------------------------------------------------------------
    s.gate("NestReeds", "thicket", 7, 7, flag("FLAG_ICHOR_HIDE_STYM_NEST_REEDS", "the nests' choking reeds cut"))
    s.item("ITEM_NET_BALL", 15, 27, item_flag("STYM", "ISLET", "islet one's reeds"))
    s.item("ITEM_SHELL_BELL", 29, 6, item_flag("STYM", "FAR_ROCK", "the far rock (the Conch)"))
    s.item("ITEM_SHARP_BEAK", 7, 4, item_flag("STYM", "NESTS", "in the reed-bed nests (the Sickle)"))
    s.item("ITEM_MAX_REPEL", 1, 16, item_flag("STYM", "WEST_SHORE", "the west shore's corner"))
    s.item("ITEM_FULL_HEAL", 38, 16, item_flag("STYM", "DEEP_REEDS", "the deep reeds' islet"))
    s.hide("ITEM_BIG_PEARL", 22, 27, hidden_flag("STYM", "HUT", "under Akanthis's stilt hut"))
    s.hide("ITEM_RAZOR_CLAW", 38, 15, hidden_flag("STYM", "DEEP_END", "the deep reeds' end"))
    s.hide("ITEM_METAL_COAT", 21, 4, hidden_flag("STYM", "ROOST", "a bronze feather at the roost's foot"))
    s.hide("ITEM_HEART_SCALE", 5, 4, hidden_flag("STYM", "NEST_EGG", "an old egg in the nests"))
    s.hide("ITEM_SUPER_REPEL", 22, 33, hidden_flag("STYM", "CAUSEWAY", "the causeway's foot"))
    # --- signs ------------------------------------------------------------------------------------------
    s.sign(*LAKE_SIGN_S, "SouthSign", text="LAKE STYMPHALIA\\nKeep to the causeway. Mind the birds. They mind you.")
    s.sign(*LAKE_SIGN_W, "WestSign", text="WEST: ROUTE 27, over the hills into Arkadia.\\nEAST: the causeway, and Lakonia.")
    s.sign(23, 27, "HutDoor", text="Akanthis's hut. Nets hang in the doorway, and the smoke smells of fish and thyme.")
    s.sign(21, 4, "NorthReeds", "NORTH", text=None)
    s.script("NorthReeds", '''    lockall
    msgbox(format("The reeds here are thick with roosting birds. Their feathers clink like coins.\\p"
                  "As you step closer, a hundred bronze heads turn toward you at once.\\pYou step back."), MSGBOX_DEFAULT)
    releaseall''')
    s.sign(30, 30, "RegrowWall", "EAST", text=None)
    s.script("RegrowWall", '''    lockall
    if (!flag(FLAG_ICHOR_GOT_DEMETERS_SICKLE)) {
        msgbox(format("A wall of reeds, green with new shoots. Behind it, water glints in rings."), MSGBOX_DEFAULT)
        releaseall
        end
    }
    msgbox(format("A wall of reeds. You cut a path with Demeter's Sickle.\\p"
                  "…By the time you look up, it's grown back.\\p"
                  "Through the stems: eight pools in a ring, around a ninth."), MSGBOX_DEFAULT)
    releaseall''')
    s.sign(39, 4, "FogBank", "NORTH", text="A bank of mist sits on the north-east reeds and never lifts, even at noon.\\p"
           "Something big shifts inside it. One feather drifts out, bronze, as long as your arm.")
    s.sign(33, 14, "DeepReeds", text="The deep reeds. The water here is black and still, and the stems close over your head.\\p"
           "In the mud at the edge, small prints. Three toes. Then nine.")
    return s


VIEWS_LAKE = [("1 the south shore", 20, 32), ("2 Akanthis's hut", 22, 27), ("3 Borboros's boardwalk", 21, 21),
              ("4 islet two", 21, 15), ("5 the roost", 21, 5), ("6 the deep reeds", 36, 15),
              ("7 islet three", 8, 13), ("8 the nests", 7, 5), ("9 the west shore", 3, 12),
              ("10 the reed wall", 32, 30), ("11 the far rock", 29, 7)]


def build_lake():
    g = plan_lake()
    paint(g, props_lake)
    blocks = g.blocks()
    border = [smid("trees", "holm_BL") | (1 << 10)] * 4
    KP.write_layout(LAKE, blocks, border, "gTileset_Aethos", STYM)
    spec = spec_lake()
    header = f"""mapscripts {LAKE}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        if (flag(FLAG_ICHOR_STYMPHALIA_FLOCK_ROSE)) {{
            setvar(VAR_TEMP_1, 1)
        }}
    }}
}}"""
    write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE", header=header)
    m = Walk(LAKE, blocks, STYM, spec, g)
    south = [(x, LAKE_H - 1) for x in range(20, 23)]
    west = [(0, y) for y in LAKE_WEST_ROWS]
    return m, [("the south shore to the west shore", south, west)], VIEWS_LAKE, "lake", set(FLOCK)


# ---------------------------------------------------------------------------
# Route 27, the Arkadian hills (44x36). The lake is east (our rows 27-29 = its
# 11-13); Arkadia is north (our x 6-7 = its south road, x 13-14). The six rows at
# Arkadia's seam keep to aethos.
# ---------------------------------------------------------------------------
R27_W, R27_H = 44, 36
R27_HERM = (16, 11)                  # land (16, 12)
R27_SPRING = (11, 11)                # spring 2x2
R27_LOW_MOUTH, R27_HIGH_MOUTH = (29, 25), (31, 18)     # door cells (the arch is above each)
R27_DRUMS, R27_PLATES = [(29, 14), (37, 13)], [(31, 12), (35, 12)]
R27_SEAL_BRIDGE = 33                 # the plank that drops over the lookout's chasm (rows 9-11)
R27_SIGN_E, R27_SIGN_FORK, R27_SIGN_N = (41, 26), (18, 10), (9, 3)
R27_CASCADE_LINK = ((2, 15), (2, 8))
R27_THREAD_LINK = ((9, 24), (9, 22))
R27_WINGS_LINK = ((38, 13), (41, 13))
R27_CACHE_DOOR = (35, 31)


def plan_r27():
    W, H = R27_W, R27_H
    g = Grid(R27, W, H, strip={(x, y) for x in range(W) for y in range(6)})
    g.rect("#", 0, 0, W - 1, H - 1)
    # --- Arkadia's seam (rows 0-5): the pines at the top of the pass, band three ------------
    g.rect("p", 6, 0, 7, 5)
    g.rect(",", 4, 2, 9, 4)
    g.put(".", (8, 1), (5, 5), (8, 5))
    g.put("k", R27_SIGN_N)
    # --- the top of the pass (rows 6-9): two rock walls, Sthenelaidas in the gap ------------
    g.rect("^", 0, 6, 5, 9)
    g.rect("^", 9, 6, 14, 9)
    g.rect(".", 6, 6, 8, 9)
    g.rect("p", 6, 6, 7, 9)
    g.put(".", (5, 8))                              # his niche
    # --- the Karyai spring under walnuts (rows 10-15) -----------------------------------
    g.rect(".", 3, 10, 26, 15)
    g.rect("p", 6, 10, 7, 13)
    g.rect("p", 6, 13, 21, 13)
    g.rect("p", 20, 13, 22, 15)
    g.rect("#", 23, 10, 26, 10)
    g.put("k", (R27_SPRING[0], R27_SPRING[1]), (R27_SPRING[0] + 1, R27_SPRING[1]),
          (R27_SPRING[0], R27_SPRING[1] + 1), (R27_SPRING[0] + 1, R27_SPRING[1] + 1))
    g.put("k", R27_HERM, R27_SIGN_FORK)
    g.rect("k", 3, 10, 5, 12) if False else None
    # the cascade (the Horn): a rock step west of the meadow, its pool, the basin above
    g.rect("^", 0, 10, 4, 14)
    g.rect("F", 2, 10, 2, 12)
    g.rect("=", 1, 13, 3, 14)
    g.rect(".", 1, 8, 3, 9)                         # the basin's ledge above the fall
    g.rect("=", 1, 8, 1, 8)
    g.put(".", (1, 15), (2, 15), (3, 15), (4, 15))
    # --- band two (rows 16-19), then the ravine and Othryades's bridge (rows 21-23) -----------
    g.rect(",", 19, 16, 23, 19)
    g.rect(".", 19, 20, 23, 20)
    g.rect("X", 3, 21, 25, 23)
    g.rect("B", 21, 21, 21, 23)
    g.put("k", (8, 24))                             # the anchor ring, on the ravine's south lip
    g.put("q", (9, 22), (10, 22))                   # a ledge in the chasm (the Thread)
    # --- the east valley (rows 24-30): the hollow, band one, the scout at the narrows ---------
    g.rect(".", 3, 24, W - 1, 30)
    g.rect("p", 20, 24, 22, 29)
    g.rect("p", 20, 27, W - 1, 29)
    g.rect(",", 30, 26, 32, 30)                     # band one, wall to wall
    g.rect("^", 23, 24, 26, 26)                     # the narrows' north crag
    g.rect("#", 23, 30, 27, 30)
    g.put(".", (25, 26))                            # the scout's niche
    g.rect(";", 5, 25, 14, 28)                      # the west meadow, long grass
    g.rect(".", 3, 24, 19, 24)
    g.rect("p", 9, 24, 9, 24)
    g.put("k", R27_SIGN_E)
    # --- the rock above the valley: the cut stair to the high ledge; the cave's mouths -------
    g.rect("^", 26, 16, W - 1, 23)
    g.rect("^", 28, 24, W - 1, 25)
    g.rect("S", 40, 19, 40, 25)
    g.rect(".", 37, 17, 42, 18)                     # the high ledge (stairs to treasure)
    g.put("k", R27_LOW_MOUTH, (R27_LOW_MOUTH[0], R27_LOW_MOUTH[1] - 1))
    g.rect(".", 27, 19, 33, 21)                     # the scouts' terrace, out of the cave's high mouth
    g.put("k", R27_HIGH_MOUTH, (R27_HIGH_MOUTH[0], R27_HIGH_MOUTH[1] - 1))
    g.rect("v", 27, 22, 28, 22)                     # ...and its wall back down to the valley
    g.rect(".", 27, 23, 28, 25)
    # --- the lookout spur (rows 6-15): the drums' yard, the chasm, the watchtower ------------
    g.rect(".", 27, 12, 38, 15)
    g.rect("#", 26, 11, 26, 15)
    g.rect("p", 26, 13, 28, 13)
    g.rect("X", 27, 9, 41, 11)
    g.rect(".", 28, 6, 42, 8)
    g.put("k", (41, 6), (42, 6), (41, 7), (42, 7), (41, 8), (42, 8))   # the tower
    g.rect("#", 39, 11, 40, 16)
    g.rect(".", 41, 12, 42, 13)                     # the eyrie across the gap of wind (the Wings)
    g.rect("^", 41, 14, 42, 15)
    for x, y in R27_PLATES:
        g.put("P", (x, y))
    # --- the ridge over the Titans' lower road (rows 31-35); the cache (the Helm) -----------
    g.rect("^", 3, 31, W - 1, 33)
    g.rect("^", 3, 31, W - 1, 32)
    g.rect("t", 3, 33, W - 1, 34)
    for x in range(3, W):                           # the road below winds between scrub
        g.put("#", (x, 33) if (x // 5) % 2 == 0 else (x, 34))
    g.exempt |= {(x, y) for x in range(3, W) for y in (33, 34) if g.at(x, y) == "t"}
    for x in range(4, 33):                          # the valley's south edge: spurs of rock
        if noise(x, 30, 133) < 30 and g.at(x, 30) == "." and g.at(x - 1, 30) != "^":
            g.put("^", (x, 30))
    # optional grass with reasons: the spring's verges, the yard's corners, the ledges
    g.rect(",", 3, 14, 6, 15)
    g.rect(",", 23, 11, 25, 12)
    g.rect(",", 8, 10, 10, 11)
    g.rect(",", 35, 14, 38, 15)
    g.rect(",", 28, 6, 31, 7)
    g.rect(",", 37, 17, 39, 18)
    g.rect(",", 34, 26, 36, 26)
    g.rect(",", 38, 30, 42, 30)
    g.rect(",", 15, 25, 19, 26)
    g.rect(",", 3, 26, 4, 28)
    g.rect(",", 41, 26, 42, 26)
    g.put("#", (R27_W - 1, 26), (R27_W - 1, 30))     # the valley meets the lake only on its road
    g.rect(",", 16, 10, 17, 10)
    g.rect(",", 12, 14, 13, 15)
    g.rect(".", 33, 31, 38, 32)                     # the Titans' cache, cut into the ridge
    g.put("^", (33, 31), (38, 31))
    g.rect(".", 3, 24, 4, 30)
    return g


def props_r27(g):
    for xy in (R27_SIGN_E, R27_SIGN_FORK, R27_SIGN_N):
        g.set(*xy, SIGN, True)
    g.set(*R27_HERM, HERM, True)
    g.spiece("spring", *R27_SPRING)
    for mouth in (R27_LOW_MOUTH, R27_HIGH_MOUTH):
        g.set(mouth[0], mouth[1] - 1, R5.CAVE_TOP, True)
        g.set(*mouth, R5.CAVE_DOOR, False)
    g.spiece("tower", 41, 6)
    g.set(42, 8, smid("tower", "door"), True)     # its low door stays shut
    g.spiece("odds", 8, 24, [("post", 0, 0)])        # the anchor ring's post
    g.spiece("odds", 27, 12, [("stele", 0, 0)])      # the seal's lever post
    # the watchtower's hilltop: scree, boulders, a fallen drum nobody moved
    for x, y in ((33, 7), (34, 8), (39, 6), (29, 8)):
        g.spiece("taygetos", x, y, [("scree", 0, 0)], False)
    g.spiece("taygetos", 38, 8, [("boulders", 0, 0)])
    g.spiece("taygetos", 32, 6, [("boulder", 0, 0)])
    g.spiece("odds", 35, 8, [("drum_L", 0, 0), ("drum_R", 1, 0)])
    # walnuts round the spring
    for x, y in ((8, 10) if False else (13, 10), (22, 11)):
        pass
    g.spiece("trees", 4, 10, [("walnut_00", 0, 0)]) if False else None


def spec_r27():
    s = Spec(R27)
    s.connections = [{"direction": "up", "map": "MAP_ARKADIA", "offset": -ARKADIA_OFFSET},
                     {"direction": "right", "map": MAP[LAKE], "offset": -R27_OFFSET}]
    s.warps = [KP.warp(*R27_LOW_MOUTH, CAVE, 0), KP.warp(*R27_HIGH_MOUTH, CAVE, 1)]
    L = "Lakonian"
    # --- trainers ----------------------------------------------------------------------------
    s.trainer("TITYOS", "SHEPHERD", 37, 26, "DOWN", 1,
              "My goats climb better than you. They battle better too. Watch.",
              "The goats are disappointed in me.",
              "There's a watchtower past the spring, over a chasm. / Old scouts' drums lie about the yard. Only a strong back moves those.",
              mandatory=False)
    team("TITYOS", "TITYOS", "Shepherd", "Shepherd", "Male", [("Kerazap", 52), ("Chelyra", 52)], music="Hiker")
    s.trainer("R27_KORE", "GOATHERD", 34, 30, "LEFT", 1,
              "One of my kids went into the cave. Nobody goes into the cave.",
              "Fine. You go into the cave.",
              "The scouts' cave climbs to a terrace over the road. It's dark as a pocket in there.", mandatory=False)
    team("R27_KORE", "KORE", "Goatherd", "Goatherd", "Female", [("Kerazap", 52), ("Harpelle", 52)])
    s.trainer("R27_LOCHAGOS", "HOPLITE", 25, 26, "DOWN", 3,
              "The narrows are mine. The Skiritai held them for Lakonia since before your grandmother.",
              "Held, and lost. Pass.",
              "Othryades keeps the ravine bridge. He hasn't stepped off it in a week.")
    team("R27_LOCHAGOS", "LOCHAGOS", L, "Hoplite", "Male", [("Hoplektor", 52), ("Geogrip", 52)])
    s.trainer("OTHRYADES", "HOPLITE", 22, 20, "LEFT", 1,
              "One bridge. One scout. That's me, and that's the bridge.",
              "Still standing. Mostly. Fine. Cross.",
              "A strap from Gylippos? Give it here. My staff's his twin.")
    team("OTHRYADES", "OTHRYADES", L, "Hoplite", "Male", [("Lykanax", 52), ("Nemeleon", 53), ("Hyphantis", 53)])
    s.trainer("R27_AGRIA", "ACOLYTE_F", 4, 26, "RIGHT", 2,
              "Artemis's border. The Karyai maidens danced here. I fight here. Same thing, she says.",
              "She'll forgive me. She forgives hunters.",
              "Arkadia's over the pass. Walk soft in the cypresses; the Huntress listens.", mandatory=False)
    team("R27_AGRIA", "AGRIA", "Acolyte", "Acolyte F", "Female", [("Hyphantis", 52), ("Kaprodon", 53)])
    s.trainer("R27_KARYATIS", "YOUTH_F", 14, 14, "DOWN", 1,
              "I came for the spring. Everybody comes for the spring. Battle while you drink?",
              "Spilled it.",
              "The builders carved the Karyai girls as pillars. Holding up a roof forever. / I'd rather dance.",
              mandatory=False)
    team("R27_KARYATIS", "KARYATIS", "Pilgrim", "Picnicker", "Female", [("Chelyra", 52), ("Sophowl", 52)])
    s.trainer("R27_PHOROS", "TITAN_GRUNT", 15, 24, "RIGHT", 2,
              "I'm not a deserter. I'm resting. In the opposite direction.",
              "Resting harder now.",
              "There's a crack in the ravine with a ring at its lip. Somebody tied off down there once.", mandatory=False)
    team("R27_PHOROS", "PHOROS", "Titanborn", "Titan Grunt", "Male", [("Gigantomb", 52), ("Taurivet", 52)], music="Aqua")
    s.trainer("R27_SKOPOS", "CADET", 31, 14, "UP", 2,
              "This is the watchtower's yard. You want the tower, you move the drums. That's the test.",
              "You passed the other test. The battle one.",
              "Two sills, two drums. The old scouts dropped the plank when both sat true.", mandatory=False)
    team("R27_SKOPOS", "SKOPOS", L, "Camper", "Male", [("Dorydrake", 52), ("Enigmaw", 53)])
    s.trainer("R27_ANABATES", "CADET_F", 38, 18, "LEFT", 1,
              "You took the stair! Nobody takes the stair. It's all knees.",
              "All knees, and now no battle.",
              "From up here you can count the helmets on the lower road. I stopped at a thousand.", mandatory=False)
    team("R27_ANABATES", "ANABATES", L, "Picnicker", "Female", [("Harpelle", 52), ("Hoplomex", 53)])
    s.trainer("STHENELAIDAS", "HOPLITE", 5, 8, "RIGHT", 3,
              "Last scout on the road. I'll keep it short. Battle.",
              "Short. Like I said.",
              "Arkadia's over the rise. Cypresses. Wolves at night. Mind both.")
    team("STHENELAIDAS", "STHENELAS", L, "Hoplite", "Male", [("Enigmaw", 53), ("Kaprodon", 53), ("Lykanax", 53)])
    s.trainer("R27_KYNEGOS", "SHEPHERD", 4, 3, "RIGHT", 1,
              "Wolf tracks in the pines. I'm following them. You're in the way.",
              "The wolves can wait.",
              "Lykanax hunt these pines after dark. Arkadia's wolves, come down for the border.", mandatory=False)
    team("R27_KYNEGOS", "KYNEGOS", "Shepherd", "Shepherd", "Male", [("Lykanax", 52), ("Nemeleon", 53)], music="Hiker")
    # --- goats, the cache's watchman, the columns ------------------------------------------------
    for i, (x, y) in enumerate(((38, 29), (35, 27), (41, 27))):
        s.person(f"Goat{i + 1}", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", x, y, "LEFT", move="MOVEMENT_TYPE_WANDER_AROUND")
        s.scripts.append(f'''script {s.px}Goat{i + 1} {{
    lock
    playmoncry(SPECIES_KERAZAP, CRY_MODE_NORMAL)
    msgbox(format("One of Tityos's Kerazap. It chews something that might be your map."))
    waitmoncry
    release
}}''')
    s.person("Watchman", "TITAN_GRUNT", 38, 32, "LEFT", FLAG_AFTER)
    s.script("Watchman", '''    lock
    if (flag(FLAG_ICHOR_HELM_ON)) {
        msgbox(format("The watchman stares straight through you, at the road.\\p“…Birds,” he mutters. “Only the birds.”"))
    } else {
        faceplayer
        msgbox(format("The column's stores. Nobody touches them that I can see. Back to your road."))
    }
    release''')
    for i, x in enumerate((8, 16, 24, 32, 40)):
        s.person(f"Column{i + 1}", "TITAN_GRUNT", x, 34 if (x // 5) % 2 == 0 else 33, "LEFT", FLAG_AFTER,
                 move="MOVEMENT_TYPE_WALK_IN_PLACE_LEFT")
        s.scripts.append(f"script {s.px}Column{i + 1} {{\n    end\n}}")
    # the cache's door: seen, you're sent back; under the Helm, his eyes slide past
    s.trigger(*R27_CACHE_DOOR, "CacheWatch", "VAR_TEMP_1", "0")
    s.script("CacheWatch", '''    if (flag(FLAG_ICHOR_HELM_ON) || flag(FLAG_ICHOR_ACT3_COMPLETE)) {
        end
    }
    lockall
    playse(SE_PIN)
    msgbox(format("WATCHMAN: Halt. The column's stores.\\pNobody comes in here that I can see. Back to the road."), MSGBOX_DEFAULT)
    closemessage
    applymovement(OBJ_EVENT_ID_PLAYER, Common_Movement_WalkUp)
    waitmovement(0)
    releaseall''')
    # --- the drum seal: two drums onto two sills drop the plank to the watchtower ----------------
    seal = flag("FLAG_ICHOR_R27_LOOKOUT_PLANK", "the lookout's drums sat on both sills; the plank is down")
    for i, (x, y) in enumerate(R27_DRUMS):
        s.gate(f"Drum{i + 1}", "drum", x, y)
    for (px, py) in R27_PLATES:
        for dx, dy in FACE.values():
            c = (px + dx, py + dy)
            if c not in R27_PLATES and 27 <= c[0] <= 38 and 12 <= c[1] <= 15:
                s.trigger(*c, "Sills", "VAR_TEMP_2", "0")
    bx = R27_SEAL_BRIDGE
    S = LT.TILESETS["stymphalia"]["structures"]["ravine"]

    def rid(n):
        cx, cy = S["names"][n]
        return S["ids"][cy][cx]
    planks = "\n".join(f"    setmetatile({bx}, {9 + j}, 0x{rid(n):03X}, FALSE)"
                       for j, n in enumerate(("bridge_N", "bridge", "bridge_S")))
    (p1x, p1y), (p2x, p2y) = R27_PLATES
    d1, d2 = s.lid + "DRUM1", s.lid + "DRUM2"
    s.script("Plank", planks + "\n    return")
    s.script("DrawSeal", f'''    if (flag({seal})) {{
        call({s.px}Plank)
        setobjectxyperm({d1}, {p1x}, {p1y})
        setobjectxyperm({d2}, {p2x}, {p2y})
    }}''')
    s.script("Sills", f'''    if (flag({seal})) {{
        end
    }}
    getobjectxy({d1}, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)
    getobjectxy({d2}, CURRENT_POSITION, VAR_0x8009, VAR_0x800A)
    if (var(VAR_0x8007) == {p1x} && var(VAR_0x8008) == {p1y} && var(VAR_0x8009) == {p2x} && var(VAR_0x800A) == {p2y}) {{
        lockall
        setflag({seal})
        playse(SE_DOOR)
        delay(20)
        call({s.px}Plank)
        special(DrawWholeMapView)
        playse(SE_M_STRENGTH)
        msgbox(format("Both drums sit true on their sills. Somewhere a rope runs out,\\p"
                      "and an old plank swings down across the chasm to the watchtower."), MSGBOX_DEFAULT)
        releaseall
    }} elif (var(VAR_0x8007) == {p1x} && var(VAR_0x8008) == {p1y}) {{
        msgbox(format("The drum settles on the grooved sill. One sill to go."), MSGBOX_AUTOCLOSE)
    }} elif (var(VAR_0x8009) == {p2x} && var(VAR_0x800A) == {p2y}) {{
        msgbox(format("The drum settles on the grooved sill. One sill to go."), MSGBOX_AUTOCLOSE)
    }}''')
    s.sign(27, 12, "Lever", text=None)
    s.script("Lever", f'''    lockall
    if (flag({seal})) {{
        msgbox(format("A scouts' post with a rope knotted round it. The plank's down."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A scouts' post, the Girdle's knot carved in it: the old drill's reset.\\pRoll the drums back where they lay?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_CLICK)
        warpsilent({MAP[R27]}, 28, 13)
        waitstate
    }}
    releaseall''')
    # --- the cascade (the Horn), the crack (the Thread), the updraft (the Wings) --------------------
    (cx0, cy0), (cx1, cy1) = R27_CASCADE_LINK
    s.sign(2, 14, "Cascade", "NORTH", text=None)
    s.script("Cascade", f'''    lockall
    if (!flag(FLAG_ICHOR_GOT_HORN_OF_ACHELOUS)) {{
        msgbox(format("The Karyai spring's overflow falls down the rock in a white rope.\\p"
                      "Something glints in the basin at the top. A river god's horn could climb water like this."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("The spring's overflow falls in a white rope.\\pSound the Horn of Achelous and climb it?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_WATERFALL)
        fadescreen(FADE_TO_WHITE)
        warpsilent({MAP[R27]}, {cx1}, {cy1})
        waitstate
    }}
    releaseall''')
    s.sign(2, 10, "CascadeDown", "SOUTH", text=None)
    s.script("CascadeDown", f'''    lockall
    msgbox(format("The fall drops away to the pool below. Ride it down?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_WATERFALL)
        fadescreen(FADE_TO_WHITE)
        warpsilent({MAP[R27]}, {cx0}, {cy0})
        waitstate
    }}
    releaseall''')
    (tx0, ty0), (tx1, ty1) = R27_THREAD_LINK
    s.sign(8, 24, "Anchor", text=None)
    s.script("Anchor", f'''    lockall
    if (!flag(FLAG_ICHOR_GOT_ARIADNES_THREAD)) {{
        msgbox(format("A bronze ring is sunk in the rock at the ravine's lip.\\p"
                      "Far down, on a ledge, something glints. A line tied off here would reach it."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A bronze ring at the ravine's lip, and a ledge far below.\\pTie off Ariadne's Thread and climb down?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_BIND)
        fadescreen(FADE_TO_BLACK)
        warpsilent({MAP[R27]}, {tx1}, {ty1})
        waitstate
    }}
    releaseall''')
    s.sign(8, 22, "ThreadUp", text=None)
    s.script("ThreadUp", f'''    lockall
    msgbox(format("Ariadne's Thread hangs down the rock from the ring above. Climb back up?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_BIND)
        fadescreen(FADE_TO_BLACK)
        warpsilent({MAP[R27]}, {tx0}, {ty0})
        waitstate
    }}
    releaseall''')
    (wx0, wy0), (wx1, wy1) = R27_WINGS_LINK
    s.sign(39, 13, "Updraft", "EAST", text=None)
    s.script("Updraft", f'''    lockall
    if (!flag(FLAG_ICHOR_GOT_DAEDALUS_WINGS)) {{
        msgbox(format("Wind roars up out of a cleft here, strong enough to lean on.\\p"
                      "Across it, on a pinnacle, a nest of sticks and bronze. Only wings would get you there."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("Wind roars straight up out of the cleft.\\pSpread Daedalus's Wings and ride it across to the pinnacle?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_FLY)
        fadescreen(FADE_TO_WHITE)
        warpsilent({MAP[R27]}, {wx1}, {wy1})
        waitstate
    }}
    releaseall''')
    s.sign(40, 13, "UpdraftBack", "WEST", text=None)
    s.script("UpdraftBack", f'''    lockall
    msgbox(format("The updraft howls up the cleft. Ride it back across?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_FLY)
        fadescreen(FADE_TO_WHITE)
        warpsilent({MAP[R27]}, {wx0}, {wy0})
        waitstate
    }}
    releaseall''')
    # --- the spring --------------------------------------------------------------------------------
    sx, sy = R27_SPRING
    s.sign(sx, sy + 1, "Spring", text=None)
    s.sign(sx + 1, sy + 1, "Spring")
    s.script("Spring", '''    lockall
    msgbox(format("A cold spring under walnut trees.\\pGirls from Karyai danced here once, for Artemis.\\p"
                  "Builders liked the dance so much they carved the girls as pillars.\\pYou drink. You feel better."), MSGBOX_DEFAULT)
    closemessage
    special(HealPlayerParty)
    playfanfare(MUS_HEAL)
    waitfanfare
    releaseall''')
    s.sign(*R27_HERM, "Herm", text=None)
    s.script("Herm", '''    lockall
    msgbox(format("EAST: STYMPHALIA. NORTH: ARKADIA.\\pA herm of Hermes on the old border, where Lakonia ends and Arkadia begins."))
    call(EventScript_IchorAnointHerm)
    releaseall''')
    # --- finds ---------------------------------------------------------------------------------
    s.item("ITEM_TM_STEEL_WING", 36, 7, item_flag("R27", "TM_STEEL_WING", "the watchtower's parapet (the Girdle)"))
    s.item("ITEM_RARE_CANDY", 42, 12, item_flag("R27", "EYRIE", "the pinnacle's nest (the Wings)"))
    s.item("ITEM_MYSTIC_WATER", 3, 8, item_flag("R27", "BASIN", "the basin above the cascade (the Horn)"))
    s.item("ITEM_NUGGET", 10, 22, item_flag("R27", "CRACK", "the ledge in the ravine (the Thread)"))
    s.item("ITEM_TM_AERIAL_ACE", 41, 17, item_flag("R27", "HIGH_LEDGE", "the high ledge up the cut stair"))
    s.item("ITEM_FULL_RESTORE", 33, 32, item_flag("R27", "CACHE", "the Titans' cache (the Helm)"))
    s.item("ITEM_ULTRA_BALL", 32, 20, item_flag("R27", "TERRACE", "the scouts' terrace"))
    s.item("ITEM_HYPER_POTION", 3, 29, item_flag("R27", "MEADOW", "the west meadow's corner"))
    s.hide("ITEM_BIG_NUGGET", 40, 8, hidden_flag("R27", "TOWER_FOOT", "the watchtower's foot"))
    s.hide("ITEM_REVIVE", 13, 10, hidden_flag("R27", "WALNUT", "under the walnut nearest the spring"))
    s.hide("ITEM_RARE_BONE", 38, 31, hidden_flag("R27", "CACHE", "the cache's back wall"))
    s.hide("ITEM_ELIXIR", 27, 21, hidden_flag("R27", "TERRACE", "the terrace's corner"))
    s.hide("ITEM_STARDUST", 5, 4, hidden_flag("R27", "PINES", "the pines at the top of the pass"))
    # --- signs ---------------------------------------------------------------------------------
    s.sign(*R27_SIGN_E, "EastSign", text="ROUTE 27\\nOver the hills into Arkadia. Scouts on the heights.")
    s.sign(*R27_SIGN_FORK, "ForkSign", text="EAST: STYMPHALIA. NORTH: ARKADIA.\\nEAST, UP THE SPUR: the lookout.")
    s.sign(*R27_SIGN_N, "NorthSign", text="ROUTE 27\\nSouth: the Karyai spring, Lake Stymphalia and Lakonia.")
    s.sign(41, 8, "Tower", text="From up here you can see the lake, the road, and all of Lakonia. No walls.\\p"
           "A scout's carved a line on the parapet: WE SEE THEM FIRST.")
    s.sign(20, 31, "AresGully", "SOUTH", text="A gully runs down through the ridge toward the lower road.\\p"
           "Spear-butts have worn the rock smooth. Somebody waits down there, some nights, to ambush the columns.")
    return s


VIEWS27 = [("1 from the lake", 40, 28), ("2 the hollow", 31, 28), ("3 the narrows", 25, 28),
           ("4 the ravine bridge", 21, 22), ("5 band two", 21, 18), ("6 the Karyai spring", 13, 12),
           ("7 the cascade", 3, 12), ("8 the drums' yard", 32, 13), ("9 the watchtower", 37, 8),
           ("10 the high ledge", 39, 18), ("11 the scouts' terrace", 30, 21), ("12 the Titans' cache", 35, 32),
           ("13 the top of the pass", 7, 7), ("14 Arkadia's pines", 7, 2)]


def build_r27():
    g = plan_r27()
    paint(g, props_r27)
    blocks = g.blocks()
    border = [R5.CYPRESS_TOP | (1 << 10)] * 4
    KP.write_layout(R27, blocks, border, "gTileset_Aethos", STYM)
    spec = spec_r27()
    header = f"""mapscripts {R27}_MapScripts {{
    MAP_SCRIPT_ON_LOAD {{
        call({spec.px}DrawSeal)
    }}
}}"""
    write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE", header=header)
    g.links += [R27_CASCADE_LINK, R27_THREAD_LINK, R27_WINGS_LINK, ((R27_SEAL_BRIDGE, 12), (R27_SEAL_BRIDGE, 8)),
                ((R27_LOW_MOUTH[0], R27_LOW_MOUTH[1] + 1), (R27_HIGH_MOUTH[0], R27_HIGH_MOUTH[1] + 1))]
    m = Walk(R27, blocks, STYM, spec, g)
    east = [(R27_W - 1, y) for y in R27_EAST_ROWS]
    north = [(x, 0) for x in (6, 7)]
    return m, [("the lake to Arkadia", east, north)], VIEWS27, "route27", set()


# ---------------------------------------------------------------------------
# The Skiritai cave (30x20, cave_dark, dark: the Torch). Its low mouth opens on
# Route 27's valley, its high mouth on the scouts' terrace above it.
# ---------------------------------------------------------------------------
CAVE_W, CAVE_H = 30, 20
CAVE_LOW, CAVE_HIGH = (4, 18), (25, 18)         # daylight_s pieces; the warps are one row below
CAVE_BRAZIER = (14, 6)
CAVE_BRAZIER_FLAG = "FLAG_ICHOR_BRAZIERS_START + 0x60"


def plan_cave():
    W, H = CAVE_W, CAVE_H
    g = [["#"] * W for _ in range(H)]

    def rect(ch, x0, y0, x1, y1):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch
    rect(".", 3, 13, 6, 18)                          # up from the low mouth
    rect(".", 4, 8, 7, 13)                           # the scouts' climb, west
    rect(".", 7, 4, 21, 9)                           # the brazier hall
    rect("#", 10, 7, 11, 9)
    rect("#", 17, 4, 18, 5)
    rect(".", 21, 6, 26, 9)                          # the passage east
    rect(".", 23, 10, 26, 18)                        # ...and down to the high mouth (the climb's top)
    rect("#", 23, 13, 23, 15)
    rect(".", 12, 10, 16, 14)                        # the side gallery, behind rubble (the Hammer)
    g[10][14] = "."
    rect(".", 17, 12, 20, 15)
    rect("~", 18, 13, 20, 15)                        # a seep's pool
    rect(".", 1, 3, 4, 6)                            # the scouts' store, behind chains (the Labrys)
    g[5][5] = "."
    g[5][6] = "."
    rect(".", 8, 14, 11, 17)                         # a crawl south of the gallery
    g[12][27] = "."                                  # Arktos's niche
    return g


def build_cave():
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
    for x, y in (CAVE_LOW, CAVE_HIGH):
        put(x, y, pieces["daylight_s"], solid=False)
    put(*CAVE_BRAZIER, pieces["brazier_cold"])
    put(19, 12, pieces["seep"])
    put(6, 9, pieces["chalk_arrow_n"])
    put(24, 11, pieces["chalk_arrow_s"])
    put(15, 14, pieces["bones"])
    put(8, 6, pieces["stalagmites"])
    put(20, 4, pieces["column"])
    put(26, 13, pieces["stalagmite"])
    put(1, 3, pieces["niche_empty"])
    put(3, 3, pieces["stele"])
    put(9, 17, pieces["rock_pile"])
    put(12, 4, pieces["pebbles"], solid=False)
    put(25, 16, pieces["pebbles"], solid=False)
    KP.write_layout(CAVE, blocks, [kit.kit_id(cat, "T|...", "wet") | 0x3400] * 4, "gTileset_Aethos", "gTileset_CaveDark")
    s = Spec(CAVE)
    s.warps = [KP.warp(CAVE_LOW[0], CAVE_LOW[1] + 1, R27, 0), KP.warp(CAVE_HIGH[0], CAVE_HIGH[1] + 1, R27, 1)]
    s.trainer("SKIRITAI_KRYPTE", "CADET_F", 7, 11, "LEFT", 3,
              "Krypteia. We train in the dark. You're the night's exercise.",
              "Exercised.",
              "The old scouts kept a store up the west climb. Bronze chains on it, stamped with an axe.")
    team("SKIRITAI_KRYPTE", "KRYPTE", "Lakonian", "Picnicker", "Female", [("Kalyptor", 52), ("Hyphantis", 53)])
    s.trainer("SKIRITAI_ARKTOS", "HOPLITE", 27, 12, "LEFT", 4,
              "Nobody passes the climb's top without a word from Lakonia.",
              "That'll do for a word.",
              "Out the high mouth there's a terrace over the valley. Drop off its wall and you're home.")
    team("SKIRITAI_ARKTOS", "ARKTOS", "Lakonian", "Hoplite", "Male", [("Plouteras", 52), ("Dorydrake", 53)])
    s.gate("Rubble", "rubble", 14, 10, flag("FLAG_ICHOR_HIDE_SKIRITAI_RUBBLE", "the cave's gallery rubble broken"))
    s.person("Chains", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 6, 5, "DOWN",
             flag("FLAG_ICHOR_HIDE_SKIRITAI_CHAINS", "the scouts' store's chains cleaved (the Labrys)"))
    s.scripts.append(f"script {s.px}Chains {{\n    goto(EventScript_IchorLabrysSeal)\n}}")
    s.item("ITEM_TM_REST", 1, 5, item_flag("SKIRITAI", "STORE", "the scouts' store (the Labrys)"))
    s.item("ITEM_HARD_STONE", 13, 13, item_flag("SKIRITAI", "GALLERY", "the gallery (the Hammer)"))
    s.item("ITEM_MAX_ETHER", 10, 16, item_flag("SKIRITAI", "CRAWL", "the crawl"))
    s.item("ITEM_SUPER_POTION", 26, 7, item_flag("SKIRITAI", "PASSAGE", "the east passage"))
    s.hide("ITEM_DUSK_STONE", 2, 4, hidden_flag("SKIRITAI", "STORE", "the store's back corner"))
    s.hide("ITEM_STAR_PIECE", 16, 14, hidden_flag("SKIRITAI", "BONES", "beside the bones"))
    s.hide("ITEM_ETHER", 3, 13, hidden_flag("SKIRITAI", "MOUTH", "inside the low mouth"))
    s.sign(3, 3, "Stele", text="THE SKIRITAI. FIRST INTO BATTLE, LAST OUT.\\nThe scouts' names follow, too many to read.")
    s.sign(6, 9, "Arrow", text="A chalk arrow, pointing up the climb. Under it, in a boy's hand: NOT FAR NOW.")
    s.sign(CAVE_BRAZIER[0], CAVE_BRAZIER[1] + 1, "Brazier", "NORTH")
    s.sign(CAVE_BRAZIER[0] + 1, CAVE_BRAZIER[1] + 1, "Brazier", "NORTH")
    bx, by = CAVE_BRAZIER
    lit = pieces["brazier_lit"]
    swap = "\n".join(f"    setmetatile({bx + i}, {by + j}, 0x{lit[j][i]:03X}, TRUE)"
                     for j in range(2) for i in range(2))
    header = f'''const SK_BRAZIER = {CAVE_BRAZIER_FLAG}
mapscripts {CAVE}_MapScripts {{
    MAP_SCRIPT_ON_LOAD {{
        if (flag(SK_BRAZIER)) {{
            call({s.px}Lit)
        }}
    }}
    MAP_SCRIPT_ON_TRANSITION {{
        if (flag(SK_BRAZIER)) {{
            setflashlevel(0)
        }}
    }}
}}'''
    s.scripts += [
        f'''script {s.px}Brazier {{
    setvar(VAR_0x8004, SK_BRAZIER)
    setvar(VAR_0x8005, TRUE)
    call(EventScript_IchorBrazier)
    if (flag(SK_BRAZIER)) {{
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
    m = Walk(CAVE, blocks, "gTileset_CaveDark", s, Grid(CAVE, W, H))
    low, high = [CAVE_LOW], [CAVE_HIGH]
    return m, [("low mouth to high mouth", low, high)], [("1 the low mouth", 4, 15), ("2 the climb", 5, 10),
                                                       ("3 the brazier hall", 14, 7), ("4 the gallery", 15, 12),
                                                       ("5 the store", 3, 5), ("6 the high mouth", 25, 15)], "cave", set()


# ---------------------------------------------------------------------------
# The seams this file writes into its neighbours
# ---------------------------------------------------------------------------

def arkadia_seam():
    """Arkadia's south road ended against limestone, with the Karneia hoplite on
    it. Open its last three rows (aethos path, as Arkadia's bottom six rows already
    are aethos), connect Route 27 below, and let the hoplite go once the road
    north from Lakonia is open (FLAG_ICHOR_LAKONIA_PARTED): before that the road
    stays shut, so nobody walks into Lakonia ahead of the story."""
    lay = ROOT / "data/layouts/Arkadia/map.bin"
    b = np.fromfile(lay, "<u2").reshape(44, 50)
    for y in (41, 42, 43):
        b[y, 13] = R5.PATH["l"] | 0x3000
        b[y, 14] = R5.PATH["r"] | 0x3000
    b.astype("<u2").tofile(lay)
    p = ROOT / "data/maps/Arkadia/map.json"
    m = json.loads(p.read_text())
    conns = [c for c in (m.get("connections") or []) if c["map"] != MAP[R27]]
    conns.append({"direction": "down", "map": MAP[R27], "offset": ARKADIA_OFFSET})
    m["connections"] = conns
    for o in m["object_events"]:
        if o.get("script") == "Arkadia_EventScript_Hoplite":
            o["flag"] = FLAG_PARTED
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Trainers: ids from world-act3's 1404-1503 block (tools/ichor/claim_ranges.md)
# ---------------------------------------------------------------------------
TRAINER_FIRST = 1404
OPP_BEGIN = "// Ichor: the road north from Lakonia begin (tools/ichor/maps/stymphalia.py)\n"
OPP_END = "// Ichor: the road north from Lakonia end\n"
PARTY_BEGIN = "/* Ichor: the road north from Lakonia begin (tools/ichor/maps/stymphalia.py) */\n"
PARTY_END = "/* Ichor: the road north from Lakonia end */\n"


def write_trainers():
    path = ROOT / "include/constants/opponents.h"
    t = path.read_text()
    ids = {tid: TRAINER_FIRST + i for i, (tid, _) in enumerate(TEAMS)}
    last = max(ids.values())
    block = OPP_BEGIN + "// Route 26, Lake Stymphalia, Route 27 and the Skiritai cave: ids " \
        f"{TRAINER_FIRST}-{last} of world-act3's 1404-1503.\n"
    block += "".join(f"#define TRAINER_ICHOR_{tid:<28} {n}\n" for tid, n in ids.items()) + OPP_END
    if OPP_BEGIN in t:
        t = t[:t.index(OPP_BEGIN)] + block + t[t.index(OPP_END) + len(OPP_END):]
    else:
        t = t.replace("#define TRAINERS_END_ACT3", block + "#define TRAINERS_END_ACT3", 1)
    t = re.sub(r"#define TRAINERS_END_ACT3 \d+[^\n]*",
               f"#define TRAINERS_END_ACT3 {last + 1} // the road north from Lakonia's {last} is Act III's highest", t)
    path.write_text(t)
    p = ROOT / "src/data/trainers.party"
    t = p.read_text()
    body = PARTY_BEGIN + "".join(party + "\n" for _, party in TEAMS) + PARTY_END
    if PARTY_BEGIN in t:
        t = t[:t.index(PARTY_BEGIN)] + body + t[t.index(PARTY_END) + len(PARTY_END):]
    else:
        anchor = "/* Ichor: Lakonia end */\n"
        t = t.replace(anchor, anchor + "\n" + body, 1)
    p.write_text(t)


# ---------------------------------------------------------------------------
# Wild tables (SCRIPT.md Part 4's, at BALANCE.md's Lakonia band, 46-50; every
# land table split into the four times of day). Slots run 20 20 10 10 10 10 5 5
# 4 4 1 1. Evolved forms only past their evolution level; the lake's Chalkip,
# the dex's rare dawn-and-dusk bird, comes at 46 rather than its own low spot.
# ---------------------------------------------------------------------------
LAND = {
    R26: (47, 49, {
        "Morning": ["HOPLOMEX", "CAIRNOLITH", "KERAZAP", "DORYDRAKE", "GELASABLE", "CHELONET",
                    "HOPLOMEX", "CAIRNOLITH", "HOPLEKTOR", "KERAZAP", "NEMELEON", "HOPLEKTOR"],
        "Day": ["HOPLOMEX", "CAIRNOLITH", "KERAZAP", "HARPELLE", "GELASABLE", "CHELONET",
                "HOPLOMEX", "DORYDRAKE", "HOPLEKTOR", "KERAZAP", "HARPELLE", "HOPLEKTOR"],
        "Evening": ["GELASABLE", "HOPLOMEX", "DORYDRAKE", "KERAZAP", "CAIRNOLITH", "NEMELEON",
                    "CHELONET", "HOPLEKTOR", "NEMELEON", "DORYDRAKE", "NEMELEON", "HOPLEKTOR"],
        "Night": ["GELASABLE", "CAIRNOLITH", "DORYDRAKE", "KERAZAP", "HOPLOMEX", "GELASABLE",
                  "CHELONET", "CAIRNOLITH", "DORYDRAKE", "KALYPTOR", "NEMELEON", "KALYPTOR"],
    }),
    LAKE: (46, 50, {
        "Morning": ["GALENYON", "GELASABLE", "BELORNIS", "CHELONET", "KERAZAP", "BELORNIS",
                    "KARKITOX", "CHALKIP", "BELORNIS", "GELASABLE", "CHALKIP", "GALENYON"],
        "Day": ["GALENYON", "GELASABLE", "BELORNIS", "CHELONET", "KERAZAP", "BELORNIS",
                "KARKITOX", "HARPELLE", "BELORNIS", "GELASABLE", "BELORNIS", "GALENYON"],
        "Evening": ["BELORNIS", "GALENYON", "KARKITOX", "CHELONET", "GELASABLE", "BELORNIS",
                    "CHALKIP", "KERAZAP", "CHALKIP", "KARKITOX", "CHALKIP", "BELORNIS"],
        "Night": ["KARKITOX", "GELASABLE", "KARKITOX", "CAIRNOLITH", "CHELONET", "GELASABLE",
                  "SOPHOWL", "KALYPTOR", "CAIRNOLITH", "SOPHOWL", "BELORNIS", "KALYPTOR"],
    }),
    R27: (48, 50, {
        "Morning": ["CAIRNOLITH", "KERAZAP", "CHELONET", "HYPHANTIS", "GELASABLE", "HYPHANTIS",
                    "NEMELEON", "HARPELLE", "CHELYRA", "ENIGMAW", "NEMELEON", "ENIGMAW"],
        "Day": ["KERAZAP", "CAIRNOLITH", "HARPELLE", "HYPHANTIS", "CHELONET", "GELASABLE",
                "CHELYRA", "HARPELLE", "ENIGMAW", "NEMELEON", "CHELYRA", "ENIGMAW"],
        "Evening": ["GELASABLE", "LYKANAX", "CAIRNOLITH", "HYPHANTIS", "KERAZAP", "NEMELEON",
                    "LYKANAX", "ENIGMAW", "CHELONET", "KAPRODON", "NEMELEON", "KAPRODON"],
        "Night": ["GELASABLE", "LYKANAX", "CAIRNOLITH", "HYPHANTIS", "KERAZAP", "KAPRODON",
                  "LYKANAX", "GELASABLE", "CHELONET", "CAIRNOLITH", "NEMELEON", "KAPRODON"],
    }),
    CAVE: (48, 50, {
        "Morning": ["CAIRNOLITH", "PLOUTERAS", "HYPHANTIS", "CHELONET", "CAIRNOLITH", "KALYPTOR",
                    "PLOUTERAS", "ENIGMAW", "HYPHANTIS", "SOPHOWL", "ENIGMAW", "KALYPTOR"],
        "Night": ["KALYPTOR", "PLOUTERAS", "HYPHANTIS", "CAIRNOLITH", "SOPHOWL", "KALYPTOR",
                  "PLOUTERAS", "ENIGMAW", "CHELONET", "SOPHOWL", "ENIGMAW", "KALYPTOR"],
    }),
}
RATE = {R26: 20, LAKE: 20, R27: 20, CAVE: 10}


def mons(rows):
    return [{"min_level": a, "max_level": b, "species": "SPECIES_" + s} for s, a, b in rows]


def water(night):
    """Stymphalia's black water and the upper Eurotas: Karkitox in the reeds,
    Galenyon off the banks; the rods bring up the first stages, lower down."""
    surf = [("KARKITOX", 47, 50), ("GALENYON", 47, 50), ("CHELONET", 47, 49), ("KARKITOX", 49, 50),
            ("KALYPTOR" if night else "GALENYON", 50, 50)]
    fish = [("KETOFRY", 30, 34), ("KARKIPOOL", 30, 34),
            ("KARKIPOOL", 38, 42), ("HALCYLING", 38, 42), ("KETOFRY", 38, 42),
            ("KARKITOX", 46, 49), ("GALENYON", 46, 49), ("KYNOKETOS" if night else "KARKITOX", 46, 49),
            ("KARKITOX", 48, 50), ("GALENYON", 50, 50)]
    return {"water_mons": {"encounter_rate": 4, "mons": mons(surf)},
            "fishing_mons": {"encounter_rate": 30, "mons": mons(fish)}}


def write_wild():
    path = ROOT / "src/data/wild_encounters.json"
    data = json.loads(path.read_text())
    group = next(gr for gr in data["wild_encounter_groups"] if gr.get("for_maps"))
    ids = {MAP[n] for n in LAND}
    keep = [e for e in group["encounters"] if e.get("map") not in ids]
    new = []
    for name, (lo, hi, tables) in LAND.items():
        for time, species in tables.items():
            rows = []
            for i, sp in enumerate(species):
                a = lo + (1 if i >= 6 else 0) + (1 if i >= 10 else 0)
                b = min(hi, a + (1 if i < 6 else 2))
                if sp == "CHALKIP":
                    a = b = 46
                rows.append((sp, min(a, hi), b))
            e = {"map": MAP[name], "base_label": f"g{name}_{time}",
                 "land_mons": {"encounter_rate": RATE[name], "mons": mons(rows)}}
            e.update(water(time == "Night"))
            if name in (R26, CAVE):
                e["rock_smash_mons"] = {"encounter_rate": 20, "mons": mons([
                    ("CAIRNOLITH", 47, 49), ("CAIRNOLITH", 48, 50), ("CHELONET", 47, 49),
                    ("PLOUTERAS", 48, 50), ("LAOLITH", 50, 50)])}
            new.append(e)
    group["encounters"] = keep + new
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Herms: the two route herms (Wings landings) and the lake's travel herm
# ---------------------------------------------------------------------------

def sub(path, old, new, once=True):
    t = path.read_text()
    if new in t:
        return
    if old not in t:
        raise SystemExit(f"{path}: can't find {old!r}")
    path.write_text(t.replace(old, new, 1 if once else -1))


def write_herms():
    hl = ROOT / "src/data/heal_locations.json"
    data = json.loads(hl.read_text())
    items = data["heal_locations"] if isinstance(data, dict) else data
    want = {"HEAL_LOCATION_HERM_AETHOS_ROUTE_26": (MAP[R26], R26_HERM[0], R26_HERM[1] + 1),
            "HEAL_LOCATION_HERM_AETHOS_ROUTE_27": (MAP[R27], R27_HERM[0], R27_HERM[1] + 1)}
    for hid, (mp, x, y) in want.items():
        row = next((h for h in items if h["id"] == hid), None)
        if row is None:
            at = next(i for i, h in enumerate(items) if h["id"] == "HEAL_LOCATION_HERM_AETHOS_ROUTE_25") + 1
            items.insert(at + (hid.endswith("27")), {"id": hid, "map": mp, "x": x, "y": y})
        else:
            row.update(map=mp, x=x, y=y)
    hl.write_text(json.dumps(data, indent=2) + "\n")
    herms = ROOT / "src/data/ichor_herms.h"
    rows = ""
    for n, name, (x, y) in ((26, R26, R26_HERM), (27, R27, R27_HERM)):
        rows += f'''    [HERM_AETHOS_ROUTE_{n}] = {{
        .map = {MAP[name]},
        .mapsec = MAPSEC_AETHOS_ROUTE_{n},
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_{n},   // ({x},{y}); land at ({x},{y + 1})
    }},
'''
    t = herms.read_text()
    if "[HERM_AETHOS_ROUTE_26]" not in t:
        sub(herms, "    [HERM_AETHOS_ROUTE_14] = {", rows + "    [HERM_AETHOS_ROUTE_14] = {")
    # the lake's travel herm (MAP_DESIGN §2: a rest stop's herm), id 24
    sub(ROOT / "include/constants/ichor.h",
        "#define TOWN_HERM_COUNT             24  // new towns take the next ids",
        "#define TOWN_HERM_STYMPHALIA        24  // Lake Stymphalia's rest stop, by Akanthis's hut\n"
        "#define TOWN_HERM_COUNT             25  // new towns take the next ids")
    sub(ROOT / "include/constants/flags.h",
        "#define FLAG_ICHOR_TOWN_HERM_SPARE_24           (FLAG_ICHOR_GENERAL_START + 0x4B8) // Ichor: travel herm 24, kept for the next town: rename it (engine, SYSTEMS §4)",
        "#define FLAG_ICHOR_TOWN_HERM_STYMPHALIA        (FLAG_ICHOR_GENERAL_START + 0x4B8) // Ichor: Lake Stymphalia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_STYMPHALIA)")
    lx, ly = LAKE_LAND
    sub(ROOT / "src/data/ichor_town_herms.h",
        "    [TOWN_HERM_ASCENT]     = { MAP_ASCENT_2F,           4, 41, HEAL_LOCATION_NONE,                COMPOUND_STRING(\"The Ascent\") },\n",
        "    [TOWN_HERM_ASCENT]     = { MAP_ASCENT_2F,           4, 41, HEAL_LOCATION_NONE,                COMPOUND_STRING(\"The Ascent\") },\n"
        f"    [TOWN_HERM_STYMPHALIA] = {{ MAP_LAKE_STYMPHALIA,    {lx}, {ly}, HEAL_LOCATION_NONE,                COMPOUND_STRING(\"Stymphalia\") }},\n")
    sub(ROOT / "tools/ichor/maps/town_herms.py",
        '    ("Ascent_2F",         (3, 41),   (3, 42),   (4, 41),   "the cloud ledges\' landing, up from the slopes"),\n',
        '    ("Ascent_2F",         (3, 41),   (3, 42),   (4, 41),   "the cloud ledges\' landing, up from the slopes"),\n'
        f'    ("LakeStymphalia",    {LAKE_HERM},  {LAKE_PLAQUE},  {LAKE_LAND},  "the causeway\'s foot, from Route 26"),\n')


# MAIN_MARKER

BUILDERS = [build_r26, build_lake, build_r27, build_cave]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    bad = 0
    for b in BUILDERS:
        m, segs, views, stem, floats = b()
        if args.only and stem not in args.only.split(","):
            continue
        problems, mand, forced = check(m, segs, 8 if stem.startswith(("route", "lake")) else 0, floats=floats)
        if args.walk:
            print(KP.walk_text(m))
        if args.render:
            KP.render(m, args.render, stem, views)
        for p in problems:
            print(f"PROBLEM {m.name}: {p}")
        print(f"{m.name}: {m.w}x{m.h}, forced grass {forced}, {len(m.spec.trainers)} trainers, "
              f"{len(mand)} on the road ({', '.join(mand)}), {len(problems)} problems")
        bad += len(problems)
    claim_flags()
    write_trainers()
    write_wild()
    write_herms()
    arkadia_seam()
    import town_herms as TH
    for row in TH.TOWNS:
        if row[0] in ("LakeStymphalia", "Lakonia"):
            TH.apply(row)
    seal = check_seal()
    print(f"the lookout's seal: {len(seal)} pushes")
    return 1 if bad else 0


def check_seal():
    """The lookout's two drums onto its two sills: solvable from the yard's mouth."""
    import ascent_lib
    m = json.loads((ROOT / f"data/maps/{R27}/map.json").read_text())
    blocks = np.fromfile(ROOT / f"data/layouts/{R27}/map.bin", "<u2").reshape(R27_H, R27_W)
    yard = {(x, y) for x in range(27, 39) for y in range(12, 16) if not blocks[y, x] & 0xC00}
    taken = {(o["x"], o["y"]) for o in m["object_events"] if "BOULDER" not in o["graphics_id"]}
    plan = ascent_lib.push_plan(yard - taken, R27_DRUMS, R27_PLATES, (28, 13))
    if not plan:
        raise SystemExit("Route 27: the lookout's drum seal can't be solved")
    PLANS["seal"] = plan
    return plan


PLANS = {}


if __name__ == "__main__":
    sys.exit(main())
