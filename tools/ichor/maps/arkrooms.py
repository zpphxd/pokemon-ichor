#!/usr/bin/env python3
"""The interiors of Styx Falls and Arkadia (Act II batch 3), on gTileset_Oikos
and three secondaries: gTileset_StyxRooms, gTileset_ArkadiaRooms and
gTileset_ArkadiaHomes.

  /usr/bin/python3 tools/ichor/maps/arkrooms.py              # everything
  /usr/bin/python3 tools/ichor/maps/arkrooms.py --no-compile --preview DIR

Each room below is a grid plus placements (tools/ichor/art/arkrooms_build.py
composes them), and its events. One run:
  1. composes the nine rooms and checks every 8x8 tile fits one palette,
  2. compiles the three secondaries with Porytiles and verifies them,
  3. writes data/layouts/<Layout>/{map,border}.bin and the layouts.json entries,
  4. writes each map.json's events from the room's spots (scripts.pory is
     hand-written and refers to them by script name and local id),
  5. checks every warp, person and readable thing is reachable from the door,
  6. renders each room from the compiled tileset over oikos to
     design/phase3/img/<MapDir>.png (2x), the one-sheet overview
     design/phase3/img/arkadia_interiors_overview.png, and refreshes the
     generated tables in design/phase3/ROOMS_arkadia.md.

Grid legend: '#' void; wall and floor characters per room. Spots:
  ("warp", label, [(x, y), ...], dest_map, dest_warp)
  ("npc", label, (x, y), facing, {gfx, script, local, flag, move, range})
  ("bg", label, (x, y), (fx, fy, facing), script)
  ("hidden", label, (x, y), item, flag)
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

import arkrooms_art as A  # noqa: E402
import arkrooms_styx  # noqa: E402,F401
import arkrooms_civic  # noqa: E402,F401
import arkrooms_homes  # noqa: E402,F401
import arkrooms_build as B  # noqa: E402

IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/ROOMS_arkadia.md"


def npc(label, xy, facing, gfx, script, **kw):
    return ("npc", label, xy, facing, dict(gfx=gfx, script=script, **kw))


def bg(label, xy, frm, script):
    return ("bg", label, xy, frm, script)


def hidden(label, xy, item, flag):
    return ("hidden", label, xy, item, flag)


def warp(tiles, dest, n):
    return ("warp", f"door to {dest} (its warp {n})", tiles, dest, n)


G = "OBJ_EVENT_GFX_ICHOR_"

ROOMS = {
    # ======================================================================
    # Styx Falls: Nonakris, the village at the foot of the black cliff (beat 39)
    # ======================================================================
    "StyxFalls_Inn": {
        "set": "styx",
        "title": "The Inn at the Falls, Nonakris",
        "map": "MAP_STYX_FALLS_INN", "layout": "LAYOUT_STYX_FALLS_INN",
        "idea": "A long, low room built back into the cirque: the back wall is the cliff itself, black "
                "and running wet, and the hearth is cut into it. The rest is whitewashed against the damp. "
                "The sleeping benches stand against the rock under their blankets; the long table takes "
                "the middle of the room. A window looks across the black pool at the falls, and over "
                "the door hangs a horse's hoof on a nail, the house's luck.",
        "floors": {".": "slate"}, "walls": {"R": "rock", "W": "nonakris"},
        "grid": ["RRRRRRRRRRRRWWWWW",
                 "RRRRRRRRRRRRWWWWW",
                 "RRRRRRRRRRRR.....",
                 ".................",
                 ".................",
                 ".................",
                 ".................",
                 ".................",
                 ".................",
                 "................."],
        "stamps": [("rock_hearth", 1, 1), ("sleep_bench_red", 5, 3), ("sleep_bench_blue", 7, 3),
                   ("sleep_bench_cream", 9, 3),
                   ("cup_shelf", 12, 0), ("window_falls", 14, 0), ("herbs", 16, 0),
                   ("bench4", 5, 5), ("long_table", 5, 6), ("bench4", 5, 8),
                   ("pithos", 16, 3), ("amphora_plain", 15, 3), ("piglet_basket", 15, 6), ("cloaks", 15, 0),
                   ("pots", 0, 3), ("firewood", 3, 3), ("puddle", 4, 3), ("puddle_b", 11, 3), ("puddle", 2, 4),
                   ("table_round", 14, 8), ("stool", 13, 8), ("stool", 15, 8), ("kalathos", 16, 9),
                   ("amphora", 0, 8), ("door_hoof", 7, 9)],
        "spots": [
            warp([(8, 9), (9, 9)], "MAP_STYX_FALLS", 0),
            npc("Aroanios the innkeeper, by his cup shelf", (13, 3), "south", G + "ELDER_M",
                "StyxFalls_Inn_EventScript_Aroanios", local="LOCALID_STYX_INN_AROANIOS"),
            npc("Eubouleus the swineherd, from Eleusa", (14, 6), "east", G + "SHEPHERD",
                "StyxFalls_Inn_EventScript_Eubouleus", local="LOCALID_STYX_INN_EUBOULEUS"),
            npc("Gryllos the Kaplet, in his basket (until he's given)", (15, 6), "west",
                "OBJ_EVENT_GFX_SPECIES(KAPLET)", "StyxFalls_Inn_EventScript_Gryllos",
                local="LOCALID_STYX_INN_GRYLLOS", flag="FLAG_ICHOR_GOT_GRYLLOS", on_furniture=True),
            npc("Alethea, at the long table (her first visit only)", (4, 7), "east", G + "ALETHEA",
                "StyxFalls_Inn_EventScript_Alethea", local="LOCALID_STYX_INN_ALETHEA", flag="FLAG_TEMP_1"),
            bg("the hoof over the door", (10, 9), (10, 8, "south"), "StyxFalls_Inn_EventScript_Hoof"),
            bg("the window", (14, 1), (14, 2, "north"), "StyxFalls_Inn_EventScript_Window"),
            bg("the hearth in the rock", (1, 3), (1, 4, "north"), "StyxFalls_Inn_EventScript_Hearth"),
            bg("the wet rock", (11, 2), (11, 3, "north"), "StyxFalls_Inn_EventScript_Rock"),
        ],
    },
    "StyxFalls_OathHouse": {
        "set": "styx",
        "title": "Horkia's house, where the oaths are kept",
        "map": "MAP_STYX_FALLS_OATH_HOUSE", "layout": "LAYOUT_STYX_FALLS_OATH_HOUSE",
        "idea": "A narrow house whose back wall is the cliff, black and wet. Ledges are cut into it and "
                "racks stand down both sides, and on every one stand hoof-cups, dozens, each tied with a "
                "scrap of linen with a name scratched on it. In the middle, the table with the wax tablet "
                "of the day's oaths; in the rock, the lamp that is never put out.",
        "floors": {".": "slate"}, "walls": {"R": "rock"},
        "grid": ["RRRRRRRRR",
                 "RRRRRRRRR",
                 "RRRRRRRRR",
                 ".........",
                 ".........",
                 ".........",
                 ".........",
                 ".........",
                 ".........",
                 "........."],
        "stamps": [("cup_ledge", 0, 1), ("cup_ledge1", 2, 2), ("lamp_niche", 4, 2), ("cup_ledge1", 6, 2),
                   ("cup_ledge", 7, 1), ("cup_ledge", 3, 0),
                   ("hoof_rack1", 0, 3), ("hoof_rack1", 0, 5), ("hoof_rack1", 8, 3), ("hoof_rack1", 8, 5),
                   ("oath_table", 3, 5), ("stool", 2, 5), ("puddle", 2, 3), ("puddle_b", 6, 3),
                   ("kalathos", 6, 7), ("bench2", 1, 9),
                   ("kline", 7, 8), ("pithos", 0, 8), ("mat", 4, 9)],
        "spots": [
            warp([(4, 9), (5, 9)], "MAP_STYX_FALLS", 1),
            npc("Horkia, keeper of the oaths", (5, 5), "west", G + "ELDER_F",
                "StyxFalls_OathHouse_EventScript_Horkia", local="LOCALID_STYX_OATH_HORKIA"),
            bg("the hoof-cups", (0, 4), (1, 4, "west"), "StyxFalls_OathHouse_EventScript_Cups"),
            bg("the hoof-cups (east)", (8, 4), (7, 4, "east"), "StyxFalls_OathHouse_EventScript_CupsEast"),
            bg("the wax tablet", (3, 5), (3, 6, "north"), "StyxFalls_OathHouse_EventScript_Tablet"),
            bg("the lamp", (4, 2), (4, 3, "north"), "StyxFalls_OathHouse_EventScript_Lamp"),
        ],
    },
    "StyxFalls_StoneHouse": {
        "set": "styx",
        "title": "Kepheus's house, and its lean-to",
        "map": "MAP_STYX_FALLS_STONE_HOUSE", "layout": "LAYOUT_STYX_FALLS_STONE_HOUSE",
        "idea": "A squat stone house under its slabs, and through the posts at its east end a lean-to of "
                "rough planks full of crowbars, mattocks and the stone-sledge on its runners, loaded "
                "again. On the trestle, his clay model of the cirque: the falls a dribble from a jug he "
                "tops up, the pool a dish that never quite fills. From the ceiling hangs a black stone "
                "with a hole worn through it.",
        "floors": {".": "slate", ",": "earth"}, "walls": {"W": "nonakris", "P": "planks"},
        "grid": ["WWWWWWWWWPPPPP",
                 "WWWWWWWWWPPPPP",
                 ".........,,,,,",
                 ".........,,,,,",
                 ".........,,,,,",
                 ".........,,,,,",
                 ".........,,,,,",
                 ".........,,,,,"],
        "stamps": [("soot", 0, 0), ("hearth", 0, 2), ("window", 6, 0), ("holed_stone", 4, 0),
                   ("kline", 7, 2), ("cirque_model", 3, 3), ("stool", 2, 4), ("chest", 0, 5),
                   ("crowbars", 10, 1), ("mattocks", 11, 1), ("rubble", 13, 2),
                   ("corner_post", 9, 1), ("sledge", 11, 4), ("rubble", 13, 6), ("amphora_plain", 8, 6), ("threshold", 4, 7)],
        "spots": [
            warp([(4, 7), (5, 7)], "MAP_STYX_FALLS", 2),
            npc("Kepheus, at his model", (5, 4), "west", G + "MAN",
                "StyxFalls_StoneHouse_EventScript_Kepheus", local="LOCALID_STYX_STONE_KEPHEUS"),
            bg("the clay model of the cirque", (4, 5), (4, 6, "north"), "StyxFalls_StoneHouse_EventScript_Model"),
            bg("the black stone with a hole in it", (4, 1), (4, 2, "north"), "StyxFalls_StoneHouse_EventScript_Stone"),
            bg("the stone-sledge", (11, 5), (10, 5, "east"), "StyxFalls_StoneHouse_EventScript_Sledge"),
            bg("the crowbars", (10, 2), (10, 3, "north"), "StyxFalls_StoneHouse_EventScript_Tools"),
            hidden("an Everstone in the rubble", (13, 6), "ITEM_EVERSTONE",
                   "FLAG_ICHOR_HIDDEN_STYX_KEPHEUS_EVERSTONE"),
        ],
    },
    # ======================================================================
    # Arkadia: a town in a cypress forest that wakes at dusk (beat 41)
    # ======================================================================
    "Arkadia_Asclepeion": {
        "set": "civic",
        "title": "The Asclepeion of Arkadia, against the outcrop",
        "map": "MAP_ARKADIA_ASCLEPEION", "layout": "LAYOUT_ARKADIA_ASCLEPEION",
        "idea": "A mountain Asclepeion built against the town's rock outcrop, so the back wall is bare grey "
                "limestone and the spring comes out of a cleft in it, into a basin beside the healer. From "
                "the basin it runs in a stone channel across the floor to a grating, and the room is full of "
                "the sound of water; patients step over it. Hunters' herbs dry under the beam, the Pithos "
                "stands in a dry niche cut in the rock, and the healer's Panacoil lies along the channel, "
                "where it's cool.",
        "floors": {".": "flags"}, "walls": {"O": "outcrop"},
        "grid": ["OOOOOOOOOOOOOOO",
                 "OOOOOOOOOOOOOOO",
                 "...............",
                 "...............",
                 "...............",
                 "...............",
                 "...............",
                 "...............",
                 "...............",
                 "...............",
                 "..............."],
        "stamps": [("jar_shelf", 0, 0), ("herbs_a", 2, 0), ("herbs_b", 3, 0), ("spring_basin", 5, 1),
                   ("ark_counter", 5, 2), ("rod_relief", 7, 1), ("herbs_a", 9, 0), ("herbs_b", 10, 0),
                   ("pithos_niche", 12, 0), ("pithos", 12, 0), ("herbs_a", 14, 0), ("lampstand", 14, 2),
                   ("mortar", 0, 2), ("channel_se", 4, 2), ("channel_v", 4, 3), ("channel_v", 4, 4),
                   ("channel_ne", 4, 5)] + [("channel_h", x, 5) for x in range(5, 13)] + [
                   ("channel_grate", 13, 5),
                   ("pallet_red", 0, 7), ("pallet_blue", 0, 9), ("pallet_red", 13, 8),
                   ("amphora", 14, 6), ("votive_table", 11, 9), ("bench2", 3, 9), ("mat", 7, 10)],
        "spots": [
            warp([(7, 10), (8, 10)], "MAP_ARKADIA", 0),
            npc("the healer, behind the counter", (7, 2), "south", G + "HEALER",
                "Arkadia_Asclepeion_EventScript_Healer", local="LOCALID_ARKADIA_HEALER"),
            npc("Panacoil, along the channel where it's cool", (10, 6), "west", "OBJ_EVENT_GFX_SPECIES(PANACOIL)",
                "Arkadia_Asclepeion_EventScript_Panacoil"),
            npc("the huntress with a bandaged arm", (2, 7), "west", G + "HUNTRESS",
                "Arkadia_Asclepeion_EventScript_Huntress"),
            npc("the old charcoal-burner", (12, 8), "east", G + "CHARCOALER",
                "Arkadia_Asclepeion_EventScript_Charcoaler"),
            npc("the young healer", (10, 3), "west", G + "ACOLYTE_F",
                "Arkadia_Asclepeion_EventScript_YoungHealer"),
            bg("the Pithos", (12, 1), (12, 2, "north"), "Arkadia_Asclepeion_EventScript_Pithos"),
            bg("the spring's channel", (4, 3), (3, 3, "east"), "Arkadia_Asclepeion_EventScript_Channel"),
            bg("the grating", (13, 5), (13, 6, "north"), "Arkadia_Asclepeion_EventScript_Grating"),
            bg("the herbs under the beam", (2, 1), (2, 2, "north"), "Arkadia_Asclepeion_EventScript_Herbs"),
        ],
    },
    "Arkadia_Agora": {
        "set": "civic",
        "title": "The Agora stall, round the great cypress",
        "map": "MAP_ARKADIA_AGORA", "layout": "LAYOUT_ARKADIA_AGORA",
        "idea": "A timber stall built round the foot of the town's biggest cypress, so the trunk stands in the "
                "middle of the shop with the shelves built round it, and its boughs are the roof. Hunting "
                "nets hang from them. On the wall, a rack of arrows (for show) and a deer's hide; on the "
                "counter, clay jars of moon-cakes for the goddess.",
        "floors": {".": "earth"}, "walls": {"T": "timber"},
        "grid": ["TTTTTTTTTTTTT",
                 "TTTTTTTTTTTTT",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 ".............",
                 "............."],
        "stamps": [("deer_hide", 0, 0), ("herbs_a", 2, 0), ("herbs_b", 3, 0), ("arrow_rack", 9, 0), ("bow", 11, 0),
                   ("cypress_trunk", 6, 2), ("roots", 6, 6), ("canopy", 4, 2),
                   ("trunk_shelf_l", 5, 4), ("trunk_shelf_r", 8, 4),
                   ("shop_counter", 1, 3), ("amphora", 0, 3), ("amphora_plain", 12, 2), ("nut_baskets", 10, 4),
                   ("fur_table", 10, 7), ("nut_baskets", 12, 6), ("pithos", 0, 7), ("kalathos", 1, 8),
                   ("mat", 6, 9)],
        "spots": [
            warp([(6, 9), (7, 9)], "MAP_ARKADIA", 1),
            npc("the stallkeeper, behind her counter", (2, 3), "south", G + "WOMAN",
                "Arkadia_Agora_EventScript_Stallkeeper", local="LOCALID_ARKADIA_AGORA_KEEPER"),
            bg("the jars of moon-cakes", (1, 4), (1, 5, "north"), "Arkadia_Agora_EventScript_MoonCakes"),
            bg("the rack of arrows", (9, 1), (9, 2, "north"), "Arkadia_Agora_EventScript_Arrows"),
            bg("the great cypress", (6, 5), (6, 6, "north"), "Arkadia_Agora_EventScript_Cypress"),
        ],
    },
    "Arkadia_NyktimosHall": {
        "set": "homes",
        "title": "Nyktimos's hall, the table laid for one more",
        "map": "MAP_ARKADIA_NYKTIMOS_HALL", "layout": "LAYOUT_ARKADIA_NYKTIMOS_HALL",
        "idea": "A long hearth hall of the oldest family in Arkadia, dark wood and smoke. Over the hearth hangs "
                "a great grey wolf pelt, and nobody sits under it. The long table is laid for one more guest "
                "than there are people in the house: at its end a bowl and a cup wait at an empty place. "
                "The old woman's loom stands by the window; a ladder climbs to the sleeping loft.",
        "floors": {".": "darkboards"}, "walls": {"S": "smoke"},
        "grid": ["SSSSSSSSSSSSSSSS",
                 "SSSSSSSSSSSSSSSS",
                 "................",
                 "................",
                 "................",
                 "................",
                 "................",
                 "................",
                 "................"],
        "stamps": [("ladder", 1, 0), ("boar_spears", 3, 0), ("wolf_pelt", 6, 0), ("hall_hearth", 6, 2),
                   ("window", 12, 0), ("loom", 13, 0), ("amphora", 0, 3), ("pithos", 15, 2),
                   ("feast_table", 5, 5), ("stool", 4, 6), ("stool", 10, 6), ("bear_rug", 6, 4),
                   ("cup_shelf", 10, 0), ("firewood", 9, 3), ("lampstand", 11, 2),
                   ("bench4", 5, 7), ("chest", 14, 6), ("amphora_plain", 0, 6), ("mat", 7, 8)],
        "spots": [
            warp([(7, 8), (8, 8)], "MAP_ARKADIA", 2),
            npc("Nyktimos, the xenia host, by his hearth", (5, 3), "south", G + "ELDER_M",
                "Arkadia_NyktimosHall_EventScript_Nyktimos", local="LOCALID_ARKADIA_NYKTIMOS"),
            npc("his old mother, at the loom", (13, 3), "north", G + "ELDER_F",
                "Arkadia_NyktimosHall_EventScript_Mother", local="LOCALID_ARKADIA_NYKTIMOS_MOTHER"),
            bg("the empty place", (9, 5), (10, 5, "west"), "Arkadia_NyktimosHall_EventScript_EmptyPlace"),
            bg("the wolf pelt over the hearth", (7, 3), (7, 4, "north"), "Arkadia_NyktimosHall_EventScript_Pelt"),
            bg("the ladder to the loft", (1, 2), (1, 3, "north"), "Arkadia_NyktimosHall_EventScript_Ladder"),
        ],
    },
    "Arkadia_KlymeneHouse": {
        "set": "civic",
        "title": "Klymene's upper room, over the racecourse",
        "map": "MAP_ARKADIA_KLYMENE_HOUSE", "layout": "LAYOUT_ARKADIA_KLYMENE_HOUSE",
        "idea": "A bright upstairs room over the old racecourse, with a wide window onto the track and a bench "
                "under it where she watches the runners. On the walls, old running sandals hang in pairs by "
                "date, a victor's ribbon has gone pale, and three wooden apples painted gold sit on their "
                "shelf. You come up into it by the stair.",
        "floors": {".": "boards"}, "walls": {"W": "arkwhite"},
        "grid": ["WWWWWWWWWWW",
                 "WWWWWWWWWWW",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "..........."],
        "stamps": [("sandals_2", 0, 1), ("sandals_1", 1, 0), ("sandals_2", 2, 1), ("track_window", 4, 0),
                   ("window_bench", 3, 2), ("ribbon", 7, 0), ("apple_shelf", 8, 1), ("amphora", 10, 2),
                   ("lampstand", 0, 3), ("kline", 9, 4), ("rug_red", 3, 6), ("table_round", 5, 5),
                   ("stool", 4, 5), ("stool", 6, 5), ("strigil", 10, 1), ("kalathos", 7, 8),
                   ("chest", 9, 7), ("stair_rail", 0, 8), ("stair_down", 1, 8)],
        "spots": [
            warp([(1, 8), (2, 8)], "MAP_ARKADIA", 3),
            npc("Klymene, by her window", (6, 2), "west", G + "ELDER_F",
                "Arkadia_KlymeneHouse_EventScript_Klymene", local="LOCALID_ARKADIA_KLYMENE"),
            npc("Parthenopaios, her grandson, stretching", (7, 4), "west", G + "YOUTH_M",
                "Arkadia_KlymeneHouse_EventScript_Parthenopaios", local="LOCALID_ARKADIA_PARTHENOPAIOS"),
            bg("the window on the track", (5, 1), (5, 2, "north"), "Arkadia_KlymeneHouse_EventScript_Window"),
            bg("the running sandals", (2, 1), (2, 2, "north"), "Arkadia_KlymeneHouse_EventScript_Sandals"),
            bg("the pale ribbon", (7, 1), (7, 2, "north"), "Arkadia_KlymeneHouse_EventScript_Ribbon"),
            bg("the golden apples", (8, 1), (8, 2, "north"), "Arkadia_KlymeneHouse_EventScript_Apples"),
        ],
    },
    "Arkadia_CharcoalHut": {
        "set": "homes",
        "title": "Hippothoos's hut, dug into the hill",
        "map": "MAP_ARKADIA_CHARCOAL_HUT", "layout": "LAYOUT_ARKADIA_CHARCOAL_HUT",
        "idea": "A charcoal-burner's hut dug half into the hillside, so the back wall is earth shored with logs. "
                "Sacks of charcoal are stacked to the roof; the long iron rake leans by them; on a board "
                "pegged to the logs he has drawn a kiln mound in soot with every vent marked. Everything, "
                "him included, is black to the elbows. His little bear sits by the door, out of the smoke.",
        "floors": {".": "charearth"}, "walls": {"E": "earthlog"},
        "grid": ["EEEEEEEEEEE",
                 "EEEEEEEEEEE",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "..........."],
        "stamps": [("charcoal_sacks", 0, 0), ("charcoal_sacks", 2, 0), ("iron_rake", 4, 0),
                   ("soot_drawing", 6, 0), ("bucket", 10, 2), ("cot", 8, 4), ("charcoal_heap", 0, 4),
                   ("charcoal_heap", 1, 3), ("stool", 6, 4), ("pots", 10, 6), ("log_pile", 8, 6),
                   ("sacking_mat", 4, 7)],
        "spots": [
            warp([(4, 7), (5, 7)], "MAP_ARKADIA", 4),
            npc("Hippothoos, the charcoal-burner", (6, 3), "south", G + "CHARCOALER",
                "Arkadia_CharcoalHut_EventScript_Hippothoos", local="LOCALID_ARKADIA_HIPPOTHOOS"),
            npc("the little bear, Arkas, by the door (until traded)", (2, 6), "east",
                "OBJ_EVENT_GFX_SPECIES(ARKOBY)", "Arkadia_CharcoalHut_EventScript_Arkas",
                local="LOCALID_ARKADIA_ARKAS", flag="FLAG_ICHOR_TRADED_ARKOBY"),
            bg("the soot drawing of a kiln", (6, 1), (6, 2, "north"), "Arkadia_CharcoalHut_EventScript_Drawing"),
            bg("the charcoal sacks", (2, 2), (2, 3, "north"), "Arkadia_CharcoalHut_EventScript_Sacks"),
            bg("the iron rake", (4, 2), (4, 3, "north"), "Arkadia_CharcoalHut_EventScript_Rake"),
        ],
    },
    "Arkadia_GoatherdHouse": {
        "set": "homes",
        "title": "Krotos's house, half of it a byre",
        "map": "MAP_ARKADIA_GOATHERD_HOUSE", "layout": "LAYOUT_ARKADIA_GOATHERD_HOUSE",
        "idea": "Half house, half byre, with a wooden rail down the middle. On the house side, his bed, the "
                "cheese press and the hearth, and his syrinx on its peg; on the other, the kids asleep on "
                "straw, the hay rack and the trough, and over the byre's back door a wooden mask of Pan, "
                "horned and grinning. When a lost kid comes home, it turns up in the pen.",
        "floors": {".": "earth", ",": "straw"}, "walls": {"B": "byre"},
        "grid": ["BBBBBBBBBBBBBB",
                 "BBBBBBBBBBBBBB",
                 ".......,,,,,,,",
                 ".......,,,,,,,",
                 ".......,,,,,,,",
                 ".......,,,,,,,",
                 ".......,,,,,,,",
                 ".......,,,,,,,",
                 ".......,,,,,,,"],
        "stamps": [("soot", 0, 0), ("hearth", 0, 2), ("syrinx", 4, 1), ("cheese_press", 3, 2),
                   ("fleece_bed", 5, 2), ("table", 1, 5), ("stool", 0, 5), ("kalathos", 6, 7),
                   ("rail_post", 7, 2), ("rail", 7, 3), ("rail_post", 7, 4), ("rail", 7, 5), ("rail_end", 7, 6),
                   ("back_door", 10, 0), ("pan_mask", 10, 0), ("hay_rack", 12, 1), ("trough", 8, 6),
                   ("kids_pair", 9, 4), ("kid_brown", 12, 5), ("kids_pair", 11, 7), ("milk_pails", 0, 7), ("mat", 2, 8)],
        "spots": [
            warp([(2, 8), (3, 8)], "MAP_ARKADIA", 5),
            npc("Krotos the goatherd", (4, 5), "south", G + "GOATHERD",
                "Arkadia_GoatherdHouse_EventScript_Krotos", local="LOCALID_ARKADIA_KROTOS"),
            npc("the first lost kid, home (after it's found)", (10, 3), "south", "OBJ_EVENT_GFX_SPECIES(KERAZAP)",
                "Arkadia_GoatherdHouse_EventScript_HomeKid", local="LOCALID_ARKADIA_KROTOS_KID_1",
                flag="FLAG_TEMP_11"),
            npc("the second lost kid, home", (12, 3), "west", "OBJ_EVENT_GFX_SPECIES(KERAZAP)",
                "Arkadia_GoatherdHouse_EventScript_HomeKid", local="LOCALID_ARKADIA_KROTOS_KID_2",
                flag="FLAG_TEMP_12"),
            npc("the third lost kid, home", (9, 8), "north", "OBJ_EVENT_GFX_SPECIES(KERAZAP)",
                "Arkadia_GoatherdHouse_EventScript_HomeKid", local="LOCALID_ARKADIA_KROTOS_KID_3",
                flag="FLAG_TEMP_13"),
            bg("the syrinx", (4, 1), (4, 2, "north"), "Arkadia_GoatherdHouse_EventScript_Syrinx"),
            bg("Pan's mask over the byre door", (10, 1), (10, 2, "north"), "Arkadia_GoatherdHouse_EventScript_PanMask"),
            bg("the kids in the straw", (9, 4), (8, 4, "east"), "Arkadia_GoatherdHouse_EventScript_Kids"),
            bg("the cheese press", (3, 3), (3, 4, "north"), "Arkadia_GoatherdHouse_EventScript_Press"),
        ],
    },
}

FACING_MOVE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
               "west": "MOVEMENT_TYPE_FACE_LEFT", "east": "MOVEMENT_TYPE_FACE_RIGHT",
               "wander": "MOVEMENT_TYPE_WANDER_AROUND", "look": "MOVEMENT_TYPE_LOOK_AROUND"}
BG_FACE = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
           "east": "BG_EVENT_PLAYER_FACING_EAST", "west": "BG_EVENT_PLAYER_FACING_WEST"}


def check_spots(name, spec, cells):
    """Every warp, NPC, coord and bg-reading tile is walkable and reachable from
    the room's door; each bg is read from the tile in front of it."""
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
            check(cells[y][x].block != B.SOLID or spot[4].get("on_furniture"),
                  f"{name}: npc '{label}' at {spot[2]} stands on furniture")
            near = [(x + dx, y + dy) for dx, dy in B.DIRS.values()]
            check(any(n in seen for n in near) or spot[2] in seen or
                  any(cells[n[1]][n[0]].behavior == "MB_COUNTER" for n in near if 0 <= n[0] < W and 0 <= n[1] < H),
                  f"{name}: npc '{label}' at {spot[2]} can't be reached")
        elif kind == "coord":
            check(cells[spot[2][1]][spot[2][0]].block != B.SOLID, f"{name}: coord {spot[2]} is solid")
        elif kind == "hidden":
            x, y = spot[2]
            near = [(x + dx, y + dy) for dx, dy in B.DIRS.values()]
            check(spot[2] in seen or any(n in seen for n in near),
                  f"{name}: hidden item '{label}' at {spot[2]} can't be reached")
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
                      "movement_type": d.get("move", FACING_MOVE[s[3]]), "movement_range_x": rx,
                      "movement_range_y": ry,
                      "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
                      "script": d["script"], "flag": d.get("flag", "0")})
            objs.append(o)
        elif s[0] == "bg":
            bgs.append({"type": "sign", "x": s[2][0], "y": s[2][1], "elevation": 0,
                        "player_facing_dir": BG_FACE[s[3][2]], "script": s[4]})
        elif s[0] == "hidden":
            bgs.append({"type": "hidden_item", "x": s[2][0], "y": s[2][1], "elevation": 3,
                        "item": s[3], "flag": s[4]})
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
            lay["secondary_tileset"] = B.TILESETS[ROOMS[name]["set"]][0]
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
           f"- Map `{spec['map']}`, layout `{spec['layout']}`: **{W}x{H}**, `gTileset_Oikos` + "
           f"`{B.TILESETS[spec['set']][0]}`.",
           f"- Render: `design/phase3/img/{name}.png` (2x).", "",
           f"![{spec['title']}](img/{name}.png)", "",
           f"{spec['idea']}", "",
           "Walk map: `#` blocked, `.` open; digits and letters are the spots below (a bg event is "
           "marked on its furniture).", "", "```", "    " + "".join(str(x % 10) for x in range(W))]
    for y in range(H):
        out.append(f"{y:3d} " + "".join(marks.get((x, y), "." if cells[y][x].block != B.SOLID else "#")
                                        for x in range(W)))
    out += ["```", "", "| # | Kind | Tile | Detail | What |", "|---|---|---|---|---|"]
    seen_coord = set()
    for key, spot in zip(keys, spec["spots"]):
        kind, label = spot[0], spot[1]
        if kind == "warp":
            out.append(f"| {key} | warp | {', '.join(f'({x},{y})' for x, y in spot[2])} | "
                       f"to `{spot[3]}` warp {spot[4]} | the exit |")
        elif kind == "npc":
            flag = f", hidden by `{spot[4]['flag']}`" if spot[4].get("flag") else ""
            out.append(f"| {key} | npc | ({spot[2][0]},{spot[2][1]}) | faces {spot[3]}, "
                       f"`{spot[4]['gfx']}`{flag} | {label} |")
        elif kind == "bg":
            fx, fy, f = spot[3]
            out.append(f"| {key} | bg | ({spot[2][0]},{spot[2][1]}) | read from ({fx},{fy}) facing {f} | {label} |")
        elif kind == "hidden":
            out.append(f"| {key} | hidden | ({spot[2][0]},{spot[2][1]}) | `{spot[3]}`, `{spot[4]}` | {label} |")
        elif kind == "coord":
            if label in seen_coord:
                continue
            seen_coord.add(label)
            tiles = [s[2] for s in spec["spots"] if s[0] == "coord" and s[1] == label]
            out.append(f"| {key} | coord | {', '.join(f'({x},{y})' for x, y in tiles)} | "
                       f"`{spot[3]}` = {spot[4]} | {label} |")
    out.append("")
    return "\n".join(out)


