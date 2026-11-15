"""The land around the harbors, for gTileset_Kirrha: Parnassos's grey crags, the
Phaidriades with Delphoi's roofs high in their cleft, laurels and plane trees,
the pilgrims' gate on the sacred road, the low fence of Apollo's plain, the
altar of Zeus the Assembler, stone steps, the rock in Kirrha's bay and the
drowned roofs of Helike off Aigion's quay.

Light comes from the top left, as everywhere in Aethos.
"""
from __future__ import annotations

import math
import random

import numpy as np

import kirrha_lib as KL
from kirrha_lib import Layer, struct

SEC = "land"


# --------------------------------------------------------------------------
# The crag kit: a grey limestone cliff band of any length and height
# --------------------------------------------------------------------------

def _grass_fill(L, x0, y0, w, h):
    """Aethos-like grass, for the few drawn-ground cells beside a crag's end."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            h_ = (x * 7 + y * 13) % 23
            L.px(x, y, "gr2" if h_ == 0 else ("gr1" if h_ in (5, 11) else "gr0"))


def _rim(L, x0, y0, w, seed=1):
    """The cliff's top: grass running to a ragged lip. Draws the lip from y0 down 5
    px (its dip varies along the 32 px period, so a long rim reads as weathered)."""
    for x in range(x0, x0 + w):
        X = x % 32
        dip = (0, 1, 1, 0, 0, 1, 2, 1, 0, 0, 0, 1, 1, 0, 1, 2, 2, 1, 0, 0, 0, 1, 0, 0,
               1, 1, 0, 0, 1, 2, 1, 0)[X]
        top = y0 + dip
        for yy in range(y0 - 1, top):
            L.px(x, yy, None)
        L.px(x, top, "pg1")
        L.px(x, top + 1, "pg5")
        L.px(x, top + 2, "pg4")
        L.px(x, top + 3, "pg4" if X % 7 else "pg5")
        L.px(x, top + 4, "pg2")


# the kit's columns: left end, mid at even map columns, mid at odd ones, right end;
# each with the texture phase that meets its neighbor
_COLS = ((0, 0), (16, 16), (32, 16), (48, 32))


def _flank(y):
    """Whether a cliff end's flank is drawn at kit row y (not on the feet's scree)."""
    return y >= 10 and not (54 <= y < 64 or y >= 70)


def cliff_kit():
    """A cliff band of any length and height: rim, two face rows (the texture
    repeats every 32 px down as well as across) and two feet, by left end, two mid
    columns and right end."""
    s = struct("cliff", "Parnassos cliff band: rim, faces and feet", 4, 5,
               walk=["XXXX"] * 5,
               notes="A grey limestone cliff, bedded and jointed, of any length and height. "
                     "Columns: left end, mid (even map column), mid (odd map column), right "
                     "end. Rows: 0 the rim (aethos grass above the lip); 1 face A, 2 face B "
                     "(stack A, B, A, B... under the rim); 3 the foot after a B row, 4 the "
                     "foot after an A row (scree on aethos grass). All impassable. "
                     "tools/ichor/maps/harbors.py's cliff() picks the parts.",
               section=SEC)
    KL.ground(s, "grass", [(x, y) for x in range(4) for y in (0, 3, 4)])
    KL.ground(s, "none", [(x, y) for x in range(4) for y in (1, 2)])
    M, B = s.M, s.B
    for (cx, ox) in _COLS:
        KL.crag_face(M, cx, 9, 16, 7, ox=ox, oy=16)
        KL.crag_face(B, cx, 16, 16, 32, ox=ox, oy=16)
        for fy in (48, 64):
            KL.crag_face(M, cx, fy, 16, 6, ox=ox, oy=16)
            for x in range(cx, cx + 16):
                M.px(x, fy + 6, "pg1")
                M.px(x, fy + 7, "pg0" if x % 5 else "pg1")
    _rim(M, 0, 8, 64)
    rnd = random.Random(7)
    for fy in (48, 64):
        for x in range(2, 62, 5):
            for k in range(rnd.randint(1, 2)):
                yy = fy + 9 + rnd.randint(0, 4)
                xx = x + rnd.randint(-1, 2)
                big = rnd.random() < 0.4
                if big:
                    M.blit([" 54 ", "5432", " 21 "], {"5": "pg5", "4": "pg4", "3": "pg3",
                                                     "2": "pg2", "1": "pg1"}, xx - 1, yy - 1)
                else:
                    M.blit(["43", "21"], {"4": "pg4", "3": "pg3", "2": "pg2", "1": "pg1"}, xx, yy)
    KL.scrub(M, 20, 6)
    KL.scrub(M, 37, 7, big=True)
    # the left end: grass west of a lit, rounded flank; a joint at its east edge
    for y in range(0, 80):
        L = B if 16 <= y < 48 else M
        if y >= 9:
            for x in range(0, 4):
                L.px(x, y, None)
        if _flank(y):
            L.px(4, y, "pg1")
            L.px(5, y, "pg5")
            L.px(6, y, "pg4")
        if 10 <= y < 48:
            jx = 14 + (1 if math.sin(y * 0.9) > 0.3 else 0)
            L.px(jx, y, "pg0")
            L.px(jx + 1, y, "pg1")
            L.px(jx + 2, y, "pg4")
    # the right end: a shadowed flank, grass east of it; a joint at its west edge
    for y in range(0, 80):
        L = B if 16 <= y < 48 else M
        if y >= 9:
            for x in range(61, 64):
                L.px(x, y, None)
        if _flank(y):
            L.px(60, y, "pg1")
            L.px(59, y, "pg2")
        if 10 <= y < 48:
            jx = 48 + (1 if math.sin(y * 0.7 + 1) > 0.3 else 0)
            L.px(jx - 1, y, "pg1")
            L.px(jx, y, "pg0")
            L.px(jx + 1, y, "pg5")
    # the rim curls down at the ends
    for x in range(0, 6):
        for y in range(8, 12):
            M.px(x, y, None)
    M.blit(["1  ", "51 ", "451"], {"1": "pg1", "5": "pg5", "4": "pg4"}, 4, 9)
    M.blit(["  1", " 21", "121"], {"1": "pg1", "2": "pg2"}, 58, 9)
    # the face rows' end cells are drawn ground: grass behind the cleared flanks
    _grass_fill(B, 0, 16, 4, 32)
    _grass_fill(B, 61, 16, 3, 32)
    s.names = {}
    for (i, col) in enumerate(("l", "m0", "m1", "r")):
        for (j, row) in enumerate(("rim", "faceA", "faceB", "footB", "footA")):
            s.names[f"{row}_{col}"] = (i, j)
    return s


def outcrop_small():
    """Two small grey rocks for the grass: a boulder with scrub, a low slab."""
    s = struct("rocks", "Small grey rocks", 2, 1, walk=["XX"],
               notes="On aethos grass: a rounded grey boulder with a tuft of scrub; a low "
                     "split slab.", section=SEC)
    KL.ground(s, "grass")
    M = s.M
    M.ellipse(2, 3, 14, 14, "pg3")
    M.ellipse(3, 3, 9, 8, "pg4")
    M.ellipse(4, 4, 6, 6, "pg5")
    M.ellipse(8, 9, 13, 13, "pg2")
    M.outline("pg1", region=(0, 0, 16, 16))
    KL.scrub(M, 9, 1)
    for x in range(3, 14):
        M.px(x, 15, "gr1")
    # the slab
    M.poly([(17, 9), (20, 6), (29, 5), (31, 8), (30, 13), (18, 13)], "pg3")
    M.hline(20, 29, 6, "pg5")
    M.hline(19, 30, 7, "pg4")
    M.line(24, 6, 25, 13, "pg1")
    M.outline("pg1", region=(16, 0, 16, 16))
    for x in range(18, 31):
        M.px(x, 14, "gr1")
    return s


# --------------------------------------------------------------------------
# The Phaidriades: two shining cliffs, the cleft, Delphoi's roofs, the falls
# --------------------------------------------------------------------------

def delphoi():
    """Delphoi's sanctuary, high in the cleft between the Phaidriades: the temple
    of Apollo's pediment and colonnade, a treasury, the terrace wall, all small
    and pale, on grey rock. 3x2."""
    s = struct("delphoi", "Delphoi's roofs high in the cleft", 3, 2, walk=["XXX", "XXX"],
               notes="The distant sanctuary between the Phaidriades: Apollo's temple with its "
                     "pediment and columns, a treasury, the polygonal terrace wall, on grey "
                     "rock. Impassable; set it above the sacred road's steps.", section=SEC)
    B, M = s.B, s.M
    KL.crag_face(B, 0, 0, 48, 32, ox=8)
    # the terrace: polygonal wall across the lower half
    M.rect(2, 18, 44, 8, "m2")
    for x in range(2, 46, 5):
        M.line(x, 18, x + 2, 25, "m4")
    M.hline(2, 45, 18, "m1")
    M.hline(2, 45, 25, "m4")
    M.hline(2, 45, 26, "ink")
    # temple of Apollo: pediment over six columns, on the terrace
    M.rect(10, 8, 26, 10, "m1")
    M.poly([(9, 8), (23, 2), (37, 8)], "m2")
    M.line(9, 8, 23, 2, "m4")
    M.line(23, 2, 37, 8, "m4")
    M.poly([(13, 7), (23, 3), (33, 7)], "tc1")
    M.hline(9, 37, 8, "m4")
    M.hline(9, 37, 9, "w0")
    for i, x in enumerate(range(11, 36, 4)):
        M.vline(x, 10, 16, "w0")
        M.vline(x + 1, 10, 16, "m3")
        M.vline(x + 2, 10, 16, "m4")
    M.hline(10, 36, 17, "m3")
    M.px(23, 1, "g1")
    M.px(23, 0, "g0")
    # a treasury to the left, lower: a little pedimented box
    M.rect(2, 12, 7, 6, "m2")
    M.poly([(1, 12), (5, 9), (9, 12)], "tc1")
    M.line(1, 12, 5, 9, "m4")
    M.line(5, 9, 9, 12, "m4")
    M.rect(4, 14, 2, 4, "m4")
    # the stoa of the Athenians to the right: a long low roof
    M.rect(38, 13, 8, 5, "m1")
    M.rect(38, 11, 8, 2, "tc1")
    M.hline(38, 45, 11, "tc2")
    for x in range(39, 46, 2):
        M.vline(x, 14, 17, "m3")
    return s


def cleft():
    """The cleft between the two cliffs: its two inner walls, deep shadow, the
    sacred road's stone steps climbing through it. 2x2, the steps walkable."""
    s = struct("cleft", "The cleft: the sacred road's steps between the cliffs", 2, 2,
               walk=["..", ".."],
               notes="The sacred road climbing the cleft between the Phaidriades in worn "
                     "stone steps, the cliffs' inner walls in shadow on either side. Walkable; "
                     "it runs from the pilgrims' gate up toward Delphoi.", section=SEC)
    B = s.B
    # steps: treads lit, risers dark, worn in the middle
    for y in range(32):
        for x in range(32):
            Y = y % 6
            c = "pg3" if Y < 3 else ("pg4" if Y == 3 else ("pg2" if Y == 4 else "pg1"))
            if 10 <= x <= 21 and Y < 3:
                c = "pg4" if (x + y) % 4 else "pg5"
            B.px(x, y, c)
    # the inner walls: shadow at the left and right
    for y in range(32):
        for x in range(0, 4):
            B.px(x, y, "pg1" if x < 3 else "pg2")
        B.px(0, y, "pg0")
        for x in range(28, 32):
            B.px(x, y, "pg0" if x > 29 else "pg1")
    KL.scrub(B, 1, 5)
    KL.scrub(B, 26, 21)
    return s


