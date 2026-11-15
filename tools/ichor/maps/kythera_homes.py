#!/usr/bin/env python3
"""Every interior on Kythera Isle and Melos (Act III, design/phase4/SCRIPT.md Part 2).

Skandeia's seven, Paphia's seven (not the Temple of Aphrodite), Myles's mill at
the Neraida falls, and Melos's three households (the boathouse has two floors).
Every house is a home and every interior is unique (design/MAP_DESIGN.md §2):
each room's shape, size and furniture are chosen for whoever lives or works
there, so the room shows the trade at a glance (the knapper's flakes and anvil
stone, the mill's millstone, the shipwright's keel).

Two kinds of room, as in the slice, each on the Aegean islands' own secondaries
(tools/ichor/art/interiors_lib.py; the pieces are catalogued in
design/phase4/ROOMS_aegean.md):
  - oikia homes and workshops are composed in oikia's style from oikia_art.py's
    pieces and the islands' own (aegean_skandeia.py, aegean_paphia.py,
    aegean_melos.py). Each town's homes share a secondary that holds exactly the
    cells they use: gTileset_OikiaSkandeia, gTileset_OikiaPaphia, and
    gTileset_OikiaMelos (Melos's households and Myles's mill, the country houses).
  - civic rooms (the Asclepeions and the Agoras) are grids of named metatiles,
    gTileset_Civic's and the islands' own (aegean_civic.py), on
    gTileset_CivicKythera.
gTileset_Oikia and gTileset_Civic are the slice's and are left as they are.

This script is the single source of each room's layout, of the tilesets above,
and of its map.json events (warps, people, readable things). It compiles the
four tilesets from the rooms, then writes, for each room:
  data/layouts/<Map>/{map,border}.bin and the layouts.json entry,
  data/maps/<Map>/map.json (scripts.pory is hand-written and never touched),
  the map's place in data/maps/map_groups.json, data/ichor_maps.inc and .gitignore,
  design/phase4/img/interiors/<Map>.png (3x) and <Map>_people.png (with the NPCs),
after checking that every warp, person and readable thing is reachable, that
bg events are read from the tile in front of them, and that no person blocks
the way to another. It also writes the pieces' reference sheets
(design/phase4/img/aegean_pieces.png, aegean_halls_pieces.png) and the generated
part of design/phase4/ROOMS_aegean.md: the tilesets' budgets, every piece, and
the metatile ids a script swaps (the orchard's tree in leaf).

The outdoor maps (MAP_KYTHERA_SKANDEIA and the rest) don't exist yet, so each
exit warp points at PLACEHOLDER until DOORS names the outdoor map's warp id.

  /usr/bin/python3 tools/ichor/maps/kythera_homes.py               # build everything
  /usr/bin/python3 tools/ichor/maps/kythera_homes.py --no-compile --review DIR
                                         # compose and check only; renders from the art
"""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))

import aegean_art as G  # noqa: E402
import aegean_civic as GC  # noqa: E402
import civic_tiles as ct  # noqa: E402
import interiors_lib as IL  # noqa: E402
import oikia_build as B  # noqa: E402
import render_map as RM  # noqa: E402

PRIMARY = "gTileset_Oikos"
# Each oikia room's secondary by town (a room may name another with tiles=...).
OIKIA_TILESETS = {
    "skandeia": "gTileset_OikiaSkandeia",
    "paphia": "gTileset_OikiaPaphia",
    "falls": "gTileset_OikiaMelos",
    "melos": "gTileset_OikiaMelos",
}
CIVIC_TILESET = "gTileset_CivicKythera"
IMG = ROOT / "design/phase4/img/interiors"
DOC = ROOT / "design/phase4/ROOMS_aegean.md"
WALK, SOLID = 0x3000, 0x0400

# The outdoor maps are the outdoor builder's. Until they exist every exit warp
# goes to PLACEHOLDER; once a town is built, add its door warp ids to DOORS
# (room name -> the outdoor map's warp id for that door) and rerun.
PLACEHOLDER = ("MAP_AKTI_TOWN", "0")
OUTDOOR = {
    "skandeia": "MAP_KYTHERA_SKANDEIA",
    "paphia": "MAP_KYTHERA_PAPHIA",
    "falls": "MAP_KYTHERA_NERAIDA_FALLS",
    "melos": "MAP_MELOS",
}
DOORS = {
    # MAP_KYTHERA_SKANDEIA's warps (tools/ichor/maps/skandeia.py)
    "KytheraSkandeia_Asclepeion": 0,
    "KytheraSkandeia_Agora": 1,
    "KytheraSkandeia_AxylosHouse": 2,
    "KytheraSkandeia_NikareteHouse": 3,
    "KytheraSkandeia_PerfumersHouse": 4,
    "KytheraSkandeia_DiversHouse": 5,
    "KytheraSkandeia_ShipwrightsHouse": 6,
    # MAP_MELOS's warps (tools/ichor/maps/melos.py)
    "Melos_Farmhouse": 0,
    "Melos_KnappersHouse": 1,
    "Melos_Boathouse": 2,
}

GROUPS = {
    "skandeia": "gMapGroup_IndoorKythera",
    "paphia": "gMapGroup_IndoorKythera",
    "falls": "gMapGroup_IndoorKythera",
    "melos": "gMapGroup_IndoorMelos",
}
MAPSEC = {
    "skandeia": "MAPSEC_KYTHERA_ISLE",
    "paphia": "MAPSEC_KYTHERA_ISLE",
    "falls": "MAPSEC_KYTHERA_ISLE",
    "melos": "MAPSEC_MELOS",
}
# MUS_ICHOR_KYTHERA and MUS_ICHOR_FOAM_ROAD (SCRIPT.md, Music) aren't written
# yet; the harbor theme stands in for the homes until they are.
HOME_MUSIC = "MUS_ICHOR_AKTI"

FACING = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
          "east": "BG_EVENT_PLAYER_FACING_EAST", "west": "BG_EVENT_PLAYER_FACING_WEST",
          "any": "BG_EVENT_PLAYER_FACING_ANY"}
DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
FACE_MOVE = {"down": "MOVEMENT_TYPE_FACE_DOWN", "up": "MOVEMENT_TYPE_FACE_UP",
             "left": "MOVEMENT_TYPE_FACE_LEFT", "right": "MOVEMENT_TYPE_FACE_RIGHT",
             "look": "MOVEMENT_TYPE_LOOK_AROUND", "wander": "MOVEMENT_TYPE_WANDER_AROUND"}
WARP_BEHAVIORS = {"MB_SOUTH_ARROW_WARP", "MB_NON_ANIMATED_DOOR"}


def obj(gfx, x, y, face, script, local_id=None, flag="0", rng=(0, 0)):
    """An object event: gfx is OBJ_EVENT_GFX_<gfx> (or a full constant)."""
    if not gfx.startswith("OBJ_EVENT_GFX_"):
        gfx = "OBJ_EVENT_GFX_" + gfx
    return {"gfx": gfx, "x": x, "y": y, "face": face, "script": script,
            "local_id": local_id, "flag": flag, "range": rng}


def bg(x, y, facing, script):
    """A bg event on (x, y), read by a player facing `facing`."""
    return {"x": x, "y": y, "facing": facing, "script": script}


# ==========================================================================
# The rooms. Each: name (the map's folder), title, town, kind, and either an
# oikia spec (floor, wall, grid, rugs, stamps) or a civic build function, plus
# its events. Exit warps go to the town; "links" are warps between this
# project's own maps (the boathouse's stairs). "solid" cells are blocked after
# composing (a tank, a ladder nobody climbs) and usually carry a bg event.
# ==========================================================================

ROOMS = []


def room(**kw):
    kw.setdefault("rugs", [])
    kw.setdefault("objects", [])
    kw.setdefault("bgs", [])
    kw.setdefault("coords", [])
    kw.setdefault("links", [])
    kw.setdefault("solid", [])
    kw.setdefault("music", HOME_MUSIC)
    ROOMS.append(kw)
    return kw


SK = "KytheraSkandeia"
PA = "KytheraPaphia"

# --------------------------------------------------------------------------
# Skandeia, the harbor: white cubes with blue doors, so its homes take the
# Aegean-blue dado. Their pieces are aegean_skandeia.py's.
# --------------------------------------------------------------------------

