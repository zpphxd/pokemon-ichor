"""gTileset_Kemet: Egypt's outdoor secondary. Every structure, by section, and the
catalog writer (design/oikoumene/TILES_kemet.md).

Batch 1 maps Naukratis, Pharos, the Delta Reeds and Memphis with it; batch 2's
Pyramid Field, the Great Pyramid's exterior, the Nile's banks, Heliopolis and
Elephantine share it (OIKOUMENE.md §7), so the desert pieces are here already and
the sheet leaves room at the end.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8), so
adding to one never renumbers another. Append new pieces at the end of their
section; new sections go after `desert`.
"""
from __future__ import annotations

import kemet_flora
import kemet_ground
import kemet_monuments
import kemet_town

NAME = "kemet"

# (start row, key, title, blurb)
SECTIONS = [
    (0, "ground", "Ground and water",
     "Black mud and its edges against the meadow and the water, the papyrus (the encounter "
     "reeds and the solid thickets with their fringes), papyrus and lotus in the water, "
     "dune grass on sand, and Naukratis's limestone quays."),
    (12, "trees", "Trees", "Date palms on grass, sand and mud, and young palms."),
    (15, "houses", "Households",
     "The house kit: roofs and their furniture, whitewashed and bare mud-brick walls, "
     "windows and doors. Every household in Naukratis and Memphis is a recipe of these "
     "parts, so each looks like whoever lives there."),
    (20, "yards", "Yards, market and marsh",
     "Granary domes, market stalls, Greek amphorae, the gnat-tower, reed fences, nets, the "
     "shaduf, boats and the seal-herders' shelter."),
    (33, "monuments", "Monuments",
     "The White Walls and their gate, the pylon of Proteus's precinct, obelisks, the "
     "sphinx, Thoth's ibis pillar, steles, and the Hellenion with its altar."),
    (49, "desert", "The desert's edge",
     "A pyramid, for the Pyramid Field (batch 2). Rows 53-63 are free for batch 2's pieces."),
]


def build():
    ground = kemet_ground.build()
    trees = kemet_flora.build()
    town = kemet_town.build()
    houses = [s for s in town if s.key.startswith("house")]
    yards = [s for s in town if not s.key.startswith("house")]
    mons = kemet_monuments.build()
    desert = [s for s in mons if s.key.startswith("pyramid")]
    mons = [s for s in mons if not s.key.startswith("pyramid")]
    parts = {"ground": ground, "trees": trees, "houses": houses, "yards": yards,
             "monuments": mons, "desert": desert}
    for key, ss in parts.items():
        for s in ss:
            s.section = key
    return [(row, parts[key]) for row, key, _, _ in SECTIONS]


def validate(structs):
    import kemet_lib
    return kemet_lib.validate(structs)


def write_catalog(used, structs):
    import kemet_catalog
    kemet_catalog.main(used, structs, SECTIONS)
