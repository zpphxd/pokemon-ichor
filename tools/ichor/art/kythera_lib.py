"""Shared toolkit for gTileset_Kythera, Act III's sea-foam island secondary.

Kythera is Aphrodite's island: white marble and pink stone, myrtle and roses,
foam-white surf on shingle and sand, scallop shells, doves and bronze mirrors.
It pairs with the aethos primary and serves Skandeia, the Foam Road, the Spring
of Kallirhoe, Echo's sea caves, Paphia, the Neraida falls, Melos, and the sea
maps of Routes 22 and 23.

It draws with agros_lib's layers and structures, as Eleusa does, and adds:

  - Kythera's palette plan: seven groups for the secondary's slots 6-12. Every
    8x8 tile of every layer (and of every animation frame) takes all its colors
    from one group; validate() enforces it.
  - Borrowed ground. A cell can sit on aethos's grass, limestone path, sand,
    sea, turquoise shallows or falling water. Its bottom layer stays empty in
    the sources; after Porytiles compiles, kythera_build.py points the cell's
    bottom tiles at aethos's own ground metatile (GROUND_METATILE). The sea, the
    shallows and the waterfall keep aethos's animation, and cost no Kythera
    tiles.
  - Animations. A structure can carry extra frames of one layer
    (Struct.anims[name] = [frame arrays]); every 8x8 tile that changes between
    frames becomes a Porytiles animated tile. The surf's foam, Aphrodite's
    rock's foam collar, the mill wheel and the obsidian's glints animate this
    way, over the borrowed sea where there is water.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import Layer, Struct, aethos  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors: agros's names (aethos ground, sea, grass...), plus Kythera's
# --------------------------------------------------------------------------

NEW = {
    # pale aqua: aethos's turquoise shallows, and foam's own shadow
    "kq1": (88, 176, 200), "kq2": (168, 224, 232),
    # aethos's sand, exactly
    "ks1": (200, 168, 104), "ks2": (232, 208, 144),
    # white rock and shingle: Aphrodite's rock, reefs, quays, pumice
    "kr0": (88, 88, 104), "kr1": (136, 136, 152), "kr2": (184, 184, 192), "kr3": (224, 224, 224),
    # rose marble and pink stone, from the cave's shadow to the sunlit marble
    "rm0": (80, 48, 64), "rm1": (136, 80, 96), "rm2": (184, 120, 128), "rm3": (224, 160, 160),
    "rm4": (240, 200, 192), "rm5": (248, 232, 224),
    "mw2": (208, 200, 200), "mw3": (152, 144, 152), "cv0": (32, 24, 40),
    # myrtle, sea-grass and leaves; bark; roses, thrift and oleander
    "my1": (48, 88, 56), "my2": (72, 128, 72), "my3": (120, 168, 88), "my4": (176, 200, 120),
    "kt1": (104, 80, 64), "kt2": (160, 128, 96),
    "rs1": (200, 48, 80), "rs2": (232, 120, 152), "rs3": (248, 192, 208),
    # Cycladic whitewash in shade, Aegean paint, rose-pink door frames, a green door
    "cw1": (224, 224, 216), "cw2": (184, 184, 184), "cw3": (128, 128, 144), "ab0": (24, 56, 120),
    "pf1": (240, 160, 176), "pf2": (200, 96, 120), "kgr": (56, 128, 104),
    # terracotta and timber
    "tc3": (240, 184, 136), "wd0": (64, 40, 24), "wd3": (208, 168, 120),
    # bronze and verdigris, Minoan paint and plaster
    "bz0": (72, 48, 32), "bz1": (136, 96, 48), "bz2": (200, 152, 72), "bz3": (240, 208, 128),
    "vg1": (64, 128, 112), "vg2": (136, 192, 168), "mr": (176, 56, 40), "pl": (232, 216, 184),
    # Melos: obsidian, from its black heart to the glassy sheen
    "ob0": (16, 16, 32), "ob1": (40, 40, 64), "ob2": (80, 80, 112), "ob3": (136, 144, 184),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

GROUPS = {
    # sea-foam and white stone: the surf, foam lace, shingle, Aphrodite's rock,
    # reefs and tide rocks, the quays (on aethos's limestone path: p1-p3),
    # Melos's pumice. The sea itself is always borrowed, so no deep blues.
    "foam": ["b3", "b4", "w0", "kq1", "kq2", "kr0", "kr1", "kr2", "kr3", "ks1", "ks2",
             "p1", "p2", "p3", "l1"],
    # rose marble and pink stone: sea-cliffs, the quarry, the temple front, the
    # great stair, plinths, the spring's kerb and its moss, the cave walls. It
    # carries aethos's grass (g1, g2; g3 is drawn as g2) so stone can sit in
    # the meadow inside one tile.
    "rose": ["rm0", "rm1", "rm2", "rm3", "rm4", "rm5", "w0", "mw2", "mw3", "cv0", "my1",
             "my2", "my3", "g1", "g2"],
    # myrtle, sea-grass and thrift, roses, narcissus, plane, oleander, apple
    "green": GRASS4 + ["t0", "my1", "my2", "my3", "my4", "kt1", "kt2", "rs1", "rs2", "rs3",
                       "w0"],
    # Cycladic houses: whitewash, Aegean doors, rose-pink frames, pots of roses
    # and basil, Melos's painted sea doors, dovecotes
    "cyc": ["w0", "cw1", "cw2", "cw3", "ab0", "b1", "b3", "pf1", "pf2", "tc1", "tc2", "my2",
            "rs1", "kgr", "ink"],
    # terracotta and timber: boats, the trireme, slips and keels, the mill
    # wheel, bridges, weirs, amphorae, hives and racks
    "terra": ["tc0", "tc1", "tc2", "tc3", "wd0", "wd1", "wd2", "wd3", "w0", "ink", "b1",
              "b2", "kr1", "kr2", "rs1"],
    # bronze: mirrors on walls, the harbor shrine's dove, the great herm; the
    # Minoan vault door's plaster and paint
    "bronze": ["bz0", "bz1", "bz2", "bz3", "vg1", "vg2", "w0", "cw1", "cw2", "cw3", "ink",
               "mr", "b1", "pl", "ab0"],
    # Melos's obsidian slope on its earth and grass
    "melos": GRASS4 + ["ob0", "ob1", "ob2", "ob3", "b4", "w0", "l0", "l1", "p1", "ks2",
                       "kt1"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# aethos ground a cell can borrow (its bottom-layer tiles)
GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sand": 0x124, "sea": 0x170,
                   "shallow": 0x0D1, "fall": 0x0B3}

# walk codes -> metatile behaviors
WALK_BEHAVIOR = {
    "G": "MB_TALL_GRASS", "J": "MB_JUMP_SOUTH", "<": "MB_JUMP_WEST", ">": "MB_JUMP_EAST",
    "D": "MB_NON_ANIMATED_DOOR", "W": "MB_OCEAN_WATER", "P": "MB_POND_WATER",
    "F": "MB_WATERFALL", "S": "MB_SAND",
}


def struct(key, title, w, h, section, walk=None, notes="", names=None, on=None):
    """A Struct whose walk codes set its behaviors, optionally on borrowed
    ground everywhere ('grass', 'sand', 'sea'...)."""
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names)
    s.behaviors = {}
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch in WALK_BEHAVIOR:
                s.behaviors[(cx, cy)] = WALK_BEHAVIOR[ch]
    s.anims = {}
    s.ground = {}
    if on:
        ground(s, on)
    return s


def ground(s, kind, cells=None):
    """Put cells (default: all) on borrowed aethos ground. Their bottom layer
    stays empty: the build supplies aethos's ground there."""
    assert kind in GROUND_METATILE, kind
    cells = cells if cells is not None else [(x, y) for y in range(s.h) for x in range(s.w)]
    for (cx, cy) in cells:
        s.ground[(cx, cy)] = kind
        s.B.rect(cx * 16, cy * 16, 16, 16, None)


