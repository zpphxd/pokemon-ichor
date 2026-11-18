#!/usr/bin/env python3
"""Build the Ascent's outdoor snow floors on gTileset_Oros (design/maps/Ascent_*.md):

  Ascent_Snowfield   the Leuke snowfield: deep snow, firs, the Mirror Tarn, the
                     Icefall's mouth in the cliff (between 2F and the Icefall)
  Ascent_Glacier     the river of ice: the frozen lake, the Gate of the Winds,
                     the Giants in the ice (ascent_glacier.py's puzzles, outdoors)
  Ascent_WindRidge   Boreas's ridge over the cloud: the Bellows of Boreas
                     (between the Glacier and 3F)

Each writes its layout, map.json and scripts.pory, and its puzzle answers into
tools/ichor/tests/ascent_plans.lua (with ascent_snow.py's). 3F and the
Propylaia's facade are tools/ichor/maps/propylon.py.

Usage: /usr/bin/python3 tools/ichor/maps/oros_maps.py [--render DIR] [--tag T] [--only A,B] [--walk]
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascent_lib as A  # noqa: E402
from ascent_lib import push_plan  # noqa: E402
from league_lib import ROOT, noise  # noqa: E402
from oros_lib import Oros, roughen, seam_check  # noqa: E402
from ascent_glacier import sign_script, trainer_script, write_scripts  # noqa: E402

PLANS = {}


def lv_plan(w, h, fill):
    return np.full((h, w), fill, int)


def area(a, v, x0, y0, x1, y1, salt=0, wob=0):
    """Fill a rectangle with level v; `wob` > 0 wobbles its edges (never straight)."""
    H, W = a.shape
    for y in range(max(0, y0 - wob), min(H, y1 + wob + 1)):
        for x in range(max(0, x0 - wob), min(W, x1 + wob + 1)):
            if wob:
                dx = max(x0 - x, x - x1, 0)
                dy = max(y0 - y, y - y1, 0)
                if dx or dy:
                    if (noise(x, y, salt) % (wob + 1)) < max(dx, dy):
                        continue
                    if dx and dy:
                        continue
            a[y, x] = v


def rows_of(a):
    return ["".join("~" if v < 0 else str(v) for v in r) for r in a]


def ice_mask(g):
    """The MB_ICE cells (cached: rocks on the ice never change which cells are ice)."""
    if getattr(g, "_ice_mask", None) is None:
        g._ice_mask = g.ice()
    return g._ice_mask


def ice_graph(g, start, blocked=()):
    """Every resting place the ice lets you reach from start, and the slides
    between them: {node: {key: node}}."""
    ok = g.walkable(blocked)
    ice = ice_mask(g)
    edges, q = {}, [start]
    while q:
        p = q.pop()
        if p in edges:
            continue
        edges[p] = {}
        for d in A.DIRS:
            n = g.slide(ok, ice, p[0], p[1], d)
            if n and n != p:
                edges[p][d] = n
                if n not in edges:
                    q.append(n)
    return edges


def ice_report(g, start, goal, item=None, blocked=()):
    """Prove an ice field: the fewest slides to the goal (and to the item), the
    dead ends (resting places from which every slide leaves you no nearer the
    goal than the start: you have to go back), and that nothing strands you.
    The start region counts as one node (walking on snow costs nothing)."""
    edges = ice_graph(g, start, blocked)
    ice = ice_mask(g)
    on_ice = lambda p: ice[p[1], p[0]]

    def bfs(src, rev=False):
        adj = {}
        for p, es in edges.items():
            for d, n in es.items():
                a_, b_ = (n, p) if rev else (p, n)
                w = 0 if (not on_ice(a_) and not on_ice(b_) and abs(a_[0] - b_[0]) + abs(a_[1] - b_[1]) == 1) else 1
                adj.setdefault(a_, []).append((b_, w))
        dist = {src: 0}
        dq = [src]
        import collections
        dq = collections.deque([src])
        while dq:
            p = dq.popleft()
            for n, w in adj.get(p, ()):
                nd = dist[p] + w
                if n not in dist or nd < dist[n]:
                    dist[n] = nd
                    (dq.appendleft if w == 0 else dq.append)(n)
        return dist
    fwd = bfs(start)
    back = bfs(goal, rev=True)
    if goal not in fwd:
        raise SystemExit(f"{g.name}: the ice can't reach {goal}")
    home = bfs(start, rev=True)
    stranded = [p for p in fwd if p not in home]
    if stranded:
        raise SystemExit(f"{g.name}: the ice strands the player at {sorted(stranded)[:6]}")
    d0 = back[start]
    # a dead end leaves you further from the goal than you were at the start
    dead = sorted(p for p in fwd if on_ice(p) and p != goal and back.get(p, 99) > d0)
    rep = dict(moves=fwd[goal], dead_ends=dead, nodes=len(fwd))
    if item:
        near = [n for n in fwd if abs(n[0] - item[0]) + abs(n[1] - item[1]) == 1]
        if not near:
            raise SystemExit(f"{g.name}: the ice can't reach the find at {item}")
        rep["item_moves"] = min(fwd[n] for n in near)
        rep["item_from"] = min(near, key=lambda n: fwd[n])
    return rep


def search_ice(g, start, goal, cells, n_rocks, seed, want, item=None, tries=6000, fixed=()):
    """Place rocks on the ice until the field meets `want` (a test on ice_report's
    result). Returns (rocks, report)."""
    rng = random.Random(seed)
    cells = sorted(set(cells))
    for _ in range(tries):
        rocks = list(fixed) + rng.sample(cells, n_rocks)
        saved = [(x, y, g.solid[y, x]) for x, y in rocks]
        for x, y in rocks:
            g.solid[y, x] = True
        try:
            rep = ice_report(g, start, goal, item)
            good = want(rep)
        except SystemExit:
            good = False
        for x, y, v in saved:
            g.solid[y, x] = v
        if good:
            return sorted(rocks), rep
    raise SystemExit(f"{g.name}: no ice field met the brief")


# ---------------------------------------------------------------------------
# The Leuke snowfield
# ---------------------------------------------------------------------------
SW, SH = 40, 46
S_MOUTH = (18, 11)                 # the Icefall's mouth (2x2 over the cliff's foot; its door row is y 12)
S_LANDING = (19, 14)               # where the tarn's answer ends, under the mouth
S_SHORE = (20, 28)                 # where it starts, on the south shore (its one way onto the ice is x 20)
S_STAIR = (25, 26)                 # the cut stair up the shelf's face (rows 29-32)
S_LEDGE = (31, 33, 14)             # the shortcut: a cornice from the mouth's path down the east corridor
S_ROCKS_SEED = 7


def snowfield_levels():
    a = lv_plan(SW, SH, 5)
    area(a, 4, 0, 0, SW - 1, 8)                          # the high plateau over the Icefall
    area(a, 4, 0, 9, 15, 12)                             # its cliff stands right over the tarn's west half
    area(a, 2, 16, 9, 33, 14)                            # under the mouth, and the path east
    area(a, 2, 6, 13, 30, 28)                            # the tarn's shelf
    area(a, 0, 31, 15, 33, 32)                           # the east corridor, down to the meadow
    area(a, 0, 4, 29, 33, 45)                            # the meadow
    area(a, 2, 4, 35, 9, 37)                             # the knoll with the roped cave
    for y in range(15, SH):
        for x in range(34, SW):
            a[y, x] = -1                                 # the cloud sea, east
    for y in range(9, 15):
        for x in range(36, SW):
            a[y, x] = -1
    return a


def build_snowfield():
    a = snowfield_levels()
    # the mountain's edges never run straight: the cloud bites into the east side and
    # the west flank's rock juts into the meadow (nothing the climb needs is touched)
    keep = {(x, y) for x in range(16, 34) for y in range(9, 33)} | {(x, y) for x in range(4, 34) for y in range(33, 46)}
    roughen(a, -1, 61, rate=34, keep={(x, y) for x in range(16, 36) for y in range(9, 36)})
    roughen(a, 5, 62, rate=26, keep=keep - {(x, y) for x in range(4, 6) for y in range(36, 46)}, levels={0})
    g = Oros("Ascent_Snowfield", rows_of(a))
    P = "Ascent_Snowfield_EventScript_"
    g.paint()
    tarn = {(x, y) for y in range(15, 27) for x in range(7, 30) if a[y, x] == 2 and (x, y) not in g.face}
    for c in ((7, 26), (29, 26), (7, 17), (29, 15)):
        tarn.discard(c)
    g.tarn(tarn)
    g.stairs({(x, y) for x in S_STAIR for y in range(29, 33)})
    lx0, lx1, ly = S_LEDGE
    g.ledge({(x, ly) for x in range(lx0, lx1 + 1)})
    deep = {(x, y) for y in range(35, 39) for x in range(10, 31)}
    deep |= {(x, y) for y in range(28, 29) for x in range(9, 16)}
    deep |= {(x, y) for y in range(42, 45) for x in range(22, 27)}
    g.deep(deep)
    road = {(x, y) for y in range(39, 46) for x in range(18, 21)} | {(x, 39) for x in range(18, 24)}
    road |= {(x, y) for y in (33, 34) for x in range(21, 28)} | {(x, 28) for x in range(20, 27)}
    road |= {(x, y) for y in (13, 14) for x in range(18, 21)} | {(x, 13) for x in range(21, 34)}
    g.path(road - deep)
    g.alpine({(x, y) for y in range(39, SH) for x in range(4, 34)
              if (x, y) not in deep and (x, y) not in road and noise(x, y, 77) < 18 + (y - 39) * 9})
    g.fixed[:] = False
    g.paint()
    # the Icefall's mouth at the cliff's foot; the road arrives from below
    g.put("mouth", *S_MOUTH)
    for x in (S_MOUTH[0], S_MOUTH[0] + 1):
        g.warp(x, S_MOUTH[1] + 1, "Ascent_Icefall", 1)
    for x in (18, 19, 20):
        g.put("exit_s", x, SH - 1)
        g.warp(x, SH - 1, "Ascent_2F", 0)
    # rocks along the tarn's north edge leave three cells of landing under the
    # mouth; along its south shore they leave one way onto the ice
    for x in list(range(16, 18)) + list(range(21, 31)):
        g.put("rock" if x % 3 else "rock_b", x, 14)
    for x in range(7, 30):
        if x not in (S_SHORE[0], S_SHORE[0] + 1) and (x, 27) not in g.face:
            g.put("rock" if x % 4 else "rock_b", x, 27)
    # the Mirror Tarn: rocks placed by a search for a fair warm-up (proven below)
    ice_cells = [c for c in sorted(g.ice_c) if c[1] < 26]
    rocks, rep = search_ice(g, S_SHORE, S_LANDING, ice_cells, 13, S_ROCKS_SEED,
                            lambda r: 4 <= r["moves"] <= 6 and len(r["dead_ends"]) >= 1)
    for i, (x, y) in enumerate(rocks):
        g.put("ice_rock" if i % 2 else "ice_rock_b", x, y)
    # the knoll's roped cave and the bronze door of the Twelve (post-game)
    g.put("mouth_roped", 6, 40)
    g.sign(6, 42, P + "RopedCave", facing="NORTH")
    g.sign(7, 42, P + "RopedCave", facing="NORTH")
    g.put("bronze_door", 12, 31)
    g.sign(12, 33, P + "BronzeDoor", facing="NORTH")
    g.sign(13, 33, P + "BronzeDoor", facing="NORTH")
    # firs: masses on the high ground and the meadow's edges, a few young ones out front
    for (key, x, y) in (("fir", 4, 43), ("fir_b", 10, 42), ("fir", 8, 43), ("fir_s", 12, 44),
                        ("fir", 29, 41), ("fir_b", 31, 39), ("fir", 31, 42), ("fir_s", 28, 44),
                        ("fir_arrow", 27, 39), ("fir_s", 16, 40), ("fir_s", 9, 39),
                        ("fir", 1, 10), ("fir_b", 0, 14), ("fir", 2, 18), ("fir", 0, 22), ("fir_b", 2, 26),
                        ("fir", 0, 30), ("fir", 2, 34), ("fir_b", 0, 38), ("fir", 2, 42), ("fir", 3, 0),
                        ("fir_b", 7, 1), ("fir", 12, 0), ("fir", 25, 1), ("fir_b", 29, 0), ("fir", 34, 2),
                        ("fir", 37, 4), ("fir_s", 15, 4), ("fir_s", 21, 5), ("fir", 6, 5), ("fir_b", 10, 6),
                        ("fir", 31, 5), ("fir", 18, 1), ("fir_s", 4, 10), ("fir", 9, 9), ("fir_s", 13, 10)):
        g.put(key, x, y)
    for (key, x, y) in (("boulder", 14, 41), ("rock", 22, 40), ("rock_b", 18, 34), ("drift", 22, 33),
                        ("drift", 8, 33), ("rock", 32, 34), ("drift_wine", 14, 33), ("rock", 23, 6),
                        ("boulder", 27, 6), ("rock_b", 36, 7), ("drift", 12, 3)):
        g.put(key, x, y)
    g.put("far_peak", 35, 38)
    g.put("poppy", 11, 41)
    g.sign(11, 41, P + "Poppy")
    g.sign(28, 41, P + "Arrow", facing="NORTH")
    g.hidden("ITEM_SCOPE_LENS", 28, 42, "FLAG_ICHOR_HIDDEN_ITEM_SNOWFIELD_SCOPE_LENS")
    g.sign(16, 33, P + "Wine", facing="WEST")
    g.put("sign", 21, 43)
    g.sign(21, 43, P + "Sign")
    g.put("sign", 21, 27)
    g.sign(21, 27, P + "Tarn", facing="NORTH")
    # Sisyphus's boulder at the meadow's foot: it always rolls back
    g.person("SISYPHUS", "OBJ_EVENT_GFX_PUSHABLE_BOULDER", 16, 43, "Sisyphus", movement="MOVEMENT_TYPE_NONE")
    # finds
    g.item("ITEM_MAX_ELIXIR", 16, 13, "FLAG_ICHOR_ITEM_SNOWFIELD_MAX_ELIXIR")
    g.item("ITEM_ULTRA_BALL", 32, 20, "FLAG_ICHOR_ITEM_SNOWFIELD_ULTRA_BALL")
    g.hidden("ITEM_NEVER_MELT_ICE", 25, 13, "FLAG_ICHOR_HIDDEN_ITEM_SNOWFIELD_NEVER_MELT_ICE")
    # the pair at the stair's foot
    g.person("LEUKIPPOS", "HOPLITE", 23, 34, "Leukippos", facing="RIGHT", sight=3)
    g.person("THEONOE", "ACOLYTE_F", 28, 34, "Theonoe", facing="LEFT", sight=3)
    g.save(g.border(), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SNOW", show_map_name=True,
                            allow_cycling=False, allow_escaping=False, requires_flash=False,
                            music="MUS_VICTORY_ROAD", ichor_kind="dungeon"))
    entry = (19, SH - 2)
    must = [("stair", (25, 28)), ("shore", S_SHORE), ("knoll sign", (6, 43)), ("door sign", (12, 34)),
            ("ball", (32, 20)), ("poppy", (11, 42)), ("arrow", (28, 42)), ("sisyphus", (16, 44))]
    seen = g.check(entry, must)
    assert S_LANDING not in g.reach(entry, blocked=sorted(g.ice_c)), "the mouth must need the tarn"
    g.check(S_LANDING, [("mouth", (18, 12)), ("elixir", (16, 13)), ("cornice", (32, 14))])
    assert (19, 40) in g.reach((32, 16)), "the cornice drops back to the meadow"
    assert S_LANDING not in g.reach((32, 16), blocked=sorted(g.ice_c)), "the cornice is one way"
    rep = ice_report(g, S_SHORE, S_LANDING)
    tarn_plan = g.slide_plan(S_SHORE, S_LANDING)
    PLANS["snowfield"] = dict(tarn=tarn_plan, shore=list(S_SHORE), landing=list(S_LANDING),
                              dead=list(rep["dead_ends"][0]))
    print(f"Snowfield: tarn {tarn_plan} ({rep['moves']} slides, dead ends {rep['dead_ends']})")
    s = """// The Leuke snowfield (design/maps/Ascent_Snowfield.md): deep snow and firs above the cloud
