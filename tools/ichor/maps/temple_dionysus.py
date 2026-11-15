#!/usr/bin/env python3
"""The Temple of Dionysus at Thyrsa: the Three-Act Play's map (design/phase3/SCRIPT.md
beat 31 and Part 5), drawn with gTileset_TempleDionysus (design/phase3/TILES_temple_dionysus.md).

ROOM below is the design; this script turns it into LAYOUT_THYRSA_CITY_TEMPLE_OF_DIONYSUS.

1. Writes data/layouts/ThyrsaCity_TempleOfDionysus/map.bin (collision 1 on every
   blocking metatile, elevation 3 throughout) and border.bin, the map's events in
   data/maps/ThyrsaCity_TempleOfDionysus/map.json, and the generated part of its
   scripts.pory (between two markers): the stage's drawing from the play's state
   (curtains, the god-machine, the mask racks) and the walk back to the rack after a
   wrong entrance.
2. Checks the map: people on walkable tiles, warps on the doormat, coord events on
   the doorways, bg events on blocking tiles the player can face; every walkable tile
   reachable once the play is done (the roof from the crane's landing); each act shut
   until the act before it is done; every setmetatile() in scripts.pory hits a cell
   that holds that piece's other state.
3. Renders, in design/phase3/img/ (from the compiled tileset, as the game draws it):
   ThyrsaCity_TempleOfDionysus.png         the layout at 2x, as a player first finds it
   temple_dionysus_map_solved.png          after the play: curtains open, the crane down
   temple_dionysus_map_events.png          2x plan: people, sight, warps, doors, signs
   With --review NAME, sheets drawn straight from the art (no compile needed):
   temple_dionysus_NAME_room.png    the room at 1x, before and after, side by side
   temple_dionysus_NAME_views.png   GBA-screen views (15 x 10 tiles) along the route, 2x

Usage: /usr/bin/python3 tools/ichor/maps/temple_dionysus.py [--check] [--review NAME]
"""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map  # noqa: E402

LAYOUT_ID = "LAYOUT_THYRSA_CITY_TEMPLE_OF_DIONYSUS"
LAYOUT_DIR = ROOT / "data/layouts/ThyrsaCity_TempleOfDionysus"
MAP_DIR = ROOT / "data/maps/ThyrsaCity_TempleOfDionysus"
CATALOG = ROOT / "build/temple_dionysus/catalog.json"
IMG = ROOT / "design/phase3/img"
PREFIX = "ThyrsaCity_TempleOfDionysus_EventScript_"

# --- The design -------------------------------------------------------------------------
# Two-letter codes; LEGEND maps each to (structure, piece) in the tileset's catalog.
LEGEND = {
    "..": ("floor", "planks"), "p2": ("floor", "planks_b"), "pk": ("floor", "planks_knot"),
    "pw": ("floor", "planks_worn"),
    "ss": ("floor", "stage"), "s2": ("floor", "stage_b"), "sg": ("floor", "stage_gilt"),
    "sm": ("floor", "stage_mark"), "sl": ("floor", "stage_lamp"), "##": ("floor", "void"),
    "dI": ("floor", "deck_ivy"), "dC": ("floor", "deck_crate"),
    "ff": ("floor", "flag"), "f2": ("floor", "flag_b"), "f3": ("floor", "flag_c"),
    "dd": ("floor", "deck"), "d2": ("floor", "deck_b"), "de": ("floor", "deck_edge"),
    "dE": ("floor", "deck_edge_b"),
    "WT": ("wall", "cap"), "WL": ("wall", "cap_corner_l"), "WR": ("wall", "cap_corner_r"),
    "SL": ("wall", "side_l"), "SR": ("wall", "side_r"),
    "We": ("wall", "cap_end_l"), "Wf": ("wall", "cap_end_r"), "Wg": ("wall", "cap_gap"),
    "Fi": ("frieze", "ivy"), "Fk": ("frieze", "kantharos"), "Fp": ("frieze", "panther"),
    "Fm": ("frieze", "maenad"), "Fs": ("frieze", "satyr"), "Fg": ("frieze", "grapes"),
    "Jl": ("frieze", "jamb_l"), "Jr": ("frieze", "jamb_r"),
    "B1": ("back", "act1"), "Bg": ("back", "act1_garland"), "B2": ("back", "act2"),
    "Bm": ("back", "act2_masks"), "Bn": ("back", "act2_masks_b"), "Bd": ("back", "deck_face"),
    "BM": ("back", "deck_face_masks"), "BG": ("back", "deck_face_garland"),
    "BA": ("back", "deck_face_arm"),
    "Iu": ("doors", "ivy_upper"), "Id": ("doors", "ivy"), "Cu": ("doors", "crown_upper"),
    "Cd": ("doors", "crown"), "Gu": ("doors", "goat_upper"), "Gd": ("doors", "goat"),
    "cu": ("doors", "crown_painted_upper"), "cd": ("doors", "crown_painted"),
    "gu": ("doors", "goat_painted_upper"), "gd": ("doors", "goat_painted"),
    "Rc": ("rack", "comic"), "Rt": ("rack", "tragic"), "Rs": ("rack", "satyr"),
    "ba": ("audience", "back_a"), "bb": ("audience", "back_b"), "bc": ("audience", "back_c"),
    "fa": ("audience", "front_a"), "fb": ("audience", "front_b"), "fc": ("audience", "front_c"),
    "bl": ("audience", "back_end_l"), "fl": ("audience", "front_end_l"),
    "br": ("audience", "back_end_r"), "fr": ("audience", "front_end_r"),
    "bA": ("audience", "back_arm"), "fA": ("audience", "front_arm"),
    "Tl": ("stair", "top_l"), "Tr": ("stair", "top_r"), "Hl": ("stair", "through_l"),
    "Hr": ("stair", "through_r"), "Kl": ("stair", "steps_l"), "Kr": ("stair", "steps_r"),
    "Ql": ("stair", "foot_closed_l"), "Qr": ("stair", "foot_closed_r"),
    "Mt": ("machine", "mast_top"), "Mm": ("machine", "mast"), "Mw": ("machine", "winch"),
    "Ma": ("machine", "arm"), "Bt": ("machine", "bronteion_top"), "Bb": ("machine", "bronteion"),
    "rc": ("machine", "rope_coil"), "am": ("machine", "amphorae"), "hk": ("machine", "hook"),
    "ep": ("machine", "edge_post"), "lp": ("machine", "lamp_post"), "th": ("machine", "throne"),
    "Eb": ("entry", "base"), "Et": ("entry", "torch_top"), "ET": ("entry", "torch"),
    "Ek": ("entry", "krater"), "Ev": ("entry", "ivy_pot"), "Ey": ("entry", "thyrsoi_top"),
    "EY": ("entry", "thyrsoi"), "Ml": ("entry", "mat_l"), "MM": ("entry", "mat"),
    "Mr": ("entry", "mat_r"), "El": ("entry", "bench_l"), "Er": ("entry", "bench_r"),
    "Ej": ("entry", "jars"),
    "Pp": ("wings", "program"), "Pt": ("wings", "program_torn"),
    "Xa": ("wings", "trunk_l"), "Xb": ("wings", "trunk_r"), "Ya": ("wings", "rail_l"),
    "Yb": ("wings", "rail_r"), "Zb": ("wings", "basket"), "Zf": ("wings", "flats"),
    "Zl": ("wings", "lamp"), "Zs": ("wings", "stool"), "Zw": ("wings", "wigs"),
    "Gl": ("wings", "goatskins_l"), "Gs": ("wings", "goatskins"), "Gr": ("wings", "goatskins_r"),
    "Zh": ("wings", "hay"), "Zp": ("wings", "corner_planks"),
}
for _a, _p in (("1", 1), ("2", 2), ("3", 3)):
    LEGEND.update({f"{_a}c": (f"skene{_p}", "cap"), f"{_a}g": (f"skene{_p}", "cap_gap"),
                   f"{_a}u": (f"skene{_p}", "upper"), f"{_a}U": (f"skene{_p}", "upper_b"),
                   f"{_a}l": (f"skene{_p}", "lower"), f"{_a}L": (f"skene{_p}", "lower_b")})
