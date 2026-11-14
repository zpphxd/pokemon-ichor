"""The Aegean: water textures and every animated tile in aethos.

The sea is a deep Aegean blue with small arcing wave crests that rock back and
forth; shallows over sand are turquoise with sunlit ripples. Beaches get a
wash of surf that runs up the sand and drains back. All animation keeps
General's tile slots and frame counts, so every water metatile still animates.

Anim tile roles (General's slot numbers):
  water 0-15   open sea under the sea-rock metatiles (a 32x32 patch)
  water 16-21  shallows over sand
  water 22-23  open sea, laid out [22 23 / 23 22] (CalmWater 0x170)
  water 24-25  sea channel
  water 26-27  rough water (currents)
  water 28-29  deep water (dive spots)
"""
import numpy as np

from aethos_lib import (PAL, art, rgba, split_tiles, join_tiles, load_rgba,
                        BASE, anim_frame_names)
from aethos_textures import SAND

SEA_LEG = dict(m="ae_m", n="ae_n", l="ae_l", h="ae_h", d="ae_d", k="ae_k", f="foam")

# One 16x8 strip [A|B]; the full sea tile is [A B / B A].
SEA_STRIP = art("""
    mmmmmmmmmmmmmmmm
    mmmmmmmmmmmmmmmm
    mmnlllhnmmmmmmmm
    mmmnnnnmmmmmmmmm
    mmmmmmmmmmmmmmmm
    mmmmmmmmmmmmmmmm
    mmmmmmmmmmnllllm
    mmmmmmmmmmmnnnmm
""", SEA_LEG)

ROUGH_STRIP = art("""
    mmmmmmmmmmmmmmmm
    mnllhlnmmmmmmmmm
    mmnnnnmmmmmmlmmm
    mmmmmmmmmmmmmmmm
    mmmmmmmmmmmmmmmm
    mmmmmmmmnllhllnm
    mmmlmmmmmnnnnnmm
    mmmmmmmmmmmmmmmm
""", SEA_LEG)

DEEP_STRIP = art("""
    dddddddddddddddd
    dddddddddddddddd
    ddmnnnmddddddddd
    dddmmmdddddddddd
    dddddddddddddddd
    dddddddddddddddd
    ddddddddddmnnnmd
    dddddddddddmmmdd
""", SEA_LEG)

SHALLOW_LEG = dict(t="ae_t", l="ae_h", s="sd_l", n="ae_l")
SHALLOW_STRIP = art("""
    tttttttttttttttt
    ttlltttttttttttt
    ttttlttttttstttt
    tttttltttttttttt
    tstttttttllltttt
    tttttttttttttltt
    ttttttttttttttlt
    tttttttstttttttt
""", SHALLOW_LEG)

# frame t: crest rows drift right in the top half and left in the bottom half
SWAY = [0, 1, 2, 1, 0, -1, -2, -1]


def sea_frame(strip, t):
    s = strip.copy()
    dx = SWAY[t % 8]
    s[:4] = np.roll(strip[:4], dx, axis=1)
    s[4:] = np.roll(strip[4:], -dx, axis=1)
    return np.concatenate([s, np.roll(s, 8, axis=1)], axis=0)  # 16x16


def shallow_frame(t):
    s = SHALLOW_STRIP.copy()
    dx = [0, 1, 1, 2, 2, 1, 1, 0][t % 8]
    s = np.roll(s, dx, axis=1)
    return np.concatenate([s, np.roll(s, 8, axis=1)], axis=0)


def quads(img16):
    """16x16 -> [A, B] 8x8 tiles of its top row (the strip)."""
    return [img16[0:8, 0:8], img16[0:8, 8:16]]


def nudge_unique(tiles, taken=None):
    """Make every tile distinct from the others (and their flips) by moving
    one pixel one step along its own ramp. Mirrors Porytiles' mangle, but
    deterministic and invisible."""
    seen = set(taken or ())
    out = []
    order = [PAL[n] for n in ("ae_k", "ae_d", "ae_m", "ae_n", "ae_l", "ae_h", "foam",
                             "ae_t", "sd_d", "sd_m", "sd_l", "lp_h")]
    for t in tiles:
        t = t.copy()
        k = 0
        while True:
            forms = {t.tobytes(), t[:, ::-1].tobytes(), t[::-1].tobytes(), t[::-1, ::-1].tobytes()}
            if not forms & seen or not t[..., 3].any():
                break
            y, x = divmod((k * 5 + 3) % 64, 8)
            c = tuple(int(v) for v in t[y, x, :3])
            if t[y, x, 3] and c in order:
                i = order.index(c)
                alt = order[i + 1] if i + 1 < len(order) and i not in (6, 10) else order[i - 1]
                t[y, x, :3] = alt
            k += 1
            if k > 400:
                raise SystemExit("aethos_water: cannot make tile unique")
        seen |= {t.tobytes()}
        out.append(t)
    return out


