"""gTileset_Skene: inside Thyrsa's stage building (MAP_THYRSA_THEATER_SKENE), on
the oikos primary.

Two parts, per design/phase3/SCRIPT.md Part 2:
  - backstage, a corridor behind the three stage doors (their backs, chalked for
    the actors), with the mask racks (empty pegs; the comic and tragic masks
    for the Dionysia, and the satyr mask Thespis brings; full of Prosomime
    after), costume rails and a water barrel;
  - the prop room through an arch, Silenos's kingdom: costume chests, a lion
    skin with the head on, a painted wooden sickle, a gold mask with closed
    eyes, a crown of stars on cork, the god-machine's winch with its rope and
    hook (and Daedalus's page pinned to it), the wine jar that is never empty,
    and the great girdle on its peg.
The walls are timber-framed ochre plaster and the floor is planking, like the
stage outside. Self-contained: its own tiles and palettes 6-12; the wall tops
and the exit mat come from oikos.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
import theater_lib  # noqa: E402,F401  (registers the shared colors)
from eleusa_lib import put  # noqa: E402
from theater_lib import Struct  # noqa: E402

NEW = {
    "kw0": (64, 40, 24), "kw1": (112, 72, 40), "kw2": (160, 112, 64), "kw3": (200, 160, 104),
    "kp1": (176, 136, 88), "kp2": (216, 184, 128), "kp3": (240, 216, 168), "kc": (232, 232, 224),
    "kx": (96, 96, 104), "kd": (40, 32, 32),
    "km1": (248, 240, 224), "km2": (200, 192, 176), "kg1": (192, 144, 40), "kg2": (248, 208, 88),
    "kr": (176, 48, 40), "kv": (136, 72, 152), "ky": (224, 168, 48), "kb": (64, 96, 160),
    "kgn": (88, 128, 64),
    "kl0": (96, 56, 24), "kl1": (168, 112, 56), "kl2": (216, 168, 96), "kl3": (240, 208, 144),
    "kt0": (120, 48, 24), "kt1": (184, 88, 48), "kt2": (224, 136, 88), "kk": (184, 152, 104),
    "kq1": (176, 144, 96), "kq2": (224, 200, 152),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GROUPS = {
    "wood": ["ink", "kw0", "kw1", "kw2", "kw3", "kp1", "kp2", "kp3", "kc", "kx", "kd"],
    "masks": ["ink", "km1", "km2", "kg1", "kg2", "kr", "kv", "kw1", "kw2", "kp1", "kp2", "kt1", "kd"],
    "cloth": ["ink", "kw0", "kw1", "kw2", "kw3", "kr", "ky", "kb", "kgn", "km1", "kv", "kp2"],
    "props": ["ink", "kl0", "kl1", "kl2", "kl3", "kw1", "kw2", "kw3", "kg1", "kg2", "kt0", "kt1",
              "kt2", "kk"],
    "rope": ["ink", "kw0", "kw1", "kw2", "kw3", "kq1", "kq2", "kx", "kd", "kp3", "kp2", "kc"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g

SECTION_ROWS = {"room": 0, "backstage": 12, "props": 30}

OIKOS_EXIT = 0x006


def struct(key, title, w, h, section, walk=None, notes="", names=None):
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names)
    return s


def fill(L, ox, oy, fn, x0=0, y0=0, x1=15, y1=15):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = fn(x, y)
            if c:
                L.px(ox + x, oy + y, c)


# --------------------------------------------------------------------------
# Floor and walls
# --------------------------------------------------------------------------

def plank(x, y, shade=False):
    """Stage planking, boards running east-west, as on the stage outside."""
    yy = y % 8
    if yy == 7:
        return "kw0"
    if yy == 0:
        return "kw2" if not shade else "kw1"
    if (x + (y // 8) * 5) % 16 == 0:
        return "kw0"
    if shade:
        return "kw1"
    return "kw2" if (x * 3 + y) % 11 else "kw3"


def wall_px(x, y, row):
    """Ochre plaster in a timber frame: row 0 carries the beam, row 1 the skirting."""
    if row == 0:
        if y == 0:
            return "ink"
        if y in (1, 2, 3):
            return ("kw2", "kw1", "kw0")[y - 1]
        return "kp2" if (x * 5 + y * 3) % 19 else "kp1"
    if y >= 12:
        return ("kw1", "kw2", "kw0", "ink")[y - 12]
    return "kp2" if (x * 5 + y * 3) % 19 else "kp1"


def room():
    out = []
    v = struct("void", "The dark above the walls", 1, 1, "room", walk=["X"],
               notes="Wall tops and the space outside the rooms, and the map's border.")
    v.B.rect(0, 0, 16, 16, "kd")
    out.append(v)
    s = struct("floor", "Planking", 2, 2, "room", walk=["..", ".."],
               notes="`a` `b` alternate along a row; `shade_*` is the row under a wall.",
               names={"a": (0, 0), "b": (1, 0), "shade_a": (0, 1), "shade_b": (1, 1)})
    fill(s.B, 0, 0, plank, x1=31)
    fill(s.B, 0, 16, lambda x, y: plank(x, y, y < 4), x1=31)
    for x in range(32):
        s.B.px(x, 16, "ink")
        s.B.px(x, 17, "kw0")
    out.append(s)
    s = struct("wall", "Timber-framed plaster wall", 3, 2, "room",
               notes="Row 0 under the beam, row 1 on the skirting. `post` is a timber upright for "
                     "corners and between panels.",
               names={"upper": (0, 0), "lower": (0, 1), "post_upper": (1, 0), "post_lower": (1, 1),
                      "lamp_upper": (2, 0), "lamp_lower": (2, 1)})
    for r in (0, 1):
        for i in range(3):
            fill(s.B, i * 16, r * 16, lambda x, y, r=r: wall_px(x, y, r))
        for y in range(16 if r == 0 else 12):
            for x, c in ((5, "ink"), (6, "kw2"), (7, "kw2"), (8, "kw1"), (9, "kw1"), (10, "ink")):
                s.B.px(16 + x, r * 16 + y, c)
    # a clay lamp on a bracket
    put(s.B, 32 + 5, 6, ["..kc..", ".kccx.", "kwwwwk", ".kwwk.", "..kk.."],
        {"k": "ink", "c": "kp3", "w": "kw1", "x": "kx"})
    out.append(s)
    # the dividing wall's openings: an arch to the prop room, a doorway to the back door
    s = struct("openings", "An arch and a doorway in the inner wall", 4, 2, "room",
               walk=["TTTT", "...."],
               notes="`arch_*`: the prop room's arch, its top drawn over the player. `door_*`: a "
                     "plain doorway, its lintel over the player.",
               names={"arch_L0": (0, 0), "arch_R0": (1, 0), "arch_L1": (0, 1), "arch_R1": (1, 1),
                      "door_L0": (2, 0), "door_R0": (3, 0), "door_L1": (2, 1), "door_R1": (3, 1)})
    for i in range(4):
        fill(s.B, i * 16, 16, lambda x, y: plank(x, y, y < 6))
        fill(s.B, i * 16, 0, lambda x, y: plank(x, y, True))
    # arch: a round-headed opening, the jambs and the head over the player
    for x in range(32):
        for y in range(16):
            dx = abs(x - 15.5)
            inside = y >= 4 + int(max(0, 8 - (196 - dx * dx) ** 0.5)) if dx < 14 else False
            if not inside:
                s.T.px(x, y, wall_px(x, y, 0))
    for x in range(32):
        for y in range(16):
            dx = abs(x - 15.5)
            edge = dx < 14 and abs(y - (4 + max(0, 8 - (196 - dx * dx) ** 0.5))) < 1.2
            if edge or (dx >= 13.5 and dx < 15):
                s.T.px(x, y, "ink" if dx >= 14 or edge else "kw2")
    for x in (0, 1, 30, 31):
        for y in range(16, 26):
            s.M.px(x, y, "kw1" if x in (1, 30) else "ink")
    # doorway: a squared opening
    for x in range(32, 64):
        for y in range(16):
            if y < 5 or x < 35 or x > 60:
                s.T.px(x, y, wall_px(x, y, 0))
        s.T.px(x, 5, "ink")
        s.T.px(x, 4, "kw0")
    for y in range(4, 16):
        s.T.px(34, y, "ink")
        s.T.px(61, y, "ink")
    out.append(s)
    return out


# --------------------------------------------------------------------------
# Backstage: door backs, racks, rails, barrel
# --------------------------------------------------------------------------

def door_back(key, title, w, mark):
    s = struct(key, title, w * 2, 2, "backstage", walk=["X" * w * 2, "X" * w * 2],
               notes="The back of a stage door, chalked for the actors. Left: shut. Right: standing "
                     "open, the stage's torchlight in the gap (each open cell is its shut cell + %d)." % w,
               names={**{f"shut_{r}{c}": (c, r) for r in (0, 1) for c in range(w)},
                      **{f"open_{r}{c}": (w + c, r) for r in (0, 1) for c in range(w)}})
    for half, open_ in ((0, False), (1, True)):
        ox = half * w * 16
        for r in (0, 1):
            for c in range(w):
                fill(s.B, ox + c * 16, r * 16, lambda x, y, r=r: wall_px(x, y, r))
        x0, x1 = ox + 3, ox + w * 16 - 4
        for y in range(5, 32):
            s.B.px(x0 - 1, y, "ink")
            s.B.px(x1 + 1, y, "ink")
            for x in range(x0, x1 + 1):
                if open_:
                    c = "kd" if y < 28 else "kw0"
                    if 8 < y < 26 and (x - x0) in (2, 3):
                        c = "kp3"     # a sliver of torchlight from the stage
                else:
                    c = "kw2" if (x - x0) % 4 else "kw1"
                    if y in (9, 22):
                        c = "kw0"
                s.B.px(x, y, c)
        for x in range(x0 - 1, x1 + 2):
            s.B.px(x, 4, "ink")
            s.B.px(x, 3, "kw0")
        if not open_:
            # the actors' chalk marks: what goes through this door
            legend = {"c": "kc"}
            if mark == "ivy":
                put(s.B, x0 + 2, 12, ["c...c", ".c.c.", "..c..", ".c.c.", "c...c", "..c..", "..c.."], legend)
            elif mark == "crown":
                put(s.B, x0 + 9, 11, ["c.c.c.c", "ccccccc", "c.....c", "ccccccc"], legend)
            else:
                put(s.B, x0 + 2, 11, ["c...c", ".ccc.", "c.c.c", ".ccc.", "..c..", ".c.c."], legend)
            s.B.px(x1 - 2, 20, "kx")
            s.B.px(x1 - 2, 21, "kx")
    return s


MASK = {
    "comic": ["..oooo..", ".oWWWWo.", "oWkWWkWo", "oWWWWWWo", "oWkWWkWo", ".oWkkWo.", "..oooo.."],
    "tragic": ["..oooo..", ".oWWWWo.", "oWkWWkWo", "oWWWWWWo", "oWWkkWWo", ".okWWko.", "..oooo.."],
    "satyr": ["o.oooo.o", "oWoWWoWo", ".oWkkWo.", ".oWWWWo.", ".oWrrWo.", "..oWWo..", "...oo..."],
    "prosomime": ["..oooo..", ".oPPPPo.", "oPkPPkPo", "oPPPPPPo", "oPkPPkPo", ".oPkkPo.", "..oooo.."],
}


def rack(key, title, masks):
    """A mask rack on the wall: a board with pegs, and what hangs on them."""
    s = struct(key, title, 2, 2, "backstage",
               notes="On the north wall, two cells wide. Interact to take a mask.")
    for r in (0, 1):
        for c in (0, 1):
            fill(s.B, c * 16, r * 16, lambda x, y, r=r: wall_px(x, y, r))
    # the board
    for x in range(2, 30):
        for y in (6, 7):
            s.M.px(x, y, "kw2" if y == 6 else "kw1")
        s.M.px(x, 5, "ink")
        s.M.px(x, 8, "ink")
    pegs = [5, 12, 19, 26]
    for px in pegs:
        put(s.M, px - 1, 9, ["oo", "kw", "oo"], {"o": "ink", "k": "kw1", "w": "kw2"})
    legend = {"o": "ink", "W": "km1", "k": "kd", "r": "kr", "P": "kv"}
    for px, m in zip(pegs, masks):
        if m:
            put(s.M, px - 4, 11, MASK[m], legend)
    if any(m == "prosomime" for m in masks):
        # a second row of Prosomime under the first, they are so many
        for px in pegs:
            put(s.M, px - 4, 20, MASK["prosomime"], legend)
    return s


def racks():
    return [rack("rack_empty", "The mask rack, its pegs empty (before the Dionysia)", [None] * 4),
            rack("rack_two", "The rack: the comic and the tragic mask", ["comic", "tragic", None, None]),
            rack("rack_three", "The rack: comic, tragic, and the satyr mask Thespis hangs there",
                 ["comic", "tragic", "satyr", None]),
            rack("rack_full", "The rack after the Dionysia: Prosomime on every peg", ["prosomime"] * 4)]


def rail():
    s = struct("rail", "A costume rail: robes for kings, Fates and satyrs", 2, 2, "backstage",
               walk=["TT", "XX"], notes="Free-standing in the corridor, its top over the player.")
    fill(s.B, 0, 0, plank, x1=31, y1=31)
    L = s.T
    for x in range(1, 31):
        L.px(x, 2, "ink")
        L.px(x, 3, "kw2")
        L.px(x, 4, "ink")
    for x in (2, 29):
        for y in range(2, 31):
            (s.M if y >= 16 else L).px(x, y, "kw1")
            (s.M if y >= 16 else L).px(x + 1, y, "ink")
    robes = [("kr", 4), ("ky", 9), ("kb", 14), ("kv", 19), ("kgn", 24)]
    for col, x0 in robes:
        for y in range(5, 26):
            w = 4 + (y - 5) // 6
            for x in range(x0 - w // 2, x0 + w // 2 + 1):
                c = col if (x + y) % 5 else "ink"
                (s.M if y >= 16 else L).px(x, y, c)
    return s


def split_tall(s, L):
    """Move a drawn object's upper cell into the top layer (over the player)
    and its lower cell into the middle layer, so no cell has three layers."""
    s.T.a[0:16] = L.a[0:16]
    s.M.a[16:32] = L.a[16:32]


def barrel():
    s = struct("barrel", "A water barrel and a dipper", 1, 2, "backstage", walk=["T", "X"],
               notes="Backstage, for the chorus's throats.")
    fill(s.B, 0, 0, plank, y1=31)
    M = A.Layer(16, 32)
    M.ellipse(1, 10, 14, 30, "kw2")
    for y in (14, 21, 27):
        M.hline(1, 14, y, "kx")
    M.outline("ink")
    M.ellipse(2, 6, 13, 13, "kw1")
    M.ellipse(4, 8, 11, 11, "kd")
    M.line(9, 2, 6, 9, "kw2")
    split_tall(s, M)
    return s


def backstage():
    return [door_back("door_back_ivy", "The ivy door, from behind", 1, "ivy"),
            door_back("door_back_crown", "The palace door, from behind", 2, "crown"),
            door_back("door_back_goat", "The goat door, from behind", 1, "goat")] + racks() + \
        [rail(), barrel()]


# --------------------------------------------------------------------------
# The prop room
# --------------------------------------------------------------------------

def on_wall(key, title, art, notes=""):
    s = struct(key, title, 1, 2, "props", notes=notes or "On a wall: upper and lower cells.")
    for r in (0, 1):
        fill(s.B, 0, r * 16, lambda x, y, r=r: wall_px(x, y, r))
    art(s.M)
    return s


def chests():
    out = []
    for i, (body, band) in enumerate((("kl1", "kg1"), ("kt1", "kg2"))):
        s = struct(f"chest_{i}", "A costume chest", 1, 1, "props", walk=["X"],
                   notes="Silenos sits on one; the other is full of beards.")
        fill(s.B, 0, 0, plank)
        M = s.M
        for x in range(1, 15):
            for y in range(3, 15):
                M.px(x, y, body if y > 6 else "kl2")
        M.outline("ink")
        M.hline(2, 13, 7, "ink")
        M.hline(2, 13, 10, band)
        put(M, 6, 8, ["oo", "oo"], {"o": "kg2"})
        out.append(s)
    return out


def lion_skin():
    s = struct("lion_skin", "A lion skin with the head still on (Herakles's, a costume, mostly)", 2, 1,
               "props", walk=["XX"], notes="Spread on the floor. The mouth is the eyehole.")
    fill(s.B, 0, 0, plank, x1=31)
    M = s.M
    M.ellipse(8, 3, 30, 14, "kl2")
    M.ellipse(1, 2, 12, 13, "kl1")
    for (x, y) in ((10, 2), (10, 13), (27, 2), (27, 13)):
        M.ellipse(x - 2, y - 2, x + 2, y + 1, "kl1")
    M.outline("ink")
    put(M, 2, 4, ["kkkk.", "kokok", "kkkkk", ".kKKk", "..kk."], {"k": "kl0", "o": "ink", "K": "kl3"})
    for x in range(12, 28, 3):
        M.px(x, 8, "kl1")
    return s


def winch(page):
    key = "winch_page" if page else "winch"
    s = struct(key, "The god-machine's winch on the wall, its rope up through a hatch"
               + (", Daedalus's page pinned to the hook" if page else ""), 2, 2, "props",
               walk=["XX", "XX"],
               notes="Mounted on the prop room's wall: the crane on the roof is worked from here, the "
                     "rope running up through a hatch in the beam. Silenos unpins the page (swap in "
                     "`winch` with the Skene_Winch labels).",
               names={"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)})
    for r in (0, 1):
        for c in (0, 1):
            fill(s.B, c * 16, r * 16, lambda x, y, r=r: wall_px(x, y, r))
    M = s.M
    # the hatch in the beam
    for x in range(18, 28):
        M.px(x, 1, "ink")
        M.px(x, 2, "kd")
        M.px(x, 3, "kd")
    # the frame and the drum, wound with rope
    for x in (2, 13):
        for y in range(10, 29):
            M.px(x, y, "ink")
            M.px(x + 1, y, "kw2")
    M.ellipse(3, 14, 14, 24, "kq1")
    for y in range(15, 24, 2):
        M.hline(4, 13, y, "kq2")
    M.hline(1, 16, 28, "ink")
    M.hline(1, 16, 27, "kw1")
    put(M, 14, 17, ["oooooo", "owwwwo", "oooooo"], {"o": "ink", "w": "kw1"})
    # the rope, up to the hatch, and the hook hanging
    M.line(13, 15, 23, 3, "kq1")
    M.line(14, 15, 24, 3, "kq2")
    for y in range(4, 20):
        M.px(24, y, "kq2" if y % 2 else "kq1")
    put(M, 21, 19, [".oxxo.", "ox..xo", "....xo", ".oxxo."], {"o": "ink", "x": "kx"})
    if page:
        put(M, 25, 8, ["oooooo", "oppppo", "opcpco", "oppppo", "opcppo", "oooooo"],
            {"o": "ink", "p": "kp3", "c": "kw0"})
    return s


def wine_jar():
    s = struct("wine_jar", "The wine jar that is never empty", 1, 2, "props", walk=["T", "X"],
               notes="A big black-figure jar: satyrs dancing round it.")
    fill(s.B, 0, 0, plank, y1=31)
    M = A.Layer(16, 32)
    M.ellipse(1, 9, 14, 30, "kt1")
    M.ellipse(4, 3, 11, 10, "kt2")
    M.outline("ink")
    M.ellipse(5, 4, 10, 8, "kt0")
    for x in range(3, 13):
        for y in range(16, 22):
            if (x + y) % 3 == 0:
                M.px(x, y, "ink")
    M.hline(2, 13, 14, "kt0")
    M.hline(2, 13, 24, "kt0")
    split_tall(s, M)
    return s


def props():
    def girdle(L, empty=False):
        put(L, 6, 3, ["oo", "ow", "oo"], {"o": "ink", "w": "kw1"})
        if empty:
            return
        for y in range(6, 28):
            for x in range(4, 12):
                L.px(x, y, "kl0" if x in (4, 11) else "kl1")
        for y in range(8, 27, 4):
            L.px(7, y, "kg2")
            L.px(8, y, "kg1")
        put(L, 4, 26, ["oooooooo", "okgggkgo", "oooooooo"], {"o": "ink", "k": "kl0", "g": "kg2"})

    def sickle(L):
        put(L, 3, 4, ["...oooo..", "..oGGGGo.", ".oGo..oGo", "oGo....o.", "oGo......", ".oGo.....",
                      "..oWo....", "...oWo...", "....oWo..", ".....oWo.", "......oo."],
            {"o": "ink", "G": "kg1", "W": "kw2"})

    def gold_mask(L):
        put(L, 2, 18, ["oooooooooooo", "okkkkkkkkkko", "oooooooooooo"], {"o": "ink", "k": "kw2"})
        put(L, 3, 8, ["..oooooo..", ".oGGGGGGo.", "oGGGGGGGGo", "oGooGGooGo", "oGGGGGGGGo",
                      "oGGGggGGGo", ".oGGGGGGo.", "..oooooo.."], {"o": "ink", "G": "kg2", "g": "kg1"})

    def crown(L):
        put(L, 2, 18, ["oooooooooooo", "okkkkkkkkkko", "oooooooooooo"], {"o": "ink", "k": "kw2"})
        put(L, 2, 10, [".g...g...g..", "gGg.gGg.gGg.", ".g...g...g..", "oKKKKKKKKKo.",
                       "oKkKkKkKkKo.", "ooooooooooo."], {"o": "ink", "g": "kg1", "G": "kg2", "K": "kk", "k": "kl2"})

    out = [on_wall("girdle", "The great leather girdle on its peg, studded with bronze",
                   lambda L: girdle(L), "Behind Silenos's chest. Swap in `girdle_empty` once it's won."),
           on_wall("girdle_empty", "The girdle's empty peg", lambda L: girdle(L, True)),
           on_wall("sickle", "A painted wooden sickle", sickle),
           on_wall("gold_mask", "A gold mask with its eyes shut, on a shelf", gold_mask),
           on_wall("crown_stars", "A crown of stars on cork, on a shelf", crown)]
    return out + chests() + [lion_skin(), winch(True), winch(False), wine_jar()]


def sections():
    return [("room", room()), ("backstage", backstage()), ("props", props())]


LABELS = {
    "door_back_ivy": [("shut_10", "Skene_DoorIvy"), ("open_10", "Skene_DoorIvyOpen"),
                      ("shut_00", "Skene_DoorIvy_Top"), ("open_00", "Skene_DoorIvyOpen_Top")],
    "door_back_crown": [("shut_10", "Skene_DoorCrownL"), ("shut_11", "Skene_DoorCrownR"),
                        ("open_10", "Skene_DoorCrownOpenL"), ("open_11", "Skene_DoorCrownOpenR"),
                        ("shut_00", "Skene_DoorCrown_TopL"), ("shut_01", "Skene_DoorCrown_TopR"),
                        ("open_00", "Skene_DoorCrownOpen_TopL"), ("open_01", "Skene_DoorCrownOpen_TopR")],
    "door_back_goat": [("shut_10", "Skene_DoorGoat"), ("open_10", "Skene_DoorGoatOpen"),
                       ("shut_00", "Skene_DoorGoat_Top"), ("open_00", "Skene_DoorGoatOpen_Top")],
    "winch_page": [("tl", "Skene_WinchPage_TL"), ("tr", "Skene_WinchPage_TR"),
                   ("bl", "Skene_WinchPage_BL"), ("br", "Skene_WinchPage_BR")],
    "winch": [("tl", "Skene_Winch_TL"), ("tr", "Skene_Winch_TR"),
              ("bl", "Skene_Winch_BL"), ("br", "Skene_Winch_BR")],
}
for _k in ("rack_empty", "rack_two", "rack_three", "rack_full"):
    _lab = "Skene_" + "".join(p.capitalize() for p in _k.split("_"))
    LABELS[_k] = [(f"c{c}{r}", f"{_lab}_{('T', 'B')[r]}{('L', 'R')[c]}") for r in (0, 1) for c in (0, 1)]
LABELS["girdle"] = [("upper", "Skene_Girdle_Upper"), ("lower", "Skene_Girdle_Lower")]
LABELS["girdle_empty"] = [("upper", "Skene_GirdleEmpty_Upper"), ("lower", "Skene_GirdleEmpty_Lower")]


def _add_names(structs):
    for s in structs:
        if s.key.startswith("rack_"):
            s.names = {f"c{c}{r}": (c, r) for r in (0, 1) for c in (0, 1)}
        if s.key in ("girdle", "girdle_empty"):
            s.names = {"upper": (0, 0), "lower": (0, 1)}
    return structs


_orig_sections = sections


def sections():  # noqa: F811
    secs = _orig_sections()
    for _, ss in secs:
        _add_names(ss)
    return secs