LEGEND.update({"2e": ("skene2", "upper_end"), "2E": ("skene2", "lower_end")})
ORCH = "OO"   # the orchestra and its altar, 5 x 4, filled in from ORCH_ORIGIN

ROOM = """
WL WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WR
SL Fg Fi Fp Fi Fm Fi Fs Fg Fi Fk Fi Fg Fp Fi Fm Fi Fs Fi Fg SR
SL lp dd d2 Bt dd dd d2 dd dd Mt dd d2 rc d2 dd am dd dd lp SR
SL dI d2 dd Bb dd dC th dd d2 Mm Mw dd d2 dd dd dd d2 dI dd SR
SL de dE de dE de de de dE de Ma de dE de de dE de de dE de SR
SL Bd BM Bd BG BM Bd BG BM Bd BA Bd BM BG Bd BM BG Bd BM Bd SR
SL ba bb bc ba bb bc ba bb bc bA bc bb ba bc bb ba bc bb ba SR
SL fa fb fc fb fa fc fb fa fc fA fb fc fa fb fc fa fb fc fa SR
SL ss ss sl s2 ss ss sl s2 ss hk ss s2 sl ss ss s2 sl ss ss SR
SL sg sg sg sg sg sg sg sg sg sg sg sg sg sg sg sg sg sg sg SR
SL 3c 3c 3c 3c 3g 3c 3c 3c 3c 3g 3c 3c 3c 3c 3g 3c 3c 3c 3c SR
SL 3u 3u 3u 3U Iu 3u 3U 3u 3u Cu 3u 3u 3U 3u Gu 3u 3U 3u 3u SR
SL Rc Rt Rs 3L Id 3l 3L 3l 3l Cd 3l 3l 3L 3l Gd 3l 3L 3l 3l SR
SL .. .. pk .. .. .. .. .. p2 .. .. .. p2 .. .. .. .. pk Zb SR
SL .. p2 .. .. pw pw pk pw pw pw pw pw pw pw pw p2 .. .. Zw SR
SL .. .. Pt .. .. .. Zl .. .. .. Ya Yb .. Zb .. Xa Xb .. Zs SR
SL Tl Tr We WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT SR
SL Hl Hr B2 Bm B2 Bn B2 Bm B2 Bn B2 Bm B2 Bn B2 Bm B2 Bn B2 SR
SL Kl Kr bl ba bb bc ba bb bc ba bb bc ba bb bc ba bb bc ba SR
SL Ql Qr fl fa fb fc fb fa fc fb fa fc fa fb fc fa fb fc fb SR
SL ss ss s2 sl ss ss s2 sl ss ss s2 sl ss ss s2 sl ss ss ss SR
SL ss s2 ss ss sm ss ss ss s2 sm ss ss ss ss sm s2 ss ss ss SR
SL 2c 2c 2c 2c 2g 2c 2c 2c 2c 2g 2c 2c 2c 2c 2g 2c WT WT WT SR
SL 2u 2u 2u 2U Iu 2u 2U 2u 2u Cu 2u 2u 2U 2u Gu 2e Gl Gs Gr SR
SL Rc Rt Rs 2L Id 2l 2L 2l 2l Cd 2l 2l 2L 2l Gd 2E Zp Zp Zh SR
SL .. .. .. .. .. pk .. .. .. .. .. .. p2 .. .. .. .. .. .. SR
SL .. .. p2 Pp pw pw pw Zf pw pw pw pw pw Zs pw pw pw pw .. SR
SL Zw .. .. .. .. .. Xa Xb .. Zb .. Zl .. .. Ya Yb .. .. .. SR
SL WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT Wf Tl Tr SR
SL B1 Bg B1 B1 Bg B1 B1 Bg B1 B1 Bg B1 B1 Bg B1 B1 Bg Hl Hr SR
SL ba bb bc ba bb bc ba bb bc ba bb bc ba bb bc ba br Kl Kr SR
SL fa fb fc fb fa fc fb fa fc fb fa fc fa fb fc fa fr Ql Qr SR
SL ss sl s2 ss ss sl s2 ss ss sl s2 ss ss sl s2 ss ss ss ss SR
SL ss s2 ss ss sm ss ss ss s2 ss ss ss ss ss s2 ss ss ss ss SR
SL 1c 1c 1c 1c 1g 1c 1c 1c 1c 1c 1c 1c 1c 1c 1c 1c 1c 1c 1c SR
SL 1u 1U 1u 1u Iu 1u 1U 1u 1u cu 1u 1u 1U 1u gu 1u 1U 1u 1u SR
SL 1l 1L 1l 1l Id 1l 1L 1l 1l cd 1l 1l Rc 1l gd 1l 1L 1l 1l SR
SL .. p2 .. pk .. .. .. .. .. .. .. .. p2 .. .. .. .. p2 .. SR
SL .. .. Zf .. pw pw pk pw pw pw pw Pp .. .. .. .. Ya Yb .. SR
SL Zs .. .. Zw .. Zl .. .. .. pw .. .. Zb p2 Xa Xb .. .. .. SR
SL WT WT WT WT WT WT WT Wf Wg Wg Wg We WT WT WT WT WT WT WT SR
SL Fg Fi Fp Fi Fs Fi Fk Jr ff ff ff Jl Fk Fi Fm Fi Fp Fi Fg SR
SL Ev ff f2 ff ff Et ff OO OO OO OO OO ff Et ff ff Ey ff Ev SR
SL ff Ek ff f3 ff ET ff OO OO OO OO OO ff ET f2 ff EY ff ff SR
SL ff ff f2 ff ff ff ff OO OO OO OO OO ff ff ff f3 ff ff ff SR
SL f3 El Er ff ff f2 ff OO OO OO OO OO ff f2 ff El Er ff ff SR
SL Ev ff ff Ej ff ff Eb ff f2 ff ff ff ff f3 ff ff ff ff Ev SR
SL ff ff f3 ff ff ff ff ff Ml MM Mr ff ff ff ff ff f2 ff ff SR
"""
ORCH_ORIGIN = (8, 42)
W, H = 21, 48

