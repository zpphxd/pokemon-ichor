"""Shared toolkit for gTileset_Skiron, the secondary for Act I's mainland road.

Skiron holds the art for Route 4 (the Isthmus road: kilns, roadside tombs, the
diolkos, the Titans' rockslide, the procession's camp, a terrace orchard) and
Route 5 (the Skironian cliffs: the road cut along the sea cliffs, pines and
scrub, the rock seat, Aphrodite's niches). It draws with agros_lib's layers and
structures, adds its own colors and palette plan, and borrows aethos ground
the way akti does:

  - Palette plan: seven groups, one per secondary palette (6-12), at most 15
    colors each. Every 8x8 tile of every layer draws from ONE group;
    validate() enforces it.
  - Borrowed ground. A structure cell can sit on aethos grass (0x001), the
    limestone path (0x1D9) or the animated sea (0x170). Its bottom layer stays
    empty in the sources, and after Porytiles compiles, skiron_build.py points
    the cell's bottom tiles at aethos's own. The ground then matches the meadow,
    path or sea around it exactly and costs no Skiron tiles, and the sea under
    the cliff foot and the surf rocks animates. The same art on two grounds is
    two metatiles but no extra tiles.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import GRASS, PATH, SEA, TALL, Layer, Struct, aethos, tile_colors  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors: agros's names (aethos's ground, bark and clay), plus Skiron's own
# --------------------------------------------------------------------------

NEW = {
    # Aleppo pine: grey-green needles in open clumps, red-grey bark
    "pn0": (40, 64, 56), "pn1": (72, 104, 80), "pn2": (112, 144, 104), "pn3": (160, 184, 136),
    "rb": (152, 96, 72),
    # Pentelic-white marble and its shadows: stelai, lekythoi, the toppled tomb
    "m1": (224, 224, 216), "m2": (192, 192, 184), "m3": (152, 152, 144), "m4": (104, 104, 104),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 and 0 <= v <= 248 for v in _c), _n
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GROUPS = {
    # tall grass and its soft edges, thyme, goat tracks
    "field": ["g1", "g2", "g3", "gd", "t0", "t1", "t3", "tg", "p1", "p2", "p3", "l0", "l1",
              "th1", "th2"],
    # stone on grass: the paved road, the diolkos, rocks, ledges, the sea cliff and its
    # foam, the cut bank and the niches (white doves, red lamps), the seat, walls, the tower
    "rock": ["g1", "g2", "g3", "gd", "l0", "l1", "p1", "p2", "p3", "k1", "k2", "k3", "ink",
             "w0", "tc1"],
    # marble: stelai, lekythoi, the family plot, the mound's marker, the toppled tomb
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "g1", "g2", "g3", "gd", "tc1", "c2", "p1",
               "l1", "k2"],
    # Aleppo pines and kermes oak
    "pine": ["g1", "g2", "g3", "gd", "pn0", "pn1", "pn2", "pn3", "rb", "k1", "k3", "c1", "c2",
             "c3", "ink"],
    # fired clay and wood: kilns, pots, hives, firewood, the cart, the ship and its cradle
    "clay": ["tc0", "tc1", "tc2", "k1", "wd1", "wd2", "l1", "p1", "p2", "g1", "g2", "g3", "gd",
             "ink", "tg"],
    # the procession's camp: linen tents, myrtle, bedrolls, baskets
    "linen": ["ink", "w0", "w1", "m3", "k1", "wd1", "wd2", "c1", "c2", "c3", "g1", "g2", "g3",
              "gd", "tc1"],
    # flowers and fruit: thyme in bloom, the orchard's pomegranates
    "bloom": ["g1", "g2", "g3", "gd", "t1", "c1", "c2", "c3", "k1", "th1", "th2", "op1", "op2",
              "tg", "ink"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    for _n in _names:
        assert _n in C, _n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

GROUND_METATILE = {"grass": GRASS, "path": PATH, "sea": SEA}


def ground(s: Struct, kind: str, cells=None):
    """Put the given cells (default: all) on borrowed aethos ground. Their bottom
    layer is cleared: the build supplies aethos's ground there."""
    if not hasattr(s, "ground"):
        s.ground = {}
    cells = cells if cells is not None else [(x, y) for y in range(s.h) for x in range(s.w)]
    for (cx, cy) in cells:
        s.ground[(cx, cy)] = kind
        s.B.rect(cx * 16, cy * 16, 16, 16, None)