# Axylos keeps the old law: one big room that is almost all table, a board on
# trestles that seats twelve with benches down both sides (the bad guests sit on
# them), the hearth at the end with a bronze pot that's never cold, nets and a
# single oar on the wall, a shelf of more bowls than one man could need, and a
# peg with an empty goat's tether.
room(
    name=f"{SK}_AxylosHouse", title="Axylos's house, Skandeia", town="skandeia", kind="oikia",
    floor="terracotta", wall="blue",
    grid=[
        "WWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWW",
        "..............",
        "..............",
        "..............",
        "..............",
        "..............",
        "#.............",
        "##............",
    ],
    rugs=[("blue", 9, 7, 3, 2)],
    stamps=[
        ("nets", 0, 0), ("oar", 2, 0), ("window", 3, 0), ("bowl_shelf", 5, 0), ("window", 7, 0),
        ("tether", 9, 0), ("herbs", 10, 0), ("soot", 11, 0), ("hearth", 11, 2), ("pots", 13, 2),
        ("bench_l", 3, 4), ("bench_m", 4, 4), ("bench_m", 5, 4), ("bench_m", 6, 4), ("bench_m", 7, 4),
        ("bench_r", 8, 4),
        ("board_l", 3, 5), ("board_bones", 4, 5), ("board_bowls", 5, 5), ("board_jug", 6, 5),
        ("board_bones", 7, 5), ("board_r", 8, 5),
        ("bench_l", 3, 6), ("bench_m", 4, 6), ("bench_m", 5, 6), ("bench_m", 6, 6), ("bench_m", 7, 6),
        ("bench_r", 8, 6),
        ("pithos", 0, 4), ("fish_basket", 1, 3), ("kline", 11, 5), ("amphora_plain", 13, 5),
        ("pots", 1, 6), ("fish_basket", 12, 7),
        ("mat", 6, 8),
    ],
    warps=[(6, 8), (7, 8)],
    objects=[
        obj("ICHOR_ELDER_M", 9, 5, "left", f"{SK}_AxylosHouse_EventScript_Axylos", "LOCALID_SKANDEIA_AXYLOS"),
        obj("ICHOR_TITAN_GRUNT", 4, 4, "down", f"{SK}_AxylosHouse_EventScript_Guest",
            "LOCALID_SKANDEIA_OCHROS", "FLAG_ICHOR_BAD_GUESTS_GONE"),
        obj("ICHOR_TITAN_GRUNT", 7, 6, "up", f"{SK}_AxylosHouse_EventScript_Guest",
            "LOCALID_SKANDEIA_PSEPHOS", "FLAG_ICHOR_BAD_GUESTS_GONE"),
        obj("ICHOR_ALETHEA", 5, 8, "up", f"{SK}_AxylosHouse_EventScript_Alethea",
            "LOCALID_SKANDEIA_ALETHEA", "FLAG_ICHOR_BAD_GUESTS_GONE"),
    ],
    bgs=[
        bg(11, 3, "north", f"{SK}_AxylosHouse_EventScript_Hearth"),
        bg(12, 3, "north", f"{SK}_AxylosHouse_EventScript_Hearth"),
        bg(5, 1, "north", f"{SK}_AxylosHouse_EventScript_Bowls"),
        bg(6, 1, "north", f"{SK}_AxylosHouse_EventScript_Bowls"),
        bg(9, 1, "north", f"{SK}_AxylosHouse_EventScript_Tether"),
    ],
)

# Skyllias, a sponge diver gone gray, and his daughter Bathykleia, who dives now.
# A cool stone room: sponges hang drying from every beam, the bronze horse from
# a wreck in its niche, a basket of black urchins, the long bench where sponges
# are beaten, stone weights by the door, and the tank sunk in the floor where
# Ankyra hammers. The bottom-right corner is the street's rock, cut away.
room(
    name=f"{SK}_DiversHouse", title="The divers' house, Skandeia", town="skandeia", kind="oikia",
    floor="flags", wall="blue",
    grid=[
        "WWWWWWWWWWWW",
        "WWWWWWWWWWWW",
        "............",
        "............",
        "............",
        "............",
        "........####",
        "........####",
    ],
    stamps=[
        ("sponges", 0, 0), ("sponges_b", 1, 0), ("nets", 2, 0), ("window", 4, 0), ("sponges", 5, 0),
        ("niche_horse", 6, 0), ("trident", 7, 0), ("window", 8, 0), ("sponges_b", 9, 0),
        ("sponges", 10, 0), ("sponges_b", 11, 0),
        ("urchins", 4, 3), ("sponge_bench", 1, 4), ("tank", 8, 3),
        ("kline", 4, 6), ("amphora_plain", 7, 6), ("fish_basket", 6, 2),
        ("diving_weights", 0, 7), ("diving_weights", 3, 7), ("diving_weights", 0, 6),
        ("mat", 1, 7),
    ],
    warps=[(1, 7), (2, 7)],
    objects=[
        obj("ICHOR_ELDER_M", 3, 2, "down", f"{SK}_DiversHouse_EventScript_Skyllias"),
        obj("ICHOR_DIVER", 7, 4, "right", f"{SK}_DiversHouse_EventScript_Bathykleia"),
        dict(obj("SPECIES(TELKANVIL)", 9, 4, "down", f"{SK}_DiversHouse_EventScript_Ankyra",
                 "LOCALID_SKANDEIA_ANKYRA", "FLAG_ICHOR_TRADED_TELKANVIL"), on_furniture=True),
    ],
    bgs=[
        bg(10, 4, "west", f"{SK}_DiversHouse_EventScript_Tank"),
        bg(4, 3, "north", f"{SK}_DiversHouse_EventScript_Urchins"),
    ],
)

# Euodia presses rose and myrtle oil for the goddess's altars. A narrow, high
# room that smells of roses: the copper still on the hearth, shelves of little
# alabaster bottles, the beam press, petals drying on cloths on every flat
# surface including the bed, and one window, its shutters barred.
room(
    name=f"{SK}_PerfumersHouse", title="The perfumer's house, Skandeia", town="skandeia", kind="oikia",
    floor="terracotta", wall="red",
    grid=[
        "WWWWWWW",
        "WWWWWWW",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
    ],
    rugs=[("red", 1, 5, 3, 2)],
    stamps=[
        ("herbs", 0, 0), ("soot", 1, 0), ("hearth_still", 1, 2), ("alabaster_shelf", 3, 0),
        ("window_shut", 5, 0), ("herbs", 6, 0), ("amphora_plain", 0, 3),
        ("press", 4, 3),
        ("rose_cloth", 0, 5), ("rose_cloth_b", 0, 6), ("rose_cloth", 6, 6), ("rose_cloth_b", 5, 6),
        ("kline_petals", 4, 7), ("myrtle", 1, 8), ("amphora", 6, 8),
        ("mat", 2, 9),
    ],
    warps=[(2, 9), (3, 9)],
    objects=[
        obj("ICHOR_WOMAN", 3, 3, "down", f"{SK}_PerfumersHouse_EventScript_Euodia"),
    ],
    bgs=[
        bg(1, 3, "north", f"{SK}_PerfumersHouse_EventScript_Still"),
        bg(2, 3, "north", f"{SK}_PerfumersHouse_EventScript_Still"),
        bg(3, 1, "north", f"{SK}_PerfumersHouse_EventScript_Bottles"),
        bg(4, 1, "north", f"{SK}_PerfumersHouse_EventScript_Bottles"),
        bg(5, 1, "north", f"{SK}_PerfumersHouse_EventScript_Window"),
        bg(4, 4, "north", f"{SK}_PerfumersHouse_EventScript_Press"),
    ],
)

# Nikarete mends nets. Two rooms: the front one all loom and nets, the back one
# her grandson's, kept as he left it: the narrow bed still made, a slingshot on
# a nail, the clay Titan helmet he made as a child, painted badly gold, and a
# window on the empty slips. After the climax Lithos sits by his bed.
room(
    name=f"{SK}_NikareteHouse", title="Nikarete's house, Skandeia", town="skandeia", kind="oikia",
    floor="boards", wall="blue",
    grid=[
        "###WWWWWWW",
        "###WWWWWWW",
        "###.......",
        "###.......",
        "###.......",
        "WWWW..WWWW",
        "WWWW..WWWW",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
    ],
    rugs=[("blue", 3, 9, 4, 2)],
    stamps=[
        # the back room, the boy's
        ("niche", 3, 0), ("chest", 4, 1), ("window", 6, 0), ("slingshot", 7, 0), ("helmet_shelf", 8, 0),
        ("bed_narrow", 7, 3), ("stool", 4, 4), ("kalathos", 9, 4),
        # the front room: the divider is its back wall
        ("loom", 1, 5), ("nets", 6, 5), ("nets", 8, 5),
        ("kalathos", 3, 8), ("fish_basket", 8, 8), ("fish_basket", 9, 9), ("table_round", 8, 10),
        ("stool", 7, 10), ("pithos", 1, 9),
        ("mat", 4, 11),
    ],
    warps=[(4, 11), (5, 11)],
    objects=[
        obj("ICHOR_ELDER_F", 3, 7, "left", f"{SK}_NikareteHouse_EventScript_Nikarete"),
        obj("ICHOR_YOUTH_M", 6, 4, "down", f"{SK}_NikareteHouse_EventScript_Lithos",
            "LOCALID_SKANDEIA_LITHOS", "FLAG_TEMP_1"),
    ],
    bgs=[
        bg(8, 1, "north", f"{SK}_NikareteHouse_EventScript_Helmet"),
        bg(6, 1, "north", f"{SK}_NikareteHouse_EventScript_Window"),
        bg(7, 3, "south", f"{SK}_NikareteHouse_EventScript_Bed"),
        bg(1, 7, "north", f"{SK}_NikareteHouse_EventScript_Loom"),
        bg(2, 7, "north", f"{SK}_NikareteHouse_EventScript_Loom"),
    ],
)

# Phereklos, the shipwright with no ships. A timber shed with his house at the
# back, open on the slip side: a half-built keel on trestles on the slip, adzes
# and augers on the wall, a model of the kind of ship his family is blamed for,
# his bed and chest in the corner, curls of shavings ankle-deep, and in the
# middle a barrel for a table with a bowl of knucklebones on it.
room(
    name=f"{SK}_ShipwrightsHouse", title="Phereklos's yard, Skandeia", town="skandeia", kind="oikia",
    floor="boards", wall="blue",
    grid=[
        "WWWWWWWWWWW####",
        "WWWWWWWWWWW####",
        "...............",
        "...............",
        "...............",
        "...............",
        "...............",
        "...............",
        "...............",
    ],
    stamps=[
        ("oar", 0, 0), ("augers", 1, 0), ("adzes", 2, 0), ("adzes", 3, 0), ("boat", 4, 0),
        ("window", 6, 0), ("chest", 8, 1), ("herbs", 10, 0),
        ("keel", 11, 2),
        ("kline", 8, 4), ("lampstand", 10, 4),
        ("barrel_bones", 5, 5), ("stool", 4, 5), ("stool", 5, 6),
        ("amphora_plain", 1, 4), ("pithos", 1, 6),
        ("shavings", 11, 4), ("shavings", 13, 4), ("shavings_b", 12, 4), ("shavings_b", 14, 4),
        ("shavings_c", 10, 3), ("shavings_b", 12, 5), ("shavings_c", 14, 5), ("shavings", 11, 5),
        ("shavings_c", 13, 6), ("shavings_c", 9, 7), ("shavings_c", 3, 3), ("shavings_c", 7, 6),
        ("mat", 6, 8),
    ],
    warps=[(6, 8), (7, 8)],
    objects=[
        obj("ICHOR_MAN", 6, 5, "left", f"{SK}_ShipwrightsHouse_EventScript_Phereklos"),
    ],
    bgs=[
        bg(4, 1, "north", f"{SK}_ShipwrightsHouse_EventScript_Model"),
        bg(5, 1, "north", f"{SK}_ShipwrightsHouse_EventScript_Model"),
        bg(3, 1, "north", f"{SK}_ShipwrightsHouse_EventScript_Tools"),
    ],
)