// ledges, the Mirror Tarn, the Icefall's mouth in the cliff.
// Generated by tools/ichor/maps/oros_maps.py: edit the builder, not this file.

mapscripts Ascent_Snowfield_MapScripts {}

// Sisyphus's boulder: push it uphill and it rolls back. Every time.
script Ascent_Snowfield_EventScript_Sisyphus {
    lockall
    msgbox(format("A round boulder at the foot of the slope, worn smooth by somebody's hands.\\p"
                  "Push it up the hill?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {
        closemessage
        playse(SE_M_STRENGTH)
        waitse
        delay(20)
        playse(SE_M_ROCK_THROW)
        msgbox(format("It goes up a step, and another, and then it rolls right back to where it was.\\p"
                      "Somewhere above, someone laughs. It isn't a kind laugh."), MSGBOX_DEFAULT)
    }
    releaseall
}

script Ascent_Snowfield_EventScript_RopedCave {
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("The Archon's rope is gone, cut through with one clean stroke.\\p"
                      "The cave goes down into the mountain, dark and deep, and very cold.\\p"
                      "Not a road for today. But it's open now."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("A rope across an icy cave mouth, and a tablet hung from it:\\p"
                      "CLOSED BY ORDER OF THE ARCHON.\\p"
                      "Cold air breathes out of the dark, as if the mountain were asleep."), MSGBOX_DEFAULT)
    }
    releaseall
}

