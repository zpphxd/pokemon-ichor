#!/usr/bin/env python3
"""The Troad's interiors: every room of Sestos and Ilion, from the megaron set.

Every house in a town is a home and every interior is unique
(design/MAP_DESIGN.md §2): each room below has its own shape, size and
furniture, chosen for who lives or works there. Public buildings of a kind (the
two Asclepeions, the two Agoras) share their counter, never their plan. Who
lives in each and what happens there is design/OIKOUMENE.md §4.1; the scripts
are each map's scripts.pory, and the render-and-critique passes are written
down in design/oikoumene/ROOMS_troad.md.

Room format (world-act1's, from oikia's):
  grid    one string per row: '.' the room's floor, 'W' its back wall, '#' void;
          `floors` and `walls` map more characters to other floors and walls
  stamps  (stamp, x, y): the stamp's top-left cell
  rugs    (design, x, y, w, h)
  spots   what the scripts need; megaron_build.py checks every one is
          walkable and reachable from warp 0:
            ("warp", label, [(x, y)])              the door mat is warp 0
            ("npc", label, (x, y), facing)
            ("bg", label, (x, y), (fx, fy, facing)) read from (fx, fy)
            ("coord", label, (x, y))
            ("counter", label, (x, y), (fx, fy, facing)) someone behind a
                                                    counter, talked to across it
  variants  {name: {"swap": {stamp: stamp}, "script": label}}: the room after
          an event; the builder writes the setmetatile script
  layout  the data/layouts/ folder; render: the 2x image in design/oikoumene/img/

  /usr/bin/python3 tools/ichor/art/megaron_build.py   # builds megaron and these rooms

Each room's warp 0 is its door mat, back to its town's warp with the room's
number (design/oikoumene/BUILD.md §5): MAP_SESTOS 0-4, MAP_ILION 0-8.
"""

# The door warps, in BUILD.md §5's order: the room's warp 0 sends to this
# warp of its town, and the town's door with this id sends to the room's warp 0.
TOWN_WARP = {
    "MAP_SESTOS_ASCLEPEION": ("MAP_SESTOS", 0),
    "MAP_SESTOS_AGORA": ("MAP_SESTOS", 1),
    "MAP_SESTOS_HEROS_TOWER": ("MAP_SESTOS", 2),
    "MAP_SESTOS_FERRY_HOUSE": ("MAP_SESTOS", 3),
    "MAP_SESTOS_NET_LOFT": ("MAP_SESTOS", 4),
    "MAP_ILION_ASCLEPEION": ("MAP_ILION", 0),
    "MAP_ILION_AGORA": ("MAP_ILION", 1),
    "MAP_ILION_PRIAMS_PALACE": ("MAP_ILION", 2),
    "MAP_ILION_CASSANDRAS_ROOM": ("MAP_ILION", 3),
    "MAP_ILION_GUEST_ROOM": ("MAP_ILION", 4),
    "MAP_ILION_HORSE_STABLE": ("MAP_ILION", 5),
    "MAP_ILION_MASONS_HOUSE": ("MAP_ILION", 6),
    "MAP_ILION_WEAVERS_HOUSE": ("MAP_ILION", 7),
    "MAP_ILION_TEMPLE_OF_ATHENA": ("MAP_ILION", 8),
}

