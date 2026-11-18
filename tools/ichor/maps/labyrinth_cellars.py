"""The Labyrinth's cellars (MAP_LABYRINTH_CELLARS; design/maps/Labyrinth_System.md):
nine small sealed rooms under the upper rings, each reached by a side stair
down from a dead end, each with treasure. Room 7 has a hole into room 8,
whose stair comes up somewhere else entirely: Ring IV's dig.

Room r's warps: 3r the arrival (the ring's stair lands here), 3r+1 and 3r+2 its
stair back up, to the ring arrival recorded in labyrinth_cellars.json by the
ring builders (labyrinth_extras.cellar_entries). Build the rings first.
"""
from __future__ import annotations

import json
from pathlib import Path

from labyrinth_lib import LMap

NAME = "LabyrinthCellars"
W, H = 28, 25
P = NAME + "_EventScript_"
REG = Path(__file__).resolve().parent / "labyrinth_cellars.json"
TREASURE = [  # (item, what the room was)
    ("ITEM_PP_UP", "a steward's strongroom, its shelves bare but one"),
    ("ITEM_RELIC_GOLD", "a cist of the old kings' coin"),
    ("ITEM_RARE_CANDY", "a pantry of honey jars, long dry"),
    ("ITEM_TM_PSYCHIC", "a scribe's cell, its tablets crumbled"),
    ("ITEM_COMET_SHARD", "a sump where something bright fell through the roof"),
    ("ITEM_TM_FLAMETHROWER", "the Titans' powder store"),
    ("ITEM_PP_MAX", "a cave pocket the Titans never found"),
    ("ITEM_STAR_PIECE", "a drain; the floor gives at the back"),
    ("ITEM_TM_EARTHQUAKE", "the deepest sump, two drops down"),
]


def build(render=True):
    from labyrinth_upper import DARK
    reg = json.loads(REG.read_text())
    m = LMap(NAME, W, H, dict(DARK, show_map_name=False))
    rooms = []
    for r in range(9):
        c, rr = r % 3, r // 3
        x0, y0 = 1 + c * 9, 1 + rr * 8
        ch = "." if r < 4 else ","
        for y in range(y0 + 2, y0 + 6):
            for x in range(x0 + 1, x0 + 7):
                m.g[y][x] = ch
        rooms.append((x0, y0))
    m.g0 = [row[:] for row in m.g]
    m.lay()
    for r, (x0, y0) in enumerate(rooms):
        if m.at(x0 + 3, y0 + 1) == "#":
            m.stairs(x0 + 3, y0 + 1, "up")
        else:
            m.named("stairs", "up_l", x0 + 3, y0 + 1, False)
            m.named("stairs", "up_r", x0 + 4, y0 + 1, False)
            m.stops |= {(x0 + 3, y0 + 1), (x0 + 4, y0 + 1)}
        back = reg.get(str(r))
        if r == 8:
            back = ["MAP_LABYRINTH_RING4", 3]          # up into Ring IV's dig, not where you came in
        dest, wid = back if back else [f"MAP_{'LABYRINTH_CELLARS'}", 3 * r]
        m.arrival(x0 + 3, y0 + 2)
        m.warp(x0 + 3, y0 + 1, dest, wid)
        m.warp(x0 + 4, y0 + 1, dest, wid)
        item, what = TREASURE[r]
        m.item(x0 + 5, y0 + 4, item, f"FLAG_ICHOR_ITEM_CELLAR_{r + 1}")
        m.sign(x0 + 1, y0 + 1, P + f"Room{r}")
        m.extra_scripts = getattr(m, "extra_scripts", []) + [
            "", f"script {P}Room{r} {{", f"    msgbox(format(\"A sealed room under the house: {what}.\"), MSGBOX_SIGN)", "}"]
    # room 7's floor gives into room 8
    x7, y7 = rooms[7]
    m.put("hole", x7 + 1, y7 + 5)
    m.stops.add((x7 + 1, y7 + 5))
    m.trigger(x7 + 1, y7 + 5, P + "Drop")
    m.extra_scripts += ["", f"script {P}Drop {{", "    lockall",
                        '    msgbox(format("The floor at the back gives way!"), MSGBOX_DEFAULT)', "    closemessage",
                        "    playse(SE_FALL)", "    warp(MAP_LABYRINTH_CELLARS, 24)", "    waitstate", "}"]
    m.gen = []
    starts = [(x0 + 3, y0 + 2) for (x0, y0) in rooms]
    m.header["ichor_kind"] = "interior"
    m.build("labyrinth_cellars", starts, views=[(13, 12)], render=render)


if __name__ == "__main__":
    import sys
    build(render="--no-render" not in sys.argv)
