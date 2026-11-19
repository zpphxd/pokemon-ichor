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
    "XeniaHouse": (8, 18), "LeapersHouse": (16, 20), "KydonsHouse": (26, 18),
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
    # ---- the upper town (design round 2): houses stepped in clusters behind the street,
    # lanes winding between their courtyard walls, a fountain square, a hive wall,
    # the headland rising as a second cliff tier on the west ----
    from knossa_bull_road import rock
    m.rect(0, 16, W - 1, 23, A.GRASS, False)
    rock(m, {(x, y) for x in range(0, 5) for y in range(15, 20)} | {(5, 16), (5, 17), (5, 18), (5, 19)})
    m.olive(1, 15)
    m.cypress(3, 16)
    # courtyard and garden walls (the coping is part of the wall, never a walk)
    def low_wall(x0, x1, y, gaps=()):
        wall_run(m, x0, x1, y, solid_top=True, gaps=gaps)
    low_wall(13, 19, 17, gaps=(14,))
    low_wall(20, 23, 18)
    m.piece("wall", "spout", 21, 18)
    m.piece("wall", "top_spout", 21, 17)
    low_wall(29, 35, 18)
    for (x, n) in ((29, "R_hive_L"), (30, "R_skep"), (31, "R_hive"), (32, "R_skep"), (33, "R_hive"),
                   (34, "R_skep"), (35, "R_hive_R")):
        m.piece("house", n, x, 17)
    m.front("xenia_house", 6, 16)
    m.front("leaper_house", 15, 18)
    m.front("honey_house", 24, 16)
    for x in (15, 16):
        m.solid[18, x] = False      # the leaper house's flat roof, up its ladder
    # lanes: down from the street, round the courtyards, to the doors and the gate
    lanes = ({(x, 19) for x in range(5, 15)} | {(x, y) for x in (11, 12) for y in range(16, 19)}
             | {(x, y) for x in (13, 14) for y in (18, 20)} | {(14, 21), (13, 21)}
             | {(x, 21) for x in range(14, 22)} | {(x, y) for x in (22, 23) for y in range(16, 18)}
             | {(x, 19) for x in range(24, 29)} | {(28, y) for y in range(16, 19)}
             | {(x, 20) for x in range(24, 29)} | {(x, y) for x in GAP for y in (22, 23)})
    square = {(x, y) for x in range(19, 24) for y in (19, 20)}
    m.path(lanes - square, context=doorcells | square | plaza)
    pave(m, square, salt=6)
    # the east gardens: a terrace brow (a ledge you hop down south), steps through it
    for x in range(29, 39):
        m.set(x, 20, A.STEPS if x == 33 else A.LEDGE["S"], False)
    for (x, y) in ((36, 16), (32, 22), (37, 21)):
        m.olive(x, y)
    for (x, y) in ((24, 21), (25, 21), (5, 20), (6, 20), (9, 20), (10, 20), (30, 19), (36, 19)):
        if int(m.mid[y, x]) == A.GRASS:
            m.set(x, y, A.ANEMONE, False)
    m.cypress(1, 12)
    m.cypress(7, 12)
    m.path({(5, 12), (5, 13), (4, 14), (5, 14), (6, 14)})
    m.grass_mix(0, 12, 39, 23, salt=5)

    # ---- the town wall, following the slope's contour; the gate; olive country beyond ----
    for (x0, x1, y) in ((0, 5, 22), (5, 11, 21), (11, 17, 23), (22, 28, 23), (28, 33, 22), (33, 39, 21)):
        wall_run(m, x0, x1, y, solid_top=True)
    m.set(22, 21, A.STELE, True)
    m.rect(0, 24, W - 1, H - 1, A.GRASS, False)
    road = ({(x, y) for x in GAP for y in (24, 25, 28, 29)} | {(x, y) for x in range(17, 21) for y in (26, 27)})
    m.path(road)
    # olive groves in staggered clumps either side of the road, never in rows
    for (x, y) in ((0, 24), (3, 24), (2, 26), (7, 25), (0, 28), (5, 28), (9, 27), (11, 25), (13, 28),
                   (25, 25), (24, 28), (27, 27), (29, 24), (31, 26), (30, 28), (33, 28), (34, 24),
                   (36, 26), (38, 24), (38, 28)):
        m.olive(x, y)
    for (x, y) in ((5, 24), (15, 25), (23, 26), (33, 25)):
        m.cypress(x, y)
    m.cypress(16, 24)
    m.cypress(22, 25)
    m.grass_mix(0, 24, W - 1, H - 1, salt=9)
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
    # by the ladder house, out of the gap that leads south to the Bull Road
    m.obj("ICHOR_KID_F", 16, 21, P + "Girl", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_AMNISOS_GIRL")
    m.obj("SPECIES(MELIBEE)", 15, 21, P + "Bombos", "MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_AMNISOS_BOMBOS")
    m.obj("ICHOR_ELDER_F", 6, 13, P + "OldWoman", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_AMNISOS_OLD_WOMAN")
    m.obj("ICHOR_HEALER", 3, 11, P + "Gennaia", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_AMNISOS_GENNAIA")
    m.obj("ICHOR_KID_M", 33, 19, P + "Kid", "MOVEMENT_TYPE_WANDER_AROUND", local_id="LOCALID_AMNISOS_KID",
          rx=2, ry=1)
    m.obj("ICHOR_FISHER", 32, 12, P + "NetMender", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_AMNISOS_NETMENDER")
    m.obj("ICHOR_WOMAN", 27, 15, P + "SaffronGirl", "MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT",
          local_id="LOCALID_AMNISOS_SAFFRON", rx=3)
    m.item_ball(6, 4, "ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_AMNISOS_MAX_REPEL")
    m.item_ball(15, 18, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_AMNISOS_HYPER_POTION")
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
            views=[(15, 7), (30, 6), (5, 8), (9, 18), (20, 18), (31, 18), (19, 25)],
            blockers=[(3, 11)])
    return m


def _const(k):
    import re
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", k).upper()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stem", default="knossa_amnisos")
    build(ap.parse_args().stem)
