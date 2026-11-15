#!/usr/bin/env python3
"""Build the Hellespont (aethos + troas): the sea lane between Thrace and the
Troad, its events, and its checks.

Writes data/layouts/Hellespont/map.bin and border.bin (64 x 34) and the events
in data/maps/Hellespont/map.json, then checks them (troad_lib.check_map, the
seams, the current, the swimmers' checkpoints).

The lane, west to east (OIKOUMENE.md §4.1; design/oikoumene/MAPS_troad.md):
  - the north shore is the Hebros Shore's strip of Thrace (COVERAGE T5): barley,
    Protesilaos's mound with its withered elms, the landing for Abdera, and the
    road up to Sestos, whose harbor opens on the north edge;
  - the middle is the current, running east in staggered races with slack water
    between them, so a surfer crossing it drifts east: cross upstream of where
    you mean to land. Helle's rock splits it;
  - the south shore is the Troad: Cape Sigeion with the mound of Achilles, the
    beach where the ships were drawn up (the road to the Skamander Plain leaves
    from it), and Rhoiteion with Ajax's mound.

Seams (BUILD.md §5; MAPS_troad.md, "Seams"):
  west  (x = 0)  Route 20, world-act2: rows 8-21 open sea; x 0-7 aethos only
  east  (x = 63) the Bosporus, pontos-towns: rows 8-21 open sea; x 56-63 aethos only
  north (y = 0)  Sestos, up, offset 28 (Sestos x 0-35 = here x 28-63): same tileset
  south (y = 33) the Skamander Plain, batch 2: the beach road x 24-27; rows 28-33 aethos only

Usage: /usr/bin/python3 tools/ichor/maps/hellespont.py [--render DIR] [--no-check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import troad_lib as T  # noqa: E402
from troad_lib import (BOULDER, FLOWERS, SEA, SEA_ROCK, STELE, Grid, behavior, hashed, hidden,  # noqa: E402
                       item_ball, obj, paint, sign, surfable)

W, H = 64, 34
NAME = "Hellespont"
LAYOUT = "LAYOUT_HELLESPONT"
SEAM_ROWS = range(8, 22)          # open sea on the west and east edges
SEA_STRIP = 8                     # aethos-only columns at each end
BEACH_ROAD = range(24, 28)        # the south edge's open road (the Skamander Plain)
SOUTH_STRIP = range(28, 34)       # aethos-only rows by the south seam
SESTOS_X = 28                     # Sestos's west edge, on this map's north edge
SESTOS_ROAD = range(30, 34)       # the road up to Sestos (Sestos x 2-5)
SESTOS_HARBOR = range(37, 56)     # Sestos's harbor mouth (Sestos x 9-27)
HEADLAND_ROAD = range(58, 61)     # the path down from Hero's point (Sestos x 30-32)
BAND = (14, 52, 11, 18)           # the current: x0, x1, y0, y1
ROCK = (30, 13)                   # Helle's rock, 3 x 2
ISLET = (37, 19, 41, 21)          # the sandbar
LANDING = 10                      # the Abdera landing stage's column


def is_gap(x, y):
    """Slack water inside the current: one cell in five, staggered two a row, plus
    the calm round Helle's rock."""
    rx, ry = ROCK
    if (x == rx - 1 or rx + 3 <= x <= rx + 4) and ry <= y <= ry + 1:
        return True
    return (x - 2 * y) % 5 == 0


CHECKPOINT_COLS = (35, 46)        # the band is full height here (the swimmers' narrows)


def band_rows(x):
    """The current's rows at column x: full in the middle of the strait, tapering
    toward both ends, its edges ragged by a row."""
    x0, x1, y0, y1 = BAND
    if not x0 <= x <= x1:
        return range(0)
    taper = max(0, 19 - x) // 2 + max(0, x - 47) // 2
    jt = 0 if x in CHECKPOINT_COLS else int(T.hashed(x, 0, 3) < 0.35)
    jb = 0 if x in CHECKPOINT_COLS else int(T.hashed(x, 1, 4) < 0.35)
    return range(y0 + taper + jt, y1 - taper - jb + 1)


