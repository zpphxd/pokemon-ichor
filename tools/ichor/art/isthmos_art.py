"""gTileset_Isthmos: Emporion's harbor and the Isthmus. Every structure, by
section, and the catalog writer.

The sister of gTileset_Emporion, for the maps outside the city walls: the port
of Lechaion (quays, warehouses and the hiring hall, ship sheds, the crane, the
harbor's goods, a merchant ship), the Diolkos with the ship on her cradle, the
shipwright's yard, and the Isthmian sanctuary of Poseidon. It carries the city's
paving, kerbs, steps and the whole house kit (drawn by the same code, so pixel
for pixel the same), so a harbor district has homes and streets of its own.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8).
"""
from __future__ import annotations

import emporion_agora
import emporion_city
import emporion_land
import emporion_port

NAME = "isthmos"

SECTIONS = [
    (0, "streets", "Streets",
     "Emporion's marble paving, kerbs and broad steps, for the harbor district's streets."),
    (5, "houses", "Houses: the kit",
     "Emporion's house kit, the same parts as gTileset_Emporion's, for the harbor "
     "district's homes: see TILES_emporion.md for how the parts combine."),
    (14, "port", "The port of Lechaion",
     "Quays, bollards, warehouses and the hiring hall, ship sheds, the crane, the harbor's "
     "goods, and two market stalls for the fish quay."),
    (27, "diolkos", "The Diolkos and the ships",
     "The merchant ship at her mooring, the Diolkos track, the same ship hauled on its "
     "wheeled cradle, the capstan, and the shipwright's yard."),
    (40, "isthmia", "The Isthmian sanctuary of Poseidon",
     "The stadium's starting line, a victor's pine wreath, and Poseidon's altar. The "
     "sanctuary's pines are aethos's stone pines."),
]


def build():
    streets, houses = emporion_city.build(yard=False, terrace=False, plaza=False)
    port = emporion_port.build_port() + [emporion_agora.stall("fish"), emporion_agora.stall("wine")]
    parts = {"streets": streets, "houses": houses, "port": port,
             "diolkos": emporion_port.build_diolkos() + emporion_land.build_shipwright(),
             "isthmia": emporion_land.build_isthmia()}
    for key, ss in parts.items():
        for s in ss:
            s.section = key
    return [(row, parts[key]) for row, key, _, _ in SECTIONS]


def write_catalog(used, structs):
    import emporion_catalog
    emporion_catalog.main(NAME, used, SECTIONS)
