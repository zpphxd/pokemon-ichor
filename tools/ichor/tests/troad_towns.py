#!/usr/bin/env python3
"""Write the data tools/ichor/tests/troad_towns.lua walks: for Sestos, the
Hellespont and Ilion, every door (where to stand, the room it leads to), every
sign and hidden item (where to stand and which way to face), the people to talk
to, a calm cell above the current, and the constants the test needs, compiled
by troad_towns.sh from the game's headers.

  troad_towns.py OUT_DIR    writes OUT_DIR/grids.lua and OUT_DIR/consts.c
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
import troad_lib as T  # noqa: E402

MAPS = ("Sestos", "Hellespont", "Ilion")
FACE = {(0, 1): "UP", (0, -1): "DOWN", (1, 0): "LEFT", (-1, 0): "RIGHT"}


def stand_for(blocks, ev, x, y, surf_ok=True):
    """A cell beside (x, y) to stand on, and the key that faces (x, y) from it.
    Land first; water if nothing else (the warp starts the player surfing)."""
    taken = {(o["x"], o["y"]) for o in ev["object_events"]}
    options = []
    for (dx, dy) in ((0, 1), (-1, 0), (1, 0), (0, -1)):
        sx, sy = x + dx, y + dy
        if (sx, sy) in taken:
            continue
        if T.walkable(blocks, sx, sy):
            options.append((0, sx, sy, FACE[(dx, dy)]))
        elif surf_ok and T.surfable(blocks, sx, sy) and \
                T.behavior(int(blocks[sy, sx]) & 0x3FF) != "MB_EASTWARD_CURRENT":
            options.append((1, sx, sy, FACE[(dx, dy)]))
    if not options:
        raise SystemExit(f"nowhere to stand beside ({x},{y})")
    return sorted(options)[0][1:]


def lua(v):
    if isinstance(v, str):
        return '"' + v + '"'
    if isinstance(v, (list, tuple)):
        return "{ " + ", ".join(lua(i) for i in v) + " }"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k} = {lua(i)}" for k, i in v.items()) + " }"
    return str(v)


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    data, names = {}, {"MAP_AKTI_TOWN", "MAP_SESTOS", "MAP_HELLESPONT", "MAP_ILION"}
    flags = {"FLAG_ICHOR_OIKOUMENE_ARRIVED", "FLAG_ICHOR_HELLESPONT_GOT_RARE_BONE"}
    for m in MAPS:
        blocks, ev = T.load(m)
        doors = []
        for w_ in ev["warp_events"]:
            assert T.walkable(blocks, w_["x"], w_["y"] + 1), (m, w_)
            doors.append({"x": w_["x"], "y": w_["y"] + 1, "dest": w_["dest_map"]})
            names.add(w_["dest_map"])
        reads = []
        for b in ev["bg_events"]:
            sx, sy, face = stand_for(blocks, ev, b["x"], b["y"])
            r = {"x": sx, "y": sy, "face": face, "what": f"{b['type']} ({b['x']},{b['y']})"}
            if b["type"] == "hidden_item":
                r["flag"] = b["flag"]
                flags.add(b["flag"])
            reads.append(r)
        talks = []
        for o in ev["object_events"]:
            if o["script"] in ("0x0", "0") or o["trainer_type"] != "TRAINER_TYPE_NONE":
                continue
            if "ITEM_BALL" in o["graphics_id"] or "ALETHEA" in o["graphics_id"] \
                    or "NAUSIKLES" in o.get("local_id", ""):
                continue
            if o["movement_type"] == "MOVEMENT_TYPE_WANDER_AROUND":
                continue
            sx, sy, face = stand_for(blocks, ev, o["x"], o["y"], surf_ok=False)
            talks.append({"x": sx, "y": sy, "face": face, "what": o.get("local_id", o["script"])})
        data[m] = {"doors": doors, "reads": reads, "talks": talks}
    # the current: a calm cell north of a race, clear of every swimmer's sight
    blocks, ev = T.load("Hellespont")
    sight = set()
    for o in ev["object_events"]:
        if o["trainer_type"] != "TRAINER_TYPE_NONE":
            sight |= set(T.sight_cells(o)) | {(o["x"], o["y"])}
    hh, ww = blocks.shape
    start = None
    for y in range(9, hh):
        for x in range(16, 28):
            above_calm = T.surfable(blocks, x, y - 1) and \
                T.behavior(int(blocks[y - 1, x]) & 0x3FF) != "MB_EASTWARD_CURRENT"
            if above_calm and T.behavior(int(blocks[y, x]) & 0x3FF) == "MB_EASTWARD_CURRENT" \
                    and (x, y - 1) not in sight and (x, y) not in sight:
                start = (x, y - 1)
                break
        if start:
            break
    data["current"] = {"x": start[0], "y": start[1]}
    (out / "grids.lua").write_text("return " + lua(data) + "\n")

    c = ['#include "global.h"', '#include "main.h"', '#include "fieldmap.h"', '#include "ichor_save.h"',
         '#include "constants/battle.h"', '#include "constants/flags.h"', '#include "constants/map_groups.h"',
         '#include "constants/opponents.h"', '#include "constants/vars.h"', "",
         "#define K(name, value) const int k_##name = (value);", ""]
    for n in sorted(names):
        c.append(f"K({n}, {n})")
    for f in sorted(flags):
        c.append(f"K({f}, {f})")
    c += [
        "K(TRAINER_KOTYS, TRAINER_ICHOR_KOTYS)",
        "K(TRAINER_FLAGS_START, TRAINER_FLAGS_START)",
        "K(B_OUTCOME_WON, B_OUTCOME_WON)",
        "K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)",
        "K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))",
        "K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))",
        "K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))",
        "K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))",
        "K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))",
        "K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))",
        "K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1)",
        "K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))",
        "K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))",
        "K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))",
        "K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))",
        "K(MAP_OFFSET, MAP_OFFSET)",
    ]
    (out / "consts.c").write_text("\n".join(c) + "\n")
    print(json.dumps({m: {k: len(v) for k, v in d.items()} for m, d in data.items() if m in MAPS}))


if __name__ == "__main__":
    main(sys.argv[1])
