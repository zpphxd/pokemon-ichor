"""Minos's tomb (design/LABYRINTH.md §6 Ring V and scene F,
design/maps/LabyrinthMinosTomb.md): a low painted chamber behind Ring V's
cracked wall, with the judge's bier and the Helm of Darkness on it. Modelled on
the Temple Tomb south of Knossos: a pillared crypt cut half into the rock, red
columns, gypsum, and the double axe on its stands either side of the bier.
"""
from __future__ import annotations

from labyrinth_lib import LMap, mid, ST
import labyrinth_tiles as LT

NAME = "LabyrinthMinosTomb"
W, H = 16, 12
P = NAME + "_EventScript_"

PLAN = [
    "################",
    "################",
    "################",
    "##............##",
    "##............##",
    "##............##",
    "#%,..........,%#",
    "#%,,........,,%#",
    "#%%,,......,,%%#",
    "##%%,......,%%##",
    "###%%%....%%%###",
    "################",
]


def build(render=True):
    from labyrinth_upper import DARK
    hdr = dict(DARK)
    hdr.update({"music": "MUS_ICHOR_HOLLOW", "show_map_name": False})
    m = LMap(NAME, W, H, hdr)
    m.g = [list(r) for r in PLAN]
    m.g0 = [row[:] for row in m.g]
    m.lay()
    # the inscription over the bier, in the north face
    for i, n in enumerate(("l", "m", "r")):
        m.named("tomb_inscription", n, 6 + i, 2)
    m.put("tomb_bier", 6, 3, cells={(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)})
    for x in (3, 12):
        m.put("tomb_pillar", x, 3)
        m.put("tomb_pillar", x, 6)
    m.put("tomb_goods", 5, 3, cells={(0, 0), (0, 1)})          # a labrys stand west of the bier
    m.put("tomb_goods", 9, 3, cells={(0, 0), (0, 1)})          # ...and east
    m.put("tomb_goods", 10, 3, cells={(1, 0)})                  # a jar
    m.put("tomb_goods", 9, 5, cells={(1, 0)})
    # the way back out: the threshold in the south
    m.named("edge", "sill_l", 7, 10, False)
    m.named("edge", "sill_r", 8, 10, False)
    m.stops |= {(7, 10), (8, 10)}
    m.warp(7, 10, "MAP_LABYRINTH_RING5", 1)
    m.warp(8, 10, "MAP_LABYRINTH_RING5", 1)
    for x in (6, 7, 8):
        m.sign(x, 4, P + "Bier")
    m.item(11, 5, "ITEM_RELIC_GOLD", "FLAG_ICHOR_ITEM_TOMB_GOLD_STATER")
    head = mid("tomb_bier", "head_empty")
    m.gen = ["if (flag(FLAG_ICHOR_GOT_HELM_OF_DARKNESS)) {", f"    setmetatile(6, 3, 0x{head:03X}, TRUE)", "}"]
    m.anchor(7, 8, "THREAD_ANCHOR_UNNAMED")
    m.hidden(5, 5, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_TOMB_PEARL")
    m.hidden(9, 5, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_TOMB_OBOL")
    m.header["ichor_kind"] = "interior"     # one chamber off Ring V, not a dungeon of its own
    errs, reach = m.build("labyrinth_minos_tomb", [(7, 9)], views=[(7, 5)], render=render)
    return errs


if __name__ == "__main__":
    import sys
    build(render="--no-render" not in sys.argv)