def civic_walls(r, kit, x0=0, x1=None):
    """The back wall (two rows, with its ends) and the shadowed floor row."""
    x1 = r.w - 1 if x1 is None else x1
    n = x1 - x0 + 1
    r.row(0, x0, [f"{kit}_wall_top_l"] + [f"{kit}_wall_top"] * (n - 2) + [f"{kit}_wall_top_r"])
    r.row(1, x0, [f"{kit}_wall_l"] + [f"{kit}_wall"] * (n - 2) + [f"{kit}_wall_r"])


def asc_floor(x, y):
    return "asc_floor_a" if (x + y) % 2 == 0 else "asc_floor_b"


def asc_shadow_row(r, y=2, x0=0, x1=None):
    x1 = r.w - 1 if x1 is None else x1
    for x in range(x0, x1 + 1):
        r.set(x, y, "asc_floor_a_sh" if (x + y) % 2 == 0 else "asc_floor_b_sh")


def checker(name, x, y):
    """name, or name_b on the checker's cream slabs."""
    return name + ("_b" if (x + y) % 2 == 1 else "")


def asc_healer(r, hx, x0, x1):
    """The healer's counter, as the Akti Asclepeion has it relative to the healer
    at (hx, 2): the spring basin at hx-2..hx-1 where the heal animation puts the
    balls, the rod of Asclepius above the healer, the counter from x0 to x1 and
    its MB_COUNTER front on row 3."""
    r.put("asc_relief", hx, 0, 1, 2)
    r.put("asc_basin", hx - 2, 1, 2, 2)
    r.set(x0, 2, "asc_counter_l")
    r.set(hx, 2, "asc_counter_staff")
    for x in range(hx + 1, x1):
        r.set(x, 2, "asc_counter_m")
    r.set(x1, 2, "asc_counter_r")
    r.row(3, x0, ["asc_counter_front_l"] + ["asc_counter_front_m"] * (x1 - x0 - 1) + ["asc_counter_front_r"])


# Skandeia's Asclepeion: a harbor one, long and low. A wide window onto the quay,
# and under it the stone bath in the floor where sailors soak their hands, fed
# by sea water through a channel from the inlet in the wall; the Pithos a tall
# jar by the window; couches for the sailors; nets drying along the cornice
# (the healer's husband had nowhere else to put them this week); the healer's
# Panacoil curled on the counter.
def skandeia_asclepeion():
    r = Civic(19, 8, asc_floor)
    civic_walls(r, "asc")
    asc_shadow_row(r)
    asc_healer(r, 5, 2, 8)
    r.put("asc_votive_wall", 6, 1, 2, 1)
    r.put("asc_votive_counter", 6, 2, 2, 1)
    r.put("asc_seawin", 10, 0, 3, 2)                # the window onto the quay
    r.set(10, 2, checker("asc_bath_l", 10, 2))      # the hand-bath under it
    r.set(11, 2, checker("asc_bath_m", 11, 2))
    r.set(12, 2, checker("asc_bath_r", 12, 2))
    r.set(13, 1, "asc_inlet")                       # the sea comes in here
    r.set(13, 2, checker("asc_channel", 13, 2))
    r.put("asc_jar", 14, 1, 1, 2)
    r.put("asc_pithos", 15, 0, 2, 3)
    r.put("asc_jar", 17, 1, 1, 2)
    r.put("asc_nets_hung", 0, 0, 2, 2)              # nets on the cornice
    r.put("asc_nets", 7, 0, 2, 1)
    r.put("asc_nets", 17, 0, 2, 1)
    r.put_checkered("asc_bench", 11, 4, 2, 1)       # the bathers' bench
    r.put_checkered("asc_column", 3, 4, 1, 3)
    r.put_checkered("asc_column", 14, 4, 1, 3)
    r.put_checkered("asc_brazier", 6, 5, 1, 2)
    r.put_checkered("asc_brazier", 12, 5, 1, 2)
    r.put_checkered("asc_kline", 0, 4, 2, 2)
    r.put_checkered("asc_kline", 16, 5, 2, 2)
    r.put_checkered("asc_snake", 1, 7)
    r.put_checkered("asc_mat", 9, 7, single=True)
    return r


room(
    name=f"{SK}_Asclepeion", title="The Asclepeion, Skandeia", town="skandeia", kind="civic",
    build=skandeia_asclepeion, music="MUS_ICHOR_ASCLEPEION",
    warps=[(9, 7)],
    objects=[
        obj("ICHOR_HEALER", 5, 2, "down", f"{SK}_Asclepeion_EventScript_Healer", "LOCALID_SKANDEIA_HEALER"),
        dict(obj("SPECIES(PANACOIL)", 8, 2, "down", f"{SK}_Asclepeion_EventScript_Panacoil"),
             on_furniture=True),
    ],
    bgs=[
        bg(15, 2, "north", f"{SK}_Asclepeion_EventScript_Pithos"),
        bg(16, 2, "north", f"{SK}_Asclepeion_EventScript_Pithos"),
        bg(11, 2, "north", f"{SK}_Asclepeion_EventScript_Bath"),
        bg(12, 2, "north", f"{SK}_Asclepeion_EventScript_Bath"),
    ],
)


# Teukros sells rope, oil, myrtle and Frankincense in a rope-and-sailcloth hall,
# from half an old boat stood up as a counter, its painted eye still on the bow:
# Frankincense in jars on the high shelves under the dove carved in the beam,
# myrtle bundles and sailcloth from the beam, coils of rope, oil jars by the posts.
def skandeia_agora():
    r = Civic(11, 9, "ago_floor")
    civic_walls(r, "ago")
    r.row(2, 0, ["ago_floor_sh"] * 11)
    r.put("ago_incense", 1, 0, 2, 3)
    r.put("ago_herbs", 3, 0, 1, 2)
    r.put("ago_herbs", 4, 0, 1, 2)
    r.put("ago_cloth_blue", 5, 0, 1, 2)
    r.put("ago_awning", 6, 0, 3, 2)
    r.row(2, 5, ["ago_boat_l", "ago_boat_m", "ago_boat_staff", "ago_boat_m2", "ago_boat_r"])
    r.row(3, 5, [f"ago_boat_front_{i}" for i in range(5)])
    r.put("ago_cloth_saffron", 9, 0, 1, 2)
    r.put("ago_amphora", 10, 3, 1, 2)
    r.put("ago_column", 2, 5, 1, 3)
    r.put("ago_column", 8, 5, 1, 3)
    r.put("ago_amphora", 3, 6, 1, 2)
    r.put("ago_jar", 7, 6, 1, 2)
    r.put("ago_jar", 0, 7, 1, 2)
    r.set(0, 3, "ago_rope")
    r.set(0, 4, "ago_rope_b")
    r.set(10, 6, "ago_rope")
    r.set(4, 4, "ago_rope_b")
    r.set(10, 8, "ago_basket_olives")
    r.set(5, 8, "ago_mat")
    return r


room(
    name=f"{SK}_Agora", title="The Agora, Skandeia", town="skandeia", kind="civic",
    build=skandeia_agora, music="MUS_ICHOR_AGORA",
    warps=[(5, 8)],
    objects=[
        obj("ICHOR_MERCHANT", 7, 2, "down", f"{SK}_Agora_EventScript_Teukros"),
    ],
    bgs=[
        bg(1, 2, "north", f"{SK}_Agora_EventScript_Frankincense"),
        bg(2, 2, "north", f"{SK}_Agora_EventScript_Frankincense"),
    ],
)


# --------------------------------------------------------------------------
# Paphia, the temple town: white houses with rose-pink doorframes, so its homes
# take the warm red dado. Their pieces are aegean_paphia.py's.
# --------------------------------------------------------------------------

# Peristera keeps the temple's doves. A round tower house: her stove and bed
# below, nesting holes all round the wall with doves looking out, the ladder up
# through the hole to the nesting floor, feathers on everything, and by the
# stove a wool basket with one egg in it that is not a dove's.
room(
    name=f"{PA}_Dovecote", title="The dovecote, Paphia", town="paphia", kind="oikia",
    floor="flags", wall="red",
    grid=[
        "#WWWWWWWW#",
        "#WWWWWWWW#",
        "#........#",
        "..........",
        "..........",
        "..........",
        "..........",
        "#........#",
        "##......##",
    ],
    rugs=[("red", 3, 5, 2, 2)],
    stamps=[
        ("pigeonholes", 1, 0), ("soot", 2, 0), ("hearth", 2, 2), ("pigeonholes_b", 4, 0),
        ("window", 5, 0), ("pigeonholes", 6, 0), ("ladder", 7, 0), ("pigeonholes_b", 8, 0),
        ("egg_basket", 4, 3), ("pithos", 8, 3), ("pots", 1, 4),
        ("kline", 6, 5), ("stool", 2, 6), ("doves", 0, 5), ("doves", 8, 6),
        ("feathers", 6, 3), ("feathers", 3, 7), ("feathers", 1, 3), ("feathers", 7, 7),
        ("mat", 4, 8),
    ],
    solid=[(7, 2)],
    warps=[(4, 8), (5, 8)],
    objects=[
        obj("ICHOR_ELDER_F", 5, 3, "down", f"{PA}_Dovecote_EventScript_Peristera"),
    ],
    bgs=[
        bg(4, 3, "north", f"{PA}_Dovecote_EventScript_Basket"),
        bg(7, 2, "north", f"{PA}_Dovecote_EventScript_Ladder"),
        bg(2, 3, "north", f"{PA}_Dovecote_EventScript_Stove"),
        bg(3, 3, "north", f"{PA}_Dovecote_EventScript_Stove"),
    ],
)

