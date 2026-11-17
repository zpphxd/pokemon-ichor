#!/usr/bin/env python3
"""Draw, compile and catalog Delphoi's tilesets with emporion_build.py's pipeline.

  gTileset_Delphoi       Route 28 and Delphoi, on aethos (delphoi_art.py)
  gTileset_TempleApollo  the Temple of Apollo and the Omphalos stair, on oikos
                         (temple_apollo_art.py)

The pipeline is emporion_build's (draw, merge near-duplicate tiles, pack the
sheet by sections, compile with Porytiles against a stand-in primary, borrow
aethos's ground, verify the 504-tile limit, write the catalog). Only the
images go to design/phase4/img/ instead.

Usage: /usr/bin/python3 tools/ichor/art/delphoi_build.py [delphoi|temple_apollo]
       [--no-compile] [--preview out.png]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import emporion_build as EB  # noqa: E402

EB.TILESETS["delphoi"] = ("delphoi_art", "gTileset_Delphoi")
EB.TILESETS["parnassos"] = ("parnassos_art", "gTileset_Parnassos")
EB.TILESETS["temple_apollo"] = ("temple_apollo_art", "gTileset_TempleApollo")
EB.IMG = EB.ROOT / "design/phase4/img"

_init = EB.Spec.__init__


def _spec_init(self, name="delphoi"):
    _init(self, name)
    self.temple = name in ("temple_hermes", "temple_apollo")
    self.sheet = EB.IMG / f"{self.dir}_sheet.png"
    self.pieces = EB.IMG / f"{self.dir}_pieces.png"


EB.Spec.__init__ = _spec_init

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.argv.insert(1, "delphoi")
    # Delphoi's set is full: tiles within 3 px of another are stored once
    # (at 3 px the merge is invisible on these hand-shaded pieces).
    if sys.argv[1] == "delphoi":
        EB.NEAR_DUPLICATE_PX = 3
        _merge = EB.merge_near_duplicates
        EB.merge_near_duplicates = lambda structs, limit=3: _merge(structs, 3)
    EB.main()
