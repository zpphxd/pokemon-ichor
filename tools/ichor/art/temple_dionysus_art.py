"""The Temple of Dionysus's interior: gTileset_TempleDionysus, the god's own stage at
Thyrsa, where Hierophant Thespis keeps the Three-Act Play (SYSTEMS.md §12: masks and
roles; design/phase3/SCRIPT.md Part 5).

The temple is a theater turned inside out: a long hall running north from the door,
three stage sets one behind another, each grander than the last. Every act is one
room in two halves. The south half is the wings: worn backstage boards, the back of
the set (the skene) with its three doors, the mask rack on its pegs, the program on a
reading stand, trunks and costume rails. The north half is the stage, and beyond it
the audience: tiers of clay votive figures with their mouths open.

  Act I    a rough set: timber and canvas, the crown and goat doors only painted on
  Act II   a painted palace front: red panels, blue and ochre bands
  Act III  a marble skene with gilded capitals; above it, the god-machine's crane on
           the skene roof, where Thespis waits

The entry is the god's orchestra: a round dancing floor with the great altar of
Dionysus at its heart, a black-figure frieze of the god's revel, bronze torches.

How the puzzle's state shows in tiles:

  Masks    The rack is a row of pegs, one cell per mask. Each peg has a full and an
           empty metatile: the empty one = the full one + 1. The peg of the mask the
           player wears is shown empty.
  Doors    A real door is three cells: the gap in the skene's cap, the door's upper
           cell (its sign: an ivy wreath, a crown, goat horns) and the doorway, which
           is walkable (a coord event on it is the entrance). Act I's crown and goat
           doors are only painted on the canvas: two blocking cells.
  Curtains The curtained stair at a stage's end: `foot_closed` blocks, and
           `foot_open` = `foot_closed` + 2 (both halves move together).
  Machine  The god-machine's arm, raised or lowered: every lowered cell is its
           raised cell + 1 (mast, deck, deck front, both tiers, the hook on stage).

Everything sits in the bottom (opaque) and middle layers, except the crane's beam
over the deck, drawn in the top layer above the player. Light falls from the top left.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import Layer, Struct  # noqa: E402,F401
from eleusa_lib import put  # noqa: E402

# --------------------------------------------------------------------------
# Colors and palette groups (every value a multiple of 8)
# --------------------------------------------------------------------------

NEW = {
    "yk": (24, 16, 24),
    # wood: backstage boards, the stage, timber, stairs, the deck and the crane
    "yw0": (48, 32, 24), "yw1": (88, 56, 40), "yw2": (128, 80, 48), "yw3": (168, 112, 64),
    "yw4": (208, 152, 96), "yw5": (240, 200, 136), "yrp": (200, 176, 128), "yir": (88, 88, 96),
    # the temple's wine-dark plaster, ivy, grapes, gold, cream
    "yp0": (48, 16, 40), "yp1": (80, 32, 56), "yp2": (112, 48, 72), "yp3": (144, 72, 96),
    "yp4": (184, 112, 128),
    "yv0": (32, 64, 40), "yv1": (64, 112, 48), "yv2": (128, 168, 72),
    "yg0": (80, 40, 112), "yg1": (136, 88, 176),
    "yo0": (168, 112, 40), "yo1": (232, 184, 72), "ycr": (240, 224, 184),
    # clay: the votive audience, kraters and pots
    "yt0": (96, 40, 24), "yt1": (152, 72, 40), "yt2": (200, 112, 64), "yt3": (232, 160, 104),
    "yrd": (176, 48, 32), "ywh": (232, 224, 200),
    # masks and cloth
    "ym0": (248, 240, 224), "ym1": (216, 200, 176), "ym2": (160, 136, 120),
    "ya0": (112, 64, 32), "ya1": (176, 120, 72),
    "yc0": (64, 16, 32), "yc1": (112, 24, 48), "yc2": (168, 48, 64), "yc3": (216, 104, 104),
    # paint: canvas, red, blue, ochre (Act I's canvas, Act II's palace front)
    "yn0": (192, 168, 128), "yn1": (224, 208, 168),
    "yr0": (128, 32, 32), "yr1": (192, 72, 48),
    "yb0": (32, 56, 104), "yb1": (72, 112, 176),
    "yy0": (184, 136, 48), "yy1": (232, 200, 104),
    # marble and stone: Act III's skene, the tiers, the orchestra, the altar
    "yq0": (104, 88, 80), "yq1": (152, 136, 120), "yq2": (192, 176, 152), "yq3": (224, 208, 184),
    "yq4": (248, 240, 224),
    # bronze and fire
    "yz0": (72, 40, 24), "yz1": (128, 80, 40), "yz2": (184, 128, 56), "yz3": (232, 184, 104),
    "yf0": (184, 48, 16), "yf1": (232, 112, 24), "yf2": (248, 184, 56), "yf3": (248, 240, 168),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME[_c] = _n
C = A.C

GROUPS = {
    "wood": ["yk", "yw0", "yw1", "yw2", "yw3", "yw4", "yw5", "yrp", "yir", "yo0", "yo1",
             "yv1", "yv2", "yc1", "yc2"],
    "wall": ["yk", "yp0", "yp1", "yp2", "yp3", "yp4", "yv0", "yv1", "yv2", "yg0", "yg1",
             "yo0", "yo1", "ycr"],
    "clay": ["yk", "yt0", "yt1", "yt2", "yt3", "yrd", "ywh", "yv1", "yv2", "yo1", "yw1",
             "yw2", "yw3", "yrp", "yir"],
    "mask": ["yk", "ym0", "ym1", "ym2", "ya0", "ya1", "yc0", "yc1", "yc2", "yc3", "yo0",
             "yo1", "yw1", "yw2", "yw3"],
    "paint": ["yk", "yn0", "yn1", "yr0", "yr1", "yb0", "yb1", "yy0", "yy1", "ywh", "yv1",
              "yv2", "yw1", "yw2", "yw3"],
    "marble": ["yk", "yq0", "yq1", "yq2", "yq3", "yq4", "yo0", "yo1", "yv0", "yv1", "yv2",
               "yc1", "yc2", "yp1", "yp2"],
    "fire": ["yk", "yz0", "yz1", "yz2", "yz3", "yf0", "yf1", "yf2", "yf3", "yt1", "yt2",
             "yv1", "yv2", "yw1", "yw2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

SEC = "temple_dionysus"


def struct(key, title, w, h, walk=None, notes="", names=None, behaviors=None):
    s = Struct(key, title, w, h, SEC, walk=walk, notes=notes, names=names)
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch == "S":
                s.behaviors[(cx, cy)] = "MB_SOUTH_ARROW_WARP"
    s.behaviors.update(behaviors or {})
    return s


def cells(keys, w):
    """names for a run of keys laid out w to a row."""
    return {k: (i % w, i // w) for i, k in enumerate(keys)}


def hflip_layer(L, ox, oy, w=16, h=16):
    L.a[oy:oy + h, ox:ox + w] = L.a[oy:oy + h, ox:ox + w][:, ::-1].copy()


# --------------------------------------------------------------------------
# Floors: backstage boards, the stage, the deck, the orchestra's flags
# --------------------------------------------------------------------------

def boards(L, ox, oy, kind="wings", v=0):
    """The wings: narrow dark backstage boards running east-west, four to a tile,
    their ends staggered. kind 'stage' and 'deck' have their own grain."""
    if kind == "stage":
        return stage_boards(L, ox, oy, v)
    if kind == "deck":
        return deck_boards(L, ox, oy, v)
    for y in range(16):
        row, yy = y // 4, y % 4
        off = ((0, 8, 4, 12) if v % 2 == 0 else (8, 2, 12, 6))[row]
        for x in range(16):
            xx = (x + off) % 16
            if yy == 3 or xx == 0:
                c = "yw0"
            elif yy == 0:
                c = "yw2" if xx > 1 else "yw1"
            else:
                c = "yw1"
            if yy == 1 and (x * 7 + row * 5 + v * 3) % 23 == 0:
                c = "yw0"
            L.px(ox + x, oy + y, c)


def flag(L, ox, oy, v=0):
    """The orchestra's paving: honey limestone slabs, staggered courses."""
    for y in range(16):
        course = y // 8
        off = (0, 4, 2)[(v + course) % 3]
        for x in range(16):
            xx = (x + off) % 8
            yy = y % 8
            if yy == 7 or xx == 7:
                c = "yq1"
            elif yy == 0 or xx == 0:
                c = "yq3"
            elif (x * 7 + y * 3 + v * 5) % 29 == 0:
                c = "yq1"
            elif (x * 3 + y * 5 + v) % 31 == 0:
                c = "yq3"
            else:
                c = "yq2"
            L.px(ox + x, oy + y, c)


