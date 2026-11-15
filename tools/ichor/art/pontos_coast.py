"""The Pontic coast for gTileset_Pontos: cliffs, rock masses and quays standing
in the dark green sea, drawn as autotiles.

A coast piece is one cell whose art depends on its 3x3 neighbourhood of land
and sea. The piece is cut from a 48x48 px drawing of that neighbourhood:

  - land cells, with convex corners rounded and concave corners filleted
    (radius CORNER px), so coastlines curve instead of stepping;
  - the cliff's face hanging FACE px below the land's south edge, into the sea
    cell below (the 3/4 view: you see a cliff's south face, not its north);
  - foam where the sea meets rock, two px deep;
  - the land's top: a rock rim and then aethos's own grass (chalk), a field of
    blue-black facets (kyanean), or quay paving (quay).

Every pixel depends only on cells within the 3x3, so neighbouring pieces meet
exactly. The pieces drawn are the ones the maps use: each map builder writes the
neighbourhoods it needs into pontos_shapes.json (`--shapes`), and this file
draws one piece per distinct result. A neighbourhood is a 9-character string of
0 (sea) and 1 (land), row by row, NW first.

Styles:
  chalk    the white cliffs of the Pontic shore: grass on top
  kyanean  the Kyaneai, the Clashing Rocks: blue-black rock right across
  quay     dressed stone: square corners, a coped edge you can walk to, an
           ashlar face on the south side
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np

import pontos_lib as P
from pontos_lib import Struct

SHAPES = Path(__file__).resolve().parent / "pontos_shapes.json"
CORNER = 5      # px: the radius of a rounded coast corner
FACE = {"chalk": 9, "kyanean": 9, "quay": 7}
STYLES = ("chalk", "kyanean", "quay")


def load_shapes():
    if not SHAPES.exists():
        return {s: [] for s in STYLES}
    data = json.loads(SHAPES.read_text())
    return {s: sorted(set(data.get(s, []))) for s in STYLES}


# --------------------------------------------------------------------------
# The neighbourhood as pixels
# --------------------------------------------------------------------------

def _cells(key):
    return [[key[r * 3 + c] == "1" for c in range(3)] for r in range(3)]


def land_pixels(key, rounded=True):
    """48x48 bool: land, with rounded convex corners and filleted concave ones."""
    cells = _cells(key)

    def cell(cx, cy):          # outside the 3x3: as the nearest cell inside it
        return cells[min(2, max(0, cy))][min(2, max(0, cx))]

    land = np.zeros((48, 48), bool)
    for cy in range(3):
        for cx in range(3):
            if cells[cy][cx]:
                land[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = True
    if not rounded:
        return land
    R = CORNER
    for j in range(4):
        for i in range(4):
            quad = {(dx, dy): cell(i - 1 + dx, j - 1 + dy) for dx in (0, 1) for dy in (0, 1)}
            n = sum(quad.values())
            px, py = i * 16, j * 16
            if n == 1 or n == 3:
                for (dx, dy), v in quad.items():
                    # n == 1: round the lone land cell's corner; n == 3: fillet the
                    # lone sea cell's corner with land
                    if (n == 1) != v:
                        continue
                    sx, sy = (1 if dx else -1), (1 if dy else -1)   # into that cell
                    cxp, cyp = px + sx * R - (0.5 if sx < 0 else -0.5), py + sy * R - (0.5 if sy < 0 else -0.5)
                    for yy in range(R):
                        for xx in range(R):
                            x = px + (xx if sx > 0 else -1 - xx)
                            y = py + (yy if sy > 0 else -1 - yy)
                            if not (0 <= x < 48 and 0 <= y < 48):
                                continue
                            pcx, pcy = x + 0.5, y + 0.5
                            far = (pcx - cxp - 0.5) ** 2 + (pcy - cyp - 0.5) ** 2 > R * R
                            if far:
                                land[y, x] = (n == 3)
            elif n == 2 and quad[(0, 0)] == quad[(1, 1)]:
                # a checkerboard: join the two land cells through the corner
                for (dx, dy), v in quad.items():
                    if v:
                        continue
                    sx, sy = (1 if dx else -1), (1 if dy else -1)
                    for yy in range(R - 1):
                        for xx in range(R - 1 - yy):
                            x = px + (xx if sx > 0 else -1 - xx)
                            y = py + (yy if sy > 0 else -1 - yy)
                            if 0 <= x < 48 and 0 <= y < 48:
                                land[y, x] = True
    return land


def _dilate(m, r=1):
    out = m.copy()
    for _ in range(r):
        n = out.copy()
        n[1:] |= out[:-1]
        n[:-1] |= out[1:]
        n[:, 1:] |= out[:, :-1]
        n[:, :-1] |= out[:, 1:]
        out = n
    return out


def _depth(m):
    """Steps from each True pixel to the nearest False one (4-connected), capped at 8."""
    d = np.zeros(m.shape, int)
    cur = m.copy()
    for k in range(1, 9):
        d[cur] = k
        e = cur.copy()
        e[1:] &= cur[:-1]
        e[:-1] &= cur[1:]
        e[:, 1:] &= cur[:, :-1]
        e[:, :-1] &= cur[:, 1:]
        cur = e
    return d


# --------------------------------------------------------------------------
# Textures that repeat every 16 px, so plain interiors share tiles
# --------------------------------------------------------------------------

def _rock_texture(seed=5):
    """16x16 blue-black facets for the Clashing Rocks' tops, tiling seamlessly."""
    from kalliste_parts import voronoi_labels
    rng = random.Random(seed)
    seeds = [(rng.randrange(16), rng.randrange(16)) for _ in range(5)]
    lab = voronoi_labels(16, 16, seeds, wrap=True, stretch=(1.0, 1.25))
    tone = ["ky3", "ky2", "ky3", "ky2", "ky1"]
    out = [["ky2"] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            k = lab[y, x]
            c = tone[k]
            if lab[y, (x + 1) % 16] != k or lab[(y + 1) % 16, x] != k:
                c = "ky0"
            elif lab[y, (x - 1) % 16] != k or lab[(y - 1) % 16, x] != k:
                c = "ky4" if tone[k] == "ky3" else "ky3"
            out[y][x] = c
    return out


ROCK_TEX = None
GRASS_TEX = None


def _quay_px(x, y):
    X, Y = x % 16, y % 16
    row = Y // 8
    bx, by = (X + (0 if row == 0 else 8)) % 16, Y % 8
    if by == 7 or bx == 15:
        return "ck1"
    if by == 0:
        return "ck4"
    if (bx, by, row) in ((4, 3, 0), (11, 5, 0), (2, 4, 1), (9, 2, 1)):
        return "ck2"
    return "ck3"


# --------------------------------------------------------------------------
# One piece
# --------------------------------------------------------------------------

INSET = {"chalk": 9, "kyanean": 12, "quay": 0}   # px of the face inside the land cell
DARKER = {"ck4": "ck3", "ck3": "ck2", "ck2": "ck1", "ck1": "ck0", "ky4": "ky3", "ky3": "ky2",
          "ky2": "ky1", "ky1": "ky0"}
LIGHTER = {v: k for k, v in DARKER.items()}


def draw(key, style, variant=0):
    """The 16x16 color names (None = sea shows) of `key`'s center cell, and
    whether the cell is solid, open land or open water.

    A cliff's south face is INSET px inside the land cell plus FACE px hanging
    into the sea cell below, so the white cliffs stand about a cell tall."""
    global ROCK_TEX, GRASS_TEX
    if ROCK_TEX is None:
        ROCK_TEX = {0: _rock_texture(5), 1: _rock_texture(17)}
        # plain meadow: aethos's grass is this color with a few specks, and a plain
        # rim lets every coast piece share its grass tiles
        GRASS_TEX = [["gr0"] * 16 for _ in range(16)]
    quay = style == "quay"
    land = land_pixels(key, rounded=not quay)
    F, S = FACE[style], INSET[style]
    # the plateau: land whose ground S px further south is land too
    plateau = land.copy()
    if S:
        below = np.ones_like(land)
        below[:-S] = land[S:]
        plateau &= below
    outer = np.zeros_like(land)
    for k in range(1, F + 1):
        outer[k:] |= land[:-k]
    outer &= ~land
    face = (land & ~plateau) | outer
    rock = land | outer
    sea = ~rock
    foam1 = sea & _dilate(rock, 1)
    foam2 = sea & _dilate(rock, 2) & ~foam1
    depth = _depth(plateau)
    out = [[None] * 16 for _ in range(16)]
    tex = ROCK_TEX[variant % 2]
    for yy in range(16):
        for xx in range(16):
            x, y = xx + 16, yy + 16
            h = P.hashed(x % 16, y % 16, 3)
            c = None
            if plateau[y, x]:
                d = depth[y, x]
                over_face = y + 1 < 48 and face[y + 1, x]
                near_face = any(y + j < 48 and face[y + j, x] for j in range(1, 7))
                if quay:
                    if d == 1 and over_face:
                        c = "ck4"
                    elif d == 1:
                        c = "ck1" if (y + 1 < 48 and sea[y + 1, x]) or (x + 1 < 48 and sea[y, x + 1]) else "ck4"
                    elif d == 2 and y >= 2 and sea[y - 2, x]:
                        c = "ck4"
                    else:
                        c = _quay_px(x, y)
                elif style == "chalk":
                    # a white lip of rock round the meadow, lit on its outer edge,
                    # grass in its shadow just inside
                    if near_face:                   # the lip over a south face
                        c = {1: "w0", 2: "ck4", 3: "gs"}.get(d, GRASS_TEX[y % 16][x % 16])
                    elif d == 1:
                        c = "ck0"
                    elif d == 2:
                        c = "w0"
                    elif d == 3:
                        c = "ck4"
                    elif d == 4:
                        c = "ck3" if h < 0.75 else "ck4"
                    elif d == 5:
                        c = "gs" if h < 0.7 else GRASS_TEX[y % 16][x % 16]
                    else:
                        c = GRASS_TEX[y % 16][x % 16]
                else:                                   # kyanean
                    if d == 1:
                        c = "ky4" if over_face else "ink"
                    elif d == 2:
                        c = "ky3" if over_face or near_face else "ky4"
                    elif d == 3 and not near_face:
                        c = "ky3"
                    else:
                        c = tex[y % 16][x % 16]
            elif face[y, x]:
                top = y
                while top - 1 >= 0 and face[top - 1, x]:
                    top -= 1
                bot = y
                while bot + 1 < 48 and face[bot + 1, x]:
                    bot += 1
                k, tall = y - top + 1, bot - top + 1
                bottom = bot - y
                left_open = x > 0 and not face[y, x - 1] and not plateau[y, x - 1]
                right_open = x < 47 and not face[y, x + 1] and not plateau[y, x + 1]
                if quay:
                    if bottom == 0:
                        c = "wt"
                    elif bottom == 1:
                        c = "wg" if h < 0.6 else "ck1"
                    elif (k - 1) % 4 == 3:
                        c = "ck1"
                    elif (x + (4 if ((k - 1) // 4) % 2 else 0)) % 8 == 0:
                        c = "ck1"
                    elif (k - 1) % 4 == 0:
                        c = "ck3"
                    else:
                        c = "ck2"
                else:
                    pre = "ck" if style == "chalk" else "ky"
                    streak = P.hashed(x % 16, 0, 11 if style == "chalk" else 13)
                    if k == 1:
                        c = pre + "4"
                    elif bottom == 0:
                        c = "wt"
                    elif bottom == 1:
                        c = "wg" if h < 0.55 else pre + "0"
                    elif streak < 0.18:
                        c = pre + "1"                     # a crack down the face
                    elif streak < 0.42:
                        c = pre + "2"
                    else:
                        c = pre + "3"
                    if 1 < k and bottom > 1 and k > tall * 0.62:
                        c = DARKER.get(c, c)              # the foot of the cliff in shadow
                    if k == 5 and streak >= 0.18:
                        c = DARKER.get(c, c)              # a band of flint
                    if left_open and bottom > 1:
                        c = LIGHTER.get(c, c)
                    if right_open:
                        c = pre + "0" if bottom > 0 else "wt"
            elif foam1[y, x]:
                c = "w0" if h < 0.72 else "pf"
            elif foam2[y, x]:
                c = "pf" if h < 0.45 else None
            out[yy][xx] = c
    center_land = key[4] == "1"
    any_sea = any(out[yy][xx] is None for yy in range(16) for xx in range(16))
    has_face = bool(outer[16:32, 16:32].any())
    if quay:
        kind = "land" if center_land else ("solid" if has_face else "water")
    elif center_land:
        all_grass = all(out[yy][xx] == "gr0" for yy in range(16) for xx in range(16))
        kind = "land" if (style == "chalk" and all_grass) else "solid"
    else:
        kind = "solid" if has_face else "water"
    return out, kind, any_sea


# --------------------------------------------------------------------------
# The pieces, one per distinct drawing
# --------------------------------------------------------------------------

def plain_key(style):
    return "1" * 9


def build(shapes=None):
    """Structures for every neighbourhood the maps need, deduplicated by art.
    Returns (structs, index) where index[style][key] = struct key."""
    shapes = shapes or load_shapes()
    structs, index = [], {s: {} for s in STYLES}
    seen = {}
    group = {"chalk": "chalk", "kyanean": "kyanean", "quay": "chalk"}
    for style in STYLES:
        keys = list(shapes[style])
        # the plain interior of a rock mass or a quay is a piece of its own
        if style in ("kyanean", "quay") and "1" * 9 not in keys:
            keys.append("1" * 9)

        for key in keys:
            if style == "chalk" and key == "1" * 9:
                continue        # plain grass: aethos's own
            if key == "0" * 9:
                continue        # open sea: the derived sea piece
            base, _, var = key.partition("#")
            art, kind, _ = draw(base, style, int(var or 0))
            if style == "chalk" and kind == "land":
                index[style][key] = "GRASS"      # nothing but meadow: aethos's grass
                continue
            sig = (style, kind, tuple(tuple(r) for r in art))
            if sig in seen:
                index[style][key] = seen[sig]
                continue
            n = len([s for s in structs if s.key.startswith(style + "_")])
            sk = f"{style}_{n:02d}"
            walk = {"solid": "X", "land": ".", "water": "."}[kind]
            s = Struct(sk, f"{style} coast piece {key}", 1, 1, walk=[walk], ground="psea",
                       notes=f"{style} autotile for neighbourhood {key[:3]}/{key[3:6]}/{key[6:]} "
                             f"(1 = land); {kind}")
            if kind == "water":
                s.behaviors[(0, 0)] = "MB_OCEAN_WATER"
            for yy in range(16):
                for xx in range(16):
                    if art[yy][xx] is not None:
                        s.M.px(xx, yy, art[yy][xx])
            s.coast = (style, kind)
            seen[sig] = sk
            index[style][key] = sk
            structs.append(s)
    return structs, index
