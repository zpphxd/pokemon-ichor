#!/usr/bin/env python3
"""Build the aethos primary tileset, Aethos's outdoor world, from scratch.

Every metatile keeps General's id, behavior and layer usage, so any layout
built on General means the same thing on aethos. The art comes from the
painters below, run in order; each later pass redraws whole metatiles over the
ones before it:

  aethos_terrain    every metatile, rebuilt from General's material map
                    (beaches, sea stacks, cliffs and ponds come from here)
  aethos_ground     dry grass, wild tall grass, anemones, paths, soil, ash
  aethos_trees      olive trees, cypress spires, stone pines
  aethos_props      ledges, dry-stone walls, steles, boulders, steps
  aethos_buildings  the Asclepeion, the Agora, farmhouse, palaestra
  aethos_water      the Aegean and every animation (water, surf, falls)

Then it writes data/tilesets/primary/aethos/porytiles_src and builds the
Porymap assets with aethos_bin: locked palettes, the tiles Petalburg uses
pinned at General's indices, animations at General's offsets, and a check
that a checksum-verified recompile changes nothing. Porytiles also
regenerates include/porytiles_generated/tilesets/aethos/.

Helpers: aethos_palcheck.py explains palette-packing trouble, and
aethos_review.py renders Hoenn towns on aethos (see design/phase1/TILES_aethos.md).

Usage: /usr/bin/python3 tools/ichor/art/paint_aethos.py [--no-compile]
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aethos_lib import (Base, Sheet, scan_anim_uses, place_anim_keys,  # noqa: E402
                        split_tiles, write)
import aethos_bin  # noqa: E402

PAINTERS = ["aethos_terrain", "aethos_ground", "aethos_trees", "aethos_props",
            "aethos_buildings"]


def build():
    base = Base()
    sheet = Sheet()
    for name in PAINTERS:
        importlib.import_module(name).paint(sheet, base)

    import aethos_ground
    import aethos_water
    frames = {
        "flower": aethos_ground.flower_frames(),
        "water": aethos_water.water_frames(),
        "sand_water_edge": aethos_water.sand_water_edge_frames(),
        "land_water_edge": aethos_water.land_water_edge_frames(),
        "waterfall": aethos_water.waterfall_frames(),
    }
    keys = {name: split_tiles(f[0]) for name, f in frames.items()}
    place_anim_keys(sheet, scan_anim_uses(base), keys)
    return sheet, frames, base


def main():
    sheet, frames, base = build()
    bad = aethos_bin.check_fit(sheet, frames)
    if bad:
        raise SystemExit("aethos: tiles that fit no palette:\n  " + "\n  ".join(bad[:60]))
    write(sheet, frames)
    print("wrote data/tilesets/primary/aethos/porytiles_src")
    if "--no-compile" not in sys.argv:
        pinned = aethos_bin.build(sheet, base, frames)
        print(f"compiled gTileset_Aethos: {len(pinned)} tiles pinned for "
              f"{', '.join(aethos_bin.COMPAT)}; a verified recompile changes nothing")


if __name__ == "__main__":
    main()
