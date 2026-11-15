#!/usr/bin/env python3
"""Build Pharos (aethos + kemet): the island off the delta and its waters
(OIKOUMENE.md §4.5; PERIODOS.md §5; COVERAGE.md Y7).

Homer put a sea-god's seals on Pharos (Odyssey 4.351-570). In Ichor they are the
pharaoh's herd, kept by his herders, and the Ditto loose among them are strays from
Proteus's troupe at Memphis. Menelaus grabbed one of the herders here and went
home calling him a god.

The map: open sea along the whole north edge (Route 34 comes in there, world-
postgame's; the six rows nearest it are aethos-only, with a sandbar), the island in
the middle with its beach, dunes, knoll, headland, south lagoon, herders' camp and
the herd, and the delta's papyrus shores in the south corners, where the sea runs on
into Naukratis's harbor. aethos's island edges are shallow water, as in Hoenn: the
walkable island is one ring inside the drawn sand.

Usage: /usr/bin/python3 tools/ichor/maps/pharos.py [--render DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import egypt_lib as E  # noqa: E402
from egypt_lib import Grid, Plan, hidden, item_ball, obj, sign  # noqa: E402

W, H = 36, 30
NAME, LAYOUT = "Pharos", "LAYOUT_PHAROS"
SOUTH_WATER = range(5, 31)     # matches Naukratis's north edge (offset 0)
P = "OBJ_EVENT_GFX_ICHOR_"
S = "Pharos_EventScript_"
LANDING = (17, 8)              # where a surfer from the north comes ashore

ISLAND = [
    (7, (13, 22)), (8, (10, 25)), (9, (8, 27)), (10, (6, 29)), (11, (5, 30)), (12, (5, 30)),
    (13, (4, 31)), (14, (4, 31)), (15, (5, 30)), (16, (5, 29)), (17, (6, 28)), (18, (7, 27)),
    (19, (9, 25)), (20, (11, 23)), (21, (13, 21)),
]
SANDBAR = [(3, (28, 30)), (4, (27, 31)), (5, (28, 30))]
DUNES = [(8, 11, 11, 13), (20, 10, 24, 12), (7, 16, 10, 17), (21, 15, 25, 17), (13, 12, 14, 14),
         (19, 18, 22, 18), (26, 16, 26, 17)]
LAGOON = [(15, 19, 18, 21), (16, 18, 17, 18)]


def plan():
    p = Plan(W, H, "~")
    for (y, (x0, x1)) in ISLAND + SANDBAR:
        p.fill(x0, y, x1, y, "s")
    for (x0, y0, x1, y1) in DUNES:
        p.fill(x0, y0, x1, y1, "d")
    for (x0, y0, x1, y1) in LAGOON:
        p.fill(x0, y0, x1, y1, "~")
    # the delta's shores in the south corners, papyrus behind mud, as in Naukratis
    p.fill(0, 24, 4, 29, "P")
    p.fill(31, 24, 35, 29, "P")
    p.fill(2, 22, 3, 23, "m")
    p.fill(0, 22, 1, 23, "P")
    p.fill(32, 22, 33, 23, "m")
    p.fill(34, 22, 35, 23, "P")
    # the north strip stays aethos-only: open sea (and the sandbar, which is aethos)
    for y in range(0, 6):
        for x in range(W):
            if p[y][x] == "~":
                p[y][x] = "o"
    return p


def compose():
    g = Grid(W, H, NAME)
    pl = plan()
    E.paint(g, pl)
    # the corners of the north edge: sea rocks (shore or cliff in the corner columns)
    for (x, y) in ((0, 0), (0, 1), (35, 0), (35, 1), (1, 0), (34, 0)):
        g.set(x, y, E.SEA_ROCKS[(x + y) % 4], True)
    # a reef west of the island and rocks offshore
    for (x, y) in ((2, 10), (2, 11), (3, 15), (32, 9), (33, 17), (9, 23), (26, 23), (7, 4),
                   (22, 3), (12, 26), (24, 27)):
        g.set(x, y, E.SEA_ROCKS[(x * 3 + y) % 4], True)
    # the herders' camp on the west beach: shelter, nets, palms
    g.put("shelter", 11, 15)
    g.put("nets", 6, 14)
    for (x, y, young) in ((10, 8, True), (24, 8, False), (27, 11, True), (14, 16, False),
                          (24, 14, False), (8, 13, True)):
        g.palm(x, y, young=young)
    # the knoll at the island's heart, the headland's boulders, the stele
    for (x, y) in ((17, 11), (18, 11), (17, 12), (29, 12), (29, 15), (28, 16)):
        g.set(x, y, E.BOULDER_SAND, True)
    g.put("stele_sand", 16, 9)
    return g, pl


SEALS = [(12, 9), (14, 9), (20, 9), (22, 9), (19, 8)]


def events():
    ev = {"object_events": [], "warp_events": [], "coord_events": [], "bg_events": []}
    o = ev["object_events"]
    # the herd, and its herder
    for i, (x, y) in enumerate(SEALS):
        gfx = "OBJ_EVENT_GFX_SPECIES(DEWGONG)" if i % 2 == 0 else "OBJ_EVENT_GFX_SPECIES(SEEL)"
        o.append(obj(gfx, x, y, S + "Seal", "MOVEMENT_TYPE_FACE_DOWN" if i % 2 else
                     "MOVEMENT_TYPE_FACE_LEFT"))
    o.append(obj("OBJ_EVENT_GFX_SPECIES(DITTO)", 23, 13, S + "Ditto", "MOVEMENT_TYPE_WANDER_AROUND",
                 rx=1, ry=1))
    o.append(obj("OBJ_EVENT_GFX_SPECIES(DITTO)", 9, 16, S + "Ditto", "MOVEMENT_TYPE_WANDER_AROUND",
                 rx=1, ry=1))
    o.append(obj(P + "SHEPHERD", 13, 17, S + "Herder", "MOVEMENT_TYPE_FACE_UP"))
    # trainers: a herder by the knoll in plain view, a boatman on the headland, a diver
    # by the lagoon
    o.append(obj(P + "SHEPHERD", 16, 13, S + "Thais", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3))
    o.append(obj(P + "SAILOR", 27, 14, S + "Harpalos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4))
    o.append(obj(P + "DIVER", 20, 17, S + "Neso", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3))
    o.append(obj(P + "MERCHANT", 28, 4, S + "Kallias", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=1))
    o.append(obj(P + "PRIESTESS", 7, 17, S + "Arsinoe", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=2))
    # the headland's tip, the dunes, and the sandbar out north
    o.append(item_ball(30, 13, "ITEM_MYSTIC_WATER", "FLAG_ICHOR_ITEM_PHAROS_MYSTIC_WATER"))
    o.append(item_ball(9, 11, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_PHAROS_ULTRA_BALL"))
    o.append(item_ball(30, 4, "ITEM_PEARL_STRING", "FLAG_ICHOR_ITEM_PHAROS_PEARL_STRING"))
    b = ev["bg_events"]
    b.append(sign(16, 9, S + "Stele"))
    b.append(sign(11, 15, S + "Shelter"))
    b.append(sign(12, 15, S + "Shelter"))
    b.append(hidden(18, 11, "ITEM_BIG_PEARL", "FLAG_ICHOR_HIDDEN_PHAROS_BIG_PEARL"))
    b.append(hidden(12, 19, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_PHAROS_STAR_PIECE"))
    return ev


CONNECTIONS = [
    # Route 34 (world-postgame) joins the north edge when it exists: ICHOR_STUB_AETHOS
    {"map": "MAP_NAUKRATIS", "offset": 0, "direction": "down"},
]

SCREENS = {"1_north": (17, 4), "2_herd": (17, 10), "3_camp": (11, 15), "4_headland": (25, 13),
           "5_lagoon": (17, 18), "6_south": (17, 25)}


def build(render_dir=None):
    g, pl = compose()
    E.write_layout(g, NAME, LAYOUT, [E.SEA, E.SEA, E.SEA, E.SEA])
    ev = events()
    E.write_map_json(NAME, ev, CONNECTIONS, music="MUS_ICHOR_ROAD", map_type="MAP_TYPE_OCEAN_ROUTE",
                     weather="WEATHER_SUNNY", show_map_name=True)
    errors, reach, blocks = E.check_map(NAME, [LANDING, (29, 4)], ev,
                                        seams=[("rows", range(0, E.SEAM_ROWS), "Route 34 (north)")])
    north = E.seam_open(blocks, "n", range(W), water=True)
    if north != list(range(2, 34)):
        errors.append(f"{NAME}: north edge water is {north}, want 2..33 (rocks only in the corners)")
    south = E.seam_open(blocks, "s", range(W), water=True)
    if south != list(SOUTH_WATER):
        errors.append(f"{NAME}: south edge water is {south}, want {list(SOUTH_WATER)}")
    # every water cell is one sea, so a surfer can go round the island
    water = {(x, y) for y in range(H) for x in range(W) if int(blocks[y, x]) >> 12 == 1
             and not int(blocks[y, x]) >> 10 & 3}
    seen, todo = {(17, 0)}, [(17, 0)]
    while todo:
        x, y = todo.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c = (x + dx, y + dy)
            if c in water and c not in seen:
                seen.add(c)
                todo.append(c)
    if seen != water:
        errors.append(f"{NAME}: {len(water - seen)} water cells are cut off from the open sea")
    if render_dir:
        out = Path(render_dir)
        png = E.render(LAYOUT, NAME, W, H, out / "pharos.png")
        E.overlay(png, NAME, W, out / "pharos_walk.png", events=ev)
        E.crops(NAME, W, H, out, "pharos", SCREENS)
    E.report(errors, NAME)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    args = ap.parse_args()
    build(args.render)
