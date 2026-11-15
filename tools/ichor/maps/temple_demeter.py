#!/usr/bin/env python3
"""The Temple of Demeter (the Telesterion): layout, events, scripts, checks and renders.

The hall is the Lesser Mysteries of design/phase2/SCRIPT.md Part 5, drawn with
gTileset_TempleDemeter (design/phase2/TILES_temple_demeter.md) on the oikos
primary: one great square hall in the dark, a forest of columns, rock-cut tiers
along the north wall with the Mystagogue's dais and Demeter's great altar, the
Anaktoron in the middle with Chloe's throne by its door, and a season brazier in
each corner. The rite follows Persephone's trail:

  teach   Autumn, front left: near the stair; Kallidike teaches at the brazier
  test    Winter, back left: across the column forest; Eumolpos on the straight line
          Spring, back right: below the tiers; Melissa on the tiers, facing the wall
  master  Summer, front right: the quarter is floored with grain pits, and Hecate's
          chalk marks the one safe way through (the chalk shows only doused)

Each brazier's flag is FLAG_ICHOR_BRAZIERS_START + 0x10..0x13 (BUILD.md); each
lights its quarter for good (a lit zone, ENGINE_API.md §2) and its column torch.

Beat 22, the night of the Mysteries, plays here too: its cast (Kerykos, Alethea, Kleon,
initiates, two Titanborn) stands where the table below puts them, hidden but for the
scene; the raid kicks over the front braziers (`overturned`) and leaves bootprints,
drawn on every load after FLAG_ICHOR_MYSTERIES_NIGHT.

Writes:
  data/layouts/EleusaVillage_TempleOfDemeter/map.bin, border.bin
  data/maps/EleusaVillage_TempleOfDemeter/map.json (events from the tables below)
  the generated block of its scripts.pory: the brazier lights, the room's drawing
  from its state, and the lit-zone and pit triggers' scripts
Checks: people on open floor; the walls, braziers and altar readable; every open
cell reachable from the stair; the Summer brazier reachable only along the chalk
path; the other three without touching a pit; every setmetatile on its own piece.
Renders, into --render DIR (the 2x maps for design/phase2/img/):
  temple_demeter.png (2x, cold, with people), temple_demeter_map_lit.png (all four lit),
  temple_demeter_map_dark.png (as the torch shows it), temple_demeter_map_events.png

Usage: /usr/bin/python3 tools/ichor/maps/temple_demeter.py [--render DIR]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))

CAT = ROOT / "build/temple_demeter/catalog.json"
NAME = "EleusaVillage_TempleOfDemeter"
LAYOUT_ID = "LAYOUT_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER"
MAP_DIR = ROOT / "data/maps" / NAME
LAYOUT_DIR = ROOT / "data/layouts" / NAME
PX = "EleusaVillage_TempleOfDemeter_EventScript_"
W, H = 27, 27
VILLAGE_DOOR_WARP = 8          # the Telesterion's door in EleusaVillage's warp list (eleusa.py)

# --- The catalog: "struct.name" -> (id, walk) -------------------------------------------
def catalog():
    cat = json.loads(CAT.read_text())
    ids, walk = {}, {}
    for s in cat["structures"]:
        names = {tuple(v): k for k, v in s.get("names", {}).items()}
        for j in range(s["h"]):
            for i in range(s["w"]):
                n = names.get((i, j), f"r{j}c{i}")
                ids[f"{s['key']}.{n}"] = s["ids"][j][i]
                walk[f"{s['key']}.{n}"] = s["walk"][j][i]
    return ids, walk


IDS, WALK = catalog()

# --- The plan -----------------------------------------------------------------------------
SEASONS = ["autumn", "winter", "spring", "summer"]          # the order of the trail
BRAZIER = {"autumn": (2, 21), "winter": (2, 6), "spring": (24, 6), "summer": (24, 21)}  # the bowl; legs below
PLAQUE = {"autumn": "a falling leaf", "winter": "a bare branch", "spring": "a sprout", "summer": "a sheaf"}
FLAG_INDEX = {s: 0x10 + i for i, s in enumerate(SEASONS)}  # FLAG_ICHOR_BRAZIERS_START + n
# each quarter's column torch: the column's top cell
COLUMN_TORCH = {"autumn": (7, 18), "winter": (7, 9), "spring": (19, 9), "summer": (19, 18)}
# the back quarters' wall sconces, lit with their brazier
SCONCES = {"winter": (4, 10), "spring": (16, 22), "autumn": (), "summer": ()}
ZONES = {"winter": (1, 6, 10, 14), "autumn": (1, 16, 10, 25),
         "spring": (16, 6, 25, 14), "summer": (16, 16, 25, 25)}     # x0, y0, x1, y1
COLUMN_X = (4, 7, 10, 16, 19, 22)
COLUMN_Y = (6, 9, 12, 15, 18, 21)
NO_COLUMN = {(10, 12), (16, 12)}          # beside the Anaktoron's walls
ANAKTORON = (11, 11)                      # 5x3, door at +2,+2
DOOR = (13, 13)
CHLOE = (13, 14)                          # in the Anaktoron's doorway
THRONE = (15, 14)                         # 1x2, beside the door
DAIS = (12, 6)                            # 4x2: the altar at +3,0, the steps at +2,+1
ALTAR = (15, 6)
STAIRS = [(12, 26), (13, 26), (14, 26)]
ARRIVAL = (13, 26)

# The Summer quarter's grain pits. S is the safe way (Hecate's chalk), P a pit;
# anything else is left as it is (C a column, B the brazier, e the last seed).
PIT_ORIGIN = (16, 17)
PITS = [
    # x 16..25
    "SSSPPPPPPP",   # y 17
    "CPSCPPCPPP",   # y 18
    "CPSCPPCPPP",   # y 19
    "PPSSSPPPPP",   # y 20
    "CPPCSPCPBP",   # y 21
    "CPPCSSCPBP",   # y 22
    "PPPPPSSSeP",   # y 23
    "PPPPPPPPPP",   # y 24 (the front row, y 25, is a walk along the wall)
]
FALL_TO = (23, 4)                          # the tiers by the Spring brazier


def pit_cells():
    pits, safe = set(), []
    ox, oy = PIT_ORIGIN
    for j, row in enumerate(PITS):
        for i, c in enumerate(row):
            if c == "P":
                pits.add((ox + i, oy + j))
            elif c in "Se":
                safe.append((ox + i, oy + j))
    return pits, safe


def seed_cell(season):
    x, y = BRAZIER[season]
    return x, y + 2


FRIEZE = ["key", "maiden", "wheat", "horses", "wheat", "seized", "key", "search", "wheat",
          "hecate", "key", "grief", "wheat", "key", "wheat", "grief", "key", "hermes", "wheat",
          "return", "key", "wheat", "maiden", "wheat", "key"]


def noise(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 100


def names_grid():
    g = [["floor.floor"] * W for _ in range(H)]
    for x in range(W):
        g[0][x] = "wall.top"
        g[H - 1][x] = "floor.void"
    g[0][0], g[0][W - 1] = "wall.corner_l", "wall.corner_r"
    for y in range(1, H - 1):
        g[y][0], g[y][W - 1] = "wall.side_l", "wall.side_r"
    for x in range(1, W - 1):
        g[1][x] = "frieze." + FRIEZE[x - 1]
        g[2][x] = "wall.lower"
    for x in (4, 10, 16, 22):
        g[2][x] = "wall_lights.sconce_cold"
    for x in (7, 19):
        g[2][x] = "wall_lights.niche_cold"
    g[2][13] = "wall.lower_chalk"            # Hecate's mark over the Anaktoron (shows doused)
    for j, row in enumerate(("top", "mid", "low")):
        for x in range(1, W - 1):
            g[3 + j][x] = f"tiers.{row}_" + ("L" if x == 1 else "R" if x == W - 2 else "M")
    # the floor, its flags varied
    for y in range(6, H - 1):
        for x in range(1, W - 1):
            n = noise(x, y, 1)
            g[y][x] = "floor.floor_b" if n < 14 else "floor.floor_c" if n < 22 else \
                      "floor.floor_cracked" if n < 25 else "floor.floor"
    # the dais and Demeter's great altar, before the tiers
    dx, dy = DAIS
    for i, n in enumerate(("L", "M", "R", "altar_empty")):
        g[dy][dx + i] = "dais." + n
    for i, n in enumerate(("riser_L", "riser_M", "steps", "riser_R")):
        g[dy + 1][dx + i] = "dais." + n
    # the forest of columns
    for cy in COLUMN_Y:
        for cx in COLUMN_X:
            if (cx, cy) in NO_COLUMN:
                continue
            g[cy][cx], g[cy + 1][cx] = "columns.top", "columns.bottom" if noise(cx, cy, 2) < 60 else "columns.bottom_b"
    for s, (cx, cy) in COLUMN_TORCH.items():
        g[cy][cx] = "columns.torch_cold"
        g[cy + 1][cx] = "columns.bottom"
    # the Anaktoron, the throne and the holy things
    ax, ay = ANAKTORON
    for j in range(3):
        for i in range(5):
            g[ay + j][ax + i] = f"anaktoron.r{j}c{i}"
    tx, ty = THRONE
    g[ty][tx], g[ty + 1][tx] = "throne.r0c0", "throne.r1c0"
    g[14][11] = "vessels.kistai"
    g[CHLOE[1]][CHLOE[0]] = "floor.floor_inlay"   # the Anaktoron's gilt threshold, where Chloe stands
    g[6][9] = "vessels.liknon"
    g[6][17] = "vessels.kykeon"
    g[6][18] = "vessels.kernos"
    # the season braziers, cold
    for s, (bx, by) in BRAZIER.items():
        g[by][bx], g[by + 1][bx] = "braziers.top_cold", f"braziers.{s}_cold"
    # the acolytes' lamps
    for (x, y) in ((6, 24), (9, 9)):
        g[y][x] = "vessels.lamp_lit"
    # the Summer quarter: pits (black, walkable, each a trigger) and the chalk path
    pits, safe = pit_cells()
    for (x, y) in pits:
        g[y][x] = "floor.void"
    for k, (x, y) in enumerate(safe):
        if (x, y) == seed_cell("summer"):
            continue
        prev = safe[k - 1] if k else (x - 1, y)
        nxt = safe[k + 1] if k + 1 < len(safe) else (x + 1, y)
        horiz = prev[1] == y and nxt[1] == y
        vert = prev[0] == x and nxt[0] == x
        g[y][x] = "floor.chalk_trail_h" if horiz else "floor.chalk_trail_v" if vert else "floor.chalk_fork"
    # the seeds' cells are plain floor: the room's drawing puts the next seed down
    for s in SEASONS:
        x, y = seed_cell(s)
        g[y][x] = "floor.floor"
    # the stair up to the daylight
    for (x, y), n in zip(STAIRS, ("up_L", "up_M", "up_R")):
        g[y][x] = "stairs." + n
    return g


def walkable_name(n):
    return WALK.get(n, "X") != "X"


def solid_grid(g):
    pits, _ = pit_cells()
    s = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            s[y, x] = not walkable_name(g[y][x]) and (x, y) not in pits
    # the Anaktoron's door stays shut until beat 22; its warp is wired, the cell blocks
    # (ON_LOAD clears it once FLAG_ICHOR_SANCTUM_OPEN is set)
    s[DOOR[1], DOOR[0]] = True
    return s


# --- Lighting -----------------------------------------------------------------------------
RING = {(-1, 0): "glow.l0", (1, 0): "glow.r0", (-1, 1): "glow.l1", (1, 1): "glow.r1",
        (-1, 2): "glow.bl", (0, 2): "glow.b", (1, 2): "glow.br"}
PLAIN = ("floor.floor", "floor.floor_b", "floor.floor_c", "floor.floor_cracked")


def light_cells(g, season):
    """(x, y, name) for the brazier, its glow, its column torch and that column's glow."""
    bx, by = BRAZIER[season]
    out = [(bx, by, "braziers.top_lit"), (bx, by + 1, f"braziers.{season}_lit")]
    for (ox, oy) in (BRAZIER[season], COLUMN_TORCH[season]):
        for (dx, dy), n in RING.items():
            x, y = ox + dx, oy + dy
            if 0 <= x < W and 0 <= y < H and g[y][x] in PLAIN:
                out.append((x, y, n))
    cx, cy = COLUMN_TORCH[season]
    out += [(cx, cy, "columns.torch_lit"), (cx, cy + 1, "columns.bottom_lit")]
    out += [(x, 2, "wall_lights.sconce_lit") for x in SCONCES[season]]
    return out


