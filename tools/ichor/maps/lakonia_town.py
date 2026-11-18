"""Lakonia: Sparta as Thucydides saw it (design/maps/Lakonia.md).

Five villages run together on the valley floor with no wall anywhere: plain
houses round beaten yards, plane trees between, the dark wall of Taygetos on
the west, the Eurotas on the east with the plain stone bridge the road comes
in by. The agora in the middle has the Persian Stoa, the chained Enyalios, the
Lesche and the mess hall; the battle school is the town's crown in the north-
west, its ring and yard under the mountain; the palaestra and the training
fields are north-east; Artemis Orthia keeps the marshy bank by the bridge;
Lampito's house is at the west end, against the rock. Across the river, on its
ridge, the Menelaion.

Warp order is the rooms' contract (tools/ichor/maps/lakonia_rooms.py):
0 Asclepeion, 1 Agora, 2 Lampito, 3 Gylippos, 4 syssition, 5 agoge,
6 palaestra, 7 Orthia, 8 Chilon, 9 Lichas.
"""
from __future__ import annotations

from lakonia_maps import A, LMap

W, H = 52, 42
ENTRY_ROW = 37               # Route 25 comes in on rows 36..38 at the east edge
EAST_SEAM_ROWS = range(ENTRY_ROW - 3, H)   # rows Route 25 overlaps (aethos only, x >= 44)


def river_cols(y):
    a = 38 + (1 if 9 <= y <= 17 else 0) - (1 if 25 <= y <= 31 else 0)
    b = 42 + (1 if 5 <= y <= 13 else 0) - (1 if y >= 34 else 0)
    return a, b


