#!/usr/bin/env python3
"""The Gulf's two interiors: Kirrha's pilgrims' hostel and Aigion's Homarion.

Every house is a home and every interior is unique (design/MAP_DESIGN.md
section 2). Both rooms are composed from pieces gTileset_Domos already has
(no new art), in emporion_rooms.py's room format. Who lives here and what
happens is in design/maps/Kirrha.md and design/maps/Aigion.md; the events and
scripts are written by tools/ichor/maps/gulf.py, which owns the Gulf maps.

  /usr/bin/python3 tools/ichor/maps/gulf.py --rooms   # builds domos and these rooms

Each room's exit is its door mat, warp 0 and 1, back to its door in the town
(gulf.py: the hostel's door is Kirrha's warp 0, the Homarion's Aigion's warp 0).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOMS_DOC = ROOT / "design/maps/Gulf_rooms.md"

ROOMS = {
    # ------------------------------------------------------------------
    # The pilgrims' hostel, Kirrha. Everyone bound for Delphoi sleeps here
    # first: the pallets in rows down the west end, sandals on pegs over
    # them, the road up the mountain scratched on the plaster by those who
    # came back down. Xenarete keeps the kitchen at the east end; the long
    # common hearth burns in the middle, where Hesychia, an old bee-priestess
    # of Delphoi, sits closest to the fire. Apollo's little altar is by the
    # window that looks up the mountain.
    "kirrha_hostel": {
        "set": "domos",
        "title": "The pilgrims' hostel, Kirrha",
        "map": "MAP_KIRRHA_PILGRIMS_HOSTEL",
        "layout": "Kirrha_PilgrimsHostel",
        "render": "kirrha_hostel.png",
        "floor": "boards",
        "floors": {",": "flags"},
        "wall": "stone",
        "grid": [
            "WWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWW",
            "........,,,,,,",
            "........,,,,,,",
            "........,,,,,,",
            "........,,,,,,",
            "........,,,,,,",
            "........,,,,,,",
            "........,,,,,,",
        ],
        "rugs": [],
        "stamps": [
            # the west end: pallets in two rows, sandals on pegs, the road on the wall
            ("sandals_pegs", 0, 1),
            ("road_map", 3, 0),
            ("pallet", 0, 2),
            ("pallet", 2, 2),
            ("pallet", 0, 5),
            ("pallet", 2, 5),
            ("lampstand", 5, 1),
            # Apollo's altar under the window that looks up the mountain
            ("window", 6, 0),
            ("altar", 7, 1),
            # the common hearth in the middle
            ("hearth_floor", 5, 4),
            ("bench", 4, 7),
            # the kitchen
            ("soot", 10, 0),
            ("hearth", 10, 2),
            ("pots", 12, 2),
            ("herbs", 9, 0),
            ("pithos", 13, 1),
            ("table", 11, 5),
            ("stool", 13, 5),
            ("water_jar", 13, 7),
            ("amphora_plain", 9, 7),
            ("mat", 7, 8),
        ],
        "spots": [
            ("warp", "door to Kirrha (south-arrow mat)", [(7, 8), (8, 8)]),
            ("npc", "Xenarete, the hostel keeper, in her kitchen", (11, 4), "south"),
            ("npc", "Hesychia, the old melissa, by the hearth", (4, 5), "east"),
            ("npc", "Lykinos, a pilgrim waiting for the road", (1, 4), "south"),
            ("bg", "the road up the mountain, on the wall", (3, 1), (3, 2, "north")),
            ("bg", "Apollo's altar", (7, 2), (7, 3, "north")),
            ("bg", "the common hearth", (5, 5), (5, 6, "north")),
            ("bg", "the kitchen hearth", (10, 3), (10, 4, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The Homarion, Aigion: the hall of Zeus Homagyrios, "who gathers men",
    # where Agamemnon called the Achaean kings before Troy. A long hall of
    # posts, the god's altar at the back between two niches, a pebble floor
    # of a host greeting a traveller (Zeus keeps the guest-right too), the
    # oath-tablets of the old league in a bronze-bound chest, a krater for
    # the oath-wine. The bronze doors to the adyton behind the altar have
    # been barred since anyone can remember.
    "aigion_homarion": {
        "set": "domos",
        "title": "The Homarion, Aigion",
        "map": "MAP_AIGION_HOMARION",
        "layout": "Aigion_Homarion",
        "render": "aigion_homarion.png",
        "floor": "flags",
        "floors": {",": "terracotta"},
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWW",
            "...............",
            "...............",
            "....,,,,,,,....",
            "....,,,,,,,....",
            "....,,,,,,,....",
            "....,,,,,,,....",
            "...............",
            "...............",
        ],
        "rugs": [("blue", 6, 2, 3, 2)],
        "stamps": [
            # the back wall: the barred bronze doors of the adyton, the altar
            # between its two niches, the lamps
            ("shed_doors", 1, 0),
            ("niche", 5, 0),
            ("altar", 7, 1),
            ("niche_horse", 9, 0),
            ("lampstand", 6, 1),
            ("lampstand", 8, 1),
            ("window", 12, 0),
            # the posts down the hall
            ("column", 3, 2),
            ("column", 11, 2),
            ("column", 3, 6),
            ("column", 11, 6),
            # the guest-right in the floor
            ("host_mosaic", 5, 5),
            # the oath: tablets in the chest, the wine in the krater
            ("chest", 12, 3),
            ("krater", 1, 3),
            ("amphora", 1, 6),
            ("bench", 12, 8),
            ("louterion", 5, 8),
            ("mat", 7, 9),
        ],
        "spots": [
            ("warp", "door to Aigion (south-arrow mat)", [(7, 9), (8, 9)]),
            ("npc", "Agesandros, the priest, beside the altar", (9, 3), "south"),
            ("npc", "Kleobis, an old oarsman of the league", (13, 6), "west"),
            ("bg", "the altar of Zeus Homagyrios", (7, 2), (7, 3, "north")),
            ("bg", "the barred bronze doors", (2, 1), (2, 2, "north")),
            ("bg", "the oath-tablets", (12, 4), (12, 5, "north")),
            ("bg", "the guest-right mosaic", (6, 5), (6, 4, "south")),
        ],
    },
}
