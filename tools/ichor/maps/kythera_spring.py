#!/usr/bin/env python3
"""MAP_KYTHERA_SPRING_OF_KALLIRHOE: the glade above the Foam Road (26 x 22).

design/phase4/SCRIPT.md Part 2 ("The Spring of Kallirhoe") and beat III-1E. A
round glade in the myrtle, reached by the stair from the Foam Road's fork (the
south edge, x 12-13, between the same myrtle hedges as the stair's foot).
Kallirhoe's pool in the middle, fed by a thin fall from a rock lip on the north
side and ringed with narcissus; the youth kneels at its south edge with a
Narcisheen beside him. The sea-grass grows in a horseshoe round the pool, open
to the south where the stair comes in. A rock stair in the north-east goes down
to Echo's caves. On the west, where the glade runs out to the sea-cliff, a
myrtle thicket (Demeter's Sickle) closes the back path to a little ledge over
the sea: a Miracle Seed and amphora #11's second sherd.

The seam with the Foam Road is exempt from MAP_DESIGN.md §5 (both kythera).

  /usr/bin/python3 tools/ichor/maps/kythera_spring.py [--no-render]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import A, Map  # noqa: E402

W, H = 26, 22
NAME = "KytheraSpringOfKallirhoe"
P = "KytheraSpringOfKallirhoe_EventScript_"
ENTRY = (12, 13)              # the stair from the Foam Road: the only open bottom-row tiles
FOAM_ROAD_STAIR_X = 41        # the Foam Road's stair starts at its x = 41, row 0
POOL = (11, 9)                # the 4x4 pool's top-left
CAVE_DOOR = (19, 5)           # the rock stair down to Echo's caves
TRIGGER_Y = 19                # Alethea's scene: the corridor's tiles on this row
CENTRE, RX, RY = (12.5, 11.0), 7.4, 5.9
SEA_X, SEA_ROWS = 2, range(0, 15)      # the sea under the west cliff
POCKET = {(x, y) for x in (3, 4) for y in range(9, 15)}     # the ledge over the sea, behind the thicket
THICKET = (5, 11)


def ell(x, y):
    return math.hypot((x - CENTRE[0]) / RX, (y - CENTRE[1]) / RY)


def glade_cells():
    """The round glade (walkable ground), the north-east nook under the cave's
    rock, and the corridor of the stair down to the Foam Road."""
    cells = {(x, y) for y in range(H) for x in range(W) if ell(x, y) <= 1.0}
    cells |= {(x, y) for x in range(16, 22) for y in range(5, 9)}
    cells |= {(x, y) for x in (12, 13) for y in range(16, H)}
    cells |= {(11, 16), (14, 16), (11, 17), (14, 17)}
    return cells


def compose():
    m = Map(NAME, "kythera", W, H, fill=A.GRASS)
    m.border = [A.SEA] * 4
    # A side area off the Foam Road, over Echo's caves: MAP_DESIGN §8.6 classes it with
    # the dungeons (as Kronion Hill is), not as a route of its own.
    m.header = {"music": "MUS_ICHOR_HOLLOW", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_ROUTE",
                "show_map_name": True, "allow_cycling": False, "allow_running": True, "ichor_kind": "dungeon"}
    glade = glade_cells()
    taken = set()

    # ---- the sea under the west cliff, and the cliff's foot round its end -------------------
    sea = {(x, y) for x in range(SEA_X) for y in SEA_ROWS}
    for (x, y) in sea:
        m.set(x, y, A.SEA, False)
    for y in SEA_ROWS:
        m.piece("cliff", "side_W", SEA_X, y)
    m.piece("cliff", "back", 0, SEA_ROWS[-1] + 1)
    m.piece("cliff", "back", 1, SEA_ROWS[-1] + 1)
    m.piece("cliff", "back_NE", SEA_X, SEA_ROWS[-1] + 1)
    taken |= sea | {(SEA_X, y) for y in SEA_ROWS} | {(x, SEA_ROWS[-1] + 1) for x in range(SEA_X + 1)}
    for name, x, y in (("tide_rock", 1, 4), ("tide_rocks", 0, 9), ("tide_rock", 1, 13)):
        m.piece("rocks", name, x, y)

    # ---- the north rock: a lip over the pool, the fall pouring from it -----------------------
    for x in range(9, 17):
        e = "_L" if x == 9 else ("_R" if x == 16 else "")
        m.piece("cliff", "lip" + e, x, 6)
        m.piece("cliff", "face" + e, x, 7)
        taken |= {(x, 6), (x, 7)}
    m.piece("cliff", "spring_lip", 12, 7)
    m.piece("falls", "thin_fall", 12, 8)
    for x in (10, 11, 13, 14, 15):
        m.piece("cliff", "foot_grass", x, 8)
    # the cave's rock, higher, to the north-east, the stair down set in its face
    for x in range(16, 22):
        e = "_L" if x == 16 else ("_R" if x == 21 else "")
        m.piece("cliff", "lip" + e, x, 3)
        m.piece("cliff", "face" + e, x, 4)
        taken |= {(x, 3), (x, 4)}
    m.piece("cave_stair", "cave_top", CAVE_DOOR[0], CAVE_DOOR[1] - 1)
    m.piece("cave_stair", "cave_stair", *CAVE_DOOR)
    for x in (16, 17, 18, 20, 21):
        m.piece("cliff", "foot_grass", x, 5)
    taken |= {(x, 5) for x in range(16, 22)}
    # behind the fall's lip, the rock's top: a little myrtle and briar
    for x in range(9, 17):
        for y in (4, 5):
            if (x, y) not in glade:
                taken.add((x, y))
    for name, x, y in (("bush", 10, 5), ("single", 15, 5), ("bush", 9, 4), ("single", 16, 2)):
        m.piece("myrtle", name, x, y)
    m.piece("flowers", "briar_L", 13, 5)
    m.piece("flowers", "briar_R", 14, 5)
    m.piece("flowers", "thrift", 11, 5)
    m.piece("flowers", "thrift", 12, 5)
    taken |= {(16, 2)}

    # ---- the ledge over the sea, behind the thicket -----------------------------------------
    m.piece("flowers", "thrift", 3, 9)
    m.piece("flowers", "thrift", 4, 14)
    m.piece("rocks", "rock_grass", 3, 14)
    m.rect(3, 11, 4, 12, A.SAND, False)
    m.piece("sand_decor", "sherd_dig", 3, 12)
    m.piece("sand_decor", "shells", 4, 11)

    # ---- the ring of myrtle round the glade, and the wood beyond it -------------------------
    # myrtle closes the ledge (its only way in is the thicket), and lines the stair's
    # corridor between the Foam Road's two hedges; the wood rings the rest
    ring = set()
    for (x, y) in POCKET:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1)):
            c = (x + dx, y + dy)
            if m.ok(*c) and c not in glade and c not in POCKET and c not in taken and c != THICKET:
                ring.add(c)
    ring |= {(11, y) for y in range(18, H)} | {(14, y) for y in range(18, H)}
    m.hedge(ring)
    m.set(THICKET[0], THICKET[1], A.GRASS, False)        # the thicket is an object (the Sickle)
    taken |= ring | glade | POCKET | {THICKET}
    m.woods({(x, y) for y in range(H) for x in range(W)} - taken, salt=5, from_bottom=True,
            singles=[("myrtle", "bush"), ("myrtle", "single"), ("flowers", "briar"), ("myrtle", "bush"),
                     ("rocks", "rock_grass")])

    # ---- the pool, its narcissus, the horseshoe of sea-grass -------------------------------
    m.put("spring_pool", *POOL)
    px, py = POOL
    # the horseshoe, drawn by hand: two arms that lean in at the top under the
    # rock and curl in at the foot toward the youth, open to the south
    west = ["..gg.", ".ggg.", "ggg..", "ggg..", "gggg.", ".ggg.", "..ggg", "...gg"]
    horseshoe = set()
    for j, row in enumerate(west):
        for i, ch in enumerate(row):
            if ch == "g":
                x, y = 6 + i, 8 + j
                horseshoe |= {(x, y), (25 - x, y)}
    horseshoe -= {(px + i, py + j) for i in range(4) for j in range(4)}
    narcissus = [(px - 1, py + j) for j in range(4)] + [(px + 4, py + j) for j in range(4)] + \
                [(px, py + 4), (px + 3, py + 4), (px - 1, py + 4), (px + 4, py + 4)]
    horseshoe -= set(narcissus)
    horseshoe -= {(9, 14)}                               # the scratched stone about the bulbs
    m.tallgrass(horseshoe)
    for k, (x, y) in enumerate(narcissus):
        m.piece("flowers", "narcissus" if k % 3 else "narcissus_b", x, y)
    m.piece("rocks", "rock_grass", 9, 14)
    for (x, y) in glade - horseshoe:
        if int(m.mid[y, x]) != A.GRASS:
            continue
        r = ell(x, y)
        k = (x * 7 + y * 13) % 11
        if r > 0.8 and k < 3:
            m.piece("flowers", "petals" if k else "thrift", x, y)
        elif r < 0.45 and k < 2:
            m.piece("flowers", "narcissus_b", x, y)

    # ---- the path up from the stair ---------------------------------------------------------
    m.path({(x, y) for x in (12, 13) for y in range(15, H)})
    return m


def events(m):
    tx = FOAM_ROAD_STAIR_X - ENTRY[0]
    m.connect("down", -tx, "MAP_KYTHERA_FOAM_ROAD")
    m.warp(CAVE_DOOR[0], CAVE_DOOR[1], "MAP_KYTHERA_ECHO_CAVES", 0)

    px, py = POOL
    m.obj("ICHOR_YOUTH_M", px + 1, py + 4, P + "Youth", "MOVEMENT_TYPE_FACE_UP",
          local_id="LOCALID_KALLIRHOE_YOUTH")
    m.obj("OBJ_EVENT_GFX_SPECIES(NARCISHEEN)", px + 2, py + 4, P + "Narcisheen", "MOVEMENT_TYPE_FACE_UP",
          local_id="LOCALID_KALLIRHOE_NARCISHEEN")
    m.obj("ICHOR_ALETHEA", 15, 16, P + "Alethea", "MOVEMENT_TYPE_FACE_UP",
          flag="FLAG_ICHOR_HIDE_ALETHEA_KALLIRHOE", local_id="LOCALID_KALLIRHOE_ALETHEA")
    m.obj("ICHOR_WOMAN", 10, 14, P + "Mother", "MOVEMENT_TYPE_FACE_UP",
          flag="FLAG_ICHOR_HIDE_KALLIRHOE_MOTHER", local_id="LOCALID_KALLIRHOE_MOTHER")
    m.obj("ICHOR_YOUTH_M", 15, 8, P + "Philotes", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2)
    m.obj("CUTTABLE_TREE", THICKET[0], THICKET[1], P + "Thicket", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_KALLIRHOE_MYRTLE_CUT", local_id="LOCALID_KALLIRHOE_THICKET")
    m.item_ball(3, 9, "ITEM_MIRACLE_SEED", "FLAG_ICHOR_ITEM_KALLIRHOE_MIRACLE_SEED")
    m.hidden(21, 6, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_KALLIRHOE_REVIVE")
    m.hidden(9, 8, "ITEM_PP_UP", "FLAG_ICHOR_HIDDEN_KALLIRHOE_PP_UP")

    m.sign(12, 8, P + "Fall")
    for y in (py + 1, py + 2):
        m.sign(px, y, P + "Pool")
        m.sign(px + 3, y, P + "Pool")
    m.sign(9, 14, P + "BulbStone")
    m.sign(3, 12, P + "DigSpot")
    for x in ENTRY:
        m.trigger(x, TRIGGER_Y, P + "AletheaScene", var="VAR_TEMP_1", value="1")


VIEWS = [(12, 19), (12, 14), (8, 11), (17, 10), (19, 6), (4, 11)]


def main():
    m = compose()
    events(m)
    # the ledge is behind the thicket (the Sickle): it opens when the thicket is cut
    m.forced_open.add(THICKET)
    must = [(19, 6, "the cave stair's foot"), (4, 10, "the ledge"), (9, 10, "the pool's west side"),
            (13, 8, "the fall's foot"), (21, 6, "the nook's corner")]
    errors = m.build("kythera_spring_of_kallirhoe", starts=[(12, H - 1), (13, H - 1)], must_reach=must,
                     views=VIEWS, render="--no-render" not in sys.argv)
    # the south seam: only the stair's two tiles are open on the bottom row
    for x in range(W):
        open_ = m.walkable(x, H - 1)
        if open_ != (x in ENTRY):
            print(f"{NAME} CHECK: bottom-row tile ({x},{H - 1}) is {'open' if open_ else 'shut'}")
            errors.append("seam")
    # the ledge is shut until the thicket is cut
    m.forced_open.discard(THICKET)
    if (4, 10) in m.reach([(12, H - 1)], blockers=[THICKET]):
        errors.append("the ledge behind the thicket is open without the Sickle")
        print(f"{NAME} CHECK: {errors[-1]}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