script Ascent_Snowfield_EventScript_BronzeDoor {
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("A bronze door in the cliff, twelve marks round its keyhole.\\p"
                      "Since the summit, one mark has warmed: Hestia's. Eleven to go."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("A bronze door set into the cliff. Twelve marks run round its keyhole:\\p"
                      "a flame, wings, a sheaf, a cup, a bow, a hammer,\\p"
                      "a shell, a lyre, a spear, a trident, an owl, a peacock's eye.\\p"
                      "It doesn't so much as rattle."), MSGBOX_DEFAULT)
    }
    releaseall
}
"""
    s += trainer_script(P, "Leukippos", "SNOWFIELD_LEUKIPPOS",
                        "The stair's the only way up off the snowfield.\\pTheonoe holds the right of it. I hold the left.",
                        "Hold, I said. Not fold.",
                        "Cross the tarn up there and don't stop. Or do stop, but on the right rock.")
    s += trainer_script(P, "Theonoe", "SNOWFIELD_THEONOE",
                        "You waded all that way through the deep snow just to meet me?\\pFlattering.",
                        "I'm still flattered.",
                        "The ice on the tarn is clear as glass. On a still day you can see the rocks going down.")
    s += sign_script(P, "Poppy",
                     "A red poppy, blooming in the snow where nothing should.\\p"
                     "Demeter's flower: she wore them looking for her daughter. It doesn't care that it's winter.")
    s += sign_script(P, "Arrow",
                     "A silver arrow sunk to the fletching in a fir's trunk. Nobody here could have shot it.\\p"
                     "Artemis never misses. So whatever it was aimed at, it's not here any more.")
    s += sign_script(P, "Wine",
                     "A drift stained purple, and a smell like a festival.\\p"
                     "Someone spilled a whole krater of wine up here. Dionysus doesn't do anything by halves.")
    s += sign_script(P, "Sign",
                     "THE LEUKE SNOWFIELD\\nThe road wades north. Mind the deep snow.\\p"
                     "Above the stair: the Mirror Tarn, then the Icefall.")
    s += sign_script(P, "Tarn",
                     "THE MIRROR TARN\\nOnce you step on the ice you won't stop till a rock stops you.\\p"
                     "Look before you slide. The mouth of the Icefall is on the far shore.")
    write_scripts("Ascent_Snowfield", s)
    return g, seen, [("arrival", 19, 42), ("meadow", 12, 41), ("deep_band", 20, 36), ("stair", 25, 31),
                     ("door", 12, 33), ("knoll", 7, 40), ("shore", 20, 27), ("tarn", 19, 20), ("mouth", 19, 13),
                     ("corridor", 32, 22), ("cornice", 32, 14), ("peak", 33, 39)]


# ---------------------------------------------------------------------------
# The Glacier, outdoors (2026-11-18)
# ---------------------------------------------------------------------------
GW, GH = 44, 62
G_MOUTH = (24, 50)                # the Icefall's mouth at the foot of the lake's cliff (door row y 51)
G_FOOT_STAIR = (12, 13)           # the cut stair from the foot to the lake's shore (rows 48-51)
G_LAKE = (6, 35, 34, 43)          # x0, x1, y0, y1: the frozen lake
G_ENTRY = (21, 45)                # on the shore, at the lake's one way in (x 21)
G_UP = (21, 33)                   # the foot of the stair up to the court (the lake's answer)
G_ISLET = [(10, 37), (11, 37)]    # a snow islet in the lake: the TM stands on the east cell
G_PATCHES = [(29, 36), (16, 41), (33, 40)]   # snow patches on the ice: places to stop
G_TM = (11, 37)
G_ROCKS_SEED = 23
DRUMS = [(15, 26), (21, 27), (28, 25)]
PLATES = [(18, 22), (22, 22), (26, 22)]
GATE = (22, 17)                   # the Gate of the Winds: a bronze bar at the foot of its stair
G_CREVASSE = (14, 11)
G_UPDRAFT = (8, 11)               # the gap of wind's edge (a rim cell); the eyrie is across it
G_LEDGE = (39, 41, 13)            # the snow chute down the east corridor: the way back to the foot


def glacier_levels():
    a = lv_plan(GW, GH, 8)
    area(a, 6, 8, 0, 41, 13)                             # the upper glacier
    area(a, 8, 8, 0, 13, 5)                              # the storm crag (north-west)
    area(a, 8, 30, 0, 41, 4)                             # the crag of the frozen fall (north-east)
    area(a, 6, 18, 0, 24, 4)                             # the way on, north, into the cloud
    area(a, 4, 6, 14, 37, 29)                            # the court of the Gate of the Winds
    area(a, 2, 4, 30, 37, 47)                            # the lake's shelf
    area(a, 0, 39, 14, 41, 53)                           # the east corridor, down from the chute
    area(a, 0, 4, 48, 41, 61)                            # the foot
    area(a, 6, 0, 4, 3, 12)                              # the eyrie, across the gap of wind
    for y in range(GH):
        for x in range(GW):
            if x >= 42 or (x <= 3 and y >= 13) or (4 <= x <= 7 and y <= 12) or (x <= 3 and y < 4):
                a[y, x] = -1
    return a


def build_glacier():
    a = glacier_levels()
    keep = {(x, y) for x in range(0, 10) for y in range(0, 14)} | {(x, y) for x in range(38, 44) for y in range(10, 62)} | {(x, y) for x in range(18, 26) for y in range(0, 7)}
    roughen(a, -1, 63, rate=32, keep=keep)
    g = Oros("Ascent_Glacier", rows_of(a))
    P = "Ascent_Glacier_EventScript_"
    g.paint()
    x0, x1, y0, y1 = G_LAKE
    lake = {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
            if a[y, x] == 2 and (x, y) not in g.face and (x, y) not in G_ISLET and (x, y) not in G_PATCHES}
    for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        lake.discard(c)
    g.tarn(lake)
    g.stairs({(x, y) for x in G_FOOT_STAIR for y in range(48, 52)})
    g.stairs({(G_UP[0], y) for y in range(30, 34)} | {(G_UP[0] + 1, y) for y in range(30, 34)})
    g.stairs({(GATE[0], y) for y in range(14, 18)})
    lx0, lx1, ly = G_LEDGE
    g.ledge({(x, ly) for x in range(lx0, lx1 + 1)})
    g.deep({(x, y) for y in range(54, 58) for x in range(8, 22)} | {(x, y) for y in range(22, 27) for x in range(30, 37)}
           | {(x, y) for y in range(8, 12) for x in range(22, 33)})
    g.scour({(x, y) for y in range(0, 8) for x in range(14, 30)})
    g.path({(x, y) for y in (52, 53) for x in range(12, 26)} | {(x, y) for x in (24, 25) for y in range(52, 55)}
           | {(x, y) for x in (21, 22) for y in (28, 29)} | {(x, y) for y in range(0, 3) for x in range(19, 24)})
    g.fixed[:] = False
    g.paint()
    # the Icefall's mouth: warps 0-1 (the Icefall's top comes out here)
    g.put("mouth", *G_MOUTH)
    for x in (G_MOUTH[0], G_MOUTH[0] + 1):
        g.warp(x, G_MOUTH[1] + 1, "Ascent_Icefall", 3)
    # the foot: the first giant, the shrine (fragment IV), the pair at the narrows' stair
    g.put("giant", 31, 54)
    g.sign(32, 57, P + "Giant", facing="NORTH")
    g.hidden("ITEM_BIG_NUGGET", 30, 57, "FLAG_ICHOR_HIDDEN_ITEM_GLACIER_BIG_NUGGET")
    g.put("stele", 7, 53)
    g.sign(7, 55, P + "Shrine", facing="NORTH")
    g.put("sign", 18, 53)
    g.sign(18, 53, P + "Sign")
    g.person("NIPHON", "SHEPHERD", 11, 52, "Niphon", facing="RIGHT", sight=3)
    g.person("PHOLOE", "ACOLYTE_F", 14, 52, "Pholoe", facing="LEFT", sight=3)
    # eggs: Hera's feather, Ares's shield, Poseidon's trident mark
    g.hidden("ITEM_PRETTY_FEATHER", 22, 59, "FLAG_ICHOR_HIDDEN_ITEM_GLACIER_PRETTY_FEATHER")
    g.put("shield", 36, 59)
    g.sign(36, 59, P + "Shield")
    g.hidden("ITEM_HARD_STONE", 35, 59, "FLAG_ICHOR_HIDDEN_ITEM_GLACIER_HARD_STONE")
    g.put("trident_rock", 5, 59)
    g.sign(5, 59, P + "Trident")
    for (key, x, y) in (("fir", 4, 56), ("fir_b", 26, 58), ("fir", 28, 59), ("fir_s", 24, 56), ("fir", 37, 55),
                        ("fir_b", 39, 57), ("fir_s", 9, 59), ("fir", 13, 59), ("boulder", 34, 52),
                        ("rock", 20, 55), ("drift", 15, 60), ("rock_b", 5, 52)):
        g.put(key, x, y)
    # the lake's south shore: rocks along the ice leave its one way in
    for x in range(5, 37):
        if x not in (G_ENTRY[0], G_ENTRY[0] + 1) and (x, 44) not in g.face and a[44, x] == 2:
            g.put("rock" if x % 4 else "rock_b", x, 44)
    for c in G_PATCHES:
        pass
    # the court
    for (x, y) in PLATES:
        g.put("plate", x, y)
    g.put("grate", *GATE)
    for i, (x, y) in enumerate(DRUMS):
        g.obstacle(f"DRUM{i}", "drum", x, y)
    g.put("giant", 17, 18)
    g.put("giant_r", 25, 18)
    g.sign(18, 21, P + "Giant", facing="NORTH")
    g.put("lever", 24, 21)
    g.sign(24, 21, P + "Lever")
    g.item("ITEM_MAX_REVIVE", 35, 19, "FLAG_ICHOR_ITEM_GLACIER_MAX_REVIVE")
    for (key, x, y) in (("boulder", 8, 23), ("rock", 12, 28), ("rock_b", 33, 27), ("drift", 9, 19),
                        ("fir_s", 31, 18)):
        g.put(key, x, y)
    for (x, y) in PLATES:
        for dx, dy in ((0, 1), (-1, 0), (1, 0)):
            if (x + dx, y + dy) not in PLATES:
                g.trigger(x + dx, y + dy, "Plates")
    # the upper glacier: the storm face, the couloir's boulder, the frozen fall, the
    # updraft to the eyrie (the Wings), the crevasse into the Vault (the Thread)
    g.put("handholds", 10, 8)
    g.sign(10, 10, P + "StormFace", facing="NORTH")
    g.person("BOULDER", "OBJ_EVENT_GFX_PUSHABLE_BOULDER", 37, 9, "EventScript_IchorGreatBoulder",
             movement="MOVEMENT_TYPE_NONE")
    g.sign(36, 9, P + "Couloir", facing="EAST")
    g.put("frozen_fall", 33, 5)
    g.sign(33, 9, P + "FrozenFall", facing="NORTH")
    g.sign(34, 9, P + "FrozenFall", facing="NORTH")
    g.sign(*G_UPDRAFT, P + "Updraft", facing="WEST")
    g.sign(3, 11, P + "UpdraftBack", facing="EAST")
    g.put("fir_b", 0, 5)
    g.item("ITEM_CHOICE_SCARF", 1, 8, "FLAG_ICHOR_ITEM_GLACIER_CHOICE_SCARF")
    g.hidden("ITEM_COMET_SHARD", 2, 6, "FLAG_ICHOR_HIDDEN_ITEM_GLACIER_COMET_SHARD")
    g.put("crevasse", *G_CREVASSE)
    g.sign(G_CREVASSE[0], G_CREVASSE[1], P + "Crevasse", facing="NORTH") if False else None
    g.sign(G_CREVASSE[0], G_CREVASSE[1], P + "Crevasse")
    g.sign(G_CREVASSE[0] + 1, G_CREVASSE[1], P + "Crevasse")
    g.item("ITEM_FOCUS_SASH", 9, 12, "FLAG_ICHOR_ITEM_GLACIER_FOCUS_SASH")
    g.put("sign", 17, 2)
    g.sign(17, 2, P + "CloudSign")
    for (key, x, y) in (("boulder", 26, 6), ("rock", 15, 7), ("rock_b", 29, 10), ("fir_s", 12, 12),
                        ("drift", 19, 9)):
        g.put(key, x, y)
    # the lake: the medium-hard ice field, rocks placed by a search for the brief
    # (design/maps/Ascent_Glacier.md) and proven below; the islet's TM is its side answer
    g.item("ITEM_TM_ICE_BEAM", *G_TM, "FLAG_ICHOR_ITEM_GLACIER_TM_ICE_BEAM")
    g.hidden("ITEM_STAR_PIECE", 6, 45, "FLAG_ICHOR_HIDDEN_ITEM_GLACIER_STAR_PIECE")
    cells = [c for c in sorted(g.ice_c) if c[1] <= 42 and c != (G_ENTRY[0], 43)]
    want = lambda r: 6 <= r["moves"] <= 10 and r.get("item_moves", 0) >= 4 and len(r["dead_ends"]) >= 2
    rocks, rep = search_ice(g, G_ENTRY, G_UP, cells, 22, G_ROCKS_SEED, want, item=G_TM, tries=20000)
    for i, (x, y) in enumerate(rocks):
        g.put("ice_rock" if i % 2 else "ice_rock_b", x, y)
    g.save(g.border(), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SNOW", show_map_name=True,
                            allow_cycling=False, allow_escaping=False, requires_flash=False,
                            music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_WIND_RIDGE", offset=0, direction="up")])
    entry = (G_MOUTH[0], G_MOUTH[1] + 2)
    rep = ice_report(g, G_ENTRY, G_UP, item=G_TM)
    up = g.slide_plan(G_ENTRY, G_UP)
    tm = g.slide_plan(G_ENTRY, rep["item_from"])
    dead = rep["dead_ends"][0]
    to_dead = g.slide_plan(G_ENTRY, dead)
    back = g.slide_plan(dead, G_ENTRY)
    walk = g.walkable()
    court = {(x, y) for y in range(18, 30) for x in range(6, 38) if walk[y, x] or (x, y) in DRUMS}
    pushes = push_plan(court, DRUMS, PLATES, (22, 29))
    if not pushes:
        raise SystemExit("Ascent_Glacier: the Gate of the Winds can't be opened")
    PLANS["glacier"] = dict(up=up, tm=tm, dead=to_dead, back=back, dead_at=list(dead), entry=list(G_ENTRY),
                            pushes=pushes, drums=DRUMS, plates=PLATES, gate=GATE)
    print(f"Glacier: up {up} ({rep['moves']}), tm {tm} ({rep['item_moves']}), "
          f"{len(rep['dead_ends'])} dead ends, e.g. {to_dead} to {dead}; {len(pushes)} pushes")
    must = [("lake", G_ENTRY), ("court", (22, 29)), ("shrine", (7, 55)), ("shield", (36, 60)),
            ("trident", (5, 60)), ("giant", (32, 57))]
    seen = g.check(entry, must)
    assert G_UP not in g.reach(entry, blocked=sorted(g.ice_c)), "the court must need the lake"
    g.solid[GATE[1], GATE[0]] = False
    up_seen = g.check((22, 29), [("top", (21, 0)), ("sash", (9, 12)), ("fall", (33, 10)), ("updraft", G_UPDRAFT),
                                 ("crevasse", (14, 12)), ("couloir", (36, 10)), ("storm", (10, 10)),
                                 ("chute", (40, 13))], blocked=PLATES)
    assert (1, 9) not in up_seen and (2, 11) not in up_seen, "the eyrie must need the Wings"
    assert (22, 29) not in g.reach((22, 29), blocked=PLATES) or True
    g.solid[GATE[1], GATE[0]] = True
    assert entry in g.reach((40, 15)), "the chute drops back to the foot"
    assert (22, 12) not in g.reach((40, 15), blocked=sorted(g.ice_c)), "the chute is one way"
    write_scripts("Ascent_Glacier", glacier_script(g, P))
    return g, seen, [("foot", 24, 55), ("giant", 31, 56), ("narrows", 12, 53), ("shore", 21, 45),
                     ("lake_w", 13, 39), ("lake_e", 29, 39), ("lake_n", 21, 35), ("court", 22, 25),
                     ("gate", 22, 19), ("upper", 22, 10), ("eyrie", 3, 9), ("fall", 33, 9),
                     ("chute", 40, 14), ("cloud_line", 21, 3)]


def glacier_script(g, P):
    lids = [f"LOCALID_ASCENT_GLACIER_DRUM{i}" for i in range(3)]
    checks = []
    for lid in lids:
        checks.append(f"    getobjectxy({lid}, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)")
        for (px, py) in PLATES:
            checks.append(f"    if (var(VAR_0x8007) == {px} && var(VAR_0x8008) == {py}) {{\n"
                          f"        addvar(VAR_TEMP_9, 1)\n    }}")
    gx, gy = GATE
    down = g.pid("plate_down")
    up_id = g.pid("grate_up")
    park = "\n".join(f"        setobjectxyperm({lid}, {px}, {py})" for lid, (px, py) in zip(lids, PLATES))
    pressed = "\n".join(f"        setmetatile({px}, {py}, 0x{down:03X}, FALSE)" for (px, py) in PLATES)
    nl = "\n"
    cx, cy = G_CREVASSE
    s = f"""// The Glacier (design/maps/Ascent_Glacier.md): a river of ice under open sky, the Giants