# Lysis, a shy young potter, and his sister. The workshop: the kick-wheel by the
# door, the beehive kiln (his Himerow sleeps on its warm top), shelves of
# perfume flasks drying, every one with the same little painted fish, pots
# everywhere, a heap of fish bones nobody has thrown away, and a ladder up to
# the beds. The left part of the house is older and its wall stands forward.
room(
    name=f"{PA}_PottersHouse", title="The potter's house, Paphia", town="paphia", kind="oikia",
    floor="terracotta", wall="red",
    grid=[
        "###WWWWWWWWW",
        "###WWWWWWWWW",
        "WWW.........",
        "WWW.........",
        "............",
        "............",
        "............",
        "............",
    ],
    stamps=[
        ("ladder", 1, 2), ("flask_shelf", 4, 0), ("jar_shelf", 6, 0), ("soot", 8, 0),
        ("kiln", 8, 2), ("window", 11, 0), ("pithos", 11, 3),
        ("fish_bones", 0, 4), ("kick_wheel", 0, 6), ("stool", 1, 6),
        ("pots", 6, 4), ("pots", 7, 5), ("amphora", 11, 6), ("amphora_plain", 9, 6), ("pots", 5, 6),
        ("mat", 2, 7),
    ],
    solid=[(1, 4)],
    warps=[(2, 7), (3, 7)],
    objects=[
        obj("ICHOR_YOUTH_M", 4, 4, "down", f"{PA}_PottersHouse_EventScript_Lysis"),
        dict(obj("SPECIES(HIMEROW)", 9, 2, "down", f"{PA}_PottersHouse_EventScript_Pothos",
                 "LOCALID_PAPHIA_POTHOS", "FLAG_ICHOR_TRADED_HIMEROW"), on_furniture=True),
    ],
    bgs=[
        bg(4, 1, "north", f"{PA}_PottersHouse_EventScript_FishFlasks"),
        bg(5, 1, "north", f"{PA}_PottersHouse_EventScript_FishFlasks"),
        bg(1, 4, "north", f"{PA}_PottersHouse_EventScript_Ladder"),
        bg(8, 3, "north", f"{PA}_PottersHouse_EventScript_Kiln"),
    ],
)


# Paphia's Asclepeion is built round an open courtyard full of roses: the
# counter on the shady side, beds under a colonnade on the other, a rose hedge
# at the back of the court, a freestanding fountain the doves bathe in, and
# Panacoil asleep in the rose bed.
def paphia_asclepeion():
    court = {(6, 3), (7, 3), (8, 3), (9, 3), (6, 4), (9, 4), (6, 7), (9, 7), (6, 8), (7, 8), (8, 8), (9, 8)}

    def fill(x, y):
        if 6 <= x <= 9 and y == 2:
            return "aka_grass_sh"
        if 6 <= x <= 9 and 3 <= y <= 8:
            if (x, y) in court:
                return "aka_grass_flowers" if (x * 5 + y * 3) % 4 == 0 else "aka_grass"
            return "aka_rose_bed"
        return asc_floor(x, y)
    r = Civic(15, 11, fill)
    civic_walls(r, "asc", 0, 5)
    civic_walls(r, "asc", 10, 14)
    r.row(0, 6, ["aka_hedge_roses_top"] * 4)
    r.row(1, 6, ["aka_hedge_roses"] * 4)
    asc_shadow_row(r, 2, 0, 5)
    asc_shadow_row(r, 2, 10, 14)
    asc_healer(r, 3, 0, 4)
    r.put("asc_fountain", 7, 1, 2, 2)               # the doves' fountain
    r.set(6, 3, "aka_roses")
    r.set(9, 3, "aka_roses_b")
    r.set(6, 8, "aka_roses_b")
    r.set(9, 8, "aka_roses")
    r.put("asc_pithos", 12, 0, 2, 3)
    r.put("asc_jar", 14, 1, 1, 2)
    for y in (3, 7):
        r.put_checkered("asc_column", 10, y, 1, 3)
    r.put_checkered("asc_column", 5, 5, 1, 3)
    r.put_checkered("asc_kline", 12, 4, 2, 2)
    r.put_checkered("asc_kline", 12, 7, 2, 2)
    r.put_checkered("asc_bench", 1, 9, 2, 1)
    r.put_checkered("asc_mat", 7, 10, single=True)
    return r


room(
    name=f"{PA}_Asclepeion", title="The Asclepeion, Paphia", town="paphia", kind="civic",
    build=paphia_asclepeion, music="MUS_ICHOR_ASCLEPEION",
    warps=[(7, 10)],
    objects=[
        obj("ICHOR_HEALER", 3, 2, "down", f"{PA}_Asclepeion_EventScript_Healer", "LOCALID_PAPHIA_HEALER"),
        obj("SPECIES(PANACOIL)", 8, 5, "down", f"{PA}_Asclepeion_EventScript_Panacoil"),
    ],
    bgs=[
        bg(12, 2, "north", f"{PA}_Asclepeion_EventScript_Pithos"),
        bg(13, 2, "north", f"{PA}_Asclepeion_EventScript_Pithos"),
        bg(7, 2, "north", f"{PA}_Asclepeion_EventScript_Fountain"),
        bg(8, 2, "north", f"{PA}_Asclepeion_EventScript_Fountain"),
    ],
)


# Theodote sells offerings to pilgrims from a covered stoa with a long marble
# counter: little marble feet and hands, the parts people want healed, on the
# counter and on the wall behind; honey cakes on the counter; shelves of incense
# at the end; cages of doves (not for sale: "they're for the goddess, and she's
# particular").
def paphia_agora():
    r = Civic(13, 9, asc_floor)
    civic_walls(r, "asc")
    asc_shadow_row(r)
    r.set(2, 2, "asc_counter_l")
    for x in (3, 5, 9):
        r.set(x, 2, "asc_counter_m")
    r.set(4, 2, "asc_counter_cakes")
    r.set(6, 2, "asc_counter_staff")
    r.put("asc_votive_counter", 7, 2, 2, 1)
    r.set(10, 2, "asc_counter_r")
    r.row(3, 2, ["asc_counter_front_l"] + ["asc_counter_front_m"] * 7 + ["asc_counter_front_r"])
    r.put("asc_votive_wall", 3, 1, 2, 1)
    r.put("asc_votive_wall", 7, 1, 2, 1)
    r.put("asc_jar", 0, 1, 1, 2)
    r.put("asc_incense", 11, 0, 2, 3)
    for x in (1, 4, 8, 11):
        r.put_checkered("asc_column", x, 5, 1, 3)
    r.put_checkered("asc_brazier", 6, 5, 1, 2)
    r.put_checkered("asc_cage", 0, 4, 1, 2)
    r.put_checkered("asc_cage", 12, 6, 1, 2)
    r.put_checkered("asc_cage", 0, 7, 1, 2)
    r.put_checkered("asc_mat", 6, 8, single=True)
    return r


room(
    name=f"{PA}_Agora", title="The Agora, Paphia", town="paphia", kind="civic",
    build=paphia_agora, music="MUS_ICHOR_AGORA",
    warps=[(6, 8)],
    objects=[
        obj("ICHOR_WOMAN", 6, 2, "down", f"{PA}_Agora_EventScript_Theodote"),
    ],
    bgs=[
        bg(7, 3, "north", f"{PA}_Agora_EventScript_Votives"),
        bg(8, 3, "north", f"{PA}_Agora_EventScript_Votives"),
    ],
)


# Pygmalion carved Galatea out of one block and talked to her every night until
# she answered. His workshop: the roofed half on the left, on a stone floor,
# with chisels in their rack, the jointed wooden model of a woman, the table set
# for two, his narrow bed against the wall and, in the corner under a dust sheet,
# the statue he never finished; the open yard on the right behind its hedge,
# where the marble blocks wait and the hoist stands with a block in its tackle.
room(
    name=f"{PA}_PygmalionsWorkshop", title="Pygmalion's workshop, Paphia", town="paphia", kind="oikia",
    floor="flags", floor2="grass", wall="red",
    grid=[
        "WWWWWWWWWWWWW",
        "WWWWWWWWWWWWW",
        ".........,,,,",
        ".........,,,,",
        ".........,,,,",
        ".........,,,,",
        ".........,,,,",
        ".........,,,,",
        ".........,,,,",
        ".........,,,,",
    ],
    stamps=[
        ("statue_sheet", 1, 0), ("window", 2, 0), ("chisel_rack", 3, 0), ("niche", 4, 0),
        ("chisel_rack", 5, 0), ("window", 6, 0), ("herbs", 7, 0), ("lay_figure", 7, 2),
        ("column", 8, 2), ("column", 8, 7),
        ("hedge", 9, 0), ("hedge", 10, 0), ("hedge", 11, 0), ("hedge", 12, 0),
        ("bed_narrow", 0, 5), ("table_two", 4, 5), ("klismos_r", 3, 5), ("klismos_l", 6, 5),
        ("amphora_plain", 6, 2), ("marble_block", 2, 8), ("kalathos", 0, 8),
        ("marble_block_big", 9, 2), ("marble_block", 11, 2), ("marble_block_b", 12, 3),
        ("hoist", 10, 5), ("marble_block_b", 9, 8), ("marble_block", 12, 8),
        ("mat_single", 3, 9),
    ],
    warps=[(3, 9)],
    objects=[
        obj("ICHOR_ELDER_M", 5, 3, "down", f"{PA}_PygmalionsWorkshop_EventScript_Pygmalion"),
    ],
    bgs=[
        bg(1, 2, "north", f"{PA}_PygmalionsWorkshop_EventScript_DustSheet"),
        bg(4, 5, "north", f"{PA}_PygmalionsWorkshop_EventScript_Table"),
        bg(5, 5, "north", f"{PA}_PygmalionsWorkshop_EventScript_Table"),
    ],
)