def blob(P, rows, x0, y0, ch):
    """Paint an irregular patch from ASCII: '#' cells take ch."""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c == "#" and 0 <= y0 + j < H and 0 <= x0 + i < W:
                P[y0 + j][x0 + i] = ch


def plan():
    P = [["~"] * W for _ in range(H)]

    def fill(x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                P[y][x] = ch

    # ---- the north shore (Thrace): the strip, x 0-36, rows 0-7 -----------------
    fill(0, 0, 36, 5, "g")
    fill(2, 6, 33, 7, "s")
    fill(34, 6, 36, 6, "g")
    fill(0, 6, 1, 7, "g")
    # the beach widens and narrows: grass runs down to it in tongues
    for x in (6, 7, 14, 15, 16, 27, 28, 29):
        P[6][x] = "g"
    fill(3, 4, 33, 4, "p")                     # the shore road
    fill(30, 0, 33, 3, "p")                    # up to Sestos
    # barley: the forced band across the strip (x 19-21, its edges ragged), and
    # optional patches in the hollows, each with a reason to go in
    blob(P, ["###.", "####", "###.", "###.", "####"], 19, 2, "T")
    blob(P, [".###", "####", ".##."], 24, 1, "T")      # round the herdsman's nook
    blob(P, ["###", "##"], 25, 5, "T")
    blob(P, ["####", ".##"], 6, 2, "T")                # by the west end's Dive Ball
    blob(P, ["##", "#"], 16, 5, "T")
    fill(24, 2, 24, 2, "g")                    # the herdsman stands clear of it
    fill(23, 4, 23, 4, "p")
    # Sestos's headland, x 56-63, rows 0-7
    fill(56, 0, 63, 5, "g")
    fill(56, 6, 61, 7, "s")
    fill(62, 6, 63, 7, "g")
    fill(58, 0, 60, 3, "p")
    # ---- the current, with its slack water, and Helle's rock -----------------
    for x in range(BAND[0], BAND[1] + 1):
        for y in band_rows(x):
            P[y][x] = "~" if is_gap(x, y) else "c"
    rx, ry = ROCK
    fill(rx, ry, rx + 2, ry + 1, "B")
    # ---- the sandbar --------------------------------------------------------
    blob(P, [".###.", "#####", ".###"], ISLET[0], ISLET[1], "s")
    # ---- the south shore (the Troad) -------------------------------------------
    fill(0, 22, 13, 33, "g")
    fill(2, 22, 13, 22, "s")
    fill(45, 22, 63, 33, "g")
    fill(45, 22, 61, 22, "s")
    fill(45, 23, 47, 23, "s")
    # the bay and its beach, then a line of dune reeds behind it
    edge = {14: 22, 15: 23, 16: 24, 17: 25, 42: 25, 43: 24, 44: 23}
    for x in range(14, 45):
        top = edge.get(x, 25)
        fill(x, top, x, 27, "s")
        fill(x, 28, x, 33, "g")
    fill(12, 23, 13, 23, "s")
    fill(14, 28, 18, 28, "s")
    fill(40, 28, 44, 28, "s")
    for x in list(range(19, 24)) + list(range(28, 40)):
        if T.hashed(x, 28, 6) < 0.7:
            P[28][x] = "L"
    # the beach road south to the plain, and the shore paths
    fill(BEACH_ROAD.start, 27, BEACH_ROAD.stop - 1, 33, "p")
    fill(4, 28, 23, 28, "p")
    fill(4, 25, 5, 27, "p")
    fill(28, 29, 52, 29, "p")
    fill(52, 25, 53, 28, "p")
    # barley on the south shore: Sigeion's slope and Rhoiteion's
    blob(P, ["#####", ".####"], 7, 30, "T")
    blob(P, ["###", ".#"], 8, 23, "T")
    blob(P, ["##.", "###", "###"], 46, 25, "T")
    blob(P, [".###", "####"], 55, 30, "T")
    return P


def compose():
    g = Grid(W, H)
    P = plan()
    paint(g, P)

    # ---- the north shore --------------------------------------------------------
    # the Chersonese's wooded hills close the north edge; the road to Sestos and
    # the strip's west end stay open
    g.forest(0, 0, 7, 1, salt=1, aethos=True)
    g.forest(8, 0, 29, 1, salt=1)
    g.forest(0, 2, 2, 7, salt=2, aethos=True)
    g.forest(34, 0, 36, 6, salt=3)
    for x in range(34, 37):
        g.set(x, 7, SEA_ROCK[x % 2], True)      # the bluff runs into the water
    # the landing for Abdera: a timber stage out from the beach
    g.part("landing", "root", LANDING, 7)
    g.part("landing", "run", LANDING, 8)
    g.part("landing", "end", LANDING, 9)
    g.set(LANDING - 1, 6, STELE, True)            # ABDERA: the landing
    g.set(5, 3, STELE, True)                      # THE HELLESPONT (west end)
    g.set(29, 3, STELE, True)                     # the fork: Sestos north, the landing west
    # Protesilaos's mound at Elaious, its elms withered at the top
    g.put("mound", 13, 2)
    g.trees(elms=((12, 2), (16, 2), (17, 2), (11, 5)))
    # the narrows: rocks on the beach under the forced band, so it can't be skirted
    for x in range(19, 22):
        g.set(x, 7, 0x0E2, True)
    # a nook in the trees for the herdsman above the narrows at x 24
    g.trees(olives=((22, 2),), cypresses=((28, 2), (18, 2), (8, 5), (4, 5)), young=((10, 2),))
    g.scatter([(3, 3), (11, 3), (16, 3), (28, 5), (33, 5), (4, 2), (15, 5)])
    g.scatter([(18, 5), (26, 4), (31, 5), (9, 4)], ["chamomile", "dry_tuft", "stones"])
    # Sestos's headland: wooded to the east edge, a path down from Hero's point
    g.forest(61, 0, 63, 7, salt=4, aethos=True)
    g.forest(56, 0, 57, 3, salt=5, aethos=True)
    g.set(58, 5, STELE, True)                     # THE BOSPORUS (east end)
    g.scatter([(60, 4), (57, 5), (59, 5)])
    # ---- the lane ---------------------------------------------------------------
    rx, ry = ROCK
    g.put("helle_rock", rx, ry)
    for (x, y, k) in ((4, 11, 0), (3, 19, 1), (5, 19, 0), (60, 10, 0), (59, 18, 1), (61, 17, 0),
                      (47, 7, 0), (52, 4, 1), (40, 3, 0), (23, 23, 1), (45, 20, 1), (6, 15, 1),
                      (12, 20, 0), (54, 21, 1)):
        g.set(x, y, SEA_ROCK[k], True)
    # ---- the south shore ---------------------------------------------------------
    g.forest(0, 22, 2, 33, salt=6, aethos=True)
    g.forest(3, 31, 11, 33, salt=7, aethos=True)
    g.forest(12, 29, 22, 33, salt=8, aethos=True)
    g.forest(23, 31, 23, 33, salt=13, aethos=True)
    g.forest(28, 30, 51, 33, salt=9, aethos=True)
    g.forest(52, 30, 54, 33, salt=10, aethos=True)
    g.forest(59, 22, 63, 33, salt=11, aethos=True)
    g.forest(55, 32, 58, 33, salt=12, aethos=True)
    # Cape Sigeion: the mound of Achilles and Patroclus, an oak, the sign
    g.put("mound", 8, 25)
    g.trees(oaks=((11, 24),), cypresses=((7, 23), (12, 26)), olives=((5, 23),))
    g.set(3, 26, STELE, True)                     # SIGEION
    # Rhoiteion: Ajax's mound and its grove
    g.put("mound", 49, 24)
    g.trees(olives=((46, 23), (55, 23)), cypresses=((48, 24), (53, 23), (57, 26)),
            pines=((56, 28),))
    g.set(54, 25, STELE, True)                    # RHOITEION
    # the beach: the road's sign, the ships' old slipways marked by stones
    g.set(23, 30, STELE, True)                    # THE SKAMANDER PLAIN, ILION
    for (x, y) in ((19, 26), (31, 26), (36, 27)):
        g.set(x, y, 0x0E2, True)
    g.scatter([(6, 27), (9, 28), (5, 30), (47, 28), (50, 28), (58, 27), (26, 31)])
    g.scatter([(13, 25), (45, 26), (53, 27)], ["chamomile", "stones", "dry_tuft"])
    return g


def border():
    return [SEA, SEA, SEA, SEA]


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def events():
    pre = "Hellespont_EventScript_"
    swim = "OBJ_EVENT_GFX_SWIMMER_M"          # ICHOR_STUB_SPRITE: an Oikoumene swimmer
    swim_f = "OBJ_EVENT_GFX_SWIMMER_F"
    objects = [
        # swimmers in the calm water (elevation 1): Leander's would-be heirs
        obj(swim, 9, 14, pre + "Glaukippos", "LOCALID_HELLESPONT_GLAUKIPPOS", "MOVEMENT_TYPE_FACE_RIGHT",
            trainer="TRAINER_TYPE_NORMAL", sight=4, elevation=1),
        obj(swim_f, 35, 8, pre + "Nerea", "LOCALID_HELLESPONT_NEREA", "MOVEMENT_TYPE_FACE_DOWN",
            trainer="TRAINER_TYPE_NORMAL", sight=2, elevation=1),
        obj(swim, 46, 19, pre + "Euphemos", "LOCALID_HELLESPONT_EUPHEMOS", "MOVEMENT_TYPE_FACE_DOWN",
            trainer="TRAINER_TYPE_NORMAL", sight=3, elevation=1),
        obj(swim_f, 36, 19, pre + "Kyane", "LOCALID_HELLESPONT_KYANE", "MOVEMENT_TYPE_FACE_DOWN",
            trainer="TRAINER_TYPE_NORMAL", sight=3, elevation=1),
        obj(swim, 55, 14, pre + "Iphitos", "LOCALID_HELLESPONT_IPHITOS", "MOVEMENT_TYPE_FACE_LEFT",
            trainer="TRAINER_TYPE_NORMAL", sight=2, elevation=1),
        # the north strip: a Thracian herdsman over the narrows
        obj("OBJ_EVENT_GFX_ICHOR_SHEPHERD", 24, 2, pre + "Kotys", "LOCALID_HELLESPONT_KOTYS",
            "MOVEMENT_TYPE_FACE_DOWN", trainer="TRAINER_TYPE_NORMAL", sight=5),
        # the south shore: a hoplite at Achilles's mound, a charioteer at Ajax's
        obj("OBJ_EVENT_GFX_ICHOR_HOPLITE", 12, 28, pre + "Menestheus", "LOCALID_HELLESPONT_MENESTHEUS",
            "MOVEMENT_TYPE_FACE_LEFT", trainer="TRAINER_TYPE_NORMAL", sight=3),
        obj("OBJ_EVENT_GFX_ICHOR_HOPLITE", 51, 27, pre + "Thrasios", "LOCALID_HELLESPONT_THRASIOS",
            "MOVEMENT_TYPE_FACE_LEFT", trainer="TRAINER_TYPE_NORMAL", sight=3),
        # people
        obj("OBJ_EVENT_GFX_ICHOR_FISHER", 11, 6, pre + "LandingFisher", "LOCALID_HELLESPONT_FISHER",
            "MOVEMENT_TYPE_FACE_RIGHT"),
        obj("OBJ_EVENT_GFX_ICHOR_ELDER_M", 26, 31, pre + "BeachElder", "LOCALID_HELLESPONT_ELDER",
            "MOVEMENT_TYPE_FACE_UP"),
        obj("OBJ_EVENT_GFX_ICHOR_KID_F", 33, 26, pre + "BeachKid", "LOCALID_HELLESPONT_KID",
            "MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1),
        # items: the sandbar, the strip's west end, Rhoiteion's grove
        item_ball(39, 20, "ITEM_PEARL_STRING", "FLAG_ICHOR_ITEM_HELLESPONT_PEARL_STRING"),
        # gulls over the water
        obj("OBJ_EVENT_GFX_SPECIES(WINGULL)", 33, 12, move="MOVEMENT_TYPE_WALK_IN_PLACE_LEFT"),
        obj("OBJ_EVENT_GFX_SPECIES(WINGULL)", 17, 21, move="MOVEMENT_TYPE_WALK_IN_PLACE_RIGHT"),
        obj("OBJ_EVENT_GFX_SPECIES(WINGULL)", 49, 3, move="MOVEMENT_TYPE_WALK_IN_PLACE_LEFT"),
        item_ball(3, 2, "ITEM_DIVE_BALL", "FLAG_ICHOR_ITEM_HELLESPONT_DIVE_BALL"),
        item_ball(58, 29, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_HELLESPONT_MAX_REVIVE"),
    ]
    bgs = [
        sign(5, 3, pre + "WestSign"),
        sign(LANDING - 1, 6, pre + "AbderaLanding"),
        sign(29, 3, pre + "ForkSign"),
        sign(58, 5, pre + "EastSign"),
        sign(3, 26, pre + "SigeionSign"),
        sign(23, 30, pre + "BeachSign"),
        sign(54, 25, pre + "RhoiteionSign"),
        sign(14, 3, pre + "Protesilaos"),
        sign(9, 26, pre + "AchillesMound"),
        sign(50, 25, pre + "AjaxMound"),
        sign(ROCK[0], ROCK[1] + 1, pre + "HellesRock"),
        hidden(LANDING, 9, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_HELLESPONT_PEARL"),
        hidden(10, 25, "ITEM_RARE_CANDY", "FLAG_ICHOR_HIDDEN_HELLESPONT_RARE_CANDY"),
        hidden(ROCK[0] + 2, ROCK[1], "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_HELLESPONT_NUGGET", elevation=1),
    ]
    connections = [
        {"map": "MAP_SESTOS", "offset": SESTOS_X, "direction": "up"},
        # the Bosporus (pontos-towns): rows 8-21 open on both edges (BUILD.md §5)
        {"map": "MAP_BOSPORUS", "offset": 0, "direction": "right"},
    ]
    return objects, [], [], bgs, connections


# Where the player stands for each review crop, west to east.
SCREENS = {
    "1_west_end": (7, 12), "2_landing": (10, 5), "3_mound": (15, 4), "4_narrows": (22, 4),
    "5_fork": (30, 5), "6_rock": (31, 14), "7_sandbar": (39, 20), "8_sigeion": (8, 26),
    "9_beach": (25, 27), "10_rhoiteion": (51, 26), "11_harbor_mouth": (46, 6), "12_east_end": (58, 12),
}


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def lane_reach(blocks, start, cut=()):
    """Cells reached on the water alone. A current cell only lets a surfer go
    east; a calm one any way that is water."""
    from collections import deque
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        if behavior(int(blocks[y, x]) & 0x3FF) == "MB_EASTWARD_CURRENT":
            nxt = [(x + 1, y)]
        else:
            nxt = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for p in nxt:
            if p not in seen and p not in cut and surfable(blocks, *p):
                seen.add(p)
                q.append(p)
    return seen


def check():
    errors, reach, blocks, ev = T.check_map(
        NAME, start=(31, 0), surf=True,
        seams=(("cols", range(0, SEA_STRIP), "Route 20 (west)"),
               ("cols", range(W - SEA_STRIP, W), "Bosporus (east)"),
               ("rows", SOUTH_STRIP, "Skamander Plain (south)")))
    errors += T.check_edge(NAME, blocks, "left", set(SEAM_ROWS))
    errors += T.check_edge(NAME, blocks, "right", set(SEAM_ROWS))
    errors += T.check_edge(NAME, blocks, "bottom", set(BEACH_ROAD))
    errors += T.check_edge(NAME, blocks, "top", set(SESTOS_ROAD) | set(SESTOS_HARBOR) | set(HEADLAND_ROAD))
    for y in SEAM_ROWS:
        for x in (0, W - 1):
            if not surfable(blocks, x, y):
                errors.append(f"{NAME}: seam cell ({x},{y}) is not open sea")
    errors += T.check_current(NAME, blocks)
    # the current is between calm channels; no swimmer floats in it or right
    # east of a race (where a surfer carried into them would stick)
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if "WINGULL" in o["graphics_id"]:
            continue                             # gulls fly
        if behavior(int(blocks[y, x]) & 0x3FF) == "MB_EASTWARD_CURRENT":
            errors.append(f"{NAME}: {o.get('local_id')} floats in the current at ({x},{y})")
        if x > 0 and behavior(int(blocks[y, x - 1]) & 0x3FF) == "MB_EASTWARD_CURRENT":
            errors.append(f"{NAME}: {o.get('local_id')} at ({x},{y}) is just east of a race")
    # the crossing really drifts: every water cell on the far side is reached,
    # and going west is only possible in the two calm channels
    if (8, 20) not in lane_reach(blocks, (55, 9)):
        errors.append(f"{NAME}: no way west by water from the east end")
    # the checkpoints: Nerea's sight closes the north channel and Euphemos's the
    # south, so with both cut nobody swims west past them
    cut = set()
    for lid in ("LOCALID_HELLESPONT_NEREA", "LOCALID_HELLESPONT_EUPHEMOS"):
        o = next(o for o in ev["object_events"] if o.get("local_id") == lid)
        cut |= set(T.sight_cells(o)) | {(o["x"], o["y"])}
    if (8, 9) in lane_reach(blocks, (55, 9), cut) or (8, 20) in lane_reach(blocks, (55, 20), cut):
        errors.append(f"{NAME}: a swimmer can go west past both checkpoints unseen")
    # on foot, the strip's narrows are Kotys's
    if not T.blocks_path(blocks, ev, "LOCALID_HELLESPONT_KOTYS", (31, 4), (8, 4)):
        errors.append(f"{NAME}: the strip's road skirts Kotys's sight")
    # the forced band: the strip's road crosses the barley at x 19-21
    cutb = blocks.copy()
    for y in range(H):
        for x in range(19, 22):
            if behavior(int(blocks[y, x]) & 0x3FF) == "MB_TALL_GRASS":
                cutb[y, x] |= T.SOLID
    if (8, 4) in T.reachable(cutb, (31, 4)):
        errors.append(f"{NAME}: the strip's forced barley at x 19-21 can be walked round")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    g = compose()
    T.set_layout(LAYOUT, W, H)
    T.write_layout(g, NAME, border())
    objects, warps, coords, bgs, conns = events()
    T.write_events(NAME, objects, warps, coords, bgs, conns,
                   music="MUS_ICHOR_TRIREME", weather="WEATHER_SUNNY", map_type="MAP_TYPE_OCEAN_ROUTE")
    if args.render:
        T.render(LAYOUT, NAME, W, H, args.render, "hellespont", SCREENS)
    if not args.no_check:
        errors = check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("hellespont: layout and events written, checks pass")


if __name__ == "__main__":
    main()
