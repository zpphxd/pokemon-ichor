"""Route 25, up the Eurotas from Gytheion to Lakonia (design/maps/Route25_Eurotas.md).

The valley floor between the river and the foot of Taygetos: the road climbs
north from the harbor past olive terraces and barley, the reed beds where the
battle school's boys cut their bedding, a ford on a side stream, Apollo's hill
at Amyklai with the Vapheio tomb in its flank, and a cutting into the plane
trees; then it turns west and the town without walls comes into view.
"""
from __future__ import annotations

from lakonia_maps import A, LMap, _hash

W, H = 28, 50
EXIT_ROW = 3                 # the road leaves by the west edge on rows 2..4
LAKONIA_ENTRY_ROW = 37       # ...into Lakonia's east road on its rows 36..38
OFFSET_LAKONIA = EXIT_ROW - LAKONIA_ENTRY_ROW
# Lakonia overlaps our west edge on rows OFFSET..OFFSET+41: keep aethos there
LEFT_SEAM_ROWS = range(0, OFFSET_LAKONIA + 42)


def west_bank(y):
    """The river's west bank column on row y (the river runs to the east edge)."""
    if y < 8:
        return 21 + (1 if y in (2, 3, 4) else 0)
    if y < 17:
        return 20 - (1 if 11 <= y <= 14 else 0)
    if y < 25:
        return 19
    if y < 32:                       # the reed beds: the river spreads west
        return 17 if 26 <= y <= 30 else 18
    if y < 38:
        return 19 + (1 if y >= 35 else 0)
    return 99


def ragged(x0, y0, x1, y1, salt, top=True, bottom=True):
    """A grass band x0..x1, y0..y1 with ragged tufts above and below it."""
    cells = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    for x in range(x0, x1 + 1):
        if top and _hash(x, y0, salt) < 500:
            cells.add((x, y0 - 1))
        if bottom and _hash(x, y1, salt + 1) < 450:
            cells.add((x, y1 + 1))
    return cells


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
    river = {(x, y) for y in range(H) for x in range(west_bank(y), W)}
    for y in range(38, 41):            # the river bends out east toward the gulf
        river |= {(x, y) for x in range(23 + (y - 38) * 2, W)}
    put(river, "w")
    # the reed beds, a soft shape in the shallows, and smaller beds upriver
    reeds = set()
    for y in range(25, 32):
        a = west_bank(y)
        b = 21 + (1 if 27 <= y <= 29 else 0) - (1 if y in (25, 31) else 0)
        reeds |= {(x, y) for x in range(a, b + 1)}
    reeds |= {(23, 27), (23, 28), (24, 28)}
    reeds |= {(20, 21), (21, 21), (20, 20), (21, 20), (22, 21)}
    reeds |= {(24, 11), (25, 11), (24, 12), (25, 12), (26, 12), (25, 10)}
    put(reeds, "r")
    # the side stream, two rows, from a spring at Taygetos's foot to the river
    put({(x, y) for x in range(4, west_bank(22)) for y in (22, 23)}, "w")
    # ---- the north: woods, the cutting, the plane trees ------------------------------
    fill(0, 0, west_bank(0) - 1, 1, "T")
    fill(0, 5, 11, 7, "T")
    fill(17, 5, west_bank(5) - 1, 9, "T")
    # ---- the road ---------------------------------------------------------------------
    fill(14, 42, 16, H - 1, "p")
    fill(14, 32, 16, 41, "p")
    fill(14, 24, 16, 31, "p")             # the bank past the reeds
    fill(15, 18, 16, 21, "p")
    fill(14, 10, 16, 17, "p")
    fill(15, 8, 16, 9, "p")               # the cutting
    fill(13, 5, 16, 7, "p")
    fill(0, 2, 16, 4, "p")                # west, into Lakonia
    g[22][15] = g[23][15] = "f"          # the ford's stepping stones
    # ---- forced grass -----------------------------------------------------------------
    put(ragged(9, 32, west_bank(32) - 1, 34, 31, top=True, bottom=False), "G")   # band 1
    put({(x, y) for x in range(3, 19) for y in range(17, 21)}
        | {(x, 16) for x in range(13, 19) if _hash(x, 16, 5) < 600}, "G")          # band 2
    put(ragged(12, 5, 16, 7, 41, top=False, bottom=False)
        | {(17, 6), (17, 7), (11, 6)}, "G")                                        # band 3
    # ---- the west fields and the farm ------------------------------------------------
    put({(x, y) for x in range(2, 12) for y in range(39, 42) if _hash(x, y, 9) < 820}, "G")
    put({(x, y) for x in range(2, 7) for y in range(28, 32) if _hash(x, y, 8) < 850}, "G")
    return g, river, reeds


