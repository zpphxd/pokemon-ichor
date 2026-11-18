#!/usr/bin/env python3
"""Lay out the four seats of the Pantheon on their own tilesets
(tools/ichor/art/pantheon_build.py; design/maps/Olympus_Pantheon.md).

Every seat is one long hall walked from the south door to the seat-holder:

  Olympus_SeatOfAres      gTileset_SeatAres      the war hall: tropaia and braziers down a bloodred floor
  Olympus_SeatOfPoseidon  gTileset_SeatPoseidon  the sea hall: a causeway across the basin, coral columns
  Olympus_SeatOfAthena    gTileset_SeatAthena    the hall of lamps: owls, scrolls, the sacred olive
  Olympus_SeatOfHera      gTileset_SeatHera      the peacock hall: feather columns, torches to the throne

The cells the scripts swap (the doors, braziers, lamps and torches) are read
from these layouts by tools/ichor/maps/league_seats.py through SWAPS, so a
re-laid hall never leaves a script pointing at a stale cell.

Usage: run through tools/ichor/maps/olympus.py (--only Ares,Poseidon,Athena,Hera).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
from league_lib import Grid, noise  # noqa: E402
import pantheon_lib as PL  # noqa: E402


def seat_fields(music="MUS_NONE"):
    return dict(map_type="MAP_TYPE_INDOOR", weather="WEATHER_NONE", show_map_name=False,
                allow_cycling=False, allow_escaping=False, music=music, ichor_kind="interior")


class Hall:
    """A Grid on one seat's tileset, with its catalog's pieces by key."""

    def __init__(self, name, folder, w, h):
        self.cat = PL.catalog(folder)
        self.g = Grid(name, w, h, primary="gTileset_Oikos",
                      secondary="gTileset_Seat" + folder.split("_", 1)[1].capitalize(), cat=None)
        self.g.cat = self.cat
        self.W, self.H = w, h

    def id(self, key, name=None):
        p = self.cat[key]
        if name is None:
            return p["ids"][0][0]
        cx, cy = p["names"][name]
        return p["ids"][cy][cx]

    def cell(self, x, y, key, solid=None, kind=""):
        p = self.cat[key]
        s = p["walk"][0][0] in "XS" if solid is None else solid
        self.g.set(x, y, p["ids"][0][0], s, kind or key)

    def piece(self, key, x, y):
        self.g.piece(key, x, y)

    def ids(self, key):
        return self.cat[key]["ids"]


# Swapped cells per seat, filled by each builder: {seat: {what: [(x, y, id, solid)]}},
# written to SWAPS_PATH for tools/ichor/maps/league_seats.py.
SWAPS = {}
SWAPS_PATH = Path(__file__).resolve().parent / "pantheon_swaps.json"


def save_swaps(seat):
    import json
    data = json.loads(SWAPS_PATH.read_text()) if SWAPS_PATH.exists() else {}
    data[seat] = SWAPS[seat]
    SWAPS_PATH.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


def pick(seq, x, y, salt):
    return seq[noise(x, y, salt) % len(seq)]


# ---------------------------------------------------------------------------
# The seat of Ares
# ---------------------------------------------------------------------------

def seat_of_ares():
    W, H = 19, 26
    A = Hall("Olympus_SeatOfAres", "seat_ares", W, H)
    g = A.g
    def fl(x, y):
        k = f"{x % 4}_{y % 2}"
        if f"crack_{k}" in A.cat and noise(x, y, 11) < 12:
            return f"crack_{k}"
        return f"floor_{k}"

    for y in range(H):
        for x in range(W):
            A.cell(x, y, fl(x, y), False, "floor")
    # the north wall: cornice, the face hung with shields and banners, the base
    face = {1: "wall1_shield", 2: "wall1_spears", 3: "wall1_shield", 4: "wall1_banner", 5: "wall1_shield",
            6: "wall1_spears", 7: "wall1_shield", 11: "wall1_shield", 12: "wall1_spears", 13: "wall1_shield",
            14: "wall1_banner", 16: "wall1_spears", 17: "wall1_shield"}
    for x in range(1, W - 1):
        A.cell(x, 0, f"wall0_{x % 2}", True)
        A.cell(x, 1, face.get(x, f"wall1_{x % 2}"), True)
        A.cell(x, 2, "wall2_banner" if face.get(x) == "wall1_banner" else f"wall2_{x % 2}", True)
    for y in range(0, H - 1):
        A.cell(0, y, "side_w", True)
        A.cell(W - 1, y, "side_e", True)
    for x in range(W):
        A.cell(x, H - 1, "void", True)
    A.cell(9, H - 1, "mat", False, "mat")
    # the dais across the head of the hall, steps down the middle
    for x in range(3, 16):
        part = "l" if x == 3 else "r" if x == 15 else "m"
        A.cell(x, 3, f"dais_{part}", False, "dais")
        A.cell(x, 4, f"dais_{part}", False, "dais")
        A.cell(x, 5, "steps" if 8 <= x <= 10 else f"riser_{part}", not (8 <= x <= 10), "dais")
    for x in range(1, 3):
        for y in (3, 4, 5):
            A.cell(x, y, f"shade_{x % 4}_{y % 2}" if y == 3 else fl(x, y), False)
    for x in range(16, 18):
        for y in (3, 4, 5):
            A.cell(x, y, f"shade_{x % 4}_{y % 2}" if y == 3 else fl(x, y), False)
    # the bronze Ares at the head of the hall, braziers either side of the polemarch
    A.piece("statue", 8, 0)
    A.piece("brazier_cold", 5, 3)
    A.piece("brazier_cold", 12, 3)
    # the far door, shut until he falls
    A.cell(15, 1, "door_shut1", True)
    A.cell(15, 2, "door_shut2", True)
    # the runner from the south door to the steps, a bronze spear-point every fourth flag
    for y in range(6, H - 1):
        A.cell(8, y, "runner_l", False, "runner")
        A.cell(9, y, "runner_point" if y % 4 == 1 else "runner_m", False, "runner")
        A.cell(10, y, "runner_r", False, "runner")
    for x in list(range(1, 8)) + list(range(11, 18)):
        A.cell(x, 6, f"shade_{x % 4}_{6 % 2}", False)
    # the phalanx: trophies of captured armor in two files, tripod braziers between
    tripods = []
    for y in (8, 14, 20):
        for x in (6, 12):
            A.piece("tropaion", x, y)
    for y in (11, 17):
        for x in (6, 12):
            A.piece("tripod_lit", x, y)
    # the colonnades down both sides; the armory in the bays behind them
    for y in (7, 13, 19):
        A.piece("column", 3, y)
        A.piece("column", 15, y)
    for y in (9, 15):
        A.piece("spear_rack", 1, y)
        A.piece("spear_rack", 16, y)
    for (x, y) in ((1, 7), (17, 7), (1, 21), (17, 21), (2, 13), (16, 13)):
        A.piece("helmet_stand", x, y)
    for (x, y) in ((7, 22), (11, 22)):
        A.piece("tripod_cold", x, y)
        tripods.append((x, y))
    # events
    g.person("BRASIDAS", "HOPLITE", 9, 4, "Brasidas", facing="DOWN")
    g.warp(9, H - 1, "Olympus_Propylaia", 0)
    g.warp(15, 2, "Olympus_SeatOfPoseidon", 0)
    g.save([A.id("void") | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("brasidas", (9, 5))])
    lit = []
    for (x, y) in ((5, 3), (12, 3)):
        ids = A.ids("brazier_lit")
        lit += [(x + dx, y + dy, ids[dy][dx], True) for dy in range(2) for dx in range(2)]
    for (x, y) in tripods:
        ids = A.ids("tripod_lit")
        lit += [(x, y + dy, ids[dy][0], True) for dy in range(2)]
    # (the aisle's tripods between the trophies burn from the start; the two at the
    # door and the polemarch's great braziers catch when he raises his spear)
    SWAPS["Ares"] = dict(
        close=[(9, H - 1, A.id("mat_shut"), True)],
        open=[(15, 1, A.id("door_open1"), True), (15, 2, A.id("door_open2"), False)],
        lit=lit, walk_in=(9, H - 1), seat=(9, 4), pan=H - 1 - 3 - 8)
    save_swaps("Ares")
    return g, [("entrance", 9, H - 4), ("hall", 9, 14), ("dais", 9, 5)]


# ---------------------------------------------------------------------------
# The seat of Poseidon
# ---------------------------------------------------------------------------

def seat_of_poseidon():
    W, H = 21, 26
    A = Hall("Olympus_SeatOfPoseidon", "seat_poseidon", W, H)
    g = A.g
    for y in range(H):
        for x in range(W):
            A.cell(x, y, f"floor_{x % 2}_{y % 2}", False, "floor")
    for x in range(1, W - 1):
        A.cell(x, 0, f"wall0_{x % 2}", True)
        A.cell(x, 1, "wall1_shell" if x % 4 == 2 else "wall1_coral" if x % 4 == 0 else f"wall1_{x % 2}", True)
        A.cell(x, 2, f"wall2_{x % 2}", True)
        A.cell(x, 3, f"shade_{x % 2}_{3 % 2}", False)
    for y in range(0, H - 1):
        A.cell(0, y, "side_w", True)
        A.cell(W - 1, y, "side_e", True)
    for x in range(W):
        A.cell(x, H - 1, "void", True)
    A.cell(10, H - 1, "mat", False, "mat")
    # the admiral's dais and the trident planted behind him
    for x in range(3, 18):
        part = "l" if x == 3 else "r" if x == 17 else "m"
        A.cell(x, 3, f"dais_{part}", False, "dais")
        A.cell(x, 4, f"dais_{part}", False, "dais")
        A.cell(x, 5, "steps" if 9 <= x <= 11 else f"riser_{part}", not (9 <= x <= 11), "dais")
    A.piece("trident", 9, 0)
    A.cell(4, 1, "door_shut1", True)
    A.cell(4, 2, "door_shut2", True)
    for x in (1, 19):
        A.piece("anchor", x, 4)
    A.piece("amphora", 2, 4)
    A.piece("amphora", 18, 4)
    # the basin, both sides of the causeway
    y0, y1 = 7, 21
    for (x0, x1) in ((2, 7), (13, 18)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                side = ("n" if y == y0 else "s" if y == y1 else "") + ("w" if x == x0 else "e" if x == x1 else "")
                A.cell(x, y, f"edge_{side}" if side else f"water_{x % 2}_{y % 2}", True, "water")
    # the causeway up the middle
    for y in range(6, H - 1):
        A.cell(8, y, "cause_l", False, "causeway")
        A.cell(9, y, "cause_m" if y % 4 == 2 else "cause_x" if "cause_x" in A.cat else f"floor_{9 % 2}_{y % 2}",
               False, "causeway")
        A.cell(10, y, "cause_m" if y % 4 == 0 else f"floor_{10 % 2}_{y % 2}", False, "causeway")
        A.cell(11, y, f"floor_{11 % 2}_{y % 2}", False, "causeway")
        A.cell(12, y, "cause_r", False, "causeway")
    # coral columns out of the water, the trireme and the dolphin
    for y in (10, 20):
        A.piece("coral_column", 6, y - 2)
        A.piece("coral_column", 14, y - 2)
    A.piece("coral_column", 3, 14)
    A.piece("trireme", 13, 13)
    A.piece("dolphin", 4, 11)
    for (x, y) in ((1, 22), (19, 22), (2, 23), (18, 23)):
        A.piece("amphora" if (x + y) % 2 else "anchor", x, y)
    g.person("THEMISTOKLES", "SAILOR", 10, 4, "Themistokles", facing="DOWN")
    g.warp(10, H - 1, "Olympus_SeatOfAres", 1)
    g.trigger(4, 2, "ExitGate")
    g.save([A.id("void") | 0x400] * 4, seat_fields())
    g.check((10, H - 2), [("themistokles", (10, 5)), ("gate", (4, 3))])
    SWAPS["Poseidon"] = dict(
        close=[(10, H - 1, A.id("mat_shut"), True)],
        open=[(4, 1, A.id("door_open1"), True), (4, 2, A.id("door_open2"), False)],
        lit=[], walk_in=(10, H - 1), seat=(10, 4))
    save_swaps("Poseidon")
    return g, [("entrance", 10, H - 4), ("basin", 10, 14), ("dais", 10, 5)]


# ---------------------------------------------------------------------------
# The seat of Athena
# ---------------------------------------------------------------------------

def seat_of_athena():
    W, H = 19, 26
    A = Hall("Olympus_SeatOfAthena", "seat_athena", W, H)
    g = A.g
    for y in range(H):
        for x in range(W):
            A.cell(x, y, f"floor_{x % 2}_{y % 2}", False, "floor")
    for x in range(1, W - 1):
        A.cell(x, 0, f"wall0_{x % 2}", True)
        A.cell(x, 1, "wall1_lamp" if x % 4 == 1 else "wall1_owl" if x in (3, 15) else f"wall1_{x % 2}", True)
        A.cell(x, 2, f"wall2_{x % 2}", True)
    for y in range(0, H - 1):
        A.cell(0, y, "side_w", True)
        A.cell(W - 1, y, "side_e", True)
    for x in range(W):
        A.cell(x, H - 1, "void", True)
    A.cell(9, H - 1, "mat", False, "mat")
    for x in range(3, 16):
        part = "l" if x == 3 else "r" if x == 15 else "m"
        A.cell(x, 3, f"dais_{part}", False, "dais")
        A.cell(x, 4, f"dais_{part}", False, "dais")
        A.cell(x, 5, "steps" if 8 <= x <= 10 else f"riser_{part}", not (8 <= x <= 10), "dais")
    for x in (1, 2, 16, 17):
        A.cell(x, 3, f"shade_{x % 2}_1", False)
    A.piece("olive", 8, 0)
    A.cell(15, 1, "door_shut1", True)
    A.cell(15, 2, "door_shut2", True)
    # the rostrum's lamps either side of the philosopher
    lamps = [(5, 3), (12, 3)]
    for x, y in lamps:
        A.piece("lamp_dim", x, y)
    # the aisle: olive bands, the owl roundel at its middle
    for y in range(6, H - 1):
        A.cell(8, y, "runner_l", False, "aisle")
        A.cell(10, y, "runner_r", False, "aisle")
    for x in list(range(1, 8)) + list(range(11, 18)):
        A.cell(x, 6, f"shade_{x % 2}_0", False)
    A.piece("roundel", 8, 13)
    # lampstands down the aisle; owls on their pedestals behind them
    for y in (9, 13, 17, 21):
        for x in (6, 12):
            A.piece("lamp_dim", x, y)
            lamps.append((x, y))
    for y in (10, 19):
        for x in (4, 14):
            A.piece("owl", x, y)
    for x in (6, 12):
        A.piece("owl", x, 6)
    # the library along the walls
    for y in (7, 11, 15, 19):
        A.piece("scroll_case", 1, y)
        A.piece("scroll_case", 16, y)
    A.piece("table", 3, 14)
    A.piece("table", 14, 14)
    for (x, y) in ((3, 8), (15, 8), (3, 22), (15, 22), (1, 23), (17, 23)):
        A.piece("basket", x, y)
    g.person("HYPATIA", "AUGUR", 9, 4, "Hypatia", facing="DOWN")
    g.warp(9, H - 1, "Olympus_SeatOfPoseidon", 0)
    g.trigger(15, 2, "ExitGate")
    g.save([A.id("void") | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("hypatia", (9, 5)), ("gate", (15, 3))])
    ids = A.ids("lamp_lit")
    SWAPS["Athena"] = dict(
        close=[(9, H - 1, A.id("mat_shut"), True)],
        open=[(15, 1, A.id("door_open1"), True), (15, 2, A.id("door_open2"), False)],
        lit=[(x, y + dy, ids[dy][0], True) for (x, y) in lamps for dy in range(2)],
        walk_in=(9, H - 1), seat=(9, 4))
    save_swaps("Athena")
    return g, [("entrance", 9, H - 4), ("hall", 9, 14), ("rostrum", 9, 5)]


# ---------------------------------------------------------------------------
# The seat of Hera
# ---------------------------------------------------------------------------

def seat_of_hera():
    W, H = 19, 28
    A = Hall("Olympus_SeatOfHera", "seat_hera", W, H)
    g = A.g
    for y in range(H):
        for x in range(W):
            A.cell(x, y, f"floor_{x % 2}_{y % 2}", False, "floor")
    for x in range(1, W - 1):
        A.cell(x, 0, f"wall0_{x % 2}", True)
        A.cell(x, 1, "wall1_feather" if x % 3 == 0 else f"wall1_{x % 2}", True)
        A.cell(x, 2, f"wall2_{x % 2}", True)
    for y in range(0, H - 1):
        A.cell(0, y, "side_w", True)
        A.cell(W - 1, y, "side_e", True)
    for x in range(W):
        A.cell(x, H - 1, "void", True)
    A.cell(9, H - 1, "mat", False, "mat")
    for x in range(2, 17):
        part = "l" if x == 2 else "r" if x == 16 else "m"
        A.cell(x, 3, f"dais_{part}", False, "dais")
        A.cell(x, 4, f"dais_{part}", False, "dais")
        A.cell(x, 5, "steps" if 8 <= x <= 10 else f"riser_{part}", not (8 <= x <= 10), "dais")
    A.cell(1, 3, "shade_1_1", False)
    A.cell(17, 3, "shade_1_1", False)
    A.piece("throne", 6, 0)
    A.cell(3, 1, "door_shut1", True)
    A.cell(3, 2, "door_shut2", True)
    for x in (6, 12):
        A.piece("brazier_cold", x, 3)
    for x in (4, 14):
        A.piece("serpent", x, 3)
    for y in range(6, H - 1):
        A.cell(8, y, "runner_l", False, "runner")
        A.cell(9, y, "runner_eye" if y % 4 == 3 else "runner_m", False, "runner")
        A.cell(10, y, "runner_r", False, "runner")
    for x in list(range(1, 8)) + list(range(11, 18)):
        A.cell(x, 6, f"shade_{x % 2}_0", False)
    for y in (7, 12, 17, 22):
        for x in (5, 13):
            A.piece("pcolumn", x, y)
    torch_rows = (24, 19, 14, 9)
    for y in torch_rows:
        for x in (7, 11):
            A.piece("torch_cold", x, y)
    for (x, y) in ((1, 9), (17, 9), (1, 19), (17, 19), (2, 14), (16, 14), (1, 24), (17, 24)):
        A.piece("urn", x, y)
    g.person("OLYMPIAS", "PRIESTESS", 9, 4, "Olympias", facing="DOWN")
    g.warp(9, H - 1, "Olympus_SeatOfAthena", 0)
    g.warp(3, 2, "Olympus_Summit", 0)
    g.save([A.id("void") | 0x400] * 4, seat_fields())
    g.check((9, H - 2), [("olympias", (9, 5)), ("door front", (3, 3))])
    t = A.ids("torch_lit")
    b = A.ids("brazier_lit")
    SWAPS["Hera"] = dict(
        close=[(9, H - 1, A.id("mat_shut"), True)],
        open=[(3, 1, A.id("door_open1"), True), (3, 2, A.id("door_open2"), False)],
        torches=[[(x, y + dy, t[dy][0], True) for x in (7, 11) for dy in range(2)] for y in torch_rows],
        braziers=[(x, 3 + dy, b[dy][0], True) for x in (6, 12) for dy in range(2)],
        walk_in=(9, H - 1), seat=(9, 4))
    SWAPS["Hera"]["lit"] = [c for row in SWAPS["Hera"]["torches"] for c in row] + SWAPS["Hera"]["braziers"]
    save_swaps("Hera")
    return g, [("entrance", 9, H - 4), ("hall", 9, 14), ("throne", 9, 5)]


BUILDERS = {"Ares": seat_of_ares, "Poseidon": seat_of_poseidon, "Athena": seat_of_athena, "Hera": seat_of_hera}
