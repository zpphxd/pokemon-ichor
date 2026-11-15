"""Shared toolkit for gTileset_Troas, the Troad's outdoor secondary.

The Troad is the plain of Troy and the strait beside it: wheat-gold fields, the
Skamander's reeds and banks, Ida's pines, heroes' burial mounds, the fast blue
Hellespont, and Ilion's great sloping walls of pale limestone (OIKOUMENE.md §4.1,
§7). It draws with emporion_lib's Struct (kalliste_lib layers, a ground kind per
cell) and is built by troas_build.py on emporion_build.py's pipeline, so cells
on grass, sand or sea borrow aethos's own ground metatile and the sea under
every rock and current animates with aethos's water.

Palette plan: seven groups for the secondary's slots 6-12. Every 8x8 tile of
every layer takes all its colors from one group; validate() enforces it.

  wood      Akti's wood group, slot for slot: the Euploia, the jetty, timber,
            bronze fittings, the stable's doors, hay, dye vats
  marble    Akti's marble group: the temple of Athena, Priam's megaron, the
            great herm, Hero's lamp
  stone     Akti's stone group: Ilion's pale limestone walls and gates, Hero's
            tower, the quay, crags and their foam, the current's streaks
  plaster   Trojan houses: ochre lime plaster, packed-clay flat roofs, timber
  plaster2  the same slot for slot with whitewash, so a white house costs no tiles
  field     wheat gold, reed green, river earth, field flowers
  grove     Ida's pines, the Troad's oaks and elms, the mounds' turf and kerbs

The first three match gTileset_Akti's groups exactly, so Akti's trireme, quay
and harbor pieces are drawn here by Akti's own painters (from_akti) and the
Euploia looks the same in both ports.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kalliste_lib as K  # noqa: E402
import akti_lib  # noqa: E402,F401  (registers Akti's colors in K.C)
import emporion_lib as E  # noqa: E402
from kalliste_lib import Layer, tile_colors  # noqa: E402,F401

ROOT = K.ROOT
SEC = "troas"

NEW = {
    # Trojan lime plaster over mudbrick, and the packed-clay flat roofs
    "pl0": (144, 104, 64), "pl1": (192, 152, 96), "pl2": (224, 192, 136), "pl3": (240, 224, 184),
    "rf0": (88, 64, 48), "rf1": (136, 96, 64), "rf2": (176, 136, 88),
    # whitewash, slot for slot with the plaster. Porytiles orders a palette by
    # color value, so each pw sorts into the same slot as its pl among the
    # group's shared colors; that is what lets the white house reuse the ochre
    # house's tiles.
    "pw0": (144, 136, 128), "pw1": (192, 184, 168), "pw2": (224, 216, 200), "pw3": (240, 232, 216),
    # wheat on the plain of Troy
    "tw0": (120, 80, 24), "tw1": (176, 128, 40), "tw2": (216, 168, 64), "tw3": (240, 208, 104),
    "tw4": (248, 232, 160),
    # the Skamander's reeds
    "rg0": (56, 80, 40), "rg1": (96, 120, 56), "rg2": (152, 160, 88),
    # Ida's black pines
    "pn0": (24, 48, 48), "pn1": (40, 80, 72), "pn2": (72, 112, 88),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "b0", "b1", "b2", "rd", "g1", "br", "g0",
             "tc1"],
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "br", "g0", "g1", "fl", "fc", "tc0", "tc1",
               "tc2"],
    "stone": ["sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "e2", "wt0", "wt1", "alg", "w0", "b3",
              "ol1"],
    "plaster": ["ink", "pl0", "pl1", "pl2", "pl3", "rf0", "rf1", "rf2", "wd0", "wd1", "wd2", "w0", "rd",
                "b1", "sk"],
    "plaster2": ["ink", "pw0", "pw1", "pw2", "pw3", "rf0", "rf1", "rf2", "wd0", "wd1", "wd2", "w0",
                 "rd", "b1", "sk"],
    "field": ["gr0", "gr1", "gr2", "tw0", "tw1", "tw2", "tw3", "tw4", "rg0", "rg1", "rg2", "e1", "e2",
              "w0", "b2"],
    "grove": ["ink", "gr0", "gr1", "gr2", "ov0", "ov1", "ov2", "ov3", "ov4", "tk0", "tk1", "tk2", "pn0",
              "pn1", "pn2"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}
WHITEWASH = dict(zip(GROUPS["plaster"], GROUPS["plaster2"]))

# Borrowed aethos ground (emporion_lib's kinds): grass 0x001, sand 0x124, sea 0x170,
# path 0x1D9.
GROUND = E.GROUND_METATILE


# --------------------------------------------------------------------------
# Structures
# --------------------------------------------------------------------------

def struct(key, title, w, h, walk=None, notes="", ground="none", names=None):
    s = E.Struct(key, title, w, h, walk=walk, notes=notes, ground=ground, section=SEC)
    s.names = dict(names or {})
    return s


def behave(s, cells, mb):
    for c in cells:
        s.behaviors[c] = mb


def from_akti(s, key=None, title=None, notes=None):
    """An Akti structure as a troas one: same layers, walk grid and behaviors, its
    borrowed cells kept and every other cell drawn ("none")."""
    t = struct(key or s.key, title or s.title, s.w, s.h, walk=list(s.walk),
               notes=s.notes if notes is None else notes)
    for ln in ("bottom", "middle", "top"):
        t.layers[ln].a[:] = s.layers[ln].a
    t.behaviors = dict(s.behaviors)
    for c, kind in getattr(s, "ground", {}).items():
        t.ground[c] = kind
    return t


def finish(s):
    return E.finish(s)


def recolor(s, mapping, key, title, notes=None):
    return E.recolor(s, mapping, key=key, title=title, notes=notes)


# --------------------------------------------------------------------------
# Validation (emporion_lib's rules against troas's groups)
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
                    if cols and not any(cols <= g for g in GROUP_RGB.values()):
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
# Painters
# --------------------------------------------------------------------------

def ashlar(L, x0, y0, w, h, ox=0, oy=0, course=8, light="s4", body="s3", joint="s1", shade="s2",
           batter=False):
    """Squared limestone in a running bond. batter: each course is lit along its
    top and set back a pixel, the way Troy's sloping walls catch the sun."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = x - ox, y - oy
            row = Y // course
            off = (8 if row % 2 else 0) + (3 if batter and row % 3 == 2 else 0)
            bx, by = (X + off) % 16, Y % course
            if by == course - 1:
                c = joint
            elif bx == 15:
                c = joint
            elif by == 0:
                c = light
            elif batter and by == 1:
                c = light if bx % 5 else body
            elif by == course - 2 or bx == 14:
                c = shade
            else:
                c = body
            L.px(x, y, c)