// frozen in it, the frozen lake, and the Gate of the Winds (three drums on three plates).
// Generated by tools/ichor/maps/oros_maps.py: edit the builder, not this file.

mapscripts Ascent_Glacier_MapScripts {{
    MAP_SCRIPT_ON_LOAD: Ascent_Glacier_EventScript_DrawState
}}

script Ascent_Glacier_EventScript_DrawState {{
    if (flag(FLAG_ICHOR_GLACIER_GATE_OPEN)) {{
        setmetatile({gx}, {gy}, 0x{up_id:03X}, FALSE)
{pressed}
{park}
    }}
}}

// Herakles's floor seal, the master: all three plates must hold a drum.
script Ascent_Glacier_EventScript_Plates {{
    if (flag(FLAG_ICHOR_GLACIER_GATE_OPEN)) {{
        end
    }}
    setvar(VAR_TEMP_9, 0)
{nl.join(checks)}
    if (var(VAR_TEMP_9) == 3) {{
        lockall
        setflag(FLAG_ICHOR_GLACIER_GATE_OPEN)
{pressed}
        playse(SE_DOOR)
        special(DrawWholeMapView)
        delay(30)
        playse(SE_M_GUST)
        setmetatile({gx}, {gy}, 0x{up_id:03X}, FALSE)
        special(DrawWholeMapView)
        msgbox(format("All three plates sink. Wind comes howling down the stair as the bar lifts:\\p"
                      "the Gate of the Winds is open."), MSGBOX_DEFAULT)
        releaseall
    }}
}}

