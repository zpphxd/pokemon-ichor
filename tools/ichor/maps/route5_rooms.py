#!/usr/bin/env python3
"""Route 5's roadside inn, the Inn of the Plain: its room and its events.

Every house is a home and every interior is unique (design/MAP_DESIGN.md
section 2). Thria moved to Act II (design/phase2/BUILD.md), so its inn stands
on Route 5 instead, at the foot of the Skironian cliffs where the road comes
out onto Eleusa's plain: Xenokles's household from SCRIPT.md Part 2, "The Inn
of the Plain", with his rest and his trade. Render-and-critique passes are in
design/phase2/MAPS_route5.md.

The room is laid out from gTileset_Domos (design/phase2/TILES_limen.md), the
set Emporion's town rooms share, by ergasteria_build.py's machinery: its new
cells are appended after Emporion's, so their metatile ids don't move.

  /usr/bin/python3 tools/ichor/maps/route5_rooms.py   # builds domos and the room, writes its events

Room format: aegina_homes.py's. The exit is warp 0, the door mat, back to the
inn's door on Route 5 (its warp 1).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOMS_DOC = ROOT / "design/phase2/MAPS_route5.md"

ROOMS = {
    # ------------------------------------------------------------------
    # The Inn of the Plain. A long, low common room under one beam: the
    # pilgrims' pallets down the west end, their sandals on pegs over them
    # (Galanthis takes the left ones), the road scratched on the plaster by
    # everyone who ever walked it; the hearth halfway down, its soot up the
    # wall, a bench-and-trestle table before it and a krater by it; wine jars
    # in a rack; the washbasin by the door, because a guest's feet come
    # first. Through two posts at the east end, the stable: trodden earth,
    # feed sacks, a water jar, and the barred doors out to the donkey yard,
    # where Xenokles's stall waits for a donkey.
    "rest_house": {
        "set": "domos",
        "title": "The Inn of the Plain, Route 5",
        "map": "MAP_ROUTE5_REST_HOUSE",
        "layout": "Route5_RestHouse",
        "render": "route5_rest_house.png",
        "floor": "terracotta",
        "floors": {",": "claydust"},
        "wall": "red",
        "grid": [
            "WWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWW",
            "............,,,,",
            "............,,,,",
            "............,,,,",
            "............,,,,",
            "............,,,,",
            "............,,,,",
            "............,,,,",
        ],
        "rugs": [],
        "stamps": [
            # the west end: pallets, sandals on pegs, the road on the wall
            ("sandals_pegs", 0, 1),
            ("road_map", 2, 0),
            ("window", 4, 0),
            ("pallet", 0, 2),
            ("pallet", 2, 2),
            ("pallet", 0, 6),
            ("lampstand", 10, 6),
            # the hearth halfway down, its soot, its pots; the table
            ("soot", 6, 0),
            ("hearth", 6, 2),
            ("pots", 5, 2),
            ("window", 9, 0),
            ("krater", 9, 2),
            ("bench", 3, 4),
            ("table", 3, 5),
            ("bench", 3, 6),
            ("stool", 5, 5),
            ("amphora_rack", 10, 0),
            # the washbasin by the door
            ("louterion", 6, 7),
            ("mat", 7, 8),
            # the stable, through two posts
            ("column", 11, 2),
            ("column", 11, 6),
            ("shed_doors", 13, 0),
            ("sack", 15, 2),
            ("sack", 12, 2),
            ("water_jar", 15, 6),
            ("sack", 12, 8),
            ("crate", 15, 8),
            ("sack", 13, 8),
        ],
        "spots": [
            ("warp", "door to Route 5 (south-arrow mat)", [(7, 8), (8, 8)]),
            ("npc", "Xenokles, the innkeeper, by his hearth", (8, 3), "south"),
            ("npc", "the stable boy, in the stable", (14, 6), "west"),
            ("npc", "Galanthis the Gelasable, at the sandals (before the trade)", (1, 4), "north"),
            ("npc", "the Onotis in the stall (after the trade)", (14, 3), "south"),
            ("bg", "the road scratched on the wall", (3, 1), (3, 2, "north")),
            ("bg", "the sandals on their pegs", (1, 1), (1, 2, "north")),
            ("bg", "the hearth", (7, 3), (7, 4, "north")),
            ("bg", "the washbasin by the door", (6, 8), (5, 8, "east")),
            ("bg", "the stable doors", (13, 1), (13, 2, "north")),
        ],
    },
}

# ---------------------------------------------------------------------------
# Events (map.json), from the spots above
# ---------------------------------------------------------------------------
PX = "Route5_RestHouse_EventScript_"
INN_DOOR_WARP = 1          # tools/ichor/maps/route5.py: warps() 1 is the inn's door


def write_events():
    spec = ROOMS["rest_house"]
    path = ROOT / "data/maps/Route5_RestHouse/map.json"
    m = json.loads(path.read_text())
    m["music"] = "MUS_ICHOR_ELEUSA"
    m["map_type"] = "MAP_TYPE_INDOOR"
    m["weather"] = "WEATHER_NONE"
    m["show_map_name"] = False
    m["connections"] = None
    objs = [
        ("LOCALID_REST_HOUSE_XENOKLES", "OBJ_EVENT_GFX_ICHOR_ELDER_M", (8, 3), "DOWN", "Xenokles", "0"),
        ("LOCALID_REST_HOUSE_STABLE_BOY", "OBJ_EVENT_GFX_ICHOR_KID_M", (14, 6), "LEFT", "StableBoy", "0"),
        ("LOCALID_REST_HOUSE_GALANTHIS", "OBJ_EVENT_GFX_SPECIES(GELASABLE)", (1, 4), "UP", "Galanthis",
         "FLAG_ICHOR_TRADED_GELASABLE"),
        ("LOCALID_REST_HOUSE_ONOTIS", "OBJ_EVENT_GFX_SPECIES(ONOTIS)", (14, 3), "DOWN", "Onotis", "FLAG_TEMP_1"),
    ]
    m["object_events"] = [{
        "local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
        "script": PX + script, "flag": flag} for lid, gfx, (x, y), facing, script, flag in objs]
    warp = next(s for s in spec["spots"] if s[0] == "warp")
    m["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": "MAP_ROUTE5_SKIRONIAN_CLIFFS",
                         "dest_warp_id": str(INN_DOOR_WARP)} for x, y in warp[2]]
    m["coord_events"] = []
    bgs = []
    names = {"the road scratched on the wall": "RoadMap", "the hearth": "Hearth",
             "the sandals on their pegs": "Sandals",
             "the washbasin by the door": "Washbasin", "the stable doors": "StableDoors"}
    for s in spec["spots"]:
        if s[0] != "bg":
            continue
        (x, y), (fx, fy, facing) = s[2], s[3]
        bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                    "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{facing.upper()}", "script": PX + names[s[1]]})
    m["bg_events"] = bgs
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def main():
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import ergasteria_build as EB
    import limen_build
    args = EB.parse_args()
    EB.build(limen_build.DOMOS, args)
    write_events()


if __name__ == "__main__":
    main()