# Leukippe polishes the temple's bronze mirrors and makes new ones. The walls
# are lined with them, hung at different angles; a mirror turns on its post as
# the ones in the rose court do; the polishing bench with its sand and felt;
# the mold and the casting pit by the door; the ladder to the loft she sleeps in.
room(
    name=f"{PA}_MirrorHouse", title="The mirror-house, Paphia", town="paphia", kind="oikia",
    floor="flags", wall="red",
    grid=[
        "WWWWWWWWWWW",
        "WWWWWWWWWWW",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
    ],
    stamps=[
        ("herbs", 0, 0), ("mirrors", 1, 0), ("window", 3, 0), ("mirrors_b", 4, 0), ("window", 6, 0),
        ("niche", 7, 0), ("mirrors", 8, 0), ("ladder", 10, 0),
        ("polish_bench", 4, 4), ("mirror_post", 8, 4),
        ("casting_pit", 1, 4), ("mirror_mold", 3, 6), ("mirror_mold", 0, 3),
        ("amphora_plain", 0, 6), ("pithos", 10, 5),
        ("mat_single", 5, 7),
    ],
    warps=[(5, 7)],
    objects=[
        obj("ICHOR_WOMAN", 6, 4, "left", f"{PA}_MirrorHouse_EventScript_Leukippe"),
    ],
    bgs=[
        bg(1, 1, "north", f"{PA}_MirrorHouse_EventScript_Mirror"),
        bg(2, 1, "north", f"{PA}_MirrorHouse_EventScript_Mirror"),
        bg(4, 1, "north", f"{PA}_MirrorHouse_EventScript_Mirror"),
        bg(5, 1, "north", f"{PA}_MirrorHouse_EventScript_Mirror"),
        bg(8, 1, "north", f"{PA}_MirrorHouse_EventScript_Mirror"),
        bg(9, 1, "north", f"{PA}_MirrorHouse_EventScript_Mirror"),
        bg(8, 5, "north", f"{PA}_MirrorHouse_EventScript_Stand"),
    ],
)


# Eumelos keeps the orchard below the north gate. The street door opens into
# his yard, where the old tree that hasn't fruited "since the goddesses
# quarrelled" stands gray and leafless (VARIANTS composes it in leaf with one
# golden apple, for the script to swap in); across a stone threshold, the
# farmhouse kitchen: the hearth, apple racks along the walls all empty but one
# tray with three small green apples, empty crates, a ladder, a pruning hook,
# and a painted plate with a golden apple on it.
room(
    name=f"{PA}_OrchardHouse", title="The orchard house, Paphia", town="paphia", kind="oikia",
    floor="terracotta", floor2="grass", wall="red",
    grid=[
        "WWWWWWWWWWWWW",
        "WWWWWWWWWWWWW",
        ".............",
        ".............",
        ".............",
        ".............",
        ".............",
        ",,,,,,,,,,,,,",
        ",,,,,,,,,,,,,",
        ",,,,,,,,,,,,,",
        ",,,,,,,,,,,,,",
    ],
    stamps=[
        ("apple_racks", 1, 0), ("window", 3, 0), ("pruning_hook", 4, 0), ("plate_gold", 5, 0),
        ("ladder_lean", 7, 0), ("soot", 9, 0), ("hearth", 9, 2), ("apple_racks_empty", 11, 0),
        ("table", 5, 4), ("stool", 4, 4), ("stool", 7, 4),
        ("apple_crate", 3, 3), ("apple_crate", 10, 5), ("apple_crate", 11, 5), ("apple_crate", 0, 5),
        ("pots", 11, 3), ("amphora_plain", 12, 4),
    ] + [("threshold", x, 6) for x in range(13)] + [
        ("apple_tree_bare", 6, 7),
        ("bench_l", 10, 9), ("bench_r", 11, 9),
        ("apple_crate", 9, 7), ("apple_crate", 4, 10), ("kalathos", 0, 8),
        ("mat_single", 2, 10),
    ],
    warps=[(2, 10)],
    objects=[
        obj("ICHOR_ELDER_M", 5, 8, "right", f"{PA}_OrchardHouse_EventScript_Eumelos"),
    ],
    bgs=[
        bg(6, 9, "north", f"{PA}_OrchardHouse_EventScript_Tree"),
        bg(7, 9, "north", f"{PA}_OrchardHouse_EventScript_Tree"),
        bg(1, 2, "north", f"{PA}_OrchardHouse_EventScript_Racks"),
        bg(2, 2, "north", f"{PA}_OrchardHouse_EventScript_Racks"),
        bg(5, 1, "north", f"{PA}_OrchardHouse_EventScript_Plate"),
        bg(6, 1, "north", f"{PA}_OrchardHouse_EventScript_Plate"),
    ],
)


# --------------------------------------------------------------------------
# The Neraida falls. The mill shares gTileset_OikiaMelos's country pieces
# (aegean_melos.py): grain, sacks, flour.
# --------------------------------------------------------------------------

# Myles's mill, the one still turning: a round room round the great millstone
# on its shaft, sacks of grain, flour on every surface, the domed bread oven in
# the wall, the ladder to his bed in the loft, and a cat white with flour.
room(
    name="KytheraNeraidaFalls_Mill", title="Myles's mill, the Neraida falls", town="falls", kind="oikia",
    floor="terracotta", wall="red",
    grid=[
        "WWWWWWWWWWWW",
        "WWWWWWWWWWWW",
        "............",
        "............",
        "............",
        "............",
        "#..........#",
        "#..........#",
        "##........##",
        "###......###",
    ],
    stamps=[
        ("herbs", 1, 0), ("soot", 2, 0), ("bread_oven", 2, 2), ("herbs", 4, 0), ("window", 5, 0),
        ("jar_shelf", 6, 0), ("ladder", 8, 0), ("niche", 10, 0), ("window", 11, 0),
        ("millstone", 5, 5),
        ("sacks", 10, 3), ("sacks", 10, 4), ("sack", 9, 3), ("sack", 10, 5), ("sacks", 1, 5),
        ("sack", 1, 6), ("pithos", 0, 3), ("kalathos", 9, 7), ("table", 2, 7), ("stool", 4, 7),
        ("flour", 4, 5), ("flour_b", 4, 6), ("flour", 7, 6), ("flour_b", 7, 5), ("flour", 5, 7),
        ("flour_b", 6, 7), ("flour_b", 5, 4), ("flour", 6, 4), ("flour_b", 9, 4), ("flour_b", 8, 7),
        ("flour_b", 2, 4), ("flour_b", 7, 8),
        ("mat", 5, 9),
    ],
    solid=[(8, 2)],
    warps=[(5, 9), (6, 9)],
    objects=[
        obj("ICHOR_ELDER_M", 4, 3, "down", "KytheraNeraidaFalls_Mill_EventScript_Myles"),
        obj("SPECIES(MEOWTH)", 8, 8, "look", "KytheraNeraidaFalls_Mill_EventScript_Cat"),
    ],
    bgs=[
        bg(6, 6, "north", "KytheraNeraidaFalls_Mill_EventScript_Millstone"),
        bg(8, 2, "north", "KytheraNeraidaFalls_Mill_EventScript_Ladder"),
        bg(2, 3, "north", "KytheraNeraidaFalls_Mill_EventScript_Oven"),
        bg(3, 3, "north", "KytheraNeraidaFalls_Mill_EventScript_Oven"),
    ],
)


# --------------------------------------------------------------------------
# Melos: Klima, the fishing hamlet on the great round bay
# --------------------------------------------------------------------------

# Kentrios found the armless goddess with his hoe. A low farmhouse, one room:
# the hearth, the hoe on its pegs, baskets of barley, and on a shelf the things
# he dug up looking for her arms: a sherd, a clay lamp, a coin, a marble toe
# that isn't hers, a blade of black glass.
room(
    name="Melos_Farmhouse", title="Kentrios's farmhouse, Melos", town="melos", kind="oikia",
    floor="terracotta", wall="red",
    grid=[
        "WWWWWWWWWWWWW",
        "WWWWWWWWWWWWW",
        ".............",
        ".............",
        ".............",
        ".............",
    ],
    stamps=[
        ("soot", 1, 0), ("hearth", 1, 2), ("herbs", 3, 0), ("finds_shelf", 4, 0), ("niche", 6, 0),
        ("window", 7, 0), ("hoe_pegs", 8, 0), ("herbs", 9, 0), ("window", 11, 0),
        ("barley_basket", 3, 3), ("barley_basket", 0, 4), ("barley_basket", 3, 4), ("pithos", 0, 2),
        ("mortar", 4, 4),
        ("kline", 10, 3), ("table", 7, 3), ("stool", 9, 3), ("amphora_plain", 12, 2),
        ("mat", 6, 5),
    ],
    warps=[(6, 5), (7, 5)],
    objects=[
        obj("ICHOR_ELDER_M", 5, 3, "down", "Melos_Farmhouse_EventScript_Kentrios"),
    ],
    bgs=[
        bg(4, 1, "north", "Melos_Farmhouse_EventScript_Shelf"),
        bg(5, 1, "north", "Melos_Farmhouse_EventScript_Shelf"),
        bg(8, 1, "north", "Melos_Farmhouse_EventScript_Hoe"),
    ],
)

