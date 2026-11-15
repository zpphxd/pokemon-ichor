#!/usr/bin/env python3
"""Build the Bosporus, MAP_BOSPORUS (aethos + pontos): a sea lane, 56 x 34.

The lane, west to north-east:
  - The Hellespont joins on the west edge, rows 8-21 open sea (BUILD.md §5). The
    8 columns nearest that seam are aethos only (MAP_DESIGN §5): blue Aegean
    water between two little aethos beaches. From column 8 the water darkens to
    the Black Sea's green: the Bosporus is where the two seas meet.
  - The Propontis basin, with an islet and its beach, rocks with a jar in their
    lee, and a swimmer in plain view to start.
  - The European ridge splits the basin from the strait. Its only way through is
    the narrows south of the ridge's tip, where an Argonaut swims guard (a
    checkpoint the builder proves can't be skirted).
  - The strait runs north to the Clashing Rocks: two blue-black rocks standing
    open across the mouth, still since the Argo passed (Argonautica 2.549-606).
    A dove's feathers are caught in the west rock's face. East of the east rock
    the old side channel still twitches: visible, shut (stretch: the timing
    passage, OIKOUMENE §4.3).
  - On the ridge above the mouth, Zeus of the Fair Wind's altar (the Hieron,
    where sailors prayed for a wind into the Black Sea), reached from a beach.
  - North edge: Salmydessos's bay (x 14-22) and the strait's mouth onto the
    Pontic Coast (x 29-48).

Connections: left MAP_HELLESPONT offset 0; up MAP_SALMYDESSOS offset 0; up
MAP_PONTIC_COAST offset 28.

Usage: /usr/bin/python3 tools/ichor/maps/bosporus.py [--render DIR] [--shapes] [--plan]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pontos_map as M  # noqa: E402
from pontos_map import Grid, hidden, item_ball, obj, sign, swimmer  # noqa: E402

W, H = 56, 34
NAME, LAYOUT = "Bosporus", "LAYOUT_BOSPORUS"
SEAM_ROWS = range(8, 22)          # open to the Hellespont
SEAM_COLS = range(0, 8)           # aethos only
BAY = range(14, 23)               # Salmydessos's bay on the north edge
MOUTH = range(29, 49)             # the strait's mouth onto the Pontic Coast
PONTIC_OFFSET = 28


def plan():
    g = [["~"] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch

    def shape(x0, y0, rows, ch):
        """Rows of (first, last) column offsets from x0, from row y0 down."""
        for j, (a, b) in enumerate(rows):
            fill(x0 + a, y0 + j, x0 + b, y0 + j, ch)

    # the seam band: aethos land, a beach each side of the Hellespont's water
    fill(0, 0, 7, 6, ".")
    fill(0, 7, 7, 7, "s")
    fill(0, 8, 7, 21, "b")
    fill(0, 22, 7, 22, "s")
    fill(0, 23, 7, H - 1, ".")
    fill(6, 22, 7, 28, "s")
    # where the Aegean's blue meets the Black Sea's green: a line of current
    for y in range(9, 21):
        if y % 3 != 1:
            g[y][8] = "R"
    # the bay's west shore and the north-west land
    fill(8, 0, 13, 7, "c")
    fill(8, 6, 8, 7, "c")
    # the headland between the bay and the strait, and the European ridge below it
    fill(23, 0, 28, 10, "c")
    fill(24, 11, 33, 21, "c")
    fill(26, 22, 31, 22, "c")
    fill(23, 10, 23, 13, "c")
    # the Hieron's landing stage on the ridge's basin side
    fill(21, 14, 23, 17, "q")
    # the Asian shore, east of the strait
    fill(49, 0, W - 1, 26, "c")
    fill(45, 10, 48, 26, "c")
    # the Clashing Rocks, standing open across the mouth
    # both rocks one shape (so they share their pieces), the west one notched by
    # the dove's crack
    rock = [(1, 3), (0, 4), (0, 4), (0, 4), (0, 4), (0, 4), (1, 3)]
    shape(30, 2, rock, "k")
    shape(42, 2, rock, "k")
    # shoals between the west rock and the headland; the side channel's ends
    for y in (2, 4, 6):
        g[y][29] = "r"
    g[1][47] = g[1][48] = "r"
    g[8][47] = g[8][48] = "r"
    # the south shore, with a cove beach and the narrows above it
    fill(8, 31, W - 1, H - 1, "c")
    fill(26, 27, W - 1, 30, "c")
    fill(8, 29, 13, 30, "c")
    fill(17, 29, 21, 30, "s")
    # the islet in the basin, with its beach on the south side
    fill(13, 13, 17, 15, "c")
    fill(14, 12, 16, 12, "c")
    fill(13, 16, 17, 17, "s")
    # rocks awash: the basin and the strait
    for (x, y) in ((19, 22), (20, 22), (10, 26), (36, 15), (40, 19), (21, 9)):
        g[y][x] = "w"
    # rough water: the current in the narrows and the strait
    for (x, y) in ((27, 24), (28, 25), (33, 25), (34, 24), (38, 12), (39, 13), (37, 18), (41, 21),
                   (36, 5), (39, 4), (38, 1)):
        g[y][x] = "R"
    # the woods: wherever the land is two cells from the sea
    def far(x, y):
        return all(g[yy][xx] not in "~bRrw" for yy in range(max(0, y - 2), min(H, y + 3))
                   for xx in range(max(0, x - 2), min(W, x + 3)))
    for (x0, y0, x1, y1) in ((45, 0, W - 1, 26), (8, 31, W - 1, H - 1), (26, 27, W - 1, 30),
                             (8, 0, 13, 5), (24, 13, 33, 21)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if g[y][x] == "c" and far(x, y):
                    g[y][x] = "%"
    # a clearing on the ridge for the walk up to the Hieron
    for (x, y) in ((24, 15), (25, 15), (25, 14), (26, 14), (26, 13), (27, 12), (25, 16)):
        if g[y][x] == "%":
            g[y][x] = "c"
    return ["".join(r) for r in g]


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

B = "Bosporus_EventScript_"
P_ = "OBJ_EVENT_GFX_"

# ICHOR_STUB_SPRITE: intended OBJ_EVENT_GFX_ICHOR_ARGONAUT (a swimming Argonaut);
# the vanilla swimmers stand in, the only sprites drawn half in the water.
EVENTS = {
    "object_events": [
        # the first trainer: in plain view by the entrance, easy
        swimmer(P_ + "SWIMMER_M", 13, 10, B + "Butes", "MOVEMENT_TYPE_FACE_LEFT", 4),
        # the checkpoint: the narrows between the ridge's tip and the south shore
        swimmer(P_ + "SWIMMER_M", 29, 24, B + "Euphemos", "MOVEMENT_TYPE_FACE_DOWN", 2),
        # optional: the bay, on the way to Salmydessos
        swimmer(P_ + "SWIMMER_F", 18, 5, B + "Kyrene", "MOVEMENT_TYPE_FACE_DOWN", 3),
        # optional: under the Clashing Rocks, watching the passage
        swimmer(P_ + "SWIMMER_M", 37, 11, B + "Iphitos", "MOVEMENT_TYPE_FACE_RIGHT", 3),
        # a jar floating in the lee of the rocks
        item_ball(20, 23, "ITEM_DIVE_BALL", "FLAG_ICHOR_ITEM_BOSPORUS_DIVE_BALL", water=True),
        # on the islet's beach
        item_ball(15, 16, "ITEM_PEARL_STRING", "FLAG_ICHOR_ITEM_BOSPORUS_PEARL_STRING"),
        # in the narrows' rough water, past the swimmer
        item_ball(37, 20, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_BOSPORUS_ULTRA_BALL", water=True),
    ],
    "warp_events": [],
    "coord_events": [],
    "bg_events": [
        sign(9, 9, B + "SignWest"),                 # a sea-mark at the entrance
        sign(38, 2, B + "SignMouth"),               # a sea-mark between the rocks
        sign(32, 9, B + "Feathers"),                # the dove's feathers in the west rock
        sign(47, 1, B + "SideChannel"),             # ICHOR_STUB_STRETCH: the side channel
        sign(26, 3, B + "Altar"),                   # Zeus of the Fair Wind's altar
        sign(25, 4, B + "HieronStele"),
        hidden(27, 2, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_BOSPORUS_STAR_PIECE"),
        hidden(3, 22, "ITEM_BIG_PEARL", "FLAG_ICHOR_HIDDEN_BOSPORUS_BIG_PEARL"),
    ],
}

MANDATORY = {"Euphemos"}


def compose(shapes_only=False):
    g = Grid(NAME, plan(), shapes_only=shapes_only)
    g.paint()
    if shapes_only:
        return g
    # the seam band's land: olives and pines on aethos grass
    g.trees(olives=((0, 0), (4, 1), (2, 3), (5, 4)), pines=((1, 24), (3, 29)),
            cypresses=((7, 1), (3, 5), (4, 25), (0, 28), (5, 31), (1, 32)))
    g.trees(olives=((0, 30), (3, 32)))
    g.set(6, 5, M.STELE, True)                     # THE BOSPORUS (from the Hellespont side)
    g.flowers([(1, 2), (6, 2), (2, 26), (5, 27), (3, 34)])
    # sea-marks: the lane's signs, read from the water
    g.put("sea_mark", 9, 9)
    g.put("sea_mark", 38, 2)
    # the feathers in the west rock's south face (a face cell under the rock)
    g.put("kyanean_feathers", 32, 9)
    # the side channel: its south mouth shut by rocks that still shiver
    g.put("kyrocks", 47, 8)
    g.put("kyrocks", 48, 8)
    # the Hieron: Zeus of the Fair Wind's altar on the ridge over the mouth
    g.block([[M.TRIPOD[0]], [M.TRIPOD[1]]], 26, 2)
    g.set(26, 2, M.TRIPOD[0], True)
    g.set(25, 4, M.STELE, True)
    g.woods()
    g.trees(oaks=((24, 6),), hazels=((27, 8), (24, 2)))
    g.flowers([(25, 2), (28, 5), (25, 16), (26, 9), (27, 4)])
    return g


def border(g):
    sea = g.k("psea")
    return [sea, sea, sea, sea]


SCREENS = {"1_hellespont": (6, 14), "2_basin": (14, 18), "3_islet": (15, 15), "4_narrows": (29, 24),
           "5_strait": (40, 15), "6_rocks": (38, 6), "7_hieron": (25, 4), "8_bay": (18, 3)}


def connections():
    return [{"map": "MAP_HELLESPONT", "offset": 0, "direction": "left"},
            {"map": "MAP_SALMYDESSOS", "offset": 0, "direction": "up"},
            {"map": "MAP_PONTIC_COAST", "offset": PONTIC_OFFSET, "direction": "up"}]


def check():
    starts = [(0, y) for y in SEAM_ROWS]
    errors, r, blocks = M.check_map(NAME, starts, seams=(("cols", SEAM_COLS, "Hellespont (west)"),))
    for y in range(H):
        k = M.cell_kind(blocks, 0, y)
        if (k == "water") != (y in SEAM_ROWS):
            errors.append(f"{NAME}: west seam row {y} is {k}")
    for x in range(W):
        k = M.cell_kind(blocks, x, 0)
        want = x in BAY or x in MOUTH
        if (k == "water") != want:
            errors.append(f"{NAME}: north edge column {x} is {k}")
    for goal, why in (([(x, 0) for x in MOUTH], "the mouth"), ([(x, 0) for x in BAY], "the bay")):
        if not any(gl in r for gl in goal):
            errors.append(f"{NAME}: no way from the Hellespont to {why}")
    ev = EVENTS["object_events"]
    for t in ev:
        if t["trainer_type"] == "TRAINER_TYPE_NORMAL" and t["script"].split("_")[-1] in MANDATORY:
            ok, line = M.check_checkpoint(NAME, blocks, t, starts, [(x, 0) for x in MOUTH])
            print(f"  {t['script']} at ({t['x']},{t['y']}) sees {line}: "
                  + ("a checkpoint" if ok else "CAN be skirted"))
            if not ok:
                errors.append(f"{NAME}: {t['script']}'s line can be skirted")
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
    M.write_events(NAME, dict(EVENTS, connections=connections()), music="MUS_ICHOR_TRIREME",
                   weather="WEATHER_SHADE", map_type="MAP_TYPE_OCEAN_ROUTE")
    if args.render:
        M.render(LAYOUT, NAME, args.render, "bosporus", SCREENS)
    errors = check()
    for e in errors:
        print("CHECK:", e)
    if errors:
        sys.exit(1)
    print("bosporus: layout written, checks pass")


if __name__ == "__main__":
    main()
