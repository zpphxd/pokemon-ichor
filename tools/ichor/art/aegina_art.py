"""Every structure in gTileset_Aegina, in metatile order.

Ids run from 0x200 in this order, so new structures go at the end to keep the
existing ids. aegina_build.py packs, compiles and catalogs them.

  aegina_harbor  Akti's harbor copies, the round basin's corners, the mole heads
  aegina_town    the inn, the mint, Aiakides's house, the gate, the turtle mosaic
  aegina_ground  dry grass, golden tall grass, ant hills
  aegina_land    Kolona and its ruins, pistachio, pine, scrub, and the detour's
                 Temple of Aphaia and Zeus's altar
"""
from __future__ import annotations

# Structures drawn for the detour maps (the Aphaia Road, the Temple of Aphaia,
# Mount Oros). The town plants some of them too (DETOUR_SHARED); the rest only
# the detour places. TILES_aegina.md lists them.
DETOUR = ("pistachio", "pine", "scrub", "dry_tall_grass", "temple_aphaia", "altar_zeus")
DETOUR_SHARED = ("pistachio", "pine", "scrub")


def build():
    import aegina_ground
    import aegina_harbor
    import aegina_land
    import aegina_town
    # new structures go at the end, so existing ids keep their places
    return (aegina_harbor.build() + aegina_town.build() + aegina_ground.build()
            + aegina_land.build() + aegina_harbor.later())
