"""Shared toolkit for gTileset_Eleusa, Eleusa Village's secondary tileset.

Eleusa is Eleusis: a farming village on the wheat plain, gold and earth, with
the sanctuary of the Mysteries at its heart. It pairs with the aethos primary.

It draws with agros_lib's layers and structures (so the agros pieces Eleusa
adopts, the alonia and the field wall, come across pixel for pixel, and the
soft-edged ground uses agros's shape engine) and adds:

  - Eleusa's palette plan: seven groups for the secondary's slots 6-12. Every
    8x8 tile of every layer takes all its colors from one group; validate()
    enforces it.
  - Borrowed ground, as Akti does it. A structure cell can sit on aethos grass,
    the limestone path or the sea. Its bottom layer stays empty in the sources;
    after Porytiles compiles, eleusa_build.py points the cell's bottom tiles at
    aethos's own ground metatile (grass 0x001, path 0x1D9, sea 0x170). The
    ground meets the meadow around it exactly, costs no Eleusa tiles, and the
    sea in the Rheitoi pools animates.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import GRASS, PATH, SEA, Layer, Struct, aethos  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors: agros's names (aethos ground, limestone, terracotta...), plus Eleusa's
# --------------------------------------------------------------------------

NEW = {
    # wheat, from the stalk's shadow to the sunlit ear
    "wk": (96, 56, 24), "wh1": (160, 104, 32), "wh2": (200, 144, 40), "wh3": (240, 192, 64),
    "wh4": (248, 224, 136),
    # stubble: earth between the rows, cut straw in shade and in sun
    "sb1": (152, 112, 56), "sb2": (200, 160, 80), "sb3": (232, 200, 120),
    # field poppies, Demeter's flower: scarlet, its light and its dark
    "pp0": (152, 24, 16), "pp1": (232, 48, 24), "pp2": (248, 120, 64),
    # Eleusa's houses: warm lime plaster over mudbrick
    "pl0": (152, 104, 64), "pl1": (200, 152, 96), "pl2": (232, 200, 144), "pl3": (248, 232, 192),
    # roof tiles, a deeper terracotta than the pots'
    "rf0": (96, 32, 16), "rf1": (152, 56, 32), "rf2": (200, 96, 56), "rf3": (232, 152, 104),
    # dark timber, door paint, the stone socle
    "wd0": (64, 40, 24), "wdx": (112, 72, 40), "wdy": (160, 112, 64),
    "ox": (128, 40, 32), "sg0": (104, 96, 88), "sg1": (152, 144, 128),
    # honey marble for the sacred buildings, and Eleusis's dark grey stone
    "m1": (240, 232, 208), "m2": (224, 208, 168), "m3": (192, 168, 120), "m4": (152, 120, 80),
    "m5": (104, 80, 56), "eg0": (56, 56, 72), "eg1": (96, 96, 112),
    "fl": (224, 80, 32), "fc": (248, 240, 168),
    # pomegranate and vine leaves
    "lf0": (40, 72, 40), "lf1": (72, 112, 48), "lf2": (120, 152, 64),
    # cave dark
    "cv": (24, 16, 24),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

GROUPS = {
    # wheat, stubble, poppies and thatch, on aethos grass
    "field": GRASS4 + ["wk", "wh1", "wh2", "wh3", "wh4", "sb1", "sb2", "sb3", "pp0", "pp1", "pp2"],
    # trees, the vine, pomegranates, on grass
    "grove": GRASS4 + ["t0", "t1", "lf0", "lf1", "lf2", "k1", "k2", "pp0", "pp1", "pp2", "ink"],
    # beaten earth and limestone: threshing floors, field walls, the Sacred Way,
    # grain heaps and the threshing sledge
    "earth": GRASS4 + ["p1", "p2", "p3", "l0", "l1", "w0", "wh1", "wh2", "wh3", "wd1", "ink"],
    # pots, pithoi, baskets, sacks and the bread oven
    "clay": ["tc0", "tc1", "tc2", "rf3", "ink", "wk", "wh1", "wh2", "wh3", "l0", "l1", "p1", "gd",
             "p2", "p3"],
    # houses: plaster, roof tiles, timber, door paint and the stone socle
    "house": ["pl0", "pl1", "pl2", "pl3", "rf0", "rf1", "rf2", "rf3", "wd0", "wdx", "wdy",
              "ox", "sg0", "sg1", "ink"],
    # the sanctuary: honey marble, grey Eleusinian stone, gold, fire, roof clay
    "marble": ["w0", "m1", "m2", "m3", "m4", "m5", "eg0", "eg1", "wh2", "wh3", "fl", "fc",
               "rf1", "rf2", "ink"],
    # rock and water: the Plutonion, the wells, the Rheitoi kerbs
    "rock": GRASS4 + ["l0", "l1", "p1", "p2", "p3", "b1", "b2", "b3", "b4", "cv", "ink"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sea": 0x170}


def ground(s: Struct, kind: str, cells=None):
    """Put the given cells (default: all) on borrowed aethos ground. Their bottom
    layer stays empty: the build supplies aethos's ground there."""
    if not hasattr(s, "ground"):
        s.ground = {}
    cells = cells if cells is not None else [(x, y) for y in range(s.h) for x in range(s.w)]
    for (cx, cy) in cells:
        s.ground[(cx, cy)] = kind
        s.B.rect(cx * 16, cy * 16, 16, 16, None)


