#!/usr/bin/env python3
"""Build Thyrsa's theater and its skene: layouts, borders, events, the crowd
table, and review renders.

  MAP_THYRSA_THEATER        (ThyrsaTheater)        40 x 34, aethos + gTileset_Theater
  MAP_THYRSA_THEATER_SKENE  (ThyrsaTheater_Skene)  oikos + gTileset_Skene

The theater is drawn in the GBA's oblique view: the skene (the stage building)
stands at the top with its painted front to the camera, the stage and its
colonnaded front below it, the orchestra's circle with the thymele, and the
cavea fanning out to the bottom of the map, where the top gate opens onto
Thyrsa's terrace. The cavea's cells come from tools/ichor/art/theater_cavea.py,
placed by signature from build/theater/catalog.json, so the map holds exactly
the cells that were painted.

The layout is the empty theater. For the Dionysia the engine fills the seats
from src/data/ichor_act2_theater.h, which this script writes: for every seat
cell, the crowd cell that replaces it, on its own pair's palette (theater_lib:
blocks 1 and 6 'low', 2 and 5 'mid', 3 and 4 'top'), so each pair's trance
pulse can stop on its own.

Writes data/layouts/<Map>/{map,border}.bin, their layouts.json entries, the
events in data/maps/<Map>/map.json, the crowd table, and renders:
  design/phase3/img/ThyrsaTheater.png          the map at 2x (the empty theater)
  design/phase3/img/ThyrsaTheater_Dionysia.png the night of the play, at 2x
  build/render/theater_review.png              collision and events marked
  build/render/theater_screens.png             GBA screens along the route

Usage: /usr/bin/python3 tools/ichor/maps/theater.py [--no-render]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))
import theater_cavea as V  # noqa: E402
import theater_lib as T  # noqa: E402

LAYOUTS = ROOT / "data/layouts/layouts.json"
IMG = ROOT / "design/phase3/img"
RENDER = ROOT / "build/render"
CROWD_H = ROOT / "src/data/ichor_act2_theater.h"

# aethos (primary) metatiles
GRASS, FLOWERS, BOULDER = 0x001, 0x004, 0x0E0
OLIVE_TOP, OLIVE_BOT, OLIVE_TIP = (0x1D4, 0x1D5), (0x1E4, 0x1E5), (0x1CE, 0x1CF)
CYPRESS_TOP, CYPRESS_BOT = 0x00E, 0x016
PINE = (0x01E, 0x01F, 0x026, 0x027)


def walk(mid):
    return mid | (3 << 12)


def block(mid):
    return mid | (1 << 10)


def sig(layers):
    return hashlib.sha1(V.key_of(layers)).hexdigest()[:16]


class Catalog:
    def __init__(self, d):
        path = ROOT / "build" / d / "catalog.json"
        if not path.exists():
            sys.exit(f"{path} is missing: run /usr/bin/python3 tools/ichor/art/theater_build.py")
        self.data = json.loads(path.read_text())
        self.by_key = {s["key"]: s for s in self.data["structures"]}

    def id(self, key, piece=None, cx=0, cy=0):
        s = self.by_key[key]
        if piece:
            cx, cy = s["names"][piece]
        return s["ids"][cy][cx]

    def struct(self, key):
        return self.by_key[key]


# ---------------------------------------------------------------------------
# The theater
# ---------------------------------------------------------------------------

# Where the people stand. (Columns 0-39, rows 0-33.)
SEAT_PLAYER = (18, 18)      # the front row, center: the player's seat
SEAT_ALETHEA = (17, 18)     # ... and Alethea beside them
SEAT_KLEON = (16, 17)       # Kleon, the front row to the left (the diagonal's first seat)
RESERVED = {SEAT_PLAYER, SEAT_ALETHEA, SEAT_KLEON}
HONEY = (22, 18)            # a front-row seat with a jar of Honey under it (hidden item)
OBOL = (0, 7)               # the west parodos's corner: a dropped obol (hidden item)

DOOR_IVY, DOOR_CROWN, DOOR_GOAT = (14, 5), (19, 5), (25, 5)   # each door's lower cell
BACK_DOOR = (30, 7)         # the skene's back door, in the east wing (warp 1)
GATE = ((19, 33), (20, 33))  # the top gate (warp 0, and 2)
THYMELE = (19, 12)
LOOM = (12, 6)              # the Fates' loom (props swapped in for the play)
KING = (21, 7)              # where the gold-masked king kneels
KLEON_EDGE = (22, 7)        # Kleon on the stage's edge, beat 33
VINE = (27, 6)              # the prop vine Silenos cuts
TORCHES = [(15, 9), (24, 9), (15, 15), (24, 15)]   # head cells; the foot is below


class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.cells = np.zeros((h, w), np.uint16)
        self.set = np.zeros((h, w), bool)

    def put(self, x, y, v, force=True):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        if self.set[y, x] and not force:
            return
        self.cells[y, x] = v
        self.set[y, x] = True

    def place(self, cat, key, x0, y0, walkmap=None):
        s = cat.struct(key)
        for cy in range(s["h"]):
            for cx in range(s["w"]):
                ch = (walkmap or s["walk"])[cy][cx]
                mid = s["ids"][cy][cx]
                self.put(x0 + cx, y0 + cy, block(mid) if ch == "X" else walk(mid))

    def solid(self, x, y):
        return bool(self.cells[y, x] & (1 << 10))


def tree_ok(g, x, y, w, h):
    return all(0 <= x + i < g.w and 0 <= y + j < g.h and not g.set[y + j, x + i]
               for j in range(h) for i in range(w))


def plant(g, cells, seed):
    """Trees, crags and flowers on the hill's grass: olives (2x2, their crown's
    tip in the cell above), stone pines, cypresses, boulders and anemones."""
    for (x, y) in sorted(cells, key=lambda c: (c[1], c[0])):
        if g.set[y, x]:
            continue
        k = V._hash(x, y, seed) % 100
        if k < 22 and tree_ok(g, x, y, 2, 2) and y >= 1 and tree_ok(g, x, y - 1, 2, 1):
            g.put(x, y - 1, walk(OLIVE_TIP[0]))
            g.put(x + 1, y - 1, walk(OLIVE_TIP[1]))
            g.put(x, y, block(OLIVE_TOP[0]))
            g.put(x + 1, y, block(OLIVE_TOP[1]))
            g.put(x, y + 1, block(OLIVE_BOT[0]))
            g.put(x + 1, y + 1, block(OLIVE_BOT[1]))
        elif k < 34 and tree_ok(g, x, y, 2, 2):
            for i, mid in enumerate(PINE):
                g.put(x + i % 2, y + i // 2, block(mid))
        elif k < 52 and tree_ok(g, x, y, 1, 2):
            g.put(x, y, block(CYPRESS_TOP))
            g.put(x, y + 1, block(CYPRESS_BOT))
        elif k < 58:
            g.put(x, y, block(BOULDER))
        elif k < 66:
            g.put(x, y, walk(FLOWERS))
        else:
            g.put(x, y, walk(GRASS))


def build_theater(cat):
    g = Grid(T.W, T.H)
    crowd = {}

    # --- the skene: wings, roof, front, doors, crane -------------------------
    def roof_row(x0, x1, y, row):
        for x in range(x0, x1 + 1):
            side = "L" if x == x0 else "R" if x == x1 else "M"
            g.put(x, y, block(cat.id("roof", f"{row}_{side}")))
    # the wings' hipped roofs, their ridges running back from the stage
    for x0 in (8, 29):
        for y in range(6):
            row = "top" if y == 0 else "eave" if y == 5 else "mid"
            for i, c in enumerate("LMR"):
                g.put(x0 + i, y, block(cat.id("wing_roof", f"{row}_{c}")))
    roof_row(11, 28, 0, "ridge")
    roof_row(11, 28, 1, "tiles")
    roof_row(11, 28, 2, "eave")
    # the god-machine stands on the roof, its arm out over the stage
    g.place(cat, "crane", 23, 0)
    # the cornice: masks, alternating
    for x in range(11, 29):
        g.put(x, 3, block(cat.id("frieze", "comic" if x % 2 else "tragic")))
    # the front: half-columns, painted panels and the three doors
    front = {11: "column", 12: "pinax_vine", 13: "column", 15: "column", 16: "wall", 17: "pinax_goat",
             18: "column", 21: "column", 22: "pinax_goat", 23: "wall", 24: "column", 26: "column",
             27: "pinax_vine", 28: "column"}
    for x, k in front.items():
        g.put(x, 4, block(cat.id("facade", f"{k}_0")))
        g.put(x, 5, block(cat.id("facade", f"{k}_1")))
    for key, (x, _), w in (("door_ivy", DOOR_IVY, 1), ("door_crown", DOOR_CROWN, 2), ("door_goat", DOOR_GOAT, 1)):
        for r in (0, 1):
            for c in range(w):
                g.put(x + c, 4 + r, block(cat.id(key, f"closed_{r}{c}")))
    # the wings' faces; the east one has the skene's back door
    g.place(cat, "wing_face", 8, 6)
    g.place(cat, "wing_door", 29, 6)

    # --- the stage and its front --------------------------------------------
    for x in range(11, 29):
        ph = "a" if x % 2 else "b"
        g.put(x, 6, walk(cat.id("stage", f"back_{ph}")))
        g.put(x, 7, walk(cat.id("stage", f"front_{ph}")))
    for x in range(11, 29):
        if x in (19, 20):
            k = "steps_L" if x == 19 else "steps_R"
            g.put(x, 8, walk(cat.id("proskenion", k)))
        elif x in (11, 28):
            g.put(x, 8, block(cat.id("proskenion", "end")))
        else:
            g.put(x, 8, block(cat.id("proskenion", "column" if x in (12, 15, 18, 21, 24, 27) else "panel")))

    # --- the cavea, the orchestra, the parodoi (cell by cell) -----------------
    cav = cat.data["cavea"]
    crw = cat.data["crowd"]
    for (cx, cy) in V.cavea_cells():
        if g.set[cy, cx]:
            continue
        le = V.paint_cell(cx, cy, False)
        mid = cav[sig(le)]
        if cy * 16 < T.CUT:
            ok = True      # the parodoi and the aisle's north edge
        else:
            ok = T.walk_cell(cx, cy)
        g.put(cx, cy, walk(mid) if ok else block(mid))
        lf = V.paint_cell(cx, cy, True)
        sf = sig(lf)
        if sf != sig(le) and (cx, cy) not in RESERVED:
            pair = T.pair_of_block(T.block_of_cell(cx, cy)) or "top"
            crowd[(cx, cy)] = crw[pair][sf]

    # the thymele at the orchestra's center
    g.place(cat, "thymele", *THYMELE)
    # torches round the orchestra (cold; the play lights them)
    for (x, y) in TORCHES:
        g.put(x, y, walk(cat.id("torch_cold_pave", "head")))
        g.put(x, y + 1, block(cat.id("torch_cold_pave", "foot")))

    # --- the top gate and the terrace ---------------------------------------
    g.place(cat, "gate", 18, 32)
    for x in list(range(12, 18)) + list(range(22, 28)):
        piece = "end" if x in (12, 27) else "wall"
        g.put(x, 33, block(cat.id("terrace_wall", piece)))

    # the hill round the skene and the terrace's corners: aethos grass and trees
    hill = [(x, y) for y in range(T.H) for x in range(T.W) if not g.set[y, x]]
    plant(g, hill, 5)
    return g, crowd


BORDER_THEATER = [PINE[0], PINE[1], PINE[2], PINE[3]]


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0", local_id=None, trainer=False,
        sight=0, item=None):
    e = {
        "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
        "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": item or str(sight), "script": script, "flag": flag,
    }
    if local_id:
        e = {"local_id": local_id, **e}
    return e


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def trigger(x, y, script, var="VAR_TEMP_0", value="0"):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": value,
            "script": script}


P = "OBJ_EVENT_GFX_ICHOR_"
TH = "ThyrsaTheater_EventScript_"
CAST = "FLAG_ICHOR_HIDE_DIONYSIA_CAST"


def theater_events(g):
    # where the play begins: the first step down from the promenade, at every
    # stair's top and at the promenade's ends by the parodoi (computed from the
    # cavea), so the workers sweeping inside are seen first
    stops = []
    for (cx, cy) in V.cavea_cells():
        if T.stair_cell(cx, cy) and T.cell_tier(cx, cy) == T.PROMENADE[0] - 1:
            stops.append((cx, cy))
    for x in (0, 1, T.W - 2, T.W - 1):
        stops.append((x, T.CUT // 16))
    ev = {
        "connections": None,
        "warp_events": [
            {"x": GATE[0][0], "y": GATE[0][1], "elevation": 3, "dest_map": "MAP_THYRSA_CITY", "dest_warp_id": "11"},
            {"x": BACK_DOOR[0], "y": BACK_DOOR[1], "elevation": 3, "dest_map": "MAP_THYRSA_THEATER_SKENE",
             "dest_warp_id": "0"},
            {"x": GATE[1][0], "y": GATE[1][1], "elevation": 3, "dest_map": "MAP_THYRSA_CITY", "dest_warp_id": "11"},
        ],
        "object_events": [
            # before the play: workers sweep the tiers and hang garlands (the city's
            # keeper turns the player away at the gate until the Mask Laurel)
            obj(P + "HARVESTER", 12, 31, TH + "Worker", "MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT", "FLAG_TEMP_1B",
                "LOCALID_THEATER_WORKER"),
            obj(P + "YOUTH_M", 8, 21, TH + "WorkerTiers", "MOVEMENT_TYPE_FACE_UP", "FLAG_TEMP_1B"),
            obj(P + "YOUTH_F", 33, 26, TH + "WorkerTiers", "MOVEMENT_TYPE_FACE_LEFT", "FLAG_TEMP_1B"),
            # the Dionysia's cast (beat 32): on stage and in the orchestra. The ones who
            # make an entrance during the play hide behind temp flags the map's
            # ON_TRANSITION sets; objects that change their look use OBJ_EVENT_GFX_VAR_n.
            obj(P + "HERALD", 20, 15, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_16",
                "LOCALID_THEATER_HERALD"),
            obj(P + "CHORUS_LEADER", 18, 13, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_ICHOR_HIDE_CHORUS_LEADER", "LOCALID_THEATER_CHORUS"),
            obj(P + "FATE_SPINNER", 11, 6, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", CAST, "LOCALID_THEATER_FATE_1"),
            obj(P + "FATE_MEASURER", 11, 7, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", CAST, "LOCALID_THEATER_FATE_2"),
            obj(P + "FATE_CUTTER", 13, 7, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", CAST, "LOCALID_THEATER_FATE_3"),
            obj(P + "BEE_WOMAN", 14, 7, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_17", "LOCALID_THEATER_BEE"),
            obj("OBJ_EVENT_GFX_ITEM_BALL", 15, 7, TH + "Jar", "MOVEMENT_TYPE_NONE", "FLAG_TEMP_18",
                "LOCALID_THEATER_JAR"),
            obj("OBJ_EVENT_GFX_VAR_1", KING[0], KING[1], TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_19",
                "LOCALID_THEATER_KING"),
            obj(P + "UNWOVEN_ACTOR", 20, 10, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_1A",
                "LOCALID_THEATER_ACTOR"),
            # in the seats
            obj("OBJ_EVENT_GFX_VAR_0", SEAT_ALETHEA[0], SEAT_ALETHEA[1], TH + "AletheaSeat", "MOVEMENT_TYPE_FACE_UP",
                CAST, "LOCALID_THEATER_ALETHEA"),
            obj("OBJ_EVENT_GFX_VAR_2", SEAT_KLEON[0], SEAT_KLEON[1], TH + "KleonSeat", "MOVEMENT_TYPE_FACE_UP",
                CAST, "LOCALID_THEATER_KLEON_SEAT"),
            # the masks that float off the cast's faces (shown only as the trance breaks)
            obj(P + "MASK", 14, 7, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_11", "LOCALID_THEATER_MASK_1"),
            obj(P + "MASK", KING[0], KING[1], TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_12",
                "LOCALID_THEATER_MASK_2"),
            obj(P + "MASK", 20, 10, TH + "Cast", "MOVEMENT_TYPE_FACE_DOWN", "FLAG_TEMP_13", "LOCALID_THEATER_MASK_3"),
            # Thespis at the palace door, and Silenos in the east parodos
            obj(P + "THESPIS", DOOR_CROWN[0], DOOR_CROWN[1] + 1, TH + "Thespis", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_TEMP_14", "LOCALID_THEATER_THESPIS"),
            obj(P + "SILENOS", 31, 8, TH + "Cast", "MOVEMENT_TYPE_FACE_LEFT", "FLAG_TEMP_15",
                "LOCALID_THEATER_SILENOS"),
            # beat 33: Kleon on the stage's edge, in the empty theater
            obj("OBJ_EVENT_GFX_VAR_3", KLEON_EDGE[0], KLEON_EDGE[1], TH + "KleonEmpty", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_ICHOR_HIDE_KLEON_THEATER", "LOCALID_THEATER_KLEON"),
            # after: a cleaner on the tiers
            obj(P + "ELDER_F", 13, 24, TH + "Cleaner", "MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT",
                "FLAG_ICHOR_HIDE_THEATER_CLEANER", "LOCALID_THEATER_CLEANER"),
        ],
        "coord_events": [trigger(x, y, TH + "TakeYourSeat", "VAR_ICHOR_DIONYSIA", "0") for (x, y) in stops]
        + [trigger(x, 8, TH + "KleonApproach", "VAR_TEMP_2", "1") for x in (19, 20)],
        "bg_events": [
            sign(THYMELE[0], THYMELE[1] + 1, TH + "Thymele", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(THYMELE[0] + 1, THYMELE[1] + 1, TH + "Thymele", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(DOOR_IVY[0], DOOR_IVY[1], TH + "StageDoor", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(DOOR_CROWN[0], DOOR_CROWN[1], TH + "StageDoor", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(DOOR_CROWN[0] + 1, DOOR_CROWN[1], TH + "StageDoor", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(DOOR_GOAT[0], DOOR_GOAT[1], TH + "StageDoor", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(9, 7, TH + "WingWindow", "BG_EVENT_PLAYER_FACING_NORTH"),
            # the Honey under the front row (Part 2), on a seat off the reserved three,
            # read from the orchestra's edge; the seat's cell has elevation 0
            {"type": "hidden_item", "x": HONEY[0], "y": HONEY[1], "elevation": 0,
             "item": "ITEM_HONEY", "flag": "FLAG_ICHOR_HIDDEN_THEATER_HONEY"},
            # an obol, a seat's price, dropped in the corner of the west parodos (polish pass)
            {"type": "hidden_item", "x": OBOL[0], "y": OBOL[1], "elevation": 3,
             "item": "ITEM_RELIC_COPPER", "flag": "FLAG_ICHOR_HIDDEN_THEATER_OBOL"},
        ],
    }
    return ev



# ---------------------------------------------------------------------------
# The skene: the backstage corridor, the prop room, the vestibule
# ---------------------------------------------------------------------------

SK_W, SK_H = 20, 12
# The doors' backs line up with the stage doors outside (theater x - 10).
SK_DOOR_IVY, SK_DOOR_CROWN, SK_DOOR_GOAT = (4, 2), (9, 2), (15, 2)
SK_RACK = (6, 1)            # the rack Thespis uses (2x2, rows 1-2)
SK_RACK2 = (12, 1)          # the second rack
SK_EXIT = (15, 11)          # the back door out to the east parodos (warp 0)
SK_ARCH = (4, 7)            # the prop room's arch (2 wide, rows 7-8)
SK_DOOR = (14, 7)           # the vestibule's doorway (2 wide, rows 7-8)
SK_SILENOS = (2, 9)         # Silenos's chest, in front of the girdle's peg
SK_GIRDLE = (2, 7)
SK_WINCH = (7, 7)
# oikos (primary); the void above the walls is the skene's own (oikos 0x000 is not drawn black)
OK_EXIT, OK_TERRA, OK_TERRA_CRACK, OK_TERRA_SHADE = 0x006, 0x008, 0x009, 0x00A
OK_AMPHORA, OK_CHEST, OK_STOOL, OK_LAMP_TOP, OK_LAMP_BASE = 0x043, 0x041, 0x040, 0x027, 0x02F


def build_skene(cat):
    g = Grid(SK_W, SK_H)
    OK_VOID = cat.id("void")
    for y in range(SK_H):
        g.put(0, y, block(OK_VOID))
        g.put(SK_W - 1, y, block(OK_VOID))
    for x in range(SK_W):
        g.put(x, 0, block(OK_VOID))

    def wall(x, y, piece):
        g.put(x, y, block(cat.id("wall", piece)))

    # the north wall: the doors' backs, the racks, lamps and posts
    north = {1: "post", 2: "plain", 3: "lamp", 5: "plain", 8: "post", 11: "post", 14: "plain",
             16: "lamp", 17: "plain", 18: "post"}
    for x, k in north.items():
        wall(x, 1, {"post": "post_upper", "plain": "upper", "lamp": "lamp_upper"}[k])
        wall(x, 2, {"post": "post_lower", "plain": "lower", "lamp": "lamp_lower"}[k])
    for key, (x, _), w in (("door_back_ivy", SK_DOOR_IVY, 1), ("door_back_crown", SK_DOOR_CROWN, 2),
                           ("door_back_goat", SK_DOOR_GOAT, 1)):
        for r in (0, 1):
            for c in range(w):
                g.put(x + c, 1 + r, block(cat.id(key, f"shut_{r}{c}")))
    for (x0, y0), key in ((SK_RACK, "rack_empty"), (SK_RACK2, "rack_empty")):
        for r in (0, 1):
            for c in (0, 1):
                g.put(x0 + c, y0 + r, block(cat.id(key, f"c{c}{r}")))
    # the corridor: planking, the row under the wall in shadow
    for y in (3, 4, 5):
        for x in range(1, SK_W - 1):
            ph = "a" if x % 2 else "b"
            g.put(x, y, walk(cat.id("floor", ph if y > 3 else f"shade_{ph}")), force=False)
    g.place(cat, "rail", 1, 4)
    g.place(cat, "chest_1", 3, 5)
    g.place(cat, "rail", 16, 4)
    g.place(cat, "barrel", 18, 4)
    # the inner wall: its top, its face, the arch and the doorway
    for x in range(1, SK_W - 1):
        g.put(x, 6, block(OK_VOID))
        wall(x, 7, "upper")
        wall(x, 8, "lower")
    for (x0, y0), pre in ((SK_ARCH, "arch"), (SK_DOOR, "door")):
        for c, side in ((0, "L"), (1, "R")):
            g.put(x0 + c, 6, walk(cat.id("floor", "shade_a" if c == 0 else "shade_b")))
            g.put(x0 + c, y0, walk(cat.id("openings", f"{pre}_{side}0")))
            g.put(x0 + c, y0 + 1, walk(cat.id("openings", f"{pre}_{side}1")))
    # the partition between the prop room and the vestibule
    for y in range(6, SK_H):
        g.put(10, y, block(OK_VOID))
    # the prop room: on its wall the girdle, the sickle, the crown of stars, the gold
    # mask, the winch; on its floor the chests, the wine jar, the lion skin
    g.place(cat, "girdle", SK_GIRDLE[0], SK_GIRDLE[1])
    g.place(cat, "sickle", 3, 7)
    g.place(cat, "crown_stars", 6, 7)
    g.place(cat, "winch_page", SK_WINCH[0], SK_WINCH[1])
    g.place(cat, "gold_mask", 9, 7)
    for y in (9, 10, 11):
        for x in range(1, 10):
            ph = "a" if x % 2 else "b"
            g.put(x, y, walk(cat.id("floor", ph if y > 9 else f"shade_{ph}")), force=False)
    g.place(cat, "chest_0", *SK_SILENOS)
    g.place(cat, "wine_jar", 1, 9)
    g.place(cat, "chest_1", 9, 9)
    g.place(cat, "lion_skin", 5, 11)
    # the vestibule: a terracotta floor by the back door, a lamp, a chest, an amphora
    for y in (9, 10, 11):
        for x in range(11, SK_W - 1):
            g.put(x, y, walk(OK_TERRA_SHADE if y == 9 else (OK_TERRA_CRACK if (x * 7 + y) % 9 == 0 else OK_TERRA)),
                  force=False)
    g.put(SK_EXIT[0], SK_EXIT[1], walk(OK_EXIT))
    g.put(11, 9, walk(OK_LAMP_TOP))
    g.put(11, 10, block(OK_LAMP_BASE))
    g.put(18, 9, block(OK_CHEST))
    g.put(18, 11, block(OK_AMPHORA))
    return g


SK = "ThyrsaTheater_Skene_EventScript_"


def skene_events():
    doors = [SK_DOOR_IVY, SK_DOOR_CROWN, (SK_DOOR_CROWN[0] + 1, SK_DOOR_CROWN[1]), SK_DOOR_GOAT]
    return {
        "connections": None,
        "warp_events": [
            {"x": SK_EXIT[0], "y": SK_EXIT[1], "elevation": 3, "dest_map": "MAP_THYRSA_THEATER",
             "dest_warp_id": "1"},
        ],
        "object_events": [
            # beat 32, backstage: Thespis at the rack, Silenos and Alethea with the player
            obj(P + "THESPIS", SK_RACK[0], 3, SK + "Thespis", "MOVEMENT_TYPE_FACE_UP",
                "FLAG_ICHOR_HIDE_THESPIS_SKENE", "LOCALID_SKENE_THESPIS"),
            obj(P + "SILENOS", 13, 4, SK + "SilenosWings", "MOVEMENT_TYPE_FACE_LEFT", "FLAG_TEMP_11",
                "LOCALID_SKENE_SILENOS_WINGS"),
            obj(P + "ALETHEA", 11, 5, SK + "AletheaWings", "MOVEMENT_TYPE_FACE_UP", "FLAG_TEMP_12",
                "LOCALID_SKENE_ALETHEA"),
            # beat 34: Silenos on his chest in the prop room
            obj(P + "SILENOS", SK_SILENOS[0], SK_SILENOS[1], SK + "Silenos", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_TEMP_13", "LOCALID_SKENE_SILENOS"),
            # the stagehand in the vestibule, after the play
            obj(P + "MAN", 13, 10, SK + "Stagehand", "MOVEMENT_TYPE_FACE_LEFT", "FLAG_TEMP_14",
                "LOCALID_SKENE_STAGEHAND"),
        ],
        "coord_events": [trigger(x, y, SK + "Entrance", "VAR_TEMP_1", "1") for (x, y) in doors]
        + [trigger(SK_EXIT[0], SK_EXIT[1] - 1, SK + "NotThatWay", "VAR_TEMP_1", "1")],
        "bg_events": [
            sign(SK_RACK[0], 2, SK + "Rack", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(SK_RACK[0] + 1, 2, SK + "Rack", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(SK_RACK2[0], 2, SK + "RackTwo", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(SK_RACK2[0] + 1, 2, SK + "RackTwo", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(3, 8, SK + "Sickle", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(6, 8, SK + "CrownOfStars", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(9, 8, SK + "GoldMask", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(SK_WINCH[0], 8, SK + "Winch", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(SK_WINCH[0] + 1, 8, SK + "Winch", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(SK_GIRDLE[0], 8, SK + "GirdlePeg", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(5, 11, SK + "LionSkin"),
            sign(6, 11, SK + "LionSkin"),
            sign(1, 10, SK + "WineJar"),
            sign(18, 5, SK + "Barrel"),
            sign(1, 5, SK + "Rail"),
            sign(2, 5, SK + "Rail"),
        ],
    }


def border_skene(cat):
    return [cat.id("void")] * 4


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def write_layout(layout_id, folder, g, border, primary, secondary):
    d = ROOT / "data/layouts" / folder
    d.mkdir(parents=True, exist_ok=True)
    g.cells.astype("<u2").tofile(d / "map.bin")
    np.array(border, "<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == layout_id:
            lay.update({"width": g.w, "height": g.h, "primary_tileset": primary, "secondary_tileset": secondary,
                        "border_filepath": f"data/layouts/{folder}/border.bin",
                        "blockdata_filepath": f"data/layouts/{folder}/map.bin"})
            break
    else:
        sys.exit(f"no layout {layout_id}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_events(folder, events, music, extra=None):
    path = ROOT / "data/maps" / folder / "map.json"
    m = json.loads(path.read_text())
    m["music"] = music
    m.update(extra or {})
    m.update(events)
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def write_crowd(crowd, slots):
    lines = [
        "// Ichor: the Dionysia's audience in Thyrsa's theater. Written by",
        "// tools/ichor/maps/theater.py; do not edit by hand.",
        "//",
        "// The layout is the empty theater. For the play, Ichor_TheaterFillSeats",
        "// (src/ichor_act2_scene.c) sets each cell below to its crowd metatile, which",
        "// is drawn on its pair's copy of the crowd's palette.",
        "",
        f"#define THEATER_PAL_CROWD       {slots['base']}",
        f"#define THEATER_PAL_PAIR_LOW    {slots['low']}",
        f"#define THEATER_PAL_PAIR_MID    {slots['mid']}",
        f"#define THEATER_PAL_PAIR_TOP    {slots['top']}",
        f"#define THEATER_CROWD_CELLS     {len(crowd)}",
        "",
        "struct IchorTheaterSeat { u8 x, y; u16 metatile; };",
        "",
        "static const struct IchorTheaterSeat sTheaterCrowd[THEATER_CROWD_CELLS] =",
        "{",
    ]
    for (x, y), mid in sorted(crowd.items(), key=lambda c: (c[0][1], c[0][0])):
        lines.append(f"    {{{x:2d}, {y:2d}, 0x{mid:03X}}},")
    lines.append("};")
    CROWD_H.write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

def renderer(primary, secondary):
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset(primary, syms)),
                           rm.Tileset(rm.resolve_tileset(secondary, syms)))


def render(name, g, primary, secondary, events, border, views, out_plain=None, scale=2, extra_cells=None):
    from PIL import Image, ImageDraw, ImageFont
    rm, r = renderer(primary, secondary)
    RENDER.mkdir(parents=True, exist_ok=True)
    blocks = g.cells.copy()
    for (x, y), mid in (extra_cells or {}).items():
        blocks[y, x] = (int(blocks[y, x]) & 0xFC00) | mid
    img = rm.render_blocks(r, blocks.ravel(), g.w)
    big = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    if out_plain:
        out_plain.parent.mkdir(parents=True, exist_ok=True)
        big.save(out_plain)
    s = 3
    rev = img.resize((img.width * s, img.height * s), Image.NEAREST).convert("RGBA")
    over = Image.new("RGBA", rev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    font = ImageFont.load_default(size=11)
    cell = 16 * s
    for y in range(g.h):
        for x in range(g.w):
            if blocks[y, x] & (1 << 10):
                d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=(255, 0, 0, 50))
    for e in events.get("object_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 4, y * cell + 4, x * cell + cell - 5, y * cell + cell - 5], outline=(40, 80, 255), width=3)
        d.text((x * cell + 2, y * cell + 2), e["script"].split("_")[-1][:8], fill=(255, 255, 255, 255), font=font,
               stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for e in events.get("warp_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 8, y * cell + 8, x * cell + cell - 9, y * cell + cell - 9], outline=(0, 255, 255), width=3)
    colors = {"sign": (255, 220, 0), "trigger": (255, 0, 255), "hidden_item": (0, 220, 120)}
    for e in events.get("bg_events", []) + events.get("coord_events", []):
        x, y = e["x"], e["y"]
        d.rectangle([x * cell + 12, y * cell + 12, x * cell + cell - 13, y * cell + cell - 13],
                    outline=colors[e["type"]], width=3)
    for i in range(max(g.w, g.h)):
        if i < g.w:
            d.text((i * cell + cell // 2 - 6, 0), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2,
                   stroke_fill=(0, 0, 0, 255))
        if i < g.h:
            d.text((2, i * cell + cell // 2 - 6), str(i), fill=(255, 255, 255, 255), font=font, stroke_width=2,
                   stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(rev, over).convert("RGB").save(RENDER / f"{name}_review.png")
    # GBA screens (15 x 10) round the given player positions
    pad = 8
    W, HH = g.w + 2 * pad, g.h + 2 * pad
    bigb = np.zeros((HH, W), np.uint16)
    for y in range(HH):
        for x in range(W):
            bigb[y, x] = border[((x - pad) & 1) + ((y - pad) & 1) * 2]
    bigb[pad:pad + g.h, pad:pad + g.w] = blocks & 0x3FF
    full = rm.render_blocks(r, bigb.ravel(), W)
    shots = []
    for (px, py) in views:
        x0, y0 = (px - 7 + pad) * 16, (py - 5 + pad) * 16 + 8
        shots.append(full.crop((x0, y0, x0 + 240, y0 + 160)).resize((480, 320), Image.NEAREST))
    cols = 3
    nrows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 488 + 8, nrows * 328 + 8), (24, 24, 32))
    for i, sh in enumerate(shots):
        sheet.paste(sh, (8 + (i % cols) * 488, 8 + (i // cols) * 328))
    sheet.save(RENDER / f"{name}_screens.png")
    return big


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()
    cat = Catalog("theater")
    g, crowd = build_theater(cat)
    ev = theater_events(g)
    write_layout("LAYOUT_THYRSA_THEATER", "ThyrsaTheater", g, BORDER_THEATER, "gTileset_Aethos", "gTileset_Theater")
    # ICHOR_STUB_MUSIC: Thyrsa's own cue is not composed; Emporion's stands in
    write_events("ThyrsaTheater", ev, "MUS_ICHOR_EMPORION",
                 {"map_type": "MAP_TYPE_CITY", "weather": "WEATHER_NONE", "show_map_name": True,
                  "allow_cycling": False})
    write_crowd(crowd, cat.data["palettes"])
    print(f"theater: {len(crowd)} seats fill for the Dionysia")
    kat = Catalog("skene")
    k = build_skene(kat)
    kev = skene_events()
    write_layout("LAYOUT_THYRSA_THEATER_SKENE", "ThyrsaTheater_Skene", k, border_skene(kat), "gTileset_Oikos",
                 "gTileset_Skene")
    # ICHOR_STUB_MUSIC: as the theater
    write_events("ThyrsaTheater_Skene", kev, "MUS_ICHOR_EMPORION",
                 {"map_type": "MAP_TYPE_INDOOR", "weather": "WEATHER_NONE", "show_map_name": False,
                  "allow_cycling": False})
    if not args.no_render:
        render("skene", k, "gTileset_Oikos", "gTileset_Skene", kev, border_skene(kat),
               [(9, 4), (5, 10), (15, 10)], IMG / "ThyrsaTheater_Skene.png", scale=2)
        views = [(19, 32), (19, 26), (19, 19), (19, 12), (19, 7), (5, 9), (30, 9), (6, 24), (33, 24)]
        render("theater", g, "gTileset_Aethos", "gTileset_Theater", ev, BORDER_THEATER, views,
               IMG / "ThyrsaTheater.png")
        render("theater_dionysia", g, "gTileset_Aethos", "gTileset_Theater", ev, BORDER_THEATER, views,
               IMG / "ThyrsaTheater_Dionysia.png", extra_cells=crowd)
        print(IMG / "ThyrsaTheater.png")


if __name__ == "__main__":
    main()
