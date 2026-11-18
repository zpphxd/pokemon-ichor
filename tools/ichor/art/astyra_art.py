"""Painters for gTileset_Akropolis and gTileset_Astyra (the awe pass, items 1-2).

Astyra is the capital (Athens): a limestone rock over the city, the Parthenon
and a bronze Athena Promachos on it, the agora and its stoas below, courtyard
houses on the slopes, the Dipylon gate and its graves outside. Every column is
painted with tools/ichor/art/columns.py, the shared column kit; STYLE.md's
"Architecture: Gen 3 craft and Greek forms" is the rulebook these follow.

The pieces are drawn at full size on one Layer and cut into structures, so a
facade is composed as one picture and then counted in tiles. Almost every cell
sits on borrowed aethos ground (path on the rock, grass or path in the city)
with its art on the middle layer (solid) or the top layer (walk behind).
astyra_build.py packs, compiles and registers both tilesets.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import columns as CK  # noqa: E402
import kythera_lib as K  # noqa: E402
from kythera_lib import Layer, anim_layer, struct  # noqa: E402

A = K.A
C = K.C

NEW = {
    # the Akropolis rock: warm gray limestone with ochre bedding
    "ar0": (64, 48, 40), "ar1": (112, 96, 80), "ar2": (160, 144, 120), "ar3": (200, 184, 152),
    "ar4": (224, 216, 184), "ar5": (240, 232, 208),
    # plastered mudbrick walls of the asty
    "hw1": (176, 152, 120), "hw2": (216, 192, 152), "hw3": (240, 224, 192),
    # the city's water
    "aw1": (40, 88, 152), "aw2": (72, 136, 200), "aw3": (144, 200, 232),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in C or C[_n] == _c, f"color name clash: {_n}"
    C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)

GROUPS = {
    "marble": CK.GROUPS["marble"],
    "bronze": CK.GROUPS["bronze"],
    "ruin": CK.GROUPS["ruin"],
    # the rock, its scrub, and the shadows it casts on path and grass
    "rock": ["ar0", "ar1", "ar2", "ar3", "ar4", "ar5", "gd", "t0", "ps", "mo1", "mo2", "iv1",
             "iv2", "g1", "g2"],
    # roofs and walls: terracotta tiles, plaster, timber doors
    "roof": ["tc0", "tc1", "tc2", "tc3", "hw1", "hw2", "hw3", "wd0", "wd1", "wd2", "ink", "cd0",
             "ps", "gd", "pr1"],
    # trees and gardens: cypress, olive, myrtle, the agora's planes
    "green": ["g1", "g2", "g3", "gd", "t0", "c1", "c2", "c3", "o4", "o5", "k1", "k2", "ink",
              "mo2", "pp1"],
    # water: the fountain house, the harbor's quays
    "water": ["aw1", "aw2", "aw3", "cm0", "cm1", "cm2", "cm3", "cm4", "cm5", "bz1", "bz2",
              "b1", "b2", "b3", "cd1"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
    for _n in _names:
        assert _n in C, _n

M = CK.RAMP["marble"]           # cm0..cm5
R = ["ar0", "ar1", "ar2", "ar3", "ar4", "ar5"]
BZ = ["bz0", "bz1", "bz2", "bz3", "pg2", "cm5"]
h, hp = K.h, K.hp


# --------------------------------------------------------------------------
# Helpers: compose on one canvas, cut into a structure
# --------------------------------------------------------------------------

def canvas(w, hh):
    return Layer(w * 16, hh * 16)


def cut(key, title, w, hh, layers, walk, names=None, notes="", on="path", section="akropolis",
        top_rows=(), top_cells=(), ground_cells=None, anims=None):
    """A structure from full-size canvases. layers: {"middle": Layer, "top": Layer,
    "bottom": Layer}. Cells in top_rows (or top_cells) move their middle art to
    the top layer. ground_cells (default: every cell with no bottom art) borrow
    aethos ground `on`."""
    s = struct(key, title, w, hh, section, walk=walk, names=names or {}, notes=notes)
    for ln, L in layers.items():
        s.layers[ln].a[:] = L.a
    for cy in range(hh):
        for cx in range(w):
            if cy in top_rows or (cx, cy) in top_cells:
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                m = s.M.a[sl].copy()
                s.T.a[sl] = np.where(m[..., 3:4] > 0, m, s.T.a[sl])
                s.M.a[sl] = 0
    if on:
        cells = ground_cells
        if cells is None:
            cells = [(x, y) for y in range(hh) for x in range(w)
                     if not (s.B.a[y * 16:y * 16 + 16, x * 16:x * 16 + 16, 3] > 0).any()]
        for c in cells:
            s.ground[c] = on
    if anims:
        for name, frames in anims.items():
            fr = anim_layer(s, name, len(frames) + 1, layer=frames[0][0])
            for F, (ln, L) in zip(fr, frames):
                F.a[:] = s.layers[ln].a
                # a frame painted on the canvas replaces the art where it differs
                F.a[:] = np.where(L.a[..., 3:4] > 0, L.a, F.a)
    return s


def crop(s, key, x0, y0, w, hh, title=None, notes="", walk=None, names=None):
    """A new structure from cells (x0..x0+w-1, y0..y0+hh-1) of s."""
    c = struct(key, title or s.title, w, hh, s.section,
               walk=walk or [row[x0:x0 + w] for row in s.walk[y0:y0 + hh]], notes=notes,
               names=names or {})
    sl = np.s_[y0 * 16:(y0 + hh) * 16, x0 * 16:(x0 + w) * 16]
    for ln in ("bottom", "middle", "top"):
        c.layers[ln].a[:] = s.layers[ln].a[sl]
    for (x, y), g in s.ground.items():
        if x0 <= x < x0 + w and y0 <= y < y0 + hh:
            c.ground[(x - x0, y - y0)] = g
    for (x, y), b in s.behaviors.items():
        if x0 <= x < x0 + w and y0 <= y < y0 + hh:
            c.behaviors[(x - x0, y - y0)] = b
    for name, an in s.anims.items():
        frames = []
        for f in an["frames"]:
            L = Layer(w * 16, hh * 16)
            L.a[:] = f.a[sl]
            frames.append(L)
        c.anims[name] = {"layer": an["layer"], "frames": frames}
    return c


def mask_draw(w, hh, fn):
    """A boolean mask w x h drawn with PIL: fn(ImageDraw)."""
    im = Image.new("1", (w, hh), 0)
    fn(ImageDraw.Draw(im))
    return np.array(im)


def outline_mask(L, m, color):
    """Outline the edge pixels of mask m on L."""
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    ys, xs = np.nonzero(edge)
    for y, x in zip(ys, xs):
        L.px(int(x), int(y), color)


def shadow_band(L, x0, x1, y, rows=4, c="ps", shift=3):
    """A cast shadow below a building's foot: falling down and right."""
    for j in range(rows):
        for x in range(x0 + shift + j, x1 + shift + 1):
            if L.get(x, y + j) is None and (j < rows - 1 or (x + y) % 2 == 0):
                L.px(x, y + j, c)


# --------------------------------------------------------------------------
# Rock: the Akropolis's cliff, in 3 rows (lip, face, foot)
# --------------------------------------------------------------------------

_ROCK_PTS = None


def _rock_points():
    global _ROCK_PTS
    if _ROCK_PTS is None:
        rng = np.random.RandomState(7)
        pts = []
        for gy in range(4):
            for gx in range(2):
                pts.append((gx * 8 + rng.randint(1, 7), gy * 8 + rng.randint(1, 7), rng.randint(0, 3)))
        _ROCK_PTS = pts
    return _ROCK_PTS


