"""The stage side of Thyrsa's theater: the skene's painted front and its three
doors, the roof and the god-machine, the paraskenia (the wings either side of
the stage), the stage floor and its colonnaded front, the parodoi, the torches
round the orchestra, the thymele (and its inky handprint), the play's props,
and the terrace gate at the top of the cavea.

Each painter fills whole 16 x 16 cells. Kits repeat: the façade is a handful of
wall, column and panel cells, and the roof three rows of three, so the skene
costs tiles by the kind of cell, not by its width.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eleusa_lib as E  # noqa: E402
import theater_cavea as V  # noqa: E402
import theater_lib as T  # noqa: E402
from eleusa_lib import put  # noqa: E402
from theater_lib import Struct  # noqa: E402

SEC_STAGE = "stage"
SEC_PROPS = "props"


def struct(key, title, w, h, section, walk=None, notes="", names=None, on=None, behaviors=None):
    s = E.struct(key, title, w, h, section, walk=walk, notes=notes, names=names, on=on)
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch == "S":
                s.behaviors[(cx, cy)] = "MB_SOUTH_ARROW_WARP"
    s.behaviors.update(behaviors or {})
    return s


def fill(L, ox, oy, fn, x0=0, y0=0, x1=15, y1=15):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = fn(x, y)
            if c:
                L.px(ox + x, oy + y, c)


def _h(x, y, salt=0):
    return V._hash(x, y, salt)


# --------------------------------------------------------------------------
# Ground the stage side shares with the cavea
# --------------------------------------------------------------------------

def paving(L, ox, oy, gx0=0, gy0=0):
    """The aisle's flagstones (theater_cavea.aisle_color), phase-locked to the
    map so the parodos meets the aisle seamlessly. (gx0, gy0) is the cell's
    map pixel position."""
    fill(L, ox, oy, lambda x, y: V.aisle_color(gx0 + x, gy0 + y, -1, 0.0))


def planks(x, y):
    """The stage floor: boards running east-west, nailed at the joists."""
    yy = y % 8
    if yy == 7:
        return "qw0"
    if yy == 0:
        return "qw2"
    if (x + (y // 8) * 5) % 16 == 0:
        return "qw0"
    if x % 8 == 3 and yy == 3:
        return "qw0"
    return "qw1" if (x * 3 + y) % 11 else "qw2"


# --------------------------------------------------------------------------
# The skene: roof, frieze, wall, columns, panels, doors
# --------------------------------------------------------------------------

def roof_px(x, y):
    """Laconian roof tiles, cover tiles every 4 px lit on the left."""
    c = x % 4
    course = y % 4
    if course == 3:
        return "qr0" if c == 3 else "qr1"
    if course == 0 and c in (1, 2):
        return "qr2"
    return ("qr2", "qr1", "qr1", "qr0")[c]


def roof_cell(L, ox, oy, row, side):
    fill(L, ox, oy, roof_px)
    if row == "ridge":
        L.hline(ox, ox + 15, oy, "ink")
        for x in range(16):
            k = x % 6
            L.px(ox + x, oy + 1, "qr2" if k < 2 else "qr1")
            L.px(ox + x, oy + 2, "qr1" if k < 4 else "qr0")
            L.px(ox + x, oy + 3, "qr0")
    elif row == "eave":
        for x in range(16):
            L.px(ox + x, oy + 9, "qr2" if x % 4 == 0 else "qr1")
            L.px(ox + x, oy + 10, "qr0")
            L.px(ox + x, oy + 11, "ink")
            L.px(ox + x, oy + 12, "qw0")
            L.px(ox + x, oy + 13, "qw1" if x % 4 else "qw0")
            L.px(ox + x, oy + 14, "qa1")
            L.px(ox + x, oy + 15, "qa2")
        for x in range(0, 16, 4):
            # antefixes: little gilt palmettes along the eave
            L.px(ox + x + 1, oy + 7, "qg2")
            L.px(ox + x, oy + 8, "qg1")
            L.px(ox + x + 1, oy + 8, "qg2")
            L.px(ox + x + 2, oy + 8, "qg1")
    if side == "L":
        for y in range(16 if row != "eave" else 12):
            L.px(ox, oy + y, "ink")
            L.px(ox + 1, oy + y, "qr2" if y % 4 != 3 else "qr1")
    elif side == "R":
        for y in range(16 if row != "eave" else 12):
            L.px(ox + 15, oy + y, "ink")
            L.px(ox + 14, oy + y, "qr0")


def wing_roof():
    s = struct("wing_roof", "A wing's hipped roof, its ridge running back from the stage", 3, 3, SEC_STAGE,
               notes="The paraskenia's roofs: the tiles run east-west down two slopes from a ridge "
                     "running north-south, so the wings stand apart from the skene's long roof. Rows "
                     "`top` `mid` (repeat) `eave`; columns L M R.",
               names={f"{r}_{c}": (i, j) for j, r in enumerate(("top", "mid", "eave"))
                      for i, c in enumerate("LMR")})
    for j, r in enumerate(("top", "mid", "eave")):
        for i, c in enumerate("LMR"):
            ox, oy = i * 16, j * 16
            fill(s.B, ox, oy, lambda x, y: roof_px(y, x if c != "R" else 15 - x))
            if c == "M":
                for y in range(16):
                    s.B.px(ox + 6, oy + y, "ink")
                    s.B.px(ox + 7, oy + y, "qr2")
                    s.B.px(ox + 8, oy + y, "qr2" if y % 4 else "qr1")
                    s.B.px(ox + 9, oy + y, "ink")
            if c == "L":
                for y in range(16):
                    s.B.px(ox, oy + y, "ink")
            if c == "R":
                for y in range(16):
                    s.B.px(ox + 15, oy + y, "ink")
                    s.B.px(ox + 14, oy + y, "qr0")
            if r == "top":
                s.B.hline(ox, ox + 15, oy, "ink")
                s.B.hline(ox, ox + 15, oy + 1, "qr2")
            if r == "eave":
                for x in range(16):
                    s.B.px(ox + x, oy + 9, "qr2" if x % 4 == 0 else "qr1")
                    s.B.px(ox + x, oy + 10, "qr0")
                    s.B.px(ox + x, oy + 11, "ink")
                    s.B.px(ox + x, oy + 12, "qw0")
                    s.B.px(ox + x, oy + 13, "qw1" if x % 4 else "qw0")
                    s.B.px(ox + x, oy + 14, "qa1")
                    s.B.px(ox + x, oy + 15, "qa2")
                for x in range(0, 16, 4):
                    s.B.px(ox + x + 1, oy + 7, "qg2")
                    s.B.px(ox + x, oy + 8, "qg1")
                    s.B.px(ox + x + 1, oy + 8, "qg2")
                    s.B.px(ox + x + 2, oy + 8, "qg1")
    return s


def roof():
    s = struct("roof", "The skene's roof: ridge, tiles and eave", 3, 3, SEC_STAGE,
               notes="Red Laconian tiles. Rows: `ridge`, `tiles` (repeat for a deeper roof, as on "
                     "the wings), `eave` (the gilt antefixes and the shadow on the wall below). "
                     "Columns L M R: repeat M for a wider roof.",
               names={f"{r}_{c}": (i, j) for j, r in enumerate(("ridge", "tiles", "eave"))
                      for i, c in enumerate("LMR")})
    for j, r in enumerate(("ridge", "tiles", "eave")):
        for i, c in enumerate("LMR"):
            roof_cell(s.B, i * 16, j * 16, r, c if c != "M" else None)
    return s


MASK_COMIC = [
    "..oooooo..",
    ".oGGGGGGo.",
    "oGkGGGGkGo",
    "oGooGGooGo",
    "oGGGkkGGGo",
    "ooGGGGGGoo",
    "oGooooooGo",
    ".oGkooKGo.",
    "..oooooo..",
]
MASK_TRAGIC = [
    "..oooooo..",
    ".oGGGGGGo.",
    "oGoGGGGoGo",
    "oGGooooGGo",
    "oGGGkkGGGo",
    "oGGGGGGGGo",
    "oGGooooGGo",
    ".oGoGGoGo.",
    "..oooooo..",
]


def frieze_cell(L, ox, oy, mask):
    """The cornice: a gilt mask on a dark red band, ivy trailing between."""
    def px(x, y):
        if y == 0:
            return "ink"
        if y in (1, 2):
            return "qa3" if y == 1 else "qa2"
        if y == 3:
            return "qa1"
        if y >= 14:
            return ("qa1", "ink")[y - 14]
        return "qd1"
    fill(L, ox, oy, px)
    # an ivy garland swagged along the band
    for x in range(16):
        yy = 5 + int(2.2 * abs(((x + 8) % 16) - 8) / 8)
        if x % 3 != 2:
            L.px(ox + x, oy + 12 - (yy - 5), "qi1" if x % 2 else "qi0")
    put(L, ox + 3, oy + 4, MASK_COMIC if mask == "comic" else MASK_TRAGIC,
        {"o": "ink", "G": "qg2", "k": "qg1", "K": "qd1"})


def frieze():
    s = struct("frieze", "The skene's cornice: comic and tragic masks", 2, 1, SEC_STAGE,
               notes="Gilt masks on the dark red band under the eave, an ivy garland between them. "
                     "Alternate `comic` and `tragic` along the front.",
               names={"comic": (0, 0), "tragic": (1, 0)})
    frieze_cell(s.B, 0, 0, "comic")
    frieze_cell(s.B, 16, 0, "tragic")
    return s


def plaster(x, y, row):
    """The painted front: buff plaster with a dado, a red band and a dark socle."""
    if row == 0:
        if y < 2:
            return "qa1" if y == 1 else "qa2"
        return "qa2" if (x * 7 + y * 3) % 23 else "qa1"
    if y < 9:
        return "qa2" if (x * 7 + y * 3) % 23 else "qa1"
    if y == 9:
        return "qd1"
    if y == 10:
        return "qa1"
    if y >= 14:
        return "ink" if y == 15 else "qw0"
    return "qw1"


def wall_cell(L, ox, oy, row):
    fill(L, ox, oy, lambda x, y: plaster(x, y, row))


def column_cell(L, ox, oy, row):
    """An engaged Ionic half-column against the front."""
    wall_cell(L, ox, oy, row)
    for y in range(16):
        if row == 0 and y < 4:
            # the capital: volutes, gilt
            put(L, ox + 3, oy, ["oooooooooo", "oGgGggGgGo", "goGggggGog", ".oooooooo."],
                {"o": "ink", "G": "qg2", "g": "qg1"})
            break
    y0 = 4 if row == 0 else 0
    y1 = 15 if row == 0 else 12
    for y in range(y0, y1 + 1):
        L.px(ox + 4, oy + y, "ink")
        L.px(ox + 5, oy + y, "qa3")
        L.px(ox + 6, oy + y, "qa3")
        L.px(ox + 7, oy + y, "qa2" if y % 3 else "qa3")
        L.px(ox + 8, oy + y, "qa2")
        L.px(ox + 9, oy + y, "qa2" if y % 3 else "qa1")
        L.px(ox + 10, oy + y, "qa1")
        L.px(ox + 11, oy + y, "ink")
    if row == 1:
        # the base
        put(L, ox + 3, oy + 13, ["oqqqqqqqqo", "oaaaaaaaao", "oooooooooo"],
            {"o": "ink", "q": "qa3", "a": "qa1"})


def pinax_cell(L, ox, oy, row, scene):
    """A painted panel set into the front: a vine on gold, or a goat, framed."""
    wall_cell(L, ox, oy, row)
    y0, y1 = (3, 15) if row == 0 else (0, 8)
    for y in range(y0, y1 + 1):
        for x in range(2, 14):
            edge = x in (2, 13) or (row == 0 and y == 3) or (row == 1 and y == 8)
            L.px(ox + x, oy + y, "qw0" if edge else "qg1")
    if row == 0:
        if scene == "vine":
            put(L, ox + 3, oy + 5, ["..ii..ii..", ".iIIiiIIi.", "..iioiii..", "...oiIo...",
                                    ".ii.oo.ii.", "iIIi..iIIi", ".ii....ii.", "...ooo...."],
                {"i": "qi0", "I": "qi1", "o": "qd1"})
        else:
            put(L, ox + 4, oy + 5, ["o......o", ".o....o.", "..oooo..", ".ooGGoo.",
                                    "..oGGo..", "...oo...", "...oo...", "........"],
                {"o": "ink", "G": "qa3"})
    else:
        if scene == "vine":
            put(L, ox + 4, oy + 1, ["oo.oo.oo", "o..o..o.", ".oo.oo..", "........"],
                {"o": "qd1"})
        else:
            put(L, ox + 5, oy + 0, ["o..o..", "o..o..", "......"], {"o": "ink"})


def facade():
    s = struct("facade", "The skene's front: wall, half-column and painted panels", 4, 2, SEC_STAGE,
               notes="Two rows: the upper wall (`*_0`) and the lower wall on its socle (`*_1`). "
                     "`wall` is plain, `column` an engaged Ionic half-column, `pinax_vine` and "
                     "`pinax_goat` painted panels. Mix them between the three doors.",
               names={f"{k}_{r}": (i, r) for i, k in enumerate(("wall", "column", "pinax_vine", "pinax_goat"))
                      for r in (0, 1)})
    for r in (0, 1):
        wall_cell(s.B, 0, r * 16, r)
        column_cell(s.B, 16, r * 16, r)
        pinax_cell(s.B, 32, r * 16, r, "vine")
        pinax_cell(s.B, 48, r * 16, r, "goat")
    return s


def door_frame(L, ox, oy, w, row):
    """The doorway's frame across w cells: a lintel on the upper row, jambs."""
    for x in range(w * 16):
        for y in range(16):
            L.px(ox + x, oy + y, plaster(x % 16, y, row))
    if row == 0:
        for x in range(1, w * 16 - 1):
            L.px(ox + x, oy + 1, "ink")
            L.px(ox + x, oy + 2, "qa3")
            L.px(ox + x, oy + 3, "qa1")
            L.px(ox + x, oy + 4, "ink")
    for y in range(5 if row == 0 else 0, 16):
        for x, c in ((1, "ink"), (2, "qa3"), (3, "qa2"), (w * 16 - 4, "qa1"), (w * 16 - 3, "qa1"),
                     (w * 16 - 2, "ink")):
            L.px(ox + x, oy + y, c)