def anim_layer(s, name, n, layer="middle"):
    """Start an animation on one of s's layers: returns n-1 extra frame Layers,
    each a copy of the layer as it is now (frame 0 is the layer itself).
    Paint the differences into them."""
    src = s.layers[layer]
    frames = []
    for _ in range(n - 1):
        L = Layer(src.w, src.h)
        L.a[:] = src.a
        frames.append(L)
    s.anims[name] = {"layer": layer, "frames": frames}
    return frames


def settle(s, name, cells):
    """Declare every cell of s outside `cells` static for animation `name`:
    copy the base layer's pixels there into each frame (art drawn on the base
    layer after anim_layer() is then not mistaken for animation)."""
    an = s.anims[name]
    base = s.layers[an["layer"]].a
    cells = set(cells)
    for cy in range(s.h):
        for cx in range(s.w):
            if (cx, cy) in cells:
                continue
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            for f in an["frames"]:
                f.a[sl] = base[sl]


def copy_struct(s, key, title=None, notes=None):
    c = struct(key, title or s.title, s.w, s.h, s.section, walk=list(s.walk),
               notes=notes if notes is not None else s.notes, names=dict(s.names))
    for ln in ("bottom", "middle", "top"):
        c.layers[ln].a[:] = s.layers[ln].a
    c.behaviors = dict(s.behaviors)
    c.ground = dict(s.ground)
    for name, an in s.anims.items():
        fr = []
        for f in an["frames"]:
            L = Layer(f.w, f.h)
            L.a[:] = f.a
            fr.append(L)
        c.anims[name] = {"layer": an["layer"], "frames": fr}
    return c


