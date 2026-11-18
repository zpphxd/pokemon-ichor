#!/usr/bin/env python3
"""Route 28: the Sacred Olives (design/maps/Route28_SacredOlives.md; SCRIPT.md
III-6A and Part 2). 56 x 28, on parnassos.

The road enters from Kirrha at rows 15-17 (Kirrha's 12-14), runs east along the
top of the lowest terrace, turns north through the narrow point at the
desecrated altar, climbs through band 2 to the upper terrace, passes the
oldest olive and Hieron's hut, dips through the hollow of band 3 and turns
north at the east gate into the gorge's mouth under the Phaedriades. Ledges
drop south from the upper road to the middle orchard and from the lower road
to the lower terrace, whose west end opens back onto the calm stretch: the
quick way home.

  /usr/bin/python3 tools/ichor/maps/delphoi_olives.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delphoi_maps import A, DMap, Plan, npc, paint, trainer  # noqa: E402

W, H = 56, 25
NAME = "Route28_SacredOlives"
S = "Route28_SacredOlives_EventScript_"


def plan():
    P = Plan(W, H)
    # the calm stretch and the lower road (three wide at Kirrha's seam)
    P.box(2, 14, 7, 18, ".")
    P.box(11, 14, 21, 14, ".")
    P.box(11, 17, 19, 17, ".")
    P.box(0, 15, 6, 17, "p")
    P.road([(6, 15), (15, 15), (15, 16), (21, 16)], width=2, salt=1)
    P.road([(22, 16), (22, 5)], width=2, salt=2, bulge=False)
    P.road([(22, 5), (31, 5), (31, 6), (42, 6), (43, 6), (43, 0)], width=2, salt=3)
    # forced band 1, walled by olive masses north and south
    P.box(8, 15, 10, 17, "G")
    P.box(7, 14, 11, 14, "T")
    P.box(7, 18, 11, 18, "T")
    # the narrow point: the road turns north between two old trunks
    P.box(19, 12, 20, 13, "T")
    P.box(24, 12, 25, 13, "T")
    P.box(22, 12, 23, 13, "p")
    P.box(21, 12, 21, 13, ".")        # the altar's alcove, Psammos's place
    P.box(21, 11, 21, 11, " ")        # the altar
    # forced band 2, four deep, right behind Psammos
    P.box(20, 8, 25, 11, "T")
    P.box(21, 8, 24, 10, "G")
    P.box(22, 11, 24, 11, "G")
    P.box(21, 11, 21, 11, " ")
    # the upper road's verge
    P.box(20, 5, 21, 7, ".")
    # the oldest olive's clearing and Hieron's hut
    P.box(26, 1, 35, 4, ".")
    P.box(28, 1, 30, 3, " ")
    P.box(31, 2, 33, 3, " ")
    # the dry-stone wall along the road's north side, a gap into the side row
    P.box(35, 4, 41, 4, "w")
    P.box(36, 4, 36, 4, ".")
    P.box(36, 1, 40, 3, "G")
    P.box(36, 1, 36, 1, ".")
    P.box(40, 1, 40, 1, ".")
    # forced band 3, in the hollow before the east gate
    P.box(38, 5, 40, 7, "G")
    P.box(37, 8, 42, 8, "T")
    # the east gate and the road north into the gorge's mouth
    P.box(42, 0, 45, 4, ".")
    P.road([(43, 4), (43, 0)], width=2, salt=4, bulge=False)
    P.box(41, 0, 41, 3, "#")
    P.box(42, 0, 42, 1, "#")
    # the Phaedriades over the gorge's mouth
    P.box(46, 0, 55, 9, "#")
    P.box(46, 4, 47, 4, ".")
    P.box(46, 5, 48, 7, ".")
    P.box(46, 8, 55, 10, "T")
    # the dry bed of the gorge's stream, running away south-east: a dead end
    P.cells([(46, 6), (47, 7), (48, 8), (49, 9), (49, 10), (50, 11), (51, 12), (52, 13),
             (53, 14), (53, 15)], "s")
    P.cells([(47, 6), (48, 7), (49, 8), (50, 10), (51, 11), (52, 12), (52, 14), (54, 15)], ".")
    # the middle orchard, under the upper road's ledge
    P.box(27, 8, 36, 8, "=")
    P.box(26, 9, 50, 17, "o")
    P.box(26, 9, 30, 10, ".")
    # the lower terrace, under the lower road's ledge; its west end is open
    P.box(12, 18, 53, 18, "=")
    P.box(2, 19, 53, 23, "o")
    P.box(2, 19, 6, 19, ".")
    P.box(2, 23, 4, 23, ".")
    P.box(51, 21, 53, 23, ".")
    # lanes of long grass through the orchards, so nobody is ever walled in
    P.road([(26, 13), (37, 13), (37, 14), (50, 14)], width=1, ch="G", salt=5)
    P.road([(26, 16), (50, 16)], width=1, ch="G", salt=6)
    for x in (33, 45):
        P.box(x, 9, x, 17, "G")
    P.road([(2, 21), (24, 21), (24, 20), (40, 20), (40, 21), (53, 21)], width=1, ch="G", salt=7)
    for x in (9, 17, 31, 47):
        P.box(x, 19, x, 23, "G")
    # room for the people and the jars in the orchards
    P.box(26, 9, 30, 11, ".")         # the pilgrim family, by band 2
    P.box(39, 11, 42, 13, ".")        # the augurs' clearing
    P.box(48, 15, 50, 17, ".")        # a jar at the middle orchard's far end
    P.box(17, 20, 21, 21, ".")        # the pilgrim sisters
    P.box(4, 22, 6, 23, ".")
    P.box(45, 4, 46, 4, ".")
    return P


def events(m):
    # the signs at both ends
    m.set(4, 14, A.STELE, True)
    m.sign(4, 14, S + "SignWest")
    m.set(46, 4, A.STELE, True)
    m.sign(46, 4, S + "SignEast")
    # III-6A: the Titans' column and Hieron
    m.trigger(2, 15, S + "ColumnScene", "VAR_TEMP_1", 1)
    m.trigger(2, 16, S + "ColumnScene", "VAR_TEMP_1", 1)
    m.trigger(2, 17, S + "ColumnScene", "VAR_TEMP_1", 1)
    for i, (x, y) in enumerate(((17, 16), (18, 16), (17, 17), (18, 17))):
        npc(m, "ICHOR_TITAN_GRUNT", x, y, S + "Column", face="right",
            flag="FLAG_ICHOR_HIDE_TITAN_COLUMN_OLIVES", local_id=f"LOCALID_OLIVES_COLUMN_{i + 1}")
    npc(m, "ICHOR_ELDER_M", 6, 14, S + "HieronRoad", face="down",
        flag="FLAG_ICHOR_HIDE_HIERON_ROAD", local_id="LOCALID_OLIVES_HIERON")
    # trainers
    trainer(m, "ICHOR_PILGRIM", 14, 14, S + "Euangelos", "down", 3)
    trainer(m, "ICHOR_TITAN_GRUNT", 21, 12, S + "Psammos", "right", 3)
    trainer(m, "ICHOR_YOUTH_M", 38, 3, S + "Phayllos", "up", 2)
    trainer(m, "ICHOR_TITAN_GRUNT", 42, 2, S + "Plinthis", "right", 4)
    trainer(m, "ICHOR_YOUTH_F", 18, 20, S + "Sisters", "down", 2)
    trainer(m, "ICHOR_WOMAN", 19, 21, S + "Sisters", "left", 2)
    trainer(m, "ICHOR_AUGUR", 40, 12, S + "Augurs", "up", 2)
    trainer(m, "ICHOR_AUGUR", 41, 12, S + "Augurs", "right", 3)
    # the pilgrim family, resting by band 2
    npc(m, "ICHOR_MAN", 27, 10, S + "Father", face="right")
    npc(m, "ICHOR_KID_F", 28, 9, S + "Girl", face="down")
    npc(m, "ICHOR_KID_M", 28, 11, S + "Boy", face="up")
    # the altar, the hut, the oldest olive
    m.sign(21, 11, S + "Altar")
    m.warp(32, 3, "MAP_ROUTE28_SACRED_OLIVES_WARDENS_HUT", 0)
    # the rest stop's travel herm and plaque, on the gorge path above Hieron's
    # clearing, are placed by tools/ichor/maps/town_herms.py (fast travel)
    m.sign(28, 3, S + "OldestOlive")
    # items: every dead end pays
    m.item_ball(40, 1, "ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_OLIVES_MAX_REPEL")
    m.item_ball(4, 23, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_OLIVES_ULTRA_BALL")
    m.item_ball(54, 15, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_OLIVES_HYPER_POTION")
    m.item_ball(49, 16, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_OLIVES_FULL_HEAL")
    m.item_ball(53, 22, "ITEM_PP_UP", "FLAG_ICHOR_ITEM_OLIVES_PP_UP")
    m.hidden(29, 3, "ITEM_LEAF_STONE", "FLAG_ICHOR_HIDDEN_ITEM_OLIVES_LEAF_STONE")
    m.hidden(20, 14, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ITEM_OLIVES_REVIVE")
    m.hidden(6, 23, "ITEM_BIG_MUSHROOM", "FLAG_ICHOR_HIDDEN_ITEM_OLIVES_BIG_MUSHROOM")
    m.hidden(48, 7, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ITEM_OLIVES_STAR_PIECE")


def build():
    rows = plan().rows()
    m = DMap(NAME, "parnassos", W, H)
    m.seam("left")
    get = paint(m, rows, salt=0)
    m.scatter({c for c in get(".") | get("o") if c[0] >= 8}, "ground",
              ["tuft", "pebbles", "leaves", "thyme", "stones"], rate=160)
    m.put("oldest_olive", 28, 1)
    m.put("hut", 31, 2)
    m.put("oldest_altar", 21, 11)
    m.olive(19, 12)
    m.olive(24, 12)
    events(m)
    m.break_runs(keep=get("p") | get("G") | get("s"))
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT[0], A.OLIVE_BOT[1]]
    m.connect("left", 6, "MAP_KIRRHA")
    m.connect("up", 30, "MAP_ROUTE28_KASTALIAN_GORGE")
    return m, rows


if __name__ == "__main__":
    m, rows = build()
    print("\n".join(rows))
    m.build(NAME.lower(), starts=[(0, 16)],
            views=[(7, 15), (21, 11), (30, 5), (42, 4), (38, 13), (20, 21)])
