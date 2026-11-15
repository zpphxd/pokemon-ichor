#!/usr/bin/env python3
"""Build the Arkadian climb: Route 11 (the Krathis gorge), Styx Falls, Route 12
(the cypress road over Kyllene) and the Cave of Maia (design/phase3/SCRIPT.md
beats 38-40, Part 2's rosters).

Each map is painted below in code: a ground grid (tools/ichor/maps/heights_lib.py
has the legend), then stamped with the tilesets' structures, then auto-tiled.
It writes:

  data/layouts/<Map>/{map,border}.bin and the layouts' entries in layouts.json
  data/maps/<Map>/map.json: events, connections and music
  build/render/heights/<Map>.png, _review.png (collision and events) and
  _screens.png (15 x 10 GBA screens along the road)
  design/phase3/img/<Map>.png (2x), for the director

Usage:
  /usr/bin/python3 tools/ichor/maps/heights.py            # build every map
  /usr/bin/python3 tools/ichor/maps/heights.py --shapes   # list the soft-ground
      shapes the maps use in tools/ichor/art/heights_shapes.json; then rebuild the
      tilesets (tools/ichor/art/heights_build.py) and run this again
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heights_lib as L  # noqa: E402
from heights_lib import ROOT, Map, item_ball, obj, sign, trigger, warp  # noqa: E402

IMG = ROOT / "design/phase3/img"
P = "OBJ_EVENT_GFX_ICHOR_"
MULE = "OBJ_EVENT_GFX_SPECIES(ONOTIS)"   # sprites3 draws the mules; Onotis's follower meanwhile
R11 = "Route11_KrathisGorge_EventScript_"
SF = "StyxFalls_EventScript_"
R12 = "Route12_CypressRoad_EventScript_"
CM = "Route12_CaveOfMaia_EventScript_"
ROAD_MUSIC = "MUS_ICHOR_ROAD"   # ICHOR_STUB_MUSIC: MUS_ICHOR_ARKADIAN_HEIGHTS isn't composed yet
NEVER = "VAR_TEMP_9"            # a drum's button: only a drum sets it off (never 99 on foot)

# Seams (design/phase3/BUILD.md, Batch 3)
R11_NORTH = 18      # Route 11's road leaves its north edge at 19-20 (verges 18, 21) toward Aigion
R11_SOUTH = 12      # ... and its south edge (the cleft) at 12-13
SF_NORTH = 12       # Styx Falls's cleft opens on its north edge at 12-13 (offset 0)
SF_EAST = 22        # Styx Falls's road leaves its east edge on rows 22-23
R12_WEST = 22       # ... and enters Route 12's west edge on rows 22-23 (offset 0)
R12_SOUTH = 28      # Route 12's road meets Arkadia at 28-31 (verges 28, 31): fixed


def fir_border(cat):
    return [cat.cell("fir", 0, 1)[0], cat.cell("fir", 1, 1)[0],
            cat.cell("fir_stack", 0, 0)[0], cat.cell("fir_stack", 1, 0)[0]]


def soften(m, x0, y0, x1, y1, ch, seed=0, grow=True, nibble=22):
    """Turn a rectangle of grass into a patch that follows the land: its corners
    eaten, its edges nibbled, a few cells bulging out where there's room."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if m.at(x, y) != ch:
                continue
            edge_x = x in (x0, x1)
            edge_y = y in (y0, y1)
            h = L.hsh(x, y, seed + 41)
            if (edge_x and edge_y) or ((edge_x or edge_y) and h < nibble):
                m.ch[y][x] = "."
    if grow:
        for y in range(y0, y1 + 1):
            for x in (x0 - 1, x1 + 1):
                if m.at(x, y) == "." and L.hsh(x, y, seed + 7) < 35 and y0 < y < y1:
                    m.ch[y][x] = ch
        for x in range(x0, x1 + 1):
            for y in (y0 - 1, y1 + 1):
                if m.at(x, y) == "." and L.hsh(x, y, seed + 9) < 35 and x0 < x < x1:
                    m.ch[y][x] = ch


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag}


def house(m, x, y, w, walls, roof_extra=None, eave_extra=None):
    """A Nonakris house: slab roof (ridge, eave) over a rubble wall row. `walls`
    maps a column offset to a wall cell name (door, window...)."""
    for i in range(w):
        side = "L" if i == 0 else ("R" if i == w - 1 else "M")
        m.named("houses", (roof_extra or {}).get(i, f"R0_{side}"), x + i, y)
        m.named("houses", (eave_extra or {}).get(i, f"R1_{side}"), x + i, y + 1)
        m.named("houses", walls.get(i, f"W_{side}"), x + i, y + 2)


def RL(text, width):
    """Expand run-length rows ("F27 #2 .3") into strings, checking each width."""
    rows = []
    for line in text.strip().splitlines():
        row = "".join(tok[0] * int(tok[1:]) for tok in line.split())
        assert len(row) == width, (len(row), line)
        rows.append(row)
    return rows


# ===========================================================================
# Route 11, the Krathis Gorge (40 x 56), climbing south from Aigion
# ===========================================================================

