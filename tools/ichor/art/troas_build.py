#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Troas, the Troad's outdoor secondary.

It runs emporion_build.py's pipeline (draw, check palette groups, merge
near-duplicate tiles, pack the 8-wide sheet section by section, compile with
Porytiles against an empty stand-in primary, point every grass, sand and sea
cell's bottom layer at aethos's own ground metatile, verify the 504-tile limit),
with troas_art.py's structures and palette plan. Images go to
design/oikoumene/img/troas_sheet.png and troas_pieces.png, and the catalog to
design/oikoumene/TILES_troas.md.

Usage: /usr/bin/python3 tools/ichor/art/troas_build.py [--no-compile] [--preview out.png]
Rebuild whenever aethos changes (the borrowed ground follows it).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_build as EB  # noqa: E402

EB.TILESETS["troas"] = ("troas_art", "gTileset_Troas")
EB.IMG = EB.ROOT / "design/oikoumene/img"

# Tiles within 3 px of another are drawn as that one (emporion uses 2). The
# Troad's courses of ashlar and its wheat differ by a pixel or three from cell to
# cell; merging them leaves room in the 504 for batch 2's Troad maps.
_merge = EB.merge_near_duplicates
EB.merge_near_duplicates = lambda structs, limit=3: _merge(structs, limit)


def main():
    sys.argv = [sys.argv[0], "troas"] + sys.argv[1:]
    EB.main()


if __name__ == "__main__":
    main()