ROOMS = {
    # ==================================================================
    # Sestos
    # ==================================================================

    # The harbor Asclepeion. Its back wall opens on the Hellespont: a broad
    # window with Asia's shore across the strait, and under it the couches,
    # so the sick can watch the boats. The counter and the spring are to the
    # left of the door, the Pithos beside them; nets on the wall, because
    # half the patients are fishermen.
    "sestos_asclepeion": {
        "title": "Sestos Asclepeion: the harbor's, with a window on the strait",
        "map": "MAP_SESTOS_ASCLEPEION",
        "layout": "Sestos_Asclepeion",
        "render": "sestos_asclepeion.png",
        "floor": "flags",
        "wall": "sea",
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
        "rugs": [("kilim", 5, 5, 3, 2)],
        "stamps": [
            ("lampstand", 0, 1),
            ("basin", 1, 1),
            ("rod", 3, 0),
            ("amphora_grey", 4, 1),
            ("counter_l", 1, 3),
            ("counter_m", 2, 3),
            ("counter_m", 3, 3),
            ("counter_r", 4, 3),
            ("great_pithos", 6, 1),
            ("sea_window", 9, 0),
            ("nets", 11, 0),
            ("kline", 9, 4),
            ("kline", 9, 7),
            ("brazier", 12, 5),
            ("fish_basket", 0, 6),
            ("stool", 1, 6),
            ("mat", 6, 8),
        ],
        "spots": [
            ("warp", "door to Sestos, warp 0 (south-arrow mat)", [(6, 8)]),
            ("counter", "the healer, behind the counter", (3, 2), (3, 4, "north")),
            ("npc", "an old woman at the window, watching the strait", (11, 2), "west"),
            ("npc", "a sailor with a rope-burned hand, by his mate's couch", (11, 4), "west"),
            ("bg", "the Pithos", (6, 2), (6, 3, "north")),
            ("bg", "the Pithos, right half", (7, 2), (7, 3, "north")),
            ("bg", "the window on the strait", (9, 1), (9, 2, "north")),
            ("bg", "the window on the strait, right half", (10, 1), (10, 2, "north")),
        ],
    },

    # A chandler's stall on the quay: rope, oil, nets and the late-game
    # stock a sailor needs a long way from home. Deep shelves behind the
    # counter, a table of goods to haggle over, rope coiled everywhere. The
    # room steps in at the bottom left, where the quay's bollard stands.
    "sestos_agora": {
        "title": "Sestos Agora: a chandler's stall on the quay",
        "map": "MAP_SESTOS_AGORA",
        "layout": "Sestos_Agora",
        "render": "sestos_agora.png",
        "floor": "boards",
        "wall": "sea",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "...........",
            "##.........",
            "##.........",
        ],
        "rugs": [],
        "stamps": [
            ("goods", 0, 1),
            ("amphora_grey", 3, 1),
            ("rope", 4, 2),
            ("counter_l", 0, 3),
            ("counter_m", 1, 3),
            ("counter_m", 2, 3),
            ("counter_m", 3, 3),
            ("counter_r", 4, 3),
            ("nets", 5, 0),
            ("window", 7, 0),
            ("goods", 8, 1),
            ("pithos", 10, 1),
            ("floats", 2, 0),
            ("table", 5, 5),
            ("stool", 4, 5),
            ("net_rack", 8, 5),
            ("rope", 10, 4),
            ("rope", 10, 6),
            ("fish_basket", 7, 7),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Sestos, warp 1 (south-arrow mat)", [(4, 7)]),
            ("counter", "the chandler, behind the counter", (2, 2), (2, 4, "north")),
            ("npc", "a sailor reading the shelves", (8, 3), "north"),
            ("bg", "the shelves of goods", (8, 2), (8, 3, "north")),
        ],
    },

    # Hero's tower: one tall room, the ground floor at the bottom, the
    # lamp room at the top, and between them the windy stair, landing by
    # landing. Ribbons on the slits mark the draughts: a carried flame dies in
    # front of one (SYSTEMS §2, the wind verb). The first landing teaches it
    # with one draught and room to step round; the second weaves between two
    # draughts and an oil jar. Hero keeps the lamp at the top; the hearth
    # whose flame she wants is at the bottom, by her bed and her oil.
    "sestos_heros_tower": {
        "title": "Hero's tower, Sestos: the lamp room, the windy stair and her rooms",
        "map": "MAP_SESTOS_HEROS_TOWER",
        "layout": "Sestos_HerosTower",
        "render": "sestos_heros_tower.png",
        "floor": "flags",
        "wall": "ashlar",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "...........",
        ],
        "rugs": [("kilim", 2, 16, 3, 2)],
        "stamps": [
            # the lamp room
            ("slit", 1, 0),
            ("sea_window", 4, 0),
            ("slit", 9, 0),
            ("great_lamp", 4, 2),
            ("pithos", 0, 2),
            ("amphora_grey", 10, 2),
            ("draught", 2, 7),
            ("draught", 6, 7),
            ("draught", 5, 11),
            # the upper landing: two draughts and an oil jar to weave between
            ("slit_draught", 2, 5),
            ("slit", 4, 5),
            ("slit_draught", 6, 5),
            ("stair", 8, 5),
            ("oil_jar", 4, 8),
            # the lower landing: one draught, room to step round it
            ("stair", 1, 9),
            ("slit", 3, 9),
            ("slit_draught", 5, 9),
            ("slit", 8, 9),
            ("amphora_grey", 10, 10),
            # the ground floor: her bed, her hearth, her oil
            ("window", 5, 13),
            ("stair", 9, 13),
            ("kline", 0, 15),
            ("brazier", 3, 14),
            ("pithos", 7, 14),
            ("pithos", 8, 14),
            ("table", 6, 17),
            ("stool", 8, 17),
            ("amphora_grey", 10, 15),
            ("mat", 5, 18),
        ],
        "spots": [
            ("warp", "door to Sestos, warp 2 (south-arrow mat)", [(5, 18)]),
            ("npc", "Hero, keeping the lamp, watching the strait", (7, 3), "south"),
            ("bg", "the great lamp", (4, 3), (4, 4, "north")),
            ("bg", "the great lamp, right half", (5, 3), (5, 4, "north")),
            ("bg", "Hero's hearth: take a flame", (3, 15), (3, 16, "north")),
            ("coord", "a draught: the upper landing, west slit", (2, 7)),
            ("coord", "a draught: the upper landing, east slit", (6, 7)),
            ("coord", "a draught: the lower landing", (5, 11)),
            ("coord", "the top of the stair, arriving in the lamp room", (8, 4)),
        ],
        "variants": {
            "lit": {"swap": {"great_lamp": "great_lamp_lit"}, "script": "Sestos_HerosTower_EventScript_LightLampTiles"},
        },
    },

    # The ferryman's house, down by the boats. Kymon swam the strait as a
    # boy, and the olive wreath he won for it hangs over his chair. Oars and
    # a net by the door, rope on the floor, his Cramorant by the fire. The
    # back wall steps forward over the sleeping bay on the right.
    "sestos_ferry_house": {
        "title": "The ferry house, Sestos: Kymon the ferryman's",
        "map": "MAP_SESTOS_FERRY_HOUSE",
        "layout": "Sestos_FerryHouse",
        "render": "sestos_ferry_house.png",
        "floor": "earth",
        "wall": "sea",
        "grid": [
            "WWWWWWW###",
            "WWWWWWW###",
            ".......WWW",
            ".......WWW",
            "..........",
            "..........",
            "..........",
            "..........",
        ],
        "rugs": [],
        "stamps": [
            ("oars", 0, 0),
            ("nets", 1, 0),
            ("wreath", 5, 0),
            ("brazier", 6, 1),
            ("window", 8, 2),
            ("stool", 3, 2),
            ("table", 2, 4),
            ("stool", 1, 4),
            ("kline", 7, 4),
            ("pithos", 9, 6),
            ("rope", 0, 6),
            ("fish_basket", 1, 7),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Sestos, warp 3 (south-arrow mat)", [(4, 7)]),
            ("npc", "Kymon the ferryman, by his chair under the wreath", (4, 2), "south"),
            ("npc", "his Cramorant, by the fire (until the trade)", (6, 3), "west"),
            ("bg", "the wreath: his prize for swimming the strait", (5, 1), (5, 2, "north")),
        ],
    },

    # The net-loft: a long low store where the harbor's nets are hung,
    # mended and dried. Two racks stand down the middle like a ship's ribs,
    # more nets and floats on the walls; the fisher mends at the far end.
    "sestos_net_loft": {
        "title": "The net-loft, Sestos",
        "map": "MAP_SESTOS_NET_LOFT",
        "layout": "Sestos_NetLoft",
        "render": "sestos_net_loft.png",
        "floor": "boards",
        "wall": "sea",
        "grid": [
            "WWWWWWWWWWWW",
            "WWWWWWWWWWWW",
            "............",
            "............",
            "............",
            "............",
            "............",
        ],
        "rugs": [],
        "stamps": [
            ("floats", 0, 0),
            ("nets", 1, 0),
            ("window", 4, 0),
            ("nets", 6, 0),
            ("floats", 8, 0),
            ("window", 10, 0),
            ("fish_basket", 0, 2),
            ("rope", 11, 2),
            ("net_rack", 2, 3),
            ("net_rack", 7, 3),
            ("stool", 10, 3),
            ("fish_basket", 0, 5),
            ("rope", 11, 6),
            ("mat", 5, 6),
        ],
        "spots": [
            ("warp", "door to Sestos, warp 4 (south-arrow mat)", [(5, 6)]),
            ("npc", "the fisher, mending a net", (10, 4), "west"),
            ("bg", "a drying rack", (3, 4), (3, 5, "north")),
        ],
    },

    # ==================================================================
    # Ilion
    # ==================================================================

    # The city's Asclepeion: frescoed, columned, built to impress. The
    # counter and spring are on the axis of the door; the Pithos stands in
    # the west corner, and the incubation couches line the east wall, where
    # pilgrims sleep hoping for a dream of the god.
    "ilion_asclepeion": {
        "title": "Ilion Asclepeion: the city's, columned, with couches for dreaming",
        "map": "MAP_ILION_ASCLEPEION",
        "layout": "Ilion_Asclepeion",
        "render": "ilion_asclepeion.png",
        "floor": "plaster",
        "wall": "fresco",
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
        "rugs": [("kilim", 6, 6, 3, 3)],
        "stamps": [
            ("great_pithos", 1, 1),
            ("lampstand", 4, 1),
            ("basin", 5, 1),
            ("rod", 7, 0),
            ("amphora_grey", 8, 1),
            ("brazier", 9, 1),
            ("counter_l", 5, 3),
            ("counter_m", 6, 3),
            ("counter_m", 7, 3),
            ("counter_m", 8, 3),
            ("counter_r", 9, 3),
            ("kline", 13, 2),
            ("kline", 13, 5),
            ("kline", 13, 8),
            ("column", 4, 4),
            ("column", 10, 4),
            ("column", 4, 8),
            ("column", 10, 8),
            ("amphora_grey", 0, 8),
            ("mat", 7, 10),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 0 (south-arrow mat)", [(7, 10)]),
            ("counter", "the healer, behind the counter", (7, 2), (7, 4, "north")),
            ("npc", "a charioteer with a strapped wrist", (12, 6), "east"),
            ("npc", "a pilgrim waiting on a dream", (12, 3), "east"),
            ("bg", "the Pithos", (1, 2), (1, 3, "north")),
            ("bg", "the Pithos, right half", (2, 2), (2, 3, "north")),
        ],
    },

    # A covered market hall on the citadel road. The stall is at the east
    # end, its counter backed by a cupboard of Trojan cloth and a rack of
    # goods; the west end is a horse-tack corner, bridles and a wheel, because
    # in Ilion everyone is buying something for a horse.
    "ilion_agora": {
        "title": "Ilion Agora: a market hall on the citadel road",
        "map": "MAP_ILION_AGORA",
        "layout": "Ilion_Agora",
        "render": "ilion_agora.png",
        "floor": "flags",
        "wall": "ashlar",
        "grid": [
            "WWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWW",
            "..............",
            "..............",
            "..............",
            "..............",
            "..............",
            "..............",
            "...........###",
        ],
        "rugs": [],
        "stamps": [
            ("bridles", 1, 0),
            ("bridles", 2, 0),
            ("wheel", 0, 2),
            ("amphora_grey", 4, 1),
            ("amphora_grey", 5, 1),
            ("window", 6, 0),
            ("goods", 8, 1),
            ("cloth_bolts", 11, 1),
            ("counter_l", 8, 3),
            ("counter_m", 9, 3),
            ("counter_m", 10, 3),
            ("counter_m", 11, 3),
            ("counter_r", 12, 3),
            ("column", 4, 5),
            ("column", 10, 5),
            ("table", 1, 5),
            ("stool", 3, 5),
            ("pithos", 13, 4),
            ("mat", 7, 8),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 1 (south-arrow mat)", [(7, 8)]),
            ("counter", "the stallkeeper, behind the counter", (10, 2), (10, 4, "north")),
            ("npc", "a horse-trader at the bridles", (2, 3), "north"),
            ("npc", "a woman fingering the cloth", (13, 6), "west"),
            ("bg", "the bridles", (1, 1), (1, 2, "north")),
        ],
    },

    # Priam's palace: a megaron in the old style. A porch of guards at the
    # door, then the hall: the great round hearth under four red columns,
    # the horse frieze behind it, and the throne against the east wall,
    # where Priam would rather talk about horses than anything else.
    "ilion_priams_palace": {
        "title": "Priam's palace, Ilion: the megaron",
        "map": "MAP_ILION_PRIAMS_PALACE",
        "layout": "Ilion_PriamsPalace",
        "render": "ilion_priams_palace.png",
        "floor": "plaster",
        "wall": "fresco",
        "grid": [
            "WWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWW",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "#..............#",
            "##............##",
            "###..........###",
        ],
        "rugs": [("kilim", 6, 10, 4, 2)],
        "stamps": [
            ("shield", 2, 0),
            ("lampstand", 4, 1),
            ("horse_fresco", 7, 0),
            ("lampstand", 11, 1),
            ("shield", 12, 0),
            ("throne", 13, 1),
            ("shield", 14, 0),
            ("round_hearth", 7, 5),
            ("column", 6, 2),
            ("column", 9, 2),
            ("column", 6, 7),
            ("column", 9, 7),
            ("table", 1, 4),
            ("klismos_r", 0, 4),
            ("klismos_l", 3, 4),
            ("krater", 2, 6),
            ("amphora_grey", 0, 7),
            ("amphora_grey", 15, 7),
            ("mat", 7, 12),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 2 (south-arrow mat)", [(7, 12)]),
            ("npc", "King Priam, beside his throne", (12, 2), "south"),
            ("npc", "a palace guard at the door, west", (5, 11), "east"),
            ("npc", "a palace guard at the door, east", (10, 11), "west"),
            ("npc", "a steward by the wine", (3, 6), "west"),
            ("bg", "the horse frieze", (8, 1), (8, 2, "north")),
            ("bg", "the hearth", (7, 6), (7, 7, "north")),
        ],
    },

    # Cassandra's room. For years she painted what she saw: Troy burning.
    # Now the visions have stopped and she's whitewashing it, half done. The
    # laurel of Apollo, who gave her the curse, sits in the corner, unwatered.
    # Her bed under the window, her chest, a tripod gone cold.
    "ilion_cassandras_room": {
        "title": "Cassandra's room, Ilion",
        "map": "MAP_ILION_CASSANDRAS_ROOM",
        "layout": "Ilion_CassandrasRoom",
        "render": "ilion_cassandras_room.png",
        "floor": "flags",
        "wall": "fresco",
        "grid": [
            "WWWWWWWWW",
            "WWWWWWWWW",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            "#........",
        ],
        "rugs": [("kilim", 2, 4, 3, 2)],
        "stamps": [
            ("fresco_troy", 1, 0),
            ("window", 6, 0),
            ("laurel", 8, 1),
            ("tripod", 0, 1),
            ("lampstand", 4, 1),
            ("kalathos", 3, 2),
            ("kline", 6, 2),
            ("stool", 5, 4),
            ("amphora_grey", 8, 5),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 3 (south-arrow mat)", [(4, 7)]),
            ("npc", "Cassandra, by the painted wall", (2, 3), "south"),
            ("bg", "the painting of Troy burning, half whitewashed", (1, 1), (1, 2, "north")),
            ("bg", "the painting, right half", (2, 1), (2, 2, "north")),
            ("bg", "the laurel", (8, 2), (8, 3, "north")),
        ],
    },

    # The pilgrims' guest-room, kept by the city for strangers: the basin
    # for their feet by the door, wine and bread on the long table, beds
    # along the far wall. Odysseus has the corner bed, as every year, and
    # sits by it whittling a little wooden horse.
    "ilion_guest_room": {
        "title": "The pilgrims' guest-room, Ilion",
        "map": "MAP_ILION_GUEST_ROOM",
        "layout": "Ilion_GuestRoom",
        "render": "ilion_guest_room.png",
        "floor": "boards",
        "wall": "ashlar",
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
        "rugs": [("kilim", 2, 3, 4, 2)],
        "stamps": [
            ("lampstand", 0, 1),
            ("window", 3, 0),
            ("krater", 1, 2),
            ("table", 3, 3),
            ("klismos_r", 2, 3),
            ("klismos_l", 5, 3),
            ("kline", 8, 1),
            ("kline", 10, 3),
            ("kline", 10, 6),
            ("horse_toy", 8, 4),
            ("stool", 7, 4),
            ("louter", 2, 6),
            ("knucklebones", 6, 6),
            ("amphora_grey", 0, 6),
            ("mat", 4, 8),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 4 (south-arrow mat)", [(4, 8)]),
            ("npc", "Odysseus, by his corner bed and his whittling", (8, 3), "south"),
            ("npc", "the host, by the basin", (3, 7), "west"),
            ("bg", "the wooden horse", (8, 4), (8, 5, "north")),
            ("bg", "the basin for guests' feet", (2, 7), (1, 7, "east")),
        ],
    },

    # The horse-breeder's stable. Troy "of the fine horses": four stalls
    # along the back wall under their hay racks, the trough in the yard,
    # bridles by the door. Idaios's Rapidash has the first stall; the third
    # is kept empty for the horse he wants.
    "ilion_horse_stable": {
        "title": "The horse-breeder's stable, Ilion",
        "map": "MAP_ILION_HORSE_STABLE",
        "layout": "Ilion_HorseStable",
        "render": "ilion_horse_stable.png",
        "floor": "earth",
        "wall": "ashlar",
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
            ("hay_rack", 0, 0),
            ("stall", 2, 2),
            ("hay_rack", 3, 0),
            ("stall", 5, 2),
            ("hay_rack", 6, 0),
            ("stall", 8, 2),
            ("hay_rack", 9, 0),
            ("stall", 11, 2),
            ("bridles", 12, 0),
            ("bridles", 13, 0),
            ("straw", 0, 3),
            ("straw", 4, 2),
            ("straw", 6, 3),
            ("straw", 10, 3),
            ("trough", 5, 6),
            ("wheel", 13, 3),
            ("straw", 1, 7),
            ("pithos", 0, 5),
            ("mat", 9, 8),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 5 (south-arrow mat)", [(9, 8)]),
            ("npc", "Idaios the horse-breeder", (8, 5), "west"),
            ("npc", "his Rapidash, in the first stall (until the trade)", (1, 2), "south"),
            ("npc", "a Ponyta, in the second stall", (3, 3), "south"),
            ("npc", "a Mudsdale, in the third stall (after the trade)", (7, 2), "south"),
            ("bg", "the trough", (5, 6), (5, 7, "north")),
        ],
    },

    # The mason's family. The workshop takes the west half, on beaten
    # earth: column drums, a capital half carved, a squared block with the
    # family's mark, the bench and the tools. The east half is the home:
    # the old mason's chair by the window, a bed, the brazier. His chisel is
    # somewhere in the Walls of Laomedon, and the rack has a gap where it hung.
    "ilion_masons_house": {
        "title": "The mason's house, Ilion: the workshop and the home",
        "map": "MAP_ILION_MASONS_HOUSE",
        "layout": "Ilion_MasonsHouse",
        "render": "ilion_masons_house.png",
        "floor": "flags",
        "floors": {",": "earth"},
        "wall": "ashlar",
        "grid": [
            "WWWWWWWWWWWW",
            "WWWWWWWWWWWW",
            ",,,,,,......",
            ",,,,,,......",
            ",,,,,,......",
            ",,,,,,......",
            ",,,,,,......",
            ",,,,,,......",
            "##,,,,......",
        ],
        "rugs": [("kilim", 8, 5, 3, 2)],
        "stamps": [
            ("tools", 1, 0),
            ("workbench", 2, 2),
            ("drum", 0, 2),
            ("drum", 0, 3),
            ("capital", 4, 4),
            ("block", 1, 5),
            ("block", 2, 5),
            ("drum", 4, 7),
            ("window", 7, 0),
            ("brazier", 10, 1),
            ("kline", 9, 3),
            ("stool", 7, 2),
            ("table", 7, 7),
            ("amphora_grey", 11, 7),
            ("mat", 6, 8),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 6 (south-arrow mat)", [(6, 8)]),
            ("npc", "Laodokos the old mason, by the window", (8, 2), "south"),
            ("npc", "his daughter Harmonia, at the workbench", (3, 3), "north"),
            ("bg", "the tool rack, with a gap", (1, 1), (1, 2, "north")),
            ("bg", "the half-carved capital", (4, 4), (4, 5, "north")),
        ],
    },

    # The peplos-weaver's house: the great upright loom fills the back
    # corner, Athena's saffron robe half woven on it. Dye pots by the
    # window, skeins drying on the wall, baskets of wool. Her Leavanny helps.
    "ilion_weavers_house": {
        "title": "The peplos-weaver's house, Ilion",
        "map": "MAP_ILION_WEAVERS_HOUSE",
        "layout": "Ilion_WeaversHouse",
        "render": "ilion_weavers_house.png",
        "floor": "boards",
        "wall": "ashlar",
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
        "rugs": [("kilim", 5, 4, 3, 2)],
        "stamps": [
            ("loom_big", 1, 0),
            ("skeins", 4, 0),
            ("window", 6, 0),
            ("skeins", 8, 0),
            ("kalathos", 0, 3),
            ("dye_vats", 6, 2),
            ("kalathos", 9, 2),
            ("stool", 3, 3),
            ("table", 7, 6),
            ("kalathos", 0, 6),
            ("amphora_grey", 9, 5),
            ("mat", 4, 7),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 7 (south-arrow mat)", [(4, 7)]),
            ("npc", "the weaver, at her loom", (2, 3), "south"),
            ("npc", "her Leavanny", (4, 4), "west"),
            ("bg", "the peplos on the loom", (1, 2), (1, 3, "north")),
            ("bg", "the dye pots", (6, 2), (6, 3, "north")),
            ("bg", "the dye pots, right", (7, 2), (7, 3, "north")),
        ],
    },

    # The temple of Athena on the citadel: a long cella between two rows of
    # red columns, the Palladion at the far end on its pedestal between two
    # braziers, votive shields on the walls, an offering table by the door.
    "ilion_temple_of_athena": {
        "title": "The temple of Athena, Ilion: the Palladion",
        "map": "MAP_ILION_TEMPLE_OF_ATHENA",
        "layout": "Ilion_TempleOfAthena",
        "render": "ilion_temple_of_athena.png",
        "floor": "plaster",
        "wall": "fresco",
        "grid": [
            "WWWWWWWWWWW",
            "WWWWWWWWWWW",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "...........",
            "#.........#",
            "##.......##",
        ],
        "rugs": [],
        "stamps": [
            ("shield", 1, 0),
            ("brazier", 4, 1),
            ("palladion", 5, 0),
            ("brazier", 6, 1),
            ("shield", 9, 0),
            ("column", 2, 3),
            ("column", 8, 3),
            ("column", 2, 7),
            ("column", 8, 7),
            ("temple_altar", 5, 6),
            ("mat", 5, 11),
        ],
        "spots": [
            ("warp", "door to Ilion, warp 8 (south-arrow mat)", [(5, 11)]),
            ("npc", "the keeper of the Palladion", (3, 3), "east"),
            ("npc", "Odysseus, before the Palladion (after his battle)", (6, 3), "north"),
            ("npc", "a worshipper at the offering table", (6, 7), "north"),
            ("bg", "the Palladion", (5, 2), (5, 3, "north")),
            ("bg", "the offering table", (5, 6), (5, 7, "north")),
        ],
    },
}


