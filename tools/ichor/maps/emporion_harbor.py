#!/usr/bin/env python3
"""Build Emporion's harbor district, MAP_EMPORION_HARBOR (aethos + isthmos).

Writes data/layouts/EmporionHarbor/map.bin and border.bin (48x26), then checks
data/maps/EmporionHarbor/map.json against the blockdata, as emporion.py does
for the city. The harbor joins the city on its north seam: the harbor road at
x = 21..25 (MAP_EMPORION_CITY's south seam), offset 0. Rows 0-5 here and the
city's rows 40-45 use aethos metatiles only (MAP_DESIGN.md §5).

Isthmos metatiles come from build/isthmos/catalog.json (TILES_isthmos.md). Make
it with /usr/bin/python3 tools/ichor/art/emporion_build.py isthmos --no-compile

Usage: /usr/bin/python3 tools/ichor/maps/emporion_harbor.py [--render DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion as E  # noqa: E402
from emporion import (  # noqa: E402
    BOULDER, HERM, SEA, STELE, Grid, Plan, check_map, paint, render, set_layout_size, walkable,
    write_layout,
)

W, H = 48, 26
LAYOUT = "LAYOUT_EMPORION_HARBOR"
NAME = "EmporionHarbor"
ROAD = range(21, 26)       # the harbor road, on the north seam (the city's main street)
SEAM_ROWS = 6

# The Euploia's berth: the player steps off her gangplank here (beat 11, the ferry).
ARRIVAL = (30, 16)
HERM_AT = (30, 13)         # the quay herm, an altar of Hermes (Kerykos's rites tutorial)
PLANTER_AT = (31, 13)      # the planter beside it: the fixed dig (the Arachne sherd)


# ---------------------------------------------------------------------------
# the plan
# ---------------------------------------------------------------------------
#
# The harbor road comes down from the city between olive gardens (an aethos band)
# into the harbor forum, a marble square with the fish market. Below it the quay
# runs the width of the harbor: warehouses and the Titans' hiring hall to the
# west, the ship sheds on their beach below them, the crane and the merchantmen
# at the south berths, the Euploia's berth by the quay herm, and the mole, the
# harbor wall, running out east with the augur at its end.

def harbor_plan():
    P = Plan(W, H)
    # the band: the road down from the city; the coast shows to the east
    P.fill(ROAD.start, 0, ROAD.stop - 1, 5, "p")
    P.fill(39, 2, 47, 5, "s")
    P.fill(41, 3, 47, 5, "~")
    P.fill(44, 2, 47, 2, "~")
    # the harbor: the yards, the forum, the quay, the water
    P.fill(0, 6, 41, 16, "q")
    P.fill(17, 6, 29, 9, "f")                     # the harbor forum
    P.fill(38, 6, 47, H - 1, "~")                 # the east water
    P.fill(0, 14, 14, 16, "s")                    # the ship sheds' beach
    P.fill(0, 17, 14, H - 1, "~")                 # their basin
    P.fill(15, 17, 41, H - 1, "~")                # the south basin
    P.fill(38, 10, 41, 11, "q")                   # the root of the mole
    P.fill(42, 10, 44, 23, "q")                   # the mole, the harbor wall
    P.fill(43, 24, 43, 24, "q")
    # the herm's bed at the head of the quay
    P.fill(29, 12, 32, 13, "g")
    P.fill(PLANTER_AT[0], PLANTER_AT[1], PLANTER_AT[0], PLANTER_AT[1], "t")
    # Isthmian Poseidon's little sanctuary at the root of the mole
    P.fill(34, 12, 37, 14, "g")
    return P


def compose_harbor():
    g = Grid(W, H, "isthmos")
    plan = harbor_plan()
    paint(g, plan)

    # ---- the band: olive gardens either side of the harbor road ----------------
    g.wall_we(2, 19, 4)
    g.wall_we(27, 36, 4)
    g.trees(pines=((3, 0), (31, 0), (14, 2)),
            olives=((0, 0), (6, 1), (10, 0), (17, 1), (27, 1), (34, 0), (36, 2), (0, 2)),
            cypresses=((20, 0), (26, 0), (20, 2), (26, 2), (13, 0)))
    g.set(20, 4, STELE, True)                          # the harbor road's sign
    for (x, y) in ((9, 3), (37, 3)):
        if g.free(x, y):
            g.set(x, y, BOULDER, True)

    # ---- the warehouses and the hiring hall (west) ------------------------------
    def warehouse(x, y, front):
        for i, part in enumerate(["W"] + ["run"] * (len(front) - 2) + ["E"]):
            g.part("roof", part, x + i, y)
            g.part("roof", "eaves_" + part if part != "run" else "eaves_run", x + i, y + 1)
            g.bldg[y, x + i] = g.bldg[y + 1, x + i] = True
        for i, col in enumerate(front):
            g.put("warehouse", x + i, y + 2, cx=col, w=1, bldg=True)
    warehouse(2, 6, [0, 1, 2, 3, 4, 5])               # the hiring hall: cart-doors (4,8), (5,8)
    warehouse(9, 6, [0, 1, 1, 1, 1, 5])               # a bonded store, shut on the quay side
    g.put("harbor_goods", 2, 9, cx=2, w=2)             # crates of shovels and bronze helmets
    g.put("harbor_goods", 7, 9, cx=0, w=2)
    g.put("harbor_goods", 10, 9, cx=0, w=2)            # amphorae stacked like firewood
    g.put("harbor_goods", 13, 9, cx=0, w=2)

    # ---- the ship sheds on their beach, the shipwright's yard beside them -------
    g.put("shed_end_w", 1, 11, bldg=True)
    for x in range(2, 14, 2):
        g.put("shed_bay", x, 11, bldg=True)
    g.put("shed_end_e", 14, 11, bldg=True)
    g.put("hull_stocks", 15, 11)                       # a hull half built, on the stocks
    g.put("timber", 18, 12)

    # ---- the forum: the fish market and the wine-seller --------------------------
    g.put("stall_wine", 18, 7)
    g.put("stall_fish", 26, 7)                         # Glykera's
    g.put("harbor_goods", 28, 9, cx=0, w=2)

    # ---- the quay: the customs post, the crane, the berths -----------------------
    g.put("harbor_goods", 22, 13, cx=0, w=4)           # off-loaded goods at the customs post
    g.put("crane", 19, 14)
    g.put("ship", 15, 17)                              # a merchantman from Tyre
    g.put("ship", 32, 18)                              # and one from Massalia
    for x in (17, 22, 27, 34, 37):
        g.put("bollards", x, 16, cx=0, w=1)
    g.put("steps", 24, 16, cy=1, w=3, h=1)             # landing steps down to the water
    g.put("harbor_goods", 34, 10, cx=0, w=4)
    # Poseidon's sanctuary: his altar and a victor's pine crown from his Isthmian
    # games, where sailors pray before they sail
    g.put("altar_poseidon", 35, 12)
    g.put("wreath_post", 37, 12)
    g.set(34, 12, E.CYPRESS_TOP, True)
    g.set(34, 13, E.CYPRESS_BOT, True)
    g.flowers([(34, 14), (35, 14), (37, 14)])
    # the herm at the head of the quay, its planter, the city's sign
    g.set(HERM_AT[0], HERM_AT[1], HERM, True)
    g.set(29, 13, STELE, True)                         # EMPORION CITY
    g.set(32, 12, E.CYPRESS_TOP, True)
    g.set(32, 13, E.CYPRESS_BOT, True)
    g.flowers([(29, 12), (30, 12), (31, 12)])
    g.solid[PLANTER_AT[1], PLANTER_AT[0]] = True       # a raised bed: dug from the quay, not walked on

    # ---- the mole ---------------------------------------------------------------
    g.put("bollards", 44, 14, cx=0, w=1)
    g.put("bollards", 42, 20, cx=0, w=1)
    g.close_edge(0, ROAD)
    return g


def border_harbor():
    return [SEA, SEA, SEA, SEA]


SCREENS = {
    "1_road": (23, 3), "2_forum": (23, 8), "3_arrival": (30, 14), "4_customs": (21, 12),
    "5_warehouses": (7, 9), "6_sheds": (8, 13), "7_mole": (40, 12), "8_augur": (43, 20),
}

# Beat 11: who walks where on the quay. The checks keep these cells open.
SCRIPTED_PATHS = {
    # Kleon sprints from (31,16) east along the berth and up the quay, out of sight
    "Kleon": [(32, 16), (33, 16)] + [(33, y) for y in range(8, 16)],
    # Kerykos hops off his bollard at (34,16), walks to the player and up to the
    # herm beside them; then away east and up the quay
    "Kerykos": [(34, 15), (33, 15), (32, 15), (31, 15), (31, 16), (31, 14), (32, 14), (33, 14)]
               + [(33, y) for y in range(6, 14)],
    # the player, walked up to the herm, then a step east to the planter
    "Player": [(30, 16), (30, 15), (30, 14), (31, 14)],
    # Alethea follows; then down a row, east, and up the quay toward the Deigma
    "Alethea": [(29, y) for y in range(14, 17)] + [(x, 15) for x in range(29, 34)]
               + [(33, y) for y in range(6, 15)],
}


def check_harbor():
    errors, reach, blocks = check_map(
        NAME, "isthmos", start=(23, 0),
        seams=(("rows", range(0, SEAM_ROWS), "city (north)"),),
        scripted=SCRIPTED_PATHS)
    for x in range(W):
        top = walkable(blocks, x, 0)
        if top != (x in ROAD):
            errors.append(f"{NAME}: north seam column {x} is {'open' if top else 'closed'}")
    if ARRIVAL not in reach:
        errors.append(f"{NAME}: the arrival tile {ARRIVAL} is not reachable")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args()
    if args.plan:
        print(harbor_plan().dump())
    g = compose_harbor()
    set_layout_size(LAYOUT, W, H)
    write_layout(g, NAME, border_harbor())
    if args.render:
        render(LAYOUT, NAME, W, H, "isthmos", args.render, "emporion_harbor", SCREENS)
    if not args.no_check:
        errors = check_harbor()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("emporion_harbor: layout written, checks pass")


if __name__ == "__main__":
    main()