def door_leaf(L, ox, oy, w, row, paint, open_):
    """The leaf (or leaves) inside the frame: painted planks, or the dark
    doorway when it stands open."""
    x0, x1 = 4, w * 16 - 5
    y0 = 5 if row == 0 else 0
    for y in range(y0, 16):
        for x in range(x0, x1 + 1):
            if open_:
                c = "ink" if (row == 1 or y > 6) else "qw0"
                if row == 1 and y >= 14:
                    c = "qw0"
            else:
                c = "qw1" if (x - x0) % 4 else "qw0"
                if row == 1 and y == 15:
                    c = "ink"
            L.px(ox + x, oy + y, c)
    if open_:
        return
    if w == 2:
        for y in range(y0, 16):
            L.px(ox + 15, oy + y, "ink")
            L.px(ox + 16, oy + y, "ink")
    legend = {"o": "ink", "G": "qg2", "g": "qg1", "i": "qi0", "I": "qi1", "a": "qa3", "r": "qd1"}
    if paint == "ivy" and row == 0:
        put(L, ox + 4, oy + 6, ["..i.....", ".iIi..i.", "..ii.iIi", "...iIi..", ".i..ii..",
                                "iIi..i..", ".ii.iIi.", "..ii.i.."], legend)
    if paint == "ivy" and row == 1:
        put(L, ox + 4, oy + 0, ["..i..i..", ".iIiiIi.", "..ii.i..", "....i...", "...iIi..",
                                "........", "........", "....G...", "...GoG..", "....G..."], legend)
    if paint == "crown" and row == 0:
        put(L, ox + 7, oy + 6, ["...G....G....G...", "..GgG..GgG..GgG..", "..GgGGGGgGGGGgG..",
                                "..GggggggggggggG.", "..GGGGGGGGGGGGGG.", "..ooooooooooooo.."], legend)
    if paint == "crown" and row == 1:
        put(L, ox + 9, oy + 4, ["G............G", "o............o", "G............G"], legend)
        for x in range(5, 27):
            if x % 5 == 0:
                L.px(ox + x, oy + 10, "qg1")
    if paint == "goat" and row == 0:
        put(L, ox + 4, oy + 6, ["a......a", ".a....a.", "..aaaa..", ".aaoaoa.", "..aaaa..",
                                "...aa...", "...rr...", "....r..."], legend)
    if paint == "goat" and row == 1:
        put(L, ox + 4, oy + 0, ["...aa...", "..a..a..", "........", "........", "........",
                                "........", "........", "....G...", "...GoG..", "....G..."], legend)