# ======================================================================
# The rooms' events. `python3 tools/ichor/maps/troad_rooms.py` writes each
# room's map.json from these (the header fields it keeps as registered), and
# checks every event sits on a spot the builder has proved reachable.
#   ("obj", gfx, (x, y), movement, script, flag, local_id)
#   ("bg", (x, y), facing, script)        facing: NORTH, SOUTH, EAST, WEST or ANY
#   ("coord", (x, y), var, value, script)
# Stand-in sprites (ICHOR_STUB_SPRITE) are listed in ROOMS_troad.md, "Stand-ins".
# ======================================================================

S = "Sestos_"
I = "Ilion_"
FACE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
        "east": "MOVEMENT_TYPE_FACE_RIGHT", "west": "MOVEMENT_TYPE_FACE_LEFT"}

EVENTS = {
    "sestos_asclepeion": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_HEALER", (3, 2), "south", S + "Asclepeion_EventScript_Healer", "0",
         "LOCALID_SESTOS_HEALER"),
        ("obj", "OBJ_EVENT_GFX_ICHOR_ELDER_F", (11, 2), "west", S + "Asclepeion_EventScript_OldWoman", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_SAILOR", (11, 4), "west", S + "Asclepeion_EventScript_Sailor", "0", None),
        ("bg", (6, 2), "NORTH", "Ichor_EventScript_Pithos"),
        ("bg", (7, 2), "NORTH", "Ichor_EventScript_Pithos"),
        ("bg", (9, 1), "NORTH", S + "Asclepeion_EventScript_Window"),
        ("bg", (10, 1), "NORTH", S + "Asclepeion_EventScript_Window"),
    ],
    "sestos_agora": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_MERCHANT", (2, 2), "south", S + "Agora_EventScript_Chandler", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_SAILOR", (8, 3), "north", S + "Agora_EventScript_Sailor", "0", None),
        ("bg", (8, 2), "NORTH", S + "Agora_EventScript_Shelves"),
    ],
    "sestos_heros_tower": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_PRIESTESS", (7, 3), "south", S + "HerosTower_EventScript_Hero", "0",
         "LOCALID_SESTOS_HERO"),
        ("bg", (4, 3), "NORTH", S + "HerosTower_EventScript_Lamp"),
        ("bg", (5, 3), "NORTH", S + "HerosTower_EventScript_Lamp"),
        ("bg", (3, 15), "NORTH", S + "HerosTower_EventScript_Hearth"),
        ("coord", (2, 7), "VAR_TEMP_3", 1, S + "HerosTower_EventScript_Draught"),
        ("coord", (6, 7), "VAR_TEMP_3", 1, S + "HerosTower_EventScript_Draught"),
        ("coord", (5, 11), "VAR_TEMP_3", 1, S + "HerosTower_EventScript_Draught"),
        ("coord", (8, 4), "VAR_TEMP_3", 1, S + "HerosTower_EventScript_FlameArrives"),
    ],
    "sestos_ferry_house": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_ELDER_M", (4, 2), "south", S + "FerryHouse_EventScript_Kymon", "0", None),
        ("obj", "OBJ_EVENT_GFX_SPECIES(CRAMORANT)", (6, 3), "west", S + "FerryHouse_EventScript_Cramorant",
         "FLAG_ICHOR_TRADED_KYMON_CRAMORANT", "LOCALID_SESTOS_CRAMORANT"),
        ("obj", "OBJ_EVENT_GFX_SPECIES(PELIPPER)", (6, 3), "west", S + "FerryHouse_EventScript_Pelipper",
         "FLAG_TEMP_1", "LOCALID_SESTOS_PELIPPER"),
        ("bg", (5, 1), "NORTH", S + "FerryHouse_EventScript_Wreath"),
    ],
    "sestos_net_loft": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_FISHER", (10, 4), "west", S + "NetLoft_EventScript_Fisher", "0", None),
        ("bg", (3, 4), "NORTH", S + "NetLoft_EventScript_Rack"),
    ],
    "ilion_asclepeion": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_HEALER", (7, 2), "south", I + "Asclepeion_EventScript_Healer", "0",
         "LOCALID_ILION_HEALER"),
        ("obj", "OBJ_EVENT_GFX_ICHOR_MAN", (12, 6), "east", I + "Asclepeion_EventScript_Charioteer", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_WOMAN", (12, 3), "east", I + "Asclepeion_EventScript_Pilgrim", "0", None),
        ("bg", (1, 2), "NORTH", "Ichor_EventScript_Pithos"),
        ("bg", (2, 2), "NORTH", "Ichor_EventScript_Pithos"),
    ],
    "ilion_agora": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_MERCHANT", (10, 2), "south", I + "Agora_EventScript_Thymbra", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_MAN", (2, 3), "north", I + "Agora_EventScript_HorseTrader", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_WOMAN", (13, 6), "west", I + "Agora_EventScript_ClothBuyer", "0", None),
        ("bg", (1, 1), "NORTH", I + "Agora_EventScript_Bridles"),
    ],
    "ilion_priams_palace": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_ELDER_M", (12, 2), "south", I + "PriamsPalace_EventScript_Priam", "0",
         "LOCALID_ILION_PRIAM"),
        ("obj", "OBJ_EVENT_GFX_ICHOR_HOPLITE", (5, 11), "east", I + "PriamsPalace_EventScript_GuardWest", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_HOPLITE", (10, 11), "west", I + "PriamsPalace_EventScript_GuardEast", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_MAN", (3, 6), "west", I + "PriamsPalace_EventScript_Steward", "0", None),
        ("bg", (8, 1), "NORTH", I + "PriamsPalace_EventScript_Frieze"),
        ("bg", (7, 6), "NORTH", I + "PriamsPalace_EventScript_Hearth"),
    ],
    "ilion_cassandras_room": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_YOUTH_F", (2, 3), "south", I + "CassandrasRoom_EventScript_Cassandra", "0",
         "LOCALID_ILION_CASSANDRA"),
        ("bg", (1, 1), "NORTH", I + "CassandrasRoom_EventScript_Painting"),
        ("bg", (2, 1), "NORTH", I + "CassandrasRoom_EventScript_Painting"),
        ("bg", (8, 2), "NORTH", I + "CassandrasRoom_EventScript_Laurel"),
    ],
    "ilion_guest_room": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_SAILOR", (8, 3), "south", I + "GuestRoom_EventScript_Odysseus", "FLAG_TEMP_1",
         "LOCALID_ILION_ODYSSEUS"),
        ("obj", "OBJ_EVENT_GFX_ICHOR_WOMAN", (3, 7), "west", I + "GuestRoom_EventScript_Host", "0", None),
        ("bg", (8, 4), "NORTH", I + "GuestRoom_EventScript_WoodenHorse"),
        ("bg", (2, 7), "EAST", I + "GuestRoom_EventScript_Basin"),
    ],
    "ilion_horse_stable": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_SHEPHERD", (8, 5), "west", I + "HorseStable_EventScript_Idaios", "0", None),
        ("obj", "OBJ_EVENT_GFX_SPECIES(RAPIDASH)", (1, 2), "south", I + "HorseStable_EventScript_Rapidash",
         "FLAG_ICHOR_TRADED_IDAIOS_RAPIDASH", "LOCALID_ILION_RAPIDASH"),
        ("obj", "OBJ_EVENT_GFX_SPECIES(PONYTA)", (3, 3), "south", I + "HorseStable_EventScript_Ponyta", "0", None),
        ("obj", "OBJ_EVENT_GFX_SPECIES(MUDSDALE)", (7, 2), "south", I + "HorseStable_EventScript_Mudsdale",
         "FLAG_TEMP_1", "LOCALID_ILION_MUDSDALE"),
        ("bg", (5, 6), "NORTH", I + "HorseStable_EventScript_Trough"),
    ],
    "ilion_masons_house": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_ELDER_M", (8, 2), "south", I + "MasonsHouse_EventScript_Laodokos", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_WOMAN", (3, 3), "north", I + "MasonsHouse_EventScript_Kallia", "0", None),
        ("bg", (1, 1), "NORTH", I + "MasonsHouse_EventScript_ToolRack"),
        ("bg", (4, 4), "NORTH", I + "MasonsHouse_EventScript_Capital"),
    ],
    "ilion_weavers_house": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_WOMAN", (2, 3), "south", I + "WeaversHouse_EventScript_Theano", "0", None),
        ("obj", "OBJ_EVENT_GFX_SPECIES(LEAVANNY)", (4, 4), "west", I + "WeaversHouse_EventScript_Leavanny", "0", None),
        ("bg", (1, 2), "NORTH", I + "WeaversHouse_EventScript_Peplos"),
        ("bg", (6, 2), "NORTH", I + "WeaversHouse_EventScript_DyePots"),
        ("bg", (7, 2), "NORTH", I + "WeaversHouse_EventScript_DyePots"),
    ],
    "ilion_temple_of_athena": [
        ("obj", "OBJ_EVENT_GFX_ICHOR_PRIESTESS", (3, 3), "east", I + "TempleOfAthena_EventScript_Keeper", "0", None),
        ("obj", "OBJ_EVENT_GFX_ICHOR_SAILOR", (6, 3), "north", I + "TempleOfAthena_EventScript_Odysseus",
         "FLAG_TEMP_1", "LOCALID_ILION_TEMPLE_ODYSSEUS"),
        ("obj", "OBJ_EVENT_GFX_ICHOR_WOMAN", (6, 7), "north", I + "TempleOfAthena_EventScript_Worshipper", "0", None),
        ("bg", (5, 2), "NORTH", I + "TempleOfAthena_EventScript_Palladion"),
        ("bg", (5, 6), "NORTH", I + "TempleOfAthena_EventScript_OfferingTable"),
    ],
}


