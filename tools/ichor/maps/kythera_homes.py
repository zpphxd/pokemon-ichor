#!/usr/bin/env python3
"""Every interior on Kythera Isle and Melos (Act III, design/phase4/SCRIPT.md Part 2).

Skandeia's seven, Paphia's seven (not the Temple of Aphrodite), Myles's mill at
the Neraida falls, and Melos's three households (the boathouse has two floors).
Every house is a home and every interior is unique (design/MAP_DESIGN.md §2):
each room's shape, size and furniture are chosen for whoever lives or works
there, from the room catalogs design/phase1/ROOMS_oikia.md and ROOMS_civic.md.

Two kinds of room, as in the slice:
  - oikia homes are composed with tools/ichor/art/oikia_build.py's composer from
    the pieces in oikia_art.py, without recompiling gTileset_Oikia: every cell a
    home uses must already be in the tileset (as elaia_homes.py and akti_homes.py
    require), so the tileset and every other room's ids stay as committed. A home
    that needs a new piece means asking the art lead for it.
  - civic rooms (the Asclepeions, the Agoras and the sculptors' and gardeners'
    yards) are grids of gTileset_Civic's named metatiles, as civic_rooms.py lays
    out the slice's.

This script is the single source of each room's layout and of its map.json
events (warps, people, readable things). It writes, for each room:
  data/layouts/<Map>/{map,border}.bin and the layouts.json entry,
  data/maps/<Map>/map.json (scripts.pory is hand-written and never touched),
  the map's place in data/maps/map_groups.json, data/ichor_maps.inc and .gitignore,
  design/phase4/img/interiors/<Map>.png (3x) and <Map>_people.png (with the NPCs),
after checking that every warp, person and readable thing is reachable, that
bg events are read from the tile in front of them, and that no person blocks
the way to another.

The outdoor maps (MAP_KYTHERA_SKANDEIA and the rest) don't exist yet, so each
exit warp points at PLACEHOLDER until DOORS names the outdoor map's warp id.

  /usr/bin/python3 tools/ichor/maps/kythera_homes.py            # build everything
  /usr/bin/python3 tools/ichor/maps/kythera_homes.py --probe    # list cells oikia lacks
  /usr/bin/python3 tools/ichor/maps/kythera_homes.py --only KytheraSkandeia_AxylosHouse
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

import civic_tiles as ct  # noqa: E402
import oikia_art as A  # noqa: E402
import oikia_build as B  # noqa: E402
import oikia_rooms as R  # noqa: E402
import render_map as RM  # noqa: E402

PRIMARY = "gTileset_Oikos"
VOID = {"oikia": 0x0210, "civic": 0x0200}
SECONDARY = {"oikia": "gTileset_Oikia", "civic": "gTileset_Civic"}
IMG = ROOT / "design/phase4/img/interiors"
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
DOORS = {}

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
# Aegean-blue dado.
# --------------------------------------------------------------------------

# Axylos keeps the old law: one big room that is almost all table, benches down
# both sides, the hearth at the end with a pot that's never cold, nets and an
# oar on the wall, a shelf of more bowls than one man could need, and a peg with
# an empty goat's tether. The bad guests (beat III-1C2) sit at his table.
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
        ("nets", 0, 0), ("oars", 2, 0), ("window", 3, 0), ("jar_shelf", 5, 0), ("window", 7, 0),
        ("soot", 11, 0), ("hearth", 11, 2), ("pots", 13, 2),
        ("table", 3, 5), ("table", 5, 5), ("table", 7, 5),
        ("stool", 3, 4), ("stool", 5, 4), ("stool", 6, 4), ("stool", 8, 4),
        ("stool", 3, 6), ("stool", 4, 6), ("stool", 5, 6), ("stool", 6, 6), ("stool", 8, 6),
        ("kline", 11, 5), ("amphora_plain", 13, 5), ("fish_basket", 1, 3), ("fish_basket", 12, 7),
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
# A cool stone room: sponges hang from every beam, a basket of black urchins,
# the long bench where sponges are beaten, stone weights by the door, and the
# tank in the floor where Ankyra hammers. The bottom-right corner is the street's
# rock, cut away.
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
    rugs=[("blue", 8, 3, 3, 2)],
    stamps=[
        ("herbs", 0, 0), ("herbs", 1, 0), ("nets", 2, 0), ("window", 4, 0), ("herbs", 5, 0),
        ("niche_horse", 6, 0), ("trident", 7, 0), ("window", 8, 0), ("jar_shelf", 9, 0), ("herbs", 11, 0),
        ("fish_basket", 4, 3), ("table", 2, 4), ("stool", 1, 4),
        ("kline", 4, 6), ("mortar", 3, 7), ("amphora_plain", 7, 6),
        ("mat", 1, 7),
    ],
    solid=[(8, 3), (9, 3), (10, 3), (8, 4), (9, 4), (10, 4)],
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

# Euodia presses rose and myrtle oil for the goddess's altars. A narrow,
# high room that smells of roses: the copper still on the hearth, shelves of
# little alabaster bottles, the press, petals drying on every flat surface
# including the bed, and one window, always shut.
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
    rugs=[("red", 1, 5, 3, 3)],
    stamps=[
        ("herbs", 0, 0), ("soot", 1, 0), ("hearth", 1, 2), ("jar_shelf", 3, 0), ("window", 5, 0), ("herbs", 6, 0), ("amphora_plain", 0, 3),
        ("myrtle", 6, 3), ("mortar", 4, 4), ("amphora", 6, 6),
        ("kline", 4, 7), ("myrtle", 1, 8),
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
# her grandson's, kept as he left it: the narrow bed still made, the clay helmet
# he made as a child, and a window on the empty slips. After the climax Lithos
# sits by his bed.
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
        # the back room
        ("chest", 4, 1), ("window", 6, 0), ("niche", 8, 0), ("kline", 7, 3), ("stool", 4, 4),
        # the front room: the divider is its back wall
        ("loom", 1, 5), ("nets", 6, 5), ("nets", 8, 5),
        ("kalathos", 3, 8), ("fish_basket", 8, 8), ("table_round", 8, 10), ("stool", 7, 10),
        ("pithos", 1, 9),
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
# back, open on the slip side: oars and tools on the wall, a model of the kind of
# ship his family is blamed for, his bed and chest in the corner, posts where the
# shed opens on the slip, and in the middle, a barrel for a table with
# knucklebones on it.
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
        ("oars", 1, 0), ("oars", 2, 0), ("trident", 3, 0), ("boat", 4, 0), ("window", 6, 0),
        ("chest", 8, 1),
        ("kline", 8, 4), ("lampstand", 10, 4),
        ("column", 12, 3), ("column", 12, 6),
        ("table_round", 4, 5), ("knucklebones", 5, 5), ("stool", 3, 5), ("stool", 4, 6),
        ("amphora_plain", 1, 4), ("pithos", 1, 6),
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


# Skandeia's Asclepeion: a harbor one, long and low, with the sea-water bath
# where sailors soak their hands beside the healer's spring, the Pithos as a tall
# jar by the window end, couches for the sailors along the far wall, and the
# healer's Panacoil curled on the counter.
def skandeia_asclepeion():
    r = Civic(19, 8, asc_floor)
    civic_walls(r, "asc")
    asc_shadow_row(r)
    asc_healer(r, 5, 2, 8)
    r.put("asc_votive_wall", 6, 1, 2, 1)
    r.put("asc_votive_counter", 6, 2, 2, 1)
    r.put("asc_basin", 11, 1, 2, 2)                 # the sea-water bath
    r.put("asc_jar", 14, 1, 1, 2)
    r.put("asc_pithos", 15, 0, 2, 3)
    r.put("asc_jar", 17, 1, 1, 2)
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


# Teukros sells rope, oil, myrtle and Frankincense in a rope-and-sailcloth hall:
# the stall under a sailcloth awning on the right, Frankincense on the high
# shelves and myrtle bundles from the beam on the left, oil jars by the posts.
def skandeia_agora():
    r = Civic(11, 9, "ago_floor")
    civic_walls(r, "ago")
    r.row(2, 0, ["ago_floor_sh"] * 11)
    r.put("ago_shelf", 1, 0, 1, 3)
    r.put("ago_shelf", 2, 0, 1, 3)
    r.put("ago_herbs", 3, 0, 1, 2)
    r.put("ago_herbs", 4, 0, 1, 2)
    r.put("ago_cloth_blue", 5, 0, 1, 2)
    r.put("ago_awning", 6, 0, 3, 2)
    r.row(2, 6, ["ago_counter_l", "ago_counter_staff", "ago_counter_r"])
    r.row(3, 6, ["ago_counter_front_l", "ago_counter_front_m", "ago_counter_front_r"])
    r.put("ago_cloth_saffron", 9, 0, 1, 2)
    r.put("ago_amphora", 10, 3, 1, 2)
    r.put("ago_column", 2, 5, 1, 3)
    r.put("ago_column", 8, 5, 1, 3)
    r.put("ago_amphora", 3, 6, 1, 2)
    r.put("ago_jar", 7, 6, 1, 2)
    r.put("ago_jar", 0, 7, 1, 2)
    r.set(0, 3, "ago_basket_olives")
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
# take the warm red dado. Mirrors hang by every door.
# --------------------------------------------------------------------------

# Peristera keeps the temple's doves. A round tower house: her stove and bed
# below, the nesting floor up the ladder, and by the stove a wool basket with
# one egg in it that is not a dove's.
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
        ("niche", 1, 0), ("soot", 2, 0), ("hearth", 2, 2), ("window", 4, 0), ("herbs", 5, 0),
        ("stairs_up", 6, 0), ("niche_horse", 8, 0),
        ("kalathos", 4, 3), ("pithos", 8, 3), ("pots", 1, 4),
        ("kline", 6, 5), ("stool", 2, 6),
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

# Lysis, a shy young potter, and his sister. The workshop: a wheel by the door,
# the kiln, shelves of perfume flasks drying (every one with the same little
# painted fish), pots everywhere, and a ladder up to the beds. The left part of
# the house is older and its wall stands further forward.
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
        ("stairs_up_r", 1, 2), ("jar_shelf", 4, 0), ("honey_shelf", 6, 0), ("soot", 8, 0),
        ("hearth", 8, 2), ("window", 11, 0), ("pithos", 11, 3),
        ("pots", 6, 4), ("pots", 7, 5), ("amphora", 11, 6), ("amphora_plain", 9, 6),
        ("table_round", 5, 6), ("stool", 6, 6),
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
# counter on the shady side, beds under a colonnade on the other, a little
# fountain the doves bathe in, and Panacoil asleep in the rose bed.
def paphia_asclepeion():
    def fill(x, y):
        if 6 <= x <= 9 and 3 <= y <= 8:
            return "aka_grass_flowers" if (x * 5 + y * 3) % 4 == 0 else "aka_grass"
        return asc_floor(x, y)
    r = Civic(15, 11, fill)
    civic_walls(r, "asc")
    asc_shadow_row(r)
    asc_healer(r, 3, 0, 4)
    r.put("asc_basin", 7, 1, 2, 2)                  # the doves' fountain
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
# counter and on the wall behind; incense and honey in the jars.
def paphia_agora():
    r = Civic(13, 9, asc_floor)
    civic_walls(r, "asc")
    asc_shadow_row(r)
    r.set(2, 2, "asc_counter_l")
    for x in (3, 4, 5, 9):
        r.set(x, 2, "asc_counter_m")
    r.set(6, 2, "asc_counter_staff")
    r.put("asc_votive_counter", 7, 2, 2, 1)
    r.set(10, 2, "asc_counter_r")
    r.row(3, 2, ["asc_counter_front_l"] + ["asc_counter_front_m"] * 7 + ["asc_counter_front_r"])
    r.put("asc_votive_wall", 3, 1, 2, 1)
    r.put("asc_votive_wall", 7, 1, 2, 1)
    r.put("asc_jar", 0, 1, 1, 2)
    r.put("asc_jar", 12, 1, 1, 2)
    for x in (1, 4, 8, 11):
        r.put_checkered("asc_column", x, 5, 1, 3)
    r.put_checkered("asc_brazier", 6, 5, 1, 2)
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
# she answered. His workshop: the roofed half on the left, with the chisels, the
# table set for two, his narrow bed and, in the corner under a dust sheet, the
# statue he started before her; the open yard on the right, where the blocks
# wait under the laurel.
def pygmalion():
    def fill(x, y):
        if x >= 8:
            if y == 2:
                return "aka_grass_sh"
            return "aka_grass_flowers" if (x * 3 + y * 7) % 9 == 0 else "aka_grass"
        if x <= 2 and 2 <= y <= 7:                   # his marble-paved corner
            return ("asc_floor_a_sh" if (x + y) % 2 == 0 else "asc_floor_b_sh") if y == 2 else asc_floor(x, y)
        if y == 2:
            return "aka_floor_sh" if x % 3 else "aka_floor_b_sh"
        return "aka_floor" if (x * 7 + y * 3) % 5 else "aka_floor_b"
    r = Civic(13, 10, fill)
    civic_walls(r, "aka", 0, 7)
    r.row(0, 8, ["aka_hedge_top"] * 5)
    r.row(1, 8, ["aka_hedge"] * 5)
    r.put("asc_statue", 1, 0, 1, 3)                 # under its dust sheet
    r.put_checkered("asc_kline", 0, 5, 2, 2)        # the narrow bed
    r.put("aka_specimens", 4, 1, 1, 2)
    r.put("aka_desk", 4, 4, 2, 2)                   # the table set for two
    r.set(3, 4, "aka_stool")
    r.set(6, 4, "aka_stool")
    r.set(7, 3, "aka_tools")
    r.set(4, 8, "aka_head")
    r.set(7, 7, "aka_crate")
    r.set(7, 8, "aka_crate")
    r.put("aka_amphora", 6, 2, 1, 2)
    r.put("aka_laurel", 11, 2, 2, 3)
    r.put("aka_bench", 9, 5, 2, 1)
    r.put("aka_bench", 10, 8, 2, 1)
    r.set(3, 9, "aka_mat")
    return r


room(
    name=f"{PA}_PygmalionsWorkshop", title="Pygmalion's workshop, Paphia", town="paphia", kind="civic",
    build=pygmalion,
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
# are lined with them, a turning mirror stands on its post as the ones in the
# rose court do, and the polishing bench and the mold wait by the door.
def mirror_house():
    r = Civic(11, 8, lambda x, y: "aka_floor" if (x * 5 + y * 3) % 4 else "aka_floor_b")
    civic_walls(r, "aka")
    for x in range(11):
        r.set(x, 2, "aka_floor_sh" if x % 3 else "aka_floor_b_sh")
    r.put("aka_map", 1, 0, 2, 2)
    r.put("aka_map", 4, 0, 2, 2)
    r.put("aka_map", 8, 0, 2, 2)
    r.put("aka_specimens", 7, 1, 1, 2)
    r.put("aka_armillary", 8, 4, 1, 2)
    r.put("aka_worktable", 2, 4, 2, 2)
    r.set(4, 5, "aka_stool")
    r.set(1, 4, "aka_tools")
    r.set(10, 3, "aka_crate")
    r.put("aka_amphora", 0, 6, 1, 2)
    r.put("aka_amphora", 10, 6, 1, 2)
    r.set(5, 7, "aka_mat")
    return r


room(
    name=f"{PA}_MirrorHouse", title="The mirror-house, Paphia", town="paphia", kind="civic",
    build=mirror_house,
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
# his walled yard, where the old tree that hasn't fruited "since the goddesses
# quarrelled" stands; across a stone threshold, the farmhouse kitchen at the
# back: apple racks and crates, all empty but one, the table, his tools, and a
# painted plate with a golden apple on it.
def orchard_house():
    def fill(x, y):
        if y >= 7:
            return "aka_grass_flowers" if (x * 3 + y * 5) % 8 == 0 else "aka_grass"
        if y == 6:
            return "aka_stylobate"
        if y == 2:
            return "aka_floor_sh" if x % 3 else "aka_floor_b_sh"
        return "aka_floor" if (x * 7 + y * 3) % 5 else "aka_floor_b"
    r = Civic(13, 11, fill)
    civic_walls(r, "aka")
    r.put("aka_scrolls", 1, 0, 2, 3)               # the apple racks
    r.put("aka_map", 5, 0, 2, 2)                   # the painted plate
    r.put("aka_specimens", 9, 1, 1, 2)
    r.put("aka_amphora", 12, 2, 1, 2)
    r.set(3, 3, "aka_crate")
    r.set(10, 4, "aka_crate")
    r.set(11, 4, "aka_crate")
    r.put("aka_desk", 5, 4, 2, 2)
    r.set(4, 4, "aka_stool")
    r.set(7, 4, "aka_stool")
    r.set(1, 5, "aka_tools")
    r.put("aka_laurel", 6, 7, 2, 3)                # the old tree
    r.put("aka_bench", 10, 9, 2, 1)
    r.set(2, 10, "aka_mat")
    return r


room(
    name=f"{PA}_OrchardHouse", title="The orchard house, Paphia", town="paphia", kind="civic",
    build=orchard_house,
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
# The Neraida falls
# --------------------------------------------------------------------------

# Myles's mill, the one still turning: a round room round the great millstone
# on its shaft, sacks and jars of grain, flour on everything, the bread oven in
# the wall, the ladder to his bed in the loft, and a cat white with flour.
room(
    name="KytheraNeraidaFalls_Mill", title="Myles's mill, the Neraida falls", town="falls", kind="oikia",
    floor="flags", wall="red",
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
    rugs=[("red", 1, 6, 3, 2)],
    stamps=[
        ("soot", 2, 0), ("hearth", 2, 2), ("herbs", 4, 0), ("window", 5, 0), ("honey_shelf", 6, 0),
        ("stairs_up_r", 8, 0), ("niche", 10, 0), ("window", 11, 0),
        ("column", 6, 4), ("mortar", 5, 6), ("mortar", 7, 6),     # the millstone on its shaft
        ("pithos", 10, 3), ("pithos", 10, 5), ("kalathos", 9, 7), ("amphora_plain", 1, 3),
        ("table", 2, 5), ("stool", 4, 5),
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
# the hearth, the hoe on its pegs, barley, and on a shelf the things he dug up
# looking for her arms.
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
        ("soot", 1, 0), ("hearth", 1, 2), ("jar_shelf", 4, 0), ("niche", 6, 0), ("window", 7, 0),
        ("trident", 8, 0), ("herbs", 9, 0), ("window", 11, 0),
        ("mortar", 4, 3), ("pithos", 3, 3), ("kline", 10, 3), ("table", 6, 4), ("stool", 8, 4),
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
# pad, cores of glass on a shelf, and on the wall a round mirror of polished
# black glass. The front of the house is older and its wall comes forward.
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
        ("herbs", 0, 1), ("herbs", 3, 1), ("chest", 1, 2), ("jar_shelf", 5, 0), ("window", 7, 0), ("klepsydra", 8, 0),
        ("mortar", 5, 4), ("stool", 6, 4), ("desk", 1, 5),
        ("amphora_plain", 8, 3), ("kline", 6, 6),
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
# over their boat. Downstairs the boat sits on rollers on the stone slip and the
# sea comes in under the painted doors; the stair goes up to the room over it.
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
    rugs=[("blue", 6, 6, 5, 2)],
    stamps=[
        ("nets", 0, 0), ("oars", 2, 0), ("oars", 3, 0), ("window", 5, 0), ("trident", 6, 0),
        ("stairs_up_r", 9, 0),
        ("fish_basket", 1, 3), ("fish_basket", 2, 3), ("amphora_plain", 11, 3), ("pithos", 1, 5),
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
        ("stairs_down", 1, 0), ("nets", 3, 0), ("window", 6, 0), ("soot", 7, 0), ("hearth", 7, 2),
        ("kline", 5, 4), ("kalathos", 7, 5), ("table_round", 2, 3), ("stool", 3, 3), ("fish_basket", 9, 5),
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

_BASE = None


def oikia_base():
    """The committed tileset's cells: the slice rooms and the catalogs."""
    global _BASE
    if _BASE is None:
        base = dict(R.ROOMS)
        base.update(R.catalog(A.STAMPS))
        composed = {n: B.compose(s) for n, s in base.items()}
        order0, ids0 = B.collect(composed)
        for name in R.ROOMS:
            committed = np.fromfile(ROOT / f"design/phase1/rooms/{name}.bin", "<u2")
            if not np.array_equal(B.blockdata(composed[name], ids0[name]), committed):
                raise SystemExit(f"kythera_homes: {name} no longer matches its committed blockdata; "
                                 "rebuild oikia first")
        _BASE = (composed, order0, {c.key(): i for i, c in enumerate(order0)})
    return _BASE


