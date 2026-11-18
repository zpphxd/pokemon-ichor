#!/usr/bin/env python3
"""Nemea's two rooms: the palaestra of the Nemean Games and Molorchos's cottage.

Every house is a home and every interior is unique (design/MAP_DESIGN.md §2).
Both rooms are laid out from gTileset_Domos by ergasteria_build.py's machinery,
after every other domos room, so the older rooms' metatile ids don't move.
tools/ichor/maps/nemea.py builds the town and writes these rooms' events and
scripts; run it (it calls this) rather than this file.

  /usr/bin/python3 tools/ichor/maps/nemea_rooms.py   # rebuild domos and the two rooms only
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOMS_DOC = ROOT / "design/maps/Nemea_rooms.md"

ROOMS = {
    # ------------------------------------------------------------------
    # The palaestra. The Games' wrestling hall: a sand pit (the skamma) in a
    # stone court between four posts, the victors' names painted on the
    # plaster, the board of this year's entrants, Herakles's altar on the back
    # wall (he founded the Games here, after the lion), the water clock that
    # times the boxers, oil for the athletes' skin, a washbasin, benches, and
    # the runners' sandals on their pegs.
    "nemea_palaestra": {
        "set": "domos",
        "title": "The palaestra, Nemea",
        "map": "MAP_NEMEA_PALAESTRA",
        "layout": "Nemea_Palaestra",
        "render": "nemea_palaestra.png",
        "floor": "terracotta",
        "floors": {",": "claydust"},
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWW",
            "................",
            "................",
            ".....,,,,,,.....",
            ".....,,,,,,.....",
            ".....,,,,,,.....",
            ".....,,,,,,.....",
            "................",
            "................",
            "................",
        ],
        "rugs": [],
        "stamps": [
            ("sandals_pegs", 0, 1),
            ("road_map", 2, 0),
            ("window", 4, 0),
            ("soot", 6, 0),
            ("hearth", 6, 2),
            ("window", 9, 0),
            ("amphora_rack", 10, 0),
            ("window", 13, 0),
            ("pallet", 0, 2),
            ("krater", 9, 2),
            ("pallet", 14, 2),
            ("column", 3, 3),
            ("column", 12, 3),
            ("bench", 1, 6),
            ("bench", 13, 6),
            ("column", 3, 7),
            ("column", 12, 7),
            ("water_jar", 9, 8),
            ("louterion", 1, 8),
            ("lampstand", 10, 8),
            ("sack", 13, 9),
            ("mat", 7, 10),
        ],
        "spots": [
            ("warp", "door to Nemea (south-arrow mat)", [(7, 10), (8, 10)]),
            ("npc", "Kleitos the trainer, by the hearth", (8, 3), "south"),
            ("npc", "Tisandros the wrestler, in the sand pit", (6, 5), "east"),
            ("npc", "Chionis the runner, by the benches", (11, 9), "west"),
            ("bg", "the course scratched on the plaster", (2, 1), (2, 2, "north")),
            ("bg", "the oil jars", (10, 1), (10, 2, "north")),
            ("bg", "the washbasin", (1, 9), (2, 9, "west")),
        ],
    },
    # ------------------------------------------------------------------
    # Molorchos's cottage. A poor laborer's one room, as in the myth where
    # he put up Herakles before the lion hunt: the hearth and its soot, a few
    # pots, herbs from the beam, one shelf of honey jars (all he has worth
    # offering), a pallet, a wool basket, the grain jar and the water jar.
    "nemea_molorchos": {
        "set": "domos",
        "title": "Molorchos's cottage, Nemea",
        "map": "MAP_NEMEA_MOLORCHOS_HOUSE",
        "layout": "Nemea_MolorchosHouse",
        "render": "nemea_molorchos.png",
        "floor": "terracotta",
        "wall": "tavern",
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
        "rugs": [],
        "stamps": [
            ("soot", 0, 0),
            ("hearth", 0, 2),
            ("pots", 2, 2),
            ("herbs", 3, 0),
            ("window", 7, 0),
            ("pithos", 9, 1),
            ("amphora", 10, 1),
            ("mortar", 7, 5),
            ("table", 3, 4),
            ("stool", 5, 4),
            ("trestle_grain", 0, 5),
            ("sack", 9, 5),
            ("mat", 5, 7),
        ],
        "spots": [
            ("warp", "door to Nemea (south-arrow mat)", [(5, 7), (6, 7)]),
            ("npc", "Molorchos, at his table", (5, 3), "south"),
            ("bg", "the honey jar", (10, 2), (10, 3, "north")),
            ("bg", "the hearth", (1, 3), (1, 4, "north")),
        ],
    },
}


def main():
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import ergasteria_build as EB
    import limen_build
    EB.build(limen_build.DOMOS, EB.parse_args())


if __name__ == "__main__":
    main()
