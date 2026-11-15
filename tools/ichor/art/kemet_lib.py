"""Shared toolkit for gTileset_Kemet, Egypt's outdoor secondary tileset.

Kemet is the Black Land: the Nile's delta and valley as Greek traders saw them
from Naukratis. Green papyrus taller than a man, black mud, white limestone,
mud-brick towns plastered white, and at the desert's edge the pyramids in their
gold. OIKOUMENE.md §4.5 and §7 set the look: Nile black, papyrus green,
limestone, ochre; pyramids, obelisks, papyrus, painted walls.

It draws with kalliste_lib's Layer and Struct (the shared primitives and the
8-wide sheet packing) and emporion_build.py's pipeline (kemet_build.py runs it),
and adds:

  - Kemet's palette plan: seven groups for the secondary's slots 6-12. Every 8x8
    tile of every layer takes all its colors from one group; validate() enforces it.
  - Ground per cell. A cell is on borrowed aethos ground ("grass", "sand", "sea",
    "path": its bottom layer is left empty and the build points it at aethos's
    own ground metatile, so the sea under a mud bank or a papyrus clump stays
    animated), on Kemet's own black mud ("mud") or quay ashlar ("quay"), drawn
    into its bottom layer, or "none" (the art fills the cell).

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kalliste_lib as K  # noqa: E402
import emporion_lib as E  # noqa: E402,F401  (registers its colors in K.C first)
from kalliste_lib import Layer, tile_colors  # noqa: E402,F401

ROOT = K.ROOT

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # Nile mud: black when wet, grey-brown where it dries and cracks
    "md0": (40, 32, 32), "md1": (64, 48, 40), "md2": (88, 72, 56), "md3": (120, 96, 72),
    "md4": (152, 128, 96), "wet": (72, 80, 88), "wet2": (112, 128, 136),
    # papyrus and palm greens, the umbels' gold, palm trunks, dates
    "pg0": (24, 64, 40), "pg1": (40, 96, 48), "pg2": (72, 136, 56), "pg3": (120, 168, 72),
    "pg4": (168, 200, 96), "um0": (200, 192, 88), "um1": (232, 224, 136),
    "tr0": (72, 48, 32), "tr1": (112, 80, 48), "tr2": (152, 112, 72),
    "dt": (160, 48, 40), "dt2": (216, 120, 48),
    # Tura limestone, from shadow to the pyramids' polished white
    "ls0": (88, 80, 72), "ls1": (136, 128, 112), "ls2": (176, 168, 144), "ls3": (208, 200, 176),
    "ls4": (232, 224, 200), "sd0": (200, 160, 96), "sd1": (232, 200, 136),
    # painted walls: red and yellow ochre, malachite, lapis, skin
    "rd0": (144, 48, 32), "rd1": (200, 88, 56), "yo0": (192, 136, 48), "yo1": (232, 184, 88),
    "mg0": (32, 104, 80), "mg1": (72, 160, 120), "lp0": (32, 56, 128), "lp1": (64, 104, 184),
    "skn": (160, 96, 56),
    # mud brick and its whitewash
    "pl0": (168, 152, 128), "pl1": (200, 184, 160), "pl2": (232, 224, 200),
    "mb0": (96, 64, 40), "mb1": (136, 96, 64), "mb2": (176, 136, 96), "door": (48, 40, 40),
    # reed bundles, linen, rope and nets
    "st0": (176, 136, 64), "st1": (216, 184, 104), "st2": (240, 224, 160),
    "ln0": (200, 192, 176), "ln1": (240, 232, 216), "net": (120, 112, 104),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # The black land: mud, its wet sheen and dry crust, the bank's foam line, and
    # aethos's meadow greens so grass tufts and shoots sit over the mud's edge.
    "nile": ["ink", "md0", "md1", "md2", "md3", "md4", "wet", "wet2", "w0", "gr0", "gr1", "gr2",
             "pg1", "pg2", "pg3"],
    # Papyrus, palms and dates: stems, umbels, fronds, trunks, the mud at their feet.
    "reed": ["ink", "pg0", "pg1", "pg2", "pg3", "pg4", "um0", "um1", "tr0", "tr1", "tr2",
             "md0", "md1", "dt", "dt2"],
    # Limestone: Memphis's white walls, obelisks, pyramids and their gold caps, the
    # sand at their feet, quays.
    "stone": ["ink", "ls0", "ls1", "ls2", "ls3", "ls4", "w0", "sd0", "sd1", "g0", "g1", "md1",
              "md2", "gr0", "gr1"],
    # Painted reliefs: the pylon's frieze, the sphinx's nemes, steles, Thoth's pillar.
    "paint": ["ink", "w0", "ls1", "ls2", "ls3", "rd0", "rd1", "yo0", "yo1", "mg0", "mg1", "lp0",
              "lp1", "skn", "g1"],
    # Mud brick plastered white, palm-log lintels, dark doorways, a little paint.
    "brick": ["ink", "pl0", "pl1", "pl2", "w0", "mb0", "mb1", "mb2", "wd0", "wd1", "wd2", "door",
              "lp1", "rd1", "net"],
    # The Hellenion: marble, terracotta, Greek blue and red, gilt.
    "hellas": ["ink", "w0", "m1", "m2", "m3", "m4", "tc0", "tc1", "tc2", "tc3", "b0", "b1", "rd",
               "g0", "g1"],
    # Boats, rope, reed bundles, linen sails and awnings, nets, pots.
    "goods": ["ink", "w0", "wd0", "wd1", "wd2", "wd3", "rp", "st0", "st1", "st2", "ln0", "ln1",
              "net", "tc1", "tc2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

GROUND_METATILE = E.GROUND_METATILE        # grass 0x001, sand 0x124, sea 0x170, path 0x1D9
BORROWED = set(GROUND_METATILE)
DRAWN = {"mud", "quay", "none"}


# --------------------------------------------------------------------------
# Structures
# --------------------------------------------------------------------------

class Struct(K.Struct):
    """A kalliste Struct with a ground kind per cell (see the module docstring)
    and named parts, so map builders place pieces by name, never by raw id."""

    def __init__(self, key, title, w, h, walk=None, notes="", ground="none", section="kemet"):
        super().__init__(key, title, w, h, section, walk=walk, notes=notes)
        self.ground = {}
        self.names = {}
        self.set_ground(ground)

    def set_ground(self, kind, cells=None):
        cells = cells if cells is not None else [(x, y) for y in range(self.h) for x in range(self.w)]
        for c in cells:
            assert kind in BORROWED | DRAWN, kind
            self.ground[c] = kind

    def ground_rows(self, rows):
        """Ground by rows of single letters: g grass, s sand, w sea, a path, m mud,
        q quay, n none."""
        key = {"g": "grass", "s": "sand", "w": "sea", "a": "path", "m": "mud", "q": "quay",
               "n": "none"}
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                self.ground[(x, y)] = key[ch]

    def name(self, **parts):
        for n, c in parts.items():
            self.names[n] = tuple(c)
        return self

    @property
    def borrowed(self):
        return {c: k for c, k in self.ground.items() if k in BORROWED}


def finish(s: Struct):
    """Paint drawn ground under the art and settle the layers.

    - "mud" and "quay" cells get their ground in the bottom layer, under whatever
      the structure drew there.
    - A drawn-ground cell that drew in both the middle and top layers is
      flattened: its middle layer is composited into the bottom.
    """
    B, M, T = s.B, s.M, s.T
    for (cx, cy), kind in s.ground.items():
        sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        if kind in ("mud", "quay"):
            ground = Layer(16, 16)
            (mud if kind == "mud" else quay)(ground, 0, 0, 16, 16, ox=-cx * 16, oy=-cy * 16)
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


def mirror(s: Struct, key, title, notes=None):
    """s flipped left to right (doors, behaviors, ground and names follow)."""
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
    t.names = {n: (t.w - 1 - x, y) for n, (x, y) in t.names.items()}
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
# Ground painters
# --------------------------------------------------------------------------

def _h(x, y, salt=0):
    """A stable hash of a pixel, 0..255."""
    v = (x * 374761393 + y * 668265263 + salt * 2246822519) & 0xFFFFFFFF
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFF


# Black mud, 16x16, repeating: dark wet ground with a few dry flakes and a wet
# glint, cell-aligned so every mud cell shares the same tiles.
MUD8 = [
    "11121111",
    "11111131",
    "12111111",
    "1111w111",
    "11111112",
    "13111111",
    "11112111",
    "1111111w",
]
MUD = [(r * 2) for r in MUD8] * 2
MUD_KEY = {"0": "md0", "1": "md1", "2": "md2", "3": "md3", "w": "wet"}


def mud(L, x0, y0, w, h, ox=0, oy=0):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            L.px(x, y, MUD_KEY[MUD[(y - oy) % 16][(x - ox) % 16]])


def quay(L, x0, y0, w, h, ox=0, oy=0):
    """Limestone quay blocks, one to an 8-px tile, lit along their tops."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            bx, by = (x - ox) % 8, (y - oy) % 8
            if by == 7 or bx == 7:
                c = "ls1"
            elif by == 0:
                c = "ls4"
            else:
                c = "ls3"
                if (bx, by) in ((2, 3), (5, 5)):
                    c = "ls2"
            L.px(x, y, c)


def outline_rect(L, x, y, w, h, c="ink"):
    L.hline(x, x + w - 1, y, c)
    L.hline(x, x + w - 1, y + h - 1, c)
    L.vline(x, y, y + h - 1, c)
    L.vline(x + w - 1, y, y + h - 1, c)


def silhouette(L, region=None, c="ink"):
    """Outline the opaque pixels of L (inside region) on their edges."""
    x0, y0, w, h = region or (0, 0, L.w, L.h)
    a = L.a[y0:y0 + h, x0:x0 + w, 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    ys, xs = np.nonzero(edge)
    for yy, xx in zip(ys, xs):
        L.px(x0 + xx, y0 + yy, c)


def mirror_half(L, x0, w, y0, y1):
    """Copy the left half of box x0..x0+w-1 (rows y0..y1-1), flipped, over its right
    half. With the middle on a tile edge, the right-hand tiles are flips of the left."""
    h = w // 2
    left = L.a[y0:y1, x0:x0 + h].copy()
    L.a[y0:y1, x0 + w - h:x0 + w] = left[:, ::-1]


def clear(L, x, y, w, h):
    L.a[y:y + h, x:x + w] = 0
