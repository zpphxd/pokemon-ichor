#!/usr/bin/env python3
"""Build Ilion (aethos + troas): Troy, its events, and its checks.

Writes data/layouts/Ilion/map.bin and border.bin (48 x 42) and the events in
data/maps/Ilion/map.json, then checks them.

The city (OIKOUMENE.md §4.1; MAPS_troad.md): Priam's citadel, the Pergamos, holds
the top of the hill inside its great sloping walls of pale limestone; the temple
of Athena is its crown, Priam's megaron and Cassandra's room beside it. The
Skaian Gate stands at the west end of the wall, barred (its hall is batch 2's),
with the oak and the twin springs below it. The open ramp gate leads up from the
lower town, where the road from the Skamander Plain (west) and the Ida Road
(east) cross the main street.

Doors (BUILD.md §5): warp 0 Asclepeion, 1 Agora, 2 Priam's palace, 3 Cassandra's
room, 4 the pilgrims' guest-room, 5 the horse-breeder's stable, 6 the mason's
house, 7 the peplos-weaver's, 8 the temple of Athena, each to its room's warp 0.

Seams, both left open for batch 2 (MAPS_troad.md, "Seams"):
  west (x = 0)  the Skamander Plain: rows 30-33 open; x 0-7 aethos only
  east (x = 47) the Ida Road: rows 30-33 open; x 40-47 aethos only

Usage: /usr/bin/python3 tools/ichor/maps/ilion.py [--render DIR] [--no-check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import troad_lib as T  # noqa: E402
from sestos import house  # noqa: E402
from troad_lib import (AGORA, ASCLEPEION, OLIVE_BOT_TIP, OLIVE_TOP, STELE, Grid, hidden, item_ball,  # noqa: E402
                       obj, paint, sign, warp)

W, H = 48, 42
NAME = "Ilion"
LAYOUT = "LAYOUT_ILION"
GATE_ROWS = range(30, 34)        # open on both the west and east edges
STRIP = 8                        # aethos-only columns at each gated edge
WALL_Y = 13                      # the great wall's top row (rows 13-15)
TEMPLE = (21, 1)                 # door (23, 5)
PALACE = (11, 5)                 # door (13, 8)
CASSANDRA = (30, 6)              # 3 x 3, door (31, 8)
SKAIAN = (10, 12)                # 4 x 4, its doors (11, 15) and (12, 15)
RAMP = (26, 13)                  # 4 x 3, the passage x 27-28
ASC = (9, 26)                    # door (10, 29)
AGO = (14, 26)                   # door (15, 29)
GUEST = (33, 26)                 # 4 x 3, door (34, 28)
STABLE = (9, 35)                 # 4 x 3, stable door (10, 37)
MASON = (33, 18)                 # 3 x 3, door (34, 20)
WEAVER = (18, 20)                # 4 x 3, door (19, 22)
WINGS = (10, 30)                 # the Wings' landing, outside the Asclepeion


def plan():
    P = [["g"] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                P[y][x] = ch

    # ---- the citadel --------------------------------------------------------
    fill(19, 6, 27, 7, "q")              # the temple's forecourt, paved in ashlar
    fill(13, 9, 34, 10, "p")             # the citadel's street, palace to Cassandra
    fill(27, 8, 28, 12, "p")             # down to the ramp gate
    fill(13, 8, 13, 8, "p")
    fill(31, 9, 31, 9, "p")
    fill(16, 11, 24, 12, "p")            # the drill yard
    # ---- the lower town --------------------------------------------------------
    fill(27, 16, 28, 38, "p")            # the main street, ramp gate to the south gardens
    fill(0, 31, 47, 32, "p")             # the street from the plain to the Ida Road
    fill(24, 29, 31, 34, "q")            # the crossroads square, paved
    fill(6, 17, 26, 17, "p")             # the lane under the wall, to the Skaian Gate
    fill(10, 16, 13, 16, "p")
    fill(10, 30, 15, 30, "p")            # in front of the Asclepeion and Agora
    fill(19, 23, 26, 23, "p")            # to the weaver's
    fill(29, 21, 34, 21, "p")            # to the mason's
    fill(34, 29, 34, 30, "p")            # to the guest-room
    fill(14, 33, 14, 34, "p")            # into the horse yard
    # fields and gardens in the lower town's south (wheat stands clear of the
    # aethos-only strips)
    fill(18, 35, 25, 38, "W")
    fill(30, 35, 38, 37, "W")
    fill(31, 38, 36, 38, "W")
    fill(34, 22, 38, 24, "t")
    fill(9, 23, 11, 24, "t")             # a walled kitchen garden by the springs
    fill(30, 24, 31, 27, "t")            # the mason's wife's beans
    return P


def compose():
    g = Grid(W, H)
    P = plan()
    paint(g, P)
    k = lambda key, part: g.cat[key]["names"][part][0]

    # ---- the citadel's walls ---------------------------------------------------
    # the north-south walls (west x 8, east x 39), rows 2-12, then the corners
    for y in range(0, WALL_Y):
        g.part("wall_ns", "ns_W", 8, y)
        g.part("wall_ns", "ns_E", 39, y)
    g.put("wall_ns", 8, WALL_Y, cx=k("wall_ns", "corner_W"), w=1)
    g.put("wall_ns", 39, WALL_Y, cx=k("wall_ns", "corner_E"), w=1)
    for x in range(9, 39):
        part = "offset" if x in (16, 23, 32, 36) else "run"
        g.put("wall", x, WALL_Y, cx=k("wall", part), w=1)
    g.put("tower", 18, WALL_Y - 1)
    g.put("tower", 34, WALL_Y - 1)
    g.put("gateway", *RAMP)
    g.put("skaian_gate", *SKAIAN)
    # ---- inside: the temple, the palace, Cassandra's room, the drill yard -----
    g.put("temple_athena", *TEMPLE)
    g.put("priams_palace", *PALACE)
    house(g, CASSANDRA[0], CASSANDRA[1], 3, rows=("roof", "up_shutters", "door"), white=True)
    g.trees(cypresses=((19, 1), (27, 1), (20, 3), (26, 3), (17, 5), (29, 4), (10, 2), (37, 2)),
            olives=((14, 1), (31, 1), (34, 4), (11, 10), (35, 10), (9, 6)),
            pines=((16, 2), (35, 7)))
    g.part("yard", "blocks", 16, 7)              # the Palladion's old pedestal stones
    g.set(25, 11, STELE, True)                   # THE PERGAMOS (inside)
    g.scatter([(18, 5), (28, 5), (33, 9), (12, 4), (36, 12), (24, 8)])
    # ---- outside the walls, the hillside to the west and east (aethos only) ----
    g.forest(0, 0, 7, 16, salt=1, aethos=True)
    g.forest(40, 0, 47, 16, salt=2, aethos=True)
    g.forest(9, 0, 38, 0, salt=3)
    # ---- the lower town ---------------------------------------------------------
    # the Skaian Gate's oak and the twin springs where the washing was done
    g.put("oak", 14, 18)
    g.put("springs", 8, 19)
    g.set(7, 17, STELE, True)                    # THE SKAIAN GATE
    # the Asclepeion and the Agora, facing the road in from the plain
    g.block(ASCLEPEION, *ASC)
    g.set(ASC[0] + 1, ASC[1] + 3, ASCLEPEION[3][1], False)
    g.block(AGORA, *AGO)
    g.set(AGO[0] + 1, AGO[1] + 3, AGORA[3][1], False)
    # the weaver's, the mason's, the guest-room
    house(g, WEAVER[0], WEAVER[1], 4, rows=("roof", "up_window", "door"))
    g.part("yard", "dye_vats", 22, 22)
    house(g, MASON[0], MASON[1], 3, rows=("roof", "up_window", "door"), white=True)
    g.part("yard", "blocks", 36, 20)
    g.part("yard", "drums", 37, 19)
    g.part("yard", "drums", 31, 19)
    house(g, GUEST[0], GUEST[1], 4, rows=("roof", "up_shutters", "door"), white=True,
          roof_parts=("roof_W", "roof_jars", "roof_E"))
    # the horse-breeder's yard: the stable, its walled paddock, hay, trough, chariot
    house(g, STABLE[0], STABLE[1], 4, rows=("roof", "up_window", "stable_door"))
    g.wall_we(8, 16, 34)
    g.set(14, 34, T.PATH["c"], False)            # the yard's gate
    g.wall_ns(8, 35, 40, "w")
    g.wall_ns(16, 35, 40, "e")
    g.wall_we(8, 16, 40)
    g.part("yard", "hay", 15, 35)
    g.part("yard", "trough", 15, 38)
    g.part("yard", "chariot_W", 11, 39)
    g.part("yard", "chariot_E", 12, 39)
    # the crossroads: the town's sign, a tripod
    g.set(23, 30, STELE, True)                   # ILION
    g.block([[T.TRIPOD[0]], [T.TRIPOD[1]]], 31, 28)
    g.solid[28, 31] = False
    # gates: signs at the plain road and the Ida Road
    g.set(4, 30, STELE, True)                    # to the Skamander Plain
    g.set(43, 33, STELE, True)                   # to the Ida Road
    # the kitchen garden's low walls, open to the lane on the south
    g.wall_we(8, 12, 22)
    g.wall_ns(8, 23, 24, "w")
    g.wall_ns(12, 23, 24, "e")
    # a cypress avenue up the main street to the ramp gate
    for y in (18, 21, 24):
        g.trees(cypresses=((26, y), (29, y)))
    # trees and gardens of the lower town
    g.trees(olives=((20, 26), (37, 30), (22, 18), (38, 18), (1, 23), (45, 22), (3, 36), (44, 37)),
            cypresses=((17, 18), (25, 20), (32, 26), (38, 26), (18, 24), (13, 22),
                       (21, 29), (36, 33), (22, 33), (19, 33), (39, 23), (6, 26), (7, 22)),
            pines=((40, 25), (2, 27)), oaks=((22, 26),))
    g.forest(0, 17, 7, 29, salt=4, aethos=True)
    g.forest(40, 17, 47, 29, salt=5, aethos=True)
    g.forest(0, 34, 7, 41, salt=6, aethos=True)
    g.forest(40, 34, 47, 41, salt=7, aethos=True)
    g.forest(17, 39, 26, 41, salt=8)
    g.forest(29, 39, 39, 41, salt=9)
    g.forest(27, 39, 28, 41, salt=11)
    g.forest(8, 41, 16, 41, salt=10)
    g.scatter([(12, 24), (24, 21), (31, 23), (37, 27), (16, 33), (39, 32), (26, 35), (29, 37),
               (8, 24), (20, 31), (35, 34)])
    g.scatter([(23, 24), (30, 27), (17, 31), (36, 39)], ["chamomile", "stones", "dry_tuft"])
    return g


def border():
    return [OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]]


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def events():
    pre = "Ilion_EventScript_"
    hop = "OBJ_EVENT_GFX_ICHOR_HOPLITE"        # ICHOR_STUB_SPRITE: OBJ_EVENT_GFX_ICHOR_TROJAN_HOPLITE
    man = "OBJ_EVENT_GFX_ICHOR_MAN"            # ICHOR_STUB_SPRITE: OBJ_EVENT_GFX_ICHOR_TROJAN_M
    woman = "OBJ_EVENT_GFX_ICHOR_WOMAN"        # ICHOR_STUB_SPRITE: OBJ_EVENT_GFX_ICHOR_TROJAN_F
    objects = [
        # the Skaian Gate's guard (ICHOR_STUB_HALL)
        obj(hop, 13, 16, pre + "SkaianGuard", "LOCALID_ILION_SKAIAN_GUARD", "MOVEMENT_TYPE_FACE_DOWN"),
        # the drill yard: two hoplites at practice, a trainer each
        obj(hop, 17, 11, pre + "Agenor", "LOCALID_ILION_AGENOR", "MOVEMENT_TYPE_FACE_RIGHT",
            trainer="TRAINER_TYPE_NORMAL", sight=3),
        obj(hop, 23, 12, pre + "Polites", "LOCALID_ILION_POLITES", "MOVEMENT_TYPE_FACE_LEFT",
            trainer="TRAINER_TYPE_NORMAL", sight=3),
        # the horse yard's charioteer, and a shepherd in from Ida by the east road
        obj(hop, 13, 37, pre + "Hippothoos", "LOCALID_ILION_HIPPOTHOOS", "MOVEMENT_TYPE_FACE_LEFT",
            trainer="TRAINER_TYPE_NORMAL", sight=2),
        obj("OBJ_EVENT_GFX_ICHOR_SHEPHERD", 38, 33, pre + "Anchises", "LOCALID_ILION_ANCHISES",
            "MOVEMENT_TYPE_FACE_UP", trainer="TRAINER_TYPE_NORMAL", sight=1),
        # people
        obj(woman, 10, 20, pre + "Washerwoman", "LOCALID_ILION_WASHERWOMAN", "MOVEMENT_TYPE_FACE_UP"),
        obj("OBJ_EVENT_GFX_ICHOR_ELDER_F", 12, 21, pre + "Grandmother", "LOCALID_ILION_GRANDMOTHER",
            "MOVEMENT_TYPE_FACE_LEFT"),
        obj(man, 26, 31, pre + "Crier", "LOCALID_ILION_CRIER", "MOVEMENT_TYPE_FACE_DOWN"),
        obj("OBJ_EVENT_GFX_ICHOR_KID_M", 29, 33, pre + "Kid", "LOCALID_ILION_KID",
            "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1),
        obj("OBJ_EVENT_GFX_ICHOR_ELDER_M", 24, 9, pre + "Veteran", "LOCALID_ILION_VETERAN",
            "MOVEMENT_TYPE_FACE_DOWN"),
        obj("OBJ_EVENT_GFX_ICHOR_PRIESTESS", 22, 7, pre + "Priestess", "LOCALID_ILION_PRIESTESS",
            "MOVEMENT_TYPE_FACE_DOWN"),
        obj(woman, 20, 24, pre + "Spinner", "LOCALID_ILION_SPINNER", "MOVEMENT_TYPE_FACE_UP"),
        obj(man, 30, 21, pre + "Quarryman", "LOCALID_ILION_QUARRYMAN", "MOVEMENT_TYPE_FACE_RIGHT"),
        obj("OBJ_EVENT_GFX_ICHOR_YOUTH_M", 2, 31, pre + "Traveler", "LOCALID_ILION_TRAVELER",
            "MOVEMENT_TYPE_FACE_RIGHT"),
        obj(hop, 28, 17, pre + "RampGuard", "LOCALID_ILION_RAMP_GUARD", "MOVEMENT_TYPE_FACE_DOWN"),
        item_ball(36, 23, "ITEM_HARD_STONE", "FLAG_ICHOR_ITEM_ILION_HARD_STONE"),
        item_ball(37, 11, "ITEM_PP_UP", "FLAG_ICHOR_ITEM_ILION_PP_UP"),
        item_ball(9, 12, "ITEM_ELIXIR", "FLAG_ICHOR_ITEM_ILION_ELIXIR"),
    ]
    warps = [
        warp(ASC[0] + 1, ASC[1] + 3, "MAP_ILION_ASCLEPEION", 0),
        warp(AGO[0] + 1, AGO[1] + 3, "MAP_ILION_AGORA", 0),
        warp(PALACE[0] + 2, PALACE[1] + 3, "MAP_ILION_PRIAMS_PALACE", 0),
        warp(CASSANDRA[0] + 1, CASSANDRA[1] + 2, "MAP_ILION_CASSANDRAS_ROOM", 0),
        warp(GUEST[0] + 1, GUEST[1] + 2, "MAP_ILION_GUEST_ROOM", 0),
        warp(STABLE[0] + 1, STABLE[1] + 2, "MAP_ILION_HORSE_STABLE", 0),
        warp(MASON[0] + 1, MASON[1] + 2, "MAP_ILION_MASONS_HOUSE", 0),
        warp(WEAVER[0] + 1, WEAVER[1] + 2, "MAP_ILION_WEAVERS_HOUSE", 0),
        warp(TEMPLE[0] + 2, TEMPLE[1] + 4, "MAP_ILION_TEMPLE_OF_ATHENA", 0),
    ]
    bgs = [
        sign(23, 30, pre + "TownSign"),
        sign(4, 30, pre + "PlainSign"),
        sign(43, 33, pre + "IdaSign"),
        sign(7, 17, pre + "SkaianSign"),
        sign(SKAIAN[0] + 1, SKAIAN[1] + 3, pre + "SkaianDoors"),
        sign(SKAIAN[0] + 2, SKAIAN[1] + 3, pre + "SkaianDoors"),
        sign(25, 11, pre + "PergamosSign"),
        sign(8, 19, pre + "WarmSpring"),
        sign(9, 19, pre + "ColdSpring"),
        sign(16, 7, pre + "PalladionStones"),
        hidden(15, 19, "ITEM_LEAF_STONE", "FLAG_ICHOR_HIDDEN_ILION_LEAF_STONE"),
        hidden(39, 15, "ITEM_REVIVAL_HERB", "FLAG_ICHOR_HIDDEN_ILION_REVIVAL_HERB"),
        hidden(9, 39, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ILION_STAR_PIECE"),
    ]
    return objects, warps, [], bgs, None


SCREENS = {
    "1_west_gate": (5, 31), "2_asclepeion": (12, 30), "3_springs": (11, 19), "4_skaian": (12, 17),
    "5_ramp": (27, 17), "6_drill_yard": (20, 11), "7_temple": (23, 7), "8_cassandra": (31, 10),
    "9_crossroads": (27, 31), "10_mason": (33, 21), "11_guest": (35, 30), "12_horse_yard": (12, 36),
    "13_fields": (27, 37), "14_east_gate": (42, 31),
}


def check():
    errors, reach, blocks, ev = T.check_map(
        NAME, start=(0, 31),
        seams=(("cols", range(0, STRIP), "Skamander Plain (west)"),
               ("cols", range(W - STRIP, W), "Ida Road (east)")))
    errors += T.check_edge(NAME, blocks, "left", set(GATE_ROWS))
    errors += T.check_edge(NAME, blocks, "right", set(GATE_ROWS))
    errors += T.check_edge(NAME, blocks, "top", set())
    errors += T.check_edge(NAME, blocks, "bottom", set())
    if (W - 1, 31) not in reach:
        errors.append(f"{NAME}: the Ida Road can't be reached from the plain's gate")
    if not T.walkable(blocks, *WINGS):
        errors.append(f"{NAME}: the Wings' landing {WINGS} is blocked")
    # the Skaian Gate is shut: its door cells are solid until the hall opens
    for x in (SKAIAN[0] + 1, SKAIAN[0] + 2):
        if T.walkable(blocks, x, SKAIAN[1] + 3):
            errors.append(f"{NAME}: the Skaian Gate's door ({x},{SKAIAN[1] + 3}) is open")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    g = compose()
    T.set_layout(LAYOUT, W, H)
    T.write_layout(g, NAME, border())
    T.write_events(NAME, *events(), music="MUS_ICHOR_EMPORION", weather="WEATHER_SUNNY",
                   map_type="MAP_TYPE_CITY")
    if args.render:
        T.render(LAYOUT, NAME, W, H, args.render, "ilion", SCREENS)
    if not args.no_check:
        errors = check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("ilion: layout and events written, checks pass")


if __name__ == "__main__":
    main()
