"""Phikion's rock and the Minyans' stonework: crags and their scrub, the goat
path's east-facing ledges, the Sphinx's ledge, the Minyan dike with its sluice,
the Treasury of Minyas (its doorway and corbelled chamber), the walled islet
of Gla, the great herm, the Onchestos racing post, and turned earth for digs.
"""
from __future__ import annotations

import numpy as np

import kithairon_ground as KG
import kithairon_stone as KS
import kopais_lib as K
import kopais_marsh as M

SEC = "stone"
FULL = "1|11111111"
SOUTH_EDGE = "1|11100011"


def _cell(w=16, h=16):
    return K.A.Layer(w, h)


def _place(s, layer, cx, cy, src, rows=1, cols=1):
    s.layers[layer].a[cy * 16:(cy + rows) * 16, cx * 16:(cx + cols) * 16] = src.a


def grass(L, x0, y0, w=16, h=16):
    L.texture(K.GRASS, x0, y0, w, h)


# --------------------------------------------------------------------------
# Phikion's crags, scrub and ledges (rock group)
# --------------------------------------------------------------------------

def crag(phase=0):
    keys = M.wanted("crag")
    w = 8
    h = max(1, (len(keys) + w - 1) // w)
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = K.struct("crag", "Phikion's grey rock", w, h, SEC, walk=["X" * w] * h, names=names,
                 notes="Mount Phikion's grey limestone, seen from above with its south face "
                       "showing, on aethos grass (Kithairon's painter, so the two mountains "
                       "match). Impassable. Names are class keys; only `1` counts.")
    for n in range(w * h):
        k = keys[min(n, len(keys) - 1)]
        KG.paint_crag_cell(s.B, (n % w) * 16, (n // w) * 16, K.binary(k), KG.grass_floor)
    return s


def _bush(L, ox, oy, cx, cy, rx, ry, tones=("oa3", "oa2", "oa1")):
    m = K.K.ellipse_mask(16, 16, cx, cy, rx, ry)
    for y, x in np.argwhere(m):
        u = (x - cx) / rx + (y - cy) / ry
        n = K.hsh(x, y, 3) % 5
        c = tones[0] if u < -0.7 else (tones[1] if u < 0.5 else tones[2])
        if n == 0 and c == tones[1]:
            c = tones[0]
        L.px(ox + x, oy + y, c)
    for y, x in np.argwhere(K.halo(m)):
        if y >= cy - 1:
            L.px(ox + x, oy + y, "ink" if y > cy + ry - 2 else "oa1")
    return m


def rock_bits():
    """Interior crag cells to scatter (a crack, boulders, a kermes-oak bush, a
    tuft), the scrub on grass (maquis bushes), and the east-facing ledges."""
    names = {"crack": (0, 0), "boulders": (1, 0), "scrub_rock": (2, 0), "tuft": (3, 0),
             "bush": (4, 0), "bush_b": (5, 0), "ledge_e": (6, 0), "ledge_e_foot": (7, 0)}
    s = K.struct("rock_bits", "Rock detail, scrub and the goat path's ledges", 8, 1, SEC,
                 walk=["XXXXXXXX"], names=names,
                 notes="`crack`, `boulders`, `scrub_rock`, `tuft`: interior crag cells to "
                       "scatter. `bush`, `bush_b`: maquis on grass (blocks). `ledge_e`: a rock "
                       "step on the goat path, MB_JUMP_EAST (jump east, down toward Thyrsa); "
                       "`ledge_e_foot` the same step where the path's south side meets rock.")
    B = s.B
    for cx in range(4):
        KG.paint_crag_cell(B, cx * 16, 0, FULL, KG.grass_floor)
    for i, (x, y) in enumerate(((2, 3), (3, 4), (4, 4), (5, 5), (6, 6), (7, 6), (8, 7), (9, 8),
                                 (10, 9), (10, 10), (11, 11), (12, 12))):
        B.px(x, y, "rk1")
        B.px(x, y - 1, "rk4")
    for (cx, cy, r) in ((5, 6, 4), (11, 10, 3), (4, 12, 2)):
        m = K.K.ellipse_mask(16, 16, cx, cy, r + 0.5, r)
        for y, x in np.argwhere(m):
            u = (x - cx) / r + (y - cy) / r
            B.px(16 + x, y, "rk5" if u < -0.8 else ("rk4" if u < 0 else ("rk3" if u < 0.8 else "rk2")))
        for y, x in np.argwhere(K.halo(m)):
            if y >= cy:
                B.px(16 + x, y, "rk1")
    _bush(B, 32, 0, 8, 8, 6.0, 4.5)
    K.put(B, 48 + 3, 5, ["..1.1...", ".121.1..", "1221212.", ".K2222K.", "..KKKK.."],
          {"1": "g3", "2": "g2", "K": "rk1"})
    # maquis bushes on grass
    for cx, (bx, by, rx, ry) in ((4, (8, 8, 6.5, 5.5)), (5, (7, 9, 5.5, 5.0))):
        grass(B, cx * 16, 0)
        for x in range(2, 14):
            if (x + 1) % 2:
                B.px(cx * 16 + x, 14, "gd")
        _bush(B, cx * 16, 0, bx, by, rx, ry)
        if cx == 5:
            for (x, y) in ((4, 6), (9, 8), (6, 11)):
                B.px(cx * 16 + x, y, "w0")        # white rock-rose
    # the goat path's ledges, as Gen 3 draws an east-facing ledge: the grass of the
    # higher ground runs up to a rock lip, then a short dark face and a shadow on
    # the lower grass to the east. A few stones break the lip so it reads as rock.
    for cx, foot in ((6, False), (7, True)):
        ox = cx * 16
        grass(B, ox, 0)
        for y in range(16):
            lip = 8 + (1 if (y // 5) % 2 else 0)
            B.px(ox + lip - 2, y, "rk3")
            B.px(ox + lip - 1, y, "rk4")
            B.px(ox + lip, y, "rk5" if y % 4 else "rk4")
            B.px(ox + lip + 1, y, "rk2")
            B.px(ox + lip + 2, y, "rk1")
            B.px(ox + lip + 3, y, "rk0" if y % 3 else "rk1")
            B.px(ox + lip + 4, y, "gd")
            if y % 2:
                B.px(ox + lip + 5, y, "gd")
        for (x, y) in ((5, 3), (6, 11), (4, 7)):
            B.px(ox + x, y, "rk3")
            B.px(ox + x, y + 1, "rk2")
        if foot:
            for x in range(16):
                for y in range(13, 16):
                    if B.get(ox + x, y) in ("g1", "g2", "g3", "gd"):
                        B.px(ox + x, y, "gd" if y == 13 else ("rk2" if y == 14 else "rk1"))
    s.behaviors[(6, 0)] = "MB_JUMP_EAST"
    s.behaviors[(7, 0)] = "MB_JUMP_EAST"
    return s


def sphinx():
    """The Sphinx's ledge: a flat grey slab high on the spur, old feathers on it.
    The middle column repeats; the east column mirrors the west."""
    names = {"NW": (0, 0), "N": (1, 0), "NE": (2, 0), "SW": (0, 1), "S": (1, 1), "SE": (2, 1),
             "N_feathers": (3, 0), "S_feathers": (3, 1), "S_dig": (4, 1)}
    s = K.struct("sphinx", "The Sphinx's ledge", 5, 2, SEC, walk=[".....", "....."], names=names,
                 notes="A flat slab of pale rock on the spur's top, scattered with big old "
                       "feathers: `NW` `N`... `NE` over `SW` `S`... `SE` (repeat the middle; "
                       "`N_feathers`, `S_feathers` are middle cells with feathers, `S_dig` one "
                       "with scraped grit, the daily dig). Walkable. The Enigmaw sits on it by "
                       "day; the Hyper Potion and the dig go here.")
    B = s.B
    grass(B, 0, 0, 80, 32)
    yy, xx = np.mgrid[0:32, 0:48]
    # a slab 3 cells wide, its middle column straight (so it repeats)
    ex = np.where(xx < 16, 16 - xx, np.where(xx >= 32, xx - 31, 0)).astype(float)
    ey = np.abs(yy - 15.5)
    slab = (ex / 14.0) ** 2 + (ey / 13.5) ** 6 <= 1.0
    for y, x in np.argwhere(slab):
        B.px(x, y, _slab_px(x, y))
    for y, x in np.argwhere(K.ring(slab)):
        B.px(x, y, "rk5" if y < 15 else "rk2")
    for y, x in np.argwhere(K.halo(slab)):
        if y >= 16:
            B.px(x, y, "rk1" if y > 28 else "gd")
    # mirror the west column onto the east (tile flips cost nothing)
    B.a[:, 32:48] = B.a[:, 0:16][:, ::-1]
    # the feathered middle cells
    B.a[:, 48:64] = B.a[:, 16:32]
    # the dig: grit scraped up in the middle of the slab
    B.a[:, 64:80] = B.a[:, 16:32]
    for y in range(16, 28):
        for x in range(67, 77):
            if ((x - 71.5) / 4.6) ** 2 + ((y - 21.5) / 3.6) ** 2 <= 1.0:
                B.px(x, y, "rk2" if (x + y) % 3 else "rk1")
    for (fx, fy, d) in ((49, 6, 1), (55, 11, -1), (50, 22, 1), (57, 18, -1)):
        for k in range(6):
            x, y = fx + k, fy + d * (k // 2)
            B.px(x, y, "w0" if k < 5 else "rk1")
            if k < 4:
                B.px(x, y + 1, "rk5" if k % 2 else "w0")
    return s


def _slab_px(x, y):
    xx, yy = x % 16, y % 16
    h = K.hsh(xx, yy, 17) % 100
    if (xx, yy) in ((3, 5), (4, 5), (5, 6), (11, 11), (12, 11)):
        return "rk2"
    return "rk4" if h < 78 else ("rk3" if h < 95 else "rk5")


# --------------------------------------------------------------------------
# The Minyan dike (stone group)
# --------------------------------------------------------------------------

def _kerb(L, ox, oy, y0, rows, dark=False, shift=0):
    """A course of dressed kerb stones along the dike's edge (8 px joints, so
    the course repeats every tile)."""
    for x in range(16):
        for j in range(rows):
            y = y0 + j
            joint = (x + shift + (4 if j % 2 else 0)) % 8 == 0
            c = "cy1" if joint else ("cy4" if j == 0 else ("cy3" if j < rows - 1 else "cy2"))
            if dark and j == rows - 1:
                c = "cy1"
            L.px(ox + x, oy + y, c)


def _paving(x, y):
    """The causeway's edge paving: dressed slabs 8 x 6, staggered, worn pale
    along their top edges (16 px periodic)."""
    xx, yy = x % 16, y % 16
    row = yy // 6 if yy < 12 else 2
    off = 4 if row % 2 else 0
    jx = (xx + off) % 8 == 0
    jy = yy in (0, 6, 12)
    if jx or jy:
        return "cy1"
    if yy in (1, 7, 13):
        return "cy4"
    h = K.hsh(xx, yy, 37) % 100
    if h < 8:
        return "cy2"
    return "cy3"


def dike():
    """The causeway: a course of dressed paving along each edge, aethos's road
    between them (borrowed, so the dike's middle costs no tiles), and the south
    face of fitted stone going down into the water; the sluice's grating and
    culvert arch; the two ends."""
    names = {"cope": (0, 0), "top": (0, 1), "kerb": (0, 2), "face": (0, 3),
             "cope_sluice": (1, 0), "top_reeds": (1, 1), "kerb_reeds": (1, 2),
             "face_sluice": (1, 3),
             "cope_W": (2, 0), "top_W": (2, 1), "kerb_W": (2, 2), "face_W": (2, 3),
             "cope_E": (3, 0), "top_E": (3, 1), "kerb_E": (3, 2), "face_E": (3, 3)}
    walk = ["....", "....", "....", "XXXX"]
    s = K.struct("dike", "The Minyan dike", 4, 4, SEC, walk=walk, names=names,
                 notes="The Minyans' causeway across the inlet, as columns: `cope` (the north "
                       "edge's paving) over `top` (aethos's road, borrowed; repeat it, the dike "
                       "is four tiles wide) over `kerb` (the south edge's paving), all walkable, "
                       "over `face` (the south face, down into the water; blocks). `cope_sluice` "
                       "over `face_sluice` is the sluice: the gate's grating and the culvert's "
                       "arch. `top_reeds`, `kerb_reeds` have reed tufts. `_W` and `_E` end the "
                       "dike where it meets the land.")
    K.ground(s, "path", [(cx, 1) for cx in range(4)])
    Mi, B = s.M, s.B
    for cx in range(4):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                B.px(ox + x, y, _paving(x, y))
                B.px(ox + x, 32 + y, _paving(x, y + 3))
        for x in range(16):
            B.px(ox + x, 0, "cy4" if x % 8 else "cy3")       # the north lip, lit
            B.px(ox + x, 47, "cy0")                          # the south lip, in shadow
            B.px(ox + x, 46, "cy1")
        for y in range(16):
            for x in range(16):
                c = KS.cyclo(x, y, dark=1 if y > 8 else 0)
                if y >= 13:
                    c = {"cy3": "cy1", "cy2": "cy1", "cy4": "cy2"}.get(c, c)
                B.px(ox + x, 48 + y, c)
        for x in range(16):
            B.px(ox + x, 48, "cy2")
            B.px(ox + x, 63, "cy0")
    # the sluice: a dark grating set in the north paving, the culvert's arch in the face
    for x in range(3, 13):
        for y in range(2, 11):
            B.px(16 + x, y, "ink" if (x % 2 == 0 or y in (2, 10)) else "cy0")
    for x in range(2, 14):
        B.px(16 + x, 1, "cy4")
        B.px(16 + x, 11, "cy2")
    for y in range(16):
        for x in range(16):
            d = ((x - 7.5) / 5.5) ** 2 + ((y - 13.0) / 9.0) ** 2
            if d <= 1.0:
                B.px(16 + x, 48 + y, "ink" if d > 0.72 or y < 9 else "cy0")
            elif d <= 1.35 and y < 13:
                B.px(16 + x, 48 + y, "cy4" if y < 8 else "cy3")
    # reed tufts: in the road's edge, and growing from a joint of the south paving
    K.put(Mi, 16 + 2, 16 + 10, [".g.g.", "gGgGg", ".GGG."], {"g": "g2", "G": "gd"})
    K.put(Mi, 16 + 11, 16 + 2, [".g.", "gGg"], {"g": "g2", "G": "gd"})
    K.put(B, 16 + 4, 32 + 5, [".g.g.", "gGgGg", ".GGG."], {"g": "g2", "G": "gd"})
    # the ends: the paving turns the corner, a bollard stone at each end
    for cx, west in ((2, True), (3, False)):
        ox = cx * 16
        edge = range(0, 3) if west else range(13, 16)
        for y in list(range(0, 16)) + list(range(32, 48)):
            for x in edge:
                c = "cy1" if (y + 2) % 8 == 0 else ("cy4" if x == (0 if west else 15) else "cy3")
                B.px(ox + x, y, c)
        for y in range(16, 32):
            for x in edge:
                c = "cy1" if (y + 2) % 8 == 0 else ("cy4" if x == (0 if west else 15) else "cy3")
                Mi.px(ox + x, y, c)
        for y in range(48, 64):
            for x in edge:
                B.px(ox + x, y, "cy2" if y < 60 else "cy0")
            B.px(ox + (3 if west else 12), y, "cy0")
        # a squat bollard on the north paving
        K.put(B, ox + (4 if west else 7), 3, ["..KKK..", ".K443K.", "K44332K", "K33221K", ".KKKKK."],
              {"K": "ink", "4": "cy4", "3": "cy3", "2": "cy2", "1": "cy1"})
    return s


# --------------------------------------------------------------------------
# The Treasury of Minyas (stone group)
# --------------------------------------------------------------------------

def _ring_px(x, y):
    """The ring wall's top: big fitted stones (16 px periodic)."""
    return KS.cyclo(x, y)


def tholos():
    """The beehive tomb, its dome fallen in long ago, so from above you look
    down into the round chamber: the ring wall's top, the corbelled courses of
    its north side stepping in and darkening, a floor of pale packed earth, and
    in the south wall the doorway under its cracked lintel and relieving
    triangle. Built from mirrored and repeating cells, to save tiles."""
    W, H = 5, 6
    walk = ["XXXXX",
            "XXXXX",
            "X...X",
            "X...X",
            "XXTXX",
            ".X.X."]
    names = {f"{x},{y}": (x, y) for y in range(H) for x in range(W)}
    s = K.struct("tholos", "The Treasury of Minyas", W, H, SEC, walk=walk, names=names,
                 notes="A 5 x 6 stamp. Row 0: the ring wall's north arc; row 1: the inner face "
                       "of the north wall, its corbelled courses stepping in and darkening up "
                       "into shadow; rows 2-3: the chamber's floor (3 x 2, walkable); row 4: the "
                       "south wall with the doorway (2,4), its cracked lintel drawn over the "
                       "player; row 5: the dromos between its two short walls. Put the column "
                       "drum (the Girdle) in the dromos at (2,5).")
    K.ground(s, "grass", [(0, 5), (4, 5)])
    K.ground(s, "path", [(1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3), (2, 5)])
    B, Mi, T = s.B, s.M, s.T
    # --- the west half; the east half is its mirror ---------------------------
    half = K.A.Layer(48, 96)
    half.texture(K.GRASS, 0, 0, 48, 96)
    cx0, cy0 = 40.0, 40.0                    # the ring's centre, in the stamp's pixels
    for y in range(80):
        for x in range(40):
            d = ((x - cx0) ** 2 + ((y - cy0) * 1.12) ** 2) ** 0.5
            if d <= 40 and d > 26:
                half.px(x, y, _ring_px(x, y))
            elif 39 < d <= 42 and y > cy0:
                half.px(x, y, "gd")
    for y in range(80):
        for x in range(40):
            d = ((x - cx0) ** 2 + ((y - cy0) * 1.12) ** 2) ** 0.5
            if 39 <= d <= 40.5:
                half.px(x, y, "cy4" if y < cy0 else "cy1")
            if 25.5 <= d <= 26.6 and y < 30:
                half.px(x, y, "ink")
    # the chamber's floor where it reaches into the wall's cells: aethos's road,
    # to match the borrowed floor cells beside it
    for y in range(28, 80):
        for x in range(0, 48):
            d = ((x - cx0) ** 2 + ((y - cy0) * 1.12) ** 2) ** 0.5
            if d <= 26 and y >= 30:
                half.rgb(x, y, K.aethos(K.PATH)[y % 16, x % 16])
    # the north wall's inner face: horizontal corbel courses, darkening upward
    for y in range(4, 30):
        for x in range(14, 48):
            d = ((x - cx0) ** 2 + ((y - cy0) * 1.12) ** 2) ** 0.5
            if d < 26:
                band = (30 - y) // 4
                c = ("cy2", "cy1", "cy2", "cy1", "cy0", "ink", "ink")[min(6, band)]
                if y % 4 == 0:
                    c = "cy0" if band < 4 else "ink"
                half.px(x, y, c)
    # the south wall's outer face either side of the doorway
    for y in range(64, 80):
        for x in range(0, 48):
            d = ((x - cx0) ** 2 + ((y - cy0) * 1.12) ** 2) ** 0.5
            if d <= 40 and x < 35:
                c = "cy3" if ((x // 8) + (y // 5)) % 2 else "cy2"
                if y % 5 == 0 or x % 8 == 0:
                    c = "cy1"
                half.px(x, y, c)
    for x in range(0, 35):
        d = ((x - cx0) ** 2 + ((64 - cy0) * 1.12) ** 2) ** 0.5
        if d <= 40:
            half.px(x, 64, "cy4")
    # the dromos's west wall
    for y in range(80, 96):
        for x in range(20, 32):
            half.px(x, y, KS.cyclo(x, y))
        half.px(31, y, "ink")
    for x in range(20, 32):
        half.px(x, 80, "cy4")
    # copy the half into cells 0-1 and its mirror into 3-4 (bottom layer), and
    # the middle column from the half's last 8 px mirrored about the centre
    full = np.zeros((96, 80, 4), np.uint8)
    full[:, 0:40] = half.a[:, 0:40]
    full[:, 40:80] = half.a[:, 0:40][:, ::-1]
    for cy in range(H):
        for cx in range(W):
            if (cx, cy) in getattr(s, "ground", {}):
                continue
            B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = full[cy * 16:cy * 16 + 16,
                                                                    cx * 16:cx * 16 + 16]
    # the doorway: a tall dark opening, the lintel and relieving triangle over it
    for y in range(64, 80):
        for x in range(32, 48):
            B.px(x, y, "l0" if x in (33, 46) else ("l1" if y > 70 else "l0"))
        B.px(32, y, "ink")
        B.px(47, y, "ink")
    for x in range(29, 51):
        for y in range(64, 70):
            T.px(x, y, "cy4" if y == 64 else ("cy3" if y < 68 else ("cy1" if y == 68 else "ink")))
    for (x, y) in ((38, 64), (39, 65), (39, 66), (40, 67), (40, 68)):
        T.px(x, y, "ink")                     # the crack across the lintel
    # fallen stones and the hole Alethea didn't dig, on the chamber floor
    K.put(Mi, 20, 50, [".33.", "3221", ".11."], {"3": "cy3", "2": "cy2", "1": "cy1"})
    K.put(Mi, 56, 38, [".33.", "3221", ".11."], {"3": "cy3", "2": "cy2", "1": "cy1"})
    # shadow along the north wall's foot, on the floor
    for x in range(16, 64):
        if x % 2 == 0:
            Mi.px(x, 32, "l0")
    return s


def gla():
    """Gla: a low rocky islet ringed by a broken Cyclopean wall with a great
    gate and no handle on it; on borrowed water. Repeating cells, mirrored."""
    W, H = 6, 4
    walk = ["XXXXXX",
            "X....X",
            "XX.XXX",
            "X....X"]
    names = {f"{x},{y}": (x, y) for y in range(H) for x in range(W)}
    s = K.struct("gla", "Gla, the walled islet", W, H, SEC, walk=walk, names=names,
                 notes="A 6 x 4 stamp: the ring wall (row 0 its north side, rows 1-2 its west "
                       "and east sides, row 2 its south face with the great gate at (3,2) and "
                       "a breach at (2,2)), grass inside (row 1), and the islet's rocky south "
                       "shore (row 3), where you land with the Conch. The Revive goes on the "
                       "shore, the dig inside the wall.")
    K.ground(s, "sea", [(x, y) for y in range(H) for x in range(W) if y in (0, 3) or x in (0, 5)])
    K.ground(s, "grass", [(x, 1) for x in range(1, 5)] + [(2, 2)])
    K.ground(s, "sea", [(3, 2), (1, 2), (4, 2)])
    Mi = s.M
    # rows 0 and 3 and the side columns: rock and wall over water
    for y in range(64):
        for x in range(96):
            inside_isl = 4 <= x < 92 and 6 <= y < 60
            if not inside_isl:
                continue
            onwall = (y < 16 and y >= 6) or x < 16 or x >= 80 or (32 <= y < 48)
            if onwall:
                if y < 16 or x < 16 or x >= 80:
                    Mi.px(x, y, KS.cyclo(x, y))
            if y >= 48:
                h = K.hsh(x % 16, y % 16, 7) % 100
                Mi.px(x, y, "g1" if h < 35 else ("g2" if h < 80 else "cy3"))
    # the wall's lit top edge and its dark foot
    for x in range(4, 92):
        Mi.px(x, 6, "cy4")
    for y in range(6, 48):
        Mi.px(4, y, "cy4")
        Mi.px(91, y, "cy1")
    # the south face: dressed blocks, the breach, the gate
    for y in range(32, 48):
        for x in range(16, 80):
            c = "cy3" if ((x // 8) + (y // 4)) % 2 else "cy2"
            if y % 4 == 0 or x % 8 == 0:
                c = "cy1"
            Mi.px(x, y, c)
    for x in range(16, 80):
        Mi.px(x, 32, "cy4")
    for y in range(36, 48):                       # the great gate, shut, no handle
        for x in range(50, 62):
            Mi.px(x, y, "l0" if (x - 50) % 3 else "ink")
    for x in range(48, 64):
        Mi.px(x, 34, "cy4")
        Mi.px(x, 35, "cy1")
    for y in range(32, 48):                       # the breach: fallen blocks, a way in
        for x in range(32, 48):
            Mi.px(x, y, None)
    K.put(Mi, 33, 38, [".33....33.", "3221..3221", ".11....11."],
          {"3": "cy3", "2": "cy2", "1": "cy1"})
    # rocks at the waterline round the islet
    for x in range(4, 92, 3):
        Mi.px(x, 60, "cy2")
        Mi.px(x + 1, 61, "cy1")
    for y in range(8, 60, 3):
        Mi.px(2, y, "cy2")
        Mi.px(93, y, "cy2")
    # the breach cell is on borrowed grass: paint its rubble on the middle layer only
    for y in range(32, 48):
        for x in range(32, 48):
            if Mi.a[y, x, 3] == 0:
                continue
    return s


# --------------------------------------------------------------------------
# The herm, the racing post, turned earth
# --------------------------------------------------------------------------

def markers():
    names = {"herm_top": (0, 0), "herm": (0, 1), "post_top": (1, 0), "post": (1, 1),
             "dig": (2, 0), "dig_floor": (2, 1), "dig_dike": (3, 1)}
    s = K.struct("markers", "The herm, the racing post, turned earth", 4, 2, SEC,
                 walk=["TT..", "XX.."], names=names,
                 notes="On borrowed grass. `herm_top` over `herm`: the great herm at the spur "
                       "fork, hung with reed garlands. `post_top` over `post`: the Onchestos "
                       "marker, Atalanta's worn racing post. `dig` turned earth on grass, "
                       "`dig_floor` on the Treasury's floor, `dig_dike` on the dike's road "
                       "(all walkable).")
    K.ground(s, "grass", [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)])
    K.ground(s, "path", [(2, 1), (3, 1)])
    st = {"K": "ink", "4": "cy4", "3": "cy3", "2": "cy2", "1": "cy1", "0": "cy0",
          "g": "g2", "G": "gd"}
    top, bot = _cell(), _cell()
    K.put(top, 4, 3, [
        "..KKKK..",
        ".K4433K.",
        "K443332K",
        "K4K33K2K",
        "K433332K",
        ".K1111K.",
        ".K1111K.",
        "..K11K..",
        ".KK44KK.",
        "gK4332Kg",
        ".GgggGG.",
        "K433332K",
        "K433322K",
    ], st)
    for y in range(16):
        for x in range(5, 11):
            bot.px(x, y, ("cy4", "cy3", "cy3", "cy3", "cy2", "cy2")[x - 5])
        bot.px(4, y, "ink")
        bot.px(11, y, "ink")
    for (y, d) in ((3, 1), (7, -1)):
        for x in range(3, 13):
            bot.px(x, y + (abs(x - 8) // 3) * d, "gd" if x % 2 else "g2")
    K.put(bot, 2, 12, ["KKKKKKKKKKKK", "K4433322211K", "KKKKKKKKKKKK"], st)
    for x in range(3, 14):
        if x % 2:
            bot.px(x, 15, "gd")
    _place(s, "top", 0, 0, top)
    _place(s, "middle", 0, 1, bot)
    # the racing post: a worn stone pillar, a groove where the ropes ran
    top, bot = _cell(), _cell()
    for y in range(9, 16):
        for x in range(6, 11):
            top.px(x, y, ("cy4", "cy3", "cy3", "cy2", "cy1")[x - 6])
        top.px(5, y, "ink")
        top.px(11, y, "ink")
    K.put(top, 5, 7, [".KKKKK.", "K44332K"], st)
    for y in range(0, 14):
        for x in range(6, 11):
            bot.px(x, y, ("cy4", "cy3", "cy3", "cy2", "cy1")[x - 6])
        bot.px(5, y, "ink")
        bot.px(11, y, "ink")
    for x in range(6, 11):
        bot.px(x, 4, "cy1")
        bot.px(x, 5, "cy0")
    for x in range(4, 13):
        bot.px(x, 14, "gd" if x % 2 else "g1")
        bot.px(x, 15, "gd")
    _place(s, "top", 1, 0, top)
    _place(s, "middle", 1, 1, bot)
    # turned earth on grass (middle layer over borrowed grass)
    dig = _cell()
    for y in range(3, 14):
        for x in range(2, 14):
            if ((x - 7.5) / 5.5) ** 2 + ((y - 8.0) / 4.5) ** 2 <= 1.0:
                dig.px(x, y, "l1" if (x * 3 + y) % 4 else "l0")
    for x in range(3, 13):
        if ((x - 7.5) / 5.5) ** 2 <= 1.0:
            dig.px(x, 13, "gd")
    _place(s, "middle", 2, 0, dig)
    # turned earth on the Treasury's floor and on the dike (both borrowed road)
    for cx in (2, 3):
        for y in range(4, 13):
            for x in range(3, 13):
                if ((x - 7.5) / 5.0) ** 2 + ((y - 8.0) / 4.0) ** 2 <= 1.0:
                    s.M.px(cx * 16 + x, 16 + y, "l0" if (x + y) % 3 else "l1")
        for x in range(4, 12):
            s.M.px(cx * 16 + x, 16 + 12, "p1")
    return s


def build(phase=0):
    return [crag(phase), rock_bits(), sphinx(), dike(), tholos(), gla(), markers()]