def laurel():
    """Apollo's laurel: a dense, dark, glossy cone-round tree, 2x2. The crown's top
    row is on the top layer."""
    s = struct("laurel", "Laurel tree", 2, 2, walk=["TT", "XX"],
               notes="Apollo's bay laurel on aethos grass: a dense dark crown, glossy lit "
                     "leaves, a short grey trunk. The top row is drawn over the player.",
               section=SEC)
    KL.ground(s, "grass")
    T, M = s.T, s.M
    crown = Layer(32, 32)
    rnd = random.Random(11)
    # the crown: an egg shape, leaf clusters shaded dark at the bottom right
    cx, cy, rx, ry = 15.5, 13.0, 13.0, 13.0
    for y in range(32):
        for x in range(32):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            d = dx * dx + dy * dy
            wob = 0.08 * math.sin(x * 1.3 + y * 0.7)
            if d <= 1.0 + wob and y < 27:
                t = (x - cx) * 0.6 + (y - cy) * 0.9
                c = "lr1"
                if t > 7:
                    c = "lr0"
                elif t < -8:
                    c = "lf1"
                crown.px(x, y, c)
    # leaf texture: little glossy leaves, lit toward the top left
    for _ in range(140):
        x, y = rnd.randint(3, 28), rnd.randint(1, 25)
        if crown.get(x, y) is None:
            continue
        t = (x - cx) * 0.6 + (y - cy) * 0.9
        if t < -2:
            crown.px(x, y, "lf2" if rnd.random() < 0.4 else "lf1")
            crown.px(x + 1, y, "lf1")
        elif t > 6:
            crown.px(x, y, "ink" if rnd.random() < 0.15 else "lr0")
        else:
            crown.px(x, y, "lr0")
            crown.px(x, y - 1, "lf1")
    crown.outline("ink")
    # trunk
    for y in range(25, 31):
        crown.px(14, y, "tk1")
        crown.px(15, y, "tk2")
        crown.px(16, y, "tk1")
        crown.px(17, y, "tk0")
    crown.hline(13, 18, 31, "tk0")
    for x in range(8, 24):
        if crown.get(x, 30) is None:
            crown.px(x, 30, "gr1")
    for y in range(32):
        for x in range(32):
            c = crown.get(x, y)
            if c:
                (T if y < 16 else M).px(x, y, c)
    return s