def on_other_ground(s, key, kind, title=None, shadow=None):
    """A copy of a structure on another borrowed ground: the same art over
    aethos's grass, path or sea. It costs metatiles but no tiles, except where
    `shadow` (a color name) repaints the art's grass shadows ('gd') for the new
    ground."""
    c = Struct(key, title or s.title, s.w, s.h, s.section, walk=list(s.walk), notes=s.notes,
               names=dict(s.names))
    for ln in ("bottom", "middle", "top"):
        c.layers[ln].a[:] = s.layers[ln].a
    c.behaviors = dict(s.behaviors)
    c.ground = {cell: kind for cell in getattr(s, "ground", {})}
    if shadow:
        for L in (c.M, c.T):
            ys, xs = np.nonzero((L.a[..., 3] > 0) & (L.a[..., :3] == C["gd"]).all(-1))
            for y, x in zip(ys, xs):
                L.px(int(x), int(y), shadow)
    return c


def struct(key, title, w, h, section, walk=None, notes="", names=None, on=None):
    """A Struct, optionally on borrowed ground everywhere ('grass', 'path')."""
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names)
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch == "D":
                s.behaviors[(cx, cy)] = "MB_NON_ANIMATED_DOOR"
    if on:
        ground(s, on)
    return s


def tile_colors(layer, tx, ty):
    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
    m = t[..., 3] > 0
    return {tuple(int(v) for v in p) for p in t[m][:, :3]}


def validate(structs, group_rgb=None):
    """Problems with a set of structures: a tile whose colors fit no palette
    group (group_rgb defaults to Eleusa's), three layers in one cell, holes
    under the sprite layer, or bad borrowed-ground cells."""
    group_rgb = group_rgb or GROUP_RGB
    problems = []
    for s in structs:
        gr = getattr(s, "ground", {})
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if cols and not any(cols <= g for g in group_rgb.values()):
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
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground draws a bottom")
                    if (s.T.a[sl][..., 3] > 0).any() and (s.M.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground uses both upper layers")
                    continue
                lower = np.maximum(s.B.a[sl][..., 3], s.M.a[sl][..., 3])
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} metatile ({cx},{cy}) has holes below the sprites layer")
    return problems


def which_group(cols):
    for g, rgb in GROUP_RGB.items():
        if cols <= rgb:
            return g
    return None


# --------------------------------------------------------------------------
# Drawing helpers shared by the Eleusa painters
# --------------------------------------------------------------------------

