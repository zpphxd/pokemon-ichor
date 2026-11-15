#!/usr/bin/env python3
"""Build Salmydessos, MAP_SALMYDESSOS (aethos + pontos): Phineus's village, 28 x 24.

A Thracian fishing village on a bay off the Bosporus's west shore. Wattle and
thatch, oak woods behind, a beach where the wrecks wash up. Phineus's house
stands over the village green, its roof still raked from the Harpies, his table
set outside; the bird-catcher keeps his dovecote next door. A stone jetty runs
out into the bay with the Euploia moored at its end.

The beach's boundary stones are the village's own history: the people of
Salmydessos lived off ships wrecked on their coast, and set up stones along the
shore so every family knew which stretch's wreckage was theirs (Xenophon,
Anabasis 7.5.12-13).

Doors (BUILD.md §5): warp 0 Phineus's house, 1 the bird-catcher's.
Connections: down MAP_BOSPORUS offset 0 (the bay's water x 14-22, the shore path
x 0-7); right MAP_PONTIC_COAST offset -20 (cliffs and woods on both sides).
Wings landing tile: (5, 7), in front of Phineus's door.

Usage: /usr/bin/python3 tools/ichor/maps/salmydessos.py [--render DIR] [--shapes] [--plan]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pontos_map as M  # noqa: E402
from pontos_map import Grid, hidden, item_ball, obj, sign, warp  # noqa: E402

W, H = 28, 24
NAME, LAYOUT = "Salmydessos", "LAYOUT_SALMYDESSOS"
LANDING = (5, 7)
PHINEUS_DOOR = (5, 6)
CATCHER_DOOR = (10, 5)
GANGPLANK = (17, 17)        # the mole cell under the Euploia's gangplank: Nausikles


def plan():
    g = [["%"] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch

    # the village's clearing in the oak woods
    fill(1, 2, 22, 10, ".")
    fill(2, 1, 8, 1, ".")
    fill(2, 11, 9, 22, ".")
    fill(1, 23, 7, 23, ".")
    # the bay: from the south edge (the Bosporus) up to the village's beach
    fill(14, 11, 22, H - 1, "~")
    # the beach: along the bay's head and down its west side, where the wrecks come in
    fill(13, 9, 22, 10, "s")
    fill(10, 11, 13, 21, "s")
    # the little stone mole off the beach, the Euploia moored on its north side
    fill(14, 17, 20, 18, "q")
    # the headland east of the bay, and the cliff west of the bay's mouth
    fill(23, 6, W - 1, H - 1, "c")
    fill(12, 22, 13, H - 1, "c")
    fill(8, 22, 11, H - 1, "%")
    # the path: from the shore path south-west (the Bosporus's beach) to the green
    for (x, y) in [(3, y) for y in range(12, 24)] + [(x, 11) for x in range(3, 9)] + \
                  [(8, y) for y in range(7, 11)] + [(x, 7) for x in range(4, 14)] + \
                  [(13, 8)]:
        g[y][x] = "p"
    # the woods: wherever the land is a cell from anything open
    out = [list(r) for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == "c" and all(g[yy][xx] not in "~bR" for yy in range(max(0, y - 2), min(H, y + 3))
                                      for xx in range(max(0, x - 2), min(W, x + 3))):
                out[y][x] = "%"
    return ["".join(r) for r in out]


S_ = "Salmydessos_EventScript_"
I = "OBJ_EVENT_GFX_ICHOR_"

EVENTS = {
    "object_events": [
        # ICHOR_STUB_SHIP: the Euploia's helmsman at the gangplank; world-postgame's
        # mooring (EventScript_IchorBoardShip) replaces him.
        obj(I + "SAILOR", GANGPLANK[0], GANGPLANK[1], "Oik_EventScript_SailHome", "MOVEMENT_TYPE_FACE_DOWN",
            local_id="LOCALID_SALMYDESSOS_NAUSIKLES"),
        obj(I + "FISHER", 20, 13, S_ + "Fisher", "MOVEMENT_TYPE_FACE_DOWN"),
        obj(I + "WOMAN", 9, 15, S_ + "StoneWoman", "MOVEMENT_TYPE_FACE_RIGHT"),
        obj(I + "ELDER_M", 9, 7, S_ + "Elder", "MOVEMENT_TYPE_FACE_LEFT"),
        obj(I + "KID_F", 14, 5, S_ + "Kid", "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1),
        obj(I + "YOUTH_M", 19, 6, S_ + "Youth", "MOVEMENT_TYPE_FACE_DOWN"),
        obj("OBJ_EVENT_GFX_SPECIES(PIDOVE)", 13, 3, S_ + "Dove", "MOVEMENT_TYPE_FACE_LEFT"),
        item_ball(20, 2, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_ITEM_SALMYDESSOS_PRETTY_FEATHER"),
    ],
    "warp_events": [
        warp(PHINEUS_DOOR[0], PHINEUS_DOOR[1], "MAP_SALMYDESSOS_PHINEUSS_HOUSE", 0),
        warp(CATCHER_DOOR[0], CATCHER_DOOR[1], "MAP_SALMYDESSOS_BIRD_CATCHERS_HOUSE", 0),
    ],
    "coord_events": [],
    "bg_events": [
        sign(4, 21, S_ + "SignSouth"),
        sign(16, 8, S_ + "SignQuay"),
        sign(7, 7, S_ + "Table"),
        sign(12, 14, S_ + "Horos"),
        sign(12, 19, S_ + "Horos"),
        hidden(10, 19, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_SALMYDESSOS_STARDUST"),
        hidden(1, 3, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_SALMYDESSOS_HEART_SCALE"),
    ],
}


def compose(shapes_only=False):
    g = Grid(NAME, plan(), shapes_only=shapes_only)
    g.paint()
    if shapes_only:
        return g
    # Phineus's house: the Harpies' claw marks still in the thatch; his table outside
    g.house(3, 4, ["roof_w", "roof_claws", "roof_run", "roof_e"],
            ["daub_w", "daub_window", "daub_door", "daub_e"])
    g.put("table", 6, 7)
    # the bird-catcher's: cages by the door, his dovecote beside the house
    g.house(9, 3, ["roof_w", "roof_run", "roof_e"], ["daub_w", "daub_door", "daub_e"])
    g.put("dovecote", 12, 3)
    g.put("cages", 8, 5)
    # the waterfront: nets drying, the fishers' pier and boat, the Euploia
    g.put("nets", 4, 9)
    g.put("pier_root", 20, 11)
    g.put("pier_run", 20, 12)
    g.put("pier_tip", 20, 13)
    g.put("boat", 15, 21)
    g.put("ship", 16, 15)
    # the beach: a wreck's ribs and the boundary stones dividing the shore
    g.put("wreck", 10, 16)
    g.put("horos", 12, 14)
    g.put("horos", 12, 19)
    g.put("horos", 11, 12)
    # the green: a stele at the waterfront, one at the shore path
    g.set(16, 8, M.STELE, True)
    g.set(4, 21, M.STELE, True)
    g.woods(salt=3)
    g.trees(oaks=((1, 4), (20, 3)), hazels=((17, 3), (21, 6), (2, 8), (7, 14), (1, 13)),
            cypresses=((6, 15), (0, 18)))
    g.flowers([(2, 2), (6, 2), (18, 7), (11, 9), (1, 10), (5, 13), (6, 19), (16, 4), (20, 8)])
    return g


def border(g):
    return [M.GRASS, M.GRASS, M.GRASS, M.GRASS]


SCREENS = {"1_shore_path": (3, 18), "2_green": (8, 7), "3_phineus": (5, 7), "4_beach_head": (17, 10),
           "5_mole": (17, 17), "6_beach": (11, 16)}


def connections():
    return [{"map": "MAP_BOSPORUS", "offset": 0, "direction": "down"},
            {"map": "MAP_PONTIC_COAST", "offset": -20, "direction": "right"}]


def check():
    starts = [(x, H - 1) for x in range(0, 8)] + [(x, H - 1) for x in range(14, 23)]
    errors, r, blocks = M.check_map(NAME, starts)
    for need, what in ((LANDING, "the Wings' landing tile"), (GANGPLANK, "Nausikles's gangplank tile")):
        if M.cell_kind(blocks, *need) != "land":
            errors.append(f"{NAME}: {what} {need} is not open land")
    errors += M.check_seam(NAME, "Bosporus", "down", 0)
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
    M.write_events(NAME, dict(EVENTS, connections=connections()), music="MUS_ICHOR_AKTI",
                   weather="WEATHER_SHADE", map_type="MAP_TYPE_TOWN")
    if args.render:
        M.render(LAYOUT, NAME, args.render, "salmydessos", SCREENS)
    errors = check()
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(1)
    print("salmydessos: layout written, checks pass")


if __name__ == "__main__":
    main()
