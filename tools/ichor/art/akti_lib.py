"""Shared toolkit for gTileset_Akti, the harbor secondary for Akti Town.

It draws with kalliste_lib's layers and structures (so the kalliste pieces Akti
copies come across pixel for pixel) and adds:

  - Akti's own palette plan: seven groups for the secondary's slots 6-12. Every
    8x8 tile of every layer must take all its colors from one group;
    validate() enforces it.
  - Borrowed ground. A structure cell can sit on aethos grass, sand or sea. Its
    bottom layer is left empty in the sources, and after Porytiles compiles,
    akti_build.py gives the cell aethos's own ground metatile's bottom tiles
    (grass 0x001, sand 0x124, sea 0x170) under its art. The ground matches the
    meadow, beach or sea around it exactly, costs no Akti tiles, and the sea
    under every boat and rock animates with aethos's water.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kalliste_lib as K  # noqa: E402
from kalliste_lib import Layer, Struct, tile_colors  # noqa: E402,F401

ROOT = K.ROOT

# --------------------------------------------------------------------------
# Colors: kalliste's names, plus Akti's additions
# --------------------------------------------------------------------------

NEW = {
    # aethos's meadow and olive greens, so shadows and tufts sit on its grass
    "gr0": (184, 184, 104), "gr1": (144, 152, 72), "gr2": (208, 200, 128),
    "ov0": (40, 56, 32), "ov1": (72, 88, 48), "ov2": (112, 128, 64), "ov3": (152, 168, 120),
    "ov4": (200, 208, 176),
    "tk0": (88, 72, 56), "tk1": (128, 120, 112), "tk2": (168, 160, 152),
    # figs and grapes
    "pu0": (80, 40, 72), "pu1": (136, 72, 112),
    # a warm limestone and marble plaza
    "pv0": (192, 168, 128), "pv1": (216, 200, 160), "pv2": (240, 224, 192),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # whitewash, Aegean paint, terracotta pots, basil: houses, the shrine, laundry
    "cyc": ["ink", "dk", "w0", "w1", "w2", "w3", "w4", "b0", "b1", "b2", "b3",
            "tc1", "tc2", "ol1", "ol2"],
    # Hestia's marble and bronze: the temple, the altar, the krene's lion
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "br", "g0", "g1", "fl", "fc",
               "tc0", "tc1", "tc2"],
    # limestone: the quay, walls, terraces, the headland and its foam and weed
    "stone": ["sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "e2", "wt0", "wt1", "alg",
              "w0", "b3", "ol1"],
    # timber, rope, pitch and bronze: every boat, nets and rope
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "b0", "b1", "b2", "rd", "g1",
             "br", "g0", "tc1"],
    # the market: amphorae, baskets, the catch, octopus, the stall's awning
    "market": ["ink", "w0", "tc0", "tc1", "tc2", "tc3", "wd1", "wd2", "wd3", "sl2", "sl3",
               "b1", "b2", "rd", "g1"],
    # the plaza's warm paving and the krene's basin water
    "plaza": ["ink", "w0", "pv0", "pv1", "pv2", "s2", "m2", "m3", "m4", "tc1", "tc2",
              "b0", "b1", "b2", "b3"],
    # meadow, olive greens, the fig and the shrubs
    "grove": ["ink", "gr0", "gr1", "gr2", "ov0", "ov1", "ov2", "ov3", "ov4", "tk0", "tk1",
              "tk2", "pu0", "pu1", "wd2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

GROUND_METATILE = {"grass": 0x001, "sand": 0x124, "sea": 0x170}


def ground(s: Struct, kind: str, cells=None):
    """Put the given cells (default: all) on borrowed aethos ground. Their bottom
    layer stays empty: the build supplies aethos's ground there."""
    if not hasattr(s, "ground"):
        s.ground = {}
    cells = cells or [(x, y) for y in range(s.h) for x in range(s.w)]
    for (cx, cy) in cells:
        s.ground[(cx, cy)] = kind
        s.B.rect(cx * 16, cy * 16, 16, 16, None)


def empty(s: Struct, cells):
    """Mark cells that are just ground (not placed from this structure)."""
    if not hasattr(s, "skip"):
        s.skip = set()
    s.skip |= set(cells)


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

_AETHOS = {}


def aethos_metatile(mid):
    """16x16 RGB of an aethos metatile (both layers), for previews."""
    if mid not in _AETHOS:
        sys.path.insert(0, str(ROOT / "tools/ichor"))
        import render_map as R
        R.read_fieldmap_constants()
        sy = R.scan_tileset_symbols()
        r = R.Renderer(R.Tileset(sy["gTileset_Aethos"]), R.Tileset(sy["gTileset_Kalliste"]))
        _AETHOS[mid] = r.metatile(mid)[0]
    return _AETHOS[mid]


def composite(s: Struct):
    """The structure as it will look in game: borrowed ground, then its layers."""
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    gr = getattr(s, "ground", {})
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        if ln == "bottom":
            for (cx, cy), kind in gr.items():
                out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos_metatile(GROUND_METATILE[kind])
            m = a[..., 3] > 0
            for (cx, cy) in gr:
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        else:
            m = a[..., 3] > 0
        out[m] = a[..., :3][m]
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
