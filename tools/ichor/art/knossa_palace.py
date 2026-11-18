"""The Palace of Minos above ground (LABYRINTH §3, §11): the Central Court's
gypsum paving and the bull-leaping lane with its painted line, ruined ashlar
walls cut with double axes, red columns that taper downward under black
capitals, porticoes crowned with horns of consecration, doorways into the
four rooms, the North Entrance's charging-bull relief, the bull-leaper fresco,
the lily prince, a light well, the Theatral Area's steps and worn paving, the
Gentle Bull's pen, a kouloura, and the stair up the palace's hill.

Its Minoan red, ochre, gypsum and black, and its fresco blues, are the
labyrinth tileset's own (knossa_lib's `minoan` and `fresco` are
labyrinth_art's, verbatim), so the palace meets Ring I in one palette.
Floors fill the bottom layer; walls, columns and furniture stand in the
middle layer over them, their tops in the top layer over the player.
"""
from __future__ import annotations

import math

import knossa_lib as N
from knossa_lib import ground, grid, struct

SEC_COURT = "court"
SEC_WALLS = "walls"
SEC_FRESCO = "fresco"

# --------------------------------------------------------------------------
# Paving: big gypsum slabs, terracotta-red plaster in the joints
# --------------------------------------------------------------------------

LAYOUTS = {
    "A": [(0, 0, 16, 9), (0, 9, 10, 7), (10, 9, 6, 7)],
    "B": [(0, 0, 7, 16), (7, 0, 9, 10), (7, 10, 9, 6)],
    "C": [(0, 0, 11, 6), (11, 0, 5, 6), (0, 6, 16, 10)],
    "D": [(0, 0, 16, 16)],
}


def slab_px(x, y, lay, worn=False, seed=0):
    """A gypsum slab's color at (x, y) in a 16 px cell laid out by `lay`:
    big slabs, a thin line of faded red plaster between them."""
    for i, (x0, y0, w, h_) in enumerate(lay):
        if x0 <= x < x0 + w and y0 <= y < y0 + h_:
            xx, yy = x - x0, y - y0
            if xx == w - 1 or yy == h_ - 1:
                return "mt2"                         # the red plaster joint, faded
            if yy == 0 or xx == 0:
                return "mg2"                         # the slab's lit edge
            k = N.h(x + 16 * i, y, 7 + seed)
            if worn and k % 9 == 0:
                return "mg0"
            if k % 29 == 0:
                return "mg0"
            return "mg1" if k % 17 else "mg2"
    return "mg1"


def pave(L, ox, oy, name="A", worn=False, seed=0):
    lay = LAYOUTS[name]
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, slab_px(x, y, lay, worn, seed))


