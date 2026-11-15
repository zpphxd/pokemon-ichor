#!/usr/bin/env python3
"""Build Aia, MAP_AIA (aethos + pontos): King Aietes's city in Colchis, 44 x 36.

Up the Phasis from the sea, the city of the sun's son:
  - The harbor is the river's mouth, open to the Pontic Coast on the west edge
    (rows 18-26). A stone quay runs down its east bank, with a mole where the
    Euploia lies moored and Nausikles waits at her gangplank (ICHOR_STUB_SHIP).
  - The Asclepeion and the Agora face the harbor plaza, the first things you see
    stepping ashore. The ram post, Aia's waystone, stands in the plaza: the ram
    that carried Phrixos here (ICHOR_STUB_HERM).
  - Colchian houses are log towers (Vitruvius 2.1.4): whole trees laid flat and
    crossed at the corners. Phrixos's sons live in one under a carved ram; the
    linen-weaver in another, her cloth drying on poles (Colchians wove linen like
    the Egyptians, Herodotus 2.105).
  - The crown: Aietes's bronze palace at the top of the main street, and before
    it the court of Hephaestus's four fountains, of milk, wine, oil and water,
    under vines (Argonautica 3.215-227). The palace door is a hall (batch 2): a
    guard turns you away (ICHOR_STUB_HALL). The palace workshop beside it opens.
  - The Phasis's reeds, where the pheasants live, fringe the harbor's south bank.
  - The main street runs on east out of the city gate to the Phasis road (batch 2,
    left open: no connection yet).

Doors (BUILD.md §5): warp 0 the Asclepeion, 1 the Agora, 2 Phrixos's sons' house,
3 the linen-weaver's, 4 the palace workshop.
Connection: left MAP_PONTIC_COAST offset -4.
Wings landing tile: (18, 15), before the Asclepeion's door.

Usage: /usr/bin/python3 tools/ichor/maps/aia.py [--render DIR] [--shapes] [--plan]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pontos_map as M  # noqa: E402
from pontos_map import Grid, hidden, item_ball, obj, sign, warp  # noqa: E402

W, H = 44, 36
NAME, LAYOUT = "Aia", "LAYOUT_AIA"
HARBOR_ROWS = range(18, 27)       # open to the Pontic Coast on the west edge
EAST_GATE = range(18, 20)         # the Phasis road, left open on the east edge (batch 2)
LANDING = (18, 15)
DOORS = [((18, 14), "MAP_AIA_ASCLEPEION"), ((22, 14), "MAP_AIA_AGORA"),
         ((25, 5), "MAP_AIA_PHRIXOS_SONS_HOUSE"), ((30, 17), "MAP_AIA_LINEN_WEAVERS_HOUSE"),
         ((41, 3), "MAP_AIA_PALACE_WORKSHOP")]
GANGPLANK = (10, 24)
PALACE_DOOR = (34, 5)            # its doors are x 34-35; the steps below them are row 6


def plan():
    g = [["."] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch

    # the Colchian shore north of the harbor, and its woods
    fill(0, 0, 13, 16, "c")
    fill(14, 0, 15, 10, "c")
    # the harbor, the Phasis's mouth
    fill(0, 17, 13, 26, "~")
    # the south bank: the reed beds, the woods behind
    fill(0, 27, 15, H - 1, "c")
    # the quay down the harbor's east bank, and the mole for the Euploia
    fill(14, 14, 15, 28, "q")
    fill(8, 24, 13, 25, "q")
    # the harbor plaza and the main street east to the gate
    fill(16, 15, 24, 23, "p")
    fill(16, 18, W - 1, 19, "p")
    fill(25, 15, 27, 23, "p")
    # the palace court: paved, the four fountains in it
    fill(28, 6, 41, 13, "q")
    fill(33, 14, 36, 17, "p")
    # lanes: to Phrixos's sons, to the linen-weaver
    fill(25, 6, 25, 14, "p")
    # the woods round the city
    fill(0, 0, 13, 13, "%")
    fill(14, 0, 22, 1, "%")
    fill(0, 31, 43, H - 1, "%")
    fill(16, 32, 24, 34, "%")
    fill(40, 22, W - 1, 30, "%")
    fill(42, 0, W - 1, 15, "%")
    # keep the cliff edge (two cells from the water) as open chalk
    for y in range(H):
        for x in range(W):
            if g[y][x] == "%" and any(g[yy][xx] in "~" for yy in range(max(0, y - 2), min(H, y + 3))
                                      for xx in range(max(0, x - 2), min(W, x + 3))):
                g[y][x] = "c"
    return ["".join(r) for r in g]


A = "Aia_EventScript_"
I = "OBJ_EVENT_GFX_ICHOR_"

EVENTS = {
    "object_events": [
        # ICHOR_STUB_SHIP: the Euploia's helmsman at her gangplank; world-postgame's
        # mooring (EventScript_IchorBoardShip) replaces him.
        obj(I + "SAILOR", GANGPLANK[0], GANGPLANK[1], "Oik_EventScript_SailHome", "MOVEMENT_TYPE_FACE_UP",
            local_id="LOCALID_AIA_NAUSIKLES"),
        # ICHOR_STUB_HALL: the palace guard, until batch 2's hall opens the doors
        obj(I + "HOPLITE", 34, 6, A + "PalaceGuard", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_AIA_GUARD"),
        obj(I + "FISHER", 15, 22, A + "Fisher", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(I + "MAN", 20, 20, A + "Porter", "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1),
        obj(I + "WOMAN", 31, 21, A + "Linen", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(I + "PRIESTESS", 38, 12, A + "Maid", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(I + "ELDER_M", 40, 8, A + "Smith", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(I + "KID_M", 33, 15, A + "Kid", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
        obj(I + "YOUTH_M", 26, 8, A + "Phrontis", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(I + "MERCHANT", 39, 19, A + "GateKeeper", "MOVEMENT_TYPE_FACE_LEFT"),
        obj("OBJ_EVENT_GFX_SPECIES(UNFEZANT)", 6, 29, A + "Pheasant", "MOVEMENT_TYPE_FACE_RIGHT"),
        obj("OBJ_EVENT_GFX_SPECIES(UNFEZANT)", 11, 30, A + "Pheasant", "MOVEMENT_TYPE_FACE_LEFT"),
        item_ball(2, 15, "ITEM_HEAT_ROCK", "FLAG_ICHOR_ITEM_AIA_HEAT_ROCK"),
    ],
    "warp_events": [warp(x, y, dest, 0) for (x, y), dest in DOORS],
    "coord_events": [],
    "bg_events": [
        sign(16, 17, A + "SignHarbor"),
        sign(22, 21, A + "RamPost"),            # ICHOR_STUB_HERM
        sign(33, 7, A + "SignPalace"),
        sign(29, 10, A + "FountainMilk"),
        sign(32, 10, A + "FountainWine"),
        sign(37, 10, A + "FountainOil"),
        sign(40, 10, A + "FountainWater"),
        sign(41, 17, A + "SignGate"),
        sign(8, 28, A + "Reeds"),
        hidden(29, 7, "ITEM_GOLD_BAR", "FLAG_ICHOR_HIDDEN_AIA_GOLD_BAR"),
        hidden(14, 29, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_HIDDEN_AIA_MIRACLE_SEED"),
    ],
}


def compose(shapes_only=False):
    g = Grid(NAME, plan(), shapes_only=shapes_only)
    g.paint()
    if shapes_only:
        return g
    # the Asclepeion and the Agora, facing the harbor plaza
    g.block(M.ASCLEPEION, 17, 11)
    g.block(M.AGORA, 21, 11)
    for (x, y) in ((18, 14), (22, 14)):
        g.solid[y, x] = False
    # Aietes's palace, the crown, and the fountains' court before it
    g.put("palace", 31, 1)
    for i, (liq, x) in enumerate((("milk", 29), ("wine", 32), ("oil", 36), ("water", 39))):
        g.put(f"fountain_{liq}", x, 9)
    for x in (31, 35, 38):
        g.put("vine_post", x, 9)
    # the palace workshop beside it
    g.house(40, 1, ["roof_w", "roof_run", "roof_e"], ["log_w", "log_door", "log_e"])
    # Phrixos's sons' log tower, the carved ram over its door
    g.house(24, 2, ["roof_w", "roof_run", "roof_e"], ["log_w", "log_door_ram", "log_e"],
            upper=["log_up_w", "log_up_window", "log_up_e"])
    # the linen-weaver's, her linen out on its poles
    g.house(29, 15, ["roof_w", "roof_run", "roof_run", "roof_e"], ["log_w", "log_door", "log_window", "log_e"])
    g.put("nets", 29, 21)
    # the harbor: the Euploia at the mole, a fishing boat, the ram post
    g.put("ship", 9, 22)
    g.put("boat", 3, 21)
    g.put("ram_post", 22, 21)
    # the reed beds along the harbor's south bank
    for x in range(0, 13):
        if g.plan[27][x] == "c" and x not in (8,):
            g.put("reeds", x, 27)
    for x in (2, 4, 6):
        g.put("reeds_water", x, 26)
    # signs and the gate's posts
    g.set(16, 17, M.STELE, True)
    g.set(33, 7, M.STELE, True)
    g.set(41, 17, M.STELE, True)
    g.set(8, 28, M.STELE, True)
    g.put("ram_post", 42, 16)
    g.put("ram_post", 42, 20)
    g.woods(salt=7)
    g.trees(oaks=((28, 15), (37, 21), (17, 27), (33, 27), (29, 3), (22, 3), (19, 6)),
            hazels=((24, 16), (31, 16), (36, 15), (39, 24), (20, 25), (23, 28), (35, 29), (18, 2)))
    g.flowers([(26, 16), (29, 17), (32, 23), (36, 24), (19, 29), (25, 29), (30, 30), (23, 7), (21, 8)])
    return g


def border(g):
    return [M.GRASS, M.GRASS, M.GRASS, M.GRASS]


SCREENS = {"1_harbor": (10, 21), "2_quay": (15, 18), "3_plaza": (20, 17), "4_street": (28, 18),
           "5_fountains": (34, 11), "6_palace": (34, 6), "7_phrixos": (25, 7), "8_linen": (30, 19),
           "9_gate": (40, 18), "10_reeds": (7, 29)}


def connections():
    return [{"map": "MAP_PONTIC_COAST", "offset": -4, "direction": "left"}]


def check():
    starts = [(0, y) for y in HARBOR_ROWS]
    errors, r, blocks = M.check_map(NAME, starts, perched=("Pheasant",))
    for y in range(H):
        k = M.cell_kind(blocks, 0, y)
        if (k == "water") != (y in HARBOR_ROWS):
            errors.append(f"{NAME}: west seam row {y} is {k}")
    for need, what in ((LANDING, "the Wings' landing tile"), (GANGPLANK, "Nausikles's gangplank tile")):
        if M.cell_kind(blocks, *need) != "land":
            errors.append(f"{NAME}: {what} {need} is not open land")
    for y in EAST_GATE:
        if (W - 1, y) not in r:
            errors.append(f"{NAME}: the east gate's road at ({W - 1},{y}) can't be reached")
    errors += M.check_seam(NAME, "PonticCoast", "left", -4)
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
    M.write_events(NAME, dict(EVENTS, connections=connections()), music="MUS_ICHOR_EMPORION",
                   weather="WEATHER_SUNNY_CLOUDS", map_type="MAP_TYPE_CITY")
    if args.render:
        M.render(LAYOUT, NAME, args.render, "aia", SCREENS)
    errors = check()
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(1)
    print("aia: layout written, checks pass")


if __name__ == "__main__":
    main()
