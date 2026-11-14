#!/usr/bin/env python3
"""Create a new Ichor map and register it everywhere the build needs it.

  python3 tools/ichor/new_map.py ElaiaVillage --group gMapGroup_TownsAndRoutes \\
      --layout-from LAYOUT_LITTLEROOT_TOWN --mapsec MAPSEC_ELAIA_VILLAGE \\
      --music MUS_LITTLEROOT --type MAP_TYPE_TOWN

What it does:
  - writes data/maps/<Name>/map.json with no events (MAP_ID derived from Name)
  - writes data/maps/<Name>/scripts.pory with an empty mapscripts block, and
    ignores the generated scripts.inc
  - appends the map to its group in data/maps/map_groups.json (creating the
    group at the end of group_order if needed, so no existing MAP_NUM moves)
  - includes the scripts from data/ichor_maps.inc
  - layout: --layout reuses an existing layout as-is; --layout-from copies one
    into data/layouts/<Name>/ as a new LAYOUT_<NAME> you can then edit
"""
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / "data/maps"
LAYOUTS = ROOT / "data/layouts/layouts.json"
GROUPS = MAPS / "map_groups.json"
INCLUDES = ROOT / "data/ichor_maps.inc"


def const_name(name):
    """ElaiaVillage_PlayersHouse_1F -> ELAIA_VILLAGE_PLAYERS_HOUSE_1F"""
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name).upper()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="CamelCase map name, e.g. AktiTown_Agora")
    ap.add_argument("--group", required=True, help="map group, e.g. gMapGroup_TownsAndRoutes")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--layout", help="reuse this existing layout id")
    src.add_argument("--layout-from", help="copy this layout id into a new LAYOUT_<NAME>")
    ap.add_argument("--primary", help="tileset for a copied layout, e.g. gTileset_Aethos")
    ap.add_argument("--secondary", help="secondary tileset for a copied layout")
    ap.add_argument("--mapsec", required=True)
    ap.add_argument("--music", required=True)
    ap.add_argument("--type", default="MAP_TYPE_INDOOR")
    ap.add_argument("--weather", default=None)
    ap.add_argument("--show-name", action="store_true", help="show the map name popup on entry")
    args = ap.parse_args()

    name = args.name
    map_dir = MAPS / name
    if map_dir.exists():
        raise SystemExit(f"{map_dir} already exists")
    map_id = "MAP_" + const_name(name)
    for other in MAPS.glob("*/map.json"):
        if f'"id": "{map_id}"' in other.read_text():
            raise SystemExit(f"{map_id} is already used by {other.parent.name}")

    layouts = json.loads(LAYOUTS.read_text())
    by_id = {l["id"]: l for l in layouts["layouts"] if "id" in l}
    if args.layout:
        if args.layout not in by_id:
            raise SystemExit(f"unknown layout {args.layout}")
        layout_id = args.layout
    else:
        if args.layout_from not in by_id:
            raise SystemExit(f"unknown layout {args.layout_from}")
        base = by_id[args.layout_from]
        layout_id = "LAYOUT_" + const_name(name)
        if layout_id in by_id:
            raise SystemExit(f"{layout_id} already exists")
        dst = ROOT / "data/layouts" / name
        dst.mkdir(parents=True)
        shutil.copy(ROOT / base["border_filepath"], dst / "border.bin")
        shutil.copy(ROOT / base["blockdata_filepath"], dst / "map.bin")
        layouts["layouts"].append({
            "id": layout_id,
            "name": f"{name}_Layout",
            "width": base["width"],
            "height": base["height"],
            "primary_tileset": args.primary or base["primary_tileset"],
            "secondary_tileset": args.secondary or base["secondary_tileset"],
            "border_filepath": f"data/layouts/{name}/border.bin",
            "blockdata_filepath": f"data/layouts/{name}/map.bin",
            "layout_version": base.get("layout_version", "emerald"),
        })
        write_json(LAYOUTS, layouts)

    outdoors = args.type in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE")
    map_dir.mkdir(parents=True)
    write_json(map_dir / "map.json", {
        "id": "MAP_" + const_name(name),
        "name": name,
        "layout": layout_id,
        "music": args.music,
        "region": "REGION_HOENN",
        "region_map_section": args.mapsec,
        "requires_flash": False,
        "weather": args.weather or ("WEATHER_SUNNY" if outdoors else "WEATHER_NONE"),
        "map_type": args.type,
        "allow_cycling": outdoors,
        "allow_escaping": False,
        "allow_running": True,
        "show_map_name": args.show_name or outdoors,
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
        "connections": None,
        "object_events": [],
        "warp_events": [],
        "coord_events": [],
        "bg_events": [],
    })
    (map_dir / "scripts.pory").write_text(f"mapscripts {name}_MapScripts {{}}\n")

    gitignore = ROOT / ".gitignore"
    ignore_line = f"data/maps/{name}/scripts.inc"
    if ignore_line not in gitignore.read_text().split("\n"):
        with gitignore.open("a") as f:
            f.write(ignore_line + "\n")

    groups = json.loads(GROUPS.read_text())
    if args.group not in groups:
        groups[args.group] = []
        groups["group_order"].append(args.group)
    groups[args.group].append(name)
    write_json(GROUPS, groups)

    if not INCLUDES.exists():
        INCLUDES.write_text("@ Ichor map scripts, included from data/event_scripts.s.\n"
                            "@ tools/ichor/new_map.py appends to this file.\n")
    with INCLUDES.open("a") as f:
        f.write(f'\t.include "data/maps/{name}/scripts.inc"\n')

    print(f"created MAP_{const_name(name)} using {layout_id}")


if __name__ == "__main__":
    main()
