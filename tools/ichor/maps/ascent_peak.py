#!/usr/bin/env python3
"""Olympus_Summit on gTileset_Chion: the altar above the cloud (design/maps/Olympus_Summit.md).

Rebuilt 2026-11-18 from tools/ichor/maps/olympus.py's Aegina version, which
drew the top of the world as a green meadow. Here the summit is what the
Ascent has promised since the cloud line: a snowfield plateau with the sea of
cloud on every side, the great ash altar of Zeus with the bronze box, the
temple of the Twelve behind it facing east over the altar, and two things the
player can see and not yet reach: the last crag of the cone (Pan's Crook's
handholds, the Prime Mover's way) and Pegaunos's cloud meadow off the east
edge. The coordinates the scripts and tests use are kept: the stair from
Hera's seat at (13,25), the Archon at (13,13) before the altar's signs at
(13,12)/(14,12), the temple door at (14,5).

The scripts are hand-written (data/maps/Olympus_Summit/scripts.pory). Run it
with ascent_snow.py (--only summit).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascent_lib as A  # noqa: E402
from ascent_lib import Snow, blob, carve, plan  # noqa: E402
from league_lib import A_STEPS, noise  # noqa: E402

W, H = 28, 26
TEMPLE = (11, 1)            # the temple of the Twelve, 7x5: its door at (14,5)
ALTAR = (12, 11)            # the great altar, 4x2: the signs at (13,12) and (14,12)
ARCHON = (13, 13)
MEADOW = (23, 6)            # Pegaunos's cloud meadow, out on the cloud (the D11 hook)


def mask(x, y):
    """The summit plateau: True on snow or rock, False where the cloud shows.
    Its rim steps; the stair from the Pantheon comes up a narrow spur, and a
    strait of cloud cuts the plateau off from Pegaunos's meadow to the east."""
    if y >= 21:
        return 10 + (y % 2) <= x <= 17 - (y % 2)
    if y >= 17:
        half = 7 + (1 if y % 3 == 0 else 0)
        return abs(x - 13.5) <= half
    if y <= 0:
        return 9 <= x <= 19
    west = 3 + (1 if (y // 2) % 3 == 1 else 0) + (1 if y in (1, 15, 16) else 0)
    east = 20 if 3 <= y <= 10 else 23 - (1 if (y // 2) % 3 == 0 else 0)
    if y in (1, 2):
        east = 21
    return west <= x <= east


def meadow(x, y):
    """Pegaunos's meadow: a lens of snow floating on the cloud, past the strait."""
    mx, my = MEADOW
    return x >= 23 and ((x - mx - 1.5) / 2.4) ** 2 + ((y - my - 1.5) / 2.2) ** 2 <= 1.0


def plan_summit():
    r = plan(W, H)
    for y in range(H):
        for x in range(W):
            if mask(x, y):
                r[y][x] = "."
    # the cone's last crag in the north-west: a stepped mass whose south face
    # carries the handholds; and an ice outcrop on the east rim
    carve(r, "#", 3, 1, 8, 5)
    carve(r, "#", 3, 6, 5, 7)
    r[1][8] = "."
    carve(r, "#", 21, 15, 23, 16)
    return r


def build_summit(PLANS=None):
    g = Snow("Olympus_Summit", plan_summit(), style="glacier")
    P = "Olympus_Summit_EventScript_"
    cloud = A.PIECES["cloud"]
    for y in range(H):
        for x in range(W):
            if not mask(x, y):
                g.set(x, y, cloud["ids"][y % 2][x % 4], True, "cloud")
    # Pegaunos's meadow: snow floating on the cloud, a herm-less island no stair reaches
    for y in range(H):
        for x in range(W):
            if not mask(x, y) and meadow(x, y):
                g.set(x, y, g.pid("snow_glitter" if noise(x, y, 83) < 30 else "snow_ripples"), True, "meadow")
    g.put("pine_snow_s", MEADOW[0] + 1, MEADOW[1])
    # the stair up from the Pantheon (warp 0: Hera's seat arrives here)
    for y in (24, 25):
        for x in (13, 14):
            g.set(x, y, A_STEPS[y - 24], False, "steps")
    g.warp(13, H - 1, "Olympus_SeatOfHera", 1)
    # the sacred way, paved, from the stair to the precinct
    for y in range(14, 24):
        for x in (13, 14):
            g.set(x, y, g.pid("paving" if (x + y) % 2 else "paving_b"), False, "way")
    # the precinct: paving round the altar and up to the temple's steps
    for y in range(6, 14):
        for x in range(10, 18):
            if not g.fixed[y, x]:
                g.set(x, y, g.pid("paving" if (x + y) % 2 else "paving_b"), False, "precinct")
    g.put("temple_twelve", *TEMPLE)
    door = (TEMPLE[0] + 3, TEMPLE[1] + 4)
    g.warp(door[0], door[1], "Olympus_HallOfHeroes", 0)
    g.trigger(door[0], door[1], "TempleDoor")
    g.put("altar_zeus", *ALTAR)
    g.sign(ALTAR[0] + 1, ALTAR[1] + 1, P + "Altar", facing="NORTH")
    g.sign(ALTAR[0] + 2, ALTAR[1] + 1, P + "Altar", facing="NORTH")
    # fire before the temple, the tripods of every Archon along the precinct
    g.put("brazier", 9, 4)
    g.put("brazier", 19, 4)
    for x in (10, 17):
        g.put("tripod", x, 8)
    g.put("herm", 9, 12)
    g.put("herm", 18, 12)
    # the hooks: the crag's handholds (Pan's Crook) and the cloud meadow
    g.put("handholds", 7, 4)
    g.sign(7, 6, P + "Crag", facing="NORTH")
    g.sign(20, 7, P + "Meadow", facing="EAST")
    # the Archons' stelai on the west terrace: a name for every Archon since Medon,
    # the last stone still blank
    for x in (5, 7, 9):
        g.put("shrine", x, 15)
    g.sign(7, 17, P + "Stelai", facing="NORTH")
    # the rim: ice boulders and crystals break its edges; the frozen offerings
    for key, x, y in (("ice_boulders", 4, 12), ("ice_rock", 20, 11), ("crystal_tall", 20, 1),
                      ("ice_rock", 7, 18), ("crystal_s", 19, 19), ("ice_rock", 6, 9),
                      ("ice_boulders", 19, 14), ("crystal_s", 9, 1), ("ice_rock", 22, 18)):
        g.put(key, x, y)
    g.accents(salt=84, rate=7)
    g.person("ARISTEIDES", "ELDER_M", ARCHON[0], ARCHON[1], "Aristeides", facing="DOWN",
             flag="FLAG_ICHOR_HIDE_ARCHON_SUMMIT")
    cl = cloud["ids"]
    g.save([cl[0][0] | (1 << 10), cl[0][1] | (1 << 10), cl[1][0] | (1 << 10), cl[1][1] | (1 << 10)],
           dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SUNNY", show_map_name=True, allow_cycling=False,
                allow_escaping=False, requires_flash=False, music="MUS_NONE", ichor_kind="interior"))
    seen = g.check((13, H - 1), [("altar", ARCHON), ("temple door", (door[0], door[1] + 1)),
                                 ("crag", (7, 6)), ("meadow sign", (19, 7)), ("stelai", (7, 17))])
    for x in range(13, 14):
        for y in range(14, H):
            assert not g.solid[y, x], ("the walk to the altar is blocked", x, y)
    return g, seen, [("stair", 13, 21), ("altar", 13, 11), ("temple", 14, 5), ("crag", 6, 6),
                     ("meadow", 23, 8)]
