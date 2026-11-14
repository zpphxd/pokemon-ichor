#!/usr/bin/env python3
"""Aegina's three homes: the inn, the mint and Aiakides's house.

Every house in a town is a home, and every interior is unique
(design/MAP_DESIGN.md section 2). These three are laid out from the ergasteria
tileset (design/phase2/TILES_ergasteria.md); the people and what happens in
each are in design/phase2/SCRIPT.md, Part 2, "Aegina Town". The render-and-
critique passes are recorded in design/phase2/ROOMS_ergasteria.md.

Room format (as oikia_rooms.py's, with two additions):
  grid    one string per row: '.' the room's floor, 'W' its wall, '#' void;
          `floors` and `walls` map more characters to other floors and walls
  stamps  (stamp, x, y), the stamp's top-left cell
  rugs    (design, x, y, w, h)
  spots   what the scripts need; ergasteria_build.py checks every warp,
          person and readable thing is walkable and reachable from warp 0.
          A "perch" is someone placed on a piece of furniture, talked to from
          the tile given, like a bg event.
  layout  the data/layouts/ folder; render: the 2x image in design/phase2/img/

  /usr/bin/python3 tools/ichor/maps/aegina_homes.py   # builds ergasteria and the rooms

Each room's exit is warp 0, the door mat, back to MAP_AEGINA_TOWN.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

ROOMS = {
    # ------------------------------------------------------------------
    # The inn. Endeis keeps it, and has seen every sailor in the gulf twice.
    # The street door opens into a little flagged courtyard: the rain cistern
    # in the middle, the turtle mosaic between it and the door, and over the
    # north side the timber gallery of guest rooms, its ladder at the west
    # end. Through the posts to the west is the common room, terracotta,
    # round its open hearth; that's where beat 10B's night scene plays:
    # Kleon with his back to the wall, Alethea by the fire with her scroll,
    # the player across from Kleon. Endeis serves from her stores by the
    # west wall, and the sailors eat at the long table on the rug.
    "inn": {
        "title": "The inn, Aegina",
        "map": "MAP_AEGINA_TOWN_INN",
        "layout": "AeginaTown_Inn",
        "render": "aegina_inn.png",
        "floor": "terracotta",
        "floors": {",": "flags"},
        "wall": "blue",
        "walls": {"G": "gallery"},
        "grid": [
            "WWWWWWWWGGGGGGGG",
            "WWWWWWWWGGGGGGGG",
            "........GGGGGGGG",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
            "........,,,,,,,,",
        ],
        "rugs": [("blue", 1, 8, 6, 3)],
        "stamps": [
            # the common room's back wall
            ("herbs", 0, 0),
            ("window", 1, 0),
            ("jar_shelf", 2, 0),
            ("window", 4, 0),
            ("niche", 5, 0),
            ("honey_shelf", 6, 0),
            # the gallery and its ladder
            ("gallery_rail", 8, 0),
            ("gallery_door", 9, 0),
            ("gallery_rail", 10, 0),
            ("gallery_door", 11, 0),
            ("gallery_blanket", 12, 0),
            ("gallery_door", 13, 0),
            ("gallery_lamp", 14, 0),
            ("gallery_door", 15, 0),
            ("ladder", 8, 1),
            # the common room: the hearth, Endeis's stores, the long table
            ("amphora", 0, 2),
            ("fish_basket", 1, 2),
            ("hearth_floor", 2, 3),
            ("bench", 0, 4),
            ("lampstand", 5, 4),
            ("pithos", 0, 6),
            ("pots", 1, 7),
            ("table_round", 6, 6),
            ("table", 2, 9),
            ("table", 4, 9),
            ("klismos_r", 1, 9),
            ("klismos_l", 6, 9),
            ("knucklebones", 0, 11),
            ("column", 7, 4),
            ("column", 7, 8),
            # the courtyard
            ("myrtle", 9, 3),
            ("myrtle", 15, 3),
            ("cistern", 11, 4),
            ("pithos", 15, 5),
            ("mosaic_turtle", 10, 7),
            ("amphora_plain", 15, 9),
            ("mat", 11, 11),
        ],
        "spots": [
            ("warp", "door to Aegina Town (south-arrow mat)", [(11, 11), (12, 11)]),
            ("npc", "Endeis, the innkeeper, by her stores and the bread table", (5, 6), "south"),
            ("npc", "Kleon, the voyage night: back to the wall, eating bread", (3, 2), "south"),
            ("npc", "Alethea, the voyage night: her scroll open by the fire", (4, 4), "west"),
            ("coord", "the player's seat by the fire (the night scene puts them here)", (2, 5)),
            ("coord", "beside the ladder's foot, where Kleon climbs to the loft", (7, 3)),
            ("bg", "the hearth", (2, 4), (2, 5, "north")),
            ("bg", "the cistern", (11, 5), (11, 6, "north")),
            ("bg", "the turtle mosaic, read from below it", (11, 9), (11, 10, "north")),
            ("bg", "the ladder to the guest gallery", (8, 3), (7, 3, "east")),
        ],
    },
    # ------------------------------------------------------------------
    # The mint. Pheidon strikes the island's turtle coins in a deep stone
    # strongroom with no window: the dies on their rack, the vault's
    # bronze-bound door with its coin slot, the turtle strongbox beside it;
    # two anvils with the blank-heating brazier between them, where he works;
    # the counting table and the balance by the door, for whoever comes in.
    "mint": {
        "title": "The mint, Aegina",
        "map": "MAP_AEGINA_TOWN_MINT",
        "layout": "AeginaTown_Mint",
        "render": "aegina_mint.png",
        "floor": "flags",
        "wall": "stone",
        "grid": [
            "WWWWWWWWW",
            "WWWWWWWWW",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
        ],
        "rugs": [],
        "stamps": [
            ("die_rack", 0, 0),
            ("lampstand", 2, 1),
            ("vault_door", 3, 0),
            ("turtle_chest", 4, 1),
            ("pithos", 7, 1),
            ("scales", 8, 1),
            ("anvil", 1, 4),
            ("brazier_small", 2, 4),
            ("anvil", 3, 4),
            ("coin_table", 6, 4),
            ("stool", 7, 5),
            ("amphora_plain", 0, 6),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Aegina Town (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "Pheidon, the moneyer, at his anvils", (2, 5), "north"),
            ("perch", "Pheidon's Chelonet, sitting on the stamps (the anvil)", (3, 4), (3, 5, "north")),
            ("bg", "the vault door and its coin slot", (3, 1), (3, 2, "north")),
            ("bg", "the strongbox", (4, 2), (4, 3, "north")),
            ("bg", "the die rack", (1, 1), (1, 2, "north")),
            ("bg", "the balance", (8, 2), (8, 3, "north")),
            ("bg", "the counting table", (6, 4), (6, 5, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # Aiakides's house. An old soldier, whose family were ants before they
    # were people. A small L of a house, the street side cut away by the
    # neighbor's yard: his bed under the shield and spear, the shrine with
    # its clay ant by the hearth, his chair at the table where the crumbs
    # fall, and in the back corner the big pot with the anthill he feeds,
    # its ants marching for the table.
    "aiakides": {
        "title": "Aiakides's house, Aegina",
        "map": "MAP_AEGINA_TOWN_AIAKIDES_HOUSE",
        "layout": "AeginaTown_AiakidesHouse",
        "render": "aegina_aiakides.png",
        "floor": "terracotta",
        "wall": "red",
        "grid": [
            "WWWWWWWW",
            "WWWWWWWW",
            "........",
            "........",
            "........",
            "........",
            "##......",
            "##......",
        ],
        "rugs": [("red", 3, 4, 3, 2)],
        "stamps": [
            ("soot", 0, 0),
            ("hearth", 0, 2),
            ("ant_shrine", 2, 1),
            ("shield_spear", 3, 0),
            ("kline", 3, 2),
            ("window", 5, 0),
            ("anthill_pot", 7, 1),
            ("ant_trail", 6, 3),
            ("ant_trail", 5, 4),
            ("table_round", 4, 5),
            ("klismos_r", 3, 5),
            ("amphora", 0, 4),
            ("pithos", 7, 5),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Aegina Town (south-arrow mat)", [(4, 7), (5, 7)]),
            ("npc", "Aiakides, by his chair", (2, 5), "east"),
            ("bg", "the clay-ant shrine", (2, 2), (2, 3, "north")),
            ("bg", "the bed, under the shield and spear", (4, 2), (5, 2, "west")),
            ("bg", "the anthill in its pot", (7, 2), (7, 3, "north")),
        ],
    },
}


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import ergasteria_build
    ergasteria_build.main()
