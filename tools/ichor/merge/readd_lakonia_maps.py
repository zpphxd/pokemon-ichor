#!/usr/bin/env python3
"""After taking upstream's layouts.json and map_groups.json in a merge, put
Lakonia's layouts and map group back from a ref (default HEAD, our side).

    python3 tools/ichor/merge/readd_lakonia_maps.py [REF]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REF = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
GROUP = "gMapGroup_Lakonia"


def show(path):
    return json.loads(subprocess.run(["git", "show", f"{REF}:{path}"], cwd=ROOT, check=True,
                                     capture_output=True, text=True).stdout)


ours_groups = show("data/maps/map_groups.json")
names = set(ours_groups[GROUP])
gp = ROOT / "data/maps/map_groups.json"
g = json.loads(gp.read_text())
if GROUP not in g["group_order"]:
    g["group_order"].append(GROUP)
g[GROUP] = ours_groups[GROUP]
gp.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")

ours_layouts = show("data/layouts/layouts.json")
lp = ROOT / "data/layouts/layouts.json"
lay = json.loads(lp.read_text())
have = {e["id"] for e in lay["layouts"]}
add = [e for e in ours_layouts["layouts"] if e["name"].replace("_Layout", "") in names and e["id"] not in have]
lay["layouts"] += add
lp.write_text(json.dumps(lay, indent=2, ensure_ascii=False) + "\n")
print(f"map group {GROUP}: {len(names)} maps; {len(add)} layouts re-added")