def pick(s, names, w=None, key=None, title=None, notes=None, section=None):
    """A new structure holding only the named single cells of s, laid out in
    rows of w (default: all in one row), in the given order. Layers, ground,
    behaviors, walk codes and animation frames come across."""
    names = list(names)
    w = w or len(names)
    hh = (len(names) + w - 1) // w
    cells = [s.names[n] for n in names]
    walk = []
    for j in range(hh):
        row = ""
        for i in range(w):
            k = j * w + i
            row += s.walk[cells[k][1]][cells[k][0]] if k < len(cells) else s.walk[cells[-1][1]][cells[-1][0]]
        walk.append(row)
    c = struct(key or s.key, title or s.title, w, hh, section or s.section, walk=walk,
               notes=notes if notes is not None else s.notes,
               names={n: (k % w, k // w) for k, n in enumerate(names)})
    srcs = {an: v for an, v in s.anims.items()}
    frames = {an: [Layer(w * 16, hh * 16) for _ in v["frames"]] for an, v in srcs.items()}
    for k in range(w * hh):
        sx, sy = cells[min(k, len(cells) - 1)]
        dx, dy = k % w, k // w
        ssl = np.s_[sy * 16:sy * 16 + 16, sx * 16:sx * 16 + 16]
        dsl = np.s_[dy * 16:dy * 16 + 16, dx * 16:dx * 16 + 16]
        for ln in ("bottom", "middle", "top"):
            c.layers[ln].a[dsl] = s.layers[ln].a[ssl]
        if (sx, sy) in s.ground:
            c.ground[(dx, dy)] = s.ground[(sx, sy)]
        if (sx, sy) in s.behaviors:
            c.behaviors[(dx, dy)] = s.behaviors[(sx, sy)]
        for an, v in srcs.items():
            for fi, f in enumerate(v["frames"]):
                frames[an][fi].a[dsl] = f.a[ssl]
    for an, v in srcs.items():
        c.anims[an] = {"layer": v["layer"], "frames": frames[an]}
    return c


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def h(x, y, k=0):
    """A cheap hash of a pixel position, 0..96."""
    return (x * 73 + y * 151 + k * 37 + (x * y + k) % 7) % 97


def hp(x, y, k=0, period=16):
    """h() on 16 px periodic coordinates, so textures tile."""
    return h(x % period, y % period, k)


def put(L, x, y, rows, legend, hflip=False):
    """Blit an ASCII grid with a legend of color names; ' ' and '.' are skipped."""
    for j, row in enumerate(rows):
        if hflip:
            row = row[::-1]
        for i, ch in enumerate(row):
            if ch in " ." or ch not in legend:
                continue
            L.px(x + i, y + j, legend[ch])


def fill(L, ox, oy, w, h_, fn, mask=None):
    """Fill a box with fn(absolute x, absolute y) -> color name (or None)."""
    for y in range(oy, oy + h_):
        for x in range(ox, ox + w):
            if mask is not None and not mask(x - ox, y - oy):
                continue
            c = fn(x, y)
            if c:
                L.px(x, y, c)


def outline(L, color="ink", ref=None):
    L.outline(color, ref)


def tex(L, mid, x, y, w, h_, mask=None):
    """Fill with an aethos metatile's pixels, locked to the 16 px grid."""
    L.texture(mid, x, y, w, h_, mask)


def shade_box(L, x0, y0, w, h_, ramp, step=1):
    """Darken a box's pixels one step along a ramp (list of names, light->dark)."""
    for y in range(y0, y0 + h_):
        for x in range(x0, x0 + w):
            c = L.get(x, y)
            if c in ramp:
                i = min(len(ramp) - 1, ramp.index(c) + step)
                L.px(x, y, ramp[i])


def tile_colors(layer, tx, ty):
    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
    m = t[..., 3] > 0
    return {tuple(int(v) for v in p) for p in t[m][:, :3]}


# --------------------------------------------------------------------------
# Animation bookkeeping
# --------------------------------------------------------------------------

def anim_tiles(s):
    """{(layer name, tx, ty): anim name} for every tile of s that changes
    between frames."""
    out = {}
    for name, an in s.anims.items():
        base = s.layers[an["layer"]].a
        for f in an["frames"]:
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                    if not np.array_equal(base[sl], f.a[sl]):
                        out[(an["layer"], tx, ty)] = name
    return out


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate(structs, group_rgb=None):
    """Problems: a tile (over all its frames) whose colors fit no group, three
    layers in one cell, holes under the sprite layer, bad borrowed cells."""
    group_rgb = group_rgb or GROUP_RGB
    problems = []
    for s in structs:
        gr = s.ground
        at = anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if (ln, tx, ty) in at:
                        an = s.anims[at[(ln, tx, ty)]]
                        for f in an["frames"]:
                            cols |= tile_colors(f, tx, ty)
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
                if n == 0:
                    problems.append(f"{s.key} metatile ({cx},{cy}) is empty")
    return problems


def which_group(cols, group_rgb=None):
    for g, rgb in (group_rgb or GROUP_RGB).items():
        if cols <= rgb:
            return g
    return None


# --------------------------------------------------------------------------
# Previews with the real aethos ground
# --------------------------------------------------------------------------

def composite(s, frame=0):
    """The structure as it will look in game: borrowed ground, then its layers
    (an animation shown at `frame`)."""
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    gr = s.ground
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        for an in s.anims.values():
            if an["layer"] == ln and frame and frame - 1 < len(an["frames"]):
                a = an["frames"][frame - 1].a
        m = a[..., 3] > 0
        if ln == "bottom":
            m = m.copy()
            for (cx, cy), kind in gr.items():
                out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos(GROUND_METATILE[kind])
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        out[m] = a[..., :3][m]
    return out


def preview(structs, scale=2, bg=(40, 40, 48), cols=4, frame=0, maxw=None):
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key, Image.fromarray(composite(s, frame)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                                Image.NEAREST)) for s in structs]
    colw = max(i.width for _, i in imgs) + pad
    if maxw:
        colw = min(colw, maxw)
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


def shelf_preview(structs, scale=2, width=1500, bg=(40, 40, 48), frame=0):
    """Pieces laid left to right in rows up to `width` px, labelled."""
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key, Image.fromarray(composite(s, frame)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                                Image.NEAREST)) for s in structs]
    rows, cur, cw = [], [], pad
    for k, i in imgs:
        w = max(i.width, len(k) * 6) + pad
        if cur and cw + w > width:
            rows.append(cur)
            cur, cw = [], pad
        cur.append((k, i))
        cw += w
    if cur:
        rows.append(cur)
    height = sum(max(i.height for _, i in r) + pad + 12 for r in rows) + pad
    out = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(out)
    y = pad
    for r in rows:
        x = pad
        for key, i in r:
            d.text((x, y), key, fill=(230, 230, 200))
            out.paste(i, (x, y + 12))
            x += max(i.width, len(key) * 6) + pad
        y += max(i.height for _, i in r) + pad + 12
    return out


