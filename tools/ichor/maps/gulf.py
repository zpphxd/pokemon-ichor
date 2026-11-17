#!/usr/bin/env python3
"""Build the Gulf stretch: Route 9 (the Schiste), Kirrha, Aigion, Route 11
(the drum pass) and the Korykian Cave, with their events, scripts, wild
tables, trainers' teams, checks and review renders.

These maps were placeholders from tools/ichor/maps/arkadia.py (a straight
road past rectangles of grass, bare outdoor hamlets). arkadia.py now skips
them; this builder owns them. The ferry (GulfTrireme's landing points), the
two hamlets' heal locations and the rooms' events are written here too. The
rooms' cells are in tools/ichor/maps/gulf_rooms.py (built on gTileset_Domos).

Route 9, the Schiste. *From Lebadeia the road comes over the shoulder of
Parnassos at the three-ways where Oedipus killed his father, then steps down
three cliff tiers and through the olive sea to Kirrha.*
  - The three-ways: the old Daulis road west (a thicket, the Sickle), the
    goat path east up to the Korykian Cave, Laius's tomb by the road.
  - Polyon in the narrows below the tomb; the first band.
  - Tier 2: the shepherds' camp and its spring (the midpoint rest), a scree
    pocket behind rubble (the Hammer), Mnason at the bend, the second band.
  - Tier 3: Akeson on the long traverse, the lookout up to Delphoi, a ravine
    shut by a great boulder (Hephaestus's Hammer, later).
  - The olive sea: Eryx among the trees, the last band, the road to Kirrha.

The Korykian Cave. *Pan's and the nymphs' great cave, high on Parnassos: one
huge hall of stalagmites, a still pool, and the nymphs' grotto beyond a
thornweb.* Dark; a brazier lights the hall. A column drum (the Girdle) opens
the east grotto; a cobweb (the Torch) a side passage; the pool's islet waits
for the Conch, the inner grotto for the Three-Flamed Torch.

Kirrha. *Delphoi's port: a crescent of beach below the olive sea, the
pilgrims' hostel at the foot of the washed-out Sacred Way, Apollo
Delphinios's rock shrine on the harbor where he came ashore as a dolphin.*

Aigion. *The Gulf landing under Achaea's hills: a fishermen's beach, and on a
terrace above it the Homarion, where Agamemnon gathered the kings.*

Route 11, the drum pass. *Up the Selinous gorge beside its river, past the
nymph spring and the waterfall, to the pass where a fallen temple's column
drums block the road; then down into the bowl of Styx Falls.*

Pieces come from build/skiron/catalog.json (make it with
/usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile).

Usage: /usr/bin/python3 tools/ichor/maps/gulf.py [--render DIR] [--walk] [--rooms]
  --render DIR  <map>.png (2x, with people), <map>_walk.png and 15x10 views
  --walk        prints each walk map (# solid, . open, , grass, ~ water)
  --rooms       also rebuilds gTileset_Domos and the two rooms (Porytiles)
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
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import kithairon as K  # noqa: E402  (the grid, bands, trees, olives, ground, walk checks)
import route5 as R5  # noqa: E402  (aethos ids, noise, behaviors, sprites)
import water_tables as WT  # noqa: E402

noise, behavior = R5.noise, R5.behavior
GFX = "OBJ_EVENT_GFX_ICHOR_"
FACE = K.FACE
SEA = 0x170
WATERFALL = 0x0B3
CAVE_TOP, CAVE_DOOR = 0x09F, 0x0A7
DOOR = 0x021
TRIPOD_TOP, TRIPOD_BASE = 0x130, 0x131
HERM = 0x01B
FARMHOUSE = [[0x008, 0x009, 0x00A], [0x010, 0x011, 0x012], [0x018, 0x019, 0x01A], [0x020, 0x021, 0x022]]
INN = R5.INN                                    # 5x4, its door at (2, 3)
PALAESTRA = [[0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
             [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
             [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
             [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
             [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]]   # its door at (3, 4)

R9, KIRRHA, AIGION, R11, CAVE = ("Route9_ParnassosCrossroads", "Kirrha", "Aigion",
                                 "Route11_DrumPass", "Route9_KorykianCave")
HOSTEL, HOMARION = "Kirrha_PilgrimsHostel", "Aigion_Homarion"


def const(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


# ---------------------------------------------------------------------------
# The grid: kithairon's, plus water and the coast
# ---------------------------------------------------------------------------
# Plan kinds beyond kithairon.py's:
#   ~  water (sea, river, pool): open, elevation 1, surfable and fishable
#   d  sand (beach)                 q  a stone quay or ford (paved, open)
#   F  a sea-cliff's foot, rocks in the surf (solid)
#   W  a waterfall (open, elevation 1: the Horn climbs it)
#   h  under a building (solid; its door is set open by the stamp)

class Grid(K.Grid):
    def __init__(self, name, w, h, rows, strip_top=False, strip_bottom=False):
        super().__init__(name, w, h, strip_top, strip_bottom)
        assert len(rows) == h, f"{name}: {len(rows)} rows, want {h}"
        for y, r in enumerate(rows):
            assert len(r) == w, f"{name} row {y} is {len(r)} wide, want {w}: {r!r}"
            self.g[y] = list(r)
        self.water = np.zeros((h, w), bool)

    def wet(self, x, y, mid, kind):
        self.set(x, y, mid, False, kind)
        self.water[y, x] = True

    def stamp(self, x0, y0, rows, door=None, kind="building"):
        for j, row in enumerate(rows):
            for i, mid in enumerate(row):
                self.set(x0 + i, y0 + j, mid, (i, j) != door, kind)


def coast(g):
    """Water, sand, quays, sea-cliff feet and waterfalls."""
    def land(x, y):
        return 0 <= x < g.w and 0 <= y < g.h and g.g[y][x] not in "d~qFW"
    for y in range(g.h):
        for x in range(g.w):
            k = g.g[y][x]
            if g.fixed[y, x] and k != "F":
                continue
            if k == "d":
                n, s, w, e = land(x, y - 1), land(x, y + 1), land(x - 1, y), land(x + 1, y)
                g.set(x, y, R5.SAND[R5.edge9(n, s, w, e)], False, "sand")
            elif k == "~":
                def sandy(dx, dy):
                    X, Y = x + dx, y + dy
                    return 0 <= X < g.w and 0 <= Y < g.h and g.g[Y][X] == "d"
                if sandy(0, -1):
                    g.wet(x, y, R5.SHORE["b"], "shore")
                elif sandy(-1, 0):
                    g.wet(x, y, R5.SHORE["r"], "shore")
                elif sandy(1, 0):
                    g.wet(x, y, R5.SHORE["l"], "shore")
                else:
                    g.wet(x, y, SEA, "sea")
            elif k == "q":
                g.named("road", ("mid", "mid2", "mid3")[noise(x, y, 7) % 3], x, y)
                g.solid[y, x] = False
            elif k == "F":
                g.named("cliff", "foot_" + "ABC"[noise(x, y, 5) % 3], x, y)
                g.solid[y, x] = True
            elif k == "W":
                g.wet(x, y, WATERFALL, "falls")


def write_layout(g, border):
    lay_dir = ROOT / f"data/layouts/{g.name}"
    lay_dir.mkdir(parents=True, exist_ok=True)
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mt[y, x]) & 0x3FF
            if g.solid[y, x]:
                out[y, x] = mid | (1 << 10)
            elif g.water[y, x]:
                out[y, x] = mid | (1 << 12)
            else:
                out[y, x] = mid | (3 << 12)
    out.astype("<u2").tofile(lay_dir / "map.bin")
    np.array(border, np.uint16).astype("<u2").tofile(lay_dir / "border.bin")
    set_layout(g.name, g.w, g.h, "gTileset_Aethos", "gTileset_Skiron")
    return out


def set_layout(name, w, h, primary, secondary):
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    lid = "LAYOUT_" + const(name)
    for l in data["layouts"]:
        if l.get("id") == lid:
            want = (w, h, primary, secondary)
            if (l["width"], l["height"], l["primary_tileset"], l["secondary_tileset"]) != want:
                l["width"], l["height"], l["primary_tileset"], l["secondary_tileset"] = want
                path.write_text(json.dumps(data, indent=2) + "\n")
            return
    raise SystemExit(f"no layout {lid}")


def olive_blocks(g):
    """Olives grow in 2x2 blocks on even columns and rows (kithairon.olives); an
    'o' cell outside a whole block would be a stray boulder, so it becomes woods."""
    whole = set()
    for y in range(0, g.h - 1, 2):
        for x in range(0, g.w - 1, 2):
            cells = [(x + i, y + j) for j in range(2) for i in range(2)]
            if all(g.g[cy][cx] == "o" for cx, cy in cells):
                whole |= set(cells)
    for y in range(g.h):
        for x in range(g.w):
            if g.g[y][x] == "o" and (x, y) not in whole:
                g.g[y][x] = "#"


def gravel_banks(g):
    """A river or spring's open banks are white gravel (STYLE.md 4.5: the
    streambeds of white stones), so the water meets them with a lit edge."""
    for y in range(g.h):
        for x in range(g.w):
            if g.g[y][x] == "." and any(0 <= x + dx < g.w and 0 <= y + dy < g.h and g.g[y + dy][x + dx] == "~"
                                         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g.g[y][x] = "d"


def build_grid(g, props, town=False, banks=False):
    olive_blocks(g)
    if banks:
        gravel_banks(g)
    edge = {(x, y): g.g[y][x] for y in range(g.h) for x in range(g.w)
            if x in (0, g.w - 1) or y in (0, g.h - 1)}
    K.notch(g, fill="." if town else ",")
    for (x, y), ch in edge.items():                    # no bays open onto the map's edge
        g.g[y][x] = ch
    K.bands(g)
    coast(g)
    props(g)
    K.trees(g)
    K.olives(g)
    K.ground(g)
    return g


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class Spec:
    """One map's events and scripts."""

    def __init__(self, name):
        self.name = name
        self.px = name + "_EventScript_"
        self.lid = "LOCALID_" + const(name) + "_"
        self.objs, self.warps, self.coords, self.bgs = [], [], [], []
        self.scripts, self.trainers, self.connections = [], [], []
        self.mapscripts = f"mapscripts {name}_MapScripts {{}}"
        self.header = {}

    def obj(self, lid, gfx, x, y, facing, script, flag="0", sight=0, trainer=False, move=None):
        gfx = gfx if gfx.startswith("OBJ_") else GFX + gfx
        o = {"local_id": self.lid + lid if lid else None, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
             "movement_type": move or (f"MOVEMENT_TYPE_FACE_{facing}" if facing else "MOVEMENT_TYPE_NONE"),
             "movement_range_x": 0, "movement_range_y": 0,
             "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
             "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}
        if lid is None:
            o.pop("local_id")
        self.objs.append(o)
        return o

    def trainer(self, tid, name, gfx, x, y, facing, sight, intro, defeat, after, mandatory=True):
        """tid: the TRAINER_ICHOR_ suffix (R9_POLYON); name: the script and local id suffix."""
        self.obj(name, gfx, x, y, facing, self.px + name, sight=sight, trainer=True)
        self.trainers.append(dict(name=name, x=x, y=y, facing=facing, sight=sight, mandatory=mandatory))
        self.scripts.append(f'''script {self.px}{name} {{
    trainerbattle_single(TRAINER_ICHOR_{tid}, format("{intro}"), format("{defeat}"))
    msgbox(format("{after}"), MSGBOX_AUTOCLOSE)
    end
}}''')

    def person(self, name, gfx, x, y, facing, flag="0", script=None, move=None):
        self.obj(name.upper(), gfx, x, y, facing, script or self.px + name, flag, move=move)

    def obstacle(self, name, kind, x, y, flag):
        gfx, script = {"thicket": ("OBJ_EVENT_GFX_CUTTABLE_TREE", "EventScript_CutTree"),
                       "rubble": ("OBJ_EVENT_GFX_BREAKABLE_ROCK", "EventScript_RockSmash"),
                       "drum": ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "EventScript_StrengthBoulder"),
                       "great": ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "EventScript_IchorGreatBoulder"),
                       "web": ("OBJ_EVENT_GFX_CUTTABLE_TREE", self.px + "Web"),
                       "thornweb": ("OBJ_EVENT_GFX_CUTTABLE_TREE", "EventScript_IchorThornweb")}[kind]
        move = "MOVEMENT_TYPE_INVISIBLE" if kind in ("web", "thornweb") else None
        o = self.obj(name.upper(), gfx, x, y, "DOWN", script, flag, move=move)
        o["_kind"] = kind

    def item(self, item, x, y, flag):
        o = self.obj(None, "OBJ_EVENT_GFX_ITEM_BALL", x, y, "DOWN", "Common_EventScript_FindItem", flag)
        o["trainer_sight_or_berry_tree_id"] = item

    def hidden(self, item, x, y, flag):
        self.bgs.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
                         "quantity": 1, "underfoot": False})

    def sign(self, x, y, script, text=None, facing="ANY"):
        self.bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                         "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{facing}", "script": self.px + script})
        if text is not None:
            self.scripts.append(f'''script {self.px}{script} {{
    msgbox(format("{text}"), MSGBOX_SIGN)
    end
}}''')

    def warp(self, x, y, dest, dest_id):
        self.warps.append({"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dest_id)})

    def coord(self, x, y, var, script):
        self.coords.append({"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": "0",
                            "script": script})

    def objects(self):
        return [{k: v for k, v in o.items() if not k.startswith("_")} for o in self.objs]


def write_events(spec):
    path = ROOT / f"data/maps/{spec.name}/map.json"
    m = json.loads(path.read_text())
    m.update(spec.header)
    m["connections"] = spec.connections or None
    m["object_events"] = spec.objects()
    m["warp_events"] = spec.warps
    m["coord_events"] = spec.coords
    m["bg_events"] = spec.bgs
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    scripts = [spec.mapscripts,
               "// Generated by tools/ichor/maps/gulf.py; edit the builder, not this file."] + spec.scripts
    (ROOT / f"data/maps/{spec.name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")


import gulf_plans as P  # noqa: E402

# ---------------------------------------------------------------------------
# Seams, landings, heal spots, doors
# ---------------------------------------------------------------------------
R9_NORTH, R9_SOUTH = range(10, 14), range(14, 18)     # Lebadeia's road; Kirrha's (offset 0)
R11_NORTH, R11_SOUTH = range(13, 17), range(11, 13)   # Aigion's road; Styx Falls's (offset -1)
KIRRHA_LANDING, AIGION_LANDING = (16, 26), (16, 5)    # where the trireme sets you down
KIRRHA_HEAL, AIGION_HEAL = (12, 12), (19, 15)          # the healer stands one north of these
CAVE_DOOR_R9 = (29, 8)
KIRRHA_DOOR, AIGION_DOOR = (21, 8), (6, 22)
DRUM = (12, 37)                                        # Route 11's column drum
BRAZIER = "FLAG_ICHOR_BRAZIERS_START + 0x2C"           # world-act2's block (ENGINE_API.md §2)


def talk(px, name, *pages, gift=None, flag=None, after=None, need=None, need_text=None):
    """A person's script: lines, and optionally a one-time gift behind a flag
    (and behind a condition `need`, with what they say before it holds)."""
    body = "\\p".join(pages)
    if gift is None:
        return f'''script {px}{name} {{
    lock
    faceplayer
    msgbox(format("{body}"))
    release
}}'''
    cond = f"!flag({flag})" + (f" && {need}" if need else "")
    early = (f'''
    if (!flag({flag}) && !({need})) {{
        msgbox(format("{need_text}"))
        release
        end
    }}''' if need else "")
    return f'''script {px}{name} {{
    lock
    faceplayer{early}
    if ({cond}) {{
        msgbox(format("{body}"))
        giveitem({gift})
        if (var(VAR_RESULT) == TRUE) {{
            setflag({flag})
        }}
        release
        end
    }}
    msgbox(format("{after}"))
    release
}}'''


# ---------------------------------------------------------------------------
# Route 9
# ---------------------------------------------------------------------------

def props_route9(g):
    g.set(15, 4, R5.SIGN, True, "sign")
    g.set(19, 55, R5.SIGN, True, "sign")
    g.set(30, 36, R5.SIGN, True, "sign")
    g.piece("milestone", 5, 9)                         # the Daulis road's last milestone
    g.piece("mound", 15, 13)                           # Laius's tomb
    g.piece("stele_low", 18, 14)
    g.set(29, 7, CAVE_TOP, True, "mouth")
    g.set(29, 8, CAVE_DOOR, False, "door")
    g.piece("tent", 20, 24)                            # the shepherds' camp
    g.piece("tent_b", 28, 24)
    g.piece("cookfire", 24, 24)


def spec_route9():
    s = Spec(R9)
    s.header = {"music": "MUS_ICHOR_ROAD", "map_type": "MAP_TYPE_ROUTE"}
    s.connections = [{"direction": "up", "map": "MAP_LEBADEIA", "offset": 0},
                     {"direction": "down", "map": "MAP_KIRRHA", "offset": 0}]
    s.trainer("R9_POLYON", "POLYON", "HOPLITE", 14, 16, "LEFT", 2,
              "The three roads meet here. So do we.", "Fair. Take the south road.",
              "A king died at this crossing once. He wouldn't give way either.")
    s.trainer("R9_MNASON", "MNASON", "HARVESTER", 5, 27, "LEFT", 2,
              "The olives below are mine. The view's free.", "Keep the view. I'll keep the olives.",
              "Mind the grass at the stair. It's thick this year.")
    s.trainer("R9_AKESON", "AKESON", "PILGRIM", 15, 37, "UP", 2,
              "I walked from Thyrsa to ask the god one question.", "Now I have two.",
              "Delphoi's up there, past the falls. The way is shut, they say.")
    s.trainer("R9_ERYX", "ERYX", "ACOLYTE_F", 16, 51, "LEFT", 2,
              "Apollo's olives. Walk softly under them.", "Softly enough.",
              "The harbor's just past the trees. Kirrha.")
    s.trainer("R9_PHILTA", "PHILTA", "SHEPHERD", 26, 27, "LEFT", 3,
              "My flock grazes up to the cave and no farther.", "Smart flock.",
              "Pan lives in the cave up the goat path. He plays at noon, they say.", mandatory=False)
    s.trainer("R9_DEINON", "DEINON", "AUGUR", 22, 9, "DOWN", 2,
              "Crows over the cave mouth. That's a sign.", "Of you, it seems.",
              "Take a light into the cave. The nymphs keep it dark.", mandatory=False)
    s.trainer("R9_THEANO", "THEANO", "AUGUR", 29, 38, "UP", 3,
              "From here you can see the temple roofs, when the cloud lets you.",
              "The cloud let you win.", "One day the falls will let you up. Not today.", mandatory=False)
    s.person("Spring", "ELDER_F", 24, 26, "LEFT")
    s.obstacle("Thicket", "thicket", 5, 11, "FLAG_ICHOR_R9_THICKET_CUT")
    s.obstacle("Scree", "rubble", 24, 29, "FLAG_ICHOR_R9_SCREE_BROKEN")
    s.obstacle("Boulder", "great", 2, 37, "FLAG_ICHOR_R9_GREAT_BOULDER")
    s.item("ITEM_PP_UP", 3, 12, "FLAG_ICHOR_ITEM_R9_DAULIS")              # behind the thicket
    s.item("ITEM_HYPER_POTION", 17, 12, "FLAG_ICHOR_ITEM_R9_HEAL")       # the three-ways meadow
    s.item("ITEM_ULTRA_BALL", 29, 30, "FLAG_ICHOR_ITEM_R9_BALL")         # the scree pocket (the Hammer)
    s.item("ITEM_ETHER", 31, 45, "FLAG_ICHOR_ITEM_R9_ETHER")             # under the goat track
    s.item("ITEM_NUGGET", 1, 40, "FLAG_ICHOR_ITEM_R9_RAVINE")            # the ravine (Hephaestus's Hammer)
    s.hidden("ITEM_HONEY", 24, 24, "FLAG_ICHOR_HIDDEN_ITEM_R9_HONEY")    # by the shepherds' fire
    s.hidden("ITEM_REVIVE", 4, 13, "FLAG_ICHOR_HIDDEN_ITEM_R9_REVIVE")   # the Daulis road's end
    s.hidden("ITEM_SUPER_REPEL", 17, 53, "FLAG_ICHOR_HIDDEN_ITEM_R9_REPEL")   # in the olives by band 4
    s.hidden("ITEM_STAR_PIECE", 15, 13, "FLAG_ICHOR_HIDDEN_ITEM_R9_TOMB")     # in Laius's tomb
    s.warp(*CAVE_DOOR_R9, "MAP_ROUTE9_KORYKIAN_CAVE", 0)
    s.sign(15, 4, "NorthSign", "Route 9, the Schiste.\\nNorth: Lebadeia. South: Kirrha and the Gulf.")
    s.sign(19, 55, "SouthSign", "Route 9, the Schiste.\\nSouth: Kirrha. North: Lebadeia.")
    s.sign(30, 36, "Delphoi", "Delphoi is above the falls. The water has taken the stair.\\p"
                              "The road continues south to Kirrha.")
    s.sign(18, 14, "Tomb", "An old king's tomb at the three-ways.\\p"
                           "Someone has left a chariot's linchpin on it.")
    s.sign(5, 9, "Milestone", "DAULIS, the stone says. The road west is lost in thorns.")
    s.sign(28, 8, "Cave", "The Korykian Cave: Pan's, and the nymphs'.\\nBring a light.", facing="NORTH")
    s.scripts.append(f'''script {s.px}Spring {{
    lock
    faceplayer
    msgbox(format("Drink. It comes off the mountain cold enough to wake the dead."))
    special(HealPlayerParty)
    if (!flag(FLAG_ICHOR_R9_SPRING_GIFT)) {{
        msgbox(format("Take a skin of it for the road down. Kirrha's water tastes of boats."))
        giveitem(ITEM_FRESH_WATER, 2)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_R9_SPRING_GIFT)
        }}
        release
        end
    }}
    msgbox(format("There. The rest of the way is downhill."))
    release
}}''')
    return s


# ---------------------------------------------------------------------------
# Kirrha
# ---------------------------------------------------------------------------

def props_kirrha(g):
    g.piece("tent", 10, 4)                             # the pilgrims' outcamp
    g.piece("cookfire", 13, 5)
    g.piece("bedrolls", 11, 7)
    g.piece("myrtle", 10, 6)
    g.piece("baskets", 13, 7)
    g.piece("stele_low", 8, 7)                         # where the Sacred Way begins
    g.stamp(19, 5, INN, door=(2, 3))                   # the pilgrims' hostel
    g.set(11, 11, HERM, True, "herm")
    g.piece("amphorae", 11, 13)
    g.piece("niches", 21, 11)                          # Apollo Delphinios's rock shrine
    g.set(22, 14, TRIPOD_TOP, True, "altar")
    g.set(22, 15, TRIPOD_BASE, True, "altar")


def spec_kirrha():
    s = Spec(KIRRHA)
    s.header = {"music": "MUS_ICHOR_AKTI", "map_type": "MAP_TYPE_TOWN"}
    s.connections = [{"direction": "up", "map": "MAP_ROUTE9_PARNASSOS_CROSSROADS", "offset": 0}]
    s.mapscripts = '''mapscripts Kirrha_MapScripts {
    MAP_SCRIPT_ON_TRANSITION {
        setrespawn(HEAL_LOCATION_KIRRHA)
    }
}'''
    s.person("Healer", "HEALER", KIRRHA_HEAL[0], KIRRHA_HEAL[1] - 1, "DOWN")
    s.person("Merchant", "MERCHANT", 10, 13, "RIGHT")
    s.person("Guide", "ELDER_F", 5, 14, "DOWN")
    s.person("Captain", "SAILOR", 15, 27, "UP")
    s.person("Fisher", "FISHER", 6, 17, "DOWN")
    s.person("Pilgrim", "PILGRIM", 12, 4, "LEFT")
    s.person("BoatL", "UPTURNED_BOAT_L", 3, 17, "DOWN", script="0x0")
    s.person("BoatR", "UPTURNED_BOAT_R", 4, 17, "DOWN", script="0x0")
    s.item("ITEM_ELIXIR", 2, 7, "FLAG_ICHOR_ITEM_KIRRHA")                 # under the falls
    s.item("ITEM_BIG_PEARL", 3, 23, "FLAG_ICHOR_ITEM_KIRRHA_ISLET")      # the islet (the Conch)
    s.hidden("ITEM_STARDUST", 23, 13, "FLAG_ICHOR_HIDDEN_ITEM_KIRRHA_SHRINE")      # among the doves' niches
    s.hidden("ITEM_HEART_SCALE", 25, 17, "FLAG_ICHOR_HIDDEN_ITEM_KIRRHA_HEADLAND")  # under the headland
    s.warp(*KIRRHA_DOOR, "MAP_KIRRHA_PILGRIMS_HOSTEL", 0)
    s.sign(9, 1, "Stair", "The Sacred Way's stair climbs into the falls and is gone.\\p"
                          "Above the water, the mountain. Above the mountain, Delphoi.", facing="NORTH")
    s.sign(8, 7, "Stele", "KIRRHA\\nHere the Sacred Way begins. Go up clean.\\nTrireme to Aigion from the quay.")
    s.sign(22, 15, "Altar", "Apollo Delphinios's altar. He came ashore here as a dolphin,\\p"
                            "leading a ship of Knossian sailors to be his priests.")
    s.sign(21, 13, "Shrine", "Lamps and doves in the rock. Someone keeps the lamps full.")
    s.scripts += [
        f'''script {s.px}Healer {{
    setvar(VAR_0x800B, LOCALID_KIRRHA_HEALER)
    call(Ichor_EventScript_AsclepeionHealer)
    waitmessage
    waitbuttonpress
    release
}}''',
        f'''script {s.px}Merchant {{
    goto(ArkadiaApproach_EventScript_Merchant)
}}''',
        talk(s.px, "Guide", "Delphoi's up there. You can see the roofs when the cloud lifts.",
             "The falls took the old stair. You'll need another way.",
             "Arkadia? Cross the Gulf. The captain's on the quay."),
        f'''script {s.px}Captain {{
    lock
    faceplayer
    msgbox(format("Across to Aigion? There's room on the Euploia."), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        setvar(VAR_ICHOR_GULF_DEST, 0)
        warp(MAP_GULF_TRIREME, 13, 4)
        waitstate
        releaseall
        end
    }}
    release
}}''',
        talk(s.px, "Fisher", "See the islet? The best pearls in the Gulf grow off it.",
             "You'd need to swim like a dolphin to get there, mind."),
        talk(s.px, "Pilgrim", "We camp here till the falls drop. Some of us have camped a year.",
             "The god will open the way when he means to."),
    ]
    return s


# ---------------------------------------------------------------------------
# Aigion
# ---------------------------------------------------------------------------

def props_aigion(g):
    for x, y in ((3, 3), (6, 4), (1, 6), (8, 6), (11, 2), (24, 6), (20, 2)):   # Helike's drowned stones
        g.set(x, y, 0x0C5, True, "stack")
    for x, y in ((9, 1), (25, 9)):
        g.named("surf_rock", "A", x, y)
        g.named("surf_rock", "B", x + 1, y)
    g.piece("tent", 1, 14)                             # the fishers' camp
    g.piece("cookfire", 4, 14)
    g.piece("tent_b", 6, 14)
    g.piece("baskets", 9, 16)
    g.piece("firewood", 4, 16)
    g.stamp(3, 18, PALAESTRA, door=(3, 4))             # the Homarion
    g.set(8, 23, TRIPOD_TOP, True, "altar")            # the oath altar before it
    g.set(8, 24, TRIPOD_BASE, True, "altar")
    g.piece("pine_tall", 18, 22)                       # the Zeus oak
    g.piece("amphorae", 21, 15)
    g.set(23, 15, HERM, True, "herm")
    g.set(12, 16, R5.SIGN, True, "sign")
    g.set(11, 29, R5.SIGN, True, "sign")


def spec_aigion():
    s = Spec(AIGION)
    s.header = {"music": "MUS_ICHOR_AKTI", "map_type": "MAP_TYPE_TOWN"}
    s.connections = [{"direction": "down", "map": "MAP_ROUTE11_DRUM_PASS", "offset": 0}]
    s.mapscripts = '''mapscripts Aigion_MapScripts {
    MAP_SCRIPT_ON_TRANSITION {
        setrespawn(HEAL_LOCATION_AIGION)
    }
}'''
    s.person("Healer", "HEALER", AIGION_HEAL[0], AIGION_HEAL[1] - 1, "DOWN")
    s.person("Merchant", "MERCHANT", 22, 15, "DOWN")
    s.person("Guide", "ELDER_F", 11, 15, "DOWN")
    s.person("Captain", "SAILOR", 15, 4, "DOWN")
    s.person("Fisher", "FISHER", 5, 15, "DOWN")
    s.person("Kid", "KID_M", 9, 12, "LEFT")
    s.person("BoatL", "UPTURNED_BOAT_L", 21, 12, "DOWN", script="0x0")
    s.person("BoatR", "UPTURNED_BOAT_R", 22, 12, "DOWN", script="0x0")
    s.item("ITEM_FULL_HEAL", 1, 27, "FLAG_ICHOR_ITEM_AIGION")             # the lane under the terrace
    s.item("ITEM_STAR_PIECE", 4, 5, "FLAG_ICHOR_ITEM_AIGION_HELIKE")      # Helike's islet (the Conch)
    s.hidden("ITEM_NET_BALL", 1, 15, "FLAG_ICHOR_HIDDEN_ITEM_AIGION_CAMP")       # in the tent
    s.hidden("ITEM_SMOKE_BALL", 2, 21, "FLAG_ICHOR_HIDDEN_ITEM_AIGION_TERRACE")  # behind the Homarion
    s.warp(*AIGION_DOOR, "MAP_AIGION_HOMARION", 0)
    s.sign(12, 16, "Sign", "AIGION\\nSouth: the drum pass and Arkadia. Trireme to Kirrha.")
    s.sign(11, 29, "SouthSign", "South: Route 11, up the Selinous gorge to the drum pass.")
    s.sign(8, 24, "Altar", "The oath altar. Here the kings swore to sail for Troy,\\n"
                           "and here the towns of Achaea still swear.")
    s.sign(18, 24, "Oak", "Zeus's oak. Every acorn on it is somebody's promise.")
    s.scripts += [
        f'''script {s.px}Healer {{
    setvar(VAR_0x800B, LOCALID_AIGION_HEALER)
    call(Ichor_EventScript_AsclepeionHealer)
    waitmessage
    waitbuttonpress
    release
}}''',
        f'''script {s.px}Merchant {{
    goto(ArkadiaApproach_EventScript_Merchant)
}}''',
        talk(s.px, "Guide", "The pass is full of fallen column drums. Nothing wrong with the road under them.",
             "There's an actor in Thyrsa with Herakles's girdle. Or so he says.",
             "Get those drums moving and it's Styx Falls, then Arkadia."),
        f'''script {s.px}Captain {{
    lock
    faceplayer
    msgbox(format("Back to Kirrha? We sail when you're aboard."), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        setvar(VAR_ICHOR_GULF_DEST, 1)
        warp(MAP_GULF_TRIREME, 13, 4)
        waitstate
        releaseall
        end
    }}
    release
}}''',
        talk(s.px, "Fisher", "On a still morning you can see Helike down there. Columns, roofs, a whole town.",
             "Poseidon took it in one night. Take these, for when you can follow the fish down.",
             gift="ITEM_DIVE_BALL", flag="FLAG_ICHOR_AIGION_FISHER_GIFT",
             after="Don't fish over Helike. Nets come up with lamps in them."),
        talk(s.px, "Kid", "The old men in the Homarion say the kings swore on that altar.",
             "I swore I'd swim to the islet. I didn't say when."),
    ]
    return s


# ---------------------------------------------------------------------------
# Route 11
# ---------------------------------------------------------------------------

def props_route11(g):
    g.set(18, 3, R5.SIGN, True, "sign")
    g.set(14, 49, R5.SIGN, True, "sign")
    g.piece("niches", 15, 18)                          # the nymphs of the Selinous
    g.piece("watchtower", 23, 13)                      # an Achaean watchtower on the gorge's rim
    g.piece("mound", 22, 39)                           # a hero's mound above the pass
    g.piece("stele_family", 25, 40)
    for x, y in ((10, 38), (14, 37), (8, 40), (17, 44)):
        if g.g[y][x] in "^.,":
            g.piece("drum", x, y)                      # the fallen temple's drums
    g.piece("stele_palmette", 7, 43) if g.room(7, 43, 1, 2, (".", ",")) else None
    g.piece("rubble", 16, 42) if g.room(16, 42, 2, 2, (".", ",")) else None


def spec_route11():
    s = Spec(R11)
    s.header = {"music": "MUS_ICHOR_ROAD", "map_type": "MAP_TYPE_ROUTE"}
    s.connections = [{"direction": "up", "map": "MAP_AIGION", "offset": 0},
                     {"direction": "down", "map": "MAP_STYX_FALLS", "offset": -1}]
    s.obstacle("Drum", "drum", *DRUM, "0")
    s.trainer("R11_DORYS", "DORYS", "HOPLITE", 16, 6, "LEFT", 2,
              "Aigion's watch. State your road.", "South, then. Go on.",
              "The gorge narrows after the stair. Watch the river.")
    s.trainer("R11_THRASEAS", "THRASEAS", "PILGRIM", 11, 16, "LEFT", 4,
              "The Selinous runs cold even in summer.", "So does my luck.",
              "There's a ford upstream, if you want the far bank.")
    s.trainer("R11_LACHON", "LACHON", "HARVESTER", 11, 21, "LEFT", 4,
              "I cut reeds in the gorge. And battlers.", "Not today.",
              "The nymphs' spring heals anyone who asks nicely.")
    s.trainer("R11_XANTHE", "XANTHE", "AUGUR", 2, 20, "UP", 3,
              "The river told me someone would cross.", "It didn't say who'd win.",
              "Look at the falls. Something up there glitters.", mandatory=False)
    s.trainer("R11_MYRINE", "MYRINE", "ACOLYTE_F", 14, 35, "LEFT", 2,
              "Artemis's old temple fell across this road.", "And you'd move it?",
              "The drums are too heavy for anyone but a hero.")
    s.trainer("R11_PHERON", "PHERON", "SHEPHERD", 14, 45, "LEFT", 3,
              "You moved the drums? Then you can move me.", "Moved.",
              "Styx Falls is down the road. Swear nothing there.")
    s.person("Spring", "ELDER_F", 14, 19, "LEFT")
    s.obstacle("Rubble", "rubble", 15, 26, "FLAG_ICHOR_R11_RUBBLE_BROKEN")
    s.item("ITEM_HYPER_POTION", 1, 22, "FLAG_ICHOR_ITEM_R11_HEAL")        # the west bank
    s.item("ITEM_ULTRA_BALL", 17, 26, "FLAG_ICHOR_ITEM_R11_BALL")         # behind the rubble (the Hammer)
    s.item("ITEM_ETHER", 8, 43, "FLAG_ICHOR_ITEM_R11_ETHER")              # the fallen temple
    s.item("ITEM_PP_UP", 3, 7, "FLAG_ICHOR_ITEM_R11_FALLS")               # above the falls (the Horn)
    s.item("ITEM_BIG_PEARL", 4, 28, "FLAG_ICHOR_ITEM_R11_ISLET")          # the river's islet (the Conch)
    s.hidden("ITEM_HONEY", 15, 20, "FLAG_ICHOR_HIDDEN_ITEM_R11_HONEY")    # the nymphs' niches
    s.hidden("ITEM_REVIVE", 2, 24, "FLAG_ICHOR_HIDDEN_ITEM_R11_REVIVE")   # the west bank's end
    s.hidden("ITEM_SUPER_REPEL", 16, 43, "FLAG_ICHOR_HIDDEN_ITEM_R11_REPEL")  # the temple's rubble
    s.sign(18, 3, "Sign0", "Route 11, the drum pass.\\nNorth: Aigion. South: Styx Falls.")
    s.sign(14, 49, "Sign1", "Route 11, the drum pass.\\nNorth: Aigion. South: Styx Falls.")
    s.scripts.append(f'''script {s.px}Spring {{
    lock
    faceplayer
    msgbox(format("The nymphs' water. Rest a moment."))
    special(HealPlayerParty)
    if (!flag(FLAG_ICHOR_R11_SPRING_GIFT)) {{
        msgbox(format("The nymphs left this in the spring. They'd want it carried."))
        giveitem(ITEM_MYSTIC_WATER)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_R11_SPRING_GIFT)
        }}
        release
        end
    }}
    msgbox(format("The pass above is all stone. Go well."))
    release
}}''')
    return s


# ---------------------------------------------------------------------------
# The Korykian Cave (cave_dark, as tools/ichor/maps/hecates_hollow.py)
# ---------------------------------------------------------------------------
CAVE_W, CAVE_H = 34, 26
CAVE_MOUTH = [(15, 25), (16, 25)]
CAVE_WEB = (5, 16)                 # web_1 on (x, y) and (x, y + 1)
CAVE_THORNWEB = (17, 4)
CAVE_BRAZIER = (21, 6)             # 2x2
CAVE_NICHE = (13, 4)               # Pan's niche, 1x2 on the hall's north face
CAVE_PIECES = [
    ("daylight_s", 15, 24), ("daylight_s", 16, 24),
    ("web_1", *CAVE_WEB), ("web_1", *CAVE_THORNWEB),
    ("brazier_cold", *CAVE_BRAZIER),
    ("niche_empty", *CAVE_NICHE),
    ("altar_stone", 12, 7),
    ("stele", 13, 22),
    ("column", 9, 9), ("column", 23, 10), ("column", 18, 16),
    ("stalagmites", 11, 13), ("stalagmite", 26, 8), ("stalagmites", 20, 12), ("stalagmite_tall", 14, 10),
    ("stalagmite", 9, 17), ("stalagmites", 25, 15), ("rock_pile", 3, 21), ("slab", 27, 21),
    ("pebbles", 16, 8), ("pebbles", 19, 14), ("pebbles", 10, 18), ("bones", 29, 19),
    ("pebbles", 15, 2), ("stalagmite", 19, 1),
]
CAVE_ZONE_EDGE = [(x, 20) for x in range(12, 18)], [(x, 21) for x in range(12, 18)]


def cave_build():
    import cave_dark_kit as kit
    cat = json.loads((ROOT / "data/tilesets/secondary/cave_dark/catalog.json").read_text())
    piece = {p["key"]: p for p in cat["pieces"]}
    rows = P.CAVE
    ids = np.array(kit.autotile(rows, cat, None), np.int32)
    kinds = kit.classify(rows)
    walk = np.zeros((CAVE_H, CAVE_W), bool)
    water = np.zeros((CAVE_H, CAVE_W), bool)
    for y in range(CAVE_H):
        for x in range(CAVE_W):
            walk[y, x] = kinds[y][x] in ("floor", "lit")
            water[y, x] = kinds[y][x] == "water"
    for key, x, y in CAVE_PIECES:
        p = piece[key]
        for j in range(p["h"]):
            for i in range(p["w"]):
                ids[y + j, x + i] = p["ids"][j][i]
                walk[y + j, x + i] = p["walk"][j][i] in set(".T^v[]")
    webs = {(x, y + j) for x, y in (CAVE_WEB, CAVE_THORNWEB) for j in (0, 1)}
    out = np.zeros((CAVE_H, CAVE_W), np.uint16)
    for y in range(CAVE_H):
        for x in range(CAVE_W):
            mid = int(ids[y, x]) & 0x3FF
            if walk[y, x] or (x, y) in webs:
                out[y, x] = mid | (3 << 12)
            elif water[y, x]:
                out[y, x] = mid | (1 << 12)
            else:
                out[y, x] = mid | (1 << 10)
    d = ROOT / f"data/layouts/{CAVE}"
    d.mkdir(parents=True, exist_ok=True)
    out.astype("<u2").tofile(d / "map.bin")
    np.full(4, cat["kit"]["T|..."] | (1 << 10), np.uint16).astype("<u2").tofile(d / "border.bin")
    set_layout(CAVE, CAVE_W, CAVE_H, "gTileset_Aethos", "gTileset_CaveDark")
    return out, walk, water, piece


def spec_cave(piece):
    s = Spec(CAVE)
    s.header = {"music": "MUS_ICHOR_HOLLOW", "requires_flash": True, "weather": "WEATHER_NONE",
                "map_type": "MAP_TYPE_UNDERGROUND", "allow_cycling": False, "allow_escaping": True,
                "show_map_name": True}
    lit = piece["brazier_lit"]["ids"]
    torn = piece["torn_1"]["ids"]
    bx, by = CAVE_BRAZIER
    draw_brazier = "\n".join(f"    setmetatile({bx + i}, {by + j}, 0x{lit[j][i]:03X}, TRUE)"
                             for j in range(2) for i in range(2))
    draw_webs = ""
    for (x, y), flag in ((CAVE_WEB, "FLAG_ICHOR_KORYKIAN_WEB_BURNT"),
                         (CAVE_THORNWEB, "FLAG_ICHOR_KORYKIAN_THORNWEB_BURNT")):
        draw_webs += f'''
    if (flag({flag})) {{
        setmetatile({x}, {y}, 0x{torn[0][0]:03X}, FALSE)
        setmetatile({x}, {y + 1}, 0x{torn[1][0]:03X}, FALSE)
    }}'''
    s.mapscripts = f'''mapscripts {CAVE}_MapScripts {{
    MAP_SCRIPT_ON_LOAD {{
        call({s.px}Draw)
    }}
    MAP_SCRIPT_ON_FRAME_TABLE [
        VAR_TEMP_9, 0: {s.px}Redraw
    ]
}}'''
    s.scripts += [
        f'''// The hall's brazier and the burnt webs, drawn before the map shows.
script {s.px}Draw {{
    if (flag({BRAZIER})) {{
        call({s.px}DrawBrazier)
    }}{draw_webs}
    return
}}''',
        f'''script {s.px}DrawBrazier {{
{draw_brazier}
    return
}}''',
        f'''script {s.px}Redraw {{
    setvar(VAR_TEMP_9, 1)
    call({s.px}Draw)
    special(DrawWholeMapView)
    end
}}''',
        f'''script {s.px}Web {{
    setvar(VAR_TEMP_9, 0)
    goto(EventScript_IchorCobweb)
}}''',
        f'''script {s.px}Thornweb {{
    setvar(VAR_TEMP_9, 0)
    goto(EventScript_IchorThornweb)
}}''',
        f'''// Pan's brazier lights the whole cave beyond the mouth's daylight (ENGINE_API.md §2).
script {s.px}Brazier {{
    setvar(VAR_0x8004, {BRAZIER})
    setvar(VAR_0x8005, TRUE)
    call(EventScript_IchorBrazier)
    if (var(VAR_RESULT) == TRUE) {{
        call({s.px}DrawBrazier)
        special(DrawWholeMapView)
        msgbox(format("The brazier roars up. Stone teeth crowd the dark, all the way to the pool."))
    }}
    releaseall
}}''',
        f'''script {s.px}EnterHall {{
    lockall
    setvar(VAR_0x8004, {BRAZIER})
    call(EventScript_IchorEnterLitZone)
    releaseall
    end
}}''',
        f'''script {s.px}LeaveHall {{
    lockall
    call(EventScript_IchorLeaveLitZone)
    releaseall
    end
}}''',
        f'''script {s.px}Niche {{
    lock
    if (!flag(FLAG_ICHOR_KIRRHA_BEE_FOUND) && flag(FLAG_ICHOR_KIRRHA_BEE_ASKED)) {{
        msgbox(format("Pan's niche: pipes of reed, knucklebones, a clay goat.\\p"
                      "Among them, a little gold bee on a broken thread."))
        setflag(FLAG_ICHOR_KIRRHA_BEE_FOUND)
        msgbox(format("You take the bee for Hesychia."))
        release
        end
    }}
    msgbox(format("Pan's niche: pipes of reed, knucklebones, a clay goat.\\p"
                  "The knucklebones are loaded. Pan doesn't lose."))
    release
}}''',
        f'''script {s.px}Altar {{
    msgbox(format("A rough altar. Honey and milk, long dried, for the nymphs."), MSGBOX_SIGN)
    end
}}''',
        f'''script {s.px}Stele {{
    msgbox(format("THE KORYKIAN CAVE\\nSacred to Pan and the nymphs. Leave what you find."), MSGBOX_SIGN)
    end
}}''',
    ]
    s.trainer("KORYKIAN_TITYROS", "TITYROS", "GOATHERD", 15, 14, "DOWN", 3,
              "Hear that? Pipes. Every noon, from nowhere.", "Even Pan stopped to listen.",
              "The pool goes deeper than any light I've carried.")
    s.trainer("KORYKIAN_KORYKIA", "KORYKIA", "ACOLYTE_F", 24, 20, "RIGHT", 3,
              "I'm named for the nymph of this cave. She lends me her bees.", "They sting for her, not me.",
              "Past the thorn curtain north is the nymphs' own grotto. No flame I have will burn it.")
    s.obstacle("Drum", "drum", 28, 12, "0")
    for k in (0, 1):
        s.obstacle(f"Web{k}", "web", CAVE_WEB[0], CAVE_WEB[1] + k, "FLAG_ICHOR_KORYKIAN_WEB_BURNT")
        s.obstacle(f"Thorn{k}", "thornweb", CAVE_THORNWEB[0], CAVE_THORNWEB[1] + k,
                   "FLAG_ICHOR_KORYKIAN_THORNWEB_BURNT")
    for o in s.objs:
        if o.get("_kind") == "thornweb":
            o["script"] = s.px + "Thornweb"
    s.item("ITEM_HARD_STONE", 30, 19, "FLAG_ICHOR_ITEM_KORYKIAN_GROTTO")
    s.item("ITEM_MOON_STONE", 3, 20, "FLAG_ICHOR_ITEM_KORYKIAN_CHAMBER")    # behind the cobweb (the Torch)
    s.item("ITEM_PEARL", 4, 10, "FLAG_ICHOR_ITEM_KORYKIAN_ISLET")           # the pool's islet (the Conch)
    s.item("ITEM_LEFTOVERS", 16, 2, "FLAG_ICHOR_ITEM_KORYKIAN_SANCTUM")     # the nymphs' grotto (the Three-Flamed Torch)
    s.item("ITEM_ESCAPE_ROPE", 25, 7, "FLAG_ICHOR_ITEM_KORYKIAN_HALL")
    s.hidden("ITEM_HONEY", 13, 7, "FLAG_ICHOR_HIDDEN_ITEM_KORYKIAN_ALTAR")
    s.hidden("ITEM_STARDUST", 32, 12, "FLAG_ICHOR_HIDDEN_ITEM_KORYKIAN_BAY")
    for i, (x, y) in enumerate(CAVE_MOUTH):
        s.warp(x, y, "MAP_ROUTE9_PARNASSOS_CROSSROADS", 0)
    for x, y in CAVE_ZONE_EDGE[0]:
        s.coord(x, y, "VAR_TEMP_5", s.px + "EnterHall")
    for x, y in CAVE_ZONE_EDGE[1]:
        s.coord(x, y, "VAR_TEMP_5", s.px + "LeaveHall")
    bx, by = CAVE_BRAZIER
    for (x, y) in ((bx, by + 1), (bx + 1, by + 1)):
        s.bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                      "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": s.px + "Brazier"})
    s.bgs.append({"type": "sign", "x": CAVE_NICHE[0], "y": CAVE_NICHE[1] + 1, "elevation": 0,
                  "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": s.px + "Niche"})
    s.bgs.append({"type": "sign", "x": 12, "y": 7, "elevation": 0,
                  "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": s.px + "Altar"})
    s.bgs.append({"type": "sign", "x": 13, "y": 22, "elevation": 0,
                  "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": s.px + "Stele"})
    return s