def build():
    g, river, reeds = land()
    m = LMap("Route25_Eurotas", "eurotas", "\n".join("".join(r) for r in g))
    m.lay_plan(salt=25)
    for y in (22, 23):
        m.piece("river", "ford", 15, y)
    lo = max(LEFT_SEAM_ROWS) + 1           # first row where eurotas pieces may sit at x < 8
    # ---- Taygetos's foot down the west, from below the seam rows ----------------------
    for y in range(lo, 36):
        for x in range(0, 3 if y < 22 or y > 23 else 4):
            name = "mass_pine" if _hash(x, y, 3) < 120 else f"mass_{x % 2}{y % 2}"
            m.piece("taygetos", name, x, y)
    for x in range(0, 3):
        m.piece("taygetos", "lip_b" if x % 2 else "lip", x, 36)
        m.piece("taygetos", "face_b" if x % 2 else "face", x, 37)
        m.piece("taygetos", "foot_b" if x % 2 else "foot", x, 38)
    for (x, y) in ((3, 33), (3, 18), (3, 27)):
        m.piece("taygetos", "scree", x, y)
    m.piece("taygetos", "boulder", 3, 35)
    # ---- woods ------------------------------------------------------------------------
    m.woods(m.cells("T"), salt=4, aethos_only=lambda x, y: x < 8 or y < 6)
    for (x, y) in ((8, 0), (17, 0)) if False else ():
        pass
    m.plane(8, 5)            # the plane trees framing the cutting and band 3
    m.plane(18, 1)
    # ---- the cutting: rock either side of the road, Arimnestos's post --------------
    for x in range(12, 15):
        m.piece("taygetos", "lip_b" if x % 2 else "lip", x, 8)
        m.piece("taygetos", "face_b" if x % 2 else "face", x, 9)
    m.set(14, 8, A.GRASS, False)            # his nook in the rock
    m.set(14, 9, A.GRASS, False)
    m.piece("taygetos", "boulder", 13, 10)
    m.piece("taygetos", "lip", 17, 8)
    m.piece("taygetos", "face", 17, 9)
    # ---- Amyklai: Apollo's low hill, with the Vapheio tomb in its flank ---------------
    for x in range(1, 13):                  # the hill's south face (rows 13..15)
        b = "_b" if x % 2 else ""
        m.piece("taygetos", "lip" + b, x, 13)
        m.piece("taygetos", "face" + b, x, 14)
        m.piece("taygetos", "foot" + b, x, 15)
    m.put("vapheio", 4, 13, cells={(i, j) for i in range(4) for j in range(3)})   # door (5..6,15)
    for y in range(10, 13):                 # the hilltop
        for x in range(1, 13):
            m.set(x, y, A.GRASS, False)
    m.woods({(x, y) for x in range(0, 12) for y in range(8, 10)} | {(0, y) for y in range(10, 13)},
            salt=9, aethos_only=lambda x, y: x < 8)
    m.put("throne", 2, 8)                   # Apollo on his throne (2..4, 8..11); top row over the woods
    m.piece("flowers", "hyacinths", 1, 11)
    m.piece("flowers", "hyacinths_b", 5, 11)
    m.put("spring", 9, 10)                  # the spring (9..10, 10..11)
    m.piece("altar", "fire_L", 6, 10)       # Amyklai's fire, before the god
    m.piece("altar", "fire_R", 7, 10)
    m.set(13, 13, A.HERM, True)             # the great herm at the hill's gate (land at (13,14))
    m.path({(x, y) for x in range(8, 14) for y in range(11, 13)}
           | {(11, 10), (12, 10), (13, 10), (12, 11), (13, 11)},
           context={(14, 10), (14, 11), (14, 12)})
    # ---- the farm and Hestia's herm-shrines -----------------------------------------
    m.put("farmhouse", 4, 24, cells={(i, j) for i in range(4) for j in range(3)})   # door (5,26)
    m.part("herm_shrine", "lit", 9, 33, 1, 1)
    m.part("herm_shrine", "lit_base", 9, 34, 1, 1)
    m.part("herm_shrine", "lit", 5, 30, 1, 1) if False else None
    lane = {(x, 35) for x in range(5, 14)} | {(5, y) for y in range(27, 36)}
    m.path(lane, context={(14, 35), (5, 26)})
    for (x, y) in ((7, 27), (9, 24), (2, 25)):
        m.olive(x, y)
    m.cypress(8, 30)
    for y in range(32, 35):                  # band 1's west wall: a dry-stone terrace
        m.set(8, y, A.WALL["M"], True)
    m.set(8, 31, A.WALL["L"], True)
    # the wood between the reed bank and the farm (rows 24..31, x 9..13)
    m.woods({(x, y) for x in range(9, 14) for y in range(26, 32)} - {(13, 27)}, salt=13,
            aethos_only=lambda x, y: x < 8)
    m.set(13, 27, A.GRASS, False)           # Teleklos's nook on the bank
    # ---- the terraces and groves of the lower valley --------------------------------
    m.ledge_run(0, 13, 36) if False else None
    m.ledge_run(4, 13, 37)
    m.ledge_run(17, 22, 42)
    for (x, y) in ((1, 43), (4, 43), (7, 43), (10, 43), (2, 46), (5, 46), (8, 46), (11, 46)):
        m.olive(x, y)
    for (x, y) in ((18, 44), (21, 44), (24, 44), (19, 47), (22, 47), (25, 47)):
        m.olive(x, y)
    m.cypress(12, 39)
    m.cypress(17, 39)
    for (x, y) in ((18, 37), (19, 34), (17, 19)):
        if int(m.mid[y, x]) in (A.GRASS, A.SHADE):
            m.piece("oleander", "bush", x, y)
    # ---- the oleander meadow over the river, past the reed thicket ------------------
    for x in range(west_bank(13), 23):
        m.piece("bridge", "foot_H", x, 13)
    meadow = {(x, y) for x in range(23, W) for y in range(13, 18)} - {(23, 17)}
    for (x, y) in meadow:
        m.set(x, y, A.TALL if _hash(x, y, 2) < 700 else A.GRASS, False)
    water = (river - meadow) | {(x, 13) for x in range(west_bank(13), 23)}
    m.soft("river", {c for c in river - meadow - reeds if not (c[1] == 13 and west_bank(13) <= c[0] < 23)}
           - {(15, 22), (15, 23)}, water | {(x, y) for x in range(4, 19) for y in (22, 23)})
    for (x, y) in ((24, 16), (27, 13)):
        m.piece("oleander", "bush", x, y)
    m.border = [A.GRASS, A.GRASS, A.GRASS, A.GRASS]
    m.seam("down")

    # ---- events -----------------------------------------------------------------------
    S = "Route25_EventScript_"
    o = m.obj

    def t(gfx, x, y, name, face, sight):
        return o(gfx, x, y, S + name, "MOVEMENT_TYPE_FACE_" + face, trainer=True, sight=sight,
                 local_id="LOCALID_ROUTE25_" + name.upper())
    t("ICHOR_CADET_F", 15, 39, "Agiatis", "DOWN", 4)
    t("ICHOR_CADET", 13, 27, "Teleklos", "RIGHT", 3)
    t("ICHOR_CADET", 17, 24, "Isadas", "LEFT", 2)
    t("ICHOR_CADET", 14, 21, "Phoibidas", "RIGHT", 2)
    t("ICHOR_FISHER", 17, 32, "Alpheios", "RIGHT", 1)
    t("ICHOR_PILGRIM", 8, 12, "Theodora", "UP", 2)
    t("ICHOR_HOPLITE", 14, 8, "Arimnestos", "RIGHT", 2)
    t("ICHOR_HARVESTER", 7, 41, "Euthymia", "UP", 3)
    o("ICHOR_CADET", 19, 28, S + "ReedCadet", "MOVEMENT_TYPE_FACE_UP")
    o("ICHOR_CADET", 20, 30, S + "ReedCadet2", "MOVEMENT_TYPE_FACE_LEFT")
    o("ICHOR_CADET", 16, 15, S + "Runner", "MOVEMENT_TYPE_WALK_UP_AND_DOWN", ry=2)
    o("ICHOR_PRIESTESS", 7, 11, S + "Polyboia", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_ROUTE25_POLYBOIA")
    o("CUTTABLE_TREE", 19, 13, "EventScript_CutTree", "MOVEMENT_TYPE_NONE")
    o("ICHOR_ELDER_F", 6, 25, S + "HearthWoman", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE25_HESTIA",
      local_id="LOCALID_ROUTE25_HESTIA")
    m.item_ball(26, 15, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_ITEM_ROUTE25_MEADOW")
    m.item_ball(3, 31, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_ROUTE25_FARM")
    m.item_ball(1, 3, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_ROUTE25_WEST")
    m.item_ball(2, 40, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_ROUTE25_FIELD")
    m.item_ball(1, 12, "ITEM_ETHER", "FLAG_ICHOR_ITEM_ROUTE25_AMYKLAI")
    m.hidden(3, 12, "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_THRONE")
    m.hidden(14, 24, "ITEM_BIG_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_FORD")
    m.hidden(27, 17, "ITEM_PP_UP", "FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_MEADOW")
    m.hidden(13, 41, "ITEM_HYPER_POTION", "FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_TERRACE")
    m.hidden(4, 34, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_SCREE")
    m.sign(13, 42, S + "SignSouth")
    m.sign(13, 13, S + "Herm")
    m.sign(17, 2, S + "SignLakonia") if False else m.sign(13, 1, S + "SignLakonia")
    m.sign(3, 11, S + "Throne")
    m.sign(9, 11, S + "Spring")
    m.sign(1, 11, S + "Hyacinths")
    m.sign(6, 10, S + "Altar")
    m.sign(5, 15, S + "Vapheio")
    m.sign(6, 25, S + "Farmhouse") if False else None
    m.sign(6, 25, S + "Hearth") if False else m.sign(5, 25, S + "Hearth")
    m.sign(9, 34, S + "HermShrine")
    for y in range(2, 5):
        m.trigger(7, y, S + "TownInView", "VAR_TEMP_1", 0)
    m.connect("down", 0, "MAP_GYTHEION")
    m.connect("left", OFFSET_LAKONIA, "MAP_LAKONIA")
    starts = [(15, H - 1)]
    blockers = [(e["x"], e["y"]) for e in m.objects if e["trainer_type"] != "TRAINER_TYPE_NONE"]
    must = [(0, 3, "the exit to Lakonia"), (5, 27, "the farmhouse door"), (8, 11, "Amyklai's spring"),
            (26, 14, "the meadow"), (5, 16, "the Vapheio door")]
    m.forced_open.add((19, 13))             # the reed thicket the Sickle cuts
    views = [(15, 45), (15, 37), (15, 29), (15, 22), (7, 12), (22, 15), (14, 7), (6, 3), (5, 30)]
    errs = m.build("route25_eurotas", starts, must, views)
    for y in LEFT_SEAM_ROWS:
        for x in range(8):
            if 0 <= y < H and int(m.mid[y, x]) >= 0x200:
                print(f"Route25_Eurotas CHECK: ({x},{y}) holds eurotas 0x{int(m.mid[y, x]):03X} in Lakonia's seam strip")
                errs.append("seam")
    print("Route25: forced grass on the way north:", m.min_grass([(15, H - 1)], [(0, 2), (0, 3), (0, 4)]))
    return errs


if __name__ == "__main__":
    build()