# --- The play ----------------------------------------------------------------------------
# Each act: its doors (lower cell: the doorway, where the coord event sits; the upper
# cell and the cap gap are the two cells above), its rack pegs, the tile in front of the
# rack where a wrong entrance lands the player, and its program.
DOORS = {1: {"ivy": (5, 36)},
         2: {"ivy": (5, 24), "crown": (10, 24), "goat": (15, 24)},
         3: {"ivy": (5, 12), "crown": (10, 12), "goat": (15, 12)}}
DOOR_ID = {"ivy": 1, "crown": 2, "goat": 3}
PAINTED = {"crown": [(10, 36)], "goat": [(15, 36)]}
RACKS = {1: {"comic": (13, 36)},
         2: {"comic": (1, 24), "tragic": (2, 24), "satyr": (3, 24)},
         3: {"comic": (1, 12), "tragic": (2, 12), "satyr": (3, 12)}}
MASK_ID = {"comic": 1, "tragic": 2, "satyr": 3}
RACK_FRONT = {1: (13, 37), 2: (2, 25), 3: (2, 13)}
PROGRAMS = {1: (12, 38), 2: (4, 26), 3: (3, 15)}
CURTAINS = {1: [(18, 31), (19, 31)], 2: [(1, 19), (2, 19)]}   # opened when act N is done
CRANE = {(10, 2): "mast_top", (10, 3): "mast", (10, 4): "arm", (10, 5): "deck_face_arm",
         (10, 6): "back_arm", (10, 7): "front_arm", (10, 8): "hook"}
HOOK = (10, 8)
ROOF_LANDING = (11, 4)            # where the god-machine sets the player down
DOOR_LANDING = (10, 46)           # where the player is set down after Thespis
MAT = [(9, 47), (10, 47), (11, 47)]
ALTAR = [(x, y) for y in (43, 44) for x in (8 + 1, 9 + 1, 10 + 1)]

# People: (local id, graphics, x, y, facing, trainer sight or None, script)
PEOPLE = [
    ("LOCALID_DIONYSUS_LASOS", "OBJ_EVENT_GFX_ICHOR_ELDER_M", 13, 46, "DOWN", None, "Lasos"),
    # The image wears Oinoe's ivy garland once it is laid: VAR_OBJ_GFX_ID_1, set in ON_TRANSITION
    ("LOCALID_DIONYSUS_IMAGE", "OBJ_EVENT_GFX_VAR_1", 7, 46, "DOWN", None, "Image"),
    ("LOCALID_DIONYSUS_MYNNISKOS", "OBJ_EVENT_GFX_ICHOR_ACTOR", 8, 39, "UP", 3, "Mynniskos"),
    ("LOCALID_DIONYSUS_THETTALOS", "OBJ_EVENT_GFX_ICHOR_ACTOR", 18, 24, "UP", 1, "Thettalos"),
    ("LOCALID_DIONYSUS_THEODOROS", "OBJ_EVENT_GFX_ICHOR_ACTOR", 4, 15, "UP", 3, "Theodoros"),
    # Thespis wears the tragic or the comic mask: VAR_OBJ_GFX_ID_0, set in ON_TRANSITION
    ("LOCALID_DIONYSUS_THESPIS", "OBJ_EVENT_GFX_VAR_0", 7, 4, "DOWN", None, "Thespis"),
]
THESPIS_AT_ALTAR = (13, 44)