def splice(path, text):
    begin, end = "<!-- arkrooms: begin generated -->", "<!-- arkrooms: end generated -->"
    doc = path.read_text()
    a, b = doc.index(begin) + len(begin), doc.index(end)
    path.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])


def build_set(which, names, composed, compile_it):
    """Merge, collect and (optionally) compile one secondary."""
    B.use(which)
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


def overview(renders, path):
    """One sheet of all nine rooms at 2x, labelled, in rows of four."""
    from PIL import Image, ImageDraw
    names = list(renders)
    cols = 4
    pad, label_h = 16, 22
    cw = max(r.shape[1] for r in renders.values()) * 2 + pad
    rows = (len(names) + cols - 1) // cols
    row_h = []
    for r in range(rows):
        row_h.append(max(renders[n].shape[0] for n in names[r * cols:(r + 1) * cols]) * 2 + pad + label_h)
    sheet = Image.new("RGB", (cols * cw + pad, sum(row_h) + pad), (232, 224, 208))
    draw = ImageDraw.Draw(sheet)
    y = pad
    for r in range(rows):
        for c, n in enumerate(names[r * cols:(r + 1) * cols]):
            im = Image.fromarray(renders[n]).resize((renders[n].shape[1] * 2, renders[n].shape[0] * 2),
                                                    Image.NEAREST)
            x = pad + c * cw + (cw - pad - im.width) // 2
            draw.text((pad + c * cw, y), ROOMS[n]["title"], fill=(40, 24, 24))
            sheet.paste(im, (x, y + label_h))
        y += row_h[r]
    sheet.save(path)


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
        names = [n for n in ROOMS if ROOMS[n]["set"] == which]
        if names:
            sets[which] = (names,) + build_set(which, names, composed, not args.no_compile)
    if args.preview:
        d = Path(args.preview)
        for n, cells in composed.items():
            if args.only and n not in args.only.split(","):
                continue
            B.save_scaled(B.image_of(cells), d / f"{n}.png", 2)
        overview({n: B.image_of(c) for n, c in composed.items()}, d / "overview.png")
    if args.no_compile:
        return

    import subprocess
    sizes, docs, stats, renders = {}, {}, [], {}
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
                raise SystemExit(f"arkrooms: {n} doesn't render as composed (first bad pixel {bad[0]})")
            d = ROOT / "data/layouts" / n
            d.mkdir(parents=True, exist_ok=True)
            blocks.tofile(d / "map.bin")
            np.array([void_id | B.SOLID] * 4, "<u2").tofile(d / "border.bin")
            B.save_scaled(got, IMG / f"{n}.png", 2)
            renders[n] = got
            write_map_json(n, ROOMS[n])
            docs[n] = room_doc(n, ROOMS[n], cells)
            print(f"arkrooms: {n} {W}x{H} on {B.SYMBOL}")
        stats.append(f"- `{B.SYMBOL}` (`data/tilesets/secondary/{B.DIR}`): **{nmeta}** metatiles of 512, "
                     f"**{ntiles}** tiles of {B.TILE_LIMIT}, palettes {pals[0]}-{pals[-1]}. "
                     f"Sheet: `design/phase3/img/{B.DIR}_sheet.png`.")
        r = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", str(B.TS),
                            "--primary", "gTileset_Oikos", "--scale", "2", "-o", str(IMG / f"{B.DIR}_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            print(r.stderr)
    write_layouts(sizes)
    overview({n: renders[n] for n in ROOMS if n in renders}, IMG / "arkadia_interiors_overview.png")
    if DOC.exists():
        splice(DOC, "\n".join(stats) + "\n\n" + "\n".join(docs[n] for n in ROOMS))


if __name__ == "__main__":
    main()
