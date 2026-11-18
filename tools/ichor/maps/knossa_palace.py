#!/usr/bin/env python3
"""The Palace of Minos above ground (design/maps/KnossaPalace.md; SCRIPT.md III-3C,
III-3D, III-3E, III-3O, III-3P's landing; LABYRINTH.md §3).

The hill of Kephala, its north slope to the Bull Road. The North Entrance is a
passage through the north wing, held by two Titanborn; it opens on the North
Pillar Hall and the whole Central Court at once. The court runs north-south
as at Knossos: the bull-leaping lane down its middle, the Gentle Bull's pen,
porticoes of red tapering columns. West: the Throne Room wing, the West
Magazines behind it, the West Court's kouloures. North-west: the Theatral
Area. East: the Grand Staircase wing and the Queen's Megaron. South: the
South Propylon with the lily prince, and the hill's face.

    python3 tools/ichor/maps/knossa_palace.py [--pass N]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_maps as KM  # noqa: E402
from knossa_maps import A, Map, ensure_map  # noqa: E402

NAME, W, H = "KnossaPalace", 60, 50
P = "KnossaPalace_EventScript_"
LANE_X, LANE_N, LANE_S = 30, 19, 27      # the leap: the bull at LANE_N, you at LANE_S
DOORS = {"ThroneRoom": (14, 23), "WestMagazines": (7, 33), "QueensMegaron": (47, 36),
         "GrandStaircase": (45, 23)}


def pave(m, cells, seed=0, clean=False):
    for (x, y) in cells:
        k = KM._hash(x, y, seed) % 23
        n = "ABCD"[(x + 2 * y + (k > 11)) % 4]
        if k == 0 and not clean:
            n = "cracked"
        elif k in (7, 15) and not clean:
            n = "weeds"
        m.piece("paving", n, x, y)


def ruin(m, cells):
    """Grass through the ruin: the cells go to grass, and paving round them breaks
    up with the edge pieces (named by where the grass is)."""
    cells = set(c for c in cells if m.ok(*c))
    for (x, y) in cells:
        m.set(x, y, A.GRASS, False)
    g = lambda x, y: (x, y) in cells  # noqa: E731
    pav = set(m.s("paving")["ids"][j][i] for j in range(4) for i in range(6))
    for (x, y) in {(x + dx, y + dy) for (x, y) in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - cells:
        if not m.ok(x, y) or int(m.mid[y, x]) not in pav:
            continue
        n, s, e, w = g(x, y - 1), g(x, y + 1), g(x + 1, y), g(x - 1, y)
        name = ("edge_NW" if n and w else "edge_NE" if n and e else "edge_SW" if s and w else
                "edge_SE" if s and e else "edge_N" if n else "edge_S" if s else "edge_E" if e else
                "edge_W" if w else None)
        if name:
            m.piece("paving", name, x, y)


def wing(m, x0, x1, y0, y1, faces=(), tops=(), shadow=False):
    """A wing of the palace standing one storey above the ruin: wall tops from
    y0 to y1-2 (the roofs and wall heads seen from above), two face rows at
    y1-1 and y1. `faces`/`tops`: {(x, y): piece} overrides."""
    faces, tops = dict(faces), dict(tops)
    for y in range(y0, y1 - 1):
        for x in range(x0, x1 + 1):
            n = "top_L" if x == x0 else ("top_R" if x == x1 else "top")
            if y > y0 and x0 < x < x1:
                # the roof behind the parapet: rubble-filled masonry, a fallen patch here and there
                n = "block" if KM._hash(x, y, 43) % 7 else "rubble"
            elif y == y0 and x0 < x < x1 and (x * 5 + y) % 6 == 0:
                n = "top_horns"
            elif x0 < x < x1 and KM._hash(x, y, 41) % 9 == 0:
                n = "top_broken"
            elif y > y0:
                n = "side"
            m.piece("walls", tops.get((x, y), n), x, y)
    for y in (y1 - 1, y1):
        for x in range(x0, x1 + 1):
            n = "face_L" if x == x0 else ("face_R" if x == x1 else
                                          ("face_shadow" if shadow and y == y1 else "face"))
            if n == "face" and KM._hash(x, y, 42) % 9 == 0:
                n = "face_labrys"
            m.piece("walls", faces.get((x, y), n), x, y)


def columns(m, x0, x1, y, every=2, horns=()):
    """A portico: the beam on row y over red columns and shaded paving on y+1."""
    for x in range(x0, x1 + 1):
        col = (x - x0) % every == 0
        n = "beam_L" if x == x0 else ("beam_R" if x == x1 else
                                      ("beam_col" if col else ("beam_horns" if x in horns else "beam")))
        m.piece("columns", n, x, y)
        m.piece("columns", "under_col" if col else "under", x, y + 1)


def column(m, x, y, broken=False):
    if broken:
        m.piece("columns", "stump", x, y + 1)
    else:
        m.piece("columns", "col_top", x, y)
        m.piece("columns", "col", x, y + 1)


def build(stem):
    ensure_map(NAME, W, H, "palace_minos", "MAP_TYPE_TOWN", "MAPSEC_PALACE_OF_MINOS", "MUS_ICHOR_TEMPLE")
    m = Map(NAME, "palace_minos", W, H, fill=A.GRASS)
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT[0], A.OLIVE_BOT[1]]

    # ---- the north slope (aethos only): olive country, the road down from the Bull Road ----
    woods = {(x, y) for x in range(0, W) for y in range(0, 6)} - {(x, y) for x in range(26, 33) for y in range(0, 6)}
    woods -= {(x, y) for x in range(4, 18) for y in range(3, 6)}
    m.woods(woods, salt=51, aethos_only=lambda x, y: True, singles=[])
    m.path({(x, y) for x in range(28, 31) for y in range(0, 7)} | {(x, 5) for x in range(10, 28)}
           | {(x, 4) for x in range(12, 28)})
    m.seam("up")

    # ---- the hill top: everything from y6 is the palace's paving ----
    plateau = {(x, y) for x in range(1, W - 1) for y in range(6, 46)}
    pave(m, plateau, seed=1)
    for x in range(0, W):
        m.piece("cliff", "back_NW" if x == 0 else ("back_NE" if x == W - 1 else "back"), x, 6)
    for x in list(range(1, 5)) + list(range(19, 24)) + list(range(43, 50)):
        m.set(x, 6, A.GRASS, False)
        m.piece("cliff", "back", x, 7)
    for y in range(7, 46):
        m.piece("cliff", "side_W", 0, y)
        m.piece("cliff", "side_E", W - 1, y)
    # the ramp up to the North Entrance, and the Theatral Area's way up from the road
    for x in range(27, 32):
        m.piece("paving", "A", x, 6)
    for x in range(10, 13):
        m.piece("paving", "B", x, 6)
    # south: the hill's face and the grass below
    m.rect(0, 45, W - 1, H - 1, A.GRASS, False)
    lipy = {x: (45 if (x // 6) % 3 == 1 else 46) for x in range(W)}
    for x in range(0, W):
        y = lipy[x]
        for yy in range(45, y):
            pave(m, {(x, yy)}, seed=9)
        stepL = x == 0 or lipy[x - 1] != y
        stepR = x == W - 1 or lipy[x + 1] != y
        m.piece("cliff", "lip_L" if x == 0 else ("lip_R" if x == W - 1 else ("lip_b" if x % 5 == 2 else "lip")), x, y)
        m.piece("cliff", "face_L" if (x == 0 or (stepL and lipy[x - 1] > y)) else
                ("face_R" if (x == W - 1 or (stepR and lipy[x + 1] > y)) else ("face_b" if x % 4 == 1 else "face")), x, y + 1)
    for x in range(1, W - 1, 3):
        m.piece("cliff", "foot_grass", x, 48)
    m.part("court_works", "stair_L", 28, 45, 2, 2)
    for (x, y) in ((2, 48), (9, 48), (16, 48), (36, 48), (44, 48), (52, 48)):
        m.olive(x, y)

    # ---- the ruin's grass: the hill takes the palace back at its edges ----
    blob = lambda x0, y0, x1, y1, s: {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)  # noqa: E731
                                      if KM._hash(x // 2, y // 2, s) < 760 or (x0 < x < x1 and y0 < y < y1)}
    zones = (blob(1, 13, 7, 16, 61) | blob(2, 41, 8, 44, 62) | blob(14, 43, 20, 44, 63) | blob(56, 8, 58, 14, 64)
             | blob(53, 24, 58, 27, 65) | blob(41, 38, 50, 44, 66) | blob(52, 38, 58, 43, 67) | blob(1, 23, 5, 25, 68)
             | blob(17, 26, 20, 31, 69) | blob(55, 28, 58, 34, 70) | blob(40, 24, 44, 27, 71)
             | blob(1, 7, 4, 9, 72) | blob(43, 7, 50, 9, 73))
    ruin(m, zones)
    # the hill's flanks: cypress and broken masonry along the edge, so it never runs straight
    for y in range(9, 44, 7):
        m.cypress(1, y)
        m.cypress(58, y + 3)
    for y in (12, 26, 33, 40):
        m.piece("walls", "rubble", 1, y)
        m.piece("walls", "block", 58, y - 2)
    for (x, y) in ((3, 14), (54, 25), (46, 41), (5, 42), (56, 39)):
        m.olive(x, y)
    m.cypress(57, 10)
    m.cypress(18, 27)

    # ---- the Theatral Area (north-west): broad steps, the dancers' worn floor ----
    for y in (8, 9):
        m.piece("court_works", "steps_L", 6, y)
        for x in range(7, 15):
            m.piece("court_works", "steps", x, y)
        m.piece("court_works", "steps_R", 15, y)
    for y in (10, 11, 12):
        for x in range(6, 16):
            m.piece("paving", "dance" if (x + y) % 2 else "dance_b", x, y)
    # its second flight, running north-south along the dance floor's east side
    for y in range(8, 13):
        m.piece("court_works", "steps_corner" if y == 8 else "steps_V", 16, y)
        m.piece("court_works", "steps_V", 17, y) if y > 8 else m.piece("court_works", "steps_R", 17, y)

    # ---- the north wing and the North Entrance passage ----
    wing(m, 18, 26, 7, 11, faces={(22, 10): "face_frieze", (23, 10): "face_frieze", (18, 10): "face_window"})
    m.part("frescoes", "bull_TL", 23, 10, 3, 2)
    wing(m, 32, 41, 7, 11, faces={(33, 10): "face_frieze", (40, 11): "face_window"})
    m.part("frescoes", "leap_TL", 36, 10, 3, 2)
    pave(m, {(x, y) for x in range(27, 32) for y in range(7, 13)}, seed=2)
    # the North Pillar Hall: a portico across the passage's mouth
    columns(m, 18, 41, 12, every=3, horns=(29,))
    m.piece("columns", "under", 29, 13)
    m.piece("columns", "beam_horns", 29, 12)
    for x in (28, 30):
        m.piece("columns", "beam", x, 12)
        m.piece("columns", "under", x, 13)

    # ---- the west: the Throne Room wing, the West Magazines, the West Court ----
    wing(m, 11, 19, 16, 19, tops={(15, 16): "top_horns"})
    wing(m, 9, 21, 20, 23, faces={(x, 22): "face_frieze" for x in range(10, 21)} | {(14, 23): "door"},
         tops={(10, 20): "top_horns", (20, 20): "top_horns"})
    m.part("court_works", "well_TL", 6, 17, 2, 2)
    wing(m, 4, 13, 27, 29)
    wing(m, 2, 15, 30, 33, faces={(7, 33): "door", (3, 32): "face_window", (12, 32): "face_window"})
    for x in range(3, 15, 2):
        m.piece("columns", "pithos_top", x, 25)
        m.piece("columns", "pithos", x, 26)
    # the West Court: a lower lawn crossed by raised paved walkways, three kouloures
    west_court = {(x, y) for x in range(1, 21) for y in range(35, 45)}
    walks = ({(x, 34) for x in range(2, 21)} | {(16, y) for y in range(34, 45)} | {(x, 40) for x in range(1, 16)}
             | {(x, 44) for x in range(16, 21)})
    ruin(m, west_court - walks)
    pave(m, walks - {(16, 34)}, seed=12, clean=True)
    m.part("court_works", "pit_TL", 4, 37, 2, 2)
    m.part("court_works", "pit_TL", 9, 42, 2, 2)
    m.part("court_works", "pit_TL", 12, 36, 2, 2)
    for (x, y) in ((3, 41), (12, 39), (17, 38)):
        m.piece("court_works", "steps_V", x, y)
    for (x, y) in ((19, 41), (2, 42)):
        column(m, x, y, broken=True)
    m.piece("walls", "rubble", 6, 43)
    m.piece("walls", "rubble", 14, 43)

    # ---- the Central Court: the lane, the pen, the porticoes ----
    court = {(x, y) for x in range(22, 39) for y in range(14, 34)}
    pave(m, court, seed=3, clean=True)
    m.piece("paving", "lane_N", LANE_X, LANE_N)
    for y in range(LANE_N + 1, LANE_S):
        m.piece("paving", "lane_line" if y == LANE_S - 1 else "lane", LANE_X, y)
    m.piece("paving", "lane_S", LANE_X, LANE_S)
    # the pen, south-east of the lane
    for x, n in ((34, "fence_L"), (35, "fence_gate"), (36, "fence"), (37, "fence_R")):
        m.piece("court_works", n, x, 28)
    m.piece("court_works", "fence_V", 34, 29)
    m.piece("court_works", "fence_V", 37, 29)
    m.piece("court_works", "trough", 35, 30)
    m.piece("court_works", "hay", 36, 30)
    m.piece("court_works", "fence_L", 34, 31)
    m.piece("court_works", "fence", 35, 31)
    m.piece("court_works", "fence", 36, 31)
    m.piece("court_works", "fence_R", 37, 31)
    for y in (14, 16, 18, 20, 26, 28, 30):
        column(m, 22, y, broken=(y == 18))
    for y in (14, 16, 18, 24, 26, 28, 30):
        column(m, 38, y, broken=(y == 28))
    columns(m, 23, 37, 33, every=2, horns=(26, 30, 34))
    m.piece("walls", "horns", 25, 32)
    m.piece("court_works", "drain", 30, 30)
    m.piece("court_works", "plinth", 27, 15)
    # the court's altar and horns of consecration, and its drains, the open heart
    m.piece("court_works", "plinth", 34, 16)
    m.piece("walls", "horns", 26, 24)
    m.piece("walls", "horns", 35, 24)
    m.piece("court_works", "drain", 26, 30)
    m.piece("court_works", "drain", 33, 19)

    # ---- the east: the Grand Staircase wing, the Queen's Megaron ----
    wing(m, 43, 52, 15, 19, tops={(47, 15): "top_horns"})
    wing(m, 40, 55, 20, 23, faces={(45, 23): "door", (42, 22): "face_frieze", (43, 22): "face_frieze",
                                   (50, 22): "face_window"}, tops={(41, 20): "top_horns"})
    m.part("court_works", "well_TL", 55, 16, 2, 2)
    m.part("court_works", "well_TL", 48, 20, 2, 2)
    wing(m, 45, 54, 28, 32)
    wing(m, 42, 56, 33, 36, faces={(47, 36): "door", (44, 35): "face_frieze", (45, 35): "face_frieze",
                                   (52, 35): "face_window"}, tops={(43, 33): "top_horns"})
    m.part("court_works", "well_TL", 39, 30, 2, 2)
    for (x, y) in ((41, 26), (57, 26), (40, 40), (57, 41), (44, 43)):
        column(m, x, y, broken=(x % 3 == 0))

    # ---- the south: the South Propylon and the lily prince ----
    wing(m, 22, 38, 39, 42, faces={(x, 42): "face_frieze" for x in range(23, 26)})
    m.part("frescoes", "prince_TL", 30, 41, 2, 2)
    m.piece("walls", "rubble", 25, 44)
    m.piece("walls", "horns", 34, 44)

    # ---- height: the hill top stands a level above the road; the ramps meet both ----
    top = {(x, y) for x in range(1, W - 1) for y in range(7, 47) if not m.solid[y, x]}
    m.raise_ground(top, 4, joins={(x, y) for x in range(27, 32) for y in (6, 7)}
                   | {(x, y) for x in range(10, 13) for y in (6, 7)} | {(28, 45), (29, 45), (28, 46), (29, 46)})
    # the West Court's lawn lies a level below its walkways; their steps join the two
    for c in west_court - walks:
        if not m.solid[c[1], c[0]]:
            m.elev[c] = 3
    for c in ((3, 41), (12, 39), (17, 38)):
        m.elev[c] = 0

    # ---- events ----
    for k, (x, y) in DOORS.items():
        m.warp(x, y, f"MAP_KNOSSA_PALACE_{_const(k)}", 0)
    m.connect("up", 14, "MAP_KNOSSA_BULL_ROAD")
    T = lambda g, x, y, s, mv, sight, lid, flag="0": m.obj(g, x, y, P + s, mv, trainer=True,  # noqa: E731
                                                           sight=sight, local_id=lid, flag=flag)
    T("ICHOR_TITAN_GRUNT", 27, 9, "Keramos", "MOVEMENT_TYPE_FACE_RIGHT", 4, "LOCALID_PALACE_KERAMOS")
    T("ICHOR_TITAN_GRUNT", 31, 10, "Gypsos", "MOVEMENT_TYPE_FACE_LEFT", 4, "LOCALID_PALACE_GYPSOS")
    m.obj("SPECIES(TAURIVET)", LANE_X, LANE_N, P + "GentleBull", "MOVEMENT_TYPE_FACE_DOWN",
          local_id="LOCALID_PALACE_GENTLE_BULL")
    m.obj("ICHOR_SARPEDON", 32, LANE_S, P + "Sarpedon", "MOVEMENT_TYPE_FACE_LEFT",
          local_id="LOCALID_PALACE_SARPEDON")
    m.obj("ICHOR_KLEON", 29, 14, P + "Kleon", "MOVEMENT_TYPE_FACE_UP",
          flag="FLAG_ICHOR_HIDE_KLEON_KNOSSA", local_id="LOCALID_PALACE_KLEON")
    m.obj("ICHOR_ALETHEA", 29, 8, P + "AletheaNight", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ALETHEA_COURT", local_id="LOCALID_PALACE_ALETHEA")
    m.obj("ICHOR_ARIADNE", 32, 21, P + "Ariadne", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ARIADNE_COURT", local_id="LOCALID_PALACE_ARIADNE")
    m.obj("SPECIES(ASTERLORN)", 33, 21, P + "Asterion", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_ASTERION_COURT", local_id="LOCALID_PALACE_ASTERION")
    m.obj("ICHOR_TITAN_GRUNT", 13, 24, P + "WestGrunt", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS")
    m.obj("ICHOR_PRIESTESS", 9, 11, P + "Dancer", "MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT", rx=2)
    m.item_ball(32, 44, "ITEM_ELIXIR", "FLAG_ICHOR_ITEM_PALACE_ELIXIR")
    m.hidden(11, 19, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_ITEM_PALACE_STAR_PIECE")
    m.hidden(25, 32, "ITEM_RELIC_GOLD", "FLAG_ICHOR_HIDDEN_ITEM_PALACE_GOLD_STATER")
    m.sign(LANE_X, LANE_S - 1, P + "LeapLine", facing="BG_EVENT_PLAYER_FACING_NORTH")
    m.sign(10, 11, P + "WornSteps")
    m.sign(24, 11, P + "ChargingBull")
    m.sign(37, 11, P + "Leapers")
    m.sign(30, 42, P + "LilyPrince")
    m.sign(31, 42, P + "LilyPrince")
    m.build(stem, starts=[(29, 0)],
            must_reach=[(LANE_X, LANE_S, "the leap's start"), (32, 44, "the Elixir"), (10, 10, "the dance floor"),
                        (7, 34, "the Magazines' door front"), (47, 37, "the Megaron's door front")],
            views=[(29, 8), (30, 20), (14, 22), (10, 38), (47, 25), (30, 42)],
            blockers=[])
    return m


def _const(k):
    import re
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", k).upper()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pass", dest="n", default="1")
    build(f"knossa_palace_pass{ap.parse_args().n}")