def route11():
    m = Map("Route11_KrathisGorge", 40, 56, "heights")
    m.aethos_rows = set(range(0, 6))        # Aigion's seam (the kirrha set): aethos only
    m.core_rows = set(range(50, 56))        # Styx Falls's seam: core and aethos only
    # South from Aigion: the gorge's mouth; the shelf and the fallen temple of
    # Artemis (the muleteer, the shepherd's cave up on the west wall); the three
    # drums in the narrows between the tumbled slope and the drop to the Krathis;
    # Apheidas's kiln and band 1; rim 1; terrace 2 (Auge at the narrow, band 2 on
    # her heels, the thirsty traveler at the turn); rim 2; terrace 3 (the great
    # herm at the spur fork, Pelasgos's spring, the side ravine's broken bridge,
    # the river spur and its pool); rim 3; terrace 4 (band 3 under the firs, the
    # side waterfall); rim 4; the gorge's head (Echemos, Azan at the cleft).
    m.grid([
        "...................==...................",   # 0  Aigion's seam: aethos only
        "...................==...................",
        "...................==...................",
        "...................==...................",
        "...................==...................",
        "...................==...................",   # 5
        "FFFFFFFFFF#........==......FFFFFFFFFFFFF",
        "FFFFFFFFFF#........==.......FFFFFFFFFFFF",
        "F#########.s..@@@@@@@@@@@@..FFFFFFFFFFFF",   # 8  the stylobate's north steps
        "F||||||||#s...@@@@@@@@@@@@..FFFRRRRRRRRR",   #    the shepherd's ledge, its cave
        "F||||||||.ss..@@@@@@@@@@@@...FRRRRRRRRRR",   # 10
        "F==========s..@@@@@@@@@@@@..#RRRRRRRRRRR",
        "FFFFFFFFFF.s..@@@@@@@@@@@@#RRRRFFFFFFFFF",   #    the south steps
        "FFFFFFFFFF..s......==...#RRRRRFFFFFFFFFF",
        "FFFFFFFFFF@@@@@@@@@==###RRRRFFFFFFFFFFFF",   #    the drums: the tumbled slope
        "FFFFFFFFFF@@@@@@@@@==@##RRRRFFFFFFFFFFFF",   # 15 drum 1 (20,15), its lip (21,15)
        "FFFFFFFFFF@@@@@@@@@@=###RRRRFFFFFFFFFFFF",   #    drum 2 (20,16)
        "FFFFFFFFFF@@@###@@@@@###RRRRFFFFFFFFFFFF",   #    the gap (20,17)
        "FFFFFFFFFF@@@|||======##RRRRFFFFFFFFFFFF",   #    the lane: drum 3 (19,18)
        "FFFFFFFFFF.@@|||..=...##RRRRFFFFFFFFFFFF",
        "FFFFFFFFFF.@@.....==...#RRRRFFFFFFFFFFFF",   # 20 Apheidas's kiln
        "FFFFFFFFFF.@@.....==....#RRRRFFFFFFFFFFF",
        "FFFFFFFFFF,,,,,,,,,,,,,,,#RRRRFFFFFFFFFF",   #    band 1: cliff to drop
        "FFFFFFFFFF,,,,,,,,,,,,,,,,#RRRRFFFFFFFFF",
        "FFFFFFFFFF,,,,,,,,,,,,,,,,#RRRRFFFFFFFFF",
        "FFFFFFFFFF,,,,,,,,,,,,,,,,,#RRRRFFFFFFFF",   # 25
        "FFFFFFFFFFrr@rnnnnrrrrrrrrrr#RRRRFFFFFFF",   #    rim 1
        "FFFFFFFFFF..=.........FFFFFFF#RRRRFFFFFF",   #    Auge's notch (21,27)
        "FFFFFFFFFF..==========,,,==..#RRRRFFFFFF",   #    band 2 on her heels
        "FFFFFFFFFF..==========,,,==..#RRRRFFFFFF",
        "FFFFFFFFFF...,,,,,.FFFFFF==..#RRRRFFFFFF",   # 30
        "FFFFFFFFFF...,,,,,.FFFFFF==..#RRRRFFFFFF",
        "FFFFFFFFFF....,,,,.FFFFFF==..#RRRRFFFFFF",
        "FFFFFFFFFFrrrrnnnnrrrrrrrr@rr#RRRRFFFFFF",   #    rim 2
        "FFFFFFFFFF................=@.#RRRRFFFFFF",   #    the great herm (27,34-35)
        "FFFFFFFFFF..===============@=#RRRRFFFFFF",   # 35
        "FFFFFFFFFF..===============,,~RRRRFFFFFF",   #    the spur's pool
        "FF..........==.....#####...,,~RRRRFFFFFF",
        "FF||||||||..==.@@..|||||...,,~RRRRFFFFFF",   #    the side ravine; Pelasgos's spring
        "FFvvvvvvvv..==.....|||||...,,,@@@@FFFFFF",
        "FF........#.==..b.......b..sssRRRRFFFFFF",   # 40 the Max Ether's ledge
        "FFFFFFFFFFrr@rrrrrrrnnnnrrrsssRRRRFFFFFF",   #    rim 3
        "F#.....#FFFF=FF,,,,F....FFFFF#RRRRFFFFFF",   #    the Calcium's ledge; band 3
        "F#.....#FFFF===,,,,====..FFFF#RRRRFFFFFF",
        "F#|||||#FFFF===,,,,====...FFF#RRRRFFFFFF",   #    the side waterfall
        "F#|||||#FFFF===,,,,====....FF#R@@RFFFFFF",   # 45 the Krathis's spring
        "F#|||||#FFFFFFF,,,,FFF=FFFFFF######FFFFF",
        "FsssssssFF#rrrrrrrrrrr@rnnnrr######FFFFF",   #    rim 4
        "FF......FF..===========...........FFFFFF",
        "FF......FF..=..FFFF...........,,,.FFFFFF",
        "FFFFFFFFFFF#==.FFFF.............FFFFFFFF",   # 50 Styx Falls's seam: core only
        "FFFFFFFFFFF#==.FFFF.............FFFFFFFF",   #    (two wide: Azan, come up to battle, leaves room)
        "FFFFFFFFFF##==|||||||.........FFFFFFFFFF",   #    Azan (12,53)
        "FFFFFFFFFF##=========FFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFF##=========FFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFF##==########FFFFFFFFFFFFFFFFFF",   # 55 the cleft (12-13)
    ])
    # tidy the woods' edges (ragged, staggered: MAP_DESIGN section 7)
    m.cells([(11, 6), (11, 7), (12, 6)], "F")
    m.cells([(36, 13), (37, 13)], "F")
    # pass 3, the route standard (15 grass cells a screen): optional grass with a
    # reason to go in, following the land
    R = m.rect
    for (x0, y0, x1, y1, s) in ((13, 6, 17, 7, 11), (22, 6, 26, 7, 12), (11, 30, 18, 32, 13),
                                (11, 34, 25, 34, 14), (14, 39, 18, 40, 15), (19, 40, 24, 40, 16),
                                (23, 43, 26, 45, 17), (23, 49, 33, 49, 18), (2, 48, 7, 49, 19),
                                (2, 40, 9, 40, 20), (2, 42, 6, 43, 21), (13, 27, 20, 27, 22),
                                (20, 20, 23, 21, 23), (27, 28, 28, 32, 24), (10, 35, 11, 40, 25),
                                (24, 48, 33, 48, 26), (20, 42, 23, 42, 27), (15, 20, 17, 21, 28),
                                (10, 27, 11, 29, 29), (10, 12, 13, 13, 30), (12, 30, 18, 32, 31),
                                (24, 37, 26, 40, 32), (21, 13, 23, 13, 33), (16, 19, 21, 19, 34),
                                (13, 49, 14, 49, 35), (2, 37, 9, 37, 26), (14, 37, 18, 37, 36)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if m.at(x, y) == ".":
                    m.ch[y][x] = ","
        soften(m, x0, y0, x1, y1, ",", seed=s, grow=False, nibble=0 if s < 27 else 8)
    m.cells([(3, 43), (6, 43), (5, 40), (18, 34), (12, 31), (23, 50)], ".")   # items, digs, trainers

    # --- stamps ---------------------------------------------------------------------------
    # the seam: Aigion's olives, pines and cypresses on aethos ground
    for (x, y) in ((0, 0), (4, 1), (8, 0), (12, 2), (2, 3), (6, 4), (10, 4), (14, 4),
                   (24, 1), (28, 0), (32, 2), (36, 0), (26, 4), (30, 4), (34, 4)):
        m.pine(x, y) if (x // 2) % 3 == 0 else m.olive(x, y)
    for (x, y) in ((16, 1), (23, 2), (17, 4), (22, 4), (38, 3)):
        m.acypress(x, y)
    m.put(21, 5, L.STELE)                                     # the north sign
    # the fallen temple's stylobate: steps, marble slabs, the peristyle's stumps
    for x in range(14, 26):
        m.named("ruins", "steps_W" if x < 20 else "steps_E", x, 8)
        for y in (9, 10, 11):
            m.named("ruins", "slabs", x, y)
        m.named("ruins", "steps_E" if x < 20 else "steps_W", x, 12)
    for (x, y) in ((14, 9), (14, 11), (16, 9), (23, 9), (25, 9), (25, 11), (16, 12), (23, 12)):
        m.named("ruins", "stump", x, y)
    m.named("ruins", "column_top", 17, 8)
    m.named("ruins", "column", 17, 9)
    m.named("ruins", "capital", 24, 11)
    m.named("ruins", "drum_lie", 15, 13)
    m.named("ruins", "drum_lie", 24, 13)
    m.named("ruins", "jars", 26, 12) if False else None
    # the tumbled stone slope west of the drums
    slope = [(x, y) for y in range(14, 20) for x in range(10, 21) if m.at(x, y) == "@"]
    for (x, y) in slope:
        k = L.hsh(x, y, 3) % 7
        m.named("ruins", ("rubble", "rubble_b", "rubble", "rubble_b", "capital", "stump", "drum_lie")[k], x, y)
    m.named("ruins", "lip", 21, 15)                          # drum 1's button
    m.named("ruins", "gap", 20, 17)                          # drum 2's button
    m.button(18, 18)                                          # drum 3's, on the lane
    m.button(5, 11)                                           # the cave drum's, on the ledge
    # the shepherd's cave in the ledge's face
    m.named("chasm", "in_L", 5, 9)
    m.named("chasm", "in_R", 6, 9)
    m.named("chasm", "mouth_L", 5, 10)
    m.named("chasm", "mouth_R", 6, 10)
    # Apheidas's kiln
    m.stamp("kiln", 11, 19)
    # stairs through the rims
    for (x, y) in ((12, 26), (26, 33), (12, 41), (22, 47)):
        m.named("terraces", "stair", x, y)
    # the great herm at the spur fork, Pelasgos's spring, runnels across the road
    m.named("marks", "herm_top", 27, 34)
    m.named("marks", "herm", 27, 35)
    m.named("spring", "spring_W", 15, 38)
    m.named("spring", "spring_E", 16, 38)
    m.named("spring", "runnel", 21, 35)
    m.named("spring", "runnel", 21, 36)
    m.named("spring", "runnel_g", 21, 37)
    m.named("rapids", "lip", 30, 39)
    m.named("rapids", "lip", 31, 39)
    m.named("rapids", "lip", 32, 39)
    m.named("rapids", "lip", 33, 39)
    m.named("rapids", "lip", 31, 45)
    m.named("rapids", "lip", 32, 45)
    m.named("marks", "dig", 28, 41)                           # the spur's daily dig spot
    # the plank bridge over the side ravine
    m.named("chasm", "plank", 5, 38)
    m.named("chasm", "plank_gap", 5, 39)
    # the side waterfall, the Calcium and the Star Piece on the ledge above it
    m.named("falls", "fall_top", 4, 44)
    m.named("falls", "fall_ledge", 4, 45)
    m.named("falls", "fall_foot", 4, 46)
    m.named("marks", "dig", 6, 43)
    # cypresses stand at the gorge's head
    for (x, y) in ((20, 49), (24, 49), (29, 48), (3, 48), (6, 48), (33, 48)):
        m.tree("cypress", x, y)
    # trees to break up the terraces
    m.tree("oak", 25, 37)
    m.tree("oak", 10, 31)
    m.tree("oak", 21, 50)
    m.put(10, 49, L.STELE)                                    # the south sign
    m.put(18, 13, L.STELE)                                    # ROAD CLOSED, by the drums
    # drums 1 and 2 stand on transition tiles (elevation 0), so they can roll
    # onto the lip and into the gap (elevation 1), where the player can't step
    m.elev.update({(20, 15): 0, (20, 16): 0, (21, 15): 1, (20, 17): 1, (20, 18): 0})
    m.force_open |= {(21, 15), (20, 17)}

    E = {
        "connections": [{"map": "MAP_STYX_FALLS", "offset": R11_SOUTH - SF_NORTH, "direction": "down"},
                        {"map": "MAP_AIGION", "offset": 6, "direction": "up"}],  # Aigion's road (13-14) meets ours (19-20)
        "object_events": [
            # beat 38: the muleteer and his mules, Alethea, the three drums
            obj(P + "MULETEER", 23, 13, R11 + "Muleteer", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_ROUTE11_MULETEER", local_id="LOCALID_ROUTE11_MULETEER"),
            obj(MULE, 26, 9, R11 + "Mule", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_ROUTE11_MULETEER", local_id="LOCALID_ROUTE11_MULE_1"),
            obj(MULE, 27, 10, R11 + "Mule", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_ROUTE11_MULETEER", local_id="LOCALID_ROUTE11_MULE_2"),
            obj(MULE, 26, 11, R11 + "Mule", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_ROUTE11_MULETEER", local_id="LOCALID_ROUTE11_MULE_3"),
            obj(P + "ALETHEA", 21, 13, R11 + "Alethea", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_ALETHEA_ROUTE11", local_id="LOCALID_ROUTE11_ALETHEA"),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 20, 15, "EventScript_StrengthBoulder",
                flag="FLAG_ICHOR_ROUTE11_DRUM_1", local_id="LOCALID_ROUTE11_DRUM_1", elevation=0),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 20, 16, "EventScript_StrengthBoulder",
                flag="FLAG_ICHOR_ROUTE11_DRUM_2", local_id="LOCALID_ROUTE11_DRUM_2", elevation=0),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 19, 18, "EventScript_StrengthBoulder",
                flag="FLAG_ICHOR_ROUTE11_DRUM_3", local_id="LOCALID_ROUTE11_DRUM_3"),
            # the fourth drum across the shepherd's cave
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 6, 11, "EventScript_StrengthBoulder",
                flag="FLAG_ICHOR_ROUTE11_CAVE_DRUM", local_id="LOCALID_ROUTE11_CAVE_DRUM"),
            item_ball(5, 9, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_ROUTE11_ULTRA_BALL_1"),
            item_ball(6, 9, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_ROUTE11_ULTRA_BALL_2"),
            # Apheidas at his kiln; band 1; Auge at the narrow; band 2
            obj(P + "CHARCOALER", 14, 20, R11 + "Apheidas", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True,
                sight=4),
            obj(P + "HUNTRESS", 21, 27, R11 + "Auge", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=4),
            obj(P + "MAN", 27, 31, R11 + "Traveler", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_DECOY_ROUTE11", local_id="LOCALID_ROUTE11_TRAVELER"),
            # terrace 3: Pelasgos at his spring; the spur's Super Potion; the ravine's Max Ether
            obj(P + "SHEPHERD", 17, 38, R11 + "Pelasgos", "MOVEMENT_TYPE_FACE_LEFT"),
            item_ball(29, 40, "ITEM_SUPER_POTION", "FLAG_ICHOR_ITEM_ROUTE11_SUPER_POTION"),
            item_ball(5, 40, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_ROUTE11_MAX_ETHER"),
            item_ball(3, 43, "ITEM_CALCIUM", "FLAG_ICHOR_ITEM_ROUTE11_CALCIUM"),
            # the gorge's head: Echemos facing up toward the falls; Azan at the cleft
            obj(P + "MAN", 27, 50, R11 + "Echemos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
            obj(P + "SHEPHERD", 12, 53, R11 + "Azan", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=4),
            item_ball(20, 53, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_ROUTE11_HYPER_POTION"),
            # the route standard's five more (MAP_DESIGN section 8)
            obj(P + "HUNTRESS", 12, 31, R11 + "Maira", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
            obj(P + "MAN", 18, 34, R11 + "Dryops", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
            obj(P + "SHEPHERD", 28, 39, R11 + "Psophis", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=3),
            obj(P + "CHARCOALER", 24, 44, R11 + "Amphidamas", "MOVEMENT_TYPE_FACE_LEFT", trainer=True,
                sight=3),
            obj(P + "GOATHERD", 23, 50, R11 + "Phylas", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=2),
        ],
        "warp_events": [],
        "coord_events": [
            trigger(x, 14, R11 + "DrumsScene") for x in (19, 20)
        ] + [
            trigger(21, 15, R11 + "DrumEdge", NEVER, "99"),
            trigger(20, 17, R11 + "DrumGap", NEVER, "99"),
            trigger(18, 18, R11 + "DrumRoll", NEVER, "99"),
            trigger(5, 11, R11 + "CaveDrumRoll", NEVER, "99"),
        ],
        "bg_events": [
            sign(21, 5, R11 + "SignNorth"),
            sign(18, 13, R11 + "SignDrums"),
            sign(27, 35, R11 + "GreatHerm"),
            sign(29, 35, R11 + "SignSpur"),
            sign(10, 49, R11 + "SignSouth"),
            sign(28, 41, R11 + "DigSpot"),
            sign(6, 43, R11 + "DigFixedStarPiece"),
            sign(4, 45, R11 + "SideFall"),
            sign(15, 38, R11 + "Spring"),
            sign(16, 38, R11 + "Spring"),
            sign(5, 39, R11 + "BrokenBridge"),
            sign(17, 9, R11 + "Column"),
            hidden(18, 15, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ROUTE11_REVIVE"),
            hidden(12, 21, "ITEM_CHARCOAL", "FLAG_ICHOR_HIDDEN_ROUTE11_CHARCOAL"),
            hidden(16, 9, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ROUTE11_STARDUST"),
        ],
    }
    views = [(19, 3), (19, 9), (20, 14), (18, 19), (18, 24), (14, 28), (22, 29), (25, 33),
             (19, 36), (28, 38), (8, 39), (15, 44), (5, 44), (14, 49), (14, 53)]
    return m, E, views


# ===========================================================================
# Styx Falls and Nonakris (36 x 30): the gorge's head
# ===========================================================================

def styx():
    m = Map("StyxFalls", 36, 30, "styx")
    m.core_rows = set(range(0, 6))          # Route 11's seam: core and aethos only
    m.core_cols = set(range(28, 36))        # Route 12's seam (the kyllene set)
    m.decor_rate = 4
    # Route 11's cleft comes down through the black cliff (12-13). The cliff is the
    # cirque's back wall, six rows tall; the Styx falls down it at x 23 into the
    # black pool. Nonakris stands on the western terrace: Horkia's house built
    # against the cliff, the inn, Kepheus's house. The road leaves by the cirque's
    # south side, east to Route 12 (rows 22-23).
    m.grid([
        "FFFFFFFFFF##==##FFFFFFFFFFFFFFFFFFFF",   # 0  Route 11's seam: core only
        "FFFFFFFFFF##==##FFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFF##==##FFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFF##==##FFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFF.##==##.FFFFFFFFFFFFFFFFFFF",
        "FFFFFFFF...#==#...FFFFFFFFFFFFFFFFFF",   # 5
        "!!!!!!!!!!!!==!!!!!!!!!!!!!!FFFFFFFF",   #    the black cliff
        "!!!!!!!!!!!!==!!!!!!!!!!!!!!FFFFFFFF",
        "!!!!!!!!!!!!==!!!!!!!!!!!!!!FFFFFFFF",
        "!!!!!!!!!!!!==!!!!!!!!!!!!!!FFFFFFFF",
        "!!!!!!!!!!!!==!!!!!!!!!!!!!!FFFFFFFF",   # 10
        "!!@@@.....!!==!!!!!!!!!!!!!!FFFFFFFF",   #    Horkia's house against the cliff
        "!!@@@.......==....!!!!!!!!!!FFFFFFFF",
        "!.@@@.......==......KKKKKKK!FFFFFFFF",   #    the black pool
        "!..===========.....KKKKKKKKKFFFFFFFF",
        "!......@@@@@==....KKKKKKKKKK........",   # 15 the inn
        "!......@@@@@==...@KKKKKKKKKK........",   #    the Oath Stone (17,16)
        "!......@@@@@==.....KKKKKKKKK........",
        "!wwww.========.......KKKKKK.........",
        "!@@@@@......==............@.........",   #    Kepheus's house; the hoof-cups
        "!@@@@@......==......................",   # 20
        "!@@@@@......==......................",
        "!..=================================",   #    the road out, to Route 12
        "!...........========================",
        "FF..........rrrrrrrrrrrrrrrrFFFFFFFF",   #    the cirque's south lip
        "FFF.......FFF.....FFFF..FFFFFFFFFFFF",   # 25
        "FFFFFF..FFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
    ])
    # the east edge is open only where the road leaves (rows 22-23)
    m.rect(35, 15, 35, 21, "F")
    m.rect(34, 15, 34, 15, "F")
    # the Styx: one thread down the black cliff into the pool
    for y, piece in zip(range(6, 13), ("thread_top", "thread", "thread_b", "thread", "thread_b",
                                        "thread", "thread_foot")):
        m.named("thread", piece, 23, y)
    # Nonakris
    house(m, 2, 11, 3, {1: "door"}, eave_extra={2: "cups"})                 # Horkia's
    house(m, 7, 15, 5, {1: "window", 2: "door_hoof", 4: "W_R"},             # the inn
          roof_extra={3: "chimney"}, eave_extra={1: "lamp"})
    house(m, 1, 19, 5, {1: "lean_to", 2: "sledge", 3: "door"},              # Kepheus's
          roof_extra={2: "chimney"})
    m.named("stones", "oath", 17, 16)
    m.named("stones", "hoofcups", 26, 19)
    m.put(14, 12, L.STELE)                                    # the north sign, at the cleft's foot
    m.put(16, 15, L.STELE)                                    # the Oath Stone's sign
    m.put(28, 21, L.STELE)                                    # the south path's sign
    m.named("marks", "dig", 6, 24)                            # the daily dig, the terrace's south end
    for (x, y) in ((31, 15), (34, 17), (32, 19)):
        m.tree("cypress", x, y)
    # the pool: the water's edge answers instead of the Conch (SCRIPT.md Part 4)
    pool_signs = []
    for y in range(m.h):
        for x in range(m.w):
            if m.at(x, y) != "K":
                continue
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                c = m.at(x + dx, y + dy)
                if c is not None and c in ".=@" and (x + dx, y + dy) not in m.stamped:
                    pool_signs.append(sign(x, y, SF + "Pool"))
                    break

    E = {
        "connections": [{"map": "MAP_ROUTE11_KRATHIS_GORGE", "offset": SF_NORTH - R11_SOUTH, "direction": "up"}, {"map": "MAP_ROUTE12_CYPRESS_ROAD", "offset": SF_EAST - R12_WEST, "direction": "right"}],
        "object_events": [
            # beat 39: Alethea at the Oath Stone, looking up
            obj(P + "ALETHEA", 16, 16, SF + "Alethea", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_SAW_STYX", local_id="LOCALID_STYX_ALETHEA"),
            # the muleteer filling hoof-cups at the pool, after beat 38
            obj(P + "MULETEER", 25, 19, SF + "Muleteer", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_TEMP_1", local_id="LOCALID_STYX_MULETEER"),
            obj(MULE, 29, 18, SF + "Mule", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_TEMP_1"),
            obj(P + "ELDER_M", 21, 19, SF + "OldMan", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "KID_F", 14, 18, SF + "Girl", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            item_ball(23, 20, "ITEM_SPELL_TAG", "FLAG_ICHOR_ITEM_STYX_FALLS_HOOF_CUP"),
        ],
        "warp_events": [
            warp(9, 17, "MAP_STYX_FALLS_INN", 0),
            warp(3, 13, "MAP_STYX_FALLS_OATH_HOUSE", 0),
            warp(4, 21, "MAP_STYX_FALLS_STONE_HOUSE", 0),
        ],
        "coord_events": [trigger(x, 12, SF + "StyxScene") for x in (12, 13)],
        "bg_events": [
            sign(14, 12, SF + "SignNorth"),
            sign(16, 15, SF + "SignOathStone"),
            sign(28, 21, SF + "SignSouth"),
            sign(17, 16, SF + "OathStone"),
            sign(6, 24, SF + "DigSpot"),
            hidden(18, 17, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_STYX_FALLS_OBOL"),
            hidden(11, 3, "ITEM_ETHER", "FLAG_ICHOR_HIDDEN_STYX_FALLS_ETHER"),
        ] + pool_signs,
    }
    views = [(12, 3), (12, 8), (13, 13), (20, 15), (6, 15), (5, 21), (25, 20), (31, 22)]
    return m, E, views


# ===========================================================================
# Route 12, the Cypress Road (56 x 36): over Kyllene's shoulder to Arkadia
# ===========================================================================

def route12():
    m = Map("Route12_CypressRoad", 56, 36, "kyllene")
    m.core_cols = set(range(0, 8))          # Styx Falls's seam: core and aethos only
    m.aethos_rows = set(range(30, 36))      # Arkadia's seam (the arkadia set): aethos only
    m.decor_rate = 9
    R = m.rect
    # West to east: the climb out of the cirque (Phegeus), stairs north through
    # two cliff steps onto Kyllene's shoulder; the west lobe of the meadow
    # (Aipytos among his goats); the neck between two rock walls (band 1); the
    # main meadow under the cave cliff (the great herm, the Cave of Maia,
    # Laodike); the hawk spur north (the drum, the nest, page IV) and the cliff
    # split; the east rock's hollow (the great boulder) and the east knoll
    # (Komatas); the narrow track down (Telphousa) into the cypress clearing
    # (band 2); the glade (the shrine, Basanos); the kiln (Kypselos); the
    # descent through the cypresses to Arkadia's gate.
    m.grid([
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF#######FFFFFFFFFFFFFFFFF",   # 0  the hawk's cliff
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF###@###FFFFFFFFFFFFFFFFF",   #    the nest (35,1)
        "FFFFFFFFFFFFFF###################.=;;;##################",   #    the spur's top
        "FFF##############FFFFF#####...####=;;;##################",
        "F.....==..;;;;;..##########...@====;;;##################",   #    the cliff split (30,4)
        "F.....==.;;;;;;..#################=#####################",   # 5
        "F.....==.;;;;;...#####||||||||||##@######...############",   #    the drum's gap (34,6)
        "F.....==....@@...#####||||||||||##=######...############",   #    the drum (34,7)
        "F.....===========;;;;.||||@|||||..=.######.#############",   #    the Cave of Maia (26,8)
        "F.....===========;;;;.=============....###.####......FFF",
        "F.....==.;;;;;;..;;;;..@........==.....###.####......FFF",   # 10
        "F.....==.;;;;;;..;;;;..@;;;;;;;.==...................FFF",
        "F____#@@##############..;;;;;;;.==.;;;;;......;;;;;;.FFF",
        "F....|@@||||||||||||||..;;;;;;;.==.;;;;;......;;;;;;.FFF",
        ".....F==..FFFFFFFFFFFF..;;;;;;;.==.;;;;;......;;;;;;.FFF",
        ".....F==;;FFFFFFFFFFFF..;;;;;;;.==.;;;;;......;;;;;;.FFF",   # 15
        "......==;;FFFFFFFFFFFF.;;;;;;;;.==............;;;;;;.FFF",
        "......==;;FFFFFFFFFFFF.;;;;;;;;.==...................FFF",
        "F____|@@||FFFFFFFFFFFF..........==...................FFF",
        "F....|@@||FFFFFFFFFFFFYYYYYYYYYYY=YYYYYYYYYYYYYYYYYYYYYY",
        ".;;;;.==..FFFFFFFFFFFFYYYYYYYYYYY=YYYYYYYYYYYYYYYYYYYYYY",   # 20
        ".;;;;.==..FFFFFFFF...@@....YYYYYY=,,,,....YYSSSSSSSSFFFF",
        "========..FFFFFFFF...@@....YYYYYY.,,,,===.YYSS@@SSSSFFFF",   #    Telphousa (33,22)
        "========..FFFFFFFF...@@....YYYYYYY,,,,======SS@@SSSSFFFF",
        "..........FFFFFFFF..,,,,,..YYYYYYY,,,,Y==YYYS,,,,,SSFFFF",
        "..........FFFFFFFF..,,,,,..YYYYYY.....Y==YYYS,,,,,SSFFFF",   # 25
        "FFFFFFFFFFFFFFFFFF.........YYYYYYnnnnYY==YYYSSSSSSSSFFFF",
        "FFFFFFFFFFFFFFFFFFYYYYYYYY...============YYYSSSSSSSSFFFF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFF|||@@||nnn||||||FFFFFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFF...==...........FFFFFFFFFFFFFF",
        ".............................==.........................",   # 30 Arkadia's seam: aethos only
        ".............................==.........................",
        ".............................==.........................",
        ".............................==.........................",
        ".............................==.........................",
        ".............................==.........................",   # 35
    ])
    # pass 2: firs on the high ground instead of bare rock, cliff faces below it
    R = m.rect
    R(3, 3, 16, 3, "|")                     # the west lobe's back wall
    R(17, 2, 31, 5, "F")                    # firs over the cave cliff and the neck
    R(27, 3, 29, 4, ".")                    # the split's far ledge (daily dig)
    R(30, 4, 33, 4, "=")
    m.cells([(30, 4)], "@")
    R(17, 6, 21, 7, "|")                    # the neck's north wall
    R(38, 2, 55, 5, "F")                    # the east rock: firs above a cliff
    R(39, 6, 55, 8, "|")
    R(41, 6, 43, 7, ".")                    # the hollow behind the great boulder
    m.cells([(42, 8)], ".")
    R(39, 9, 46, 11, ".")
    m.cells([(41, 9), (43, 9)], "b")
    R(32, 5, 33, 7, "#")
    R(35, 5, 38, 7, "#")
    R(36, 3, 38, 4, "F")
    m.cells([(38, 2)], "F")
    for (x0, y0, x1, y1, s) in ((9, 4, 14, 6, 1), (9, 10, 14, 11, 2), (24, 11, 30, 17, 3),
                                (35, 12, 39, 15, 4), (46, 12, 51, 17, 5), (20, 24, 24, 25, 6),
                                (45, 24, 49, 25, 7)):
        soften(m, x0, y0, x1, y1, ";" if s < 6 else ",", seed=s)
    # pass 3, the route standard: more grass by the climb and under the cypresses
    for (x0, y0, x1, y1, ch) in ((1, 24, 9, 25, ","), (1, 16, 5, 17, ","), (23, 18, 30, 18, ";"),
                                 (36, 17, 44, 18, ";"), (18, 26, 25, 26, ",")):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if m.at(x, y) == ".":
                    m.ch[y][x] = ch
    # the west edge is open only where the road comes in (rows 22-23), the south
    # edge only at the road to Arkadia's gate (28-31)
    m.cells([(0, 14), (0, 15), (0, 16), (0, 17), (0, 20), (0, 21), (0, 24), (0, 25)], "F")

    # --- stamps --------------------------------------------------------------------------
    for (x, y) in ((6, 12), (7, 12), (6, 13), (7, 13), (6, 18), (7, 18), (6, 19), (7, 19),
                   (29, 28), (30, 28)):
        m.named("terraces", "stair", x, y)                    # rock-cut steps up the cliffs
    m.named("hawk", "gap", 34, 6)
    m.named("split", "split", 30, 4)
    m.named("tortoises", "nest", 35, 1)
    m.named("cave_door", "door", 26, 8)
    m.named("marks", "herm_top", 23, 10)
    m.named("marks", "herm", 23, 11)
    m.named("marks", "dig", 28, 4)                            # across the split (daily)
    m.named("marks", "dig", 50, 10)                           # the east knoll (daily)
    m.named("marks", "dig", 25, 10)                           # the Potsherd at the cave's mouth (fixed)
    m.named("tortoises", "tort_big_L", 12, 7)
    m.named("tortoises", "tort_big_R", 13, 7)
    for (x, y) in ((10, 6), (15, 5), (27, 13), (37, 10), (42, 15), (29, 17), (44, 12), (49, 15),
                      (16, 10), (24, 17)):
        if m.at(x, y) in (".", ";"):
            m.named("tortoises", ("tort", "tort_b")[(x + y) % 2], x, y)
    m.named("shrine", "bad_top", 46, 22)
    m.named("shrine", "bad_top_R", 47, 22)
    m.named("shrine", "base", 46, 23)
    m.named("shrine", "base_R", 47, 23)
    m.stamp("kiln", 21, 21)
    m.put(5, 21, L.STELE)                                     # the west sign
    m.put(31, 31, L.STELE)                                    # the south sign
    m.put(35, 8, L.STELE)                                     # the hawk spur's sign
    m.put(21, 9, L.STELE)                                     # the cave's sign, by the herm
    # Arkadia's seam: cypresses, pines and olives on aethos ground, the road between;
    # a row of trees along the edge, so it's open only at the road (28-31)
    for x in list(range(0, 28, 2)) + list(range(32, 56, 2)):
        m.pine(x, 34) if (x // 2) % 3 == 0 else m.olive(x, 34)
    for (x, y) in ((0, 30), (4, 31), (8, 30), (12, 31), (16, 31), (20, 30), (44, 30), (48, 31),
                   (52, 30), (38, 31), (24, 31)):
        m.pine(x, y) if (x // 2) % 3 == 0 else m.olive(x, y)
    for (x, y) in ((33, 30), (19, 33), (36, 30), (27, 31), (32, 32), (11, 33), (41, 33), (46, 32),
                   (6, 32), (53, 32)):
        m.acypress(x, y)
    m.elev.update({(34, 7): 0, (34, 6): 1, (34, 5): 0})
    m.force_open |= {(34, 6)}

    E = {
        "connections": [{"map": "MAP_STYX_FALLS", "offset": R12_WEST - SF_EAST, "direction": "left"}, {"map": "MAP_ARKADIA", "offset": 6, "direction": "down"}],
        "object_events": [
            obj(P + "SHEPHERD", 9, 21, R12 + "Phegeus", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4),
            obj(P + "GOATHERD", 11, 7, R12 + "Aipytos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
            obj("OBJ_EVENT_GFX_SPECIES(KERAZAP)", 9, 7, R12 + "Goat", "MOVEMENT_TYPE_WANDER_AROUND",
                rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(KERAZAP)", 14, 10, R12 + "Goat", "MOVEMENT_TYPE_FACE_LEFT"),
            obj(P + "HUNTRESS", 37, 2, R12 + "Loxo", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2),
            obj(P + "YOUTH_F", 27, 10, R12 + "Laodike", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=0),
            obj(P + "GOATHERD", 48, 12, R12 + "Korythos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3),
            obj(P + "HUNTRESS", 33, 22, R12 + "Telphousa", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1),  # sight 1: walking up she would plug the track
            obj(P + "CHARCOALER", 23, 23, R12 + "Kypselos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=1),
            obj(P + "TITAN_GRUNT", 46, 24, R12 + "Basanos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 34, 7, "EventScript_StrengthBoulder",
                flag="FLAG_ICHOR_ROUTE12_HAWK_DRUM", local_id="LOCALID_ROUTE12_HAWK_DRUM", elevation=0),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 42, 9, "EventScript_IchorGreatBoulder",
                local_id="LOCALID_ROUTE12_GREAT_BOULDER"),
            item_ball(42, 6, "ITEM_RARE_CANDY", "FLAG_ICHOR_ITEM_ROUTE12_RARE_CANDY"),
            item_ball(49, 16, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_ROUTE12_HYPER_POTION"),
            item_ball(50, 22, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_ROUTE12_FULL_HEAL"),
        ],
        "warp_events": [warp(26, 8, "MAP_ROUTE12_CAVE_OF_MAIA", 0)],
        "coord_events": [trigger(34, 6, R12 + "HawkDrumStep", NEVER, "99")],
        "bg_events": [
            sign(5, 21, R12 + "SignWest"),
            sign(31, 31, R12 + "SignSouth"),
            sign(35, 8, R12 + "SignHawk"),
            sign(21, 9, R12 + "SignCave"),
            sign(23, 11, R12 + "GreatHerm"),
            sign(35, 1, R12 + "HawkNest"),
            sign(28, 4, R12 + "DigSpot"),
            sign(50, 10, R12 + "DigSpot"),
            sign(25, 10, R12 + "DigPotsherd"),
            sign(30, 4, R12 + "CliffSplit"),
            sign(46, 23, R12 + "Shrine"),
            sign(47, 23, R12 + "Shrine"),
            sign(13, 7, R12 + "TortoiseBoulder"),
            sign(27, 13, R12 + "TortoiseBoulder"),
            hidden(33, 8, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_HIDDEN_ROUTE12_PRETTY_FEATHER"),
            hidden(12, 7, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_ROUTE12_HEART_SCALE"),
            hidden(22, 11, "ITEM_HONEY", "FLAG_ICHOR_HIDDEN_ROUTE12_HONEY"),
        ],
    }
    views = [(3, 22), (7, 16), (8, 9), (18, 9), (26, 11), (34, 4), (43, 10), (48, 14), (33, 19),
             (36, 23), (46, 24), (22, 24), (30, 28), (29, 33)]
    return m, E, views


# ===========================================================================
# The Cave of Maia (20 x 11): where Hermes was born
# ===========================================================================

def cave():
    m = Map("Route12_CaveOfMaia", 20, 11, "maia")
    # Shallow and dry, wider than deep. The back wall: the cradle niche, the
    # tortoise-shell lyre above it. By the entrance, the altar of Hermes and his
    # face carved in an outcrop. The priestess's lamp, stool and jar.
    m.grid([
        "####################",
        "####################",
        "###||||||||||||||###",   #    the back wall: the lyre (9,2)
        "##||||||||||||||||##",   #    the cradle niche (9-10,3)
        "#..................#",
        "#..................#",   # 5
        "#..................#",
        "##...........##....#",   #    the herm's outcrop (13-14,7-8)
        "###..........||...##",
        "#######....#########",
        "#########..#########",   # 10 the way out (9-10,10)
    ])
    m.named("maia", "lyre", 8, 3)
    m.named("maia", "cradle_L", 9, 3)
    m.named("maia", "cradle_R", 10, 3)
    m.named("maia", "herm_face", 13, 8)
    m.named("maia", "altar_L", 15, 7)
    m.named("maia", "altar_R", 16, 7)
    m.named("maia", "lamp", 5, 4)
    m.named("maia", "stool", 4, 5)
    m.named("maia", "jar", 16, 4)
    m.named("maia", "spring", 17, 5)
    m.named("cfloor", "exit", 9, 10)
    m.named("cfloor", "exit", 10, 10)
    E = {
        "object_events": [
            obj(P + "PRIESTESS", 5, 5, CM + "Priestess", "MOVEMENT_TYPE_FACE_DOWN",
                local_id="LOCALID_MAIA_PRIESTESS"),
            obj(P + "ALETHEA", 10, 4, CM + "Alethea", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_HIDE_ALETHEA_MAIA", local_id="LOCALID_MAIA_ALETHEA"),
            obj(P + "MAN", 3, 7, CM + "Euandros", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
            # pilgrims' leavings at the cave's two dead ends (the route standard's two items)
            item_ball(1, 4, "ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_MAIA_MAX_REPEL"),
            item_ball(18, 4, "ITEM_LEPPA_BERRY", "FLAG_ICHOR_ITEM_MAIA_LEPPA_BERRY"),
        ],
        "warp_events": [warp(9, 10, "MAP_ROUTE12_CYPRESS_ROAD", 0), warp(10, 10, "MAP_ROUTE12_CYPRESS_ROAD", 0)],
        "coord_events": [trigger(x, 9, CM + "AletheaScene") for x in (9, 10)],
        "bg_events": [
            sign(8, 3, CM + "Lyre"),
            sign(9, 3, CM + "Cradle"),
            sign(10, 3, CM + "Cradle"),
            sign(13, 8, CM + "HermFace"),
            sign(15, 7, "EventScript_IchorAltar_Hermes"),
            sign(16, 7, "EventScript_IchorAltar_Hermes"),
            sign(5, 4, CM + "Lamp"),
            hidden(11, 3, "ITEM_PP_UP", "FLAG_ICHOR_HIDDEN_MAIA_PP_UP"),
            hidden(16, 4, "ITEM_FRESH_WATER", "FLAG_ICHOR_HIDDEN_MAIA_FRESH_WATER"),
        ],
    }
    return m, E, [(9, 9), (9, 5), (15, 6)]


# ===========================================================================
# Running the builds
# ===========================================================================

MAPS = {
    "route11": ("LAYOUT_ROUTE11_KRATHIS_GORGE", "Route11_KrathisGorge", route11, ROAD_MUSIC, None),
    "styx": ("LAYOUT_STYX_FALLS", "StyxFalls", styx, ROAD_MUSIC, None),
    "route12": ("LAYOUT_ROUTE12_CYPRESS_ROAD", "Route12_CypressRoad", route12, ROAD_MUSIC, None),
    "cave": ("LAYOUT_ROUTE12_CAVE_OF_MAIA", "Route12_CaveOfMaia", cave, "MUS_ICHOR_HOLLOW", None),
}
BORDERS = {"cave": lambda c: [c.named("cwall", "1|11111111")[0]] * 4}
ENTRIES = {"route11": [(19, 0), (20, 0)], "styx": [(12, 0), (13, 0)], "route12": [(0, 22), (0, 23)],
           "cave": [(9, 10), (10, 10)]}
EXITS = {"route11": [(12, 55), (13, 55)], "styx": [(35, 22), (35, 23)], "route12": [(29, 35), (30, 35)]}
UNREACHABLE_OK = {
    "route11": {(5, 40), (3, 43), (6, 43), (4, 45)},
    "route12": {(42, 6), (28, 4), (30, 4)},        # behind the great boulder; across the split
}
# Cells scripts open (drums moved, the gap filled) for the reach check
OPENS = {"route11": {(20, 15), (20, 16), (19, 18), (6, 11), (20, 17)},
         "route12": {(34, 7), (34, 6)}}


def check(key, m, E):
    people = {(o["x"], o["y"]) for o in E.get("object_events", [])
              if o["script"] != "Common_EventScript_FindItem"}
    opens = OPENS.get(key, set())
    m.force_open |= opens
    seen = L.reach(m, ENTRIES[key], blocked_extra=people - opens)
    bad = []
    targets = [(o["x"], o["y"], o["script"].split("_")[-1]) for o in E.get("object_events", [])]
    targets += [(b["x"], b["y"], b.get("script", b.get("item", "?")).split("_")[-1]) for b in E.get("bg_events", [])]
    for (x, y, what) in targets:
        near = {(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))}
        if not (near & seen) and (x, y) not in UNREACHABLE_OK.get(key, ()):
            bad.append(f"{what}@{x},{y}")
    if key in EXITS and not (set(EXITS[key]) & seen):
        bad.append("THE FAR EXIT")
    print(f"  {m.name}: {len(seen)} cells reachable" + (f"; OUT OF REACH: {', '.join(bad)}" if bad else ""))
    # A trainer who spots the player walks over and stays there until the map
    # reloads: from every tile they can spot the player on, the player must still
    # reach everything they could before (a trainer must never plug a narrow way).
    facing = {"MOVEMENT_TYPE_FACE_UP": (0, -1), "MOVEMENT_TYPE_FACE_DOWN": (0, 1),
              "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}
    for o in E.get("object_events", []):
        d = facing.get(o.get("movement_type"))
        if o.get("trainer_type") != "TRAINER_TYPE_NORMAL" or not d:
            continue
        t = (o["x"], o["y"])
        for k in range(2, int(o.get("trainer_sight_or_berry_tree_id") or 0) + 1):
            p = (t[0] + d[0] * k, t[1] + d[1] * k)
            if p not in seen:
                break
            stop = (p[0] - d[0], p[1] - d[1])
            before = L.reach(m, [p], blocked_extra=people - opens)
            after = L.reach(m, [p], blocked_extra=(people - opens - {t}) | {stop})
            cut = before - after - {stop}
            if cut:
                print(f"  {m.name}: TRAINER PLUGS THE WAY: {o['script'].split('_')[-1]} spots the player at "
                      f"{p}, stops at {stop} and cuts off {len(cut)} cells")
                break
    m.force_open -= opens
    if key in EXITS:
        forced, _ = L.forced_bands(m, ENTRIES[key], EXITS[key], people - opens, opens)
        print(f"  {m.name}: forced grass bands: " +
              ("; ".join(f"x {a}-{b}, y {c}-{d} ({n} cells)" for a, b, c, d, n in forced) or "NONE"))


def build(only=None, shapes_only=False, tag=""):
    built = {}
    missing = []
    for key, (layout, folder, fn, music, extra) in MAPS.items():
        if only and key not in only:
            continue
        m, E, views = fn()
        m.missing = missing
        L.RENDER.mkdir(parents=True, exist_ok=True)
        (L.RENDER / f"{m.name}.txt").write_text(
            "\n".join(f"{y:2d} " + "".join(r) for y, r in enumerate(m.ch)) + "\n")
        m.autotile()
        built[key] = (m, E, views, layout, folder, music, extra)
    if shapes_only:
        data = json.loads(L.SHAPES.read_text()) if L.SHAPES.exists() else {}
        fresh = {}
        for kind in L.SHAPE_SETS:
            used = set(data.get(kind, [])) if only else set()
            for (m, *_rest) in built.values():
                used |= m.shapes_used[kind]
            if used:
                fresh[kind] = sorted(used)
            elif kind in data:
                fresh[kind] = data[kind]
        L.SHAPES.write_text(json.dumps(fresh, indent=1) + "\n")
        print({k: len(v) for k, v in fresh.items()}, "->", L.SHAPES.relative_to(ROOT))
        return
    if missing:
        print(f"{len(missing)} shape cells drawn with stand-ins: run --shapes, rebuild the art")
    errs = []
    for key, (m, *_r) in built.items():
        errs += m.check_seams()
    if errs:
        sys.exit("seam errors:\n  " + "\n  ".join(errs[:20]))
    for key, (m, E, views, layout, folder, music, extra) in built.items():
        border = BORDERS.get(key, fir_border)(m.cat)
        L.write_layout(layout, folder, m, border)
        L.write_events(folder, E, music, extra)
        L.render(m, E, border, views, tag)
        IMG.mkdir(parents=True, exist_ok=True)
        shutil.copy2(L.RENDER / f"{m.name}{tag}.png", IMG / f"{folder}.png")
        print(f"{folder}: {m.w}x{m.h} -> {(IMG / f'{folder}.png').relative_to(ROOT)}")
        check(key, m, E)
    return built


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    build(args.only.split(",") if args.only else None, args.shapes, args.tag)


if __name__ == "__main__":
    main()