# Sun glints that make each tile of the 32x32 sea patch its own tile, so the
# key frame needs no nudging. They sit on rows the wave crests never cross.
GLINTS = [(0, 1), (4, 5), (1, 3), (5, 7), (4, 0), (0, 4), (5, 2), (1, 6),
          (0, 3), (5, 5), (4, 6), (1, 0), (0, 7), (4, 1), (5, 4), (1, 4)]
# Shallows slots 18-21 repeat 16-17's ripple; a pebble tells them apart.
SHALLOW_MARKS = {2: (6, 6), 3: (2, 1), 4: (6, 2), 5: (1, 5)}

CHANNEL_STRIP = art("""
    mmmmmmmmmmmmmmmm
    mmmmmmdmmmmmmmmm
    mmnllnmmmmmmmmmm
    mmmmmmmmmmmmmdmm
    mmmmmmmmmmmmmmmm
    mmdmmmmmmmmmmmmm
    mmmmmmmmmmnllnmm
    mmmmmmmmmmmmmmmm
""", SEA_LEG)


def water_frames():
    """[key, f0..f7] for the 30-tile water anim (16x120 each)."""
    frames = []
    for t in range(8):
        sea = sea_frame(SEA_STRIP, t)
        rough = sea_frame(ROUGH_STRIP, (t * 2) % 8)
        deep = sea_frame(DEEP_STRIP, t)
        chan = sea_frame(CHANNEL_STRIP, (t + 4) % 8)
        shal = shallow_frame(t)
        tiles = []
        # 0-15: a 32x32 patch of open sea under the sea rocks, four rows of
        # four tiles (General's slot order).
        patch = np.tile(sea, (2, 2, 1))
        for k in range(16):
            r, c = divmod(k, 4)
            tile = patch[r * 8:r * 8 + 8, c * 8:c * 8 + 8].copy()
            gy, gx = GLINTS[k]
            tile[gy, gx] = rgba("ae_h")
            tiles.append(tile)
        # 16-21: shallows
        for k in range(6):
            tile = shal[(k // 2 % 2) * 8:(k // 2 % 2) * 8 + 8, (k % 2) * 8:(k % 2) * 8 + 8].copy()
            if k in SHALLOW_MARKS:
                y, x = SHALLOW_MARKS[k]
                tile[y, x] = rgba("sd_l")
            tiles.append(tile)
        tiles += quads(sea)       # 22-23 open sea
        tiles += quads(chan)      # 24-25 channel
        tiles += quads(rough)     # 26-27 currents
        tiles += quads(deep)      # 28-29 deep water
        frames.append(tiles)
    key = nudge_unique(frames[0])
    return [join_tiles(key, 2)] + [join_tiles(f, 2) for f in frames]


# --------------------------------------------------------------------------
# Surf on sand: General's key gives the sand shape; we wash foam over it.
# --------------------------------------------------------------------------

def _edge_distance(mask):
    """Chebyshev distance (in px) from each sand pixel to the nearest
    transparent (water) pixel inside the same 8x8 tile."""
    h, w = mask.shape
    dist = np.full((h, w), 99)
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            m = mask[ty:ty + 8, tx:tx + 8]
            water = np.argwhere(~m)
            for y in range(8):
                for x in range(8):
                    if not m[y, x] or not len(water):
                        continue
                    d = np.abs(water - (y, x)).max(1).min()
                    dist[ty + y, tx + x] = d
    return dist


WASH = [1, 2, 3, 4, 3, 2, 1]  # surf reach per frame (7 frames)


def sand_water_edge_frames():
    base_key = load_rgba(BASE / "anim/sand_water_edge/key.png")
    mask = base_key[..., 3] > 0
    dist = _edge_distance(mask)
    h, w = mask.shape
    sand = np.tile(SAND, (h // 16 + 1, w // 16 + 1, 1))[:h, :w]
    frames = []
    for reach in WASH:
        f = np.zeros_like(base_key)
        f[mask] = sand[mask]
        if reach:
            wet = mask & (dist <= reach + 1)
            f[wet] = rgba("sd_d")
            sea = mask & (dist < reach)
            f[sea] = rgba("ae_t")
            front = mask & (dist == reach)
            f[front] = rgba("foam")
            glint = sea & ((np.add.outer(np.arange(h), np.arange(w)) % 5) == 0)
            f[glint] = rgba("ae_h")
        frames.append(f)
    key = nudge_unique(split_tiles(frames[0]))
    return [join_tiles(key, w // 8)] + frames


def land_water_edge_frames():
    """Rocky shore surf (only Hoenn secondaries use these slots)."""
    base_key = load_rgba(BASE / "anim/land_water_edge/key.png")
    mask = base_key[..., 3] > 0
    h, w = mask.shape
    from aethos_lib import solid
    rock = np.zeros((h, w, 4), np.uint8)
    yy, xx = np.mgrid[0:h, 0:w]
    rock[:] = rgba("mb_m")
    rock[(yy % 4) == 3] = rgba("mb_d")
    rock[((yy % 4) == 0) & ((xx % 6) == 1)] = rgba("mb_l")
    frames = []
    for t in range(4):
        f = np.zeros_like(base_key)
        f[mask] = rock[mask]
        edge = mask & ((yy + xx + t * 2) % 7 == 0) & (yy % 4 != 3)
        f[edge] = rgba("foam")
        frames.append(f)
    key = nudge_unique(split_tiles(frames[0]))
    return [join_tiles(key, w // 8)] + frames


WF_LEG = dict(n="ae_n", l="ae_l", h="ae_h", m="ae_m", f="foam")
# A 16-row column of falling water; frames scroll it down 4 px at a time.
WF_BODY = art("""
    nlnnhnln
    nlnnlnhn
    nhnnlnln
    nlnhlnln
    nlnnlnln
    hlnnlnln
    nlnnhnln
    nlnnlnlh
    nlhnlnln
    nlnnlnhn
    nlnhlnln
    hlnnlnln
    nlnnlhln
    nlnnlnln
    nhnnlnln
    nlnnlnhn
""", WF_LEG)


def waterfall_frames():
    """Six 8x8 tiles, General's vertical pairs (each mirrored by a flip for
    the right half of its metatile):
      0-1  falling water, top and bottom of a metatile (0x0B3 and kin)
      2-3  the lip where calm water tips over, and the fall below it
      4-5  the fall plunging into foam, and the foam spreading into the pool
    """
    frames = []
    for t in range(4):
        b = np.roll(WF_BODY, t * 4, axis=0)
        body_top, body_bot = b[0:8].copy(), b[8:16].copy()
        lip = b[0:8].copy()
        lip[0:2] = rgba("ae_m")
        lip[2] = rgba("ae_l")
        lip[3] = rgba("ae_h")
        lip[3, (np.arange(8) + t) % 3 == 0] = rgba("foam")
        under_lip = b[4:12].copy()
        plunge = b[0:8].copy()
        plunge[5:8] = rgba("foam")
        plunge[4, (np.arange(8) + t) % 2 == 0] = rgba("foam")
        pool = np.zeros((8, 8, 4), np.uint8)
        pool[:] = rgba("ae_m")
        pool[0:2] = rgba("foam")
        pool[2, (np.arange(8) + t) % 2 == 0] = rgba("foam")
        pool[3, (np.arange(8) + t * 3) % 3 == 0] = rgba("ae_h")
        pool[5, (np.arange(8) + t * 3) % 4 == 1] = rgba("ae_l")
        frames.append([body_top, body_bot, lip, under_lip, plunge, pool])
    key = nudge_unique(frames[0])
    return [join_tiles(key, 1)] + [join_tiles(f, 1) for f in frames]


def sea_texture(kind="sea", t=0):
    """Static 16x16 water texture matching anim frame t."""
    if kind == "sea":
        return sea_frame(SEA_STRIP, t)
    if kind == "rough":
        return sea_frame(ROUGH_STRIP, t)
    if kind == "deep":
        return sea_frame(DEEP_STRIP, t)
    if kind == "shallow":
        return shallow_frame(t)
    raise KeyError(kind)