ELEVATION = 3


def load_catalog():
    if not CATALOG.exists():
        sys.exit("temple_dionysus: run tools/ichor/art/temple_dionysus_build.py first")
    cat = {s["key"]: s for s in json.loads(CATALOG.read_text())["structures"]}
    return cat


class Pieces:
    """(structure, piece) <-> metatile id, and walk codes, from the tileset's catalog."""

    def __init__(self, cat):
        self.cat = cat
        self.id = {}
        self.walk = {}
        self.top = {}
        for key, s in cat.items():
            for name, (cx, cy) in s["names"].items():
                mid = s["ids"][cy][cx]
                self.id[(key, name)] = mid
                self.walk[mid] = s["walk"][cy][cx]
                self.top[mid] = s.get("top", [[False] * s["w"]] * s["h"])[cy][cx]
            # unnamed cells of a structure (the orchestra) by position
            for cy in range(s["h"]):
                for cx in range(s["w"]):
                    mid = s["ids"][cy][cx]
                    self.walk.setdefault(mid, s["walk"][cy][cx])
        self.name = {v: k for k, v in self.id.items()}

    def __call__(self, key, name):
        return self.id[(key, name)]

    def passable(self, mid):
        return self.walk[mid] in ".ST"


def grid_ids(pieces, room=None):
    rows = [r.split() for r in (room or ROOM).strip().splitlines()]
    if len(rows) != H:
        raise ValueError(f"ROOM is {len(rows)} rows, expected {H}")
    for n, r in enumerate(rows):
        if len(r) != W:
            raise ValueError(f"ROOM row {n} is {len(r)} wide, expected {W}")
    g = [[None if c == ORCH else pieces(*LEGEND[c]) for c in r] for r in rows]
    ox, oy = ORCH_ORIGIN
    orch = pieces.cat["orchestra"]
    for j in range(orch["h"]):
        for i in range(orch["w"]):
            if rows[oy + j][ox + i] != ORCH:
                raise ValueError(f"orchestra cell ({ox + i},{oy + j}) is {rows[oy + j][ox + i]}")
            g[oy + j][ox + i] = orch["ids"][j][i]
    if any(v is None for r in g for v in r):
        raise ValueError("ROOM has orchestra cells outside ORCH_ORIGIN's block")
    return g


def lowered(pieces, key, name):
    """The other state of a two-state piece (lowered/open/empty), by its name."""
    mid = pieces(key, name)
    return {"mast_top": pieces("machine", "mast_top_lowered"),
            "mast": pieces("machine", "mast_lowered"),
            "arm": pieces("machine", "arm_lowered"),
            "deck_face_arm": pieces("back", "deck_face_arm_lowered"),
            "back_arm": pieces("audience", "back_arm_lowered"),
            "front_arm": pieces("audience", "front_arm_lowered"),
            "hook": pieces("machine", "hook_lowered")}.get(name, mid)


def staged(pieces, g, state=0, mask=None):
    """The grid at a state of the play: 0 nothing done, 1 Act I done, 2 Act II done,
    3 the play done (the crane down). mask = (act, mask name) shows that peg empty."""
    out = [row[:] for row in g]
    opened = {"foot_closed_l": pieces("stair", "foot_open_l"),
              "foot_closed_r": pieces("stair", "foot_open_r")}
    for act, cells in CURTAINS.items():
        if state >= act:
            for x, y in cells:
                out[y][x] = opened[pieces.name[out[y][x]][1]]
    if state >= 3:
        for (x, y), name in CRANE.items():
            key = pieces.name[out[y][x]][0]
            out[y][x] = lowered(pieces, key, name)
    if mask:
        act, m = mask
        x, y = RACKS[act][m]
        out[y][x] = pieces("rack", f"{m}_empty")
    return out


def layout_blocks(pieces, g):
    out = []
    for row in g:
        for mid in row:
            v = mid | ((0 if pieces.passable(mid) else 1) << 10) | (ELEVATION << 12)
            out.append(v)
    return np.array(out, "<u2")


def border_blocks(pieces):
    return np.array([pieces("floor", "void")] * 4, "<u2")


# --- map.json events ----------------------------------------------------------------------

def events():
    obj = []
    for lid, gfx, x, y, facing, sight, script in PEOPLE:
        obj.append({
            "local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": ELEVATION,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0,
            "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight or 0),
            "script": PREFIX + script, "flag": "0"})
    warps = [{"x": x, "y": y, "elevation": 0, "dest_map": "MAP_THYRSA_CITY", "dest_warp_id": "3"}
             for x, y in [MAT[1], MAT[0], MAT[2]]]
    coords = []
    for act, doors in DOORS.items():
        for door, (x, y) in doors.items():
            coords.append({"type": "trigger", "x": x, "y": y, "elevation": ELEVATION,
                           "var": "VAR_ICHOR_THREE_ACT_PLAY", "var_value": str(act - 1),
                           "script": f"{PREFIX}Door_Act{act}_{door.title()}"})
    for x in (9, 10, 11):
        coords.append({"type": "trigger", "x": x, "y": 46, "elevation": ELEVATION,
                       "var": "VAR_ICHOR_THREE_ACT_PLAY", "var_value": "0",
                       "script": f"{PREFIX}LasosWelcome"})
    bgs = []

    def sign(x, y, script, facing="ANY"):
        bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                    "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{facing}",
                    "script": PREFIX + script})
    for act, (x, y) in PROGRAMS.items():
        sign(x, y, f"Program_Act{act}")
    for act, pegs in RACKS.items():
        for (x, y) in pegs.values():
            sign(x, y, f"Rack_Act{act}", "NORTH")
    for kind, cellsl in PAINTED.items():
        for x, y in cellsl:
            sign(x, y, f"Painted{kind.title()}Door", "NORTH")
    for act, cellsl in CURTAINS.items():
        for x, y in cellsl:
            sign(x, y, f"Curtain_Act{act}", "NORTH")
    sign(*HOOK, "Hook", "NORTH")
    for x, y in ALTAR:
        sign(x, y, "Altar")
    sign(4, 2, "Thunder")
    sign(4, 3, "Thunder")
    sign(2, 43, "Krater")
    sign(17, 42, "Thyrsoi")
    sign(17, 43, "Thyrsoi")
    return {"object_events": obj, "warp_events": warps, "coord_events": coords, "bg_events": bgs}


