#!/usr/bin/env python3
"""The climax's events on the world's existing maps (design/phase4/SCRIPT.md III-10
and III-12): the Fates at their three sanctuaries, Phaedon at Elpis's bedside and at
dawn, Daphne in her chair, the Stoa's unfinished decree. Each event is added once
(by local id or by position), so the script can run again after the maps change.

  python3 tools/ichor/maps/climax_world.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def obj(local_id, gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", flag="0"):
    return {"local_id": local_id, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": move, "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
            "script": script, "flag": flag}


def coord(x, y, script, var="VAR_TEMP_0", value="0"):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": str(value),
            "script": script}


def sign(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": script}


ADD = {
    # III-10E and III-12B: Elpis's room
    "Astyra_PhaedonsHouse": {
        "objects": [
            obj("LOCALID_PHAEDONS_HOUSE_BEDSIDE", "OBJ_EVENT_GFX_ICHOR_PHAEDON", 9, 4,
                "Astyra_PhaedonsHouse_EventScript_Bedside", "MOVEMENT_TYPE_FACE_RIGHT",
                "FLAG_ICHOR_HIDE_PHAEDON_BEDSIDE"),
            obj("LOCALID_PHAEDONS_HOUSE_DAPHNE_CHAIR", "OBJ_EVENT_GFX_ICHOR_PROFESSOR_DAPHNE", 11, 4,
                "Astyra_PhaedonsHouse_EventScript_DaphneChair", "MOVEMENT_TYPE_FACE_LEFT",
                "FLAG_ICHOR_HIDE_DAWN_CAST"),
            obj("LOCALID_PHAEDONS_HOUSE_PHAEDON_DAWN", "OBJ_EVENT_GFX_ICHOR_PHAEDON", 8, 11,
                "Astyra_PhaedonsHouse_EventScript_PhaedonDawn", "MOVEMENT_TYPE_FACE_UP",
                "FLAG_ICHOR_HIDE_DAWN_CAST"),
        ],
    },
    # III-10C: the Cutter on the cold anvil, beside Talos (21,8)
    "Kaldera_TelchinesForge": {
        "objects": [
            obj("LOCALID_FORGE_CUTTER", "OBJ_EVENT_GFX_SPECIES(THANIRA)", 19, 8,
                "Kaldera_TelchinesForge_EventScript_Cutter", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_ICHOR_HIDE_FATE_CUTTER"),
        ],
    },
    # III-10F: the Spinner among the roots of the old olive
    "ElaiaVillage": {
        "objects": [
            obj("LOCALID_ELAIA_SPINNER", "OBJ_EVENT_GFX_SPECIES(NEMIRA)", 12, 19,
                "ElaiaVillage_EventScript_Spinner", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_ICHOR_HIDE_FATE_SPINNER"),
        ],
    },
    # III-10D: the Measurer at the Pool of Mnemosyne, Arkadia's falls pool
    "Arkadia": {
        "objects": [
            obj("LOCALID_ARKADIA_MEASURER", "OBJ_EVENT_GFX_SPECIES(LOTIRA)", 28, 36,
                "Arkadia_EventScript_Measurer", "MOVEMENT_TYPE_FACE_RIGHT",
                "FLAG_ICHOR_HIDE_FATE_MEASURER"),
        ],
    },
    # III-10G: Kleon, awake and in color, where he stood mid-swing in the court's
    # gate; the wake runs as you pass him (any tile round the gate)
    "Delphoi": {
        "objects": [
            obj("LOCALID_DELPHOI_KLEON_FREE", "OBJ_EVENT_GFX_ICHOR_KLEON_FREE", 23, 18,
                "Climax_EventScript_DelphoiKleonTalk", "MOVEMENT_TYPE_FACE_DOWN",
                "FLAG_ICHOR_HIDE_KLEON_FREE_DELPHOI"),
        ],
        "coords": [coord(x, y, "Climax_EventScript_DelphoiKleonWakes", "VAR_ICHOR_ACT3", 15)
                   for (x, y) in ((21, 18), (22, 18), (24, 18), (25, 18), (23, 19), (24, 19),
                                  (21, 16), (22, 16))],
    },
    # III-10E: Lykophron's desk in the Stoa, the unfinished decree under his hand
    "Astyra_Stoa": {
        "bgs": [sign(21, 12, "Astyra_Stoa_EventScript_UnfinishedDecree")],
    },
}


def main():
    for name, add in ADD.items():
        p = ROOT / "data/maps" / name / "map.json"
        d = json.loads(p.read_text())
        have = {o.get("local_id") for o in d.get("object_events", [])}
        for o in add.get("objects", []):
            if o["local_id"] not in have:
                d.setdefault("object_events", []).append(o)
        for kind, key in (("coords", "coord_events"), ("bgs", "bg_events")):
            spots = {(e["x"], e["y"]) for e in d.get(key) or []}
            for e in add.get(kind, []):
                if (e["x"], e["y"]) not in spots:
                    d.setdefault(key, [])
                    d[key].append(e)
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        print("updated", name)


if __name__ == "__main__":
    main()
