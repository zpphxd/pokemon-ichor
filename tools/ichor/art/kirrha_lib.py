"""Shared toolkit for gTileset_Kirrha, the two harbor towns of the Gulf crossing.

Kirrha is Delphoi's harbor at the head of the Krisaian gulf, under the grey
cliffs of Parnassos; Aigion is an Achaean port on a terrace across the gulf.
One secondary serves both towns and Panopeus's ferry between them (Route 10),
on the `aethos` primary. It draws with emporion_lib's Struct (borrowed aethos
ground per cell) and kalliste_lib's Layer and sheet packing, and adds:

  - Kirrha's palette plan: seven groups for the secondary's slots 6-12. Every
    8x8 tile of every layer takes all its colors from one group; validate()
    enforces it.
  - The grey limestone of Parnassos ("crag"): a neutral grey drawn from
    aethos's own warm greys (168,160,152 and 128,120,112), with the rust
    streaks of the Phaidriades, laurel scrub in the cracks, and aethos's grass
    on the rims, so the crags sit on aethos ground and read as the same
    mountain coast as SCRIPT.md Part 10's `parnassos` set.
  - "clay" (limewash, laurel-green shutters: Kirrha) and "clay2" (ochre
    stucco, blue shutters: Aigion) are parallel slot for slot, so an Aigion
    house part is the Kirrha part's own tile in another palette.
  - Ground per cell: borrowed aethos ground ("grass", "path", "sand", "sea":
    the bottom layer points at aethos's metatile, so the sea under a moored
    boat animates with the gulf around it), the grey quay paving ("quay"),
    the ferry's deck planks ("deck"), or "none".

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_lib as E  # noqa: E402
import kalliste_lib as K  # noqa: E402
from kalliste_lib import Layer, tile_colors  # noqa: E402,F401

ROOT = K.ROOT

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # Parnassos limestone: neutral grey, aethos's warm greys in the middle of the ramp
    "pg0": (48, 48, 56), "pg1": (88, 88, 96), "pg2": (128, 120, 112), "pg3": (168, 160, 152),
    "pg4": (200, 192, 184), "pg5": (232, 224, 216), "prs": (160, 112, 80),
    # laurel scrub and weed in the cracks, wet stone's algae
    "lv0": (32, 56, 40), "lv1": (56, 88, 56), "lv2": (96, 128, 72),
    # Kirrha's limewash and laurel-green shutters
    "lm0": (152, 144, 136), "lm1": (192, 184, 176), "lm2": (232, 224, 216), "lm3": (248, 240, 232),
    "dg0": (40, 80, 64), "dg1": (72, 128, 96),
    # Aigion's ochre stucco and blue shutters (the parallel of the above)
    "ko0": (152, 104, 48), "ko1": (192, 144, 72), "ko2": (224, 184, 112), "ko3": (240, 216, 160),
    "kb0": (40, 72, 128), "kb1": (80, 120, 184),
    # sail linen, tar
    "sa0": (216, 208, 184), "kt": (64, 56, 56),
    # under clear water: the drowned town's roofs and walls
    "sub0": (64, 88, 128), "sub1": (96, 112, 144), "sub2": (136, 144, 160), "tq": (88, 176, 200),
    # leaves: laurel (dark, glossy), plane and fig (fresh); plane bark
    "lr0": (24, 48, 40), "lr1": (48, 80, 56), "lf1": (96, 144, 72), "lf2": (152, 192, 104),
    "tk2": (184, 176, 152),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # Grey limestone: the crags, the quay, piers, the gate's posts; laurel scrub and
    # algae; aethos's grass on rims and at feet.
    "crag": ["ink", "pg0", "pg1", "pg2", "pg3", "pg4", "pg5", "prs", "lv0", "lv1", "lv2",
             "gr0", "gr1", "gr2", "e1"],
    # Kirrha's houses: terracotta, limewash, laurel-green paint, door timber.
    "clay": ["ink", "tc0", "tc1", "tc2", "tc3", "lm0", "lm1", "lm2", "lm3", "dg0", "dg1",
             "wd0", "wd1", "pg1", "pg3"],
    # Aigion's houses, slot for slot: ochre stucco and blue paint.
    "clay2": ["ink", "tc0", "tc1", "tc2", "tc3", "ko0", "ko1", "ko2", "ko3", "kb0", "kb1",
              "wd0", "wd1", "pg1", "pg3"],
    # Timber, rope, linen and paint: boats, nets, racks, the shed, the gate, the deck.
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "sa0", "oc1", "rd", "b0", "b1",
             "b2", "lv1", "b3"],
    # Drawn water, foam, and what lies under it.
    "sea": ["ink", "w0", "b0", "wa1", "b1", "wr", "wa3", "b2", "b3", "tq", "sub0", "sub1",
            "sub2", "pg3", "pg4"],
    # Trees on aethos grass: laurel, olive, fig, plane.
    "grove": ["ink", "gr0", "gr1", "gr2", "ov0", "ov1", "ov2", "ov3", "lr0", "lr1", "lf1",
              "lf2", "tk0", "tk1", "tk2"],
    # Marble, bronze and the market's goods: fish, bread, amphorae, Delphoi's roofs, the
    # altar of Zeus.
    "market": ["ink", "w0", "m1", "m2", "m3", "m4", "g0", "g1", "tc0", "tc1", "tc2", "sl2",
               "sl3", "br", "rd"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# clay -> clay2: an Aigion house part is the Kirrha part, slot for slot
AIGION = dict(zip(GROUPS["clay"], GROUPS["clay2"]))

# Ground kinds: "quay" and "deck" are drawn here; the rest are aethos's.
E.DRAWN.update({"quay", "deck"})
Struct = E.Struct


def struct(key, title, w, h, walk=None, notes="", ground="none", section="harbor"):
    return Struct(key, title, w, h, walk=walk, notes=notes, ground=ground, section=section)


def ground(s, kind, cells=None):
    s.set_ground(kind, cells)


# --------------------------------------------------------------------------
# Stone
# --------------------------------------------------------------------------

def quay_paving(L, x0, y0, w, h, ox=0, oy=0):
    """Kirrha's quay: big grey limestone blocks in running bond, soft joints,
    a lit top edge on each course. Repeats every 16 px."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 16, (y - oy) % 16
            row = Y // 8
            off = 0 if row == 0 else 8
            bx, by = (X + off) % 16, Y % 8
            if by == 7 or bx == 15:
                c = "pg2"
            elif by == 0:
                c = "pg4"
            else:
                c = "pg3"
                if (bx, by) in ((4, 3), (11, 5), (7, 2)) and row == 0 or \
                        (bx, by) in ((2, 4), (9, 2), (13, 5)) and row == 1:
                    c = "pg2"
                elif (bx, by) in ((1, 1), (2, 1)):
                    c = "pg4"
            L.px(x, y, c)