def regrounded(s: Struct, key: str, title: str, kind: str, notes=None):
    """A copy of a borrowed-ground structure on another aethos ground: the same
    art (so no new tiles), a new metatile for each cell."""
    t = Struct(key, title, s.w, s.h, s.section, walk=list(s.walk), notes=notes or s.notes,
               names=dict(s.names))
    for ln in ("bottom", "middle", "top"):
        t.layers[ln].a[:] = s.layers[ln].a
    t.behaviors = dict(s.behaviors)
    t.ground = {c: kind for c in getattr(s, "ground", {})}
    return t


def behave(s: Struct, cells, mb):
    for c in cells:
        s.behaviors[c] = mb


# --------------------------------------------------------------------------
# Small drawing helpers
# --------------------------------------------------------------------------

def disc(w, h, cx, cy, rx, ry):
    yy, xx = np.mgrid[0:h, 0:w]
    return ((xx - cx) / max(rx, 0.5)) ** 2 + ((yy - cy) / max(ry, 0.5)) ** 2 <= 1.0


def shade_ramp(L, mask, ramp, cx, cy, rx, ry, rim=None):
    """Fill a mask with a ramp lit from the top left (ramp: dark -> light)."""
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        u = ((x - cx) / max(rx, 1) + (y - cy) / max(ry, 1)) / 2
        k = 0.5 - 0.75 * u
        idx = int(max(0, min(len(ramp) - 1, round(k * (len(ramp) - 1)))))
        L.px(x, y, ramp[idx])
    if rim:
        pad = np.pad(mask, 1)
        edge = mask & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        for y, x in zip(*np.nonzero(edge)):
            L.px(x, y, rim)


def cast_shadow(L, x0, y0, w, h, dither=True, color="gd"):
    """A shadow on borrowed grass: opaque pixels of the shadow color in the art
    layer (the grass shows through the gaps of the dither)."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if not dither or (x + y) % 2 == 0:
                if L.get(x, y) is None:
                    L.px(x, y, color)


def oval_shadow(L, cx, cy, rx, ry, color="gd"):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if (d <= 0.5 or (d <= 1.0 and (x + y) % 2 == 0)) and L.get(x, y) is None:
                L.px(x, y, color)


def grass_floor(s, cells=None):
    """Paint aethos grass into the bottom layer (for cells that can't borrow)."""
    if cells is None:
        s.B.texture(GRASS, 0, 0, s.w * 16, s.h * 16)
    else:
        for (cx, cy) in cells:
            s.B.texture(GRASS, cx * 16, cy * 16, 16, 16)


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
                    if cols and not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(A.RGB2NAME.get(c, str(c)) for c in cols)
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
        m = a[..., 3] > 0
        if ln == "bottom":
            for (cx, cy), kind in gr.items():
                out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos(GROUND_METATILE[kind])
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        out[m] = a[..., :3][m]
    return out


def preview(structs, scale=2, bg=(40, 40, 48), width=1100):
    """Every structure composited with its key, flowed into rows."""
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key, Image.fromarray(composite(s)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                         Image.NEAREST)) for s in structs]
    rows, row, x = [], [], pad
    for key, im in imgs:
        if row and x + im.width > width:
            rows.append(row)
            row, x = [], pad
        row.append((key, im))
        x += max(im.width, 6 * len(key)) + pad
    if row:
        rows.append(row)
    height = sum(max(i.height for _, i in r) + pad + 12 for r in rows) + pad
    out = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(out)
    y = pad
    for r in rows:
        x = pad
        for key, im in r:
            d.text((x, y), key, fill=(230, 230, 200))
            out.paste(im, (x, y + 12))
            x += max(im.width, 6 * len(key)) + pad
        y += max(i.height for _, i in r) + pad + 12
    return out
