#!/usr/bin/env python3
"""Build Memphis (aethos + kemet): the old capital inside its White Walls
(OIKOUMENE.md §4.5; PERIODOS.md §4.5; BUILD.md §5).

The road from the Delta Reeds enters by the north gate into a plaza between the
Asclepeion and the Agora (Greeks have lived in Memphis since Psamtik's day). The
avenue runs south to a crossroads where the alabaster sphinx lies; east of it the
sacred way leads to the pylon of the precinct of Proteus, flanked by obelisks, its
doors shut and a Carian guard before them until batch 2's hall opens. The west
quarter holds the households: the Apis keepers' byre with the temple herd's pen,
the scribe of Thoth and the embalmer. The south gate opens onto the desert road;
the six rows nearest the south edge are aethos-only, for the Nile and the Pyramid
Field (batch 2).

Usage: /usr/bin/python3 tools/ichor/maps/memphis.py [--render DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import egypt_lib as E  # noqa: E402
from egypt_lib import Grid, Plan, hidden, item_ball, obj, sign, warp  # noqa: E402

W, H = 40, 36
NAME, LAYOUT = "Memphis", "LAYOUT_MEMPHIS"
NORTH_ROAD = range(18, 21)       # under the Delta Reeds' south road (offset 4)
SOUTH_EDGE = range(14, 26)       # the desert road and its verges, open for batch 2
WINGS_LANDING = (13, 10)         # outside the Asclepeion's door
HALL_DOOR = (32, 20)             # the pylon's doors: ICHOR_STUB_HALL
P = "OBJ_EVENT_GFX_ICHOR_"
S = "Memphis_EventScript_"

DOORS = [
    ("Asclepeion", (13, 9), "MAP_MEMPHIS_ASCLEPEION"),
    ("Agora", (24, 9), "MAP_MEMPHIS_AGORA"),
    ("ApisStable", (4, 9), "MAP_MEMPHIS_APIS_STABLE"),
    ("ScribesHouse", (4, 20), "MAP_MEMPHIS_SCRIBES_HOUSE"),
    ("EmbalmersHouse", (10, 20), "MAP_MEMPHIS_EMBALMERS_HOUSE"),
]


def plan():
    p = Plan(W, H)
    # outside the north wall: papyrus up to the walls, the road in
    p.fill(0, 0, 39, 1, "P")
    p.fill(18, 0, 20, 1, "p")
    # the walls' footprint
    p.fill(0, 2, 39, 3, "B")
    p.fill(0, 2, 0, 28, "B")
    p.fill(39, 2, 39, 28, "B")
    p.fill(0, 27, 39, 28, "B")
    # the gate plaza between the Asclepeion and the Agora, the avenue south
    p.fill(11, 5, 28, 11, "p")
    p.fill(18, 2, 19, 4, "p")
    p.fill(18, 12, 20, 29, "p")
    # the crossroads and the sacred way east to the pylon
    p.fill(13, 22, 26, 25, "p")
    p.fill(21, 21, 37, 23, "p")
    # the west quarter's lanes
    p.fill(1, 10, 10, 11, "p")
    p.fill(2, 21, 14, 21, "p")
    p.fill(11, 12, 12, 21, "p")
    # the herd's pen: bare earth
    p.fill(2, 13, 8, 16, "m")
    # the precinct behind its walls: palms over the wall
    p.fill(27, 6, 38, 20, "B")
    # outside the south gate: the desert road (aethos only below row 29)
    p.fill(0, 29, 39, 35, "g")
    p.fill(10, 31, 30, 35, "s")
    p.fill(17, 30, 21, 35, "p")
    p.fill(0, 33, 9, 35, "s")
    p.fill(31, 33, 39, 35, "s")
    return p


def compose():
    g = Grid(W, H, NAME)
    pl = plan()
    E.paint(g, pl)
    # the White Walls: north, round both sides, south; gates north and south
    walls = [(x, 2) for x in range(W) if not 17 <= x <= 20] + [(17, 2), (20, 2)]
    walls += [(0, y) for y in range(2, 28)] + [(39, y) for y in range(2, 28)]
    walls += [(x, 27) for x in range(W) if not 17 <= x <= 20] + [(17, 27), (20, 27)]
    E.wall(g, walls, skip_faces=[(17, 3), (20, 3), (17, 28), (20, 28)])
    g.put("wall_gate", 17, 2)
    g.put("wall_gate", 17, 27)
    # the gate plaza
    g.block(E.ASCLEPEION, 12, 6)
    g.block(E.AGORA, 23, 6)
    g.set(13, 9, E.ASCLEPEION[3][1], False)
    g.set(24, 9, E.AGORA[3][1], False)
    g.put("stall_bread_path", 15, 7)
    g.put("stall_pots_path", 21, 7)
    # the precinct of Proteus: its walls, the pylon in the south wall, obelisks
    pw = [(x, 7) for x in range(27, 39)] + [(27, y) for y in range(7, 20)] + \
         [(38, y) for y in range(7, 20)] + [(28, 19), (36, 19), (37, 19)]
    E.wall(g, pw, skip_faces=[(28, 20), (36, 20)])
    g.put("pylon", 29, 16)
    g.set(HALL_DOOR[0], HALL_DOOR[1], g.k("pylon", "door"), True)     # shut until batch 2
    for (x, y) in ((29, 9), (34, 9), (31, 11), (36, 12), (28, 12)):
        g.palm(x, y)
    g.put("obelisk", 28, 21)
    g.put("obelisk", 36, 21)
    # the alabaster sphinx at the crossroads
    g.put("sphinx", 14, 22)
    # the west quarter: the Apis keepers' byre and the herd's pen, the scribe, the
    # embalmer
    g.house(2, 7, [["roof_W", "roof_shade_l", "roof_shade_r", "roof_jars", "roof_E"],
                   ["rup_W", "rup", "rup", "rup", "rup_E"],
                   ["rlo_W", "rlo", "rlo_door_wide", "rlo", "rlo_E"]])
    for x in range(2, 9):
        if x not in (5,):
            g.part("fence", "run", x, 12)
        g.part("fence", "run", x, 17)
    for y in range(13, 17):
        g.part("fence", "v", 1, y)
        g.part("fence", "v", 9, y)
    g.house(2, 18, [["roof_W", "roof_dovecote", "roof_scrolls", "roof_E"],
                    ["up_W", "up_win", "up_ibis", "up_E"],
                    ["lo_W", "lo_win", "lo_door_blue", "lo_E"]])
    g.house(8, 18, [["roof_W", "roof_linen_l", "roof_linen_r", "roof_E"],
                    ["up_W", "up_win", "up", "up_E"],
                    ["lo_W", "lo_jars", "lo_door_red", "lo_E"]])
    # palms and granaries
    for (x, y) in ((1, 4), (6, 4), (9, 13), (14, 13), (22, 12), (24, 15), (15, 17), (35, 24),
                   (31, 24), (2, 23), (6, 23), (10, 23), (27, 24)):
        if all(pl[yy][xx] == "g" for xx in (x, x + 1) for yy in (y, y + 1, y + 2)):
            g.palm(x, y)
    g.put("granary", 25, 13)
    g.put("granary", 26, 13)
    g.put("amphorae_path", 23, 25)
    # the city's steles
    g.put("stele_path", 17, 5)
    g.put("stele_path", 26, 21)
    return g, pl


def events():
    ev = {"object_events": [], "warp_events": [], "coord_events": [], "bg_events": []}
    o = ev["object_events"]
    # the pylon's guard: a Carian mercenary, the pharaoh's (ICHOR_STUB_HALL)
    o.append(obj(P + "HOPLITE", HALL_DOOR[0] - 1, HALL_DOOR[1] + 1, S + "PylonGuard", "MOVEMENT_TYPE_FACE_DOWN",
                 local_id="LOCALID_MEMPHIS_PYLON_GUARD"))
    # the temple herd in its pen, one of them maybe the true Apis
    for (x, y) in ((3, 14), (6, 15), (7, 13)):
        o.append(obj("OBJ_EVENT_GFX_SPECIES(TAUROS)", x, y, S + "Herd", "MOVEMENT_TYPE_WANDER_AROUND",
                     rx=1, ry=1))
    o.append(obj(P + "SHEPHERD", 5, 11, S + "Herdsman", "MOVEMENT_TYPE_FACE_DOWN"))
    # the plaza and the streets
    o.append(obj(P + "MERCHANT", 16, 9, S + "Baker", "MOVEMENT_TYPE_FACE_DOWN"))
    o.append(obj(P + "WOMAN", 22, 9, S + "PotSeller", "MOVEMENT_TYPE_FACE_DOWN"))
    o.append(obj(P + "MAN", 19, 14, S + "Greek", "MOVEMENT_TYPE_FACE_RIGHT"))
    o.append(obj(P + "MERCHANT", 20, 14, S + "Tyrian", "MOVEMENT_TYPE_FACE_LEFT"))
    o.append(obj(P + "ELDER_M", 17, 24, S + "SphinxSage", "MOVEMENT_TYPE_FACE_LEFT"))
    o.append(obj(P + "KID_F", 25, 22, S + "Kid", "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1))
    o.append(obj(P + "PRIESTESS", 34, 22, S + "Priestess", "MOVEMENT_TYPE_FACE_UP"))
    # the desert road: two travellers who'll fight (optional, facing away)
    o.append(obj(P + "AUGUR", 23, 32, S + "Amenemope", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3))
    o.append(obj(P + "ELDER_F", 14, 33, S + "Nefertari", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3))
    o.append(item_ball(37, 34, "ITEM_SOFT_SAND", "FLAG_ICHOR_ITEM_MEMPHIS_SOFT_SAND"))
    for i, (room, (x, y), dest) in enumerate(DOORS):
        ev["warp_events"].append(warp(x, y, dest, 0))
    b = ev["bg_events"]
    b.append(sign(17, 5, S + "CitySign"))
    b.append(sign(26, 21, S + "SacredWay"))
    b.append(sign(HALL_DOOR[0], HALL_DOOR[1], S + "PylonDoor"))      # ICHOR_STUB_HALL
    for x in range(29, 36):
        if x not in (HALL_DOOR[0] - 1, HALL_DOOR[0]):
            b.append(sign(x, 20, S + "PylonRelief", "BG_EVENT_PLAYER_FACING_NORTH"))
    b.append(sign(28, 23, S + "Obelisk"))
    b.append(sign(36, 23, S + "Obelisk"))
    for x in range(14, 17):
        b.append(sign(x, 23, S + "Sphinx"))
    b.append(sign(16, 31, S + "SouthSign"))
    # ICHOR_STUB_HIDDEN: Stardust at (16, 22), under the sphinx's paw, when bank-flag
    # hidden items land (MAPS_egypt.md)
    b.append(hidden(8, 16, "ITEM_RARE_BONE", "FLAG_ICHOR_HIDDEN_MEMPHIS_RARE_BONE"))
    return ev


CONNECTIONS = [
    {"map": "MAP_DELTA_REEDS", "offset": 4, "direction": "up"},
    # south: the Nile and the Pyramid Field, batch 2
]

SCREENS = {"1_north_gate": (19, 4), "2_plaza": (19, 8), "3_herd": (6, 12), "4_households": (7, 20),
           "5_sphinx": (18, 23), "6_pylon": (31, 22), "7_south_gate": (19, 28), "8_desert": (19, 33)}


def build(render_dir=None):
    g, pl = compose()
    E.write_layout(g, NAME, LAYOUT, [E.GRASS, E.GRASS, E.GRASS, E.GRASS])
    ev = events()
    E.write_map_json(NAME, ev, CONNECTIONS, music="MUS_ICHOR_EMPORION", map_type="MAP_TYPE_CITY",
                     weather="WEATHER_SUNNY", show_map_name=True)
    errors, reach, blocks = E.check_map(NAME, (19, 0), ev,
                                        seams=[("rows", range(H - E.SEAM_ROWS, H), "south (batch 2)")])
    got = E.seam_open(blocks, "n", range(W))
    if not set(NORTH_ROAD) <= set(got):
        errors.append(f"{NAME}: north edge doesn't open at the road {list(NORTH_ROAD)}: {got}")
    south = E.seam_open(blocks, "s", range(W))
    if not set(SOUTH_EDGE) <= set(south):
        errors.append(f"{NAME}: south edge must stay open at {list(SOUTH_EDGE)}: open at {south}")
    if WINGS_LANDING not in reach:
        errors.append(f"{NAME}: the Wings landing {WINGS_LANDING} is unreachable")
    if render_dir:
        out = Path(render_dir)
        png = E.render(LAYOUT, NAME, W, H, out / "memphis.png")
        E.overlay(png, NAME, W, out / "memphis_walk.png", events=ev)
        E.crops(NAME, W, H, out, "memphis", SCREENS)
    E.report(errors, NAME)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    args = ap.parse_args()
    build(args.render)
