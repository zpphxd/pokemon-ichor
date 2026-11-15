"""Kits the far lands' sets share, each drawn in the set's own colors:

  cliff_kit()   a rock-face kit for plateaus and crags (the Arimaspian
                heights, Erytheia's red crags, Atlas's ridge): lips, faces,
                feet, sides, backs and inner corners, plus face variants
  rock_px()     the strata texture those faces use
  fence_kit()   a two-rail timber fence: runs, ends, corners and a gate
  adit()        a timber-framed mine head set into a rock face
  boulder()     a lit boulder on the ground
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
from farlands_lib import ground, put, struct


# --------------------------------------------------------------------------
# Rock
# --------------------------------------------------------------------------

def rock_px(X, Y, ramp, shade=0, seed=0, vein=None):
    """A layered rock face, 16 px periodic: strata that wave a little, each lit
    along its top, a joint now and then. ramp: 5 colors dark -> light.
    shade: +1 darker (a face turned from the light). vein: (dark, light)
    gold veins threading across."""
    x, y = X % 16, Y % 16
    band = (y + int(round(1.2 * math.sin(2 * math.pi * (x + seed) / 16)))) % 16
    b = band // 4
    t = band % 4
    k = F.hp(X, Y, 61 + seed)
    i = 3 if t == 0 else (2 if t in (1, 2) else 1)
    if (b * 5 + x // 5 + seed) % 4 == 0 and t == 3:
        i = 0
    if k % 9 == 0:
        i = max(0, i - 1)
    if k % 17 == 0:
        i = min(4, i + 1)
    # vertical joints
    jx = (b * 7 + 3 + seed) % 16
    if x == jx and t != 0:
        i = 0
    if x == (jx + 1) % 16 and t != 0:
        i = min(4, i + 1)
    i = max(0, min(4, i - shade))
    c = ramp[i]
    if vein:
        vy = (6 + int(round(2.5 * math.sin(2 * math.pi * (x + 2 * seed) / 16)))) % 16
        if y == vy or (y == (vy + 1) % 16 and x % 5 == 2):
            c = vein[1] if (x + y) % 3 else vein[0]
        elif y == (vy + 1) % 16 and k % 2:
            c = vein[0]
    return c


CLIFF_NAMES = {
    "back_NW": (0, 0), "back": (1, 0), "back_b": (2, 0), "back_NE": (3, 0),
    "side_W": (0, 1), "side_E": (3, 1), "in_NW": (1, 1), "in_NE": (2, 1),
    "lip_L": (0, 2), "lip": (1, 2), "lip_b": (2, 2), "lip_R": (3, 2),
    "face_L": (0, 3), "face": (1, 3), "face_b": (2, 3), "face_R": (3, 3),
    "foot_L": (0, 4), "foot": (1, 4), "foot_b": (2, 4), "foot_R": (3, 4),
}


def cliff_kit(key, title, section, ramp, edge, grass_shadow, notes, oik=False, seed=0, snow=None,
              extra_faces=(), variants=False):
    """A rock-face kit on borrowed grass. ramp: 5 rock colors dark -> light;
    edge: the outline color where rock meets grass; grass_shadow: the shadow
    cast on the ground at the foot. snow: (shade, lit) to dust the lips and
    backs (a snowline). extra_faces: [(name, painter(L, ox, oy))] face
    variants appended in a sixth row."""
    names = dict(CLIFF_NAMES)
    rows = 5
    if extra_faces:
        for i, (n, _) in enumerate(extra_faces):
            names[n] = (i % 4, 5 + i // 4)
        rows = 5 + (len(extra_faces) + 3) // 4
    walk = ["XXXX", "XXXX", "XXXX", "XXXX", "...."] + ["XXXX"] * (rows - 5)
    s = struct(key, title, 4, rows, section, walk=walk, names=names, notes=notes, oik=oik)
    ground(s, "grass")
    M = s.M

    def rk(X, Y, sh=0):
        return rock_px(X, Y, ramp, sh, seed)

    def wob(t, a=1.0, ph=0.0):
        return a * math.sin(2 * math.pi * (t + ph) / 16) + 0.5 * a * math.sin(4 * math.pi * (t + ph) / 16 + 1.1)

    def lip_cell(ox, oy, end=None, b=0):
        # the plateau's crest: grass above, the rock's brow below, rounding
        # into the face beneath
        for x in range(16):
            top = 9 + int(round(wob(x + 5 * b, 1.0)))
            if end == "L":
                top += max(0, 5 - x)
            if end == "R":
                top += max(0, x - 10)
            for y in range(top, 16):
                if end == "L" and x < 5 - (y - top) // 2 and y - top < 8:
                    continue
                if end == "R" and x > 10 + (y - top) // 2 and y - top < 8:
                    continue
                c = rk(ox + x, oy + y, -1 if y - top < 2 else 0)
                if y == top:
                    c = ramp[4]
                M.px(ox + x, oy + y, c)
            M.px(ox + x, oy + top - 1, edge) if top - 1 >= 0 and M.get(ox + x, oy + top) else None
        if end:
            sub = M.a[oy:oy + 16, ox:ox + 16, 3] > 0
            for y, x in np.argwhere(F.edge_of(sub)):
                if (end == "L" and x < 8) or (end == "R" and x > 7):
                    M.px(ox + x, oy + y, edge)
        if snow:
            for x in range(16):
                for y in range(16):
                    if M.get(ox + x, oy + y) == ramp[4] or (M.get(ox + x, oy + y) and y < 13 and
                                                             F.hp(ox + x, oy + y, 3) % 3 == 0 and
                                                             M.get(ox + x, oy + y - 1) is None):
                        M.px(ox + x, oy + y, snow[1])

    def face_cell(ox, oy, end=None, b=0, vein=None):
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 3 + (1 if y > 11 else 0):
                    continue
                if end == "R" and x > 12 - (1 if y > 11 else 0):
                    continue
                c = rock_px(ox + x + 5 * b, oy + y, ramp, 0, seed, vein)
                if end == "L" and x < 6:
                    c = rock_px(ox + x, oy + y, ramp, -1, seed, vein)
                if end == "R" and x > 9:
                    c = rock_px(ox + x, oy + y, ramp, 1, seed, vein)
                M.px(ox + x, oy + y, c)
        if end:
            for y in range(16):
                xs = [x for x in range(16) if M.get(ox + x, oy + y)]
                if xs:
                    M.px(ox + (xs[0] if end == "L" else xs[-1]), oy + y, edge)

    def foot_cell(ox, oy, end=None, b=0):
        # the face's last rows, then rubble and shadow on the ground
        for x in range(16):
            bot = 5 + int(round(wob(x + 3 * b + 7, 1.2)))
            if end == "L" and x < 3:
                continue
            if end == "R" and x > 12:
                continue
            for y in range(0, bot):
                M.px(ox + x, oy + y, rk(ox + x, oy + y, 1 if y >= bot - 2 else 0))
            M.px(ox + x, oy + bot, edge)
            for y in range(bot + 1, min(16, bot + 3)):
                if (x + y) % 2 == 0 or y == bot + 1:
                    M.px(ox + x, oy + y, grass_shadow)
        # fallen stones
        for (sx, sy) in ((3 + 4 * b, 10), (11, 12), (7, 13)):
            if end == "L" and sx < 5:
                continue
            put(M, ox + sx - 1, oy + sy - 1, [".43.", "4322", ".11."],
                {"4": ramp[4], "3": ramp[3], "2": ramp[2], "1": ramp[0]})
        if end:
            for y in range(0, 8):
                xs = [x for x in range(16) if M.get(ox + x, oy + y)]
                if xs:
                    M.px(ox + (xs[0] if end == "L" else xs[-1]), oy + y, edge)

    def side_cell(ox, oy, side):
        # a plateau edge seen from above: grass, then a strip of rock dropping away
        for y in range(16):
            w = 5 + int(round(wob(y + 2, 1.0)))
            for i in range(w):
                x = i if side == "W" else 15 - i
                c = rk(ox + x, oy + y, 0 if side == "W" else 1)
                if i == w - 1:
                    c = ramp[4] if side == "W" else ramp[3]
                M.px(ox + x, oy + y, c)
            inner = w if side == "W" else 15 - w
            M.px(ox + inner, oy + y, edge)
        if snow:
            for y in range(16):
                for x in range(16):
                    if M.get(ox + x, oy + y) in (ramp[4], ramp[3]) and F.hp(ox + x, oy + y, 5) % 2:
                        M.px(ox + x, oy + y, snow[1])

    def back_cell(ox, oy, end=None, b=0):
        # the plateau's north rim: a thin band of rock at the top of the cell
        for x in range(16):
            hgt = 4 + int(round(wob(x + 6 * b, 0.9)))
            if end == "W":
                hgt = max(hgt, 4 + max(0, 6 - x))
            if end == "E":
                hgt = max(hgt, 4 + max(0, x - 9))
            for y in range(hgt):
                M.px(ox + x, oy + y, rk(ox + x, oy + y, 1 if y < 2 else 0))
            M.px(ox + x, oy + hgt - 1, ramp[4])
            M.px(ox + x, oy + hgt, edge)
        if end == "W":
            for y in range(16):
                w = 5 + int(round(wob(y + 2, 1.0)))
                for i in range(w):
                    if not M.get(ox + i, oy + y):
                        M.px(ox + i, oy + y, rk(ox + i, oy + y))
                M.px(ox + w, oy + y, edge) if not M.get(ox + w, oy + y) else None
        if end == "E":
            for y in range(16):
                w = 5 + int(round(wob(y + 2, 1.0)))
                for i in range(w):
                    if not M.get(ox + 15 - i, oy + y):
                        M.px(ox + 15 - i, oy + y, rk(ox + 15 - i, oy + y, 1))
                M.px(ox + 15 - w, oy + y, edge) if not M.get(ox + 15 - w, oy + y) else None
        if snow:
            for y in range(16):
                for x in range(16):
                    if M.get(ox + x, oy + y) == ramp[4] or (M.get(ox + x, oy + y) and F.hp(ox + x, oy + y, 9) % 4 == 0):
                        M.px(ox + x, oy + y, snow[1] if y < 3 else snow[0])

    def inner_cell(ox, oy, side):
        # an inner corner: the face turns north; only a corner of rock shows
        for y in range(16):
            for x in range(16):
                d = math.hypot((x if side == "W" else 15 - x), y)
                if d < 6 + wob(x + y, 0.8):
                    M.px(ox + x, oy + y, rk(ox + x, oy + y))
        sub = M.a[oy:oy + 16, ox:ox + 16, 3] > 0
        for y, x in np.argwhere(F.edge_of(sub)):
            if (side == "W" and (x > 0 and y > 0)) or (side == "E" and (x < 15 and y > 0)):
                M.px(ox + x, oy + y, edge)

    n = names
    back_cell(*[v * 16 for v in n["back_NW"]], end="W")
    back_cell(*[v * 16 for v in n["back"]])
    back_cell(*[v * 16 for v in n["back_b"]], b=1 if variants else 0)
    back_cell(*[v * 16 for v in n["back_NE"]], end="E")
    side_cell(*[v * 16 for v in n["side_W"]], "W")
    side_cell(*[v * 16 for v in n["side_E"]], "E")
    inner_cell(*[v * 16 for v in n["in_NW"]], "W")
    inner_cell(*[v * 16 for v in n["in_NE"]], "E")
    lip_cell(*[v * 16 for v in n["lip_L"]], end="L")
    lip_cell(*[v * 16 for v in n["lip"]])
    lip_cell(*[v * 16 for v in n["lip_b"]], b=1 if variants else 0)
    lip_cell(*[v * 16 for v in n["lip_R"]], end="R")
    face_cell(*[v * 16 for v in n["face_L"]], end="L")
    face_cell(*[v * 16 for v in n["face"]])
    face_cell(*[v * 16 for v in n["face_b"]], b=1)
    face_cell(*[v * 16 for v in n["face_R"]], end="R")
    foot_cell(*[v * 16 for v in n["foot_L"]], end="L")
    foot_cell(*[v * 16 for v in n["foot"]])
    foot_cell(*[v * 16 for v in n["foot_b"]], b=1 if variants else 0)
    foot_cell(*[v * 16 for v in n["foot_R"]], end="R")
    s.face_cell = face_cell
    if not variants:
        for k in ("back_b", "lip_b", "foot_b"):
            del s.names[k]
    for name, painter in extra_faces:
        cx, cy = names[name]
        face_cell(cx * 16, cy * 16)
        painter(s, M, cx * 16, cy * 16)
    return s


CLIFF_NOTES = (
    "How to build a crag: a plateau of high ground, its cells plain aethos grass. Its south edge is "
    "three rows: `lip` (the crest, grass above the rock's brow), `face` (bare rock; stack two for a "
    "taller cliff) and `foot` (the face's base, rubble and shadow on the ground, walkable). `_L` and "
    "`_R` end a run where the plateau's west and east edges turn north; `face_b` breaks up a long run. "
    "The west and east edges are `side_W` and `side_E` (a strip of rock falling away), the north edge "
    "`back` (a thin rim) with its corners `back_NW` and `back_NE`; `in_NW` and `in_NE` are inner "
    "corners where a south face meets a side running north. Everything but `foot` is impassable, "
    "on borrowed aethos grass. Use aethos's ledges (`087` and kin) for one-way drops.")


# --------------------------------------------------------------------------
# Timber
# --------------------------------------------------------------------------

def plank_px(X, Y, ramp, vertical=False, seed=0):
    """Weathered planks: grain lines, a darker seam between boards."""
    a, b = (Y, X) if vertical else (X, Y)
    board = b % 16 // 4
    t = b % 4
    k = F.hp(X, Y, 71 + seed)
    i = 2 if t in (1, 2) else (3 if t == 0 else 0)
    if (a + board * 5) % 7 == 0 and t != 3:
        i = 1
    if k % 11 == 0:
        i = max(0, i - 1)
    return ramp[i]


FENCE_NAMES = {"H_L": (0, 0), "H": (1, 0), "H_R": (2, 0), "gate": (3, 0),
               "V_T": (0, 1), "V": (1, 1), "V_B": (2, 1), "gate_V": (3, 1),
               "NW": (0, 2), "NE": (1, 2), "SW": (2, 2), "SE": (3, 2)}


def fence_kit(key, title, section, wood, shadow, notes, oik=False):
    """A two-rail timber fence on borrowed grass. wood: 4 colors dark -> light."""
    s = struct(key, title, 4, 3, section, walk=["XXX.", "XXX.", "XXXX"], names=dict(FENCE_NAMES),
               notes=notes, oik=oik)
    ground(s, "grass")
    M = s.M
    d, m, l, hi = wood

    def post(X, Y, tall=9):
        for y in range(tall):
            M.px(X, Y + y, l if y == 0 else m)
            M.px(X + 1, Y + y, d)
        M.px(X, Y + tall, shadow)
        M.px(X + 1, Y + tall, shadow)
        M.px(X + 2, Y + tall, shadow)

    def hrail(X0, X1, Y):
        for x in range(X0, X1 + 1):
            M.px(x, Y, hi if x % 5 else l)
            M.px(x, Y + 1, d)
            if M.get(x, Y + 2) is None:
                M.px(x, Y + 3, shadow) if (x % 2) else None

    def hfence(ox, oy, left=True, right=True, gap=False):
        top = oy + 5
        if not gap:
            hrail(ox + (5 if not left else 0), ox + (10 if not right else 15), top + 1)
            hrail(ox + (5 if not left else 0), ox + (10 if not right else 15), top + 5)
        posts = [ox + 2, ox + 10] if not gap else [ox + 1, ox + 13]
        if not left:
            posts = [p for p in posts if p >= ox + 5]
        if not right:
            posts = [p for p in posts if p <= ox + 10]
        for p in posts:
            post(p, top - 1)

    def vfence(ox, oy, top=True, bottom=True, gap=False):
        x = ox + 7
        y0 = oy + (0 if top else 6)
        y1 = oy + (15 if bottom else 9)
        if not gap:
            for y in range(y0, y1 + 1):
                M.px(x - 1, y, l)
                M.px(x, y, m)
                M.px(x + 1, y, d)
                M.px(x + 3, y, d)
                M.px(x + 4, y, m)
                M.px(x + 5, y, d)
        for py in ([oy + 1, oy + 9] if not gap else [oy + 1, oy + 11]):
            if y0 - 1 <= py <= y1:
                post(x + 1, py - 1, 6)

    hfence(0, 0, left=False)
    hfence(16, 0)
    hfence(32, 0, right=False)
    hfence(48, 0, gap=True)
    vfence(0, 16, top=False)
    vfence(16, 16)
    vfence(32, 16, bottom=False)
    vfence(48, 16, gap=True)
    # corners: a horizontal run meets a vertical one
    hfence(0, 32, left=False)
    vfence(0, 32, top=False)
    hfence(16, 32, right=False)
    vfence(16, 32, top=False)
    hfence(32, 32, left=False)
    vfence(32, 32, bottom=False)
    hfence(48, 32, right=False)
    vfence(48, 32, bottom=False)
    return s


FENCE_NOTES = (
    "A two-rail timber fence on borrowed grass, impassable. `H_L` `H` `H_R`: a west-east run and "
    "its ends; `V_T` `V` `V_B`: a north-south run; `NW` `NE` `SW` `SE`: the corners of a paddock "
    "(`NW` is its top-left); `gate` and `gate_V`: an open gateway in a run (walkable).")


def adit(M, ox, oy, wood, dark, rock_edge, spoil=None):
    """A mine head in a rock face: a timber door frame round a dark mouth.
    wood: (dark, mid, light); dark: (inside, deeper)."""
    d, m, l = wood
    # the mouth
    for y in range(3, 16):
        for x in range(4, 12):
            M.px(ox + x, oy + y, dark[1] if y > 6 and 5 <= x <= 10 else dark[0])
    # props and lintel
    for y in range(2, 16):
        for (x, c) in ((3, l), (4, m), (11, m), (12, d)):
            M.px(ox + x, oy + y, c)
    for x in range(2, 14):
        M.px(ox + x, oy + 2, l)
        M.px(ox + x, oy + 3, m if x % 4 else d)
        M.px(ox + x, oy + 1, rock_edge)
    # a rail of planks going in
    for y in range(9, 16, 3):
        for x in range(6, 10):
            M.px(ox + x, oy + y, m)
    if spoil:
        for (x, y) in ((1, 14), (2, 15), (14, 13), (13, 15), (15, 15)):
            M.px(ox + x, oy + y, spoil)


def cave_mouth(M, ox, oy, dark, rim):
    """A natural cave mouth in a rock face: a ragged dark arch."""
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 7.5) / 6.0, (y - 15) / 12.5)
            if d < 1 + 0.06 * math.sin(x * 2.1 + y):
                M.px(ox + x, oy + y, dark[1] if d < 0.7 else dark[0])
            elif d < 1.15:
                M.px(ox + x, oy + y, rim)


def boulder(L, ox, oy, cx, cy, rx, ry, ramp, edge, shadow, seed=0):
    """A lit boulder: lit top-left, dark bottom-right, outlined, a shadow."""
    m = F.blob(cx, cy, rx, ry, 16, 16, wobble=0.08, k=5, seed=seed)
    for y in range(16):
        for x in range(16):
            if not m[y, x] and y > 0 and m[y - 1, x] and shadow:
                L.px(ox + x, oy + y, shadow)
                if y + 1 < 16:
                    L.px(ox + x + 1, oy + y + 1, shadow) if not m[min(15, y + 1), min(15, x + 1)] else None
    for y, x in np.argwhere(m):
        u = (x - cx) / rx + (y - cy) / ry
        k = F.h(x, y, seed)
        i = 3 if u < -0.6 else (2 if u < 0.2 else (1 if u < 0.9 else 0))
        if k % 7 == 0:
            i = max(0, i - 1)
        L.px(ox + x, oy + y, ramp[i + 1] if i + 1 < len(ramp) else ramp[-1])
    for y, x in np.argwhere(F.edge_of(m)):
        L.px(ox + x, oy + y, edge)