LABEL = {"braziers.top_lit": "BrazierTop_Lit", "columns.torch_lit": "ColumnTorch_Lit",
         "columns.bottom_lit": "ColumnBottom_Lit", "floor.floor": "Floor", "floor.seed": "Floor_Seed",
         "glow.l0": "Glow_L0", "glow.r0": "Glow_R0", "glow.l1": "Glow_L1", "glow.r1": "Glow_R1",
         "glow.bl": "Glow_BL", "glow.b": "Glow_B", "glow.br": "Glow_BR",
         "wall_lights.sconce_lit": "Sconce_Lit"}
for _s in SEASONS:
    LABEL[f"braziers.{_s}_lit"] = f"Brazier{_s.title()}_Lit"


def lit_grid(g, seasons):
    out = [row[:] for row in g]
    for s in seasons:
        for x, y, n in light_cells(g, s):
            out[y][x] = n
    return out


# The raid (beat 22): a kicked brazier lies on its side across its legs' cell and the
# one east of it (`overturned`, 2x1), the bowl's cell is bare floor, and its glow and
# its column torch go cold, so its quarter is dark again.
RAID_TRACKS = [(13, 15), (13, 16)]        # bootprints out of the Anaktoron's door


def kick_cells(g, season):
    """(x, y, metatile id, solid) for a brazier kicked over."""
    bx, by = BRAZIER[season]
    out = [(bx, by, IDS["floor.floor"], False),
           (bx, by + 1, IDS["overturned.r0c0"], True),
           (bx + 1, by + 1, IDS["overturned.r0c1"], True)]
    taken = {(x, y) for x, y, _, _ in out}
    for x, y, n in light_cells(g, season):
        if (x, y) in taken:
            continue
        base = g[y][x]
        out.append((x, y, IDS[base], not walkable_name(base)))
    return out