# ---------------------------------------------------------------------------
# The rooms' events (their cells: gulf_rooms.py)
# ---------------------------------------------------------------------------

def spec_hostel():
    s = Spec(HOSTEL)
    s.header = {"music": "MUS_ICHOR_AKTI", "map_type": "MAP_TYPE_INDOOR", "weather": "WEATHER_NONE",
                "show_map_name": False}
    s.person("Xenarete", "WOMAN", 11, 4, "DOWN")
    s.person("Hesychia", "ELDER_F", 4, 5, "RIGHT")
    s.person("Lykinos", "PILGRIM", 1, 4, "DOWN")
    for x in (7, 8):
        s.warp(x, 8, "MAP_KIRRHA", 0)
    s.sign(3, 1, "RoadMap", "The road up the mountain, scratched by those who came back down.\\p"
                            "Each has drawn the falls bigger than the last.", facing="NORTH")
    s.sign(7, 2, "Altar", "A little altar of Apollo, under the window that looks up the mountain.",
           facing="NORTH")
    s.sign(5, 5, "Hearth", "The common hearth. A pot of lentils has been going since morning.",
           facing="NORTH")
    s.sign(10, 3, "Kitchen", "Xenarete's kitchen hearth. Bread rising on the warm stones.", facing="NORTH")
    s.scripts += [
        talk(s.px, "Xenarete", "Pilgrims, sailors, lost sheep, I feed them all.",
             "Here. Water from the Kastalian spring, carried down by the last priest who came.",
             "It keeps a water-dweller strong.",
             gift="ITEM_MYSTIC_WATER", flag="FLAG_ICHOR_KIRRHA_WATER_GIFT",
             after="Eat something before you climb anywhere."),
        f'''script {s.px}Hesychia {{
    lock
    faceplayer
    if (flag(FLAG_ICHOR_KIRRHA_BELL_GIFT)) {{
        msgbox(format("Bees know the way home in the dark. So do daughters."))
        release
        end
    }}
    if (flag(FLAG_ICHOR_KIRRHA_BEE_FOUND)) {{
        msgbox(format("My bee! Pan kept it all these years.\\p"
                      "I was a melissa once, a bee of Delphoi. So was a girl I loved,\\p"
                      "who ran away to the islands. She had your eyes.\\p"
                      "Take the hive bell. It brings a friend's heart close."))
        giveitem(ITEM_SOOTHE_BELL)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_KIRRHA_BELL_GIFT)
        }}
        release
        end
    }}
    msgbox(format("I left a gold bee in Pan's cave, up the goat path on the Schiste,\\p"
                  "the year I left the god's service. I'm too old for the climb now.\\p"
                  "If you go, look in Pan's niche. Bring a light."))
    setflag(FLAG_ICHOR_KIRRHA_BEE_ASKED)
    release
}}''',
        talk(s.px, "Lykinos", "I've asked the god the same question for a year: when will the falls let us up?",
             "The water answers. It says not yet."),
    ]
    return s


