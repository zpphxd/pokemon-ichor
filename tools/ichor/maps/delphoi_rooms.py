#!/usr/bin/env python3
"""Delphoi's interiors and Hieron's hut (phase4 SCRIPT.md Part 2, "Delphoi" and
"Hieron's hut").

Every house is a home and every interior is unique (design/MAP_DESIGN.md §2):
each room is shaped and furnished for who lives or works there. They are laid
out from gTileset_OikiaDelphoi (limen's kit, ergasteria's treasury pieces and
Delphoi's own, tools/ichor/art/delphoi_rooms_art.py) by ergasteria_build.py's
machinery: compose, deduplicate, compile with Porytiles, check every room
renders identically on oikos, aethos and building, write the layouts. This
script also writes each room's events (EVENTS below) into its map.json.

  /usr/bin/python3 tools/ichor/maps/delphoi_rooms.py [--no-compile] [--preview DIR]

Each room's exit is warp 0, the door mat, back to its outside door.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
ROOMS_DOC = ROOT / "design/phase4/ROOMS_delphoi.md"

R = "design/phase4/img/rooms/"

ROOMS = {
    # Hieron's hut: one room built against the oldest olive, a great root coming
    # in through the back wall as a bench, the spring's channel across the floor.
    "hut": {
        "set": "oikia_delphoi", "title": "Hieron's hut, the Sacred Olives",
        "map": "MAP_ROUTE28_SACRED_OLIVES_WARDENS_HUT", "layout": "Route28_SacredOlives_WardensHut",
        "render": "delphoi_hut.png", "floor": "flags", "floors": {"~": "sea"}, "blocked": "~",
        "wall": "stone",
        "grid": ["WWWWWWWW", "WWWWWWWW", "........", "~~~~~~..", "........", "........", "........"],
        "rugs": [],
        "stamps": [("drying_shelf", 0, 0), ("sandals_pegs", 3, 0), ("oar_hung", 5, 0), ("water_jar", 7, 1),
                   ("pallet", 0, 4), ("bench", 0, 6), ("hearth_floor", 5, 4), ("kalathos", 3, 5),
                   ("mat", 3, 6)],
        "spots": [("warp", "door to the Sacred Olives (south-arrow mat)", [(3, 6), (4, 6)]),
                  ("npc", "Hieron, by his spring", (6, 2), "south"),
                  ("bg", "the spring's channel", (2, 3), (2, 4, "north")),
                  ("bg", "the olive-wood carvings", (0, 1), (0, 2, "north")),
                  ("bg", "the pruning hook, rusted shut", (5, 1), (5, 2, "north"))],
    },
    # The Asclepeion: cut back into the rock, the Kastalian running out of a crack
    # into a basin behind the counter; votive limbs on the walls; benches.
    "asclepeion": {
        "set": "oikia_delphoi", "title": "The Asclepeion, Delphoi",
        "map": "MAP_DELPHOI_ASCLEPEION", "layout": "Delphoi_Asclepeion",
        "render": "delphoi_asclepeion.png", "floor": "flags", "wall": "stone",
        "grid": ["WWWWWWWWWWWW", "WWWWWWWWWWWW", "............", "............", "............",
                 "............", "............", "............"],
        "rugs": [("blue", 4, 5, 4, 2)],
        "stamps": [("votives", 0, 1), ("louterion", 3, 0), ("niche", 5, 0), ("votives", 7, 1),
                   ("water_jar", 9, 0), ("votives", 10, 1),
                   ("counter_plank", 4, 3), ("counter_plank", 6, 3), ("pithos", 11, 2),
                   ("pallet", 0, 3), ("pallet", 0, 5), ("bench", 9, 6), ("myrtle", 11, 5),
                   ("mat", 5, 7)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(5, 7), (6, 7)]),
                  ("npc", "Epione, behind the counter", (5, 2), "south"),
                  ("npc", "Ochthos and his mother by the basin (after the climax)", (2, 2), "south"),
                  ("bg", "the votive limbs", (7, 1), (7, 2, "north"))],
    },
    # The Agora: a long portico, its stalls under the awning, the tripods for sale.
    "agora": {
        "set": "oikia_delphoi", "title": "The Agora, Delphoi",
        "map": "MAP_DELPHOI_AGORA", "layout": "Delphoi_Agora",
        "render": "delphoi_agora.png", "floor": "terracotta", "wall": "red",
        "grid": ["WWWWWWWWWWWWWW", "WWWWWWWWWWWWWW", "..............", "..............", "..............",
                 "..............", "..............", "#############."],
        "rugs": [],
        "stamps": [("window", 0, 0), ("lead_strips", 1, 1), ("tripod_small", 4, 1), ("tripod_small", 5, 1),
                   ("honey_shelf", 7, 0), ("window", 10, 0), ("amphora_rack", 12, 0),
                   ("counter_plank", 5, 3), ("counter_plank", 7, 3),
                   ("trestle_cups", 0, 4), ("trestle_grain", 10, 4), ("sack", 12, 6), ("kalathos", 0, 6),
                   ("mat", 12, 7)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(12, 7), (13, 7)]),
                  ("npc", "Lampsakos, behind the counter", (6, 2), "south"),
                  ("bg", "the little bronze tripods", (4, 2), (4, 3, "north"))],
    },
    # The House of the Melissai: long and low, its back wall a honeycomb of hive-
    # jars; wax benches, honey racks, veils by the door; a curtained inner room.
    "melissai": {
        "set": "oikia_delphoi", "title": "The House of the Melissai, Delphoi",
        "map": "MAP_DELPHOI_HOUSE_OF_THE_MELISSAI", "layout": "Delphoi_HouseOfTheMelissai",
        "render": "delphoi_melissai.png", "floor": "flags", "wall": "stone",
        "grid": ["WWWWWWWWWWWWWWWW", "WWWWWWWWWWWWWWWW", "................", "................",
                 "................", "................", "................"],
        "rugs": [],
        "stamps": [("hive_wall", 0, 0), ("hive_wall", 2, 0), ("hive_wall", 4, 0), ("honey_shelf", 7, 0),
                   ("jar_shelf", 9, 0), ("curtain_bed", 13, 0), ("ribbon_door", 12, 1),
                   ("workbench", 2, 3), ("bench", 2, 4), ("drying_shelf", 7, 3), ("kalathos", 6, 5),
                   ("water_jar", 15, 4), ("pots", 0, 5), ("mat", 9, 6)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(9, 6), (10, 6)]),
                  ("npc", "Hagne, at the wax bench", (5, 3), "south"),
                  ("npc", "Mom, in the inner room (III-7 to III-8)", (14, 2), "south"),
                  ("bg", "the honey racks", (7, 1), (7, 2, "north")),
                  ("bg", "the curtain", (12, 2), (11, 2, "east"))],
    },
    # Theokles's study: wax tablets everywhere, the chart of long and short beats,
    # a mostly dead laurel, two stools at one desk.
    "theokles": {
        "set": "oikia_delphoi", "title": "Theokles's house, Delphoi",
        "map": "MAP_DELPHOI_THEOKLES_HOUSE", "layout": "Delphoi_TheoklesHouse",
        "render": "delphoi_theokles.png", "floor": "boards", "wall": "blue",
        "grid": ["WWWWWWWWW", "WWWWWWWWW", ".........", ".........", ".........", "##......."],
        "rugs": [],
        "stamps": [("scrolls", 0, 0), ("notice_board", 3, 0), ("niche", 5, 0), ("scrolls", 6, 0),
                   ("laurel_pot", 8, 2), ("desk", 3, 3), ("stool", 2, 3), ("stool", 5, 3),
                   ("mat", 5, 5)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(5, 5), (6, 5)]),
                  ("npc", "Theokles, at his desk", (4, 2), "south"),
                  ("bg", "the two stools; the second one dusty", (5, 3), (6, 3, "west"))],
    },
    # The Pilgrims' House: a courtyard house; mats under a gallery, a long table of
    # mismatched bowls, a hearth, the wall of question strips, a pot of lentils.
    "pilgrims": {
        "set": "oikia_delphoi", "title": "The Pilgrims' House, Delphoi",
        "map": "MAP_DELPHOI_PILGRIMS_HOUSE", "layout": "Delphoi_PilgrimsHouse",
        "render": "delphoi_pilgrims.png", "floor": "terracotta", "floors": {",": "flags"},
        "wall": "red",
        "grid": ["WWWWWWWWWWWWWW", "WWWWWWWWWWWWWW", "..............", "....,,,,,,....",
                 "....,,,,,,....", "....,,,,,,....", "..............", ".............."],
        "rugs": [("red", 0, 6, 3, 2)],
        "stamps": [("lead_strips", 0, 1), ("lead_strips", 2, 1), ("lead_strips", 4, 1), ("window", 7, 0),
                   ("hearth", 11, 0), ("kline_side", 0, 3), ("kline_side", 1, 3), ("kline_side_r", 13, 3),
                   ("table", 6, 4), ("table", 8, 4), ("krater", 10, 3), ("pithos", 13, 6),
                   ("mat", 6, 7)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(6, 7), (7, 7)]),
                  ("npc", "Theoxena, by her lentils", (11, 2), "south"),
                  ("npc", "Philagros, at the long table", (7, 5), "north"),
                  ("bg", "the question strips", (2, 1), (2, 2, "north"))],
    },
    # Koretas's house: half of it a byre behind a low wall; the hearth and bed
    # shelf at the family's end; cheese baskets; the carved goat over the hearth.
    "koretas": {
        "set": "oikia_delphoi", "title": "Koretas's house, Delphoi",
        "map": "MAP_DELPHOI_KORETAS_HOUSE", "layout": "Delphoi_KoretasHouse",
        "render": "delphoi_koretas.png", "floor": "flags", "floors": {":": "claydust"},
        "wall": "stone",
        "grid": ["WWWWWWWWWW", "WWWWWWWWWW", "......::::", "......::::", "......::::", "......::::",
                 ".........."],
        "rugs": [("red", 1, 4, 2, 2)],
        "stamps": [("hearth", 0, 0), ("niche_horse", 2, 0), ("herbs", 3, 0), ("window", 4, 0),
                   ("curtain_bed", 0, 2), ("sack", 6, 2), ("kalathos", 9, 2), ("crate", 9, 4),
                   ("water_jar", 5, 4), ("mat", 3, 6)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(3, 6), (4, 6)]),
                  ("npc", "Koretas, by his hearth", (2, 3), "south"),
                  ("npc", "Aix, in the byre", (7, 3), "west")],
    },
    # Chrysothemis's practice room: kitharas on pegs, a raised platform, one stool
    # for the audience, his teacher's laurel crown on a nail.
    "kitharode": {
        "set": "oikia_delphoi", "title": "Chrysothemis's house, Delphoi",
        "map": "MAP_DELPHOI_KITHARODE_HOUSE", "layout": "Delphoi_KitharodeHouse",
        "render": "delphoi_kitharode.png", "floor": "terracotta", "floors": {"=": "boards"},
        "wall": "blue",
        "grid": ["WWWWWWWWWW", "WWWWWWWWWW", "===.......", "===.......", "===.......", "..........",
                 "####......"],
        "rugs": [],
        "stamps": [("kitharas", 0, 0), ("myrtle", 3, 0), ("window", 5, 0), ("kitharas", 7, 0),
                   ("stool", 6, 3), ("lampstand", 9, 3), ("mat", 6, 6)],
        "spots": [("warp", "door to Delphoi (south-arrow mat)", [(6, 6), (7, 6)]),
                  ("npc", "Chrysothemis, on his platform", (1, 3), "east"),
                  ("bg", "the kitharas on pegs", (8, 1), (8, 2, "north"))],
    },
    # Astyra's treasury: one marble room of captured shields, helmets, a bronze
    # prow, hymns with their notes carved over the words.
    "astyra": {
        "set": "oikia_delphoi", "title": "The treasury of Astyra, Delphoi",
        "map": "MAP_DELPHOI_ASTYRAN_TREASURY", "layout": "Delphoi_AstyranTreasury",
        "render": "delphoi_astyra.png", "floor": "flags", "wall": "stone",
        "grid": ["WWWWWWWWW", "WWWWWWWWW", ".........", ".........", ".........", ".........",
                 "........."],
        "rugs": [],
        "stamps": [("shield_spear", 0, 0), ("votive_shelf", 2, 1), ("shield_spear", 7, 0), ("votive_shelf", 5, 1),
                   ("trestle_helmet", 0, 3), ("boat", 7, 3), ("column", 3, 2), ("column", 5, 2),
                   ("mat", 3, 6)],
        "spots": [("warp", "door to the Sacred Way (south-arrow mat)", [(3, 6), (4, 6)]),
                  ("npc", "Aristion, polishing", (4, 4), "south"),
                  ("npc", "Alethea, copying a hymn (III-6C to III-8)", (2, 2), "north"),
                  ("bg", "the hymn, with the notes carved over the words", (2, 1), (2, 2, "north"))],
    },
    # The Siphnians' treasury: a frieze of gods and giants all the way round, gold
    # leaf scraped off; a chest with a padlock and a gilded rock on it.
    "siphnos": {
        "set": "oikia_delphoi", "title": "The treasury of the Siphnians, Delphoi",
        "map": "MAP_DELPHOI_SIPHNIAN_TREASURY", "layout": "Delphoi_SiphnianTreasury",
        "render": "delphoi_siphnos.png", "floor": "flags", "wall": "stone",
        "grid": ["WWWWWWWWWW", "WWWWWWWWWW", "..........", "..........", "..........", ".........."],
        "rugs": [("blue", 3, 3, 4, 2)],
        "stamps": [("frieze", 0, 1), ("frieze", 2, 1), ("frieze", 4, 1), ("frieze", 6, 1), ("frieze", 8, 1),
                   ("turtle_chest", 4, 2), ("scales", 0, 2), ("votive_shelf", 8, 3), ("mat", 4, 5)],
        "spots": [("warp", "door to the Sacred Way (south-arrow mat)", [(4, 5), (5, 5)]),
                  ("npc", "Eupolis, by his empty chest", (6, 3), "south"),
                  ("bg", "the frieze of gods and giants", (2, 1), (2, 2, "north")),
                  ("bg", "the gilded rock on the chest", (4, 3), (4, 4, "north"))],
    },
    # The Lesche of the Knidians: a long clubhouse hall, stone benches along both
    # walls, two great paintings over them, Polemon's enormous guidebook.
    "lesche": {
        "set": "oikia_delphoi", "title": "The Lesche of the Knidians, Delphoi",
        "map": "MAP_DELPHOI_LESCHE", "layout": "Delphoi_Lesche",
        "render": "delphoi_lesche.png", "floor": "flags", "wall": "tavern",
        "grid": ["WWWWWWWWWWWWWWWW", "WWWWWWWWWWWWWWWW", "................", "................",
                 "................", "................", "................"],
        "rugs": [],
        "stamps": [("painting_city", 0, 1), ("painting_city", 2, 1), ("painting_city", 4, 1),
                   ("painting_dead", 10, 1), ("painting_dead", 12, 1), ("painting_dead", 14, 1),
                   ("column", 7, 0), ("bench", 0, 2), ("bench", 3, 2), ("bench", 11, 2), ("bench", 14, 2),
                   ("desk", 7, 4), ("lampstand", 6, 4), ("mat", 7, 6)],
        "spots": [("warp", "door to the Sacred Way (south-arrow mat)", [(7, 6), (8, 6)]),
                  ("npc", "Polemon, at his guidebook", (9, 4), "west"),
                  ("bg", "the rope-plaiter and the donkey", (12, 2), (12, 3, "north")),
                  ("bg", "the city falling", (2, 2), (2, 3, "north"))],
    },
}

# The events each room's map.json gets: (local id, gfx, x, y, script, facing, flag).
# Warp 0 is the mat; its destination is the outside door's warp id.
DOOR = {
    "hut": ("MAP_ROUTE28_SACRED_OLIVES", 0),
    "asclepeion": ("MAP_DELPHOI", 4), "agora": ("MAP_DELPHOI", 5),
    "melissai": ("MAP_DELPHOI", 6), "pilgrims": ("MAP_DELPHOI", 7), "koretas": ("MAP_DELPHOI", 8),
    "theokles": ("MAP_DELPHOI", 9), "kitharode": ("MAP_DELPHOI", 10),
    "astyra": ("MAP_DELPHOI", 2), "siphnos": ("MAP_DELPHOI", 1), "lesche": ("MAP_DELPHOI", 3),
}
PEOPLE = {
    "hut": [("LOCALID_HUT_HIERON", "ICHOR_ELDER_M", "Hieron", None)],
    "asclepeion": [("LOCALID_DELPHOI_HEALER", "ICHOR_HEALER", "Healer", None),
                   ("LOCALID_DELPHOI_OCHTHOS", "ICHOR_YOUTH_M", "Ochthos", "FLAG_ICHOR_HIDE_OCHTHOS_DELPHOI")],
    "agora": [("LOCALID_DELPHOI_LAMPSAKOS", "ICHOR_MERCHANT", "Lampsakos", None)],
    "melissai": [("LOCALID_MELISSAI_HAGNE", "ICHOR_ELDER_F", "Hagne", None),
                 ("LOCALID_MELISSAI_MOM", "ICHOR_MOM", "Mom", "FLAG_ICHOR_HIDE_MOM_MELISSAI")],
    "theokles": [("LOCALID_THEOKLES", "ICHOR_ELDER_M", "Theokles", None)],
    "pilgrims": [("LOCALID_PILGRIMS_THEOXENA", "ICHOR_WOMAN", "Theoxena", None),
                 ("LOCALID_PILGRIMS_PHILAGROS", "ICHOR_PILGRIM", "Philagros", "FLAG_ICHOR_GOT_PHILAGROS_BELL")],
    "koretas": [("LOCALID_KORETAS", "ICHOR_GOATHERD", "Koretas", None),
                ("LOCALID_KORETAS_AIX", "ICHOR_KID_F", "Aix", None)],
    "kitharode": [("LOCALID_CHRYSOTHEMIS", "ICHOR_YOUTH_M", "Chrysothemis", None)],
    "astyra": [("LOCALID_ASTYRA_ARISTION", "ICHOR_ELDER_M", "Aristion", None),
               ("LOCALID_ASTYRA_ALETHEA", "ICHOR_ALETHEA", "Alethea", "FLAG_ICHOR_HIDE_ALETHEA_TREASURY")],
    "siphnos": [("LOCALID_SIPHNOS_EUPOLIS", "ICHOR_MAN", "Eupolis", None)],
    "lesche": [("LOCALID_LESCHE_POLEMON", "ICHOR_SCHOLAR" if False else "ICHOR_ELDER_M", "Polemon", None)],
}
FACE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
        "west": "MOVEMENT_TYPE_FACE_LEFT", "east": "MOVEMENT_TYPE_FACE_RIGHT"}
FACING = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
          "west": "BG_EVENT_PLAYER_FACING_WEST", "east": "BG_EVENT_PLAYER_FACING_EAST"}


def write_events():
    for key, spec in ROOMS.items():
        name = spec["layout"]
        prefix = name + "_EventScript_"
        mp = ROOT / "data/maps" / name / "map.json"
        mj = json.loads(mp.read_text())
        warp = next(s for s in spec["spots"] if s[0] == "warp")
        dest, dw = DOOR[key]
        mj["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(dw)}
                             for (x, y) in warp[2]]
        npcs = [s for s in spec["spots"] if s[0] == "npc"]
        objs = []
        for (lid, gfx, script, flag), s in zip(PEOPLE[key], npcs):
            (x, y), face = s[2], s[3]
            objs.append({"local_id": lid, "graphics_id": "OBJ_EVENT_GFX_" + gfx, "x": x, "y": y,
                         "elevation": 3, "movement_type": FACE[face], "movement_range_x": 0,
                         "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
                         "trainer_sight_or_berry_tree_id": "0", "script": prefix + script,
                         "flag": flag or "0"})
        mj["object_events"] = objs
        bgs = []
        for i, s in enumerate(x for x in spec["spots"] if x[0] == "bg"):
            (x, y) = s[2]
            bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                        "player_facing_dir": FACING[s[3][2]], "script": prefix + f"Thing{i + 1}"})
        mj["bg_events"] = bgs
        mj["coord_events"] = []
        mp.write_text(json.dumps(mj, indent=2, ensure_ascii=False) + "\n")


def main():
    import ergasteria_build as EB
    import delphoi_rooms_art as DA
    me = sys.modules[__name__]
    EB.room_modules = lambda: [me]
    EB.IMG = ROOT / R.rstrip("/")
    EB.IMG.mkdir(parents=True, exist_ok=True)
    rs = EB.RoomSet("oikia_delphoi", "gTileset_OikiaDelphoi", DA,
                    tiles_doc=ROOT / "design/phase4/TILES_oikia_delphoi.md", default_rooms_doc=ROOMS_DOC)
    EB.build(rs, EB.parse_args())
    write_events()


if __name__ == "__main__":
    main()
