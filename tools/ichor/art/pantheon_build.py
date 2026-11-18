#!/usr/bin/env python3
"""Draw, compile and catalog the four Pantheon seats' secondaries
(tools/ichor/art/pantheon_lib.py): gTileset_SeatAres, SeatPoseidon, SeatAthena
and SeatHera. Writes each one's porytiles_src and porytiles_bin, its
catalog.json (tools/ichor/maps/olympus.py and league_seats.py read it) and its
numbered sheet in design/maps/img/.

Usage: /usr/bin/python3 tools/ichor/art/pantheon_build.py [--only ares,...] [--no-compile] [--preview DIR]
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pantheon_lib import ROOT  # noqa: E402

SEATS = ("ares", "poseidon", "athena", "hera")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=",".join(SEATS))
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview")
    args = ap.parse_args()
    for key in args.only.split(","):
        mod = importlib.import_module(f"pantheon_{key}")
        pv = str(Path(args.preview) / f"{key}_preview.png") if args.preview else None
        if pv:
            Path(args.preview).mkdir(parents=True, exist_ok=True)
        mod.SEAT.build(compile_=not args.no_compile, preview_out=pv,
                       sheet_out=ROOT / f"design/maps/img/seat_{key}_sheet.png")


if __name__ == "__main__":
    main()
