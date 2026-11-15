#!/usr/bin/env python3
"""Emporion's nine interiors.

Every house is a home and every interior is unique (design/MAP_DESIGN.md
section 2). Who is in each room and what happens there is in
design/phase2/SCRIPT.md, Part 2, "Emporion interiors", and beats 12 and 13;
the render-and-critique passes are recorded in design/phase2/ROOMS_emporion.md.

The rooms come from three secondary tilesets on the oikos primary:
  ergasteria  the Hephaisteion's forge (tools/ichor/art/ergasteria_build.py)
  limen       the Deigma, the Dolphin, Philoxenos's andron, the widow's room,
              the runners' barracks, Euphronios's workshop and the hiring
              hall (tools/ichor/art/limen_build.py)
  civic       the Asclepeion, with the slice's counter and Pithos
              (tools/ichor/art/civic_tiles.py; laid out in ASCLEPEION below)

Room format: aegina_homes.py's (grid, floors, walls, stamps, rugs, spots),
plus "set", "blocked" and "variants" (ergasteria_build.py's docstring).

  /usr/bin/python3 tools/ichor/maps/emporion_rooms.py   # builds all three sets and the rooms

Each room's exit is warp 0, the door mat (the widow's stairs), back to
MAP_EMPORION_CITY or MAP_EMPORION_HARBOR.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOMS_DOC = ROOT / "design/phase2/ROOMS_emporion.md"

ROOMS = {
    # ------------------------------------------------------------------
    # The Hephaisteion's forge. A small Doric temple on the hill above the
    # Agora; its forge is built into the courtyard under a smoke-black roof.
    # The great forge stands against the back wall, its hood running up into
    # the flue, the bellows at its right hand and the charcoal at its left;
    # Kedalion sits on his anvil in front of it, glaring at the cold hearth.
    # The quenching trough and the tongs rack are within a step of the
    # anvil, where a smith wants them. Toward the door the courtyard opens
    # out on limestone between two columns, and the shelf of votives waits
    # for customers by the mat.
    "hephaisteion": {
        "set": "ergasteria",
        "title": "The Hephaisteion, Emporion",
        "map": "MAP_EMPORION_CITY_HEPHAISTEION",
        "layout": "EmporionCity_Hephaisteion",
        "render": "emporion_hephaisteion.png",
        "floor": "earth",
        "wall": "smoke",
        "grid": [
            "WWWWWWWWWWWW",
            "WWWWWWWWWWWW",
            "............",
            "............",
            "............",
            "............",
            "............",
            "............",
            "............",
        ],
        "rugs": [],
        "stamps": [
            ("pithos", 0, 1),
            ("charcoal_basket", 2, 2),
            ("forge_hood", 3, 0),
            ("forge_cold", 3, 2),
            ("bellows", 6, 2),
            ("tongs_rack", 8, 1),
            ("amphora_plain", 11, 1),
            ("smith_anvil", 4, 4),
            ("quench_trough", 7, 4),
            ("workbench", 0, 6),
            ("column", 2, 5),
            ("column", 10, 5),
            ("charcoal_basket", 7, 2),
            ("pithos", 10, 2),
            ("stool", 6, 4),
            ("lampstand", 11, 6),
            ("bench", 3, 7),
            ("pots", 0, 8),
            ("votive_shelf", 8, 8),
            ("mat", 5, 8),
        ],
        "variants": {
            "lit": {"swap": {"forge_hood": "forge_hood_lit", "forge_cold": "forge_lit"},
                    "script": "EmporionCity_Hephaisteion_EventScript_LightForge"},
        },
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(5, 8), (6, 8)]),
            ("perch", "Kedalion, sitting on his anvil, glaring at the forge", (4, 4), (4, 5, "north")),
            ("npc", "the apprentice, by the trough", (9, 5), "west"),
            ("bg", "the forge", (4, 2), (4, 3, "north")),
            ("bg", "the bellows", (6, 2), (6, 3, "north")),
            ("bg", "the tongs rack", (8, 1), (8, 2, "north")),
            ("bg", "the quenching trough", (7, 4), (7, 5, "north")),
            ("bg", "the votive shelf, by the door", (8, 8), (8, 7, "south")),
        ],
    },
    # ------------------------------------------------------------------
    # The Deigma, the merchants' exchange: a long colonnaded hall, its east
    # side open on the harbor between columns. Samples lie on trestles in two
    # rows (wool, Lampis's lamps, oil; grain and the one bronze helmet), the
    # stock stands against the ashlar, a stuffed tunny hangs over the fish
    # trade's corner, and by the door are the scribe's desk and the notice
    # board, where beat 12 ends at the Archon's seal.
    "deigma": {
        "set": "limen",
        "title": "The Deigma, Emporion",
        "map": "MAP_EMPORION_CITY_DEIGMA",
        "layout": "EmporionCity_Deigma",
        "render": "emporion_deigma.png",
        "floor": "flags",
        "floors": {"~": "sea"},
        "blocked": "~",
        "wall": "stone",
        "grid": [
            "WWWWWWWWWWWWWWWW~~",
            "WWWWWWWWWWWWWWWW~~",
            "................~~",
            "................~~",
            "................~~",
            "................~~",
            "................~~",
            "................~~",
            "................~~",
            "................~~",
        ],
        "rugs": [],
        "stamps": [
            ("amphora_plain", 0, 1),
            ("amphora", 1, 1),
            ("amphora_plain", 2, 1),
            ("scrolls", 4, 0),
            ("fish_mounted", 8, 1),
            ("scales", 11, 1),
            ("pithos", 13, 1),
            ("column", 15, 2),
            ("column", 15, 6),
            ("trestle_wool", 2, 3),
            ("trestle_lamps", 6, 3),
            ("trestle_oil", 10, 3),
            ("trestle_grain", 5, 6),
            ("trestle_helmet", 9, 6),
            ("sack", 12, 7),
            ("sack", 13, 7),
            ("sack", 12, 6),
            ("amphora_plain", 14, 7),
            ("notice_board", 0, 7),
            ("desk", 4, 8),
            ("stool", 6, 8),
            ("mat", 2, 9),
        ],
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(2, 9), (3, 9)]),
            ("npc", "Lampis, the lamp-seller, beside his lamps", (8, 4), "west"),
            ("npc", "Alethea, at Lampis's table (beat 12 only)", (7, 5), "north"),
            ("coord", "the player's place in beat 12, beside Alethea", (6, 5)),
            ("coord", "Alethea at the notice board (beat 12)", (1, 8)),
            ("coord", "the player behind her at the notice board (beat 12)", (2, 8)),
            ("npc", "Thaletas, the trader, by the water with his Narkeray", (14, 5), "west"),
            ("npc", "the wool merchant, at her bolts", (1, 4), "east"),
            ("npc", "the grain merchant, by his sacks", (7, 7), "west"),
            ("bg", "the public notice, sealed with the Archon's owl", (0, 8), (1, 8, "west")),
            ("bg", "the scribe's desk", (4, 8), (4, 7, "south")),
            ("bg", "the stuffed tunny", (8, 1), (8, 2, "north")),
            ("bg", "the bronze helmet", (9, 7), (9, 8, "north")),
            ("bg", "Lampis's lamps", (6, 4), (6, 5, "north")),
            ("bg", "the wool", (3, 4), (3, 5, "north")),
            ("bg", "the oil", (10, 4), (10, 5, "north")),
            ("bg", "the grain", (5, 7), (4, 7, "east")),
        ],
    },
    # ------------------------------------------------------------------
    # The Dolphin, a harbor tavern. Low and smoky, its two windows on the
    # quay with the long benches under them; wine amphorae racked in both
    # back corners and the krater between the windows; the dolphin mosaic,
    # the tavern's sign, in the middle of the floor; tables for the sailors;
    # and in the corner by the door the knucklebones table, worn pale, where
    # Myrtale has sat for thirty-nine years.
    "tavern": {
        "set": "limen",
        "title": "The Dolphin, a tavern, Emporion",
        "map": "MAP_EMPORION_CITY_TAVERN",
        "layout": "EmporionCity_Tavern",
        "render": "emporion_tavern.png",
        "floor": "terracotta",
        "wall": "tavern",
        "grid": [
            "WWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWW",
            "..............",
            "..............",
            "..............",
            "..............",
            "..............",
            "..............",
            "..............",
        ],
        "rugs": [],
        "stamps": [
            ("amphora_rack", 0, 0),
            ("nets", 2, 0),
            ("sea_window", 4, 0),
            ("krater", 7, 1),
            ("sea_window", 8, 0),
            ("nets", 10, 0),
            ("amphora_rack", 12, 0),
            ("bench", 4, 2),
            ("bench", 8, 2),
            ("dolphin_mosaic", 5, 4),
            ("table", 1, 4),
            ("stool", 0, 4),
            ("stool", 3, 4),
            ("table", 11, 4),
            ("stool", 13, 4),
            ("lampstand", 13, 6),
            ("bones_table", 0, 7),
            ("stool", 2, 7),
            ("fish_basket", 12, 8),
            ("mat", 6, 8),
        ],
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(6, 8), (7, 8)]),
            ("npc", "Myrtale, the champion, at the knucklebones table", (1, 6), "south"),
            ("npc", "Strepsiades, at the corner table", (2, 5), "north"),
            ("npc", "Stratyllis, on the bench by the window", (10, 3), "south"),
            ("bg", "the knucklebones table", (0, 7), (0, 6, "south")),
            ("bg", "the dolphin mosaic, read from below", (6, 5), (6, 6, "north")),
            ("bg", "the amphora rack", (0, 1), (0, 2, "north")),
            ("bg", "the krater", (7, 2), (7, 3, "north")),
            ("bg", "the nets", (10, 1), (10, 2, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # Philoxenos's house: an andron, the dining room of a man who keeps the
    # old law of hospitality. Seven couches round the walls (three along the
    # back, two down each side), a small table at each, the host-greeting
    # mosaic in the middle; the door is off-center, as an andron's is, so
    # the couches fit. Through the columns on the right are the cook's hearth
    # and the guest bed behind its striped curtain.
    "philoxenos": {
        "set": "domos",
        "title": "Philoxenos's house, Emporion",
        "map": "MAP_EMPORION_CITY_PHILOXENOS_HOUSE",
        "layout": "EmporionCity_PhiloxenosHouse",
        "render": "emporion_philoxenos.png",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWW",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
            "...............",
        ],
        "rugs": [],
        "stamps": [
            ("window", 2, 0),
            ("niche", 5, 0),
            ("window", 8, 0),
            ("kline", 1, 2),
            ("kline", 4, 2),
            ("kline", 7, 2),
            ("kline_side", 0, 4),
            ("kline_side", 0, 7),
            ("kline_side_r", 9, 4),
            ("kline_side_r", 9, 7),
            ("table_round", 2, 4),
            ("table_round", 5, 4),
            ("table_round", 8, 4),
            ("host_mosaic", 3, 6),
            ("column", 10, 2),
            ("column", 10, 6),
            ("soot", 12, 0),
            ("hearth", 12, 2),
            ("pots", 11, 3),
            ("amphora", 14, 2),
            ("krater", 14, 5),
            ("curtain_bed", 12, 8),
            ("louterion", 5, 9),
            ("lampstand", 0, 9),
            ("mat", 6, 10),
        ],
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(6, 10), (7, 10)]),
            ("npc", "Philoxenos, at the head of his table", (5, 8), "south"),
            ("npc", "his cook, at the hearth", (13, 4), "west"),
            ("bg", "the host-greeting mosaic", (4, 7), (4, 8, "north")),
            ("bg", "the hearth", (12, 3), (12, 4, "north")),
            ("bg", "the guest bed behind its curtain", (12, 9), (11, 9, "east")),
            ("bg", "the washbasin by the door", (5, 9), (5, 8, "south")),
        ],
    },
    # ------------------------------------------------------------------
    # The widow's house: Penelopeia's narrow room up over the rope-maker's
    # yard. The big upright loom with the shroud on it fills the back
    # corner; the window on the sea has her stool in front of it; her
    # husband's oar hangs across the wall beside it, and under Poseidon's
    # trident is a little altar with a dried starfish. Her bed and her chest
    # are along the walls, the wool basket by the loom.
    "widow": {
        "set": "limen",
        "title": "The widow's house, Emporion",
        "map": "MAP_EMPORION_CITY_WIDOWS_HOUSE",
        "layout": "EmporionCity_WidowsHouse",
        "render": "emporion_widow.png",
        "floor": "boards",
        "wall": "blue",
        "grid": [
            "WWWWWWWW",
            "WWWWWWWW",
            "........",
            "........",
            "........",
            "........",
            "........",
            "........",
        ],
        "rugs": [("blue", 3, 4, 3, 2)],
        "stamps": [
            ("loom_shroud", 0, 0),
            ("sea_window", 3, 0),
            ("oar_hung", 5, 0),
            ("trident", 7, 0),
            ("stool", 3, 2),
            ("starfish_altar", 7, 2),
            ("kalathos", 2, 2),
            ("kline", 0, 4),
            ("chest", 6, 4),
            ("lampstand", 7, 6),
            ("mat", 3, 7),
        ],
        "spots": [
            ("warp", "the stair door down to the yard (south-arrow mat)", [(3, 7), (4, 7)]),
            ("npc", "Penelopeia, beside her loom", (3, 3), "west"),
            ("bg", "the loom and its shroud", (1, 2), (1, 3, "north")),
            ("bg", "the window on the sea", (4, 1), (4, 2, "north")),
            ("bg", "her husband's oar", (6, 1), (6, 2, "north")),
            ("bg", "the shrine of Poseidon", (7, 2), (7, 3, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The runners' house: the barracks of Kerykos's day-runners. Straw
    # pallets in rows along both walls, sandals in pairs on the pegs over
    # them, the road map of all Aethos scratched into the plaster, the back
    # door to the training yard with the finishing ribbon nailed over it, the
    # klepsydra that times them, and the big water jar with its ladle.
    "runners": {
        "set": "domos",
        "title": "The runners' house, Emporion",
        "map": "MAP_EMPORION_CITY_RUNNERS_HOUSE",
        "layout": "EmporionCity_RunnersHouse",
        "render": "emporion_runners.png",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWWW",
            "WWWWWWWWWWWWW",
            ".............",
            ".............",
            ".............",
            ".............",
            ".............",
            ".............",
            ".............",
        ],
        "rugs": [],
        "stamps": [
            ("sandals_pegs", 0, 1),
            ("road_map", 3, 0),
            ("ribbon_door", 6, 0),
            ("sandals_pegs", 8, 1),
            ("klepsydra", 7, 0),
            ("water_jar", 12, 1),
            ("pallet", 0, 2),
            ("pallet", 2, 2),
            ("pallet", 8, 2),
            ("pallet", 10, 2),
            ("pallet", 0, 5),
            ("pallet", 2, 5),
            ("table", 8, 5),
            ("stool", 7, 5),
            ("stool", 10, 5),
            ("bench", 8, 7),
            ("amphora_plain", 12, 6),
            ("mat", 5, 8),
        ],
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(5, 8), (6, 8)]),
            ("npc", "Dromokleia, the chief runner, under her map", (4, 3), "south"),
            ("npc", "a runner, stretching", (6, 5), "east"),
            ("npc", "a runner, on his pallet", (1, 4), "south"),
            ("bg", "the road map scratched on the wall", (3, 1), (3, 2, "north")),
            ("bg", "the finishing ribbon over the back door", (6, 1), (6, 2, "north")),
            ("bg", "the water jar", (12, 2), (12, 3, "north")),
            ("bg", "the klepsydra", (7, 1), (7, 2, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # Euphronios's workshop. The domed kiln at the back, its chimney up
    # through the roof; long shelves of new cups and jars drying on the walls
    # either side, his name scrawled in slip wherever there was plaster; the
    # paint table with cups half done, the slip pots and the clay bin; and
    # by the door the wheel, with the half-painted cup of a creature nobody
    # has drawn yet.
    "potter": {
        "set": "domos",
        "title": "Euphronios's workshop, Emporion",
        "map": "MAP_EMPORION_CITY_POTTERS_WORKSHOP",
        "layout": "EmporionCity_PottersWorkshop",
        "render": "emporion_potter.png",
        "floor": "claydust",
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWW",
            "WWWWWWWWWWWW",
            "............",
            "............",
            "............",
            "............",
            "............",
            "............",
            "............",
        ],
        "rugs": [],
        "stamps": [
            ("drying_shelf", 0, 0),
            ("scrawl", 2, 0),
            ("kiln", 5, 0),
            ("scrawl", 7, 0),
            ("drying_shelf", 9, 0),
            ("amphora", 11, 2),
            ("amphora_plain", 10, 2),
            ("trestle_cups", 1, 3),
            ("stool", 2, 5),
            ("clay_bin", 4, 4),
            ("slip_pots", 0, 6),
            ("pithos", 10, 5),
            ("wheel", 8, 7),
            ("stool", 9, 7),
            ("mat", 5, 8),
        ],
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(5, 8), (6, 8)]),
            ("npc", "Euphronios, at his paint table", (3, 4), "west"),
            ("npc", "the apprentice, at the wheel", (9, 6), "south"),
            ("bg", "the kiln", (6, 2), (6, 3, "north")),
            ("bg", "the half-painted cup on the wheel", (8, 7), (7, 7, "east")),
            ("bg", "EUPHRONIOS PAINTED ME, on the wall", (3, 1), (3, 2, "north")),
            ("bg", "the drying shelves", (0, 1), (0, 2, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The hiring hall: a long warehouse among the shipsheds where the Titans'
    # crew boss signs on dockhands. Crates of shovels and bronze helmets
    # stacked along the walls (one with a sickle chalked small on it), the
    # hoist by the barred shed doors, and his pay table, ledger and silver,
    # across the middle like a counter. After Act I the crates are gone
    # (the "empty" variant) and only the ledger is left, open.
    "hiring_hall": {
        "set": "limen",
        "title": "The hiring hall, Emporion's harbor",
        "map": "MAP_EMPORION_CITY_HIRING_HALL",
        "layout": "EmporionCity_HiringHall",
        "render": "emporion_hiring_hall.png",
        "floor": "boards",
        "wall": "timber",
        "grid": [
            "WWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWW",
            ".................",
            ".................",
            ".................",
            ".................",
            ".................",
            ".................",
        ],
        "rugs": [],
        "stamps": [
            ("crate_stack", 0, 1),
            ("crate_shovels", 1, 2),
            ("hoist", 3, 0),
            ("shed_doors", 4, 0),
            ("crate_helmets", 7, 2),
            ("crate_stack", 13, 1),
            ("crate_sickle", 14, 2),
            ("crate_stack", 15, 1),
            ("crate_shovels", 16, 2),
            ("trestle_ledger", 8, 4),
            ("stool", 10, 3),
            ("crate_stack", 0, 4),
            ("crate", 1, 5),
            ("crate", 0, 6),
            ("crate_helmets", 1, 6),
            ("crate_shovels", 2, 6),
            ("sack", 5, 2),
            ("sack", 6, 2),
            ("crate_stack", 16, 4),
            ("crate_stack", 12, 4),
            ("crate", 13, 5),
            ("crate_shovels", 4, 5),
            ("crate", 5, 5),
            ("crate_helmets", 15, 5),
            ("crate_shovels", 15, 6),
            ("crate", 16, 6),
            ("crate", 14, 6),
            ("mat", 8, 7),
        ],
        "variants": {
            "empty": {"drop": ["crate_stack", "crate_shovels", "crate_helmets", "crate_sickle",
                               "crate", "stool", "sack"],
                      "script": "EmporionCity_HiringHall_EventScript_EmptyHall"},
        },
        "spots": [
            ("warp", "door to the harbor (south-arrow mat)", [(8, 7), (9, 7)]),
            ("npc", "the crew boss, behind his pay table (talked to across it)", (9, 3), "south"),
            ("npc", "a dockhand, waiting to sign on", (6, 5), "east"),
            ("bg", "the ledger (after Act I)", (8, 4), (8, 5, "north")),
            ("bg", "the crate with the sickle chalked on it", (14, 2), (14, 3, "north")),
            ("bg", "the crates of shovels", (1, 2), (1, 3, "north")),
            ("bg", "the hoist", (3, 2), (3, 3, "north")),
        ],
    },
}


# ----------------------------------------------------------------------
# The Asclepeion is built from civic, the slice's set of public halls, so it
# shares Akti's counter, Pithos, statue and couches; it is laid out with
# civic_rooms.py's Room (a grid of civic metatile names) rather than composed.
# A harbor Asclepeion, long and bright: the Pithos in its niche between two
# jars at the back left; Asclepius by the wide sea window; the healer at her
# counter with the harbor at her back and the Panacoil coiled round the
# counter's post; the ship's-rope bell-pull at the counter's end; bronze
# anchors and clay votives hung by sailors on the wall to the right; and the
# couches of the ward down the right side behind a colonnade.
ASCLEPEION = {
    "title": "The Asclepeion, Emporion",
    "map": "MAP_EMPORION_CITY_ASCLEPEION",
    "layout": "EmporionCity_Asclepeion",
    "render": "emporion_asclepeion.png",
    "size": (17, 9),
    "spots": [
        ("warp", "door to Emporion (the threshold mosaic)", [(8, 8)]),
        ("perch", "the healer, at the counter with the sea behind her", (8, 2), (8, 4, "north")),
        ("perch", "the Panacoil, coiled round the counter's post", (6, 2), (6, 4, "north")),
        ("npc", "the sailor with a sunburn, by the couches", (13, 4), "east"),
        ("npc", "the old woman, by the statue", (4, 3), "north"),
        ("npc", "the young healer, in the ward", (13, 7), "west"),
        ("bg", "the Pithos", (1, 2), (1, 3, "north")),
        ("bg", "the Pithos", (2, 2), (2, 3, "north")),
        ("bg", "the statue of Asclepius", (5, 2), (5, 3, "north")),
        ("bg", "the bell-pull", (11, 1), (11, 2, "north")),
        ("bg", "the sea window (beside the counter)", (5, 2), (5, 3, "north")),
        ("bg", "the anchors", (12, 1), (12, 2, "north")),
    ],
}


def asclepeion_room():
    import civic_rooms as CR
    W, H = ASCLEPEION["size"]
    r = CR.Room("emporion_asclepeion", W, H, CR.checker("asc_floor_a", "asc_floor_b"))
    r.row(0, 0, ["asc_wall_top_l"] + ["asc_wall_top"] * (W - 2) + ["asc_wall_top_r"])
    r.row(1, 0, ["asc_wall_l"] + ["asc_wall"] * (W - 2) + ["asc_wall_r"])
    r.row(2, 0, [("asc_floor_a_sh" if x % 2 == 0 else "asc_floor_b_sh") for x in range(W)])
    # The Pithos in its niche between two jars, back left.
    r.put("asc_jar", 0, 1, 1, 2)
    r.put("asc_pithos", 1, 0, 2, 3)
    r.put("asc_jar", 3, 1, 1, 2)
    # Asclepius by the window; the sea window behind the counter.
    r.put("asc_statue", 5, 0, 1, 3)
    r.put("asc_sea_window", 6, 0, 4, 2)
    r.set(6, 2, "asc_counter_l")
    r.set(7, 2, "asc_counter_m")
    r.set(8, 2, "asc_counter_staff")
    r.put("asc_votive_counter", 9, 2, 2, 1)
    r.row(3, 6, ["asc_counter_front_l", "asc_counter_front_m", "asc_counter_front_m",
                 "asc_counter_front_m", "asc_counter_front_r"])
    r.set(10, 2, "asc_counter_r")
    # The bell-pull at the counter's end; anchors and clay votives by sailors.
    r.put("asc_bell_rope", 11, 0, 1, 2)
    r.put("asc_anchors", 12, 1, 1, 1)
    r.put("asc_votive_wall", 13, 1, 2, 1)
    r.put("asc_anchors", 15, 1, 1, 1)
    # The ward: a colonnade, and the couches down the right side.
    for y in (3, 6):
        r.put_checkered("asc_column", 12, y, 1, 3)
    r.put_checkered("asc_kline", 15, 3, 2, 2)
    r.put_checkered("asc_kline", 15, 6, 2, 2)
    r.put_checkered("asc_snake", 14, 8)
    # A brazier by the Pithos niche, a bench for those waiting, the threshold.
    r.put_checkered("asc_brazier", 0, 4, 1, 2)
    r.put_checkered("asc_bench", 1, 7, 2, 1)
    r.put_checkered("asc_bench", 4, 7, 2, 1)
    r.put_checkered("asc_mat", 8, 8, single=True)
    return r


def build_asclepeion():
    """Write the Asclepeion's layout and its 2x render; check its spots and
    that it renders the same on two primaries (civic borrows nothing)."""
    import subprocess
    import numpy as np
    from PIL import Image
    import civic_tiles as ct
    ct.define()
    r = asclepeion_room()
    blocks = r.blocks()
    W, H = ASCLEPEION["size"]

    def solid(x, y):
        return not (0 <= x < W and 0 <= y < H) or bool(blocks[y * W + x] & 0x0C00)
    start = ASCLEPEION["spots"][0][2][0]
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and not solid(*n):
                seen.add(n)
                todo.append(n)
    dirs = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    for spot in ASCLEPEION["spots"]:
        kind, label = spot[0], spot[1]
        if kind == "npc":
            assert not solid(*spot[2]) and spot[2] in seen, f"asclepeion: {label} at {spot[2]} is unreachable"
        elif kind in ("bg", "perch"):
            fx, fy, facing = spot[3]
            assert (fx, fy) in seen, f"asclepeion: {label} is read from {(fx, fy)}, which is unreachable"
            dx, dy = dirs[facing]
            tx, ty = fx + dx, fy + dy
            if kind == "perch":         # talked to across the counter
                assert ct.METATILES[ct.BY_NAME[r.grid[ty][tx]]]["behavior"] == "MB_COUNTER"
                tx, ty = tx + dx, ty + dy
            assert (tx, ty) == spot[2], f"asclepeion: {label}: {(fx, fy)} facing {facing} misses {spot[2]}"
    d = ROOT / "data/layouts" / ASCLEPEION["layout"]
    blocks.tofile(d / "map.bin")
    np.array([(ct.FIRST_ID + ct.BY_NAME["void"]) | 0x0400] * 4, "<u2").tofile(d / "border.bin")
    out = {}
    for prim in ("oikos", "aethos", "building"):
        png = ROOT / f"build/render/emporion_asclepeion_{prim}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["/usr/bin/python3", str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(d / "map.bin"),
                        "--width", str(W), "--primary", prim, "--secondary", "civic", "--scale", "2",
                        "-o", str(png)], cwd=ROOT, check=True, capture_output=True)
        out[prim] = np.array(Image.open(png).convert("RGB"))
    assert all(np.array_equal(out["oikos"], v) for v in out.values()), "asclepeion: renders differ by primary"
    Image.fromarray(out["oikos"]).save(ROOT / "design/phase2/img" / ASCLEPEION["render"])
    # layouts.json: size and tilesets
    import ergasteria_build as EB
    civic = EB.RoomSet("civic", "gTileset_Civic", EB.EA, tiles_doc=ROOT / "design/phase1/TILES_civic.md")
    EB.update_layouts_json(civic, {ASCLEPEION["layout"]: (W, H)})
    print(f"civic: asclepeion {W}x{H} -> data/layouts/{ASCLEPEION['layout']}, design/phase2/img/{ASCLEPEION['render']}")


def build_all():
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import ergasteria_build as EB
    import limen_build
    args = EB.parse_args()
    EB.build(EB.ERGASTERIA, args)
    EB.build(limen_build.LIMEN, args)
    EB.build(limen_build.DOMOS, args)
    if not args.no_compile:
        build_asclepeion()


if __name__ == "__main__":
    build_all()
