#!/usr/bin/env python3
"""Build the Ascent: Olympus from the sea to the Pantheon's door (design/LEAGUE.md).

  Ascent_1F  the Pierian slopes: three terraces over the sea, the beacon knoll
  Ascent_2F  the cloud ledges: cliff traverses in the fog, the ex-Titanborn camp
  Ascent_3F  the snowline: walled terraces and the processional stair

All three are aethos + gTileset_Skiron (design/phase2/TILES_skiron.md), built
with tools/ichor/maps/league_lib.py, and connected top to bottom (they share a
secondary, so the seams need no aethos-only strip).

Usage: /usr/bin/python3 tools/ichor/maps/ascent.py [--render DIR] [--walk] [--tag TAG]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import league_lib as L  # noqa: E402
from league_lib import (A_HERM, A_SIGN, A_STEPS, A_TRIPOD_BASE, A_TRIPOD_TOP, A_PALAESTRA,  # noqa: E402
                        A_PALAESTRA_DOOR, Grid, bank_run, ground, massif, noise, rockland, sea_cliff, woods)

PX1, PX2, PX3 = "Ascent_1F_EventScript_", "Ascent_2F_EventScript_", "Ascent_3F_EventScript_"

# The seams: 1F's exit road (x 4-6) runs into 2F's entry (same columns, offset 0);
# 2F's exit (x 30-32) into 3F's entry.
SEAM12 = (4, 6)
SEAM23 = (30, 32)


def pine_border(g):
    s = g.cat["pine_tall"]
    return [s["ids"][1][0] | 0x400, s["ids"][1][1] | 0x400, s["ids"][2][0] | 0x400, s["ids"][2][1] | 0x400]


def rock_border(g):
    s = g.cat["boulders"]
    return [s["ids"][0][0] | 0x400, s["ids"][0][1] | 0x400, s["ids"][1][0] | 0x400, s["ids"][1][1] | 0x400]


# ---------------------------------------------------------------------------
# 1F: the Pierian slopes
# ---------------------------------------------------------------------------
W1, H1 = 48, 40


def build_1f():
    g = Grid("Ascent_1F", W1, H1)
    g.fill("wood", 0, 0, W1 - 1, H1 - 1)
    g.fill("sea", 0, 34, W1 - 1, H1 - 1)

    # --- leg A, the coast road (from the east road end west to the bend) -----------
    g.fill("grass", 2, 24, 45, 29)
    g.fill("path", 3, 27, 44, 28)
    g.fill("road", 40, 26, 45, 28)           # the Tempe road comes in paved
    g.fill("road", 2, 25, 6, 28)             # the west bend, paved under the stelai
    g.rows("tall", 26, 24, ["..###.",
                            ".#####",
                            "######",
                            "######",
                            ".####."])       # forced band 1, round the herm's rock
    g.rows("tall", 8, 28, ["..#####", "#######"])
    # the brink: scrub and rock break the cliff's line
    g.rows("wood", 2, 29, ["###.....##.........#.............##.......####"])
    g.rows("crag", 19, 28, ["..", ".."])
    # --- the west cutting through bank 1 -------------------------------------------
    g.fill("road", 3, 21, 5, 24)
    # --- leg B ----------------------------------------------------------------
    g.fill("grass", 2, 12, 44, 22)
    g.fill("path", 3, 19, 5, 20)
    g.fill("path", 5, 19, 40, 20)
    g.fill("path", 14, 21, 24, 21)
    g.rows("tall", 2, 13, [".####.....",
                           "#######...",
                           "########..",
                           "#######...",
                           ".#####...."])     # the pine meadow at the bend
    g.rows("tall", 14, 19, ["######", "######", "######", "..####"])   # forced band 2, the squeeze
    g.rows("tall", 31, 13, ["...####.....",
                            "..######....",
                            ".#######....",
                            "..#####.....",
                            "...##......."])
    g.rows("scree", 32, 14, ["......##", ".....###", "....###.", "..####..", ".####..."])
    g.fill("path", 39, 13, 41, 20)
    g.rows("wood", 6, 12, ["###", "##.", "#.."])
    g.rows("wood", 2, 18, ["##", "#."])
    g.rows("wood", 42, 12, ["...", "..#", ".##", "..#", "#..", "#..", "#..", "##.", "###", "###", "###"])
    # the knoll: x 14-30 over its bank, the cleft at x 22 (the drum)
    g.fill("grass", 14, 12, 30, 15)
    g.fill("path", 22, 16, 22, 18)
    # --- leg C ----------------------------------------------------------------
    g.fill("grass", 2, 3, 44, 10)
    g.fill("path", 40, 6, 42, 9)
    g.fill("road", 40, 9, 42, 13)            # the east cutting through bank 2
    g.fill("path", 8, 5, 41, 6)
    g.rows("scree", 3, 0, [".#####.", ".#####.", ".#####.", "######.", "#######", "######.", ".####.."])
    g.fill("road", 4, 0, 6, 5)               # the old road up into the cloud
    g.rows("tall", 17, 3, ["..###..", ".#####.", "#######", "#######", "#######", ".#####."])  # band 3
    g.rows("tall", 27, 3, ["######", ".####."])
    g.rows("scree", 32, 3, ["....####", "...####.", "..####..", ".####...", "####...."])  # the torrent bed
    g.fill("path", 32, 5, 37, 6)             # the road fords it
    g.rows("wood", 2, 3, ["#", "#", ".", ".", ".", "##", "###", "###"])
    g.rows("wood", 8, 3, ["######...........#######..................."])
    g.rows("wood", 9, 2, ["####"])
    g.rows("wood", 24, 7, ["##", "###", "##"])
    g.rows("wood", 43, 3, ["##", "##", "##", "#.", "#."])
    g.rows("crag", 38, 3, ["....", ".%%.", "...."])
    g.fill("wood", 46, 23, 47, 29)           # the rockfall closing the Tempe road

    # --- banks, stepped -------------------------------------------------------
    bank_run(g, 0, 9, 11, ends=(False, True))
    bank_run(g, 10, 20, 9, ends=(True, True))
    bank_run(g, 21, 31, 11, ends=(True, True))
    bank_run(g, 32, 39, 10, ends=(True, True))
    bank_run(g, 43, 47, 11, ends=(True, False))
    bank_run(g, 0, 2, 22, ends=(False, True))
    bank_run(g, 6, 15, 22, ends=(True, True))
    bank_run(g, 16, 24, 23, ends=(True, True))
    bank_run(g, 25, 34, 21, ends=(True, True))
    bank_run(g, 40, 47, 22, ends=(True, False))
    bank_run(g, 14, 21, 16, ends=(True, True))
    bank_run(g, 23, 30, 16, ends=(True, True))
    sea_cliff(g, 0, W1 - 1, 30, faces=3)
    # the shortcut: a grass slope down to a terrace lip, leg B to leg A
    for x in range(35, 40):
        for y in (21, 22, 23):
            g.g[y][x] = "grass"
    g.named("lip", "W", 35, 24)
    for x in range(36, 39):
        g.named("lip", "run", x, 24)
    g.named("lip", "E", 39, 24)
    # the Pierian spring: a thin fall down bank 2 into a pool, under the Muses' niches
    g.piece("niches", 26, 11)
    for y in (12, 13):
        g.set(29, y, 0x0B3 if y == 12 else 0x0BB, True, "fall")
    g.set(29, 11, 0x0B9, True, "fall")
    g.stamp(28, 14, [[0x0C8, 0x0C1, 0x0CA], [0x0D8, 0x0D9, 0x0DA]], solid=False, kind="pool")
    for x in (28, 29, 30):
        for y in (14, 15):
            g.water[y, x] = True
    g.solid[14, 29] = True

    # --- set pieces ------------------------------------------------------------
    g.piece("watchtower", 16, 12)                        # the beacon tower on the knoll
    g.piece("boulders", 19, 12)
    g.piece("stele_family", 7, 24)                       # the fallen climbers at the west bend
    g.piece("stele_palmette", 9, 24)
    g.piece("lekythos", 10, 24)
    g.piece("mound", 11, 24)
    g.piece("stele_low", 14, 25)
    g.piece("stele_low", 7, 26)
    g.piece("milestone", 39, 26)
    g.piece("milestone", 13, 21)
    g.piece("milestone", 31, 7)
    g.piece("cart", 43, 28 - 0)
    g.piece("rock_seat", 23, 24)                         # the guard's seat over the gulf
    g.piece("pine_lean_w", 22, 12)
    g.rows("crag", 27, 7, ["##..", "###.", ".##."])     # boulders where the torrent spreads
    g.piece("pine_tall", 35, 7)
    # the goatherd's fold on the torrent's far bank: a dry-stone pen, two goats
    for x in range(38, 42):
        g.named("terrace_wall", "W" if x == 38 else "E" if x == 41 else "run", x, 7)
    g.named("terrace_wall", "steps", 40, 7)
    g.piece("hives", 38, 4) if False else None
    g.piece("bedrolls", 42, 8)
    # the bend's meadow: an outcrop and a leaning pine frame it
    g.piece("boulders", 9, 16)
    g.piece("pine_lean", 10, 13)
    g.rows("crag", 25, 3, ["##", "#."])
    for x, y in ((6, 36), (17, 37), (31, 35), (40, 36)):
        g.piece("surf_rock", x, y)
    for x, y in ((25, 29), (33, 29), (15, 8), (26, 10), (36, 3), (17, 3)):
        g.piece("rock", x, y)
    g.piece("boulders", 44, 26)
    g.piece("pine_tall", 11, 13)
    g.piece("pine_young", 13, 14)
    g.piece("pine_lean", 36, 21)
    g.set(28, 26, A_HERM, True, "herm")
    woods(g)
    rockland(g)
    ground(g, thyme=10)

    # --- events ---------------------------------------------------------------
    g.person("PHILON", "TITAN_GRUNT", 35, 26, "Philon", facing="DOWN", sight=3)
    g.person("LAMPON", "HOPLITE", 20, 18, "Lampon", facing="DOWN", sight=3)
    g.person("THEANO", "AUGUR", 41, 15, "Theano", facing="LEFT", sight=4)
    g.person("KALLIAS", "TITAN_GRUNT", 9, 7, "Kallias", facing="LEFT", sight=4)
    g.person("MULETEER", "MAN", 44, 27, "Muleteer", facing="LEFT")
    g.person("GOAT", "OBJ_EVENT_GFX_SPECIES(KERAZAP)", 45, 26, "Goat", facing="LEFT")
    g.person("FOLD_GOAT_A", "OBJ_EVENT_GFX_SPECIES(ERIPIP)", 39, 6, "FoldGoat", movement="MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1)
    g.person("GOATHERD", "GOATHERD", 42, 6, "Goatherd", facing="LEFT")
    g.obstacle("DRUM", "drum", 22, 17)
    g.item("ITEM_FULL_RESTORE", 21, 14, "FLAG_ICHOR_ITEM_ASCENT1_FULL_RESTORE")
    g.item("ITEM_ULTRA_BALL", 43, 18, "FLAG_ICHOR_ITEM_ASCENT1_ULTRA_BALL")
    g.item("ITEM_MAX_REPEL", 37, 4, "FLAG_ICHOR_ITEM_ASCENT1_MAX_REPEL")
    g.hidden("ITEM_STARDUST", 8, 25, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT1_STARDUST")
    g.set(41, 25, A_SIGN, True, "sign")
    g.sign(41, 25, PX1 + "RoadSign")
    g.sign(16, 15, PX1 + "Beacon")
    g.sign(17, 15, PX1 + "Beacon")
    g.sign(7, 25, PX1 + "Stelai")
    g.sign(27, 13, PX1 + "Niches", facing="NORTH")
    g.sign(28, 26, PX1 + "Herm")
    g.set(7, 4, A_SIGN, True, "sign")
    g.sign(7, 4, PX1 + "CloudSign")
    g.save(pine_border(g), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SUNNY", show_map_name=True,
                                allow_cycling=False, music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_2F", offset=0, direction="up")])
    must = [("muleteer", (44, 27)), ("exit", (5, 0)), ("knoll item", (21, 14)), ("ultra ball", (43, 18)),
            ("max repel", (37, 4)), ("theano", (41, 15)), ("stelai", (8, 25)), ("beacon", (16, 15)),
            ("niches", (27, 13))]
    seen = g.check((44, 26), must)
    return g, seen, [("01_road_end", 40, 27), ("02_band1", 29, 27), ("03_stelai", 8, 26),
                     ("04_cutting", 5, 20), ("05_squeeze", 18, 20), ("06_knoll", 22, 14),
                     ("07_torrent", 36, 16), ("08_east_cut", 41, 9), ("09_band3", 22, 6),
                     ("10_exit", 6, 3), ("11_meadow", 6, 15), ("12_spring", 29, 15)]


# ---------------------------------------------------------------------------
# 2F: the cloud ledges
# ---------------------------------------------------------------------------
W2, H2 = 40, 44


def build_2f():
    g = Grid("Ascent_2F", W2, H2)
    g.fill("mass", 0, 0, W2 - 1, H2 - 1)
    # the drop: cloud and the sea far below, east of the landing
    g.fill("sea", 10, 41, W2 - 1, H2 - 1)
    # --- the landing, where 1F's road comes up into the cloud ---------------------
    g.fill("scree", 2, 36, 9, 43)
    g.fill("road", 4, 39, 6, 43)
    g.rows("crag", 2, 36, ["#.......", "##......", "#.......", "........",
                           "##....##", "##....##", "#.....##", "#.....##"])
    # --- ledge 1: a traverse east along the face, rows 35-36 ----------------------
    g.fill("path", 4, 35, 37, 36)
    g.fill("tall", 18, 35, 21, 36)                  # mountain grass on the ledge: no way round
    g.fill("tall", 27, 35, 28, 36)
    g.fill("scree", 33, 30, 38, 36)                 # the scree fan up the gully
    g.fill("path", 34, 29, 36, 34)
    # --- ledge 2 and the camp under the overhang, rows 22-30 ----------------------
    g.fill("dry", 2, 22, 16, 30)
    g.fill("path", 3, 28, 38, 29)
    g.fill("dry", 17, 26, 38, 30)
    g.fill("mass", 17, 26, 39, 26)
    g.rows("mass", 30, 27, ["..####...."])
    g.rows("tall", 19, 27, ["..#####...", "#########.", ".######..."])
    g.rows("scree", 29, 27, [".##.......", "####..##..", "##..####..", ".........."])
    g.rows("crag", 17, 30, ["##.....###...##......"])
    g.rows("scree", 20, 12, [])
    g.fill("path", 6, 17, 8, 27)                    # up out of the camp
    # --- ledge 3: an alpine shelf, rows 12-17 -------------------------------------
    g.fill("dry", 2, 12, 34, 17)
    g.fill("path", 6, 14, 31, 15)
    g.rows("tall", 12, 12, [".######.",
                            "########",
                            "########",
                            "########",
                            ".######.",
                            "..####.."])            # the forced band
    g.rows("tall", 24, 12, ["....##", "..####"])
    g.rows("scree", 22, 15, ["..####...", ".######..", "..###...."])
    g.rows("scree", 3, 15, [".###", "####"])
    g.rows("crag", 2, 12, ["###", "##.", "#..", "...", "#..", "##."])
    g.rows("crag", 33, 12, ["##", "##", "#.", "#.", "##", "##"])
    g.fill("dry", 17, 9, 22, 11)                    # a pocket behind the rubble
    g.fill("path", 29, 7, 31, 13)
    # --- ledge 4: the light through the cloud, the way to 3F ----------------------
    g.fill("dry", 14, 2, 36, 7)
    g.fill("road", 30, 0, 32, 6)
    g.fill("path", 18, 5, 31, 6)
    g.rows("crag", 14, 2, ["####......", "##........", "#.........", "##........", "###......."])
    g.rows("crag", 34, 2, ["###", "##.", "#..", "##.", "###", "###"])
    g.rows("tall", 20, 2, [".###", "####"])
    # --- the faces ---------------------------------------------------------------
    bank_run(g, 0, 24, 31, ends=(False, True), tall=True)    # over ledge 1
    bank_run(g, 28, 32, 31, ends=(True, True), tall=True)
    for x in range(25, 28):                                    # a scree slope: the way back down
        for y in (31, 32, 33):
            g.g[y][x] = "scree"
        g.named("lip", "W" if x == 25 else "E" if x == 27 else "run", x, 34)
    bank_run(g, 37, 39, 31, ends=(True, False), tall=True)
    sea_cliff(g, 10, W2 - 1, 37, faces=2)                     # under ledge 1, into the cloud
    bank_run(g, 0, 5, 18, ends=(False, True), tall=True)     # the overhang's back wall
    bank_run(g, 9, 16, 18, ends=(True, True), tall=True)
    bank_run(g, 17, 39, 22, ends=(True, False), tall=True)    # over ledge 2, east
    bank_run(g, 0, 16, 8, ends=(False, True))
    bank_run(g, 17, 22, 6, ends=(True, True))                 # behind the rubble pocket
    bank_run(g, 23, 28, 8, ends=(True, True))
    bank_run(g, 32, 39, 8, ends=(True, False))
    # --- the camp ----------------------------------------------------------------
    g.piece("tent", 3, 22)
    g.piece("tent_b", 11, 22)
    g.piece("cookfire", 8, 25)
    g.piece("bedrolls", 6, 24)
    g.piece("bedrolls", 10, 25)
    g.piece("baskets", 14, 23)
    g.piece("firewood", 3, 26)
    g.piece("amphorae", 15, 25)
    g.stamp(2, 29, [[0x0C8, 0x0C9, 0x0CA], [0x0D8, 0x0D9, 0x0DA]], solid=False, kind="pool")  # the spring
    for x in (2, 3, 4):
        for y in (29, 30):
            g.water[y, x] = True
    g.piece("pine_young", 25, 26)
    g.piece("pine_tall", 15, 12)
    for x, y in ((13, 35), (30, 35), (21, 36), (36, 29), (19, 29), (11, 16), (26, 16), (22, 5),
                 (14, 17), (22, 17), (29, 17), (28, 36), (35, 36), (23, 35), (24, 2), (10, 30)):
        g.piece("rock", x, y)                                  # fallen stones break the ledges' lines
    massif(g)
    rockland(g)
    ground(g, thyme=0)
    g.solid |= g.water
    g.water[:] = False

    # --- events ------------------------------------------------------------------
    g.person("AGATHE", "TITAN_GRUNT", 25, 35, "Agathe", facing="DOWN", sight=1)
    g.person("NIKIAS", "PILGRIM", 30, 27, "Nikias", facing="LEFT", sight=3)
    g.person("EIRENE", "ACOLYTE_F", 22, 13, "Eirene", facing="DOWN", sight=2)
    g.person("DEXIOS", "TITAN_GRUNT", 28, 5, "Dexios", facing="DOWN", sight=1)
    g.person("COOK", "TITAN_GRUNT", 9, 26, "Cook", facing="UP")
    g.person("SITTER", "TITAN_GRUNT", 7, 26, "Sitter", facing="RIGHT")
    g.person("WATCHER", "TITAN_GRUNT", 14, 28, "Watcher", facing="LEFT")
    g.obstacle("RUBBLE", "rubble", 20, 12)
    g.item("ITEM_MAX_REVIVE", 37, 35, "FLAG_ICHOR_ITEM_ASCENT2_MAX_REVIVE")
    g.item("ITEM_PP_MAX", 19, 10, "FLAG_ICHOR_ITEM_ASCENT2_PP_MAX")
    g.hidden("ITEM_BIG_NUGGET", 5, 35, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT2_BIG_NUGGET")
    g.hidden("ITEM_ELIXIR", 14, 22, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT2_ELIXIR")
    g.set(8, 37, A_SIGN, True, "sign")
    g.sign(8, 37, PX2 + "LedgeSign")
    g.sign(8, 25, PX2 + "Cookfire")
    g.save(rock_border(g), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_FOG_HORIZONTAL", show_map_name=False,
                                allow_cycling=False, music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_1F", offset=0, direction="down"),
                        dict(map="MAP_ASCENT_3F", offset=0, direction="up")])
    must = [("entry", (5, 43)), ("exit", (31, 0)), ("max revive", (37, 35)), ("pp max", (19, 10)),
            ("cook", (9, 26)), ("hidden", (5, 35)), ("nikias", (30, 27))]
    seen = g.check((5, 43), must, blocked=[(20, 12)])
    return g, seen, [("01_landing", 5, 39), ("02_ledge1", 18, 35), ("03_gully", 34, 32),
                     ("04_ledge2", 24, 28), ("05_camp", 8, 25), ("06_shelf", 14, 14),
                     ("07_rubble", 21, 11), ("08_top", 26, 4)]


# ---------------------------------------------------------------------------
# 3F: the snowline and the processional stair
# ---------------------------------------------------------------------------
W3, H3 = 36, 40


def stair(g, x0, x1, y0, y1):
    """Marble steps cut through a bank: walkable, the bank's ends on either side."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g.set(x, y, A_STEPS[(y - y0) % 2], False, "steps")


