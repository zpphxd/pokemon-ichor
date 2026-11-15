"""The Gulf ferry's deck (MAP_GULF_FERRY_DECK, 20x12, aethos + gulf_ferry): Route
10, Panopeus's boat under way across the Gulf of Korinthos. See harbors.py.

The boat lies west-east, its bow toward Aigion: the far rail along row 3 (fish
over it), the deck in rows 4-6, the near rail, the hull's side and the waterline
in rows 7-9, aethos's animated gulf all round. Amidships the mast and the
patched sail (over the far rail and the water), the goats' pen; at the bow the
lashed amphorae and grain, where Lamprias sits facing the sea; at the stern the
deckhouse and the steering oar, where Panopeus stands and Alethea watches the
wake. Reached only by the quays' scripted warps.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harbors as H  # noqa: E402
from harbors import SEA, Grid, hidden, item_ball, obj, sign  # noqa: E402

NAME, LAYOUT = "GulfFerry_Deck", "LAYOUT_GULF_FERRY_DECK"
W, HGT = 20, 12
S = "GulfFerry_Deck_EventScript_"
ARRIVAL = (11, 6)          # where the quays' warps land the player
PANOPEUS = (16, 5)
ALETHEA = (16, 6)


def compose():
    g = Grid("gulf_ferry", W, HGT)
    for y in range(HGT):
        for x in range(W):
            g.set(x, y, SEA, True, built=False)    # open water: impassable on foot
    g.put("bow", 1, 2)
    for x in range(4, 16, 2):
        g.put("midships", x, 3)
    g.put("stern", 16, 2)
    g.put("sail", 7, 1)
    g.put("deckhouse", 13, 3)
    g.put("goat_pen", 6, 5)
    g.put("bow_cargo", 4, 5)
    g.put("grain_sack", 4, 4)                   # grain for Arkadia, by Lamprias
    g.put("grain_sack", 12, 6)                  # more grain, by the stern
    # the water: surfable and fishable in the game's terms (elevation 1), but not
    # walkable; the map's ON_TRANSITION forbids relics, so no one surfs off a ferry
    for y in range(HGT):
        for x in range(W):
            if g.behavior(int(g.mid[y, x])) in H.SURF_BEHAVIORS:
                g.solid[y, x] = False
    return g


def border():
    return [SEA, SEA, SEA, SEA]


def events():
    objects = [
        obj("LOCALID_GULF_FERRY_PANOPEUS", "OBJ_EVENT_GFX_ICHOR_PANOPEUS", *PANOPEUS, S + "Panopeus",
            move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_GULF_FERRY_ALETHEA", "OBJ_EVENT_GFX_ICHOR_ALETHEA", *ALETHEA, S + "Alethea",
            flag="FLAG_ICHOR_HIDE_ALETHEA_GULF_FERRY", move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_GULF_FERRY_GOAT_1", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 6, 5, S + "Goat",
            move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_GULF_FERRY_GOAT_2", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 8, 6, S + "Goat",
            move="MOVEMENT_TYPE_LOOK_AROUND"),
        obj("LOCALID_GULF_FERRY_KEPHISIOS", "OBJ_EVENT_GFX_ICHOR_FISHER", 11, 3, S + "Kephisios",
            trainer=True, sight=1, move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_GULF_FERRY_LAMPRIAS", "OBJ_EVENT_GFX_ICHOR_MERCHANT", 2, 4, S + "Lamprias",
            trainer=True, sight=1, move="MOVEMENT_TYPE_FACE_LEFT"),
        item_ball("LOCALID_GULF_FERRY_ITEM_SUPER_POTION", 3, 6, "ITEM_SUPER_POTION",
                  "FLAG_ICHOR_ITEM_GULF_FERRY_SUPER_POTION"),
    ]
    bgs = [
        sign(10, 7, S + "Rail"),
        sign(13, 7, S + "Rail"),
        sign(14, 4, S + "Deckhouse"),
        hidden(8, 5, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_GULF_FERRY_HEART_SCALE"),
    ]
    return objects, [], [], bgs


HEADER = {
    "layout": LAYOUT,
    "music": "MUS_ICHOR_TRIREME",
    "map_type": "MAP_TYPE_OCEAN_ROUTE",
    "weather": "WEATHER_SUNNY",
    "allow_cycling": False, "allow_escaping": False, "allow_running": True,
    "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": None,
}


def build():
    g = compose()
    H.write_layout(NAME, LAYOUT, g, border(), "gTileset_GulfFerry")
    H.write_map_json(NAME, HEADER, *events())
    return g


SCREENS = {"1_deck": (10, 5)}


def render(out_dir):
    return H.render(NAME, LAYOUT, out_dir, "gulf_ferry", SCREENS)


def check(g):
    errors, reach, blocks = H.common_checks(
        g, NAME, ARRIVAL, solid_ok=("LOCALID_GULF_FERRY_GOAT_1", "LOCALID_GULF_FERRY_GOAT_2"),
        unreachable_ok=())
    for p in (PANOPEUS, ALETHEA):
        near = [(p[0] + dx, p[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if not any(q in reach for q in near):
            errors.append(f"Deck: nobody can reach {p}")
    # fishing: some deck cell looks north over the far rail onto water
    if not any(H.walkable(blocks, x, 3) and (int(blocks[2, x]) >> 12) == 1 for x in range(W)):
        errors.append("Deck: no deck cell faces open water to fish from")
    # people stand in the way on a deck this small: with every object as an obstacle,
    # each one still has a free cell beside it to be talked to (or picked up) from
    ev = H.json.loads((H.ROOT / f"data/maps/{NAME}/map.json").read_text())
    occupied = {(o["x"], o["y"]) for o in ev["object_events"]}
    free_reach = H.reachable(blocks, ARRIVAL, blocked=occupied)
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in free_reach for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            errors.append(f"Deck: {o['local_id']} at ({x},{y}) is walled in by the others")
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        if not any((x + dx, y + dy) in free_reach for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            errors.append(f"Deck: bg event at ({x},{y}) is walled in by the people")
    # nothing walkable reaches the map's edge
    for (x, y) in reach:
        if x in (0, W - 1) or y in (0, HGT - 1):
            errors.append(f"Deck: ({x},{y}) at the map's edge is reachable")
    return errors
