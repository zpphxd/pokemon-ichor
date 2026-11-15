#!/usr/bin/env python3
"""Build Sestos (aethos + troas): the Troad's port on the Hellespont, its events,
and its checks.

Writes data/layouts/Sestos/map.bin and border.bin (36 x 30) and the events in
data/maps/Sestos/map.json, then checks them.

The town (OIKOUMENE.md §4.1, §2; MAPS_troad.md): a harbor opening south onto the
strait, an L of quays round its inner basin, the Euploia moored by the mole with
Nausikles at her gangplank, and Hero's round tower on the eastern point with
the lamp she lights every night for a swimmer. The Asclepeion and the Agora face
the quay. Up the hill, past the herm at the crossroads, the old acropolis wall
and its grove look out over the water to Abydos.

Doors (BUILD.md §5): warp 0 Asclepeion, 1 Agora, 2 Hero's tower, 3 the ferry
house, 4 the net-loft, each to its room's warp 0.

Seam: the south edge is the Hellespont's north edge (down, offset -28): the road
to the Hebros strip x 2-5, the harbor mouth x 9-27, the headland path x 30-32.
Same tileset on both sides, so no aethos-only strip.

Usage: /usr/bin/python3 tools/ichor/maps/sestos.py [--render DIR] [--no-check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import troad_lib as T  # noqa: E402
from troad_lib import (AGORA, ASCLEPEION, OLIVE_TOP, OLIVE_BOT_TIP, STELE, Grid, hidden, item_ball,  # noqa: E402
                       obj, paint, sign, trigger, warp)

W, H = 36, 30
NAME = "Sestos"
LAYOUT = "LAYOUT_SESTOS"
ROAD = range(2, 6)           # to the Hebros strip (Hellespont x 30-33)
MOUTH = range(9, 28)         # the harbor mouth (Hellespont x 37-55)
POINT_ROAD = range(30, 33)   # down from Hero's point (Hellespont x 58-60)
SHIP = (9, 20)               # the trireme's top-left; her gangplank lands at (12, 23)
GANGPLANK = (12, 23)
TOWER = (27, 22)             # Hero's tower's top-left (lamp row); door (27, 26)
ASC = (4, 11)                # the Asclepeion's top-left; door (5, 14)
AGO = (9, 11)                # the Agora's; door (10, 14)
LOFT = (14, 11)              # the net-loft, 3 x 4; door (15, 14)
FERRY = (20, 12)             # the ferry house, 4 x 3; door (21, 14)
WINGS = (5, 15)              # the Wings' landing, outside the Asclepeion


def plan():
    P = [["g"] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                P[y][x] = ch

    # the harbor: inner basin, the mole, the outer harbor, the mouth
    fill(9, 19, 26, 29, "~")
    fill(5, 17, 26, 18, "q")          # the town quay
    fill(5, 19, 8, 24, "q")           # the west quay
    fill(9, 23, 20, 24, "q")          # the mole
    fill(27, 25, 27, 29, "~")
    # the headland, its shore
    fill(27, 12, 35, 24, "g")
    fill(28, 25, 35, 28, "g")
    fill(26, 19, 26, 22, "s")
    fill(27, 23, 27, 24, "s")
    fill(28, 26, 29, 28, "s")
    # streets
    fill(2, 15, 33, 16, "p")          # the quay street
    fill(2, 17, 4, 29, "p")           # the road down to the Hebros strip
    fill(5, 25, 5, 29, "p")
    fill(17, 5, 18, 14, "p")          # up the hill to the acropolis gate
    fill(2, 10, 33, 10, "p")          # the upper lane
    fill(30, 11, 32, 29, "p")         # down the headland
    fill(27, 27, 29, 27, "p")         # to the tower door
    fill(16, 1, 19, 2, "p")           # inside the acropolis
    # gardens: the bean rows west, a wheat plot east, both walled
    fill(3, 6, 6, 8, "t")
    fill(28, 6, 32, 8, "W")
    fill(21, 11, 23, 11, "t")         # the ferryman's herbs
    return P


def compose():
    g = Grid(W, H)
    P = plan()
    paint(g, P)

    # ---- the harbor -----------------------------------------------------------
    g.put("trireme", *SHIP)
    g.put("quay_gangplank", *GANGPLANK)
    g.put("bollard_line", 10, 23)
    g.put("bollard_line", 15, 23)
    g.put("bollard_line", 20, 18)
    g.put("bollard_line", 24, 18)
    g.set(8, 17, STELE, True)                     # THE QUAY: the harbor's sign
    # ---- Hero's tower on the point ------------------------------------------------
    g.put("heros_tower", *TOWER)
    # ---- the quay street: Asclepeion and Agora facing the harbor ---------------
    g.block(ASCLEPEION, *ASC)
    g.set(ASC[0] + 1, ASC[1] + 3, ASCLEPEION[3][1], False)
    g.block(AGORA, *AGO)
    g.set(AGO[0] + 1, AGO[1] + 3, AGORA[3][1], False)
    # the net-loft: a tall white house, two storeys over the quay
    house(g, LOFT[0], LOFT[1], 3, rows=("roof", "up_shutters", "up_window", "door"), white=True,
          roof_parts=("roof_W", "roof_jars", "roof_E"))
    # the ferry house, ochre, by the harbor mouth
    house(g, FERRY[0], FERRY[1], 4, rows=("roof", "up_window", "door"))
    g.put("yard", 18, 13, cx=0, w=1)              # hay for the ferry's mule
    g.put("yard", 25, 13, cx=4, w=1)              # tubs of pitch and dye for the nets
    # ---- the upper town -----------------------------------------------------------
    g.put("great_herm", 19, 8)                    # the crossroads herm (ICHOR_STUB_HERM)
    g.set(16, 11, STELE, True)                    # SESTOS: the town sign by the herm
    g.set(5, 27, STELE, True)                     # the road down to the Hebros strip
    g.set(29, 28, STELE, True)                    # HERO'S POINT, by the path to the strait
    # the acropolis wall, its open gate and a tower, rows 3-5
    for x in range(10, 27):
        part = "end_W" if x == 10 else "end_E" if x == 26 else "offset" if x in (13, 22) else "run"
        g.put("wall", x, 3, cx=g.cat["wall"]["names"][part][0], w=1)
    g.put("gateway", 16, 3)
    g.put("tower", 23, 2)
    # the acropolis grove behind the wall
    g.trees(olives=((12, 0), (21, 0), (24, 0), (9, 1)), cypresses=((14, 0), (20, 1), (27, 0)))
    g.set(15, 1, 0x0E0, True)
    # gardens and groves
    g.trees(olives=((0, 2), (3, 3), (7, 6), (24, 7), (33, 6), (26, 10)),
            pines=((0, 11), (33, 12)),
            cypresses=((8, 3), (6, 1), (2, 1), (28, 3), (34, 2), (12, 7), (22, 7), (14, 7)),
            ida=((31, 1), (27, 16)), oaks=((24, 21 - 1),))
    g.trees(olives=((28, 13), (33, 17), (33, 21), (28, 19)), cypresses=((29, 16), (34, 24), (26, 13)))
    # garden walls: dry stone round the bean rows and the wheat plot, a gap to
    # each from the lane
    g.wall_we(2, 7, 5)
    g.wall_ns(2, 6, 8, "w")
    g.wall_ns(7, 6, 8, "e")
    g.wall_we(27, 33, 5)
    g.wall_ns(27, 6, 8, "w")
    g.wall_ns(33, 6, 8, "e")
    # the quay's goods and the harbor front's shade trees
    g.part("yard", "blocks", 9, 18)
    g.trees(cypresses=((13, 7), (21, 6), (11, 6)), olives=((9, 6),))
    # the west side down to the road
    g.trees(olives=((0, 18), (0, 22), (6, 26)), cypresses=((0, 25), (1, 20), (7, 27)),
            pines=((0, 27),))
    # close the edges: west, north, east; the south edge is the seam
    g.forest(0, 28, 1, 29, salt=1)
    g.forest(6, 28, 8, 29, salt=2)
    g.forest(33, 26, 35, 29, salt=3)
    g.forest(28, 28, 29, 29, salt=4)
    g.forest(0, 0, 35, 0, salt=5)
    g.forest(0, 1, 1, 27, salt=6)
    g.forest(34, 1, 35, 25, salt=7)
    g.scatter([(1, 13), (7, 9), (13, 9), (23, 9), (29, 11), (34, 14), (28, 23), (31, 9), (20, 6)])
    g.scatter([(3, 12), (25, 11), (33, 19), (28, 21)], ["chamomile", "dry_tuft", "stones"])
    return g


def house(g, x, y, width, rows, white=False, roof_parts=None):
    """A Trojan house from the kit: rows name the middle part of each row below
    the roof ('roof', 'up', 'up_window', 'up_shutters', 'door', 'lo_window', ...)."""
    key = "house_kit_white" if white else "house_kit"
    for j, kind in enumerate(rows):
        for i in range(width):
            if j == 0:
                parts = roof_parts or ("roof_W", "roof", "roof_E")
                p = parts[0] if i == 0 else parts[2] if i == width - 1 else parts[1]
            else:
                tier = "lo" if j == len(rows) - 1 else "up"
                if i == 0:
                    p = f"{tier}_W"
                elif i == width - 1:
                    p = f"{tier}_E"
                elif i == 1 or width == 3:
                    p = kind if kind != "roof" else tier
                else:
                    p = "lo_window" if tier == "lo" else "up_window" if kind != "up_window" else "up"
            g.part(key, p, x + i, y + j)


def border():
    return [OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]]


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def events():
    pre = "Sestos_EventScript_"
    objects = [
        # the ship: Nausikles on the gangplank's foot (ICHOR_STUB_SHIP)
        obj("OBJ_EVENT_GFX_ICHOR_SAILOR", *GANGPLANK, pre + "Nausikles", "LOCALID_SESTOS_NAUSIKLES",
            "MOVEMENT_TYPE_FACE_DOWN"),
        # Alethea waits at the mole's root the first time anyone lands
        obj("OBJ_EVENT_GFX_ICHOR_ALETHEA", 7, 22, pre + "Alethea", "LOCALID_SESTOS_ALETHEA",
            "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_OIKOUMENE_ARRIVED"),
        # the quay
        obj("OBJ_EVENT_GFX_ICHOR_FISHER", 13, 17, pre + "QuayFisher", "LOCALID_SESTOS_QUAY_FISHER",
            "MOVEMENT_TYPE_FACE_DOWN"),
        obj("OBJ_EVENT_GFX_ICHOR_SAILOR", 22, 17, pre + "Sailor", "LOCALID_SESTOS_SAILOR",
            "MOVEMENT_TYPE_FACE_LEFT"),
        obj("OBJ_EVENT_GFX_ICHOR_WOMAN", 19, 16, pre + "NetMender", "LOCALID_SESTOS_NET_MENDER",
            "MOVEMENT_TYPE_FACE_DOWN"),
        obj("OBJ_EVENT_GFX_ICHOR_KID_M", 7, 19, pre + "Kid", "LOCALID_SESTOS_KID",
            "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=2),
        obj("OBJ_EVENT_GFX_ICHOR_UPTURNED_BOAT_L", 24, 17, "0x0", None, "MOVEMENT_TYPE_NONE"),
        obj("OBJ_EVENT_GFX_ICHOR_UPTURNED_BOAT_R", 25, 17, "0x0", None, "MOVEMENT_TYPE_NONE"),
        # the point and the upper town
        obj("OBJ_EVENT_GFX_ICHOR_ELDER_F", 29, 27, pre + "TowerWatcher", "LOCALID_SESTOS_TOWER_WATCHER",
            "MOVEMENT_TYPE_FACE_LEFT"),
        obj("OBJ_EVENT_GFX_ICHOR_ELDER_M", 20, 10, pre + "HermElder", "LOCALID_SESTOS_HERM_ELDER",
            "MOVEMENT_TYPE_FACE_LEFT"),
        obj("OBJ_EVENT_GFX_ICHOR_HOPLITE", 15, 6, pre + "GateGuard", "LOCALID_SESTOS_GATE_GUARD",
            "MOVEMENT_TYPE_FACE_DOWN"),
        obj("OBJ_EVENT_GFX_ICHOR_YOUTH_F", 3, 9, pre + "Gardener", "LOCALID_SESTOS_GARDENER",
            "MOVEMENT_TYPE_FACE_UP"),
        item_ball(18, 1, "ITEM_STAR_PIECE", "FLAG_ICHOR_ITEM_SESTOS_STAR_PIECE"),
    ]
    warps = [
        warp(ASC[0] + 1, ASC[1] + 3, "MAP_SESTOS_ASCLEPEION", 0),
        warp(AGO[0] + 1, AGO[1] + 3, "MAP_SESTOS_AGORA", 0),
        warp(TOWER[0], TOWER[1] + 4, "MAP_SESTOS_HEROS_TOWER", 0),
        warp(FERRY[0] + 1, FERRY[1] + 2, "MAP_SESTOS_FERRY_HOUSE", 0),
        warp(LOFT[0] + 1, LOFT[1] + 3, "MAP_SESTOS_NET_LOFT", 0),
    ]
    coords = [
        trigger(8, 23, "VAR_TEMP_1", 0, pre + "AletheaY23"),
        trigger(8, 24, "VAR_TEMP_1", 0, pre + "AletheaY24"),
    ]
    bgs = [
        sign(16, 11, pre + "TownSign"),
        sign(8, 17, pre + "QuaySign"),
        sign(19, 9, pre + "Herm"),
        sign(TOWER[0] + 1, TOWER[1] + 4, pre + "TowerPlaque"),
        sign(17, 3, pre + "AcropolisWall"),
        sign(5, 27, pre + "RoadSign"),
        sign(29, 28, pre + "PointSign"),
        hidden(20, 24, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_SESTOS_HEART_SCALE"),
        hidden(34, 11, "ITEM_ULTRA_BALL", "FLAG_ICHOR_HIDDEN_SESTOS_ULTRA_BALL"),
    ]
    connections = [{"map": "MAP_HELLESPONT", "offset": -28, "direction": "down"}]
    return objects, warps, coords, bgs, connections


SCREENS = {
    "1_mole": (12, 24), "2_quay": (12, 16), "3_point": (29, 26), "4_herm": (18, 10),
    "5_acropolis": (17, 4), "6_road": (3, 25), "7_headland": (31, 18), "8_gardens": (5, 8),
}

# Cells the scenes walk people across.
SCRIPTED = {"Alethea": [(7, 23), (7, 24)], "Player": [(8, 23), (8, 24)]}


def check():
    errors, reach, blocks, ev = T.check_map(NAME, start=(3, H - 1), scripted=SCRIPTED, surf=True)
    errors += T.check_edge(NAME, blocks, "bottom", set(ROAD) | set(MOUTH) | set(POINT_ROAD))
    for side in ("top", "left", "right"):
        errors += T.check_edge(NAME, blocks, side, set())
    # the mole is the landing: everyone off it to the town crosses Alethea's line
    cut = blocks.copy()
    cut[23, 8] |= T.SOLID
    cut[24, 8] |= T.SOLID
    if (6, 23) in T.reachable(cut, (12, 24)):
        errors.append(f"{NAME}: the mole reaches the town without crossing Alethea's triggers")
    # the Wings' landing is open, in front of the Asclepeion's door
    if not T.walkable(blocks, *WINGS):
        errors.append(f"{NAME}: the Wings' landing {WINGS} is blocked")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    g = compose()
    T.set_layout(LAYOUT, W, H)
    T.write_layout(g, NAME, border())
    T.write_events(NAME, *events(), music="MUS_ICHOR_AKTI", weather="WEATHER_SUNNY", map_type="MAP_TYPE_TOWN")
    if args.render:
        T.render(LAYOUT, NAME, W, H, args.render, "sestos", SCREENS)
    if not args.no_check:
        errors = check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("sestos: layout and events written, checks pass")


if __name__ == "__main__":
    main()
