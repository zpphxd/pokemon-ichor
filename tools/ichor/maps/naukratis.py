#!/usr/bin/env python3
"""Build Naukratis (aethos + kemet): the Greeks' trading port in the Nile delta, a
first port, and the Oikoumene's hub (OIKOUMENE.md §4.5; BUILD.md §5).

Writes data/layouts/Naukratis/ and data/maps/Naukratis/map.json, then checks them:
doors on door metatiles, people on walkable ground, every person and sign
reachable, Alethea's quay scene on the only way off the quay.

The plan: the harbor basin opens north onto Pharos's waters, walled by papyrus. The
quay (Nausikles at the mooring steps, a Nile boat alongside, Naukratis ware waiting
to ship) climbs one stair into town between the Asclepeion and the Agora, which face
the market square. East of the square, behind white walls, is the Hellenion, the
shrine nine Greek cities built together: the town's signature. The households sit
round the square and down the south road; Thoth's ibis pillar stands at the
crossroads; the road leaves south for the Delta Reeds and Memphis.

Usage: /usr/bin/python3 tools/ichor/maps/naukratis.py [--render DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import egypt_lib as E  # noqa: E402
from egypt_lib import Grid, Plan, hidden, item_ball, obj, sign, trigger, warp  # noqa: E402

W, H = 36, 34
NAME, LAYOUT = "Naukratis", "LAYOUT_NAUKRATIS"
NORTH_WATER = range(5, 31)     # open water on the north edge, under Pharos's south edge
SOUTH_ROAD = range(16, 19)     # the road on the south edge, onto the Delta Reeds
STAIR = (17, 9)                # the one stair from the quay into town
MOORING = (10, 6)              # Nausikles's steps
WINGS_LANDING = (13, 14)       # outside the Asclepeion's door
P = "OBJ_EVENT_GFX_ICHOR_"
S = "Naukratis_EventScript_"

# the households' doors, warp ids 0-6 in BUILD.md §5's order
DOORS = [
    ("Asclepeion", (13, 13), "MAP_NAUKRATIS_ASCLEPEION"),
    ("Agora", (20, 13), "MAP_NAUKRATIS_AGORA"),
    ("FieldStation", (3, 17), "MAP_NAUKRATIS_FIELD_STATION"),
    ("EggOvens", (7, 21), "MAP_NAUKRATIS_EGG_OVENS"),
    ("IncenseShop", (13, 21), "MAP_NAUKRATIS_INCENSE_SHOP"),
    ("PottersHouse", (22, 22), "MAP_NAUKRATIS_POTTERS_HOUSE"),
    ("NetLoft", (3, 12), "MAP_NAUKRATIS_NET_LOFT"),
]


def plan():
    p = Plan(W, H)
    # the basin, papyrus round it, mud banks at its sides
    p.fill(0, 0, 35, 9, "P")
    p.fill(3, 4, 32, 5, "m")
    p.fill(5, 0, 30, 5, "~")
    p.fill(4, 4, 31, 5, "~")
    p.cells([(3, 4), (3, 5), (32, 4), (32, 5), (4, 3), (31, 3)], "m")
    p.cells([(8, 1), (26, 2), (13, 3)], "w")
    # the quay, three rows deep, and its wall face below
    p.fill(4, 6, 31, 8, "q")
    p.fill(4, 9, 31, 9, "B")
    p.fill(2, 6, 3, 9, "P")
    p.fill(32, 6, 33, 9, "P")
    # the stair lane down between the Asclepeion and the Agora, and the square
    p.fill(16, 10, 18, 13, "p")
    p.fill(5, 14, 23, 18, "p")
    p.fill(1, 13, 4, 13, "p")             # the lane past the net-loft's door
    p.fill(4, 13, 6, 14, "p")
    # the south road, and the lanes to the houses
    p.fill(16, 19, 18, 33, "p")
    p.fill(6, 22, 15, 22, "p")
    p.fill(19, 23, 23, 23, "p")
    # the Hellenion's court: an axis from its gate to the temple
    p.fill(26, 13, 32, 20, "g")
    p.fill(28, 17, 29, 23, "p")
    # the irrigation canal west of the road, lotus on it, a shaduf at its edge
    p.fill(1, 24, 14, 29, "m")
    p.fill(2, 26, 13, 28, "~")
    p.cells([(4, 27), (9, 26), (12, 28)], "w")
    # the clay pit by the potter's
    p.fill(24, 24, 28, 26, "m")
    # papyrus round the town's edges, open only at the south road
    p.fill(0, 30, 15, 33, "P")
    p.fill(19, 30, 35, 33, "P")
    p.fill(0, 22, 1, 33, "P")
    p.fill(34, 22, 35, 33, "P")
    return p


def compose():
    g = Grid(W, H, NAME)
    pl = plan()
    E.paint(g, pl)
    # the quay's furniture: the mooring, bollards, the boat alongside, pottery
    g.part("quay", "steps", *MOORING)
    for x in (7, 14, 23, 28):
        g.part("quay", "bollard", x, 6)
    g.put("nile_boat", 20, 2)
    g.put("amphorae", 24, 7)
    g.put("amphorae", 5, 8)
    # the harbor wall, with its one stair
    E.face_row(g, [(x, 9) for x in range(4, 32) if x != STAIR[0]])
    g.set(STAIR[0], STAIR[1], 0x0AF)
    # the Asclepeion and the Agora face the square
    g.block(E.ASCLEPEION, 12, 10)
    g.block(E.AGORA, 19, 10)
    g.set(13, 13, E.ASCLEPEION[3][1], False)
    g.set(20, 13, E.AGORA[3][1], False)
    # the net-loft by the harbor, west of the Asclepeion
    g.house(2, 10, [["roof_W", "roof_nets_l", "roof_nets_r", "roof_E"],
                    ["up_W", "up_win", "up", "up_E"],
                    ["lo_W", "lo_door_red", "lo_win", "lo_E"]])
    g.palm(7, 10)
    g.palm(9, 11, young=True)
    # households round the square and down the road
    g.house(1, 15, [["roof_W", "roof_loggia_l", "roof_loggia_r", "roof_jars", "roof_E"],
                    ["up_W", "up_win", "up", "up_win", "up_E"],
                    ["lo_W", "lo_win", "lo_door_blue", "lo_win", "lo_E"]])          # Daphne
    g.house(6, 19, [["roof_W", "roof_dome", "roof_dome", "roof_jars", "roof_E"],
                    ["rup_W", "rup", "rup", "rup", "rup_E"],
                    ["rlo_W", "rlo_door_red", "rlo", "rlo", "rlo_E"]])              # egg-ovens
    g.house(11, 19, [["roof_W", "roof_malqaf", "roof_jars", "roof_E"],
                     ["up_W", "up_win", "up_win", "up_E"],
                     ["lo_W", "lo_jars", "lo_door_awning", "lo_E"]])                # incense
    g.house(20, 20, [["roof_W", "roof_pots", "roof_pots", "roof_E"],
                     ["rup_W", "rup", "rup", "rup_E"],
                     ["rlo_W", "rlo", "rlo_door", "rlo_E"]])                        # potter
    g.put("amphorae", 24, 22)
    # the Hellenion: white walls round a court, the temple, the altar, its gate
    walls = [(x, 11) for x in range(25, 35)] + [(25, y) for y in range(11, 22)] + \
            [(34, y) for y in range(11, 22)] + [(x, 21) for x in range(25, 35) if not 27 <= x <= 30]
    E.wall(g, walls + [(27, 21), (30, 21)], skip_faces=[(27, 22), (30, 22)])
    g.put("wall_gate", 27, 21)
    g.put("hellenion", 27, 13)
    g.put("altar_greek", 28, 18)
    g.put("stele_path", 27, 18)
    g.put("palm_young", 26, 13)
    g.put("palm_young", 33, 13)
    g.palm(32, 17)
    g.palm(26, 17)
    # the square: Thoth's ibis pillar, the market
    g.put("ibis_pillar_path", 11, 15)
    g.put("stall_bread", 6, 15)
    g.put("stall_pots", 20, 15)
    g.put("stele_path", 15, 13)          # NAUKRATIS, by the stair's foot
    # palms along the road and round the canal and the clay pit
    for (x, y) in ((2, 21), (14, 24), (19, 25), (23, 27), (26, 27), (29, 25), (31, 22),
                   (32, 27), (20, 28) , (2, 13)):
        if all(pl[yy][xx] in "gm" for xx in (x, x + 1) for yy in (y, y + 1, y + 2)):
            g.palm(x, y)
    for (x, y) in ((24, 19), (25, 19)):
        g.put("granary", x, y)
    g.put("shaduf", 5, 24)
    g.put("stele", 15, 29)              # NAUKRATIS, by the south road
    return g, pl


def events():
    ev = {"object_events": [], "warp_events": [], "coord_events": [], "bg_events": []}
    o = ev["object_events"]
    # the quay
    o.append(obj(P + "SAILOR", *MOORING, "Oik_EventScript_SailHome", local_id="LOCALID_NAUKRATIS_NAUSIKLES"))
    o.append(obj(P + "ALETHEA", 17, 11, S + "Alethea", "MOVEMENT_TYPE_FACE_UP",
                 flag="FLAG_ICHOR_OIKOUMENE_ARRIVED", local_id="LOCALID_NAUKRATIS_ALETHEA"))
    o.append(obj(P + "SAILOR", 26, 7, S + "Boatman", "MOVEMENT_TYPE_FACE_UP"))
    o.append(obj(P + "FISHER", 6, 7, S + "Fisher", "MOVEMENT_TYPE_FACE_UP"))
    # the square: the argument about which continent this is
    o.append(obj(P + "MAN", 13, 17, S + "Ionian", "MOVEMENT_TYPE_FACE_RIGHT"))
    o.append(obj(P + "MERCHANT", 14, 17, S + "Egyptian", "MOVEMENT_TYPE_FACE_LEFT"))
    o.append(obj(P + "YOUTH_F", 14, 18, S + "Libyan", "MOVEMENT_TYPE_FACE_UP"))
    o.append(obj(P + "WOMAN", 7, 17, S + "BreadSeller", "MOVEMENT_TYPE_FACE_DOWN"))
    o.append(obj(P + "KID_M", 21, 18, S + "Kid", "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1))
    # the Hellenion's priest and a pilgrim
    o.append(obj(P + "PRIESTESS", 30, 18, S + "Priestess", "MOVEMENT_TYPE_FACE_LEFT"))
    o.append(obj(P + "ELDER_M", 31, 20, S + "Samian", "MOVEMENT_TYPE_FACE_UP"))
    # the south road
    o.append(obj(P + "HARVESTER", 7, 25, S + "Gardener", "MOVEMENT_TYPE_FACE_LEFT"))
    o.append(obj(P + "ELDER_F", 24, 23, S + "OldWoman", "MOVEMENT_TYPE_FACE_DOWN"))
    # a sailor's forgotten luck, in the lee of the Asclepeion
    o.append(item_ball(10, 10, "ITEM_LUCKY_EGG", "FLAG_ICHOR_ITEM_NAUKRATIS_AMPHORA"))
    # doors
    for i, (room, (x, y), dest) in enumerate(DOORS):
        ev["warp_events"].append(warp(x, y, dest, 0))
    # Alethea's scene waits at the foot of the stair, the only way off the quay
    ev["coord_events"].append(trigger(STAIR[0], STAIR[1] + 1, S + "AletheaScene"))
    b = ev["bg_events"]
    b.append(sign(15, 13, S + "TownSign"))
    b.append(sign(15, 29, S + "SouthSign"))
    b.append(sign(11, 16, S + "IbisPillar"))          # ICHOR_STUB_HERM
    b.append(sign(27, 18, S + "HellenionStele"))
    for x in range(27, 32):
        b.append(sign(x, 16, S + "Temple", "BG_EVENT_PLAYER_FACING_NORTH"))
    b.append(sign(28, 18, S + "Altar"))
    b.append(sign(29, 18, S + "Altar"))
    b.append(hidden(28, 6, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_NAUKRATIS_PEARL"))
    # ICHOR_STUB_HIDDEN: Stardust at (26, 20), the Hellenion's court, when bank-flag hidden
    # items land (MAPS_egypt.md)
    return ev


CONNECTIONS = [
    {"map": "MAP_PHAROS", "offset": 0, "direction": "up"},
    {"map": "MAP_DELTA_REEDS", "offset": 2, "direction": "down"},
]

SCREENS = {"1_quay": (10, 7), "2_stair": (17, 11), "3_square": (13, 16), "4_hellenion": (29, 19),
           "5_households": (10, 22), "6_south": (17, 27)}


def build(render_dir=None):
    g, pl = compose()
    E.write_layout(g, NAME, LAYOUT, [g.k("thicket", "c"), g.k("thicket", "c2"),
                                     g.k("thicket", "c2"), g.k("thicket", "c")])
    ev = events()
    E.write_map_json(NAME, ev, CONNECTIONS, music="MUS_ICHOR_EMPORION", map_type="MAP_TYPE_TOWN",
                     weather="WEATHER_SUNNY", show_map_name=True)
    errors, reach, blocks = E.check_map(NAME, (17, 20), ev, water_ok=("LOCALID_NAUKRATIS_NAUSIKLES",))
    # the seams: open water north, the road south
    north = E.seam_open(blocks, "n", range(W), water=True)
    if north != list(NORTH_WATER):
        errors.append(f"{NAME}: north seam water is {north}, want {list(NORTH_WATER)}")
    south = E.seam_open(blocks, "s", range(W))
    if south != list(SOUTH_ROAD):
        errors.append(f"{NAME}: south seam is open at {south}, want {list(SOUTH_ROAD)}")
    # Alethea's trigger is the only way off the quay
    quay = E.reachable(blocks, MOORING)
    cut = blocks.copy()
    cut[STAIR[1] + 1, STAIR[0]] |= E.SOLID
    if (17, 20) in E.reachable(cut, (MOORING[0], MOORING[1] + 1)):
        errors.append(f"{NAME}: the quay reaches town without crossing Alethea's trigger")
    if (17, 20) not in quay:
        errors.append(f"{NAME}: the quay doesn't reach town")
    if WINGS_LANDING not in reach:
        errors.append(f"{NAME}: the Wings landing {WINGS_LANDING} is unreachable")
    if render_dir:
        out = Path(render_dir)
        png = E.render(LAYOUT, NAME, W, H, out / "naukratis.png")
        E.overlay(png, NAME, W, out / "naukratis_walk.png", events=ev)
        E.crops(NAME, W, H, out, "naukratis", SCREENS)
    E.report(errors, NAME)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    args = ap.parse_args()
    build(args.render)
