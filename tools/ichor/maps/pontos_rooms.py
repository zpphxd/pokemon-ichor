#!/usr/bin/env python3
"""The Black Sea's rooms: Salmydessos's two and Aia's five (batch 1).

Every house is a home and every interior is unique (design/MAP_DESIGN.md §2).
Who lives in each and what happens there is design/OIKOUMENE.md §4.3; the
rooms' plans, people and render-and-critique passes are written down in
design/oikoumene/ROOMS_pontos.md. Every room is built from gTileset_Chalkeon
(tools/ichor/art/chalkeon_art.py) on the oikos primary.

Room format (world-act1's aegina_homes.py, after oikia_rooms.py):
  grid    one string per row: '.' the room's floor, 'W' its wall, '#' void;
          `floors` and `walls` map more characters to other floors and walls
  stamps  (stamp, x, y), the stamp's top-left cell
  spots   what the scripts need; chalkeon_build.py checks that every warp,
          person and readable thing is walkable and reachable from warp 0.
          A "perch" is someone placed on furniture, talked to from the tile
          given, like a bg event.
  variants  the room after an event: stamps swapped; the builder writes the
          setmetatile script into the map's scripts.pory
  layout  the data/layouts/ folder; render: the 2x image in design/oikoumene/img/

Door warps (design/oikoumene/BUILD.md §5): each room's warp 0 is its door mat,
back to MAP_SALMYDESSOS or MAP_AIA warp i, where i is the room's place in
BUILD.md's table (Salmydessos: 0 Phineus, 1 the bird-catcher; Aia: 0
Asclepeion, 1 Agora, 2 Phrixos's sons, 3 the linen-weaver, 4 the workshop).

  /usr/bin/python3 tools/ichor/maps/pontos_rooms.py   # builds chalkeon and the rooms
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

ROOMS = {
    # ------------------------------------------------------------------
    # Phineus's house. The blind seer's spare room: a long table, bare,
    # scored by forty years of Harpies' claws; he ate standing so he could
    # run. The shutters stay shut (he has no use for the light), the claw
    # marks run down the plaster beside them, and a dark feather is still
    # caught in the beam. His couch in the far corner; the jars by the west
    # wall full for the first time in his life; one new stool he keeps
    # forgetting to sit on. The dove's cage hangs by the window.
    "phineus": {
        "title": "Phineus's house, Salmydessos",
        "map": "MAP_SALMYDESSOS_PHINEUSS_HOUSE",
        "layout": "Salmydessos_PhineussHouse",
        "render": "salmydessos_phineus.png",
        "floor": "flags",
        "wall": "plaster",
        "town": ("MAP_SALMYDESSOS", 0),
        "grid": [
            "WWWWWWWWWW",
            "WWWWWWWWWW",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
        ],
        "stamps": [
            ("shutters_shut", 2, 0),
            ("dove_cage", 3, 0),
            ("claw_marks", 6, 0),
            ("pithos", 0, 2),
            ("amphora", 1, 2),
            ("kline", 8, 2),
            ("table_bare", 3, 4),
            ("stool", 7, 5),
            ("mat", 4, 7),
        ],
        "variants": {
            "dove_given": {"swap": {"dove_cage": "dove_cage_empty"},
                           "script": "Salmydessos_PhineussHouse_EventScript_EmptyCage"},
        },
        "spots": [
            ("warp", "door to Salmydessos (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "Phineus, at the head of his bare table", (6, 4), "west"),
            ("bg", "the dove's cage, hung by the window", (3, 1), (3, 2, "north")),
            ("bg", "the shutters, barred", (2, 1), (2, 2, "north")),
            ("bg", "the claw marks and the feather", (6, 1), (6, 2, "north")),
            ("bg", "the bare table", (4, 4), (4, 5, "north")),
            ("bg", "the full jars", (1, 3), (1, 4, "north")),
            ("bg", "the new stool", (7, 5), (7, 6, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The bird-catcher's house. Ixos traps songbirds on the cliffs with
    # lime-sticks and a decoy owl and sells them in cages. A wattle-and-daub
    # room: his stock stacked on a pole rack by the west wall, a spare cage
    # on the wall, the lime-sticks standing by the east wall, the decoy on its
    # post in the middle of the floor, his table of seed. His Unfezant has
    # the run of the place.
    "birdcatcher": {
        "title": "The bird-catcher's house, Salmydessos",
        "map": "MAP_SALMYDESSOS_BIRD_CATCHERS_HOUSE",
        "layout": "Salmydessos_BirdCatchersHouse",
        "render": "salmydessos_birdcatcher.png",
        "floor": "earth",
        "wall": "wattle",
        "town": ("MAP_SALMYDESSOS", 1),
        "grid": [
            "WWWWWWWWW",
            "WWWWWWWWW",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
        ],
        "stamps": [
            ("cage_stack", 0, 1),
            ("dove_cage_empty", 3, 0),
            ("lime_sticks", 8, 1),
            ("pots", 2, 2),
            ("decoy_owl", 5, 4),
            ("table_round", 7, 4),
            ("mat", 3, 6),
        ],
        "spots": [
            ("warp", "door to Salmydessos (south-arrow mat)", [(3, 6), (4, 6)]),
            ("npc", "Ixos, the bird-catcher", (4, 3), "south"),
            ("npc", "his Unfezant (the player's Pidgeot after the trade), by the decoy", (6, 4), "west"),
            ("bg", "the cages", (1, 2), (1, 3, "north")),
            ("bg", "the lime-sticks", (8, 2), (8, 3, "north")),
            ("bg", "the decoy owl", (5, 4), (5, 5, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The Asclepeion. Bronze and enamel, the way Aietes builds. The healer's
    # counter runs along the west half of the back wall, a bronze bull's head
    # pouring the spring into its basin; Medea's country's herbs on the shelf
    # behind it; the Pithos in the east corner. The couches stand along the
    # east wall, under the lamp, and Asclepius's serpent coils on its post
    # between them and the door.
    "asclepeion": {
        "title": "The Asclepeion, Aia",
        "map": "MAP_AIA_ASCLEPEION",
        "layout": "Aia_Asclepeion",
        "render": "aia_asclepeion.png",
        "floor": "enamel",
        "wall": "bronze_enamel",
        "town": ("MAP_AIA", 0),
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
            ".............",
        ],
        "stamps": [
            ("bull_fountain", 2, 1),
            ("asc_top_l", 1, 2),
            ("asc_top_m", 4, 2),
            ("asc_top_m", 5, 2),
            ("asc_top_r", 6, 2),
            ("asc_front_l", 1, 3),
            ("asc_front_m", 2, 3),
            ("asc_front_m", 3, 3),
            ("asc_front_rod", 4, 3),
            ("asc_front_m", 5, 3),
            ("asc_front_r", 6, 3),
            ("jar_shelf", 4, 0),
            ("pithos_great", 10, 1),
            ("kline", 11, 6),
            ("kline", 11, 8),
            ("kline", 0, 5),
            ("kline", 0, 7),
            ("serpent_post", 8, 6),
            ("mat", 6, 9),
        ],
        "spots": [
            ("warp", "door to Aia (south-arrow mat)", [(6, 9), (7, 9)]),
            ("counter", "the healer, behind the counter", (4, 2), (4, 4, "north")),
            ("npc", "a Colchian woman, sitting up with the sick by the couches", (10, 7), "east"),
            ("npc", "an old man by the Pithos", (9, 3), "east"),
            ("bg", "the Pithos (left)", (10, 2), (10, 3, "north")),
            ("bg", "the Pithos (right)", (11, 2), (11, 3, "north")),
            ("bg", "the bronze serpent", (8, 7), (8, 8, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The Agora. A timber market hall with two posts down the middle. The
    # stall runs along the east half of the back wall, the Pontic honey on
    # the shelf behind it, a balance at one end. On the west wall a fleece
    # stretched on its frame, gold dust from the Phasis caught in the wool;
    # pheasants hung by the window; linen and pitch by the walls.
    "agora": {
        "title": "The Agora, Aia",
        "map": "MAP_AIA_AGORA",
        "layout": "Aia_Agora",
        "render": "aia_agora.png",
        "floor": "planks",
        "wall": "logs",
        "town": ("MAP_AIA", 1),
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
        "stamps": [
            ("fleece_frame", 1, 0),
            ("window_lattice", 4, 0),
            ("pheasants", 5, 0),
            ("window_lattice", 11, 0),
            ("stall_top_l", 7, 2),
            ("stall_top_m", 8, 2),
            ("stall_top_m", 9, 2),
            ("stall_top_r", 10, 2),
            ("stall_front_l", 7, 3),
            ("stall_front_m", 8, 3),
            ("stall_front_m", 9, 3),
            ("stall_front_r", 10, 3),
            ("linen_bolts", 0, 2),
            ("linen_bolts", 0, 3),
            ("log_post", 2, 5),
            ("log_post", 9, 5),
            ("amphora", 11, 5),
            ("pots", 11, 7),
            ("pithos", 0, 6),
            ("mat", 5, 8),
        ],
        "spots": [
            ("warp", "door to Aia (south-arrow mat)", [(5, 8), (6, 8)]),
            ("counter", "the stallkeeper, behind the counter", (9, 2), (9, 4, "north")),
            ("npc", "a Colchian man, looking at the fleece", (2, 3), "north"),
            ("npc", "a Greek sailor, haggling over honey", (6, 5), "east"),
            ("bg", "the fleece on its frame", (1, 1), (1, 2, "north")),
            ("bg", "the pheasants", (5, 1), (5, 2, "north")),
            ("bg", "the linen", (0, 3), (1, 3, "west")),
        ],
    },
    # ------------------------------------------------------------------
    # Phrixos's sons' house. Exiles from Greece in a Colchian log house:
    # their father kept a Greek hearth and a Greek table, and the painted
    # panel of the ram that brought him here hangs over the altar of Zeus of
    # Escape, to whom he sacrificed it. Their model of the ship that wrecked
    # them on the Isle of Ares, and the oars they kept; their father's couch.
    "phrixos": {
        "title": "Phrixos's sons' house, Aia",
        "map": "MAP_AIA_PHRIXOS_SONS_HOUSE",
        "layout": "Aia_PhrixosSonsHouse",
        "render": "aia_phrixos.png",
        "floor": "planks",
        "wall": "logs",
        "town": ("MAP_AIA", 2),
        "grid": [
            "WWWWWWWWWW",
            "WWWWWWWWWW",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
            "..........",
        ],
        "stamps": [
            ("hearth", 0, 2),
            ("window_lattice", 2, 0),
            ("ram_panel", 4, 0),
            ("altar", 4, 2),
            ("window_lattice", 7, 0),
            ("kline", 8, 4),
            ("table", 3, 5),
            ("klismos_r", 2, 5),
            ("klismos_l", 5, 5),
            ("amphora", 0, 5),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Aia (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "Argos, the eldest, by his father's altar", (5, 3), "south"),
            ("perch", "Phrontis, on his chair at the table", (2, 5), (2, 6, "north")),
            ("npc", "Melas, minding the hearth", (2, 3), "west"),
            ("bg", "the ram panel", (5, 1), (5, 2, "north")),
            ("bg", "the altar of Zeus of Escape", (4, 3), (4, 4, "north")),
            ("bg", "the hearth", (1, 3), (1, 4, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The linen-weaver's house. Byssa weaves linen the way the Egyptians do
    # (Herodotus 2.105), on a ground loom pegged into the earth floor, which
    # takes up the middle of the room. Flax leans on the west wall, still in
    # flower; linen bleaches on a line across the back; bolts of it wait by
    # the east wall, and the flax rets in a tub by the door. Her Persian
    # sleeps wherever the light is.
    "linen": {
        "title": "The linen-weaver's house, Aia",
        "map": "MAP_AIA_LINEN_WEAVERS_HOUSE",
        "layout": "Aia_LinenWeaversHouse",
        "render": "aia_linen.png",
        "floor": "earth",
        "wall": "logs",
        "town": ("MAP_AIA", 3),
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
        ],
        "stamps": [
            ("flax", 0, 1),
            ("flax", 1, 1),
            ("window_lattice", 3, 0),
            ("linen_line", 5, 0),
            ("window_lattice", 8, 0),
            ("linen_bolts", 9, 2),
            ("linen_bolts", 10, 2),
            ("ground_loom", 3, 3),
            ("kalathos", 7, 3),
            ("pithos", 10, 4),
            ("retting_tub", 8, 6),
            ("mat", 5, 7),
        ],
        "spots": [
            ("warp", "door to Aia (south-arrow mat)", [(5, 7), (6, 7)]),
            ("npc", "Byssa, the linen-weaver, at the end of her loom", (6, 4), "west"),
            ("npc", "her Persian, asleep in the light (the player's Liepard after the trade)", (2, 6), "south"),
            ("bg", "the ground loom", (4, 4), (4, 5, "north")),
            ("bg", "the linen on its line", (5, 1), (5, 2, "north")),
            ("bg", "the flax", (1, 2), (1, 3, "north")),
            ("bg", "the linen bolts", (9, 2), (9, 3, "north")),
            ("bg", "the retting tub", (8, 6), (8, 5, "south")),
        ],
    },
    # ------------------------------------------------------------------
    # The palace workshop. Hephaestus's self-moving works, which Aietes
    # keeps a tinker to oil. A bull's head in the back wall breathes on the
    # fire-jar below it; a golden maid stands against the wall and turns her
    # head; Tekton's bench, with a tripod half on its wheels. Round the room,
    # the five works a Rotom can get into: the fire-jar, the wash-basin, the
    # cold krater, the fan and the reaping-sledge.
    "workshop": {
        "title": "The palace workshop, Aia",
        "map": "MAP_AIA_PALACE_WORKSHOP",
        "layout": "Aia_PalaceWorkshop",
        "render": "aia_workshop.png",
        "floor": "flags",
        "wall": "bronze",
        "town": ("MAP_AIA", 4),
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
        "stamps": [
            ("golden_maid", 1, 1),
            ("bull_head", 6, 0),
            ("fire_jar", 6, 2),
            ("workbench", 9, 3),
            ("tripod_wheels", 4, 3),
            ("wash_basin", 2, 4),
            ("cold_krater", 11, 5),
            ("fan", 4, 6),
            ("sledge", 9, 7),
            ("mat", 6, 8),
        ],
        "spots": [
            ("warp", "door to Aia (south-arrow mat)", [(6, 8), (7, 8)]),
            ("npc", "Tekton, the palace's tinker, at his bench", (10, 4), "north"),
            ("npc", "a Rotom, loose in the works", (7, 5), "south"),
            ("bg", "the fire-jar", (6, 3), (6, 4, "north")),
            ("bg", "the wash-basin", (2, 5), (2, 6, "north")),
            ("bg", "the cold krater", (11, 6), (11, 7, "north")),
            ("bg", "the fan", (4, 7), (4, 8, "north")),
            ("bg", "the reaping-sledge", (9, 7), (9, 6, "south")),
            ("bg", "the golden maid", (1, 2), (1, 3, "north")),
            ("bg", "the wheeled tripod", (4, 3), (4, 4, "north")),
            ("bg", "the workbench", (9, 3), (9, 4, "north")),
        ],
    },
}


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import chalkeon_build
    chalkeon_build.main()