def spec_homarion():
    s = Spec(HOMARION)
    s.header = {"music": "MUS_ICHOR_TEMPLE", "map_type": "MAP_TYPE_INDOOR", "weather": "WEATHER_NONE",
                "show_map_name": False}
    s.person("Agesandros", "PRIESTESS", 9, 3, "DOWN")
    s.person("Kleobis", "ELDER_M", 13, 6, "LEFT")
    for x in (7, 8):
        s.warp(x, 9, "MAP_AIGION", 0)
    s.sign(7, 2, "Altar", "The altar of Zeus Homagyrios, who gathers men.\\p"
                          "Every king who sailed for Troy left a scratch on it.", facing="NORTH")
    s.sign(2, 1, "Doors", "Bronze doors to the adyton, barred with a beam as thick as a mast.\\p"
                          "Wax seals over the bar, each with a different city's stamp.", facing="NORTH")
    s.sign(12, 4, "Tablets", "Bronze tablets: the oaths of the Achaean towns.\\p"
                             "The oldest is in letters nobody can read any more.", facing="NORTH")
    s.sign(6, 5, "Mosaic", "A host stepping out of his door to greet a traveller.\\nZeus keeps the guest-right too.",
           facing="SOUTH")
    s.scripts += [
        f'''script {s.px}Agesandros {{
    lock
    faceplayer
    if (flag(FLAG_BADGE05_GET) && !flag(FLAG_ICHOR_AIGION_PRIEST_GIFT)) {{
        msgbox(format("The Huntress's laurel. Then you've kept faith in Arkadia.\\p"
                      "The god gathers those who keep faith. Wear this; it was a king's."))
        giveitem(ITEM_KINGS_ROCK)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_AIGION_PRIEST_GIFT)
        }}
        release
        end
    }}
    if (flag(FLAG_ICHOR_AIGION_PRIEST_GIFT)) {{
        msgbox(format("The doors stay barred until the towns all agree to open them.\\p"
                      "They have not agreed on anything for a thousand years."))
        release
        end
    }}
    msgbox(format("This is where the kings gathered before Troy.\\p"
                  "Come back with a laurel from Arkadia and the god will know your name."))
    release
}}''',
        talk(s.px, "Kleobis", "I rowed for the league when I was young. Forty oars and one oath.",
             "Take this. The sea gave it back to me, so it's lucky.",
             gift="ITEM_SHELL_BELL", flag="FLAG_ICHOR_AIGION_OATH_GIFT",
             after="An oath is a rope. Pull it or it pulls you."),
    ]
    return s


