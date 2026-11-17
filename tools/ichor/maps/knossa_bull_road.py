#!/usr/bin/env python3
"""The Bull Road, its vineyard terraces and the Bronze Heel (design/maps/
KnossaBullRoad.md, KnossaBullRoad_Vineyard.md, KnossaBronzeHeel.md; SCRIPT.md
III-3B, Part 2-4; LABYRINTH.md §2).

    python3 tools/ichor/maps/knossa_bull_road.py [road|vineyard|heel ...] [--pass N]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_maps as KM  # noqa: E402
from knossa_maps import A, Map, ensure_map  # noqa: E402

TALL = A.TALL


# --------------------------------------------------------------------------------------------
# shared ground tools
# --------------------------------------------------------------------------------------------
def rock(m, cells, key="cliff", elev=4):
    """A raised limestone block over `cells` (the plateau, grass on top) with its
    edges: back on the north, sides, the lip on the south over a face row drawn
    into the cell below (which the caller leaves out of `cells`)."""
    cells = set(cells)
    inn = lambda x, y: (x, y) in cells  # noqa: E731
    for (x, y) in cells:
        n, s, e, w = inn(x, y - 1), inn(x, y + 1), inn(x + 1, y), inn(x - 1, y)
        if not s:
            name = "lip_L" if not w else ("lip_R" if not e else ("lip_b" if (x * 3 + y) % 5 == 0 else "lip"))
            m.piece(key, name, x, y)
            fy = y + 1
            if m.ok(x, fy) and (x, fy) not in cells:
                fname = "face_L" if not w else ("face_R" if not e else ("face_b" if (x + y) % 3 == 0 else "face"))
                m.piece(key, fname, x, fy)
        elif not n:
            m.piece(key, "back_NW" if not w else ("back_NE" if not e else "back"), x, y)
        elif not w:
            m.piece(key, "side_W", x, y)
        elif not e:
            m.piece(key, "side_E", x, y)
        else:
            m.set(x, y, A.GRASS, False)
            m.elev[(x, y)] = elev


def road(m, spine, salt=0):
    """A worn road along a spine of (y, x0, x1) rows, drawn with the patch kit."""
    cells = {(x, y) for (y, x0, x1) in spine for x in range(x0, x1 + 1)}
    m.path(cells)
    return cells


def grove(m, cells, salt=0):
    """An olive and cypress wood over cells (aethos), walked round, never into."""
    return m.woods(cells, salt=salt, aethos_only=lambda x, y: True, singles=[])


def brow(m, x0, x1, y, stairs=()):
    """A terrace brow: a ledge you hop down to the north, stairs where a path climbs."""
    for x in range(x0, x1 + 1):
        if x in stairs:
            m.piece("brow", "stair", x, y)
        else:
            m.piece("brow", "L" if x == x0 else ("R" if x == x1 else ("M2" if (x * 7 + y) % 4 == 0 else "M")), x, y)


def vine_patch(m, x0, y0, w, h):
    """A patch of vines (tall grass for encounters) with its soft edges."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            v = "N" if y == y0 else ("S" if y == y0 + h - 1 else "")
            hz = "W" if x == x0 else ("E" if x == x0 + w - 1 else "")
            nm = (v + hz) or ("C_grapes" if KM._hash(x, y, 5) < 250 else "C")
            m.piece("vines", nm, x, y)


def herb(m, cells, salt=0):
    """Phrygana in clumps on open ground: thyme, sage, asphodel, burnet."""
    kinds = ("thyme", "thyme_b", "asphodel", "thyme", "sage", "burnet")
    for (x, y) in cells:
        if int(m.mid[y, x]) == A.GRASS:
            m.piece("phrygana", kinds[KM._hash(x, y, salt) % len(kinds)], x, y)


