"""Arkadia's town: rock and its faces, terrace walls, the house kit (timber and
stone under shingles), the Asclepeion against its outcrop, the Agora's stall round
the town's biggest cypress, Hippothoos's hut and kiln, Krotos's byre and fence, the
old racecourse, Iamos's old wall, Pan's grotto, the temple hill's stair, the Temple
of Artemis and its precinct gate, and the Cypress Wood's gate.

Each 8x8 tile of each layer draws from one of arkadia_lib.TOWN_GROUPS. Where a
piece has two materials in one cell, they sit on different layers.
"""
from __future__ import annotations

import numpy as np

import arkadia_lib as L
import kithairon_ground as KG

SEC = "town"
FACE = KG.FACE


def full(key, title, w, h, walk, notes, names=None, section=SEC):
    """A structure that draws its own ground everywhere."""
    return L.struct(key, title, w, h, section, walk=walk, notes=notes, names=names)


def grass_fill(layer, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            layer.px(x, y, L.grass_px(x, y))


def rock_top_fill(layer, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            layer.px(x, y, KG.rock_top(x, y))


# --------------------------------------------------------------------------
# Rock: Kithairon's crag painter (the climb's rock, so Route 12 and the town
# match), its tall faces, the grotto, the spring, the cave behind the falls
# --------------------------------------------------------------------------

def rock(keys):
    return L.K.shape_set("rock", "Rock with a south face", SEC, keys,
                         lambda s, ox, oy, k: KG.paint_crag_cell(s.B, ox, oy, k, KG.grass_floor),
                         "X", "The grey rock of the Arkadian hills seen from above, its south "
                              "face showing, on aethos grass: the Asclepeion's outcrop and the "
                              "temple hill. Where `face` cells continue below, the rock above "
                              "them is drawn as region (no face). Impassable. Names are blob keys.")


def face_px(x, depth, lip=False, foot=False, total=16):
    """A tall rock face: rough vertical columns, strata every 6 px."""
    xx = x % 16
    if lip and depth < 2:
        return "rk5" if (xx % 4 and depth == 0) else "rk4"
    if foot and depth >= total - 2:
        return "rk0"
    cols = [1, 6, 10, 14]
    sway = (depth // 5) % 2
    edge = [(c + sway * (1 if j % 2 else -1)) % 16 for j, c in enumerate(cols)]
    if xx in edge:
        return "rk1" if not (foot and depth > total - 6) else "rk0"
    if (xx - 1) % 16 in edge:
        return "rk3"
    if depth % 6 == 3 and (xx * 3 + depth) % 5 < 3:
        return "rk1"
    if foot and depth > total - 5:
        return "rk1" if (xx + depth) % 3 == 0 else "rk2"
    return "rk2" if (xx + depth * 3) % 7 else "rk3"


def face_cell(Lr, ox, oy, kind, side):
    """kind: top (the lip), mid, foot; side: '', 'W', 'E' (the face's end, grass beyond)."""
    for y in range(16):
        for x in range(16):
            c = face_px(x, y, lip=kind == "top", foot=kind == "foot")
            Lr.px(ox + x, oy + y, c)
    if side:
        # the face's end: a ragged edge, grass beyond it, a shadow on the grass
        for y in range(16):
            w = 3 + (1 if (y // 3) % 2 else 0) + (1 if kind == "foot" and y > 10 else 0)
            for i in range(w):
                x = i if side == "W" else 15 - i
                Lr.px(ox + x, oy + y, L.grass_px(x, y))
            ex = w if side == "W" else 15 - w
            Lr.px(ox + ex, oy + y, "rk0" if side == "E" else "rk1")
            sx = w - 1 if side == "W" else 16 - w
            if side == "E":
                c = Lr.get(ox + sx, oy + y)
                Lr.px(ox + sx, oy + y, {"g3": "g1", "g2": "g1", "g1": "gd"}.get(c, c))


def faces():
    names = {}
    order = []
    for kind in ("top", "mid", "foot"):
        for side in ("", "W", "E"):
            names[f"{kind}{side}"] = (len(order) % 3, len(order) // 3)
            order.append((kind, side))
    s = full("face", "Tall rock faces", 3, 3, ["XXX"] * 3,
             "A rock face more than one row tall, below `rock`: `top` (the lip), `mid`, `foot` "
             "(the dark foot); `W` and `E` are the face's ends with grass beside them. The "
             "waterfall cliff is six rows of it, the temple hill's front two.", names=names)
    for (kind, side), (cx, cy) in zip(order, [names[f"{k}{sd}"] for k, sd in order]):
        face_cell(s.B, cx * 16, cy * 16, kind, side)
    return s


def grotto():
    """Pan's grotto: a shallow cave mouth in the rock face, a syrinx carved over it."""
    s = full("grotto", "Pan's grotto", 2, 1, ["XX"],
             "A shallow cave mouth in the outcrop's south face, a syrinx carved over it: lay it "
             "where the outcrop's face row is. Too shallow to enter: a sign event in front.",
             names={"L": (0, 0), "R": (1, 0)})
    B = s.B
    # the face, as the crag painter draws a south edge: 2 px of rock top, then face
    for y in range(16):
        for x in range(32):
            if y < 2:
                B.px(x, y, "rk5" if x % 4 else "rk4")
            else:
                B.px(x, y, KG.rock_face(x, y, y - 2) if y - 2 < FACE else "rk0")
    # the mouth: a dark arch, lit on its west lip
    for y in range(6, 16):
        r = 8 if y > 9 else [3, 5, 6, 7][y - 6]
        for x in range(16 - r, 16 + r):
            B.px(x, y, "cv")
        B.px(16 - r - 1, y, "rk4")
        B.px(16 + r, y, "rk0")
    # moss on the lip, and a fern in the mouth
    for x in (9, 10, 21, 22, 23):
        B.px(x, 5, "ar0")
    # the syrinx: seven reeds, carved, lengths falling to the right
    for i in range(7):
        x = 10 + i * 2
        h = 5 - i // 2
        for y in range(1, 1 + h):
            B.px(x, y, "rk1")
        B.px(x, 1 + h, "rk0")
    B.hline(10, 22, 2, "rk1")
    return s


def spout():
    """The Asclepeion's spring: it rises from the outcrop and spills into a basin."""
    s = full("spring", "The spring and its basin", 1, 2, ["X", "X"],
             "`spout`: the outcrop's face with the spring pouring from a crack (lay it in the "
             "face row beside the Asclepeion); `basin`: a stone basin on grass below it.",
             names={"spout": (0, 0), "basin": (0, 1)})
    B = s.B
    for y in range(16):
        for x in range(16):
            B.px(x, y, "rk5" if y < 2 and x % 4 else ("rk4" if y < 2 else KG.rock_face(x, y, y - 2)))
    for y in range(6, 16):
        for x in (7, 8):
            B.px(x, y, "ar2" if (y + x) % 3 else "rk5")
    B.px(6, 6, "rk0")
    B.px(9, 6, "rk0")
    grass_fill(B, 0, 16, 16, 16)
    for y in range(18, 30):
        for x in range(2, 14):
            edge = y in (18, 29) or x in (2, 13)
            B.px(x, y, "rk1" if edge else ("rk3" if y < 20 else "ar2"))
    for y in range(16, 22):
        B.px(7, y, "ar2")
        B.px(8, y, "rk5" if y % 2 else "ar2")
    for x in range(3, 13):
        B.px(x, 30, "gd")
    return s


def cliff_cave():
    """A cave mouth halfway up the falls, with something glinting inside."""
    s = full("cliff_cave", "The cave mouth beside the falls", 1, 1, ["X"],
             "A face cell (`face`'s `mid`) with a dark cave mouth and a glint inside: the Horn "
             "of Achelous's cave (Act III). Lay it beside the waterfall.")
    B = s.B
    face_cell(B, 0, 0, "mid", "")
    for y in range(4, 15):
        r = [2, 3, 4, 5, 5, 5, 6, 6, 6, 6, 6][y - 4]
        for x in range(8 - r, 8 + r):
            B.px(x, y, "cv")
        B.px(8 - r - 1, y, "rk4")
        B.px(8 + r, y, "rk0")
    B.hline(2, 13, 15, "rk3")
    B.px(9, 10, "ar1")
    B.px(10, 9, "ar1")
    B.px(10, 10, "rk5")
    return s


def terrace():
    """A dry-stone retaining wall one row tall: the upper level to the north."""
    s = full("terrace", "Terrace wall", 4, 1, ["XXX."],
             "A dry-stone terrace wall, the upper level north of it: `W` end, `run`, `E` end, "
             "`stair` (walkable steps up through it).",
             names={"W": (0, 0), "run": (1, 0), "E": (2, 0), "stair": (3, 0)})
    B = s.B
    for cx in range(4):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                X = ox + x
                if y < 3:
                    c = L.grass_px(x, y)
                    if y == 2:
                        c = "rk4" if x % 5 else "rk5"
                elif y > 13:
                    c = "gd" if (x + y) % 2 else "g1"
                else:
                    # courses of rough stones, 4 px tall, staggered
                    row = (y - 3) // 4
                    off = (row * 5) % 8
                    jx = (x + off + ox) % 8
                    jy = (y - 3) % 4
                    if jx == 0 or jy == 3:
                        c = "rk0"
                    elif jy == 0:
                        c = "rk4"
                    elif jx == 1:
                        c = "rk3"
                    else:
                        c = "rk2" if (X * 3 + y) % 9 else "rk1"
                B.px(X, y, c)
        if cx == 0:
            for y in range(16):
                for x in range(3 if y < 13 else 2):
                    B.px(ox + x, y, L.grass_px(x, y))
                B.px(ox + 3, y, "rk1")
        if cx == 2:
            for y in range(16):
                for x in range(13, 16):
                    B.px(ox + x, y, L.grass_px(x, y))
                B.px(ox + 12, y, "rk0")
        if cx == 3:
            # steps: four treads climbing north, cheeks either side
            for y in range(16):
                for x in range(16):
                    if x < 2 or x > 13:
                        c = "rk1" if x in (1, 14) else "rk2"
                    else:
                        t = y % 4
                        c = "rk4" if t == 0 else ("rk3" if t == 1 else ("rk2" if t == 2 else "rk1"))
                    B.px(ox + x, y, c)
    return s


def oldwall():
    """Iamos's stretch of old wall: Cyclopean blocks, broken at both ends."""
    s = full("oldwall", "Iamos's old wall", 2, 1, ["XX"],
             "A stub of the old wall, Cyclopean, on grass: `W` and `E`, broken at both ends. "
             "Iamos sits on it.", names={"W": (0, 0), "E": (1, 0)})
    B = s.B
    grass_fill(B, 0, 0, 32, 16)
    blocks = [(2, 4, 13, 9), (13, 3, 22, 9), (22, 5, 30, 9),
              (4, 9, 16, 14), (16, 9, 28, 14)]
    for (x0, y0, x1, y1) in blocks:
        for y in range(y0, y1):
            for x in range(x0, x1):
                c = "rk3" if y == y0 else ("rk2" if (x + y) % 7 else "rk1")
                if x == x0:
                    c = "rk4"
                B.px(x, y, c)
        for x in range(x0, x1):
            B.px(x, y1, "rk0")
        for y in range(y0, y1 + 1):
            B.px(x1, y, "rk0")
    for x in range(3, 30):
        B.px(x, 15, "gd")
        if x % 5 == 0:
            B.px(x, 3 if 13 <= x < 22 else 4, "ar0")
    return s


def stair():
    """The temple hill's stair: three rows, up through the lip and the face."""
    s = full("stair", "The temple stair", 3, 3, ["...", "...", "..."],
             "A broad stone stair through the temple hill's lip (row 0) and its two-row face "
             "(rows 1-2): west cheek, run, east cheek. Walkable. The first step is the race's "
             "turning point.",
             names={"W0": (0, 0), "run0": (1, 0), "E0": (2, 0), "W1": (0, 1), "run1": (1, 1),
                    "E1": (2, 1), "W2": (0, 2), "run2": (1, 2), "E2": (2, 2)})
    B = s.B
    for y in range(48):
        for x in range(48):
            t = y % 8
            c = "rk4" if t == 0 else ("rk3" if t in (1, 2, 3) else ("rk2" if t in (4, 5, 6) else "rk1"))
            if x < 5 or x > 42:
                c = face_px(x, y % 16, lip=y < 2, foot=y >= 46)
                if x in (5 - 1, 43):
                    c = "rk0" if x == 43 else "rk4"
            elif x in (5, 6) or x in (41, 42):
                c = "rk1" if t else "rk3"
            B.px(x, y, c)
    s.B.a[:, 24:] = s.B.a[:, :24][:, ::-1]
    return s


# --------------------------------------------------------------------------
# The house kit: timber and stone under weathered shingles
# --------------------------------------------------------------------------

def shingles(Lr, ox, oy, w, h, row0=0):
    """Courses of wooden shingles, 8 x 4, staggered by half a shingle, lit along their
    top edge and shadowed under each course. The roof darkens toward the eaves. The
    texture repeats every 8 px across, so a long roof costs a handful of tiles."""
    for y in range(h):
        for x in range(w):
            Y = row0 + y
            X = ox + x
            course = Y // 4
            off = (course % 2) * 4
            jx = (X + off) % 8
            jy = Y % 4
            band = min(3, Y // 8)
            body = ("ah3", "ah2", "ah2", "ah1")[band]
            lit = ("ah3", "ah3", "ah2", "ah2")[band]
            if jy == 3:
                c = "ah0"
            elif jx == 0:
                c = "ah1" if band < 3 else "ah0"
            elif jy == 0:
                c = lit if jx < 6 else body
            else:
                c = body if jx != 7 else "ah1"
            Lr.px(ox + x, oy + y, c)


def daub_frame(Lr, ox, oy, w, h, posts=(0,)):
    """Timber framing with daub panels between (8 px periodic)."""
    for y in range(h):
        for x in range(w):
            c = "ap0" if ((ox + x) % 8 != 5 or y % 4 != 2) else "as3"
            Lr.px(ox + x, oy + y, c)
    for px in posts:
        for y in range(h):
            Lr.px(ox + px, oy + y, "at1")
            Lr.px(ox + px + 1, oy + y, "at0")


def rubble(Lr, ox, oy, w, h, seed=0):
    """A footing of rough grey stones (8 px periodic across)."""
    for y in range(h):
        for x in range(w):
            X = ox + x
            row = y // 3
            jx = (X + row * 4) % 8
            jy = y % 3
            if jy == 2 or jx == 0:
                c = "as0"
            elif jy == 0 and jx < 5:
                c = "as3"
            else:
                c = "as2" if jx != 6 else "as1"
            Lr.px(ox + x, oy + y, c)


def house_kit():
    names = {"ridgeW": (0, 0), "ridge": (1, 0), "ridgeE": (2, 0),
             "eaveW": (0, 1), "eave": (1, 1), "eaveE": (2, 1),
             "upW": (3, 0), "up": (4, 0), "upWin": (5, 0), "upE": (6, 0), "upRibbon": (7, 0),
             "wallW": (3, 1), "wall": (4, 1), "wallWin": (5, 1), "wallE": (6, 1), "door": (7, 1),
             "doorWolf": (0, 2), "doorPan": (1, 2), "wallSacks": (2, 2), "louvre": (3, 2),
             "doorWide": (4, 2)}
    walk = ["XXXXXXXX", "XXXXXXXD", "DDXXD..."]
    s = full("house", "The house kit: timber and stone under shingles", 8, 3, walk,
             "Arkadia's houses, built from parts. Roofs: `ridgeW` `ridge`… `ridgeE` over "
             "`eaveW` `eave`… `eaveE` (weathered wooden shingles). An upper storey of timber "
             "and daub: `upW` `up` `upWin` `upE`, and `upRibbon` (Klymene's window, a victor's "
             "ribbon on the sill). The ground storey, daub over a stone footing: `wallW` "
             "`wall` `wallWin` `wallE`, doors `door`, `doorWolf` (Nyktimos's hall: the grey "
             "wolf pelt over the lintel), `doorPan` (Krotos's: the horned mask), `doorWide` (the "
             "hall's double door), `wallSacks` (charcoal sacks against the wall), and `louvre` "
             "(a roof cell with a smoke louvre). Doors are MB_NON_ANIMATED_DOOR.", names=names)
    B = s.B
    # roofs
    for cx in range(3):
        for cy in range(2):
            ox, oy = cx * 16, cy * 16
            shingles(B, ox, oy, 16, 16, row0=cy * 16)
            if cy == 0:
                # the ridge: a capping beam along the top
                B.hline(ox, ox + 15, oy, "at0")
                B.hline(ox, ox + 15, oy + 1, "at2")
                B.hline(ox, ox + 15, oy + 2, "at1")
            else:
                # the eave board and its shadow
                B.hline(ox, ox + 15, oy + 13, "at2")
                B.hline(ox, ox + 15, oy + 14, "at1")
                B.hline(ox, ox + 15, oy + 15, "at0")
            if cx == 0:
                for y in range(16):
                    B.px(ox, oy + y, "at0")
                    B.px(ox + 1, oy + y, "at2")
                    B.px(ox + 2, oy + y, "at1")
            if cx == 2:
                for y in range(16):
                    B.px(ox + 15, oy + y, "at0")
                    B.px(ox + 14, oy + y, "at1")
                    B.px(ox + 13, oy + y, "at2")
    # the louvre: a little gabled vent on the ridge, a wisp of smoke
    ox, oy = 48, 32
    shingles(B, ox, oy, 16, 16)
    B.hline(ox, ox + 15, oy, "at0")
    B.hline(ox, ox + 15, oy + 1, "at2")
    B.hline(ox, ox + 15, oy + 2, "at1")
    for y in range(3, 10):
        for x in range(4, 12):
            B.px(ox + x, oy + y, "at1" if x in (4, 11) else ("ah0" if y > 4 else "at2"))
    B.hline(ox + 3, ox + 12, oy + 3, "at2")
    # the upper storey: daub between posts, a beam below
    for i, key in enumerate(("upW", "up", "upWin", "upE", "upRibbon")):
        ox, oy = (3 + i) * 16, 0
        daub_frame(B, ox, oy, 16, 16, posts=(0, 7) if key != "upW" else (0, 7))
        B.hline(ox, ox + 15, oy + 13, "at1")
        B.hline(ox, ox + 15, oy + 14, "at0")
        B.hline(ox, ox + 15, oy + 15, "as0")
        for x in range(16):
            B.px(ox + x, oy, "at0")
        if key in ("upWin", "upRibbon"):
            for y in range(3, 11):
                for x in range(3, 13):
                    B.px(ox + x, oy + y, "at0" if x in (3, 12) or y in (3, 10) else
                         ("al2" if key == "upRibbon" and y > 5 else "as0"))
            for y in range(4, 10):
                B.px(ox + 7, oy + y, "at1")
            if key == "upRibbon":
                # the sill, the ribbon hung from it, pale with age
                B.hline(ox + 2, ox + 13, oy + 11, "at2")
                for y in range(11, 15):
                    B.px(ox + 9, oy + y, "ad0")
                    B.px(ox + 10, oy + y, "ap0" if y % 2 else "ad0")
        if key == "upW":
            for y in range(16):
                B.px(ox, oy + y, "at0")
                B.px(ox + 1, oy + y, "at1")
        if key == "upE":
            for y in range(16):
                B.px(ox + 15, oy + y, "at0")
                B.px(ox + 14, oy + y, "at1")
    # the ground storey: daub over a stone footing, the eave's shadow on top
    def ground_wall(ox, oy, seed):
        daub_frame(B, ox, oy, 16, 8, posts=(0,))
        B.hline(ox, ox + 15, oy, "as0")
        B.hline(ox, ox + 15, oy + 1, "as1")
        B.hline(ox, ox + 15, oy + 8, "at1")
        rubble(B, ox, oy + 9, 16, 7, seed=seed)
    for i, key in enumerate(("wallW", "wall", "wallWin", "wallE", "door")):
        ox, oy = (3 + i) * 16, 16
        ground_wall(ox, oy, i)
        if key == "wallW":
            for y in range(16):
                B.px(ox, oy + y, "at0")
                B.px(ox + 1, oy + y, "as3" if y > 8 else "at1")
        if key == "wallE":
            for y in range(16):
                B.px(ox + 15, oy + y, "at0")
                B.px(ox + 14, oy + y, "as1" if y > 8 else "at1")
        if key == "wallWin":
            for y in range(2, 8):
                for x in range(4, 12):
                    B.px(ox + x, oy + y, "at0" if x in (4, 11) or y in (2, 7) else "as0")
            for x in range(4, 12):
                B.px(ox + x, oy + 8, "at2")
    def door_cell(ox, oy, seed, wide=False):
        ground_wall(ox, oy, seed)
        x0, x1 = (2, 14) if wide else (3, 13)
        for y in range(2, 16):
            for x in range(x0, x1):
                if x in (x0, x1 - 1) or y == 2:
                    c = "at0"
                elif wide and x == (x0 + x1) // 2:
                    c = "at0"
                else:
                    c = "at1" if (x - x0) % 3 else "at2"
                B.px(ox + x, oy + y, c)
        B.hline(ox + x0 - 1, ox + x1, oy + 1, "at2")
        B.px(ox + x1 - 3, oy + 9, "as3")
    door_cell(7 * 16, 16, 4)
    door_cell(0, 32, 5)
    door_cell(16, 32, 6)
    door_cell(64, 32, 7, wide=True)
    # the wolf pelt over the hall's lintel
    B.blit(["  k        k  ",
            " kgk      kgk ",
            "kgggkkkkkkgggk",
            " kggggggggggk ",
            "  kgwggggwgk  ",
            "   kggggggk   ",
            "    kkggkk    "],
           {"k": "as0", "g": "as2", "w": "ap0"}, 1, 32 - 3 + 3)
    # Pan's horned mask over Krotos's door
    B.blit(["k        k",
            "kk      kk",
            " kkaaaakk ",
            "  aakaka  ",
            "  aaaaaa  ",
            "   akka   ",
            "    aa    "],
           {"k": "at0", "a": "at2"}, 16 + 3, 32 + 2)
    # charcoal sacks against a wall
    ox, oy = 32, 32
    ground_wall(ox, oy, 8)
    for (x0, y0) in ((1, 7), (6, 6), (10, 8)):
        for y in range(y0, 16):
            for x in range(x0, x0 + 6):
                edge = x in (x0, x0 + 5) or y == y0
                B.px(ox + x, oy + y, "as0" if edge else ("ah1" if (x + y) % 3 else "ah0"))
    return s


def asclepeion():
    """The mountain Asclepeion: stone under shingles, the rod of Asclepius on a white
    plaque, a timber porch; it stands against the outcrop (its back is the rock)."""
    s = full("asclepeion", "The Asclepeion", 5, 4,
             ["XXXXX", "XXXXX", "XXXXX", "XXDXX"],
             "The Asclepeion, 5x4: shingles over stone, the rod of Asclepius on a white plaque, "
             "a porch on two posts, the door at (2,3) (MB_NON_ANIMATED_DOOR). Build it against "
             "the outcrop's south face, the spring's `spout` and `basin` beside its west wall.",
             names={"door": (2, 3)})
    B = s.B
    shingles(B, 0, 0, 80, 32)
    B.hline(0, 79, 0, "at0")
    B.hline(0, 79, 1, "at2")
    B.hline(0, 79, 2, "at1")
    for y in range(32):
        for x, c in ((0, "at0"), (1, "at2"), (2, "at1"), (79, "at0"), (78, "at1"), (77, "at2")):
            B.px(x, y, c)
    B.hline(0, 79, 29, "at2")
    B.hline(0, 79, 30, "at1")
    B.hline(0, 79, 31, "at0")
    # a white ridge-tile cross for the healers
    for y in range(4, 11):
        B.px(39, y, "ap0")
        B.px(40, y, "ap0")
    B.hline(36, 43, 6, "ap0")
    B.hline(36, 43, 7, "ap0")
    # stone walls, ashlar courses
    for y in range(32, 64):
        for x in range(80):
            row = (y - 32) // 4
            jx = (x + (row % 2) * 4) % 8
            jy = (y - 32) % 4
            c = "as0" if jx == 0 or jy == 3 else ("as3" if jy == 0 else ("as2" if jx != 6 else "as1"))
            B.px(x, y, c)
    B.hline(0, 79, 32, "as0")
    B.hline(0, 79, 33, "as0")
    # windows either side of the plaque
    for wx in (12, 60):
        for y in range(37, 45):
            for x in range(wx, wx + 8):
                B.px(x, y, "at0" if x in (wx, wx + 7) or y in (37, 44) else "as0")
        B.hline(wx - 1, wx + 8, 45, "as3")
    # the plaque: the rod of Asclepius, a serpent round a staff
    for y in range(35, 47):
        for x in range(32, 48):
            B.px(x, y, "ap0" if 32 < x < 47 and 35 < y < 46 else "as1")
    for y in range(37, 45):
        B.px(40, y, "at0")
    for (x, y) in ((38, 38), (39, 39), (41, 40), (42, 41), (41, 42), (39, 43), (38, 42), (41, 37),
                   (42, 38)):
        B.px(x, y, "ad0")
    # the porch: a beam on two posts, the door between
    B.hline(16, 63, 48, "at1")
    B.hline(16, 63, 49, "at0")
    for px in (21, 22, 57, 58):
        for y in range(50, 64):
            B.px(px, y, "at2" if px % 2 else "at1")
    for y in range(51, 64):
        for x in range(33, 47):
            B.px(x, y, "at0" if x in (33, 46) or y == 51 else ("at1" if (x - 33) % 3 else "at2"))
    B.px(43, 57, "as3")
    s.behaviors[(2, 3)] = "MB_NON_ANIMATED_DOOR"
    return s


def agora():
    """The Agora: a timber stall built round the foot of the town's biggest cypress."""
    s = full("agora", "The Agora's stall round the great cypress", 4, 6,
             ["XXXX", "XXXX", "XXXX", "XXXX", "XXXX", "XDXX"],
             "The town's biggest cypress (rows 0-2, on grass) with the Agora's stall built round "
             "its trunk (rows 3-5): a striped awning, nets and jars, the counter, the door at "
             "(1,5) (MB_NON_ANIMATED_DOOR).", names={"door": (1, 5)})
    L.ground(s, "grass", [(x, y) for y in range(3) for x in range(4)])
    # the crown: a vast flame, 64 x 48, its foot hidden by the awning
    art = L.Layer(64, 48)
    g = L.Layer(64, 48)
    for y in range(48):
        for x in range(64):
            g.px(x, y, L.grass_px(x, y))
    m = L.cypress_mask(64, 48, 31.5, 0, 58, 23.0, belly=0.74, seed=9, wobble=0.0)
    L.paint_foliage(art, m, cx=31.5, seed=9)
    art.a[:, 32:] = art.a[:, :32][:, ::-1]
    for y in range(48):
        for x in range(64):
            if art.a[y, x, 3]:
                s.M.a[y, x] = art.a[y, x]
            elif y > 40:
                # the crown's shadow on the grass at its sides
                c = L.grass_px(x, y)
                s.M.px(x, y, {"g3": "g1", "g2": "g1", "g1": "gd"}.get(c, c))
    B = s.B
    # The stall draws only from the town group: timber (at1, at2), ink for the dark,
    # the awning's saffron and red, earth-colored jars, grey nets.
    # the awning: saffron and red stripes, scalloped
    for y in range(48, 64):
        for x in range(64):
            if y < 50:
                c = "ink" if y == 48 else "at2"
            else:
                c = "af0" if (x // 4) % 2 else "af1"
            B.px(x, y, c)
    for x in range(64):
        B.px(x, 63 - (1 if x % 4 in (1, 2) else 0), "ink")
    # the trunk rising through the awning
    for y in range(48, 80):
        for x in range(28, 36):
            B.px(x, y, "ink" if x in (28, 35) else ("at1" if x < 32 else "ink"))
    # under the awning: nets hung from the boughs, shelves of jars, moon-cakes
    for y in range(64, 76):
        for x in range(64):
            if 28 <= x < 36:
                continue
            c = "ink" if (x + y) % 4 or y < 66 else "at1"
            B.px(x, y, c)
    for x in range(0, 64):
        for y in range(66, 74):
            if (x + y) % 4 == 0 and not 28 <= x < 36:
                B.px(x, y, "ak1")
    # a jar every 8 px along the shelf, red and earthen by turns of a cell
    for x0 in range(0, 64, 8):
        if 26 <= x0 < 36:
            continue
        c1 = "af1" if (x0 // 16) % 2 == 0 else "ae1"
        for y in range(70, 76):
            for x in range(x0 + 1, x0 + 6):
                B.px(x, y, c1 if x not in (x0 + 1, x0 + 5) and y > 70 else "ink")
        B.px(x0 + 3, 72, "ae2")
    # the counter and the front
    for y in range(76, 80):
        for x in range(64):
            B.px(x, y, "at2" if y == 76 else ("at1" if y < 79 else "ink"))
    for x in range(6, 26, 4):
        B.px(x, 75, "ae2")
        B.px(x + 1, 75, "ae2")
    for y in range(80, 96):
        for x in range(64):
            c = "at1" if (x % 8) else "ink"
            if y < 82:
                c = "at2"
            B.px(x, y, c)
    for y in range(82, 96):
        for x in range(18, 30):
            B.px(x, y, "ink" if x in (18, 29) or y == 82 or y < 88 else "at1")
    # a painted board: a jar and a coin, the market's sign
    for y in range(84, 92):
        for x in range(40, 56):
            B.px(x, y, "ae2" if 40 < x < 55 and 84 < y < 91 else "ink")
    B.blit([" kk ", "kaak", "kaak", " kk "], {"k": "ink", "a": "af1"}, 44, 85)
    B.blit([" kk", "kak", " kk"], {"k": "ink", "a": "af0"}, 50, 86)
    s.behaviors[(1, 5)] = "MB_NON_ANIMATED_DOOR"
    return s


def hut():
    """Hippothoos's hut: dug half into the bank, turf on its roof, logs for a front."""
    s = full("hut", "Hippothoos's charcoal hut", 4, 3, ["XXXX", "XXXX", "XXDX"],
             "A hut dug half into the hillside: turf on the roof, a front of split logs, "
             "charcoal sacks stacked by the door at (2,2) (MB_NON_ANIMATED_DOOR).",
             names={"door": (2, 2)})
    B = s.B
    # the turf roof: a green hump with earth showing at its edge
    for y in range(32):
        for x in range(64):
            c = L.grass_px(x, y)
            dx = (x - 31.5) / 34
            top = 3 + 10 * dx * dx * 4
            if y < top:
                c = L.grass_px(x, y)
            else:
                c = "g1" if (x % 8 != 3 or y % 4 != 1) else "g3"
                if x % 8 == 6 and y % 4 == 3:
                    c = "gd"
                if y > 26:
                    c = "ae0" if y > 28 else "ae1"
            B.px(x, y, c)
    # turf edge tufts
    for x in range(0, 64, 3):
        B.px(x, 26, "g2")
    # the smoke hole and its wisp
    for y in range(8, 12):
        for x in range(30, 34):
            B.px(x, y, "ink")
    for (x, y) in ((31, 7), (32, 5), (31, 3), (32, 1)):
        B.px(x, y, "ak1")
        B.px(x + 1, y, "ak0")
    # the log front
    for y in range(32, 48):
        for x in range(64):
            jy = (y - 32) % 4
            c = "ink" if jy == 3 else ("at2" if jy == 0 else "at1")
            if (x + ((y - 32) // 4) * 3) % 8 == 0 and jy != 3:
                c = "ink"
            B.px(x, y, c)
    for y in range(36, 46):
        for x in range(36, 44):
            B.px(x, y, "ink")
    for y in range(36, 48):
        for x in range(36, 44):
            if x in (36, 43) or y == 36:
                B.px(x, y, "ink")
            else:
                B.px(x, y, "ink" if y < 38 else ("at1" if (x - 36) % 3 else "ink"))
    # charcoal sacks at the left
    for (x0, y0) in ((3, 39), (11, 37), (19, 40)):
        for y in range(y0, 48):
            for x in range(x0, x0 + 8):
                edge = x in (x0, x0 + 7) or y == y0
                B.px(x, y, "ink" if edge else ("ak0" if (x + y) % 3 else "ink"))
    s.behaviors[(2, 2)] = "MB_NON_ANIMATED_DOOR"
    return s


def kiln():
    """A charcoal kiln: an earth mound with vents, smoking day and night."""
    s = L.struct("kiln", "A charcoal kiln", 2, 2, SEC, walk=["XX", "XX"], on="grass",
                 notes="A smoking charcoal kiln on grass: an earth mound with its vents.")
    M = s.M
    for y in range(32):
        for x in range(32):
            dx, dy = (x - 15.5) / 14.5, (y - 21) / 11
            if dx * dx + dy * dy <= 1 and y >= 10:
                c = "ae1" if dx < -0.2 else ("ae0" if dx > 0.4 else "ae1")
                if dx * dx + dy * dy > 0.82:
                    c = "ae0"
                if (x * 5 + y * 3) % 13 == 0:
                    c = "ae2"
                M.px(x, y, c)
            elif y >= 28 and abs(x - 16) < 15:
                M.px(x, y, "gd" if (x + y) % 2 else None)
    for (x, y) in ((8, 20), (16, 16), (24, 21), (12, 26), (21, 27)):
        M.blit(["kk", "kh"], {"k": "ink", "h": "al1"}, x, y)
    for (x, y, c) in ((16, 12, "ak0"), (15, 10, "ak1"), (16, 8, "ak1"), (17, 6, "ak0"), (16, 4, "ak1"),
                      (15, 2, "ak1"), (17, 11, "ak1"), (14, 7, "ak0")):
        M.px(x, y, c)
        M.px(x + 1, y, c)
    return s


def byre():
    """Krotos's byre: a wattle lean-to with a straw roof, open to the pasture."""
    s = full("byre", "Krotos's byre", 2, 3, ["XX", "XX", "XX"],
             "A wattle lean-to for the kids, with a straw roof, against the goatherd's house.")
    B = s.B
    for y in range(16):
        for x in range(32):
            c = "af0" if (x + y * 2) % 5 else "at2"
            if y < 2:
                c = "at1"
            if y > 13:
                c = "ink"
            B.px(x, y, c)
    for y in range(16, 48):
        for x in range(32):
            c = "at1" if ((x // 2) + (y // 4)) % 2 else "at2"
            if x % 8 == 0:
                c = "ink"
            B.px(x, y, c)
    for y in range(30, 48):
        for x in range(10, 22):
            B.px(x, y, "ink" if y < 33 else ("af0" if (x + y) % 4 == 0 and y > 42 else "ink"))
    return s


def fence():
    """Post-and-rail fence on grass, for the goat pasture. The corners come in
    mirrored pairs, so Porytiles stores each pair once."""
    names = {"h": (0, 0), "v": (1, 0), "nw": (2, 0), "ne": (3, 0), "sw": (4, 0), "se": (5, 0),
             "gate": (6, 0)}
    s = L.struct("fence", "Post-and-rail fence", 7, 1, SEC, walk=["XXXXXX."], on="grass",
                 names=names, notes="The goat pasture's fence on grass: `h` and `v` runs, "
                                    "corners `nw` `ne` `sw` `se`, and an open `gate` (walkable).")
    M = s.M

    def post(ox, x, y0=5, y1=13):
        for y in range(y0, y1):
            M.px(ox + x, y, "at2")
            M.px(ox + x + 1, y, "at1")
        M.px(ox + x, y1, "gd")
        M.px(ox + x + 1, y1, "gd")

    def rails(ox, x0, x1):
        for x in range(x0, x1):
            M.px(ox + x, 7, "at2")
            M.px(ox + x, 8, "at1")
            M.px(ox + x, 10, "at2")
            M.px(ox + x, 11, "at1")
            M.px(ox + x, 12, "gd")

    def vrail(ox, y0, y1):
        for y in range(y0, y1):
            M.px(ox + 7, y, "at2")
            M.px(ox + 8, y, "at1")

    rails(0, 0, 16)
    post(0, 3)
    post(0, 11)
    vrail(16, 0, 16)
    post(16, 7, 3, 9)
    rails(32, 8, 16); vrail(32, 7, 16); post(32, 7)
    rails(64, 8, 16); vrail(64, 0, 9); post(64, 7)
    for (src, dst) in ((32, 48), (64, 80)):
        M.a[:, dst:dst + 16] = M.a[:, src:src + 16][:, ::-1]
    post(96, 0)
    post(96, 14)
    return s


def track():
    """The old racecourse: a flat track of packed earth, kerbed, two cells wide."""
    names = {"W": (0, 0), "E": (1, 0), "post": (2, 0)}
    s = full("track", "The old racecourse", 3, 1, ["..X"],
             "The old racecourse, two cells wide, running north-south: `W` and `E` its two "
             "halves (stone kerbs outside), `post` the carved finishing post on grass beside "
             "the track (blocks).", names=names)
    B = s.B
    for cx in range(2):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                c = "ae1" if ((x % 8) * 3 + y * 5) % 9 else "ae0"
                if (x + y * 7) % 23 == 0:
                    c = "ae2"
                B.px(ox + x, y, c)
        if cx in (0, 2):
            for y in range(16):
                B.px(ox, y, L.grass_px(0, y))
                B.px(ox + 1, y, "ak1" if y % 4 else "ak0")
                B.px(ox + 2, y, "ae0")
        if cx in (1, 3):
            for y in range(16):
                B.px(ox + 15, y, L.grass_px(15, y))
                B.px(ox + 14, y, "ak1" if y % 4 else "ak0")
                B.px(ox + 13, y, "ae0")
            # the lane line between the halves
        for y in range(0, 16, 3):
            B.px(ox + (15 if cx in (0, 2) else 0), y, "ae2")
    # the finishing post, carved and worn, on grass
    ox = 32
    grass_fill(B, ox, 0, 16, 16)
    for y in range(1, 14):
        for x in range(6, 10):
            B.px(ox + x, y, "at2" if x < 8 else "at1")
        B.px(ox + 5, y, "ink")
        B.px(ox + 10, y, "ink")
    B.hline(ox + 5, ox + 10, 0, "ink")
    B.blit(["kaak", "kaak"], {"k": "ink", "a": "af0"}, ox + 6, 3)
    B.hline(ox + 4, ox + 12, 14, "gd")
    return s


# --------------------------------------------------------------------------
# The Temple of Artemis and its precinct
# --------------------------------------------------------------------------

def temple():
    """The small Doric temple on its hill: a roof of terracotta, a pediment with the
    silver moon disc, a blue-and-marble frieze, four columns. It stands on rock."""
    s = full("temple", "The Temple of Artemis", 5, 4, ["XXXXX"] * 4,
             "The small Doric temple on the hill, 5x4, on the hill's rock top: terracotta "
             "roof, the pediment with its silver moon disc, the frieze, four columns. The way "
             "in is the precinct's gate below it.")
    rock_top_fill(s.B, 0, 0, 80, 64)
    M = s.M
    W = 80
    # the roof: tiles in rows, a ridge, seen from above and in front
    for y in range(2, 20):
        for x in range(4, 76):
            jy = (y - 2) % 4
            c = "tc1" if jy else "tc0"
            if (x + ((y - 2) // 4) * 3) % 6 == 0:
                c = "tc0"
            elif jy == 1:
                c = "tc2"
            M.px(x, y, c)
    M.hline(4, 75, 2, "tc0")
    for y in range(2, 20):
        M.px(4, y, "tc0")
        M.px(75, y, "tc0")
    # the pediment: a low triangle of marble, the disc in its middle
    for y in range(20, 34):
        half = 36 * (y - 20) / 13
        for x in range(4, 76):
            d = abs(x - 39.5)
            if d <= half:
                c = "am2" if d < half - 2 else "am3"
                M.px(x, y, c)
            elif y < 33:
                M.px(x, y, "tc1" if (x + y) % 5 else "tc0")
        M.px(int(39.5 - half), y, "am1")
        M.px(int(39.5 + half), y, "am4")
    for y in range(22, 33):
        for x in range(32, 48):
            dx, dy = x - 39.5, y - 27.5
            r = (dx * dx + dy * dy) ** 0.5
            if r <= 5.6:
                c = "av2" if dx + dy < -2 else ("av1" if r < 4.6 else "av0")
                M.px(x, y, c)
    # the cornice and the frieze: triglyphs and metopes
    M.hline(2, 77, 34, "am1")
    M.hline(2, 77, 35, "am3")
    for y in range(36, 42):
        for x in range(4, 76):
            k = (x - 4) % 10
            M.px(x, y, "ab0" if k < 3 else "am2")
            if k == 1:
                M.px(x, y, "av0")
    M.hline(4, 75, 42, "am4")
    # four columns, fluted, the cella's shadow between them
    for y in range(43, 60):
        for x in range(4, 76):
            M.px(x, y, "ab0" if y < 47 else "ink")
    for cx in (12, 30, 49, 67):
        for y in range(43, 60):
            for x in range(cx - 3, cx + 4):
                d = x - cx
                c = "am1" if d < -1 else ("am2" if d < 1 else "am3")
                if d in (-1, 2) and y > 45:
                    c = "am4" if d == 2 else "am2"
                M.px(x, y, c)
        M.hline(cx - 4, cx + 4, 43, "am1")
    # the stylobate
    for y in range(60, 64):
        M.hline(2, 77, y, "am1" if y == 60 else ("am2" if y < 63 else "am4"))
    L.mirror_cells(s, "middle")
    return s


def precinct():
    """The precinct wall and its gate (the warp into the night garden)."""
    names = {"topW": (0, 0), "top": (1, 0), "propW": (2, 0), "prop": (3, 0),
             "faceW": (0, 1), "face": (1, 1), "col": (2, 1), "gate": (3, 1)}
    s = full("precinct", "The precinct wall and gate", 4, 2, ["XXXX", "XXXD"],
             "The low marble wall round the temple's precinct, seen from the stair: `topW` and "
             "`top` (its coping, rock behind), `faceW` and `face` (its face); the gate: "
             "`propW` `prop` `propW` mirrored (the propylon's little roof) over `col` `gate` "
             "`col` mirrored. Mirror the west pieces for the east (they're symmetric about the "
             "gate). The gate is MB_NON_ANIMATED_DOOR: the warp into the night garden.",
             names=names)
    rock_top_fill(s.B, 0, 0, 64, 16)
    M = s.M
    # the coping, with the rock behind it
    for x in range(0, 32):
        for y in range(10, 16):
            M.px(x, y, "am1" if y == 10 else ("am2" if y < 15 else "am3"))
    for y in range(10, 16):
        M.px(0, y, "am4")
    # the propylon's roof: tiles, a little pediment, centred on the gate's cell
    # (x 55.5), so the east half is this one mirrored
    for y in range(0, 16):
        for x in range(36, 64):
            d = abs(x - 55.5)
            if y < 9:
                M.px(x, y, "tc1" if (y % 3) else "tc0")
            elif d < 19 - (y - 9) * 2.5:
                M.px(x, y, "am2" if d < 17 - (y - 9) * 2.5 else "am1")
            else:
                M.px(x, y, "tc0" if y == 9 else "am3")
    M.hline(36, 63, 0, "tc0")
    for y in range(16):
        M.px(36, y, "tc0" if y < 9 else "am4")
    # a crescent on the gable
    for (x, y) in ((55, 11), (54, 12), (54, 13), (55, 14), (56, 14)):
        M.px(x, y, "av1")
    # the face of the wall: big marble blocks
    B = s.B
    for y in range(16, 32):
        for x in range(0, 32):
            jx = (x + ((y - 16) // 8) * 8) % 16
            jy = (y - 16) % 8
            c = "am4" if jx == 0 or jy == 7 else ("am1" if jy == 0 else "am2")
            B.px(x, y, c)
    for y in range(16, 32):
        B.px(0, y, "am4")
    # the gate's columns and the dark of the garden beyond
    for y in range(16, 32):
        for x in range(32, 64):
            c = "am2"
            if 40 <= x <= 47:
                d = x - 43.5
                c = "am1" if d < -1 else ("am2" if d < 1.5 else "am3")
            elif x > 47:
                d = abs(x - 55.5)
                c = "ab0" if y < 24 else "ink"
                if y > 28:
                    c = "rk1"
                if d > 6.5:
                    c = "am4" if y < 30 else "am3"
            B.px(x, y, c)
    s.behaviors[(3, 1)] = "MB_NON_ANIMATED_DOOR"
    return s


def woodgate():
    """The Cypress Wood's gate: two great trunks under the canopy, a lintel with the
    crescent, the dark of the Wood between them."""
    s = full("woodgate", "The Cypress Wood's gate", 3, 4,
             ["XXX", "XXX", "XXX", "X.X"],
             "Cut into the canopy on the square's west: the crowns over a timber lintel with "
             "Artemis's crescent, two great trunks, the dark of the Wood between them. The "
             "opening's floor (1,3) is MB_NON_ANIMATED_DOOR: the warp into the Wood.",
             names={"door": (1, 3)})
    B = s.B
    ramp = L.RAMP_TOWN
    for y in range(64):
        for x in range(48):
            B.px(x, y, L.crown_texture(x, y, ramp))
    # the dark of the Wood
    for y in range(26, 64):
        for x in range(13, 35):
            depth = min(y - 26, 20)
            c = "ac0" if depth > 6 else "ac1"
            if y > 60:
                c = "ac1" if (x + y) % 3 else "ac0"
            B.px(x, y, c)
    # the trunks
    for y in range(20, 64):
        for (x0, x1) in ((6, 14), (34, 42)):
            for x in range(x0, x1):
                c = "k1" if x - x0 in (1, 2, 3) else "ink"
                if (y * 3 + x) % 11 == 0:
                    c = "ac0"
                B.px(x, y, c)
        for x in (5, 14, 33, 42):
            B.px(x, y, "ac0")
    # roots
    for (x, y) in ((4, 62), (3, 63), (15, 62), (16, 63), (32, 62), (31, 63), (43, 62), (44, 63)):
        B.px(x, y, "k1")
    # grass at the foot either side
    for y in range(58, 64):
        for x in list(range(0, 4)) + list(range(44, 48)):
            B.px(x, y, L.grass_px(x, y))
    B.a[:, 24:] = B.a[:, :24][:, ::-1]
    # the lintel, on the top layer of its row: a beam with a carved crescent
    T = s.T
    for y in range(22, 30):
        for x in range(2, 46):
            T.px(x, y, "at0" if y in (22, 29) else ("at2" if y < 25 else "at1"))
    for (x, y) in ((23, 24), (22, 25), (22, 26), (23, 27), (24, 27), (25, 26)):
        T.px(x, y, "ap0")
    s.behaviors[(1, 3)] = "MB_NON_ANIMATED_DOOR"
    return s


def build(shapes):
    import arkadia_trees as TR
    out = TR.town(shapes["town_canopy"])
    out += [rock(shapes["town_rock"]), faces(), grotto(), spout(), cliff_cave(), terrace(),
            oldwall(), stair(), house_kit(), asclepeion(), agora(), hut(), kiln(), byre(),
            fence(), track(), temple(), precinct(), woodgate()]
    pr = next(s for s in out if s.key == "precinct")
    out.append(L.mirrored(pr, "precinct_e", "The precinct wall and gate, east half",
                          notes="`precinct` mirrored: lay its columns 1-3 east of the gate."))
    return out