# Melanippos knaps obsidian the way his family always has. A workshop with a
# stone floor deep in black flakes, the knee-high anvil stone with its leather
# pad, antler hammers in a row, cores of glass on a shelf, the bench where he
# polishes black mirrors, and on the wall a round mirror of polished black
# glass. The front of the house is older and its wall comes forward.
room(
    name="Melos_KnappersHouse", title="Melanippos's house, Melos", town="melos", kind="oikia",
    floor="flags", wall="blue",
    grid=[
        "####WWWWW",
        "WWWWWWWWW",
        "WWWW.....",
        ".........",
        ".........",
        ".........",
        ".........",
        ".........",
    ],
    stamps=[
        ("herbs", 0, 1), ("antler_hammers", 3, 1), ("chest", 1, 2), ("cores_shelf", 5, 0),
        ("window", 7, 0), ("obsidian_mirror", 8, 0),
        ("anvil_stone", 5, 4), ("polish_bench", 1, 5),
        ("amphora_plain", 8, 3), ("kline", 6, 6),
        ("flakes", 4, 3), ("flakes_b", 5, 3), ("flakes", 6, 4), ("flakes_c", 6, 3),
        ("flakes", 5, 5), ("flakes_b", 4, 5), ("flakes_c", 6, 5), ("flakes_b", 3, 4),
        ("flakes_c", 7, 4), ("flakes_c", 2, 4), ("flakes_c", 5, 6), ("flakes_c", 0, 3),
        ("mat", 3, 7),
    ],
    warps=[(3, 7), (4, 7)],
    objects=[
        obj("ICHOR_ELDER_M", 4, 4, "right", "Melos_KnappersHouse_EventScript_Melanippos",
            "LOCALID_MELOS_MELANIPPOS"),
    ],
    bgs=[
        bg(8, 1, "north", "Melos_KnappersHouse_EventScript_Mirror"),
        bg(5, 1, "north", "Melos_KnappersHouse_EventScript_Cores"),
        bg(6, 1, "north", "Melos_KnappersHouse_EventScript_Cores"),
        bg(5, 4, "north", "Melos_KnappersHouse_EventScript_Anvil"),
    ],
)

# The boathouse: Myrtis and Kalchedon, fishers, and their baby live in the room
# over their boat. Downstairs the boat sits on rollers on the stone slip, which
# runs down into the sea that comes in under the painted doors; the stair goes
# up to the room over it.
room(
    name="Melos_Boathouse", title="The boathouse, Melos", town="melos", kind="oikia",
    floor="flags", wall="blue",
    grid=[
        "WWWWWWWWWWWW",
        "WWWWWWWWWWWW",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
    ],
    stamps=[
        ("nets", 0, 0), ("oars", 2, 0), ("oar", 3, 0), ("window", 5, 0), ("trident", 6, 0),
        ("nets", 7, 0), ("stairs_up_r", 9, 0),
        ("fish_basket", 1, 3), ("fish_basket", 2, 3), ("amphora_plain", 11, 3), ("pithos", 1, 5),
        ("rollers", 6, 4), ("rollers", 7, 4), ("rollers", 6, 5), ("rollers", 7, 5),
        ("sea_edge", 6, 6), ("sea_edge", 7, 6), ("sea_edge", 8, 6), ("sea_edge", 9, 6), ("sea_edge", 10, 6),
        ("sea_doors_l", 6, 7), ("sea_doors_r", 7, 7), ("sea_doors_m", 8, 7), ("sea_doors_l", 9, 7),
        ("sea_doors_r", 10, 7),
        ("diving_weights", 11, 5), ("urchins", 4, 2),
        ("mat", 2, 7),
    ],
    solid=[(x, y) for x in range(6, 11) for y in (6, 7)],
    warps=[(2, 7), (3, 7)],
    links=[(9, 2, "MAP_MELOS_BOATHOUSE_LOFT", 0)],
    objects=[
        obj("ICHOR_UPTURNED_BOAT_L", 6, 4, "down", "Melos_Boathouse_EventScript_Boat"),
        obj("ICHOR_UPTURNED_BOAT_R", 7, 4, "down", "Melos_Boathouse_EventScript_Boat"),
    ],
    bgs=[
        bg(8, 6, "south", "Melos_Boathouse_EventScript_SeaDoors"),
        bg(9, 6, "south", "Melos_Boathouse_EventScript_SeaDoors"),
    ],
)

# The room over the boat: a bed, a cradle hung from the beam on ropes, nets, a
# hearth on a stone slab, and a window right over the water.
room(
    name="Melos_BoathouseLoft", title="The room over the boat, Melos", town="melos", kind="oikia",
    floor="boards", wall="blue",
    grid=[
        "WWWWWWWWWW",
        "WWWWWWWWWW",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
    ],
    rugs=[("red", 2, 4, 3, 2)],
    stamps=[
        ("stairs_down", 1, 0), ("nets", 3, 0), ("herbs", 5, 0), ("window", 6, 0), ("soot", 7, 0),
        ("hearth", 7, 2), ("sponges_b", 9, 0),
        ("kline", 5, 4), ("cradle", 7, 5), ("table_round", 2, 3), ("stool", 3, 3), ("fish_basket", 9, 5),
        ("kalathos", 0, 5), ("pots", 9, 2),
    ],
    warps=[],
    links=[(1, 1, "MAP_MELOS_BOATHOUSE", 2)],
    objects=[
        obj("ICHOR_WOMAN", 6, 3, "down", "Melos_BoathouseLoft_EventScript_Myrtis"),
        obj("ICHOR_FISHER", 4, 5, "up", "Melos_BoathouseLoft_EventScript_Kalchedon",
            "LOCALID_MELOS_KALCHEDON"),
    ],
    bgs=[
        bg(7, 5, "west", "Melos_BoathouseLoft_EventScript_Cradle"),
        bg(6, 1, "north", "Melos_BoathouseLoft_EventScript_Window"),
        bg(7, 3, "north", "Melos_BoathouseLoft_EventScript_Hearth"),
        bg(8, 3, "north", "Melos_BoathouseLoft_EventScript_Hearth"),
    ],
)


# ==========================================================================
# Composition
# ==========================================================================

_KITS = {}


def kits():
    """The Aegean islands' tilesets: an OikiaKit per town, one CivicKit."""
    if not _KITS:
        stamps = G.load()
        for sym in dict.fromkeys(OIKIA_TILESETS.values()):
            _KITS[sym] = IL.OikiaKit(sym, G.PALETTES, stamps, G.FLOORS)
        _KITS[CIVIC_TILESET] = IL.CivicKit(CIVIC_TILESET, GC.define, GC.PALETTES)
    return _KITS


def tileset_of(rm):
    if rm["kind"] == "civic":
        return CIVIC_TILESET
    return rm.get("tiles") or OIKIA_TILESETS[rm["town"]]


# Variants composed into a room's tileset that no layout uses yet: the cells a
# script swaps in with setmetatile. (room, variant name, stamp swaps)
VARIANTS = [
    ("KytheraPaphia_OrchardHouse", "gold", {"apple_tree_bare": "apple_tree_gold"}),
]


def variant_spec(rm, swaps):
    return dict(rm, stamps=[(swaps.get(n, n), x, y) for (n, x, y) in rm["stamps"]])


class Civic:
    """A civic room under construction: a grid of metatile names."""

    def __init__(self, w, h, fill):
        self.w, self.h = w, h
        self.grid = [[fill(x, y) if callable(fill) else fill for x in range(w)] for y in range(h)]

    def set(self, x, y, name):
        if name not in ct.BY_NAME:
            raise KeyError(f"no civic metatile {name}")
        if not (0 <= x < self.w and 0 <= y < self.h):
            raise ValueError(f"{name} at ({x},{y}) is off the room")
        self.grid[y][x] = name

    def row(self, y, x0, names):
        for i, n in enumerate(names):
            self.set(x0 + i, y, n)

    def fill(self, x0, y0, w, h, name):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                self.set(x, y, name)

    def put(self, prefix, x, y, w, h):
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, f"{prefix}_{i}_{j}")

    def put_checkered(self, prefix, x, y, w=1, h=1, single=False):
        """An object on the Asclepeion's checker: cells on cream slabs take
        the _b variant (civic_rooms.py's rule)."""
        for j in range(h):
            for i in range(w):
                b = (x + i + y + j) % 2 == 1
                p = prefix + ("_b" if b else "")
                self.set(x + i, y + j, p if single else f"{p}_{i}_{j}")