# --------------------------------------------------------------------------
# Tile accounting, and near-duplicate merging (animated tiles excluded)
# --------------------------------------------------------------------------

def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def tiles_of(structs, include_anim=True):
    """Every distinct 8x8 tile up to flips, with where each is drawn. Borrowed
    ground and fully transparent tiles don't count."""
    occ = {}
    for s in structs:
        gr = s.ground
        at = anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    if not include_anim and (ln, tx, ty) in at:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    occ.setdefault(min(v.tobytes() for v in _flips(t)), []).append((s.key, layer, tx, ty))
    return occ


def merge_near_duplicates(structs, limit=2, group_rgb=None):
    """Redraw each static tile within `limit` pixels of another as that other
    tile. A tile is merged at most once, into one never merged itself, and
    only within the same palette group. Animated tiles are left alone."""
    group_rgb = group_rgb or GROUP_RGB
    occ = tiles_of(structs, include_anim=False)
    keys = list(occ)
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}

    def grp(k):
        a = arr[k]
        m = a[..., 3] > 0
        return which_group({tuple(int(v) for v in p) for p in a[m][:, :3]}, group_rgb)
    groups = {k: grp(k) for k in keys}
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
        if a in dropped or b in dropped or groups[a] != groups[b]:
            continue
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
    sides are in the region. Cells off the grid count as in the region."""
    hh, ww = len(region), len(region[0])

    def at(i, j):
        if not (0 <= i < ww and 0 <= j < hh):
            return 1
        return 1 if region[j][i] else 0
    b = [at(x + dx, y + dy) for dx, dy in NEIGHBORS]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)