def build_3f():
    g = Grid("Ascent_3F", W3, H3)
    g.fill("mass", 0, 0, W3 - 1, H3 - 1)
    # --- the entry from the cloud ledges -----------------------------------------
    g.fill("scree", 27, 33, 34, 39)
    g.fill("road", 30, 34, 32, 39)
    g.rows("crag", 27, 34, ["##.....#", "#......#", "##....##", "##....##", "###...##", "###...##"])
    # --- terrace 1 (rows 26-33) ---------------------------------------------------
    g.fill("dry", 2, 26, 34, 33)
    g.fill("path", 6, 29, 32, 30)
    g.fill("path", 30, 29, 32, 33)
    g.rows("tall", 17, 26, [".####.", "######", "######", "######", "######", "######", ".####.", "..##.."])
    g.rows("scree", 22, 26, ["..####..", ".#######", "..#####.", "...###.."])
    g.rows("scree", 3, 26, ["....####", "...######", "..#######"])
    g.rows("scree", 9, 31, ["######", "..####"])
    g.rows("crag", 2, 31, ["###.......", "####....##", "#####..###"])
    g.rows("crag", 24, 31, ["...##.", "..####"])
    g.fill("path", 6, 26, 8, 28)
    # --- terrace 2 (rows 18-22) ---------------------------------------------------
    g.fill("dry", 1, 18, 34, 22)
    g.fill("path", 6, 19, 29, 20)
    g.fill("path", 27, 18, 29, 19)
    g.rows("tall", 11, 18, ["...####...", ".#######..", "#########.", "..########", "....####.."])
    g.rows("scree", 6, 21, ["#####", ".###."])
    g.rows("scree", 21, 21, ["#####...", ".######."])
    g.rows("crag", 31, 18, ["####", "###.", "##..", "###.", "####"])
    g.fill("mass", 5, 18, 5, 18)
    # the pocket behind the drum and the rubble (x 1-3)
    g.rows("mass", 1, 18, ["####", "#.##", "....", "####", "####"])
    # --- terrace 3, the processional terrace (rows 11-14) ------------------------
    g.fill("dry", 1, 11, 34, 14)
    g.fill("road", 13, 11, 22, 14)
    g.fill("path", 23, 12, 29, 14)
    g.rows("crag", 30, 11, ["#####", "##..#", "#...#", "##.##"])
    g.rows("scree", 2, 11, [".#####..", "########", ".####..."])
    # --- the platform before the propylaia (rows 2-7) ----------------------------
    g.fill("dry", 9, 4, 26, 7)
    g.fill("road", 12, 6, 23, 7)
    g.rows("crag", 9, 4, ["###.......#####.###", "##..........#....##", "#..................", "##.................."])
    # --- banks and stairs ----------------------------------------------------------
    bank_run(g, 0, 5, 23, ends=(False, True), tall=False)
    bank_run(g, 9, 29, 23, ends=(True, True))
    bank_run(g, 33, 35, 23, ends=(True, False))
    for x in range(30, 33):                                    # a terrace lip: the quick way down
        for y in (23, 24):
            g.g[y][x] = "dry"
        g.named("lip", "W" if x == 30 else "E" if x == 32 else "run", x, 25)
    stair(g, 6, 8, 23, 25)
    bank_run(g, 0, 26, 15, ends=(False, True))
    bank_run(g, 30, 35, 15, ends=(True, False))
    stair(g, 27, 29, 15, 17)
    bank_run(g, 0, 14, 8, ends=(False, True), tall=False)
    bank_run(g, 21, 35, 8, ends=(True, False))
    stair(g, 15, 20, 8, 10)
    # the propylaia: the palaestra's colonnade, the Pantheon's gatehouse
    g.stamp(15, 2, A_PALAESTRA)
    px, py = 15 + A_PALAESTRA_DOOR[0], 2 + A_PALAESTRA_DOOR[1]
    g.solid[py, px] = False
    for x in (13, 22):
        g.set(x, 5, A_TRIPOD_TOP, False, "tripod")
        g.set(x, 6, A_TRIPOD_BASE, True, "tripod")
    for x in (14, 21):
        g.set(x, 11, A_TRIPOD_TOP, False, "tripod")
        g.set(x, 12, A_TRIPOD_BASE, True, "tripod")
    g.set(12, 13, A_HERM, True, "herm")
    g.set(23, 13, A_HERM, True, "herm")
    # cairns of the snowline
    g.piece("boulders", 33, 26)
    g.piece("rock", 2, 12)
    g.piece("pine_young", 10, 26)
    g.piece("pine_young", 25, 18)
    g.piece("pine_tall", 3, 26)
    for x, y in ((14, 26), (27, 26), (10, 18), (21, 18), (8, 11), (28, 14), (16, 33), (24, 22),
                 (5, 14), (10, 14), (25, 14), (12, 22), (18, 22), (20, 26)):
        g.piece("rock", x, y)                                  # cairns along the terraces
    massif(g)
    rockland(g)
    ground(g, thyme=0)

    # --- events ------------------------------------------------------------------
    g.person("STHENELOS", "HOPLITE", 5, 27, "Sthenelos", facing="RIGHT", sight=3)
    g.person("GORGO", "TITAN_GRUNT", 26, 18, "Gorgo", facing="RIGHT", sight=3)
    g.person("MELITE", "ACOLYTE_F", 24, 12, "Melite", facing="LEFT", sight=3)
    g.obstacle("DRUM", "drum", 2, 20)
    g.obstacle("RUBBLE", "rubble", 4, 20)
    g.item("ITEM_RARE_CANDY", 2, 19, "FLAG_ICHOR_ITEM_ASCENT3_RARE_CANDY")
    g.item("ITEM_FULL_HEAL", 3, 13, "FLAG_ICHOR_ITEM_ASCENT3_FULL_HEAL")
    g.hidden("ITEM_COMET_SHARD", 32, 27, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_COMET_SHARD")
    g.hidden("ITEM_STAR_PIECE", 25, 5, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_STAR_PIECE")
    g.warp(px, py, "Olympus_Propylaia", 0)
    g.set(26, 33, A_SIGN, True, "sign")
    g.sign(26, 33, PX3 + "SnowSign")
    g.sign(12, 13, PX3 + "Herm")
    g.sign(23, 13, PX3 + "Herm")
    g.set(19, 7, A_SIGN, True, "sign") if False else None
    g.save(rock_border(g), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SNOW", show_map_name=False,
                                allow_cycling=False, music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_2F", offset=0, direction="down")])
    must = [("entry", (31, 39)), ("door", (px, py + 1)), ("full heal", (3, 13)), ("comet", (32, 27)),
            ("melite", (24, 12))]
    seen = g.check((31, 39), must)
    return g, seen, [("01_entry", 30, 34), ("02_terrace1", 18, 29), ("03_stair1", 7, 26),
                     ("04_terrace2", 16, 20), ("05_pocket", 5, 20), ("06_stair2", 27, 16),
                     ("07_procession", 18, 13), ("08_propylaia", 18, 5)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", help="write review renders to this directory")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--tag", default="")
    ap.add_argument("--only", default="1F,2F,3F")
    args = ap.parse_args()
    builders = {"1F": build_1f, "2F": build_2f, "3F": build_3f}
    for key in args.only.split(","):
        if key not in builders:
            continue
        g, seen, views = builders[key]()
        if g.missing:
            print(f"{g.name}: soft-ground shapes not in the tileset (drawn plain): {sorted(g.missing)[:12]}")
        if args.walk:
            print(g.walk_text(seen))
        if args.render:
            print(L.render(g, args.render, views, args.tag))


if __name__ == "__main__":
    main()
