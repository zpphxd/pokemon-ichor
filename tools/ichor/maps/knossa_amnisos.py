#!/usr/bin/env python3
"""Amnisos, the harbor of Knossa (design/maps/KnossaAmnisos.md; SCRIPT.md III-3A,
III-4, Part 2; LABYRINTH.md §2).

    python3 tools/ichor/maps/knossa_amnisos.py [--stem knossa_amnisos_passN]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knossa_maps import A, Map, ensure_map, pave, quay, wall_run  # noqa: E402

NAME, W, H = "KnossaAmnisos", 40, 30
P = "KnossaAmnisos_EventScript_"

# doors: (x, y) on this map -> interior
DOORS = {
    "Asclepeion": (10, 13), "Agora": (16, 13), "Tavern": (26, 13), "FishersHut": (34, 12),
    "XeniaHouse": (11, 19), "LeapersHouse": (17, 19), "KydonsHouse": (24, 19),
}
GAP = range(18, 22)          # the south gap in the town wall, onto the Bull Road


def build(stem):
    ensure_map(NAME, W, H, "amnisos", "MAP_TYPE_TOWN", "MAPSEC_AMNISOS", "MUS_ICHOR_AKTI")
    m = Map(NAME, "amnisos", W, H, fill=A.SEA)
    m.border = [A.SEA] * 4

    # ---- the headland in the west: a limestone bluff, the cave in its south face ----
    m.rect(0, 0, 7, 8, A.GRASS, False)
    for y in range(0, 9):
        m.piece("cliff", "side_E", 8, y)
    m.piece("cliff", "lip_L", 0, 9)
    for x in range(1, 8):
        m.piece("cliff", "lip" if x % 3 else "lip_b", x, 9)
    m.piece("cliff", "lip_R", 8, 9)
    for y in (10, 11):
        m.piece("cliff", "face_L", 0, y)
        for x in range(1, 8):
            m.piece("cliff", "face" if (x + y) % 3 else "face_b", x, y)
        m.piece("cliff", "face_R", 8, y)
    m.put("cave_mouth", 2, 9)
    m.olive(1, 1)
    m.olive(4, 0)
    m.cypress(0, 4)
    m.cypress(7, 5)
    m.set(6, 2, A.STELE, True)
    m.grass_mix(0, 0, 7, 8, salt=3)
    m.path({(5, 8), (5, 7), (6, 7), (6, 6), (5, 6), (4, 6), (4, 5), (3, 5), (3, 4)})
    m.raise_ground({(x, y) for x in range(0, 8) for y in range(0, 9)}, 4, joins={(5, 9), (5, 10), (5, 11)})

    # ---- the harbor: quay, jetty, the mole with the Titan ships, the beach ----
    quay_mask = {(x, y) for x in range(9, 22) for y in range(6, 10)}
    quay_mask |= {(x, y) for x in range(13, 16) for y in range(1, 6)}       # the jetty
    quay_mask |= {(x, y) for x in range(20, 23) for y in range(3, 10)}      # the mole's root
    quay_mask |= {(x, y) for x in range(20, 38) for y in range(3, 6)}       # the mole
    quay(m, quay_mask, land={(8, y) for y in range(0, 12)})
    pave(m, [(x, y) for x in range(10, 21) for y in range(7, 10)], salt=1)
    pave(m, [(14, y) for y in range(2, 6)], salt=2)
    m.piece("quay", "N_plank", 17, 6)
    m.piece("kaiki", "afloat", 11, 4)
    m.piece("kaiki", "afloat", 18, 3)
    m.put("titan_trireme", 22, 0)
    m.put("titan_trireme", 30, 0)
    for (x, y, g) in ((10, 9, "amphorae"), (12, 7, "bollard"), (19, 7, "bollard"), (20, 9, "crate"),
                      (21, 4, "rope"), (37, 4, "oars")):
        m.piece("gear", g, x, y)
    m.piece("shrine", "top", 15, 8)
    m.piece("shrine", "base", 15, 9)
    # the basin between the mole and the beach, and the beach
    rows = []
    for y in range(6, 14):
        rows.append("".join("~" if y < 9 or (y == 9 and x > 34) else "#" for x in range(23, 40)))
    m.shore(rows, 23, 6)
    for (x, y, d) in ((25, 10, "shells"), (30, 12, "wrack"), (37, 11, "lace"), (31, 10, "footprints"),
                      (28, 12, "sherd_dig")):
        m.piece("sand_decor", d, x, y)
    m.piece("kaiki", "beached", 29, 10)
    m.piece("kaiki", "beached", 37, 12)
    m.piece("gear", "nets", 31, 11)

    # ---- the harbor terrace: Asclepeion and Agora facing the quay, the tavern, the hut ----
    m.rect(9, 10, 22, 13, A.GRASS, False)
    m.block(A.ASCLEPEION, 9, 10)
    m.block(A.AGORA, 15, 10)
    m.front("tavern", 24, 11)
    m.front("fisher_hut", 33, 11)
    m.rect(0, 12, 8, 13, A.GRASS, False)

    # ---- the town: a street along the slope, houses with hives on every roof ----
    m.rect(0, 14, W - 1, 21, A.GRASS, False)
    street = {(x, y) for x in range(4, 40) for y in (14, 15)}
    street |= {(x, 13) for x in (13, 14, 19, 20, 21, 22)} | {(x, y) for x in (13, 14) for y in (10, 11, 12)}
    street |= {(x, y) for x in (19, 20, 21, 22) for y in (10, 11, 12)}
    street |= {(11, 13), (16, 13), (10, 13), (12, 13), (15, 13), (17, 13), (26, 13), (25, 13), (27, 13)}
    street |= {(5, 12), (5, 13), (4, 13), (6, 13), (6, 12), (9, 13)}
    doorcells = set(DOORS.values())
    plaza = {(x, y) for x in range(8, 24) for y in range(13, 16)} - doorcells
    m.path(street - doorcells - plaza, context=doorcells | plaza)
    pave(m, plaza, salt=4)
    m.set(8, 13, A.HERM, True)
    for (x, y) in ((7, 15), (7, 16), (24, 16), (25, 16), (12, 16), (19, 16), (26, 16), (27, 16)):
        if int(m.mid[y, x]) == A.GRASS:
            m.set(x, y, A.ANEMONE, False)
    wall_run(m, 8, 27, 17, solid_top=False, gaps=(14, 15, 20, 21))
    for x in range(8, 28):
        if x not in (14, 15, 20, 21):
            m.solid[16, x] = True       # the coping is the wall's own top, not a walk
    m.front("xenia_house", 9, 17)
    m.front("leaper_house", 16, 17)
    m.front("honey_house", 22, 17)
    # the leaper house's flat roof: up the ladder, a walk along the roof
    for x in (16, 17):
        m.solid[17, x] = False
    lanes = {(x, y) for x in range(6, 31) for y in (20, 21)} | {(x, y) for x in (14, 15, 20, 21)
                                                                  for y in (16, 17, 18, 19)}
    m.path(lanes | {(x, 22) for x in GAP} | {(x, 23) for x in GAP}, context=doorcells)
    # the cave path's foot, and the west end of town
    m.cypress(1, 12)
    m.cypress(7, 12)
    m.path({(5, 12), (5, 13), (4, 14), (5, 14), (6, 14)})
    m.olive(0, 15)
    m.olive(2, 18)
    m.grass_mix(0, 12, 8, 21, salt=5)
    # the hive garden in the east: olives over the beach road
    for (x, y) in ((31, 16), (35, 17), (33, 19), (37, 15), (29, 18)):
        m.olive(x, y)
    m.grass_mix(28, 16, 39, 21, salt=7)

    # ---- the town wall and the south gap; the olive country beyond (aethos only) ----
    wall_run(m, 0, W - 1, 23, solid_top=True, gaps=tuple(GAP))
    m.set(22, 21, A.STELE, True)
    m.rect(0, 24, W - 1, H - 1, A.GRASS, False)
    road = {(x, y) for x in GAP for y in range(22, H)}
    m.path(road)
    for (x, y) in ((1, 25), (5, 24), (9, 26), (13, 24), (15, 27), (2, 28), (24, 25), (28, 24), (32, 26),
                   (36, 24), (25, 28), (34, 28), (11, 28), (38, 27)):
        m.olive(x, y)
    m.cypress(17, 25)
    m.cypress(22, 25)
    m.grass_mix(0, 24, W - 1, H - 1, salt=9)
    for (x, y) in ((3, 21), (35, 21), (8, 21), (30, 20)):
        m.set(x, y, A.BOULDER_GRASS, True)
    for (x, y) in ((29, 14), (33, 15), (38, 14)):
        m.set(x, y, A.ANEMONE, False)
    m.seam("down")

    # ---- events --------------------------------------------------------------------------
    warp_ids = {}
    for k, (x, y) in DOORS.items():
        warp_ids[k] = m.warp(x, y, f"MAP_KNOSSA_AMNISOS_{_const(k)}", 0)
    m.connect("down", 5, "MAP_KNOSSA_BULL_ROAD")

    m.obj("ICHOR_SAILOR", 17, 7, P + "Nausikles", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_NAUSIKLES_AMNISOS", local_id="LOCALID_AMNISOS_NAUSIKLES")
    m.obj("ICHOR_ALETHEA", 18, 8, P + "Alethea", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_ALETHEA_AMNISOS_QUAY", local_id="LOCALID_AMNISOS_ALETHEA")
    m.obj("ICHOR_TITAN_GRUNT", 27, 4, P + "Veteran", "MOVEMENT_TYPE_FACE_UP",
          flag="FLAG_ICHOR_HIDE_AMNISOS_VETERAN", local_id="LOCALID_AMNISOS_VETERAN")
    m.obj("ICHOR_FISHER", 19, 9, P + "Sailor", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_AMNISOS_SAILOR")
    m.obj("ICHOR_KID_F", 18, 20, P + "Girl", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_AMNISOS_GIRL")
    m.obj("SPECIES(MELIBEE)", 19, 20, P + "Bombos", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_AMNISOS_BOMBOS")
    m.obj("ICHOR_ELDER_F", 6, 13, P + "OldWoman", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_AMNISOS_OLD_WOMAN")
    m.obj("ICHOR_HEALER", 3, 11, P + "Gennaia", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_AMNISOS_GENNAIA")
    m.obj("ICHOR_KID_M", 33, 18, P + "Kid", "MOVEMENT_TYPE_WANDER_AROUND", local_id="LOCALID_AMNISOS_KID",
          rx=2, ry=1)
    m.obj("ICHOR_FISHER", 32, 12, P + "NetMender", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_AMNISOS_NETMENDER")
    m.obj("ICHOR_WOMAN", 27, 15, P + "SaffronGirl", "MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT",
          local_id="LOCALID_AMNISOS_SAFFRON", rx=3)
    m.item_ball(6, 4, "ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_AMNISOS_MAX_REPEL")
    m.item_ball(16, 17, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_AMNISOS_HYPER_POTION")
    m.hidden(14, 2, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_AMNISOS_PEARL")
    m.hidden(15, 8, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_AMNISOS_OBOL")
    m.sign(16, 9, P + "Shrine")
    m.sign(22, 21, P + "SouthSign")
    m.sign(6, 2, P + "CaveSign")
    m.set(21, 9, A.STELE, True)
    m.sign(21, 9, P + "QuaySign")
    m.header = {"weather": "WEATHER_SUNNY"}

    m.build(stem, starts=[(16, 7)],
            must_reach=[(14, 2, "the jetty's end"), (6, 5, "the cave path's top")],
            views=[(15, 7), (30, 6), (5, 8), (16, 15), (30, 16), (19, 25)],
            blockers=[(3, 11)])
    return m


def _const(k):
    import re
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", k).upper()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stem", default="knossa_amnisos")
    build(ap.parse_args().stem)