# --- Events -------------------------------------------------------------------------------
GFX = "OBJ_EVENT_GFX_ICHOR_"
CROWD = "FLAG_ICHOR_HIDE_MYSTERIES_CROWD"        # beat 22's congregation, there only for the scene
GRUNTS = "FLAG_ICHOR_HIDE_TELESTERION_GRUNTS"    # the two who climb out of the Anaktoron
SCENE_FLAGS = {CROWD, GRUNTS, "FLAG_ICHOR_HIDE_KLEON_TELESTERION"}
OBJECTS = [
    # local id, gfx, x, y, facing, script, hide flag[, trainer sight]
    ("DOSO", GFX + "ELDER_F", 11, 25, "RIGHT", "Doso", "0"),
    # the acolytes (SCRIPT.md Part 3). Kallidike's sight covers the Autumn seed; Eumolpos
    # faces the straight line (y 8) to the Winter brazier; Melissa faces the wall, so she
    # only battles when spoken to.
    ("KALLIDIKE", GFX + "ACOLYTE_F", 5, 23, "LEFT", "Kallidike", "0", 3),
    ("EUMOLPOS", GFX + "ACOLYTE_M", 8, 9, "UP", "Eumolpos", "0", 1),
    ("MELISSA", GFX + "ACOLYTE_F", 23, 3, "UP", "Melissa", "0", 1),
    ("CHLOE", GFX + "PRIESTESS", CHLOE[0], CHLOE[1], "DOWN", "Chloe", "FLAG_ICHOR_HIDE_CHLOE_TELESTERION"),
    # beat 22, the night of the Mysteries: the player stands at the front (13, 17), Alethea
    # beside them, Kleon two places along; Kerykos by the holy baskets; initiates behind.
    # The grunts climb out of the Anaktoron's door. After the scene Kleon keeps the door
    # (ON_TRANSITION moves him to KLEON_DOOR) until beat 24. ICHOR_STUB_SPRITE: initiates
    # are drawn as pilgrims and youths.
    ("KERYKOS", GFX + "KERYKOS", 11, 15, "DOWN", "Hush", CROWD),
    ("ALETHEA", GFX + "ALETHEA", 12, 17, "UP", "Hush", CROWD),
    ("KLEON", GFX + "KLEON", 15, 17, "UP", "Kleon", "FLAG_ICHOR_HIDE_KLEON_TELESTERION"),
    ("PSAMMIS", GFX + "TITAN_GRUNT", DOOR[0], DOOR[1], "DOWN", "Hush", GRUNTS),
    ("CHERSOS", GFX + "TITAN_GRUNT", DOOR[0], DOOR[1], "DOWN", "Hush", GRUNTS),
    ("INITIATE_1", GFX + "PILGRIM", 11, 17, "UP", "Hush", CROWD),
    ("INITIATE_2", GFX + "YOUTH_F", 12, 18, "UP", "Hush", CROWD),
    ("INITIATE_3", GFX + "YOUTH_M", 14, 18, "UP", "Hush", CROWD),
    ("INITIATE_4", GFX + "PILGRIM", 15, 18, "UP", "Hush", CROWD),
]
MYSTERIES_SPOT = (13, 17)                 # where Kerykos's YES lands the player (eleusa scripts)
KLEON_DOOR = (14, 14)                     # Kleon's post at the Anaktoron's door after beat 22
KICKED = ("autumn", "summer")             # the braziers the grunts kick over (the front two)