# ---------------------------------------------------------------------------
# Wild tables
# ---------------------------------------------------------------------------
# Land slots run 20 20 10 10 10 10 5 5 4 4 1 1 percent. Levels follow BALANCE.md
# (Arkadia: wild 26-33): Route 9 27-31, the cave 28-32, Route 11 29-33.
WILD = {
    R9: ("MAP_ROUTE9_PARNASSOS_CROSSROADS", 27, 31, 22, {
        "Morning": ["NEBREL", "AMPELIX", "LOPHOPS", "ERIPIP", "PEBBLITH", "MELIBEE",
                    "GALEKIT", "KERAZAP", "ONOTIS", "CAIRNOLITH", "HARPELLE", "MIDONOS"],
        "Day": ["NEBREL", "AMPELIX", "ERIPIP", "LOPHOPS", "MELIBEE", "PEBBLITH",
                "KERAZAP", "GALEKIT", "ONOTIS", "CAIRNOLITH", "HARPELLE", "MIDONOS"],
        "Evening": ["AMPELIX", "GELASABLE", "NEBREL", "PEBBLITH", "BOTRYKIT", "LOPHOPS",
                    "LYKOPUP", "PROSOMIME", "ERIPIP", "CAIRNOLITH", "HARPELLE", "KERAZAP"],
        "Night": ["GELASABLE", "LYKOPUP", "PROSOMIME", "BOTRYKIT", "PEBBLITH", "SPALUNK",
                  "AMPELIX", "RAKNIT", "GALEKIT", "CAIRNOLITH", "PROSOMIME", "MIDONOS"],
    }),
    R11: ("MAP_ROUTE11_DRUM_PASS", 29, 33, 22, {
        "Morning": ["ERIPIP", "NEBREL", "PEBBLITH", "KERAZAP", "ARKOBY", "LOPHOPS",
                    "MELIBEE", "ONOTIS", "CAIRNOLITH", "HARPELLE", "MIDONOS", "ARKOBY"],
        "Day": ["ERIPIP", "PEBBLITH", "NEBREL", "ARKOBY", "KERAZAP", "MELIBEE",
                "LOPHOPS", "CAIRNOLITH", "ONOTIS", "HARPELLE", "MIDONOS", "RAKNIT"],
        "Evening": ["PEBBLITH", "GELASABLE", "ARKOBY", "LYKOPUP", "ERIPIP", "BOTRYKIT",
                    "PROSOMIME", "CAIRNOLITH", "RAKNIT", "KERAZAP", "HARPELLE", "MIDONOS"],
        "Night": ["LYKOPUP", "GELASABLE", "PROSOMIME", "RAKNIT", "PEBBLITH", "SPALUNK",
                  "BOTRYKIT", "ARKOBY", "CAIRNOLITH", "LYKOPUP", "PROSOMIME", "RAKNIT"],
    }),
    CAVE: ("MAP_ROUTE9_KORYKIAN_CAVE", 28, 32, 8, {
        "Morning": ["SPALUNK", "PEBBLITH", "GALEKIT", "CAIRNOLITH", "RAKNIT", "GELASABLE",
                    "SPALUNK", "PEBBLITH", "MELIBEE", "CAIRNOLITH", "ARKOBY", "MELISSEER"],
        "Night": ["SPALUNK", "RAKNIT", "GELASABLE", "PEBBLITH", "PROSOMIME", "CAIRNOLITH",
                  "LYKOPUP", "SPALUNK", "RAKNIT", "GELASABLE", "ARKOBY", "PROSOMIME"],
    }),
}
MIN_LEVEL = {"CAIRNOLITH": 25, "HARPELLE": 26, "MIDONOS": 25, "GELASABLE": 20, "MELISSEER": 31,
             "KERAZAP": 0}
