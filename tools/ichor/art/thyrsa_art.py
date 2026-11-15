"""gTileset_Thyrsa: Thyrsa City. Every structure, by section.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8), so
adding to one section never renumbers another. Append new pieces at the end of
their section. thyrsa_build.py draws, compiles and catalogs it.
"""
from __future__ import annotations

import thyrsa_civic
import thyrsa_polish
import thyrsa_town
import thyrsa_vines
import thyrsa_walls

NAME = "thyrsa"

# (start row, key, title, blurb)
SECTIONS = [
    (0, "streets", "Streets",
     "The grey-buff street flags and their shaded variants, kerbs against grass, broad "
     "steps, the Cyclopean terrace walls that hold the city's levels, the Kadmeia's parapet, "
     "and steles for signs."),
    (7, "walls", "The city walls and gates",
     "The Cyclopean wall in one masonry texture: the north and south walls' battlement and "
     "face, ivy curtains, the north-south strips, the Elektran Gate, the side gates (the "
     "Neistan and the Proitid), the bricked-up gates, and the theater's high gate."),
    (27, "houses", "Houses: the kit",
     "One- and two-storey houses built from parts: a terracotta roof (two rows), an upper "
     "storey and a ground storey, each a strip of one-cell parts, in ochre with wine-purple "
     "paint or limewashed with vine-green paint. Masks hang over the doors for the festival. "
     "Also Chthonia's house of rough stones, and a yard wall with a fig."),
    (38, "civic", "The Agora, the temple and the sacred places",
     "The Agora and the market stalls, the festival garlands, the Temple of Dionysus, the "
     "Asclepeion and the fountain house of Dirke, and Semele's chamber; then the polish "
     "pass's pieces for the square and the yards: the god's fountain, the mask stall, the "
     "festival's litter, a washing line and a stone bench."),
    (56, "vines", "The vineyards",
     "Vine rows (the city's tall grass), the old trellises, the wine press, the marked ivy, "
     "and wine jars."),
]


def build():
    parts = {
        "streets": thyrsa_walls.build_streets(),
        "walls": thyrsa_walls.build_walls(),
        "houses": thyrsa_town.build_houses(),
        "civic": thyrsa_town.build_market() + thyrsa_civic.build() + thyrsa_polish.build(),
        "vines": thyrsa_vines.build(),
    }
    for key, ss in parts.items():
        for s in ss:
            s.section = key
    return [(row, parts[key]) for row, key, _, _ in SECTIONS]
