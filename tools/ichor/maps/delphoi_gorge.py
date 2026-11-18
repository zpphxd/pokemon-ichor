#!/usr/bin/env python3
"""Route 28: the Kastalian Gorge (design/maps/Route28_KastalianGorge.md;
SCRIPT.md III-6B and Part 2). 30 x 47, on parnassos.

South to north: the camp's south tents and the sentries; band 1 between the
tents and the white water; the camp lane past the cookhouse (Kisseris), the
plank bridge to the west bank (Chomas by his fire, the corral); the
quartermaster's side terrace; the cutting (Agrios); band 2 in the laurel scrub;
the great herm at the foot of the lower fall; the lower fall (the Horn); the
middle ledge (Asbolos, band 3, Chrysis at the pool); the upper fall (the Horn);
the upper pool and the path north into Delphoi. The rapids are white water no
one can swim; only the pools are surfable. A cracked boulder on the middle
ledge opens a ledged path back down to the camp.

The top six rows meet Delphoi (another secondary) and use only aethos.

  /usr/bin/python3 tools/ichor/maps/delphoi_gorge.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delphoi_maps import POND, A, DMap, Plan, npc, paint, trainer  # noqa: E402

W, H = 30, 47
NAME = "Route28_KastalianGorge"
S = "Route28_KastalianGorge_EventScript_"


def plan():
    P = Plan(W, H, fill="#")
    P.box(0, 0, 29, 5, "T")
    # --- the top: the upper pool, the landing and the path to Delphoi (aethos only)
    P.box(4, 0, 25, 5, "T")
    P.box(12, 0, 15, 3, "p")
    P.box(10, 1, 17, 3, ".")
    P.box(12, 0, 15, 2, "p")
    P.box(6, 4, 13, 6, "~")
    P.box(14, 3, 17, 4, ".")
    # --- the upper fall
    P.box(7, 7, 8, 8, "F")
    # --- the middle level: the pool, the ledge path, the basin over the lower fall
    P.box(5, 9, 10, 10, "~")           # the pool (Chrysis fills her jars at its west end)
    P.box(4, 9, 4, 10, ".")
    P.box(11, 9, 18, 13, ".")          # the middle ledge
    P.box(14, 9, 15, 11, "G")          # band 3, along the pool's rim
    P.box(16, 9, 18, 11, "G")
    P.box(11, 11, 13, 11, "#")
    P.box(5, 12, 9, 13, "~")           # the basin at the lower fall's top
    P.box(10, 12, 10, 13, ".")
    P.box(4, 12, 4, 12, " ")           # the niche behind the fall
    P.box(19, 12, 20, 13, ".")         # the boulder's ledge, east
    # --- the lower fall and its plunge pool, the herm's landing
    P.box(7, 14, 8, 16, "F")
    P.box(5, 17, 9, 18, "~")
    P.box(10, 16, 16, 18, ".")
    # --- band 2, in the laurel scrub at the cutting's mouth
    P.box(10, 19, 16, 22, "T")
    P.box(11, 19, 15, 22, "G")
    # --- the cutting
    P.box(13, 23, 13, 26, "p")
    # --- the shortcut down from the middle ledge (opened by the Bronze Hammer)
    P.box(19, 14, 20, 26, ".")
    P.box(19, 18, 20, 18, "=")
    P.box(19, 23, 20, 23, "=")
    # --- the white water: the stream down the west of the gorge
    P.box(7, 19, 9, 46, "r")
    P.box(9, 19, 9, 22, "#")
    # --- the camp: the lane on the east bank
    P.box(12, 27, 16, 46, ".")
    P.road([(13, 27), (13, 46)], width=3, salt=11, bulge=False)
    P.box(17, 27, 24, 33, "T")
    P.box(18, 27, 23, 31, "G")         # the quartermaster's terrace, optional grass
    P.box(19, 26, 21, 26, ".")
    P.box(19, 27, 21, 27, "G")
    P.box(10, 31, 11, 34, " ")         # the cookhouse's oven
    P.box(10, 35, 12, 40, " ")         # crates and a small tent west of the lane
    P.box(16, 34, 24, 46, " ")         # the south tents
    P.box(16, 36, 16, 46, ".")
    # band 1, between the tents' ropes and the white water
    P.box(13, 37, 15, 39, "G")
    # --- the west bank: the corral, Chomas's fire, reached by the plank bridge
    P.box(4, 27, 6, 44, ".")
    P.box(4, 41, 6, 44, "G")
    P.box(7, 35, 9, 35, "b")
    P.box(10, 35, 11, 35, "p")
    # the foot: sentries and the sign
    P.box(12, 44, 16, 46, ".")
    P.road([(13, 44), (13, 46)], width=3, salt=12, bulge=False)
    P.box(12, 46, 12, 46, "#")
    P.box(16, 46, 16, 46, "#")
    return P


def build():
    rows = plan().rows()
    m = DMap(NAME, "parnassos", W, H)
    m.seam("up")
    get = paint(m, rows, salt=40)
    # white water: nobody swims the rapids, and nobody fishes them
    r = get("r")
    for (x, y) in r:
        side = "W" if (x - 1, y) not in r else "E" if (x + 1, y) not in r else "M"
        m.piece("rapids", side + ("2" if y % 2 else ""), x, y, solid=True)
    for (x, y) in get("F"):
        m.set(x, y, A.FALL, False)
    for (x, y) in get("b"):
        m.piece("camp_props", "bridge_EW", x, y, solid=False)
    m.scatter({c for c in get(".") if c[1] >= 6}, "ground", ["tuft", "pebbles", "stones", "thyme"], rate=170)
    # long grass grown up between the guy-ropes and along the west bank: nobody
    # in the muster has cut anything
    for y in range(27, 47):
        for x in list(range(4, 7)) + list(range(16, 25)):
            if int(m.mid[y, x]) == A.GRASS and not m.solid[y, x] and (x, y) not in ((5, 28), (5, 29)):
                m.set(x, y, A.TALL, False)
    for x in range(17, 25):                # the gorge's foot east of the lane: thicket
        m.piece("bush", "mastic" if x % 2 else "laurel", x, 46, solid=True)
    # the camp's tents and furniture
    for (k, x, y) in (("tent", 17, 34), ("tent", 21, 34), ("tent_small", 17, 38), ("tent", 20, 38),
                      ("tent_small", 23, 38), ("tent", 17, 42), ("tent", 21, 42)):
        m.put(k, x, y)
    m.part("camp_props", "oven_TL", 10, 31, 2, 2)
    m.piece("camp_props", "rack_W", 10, 33)
    m.piece("camp_props", "rack_E", 11, 33)
    m.piece("camp_props", "fire", 10, 34)
    m.piece("camp_props", "crates", 11, 34)
    m.put("tent_small", 10, 36)
    m.piece("camp_props", "crate", 10, 38)
    m.piece("camp_props", "crates", 11, 38)
    m.piece("camp_props", "banner_top", 12, 39)
    m.piece("camp_props", "banner", 12, 40)
    m.piece("camp_props", "banner_top", 16, 33)
    m.piece("camp_props", "banner", 16, 34)
    for x in (16,):
        for y in range(35, 46):
            if not m.solid[y, x]:
                pass
    m.put("tent_small", 22, 26)        # the quartermaster's tent
    m.piece("camp_props", "crate", 23, 28)
    # the west bank: the corral's fence and Chomas's fire
    for y in range(27, 33):
        m.set(4, y, A.WALL["M"], True)
    for x in (5, 6):
        m.set(x, 27, A.WALL["M"], True)
    m.piece("camp_props", "fire", 5, 37)
    m.piece("camp_props", "ash", 4, 38)
    # the great herm at the foot of the lower fall
    m.set(10, 16, A.HERM, True)
    m.cliff({(4, 12)}, edge_in=True)
    m.set(4, 12, A.SHADE, True)
    # the cutting's rock, east of Agrios
    m.cliff({(14, y) for y in range(23, 27)})
    m.border = [m.s("phaedriades")["ids"][1][1], m.s("phaedriades")["ids"][1][2],
                m.s("phaedriades")["ids"][2][1], m.s("phaedriades")["ids"][2][2]]
    m.border = [A.PINE_TOP[0], A.PINE_TOP[1], A.PINE_BOT[0], A.PINE_BOT[1]]
    events(m)
    m.break_runs(keep=get("p") | get("G") | get("."), longest=9)
    m.connect("down", -30, "MAP_ROUTE28_SACRED_OLIVES")
    m.connect("up", -26, "MAP_DELPHOI")
    return m, rows


def events(m):
    # signs
    m.set(16, 45, A.STELE, True)
    m.sign(16, 45, S + "SignFoot")
    m.sign(10, 16, S + "Herm")
    m.set(17, 2, A.STELE, True)
    m.sign(17, 2, S + "SignTop")
    # III-6B: the sentries
    for x in (13, 14, 15):
        m.trigger(x, 44, S + "Sentries", "VAR_TEMP_1", 1)
    npc(m, "ICHOR_TITAN_GRUNT", 13, 42, S + "Sentry1", face="down", local_id="LOCALID_GORGE_SENTRY_1")
    npc(m, "ICHOR_TITAN_GRUNT", 15, 42, S + "Sentry2", face="down", local_id="LOCALID_GORGE_SENTRY_2")
    # the camp's people (STORY §5's archetypes)
    npc(m, "ICHOR_MAN", 12, 32, S + "Cook", face="right")
    npc(m, "ICHOR_YOUTH_M", 6, 33, S + "Ochthos", face="left", flag="FLAG_ICHOR_HIDE_OCHTHOS_GORGE")
    npc(m, "ICHOR_KID_M", 15, 41, S + "Kid", face="left")
    npc(m, "ICHOR_WOMAN", 16, 37, S + "Mother", face="left")
    npc(m, "MOVEMENT_TYPE_NONE" if False else "ICHOR_SHEPHERD", 5, 29, S + "Corral", face="down")
    # trainers
    trainer(m, "ICHOR_TITAN_GRUNT", 12, 34, S + "Kisseris", "right", 3)
    trainer(m, "ICHOR_TITAN_GRUNT", 5, 36, S + "Chomas", "up", 1)
    trainer(m, "ICHOR_HOPLITE", 13, 23, S + "Agrios", "down", 4, local_id="LOCALID_GORGE_AGRIOS")
    trainer(m, "ICHOR_TITAN_GRUNT", 17, 12, S + "Asbolos", "left", 4)
    trainer(m, "ICHOR_PRIESTESS", 4, 10, S + "Chrysis", "right", 1)
    trainer(m, "ICHOR_TITAN_GRUNT", 14, 17, S + "Skaphe", "left", 3)
    trainer(m, "ICHOR_TITAN_GRUNT", 19, 30, S + "Twins", "left", 2)
    trainer(m, "ICHOR_TITAN_GRUNT", 20, 30, S + "Twins", "left", 2)
    # the cracked boulder: the shortcut down from the middle ledge
    m.obj("BREAKABLE_ROCK", 19, 14, "EventScript_RockSmash", flag="FLAG_ICHOR_GORGE_BOULDER")
    # items
    m.item_ball(22, 29, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_GORGE_MAX_ETHER")
    m.item_ball(5, 28, "ITEM_ETHER", "FLAG_ICHOR_ITEM_GORGE_ETHER")
    m.item_ball(18, 10, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_GORGE_REVIVE")
    m.item_ball(5, 44, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_GORGE_FULL_HEAL")
    m.item_ball(16, 3, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_GORGE_ULTRA_BALL")
    m.hidden(23, 28, "ITEM_FULL_RESTORE", "FLAG_ICHOR_HIDDEN_ITEM_GORGE_FULL_RESTORE")
    m.hidden(4, 12, "ITEM_MYSTIC_WATER", "FLAG_ICHOR_HIDDEN_ITEM_GORGE_MYSTIC_WATER")
    m.hidden(11, 18, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_GORGE_PEARL")
    m.hidden(6, 30, "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_ITEM_GORGE_NUGGET")


if __name__ == "__main__":
    m, rows = build()
    print("\n".join(rows))
    water = {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c in "~F"}
    m.build(NAME.lower(), starts=[(14, 46)], extra={(19, 14)} | water,
            views=[(14, 41), (12, 33), (13, 23), (11, 16), (12, 10), (12, 3)])
