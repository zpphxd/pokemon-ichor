"""gTileset_Pontos: every structure, by section.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8), so
adding to one never renumbers another. Rows 50-63 are left for batch 2: the
Phasis, the Field of Ares's furrows, the Grove of Ares's oak, Leuke's bone-white
rock and seabirds, and the Caucasus caves' mouths.
"""
from __future__ import annotations

import pontos_coast
import pontos_props
import pontos_town

NAME = "pontos"

SECTIONS = [
    (0, "sea", "The Pontic sea",
     "aethos's animated water, re-pointed at palette 12 so it is the Black Sea's dark green: "
     "open sea, rough water, the beach edges and rocks in the sea. No tiles of their own."),
    (3, "coast", "The coast: cliffs, the Kyaneai and quays",
     "Autotiles: one piece per 3x3 neighbourhood of land and sea the maps use "
     "(pontos_shapes.json). chalk = the white cliffs, kyanean = the Clashing Rocks, quay = "
     "dressed stone. Map builders place them through build/pontos/coast_index.json."),
    (22, "rocks", "Rocks and landmarks",
     "Chalk and kyanean crags, the lighthouse, the shrine of Zeus of the Fair Wind, the "
     "Acherusian cave, whirlpools, and the dove's feathers in the Clashing Rocks."),
    (25, "isle", "The Isle of Ares and the woods",
     "The Amazons' black stone, the birds' feathers in the turf, the shield post, the roost, "
     "a dead perch; Pontic oaks, hazel, the Phasis's reeds."),
    (29, "salmydessos", "Salmydessos",
     "The thatch-roof kit (shared with Aia), wattle-and-daub walls, the pier, a fishing boat, "
     "nets, the wreck and its boundary stones, Phineus's table, the dovecote and cages, "
     "sea-marks."),
    (35, "aia", "Aia",
     "Colchian log walls (Vitruvius's towers), Aietes's bronze palace, Hephaestus's four "
     "fountains and their vines, the ram post, the Euploia at her mooring."),
]
BATCH2_ROW = 50


def build():
    coast, index = pontos_coast.build()
    parts = {
        "sea": pontos_props.build_sea(),
        "coast": coast,
        "rocks": pontos_props.build_rocks() + pontos_props.build_shore(),
        "isle": pontos_props.build_isle() + pontos_props.build_flora(),
        "salmydessos": pontos_town.build_salmydessos(),
        "aia": pontos_town.build_aia(),
    }
    for key, ss in parts.items():
        for s in ss:
            s.section = key
    build.index = index
    return [(row, parts[key]) for row, key, _, _ in SECTIONS]