def coping_n(L, x, y, w):
    """The quay's edge with water beyond to the north: rounded coping."""
    L.hline(x, x + w - 1, y, "pg1")
    L.hline(x, x + w - 1, y + 1, "pg5")
    L.hline(x, x + w - 1, y + 2, "pg4")
    L.hline(x, x + w - 1, y + 3, "pg4")
    L.hline(x, x + w - 1, y + 4, "pg2")
    for jx in range(x + 7, x + w, 16):
        L.vline(jx, y + 1, y + 4, "pg2")


def quay_face(L, x, y, w, h):
    """The quay's face, wet toward the waterline, weed at its foot."""
    for j in range(h):
        for i in range(w):
            X, Y = x + i, y + j
            row = j // 4
            off = 8 if row % 2 else 0
            bx, by = (X + off) % 16, j % 4
            wet = j >= h - 4
            if bx == 15 or by == 3:
                c = "pg0" if wet else "pg1"
            elif by == 0:
                c = "pg3" if not wet else "pg2"
            else:
                c = "pg2" if not wet else "pg1"
            if j == h - 1 or (j == h - 2 and X % 3 == 0):
                c = "lv1"
            L.px(X, Y, c)


# The crag's face: Voronoi lumps on a 32 px torus, narrow and tall (limestone
# weathers into vertical flutes), each lump lit along its top-left and shaded at
# its bottom-right, thin dark crevices between them, rust down a couple.
_FACE = {}