def put(L, x, y, rows, legend, hflip=False):
    """Blit an ASCII grid with a legend of color names; ' ' and '.' are skipped."""
    for j, row in enumerate(rows):
        if hflip:
            row = row[::-1]
        for i, ch in enumerate(row):
            if ch in " ." or ch not in legend:
                continue
            L.px(x + i, y + j, legend[ch])


def copy_layer(dst, src, ox=0, oy=0):
    """Paint src's opaque pixels onto dst at (ox, oy)."""
    h, w = src.a.shape[:2]
    for y in range(h):
        for x in range(w):
            if src.a[y, x, 3]:
                yy, xx = oy + y, ox + x
                if 0 <= yy < dst.h and 0 <= xx < dst.w:
                    dst.a[yy, xx] = src.a[y, x]


def mirror_half(L, width):
    """Mirror the left half of a layer onto its right half (width in pixels)."""
    half = width // 2
    L.a[:, width - half:width] = L.a[:, :half][:, ::-1]


def grass(L, x, y, w, h, mask=None):
    L.texture(GRASS, x, y, w, h, mask)


def outline(L, color="ink"):
    """1 px dark outline on the silhouette edge of L's opaque pixels."""
    L.outline(color)


def shadow_on_grass(L, x0, y0, w, h, dither=True):
    """Darken aethos grass in a box (cast shadow): g2/g3 -> g1, g1 -> gd."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = L.get(x, y)
            if c in ("g2", "g3") and (not dither or (x + y) % 2 == 0 or y > y0):
                L.px(x, y, "g1")
            elif c == "g1":
                L.px(x, y, "gd")


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


def preview(structs, scale=2, bg=(40, 40, 48), cols=4):
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


# --------------------------------------------------------------------------
# Tile accounting (what Porytiles will store), and near-duplicate merging
# --------------------------------------------------------------------------

def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def tiles_of(structs):
    """Every distinct 8x8 tile up to flips, with where each is drawn. Borrowed
    ground and fully transparent tiles don't count."""
    occ = {}
    for s in structs:
        gr = getattr(s, "ground", {})
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    occ.setdefault(min(v.tobytes() for v in _flips(t)), []).append((s.key, layer, tx, ty))
    return occ


def merge_near_duplicates(structs, limit=2):
    """Redraw each tile within `limit` pixels of another as that other tile (as
    akti_build does). A tile is merged at most once, into one never merged
    itself. Tiles in different palette groups are never merged."""
    occ = tiles_of(structs)
    keys = list(occ)
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in _flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= limit)[0]:
            if j > i:
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, merges = set(), set(), []
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped:
            continue
        # transparency must match exactly, or a layer would gain or lose a hole
        if ((arr[a][..., 3] > 0) != (arr[b][..., 3] > 0)).any() and \
                all(((v[..., 3] > 0) != (arr[a][..., 3] > 0)).any() for v in _flips(arr[b])):
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (_, layer, tx, ty) in occ[drop]:
            cur = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            best = min(_flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
            if ((best[..., 3] > 0) != (cur[..., 3] > 0)).any():
                continue
            layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = best
        dropped.add(drop)
        kept.add(keep)
        merges.append(d)
    return merges


# --------------------------------------------------------------------------
# Shape keys for soft ground, from a region mask (map builders use this)
# --------------------------------------------------------------------------

NEIGHBORS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def blob_key(region, x, y):
    """The agros shape key of cell (x, y) in a boolean region grid [y][x]:
    '1|' then N NE E SE S SW W NW, a diagonal counting only when both of its
    sides are in the region. Cells off the grid count as in the region, so a
    field running off the map's edge keeps its interior."""
    h, w = len(region), len(region[0])

    def at(i, j):
        if not (0 <= i < w and 0 <= j < h):
            return 1
        return 1 if region[j][i] else 0
    b = [at(x + dx, y + dy) for dx, dy in NEIGHBORS]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)
