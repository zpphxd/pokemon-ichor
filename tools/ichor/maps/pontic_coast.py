#!/usr/bin/env python3
"""Build the Pontic Coast, MAP_PONTIC_COAST (aethos + pontos): a sea lane, 80 x 40.

East along the Black Sea's south shore, from the Bosporus's mouth to Colchis:
  - The mouth: the Bosporus joins on the south edge (x 1-20). West of it the
    Thracian cliffs run up to Salmydessos's woods.
  - Herakleia: a hooked headland, and in the small bay inside the hook the
    Acherusian cave, where Herakles hauled Kerberos up into the light.
  - Sinope: a Milesian colony on its peninsula, a lighthouse on the point and a
    quay you can land at.
  - The whirlpool cove: three whirlpools across a cove's mouth and a jar on the
    beach inside. Triton's Conch calms them (ICHOR_STUB_RELIC).
  - Themiskyra's landing: a beach at the Thermodon's mouth. The Amazons' town is
    LABORS's (world-postgame's): until it exists, the riders wave you off
    (ICHOR_STUB_PG_LANDING). The landing tile is LANDING_THEMISKYRA.
  - The Isle of Ares offshore: the birds' isle (Argonautica 2.1030-1089), with
    its beach, its grass, the Amazons' black stone, a shield on a post, dead trees
    the birds perch in and their feathers in the turf. On a black crag north of it,
    something bigger roosts (ICHOR_STUB_LEGEND: Yveltal).
  - The north-west reach (the west edge, rows 0-15) is left open for Leuke, the
    White Isle (batch 2).
  - East: the Phasis's mouth, rows 22-30 of the east edge, into Aia's harbor.

Connections: down MAP_BOSPORUS offset -28; left MAP_SALMYDESSOS offset 16;
right MAP_AIA offset 4.

Usage: /usr/bin/python3 tools/ichor/maps/pontic_coast.py [--render DIR] [--shapes] [--plan]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pontos_map as M  # noqa: E402
from pontos_map import Grid, hidden, item_ball, obj, sign, swimmer  # noqa: E402

W, H = 80, 40
NAME, LAYOUT = "PonticCoast", "LAYOUT_PONTIC_COAST"
MOUTH = range(1, 21)              # the Bosporus's mouth on the south edge
EAST_WATER = range(22, 31)        # the Phasis mouth on the east edge, into Aia's harbor
NW_REACH = range(0, 16)           # left open on the west edge for Leuke (batch 2)
LANDING_THEMISKYRA = (65, 30)     # world-postgame's harbor will warp here
AIA_OFFSET = 4


def plan():
    g = [["~"] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch

    # the Thracian side of the mouth, up to Salmydessos's woods
    fill(0, 16, 4, 25, "c")
    fill(0, 26, 2, 36, "c")
    fill(0, 37, 0, 39, "c")
    # the Anatolian shore, east of the mouth, running east
    fill(21, 33, 79, 39, "c")
    fill(21, 30, 33, 32, "c")
    # Herakleia's hooked headland, and the little bay inside its hook
    fill(22, 22, 31, 29, "c")
    fill(24, 20, 30, 21, "c")
    fill(26, 23, 29, 25, "~")
    fill(29, 23, 31, 24, "~")
    # Sinope's peninsula, its quay on the east side
    fill(37, 26, 45, 32, "c")
    fill(38, 18, 44, 25, "c")
    fill(39, 15, 43, 17, "c")
    fill(40, 13, 42, 14, "c")
    fill(45, 21, 47, 24, "q")
    # the whirlpool cove: headlands either side, the cove, its beach
    fill(48, 26, 51, 32, "c")
    fill(57, 26, 61, 32, "c")
    fill(52, 30, 56, 32, "s")
    g[26][53] = g[26][54] = g[26][55] = "W"
    fill(52, 26, 52, 26, "c")
    fill(56, 26, 56, 26, "c")
    # Themiskyra's landing: a beach at the Thermodon's mouth
    fill(62, 29, 68, 32, "s")
    fill(63, 28, 67, 28, "s")
    # Colchis: the north shore of the Phasis's mouth, and the south shore
    fill(71, 4, 79, 20, "c")
    fill(69, 10, 70, 20, "c")
    fill(69, 33, 79, 33, "c")
    fill(72, 31, 79, 32, "c")
    # the Isle of Ares, its beach on the south, its grass
    fill(52, 6, 63, 13, "c")
    fill(54, 4, 61, 5, "c")
    fill(51, 8, 51, 12, "c")
    fill(55, 14, 60, 15, "s")
    fill(54, 7, 61, 12, ",")
    fill(56, 6, 59, 6, ",")
    # the black crag north of the isle, where the roost is
    fill(48, 1, 51, 4, "k")
    # rocks and stacks: the open sea's landmarks
    for (x, y) in ((12, 8), (13, 8), (33, 6), (66, 18), (46, 9), (20, 18), (8, 24)):
        g[y][x] = "w"
    # rough water: the current out of the Bosporus, the swell off the capes
    for (x, y) in ((10, 33), (12, 30), (9, 27), (14, 25), (32, 19), (48, 17), (70, 26), (73, 28)):
        g[y][x] = "R"
    # the woods: wherever the land is two cells from the sea
    def far(x, y):
        return all(g[yy][xx] not in "~bRrwW" for yy in range(max(0, y - 2), min(H, y + 3))
                   for xx in range(max(0, x - 2), min(W, x + 3)))
    out = [list(r) for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == "c" and far(x, y):
                out[y][x] = "%"
    # the cove's beach is reached only past the whirlpools: woods close its sides
    for y in range(29, 33):
        out[y][51] = out[y][57] = "%"
    # Sinope's lane to its lighthouse, the isle's clearing: keep them open
    for (x, y) in [(41, y) for y in range(18, 27)] + [(42, 20), (42, 22), (40, 19)]:
        out[y][x] = "c"
    for y in range(6, 14):
        for x in range(52, 64):
            if out[y][x] == "%":
                out[y][x] = "c"
    return ["".join(r) for r in out]


PC = "PonticCoast_EventScript_"
I = "OBJ_EVENT_GFX_ICHOR_"
P_ = "OBJ_EVENT_GFX_"

# ICHOR_STUB_SPRITE: the swimmers stand in for OBJ_EVENT_GFX_ICHOR_ARGONAUT (swimming).
EVENTS = {
    "object_events": [
        # the first: in plain view out of the Bosporus's mouth
        swimmer(P_ + "SWIMMER_M", 9, 30, PC + "Palaimonios", "MOVEMENT_TYPE_FACE_DOWN", 4),
        # off the Thracian cliffs, toward the north-west reach
        swimmer(P_ + "SWIMMER_F", 6, 12, PC + "Kleite", "MOVEMENT_TYPE_FACE_RIGHT", 4),
        # off Herakleia's cape
        swimmer(P_ + "SWIMMER_M", 24, 16, PC + "Ankaios", "MOVEMENT_TYPE_FACE_LEFT", 4),
        # on Sinope's quay: a trader off a Milesian ship (ICHOR_STUB_CLASS: Phoenician Trader)
        obj(I + "MERCHANT", 47, 21, PC + "Autolykos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
        # between Sinope and the isle
        swimmer(P_ + "SWIMMER_M", 48, 14, PC + "Phlogios", "MOVEMENT_TYPE_FACE_DOWN", 4),
        # on the Isle of Ares, among the perches (ICHOR_STUB_CLASS: Argonaut)
        obj(I + "HOPLITE", 58, 10, PC + "Amphidamas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
        # off the Thermodon's mouth (ICHOR_STUB_CLASS: Amazon, LABORS's class)
        swimmer(P_ + "SWIMMER_F", 64, 23, PC + "Antiope", "MOVEMENT_TYPE_FACE_DOWN", 3),
        # the last, before Colchis: a Colchian watching the strait (ICHOR_STUB_CLASS: Colchian Sorceress)
        swimmer(P_ + "SWIMMER_F", 72, 24, PC + "Asterodeia", "MOVEMENT_TYPE_FACE_LEFT", 4),
        # people
        obj(I + "FISHER", 45, 24, PC + "SinopeFisher", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(I + "ELDER_M", 41, 19, PC + "Colonist", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(I + "YOUTH_F", 65, 29, PC + "AmazonRider", "MOVEMENT_TYPE_FACE_DOWN",
            local_id="LOCALID_PONTIC_AMAZON"),
        # items: in the lee of the stacks; on the isle; the cove's jar beyond the whirlpools
        item_ball(14, 8, "ITEM_NET_BALL", "FLAG_ICHOR_ITEM_PONTIC_NET_BALL", water=True),
        item_ball(53, 12, "ITEM_SHARP_BEAK", "FLAG_ICHOR_ITEM_PONTIC_SHARP_BEAK"),
        item_ball(54, 31, "ITEM_MYSTIC_WATER", "FLAG_ICHOR_ITEM_PONTIC_MYSTIC_WATER"),
        item_ball(35, 31, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_PONTIC_ULTRA_BALL", water=True),
    ],
    "warp_events": [],
    "coord_events": [],
    "bg_events": [
        sign(12, 34, PC + "SignMouth"),          # a sea-mark out of the Bosporus
        sign(3, 4, PC + "SignReach"),            # the north-west reach (Leuke, batch 2)
        sign(27, 23, PC + "Acheron"),            # the cave in Herakleia's bay
        sign(41, 16, PC + "Lighthouse"),     # its base, read from the lane below
        sign(44, 23, PC + "SignSinope"),
        sign(54, 26, PC + "Whirlpool"),          # ICHOR_STUB_RELIC: Triton's Conch
        sign(64, 28, PC + "Themiskyra"),         # ICHOR_STUB_PG_LANDING
        sign(57, 9, PC + "AresStone"),
        sign(60, 11, PC + "ShieldPost"),
        sign(49, 5, PC + "Roost"),               # ICHOR_STUB_LEGEND: Yveltal
        sign(69, 27, PC + "SignColchis"),        # a sea-mark before Aia
        hidden(60, 6, "ITEM_RAZOR_CLAW", "FLAG_ICHOR_HIDDEN_PONTIC_RAZOR_CLAW"),
        hidden(43, 27, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_PONTIC_STAR_PIECE"),
    ],
}

MANDATORY = {}


def compose(shapes_only=False):
    g = Grid(NAME, plan(), shapes_only=shapes_only)
    g.paint()
    if shapes_only:
        return g
    # sea-marks: the lane's signs
    g.put("sea_mark", 12, 34)
    g.put("sea_mark", 3, 4)
    g.put("sea_mark", 69, 27)
    # stacks off the capes
    g.put("stack", 33, 15)
    g.put("stack", 19, 10)
    # Herakleia: the Acherusian cave in the hook's south face
    g.put("acheron", 27, 23)
    # Sinope: the lighthouse on the point, the colony's stele by its quay
    g.put("lighthouse", 41, 14)
    g.trees(hazels=((40, 15), (42, 15)))
    g.set(44, 23, M.STELE, True)
    g.block([[M.TRIPOD[0]], [M.TRIPOD[1]]], 39, 20)
    # the whirlpools are painted from the plan; the cove's beach holds the jar
    # Themiskyra's landing: a stele, the Amazons' spears planted in the sand
    g.set(64, 28, M.STELE, True)
    # the Isle of Ares
    g.put("ares_stone", 57, 8)
    g.put("shield_post", 60, 10)
    g.put("snag", 55, 5)
    g.put("snag", 62, 7)
    g.put("feathers_ground", 54, 9)
    g.put("feathers_ground", 59, 12)
    g.put("feathers_ground", 62, 10)
    g.put("roost", 49, 2)
    # the Phasis's mouth: reeds in the shallows
    for (x, y) in ((70, 21), (71, 22), (75, 30), (76, 30), (68, 21)):
        if g.plan[y][x] == "~":
            g.put("reeds_water", x, y)
    g.woods(salt=5)
    g.trees(hazels=((42, 25), (40, 27), (53, 6), (62, 12)), oaks=((43, 18),))
    g.flowers([(40, 23), (42, 27), (56, 13), (61, 9), (53, 10)])
    return g


def border(g):
    sea = g.k("psea")
    return [sea, sea, sea, sea]


SCREENS = {"1_mouth": (10, 33), "2_reach": (6, 10), "3_herakleia": (27, 25), "4_sinope": (43, 21),
           "5_cove": (54, 28), "6_themiskyra": (65, 30), "7_isle": (57, 11), "8_roost": (50, 5),
           "9_colchis": (74, 27)}


def connections():
    return [{"map": "MAP_BOSPORUS", "offset": -28, "direction": "down"},
            {"map": "MAP_SALMYDESSOS", "offset": 16, "direction": "left"},
            {"map": "MAP_AIA", "offset": AIA_OFFSET, "direction": "right"}]


def check():
    starts = [(x, H - 1) for x in MOUTH]
    errors, r, blocks = M.check_map(NAME, starts, locked={(54, 31)})
    for x in range(W):
        k = M.cell_kind(blocks, x, H - 1)
        if (k == "water") != (x in MOUTH):
            errors.append(f"{NAME}: south edge column {x} is {k}")
    for y in range(H):
        k = M.cell_kind(blocks, W - 1, y)
        if y >= AIA_OFFSET and (k == "water") != (y in EAST_WATER):
            errors.append(f"{NAME}: east edge row {y} is {k}")
        k = M.cell_kind(blocks, 0, y)
        if (k == "water") != (y in NW_REACH):
            errors.append(f"{NAME}: west edge row {y} is {k}")
    for goal, why in (([(W - 1, y) for y in EAST_WATER], "Aia"), ([LANDING_THEMISKYRA], "Themiskyra's landing"),
                      ([(57, 11)], "the Isle of Ares")):
        if not any(gl in r for gl in goal):
            errors.append(f"{NAME}: no way from the Bosporus to {why}")
    if (54, 31) in r:
        errors.append(f"{NAME}: the whirlpool cove's jar is reachable without Triton's Conch")
    errors += M.check_seam(NAME, "Bosporus", "down", -28)
    errors += M.check_seam(NAME, "Salmydessos", "left", 16)
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--shapes", action="store_true")
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args()
    if args.plan:
        print("\n".join(plan()))
        return
    if args.shapes:
        M.write_shapes(compose(shapes_only=True))
        return
    g = compose()
    M.write_layout(LAYOUT, NAME, g, border(g))
    M.write_events(NAME, dict(EVENTS, connections=connections()), music="MUS_ICHOR_TRIREME",
                   weather="WEATHER_SHADE", map_type="MAP_TYPE_OCEAN_ROUTE")
    if args.render:
        M.render(LAYOUT, NAME, args.render, "pontic_coast", SCREENS)
    errors = check()
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(1)
    print("pontic_coast: layout written, checks pass")


if __name__ == "__main__":
    main()
