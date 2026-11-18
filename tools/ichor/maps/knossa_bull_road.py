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
    """An olive and cypress wood over cells, walked round, never into. The odd cells
    left between trunks get scrub (sage, burnet) except in the seam strips, which
    keep to aethos's shade."""
    seam = lambda x, y: y < 6 or y >= m.h - 6 or m.ts != "bull_road"  # noqa: E731
    return m.woods(cells, salt=salt, aethos_only=seam,
                   singles=[("phrygana", "sage"), ("phrygana", "burnet")])


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
    """Design round 2 (2026-11-17): the road bends with the valley; soft-edged
    grass; terraces, outcrops, scrub, a wayside shrine and the herd's pasture,
    so every 15x10 screen has its landmark."""
    name, P = "KnossaBullRoad", "KnossaBullRoad_EventScript_"
    W, H = 30, 50
    ensure_map(name, W, H, "bull_road", "MAP_TYPE_ROUTE", "MAPSEC_BULL_ROAD", "MUS_ICHOR_ROAD")
    m = Map(name, "bull_road", W, H, fill=A.GRASS)
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT[0], A.OLIVE_BOT[1]]

    # the road's spine: (y, x0, x1), bending with the valley
    spine = ([(0, 13, 16), (1, 13, 16), (2, 13, 16), (3, 14, 17), (4, 14, 17), (5, 15, 18), (6, 15, 18),
              (7, 14, 17), (8, 13, 16), (9, 12, 15), (10, 12, 15), (11, 12, 15), (12, 11, 14), (13, 11, 14),
              (14, 11, 14), (15, 11, 15), (16, 11, 15), (17, 12, 14)]
             + [(y, 12, 14) for y in range(18, 25)]
             + [(25, 12, 15), (26, 13, 16), (27, 14, 17), (28, 14, 17), (29, 15, 17), (30, 15, 17),
                (31, 15, 17), (32, 15, 18), (33, 16, 19), (34, 16, 19), (35, 16, 19), (36, 15, 18),
                (37, 15, 18), (38, 14, 17), (39, 14, 17), (40, 14, 17), (41, 14, 16), (42, 14, 16),
                (43, 14, 16)] + [(y, 14, 16) for y in range(44, 50)])
    fork = [(14, 16, 18), (15, 16, 21), (16, 19, 25), (15, 23, 29), (14, 26, 29), (16, 26, 29)]
    to_vineyard = [(33, 0, 4), (34, 0, 7), (33, 5, 9), (34, 8, 15), (33, 10, 15)]

    # ---- screen 1: olive country out of Amnisos (aethos only, the seam) ----
    grove(m, {(x, y) for x in range(0, 11) for y in range(0, 6)} - {(9, 4), (10, 4), (9, 5), (10, 5), (5, 3), (6, 3)}
          - {(x, y) for x in range(0, 4) for y in range(4, 6)}, salt=1)
    grove(m, {(x, y) for x in range(20, 30) for y in range(0, 6)} - {(20, 4), (21, 4), (20, 5), (21, 5)}
          - {(x, 5) for x in range(26, 30)}, salt=2)
    # ---- screen 2: the beekeepers' terraces ----
    brow(m, 0, 13, 7, stairs=(3, 4))
    brow(m, 19, 29, 7, stairs=(26,))
    for (x, y) in ((1, 8), (5, 8), (22, 8), (27, 8)):
        m.olive(x, y)
    herb(m, {(x, y) for x in range(18, 29) for y in range(8, 10) if KM._hash(x, y, 3) < 420}, salt=3)
    herb(m, {(x, y) for x in range(0, 11) for y in range(9, 10)}, salt=4)
    grove(m, {(x, y) for x in range(0, 7) for y in range(10, 14)} | {(7, 10), (8, 10)}, salt=5)
    grove(m, {(x, y) for x in range(21, 30) for y in range(10, 13)} | {(20, 12)}, salt=6)
    band1 = ({(x, y) for x in range(7, 20) for y in range(10, 13)} - {(7, 10), (8, 10), (19, 10), (20, 12)}
             | {(9, 9), (10, 9), (16, 9), (17, 9)})
    # ---- screen 3: the fork and the great herm, an outcrop over the shore path ----
    for (x, y) in ((4, 15), (7, 14), (1, 16)):
        m.olive(x, y)
    m.cypress(9, 14)
    for (x, y) in ((17, 12), (18, 12), (22, 13), (24, 17), (27, 13)):
        m.set(x, y, A.BOULDER_GRASS, True)
    herb(m, {(x, y) for x in range(16, 30) for y in range(13, 18) if KM._hash(x, y, 7) < 260}, salt=7)
    brow(m, 0, 10, 17, stairs=(5,))
    brow(m, 16, 29, 18, stairs=(20,))
    # ---- screen 4: the cutting, its lips ragged ----
    west = {(x, y) for x in range(0, 11) for y in range(18, (24, 24, 24, 24, 25, 25, 25, 25, 23, 23, 23)[x])}
    west -= {(x, 18) for x in range(0, 4)}
    east = {(x, y) for x in range(16, 30) for y in range(19, 24 if x < 25 else 23)}
    east -= {(x, 19) for x in range(25, 30)}
    rock(m, west)
    rock(m, east)
    band2 = {(x, y) for x in range(11, 16) for y in range(20, 24)}
    # ---- screen 5: the herd's pasture, the wayside shrine ----
    brow(m, 0, 9, 26, stairs=(4,))
    brow(m, 21, 29, 30, stairs=(25,))
    pasture_w = {(x, y) for x in range(1, 10) for y in range(28, 33)
                 if not ((x < 3 or x > 7) and (y in (28, 32)))} - {(8, 29), (9, 29), (4, 30)}
    pasture_e = {(x, y) for x in range(21, 29) for y in range(25, 29) if not (x > 26 and y == 25)}
    m.set(25, 32, A.TRIPOD_TOP, False)
    m.set(25, 33, A.TRIPOD, True)
    m.cypress(24, 31)
    m.cypress(26, 31)
    for (x, y) in ((11, 27), (11, 28), (19, 27), (22, 34), (2, 34)):
        m.set(x, y, A.BOULDER_GRASS, True)
    herb(m, {(x, y) for x in range(0, 30) for y in range(25, 37) if KM._hash(x, y, 8) < 110}, salt=8)
    m.olive(27, 34)
    m.put("mitato", 20, 33)
    # ---- screen 6: the old olive grove (band 3) and the narrow approach ----
    grove(m, {(x, y) for x in range(0, 11) for y in range(36, 44)} - {(x, y) for x in range(0, 11) for y in (33, 34, 35)}
          - {(9, 36), (10, 36)}, salt=9)
    grove(m, {(x, y) for x in range(23, 30) for y in range(36, 44)} - {(23, 36), (24, 36), (23, 39), (24, 39), (25, 39),
                                                                       (24, 40), (25, 40), (26, 39)}, salt=10)
    band3 = {(x, y) for x in range(11, 23) for y in range(37, 40)} - {(11, 37), (22, 39)}
    grove(m, {(x, y) for x in range(0, 13) for y in range(44, 50)}, salt=11)
    grove(m, {(x, y) for x in range(18, 30) for y in range(44, 50)}, salt=12)
    grove(m, {(x, y) for x in range(10, 13) for y in range(41, 44)}
          | {(x, y) for x in range(18, 23) for y in range(40, 44)}, salt=13)

    road(m, spine)
    road(m, fork)
    m.path({(x, y) for (y, x0, x1) in to_vineyard for x in range(x0, x1 + 1)} - {(x, y) for x in range(15, 20)
                                                                                for y in (33, 34)},
           context={(x, y) for (y, x0, x1) in spine for x in range(x0, x1 + 1)})
    m.path({(19, 36), (20, 36), (21, 36), (22, 36)}, context={(21, 35)})
    m.meadow(band1 | band2 | band3)
    m.meadow(pasture_w, walls_in=False)
    m.meadow(pasture_e, walls_in=False)
    m.put("herm", 11, 14)
    for (x, n) in ((19, "top_L"), (20, "top"), (21, "top_R")):
        m.piece("labrys_door", n, x, 23)
    for (x, n) in ((19, "foot_L"), (20, "door"), (21, "foot_R")):
        m.piece("labrys_door", n, x, 24)
    m.seam("up")
    m.seam("down")

    # ---- events ----
    m.warp(21, 35, "MAP_KNOSSA_BULL_ROAD_HUT", 0)
    m.connect("up", -5, "MAP_KNOSSA_AMNISOS")
    m.connect("down", -14, "MAP_KNOSSA_PALACE")
    m.connect("right", 11, "MAP_KNOSSA_BRONZE_HEEL")
    m.connect("left", 21, "MAP_KNOSSA_BULL_ROAD_VINEYARD")
    T = lambda g, x, y, s, mv, sight, tid: m.obj(g, x, y, P + s, mv, trainer=True, sight=sight,  # noqa: E731
                                                 local_id=f"LOCALID_BULL_ROAD_{tid}")
    T("ICHOR_WOMAN", 19, 8, "Kerinthe", "MOVEMENT_TYPE_FACE_LEFT", 3, "KERINTHE")
    T("ICHOR_AUGUR", 10, 16, "Telemos", "MOVEMENT_TYPE_FACE_RIGHT", 3, "TELEMOS")
    T("ICHOR_YOUTH_M", 11, 19, "Euphemos", "MOVEMENT_TYPE_FACE_RIGHT", 3, "EUPHEMOS")
    T("ICHOR_SHEPHERD", 10, 27, "Boukolion", "MOVEMENT_TYPE_FACE_RIGHT", 4, "BOUKOLION")
    T("ICHOR_YOUTH_F", 19, 29, "Kybiste", "MOVEMENT_TYPE_FACE_LEFT", 3, "KYBISTE")
    T("ICHOR_HARVESTER", 5, 30, "Krokale", "MOVEMENT_TYPE_FACE_DOWN", 2, "KROKALE")
    T("ICHOR_PILGRIM", 23, 32, "Theoris", "MOVEMENT_TYPE_FACE_LEFT", 3, "THEORIS")
    T("ICHOR_HARVESTER", 22, 38, "Elais", "MOVEMENT_TYPE_FACE_LEFT", 4, "ELAIS")
    T("ICHOR_PRIESTESS", 13, 42, "Phaistia", "MOVEMENT_TYPE_FACE_RIGHT", 3, "PHAISTIA")
    m.obj("ICHOR_SHEPHERD", 8, 29, P + "Milon", "MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_BULL_ROAD_MILON")
    for i, (x, y) in enumerate(((11, 30), (18, 26), (24, 27))):
        m.obj("SPECIES(TAURIVET)", x, y, P + "Herd", "MOVEMENT_TYPE_WANDER_AROUND",
              local_id=f"LOCALID_BULL_ROAD_HERD_{i + 1}", rx=2, ry=1)
    m.obj("ICHOR_TITAN_GRUNT", 13, 46, P + "SouthGrunt", "MOVEMENT_TYPE_FACE_RIGHT",
          flag="FLAG_ICHOR_HIDE_BULL_ROAD_GRUNTS", local_id="LOCALID_BULL_ROAD_GRUNT_1")
    m.obj("ICHOR_TITAN_GRUNT", 17, 46, P + "SouthGrunt", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_BULL_ROAD_GRUNTS", local_id="LOCALID_BULL_ROAD_GRUNT_2")
    m.set(25, 9, A.GRASS, False)
    m.set(25, 8, A.GRASS, False)
    m.set(26, 8, A.GRASS, False)
    m.set(1, 25, A.GRASS, False)
    m.item_ball(25, 9, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_BULL_ROAD_ULTRA_BALL")
    m.item_ball(1, 25, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_BULL_ROAD_FULL_HEAL")
    m.item_ball(24, 34, "ITEM_MAX_POTION", "FLAG_ICHOR_ITEM_BULL_ROAD_MAX_POTION")
    m.item_ball(2, 32, "ITEM_HP_UP", "FLAG_ICHOR_ITEM_BULL_ROAD_HP_UP")
    m.item_ball(25, 40, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_BULL_ROAD_REVIVE")
    m.hidden(11, 13, "ITEM_OLIVE_OIL", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_OLIVE_OIL")
    m.hidden(10, 22, "ITEM_RELIC_SILVER", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_SILVER_OWL")
    m.hidden(23, 35, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_STAR_PIECE")
    m.hidden(10, 38, "ITEM_MAX_ETHER", "FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_MAX_ETHER")
    m.set(12, 2, A.STELE, True)
    m.sign(12, 2, P + "NorthSign")
    m.sign(11, 15, P + "Herm")
    m.sign(15, 31, P + "MilonsLine", facing="BG_EVENT_PLAYER_FACING_NORTH")
    m.sign(20, 24, P + "LabrysDoor")
    m.sign(25, 33, P + "Shrine")
    m.set(18, 41, A.STELE, True)
    m.sign(18, 41, P + "SouthSign")
    m.build(stem, starts=[(14, 0)],
            must_reach=[(15, 49, "the palace"), (29, 15, "the Heel fork"), (0, 33, "the vineyard gap"),
                        (2, 33, "the HP Up"), (25, 40, "the Revive"), (15, 32, "Milon's line")],
            views=[(14, 4), (14, 11), (18, 15), (14, 21), (15, 30), (18, 38), (15, 45)])
    print("forced grass north->south:", m.min_grass([(x, 0) for x in range(13, 17)],
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
    m.connect("right", -21, "MAP_KNOSSA_BULL_ROAD")
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
    m.meadow({(x, y) for (x, y) in beach_grass if not m.solid[y, x] and int(m.mid[y, x]) == A.GRASS},
             walls_in=False)
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
