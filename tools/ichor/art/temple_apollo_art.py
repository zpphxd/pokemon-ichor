"""gTileset_TempleApollo: the Temple of Apollo's rite (the Pythian Light) and the
Omphalos stair, on the oikos primary.

Inside, the temple is dim: dark polished marble, pale walls under a dark
cornice, bronze grilles between the chambers, gilded tripods, lyres, the bronze
serpent and laurels; the god's light is a gold stripe on the floor (silver by
night), passed mirror to mirror. The adyton is bare rock over the chasm, with
steaming vents, a bronze brazier and the tripod. The stair below the Omphalos
is pale rock going down into the dark.

Palette plan (secondary slots 6-12):
  marble  the floor, the walls and the cornice
  sun     the floor with the gold beam
  moon    the floor with the silver beam
  bronze  grilles, gates, tripods, the serpent, discs, the brazier, fire
  rock    the adyton's floor, the vents, the chasm, the stair's rock
  laurel  potted laurels and garlands, terracotta
  lyre    the lyres and kitharas on their stands, ivory and gut
"""
from __future__ import annotations

import math

import numpy as np

import emporion_lib as E
import kalliste_lib as K
from emporion_lib import Struct, finish
from kalliste_lib import Layer

NAME = "temple_apollo"

NEW = {
    "fd0": (24, 24, 40), "fd1": (48, 48, 64), "fd2": (72, 72, 88), "fd3": (104, 104, 120),
    "gl0": (176, 128, 32), "gl1": (232, 184, 56), "gl2": (248, 232, 136), "gl3": (248, 248, 208),
    "sv0": (112, 128, 160), "sv1": (168, 184, 208), "sv2": (216, 224, 240),
    "bz0": (72, 40, 16), "bz1": (128, 80, 32), "bz2": (184, 128, 56),
    "rk0": (40, 32, 32), "rk1": (80, 64, 56), "rk2": (120, 104, 88), "rk3": (160, 144, 120),
    "rk4": (200, 184, 160), "stm": (224, 224, 216),
    "iv": (232, 216, 184),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    "marble": ["ink", "fd0", "fd1", "fd2", "fd3", "w0", "m1", "m2", "m3", "m4", "m5", "rd", "b0",
               "g0", "g1"],
    "sun": ["ink", "fd0", "fd1", "fd2", "fd3", "gl0", "gl1", "gl2", "gl3", "w0"],
    "moon": ["ink", "fd0", "fd1", "fd2", "fd3", "sv0", "sv1", "sv2", "w0"],
    "bronze": ["ink", "fd0", "fd1", "fd2", "fd3", "bz0", "bz1", "bz2", "g0", "g1", "gl2", "fl",
               "fc", "w0", "rd"],
    "rock": ["ink", "rk0", "rk1", "rk2", "rk3", "rk4", "stm", "w0", "m3", "fd1", "fd2", "fd0"],
    "laurel": ["ink", "c1", "c2", "c3", "ov3", "tc0", "tc1", "tc2", "fd0", "fd1", "fd2", "fd3",
               "rd"],
    "lyre": ["ink", "iv", "bz0", "bz1", "bz2", "g1", "fd0", "fd1", "fd2", "fd3", "w0", "wd0",
             "wd1", "wd2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}


def validate(structs):
    saved = E.GROUP_RGB
    E.GROUP_RGB = GROUP_RGB
    try:
        return E.validate(structs)
    finally:
        E.GROUP_RGB = saved


def S(key, title, w, h, walk, names=None):
    s = Struct(key, title, w, h, walk=walk, ground="none")
    s.names = names or {}
    return s


def floor(L, x0, y0, w=16, h=16, ox=0, oy=0):
    """Dark polished marble: big square slabs, a faint lit edge top-left, the
    joints darker, a soft gleam on each slab."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 16, (y - oy) % 16
            if X == 15 or Y == 15:
                c = "fd0"
            elif X == 0 or Y == 0:
                c = "fd3"
            elif (X + Y) in (5, 6) and X < 7:
                c = "fd3"
            else:
                c = "fd2" if (X * 3 + Y * 5) % 17 else "fd1"
            L.px(x, y, c)


def floor_kit():
    s = S("floor", "Dark marble floor, and the light patch under the smoke-hole", 3, 1, walk=["..."],
          names={"floor": (0, 0), "floor2": (1, 0), "light": (2, 0)})
    floor(s.B, 0, 0, 48, 16)
    for (x, y) in ((20, 4), (21, 4), (26, 10), (27, 9)):
        s.B.px(x, y, "fd1")
    # a pool of dim light on the floor where the roof lets the sun in
    for y in range(16):
        for x in range(32, 48):
            d = ((x - 40) / 7.5) ** 2 + ((y - 8) / 7.5) ** 2
            if d < 1 and s.B.get(x, y) in ("fd2", "fd1"):
                s.B.px(x, y, "fd3")
    return finish(s)


def beam_kit(key, title, hi, mid, lo):
    """The six beam pieces, in the order the trace expects: east-west,
    north-south, and the corners joining the tile's north and east, north and
    west, south and east, south and west sides."""
    s = S(key, title, 6, 1, walk=["......"],
          names={"EW": (0, 0), "NS": (1, 0), "NE": (2, 0), "NW": (3, 0), "SE": (4, 0), "SW": (5, 0)})
    floor(s.B, 0, 0, 96, 16)
    arms = {0: "EW", 1: "NS", 2: "NE", 3: "NW", 4: "SE", 5: "SW"}

    def stripe(ox, n, e, s_, w):
        for y in range(16):
            for x in range(16):
                dx, dy = abs(x - 7.5), abs(y - 7.5)
                inn = False
                if (n and y <= 8 and dx < 3) or (s_ and y >= 7 and dx < 3):
                    inn = True
                if (w and x <= 8 and dy < 3) or (e and x >= 7 and dy < 3):
                    inn = True
                halo = False
                if (n and y <= 8 and dx < 4) or (s_ and y >= 7 and dx < 4):
                    halo = True
                if (w and x <= 8 and dy < 4) or (e and x >= 7 and dy < 4):
                    halo = True
                if inn:
                    core = (n or s_) and dx < 1.5 or (e or w) and dy < 1.5
                    s.B.px(ox + x, y, hi if core else mid)
                elif halo:
                    s.B.px(ox + x, y, lo)
    for i, k in arms.items():
        stripe(i * 16, "N" in k, "E" in k or k == "EW", "S" in k or k == "NS", "W" in k or k == "EW")
    return finish(s)


def wall_kit():
    """The cella's walls: a dark cornice row over a pale wall row with Doric
    pilasters; the wall with a lyre hung on it, with the gold disc (dark and
    blazing), with the high window letting the shaft of sun in, and with KNOW
    THYSELF cut in it. All solid."""
    names = {"top": (0, 0), "top2": (1, 0), "wall": (0, 1), "pilaster": (1, 1), "disc": (2, 1),
             "disc_lit": (3, 1), "window": (4, 1), "inscription": (5, 1), "lyre": (2, 0),
             "top_disc": (3, 0), "side_W": (4, 0), "side_E": (5, 0)}
    s = S("wall", "Walls: cornice, face, pilaster, disc dark and lit, window, inscription, lyre", 6, 2,
          walk=["XXXXXX", "XXXXXX"], names=names)
    B = s.B
    for x in range(96):
        for y in range(16):
            B.px(x, y, "fd0" if y < 12 else "fd1")
        B.px(x, 12, "m4")
        B.px(x, 13, "m3")
        B.px(x, 14, "m2")
        B.px(x, 15, "rd" if x % 4 else "b0")
    for x in range(96):
        for y in range(16, 32):
            c = "m1" if (x % 16) not in (0, 15) else "m3"
            if y >= 28:
                c = "rd" if y < 30 else "m4"
            B.px(x, y, c)
    # the pilaster
    E.shaft(B, 20, 16, 8, 12, ramp=("m4", "m3", "m2", "m1", "w0"))
    # the gold sun-discs, dark and blazing
    for ox, lit in ((32, False), (48, True)):
        B.ellipse(ox + 3, 18, ox + 12, 27, "ink")
        B.ellipse(ox + 4, 19, ox + 11, 26, "g1" if lit else "m4")
        B.ellipse(ox + 5, 20, ox + 9, 24, "w0" if lit else "m3")
        if lit:
            for a in range(0, 360, 45):
                x = ox + 8 + int(6.5 * math.cos(math.radians(a)))
                y = 22 + int(6.5 * math.sin(math.radians(a)))
                B.px(x, y, "g0")
    # the high window: a slot of sky and a shaft of light falling from it
    B.rect(68, 17, 8, 8, "ink")
    B.rect(69, 18, 6, 6, "w0")
    for y in range(25, 32):
        for x in range(68 + (y - 25) // 2, 76 + (y - 25) // 2):
            if x < 80:
                B.px(x, y, "w0" if (x + y) % 3 else "m1")
    # KNOW THYSELF: a line of cut letters
    for x in range(82, 94, 2):
        B.px(x, 21, "ink")
        B.px(x, 22, "m4")
    for x in range(84, 92, 2):
        B.px(x, 24, "ink")
    # a lyre hung on the cornice row (bronze group colors only)
    L = Layer(16, 16)
    L.vline(36, 2, 11, "g1") if False else None
    for y in range(2, 11):
        B.px(34, y, "g1")
        B.px(41, y, "g1")
    B.hline(34, 41, 2, "g0")
    B.rect(35, 9, 6, 2, "g0")
    for x in (36, 38, 40):
        B.vline(x, 3, 8, "w0")
    # top_disc (the cornice above a disc): a gold rim line
    B.hline(51, 60, 11, "g0")
    # the side walls' columns
    for ox, dark in ((64, False), (80, True)):
        for y in range(16):
            for x in range(ox, ox + 16):
                B.px(x, y, "fd1" if (x - ox) % 5 else "fd0")
    return finish(s)


def screens():
    """The bronze-grilled screens between the chambers (solid), a gate shut
    (solid) and open (walkable), and the gold disc set in a screen (solid)."""
    s = S("screen", "Bronze screens: grille, gate shut, gate open, disc in a screen", 5, 1,
          walk=["XX.XX"], names={"grille": (0, 0), "shut": (1, 0), "open": (2, 0),
                                 "disc": (3, 0), "disc_lit": (4, 0)})
    B = s.B
    floor(B, 0, 0, 80, 16)
    for ox in (0, 16, 48, 64):
        B.rect(ox, 10, 16, 6, "bz0")
        B.hline(ox, ox + 15, 10, "bz2")
        for x in range(ox, ox + 16, 4):
            B.vline(x + 1, 0, 9, "bz1")
            B.vline(x + 2, 0, 9, "bz2")
        B.hline(ox, ox + 15, 0, "bz2")
        B.hline(ox, ox + 15, 4, "bz1")
    # the gate shut: heavier bars and a bolt
    B.rect(16, 0, 16, 16, "bz0")
    for x in range(17, 32, 3):
        B.vline(x, 0, 15, "bz2")
    B.rect(22, 6, 4, 3, "g1")
    # the gate open: the posts at either side, the floor between
    for x in (32, 46):
        B.vline(x, 0, 15, "bz1")
        B.vline(x + 1, 0, 15, "bz2")
    # discs set in the screen
    for ox, lit in ((48, False), (64, True)):
        B.ellipse(ox + 3, 1, ox + 12, 10, "ink")
        B.ellipse(ox + 4, 2, ox + 11, 9, "g1" if lit else "bz1")
        B.ellipse(ox + 6, 3, ox + 9, 6, "gl2" if lit else "bz2")
    return finish(s)


def props():
    """Gilded tripods, the bronze serpent coiled on its pillar, potted laurels,
    a lyre and a kithara on stands, the steps down to the adyton."""
    s = S("props", "Tripods, the serpent pillar, laurels, lyres, steps", 8, 2,
          walk=["TTTXT.XX", "XXXXX.XX"],
          names={"tripod_top": (0, 0), "tripod": (0, 1), "serpent_TL": (1, 0), "serpent_TR": (2, 0),
                 "serpent_BL": (1, 1), "serpent_BR": (2, 1), "laurel_top": (4, 0), "laurel": (4, 1),
                 "lyre": (3, 1), "kithara": (3, 0), "steps": (5, 0), "steps2": (5, 1),
                 "brazier": (6, 0), "brazier_lit": (7, 0), "vent": (6, 1), "chasm": (7, 1)})
    B, T = s.B, s.T
    floor(B, 0, 0, 128, 32)
    # a gilded tripod: three legs, a bowl, ring handles
    for (x0, y0) in ((0, 0),):
        for i, lx in enumerate((3, 8, 12)):
            B.line(x0 + 7, y0 + 18, x0 + lx, y0 + 30, "g0")
            B.line(x0 + 8, y0 + 18, x0 + lx + 1, y0 + 30, "g1")
        T.ellipse(x0 + 2, y0 + 8, x0 + 13, y0 + 17, "ink")
        T.ellipse(x0 + 3, y0 + 9, x0 + 12, y0 + 16, "g1")
        T.ellipse(x0 + 4, y0 + 9, x0 + 11, y0 + 12, "g0")
        T.ellipse(x0 + 4, y0 + 3, x0 + 7, y0 + 8, "g1")
        T.ellipse(x0 + 8, y0 + 3, x0 + 11, y0 + 8, "g1")
    # the bronze serpent round its pillar
    B.rect(22, 0, 12, 32, "fd3")
    B.vline(22, 0, 31, "ink")
    B.vline(33, 0, 31, "ink")
    for y in range(2, 30):
        ph = math.sin(y * 0.55)
        x = 28 + int(ph * 9)
        for k in range(-2, 3):
            B.px(x + k, y, "bz1" if k < 0 else "bz2" if k == 0 else "bz0")
    B.ellipse(16, 0, 26, 7, "bz2")
    B.px(19, 3, "ink")
    B.px(18, 5, "rd")
    T.a[:16, 16:48] = B.a[:16, 16:48]
    B.a[:16, 16:48] = 0
    floor(B, 16, 0, 32, 16, ox=16)
    # a potted laurel
    E.amphora(B, 66, 22, body="tc1", lit="tc2", shade="tc0", dark="tc0") if False else None
    B.ellipse(67, 22, 76, 31, "tc1")
    B.ellipse(68, 22, 74, 26, "tc2")
    B.hline(67, 76, 31, "ink")
    for (cx, cy, r) in ((72, 8, 6), (69, 14, 5), (75, 15, 5), (72, 20, 4)):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    c = "c3" if (x - cx) + (y - cy) < -r // 2 else "c2" if (x - cx) + (y - cy) < r // 2 else "c1"
                    (T if y < 16 else B).px(x, y, c)
    # a lyre and a kithara on stands
    for (ox, oy, big) in ((48, 16, False), (48, 0, True)):
        top = oy + (1 if big else 3)
        B.line(ox + 4, oy + 14, ox + 3, top, "wd1")
        B.line(ox + 11, oy + 14, ox + 12, top, "wd1")
        B.hline(ox + 3, ox + 12, top, "bz2")
        B.rect(ox + 4, oy + 11, 8, 3, "iv" if big else "bz1")
        for x in range(ox + 5, ox + 12, 2):
            B.vline(x, top + 1, oy + 10, "w0")
        B.hline(ox + 2, ox + 13, oy + 15, "fd0")
    # the steps down to the adyton
    for y in range(32):
        for x in range(80, 96):
            t = y % 6
            B.px(x, y, "fd3" if t == 0 else "fd2" if t < 3 else "fd1" if t < 5 else "fd0")
    # the brazier, cold and lit
    for ox in (96, 112):
        B.line(ox + 4, 14, ox + 6, 8, "bz1")
        B.line(ox + 11, 14, ox + 9, 8, "bz1")
        B.ellipse(ox + 2, 4, ox + 13, 10, "ink")
        B.ellipse(ox + 3, 5, ox + 12, 9, "bz2")
        B.ellipse(ox + 4, 5, ox + 11, 7, "bz0")
    T.a[0:8, 112:128] = 0
    E.flame(T, 115, -1, big=True)
    # a vent in the adyton's rock (walkable), and the chasm (solid)
    for y in range(16, 32):
        for x in range(96, 128):
            B.px(x, y, "rk2" if (x * 7 + y * 3) % 11 else "rk1")
    B.ellipse(100, 22, 107, 27, "rk0")
    for (x, y) in ((102, 20), (103, 18), (104, 21), (101, 17), (104, 16)):
        B.px(x, y, "stm")
    B.rect(112, 16, 16, 16, "rk0")
    for y in range(16, 32):
        B.px(112 + (y % 3), y, "ink")
        B.px(126 - (y % 4), y, "ink")
    return finish(s)


def adyton():
    """The adyton's rock floor (two looks), and the Pythia's tripod over the
    crack, cold and lit: 3 x 2, solid."""
    s = S("adyton", "The adyton: rock floor, and the tripod over the chasm (cold, lit)", 8, 2,
          walk=["..XXXXXX", "..XXXXXX"],
          names={"rock": (0, 0), "rock2": (1, 0), "rock3": (0, 1), "rock4": (1, 1),
                 "tripod_TL": (2, 0), "tripod_lit_TL": (5, 0)})
    B, T = s.B, s.T
    for y in range(32):
        for x in range(32):
            c = "rk2"
            if (x * 7 + y * 3) % 11 == 0:
                c = "rk1"
            elif (x * 5 + y * 9) % 13 == 0:
                c = "rk3"
            B.px(x, y, c)
    for ox, lit in ((32, False), (80, True)):
        for y in range(32):
            for x in range(ox, ox + 48):
                B.px(x, y, "rk2" if (x * 7 + y * 3) % 11 else "rk1")
        # the crack in the rock, black, vapour rising
        B.poly([(ox + 10, 31), (ox + 18, 18), (ox + 26, 20), (ox + 30, 12), (ox + 38, 31)], "rk0")
        B.line(ox + 18, 18, ox + 26, 31, "ink")
        for (x, y) in ((ox + 22, 10), (ox + 24, 7), (ox + 21, 5), (ox + 25, 3)):
            B.px(x, y, "stm" if not lit else "w0")
        # the tripod's legs over the crack
        for lx in (ox + 13, ox + 24, ox + 34):
            B.line(ox + 24, 10, lx, 30, "rk4")
        B.ellipse(ox + 15, 4, ox + 33, 13, "ink")
        B.ellipse(ox + 16, 5, ox + 32, 12, "rk4")
        B.ellipse(ox + 17, 5, ox + 31, 8, "rk3")
    tmp = Layer(128, 32)
    E.flame(tmp, 80 + 18, 0, big=True)
    E.flame(tmp, 80 + 25, 1, big=True)
    T.a[:16, 96:112] = tmp.a[:16, 96:112]
    s.names.update({"tripod_TC": (3, 0), "tripod_TR": (4, 0), "tripod_BL": (2, 1),
                    "tripod_BC": (3, 1), "tripod_BR": (4, 1), "tripod_lit_TC": (6, 0),
                    "tripod_lit_TR": (7, 0), "tripod_lit_BL": (5, 1), "tripod_lit_BC": (6, 1),
                    "tripod_lit_BR": (7, 1)})
    return finish(s)


def stair():
    """The Omphalos stair: pale steps cut in old rock, the rock walls, a burnt
    torch, a charred knot, the carving of three women and a loom."""
    s = S("stair", "The Omphalos stair: steps, rock, the torch, the knot, the carving, the way up and down", 8, 1,
          walk=["..X..X.."], names={"steps": (0, 0), "landing": (1, 0), "rock": (2, 0),
                                    "torch": (3, 0), "knot": (4, 0), "carving": (5, 0),
                                    "way_up": (6, 0), "way_down": (7, 0)})
    s.behaviors[(6, 0)] = "MB_NORTH_ARROW_WARP"
    s.behaviors[(7, 0)] = "MB_SOUTH_ARROW_WARP"
    B = s.B
    for y in range(16):
        for x in range(16):
            t = y % 4
            B.px(96 + x, y, "w0" if y < 3 else "rk4" if t == 0 else "rk3")
            B.px(112 + x, y, "rk0" if y > 9 else ("rk2" if t == 0 else "rk1"))
    for y in range(16):
        for x in range(16):
            t = y % 4
            B.px(x, y, "rk4" if t == 0 else "rk3" if t < 3 else "rk1")
            B.px(16 + x, y, "rk3" if (x * 3 + y * 7) % 9 else "rk2")
            B.px(32 + x, y, "rk1" if (x * 7 + y * 3) % 5 else "rk0")
            B.px(48 + x, y, "rk3" if (x * 3 + y * 7) % 9 else "rk2")
            B.px(64 + x, y, "rk3" if (x * 3 + y * 7) % 9 else "rk2")
            B.px(80 + x, y, "rk1" if (x * 7 + y * 3) % 5 else "rk0")
    B.line(50, 12, 60, 6, "rk0")
    B.line(50, 13, 60, 7, "ink")
    B.rect(59, 5, 3, 3, "ink")
    B.ellipse(68, 6, 75, 11, "rk0")
    B.px(71, 8, "ink")
    # three women and a loom, scratched into the rock
    for i, fx in enumerate((82, 86, 90)):
        B.ellipse(fx, 2, fx + 2, 4, "rk4")
        B.vline(fx + 1, 5, 12, "rk4")
        B.line(fx + 1, 7, fx + 3, 9, "rk4")
    B.hline(81, 94, 13, "rk4")
    for x in range(81, 95, 2):
        B.px(x, 14, "rk3")
    return finish(s)


def build():
    parts = [("floor", [floor_kit(), beam_kit("beam", "The sun's beam on the floor", "gl3", "gl1", "gl0"),
                        beam_kit("moonbeam", "The moon's beam on the floor", "sv2", "sv1", "sv0")]),
             ("walls", [wall_kit(), screens()]),
             ("things", [props(), adyton(), stair()])]
    sections, start = [], 0
    for name, ss in parts:
        for s in ss:
            s.section = name
        end = K.pack([(start, ss)])
        sections.append((start, ss))
        start = end + 1
    return sections


def write_catalog(used, structs):
    import delphoi_art as D
    D.write_catalog(used, structs, name=NAME, maps="the Temple of Apollo and the Omphalos stair (on oikos)")
