#!/usr/bin/env python3
"""MAP_KYTHERA_SPRING_OF_KALLIRHOE: the glade above the Foam Road (26 x 22).

design/phase4/SCRIPT.md Part 2 ("The Spring of Kallirhoe") and beat III-1E. A
round glade in the myrtle, reached by the stair from the Foam Road's fork (the
south edge, x 12-13). Kallirhoe's pool in the middle, fed by a thin fall from a
rock lip on the north side and ringed with narcissus; the youth kneels at its
south edge with a Narcisheen beside him. Grass grows in a horseshoe round the
pool. A rock stair in the north-east goes down to Echo's caves. On the west, a
myrtle thicket (Demeter's Sickle) closes the back path to a little ledge over
the sea: a Miracle Seed and amphora #11's second sherd.

The seam with the Foam Road is exempt from MAP_DESIGN.md §5 (both kythera).

  /usr/bin/python3 tools/ichor/maps/kythera_spring.py [--no-render]
"""
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


RING_PIECE = {  # myrtle piece by which ring neighbours (N, E, S, W) are myrtle too
    (0, 1, 0, 1): "M", (1, 0, 1, 0): "V", (0, 1, 0, 0): "L", (0, 0, 0, 1): "R",
    (0, 0, 1, 0): "T", (1, 0, 0, 0): "B", (0, 1, 1, 0): "NW", (0, 0, 1, 1): "NE",
    (1, 1, 0, 0): "SW", (1, 0, 0, 1): "SE", (0, 0, 0, 0): "single",
}


def glade_cells():
    """The round glade (walkable ground), the north-east nook under the cave's
    rock, the funnel and the stair corridor down to the Foam Road."""
    cells = set()
    for y in range(H):
        for x in range(W):
            if ((x - 12.5) / 6.6) ** 2 + ((y - 11.2) / 6.0) ** 2 <= 1.0:
                cells.add((x, y))
    cells |= {(x, y) for x in range(16, 22) for y in range(5, 9)}
    cells |= {(x, y) for x in (12, 13) for y in range(16, H)}
    cells |= {(11, 16), (14, 16), (10, 15), (15, 15)}
    return cells


POCKET = {(x, y) for x in (3, 4) for y in range(9, 15)}     # the ledge over the sea, behind the thicket
THICKET = (5, 11)


def myrtle_ring(m, glade, taken):
    ring = set()
    for (x, y) in glade | POCKET:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                c = (x + dx, y + dy)
                if m.ok(*c) and c not in glade and c not in POCKET and c not in taken:
                    ring.add(c)
    for (x, y) in ring:
        key = tuple(int(c in ring) for c in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)))
        name = RING_PIECE.get(key)
        if name is None:
            name = "M" if key[1] and key[3] else "V"
        if name == "M" and (x * 7 + y) % 5 == 0:
            name = "M2"
        m.piece("myrtle", name, x, y)
    return ring


