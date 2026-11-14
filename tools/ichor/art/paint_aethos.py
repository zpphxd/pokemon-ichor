#!/usr/bin/env python3
"""Build the aethos primary tileset, Aethos's outdoor world, from scratch.

Every metatile keeps General's id, behavior and layer usage, so any layout
built on General means the same thing on aethos. The art comes from the
painters below, run in order; each later pass redraws whole metatiles over the
ones before it:

  aethos_terrain    every metatile, rebuilt from General's material map
  aethos_ground     dry grass, wild tall grass, anemones, paths, soil, ash
  aethos_water      the Aegean, surf, shallows, waterfalls (and the anims)
  aethos_trees      olive trees, cypress spires, stone pines
  aethos_coast      beaches, sea rocks, rocky shores
  aethos_props      ledges, dry-stone walls, steles, boulders, steps
  aethos_buildings  the Asclepeion, the Agora, farmhouse, palaestra

Then it writes data/tilesets/primary/aethos/porytiles_src and compiles it
with Porytiles (which also regenerates the anim code in
include/porytiles_generated/tilesets/aethos/).

Usage: /usr/bin/python3 tools/ichor/art/paint_aethos.py [--no-compile]
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aethos_lib import (Base, Sheet, scan_anim_uses, place_anim_keys,  # noqa: E402
                        split_tiles, write, compile_tileset)

PAINTERS = ["aethos_terrain", "aethos_ground", "aethos_trees", "aethos_coast",
            "aethos_props", "aethos_buildings"]


def build():
    base = Base()
    sheet = Sheet()
    for name in PAINTERS:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name == name:
                continue
            raise
        mod.paint(sheet, base)

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
    return sheet, frames


def main():
    sheet, frames = build()
    write(sheet, frames)
    print("wrote data/tilesets/primary/aethos/porytiles_src")
    if "--no-compile" not in sys.argv:
        compile_tileset()
        print("compiled gTileset_Aethos")


if __name__ == "__main__":
    main()
