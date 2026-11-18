#!/usr/bin/env python3
"""Astyra, its harbor and the Akropolis: the awe pass, items 1 and 2.

A dedicated builder (the old tools/ichor/maps/astyra.py rebuilt every Act II
road and stripped objects; this one touches only these three maps). It lays
each map from gTileset_Astyra / gTileset_Akropolis (tools/ichor/art/
astyra_build.py) and the aethos primary, keeps every story event (the same
local ids, scripts, flags, items and warps in the same order), checks the
maps (kythera_maps.Map.check: reachable warps, people on open ground, signs
readable, the Route 16 seam aethos-only) and renders them.

    /usr/bin/python3 tools/ichor/maps/astyra_capital.py            # all three
    /usr/bin/python3 tools/ichor/maps/astyra_capital.py --no-render

Then run tools/ichor/maps/town_herms.py (it re-adds Astyra's herm and plaque).

Sentences (STYLE.md §4.6):
  Astyra     a capital under its Akropolis: the rock and its wall across the
             north, Promachos's spear and the Parthenon's pediment over it,
             the Panathenaic Way climbing from the Dipylon gate past the agora
             to the rock-cut stair.
  Akropolis  a switchback ramp up the rock to the Propylaia, and through it
             the bronze Athena, the Parthenon on its krepis, the Erechtheion's
             maidens and the Old Temple lying in its foundations.
  Harbor     the city's harbor under its wall: a quay, ship sheds, the salt
             spring's sea-door in the rock.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import astyra_tiles  # noqa: E402
import kythera_maps as KM  # noqa: E402
from kythera_maps import A, Map  # noqa: E402

KM.KT = astyra_tiles
KM.IMG = ROOT / "design/awe/img"

HERM, STELE, STEPS, EXIT_MAT = 0x01B, 0x003, 0x0AF, 0x024
LEDGE_S = 0x087
ANEMONE = 0x004


def events(name):
    return json.loads((ROOT / "data/maps" / name / "map.json").read_text())


def keep_obj(m, src, local_id, x, y, **kw):
    """Copy an object event from the old map.json by local id (or script), at a new place."""
    for o in src["object_events"]:
        if o.get("local_id") == local_id or (local_id.startswith("script:") and o["script"] == local_id[7:]):
            e = dict(o)
            e["x"], e["y"] = x, y
            e.update(kw)
            m.objects.append(e)
            return e
    raise SystemExit(f"no object {local_id}")


def row(m, key, names, x, y):
    for i, n in enumerate(names):
        m.piece(key, n, x + i, y)


def scatter_ground(m, cells, salt=0):
    """Grass variety (STYLE §4.2): deep shade in clumps under buildings and a
    few anemone beds; the rest plain."""
    for (x, y) in cells:
        if int(m.mid[y, x]) != A.GRASS or m.solid[y, x]:
            continue
        h = KM._hash(x, y, salt)
        if h < 40:
            m.set(x, y, ANEMONE, False)
        elif h < 140:
            m.set(x, y, A.SHADE, False)


# ==========================================================================
# Astyra
# ==========================================================================

def stoa_front(m, x0, y0, width, door_at):
    """The Stoa of the Archon: pedimented wings of 3 at each end, the long tiled
    roof between, a colonnade of painted bays, the door at x = door_at, the
    step in front with herms standing on it every few bays."""
    k = "stoa"
    inner = width - 6
    row(m, k, ["P_L", "P_M", "P_R"], x0, y0)
    row(m, k, ["Q_L", "Q_M", "Q_R"], x0, y0 + 1)
    row(m, k, ["P_L", "P_M", "P_R"], x0 + width - 3, y0)
    row(m, k, ["Q_L", "Q_M", "Q_R"], x0 + width - 3, y0 + 1)
    row(m, k, ["RT_L"] + ["RT_M"] * (inner - 2) + ["RT_R"], x0 + 3, y0)
    row(m, k, ["RB_L"] + ["RB_M"] * (inner - 2) + ["RB_R"], x0 + 3, y0 + 1)
    bays = ["C_M", "C_M2", "C_M3"]
    for i in range(width):
        x = x0 + i
        if i == 0:
            c, b = "C_L", "B_L"
        elif i == width - 1:
            c, b = "C_R", "B_R"
        elif x == door_at:
            c, b = "C_door", "B_door"
        else:
            c = bays[(i * 2) % 3] if i not in (2, width - 3) else "C_L" if i == 2 else "C_R"
            b = "B" + c[1:]
        m.piece(k, c, x, y0 + 2)
        m.piece(k, b, x, y0 + 3)
        s = "S_L" if i == 0 else "S_R" if i == width - 1 else ("S_M2" if i % 2 else "S_M")
        m.piece(k, s, x, y0 + 4)
    # herms on the step (the Stoa of the Herms), and to break the long edge
    for i in range(4, width - 2, 6):
        if x0 + i != door_at:
            m.set(x0 + i, y0 + 4, HERM, True)


def house_block(m, x, y, w, kind, windows=(), jar=None, on_path=False):
    """A courtyard-house block w wide: kind 'low' (flat roof terrace over one
    storey, 2 rows), 'one' (pitched roof, one storey, 3 rows) or 'two'
    (pitched roof over an upper storey, 4 rows). Blank walls; life is inside."""
    k = "house"
    rows_ = []
    if kind == "low":
        rows_ = [["F_L"] + ["F_M"] * (w - 2) + ["F_R"]]
    else:
        rows_ = [["RT_L"] + ["RT_M"] * (w - 2) + ["RT_R"], ["RB_L"] + ["RB_M"] * (w - 2) + ["RB_R"]]
        if kind == "two":
            rows_.append(["U_L"] + ["U_M"] * (w - 2) + ["U_R"])
    wall = ["W_L"] + ["W_M"] * (w - 2) + ["W_R"]
    for i in windows:
        wall[i] = "W_win"
    if jar is not None:
        wall[jar] = "W_jar"
    rows_.append(wall)
    for j, r in enumerate(rows_):
        row(m, k, r, x, y + j)
    return len(rows_)


def city(render=True):
    src = events("Astyra")
    m = Map("Astyra", "astyra", 48, 48, fill=A.GRASS)
    m.border = [0x00E, 0x016, 0x016, 0x00E]          # cypress, the woods beyond the walls
    m.header = {"music": src["music"]}

    # --- the rock: plateau, skyline, the wall, the cliff ------------------------------------
    m.rect(8, 0, 43, 5, A.PATH, True)
    m.put("skyline_promachos", 13, 0)
    m.put("skyline_parthenon", 22, 1)
    # the wall along the rock's edge, the gate at x 11 over the rock-cut stair
    GATE = 11
    for x in range(8, 43):
        name = "L" if x == 8 else "R" if x == 42 else "gate" if x == GATE else \
            "gate_L" if x == GATE - 1 else "gate_R" if x == GATE + 1 else ("M_b" if x % 7 == 3 else "M")
        m.piece("akro_wall", name, x, 5)
    # the cliff: three rows of face under the wall, the foot on the grass; it
    # bulges a row lower in places, so its foot steps (no straight edge > 6)
    bulge = {x for x in range(8, 43) if (x // 5) % 2 == 1 and x not in range(GATE - 1, GATE + 2)}
    for x in range(8, 43):
        sfx = "_W" if x == 8 else "_E" if x == 42 else ""
        face = ("face" + sfx) if sfx else ("face" if x % 2 else "face_b")
        foot = ("foot" + sfx) if sfx else ("foot" if x % 2 else "foot_b")
        last = 9 if x in bulge else 8
        for y in range(6, last + 1):
            m.piece("cliff", face, x, y)
        m.piece("cliff", foot, x, last + 1)
    for y in (6, 7, 8):
        m.piece("rock_stair", "face", GATE, y)
    m.piece("rock_stair", "foot", GATE, 9)
    # the woods round the rock's shoulders, and over the whole west strip (aethos only)
    wood = {(x, y) for y in range(0, 10) for x in range(0, 8)} | {(x, y) for y in range(0, 10) for x in range(43, 48)}
    wood |= {(x, y) for y in range(10, 31) for x in range(0, 8)} | {(x, y) for y in range(37, 48) for x in range(0, 8)}
    wood -= {(5, 37)}
    m.woods(wood, salt=3, singles=[])

    # --- the city wall: west run, the Dipylon, the south run and the harbor gate -------------
    WX = 8
    m.piece("city_wall", "v_end_N", WX, 11)
    for y in range(12, 44):
        if 29 <= y <= 37:
            continue
        m.piece("city_wall", "v", WX, y)
    # the Dipylon: two towers astride the wall line, the road between them
    for ty in (29, 36):
        m.piece("city_wall", "tower_TL", 8, ty)
        m.piece("city_wall", "tower_TR", 9, ty)
        m.piece("city_wall", "tower_BL", 8, ty + 1)
        m.piece("city_wall", "tower_BR", 9, ty + 1)
    SY = 44
    for x in range(9, 48):
        if x == 25:
            m.piece("city_wall", "gate_top", x, SY)
            m.piece("city_wall", "gate_face", x, SY + 1)
            continue
        if x in (23, 24, 26, 27):
            n = {23: ("tower_TL", "tower_BL"), 24: ("tower_TR", "tower_BR"), 26: ("tower_TL", "tower_BL"),
                 27: ("tower_TR", "tower_BR")}[x]
            m.piece("city_wall", n[0], x, SY)
            m.piece("city_wall", n[1], x, SY + 1)
            continue
        m.piece("city_wall", "h_top", x, SY)
        m.piece("city_wall", "h_face_b" if x % 6 == 2 else "h_face", x, SY + 1)
    m.piece("city_wall", "tower_TR", WX, SY)
    m.piece("city_wall", "tower_BR", WX, SY + 1)

    # --- streets ---------------------------------------------------------------------------
    paths = set()
    paths |= {(x, y) for x in range(0, 48) for y in range(32, 36)}       # the Dipylon road
    for y in range(10, 32):                                               # the Panathenaic Way
        x0 = 15 if y >= 27 else 14 if y >= 22 else 13 if y >= 18 else 11
        paths |= {(x0 + i, y) for i in range(3)}
    paths |= {(x, y) for x in range(11, 42) for y in (10, 11)}            # the Peripatos under the rock
    paths |= {(x, 17) for x in range(12, 42)}                             # the street before the stoas
    paths |= {(x, y) for x in range(17, 34) for y in range(18, 23)}       # the agora's paving
    paths |= {(x, y) for x in range(20, 30) for y in range(23, 28)}
    paths |= {(x, y) for x in range(24, 27) for y in range(36, 48)}       # the harbor road
    paths |= {(x, 41) for x in range(9, 47)}                              # the lane between the blocks
    paths |= {(x, y) for x in range(43, 46) for y in range(18, 32)}       # up the Pnyx's east side
    m.path({p for p in paths if not m.solid[p[1], p[0]]})
    m.set(25, 47, EXIT_MAT, False)

    # --- the Stoa of the Archon, the Library, the fountain house, the agora ------------------
    STOA_X, STOA_W, DOOR = 15, 18, 24
    stoa_front(m, STOA_X, 12, STOA_W, DOOR)
    m.put("library", 35, 12)
    m.put("fountain", 31, 18)
    m.put("altar", 18, 19)
    m.put("kodros", 17, 23)
    m.put("kairos", 27, 23)
    m.put("stall", 21, 27)
    m.put("stall", 28, 27)
    for (x, y) in ((33, 24), (33, 28), (18, 28)):
        m.olive(x, y)
    for (x, y) in ((16, 19), (13, 24), (19, 17 - 1 + 1), (30, 26)):
        if not m.solid[y, x]:
            m.set(x, y, HERM, True)                     # herms where the ways cross

    # --- the Asclepeion by the gate, Phaedon's house, the asty ------------------------------
    m.put("asclepeion", 10, 28)
    house_block(m, 19, 29, 4, "one", windows=(3,))       # Phaedon and Elpis
    m.piece("house", "door", 20, 31)
    house_block(m, 9, 12, 2, "one")
    house_block(m, 9, 18, 3, "two", windows=(1,))
    house_block(m, 9, 23, 3, "low", windows=(1,), jar=2)
    house_block(m, 10, 37, 5, "one", windows=(2,), jar=4)
    house_block(m, 16, 37, 7, "two", windows=(1, 5))
    house_block(m, 28, 37, 5, "low", windows=(2,))
    house_block(m, 34, 37, 6, "two", windows=(2, 4), jar=1)
    house_block(m, 41, 36, 6, "one", windows=(3,))
    house_block(m, 10, 42, 5, "low", jar=1)
    house_block(m, 16, 42, 7, "low", windows=(3,))
    house_block(m, 28, 42, 6, "low", windows=(1,))
    house_block(m, 35, 42, 6, "low", jar=4)
    house_block(m, 42, 42, 5, "low", windows=(2,))
    house_block(m, 36, 26, 5, "one", windows=(2,))
    house_block(m, 36, 29, 5, "low", jar=3)
    house_block(m, 43, 11, 5, "two", windows=(1, 3))
    house_block(m, 43, 15, 5, "low")

    # --- the Pnyx: terraces east of the agora, the speaker's platform on top -----------------
    for y in (22, 25):
        for x in range(38, 43):
            m.set(x, y, LEDGE_S, True)
    m.put("bema", 39, 19)
    for y in (18, 20, 22, 24, 26, 28, 30):
        m.cypress(46, y)

    # --- the Kerameikos outside the Dipylon (aethos only: x < 8) -----------------------------
    for x in (1, 3, 5, 7):
        m.set(x, 31, STELE, True)
    for x in (2, 4, 6):
        m.set(x, 36, STELE, True)
    for x in (2, 6):
        m.cypress(x, 29)
    m.piece("kerameikos", "stub", 12, 36)
    m.piece("kerameikos", "poppies", 13, 36)
    m.piece("kerameikos", "plinth_feet", 14, 36)
    m.set(10, 36, STELE, True)
    m.set(0, 31, A.SHADE, True)                         # the road's verges meet Route 16's trees
    m.set(0, 36, A.SHADE, True)
    scatter_ground(m, [(x, y) for y in range(10, 44) for x in range(9, 47)], salt=5)
    # cypresses outside the south wall, herms along the Peripatos (STYLE: a step,
    # a notch or an object every 6 cells)
    for x in (12, 18, 30, 37, 42):
        m.olive(x, 46)
    for x in (18, 23, 29):
        m.set(x, 11, HERM, True)

    # --- events -------------------------------------------------------------------------------
    m.warp(12, 31, "MAP_ASTYRA_ASCLEPEION", 0)
    m.warp(20, 31, "MAP_ASTYRA_PHAEDONS_HOUSE", 0)
    m.warp(38, 15, "MAP_ASTYRA_LIBRARY", 0)
    m.warp(DOOR, 15, "MAP_ASTYRA_STOA", 0)
    m.warp(GATE, 5, "MAP_ASTYRA_AKROPOLIS", 0)
    m.warp(25, 47, "MAP_ASTYRA_HARBOR", 0)
    keep_obj(m, src, "LOCALID_ASTYRA_PREACHER", 22, 24)
    keep_obj(m, src, "LOCALID_ASTYRA_HERALD", 27, 18)
    keep_obj(m, src, "LOCALID_ASTYRA_MERCHANT", 23, 28)
    keep_obj(m, src, "LOCALID_ASTYRA_ALETHEA", 30, 23)
    keep_obj(m, src, "LOCALID_ASTYRA_CLERK", DOOR + 2, 17)
    keep_obj(m, src, "LOCALID_ASTYRA_GUARD", GATE + 1, 10)
    keep_obj(m, src, "LOCALID_ASTYRA_MULETEER", 43, 33)
    keep_obj(m, src, "LOCALID_ASTYRA_KERYKOS", 25, 22)
    m.item_ball(5, 37, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_ASTYRA_KERAMEIKOS")
    m.hidden(30, 21, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ASTYRA_AGORA")
    m.hidden(42, 19, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ASTYRA_PNYX")
    m.sign(10, 36, "Astyra_EventScript_Sign")
    m.sign(14, 31, "Astyra_EventScript_ClinicSign")
    m.sign(22, 31, "Astyra_EventScript_HouseSign")
    m.sign(37, 17, "Astyra_EventScript_LibrarySign")
    m.set(37, 17, STELE, True)
    m.sign(17, 25, "Astyra_EventScript_Kodros")
    m.sign(27, 25, "Astyra_EventScript_Kairos")
    m.sign(GATE + 3, 9, "Astyra_EventScript_Perdix")
    m.sign(40, 20, "Astyra_EventScript_Bema")
    m.sign(33, 20, "Astyra_EventScript_Fountain")
    for y in (32, 33, 34, 35):
        m.trigger(1, y, "Astyra_EventScript_Reveal")
    m.connect("left", 22, "MAP_ROUTE16_CAPITAL_PASS")
    m.seam("left", 8)
    views = [(7, 33), (14, 21), (24, 14), (25, 5), (38, 15), (12, 30), (25, 38), (40, 22), (25, 44)]
    must = [(25, 46, "the harbor road"), (42, 33, "the Ascent's landing"), (4, 33, "the herm's landing")]
    return m.build("astyra", [(0, 33)], must_reach=must, views=views, render=render)


# ==========================================================================
# The harbor
# ==========================================================================

def harbor(render=True):
    src = events("Astyra_Harbor")
    m = Map("Astyra_Harbor", "astyra", 32, 24, fill=A.SEA)
    m.border = [A.SEA] * 4
    m.header = {"music": src["music"]}
    # the west rock and its sea-door
    for y in range(24):
        for x in range(0, 8):
            m.piece("cliff", "rock", x, y)
        m.piece("cliff", "face_E", 7, y)
    m.put("sea_door", 7, 11)
    # the city behind its wall: roofs over the harbor wall (rows 0-2)
    m.rect(18, 0, 31, 2, A.PATH, True)
    house_block(m, 18, 0, 6, "one", windows=(2,))
    house_block(m, 24, 1, 3, "low")
    house_block(m, 27, 0, 5, "one", windows=(1, 3))
    for x in range(18, 32):
        n = "L" if x == 18 else "R" if x == 31 else "gate" if x == 26 else \
            "gate_L" if x == 25 else "gate_R" if x == 27 else ("M_b" if x % 5 == 0 else "M")
        m.piece("akro_wall", n, x, 3)
    # the quay: north basin, the pier, the south quay with the ship sheds
    land = {(x, y) for x in range(19, 32) for y in range(4, 11)}
    land |= {(x, y) for x in range(20, 30) for y in range(11, 18)}
    land |= {(x, y) for x in range(17, 20) for y in range(12, 13)}
    for (x, y) in land:
        m.set(x, y, A.PATH, False)
    # a worn verge of grass under the wall, the rest open quay
    verge = {(x, 4) for x in range(19, 32) if x not in (25, 26, 27)} | {(x, 5) for x in range(19, 24)}
    for (x, y) in verge:
        m.set(x, y, A.GRASS, False)
    m.path(land - verge, context={(x, y) for x in range(32) for y in range(24)} - verge)
    for x in (20, 21, 22):
        m.set(x, 5, LEDGE_S, True)                      # the verge's terrace lip
    for (x, y) in ((1, 13), (3, 6), (5, 19)):
        pass
    for (x, y, mid) in ((8, 3, 0x0C5), (9, 17, 0x0CD), (8, 21, 0x18C), (14, 6, 0x194), (12, 20, 0x0C5),
                        (10, 7, 0x0CD), (15, 22, 0x18C)):
        m.set(x, y, mid, True)                          # sea rocks at the cliff's foot
    for (x, y) in ((11, 2), (13, 15), (9, 9)):
        m.set(x, y, 0x14E, False)                       # a ruffle of current
    # the west rock is a stepped mass: ledges of face and foot in it
    for (x0, y0, w) in ((1, 4, 4), (2, 15, 4), (0, 20, 3)):
        for i in range(w):
            m.piece("cliff", "face" if i % 2 else "face_b", x0 + i, y0)
            m.piece("cliff", "foot" if i % 2 else "foot_b", x0 + i, y0 + 1)
    # quay edges where the land meets the sea
    for y in range(4, 11):
        m.piece("quay", "W", 18, y)
    for x in range(19, 32):
        if x < 20 or x > 29:
            m.piece("quay", "N", x, 11)
    for y in range(11, 18):
        m.piece("quay", "W", 19, y) if y not in (12,) else None
        m.piece("quay", "E", 30, y)
    m.piece("quay", "S", 16, 11)
    m.piece("quay", "S", 17, 11)
    m.piece("quay", "S", 18, 11)
    m.piece("quay", "N", 17, 13)
    m.piece("quay", "N", 18, 13)
    m.piece("quay", "steps", 16, 12)
    for x in range(20, 30):
        m.piece("quay", "N", x, 18)
    # ship sheds on the south quay, their slips running into the water
    m.put("ship_shed", 21, 16)
    m.put("ship_shed", 25, 16)
    for (x, y) in ((22, 5), (28, 9), (20, 14)):
        m.piece("quay", "bollard", x, y)
    m.piece("quay", "ring", 29, 15)
    # a harbor stall and the herm of the harbor
    m.put("stall", 28, 5)
    m.set(23, 4, HERM, True)
    # events, the same as before
    m.warp(26, 3, "MAP_ASTYRA", 5)
    keep_obj(m, src, "LOCALID_ASTYRA_HARBOR_MARINER", 25, 12)
    for o in src["object_events"]:
        if o.get("script") == "Common_EventScript_FindItem":
            e = dict(o)
            e["x"], e["y"] = 28, 13
            m.objects.append(e)
    for b in src["bg_events"]:
        e = dict(b)
        if b.get("script") == "Astyra_Harbor_EventScript_SeaDoor":
            e["x"], e["y"] = 7, 12
        elif b.get("script") == "Astyra_Harbor_EventScript_Sign":
            e["x"], e["y"] = 27, 4
            m.set(27, 4, STELE, True)
        elif b.get("flag") == "FLAG_ICHOR_HIDDEN_ASTYRA_HARBOR_SALT":
            e["x"], e["y"] = 19, 9
        elif b.get("flag") == "FLAG_ICHOR_HIDDEN_ASTYRA_HARBOR_SCALE":
            e["x"], e["y"] = 24, 15
        m.bgs.append(e)
    views = [(24, 6), (12, 12), (24, 14)]
    must = [(24, 13, "the ferry landing"), (10, 12, "the dolphin's water")]
    return m.build("astyra_harbor", [(26, 4)], must_reach=must[:1], views=views, render=render)


# ==========================================================================
# The Akropolis
# ==========================================================================

AK_W, AK_H = 44, 54
OLIVE = (16, 6)                 # the olive's top-left cell (2 x 2), its tip in row 5
WELL, TRIDENT, CLEFT = (22, 5), (21, 5), (20, 4)
PASSAGE = 19                    # the Propylaia's passage column
ENTRY = (22, 53)


def pave_cells(m, cells, salt=0):
    """Lay the paved way over `cells` (a set of path cells): each takes the
    9-patch piece its neighbors call for, so the kerb wraps every edge and
    every prop standing in the way; a few flags are cracked (`C2`). Slivers
    one cell thick and scraps under four cells stay worn path."""
    cells = set(cells)
    while True:
        thin = {(x, y) for (x, y) in cells
                if not ((x, y - 1) in cells or (x, y + 1) in cells)
                or not ((x - 1, y) in cells or (x + 1, y) in cells)}
        if not thin:
            break
        cells -= thin
    seen = set()
    for c in sorted(cells):
        if c in seen:
            continue
        comp, todo = set(), [c]
        while todo:
            p = todo.pop()
            if p in comp or p not in cells:
                continue
            comp.add(p)
            todo += [(p[0] + dx, p[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        seen |= comp
        if len(comp) < 4:
            cells -= comp
    for (x, y) in cells:
        n, s_, w, e = ((x, y - 1) in cells, (x, y + 1) in cells, (x - 1, y) in cells, (x + 1, y) in cells)
        v = "T" if not n else "B" if not s_ else ""
        h_ = "L" if not w else "R" if not e else ""
        name = (v + h_) or ("C2" if KM._hash(x, y, salt) < 70 else "C")
        m.piece("pave", name, x, y)


def votive_at(m, kind, x, y):
    """A votive statue (kouros or kore), 1 x 2: the figure at (x, y), its plinth below."""
    m.piece("votive", kind + "_top", x, y)
    m.piece("votive", kind, x, y + 1)


def brazier_at(m, x, y):
    m.piece("brazier", "fire", x, y)
    m.piece("brazier", "stand", x, y + 1)


def akropolis(render=True):
    src = events("Astyra_Akropolis")
    m = Map("Astyra_Akropolis", "akropolis", AK_W, AK_H, fill=A.PATH)
    m.border = [astyra_tiles.mid("akropolis", "cliff", "rock")] * 4
    m.header = {"music": src["music"]}
    rock = astyra_tiles.mid("akropolis", "cliff", "rock")
    m.rect(0, 0, AK_W - 1, AK_H - 1, rock, True)

    # --- the plateau (rows 0-26) --------------------------------------------------------------
    m.rect(2, 2, 41, 26, A.PATH, False)
    for x in range(2, 42):
        m.piece("edge", "wall_N_drums" if x % 7 == 3 else "wall_N", x, 0)
        m.piece("edge", "wall_N_face_d" if x % 7 == 3 else "wall_N_face", x, 1)
    for y in range(0, 27):
        m.piece("edge", "edge_W", 1, y)
        m.piece("edge", "edge_E", 42, y)
    # the Pandroseion: a patch of grass round Athena's olive
    grass = {(x, y) for x in range(14, 20) for y in range(5, 10)}
    # the sacred grove on its terrace, south-east, its lip a ledge down to the rim walk
    grove = {(x, y) for x in range(33, 41) for y in range(18, 26)}
    for (x, y) in grass | grove:
        m.set(x, y, A.GRASS, False)
    plateau = {(x, y) for x in range(2, 42) for y in range(2, 27)}
    m.path({(x, y) for x in range(13, 21) for y in range(4, 11)} - grass, context=plateau - grass)
    m.path({(x, y) for x in range(31, 42) for y in range(16, 27)} - grove, context=plateau - grove)
    for x in range(33, 38):
        m.set(x, 25, A.LEDGE["SL"] if x == 33 else A.LEDGE["SR"] if x == 37 else A.LEDGE["S"], True)
    m.olive(*OLIVE)
    # Poseidon's marks and the salt spring
    m.piece("spring", "trident", *TRIDENT)
    m.piece("spring", "well_shut", *WELL)
    m.piece("spring", "cleft", *CLEFT)
    m.forced_open.add(WELL)
    # the Erechtheion and its maidens, north-west; the Parthenon north-east; the altar before it
    m.put("erechtheion", 3, 2)
    m.put("parthenon", 26, 4)
    m.put("altar", 31, 14)
    # the Old Temple's foundations, its two standing columns and its fallen drums in one heap
    fx0, fy0, fx1, fy1 = 3, 11, 11, 17
    for y in range(fy0, fy1 + 1):
        for x in range(fx0, fx1 + 1):
            v = "T" if y == fy0 else "B" if y == fy1 else ""
            h = "L" if x == fx0 else "R" if x == fx1 else ""
            n = (v + h) or ("crack" if (x * 7 + y * 3) % 11 == 0 else "crack_b" if (x * 5 + y) % 13 == 0 else "C")
            m.piece("foundations", n, x, y)
    for x in range(fx0 + 2, fx1 - 1):
        m.piece("foundations", "step", x, fy1 + 1)
    m.put("old_columns", 4, 11)
    m.put("col_moss3", 7, 11)
    for (x, y, n) in ((9, 13, "drum"), (10, 13, "stub"), (9, 14, "drum"), (10, 14, "poppies"),
                      (5, 16, "poppies"), (6, 16, "drum")):
        m.piece("ruins", n, x, y)
    # Athena Promachos, facing the Propylaia
    m.put("promachos", 12, 15)

    # --- the processional ways ----------------------------------------------------------------
    props = set()

    def prop(x, y, h=1):
        props.update((x, y + j) for j in range(h))
    # the Sacred Way: from the Propylaia's court north past Promachos to the
    # Erechtheion's porch; east to the altar court below the Parthenon
    way = {(x, y) for x in range(11, 24) for y in range(24, 27)}            # the gate court
    way |= {(x, y) for x in range(18, 21) for y in range(10, 24)}           # north
    way |= {(x, y) for x in range(3, 14) for y in range(9, 11)}             # to the Erechtheion
    way |= {(x, y) for x in range(12, 18) for y in range(10, 12)}
    way |= {(x, y) for x in range(21, 31) for y in range(17, 20)}           # east
    way |= {(x, y) for x in range(28, 37) for y in range(12, 18)}           # the altar court
    way -= {(x, y) for x in range(31, 34) for y in range(14, 16)}           # the altar itself
    # braziers, lit, at the gate, by the altar, at the Erechtheion's porch and by the grove
    for (x, y) in ((17, 22), (21, 22), (30, 13), (34, 13), (3, 9), (13, 7), (41, 23), (33, 2), (24, 15),
                   (38, 12), (2, 21)):
        brazier_at(m, x, y)
        prop(x, y, 2)
    # votives lining the Sacred Way (row 21 stays clear: Kleon leaves along it),
    # a line of offerings before the north wall, more along the rims
    vot = [(17, 12), (17, 15), (17, 18), (21, 12), (21, 14), (27, 20),
           (14, 2), (17, 2), (20, 2), (27, 2), (30, 2), (36, 2), (39, 2), (41, 3),
           (2, 5), (2, 12), (2, 15), (41, 7), (41, 12), (26, 24), (32, 24)]
    for i, (x, y) in enumerate(vot):
        votive_at(m, "kore" if i % 2 else "kouros", x, y)
        prop(x, y, 2)
    # the bare rock breaking through where the plateau is highest
    for (x, y) in ((23, 2), (2, 18), (6, 22), (24, 22), (29, 21)):
        m.put("outcrop", x, y)
        props.update((x + i, y + j) for i in range(3) for j in range(2))
    # fallen drums lying where they fell, in heaps, not strewn
    for (x, y, n) in ((9, 20, "drum"), (10, 20, "stub"), (10, 21, "drum"), (4, 25, "drum"), (5, 25, "poppies"),
                      (41, 17, "stub"), (11, 25, "stub"), (2, 25, "drum"),
                      # votive bases left before the north wall and the Parthenon's steps
                      (29, 2, "stub"), (35, 2, "drum"), (40, 2, "stub"), (27, 12, "stub"), (37, 12, "drum"), (12, 26, "stub"), (8, 9, "drum")):
        m.piece("ruins", n, x, y)
        prop(x, y)
    # the grove's olives and its anemones
    for (x, y) in ((34, 19), (38, 20), (35, 23)):
        m.olive(x, y)
    for (x, y) in ((33, 24), (37, 24), (40, 18), (39, 23), (37, 18)):
        m.set(x, y, ANEMONE, False)
    pave_cells(m, {c for c in way - props if int(m.mid[c[1], c[0]]) not in (A.GRASS,)}, salt=11)
    # a few votive bases along the south rim walk, breaking its line
    for (x, y, n) in ((5, 26, "stub"), (27, 26, "drum"), (36, 26, "stub"), (37, 26, "poppies")):
        m.piece("ruins", n, x, y)

    # --- the Propylaia and the south cliff (rows 27-36) ---------------------------------------
    PX = PASSAGE - 6
    m.put("propylaia", PX, 27)
    for x in range(1, 43):
        if PX <= x < PX + 13:
            continue
        sfx = "_W" if x == 1 else "_E" if x == 42 else ""
        m.piece("cliff", ("lip" + sfx) if sfx else ("lip" if x % 2 else "lip_b"), x, 27)
        for y in range(28, 34):
            m.piece("cliff", ("face" + sfx) if sfx else ("face" if x % 2 else "face_b"), x, y)
    for x in range(1, 43):
        W, E = x == 1, x == 42
        sfx = "_W" if W else "_E" if E else ""
        if x in (PASSAGE - 1, PASSAGE, PASSAGE + 1):
            continue
        m.piece("cliff", ("lip" + sfx) if sfx else ("lip" if x % 2 else "lip_b"), x, 34)
        m.piece("cliff", ("face" + sfx) if sfx else ("face" if x % 2 else "face_b"), x, 35)
        m.piece("cliff", ("foot" + sfx) if sfx else ("foot" if x % 2 else "foot_b"), x, 36)
    row(m, "ramp", ["stair_top_L", "stair_top", "stair_top_R"], PASSAGE - 1, 34)
    row(m, "ramp", ["stair_L", "stair", "stair_R"], PASSAGE - 1, 35)
    row(m, "ramp", ["stair_L", "stair", "stair_R"], PASSAGE - 1, 36)
    m.set(PASSAGE - 1, 34, int(m.mid[34, PASSAGE - 1]), True)
    m.set(PASSAGE + 1, 34, int(m.mid[34, PASSAGE + 1]), True)

    # --- the switchback ramp (rows 37-53) -----------------------------------------------------
    ramp_props = set()

    def wall(y, x0, x1, stair, piers):
        """A retaining wall: coping and face, a stair cut through it, buttress
        piers (no run of plain wall over 6) with their feet on the terrace below."""
        for x in range(x0, x1 + 1):
            if stair[0] <= x <= stair[1]:
                n = "L" if x == stair[0] else "R" if x == stair[1] else ""
                m.piece("ramp", "stair_top" + ("_" + n if n else ""), x, y)
                m.piece("ramp", "stair" + ("_" + n if n else ""), x, y + 1)
                continue
            if x in piers:
                m.piece("ramp", "cap_pier", x, y)
                m.piece("ramp", "wall_pier", x, y + 1)
                m.piece("ramp", "foot_pier", x, y + 2)
                ramp_props.add((x, y + 2))
                continue
            n = "_L" if x == x0 else "_R" if x == x1 else ""
            m.piece("ramp", "cap" + n, x, y)
            m.piece("ramp", "wall" + n, x, y + 1)
    legs = {}
    for (y0, x0, x1) in ((37, 4, 38), (42, 4, 38), (47, 4, 37)):          # legs C, B, A
        m.rect(x0, y0, x1, y0 + 2, A.PATH, False)
        legs[y0] = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y0 + 3)}
    wall(40, 3, 39, (33, 35), (6, 12, 18, 24, 30))
    wall(45, 3, 39, (6, 8), (13, 19, 26, 31))
    m.rect(21, 50, 23, 53, A.PATH, False)
    m.set(*ENTRY, EXIT_MAT, False)
    # gardens where the legs run past their turns: cypress and olive in beds
    beds = {(x, y) for x in range(4, 15) for y in range(37, 40)}           # leg C, west of its stair
    beds |= {(x, y) for x in range(36, 39) for y in range(37, 40)}         # leg C, east
    beds |= {(x, y) for x in range(4, 6) for y in range(42, 44)}           # leg B, west
    beds |= {(x, y) for x in range(33, 38) for y in range(47, 50)}         # leg A, east
    for (x, y) in beds:
        m.set(x, y, A.GRASS, False)
    ramp = set().union(*legs.values())
    m.path({c for c in ramp if c not in beds and any((c[0] + dx, c[1] + dy) in beds
            for dx in (-1, 0, 1) for dy in (-1, 0, 1))}, context=ramp - beds)
    for x in (4, 6, 8, 10, 37):
        m.cypress(x, 38)
    for (x, y) in ((8, 37), (37, 37)):
        m.set(x, y, A.BOULDER_GRASS, True)
    m.olive(11, 38)
    m.cypress(4, 42)
    for x in (33, 35, 37):
        m.cypress(x, 48)
    # herms at the turns, braziers at the Propylaia stair's foot, votives on the belvedere
    m.set(14, 37, HERM, True)                     # in the garden bed
    ramp_props.add((14, 37))
    for i, (x, y) in enumerate(((32, 38), (9, 43), (5, 47))):
        votive_at(m, "kore" if i % 2 else "kouros", x, y)
        ramp_props.update({(x, y), (x, y + 1)})
    for (x, y) in ((17, 37), (21, 37)):
        brazier_at(m, x, y)
        ramp_props.update({(x, y), (x, y + 1)})
    votive_at(m, "kore", 28, 47)
    votive_at(m, "kouros", 23, 47)
    ramp_props.update({(28, 47), (28, 48), (23, 47), (23, 48)})
    # votive bases along each leg's outer edge, so no run of wall foot passes 6 bare cells
    for (x, y, n) in ((25, 39, "stub"), (16, 39, "drum"), (20, 39, "stub"), (26, 37, "stub"),
                      (31, 37, "drum"), (7, 49, "drum"), (15, 44, "drum"), (21, 44, "stub"), (27, 44, "drum"), (35, 44, "stub"),
                      (16, 49, "stub"), (25, 49, "drum"), (31, 49, "stub")):
        m.piece("ruins", n, x, y)
        ramp_props.add((x, y))
    ramp_pave = {c for c in ramp - beds - ramp_props if int(m.mid[c[1], c[0]]) == A.PATH}
    ramp_pave -= {(4, 47), (4, 48), (4, 49), (5, 48), (5, 49)}              # the worn west end, where the revive hides
    pave_cells(m, ramp_pave, salt=5)
    # the view edge: a parapet along leg A's south side over the planted slope below
    slope = {(x, y) for x in range(5, 21) for y in range(50, 54)} | {(x, y) for x in range(24, 37) for y in range(50, 54)}
    for (x, y) in slope:
        m.set(x, y, A.GRASS, False)
    for x0, x1 in ((5, 20), (24, 36)):
        for x in range(x0, x1 + 1):
            m.set(x, 50, A.WALL["L"] if x == x0 else A.WALL["R"] if x == x1 else A.WALL["M"], True)
    for (x, y) in ((6, 51), (10, 52), (15, 51), (26, 52), (30, 51), (34, 52)):
        m.olive(x, y)
    for x in (13, 19, 24, 29, 36):
        m.cypress(x, 51 if x % 2 else 52)

    # --- events ---------------------------------------------------------------------------------
    m.warp(ENTRY[0], ENTRY[1], "MAP_ASTYRA", 4)
    m.warp(WELL[0], WELL[1], "MAP_SALT_WELL_B1F", 0)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_CAPTAIN", 22, 50)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_ALETHEA", 21, 52)
    # Pair one at the first stair, west end of leg A; pair two at the second, east end of leg B
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_LITHOS", 9, 47, movement_type="MOVEMENT_TYPE_FACE_RIGHT")
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_KONIORTOS", 9, 49, movement_type="MOVEMENT_TYPE_FACE_RIGHT")
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_SIDEROS", 32, 42, movement_type="MOVEMENT_TYPE_FACE_LEFT")
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_CHALKOS", 32, 44, movement_type="MOVEMENT_TYPE_FACE_LEFT")
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_KLEON", PASSAGE, 23)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_RHEA", 17, 9)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_DIGGERWEST", 15, 8)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_DIGGEREAST", 18, 7)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_CARETAKER", 22, 8)
    keep_obj(m, src, "LOCALID_ASTYRA_AKROPOLIS_HEALINGJAR", 38, 43)
    for y in (47, 48, 49):
        m.trigger(12, y, "Astyra_Akropolis_EventScript_PairOne", var="VAR_TEMP_1")
    for y in (42, 43, 44):
        m.trigger(29, y, "Astyra_Akropolis_EventScript_PairTwo", var="VAR_TEMP_1")
    m.trigger(PASSAGE, 27, "Astyra_Akropolis_EventScript_Kleon", var="VAR_TEMP_1")
    m.trigger(PASSAGE, 26, "Astyra_Akropolis_EventScript_Reveal", var="VAR_TEMP_1")
    for x in list(range(2, 26)) + [40, 41]:
        if not m.solid[11, x]:
            m.trigger(x, 11, "Astyra_Akropolis_EventScript_Rhea", var="VAR_TEMP_1")
    for b in src["bg_events"]:
        e = dict(b)
        sc = b.get("script")
        if sc in ("Astyra_Akropolis_EventScript_Promachos", "Astyra_Akropolis_EventScript_Altar"):
            continue
        if b.get("flag") == "FLAG_ICHOR_HIDDEN_AKROPOLIS_REVIVE":
            e["x"], e["y"] = 4, 48
        elif b.get("flag") == "FLAG_ICHOR_HIDDEN_AKROPOLIS_ETHER":
            e["x"], e["y"] = 14, 5
        elif sc == "Astyra_Akropolis_EventScript_Olive":
            e["x"], e["y"] = 16, 8
        elif sc == "Astyra_Akropolis_EventScript_SpringStair":
            e["x"], e["y"] = CLEFT
        elif sc == "Astyra_Akropolis_EventScript_Trident":
            e["x"], e["y"] = TRIDENT
        m.bgs.append(e)
    m.sign(14, 22, "Astyra_Akropolis_EventScript_Promachos")
    m.sign(32, 15, "Astyra_Akropolis_EventScript_Altar")
    for t in m.coords:
        t["elevation"] = 0
    views = [ENTRY, (10, 46), (30, 41), (19, 37), (19, 30), (19, 24), (14, 18), (32, 14), (18, 8), (7, 14)]
    starts = [(ENTRY[0], ENTRY[1] - 1)]
    must = [(16, 9, "the olive"), (OLIVE[0] + 6, 8, "the caretaker"), (38, 42, "the jar's nook")]
    blockers = []
    return m.build("akropolis", starts, must_reach=must, views=views, blockers=blockers, render=render)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("maps", nargs="*", default=["city", "harbor", "akropolis"])
    a = ap.parse_args()
    bad = 0
    for name in a.maps:
        bad += len({"city": city, "harbor": harbor, "akropolis": akropolis}[name](not a.no_render))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