def compose_all(compile_=True):
    """Compose every room, collect each tileset's cells, build the tilesets,
    and return {room: (blocks, behaviors, w, h)} plus each variant's ids."""
    ks = kits()
    shapes = {}
    oikia_layouts = {sym: {} for sym in ks if sym != CIVIC_TILESET}
    civic_grids = {}
    for rm in ROOMS:
        sym = tileset_of(rm)
        if rm["kind"] == "oikia":
            cells = ks[sym].compose(rm)
            oikia_layouts[sym][rm["name"]] = cells
            shapes[rm["name"]] = cells
        else:
            r = rm["build"]()
            civic_grids[rm["name"]] = r.grid
            shapes[rm["name"]] = r
    for (room, vname, swaps) in VARIANTS:
        rm = next(r for r in ROOMS if r["name"] == room)
        oikia_layouts[tileset_of(rm)][f"{room}@{vname}"] = ks[tileset_of(rm)].compose(variant_spec(rm, swaps))
    out, ids_all, stats = {}, {}, {}
    for sym, layouts in oikia_layouts.items():
        if not layouts:
            continue
        kit = ks[sym]
        ids = kit.collect(layouts)
        ids_all.update(ids)
        stats[sym] = kit.build(compile_)
        for name, cells in layouts.items():
            if "@" in name:
                continue
            h, w = len(cells), len(cells[0])
            blocks = kit.blocks(cells, ids[name]).astype("<u2")
            beh = [[cells[y][x].behavior for x in range(w)] for y in range(h)]
            out[name] = (blocks, beh, w, h)
    kit = ks[CIVIC_TILESET]
    cids = kit.collect(civic_grids)
    stats[CIVIC_TILESET] = kit.build(compile_)
    for name, grid in civic_grids.items():
        h, w = len(grid), len(grid[0])
        blocks = np.zeros(w * h, "<u2")
        beh = [["MB_NORMAL"] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                m = ct.METATILES[ct.BY_NAME[grid[y][x]]]
                blocks[y * w + x] = cids[grid[y][x]] | (SOLID if m["solid"] else WALK)
                beh[y][x] = m["behavior"]
        out[name] = (blocks, beh, w, h)
    for rm in ROOMS:
        blocks, beh, w, h = out[rm["name"]]
        for (x, y) in rm["solid"]:
            blocks[y * w + x] = (blocks[y * w + x] & 0x03FF) | SOLID
    return out, shapes, ids_all, stats


def void_id(rm):
    kit = kits()[tileset_of(rm)]
    return kit.ids["void"] if rm["kind"] == "civic" else kit.void_id()


# ==========================================================================
# Checks
# ==========================================================================

def check(rm, blocks, beh, w, h):
    """Warps on warp tiles; people and readable things reachable; nobody in the
    way of anybody else. Returns a list of problems."""
    name = rm["name"]
    probs = []

    def solid(x, y):
        return not (0 <= x < w and 0 <= y < h) or bool(blocks[y * w + x] & 0x0C00)

    warps = [tuple(p) for p in rm["warps"]] + [tuple(l[:2]) for l in rm["links"]]
    for (x, y) in warps:
        if beh[y][x] not in WARP_BEHAVIORS:
            probs.append(f"warp at ({x},{y}) is on {beh[y][x]}, not a warp tile")
    people = {(o["x"], o["y"]) for o in rm["objects"]}
    wanderers = {(o["x"], o["y"]) for o in rm["objects"] if o["face"] == "wander"}

    def reach(blockers):
        start = warps[0]
        seen, todo = {start}, deque([start])
        while todo:
            x, y = todo.popleft()
            for dx, dy in DIRS.values():
                n = (x + dx, y + dy)
                if n in seen or solid(*n) or n in blockers:
                    continue
                seen.add(n)
                todo.append(n)
        return seen

    free = reach(set())
    blocked = reach(people - wanderers)
    for o in rm["objects"]:
        p = (o["x"], o["y"])
        if solid(*p) and not o.get("on_furniture"):
            probs.append(f"{o['script']} stands on a solid tile {p}")
        if beh[p[1]][p[0]] in WARP_BEHAVIORS:
            probs.append(f"{o['script']} stands on a warp {p}")
        # someone can stand next to it (or across a counter) once the others are placed
        ok = False
        for dx, dy in DIRS.values():
            n = (p[0] + dx, p[1] + dy)
            if n in blocked:
                ok = True
            m = (p[0] + 2 * dx, p[1] + 2 * dy)
            if 0 <= n[0] < w and 0 <= n[1] < h and beh[n[1]][n[0]] == "MB_COUNTER" and m in blocked:
                ok = True
        if not ok and not o.get("unreached"):
            probs.append(f"nobody can reach {o['script']} at {p}")
        rx, ry = o["range"]
        if o["face"] == "wander":
            for yy in range(p[1] - ry, p[1] + ry + 1):
                for xx in range(p[0] - rx, p[0] + rx + 1):
                    if (xx, yy) not in free:
                        probs.append(f"{o['script']}'s wander range covers ({xx},{yy}), not open floor")
                    if beh[yy][xx] in WARP_BEHAVIORS if 0 <= xx < w and 0 <= yy < h else False:
                        probs.append(f"{o['script']}'s wander range covers a warp ({xx},{yy})")
    for b in rm["bgs"]:
        dx, dy = DIRS[b["facing"]] if b["facing"] in DIRS else (0, 1)
        frm = (b["x"] - dx, b["y"] - dy)
        if frm not in blocked:
            probs.append(f"bg {b['script']} at ({b['x']},{b['y']}) is read from {frm}, which nobody can reach")
    for c in rm["coords"]:
        if (c["x"], c["y"]) not in blocked:
            probs.append(f"coord {c['script']} at ({c['x']},{c['y']}) is unreachable")
    for (x, y) in warps:
        if (x, y) not in blocked:
            probs.append(f"warp ({x},{y}) can't be reached past the people")
    return [f"{name}: {p}" for p in probs]


# ==========================================================================
# Writing
# ==========================================================================

def load_json(p):
    return json.loads(p.read_text())


def write_json(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def const_name(name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name).upper()


def map_id(rm):
    return "MAP_" + const_name(rm["name"])


def layout_id(rm):
    return "LAYOUT_" + const_name(rm["name"])


def register(rm, w, h):
    """layouts.json, map_groups.json, ichor_maps.inc and .gitignore, idempotently."""
    name = rm["name"]
    lay_path = ROOT / "data/layouts/layouts.json"
    lays = load_json(lay_path)
    entry = {
        "id": layout_id(rm),
        "name": f"{name}_Layout",
        "width": w,
        "height": h,
        "primary_tileset": PRIMARY,
        "secondary_tileset": tileset_of(rm),
        "border_filepath": f"data/layouts/{name}/border.bin",
        "blockdata_filepath": f"data/layouts/{name}/map.bin",
        "layout_version": "emerald",
    }
    for i, l in enumerate(lays["layouts"]):
        if l.get("id") == entry["id"]:
            if l != entry:
                lays["layouts"][i] = entry
                write_json(lay_path, lays)
            break
    else:
        lays["layouts"].append(entry)
        write_json(lay_path, lays)

    grp_path = ROOT / "data/maps/map_groups.json"
    groups = load_json(grp_path)
    group = GROUPS[rm["town"]]
    if group not in groups:
        groups[group] = []
        groups["group_order"].append(group)
    if name not in groups[group]:
        groups[group].append(name)
        write_json(grp_path, groups)

    inc = ROOT / "data/ichor_maps.inc"
    line = f'\t.include "data/maps/{name}/scripts.inc"'
    if line not in inc.read_text().split("\n"):
        with inc.open("a") as f:
            f.write(line + "\n")
    gi = ROOT / ".gitignore"
    ign = f"data/maps/{name}/scripts.inc"
    if ign not in gi.read_text().split("\n"):
        with gi.open("a") as f:
            f.write(ign + "\n")
    pory = ROOT / f"data/maps/{name}/scripts.pory"
    if not pory.exists():
        pory.parent.mkdir(parents=True, exist_ok=True)
        pory.write_text(f"mapscripts {name}_MapScripts {{}}\n")


def write_map_json(rm):
    name = rm["name"]
    town = rm["town"]
    if name in DOORS:
        dest = (OUTDOOR[town], str(DOORS[name]))
    else:
        dest = PLACEHOLDER
    objects = []
    for o in rm["objects"]:
        ev = {}
        if o["local_id"]:
            ev["local_id"] = o["local_id"]
        rx, ry = o["range"]
        ev.update({
            "graphics_id": o["gfx"],
            "x": o["x"],
            "y": o["y"],
            "elevation": 3,
            "movement_type": FACE_MOVE.get(o["face"], o["face"]),
            "movement_range_x": rx,
            "movement_range_y": ry,
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0",
            "script": o["script"],
            "flag": o["flag"],
        })
        objects.append(ev)
    warps = [{"x": x, "y": y, "elevation": 0, "dest_map": dest[0], "dest_warp_id": dest[1]}
             for (x, y) in rm["warps"]]
    warps += [{"x": x, "y": y, "elevation": 0, "dest_map": m, "dest_warp_id": str(i)}
              for (x, y, m, i) in rm["links"]]
    coords = [{"type": "trigger", "x": c["x"], "y": c["y"], "elevation": 3, "var": c["var"],
               "var_value": str(c["value"]), "script": c["script"]} for c in rm["coords"]]
    bgs = [{"type": "sign", "x": b["x"], "y": b["y"], "elevation": 0,
            "player_facing_dir": FACING[b["facing"]], "script": b["script"]} for b in rm["bgs"]]
    data = {
        "id": map_id(rm),
        "name": name,
        "layout": layout_id(rm),
        "music": rm["music"],
        "region": "REGION_HOENN",
        "region_map_section": MAPSEC[town],
        "requires_flash": False,
        "weather": "WEATHER_NONE",
        "map_type": "MAP_TYPE_INDOOR",
        "allow_cycling": False,
        "allow_escaping": False,
        "allow_running": True,
        "show_map_name": False,
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
        "connections": None,
        "object_events": objects,
        "warp_events": warps,
        "coord_events": coords,
        "bg_events": bgs,
    }
    p = ROOT / f"data/maps/{name}/map.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    write_json(p, data)


# ==========================================================================
# Rendering
# ==========================================================================

_RENDERERS = {}


def render(rm, blocks, w):
    """The room through the compiled tileset, on the oikos primary."""
    sym = tileset_of(rm)
    if sym not in _RENDERERS:
        RM.read_fieldmap_constants()
        syms = RM.scan_tileset_symbols()
        _RENDERERS[sym] = RM.Renderer(RM.Tileset(RM.resolve_tileset(PRIMARY, syms)),
                                      RM.Tileset(RM.resolve_tileset(sym, syms)))
    return np.array(RM.render_blocks(_RENDERERS[sym], blocks, w).convert("RGB"))


def composed_image(rm, shape):
    """The room as composed from the art, before compiling (oikia: the cells'
    layers; civic: the named metatiles' layers)."""
    if rm["kind"] == "oikia":
        return B.image_of(shape)
    grid = shape.grid
    h, w = len(grid), len(grid[0])
    out = np.zeros((h * 16, w * 16, 3), np.uint8)
    for y in range(h):
        for x in range(w):
            m = ct.METATILES[ct.BY_NAME[grid[y][x]]]
            px = ct.to_rgba(m["bottom"])[..., :3].copy()
            for k in ("middle", "top"):
                if m[k] is not None:
                    lay = ct.to_rgba(m[k])
                    keep = ~(lay[..., :3] == (255, 0, 255)).all(-1)
                    px[keep] = lay[..., :3][keep]
            out[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = px
    return out


SPRITES = ROOT / "graphics/object_events/pics/people/ichor"
FRAME = {"down": 0, "up": 1, "left": 2, "right": 2, "look": 0, "wander": 0}


def with_people(img, rm):
    """The render with each NPC's first frame drawn on its tile (Pokémon and
    things without an Ichor walker get a small marker)."""
    out = Image.fromarray(img).convert("RGBA")
    for o in sorted(rm["objects"], key=lambda o: o["y"]):
        g = o["gfx"].replace("OBJ_EVENT_GFX_ICHOR_", "").lower()
        p = SPRITES / f"{g}.png"
        x, y = o["x"] * 16, o["y"] * 16
        misc = ROOT / f"graphics/object_events/pics/misc/ichor/{g}.png"
        if misc.exists():
            sheet = Image.open(misc).convert("RGBA")
            arr = np.array(sheet)
            pal0 = np.array(Image.open(misc).convert("RGB"))[0, 0]
            arr[(arr[..., :3] == pal0).all(-1)] = 0
            out.alpha_composite(Image.fromarray(arr[:16, :16]), (x, y))
        elif p.exists():
            sheet = Image.open(p)
            pal = sheet.getpalette()
            arr = np.array(sheet)
            f = FRAME.get(o["face"], 0)
            fr = arr[:, f * 16:(f + 1) * 16]
            rgba = np.zeros((32, 16, 4), np.uint8)
            for j in range(32):
                for i in range(16):
                    v = fr[j, i]
                    if v:
                        rgba[j, i] = (*pal[v * 3:v * 3 + 3], 255)
            spr = Image.fromarray(rgba)
            if o["face"] == "right":
                spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
            out.alpha_composite(spr, (x, y - 16))
        else:
            m = Image.new("RGBA", (10, 10), (240, 60, 160, 255))
            out.alpha_composite(m, (x + 3, y + 3))
    return np.array(out.convert("RGB"))


def save(arr, path, scale=3):
    im = Image.fromarray(arr)
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


# ==========================================================================

def variant_doc(ids_all):
    """Markdown: for each variant, the cells that differ and both metatile ids
    (what a script passes to setmetatile)."""
    lines = []
    for (room, vname, swaps) in VARIANTS:
        base, var = ids_all[room], ids_all[f"{room}@{vname}"]
        rm = next(r for r in ROOMS if r["name"] == room)
        lines.append(f"`{map_id(rm)}`, {vname} ({', '.join(f'`{a}` to `{b}`' for a, b in swaps.items())}), "
                     f"on `{tileset_of(rm)}`:")
        lines.append("")
        lines.append("| Cell | As built | Swapped in |")
        lines.append("|---|---|---|")
        for y, (ra, rb) in enumerate(zip(base, var)):
            for x, (ia, ib) in enumerate(zip(ra, rb)):
                if ia != ib:
                    lines.append(f"| ({x},{y}) | `0x{ia:03X}` | `0x{ib:03X}` |")
        lines.append("")
    return "\n".join(lines)


PIECES_IMG = ROOT / "design/phase4/img/aegean_pieces.png"
HALLS_IMG = ROOT / "design/phase4/img/aegean_halls_pieces.png"


def civic_cells_image(names_grid):
    h, w = len(names_grid), len(names_grid[0])
    out = np.zeros((h * 16, w * 16, 3), np.uint8)
    for y in range(h):
        for x in range(w):
            m = ct.METATILES[ct.BY_NAME[names_grid[y][x]]]
            px = ct.to_rgba(m["bottom"])[..., :3].copy()
            for k in ("middle", "top"):
                if m[k] is not None:
                    lay = ct.to_rgba(m[k])
                    keep = ~(lay[..., :3] == (255, 0, 255)).all(-1)
                    px[keep] = lay[..., :3][keep]
            out[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = px
    return out


def new_civic_pieces():
    """The islands' own civic metatiles, grouped into pieces: prefix -> grid."""
    groups = {}
    for m in ct.METATILES[GC.FIRST_NEW:]:
        mm = re.match(r"(.+)_(\d+)_(\d+)$", m["name"])
        if mm:
            groups.setdefault(mm.group(1), {})[(int(mm.group(2)), int(mm.group(3)))] = m["name"]
        else:
            groups[m["name"]] = {(0, 0): m["name"]}
    out = {}
    for prefix, cells in groups.items():
        w = max(x for x, _ in cells) + 1
        h = max(y for _, y in cells) + 1
        out[prefix] = [[cells[(x, y)] for x in range(w)] for y in range(h)]
    return out


def pieces_reference(stats):
    """The reference sheets and the generated part of ROOMS_aegean.md: the
    tilesets' budgets, every piece with where it is used, the variant ids."""
    used = {}
    on_wall = set()
    for rm in ROOMS:
        if rm["kind"] != "oikia":
            continue
        for (n, x, y) in rm["stamps"]:
            used.setdefault(n, {})[rm["name"]] = (rm, x, y)
            if y == 0:
                on_wall.add(n)
    for (room, vname, swaps) in VARIANTS:
        rm = next(r for r in ROOMS if r["name"] == room)
        for new in swaps.values():
            used.setdefault(new, {})[f"{room} ({vname})"] = (rm, 0, 0)
    items, rows = [], []
    for name, st in G.STAMPS.items():
        where = used.get(name, {})
        rm = next(iter(where.values()))[0] if where else {"floor": "terracotta", "wall": "red"}
        floor = (G.FLOORS.get(rm.get("floor2")) or {}).get("plain") if name.startswith("apple_tree") \
            else None
        floor = floor if floor is not None else B.A.FLOORS.get(rm["floor"], G.FLOORS.get(rm["floor"]))["plain"]
        items.append((name, IL.stamp_preview(st, floor, B.A.WALLS[rm["wall"]], name in on_wall)))
        rooms = ", ".join(sorted(r.replace("Kythera", "") for r in where)) or "(none yet)"
        rows.append(f"| `{name}` | {st['w']}x{st['h']} | {st['pal']} | {rooms} | {st['note']} |")
    IL.pieces_sheet(items, PIECES_IMG)
    halls = new_civic_pieces()
    IL.pieces_sheet([(p, civic_cells_image(g)) for p, g in halls.items()], HALLS_IMG, cols=8)
    lines = ["Tilesets as built:", "",
             "| Tileset | Rooms | Metatiles | Tiles (of 504) |", "|---|---|---|---|"]
    for sym, (n, tiles) in stats.items():
        rooms = [r["name"].replace("Kythera", "") for r in ROOMS if tileset_of(r) == sym]
        lines.append(f"| `{sym}` | {', '.join(rooms)} | {n} | {tiles} |")
    lines += ["", "### The homes' pieces", "",
              "Stamps for `room(... stamps=[(name, x, y)])`, drawn in oikia's palettes "
              "(![every piece](img/aegean_pieces.png)). Oikia's own pieces "
              "(`design/phase1/TILES_oikia.md`) can be used too.", "",
              "| Stamp | Cells | Palette | Used in | What it is |", "|---|---|---|---|---|"] + rows
    lines += ["", "### The halls' pieces", "",
              "Named metatiles for the civic rooms' `Civic` grids, added to gTileset_Civic's "
              "(![every piece](img/aegean_halls_pieces.png)). A piece of several cells is "
              "`<prefix>_<x>_<y>`; put it with `r.put(prefix, x, y, w, h)`.", "",
              "| Piece | Cells |", "|---|---|"]
    for p, g in halls.items():
        lines.append(f"| `{p}` | {len(g[0])}x{len(g)} |")
    return "\n".join(lines)


def splice_doc(text):
    begin, end = "<!-- kythera_homes: begin generated -->", "<!-- kythera_homes: end generated -->"
    doc = DOC.read_text()
    if begin not in doc:
        return
    a, b = doc.index(begin) + len(begin), doc.index(end)
    DOC.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="compose and check only; write source-composed renders to --review")
    ap.add_argument("--review", metavar="DIR", help="write the people renders here instead of IMG")
    args = ap.parse_args()

    names = [r["name"] for r in ROOMS]
    assert len(names) == len(set(names)), "duplicate room"
    out, shapes, ids_all, stats = compose_all(compile_=not args.no_compile)
    bad = []
    for rm in ROOMS:
        blocks, beh, w, h = out[rm["name"]]
        bad += check(rm, blocks, beh, w, h)
    for sym, (n, tiles) in stats.items():
        print(f"kythera_homes: {sym}: {n} metatiles" + (f", {tiles} tiles of {IL.MAX_TILES}" if tiles else ""))
    if bad:
        print("\n".join(bad))
        raise SystemExit("kythera_homes: fix the rooms above")
    if args.no_compile:
        if args.review:
            for rm in ROOMS:
                img = composed_image(rm, shapes[rm["name"]])
                save(with_people(img, rm), Path(args.review) / f"{rm['name']}_people.png")
        return
    for rm in ROOMS:
        blocks, beh, w, h = out[rm["name"]]
        img = render(rm, blocks, w)
        if not np.array_equal(img, composed_image(rm, shapes[rm["name"]])):
            raise SystemExit(f"kythera_homes: {rm['name']} doesn't render as composed")
        d = ROOT / "data/layouts" / rm["name"]
        d.mkdir(parents=True, exist_ok=True)
        blocks.astype("<u2").tofile(d / "map.bin")
        np.array([void_id(rm)] * 4, "<u2").tofile(d / "border.bin")
        register(rm, w, h)
        write_map_json(rm)
        save(img, IMG / f"{rm['name']}.png")
        dest = Path(args.review) if args.review else IMG
        save(with_people(img, rm), dest / f"{rm['name']}_people.png")
        print(f"kythera_homes: {rm['name']} {w}x{h} on {tileset_of(rm)}")
    if DOC.exists():
        splice_doc(pieces_reference(stats) + "\n\n### Script swaps\n\n" + variant_doc(ids_all))


if __name__ == "__main__":
    main()
