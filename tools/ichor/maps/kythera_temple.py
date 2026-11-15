#!/usr/bin/env python3
"""MAP_KYTHERA_TEMPLE_OF_APHRODITE: Galatea's Gallery (design/phase4/SCRIPT.md
beat III-1G and Part 5), on the oikos primary and the temple_aphrodite
secondary (design/phase4/TILES_temple_aphrodite.md). 21 x 36.

Three rooms one behind the other, each larger than the last, entered from the
south: the pronaos (teach), the gallery (test) and the rose court (master), with
Galatea's dais at the court's north end.

- Statues are object events with the engine's MOVEMENT_TYPE_ICHOR_STATUE types
  (src/ichor_statue.c). Only the room the player is in has live statues: the map
  script gives the others a still FACE type and puts them back on their plinths
  whenever the player steps into a room (scripts.pory, Gallery_SetRoom).
- Every mirror is an object with a MOVEMENT_TYPE_ICHOR_MIRROR type. The wall
  mirrors (M0, W1, W2) are invisible markers on their wall tiles, over the
  metatile that draws them; the rose court's stands (P1 fixed, P2 and P3
  turnable) are bronze sprites whose frame shows which way they point.

The rite is checked here against gallery_sim.py, a model of the engine's step.
The statues chase whoever doesn't watch them, so the danger is the one coming
from ahead: sentries on short ranges guard the tempting routes, and trailers
let out of their niches behind you freeze in the mirrors on the right route.
- pronaos (teach): the walk up to the door is safe; walking back is not;
- gallery (test): up the west aisle facing W1 and along the north aisle facing W2
  is safe; the east route past the hall's sentries is touched;
- rose court (master): up the east lane, P2 turned to face down it, and along the
  north walk facing P1 is safe; the garden lane between the sentries is touched.
The routes are written to tools/ichor/tests/act3_galatea_routes.lua for the test.

  /usr/bin/python3 tools/ichor/maps/kythera_temple.py [--no-render]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import ROOT, Map  # noqa: E402
from gallery_search import plain_route  # noqa: E402
from gallery_sim import Sim, Statue  # noqa: E402

NAME = "KytheraTempleOfAphrodite"
P = "KytheraTempleOfAphrodite_EventScript_"
W, H = 21, 36

# --------------------------------------------------------------------------------------
# The plan, one character a cell (LEGEND below). The dais is placed in code over the
# 'a' cells; beds ('#') take their kerbs from their neighbours.
# --------------------------------------------------------------------------------------
PLAN = [
    #012345678901234567890
    "[<TTTTTTTTTTTTTTTTT>]",  # 0   the court's back wall
    "[FFFFFFFFFFFFFFFFFFF]",  # 1
    "{LLLLLLLLaaaaLLLLLLL}",  # 2   the dais's awning (9..12)
    "[%%%%####aaaa&&&&%%%]",  # 3   Galatea on the dais's stand (10,3)
    "[%%%%####aaaa&&&&%%%]",  # 4   the dais's steps
    "[#ooo####iiii&&V&Y%%]",  # 5   Anthousa's alcove; the inlay; P3 (15,5); P2 (17,5)
    "[Zggggggggoooogggg%%]",  # 6   the north walk; P1 (1,6); petals before the dais
    "[###&&&&%%%%&&&g#g##]",  # 7   the garden lane (15) and the east lane (17)
    "[###&u&&%%%%&ggg#g#u]",  # 8   S8's pocket (13..14, 8)
    "[###&&&&%%%%&&&g#ggg]",  # 9   S7's way out of its niche (18..19, 9)
    "[%%%%####&&&&ggg#g#g]",  # 10  S9's pocket (13..14, 10); S7's niche (19,10)
    "[%u%%####&u&&&&g#g##]",  # 11
    "[%%%%####&&&&&&ggg##]",  # 12  the south walk; the doorway's step (16,12)
    "[PWPPPPPPPPPPPPPdPPP]",  # 13  the partition; W1's top; the doorway (16,13)
    "{(wLLLLLLLLLLLLLDLL)}",  # 14  W1 (2,14); the doorway (16,14)
    " [.................E ",  # 15  the north aisle; W2 (19,15)
    " [.CCCCCCCCCCCCCpC.] ",  # 16  the colonnade; Rhodanthe's niche (16,16)
    " [.ccccccccccccccc.] ",  # 17
    " [...q...q...q.....] ",  # 18  the hall; roses laid on empty plinths
    " [.................] ",  # 19
    " [.................] ",  # 20
    " [.................] ",  # 21
    " [........b...b....] ",  # 22  marble benches along the south wall
    " [PPMdPPPPPPPPPPPPP] ",  # 23  M0's top (4,23); the doorway (5,23)
    "   {mDR}             ",  # 24  M0 (4,24); the doorway (5,24); the fresco (6,24)
    "   [...]             ",  # 25
    " <TT...]             ",  # 26  the niche's cornice
    " [LL.i.]             ",  # 27  the niche's back wall; a scallop in the floor
    " [.....]             ",  # 28  S1's niche (2..3,28)
    " [pb...]             ",  # 29  S1 on its plinth (2,29); a bench (3,29)
    " [PP...]             ",  # 30
    "   [.i.]             ",  # 31  a scallop inlaid in the floor
    "   [...]             ",  # 32
    "   [..A]             ",  # 33  the dove altar (6,33); Charis above it (6,32)
    "   [...]             ",  # 34
    "    [x]              ",  # 35  the entrance step (5,35)
]

WALLS = {"[": "side_L", "]": "side_R", "{": "side_L_low", "}": "side_R_low", "<": "top_L", ">": "top_R",
         "T": "top", "L": "lower", "R": "fresco", "P": "part", "d": "door_top", "D": "door",
         "(": "inner_L", ")": "inner_R"}
MIRROR_TILES = {"M": "mirror_tall_top", "m": "mirror_tall", "W": "mirror_N_top", "w": "mirror_N", "E": "mirror_E"}
FLOORS = {".": "floor", "i": "inlay", "x": "exit", "h": "threshold"}
GALLERY = {"C": "col_top", "c": "col_base", "p": "plinth", "q": "plinth_rose", "A": "altar", "b": "bench"}
BEDS = "#&%"            # rose beds; each letter is its own bed, kerbed against the others

# The rooms, by the rows of their floors.
ROOMS = {0: range(25, 36), 1: range(15, 23), 2: range(3, 13)}
DOORS = {0: (5, 34), 1: (5, 22), 2: (16, 12)}       # where a touch sends you back to
ENTRANCE = (5, 35)


def hashed(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def bed_piece(beds, x, y):
    n, s = (x, y - 1) in beds, (x, y + 1) in beds
    w, e = (x - 1, y) in beds, (x + 1, y) in beds
    if not n and not w:
        return "bed_NW"
    if not n and not e:
        return "bed_NE"
    if not s and not w:
        return "bed_SW"
    if not s and not e:
        return "bed_SE"
    if not n:
        return "bed_N"
    if not s:
        return "bed_S"
    if not w:
        return "bed_W"
    if not e:
        return "bed_E"
    return "bed"


def compose():
    m = Map(NAME, "temple_aphrodite", W, H, fill=0, primary="oikos")
    void = m.s("floor")["ids"][0][7]
    m.rect(0, 0, W - 1, H - 1, void, True)
    m.border = [void] * 4
    m.header = {"music": "MUS_ICHOR_TEMPLE", "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_INDOOR",
                "show_map_name": False, "allow_cycling": False, "allow_running": True,
                "allow_escaping": False}
    beds = {ch: {(x, y) for y, r in enumerate(PLAN) for x, c in enumerate(r) if c == ch} for ch in BEDS}
    for y, row in enumerate(PLAN):
        for x, c in enumerate(row[:W]):
            if c in WALLS:
                m.piece("walls", WALLS[c], x, y)
            elif c == "F":
                n = "frieze_rose" if x % 4 == 1 else ("frieze_dove" if x % 4 == 3 else "frieze")
                m.piece("walls", n, x, y)
            elif c in MIRROR_TILES:
                m.piece("mirrors", MIRROR_TILES[c], x, y, solid=True)
            elif c in FLOORS:
                n = FLOORS[c]
                if n == "floor":
                    r = hashed(x, y)
                    n = "petals" if r < 0.07 else ("petals_b" if r < 0.12 else ("floor_b" if r < 0.45 else "floor"))
                m.piece("floor", n, x, y)
            elif c in GALLERY:
                m.piece("gallery", GALLERY[c], x, y)
            elif c in "g8 9 7".replace(" ", ""):
                r = hashed(x, y, 3)
                m.piece("court", "gravel_b" if r < 0.3 else "gravel", x, y)
            elif c == "o":
                m.piece("court", "gravel_petals", x, y)
            elif c in BEDS:
                m.piece("court", bed_piece(beds[c], x, y), x, y, solid=True)
            elif c == "u":
                m.piece("court", "urn", x, y)
            elif c in "ZYV":
                m.piece("court", "gravel", x, y)            # the stands' own cells
    m.put("dais", 9, 2)
    # Passable overrides: the doorways' upper halves, the plinths
    for (x, y) in ((16, 13), (5, 23)):
        m.solid[y, x] = False
    return m


# --------------------------------------------------------------------------------------
# Objects. Statues: (local id, x, y, range or None). Mirrors: (local id, x, y, facing,
# gfx, turnable).
# --------------------------------------------------------------------------------------
STATUES = {
    0: [("LOCALID_GALLERY_S1", 2, 29, None)],
    1: [("LOCALID_GALLERY_S2", 9, 20, (3, 2)), ("LOCALID_GALLERY_S3", 13, 21, (2, 1)),
        ("LOCALID_GALLERY_S4", 17, 19, (1, 3)), ("LOCALID_GALLERY_S5", 8, 22, None)],
    2: [("LOCALID_GALLERY_S7", 19, 10, None), ("LOCALID_GALLERY_S8", 13, 8, (1, 1)),
        ("LOCALID_GALLERY_S9", 13, 10, (1, 1))],
}
MIRRORS = [
    ("LOCALID_GALLERY_M0", 4, 24, "S", "ICHOR_MIRROR_MARK", False),
    ("LOCALID_GALLERY_W1", 2, 14, "S", "ICHOR_MIRROR_MARK", False),
    ("LOCALID_GALLERY_W2", 19, 15, "W", "ICHOR_MIRROR_MARK", False),
    ("LOCALID_GALLERY_P1", 1, 6, "E", "ICHOR_MIRROR", False),
    ("LOCALID_GALLERY_P2", 17, 5, "E", "ICHOR_MIRROR", True),
    ("LOCALID_GALLERY_P3", 15, 5, "N", "ICHOR_MIRROR", True),
]
RIGHT = {"LOCALID_GALLERY_P2": "S", "LOCALID_GALLERY_P3": "S"}   # turned to look down their lanes
PEOPLE = {"LOCALID_GALLERY_CHARIS": (6, 32), "LOCALID_GALLERY_RHODANTHE": (16, 16),
          "LOCALID_GALLERY_ANTHOUSA": (3, 5), "LOCALID_GALLERY_GALATEA": (10, 3)}
DIR_MOVE = {"S": "", "N": "_UP", "W": "_LEFT", "E": "_RIGHT"}

# The intended routes, room by room (from the room's door), and the tempting ones.
ROUTES = {
    # up the west side facing M0 (S1 falls in behind you and freezes), across, through the door
    "pronaos": ((5, 34), ["W"] + ["N"] * 9 + ["E", "N", "N", "N"]),
    # the same, then turning back toward S1
    "pronaos_back": ((5, 34), ["W"] + ["N"] * 7 + ["S", "S", "S"]),
    # up the west aisle facing W1, along the north aisle facing W2, Rhodanthe, the door
    "gallery": ((5, 22), ["W", "W", "W"] + ["N"] * 7 + ["E"] * 14 + ["N", "N"]),
    # straight across the hall toward the door and up the east aisle
    "gallery_east": ((5, 22), ["N"] + ["E"] * 13 + ["N"] * 6 + ["W", "W", "N", "N"]),
    "court": ((16, 12), ["E"] + ["N"] * 6 + ["tLOCALID_GALLERY_P2"] + ["W"] * 5 + ["N"]),
    "court_garden": ((16, 12), ["W"] + ["N"] * 6 + ["W"] * 3 + ["N"]),
}


def events(m):
    m.warp(5, 35, "MAP_KYTHERA_PAPHIA", 0)
    m.obj("ICHOR_YOUTH_F", 6, 32, P + "Charis", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_GALLERY_CHARIS")
    for room, statues in STATUES.items():
        for (lid, x, y, rng) in statues:
            e = m.obj("TRICK_HOUSE_STATUE", x, y, P + "Statue", "MOVEMENT_TYPE_ICHOR_STATUE", local_id=lid)
            if rng:
                e["movement_range_x"], e["movement_range_y"] = rng
    for (lid, x, y, f, gfx, turnable) in MIRRORS:
        e = m.obj(gfx, x, y, P + ("TurnMirror" if turnable else ("FixedMirror" if gfx == "ICHOR_MIRROR" else "WallMirror")),
                  "MOVEMENT_TYPE_ICHOR_MIRROR" + DIR_MOVE[f], local_id=lid)
        if y in (14, 24) or x == 19:
            e["_floats"] = True                                    # a marker on its wall tile
    m.obj("ICHOR_ACOLYTE_F", 16, 16, P + "Rhodanthe", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1,
          local_id="LOCALID_GALLERY_RHODANTHE")
    m.obj("ICHOR_ACOLYTE_F", 3, 5, P + "Anthousa", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1,
          local_id="LOCALID_GALLERY_ANTHOUSA")
    m.item_ball(2, 5, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_TEMPLE_APHRODITE_MAX_REVIVE")
    m.obj("ICHOR_PRIESTESS", 10, 3, P + "Galatea", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_GALLERY_GALATEA")
    # stepping into a room wakes its statues (VAR_TEMP_1: the room the player was in)
    m.trigger(5, 22, P + "EnterGallery", "VAR_TEMP_1", 0)
    m.trigger(5, 25, P + "EnterPronaos", "VAR_TEMP_1", 1)
    m.trigger(16, 12, P + "EnterCourt", "VAR_TEMP_1", 1)
    m.trigger(16, 15, P + "EnterGallery", "VAR_TEMP_1", 2)
    for x in range(9, 13):
        m.trigger(x, 5, P + "DaisStep", "VAR_TEMP_1", 2)
    m.sign(6, 24, P + "Fresco", "BG_EVENT_PLAYER_FACING_NORTH")
    m.sign(6, 33, P + "DoveAltar")
    m.sign(3, 29, P + "Bench")
    m.sign(19, 8, P + "Urn")


# --------------------------------------------------------------------------------------
# The model checks
# --------------------------------------------------------------------------------------
def walkable_grid(m):
    def walk(x, y):
        return m.walkable(x, y) and m.behavior(int(m.mid[y, x])) != "MB_SOUTH_ARROW_WARP" or (x, y) == ENTRANCE
    return walk


def sim_for(m, room, turned=False):
    statues = [Statue(lid, x, y, rng) for (lid, x, y, rng) in STATUES[room]]
    mirrors = {lid: [x, y, (RIGHT.get(lid, f) if turned else f)] for (lid, x, y, f, _, _) in MIRRORS}
    people = list(PEOPLE.values())
    s = Sim(walkable_grid(m), statues, mirrors, people)
    s.sight = {(16, 15)} if room == 1 else set()           # Rhodanthe spots you at the door
    return s


def check_rite(m):
    errors = []
    expect = {"pronaos": (0, True), "pronaos_back": (0, False), "gallery": (1, True), "gallery_east": (1, False),
              "court": (2, True), "court_garden": (2, False)}
    for name, (room, safe) in expect.items():
        start, route = ROUTES[name]
        s = sim_for(m, room)
        touched, step, end = s.play(start, route)
        ok = (touched is None) if safe else (touched not in (None, "bump"))
        print(f"  {name:13s} {'safe' if touched is None else f'touched by {touched} at step {step} {end}'}")
        if not ok:
            errors.append(f"route {name}: expected {'safe' if safe else 'a touch'}, got {touched} at step {step} {end}")
    # the court's route needs P2: unturned, the trailer reaches you at the north walk?
    start, route = ROUTES["court"]
    s = sim_for(m, 2)
    t, step, end = s.play(start, [a for a in route if not a.startswith("t")])
    print(f"  court, P2 unturned: {'safe' if t is None else f'touched by {t} at step {step}'}")
    for name, room in (("gallery", 1), ("pronaos", 0), ("court", 2)):
        start, route = ROUTES[name]
        s = sim_for(m, room)
        s.mirrors = {}
        t, step, end = s.play(start, [a for a in route if not a.startswith("t")])
        print(f"  {name}, no mirrors at all: {'safe' if t is None else f'touched by {t} at step {step} {end}'}")
    # the plain shortest walk in the gallery and the court must be touched
    for room, start, goal in ((2, (16, 12), (12, 5)),):
        s = sim_for(m, room)
        r = plain_route(s, start, goal)
        t, step, end = s.walk(start, r)
        print(f"  room {room} plain {r}: {'safe' if t is None else f'touched by {t}'}")
        if t is None:
            errors.append(f"room {room}: the plain shortest walk {r} is never touched")
    return errors


def write_routes(m):
    """Each route with the model's prediction: touched by whom at which step (or
    none), where the player ends, and where every statue of the room stands."""
    out = ROOT / "tools/ichor/tests/act3_galatea_routes.lua"
    room_of = {"pronaos": 0, "pronaos_back": 0, "gallery": 1, "gallery_east": 1, "court": 2, "court_garden": 2}
    lines = ["-- Galatea's Gallery: the routes tools/ichor/maps/kythera_temple.py checks against its",
             "-- model of the statues, with the model's predictions. Generated; do not edit.", "return {"]
    for name, (start, route) in ROUTES.items():
        s = sim_for(m, room_of[name])
        touched, step, end = s.play(start, route)
        acts = ", ".join(f'"{a}"' for a in route)
        statues = ", ".join(f"{st.name} = {{ {st.x}, {st.y} }}" for st in s.statues)
        s2 = sim_for(m, room_of[name])
        s2.play(start, route[:-1])
        before = ", ".join(f"{st.name} = {{ {st.x}, {st.y} }}" for st in s2.statues)
        lines.append(f"  {name} = {{ x = {start[0]}, y = {start[1]}, steps = {{ {acts} }},")
        lines.append(f'    touched = {f"{chr(34)}{touched}{chr(34)}" if touched else "nil"}, at = {step}, '
                     f"endx = {end[0]}, endy = {end[1]},")
        lines.append(f"    statues = {{ {statues} }},")
        lines.append(f"    before_last = {{ {before} }} }},")
    lines.append("}")
    out.write_text("\n".join(lines) + "\n")


VIEWS = [(5, 31), (5, 26), (5, 20), (10, 16), (16, 16), (16, 10), (12, 6), (5, 6), (10, 4)]


def main():
    m = compose()
    events(m)
    errors = check_rite(m)
    write_routes(m)
    must = [(5, 22, "the gallery"), (16, 12, "the rose court"), (12, 5, "the dais's inlay"), (3, 6, "Anthousa")]
    found, _ = m.check([(5, 34)], must, blockers=[(6, 32)])
    errors += found
    for o in m.objects:
        o.pop("_floats", None)
    m.write()
    if "--no-render" not in sys.argv:
        m.render("kythera_temple_of_aphrodite", VIEWS)
    for e in errors:
        print(f"{NAME} CHECK: {e}")
    print(f"{NAME}: {W}x{H}, {len(m.objects)} objects; {'checks pass' if not errors else f'{len(errors)} problems'}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
