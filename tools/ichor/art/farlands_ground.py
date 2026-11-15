"""Soft ground for the far lands: every grass, earth, road and water region is a
set of 47 soft-edged shapes (agros_ground's blob machinery), drawn as an
overlay on borrowed aethos ground, so it fades into aethos's own grass (or
sand) with no seam and costs few tiles.

  blob_set()   a region painted over borrowed ground (or over a drawn base),
               one cell per shape key (farlands_lib.blob_key gives the key)
  join_set()   a road meeting aethos's limestone path: the cells where a dirt
               road (or red earth track) becomes the aethos path patch
               (0x1D0-0x1E2), so a road can run into a seam strip
  water_set()  water over borrowed aethos sea, its banks drawn over the land
               part of each edge cell

Each painter gets (layer, ox, oy, key, X, Y) and paints one 16x16 cell.
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
from agros_ground import blob_keys, halo, ring, visible
from farlands_lib import struct

KEYS = blob_keys()
FULL = "1|11111111"


def keys_grid(w=8):
    hh = (len(KEYS) + w - 1) // w
    return {k: (i % w, i // w) for i, k in enumerate(KEYS)}, hh


def blob_set(key, title, section, painter, on="grass", walk=".", notes="", base=None, oik=False,
             behavior=None):
    """A Struct with one cell per shape key, 8 wide. painter(L, ox, oy, key)
    draws the region's art into the middle layer. on: the borrowed aethos
    ground under it, or None with base(L, ox, oy) drawing an opaque bottom."""
    names, hh = keys_grid()
    w = 8
    s = struct(key, title, w, hh, section, walk=[walk * w] * hh, names=names, notes=notes, oik=oik)
    if behavior:
        for cy in range(hh):
            for cx in range(w):
                s.behaviors[(cx, cy)] = behavior
    if on:
        F.ground(s, on)
    for k, (cx, cy) in names.items():
        if base:
            base(s.B, cx * 16, cy * 16)
        painter(s.M, cx * 16, cy * 16, k)
    for i in range(len(KEYS), w * hh):
        cx, cy = i % w, i // w
        if base:
            base(s.B, cx * 16, cy * 16)
        painter(s.M, cx * 16, cy * 16, KEYS[-1])
    return s


def soft_mask(key, margin=1.0, radius=3.0, amp=1.4, seed=1.1, jag=0.0):
    vis, _ = visible(key, margin=margin, radius=radius, amp=amp, seed=seed, jag=jag)
    return vis


# --------------------------------------------------------------------------
# Tall grasses: tufts in staggered rows, lit from the top left
# --------------------------------------------------------------------------

def tuft_texture(ramp, gap, base, tip, tufts=None, seed=0, plume=None, lean=0.0):
    """A 16x16 periodic texture of grass tufts: {(x, y): color}. ramp is the
    blade ramp dark -> light (4); gap the color between tufts; base the
    color at a tuft's foot; tip the tip highlight; plume (optional) a pale
    color for feather-grass awns."""
    t = {}
    for y in range(16):
        for x in range(16):
            # between tufts: dark, with a green fleck at the foot of each row
            c = gap[0] if F.hp(x, y, 5 + seed) % 4 else gap[1]
            t[(x, y)] = c
    tufts = tufts or [(3, 7, 0), (11, 6, 1), (7, 15, 2), (15, 14, 3)]
    for (bx, by, k) in tufts:
        # the tuft's shadow at its foot
        for dx in range(-3, 4):
            t[((bx + dx) % 16, (by + 1) % 16)] = gap[0]
        blades = [(-4, 5), (-3, 7), (-1, 8), (0, 6), (1, 8), (3, 7), (4, 5)]
        for i, (dx, ht) in enumerate(blades):
            ht = ht - (F.h(k, i, seed) % 2)
            x0, y0 = bx, by
            x1, y1 = bx + dx + lean, by - ht
            n = max(abs(int(round(x1 - x0))), ht) + 1
            for j in range(n + 1):
                u = j / n
                X = int(round(x0 + (x1 - x0) * u * u if dx else x0 + (x1 - x0) * u))
                Y = int(round(y0 + (y1 - y0) * u))
                lvl = 0 if u < 0.25 else (1 if u < 0.55 else (2 if u < 0.85 else 3))
                if dx < 0:
                    lvl = min(3, lvl + 1) if u > 0.3 else lvl
                elif dx > 1:
                    lvl = max(0, lvl - 1)
                c = ramp[lvl]
                if u < 0.15:
                    c = base
                if j == n and dx <= 0:
                    c = tip
                t[(X % 16, Y % 16)] = c
            if plume and abs(dx) >= 3:
                # an awn arching out from the blade's tip
                px, py = bx + dx + lean, by - ht
                for j in range(1, 4):
                    t[(int(px + j * (1 if dx > 0 else -1)) % 16, int(py - (1 if j < 2 else 0)) % 16)] = plume
    return t


def recolor_tex(mid, mapping):
    """An aethos metatile's pixels as a {(x, y): color} texture, recolored by
    name. Grass cut from aethos's own barley (0x00D) or reeds (0x015) keeps
    their exact shapes, so the field effect cut from them still fits."""
    a = F.aethos(mid)
    t = {}
    for y in range(16):
        for x in range(16):
            n = F.A.RGB2NAME[tuple(int(v) for v in a[y, x])]
            t[(x, y)] = mapping.get(n, n)
    return t


def blade_texture(ramp, gap, foot, tip, per_row=7, rows=(7, 15), seed=0, plume=None,
                  plume_every=3, hmin=5, hmax=9, lean=0.0):
    """A 16x16 periodic field of grass blades standing in two staggered rows:
    {(x, y): color}. ramp: blade colors dark -> light (4); gap: (deep shadow,
    shade) between blades; foot: a blade's base; tip: its lit tip; plume: a
    pale awn waving off every plume_every-th blade (feather-grass)."""
    t = {}
    for y in range(16):
        for x in range(16):
            # the shadow deepens toward each row's foot
            dy = min((r - y) % 16 for r in rows)
            t[(x, y)] = gap[0] if dy <= 1 or F.hp(x, y, 5 + seed) % 5 == 0 else gap[1]
    blades = []
    for ri, base in enumerate(rows):
        off = (ri * 16 / per_row / 2) + (seed % 3) * 0.7
        for k in range(per_row):
            hh = F.h(k, ri, seed + 11)
            x = int(round(k * 16 / per_row + off + (hh % 3) - 1)) % 16
            by = base - (hh // 3) % 2
            ht = hmin + (hh // 7) % (hmax - hmin + 1)
            ln = lean + ((hh // 5) % 3 - 1) * 0.8
            blades.append((by, x, ht, ln, k))
    blades.sort()
    for (by, x, ht, ln, k) in blades:
        for j in range(ht + 1):
            u = j / ht
            X = int(round(x + ln * u * u))
            Y = by - j
            lvl = 0 if u < 0.3 else (1 if u < 0.6 else (2 if u < 0.85 else 3))
            if ln < -0.3 and u > 0.2:
                lvl = min(3, lvl + 1)
            c = foot if u < 0.18 else ramp[lvl]
            if j == ht:
                c = tip
            t[(X % 16, Y % 16)] = c
            # a darker edge on the blade's right side near the foot: depth
            if u < 0.5 and t.get(((X + 1) % 16, Y % 16)) in gap:
                t[((X + 1) % 16, Y % 16)] = gap[0]
        if plume and k % plume_every == 0:
            px, py = int(round(x + ln)), by - ht
            d = 1 if ln >= 0 else -1
            for j in range(1, 5):
                t[((px + d * j) % 16, (py - (1 if j < 3 else 0) + (1 if j == 4 else 0)) % 16)] = plume
    return t


def grass_overlay(tex, ring_c, awn_c, tip_c, margin=1.0, radius=4.5, amp=2.2, seed=1.1, jag=1.2,
                  awns=True):
    """Painter for a tall-grass region over borrowed ground."""
    def paint(L, ox, oy, key):
        vis = soft_mask(key, margin, radius, amp, seed, jag)
        for y in range(16):
            for x in range(16):
                if vis[y, x]:
                    L.px(ox + x, oy + y, tex[((ox + x) % 16, (oy + y) % 16)])
        for y, x in np.argwhere(ring(vis)):
            # the clump's rim: dark on the shaded (bottom, right) side, kept lit on top
            below = y + 1 < 16 and not vis[y + 1, x]
            right = x + 1 < 16 and not vis[y, x + 1]
            if below or right:
                L.px(ox + x, oy + y, ring_c)
        if awns:
            for y, x in np.argwhere(halo(vis)):
                if y + 1 < 16 and vis[y + 1, x] and (x * 5 + y * 3 + ox // 16) % 4 == 0:
                    L.px(ox + x, oy + y, awn_c)
                    if y - 1 >= 0 and not vis[y - 1, x] and (x + y) % 3 == 0:
                        L.px(ox + x, oy + y - 1, tip_c)
    return paint


# --------------------------------------------------------------------------
# Earth: dirt roads, red earth, mud
# --------------------------------------------------------------------------

def earth_overlay(px_fn, ring_c, halo_c=None, margin=2.5, radius=4.5, amp=1.8, seed=2.3,
                  halo_rate=3, ring_rate=1):
    """Painter for an earth region (a road, a field of red earth, mud).
    px_fn(X, Y) -> color of the region's texture at absolute pixel X, Y."""
    def paint(L, ox, oy, key):
        vis = soft_mask(key, margin, radius, amp, seed)
        for y in range(16):
            for x in range(16):
                if vis[y, x]:
                    L.px(ox + x, oy + y, px_fn(ox + x, oy + y))
        for y, x in np.argwhere(ring(vis)):
            if (x * 3 + y) % ring_rate == 0:
                L.px(ox + x, oy + y, ring_c)
        if halo_c:
            for y, x in np.argwhere(halo(vis)):
                if (x + 2 * y) % halo_rate == 0:
                    L.px(ox + x, oy + y, halo_c)
    return paint


