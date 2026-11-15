#!/usr/bin/env python3
"""Static checks over the slice's maps: what the playthrough can't see by walking.

The checks themselves (REACH, WARP, EDGE, MIXED, ONSOLID) live in
tools/ichor/mapdata.py, shared with tools/ichor/map_audit.py, which runs them
over any set of maps along with the route standard (MAP_DESIGN.md §8).

  tools/ichor/tests/slice_map_audit.py            (prints findings; exit 0)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mapdata import Repo, structural_checks  # noqa: E402

# Every slice map in map_groups.json, so a new house is audited without editing this list.
SLICE_PREFIXES = ("ElaiaVillage", "KallisteRoute1", "AktiTown")


def main():
    repo = Repo()
    findings = 0
    for name in [n for n in repo.names if n.startswith(SLICE_PREFIXES)]:
        for kind, msg in structural_checks(repo.map(name)):
            findings += 1
            print(f"{kind:8s} {name}: {msg}")
    print(f"{findings} finding(s)")


if __name__ == "__main__":
    main()
