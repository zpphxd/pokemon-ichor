"""Trophonios's cave: the kit. Walls (a dark cap and a tall limestone face),
the floor and its shadows, the priests' paving, the underground Herkyna and
its ford, ledges.

Walls are drawn as two parts, both chosen by the map builder
(tools/ichor/maps/trophonios.py) from a grid of rock and floor:

  cap   rock seen from above. One piece per blob shape key over the rock
        region (face cells count as rock), with a lit rim where the rock
        meets the floor to its north, west or east.
  face  the south face of every rock mass, H cells tall (1 to 3: the lowest
        H rock cells above a floor cell). A face piece is named
        "H r t e": its height H, its row r (0 = top), its top t ("c" under
        the cap, "f" free-standing, floor above) and its ends e ("M" running
        on both sides, "W" ending on the west, "E" on the east, "B" both).

The shapes the maps use are listed in trophonios_shapes.json
(`trophonios.py --shapes` writes it), and only those are drawn.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import trophonios_lib as T

SEC = "kit"
SHAPES = Path(__file__).resolve().parent / "trophonios_shapes.json"
FULL = "1|11111111"


def wanted(kind):
    defaults = {
        "cap": [FULL, "1|00111110", "1|10001111", "1|11100011", "1|00111000", "1|10000011",
                "1|00001110", "1|11111000", "1|10001110", "1|00100010"],
        "face": ["20cM", "21cM", "20cW", "21cW", "20cE", "21cE", "30fM", "31fM", "32fM"],
        "water": [FULL, "1|00100010", "1|00111000", "1|10000011", "1|10001111", "1|11111000"],
    }
    keys = list(defaults[kind])
    if SHAPES.exists():
        keys = sorted(set(json.loads(SHAPES.read_text()).get(kind, [])) | {defaults[kind][0]})
    if kind != "face" and FULL in keys:
        keys.remove(FULL)
        keys.insert(0, FULL)
    # variants the map builder scatters, so big runs never repeat one cell
    if kind == "cap":
        keys[1:1] = [FULL + "~1", FULL + "~2"]
    if kind == "face":
        keys += [k + f"~{v}" for k in list(keys) if k.endswith("M") and "~" not in k for v in (1, 2)]
    return keys


def shape_set(key, title, keys, painter, walk_code, notes):
    w = 8
    h = max(1, (len(keys) + w - 1) // w)
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = T.struct(key, title, w, h, SEC, walk=[walk_code * w] * h, notes=notes, names=names)
    for n in range(w * h):
        cx, cy = n % w, n // w
        painter(s, cx * 16, cy * 16, keys[min(n, len(keys) - 1)])
    return s


# --------------------------------------------------------------------------
# The cap
# --------------------------------------------------------------------------

def paint_cap(s, ox, oy, key):
    key, _, var = key.partition("~")
    var = int(var or 0)
    V = T.soft(key, margin=1.0, radius=3.0, amp=1.4, seed=2.3, jag=0.5)
    c = np.s_[16:32, 16:32]
    v = V[c]
    full = v.all()
    L = s.B if full else s.M
    if not full:
        T.floor_cell(s.B, ox, oy, 0)
    for y in range(16):
        for x in range(16):
            if v[y, x]:
                L.px(ox + x, oy + y, T.cap_px(ox + x, oy + y, var))
    if full:
        return
    # the rim: lit on the west and north, dark on the east; a dark line outside
    rim = T.ring(V)[c] & v
    for y, x in np.argwhere(rim):
        W = not V[y + 16, x + 15]
        N = not V[y + 15, x + 16]
        Ee = not V[y + 16, x + 17]
        if W or N:
            L.px(ox + x, oy + y, "fc2" if (x + y) % 3 else "fc1")
        elif Ee:
            L.px(ox + x, oy + y, "fc0")
        else:
            L.px(ox + x, oy + y, "cp1")
    for y, x in np.argwhere(T.halo(V)[c]):
        L.px(ox + x, oy + y, "tink")


def cap():
    return shape_set("cap", "Rock seen from above: the cap", wanted("cap"), paint_cap, "X",
                     "The dark top of every rock mass. Names are blob shape keys over the rock "
                     "region (face cells count as rock); edge pieces draw the rock in the middle "
                     "layer over the plain floor. Impassable.")


# --------------------------------------------------------------------------
# The face
# --------------------------------------------------------------------------

FACE_SEED = 4


def face_mask(end, top_free):
    """Which pixels of a face cell are rock (bool 16 x 16): the ends curve in."""
    m = np.ones((16, 16), bool)
    for y in range(16):
        inset = 2 + (1 if (y // 3) % 2 else 0)
        if end in ("W", "B"):
            m[y, :inset] = False
        if end in ("E", "B"):
            m[y, 16 - inset:] = False
    return m


def paint_face_cell(s, ox, oy, H, r, top, end, L=None, floor_variant=0, variant=0):
    """One cell of a face H tall, row r. Full-width faces go in the bottom
    layer; ends (W, E, B) in the middle layer over the floor."""
    m = face_mask(end, top == "f")
    whole = m.all()
    if L is None:
        L = s.B if whole else s.M
    if not whole:
        T.floor_cell(s.B, ox, oy, floor_variant)
    T.paint_face(L, ox, oy, r, H, FACE_SEED, mask=m, variant=variant)
    # the lip: the top row of the face
    if r == 0:
        for x in range(16):
            if not m[0, x]:
                continue
            if top == "c":
                L.px(ox + x, oy + 0, "cp1")
                L.px(ox + x, oy + 1, "fc5" if (x % 5) else "fc4")
                L.px(ox + x, oy + 2, "fc4")
            else:
                # free-standing: the floor above ends in a worn edge
                L.px(ox + x, oy + 0, "fc5" if x % 4 else "fc4")
                L.px(ox + x, oy + 1, "fc4")
                L.px(ox + x, oy + 2, "fc3" if x % 3 else "fc4")
    # the base: the face meets the floor in deep shadow
    if r == H - 1:
        for x in range(16):
            if m[15, x]:
                L.px(ox + x, oy + 15, "fc0")
                if x % 2:
                    L.px(ox + x, oy + 14, "fc0")
    # the ends: a dark edge
    for y in range(16):
        xs = np.nonzero(m[y])[0]
        if len(xs) == 0:
            continue
        if end in ("W", "B"):
            L.px(ox + int(xs[0]), oy + y, "fc1" if y > 2 else "fc3")
        if end in ("E", "B"):
            L.px(ox + int(xs[-1]), oy + y, "fc0" if y > 2 else "fc2")
            if len(xs) > 1:
                L.px(ox + int(xs[-2]), oy + y, "fc1")


def paint_face_key(s, ox, oy, k):
    k, _, var = k.partition("~")
    H, r, top, end = int(k[0]), int(k[1]), k[2], k[3]
    paint_face_cell(s, ox, oy, H, r, top, end, variant=int(var or 0))


def face():
    keys = wanted("face")
    return shape_set("face", "The limestone face", keys, paint_face_key, "X",
                     "The south face of every rock mass, 1 to 3 cells tall. Names are "
                     "`H r t e`: height, row (0 = top), top (`c` under the cap, `f` with floor "
                     "above) and ends (`M` none, `W`, `E`, `B` both). Impassable.")


# --------------------------------------------------------------------------
# The floor
# --------------------------------------------------------------------------

FLOOR_NAMES = ["plain", "pebbles", "crack", "damp", "gravel", "flat", "plain_b", "plain_c"]


def floor():
    names = {n: (i, 0) for i, n in enumerate(FLOOR_NAMES)}
    names.update({"sh": (0, 1), "shW": (1, 1), "shE": (2, 1), "shB": (3, 1),
                  "sh_b": (4, 1), "sh_c": (5, 1)})
    s = T.struct("floor", "The cave floor", 8, 2, SEC, walk=["........", "........"], names=names,
                 notes="`plain` (and `plain_b`, `plain_c`, mottled differently), `pebbles`, "
                       "`crack`, `damp`, `gravel` and `flat` (a stone set in the clay); `sh` the "
                       "floor below a face, in its shadow (`sh_b`, `sh_c` vary it; `shW`, `shE`, "
                       "`shB` where the face above ends on that side).")
    for i in range(8):
        T.floor_cell(s.B, i * 16, 0, i)
    for i, (end, var) in enumerate((("M", 0), ("W", 0), ("E", 0), ("B", 0), ("M", 6), ("M", 7),
                                    ("M", 7), ("M", 7))):
        ox, oy = i * 16, 16
        T.floor_cell(s.B, ox, oy, var)
        m = face_mask(end, False)
        for x in range(16):
            if not m[15, x]:
                continue
            for y in range(4):
                cur = s.B.get(ox + x, oy + y)
                if y == 0 or (y == 1 and (x % 2 == 0)):
                    s.B.px(ox + x, oy + y, "cs0")
                elif y < 3 or (x + y) % 2 == 0:
                    s.B.px(ox + x, oy + y, {"fl2": "fl1", "fl3": "fl2", "fl1": "fl0"}.get(cur, cur))
    return s


def pave():
    """The priests' paving in the upper chamber: big cut flags with grout, a
    worn curb at the edges where the cave floor begins."""
    names = {"tl": (0, 0), "t": (1, 0), "tr": (2, 0), "l": (0, 1), "c": (1, 1), "r": (2, 1),
             "bl": (0, 2), "b": (1, 2), "br": (2, 2), "c2": (3, 0), "c3": (3, 1), "worn": (3, 2)}
    s = T.struct("pave", "The priests' paving", 4, 3, SEC, walk=["....", "....", "...."],
                 names=names,
                 notes="Cut limestone flags in the upper chamber: a rectangle of `tl` `t` `tr` / "
                       "`l` `c` `r` / `bl` `b` `br`; `c2`, `c3` and `worn` vary the middle.")

    def flag_px(x, y, seed):
        # flags 8 x 8 offset every other row, 1 px grout
        row = y // 8
        xo = (x + (4 if row % 2 else 0)) % 8
        if y % 8 == 7 or xo == 7:
            return "fl1"
        if y % 8 == 0 or xo == 0:
            return "pv1" if (x + y) % 5 else "pv2"
        h = T.hsh(x, y, seed) % 100
        return "fl3" if h < 22 else ("fl4" if h < 88 else "pv1")

    for cy in range(3):
        for cx in range(4):
            ox, oy = cx * 16, cy * 16
            seed = 1 if cx < 3 else 2 + cy
            for y in range(16):
                for x in range(16):
                    s.B.px(ox + x, oy + y, flag_px(x, y, seed))
            if cx == 3 and cy == 2:
                # worn: a hollow in the middle where feet have stood
                m = T.ellipse_mask(16, 16, 8, 8, 5.5, 4)
                for y, x in np.argwhere(m):
                    s.B.px(ox + x, oy + y, "fl3" if (x + y) % 2 else "fl4")
            if cx < 3:
                # edges: the paving ends in a worn curb on the cave floor
                for y in range(16):
                    for x in range(16):
                        gx, gy = x, y
                        out = False
                        if cy == 0 and gy < 3:
                            out = True
                        if cy == 2 and gy > 12:
                            out = True
                        if cx == 0 and gx < 3:
                            out = True
                        if cx == 2 and gx > 12:
                            out = True
                        if out:
                            s.B.px(ox + x, oy + y, T.floor_px(x, y))
                        else:
                            edge = (cy == 0 and gy == 3) or (cy == 2 and gy == 12) or \
                                   (cx == 0 and gx == 3) or (cx == 2 and gx == 12)
                            if edge:
                                s.B.px(ox + x, oy + y, "fl0" if (cy == 2 or cx == 2) else "pv2")
    return s


# --------------------------------------------------------------------------
# The underground Herkyna
# --------------------------------------------------------------------------

WATER_FLOOR = {"fl4": "fl3", "fl5": "fl3", "fl0": "fl1"}


def water_px(x, y, seed=0):
    """Dark running water, flowing west: long streaks."""
    xx = (x + (y * 3)) % 16
    band = (y + (x // 6)) % 4
    if band == 0 and xx < 6:
        return "wa3"
    if band == 2 and 8 <= xx < 11:
        return "wa2"
    return "wa1" if (x + 2 * y) % 7 else "wa2"


def paint_water(s, ox, oy, key):
    V = T.soft(key, margin=1.5, radius=3.0, amp=1.2, seed=5.1, jag=0.4)
    c = np.s_[16:32, 16:32]
    v = V[c]
    for y in range(16):
        for x in range(16):
            if v[y, x]:
                s.B.px(ox + x, oy + y, water_px(ox + x, y))
            else:
                f = T.floor_px(x, y)
                s.B.px(ox + x, oy + y, WATER_FLOOR.get(f, f))
    # the bank: pebbles at the waterline, foam where it rubs
    for y, x in np.argwhere(T.ring(V)[c] & v):
        s.B.px(ox + x, oy + y, "fm" if (x * 3 + y) % 7 == 0 else "wa3")
    for y, x in np.argwhere(T.halo(V)[c]):
        s.B.px(ox + x, oy + y, "fc2" if (x + y) % 3 else "fc1")
    h2 = T.halo(T.halo(V) | V)[c]
    for y, x in np.argwhere(h2):
        if (x + 2 * y) % 4 == 0:
            s.B.px(ox + x, oy + y, "fc3")


def water():
    return shape_set("water", "The underground Herkyna", wanted("water"), paint_water, "X",
                     "Dark running water with pebbly banks, the river Herkyna under the hill. "
                     "Names are blob shape keys. Not surfable: blocked.")


def ford():
    """Where the stream runs shallow over stones: walkable (MB_SHALLOW_WATER)."""
    names = {"top": (0, 0), "bot": (0, 1), "one": (1, 0), "stones": (1, 1)}
    s = T.struct("ford", "The ford", 2, 2, SEC, walk=["..", ".."], names=names,
                 notes="The stream shallow over flat stones, walkable: `top` over `bot` across a "
                       "two-row stream, `one` across a one-row stream (banks on both sides), "
                       "`stones` a shallow cell with no banks. MB_SHALLOW_WATER.")
    for (cx, cy) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        ox, oy = cx * 16, cy * 16
        bank_n = (cx, cy) in ((0, 0), (1, 0))
        bank_s = (cx, cy) in ((0, 1), (1, 0))
        for y in range(16):
            for x in range(16):
                if (bank_n and y < 3) or (bank_s and y > 12):
                    f = T.floor_px(x, y)
                    s.B.px(ox + x, oy + y, WATER_FLOOR.get(f, f))
                    continue
                c = "wa3" if (x + y * 2) % 5 else "wa4"
                s.B.px(ox + x, oy + y, c)
        # flat stepping stones
        for (sx, sy) in ((3, 5), (10, 4), (6, 10), (12, 11)):
            m = T.ellipse_mask(16, 16, sx, sy, 2.6, 1.8)
            for y, x in np.argwhere(m):
                if 0 <= y < 16 and 0 <= x < 16:
                    s.B.px(ox + x, oy + y, "fc3" if y < sy else "fc2")
        for x in range(16):
            if bank_n:
                s.B.px(ox + x, oy + 3, "fc2" if x % 3 else "fm")
            if bank_s:
                s.B.px(ox + x, oy + 12, "fm" if x % 4 == 1 else "wa4")
        s.behaviors[(cx, cy)] = "MB_SHALLOW_WATER"
    return s


# --------------------------------------------------------------------------
# Ledges
# --------------------------------------------------------------------------

def ledge():
    names = {"W": (0, 0), "M": (1, 0), "E": (2, 0)}
    s = T.struct("ledge", "A rock ledge (jump south)", 3, 1, SEC, walk=["JJJ"], names=names,
                 notes="A low step in the floor, hopped down southward: `W` `M` `E`.")
    # a short limestone step: the shelf's worn lip, a face 8 px tall, its shadow below
    for cx, end in enumerate(("W", "M", "E")):
        ox = cx * 16
        T.floor_cell(s.B, ox, 0, 0)
        x0 = 2 if end == "W" else 0
        x1 = 13 if end == "E" else 15
        for x in range(16):
            for y in (14, 15):
                if x0 <= x <= x1 and (y == 14 or x % 2):
                    s.B.px(ox + x, y, "cs0")
        for x in range(x0, x1 + 1):
            s.M.px(ox + x, 4, "fc5" if x % 3 else "fc4")
            s.M.px(ox + x, 5, "fc4")
            for y in range(6, 13):
                s.M.px(ox + x, y, T.face_px(x, y - 2, 0, 1, 4, cx))
            s.M.px(ox + x, 13, "fc0")
        for y in range(4, 14):
            if end == "W":
                s.M.px(ox + x0, y, "fc1")
            if end == "E":
                s.M.px(ox + x1, y, "fc0")
    return s


def build():
    return [cap(), face(), floor(), pave(), water(), ford(), ledge()]