# --------------------------------------------------------------------------
# Joins: a road meeting aethos's limestone path
# --------------------------------------------------------------------------

# the aethos path patch: (path side) -> the aethos piece the join's far half copies
PATH_PIECE = {
    # path to the south of the join: a north-south road's L, C, R cells
    ("S", "L"): 0x1D8, ("S", "C"): 0x1D9, ("S", "R"): 0x1DA,
    ("N", "L"): 0x1D8, ("N", "C"): 0x1D9, ("N", "R"): 0x1DA,
    # path to the east or west: an east-west road's T, C, B cells
    ("E", "T"): 0x1D1, ("E", "C"): 0x1D9, ("E", "B"): 0x1E1,
    ("W", "T"): 0x1D1, ("W", "C"): 0x1D9, ("W", "B"): 0x1E1,
}
# the road blob's shape key for the same cell of a straight road
ROAD_KEY = {
    "L": "1|11111000", "C": FULL, "R": "1|10001111",
    "T": "1|00111110", "B": "1|11100011",
}


def join_set(key, title, section, road_painter, road_base, blend_c, notes, oik=False):
    """Twelve cells where a road (drawn by road_painter over road_base's
    ground) becomes aethos's limestone path. Named `<side>_<cell>`: `S_L` is
    the left cell of a north-south road with the aethos path to its south.
    The half toward the path copies aethos's path piece pixel for pixel; the
    other half is the road's own straight piece; they meet in a ragged band."""
    names = {}
    order = [("S", "L"), ("S", "C"), ("S", "R"), ("N", "L"), ("N", "C"), ("N", "R"),
             ("E", "T"), ("E", "C"), ("E", "B"), ("W", "T"), ("W", "C"), ("W", "B")]
    w = 6
    for i, (side, cell) in enumerate(order):
        names[f"{side}_{cell}"] = (i % w, i // w)
    s = struct(key, title, w, 2, section, walk=["......", "......"], names=names, notes=notes,
               oik=oik)
    B = s.B
    tmp = F.Layer(16, 16)
    for (side, cell), (cx, cy) in ((k, names[f"{k[0]}_{k[1]}"]) for k in order):
        ox, oy = cx * 16, cy * 16
        # the road's own straight piece, at this cell's absolute position so
        # textures stay phase-locked
        road = F.Layer(s.w * 16, s.h * 16)
        road_base(road, ox, oy)
        road_painter(road, ox, oy, ROAD_KEY[cell])
        aeth = F.aethos(PATH_PIECE[(side, cell)])
        for y in range(16):
            for x in range(16):
                # u: 0 on the road side, 1 on the path side
                u = {"S": y / 15, "N": 1 - y / 15, "E": x / 15, "W": 1 - x / 15}[side]
                along = x if side in "NS" else y
                cut = 0.5 + 0.12 * math.sin(along * 0.9 + 1.3) + 0.06 * math.sin(along * 2.3)
                if u > cut:
                    B.rgb(ox + x, oy + y, aeth[y, x])
                else:
                    c = road.a[oy + y, ox + x]
                    B.rgb(ox + x, oy + y, c[:3])
                # the ragged band where wheels drag dirt onto the stone
                if abs(u - cut) < 0.07 and F.hp(ox + x, oy + y, 9) % 3 == 0:
                    rgb = tuple(int(v) for v in B.a[oy + y, ox + x, :3])
                    if F.A.RGB2NAME.get(rgb, "").startswith("p"):
                        B.px(ox + x, oy + y, blend_c)
    del tmp
    return s


# --------------------------------------------------------------------------
# Water with soft banks
# --------------------------------------------------------------------------

def water_painter(land_px, lip, shallow, ripple, margin=2.0, radius=5.0, amp=2.0, seed=4.1,
                  reeds=None):
    """Painter for a water region over borrowed aethos sea: the land part of
    an edge cell is drawn with land_px(X, Y) (aethos grass, pixel for pixel,
    so it meets the land beside it), a bank lip of `lip` colors (outer,
    inner), a pale shallow fringe, and a ripple line. reeds: (dark, mid,
    light, head) to plant clumps along the bank now and then."""
    def paint(L, ox, oy, key):
        vis = soft_mask(key, margin, radius, amp, seed)
        land = ~vis
        for y in range(16):
            for x in range(16):
                if land[y, x]:
                    L.px(ox + x, oy + y, land_px(ox + x, oy + y))
        lip_px = ring(land)

        def water_at(xx, yy):
            return 0 <= xx < 16 and 0 <= yy < 16 and vis[yy, xx]
        for y, x in np.argwhere(lip_px):
            if water_at(x, y + 1):
                # the bank drops to water below it: an earth face, two rows
                L.px(ox + x, oy + y, lip[0])
                if y - 1 >= 0 and land[y - 1, x]:
                    L.px(ox + x, oy + y - 1, lip[1])
            elif water_at(x, y - 1):
                # the bank's sunlit top edge
                L.px(ox + x, oy + y, lip[2] if len(lip) > 2 else lip[1])
            else:
                L.px(ox + x, oy + y, lip[1])
        # shallows: water pixels under a bank darken with its reflection,
        # those below the land's lit lip catch the light
        wet = halo(land) & vis
        for y, x in np.argwhere(wet):
            if y - 1 >= 0 and land[y - 1, x]:
                L.px(ox + x, oy + y, shallow)
            elif (x + y) % 2 == 0:
                L.px(ox + x, oy + y, ripple)
        # a ripple line a little way out
        p = np.pad(land, 3, constant_values=False)
        near = np.zeros_like(land)
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if 2.5 <= math.hypot(dx, dy) <= 3.5:
                    near |= p[3 + dy:3 + dy + 16, 3 + dx:3 + dx + 16]
        for y, x in np.argwhere(near & vis & ~wet):
            if (x + 2 * y) % 5 < 2:
                L.px(ox + x, oy + y, ripple)
        if reeds and key != FULL:
            # a reed clump on the bank wherever the bank faces north or west
            for (rx, ry) in ((4, 3), (11, 5), (6, 12), (13, 12)):
                if land[ry, rx] and not land[min(15, ry + 2), rx]:
                    reed_clump(L, ox + rx, oy + ry, reeds, small=True)
    return paint


def reed_clump(L, X, Y, cols, small=False):
    """A clump of reeds whose foot is at (X, Y): stems fanning up, a few
    cattail heads. cols = (dark, mid, light, head)."""
    d, m, l, hd = cols
    stems = [(-2, 5), (-1, 7), (0, 6), (1, 8), (2, 5)] if not small else [(-1, 4), (0, 5), (1, 4)]
    for i, (dx, ht) in enumerate(stems):
        for j in range(ht + 1):
            u = j / ht
            x = X + int(round(dx * u))
            y = Y - j
            L.px(x, y, d if u < 0.3 else (m if u < 0.7 else l))
        if i % 2 == 1 and not small:
            L.px(X + dx, Y - ht - 1, hd)
            L.px(X + dx, Y - ht, hd)
