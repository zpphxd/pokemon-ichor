"""Shared toolkit for gTileset_Aegina, the island secondary for Aegina Town and
the Aegina detour (the Aphaia Road, the Temple of Aphaia, Mount Oros).

It draws with kalliste_lib's layers and structures, like akti_lib, so the
harbor pieces copied from Akti come across pixel for pixel, and adds:

  - Aegina's own palette plan: seven groups for the secondary's slots 6-12.
    Every 8x8 tile of every layer takes all its colors from one group;
    validate() enforces it. Stone, wood and marble are Akti's groups, so the
    copied quay, boats and trireme fit unchanged.
  - Borrowed ground, as in Akti: a cell can sit on aethos grass, sand, sea or
    limestone path. Its bottom layer stays empty in the sources, and after
    Porytiles compiles, aegina_build.py points it at aethos's own ground metatile.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import akti_lib  # noqa: E402,F401  (registers Akti's colors: grove greens, the plaza)
import kalliste_lib as K  # noqa: E402
from kalliste_lib import Layer, Struct, tile_colors  # noqa: E402,F401

ROOT = K.ROOT

# --------------------------------------------------------------------------
# Colors: Akti's names, plus Aegina's
# --------------------------------------------------------------------------

NEW = {
    # sun-dried grass and straw: tawny where aethos's meadow is green
    "dg0": (128, 96, 48), "dg1": (176, 144, 72), "dg2": (208, 176, 96), "dg3": (232, 208, 136),
    # the red earth of the ant hills
    "ea0": (96, 56, 40), "ea1": (144, 96, 64), "ea2": (184, 136, 88),
    "an0": (104, 32, 24),
    # Aegina's houses: honey-ochre plaster, sea-green doors and shutters
    "oc0": (144, 104, 56), "oc1": (192, 152, 88), "oc2": (224, 192, 128), "oc3": (240, 224, 176),
    "te0": (24, 72, 80), "te1": (48, 120, 120), "te2": (104, 176, 160),
    # pistachio husks, rosy when ripe
    "pk0": (160, 56, 72), "pk1": (224, 128, 128),
    # the Temple of Aphaia: golden poros, its pediment painted blue and red
    "po0": (112, 88, 64), "po1": (168, 136, 96), "po2": (208, 176, 128), "po3": (232, 208, 160),
    "po4": (248, 232, 192),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # limestone: the quay and the mole, every crag, Kolona's column, the mint's ashlar
    "stone": ["sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "e2", "wt0", "wt1", "alg",
              "w0", "b3", "ol1"],
    # timber, rope, pitch and bronze: the trireme, the kaikia, gates, galleries, the beacon
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "b0", "b1", "b2", "rd", "g1",
             "br", "g0", "tc1"],
    # marble and bronze: Zeus's altar, fire, the turtle coin
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "br", "g0", "g1", "fl", "fc",
               "tc0", "tc1", "tc2"],
    # aethos's meadow and the trees: pistachios, pines, shrubs
    "grove": ["ink", "gr0", "gr1", "gr2", "ov0", "ov1", "ov2", "ov3", "ov4", "tk0", "tk1",
              "tk2", "pk0", "pk1", "wd2"],
    # the dry hills: straw, red earth, ants, and the meadow green they fade into
    "dry": ["ink", "gr0", "gr1", "gr2", "dg0", "dg1", "dg2", "dg3", "ea0", "ea1", "ea2",
            "an0", "s3", "s4", "tk1"],
    # the houses: ochre plaster, terracotta roofs, sea-green paint, amphorae
    "house": ["ink", "dk", "w0", "oc0", "oc1", "oc2", "oc3", "tc0", "tc1", "tc2", "tc3",
              "te0", "te1", "te2", "wd1"],
    # Aphaia's golden poros with its painted blue and red, and the pebble mosaics
    "poros": ["ink", "w0", "po0", "po1", "po2", "po3", "po4", "b0", "b1", "b2", "rd",
              "tc1", "te1", "dk", "sk"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# aethos ground metatiles a cell can borrow
GROUND_METATILE = {"grass": 0x001, "sand": 0x124, "sea": 0x170, "path": 0x1D9}


def ground(s: Struct, kind: str, cells=None):
    """Put the given cells (default: all) on borrowed aethos ground. Their bottom
    layer stays empty: the build supplies aethos's ground there."""
    assert kind in GROUND_METATILE, kind
    if not hasattr(s, "ground"):
        s.ground = {}
    cells = cells or [(x, y) for y in range(s.h) for x in range(s.w)]
    for (cx, cy) in cells:
        s.ground[(cx, cy)] = kind
        s.B.rect(cx * 16, cy * 16, 16, 16, None)


def retitle(s, key, title, notes=None, walk=None, section="aegina"):
    s.key, s.title, s.section = key, title, section
    if notes is not None:
        s.notes = notes
    if walk is not None:
        s.walk = walk
    return s


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate(structs):
    problems = []
    for s in structs:
        gr = getattr(s, "ground", {})
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
                        problems.append(f"{s.key} metatile ({cx},{cy}) on borrowed ground draws a bottom")
                    if (s.T.a[sl][..., 3] > 0).any() and (s.M.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} metatile ({cx},{cy}) on borrowed ground uses both upper layers")
                    continue
                lower = np.maximum(s.B.a[sl][..., 3], s.M.a[sl][..., 3])
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} metatile ({cx},{cy}) has holes below the sprites layer")
    return problems


# --------------------------------------------------------------------------
# Previews with the real aethos ground
# --------------------------------------------------------------------------

def composite(s: Struct):
    """The structure as it will look in game: borrowed ground, then its layers."""
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    gr = getattr(s, "ground", {})
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        if ln == "bottom":
            for (cx, cy), kind in gr.items():
                out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = \
                    akti_lib.aethos_metatile(GROUND_METATILE[kind])
            m = a[..., 3] > 0
            for (cx, cy) in gr:
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        else:
            m = a[..., 3] > 0
        out[m] = a[..., :3][m]
    for (cx, cy) in getattr(s, "skip", ()):          # not part of the structure
        out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = (40, 40, 48)
    return out


def preview(structs, scale=3, bg=(40, 40, 48), cols=2):
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key, Image.fromarray(composite(s)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                         Image.NEAREST)) for s in structs]
    colw = max(i.width for _, i in imgs) + pad
    rows = [imgs[i:i + cols] for i in range(0, len(imgs), cols)]
    height = sum(max(i.height for _, i in r) + pad + 12 for r in rows) + pad
    out = Image.new("RGB", (cols * colw + pad, height), bg)
    d = ImageDraw.Draw(out)
    y = pad
    for r in rows:
        x = pad
        for key, i in r:
            d.text((x, y), key, fill=(230, 230, 200))
            out.paste(i, (x, y + 12))
            x += colw
        y += max(i.height for _, i in r) + pad + 12
    return out


def outline_mask(M, colors, edge_color):
    """Darken the silhouette edge of pixels whose color is in `colors`."""
    a = M.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if M.get(x, y) in colors:
            M.px(x, y, edge_color)
