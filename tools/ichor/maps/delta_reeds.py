#!/usr/bin/env python3
"""Build the Delta Reeds (aethos + kemet): the route from Naukratis south through
the papyrus to Memphis (OIKOUMENE.md §4.5; COVERAGE.md Y1, and Y2 on its water).

Papyrus taller than a man walls the way into mazes; the reeds you can walk through
are the wild Pokemon's. Herodotus says the marsh people sleep up towers, above the
gnats (2.95): two gnat-towers stand on the route, and the second family's tower is
the rest point. A canal runs down the west side with lotus and an islet; Thoth's
ibis pillar stands at the clearing; the Papyrus Shallows Nursery's gate is fenced
shut on the east edge until batch 2 opens it.

The rhythm, north to south: Naukratis's road, an easy fowler in plain view, the
first band; the open marsh and the first gnat-tower; the first narrows (Sobek's
boatman); the papyrus maze, the second band; the clearing (rest, pillar, Nursery
gate); the second narrows; the third band; the fishing pool; the last narrows
under Memphis's walls.

The builder proves the route standard: no walk from Naukratis to Memphis avoids
the three forced bands; each mandatory trainer's sight line cuts every walk past
it; every dead end has an item.

Usage: /usr/bin/python3 tools/ichor/maps/delta_reeds.py [--render DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import egypt_lib as E  # noqa: E402
from egypt_lib import Grid, Plan, hidden, item_ball, obj, sign  # noqa: E402

W, H = 32, 46
NAME, LAYOUT = "DeltaReeds", "LAYOUT_DELTA_REEDS"
NORTH_ROAD = range(14, 17)       # under Naukratis's south road (Naukratis x 16-18: offset 2)
SOUTH_ROAD = range(14, 17)       # onto Memphis's north gate
NURSERY = (31, range(23, 26))    # the fenced opening: east edge, rows 23-25
P = "OBJ_EVENT_GFX_ICHOR_"
S = "DeltaReeds_EventScript_"


def plan():
    p = Plan(W, H, "P")
    # 1. the road in from Naukratis; reeds either side of the sign
    p.fill(14, 0, 16, 0, "p")
    p.fill(12, 1, 18, 4, "g")
    p.fill(14, 1, 16, 4, "p")
    p.fill(11, 1, 11, 3, "R")
    p.fill(17, 1, 20, 2, "R")
    p.fill(19, 3, 20, 3, "R")
    p.fill(11, 4, 20, 4, "g")
    p.fill(14, 4, 16, 4, "p")
    # band 1
    p.fill(10, 5, 20, 7, "R")
    # 2. the open marsh: the first pool (lotus) west, the first gnat-tower east;
    # reeds in the middle and round the tower (the way through stays dry at x 13)
    p.fill(10, 8, 27, 13, "g")
    p.fill(2, 8, 9, 13, "m")
    p.fill(3, 9, 7, 12, "~")
    p.cells([(4, 10), (6, 11)], "w")
    p.fill(10, 9, 12, 13, "r")
    p.fill(21, 8, 26, 13, "m")
    p.fill(25, 8, 27, 10, "R")
    p.fill(24, 11, 26, 12, "r")
    p.fill(14, 9, 16, 11, "R")
    p.fill(17, 11, 20, 13, "R")
    # 3. the first narrows: a gap in the papyrus, x 14-17
    p.fill(14, 14, 17, 16, "g")
    # 4. the maze and band 2 (thicket pillars stand in it)
    p.fill(9, 17, 25, 20, "R")
    p.fill(12, 18, 13, 19, "P")
    p.fill(19, 17, 20, 18, "P")
    p.fill(23, 19, 24, 20, "P")
    # 5. the clearing: the second pool with its islet, the rest point's tower, the
    # pillar, the Nursery gate; reeds round its edges, the way down dry at x 17-22
    p.fill(10, 21, 30, 26, "g")
    p.fill(2, 21, 14, 26, "m")
    p.fill(3, 22, 7, 25, "~")
    p.fill(4, 23, 5, 24, "m")
    p.cells([(7, 22), (3, 25)], "w")
    p.fill(12, 22, 14, 23, "r")
    p.fill(12, 25, 15, 26, "r")
    p.fill(26, 21, 30, 22, "R")
    p.fill(24, 23, 27, 24, "R")
    p.fill(23, 25, 27, 26, "R")
    p.fill(16, 25, 18, 26, "R")
    p.fill(28, 23, 31, 25, "g")
    # 6. the second narrows (gap x 18-21) and its west corridor to a dead end
    p.fill(18, 27, 21, 31, "g")
    p.fill(11, 29, 17, 29, "r")
    # 7. band 3
    p.fill(9, 32, 26, 35, "R")
    p.fill(15, 33, 16, 34, "P")
    p.fill(9, 33, 11, 35, "r")
    p.fill(9, 32, 11, 32, "m")
    # 8. the meadow: the third pool west, the fishing pool east, reeds either side
    # of the dry way down at x 14-17
    p.fill(10, 36, 30, 40, "g")
    p.fill(2, 36, 9, 40, "m")
    p.fill(3, 37, 7, 39, "~")
    p.cells([(5, 38)], "w")
    p.fill(22, 36, 29, 40, "m")
    p.fill(23, 37, 28, 39, "~")
    p.cells([(25, 38)], "w")
    p.fill(10, 37, 13, 40, "R")
    p.fill(18, 37, 21, 40, "R")
    # 9. the last narrows under Memphis
    p.fill(13, 41, 17, 44, "g")
    p.fill(14, 41, 16, 45, "p")
    return p


def compose():
    g = Grid(W, H, NAME)
    pl = plan()
    E.paint(g, pl)
    g.put("stele", 12, 1)                     # the north sign
    g.put("gnat_tower", 22, 9)                # the first tower
    g.put("gnat_tower", 10, 21)               # the rest point's
    g.put("ibis_pillar", 17, 21)              # Thoth's waystone
    # the Papyrus Shallows' gate: a reed fence across the opening, shut (batch 2)
    for y in NURSERY[1]:
        g.part("fence", "v" if y != 24 else "gate", 29, y)
    g.put("stele", 28, 23)                    # the Nursery's notice
    g.palm(15, 23)
    g.palm(20, 24)
    g.put("stele", 13, 42)                    # the south sign
    g.put("papyrus_water", 7, 9)
    g.put("papyrus_water", 3, 39)
    g.put("papyrus_water", 28, 37)
    return g, pl


# trainers MAP_DESIGN calls checkpoints: name -> (x, y, facing, sight)
MANDATORY = {
    "Sobekhotep": (14, 15, "E", 3),
    "Ankhu": (21, 28, "W", 3),
    "Menna": (17, 42, "W", 3),
}


def events():
    ev = {"object_events": [], "warp_events": [], "coord_events": [], "bg_events": []}
    o = ev["object_events"]
    T = lambda gfx, x, y, name, face, sight: obj(P + gfx, x, y, S + name, face, trainer=True, sight=sight)
    # 700, the easy first trainer, in plain view on the road in
    o.append(T("HARVESTER", 18, 3, "Pa", "MOVEMENT_TYPE_FACE_LEFT", 2))
    # the narrows
    o.append(T("SAILOR", 14, 15, "Sobekhotep", "MOVEMENT_TYPE_FACE_RIGHT", 3))
    o.append(T("ACOLYTE_M", 21, 28, "Ankhu", "MOVEMENT_TYPE_FACE_LEFT", 3))
    o.append(T("HOPLITE", 17, 42, "Menna", "MOVEMENT_TYPE_FACE_LEFT", 3))
    # optional: off the path or facing away
    o.append(T("AUGUR", 27, 12, "Nebamun", "MOVEMENT_TYPE_FACE_LEFT", 2))
    o.append(T("FISHER", 22, 38, "Iuny", "MOVEMENT_TYPE_FACE_RIGHT", 1))
    o.append(T("KID_F", 25, 24, "Merit", "MOVEMENT_TYPE_FACE_DOWN", 2))
    o.append(T("ELDER_M", 10, 39, "Khety", "MOVEMENT_TYPE_FACE_UP", 2))
    o.append(T("PRIESTESS", 29, 36, "Tiye", "MOVEMENT_TYPE_FACE_LEFT", 2))
    # the gnat-tower families: the first tower's sleeper, the rest point's healer
    o.append(obj(P + "ELDER_F", 24, 13, S + "TowerGranny", "MOVEMENT_TYPE_FACE_DOWN"))
    o.append(obj(P + "WOMAN", 12, 24, S + "Healer", "MOVEMENT_TYPE_FACE_DOWN"))
    o.append(obj(P + "KID_M", 19, 24, S + "TowerKid", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1))
    # the Nursery's keeper at its gate
    o.append(obj(P + "SHEPHERD", 28, 24, S + "NurseryKeeper", "MOVEMENT_TYPE_FACE_LEFT"))
    # items: every dead end pays
    o.append(item_ball(27, 8, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_ITEM_DELTA_MIRACLE_SEED"))
    o.append(item_ball(2, 13, "ITEM_DUSK_BALL", "FLAG_ICHOR_ITEM_DELTA_DUSK_BALL"))
    o.append(item_ball(4, 23, "ITEM_MYSTIC_WATER", "FLAG_ICHOR_ITEM_DELTA_ISLET"))
    o.append(item_ball(11, 29, "ITEM_FULL_RESTORE", "FLAG_ICHOR_ITEM_DELTA_FULL_RESTORE"))
    o.append(item_ball(9, 40, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_DELTA_ULTRA_BALL"))
    b = ev["bg_events"]
    b.append(sign(12, 1, S + "NorthSign"))
    b.append(sign(13, 42, S + "SouthSign"))
    b.append(sign(17, 22, S + "IbisPillar"))          # ICHOR_STUB_HERM
    b.append(sign(28, 23, S + "NurserySign"))
    for y in NURSERY[1]:
        b.append(sign(29, y, S + "NurseryFence"))
    b.append(sign(22, 12, S + "GnatTower"))
    b.append(sign(23, 12, S + "GnatTower"))
    b.append(hidden(28, 36, "ITEM_BIG_ROOT", "FLAG_ICHOR_HIDDEN_DELTA_BIG_ROOT"))
    b.append(hidden(17, 31, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_DELTA_REVIVE"))
    b.append(hidden(26, 13, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_DELTA_HEART_SCALE"))
    b.append(hidden(16, 22, "ITEM_SHINY_STONE", "FLAG_ICHOR_HIDDEN_DELTA_SHINY_STONE"))
    return ev


CONNECTIONS = [
    {"map": "MAP_NAUKRATIS", "offset": -2, "direction": "up"},
    {"map": "MAP_MEMPHIS", "offset": -4, "direction": "down"},
]

SCREENS = {"1_road_in": (15, 3), "2_band1": (15, 7), "3_tower": (19, 11), "4_narrows1": (15, 15),
           "5_maze": (16, 19), "6_clearing": (17, 23), "7_nursery": (26, 24),
           "8_narrows2": (19, 28), "9_band3": (17, 33), "10_pool": (21, 38), "11_out": (15, 42)}
STARTS = [(x, 0) for x in NORTH_ROAD]
GOALS = [(x, H - 1) for x in SOUTH_ROAD]


def check_route(blocks, ev):
    errs = []
    w = E.Walk(blocks)
    if w.cost(STARTS, GOALS) is None:
        return ["DeltaReeds: no walk at all from Naukratis to Memphis"]
    bands = w.forced_bands(STARTS, GOALS)
    for part, depth in bands:
        ys = sorted({y for _, y in part})
        print(f"  forced band: rows {ys[0]}-{ys[-1]}, {len(part)} cells, crossed in no fewer than "
              f"{depth} steps")
    if len(bands) < 3:
        errs.append(f"DeltaReeds: {len(bands)} forced bands, want 3")
    if any(d < 3 for _, d in bands):
        errs.append("DeltaReeds: a forced band can be crossed in under 3 steps (a post-game route)")
    built = {e["script"].split("_")[-1]: e for e in ev["object_events"]
             if e["trainer_type"] != "TRAINER_TYPE_NONE"}
    for name, (x, y, facing, reach) in MANDATORY.items():
        e = built[name]
        if (e["x"], e["y"], E.FACING[e["movement_type"]], int(e["trainer_sight_or_berry_tree_id"])) != \
                (x, y, E.FACING[facing], reach):
            errs.append(f"DeltaReeds: {name}'s event does not match MANDATORY")
        line = w.sight(x, y, facing, reach)
        skirt = w.cost(STARTS, GOALS, avoid=set(line) | {(x, y)})
        print(f"  {name} at ({x},{y}) sees {line}: " + ("cannot be skirted" if skirt is None else "CAN be skirted"))
        if skirt is not None:
            errs.append(f"DeltaReeds: {name}'s line can be skirted")
    for name in sorted(set(built) - set(MANDATORY)):
        print(f"  {name} is optional")
    # grass: how much of the walkable ground beyond the forced bands is reeds
    walk = [c for c, k in w.kind.items() if k in ("open", "grass")]
    forced = set().union(*[p for p, _ in bands]) if bands else set()
    grass = [c for c in walk if w.kind[c] == "grass" and c not in forced]
    rest = [c for c in walk if c not in forced]
    share = len(grass) / max(1, len(rest))
    print(f"  reeds: {len(forced)} cells in forced bands; {len(grass)} of the other {len(rest)} "
          f"walkable cells ({share:.0%})")
    if share < 0.3:
        errs.append(f"DeltaReeds: only {share:.0%} of the ground beyond the bands is reeds; want about a third")
    return errs


def dead_ends(blocks, ev):
    """Cells with a single walkable neighbour (corridor ends): each must hold an item
    or a person, or be next to one."""
    w = E.Walk(blocks)
    ok = {(o["x"], o["y"]) for o in ev["object_events"]} | \
         {(b["x"], b["y"]) for b in ev["bg_events"]}
    errs = []
    for (x, y), k in w.kind.items():
        if k not in ("open", "grass") or y in (0, H - 1):
            continue
        n = [(x + dx, y + dy) for dx, dy in E.STEPS if w.kind.get((x + dx, y + dy)) in ("open", "grass")]
        if len(n) == 1 and not ({(x, y)} | {(x + dx, y + dy) for dx, dy in E.STEPS}) & ok:
            errs.append(f"DeltaReeds: dead end at ({x},{y}) pays nothing")
    return errs


def build(render_dir=None):
    g, pl = compose()
    E.write_layout(g, NAME, LAYOUT, [g.k("thicket", "c"), g.k("thicket", "c2"),
                                     g.k("thicket", "c2"), g.k("thicket", "c")])
    ev = events()
    E.write_map_json(NAME, ev, CONNECTIONS, music="MUS_ICHOR_ROAD", map_type="MAP_TYPE_ROUTE",
                     weather="WEATHER_SUNNY", show_map_name=True)
    errors, reach, blocks = E.check_map(NAME, [(15, 0), (4, 23)], ev)   # the islet is reached by surfing
    for edge, want in (("n", NORTH_ROAD), ("s", SOUTH_ROAD)):
        got = E.seam_open(blocks, edge, range(W))
        if got != list(want):
            errors.append(f"{NAME}: {edge} seam open at {got}, want {list(want)}")
    east = E.seam_open(blocks, "e", range(H))
    if east != list(NURSERY[1]):
        errors.append(f"{NAME}: east edge open at {east}, want only the Nursery's rows {list(NURSERY[1])}")
    errors += check_route(blocks, ev)
    errors += dead_ends(blocks, ev)
    if render_dir:
        out = Path(render_dir)
        png = E.render(LAYOUT, NAME, W, H, out / "delta_reeds.png")
        E.overlay(png, NAME, W, out / "delta_reeds_walk.png", events=ev)
        E.crops(NAME, W, H, out, "delta_reeds", SCREENS)
    E.report(errors, NAME)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    args = ap.parse_args()
    build(args.render)