WATER = {R9: WT.pond(28), R11: WT.pond(30), CAVE: WT.pond(29)}
# the Hammer's rubble: limestone and what lives under it
SMASH = {R9: [("PEBBLITH", 27, 30), ("SPALUNK", 27, 30), ("PEBBLITH", 29, 31), ("CAIRNOLITH", 29, 31),
              ("CHELONET", 28, 31)],
         R11: [("PEBBLITH", 29, 32), ("SPALUNK", 29, 32), ("CAIRNOLITH", 30, 33), ("PEBBLITH", 31, 33),
               ("CHELONET", 30, 33)]}


def write_wild():
    path = ROOT / "src/data/wild_encounters.json"
    data = json.loads(path.read_text())
    group = next(gr for gr in data["wild_encounter_groups"] if gr.get("for_maps"))
    ids = {v[0] for v in WILD.values()}
    old = group["encounters"]
    at = next((i for i, e in enumerate(old) if e.get("map") in ids), len(old))
    new = []
    for name, (mapid, lo, hi, rate, tables) in WILD.items():
        for time, species in tables.items():
            mons = []
            for i, sp in enumerate(species):
                a = max(lo, MIN_LEVEL.get(sp, lo))
                b = hi if i % 3 else max(a, hi - 1)
                mons.append({"min_level": a, "max_level": b, "species": "SPECIES_" + sp})
            e = {"map": mapid, "base_label": f"g{name}_{time}", "land_mons": {"encounter_rate": rate, "mons": mons}}
            if time == "Morning":
                e.update(json.loads(json.dumps(WATER[name])))
                if name in SMASH:
                    e["rock_smash_mons"] = {"encounter_rate": 20, "mons": [
                        {"min_level": a, "max_level": b, "species": "SPECIES_" + sp} for sp, a, b in SMASH[name]]}
            new.append(e)
    keep = [e for e in old if e.get("map") not in ids]
    before = [e for e in old[:at] if e.get("map") not in ids]
    group["encounters"] = before + new + keep[len(before):]
    WT.apply(group["encounters"], maps={"MAP_KIRRHA", "MAP_AIGION", "MAP_GULF_TRIREME"})
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# The new trainers: ids from world-act2's 820-849 block (claim_ranges.md),
# from the top, so the Gulf's never meets another builder's on a line
# ---------------------------------------------------------------------------
NEW_TRAINERS = [
    # tag, id, name, class, pic, gender, team [(species, level)]
    ("R9_THEANO", 847, "THEANO", "Augur", "Augur", "Female", [("Prosomime", 31), ("Kerazap", 32)]),
    ("KORYKIAN_TITYROS", 848, "TITYROS", "Goatherd", "Goatherd", "Male",
     [("Arkoby", 31), ("Lykopup", 31), ("Arkoby", 33)]),
    ("KORYKIAN_KORYKIA", 849, "KORYKIA", "Beekeeper", "Beekeeper", "Female",
     [("Melibee", 31), ("Melisseer", 33)]),
]