def write_map_json(ev):
    p = MAP_DIR / "map.json"
    d = json.loads(p.read_text())
    d["music"] = "MUS_ICHOR_TEMPLE_HERMES"   # ICHOR_STUB_MUSIC: MUS_ICHOR_TEMPLE_DIONYSUS
    d.update(ev)
    p.write_text(json.dumps(d, indent=2) + "\n")


# --- The generated scripts ----------------------------------------------------------------

SCRIPT_BEGIN = ("// --- Stage scripts: generated by tools/ichor/maps/temple_dionysus.py from the "
                "room. Do not edit. ---")
SCRIPT_END = "// --- End of generated stage scripts. ---"


def label(pieces, mid):
    key, name = pieces.name[mid]
    table = {
        ("rack", "comic"): "Peg_Comic", ("rack", "comic_empty"): "Peg_Comic_Empty",
        ("rack", "tragic"): "Peg_Tragic", ("rack", "tragic_empty"): "Peg_Tragic_Empty",
        ("rack", "satyr"): "Peg_Satyr", ("rack", "satyr_empty"): "Peg_Satyr_Empty",
        ("stair", "foot_closed_l"): "CurtainClosed_L", ("stair", "foot_closed_r"): "CurtainClosed_R",
        ("stair", "foot_open_l"): "CurtainOpen_L", ("stair", "foot_open_r"): "CurtainOpen_R",
        ("machine", "mast_top"): "MastTop", ("machine", "mast_top_lowered"): "MastTop_Lowered",
        ("machine", "mast"): "Mast", ("machine", "mast_lowered"): "Mast_Lowered",
        ("machine", "arm"): "Arm", ("machine", "arm_lowered"): "Arm_Lowered",
        ("machine", "hook"): "Hook", ("machine", "hook_lowered"): "Hook_Lowered",
        ("back", "deck_face_arm"): "DeckFaceArm", ("back", "deck_face_arm_lowered"): "DeckFaceArm_Lowered",
        ("audience", "back_arm"): "TierBackArm", ("audience", "back_arm_lowered"): "TierBackArm_Lowered",
        ("audience", "front_arm"): "TierFrontArm", ("audience", "front_arm_lowered"): "TierFrontArm_Lowered",
    }
    return "METATILE_TempleDionysus_" + table[(key, name)]


def setmt(pieces, x, y, mid):
    blocked = "FALSE" if pieces.passable(mid) else "TRUE"
    return f"    setmetatile({x}, {y}, {label(pieces, mid)}, {blocked})"


def return_path(act, door_xy):
    """The walk from a doorway back to the act's rack: down into the wings, then along
    the row in front of the skene."""
    x, y = door_xy
    fx, fy = RACK_FRONT[act]
    assert fy == y + 1
    steps = ["walk_faster_down"]
    dx = fx - x
    if dx:
        steps.append(f"walk_faster_{'right' if dx > 0 else 'left'} * {abs(dx)}")
    steps.append("face_up")
    return steps


def generated_script(pieces, g):
    out = [SCRIPT_BEGIN, ""]
    out.append("// Draws the stage from the play's state: the curtains of finished acts drawn back,")
    out.append("// and the god-machine's arm swung down once the play is done.")
    out.append(f"script {PREFIX}DrawStage {{")
    solved = staged(pieces, g, 3)
    for act, cellsl in CURTAINS.items():
        out.append(f"    if (var(VAR_ICHOR_THREE_ACT_PLAY) >= {act}) {{")
        for x, y in cellsl:
            out.append("    " + setmt(pieces, x, y, solved[y][x]))
        out.append("    }")
    out.append("    if (var(VAR_ICHOR_THREE_ACT_PLAY) >= 3) {")
    for (x, y) in CRANE:
        out.append("    " + setmt(pieces, x, y, solved[y][x]))
    out.append("    }")
    out.append("    return")
    out.append("}")
    out.append("")
    out.append("// Every peg full, then the peg of the mask the player wears (VAR_TEMP_1) on the rack")
    out.append("// it came from (VAR_TEMP_3) empty.")
    out.append(f"script {PREFIX}DrawRacks {{")
    for act, pegs in RACKS.items():
        for m, (x, y) in pegs.items():
            out.append(setmt(pieces, x, y, g[y][x]))
    for act, pegs in RACKS.items():
        for m, (x, y) in pegs.items():
            out.append(f"    if (var(VAR_TEMP_3) == {act} && var(VAR_TEMP_1) == {MASK_ID[m]}) {{")
            out.append("    " + setmt(pieces, x, y, pieces("rack", f"{m}_empty")))
            out.append("    }")
    out.append("    return")
    out.append("}")
    out.append("")
    out.append("// A wrong entrance: back down into the wings and along to the act's rack (the screen")
    out.append("// is black while this plays).")
    out.append(f"script {PREFIX}WalkBackToRack {{")
    first = True
    for act, doors in DOORS.items():
        for door in doors:
            kw = "if" if first else "} elif"
            out.append(f"    {kw} (var(VAR_0x8005) == {act} && var(VAR_0x8004) == {DOOR_ID[door]}) {{")
            out.append(f"        applymovement(LOCALID_PLAYER, {PREFIX[:-12]}Movement_Back_Act{act}_{door.title()})")
            first = False
    out.append("    }")
    out.append("    waitmovement(0)")
    out.append("    return")
    out.append("}")
    for act, doors in DOORS.items():
        for door, xy in doors.items():
            out.append("")
            out.append(f"movement {PREFIX[:-12]}Movement_Back_Act{act}_{door.title()} {{")
            for st in return_path(act, xy):
                out.append(f"    {st}")
            out.append("}")
    out.append("")
    out.append(SCRIPT_END)
    return "\n".join(out)