# --------------------------------------------------------------------------------------------
# the Bull Road, 30 x 50
# --------------------------------------------------------------------------------------------
def bull_road(stem):
    name, P = "KnossaBullRoad", "KnossaBullRoad_EventScript_"
    W, H = 30, 50
    ensure_map(name, W, H, "bull_road", "MAP_TYPE_ROUTE", "MAPSEC_BULL_ROAD", "MUS_ICHOR_ROAD")
    m = Map(name, "bull_road", W, H, fill=A.GRASS)
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT[0], A.OLIVE_BOT[1]]

    spine = ([(y, 14, 17) for y in range(0, 6)] + [(y, 13, 16) for y in range(6, 13)]
             + [(y, 12, 15) for y in range(13, 18)] + [(y, 12, 14) for y in range(18, 25)]
             + [(25, 12, 15), (26, 13, 16), (27, 13, 17), (28, 14, 17), (29, 14, 17), (30, 14, 17),
                (31, 15, 18), (32, 15, 18), (33, 15, 18)] + [(y, 15, 17) for y in range(34, 41)]
             + [(y, 14, 16) for y in range(41, 50)])
    # the fork: east to the Bronze Heel, along the ridge
    fork = [(14, 16, 29), (15, 16, 29), (16, 18, 29)]

    # ---- the north end: olive country out of Amnisos (aethos only, the seam) ----
    grove(m, {(x, y) for x in range(0, 11) for y in range(0, 6)} - {(5, 2), (6, 2), (5, 3), (6, 3)}, salt=1)
    grove(m, {(x, y) for x in range(21, 30) for y in range(0, 6)} - {(24, 3), (25, 3)}, salt=2)

    # ---- the first terraces: brows step down northward, Kerinthe's skeps ----
    brow(m, 0, 12, 6)
    brow(m, 17, 29, 6)
    herb(m, {(x, y) for x in range(18, 28) for y in range(7, 9) if KM._hash(x, y, 3) < 300}, salt=3)
    herb(m, {(x, y) for x in range(1, 12) for y in range(7, 9) if KM._hash(x, y, 4) < 220}, salt=4)
    # band 1: three deep between olive woods
    grove(m, {(x, y) for x in range(0, 9) for y in range(9, 14)}, salt=5)
    grove(m, {(x, y) for x in range(21, 30) for y in range(9, 13)}, salt=6)
    band1 = {(x, y) for x in range(9, 21) for y in range(10, 13)}
    # ---- the fork and the great herm ----
    brow(m, 0, 11, 17)
    brow(m, 17, 29, 17)
    # ---- the cutting: limestone both sides, the road squeezed to three ----
    rock(m, {(x, y) for x in range(0, 11) for y in range(18, 24)})
    rock(m, {(x, y) for x in range(16, 30) for y in range(18, 23)})
    band2 = {(x, y) for x in range(11, 16) for y in range(20, 24)}
    # ---- the meadow: the herd crosses; terraces west and east ----
    brow(m, 0, 9, 28)
    brow(m, 21, 29, 28)
    herb(m, {(x, y) for x in range(0, 30) for y in range(25, 35) if KM._hash(x, y, 7) < 90}, salt=7)
    meadow_w = {(x, y) for x in range(1, 9) for y in range(30, 35) if KM._hash(x // 2, y, 8) < 820}
    meadow_e = {(x, y) for x in range(22, 29) for y in range(24, 28)}
    # ---- the olive grove of band 3 and the hut ----
    grove(m, {(x, y) for x in range(0, 11) for y in range(36, 44)} - {(4, 40), (5, 40), (4, 41), (5, 41)}, salt=9)
    grove(m, {(x, y) for x in range(24, 30) for y in range(36, 44)} - {(24, 39), (25, 39), (26, 39), (24, 40), (25, 40)}, salt=10)
    band3 = {(x, y) for x in range(11, 24) for y in range(37, 40)}
    m.put("mitato", 20, 33)
    # the narrow approach to the palace
    grove(m, {(x, y) for x in range(0, 13) for y in range(44, 50)}, salt=11)
    grove(m, {(x, y) for x in range(18, 30) for y in range(44, 50)}, salt=12)
    grove(m, {(x, y) for x in range(10, 13) for y in range(41, 44)} | {(x, y) for x in range(18, 24)
                                                                         for y in range(40, 44)}, salt=13)

    road(m, spine)
    road(m, fork)
    m.path({(x, 36) for x in (20, 21, 22)} | {(21, 35)} - {(21, 35)} | {(19, 34), (19, 35), (19, 36)},
           context={(21, 35)})
    for c in band1 | band2 | band3 | meadow_w | meadow_e:
        x, y = c
        if not m.solid[y, x] and int(m.mid[y, x]) not in (m.id("brow", "stair"),):
            m.set(x, y, TALL, False)
    # vine rows on the east terrace (optional grass, the vineyard's cousins)
    vine_patch(m, 22, 30, 4, 3)
    m.put("herm", 11, 14)
    for (x, n) in ((19, "top_L"), (20, "top"), (21, "top_R")):
        m.piece("labrys_door", n, x, 22)
    for (x, n) in ((19, "foot_L"), (20, "door"), (21, "foot_R")):
        m.piece("labrys_door", n, x, 23)
    for (x, y) in ((3, 25), (26, 25), (7, 34), (27, 34)):
        m.olive(x, y)
    m.cypress(10, 25)
    m.cypress(18, 25)
    for (x, y) in ((0, 33), (29, 30)):
        m.set(x, y, A.BOULDER_GRASS, True)
    m.seam("up")
    m.seam("down")

    # ---- events ----
    m.warp(21, 35, "MAP_KNOSSA_BULL_ROAD_HUT", 0)
    m.connect("up", -5, "MAP_KNOSSA_AMNISOS")
    m.connect("down", -14, "MAP_KNOSSA_PALACE")
    m.connect("right", 11, "MAP_KNOSSA_BRONZE_HEEL")
    m.connect("left", 23, "MAP_KNOSSA_BULL_ROAD_VINEYARD")
    T = lambda g, x, y, s, mv, sight, tid: m.obj(g, x, y, P + s, mv, trainer=True, sight=sight,  # noqa: E731
                                                 local_id=f"LOCALID_BULL_ROAD_{tid}")
    T("ICHOR_WOMAN", 19, 7, "Kerinthe", "MOVEMENT_TYPE_FACE_LEFT", 3, "KERINTHE")
    T("ICHOR_AUGUR", 10, 15, "Telemos", "MOVEMENT_TYPE_FACE_RIGHT", 3, "TELEMOS")
    T("ICHOR_YOUTH_M", 11, 19, "Euphemos", "MOVEMENT_TYPE_FACE_RIGHT", 3, "EUPHEMOS")
    T("ICHOR_SHEPHERD", 9, 26, "Boukolion", "MOVEMENT_TYPE_FACE_RIGHT", 4, "BOUKOLION")
    T("ICHOR_YOUTH_F", 20, 29, "Kybiste", "MOVEMENT_TYPE_FACE_LEFT", 3, "KYBISTE")
    T("ICHOR_HARVESTER", 4, 31, "Krokale", "MOVEMENT_TYPE_FACE_RIGHT", 3, "KROKALE")
    T("ICHOR_PILGRIM", 25, 26, "Theoris", "MOVEMENT_TYPE_FACE_DOWN", 2, "THEORIS")
    T("ICHOR_HARVESTER", 23, 38, "Elais", "MOVEMENT_TYPE_FACE_LEFT", 4, "ELAIS")
    T("ICHOR_PRIESTESS", 13, 42, "Phaistia", "MOVEMENT_TYPE_FACE_RIGHT", 3, "PHAISTIA")
    m.obj("ICHOR_SHEPHERD", 8, 29, P + "Milon", "MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_BULL_ROAD_MILON")
    for i, (x, y) in enumerate(((11, 29), (17, 26), (20, 31))):
        m.obj("SPECIES(TAURIVET)", x, y, P + "Herd", "MOVEMENT_TYPE_WANDER_AROUND",
              local_id=f"LOCALID_BULL_ROAD_HERD_{i + 1}", rx=2, ry=1)
    m.obj("ICHOR_TITAN_GRUNT", 13, 46, P + "SouthGrunt", "MOVEMENT_TYPE_FACE_RIGHT",
          flag="FLAG_ICHOR_HIDE_BULL_ROAD_GRUNTS", local_id="LOCALID_BULL_ROAD_GRUNT_1")
    m.obj("ICHOR_TITAN_GRUNT", 17, 46, P + "SouthGrunt", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_BULL_ROAD_GRUNTS", local_id="LOCALID_BULL_ROAD_GRUNT_2")
    m.item_ball(28, 8, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_BULL_ROAD_ULTRA_BALL")
    m.item_ball(2, 26, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_BULL_ROAD_FULL_HEAL")
    m.item_ball(24, 34, "ITEM_MAX_POTION", "FLAG_ICHOR_ITEM_BULL_ROAD_MAX_POTION")
    m.item_ball(2, 32, "ITEM_HP_UP", "FLAG_ICHOR_ITEM_BULL_ROAD_HP_UP")
    m.item_ball(25, 39, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_BULL_ROAD_REVIVE")
    m.hidden(11, 13, "ITEM_OLIVE_OIL", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_OLIVE_OIL")
    m.hidden(10, 22, "ITEM_RELIC_SILVER", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_SILVER_OWL")
    m.hidden(23, 35, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_STAR_PIECE")
    m.hidden(10, 38, "ITEM_MAX_ETHER", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_MAX_ETHER")
    m.set(13, 2, A.STELE, True)
    m.sign(13, 2, P + "NorthSign")
    m.sign(11, 15, P + "Herm")
    m.sign(15, 31, P + "MilonsLine", facing="BG_EVENT_PLAYER_FACING_NORTH")
    m.sign(20, 23, P + "LabrysDoor")
    m.set(18, 41, A.STELE, True)
    m.sign(18, 41, P + "SouthSign")
    starts = [(15, 0)]
    m.build(stem, starts=starts,
            must_reach=[(15, 49, "the palace"), (29, 15, "the Heel fork"), (0, 31, "the vineyard gap"),
                        (2, 33, "the HP Up"), (25, 40, "the Revive")],
            views=[(15, 5), (14, 12), (14, 20), (14, 30), (18, 37), (15, 45)],
            blockers=[])
    print("forced grass north->south:", m.min_grass([(x, 0) for x in range(14, 18)],
                                                    [(x, 49) for x in range(14, 17)]))
    return m


# --------------------------------------------------------------------------------------------
# the vineyard terraces, 20 x 16 (connected west of the meadow)
# --------------------------------------------------------------------------------------------
def vineyard(stem):
    name, P = "KnossaBullRoad_Vineyard", "KnossaBullRoad_Vineyard_EventScript_"
    W, H = 20, 16
    ensure_map(name, W, H, "bull_road", "MAP_TYPE_ROUTE", "MAPSEC_BULL_ROAD", "MUS_ICHOR_ROAD",
               ichor_kind="dungeon")
    m = Map(name, "bull_road", W, H, fill=A.GRASS)
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT[0], A.OLIVE_BOT[1]]
    # three terraces stepping up to the north-west, each a band of vines
    grove(m, {(x, y) for x in range(0, W) for y in range(0, 2)}, salt=21)
    grove(m, {(x, y) for x in range(0, 2) for y in range(2, H)}, salt=22)
    grove(m, {(x, y) for x in range(2, W) for y in range(14, H)}, salt=23)

    def patch(x0, y0, w, h):
        vine_patch(m, x0, y0, w, h)
    patch(3, 2, 10, 3)
    for x in range(2, 18):
        m.piece("terrace", "M" if x % 4 else "M2", x, 6)
        m.piece("terrace", "top" if x % 4 else "top_M2", x, 5)
    m.piece("terrace", "steps", 15, 6)
    m.piece("terrace", "top_steps", 15, 5)
    patch(3, 7, 11, 3)
    for x in range(2, 18):
        m.piece("terrace", "M" if x % 4 else "M2", x, 11)
        m.piece("terrace", "top" if x % 4 else "top_M2", x, 10)
    m.piece("terrace", "steps", 4, 11)
    m.piece("terrace", "top_steps", 4, 10)
    patch(6, 12, 9, 2)
    m.path({(x, y) for x in (16, 17) for y in range(2, 14)} | {(x, 12) for x in (17, 18, 19)}
           | {(x, 13) for x in (17, 18, 19)})
    m.piece("vines", "sign", 18, 11)
    brow(m, 2, 9, 13, stairs=(4, 5))
    m.set(9, 6, A.BOULDER_GRASS, True)
    m.set(12, 11, A.BOULDER_GRASS, True)
    m.connect("right", -23, "MAP_KNOSSA_BULL_ROAD")
    T = lambda g, x, y, s, mv, sight, tid: m.obj(g, x, y, P + s, mv, trainer=True, sight=sight,  # noqa: E731
                                                 local_id=f"LOCALID_VINEYARD_{tid}")
    T("ICHOR_YOUTH_M", 14, 8, "Iphitos", "MOVEMENT_TYPE_FACE_LEFT", 3, "IPHITOS")
    T("ICHOR_ELDER_M", 13, 3, "Propolis", "MOVEMENT_TYPE_FACE_DOWN", 2, "PROPOLIS")
    m.item_ball(2, 2, "ITEM_PP_UP", "FLAG_ICHOR_ITEM_VINEYARD_PP_UP")
    m.item_ball(3, 13, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_VINEYARD_ULTRA_BALL")
    m.hidden(2, 12, "ITEM_WINE", "FLAG_ICHOR_HIDDEN_ITEM_VINEYARD_WINE")
    m.hidden(18, 10, "ITEM_ELIXIR", "FLAG_ICHOR_HIDDEN_ITEM_VINEYARD_ELIXIR")
    m.sign(18, 11, P + "Sign")
    m.build(stem, starts=[(19, 12)], must_reach=[(2, 3, "the sealed jar"), (3, 12, "the low corner")],
            views=[(9, 5), (10, 10)])
    return m


# --------------------------------------------------------------------------------------------
# the Bronze Heel, 30 x 20 (east of the fork)
# --------------------------------------------------------------------------------------------
def bronze_heel(stem):
    name, P = "KnossaBronzeHeel", "KnossaBronzeHeel_EventScript_"
    W, H = 30, 20
    ensure_map(name, W, H, "bull_road", "MAP_TYPE_ROUTE", "MAPSEC_BULL_ROAD", "MUS_ICHOR_ROAD",
               ichor_kind="dungeon")
    m = Map(name, "bull_road", W, H, fill=A.GRASS)
    m.border = [A.SEA] * 4
    grove(m, {(x, y) for x in range(0, W) for y in range(0, 2)}, salt=31)
    grove(m, {(x, y) for x in range(24, W) for y in range(2, 9)}, salt=32)
    # the headland's grass, where the beach grass grows long
    beach_grass = {(x, y) for x in range(8, 22) for y in range(3, 8) if KM._hash(x // 2, y, 33) < 700}
    beach_grass |= {(x, y) for x in range(2, 7) for y in range(6, 9)}
    # the low cliff down to the beach, a gap where the path goes down
    rock(m, {(x, y) for x in range(0, W) for y in range(8, 10) if not 6 <= x <= 8})
    # sand and sea
    rows = []
    for y in range(11, H):
        r = ""
        for x in range(W):
            shore = 15 + (1 if x > 20 else 0) - (1 if x < 6 else 0)
            r += "#" if y < shore else "~"
        rows.append(r)
    m.shore(rows, 0, 11)
    m.rect(6, 9, 8, 10, A.SAND, False)
    m.path({(x, y) for y in (3, 4, 5) for x in range(0, 8)} | {(x, y) for x in (6, 7) for y in range(6, 9)})
    # the giant's foot on the beach, the tide pools, the spit out to the point
    m.put("talos_foot", 11, 10)
    for (x, y, n) in ((20, 12, "pool"), (21, 12, "pool_b"), (22, 12, "pool_dig"), (23, 12, "urchins"),
                      (20, 13, "ledge_skull"), (21, 13, "ledge_dart")):
        m.piece("tide_pools", n, x, y)
    for y in range(15, H):
        m.piece("rocks", "spit_V" if y < H - 1 else "spit_head", 26, y)
    m.piece("rocks", "tide_rocks", 25, 16)
    m.piece("rocks", "tide_rock", 27, 17)
    m.piece("rocks", "rocks_sand", 3, 13)
    for (x, y, d) in ((5, 12, "shells"), (9, 14, "wrack"), (18, 13, "lace"), (23, 14, "footprints")):
        m.piece("sand_decor", d, x, y)
    for c in beach_grass:
        x, y = c
        if not m.solid[y, x] and int(m.mid[y, x]) == A.GRASS:
            m.set(x, y, TALL, False)
    herb(m, {(x, y) for x in range(0, 24) for y in range(2, 8) if KM._hash(x, y, 34) < 120}, salt=34)
    brow(m, 9, 21, 6, stairs=(15, 16))
    for x in (13, 19, 23):
        m.set(x, 8, A.BOULDER_GRASS, True)
    m.connect("left", -11, "MAP_KNOSSA_BULL_ROAD")
    m.obj("ICHOR_ALETHEA", 12, 14, P + "Alethea", "MOVEMENT_TYPE_FACE_UP",
          flag="FLAG_ICHOR_HIDE_ALETHEA_HEEL", local_id="LOCALID_HEEL_ALETHEA")
    m.obj("ICHOR_YOUTH_F", 16, 12, P + "Glauke", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3,
          local_id="LOCALID_HEEL_GLAUKE")
    m.item_ball(22, 3, "ITEM_RARE_CANDY", "FLAG_ICHOR_ITEM_BRONZE_HEEL_RARE_CANDY")
    m.item_ball(28, 14, "ITEM_BIG_PEARL", "FLAG_ICHOR_ITEM_BRONZE_HEEL_BIG_PEARL")
    m.hidden(26, H - 1, "ITEM_METAL_COAT", "FLAG_ICHOR_HIDDEN_ITEM_BRONZE_HEEL_METAL_COAT")
    m.hidden(16, 12, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ITEM_BRONZE_HEEL_STARDUST")
    m.sign(12, 13, P + "Foot")
    m.sign(13, 13, P + "Foot")
    m.sign(20, 13, P + "FossilLedge")
    m.sign(21, 13, P + "FossilLedge")
    m.build(stem, starts=[(0, 4)], must_reach=[(26, H - 1, "the point"), (22, 3, "the high grass")],
            views=[(7, 5), (14, 13), (24, 14)])
    return m


BUILDERS = {"road": bull_road, "vineyard": vineyard, "heel": bronze_heel}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--pass", dest="n", default="1")
    a = ap.parse_args()
    stems = {"road": "knossa_bull_road", "vineyard": "knossa_vineyard", "heel": "knossa_bronze_heel"}
    for n in a.names or BUILDERS:
        BUILDERS[n](f"{stems[n]}_pass{a.n}")