def write_trainers():
    path = ROOT / "include/constants/opponents.h"
    text = path.read_text()
    start, end = "// Gulf: tools/ichor/maps/gulf.py\n", "// End Gulf.\n"
    block = start + "".join(f"#define TRAINER_ICHOR_{tag:<28} {tid}\n" for tag, tid, *_ in NEW_TRAINERS) + end
    if start in text:
        text = text.split(start)[0] + block + text.split(end, 1)[1]
    else:
        anchor = "#define TRAINERS_END_ACT2"
        i = text.index(anchor)
        text = text[:i] + block + text[i:]
    top = max(t[1] for t in NEW_TRAINERS) + 1
    text = re.sub(r"(#define TRAINERS_END_ACT2\s+)(\d+)",
                  lambda m: m.group(1) + str(max(int(m.group(2)), top)), text)
    path.write_text(text)
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Gulf teams (tools/ichor/maps/gulf.py). */", "/* End Gulf teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    out = before.rstrip() + "\n\n" + start + "\n"
    for tag, _, name, cls, pic, gender, team in NEW_TRAINERS:
        out += f"\n=== TRAINER_ICHOR_{tag} ===\nName: {name}\nClass: {cls}\nPic: {pic}\n"
        out += f"Gender: {gender}\nMusic: {gender}\nAI: Basic Trainer\n"
        for species, level in team:
            out += f"\n{species}\nLevel: {level}\nIVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    path.write_text(out + "\n" + end + after + ("" if after else "\n"))


# ---------------------------------------------------------------------------
# The ferry's landings and the hamlets' heal locations
# ---------------------------------------------------------------------------

def write_ferry_and_heal():
    path = ROOT / "data/maps/GulfTrireme/scripts.pory"
    text = path.read_text()
    text = re.sub(r"warp\(MAP_KIRRHA, \d+, \d+\)", f"warp(MAP_KIRRHA, {KIRRHA_LANDING[0]}, {KIRRHA_LANDING[1]})", text)
    text = re.sub(r"warp\(MAP_AIGION, \d+, \d+\)", f"warp(MAP_AIGION, {AIGION_LANDING[0]}, {AIGION_LANDING[1]})", text)
    path.write_text(text)
    path = ROOT / "src/data/heal_locations.json"
    data = json.loads(path.read_text())
    for h in data["heal_locations"]:
        spot = {"HEAL_LOCATION_KIRRHA": KIRRHA_HEAL, "HEAL_LOCATION_AIGION": AIGION_HEAL}.get(h["id"])
        if spot:
            h["x"], h["y"] = spot
            h["respawn_x"], h["respawn_y"] = spot
    path.write_text(json.dumps(data, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def blockers(g, spec, water_blocks=True):
    people = {(o["x"], o["y"]) for o in spec.objs if o.get("_kind") not in ("thicket", "rubble", "drum", "great",
                                                                             "web", "thornweb")}
    gates = {(o["x"], o["y"]) for o in spec.objs if o.get("_kind")}
    wet = {(x, y) for y in range(g.h) for x in range(g.w) if g.water[y, x]} if water_blocks else set()
    return people, gates, wet


def check_outdoor(g, spec, ends, forced_min=None):
    """ends: {label: [cells on the map's edge or at its warps]}; the first two
    named ends are the route's ends for forced grass."""
    problems = []
    people, gates, wet = blockers(g, spec)
    for o in spec.objs:
        if g.solid[o["y"], o["x"]] or g.water[o["y"], o["x"]]:
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} at ({o['x']},{o['y']}) "
                            "stands on a solid or wet cell")
    for edge, cols in spec._edges:
        y = 0 if edge == "up" else g.h - 1
        open_ = {x for x in range(g.w) if not g.solid[y, x] and not g.water[y, x]}
        if open_ != set(cols):
            problems.append(f"{edge} edge is open at {sorted(open_)}, wanted {sorted(cols)}")
    drums = {(o["x"], o["y"]) for o in spec.objs if o.get("_kind") == "drum"}
    blocked = frozenset(people | (gates - drums) | wet)     # the Girdle is in hand by the drum pass
    labels = list(ends)
    if drums and set(ends[labels[1]]) & K.reach(g, ends[labels[0]], frozenset(blocked | drums)):
        problems.append("the column drum doesn't close the road")
    a = ends[labels[0]]
    for lab in labels[1:]:
        if not set(ends[lab]) & K.reach(g, a, blocked):
            problems.append(f"can't walk from {labels[0]} to {lab} (gates shut)")
    allr = K.reach(g, [c for v in ends.values() for c in v], frozenset(people | wet))
    for o in spec.objs:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in allr for dx, dy in FACE.values()):
            kind = o.get("_kind")
            if o["graphics_id"].endswith("ITEM_BALL") and any(
                    g.water[y + dy, x + dx] for dx, dy in FACE.values() if 0 <= x + dx < g.w and 0 <= y + dy < g.h):
                continue                                   # an islet's item: the Conch
            problems.append(f"{o.get('local_id') or o['trainer_sight_or_berry_tree_id']} at ({x},{y}) "
                            f"can't be reached{' (' + kind + ')' if kind else ''}")
    for b in spec.bgs:
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and not g.solid[y, x]:
            problems.append(f"sign {b['script']} at ({x},{y}) is on walkable ground")
        spots = [(x, y + 1)] if b.get("player_facing_dir", "").endswith("NORTH") else \
            [(x, y - 1)] if b.get("player_facing_dir", "").endswith("SOUTH") else \
            [(x + dx, y + dy) for dx, dy in FACE.values()]
        if not any(p in allr for p in spots):
            problems.append(f"{b.get('script', b.get('item'))} at ({x},{y}) can't be read")
    pockets = [(x, y) for y in range(g.h) for x in range(g.w)
               if not g.solid[y, x] and not g.water[y, x] and (x, y) not in allr and (x, y) not in people | gates]
    wet_ok = set()
    for c in pockets:                                   # a pocket that touches water waits for the Conch or the Horn
        if c in wet_ok:
            continue
        comp = K.reach(g, [c], frozenset(people | wet)) & set(pockets)
        if any(g.water[y + dy, x + dx] for x, y in comp for dx, dy in FACE.values()
               if 0 <= x + dx < g.w and 0 <= y + dy < g.h):
            wet_ok |= comp
    rest = [c for c in pockets if c not in wet_ok]
    if rest:
        problems.append(f"walkable but cut off: {rest[:10]}")
    endcells = [c for v in ends.values() for c in v]
    for c in sorted(allr):
        if not set(endcells) & K.reach(g, [c], frozenset(people | wet)):
            problems.append(f"trap at {c}")
            break
    fg, mand = None, []
    if forced_min is not None:
        s_cells, n_cells = ends[labels[1]], ends[labels[0]]
        fg = min(v for v in (K.grass_cost(g, s_cells, n_cells, blocked), K.grass_cost(g, n_cells, s_cells, blocked))
                 if v is not None) if K.grass_cost(g, s_cells, n_cells, blocked) is not None else None
        if fg is None or fg < forced_min:
            problems.append(f"forced grass is {fg} < {forced_min}")
        for t in spec.trainers:
            cells = set(K.sight(g, t))
            cut = not set(n_cells) & K.reach(g, s_cells, frozenset(blocked | cells))
            if t["mandatory"] and not cut:
                problems.append(f"{t['name']}'s sight can be walked round")
            if cut:
                mand.append(t["name"])
            if len(cells) < t["sight"]:
                problems.append(f"{t['name']} sees {len(cells)} of {t['sight']} cells (blocked)")
            for stop in K.sight(g, t)[:-1]:
                if not set(n_cells) & K.reach(g, s_cells, frozenset((blocked - {(t['x'], t['y'])}) | {stop})):
                    problems.append(f"{t['name']} could stop at {stop} and block the road")
    stacked = {}
    for t in spec.trainers:
        for c in K.sight(g, t):
            stacked[c] = stacked.get(c, 0) + 1
    if any(v >= 3 for v in stacked.values()):
        problems.append("three sight lines on one cell")
    return problems, mand, fg


def walk_text(g, spec):
    objs = {(o["x"], o["y"]): o for o in spec.objs}
    sights = {c for t in spec.trainers for c in K.sight(g, t)}
    rows = ["    " + "".join(str(x % 10) for x in range(g.w))]
    for y in range(g.h):
        line = ""
        for x in range(g.w):
            o = objs.get((x, y))
            b = behavior(int(g.mt[y, x]))
            if o is not None:
                line += "T" if o["trainer_type"] != "TRAINER_TYPE_NONE" else \
                        "*" if o.get("_kind") else "o" if o["graphics_id"].endswith("ITEM_BALL") else "@"
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


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

def render(name, w, h, blocks, objs, out_dir, stem, views, secondary="gTileset_Skiron", walk=None, sights=()):
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
            spr, fw, fh = R5.sprite(gfx, facing)
        except (FileNotFoundError, KeyError, ValueError):
            continue
        flat.paste(spr, (o["x"] * 16 + 8 - fw // 2, o["y"] * 16 + 16 - fh), spr)
    flat.convert("RGB").resize((w * 32, h * 32), Image.NEAREST).save(out_dir / f"{stem}.png")
    if walk is not None:
        im = flat.resize((w * 32, h * 32), Image.NEAREST)
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d, c = ImageDraw.Draw(ov), 32
        for y in range(h):
            for x in range(w):
                col = walk(x, y)
                if col:
                    d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=col)
        for (sx, sy), col in sights:
            d.rectangle([sx * c + 6, sy * c + 6, sx * c + c - 7, sy * c + c - 7], outline=col, width=3)
        Image.alpha_composite(im, ov).convert("RGB").save(out_dir / f"{stem}_walk.png")
    shots = []
    for label, px, py in views:
        x0 = min(max(px - 7, 0), w - 15) * 16
        y0 = min(max(py - 5, 0), h - 10) * 16
        shots.append((label, flat.crop((x0, y0, x0 + 240, y0 + 160)).convert("RGB")))
    if shots:
        cols = 3
        rows = (len(shots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 248 + 8, rows * 178 + 8), (24, 24, 32))
        sd = ImageDraw.Draw(sheet)
        for i, (label, v) in enumerate(shots):
            x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
            sheet.paste(v, (x, y + 10))
            sd.text((x, y - 2), label, fill=(230, 230, 200))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / f"{stem}_views.png")


def walk_colors(g):
    def col(x, y):
        b = behavior(int(g.mt[y, x]))
        if g.water[y, x]:
            return (0, 60, 255, 50)
        if b.startswith("MB_JUMP"):
            return (0, 120, 255, 90)
        if g.solid[y, x]:
            return (255, 0, 0, 60)
        if b == "MB_TALL_GRASS":
            return (0, 255, 0, 45)
        return None
    return col


VIEWS = {
    R9: [("1 from Lebadeia", 12, 4), ("2 the three-ways", 14, 11), ("3 the Korykian crag", 25, 9),
         ("4 tier 1's stair", 12, 20), ("5 the shepherds' camp", 23, 26), ("6 Mnason's bend", 5, 28),
         ("7 the traverse", 15, 36), ("8 the lookout", 27, 37), ("9 the olive sea", 18, 50)],
    KIRRHA: [("1 from the olives", 15, 4), ("2 the falls and the outcamp", 7, 5), ("3 the plaza", 14, 11),
             ("4 Apollo's shrine", 21, 13), ("5 the beach", 10, 17), ("6 the quay", 15, 25)],
    AIGION: [("1 the landing", 15, 6), ("2 Helike's islet", 5, 5), ("3 the beach", 12, 12),
             ("4 the fishers' camp", 5, 15), ("5 the Homarion", 6, 22), ("6 the road south", 14, 27)],
    R11: [("1 from Aigion", 15, 4), ("2 the falls", 6, 9), ("3 the gorge", 8, 16), ("4 the nymphs' spring", 12, 20),
          ("5 the pool", 7, 28), ("6 the pass", 11, 34), ("7 the drums", 12, 40), ("8 to Styx Falls", 12, 47)],
    CAVE: [("1 the mouth", 16, 22), ("2 the great hall", 16, 11), ("3 the pool", 7, 11),
           ("4 the drum passage", 28, 13), ("5 the east grotto", 27, 19), ("6 the thornweb", 17, 4)],
}
STEM = {R9: "route9", KIRRHA: "kirrha", AIGION: "aigion", R11: "route11", CAVE: "korykian_cave"}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def outdoor(name, rows, w, h, props, specf, border, strip_top=False, strip_bottom=False, town=False,
            banks=False):
    g = build_grid(Grid(name, w, h, rows, strip_top, strip_bottom), props, town=town, banks=banks)
    spec = specf()
    blocks = write_layout(g, border)
    write_events(spec)
    return g, spec, blocks


def pine_border(g):
    s = g.cat["pine_tall"]
    return [s["ids"][1][0] | (1 << 10), s["ids"][1][1] | (1 << 10), s["ids"][2][0] | (1 << 10),
            s["ids"][2][1] | (1 << 10)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--rooms", action="store_true")
    args = ap.parse_args()
    if not K.CAT.exists():
        sys.exit(f"{K.CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    sea = [SEA | (1 << 12)] * 4
    probe = K.Grid("probe", 1, 1)
    pines = pine_border(probe)
    built = []
    g, s, b = outdoor(R9, P.ROUTE9, 32, 58, props_route9, spec_route9, pines, strip_top=True, banks=True)
    s._edges = [("up", R9_NORTH), ("down", R9_SOUTH)]
    built.append((g, s, b, {"Lebadeia": [(x, 0) for x in R9_NORTH], "Kirrha": [(x, g.h - 1) for x in R9_SOUTH],
                            "the cave": [CAVE_DOOR_R9]}, 8))
    g, s, b = outdoor(KIRRHA, P.KIRRHA, 28, 32, props_kirrha, spec_kirrha, sea, town=True)
    s._edges = [("up", R9_SOUTH)]
    built.append((g, s, b, {"Route 9": [(x, 0) for x in R9_SOUTH], "the quay": [KIRRHA_LANDING],
                            "the hostel": [(KIRRHA_DOOR[0], KIRRHA_DOOR[1] + 1)],
                            "the healer": [KIRRHA_HEAL]}, None))
    g, s, b = outdoor(AIGION, P.AIGION, 28, 32, props_aigion, spec_aigion, sea, town=True)
    s._edges = [("down", R11_NORTH)]
    built.append((g, s, b, {"Route 11": [(x, g.h - 1) for x in R11_NORTH], "the quay": [AIGION_LANDING],
                            "the Homarion": [(AIGION_DOOR[0], AIGION_DOOR[1] + 1)],
                            "the healer": [AIGION_HEAL]}, None))
    g, s, b = outdoor(R11, P.ROUTE11, 30, 52, props_route11, spec_route11, pines, strip_bottom=True,
                      banks=True)
    s._edges = [("up", R11_NORTH), ("down", R11_SOUTH)]
    built.append((g, s, b, {"Aigion": [(x, 0) for x in R11_NORTH], "Styx Falls": [(x, g.h - 1) for x in R11_SOUTH]},
                   8))
    cave_blocks, cave_walk, cave_water, cave_piece = cave_build()
    cave = spec_cave(cave_piece)
    write_events(cave)
    for spec in (spec_hostel(), spec_homarion()):
        write_events(spec)
    write_wild()
    write_trainers()
    write_ferry_and_heal()
    if args.rooms:
        import ergasteria_build as EB
        import limen_build
        sys.argv = sys.argv[:1]
        EB.build(limen_build.DOMOS, EB.parse_args())
    bad = 0
    for g, spec, blocks, ends, fmin in built:
        # the drum stands in Route 11's only road: it counts as a gate, not a person
        problems, mand, fg = check_outdoor(g, spec, ends, fmin)
        if args.walk:
            print(walk_text(g, spec))
        if args.render:
            sights = [(c, (255, 160, 0, 255) if t["mandatory"] else (255, 255, 120, 255))
                      for t in spec.trainers for c in K.sight(g, t)]
            render(g.name, g.w, g.h, blocks, spec.objects(), args.render, STEM[g.name], VIEWS[g.name],
                   walk=walk_colors(g), sights=sights)
        for p in problems:
            print(f"PROBLEM {spec.name}: {p}")
        print(f"{spec.name}: {g.w}x{g.h}, forced grass {fg}, {len(spec.trainers)} trainers, "
              f"{len(mand)} on the only road ({', '.join(mand)}), {len(problems)} problems")
        bad += len(problems)
    if args.render:
        render(CAVE, CAVE_W, CAVE_H, cave_blocks, cave.objects(), args.render, STEM[CAVE], VIEWS[CAVE],
               secondary="gTileset_CaveDark")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