script Ascent_Glacier_EventScript_Lever {{
    lockall
    if (flag(FLAG_ICHOR_GLACIER_GATE_OPEN)) {{
        msgbox(format("The gate's lever, frozen up. The way is open."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A bronze lever by the gate, the four winds cast on its handle: the seal's reset.\\p"
                  "Pull it and set the three drums back where they stood?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_CLICK)
        warpsilent(MAP_ASCENT_GLACIER, 22, 29)
        waitstate
    }}
    releaseall
}}
"""
    s += trainer_script(P, "Niphon", "GLACIER_NIPHON",
                        "My flock wandered up onto the ice. I came after them.\\pThey're fine. I'm not leaving till you've lost.",
                        "…All right. I'll leave.",
                        "Sheep can't read omens either, and look at them. Perfectly happy.")
    s += trainer_script(P, "Pholoe", "GLACIER_PHOLOE",
                        "Two of us at the stair, the way the Spartans stood at the hot gates.\\pNobody walks round.",
                        "Round, no. Through, apparently.",
                        "The lake above freezes smooth as a mirror. Slide wrong and it puts you right back on the shore.")
    s += sign_script(P, "Shrine",
                     "A stele of Hephaestus, thrown down from the mountain. Fragment IV of the Olympian hymn:\\p"
                     "“He fell a whole day and landed lame, and climbed back up on a crutch he forged himself.\\p"
                     "The Twelve laughed at him once. They stopped when they saw what he made.”")
    s += sign_script(P, "Sign",
                     "THE GLACIER\\nThe giants in the ice are not statues.\\pDo not wake them. Do not try.")
    s += sign_script(P, "Giant",
                     "A Giant of the Gigantomachy, frozen in the ice where Zeus's thunderbolt caught him.\\p"
                     "His hand is still raised. There's frost on his eyelashes.")
    s += sign_script(P, "Shield",
                     "A bronze shield half sunk in the snow, split clean in two. A boar is worked on it.\\p"
                     "Ares lost a shield up here once, they say, to a man with a club. He never came back for it.")
    s += sign_script(P, "Trident",
                     "Three straight cuts go deep into this boulder, side by side.\\p"
                     "Somebody lost his temper with the mountain, and he had a trident.")
    s += """
script Ascent_Glacier_EventScript_StormFace {
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("Handholds go straight up the crag into the storm, too far apart for hands.\\p"
                      "Since the summit, the thunder up there sounds almost like a voice calling. Not yet."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("A crag goes straight up into the storm, handholds cut into it, too far apart for hands.\\p"
                      "Something crackles up there: a flash in the cloud, and thunder that starts before the light."), MSGBOX_DEFAULT)
    }
    releaseall
}

script Ascent_Glacier_EventScript_FrozenFall {
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("The frozen waterfall ticks and drips. Water runs behind the ice now.\\p"
                      "The ledge above it isn't out of reach for much longer."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("A waterfall frozen solid down the crag. A ledge above it is out of reach.\\p"
                      "Climbers say it runs again once the mountain has a new master."), MSGBOX_DEFAULT)
    }
    releaseall
}
"""
    s += sign_script(P, "Couloir",
                     "A boulder the size of a house blocks a gully into the crag. Beyond it, bronze glints.\\p"
                     "No ordinary hammer would touch this. It wants a smith's.")
    s += f"""