def land():
    g = [["." for _ in range(W)] for _ in range(H)]

    def fill(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = c

    def put(cells, c):
        for (x, y) in cells:
            if 0 <= x < W and 0 <= y < H:
                g[y][x] = c
    fill(0, 0, 3, H - 1, "M")                      # Taygetos, the west wall
    fill(4, 0, 23, 1, "M")                          # and its spur over the agoge
    for y in range(H):
        a, b = river_cols(y)
        fill(a, y, b, y, "w")
    fill(27, 0, 36, 1, "T")                         # the north woods by the gap
    fill(44, 0, W - 1, 2, "T")                      # the far bank's woods
    # ---- roads --------------------------------------------------------------------------
    fill(24, 0, 26, 16, "p")                        # north to Route 26
    fill(37, ENTRY_ROW - 1, W - 1, ENTRY_ROW + 1, "p")
    fill(25, ENTRY_ROW - 1, 36, ENTRY_ROW + 1, "p")
    fill(24, 28, 27, ENTRY_ROW + 1, "p")            # up to the agora
    fill(20, ENTRY_ROW, 23, ENTRY_ROW + 1, "p")
    fill(20, ENTRY_ROW, 22, H - 1, "p")             # the Mani road, south
    fill(15, 18, 34, 28, "p")                       # the agora
    fill(5, 22, 15, 23, "p")                        # the west lane past Gylippos
    fill(8, 23, 9, 34, "p")
    fill(8, 33, 19, 34, "p")
    fill(16, 28, 19, 33, "p")
    # ---- the training fields (north-east, the town's only tall grass) -----------------
    fields = {(x, y) for x in range(28, 37) for y in range(3, 10)}
    fields |= {(27, y) for y in range(5, 9)} | {(x, 10) for x in range(29, 35)}
    fields -= {(36, 3), (36, 4), (28, 3)}
    put(fields, "G")
    return g


def build():
    g = land()
    m = LMap("Lakonia", "lakonia", "\n".join("".join(r) for r in g))
    m.lay_plan(salt=7)
    # ---- Taygetos -----------------------------------------------------------------------
    for y in range(2, H):
        m.piece("taygetos", "side_E", 3, y)
    for x in range(4, 24):
        m.piece("taygetos", "lip_b" if x % 2 else "lip", x, 1)
        m.piece("taygetos", "pine_face" if x in (6, 13, 20) else ("face_b" if x % 2 else "face"), x, 2)
        m.piece("taygetos", "foot_b" if x % 2 else "foot", x, 3)
    m.piece("taygetos", "side_E_foot", 3, 3)
    for (x, y) in ((4, 12), (4, 29), (5, 19), (4, 38), (22, 4)):
        m.piece("taygetos", "scree", x, y)
    for (x, y) in ((4, 16), (4, 40), (4, 25), (4, 33), (4, 6)):
        m.piece("taygetos", "boulder", x, y)
    # a cleft in the rock behind the agoge's yard, choked with rubble (the Bronze Hammer)
    for (x, y) in ((1, 9), (2, 9), (2, 10), (3, 10)):
        m.piece("taygetos", "scree", x, y)
    # the agoge stands a terrace above the village: its yard drops to the lanes
    m.ledge_run(5, 9, 17)
    m.ledge_run(13, 19, 17)
    m.woods(m.cells("T"), salt=3, aethos_only=lambda x, y: x >= 44 and y in EAST_SEAM_ROWS)
    # ---- the agoge: barracks, the great yard, the ring ----------------------------------
    yard = {(x, y) for x in range(5, 23) for y in range(7, 17)}
    yard |= {(x, y) for x in range(13, 24) for y in (4, 5, 6)}
    yard -= {(5, 16), (22, 16), (22, 7), (5, 7), (6, 16)}
    m.soft("yard", yard, yard, edge_in=False)
    m.front("barracks", 6, 4)                        # door (9,6)
    m.put("ring", 12, 7)                             # (12..20, 7..15); the gap (16,15)
    m.piece("well", "well", 7, 13)
    m.part("house", "G_spears", 21, 9, 1, 1)         # a rack of practice spears in the yard
    m.part("house", "G_wood", 6, 9, 1, 1)
    # ---- the Sown Field, the wrestling sands, the palaestra -----------------------------
    m.put("sown", 30, 5, cells={(i, j) for i in range(3) for j in range(3)})
    sx, sy = 29, 12                                  # the wrestling sands (29..35, 12..14)
    for y in range(sy, sy + 3):
        for x in range(sx, sx + 7):
            v = "T" if y == sy else ("B" if y == sy + 2 else "")
            h = "L" if x == sx else ("R" if x == sx + 6 else "")
            n = (v + h) or ("C_b" if (x + y) % 4 == 0 else "C")
            if n in ("T", "B") and x == sx + 3:
                n += "_gap"
            m.piece("sands", n, x, y)
    cols = ["roof_L", "roof", "roof", "roof", "roof", "roof", "roof_R"]
    mids = ["col_L", "gap", "col", "gap", "col", "gap", "col_R"]
    base = ["base_L", "base_gap", "base_col", "door", "base_col", "base_gap", "base_R"]
    for i in range(7):                               # the palaestra's porch, door (31,17)
        m.piece("colonnade", cols[i], 28 + i, 15)
        m.piece("colonnade", mids[i], 28 + i, 16)
        m.piece("colonnade", base[i], 28 + i, 17)
    # ---- the agora ------------------------------------------------------------------------
    m.house([["RB_L", "RB_M", "RB_M", "RB_M", "RB_R"],          # the Lesche: an open porch
             ["RF_L", "RF_M", "RF_M", "RF_M", "RF_R"],
             ["P_L", "P_col", "G_open", "P_col", "P_R"]], 15, 18)
    m.front("syssition", 20, 17)                     # door (23,18)
    m.put("stoa", 27, 20)                            # the Persian Stoa (27..33, 20..25)
    m.put("enyalios", 24, 23)                        # the chained war god (24, 23..24)
    m.plane(16, 25)
    m.cypress(15, 27)
    m.cypress(34, 18) if False else None
    # ---- the civic buildings by the way in ---------------------------------------------
    m.aethos_building(A.ASCLEPEION, 28, 33)          # door (29,36)
    m.aethos_building(A.AGORA, 32, 33)               # door (33,36)
    # ---- Orthia, on the marshy bank north of the bridge ---------------------------------
    m.put("orthia", 34, 28)                          # door (35,30)
    m.set(35, 31, A.PATCH["C"], False)               # its step (the cheese altar is inside)
    m.put("willow", 32, 28)
    for (x, y) in ((37, 26), (37, 30)):
        if m.behavior(int(m.mid[y, x])) == "MB_POND_WATER":
            m.piece("river", "tuft", x, y)
    m.piece("oleander", "bush", 36, 32)
    # ---- the bridge over the Eurotas ---------------------------------------------------
    a, b = river_cols(ENTRY_ROW)
    for x in range(a - 1, b + 2):
        m.piece("bridge", "deck_W" if x == a - 1 else ("deck_E" if x == b + 1 else "deck"), x, ENTRY_ROW)
        m.piece("bridge", "face_W" if x == a - 1 else ("face_E" if x == b + 1 else "arch"), x, ENTRY_ROW + 1)
    # ---- the west village: Gylippos, Lampito, Chilon, Lichas ---------------------------
    m.front("low_house", 5, 20)                      # Gylippos, door (6,21)
    m.front("lampito", 10, 26)                       # Lampito, door (11,28)
    lyard = {(x, y) for x in range(9, 16) for y in range(29, 33)} - {(9, 32), (15, 32), (15, 29)}
    m.soft("yard", lyard, lyard, edge_in=False)
    m.piece("well", "well", 14, 30)
    m.put("burial", 5, 27)                           # the burial plot beside the house (5..7, 27..28)
    m.front("house", 5, 35)                          # Chilon, door (6,37)
    m.front("house_wide", 12, 36)                    # Lichas, door (14,39)
    cyard = {(x, y) for x in range(10, 18) for y in range(40, 42)} | {(x, 39) for x in range(16, 19)}
    m.soft("yard", cyard - m.cells("p"), cyard, edge_in=True)
    # ---- trees between the villages ------------------------------------------------------
    m.plane(10, 18)
    for (x, y) in ((5, 24), (5, 31), (24, 39), (27, 39)):
        m.olive(x, y)
    m.cypress(8, 27)
    for x in range(20, 23):                          # the Mani road's rope
        m.piece("rope", "post_L" if x == 20 else ("post_R" if x == 22 else "rope"), x, 40)
    m.set(19, 40, A.STELE, True)
    for x in range(24, 27):                          # the north road, roped until Route 26 opens
        m.piece("rope", "post_L" if x == 24 else ("post_R" if x == 26 else "rope"), x, 1)
    # ---- across the river: the Menelaion on its ridge, and olive groves ------------------
    for x in range(45, 51):
        m.piece("taygetos", "lip_b" if x % 2 else "lip", x, 12)
        m.piece("taygetos", "face_b" if x % 2 else "face", x, 13)
        m.piece("taygetos", "foot_b" if x % 2 else "foot", x, 14)
    m.set(47, 8, A.TRIPOD_TOP, False)               # Helen and Menelaos's shrine: a tripod on the ridge
    m.set(47, 9, A.TRIPOD, True)
    for (x, y) in ((45, 7), (50, 7), (45, 10), (50, 10)):
        m.cypress(x, y)
    # the far bank's olive groves, with a lane down to the river
    groves = {(x, y) for x in range(44, W) for y in range(15, H)
              if int(m.mid[y, x]) in (A.GRASS, A.SHADE) and not m.solid[y, x]
              and not (ENTRY_ROW - 1 <= y <= ENTRY_ROW + 1) and x != (47 if y < 25 else 49)
              and not (y == 25 and 47 <= x <= 49) and (x, y) not in ((44, 20), (44, 27), (44, 32), (45, 27))}
    m.woods(groves, salt=17, aethos_only=lambda x, y: x >= 44 and y in EAST_SEAM_ROWS)
    # the village south of the agora: a yard round its well, olives, a plane
    syard = {(x, y) for x in range(19, 24) for y in range(30, 35)} - {(19, 30), (19, 34)}
    m.soft("yard", syard, syard | m.cells("p"), edge_in=False)
    m.piece("well", "well", 21, 32)
    m.plane(28, 28) if False else None
    m.woods({(x, y) for x in range(28, 31) for y in range(28, 32)}, salt=23, aethos_only=lambda x, y: False)
    # the south-west village: a garden of olives between Chilon's and the Mani road
    m.woods({(x, y) for x in range(10, 18) for y in range(37, 39)
             if int(m.mid[y, x]) in (A.GRASS, A.SHADE) and not m.solid[y, x]}, salt=29,
            aethos_only=lambda x, y: False)
    m.woods({(x, y) for x in range(5, 9) for y in range(30, 34)
             if int(m.mid[y, x]) in (A.GRASS, A.SHADE) and not m.solid[y, x] and (x, y) != (7, 29)},
            salt=31, aethos_only=lambda x, y: False)
    m.border = [A.GRASS, A.GRASS, A.GRASS, A.GRASS]
    # no up seam yet: Route 26 is not built (its builder agrees the north strip)

    # ---- events -------------------------------------------------------------------------
    S = "Lakonia_EventScript_"
    w = m.warp
    w(29, 36, "MAP_LAKONIA_ASCLEPEION", 0)
    w(33, 36, "MAP_LAKONIA_AGORA", 0)
    w(11, 28, "MAP_LAKONIA_LAMPITOS_HOUSE", 0)
    w(6, 21, "MAP_LAKONIA_GYLIPPOS_HOUSE", 0)
    w(23, 18, "MAP_LAKONIA_SYSSITION", 0)
    w(9, 6, "MAP_LAKONIA_AGOGE", 0)
    w(31, 17, "MAP_LAKONIA_PALAESTRA", 0)
    w(35, 30, "MAP_LAKONIA_ORTHIA", 0)
    w(6, 37, "MAP_LAKONIA_CHILON_HOUSE", 0)
    w(14, 39, "MAP_LAKONIA_LICHAS_HOUSE", 0)
    o = m.obj
    # the story's people (ON_TRANSITION moves them by beat)
    o("ICHOR_ELDER_M", 17, 21, S + "Gylippos", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_LAKONIA_GYLIPPOS")
    o("ICHOR_ALETHEA", 26, 26, S + "Alethea", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ALETHEA_LAKONIA",
      local_id="LOCALID_LAKONIA_ALETHEA")
    o("ICHOR_RHEA_UNMASKED", 13, 31, S + "Rhea", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_RHEA_LAKONIA",
      local_id="LOCALID_LAKONIA_RHEA")
    o("ICHOR_KLEON", 12, 31, S + "Kleon", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_KLEON_LAKONIA",
      local_id="LOCALID_LAKONIA_KLEON")
    o("ICHOR_BRASIDAS", 20, 9, S + "Brasidas", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_ICHOR_HIDE_BRASIDAS_LAKONIA",
      local_id="LOCALID_LAKONIA_BRASIDAS")["_floats"] = True
    # III-5F's lane: the Voice and his helmets, outside Lampito's yard (scene only)
    scene = (("ICHOR_IAPETOS", 12, 34, "IAPETOS"), ("ICHOR_GIGAS", 11, 33, "GRATION"),
             ("ICHOR_GIGAS", 14, 34, "PALLAS"), ("ICHOR_TITAN_GRUNT", 10, 34, "KACHLEX_GATE"),
             ("ICHOR_TITAN_GRUNT", 15, 33, "PLINTHOS_GATE"))
    for i, (gfx, x, y, name) in enumerate(scene):
        o(gfx, x, y, S + "Nothing", "MOVEMENT_TYPE_FACE_UP", flag=f"FLAG_TEMP_{0x11 + i:X}",
          local_id="LOCALID_LAKONIA_" + name)
    # the doubters, after III-5F, on the stoa's steps (optional battles)
    o("ICHOR_TITAN_GRUNT", 28, 26, S + "Kachlex", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_TEMP_16", trainer=True,
      sight=1, local_id="LOCALID_LAKONIA_KACHLEX")
    o("ICHOR_TITAN_GRUNT", 32, 26, S + "Plinthos", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_TEMP_17", trainer=True,
      sight=1, local_id="LOCALID_LAKONIA_PLINTHOS")
    # III-5I's crowd on the ring's wall (scene only)
    for i, (x, y) in enumerate(((13, 8), (20, 10), (12, 11), (20, 12), (13, 14))):
        o("ICHOR_CADET" if i % 2 == 0 else "ICHOR_CADET_F", x, y, S + "RingCadet",
          "MOVEMENT_TYPE_FACE_RIGHT" if x < 16 else "MOVEMENT_TYPE_FACE_LEFT", flag=f"FLAG_TEMP_{0x18 + i:X}",
          local_id=f"LOCALID_LAKONIA_RING_CADET_{i + 1}")["_floats"] = True
    # townsfolk
    o("ICHOR_ELDER_M", 19, 22, S + "CountingElder", "MOVEMENT_TYPE_FACE_DOWN")
    o("ICHOR_WOMAN", 17, 41, S + "Mother", "MOVEMENT_TYPE_FACE_UP")
    o("ICHOR_AUGUR", 17, 18, S + "Augur", "MOVEMENT_TYPE_FACE_DOWN")["_floats"] = True
    o("ICHOR_CADET", 26, 30, S + "Cadet", "MOVEMENT_TYPE_WALK_UP_AND_DOWN", ry=3)
    o("ICHOR_CADET_F", 10, 10, S + "CadetYard", "MOVEMENT_TYPE_WANDER_AROUND", rx=3, ry=2)
    o("ICHOR_CADET", 33, 8, S + "CadetField", "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1)
    o("ICHOR_CADET", 27, 2, S + "NorthGuard", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_LAKONIA_NORTH_GUARD")
    o("ICHOR_HOPLITE", 31, 13, S + "Wrestler", "MOVEMENT_TYPE_FACE_LEFT")
    m.item_ball(49, 9, "ITEM_RARE_CANDY", "FLAG_ICHOR_ITEM_LAKONIA_MENELAION")
    o("BREAKABLE_ROCK", 3, 10, "EventScript_RockSmash", "MOVEMENT_TYPE_NONE", flag="FLAG_ICHOR_HIDE_LAKONIA_RUBBLE")
    m.item_ball(1, 9, "ITEM_FOCUS_BAND", "FLAG_ICHOR_ITEM_LAKONIA_CLEFT")
    m.forced_open.add((3, 10))
    m.hidden(46, 9, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ITEM_LAKONIA_MENELAION")
    m.hidden(5, 12, "ITEM_ELIXIR", "FLAG_ICHOR_HIDDEN_ITEM_LAKONIA_AGOGE")
    m.hidden(34, 39, "ITEM_FULL_RESTORE", "FLAG_ICHOR_HIDDEN_ITEM_LAKONIA_BRIDGE")
    m.sign(19, 40, S + "ManiRoad")
    m.set(27, 29, A.STELE, True)                 # Leonidas's cenotaph, on the road up from the bridge
    m.sign(27, 29, S + "Leonidas")
    m.sign(3, 24, S + "Kaiadas")                 # the mountain's face over the west village
    m.set(37, ENTRY_ROW - 2, A.HERM, True)      # the town's great herm, at the bridge's west end
    m.sign(37, ENTRY_ROW - 2, S + "TownHerm")
    m.sign(24, 24, S + "Enyalios")
    m.sign(30, 25, S + "PersianStoa")
    m.sign(6, 28, S + "BurialPlot")
    m.sign(16, 15, S + "Ring") if False else None
    m.sign(47, 9, S + "Menelaion")
    m.sign(14, 30, S + "Well")
    for y in range(ENTRY_ROW - 1, ENTRY_ROW + 2):
        m.trigger(36, y, S + "Arrival", "VAR_TEMP_1", 0)
    m.trigger(16, 15, S + "RingGap", "VAR_TEMP_2", 0)
    for x in range(24, 27):
        m.trigger(x, 4, S + "GoatPaths", "VAR_TEMP_3", 0)
    m.connect("right", ENTRY_ROW - 3, "MAP_ROUTE25_EUROTAS")
    starts = [(W - 1, ENTRY_ROW)]
    must = [(24, 22, "the agora"), (16, 13, "the ring"), (11, 29, "Lampito's step")]
    views = [(44, 37), (31, 35), (24, 23), (12, 30), (16, 11), (26, 5), (32, 11), (8, 37), (47, 9)]
    errs = m.build("lakonia", starts, must, views)
    for y in EAST_SEAM_ROWS:
        for x in range(W - 8, W):
            if int(m.mid[y, x]) >= 0x200:
                print(f"Lakonia CHECK: ({x},{y}) holds lakonia 0x{int(m.mid[y, x]):03X} in Route 25's seam strip")
                errs.append("seam")
    return errs


if __name__ == "__main__":
    build()
