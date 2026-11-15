"""The Temple of Artemis at Arkadia: gTileset_TempleArtemis, the goddess's night garden,
where Hierophant Kallisto keeps the Hunt for the Hind (SYSTEMS.md §12: stealth;
design/phase3/SCRIPT.md beat 44 and Part 5).

The temple has no roof. It is a walled garden under the same moonlit night at any
hour, three gardens climbing a hill, each walled in clipped laurel and entered by a
hunters' arch. The paths run between myrtle bushes, stone stelae and cypress trunks,
which block a hound's sight. Pools of moonlight lie on the clearings, drawn as their
own clearly brighter ground. At the top a grey rock rises out of the brightest
moonlight, with a stair cut into its face; Kallisto sits on it.

The set is drawn in the temple's own night palette and placed on an indoor map, so
the clock's tint never touches it (TILES_temple_artemis.md says why).

How the trial's state shows in tiles:

  Stair hedge  The laurel hedge across the foot of the rock's stair: `hedge_l`/`_r`
               block; `lowered_l`/`_r` (= the hedge + 1) is the same hedge clipped
               down to its roots, walkable. It lowers at the hind's third touch.
  Anthia's gate A woven laurel gate in her grove's hedge: `gate_top`/`gate` block;
               `gate_top_open`/`gate_open` (= the closed piece + 1) stand open.

Light: the moon stands high in the south-west, behind the player's shoulder, so tops
and south faces catch a cool silver light; shadows fall north-east.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_ground as AG  # noqa: E402
import agros_lib as A  # noqa: E402
from agros_lib import Layer, Struct  # noqa: E402,F401
from eleusa_lib import put  # noqa: E402

# --------------------------------------------------------------------------
# Colors and palette groups (every value a multiple of 8)
# --------------------------------------------------------------------------

NEW = {
    "nk": (8, 16, 24),
    # the night lawn
    "ng0": (24, 40, 48), "ng1": (32, 56, 64), "ng2": (48, 72, 72), "ng3": (64, 96, 88),
    "ng4": (88, 120, 112),
    # gravel walks
    "np0": (56, 64, 80), "np1": (88, 96, 120), "np2": (120, 128, 152), "np3": (160, 168, 192),
    # asphodel in the lawn
    "nf0": (144, 152, 184), "nf1": (216, 224, 240), "nf2": (216, 184, 96),
    # moonlit ground: the lawn silvered
    "nm0": (72, 104, 120), "nm1": (104, 144, 152), "nm2": (136, 176, 184), "nm3": (176, 208, 216),
    "nm4": (216, 232, 240),
    # clipped laurel
    "nl0": (8, 24, 24), "nl1": (16, 40, 32), "nl2": (32, 64, 48), "nl3": (48, 88, 64),
    "nl4": (80, 120, 88), "nl5": (136, 176, 152),
    # myrtle and cypress, darker and bluer than laurel, silver where the moon touches
    "ny0": (16, 40, 48), "ny1": (40, 72, 80), "ny2": (72, 112, 112), "ny3": (128, 168, 160),
    # myrtle's white flowers
    "nw0": (160, 168, 200), "nw1": (232, 232, 248),
    # trunks
    "nt0": (40, 32, 40), "nt1": (80, 64, 64),
    # cut marble: stelae, arches, the altar, the statue, the porch
    "ns0": (40, 48, 64), "ns1": (64, 72, 96), "ns2": (96, 104, 128), "ns3": (136, 144, 168),
    "ns4": (184, 192, 208), "ns5": (224, 232, 240), "nsw": (248, 248, 248),
    "nau0": (136, 104, 48), "nau1": (200, 160, 72),
    # the hill's own rock: warmer greys than the marble
    "nr0": (32, 32, 40), "nr1": (56, 56, 64), "nr2": (88, 88, 96), "nr3": (120, 120, 128),
    "nr4": (160, 160, 168), "nr5": (208, 208, 216),
    # wood, bronze, lamp flame and saffron cloth (the kennels, lamps, the bench's rug)
    "nb0": (48, 32, 32), "nb1": (88, 56, 48), "nb2": (136, 96, 64), "nb3": (184, 136, 88),
    "nz1": (152, 104, 48), "nz2": (208, 160, 80),
    "ne0": (208, 88, 40), "ne1": (240, 168, 64), "ne2": (248, 232, 152),
    "nc0": (200, 120, 40),
    # still water
    "nq0": (8, 16, 40), "nq1": (16, 32, 64), "nq2": (32, 56, 96), "nq3": (64, 96, 136),
    "nq4": (152, 184, 216),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME[_c] = _n
C = A.C

GROUPS = {
    # lawn, walks, flowers in the lawn, the lawn in a hedge's or bush's shadow
    "ground": ["nk", "ng0", "ng1", "ng2", "ng3", "ng4", "np0", "np1", "np2", "np3",
               "nf0", "nf1", "nf2"],
    # moonlit ground and where it fades into the lawn
    "moon": ["nk", "ng0", "ng1", "ng2", "ng3", "ng4", "nm0", "nm1", "nm2", "nm3", "nm4", "nf1"],
    # laurel hedges, myrtle, cypress
    "leaf": ["nk", "nl0", "nl1", "nl2", "nl3", "nl4", "nl5", "ny0", "ny1", "ny2", "ny3", "nw0",
             "nw1", "nt0", "nt1"],
    # marble and its garlands, gilding
    "stone": ["nk", "ns0", "ns1", "ns2", "ns3", "ns4", "ns5", "nsw", "nl2", "nl3", "nl4",
              "nau0", "nau1"],
    # the rock and the lawn at its foot
    "rock": ["nk", "nr0", "nr1", "nr2", "nr3", "nr4", "nr5", "ng0", "ng1", "ng2", "ng3",
             "nl2", "nl3", "nm3", "nm4"],
    # wood, bronze, flame, saffron
    "warm": ["nk", "nb0", "nb1", "nb2", "nb3", "nz1", "nz2", "ne0", "ne1", "ne2", "nc0",
             "ns1", "ns2"],
    # still water and its stone lip
    "water": ["nk", "nq0", "nq1", "nq2", "nq3", "nq4", "nm4", "nr1", "nr2", "nr3", "nr4"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

SEC = "temple_artemis"


def struct(key, title, w, h, walk=None, notes="", names=None, behaviors=None):
    s = Struct(key, title, w, h, SEC, walk=walk, notes=notes, names=names)
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch == "S":
                s.behaviors[(cx, cy)] = "MB_SOUTH_ARROW_WARP"
    s.behaviors.update(behaviors or {})
    return s


def cells(keys, w):
    """names for a run of keys laid out w to a row."""
    return {k: (i % w, i // w) for i, k in enumerate(keys)}


def h32(*v):
    """A small deterministic hash."""
    x = 2166136261
    for n in v:
        x = ((x ^ (int(n) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    x ^= x >> 13
    x = (x * 0x5BD1E995) & 0xFFFFFFFF
    x ^= x >> 15
    return x


# --------------------------------------------------------------------------
# Textures: 16 x 16 and periodic, so pieces cut from them join seamlessly
# --------------------------------------------------------------------------

def lawn_texture(seed=0, colors=("ng0", "ng1", "ng2", "ng3", "ng4"), tips=5):
    """Clipped night lawn: short blades in soft tufts on a dark ground, a few tips catching
    the moon. Low contrast, so the things standing on it read."""
    c0, c1, c2, c3, c4 = colors
    T = Layer(16, 16)
    T.rect(0, 0, 16, 16, c1)
    # tufts on a jittered 4 x 4 grid, wrapping at the edges: a blade pair, a shadow under
    for gy in range(4):
        for gx in range(4):
            h = h32(gx, gy, seed)
            x = gx * 4 + h % 3
            y = gy * 4 + (h >> 3) % 3
            T.px(x % 16, y % 16, c2)
            T.px((x + 1) % 16, (y + 1) % 16, c2)
            if (h >> 6) % 3 == 0:
                T.px(x % 16, (y - 1) % 16, c3)
            if (h >> 11) % tips == 0:
                T.px((x + 1) % 16, y % 16, c4 if (h >> 13) % 3 == 0 else c3)
            if (h >> 9) % 2:
                T.px((x + 2) % 16, (y + 2) % 16, c0)
    return T


def moon_texture():
    """The same lawn, silvered by moonlight: unmistakably brighter, and smooth."""
    return lawn_texture(seed=7, colors=("nm0", "nm1", "nm2", "nm3", "nm4"), tips=4)


def gravel_texture():
    """A walk of crushed pale stone, raked."""
    T = Layer(16, 16)
    T.rect(0, 0, 16, 16, "np1")
    for y in range(16):
        for x in range(16):
            h = h32(x, y, 3) % 23
            if h == 0:
                T.px(x, y, "np3")
                T.px((x + 1) % 16, y, "np2")
            elif h in (5, 9):
                T.px(x, y, "np2")
            elif h == 14:
                T.px(x, y, "np0")
    return T


LAUREL_LEAF = [".33.", "3443", "2332", ".11."]


def laurel_top_texture():
    """The flat clipped top of a laurel hedge: a carpet of leaves, each lit on its upper
    edge, the gaps between them dark, here and there a leaf the moon catches."""
    T = Layer(16, 16)
    T.rect(0, 0, 16, 16, "nl1")
    for gy in range(4):
        for gx in range(4):
            h = h32(gx, gy, 21)
            x = gx * 4 + (2 if gy % 2 else 0) + h % 2 - 1
            y = gy * 4 + (h >> 2) % 2 - 1
            for j, row in enumerate(LAUREL_LEAF):
                for i, ch in enumerate(row):
                    if ch == ".":
                        continue
                    c = {"1": "nl1", "2": "nl2", "3": "nl3", "4": "nl4"}[ch]
                    if ch == "4" and (h >> 4) % 5 == 0:
                        c = "nl5"
                    T.px((x + i) % 16, (y + j) % 16, c)
    return T


def laurel_face_texture():
    """The clipped south face of a hedge: leaves hanging in its own shadow."""
    T = Layer(16, 16)
    T.rect(0, 0, 16, 16, "nl0")
    for gy in range(4):
        for gx in range(4):
            h = h32(gx, gy, 31)
            x = gx * 4 + (2 if gy % 2 else 0) + h % 2
            y = gy * 4 + (h >> 2) % 2
            for j, row in enumerate([".22.", "2332", ".11."]):
                for i, ch in enumerate(row):
                    if ch == ".":
                        continue
                    T.px((x + i) % 16, (y + j) % 16, {"1": "nl1", "2": "nl2", "3": "nl3"}[ch])
    return T


def myrtle_texture():
    T = Layer(16, 16)
    T.rect(0, 0, 16, 16, "ny1")
    for gy in range(5):
        for gx in range(5):
            h = h32(gx, gy, 41)
            x = gx * 3 + h % 2
            y = gy * 3 + (h >> 1) % 2
            T.px(x % 16, y % 16, "ny2")
            T.px((x + 1) % 16, (y + 1) % 16, "ny0")
    return T


def rock_texture():
    """The hill's grey rock: blocky, cracked, cold."""
    T = Layer(16, 16)
    T.rect(0, 0, 16, 16, "nr2")
    for y in range(16):
        for x in range(16):
            h = h32(x // 2, y // 2, 51) % 9
            if h == 0:
                T.px(x, y, "nr3")
            elif h == 1:
                T.px(x, y, "nr1")
    for x in range(16):
        if h32(x, 61) % 3:
            T.px(x, 7, "nr1")
    for y in range(8):
        T.px(5, y, "nr1")
    for y in range(8, 16):
        T.px(12, y, "nr1")
    return T


_TEX = {}


def tex(name):
    if name not in _TEX:
        _TEX[name] = {"lawn": lambda: lawn_texture(), "lawn_b": lambda: lawn_texture(seed=5),
                      "moon": moon_texture, "gravel": gravel_texture,
                      "laurel": laurel_top_texture, "face": laurel_face_texture,
                      "myrtle": myrtle_texture, "rock": rock_texture}[name]()
    return _TEX[name]


def paint_tex(L, t, ox, oy, mask=None, dx=0, dy=0):
    """Fill a 16 x 16 cell with a texture, phase-locked to the grid (plus a shift)."""
    T = tex(t) if isinstance(t, str) else t
    for y in range(16):
        for x in range(16):
            if mask is None or mask[y, x]:
                L.a[oy + y, ox + x] = T.a[(y + dy) % 16, (x + dx) % 16]


def lawn(L, ox, oy, v=0):
    paint_tex(L, "lawn_b" if v % 2 else "lawn", ox, oy)


# --------------------------------------------------------------------------
# Floors: the lawn, flowers, shadows, the porch's paving, the mat
# --------------------------------------------------------------------------

ASPHODEL = ["..W..", ".WYW.", "..W..", "..g.."]


def floor_pieces():
    keys = ["lawn", "lawn_b", "lawn_flowers", "lawn_flowers_b", "lawn_shade", "lawn_shade_b",
            "void", "lawn_tuft",
            "pave", "pave_b", "pave_c", "pave_moon", "mat_l", "mat_r", "pave_shade", "pave_worn"]
    s = struct("floor", "Floors: the night lawn, the porch's paving, the door", 8, 2,
               walk=["......X.", "....SS.."],
               names=cells(keys, 8),
               notes="`lawn` is the clipped night lawn (`_b` a second grain; `_tuft` a darker "
                     "tussock; `_flowers` white asphodel). `lawn_shade` is the lawn under a "
                     "hedge's face, in its shadow: put it on the row south of every hedge face. "
                     "`pave` is the porch's marble paving (`_b`, `_c`, `_worn` to break a run; "
                     "`_moon` a slab in a pool of moonlight; `_shade` under a hedge). The "
                     "doormat (`mat_l`, `mat_r`) is MB_SOUTH_ARROW_WARP: a warp on each. `void` "
                     "blocks: the border.")
    L = s.B
    for i, k in enumerate(keys):
        ox, oy = (i % 8) * 16, (i // 8) * 16
        if k.startswith("lawn"):
            lawn(L, ox, oy, 1 if k.endswith("_b") else 0)
            if k.startswith("lawn_flowers"):
                spots = [(2, 3), (10, 9)] if k == "lawn_flowers" else [(8, 2), (3, 10), (11, 12)]
                for fx, fy in spots:
                    put(L, ox + fx, oy + fy, ASPHODEL, {"W": "nf1", "Y": "nf2", "g": "ng3"})
                    L.px(ox + fx + 1, oy + fy + 1, "nf0")
            if k.startswith("lawn_shade"):
                # the hedge's shadow, falling north-east of the moon: darkest at the top
                for y in range(16):
                    for x in range(16):
                        c = L.get(ox + x, oy + y)
                        if y < 5 or (y < 9 and (x + y) % 2 == 0):
                            L.px(ox + x, oy + y, {"ng3": "ng1", "ng2": "ng0", "ng4": "ng2"}.get(c, "ng0"))
                        elif y < 11 and c in ("ng3", "ng4"):
                            L.px(ox + x, oy + y, "ng2")
            if k == "lawn_tuft":
                put(L, ox + 4, oy + 5, [".3.3.3.", "2323232", "1212121", ".1.1.1."],
                    {"3": "ng3", "2": "ng2", "1": "ng0"})
        elif k == "void":
            L.rect(ox, oy, 16, 16, "nk")
        elif k.startswith("pave") or k.startswith("mat"):
            pave(L, ox, oy, {"pave": 0, "pave_b": 1, "pave_c": 2}.get(k, 0))
            if k == "pave_moon":
                for y in range(16):
                    for x in range(16):
                        c = L.get(ox + x, oy + y)
                        L.px(ox + x, oy + y, {"ns1": "ns3", "ns2": "ns4", "ns3": "ns5",
                                               "ns0": "ns2"}.get(c, c))
            if k == "pave_shade":
                for y in range(7):
                    for x in range(16):
                        c = L.get(ox + x, oy + y)
                        if y < 4 or (x + y) % 2 == 0:
                            L.px(ox + x, oy + y, {"ns3": "ns1", "ns2": "ns1", "ns1": "ns0"}.get(c, c))
            if k == "pave_worn":
                for y in range(16):
                    for x in range(5, 11):
                        if (x * 3 + y) % 4 == 0 and L.get(ox + x, oy + y) == "ns2":
                            L.px(ox + x, oy + y, "ns3")
            if k.startswith("mat"):
                mat(L, ox, oy, k == "mat_r")
    return s


def pave(L, ox, oy, v=0):
    """Marble slabs, two courses to a cell, joints staggered."""
    for y in range(16):
        course = y // 8
        off = (0, 5, 3)[(v + course) % 3]
        for x in range(16):
            xx = (x + off) % 8
            yy = y % 8
            if yy == 7 or xx == 7:
                c = "ns1"
            elif yy == 0 or xx == 0:
                c = "ns3"
            elif h32(x, y, v, 71) % 29 == 0:
                c = "ns1"
            else:
                c = "ns2"
            L.px(ox + x, oy + y, c)


def mat(L, ox, oy, right):
    """The threshold of the garden's gate: a worn stone sill with a deer-hide mat."""
    for y in range(3, 16):
        for x in range(16):
            xx = 15 - x if right else x
            if y in (3, 15):
                c = "ns0"
            elif xx == 0 and y < 15:
                c = "ns0"
            elif y % 4 == 1:
                c = "ns3"
            else:
                c = "ns2" if (x + y) % 5 else "ns3"
            L.px(ox + x, oy + y, c)


# --------------------------------------------------------------------------
# Soft ground: moonlight and the gravel walks, all 47 shapes each
# --------------------------------------------------------------------------

def paint_moon(L, ox, oy, key):
    """A pool of moonlight on the lawn: the silvered lawn, a pale rim, a dithered fall."""
    vis, _ = AG.visible(key, margin=1.0, radius=3.5, amp=1.2, seed=0.9, jag=0.6)
    paint_tex(L, "lawn", ox, oy)
    paint_tex(L, "moon", ox, oy, vis)
    for y, x in np.argwhere(AG.ring(vis)):
        L.px(ox + x, oy + y, "nm1" if (x + y) % 2 else "nm2")
    # the light spills a pixel or two into the lawn, dithered
    for y, x in np.argwhere(AG.halo(vis)):
        if (x + y) % 2 == 0:
            L.px(ox + x, oy + y, "nm0")
    halo2 = AG.halo(AG.halo(vis) | vis)
    for y, x in np.argwhere(halo2):
        if (x * 3 + y) % 4 == 0:
            L.px(ox + x, oy + y, "ng3")


def paint_gravel(L, ox, oy, key):
    """A raked gravel walk: lawn margins scalloped, a dark lip where the gravel is cut."""
    vis, _ = AG.visible(key, margin=2.5, radius=2.0, amp=1.0, seed=2.9)
    paint_tex(L, "lawn", ox, oy)
    paint_tex(L, "gravel", ox, oy, vis)
    for y, x in np.argwhere(AG.ring(vis)):
        below = y + 1 >= 16 or not vis[y + 1, x]
        L.px(ox + x, oy + y, "np0" if below else ("np2" if (x + y) % 3 == 0 else "np1"))
    for y, x in np.argwhere(AG.halo(vis)):
        if (x + 2 * y) % 3:
            L.px(ox + x, oy + y, "ng0")


def soft_sets():
    keys = AG.blob_keys()
    moon = AG.shape_set("moon", "Moonlight: pools of pale ground, every shape", keys, paint_moon,
                        ".", SEC,
                        "The lawn where the moon lies on it, clearly brighter: a hound that "
                        "patrols it sees 6 tiles, not 3. Every one of the 47 blob shapes, named "
                        "by shape key (`eleusa_lib.blob_key`); `1|11111111` is the middle of a "
                        "pool. Walkable.")
    path = AG.shape_set("walk", "Gravel walks, every shape", keys, paint_gravel, ".", SEC,
                        "Raked gravel walks through the lawn, named by shape key like the "
                        "moonlight. Walkable.")
    return [moon, path]


# --------------------------------------------------------------------------
# The clipped laurel hedge: every shape of a hedge mass
# --------------------------------------------------------------------------
# A hedge cell whose south neighbor is not hedge shows the hedge's clipped south face;
# every other hedge cell shows its flat top. Edges to open ground get a dark rim (and a
# moonlit lip along a top's south edge, where the top turns down into the face).

def paint_hedge(L, ox, oy, key):
    _, nb = key.split("|")
    n, ne, e, se, s, sw, w, nw = (c == "1" for c in nb)
    face = not s
    paint_tex(L, "laurel", ox, oy)
    if face:
        # the top's front lip on rows 0-3, then the hanging face, then the foot
        lip = 3 if n else 6
        if not n:
            for x in range(16):
                L.px(ox + x, oy + 0, "nk")
                L.px(ox + x, oy + 1, "nl2")
        for y in range(16):
            for x in range(16):
                if y == lip:
                    L.px(ox + x, oy + y, "nl5" if (x + ox) % 3 else "nl4")
                elif y == lip + 1:
                    L.px(ox + x, oy + y, "nl4" if (x + ox) % 2 else "nl3")
                elif y > lip + 1:
                    t = tex("face").a[y % 16, (x + ox) % 16]
                    L.a[oy + y, ox + x] = t
                    if y >= 14:
                        L.px(ox + x, oy + y, "nl0" if y == 15 else ("nl1" if (x + y) % 2 else "nl0"))
        # ends of a face: the hedge's corner turns away, rimmed
        for side, out in (("w", not w), ("e", not e)):
            if not out:
                continue
            for y in range(16):
                xs = (0, 1) if side == "w" else (15, 14)
                L.px(ox + xs[0], oy + y, "nk")
                if y > lip + 1:
                    L.px(ox + xs[1], oy + y, "nl0" if side == "e" else "nl2")
                elif y > 0:
                    L.px(ox + xs[1], oy + y, "nl4" if side == "w" else "nl2")
    else:
        if not n:
            for x in range(16):
                L.px(ox + x, oy + 0, "nk")
                L.px(ox + x, oy + 1, "nl1")
                L.px(ox + x, oy + 2, "nl4" if (x + ox) % 4 else "nl5")
        if not w:
            for y in range(16):
                L.px(ox + 0, oy + y, "nk")
                L.px(ox + 1, oy + y, "nl4" if (y + oy) % 3 else "nl5")
        if not e:
            for y in range(16):
                L.px(ox + 15, oy + y, "nk")
                L.px(ox + 14, oy + y, "nl1")
        # inner corners: open ground only touches diagonally
        if n and w and not nw:
            put(L, ox, oy, ["kk", "k4"], {"k": "nk", "4": "nl4"})
        if n and e and not ne:
            put(L, ox + 14, oy, ["kk", "1k"], {"k": "nk", "1": "nl1"})
        if s and w and not sw:
            # a face begins south-west of this top: its lip shows in the corner
            put(L, ox, oy + 13, ["k5", "k4", "kk"], {"k": "nk", "5": "nl5", "4": "nl4"})
        if s and e and not se:
            put(L, ox + 14, oy + 13, ["5k", "4k", "kk"], {"k": "nk", "5": "nl5", "4": "nl4"})
        if not n and not w:
            L.px(ox + 1, oy + 1, "nk")
        if not n and not e:
            L.px(ox + 14, oy + 1, "nk")


def hedge_set():
    keys = AG.blob_keys()
    return AG.shape_set("hedge", "Clipped laurel hedges, every shape", keys, paint_hedge, "X", SEC,
                        "The garden's walls: clipped laurel, a flat moonlit top and a dark south "
                        "face. Named by shape key of the hedge mass (`eleusa_lib.blob_key`). A "
                        "cell whose south neighbor isn't hedge draws the face; give hedge walls "
                        "two rows (top, face) so the face sits under a top. Blocks.")


# --------------------------------------------------------------------------
# The hunters' arches
# --------------------------------------------------------------------------
# 4 x 3, set into a two-row hedge wall: the crown over the lawn behind the wall (drawn
# over the player), the posts' capitals and the lintel in the wall's top row, the posts
# and the opening in its face row.

EMBLEMS = {
    # the lintel's carved device, 20 x 8 across its two cells
    "antlers": [
        "..K.K..........K.K..",
        "..KK.K........K.KK..",
        "...KK.KK....KK.KK...",
        ".....KKKK..KKKK.....",
        ".......KKKKKK.......",
        "........KWWK........",
        ".........KK.........",
        "....................",
    ],
    "bow": [
        "..KKK...............",
        ".K...KKK............",
        "K.......KKKKK.....K.",
        "WWWWWWWWWWWWWWWWWWWK",
        "K.......KKKKK.....K.",
        ".K...KKK............",
        "..KKK...............",
        "....................",
    ],
    "moon": [
        "......KKKK..........",
        "....KK..............",
        "...K.......W.....W..",
        "...K......WWW.......",
        "...K.......W........",
        "....KK...........W..",
        "......KKKK..........",
        "....................",
    ],
}

CROWNS = {
    # what rises over the lintel, 32 x 14 across the two middle crown cells (bottom-aligned)
    "antlers": [
        "......4...4............4...4....",
        ".....4.4.4..............4.4.4...",
        "......44.4...4......4...4.44....",
        "........444.4........4.444......",
        ".........44444......44444.......",
        "...........4444....4444.........",
        ".............44444444...........",
        "..............433334............",
        "..............322223............",
        "..............322223............",
        ".............33222233...........",
        "............3322222233..........",
        "...........333333333333.........",
        "..........22222222222222........",
    ],
    "bow": [
        "...............4................",
        "..............434...............",
        ".............4.3.4..............",
        "...........44..3..44............",
        "........444....3....444.........",
        "......44.......3.......44.......",
        ".....4.........3.........4......",
        "....4..........3..........4.....",
        "....4..........3..........4.....",
        "...34444444444444444444444443...",
        "..............2222..............",
        ".............322223.............",
        "...........3333333333...........",
        "..........22222222222222........",
    ],
    "moon": [
        "...............5555.............",
        ".............55443..............",
        "............5443................",
        "...........5443.........4.......",
        "...........543.........444......",
        "...........543..........4.......",
        "...........5443.................",
        "............5443................",
        ".............55443..............",
        "...............5555.............",
        "..............322223............",
        ".............33222233...........",
        "...........333333333333.........",
        "..........22222222222222........",
    ],
}


def threshold(L, ox, oy, lit=False):
    """The stone sill through an arch, worn smooth."""
    for y in range(16):
        for x in range(16):
            if y % 8 == 7:
                c = "ns1"
            elif x % 16 == 0 and y < 8:
                c = "ns1"
            elif (x + 4) % 16 == 0 and y >= 8:
                c = "ns1"
            else:
                c = "ns3" if lit else "ns2"
                if h32(x, y, 81) % 17 == 0:
                    c = "ns3" if not lit else "ns4"
            L.px(ox + x, oy + y, c)


def post(L, ox, oy, side, part, garland=True):
    """A marble post 12 px wide, centered in its cell; part 'cap' or 'shaft'."""
    x0 = ox + 2
    if part == "cap":
        # capital: an abacus slab over a necking, seen from a little above
        for y in range(16):
            for x in range(12):
                if y < 2:
                    c = "nk" if y == 0 else "ns5"
                elif y < 6:
                    c = "ns4" if x < 10 else "ns2"
                    if x == 0:
                        c = "ns5"
                elif y < 8:
                    c = "ns2" if x else "ns3"
                else:
                    c = "ns3" if x < 4 else ("ns2" if x < 9 else "ns1")
                if x in (0, 11) and y >= 2:
                    c = "nk" if x == 11 else c
                L.px(x0 + x, oy + y, c)
        L.hline(x0, x0 + 11, oy + 7, "ns1")
    else:
        for y in range(16):
            for x in range(12):
                c = "ns3" if x < 4 else ("ns2" if x < 9 else "ns1")
                if x in (3, 6, 9):
                    c = "ns1" if x != 3 else "ns2"     # flutes
                if x == 11:
                    c = "nk"
                if x == 0:
                    c = "ns4"
                L.px(x0 + x, oy + y, c)
        # base
        L.rect(x0 - 1, oy + 13, 14, 3, "ns2")
        L.hline(x0 - 1, x0 + 12, oy + 13, "ns4")
        L.hline(x0 - 1, x0 + 12, oy + 15, "ns0")
        if garland:
            # a laurel garland twisted round the shaft
            for i, y in enumerate(range(1, 12, 2)):
                gx = x0 + (i * 4) % 12
                L.px(gx, oy + y, "nl3")
                L.px(gx + 1, oy + y, "nl4")
                L.px(gx + 1, oy + y + 1, "nl2")


def arch(variant):
    title = {"antlers": "The first hunters' arch: antlers", "bow": "The second hunters' arch: the bow",
             "moon": "The third hunters' arch: the crescent moon"}[variant]
    key = f"arch_{variant}"
    names = {"crown_l": (0, 0), "crown_ml": (1, 0), "crown_mr": (2, 0), "crown_r": (3, 0),
             "cap_l": (0, 1), "lintel_l": (1, 1), "lintel_r": (2, 1), "cap_r": (3, 1),
             "post_l": (0, 2), "open_l": (1, 2), "open_r": (2, 2), "post_r": (3, 2)}
    s = struct(key, title, 4, 3, walk=["TTTT", "XTTX", "X..X"], names=names,
               notes="Set it into a two-row hedge wall: row 0 over the lawn north of the wall "
                     "(the crown, drawn over the player), row 1 in the wall's top row (the "
                     "capitals and the lintel, walked under), row 2 in its face row (the posts "
                     "and the opening). The lawn under the crown is plain `lawn`.")
    B, M, T = s.B, s.M, s.T
    for cx in range(4):
        lawn(B, cx * 16, 0)
    # the sill through the opening, both rows
    for cx in (1, 2):
        threshold(B, cx * 16, 16, lit=False)
        threshold(B, cx * 16, 32, lit=True)
    # hedge top behind the capitals, hedge face behind the shafts
    for cx in (0, 3):
        paint_tex(B, "laurel", cx * 16, 16)
        paint_tex(B, "face", cx * 16, 32)
        for x in range(16):
            B.px(cx * 16 + x, 32 + 15, "nl0")
    post(M, 0, 16, "l", "cap")
    post(M, 48, 16, "r", "cap")
    post(M, 0, 32, "l", "shaft")
    post(M, 48, 32, "r", "shaft")
    # the lintel: a marble beam across both middle cells, drawn over the player
    for y in range(16):
        for x in range(16, 48):
            if y < 2:
                c = "nk" if y == 0 else "ns5"
            elif y < 4:
                c = "ns4"
            elif y < 13:
                c = "ns3"
            elif y < 15:
                c = "ns2"
            else:
                c = "nk"
            T.px(x, 16 + y, c)
    put(T, 22, 20, EMBLEMS[variant], {"K": "ns1", "W": "nau1"})
    # a laurel swag hangs under the lintel's ends
    for x in range(16, 48):
        dy = int(2 * math.sin((x - 16) / 31 * math.pi))
        T.px(x, 16 + 13 + dy, "nl3")
        if (x % 3) == 0:
            T.px(x, 16 + 14 + dy, "nl4")
            T.px(x, 16 + 12 + dy, "nl2")
    # the opening's shadow under the lintel, on the sill
    for x in range(18, 46):
        B.px(x, 32 + 0, "ns1")
        if x % 2:
            B.px(x, 32 + 1, "ns1")
    # the crown: the device rising over the lintel, and two finials on the capitals
    put(T, 16, 2, CROWNS[variant], {"5": "nsw", "4": "ns4", "3": "ns3", "2": "ns2"})
    for fx in (6, 54):
        put(T, fx - 3, 6, [".44.", "4553", "4553", ".33.", "2222", ".22."],
            {"5": "nsw", "4": "ns4", "3": "ns3", "2": "ns2"})
    return s


# --------------------------------------------------------------------------
# Myrtle, cypress and stelae: what blocks a hound's eye
# --------------------------------------------------------------------------

def blob_mask(w, h, cx, cy, rx, ry, seed=0, wob=1.2):
    """An irregular round mask (a bush's outline), in pixels."""
    m = np.zeros((h, w), bool)
    for y in range(h):
        for x in range(w):
            a = math.atan2(y - cy, x - cx)
            r = 1 + 0.12 * math.sin(5 * a + seed) + 0.08 * math.sin(9 * a + 2 * seed)
            if ((x - cx) / (rx * r)) ** 2 + ((y - cy) / (ry * r)) ** 2 <= 1:
                m[y, x] = True
    return m


def paint_bush(L, ox, oy, mask, flowers=0, seed=0):
    """Myrtle: a dense round shrub of leaf clumps, each lit on its south-west side by the
    moon, the whole lit silver along its south-west rim; white stars of flowers."""
    h, w = mask.shape
    ys, xs = np.nonzero(mask)
    cy, cx = ys.mean(), xs.mean()
    # the body in shade, then clumps of leaves (5 px discs) laid over it, lit from the SW
    for y, x in zip(ys, xs):
        L.px(ox + x, oy + y, "ny0")
    step = 4
    for gy in range(-1, h // step + 1):
        for gx in range(-1, w // step + 1):
            hh = h32(gx, gy, seed, 77)
            px = gx * step + (2 if gy % 2 else 0) + hh % 2
            py = gy * step + (hh >> 2) % 2
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dx * dx + dy * dy > 5:
                        continue
                    x, y = px + dx, py + dy
                    if not (0 <= x < w and 0 <= y < h and mask[y, x]):
                        continue
                    lit = dx - dy < -1          # the clump's lower-left
                    dark = dx - dy > 1
                    c = "ny2" if lit else ("ny0" if dark else "ny1")
                    L.px(ox + x, oy + y, c)
    # the whole bush: the moon's side lighter, the far side in its own shadow
    for y, x in zip(ys, xs):
        d = (x - cx) / w - (y - cy) / h
        c = L.get(ox + x, oy + y)
        if d > 0.25 and c == "ny1":
            L.px(ox + x, oy + y, "ny0")
        elif d < -0.3 and c == "ny1":
            L.px(ox + x, oy + y, "ny2")
    edge = AG.ring(mask)
    for y, x in np.argwhere(edge):
        L.px(ox + x, oy + y, "nk")
    # a silver rim just inside the lit edge
    inner = AG.ring(mask & ~edge)
    for y, x in np.argwhere(inner):
        d = (x - cx) / w - (y - cy) / h
        if d < -0.15:
            L.px(ox + x, oy + y, "ny3")
    # flowers
    pts = [(x, y) for y, x in zip(ys, xs) if not edge[y, x] and h32(x, y, seed, 5) % 41 == 0]
    for x, y in pts[:flowers]:
        L.px(ox + x, oy + y, "nw1")
        if y + 1 < h and mask[y + 1, x]:
            L.px(ox + x, oy + y + 1, "nw0")


def bush_shadow(B, ox, oy, mask, sx=2, sy=2):
    """The bush's shadow on the lawn, thrown north-east."""
    h, w = mask.shape
    for y in range(h):
        for x in range(w):
            if mask[y, x]:
                tx, ty = x + sx, y - sy
                if 0 <= tx < w and 0 <= ty < h and not mask[ty, tx]:
                    c = B.get(ox + tx, oy + ty)
                    B.px(ox + tx, oy + ty, {"ng3": "ng1", "ng2": "ng0", "ng1": "ng0",
                                             "ng4": "ng2"}.get(c, c))


def bush_pieces():
    keys = ["myrtle", "myrtle_b", "myrtle_flowers", "big_tl", "big_tr", "big_bl", "big_br",
            "stump"]
    s = struct("bush", "Myrtle: small bushes and the big one", 8, 1, walk=["XXXXXXXX"],
               names=cells(keys, 8),
               notes="Myrtle bushes on the lawn, dense enough to stop a hound's eye. `myrtle`, "
                     "`_b`, `_flowers` (in white flower) are one cell. `big_*` is the great "
                     "myrtle, 2 x 2: place `big_tl` `big_tr` over `big_bl` `big_br`. `stump` is "
                     "an old cut laurel trunk. All block.")
    B, M = s.B, s.M
    for i in range(8):
        lawn(B, i * 16, 0, i)
    for i, (k, fl, sd) in enumerate((("myrtle", 2, 1), ("myrtle_b", 0, 2), ("myrtle_flowers", 7, 3))):
        m = blob_mask(16, 16, 7.5, 8.5, 7.2, 7.0, seed=sd)
        bush_shadow(B, i * 16, 0, m)
        paint_bush(M, i * 16, 0, m, flowers=fl, seed=sd)
    # the big myrtle, 32 x 32 over four cells
    big = blob_mask(32, 32, 15.5, 16.5, 15.4, 15.0, seed=4, wob=1.5)
    Bb, Mb = Layer(32, 32), Layer(32, 32)
    for cy in range(2):
        for cx in range(2):
            lawn(Bb, cx * 16, cy * 16, cx + cy)
    bush_shadow(Bb, 0, 0, big, 3, 3)
    paint_bush(Mb, 0, 0, big, flowers=9, seed=4)
    for n, (cx, cy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
        dst = (3 + n) * 16
        B.a[0:16, dst:dst + 16] = Bb.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        M.a[0:16, dst:dst + 16] = Mb.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
    # the stump
    put(M, 7 * 16 + 3, 5, [
        "..kkkkkkkk..",
        ".k1112111k..",
        "k1222222211k",
        "k1233333221k",
        "k1223332221k",
        "k0122222110k",
        "k0011111000k",
        ".k00000000k.",
        "..kk0kk0kk..",
    ], {"k": "nk", "0": "nt0", "1": "nt1", "2": "nb2" if False else "nt1", "3": "nw0"})
    return s


def stele(M, ox, oy, relief):
    """A grave stele, 12 px wide: a palmette crown, a carved relief, a plinth.
    Drawn over 32 rows (the cell above and the base cell)."""
    x0 = ox + 2
    # palmette crown
    put(M, x0, oy + 3, [
        "....4554....",
        "..44533544..",
        ".4533223354.",
        "433222222334",
        "kkkkkkkkkkkk",
    ], {"5": "ns5", "4": "ns4", "3": "ns3", "2": "ns2", "k": "ns1"})
    # the slab
    for y in range(8, 30):
        for x in range(12):
            c = "ns3" if x < 3 else ("ns2" if x < 9 else "ns1")
            if x == 0:
                c = "ns4"
            if x == 11:
                c = "nk"
            M.px(x0 + x, oy + y, c)
    M.hline(x0, x0 + 11, oy + 8, "ns4")
    # the relief, sunk into the slab
    reliefs = {
        "deer": [
            "..1.1...",
            "..11..1.",
            "...111..",
            "...44...",
            "..4444..",
            ".444444.",
            "4.4444.4",
            "..4..4..",
            "..4..4..",
        ],
        "bow": [
            ".1......",
            "1.11....",
            "1...1...",
            "1....1..",
            "4444444.",
            "1....1..",
            "1...1...",
            "1.11....",
            ".1......",
        ],
        "wreath": [
            "..4444..",
            ".4....4.",
            "4..11..4",
            "4.1..1.4",
            "4.1..1.4",
            "4..11..4",
            ".4....4.",
            "..4..4..",
            ".4....4.",
        ],
    }[relief]
    put(M, x0 + 2, oy + 12, reliefs, {"1": "ns1", "4": "ns4"})
    # plinth
    M.rect(x0 - 1, oy + 27, 14, 4, "ns2")
    M.hline(x0 - 1, x0 + 12, oy + 27, "ns4")
    M.hline(x0 - 1, x0 + 12, oy + 30, "ns0")
    M.px(x0 + 12, oy + 28, "nk")
    M.px(x0 + 12, oy + 29, "nk")


def cypress(M, ox, oy, tall, seed=0):
    """A cypress: a dark flame of foliage, a short trunk. 32 or 48 px tall."""
    h = 48 if tall else 32
    top = 1
    trunk_h = 5
    body = h - trunk_h - top
    for y in range(body):
        t = y / body
        half = 2.0 + 5.2 * math.sin(min(1.0, t * 1.15) * math.pi * 0.62) if t < 0.92 else 4.5
        half += 0.6 * math.sin(y * 1.7 + seed)
        for x in range(16):
            dx = x - 7.5
            if abs(dx) <= half:
                edge = abs(dx) > half - 1
                if edge:
                    c = "nk"
                elif dx < -half * 0.35:
                    c = "ny2" if (x + y) % 3 else "ny1"
                elif dx > half * 0.4:
                    c = "ny0"
                else:
                    c = "ny1" if h32(x, y // 2, 91, seed) % 4 else "ny0"
                M.px(ox + x, oy + top + y, c)
    for y in range(trunk_h):
        for x in (6, 7, 8, 9):
            M.px(ox + x, oy + top + body + y, "nt1" if x < 8 else "nt0")
    M.hline(ox + 5, ox + 10, oy + h - 1, "nk")


def tall_pieces():
    keys = ["stele_deer_top", "stele_bow_top", "stele_wreath_top", "cypress_top",
            "cypress_b_top", "lamp_top",
            "stele_deer", "stele_bow", "stele_wreath", "cypress", "cypress_b", "lamp"]
    names = {k: (i % 6, i // 6) for i, k in enumerate(keys)}
    s = struct("tall", "Stelae, cypresses, lamps: tall things on the lawn", 6, 2,
               walk=["TTTTTT", "XXXXXX"], names=names,
               notes="Each is a base (blocks) under a top drawn over the player in the cell "
                     "above, which must be plain `lawn` (the lamp's, plain `pave`). Stelae "
                     "carry a deer, a bow or a laurel wreath, and stop a hound's eye. "
                     "`cypress` and `cypress_b` are a cypress two cells tall. `lamp` is a "
                     "bronze lampstand, burning (the porch's).")
    B, M, T = s.B, s.M, s.T
    for i in range(6):
        if i == 5:
            pave(B, i * 16, 0, 1)
            pave(B, i * 16, 16, 2)
        else:
            lawn(B, i * 16, 0, i)
            lawn(B, i * 16, 16, i + 1)
    for i, rel in enumerate(("deer", "bow", "wreath")):
        L = Layer(16, 32)
        stele(L, 0, 0, rel)
        T.a[0:16, i * 16:i * 16 + 16] = L.a[0:16]
        M.a[16:32, i * 16:i * 16 + 16] = L.a[16:32]
        # its shadow on the lawn behind it, thrown north-east
        for x in range(6, 16):
            for y in range(9, 16):
                c = B.get(i * 16 + x, y)
                if (x + y) % 2 == 0 or y > 12:
                    B.px(i * 16 + x, y, {"ng3": "ng1", "ng2": "ng0", "ng1": "ng0",
                                         "ng4": "ng2"}.get(c, c))
    for i, seed in ((3, 0), (4, 1)):
        L = Layer(16, 32)
        cypress(L, 0, 0, False, seed)
        T.a[0:16, i * 16:i * 16 + 16] = L.a[0:16]
        M.a[16:32, i * 16:i * 16 + 16] = L.a[16:32]
    L = Layer(16, 32)
    lampstand(L, 0, 0)
    T.a[0:16, 80:96] = L.a[0:16]
    M.a[16:32, 80:96] = L.a[16:32]
    out = [s]
    # the tall cypress: three cells, a landmark
    s = struct("tallcypress", "A tall cypress", 1, 3, walk=["T", "T", "X"],
               names={"top": (0, 0), "mid": (0, 1), "base": (0, 2)},
               notes="A cypress three cells tall: `top` over `mid` (both drawn over the player) "
                     "over `base`, on plain `lawn`.")
    for cy in range(3):
        lawn(s.B, 0, cy * 16, cy)
    L = Layer(16, 48)
    cypress(L, 0, 0, True, 2)
    s.T.a[0:32, 0:16] = L.a[0:32]
    s.M.a[32:48, 0:16] = L.a[32:48]
    out.append(s)
    return out


def lampstand(L, ox, oy):
    """A tall bronze lampstand with a burning bowl: the porch's only flame."""
    put(L, ox + 3, oy + 2, [
        "....2.....",
        "...212....",
        "..21012...",
        "..20002...",
        ".2100012..",
        "..10001...",
    ], {"0": "ne2", "1": "ne1", "2": "ne0"})
    put(L, ox + 2, oy + 8, [
        "kkkkkkkkkkk",
        "k2222222221k",
        ".k11111111k.",
        "..kk1111kk..",
        "....k21k....",
    ], {"k": "nk", "2": "nz2", "1": "nz1"})
    for y in range(13, 28):
        L.px(ox + 7, oy + y, "nz2")
        L.px(ox + 8, oy + y, "nz1")
        L.px(ox + 9, oy + y, "nk")
    for y in (17, 22):
        L.hline(ox + 6, ox + 9, oy + y, "nz2")
    put(L, ox + 3, oy + 27, [
        "..k2221k..",
        ".k2111111k",
        "k21k..k11k",
        "kk......kk",
    ], {"k": "nk", "2": "nz2", "1": "nz1"})


# --------------------------------------------------------------------------
# The porch: kennels, the great altar, Artemis's statue, the bench, the gate wall
# --------------------------------------------------------------------------

KENNEL = [
    # 32 x 30: a wooden kennel with a gabled roof of bark shingles, door to the south
    "...........kkkkkkkkkk...........",
    ".........kk3333333333kk.........",
    ".......kk33222222222233kk.......",
    ".....kk3322222222222222233kk....",
    "...kk332222222222222222222233kk.",
    ".kk3322111111111111111111112233k",
    "k33221111111111111111111111112kk",
    "k3221000000000000000000000001kk.",
    "kk11000000000000000000000000kk..",
    ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
    "..k3322223322223322223322223k...",
    "..k3221122211221122211222113k...",
    "..k32111221kkkkkkkk112211113k...",
    "..k3211122kk......kk22111123k...",
    "..k3211122k........k22111123k...",
    "..k3211112k........k21111123k...",
    "..k3221112k........k21111223k...",
    "..k3221122k........k22111223k...",
    "..k3222222k........k22222223k...",
    "..k3221122k........k21122223k...",
    "..kk111111k........k1111111kk...",
    "...kkkkkkkk........kkkkkkkkk....",
]


def porch_pieces():
    out = []
    keys = ["kennel_tl", "kennel_tr", "kennel_bl", "kennel_br", "bowl", "leash", "bench_l",
            "bench_r"]
    s = struct("kennel", "The hounds' kennels, a bowl, Anthia's bench", 8, 1, walk=["XXXXXXXX"],
               names=cells(keys, 8),
               notes="By the porch: the temple hounds' kennels (2 x 2: `kennel_tl` `kennel_tr` "
                     "over `kennel_bl` `kennel_br`), a bronze water `bowl`, a `leash` coiled on "
                     "a post, all on the porch's paving. `bench_l` `bench_r`: a marble bench "
                     "with a fleece thrown over it, on the lawn (Anthia's grove). All block.")
    B, M = s.B, s.M
    for i in range(6):
        pave(B, i * 16, 0, i)
    for i in (6, 7):
        lawn(B, i * 16, 0, i)
    K = Layer(32, 32)
    put(K, 0, 7, KENNEL, {"k": "nk", "3": "nb3", "2": "nb2", "1": "nb1", "0": "nb0"})
    for x in range(11, 19):
        K.px(x, 7 + 20, "nc0" if x % 2 else "nb2")
    for n, (cx, cy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
        dst = n * 16
        M.a[0:16, dst:dst + 16] = K.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
    put(M, 4 * 16 + 2, 6, [
        "..kkkkkkkk..",
        ".k22222222k.",
        "k2211111122k",
        "k21ssssss12k",
        "k21sSSSss12k",
        ".k11111111k.",
        "..kkkkkkkk..",
    ], {"k": "nk", "2": "nz2", "1": "nz1", "s": "ns1", "S": "ns2"})
    put(M, 5 * 16 + 3, 1, [
        "...kkkk...",
        "...k21k...",
        ".kkk21kkk.",
        "k2222222kk",
        "k2kkkkkk2k",
        "k2k.21.k2k",
        "k2k.21.k2k",
        ".k222222k.",
        "..kk21kk..",
        "....21....",
        "....21....",
        "...k21k...",
        "..kkkkkk..",
    ], {"k": "nk", "2": "nb3", "1": "nb2"})
    bench = [
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
        ".k5555555555555555555555555554k.",
        ".k4444wwwwwwwwww44444444444443k.",
        ".k444wWWWWWWWWWWw4444444444443k.",
        ".k333wWWWWWWWWWWw3333333333332k.",
        ".kkkkwWWWWWWWWWWwkkkkkkkkkkkkkk.",
        "..k3wWWWWWWWWWWWWw2k.....k32k...",
        "..k32wwwwwwwwwwww2k......k32k...",
        "..k322k.........k........k32k...",
        "..k322k..................k22k...",
        "..kkkkk..................kkkk...",
    ]
    Lb = Layer(32, 16)
    put(Lb, 0, 3, bench, {"k": "nk", "5": "ns5", "4": "ns4", "3": "ns3", "2": "ns2",
                          "w": "ns4", "W": "nsw"})
    M.a[0:16, 96:128] = Lb.a[0:16, 0:32]
    out.append(s)

    s = struct("altar", "The great altar of Artemis", 3, 2, walk=["XXX", "XXX"],
               names={"altar_tl": (0, 0), "altar_tm": (1, 0), "altar_tr": (2, 0),
                      "altar_bl": (0, 1), "altar_bm": (1, 1), "altar_br": (2, 1)},
               notes="The great altar (3 x 2) on the porch's paving: a marble table under a "
                     "silver crescent, a bow and a quiver carved on its front, the first "
                     "feathers of the hunt laid on top.")
    for cy in range(2):
        for cx in range(3):
            pave(s.B, cx * 16, cy * 16, cx + cy)
    altar(s.M, 0, 0)
    out.append(s)

    s = struct("statue", "Artemis", 2, 3, walk=["TT", "XX", "XX"],
               names={"tl": (0, 0), "tr": (1, 0), "ml": (0, 1), "mr": (1, 1),
                      "bl": (0, 2), "br": (1, 2)},
               notes="The goddess on her plinth, drawing an arrow from her quiver, on the "
                     "porch's paving: `tl` `tr` (drawn over the player) over `ml` `mr` over "
                     "`bl` `br`.")
    for cy in range(3):
        for cx in range(2):
            pave(s.B, cx * 16, cy * 16, cx + cy)
    st = statue_layer()
    s.T.a[0:16, 0:32] = st.a[0:16]
    s.M.a[16:48, 0:32] = st.a[16:48]
    out.append(s)
    return out


ALTAR = [
    # 48 x 32
    "................................................",
    "................55555...........................",
    "..............55444355..........................",
    "............554.....3355........................",
    "...........54...........1...1...1..........1....",
    "..........54.............1.1...1..........1.....",
    "..........53........cc....1...1....w.....1......",
    "..........53......cc..c..1.1.1.....w....1.......",
    "...kkkkkkkk53kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
    "..k5555555553555555555555555555555555555555554k.",
    "..k4444444444444444444444444444444444444444443k.",
    "..k3333333333333333333333333333333333333333332k.",
    "..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
    "...k4433444444444444444444444444444444444332k...",
    "...k43k1111111111111111111111111111111111k32k...",
    "...k43k1.....................bbbbbb.....1k32k...",
    "...k43k1....aaaaa..........bb......b....1k32k...",
    "...k43k1...a.....aa.......b.........b...1k32k...",
    "...k43k1..a........a.....b..........b...1k32k...",
    "...k43k1..a.........44444444444444444b..1k32k...",
    "...k43k1..a........a.....b..........b...1k32k...",
    "...k43k1...a.....aa.......b.........b...1k32k...",
    "...k43k1....aaaaa..........bb......b....1k32k...",
    "...k43k1.....................bbbbbb.....1k32k...",
    "...k43k1111111111111111111111111111111111k32k...",
    "...k4433333333333333333333333333333333333332k...",
    "..kk555555555555555555555555555555555555555kkk..",
    "..k44444444444444444444444444444444444444443k...",
    "..k33333333333333333333333333333333333333332k...",
    "..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "................................................",
    "................................................",
]


def altar(M, ox, oy):
    put(M, ox, oy, ALTAR, {"k": "nk", "5": "ns5", "4": "ns4", "3": "ns3", "2": "ns2",
                           "1": "ns1", "a": "ns1", "b": "ns1", "c": "nau1", "w": "nsw"})
    # the silver crescent standing on the altar's back edge
    put(M, ox + 10, oy + 1, [".......", "..5555.", ".5.....", "5......"], {"5": "nsw"})
    # feathers laid on the table
    for i, x in enumerate((24, 28, 33, 38)):
        M.px(ox + x, oy + 6, "nsw")
        M.px(ox + x + 1, oy + 5, "ns4")
        M.px(ox + x + 2, oy + 4, "ns4")


STATUE = [
    # 32 x 48: Artemis drawing an arrow from her quiver, a hound at her knee
    "................................",
    "..............kkk...............",
    ".............k545k..............",
    ".............k454k..1...........",
    "..............k4k..1.1..........",
    "............kk444kk1..1.........",
    "...........k4554455k...1........",
    "..........k45k5544k5k..1........",
    "..........k4k.k544kk4k.1........",
    "..........k4k.k544k.k45k........",
    "..........k4k.k543k..k4k........",
    "...........k..k443k..1..........",
    "..............k4443k1...........",
    ".............k454433k...........",
    ".............k4544333k..........",
    "............k45443333k..........",
    "............k454433332k.........",
    "...........k4544333332k.........",
    "...........k4544333332k.........",
    "....kkk....k4544333332k.........",
    "...k454k...k454433333k..........",
    "..k4544kk..k454433332k..........",
    "..k4k44544kk45443332k...........",
    "...k.k44454k4544332k............",
    "......k4443k4k43k32k............",
    "......k4k3kk4k.k3k3k............",
    "......k4k.k4k..k3k3k............",
    "......kk..kk...kk.kk............",
    "..kkkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "..k5555555555555555555555554k...",
    "..k4444444444444444444444443k...",
    "..k3333333333333333333333332k...",
    "..kkkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "...k44444444444444444444443k....",
    "...k43333333333333333333332k....",
    "...k43333333333333333333332k....",
    "...k43333333333333333333332k....",
    "...k43333333333333333333332k....",
    "...k43333333333333333333332k....",
    "...k42222222222222222222221k....",
    "..kk555555555555555555555555kk..",
    "..k4444444444444444444444444443k",
    "..k3333333333333333333333333332k",
    "..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    "................................",
    "................................",
    "................................",
    "................................",
]


def statue_layer():
    L = Layer(32, 48)
    put(L, 0, 0, STATUE, {"k": "nk", "5": "nsw", "4": "ns4", "3": "ns3", "2": "ns2",
                          "1": "ns2"})
    return L


# --------------------------------------------------------------------------
# The moonlit rock and its stair, the hedge across the stair, Anthia's gate, the pool
# --------------------------------------------------------------------------

ROCK_KEYS = [
    # row 0: the flat (walkable)
    "flat", "flat_b", "flat_shade", "flat_w", "flat_e", "seat", "corner_w", "corner_e",
    # row 1: the lip and the cliff's upper course
    "lip", "lip_w", "lip_e", "stair_top", "cliff", "cliff_w", "cliff_e", "stair",
    # row 2: the cliff's foot course, the stair's foot, the rubble and the landing
    "foot", "foot_w", "foot_e", "stair_foot", "rubble", "boulder", "landing", "cliff_b",
]
FLAT_CRACKS = {(2, 3), (3, 4), (4, 4), (5, 5), (10, 9), (11, 10), (11, 11), (12, 12), (7, 14),
               (8, 14)}


def rock_flat_px(x, y):
    """The rock's moonlit flat: pale stone worn smooth, soft mottling, a few hairline
    cracks and glints. 16-periodic."""
    xx, yy = x % 16, y % 16
    if (xx, yy) in FLAT_CRACKS:
        return "nr3"
    if (xx - 1, yy - 1) in FLAT_CRACKS:
        return "nr5"
    patch = h32(xx // 4, yy // 4, 11) % 5
    if patch == 0 and (xx + yy) % 2 == 0:
        return "nr3"
    if h32(xx, yy, 13) % 61 == 0:
        return "nr5"
    return "nr4"


def rock_face_px(x, y, course):
    """The cliff: two courses of rough-laid stones to a cell, each lit along its top and
    its west edge by the moon. course 0 the upper cliff row, 1 the foot (darker)."""
    xx, yy = x % 16, y % 16
    row = yy // 8
    ly = yy % 8
    joints = (0, 9) if row == 0 else (4, 13)
    lx = min((xx - j) % 16 for j in joints)
    if ly == 7 or lx == 0:
        c = "nk"
    elif ly == 0 or lx == 1:
        c = "nr3"
    elif ly == 6:
        c = "nr1"
    else:
        c = "nr2"
        if h32(xx, yy, 7) % 13 == 0:
            c = "nr3"
    if course == 1 and row == 1 and c in ("nr2", "nr3"):
        c = "nr1" if (xx + yy) % 2 else "nr2"
    return c


def rock_pieces():
    """The moonlit rock, as cell types the map composes: its flat on top (walkable), the
    lip where the flat drops, two courses of cliff, the stair cut through them, rubble and
    boulders at the foot, and the landing at the stair's foot where Prokris stands."""
    walk = ["......XX", "....XXX.", "XXX.XX.X"]
    s = struct("rock", "The moonlit rock", 8, 3, walk=walk, names=cells(ROCK_KEYS, 8),
               notes="Kallisto's rock, built from cell types. Row by row of the rock: the "
                     "`flat` on top (`_b`; `_shade` under the hedge; `_w`/`_e` its sides, the "
                     "lawn beyond; `corner_w`/`_e` lawn with the rock's rounded corner, "
                     "blocking), the `lip` where it drops (`_w`, `_e`; `stair_top` where the "
                     "stair begins), the `cliff` (`_b`, `_w`, `_e`; `stair`), the cliff's "
                     "`foot` (`_w`, `_e`; `stair_foot`), and in front of it `rubble`, a "
                     "`boulder` and a `landing` of flat rock. `seat` is the flat stone "
                     "Kallisto sits on (walkable: she stands on it).")
    B, M = s.B, s.M
    pos = {k: ((i % 8) * 16, (i // 8) * 16) for i, k in enumerate(ROCK_KEYS)}

    def lawn_cell(k):
        ox, oy = pos[k]
        lawn(B, ox, oy, 0)

    def flat_cell(k, side=None):
        ox, oy = pos[k]
        for y in range(16):
            for x in range(16):
                B.px(ox + x, oy + y, rock_flat_px(x + (5 if k == "flat_b" else 0), y))
        if side:
            lawn_strip(ox, oy, side)

    def lawn_strip(ox, oy, side, top=0, bottom=16):
        # the lawn beyond the rock's side, and the rock's lit or shaded edge
        for y in range(top, bottom):
            for x in range(16):
                xx = x if side == "w" else 15 - x
                if xx < 3:
                    B.a[oy + y, ox + x] = tex("lawn").a[y % 16, x % 16]
                elif xx == 3:
                    B.px(ox + x, oy + y, "nk")
                elif xx == 4:
                    B.px(ox + x, oy + y, "nr5" if side == "w" else "nr2")

    def face_cell(k, course, side=None):
        ox, oy = pos[k]
        for y in range(16):
            for x in range(16):
                B.px(ox + x, oy + y, rock_face_px(x + (7 if k == "cliff_b" else 0), y, course))
        if side:
            lawn_strip(ox, oy, side)

    for k in ("flat", "flat_b"):
        flat_cell(k)
    flat_cell("flat_shade")
    ox, oy = pos["flat_shade"]
    for y in range(6):
        for x in range(16):
            if y < 3 or (x + y) % 2 == 0:
                c = B.get(ox + x, oy + y)
                B.px(ox + x, oy + y, {"nr4": "nr2", "nr5": "nr3", "nr3": "nr2", "nm4": "nr3"}.get(c, c))
    flat_cell("flat_w", "w")
    flat_cell("flat_e", "e")
    # the seat: a flat slab, a bearskin over it
    flat_cell("seat")
    ox, oy = pos["seat"]
    put(M, ox + 1, oy + 3, [
        ".kkkkkkkkkkkk.",
        "k555555555554k",
        "k4bbbbbbbbb43k",
        "k4b1b1b1b1b43k",
        "k4bbbbbbbbb43k",
        "k33333333333kk",
        ".kkkkkkkkkkkk.",
    ], {"k": "nk", "5": "nr5", "4": "nr4", "3": "nr3", "b": "nr1", "1": "nr0"})
    # rounded corners: lawn, the rock's corner in its inner quarter
    for k, side in (("corner_w", "w"), ("corner_e", "e")):
        ox, oy = pos[k]
        lawn(B, ox, oy, 1)
        for y in range(16):
            for x in range(16):
                xx = x if side == "w" else 15 - x
                d = math.hypot(15.5 - xx, 15.5 - y)
                if d < 11:
                    B.px(ox + x, oy + y, rock_flat_px(x, y))
                elif d < 12:
                    B.px(ox + x, oy + y, "nk")
                elif d < 13 and xx > 6 and y > 6:
                    B.px(ox + x, oy + y, "ng0")
    # the lip: the flat's front edge, a bright rim, the drop
    for k, side in (("lip", None), ("lip_w", "w"), ("lip_e", "e"), ("stair_top", None)):
        ox, oy = pos[k]
        for y in range(16):
            for x in range(16):
                if y < 10:
                    c = rock_flat_px(x, y)
                elif y == 10:
                    c = "nr5"
                elif y == 11:
                    c = "nr4" if x % 3 else "nr5"
                elif y < 15:
                    c = rock_face_px(x, y, 0) if k != "stair_top" else ("nr3" if y % 3 else "nr4")
                else:
                    c = "nk" if k != "stair_top" else "nr1"
                B.px(ox + x, oy + y, c)
        if side:
            lawn_strip(ox, oy, side)
        if k == "stair_top":
            for y in range(10, 16):
                B.px(ox + 0, oy + y, "nk")
                B.px(ox + 15, oy + y, "nk")
    face_cell("cliff", 0)
    face_cell("cliff_b", 0)
    face_cell("cliff_w", 0, "w")
    face_cell("cliff_e", 0, "e")
    face_cell("foot", 1)
    face_cell("foot_w", 1, "w")
    face_cell("foot_e", 1, "e")
    # the stair: steps cut into the cliff, one cell wide each (two side by side)
    for k in ("stair", "stair_foot"):
        ox, oy = pos[k]
        for y in range(16):
            for x in range(16):
                step = y % 8
                c = "nr4" if step == 0 else ("nr3" if step < 5 else "nr2")
                if step == 7:
                    c = "nr1"
                B.px(ox + x, oy + y, c)
        if k == "stair_foot":
            for x in range(16):
                B.px(ox + x, oy + 15, "nr1")
    # rubble at the foot: stones on the lawn, blocking
    ox, oy = pos["rubble"]
    lawn(B, ox, oy, 0)
    for (cx, cy, rx, ry, sd) in ((4, 5, 4, 3, 1), (11, 4, 4, 3, 2), (7, 11, 5, 4, 3)):
        m = blob_mask(16, 16, cx, cy, rx, ry, seed=sd)
        for y, x in np.argwhere(m):
            d = (x - cx) - (y - cy)
            B.px(ox + x, oy + y, "nr4" if d < -2 else ("nr1" if d > 2 else "nr2"))
        for y, x in np.argwhere(AG.ring(m)):
            B.px(ox + x, oy + y, "nk")
    ox, oy = pos["boulder"]
    lawn(B, ox, oy, 1)
    m = blob_mask(16, 16, 7.5, 8.5, 7.0, 6.5, seed=4)
    for y, x in np.argwhere(m):
        d = (x - 7.5) - (y - 8.5)
        B.px(ox + x, oy + y, "nr4" if d < -4 else ("nr1" if d > 3 else ("nr3" if d < 0 else "nr2")))
    for y, x in np.argwhere(AG.ring(m)):
        B.px(ox + x, oy + y, "nk")
    ox, oy = pos["landing"]
    for y in range(16):
        for x in range(16):
            c = "nr3" if h32(x, y, 3) % 9 else "nr2"
            if y < 2:
                c = "nr1"
            B.px(ox + x, oy + y, c)
    # the rock's palette has no room for the lawn's brightest tip
    for y in range(B.h):
        for x in range(B.w):
            if B.get(x, y) == "ng4":
                B.px(x, y, "ng3")
    return s


def stairhedge_pieces():
    keys = ["hedge_l", "hedge_lowered_l", "hedge_r", "hedge_lowered_r",
            "gate_top", "gate_top_open", "gate", "gate_open"]
    s = struct("gates", "The hedge across the stair, and Anthia's gate", 8, 1,
               walk=["X.X.X.X."], names=cells(keys, 8),
               notes="`hedge_l` `hedge_r`: the low laurel hedge across the foot of the rock's "
                     "stair, on the rock's stair rock; `hedge_lowered_*` (= the hedge + 1) is "
                     "the same hedge clipped to its roots, walkable. `gate_top` over `gate`: "
                     "Anthia's woven laurel gate in a hedge wall's top and face rows; "
                     "`gate_top_open` and `gate_open` (= the closed piece + 1) stand open.")
    B, M, T = s.B, s.M, s.T
    # the stair's foot under the hedge: stone steps
    for i, k in enumerate(keys[:4]):
        ox = i * 16
        for y in range(16):
            for x in range(16):
                step = y % 6
                c = "nr4" if step == 0 else ("nr3" if step < 4 else "nr2")
                if (k.endswith("_l") and x == 0) or (k.endswith("_r") and x == 15):
                    c = "nr1"
                if step == 5:
                    c = "nr1"
                B.px(ox + x, y, c)
        if "lowered" in k:
            # roots and clippings: a dark line of stubs across the step
            for x in range(16):
                if (x + i) % 3 == 0:
                    M.px(ox + x, 10, "nl1")
                    M.px(ox + x, 9, "nl3")
                if (x * 5 + i) % 7 == 0:
                    M.px(ox + x, 12, "nl4")
        else:
            # a low hedge: clipped top (rows 2-8), face (rows 9-14)
            for y in range(1, 15):
                for x in range(16):
                    if y == 1:
                        c = "nk"
                    elif y < 9:
                        t = tex("laurel").a[y % 16, (x + ox) % 16]
                        M.a[y, ox + x] = t
                        continue
                    elif y == 9:
                        c = "nl5" if x % 3 else "nl4"
                    elif y < 14:
                        t = tex("face").a[y % 16, (x + ox) % 16]
                        M.a[y, ox + x] = t
                        continue
                    else:
                        c = "nl0"
                    M.px(ox + x, y, c)
            side = 0 if k.endswith("_l") else 15
            for y in range(1, 15):
                M.px(ox + side, y, "nk")
    # Anthia's gate: in a hedge wall. The top cell: the hedge top with a gap for an arbor
    # over it; the face cell: a woven laurel gate on a wooden frame
    for i, k in enumerate(keys[4:]):
        ox = (4 + i) * 16
        if k.startswith("gate_top"):
            paint_tex(B, "laurel", ox, 0)
            if k.endswith("open"):
                lawn(B, ox, 0)
                for y in range(16):
                    B.px(ox + 0, y, "nk")
                    B.px(ox + 15, y, "nk")
            # a woven arbor of bent laurel over the gate (top layer)
            for x in range(16):
                y = 3 + int(2.5 * (1 - math.sin(x / 15 * math.pi)))
                T.px(ox + x, y, "nl4")
                T.px(ox + x, y + 1, "nl2")
                if x % 3 == 0:
                    T.px(ox + x, y - 1, "nl3")
        else:
            if k.endswith("open"):
                lawn(B, ox, 0)
                for y in range(16):
                    B.px(ox + 0, y, "nk")
                    B.px(ox + 15, y, "nk")
                # the gate swung back against the hedge, seen edge-on
                for y in range(2, 15):
                    M.px(ox + 1, y, "nt1")
                    M.px(ox + 2, y, "nl3" if y % 2 else "nl4")
            else:
                paint_tex(B, "face", ox, 0)
                for y in range(16):
                    for x in range(16):
                        if x in (1, 14) or y in (2, 13):
                            c = "nt1" if x in (1, 14) or y == 2 else "nt0"
                        elif 2 < y < 13 and 1 < x < 14:
                            c = "nl3" if (x + y) % 4 < 2 else "nl2"
                            if (x - y) % 4 == 0:
                                c = "nl4"
                        else:
                            continue
                        M.px(ox + x, y, c)
                M.px(ox + 11, 8, "nz2" if False else "nt1")
    return s


def pool_pieces():
    keys = ["pool_l", "pool_r"]
    s = struct("pool", "The moon pool on the rock", 2, 1, walk=["XX"], names=cells(keys, 2),
               notes="A basin cut in the rock's flat, holding still black water and the "
                     "moon's reflection. Blocks; place on the rock's flat.")
    B, M = s.B, s.M
    for y in range(16):
        for x in range(32):
            B.px(x, y, rock_flat_px(x, y))
    yy, xx = np.mgrid[0:16, 0:32]
    rim = ((xx - 15.5) / 15.0) ** 2 + ((yy - 8.0) / 7.2) ** 2 <= 1
    water = ((xx - 15.5) / 12.5) ** 2 + ((yy - 8.5) / 5.2) ** 2 <= 1
    for y, x in np.argwhere(rim & ~water):
        # the basin's cut lip: lit on the far (north) side, in shadow on the near one
        M.px(x, y, "nr4" if y < 6 else ("nr3" if y < 10 else "nr2"))
    for y, x in np.argwhere(AG.ring(rim)):
        M.px(x, y, "nk")
    for y, x in np.argwhere(water):
        c = "nq0" if y < 6 else "nq1"
        if (y == 8 or y == 11) and h32(x, 5) % 3 == 0:
            c = "nq2"
        M.px(x, y, c)
    for y, x in np.argwhere(AG.ring(water)):
        if y < 9:
            M.px(x, y, "nk")
    # the moon lying in the water, and two stars
    put(M, 13, 6, [".444.", "44443", "44433", ".333."], {"4": "nq4", "3": "nq3"})
    M.px(8, 9, "nm4")
    M.px(23, 7, "nm4")
    return s


def split(s, cols):
    """Cut a structure wider than the sheet into column bands, keeping its cell names."""
    out = []
    x0 = 0
    for n, w in enumerate(cols):
        names = {k: (cx - x0, cy) for k, (cx, cy) in s.names.items() if x0 <= cx < x0 + w}
        p = Struct(f"{s.key}_{n}", f"{s.title} ({'west' if n == 0 else 'east'} half)", w, s.h,
                   SEC, walk=[r[x0:x0 + w] for r in s.walk], notes=s.notes, names=names)
        for ln in ("bottom", "middle", "top"):
            p.layers[ln].a[:] = s.layers[ln].a[:, x0 * 16:(x0 + w) * 16]
        p.behaviors = {(cx - x0, cy): mb for (cx, cy), mb in s.behaviors.items() if x0 <= cx < x0 + w}
        out.append(p)
        x0 += w
    return out


def build():
    structs = [floor_pieces()]
    structs += soft_sets()
    structs.append(hedge_set())
    structs += [arch("antlers"), arch("bow"), arch("moon")]
    structs.append(bush_pieces())
    structs += tall_pieces()
    structs += porch_pieces()
    structs.append(rock_pieces())
    structs.append(stairhedge_pieces())
    structs.append(pool_pieces())
    return structs