def _spot_tiles(spec):
    """Where the builder proved people, readable things and triggers may go."""
    people, signs, coords = set(), set(), set()
    for s in spec["spots"]:
        if s[0] in ("npc", "counter"):
            people.add(s[2])
        elif s[0] == "bg":
            signs.add(s[2])
        elif s[0] == "coord":
            coords.add(s[2])
    return people, signs, coords


def write_maps():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[3]
    for name, spec in ROOMS.items():
        people, signs, coords = _spot_tiles(spec)
        path = root / "data/maps" / spec["layout"] / "map.json"
        data = json.loads(path.read_text())
        assert data["id"] == spec["map"], f"{name}: {path} is {data['id']}"
        objs, bgs, trig = [], [], []
        for ev in EVENTS[name]:
            if ev[0] == "obj":
                _, gfx, (x, y), facing, script, flag, local_id = ev
                assert (x, y) in people, f"{name}: no npc spot at {(x, y)} for {script}"
                o = {}
                if local_id:
                    o["local_id"] = local_id
                o.update({"graphics_id": gfx, "x": x, "y": y, "elevation": 3,
                          "movement_type": FACE[facing], "movement_range_x": 0, "movement_range_y": 0,
                          "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
                          "script": script, "flag": flag})
                objs.append(o)
            elif ev[0] == "bg":
                _, (x, y), facing, script = ev
                assert (x, y) in signs, f"{name}: no bg spot at {(x, y)} for {script}"
                bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                            "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{facing}", "script": script})
            else:
                _, (x, y), var, value, script = ev
                assert (x, y) in coords, f"{name}: no coord spot at {(x, y)} for {script}"
                trig.append({"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var,
                             "var_value": str(value), "script": script})
        town, warp = TOWN_WARP[spec["map"]]
        mat = [s for s in spec["spots"] if s[0] == "warp"][0][2][0]
        data["object_events"] = objs
        data["warp_events"] = [{"x": mat[0], "y": mat[1], "elevation": 0, "dest_map": town,
                                "dest_warp_id": str(warp)}]
        data["coord_events"] = trig
        data["bg_events"] = bgs
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"troad_rooms: {path.relative_to(root)}: {len(objs)} people, {len(bgs)} signs, "
              f"{len(trig)} triggers, warp 0 -> {town} {warp}")


if __name__ == "__main__":
    write_maps()