def doors():
    out = []
    for key, title, w, paint in (("door_ivy", "The ivy door (stage left: the Comic)", 1, "ivy"),
                                 ("door_crown", "The crown door (center: the palace, the Tragic)", 2, "crown"),
                                 ("door_goat", "The goat door (stage right: the Satyr)", 1, "goat")):
        s = struct(key, title, w * 2, 2, SEC_STAGE, walk=["X" * (w * 2)] * 2,
                   notes="Closed (left) and standing open (right). The play's entrances open a door with "
                         "setmetatile and close it again behind the player: each open cell is its closed "
                         "cell + %d." % w,
                   names={**{f"closed_{r}{c}": (c, r) for r in (0, 1) for c in range(w)},
                          **{f"open_{r}{c}": (w + c, r) for r in (0, 1) for c in range(w)}})
        for r in (0, 1):
            door_frame(s.B, 0, r * 16, w, r)
            door_leaf(s.B, 0, r * 16, w, r, paint, False)
            door_frame(s.B, w * 16, r * 16, w, r)
            door_leaf(s.B, w * 16, r * 16, w, r, paint, True)
        out.append(s)
    return out


def wing_face(door):
    """A paraskenion's south face: two rows of wall under its eave, with the
    skene's back door in the east wing."""
    key = "wing_door" if door else "wing_face"
    s = struct(key, "The east wing's face, with the back door into the skene" if door
               else "A wing's face (the paraskenion)", 3, 2, SEC_STAGE,
               walk=["XXX", "XDX" if door else "XXX"],
               notes="Under the wing's eave row. " + (
                   "The back door is the theater's warp 1, into the skene (MB_NON_ANIMATED_DOOR)."
                   if door else "A painted window between two pilasters."))
    for r in (0, 1):
        for i in range(3):
            wall_cell(s.B, i * 16, r * 16, r)
    for r in (0, 1):
        for ox in (0, 32):
            for y in range(16 if r == 0 else 13):
                x = ox + (2 if ox == 0 else 12)
                s.B.px(x, r * 16 + y, "ink")
                s.B.px(x + 1, r * 16 + y, "qa3")
                s.B.px(x + 2, r * 16 + y, "qa1")
                s.B.px(x + 3, r * 16 + y, "ink")
    if door:
        door_frame(s.B, 16, 0, 1, 0)
        door_frame(s.B, 16, 16, 1, 1)
        for y in range(5, 32):
            for x in range(20, 28):
                s.B.px(x, y, "qw1" if (x - 20) % 3 else "qw0")
        put(s.B, 25, 22, ["G", "o"], {"G": "qg2", "o": "ink"})
    else:
        put(s.B, 19, 4, ["oooooooooo", "oqqqqqqqqo", "oqiIiiIiqo", "oqIiiIiiqo", "oqqqqqqqqo",
                         "oooooooooo"], {"o": "ink", "q": "qa1", "i": "qi0", "I": "qi1"})
    return s