def floor_pieces():
    keys = ["planks", "planks_b", "planks_knot", "planks_worn", "stage", "stage_b",
            "stage_gilt", "stage_mark", "void", "flag", "flag_b", "flag_c", "deck", "deck_b",
            "deck_edge", "deck_edge_b", "stage_lamp", "deck_ivy", "deck_crate"]
    s = struct("floor", "Floors: the wings, the stage, the roof, the orchestra", 8, 3,
               walk=["........", "X.......", "XXXXXXXX"],
               names=cells(keys, 8),
               notes="`planks` are the wings' dark backstage boards (`_b`, `_knot` and "
                     "`_worn` to break a run). `stage` is the stage's wide honey-coloured "
                     "boards (`stage_gilt` has a gilt inlay, for Act III; `stage_mark` a chalk "
                     "cross where an actor stands); `stage_lamp` is a footlight, a clay lamp "
                     "burning at the stage's front edge (blocks; `_gilt` for Act III). `deck` "
                     "is the skene roof's weathered planks, laid north-south; `deck_edge` is "
                     "the roof's front row, its lip dropping to the audience; `deck_ivy` a "
                     "pot of ivy and `deck_crate` Thespis's empty mask crate on the roof. "
                     "`flag` paves the orchestra. `void` blocks: the border.")
    L, M = s.B, s.M
    for i, k in enumerate(keys):
        ox, oy = (i % 8) * 16, (i // 8) * 16
        if k.startswith("planks"):
            boards(L, ox, oy, "wings", 1 if k == "planks_b" else 0)
            if k == "planks_knot":
                put(L, ox + 9, oy + 4, [".00.", "0..0", ".00."], {"0": "yw0", ".": "yw2"})
            if k == "planks_worn":
                for y in range(16):
                    for x in range(6, 10):
                        if L.get(ox + x, oy + y) == "yw1" and (x + y) % 3 == 0:
                            L.px(ox + x, oy + y, "yw2")
        elif k.startswith("stage"):
            stage_boards(L, ox, oy, 1 if k == "stage_b" else 0)
            if k in ("stage_gilt", "stage_lamp_gilt"):
                for x in range(16):
                    L.px(ox + x, oy + 6, "yo0")
                    L.px(ox + x, oy + 7, "yo1" if x % 4 else "yo0")
                    L.px(ox + x, oy + 8, "yo0")
            if k == "stage_mark":
                put(L, ox + 5, oy + 9, ["w....w", ".w..w.", "..ww..", ".w..w.", "w....w"],
                    {"w": "yw5"})
            if k.startswith("stage_lamp"):
                footlight(M, ox, oy)
        elif k == "void":
            L.rect(ox, oy, 16, 16, "yk")
        elif k.startswith("flag"):
            flag(L, ox, oy, {"flag": 0, "flag_b": 1, "flag_c": 2}[k])
        elif k.startswith("deck"):
            deck_boards(L, ox, oy, 1 if k.endswith("_b") else 0)
            if k.startswith("deck_edge"):
                for x in range(16):
                    L.px(ox + x, oy + 12, "yw3")
                    L.px(ox + x, oy + 13, "yw4" if x % 4 else "yw3")
                    L.px(ox + x, oy + 14, "yw1")
                    L.px(ox + x, oy + 15, "yw0")
            if k == "deck_ivy":
                put(M, ox + 1, oy, [
                    "...v..vV..v...",
                    "..vVv.vVv.Vv..",
                    ".vVvVvVvVvVvv.",
                    "vVv.vVVvVv.vVv",
                    ".v.vVvVVvVv.v.",
                    "...vVvVvVv....",
                    "..kttttttttk..",
                    "..kTTTTTTTTk..",
                    "...kTTTTTTk...",
                    "...kTttttTk...",
                    "...ktTTTTtk...",
                    "....kttttk....",
                    "....kkkkkk....",
                ], {"v": "yv1", "V": "yv2", "k": "yz0", "t": "yt1", "T": "yt2"})
            if k == "deck_crate":
                put(M, ox + 1, oy + 2, [
                    "kkkkkkkkkkkkkk",
                    "kWwwwwwwwwwwWk",
                    "kwkkkkkkkkkkwk",
                    "kwkyYyyYyYykwk",
                    "kwkYyyYyyyYkwk",
                    "kwkkkkkkkkkkwk",
                    "kWwwwwwwwwwwWk",
                    "kwwwlwwlwwlwwk",
                    "kwwlwlwlwlwlwk",
                    "kwwwlwwlwwlwwk",
                    "kWwwwwwwwwwwWk",
                    "kkkkkkkkkkkkkk",
                ], {"k": "yw0", "w": "yw2", "W": "yw3", "y": "yw4", "Y": "yw5", "l": "yw1"})
    return s


# --------------------------------------------------------------------------
# The temple's walls: caps, side walls, the black-figure frieze
# --------------------------------------------------------------------------

def cap(L, ox, oy, end=None):
    """The top of a wall seen from above: dark wine plaster, a gilt cornice at its
    south edge. end 'L'/'R' gives the wall a finished end on that side (an opening
    or a stair beside it)."""
    for y in range(16):
        for x in range(16):
            if y < 11:
                c = "yp0" if (x * 3 + y * 5) % 9 else "yp1"
                if y == 0:
                    c = "yp1"
            elif y == 11:
                c = "yo0"
            elif y == 12:
                c = "yo1" if x % 4 else "yo0"
            elif y == 13:
                c = "yp3"
            else:
                c = "yp2"
            L.px(ox + x, oy + y, c)
    if end:
        # 'L': the wall ends on its left (an opening to the left), 'R' on its right
        for y in range(16):
            for i in range(3):
                x = i if end == "L" else 15 - i
                c = ("yp2", "yp3", "yp4")[i] if y < 11 else ("yp1", "yo0", "yo1")[i]
                L.px(ox + x, oy + y, c)


def side_wall(L, ox, oy, side):
    """The side walls from above: wine dark, a lit rim toward the room."""
    for y in range(16):
        for x in range(16):
            xx = x if side == "L" else 15 - x
            if xx < 11:
                c = "yp0" if (x + y * 3) % 7 else "yp1"
            elif xx == 11:
                c = "yo0"
            elif xx == 12:
                c = "yp4"
            elif xx == 13:
                c = "yp3"
            else:
                c = "yp2"
            L.px(ox + x, oy + y, c)


def cap_corner(L, ox, oy, side):
    cap(L, ox, oy)
    for y in range(16):
        for x in range(16):
            xx = x if side == "L" else 15 - x
            if xx < 11:
                L.px(ox + x, oy + y, "yp0" if (x + y * 3) % 7 else "yp1")
            elif xx == 11:
                L.px(ox + x, oy + y, "yo0")
            elif xx == 12:
                L.px(ox + x, oy + y, "yp4" if y < 11 else "yo1")


# Black-figure motifs on the frieze's gold band: 16 x 10, K black, W cream, R wine
FRIEZE = {
    "ivy": [
        "....K.......K...",
        "...KK..K...KK...",
        "..KK..KKK.KK..K.",
        ".KKKKKKKKKKKKKK.",
        "KK..KK...K..KK.K",
        "K..KKK..KKK..KK.",
        "...KK..KKK....K.",
        "....K...K.......",
        "................",
        "................",
    ],
    "kantharos": [
        "................",
        "..KKKKKKKKKKKK..",
        ".K.KKKKKKKKKK.K.",
        "K..KKKKKKKKKK..K",
        "K...KKKKKKKK...K",
        ".KK..KKKKKK..KK.",
        "......KKKK......",
        ".......KK.......",
        ".....KKKKKK.....",
        "....KKKKKKKK....",
    ],
    "panther": [
        "............KK..",
        "...........KWKK.",
        "..KKKKKKKKKKKKK.",
        ".KKWKKWKKWKKKK..",
        "K.KKKKKKKKKKKK..",
        "..KKKKKKKKKKK...",
        "..K.K.....K.K...",
        "..K..K....K..K..",
        ".KK..KK..KK..KK.",
        "................",
    ],
    "maenad": [
        ".V....KK........",
        "VVV..KWWK.......",
        ".K...KWWK.......",
        ".K..KKKKKK......",
        ".KKKKRRRRKK.....",
        ".K..KRRRRK.K....",
        ".K..KRRRRRK.....",
        ".K..KRRRRRRK....",
        ".K.KRRRRRRRRK...",
        ".K..KK....KK....",
    ],
    "satyr": [
        "..K.K...........",
        "..KKKK..........",
        "..KWKK......KK..",
        "...KKK.....KKKK.",
        "..KKKKK...KKKKKK",
        ".KKKKKKKKKKKKKK.",
        "K.KKKKK....KKKK.",
        "..KK.KK.........",
        ".KK...KK........",
        "KK.....KK.......",
    ],
    "grapes": [
        "......KK........",
        ".....K..K..K....",
        "..KKKKKKKKKK....",
        "...VKVKVKV......",
        "...KVKVKVK......",
        "....VKVKV.......",
        "....KVKVK.......",
        ".....VKV........",
        "......V.........",
        "................",
    ],
}
FRIEZE_LEGEND = {"K": "yk", "W": "ycr", "R": "yp1", "V": "yg0"}


def frieze_ground(L, ox, oy):
    """The temple's wall face: wine plaster, a gold band painted with black
    figures, a dark dado."""
    for y in range(16):
        for x in range(16):
            if y == 0:
                c = "yp2"
            elif y == 1:
                c = "yp3"
            elif y == 2:
                c = "yo0"
            elif y < 13:
                c = "yo1"
            elif y == 13:
                c = "yo0"
            elif y == 14:
                c = "yp2"
            else:
                c = "yp1"
            L.px(ox + x, oy + y, c)


def frieze_cell(L, ox, oy, motif):
    frieze_ground(L, ox, oy)
    if motif in FRIEZE:
        put(L, ox, oy + 3, FRIEZE[motif], FRIEZE_LEGEND)


def jamb(L, ox, oy, side):
    """The frieze wall ending at an opening: a plastered pilaster."""
    frieze_ground(L, ox, oy)
    for y in range(16):
        for x in range(16):
            xx = x if side == "L" else 15 - x   # 'L': opening to the left
            if xx < 5:
                L.px(ox + x, oy + y, "yk" if xx < 4 else "yp1")
            elif xx < 9:
                c = ("yp4", "yp3", "yp3", "yp2")[xx - 5]
                if y in (2, 13):
                    c = "yo0"
                L.px(ox + x, oy + y, c)


def wall_pieces():
    out = []
    keys = ["cap", "cap_corner_l", "cap_corner_r", "side_l", "side_r", "cap_end_l", "cap_end_r",
            "cap_gap"]
    s = struct("wall", "The temple's walls: caps, corners, side walls", 8, 1,
               walk=["XXXXXXX."],
               names=cells(keys, 8),
               notes="`cap` is the top of a wall seen from above, with a gilt cornice on its "
                     "south edge; every room's north wall starts with it. `side_l`/`side_r` run "
                     "down the map's edges. `cap_end_l` is the cap ending with an opening to its "
                     "left, `cap_end_r` an opening to its right (the parodos, a stair's top). "
                     "`cap_gap` is the walkable floor of an opening through a cap row.")
    L = s.B
    cap(L, 0, 0)
    cap_corner(L, 16, 0, "L")
    cap_corner(L, 32, 0, "R")
    side_wall(L, 48, 0, "L")
    side_wall(L, 64, 0, "R")
    cap(L, 80, 0, "L")
    cap(L, 96, 0, "R")
    boards(L, 112, 0, "wings", 1)
    for x in range(16):
        L.px(112 + x, 0, "yw0")
        L.px(112 + x, 15, "yw0")
    out.append(s)

    motifs = ["ivy", "kantharos", "panther", "maenad", "satyr", "grapes"]
    keys = motifs + ["jamb_l", "jamb_r"]
    s = struct("frieze", "The frieze: the god's revel in black figure", 8, 1, walk=["XXXXXXXX"],
               names=cells(keys, 8),
               notes="The temple's wall face, a gold band painted in black figure like a wine "
                     "cup: `ivy` and `grapes` between the revellers, `kantharos` (the god's "
                     "cup), `panther`, `maenad` (with her thyrsus), `satyr`. Hang it under a "
                     "`cap`. `jamb_l` ends the wall at an opening to its left, `jamb_r` to its "
                     "right.")
    for i, m in enumerate(motifs):
        frieze_cell(s.B, i * 16, 0, m)
    jamb(s.B, 96, 0, "L")
    jamb(s.B, 112, 0, "R")
    out.append(s)
    return out


# --------------------------------------------------------------------------
# The back walls behind each act's audience
# --------------------------------------------------------------------------

GARLAND = [
    "VV............VV",
    ".VvV........VvV.",
    "..VVv......vVV..",
    "...vVVvVVvVVv...",
    ".....vVgVVv.....",
    "......gGg.......",
    ".......g........",
]


def plaster(L, ox, oy, dado=True):
    for y in range(16):
        for x in range(16):
            c = "yp2"
            if (x * 7 + y * 11) % 19 == 0:
                c = "yp3"
            if (x * 5 + y * 3) % 23 == 0:
                c = "yp1"
            if dado and y >= 12:
                c = ("yo0", "yp1", "yp1", "yp0")[y - 12]
            L.px(ox + x, oy + y, c)


def mask_face(L, ox, oy, kind, legend):
    put(L, ox, oy, MASKS[kind], legend)


# The three masks, 12 x 12. W white, w shade, d dark shade, K holes, r lips,
# S satyr skin, s its shade, B beard, E ear
MASKS = {
    "comic": [
        "...wwwwww...",
        ".wwWWWWWWww.",
        "wWWWWWWWWWWw",
        "wWKKWWWWKKWw",
        "wWWKKWWKKWWw",
        "wWWWWWWWWWWw",
        "wrWWWWWWWWrw",
        "wWKWWWWWWKWw",
        "wWKKKKKKKKWw",
        ".wWKrrrrKWw.",
        "..wwKKKKww..",
        "....wwww....",
    ],
    "tragic": [
        "...wwwwww...",
        ".wwWWWWWWww.",
        "wWWKWWWWKWWw",
        "wWWWKWWKWWWw",
        "wWKKKWWKKKWw",
        "wWWKKWWKKWWw",
        "wWWWWWWWWWWw",
        "wWWWWddWWWWw",
        "wWWWKKKKWWWw",
        ".wWKKrrKKWw.",
        "..wKwwwwKw..",
        "...wwwwww...",
    ],
    "satyr": [
        "E..ssssss..E",
        "EEsSSSSSSsEE",
        ".EsSSSSSSsE.",
        ".sSKKSSKKSs.",
        ".sSKKSSKKSs.",
        ".sSSSddSSSs.",
        ".sSSdKKdSSs.",
        ".sSKSSSSKSs.",
        "..sSKKKKSs..",
        "..BBsSSsBB..",
        "...BBBBBB...",
        "....BBBB....",
    ],
}
MASK_LEGEND = {"W": "ym0", "w": "ym1", "d": "ym2", "K": "yk", "r": "yc2",
               "S": "ya1", "s": "ya0", "B": "yk", "E": "ya0"}
PAINTED_LEGEND = {"W": "ycr", "w": "yp4", "d": "yp3", "K": "yk", "r": "yp1",
                  "S": "yo1", "s": "yo0", "B": "yk", "E": "yo0"}


def back_wall_pieces():
    keys = ["act1", "act1_garland", "act2", "act2_masks", "act2_masks_b", "deck_face",
            "deck_face_masks", "deck_face_garland", "deck_face_arm", "deck_face_arm_lowered"]
    s = struct("back", "Back walls behind the audience", 5, 2, walk=["XXXXX", "XXXXX"],
               names=cells(keys, 5),
               notes="The wall each act's audience sits against, under a `cap`. Act I's is "
                     "plain wine plaster (`act1_garland` hung with an ivy garland); Act II's "
                     "is hung with painted masks (`act2_masks` the comic, `_b` the tragic). "
                     "Act III's is the front of the skene roof, carved and gilt "
                     "(`deck_face`, with gilt masks); `deck_face_arm` is the cell under the "
                     "god-machine, and `deck_face_arm_lowered` (+1) the same with the boom "
                     "swung down over it, its pulley and rope.")
    L, M = s.B, s.M
    pos = s.names
    for k in keys:
        cx, cy = pos[k]
        ox, oy = cx * 16, cy * 16
        if k.startswith("act1") or k.startswith("act2"):
            plaster(L, ox, oy)
        else:
            for y in range(16):
                for x in range(16):
                    if y < 2:
                        c = ("yo1", "yo0")[y]
                    elif y < 13:
                        c = "yw2" if (x % 8) not in (0, 7) else "yw1"
                        if (x % 8) == 1:
                            c = "yw3"
                        if y == 2:
                            c = "yw1"
                    else:
                        c = ("yo0", "yw1", "yw0")[y - 13]
                    L.px(ox + x, oy + y, c)
        if k.startswith("act2"):
            for x in range(16):
                L.px(ox + x, oy + 1, "yo0")
                L.px(ox + x, oy + 2, "yp4" if x % 3 else "yo1")
                L.px(ox + x, oy + 3, "yo0")
    cx, cy = pos["act1_garland"]
    put(M, cx * 16, cy * 16 + 1, GARLAND, {"V": "yv1", "v": "yv2", "g": "yg0", "G": "yg1"})
    wall_masks = {
        "act2_masks": [
            "...ccccc...",
            ".ccCCCCCcc.",
            "cCCCCCCCCCc",
            "cCKKCCCKKCc",
            "cCCCCCCCCCc",
            "cpCCCCCCCpc",
            "cCKCCCCCKCc",
            "cCKKKKKKKCc",
            ".cCKpppKCc.",
            "..cCKKKCc..",
            "...ccccc...",
        ],
        "act2_masks_b": [
            "...ccccc...",
            ".ccCCCCCcc.",
            "cCKCCCCCKCc",
            "cCCKKCKKCCc",
            "cCKKKCKKKCc",
            "cCCCCCCCCCc",
            "cCCCKKKCCCc",
            "cCCKCCCKCCc",
            ".cKCCCCCKc.",
            "..cCCCCCc..",
            "...ccccc...",
        ],
    }
    for k, rows in wall_masks.items():
        cx, cy = pos[k]
        put(L, cx * 16 + 2, cy * 16 + 4, rows, {"c": "yp4", "C": "ycr", "K": "yk", "p": "yp3"})
        L.px(cx * 16 + 7, cy * 16 + 4, "yo1")
        for y in range(9, 14):
            L.px(cx * 16 + 1, cy * 16 + y, "yp4" if y % 2 else "yp3")
            L.px(cx * 16 + 14, cy * 16 + y, "yp4" if y % 2 else "yp3")
    cx, cy = pos["deck_face_garland"]
    put(M, cx * 16, cy * 16 + 3, GARLAND, {"V": "yv1", "v": "yv2", "g": "yg0", "G": "yg1"})
    cx, cy = pos["deck_face_masks"]
    mask_small = {"comic": ["..WWWW..", ".WKWWKW.", "WWWWWWWW", "WKWWWWKW", ".WKKKKW.", "..WWWW.."],
                  "tragic": ["..WWWW..", ".WKWWKW.", "WWWWWWWW", "WWKKKKWW", ".KWWWWK.", "..WWWW.."]}
    put(M, cx * 16, cy * 16 + 4, mask_small["comic"], {"W": "yo1", "K": "yc1"})
    put(M, cx * 16 + 8, cy * 16 + 5, mask_small["tragic"], {"W": "yo1", "K": "yc1"})
    for k in ("deck_face_arm", "deck_face_arm_lowered"):
        cx, cy = pos[k]
        ox, oy = cx * 16, cy * 16
        put(L, ox + 5, oy + 3, ["iiiiii", "i....i", "i....i", "iiiiii"], {"i": "yir"})
        if k.endswith("lowered"):
            beam(M, ox, oy, 0, 9)
            put(M, ox + 3, oy + 8, ["kkkkkkkkkk", "kiiwwwwiik", "kiiwkkwiik", "kkkkkkkkkk"],
                {"k": "yk", "i": "yir", "w": "yw3"})
            rope(M, ox, oy, 12, 16)
    return s


# --------------------------------------------------------------------------
# The skene: caps, faces, doors (each act its own look)
# --------------------------------------------------------------------------

def skene_cap(L, ox, oy, act, gap=False):
    """The top of the skene, seen from the stage: a beam (I), a painted lintel
    (II), a marble cornice (III). With gap, the opening over a door, walkable: the
    cap's two ends and, between them, the threshold lit from the stage."""
    for y in range(16):
        for x in range(16):
            if act == 1:
                c = "yw2" if 3 <= y <= 12 else ("yw1" if y in (2, 13) else "yw0")
                if y == 4 or (y == 8 and x % 5 == 0):
                    c = "yw3"
                if y == 15:
                    c = "yw1"
            elif act == 2:
                c = ("yw1", "yy0", "yy1", "yy0", "yb0", "yb1", "yb1", "yb0", "yr0", "yr1", "yr1",
                     "yr1", "yr0", "yy0", "yy1", "yw1")[y]
                if 4 <= y <= 7 and (x + (y - 4)) % 4 == 0:
                    c = "yy1"
            else:
                c = ("yq1", "yq3", "yq4", "yq3", "yq2", "yq2", "yo1", "yo0", "yq3", "yq2",
                     "yq2", "yq2", "yq1", "yo0", "yo1", "yq1")[y]
                if 8 <= y <= 11 and x % 4 == 0:
                    c = "yq1"
            L.px(ox + x, oy + y, c)
    if not gap:
        return
    edge, joint, board, lit = {1: ("yw0", "yw2", "yw4", "yw5"), 2: ("yk", "yw2", "yw3", "yy1"),
                               3: ("yq0", "yq1", "yq3", "yq4")}[act]
    for y in range(16):
        for x in range(3, 13):
            c = board if y % 8 else joint
            if y % 8 == 1:
                c = lit
            if x == 3:
                c = edge
            if x == 12:
                c = joint
            L.px(ox + x, oy + y, c)


def act1_face(L, ox, oy, row, v=0):
    """Act I's set from behind: canvas stretched on rough timber."""
    for y in range(16):
        for x in range(16):
            c = "yn1" if (x + y * 2) % 5 else "yn0"
            if (x * 3 + y) % 11 == 0:
                c = "yn0"
            L.px(ox + x, oy + y, c)
    # the studs at the cell edges and a rail
    for y in range(16):
        L.px(ox + 0, oy + y, "yw1")
        L.px(ox + 1, oy + y, "yw2")
        L.px(ox + 2, oy + y, "yw3")
    if row == 0:
        for x in range(16):
            L.px(ox + x, oy + 0, "yw1")
            L.px(ox + x, oy + 1, "yw3")
            L.px(ox + x, oy + 2, "yw2")
            L.px(ox + x, oy + 3, "yw1")
        if v:
            # a diagonal brace, and a painted ivy leaf showing through the canvas
            for i in range(11):
                L.px(ox + 3 + i, oy + 4 + i, "yw2")
                L.px(ox + 4 + i, oy + 4 + i, "yw3")
                L.px(ox + 3 + i, oy + 5 + i, "yw1")
    else:
        for x in range(16):
            L.px(ox + x, oy + 12, "yw1")
            L.px(ox + x, oy + 13, "yw3")
            L.px(ox + x, oy + 14, "yw2")
            L.px(ox + x, oy + 15, "yk")
        if v:
            put(L, ox + 6, oy + 3, [".vv..", "vVVv.", ".vVVv", "..vv.", "...v."],
                {"v": "yv1", "V": "yv2"})


def act2_face(L, ox, oy, row, v=0):
    """Act II's palace front: red panels in ochre frames, blue bands."""
    for y in range(16):
        for x in range(16):
            if row == 0:
                if y < 3:
                    c = ("yb0", "yb1", "yb0")[y]
                elif y < 5:
                    c = ("yy1", "yy0")[y - 3]
                else:
                    c = "yr1" if 2 <= x <= 13 else "yy0"
                    if x in (2, 13) or y == 5:
                        c = "yy1" if x != 13 else "yy0"
                    if (x * 5 + y * 3) % 17 == 0 and 3 <= x <= 12:
                        c = "yr0"
                if y == 3 and x % 4 == 1:
                    c = "yb1"
            else:
                if y < 9:
                    c = "yr1" if 2 <= x <= 13 else "yy0"
                    if x in (2, 13) or y == 8:
                        c = "yy0"
                    if (x * 5 + y * 3) % 17 == 0 and 3 <= x <= 12:
                        c = "yr0"
                elif y < 11:
                    c = ("yy1", "yy0")[y - 9]
                else:
                    c = ("yb1", "yb0", "yb0", "yb0", "yk")[y - 11]
                    if y == 12 and (x + 1) % 4 == 0:
                        c = "yb1"
            L.px(ox + x, oy + y, c)
    if v and row == 0:
        # a painted rosette in the panel
        put(L, ox + 5, oy + 7, [".y..y.", "..yy..", "yyWWyy", "..yy..", ".y..y."],
            {"y": "yy1", "W": "ywh"})
    if v and row == 1:
        put(L, ox + 4, oy + 2, ["..v.v...", ".vvvvv..", "vv.v.vv.", "..vvv...", "...v...."],
            {"v": "yv1"})


def act2_end(L, ox, oy, row):
    """The east end of Act II's set, by the satyrs' corner: a painted pilaster."""
    act2_face(L, ox, oy, row)
    for y in range(16):
        for x in range(8, 16):
            c = ("yy1", "yy0", "yb1", "yb0", "yk", "yk", "yk", "yk")[x - 8]
            L.px(ox + x, oy + y, c)


def act3_face(L, ox, oy, row, v=0):
    """Act III's marble skene: ashlar, gilt capitals above, ivy carved below."""
    for y in range(16):
        for x in range(16):
            course = y // 5
            off = 0 if course % 2 == 0 else 8
            if y % 5 == 4 or (x + off) % 16 == 0:
                c = "yq1"
            elif y % 5 == 0 or (x + off) % 16 == 1:
                c = "yq4"
            else:
                c = "yq3" if (x * 3 + y * 7) % 13 else "yq2"
            L.px(ox + x, oy + y, c)
    if row == 0:
        for x in range(16):
            L.px(ox + x, oy + 0, "yo0")
            L.px(ox + x, oy + 1, "yo1")
        if v:
            # a fluted pilaster under a gilt capital
            for y in range(2, 16):
                for x in range(5, 11):
                    L.px(ox + x, oy + y, ("yq2", "yq4", "yq3", "yq4", "yq3", "yq1")[x - 5])
            put(L, ox + 3, oy + 2, ["oOOOOOOOOo", ".oOOOOOOo.", "..oooooo.."], {"o": "yo0", "O": "yo1"})
    else:
        for x in range(16):
            L.px(ox + x, oy + 13, "yo0")
            L.px(ox + x, oy + 14, "yq1")
            L.px(ox + x, oy + 15, "yk")
        if v:
            for y in range(0, 13):
                for x in range(5, 11):
                    L.px(ox + x, oy + y, ("yq2", "yq4", "yq3", "yq4", "yq3", "yq1")[x - 5])
        else:
            put(L, ox + 2, oy + 4, ["..v.....v...", ".vVv...vVv..", "v.v.vvv.v.v.", "...v...v...."],
                {"v": "yv0", "V": "yv1"})


def door_frame(L, ox, oy, row, painted=None):
    """A real door seen from the wings: oak posts and a dark lintel plaque for the
    sign (row 0), the doorway dark under it, and the stage's light on the boards
    beyond (row 1). painted gives Act I's flat door painted on canvas instead."""
    if painted:
        act1_face(L, ox, oy, row)
        frame, panel, shade = (("yr0", "yr1", "yy0") if painted == "crown" else ("yw1", "yw2", "yn0"))
        y0, y1 = (6, 16) if row == 0 else (0, 14)
        for y in range(y0, y1):
            for x in range(3, 13):
                c = panel
                if x in (3, 12) or (row == 0 and y == y0) or (row == 1 and y == y1 - 1):
                    c = frame
                elif x in (7, 8):
                    c = frame
                elif (row == 0 and y in (y0 + 2,)) or (row == 1 and y in (4, 10)):
                    c = shade
                L.px(ox + x, oy + y, c)
            L.px(ox + 13, oy + y, "yn0")
        if row == 1:
            L.px(ox + 10, oy + 7, "yy1")
        return
    for y in range(16):
        for x in range(16):
            if x <= 2 or x >= 13:
                c = ("yw0", "yw3", "yw2")[x] if x <= 2 else ("yw0", "yw1", "yw2")[15 - x]
                if y % 8 == 4 and x in (1, 14):
                    c = "yo1"
            elif row == 0 and y < 7:
                # the lintel: a dark plaque in a gilt frame, for the sign to stand out on
                c = "yk"
                if y in (0, 6):
                    c = "yo0"
                if x in (3, 12):
                    c = "yo0"
            elif row == 0:
                c = "yk" if x in (3, 12) or y < 10 else "yw0"
            else:
                if x in (3, 12):
                    c = "yk"
                elif y < 6:
                    c = "yw0"
                elif y < 15:
                    c = "yw4" if (y - 6) % 4 else "yw3"
                    if y == 6:
                        c = "yw2"
                    if x == 11 and y > 6:
                        c = "yw3"
                else:
                    c = "yw1"
            L.px(ox + x, oy + y, c)


def door_sign(M, ox, oy, kind):
    """The door's sign on its dark lintel, in the middle layer."""
    if kind == "ivy":
        put(M, ox + 3, oy + 1, [
            "vV.vVv.Vv.",
            "VvVVvVvVVv",
            ".vV.gg.Vv.",
            "...gGGg...",
            "....gg....",
        ], {"v": "yv1", "V": "yv2", "g": "yg0", "G": "yg1"})
    elif kind == "crown":
        put(M, ox + 3, oy + 1, [
            "o..o..o..o",
            "Oo.OoOO.oO",
            "OOOOOOOOOO",
            "ORoOoOoRoO",
            "oooooooooo",
        ], {"o": "yo0", "O": "yo1", "R": "yc2"})
    elif kind == "goat":
        put(M, ox + 3, oy + 1, [
            "W........W",
            ".WW....WW.",
            "...WwwW...",
            "...wKKw...",
            "....ww....",
        ], {"W": "ycr", "w": "yp4", "K": "yk"})


def door_curtain(M, ox, oy, row):
    """The doorway's wine-red curtain: a valance across the top (row 0) and the
    drape pulled back to the left post and tied (row 1)."""
    if row == 0:
        for x in range(3, 13):
            for y in (8, 9, 10):
                M.px(ox + x, oy + y, ("yc1", "yc2", "yo1" if x % 2 else "yo0")[y - 8])
        for y in range(11, 16):
            for x in range(3, 3 + 4):
                M.px(ox + x, oy + y, ("yc1", "yc2", "yc3", "yc2")[x - 3])
        return
    for y in range(0, 14):
        w = 4 if y < 5 else (2 if y < 8 else 3 + (y - 8) // 3)
        for i in range(w):
            M.px(ox + 3 + i, oy + y, ("yc1", "yc2", "yc3", "yc2", "yc1")[i])
        M.px(ox + 3 + w, oy + y, "yc0")
    for x in range(3, 8):
        M.px(ox + x, oy + 6, "yo1")
    M.px(ox + 6, oy + 7, "yo0")


def skene_pieces():
    out = []
    for act, face in ((1, act1_face), (2, act2_face), (3, act3_face)):
        roman = "I" * act
        keys = ["cap", "cap_gap", "upper", "upper_b", "lower", "lower_b"]
        if act == 2:
            keys += ["upper_end", "lower_end"]
        s = struct(f"skene{act}", f"Act {roman}'s set seen from the wings", len(keys), 1,
                   walk=["X.XXXXXX"[:len(keys)]],
                   names=cells(keys, 8),
                   notes={1: "Rough timber and canvas, the back of a travelling set. Three rows: "
                             "`cap` (the top beam, seen from the stage), `upper`, `lower` "
                             "(`_b` braced, or with ivy painted through the canvas). "
                             "`cap_gap` is the way through the cap over a real door: walkable.",
                          2: "A painted palace front: red panels in ochre frames between blue "
                             "bands (`_b` with a rosette or painted ivy). `upper_end` and "
                             "`lower_end` finish the set's east end, by the satyrs' corner.",
                          3: "The marble skene, the grandest: ashlar under a gilt band, ivy "
                             "carved low (`_b` is a fluted pilaster, upper and lower)."}[act])
        L = s.B
        skene_cap(L, 0, 0, act)
        skene_cap(L, 16, 0, act, gap=True)
        face(L, 32, 0, 0)
        face(L, 48, 0, 0, 1)
        face(L, 64, 0, 1)
        face(L, 80, 0, 1, 1)
        if act == 2:
            act2_end(L, 96, 0, 0)
            act2_end(L, 112, 0, 1)
        out.append(s)

    keys = ["ivy_upper", "crown_upper", "goat_upper", "ivy", "crown", "goat",
            "crown_painted_upper", "goat_painted_upper", "crown_painted", "goat_painted"]
    s = struct("doors", "The three doors, and Act I's painted two", 5, 2,
               walk=[".....", ".XXXX"],
               names={"ivy_upper": (0, 0), "crown_upper": (1, 0), "goat_upper": (2, 0),
                      "ivy": (3, 0), "crown": (4, 0),
                      "goat": (0, 1), "crown_painted_upper": (1, 1), "goat_painted_upper": (2, 1),
                      "crown_painted": (3, 1), "goat_painted": (4, 1)},
               notes="A real door is `<kind>_upper` (its sign on the lintel: an ivy garland "
                     "with grapes, a gilt crown, goat horns) over the doorway `<kind>`, both "
                     "walkable: put the entrance's coord event on the doorway, and the act's "
                     "`cap_gap` above the upper cell. The doorway is dark under a wine-red "
                     "valance, its curtain tied back, and the stage's light lies on the boards "
                     "beyond. Act I's crown and goat doors are only painted on its canvas "
                     "(`*_painted_upper` over `*_painted`): both block.")
    L, M = s.B, s.M
    pos = s.names
    for kind in ("ivy", "crown", "goat"):
        ux, uy = pos[f"{kind}_upper"]
        lx, ly = pos[kind]
        door_frame(L, ux * 16, uy * 16, 0)
        door_frame(L, lx * 16, ly * 16, 1)
        door_sign(M, ux * 16, uy * 16 + 0, kind)
        door_curtain(M, ux * 16, uy * 16, 0)
        door_curtain(M, lx * 16, ly * 16, 1)
    for kind in ("crown", "goat"):
        ux, uy = pos[f"{kind}_painted_upper"]
        lx, ly = pos[f"{kind}_painted"]
        door_frame(L, ux * 16, uy * 16, 0, painted=kind)
        door_frame(L, lx * 16, ly * 16, 1, painted=kind)
        # the sign painted flat on the canvas above it
        if kind == "crown":
            put(L, ux * 16 + 2, uy * 16 + 0, [
                ".y...y...y..",
                "yYy.yYy.yYy.",
                "yYYyYYYyYYy.",
                "yyyyyyyyyyy.",
            ], {"y": "yy0", "Y": "yy1"})
        else:
            put(L, ux * 16 + 2, uy * 16 + 0, [
                "w..........w",
                ".ww......ww.",
                "...wwnnww...",
                ".....nn.....",
            ], {"w": "yw1", "n": "yw2"})
    out.append(s)
    return out


# --------------------------------------------------------------------------
# The mask rack: one peg per mask, full or empty (+1)
# --------------------------------------------------------------------------

def peg_board(L, ox, oy):
    for y in range(16):
        for x in range(16):
            c = "yw2"
            if x in (0, 15):
                c = "yw0"
            elif x in (1,):
                c = "yw3"
            elif x == 14:
                c = "yw1"
            elif y in (0, 1):
                c = ("yw1", "yw3")[y]
            elif y >= 14:
                c = ("yw1", "yk")[y - 14]
            elif (x * 3 + y * 7) % 11 == 0:
                c = "yw1"
            L.px(ox + x, oy + y, c)


def rack_pieces():
    keys = ["comic", "comic_empty", "tragic", "tragic_empty", "satyr", "satyr_empty"]
    s = struct("rack", "The mask rack: pegs, full or empty", 6, 1, walk=["XXXXXX"],
               names=cells(keys, 6),
               notes="Hang the rack on a skene's `lower` row, one cell per mask, faced from "
                     "the wings. Each peg is a little oak board; `<mask>_empty` (= the full "
                     "peg + 1) is the same peg with its mask gone, for the mask the player is "
                     "wearing. Act I's rack is the comic peg alone.")
    L, M = s.B, s.M
    for i, k in enumerate(keys):
        ox = i * 16
        peg_board(L, ox, 0)
        put(L, ox + 6, 2, ["kk", "kk", ".k"], {"k": "yk"})   # the peg
        if not k.endswith("_empty"):
            mask_face(M, ox + 2, 3, k, MASK_LEGEND)
            M.px(ox + 7, 3, "yo0")
            M.px(ox + 8, 3, "yo0")
    return s


# --------------------------------------------------------------------------
# The audience: clay votive figures on stone tiers
# --------------------------------------------------------------------------

def tier(L, ox, oy, end=None):
    """One stone tier: the seat's top, the lit nose of the step, its riser."""
    for y in range(16):
        for x in range(16):
            if y == 0:
                c = "yq1"
            elif y < 8:
                c = "yq2" if (x * 7 + y * 5) % 23 else "yq3"
            elif y == 8:
                c = "yq4"
            elif y == 9:
                c = "yq3"
            elif y < 15:
                c = "yq1" if (x + y) % 11 else "yq0"
            else:
                c = "yq0"
            L.px(ox + x, oy + y, c)
    if end:
        for x in (range(12, 16) if end == "R" else range(0, 4)):
            xx = x - 12 if end == "R" else 3 - x
            for y in range(16):
                L.px(ox + x, oy + y, ("yq4", "yq2", "yq1", "yq0")[xx] if y < 15 else "yq0")


# a votive figure, 5 wide: H head, h shade, K mouth and eyes, B body
FIG_LEGEND = {"H": "yt3", "o": "yt1", "K": "yk", "B": "yt2", "b": "yt1", "k": "yk",
              "R": "yrd", "r": "yt0", "v": "yv1", "V": "yv2", "W": "ywh"}

TIER_SETS = {
    "back_a": [("hair", 0, 1), ("white wreath", 8, 0)],
    "back_b": [("plain", 1, 0), ("hair red", 9, 1)],
    "back_c": [("wreath", 0, 0), ("arms", 9, 1)],
    "front_a": [("white", 1, 1), ("hair", 9, 0)],
    "front_b": [("hair red", 0, 0), ("wreath", 8, 1)],
    "front_c": [("plain arms", 1, 0), ("white hair", 9, 1)],
}


def figures(M, ox, oy, layout, skip=()):
    for i, (kind, fx, fy) in enumerate(layout):
        if i in skip:
            continue
        put(M, ox + fx, oy + fy + 1, figure_rows(kind), FIG_LEGEND)


def rope(M, ox, oy, y0, y1):
    for y in range(y0, y1):
        M.px(ox + 7, oy + y, "yrp")
        M.px(ox + 8, oy + y, "yw2")


def tier_pieces():
    keys = list(TIER_SETS) + ["back_end_l", "front_end_l", "back_end_r", "front_end_r",
                              "back_arm", "back_arm_lowered", "front_arm", "front_arm_lowered"]
    s = struct("audience", "The audience: clay votive figures on stone tiers", 7, 2,
               walk=["XXXXXXX", "XXXXXXX"],
               names=cells(keys, 7),
               notes="Two tiers along each act's back wall: a `back_*` row against the wall "
                     "and a `front_*` row before it, each in three arrangements. The audience "
                     "is clay votives, two to a seat, with painted hair, white faces, ivy "
                     "wreaths, red robes, and their mouths open. `*_end_l`/`*_end_r` finish a "
                     "run beside a stair. Under the god-machine: `back_arm`/`front_arm`, and "
                     "`*_lowered` (+1) with its rope hanging down over the figures.")
    L, M = s.B, s.M
    for i, k in enumerate(keys):
        ox, oy = (i % 7) * 16, (i // 7) * 16
        if k in TIER_SETS:
            tier(L, ox, oy)
            figures(M, ox, oy, TIER_SETS[k])
        elif "end" in k:
            side = "L" if k.endswith("_l") else "R"
            tier(L, ox, oy, end=side)
            lay = TIER_SETS["back_a" if k.startswith("back") else "front_b"]
            figures(M, ox, oy, [lay[1]] if side == "L" else [lay[0]])
        else:
            tier(L, ox, oy)
            lay = TIER_SETS["back_c" if k.startswith("back") else "front_a"]
            figures(M, ox, oy, [(lay[0][0], 0, lay[0][2]), (lay[1][0], 9, lay[1][2])])
            if k.endswith("_lowered"):
                rope(M, ox, oy, 0, 16)
    return s


# --------------------------------------------------------------------------
# The curtained stair at a stage's end
# --------------------------------------------------------------------------

def steps(L, ox, oy, side, top=False):
    """Wooden steps rising north, with a banister on the outer edge."""
    for y in range(16):
        for x in range(16):
            yy = y % 4
            c = ("yw4", "yw3", "yw2", "yw0")[yy]
            if top and y < 4:
                c = "yw2"
            L.px(ox + x, oy + y, c)
    bx = range(0, 3) if side == "L" else range(13, 16)
    for x in bx:
        for y in range(16):
            xx = x if side == "L" else 15 - x
            L.px(ox + x, oy + y, ("yw1", "yw3", "yw2")[xx] if y % 8 else "yo0")


def curtain(M, ox, oy, side, open_):
    """A wine-red stage curtain with a gilt fringe. Closed, it hangs across the
    stair; open, it is drawn back to the outer post and tied."""
    if not open_:
        for y in range(16):
            for x in range(16):
                fold = (x + (0 if side == "L" else 8)) % 8
                c = ("yc0", "yc1", "yc2", "yc2", "yc3", "yc2", "yc1", "yc1")[fold]
                if y >= 14:
                    c = "yo1" if (x + y) % 2 else "yo0"
                if y == 0:
                    c = "yo0"
                M.px(ox + x, oy + y, c)
        return
    # drawn back: a narrow fall of cloth at the outer edge, tied with a gilt cord
    for y in range(16):
        w = 5 if y < 6 else (3 if y < 11 else 4)
        for i in range(w):
            x = i if side == "L" else 15 - i
            c = ("yc1", "yc2", "yc3", "yc2", "yc1")[i % 5]
            if y >= 14:
                c = "yo1" if (x + y) % 2 else "yo0"
            M.px(ox + x, oy + y, c)
    cx = 3 if side == "L" else 12
    for x in range(cx - 2, cx + 3):
        M.px(ox + x, oy + 7, "yo1")
    M.px(ox + cx, oy + 8, "yo0")


def stair_pieces():
    keys = ["top_l", "top_r", "through_l", "through_r", "steps_l", "steps_r",
            "foot_closed_l", "foot_closed_r", "foot_open_l", "foot_open_r"]
    s = struct("stair", "The curtained stair: up from a stage to the next act's wings", 2, 5,
               walk=["..", "..", "..", "XX", ".."],
               names={"top_l": (0, 0), "top_r": (1, 0), "through_l": (0, 1), "through_r": (1, 1),
                      "steps_l": (0, 2), "steps_r": (1, 2), "foot_closed_l": (0, 3),
                      "foot_closed_r": (1, 3), "foot_open_l": (0, 4), "foot_open_r": (1, 4)},
               notes="Two cells wide, five rows from the next act's wall `cap` (`top`) down "
                     "through its back wall (`through`) and past the audience (`steps`) to the "
                     "stage (`foot`). The curtain hangs at the foot: `foot_closed_*` blocks; "
                     "`foot_open_*` is the same stair with the curtain drawn back "
                     "and tied, walkable.")
    L, M = s.B, s.M
    for side, cx in (("L", 0), ("R", 1)):
        steps(L, cx * 16, 0, side, top=True)
        steps(L, cx * 16, 16, side)
        # the back wall's thickness either side of the stair's way through it
        for y in range(16):
            for x in (range(0, 3) if side == "L" else range(13, 16)):
                L.px(cx * 16 + x, 16 + y, "yw1" if y < 13 else "yw0")
        steps(L, cx * 16, 32, side)
        steps(L, cx * 16, 48, side)
        curtain(M, cx * 16, 48, side, False)
        steps(L, cx * 16, 64, side)
        curtain(M, cx * 16, 64, side, True)
    return s


# --------------------------------------------------------------------------
# The skene roof and the god-machine
# --------------------------------------------------------------------------

def deck_pieces():
    keys = ["mast_top", "mast_top_lowered", "mast", "mast_lowered", "arm", "arm_lowered",
            "hook", "hook_lowered", "winch", "bronteion_top", "bronteion", "rope_coil",
            "amphorae", "edge_post", "lamp_post", "throne"]
    s = struct("machine", "The skene roof and the god-machine", 8, 2,
               walk=["XXXX...X", "XXXXXXXX"],
               names=cells(keys, 8),
               notes="On the roof (`deck` boards): the crane's `mast_top` over `mast`, its "
                     "`winch` beside it, and in front, on the roof's edge, `arm`. Each has a "
                     "`_lowered` twin (+1): raised, the boom stands up against the mast; "
                     "lowered, it swings forward over the audience, over the player's head on "
                     "the edge (drawn in the top layer), past `deck_face_arm`, and lets its "
                     "rope down the tiers' `*_arm` cells to `hook_lowered` on the stage "
                     "(`hook` is plain stage boards; lowered, it blocks: face it to hold on). "
                     "Props: the thunder machine (`bronteion_top` over `bronteion`), a "
                     "`rope_coil`, `amphorae`, an `edge_post`, a `lamp_post`, and the "
                     "Hierophant's `throne`.")
    L, M, T = s.B, s.M, s.T
    pos = s.names
    for k in keys:
        cx, cy = pos[k]
        ox, oy = cx * 16, cy * 16
        if k.startswith("hook"):
            stage_boards(L, ox, oy)
        elif k.startswith("arm"):
            deck_boards(L, ox, oy)
            for x in range(16):
                L.px(ox + x, oy + 12, "yw3")
                L.px(ox + x, oy + 13, "yw4" if x % 4 else "yw3")
                L.px(ox + x, oy + 14, "yw1")
                L.px(ox + x, oy + 15, "yw0")
        else:
            deck_boards(L, ox, oy)
    # the mast: a squared oak post with iron bands
    for k in ("mast_top", "mast_top_lowered", "mast", "mast_lowered"):
        cx, cy = pos[k]
        ox, oy = cx * 16, cy * 16
        mast(M, ox, oy)
        for yb in ((4, 12) if k.startswith("mast_top") else (6,)):
            for i in range(1, 7):
                M.px(ox + 4 + i, oy + yb, "yir")
            M.px(ox + 5, oy + yb + 1, "yir")
        if k.startswith("mast_top"):
            # the pulley block at the head
            put(M, ox + 3, oy, [
                "kkkkkkkkkk",
                "kwWWWWWWwk",
                "kwWiiiiWwk",
                "kwWiwwiWwk",
                "kwWiiiiWwk",
                "kkkkkkkkkk",
            ], {"k": "yk", "w": "yw2", "W": "yw3", "i": "yir"})
        if k == "mast":
            put(M, ox + 2, oy + 12, [
                "kkkkkkkkkkkk",
                "kwwwwwwwwwwk",
                "kWWWWWWWWWWk",
                ".kkkkkkkkkk.",
            ], {"k": "yw0", "w": "yw2", "W": "yw3"})
        if k == "mast_lowered":
            put(M, ox + 2, oy + 12, [
                "kkkkkkkkkkkk",
                "kwwwwwwwwwwk",
                "kWWWWWWWWWWk",
                ".kkkkkkkkkk.",
            ], {"k": "yw0", "w": "yw2", "W": "yw3"})
    # raised: the boom stands up against the mast, lashed to it
    cx, cy = pos["mast_top"]
    ox, oy = cx * 16, cy * 16
    for y in range(6, 16):
        for i, c in enumerate(("yw0", "yw3", "yw2", "yw1", "yw0")):
            M.px(ox + 11 + i, oy + y, c)
    for x in range(11, 16):
        M.px(ox + x, oy + 9, "yrp")
    cx, cy = pos["mast"]
    ox, oy = cx * 16, cy * 16
    for y in range(0, 11):
        for i, c in enumerate(("yw0", "yw3", "yw2", "yw1", "yw0")):
            M.px(ox + 11 + i, oy + y, c)
    for x in range(11, 16):
        M.px(ox + x, oy + 5, "yrp")
    # lowered: the boom swings forward from the head, in front of the mast
    cx, cy = pos["mast_top_lowered"]
    ox, oy = cx * 16, cy * 16
    beam(M, ox, oy, 6, 16)
    put(M, ox + 3, oy + 5, ["kkkkkkkkkk", "kiiiiiiiik"], {"k": "yk", "i": "yir"})
    cx, cy = pos["mast_lowered"]
    beam(M, cx * 16, cy * 16, 0, 12)
    cx, cy = pos["arm_lowered"]
    ox, oy = cx * 16, cy * 16
    for y in range(16):
        for i, c in enumerate(("yw0", "yw3", "yw4", "yw4", "yw3", "yw2", "yw1", "yw0")):
            T.px(ox + 4 + i, oy + y, c)
        if y % 6 == 3:
            for i in range(1, 7):
                T.px(ox + 4 + i, oy + y, "yir")
    # the winch: a spoked wheel on a drum of rope
    cx, cy = pos["winch"]
    put(M, cx * 16, cy * 16 + 1, [
        "....kkkkkk......",
        "..kkwWWWWwkk....",
        ".kwWk.W..kWwk...",
        ".kWk..W...kWk...",
        "kwW.k.W..k.Wwk..",
        "kW....kik...Wk..",
        "kWWWWWiiiWWWWkrr",
        "kW....kik...Wkrr",
        "kwW.k.W..k.Wwkrr",
        ".kWk..W...kWk.rr",
        ".kwWk.W..kWwk...",
        "..kkwWWWWwkk....",
        "....kkkkkk......",
        "...kk....kk.....",
    ], {"k": "yw0", "w": "yw2", "W": "yw3", "i": "yir", "r": "yrp"})
    # the hook: the rope down from the beam, and a big iron hook at shoulder height
    cx, cy = pos["hook_lowered"]
    ox, oy = cx * 16, cy * 16
    rope(M, ox, oy, 0, 6)
    put(M, ox + 3, oy + 5, [
        "...kkkkk..",
        "...kiiik..",
        "....kik...",
        "....kik...",
        ".k..kik...",
        "kik.kik...",
        "kiiikik...",
        ".kiiiik...",
        "..kkkk....",
    ], {"k": "yk", "i": "yir"})
    # the thunder machine: a bronze sheet hung in an oak frame
    legend = {"k": "yw0", "w": "yw3", "r": "yrp", "z": "yo0", "Z": "yo1"}
    cx, cy = pos["bronteion_top"]
    put(M, cx * 16, cy * 16 + 2, [
        "kkkkkkkkkkkkkkkk",
        "kwwwwwwwwwwwwwwk",
        "kkkkkkkkkkkkkkkk",
        ".k..r......r..k.",
        ".k.zzzzzzzzzz.k.",
        ".k.zZZZZZZZZz.k.",
        ".k.zZzzzzzzZz.k.",
        ".k.zZzZZZZzZz.k.",
        ".k.zZzZzzZzZz.k.",
        ".k.zZzZZZZzZz.k.",
        ".k.zZzzzzzzZz.k.",
        ".k.zZZZZZZZZz.k.",
        ".k.zzzzzzzzzz.k.",
        ".k............k.",
    ], legend)
    cx, cy = pos["bronteion"]
    put(M, cx * 16, cy * 16, [
        ".k............k.",
        ".k....k..k....k.",
        ".k....kkkk....k.",
        ".k............k.",
        ".k............k.",
        ".k............k.",
        "kkk..........kkk",
        "kwk..........kwk",
        "kkk..........kkk",
    ], legend)
    cx, cy = pos["rope_coil"]
    put(M, cx * 16 + 2, cy * 16 + 4, [
        "...rrrrrr...",
        ".rrRRRRRRrr.",
        "rRRrrrrrrRRr",
        "rRrRRRRRRrRr",
        "rRrRkkkkRrRr",
        "rRrRRRRRRrRr",
        "rRRrrrrrrRRr",
        ".rrRRRRRRrr.",
        "...rrrrrr...",
    ], {"r": "yw3", "R": "yrp", "k": "yw1"})
    cx, cy = pos["amphorae"]
    for ax in (1, 8):
        put(M, cx * 16 + ax, cy * 16 + 1, [
            "..kk..",
            ".k..k.",
            "..kk..",
            ".kwwk.",
            "kwWWwk",
            "kwWWwk",
            "kwWwwk",
            "kwwwwk",
            ".kwwk.",
            "..kk..",
            "..kk..",
            ".kkkk.",
        ], {"k": "yw1", "w": "yw3", "W": "yw4"})
    cx, cy = pos["edge_post"]
    put(M, cx * 16 + 5, cy * 16 + 1, ["kkkkkk", "kWwwwk", "kkkkkk"] + ["kWwwwk"] * 9 + ["kkkkkk"],
        {"k": "yw0", "w": "yw2", "W": "yw3"})
    cx, cy = pos["lamp_post"]
    put(M, cx * 16 + 4, cy * 16, [
        "..oo....",
        ".oOOo...",
        "kkkkkkk.",
        ".kwwwk..",
        "..kwk...",
        "..kwk...",
        "..kwk...",
        "..kwk...",
        "..kwk...",
        "..kwk...",
        "..kwk...",
        "..kwk...",
        ".kkwkk..",
        ".kwwwk..",
        ".kkkkk..",
    ], {"k": "yw0", "w": "yw3", "o": "yo0", "O": "yo1"})
    cx, cy = pos["throne"]
    put(M, cx * 16 + 2, cy * 16, [
        "..kkkkkkkk..",
        ".kWwwwwwwwk.",
        ".kwkkkkkkwk.",
        ".kwkcCCckwk.",
        ".kwkcCCckwk.",
        ".kwkkkkkkwk.",
        "kkwwwwwwwwkk",
        "kWwwwwwwwwWk",
        "kwccccccccwk",
        "kwcCCCCCCcwk",
        "kkkkkkkkkkkk",
        ".kw......wk.",
        ".kw......wk.",
        ".kk......kk.",
    ], {"k": "yw0", "w": "yw2", "W": "yw4", "c": "yc1", "C": "yc2"})
    return s


# --------------------------------------------------------------------------
# The orchestra: the great altar, its ring, the god's image's base, torches
# --------------------------------------------------------------------------

def ring_px(x, y, w, h):
    """Distance-to-ellipse band of the orchestra's marble ring, for pixel (x, y)
    of a w x h px region."""
    cx, cy = (w - 1) / 2, (h - 1) / 2
    rx, ry = w / 2 - 3, h / 2 - 3
    d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
    return d


def orchestra_pieces():
    W, H = 5, 4
    s = struct("orchestra", "The god's orchestra: the dancing floor round the great altar", W, H,
               walk=[".....", ".XXX.", ".XXX.", "....."],
               names={f"r{y}{x}": (x, y) for y in range(H) for x in range(W)},
               notes="Five by four. A round dancing floor of pale marble, ringed in grey, on "
                     "the orchestra's flags; the great altar of Dionysus stands in the middle "
                     "(the inner 3 x 2, blocking): a marble table with scrolled ends, hung "
                     "with ivy, its top stained with wine, a black kantharos and a bunch of "
                     "grapes on it, a panther carved on its front. Place it whole; "
                     "`r<row><col>` names each cell. The block is drawn symmetric, so its "
                     "right half costs no tiles.")
    L, M = s.B, s.M
    pw, ph = W * 16, H * 16
    for cy in range(H):
        for cx in range(3):
            flag(L, cx * 16, cy * 16, (cx + cy) % 3)
    # the ring, the floor inside it, the altar: drawn on the left half, then mirrored
    for y in range(ph):
        for x in range(pw // 2 + 1):
            d = ring_px(x, y, pw, ph)
            if d <= 1.0:
                c = "yq3" if (x * 3 + y * 7) % 17 else "yq4"
                if d > 0.86:
                    c = "yq1" if d < 0.93 else "yq0"
                elif d > 0.80:
                    c = "yq4"
                L.px(x, y, c)
    ax, ay = 16 + 1, 16 + 1      # the altar block: 46 x 30, top 13 rows, then its front
    aw, ah = 46, 30
    top = 13
    for y in range(ah):
        for x in range(aw // 2 + 1):
            if y == 0:
                c = "yq0"
            elif y == 1:
                c = "yq4"
            elif y < top - 1:
                c = "yq3" if (x + y) % 9 else "yq2"
            elif y == top - 1:
                c = "yq4"
            elif y == top:
                c = "yq1"
            elif y < ah - 4:
                c = "yq2"
                if 6 <= x and (y in (top + 2, ah - 6)):
                    c = "yq1"
                if x == 6 and top + 2 <= y <= ah - 6:
                    c = "yq1"
            elif y < ah - 2:
                c = ("yq3", "yq1")[y - (ah - 4)]
            else:
                c = ("yq0", "yk")[y - (ah - 2)]
            if x == 0:
                c = "yq0"
            L.px(ax + x, ay + y, c)
    # the volutes: scrolled cushions at each end of the top
    put(L, ax + 1, ay + 1, [
        ".oooooo.",
        "oQQQQQQo",
        "oQoooooQ",
        "oQoQQQoQ",
        "oQoQooQQ",
        "oQoQQQQo",
        "oQooooo.",
        "oQQQQQQo",
        "oooooooo",
        "oQQQQQQo",
        "oQQQQQQo",
        ".oooooo.",
    ], {"o": "yq1", "Q": "yq4"})
    for y in range(ph):
        for x in range(pw // 2 + 1, pw):
            L.a[y, x] = L.a[y, pw - 1 - x]
    # ivy along the front edge (symmetric too)
    for x in range(1, aw // 2 + 1):
        y = top + 1 + (2 if (x // 5) % 2 else 0) - (1 if x % 5 == 2 else 0)
        L.px(ax + x, ay + y, "yv1" if x % 3 else "yv2")
        L.px(ax + aw - 1 - x, ay + y, "yv1" if x % 3 else "yv2")
        if x % 5 == 0:
            L.px(ax + x, ay + y + 1, "yv0")
            L.px(ax + aw - 1 - x, ay + y + 1, "yv0")
    # the panther carved in the front's middle panel
    put(L, ax + 14, ay + top + 5, [
        "...............kk.",
        "..............kqqk",
        "..kkkkkkkkkkkkkqk.",
        ".kqqqqqqqqqqqqqk..",
        "k.kqqqqqqqqqqqk...",
        "..kq.k......kq.k..",
        "..k..k......k..k..",
    ], {"k": "yq1", "q": "yq4"})
    # on the slab: the kantharos, grapes, a spill of wine
    put(M, ax + 17, ay + 1, [
        "k...kkkkkk...k",
        "kk.kKKKKKKk.kk",
        ".kkKKWKKKKKkk.",
        "...kKKKKKKk...",
        "....kKKKKk....",
        ".....kKKk.....",
        "......kk......",
        "....kkkkkk....",
        "...kKKKKKKk...",
    ], {"k": "yk", "K": "yt0", "W": "ywh"})
    put(M, ax + 9, ay + 4, [
        "..vv.",
        ".vVv.",
        "ggGg.",
        "gGgGg",
        ".gGg.",
        ".gg..",
    ], {"v": "yv1", "V": "yv2", "g": "yg0", "G": "yg1"})
    put(M, ax + 32, ay + 4, ["..cc....", ".cCCc...", "cCCCCcc.", ".cCCCCCc", "..ccCCc.", "....cc.."],
        {"c": "yc1", "C": "yc2"})
    return s


def entry_pieces():
    out = []
    keys = ["base", "torch_top", "torch", "krater", "ivy_pot", "thyrsoi_top", "thyrsoi",
            "mat_l", "mat", "mat_r", "bench_l", "bench_r", "jars"]
    s = struct("entry", "The entry: the god's image's base, torches, the doormat", 7, 2,
               walk=["XXXXXXX", "SSSXXX."],
               names=cells(keys, 7),
               notes="`base` is the low stone base inside the door where the god's old "
                     "wooden image stands (an object on top of it). `torch_top` over `torch`: "
                     "a tall bronze torch, burning. `krater`: a wine krater painted in black "
                     "figure. `ivy_pot`. `thyrsoi_top` over `thyrsoi`: a stand of ivy-tipped "
                     "staves. `bench_l`/`bench_r` a marble bench. `jars` two wine jars. The "
                     "doormat (`mat_l`, `mat`, `mat_r`) is MB_SOUTH_ARROW_WARP: a warp on each.")
    L, M = s.B, s.M
    pos = s.names
    for k in keys:
        cx, cy = pos[k]
        flag(L, cx * 16, cy * 16, (cx + cy) % 3)
    cx, cy = pos["base"]
    put(M, cx * 16 + 1, cy * 16 + 6, [
        ".kkkkkkkkkkkk.",
        "kQQQQQQQQQQQQk",
        "kqqqqqqqqqqqqk",
        "kqqqqqqqqqqqqk",
        "kQQQQQQQQQQQQk",
        "kqqqvvqqqqqqqk",
        "kqqvVVvqqvqqqk",
        "kkkkkkkkkkkkkk",
        ".kkkkkkkkkkkk.",
    ], {"k": "yq0", "Q": "yq4", "q": "yq2", "v": "yv1", "V": "yv2"})
    cx, cy = pos["torch_top"]
    put(M, cx * 16 + 4, cy * 16 + 2, [
        "...ff...",
        "..fFFf..",
        ".fFWWFf.",
        ".fFWWFf.",
        "..fFFf..",
        "kzzzzzzk",
        ".kZZZZk.",
        "..kzzk..",
        "...zz...",
        "...zz...",
        "...zz...",
        "...zZ...",
        "...zZ...",
        "...zZ...",
    ], {"f": "yf1", "F": "yf2", "W": "yf3", "k": "yz0", "z": "yz1", "Z": "yz3"})
    cx, cy = pos["torch"]
    put(M, cx * 16 + 4, cy * 16, [
        "...zZ...",
        "...zZ...",
        "...zZ...",
        "...zZ...",
        "..kzZk..",
        "...zZ...",
        "...zZ...",
        "...zZ...",
        "..zzZz..",
        ".z.zZ.z.",
        "z..zZ..z",
        "z..zz..z",
        "kk.kk.kk",
    ], {"k": "yz0", "z": "yz1", "Z": "yz3"})
    cx, cy = pos["krater"]
    put(M, cx * 16 + 1, cy * 16 + 1, [
        "kkkkkkkkkkkkkk",
        "kttttttttttttk",
        ".kkkkkkkkkkkk.",
        "..kTTTTTTTTk..",
        "kkkTkkTTkkTkkk",
        "k.kTkkkTkkTk.k",
        "kkkTTkkkkTTkkk",
        "..kTTTTTTTTk..",
        "...kkkkkkkk...",
        "....kTTTTk....",
        ".....kTTk.....",
        "......kk......",
        "....kkkkkk....",
        "...kTTTTTTk...",
    ], {"k": "yk", "t": "yt1", "T": "yt2"})
    cx, cy = pos["ivy_pot"]
    put(M, cx * 16 + 1, cy * 16, [
        "...v..vV..v...",
        "..vVv.vVv.Vv..",
        ".vVvVvVvVvVvv.",
        "vVv.vVVvVv.vVv",
        ".v.vVvVVvVv.v.",
        "...vVvVvVv....",
        "..kttttttttk..",
        "..kTTTTTTTTk..",
        "...kTTTTTTk...",
        "...kTttttTk...",
        "...ktTTTTtk...",
        "....kttttk....",
        "....kkkkkk....",
    ], {"v": "yv1", "V": "yv2", "k": "yz0", "t": "yt1", "T": "yt2"})
    for k, rows in (("thyrsoi_top", [
            ".v...v....v.....",
            "vVv.vVv..vVv....",
            ".v...v....v.....",
            ".w...w....w.....",
            ".w...w....w.....",
            "..w..w...w......",
            "..w..w...w......",
            "..w..w...w......",
            "..w..w...w......",
            "...w.w..w.......",
            "...w.w..w.......",
            "...w.w..w.......",
            "...w.w..w.......",
            "...w.w..w.......",
            "...w.w..w.......",
            "...w.w..w.......",
            ]), ("thyrsoi", [
            "...w.w..w.......",
            "...w.w..w.......",
            "..kkkkkkkkk.....",
            "..kWWWWWWWk.....",
            "..kwwwwwwwk.....",
            "..kwwwwwwwk.....",
            "..kWWWWWWWk.....",
            "..kwwwwwwwk.....",
            "..kkkkkkkkk.....",
            ])):
        cx, cy = pos[k]
        put(M, cx * 16 + 3, cy * 16, rows, {"v": "yv1", "V": "yv2", "w": "yw3", "W": "yw4", "k": "yw0"})
    # the doormat: a wine-red rug with a gilt meander
    for k in ("mat_l", "mat", "mat_r"):
        cx, cy = pos[k]
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                c = "yc1"
                if y in (2, 13):
                    c = "yo0"
                elif 4 <= y <= 11 and (x + (y // 4) * 2) % 6 == 0:
                    c = "yo1"
                elif y in (0, 15):
                    c = "yc0"
                if k == "mat_l" and x < 2:
                    c = "yc0" if x == 0 else "yo0"
                if k == "mat_r" and x > 13:
                    c = "yc0" if x == 15 else "yo0"
                L.px(ox + x, oy + y, c)
    bench = [
        "................................",
        ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
        "kQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQk",
        "kqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk",
        "kqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk",
        "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
        "..kQqk....................kQqk..",
        "..kqqk....................kqqk..",
        "..kqqk....................kqqk..",
        "..kkkk....................kkkk..",
    ]
    cx, cy = pos["bench_l"]
    put(M, cx * 16, cy * 16 + 3, bench, {"k": "yq0", "Q": "yq4", "q": "yq2"})
    cx, cy = pos["jars"]
    for jx in (1, 8):
        put(M, cx * 16 + jx, cy * 16 + 2, [
            "..kk..",
            ".kttk.",
            "kTTTTk",
            "kTttTk",
            "kTTTTk",
            "kTTTTk",
            ".kTTk.",
            "..kk..",
            ".kkkk.",
        ], {"k": "yk", "t": "yt1", "T": "yt2"})
    out.append(s)
    return out


# --------------------------------------------------------------------------
# The wings: the program, trunks, rails, lamps, the satyrs' corner
# --------------------------------------------------------------------------

def program_stand(M, ox, oy, torn=False):
    rows = [
        "..kkkkkkkkkkkk..",
        "..kPPPPPPPPPPk..",
        "..kPllllllllPk..",
        "..kPPPPPPPPPPk..",
        "..kPllllllPPPk..",
        "..kPPPPPPPPPPk..",
        "..kPlllllllPPk..",
        "..kPPPPPPPPPPk..",
        "..kkkkkkkkkkkk..",
        ".kwwwwwwwwwwwwk.",
        "..kkkkkkkkkkkk..",
        "......kwwk......",
        "......kwWk......",
        ".....kkwWkk.....",
        "....kwwwwwwk....",
        "....kkkkkkkk....",
    ]
    if torn:
        rows[5] = "..kPPPkPPkPPPk.."
        rows[6] = "..kPk.k..kPk.k.."
        rows[7] = "..kk.......k...."
        rows[8] = "................"
        rows[9] = ".kwwwwwwwwwwwwk."
    put(M, ox, oy, rows, {"k": "yw0", "P": "yw5", "l": "yw1", "w": "yw3", "W": "yw4"})


def props_pieces():
    keys = ["program", "program_torn", "trunk_l", "trunk_r", "rail_l", "rail_r", "basket",
            "flats", "lamp", "stool", "goatskins_l", "goatskins", "goatskins_r", "hay",
            "corner_planks", "wigs"]
    s = struct("wings", "The wings: the program, trunks, rails and the satyrs' corner", 8, 2,
               walk=["XXXXXXXX", "XXXXXX.X"],
               names=cells(keys, 8),
               notes="`program` is the act's program on a reading stand (`program_torn`: Act "
                     "III's, the scroll torn off below). A costume `trunk_l`/`_r`, a costume "
                     "`rail_l`/`_r` hung with robes, a `basket` of props, stacked scenery "
                     "`flats`, an oil `lamp` on a stand, a `stool`, a `wigs` stand. The "
                     "satyrs' corner (Act II's alcove): its back wall hung with goatskins "
                     "(`goatskins_l`, `goatskins`, `goatskins_r`) under a `cap`, a `hay` bale, "
                     "and `corner_planks` to walk on.")
    L, M = s.B, s.M
    pos = s.names
    for k in keys:
        cx, cy = pos[k]
        boards(L, cx * 16, cy * 16, "wings", (cx + cy) % 2)
    program_stand(M, pos["program"][0] * 16, pos["program"][1] * 16)
    program_stand(M, pos["program_torn"][0] * 16, pos["program_torn"][1] * 16, torn=True)
    # the trunk: 2 wide
    cx, cy = pos["trunk_l"]
    rows = [
        "................................",
        ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
        "kwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwk",
        "kWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWk",
        "kkkkkkkkkkkkkkkoOkkkkkkkkkkkkkkk",
        "kwwiwwwwwwwwwwwoOwwwwwwwwwwwiwwk",
        "kwwiwwwwwwwwwwwkkwwwwwwwwwwwiwwk",
        "kwwiwwwwwwwwwwwwwwwwwwwwwwwwiwwk",
        "kWWiWWWWWWWWWWWWWWWWWWWWWWWWiWWk",
        "kwwiwwwwwwwwwwwwwwwwwwwwwwwwiwwk",
        "kwwiwwwwwwwwwwwwwwwwwwwwwwwwiwwk",
        "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
        ".kk..........................kk.",
    ]
    put(M, cx * 16, cy * 16 + 2, rows, {"k": "yw0", "w": "yw2", "W": "yw3", "i": "yir",
                                        "o": "yo0", "O": "yo1"})
    # the costume rail: robes on a pole
    cx, cy = pos["rail_l"]
    rows = [
        "k..............................k",
        "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
        "k.cc.cccc.aaaa.CCCC.cccc.aa.cc.k",
        "k.cc.cCcc.aAaa.CcCC.cCcc.aA.cc.k",
        "k.cc.cCcc.aAaa.CcCC.cCcc.aA.cc.k",
        "k.cc.cCcc.aAaa.CcCC.cCcc.aA.cc.k",
        "k.cc.cCcc.aAaa.CcCC.cCcc.aA.cc.k",
        "k.cc.cCcc.aAaa.CcCC.cCcc.aA.cc.k",
        "k.c..cCcc.aAa..CcC..cCc..aA..c.k",
        "k....cc...aa...Cc...cc....a....k",
        "k..............................k",
        "kk............................kk",
    ]
    put(M, cx * 16, cy * 16 + 3, rows, {"k": "yw1", "c": "yc2", "C": "yc3", "a": "ya1",
                                        "A": "ym1"})
    cx, cy = pos["basket"]
    put(M, cx * 16 + 1, cy * 16 + 1, [
        "..v.....m.....",
        ".vVv...mmm....",
        "..w...mKmKm...",
        "..w...mmmmm...",
        ".kkkkkkkkkkkk.",
        "kwWwWwWwWwWwWk",
        "kWwWwWwWwWwWwk",
        "kwWwWwWwWwWwWk",
        "kWwWwWwWwWwWwk",
        ".kwWwWwWwWwWk.",
        ".kkkkkkkkkkkk.",
    ], {"v": "yv1", "V": "yv2", "w": "yw3", "W": "yw4", "k": "yw1", "m": "yo1", "K": "yw1"})
    cx, cy = pos["flats"]
    put(M, cx * 16 + 1, cy * 16, [
        "..kkkkkkkk....",
        "..kvvvvvvk....",
        ".kkvVvvVvkk...",
        ".kwkvvvvvkwk..",
        "kwwkvVvvvkwwk.",
        "kwwkvvvVvkwwk.",
        "kwwkvvvvvkwwk.",
        "kwwkvVvvvkwwk.",
        "kwwkvvvvvkwwk.",
        "kwwkvvvVvkwwk.",
        "kwwkvvvvvkwwk.",
        "kwwkkkkkkkwwk.",
        "kwwwwwwwwwwwk.",
        "kkkkkkkkkkkkk.",
    ], {"k": "yw0", "w": "yw2", "v": "yv1", "V": "yv2"})
    cx, cy = pos["lamp"]
    put(M, cx * 16 + 4, cy * 16, [
        "...ff...",
        "..fWf...",
        "..fFf...",
        "kzzzzzk.",
        ".kzzzk..",
        "...z....",
        "...z....",
        "...z....",
        "...z....",
        "...z....",
        "...z....",
        "..zzz...",
        ".z.z.z..",
        "z..z..z.",
        "k..k..k.",
    ], {"f": "yf1", "F": "yf2", "W": "yf3", "k": "yz0", "z": "yz2"})
    cx, cy = pos["stool"]
    put(M, cx * 16 + 3, cy * 16 + 4, [
        ".kkkkkkkk.",
        "kWWWWWWWWk",
        "kwwwwwwwwk",
        ".kkkkkkkk.",
        ".kw....wk.",
        ".kw....wk.",
        ".kw....wk.",
        ".kk....kk.",
    ], {"k": "yw0", "w": "yw2", "W": "yw4"})
    cx, cy = pos["wigs"]
    put(M, cx * 16 + 3, cy * 16, [
        "..kkkkkk..",
        ".kKKKKKKk.",
        "kKkKKKKkKk",
        "kKmmmmmmKk",
        "kKmmmmmmKk",
        "kK.mmmm.Kk",
        "kK..mm..Kk",
        ".k..ww..k.",
        "....ww....",
        "....ww....",
        "....ww....",
        "...wwww...",
        "..wwwwww..",
        "..kkkkkk..",
    ], {"k": "yk", "K": "yw1", "m": "ym1", "w": "yw2"})
    # the satyrs' corner: rough timber wall with goatskins
    for k in ("goatskins_l", "goatskins", "goatskins_r"):
        cx, cy = pos[k]
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                c = "yw1" if x % 5 else "yw0"
                if (x * 3 + y * 7) % 13 == 0:
                    c = "yw2"
                if y >= 14:
                    c = ("yw0", "yk")[y - 14]
                L.px(ox + x, oy + y, c)
        if k == "goatskins_l":
            for y in range(16):
                for x in range(0, 3):
                    L.px(ox + x, oy + y, ("yw3", "yw2", "yw1")[x])
        if k == "goatskins_r":
            for y in range(16):
                for x in range(13, 16):
                    L.px(ox + x, oy + y, ("yw1", "yw2", "yw0")[x - 13])
        skin = [
            "a..aa..a",
            "aaAAAAaa",
            ".aAAAAa.",
            ".aAaAAa.",
            ".aAAAaa.",
            ".aAAAAa.",
            "aaAaAAaa",
            "a.aAAa.a",
            "...aa...",
        ]
        put(M, ox + 4, oy + 2, skin, {"a": "ya0", "A": "ya1"})
        if k == "goatskins":
            put(M, ox + 1, oy + 1, ["E..E", ".EE."], {"E": "ycr"} if False else {"E": "ym1"})
    cx, cy = pos["hay"]
    put(M, cx * 16 + 1, cy * 16 + 3, [
        "..wwWwwWwwWw..",
        ".wWwwWwWwwWwW.",
        "wWwWwwWwWwwWwW",
        "kkkkkkkkkkkkkk",
        "wWwwWwWwwWwWww",
        "wwWwwWwwWwwWwW",
        "kkkkkkkkkkkkkk",
        "wWwWwwWwWwwWww",
        ".wwWwWwwWwWww.",
        "..kkkkkkkkkk..",
    ], {"w": "yw4", "W": "yw5", "k": "yw2"})
    return s


def stage_boards(L, ox, oy, v=0):
    """The stage: wide boards of honey-coloured pine, polished."""
    for y in range(16):
        row, yy = y // 8, y % 8
        off = (0, 8)[(row + v) % 2]
        for x in range(16):
            xx = (x + off) % 16
            if yy == 7:
                c = "yw2"
            elif xx == 0:
                c = "yw3"
            elif yy == 0:
                c = "yw5"
            elif yy == 4 and (x + row * 3) % 7 < 3:
                c = "yw3"
            else:
                c = "yw4"
            L.px(ox + x, oy + y, c)


def deck_boards(L, ox, oy, v=0):
    """The skene roof: weathered planks running north-south, iron-nailed."""
    for x in range(16):
        col, xx = x // 4, x % 4
        off = ((0, 10, 5, 13) if v == 0 else (6, 1, 12, 3))[col]
        for y in range(16):
            yy = (y + off) % 16
            if xx == 3 or yy == 0:
                c = "yw0"
            elif xx == 0:
                c = "yw3"
            else:
                c = "yw2"
            if xx in (1, 2) and (y * 3 + col * 7 + v) % 19 == 0:
                c = "yw1"
            if yy == 1 and xx == 1:
                c = "yir"
            L.px(ox + x, oy + y, c)


FIGURE = [
    "..ooo..",
    ".oHHHo.",
    "oHHHHHo",
    "oHKHKHo",
    "oHHHHHo",
    "oHHKHHo",
    ".oHKHo.",
    "..ooo..",
    ".bBBBb.",
    "bBBBBBb",
    "bBBBBBb",
]


def figure_rows(kind):
    rows = [list(r) for r in FIGURE]
    if "hair" in kind:
        rows[0] = list("..kkk..")
        rows[1] = list(".kkkkk.")
        rows[2] = list("okHHHko")
    if "wreath" in kind:
        rows[0] = list(".v.v.v.")
        rows[1] = list("vVvVvVv")
    if "white" in kind:
        rows = [["W" if c == "H" else c for c in r] for r in rows]
    if "red" in kind:
        rows = [["R" if c == "B" else ("r" if c == "b" else c) for c in r] for r in rows[:8]] + \
               [["R" if c == "B" else ("r" if c == "b" else c) for c in r] for r in rows[8:]]
    if "arms" in kind:
        for y in range(1, 8):
            rows[y][0] = "b" if y > 1 else "o"
            rows[y][6] = "b" if y > 1 else "o"
        rows[0][0] = "o"
        rows[0][6] = "o"
    return ["".join(r) for r in rows]


def plank_wall(L, ox, oy):
    for y in range(16):
        for x in range(16):
            c = "yw1" if x % 5 else "yw0"
            if (x * 3 + y * 7) % 13 == 0:
                c = "yw2"
            if y >= 14:
                c = ("yw0", "yk")[y - 14]
            L.px(ox + x, oy + y, c)


MAST = ("yw0", "yw3", "yw4", "yw3", "yw2", "yw2", "yw1", "yw0")   # x 4..11, lit from the left


def mast(M, ox, oy, y0=0, y1=16):
    for y in range(y0, y1):
        for i, c in enumerate(MAST):
            M.px(ox + 4 + i, oy + y, c)


def beam(L, ox, oy, y0=0, y1=16):
    """The crane's boom swung toward the stage, seen from above: a squared timber
    with iron straps."""
    for y in range(y0, y1):
        for i, c in enumerate(("yw0", "yw3", "yw4", "yw4", "yw3", "yw2", "yw1", "yw0")):
            L.px(ox + 4 + i, oy + y, c)
        if (y - y0) % 6 == 3:
            for i in range(1, 7):
                L.px(ox + 4 + i, oy + y, "yir")


def footlight(M, ox, oy):
    """A clay oil lamp at the stage's front edge, burning."""
    put(M, ox + 4, oy + 1, [
        "....f...",
        "...fFf..",
        "...fWf..",
        ".kkzzkk.",
        "kzZZZZzk",
        "kzzzzzzk",
        ".kkkkkk.",
    ], {"f": "yf1", "F": "yf2", "W": "yf3", "k": "yz0", "z": "yz1", "Z": "yz3"})


def build():
    structs = [floor_pieces()]
    structs += wall_pieces()
    structs.append(back_wall_pieces())
    structs += skene_pieces()
    structs.append(rack_pieces())
    structs.append(tier_pieces())
    structs.append(stair_pieces())
    structs.append(deck_pieces())
    structs.append(orchestra_pieces())
    structs += entry_pieces()
    structs.append(props_pieces())
    return structs