def bg_events():
    out = []
    for s, (bx, by) in BRAZIER.items():
        name = "Brazier" + s.title()
        out += [(bx, by, "ANY", name), (bx, by + 1, "ANY", name)]
    out.append((ALTAR[0], ALTAR[1], "ANY", "GreatAltar"))           # ICHOR_STUB_RITES
    out.append((THRONE[0], THRONE[1], "ANY", "Throne"))
    out.append((THRONE[0], THRONE[1] + 1, "ANY", "Throne"))
    return out


def zone_of(x, y):
    for s, (x0, y0, x1, y1) in ZONES.items():
        if x0 <= x <= x1 and y0 <= y <= y1:
            return s
    return None


PIT_VAR = "VAR_TEMP_C"        # 1 once the pits are boarded over (the Harvest Laurel)
ZONE_VAR = "VAR_TEMP_B"       # 1 while the player stands in a lit quarter
# (Not VAR_TEMP_2 and _3: the engine keeps a carried flame's steps and kind there.)


def coord_events(solid):
    """Pit triggers on every pit, then the lit zones' rings: entering on the zone's
    edge cells, leaving on the dark cells just outside it."""
    pits, _ = pit_cells()
    out = [(x, y, PIT_VAR, "0", "Pit") for (x, y) in sorted(pits, key=lambda p: (p[1], p[0]))]
    taken = set(pits)

    def open_(x, y):
        return 0 <= x < W and 0 <= y < H and not solid[y, x]
    enter, leave = [], set()
    for y in range(H):
        for x in range(W):
            z = zone_of(x, y)
            if not z or not open_(x, y) or (x, y) in taken:
                continue
            outside = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                       if open_(x + dx, y + dy) and zone_of(x + dx, y + dy) != z]
            if outside:
                enter.append((x, y, z))
                for p in outside:
                    if zone_of(*p) is None and p not in taken:
                        leave.add(p)
    for (x, y, z) in enter:
        out.append((x, y, ZONE_VAR, "0", "Enter" + z.title()))
    for (x, y) in sorted(leave, key=lambda p: (p[1], p[0])):
        out.append((x, y, ZONE_VAR, "1", "LeaveLitZone"))
    return out