def _hash(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000


def woods(m, free, salt=0):
    """Fill `free` with an uneven wood: olives and the odd stone pine placed in a
    shuffled order (so no two rows line up), cypresses in the gaps they leave,
    then myrtle bushes, briar and a rock in the last single cells."""
    free = set(free)
    spots = sorted(((x, y) for y in range(-1, H) for x in range(W)), key=lambda c: _hash(*c, salt))
    for (x, y) in spots:
        cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        if not all(c in free for c in cells):
            continue
        if _hash(x, y, salt + 1) < 140:
            m.pine(x, y)
        else:
            m.olive(x, y)
        free -= set(cells)
        free.discard((x, y - 1))
        free.discard((x + 1, y - 1))
    for (x, y) in sorted(free, key=lambda c: _hash(*c, salt + 2)):
        if (x, y) in free and (x, y + 1) in free:
            m.cypress(x, y)
            free -= {(x, y), (x, y + 1)}
    for (x, y) in sorted(free):
        r = _hash(x, y, salt + 3) % 6
        if r < 3:
            m.piece("myrtle", "bush", x, y)
        elif r < 5:
            m.piece("flowers", "briar", x, y)
        else:
            m.piece("rocks", "rock_grass", x, y)


def compose():
    m = Map(NAME, "kythera", W, H, fill=A.GRASS)
    m.border = [A.SEA] * 4
    m.header = {"music": "MUS_ICHOR_HOLLOW", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_ROUTE",
                "show_map_name": True, "allow_cycling": False, "allow_running": True}
    glade = glade_cells()
    taken = set()

    # ---- the sea to the west, under a sea-cliff ---------------------------------------------
    for y in range(H):
        m.set(0, y, A.SEA, False)
        m.set(1, y, A.SEA, False)
        m.piece("cliff", "side_W", 2, y)
        taken |= {(0, y), (1, y), (2, y)}
    # and to the east: the glade sits on a headland, the sea both sides of it
    for y in range(H):
        m.set(24, y, A.SEA, False)
        m.set(25, y, A.SEA, False)
        m.piece("cliff", "side_E", 23, y)
        taken |= {(23, y), (24, y), (25, y)}
    m.piece("rocks", "tide_rocks", 25, 8)
    m.piece("rocks", "tide_rock", 24, 15)
    m.piece("rocks", "tide_rock", 1, 6)
    m.piece("rocks", "tide_rocks", 0, 12)
    m.piece("rocks", "tide_rock", 1, 18)

    # ---- the north rock: a lip over the pool, the fall pouring from it ----------------------
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
    # behind the fall's lip, the rock's top: grass and a little myrtle
    for x in range(9, 17):
        for y in (4, 5):
            if (x, y) not in glade:
                taken.add((x, y))
    m.piece("myrtle", "bush", 10, 5)
    m.piece("flowers", "briar_L", 13, 5)
    m.piece("flowers", "briar_R", 14, 5)
    m.piece("flowers", "thrift", 11, 5)
    m.piece("myrtle", "single", 15, 5)
    m.piece("myrtle", "bush", 9, 4)
    m.piece("myrtle", "single", 16, 2)
    taken |= {(16, 2)}

    # ---- the ledge over the sea, behind the thicket -----------------------------------------
    m.piece("flowers", "thrift", 3, 9)
    m.piece("flowers", "thrift", 4, 14)
    m.piece("rocks", "rock_grass", 3, 14)
    m.rect(3, 11, 4, 12, A.SAND, False)
    m.piece("sand_decor", "sherd_dig", 3, 12)
    m.piece("sand_decor", "shells", 4, 11)

    # ---- the ring of myrtle round the glade, and the wood beyond it -------------------------
    ring = myrtle_ring(m, glade, taken | {THICKET})
    m.set(THICKET[0], THICKET[1], A.GRASS, False)        # the thicket is an object (the Sickle)
    taken |= ring | glade | POCKET | {THICKET}
    woods(m, {(x, y) for y in range(H) for x in range(W)} - taken)

    # ---- the pool, its narcissus, the youth's patch -----------------------------------------
    m.put("spring_pool", *POOL)
    px, py = POOL
    ring2 = [(px - 1, py + j) for j in range(4)] + [(px + 4, py + j) for j in range(4)] + \
            [(px, py + 4), (px + 3, py + 4), (px - 1, py + 4), (px + 4, py + 4)]
    for k, (x, y) in enumerate(ring2):
        m.piece("flowers", "narcissus" if k % 3 else "narcissus_b", x, y)

    # ---- the horseshoe of sea-grass round the pool ------------------------------------------
    m.blob("seagrass", ["..##...",
                        ".###...",
                        "####...",
                        "###....",
                        "###....",
                        "####...",
                        ".####..",
                        "..###.."], 5, 8, edge_in=False)
    m.blob("seagrass", ["...##..",
                        "...###.",
                        "...####",
                        "....###",
                        "....###",
                        "...####",
                        "..####.",
                        "..###.."], 14, 8, edge_in=False)
    for x, y in ((7, 6), (6, 7)):
        m.piece("flowers", "petals", x, y)
    for x, y in ((9, 16), (16, 16), (8, 8), (17, 8)):
        m.piece("flowers", "petals", x, y)
    for x, y in ((10, 15), (15, 15), (7, 15), (18, 7)):
        m.piece("flowers", "thrift", x, y)
    m.piece("rocks", "rock_grass", 9, 14)          # the scratched stone about the bulbs

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

    m.sign(12, 8, P + "Fall")
    for y in (py + 1, py + 2):
        m.sign(px, y, P + "Pool")
        m.sign(px + 3, y, P + "Pool")
    m.sign(9, 14, P + "BulbStone")
    m.sign(3, 12, P + "DigSpot")
    for x in ENTRY:
        m.trigger(x, TRIGGER_Y, P + "AletheaScene", var="VAR_TEMP_1", value="1")


VIEWS = [(12, 19), (12, 14), (8, 11), (17, 10), (19, 6), (3, 11)]


def main():
    m = compose()
    events(m)
    # the ledge is behind the thicket (the Sickle): it opens when the thicket is cut
    m.forced_open.add(THICKET)
    must = [(19, 6, "the cave stair's foot"), (4, 10, "the ledge"), (10, 10, "the pool's west side"),
            (13, 8, "the fall's foot")]
    errors = m.build("kythera_spring_of_kallirhoe", starts=[(12, H - 1), (13, H - 1)], must_reach=must,
                     views=VIEWS, render="--no-render" not in sys.argv)
    # the south seam: only the stair's two tiles are open on the bottom row
    for x in range(W):
        open_ = m.walkable(x, H - 1)
        if open_ != (x in ENTRY):
            print(f"{NAME} CHECK: bottom-row tile ({x},{H - 1}) is {'open' if open_ else 'shut'}")
            errors.append("seam")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