def _voronoi(period, n, seed, sx, sy):
    rnd = random.Random(seed)
    pts = []
    k = int(math.ceil(math.sqrt(n)))
    cell = period / k
    for j in range(k):
        for i in range(k):
            if len(pts) >= n:
                break
            pts.append(((i + 0.15 + 0.7 * rnd.random()) * cell, (j + 0.15 + 0.7 * rnd.random()) * cell))
    yy, xx = np.mgrid[0:period, 0:period]
    best = np.full((period, period), 1e9)
    second = np.full((period, period), 1e9)
    lab = np.zeros((period, period), int)
    offx = np.zeros((period, period))
    offy = np.zeros((period, period))
    for idx, (px, py) in enumerate(pts):
        for ox in (-period, 0, period):
            for oy in (-period, 0, period):
                dx, dy = xx - px - ox, yy - py - oy
                d = np.hypot(dx * sx, dy * sy)
                upd = d < best
                second = np.where(upd, best, np.minimum(second, d))
                best = np.where(upd, d, best)
                lab = np.where(upd, idx, lab)
                offx = np.where(upd, dx, offx)
                offy = np.where(upd, dy, offy)
    return lab, best, second, offx, offy


_RAMP = ["pg1", "pg2", "pg3", "pg4", "pg5"]
_BASE = (3, 3, 2, 3, 2, 3, 3, 2, 3, 2)


def _face_tex():
    if "t" in _FACE:
        return _FACE["t"]
    P = 32
    lab, d1, d2, offx, offy = _voronoi(P, 9, 17, sx=1.5, sy=0.75)
    gap = d2 - d1
    out = np.empty((P, P), object)
    for y in range(P):
        for x in range(P):
            b = lab[y, x]
            g = gap[y, x]
            if g < 0.75:
                out[y, x] = "pg0" if g < 0.4 else "pg1"
                continue
            i = _BASE[b % len(_BASE)]
            # lit toward the top left, shaded toward the bottom right
            t = offx[y, x] * 0.7 + offy[y, x] * 1.0
            edge = g < 2.2
            if edge and t < -1.0:
                i += 2
            elif t < -3.5:
                i += 1
            elif edge and t > 1.0:
                i -= 1
            elif t > 4.0:
                i -= 1
            out[y, x] = _RAMP[max(0, min(4, i))]
    # rust streaks down two lumps
    for (rx, ry0, ry1) in ((9, 4, 15), (24, 18, 27)):
        for y in range(ry0, ry1):
            if out[y, rx] in ("pg3", "pg2", "pg4"):
                out[y, rx] = "prs"
            if y % 3 == 0 and out[y, rx + 1] in ("pg3", "pg2"):
                out[y, rx + 1] = "prs"
    _FACE["t"] = out
    return out


def crag_face(L, x0, y0, w, h, ox=0, oy=0, seed=0, rust=True):
    """The grey face of a Parnassos crag: fluted limestone in irregular lumps, each
    lit along its top-left and shaded at its bottom-right, thin dark crevices
    between, rust streaks down two of them, the way the Phaidriades shine.
    Repeats every 32 px both ways: a cell at map column c and row r meets its
    neighbors when ox = -16 * (c % 2) and oy = -16 * (r % 2) (the cliff kit carries
    both phases)."""
    tex = _face_tex()
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = tex[(y - oy) % 32][(x - ox) % 32]
            if not rust and c == "prs":
                c = "pg3"
            L.px(x, y, c)


def crag_rim(L, x0, y0, w, oy=0):
    """The crag's lit top lip: a pale band with dark undercut, scrub in the
    joints. Drawn 5 px tall from y0."""
    for x in range(x0, x0 + w):
        L.px(x, y0, "pg1")
        L.px(x, y0 + 1, "pg5")
        L.px(x, y0 + 2, "pg4")
        L.px(x, y0 + 3, "pg3")
        L.px(x, y0 + 4, "pg1")


def scrub(L, x, y, big=False, seed=0):
    """A tuft of laurel scrub clinging to the rock: 5x3 (or 7x4)."""
    if big:
        L.blit(["  121  ", " 12221 ", "1222101", " 10001 "],
               {"1": "lv1", "2": "lv2", "0": "lv0"}, x, y)
    else:
        L.blit([" 121 ", "12201", " 000 "], {"1": "lv1", "2": "lv2", "0": "lv0"}, x, y)


# --------------------------------------------------------------------------
# Timber, linen, water
# --------------------------------------------------------------------------

