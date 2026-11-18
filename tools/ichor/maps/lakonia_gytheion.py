"""Gytheion, Sparta's harbor on the Lakonian Gulf (design/maps/Gytheion.md).

A hamlet round a small bay under a wooded hill: the theater cut into the hill
with the Asclepeion as its stage-building, the purple quay on the bay, the
shingle beach where the dyers work, and the causeway out to Kranai. Route 25
leaves by the gap in the north woods.
"""
from __future__ import annotations

from lakonia_maps import A, LMap, _hash

W, H = 34, 30


def land():
    """The plan: every cell a character (lakonia_maps' legend)."""
    g = [["." for _ in range(W)] for _ in range(H)]

    def fill(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < W and 0 <= y < H:
                    g[y][x] = c
    # the wooded hill behind the hamlet, and the headland's woods (north)
    fill(0, 0, W - 1, 5, "T")
    for y in range(0, 6):                       # the gap: the north road
        for x in range(13, 18):
            g[y][x] = "."
    fill(14, 0, 16, 5, "p")
    fill(12, 4, 12, 5, ".")
    fill(18, 4, 19, 5, ".")
    # the hill wraps the theater on the west
    fill(0, 6, 2, 12, "T")
    fill(0, 6, 12, 6, "T")
    fill(10, 7, 12, 10, "T")
    fill(11, 11, 12, 11, "T")
    # the headland: dark rock down to the sea (rows 6-9 east), then the bay
    fill(26, 6, W - 1, 8, "R")
    fill(27, 9, W - 1, H - 1, "~")
    # the bay below the quay
    fill(12, 19, W - 1, H - 1, "~")
    # the shingle beach on the west shore
    fill(0, 18, 11, H - 1, "s")
    fill(12, 18, 12, 18, "s")
    # Kranai: a low sand islet off the beach
    for y, (a, b) in zip(range(20, 29), ((25, 28), (24, 29), (23, 30), (23, 30), (22, 30),
                                          (23, 30), (23, 29), (24, 29), (25, 27))):
        fill(a, y, b, y, "s")
    # the Old Man of the Sea's islet off the headland (by Surf)
    for (x, y) in ((31, 11), (32, 11), (30, 12), (31, 12), (32, 12), (31, 13)):
        g[y][x] = "s"
    # the road down from the gap to the quay
    fill(14, 6, 16, 9, "p")
    fill(13, 10, 15, 12, "p")
    fill(13, 13, 25, 17, "p")                  # the quay's paved top
    fill(3, 13, 12, 15, "p")                   # the plaza under the theater
    fill(0, 16, 12, 17, ".")                   # a grass bank down to the beach
    fill(6, 16, 8, 17, "p")                    # the lane down to the dye-works
    fill(0, 13, 2, 15, ".")
    return ["".join(r) for r in g]


def build():
    m = LMap("Gytheion", "gytheion", "\n".join(land()))
    plan = m.plan
    m.lay_plan(salt=11)
    # --- the woods: the hill and the headland's crown --------------------------------
    woods = m.cells("T")
    seam_rows = lambda x, y: y < 6     # noqa: E731  aethos only by the north seam
    m.woods(woods, salt=3, aethos_only=lambda x, y: True,
            singles=None)
    # --- the headland: Taygetos's last spur drops into the sea ------------------------
    for x in range(26, W):
        b = "_b" if x % 2 else ""
        m.piece("taygetos", f"mass_{x % 2}0", x, 6)
        m.piece("taygetos", "lip" + b, x, 7) if False else m.piece("taygetos", "face" + b, x, 7)
        m.piece("taygetos", "foot_sea" + b, x, 8)
    m.piece("taygetos", "side_E", 26, 6) if False else None
    # the Old Man of the Sea's islet: a ruined shrine off the headland, by Surf
    m.piece("taygetos", "stack", 29, 26)
    # --- the theater cut into the hill, and its stage-building, the Asclepeion -------
    m.put("theater", 3, 7)
    m.put("skene", 4, 11)            # door at (7,12)
    for x in (3, 10):
        m.set(x, 11, A.SHADE, True)
        m.set(x, 12, A.SHADE, True)
    m.cypress(10, 11)
    m.cypress(3, 11)
    # --- the houses on the slope above the quay --------------------------------------
    m.front("house", 18, 8)          # Timaia's house, door (19,10)
    m.front("house", 22, 8)          # Lysandros's house, door (23,10)
    m.piece("house", "G_jar", 21, 10)
    m.set(21, 9, A.GRASS, False)
    m.set(21, 8, A.GRASS, False)
    m.olive(18, 6) if False else None
    for (x, y) in ((24, 11), (25, 11), (25, 12), (24, 12), (17, 11), (18, 11), (19, 11), (20, 11),
                   (21, 11), (22, 11), (23, 11)):
        m.set(x, y, A.PATCH["C"], False)
    m.path({(x, y) for x in range(17, 26) for y in range(11, 13)} |
           {(19, 11), (23, 11)}, context={(x, 13) for x in range(13, 26)} | {(16, y) for y in range(6, 13)})
    # the garden plots between the houses and the gap
    for (x, y) in ((17, 7), (17, 8), (17, 9), (17, 10), (21, 7), (25, 9), (25, 10)):
        m.set(x, y, A.ANEMONE if (x + y) % 3 == 0 else A.GRASS, False)
    m.olive(19, 6)
    m.olive(23, 6)
    m.cypress(13, 9)
    m.cypress(13, 7)
    m.set(12, 12, A.BOULDER_GRASS, True)
    # the grass bank between the plaza and the beach: olives, an anemone bed
    m.olive(0, 16)
    m.olive(10, 16)
    m.cypress(2, 16)
    for (x, y) in ((3, 16), (4, 16), (9, 17)):
        m.set(x, y, A.ANEMONE, False)
    m.ledge_run(3, 5, 17)                       # the bank drops to the beach
    # --- the quay -------------------------------------------------------------------
    for x in range(13, 26):
        name = "ring_S" if x in (15, 22) else ("S_b" if x == 20 else "S")
        m.piece("quay", name, x, 18)
    m.piece("quay", "out_SE", 26, 18)
    for y in range(9, 18):
        m.piece("quay", "E", 26, y)
    m.piece("quay", "in_NE", 26, 9) if False else None
    m.piece("quayside", "steps_S", 17, 18)     # the purple steps down to the water
    m.piece("quayside", "steps_SL", 23, 18)
    m.piece("quayside", "steps_SR", 24, 18)
    for (x, y) in ((16, 17), (18, 17), (17, 16), (19, 16), (23, 17), (24, 16)):
        m.piece("quayside", "stain" if (x + y) % 2 else "stain_b", x, y)
    m.piece("quayside", "bucket", 18, 16)       # Kleon's helmet, bailing a boat
    m.piece("quayside", "mooring", 25, 13)
    m.piece("quayside", "mooring", 25, 16)
    m.piece("quayside", "amphorae", 13, 14)
    m.piece("quayside", "basket", 21, 17)
    m.piece("quayside", "drain", 20, 17)
    m.part("kaiki", "afloat", 16, 19, 3, 2)     # the fisherman's boat at the steps
    m.part("kaiki", "afloat", 27, 14, 3, 2)     # moored off the east quay
    # the stall under the purple awning, beside the Asclepeion
    m.put("stall", 9, 13)                       # counter (9..11,14); keeper at (10,13)
    # --- the beach, the dye-works and the murex heaps -------------------------------
    beach = m.cells("s")
    sea = m.cells("~")
    m.coast(sea - {(x, y) for x in range(13, 27) for y in range(19, 20)} | sea, key="surf")
    # the quay's own edges stay quay (coast() redrew the row under it as surf)
    for x in range(13, 26):
        if x not in (17, 23, 24):
            m.piece("quay", "ring_S" if x in (15, 22) else ("S_b" if x == 20 else "S"), x, 18)
    m.put("dyeworks", 2, 19)                    # door (4,20); its open end looks to sea
    m.part("quayside", "heap_TL", 0, 19, 2, 2)  # crushed murex, gray like snow
    m.piece("quayside", "heap_small", 7, 19)
    m.piece("quayside", "heap_small", 1, 22)
    m.piece("vats", "vat", 7, 21)
    m.piece("vats", "vat_b", 8, 21)
    m.piece("vats", "skein_rack", 9, 19)
    m.piece("vats", "nets_L", 2, 25)
    m.piece("vats", "nets_R", 3, 25)
    for (x, y) in sorted(beach):
        if (x, y) in {(c, r) for c in range(23, 31) for r in range(21, 29)}:
            continue
        if m.behavior(int(m.mid[y, x])) == "MB_SAND" or int(m.mid[y, x]) == A.SAND:
            h = _hash(x, y, 77)
            if h < 45:
                m.piece("quayside", "pebbles" if h % 2 else "pebbles_b", x, y)
            elif h < 70:
                m.piece("quayside", "shells_sand", x, y)
    # where the grass bank meets the beach: the sand rim
    grassy = lambda x, y: m.ok(x, y) and m.plan[y][x] in ".T"     # noqa: E731
    m.sand_rim([(x, 18) for x in range(0, 12) if int(m.mid[18, x]) == A.SAND], grassy)
    # --- the causeway to Kranai, and the shrine ------------------------------------
    for x in range(12, 23):
        m.piece("kranai_way", "H_W" if x == 12 else ("H_E" if x == 22 else ("H_b" if x % 3 == 0 else "H")), x, 24)
    m.put("kranai_shrine", 26, 22)              # door (27,23)
    m.set(32, 11, A.STELE, True)                # the islet's ruined shrine
    m.cypress(24, 22)
    m.cypress(29, 22)
    # --- the land's last touches ------------------------------------------------------
    m.set(3, 15, A.HERM, True)                  # a herm at the plaza's west end
    m.set(13, 6, A.STELE, True)                 # the town sign at the gap
    m.border = [A.SEA, A.SEA, A.SEA, A.SEA]
    m.seam("up")

    # --- events ----------------------------------------------------------------------
    S = "Gytheion_EventScript_"
    w = m.warp
    w(7, 12, "MAP_GYTHEION_ASCLEPEION", 0)
    w(4, 20, "MAP_GYTHEION_DYEWORKS", 0)
    w(23, 10, "MAP_GYTHEION_LYSANDROS_HOUSE", 0)
    w(19, 10, "MAP_GYTHEION_TIMAIA_HOUSE", 0)
    w(27, 23, "MAP_GYTHEION_KRANAI_SHRINE", 0)
    o = m.obj
    o("ICHOR_FISHER", 17, 17, S + "Fisherman", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_GYTHEION_FISHERMAN")
    o("ICHOR_SAILOR", 25, 14, S + "Nausikles", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_GYTHEION_NAUSIKLES")
    o("ICHOR_ALETHEA", 24, 15, S + "Alethea", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_ICHOR_HIDE_ALETHEA_GYTHEION",
      local_id="LOCALID_GYTHEION_ALETHEA")
    o("ICHOR_MERCHANT", 10, 13, S + "Stallkeeper", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_GYTHEION_STALLKEEPER")
    o("ICHOR_KID_M", 6, 22, S + "DyersBoy", "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1)
    o("ICHOR_ELDER_F", 17, 24, S + "OldWoman", "MOVEMENT_TYPE_FACE_RIGHT")
    o("ICHOR_MAN", 15, 3, S + "Lakonian", "MOVEMENT_TYPE_FACE_DOWN")
    o("ICHOR_HEALER", 5, 14, S + "Patient", "MOVEMENT_TYPE_FACE_UP")
    m.item_ball(1, 27, "ITEM_NET_BALL", "FLAG_ICHOR_ITEM_GYTHEION_NET_BALL")
    m.item_ball(30, 12, "ITEM_MYSTIC_WATER", "FLAG_ICHOR_ITEM_GYTHEION_ISLET")
    m.hidden(31, 13, "ITEM_PEARL_STRING", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_ISLET")
    m.sign(32, 11, S + "Proteus")
    m.sign(13, 7, S + "TownSign")
    m.sign(3, 15, S + "Herm")
    m.sign(26, 12, S + "Cape")
    m.sign(5, 12, S + "TheaterView")
    # the town's travel herm, by the Euploia's berth: tools/ichor/maps/town_herms.py
    # the Shoal Shells for Porphyris (four, so one can be missed), and the town's own
    m.hidden(0, 29, "ITEM_SHOAL_SHELL", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_1")
    m.hidden(30, 27, "ITEM_SHOAL_SHELL", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_2")
    m.hidden(11, 28, "ITEM_SHOAL_SHELL", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_3")
    m.hidden(25, 17, "ITEM_SHOAL_SHELL", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_4")
    m.hidden(12, 13, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_THEATER")
    m.hidden(24, 28, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_KRANAI")
    m.connect("up", 0, "MAP_ROUTE25_EUROTAS")
    m.header.update({"weather": "WEATHER_SUNNY"})
    starts = [(15, 0)]
    must = [(7, 13, "the Asclepeion door's step"), (25, 15, "the arrival tile"), (27, 24, "Kranai"),
            (4, 21, "the dye-works")]
    views = [(15, 3), (8, 11), (20, 12), (22, 16), (6, 22), (22, 24)]
    return m.build("gytheion", starts, must, views)


if __name__ == "__main__":
    build()