def rock_px(X, Y, seed=0):
    """Limestone face, 32 px periodic: fractured facets (a periodic Voronoi),
    each lit on its upper left and shaded on its lower right, dark cracks
    between them, and a faint horizontal bedding every 8 rows."""
    x, y = X % 16, Y % 32
    best = []
    for (px, py, v) in _rock_points():
        for ox in (-16, 0, 16):
            for oy in (-32, 0, 32):
                dx, dy = x - (px + ox), y - (py + oy) * 1.0
                best.append((dx * dx + dy * dy * 1.6, dx, dy, v))
    best.sort()
    d1, dx, dy, v = best[0]
    d2 = best[1][0]
    gap = math.sqrt(d2) - math.sqrt(d1)
    if gap < 0.9:
        return "ar1" if (dx + dy) > 0 else "ar0" if gap < 0.45 else "ar1"
    k = 2 + (v % 2)
    if dx + dy < -3:
        k += 1
    elif dx + dy > 3:
        k -= 1
    if y % 8 == 0 and hp(X, Y, 5) % 3:
        k = max(1, k - 1)
    return R[max(1, min(5, k))]


def cliff(on="path", key="cliff", section="akropolis", foot_on=None):
    """The rock's south face, three cells tall. Names: lip, lip_b (row 0: the
    upper ground's rim and the face's top), face, face_b (row 1), foot, foot_b
    (row 2: the face meeting the lower ground, with its cast shadow); and the
    ends: lip_W, face_W, foot_W, lip_E, face_E, foot_E. Use the lip row along
    the top of the drop and the foot row on the lower ground."""
    foot_on = foot_on or on
    w = 8
    s = struct(key, "the Akropolis cliff", w, 3, section, walk=["X" * w] * 3,
               names={"lip": (0, 0), "lip_b": (1, 0), "face": (0, 1), "face_b": (1, 1),
                      "foot": (0, 2), "foot_b": (1, 2), "lip_W": (2, 0), "face_W": (2, 1),
                      "foot_W": (2, 2), "lip_E": (3, 0), "face_E": (3, 1), "foot_E": (3, 2),
                      "lip_cap": (4, 0), "face_bush": (4, 1), "foot_bush": (4, 2),
                      "scrub": (5, 0), "boulder": (5, 1), "rock": (5, 2),
                      "lip_in_W": (6, 0), "lip_in_E": (7, 0)})
    L = s.M
    sh = CK.SHADOW.get(foot_on, "gd")
    for cx in range(w):
        for cy in range(3):
            s.ground[(cx, cy)] = on if cy < 2 else foot_on
    # rows: lip (upper ground 0-4, rim 5-6, face 7-15), face, foot (face 0-10, crevice 11, shadow)
    def col(ox, seed, kind):
        for y in range(48):
            for x in range(16):
                X, Y = ox + x, y
                top = 5
                bot = 43
                edge_l = kind == "W" and x < 4 + (y // 6) % 2
                edge_r = kind == "E" and x > 11 - (y // 6) % 2
                if edge_l or edge_r:
                    continue
                if y < top:
                    continue
                if y < top + 2:
                    L.px(X, Y, "ar5" if y == top else "ar4")
                    continue
                if y > bot:
                    if y == bot + 1:
                        L.px(X, Y, "ar0")
                    elif y <= bot + 4 and (x + y) % 2 == 0 or y <= bot + 2:
                        L.px(X, Y, sh)
                    continue
                L.px(X, Y, rock_px(X, Y))
            # the side edges: lit on the west, dark on the east
        if kind == "W":
            for y in range(5, 44):
                x = 4 + (y // 6) % 2
                L.px(ox + x, y, "ar5" if y < 30 else "ar3")
                L.px(ox + x + 1, y, "ar4")
        if kind == "E":
            for y in range(5, 44):
                x = 11 - (y // 6) % 2
                L.px(ox + x, y, "ar0")
                L.px(ox + x - 1, y, "ar1")
    col(0, 0, None)
    col(16, 1, None)
    col(32, 2, "W")
    col(48, 3, "E")
    col(64, 4, None)
    # face_bush: caper and scrub clinging to the face
    for (dx, dy) in ((4, 22), (5, 21), (6, 22), (5, 23), (9, 26), (10, 25), (11, 26), (3, 30)):
        L.px(64 + dx, dy, "iv2")
        L.px(64 + dx, dy + 1, "iv1")
    for (dx, dy) in ((6, 37), (7, 36), (8, 37), (12, 39)):
        L.px(64 + dx, dy, "mo2")
        L.px(64 + dx + 1, dy + 1, "mo1")
    # lip_cap: the rim with a little parapet of stones
    for x in range(64, 80):
        if (x // 4) % 2 == 0:
            L.px(x, 3, "ar4")
            L.px(x, 4, "ar2")
    # scrub on the upper ground (walkable rim), a boulder, bare rock (solid fill)
    for (dx, dy, c) in ((4, 8, "iv2"), (5, 7, "iv2"), (6, 8, "iv1"), (5, 9, "iv1"), (10, 11, "mo2"),
                        (11, 10, "mo2"), (11, 12, "mo1"), (3, 12, "mo1")):
        L.px(80 + dx, dy, c)
    b = mask_draw(16, 16, lambda d: d.ellipse([2, 4, 13, 13], fill=1))
    for y in range(16):
        for x in range(16):
            if b[y, x]:
                L.px(80 + x, 16 + y, "ar4" if x + y < 12 else "ar3" if x + y < 18 else "ar2")
    outline_mask(L, np.pad(b, ((16, 16), (80, 48)))[:48, :128], "ar0")
    for x in range(5, 15):
        L.px(80 + x, 16 + 14, "ps" if on == "path" else "gd")
    for y in range(32, 48):
        for x in range(80, 96):
            L.px(x, y, rock_px(x, y, 2))
    # inner corners of the lip, where the rim turns north
    for ox, kind in ((96, "W"), (112, "E")):
        for y in range(16):
            for x in range(16):
                if kind == "W" and x >= 10 and y >= 5:
                    L.px(ox + x, y, rock_px(ox + x, y + 16, 1) if x > 11 else "ar5" if x == 10 else "ar4")
                if kind == "E" and x <= 5 and y >= 5:
                    L.px(ox + x, y, rock_px(ox + x, y + 16, 2) if x < 4 else "ar1" if x == 5 else "ar2")
        for x in range(16):
            if (kind == "W" and x < 10) or (kind == "E" and x > 5):
                L.px(ox + x, 5, "ar5")
                L.px(ox + x, 6, "ar4")
                for y in range(7, 16):
                    L.px(ox + x, y, rock_px(ox + x, y, 3))
    s.walk = ["XXXXX.XX", "XXXXXXXX", "XXXXXXXX"]
    return s


def plateau_edge(on="path", key="edge"):
    """The rock's west and east rims seen from above (the drop is off-map):
    edge_W, edge_E (straight), and the north wall: wall_N (a coursed wall with
    old column drums built into it, as Themistokles built them), wall_N_drums."""
    s = struct(key, "the plateau's rims and the north wall", 5, 2, "akropolis",
               walk=["XXXXX", "XXXXX"], on=on,
               names={"edge_W": (0, 0), "edge_E": (1, 0), "wall_N": (2, 0), "wall_N_drums": (3, 0),
                      "wall_N_b": (4, 0), "wall_N_face": (2, 1), "wall_N_face_d": (3, 1),
                      "wall_N_face_b": (4, 1), "edge_W_b": (0, 1), "edge_E_b": (1, 1)})
    L = s.M
    for cy in range(2):
        for y in range(16):
            yy = cy * 16 + y
            for x in range(16):
                if x < 7:
                    L.px(x, yy, rock_px(x, yy, 1) if x < 5 else "ar5" if x == 6 else "ar4")
                if x > 8:
                    L.px(16 + x, yy, rock_px(16 + x, yy, 2) if x > 10 else "ar1" if x == 9 else "ar2")
    # the north wall: top course (row 0) and its face (row 1)
    for i, drums in ((2, False), (3, True), (4, False)):
        ox = i * 16
        for y in range(32):
            for x in range(16):
                X = ox + x
                if y < 6:
                    continue
                if y < 9:
                    L.px(X, y, "ar5" if y == 6 else "ar4")
                    continue
                if y > 28:
                    if (x + y) % 2 == 0 or y == 29:
                        L.px(X, y, "ps")
                    continue
                if y == 28:
                    L.px(X, y, "ar0")
                    continue
                course = (y - 9) // 5
                jx = (x + 6 * (course % 2) + i * 3) % 12
                c = "ar1" if (y - 9) % 5 == 4 or jx == 0 else "ar3" if (y - 9) % 5 == 0 else "ar2"
                L.px(X, y, c)
        if drums:
            # two column drums laid in the wall's face, round ends out
            for dx in (1, 8):
                for j in range(8):
                    for k in range(7):
                        if (k, j) in ((0, 0), (6, 0), (0, 7), (6, 7)):
                            continue
                        e = k in (0, 6) or j in (0, 7)
                        L.px(ox + dx + k, 17 + j, "ar0" if e else "ar5" if j < 3 else "ar4" if j < 6 else "ar3")
    # ordering fix: the face row of wall cells is on the second row
    return s


# --------------------------------------------------------------------------
# Retaining walls and stairs: the switchback ramp
# --------------------------------------------------------------------------

def poly_wall_px(X, Y, seed=0):
    """Polygonal masonry: irregular fitted blocks, joints dark, faces lit."""
    x, y = X % 32, Y % 16
    # a fixed pattern of block seams in a 32 x 16 tile, lines at angles
    seams = [(0, 6, 9, 5), (9, 5, 17, 7), (17, 7, 25, 4), (25, 4, 32, 6),
             (0, 12, 12, 13), (12, 13, 21, 11), (21, 11, 32, 13),
             (9, 5, 11, 13), (17, 7, 15, 13), (25, 4, 23, 11), (5, 0, 4, 6), (20, 0, 21, 7),
             (29, 0, 28, 4), (6, 12, 7, 16), (27, 13, 26, 16), (15, 13, 16, 16)]
    for (x0, y0, x1, y1) in seams:
        if x1 == x0:
            continue
        if min(x0, x1) <= x <= max(x0, x1) and abs(x1 - x0) >= abs(y1 - y0):
            yy = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
            if abs(yy - y) < 0.6:
                return "ar0"
            if abs(yy - (y - 1)) < 0.6:
                return "ar4"
        if min(y0, y1) <= y <= max(y0, y1) and abs(y1 - y0) > abs(x1 - x0) - 1:
            xx = x0 + (x1 - x0) * (y - y0) / max(1, (y1 - y0))
            if abs(xx - x) < 0.6:
                return "ar1"
    k = hp(X, Y, 17 + seed)
    return "ar3" if k % 9 == 0 else "ar2"


def ramp_kit(key="ramp"):
    """The switchback ramp's pieces, on borrowed path:
      cap_L, cap, cap_R   the upper terrace's edge: path, a coping course, the
                          top of the wall face (row 0)
      wall_L, wall, wall_R
                          the wall face and its cast shadow on the lower path
      stair_L, stair, stair_R, stair_top_L/M/R
                          marble steps cut up through the wall (walkable)
      post                a stone bollard by a stair head
    """
    names = {"cap_L": (0, 0), "cap": (1, 0), "cap_R": (2, 0), "stair_top_L": (3, 0), "stair_top": (4, 0),
             "stair_top_R": (5, 0), "post": (6, 0), "cap_b": (7, 0),
             "wall_L": (0, 1), "wall": (1, 1), "wall_R": (2, 1), "stair_L": (3, 1), "stair": (4, 1),
             "stair_R": (5, 1), "wall_b": (7, 1), "wall_drain": (6, 1)}
    s = struct(key, "the ramp's retaining walls and stairs", 8, 2, "akropolis",
               walk=["XXX...XX", "XXX...XX"], names=names, on="path")
    keep = ["cap_L", "cap", "cap_R", "stair_top_L", "stair_top", "stair_top_R", "post",
            "wall_L", "wall", "wall_R", "stair_L", "stair", "stair_R"]
    L = s.M
    for name in ("cap_L", "cap", "cap_R", "cap_b", "wall_L", "wall", "wall_R", "wall_b", "wall_drain"):
        cx, cy = names[name]
        seed = cx
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                yy = cy * 16 + y          # 0..31 over the two rows
                endL = name.endswith("_L") and x < 3
                endR = name.endswith("_R") and x > 12
                if yy < 6:
                    continue
                if yy < 10:
                    if endL or endR:
                        continue
                    L.px(X, Y, "ar5" if yy == 6 else "ar4" if yy < 9 else "ar1")
                    if yy in (7, 8) and (x + seed * 5) % 8 == 0:
                        L.px(X, Y, "ar2")
                    continue
                if yy > 25:
                    if endL or endR:
                        continue
                    if yy == 26:
                        L.px(X, Y, "ar0")
                    elif yy < 29 or (x + yy) % 2 == 0:
                        L.px(X, Y, "ps")
                    continue
                if endL:
                    L.px(X, Y, "ar4" if x == 2 else None) if x == 2 else None
                    continue
                if endR:
                    L.px(X, Y, "ar0") if x == 13 else None
                    continue
                L.px(X, Y, poly_wall_px(X, yy, seed))
        if name == "wall_drain":
            for y in range(18, 24):
                for x in range(6, 10):
                    L.px(cx * 16 + x, y, "ar0" if y < 22 else "ar1")
            for y in range(24, 26):
                L.px(cx * 16 + 7, y, "iv1")
    # stairs: treads lit, risers shaded, cheek walls at the sides
    for name in ("stair_top_L", "stair_top", "stair_top_R", "stair_L", "stair", "stair_R"):
        cx, cy = names[name]
        for y in range(16):
            yy = cy * 16 + y
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                if yy < 6:
                    continue
                cheek = (name.endswith("_L") and x < 3) or (name.endswith("_R") and x > 12)
                if cheek:
                    L.px(X, Y, "ar4" if x in (0, 15) and name.endswith("_L") == (x == 0) else
                         poly_wall_px(X, yy, 2) if yy < 26 else "ar2")
                    continue
                t = (yy - 6) % 5
                L.px(X, Y, "ar5" if t == 0 else "ar4" if t < 3 else "ar3" if t == 3 else "ar1")
    # a bollard
    cx, cy = names["post"]
    for y in range(6, 15):
        for x in range(5, 11):
            e = x in (5, 10) or y == 14
            L.px(cx * 16 + x, y, "ar0" if e else "ar5" if x < 7 else "ar3" if x < 9 else "ar2")
    for x in range(8, 13):
        L.px(cx * 16 + x, 15, "ps")
    return K.pick(s, keep, w=7, key=key)


# --------------------------------------------------------------------------
# The Parthenon (14 x 8): octastyle Doric, polychrome, on a krepis of 3 steps
# --------------------------------------------------------------------------

def pediment(L, x0, x1, apex, base, sculpture=True, color="pb1", akroteria=True):
    """A pediment from x0 to x1 (x0 on an 8 px boundary): raking cornices
    rising 1 px in 4 from the corners to the apex (so the rake's tiles repeat
    every 32 px), a blue tympanum, a row of small figures standing in its
    lower band and a taller pair under the apex, the horizontal geison at
    `base`. `apex` is ignored (the slope sets it); it is kept for callers."""
    mid = (x0 + x1 + 1) // 2

    def top(x):
        return base - min(x - x0, x1 - x) // 4
    for x in range(x0, x1 + 1):
        t = top(x)
        L.px(x, t - 1, "cm0")
        L.px(x, t, "cm5" if x < mid else "cm4")
        L.px(x, t + 1, "cm3" if x < mid else "cm2")
        L.px(x, t + 2, "cm1")
        for y in range(t + 3, base):
            L.px(x, y, color)
    for x in range(x0, x1 + 1):
        L.px(x, base, "cm0")
        L.px(x, base + 1, "cm5" if x < mid else "cm4")
        L.px(x, base + 2, "pr1" if (x // 4) % 2 == 0 else "cm3")
        L.px(x, base + 3, "cm1")
    if sculpture:
        fig = [".hh.", ".hh.", "hhhm", "hhhm", ".hm.", ".hm.", ".hm.", "hh.m"]
        for fx in range(x0 + 4, x1 - 4, 16):
            if top(fx) > base - 12 or top(fx + 4) > base - 12 or abs(fx + 2 - mid) < 14:
                continue
            for j, row in enumerate(fig):
                for i, ch in enumerate(row):
                    if ch != ".":
                        L.px(fx + i, base - 8 + j, "cm4" if ch == "h" else "cm2")
        if top(mid) < base - 16:
            # the contest under the apex: two tall figures face to face
            big = [".hh..", ".hh..", "hhhh.", "hhhmh", ".hhm.", ".hhm.", ".hm..", ".hm..",
                   ".hm..", ".hm..", "hh.m."]
            for side in (-1, 1):
                ox = mid - 7 if side < 0 else mid + 2
                for j, row in enumerate(big):
                    if side > 0:
                        row = row[::-1]
                    for i, ch in enumerate(row):
                        if ch != ".":
                            L.px(ox + i, base - 11 + j, "cm5" if ch == "h" else "cm2")
            for y in range(base - 9, base):
                L.px(mid, y, "pg1")              # the olive between them, in gold
            L.px(mid - 1, base - 9, "pg2")
            L.px(mid + 1, base - 8, "pg2")
    if akroteria:
        a = mid
        palm = [".g.", "gGg", ".g."]
        for j, row in enumerate(palm):
            for i, ch in enumerate(row):
                if ch != ".":
                    L.px(a - 2 + i, top(a) - 4 + j, "pg2" if ch == "G" else "pg1")
        for cx0 in (x0 + 1, x1 - 3):
            for j, row in enumerate([".g.", "gGg"]):
                for i, ch in enumerate(row):
                    if ch != ".":
                        L.px(cx0 + i, base - 3 + j, "pg2" if ch == "G" else "pg1")


def doric_frieze(L, x0, x1, y, step, rows=10, offset=0):
    """Triglyphs (blue, three bars) every `step` px, metopes between them with
    a small relief, the taenia and guttae under it. y is the top row."""
    for x in range(x0, x1 + 1):
        for j in range(rows):
            L.px(x, y + j, "cm4" if j < rows - 1 else "cm2")
    k = 0
    for tx in range(x0 + offset, x1 + 1, step):
        a, b = tx - 3, tx + 2
        for x in range(max(x0, a), min(x1, b) + 1):
            for j in range(rows - 1):
                g = (x - a) in (1, 4)
                L.px(x, y + j, "pb0" if g else "pb1")
            L.px(x, y, "pb0")
        # a metope's relief between this triglyph and the next
        mx = tx + step // 2
        if mx + 3 <= x1:
            fig = [".h.", "hhm", ".hm", "h.m"]
            for j, row in enumerate(fig):
                for i, ch in enumerate(row):
                    if ch != ".":
                        L.px(mx - 1 + i, y + 3 + j, "cm5" if ch == "h" else "cm2")
        k += 1
    for x in range(x0, x1 + 1):
        L.px(x, y + rows, "pr1")             # the painted taenia
        L.px(x, y + rows + 1, "cm1" if ((x - x0 - offset) % step) in range(step - 3, step) or
             ((x - x0 - offset) % step) < 3 else "cm3")      # guttae under each triglyph


def parthenon(key="parthenon"):
    """The Parthenon, 14 x 8 on borrowed path, every cell solid. Names its
    cells by position: 'r{row}c{col}'."""
    W, H = 14, 8
    L = canvas(W, H)
    x0, x1 = 0, W * 16 - 1
    # behind the colonnade: the dark pronaos, the cella door, an inner row of columns
    for y in range(52, 102):
        for x in range(4, x1 - 3):
            L.px(x, y, "cd1" if y > 58 else "cd0")
    for x in range(104, 120):
        for y in range(68, 102):
            e = x in (104, 119) or y == 68
            L.px(x, y, "pg1" if e or (x - 104) % 5 == 0 else "cd0")
    L.px(111, 82, "pg2")            # gold in the dark: the Parthenos's glint
    for cx in range(28, 200, 28):
        for y in range(66, 101):
            for i in range(-3, 3):
                L.px(cx + i, y, "cm0" if i in (-3, 2) else "cm2" if i == -2 else "cm1")
        for i in range(-5, 5):
            L.px(cx + i, 64, "cm1")
            L.px(cx + i, 65, "cm2")
    # the order: 8 columns at a 28 px pitch
    for k in range(8):
        CK.paint_column(L, 14 + 28 * k, 56, 101, "doric", "poly")
    # entablature: architrave with gold shields, the triglyph frieze, the geison
    CK.paint_architrave(L, x0 + 2, x1 - 2, 48, 8)
    for k in range(7):
        sx = 28 + 28 * k
        for (i, j) in ((0, 1), (1, 1), (2, 1), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3),
                       (2, 3), (-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (0, 5), (1, 5), (2, 5)):
            L.px(sx - 1 + i, 48 + j, "pg2" if i + j < 3 else "pg1")
    doric_frieze(L, x0 + 2, x1 - 2, 36, 14, rows=10, offset=12)
    pediment(L, x0, x1, 4, 32)
    # krepis: three steps, each a lit tread, a riser with block joints, a shadow line
    for s_ in range(3):
        a, b = 6 - 3 * s_, x1 - 6 + 3 * s_
        y = 102 + 8 * s_
        for x in range(a, b + 1):
            e = x in (a, b)
            for j in range(8):
                if j < 3:
                    c = "cm5" if j == 0 else "cm4"
                elif j < 7:
                    c = "cm3" if x % 16 != 8 else "cm2"
                else:
                    c = "cm1"
                L.px(x, y + j, "cm0" if e else c)
    shadow_band(L, 0, x1, 126, rows=2)
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    return cut(key, "the Parthenon", W, H, {"middle": L}, ["X" * W] * H, names=names,
               notes="The Parthenon (14 x 8) on borrowed path: an octastyle Doric front with painted "
                     "capitals, a blue-and-red triglyph frieze, gold shields on the architrave, a "
                     "sculpted pediment and gold akroteria, on a krepis of three steps. Solid; stand "
                     "the player on the row below it (the shadow is drawn into row 7).")


# --------------------------------------------------------------------------
# Athena Promachos (4 x 9): bronze, the spear tip gleaming
# --------------------------------------------------------------------------

def _promachos_figure():
    """Region labels for the figure on a 64 x 144 canvas."""
    W, H = 64, 144
    lab = np.zeros((H, W), np.uint8)
    regions = {}

    def region(n, fn):
        regions[n] = len(regions) + 1
        m = mask_draw(W, H, fn)
        lab[m] = regions[n]
    # back to front
    region("crest", lambda d: d.polygon([(29, 16), (27, 9), (29, 4), (33, 3), (37, 6), (38, 11), (36, 17)], fill=1))
    region("skirt", lambda d: d.polygon([(23, 62), (41, 62), (44, 88), (46, 110), (19, 110), (20, 88)], fill=1))
    region("torso", lambda d: d.polygon([(22, 36), (42, 36), (41, 62), (23, 62)], fill=1))
    region("aegis", lambda d: d.polygon([(19, 31), (45, 31), (44, 40), (32, 46), (20, 40)], fill=1))
    region("neck", lambda d: d.rectangle([29, 26, 35, 31], fill=1))
    region("helmet", lambda d: d.ellipse([25, 13, 39, 27], fill=1))
    region("face", lambda d: d.rectangle([28, 20, 36, 28], fill=1))
    region("arm_r", lambda d: d.polygon([(20, 32), (24, 34), (16, 47), (12, 46)], fill=1))
    region("hand_r", lambda d: d.ellipse([9, 43, 16, 50], fill=1))
    region("spear", lambda d: d.rectangle([11, 10, 13, 112], fill=1))
    region("tip", lambda d: d.polygon([(12, 0), (14, 4), (14, 9), (12, 11), (10, 9), (10, 4)], fill=1))
    region("arm_l", lambda d: d.polygon([(41, 33), (45, 35), (48, 48), (44, 49)], fill=1))
    region("shield", lambda d: d.ellipse([37, 40, 61, 72], fill=1))
    region("feet", lambda d: d.polygon([(22, 108), (30, 108), (30, 113), (21, 113)], fill=1))
    region("feet2", lambda d: d.polygon([(35, 108), (43, 108), (44, 113), (35, 113)], fill=1))
    region("girdle", lambda d: d.rectangle([23, 52, 41, 54], fill=1))
    return lab, regions


def promachos(key="promachos", anim=True):
    """Athena Promachos, 4 x 9 on borrowed path: her figure on the top layer
    (rows 0-6, walk T: the player walks behind her shins), the plinth on the
    middle layer (rows 7-8, solid). Animation 'glint': a sparkle runs down the
    gold spear tip (cell r0c0)."""
    W, H = 4, 9
    L = canvas(W, H)
    lab, reg = _promachos_figure()
    inv = {v: k for k, v in reg.items()}
    for y in range(lab.shape[0]):
        for x in range(lab.shape[1]):
            r = inv.get(int(lab[y, x]))
            if not r:
                continue
            c = None
            if r == "crest":
                c = "pr1" if x < 35 else "bz0" if x > 36 else "pr1"
                if x in (32, 33):
                    c = "bz2"
            elif r in ("helmet",):
                c = "bz3" if x < 30 else "bz2" if x < 35 else "bz1"
                if y > 24 and (x < 29 or x > 35):
                    c = "bz1"
            elif r == "face":
                c = "bz2" if x < 32 else "bz1"
                if y == 23 and x in (30, 34):
                    c = "bz0"
                if y == 26 and x in (31, 32, 33):
                    c = "bz1"
            elif r == "neck":
                c = "bz1"
            elif r == "aegis":
                # scales: a checker of lit and dark, snakes at the hem, the gorgoneion
                c = "vg2" if (x + y) % 3 == 0 else "bz2" if x < 32 else "bz1"
                if (x - 32) ** 2 + (y - 37) ** 2 <= 5:
                    c = "pg2" if x < 32 else "pg1"
                if y >= 39 and (x % 3 == 0):
                    c = "vg1"
            elif r == "torso":
                c = "bz3" if x < 26 else "bz2" if x < 36 else "bz1"
                if x in (29, 34) and y > 44:
                    c = "bz1"
            elif r == "girdle":
                c = "pg2" if x < 30 else "pg1"
            elif r == "skirt":
                # long peplos folds, lit on the left
                f = (x - 18) % 4
                base = "bz3" if x < 25 else "bz2" if x < 37 else "bz1"
                c = base if f else ("bz1" if x < 37 else "bz0")
                if f == 1 and x < 30:
                    c = "bz3"
                if y > 104:
                    c = "bz1" if f else "bz0"
                if (x * 7 + y) % 23 == 0:
                    c = "vg1"
            elif r in ("arm_r", "arm_l"):
                c = "bz3" if r == "arm_r" else "bz1"
            elif r == "hand_r":
                c = "bz2"
            elif r == "spear":
                c = "bz1" if x == 11 else "bz0" if x == 13 else "bz2"
            elif r == "tip":
                c = "pg2" if x < 12 else "pg1"
                if x == 12 and y < 9:
                    c = "cm5"
            elif r == "shield":
                d = math.hypot((x - 49) / 12, (y - 56) / 16)
                if d > 0.86:
                    c = "bz3" if (x < 49 and y < 56) else "bz1"
                elif d > 0.78:
                    c = "bz0"
                else:
                    c = "bz2" if x < 47 else "bz1"
                    # the device: an owl's face in gold
                    if (abs(x - 47) <= 1 or abs(x - 51) <= 1) and 52 <= y <= 54:
                        c = "pg2"
                    if x in (47, 51) and y == 53:
                        c = "bz0"
                    if x == 49 and 55 <= y <= 57:
                        c = "pg1"
                    if (x + y) % 11 == 0 and d < 0.6:
                        c = "vg1"
            elif r in ("feet", "feet2"):
                c = "bz2" if r == "feet" else "bz1"
            if c:
                L.px(x, y, c)
    m = lab > 0
    # the silhouette outline, in bronze's darkest
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if lab[y, x] != reg["tip"]:
            L.px(int(x), int(y), "bz0")
    # the plinth: cornice, die with an inscription, base moulding (marble)
    P = canvas(W, H)
    for y in range(112, 142):
        for x in range(2, 62):
            if y < 116 and x in range(2, 62):
                c = "cm5" if y == 112 else "cm4" if y < 115 else "cm1"
            elif 116 <= y < 134:
                if x < 5 or x > 58:
                    continue
                c = "cm4" if x < 12 else "cm3" if x < 48 else "cm2"
                if x in (5, 58):
                    c = "cm0"
                if y == 124 and 14 <= x <= 50 and x % 3:
                    c = "cm1"
                if y == 127 and 18 <= x <= 46 and x % 4:
                    c = "cm2"
            else:
                c = "cm5" if y == 134 else "cm3" if y < 140 else "cm1"
            if x in (2, 61) or y == 141:
                c = "cm0"
            P.px(x, y, c)
    for y in range(142, 144):
        for x in range(6, 64):
            if y == 142 or x % 2 == 0:
                P.px(x, y, "ps")
    # her feet sit on the cornice: copy them over the plinth top
    for y in range(112, 114):
        for x in range(0, 64):
            if L.get(x, y):
                P.px(x, y, L.get(x, y))
    L.a[112:] = 0
    frames = []
    if anim:
        # a sparkle travels down the gold tip and flares at its point
        for f in range(3):
            F = canvas(W, H)
            if f == 0:
                for (x, y) in ((12, 2), (11, 3), (13, 3), (12, 4)):
                    F.px(x, y, "cm5")
            elif f == 1:
                for (x, y) in ((12, 0), (12, 1), (9, 2), (15, 2), (10, 2), (14, 2), (12, 3), (12, 4),
                                  (11, 1), (13, 1), (11, 3), (13, 3)):
                    F.px(x, y, "cm5" if (x, y) not in ((9, 2), (15, 2)) else "pg2")
            else:
                for (x, y) in ((12, 6), (11, 7), (13, 7), (12, 8)):
                    F.px(x, y, "cm5")
            frames.append(("top", F))
    walk = ["TTTT"] * 7 + ["XXXX"] * 2
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    s = cut(key, "Athena Promachos", W, H, {"middle": P, "top": L}, walk, names=names,
            notes="Athena Promachos, bronze, 4 x 9 on borrowed path: helmet and red crest, the aegis "
                  "with its gorgoneion, the owl-shield on her left arm, the spear in her right with "
                  "its gold tip (the gleam sailors saw from Sounion; animation `glint` on r0c0). "
                  "Rows 0-6 are drawn over the player (T), rows 7-8 are the marble plinth (X).",
            anims={"glint": frames} if anim else None)
    if anim:
        K.settle(s, "glint", [(0, 0)])
    return s


# --------------------------------------------------------------------------
# The Erechtheion and the Porch of the Maidens (14 x 7)
# --------------------------------------------------------------------------

def karyatid(L, cx, top, bottom, k=0):
    """A maiden carrying the entablature: polos (basket capital), head, braids,
    a peplos with folds, the relaxed knee bending through the drapery."""
    rows = bottom - top
    # polos: a small Ionic-ish basket, 12 wide
    for x in range(cx - 6, cx + 6):
        L.px(x, top, "cm0" if x in (cx - 6, cx + 5) else "cm5")
        L.px(x, top + 1, "cm0" if x in (cx - 6, cx + 5) else "cm3")
        L.px(x, top + 2, "cm1")
    for x in range(cx - 4, cx + 4):
        L.px(x, top + 3, "cm0" if x in (cx - 4, cx + 3) else "cm4" if x < cx else "cm2")
        L.px(x, top + 4, "cm0" if x in (cx - 4, cx + 3) else "cm3")
    # head and hair
    hy = top + 5
    for j in range(6):
        for x in range(cx - 3, cx + 3):
            c = "cm4" if x < cx - 1 else "cm3" if x < cx + 1 else "cm2"
            if j < 2:
                c = "pr1" if (x + j) % 3 == 0 and k % 2 == 0 else "cm2"   # painted hair band
            L.px(x, hy + j, c)
        L.px(cx - 4, hy + j, "cm1")                  # braids down each side
        L.px(cx + 3, hy + j, "cm1")
    L.px(cx - 2, hy + 3, "cm1")
    L.px(cx + 1, hy + 3, "cm1")
    # shoulders, the peplos
    for y in range(hy + 6, bottom - 1):
        t = (y - hy - 6) / max(1, bottom - hy - 7)
        half = 5 if t < 0.15 else 5
        for x in range(cx - half, cx + half):
            f = (x - cx) % 3
            c = "cm4" if x < cx - 2 else "cm3" if x < cx + 2 else "cm2"
            if f == 0:
                c = "cm2" if x < cx else "cm1"
            if t > 0.55 and ((k % 2 == 0 and x == cx - 3) or (k % 2 and x == cx + 2)):
                c = "cm5"                               # the bent knee pushing the cloth
            if t < 0.2 and y == hy + 8:
                c = "pb1" if x % 2 else "cm3"           # the painted neckline
            L.px(x, y, c)
        L.px(cx - half - 1, y, "cm0")
        L.px(cx + half, y, "cm0")
    for x in range(cx - 6, cx + 6):
        L.px(x, bottom - 1, "cm1")
        L.px(x, bottom, "cm0")


def erechtheion(key="erechtheion"):
    """The Erechtheion (10 x 7) on borrowed path: the Ionic east porch (four
    painted columns between antae, a frieze of dark stone with white figures,
    the bronze doors) and, at its west end, the Porch of the Maidens on its
    high podium, facing south. Solid."""
    W, H = 10, 7
    L = canvas(W, H)
    MX = 95                       # the main block's right edge; the porch is x 96..159
    for y in range(36, 96):
        for x in range(4, MX - 3):
            L.px(x, y, "cd1" if y > 44 else "cd0")
    for x in range(42, 54):
        for y in range(60, 96):
            e = y == 60 or x in (42, 53) or (x - 42) % 6 == 0
            L.px(x, y, "pg1" if e else "cd0")
    for k in range(1, 5):
        CK.paint_column(L, 16 * k + 8, 46, 96, "ionic", "poly")
    # antae: the cella's side walls, ashlar
    for ax in (2, MX - 11):
        for y in range(40, 97):
            for x in range(ax, ax + 10):
                c = "cm4" if x < ax + 4 else "cm3"
                if (y - 40) % 8 == 7 or (x + 4 * ((y - 40) // 8)) % 8 == 0:
                    c = "cm2"
                if x in (ax, ax + 9):
                    c = "cm0"
                L.px(x, y, c)
    # Ionic entablature: three fasciae, the dark-stone frieze with white figures, dentils
    for x in range(2, MX - 1):
        for j, c in enumerate(["cm0", "cm5", "cm4", "cm2", "cm5", "cm3", "cm1", "cm5", "cm4", "cm1"]):
            L.px(x, 36 + j, c if x not in (2, MX - 2) else "cm0")
    for x in range(2, MX - 1):
        for j in range(6):
            L.px(x, 30 + j, "cd1" if x not in (2, MX - 2) else "cm0")
        if x % 16 in (6, 7) and x < MX - 4:
            for j in range(1, 5):
                L.px(x, 30 + j, "cm5" if x % 16 == 6 else "cm3")
            L.px(x + 1, 30, "cm4")
        L.px(x, 29, "cm1" if x % 4 else "cm4")     # dentils
    pediment(L, 0, MX, 6, 25, color="pb1")
    # the Porch of the Maidens: x 96..159, lower, on a high podium
    P0, P1 = MX + 1, W * 16 - 1
    for y in range(48, 92):
        for x in range(P0 + 2, P1 - 1):
            L.px(x, y, "cd1" if y > 56 else "cd0")
    for x in range(P0, P1 + 1):
        L.px(x, 46, "cm0")
        L.px(x, 47, "cm5")
        L.px(x, 48, "cm4" if x % 4 else "cm1")      # dentils
        L.px(x, 49, "cm3")
        L.px(x, 50, "cm5" if x < P1 - 3 else "cm3")
        L.px(x, 51, "cm2")
        L.px(x, 52, "cm1")
    for k in range(4):
        karyatid(L, P0 + 8 + 16 * k, 53, 82, 0)
    for y in range(83, 112):
        for x in range(P0, P1 + 1):
            c = "cm4" if y < 86 else "cm3" if hp(x, y, 3) % 11 else "cm2"
            if y in (83, 111) or x in (P0, P1):
                c = "cm0"
            if y == 84:
                c = "cm5"
            if 86 <= y and (y - 86) % 8 == 7:
                c = "cm2"
            L.px(x, y, c)
    # the main block's krepis
    for s_ in range(2):
        a, b = 2 - 2 * s_, MX - 2 + 2 * s_
        y = 97 + 7 * s_
        for x in range(max(0, a), b + 1):
            for j in range(7):
                c = "cm5" if j == 0 else "cm4" if j < 3 else "cm3" if j < 6 else "cm1"
                L.px(x, y + j, "cm0" if x in (a, b) else c)
    shadow_band(L, 0, P1, 111, rows=1)
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    return cut(key, "the Erechtheion", W, H, {"middle": L}, ["X" * W] * H, names=names,
               notes="The Erechtheion (10 x 7) on borrowed path: the Ionic east porch with painted "
                     "capitals and its dark-stone frieze of white figures, the bronze doors, and the "
                     "Porch of the Maidens (cells 6-9) on its high podium. Solid.")


# --------------------------------------------------------------------------
# The Propylaia (13 x 7) and the temple of Athena Nike on its bastion
# --------------------------------------------------------------------------

def propylaia(key="propylaia"):
    """The Propylaia, 13 x 7: six Doric columns at a 32 px pitch (the 1-tile
    intercolumniation), five doorways in the gate wall behind them, a pediment.
    Column 6 is the passage: walkable all the way up, the doorway's dark floor
    on the bottom layer, the lintel and pediment over the player (top layer)."""
    W, H = 13, 7
    L = canvas(W, H)
    B = canvas(W, H)
    x1 = W * 16 - 1
    for y in range(50, 100):
        for x in range(2, x1 - 1):
            L.px(x, y, "cd1" if y > 56 else "cd0")
    # five doorways behind the gaps (cells 2, 4, 6, 8, 10), the middle one open
    for k, cell in enumerate((2, 4, 6, 8, 10)):
        a = cell * 16 + 2
        top = 66 if cell != 6 else 58
        for x in range(a, a + 12):
            for y in range(top, 100):
                e = x in (a, a + 11) or y == top
                L.px(x, y, "cm2" if e else "cd0")
        for x in range(a - 1, a + 13):
            L.px(x, top - 1, "cm4")
            L.px(x, top - 2, "cm3")
    for k in range(6):
        CK.paint_column(L, 24 + 32 * k, 52, 99, "doric", "poly")
    CK.paint_architrave(L, 2, x1 - 2, 44, 8)
    doric_frieze(L, 2, x1 - 2, 33, 16, rows=9, offset=6)
    pediment(L, 0, x1, 4, 30)
    # krepis of three low steps
    for s_ in range(3):
        y = 100 + 4 * s_
        a, b = 4 - s_, x1 - 4 + s_
        for x in range(a, b + 1):
            for j in range(4):
                c = "cm5" if j == 0 else "cm4" if j == 1 else "cm3" if j == 2 else "cm1"
                L.px(x, y + j, "cm0" if x in (a, b) else c)
    # the passage column: floor on the bottom, overhead parts on top
    px0 = 6 * 16
    for y in range(48, 112):
        for x in range(px0, px0 + 16):
            c = L.get(x, y)
            B.px(x, y, c if c else "cd0")
            L.px(x, y, None)
    # the passage's floor: worn marble paving in the dark
    for y in range(59, 100):
        for x in range(px0 + 1, px0 + 15):
            B.px(x, y, "cm1" if (y - 59) % 8 == 7 or (x - px0 + 4 * ((y - 59) // 8)) % 8 == 0 else "cd1")
    for y in range(100, 112):
        for x in range(px0, px0 + 16):
            t = (y - 100) % 4
            B.px(x, y, "cm5" if t == 0 else "cm4" if t == 1 else "cm3" if t == 2 else "cm1")
    walk = []
    for y in range(H):
        walk.append("".join("." if x == 6 else "X" for x in range(W)))
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    pas = [(6, y) for y in range(H)]
    s = cut(key, "the Propylaia", W, H, {"middle": L, "bottom": B}, walk, names=names,
            top_cells=[(6, y) for y in range(0, 3)],
            notes="The Propylaia (13 x 7): six Doric columns (painted) at a 32 px pitch, a doorway "
                  "behind every gap, and the passage up column 6, walkable: its floor is drawn on "
                  "the bottom layer and the lintel and pediment over the player. Rows 0-3 of "
                  "column 6 sit on borrowed path. Everything else is solid.")
    # the passage's upper cells need ground under the overhead art
    for y in range(0, 3):
        sl = np.s_[y * 16:y * 16 + 16, px0:px0 + 16]
        s.B.a[sl] = 0
        s.ground[(6, y)] = "path"
    for y in range(3, H):
        s.ground.pop((6, y), None)
    return s


def nike(key="nike"):
    """The little Ionic temple of Athena Nike (4 x 4) on borrowed path: four
    columns at a 16 px pitch, a pediment, a frieze; solid."""
    W, H = 4, 4
    L = canvas(W, H)
    for y in range(26, 56):
        for x in range(2, 62):
            L.px(x, y, "cd1" if y > 30 else "cd0")
    for k in range(4):
        CK.paint_column(L, 8 + 16 * k, 28, 56, "ionic", "marble")
    for x in range(1, 63):
        for j, c in enumerate(["cm0", "cm5", "cm3", "cm1", "pb1", "pb1", "pb1", "cm1"]):
            L.px(x, 18 + j, c if x not in (1, 62) else "cm0")
        if x % 6 == 3:
            L.px(x, 22, "cm5")
            L.px(x, 23, "cm4")
    pediment(L, 0, 63, 4, 15, sculpture=False)
    for s_ in range(2):
        y = 57 + 3 * s_
        for x in range(2 - s_, 62 + s_):
            for j in range(3):
                L.px(x, y + j, "cm5" if j == 0 else "cm3" if j == 1 else "cm1")
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    return cut(key, "the temple of Athena Nike", W, H, {"middle": L}, ["XXXX"] * H, names=names,
               notes="Athena Nike's little Ionic temple (4 x 4) on borrowed path, for the bastion "
                     "beside the Propylaia. Solid.")


def altar(key="altar", on="path", section="akropolis"):
    """The great altar (3 x 2) in front of a temple: a stepped block with a
    fire bowl's soot, horns at the corners; solid."""
    W, H = 3, 2
    L = canvas(W, H)
    for y in range(6, 28):
        for x in range(2, 46):
            c = "cm4" if y < 10 else "cm3" if x < 30 else "cm2"
            if y == 6:
                c = "cm5"
            if y in (10, 22):
                c = "cm1"
            if x in (2, 45) or y == 27:
                c = "cm0"
            L.px(x, y, c)
    for x in range(14, 34):
        for y in range(7, 10):
            L.px(x, y, "cd1" if (x + y) % 3 else "cd0")
    for (x, y) in ((2, 4), (3, 4), (2, 5), (44, 4), (45, 4), (45, 5)):
        L.px(x, y, "cm4")
    for x in range(8, 40, 6):
        L.px(x, 16, "pr1")                      # a painted garland
        L.px(x + 1, 17, "pr1")
        L.px(x + 2, 16, "pr1")
    shadow_band(L, 2, 46, 28, rows=3, c=CK.SHADOW.get(on, "ps"))
    return cut(key, "an altar", W, H, {"middle": L}, ["XXX", "XXX"], on=on, section=section,
               names={"L": (0, 0), "M": (1, 0), "R": (2, 0), "BL": (0, 1), "B": (1, 1), "BR": (2, 1)},
               notes="An altar (3 x 2): a marble block with corner horns, a garland and the fire's "
                     "soot, its shadow on the floor; solid. It stands outside, in front of the temple.")


def foundations(key="foundations", on="path"):
    """The Old Temple's foundations: a stylobate outline of grey blocks on
    borrowed path (walkable), as a 9-patch (TL T TR / L C R / BL B BR) plus
    'crack' (paving with grass in the joints) and 'step' (a half-buried step,
    the top two treads showing)."""
    names = {"TL": (0, 0), "T": (1, 0), "TR": (2, 0), "L": (0, 1), "C": (1, 1), "R": (2, 1),
             "BL": (0, 2), "B": (1, 2), "BR": (2, 2), "crack": (3, 0), "crack_b": (3, 1), "step": (3, 2)}
    s = struct(key, "the Old Temple's foundations", 4, 3, "akropolis", walk=["...."] * 3, names=names, on=on)
    Lm = s.M
    rmp = CK.RAMP["moss"]

    def block(x0, y0, w, hh):
        for y in range(y0, y0 + hh):
            for x in range(x0, x0 + w):
                e = x in (x0, x0 + w - 1) or y in (y0, y0 + hh - 1)
                c = rmp[0] if (y == y0 + hh - 1 or x == x0 + w - 1) else rmp[4] if y == y0 or x == x0 else rmp[3]
                if not e and hp(x, y, 9) % 13 == 0:
                    c = rmp[2]
                Lm.px(x, y, c)
    for n, (cx, cy) in names.items():
        ox, oy = cx * 16, cy * 16
        if n in ("T", "TL", "TR"):
            for bx in range(0, 16, 8):
                block(ox + bx, oy + 4, 8, 6)
        if n in ("B", "BL", "BR"):
            for bx in range(0, 16, 8):
                block(ox + bx, oy + 6, 8, 6)
        if n in ("L", "TL", "BL"):
            for by in range(0, 16, 8):
                block(ox + 3, oy + by, 6, 8)
        if n in ("R", "TR", "BR"):
            for by in range(0, 16, 8):
                block(ox + 7, oy + by, 6, 8)
        if n in ("crack", "crack_b"):
            for by in range(0, 16, 8):
                for bx in range(0, 16, 8):
                    if (bx + by + (cy * 8)) % 16 == 0 or n == "crack_b":
                        block(ox + bx, oy + by, 8, 8)
            for (dx, dy, c) in ((7, 3, "mo2"), (8, 4, "mo1"), (3, 8, "pp1"), (12, 11, "mo2"), (7, 15, "mo1")):
                Lm.px(ox + dx, oy + dy, c)
        if n == "step":
            for j in range(2):
                for x in range(ox, ox + 16):
                    Lm.px(x, oy + 6 + 5 * j, rmp[4])
                    for k in range(1, 4):
                        Lm.px(x, oy + 6 + 5 * j + k, rmp[3] if (x + k) % 7 else rmp[2])
                    Lm.px(x, oy + 10 + 5 * j, rmp[1])
            for (dx, dy, c) in ((3, 5, "mo2"), (4, 5, "mo1"), (11, 10, "mo2"), (12, 4, "iv2")):
                Lm.px(ox + dx, oy + dy, c)
    return s


def old_columns(key="old_columns", on="path"):
    """Two standing columns of the Old Temple (2 x 4), moss-weathered, of
    uneven height, one architrave block still across them (top layer: walk
    behind; the bases are solid)."""
    W, H = 2, 4
    L = canvas(W, H)
    CK.paint_column(L, 8, 9, 61, "doric", "moss")
    CK.paint_column(L, 24, 9, 61, "doric", "moss")
    # snap the right column's top under the block's broken end
    for x in range(16, 32):
        for y in range(0, 9):
            L.px(x, y, None)
    # the architrave block across both, cracked at the right end
    for x in range(1, 27):
        for y in range(3, 9):
            c = "wm4" if y == 3 else "wm3" if y < 7 else "wm1"
            if x in (1,) or y == 8:
                c = "wm0"
            if x > 22 and y < 3 + (x - 22):
                continue
            L.px(x, y, c)
    for x in range(4, 22, 5):
        L.px(x, 5, "mo2")
    CK.cast_shadow(L, 8, 63, "path", 8, 3)
    CK.cast_shadow(L, 24, 63, "path", 7, 3)
    walk = ["TT", "TT", "TT", "XX"]
    names = {"TL": (0, 0), "TR": (1, 0), "UL": (0, 1), "UR": (1, 1), "ML": (0, 2), "MR": (1, 2),
             "BL": (0, 3), "BR": (1, 3)}
    return cut(key, "two standing columns of the Old Temple", W, H, {"middle": L}, walk, names=names,
               top_rows=(0, 1, 2), on=on,
               notes="Two moss-weathered Doric columns (2 x 4) with one architrave block still across "
                     "them: the Old Temple, burned long ago. Rows 0-2 over the player, bases solid.")


def spring(key="spring", on="path"):
    """Poseidon's marks and the salt spring, by the Erechtheion's north porch
    (on borrowed path): 'trident' (three cuts in the rock, salt in the
    grooves; solid, read it), 'well_shut' (the sealed spring stone; solid),
    'well_open' (the stone pulled aside, a stair down into the dark: a door),
    'cleft' (a crack in the paving breathing salt air; solid) and 'rubble'
    (the cleft buried by the raid's fall; solid)."""
    names = {"trident": (0, 0), "well_shut": (1, 0), "well_open": (2, 0), "cleft": (3, 0), "rubble": (4, 0)}
    s = struct(key, "Poseidon's marks and the salt spring", 5, 1, "akropolis", walk=["XXDXX"], names=names, on=on)
    L = s.M
    # the trident marks: a worn rock outcrop with three long cuts
    b = mask_draw(16, 16, lambda d: d.polygon([(1, 13), (2, 5), (6, 2), (12, 3), (15, 7), (14, 14)], fill=1))
    for y in range(16):
        for x in range(16):
            if b[y, x]:
                L.px(x, y, rock_px(x, y + 5, 1))
    outline_mask(L, np.pad(b, ((0, 0), (0, 64))), "ar0")
    for cx in (5, 8, 11):
        for y in range(5, 12):
            L.px(cx, y, "ar0")
            L.px(cx - 1, y, "ar4")
        L.px(cx, 7, "ar5")                      # salt beads in the grooves
        L.px(cx, 10, "ar5")
    # the sealed stone and the opened stair
    for i, opened in ((1, False), (2, True)):
        ox = i * 16
        for y in range(2, 15):
            for x in range(1, 15):
                e = x in (1, 14) or y in (2, 14)
                c = "ar0" if e else "ar4" if y < 5 else "ar3" if x < 10 else "ar2"
                L.px(ox + x, y, c)
        if opened:
            for y in range(4, 14):
                for x in range(3, 13):
                    t_ = (y - 4) % 3
                    L.px(ox + x, y, "ar0" if y > 10 else "ar1" if t_ == 0 else "ar0")
            for x in range(3, 13):
                L.px(ox + x, 4, "ar1")
            L.px(ox + 6, 7, "aw2" if False else "ar2")
        else:
            # a trident and waves cut on the lid
            for y in range(5, 12):
                L.px(ox + 8, y, "ar1")
            for x in (5, 11):
                for y in range(5, 8):
                    L.px(ox + x, y, "ar1")
            for x in range(5, 12):
                L.px(ox + x, 8, "ar1")
            for x in range(3, 13):
                L.px(ox + x, 12, "ar1" if x % 3 else "ar4")
    # the cleft and its rubble
    ox = 48
    for (x, y) in ((3, 6), (4, 7), (5, 7), (6, 8), (7, 8), (8, 9), (9, 9), (10, 10), (11, 10), (12, 11)):
        L.px(ox + x, y, "ar0")
        L.px(ox + x, y + 1, "ar1")
        L.px(ox + x - 1, y - 1, "ar4")
    for (x, y) in ((6, 5), (9, 7), (11, 12)):
        L.px(ox + x, y, "ar5")
    ox = 64
    for (cx_, cy_, r_) in ((5, 10, 4), (10, 9, 4), (8, 5, 3), (12, 12, 2), (3, 13, 2)):
        m = mask_draw(16, 16, lambda d, cx_=cx_, cy_=cy_, r_=r_: d.ellipse([cx_ - r_, cy_ - r_, cx_ + r_, cy_ + r_ - 1], fill=1))
        for y in range(16):
            for x in range(16):
                if m[y, x]:
                    L.px(ox + x, y, "ar4" if x - cx_ + y - cy_ < -1 else "ar3" if x - cx_ + y - cy_ < 2 else "ar1")
    for x in range(4, 16):
        if L.get(ox + x, 15) is None:
            L.px(ox + x, 15, "ps")
    s.behaviors[(2, 0)] = "MB_NON_ANIMATED_DOOR"
    s.notes = ("Poseidon's marks: `trident` (read it), `well_shut` and `well_open` (the salt spring's stone, "
               "shut and opened: a door down to the Salt Well), `cleft` (the spring stair's crack) and "
               "`rubble` (the cleft after the raid). Scripts swap them: METATILE_Akropolis_WellOpen, "
               "METATILE_Akropolis_Rubble.")
    return s


def akropolis_structures():
    """Every structure gTileset_Akropolis holds, by key."""
    out = {}
    cl = cliff("path")
    cl = K.pick(cl, ["lip", "lip_b", "lip_W", "lip_E", "lip_in_W", "lip_in_E", "face", "face_b", "face_W",
                     "face_E", "rock", "foot", "foot_b", "foot_W", "foot_E"], w=5, key="cliff",
                notes="The Akropolis rock's face, three cells tall: `lip` (`lip_b`) along the top of the "
                      "drop, `face` (`face_b`, `face_bush`) below it, `foot` (`foot_b`) on the lower "
                      "ground with the cast shadow; `_W` and `_E` ends; `lip_in_W` `lip_in_E` where the "
                      "rim turns north; `rock` is solid bare rock. All solid.")
    ed = K.pick(plateau_edge(), ["edge_W", "edge_E", "wall_N", "wall_N_drums", "wall_N_face",
                                 "wall_N_face_d"], w=6, key="edge",
                notes="The plateau's rims: `edge_W` and `edge_E` (the drop off-map), and the north wall, "
                      "top `wall_N` (`wall_N_drums`) over face `wall_N_face` (`wall_N_face_d`, with old "
                      "column drums built in). All solid.")
    import astyra_statues as ST
    for s in (cl, ed, ramp_kit(), parthenon(), ST.promachos(), erechtheion(),
              propylaia(), altar(), foundations(), old_columns(), spring(),
              K.pick(CK.ruins("moss", "path", key="ruins"),
                     ["stub", "drum", "cap_doric", "plinth_feet", "poppies"], w=5, key="ruins"),
              CK.free_column("doric", "moss", 3, "path", key="col_moss3")):
        out[s.key] = s
    return out


if __name__ == "__main__":
    by = akropolis_structures()
    out = K.ROOT / "build/astyra_art"
    out.mkdir(parents=True, exist_ok=True)
    K.shelf_preview(list(by.values()), scale=2, width=1800).save(out / "akropolis_pieces.png")
    print(out / "akropolis_pieces.png")