def planks(L, x0, y0, w, h, ox=0, oy=0, horizontal=True):
    """Weathered deck planks, 4 px wide, butt joints staggered. Repeats every 16 px."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 16, (y - oy) % 16
            if not horizontal:
                X, Y = Y, X
            row = Y // 4
            by = Y % 4
            joint = (X + row * 5) % 16 == 0
            if by == 3:
                c = "wd1"
            elif joint:
                c = "wd1"
            elif by == 0:
                c = "wd3"
            else:
                c = "wd2"
                if (X * 7 + row * 3) % 13 == 0:
                    c = "wd3"
            L.px(x, y, c)


def sea(L, x, y, w, h):
    """Open water drawn to match aethos's calm sea (b1 with wr ripples); it does
    not animate, so use it only where a drawn thing sits in the water."""
    L.rect(x, y, w, h, "b1")
    rip = [(7, 0), (8, 1), (8, 2), (9, 3), (9, 4), (10, 5), (11, 6), (12, 6), (13, 7), (14, 7),
           (15, 8), (0, 9), (0, 10), (1, 11), (1, 12), (2, 13), (3, 14), (4, 14), (5, 15), (6, 15)]
    for j in range(y, y + h):
        for i in range(x, x + w):
            if ((i % 16), (j % 16)) in rip:
                L.px(i, j, "wr")


def boat_eye(L, x, y):
    L.blit(["  kkk  ", " kwwbk ", "kwwbbwk", " kkkkk "], {"k": "ink", "w": "w0", "b": "b0"}, x, y)


def foam_line(L, x0, x1, y, every=3):
    """A ragged line of foam and shadow along a hull's waterline (sea group)."""
    for x in range(x0, x1 + 1):
        L.px(x, y, "wa1")
        if (x - x0) % every == 0:
            L.px(x, y + 1, "b3")


# --------------------------------------------------------------------------
# Validation (emporion_lib's, against Kirrha's groups)
# --------------------------------------------------------------------------

def validate(structs):
    problems = []
    for s in structs:
        gr = s.borrowed
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if not cols:
                        continue
                    if not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                n = sum(1 for layer in s.layers.values() if (layer.a[sl][..., 3] > 0).any())
                if n == 3:
                    problems.append(f"{s.key} metatile ({cx},{cy}) has three layers")
                if (cx, cy) in gr:
                    if (s.B.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground draws a bottom")
                    if (s.T.a[sl][..., 3] > 0).any() and (s.M.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground uses both upper layers")
                    continue
                lower = np.maximum(s.B.a[sl][..., 3], s.M.a[sl][..., 3])
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} ({cx},{cy}) has holes below the sprites layer")
    return problems


# --------------------------------------------------------------------------
# Finishing
# --------------------------------------------------------------------------

def finish(s, phase=(0, 0)):
    """Paint drawn ground ("quay", "deck") under the art, phase-locked so a prop on
    the quay meets the quay around it, then resolve layers as emporion_lib does: a
    drawn-ground cell that drew in both upper layers has its middle layer
    composited down into the bottom."""
    B, M, T = s.B, s.M, s.T
    for (cx, cy), kind in s.ground.items():
        sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        if kind in ("quay", "deck"):
            g = Layer(16, 16)
            if kind == "quay":
                quay_paving(g, 0, 0, 16, 16)
            else:
                planks(g, 0, 0, 16, 16)
            art = B.a[sl].copy()
            if (art[..., 3] > 0).any():
                up = M.a[sl].copy()
                m = up[..., 3] > 0
                art[m] = up[m]
                M.a[sl] = art
            B.a[sl] = g.a
        if kind in E.BORROWED:
            continue
        hasM = (M.a[sl][..., 3] > 0).any()
        hasT = (T.a[sl][..., 3] > 0).any()
        if hasM and hasT:
            src = M.a[sl]
            m = src[..., 3] > 0
            B.a[sl][m] = src[m]
            M.a[sl] = 0
    return s


def recolor(s, mapping, key=None, title=None, notes=None):
    t = E.recolor(s, mapping, key=key, title=title, notes=notes)
    t.names = dict(getattr(s, "names", {}))
    return t


mirror = E.mirror
outline_rect = E.outline_rect
stucco = E.stucco


def roof(L, x0, y0, w, h, ridge=True, eaves=True, ends=(True, True)):
    """emporion_lib's terracotta roof, its white ridge glints in Kirrha's limewash
    (the clay group has no pure white)."""
    E.roof(L, x0, y0, w, h, ridge=ridge, eaves=eaves, ends=ends)
    L.replace(x0, y0, w, h, "w0", "lm3")
amphora = E.amphora
hashed_rng = random.Random


# Porytiles sorts each palette's colors by value, so an Aigion part is the Kirrha
# part's own 4bpp tile only if the two groups sort in step, slot for slot.
def _key(n):
    return C[n]


_clay = sorted(GROUPS["clay"], key=_key)
_two = sorted(GROUPS["clay2"], key=_key)
IN_STEP = [AIGION[n] for n in _clay] == _two