def plaster(L, x0, y0, w, h, ox=0, oy=0, pal="pl"):
    """Lime plaster over mudbrick: a warm wash, a few brick courses showing
    through where it has worn. Symmetric within every 8 px."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 8, (y - oy) % 16
            c = f"{pal}2"
            if (X, Y) in ((2, 3), (5, 3), (1, 11), (6, 11)):
                c = f"{pal}3"
            elif (X, Y) in ((3, 7), (4, 7), (2, 14), (5, 14)):
                c = f"{pal}1"
            L.px(x, y, c)


def speckle(L, x0, y0, w, h, cols, seed=0, density=0.08):
    rng = np.random.default_rng(seed)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if rng.random() < density and L.get(x, y) is not None:
                L.px(x, y, cols[int(rng.integers(len(cols)))])


def mirror_x(L, x0, w, y0, y1):
    """Rows y0..y1-1 of the box x0..x0+w-1 made mirror-symmetric (left half kept)."""
    E.mirror_half(L, x0, w, y0, y1)


def outline_mask(L, mask, ox, oy, c):
    pad = np.pad(mask, 1)
    edge = mask & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(ox + x, oy + y, c)


def blob(L, cx, cy, rx, ry, c):
    yy, xx = np.mgrid[0:L.h, 0:L.w]
    m = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
    L.mask_fill(m, c)
    return m


def preview(structs, scale=2, cols=5):
    return E.preview(structs, scale=scale, cols=cols)
