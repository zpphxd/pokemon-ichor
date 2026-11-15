"""gTileset_Troas: the Troad. Every structure, by section, and the catalog writer.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8), so
adding to one section never renumbers another. Append new pieces at the end of
their section. Batch 2's Troad maps (the Skamander Plain, the Ida Road, Gargaros
Peak) add their pieces in the spare rows after each section.
"""
from __future__ import annotations

import troas_land
import troas_sea
import troas_town
import troas_walls
from troas_lib import GROUPS, validate  # noqa: F401  (emporion_build reads both)

NAME = "troas"

# (start row, key, title, blurb)
SECTIONS = [
    (0, "land", "The plain",
     "Wheat (the Troad's tall grass) and the Skamander's banks in soft-edged shapes, reeds, a "
     "heroes' burial mound, Ida's black pines, the valonia oak, Protesilaos's withered elm, and "
     "flowers and stones for the grass."),
    (12, "sea", "The Hellespont",
     "The eastward current, Helle's rock with its gilded ram, and a timber landing stage."),
    (16, "harbor", "Sestos's harbor",
     "Akti's quay, the Euploia and her gangplank's foot, and a bollard, drawn by Akti's own "
     "painters so the ship is the same in both ports."),
    (24, "walls", "Ilion's walls and Hero's tower",
     "The great sloping wall west-east and north-south with its corners, a bastion tower, the "
     "open ramp gate, the Skaian Gate's outer face (its doors shut: batch 2's hall), and Hero's "
     "tower with its lamp."),
    (40, "town", "Houses, the palace and the temple",
     "The Trojan house kit in ochre and in whitewash, Priam's megaron, the temple of Athena, a "
     "great herm, yard things (hay, trough, the mason's blocks and drums, dye vats, a chariot, "
     "wool drying) and the twin springs."),
]


def build():
    parts = {"land": troas_land.build(), "sea": troas_sea.build_sea(),
             "harbor": troas_sea.build_harbor(), "walls": troas_walls.build(),
             "town": troas_town.build()}
    order = {
        "walls": ["wall", "tower", "wall_ns", "gateway", "skaian_gate", "heros_tower"],
        "town": ["house_kit", "springs", "house_kit_white", "great_herm", "priams_palace",
                 "temple_athena", "yard"],
        "harbor": ["quay", "quay_gangplank", "bollard_line", "trireme"],
    }
    for key, ss in parts.items():
        if key in order:
            by = {s.key: s for s in ss}
            ss[:] = [by[k] for k in order[key]]
        for s in ss:
            s.section = key
    return [(row, parts[key]) for row, key, _, _ in SECTIONS]


def write_catalog(used, structs):
    import troas_catalog
    troas_catalog.main(used, structs, SECTIONS)