def wings():
    return [wing_face(False), wing_face(True)]


# --------------------------------------------------------------------------
# The stage and its front
# --------------------------------------------------------------------------

def stage():
    s = struct("stage", "The stage floor (logeion)", 2, 2, SEC_STAGE, walk=["..", ".."],
               notes="Planks. `back` is the row against the skene, in its shadow; `front` the row "
                     "along the stage's edge.", names={"back_a": (0, 0), "back_b": (1, 0),
                                                       "front_a": (0, 1), "front_b": (1, 1)})
    fill(s.B, 0, 0, lambda x, y: planks(x, y), x1=31, y1=31)
    for x in range(32):
        s.B.px(x, 0, "ink")
        s.B.px(x, 1, "qw0")
        s.B.px(x, 2, "qw0" if x % 2 else "qw1")
        s.B.px(x, 31, "qw0")
    return s


def proskenion():
    s = struct("proskenion", "The stage's front: columns, painted panels and the steps down",
               5, 1, SEC_STAGE, walk=["XXX.."],
               notes="The low colonnade under the stage's edge, seen from the orchestra. `column` and "
                     "`panel` repeat; `end_L` / `end_R` close it against the parodoi; `steps_L` "
                     "`steps_R` go down from the stage to the orchestra (walkable).",
               names={"column": (0, 0), "panel": (1, 0), "end": (2, 0), "steps_L": (3, 0),
                      "steps_R": (4, 0)})
    # column and panel: the stage's lip, then the front
    for ox, kind in ((0, "column"), (16, "panel"), (32, "end")):
        def px(x, y, kind=kind):
            if y == 0:
                return "ink"
            if y in (1, 2):
                return "qw2" if y == 1 else "qw1"
            if y == 3:
                return "ink"
            if y >= 14:
                return "ink" if y == 15 else "qw0"
            if kind == "panel":
                if x in (0, 15) or y in (4, 13):
                    return "qw0"
                return "qd1" if (x + y) % 9 else "qg1"
            return "qa2"
        fill(s.B, ox, 0, px)
    put(s.B, 4, 4, ["oaqqao..", "oaqqao..", "oaqqao..", "oaqqao..", "oaqqao..", "oaqqao..",
                    "oaqqao..", "oaqqao..", "oaqqao..", "oooooo.."], {"o": "ink", "a": "qa1", "q": "qa3"})
    put(s.B, 32 + 0, 4, ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"], {"o": "ink"})
    # an ivy wreath painted on the panel
    put(s.B, 16 + 4, 6, ["..iiii..", ".i....i.", "i......i", "i......i", ".i....i.", "..iiii.."],
        {"i": "qi1"})
    # the steps down (in the earth palette: stone)
    for ox in (48, 64):
        def st(x, y, ox=ox):
            side = (x if ox == 48 else 15 - x)
            if side == 0:
                return "qp0"
            if side == 1:
                return "qp1"
            k = y % 5
            return "qp3" if k == 0 else ("qp1" if k == 4 else "qp2")
        fill(s.B, ox, 0, st)
    return s


# --------------------------------------------------------------------------
# The parodos, the cut's cap and the terrace gate
# --------------------------------------------------------------------------

def parodos():
    s = struct("parodos", "The parodoi's paving", 2, 2, SEC_STAGE, walk=["..", ".."],
               notes="The side passages' flagstones, laid as the aisle's. Use the cell whose (x % 2, "
                     "y % 2) matches its map cell (`p00` at even x, even y), so the joints run on.",
               names={"p00": (0, 0), "p10": (1, 0), "p01": (0, 1), "p11": (1, 1)})
    for j in (0, 1):
        for i in (0, 1):
            paving(s.B, i * 16, j * 16, i * 16, j * 16)
    return s


def gate():
    """The theater's top gate: a propylon on the cavea's top, the way back to
    Thyrsa's terrace (warp 0). Two limestone piers carry an architrave; the
    player walks under it onto the threshold, an exit mat."""
    s = struct("gate", "The top gate (propylon) to Thyrsa's terrace", 4, 2, SEC_STAGE,
               walk=["XTTX", "XSSX"],
               notes="Rows 32-33, columns 18-21. The architrave is drawn over the player (`lintel_*`); "
                     "the threshold cells are MB_SOUTH_ARROW_WARP: warps 0 and 2, to Thyrsa.",
               names={"pier_top_L": (0, 0), "lintel_L": (1, 0), "lintel_R": (2, 0), "pier_top_R": (3, 0),
                      "pier_L": (0, 1), "door_L": (1, 1), "door_R": (2, 1), "pier_R": (3, 1)})
    B, Tp = s.B, s.T
    # the paving under the architrave and the threshold's pebble mosaic: a kantharos
    for ox in (16, 32):
        def pave(x, y, ox=ox):
            return "qp2" if (x + ox) % 32 and y % 16 else "qp1"
        fill(B, ox, 0, pave)

        def th(x, y, ox=ox):
            gx = x + (ox - 16)
            d = ((gx - 15.5) ** 2 / 110 + (y - 8) ** 2 / 26)
            if d < 1:
                return "qe0" if ((gx + y) % 3 == 0) else "qe1"
            if d < 1.25:
                return "qp1"
            return "qp2" if (gx * 3 + y * 5) % 7 else "qp3"
        fill(B, ox, 16, th)
    # the piers, two rows tall
    for ox in (0, 48):
        def pier(x, y, ox=ox):
            if x in (1, 14):
                return "ink"
            if x == 0 or x == 15:
                return None
            if y >= 30:
                return "ink" if y == 31 else "qp1"
            if y >= 26:
                return "qp3" if y == 26 else "qp2"
            return ("qp3" if x < 5 else "qp2" if x < 11 else "qp1") if (y // 5 + x // 7) % 5 else "qp1"
        for y in range(32):
            for x in range(16):
                c = pier(x, y)
                B.px(ox + x, y, c if c else ("qp2" if (x + y) % 3 else "qp1"))
    # the architrave and its frieze: a dark band with painted ivy (in the top
    # layer over the passage, so the player walks under it)
    for x in range(64):
        for y in range(0, 11):
            c = "ink" if y in (0, 10) else "qp3" if y == 1 else "qp2" if y < 4 else "qe0" if y < 8 else "qp1"
            if y in (5, 6) and x % 6 in (1, 2):
                c = "qe2"
            (Tp if 16 <= x < 48 else B).px(x, y, c)
    for x in (0, 63):
        for y in range(11):
            B.px(x, y, "ink")
    return s


def terrace_wall():
    s = struct("terrace_wall", "The terrace wall either side of the gate, on grass", 2, 1, SEC_PROPS,
               walk=["XX"], on="grass",
               notes="A low limestone wall with ivy swags along the cavea's top. `wall` runs; "
                     "`end` stops it (its east face; flip nothing, it is drawn for the west end and "
                     "the build mirrors nothing, so use it at both ends).",
               names={"wall": (0, 0), "end": (1, 0)})

    def wall(x, y):
        if y < 4:
            return None
        if y == 4:
            return "ink"
        if y == 5:
            return "qm1"
        if y == 15:
            return "ink"
        return "qp2" if (x + (y // 4) * 4) % 8 else "qo1"
    fill(s.M, 0, 0, wall)
    fill(s.M, 16, 0, wall, x1=11)
    for y in range(4, 16):
        s.M.px(16 + 11, y, "ink")
    for x in range(0, 28):
        if x % 3 != 1:
            yy = 7 + int(2 * abs(((x + 4) % 16) - 8) / 8)
            s.M.px(x, yy, "qi1" if x % 2 else "ink")
    return s


# --------------------------------------------------------------------------
# Torches, the thymele, the play's props, the god-machine, the hill
# --------------------------------------------------------------------------

def torch(lit, ground):
    key = f"torch_{'lit' if lit else 'cold'}_{ground}"
    s = struct(key, f"A bronze torch stand, {'lit' if lit else 'cold'}, on "
               f"{'the aisle' if ground == 'pave' else 'grass'}", 1, 2,
               SEC_PROPS, walk=["T", "X"], on="grass" if ground == "grass" else None,
               notes="Two cells: the flame (drawn over the player) and the stand. The lit cell is the "
                     "cold one - 2 in each pair (lit and cold are built in that order).",
               names={"head": (0, 0), "foot": (0, 1)})
    if ground == "pave":
        paving(s.B, 0, 0, 0, 0)
        paving(s.B, 0, 16, 0, 16)
    L = s.T if ground == "pave" else s.M
    F = s.M
    # the bowl and the flame (top cell)
    put(L, 4, 9, ["oooooooo", "obbbbbbo", ".oooooo."], {"o": "ink", "b": "qb1"})
    if lit:
        put(L, 5, 0, ["...f..", "..fF..", ".fFFf.", ".FyyF.", "fFyyFf", ".FFFF.", "..ff.."],
            {"f": "qn", "F": "qf1", "y": "qf2"})
    else:
        put(L, 5, 6, ["......", ".o..o.", "oooooo"], {"o": "ink"})
    # the stand: three bronze legs
    put(F, 5, 16, ["..oo..", "..bo..", "..bo..", "..bo..", "..bo..", ".obbo.", ".o..o.",
                   "o....o", "o....o", "o....o", "oo..oo"], {"o": "ink", "b": "qb1"})
    if ground == "pave":
        pass
    return s


def torches():
    return [torch(True, "pave"), torch(False, "pave")]


def thymele(inky):
    key = "thymele_ink" if inky else "thymele"
    s = struct(key, "The thymele, the god's altar in the orchestra" + (", with the inky handprint"
                                                                      if inky else ""),
               2, 2, SEC_PROPS, walk=["XX", "XX"],
               names={"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)},
               notes="A low round altar of white marble, wreathed in ivy, an offering of grapes "
                     "and a cup on it, on the orchestra's earth. "
                     + ("After the Dionysia: black ink on the altar's lip in the shape of a hand. "
                        "Swap it in over `thymele` (setmetatile, the Theater_ThymeleInk labels)." if inky else
                        "Sits at the orchestra's center, cells (19,12)-(20,13)."))
    for j in (0, 1):
        for i in (0, 1):
            V_px = lambda x, y, i=i, j=j: V.earth_color(304 + i * 16 + x, 192 + j * 16 + y)
            fill(s.B, i * 16, j * 16, V_px)
    M = s.M
    # a square altar: the base step, the front face, the top with its rim
    for x in range(4, 28):
        for y in range(22, 27):
            M.px(x, y, "qp2")
    for x in range(6, 26):
        for y in range(13, 23):
            M.px(x, y, "qm1" if x < 21 else "qp2")
    for x in range(6, 26):
        for y in range(6, 13):
            M.px(x, y, "qm1")
    M.outline("ink")
    for x in range(7, 25):
        M.px(x, 12, "qp2")
        M.px(x, 13, "ink")
    for y in range(7, 12):
        M.px(7, y, "qp2")
        M.px(24, y, "qp2")
    for x in range(5, 27):
        M.px(x, 22, "ink")
    # an ivy garland swagged across the face
    for x in range(7, 25):
        y = 15 + int(round(2.5 * abs(((x - 7) % 9) - 4.5) / 4.5))
        M.px(x, 19 - (y - 15), "qi1" if x % 3 else "ink")
    # the god's fire on the top
    put(M, 12, 2, ["...f....", "..fF.f..", ".fFyFFf.", ".FyyyyF.", "fFyyyyFf", ".ffffff."],
        {"f": "qn", "F": "qf1", "y": "qf2"})
    if inky:
        # four fingers and a thumb, black ink gripping the lip
        put(M, 17, 11, ["o.o.o.o...", "o.o.o.o...", "ooooooo.oo", "ooooooooo.", ".oooooo...",
                        "..oooo...."], {"o": "ink"})
    return s


def loom(fallen):
    key = "loom_fallen" if fallen else "loom"
    s = struct(key, "The Fates' loom, a stage prop" + (", knocked flat" if fallen else ""), 1, 2,
               SEC_PROPS, walk=["T", "X"] if not fallen else [".", "X"],
               notes="On the stage's planks. The comic entrance knocks it over: swap `loom` for "
                     "`loom_fallen` (each cell + 2).", names={"top": (0, 0), "bottom": (0, 1)})
    fill(s.B, 0, 0, lambda x, y: planks(x, y), y1=31)
    if not fallen:
        L = s.T
        # two uprights, a beam, the warp threads weighted at the foot
        for y in range(2, 30):
            s.M.px(2, y, "ink") if y >= 16 else L.px(2, y, "ink")
            s.M.px(3, y, "qo1") if y >= 16 else L.px(3, y, "qo1")
            s.M.px(12, y, "qo1") if y >= 16 else L.px(12, y, "qo1")
            s.M.px(13, y, "ink") if y >= 16 else L.px(13, y, "ink")
        for x in range(1, 15):
            L.px(x, 2, "ink")
            L.px(x, 3, "qo2")
            L.px(x, 4, "qo1")
        for x in range(4, 12):
            for y in range(5, 26):
                c = "qn" if x % 2 else "qm1"
                if y < 12 and x in (5, 6, 9):
                    c = "qi1"
                (s.M if y >= 16 else L).px(x, y, c)
        for x in range(4, 12, 2):
            s.M.px(x, 27, "ink")
            s.M.px(x, 28, "qp2")
    else:
        put(s.M, 0, 18, ["oooooooooooooooo", "oqqqqqqqqqqqqqqo", "onmnmnmnmnmnmnmo",
                         "onmnmnmnmnmnmnmo", "oqqqqqqqqqqqqqqo", "oooooooooooooooo",
                         ".o.o.......o.o..", "o...o.....o...o."],
            {"o": "ink", "q": "qo1", "n": "qn", "m": "qm1"})
    return s


def vine(cut):
    key = "vine_cut" if cut else "vine"
    s = struct(key, "A prop vine on a trellis" + (", its grapes cut" if cut else ""), 1, 2, SEC_PROPS,
               walk=["T", "X"], notes="On the stage. Silenos cuts its grapes with the sickle: swap in "
                                      "`vine_cut` (each cell + 2).", names={"top": (0, 0), "bottom": (0, 1)})
    fill(s.B, 0, 0, lambda x, y: planks(x, y), y1=31)
    L = s.T
    for y in range(3, 30):
        (s.M if y >= 16 else L).px(7, y, "ink")
        (s.M if y >= 16 else L).px(8, y, "qo1")
    for x in range(1, 15):
        L.px(x, 3, "ink")
        L.px(x, 4, "qo1")
    leaves = ["..ii.....ii...", ".iIIi...iIIi..", "iIiIIi.iIiIIi.", ".iIi....iIIi..",
              "..i.....i.....", "..............", "...ii....ii...", "..iIIi..iIIi..",
              "...ii....ii..."]
    put(L, 1, 5, leaves, {"i": "ink", "I": "qi1"})
    if not cut:
        put(L, 2, 9, ["oo....oo", "ono..ono", ".o....o."], {"o": "ink", "n": "qn"})
        put(s.M, 5, 17, ["oo..oo", "on.ono", ".o..o."], {"o": "ink", "n": "qn"})
    return s


def crane():
    """The god-machine: a wooden crane on the skene's roof, its arm out over the
    stage and a hook on a rope."""
    s = struct("crane", "The god-machine (mechane) on the skene's roof", 3, 3, SEC_PROPS,
               walk=["XXX", "XXX", "XXX"],
               notes="Drawn over the roof's cells: its bottom layer is the roof (`roof` M cells) and the "
                     "crane lies on it. Put it on the main roof, its arm reaching down over the cornice.")
    for j in range(3):
        for i in range(3):
            roof_cell(s.B, i * 16, j * 16, ("ridge", "tiles", "eave")[j], None)
    M = s.M
    # the counterweight: a stone block on the roof, lashed down
    put(M, 0, 18, ["oooooooo", "oqqqqqqo", "oqppppqo", "oqppppqo", "oooooooo"],
        {"o": "ink", "q": "qm1", "p": "qp2"})
    # the mast: a squared timber with a block at its head
    for y in range(2, 34):
        for x, c in ((7, "ink"), (8, "qo2"), (9, "qo2"), (10, "qo1"), (11, "ink")):
            M.px(x, y, c)
    put(M, 5, 0, ["ooooooooo", "oqqqqqqqo", "ooooooooo"], {"o": "ink", "q": "qo1"})
    # the arm: two beams out over the stage, falling to the hook
    for t in range(0, 34):
        x, y = 10 + t, 3 + (t * 2) // 5
        for k, c in enumerate(("ink", "qo2", "qo1", "ink")):
            M.px(x, y + k, c)
    # a stay from the mast's head back to the counterweight
    M.line(8, 2, 2, 18, "qo1")
    # the rope and the hook at the arm's end
    for y in range(18, 42):
        M.px(42, y, "qo2" if y % 2 else "qo1")
        M.px(43, y, "ink")
    put(M, 39, 41, [".obbo.", "ob..bo", "....bo", ".obbo."], {"o": "ink", "b": "qb1"})
    # the winch at the mast's foot
    put(M, 11, 26, ["oooooo", "obqqbo", "obqqbo", "oooooo"], {"o": "ink", "b": "qb1", "q": "qo1"})
    return s


def rocks():
    s = struct("rock", "Grey crag of the theater hill, on grass", 2, 2, SEC_PROPS, walk=["XX", "XX"],
               on="grass", notes="A crag showing through the hill's grass, beside the skene and the "
                                 "parodoi. It sits on aethos grass.")
    M = s.M
    M.ellipse(2, 6, 29, 29, "qp2")
    M.ellipse(4, 4, 22, 20, "qm1")
    M.ellipse(16, 12, 28, 27, "qp2")
    M.outline("ink")
    for y in range(8, 28, 5):
        M.line(8, y, 14, y + 3, "ink")
    for x, y in ((6, 8), (20, 18), (12, 22)):
        M.px(x, y, "qi1")
        M.px(x + 1, y, "qi1")
    return s


def build():
    return [roof(), wing_roof(), frieze(), facade()] + doors() + wings() + \
        [stage(), proskenion(), parodos(), gate()]


def build_props():
    return torches() + [thymele(False), thymele(True), loom(False), loom(True), vine(False),
                        vine(True), crane(), terrace_wall()]
