#!/usr/bin/env python3
"""The nine interiors of the road west (Act II batch 2), on gTileset_Oikos and
three secondaries of their own: gTileset_LebadeiaRooms, gTileset_KirrhaRooms
and gTileset_AigionRooms.

  /usr/bin/python3 tools/ichor/maps/westrooms.py              # everything
  /usr/bin/python3 tools/ichor/maps/westrooms.py --no-compile --preview DIR [--only A,B]

Each room below is a grid plus placements (tools/ichor/art/westrooms_build.py
composes them), and its events. One run:
  1. composes the nine rooms and checks every 8x8 tile fits one palette,
  2. compiles each town's secondary with Porytiles and verifies it,
  3. writes data/layouts/<Layout>/{map,border}.bin and the layouts.json entries,
  4. writes each map.json's events and music from the room's spots
     (scripts.pory is hand-written and refers to them by script name and
     local id),
  5. checks every warp, person and readable thing is reachable from the door,
     and every healer can only be talked to across the counter,
  6. renders each room from the compiled tileset over oikos to
     design/phase3/img/<MapDir>.png (2x), the one-sheet overview
     design/phase3/img/west_interiors_overview.png, and refreshes the
     generated tables in design/phase3/ROOMS_west.md.

Grid legend: '#' void; wall and floor characters per room. Spots:
  ("warp", label, [(x, y), ...], dest_map, dest_warp)
  ("npc", label, (x, y), facing, {gfx, script, local, flag, move, range, on_furniture})
  ("bg", label, (x, y), (fx, fy, facing), script)
  ("hidden", label, (x, y), (fx, fy, facing), (item, flag))
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))

import westrooms_art as A  # noqa: E402
import westrooms_lebadeia  # noqa: E402,F401
import westrooms_kirrha  # noqa: E402,F401
import westrooms_aigion  # noqa: E402,F401
import westrooms_build as B  # noqa: E402

IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/ROOMS_west.md"


def npc(label, xy, facing, gfx, script, **kw):
    return ("npc", label, xy, facing, dict(gfx=gfx, script=script, **kw))


def bg(label, xy, frm, script):
    return ("bg", label, xy, frm, script)


def warp(tiles, dest, n):
    return ("warp", f"door to {dest} (its warp {n})", tiles, dest, n)


G = "OBJ_EVENT_GFX_ICHOR_"

ROOMS = {
    # ======================================================================
    # Lebadeia (beat 35B): the hamlet in the gorge, between the two springs
    # ======================================================================
    "Lebadeia_PilgrimsHall": {
        "title": "The pilgrims' hall, Lebadeia",
        "town": "Lebadeia",
        "map": "MAP_LEBADEIA_PILGRIMS_HALL", "layout": "LAYOUT_LEBADEIA_PILGRIMS_HALL",
        "music": "MUS_ICHOR_ASCLEPEION",
        "idea": "A long, low hall cut half into the hill, so the back wall is the living rock, and the "
                "rock is covered with rows of little wooden tablets on pegs: what every pilgrim saw below. "
                "Sleeping benches run down both sides with blankets folded at their feet. In the middle the "
                "fire burns in its pit, its smoke going up to a hole in the rock, and the hall-keeper tends "
                "it behind the stone kerb where the pilgrims sit to dry out. A basket of honey cakes waits "
                "by the door.",
        "floor": "rockcut", "walls": {"R": "rock"},
        "grid": ["RRRRRRRRRRRRRR",
                 "RRRRRRRRRRRRRR",
                 "R............R",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 ".............."],
        "stamps": [("votives_a", 1, 0), ("votives_b", 2, 0), ("rock_lamp", 3, 1), ("votives_c", 4, 0),
                   ("votives_d", 5, 0), ("votives_new", 6, 0), ("votives_new", 7, 0), ("votives_a", 8, 0),
                   ("votives_b", 9, 0), ("rock_lamp", 10, 1), ("votives_c", 11, 0), ("staffs", 12, 1),
                   ("sleep_bench", 0, 3), ("bundles", 0, 5), ("sleep_bench_b", 0, 6),
                   ("sleep_bench_b", 13, 3), ("hydria", 13, 5), ("sleep_bench", 13, 6),
                   ("smoke", 5, 2), ("firepit", 5, 4), ("kindling", 7, 4), ("blankets", 8, 5),
                   ("hearth_kerb", 5, 6),
                   ("table", 10, 6), ("stool", 9, 6), ("stool", 12, 6), ("bed_roll", 1, 2),
                   ("bed_roll", 10, 3),
                   ("honey_cakes", 9, 8), ("mat", 6, 8)],
        "spots": [
            warp([(6, 8), (7, 8)], "MAP_LEBADEIA", 0),
            npc("the hall-keeper, at the fire (heals)", (7, 5), "south", G + "HEALER",
                "Lebadeia_PilgrimsHall_EventScript_Keeper", local="LOCALID_LEBADEIA_HALL_KEEPER", healer=True),
            npc("a pilgrim on a bench, under a blanket", (0, 3), "east", G + "PILGRIM_BLANKET",
                "Lebadeia_PilgrimsHall_EventScript_BenchPilgrim", on_furniture=True),
            npc("a pilgrim drying out by the fire", (3, 5), "east", G + "PILGRIM_BLANKET_2",
                "Lebadeia_PilgrimsHall_EventScript_WeaverPilgrim"),
            bg("the votive wall", (2, 1), (2, 2, "north"), "Lebadeia_PilgrimsHall_EventScript_VotiveWall"),
            bg("the votive wall (the newest tablets)", (6, 1), (6, 2, "north"),
               "Lebadeia_PilgrimsHall_EventScript_VotiveWall"),
            bg("the votive wall (the newest tablets)", (7, 1), (7, 2, "north"),
               "Lebadeia_PilgrimsHall_EventScript_VotiveWall"),
            bg("the votive wall", (9, 1), (9, 2, "north"), "Lebadeia_PilgrimsHall_EventScript_VotiveWall"),
            bg("the fire", (5, 4), (5, 3, "south"), "Lebadeia_PilgrimsHall_EventScript_Fire"),
            bg("the honey cakes", (9, 8), (9, 7, "south"), "Lebadeia_PilgrimsHall_EventScript_HoneyCakes"),
            bg("the staffs and the white linen", (12, 2), (11, 2, "east"),
               "Lebadeia_PilgrimsHall_EventScript_Staffs"),
        ],
    },
    "Lebadeia_HerkynaHouse": {
        "title": "Herkyna's house, by the river",
        "town": "Lebadeia",
        "map": "MAP_LEBADEIA_HERKYNA_HOUSE", "layout": "LAYOUT_LEBADEIA_HERKYNA_HOUSE",
        "music": "MUS_ICHOR_ROAD",
        "idea": "A round river house, its wall curving away at both ends. The mill-race runs straight through "
                "it in a stone channel, in under the west wall and out under the east toward the mill, with "
                "one plank to step over. Pebbles from the river floor the back of the house, round the "
                "hearth and the grandmother's spinning stool; reed mats the front, where the empty goose pen "
                "of woven willow waits by the door. On the windowsill, a clay girl holds a clay goose.",
        "floors": {".": "pebbles", ",": "reeds"}, "wall": "leb",
        "grid": ["##WWWWWWWWW##",
                 "#WWWWWWWWWWW#",
                 "WW.........WW",
                 "W...........W",
                 ".............",
                 ".............",
                 ".............",
                 ",,,,,,,,,,,,,",
                 ",,,,,,,,,,,,,",
                 "#,,,,,,,,,,,#",
                 "##,,,,,,,,,##"],
        "stamps": [("window_goose", 3, 0), ("soot", 5, 0), ("herbs", 8, 0), ("hearth", 5, 2),
                   ("spin_stool", 8, 3), ("kline", 9, 2), ("pallet", 1, 4), ("amphora", 11, 4),
                   ("kalathos", 3, 4),
                   ("race_in", 0, 6), ("race_a", 1, 6), ("race_b", 2, 6), ("race_c", 3, 6), ("race_plank", 4, 6),
                   ("race_a", 5, 6), ("race_b", 6, 6), ("race_c", 7, 6), ("race_a", 8, 6), ("race_b", 9, 6),
                   ("race_c", 10, 6), ("race_a", 11, 6), ("race_out", 12, 6),
                   ("quern", 11, 7), ("eel_trap", 1, 7), ("goose_pen", 8, 8), ("pots", 2, 9),
                   ("toy_goose", 3, 8), ("river_stones", 10, 9), ("mat", 5, 10)],
        "spots": [
            warp([(5, 10), (6, 10)], "MAP_LEBADEIA", 1),
            npc("Herkyna, by the empty pen", (7, 8), "east", G + "HERKYNA",
                "Lebadeia_HerkynaHouse_EventScript_Herkyna", local="LOCALID_HERKYNA_HOUSE_HERKYNA"),
            npc("her grandmother, spinning by the hearth", (7, 3), "east", G + "ELDER_F",
                "Lebadeia_HerkynaHouse_EventScript_Grandmother", local="LOCALID_HERKYNA_HOUSE_GRANDMOTHER"),
            npc("Goose, home in the pen (after FLAG_ICHOR_FOUND_HERKYNAS_GOOSE)", (9, 9), "west",
                "OBJ_EVENT_GFX_SPECIES(HALCYLING)", "Lebadeia_HerkynaHouse_EventScript_Goose",
                local="LOCALID_HERKYNA_HOUSE_GOOSE", flag="FLAG_TEMP_1", on_furniture=True),
            bg("the clay girl and her goose", (3, 1), (3, 2, "north"), "Lebadeia_HerkynaHouse_EventScript_Figure"),
            bg("the mill-race", (2, 6), (2, 7, "north"), "Lebadeia_HerkynaHouse_EventScript_Race"),
            bg("the empty pen", (8, 9), (7, 9, "east"), "Lebadeia_HerkynaHouse_EventScript_Pen"),
            bg("the hearth", (5, 3), (5, 4, "north"), "Lebadeia_HerkynaHouse_EventScript_Hearth"),
        ],
    },
    "Lebadeia_MasonsHouse": {
        "title": "The mason's house, Lebadeia",
        "town": "Lebadeia",
        "map": "MAP_LEBADEIA_MASONS_HOUSE", "layout": "LAYOUT_LEBADEIA_MASONS_HOUSE",
        "music": "MUS_ICHOR_ROAD",
        "idea": "A stone-cutter's workroom. Agamedes built its back wall himself, rough-laid stones with no "
                "plaster, and left one loose for luck; he can't remember which. The rest is plastered and "
                "hung with his chisels in rows. In the middle of the floor a votive block: a snake coming up "
                "out of the rough stone, half carved. Stone dust lies in drifts in every corner.",
        "floor": "chips", "walls": {"X": "rubble", "W": "leb"},
        "grid": ["XXXXXXXXWWWW",
                 "XXXXXXXXWWWW",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............",
                 "............"],
        "stamps": [("chisels", 8, 0), ("window", 9, 0), ("chisels", 10, 0), ("mason_tools", 11, 0),
                   ("workbench", 8, 3), ("bucket", 11, 3), ("snake_relief", 3, 3), ("blocks", 9, 5),
                   ("drum_offcut", 11, 5), ("quern", 0, 4), ("amphora_plain", 0, 5), ("kline", 10, 6),
                   ("herm_blank", 7, 4), ("lampstand", 1, 5),
                   ("dust_a", 0, 2), ("dust_b", 7, 2), ("dust_c", 11, 2), ("dust_a", 7, 7), ("dust_b", 0, 7),
                   ("mat", 4, 7)],
        "spots": [warp([(4, 7), (5, 7)], "MAP_LEBADEIA", 2),
                  npc("Agamedes, at his snake", (5, 4), "west", G + "AGAMEDES",
                      "Lebadeia_MasonsHouse_EventScript_Agamedes", local="LOCALID_MASONS_HOUSE_AGAMEDES"),
                  bg("the snake relief", (3, 4), (3, 5, "north"), "Lebadeia_MasonsHouse_EventScript_Relief"),
                  bg("the chisels", (8, 1), (8, 2, "north"), "Lebadeia_MasonsHouse_EventScript_Chisels"),
                  bg("the workbench", (9, 3), (9, 4, "north"), "Lebadeia_MasonsHouse_EventScript_Bench"),
                  ("hidden", "Stardust, glittering in the drift of stone dust in the corner", (0, 7),
                   (1, 7, "west"), ("ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_LEBADEIA_MASON_STARDUST"))]
        + [bg("the loose stone (third from the left, bottom course)" if x == 2 else "a rough stone", (x, 1),
              (x, 2, "north"),
              "Lebadeia_MasonsHouse_EventScript_LooseStone" if x == 2 else
              "Lebadeia_MasonsHouse_EventScript_RoughStone") for x in range(8)],
    },
    # ======================================================================
    # Kirrha (beat 37A): Delphoi's harbor, full of people who can't ask
    # ======================================================================
    "Kirrha_Inn": {
        "title": "The pilgrims' inn, Kirrha",
        "town": "Kirrha",
        "map": "MAP_KIRRHA_INN", "layout": "LAYOUT_KIRRHA_INN",
        "music": "MUS_ICHOR_ASCLEPEION",
        "idea": "A square inn round an open courtyard, the well in the middle under the sky. Sleeping alcoves "
                "line three sides behind curtains of old patched sailcloth; the long table takes the fourth, "
                "with the hearth behind it and Strophios between, and over the hearth the big painted sign of "
                "a ship and a mule. The pilgrims' bundles wait on a shelf, every one with a name tag tied on.",
        "floors": {".": "terracotta", ",": "cobbles"}, "wall": "kir",
        "grid": ["WWWWWWWWWWWWWWW",
                 "WWWWWWWWWWWWWWW",
                 "...............",
                 "...............",
                 "...,,,,,,,,,...",
                 "...,,,,,,,,,...",
                 "...,,,,,,,,,...",
                 "...,,,,,,,,,...",
                 "...,,,,,,,,,...",
                 "...............",
                 "...............",
                 "..............."],
        "stamps": [("inn_sign", 3, 0), ("hearth", 4, 1), ("blankets", 7, 2), ("long_table", 5, 3),
                   ("bundle_shelf", 9, 0), ("window", 12, 0), ("herbs", 14, 0),
                   ("alcove_w", 0, 3), ("alcove_w", 0, 5), ("alcove_w", 0, 7),
                   ("alcove_e", 13, 3), ("alcove_e", 13, 5), ("alcove_e", 13, 7),
                   ("alcove_s", 2, 10), ("alcove_s", 4, 10), ("alcove_s", 9, 10), ("alcove_s", 11, 10),
                   ("well", 6, 5), ("amphora", 0, 9), ("pithos", 14, 9), ("stool", 10, 4),
                   ("bundles", 3, 2), ("mat", 6, 11)],
        "spots": [
            warp([(6, 11), (7, 11)], "MAP_KIRRHA", 0),
            npc("Strophios, behind the long table (heals)", (6, 2), "south", G + "STROPHIOS",
                "Kirrha_Inn_EventScript_Strophios", local="LOCALID_KIRRHA_INN_STROPHIOS", healer=True),
            npc("the whiteout heal's respawn NPC: never shown (Strophios's sprite has no bow frame)", (6, 2), "south",
                G + "STROPHIOS", "Kirrha_Inn_EventScript_Strophios", local="LOCALID_KIRRHA_INN_RESPAWN",
                flag="FLAG_SYS_POKEMON_GET"),
            npc("Pylades, by the bundles", (11, 2), "south", G + "PYLADES",
                "Kirrha_Inn_EventScript_Pylades", local="LOCALID_KIRRHA_INN_PYLADES"),
            npc("Xenodike, beside Pylades (after FLAG_ICHOR_XENODIKE_CAME_DOWN)", (12, 2), "west", G + "XENODIKE",
                "Kirrha_Inn_EventScript_Xenodike", local="LOCALID_KIRRHA_INN_XENODIKE", flag="FLAG_TEMP_1"),
            npc("a pilgrim sitting by the well, waiting", (9, 6), "west", G + "PILGRIM_BLANKET_3",
                "Kirrha_Inn_EventScript_WellPilgrim"),
            bg("the painted sign, over the hearth (read across the table)", (5, 3), (5, 4, "north"),
               "Kirrha_Inn_EventScript_Sign"),
            bg("the bundles with their name tags", (9, 1), (9, 2, "north"), "Kirrha_Inn_EventScript_Bundles"),
            bg("the bundles with their name tags", (10, 1), (10, 2, "north"), "Kirrha_Inn_EventScript_Bundles"),
            bg("the well", (6, 6), (6, 7, "north"), "Kirrha_Inn_EventScript_Well"),
            bg("the well", (7, 6), (7, 7, "north"), "Kirrha_Inn_EventScript_Well"),
            bg("an alcove", (1, 4), (2, 4, "west"), "Kirrha_Inn_EventScript_Alcove"),
            ("hidden", "a pilgrim's coin down the well, asked of the well instead of the god", (7, 5),
             (7, 4, "south"), ("ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_KIRRHA_INN_RELIC_COPPER")),
        ],
    },
    "Kirrha_Agora": {
        "title": "The Agora stall, Kirrha",
        "town": "Kirrha",
        "map": "MAP_KIRRHA_AGORA", "layout": "LAYOUT_KIRRHA_AGORA",
        "music": "MUS_ICHOR_AGORA",
        "idea": "A fishing shed on the quay, its tarred planks still smelling of nets, turned into a "
                "pilgrims' stall. The counter is an upturned boat with its eye painted on the bow. From "
                "every beam hang votives on strings, laurel wreaths and little clay omphaloi and clay feet "
                "for the healing god; nobody is buying them, so there is a crate of potions. A ship's "
                "lantern hangs over the door.",
        "floor": "boards", "walls": {"S": "shed"},
        "grid": ["SSSSSSSSSSS",
                 "SSSSSSSSSSS",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "...........",
                 "..........."],
        "stamps": [("oars", 0, 0), ("net_hang", 1, 0), ("votive_strings_a", 3, 0), ("votive_strings_b", 4, 0),
                   ("votive_strings_a", 5, 0), ("window", 6, 0), ("votive_strings_b", 7, 0),
                   ("votive_strings_a", 8, 0), ("net_hang", 9, 0),
                   ("boat_counter", 1, 3), ("potion_crate", 2, 2), ("rope_coil", 4, 2),
                   ("hang_wreaths", 6, 2), ("hang_feet", 8, 2), ("hang_omphaloi", 10, 2),
                   ("votive_table", 8, 4), ("lantern", 5, 6),
                   ("potion_crate", 10, 6), ("anchor_stone", 9, 6), ("sack", 0, 6), ("rope_coil", 1, 7),
                   ("mat", 5, 7)],
        "spots": [
            warp([(5, 7), (6, 7)], "MAP_KIRRHA", 1),
            npc("the stallkeeper, behind the boat", (3, 2), "south", G + "MERCHANT",
                "Kirrha_Agora_EventScript_Stallkeeper", local="LOCALID_KIRRHA_AGORA_KEEPER"),
            bg("the votives on their strings", (7, 1), (7, 2, "north"), "Kirrha_Agora_EventScript_Votives"),
            bg("the eye on the boat", (5, 3), (5, 4, "north"), "Kirrha_Agora_EventScript_Boat"),
            bg("the table of votives", (8, 4), (8, 5, "north"), "Kirrha_Agora_EventScript_VotiveTable"),
            bg("the crate of potions", (10, 6), (10, 5, "south"), "Kirrha_Agora_EventScript_Potions"),
        ],
    },
    "Kirrha_MuleteersHouse": {
        "title": "The muleteer's house, Kirrha",
        "town": "Kirrha",
        "map": "MAP_KIRRHA_MULETEERS_HOUSE", "layout": "LAYOUT_KIRRHA_MULETEERS_HOUSE",
        "music": "MUS_ICHOR_ROAD",
        "idea": "Half house, half stable. Three mule stalls of rough boards stand under the hay loft, two "
                "of them empty for nine days and one with a mule asleep in the straw; a ladder leans up to "
                "the loft. The muleteer's end is squeezed in beside it: harness and bells on the wall, his "
                "bed in the corner by the hearth, and on the windowsill a wooden beehive that something "
                "came down off the mountain and moved into.",
        "floors": {",": "straw", ".": "boards"}, "walls": {"L": "loft", "W": "kir"},
        "grid": ["LLLLLLLLLWWWWW",
                 "LLLLLLLLLWWWWW",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,.....",
                 ",,,,,,,,,....."],
        "stamps": [("manger", 0, 2), ("stall_wall", 2, 2), ("manger", 3, 2), ("stall_wall", 5, 2),
                   ("manger", 6, 2), ("mule", 6, 3), ("ladder", 8, 0), ("hay", 0, 4),
                   ("harness", 9, 0), ("soot", 10, 0), ("hearth", 10, 2), ("window_hive", 12, 0),
                   ("herbs", 13, 0), ("kline", 12, 2),
                   ("trough", 0, 6), ("panniers", 3, 6), ("sack", 0, 8), ("hay", 4, 3),
                   ("table", 10, 6), ("stool", 9, 6), ("stool", 12, 6), ("amphora", 13, 7),
                   ("mat", 7, 9)],
        "spots": [
            warp([(7, 9), (8, 9)], "MAP_KIRRHA", 2),
            npc("the muleteer, by his hearth", (10, 4), "south", G + "MULETEER",
                "Kirrha_MuleteersHouse_EventScript_Muleteer", local="LOCALID_KIRRHA_MULETEER"),
            npc("the Melisseer from the beehive (until it is traded)", (13, 4), "west",
                "OBJ_EVENT_GFX_SPECIES(MELISSEER)", "Kirrha_MuleteersHouse_EventScript_Melisseer",
                local="LOCALID_KIRRHA_MULETEER_MELISSEER", flag="FLAG_ICHOR_TRADED_MELISSEER"),
            bg("the sleeping mule", (7, 4), (7, 5, "north"), "Kirrha_MuleteersHouse_EventScript_Mule"),
            bg("the bed, under the beehive on the sill", (12, 3), (12, 4, "north"),
               "Kirrha_MuleteersHouse_EventScript_Hive"),
            bg("the ladder to the loft", (8, 2), (8, 3, "north"), "Kirrha_MuleteersHouse_EventScript_Ladder"),
            bg("an empty stall", (3, 2), (3, 3, "north"), "Kirrha_MuleteersHouse_EventScript_EmptyStall"),
        ],
    },
    "Kirrha_SweepersHouse": {
        "title": "Thyia's house, the old sweeper's",
        "town": "Kirrha",
        "map": "MAP_KIRRHA_SWEEPERS_HOUSE", "layout": "LAYOUT_KIRRHA_SWEEPERS_HOUSE",
        "music": "MUS_ICHOR_ROAD",
        "idea": "A small whitewashed room full of brooms: stood in every corner, a bundle of new ones "
                "hung from the beam to dry, and over the bed, on two pegs like a sword, the old one she "
                "swept the god's floor with for forty years. The floor is spotless. By the window, in a "
                "big clay pot, a young laurel cut from the tree at the temple door.",
        "floor": "flags", "wall": "kir",
        "grid": ["WWWWWWWWW",
                 "WWWWWWWWW",
                 ".........",
                 ".........",
                 ".........",
                 ".........",
                 ".........",
                 "........."],
        "stamps": [("broom_sword", 0, 1), ("kline", 0, 2), ("brooms_drying", 3, 0), ("window", 5, 0),
                   ("laurel_pot", 6, 1), ("brooms_a", 8, 1), ("brooms_b", 0, 6), ("brooms_a", 8, 6),
                   ("table_round", 4, 4), ("stool", 3, 4), ("pots", 2, 6), ("dustpan", 7, 7),
                   ("chest", 6, 4), ("kalathos", 2, 2), ("mat", 4, 7)],
        "spots": [
            warp([(4, 7), (5, 7)], "MAP_KIRRHA", 3),
            npc("Thyia, at her table", (5, 4), "west", G + "THYIA",
                "Kirrha_SweepersHouse_EventScript_Thyia", local="LOCALID_KIRRHA_THYIA"),
            bg("the young laurel in its pot", (6, 2), (6, 3, "north"), "Kirrha_SweepersHouse_EventScript_Laurel"),
            bg("the old broom over the bed", (1, 3), (2, 3, "west"), "Kirrha_SweepersHouse_EventScript_OldBroom"),
            bg("the new brooms drying", (3, 1), (3, 2, "north"), "Kirrha_SweepersHouse_EventScript_NewBrooms"),
            bg("the brooms in the corner", (8, 2), (8, 3, "north"), "Kirrha_SweepersHouse_EventScript_CornerBrooms"),
        ],
    },
    # ======================================================================
    # Aigion (beat 37C): the Achaean shore, where a war began with a meeting
    # ======================================================================
    "Aigion_AchaeansHouse": {
        "title": "The old Achaean's house, Aigion",
        "town": "Aigion",
        "map": "MAP_AIGION_ACHAEANS_HOUSE", "layout": "LAYOUT_AIGION_ACHAEANS_HOUSE",
        "music": "MUS_ICHOR_ROAD",
        "idea": "A long narrow house, and its wall is one long frieze of black ships, every one with its "
                "number painted over its prow: the Catalogue of Ships, four hundred and one onward, as far as "
                "Tisamenos has got. His chair is turned to face it. A model trireme stands on its stand in the "
                "middle of the floor, and under the window a chest stands open, full of wax tablets. He has "
                "floored the house with ship's planking, because that is what he knows.",
        "floor": "planks", "walls": {"F": "ships"},
        "grid": ["FFFFFFFFFFFFFF",
                 "FFFFFFFFFFFFFF",
                 "..............",
                 "..............",
                 "..............",
                 "..............",
                 ".............."],
        "stamps": [("kline", 0, 2), ("lampstand", 2, 2), ("chair_back", 5, 3), ("model_ship", 8, 4),
                   ("window", 11, 0), ("tablet_chest", 11, 2), ("amphora", 13, 4), ("stool", 12, 5),
                   ("table_round", 3, 5), ("anchor_stone", 6, 5), ("rope_coil", 1, 5), ("mat", 3, 6)],
        "spots": [
            warp([(3, 6), (4, 6)], "MAP_AIGION", 0),
            npc("Tisamenos, reciting to the frieze", (6, 2), "north", G + "TISAMENOS",
                "Aigion_AchaeansHouse_EventScript_Tisamenos", local="LOCALID_AIGION_TISAMENOS"),
            bg("the frieze of ships", (4, 1), (4, 2, "north"), "Aigion_AchaeansHouse_EventScript_Frieze"),
            bg("the frieze of ships", (9, 1), (9, 2, "north"), "Aigion_AchaeansHouse_EventScript_Frieze"),
            bg("the model ship", (8, 4), (8, 3, "south"), "Aigion_AchaeansHouse_EventScript_Model"),
            bg("the chest of wax tablets", (12, 2), (12, 3, "north"), "Aigion_AchaeansHouse_EventScript_Tablets"),
            bg("his chair", (5, 3), (5, 4, "north"), "Aigion_AchaeansHouse_EventScript_Chair"),
        ],
    },
    "Aigion_GoatherdsHouse": {
        "title": "The goatherd's house, Aigion",
        "town": "Aigion",
        "map": "MAP_AIGION_GOATHERDS_HOUSE", "layout": "LAYOUT_AIGION_GOATHERDS_HOUSE",
        "music": "MUS_ICHOR_ROAD",
        "idea": "Half a house and half a cave: Helike built against the hillside, so the back wall of the "
                "cave end is living rock, mossy in the cracks. The goat pen is indoors there, a ring of dry "
                "stones round clean straw, with a baby's cradle in it and a Kerazap kid asleep in the cradle. "
                "Cheeses ripen on racks in the cool of the rock. The house end is whitewashed, and along its "
                "wall hangs a row of bronze goat bells, from big to tiny.",
        "floors": {",": "cave", ".": "earth"}, "walls": {"H": "hill", "W": "aig"},
        "grid": ["HHHHHHHWWWWWW",
                 "HHHHHHHWWWWWW",
                 "H,,,,,,......",
                 ",,,,,,,......",
                 ",,,,,,,......",
                 ",,,,,,,......",
                 ",,,,,,,......",
                 ",,,,,,,......",
                 ",,,,,,,......"],
        "stamps": [("cheese_rack", 5, 1), ("goat_pen", 1, 3), ("milk_pails", 7, 2),
                   ("goatskins", 7, 0), ("goat_bells", 8, 1), ("soot", 11, 0), ("hearth", 11, 2),
                   ("kline", 11, 5), ("table", 8, 5), ("stool", 10, 5), ("amphora_plain", 0, 6),
                   ("hay", 5, 7), ("mat", 8, 8)],
        "spots": [
            warp([(8, 8), (9, 8)], "MAP_AIGION", 1),
            npc("Helike, by the hearth", (10, 3), "west", G + "HELIKE",
                "Aigion_GoatherdsHouse_EventScript_Helike", local="LOCALID_AIGION_HELIKE"),
            npc("the Kerazap kid, asleep in the cradle", (2, 4), "south", "OBJ_EVENT_GFX_SPECIES(KERAZAP)",
                "Aigion_GoatherdsHouse_EventScript_Kid", local="LOCALID_AIGION_KERAZAP_KID", on_furniture=True),
            bg("the goat bells", (9, 1), (9, 2, "north"), "Aigion_GoatherdsHouse_EventScript_Bells"),
            bg("the cheese racks", (5, 2), (5, 3, "north"), "Aigion_GoatherdsHouse_EventScript_Cheeses"),
            bg("the living rock", (1, 1), (1, 2, "north"), "Aigion_GoatherdsHouse_EventScript_Rock"),
            bg("the goat pen", (3, 4), (3, 5, "north"), "Aigion_GoatherdsHouse_EventScript_Pen"),
        ],
    },
}

FACING_MOVE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
               "west": "MOVEMENT_TYPE_FACE_LEFT", "east": "MOVEMENT_TYPE_FACE_RIGHT",
               "wander": "MOVEMENT_TYPE_WANDER_AROUND"}
BG_FACE = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
           "east": "BG_EVENT_PLAYER_FACING_EAST", "west": "BG_EVENT_PLAYER_FACING_WEST"}

# Which secondary each room is drawn from (westrooms_build.TILESETS).
SET_OF = {
    "Lebadeia_PilgrimsHall": "stone", "Lebadeia_MasonsHouse": "stone",
    "Kirrha_Inn": "harbor", "Kirrha_Agora": "harbor", "Kirrha_MuleteersHouse": "harbor",
    "Kirrha_SweepersHouse": "harbor",
    "Lebadeia_HerkynaHouse": "homes", "Aigion_AchaeansHouse": "homes", "Aigion_GoatherdsHouse": "homes",
}


def check_spots(name, spec, cells):
    """Every warp, NPC and bg-reading tile is walkable and reachable from the
    room's door; each bg is read from the tile in front of it; a healer can be
    talked to only from two tiles south, across a counter, so the heal's
    balls land where they are drawn for."""
    H, W = len(cells), len(cells[0])
    people = {s[2] for s in spec["spots"] if s[0] == "npc"}

    def walkable(x, y):
        return 0 <= x < W and 0 <= y < H and cells[y][x].block != B.SOLID

    def open_(x, y):
        return walkable(x, y) and (x, y) not in people

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
            d = spot[4]
            check(cells[y][x].block != B.SOLID or d.get("on_furniture"),
                  f"{name}: npc '{label}' at {spot[2]} stands on furniture")
            near = [(x + dx, y + dy) for dx, dy in B.DIRS.values()]
            counter = (x, y + 1)
            reach = any(n in seen for n in near) or \
                (0 <= y + 1 < H and cells[y + 1][x].behavior == "MB_COUNTER" and (x, y + 2) in seen)
            check(reach, f"{name}: npc '{label}' at {spot[2]} can't be reached")
            if d.get("healer"):
                check(cells[counter[1]][counter[0]].behavior == "MB_COUNTER",
                      f"{name}: the healer at {spot[2]} has no counter in front")
                check((x, y + 2) in seen, f"{name}: the healer's talking tile {(x, y + 2)} is unreachable")
                check(not any(n in seen for n in near), f"{name}: the healer can be reached from the side")
        elif kind in ("bg", "hidden"):
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
        elif s[0] == "hidden":
            item, flag = s[4]
            bgs.append({"type": "hidden_item", "x": s[2][0], "y": s[2][1], "elevation": 3,
                        "item": item, "flag": flag})
    return objs, warps, coords, bgs


def write_map_json(name, spec):
    p = ROOT / f"data/maps/{name}/map.json"
    m = json.loads(p.read_text())
    assert m["id"] == spec["map"], (m["id"], spec["map"])
    objs, warps, coords, bgs = map_events(spec)
    m["music"] = spec["music"]
    m["object_events"], m["warp_events"], m["coord_events"], m["bg_events"] = objs, warps, coords, bgs
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def write_layouts(sizes):
    p = ROOT / "data/layouts/layouts.json"
    d = json.loads(p.read_text())
    want = {spec["layout"]: (name, sizes[name]) for name, spec in ROOMS.items() if name in sizes}
    for lay in d["layouts"]:
        if lay.get("id") in want:
            name, (w, h) = want[lay["id"]]
            lay["width"], lay["height"] = w, h
            lay["primary_tileset"] = "gTileset_Oikos"
            lay["secondary_tileset"] = B.TILESETS[SET_OF[name]][0]
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
           f"`{B.TILESETS[SET_OF[name]][0]}`; music `{spec['music']}`.",
           f"- Render: `design/phase3/img/{name}.png` (2x).", "",
           f"![{spec['title']}](img/{name}.png)", "",
           f"{spec['idea']}", "",
           "Walk map: `#` blocked, `.` open; digits and letters are the spots below (a bg event is "
           "marked on its furniture).", "", "```", "    " + "".join(str(x % 10) for x in range(W))]
    for y in range(H):
        out.append(f"{y:3d} " + "".join(marks.get((x, y), "." if cells[y][x].block != B.SOLID else "#")
                                        for x in range(W)))
    out += ["```", "", "| # | Kind | Tile | Detail | What |", "|---|---|---|---|---|"]
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
        elif kind == "hidden":
            fx, fy, f = spot[3]
            out.append(f"| {key} | hidden | ({spot[2][0]},{spot[2][1]}) | `{spot[4][0]}`, `{spot[4][1]}` | {label} |")
    out.append("")
    return "\n".join(out)


def splice(path, text):
    begin, end = "<!-- westrooms: begin generated -->", "<!-- westrooms: end generated -->"
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
    """One sheet of the nine rooms, grouped by town, each labelled."""
    from PIL import Image, ImageDraw
    towns = []
    for n, spec in ROOMS.items():
        if n not in renders:
            continue
        if not towns or towns[-1][0] != spec["town"]:
            towns.append((spec["town"], []))
        towns[-1][1].append(n)
    pad, label = 16, 18
    rows = []
    for town, names in towns:
        w = sum(renders[n].width for n in names) + pad * (len(names) + 1)
        h = max(renders[n].height for n in names) + label + pad * 2
        rows.append((town, names, w, h))
    W = max(r[2] for r in rows)
    H = sum(r[3] for r in rows)
    sheet = Image.new("RGB", (W, H), (232, 224, 208))
    d = ImageDraw.Draw(sheet)
    y = 0
    for town, names, w, h in rows:
        x = pad
        for n in names:
            d.text((x, y + pad // 2), f"{town}: {ROOMS[n]['title'].split(',')[0]}", fill=(40, 24, 24))
            sheet.paste(renders[n], (x, y + pad // 2 + label))
            x += renders[n].width + pad
        y += h
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
        names = [n for n in ROOMS if SET_OF[n] == which]
        if names:
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
    from PIL import Image
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
                raise SystemExit(f"westrooms: {n} doesn't render as composed (first bad pixel {bad[0]})")
            d = ROOT / "data/layouts" / n
            d.mkdir(parents=True, exist_ok=True)
            blocks.tofile(d / "map.bin")
            np.array([void_id | B.SOLID] * 4, "<u2").tofile(d / "border.bin")
            B.save_scaled(got, IMG / f"{n}.png", 2)
            renders[n] = Image.fromarray(got).resize((W * 32, H * 32), Image.NEAREST)
            write_map_json(n, ROOMS[n])
            docs[n] = room_doc(n, ROOMS[n], cells)
            print(f"westrooms: {n} {W}x{H} on {B.SYMBOL}")
        stats.append(f"- `{B.SYMBOL}` (`data/tilesets/secondary/{B.DIR}`): **{nmeta}** metatiles of 512, "
                     f"**{ntiles}** tiles of {B.TILE_LIMIT}, palettes {pals[0]}-{pals[-1]}. "
                     f"Sheet: `design/phase3/img/{B.DIR}_sheet.png`.")
        r = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", str(B.TS),
                            "--primary", "gTileset_Oikos", "--scale", "2", "-o", str(IMG / f"{B.DIR}_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            print(r.stderr)
    write_layouts(sizes)
    overview(renders, IMG / "west_interiors_overview.png")
    if DOC.exists():
        splice(DOC, "\n".join(stats) + "\n\n" + "\n".join(docs[n] for n in ROOMS if n in docs))


if __name__ == "__main__":
    main()