def plane(hollow=False):
    """An old plane tree, 3x3: a broad pale-green crown of big lobed leaves over a
    mottled cream-and-grey trunk. The hollow variant has a dark hole with bees, where
    the wild honey is."""
    key = "plane_hollow" if hollow else "plane"
    s = struct(key, "Old plane tree" + (", hollow" if hollow else ""), 3, 3,
               walk=["TTT", "XXX", ".X."],
               notes="One of the ring of old planes round the altar of Zeus at Aigion, on "
                     "aethos grass. The crown's top row is drawn over the player; the roots' "
                     "outer cells are walkable." + (" A hollow in the trunk, bees at its "
                                                    "mouth (the hidden Honey)." if hollow else ""),
               section=SEC)
    KL.ground(s, "grass")
    T, M = s.T, s.M
    L = Layer(48, 48)
    rnd = random.Random(31 if not hollow else 31)
    blobs = [(24, 15, 18, 13), (12, 20, 10, 9), (36, 20, 10, 9), (24, 8, 12, 8), (17, 26, 9, 6),
             (31, 26, 9, 6)]
    mask = np.zeros((48, 48), bool)
    for (bx, by, rx, ry) in blobs:
        yy, xx = np.mgrid[0:48, 0:48]
        mask |= ((xx - bx) / rx) ** 2 + ((yy - by) / ry) ** 2 <= 1
    mask[33:, :] = False
    # trunk first (under the crown)
    # a plane's bark flakes off in patches: cream, grey-green and olive, mottled,
    # lit on the left; the trunk a column flaring only at the roots
    for y in range(26, 47):
        spread = 0 if y < 43 else (y - 43)
        x0, x1 = 20 - spread, 27 + spread
        for x in range(x0, x1 + 1):
            u = (x - x0) / max(1, x1 - x0)
            c = "tk2" if u < 0.45 else "tk1"
            blot = ((x // 3) * 7 + (y // 4) * 5) % 9
            if blot == 0:
                c = "ov3" if u < 0.5 else "ov2"
            elif blot == 4 and u > 0.3:
                c = "tk2"
            if u > 0.82:
                c = "tk0"
            L.px(x, y, c)
        L.px(x0 - 1, y, "ink")
        L.px(x1 + 1, y, "ink")
    for x in range(15, 34):
        L.px(x, 47, "tk0" if 18 < x < 30 else "gr1")
    # roots
    L.line(19, 44, 15, 47, "tk1")
    L.line(28, 44, 32, 47, "tk0")
    if hollow:
        L.ellipse(21, 33, 26, 40, "ink")
        L.ellipse(22, 34, 25, 39, "tk0")
        L.px(23, 36, "ink")
        for (bx, by) in ((27, 32), (29, 35), (19, 31), (28, 38)):
            L.px(bx, by, "ink")
            L.px(bx + 1, by, "g1" if False else "gr2")
    # crown
    for y in range(48):
        for x in range(48):
            if mask[y, x]:
                t = (x - 24) * 0.5 + (y - 16) * 0.9
                c = "lf1"
                if t > 9:
                    c = "ov1"
                elif t > 4:
                    c = "ov2"
                elif t < -9:
                    c = "lf2"
                L.px(x, y, c)
    # lobed leaf clusters: lit tops, shadow undersides
    for _ in range(90):
        x, y = rnd.randint(4, 44), rnd.randint(1, 31)
        if not mask[y, x]:
            continue
        t = (x - 24) * 0.5 + (y - 16) * 0.9
        L.blit([" 2 ", "222", " 1 "] if t < 2 else [" 1 ", "111", " 0 "],
               {"2": "lf2", "1": "lf1" if t < 2 else "ov2", "0": "ov1"}, x - 1, y - 1)
    edge = mask & ~(np.roll(mask, 1, 0) & np.roll(mask, -1, 0) & np.roll(mask, 1, 1) &
                    np.roll(mask, -1, 1))
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "ov0" if y > 14 else "ov1")
    for y in range(48):
        for x in range(48):
            c = L.get(x, y)
            if c:
                (T if y < 16 else M).px(x, y, c)
    return s


# --------------------------------------------------------------------------
# The sacred road's gate, the fence of Apollo's plain
# --------------------------------------------------------------------------

def pilgrims_gate():
    """A wooden gate across the sacred road between two stone piers, shut, a
    laurel wreath tied at its middle. 4x2: pier, leaf, leaf, pier."""
    s = struct("gate", "The pilgrims' gate on the sacred road", 4, 2,
               walk=["XXXX", "XXXX"],
               notes="Route 28's closed gate at Kirrha's north edge: two dressed piers with "
                     "laurel on their caps, two plank leaves barred shut, a wreath at the "
                     "join. On aethos path (the road runs on behind it). All impassable until "
                     "Act III. The right pier's foot has a crack (the hidden Bronze Obol).",
               section=SEC)
    KL.ground(s, "path", [(1, 0), (2, 0), (1, 1), (2, 1)])
    KL.ground(s, "grass", [(0, 0), (3, 0), (0, 1), (3, 1)])
    M = s.M
    # piers (crag group), each one cell wide, 2 tall
    for px in (0, 48):
        M.rect(px + 2, 6, 12, 26, "pg3")
        for y in range(6, 32, 6):
            M.hline(px + 2, px + 13, y, "pg1")
            M.hline(px + 3, px + 12, y + 1, "pg4")
        M.vline(px + 2, 6, 31, "pg1")
        M.vline(px + 3, 7, 30, "pg5")
        M.vline(px + 13, 6, 31, "pg0")
        M.vline(px + 12, 7, 30, "pg2")
        # cap
        M.rect(px + 1, 2, 14, 4, "pg4")
        M.hline(px + 1, px + 14, 2, "pg5")
        M.hline(px + 1, px + 14, 5, "pg1")
        M.vline(px + 1, 2, 5, "pg1")
        M.vline(px + 14, 2, 5, "pg0")
        KL.scrub(M, px + 5, 0)
    # the crack at the right pier's foot
    M.line(54, 25, 56, 31, "pg0")
    M.px(57, 29, "pg0")
    # the leaves (wood group): planks, two bars, iron studs; drawn in cells 1-2
    for x in range(16, 48):
        for y in range(4, 31):
            X = (x - 16) % 6
            c = "wd2" if X not in (0, 5) else ("wd1" if X == 5 else "wd3")
            M.px(x, y, c)
        M.px(x, 3, "wd3")
        M.px(x, 31, "wd0")
        M.px(x, 30, "wd1")
    M.vline(31, 3, 31, "wd0")
    M.vline(32, 3, 31, "ink")
    for by in (9, 22):
        M.rect(16, by, 32, 3, "wd1")
        M.hline(16, 47, by, "wd3")
        M.hline(16, 47, by + 2, "wd0")
        for sx in (19, 27, 36, 44):
            M.px(sx, by + 1, "ink")
    # the wreath where the leaves meet (wood group carries the laurel green)
    M.ellipse(27, 12, 36, 20, "lv1")
    M.ellipse(29, 14, 34, 18, "wd2")
    for (wx, wy) in ((28, 13), (35, 13), (27, 16), (36, 17), (30, 19), (33, 19), (31, 12)):
        M.px(wx, wy, "rp")
    M.px(31, 20, "rd")
    M.px(32, 21, "rd")
    M.px(31, 22, "rd")
    return s


def fence():
    """The low post-and-rail fence of Apollo's plain: a run west-east, its ends,
    a run north-south, and a corner. On aethos grass."""
    s = struct("fence", "Low fence of Apollo's plain", 5, 1, walk=["XXXXX"],
               notes="Weathered post-and-rail on aethos grass. Cells: west end, run, east end, "
                     "north-south run, south-west corner. Impassable.", section=SEC)
    KL.ground(s, "grass")
    M = s.M

    def post(x, y0=4):
        M.rect(x, y0, 3, 11, "wd2")
        M.vline(x, y0, y0 + 10, "wd3")
        M.vline(x + 2, y0, y0 + 10, "wd0")
        M.hline(x, x + 2, y0, "wd3")
        M.hline(x - 1, x + 3, y0 + 11, "kt" if False else "wd0")

    def rails(x0, x1):
        for ry in (6, 10):
            M.hline(x0, x1, ry, "wd3")
            M.hline(x0, x1, ry + 1, "wd1")
    # west end, run, east end
    rails(8, 15)
    post(6)
    rails(16, 31)
    post(22)
    rails(32, 40)
    post(39)
    # north-south run: posts and a rail seen end-on, running the cell's height
    for y in range(0, 16):
        M.px(54, y, "wd3")
        M.px(55, y, "wd1")
        M.px(57, y, "wd3")
        M.px(58, y, "wd1")
    post(54, 2)
    # the corner: run from the west meets the north-south line
    rails(64, 72)
    for y in range(0, 12):
        M.px(70, y, "wd3")
        M.px(71, y, "wd1")
    post(69)
    return s


# --------------------------------------------------------------------------
# Aigion: the altar of Zeus, the terrace steps, the drowned roofs
# --------------------------------------------------------------------------

def zeus_altar():
    """The altar of Zeus the Assembler: a long marble altar on a step, an oak
    wreath and a bronze eagle on it, fire in its bowl. 2x2."""
    s = struct("zeus_altar", "Altar of Zeus the Assembler", 2, 2, walk=["XX", "XX"],
               notes="Aigion's altar in the ring of planes: a marble altar on a stepped "
                     "base, a bronze eagle on the top, a fire burning, an oak wreath on its "
                     "front. On aethos grass. The bg event runs EventScript_IchorAltar_Zeus.",
               section=SEC)
    KL.ground(s, "grass")
    M, T = s.M, s.T
    # base step
    M.rect(1, 22, 30, 8, "m3")
    M.hline(1, 30, 22, "m1")
    M.hline(1, 30, 29, "m4")
    M.vline(1, 22, 29, "m4")
    M.vline(30, 22, 29, "m4")
    for x in range(1, 31):
        M.px(x, 30, "ink")
    # altar body
    M.rect(4, 9, 24, 13, "m2")
    M.hline(4, 27, 9, "w0")
    M.hline(4, 27, 10, "m1")
    M.vline(4, 9, 21, "m1")
    M.vline(27, 9, 21, "m4")
    M.hline(4, 27, 21, "m4")
    # volutes at the corners
    for vx in (3, 25):
        M.ellipse(vx, 6, vx + 4, 10, "m1")
        M.px(vx + 2, 8, "m4")
    # oak wreath on the front (market group has no leaf green: a bronze wreath)
    M.ellipse(11, 12, 20, 20, "g0")
    M.ellipse(13, 14, 18, 18, "m2")
    for (wx, wy) in ((12, 13), (19, 13), (11, 17), (20, 17), (15, 20)):
        M.px(wx, wy, "g1")
    # the fire and the eagle (middle layer: a borrowed-grass cell takes one upper layer)
    M.blit(["   r   ", "  rgr  ", " rgggr ", "  rgr  "], {"r": "rd", "g": "g1"}, 6, 3)
    M.blit(["  kk  ", " kbbk ", "kbbbbk", " k  k "], {"k": "ink", "b": "br"}, 19, 3)
    M.px(21, 3, "g1")
    return s


def steps():
    """Stone steps across a street climbing south (Aigion), 3 wide: west end, mid,
    east end. Walkable both ways."""
    s = struct("steps", "Stone steps up the street", 3, 1, walk=["..."],
               notes="Worn grey steps across a street that climbs southward: lit treads, "
                     "dark risers. Walkable. West end, mid, east end (grass beyond the ends "
                     "is aethos's).", section=SEC)
    B = s.B
    for y in range(16):
        for x in range(48):
            Y = y % 8
            c = "pg3" if Y < 4 else ("pg4" if Y == 4 else ("pg2" if Y < 7 else "pg1"))
            if (x * 5 + y * 3) % 17 == 0 and Y < 4:
                c = "pg4"
            B.px(x, y, c)
    for y in range(16):
        B.px(0, y, "pg1")
        B.px(1, y, "pg4")
        B.px(47, y, "pg0")
        B.px(46, y, "pg2")
    return s


def bay_rock():
    """Kirrha's rock in the bay: a low grey islet with a flat top you can stand on
    (from the water, with the Conch). 2x2 on aethos sea."""
    s = struct("bay_rock", "Rock in the bay", 2, 2, walk=["..", ".."],
               notes="A flat-topped grey rock awash in the gulf, foam at its foot, on aethos's "
                     "animated sea. Walkable from the water (Poseidon's Conch): the Big "
                     "Pearl's item ball sits on it.", section=SEC)
    KL.ground(s, "sea")
    M = s.M
    L = Layer(32, 32)
    L.poly([(4, 22), (3, 12), (8, 5), (16, 3), (25, 5), (29, 11), (29, 22), (24, 27), (8, 27)],
           "pg3")
    m = L.a[..., 3] > 0
    for y in range(32):
        for x in range(32):
            if not m[y, x]:
                continue
            c = "pg3"
            if y > 20:
                c = "sub2" if x < 24 else "sub0"
            elif x + y < 18:
                c = "pg4"
            if (x * 7 + y * 3) % 23 == 0:
                c = "sub2"
            L.px(x, y, c)
    L.outline("ink")
    for x in range(5, 28):
        L.px(x, 28, "w0" if x % 3 else "b3")
        if x % 4 == 1:
            L.px(x, 29, "b3")
    for y in range(8, 24, 3):
        L.px(1, y, "b3")
        L.px(30, y + 1, "w0")
    M.copy_from(L)
    return s


def drowned_roofs():
    """Helike under clear, still water off Aigion's quay: terracotta roofs and a
    bell-less tower, drowned and blue. 3x2, on aethos sea."""
    s = struct("drowned", "Helike's drowned roofs under clear water", 3, 2,
               walk=["XXX", "XXX"],
               notes="Roofs and a tower top under the water, seen through it: on aethos's "
                     "animated sea, so the gulf ripples round them. Water: elevation 1 and "
                     "surfable like the sea around (set by the map builder).", section=SEC)
    KL.ground(s, "sea")
    M = s.M

    def roof_shape(x, y, w, h):
        M.poly([(x, y + h), (x + 3, y), (x + w - 3, y), (x + w, y + h)], "sub1")
        for yy in range(y + 1, y + h, 2):
            M.hline(x + 2, x + w - 2, yy, "sub0")
        M.hline(x + 3, x + w - 3, y, "sub2")
    roof_shape(2, 3, 16, 7)
    roof_shape(20, 6, 14, 6)
    roof_shape(6, 18, 18, 8)
    roof_shape(30, 19, 14, 7)
    # the tower's top, square, a dark belfry opening
    M.rect(36, 2, 8, 10, "sub1")
    M.rect(38, 4, 4, 4, "b0")
    M.hline(36, 43, 2, "sub2")
    # a few weeds and fish shadows
    for (x, y) in ((25, 14), (12, 13), (40, 28)):
        M.px(x, y, "tq")
        M.px(x + 1, y + 1, "tq")
    return s


def well():
    """A village well: a round grey well-head, a timber frame and pulley, a bucket on
    its rope. 1x1 on grass."""
    s = struct("well", "Village well", 1, 1, walk=["X"],
               notes="A round limestone well-head with a timber frame and a bucket, on aethos "
                     "grass. Impassable.", section=SEC)
    KL.ground(s, "grass")
    M = s.M
    M.ellipse(1, 7, 14, 15, "pg3")
    M.ellipse(2, 7, 13, 11, "pg4")
    M.ellipse(4, 8, 11, 10, "pg0")
    M.hline(3, 12, 13, "pg2")
    M.hline(3, 12, 15, "pg1")
    M.outline("ink")
    M.vline(2, 1, 9, "pg1")
    M.vline(13, 1, 9, "pg1")
    M.hline(1, 14, 1, "pg2")
    M.hline(1, 14, 2, "pg1")
    M.vline(8, 3, 6, "lv0")
    M.rect(6, 5, 4, 3, "pg2")
    return s


def bench():
    """A long stone bench, for the grove's meetings ("shorter ones"). 2x1 on grass."""
    s = struct("bench", "Stone bench", 2, 1, walk=["XX"],
               notes="A long limestone bench on two blocks, on aethos grass, worn smooth. "
                     "Impassable.", section=SEC)
    KL.ground(s, "grass")
    M = s.M
    M.rect(1, 5, 30, 4, "pg4")
    M.hline(1, 30, 5, "pg5")
    M.hline(1, 30, 8, "pg2")
    M.rect(3, 9, 5, 5, "pg3")
    M.rect(24, 9, 5, 5, "pg3")
    M.vline(7, 9, 13, "pg1")
    M.vline(28, 9, 13, "pg1")
    M.outline("ink")
    for x in range(2, 30):
        M.px(x, 15, "gr1")
    return s


def build():
    return [cliff_kit(), outcrop_small(), delphoi(), cleft(), laurel(),
            plane(), plane(hollow=True), pilgrims_gate(), fence(), zeus_altar(), steps(),
            bay_rock(), drowned_roofs(), well(), bench()]