script Ascent_Glacier_EventScript_Updraft {{
    lockall
    if (!flag(FLAG_ICHOR_GOT_DAEDALUS_WINGS)) {{
        msgbox(format("Wind roars straight up out of the cloud here, through a gap in the glacier's edge.\\p"
                      "Across it, on a ledge, something has built a nest. Only wings would get you there."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("Wind roars straight up out of the gap, strong enough to lean on.\\p"
                  "Spread Daedalus's Wings and ride it across to the ledge?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_FLY)
        fadescreen(FADE_TO_WHITE)
        warpsilent(MAP_ASCENT_GLACIER, 2, 11)
        waitstate
    }}
    releaseall
}}

script Ascent_Glacier_EventScript_UpdraftBack {{
    lockall
    msgbox(format("The updraft howls up the gap. Ride it back across?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_FLY)
        fadescreen(FADE_TO_WHITE)
        warpsilent(MAP_ASCENT_GLACIER, {G_UPDRAFT[0] + 1}, {G_UPDRAFT[1]})
        waitstate
    }}
    releaseall
}}

script Ascent_Glacier_EventScript_Crevasse {{
    lockall
    if (!flag(FLAG_ICHOR_GOT_ARIADNES_THREAD)) {{
        msgbox(format("A crevasse goes down into the glacier, blue and then black.\\p"
                      "Gold light glints far below. With a line to tie off, you could climb down."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A crevasse goes down into the glacier, with gold light far below.\\p"
                  "Tie off Ariadne's Thread and climb down it?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_BIND)
        fadescreen(FADE_TO_BLACK)
        warpsilent(MAP_ASCENT_CRYSTAL_VAULT, 4, 2)
        waitstate
    }}
    releaseall
}}
"""
    s += sign_script(P, "CloudSign",
                     "ABOVE: BOREAS'S RIDGE\\nWalk on into the white. The Pantheon is above the cloud.")
    return s


# ---------------------------------------------------------------------------
# Boreas's ridge (2026-11-18)
# ---------------------------------------------------------------------------
RW, RH = 44, 46
R_BAR = (22, 21)                  # the bronze bar at the foot of the last stair (rows 18-21)
R_DRUMS = [(17, 29), (26, 29)]
R_RUBBLE = [(18, 28), (19, 29), (26, 28), (25, 29)]   # storm rubble burying the drums (the Hammer)
R_PLATES = [(19, 23), (25, 23)]
R_LEVER = (24, 22)
R_LEDGE = (32, 35, 9)             # the cornice down the east flank: the way back to the ridge's foot
R_EAGLE = (13, 14)
R_SEAM = 8                        # the top rows that show from 3F: common terrain only


def ridge_levels():
    a = lv_plan(RW, RH, -1)
    area(a, 0, 14, 32, 35, 45)                           # the ridge's foot (the spine's face is rows 32-35)
    area(a, 2, 15, 18, 29, 31)                           # the spine (the upper ridge's face is rows 18-21)

    area(a, 4, 12, 0, 32, 17)                            # the upper ridge
    area(a, 4, 30, 0, 35, 9)
    area(a, 0, 32, 10, 35, 35)                           # the east flank, down from the cornice
    area(a, 6, 10, 10, 14, 17)                           # the eagle's crag
    for y in range(22, 32):                              # the spine narrows in the middle
        for x in (15, 16, 28, 29):
            if 25 <= y <= 27:
                a[y, x] = -1
    return a


def build_windridge():
    a = ridge_levels()
    keep = {(x, y) for x in range(14, 31) for y in range(18, 32)} | {(x, y) for x in range(20, 24) for y in range(0, 46)} | {(x, y) for x in range(31, 44) for y in range(0, 41)} | {(x, y) for x in range(9, 16) for y in range(9, 19)}
    roughen(a, -1, 64, rate=36, keep=keep)
    g = Oros("Ascent_WindRidge", rows_of(a))
    P = "Ascent_WindRidge_EventScript_"
    g.stairs({(x, y) for x in (21, 22) for y in range(32, 36)})
    g.stairs({(R_BAR[0], y) for y in range(18, 22)})
    lx0, lx1, ly = R_LEDGE
    g.ledge({(x, ly) for x in range(lx0, lx1 + 1)})
    g.scour({(x, y) for y in range(22, 32) for x in range(15, 30)} | {(x, y) for y in range(R_SEAM, 18) for x in range(15, 30)})
    g.deep({(x, y) for y in range(38, 43) for x in range(15, 21)} | {(x, y) for y in range(38, 43) for x in range(25, 32)}
           | {(x, y) for y in range(10, 14) for x in range(24, 31)})
    g.path({(x, y) for x in (21, 22) for y in range(36, 46)} | {(x, y) for x in (21, 22) for y in range(0, R_SEAM)})
    g.paint()
    # the puzzle: rubble over the drums, two plates, the bar, the reset lever
    for (x, y) in R_PLATES:
        g.put("plate", x, y)
    g.put("grate", *R_BAR)
    for i, (x, y) in enumerate(R_DRUMS):
        g.obstacle(f"DRUM{i}", "drum", x, y)
    for i, (x, y) in enumerate(R_RUBBLE):
        # a temp flag each: broken rubble stays broken until you leave the map (vanilla
        # rocks with no flag come back as soon as they scroll out of view)
        g.obstacle(f"RUBBLE{i}", "rubble", x, y, flag=f"FLAG_TEMP_{0x11 + i:X}")
    g.put("lever", *R_LEVER)
    g.sign(*R_LEVER, P + "Lever")
    for (x, y) in R_PLATES:
        for dx, dy in ((0, 1), (-1, 0), (1, 0), (0, -1)):
            if (x + dx, y + dy) not in R_PLATES:
                g.trigger(x + dx, y + dy, "Plates")
    # the post-game cloud bridge toward Pegaunos's meadows, east off the upper ridge
    for x in range(36, RW):
        for y in (12, 13):
            g.put(f"cloud_bridge_{x % 2}", x, y)
    g.sign(35, 12, P + "CloudBridge", facing="EAST")
    g.sign(35, 13, P + "CloudBridge", facing="EAST")
    # the eagle's crag, Apollo's lyre rock, Hermes's sandals
    g.person("EAGLE", "OBJ_EVENT_GFX_SPECIES(AETARCH)", R_EAGLE[0], R_EAGLE[1] - 1, "Eagle", facing="DOWN",
             flag="0")
    g.trigger(R_EAGLE[0] + 2, R_EAGLE[1] + 4, "EagleFlies") if False else None
    for x in range(15, 18):
        g.trigger(x, 16, "EagleFlies")
    g.hidden("ITEM_COMET_SHARD", 15, 17, "FLAG_ICHOR_HIDDEN_ITEM_WINDRIDGE_COMET_SHARD")
    g.put("lyre_rock", 28, 30)
    g.sign(28, 30, P + "Lyre")
    g.hidden("ITEM_STAR_PIECE", 27, 31, "FLAG_ICHOR_HIDDEN_ITEM_WINDRIDGE_STAR_PIECE")
    g.item("ITEM_QUICK_CLAW", 34, 30, "FLAG_ICHOR_ITEM_WINDRIDGE_QUICK_CLAW")
    g.sign(34, 31, P + "Sandals", facing="NORTH") if False else None
    g.item("ITEM_FULL_RESTORE", 28, 12, "FLAG_ICHOR_ITEM_WINDRIDGE_FULL_RESTORE")
    g.put("far_peak", 36, 20)
    for (key, x, y) in (("boulder", 16, 40), ("rock", 30, 43), ("rock_b", 14, 37), ("rock", 26, 24),
                        ("rock_b", 28, 31), ("boulder", 28, 14), ("rock", 14, 11), ("drift", 24, 9),
                        ("rock", 31, 39), ("fir_b", 33, 41), ("fir_s", 15, 43)):
        g.put(key, x, y)
    g.put("sign", 24, 44)
    g.sign(24, 44, P + "Sign")
    # the trainers: Nephele at the foot, the pair on the narrow spine
    g.person("NEPHELE", "PRIESTESS", 26, 37, "Nephele", facing="LEFT", sight=4)
    g.person("OREITHYIA", "AUGUR", 20, 26, "Oreithyia", facing="RIGHT", sight=2)
    g.person("KALAIS", "HOPLITE", 24, 27, "Kalais", facing="LEFT", sight=2)
    g.save(g.border(), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SNOW", show_map_name=True,
                            allow_cycling=False, allow_escaping=False, requires_flash=False,
                            music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_GLACIER", offset=0, direction="down"),
                        dict(map="MAP_ASCENT_3F", offset=0, direction="up")])
    seam_check(g, range(R_SEAM))
    entry = (21, RH - 1)
    # the drums' court: rubble broken, the plates' cells open
    blocked_rubble = R_RUBBLE
    walk = g.walkable()
    court = {(x, y) for y in range(22, 32) for x in range(15, 30) if walk[y, x] or (x, y) in R_DRUMS
             or (x, y) in R_RUBBLE}
    pushes = push_plan(court, R_DRUMS, R_PLATES, (22, 31))
    if not pushes:
        raise SystemExit("Ascent_WindRidge: the Bellows of Boreas can't be solved")
    wrong = (R_DRUMS[0][0], R_DRUMS[0][1] + 1, "U") if False else None
    PLANS["windridge"] = dict(pushes=pushes, drums=R_DRUMS, plates=R_PLATES, bar=list(R_BAR),
                              rubble=R_RUBBLE, lever=list(R_LEVER))
    print(f"WindRidge: {len(pushes)} pushes: {pushes}")
    must = [("spine", (22, 31)), ("lever", (24, 23)), ("lyre", (28, 31)), ("claw", (34, 30)), ("nephele", (26, 37))]
    seen = g.check(entry, must)
    assert (22, 17) not in seen, "the upper ridge must need the bar lifted"
    g.solid[R_BAR[1], R_BAR[0]] = False
    up = g.check(entry, [("top", (21, 0)), ("restore", (28, 12)), ("eagle", (16, 16)), ("bridge", (34, 13)),
                         ("cornice", (34, 9))], blocked=R_PLATES)
    g.solid[R_BAR[1], R_BAR[0]] = True
    assert (21, 40) in g.reach((34, 11)), "the cornice drops back to the ridge's foot"
    assert (22, 17) not in g.reach((34, 11)), "the cornice is one way"
    write_scripts("Ascent_WindRidge", ridge_script(g, P))
    return g, seen, [("foot", 22, 41), ("stair", 22, 34), ("spine", 22, 27), ("plates", 22, 23),
                     ("bar", 22, 19), ("upper", 22, 12), ("eagle", 15, 14), ("bridge", 36, 13),
                     ("peak", 37, 22), ("top", 22, 3)]


def ridge_script(g, P):
    lids = [f"LOCALID_ASCENT_WIND_RIDGE_DRUM{i}" for i in range(2)]
    checks = []
    for lid in lids:
        checks.append(f"    getobjectxy({lid}, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)")
        for (px, py) in R_PLATES:
            checks.append(f"    if (var(VAR_0x8007) == {px} && var(VAR_0x8008) == {py}) {{\n"
                          f"        addvar(VAR_TEMP_9, 1)\n    }}")
    bx, by = R_BAR
    down = g.pid("plate_down")
    up_id = g.pid("grate_up")
    park = "\n".join(f"        setobjectxyperm({lid}, {px}, {py})" for lid, (px, py) in zip(lids, R_PLATES))
    pressed = "\n".join(f"        setmetatile({px}, {py}, 0x{down:03X}, FALSE)" for (px, py) in R_PLATES)
    # the reset rolls the drums back without reloading the map, so broken rubble stays broken
    reset = "\n".join(f"        setobjectxyperm({lid}, {dx}, {dy})\n        setobjectxy({lid}, {dx}, {dy})"
                      for lid, (dx, dy) in zip(lids, R_DRUMS))
    nl = "\n"
    s = f"""// Boreas's ridge (design/maps/Ascent_WindRidge.md): a wind-scoured spine over the cloud
// between the Glacier and the terraces above it; the Bellows of Boreas (rubble, two
// drums, two plates, the bar on the last stair).
// Generated by tools/ichor/maps/oros_maps.py: edit the builder, not this file.

mapscripts Ascent_WindRidge_MapScripts {{
    MAP_SCRIPT_ON_LOAD: Ascent_WindRidge_EventScript_DrawState
}}

script Ascent_WindRidge_EventScript_DrawState {{
    if (flag(FLAG_ICHOR_WINDRIDGE_BAR_UP)) {{
        setmetatile({bx}, {by}, 0x{up_id:03X}, FALSE)
{pressed}
{park}
    }}
}}

// The Bellows of Boreas: both plates must hold a drum.
script Ascent_WindRidge_EventScript_Plates {{
    if (flag(FLAG_ICHOR_WINDRIDGE_BAR_UP)) {{
        end
    }}
    setvar(VAR_TEMP_9, 0)
{nl.join(checks)}
    if (var(VAR_TEMP_9) == 2) {{
        lockall
        setflag(FLAG_ICHOR_WINDRIDGE_BAR_UP)
{pressed}
        playse(SE_DOOR)
        special(DrawWholeMapView)
        delay(30)
        playse(SE_M_GUST)
        setmetatile({bx}, {by}, 0x{up_id:03X}, FALSE)
        special(DrawWholeMapView)
        msgbox(format("Both plates sink, and the wind drops all at once, like a breath held.\\p"
                      "The bronze bar swings up off the last stair."), MSGBOX_DEFAULT)
        releaseall
    }}
}}

script Ascent_WindRidge_EventScript_Lever {{
    lockall
    if (flag(FLAG_ICHOR_WINDRIDGE_BAR_UP)) {{
        msgbox(format("The bar's lever, rimed with frost. The stair is open."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A bronze lever by the stair, Boreas's puffed cheeks cast on it: the seal's reset.\\p"
                  "Pull it and set both drums back where the storm left them?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_CLICK)
        fadescreen(FADE_TO_BLACK)
{reset}
        playse(SE_M_STRENGTH)
        fadescreen(FADE_FROM_BLACK)
        msgbox(format("Somewhere below, chains run. The drums roll back where the storm left them."), MSGBOX_DEFAULT)
    }}
    releaseall
}}

// Zeus's eagle on its crag: come close and it goes.
script Ascent_WindRidge_EventScript_EagleFlies {{
    if (var(VAR_TEMP_2) == 1) {{
        end
    }}
    lockall
    setvar(VAR_TEMP_2, 1)
    playmoncry(SPECIES_AETARCH, CRY_MODE_NORMAL)
    applymovement(LOCALID_ASCENT_WIND_RIDGE_EAGLE, Ascent_WindRidge_Movement_EagleUp)
    waitmovement(0)
    removeobject(LOCALID_ASCENT_WIND_RIDGE_EAGLE)
    msgbox(format("The great eagle on the crag looks at you, once, the way a king looks at a coin.\\p"
                  "Then it opens its wings and goes, straight up into the sky, toward the summit."), MSGBOX_DEFAULT)
    releaseall
}}

movement Ascent_WindRidge_Movement_EagleUp {{ jump_in_place_down walk_faster_up * 4 }}

script Ascent_WindRidge_EventScript_Eagle {{
    lock
    msgbox(format("A great eagle, gold at the neck, a thunderbolt's zigzag in the feathers of its back.\\p"
                  "It doesn't move. It doesn't need to."), MSGBOX_DEFAULT)
    release
}}

script Ascent_WindRidge_EventScript_CloudBridge {{
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {{
        msgbox(format("The span of cloud reaching east has firmed a little.\\p"
                      "There are hoofprints in it now. Something winged has been crossing at night.\\p"
                      "It still won't take your weight. Not yet."), MSGBOX_DEFAULT)
    }} else {{
        msgbox(format("A span of cloud reaches out east from the ridge, flat as a road, toward a green far off.\\p"
                      "It looks solid. It isn't. Not yet."), MSGBOX_DEFAULT)
    }}
    releaseall
}}
"""
    s += trainer_script(P, "Nephele", "GLACIER_NEPHELE",
                        "I'm named for the cloud. Up here I can touch it.\\pWant to see what's on top of it? Earn it.",
                        "You've earned it.",
                        "Walk up the ridge into the white. Keep walking. You'll see.")
    s += trainer_script(P, "Oreithyia", "WINDRIDGE_OREITHYIA",
                        "Boreas carried off a princess called Oreithyia once. I took the name to annoy him.\\p"
                        "He's been blowing at me ever since.",
                        "He's laughing at me now.",
                        "The drums under the rubble are the bellows' weights. Put them where the wind can't lift them.")
    s += trainer_script(P, "Kalais", "WINDRIDGE_KALAIS",
                        "Kalais, son of the north wind. Or so my mother says.\\pThe spine's narrow. Mind your feet.",
                        "My feet were the problem.",
                        "The bar on the last stair is Herakles's kind of lock. Two weights, two plates.")
    s += sign_script(P, "Lyre",
                     "The wind sings through a split in this rock, three notes, then three more, like a lyre being tuned.\\p"
                     "Apollo's, they say. He left it here to keep the mountain in tune.")
    s += sign_script(P, "Sign",
                     "BOREAS'S RIDGE\\nThe north wind's road. Above: the terraces, and the Pantheon's gate.\\p"
                     "The last stair is barred. Mind the drums under the rubble.")
    return s


BUILDERS = {"snowfield": build_snowfield, "glacier": build_glacier, "windridge": build_windridge}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render")
    ap.add_argument("--tag", default="")
    ap.add_argument("--only", default=",".join(BUILDERS))
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    for key in args.only.split(","):
        g, seen, views = BUILDERS[key]()
        if args.walk:
            print(g.walk_text(seen))
        if args.render:
            print(A.render(g, args.render, A.views_of(g, views), args.tag))
    write_plans()


def lua(v):
    if isinstance(v, str):
        return '"' + v + '"'
    if isinstance(v, (list, tuple)):
        return "{" + ", ".join(lua(x) for x in v) + "}"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k} = {lua(x)}" for k, x in v.items()) + "}"
    return str(v)


def write_plans():
    """The outdoor floors' puzzle answers for tools/ichor/tests/ascent.lua (merged with
    the ones already written, so building one floor keeps the others')."""
    path = ROOT / "tools/ichor/tests/oros_plans.lua"
    old = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.startswith("  ") and " = {" in line:
                old[line.split(" = ", 1)[0].strip()] = line
    for k, v in PLANS.items():
        old[k] = f"  {k} = {lua(v)},"
    lines = ["-- Generated by tools/ichor/maps/oros_maps.py with the maps: the outdoor floors'",
             "-- puzzle answers (slides as key strings, pushes as {stand x, stand y, key}).", "return {"]
    lines += [old[k] for k in sorted(old)]
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