def compose_oikia(spec):
    """(blocks, behaviors, w, h, missing) for an oikia room; missing lists the
    cells gTileset_Oikia doesn't have, as (x, y, what's there)."""
    composed, order0, index = oikia_base()
    cells = B.compose(spec)
    h, w = len(cells), len(cells[0])
    missing = []
    for y in range(h):
        for x in range(w):
            if cells[y][x].key() not in index:
                what = [n for (n, sx, sy) in spec["stamps"]
                        if sx <= x < sx + A.STAMPS[n]["w"] and sy <= y < sy + A.STAMPS[n]["h"]]
                missing.append((x, y, ",".join(what) or "floor"))
    if missing:
        return None, None, w, h, missing
    blocks = np.zeros(w * h, "<u2")
    beh = [["MB_NORMAL"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            c = cells[y][x]
            blocks[y * w + x] = (0x200 + index[c.key()]) | c.block
            beh[y][x] = c.behavior
    return blocks, beh, w, h, []


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


def compose_civic(build):
    ct.define() if not ct.METATILES else None
    r = build()
    blocks = np.zeros(r.w * r.h, "<u2")
    beh = [["MB_NORMAL"] * r.w for _ in range(r.h)]
    for y in range(r.h):
        for x in range(r.w):
            m = ct.METATILES[ct.BY_NAME[r.grid[y][x]]]
            blocks[y * r.w + x] = (ct.FIRST_ID + ct.BY_NAME[r.grid[y][x]]) | (SOLID if m["solid"] else WALK)
            beh[y][x] = m["behavior"]
    return blocks, beh, r.w, r.h


def compose(rm):
    if rm["kind"] == "oikia":
        blocks, beh, w, h, missing = compose_oikia(rm)
        if missing:
            return None, None, w, h, missing
    else:
        blocks, beh, w, h = compose_civic(rm["build"])
    for (x, y) in rm["solid"]:
        blocks[y * w + x] = (blocks[y * w + x] & 0x03FF) | SOLID
    return blocks, beh, w, h, []


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
        "secondary_tileset": SECONDARY[rm["kind"]],
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
    kind = rm["kind"]
    if kind not in _RENDERERS:
        RM.read_fieldmap_constants()
        syms = RM.scan_tileset_symbols()
        _RENDERERS[kind] = RM.Renderer(RM.Tileset(RM.resolve_tileset(PRIMARY, syms)),
                                       RM.Tileset(RM.resolve_tileset(SECONDARY[kind], syms)))
    return np.array(RM.render_blocks(_RENDERERS[kind], blocks, w).convert("RGB"))


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

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--probe", action="store_true", help="only list the cells oikia lacks")
    ap.add_argument("--only", help="build one room")
    ap.add_argument("--review", metavar="DIR", help="also write the people renders here instead of IMG")
    args = ap.parse_args()

    ct.define()
    rooms = [r for r in ROOMS if not args.only or r["name"] == args.only]
    names = [r["name"] for r in ROOMS]
    assert len(names) == len(set(names)), "duplicate room"
    bad = []
    built = []
    for rm in rooms:
        blocks, beh, w, h, missing = compose(rm)
        if missing:
            bad.append(f"{rm['name']}: {len(missing)} cells not in gTileset_Oikia: " +
                       "; ".join(f"({x},{y}) {what}" for x, y, what in missing))
            continue
        if args.probe:
            continue
        probs = check(rm, blocks, beh, w, h)
        bad += probs
        built.append((rm, blocks, w, h))
    if bad:
        print("\n".join(bad))
        if args.probe:
            return
        raise SystemExit("kythera_homes: fix the rooms above")
    if args.probe:
        print("kythera_homes: every cell is in the tileset")
        return
    for rm, blocks, w, h in built:
        d = ROOT / "data/layouts" / rm["name"]
        d.mkdir(parents=True, exist_ok=True)
        blocks.astype("<u2").tofile(d / "map.bin")
        np.array([VOID[rm["kind"]]] * 4, "<u2").tofile(d / "border.bin")
        register(rm, w, h)
        write_map_json(rm)
        img = render(rm, blocks, w)
        save(img, IMG / f"{rm['name']}.png")
        out = Path(args.review) if args.review else IMG
        save(with_people(img, rm), out / f"{rm['name']}_people.png")
        print(f"kythera_homes: {rm['name']} {w}x{h} {rm['kind']}")


if __name__ == "__main__":
    main()