def paving():
    names = {"A": (0, 0), "B": (1, 0), "C": (2, 0), "D": (3, 0), "cracked": (4, 0),
             "weeds": (5, 0), "edge_N": (0, 1), "edge_S": (1, 1), "edge_W": (2, 1),
             "edge_E": (3, 1), "edge_NW": (4, 1), "edge_NE": (5, 1), "edge_SW": (0, 2),
             "edge_SE": (1, 2), "lane": (2, 2), "lane_line": (3, 2), "lane_N": (4, 2),
             "lane_S": (5, 2), "lane_h": (0, 3), "lane_h_line": (1, 3), "lane_W": (2, 3),
             "lane_E": (3, 3), "dance": (4, 3), "dance_b": (5, 3)}
    s = struct("paving", "Court paving and the bull-leaping lane", 6, 4, SEC_COURT,
               walk=["......", "......", "......", "......"], names=names,
               notes="The Central Court's gypsum paving, big slabs set in red plaster (LABYRINTH "
                     "§3). Lay `A` `B` `C` `D` in a mix, `cracked` and `weeds` (grass in the "
                     "joints, the palace is a ruin above ground) here and there. Where the "
                     "paving meets grass it breaks up: `edge_N` (grass to the north) `edge_S` "
                     "`edge_W` `edge_E` and the outer corners `edge_NW` `edge_NE` `edge_SW` "
                     "`edge_SE` (on borrowed grass). **The bull-leaping lane** (LABYRINTH §3): "
                     "nine cells of smoother gypsum edged in painted red, north-south `lane_N`, "
                     "`lane` x7, `lane_S` (the bull paws at `lane_N`, you stand at `lane_S`), or "
                     "west-east `lane_W` `lane_h` `lane_E`; `lane_line` / `lane_h_line` is the "
                     "painted line across it, on the cell in front of you, where you press A "
                     "as his head crosses. **The Theatral Area**: `dance` and `dance_b`, its "
                     "worn paving, rings scuffed into the slabs by dancers, the dancing floor's "
                     "twin. All walkable.")
    B, M = s.B, s.M
    for i, n in enumerate("ABCD"):
        pave(B, i * 16, 0, n)
    pave(B, 64, 0, "D", seed=3)
    for (a, b, c, d) in ((66, 2, 69, 7), (69, 7, 68, 11), (68, 11, 72, 14)):
        B.line(a, b, c, d, "mg0")
    pave(B, 80, 0, "C", seed=5)
    # weeds in the joints (green, middle layer)
    for (x, y) in ((80 + 6, 5), (80 + 11, 5), (80 + 3, 14), (80 + 13, 12), (80 + 7, 9)):
        grid(M, x - 1, y - 2, [".g.", "gGg", "g.g"], {"g": "g2", "G": "my3"})
    # edges onto borrowed grass: the slabs break up at the margin
    edges = {"edge_N": (0, 1), "edge_S": (1, 1), "edge_W": (2, 1), "edge_E": (3, 1),
             "edge_NW": (4, 1), "edge_NE": (5, 1), "edge_SW": (0, 2), "edge_SE": (1, 2)}
    for nm, (cx, cy) in edges.items():
        ground(s, "grass", [(cx, cy)])
        ox, oy = cx * 16, cy * 16
        d = nm.split("_")[1]
        lay = LAYOUTS["ABCD"[(cx + cy) % 4]]
        for y in range(16):
            for x in range(16):
                keep = True
                jag = N.h(x // 3, y // 3, cx + cy) % 3
                if "N" in d and y < 4 + jag:
                    keep = False
                if "S" in d and y > 11 - jag:
                    keep = False
                if "W" in d and x < 4 + jag:
                    keep = False
                if "E" in d and x > 11 - jag:
                    keep = False
                if keep:
                    M.px(ox + x, oy + y, slab_px(x, y, lay))
        # the broken margin: a dark lip where slab meets earth
        for y in range(16):
            for x in range(16):
                if M.get(ox + x, oy + y) is not None:
                    for (dx, dy) in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < 16 and 0 <= yy < 16 and M.get(ox + xx, oy + yy) is None:
                            M.px(ox + x, oy + y, "mo0" if dy >= 0 else "mg2")
                            break
    # the lane: smooth gypsum between painted red borders
    def lane(ox, oy, vertical=True, line=False, end=None):
        for y in range(16):
            for x in range(16):
                u, v = (x, y) if vertical else (y, x)
                if u in (1, 14):
                    c = "mr1"
                elif u in (2, 13):
                    c = "mr2"
                elif u in (0, 15):
                    c = "mt1"
                else:
                    c = "mg2" if (v + u) % 7 else "mg1"
                if line and v in (7, 8) and 2 < u < 13:
                    c = "mr1" if v == 7 else "mr0"
                if end == "start" and v < 2 and 0 < u < 15:
                    c = "mr1" if v == 1 else "mt1"
                if end == "stop" and v > 13 and 0 < u < 15:
                    c = "mr1" if v == 14 else "mt1"
                pt = (u, v) if True else None
                B.px(ox + (x if vertical else x), oy + (y if vertical else y),
                     c)
        if end:
            # a painted rosette at each end of the lane
            cx_, cy_ = 8, (5 if end == "start" else 10)
            for y in range(16):
                for x in range(16):
                    u, v = (x, y) if vertical else (y, x)
                    if math.hypot(u - 7.5, v - cy_) < 3.2:
                        c = "mr1" if math.hypot(u - 7.5, v - cy_) > 1.8 else "mo1"
                        B.px(ox + x, oy + y, c)
    lane(32, 32)
    lane(48, 32, line=True)
    lane(64, 32, end="start")
    lane(80, 32, end="stop")
    lane(0, 48, vertical=False)
    lane(16, 48, vertical=False, line=True)
    lane(32, 48, vertical=False, end="start")
    lane(48, 48, vertical=False, end="stop")
    # the Theatral Area's paving: rings worn into the slabs
    for cx, rr in ((4, 6.0), (5, 6.0)):
        ox, oy = cx * 16, 48
        pave(B, ox, oy, "D", seed=cx)
        for y in range(16):
            for x in range(16):
                # a ring scuffed by circling feet, worn deeper on one side
                d = math.hypot(x - 7.5, (y - 7.5) * 1.15)
                ang = math.atan2(y - 7.5, x - 7.5)
                if abs(d - rr) < 0.55 and (cx == 4 or math.sin(ang) > -0.4):
                    B.px(ox + x, oy + y, "mg0")
    return s


# --------------------------------------------------------------------------
# Walls: gypsum ashlar, masons' double axes, ruined tops
# --------------------------------------------------------------------------

def ashlar(x, y, dark=False):
    """Gypsum ashlar on the wall's face, 16 px periodic: big blocks in two
    courses, each lit along its top."""
    course = y // 8
    off = 0 if course % 2 == 0 else 8
    xx = (x + off) % 16
    yy = y % 8
    if yy == 7 or xx == 15:
        c = "mb" if dark else "mg0"
    elif yy == 0:
        c = "mg2"
    elif xx == 0:
        c = "mg2"
    elif yy == 6:
        c = "mg0"
    else:
        c = "mg1"
    if dark and c in ("mg1", "mg2"):
        c = {"mg1": "mg0", "mg2": "mg1"}[c]
    return c


def walls():
    names = {"top_L": (0, 0), "top": (1, 0), "top_R": (2, 0), "top_broken": (3, 0),
             "top_horns": (4, 0), "side": (5, 0), "side_N": (6, 0), "side_S": (7, 0),
             "face_L": (0, 1), "face": (1, 1), "face_R": (2, 1), "face_labrys": (3, 1),
             "face_frieze": (4, 1), "corner_NW": (5, 1), "corner_NE": (6, 1), "side_T": (7, 1),
             "door": (0, 2), "door_stair": (1, 2), "face_window": (2, 2), "face_shadow": (3, 2),
             "horns": (4, 2), "rubble": (5, 2), "block": (6, 2), "corner_SW": (7, 2)}
    s = struct("walls", "Gypsum ashlar walls, doorways and horns", 8, 3, SEC_WALLS,
               walk=["XXXXXXXX", "XXXXXXXX", "DDXXXXXX"], names=names,
               notes="The palace's walls, standing one storey above the ruin, in gypsum ashlar "
                     "(on court paving). A wall running west to east is a `top_*` row (its top "
                     "seen from above, drawn over the player) over a `face_*` row: `_L` `_R` end "
                     "it; `top_broken` is a gap in the top course, `top_horns` a top course "
                     "crowned with horns of consecration. Faces: `face_labrys` (a block cut with "
                     "the masons' double axe), `face_frieze` (a red and ochre painted band, for "
                     "the court's west façade), `face_window` (a small high window), "
                     "`face_shadow` (the face in the shadow of a portico). **Doorways** "
                     "(`MB_NON_ANIMATED_DOOR`, warps to the rooms): `door` (gypsum jambs, a "
                     "red lintel; the Throne Room, the West Magazines, the Queen's Megaron) and "
                     "`door_stair` (steps going down into the dark: the Grand Staircase). A wall "
                     "running north to south is `side` (its top, a strip), ending `side_N` / "
                     "`side_S`, `side_T` where it meets a west-east wall; turn corners with "
                     "`corner_NW` `corner_NE` `corner_SW` (the top's corner). Loose: `horns` "
                     "(great horns of consecration on a plinth, impassable), `rubble` (fallen "
                     "blocks, impassable), `block` (one fallen block). The paving under each "
                     "piece is `paving.A`, so lay `A` around walls, or let the mix fall where it "
                     "may.")
    B, M, Tl = s.B, s.M, s.T
    # paving under everything
    for cy in range(3):
        for cx in range(8):
            pave(B, cx * 16, cy * 16, "A")
    # tops: the upper course's top surface, cut stone, ochre mortar
    def top_cell(ox, oy, end=None, broken=False, horns=False):
        y0, y1 = 6, 16
        for y in range(y0, y1):
            for x in range(16):
                if end == "L" and x < 2:
                    continue
                if end == "R" and x > 13:
                    continue
                if broken and 4 <= x <= 10 and y < 11 + (x % 3):
                    continue
                yy = y - y0
                if yy == 0:
                    c = "mb"
                elif yy == 1:
                    c = "mg2"
                elif yy >= 8:
                    c = "mg2" if yy == 8 else "mg1"
                else:
                    k = (x + (3 if yy > 3 else 0)) % 8
                    c = "mo2" if k == 0 else ("mg1" if yy % 4 else "mg0")
                Tl.px(ox + x, oy + y, c)
            if end == "L":
                for y in range(y0, y1):
                    Tl.px(ox + 2, oy + y, "mb")
            if end == "R":
                for y in range(y0, y1):
                    Tl.px(ox + 13, oy + y, "mb")
        if horns:
            grid(Tl, ox + 1, oy + 0, [
                "kk..........kk",
                "k2k........k1k",
                "k22k......k11k",
                "k222kkkkkk111k",
                "k2222222221110",
                "kkkkkkkkkkkkkk",
            ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
    top_cell(0, 0, "L")
    top_cell(16, 0)
    top_cell(32, 0, "R")
    top_cell(48, 0, broken=True)
    top_cell(64, 0, horns=True)
    # faces
    def face_cell(ox, oy, end=None, dark=False):
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 2:
                    continue
                if end == "R" and x > 13:
                    continue
                c = ashlar(ox + x, y, dark)
                if y >= 14:
                    c = "mo0" if y == 14 else "mt0"
                M.px(ox + x, oy + y, c)
        if end == "L":
            for y in range(16):
                M.px(ox + 2, oy + y, "mg2")
        if end == "R":
            for y in range(16):
                M.px(ox + 13, oy + y, "mb")
                M.px(ox + 12, oy + y, "mg0")
    face_cell(0, 16, "L")
    face_cell(16, 16)
    face_cell(32, 16, "R")
    face_cell(48, 16)
    grid(M, 48 + 4, 16 + 2, [
        "k.....k",
        "kk...kk",
        "kkk.kkk",
        "kkkkkkk",
        "kkk.kkk",
        "kk.k.kk",
        "k..k..k",
        "...k...",
        "...k...",
        "...k...",
    ], {"k": "mg0"})
    face_cell(64, 16)
    for x in range(16):
        for y in range(5, 11):
            c = "mr1" if y in (6, 9) else ("mo1" if y in (7, 8) else "mr0")
            if y in (7, 8) and (x % 6) in (2, 3):
                c = "mr1"
            M.px(64 + x, 16 + y, c)
    face_cell(16, 32)    # under the window; window drawn below
    face_cell(32, 32)
    grid(M, 32 + 4, 32 + 2, [
        "kkkkkkkk",
        "krrrrrrk",
        "kr0000rk",
        "kr0000rk",
        "kr0000rk",
        "krrrrrrk",
        "kkkkkkkk",
    ], {"k": "mt0", "r": "mr1", "0": "mb"})
    face_cell(48, 32, dark=True)
    # side walls: a north-south wall's top, a strip down the middle
    def side_cell(ox, oy, n_end=False, s_end=False, t=False):
        for y in range(16):
            for x in range(5, 11):
                if n_end and y < 4:
                    continue
                if s_end and y > 11:
                    continue
                c = "mg1" if x not in (5, 10) else ("mg2" if x == 5 else "mg0")
                if (y + 3) % 8 == 0:
                    c = "mo2"
                (M if s_end else Tl).px(ox + x, oy + y, c)
            if t:
                pass
        if n_end:
            for x in range(5, 11):
                Tl.px(ox + x, oy + 4, "mg2")
                Tl.px(ox + x, oy + 3, "mb")
        if s_end:
            # the wall's end face, seen from the south
            for y in range(12, 16):
                for x in range(5, 11):
                    M.px(ox + x, oy + y, ashlar(x, y))
            for x in range(5, 11):
                M.px(ox + x, oy + 15, "mt0")
    side_cell(80, 0)
    side_cell(96, 0, n_end=True)
    side_cell(112, 0, s_end=True)
    # side_T: a north-south wall meeting a west-east wall's top
    top_cell(112, 16)
    for y in range(0, 7):
        for x in range(5, 11):
            Tl.px(112 + x, 16 + y, "mg1" if x not in (5, 10) else ("mg2" if x == 5 else "mg0"))
    # corners: tops turning
    for (cx, cy, nm) in ((5, 1, "NW"), (6, 1, "NE"), (7, 2, "SW")):
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                if nm == "NW" and ((y >= 6 and x >= 5) and (y < 16)) and not (x > 10 and y > 15):
                    inside = (y >= 6 and x >= 5) and (x <= 10 or y <= 15)
                    if inside and (y < 16 and (x <= 10 or y >= 6)):
                        c = "mg1"
                        if y == 6 or x == 5:
                            c = "mb" if (y == 6 and x >= 5) or (x == 5 and y >= 6) else c
                        Tl.px(ox + x, oy + y, c)
                if nm == "NE" and y >= 6 and x <= 10:
                    c = "mg1"
                    if y == 6 or x == 10:
                        c = "mb"
                    Tl.px(ox + x, oy + y, c)
                if nm == "SW" and y <= 15 and 5 <= x <= 10 and y < 6:
                    Tl.px(ox + x, oy + y, "mg1" if x not in (5, 10) else "mg0")
        if nm == "SW":
            top_cell(ox, oy, "L")
            for y in range(0, 7):
                for x in range(5, 11):
                    Tl.px(ox + x, oy + y, "mg1" if x not in (5, 10) else ("mg2" if x == 5 else "mg0"))
    # doorways in a face
    for cx, stair in ((0, False), (1, True)):
        ox, oy = cx * 16, 32
        face_cell(ox, oy)
        for y in range(2, 16):
            for x in range(3, 13):
                if x in (3, 12):
                    c = "mg2" if x == 3 else "mg0"
                elif y < 5:
                    c = ("mr1", "mr0", "mb")[y - 2]
                else:
                    c = "ink"
                    if stair and y >= 8:
                        d = y - 8
                        c = ("mg1", "mg0", "mb", "ink")[d % 4] if d < 8 else "ink"
                        if d % 4 == 0:
                            c = "mg2" if y < 12 else "mg1"
                M.px(ox + x, oy + y, c)
        for x in range(2, 14):
            M.px(ox + x, oy + 15, "mg0")
    # great horns of consecration on a plinth (loose)
    ox, oy = 64, 32
    grid(M, ox + 1, oy + 2, [
        "kk..........kk",
        "k2k........k1k",
        "k22k......k11k",
        "k222k....k111k",
        "k2222kkkk1111k",
        "k222222222111k",
        "kkkkkkkkkkkkkk",
        ".k2222222110k.",
        ".k2222222110k.",
        ".k1111111000k.",
        ".kkkkkkkkkkkk.",
    ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
    # rubble and a fallen block
    for (rx, ry) in ((1, 6), (7, 3), (9, 9), (3, 11)):
        grid(M, 80 + rx, 32 + ry, [".kkkk.", "k2221k", "k2111k", "k1100k", ".kkkk."],
             {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
    grid(M, 96 + 2, 32 + 4, [
        ".kkkkkkkkkk.",
        "k2222222221k",
        "k2111111110k",
        "k21k1k11110k",
        "k2111111100k",
        "k1000000000k",
        ".kkkkkkkkkk.",
    ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
    s.walk = ["XXXXXXXX", "XXXXXXXX", "DDXXXXXX"]
    s.behaviors = {(0, 2): "MB_NON_ANIMATED_DOOR", (1, 2): "MB_NON_ANIMATED_DOOR"}
    return s


# --------------------------------------------------------------------------
# Columns and porticoes
# --------------------------------------------------------------------------

def column(L_top, L, ox, oy, broken=False):
    """A Minoan column, 1 x 2 cells from oy: a black cushion capital on a
    square abacus, a red shaft wider at the top than the foot, a gypsum base."""
    # abacus and capital (top cell, drawn over the player)
    if not broken:
        grid(L_top, ox + 1, oy + 6, [
            "kkkkkkkkkkkkkk",
            "k666666666655k",
            "kkkkkkkkkkkkkk",
            ".kbbbbbbbbbbk.",
            "kbBbbbbbbbbbbk",
            "kbBbbbbbbbbbbk",
            ".kbbbbbbbbbbk.",
            "..kkkkkkkkkk..",
            "..k23333332k..",
            "..kkkkkkkkkk..",
        ], {"k": "ink", "6": "mg2", "5": "mg1", "b": "mb", "B": "mg0", "2": "mo1", "3": "mo0"})
    # the shaft: from 10 px wide under the capital to 7 at the foot
    y_top = oy + 16 if not broken else oy + 22
    for y in range(y_top, oy + 29):
        t = (y - (oy + 16)) / 13.0
        half = 5.0 - 1.6 * t
        for x in range(16):
            d = x + 0.5 - 8
            if abs(d) <= half:
                if d < -half + 1.2:
                    c = "mr3"
                elif d < -half + 3:
                    c = "mr2"
                elif d > half - 1.2:
                    c = "mr0"
                else:
                    c = "mr1"
                L.px(ox + x, y, c)
            elif abs(d) <= half + 1:
                L.px(ox + x, y, "ink")
    if broken:
        for x in range(3, 13):
            if L.get(ox + x, oy + 22) is not None:
                L.px(ox + x, oy + 22 + (x % 3 == 0), "mr3")
                L.px(ox + x, oy + 21 + (x % 2), "ink")
    # the base: a gypsum disc
    grid(L, ox + 2, oy + 28, [
        ".kkkkkkkkkk.",
        "k2222222111k",
        "k1111111000k",
        ".kkkkkkkkkk.",
    ], {"k": "ink", "2": "mg2", "1": "mg1", "0": "mg0"})


def columns():
    names = {"col_top": (0, 0), "col": (0, 1), "beam_col": (1, 0), "stump": (1, 1),
             "beam_L": (2, 0), "beam": (3, 0), "beam_R": (4, 0), "beam_horns": (5, 0),
             "under_col": (2, 1), "under": (3, 1), "pithos_top": (5, 1),
             "pithos": (5, 2), "col_grass_top": (6, 0), "col_grass": (6, 1)}
    s = struct("columns", "Red columns, porticoes and a pithos", 7, 3, SEC_WALLS,
               walk=["TTTTTTT", "XXXXXXX", "XXXXXXX"], names=names,
               notes="LABYRINTH §3's columns: red shafts that **taper downward**, wider at the "
                     "top, under black cushion capitals, on gypsum bases (on court paving). A "
                     "column is `col_top` (the capital, drawn over the player) over `col` "
                     "(impassable); `stump_top` over `stump` is one broken off; `col_grass_top` "
                     "over `col_grass` stands in the grass (borrowed). **A portico**: a beam "
                     "row over a row of columns and the shaded floor between them: `beam_L` "
                     "`beam` (`beam_horns`, horns of consecration on the roof line) `beam_R` "
                     "above, `beam_col` where a column's capital meets the beam; under the "
                     "beam, `under_col` (a column in the portico's shade) alternating with "
                     "`under` (shaded paving, walkable). `pithos_top` over `pithos`: a giant "
                     "storage jar taller than you, its rope bands in relief (impassable).")
    B, M, Tl = s.B, s.M, s.T
    for cy in range(3):
        for cx in range(6):
            pave(B, cx * 16, cy * 16, "A")
    column(Tl, M, 0, 0)
    column(Tl, M, 16, 0, broken=True)
    # the column in the grass
    ground(s, "grass", [(6, 0), (6, 1), (6, 2)])
    column(Tl, M, 96, 0)
    for x in range(96 + 3, 96 + 13):
        if M.get(x, 31) is None:
            M.px(x, 31, "mt0")
    # portico beam: banded red, black and ochre timber, its roof's edge above
    def beam(ox, oy, end=None, horns=False):
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 1:
                    continue
                if end == "R" and x > 14:
                    continue
                if y < 6:
                    continue
                c = {6: "mb", 7: "mg2", 8: "mg1", 9: "mb", 10: "mr2", 11: "mr1", 12: "mr1",
                     13: "mr0", 14: "ink", 15: "mb"}[y]
                if y in (10, 11, 12) and x % 8 == 3:
                    c = "mo1"
                Tl.px(ox + x, oy + y, c)
        if horns:
            grid(Tl, ox + 2, oy + 0, [
                "kk........kk",
                "k2k......k1k",
                "k22k....k11k",
                "k222kkkk111k",
                "k22222221110",
                "kkkkkkkkkkkk",
            ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
    beam(32, 0, "L")
    beam(48, 0)
    beam(64, 0, "R")
    beam(80, 0, horns=True)
    # under the beam: the portico's shade on the paving, a column in it
    for (cx, col) in ((2, True), (3, False), (4, True)):
        ox, oy = cx * 16, 16
        for y in range(16):
            for x in range(16):
                c = B.get(ox + x, oy + y)
                B.px(ox + x, oy + y, {"mg2": "mg1", "mg1": "mg0", "mg0": "mo0", "mt1": "mt0"}.get(c, c)
                     if y < 10 else c)
        if col:
            # the shaft continues up to the beam in the shade
            for y in range(0, 13):
                t = y / 13.0
                half = 4.6 - 1.2 * t
                for x in range(16):
                    d = x + 0.5 - 8
                    if abs(d) <= half:
                        c = "mr2" if d < -half + 2 else ("mr0" if d > half - 1.5 else "mr1")
                        M.px(ox + x, oy + y, c)
                    elif abs(d) <= half + 1:
                        M.px(ox + x, oy + y, "ink")
            grid(M, ox + 2, oy + 12, [
                ".kkkkkkkkkk.",
                "k2222222111k",
                "k1111111000k",
                ".kkkkkkkkkk.",
            ], {"k": "ink", "2": "mg1", "1": "mg0", "0": "mo0"})
    # the column top under a beam: capital merging into the beam above
    for y in range(16):
        for x in range(16):
            if Tl.a[y, 48 + x, 3]:
                Tl.a[y, 16 + x] = Tl.a[y, 48 + x]
    grid(Tl, 16 + 2, 14, ["kkkkkkkkkkkk", ".kbbbbbbbbk."], {"k": "ink", "b": "mb"})
    # the pithos, taller than a man
    ox = 80
    grid(M, ox + 2, 16 + 4, [
        "....kkkkkk....",
        "...k222211k...",
        "..kk221110kk..",
        ".k2222111100k.",
        "k222211111100k",
        "k2k11k11k11k0k",
        "k222211111100k",
        "k221r1r1r1r10k",
        "k2r1r1r1r1r10k",
        "k222111111100k",
        "kk2kk1kk1kk0kk",
        "k222111111100k",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "r": "mr1"})
    grid(M, ox + 2, 32, [
        "k222111111100k",
        "k221111111000k",
        ".k2111111100k.",
        ".kk2kk1kkk0kk.",
        "..k21111100k..",
        "..k21111100k..",
        "...k211100k...",
        "...k111000k...",
        "....kkkkkk....",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0"})
    s.walk = ["TTTTTTT", "XX..X.X" if False else "XXX.XXX", "XXXXXXX"]
    s.walk = ["TTTTTTT", "XXX.XXX", "XXXXXXX"]
    return N.pick(s, ["col_top", "beam_col", "beam_L", "beam", "beam_R", "beam_horns",
                      "col_grass_top", "col", "stump", "under_col", "under",
                      "pithos_top", "col_grass", "pithos"], w=7, key="columns",
                  notes=s.notes, section=SEC_WALLS)


# --------------------------------------------------------------------------
# Frescoes and reliefs: on a wall two face rows tall
# --------------------------------------------------------------------------

def bull(L, ox, oy, sc=1.0, body="fs", shade="fr", lit="fcr", flip=False, charging=True):
    """A bull in profile, facing west (east if flip): body, lowered head,
    forward horns, legs at the gallop, the tail flung up."""
    import numpy as np
    W, H = int(48 * sc) + 2, int(32 * sc) + 2
    sub = N.Layer(W, H)

    def P(x, y):
        return (x * sc, y * sc)
    sub.ellipse(*P(15, 9), *P(39, 23), body)            # the barrel
    sub.ellipse(*P(10, 7), *P(22, 21), body)            # the shoulder
    if charging:
        sub.ellipse(*P(3, 13), *P(13, 22), body)        # the head, lowered
    else:
        sub.ellipse(*P(3, 8), *P(13, 17), body)
    hy = 13 if charging else 8
    # legs: forelegs reaching, hind legs driving
    for (a, b, c, d) in ((14, 19, 9, 29), (18, 20, 15, 30), (33, 20, 38, 29), (36, 19, 42, 27)):
        for t in range(0, 11):
            x = a + (c - a) * t / 10
            y = b + (d - b) * t / 10
            sub.rect(int(x * sc), int(y * sc), max(2, int(2 * sc)), max(2, int(2 * sc)), body)
    # tail
    for t in range(0, 12):
        x = 38 + t * 0.6
        y = 12 - t * 0.7 + (t * t) * 0.03
        sub.px(int(x * sc), int(y * sc), body)
    # shade the belly, light the back
    a = sub.a
    m = a[..., 3] > 0
    ys, xs = np.nonzero(m)
    top = {}
    for y, x in zip(ys, xs):
        top[x] = min(top.get(x, 999), y)
    for y, x in zip(ys, xs):
        if y - top[x] < max(1, int(2 * sc)):
            sub.px(int(x), int(y), lit)
        elif y > (19 * sc) and x < 40 * sc:
            sub.px(int(x), int(y), shade)
    sub.outline("ink")
    # horns, pale, curving forward
    for (hx0, hy0, hx1, hy1) in ((7, hy, 1, hy - 4), (9, hy - 1, 5, hy - 6)):
        for t in range(0, 8):
            x = hx0 + (hx1 - hx0) * t / 7
            y = hy0 + (hy1 - hy0) * t / 7 - (0.08 * t * (7 - t))
            sub.px(int(x * sc), int(y * sc), "fw")
    sub.px(int(6 * sc), int((hy + 3) * sc), "ink")       # the eye
    for y in range(H):
        for x in range(W):
            if sub.a[y, x, 3]:
                xx = (W - 1 - x) if flip else x
                if 0 <= oy + y < L.h and 0 <= ox + xx < L.w:
                    L.a[oy + y, ox + xx] = sub.a[y, x]


BULL = [
    "............kkkk.........................",
    "..........kkllllkkkkk....................",
    ".........kllllllllllllkkkkkkkkkk......kk.",
    "...hh...kllllbbbbbbbbbbbbbbbbbllkk...k.k.",
    "..h..h.kbbbbbbbbbbbbbbbbbbbbbbbbbbkkk..k.",
    "..h...kbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk....",
    "...h.kbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk...",
    "....kbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk...",
    "...kbbebbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk...",
    "..kbbbbbbbkbbbbbbbbbbbbbbbbbbbbbbbbbbk...",
    ".kbbbbbbbkkbbbbbbbbbbbbbbbbbbbbbbbbbk....",
    ".kbbbbddk.kbbbbbbbdddddddddddddbbbbbk....",
    "..kdddkk..kbbbddddkkkkkkkkkkkkkddbbbk....",
    "...kkk...kbbddkk.............kkdddbk.....",
    ".........kbdk..kk.............kkddk......",
    "........kbdk...kdk.............kddk......",
    ".......kbdk....kdk..............kddk.....",
    "......kbdk.....kdk...............kddk....",
    ".....kbdk......kdk................kddk...",
    "....kddk.......kddk................kddk..",
    "...kkkk........kkkk................kkkk..",
]


def bull_sprite(L, ox, oy, body, dark, light, horn="fw", spots=None):
    """The fresco bull, head down at the charge, facing west (41 x 21)."""
    lg = {"k": "ink", "b": body, "d": dark, "l": light, "h": horn, "e": "ink"}
    grid(L, ox, oy, BULL, lg)
    for (x, y) in spots or ():
        grid(L, ox + x, oy + y, ["dd", "d."], {"d": dark})


def figure(L, x, y, skin, kilt="fy0", pose="stand"):
    """A small fresco figure (about 4 x 10): a dark head of curls, skin, a kilt."""
    if pose == "stand":
        grid(L, x, y, [
            ".kk.",
            "kssk",
            ".ss.",
            "sssss",
            ".yy.",
            ".yy.",
            ".s.s",
            ".s.s",
        ], {"k": "ink", "s": skin, "y": kilt})
    elif pose == "arms_up":
        grid(L, x, y, [
            "s..s",
            "skks",
            ".ss.",
            ".ss.",
            ".yy.",
            ".yy.",
            ".s.s",
            "s..s",
        ], {"k": "ink", "s": skin, "y": kilt})
    elif pose == "vault":
        # upside down over the bull's back, legs flung up and over
        grid(L, x, y, [
            "s.....s",
            ".s...s.",
            "..yyy..",
            "..sss..",
            "..sss..",
            "...k...",
            "..kkk..",
        ], {"k": "ink", "s": skin, "y": kilt})


def frescoes():
    names = {"bull_TL": (0, 0), "bull_T": (1, 0), "bull_TR": (2, 0), "bull_BL": (0, 1),
             "bull_B": (1, 1), "bull_BR": (2, 1),
             "leap_TL": (3, 0), "leap_T": (4, 0), "leap_TR": (5, 0), "leap_BL": (3, 1),
             "leap_B": (4, 1), "leap_BR": (5, 1),
             "prince_TL": (6, 0), "prince_TR": (7, 0), "prince_BL": (6, 1), "prince_BR": (7, 1)}
    s = struct("frescoes", "The charging bull, the bull-leapers, the lily prince", 8, 2,
               SEC_FRESCO, walk=["XXXXXXXX", "XXXXXXXX"], names=names,
               notes="Panels for a wall two face rows tall (stack `walls.face` over `walls.face`; "
                     "the panels' ground is that ashlar). **The charging bull** (`bull_*`, 3 x "
                     "2), the North Entrance's painted relief: a red bull head-down at the "
                     "charge under an olive, on a pale sky. **The bull-leapers** (`leap_*`, 3 x "
                     "2), for the Central Court's east wall: on a blue ground a white bull at "
                     "the gallop, one leaper vaulting his back, one gripping his horns, one "
                     "waiting at his tail to catch, in a border of painted checks. **The lily "
                     "prince** (`prince_*`, 2 x 2), the relief in the corridor south of the "
                     "court: a red-skinned youth in a crown of lilies and plumes, walking among "
                     "lilies. All impassable; each is a bg event.")
    B, M = s.B, s.M
    for cy in range(2):
        for cx in range(8):
            for y in range(16):
                for x in range(16):
                    c = ashlar(cx * 16 + x, cy * 16 + y)
                    if cy == 1 and y >= 14:
                        c = "mo0" if y == 14 else "mt0"
                    B.px(cx * 16 + x, cy * 16 + y, c)

    def frame(ox, w, h_, ground_c, border="checks"):
        for y in range(2, h_ - 2):
            for x in range(1, w - 1):
                edge = x in (1, w - 2) or y in (2, h_ - 3)
                inner = x in (2, w - 3) or y in (3, h_ - 4)
                if edge:
                    c = "ink"
                elif inner:
                    if border == "checks":
                        c = "fr" if ((x + y) // 2) % 2 else "fw"
                    else:
                        c = border
                else:
                    c = ground_c(x, y) if callable(ground_c) else ground_c
                M.px(ox + x, y, c)
    # the charging bull: pale sky, an olive, ground line
    def sky(x, y):
        if y > 25:
            return "fy0" if (x + y) % 3 else "fy1"
        return "fb3"
    frame(0, 48, 32, sky, border="fr")
    # the olive: a gnarled trunk and a grey-green crown behind the bull
    for y in range(8, 26):
        M.px(40 + (y % 3 == 0), y, "fs")
        M.px(41, y, "ink" if y % 4 else "fs")
    M.ellipse(32, 4, 45, 14, "fg0")
    for (x, y) in ((34, 6), (37, 5), (40, 7), (43, 9), (36, 10), (41, 11), (33, 9)):
        grid(M, x, y, ["ll", ".l"], {"l": "fg1"})
    bull_sprite(M, 3, 6, "fs", "fr", "fcr")
    # the bull-leapers: a blue ground, a white bull, three leapers
    frame(48, 48, 32, "fb1", border="checks")
    bull_sprite(M, 48 + 3, 9, "fw", "fq", "fw", horn="fy1",
                spots=((16, 6), (22, 4), (27, 7), (13, 9)))
    figure(M, 48 + 18, 2, "fs", pose="vault")          # vaulting his back
    figure(M, 48 + 3, 3, "fw", kilt="fy0", pose="arms_up")   # at his horns
    figure(M, 48 + 39, 14, "fw", kilt="fy0", pose="arms_up")  # to catch
    # the lily prince: a red ground, the youth among lilies
    def red(x, y):
        return "fr" if y < 26 else "fs"
    frame(96, 32, 32, red, border="fy0")

    def lily(x, y):
        grid(M, x, y, [
            "w.w.w",
            ".www.",
            "..y..",
            "..g..",
            ".gg..",
        ], {"w": "fw", "y": "fy1", "g": "fg0"})
    for (x, y) in ((96 + 4, 16), (96 + 23, 18), (96 + 5, 24), (96 + 24, 9)):
        lily(x, y)
    grid(M, 96 + 11, 3, [
        "..b.w.b...",
        ".bwbwbwb..",
        "..wwwww...",
        "...kkk....",
        "..kssk....",
        "...ss.....",
        "..ssss....",
        ".sssss.s..",
        "s.sss..s..",
        "s.sss.....",
        "..yyy.....",
        "..ybyy....",
        "..yyyy....",
        "..s..s....",
        "..s..s....",
        "..s...s...",
        "..s...s...",
        ".ss..ss...",
    ], {"b": "fb2", "w": "fw", "k": "ink", "s": "fcr", "y": "fy0"})
    # his skin red-brown, as the Minoans painted men
    for y in range(3, 22):
        for x in range(96 + 10, 96 + 22):
            if M.get(x, y) == "pl" or M.get(x, y) == "fcr":
                M.px(x, y, "fs" if (x + y) % 5 else "fp")
    return s


# --------------------------------------------------------------------------
# The Theatral Area, the pen, a light well, a kouloura, the hill's stair
# --------------------------------------------------------------------------

def court_works():
    names = {"steps_L": (0, 0), "steps": (1, 0), "steps_R": (2, 0), "steps_corner": (3, 0),
             "steps_V": (4, 0), "fence_L": (0, 1), "fence": (1, 1), "fence_R": (2, 1),
             "fence_V": (3, 1), "fence_gate": (4, 1), "well_TL": (5, 0), "well_TR": (6, 0),
             "well_BL": (5, 1), "well_BR": (6, 1), "pit_TL": (0, 2), "pit_TR": (1, 2),
             "pit_BL": (0, 3), "pit_BR": (1, 3), "stair_L": (2, 2), "stair_R": (3, 2),
             "stair_foot_L": (2, 3), "stair_foot_R": (3, 3), "trough": (4, 2),
             "hay": (4, 3), "drain": (5, 2), "plinth": (6, 2)}
    s = struct("court_works", "The Theatral Area, the pen, a light well, the hill's stair", 7, 4,
               SEC_COURT, walk=["..XX.XX", "XXXX.XX", "XX..XX.", "XX..XX."], names=names,
               notes="On court paving. **The Theatral Area** (LABYRINTH §3): broad shallow "
                     "steps where the court watched the dances, seen from the front: `steps_L` "
                     "`steps` `steps_R` (walkable, you climb them), `steps_V` a flight running "
                     "north (walkable), `steps_corner` where two flights meet (impassable). Lay "
                     "its floor with `paving.dance`. **The Gentle Bull's pen** in the Central "
                     "Court: a timber rail fence, `fence_L` `fence` `fence_R` west to east, "
                     "`fence_V` north to south, `fence_gate` (Sarpedon opens it; impassable "
                     "until scripted), `trough` and `hay` inside (impassable). **A light well** "
                     "(`well_*`, 2 x 2): a square shaft open to the sky, a parapet round it and "
                     "a red column going down into the dark (impassable). **A kouloura** "
                     "(`pit_*`, 2 x 2): the West Court's round stone-lined pit, grass in it "
                     "(impassable). **The stair up the palace's hill**: `stair_L` `stair_R` "
                     "over `stair_foot_L` `stair_foot_R`, a broad gypsum stair (walkable), set "
                     "in the hill's limestone face (`cliff`) where the Bull Road arrives. "
                     "`drain`: a stone channel in the paving (walkable); `plinth`: an empty "
                     "statue base (impassable).")
    B, M, Tl = s.B, s.M, s.T
    for cy in range(4):
        for cx in range(7):
            pave(B, cx * 16, cy * 16, "ABCD"[(cx + cy) % 4])
    # steps, seen from the front: three treads a cell
    def treads(ox, oy, end=None):
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 2:
                    continue
                if end == "R" and x > 13:
                    continue
                k = y % 5
                c = ("mg2", "mg1", "mg1", "mg0", "mo0")[k]
                if (x + (y // 5) * 5) % 11 == 0 and k in (1, 2):
                    c = "mg0"
                B.px(ox + x, oy + y, c)
        if end == "L":
            for y in range(16):
                B.px(ox + 2, oy + y, "mb")
        if end == "R":
            for y in range(16):
                B.px(ox + 13, oy + y, "mb")
    treads(0, 0, "L")
    treads(16, 0)
    treads(32, 0, "R")
    treads(48, 0)
    for y in range(16):        # the corner: a flight turning north
        for x in range(8):
            B.px(48 + x, y, ("mg2", "mg1", "mg1", "mg0", "mo0")[x % 5])
    for y in range(16):        # steps_V: treads running north, seen side-on
        for x in range(16):
            B.px(64 + x, y, ("mg2", "mg1", "mg1", "mg0", "mo0")[x % 5])
    # the pen's timber rails (terra), over paving
    def rail(ox, oy, kind):
        if kind in ("L", "M", "R", "G"):
            for x in range(16):
                if kind == "L" and x < 3:
                    continue
                if kind == "R" and x > 12:
                    continue
                for y in (5, 6, 10, 11):
                    M.px(ox + x, oy + y, "wd2" if y in (5, 10) else "wd1")
                M.px(ox + x, oy + 12, "wd0")
            posts = {"L": (3,), "R": (11,), "M": (7,), "G": (1, 13)}[kind]
            for px_ in posts:
                for y in range(2, 15):
                    M.px(ox + px_, oy + y, "wd1")
                    M.px(ox + px_ + 1, oy + y, "wd0")
                M.px(ox + px_, oy + 2, "wd3")
            if kind == "G":
                for x in range(3, 13):
                    for y in (5, 6, 10, 11):
                        M.px(ox + x, oy + y, "wd3" if y in (5, 10) else "wd2")
                M.line(ox + 3, oy + 11, ox + 12, oy + 5, "wd1")
                M.px(ox + 12, oy + 8, "ink")
        else:
            for y in range(16):
                for x in (6, 9):
                    M.px(ox + x, oy + y, "wd2" if x == 6 else "wd1")
                M.px(ox + 7, oy + y, "wd0" if y % 8 == 0 else None)
            for y in (3, 11):
                for x in range(5, 11):
                    M.px(ox + x, oy + y, "wd1")
    rail(0, 16, "L")
    rail(16, 16, "M")
    rail(32, 16, "R")
    rail(48, 16, "V")
    rail(64, 16, "G")
    # the light well: a parapet round a dark square shaft, a column below
    for y in range(32):
        for x in range(32):
            X, Y = 80 + x, y
            if x < 3 or x > 28 or y < 3 or y > 28:
                c = "mg2" if (x < 3 or y < 3) else "mg0"
                if x in (0, 31) or y in (0, 31):
                    c = "mb"
                M.px(X, Y, c)
            else:
                depth = min(x - 3, 28 - x, y - 3, 28 - y)
                c = "mb" if y < 8 else "ink"
                if y < 6:
                    c = "mg0"
                M.px(X, Y, c)
    for y in range(8, 27):
        for x in range(20, 26):
            M.px(80 + x, y, "mr1" if x < 24 else "mr0")
        M.px(80 + 19, y, "ink")
        M.px(80 + 26, y, "ink")
    grid(M, 80 + 18, 6, ["kkkkkkkkkk", "kbbbbbbbbk"], {"k": "ink", "b": "mb"})
    # the kouloura: a round pit lined with stones, grass growing in it
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - 15.5, (y - 15.5) * 1.1)
            if d < 11:
                c = "mo0" if y < 12 else "mt0"
                if d < 9 and y > 10:
                    c = "mt0"
                M.px(x, 32 + y, c)
            elif d < 14:
                ang = math.atan2(y - 15.5, x - 15.5)
                k = int((ang + math.pi) / (2 * math.pi) * 18)
                c = "mg1" if k % 2 else "mg0"
                if d > 13.2 or (d < 11.6 and y > 15):
                    c = "mb"
                if d < 11.8 and y <= 15:
                    c = "mg2"
                M.px(x, 32 + y, c)
    for (gx, gy) in ((12, 20), (17, 23), (20, 18), (14, 26)):
        grid(M, gx, 32 + gy, ["g.g", ".g."], {"g": "mo1"})
    # the stair up the hill: broad gypsum treads between limestone cheeks
    for y in range(32):
        for x in range(32):
            X, Y = 32 + x, 32 + y
            if x < 3 or x > 28:
                c = "mg0" if x in (0, 31) else "mg1"
                if x in (2, 29):
                    c = "mb"
            else:
                k = y % 6
                c = ("mg2", "mg2", "mg1", "mg1", "mg0", "mb")[k]
            B.px(X, Y, c)
    # trough and hay inside the pen
    grid(M, 64 + 2, 32 + 6, [
        "kkkkkkkkkkkk",
        "k2222222221k",
        "k1bbbbbbb10k",
        "k1111111100k",
        ".kkkkkkkkkk.",
    ], {"k": "wd0", "2": "wd3", "1": "wd2", "0": "wd1", "b": "b1"})
    grid(M, 64 + 2, 48 + 4, [
        "..y.yy.y....",
        ".yYyyYyyy...",
        "yYyyYyyYyy..",
        "yyYyyyYyyyy.",
        ".tttttttttt.",
    ], {"y": "tc3", "Y": "wd3", "t": "wd1"})
    # a drain channel and an empty plinth
    for y in range(16):
        for x in range(6, 10):
            B.px(80 + x, 32 + y, "mb" if x in (6, 9) else "mt0")
    grid(M, 96 + 2, 32 + 4, [
        ".kkkkkkkkkk.",
        "k2222222221k",
        "k2111111110k",
        "k2111111110k",
        "k1000000000k",
        ".kkkkkkkkkk.",
    ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})
    s.walk = ["...X.XX", "XXXXXXX", "XX..X.X", "XX..X.X"]
    return N.pick(s, ["steps_L", "steps", "steps_R", "steps_V", "steps_corner", "well_TL",
                      "well_TR", "fence_L", "fence", "fence_R", "fence_V", "fence_gate",
                      "well_BL", "well_BR", "pit_TL", "pit_TR", "stair_L", "stair_R", "trough",
                      "drain", "plinth", "pit_BL", "pit_BR", "stair_foot_L", "stair_foot_R",
                      "hay"], w=7, key="court_works", notes=s.notes, section=SEC_COURT)


def build():
    return [paving(), walls(), columns(), frescoes(), court_works()]
