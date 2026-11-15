#!/usr/bin/env python3
"""The interiors of Thyrsa and Eleutherai (Act II batch 1), on gTileset_Oikos
and gTileset_ThyrsaRooms.

  /usr/bin/python3 tools/ichor/maps/thyrsa_rooms.py              # everything
  /usr/bin/python3 tools/ichor/maps/thyrsa_rooms.py --no-compile # compose and preview only
  /usr/bin/python3 tools/ichor/maps/thyrsa_rooms.py --preview DIR

Each room below is a grid plus placements (tools/ichor/art/thyrsa_rooms_build.py
composes them), and its events. One run:
  1. composes the thirteen rooms and checks every 8x8 tile fits one palette,
  2. compiles gTileset_ThyrsaRooms with Porytiles and verifies it,
  3. writes data/layouts/<Layout>/{map,border}.bin and the layouts.json entries,
  4. writes each map.json's events from the room's spots (scripts.pory is
     hand-written and refers to them by script name and local id),
  5. checks every warp, person and readable thing is reachable from the door,
  6. renders each room from the compiled tileset over oikos to
     design/phase3/img/<MapDir>.png (2x), and refreshes the generated tables in
     design/phase3/ROOMS_thyrsa.md.

Grid legend: '#' void; wall and floor characters per room ('W' and '.' by
default). Spots:
  ("warp", label, [(x, y), ...], dest_map, dest_warp)
  ("npc", label, (x, y), facing, {gfx, script, local, flag, move, range, trainer})
  ("bg", label, (x, y), (fx, fy, facing), script)
  ("coord", label, (x, y), var, value, script)
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))

import thyrsa_rooms_art as A  # noqa: E402
import thyrsa_rooms_kithairon  # noqa: E402,F401
import thyrsa_rooms_civic  # noqa: E402,F401
import thyrsa_rooms_homes  # noqa: E402,F401
import thyrsa_rooms_build as B  # noqa: E402

IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/ROOMS_thyrsa.md"


def npc(label, xy, facing, gfx, script, **kw):
    return ("npc", label, xy, facing, dict(gfx=gfx, script=script, **kw))


def bg(label, xy, frm, script):
    return ("bg", label, xy, frm, script)


def warp(tiles, dest, n):
    return ("warp", f"door to {dest} (its warp {n})", tiles, dest, n)


def coord(label, xy, var, value, script):
    return ("coord", label, xy, var, value, script)


G = "OBJ_EVENT_GFX_ICHOR_"

ROOMS = {
    # ======================================================================
    # Eleutherai (beat 27): a border fort on its crag, the god's empty temple
    # ======================================================================
    "Eleutherai_WatchHouse": {
        "title": "The watch-house, Eleutherai",
        "map": "MAP_ELEUTHERAI_WATCH_HOUSE", "layout": "LAYOUT_ELEUTHERAI_WATCH_HOUSE",
        "idea": "A long barrack inside the fort wall: bare ashlar, a beaten-earth floor. Three cots "
                "heads-to-the-wall under three shields; the spear rack and the captain's helmets; one "
                "arrow slit over the road; and at the far end the hearth, the soup cauldron on its chain. "
                "The dice table sits in the middle where the off-duty men can see the door.",
        "floor": "earth", "wall": "fort",
        "grid": ["WWWWWWWWWWWWWWWW",
                 "WWWWWWWWWWWWWWWW",
                 "................",
                 "................",
                 "................",
                 "................",
                 "................",
                 "................"],
        "stamps": [("shield_club", 1, 1), ("shield_ring", 2, 1), ("shield_club", 3, 1),
                   ("bunk", 1, 2), ("bunk", 2, 2), ("bunk", 3, 2),
                   ("arrow_slit", 5, 0), ("spear_rack", 7, 0), ("helmet_shelf", 10, 1),
                   ("pots", 12, 2), ("hearth_chain", 13, 1), ("pithos", 15, 2),
                   ("bench", 6, 3), ("dice_table", 6, 4), ("bench", 6, 5),
                   ("amphora_plain", 0, 5), ("fleece", 1, 5), ("chest", 13, 5), ("mat", 7, 7)],
        "spots": [
            warp([(7, 7), (8, 7)], "MAP_ELEUTHERAI", 0),
            npc("Opsimos the cook, at the hearth", (12, 3), "south", G + "MAN",
                "Eleutherai_WatchHouse_EventScript_Opsimos", local="LOCALID_WATCH_HOUSE_OPSIMOS"),
            npc("Captain Peneleos", (10, 5), "west", G + "HOPLITE",
                "Eleutherai_WatchHouse_EventScript_Peneleos", local="LOCALID_WATCH_HOUSE_PENELEOS"),
            npc("Timolaos, the recruit (TRAINER_ICHOR_TIMOLAOS)", (9, 2), "south", G + "YOUTH_M",
                "Eleutherai_WatchHouse_EventScript_Timolaos", local="LOCALID_WATCH_HOUSE_TIMOLAOS"),
            bg("arrow slit", (5, 1), (5, 2, "north"), "Eleutherai_WatchHouse_EventScript_ArrowSlit"),
            bg("spear rack", (8, 2), (8, 3, "north"), "Eleutherai_WatchHouse_EventScript_Spears"),
            bg("dice table", (6, 4), (5, 4, "east"), "Eleutherai_WatchHouse_EventScript_DiceTable"),
            bg("cauldron", (14, 3), (14, 4, "north"), "Eleutherai_WatchHouse_EventScript_Cauldron"),
        ],
    },
    "Eleutherai_OinoeHouse": {
        "title": "Oinoe's house, Eleutherai",
        "map": "MAP_ELEUTHERAI_OINOE_HOUSE", "layout": "LAYOUT_ELEUTHERAI_OINOE_HOUSE",
        "idea": "One whitewashed room beside the empty temple. Everything in it is for the god who left: "
                "the ivy band on the loom, the garlands drying on the beam, the little dog-faced god in his "
                "niche between them, and a row of brooms worn shorter one by one. Her own bed is a pallet.",
        "floor": "earth", "wall": "eleu",
        "grid": ["WWWWWWWWW",
                 "WWWWWWWWW",
                 ".........",
                 ".........",
                 ".........",
                 ".........",
                 "........."],
        "stamps": [("loom_ivy", 0, 0), ("kalathos", 2, 2), ("garlands", 3, 0), ("god_niche", 4, 0),
                   ("garlands", 5, 0), ("window", 6, 0), ("brooms", 7, 1), ("pots", 0, 4),
                   ("table_round", 3, 4), ("stool", 4, 4), ("pallet", 7, 4),
                   ("mat", 3, 6), ("broom_stub", 5, 6)],
        "spots": [
            warp([(3, 6), (4, 6)], "MAP_ELEUTHERAI", 1),
            npc("Oinoe", (5, 3), "south", G + "ELDER_F", "Eleutherai_OinoeHouse_EventScript_Oinoe",
                local="LOCALID_OINOE_HOUSE_OINOE"),
            bg("the god in his niche", (4, 1), (4, 2, "north"), "Eleutherai_OinoeHouse_EventScript_Niche"),
            bg("the brooms", (7, 2), (7, 3, "north"), "Eleutherai_OinoeHouse_EventScript_Brooms"),
            bg("the loom", (1, 2), (1, 3, "north"), "Eleutherai_OinoeHouse_EventScript_Loom"),
            bg("the stub of a broom", (5, 6), (5, 5, "south"), "Eleutherai_OinoeHouse_EventScript_StubBroom"),
        ],
    },
    "Eleutherai_LysidikeHouse": {
        "title": "Lysidike's house, Eleutherai",
        "map": "MAP_ELEUTHERAI_LYSIDIKE_HOUSE", "layout": "LAYOUT_ELEUTHERAI_LYSIDIKE_HOUSE",
        "idea": "A herder's farmhouse: the lambing pen takes a whole corner, a lamb asleep in its straw; "
                "new cheeses dry on a board by the milk pails; the hearth is the middle of the house. The "
                "twins' cots stand side by side and could not be less alike: a lyre on one, lead weights "
                "on the other.",
        "floor": "earth", "wall": "eleu",
        "grid": ["WWWWWWWWWWWW",
                 "WWWWWWWWWWWW",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............"],
        "stamps": [("window", 1, 0), ("cot_lyre", 2, 2), ("cot_weights", 3, 2), ("herbs", 4, 0),
                   ("soot", 5, 0), ("hearth", 5, 2), ("cheese_shelf", 7, 1), ("milk_pails", 7, 2),
                   ("pen", 9, 2), ("fleece", 0, 4), ("pithos", 0, 5), ("stool", 3, 5), ("table", 4, 5),
                   ("stool", 6, 5), ("amphora", 11, 6), ("mat", 5, 7)],
        "spots": [
            warp([(5, 7), (6, 7)], "MAP_ELEUTHERAI", 2),
            npc("Lysidike, at the hearth", (7, 3), "west", G + "WOMAN", "Eleutherai_LysidikeHouse_EventScript_Lysidike",
                local="LOCALID_LYSIDIKE_HOUSE_LYSIDIKE"),
            npc("Amphis, by his cot", (2, 4), "south", G + "KID_M", "Eleutherai_LysidikeHouse_EventScript_Amphis",
                local="LOCALID_LYSIDIKE_HOUSE_AMPHIS"),
            npc("Zetes, by his", (3, 4), "south", G + "KID_M", "Eleutherai_LysidikeHouse_EventScript_Zetes",
                local="LOCALID_LYSIDIKE_HOUSE_ZETES"),
            bg("the lambing pen", (10, 4), (10, 5, "north"), "Eleutherai_LysidikeHouse_EventScript_Pen"),
            bg("the cheese board", (8, 1), (8, 2, "north"), "Eleutherai_LysidikeHouse_EventScript_Cheeses"),
            bg("the hearth", (5, 3), (5, 4, "north"), "Eleutherai_LysidikeHouse_EventScript_Hearth"),
        ],
    },
    # ======================================================================
    # Thyrsa (beat 30): the god's own city
    # ======================================================================
    "ThyrsaCity_Asclepeion": {
        "title": "The Asclepeion of Thyrsa, round the spring of Dirke",
        "map": "MAP_THYRSA_CITY_ASCLEPEION", "layout": "LAYOUT_THYRSA_CITY_ASCLEPEION",
        "idea": "A courtyard, not a hall: the floor dappled under a vine pergola, the spring of Dirke "
                "in a sunken pool in the middle, its runnel carried under the healer's carved counter to "
                "the basin beside her. Asclepius stands at the basin's head with ivy on his staff, and "
                "every pergola post wears an actor's thank-offering mask.",
        "floors": {".": "flags", ",": "dappled"}, "wall": "thyrsa", "ivy": True,
        "grid": ["WWWWWWWWWWWWWWW",
                 "WWWWWWWWWWWWWWW",
                 "...............",
                 "...............",
                 ".,,,,,,,,,,,,,.",
                 ".,,,,,,,,,,,,,.",
                 ".,,,,,,,,,,,,,.",
                 ".,,,,,,,,,,,,,.",
                 ".,,,,,,,,,,,,,.",
                 ".,,,,,,,,,,,,,.",
                 "..............."],
        "stamps": [("lampstand", 0, 2), ("asc_statue", 4, 1), ("asc_basin", 5, 1), ("asc_counter", 5, 2), ("rod_relief", 7, 0),
                   ("pithos_great", 13, 1), ("lampstand", 14, 2),
                   ("runnel", 8, 4), ("spring_pool", 7, 5),
                   ("post_comic", 2, 4), ("vines_a", 3, 4), ("vines_b", 2, 6), ("post_tragic", 2, 7),
                   ("vines_a", 3, 7),
                   ("post_satyr", 12, 4), ("vines_b", 11, 4), ("vines_a", 12, 6), ("post_comic", 12, 7),
                   ("vines_b", 11, 7),
                   ("kline", 0, 9), ("kline", 13, 9), ("mat", 7, 10)],
        "spots": [
            warp([(7, 10), (8, 10)], "MAP_THYRSA_CITY", 0),
            npc("the healer, behind the counter", (7, 2), "south", G + "HEALER",
                "ThyrsaCity_Asclepeion_EventScript_Healer", local="LOCALID_THYRSA_HEALER"),
            npc("the satyr-actor with a bandaged ankle", (1, 8), "south", G + "SATYR",
                "ThyrsaCity_Asclepeion_EventScript_SatyrActor"),
            npc("the pilgrim with a headache", (13, 8), "south", G + "MAN",
                "ThyrsaCity_Asclepeion_EventScript_Pilgrim"),
            npc("the young healer", (10, 3), "west", G + "ACOLYTE_F",
                "ThyrsaCity_Asclepeion_EventScript_YoungHealer"),
            npc("Panacoil, coiled at the pool's rim", (10, 5), "west", "OBJ_EVENT_GFX_SPECIES(PANACOIL)",
                "ThyrsaCity_Asclepeion_EventScript_Panacoil"),
            bg("statue of Asclepius", (4, 2), (4, 3, "north"), "ThyrsaCity_Asclepeion_EventScript_Statue"),
            bg("the Pithos", (13, 2), (13, 3, "north"), "ThyrsaCity_Asclepeion_EventScript_Pithos"),
            bg("the spring of Dirke", (8, 6), (8, 7, "north"), "ThyrsaCity_Asclepeion_EventScript_Spring"),
        ],
    },
    "ThyrsaCity_Agora": {
        "title": "The Agora of Thyrsa, a covered market hall",
        "map": "MAP_THYRSA_CITY_AGORA", "layout": "LAYOUT_THYRSA_CITY_AGORA",
        "idea": "Two counters meet at right angles round a pyramid of amphorae: goods down the west "
                "side, wine and offerings along the north wall under a row of festival masks. The day's "
                "prices are chalked on a board; the treading vat waits empty by the back door for the "
                "vintage.",
        "floor": "terracotta", "wall": "thyrsa", "ivy": True,
        "grid": ["WWWWWWWWWWWWWW",
                 "WWWWWWWWWWWWWW",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 ".............."],
        "stamps": [("amphora_pyramid", 0, 2), ("mask_comic", 2, 0), ("mask_tragic", 3, 0),
                   ("mask_satyr", 4, 0), ("mask_king", 5, 0), ("mask_comic", 6, 0),
                   ("wine_counter", 3, 2), ("chalk_board", 7, 2), ("side_counter", 1, 4),
                   ("herbs", 8, 0), ("herbs", 10, 0), ("back_door", 11, 0), ("tread_vat", 12, 2), ("sacks", 12, 5), ("sacks", 13, 5), ("table", 9, 7), ("grape_basket", 4, 7), ("sacks", 5, 7),
                   ("amphora", 13, 6), ("amphora", 0, 8), ("mat", 6, 9)],
        "spots": [
            warp([(6, 9), (7, 9)], "MAP_THYRSA_CITY", 1),
            npc("the general stallkeeper, behind the goods counter", (0, 5), "east", G + "MERCHANT",
                "ThyrsaCity_Agora_EventScript_GoodsKeeper", local="LOCALID_THYRSA_AGORA_GOODS"),
            npc("the wine-and-offerings stallkeeper", (4, 2), "south", G + "HARVESTER_THYRSA",
                "ThyrsaCity_Agora_EventScript_WineKeeper", local="LOCALID_THYRSA_AGORA_WINE"),
            npc("the mask-seller (until the Dionysia is done)", (9, 3), "south", G + "ACTOR",
                "ThyrsaCity_Agora_EventScript_MaskSeller", flag="FLAG_ICHOR_DIONYSIA_DONE"),
            npc("a customer", (6, 6), "wander", G + "WOMAN", "ThyrsaCity_Agora_EventScript_Customer",
                range=(1, 1)),
            bg("the chalk board", (7, 3), (7, 4, "north"), "ThyrsaCity_Agora_EventScript_ChalkBoard"),
            bg("the treading vat", (12, 3), (12, 4, "north"), "ThyrsaCity_Agora_EventScript_Vat"),
            bg("the amphora pyramid", (1, 3), (2, 3, "west"), "ThyrsaCity_Agora_EventScript_Pyramid"),
        ],
    },
    "ThyrsaCity_Tavern": {
        "title": "The Kantharos, a cellar tavern",
        "map": "MAP_THYRSA_CITY_TAVERN", "layout": "LAYOUT_THYRSA_CITY_TAVERN",
        "idea": "Down five steps into a barrel vault: cool, dim, lamp-lit. A black-figure frieze runs "
                "round the walls, satyrs chasing maenads and the maenads winning. The great cup hangs "
                "over the bar; the floor sinks into a worn bowl round the knucklebones table, benches "
                "at its lip.",
        "floor": "darkflags", "wall": "cellar",
        "grid": ["WWWWWWWWWWWWW",
                 "WWWWWWWWWWWWW",
                 "WWWWWWWWWWWWW",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 "............."],
        "stamps": [("wall_lamp", 2, 2), ("wall_lamp", 6, 2), ("great_cup", 9, 2), ("wine_rack", 11, 2),
                   ("bar", 8, 3), ("amphora_plain", 0, 3), ("amphora", 1, 3),
                   ("bench", 3, 4), ("pit", 3, 5), ("kb_table", 4, 6), ("bench", 3, 8),
                   ("table_round", 10, 7), ("stool", 11, 7), ("stool", 9, 7), ("table_round", 1, 7), ("stool", 0, 7), ("stool", 2, 7), ("amphora", 12, 5),
                   ("stairs_up_s", 5, 9)],
        "spots": [
            warp([(5, 9), (6, 9)], "MAP_THYRSA_CITY", 2),
            npc("Aristomache, Thyrsa's champion, behind the bar", (9, 3), "south", G + "WOMAN",
                "ThyrsaCity_Tavern_EventScript_Aristomache", local="LOCALID_KANTHAROS_ARISTOMACHE"),
            npc("Phaidimos, at the table", (3, 6), "east", G + "ELDER_M",
                "ThyrsaCity_Tavern_EventScript_Phaidimos", local="LOCALID_KANTHAROS_PHAIDIMOS"),
            npc("Glauke, at the table", (5, 6), "west", G + "YOUTH_F",
                "ThyrsaCity_Tavern_EventScript_Glauke", local="LOCALID_KANTHAROS_GLAUKE"),
            bg("the frieze", (3, 2), (3, 3, "north"), "ThyrsaCity_Tavern_EventScript_Frieze"),
            bg("the knucklebones table", (4, 6), (4, 5, "south"), "ThyrsaCity_Tavern_EventScript_BonesTable"),
            bg("the great cup (from the bar's end)", (11, 3), (11, 4, "north"), "ThyrsaCity_Tavern_EventScript_GreatCup"),
        ],
    },
    "ThyrsaCity_PindarosHouse": {
        "title": "Pindaros's house: the poet's upper room",
        "map": "MAP_THYRSA_CITY_PINDAROS_HOUSE", "layout": "LAYOUT_THYRSA_CITY_PINDAROS_HOUSE",
        "idea": "An upper room up a stair from the courtyard. Half the back wall is pigeonholes of odes, "
                "each tagged with a victor; the writing table stands at the window with the lyre on its "
                "peg beside it. Three couches make a U round the table, one always made up for a guest. "
                "His own victor's tripod, won for a song, has the corner.",
        "floor": "boards", "wall": "thyrsa",
        "grid": ["WWWWWWWWWWWW",
                 "WWWWWWWWWWWW",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............"],
        "stamps": [("pigeonholes", 0, 0), ("pigeonholes", 2, 0), ("pigeonholes", 4, 0),
                   ("window", 7, 0), ("klismos_r", 6, 2), ("desk", 7, 2), ("lyre_peg", 9, 0),
                   ("victor_tripod", 11, 1), ("kline", 5, 3), ("kline_v", 4, 5), ("table", 5, 5),
                   ("kline_v_guest", 7, 5), ("amphora", 11, 5), ("lampstand", 0, 4),
                   ("stairs_down_s", 1, 8)],
        "spots": [
            warp([(1, 8), (2, 8)], "MAP_THYRSA_CITY", 8),
            npc("Pindaros, the host", (8, 4), "south", G + "ELDER_M",
                "ThyrsaCity_PindarosHouse_EventScript_Pindaros", local="LOCALID_PINDAROS"),
            bg("the pigeonholes of odes", (1, 1), (1, 2, "north"), "ThyrsaCity_PindarosHouse_EventScript_Odes"),
            bg("the writing table", (7, 2), (7, 3, "north"), "ThyrsaCity_PindarosHouse_EventScript_Desk"),
            bg("the lyre", (9, 1), (9, 2, "north"), "ThyrsaCity_PindarosHouse_EventScript_Lyre"),
            bg("the victor's tripod", (11, 2), (11, 3, "north"), "ThyrsaCity_PindarosHouse_EventScript_Tripod"),
            bg("the guest's couch", (7, 6), (7, 7, "north"), "ThyrsaCity_PindarosHouse_EventScript_GuestCouch"),
        ],
    },
    "ThyrsaCity_MantoHouse": {
        "title": "Manto's house, on the Kadmeia wall",
        "map": "MAP_THYRSA_CITY_MANTO_HOUSE", "layout": "LAYOUT_THYRSA_CITY_MANTO_HOUSE",
        "idea": "A dim room of old dark flags with one window, and it faces the sky. Birdcages hang "
                "from the beams with their doors open; the birds come and go. A tripod stands over a "
                "brazier long cold. Teiresias's cornel staff leans by the door, and feathers wait in "
                "pots, sorted by a woman who cannot see their colors.",
        "floor": "darkflags", "wall": "thyrsa",
        "grid": ["WWWWWWWWWW",
                 "WWWWWWWWWW",
                 "..........",
                 "..........",
                 "..........",
                 "..........",
                 "..........",
                 ".........."],
        "stamps": [("herbs", 0, 0), ("kalathos", 0, 2), ("cornel_staff", 2, 0), ("sky_window", 5, 0), ("tripod_cold", 3, 2),
                   ("feather_pots", 7, 2), ("pithos", 9, 4), ("pallet", 0, 6), ("stool", 6, 4),
                   ("cage_a", 2, 4), ("cage_b", 6, 2), ("cage_c", 8, 6), ("cage_b", 1, 3),
                   ("mat", 4, 7)],
        "spots": [
            warp([(4, 7), (5, 7)], "MAP_THYRSA_CITY", 7),
            npc("Manto", (5, 3), "south", G + "MANTO", "ThyrsaCity_MantoHouse_EventScript_Manto",
                local="LOCALID_MANTO_HOUSE_MANTO"),
            bg("the window to the sky", (5, 1), (5, 2, "north"), "ThyrsaCity_MantoHouse_EventScript_Window"),
            bg("the cold brazier", (3, 3), (3, 4, "north"), "ThyrsaCity_MantoHouse_EventScript_Brazier"),
            bg("the cornel staff", (2, 1), (2, 2, "north"), "ThyrsaCity_MantoHouse_EventScript_Staff"),
            bg("the feather pots", (7, 2), (7, 3, "north"), "ThyrsaCity_MantoHouse_EventScript_Feathers"),
        ],
    },
    "ThyrsaCity_VintnerHouse": {
        "title": "Staphylos's house: the vintner's press-house",
        "map": "MAP_THYRSA_CITY_VINTNER_HOUSE", "layout": "LAYOUT_THYRSA_CITY_VINTNER_HOUSE",
        "idea": "A farmhouse built round its own press. The treading floor stands waist-high in the "
                "middle, heaped with grapes, its spout running into the vat sunk before it; the beam "
                "press leans out of the back wall. Pitch-sealed jars line the west side, raisins dry "
                "on mats along the east, and the bronze panther keeps the family shrine.",
        "floor": "flags", "wall": "thyrsa", "ivy": True,
        "grid": ["WWWWWWWWWWWWWW",
                 "WWWWWWWWWWWWWW",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 ".............."],
        "stamps": [("window", 3, 0), ("pitch_jar", 0, 2), ("pitch_jar", 1, 2), ("pitch_jar", 0, 5),
                   ("beam_press", 5, 1), ("panther_shrine", 11, 1), ("tread_floor", 5, 3),
                   ("sunk_vat", 6, 6), ("grape_mats", 11, 4), ("grape_mats", 11, 6),
                   ("amphora", 13, 8), ("kalathos", 1, 8), ("grape_basket", 2, 4), ("grape_basket", 9, 6), ("mat", 6, 9)],
        "spots": [
            warp([(6, 9), (7, 9)], "MAP_THYRSA_CITY", 10),
            npc("Staphylos", (4, 6), "east", G + "VINTNER", "ThyrsaCity_VintnerHouse_EventScript_Staphylos",
                local="LOCALID_VINTNER_STAPHYLOS"),
            npc("Erigone", (10, 3), "west", G + "YOUTH_F_THYRSA", "ThyrsaCity_VintnerHouse_EventScript_Erigone",
                local="LOCALID_VINTNER_ERIGONE"),
            bg("the panther shrine", (11, 2), (11, 3, "north"), "ThyrsaCity_VintnerHouse_EventScript_Shrine"),
            bg("the beam press", (6, 2), (6, 3, "north"), "ThyrsaCity_VintnerHouse_EventScript_Press"),
            bg("the vat", (7, 6), (7, 7, "north"), "ThyrsaCity_VintnerHouse_EventScript_Vat"),
        ] + [coord("treading floor: a step", (x, y), "VAR_TEMP_2", 1,
                   "ThyrsaCity_VintnerHouse_EventScript_TreadStep")
             for y in (3, 4) for x in (5, 6, 7, 8)]
          + [coord("off the floor: the treading ends", xy, "VAR_TEMP_2", 1,
                   "ThyrsaCity_VintnerHouse_EventScript_TreadOff")
             for xy in ((4, 3), (4, 4), (9, 3), (9, 4), (8, 2))],
    },
    "ThyrsaCity_ActorHouse": {
        "title": "Polos's house: the old actor's narrow house",
        "map": "MAP_THYRSA_CITY_ACTOR_HOUSE", "layout": "LAYOUT_THYRSA_CITY_ACTOR_HOUSE",
        "idea": "Narrow and tall, and the back wall is faces: every mask he wore, labelled with the part, "
                "Elektra's among them. His boots stand on their shelf, the costume trunk sits under the "
                "window, the bronze mirror is worn bright. The urn stands alone on its own small table.",
        "floor": "boards", "wall": "thyrsa",
        "grid": ["WWWWWWW",
                 "WWWWWWW",
                 ".......",
                 ".......",
                 ".......",
                 ".......",
                 ".......",
                 ".......",
                 ".......",
                 "......."],
        "stamps": [("mask_king", 0, 0), ("mask_tragic", 1, 0), ("mask_elektra", 2, 0), ("mask_comic", 3, 0),
                   ("mask_satyr", 4, 0), ("boot_shelf", 0, 1), ("bronze_mirror", 3, 1),
                   ("window", 5, 0), ("costume_trunk", 5, 2), ("urn_table", 1, 5), ("klismos_l", 2, 5),
                   ("kline_v", 0, 7), ("lampstand", 6, 6), ("mat", 3, 9)],
        "spots": [
            warp([(3, 9), (4, 9)], "MAP_THYRSA_CITY", 5),
            npc("Polos", (4, 4), "south", G + "ACTOR", "ThyrsaCity_ActorHouse_EventScript_Polos",
                local="LOCALID_ACTOR_HOUSE_POLOS"),
            bg("the wall of masks", (2, 1), (2, 2, "north"), "ThyrsaCity_ActorHouse_EventScript_Masks"),
            bg("the boots", (0, 1), (0, 2, "north"), "ThyrsaCity_ActorHouse_EventScript_Boots"),
            bg("the bronze mirror", (3, 2), (3, 3, "north"), "ThyrsaCity_ActorHouse_EventScript_Mirror"),
            bg("the costume trunk", (5, 2), (5, 3, "north"), "ThyrsaCity_ActorHouse_EventScript_Trunk"),
            bg("the urn", (1, 5), (1, 6, "north"), "ThyrsaCity_ActorHouse_EventScript_Urn"),
        ],
    },
    "ThyrsaCity_EudoraHouse": {
        "title": "Eudora's house, and its courtyard",
        "map": "MAP_THYRSA_CITY_EUDORA_HOUSE", "layout": "LAYOUT_THYRSA_CITY_EUDORA_HOUSE",
        "idea": "Two rooms' worth of house under a partition wall, and through its doorway a walled "
                "courtyard of bare earth where the old fig stands over a patch of turned earth. Indoors, "
                "the soldier's cloak half-mended on the loom, his father's helmet on its peg by the "
                "door, and a bed made up that nobody sleeps in.",
        "floors": {".": "terracotta", ",": "earth"}, "walls": {"E": "eleu", "W": "thyrsa"},
        "grid": ["EEEEEEEEEEEEE",
                 "EEEEEEEEEEEEE",
                 ",,,,,,,,,,,,,",
                 ",,,,,,,,,,,,,",
                 ",,,,,,,,,,,,,",
                 "WWWWWWW.WWWWW",
                 "WWWWWWW.WWWWW",
                 ".............",
                 ".............",
                 ".............",
                 "............."],
        "stamps": [("fig_tree", 2, 2), ("turned_earth", 4, 4), ("amphora", 11, 2), ("stool", 9, 3),
                   ("pots", 10, 3), ("lintel", 7, 5), ("loom_cloak", 0, 5), ("window", 3, 5),
                   ("helmet_peg", 8, 6), ("chest", 9, 7), ("kline_v", 11, 7), ("table", 4, 8),
                   ("stool", 3, 8), ("stool", 6, 8), ("amphora", 0, 9), ("mat", 5, 10)],
        "spots": [
            warp([(5, 10), (6, 10)], "MAP_THYRSA_CITY", 6),
            npc("Eudora, at the loom", (2, 7), "west", G + "WOMAN_THYRSA", "ThyrsaCity_EudoraHouse_EventScript_Eudora",
                local="LOCALID_EUDORA_HOUSE_EUDORA"),
            npc("Hippias, asleep on his bed in his boots (after FLAG_ICHOR_GYPSOS_WENT_HOME)", (11, 8), "south",
                G + "YOUTH_M", "ThyrsaCity_EudoraHouse_EventScript_Hippias", local="LOCALID_EUDORA_HOUSE_HIPPIAS",
                flag="FLAG_TEMP_1"),
            bg("the turned earth under the fig (ICHOR_STUB_DIG)", (4, 4), (5, 4, "west"),
               "ThyrsaCity_EudoraHouse_EventScript_TurnedEarth"),
            bg("the fig", (3, 4), (2, 4, "east"),
               "ThyrsaCity_EudoraHouse_EventScript_Fig"),
            bg("the helmet on its peg", (8, 6), (8, 7, "north"), "ThyrsaCity_EudoraHouse_EventScript_Helmet"),
            bg("the loom", (1, 7), (1, 8, "north"),
               "ThyrsaCity_EudoraHouse_EventScript_Loom"),
        ],
    },
    "ThyrsaCity_MaskWorkshop": {
        "title": "Euthykles's workshop, the mask-maker's",
        "map": "MAP_THYRSA_CITY_MASK_WORKSHOP", "layout": "LAYOUT_THYRSA_CITY_MASK_WORKSHOP",
        "idea": "Long and low, and every surface has a face on it: blank linen masks drying on rows of "
                "wooden heads, painted ones pinned up to set, wigs on pegs, plaster and paint by the "
                "cutting bench. At the back, alone on a high shelf, one mask that is looking at you.",
        "floor": "terracotta", "wall": "thyrsa",
        "grid": ["WWWWWWWWWWWWWWWW",
                 "WWWWWWWWWWWWWWWW",
                 "................",
                 "................",
                 "................",
                 "................",
                 "................"],
        "stamps": [("mask_blank", 1, 1), ("mask_blank", 2, 1), ("mask_blank", 3, 1), ("mask_comic", 2, 0),
                   ("mask_tragic", 4, 0), ("mask_satyr", 5, 1), ("mask_blank", 6, 0), ("wig_pegs", 8, 0),
                   ("wig_pegs", 9, 0), ("window", 11, 0), ("high_shelf", 13, 1),
                   ("mask_heads", 1, 3), ("mask_heads", 4, 3), ("mask_heads", 1, 5),
                   ("cutting_bench", 9, 3), ("paint_pots", 12, 3), ("plaster_vat", 14, 3),
                   ("mask_heads", 12, 5), ("amphora", 15, 2), ("mat", 6, 6)],
        "spots": [
            warp([(6, 6), (7, 6)], "MAP_THYRSA_CITY", 4),
            npc("Euthykles, at the cutting bench", (10, 4), "north", G + "MERCHANT_THYRSA",
                "ThyrsaCity_MaskWorkshop_EventScript_Euthykles", local="LOCALID_MASK_WORKSHOP_EUTHYKLES"),
            npc("the mask on the high shelf (an object)", (13, 1), "south", G + "MASK",
                "ThyrsaCity_MaskWorkshop_EventScript_ShelfMask", local="LOCALID_MASK_WORKSHOP_MASK",
                flag="FLAG_ICHOR_TRADED_PROSOMIME"),
            bg("the wigs", (8, 1), (8, 2, "north"), "ThyrsaCity_MaskWorkshop_EventScript_Wigs"),
            bg("the masks drying on heads", (1, 3), (1, 4, "north"), "ThyrsaCity_MaskWorkshop_EventScript_Heads"),
            bg("the paint pots", (12, 3), (12, 4, "north"), "ThyrsaCity_MaskWorkshop_EventScript_Paint"),
        ],
    },
    "ThyrsaCity_SownHouse": {
        "title": "Chthonia's house, of the Sown Men",
        "map": "MAP_THYRSA_CITY_SOWN_HOUSE", "layout": "LAYOUT_THYRSA_CITY_SOWN_HOUSE",
        "idea": "The oldest house in the city: walls of huge rough stones, dark flags worn smooth. Over "
                "the hearth hangs the dragon's tooth; the family's old spears stand in their rack; five "
                "clay soldiers line the shelf, the five who were left standing.",
        "floor": "darkflags", "wall": "cyclopean",
        "grid": ["WWWWWWWWWWW",
                 "WWWWWWWWWWW",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "..........."],
        "stamps": [("clay_men", 0, 1), ("dragon_tooth", 3, 1), ("hearth", 3, 2), ("shield_club", 6, 1), ("spear_rack", 7, 0),
                   ("chest", 9, 1), ("kline", 0, 5), ("table_round", 6, 5), ("stool", 7, 5),
                   ("pithos", 10, 4), ("bench", 7, 7), ("mat", 4, 7)],
        "spots": [
            warp([(4, 7), (5, 7)], "MAP_THYRSA_CITY", 9),
            npc("Chthonia, by the hearth", (5, 3), "west", G + "MOM_THYRSA", "ThyrsaCity_SownHouse_EventScript_Chthonia",
                local="LOCALID_SOWN_HOUSE_CHTHONIA"),
            npc("Udaios, her grandson", (6, 4), "south", G + "KID_M_THYRSA", "ThyrsaCity_SownHouse_EventScript_Udaios",
                local="LOCALID_SOWN_HOUSE_UDAIOS"),
            bg("the hearth and the tooth over it", (3, 3), (3, 4, "north"), "ThyrsaCity_SownHouse_EventScript_Tooth"),
            bg("the five clay men", (0, 1), (0, 2, "north"), "ThyrsaCity_SownHouse_EventScript_ClayMen"),
            bg("the old spears", (7, 2), (7, 3, "north"), "ThyrsaCity_SownHouse_EventScript_Spears"),
            bg("the wall stones", (2, 1), (2, 2, "north"), "ThyrsaCity_SownHouse_EventScript_Walls"),
        ],
    },
}

FACING_MOVE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
               "west": "MOVEMENT_TYPE_FACE_LEFT", "east": "MOVEMENT_TYPE_FACE_RIGHT",
               "wander": "MOVEMENT_TYPE_WANDER_AROUND"}
BG_FACE = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
           "east": "BG_EVENT_PLAYER_FACING_EAST", "west": "BG_EVENT_PLAYER_FACING_WEST"}


def check_spots(name, spec, cells):
    """Every warp, NPC, coord and bg-reading tile is walkable and reachable from
    the room's door; each bg is read from the tile in front of it; no NPC stands
    where it would block the only way to something."""
    H, W = len(cells), len(cells[0])
    people = {s[2] for s in spec["spots"] if s[0] == "npc"}

    def open_(x, y, block_people=True):
        if not (0 <= x < W and 0 <= y < H) or cells[y][x].block == B.SOLID:
            return False
        return not (block_people and (x, y) in people)

    start = spec["spots"][0][2][0]
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in B.DIRS.values():
            n = (x + dx, y + dy)
            if n not in seen and open_(*n):
                seen.add(n)
                todo.append(n)
    errs = []

    def check(ok, msg):
        if not ok:
            errs.append(msg)
    for spot in spec["spots"]:
        kind, label = spot[0], spot[1]
        if kind == "warp":
            for t in spot[2]:
                check(t in seen, f"{name}: warp at {t} is unreachable")
                check(cells[t[1]][t[0]].behavior != "MB_NORMAL", f"{name}: {t} is not a warp tile")
        elif kind == "npc":
            x, y = spot[2]
            check(cells[y][x].block != B.SOLID or spot[4].get("on_furniture") or "object" in label \
                or "asleep" in label, f"{name}: npc '{label}' at {spot[2]} stands on furniture")
            near = [(x + dx, y + dy) for dx, dy in B.DIRS.values()]
            check(any(n in seen for n in near) or spot[2] in seen or \
                any(cells[n[1]][n[0]].behavior == "MB_COUNTER" for n in near if 0 <= n[0] < W and 0 <= n[1] < H), \
                f"{name}: npc '{label}' at {spot[2]} can't be reached")
        elif kind == "coord":
            check(cells[spot[2][1]][spot[2][0]].block != B.SOLID, f"{name}: coord {spot[2]} is solid")
        elif kind == "bg":
            at, (fx, fy, facing) = spot[2], spot[3]
            check((fx, fy) in seen, f"{name}: bg '{label}' is read from {(fx, fy)}, which is unreachable")
            dx, dy = B.DIRS[facing]
            check((fx + dx, fy + dy) == at, f"{name}: bg '{label}': {(fx, fy)} facing {facing} misses {at}")
    if errs:
        raise SystemExit("\n".join(errs))
    return seen


def map_events(spec):
    objs, warps, coords, bgs = [], [], [], []
    for s in spec["spots"]:
        if s[0] == "warp":
            for (x, y) in s[2]:
                warps.append({"x": x, "y": y, "elevation": 0, "dest_map": s[3], "dest_warp_id": str(s[4])})
        elif s[0] == "npc":
            d = s[4]
            o = {}
            if d.get("local"):
                o["local_id"] = d["local"]
            rx, ry = d.get("range", (0, 0))
            o.update({"graphics_id": d["gfx"], "x": s[2][0], "y": s[2][1], "elevation": 3,
                      "movement_type": FACING_MOVE[s[3]], "movement_range_x": rx, "movement_range_y": ry,
                      "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
                      "script": d["script"], "flag": d.get("flag", "0")})
            objs.append(o)
        elif s[0] == "bg":
            bgs.append({"type": "sign", "x": s[2][0], "y": s[2][1], "elevation": 0,
                        "player_facing_dir": BG_FACE[s[3][2]], "script": s[4]})
        elif s[0] == "coord":
            coords.append({"type": "trigger", "x": s[2][0], "y": s[2][1], "elevation": 3,
                           "var": s[3], "var_value": str(s[4]), "script": s[5]})
    return objs, warps, coords, bgs


def write_map_json(name, spec):
    p = ROOT / f"data/maps/{name}/map.json"
    m = json.loads(p.read_text())
    assert m["id"] == spec["map"], (m["id"], spec["map"])
    objs, warps, coords, bgs = map_events(spec)
    m["object_events"], m["warp_events"], m["coord_events"], m["bg_events"] = objs, warps, coords, bgs
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def write_layouts(sizes):
    p = ROOT / "data/layouts/layouts.json"
    d = json.loads(p.read_text())
    want = {spec["layout"]: (name, sizes[name]) for name, spec in ROOMS.items()}
    for lay in d["layouts"]:
        if lay.get("id") in want:
            name, (w, h) = want[lay["id"]]
            lay["width"], lay["height"] = w, h
            lay["primary_tileset"] = "gTileset_Oikos"
            lay["secondary_tileset"] = B.TILESETS[tileset_of(name)][0]
            assert lay["blockdata_filepath"] == f"data/layouts/{name}/map.bin", lay
            del want[lay["id"]]
    assert not want, f"layouts not registered: {sorted(want)}"
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def room_doc(name, spec, cells):
    H, W = len(cells), len(cells[0])
    marks = {}
    keys = []
    for i, spot in enumerate(spec["spots"], 1):
        key = str(i) if i < 10 else chr(ord("a") + i - 10) if i < 36 else "*"
        keys.append(key)
        tiles = spot[2] if spot[0] == "warp" else [spot[2]]
        for t in tiles:
            marks.setdefault(t, key)
    out = [f"### {spec['title']}", "",
           f"- Map `{spec['map']}`, layout `{spec['layout']}`: **{W}x{H}**, `gTileset_Oikos` + `{B.TILESETS[tileset_of(name)][0]}`.",
           f"- Render: `design/phase3/img/{name}.png` (2x).", "",
           f"![{spec['title']}](img/{name}.png)", "",
           f"{spec['idea']}", "",
           "Walk map: `#` blocked, `.` open; digits and letters are the spots below (a bg event is "
           "marked on its furniture).", "", "```", "    " + "".join(str(x % 10) for x in range(W))]
    for y in range(H):
        out.append(f"{y:3d} " + "".join(marks.get((x, y), "." if cells[y][x].block != B.SOLID else "#")
                                        for x in range(W)))
    out += ["```", "", "| # | Kind | Tile | Detail | What |", "|---|---|---|---|---|"]
    coords_done = False
    for key, spot in zip(keys, spec["spots"]):
        kind, label = spot[0], spot[1]
        if kind == "warp":
            out.append(f"| {key} | warp | {', '.join(f'({x},{y})' for x, y in spot[2])} | "
                       f"to `{spot[3]}` warp {spot[4]} | the exit |")
        elif kind == "npc":
            out.append(f"| {key} | npc | ({spot[2][0]},{spot[2][1]}) | faces {spot[3]}, "
                       f"`{spot[4]['gfx']}` | {label} |")
        elif kind == "bg":
            fx, fy, f = spot[3]
            out.append(f"| {key} | bg | ({spot[2][0]},{spot[2][1]}) | read from ({fx},{fy}) facing {f} | {label} |")
        elif kind == "coord":
            if label.startswith("treading floor") or label.startswith("off the floor"):
                if coords_done == label:
                    continue
                coords_done = label
                tiles = [s[2] for s in spec["spots"] if s[0] == "coord" and s[1] == label]
                out.append(f"| {key} | coord | {', '.join(f'({x},{y})' for x, y in tiles)} | "
                           f"`{spot[3]}` = {spot[4]} | {label} |")
    out.append("")
    return "\n".join(out)


def splice(path, text):
    begin, end = "<!-- thyrsa_rooms: begin generated -->", "<!-- thyrsa_rooms: end generated -->"
    doc = path.read_text()
    a, b = doc.index(begin) + len(begin), doc.index(end)
    path.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])


# Which secondary each room is drawn from (thyrsa_rooms_build.TILESETS).
SET_OF = {
    "ThyrsaCity_Asclepeion": "rooms", "ThyrsaCity_Agora": "rooms",
    "ThyrsaCity_PindarosHouse": "rooms", "ThyrsaCity_ActorHouse": "rooms",
    "ThyrsaCity_VintnerHouse": "homes", "ThyrsaCity_EudoraHouse": "homes",
    "ThyrsaCity_MaskWorkshop": "homes", "ThyrsaCity_MantoHouse": "homes",
    "Eleutherai_WatchHouse": "stone", "Eleutherai_OinoeHouse": "stone",
    "Eleutherai_LysidikeHouse": "stone", "ThyrsaCity_Tavern": "stone", "ThyrsaCity_SownHouse": "stone",
}


def tileset_of(name):
    return SET_OF[name]


def build_set(which, names, composed, compile_it):
    """Merge, collect and (optionally) compile one secondary."""
    B.use(which)
    floors, walls = set(), set()
    for n in names:
        spec = ROOMS[n]
        floors |= set((spec.get("floors") or {".": spec["floor"]}).values())
        walls |= set((spec.get("walls") or {"W": spec["wall"]}).values())
    base = B.basics(set(), set())        # just the void: floors and walls come in as the rooms use them
    layouts = {n: composed[n] for n in names}
    merged = B.merge_near_duplicates(dict(layouts, _base=[base]))
    order, ids = B.collect(layouts, base)
    ntiles = B.count_tiles(order)
    print(f"{B.SYMBOL}: {len(order)} metatiles, {ntiles} tiles ({merged} near-duplicates merged)")
    if not compile_it:
        return order, ids, base, None
    B.write_sources(order)
    B.compile()
    return order, ids, base, B.verify()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true", help="compose, check and preview only")
    ap.add_argument("--preview", metavar="DIR", help="write source-composed previews (2x) here")
    ap.add_argument("--only", help="comma-separated rooms to preview")
    args = ap.parse_args()

    B.check_palettes()
    B.check_stamps()
    composed = {n: B.compose(s) for n, s in ROOMS.items()}
    for n, s in ROOMS.items():
        check_spots(n, s, composed[n])
    sets = {}
    for which in B.TILESETS:
        names = [n for n in ROOMS if tileset_of(n) == which]
        sets[which] = (names,) + build_set(which, names, composed, not args.no_compile)
    if args.preview:
        d = Path(args.preview)
        for n, cells in composed.items():
            if args.only and n not in args.only.split(","):
                continue
            B.save_scaled(B.image_of(cells), d / f"{n}.png", 2)
    if args.no_compile:
        return

    import subprocess
    sizes, docs, stats = {}, {}, []
    for which, (names, order, ids, base, (nmeta, ntiles, pals)) in sets.items():
        B.use(which)
        void_id = B.FIRST_METATILE + next(i for i, c in enumerate(order) if c.kind == "void")
        for n in names:
            cells = composed[n]
            H, W = len(cells), len(cells[0])
            sizes[n] = (W, H)
            blocks = B.blockdata(cells, ids[n])
            got = B.render_compiled(blocks, W)
            want = B.image_of(cells)
            if not np.array_equal(got, want):
                bad = np.argwhere((got != want).any(-1))
                raise SystemExit(f"thyrsa_rooms: {n} doesn't render as composed (first bad pixel {bad[0]})")
            d = ROOT / "data/layouts" / n
            d.mkdir(parents=True, exist_ok=True)
            blocks.tofile(d / "map.bin")
            np.array([void_id | B.SOLID] * 4, "<u2").tofile(d / "border.bin")
            B.save_scaled(got, IMG / f"{n}.png", 2)
            write_map_json(n, ROOMS[n])
            docs[n] = room_doc(n, ROOMS[n], cells)
            print(f"thyrsa_rooms: {n} {W}x{H} on {B.SYMBOL}")
        stats.append(f"- `{B.SYMBOL}` (`data/tilesets/secondary/{B.DIR}`): **{nmeta}** metatiles of 512, "
                     f"**{ntiles}** tiles of {B.TILE_LIMIT}, palettes {pals[0]}-{pals[-1]}. "
                     f"Sheet: `design/phase3/img/{B.DIR}_sheet.png`.")
        r = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", str(B.TS),
                            "--primary", "gTileset_Oikos", "--scale", "2", "-o", str(IMG / f"{B.DIR}_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            print(r.stderr)
    write_layouts(sizes)
    if DOC.exists():
        splice(DOC, "\n".join(stats) + "\n\n" + "\n".join(docs[n] for n in ROOMS))


if __name__ == "__main__":
    main()
