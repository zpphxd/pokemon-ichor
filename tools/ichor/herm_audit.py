#!/usr/bin/env python3
"""Every town gets a travel herm at its entrance (design/MAP_DESIGN.md §7, SYSTEMS.md §4).

  /usr/bin/python3 tools/ichor/herm_audit.py          exit 1 on any FAIL
  /usr/bin/python3 tools/ichor/herm_audit.py -v       also print each town's distance

Checks, from the data the game builds:

  * Every heal location with a healer (a "respawn_map" in
    src/data/heal_locations.json) belongs to a row of src/data/ichor_town_herms.h.
    A new town with an Asclepeion or healer fails until it has a travel herm.
  * Every row's map stands one great herm (OBJ_EVENT_GFX_ICHOR_GREAT_HERM, running
    EventScript_IchorTownHerm) and its plaque (OBJ_EVENT_GFX_ICHOR_HERM_PLAQUE).
    tools/ichor/maps/town_herms.py places both.
  * The row's landing tile is beside the herm, open, and the player can walk
    there from the town's entrances.
  * The herm is near an entrance: the landing tile is at most MAX_STEPS steps
    from where the player arrives (a connected edge, a door from another map, or
    a scripted arrival such as a ferry's warp).

smoke_test.sh runs it. Python 3 stdlib only.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import REPO, Repo, Walker, bfs, entries  # noqa: E402

MAX_STEPS = 16  # a screen's width: the herm is in view as the town opens up
HERM_GFX = "OBJ_EVENT_GFX_ICHOR_GREAT_HERM"
PLAQUE_GFX = "OBJ_EVENT_GFX_ICHOR_HERM_PLAQUE"
ROW = re.compile(r"\[(TOWN_HERM_\w+)\]\s*=\s*\{\s*(MAP_\w+),\s*(\d+),\s*(\d+),\s*(HEAL_LOCATION_\w+),")
ARRIVAL = re.compile(r"\bwarp\w*\s*\(?\s*(MAP_\w+)\s*,\s*(\d+)\s*,\s*(\d+)")


def scripted_arrivals(root):
    """MAP -> [(x, y)] for every script that warps the player to a map's coordinates."""
    out = {}
    for p in list((root / "data").rglob("*.pory")) + list((root / "data/scripts").rglob("*.inc")):
        for m in ARRIVAL.finditer(p.read_text(errors="replace")):
            out.setdefault(m.group(1), []).append((int(m.group(2)), int(m.group(3))))
    return out


def main():
    verbose = "-v" in sys.argv[1:]
    repo = Repo(REPO)
    rows = ROW.findall((REPO / "src/data/ichor_town_herms.h").read_text())
    heals = json.loads((REPO / "src/data/heal_locations.json").read_text())["heal_locations"]
    arrivals = scripted_arrivals(REPO)
    fails = []

    covered = {heal for _, _, _, _, heal in rows}
    for h in heals:
        if "respawn_map" in h and h["id"] not in covered:
            fails.append(f"{h['id']} ({h['map']}) has a healer but no travel herm row in "
                         "src/data/ichor_town_herms.h")

    sys.path.insert(0, str(REPO / "tools/ichor/maps"))
    from town_herms import TOWNS
    placed = {row[0]: row[3] for row in TOWNS}

    for town, map_id, lx, ly, _ in rows:
        lx, ly = int(lx), int(ly)
        name = repo.name_of(map_id)
        if name is None:
            fails.append(f"{town}: no map {map_id}")
            continue
        if placed.get(name) != (lx, ly):
            fails.append(f"{town}: the landing tile ({lx},{ly}) differs from tools/ichor/maps/town_herms.py's "
                         f"{placed.get(name)} for {name}")
        m = repo.map(name)
        herms = [o for o in m.objects if o.get("graphics_id") == HERM_GFX]
        plaques = [o for o in m.objects if o.get("graphics_id") == PLAQUE_GFX]
        if len(herms) != 1 or herms[0].get("script") != "EventScript_IchorTownHerm":
            fails.append(f"{town}: {name} needs one {HERM_GFX} running EventScript_IchorTownHerm "
                         "(tools/ichor/maps/town_herms.py)")
            continue
        if not plaques:
            fails.append(f"{town}: {name} has no {PLAQUE_GFX} beside its herm")
        hx, hy = herms[0]["x"], herms[0]["y"]
        if max(abs(hx - lx), abs(hy - ly)) != 1:
            fails.append(f"{town}: the landing tile ({lx},{ly}) is not beside the herm ({hx},{hy})")

        # Where the player arrives: connected edges, doors in from other maps
        # (not this town's own houses), and scripted arrivals.
        starts = []
        for label, cells in entries(m):
            if label.startswith("warp"):
                dest = label.split(" to ", 1)[1]
                if dest.startswith(map_id + "_"):
                    continue
            starts += cells
        starts += arrivals.get(map_id, [])
        w = Walker(m)
        adj = w.graph(w.starts(starts))
        dist = bfs(adj, [s for s in adj if (s[0], s[1]) in set(starts)])
        steps = min((d for (x, y, _), d in dist.items() if (x, y) == (lx, ly)), default=None)
        if steps is None:
            fails.append(f"{town}: the landing tile ({lx},{ly}) on {name} can't be walked to from an entrance")
        elif steps > MAX_STEPS:
            fails.append(f"{town}: the herm on {name} is {steps} steps from the nearest entrance "
                         f"(at most {MAX_STEPS}): stand it where the player arrives")
        elif verbose:
            print(f"herm_audit: {town:24} {name:18} herm ({hx},{hy}) landing ({lx},{ly}) {steps} steps in")

    for f in fails:
        print("herm_audit FAIL:", f)
    if not fails:
        print(f"herm_audit: {len(rows)} towns, each with a travel herm by its entrance")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