def spliced_script(pieces, g):
    text = (MAP_DIR / "scripts.pory").read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"temple_dionysus: scripts.pory needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    return text[:a] + generated_script(pieces, g) + text[b + len(SCRIPT_END):]


# --- Checks -----------------------------------------------------------------------------

def walkable(pieces, g, x, y):
    return 0 <= y < H and 0 <= x < W and pieces.passable(g[y][x])


def reachable(pieces, g, start, people=()):
    seen = {start}
    todo = deque([start])
    while todo:
        x, y = todo.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and n not in people and walkable(pieces, g, *n):
                seen.add(n)
                todo.append(n)
    return seen


def metatile_labels():
    text = (ROOT / "include/constants/metatile_labels.h").read_text()
    return {k: int(v, 16) for k, v in re.findall(r"#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+)", text)}


def check(pieces, g, ev):
    errors = []
    people = {(o["x"], o["y"]) for o in ev["object_events"]}
    solved = staged(pieces, g, 3)
    start = MAT[1]

    for o in ev["object_events"]:
        if not walkable(pieces, g, o["x"], o["y"]) and o["local_id"] != "LOCALID_DIONYSUS_IMAGE":
            errors.append(f"{o['local_id']} stands on a blocking tile")
    tx, ty = THESPIS_AT_ALTAR
    if not walkable(pieces, g, tx, ty):
        errors.append("Thespis's place by the altar is blocked")
    for w in ev["warp_events"]:
        if pieces.name[g[w["y"]][w["x"]]][1] not in ("mat", "mat_l", "mat_r"):
            errors.append(f"warp at ({w['x']},{w['y']}) is not on the doormat")
    for c in ev["coord_events"]:
        nm = pieces.name[g[c["y"]][c["x"]]][1]
        if c["script"].endswith("LasosWelcome"):
            if not walkable(pieces, g, c["x"], c["y"]):
                errors.append(f"Lasos's trigger ({c['x']},{c['y']}) is blocked")
        elif nm not in ("ivy", "crown", "goat"):
            errors.append(f"door trigger at ({c['x']},{c['y']}) is on {nm}, not a doorway")
    for act, doors in DOORS.items():
        for door, (x, y) in doors.items():
            want = [pieces.name[g[y - 2][x]][1], pieces.name[g[y - 1][x]][1], pieces.name[g[y][x]][1]]
            if want != ["cap_gap", f"{door}_upper", door]:
                errors.append(f"Act {act}'s {door} door at ({x},{y}) is {want}")
            if not walkable(pieces, g, x, y + 1) or not walkable(pieces, g, x, y - 3):
                errors.append(f"Act {act}'s {door} door at ({x},{y}) has no wings or stage tile")
            for st in return_path(act, (x, y)):
                pass
            fx, fy = RACK_FRONT[act]
            for xx in range(min(x, fx), max(x, fx) + 1):
                if not walkable(pieces, g, xx, y + 1):
                    errors.append(f"the walk back from Act {act}'s {door} door crosses a blocked tile ({xx},{y + 1})")
    for act, pegs in RACKS.items():
        for m, (x, y) in pegs.items():
            if pieces.name[g[y][x]] != ("rack", m):
                errors.append(f"Act {act}'s {m} peg at ({x},{y}) is {pieces.name[g[y][x]]}")
    for (x, y), name in CRANE.items():
        if pieces.name[g[y][x]][1] != name:
            errors.append(f"the crane cell ({x},{y}) is {pieces.name[g[y][x]]}, not {name}")

    empty_room = reachable(pieces, solved, start)
    roof = reachable(pieces, solved, ROOF_LANDING)
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        if walkable(pieces, g, x, y) and not b["script"].endswith(("Curtain_Act1", "Curtain_Act2", "Hook")):
            errors.append(f"bg event at ({x},{y}) is on a walkable tile")
        if not any((x + dx, y + dy) in empty_room | roof for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            errors.append(f"bg event at ({x},{y}) can't be faced from anywhere")

    every = {(x, y) for y in range(H) for x in range(W) if walkable(pieces, solved, x, y)}
    stranded = sorted(every - empty_room - roof)
    if stranded:
        errors.append(f"walkable but unreachable: {stranded}")
    if roof & empty_room:
        errors.append("the skene roof can be walked to: it should only be reached by the machine")
    if ROOF_LANDING not in roof or THESPIS_AT_ALTAR not in empty_room or DOOR_LANDING not in empty_room:
        errors.append("a landing tile is unreachable")

    # Each act stays shut until the one before it is done.
    for state in (0, 1, 2):
        here = reachable(pieces, staged(pieces, g, state), start)
        for act in (2, 3):
            fx, fy = RACK_FRONT[act]
            if act <= state + 1 and (fx, fy) not in here:
                errors.append(f"with {state} acts done, Act {act}'s wings should be open")
            if act > state + 1 and (fx, fy) in here:
                errors.append(f"with {state} acts done, Act {act}'s wings are already open")
        # the stage of the act being played is only reached through its doors
        act = state + 1
        sx, sy = list(DOORS[act].values())[0]
        stage = (sx, sy - 3)
        walls = {(x, y) for x, y in DOORS[act].values()}
        if stage in reachable(pieces, staged(pieces, g, state), start, walls):
            errors.append(f"Act {act}'s stage can be reached without going through a door")

    # Trainers: sight across the only way between the rack and the doors.
    for lid, gfx, x, y, facing, sight, script in PEOPLE:
        if script in ("Mynniskos", "Theodoros"):
            act = 1 if script == "Mynniskos" else 3
            col = {(x, y - k) for k in range(1, sight + 1)}
            here = staged(pieces, g, 3)
            rf = RACK_FRONT[act]
            for door, dxy in DOORS[act].items():
                if door != "ivy" and act == 1:
                    continue
                front = (dxy[0], dxy[1] + 1)
                if front in reachable(pieces, here, rf, col | {(x, y)}):
                    errors.append(f"{script} can be walked round between the rack and the {door} door")

    labels = metatile_labels()
    script = (MAP_DIR / "scripts.pory").read_text()
    calls = re.findall(r"setmetatile\((\d+),\s*(\d+),\s*(METATILE_\w+)", script)
    for x, y, lab in calls:
        x, y = int(x), int(y)
        if lab not in labels:
            errors.append(f"setmetatile uses unknown label {lab}")
            continue
        mid = labels[lab]
        allowed = {g[y][x], solved[y][x]}
        for act, pegs in RACKS.items():
            for m, xy in pegs.items():
                if xy == (x, y):
                    allowed.add(pieces("rack", f"{m}_empty"))
        if mid not in allowed:
            errors.append(f"setmetatile({x}, {y}, {lab}) puts {pieces.name.get(mid)} over {pieces.name[g[y][x]]}")
    if script != spliced_script(pieces, g):
        errors.append("scripts.pory's stage scripts are out of date; run tools/ichor/maps/temple_dionysus.py")
    return errors


# --- Renders ------------------------------------------------------------------------------

def compiled_renderer(layout):
    render_map.read_fieldmap_constants()
    symbols = render_map.scan_tileset_symbols()
    prim = render_map.resolve_tileset(layout["primary_tileset"], symbols)
    sec = render_map.resolve_tileset(layout["secondary_tileset"], symbols)
    return render_map.Renderer(render_map.Tileset(prim), render_map.Tileset(sec))


class SourceRenderer:
    """Draws metatiles straight from the art's layers (no Porytiles compile)."""

    def __init__(self, pieces):
        import eleusa_lib as E
        import temple_dionysus_art as T
        self.tiles = {}
        for s in T.build():
            img = E.composite(s)
            d = pieces.cat[s.key]
            for cy in range(s.h):
                for cx in range(s.w):
                    self.tiles[d["ids"][cy][cx]] = img[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        self.void = self.tiles[pieces("floor", "void")]

    def render(self, g, margin=0):
        h, w = len(g), len(g[0])
        img = np.empty(((h + 2 * margin) * 16, (w + 2 * margin) * 16, 3), np.uint8)
        for y in range(h + 2 * margin):
            for x in range(w + 2 * margin):
                gx, gy = x - margin, y - margin
                inside = 0 <= gx < w and 0 <= gy < h
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = self.tiles[g[gy][gx]] if inside else self.void
        return Image.fromarray(img)


def scaled(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


def font(size):
    return ImageFont.load_default(size=size)


def labelled(img, text, pad=22):
    out = Image.new("RGB", (img.width, img.height + pad), (40, 40, 48))
    out.paste(img, (0, pad))
    ImageDraw.Draw(out).text((6, 4), text, fill=(230, 230, 200), font=font(14))
    return out


def sheet(images, cols, gap=10, bg=(40, 40, 48)):
    w = max(i.width for i in images)
    h = max(i.height for i in images)
    rows = (len(images) + cols - 1) // cols
    out = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * h + (rows + 1) * gap), bg)
    for n, im in enumerate(images):
        r, c = divmod(n, cols)
        out.paste(im, (gap + c * (w + gap), gap + r * (h + gap)))
    return out


def screen_view(img, margin, cx, cy):
    """The 240 x 160 GBA screen with the camera on tile (cx, cy)."""
    x0 = (cx + margin - 7) * 16
    y0 = (cy + margin) * 16 - 72
    return img.crop((x0, y0, x0 + 240, y0 + 160))


VIEWS = [
    ("the door: Lasos, the image, the altar", 10, 46), ("the parodos", 10, 41),
    ("Act I's wings", 10, 38), ("Mynniskos and the ivy door", 7, 38),
    ("Act I's stage and the curtain", 14, 32), ("the stair up", 18, 29),
    ("Act II's wings: the satyrs' corner", 15, 26), ("Act II's rack and program", 6, 26),
    ("Act II's stage", 6, 20), ("Act III's wings", 6, 14), ("Act III's doors", 13, 14),
    ("the god-machine's hook", 10, 9), ("the skene roof", 10, 4),
]


def overlay(base, ev, pieces, g, s=2):
    img = scaled(base, s).convert("RGBA")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    c = 16 * s

    def box(x, y, fill, outline):
        d.rectangle([x * c + 1, y * c + 1, x * c + c - 2, y * c + c - 2], fill=fill, outline=outline, width=2)

    for b in ev["bg_events"]:
        box(b["x"], b["y"], (80, 160, 255, 60), (80, 160, 255, 220))
    for t in ev["coord_events"]:
        box(t["x"], t["y"], (255, 220, 0, 70), (255, 220, 0, 230))
    for w in ev["warp_events"]:
        d.rectangle([w["x"] * c + 6, w["y"] * c + 6, w["x"] * c + c - 7, w["y"] * c + c - 7],
                    outline=(255, 60, 200, 255), width=2)
    for act, (x, y) in RACK_FRONT.items():
        d.ellipse([x * c + 8, y * c + 8, x * c + c - 9, y * c + c - 9], outline=(120, 255, 255, 255), width=2)
    sight = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if o["trainer_type"] != "TRAINER_TYPE_NONE":
            dx, dy = sight[o["movement_type"].split("_")[-1]]
            for k in range(1, int(o["trainer_sight_or_berry_tree_id"]) + 1):
                if walkable(pieces, g, x + dx * k, y + dy * k):
                    box(x + dx * k, y + dy * k, (255, 60, 40, 70), (255, 60, 40, 255))
        box(x, y, (40, 220, 90, 110), (20, 120, 40, 255))
        name = o["local_id"].removeprefix("LOCALID_DIONYSUS_").title()
        d.text((x * c + c // 2, y * c - 2), name, fill=(255, 255, 255, 255), font=font(11),
               anchor="md", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    tx, ty = THESPIS_AT_ALTAR
    d.rectangle([tx * c + 4, ty * c + 4, tx * c + c - 5, ty * c + c - 5], outline=(40, 220, 90, 200), width=1)
    img = Image.alpha_composite(img, over)
    key = [((40, 220, 90), "person (Thespis's place after the laurel, outlined)"),
           ((255, 60, 40), "trainer sight"), ((80, 160, 255), "bg event"),
           ((255, 220, 0), "coord event: the doors, Lasos's welcome"),
           ((255, 60, 200), "warp to Thyrsa"), ((120, 255, 255), "where a wrong entrance sets you down")]
    pad = 18
    out = Image.new("RGBA", (img.width, img.height + pad * len(key) + 8), (40, 40, 48, 255))
    out.paste(img, (0, 0))
    d = ImageDraw.Draw(out)
    for i, (col, text) in enumerate(key):
        y = img.height + 6 + i * pad
        d.rectangle([8, y, 20, y + 12], fill=col)
        d.text((28, y), text, fill=(230, 230, 200), font=font(11))
    return out.convert("RGB")


def review(name, pieces, g):
    r = SourceRenderer(pieces)
    first = r.render(g)
    solved = r.render(staged(pieces, g, 3, mask=(3, "satyr")))
    sheet([labelled(first, "as you first find it"), labelled(solved, "the play done (wearing the satyr mask)")],
          2).save(IMG / f"temple_dionysus_{name}_room.png")
    margin = 8
    big = r.render(staged(pieces, g, 3), margin)
    views = [labelled(scaled(screen_view(big, margin, x, y), 2), f"{t} ({x},{y})") for t, x, y in VIEWS]
    sheet(views, 3).save(IMG / f"temple_dionysus_{name}_views.png")
    return [IMG / f"temple_dionysus_{name}_{k}.png" for k in ("room", "views")]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="verify the layout files are current")
    ap.add_argument("--review", metavar="NAME", help="write review sheets from the art")
    args = ap.parse_args()

    pieces = Pieces(load_catalog())
    g = grid_ids(pieces)
    if args.review:
        for p in review(args.review, pieces, g):
            print(p.relative_to(ROOT))
        return

    layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    layout = next(l for l in layouts if l.get("id") == LAYOUT_ID)
    if (layout["width"], layout["height"]) != (W, H):
        sys.exit(f"temple_dionysus: layouts.json says {layout['width']}x{layout['height']}, the room is {W}x{H}")

    blocks, border = layout_blocks(pieces, g), border_blocks(pieces)
    ev = events()
    if args.check:
        stale = [p.name for p, want in ((LAYOUT_DIR / "map.bin", blocks), (LAYOUT_DIR / "border.bin", border))
                 if not p.exists() or not np.array_equal(np.fromfile(p, "<u2"), want)]
        cur = json.loads((MAP_DIR / "map.json").read_text())
        if any(cur[k] != v for k, v in ev.items()):
            stale.append("map.json")
        if stale:
            sys.exit(f"temple_dionysus: {', '.join(stale)} out of date; run tools/ichor/maps/temple_dionysus.py")
    else:
        LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
        blocks.tofile(LAYOUT_DIR / "map.bin")
        border.tofile(LAYOUT_DIR / "border.bin")
        write_map_json(ev)
        (MAP_DIR / "scripts.pory").write_text(spliced_script(pieces, g))

    errors = check(pieces, g, ev)
    if errors:
        sys.exit("temple_dionysus: " + "\n  ".join(["layout check failed:"] + errors))

    if not args.check:
        r = compiled_renderer(layout)
        first = render_map.render_blocks(r, blocks, W)
        solved = render_map.render_blocks(r, layout_blocks(pieces, staged(pieces, g, 3)), W)
        IMG.mkdir(parents=True, exist_ok=True)
        scaled(first, 2).save(IMG / "ThyrsaCity_TempleOfDionysus.png")
        scaled(solved, 2).save(IMG / "temple_dionysus_map_solved.png")
        overlay(first, ev, pieces, g).save(IMG / "temple_dionysus_map_events.png")
    print(f"temple_dionysus: {W}x{H} on {layout['primary_tileset']} + {layout['secondary_tileset']}, "
          f"{len(ev['object_events'])} people, {len(ev['coord_events'])} triggers, "
          f"{len(ev['bg_events'])} bg events; checks pass")


if __name__ == "__main__":
    main()
