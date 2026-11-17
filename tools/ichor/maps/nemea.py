#!/usr/bin/env python3
"""Build the Arkadia--Nemea--Emporion return loop: Route 13, Nemea, Route 14
and the Tretos (Route 14's cave), with their events, scripts, wild tables and
review renders. This file owns those maps; tools/ichor/maps/nemea_rooms.py
lays out Nemea's two rooms, and this file writes their events.

Route 13, the highland road (56x28). *Down out of Arkadia: a hoplite at the
wood's edge, the oak wood and its acorn-gatherer, a clearing with the great
herm, then the scarp. A cut stair drops to the valley road under the cliff, a
pilgrim and the second band, and a ford over the brook where a shepherd
waits.* Off the road: the high meadow and its beekeeper, a hermit's cell
behind rubble (the Hammer), a glade behind a thicket (the Sickle), the rim
that hops back down to the road, Pan's corner in the lower wood, and a crag
pocket above the cliff that only climbing reaches.

Nemea (44x36). *The Games' valley.* The palaestra (a room), Molorchos's
cottage (a room), the healer's tent and the merchant's cart on the road,
Zeus's ruined temple on its paving with Opheltes's mound and the Langia
spring beside it, the stadium's sand track, the athletes' outcamp, the
river pool with its islet (the Conch), and the lion's den in the crag:
two mouths, one behind a great boulder (Hephaestus's Hammer), one high in
the cliff (climbing). The den stays sealed until the Labors.

Route 14, the Tretos road (80x26). *The Nemean hills close into a gorge.* A
hoplite on the valley road, a stair up the gorge wall, the gorge itself with
its herm and a band, and the cave mouth at the ridge. A stream bed below
with a rubble-shut gully (the Hammer) and a great-boulder cleft (later).
East of the ridge: the ravine, the ford, the knoll's stair and its ledge
back down, the river pool's islet (the Conch), and the Isthmus plain to
Emporion's Nemea Gate. A column drum on the ridge top (the Girdle) opens a
one-way shortcut back west over the ridge.

The Tretos (36x20), Route 14's cave: dark (the Torch), with rubble on the
road through (the Hammer), a cobweb over a side room (the Torch), the
brazier that lights the cave for good, an underground pool with an islet
(the Conch), a thornweb (the Three-Flamed Torch) and a great boulder
(Hephaestus's Hammer) closing two deeper passages.

Pieces come from build/skiron/catalog.json (make it with
/usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile) and the cave
from data/tilesets/secondary/cave_dark/catalog.json.

Usage: /usr/bin/python3 tools/ichor/maps/nemea.py [--render DIR] [--walk] [--no-rooms]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import kithairon as K  # noqa: E402  (the Skiron grid, painters and checks)
import route5 as R5  # noqa: E402
import water_tables  # noqa: E402
from thyrsa import Map, const, obj, read, write  # noqa: E402,F401

GFX = "OBJ_EVENT_GFX_ICHOR_"
SIGN, GRASS, TALL, BOULDER = R5.SIGN, R5.GRASS, R5.TALL, R5.BOULDER
SEAM_COLS = 8              # columns nearest a left/right seam to a non-Skiron map: aethos only
HERM = 0x01B
CAVE_TOP, CAVE_DOOR = R5.CAVE_TOP, R5.CAVE_DOOR
FORD = 0x13B               # stepping stones in the shallows (MB_SHALLOW_WATER, wadeable)
RIVER = 0x170
SAND = R5.SAND
SOIL = {"tl": 0x103, "t": 0x104, "tr": 0x105, "l": 0x10B, "c": 0x10C, "r": 0x10D,
        "bl": 0x113, "b": 0x114, "br": 0x115}
ASH = {"tl": 0x100, "t": 0x101, "tr": 0x102, "l": 0x108, "c": 0x109, "r": 0x10A,
       "bl": 0x110, "b": 0x111, "br": 0x112}
SPRING = [[0x0B0, 0x0B1, 0x0B2], [0x0B8, 0x0B9, 0x0BA], [0x0C0, 0x0C1, 0x0C2]]
ALTAR, TRIPOD = 0x131, 0x130
PALAESTRA = [[0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
             [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
             [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
             [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
             [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]]
COTTAGE = [[0x008, 0x009, 0x00A], [0x010, 0x011, 0x012], [0x018, 0x019, 0x01A], [0x020, 0x021, 0x022]]

R13, NEMEA, R14, TRETOS = "Route13_HighlandRoad", "Nemea", "Route14_NemeaRoad", "Route14_Tretos"
PALAESTRA_MAP, COTTAGE_MAP = "Nemea_Palaestra", "Nemea_MolorchosHouse"

# Seams. A left/right connection's offset is the neighbour's shift down, so its
# row = ours - offset.
ARKADIA_ROWS = range(10, 14)       # Arkadia's right edge is open at its rows 22-25 (offset -12)
R13_EAST_ROWS = range(17, 19)      # = Nemea's west rows (offset 0)
NEMEA_EAST_ROWS = range(17, 19)    # = Route 14's west rows (offset 0)
GATE_ROW = 13                      # Route 14's exit row; Emporion's one-tile Nemea Gate is its y 41
EMPORION_OFFSET = GATE_ROW - 41

# The old placeholder builder (kept for astyra.py, which builds Routes 15 and 16
# with it): roads() and encounters_and_teams() below.
ROADS = [
    ("Route13_HighlandRoad", "R13", 30,
     ["POLYDOROS", "ANTHE", "LYKON", "THEANO", "KALLIAS", "AGLAON"]),
    ("Route14_NemeaRoad", "R14", 31,
     ["ISON", "PHILOMELE", "NEOKLES", "ERATO", "DEMADES", "KLEARCHOS"]),
]


# ---------------------------------------------------------------------------
# The grid: kithairon's, plus seam columns, water, sand, fords, soil and paving
# ---------------------------------------------------------------------------
#   ~  river or pool water (elevation 1, fishable)   _  sand: riverbed or track
#   x  stepping stones (wadeable)                    O  tilled soil (vines)
#   A  stone paving (the temple's)
class Grid(K.Grid):
    def __init__(self, name, w, h, west=False, east=False):
        super().__init__(name, w, h)
        self.cols = set()
        if west:
            self.cols |= set(range(SEAM_COLS))
        if east:
            self.cols |= set(range(w - SEAM_COLS, w))
        self.water = np.zeros((h, w), bool)


def autotile(g, ch, ids, same):
    for y in range(g.h):
        for x in range(g.w):
            if g.g[y][x] != ch or g.fixed[y, x]:
                continue

            def out(dx, dy):
                X, Y = x + dx, y + dy
                return 0 <= X < g.w and 0 <= Y < g.h and g.g[Y][X] not in same
            n, s, w, e = out(0, -1), out(0, 1), out(-1, 0), out(1, 0)
            key = "c" if (n and s) or (w and e) else R5.edge9(n, s, w, e)
            g.set(x, y, ids[key], False, "ground_" + ch)


def terrain(g):
    """Water with sandy banks, fords, sand, soil and paving, before the trees."""
    wet = set("~x")
    for y in range(g.h):
        for x in range(g.w):
            if g.g[y][x] == "~":
                def dry(dx, dy):
                    X, Y = x + dx, y + dy
                    return 0 <= X < g.w and 0 <= Y < g.h and g.g[Y][X] not in wet
                n, s, w, e = dry(0, -1), dry(0, 1), dry(-1, 0), dry(1, 0)
                # a pool's corner takes its north or south edge: the set has no
                # concave corner, and an island's convex one bulges the water out
                mid = {(1, 0, 1, 0): 0x12C, (1, 0, 0, 1): 0x12C, (0, 1, 1, 0): 0x11C, (0, 1, 0, 1): 0x11C,
                       (1, 0, 0, 0): 0x12C, (0, 1, 0, 0): 0x11C, (0, 0, 1, 0): 0x125, (0, 0, 0, 1): 0x123,
                       }.get((n, s, w, e), RIVER)
                g.set(x, y, mid, False, "water")
                g.water[y, x] = True
            elif g.g[y][x] == "x":
                g.set(x, y, FORD, False, "ford")
    autotile(g, "_", SAND, set("_~x"))
    autotile(g, "O", SOIL, set("O"))
    autotile(g, "A", ASH, set("A"))


def blob(g, ch, cx, cy, rx, ry, salt=0, only=None):
    """An irregular patch (grass, a meadow) instead of a rectangle: an ellipse
    whose rim is jittered by noise."""
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if not (0 <= x < g.w and 0 <= y < g.h):
                continue
            d = ((x - cx) / (rx + .5)) ** 2 + ((y - cy) / (ry + .5)) ** 2
            if d <= 1 - (K.noise(x, y, 60 + salt) - 50) / 160 and (only is None or g.g[y][x] in only):
                g.g[y][x] = ch


def round_pools(g):
    """A pool's corner cells become bank: the water set has edges and convex
    corners (an island's), not concave ones, so a square corner would show a
    spur of sand poking into the water."""
    wet = set("~x")
    corners = []
    for y in range(g.h):
        for x in range(g.w):
            if g.g[y][x] != "~":
                continue
            dry = [not (0 <= x + dx < g.w and 0 <= y + dy < g.h) or g.g[y + dy][x + dx] not in wet
                   for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0))]
            if (dry[0] or dry[1]) and (dry[2] or dry[3]):
                corners.append((x, y))
    for x, y in corners:
        g.g[y][x] = "_"


def massif(g, ch="M"):
    """Bare rock in bulk (league_lib.massif's way): every column of the mass is
    a cliff in strata, brink on top, faces down its height, a foot at the
    bottom, side pieces where it's open, so a ridge reads as one wall of rock."""
    def m(x, y):
        return 0 <= x < g.w and 0 <= y < g.h and g.g[y][x] == ch
    for x in range(g.w):
        y = 0
        while y < g.h:
            if not m(x, y) or g.fixed[y, x]:
                y += 1
                continue
            y0 = y
            while y < g.h and m(x, y) and not g.fixed[y, x]:
                y += 1
            y1 = y - 1
            for yy in range(y0, y1 + 1):
                top, bottom = yy == y0 and y0 > 0, yy == y1 and y1 < g.h - 1
                open_w, open_e = not m(x - 1, yy) and x > 0, not m(x + 1, yy) and x < g.w - 1
                if top:
                    g.named("cliff_brink", "B" if K.noise(x, yy, 4) < 22 else "A", x, yy)
                elif bottom:
                    below = g.at(x, yy + 1)
                    g.named("bank" if below == "p" else "bank_grass", "foot_" + "ABC"[K.noise(x, yy, 5) % 3], x, yy)
                elif open_w and not open_e:
                    g.named("cliff_side", "side_w", x, yy)
                elif open_e and not open_w:
                    g.named("cliff_side", "side_e", x, yy)
                else:
                    face = "face_u_" if (yy - y0) % 2 else "face_l_"
                    n = K.noise(x, yy, 11)
                    var = ("B" if n < 16 else "C" if n < 30 else "A") if face == "face_u_" else ("C" if n < 20 else "A")
                    g.named("cliff", face + var, x, yy)
                g.solid[yy, x] = True


def seam_columns(g):
    """The columns nearest a seam to another secondary tileset take aethos
    pieces only: cypresses, stone pines and boulders for woods, aethos tall
    grass, plain grass (MAP_DESIGN.md §5)."""
    for y in range(g.h):
        for x in sorted(g.cols):
            if g.fixed[y, x]:
                continue
            k = g.g[y][x]
            if k in "#^":
                n = K.noise(x, y, 77 + y // 3)
                if n < 45 and g.room(x, y, 2, 2, ("#", "^"), strip_ok=True) and x + 1 in g.cols:
                    for j in range(2):
                        for i in range(2):
                            g.set(x + i, y + j, R5.STONE_PINE[j][i], True, "woods")
                elif g.room(x, y, 1, 2, ("#", "^"), strip_ok=True) and n < 75:
                    g.set(x, y, R5.CYPRESS_TOP, True, "woods")
                    g.set(x, y + 1, R5.CYPRESS_BOT, True, "woods")
                else:
                    g.set(x, y, BOULDER, True, "woods")
            elif k == ",":
                g.set(x, y, TALL, False, "tall")
            elif k in ".k":
                g.set(x, y, GRASS, False, "grass")


def check_seams(g):
    bad = [(x, y) for y in range(g.h) for x in g.cols if int(g.mt[y, x]) >= 0x200]
    if bad:
        raise SystemExit(f"{g.name}: Skiron metatiles in a seam column at {bad[:6]}")


def stamp(g, rows, x, y, door=None, kind="building"):
    for j, row in enumerate(rows):
        for i, mid in enumerate(row):
            g.set(x + i, y + j, mid, (i, j) != door, kind)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
class Spec(K.Spec):
    """kithairon's Spec, with warps, coord events, later gates and more kinds of
    obstacle: rubble (the Hammer), drums (the Girdle), great boulders
    (Hephaestus's Hammer) and webs."""

    def __init__(self, name, map_id, tag):
        super().__init__(name, map_id, tag)
        self.warps, self.coords, self.extra = [], [], []

    def gate(self, name, gfx, x, y, script, flag="0", invisible=False):
        o = K.obj(None, "OBJ_EVENT_GFX_" + gfx, x, y, None, script, flag)
        o["local_id"] = "LOCALID_" + R5.re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", self.name).upper() + "_" + name.upper()
        if invisible:
            o["movement_type"] = "MOVEMENT_TYPE_INVISIBLE"
        self.extra.append(o)

    def objects(self):
        return super().objects() + self.extra


def write_events(spec, music="MUS_ICHOR_ROAD", kind="MAP_TYPE_ROUTE", mapscripts=None, header=None):
    path = ROOT / f"data/maps/{spec.name}/map.json"
    m = json.loads(path.read_text())
    m["music"] = music
    m["map_type"] = kind
    m["connections"] = spec.connections or None
    m["object_events"] = spec.objects()
    m["warp_events"] = spec.warps
    m["coord_events"] = spec.coords
    m["bg_events"] = spec.bgs()
    path.write_text(json.dumps(m, indent=2) + "\n")
    scripts = [mapscripts or f"mapscripts {spec.name}_MapScripts {{}}",
               "// Generated by tools/ichor/maps/nemea.py; edit the builder, not this file."]
    for t in spec.trainers:
        tid = t.get("id", f"TRAINER_ICHOR_{spec.tag}_{t['name']}")
        scripts.append(f'''script {spec.px}{t["name"]} {{
    trainerbattle_single({tid}, format("{t["intro"]}"), format("{t["defeat"]}"))
    msgbox(format("{t["after"]}"), MSGBOX_AUTOCLOSE)
    end
}}''')
    scripts += spec.scripts
    (ROOT / f"data/maps/{spec.name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")


def trainer(s, name, gfx, x, y, facing, sight, intro, defeat, after, mandatory=True, tid=None):
    s.trainer(name, gfx, x, y, facing, sight, intro, defeat, mandatory)
    s.trainers[-1]["after"] = after
    if tid:
        s.trainers[-1]["id"] = tid


def sign(s, name, x, y, text, facing="ANY"):
    s.signs.append((x, y, facing, name))
    s.scripts.append(f'''script {s.px}{name} {{
    msgbox(format("{text}"), MSGBOX_SIGN)
    end
}}''')


def talker(s, name, text):
    s.scripts.append(f'''script {s.px}{name} {{
    lock
    faceplayer
    msgbox(format("{text}"))
    release
}}''')


def item(s, it, x, y, flag):
    s.items.append(("ITEM_" + it, x, y, "FLAG_ICHOR_" + flag))


def hidden(s, it, x, y, flag):
    s.hidden.append(("ITEM_" + it, x, y, "FLAG_ICHOR_" + flag))


def gift(s, name, flag, before, it, after):
    s.scripts.append(f'''script {s.px}{name} {{
    lock
    faceplayer
    if (!flag({flag})) {{
        msgbox(format("{before}"))
        giveitem({it})
        if (var(VAR_RESULT) == TRUE) {{
            setflag({flag})
        }}
        release
        end
    }}
    msgbox(format("{after}"))
    release
}}''')


# ---------------------------------------------------------------------------
# Route 13, the highland road (56x28)
# ---------------------------------------------------------------------------
def plan_r13():
    W, H = 56, 28
    g = Grid(R13, W, H, west=True)
    r = g.rect
    # --- the plateau: Arkadia's road, the hoplite's meadow ------------------------
    r("p", 0, 10, 9, 13)                       # Arkadia's road, four wide
    r(".", 8, 5, 13, 9)                        # the meadow at the wood's edge
    blob(g, ",", 10.5, 6, 2, 1.5, only=".")
    r(".", 10, 10, 13, 10)
    r(".", 2, 5, 7, 8)                         # a meadow in Arkadia's cypresses
    r(".", 5, 9, 7, 9)
    blob(g, ",", 4, 6.5, 2, 1.2, 3, only=".")
    g.put("k", (2, 9))                         # the west sign
    r("p", 10, 11, 31, 12)                     # the road, two wide
    # --- the oak wood: band 1, Anthe -------------------------------------------
    r(",", 15, 11, 18, 12)
    g.put(".", (21, 10))                       # Anthe's niche
    # --- the clearing and the herm -----------------------------------------------
    r(".", 24, 9, 29, 13)
    g.put("k", (25, 9))
    # --- the high meadow (optional): long grass, the hives, the beekeeper ---------
    r(".", 24, 2, 44, 8)
    blob(g, ",", 30, 4, 3.5, 1.6, only=".")
    blob(g, ",", 40, 7, 3.5, 1.5, 1, only=".")
    r("#", 34, 2, 36, 4)
    r("#", 24, 2, 25, 3)
    g.put("k", (40, 3), (41, 3))               # the hives
    # the hermit's cell, behind rubble (the Hammer)
    r(".", 16, 3, 21, 6)
    r(".", 22, 5, 23, 5)
    g.put("k", (19, 3))
    # the glade, behind a thicket (the Sickle)
    r(".", 45, 5, 46, 5)
    r(".", 47, 2, 53, 7)
    blob(g, ",", 50.5, 5, 2, 1.4, 2, only=".")
    # --- the scarp: the stair, the rim and its ledge, the crag pocket -------------
    r("p", 30, 13, 31, 13)
    for y, ch in ((14, "b"), (15, "u"), (16, "f")):
        r(ch, 8, y, W - 1, y)
        r("s" if ch == "u" else "p", 30, y, 31, y)
        r("v" if ch == "u" else ".", 33, y, 35, y)
    r(".", 33, 9, 44, 13)                      # the rim, east of the clearing's wood
    blob(g, ",", 40, 11, 2.5, 1.4, 4, only=".")
    r(".", 46, 11, 48, 13)                     # the crag pocket: climbing only
    g.put("k", (49, 16))                       # the east sign
    # --- the valley road: Lykon, band 2, the ford, Kallias -----------------------
    r("p", 30, 17, W - 1, 18)
    g.put(".", (37, 19))                       # Lykon's niche
    r(",", 39, 17, 42, 18)
    r("x", 50, 17, 51, 18)                     # the ford
    r("_", 49, 19, 52, 26)                     # the brook's sandy bed
    r("~", 50, 19, 51, 25)
    g.put(".", (53, 19))                       # Kallias's spot
    # the south meadow (optional): Aglaon's knoll
    g.put(".", (45, 19))
    r(".", 41, 20, 47, 25)
    blob(g, ",", 44, 22, 2.5, 1.5, 5, only=".")
    # the lower wood west of the stair (optional): Pan's corner, Theano
    r("p", 24, 17, 29, 18)
    r(".", 12, 17, 29, 24)
    blob(g, ",", 17, 20.5, 3.5, 2, 6, only=".")
    blob(g, ",", 26, 22.5, 2.5, 2, 7, only=".")
    r("#", 21, 22, 23, 24)
    r("#", 12, 17, 14, 17)
    g.put("k", (13, 18))                       # Pan's stele
    return g


def props_r13(g):
    g.set(2, 9, SIGN, True, "sign")
    g.set(25, 9, HERM, True, "herm")
    g.piece("hives", 40, 3)
    g.piece("stele_low", 19, 3)
    g.piece("niches", 20, 14)
    g.set(49, 16, SIGN, True, "sign")
    g.piece("stele_palmette", 13, 17)
    g.piece("pine_tall", 44, 2)
    g.piece("rock", 30, 9)
    g.piece("boulders", 27, 6)
    g.piece("pine_tall", 46, 20)
    for x, y in ((22, 17), (44, 17), (48, 17)):   # fallen rock at the cliff foot
        g.piece("rock_path" if g.g[y][x] == "p" else "rock", x, y)


def spec_r13():
    s = Spec(R13, "MAP_ROUTE13_HIGHLAND_ROAD", "R13")
    s.connections = [{"direction": "left", "map": "MAP_ARKADIA", "offset": -12},
                     {"direction": "right", "map": "MAP_NEMEA", "offset": 0}]
    trainer(s, "POLYDOROS", "HOPLITE", 12, 9, "DOWN", 3,
            "Arkadia's border watch. Show me you're fit for the lowlands.",
            "Fit enough.", "Nemea's healer keeps a lamp burning by the road.", mandatory=False)
    trainer(s, "ANTHE", "HARVESTER", 21, 10, "DOWN", 2,
            "Acorns for the pigs, battles for me.", "The pigs win today.",
            "The oaks here are older than the city.")
    trainer(s, "LYKON", "PILGRIM", 37, 19, "UP", 2,
            "That stair is steeper going down. Ask my knees.", "Ask them again tomorrow.",
            "Nemea's sanctuary is down the valley.")
    trainer(s, "THEANO", "ACOLYTE_F", 22, 18, "LEFT", 4,
            "Pan's corner is no place for shouting.", "...Fine. One shout.",
            "Leave a little honey at his stele. He likes that.", mandatory=False)
    trainer(s, "KALLIAS", "SHEPHERD", 53, 19, "UP", 2,
            "Mind the stepping stones. I'll mind you.", "You kept your footing.",
            "Nemea's just past the bend.")
    trainer(s, "AGLAON", "AUGUR", 46, 24, "LEFT", 3,
            "The birds fly low over this meadow. Rain, or a battle.", "A battle, then.",
            "Clear skies over Nemea.", mandatory=False)
    s.people += [("Beekeeper", "ELDER_M", 42, 4, "DOWN", "0")]
    s.thickets += [("GladeThicket", 46, 5, "0")]
    s.gate("CellRubble", "BREAKABLE_ROCK", 23, 5, "EventScript_RockSmash", "FLAG_ICHOR_R13_RUBBLE")
    item(s, "HYPER_POTION", 30, 7, "ITEM_R13_HEAL")
    item(s, "ULTRA_BALL", 43, 13, "ITEM_R13_BALL")
    item(s, "ETHER", 13, 23, "ITEM_R13_ETHER")
    item(s, "MAX_ETHER", 17, 4, "ITEM_R13_CELL")
    item(s, "MOON_STONE", 52, 3, "ITEM_R13_GLADE")
    item(s, "PP_UP", 47, 12, "ITEM_R13_CRAG")
    hidden(s, "HONEY", 41, 3, "HIDDEN_ITEM_R13_HONEY")          # in the hives
    hidden(s, "REVIVE", 41, 25, "HIDDEN_ITEM_R13_REVIVE")       # Aglaon's knoll
    hidden(s, "SUPER_REPEL", 21, 22, "HIDDEN_ITEM_R13_REPEL")   # in the oaks by Pan's corner
    sign(s, "Sign0", 2, 9, "Route 13, the highland road.\\nWest: Arkadia. East: Nemea, then Emporion.")
    sign(s, "Sign1", 49, 16, "Route 13.\\nWest: up to Arkadia. East: Nemea.")
    s.signs.append((25, 9, "ANY", "Herm"))
    s.scripts.append(f'''script {s.px}Herm {{
    goto(EventScript_IchorGreatHerm)
}}''')
    sign(s, "Handholds", 47, 16, "Old handholds climb the rock. They lead to a ledge up on the scarp.\\p"
         "Something glints up there, out of reach.", "NORTH")
    sign(s, "Cell", 19, 3, "A hermit's stone. The name is worn away, but not the little carved bee.")
    sign(s, "Niches", 21, 16, "Niches cut in the scarp, with clay goats and a bow left in them.\p"
         "Offerings to Artemis, from hunters going down to the valley.", "NORTH")
    sign(s, "Pan", 13, 18, "A stele of Pan, goat-legged, piping. Someone has left a honeycomb.")
    gift(s, "Beekeeper", "FLAG_ICHOR_R13_BEEKEEPER_GIFT",
         "Aristaios taught my grandmother's grandmother to keep bees, they say.\\p"
         "Take a berry from the hedge. The bees won't miss it.", "ITEM_SITRUS_BERRY",
         "Don't swat. They remember faces.")
    return s


# ---------------------------------------------------------------------------
# Nemea (44x36)
# ---------------------------------------------------------------------------
def plan_nemea():
    W, H = 44, 36
    g = Grid(NEMEA, W, H)
    r = g.rect
    r("p", 0, 17, W - 1, 18)                   # the road through
    # --- the palaestra and its yard ----------------------------------------------
    r(".", 1, 9, 11, 16)
    r("k", 3, 4, 8, 8)
    r("p", 6, 9, 7, 16)
    # --- the healer's tent, the merchant's cart, the sign --------------------------
    r(".", 11, 12, 17, 16)
    r("k", 12, 13, 13, 14)
    r(".", 22, 12, 27, 16)
    r("k", 23, 13, 25, 14)
    g.put("k", (16, 16))
    # --- Zeus's sanctuary: the paving, the altar, Opheltes's mound, the spring -------
    r(".", 12, 2, 31, 11)
    r("A", 14, 4, 25, 8)                       # the temple's platform
    r("w", 14, 9, 25, 9)                       # its steps all round, a stair at the front
    r("s", 19, 9, 20, 9)
    r("p", 19, 10, 20, 16)
    g.put("k", (22, 10), (22, 11))             # the altar and its tripod
    r("o", 0, 10, 3, 15)                       # olives in the palaestra's yard
    r("o", 8, 10, 11, 13)
    r("k", 27, 4, 29, 5)                       # the mound
    g.put("k", (28, 6))
    r("k", 27, 8, 29, 10)                      # the spring
    r(",", 13, 2, 14, 2)
    # --- the lion's den: crag, a four-row cliff, two mouths, the lion grass ---------
    r("^", 32, 0, W - 1, 16)
    for y, ch in ((5, "b"), (6, "u"), (7, "l"), (8, "f")):
        r(ch, 33, y, 42, y)
    r(".", 32, 9, 42, 16)
    blob(g, ",", 37.5, 12.5, 4, 2, 8, only=".")
    g.put("k", (34, 9))                        # the warning stele
    g.put(".", (36, 9))                        # under the boulder
    # --- Molorchos's cottage, his soil, the guide -----------------------------------
    r(".", 1, 19, 12, 26)
    r("k", 2, 20, 4, 23)
    r("O", 7, 20, 11, 23)
    # --- the stadium ----------------------------------------------------------------
    r("p", 13, 19, 14, 27)
    r(".", 2, 27, 27, 27)
    r("w", 3, 27, 26, 27)                      # the stone seats along the track
    r("s", 13, 27, 14, 27)
    r("s", 21, 27, 22, 27)
    r("_", 3, 28, 26, 31)
    r(".", 2, 32, 27, 32)
    g.put("k", (2, 28), (2, 29), (3, 32), (26, 32))   # the tunnel; the turning posts
    r(".", 15, 19, 26, 26)                     # the meadow above the track
    blob(g, ",", 21, 22.5, 5, 2.6, 9, only=".")
    # --- the outcamp --------------------------------------------------------------
    r(".", 28, 19, 42, 26)
    for x in (29, 32, 35):
        r("k", x, 20, x + 1, 21)
    g.put("k", (31, 23), (34, 23), (35, 23), (37, 23), (38, 23), (40, 21), (41, 21))
    # --- the river pool and its islet ---------------------------------------------
    r("_", 28, 27, 42, 34)
    r("~", 30, 29, 41, 33)
    r("_", 35, 31, 36, 31)
    r(".", 2, 33, 13, 34)
    blob(g, ",", 7, 33.5, 4.5, 1.2, 10, only=".")
    return g


def props_nemea(g):
    stamp(g, PALAESTRA, 3, 4, door=(3, 4))
    stamp(g, COTTAGE, 2, 20, door=(1, 3))
    g.piece("tent", 12, 13)
    g.piece("cart", 23, 13)
    g.set(16, 16, SIGN, True, "sign")
    # Zeus's temple: drums and rubble on the paving, stumps of columns
    for x, y in ((13, 5), (13, 8), (26, 6), (26, 8), (16, 11), (17, 10)):
        g.piece("drum", x, y)
    g.piece("rubble", 15, 5)
    g.piece("rubble", 22, 5)
    for x in (16, 18, 21, 23):
        g.piece("stele_palmette", x, 2)
    g.set(22, 10, TRIPOD, True, "altar")
    g.set(22, 11, ALTAR, True, "altar")
    g.piece("mound", 27, 4)
    g.piece("stele_low", 28, 6)
    stamp(g, SPRING, 27, 8, kind="spring")
    # the den
    g.set(36, 7, CAVE_TOP, True, "den")
    g.set(36, 8, CAVE_DOOR, True, "den")
    for x in range(33, 43):
        if x not in (36, 40):
            g.named("cliff", "face_l_" + "AC"[K.noise(x, 7, 3) % 2], x, 7)
    g.named("cliff", "face_l_B", 40, 7)
    g.piece("stele_low", 34, 9)
    # the stadium's turning posts, the cottage's yard
    g.set(2, 28, CAVE_TOP, True, "tunnel")
    g.set(2, 29, CAVE_DOOR, True, "tunnel")
    g.piece("milestone", 3, 32)
    g.piece("milestone", 26, 32)
    g.piece("hives", 5, 24)
    g.piece("baskets", 12, 21)
    # the outcamp
    g.piece("tent", 29, 20)
    g.piece("tent_b", 32, 20)
    g.piece("tent", 35, 20)
    g.piece("cookfire", 31, 23)
    g.piece("bedrolls", 34, 23)
    g.piece("bedrolls", 35, 23)
    g.piece("firewood", 37, 23)
    g.piece("amphorae", 40, 21)
    g.piece("baskets", 41, 21)
    for x, y in ((35, 28), (35, 34), (42, 30), (42, 23)):
        g.piece("rock_path" if g.g[y][x] == "_" else "rock", x, y)
    g.piece("rock", 8, 34)


def spec_nemea():
    s = Spec(NEMEA, "MAP_NEMEA", "NEMEA")
    s.connections = [{"direction": "left", "map": "MAP_ROUTE13_HIGHLAND_ROAD", "offset": 0},
                     {"direction": "right", "map": "MAP_ROUTE14_NEMEA_ROAD", "offset": 0}]
    s.warps = [dict(x=6, y=8, elevation=0, dest_map="MAP_NEMEA_PALAESTRA", dest_warp_id="0"),
               dict(x=3, y=23, elevation=0, dest_map="MAP_NEMEA_MOLORCHOS_HOUSE", dest_warp_id="0")]
    s.people += [("Healer", "HEALER", 12, 15, "DOWN", "0"),
                 ("Merchant", "MERCHANT", 24, 15, "DOWN", "0"),
                 ("Guide", "SHEPHERD", 9, 19, "DOWN", "0"),
                 ("Runner", "YOUTH_M", 30, 24, "LEFT", "0"),
                 ("Discus", "YOUTH_F", 37, 25, "UP", "0"),
                 ("Keeper", "ELDER_F", 17, 12, "DOWN", "0")]
    s.gate("LionBoulder", "PUSHABLE_BOULDER", 36, 9, "EventScript_IchorGreatBoulder",
           "FLAG_ICHOR_NEMEA_LION_BOULDER")
    item(s, "RARE_CANDY", 25, 31, "ITEM_NEMEA_TRACK")
    item(s, "BIG_PEARL", 36, 31, "ITEM_NEMEA_ISLET")
    hidden(s, "STAR_PIECE", 28, 4, "HIDDEN_ITEM_NEMEA_MOUND")
    hidden(s, "NUGGET", 29, 8, "HIDDEN_ITEM_NEMEA_SPRING")
    sign(s, "Sign", 16, 16, "NEMEA\\nWhere the Games are held for Zeus.\\pWest: Arkadia. East: the Tretos road to Emporion.")
    s.signs += [(22, 11, "ANY", "Zeus"), (34, 9, "ANY", "LionCave")]
    s.scripts.append(f'''script {s.px}Zeus {{
    msgbox(format("The altar of Zeus's old temple. Its columns lie in drums across the paving.\\p"
                  "A shepherd has left a little wool at the foot of the stone."), MSGBOX_SIGN)
    end
}}''')
    s.scripts.append(f'''script {s.px}LionCave {{
    msgbox(format("A warning stele: THE LION'S DEN. KEEP OUT.\\p"
                  "The den has two mouths. A great boulder seals the low one.\\p"
                  "The other is high in the cliff. Something breathes inside."), MSGBOX_SIGN)
    end
}}''')
    sign(s, "Mound", 28, 6, "The mound of Opheltes, the baby the Games were first held for.\\p"
         "Victors still leave a sprig of wild celery here.")
    s.signs += [(27, 9, "ANY", "Spring"), (29, 9, "ANY", "Spring")]
    s.scripts.append(f'''script {s.px}Spring {{
    msgbox(format("The Langia spring. Its water falls from a cleft in the stone.\\p"
                  "Behind the fall there's a hollow, and the gleam of something old.\\p"
                  "You'd need to climb the water itself to reach it."), MSGBOX_SIGN)
    end
}}''')
    sign(s, "HighMouth", 40, 8, "Handholds cut long ago climb to the den's high mouth.\\p"
         "Claw marks score the rock beside them.", "NORTH")
    sign(s, "Track", 3, 32, "A turning post of the stadium. Runners round it and race back.")
    sign(s, "Tunnel", 2, 29, "The athletes' tunnel, where runners came out to the crowd.\p"
         "Its far end is bricked up. Someone has scratched a pair of wings on the bricks.")
    s.scripts.append(f'''script {s.px}Healer {{
    setvar(VAR_0x800B, LOCALID_NEMEA_HEALER)
    call(Ichor_EventScript_AsclepeionHealer)
    waitmessage
    waitbuttonpress
    release
}}''')
    s.scripts.append(f'''script {s.px}Merchant {{
    goto(ArkadiaApproach_EventScript_Merchant)
}}''')
    talker(s, "Guide", "Down from Arkadia? Then you've seen the new moon.\\p"
           "Emporion lies east, through the Tretos. Take a light; the pass runs under the hill.\\p"
           "Stay on the road. I still count my goats twice.")
    talker(s, "Runner", "We train for the next Games. One lap of the track, there and back.\\p"
           "The old runners say a pair of winged sandals once ran it in a breath.\\p"
           "If you ever find wings for your feet, come race me.")
    talker(s, "Discus", "The prize here is a crown of wild celery. It wilts in a week.\\p"
           "That's the point. You have to keep winning.")
    talker(s, "Keeper", "I sweep Zeus's paving. Every drum you see was a column once.\\p"
           "Herakles dedicated the Games here, after the lion. Its den is up in the crag.\\p"
           "It's been sealed since. Some nights, it isn't quiet.")
    return s


# ---------------------------------------------------------------------------
# Route 14, the Tretos road (80x26)
# ---------------------------------------------------------------------------
DRUM = (45, 3)


def plan_r14():
    W, H = 80, 26
    g = Grid(R14, W, H, east=True)
    r = g.rect
    for y in range(H):
        for x in range(W):
            g.g[y][x] = "^"
    # --- the Nemean hills: the valley road, Ison, band 0 ---------------------------
    r("#", 0, 0, 9, H - 1)
    r("p", 0, 17, 15, 18)
    r(".", 2, 10, 7, 16)                      # the hills' sheep meadow
    blob(g, ",", 4.5, 12.5, 2.8, 3, 11, only=".")
    g.put(".", (8, 16))                       # Ison's niche
    g.put("k", (2, 15))                       # the west sign
    r(",", 10, 17, 13, 18)
    # --- the gorge wall and its stair ----------------------------------------------
    r("p", 14, 15, 15, 16)
    for y, ch in ((12, "b"), (13, "u"), (14, "f")):
        r(ch, 10, y, 30, y)
        r("s" if ch == "u" else "p", 14, y, 15, y)
    # --- the gorge: Philomele, band 1, the herm, the mouth -------------------------
    r("p", 14, 8, 29, 9)
    r("p", 14, 10, 15, 11)
    r(".", 10, 5, 13, 11)
    r(".", 16, 10, 17, 11)
    r(",", 19, 8, 22, 9)
    g.put("k", (23, 7))                       # the herm
    r(".", 24, 5, 29, 7)
    r(",", 24, 5, 27, 6)
    g.put("k", (29, 6), (29, 7))              # the Tretos's west mouth
    r(".", 28, 3, 31, 4)                      # where the ledge comes down
    r("<", 32, 3, 32, 3)
    # the ridge and the rock behind the east mouth: bare limestone
    for x in range(30, 47):                   # a ragged skyline, a pine terrace halfway down
        top = 5 + K.noise(x // 2, 0, 31) % 3
        r("M", x, top, x, 13 if x > 30 else 18)
        if x > 30:
            r("M", x, 16 + K.noise(x // 3, 1, 32) % 2, x, 25)
    r("M", 49, 0, 55, 8)
    g.put("M", (55, 9))
    # the cleft behind the great boulder (later): a lion-hunters' shrine
    r(".", 10, 2, 12, 4)
    # --- the stream bed below the road: rubble gully, fishing, Neokles ------------------
    r("_", 14, 19, 30, 25)
    r("~", 16, 21, 29, 23)
    r(".", 7, 22, 13, 22)
    r(".", 2, 21, 6, 24)
    r(",", 3, 23, 6, 24)
    # --- the ridge top: the drum's shortcut, west only ----------------------------
    r("p", 33, 3, 44, 3)
    g.put(".", DRUM, (45, 2), (45, 4), (46, 4))
    # --- the ravine: the east mouth, the ford, Demades, band 2 ---------------------
    r(".", 47, 4, 48, 9)
    g.put("k", (49, 7), (49, 8))              # the east mouth
    r("p", 49, 9, 50, 14)
    r("p", 49, 13, W - 1, 14)
    r("x", 52, 13, 53, 14)
    r("_", 51, 15, 56, 15)
    r("_", 51, 16, 58, 25)
    r("_", 51, 9, 54, 12)
    r("~", 52, 9, 53, 12)
    r("~", 52, 16, 57, 24)
    r("_", 54, 19, 55, 21)                    # the islet
    r(",", 57, 13, 60, 14)
    g.put(".", (62, 15))                      # Demades's niche
    # the knoll: cliff and stair up, ledge back down
    for y, ch in ((10, "b"), (11, "u"), (12, "f")):
        r(ch, 55, y, 71, y)
        r("s" if ch == "u" else "p", 66, y, 67, y)
        r("v" if ch == "u" else ".", 59, y, 59, y)
    r(".", 56, 3, 71, 9)
    blob(g, ",", 62, 6, 6.5, 2.6, 12, only=".")
    r("#", 68, 3, 71, 5)
    # the south meadow, behind a thicket (the Sickle)
    g.put(".", (64, 15))
    r(".", 60, 16, 70, 23)
    blob(g, ",", 65, 19.5, 5, 3, 13, only=".")
    # Antikles at the plain's edge
    g.put(".", (69, 12))
    # --- the Isthmus plain (aethos only) ------------------------------------------
    r("o", 72, 0, W - 1, H - 1)
    r(".", 71, 12, W - 3, 15)
    r("p", 71, 13, W - 3, 14)
    r("p", W - 2, GATE_ROW, W - 1, GATE_ROW)
    g.put("k", (74, 12))
    return g


def props_r14(g):
    g.set(23, 7, HERM, True, "herm")
    g.set(29, 6, CAVE_TOP, True, "mouth")
    g.set(29, 7, CAVE_DOOR, False, "mouth")
    g.set(49, 7, CAVE_TOP, True, "mouth")
    g.set(49, 8, CAVE_DOOR, False, "mouth")
    g.set(74, 12, SIGN, True, "sign")
    g.set(2, 15, SIGN, True, "sign")
    for x, y in ((19, 20), (26, 20), (23, 19), (19, 24), (25, 24), (51, 20), (57, 25)):
        g.piece("rock_path", x, y)
    g.piece("stele_family", 11, 2)
    g.piece("rock", 61, 3)


def spec_r14():
    s = Spec(R14, "MAP_ROUTE14_NEMEA_ROAD", "R14")
    s.connections = [{"direction": "left", "map": "MAP_NEMEA", "offset": 0},
                     {"direction": "right", "map": "MAP_EMPORION_CITY", "offset": EMPORION_OFFSET}]
    s.warps = [dict(x=29, y=7, elevation=0, dest_map="MAP_ROUTE14_TRETOS", dest_warp_id="0"),
               dict(x=49, y=8, elevation=0, dest_map="MAP_ROUTE14_TRETOS", dest_warp_id="1")]
    trainer(s, "ISON", "HOPLITE", 8, 16, "DOWN", 2,
            "The Tretos road. Nemea's watch checks everyone headed for the Isthmus.", "Checked.",
            "Nemea's healer keeps a lamp burning by the road.")
    trainer(s, "PHILOMELE", "HARVESTER", 17, 10, "UP", 2,
            "Nothing grows in the gorge but stubbornness.", "And you, apparently.",
            "The Tretos is dark. Keep your torch high.")
    trainer(s, "NEOKLES", "PILGRIM", 22, 20, "DOWN", 1,
            "The stream goes into the hill and never comes out. Where does it go?", "Not my way, at least.",
            "Fishing's good where it sinks.", mandatory=False)
    trainer(s, "ERATO", "ACOLYTE_F", 47, 6, "DOWN", 2,
            "Hecate's roads run through the dark. I came to walk one.", "You walk it faster.",
            "The old brazier in the Tretos still takes a flame.", mandatory=False)
    trainer(s, "DEMADES", "SHEPHERD", 62, 15, "UP", 2,
            "My flock fords here. So do you, after me.", "After you, then.",
            "Emporion's gate is just past the olives.")
    trainer(s, "KLEARCHOS", "AUGUR", 64, 4, "DOWN", 3,
            "From the knoll I read the whole Isthmus. Your turn to be read.", "A good omen, for you.",
            "Hop off the edge. It's the quick way down.", mandatory=False)
    trainer(s, "ANTIKLES", "GOATHERD", 69, 12, "DOWN", 2,
            "My goats climbed the knoll. I'll climb you.", "Down I go.",
            "The olives start here. That's the Isthmus.", tid="TRAINER_ICHOR_R14_ANTIKLES")
    trainer(s, "DORKON", "YOUTH_M", 68, 21, "LEFT", 3,
            "Running the Isthmus for the Games. Race me in a battle!", "Winded!",
            "Nemea's track is the best in the world. Don't tell Olympia.", mandatory=False,
            tid="TRAINER_ICHOR_R14_DORKON")
    s.thickets += [("MeadowThicket", 64, 15, "0")]
    s.people += [("Herdsman", "SHEPHERD", 3, 10, "DOWN", "0")]
    gift(s, "Herdsman", "FLAG_ICHOR_R14_HERDSMAN_GIFT",
         "My sheep graze these hills, and the lion hasn't had one in three generations.\\p"
         "Still, I carry this when I go near the Tretos. Here, you take it.", "ITEM_LUM_BERRY",
         "Sheep don't fear the dark. Shepherds do.")
    s.gate("GullyRubble", "BREAKABLE_ROCK", 9, 22, "EventScript_RockSmash", "FLAG_ICHOR_R14_RUBBLE")
    s.gate("Drum", "PUSHABLE_BOULDER", DRUM[0], DRUM[1], "EventScript_StrengthBoulder")
    s.gate("CleftBoulder", "PUSHABLE_BOULDER", 11, 5, "EventScript_IchorGreatBoulder",
           "FLAG_ICHOR_R14_GREAT_BOULDER")
    item(s, "HYPER_POTION", 26, 6, "ITEM_R14_HEAL")
    item(s, "ULTRA_BALL", 70, 6, "ITEM_R14_BALL")
    item(s, "ETHER", 68, 17, "ITEM_R14_ETHER")
    item(s, "HARD_STONE", 3, 22, "ITEM_R14_GULLY")
    item(s, "PEARL", 55, 20, "ITEM_R14_ISLET")
    hidden(s, "HONEY", 60, 3, "HIDDEN_ITEM_R14_HONEY")
    hidden(s, "REVIVE", 30, 25, "HIDDEN_ITEM_R14_REVIVE")
    hidden(s, "SUPER_REPEL", 12, 3, "HIDDEN_ITEM_R14_REPEL")
    sign(s, "Sign0", 2, 15, "Route 14, the Tretos road.\\nWest: Nemea. East: through the Tretos to Emporion.")
    sign(s, "Sign1", 74, 12, "Route 14.\\nEast: Emporion's Nemea Gate. West: the Tretos and Nemea.")
    s.signs.append((23, 7, "ANY", "Herm"))
    s.scripts.append(f'''script {s.px}Herm {{
    goto(EventScript_IchorGreatHerm)
}}''')
    sign(s, "Cleft", 11, 2, "A stele of the lion hunters. Their names run down it, then stop.")
    return s


# ---------------------------------------------------------------------------
# The Tretos (36x20): Route 14's cave
# ---------------------------------------------------------------------------
WEBS = {"Web": (14, 3), "Thornweb": (22, 15)}        # web_1 on (x, y) and (x, y + 1)
WEB_FLAG = {"Web": "FLAG_ICHOR_HIDE_TRETOS_WEB", "Thornweb": "FLAG_ICHOR_HIDE_TRETOS_THORNWEB"}
BRAZIER = (17, 4)
BRAZIER_FLAG = "FLAG_ICHOR_BRAZIERS_START + 0x2E"


def plan_tretos():
    W, H = 36, 20
    grid = [["#"] * W for _ in range(H)]

    def r(x0, y0, x1, y1, ch="."):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                grid[y][x] = ch
    r(0, 8, 3, 10, ",")                       # daylight at the west mouth
    r(2, 7, 8, 11)                            # the west hall
    r(9, 9, 12, 9)                            # the neck, shut by rubble
    r(13, 6, 24, 14)                          # the chamber
    r(13, 5, 15, 5)
    r(16, 6, 21, 6)
    r(15, 9, 22, 12, "~")                     # the pool
    r(18, 10, 19, 11)                         # its islet
    r(14, 3, 14, 4)                           # the cobweb's neck
    r(12, 1, 16, 2)                           # the bone room
    r(22, 15, 22, 16)                         # the thornweb's neck
    r(18, 17, 27, 18)                         # the deep room
    r(25, 9, 33, 10)                          # the east passage
    r(32, 8, 35, 10, ",")                     # daylight at the east mouth
    r(29, 4, 29, 8)                           # the boulder tunnel (later)
    r(27, 2, 31, 3)
    r(24, 13, 26, 14)
    return grid


def build_tretos():
    import cave_dark_kit as kit
    cat = json.loads((ROOT / "data/tilesets/secondary/cave_dark/catalog.json").read_text())
    piece = {p["key"]: p["ids"] for p in cat["pieces"]}
    grid = plan_tretos()
    H, W = len(grid), len(grid[0])
    ids = kit.autotile(["".join(r) for r in grid], cat)
    cells = np.zeros((H, W), np.uint16)
    solid = np.array([[grid[y][x] == "#" for x in range(W)] for y in range(H)])
    water = np.array([[grid[y][x] == "~" for x in range(W)] for y in range(H)])
    mt = np.array(ids, np.int32)

    def put(key, x, y, block=True):
        for j, row in enumerate(piece[key]):
            for i, mid in enumerate(row):
                mt[y + j, x + i] = mid
                solid[y + j, x + i] = block
    # the mouths: daylight and the arrow-warp cells at the edges
    put("daylight_w", 0, 9, False)
    put("daylight_e", 34, 9, False)
    put("brazier_cold", BRAZIER[0], BRAZIER[1])
    for name, (x, y) in WEBS.items():
        put("web_1", x, y, False)             # the objects block it until it burns
    put("bones", 15, 2)
    put("seep", 2, 6)
    put("stele", 30, 2)
    put("stalagmite", 7, 7)
    put("stalagmites", 23, 7)
    put("pebbles", 5, 10, False)
    put("rock_pile", 13, 13)
    put("column", 26, 2)
    put("boulder", 20, 7)
    put("rock_pile", 28, 10)
    put("ledge_east", 31, 10)                 # a step down toward the east mouth
    for y in range(H):
        for x in range(W):
            m = int(mt[y, x]) & 0x3FF
            if water[y, x]:
                cells[y, x] = m | (1 << 12)
            elif solid[y, x]:
                cells[y, x] = m | (1 << 10)
            else:
                cells[y, x] = m | (3 << 12)
    lay = ROOT / "data/layouts" / TRETOS
    cells.astype("<u2").tofile(lay / "map.bin")
    rock = cat["kit"]["T|..."]
    np.full(4, rock | (1 << 10), np.uint16).astype("<u2").tofile(lay / "border.bin")
    data = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    for l in data["layouts"]:
        if l.get("id") == "LAYOUT_ROUTE14_TRETOS":
            l.update(width=W, height=H, primary_tileset="gTileset_Aethos", secondary_tileset="gTileset_CaveDark")
    (ROOT / "data/layouts/layouts.json").write_text(json.dumps(data, indent=2) + "\n")
    return cells, solid, water, piece


def spec_tretos(piece):
    s = Spec(TRETOS, "MAP_ROUTE14_TRETOS", "TRETOS")
    s.connections = []
    s.warps = [dict(x=0, y=9, elevation=0, dest_map="MAP_ROUTE14_NEMEA_ROAD", dest_warp_id="0"),
               dict(x=35, y=9, elevation=0, dest_map="MAP_ROUTE14_NEMEA_ROAD", dest_warp_id="1")]
    trainer(s, "LYSANDRA", "ACOLYTE_F", 23, 8, "LEFT", 3,
            "Hecate keeps the roads under the hills. I keep her lamps lit.", "Your light's brighter.",
            "Light the old brazier. The Tretos stays bright for whoever comes after.",
            mandatory=False, tid="TRAINER_ICHOR_TRETOS_LYSANDRA")
    s.gate("Rubble", "BREAKABLE_ROCK", 10, 9, "EventScript_RockSmash", "FLAG_ICHOR_TRETOS_RUBBLE")
    s.gate("GreatBoulder", "PUSHABLE_BOULDER", 29, 8, "EventScript_IchorGreatBoulder",
           "FLAG_ICHOR_TRETOS_GREAT_BOULDER")
    for name, (x, y) in WEBS.items():
        for j in range(2):
            s.gate(f"{name}{j + 1}", "CUTTABLE_TREE", x, y + j, f"{s.px}{name}", WEB_FLAG[name], invisible=True)
    item(s, "HYPER_POTION", 4, 8, "ITEM_TRETOS_HEAL")
    item(s, "DUSK_BALL", 13, 1, "ITEM_TRETOS_BALL")
    item(s, "BIG_PEARL", 19, 10, "ITEM_TRETOS_POOL")
    item(s, "PROTEIN", 26, 18, "ITEM_TRETOS_DEEP")
    hidden(s, "ESCAPE_ROPE", 15, 2, "HIDDEN_ITEM_TRETOS_BONES")
    hidden(s, "HEART_SCALE", 2, 7, "HIDDEN_ITEM_TRETOS_SEEP")
    s.signs += [(BRAZIER[0], BRAZIER[1] + 1, "ANY", "Brazier"), (BRAZIER[0] + 1, BRAZIER[1] + 1, "ANY", "Brazier")]
    sign(s, "Stele", 30, 2, "Claw marks, each as long as an arm, run along the wall and away north.\\p"
         "Toward Nemea. Toward the den.")
    lit = piece["brazier_lit"]
    torn = piece["torn_1"]
    web = piece["web_1"]
    bx, by = BRAZIER
    s.scripts += [
        f'''script {s.px}Brazier {{
    setvar(VAR_0x8004, {BRAZIER_FLAG})
    setvar(VAR_0x8005, TRUE)
    call(EventScript_IchorBrazier)
    if (var(VAR_RESULT) == TRUE) {{
        call({s.px}Lit)
        special(DrawWholeMapView)
    }}
    releaseall
}}''',
        f'''script {s.px}Lit {{
    setmetatile({bx}, {by}, 0x{lit[0][0]:03X}, TRUE)
    setmetatile({bx + 1}, {by}, 0x{lit[0][1]:03X}, TRUE)
    setmetatile({bx}, {by + 1}, 0x{lit[1][0]:03X}, TRUE)
    setmetatile({bx + 1}, {by + 1}, 0x{lit[1][1]:03X}, TRUE)
    return
}}''',
        f'''script {s.px}Web {{
    setvar(VAR_TEMP_9, 0)
    goto(EventScript_IchorCobweb)
}}''',
        f'''script {s.px}Thornweb {{
    setvar(VAR_TEMP_9, 0)
    goto(EventScript_IchorThornweb)
}}''',
        f'''script {s.px}RedrawWebs {{
    setvar(VAR_TEMP_9, 1)
    call({s.px}DrawWebs)
    special(DrawWholeMapView)
    end
}}''',
        f'''script {s.px}DrawWebs {{
''' + "".join(f'''    if (flag({WEB_FLAG[n]})) {{
        setmetatile({x}, {y}, 0x{torn[0][0]:03X}, FALSE)
        setmetatile({x}, {y + 1}, 0x{torn[1][0]:03X}, FALSE)
    }} else {{
        setmetatile({x}, {y}, 0x{web[0][0]:03X}, FALSE)
        setmetatile({x}, {y + 1}, 0x{web[1][0]:03X}, FALSE)
    }}
''' for n, (x, y) in WEBS.items()) + '''    return
}''',
    ]
    mapscripts = f'''mapscripts {TRETOS}_MapScripts {{
    MAP_SCRIPT_ON_LOAD {{
        if (flag({BRAZIER_FLAG})) {{
            call({s.px}Lit)
        }}
        call({s.px}DrawWebs)
    }}
    MAP_SCRIPT_ON_TRANSITION {{
        if (flag({BRAZIER_FLAG})) {{
            setflashlevel(0)
        }}
    }}
    MAP_SCRIPT_ON_FRAME_TABLE [
        VAR_TEMP_9, 0: {s.px}RedrawWebs
    ]
}}'''
    return s, mapscripts


# ---------------------------------------------------------------------------
# Nemea's rooms: events and scripts (their layouts are nemea_rooms.py's)
# ---------------------------------------------------------------------------
def rooms():
    for name, door, mat, people, bgs, scripts in (
        (PALAESTRA_MAP, 0, [(7, 10), (8, 10)],
         [("KLEITOMACHOS", "ELDER_M", 8, 3, "DOWN", True), ("Tisandros", "HOPLITE", 6, 5, "RIGHT", False),
          ("Chionis", "YOUTH_F", 11, 9, "LEFT", False)],
         [(2, 1, "NORTH", "Course"), (10, 1, "NORTH", "Oil"), (1, 9, "WEST", "Basin")],
         [f'''script {PALAESTRA_MAP}_EventScript_KLEITOMACHOS {{
    trainerbattle_single(TRAINER_ICHOR_NEMEA_KLEITOMACHOS,
        format("I trained wrestlers for six Games. Show me your hold."),
        format("Herakles would've nodded at that."))
    lock
    faceplayer
    if (!flag(FLAG_ICHOR_NEMEA_PALAESTRA_GIFT)) {{
        msgbox(format("Herakles strangled the lion. No club, no arrows. Just grip.\\p"
                      "Wear this. It's what we give the ones who hold on."))
        giveitem(ITEM_MUSCLE_BAND)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_NEMEA_PALAESTRA_GIFT)
        }}
        release
        end
    }}
    msgbox(format("Sand on your hands. Oil on your skin. Then grip."))
    release
}}''',
          f'''script {PALAESTRA_MAP}_EventScript_Tisandros {{
    lock
    faceplayer
    msgbox(format("Pankration. Anything goes, except biting and gouging.\\p"
                  "The lion didn't know the rules. Herakles won anyway."))
    release
}}''',
          f'''script {PALAESTRA_MAP}_EventScript_Chionis {{
    lock
    faceplayer
    msgbox(format("The track's in the valley, past the farm. One stade, there and back.\\p"
                  "Someone with wings on their feet could do it before the judges blink."))
    release
}}''',
          f'''script {PALAESTRA_MAP}_EventScript_Course {{
    msgbox(format("The stadium course, scratched into the plaster.\\pA tunnel at one end, a turning post at each."), MSGBOX_SIGN)
    end
}}''',
          f'''script {PALAESTRA_MAP}_EventScript_Oil {{
    msgbox(format("Jars of olive oil for the athletes' skin. Then the sand goes on."), MSGBOX_SIGN)
    end
}}''',
          f'''script {PALAESTRA_MAP}_EventScript_Basin {{
    msgbox(format("A washbasin. The water's gray with sand."), MSGBOX_SIGN)
    end
}}''']),
        (COTTAGE_MAP, 1, [(5, 7), (6, 7)],
         [("Molorchos", "ELDER_M", 5, 3, "DOWN", False)],
         [(10, 2, "NORTH", "Jar"), (1, 3, "NORTH", "Hearth")],
         [f'''script {COTTAGE_MAP}_EventScript_Molorchos {{
    lock
    faceplayer
    if (flag(FLAG_ICHOR_NEMEA_HONEY_GIVEN)) {{
        msgbox(format("A hero slept on that floor once. Ate my bread, went up to the den.\\p"
                      "I waited thirty days for him. I'll wait for you too, if you go up there."))
        release
        end
    }}
    msgbox(format("I'm Molorchos. A day laborer, nothing more.\\p"
                  "I owe Zeus a cake for the Games, and I've no honey for it.\\p"
                  "The highland hives have plenty. Could you spare me one Honey?"))
    checkitem(ITEM_HONEY, 1)
    if (var(VAR_RESULT) == FALSE) {{
        msgbox(format("No? Then the cake will be dry. Zeus has eaten worse."))
        release
        end
    }}
    msgbox(format("Give Molorchos one Honey?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == NO) {{
        release
        end
    }}
    removeitem(ITEM_HONEY, 1)
    msgbox(format("Bless you. Here, for your trouble.\\p"
                  "A hero left it on my bench years ago. A strip of the lion's own hide."))
    giveitem(ITEM_SILK_SCARF)
    if (var(VAR_RESULT) == TRUE) {{
        setflag(FLAG_ICHOR_NEMEA_HONEY_GIVEN)
    }} else {{
        additem(ITEM_HONEY, 1)
    }}
    release
}}''',
          f'''script {COTTAGE_MAP}_EventScript_Jar {{
    msgbox(format("A jar with a little honey scraped from its sides."), MSGBOX_SIGN)
    end
}}''',
          f'''script {COTTAGE_MAP}_EventScript_Hearth {{
    msgbox(format("A small fire, carefully fed."), MSGBOX_SIGN)
    end
}}''']),
    ):
        path = ROOT / f"data/maps/{name}/map.json"
        m = json.loads(path.read_text())
        m.update(music="MUS_ICHOR_AGORA" if name == PALAESTRA_MAP else "MUS_ICHOR_ROAD",
                 map_type="MAP_TYPE_INDOOR", weather="WEATHER_NONE", show_map_name=False, connections=None,
                 coord_events=[])
        lid = "LOCALID_" + const(name) + "_"
        m["object_events"] = [{
            "local_id": lid + n.upper(), "graphics_id": GFX + gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": f"MOVEMENT_TYPE_FACE_{f}", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if t else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0", "script": f"{name}_EventScript_{n}", "flag": "0"}
            for n, gfx, x, y, f, t in people]
        m["warp_events"] = [dict(x=x, y=y, elevation=0, dest_map="MAP_NEMEA", dest_warp_id=str(door))
                            for x, y in mat]
        m["bg_events"] = [dict(type="sign", x=x, y=y, elevation=0,
                               player_facing_dir=f"BG_EVENT_PLAYER_FACING_{f}", script=f"{name}_EventScript_{n}")
                          for x, y, f, n in bgs]
        path.write_text(json.dumps(m, indent=2) + "\n")
        pory = ROOT / f"data/maps/{name}/scripts.pory"
        pory.write_text("\n\n".join([f"mapscripts {name}_MapScripts {{}}",
                                     "// Generated by tools/ichor/maps/nemea.py; edit the builder, not this file."]
                                    + scripts) + "\n")


# ---------------------------------------------------------------------------
# Layout, checks and renders for the outdoor maps
# ---------------------------------------------------------------------------
def write_layout(g, border_key="pine_tall"):
    lay_dir = ROOT / f"data/layouts/{g.name}"
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mt[y, x]) & 0x3FF
            if g.water[y, x]:
                out[y, x] = mid | (1 << 12)
            elif g.solid[y, x]:
                out[y, x] = mid | (1 << 10)
            else:
                out[y, x] = mid | (3 << 12)
    out.astype("<u2").tofile(lay_dir / "map.bin")
    s = g.cat[border_key]
    border = np.array([s["ids"][1][0], s["ids"][1][1], s["ids"][2][0], s["ids"][2][1]], np.uint16) | (1 << 10)
    if g.cols:
        border = np.array([R5.STONE_PINE[0][0], R5.STONE_PINE[0][1], R5.STONE_PINE[1][0],
                           R5.STONE_PINE[1][1]], np.uint16) | (1 << 10)
    border.astype("<u2").tofile(lay_dir / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    lid = "LAYOUT_" + R5.re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", g.name).upper()
    for l in data["layouts"]:
        if l.get("id") == lid:
            l.update(width=g.w, height=g.h, primary_tileset="gTileset_Aethos", secondary_tileset="gTileset_Skiron")
    path.write_text(json.dumps(data, indent=2) + "\n")
    return out


def edge_cells(g, side, rows=None):
    if side == "left":
        return [(0, y) for y in (rows or range(g.h)) if not g.solid[y, 0] and not g.water[y, 0]]
    return [(g.w - 1, y) for y in (rows or range(g.h)) if not g.solid[y, g.w - 1] and not g.water[y, g.w - 1]]


def check(g, spec, pairs, gates_open=()):
    """pairs: [((label, cells), (label, cells))], the ends a walker joins.
    Returns problems, mandatory trainers, forced grass for each pair."""
    problems = []
    objs = spec.objects()
    water = {(x, y) for y in range(g.h) for x in range(g.w) if g.water[y, x]}
    gates = {(o["x"], o["y"]) for o in objs if o["graphics_id"].endswith(("CUTTABLE_TREE", "BREAKABLE_ROCK",
                                                                          "PUSHABLE_BOULDER"))}
    people = {(o["x"], o["y"]) for o in objs} - gates
    wall = frozenset(people | water)
    for o in objs:
        if g.solid[o["y"], o["x"]]:
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} on a solid cell")
    open_gates = frozenset(gates - set(gates_open))
    for (la, a), (lb, b) in pairs:
        if not set(b) & K.reach(g, a, frozenset(wall | open_gates)):
            problems.append(f"can't walk from {la} to {lb}")
    starts = [c for pair in pairs for _, cells in pair for c in cells]
    allr = K.reach(g, starts, wall)
    for o in objs:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in allr for dx, dy in K.FACE.values()):
            if "PUSHABLE" not in o["graphics_id"] and o["graphics_id"] != "OBJ_EVENT_GFX_ITEM_BALL":
                problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} at ({x},{y}) can't be reached")
    for b in spec.bgs():
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and not g.solid[y, x]:
            problems.append(f"sign {b['script']} at ({x},{y}) is on walkable ground")
        spots = [(x, y + 1)] if b.get("player_facing_dir", "").endswith("NORTH") else \
            [(x + dx, y + dy) for dx, dy in K.FACE.values()]
        if b["type"] == "sign" and not any(p in allr for p in spots):
            problems.append(f"{b.get('script', b.get('item'))} at ({x},{y}) can't be read")
    for c in sorted(allr):
        if not set(starts) & K.reach(g, [c], wall):
            problems.append(f"trap at {c}")
            break
    forced = []
    for (la, a), (lb, b) in pairs:
        f1 = K.grass_cost(g, a, b, frozenset(wall | open_gates))
        f2 = K.grass_cost(g, b, a, frozenset(wall | open_gates))
        forced.append((la, lb, f1, f2))
    mand = []
    for t in spec.trainers:
        cells = set(K.sight(g, t))
        cut = any(not set(b) & K.reach(g, a, frozenset(wall | open_gates | cells))
                  for (_, a), (_, b) in pairs)
        if t["mandatory"] and not cut:
            problems.append(f"{t['name']}'s sight can be walked round")
        if cut:
            mand.append(t["name"])
        if len(cells) < t["sight"]:
            problems.append(f"{t['name']} sees {len(cells)} of {t['sight']} cells (blocked)")
    return problems, mand, forced


def walk_text(g, spec):
    objs = {(o["x"], o["y"]): o for o in spec.objects()}
    sights = {c for t in spec.trainers for c in K.sight(g, t)}
    rows = ["    " + "".join(str(x % 10) for x in range(g.w))]
    for y in range(g.h):
        line = ""
        for x in range(g.w):
            o = objs.get((x, y))
            b = K.behavior(int(g.mt[y, x]))
            if o is not None:
                gfx = o["graphics_id"]
                line += "T" if o["trainer_type"] != "TRAINER_TYPE_NONE" else \
                        "*" if gfx.endswith("CUTTABLE_TREE") else "%" if gfx.endswith("BREAKABLE_ROCK") else \
                        "D" if gfx.endswith("PUSHABLE_BOULDER") else "o" if gfx.endswith("ITEM_BALL") else "@"
            elif g.water[y, x]:
                line += "~"
            elif b.startswith("MB_JUMP"):
                line += {"MB_JUMP_SOUTH": "v", "MB_JUMP_WEST": "<", "MB_JUMP_EAST": ">"}.get(b, "j")
            elif g.solid[y, x]:
                line += "#"
            elif (x, y) in sights:
                line += "!"
            elif b == "MB_TALL_GRASS":
                line += ","
            else:
                line += "."
        rows.append(f"{y:3d} {line}")
    return "\n".join(rows)


def render(name, w, h, blocks, objs, out_dir, stem, secondary="gTileset_Skiron", views=(), walk=None):
    from PIL import Image, ImageDraw
    import render_map as RM
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset("gTileset_Aethos", syms)),
                    RM.Tileset(RM.resolve_tileset(secondary, syms)))
    flat = RM.render_blocks(r, blocks.reshape(-1), w).convert("RGBA")
    for o in objs:
        gfx = o["graphics_id"]
        if o["movement_type"] == "MOVEMENT_TYPE_INVISIBLE":
            continue
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE" in o["movement_type"] else "DOWN"
        try:
            if gfx == "OBJ_EVENT_GFX_ITEM_BALL":
                spr = Image.open(ROOT / "graphics/object_events/pics/misc/ichor_item_jar.png").convert("RGBA")
                spr = spr.crop((0, 0, 16, spr.height))
                fw, fh = 16, spr.height
            else:
                spr, fw, fh = R5.sprite(gfx, facing)
        except (FileNotFoundError, KeyError, OSError):
            continue
        flat.paste(spr, (o["x"] * 16 + 8 - fw // 2, o["y"] * 16 + 16 - fh), spr)
    flat.convert("RGB").resize((w * 32, h * 32), Image.NEAREST).save(out_dir / f"{stem}.png")
    if walk is not None:
        g, spec = walk
        im = flat.resize((w * 32, h * 32), Image.NEAREST)
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d, c = ImageDraw.Draw(ov), 32
        for y in range(h):
            for x in range(w):
                b = K.behavior(int(g.mt[y, x]))
                box = [x * c, y * c, x * c + c - 1, y * c + c - 1]
                if b.startswith("MB_JUMP"):
                    d.rectangle(box, fill=(0, 120, 255, 90))
                elif g.water[y, x]:
                    d.rectangle(box, fill=(0, 0, 255, 50))
                elif g.solid[y, x]:
                    d.rectangle(box, fill=(255, 0, 0, 60))
                elif b == "MB_TALL_GRASS":
                    d.rectangle(box, fill=(0, 255, 0, 45))
        for t in spec.trainers:
            col = (255, 160, 0, 255) if t["mandatory"] else (255, 255, 120, 255)
            for (sx, sy) in K.sight(g, t):
                d.rectangle([sx * c + 6, sy * c + 6, sx * c + c - 7, sy * c + c - 7], outline=col, width=3)
        Image.alpha_composite(im, ov).convert("RGB").save(out_dir / f"{stem}_walk.png")
    if views:
        shots = []
        for vname, px, py in views:
            x0 = min(max(px - 7, 0), w - 15) * 16
            y0 = min(max(py - 5, 0), h - 10) * 16
            shots.append((vname, flat.crop((x0, y0, x0 + 240, y0 + 160)).convert("RGB")))
        cols = 3
        rows_n = (len(shots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 248 + 8, rows_n * 178 + 8), (24, 24, 32))
        sd = ImageDraw.Draw(sheet)
        for i, (vname, v) in enumerate(shots):
            x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
            sheet.paste(v, (x, y + 10))
            sd.text((x, y - 2), vname, fill=(230, 230, 200))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / f"{stem}_views.png")


VIEWS = {
    R13: [("1 Arkadia's road", 7, 10), ("2 the oak wood", 19, 11), ("3 the clearing, the herm", 27, 9),
          ("4 the high meadow", 36, 5), ("5 the stair, Lykon", 33, 16), ("6 the ford, Kallias", 49, 19),
          ("7 the lower wood", 20, 21), ("8 the glade", 50, 4)],
    NEMEA: [("1 the west road", 7, 14), ("2 Zeus's temple", 20, 7), ("3 the den", 37, 9),
            ("4 the cottage, the vines", 7, 23), ("5 the stadium", 15, 29), ("6 the outcamp", 34, 23),
            ("7 the river pool", 35, 31)],
    R14: [("1 from Nemea", 7, 17), ("2 the gorge stair", 15, 12), ("3 the gorge, the mouth", 24, 7),
          ("4 the stream bed", 18, 22), ("5 the ridge top", 40, 4), ("6 the east mouth, the ford", 52, 11),
          ("7 the knoll", 63, 7), ("8 the south meadow", 64, 20), ("9 the Isthmus plain", 73, 13)],
}


def build(plan, props, specf, notch=True):
    g = plan()
    if notch:
        K.notch(g)
        for y in range(g.h):                  # no bays cut into the map's own edge
            for x in range(g.w):
                if (x in (0, g.w - 1) or y in (0, g.h - 1)) and g.g[y][x] == "," and \
                        not any(g.at(x + dx, y + dy) in ("p", ".") and g.at(x + dx, y + dy) is not None
                                and (x + dx in (0, g.w - 1) or y + dy in (0, g.h - 1))
                                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                    g.g[y][x] = "#"
    K.bands(g)
    massif(g)
    terrain(g)
    props(g)
    seam_columns(g)
    K.trees(g)
    K.olives(g)
    K.ground(g)
    seam_columns(g)
    check_seams(g)
    spec = specf()
    blocks = write_layout(g)
    return g, spec, blocks


# ---------------------------------------------------------------------------
# Wild tables and the new trainers' parties
# ---------------------------------------------------------------------------
LAND = {
    R13: (30, 32, {
        "Morning": ["KLADOE", "GALENYON", "KERAZAP", "ELAPLING", "CAIRNOLITH", "MELISSEER",
                    "KLADOE", "GALENYON", "NEMELEON", "KERAZAP", "ELAPLING", "NEMELEON"],
        "Day": ["GALENYON", "KLADOE", "KERAZAP", "MELISSEER", "CAIRNOLITH", "ELAPLING",
                "GALENYON", "KLADOE", "NEMELEON", "MELISSEER", "CAIRNOLITH", "NEMELEON"],
        "Evening": ["KLADOE", "ELAPLING", "KERAZAP", "GALENYON", "HARPELLE", "CAIRNOLITH",
                    "LYKANAX", "KLADOE", "NEMELEON", "HARPELLE", "PROSOMIME", "NEMELEON"],
        "Night": ["LYKANAX", "HARPELLE", "PROSOMIME", "CAIRNOLITH", "KERAZAP", "ELAPLING",
                  "LYKANAX", "HARPELLE", "NEMELEON", "PROSOMIME", "LYKANAX", "NEMELEON"],
    }),
    NEMEA: (31, 33, {
        "Morning": ["NEMELEON", "MELISSEER", "KLADOE", "GALENYON", "ELAPLING", "KERAZAP",
                    "NEMELEON", "MELISSEER", "HOPLOMEX", "KLADOE", "GALENYON", "HOPLOMEX"],
        "Day": ["MELISSEER", "NEMELEON", "GALENYON", "KLADOE", "KERAZAP", "ELAPLING",
                "MELISSEER", "NEMELEON", "HOPLOMEX", "GALENYON", "KLADOE", "HOPLOMEX"],
        "Evening": ["NEMELEON", "HARPELLE", "MELISSEER", "KLADOE", "LYKANAX", "ELAPLING",
                    "NEMELEON", "HARPELLE", "PROSOMIME", "MELISSEER", "LYKANAX", "NEMELEON"],
        "Night": ["NEMELEON", "LYKANAX", "HARPELLE", "PROSOMIME", "NEMELEON", "LYKANAX",
                  "HARPELLE", "PROSOMIME", "NEMELEON", "LYKANAX", "HARPELLE", "NEMELEON"],
    }),
    R14: (31, 33, {
        "Morning": ["CAIRNOLITH", "HOPLOMEX", "KERAZAP", "GALENYON", "MELISSEER", "KLADOE",
                    "CAIRNOLITH", "HOPLOMEX", "NEMELEON", "KERAZAP", "GALENYON", "NEMELEON"],
        "Day": ["HOPLOMEX", "CAIRNOLITH", "GALENYON", "KERAZAP", "MELISSEER", "KLADOE",
                "HOPLOMEX", "CAIRNOLITH", "NEMELEON", "GALENYON", "MELISSEER", "NEMELEON"],
        "Evening": ["CAIRNOLITH", "HOPLOMEX", "HARPELLE", "KERAZAP", "LYKANAX", "MELISSEER",
                    "CAIRNOLITH", "PROSOMIME", "NEMELEON", "HARPELLE", "LYKANAX", "NEMELEON"],
        "Night": ["LYKANAX", "HARPELLE", "CAIRNOLITH", "PROSOMIME", "HOPLOMEX", "KERAZAP",
                  "LYKANAX", "HARPELLE", "NEMELEON", "PROSOMIME", "CAIRNOLITH", "NEMELEON"],
    }),
    TRETOS: (32, 34, {
        "Morning": ["CAIRNOLITH", "KERAZAP", "PROSOMIME", "HARPELLE", "LYKANAX", "CAIRNOLITH",
                    "KERAZAP", "PROSOMIME", "HOPLOMEX", "HARPELLE", "NEMELEON", "NEMELEON"],
        "Night": ["PROSOMIME", "LYKANAX", "CAIRNOLITH", "HARPELLE", "KERAZAP", "PROSOMIME",
                  "LYKANAX", "CAIRNOLITH", "HARPELLE", "HOPLOMEX", "NEMELEON", "NEMELEON"],
    }),
}
WATER = {R13: water_tables.pond(31), NEMEA: water_tables.pond(32), R14: water_tables.pond(32),
         TRETOS: water_tables.pond(33)}
ROCK = {R13: ("CAIRNOLITH", "KERAZAP", "CAIRNOLITH", "KERAZAP", "CAIRNOLITH"),
        R14: ("CAIRNOLITH", "KERAZAP", "CAIRNOLITH", "HOPLOMEX", "CAIRNOLITH"),
        TRETOS: ("CAIRNOLITH", "KERAZAP", "CAIRNOLITH", "HOPLOMEX", "KERAZAP")}
MAP_IDS = {R13: "MAP_ROUTE13_HIGHLAND_ROAD", NEMEA: "MAP_NEMEA", R14: "MAP_ROUTE14_NEMEA_ROAD",
           TRETOS: "MAP_ROUTE14_TRETOS"}


def write_wild():
    path = ROOT / "src/data/wild_encounters.json"
    data = json.loads(path.read_text())
    group = next(gr for gr in data["wild_encounter_groups"] if gr.get("for_maps"))
    ids = set(MAP_IDS.values())
    at = next((i for i, e in enumerate(group["encounters"]) if e.get("map") in ids), len(group["encounters"]))
    before = [e for e in group["encounters"][:at] if e.get("map") not in ids]
    after = [e for e in group["encounters"][at:] if e.get("map") not in ids]
    new = []
    for name, (lo, hi, tables) in LAND.items():
        for time, species in tables.items():
            mons = []
            for i, sp in enumerate(species):
                mons.append({"min_level": lo if i % 3 else lo + 1, "max_level": hi, "species": "SPECIES_" + sp})
            e = {"map": MAP_IDS[name], "base_label": f"g{name}_{time}",
                 "land_mons": {"encounter_rate": 10 if name == TRETOS else 25, "mons": mons}}
            if time == "Morning":
                e.update(json.loads(json.dumps(WATER[name])))
                if name in ROCK:
                    e["rock_smash_mons"] = {"encounter_rate": 20, "mons": [
                        {"min_level": lo, "max_level": hi, "species": "SPECIES_" + sp} for sp in ROCK[name]]}
            new.append(e)
    group["encounters"] = before + new + after
    path.write_text(json.dumps(data, indent=2) + "\n")


NEW_TEAMS = [
    ("TRAINER_ICHOR_R14_ANTIKLES", "ANTIKLES", "Goatherd", "Goatherd", "Male", "Hiker",
     [("Cairnolith", 35), ("Kerazap", 35), ("Hoplomex", 36)]),
    ("TRAINER_ICHOR_R14_DORKON", "DORKON", "Runner", "Runner", "Male", "Cool",
     [("Galenyon", 35), ("Elapling", 36)]),
    ("TRAINER_ICHOR_TRETOS_LYSANDRA", "LYSANDRA", "Acolyte", "Acolyte F", "Female", "Female",
     [("Prosomime", 35), ("Lykanax", 35), ("Harpelle", 36)]),
    ("TRAINER_ICHOR_NEMEA_KLEITOMACHOS", "KLEITOS", "Hoplite", "Hoplite", "Male", "Male",
     [("Hoplomex", 36), ("Cairnolith", 36), ("Nemeleon", 37)]),
]


def write_teams():
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Nemea rebuild teams (tools/ichor/maps/nemea.py). */", "/* End Nemea rebuild teams. */"
    text = path.read_text()
    block = start + "\n"
    for tid, name, cls, pic, gender, music, mons in NEW_TEAMS:
        block += f"\n=== {tid} ===\nName: {name}\nClass: {cls}\nPic: {pic}\nGender: {gender}\nMusic: {music}\n"
        block += "AI: Basic Trainer\n"
        for sp, lv in mons:
            block += f"\n{sp}\nLevel: {lv}\nIVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    block += "\n" + end
    if start in text:
        a = text.index(start)
        b = text.index(end) + len(end)
        text = text[:a] + block + text[b:]
    else:
        anchor = "/* End Nemea return teams. */"
        a = text.index(anchor) + len(anchor)
        text = text[:a] + "\n\n" + block + text[a:]
    path.write_text(text)


def heal_locations(herm13, herm14, healer):
    path = ROOT / "src/data/heal_locations.json"
    data = json.loads(path.read_text())
    for h in data["heal_locations"]:
        if h["id"] == "HEAL_LOCATION_NEMEA":
            h.update(x=healer[0], y=healer[1] + 1, respawn_x=healer[0], respawn_y=healer[1] + 1)
        elif h["id"] == "HEAL_LOCATION_HERM_AETHOS_ROUTE_13":
            h.update(x=herm13[0], y=herm13[1] + 1)
        elif h["id"] == "HEAL_LOCATION_HERM_AETHOS_ROUTE_14":
            h.update(x=herm14[0], y=herm14[1] + 1)
    path.write_text(json.dumps(data, indent=2) + "\n")


def emporion_connection():
    path = ROOT / "data/maps/EmporionCity/map.json"
    m = json.loads(path.read_text())
    for c in m["connections"]:
        if c["map"] == "MAP_ROUTE14_NEMEA_ROAD":
            c["offset"] = -EMPORION_OFFSET
    path.write_text(json.dumps(m, indent=2) + "\n")


# ---------------------------------------------------------------------------
# The old placeholder road builder, still used by astyra.py for Routes 15-16
# ---------------------------------------------------------------------------
def roads(records=ROADS):
    links = {"R15": ("EleusaVillage", "Daphni", -14, 0),
             "R16": ("Daphni", "Astyra", 0, -22)}
    for name, tag, base, names in records:
        if tag in ("R13", "R14"):
            continue        # built above, by plan_r13 / plan_r14
        m = Map(name, 48, 24)
        m.json["music"] = "MUS_ICHOR_ROAD"
        if tag == "R16":
            m.rect(0, 0, 47, 23, 0x0E1, True)
        if tag == "R15":
            m.rect(0, 0, 47, 23, 0x170, True)
        m.rect(0, 10, 47, 13, 0x1D9)
        for x0, x1 in ((4, 11), (23, 31), (39, 43)):
            m.rect(x0, 4, x1, 19, 0x001)
            m.rect(x0, 5, x1 - 1, 7, 0x00D)
            m.rect(x0 + 1, 16, x1, 18, 0x00D)
        for x in (16, 34):
            m.rect(x, 10, x + 3, 13, 0x00D)
        left, right, left_offset, right_offset = links[tag]
        m.connection("left", left, left_offset)
        m.connection("right", right, right_offset)
        scripts = [f"mapscripts {name}_MapScripts {{}}"]
        positions = [(14, 10, "DOWN", 3), (6, 6, "RIGHT", 1), (26, 6, "DOWN", 1),
                     (32, 10, "DOWN", 3), (29, 18, "LEFT", 1), (41, 18, "UP", 1)]
        for i, (trainer_name, (x, y, facing, sight)) in enumerate(zip(names, positions)):
            m.person(trainer_name, x, y, gfx=("HOPLITE", "HARVESTER", "PILGRIM",
                                              "ACOLYTE_F", "SHEPHERD", "AUGUR")[i],
                     facing=facing, sight=sight)
            scripts.append(f'''script {m.prefix}{trainer_name} {{
    trainerbattle_single(TRAINER_ICHOR_{tag}_{trainer_name},
        format("The capital is close. Are you ready for its welcome?"),
        format("You kept your footing."))
    msgbox(format("Daphni's healer tends travelers on the capital road."), MSGBOX_AUTOCLOSE)
    end
}}''')
        for (x, y), suffix, it in zip(((4, 4), (23, 19), (42, 4)),
                                      ("HEAL", "BALL", "ETHER"), ("HYPER_POTION", "ULTRA_BALL", "ETHER")):
            e = obj("", x, y, "Common_EventScript_FindItem", flag=f"FLAG_ICHOR_ITEM_{tag}_{suffix}")
            e.pop("local_id")
            e.update(graphics_id="OBJ_EVENT_GFX_ITEM_BALL", trainer_sight_or_berry_tree_id="ITEM_" + it)
            m.json["object_events"].append(e)
        for (x, y), suffix, it in zip(((10, 5), (30, 18), (42, 19)),
                                      ("HONEY", "REVIVE", "REPEL"), ("HONEY", "REVIVE", "SUPER_REPEL")):
            m.json["bg_events"].append(dict(type="hidden_item", x=x, y=y, elevation=3,
                item="ITEM_" + it, flag=f"FLAG_ICHOR_HIDDEN_ITEM_{tag}_{suffix}",
                quantity=1, underfoot=False))
        directions = {"R15": "West: Eleusa. East: Daphni, past the salt lakes.",
                      "R16": "West: Daphni. East: Astyra, beneath the Akropolis."}[tag]
        for i, x in enumerate((2, 45)):
            m.sign("Sign" + str(i), x, 9)
            scripts.append(f'''script {m.prefix}Sign{i} {{
    msgbox(format("{directions}"), MSGBOX_SIGN)
    end
}}''')
        m.rect(26, 8, 28, 9, 0x001)
        m.sign("Herm", 27, 8, tile=0x01B)
        scripts.append(f'''script {m.prefix}Herm {{
    goto(EventScript_IchorGreatHerm)
}}''')
        (ROOT / f"data/maps/{name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")
        m.save()


def encounters_and_teams(records=ROADS, chapter="Nemea return"):
    """Placeholder wild tables and parties for a list of road records (astyra.py
    uses it for Routes 15-16). Routes 13 and 14's wild tables are write_wild()'s;
    their parties stay in the Nemea return block."""
    wild = read("src/data/wild_encounters.json")
    group = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    records = list(records)
    road_records = [r for r in records if r[1] not in ("R13", "R14")]
    ids = {"MAP_" + const(r[0]) for r in road_records}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in ids]
    for name, tag, level, _ in road_records:
        for time in ("Morning", "Day", "Evening", "Night"):
            species = ["KLADOE", "GALENYON", "CAIRNOLITH", "ELAPLING", "KERAZAP", "NEMELEON"]
            if tag in ("R15", "R16"):
                species[3:5] = ["THYRSIVY", "HOPLOMEX"]
            if tag == "R16":
                species[0] = "DAPHNYAD"
            if time == "Night":
                species[0:2] = ["LYKANAX", "HARPELLE"]
            group["encounters"].append(dict(map="MAP_" + const(name),
                base_label=f"g{name}_{time}", land_mons=dict(encounter_rate=15,
                    mons=[dict(min_level=level, max_level=level + 2,
                               species="SPECIES_" + species[i % 6]) for i in range(12)])))
    water_tables.apply(group["encounters"], {"MAP_ROUTE15_MYSTERY_ROAD"})
    write("src/data/wild_encounters.json", wild)
    path = ROOT / "src/data/trainers.party"
    start, end = f"/* {chapter} teams. */", f"/* End {chapter} teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    pairs = [("Galenyon", "Hoplomex"), ("Thyrsivy", "Elapling"),
             ("Cairnolith", "Kerazap"), ("Harpelle", "Prosomime"),
             ("Nemeleon", "Kladoe"), ("Lykanax", "Melisseer")]
    for _, tag, base, names in records:
        for i, name in enumerate(names):
            cls, pic = [("Hoplite", "Hoplite"), ("Harvester", "Harvester"),
                        ("Pilgrim", "Pilgrim"), ("Acolyte", "Acolyte F"),
                        ("Shepherd", "Shepherd"), ("Augur", "Augur")][i]
            text += f"\n=== TRAINER_ICHOR_{tag}_{name} ===\nName: {name}\nClass: {cls}\nPic: {pic}\n"
            text += ("Gender: Female\n" if i in (1, 3) else "Gender: Male\n")
            text += "Music: Male\nAI: Basic Trainer\n"
            for j, species in enumerate(pairs[i]):
                if tag in ("R15", "R16") and species == "Kladoe":
                    species = "Daphnyad"
                text += f"\n{species}\nLevel: {base + (2 if tag == 'R16' else 3) + i // 3 + j}\n"
                text += "IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    path.write_text(text + "\n" + end + after + ("" if after else "\n"))


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--stem-suffix", default="", help="added to each render's name (e.g. _pass1)")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--no-rooms", action="store_true", help="skip rebuilding domos for Nemea's rooms")
    args = ap.parse_args()
    if not K.CAT.exists():
        sys.exit(f"{K.CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    bad = 0
    g13, s13, b13 = build(plan_r13, props_r13, spec_r13)
    gn, sn, bn = build(plan_nemea, props_nemea, spec_nemea)
    g14, s14, b14 = build(plan_r14, props_r14, spec_r14)
    write_events(s13)
    nemea_scripts = '''mapscripts Nemea_MapScripts {
    MAP_SCRIPT_ON_TRANSITION {
        setrespawn(HEAL_LOCATION_NEMEA)
    }
}'''
    write_events(sn, kind="MAP_TYPE_TOWN", mapscripts=nemea_scripts)
    write_events(s14)
    cells, csolid, cwater, piece = build_tretos()
    st, tscripts = spec_tretos(piece)
    write_events(st, music="MUS_ICHOR_HOLLOW", kind="MAP_TYPE_UNDERGROUND", mapscripts=tscripts)
    tj = ROOT / f"data/maps/{TRETOS}/map.json"
    m = json.loads(tj.read_text())
    m.update(requires_flash=True, allow_cycling=False, allow_escaping=True, weather="WEATHER_NONE",
             show_map_name=True, connections=None)
    tj.write_text(json.dumps(m, indent=2) + "\n")
    rooms()
    if not args.no_rooms:
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/maps/nemea_rooms.py")], check=True, cwd=ROOT)
    write_wild()
    write_teams()
    heal_locations((25, 9), (23, 7), (12, 15))
    emporion_connection()

    w14, e14 = ("the west mouth", [(29, 8)]), ("the east mouth", [(49, 9)])
    results = [
        (g13, s13, b13, [(("Arkadia", edge_cells(g13, "left")), ("Nemea", edge_cells(g13, "right")))]),
        (gn, sn, bn, [(("Route 13", edge_cells(gn, "left")), ("Route 14", edge_cells(gn, "right")))]),
        (g14, s14, b14, [(("Nemea", edge_cells(g14, "left")), w14),
                         (e14, ("Emporion", edge_cells(g14, "right")))]),
    ]
    for g, spec, blocks, pairs in results:
        problems, mand, forced = check(g, spec, pairs)
        if args.walk:
            print(walk_text(g, spec))
        if args.render:
            stem = {R13: "route13", NEMEA: "nemea", R14: "route14"}[g.name] + args.stem_suffix
            render(g.name, g.w, g.h, blocks, spec.objects(), args.render, stem, views=VIEWS[g.name],
                   walk=(g, spec))
        for p in problems:
            print(f"PROBLEM {spec.name}: {p}")
        print(f"{spec.name}: {g.w}x{g.h}, forced grass {forced}, "
              f"{len(spec.trainers)} trainers, on the only road: {', '.join(mand) or 'none'}, "
              f"{len(problems)} problems")
        bad += len(problems)
    if args.render:
        render(TRETOS, cells.shape[1], cells.shape[0], cells, st.objects(), args.render,
               "tretos" + args.stem_suffix, secondary="gTileset_CaveDark")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
