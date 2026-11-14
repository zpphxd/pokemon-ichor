"""Shared toolkit for gTileset_Emporion, Emporion City's secondary tileset.

Emporion is Corinth on the Isthmus: a rich, busy trading port in marble and
painted stone. It draws with kalliste_lib's Layer and Struct (so the shared
primitives and the 8-wide sheet packing are the same as every other Ichor
secondary) and adds:

  - Emporion's own palette plan: seven groups for the secondary's slots 6-12.
    Every 8x8 tile of every layer must take all its colors from one group;
    validate() enforces it.
  - Two of the groups are parallel: "clay" (ochre stucco, Aegean-blue paint)
    and "clay2" (rose stucco, green paint) list their colors slot for slot, so a
    house part drawn in clay and recolored to clay2 is the same 4bpp tile in
    another palette. Porytiles aligns the slots and stores it once: the rose
    houses cost no tiles of their own.
  - Ground per cell. A cell is on borrowed aethos ground ("grass", "sand",
    "sea", "path": its bottom layer is left empty and the build points it at
    aethos's own ground metatile), on Emporion's own marble paving ("pave") or
    quay paving ("quay"), drawn into its bottom layer, or "none" (the art fills
    the cell). The paving repeats every 16 px, so every paved cell shares the
    same few tiles.
  - Painters for the city: paving, terracotta roofs, stucco, columns of the
    three orders, doors, windows, awnings, amphorae and figures.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kalliste_lib as K  # noqa: E402
from kalliste_lib import Layer, tile_colors  # noqa: E402,F401

ROOT = K.ROOT

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # ochre stucco and its parallel, rose stucco
    "oc0": (152, 96, 40), "oc1": (200, 144, 64), "oc2": (232, 184, 104), "oc3": (248, 224, 160),
    "rs0": (128, 56, 64), "rs1": (184, 104, 104), "rs2": (224, 152, 144), "rs3": (248, 208, 200),
    # sea-green paint, the parallel of Aegean blue on the rose houses
    "gn0": (24, 80, 72), "gn1": (48, 136, 112),
    # the market's goods
    "pu0": (80, 40, 72), "pu1": (136, 72, 112), "sf": (232, 168, 40), "sf2": (248, 216, 112),
    "sl2": (136, 144, 152), "sl3": (168, 176, 176),
    # aethos's meadow, olive and pine greens, so shadows and plants sit on its grass
    "gr0": (184, 184, 104), "gr1": (144, 152, 72), "gr2": (208, 200, 128),
    "ov0": (40, 56, 32), "ov1": (72, 88, 48), "ov2": (112, 128, 64), "ov3": (152, 168, 120),
    "c1": (24, 56, 40), "c2": (40, 88, 56), "c3": (72, 120, 72),
    "tk0": (88, 72, 56), "tk1": (128, 120, 112),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # Marble, gold and painted blue and red: temples, colonnades, the Peirene, the
    # paving and kerbs, statues, the notice board, fountain water.
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "g0", "g1", "br", "b0", "b1", "b2",
               "b3", "rd"],
    # Terracotta roofs, ochre stucco, Aegean-blue doors and shutters, timber.
    "clay": ["ink", "tc0", "tc1", "tc2", "tc3", "oc0", "oc1", "oc2", "oc3", "w0", "w2", "b0",
             "b1", "wd0", "wd1"],
    # The same, slot for slot, with rose stucco and sea-green paint.
    "clay2": ["ink", "tc0", "tc1", "tc2", "tc3", "rs0", "rs1", "rs2", "rs3", "w0", "w2", "gn0",
              "gn1", "wd0", "wd1"],
    # Poros limestone: ashlar, quays, warehouses, the Diolkos, Acrocorinth's crag and walls.
    "stone": ["ink", "sk", "s0", "s1", "s2", "s3", "s4", "s5", "wt0", "wt1", "ol1", "ol2", "w0",
              "e1", "e2"],
    # Timber, rope, ships, cranes, bronze and fire: the port, the smiths, the forge.
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "b0", "b1", "rd", "g0", "g1", "br",
             "fl", "fc"],
    # The market's goods: pots and vases, cloth, spices, fish, wine; the kilns.
    "market": ["ink", "w0", "tc0", "tc1", "tc2", "pu0", "pu1", "sf", "sf2", "ol1", "sl2", "sl3",
               "rd", "wd1", "wd2"],
    # Aethos's grass, pines, olives and planters.
    "grove": ["ink", "gr0", "gr1", "gr2", "ov0", "ov1", "ov2", "ov3", "c1", "c2", "c3", "tk0",
              "tk1", "tc1", "tc2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# clay -> clay2: the rose house is the ochre house, slot for slot
ROSE = dict(zip(GROUPS["clay"], GROUPS["clay2"]))

GROUND_METATILE = {"grass": 0x001, "sand": 0x124, "sea": 0x170, "path": 0x1D9}
BORROWED = set(GROUND_METATILE)
DRAWN = {"pave", "quay", "none"}


# --------------------------------------------------------------------------
# Structures
# --------------------------------------------------------------------------

class Struct(K.Struct):
    """A kalliste Struct with a ground kind per cell (see the module docstring)."""

    def __init__(self, key, title, w, h, walk=None, notes="", ground="pave", section="emporion"):
        super().__init__(key, title, w, h, section, walk=walk, notes=notes)
        self.ground = {}
        self.set_ground(ground)

    def set_ground(self, kind, cells=None):
        cells = cells if cells is not None else [(x, y) for y in range(self.h) for x in range(self.w)]
        for c in cells:
            assert kind in BORROWED | DRAWN, kind
            self.ground[c] = kind

    def ground_rows(self, rows):
        """Ground by rows of single letters: g grass, s sand, w sea, p pave, q quay,
        a path, n none."""
        key = {"g": "grass", "s": "sand", "w": "sea", "p": "pave", "q": "quay", "a": "path",
               "n": "none"}
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                self.ground[(x, y)] = key[ch]

    @property
    def borrowed(self):
        return {c: k for c, k in self.ground.items() if k in BORROWED}


def finish(s: Struct):
    """Paint drawn ground under the art, and resolve layers.

    - "pave" and "quay" cells get the paving in their bottom layer, under whatever
      the structure drew there (the paving goes first).
    - A cell that drew in both the middle and top layers is flattened: its middle
      layer is composited into the bottom, which holds the ground. On borrowed
      ground that is impossible (the bottom is aethos's) and validate() reports it.
    """
    B, M, T = s.B, s.M, s.T
    for (cx, cy), kind in s.ground.items():
        sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        if kind in ("pave", "quay"):
            ground = Layer(16, 16)
            (paving if kind == "pave" else quay_paving)(ground, 0, 0, 16, 16)
            old = B.a[sl].copy()
            B.a[sl] = ground.a
            m = old[..., 3] > 0
            B.a[sl][m] = old[m]
        if kind in BORROWED:
            continue
        hasM = (M.a[sl][..., 3] > 0).any()
        hasT = (T.a[sl][..., 3] > 0).any()
        if hasM and hasT:
            src = M.a[sl]
            m = src[..., 3] > 0
            B.a[sl][m] = src[m]
            M.a[sl] = 0
    return s


def recolor(s: Struct, mapping, key=None, title=None, notes=None):
    """A copy of s with colors swapped by name (e.g. ROSE: ochre -> rose)."""
    import copy
    t = copy.deepcopy(s)
    if key:
        t.key = key
    if title:
        t.title = title
    if notes is not None:
        t.notes = notes
    rgb = {C[a]: C[b] for a, b in mapping.items()}
    for layer in t.layers.values():
        a = layer.a
        flat = a.reshape(-1, 4)
        for i in np.nonzero(flat[:, 3])[0]:
            c = tuple(int(v) for v in flat[i, :3])
            if c in rgb:
                flat[i, :3] = rgb[c]
    return t


def mirror(s: Struct, key, title, notes=None):
    """s flipped left to right (doors, behaviors and ground follow)."""
    import copy
    t = copy.deepcopy(s)
    t.key, t.title = key, title
    if notes is not None:
        t.notes = notes
    for layer in t.layers.values():
        layer.a[:] = layer.a[:, ::-1].copy()
    t.walk = [row[::-1] for row in t.walk]
    t.behaviors = {(t.w - 1 - x, y): mb for (x, y), mb in t.behaviors.items()}
    t.ground = {(t.w - 1 - x, y): g for (x, y), g in t.ground.items()}
    return t


def sub(s: Struct, key, title, x0, y0, w, h, walk=None, notes=""):
    """Cells (x0, y0)..(x0+w-1, y0+h-1) of s as their own structure."""
    t = Struct(key, title, w, h, walk=walk or [r[x0:x0 + w] for r in s.walk[y0:y0 + h]],
               notes=notes)
    for ln in ("bottom", "middle", "top"):
        t.layers[ln].a[:] = s.layers[ln].a[y0 * 16:(y0 + h) * 16, x0 * 16:(x0 + w) * 16]
    t.ground = {(x - x0, y - y0): g for (x, y), g in s.ground.items()
                if x0 <= x < x0 + w and y0 <= y < y0 + h}
    t.behaviors = {(x - x0, y - y0): mb for (x, y), mb in s.behaviors.items()
                   if x0 <= x < x0 + w and y0 <= y < y0 + h}
    return t


# --------------------------------------------------------------------------
# Validation
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
# Previews with the real aethos ground
# --------------------------------------------------------------------------

_AETHOS = {}


def aethos_metatile(mid):
    if mid not in _AETHOS:
        sys.path.insert(0, str(ROOT / "tools/ichor"))
        import render_map as R
        R.read_fieldmap_constants()
        sy = R.scan_tileset_symbols()
        r = R.Renderer(R.Tileset(sy["gTileset_Aethos"]), R.Tileset(sy["gTileset_Kalliste"]))
        _AETHOS[mid] = r.metatile(mid)[0]
    return _AETHOS[mid]


def composite(s: Struct):
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    gr = s.borrowed
    for (cx, cy), kind in gr.items():
        out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos_metatile(GROUND_METATILE[kind])
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        m = a[..., 3] > 0
        if ln == "bottom":
            for (cx, cy) in gr:
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        out[m] = a[..., :3][m]
    return out


def preview(structs, scale=2, bg=(40, 40, 48), cols=4):
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key, Image.fromarray(composite(s)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                         Image.NEAREST)) for s in structs]
    colw = max(i.width for _, i in imgs) + pad
    colw = max(colw, 16 * 4 * scale + pad)
    rows = []
    cur, curw = [], 0
    maxw = cols * (16 * 5 * scale + pad)
    for k, i in imgs:
        if cur and curw + i.width + pad > maxw:
            rows.append(cur)
            cur, curw = [], 0
        cur.append((k, i))
        curw += max(i.width, 80) + pad
    if cur:
        rows.append(cur)
    width = max(sum(max(i.width, 80) + pad for _, i in r) for r in rows) + pad
    height = sum(max(i.height for _, i in r) + pad + 12 for r in rows) + pad
    out = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(out)
    y = pad
    for r in rows:
        x = pad
        for key, i in r:
            d.text((x, y), key, fill=(230, 230, 200))
            out.paste(i, (x, y + 12))
            x += max(i.width, 80) + pad
        y += max(i.height for _, i in r) + pad + 12
    return out


# --------------------------------------------------------------------------
# Ground painters
# --------------------------------------------------------------------------

# The street paving's joints within one 16x16 cell. Two courses, 9 and 7 px,
# their vertical joints staggered and crossing the cell's edges, so a street
# reads as long marble flags, not a grid. '#' joint, '+' joint crossing, '^' a
# slab's lit top edge, '.' slab, ',' a faint fleck.
PAVE = {
    # one great square flag per cell, softly bevelled
    0: ["^^^^^^^^^^^^^^^#",
        "^..............#",
        "^...........,..#",
        "^..............#",
        "^....,.........#",
        "^..............#",
        "^..............#",
        "^.........,....#",
        "^..............#",
        "^..............#",
        "^..,...........#",
        "^..............#",
        "^........,.....#",
        "^..............#",
        "^..............#",
        "###############+"],
    # the flag split into two
    1: ["^^^^^^^^^^^^^^^#",
        "^..............#",
        "^......,.......#",
        "^..............#",
        "^..............#",
        "^..............#",
        "^...........,..#",
        "###############+",
        "^^^^^^^^^^^^^^^#",
        "^..............#",
        "^...,..........#",
        "^..............#",
        "^..............#",
        "^.........,....#",
        "^..............#",
        "###############+"],
    # four smaller flags, worn
    2: ["^^^^^^^#^^^^^^^#",
        "^......#^......#",
        "^..,...#^......#",
        "^......#^....,.#",
        "^......#^......#",
        "^......#^......#",
        "^......#^......#",
        "#######+#######+",
        "^^^^^^^#^^^^^^^#",
        "^......#^......#",
        "^......#^..,...#",
        "^......#^......#",
        "^.,....#^......#",
        "^......#^......#",
        "^......#^......#",
        "#######+#######+"],
}
PAVE_KEY = {"#": "m2", "+": "m3", "^": "w0", ".": "m1", ",": "m2"}


def paving(L, x0, y0, w, h, ox=0, oy=0, variant=0):
    """Emporion's street paving: great square marble flags, one to a cell, softly
    bevelled (lit on the top and left edges, a grey joint right and below).
    Repeats every 16 px, so it is cell-aligned. Variant 1 splits the flag in two
    and variant 2 in four, for scattering; all meet each other on every side."""
    pat = PAVE[variant]
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            L.px(x, y, PAVE_KEY[pat[(y - oy) % 16][(x - ox) % 16]])


def shade_paving(L, x0, y0, north=True, west=False):
    """Darken the top (north) or left (west) edge of a paved cell: the shadow a
    building or wall casts on the street south or east of it (light from the top
    left)."""
    dark = {"w0": "m2", "m1": "m2", "m2": "m3", "m3": "m4"}
    for y in range(16):
        for x in range(16):
            if (north and y < 3) or (west and x < 3):
                c = L.get(x0 + x, y0 + y)
                if c in dark:
                    L.px(x0 + x, y0 + y, dark[c] if (y < 2 or x < 2) else
                         ("m2" if c in ("w0", "m1") else c))


def quay_paving(L, x0, y0, w, h, ox=0, oy=0):
    """Lechaion's quays and the workshops' yards: courses of warm poros blocks in
    a running bond, soft joints, the courses lit along their tops. Repeats every
    16 px."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 16, (y - oy) % 16
            row = Y // 8
            off = 0 if row == 0 else 8
            bx, by = (X + off) % 16, Y % 8
            if by == 7:
                c = "s2"
            elif bx == 15:
                c = "s2"
            elif by == 0:
                c = "s4"
            else:
                c = "s3"
                if (bx, by) in ((4, 3), (11, 5), (7, 2)) and row == 0 or \
                        (bx, by) in ((2, 4), (9, 2), (13, 5)) and row == 1:
                    c = "s2"
            L.px(x, y, c)


# --------------------------------------------------------------------------
# Building painters
# --------------------------------------------------------------------------

def roof(L, x0, y0, w, h, ridge=True, eaves=True, pal="clay", ends=(True, True)):
    """A Greek terracotta roof seen from the front: rows of flat pan tiles under
    ridged cover tiles every 8 px, a ridge capping along the top, and a row of
    palmette antefixes along the eaves. Light from the left: each cover tile's
    left flank is lit. h >= 12. Repeats every 8 px across, so long roofs are
    cheap."""
    T0, T1, T2, T3 = "tc0", "tc1", "tc2", "tc3"
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X = (x - x0) % 8
            Y = (y - y0) % 4
            # pan tiles in courses 4 px tall: a lit lip at each course's top,
            # the course's shadow at its foot; a rounded cover tile over every
            # joint (lit flank, shaded flank)
            if X == 6:
                c = T2 if Y != 3 else T1
            elif X == 7:
                c = T0
            else:
                c = T1
                if Y == 0:
                    c = T2
                elif Y == 3:
                    c = T0 if X in (0, 1, 5) else T1
            L.px(x, y, c)
    if ridge:
        L.hline(x0, x0 + w - 1, y0, "ink")
        L.hline(x0, x0 + w - 1, y0 + 1, T2)
        L.hline(x0, x0 + w - 1, y0 + 2, T3)
        L.hline(x0, x0 + w - 1, y0 + 3, T1)
        L.hline(x0, x0 + w - 1, y0 + 4, T0)
        for x in range(x0 + 4, x0 + w, 8):
            L.px(x, y0 + 2, "w0")
    if eaves:
        ye = y0 + h - 1
        L.hline(x0, x0 + w - 1, ye, "ink")
        L.hline(x0, x0 + w - 1, ye - 1, T0)
        for x in range(x0, x0 + w):
            X = (x - x0) % 8
            # antefix: a little palmette over each cover tile's end
            if X in (6, 7):
                L.px(x, ye - 2, T3 if X == 6 else T1)
                L.px(x, ye - 1, T2 if X == 6 else T0)
            if X == 6:
                L.px(x, ye - 3, T3)
    if ends[0]:
        L.vline(x0, y0, y0 + h - 1, "ink")
    if ends[1]:
        L.vline(x0 + w - 1, y0, y0 + h - 1, "ink")


def stucco(L, x0, y0, w, h, base="oc2", lit="oc3", shade="oc1", ox=0, oy=0):
    """Painted stucco: a flat wash with a faint 8 px speckle, mirror-symmetric
    within every 8 px so a mirrored door or window cell keeps the wall's tiles."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 8, (y - oy) % 8
            c = base
            if (X, Y) in ((2, 1), (5, 1)):
                c = lit
            elif (X, Y) in ((1, 5), (6, 5)):
                c = shade
            L.px(x, y, c)


def ashlar(L, x0, y0, w, h, ox=0, oy=0, course=8, light="s4", body="s3", joint="s1",
           shade="s2"):
    """Squared poros blocks in a running bond, courses `course` px tall."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = x - ox, y - oy
            row = Y // course
            off = 8 if row % 2 else 0
            bx, by = (X + off) % 16, Y % course
            if by == course - 1 or bx == 15:
                c = joint
            elif by == 0 or bx == 0:
                c = light
            elif by == course - 2:
                c = shade
            else:
                c = body
            L.px(x, y, c)


def outline_rect(L, x, y, w, h, c="ink"):
    L.hline(x, x + w - 1, y, c)
    L.hline(x, x + w - 1, y + h - 1, c)
    L.vline(x, y, y + h - 1, c)
    L.vline(x + w - 1, y, y + h - 1, c)


def shaft(L, x, y, w, h, ramp=("m4", "m3", "m2", "m1", "w0"), outline="ink", fluted=True):
    """A column shaft x..x+w-1, y..y+h-1: outline, lit left flank, shaded right,
    flutes as faint vertical lines."""
    d2, d1, m, l1, hi = ramp
    for yy in range(y, y + h):
        for i in range(w):
            if i == 0 or i == w - 1:
                c = outline
            elif i == 1:
                c = l1
            elif i == 2:
                c = hi
            elif i == w - 2:
                c = d2
            elif i == w - 3:
                c = d1
            else:
                c = m
                if fluted and w >= 7 and i % 2 == 0 and i not in (2,):
                    c = l1
            L.px(x + i, yy, c)


def ionic_capital(L, x, y, w, ramp=("m4", "m3", "m2", "m1", "w0"), gold=False):
    """An Ionic capital over a shaft x..x+w-1 whose top is at y+5: an abacus and
    two volutes scrolling out past the shaft. 5 px tall."""
    d2, d1, m, l1, hi = ramp
    L.rect(x - 2, y, w + 4, 2, l1)
    L.hline(x - 2, x + w + 1, y, "ink")
    L.hline(x - 1, x + w, y + 1, hi)
    L.rect(x - 1, y + 2, w + 2, 2, m)
    L.hline(x - 1, x + w, y + 2, l1)
    # the volutes: a coil at each end
    for vx, side in ((x - 3, -1), (x + w, 1)):
        L.blit(["kkk", "kgk" if gold else "k1k", "kkk"], {"k": "ink", "1": d1, "g": "g0"}, vx, y + 1)
        L.px(vx + 1, y + 2, "g1" if gold else hi)
    L.hline(x, x + w - 1, y + 4, d1)
    L.vline(x - 1, y + 2, y + 3, "ink")
    L.vline(x + w, y + 2, y + 3, "ink")


def doric_capital(L, x, y, w, ramp=("m4", "m3", "m2", "m1", "w0")):
    """A Doric abacus and echinus over a shaft x..x+w-1. 5 px tall."""
    d2, d1, m, l1, hi = ramp
    L.rect(x - 2, y, w + 4, 3, l1)
    L.hline(x - 2, x + w + 1, y, "ink")
    L.hline(x - 2, x + w + 1, y + 2, d1)
    L.vline(x - 2, y, y + 2, "ink")
    L.vline(x + w + 1, y, y + 2, "ink")
    L.hline(x - 1, x + w, y + 1, hi)
    L.rect(x - 1, y + 3, w + 2, 2, m)
    L.hline(x - 1, x + w, y + 3, l1)
    L.vline(x - 1, y + 3, y + 4, "ink")
    L.vline(x + w, y + 3, y + 4, "ink")


def corinthian_capital(L, x, y, w):
    """Corinth's own order: a bell of acanthus leaves under a concave abacus with
    corner volutes. 7 px tall, over a shaft x..x+w-1 whose top is at y+7."""
    L.rect(x - 2, y, w + 4, 2, "m1")
    L.hline(x - 2, x + w + 1, y, "ink")
    L.hline(x - 1, x + w, y + 1, "w0")
    L.px(x - 2, y + 1, "ink")
    L.px(x + w + 1, y + 1, "ink")
    L.px(x - 3, y + 2, "ink")
    L.px(x + w + 2, y + 2, "ink")
    for yy in range(y + 2, y + 7):
        k = (yy - y - 2)
        x0, x1 = x - 2 + k // 3, x + w + 1 - k // 3
        L.hline(x0, x1, yy, "m2")
        L.px(x0, yy, "ink")
        L.px(x1, yy, "ink")
        for xx in range(x0 + 1, x1):
            if (xx + yy) % 3 == 0:
                L.px(xx, yy, "m3")
            elif (xx + 2 * yy) % 4 == 0:
                L.px(xx, yy, "w0")
    L.px(x - 1, y + 2, "m3")
    L.px(x + w, y + 2, "m3")


def amphora(L, x, y, body="tc2", lit="tc3", shade="tc1", dark="tc0", ink="ink", figure=None,
            small=False):
    """A transport/storage amphora 7 px wide, 12 px tall (9 if small), outlined.
    figure: a color for a black-figure band."""
    if small:
        rows = [
            " kkk ",
            " kbk ",
            "kkbkk",
            "klbbsk",
            "klbbsk",
            "klbbsk",
            " kbsk ",
            "  kk  ",
        ]
        rows = [r.ljust(6) for r in rows]
    else:
        rows = [
            "  kkk  ",
            "  kbk  ",
            "kkkbkkk",
            "k kbk k",
            " klbbsk",
            "klbbbbsk",
            "klbbbbsk",
            "klbbbbsk",
            " klbbsk ",
            " klbbsk ",
            "  kbsk  ",
            "   kk   ",
        ]
        rows = [r.ljust(8) for r in rows]
    L.blit(rows, {"k": ink, "b": body, "l": lit, "s": shade}, x, y)
    if figure and not small:
        for xx in range(x + 2, x + 6):
            L.px(xx, y + 6, figure)
        L.px(x + 3, y + 5, figure)
        L.px(x + 5, y + 7, figure)


def flame(L, x, y, big=False):
    """A small flame (wood group): 5x6, or 7x8 if big."""
    if big:
        rows = ["   f   ", "  ffc  ", " fccf f", " fcyccf", "fcyyycf", "fcyyycf", " fcyycf", "  fff  "]
    else:
        rows = ["  f  ", " fcf ", " fcf ", "fcycf", "fcycf", " fff "]
    L.blit(rows, {"f": "fl", "c": "g1", "y": "fc"}, x, y)


def awning(L, x0, y0, w, h, c1, c2, edge, scallop=True, stripe=4):
    """A striped canvas awning seen from above-front: stripes `stripe` px wide,
    a shaded valance with a scalloped hem. Light from the left."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X = x - x0
            c = c1 if (X // stripe) % 2 == 0 else c2
            L.px(x, y, c)
    L.hline(x0, x0 + w - 1, y0, "ink")
    L.vline(x0, y0, y0 + h - 1, "ink")
    L.vline(x0 + w - 1, y0, y0 + h - 1, "ink")
    L.hline(x0 + 1, x0 + w - 2, y0 + h - 3, edge)
    if scallop:
        for x in range(x0, x0 + w):
            X = (x - x0) % 4
            L.px(x, y0 + h - 1, "ink" if X in (0, 3) else (c1 if ((x - x0) // stripe) % 2 == 0 else c2))
            if X in (0, 3):
                L.px(x, y0 + h - 2, edge)
        L.hline(x0, x0 + w - 1, y0 + h, "ink")


def shadow_px(L, pts, c):
    for (x, y) in pts:
        L.px(x, y, c)


def ellipse_mask(w, h):
    yy, xx = np.mgrid[0:h, 0:w]
    return ((xx - (w - 1) / 2) / (w / 2)) ** 2 + ((yy - (h - 1) / 2) / (h / 2)) ** 2 <= 1.0


def fill_mask(L, mask, x, y, c):
    ys, xs = np.nonzero(mask)
    for yy, xx in zip(ys, xs):
        L.px(x + xx, y + yy, c)


def silhouette_outline(L, region, c="ink"):
    """Outline the opaque pixels of L inside region (x, y, w, h) on their edges."""
    x0, y0, w, h = region
    a = L.a[y0:y0 + h, x0:x0 + w, 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    ys, xs = np.nonzero(edge)
    for yy, xx in zip(ys, xs):
        L.px(x0 + xx, y0 + yy, c)


def clear(L, x, y, w, h):
    L.a[y:y + h, x:x + w] = 0


def mirror_half(L, x0, w, y0, y1):
    """Make rows y0..y1-1 of the box x0..x0+w-1 mirror-symmetric: copy its left
    half, flipped, over its right half. With the box's middle on a tile edge,
    Porytiles stores every right-hand tile as its left-hand twin, flipped, so a
    symmetric front costs half its tiles."""
    h = w // 2
    left = L.a[y0:y1, x0:x0 + h].copy()
    L.a[y0:y1, x0 + w - h:x0 + w] = left[:, ::-1]


def deg(a):
    return math.radians(a)