def write_events(solid):
    m = json.loads((MAP_DIR / "map.json").read_text())
    m["music"] = "MUS_ICHOR_TEMPLE_DEMETER"
    m["requires_flash"] = True                 # a dark map (ENGINE_API.md §2)
    m["map_type"] = "MAP_TYPE_INDOOR"
    m["object_events"] = [{
        "local_id": f"LOCALID_TEMPLE_DEMETER_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": f"MOVEMENT_TYPE_FACE_{f}", "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": str(sight[0]) if sight else "0",
        "script": PX + s, "flag": flag} for lid, gfx, x, y, f, s, flag, *sight in OBJECTS]
    warps = [{"x": x, "y": y, "elevation": 0, "dest_map": "MAP_ELEUSA_VILLAGE",
              "dest_warp_id": str(VILLAGE_DOOR_WARP)} for x, y in STAIRS]
    warps.append({"x": DOOR[0], "y": DOOR[1], "elevation": 0, "dest_map": "MAP_ELEUSA_SANCTUM_B1F",
                  "dest_warp_id": "0"})
    # warp 0 must be the middle step: the village's door arrives there
    warps[0], warps[1] = warps[1], warps[0]
    m["warp_events"] = warps
    m["coord_events"] = [{"type": "trigger", "x": x, "y": y, "elevation": 0, "var": v, "var_value": val,
                          "script": PX + s} for x, y, v, val, s in coord_events(solid)]
    m["bg_events"] = [{"type": "sign", "x": x, "y": y, "elevation": 0,
                       "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": PX + s}
                      for x, y, f, s in bg_events()]
    (MAP_DIR / "map.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    return m


# --- The generated scripts ----------------------------------------------------------------
SCRIPT_BEGIN = "// --- Generated by tools/ichor/maps/temple_demeter.py from the room. Do not edit. ---"
SCRIPT_END = "// --- End of the generated block. ---"


def script_block(g):
    pits, _ = pit_cells()
    o = [SCRIPT_BEGIN, ""]
    o.append("// Draws the hall from the rite's state: the lit braziers and their quarters,")
    o.append("// the one seed that glows (the next brazier's), the pits once boarded over,")
    o.append("// and the Anaktoron's door, shut until the sanctum opens.")
    o.append(f"script {PX}DrawHall {{")
    for s in SEASONS:
        o.append(f"    if (flag(FLAG_ICHOR_BRAZIERS_START + 0x{FLAG_INDEX[s]:02X})) {{")
        o.append(f"        call({PX}Light{s.title()})")
        o.append("    }")
    o.append(f"    call({PX}DrawSeed)")
    o.append("    if (flag(FLAG_BADGE03_GET)) {")
    o.append(f"        call({PX}BoardPits)")
    o.append("    }")
    o.append("    if (flag(FLAG_ICHOR_MYSTERIES_NIGHT)) {")
    o.append(f"        call({PX}DrawRaid)")
    o.append("    }")
    o.append("    if (!flag(FLAG_ICHOR_SANCTUM_OPEN)) {")
    o.append(f"        setmetatile({DOOR[0]}, {DOOR[1]}, 0x{IDS['anaktoron.r2c2']:03X}, TRUE)")
    o.append("    } else {")
    o.append(f"        setmetatile({DOOR[0]}, {DOOR[1]}, 0x{IDS['anaktoron.r2c2']:03X}, FALSE)")
    o.append("    }")
    o.append("    return")
    o.append("}")
    o.append("")
    o.append("// Only the next seed on the trail is set down (latent: it shows when doused).")
    o.append(f"script {PX}DrawSeed {{")
    for k, s in enumerate(SEASONS):
        x, y = seed_cell(s)
        kw = "if" if k == 0 else "elif"
        o.append(f"    {kw} (!flag(FLAG_ICHOR_BRAZIERS_START + 0x{FLAG_INDEX[s]:02X})) {{")
        o.append(f"        setmetatile({x}, {y}, METATILE_TempleDemeter_Floor_Seed, FALSE)")
        o.append("    }")
    o.append("    return")
    o.append("}")
    for s in SEASONS:
        o.append("")
        o.append(f"script {PX}Light{s.title()} {{")
        for x, y, n in light_cells(g, s):
            o.append(f"    setmetatile({x}, {y}, METATILE_TempleDemeter_{LABEL[n]}, {'FALSE' if n.startswith('glow') else 'TRUE'})")
        o.append("    return")
        o.append("}")
    o.append("")
    o.append("// After the Harvest Laurel the pits are boarded over: plain floor.")
    o.append(f"script {PX}BoardPits {{")
    for (x, y) in sorted(pits, key=lambda p: (p[1], p[0])):
        o.append(f"    setmetatile({x}, {y}, METATILE_TempleDemeter_Floor, FALSE)")
    o.append("    return")
    o.append("}")
    o.append("")
    o.append("// The night of the Mysteries (beat 22): the grunts kick over the front braziers,")
    o.append("// and leave bootprints out of the Anaktoron's door.")
    o.append(f"script {PX}DrawRaid {{")
    for s in KICKED:
        o.append(f"    call({PX}Kick{s.title()})")
    for (x, y) in RAID_TRACKS:
        o.append(f"    setmetatile({x}, {y}, 0x{IDS['floor.bootprints']:03X}, FALSE)")
    o.append("    return")
    o.append("}")
    for s in KICKED:
        o.append("")
        o.append(f"script {PX}Kick{s.title()} {{")
        for x, y, mid, solid in kick_cells(g, s):
            o.append(f"    setmetatile({x}, {y}, 0x{mid:03X}, {'TRUE' if solid else 'FALSE'})")
        o.append("    return")
        o.append("}")
    o.append("")
    o.append(SCRIPT_END)
    return "\n".join(o)


def splice_script(g):
    path = MAP_DIR / "scripts.pory"
    text = path.read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"temple_demeter: {path} needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    new = text[:a] + script_block(g) + text[b + len(SCRIPT_END):]
    if new != text:
        path.write_text(new)


# --- Output -------------------------------------------------------------------------------
def blockdata(g, solid):
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            out[y, x] = IDS[g[y][x]] | (int(solid[y, x]) << 10) | (3 << 12)
    return out


def write_layout(g, solid):
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    blockdata(g, solid).astype("<u2").tofile(LAYOUT_DIR / "map.bin")
    np.full(4, IDS["floor.void"], np.uint16).astype("<u2").tofile(LAYOUT_DIR / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    for l in data["layouts"]:
        if l.get("id") == LAYOUT_ID and (l["width"], l["height"]) != (W, H):
            l["width"], l["height"] = W, H
            l["primary_tileset"], l["secondary_tileset"] = "gTileset_Oikos", "gTileset_TempleDemeter"
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# --- Checks -------------------------------------------------------------------------------
def reach(solid, start, blocked=frozenset()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < W and 0 <= p[1] < H and p not in seen and not solid[p[1], p[0]] and p not in blocked:
                seen.add(p)
                q.append(p)
    return seen


def labels():
    text = (ROOT / "include/constants/metatile_labels.h").read_text()
    return {k: int(v, 16) for k, v in re.findall(r"#define (METATILE_TempleDemeter_\w+)\s+(0x[0-9A-Fa-f]+)", text)}


def check(g, solid, m):
    errors = []
    pits, safe = pit_cells()
    # beat 22's cast is only in the hall for its scene, so the rite's walks ignore them
    people = {(o["x"], o["y"]) for o in m["object_events"] if o["flag"] not in SCENE_FLAGS}
    every = reach(solid, ARRIVAL)
    open_cells = {(x, y) for y in range(H) for x in range(W) if not solid[y, x]}
    stranded = sorted(open_cells - every)
    if stranded:
        errors.append(f"open but unreachable from the stair: {stranded[:10]}")
    for o in m["object_events"]:
        if o["flag"] == GRUNTS:
            if (o["x"], o["y"]) != DOOR:
                errors.append(f"{o['local_id']} should climb out of the Anaktoron's door {DOOR}")
            continue
        if solid[o["y"], o["x"]] or (o["x"], o["y"]) in pits:
            errors.append(f"{o['local_id']} stands on {g[o['y']][o['x']]}")
    # beat 22: the scene's spot, and Kleon's post beside the door (not in front of it)
    for what, (x, y) in (("the Mysteries' spot", MYSTERIES_SPOT), ("Kleon's post", KLEON_DOOR)):
        if solid[y, x] or (x, y) in pits or (x, y) not in every:
            errors.append(f"{what} {(x, y)} isn't open floor")
    if KLEON_DOOR == CHLOE or reach(solid, ARRIVAL, frozenset({KLEON_DOOR})).isdisjoint({CHLOE}):
        errors.append("Kleon's post blocks the way to the Anaktoron's door")
    for s in KICKED:
        for x, y, mid, _ in kick_cells(g, s)[:3]:
            if (x, y) in (DOOR, CHLOE, MYSTERIES_SPOT) or g[y][x].startswith(("columns", "anaktoron")):
                errors.append(f"the kicked {s} brazier lands on {g[y][x]} at ({x},{y})")
    no_pits = reach(solid, ARRIVAL, frozenset(pits) | people)
    for s in ("autumn", "winter", "spring"):
        x, y = BRAZIER[s]
        if not any(p in no_pits for p in ((x - 1, y), (x + 1, y), (x - 1, y + 1), (x + 1, y + 1), (x, y + 2))):
            errors.append(f"the {s} brazier can't be reached without crossing a pit")
    # Summer: only along the chalk
    x, y = BRAZIER["summer"]
    fronts = [(x - 1, y), (x + 1, y), (x - 1, y + 1), (x + 1, y + 1), (x, y + 2)]
    off_path = frozenset(open_cells - set(safe)) & frozenset((a, b) for (a, b) in open_cells if a >= PIT_ORIGIN[0] and b >= PIT_ORIGIN[1])
    if any(p in no_pits for p in fronts) is False:
        errors.append("the Summer brazier can't be reached along the chalk")
    via_chalk_only = reach(solid, ARRIVAL, off_path | people)
    if not any(p in via_chalk_only for p in fronts):
        errors.append("the chalk path doesn't reach the Summer brazier")
    for b in m["bg_events"]:
        bx, by = b["x"], b["y"]
        if not any((bx + dx, by + dy) in every for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            errors.append(f"bg event ({bx},{by}) can't be faced")
    for w in m["warp_events"]:
        n = g[w["y"]][w["x"]]
        if not (n.startswith("stairs.") or n == "anaktoron.r2c2"):
            errors.append(f"warp ({w['x']},{w['y']}) is on {n}")
    for c in m["coord_events"]:
        if solid[c["y"], c["x"]]:
            errors.append(f"trigger ({c['x']},{c['y']}) is on a solid cell")
    if len({(c["x"], c["y"]) for c in m["coord_events"]}) != len(m["coord_events"]):
        errors.append("two triggers share a cell")
    # every setmetatile lands on the piece it swaps
    lab = labels()
    names = {v: k for k, v in IDS.items()}
    allowed = {}
    for s in SEASONS:
        for x, y, n in light_cells(g, s):
            allowed.setdefault((x, y), set()).add(IDS[n])
    for s in SEASONS:
        allowed.setdefault(seed_cell(s), set()).add(IDS["floor.seed"])
    for (x, y) in pits:
        allowed.setdefault((x, y), set()).add(IDS["floor.floor"])
    script = (MAP_DIR / "scripts.pory").read_text()
    for x, y, label in re.findall(r"setmetatile\((\d+),\s*(\d+),\s*(METATILE_\w+)", script):
        x, y = int(x), int(y)
        if lab.get(label) not in allowed.get((x, y), set()):
            errors.append(f"setmetatile({x}, {y}, {label}) puts {names.get(lab.get(label))} over {g[y][x]}")
    return errors


# --- Renders ------------------------------------------------------------------------------
def renderer():
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R, R.Renderer(R.Tileset(R.resolve_tileset("oikos", syms)),
                         R.Tileset(R.resolve_tileset("gTileset_TempleDemeter", syms)))


def people(im, scale):
    from PIL import Image
    for lid, gfx, x, y, facing, script, flag, *_ in OBJECTS:
        if flag != "0":
            continue
        sheet = Image.open(ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png")
        frame = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}[facing]
        crop = sheet.crop((frame * 16, 0, frame * 16 + 16, 32))
        spr = crop.convert("RGBA")
        if sheet.mode == "P":
            idx, px = crop.load(), spr.load()
            for j in range(32):
                for i in range(16):
                    if idx[i, j] == 0:
                        px[i, j] = (0, 0, 0, 0)
        if facing == "RIGHT":
            spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
        spr = spr.resize((16 * scale, 32 * scale), Image.NEAREST)
        im.paste(spr, (x * 16 * scale, (y * 16 - 16) * scale), spr)
    return im


def render(g, solid, m, out):
    from PIL import Image, ImageDraw
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    R, r = renderer()
    def img(grid):
        return R.render_blocks(r, blockdata(grid, solid).reshape(-1), W).convert("RGBA")
    cold = img(g)
    s = 2
    people(cold.resize((W * 16 * s, H * 16 * s), Image.NEAREST), s).convert("RGB").save(out / "temple_demeter.png")
    lit = img(lit_grid(g, SEASONS))
    people(lit.resize((W * 16 * s, H * 16 * s), Image.NEAREST), s).convert("RGB").save(out / "temple_demeter_map_lit.png")
    # in the dark: the torch's 3.5-tile radius round the player at the Spring brazier's foot,
    # with Autumn and Winter lit (their quarters bright)
    two = img(lit_grid(g, ["autumn", "winter"]))
    arr = np.array(two).astype(np.float32)
    px, py = (seed_cell("spring")[0] * 16 + 8, seed_cell("spring")[1] * 16 + 8)
    yy, xx = np.mgrid[0:H * 16, 0:W * 16]
    near = (xx - px) ** 2 + (yy - py) ** 2 <= 56 ** 2
    bright = np.zeros_like(near)
    for sname in ("autumn", "winter"):
        x0, y0, x1, y1 = ZONES[sname]
        bright |= (xx >= x0 * 16) & (xx < (x1 + 1) * 16) & (yy >= y0 * 16) & (yy < (y1 + 1) * 16)
    mask = near | bright
    arr[..., :3][~mask] *= 0.08
    Image.fromarray(arr.astype(np.uint8)).resize((W * 16 * s, H * 16 * s), Image.NEAREST).convert("RGB").save(out / "temple_demeter_map_dark.png")
    # events
    ev = cold.resize((W * 16 * s, H * 16 * s), Image.NEAREST)
    ov = Image.new("RGBA", ev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = 16 * s
    for y in range(H):
        for x in range(W):
            if solid[y, x]:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 50))
    colors = {"Pit": (40, 40, 255, 140), "LeaveLitZone": (255, 255, 255, 90)}
    for e in m["coord_events"]:
        name = e["script"][len(PX):]
        col = colors.get(name, (255, 200, 0, 110))
        d.rectangle([e["x"] * c + 4, e["y"] * c + 4, e["x"] * c + c - 5, e["y"] * c + c - 5], fill=col)
    for b in m["bg_events"]:
        d.rectangle([b["x"] * c + 2, b["y"] * c + 2, b["x"] * c + c - 3, b["y"] * c + c - 3], outline=(80, 160, 255, 255), width=2)
    for w in m["warp_events"]:
        d.rectangle([w["x"] * c + 6, w["y"] * c + 6, w["x"] * c + c - 7, w["y"] * c + c - 7], outline=(255, 60, 200, 255), width=3)
    for o in m["object_events"]:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=(40, 255, 90, 255), width=3)
    Image.alpha_composite(ev, ov).convert("RGB").save(out / "temple_demeter_map_events.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run /usr/bin/python3 tools/ichor/art/temple_demeter_build.py --no-compile first")
    g = names_grid()
    solid = solid_grid(g)
    write_layout(g, solid)
    m = write_events(solid)
    splice_script(g)
    errors = check(g, solid, m)
    if args.render:
        render(g, solid, m, args.render)
    for e in errors:
        print("PROBLEM:", e)
    print(f"temple_demeter: {W}x{H}, {len(m['object_events'])} people, {len(m['coord_events'])} triggers, "
          f"{len(m['bg_events'])} bg events, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
