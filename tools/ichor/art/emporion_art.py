"""gTileset_Emporion: the city. Every structure, by section, and the catalog writer.

Emporion's harbor, the Diolkos and the Isthmian sanctuary are in a sister
tileset, gTileset_Isthmos (isthmos_art.py): the whole Isthmus did not fit one
secondary's 504 tiles. Both draw their shared parts (paving, kerbs, steps, the
house kit) with the same code, so the two meet pixel for pixel.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8), so
adding to one section never renumbers another. Append new pieces at the end of
their section.
"""
from __future__ import annotations

import emporion_agora
import emporion_city
import emporion_land
import emporion_monuments

NAME = "emporion"

# (start row, key, title, blurb)
SECTIONS = [
    (0, "streets", "Streets",
     "Marble paving and its variants, kerbs against grass, broad steps, the poros yard "
     "paving of the workshops, and the terrace walls that hold the city's levels, with the "
     "cistern mouth under the Agora steps."),
    (7, "houses", "Houses: the kit",
     "Two-storey merchant houses built from parts: a terracotta roof (two rows), an upper "
     "storey and a ground storey, each a strip of one-cell parts. Every wall part comes in "
     "ochre with Aegean-blue paint and in rose with sea-green paint. The recipes after the "
     "kit show eight houses made from it."),
    (16, "agora", "The Agora",
     "The stoa and its bays (the Agora shop among them), the market's stalls, the notice "
     "board with the owl seal, and Pegasus on his column."),
    (34, "monuments", "Monuments",
     "The Temple of Hermes, Emporion's Asclepeion, the Peirene fountain house, the "
     "Hephaisteion and its forge, the great herm, and the street furniture."),
    (53, "land", "Acrocorinth and the workshops",
     "The crag and its walls over the city; the bronze-smith's, the potter's and the "
     "perfumer's yards."),
]


def build():
    streets, houses = emporion_city.build(yard=True)
    parts = {"streets": streets, "houses": houses, "agora": emporion_agora.build(),
             "monuments": emporion_monuments.build(), "land": emporion_land.build_city()}
    for key, ss in parts.items():
        for s in ss:
            s.section = key
    return [(row, parts[key]) for row, key, _, _ in SECTIONS]


def write_catalog(used, structs):
    import emporion_catalog
    emporion_catalog.main(NAME, used, SECTIONS)
