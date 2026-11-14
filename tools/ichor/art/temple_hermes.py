"""gTileset_TempleHermes: the Temple of Hermes's interior and the Herald's Run.

Emporion's temple (Laurel 2, Hierophant Kerykos the Herald, Flying). The hall is
cool Ionic marble under a frieze of golden wings on Aegean blue, with a racetrack
inlaid in red porphyry and gold. Everything the Herald's Run (SYSTEMS.md §12)
needs is here:

- herald-herms, the posts the scrolls are delivered to: a head that faces any of
  four ways (it swivels to point the way once anointed), plain or anointed
  (oil-bright, a laurel wreath on the head), on a shaft plain or holding a
  delivered scroll;
- Hermes's one-way turnstiles, one per direction of passage;
- bronze lattice gates, open or shut, across either run of a wall;
- a low marble balustrade that joins any way, for the switchback stoa;
- the racetrack inlay: lanes, turns, the starting sill, direction chevrons;
- relay torches, lit or cold; the step-glass (a bronze klepsydra);
- scroll pigeonholes in the wall and as a cabinet, full or emptied, and the
  table where Kerykos lays out the sealed scrolls; a stand of anointing oil;
- the herald's rostrum: a raised platform with its edges, risers and steps, and
  a lectern to speak across; a statue of Hermes; Ionic columns; a winged mosaic;
- the walls (cornice, frieze, lower wall), the side walls and the doormat.

Like the Temple of Hestia it uses only its own tiles and palettes 6-12, and every
bottom layer is opaque, so it works on any primary (it is drawn for oikos).
Objects stand in the middle layer over the floor; nothing is drawn over sprites.
"""
from __future__ import annotations

import math

import numpy as np

import emporion_lib as E
import kalliste_lib as K
from emporion_lib import tile_colors

# --------------------------------------------------------------------------
# Colors and palette groups (all multiples of 8)
# --------------------------------------------------------------------------

NEW = {
    "hk": (32, 24, 40), "hw": (248, 248, 248),
    "hm0": (232, 232, 224), "hm1": (208, 208, 200), "hm2": (176, 176, 176),
    "hm3": (136, 136, 144), "hm4": (96, 96, 112),
    "hp0": (104, 32, 40), "hp1": (152, 56, 56), "hp2": (200, 96, 88),
    "hg0": (192, 144, 40), "hg1": (240, 200, 88),
    "hb0": (32, 56, 112), "hb1": (56, 96, 168), "hb2": (112, 152, 216),
    "hz0": (88, 56, 24), "hz1": (136, 88, 32), "hz2": (192, 136, 56), "hz3": (232, 192, 120),
    "hf0": (216, 72, 32), "hf1": (248, 232, 160),
    "hd0": (72, 40, 24), "hd1": (120, 72, 40), "hd2": (168, 112, 64),
    "hy0": (200, 176, 120), "hy1": (232, 216, 168),
    "hl0": (48, 88, 48), "hl1": (96, 136, 64),
    "hr": (184, 40, 32), "hc0": (152, 72, 40), "hc1": (208, 120, 72),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # the floor: marble slabs, the porphyry racetrack and its gold, the mosaic, the mat
    "floor": ["hk", "hw", "hm0", "hm1", "hm2", "hm3", "hm4", "hp0", "hp1", "hp2", "hg0", "hg1",
              "hb0", "hb1", "hb2"],
    # standing marble: columns, herms (with oil and laurel), balustrades, the rostrum, statue
    "marble": ["hk", "hw", "hm0", "hm1", "hm2", "hm3", "hm4", "hg0", "hg1", "hl0", "hl1", "hb0",
               "hb1", "hz1", "hr"],
    # the walls and the painted frieze
    "frieze": ["hk", "hw", "hm0", "hm1", "hm2", "hm3", "hm4", "hb0", "hb1", "hb2", "hg0", "hg1",
               "hr", "hp1", "hz1"],
    # bronze and fire: turnstiles, gates, torches, the step-glass
    "bronze": ["hk", "hz0", "hz1", "hz2", "hz3", "hf0", "hf1", "hg1", "hw", "hb1", "hb2", "hm2",
               "hm3", "hd0", "hr"],
    # cedar, papyrus and clay: pigeonholes, scrolls and seals, the table, the oil, the mat
    "wood": ["hk", "hd0", "hd1", "hd2", "hy0", "hy1", "hw", "hr", "hg0", "hg1", "hb1", "hc0",
             "hc1", "hl1", "hm3"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15 and len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

SEC = "temple_hermes"


class Struct(E.Struct):
    def __init__(self, key, title, w, h, walk=None, notes=""):
        super().__init__(key, title, w, h, walk=walk, notes=notes, ground="none",
                         section=SEC)


def validate(structs):
    problems = []
    for s in structs:
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    cols = tile_colors(layer, tx, ty)
                    if cols and not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                n = sum(1 for layer in s.layers.values() if (layer.a[sl][..., 3] > 0).any())
                if n == 3:
                    problems.append(f"{s.key} ({cx},{cy}) has three layers")
                if not (s.B.a[sl][..., 3] > 0).all():
                    problems.append(f"{s.key} ({cx},{cy}) has a bottom layer that isn't opaque")
    return problems


# --------------------------------------------------------------------------
# Floors
# --------------------------------------------------------------------------

def floor(L, x0, y0, variant=0):
    """A 16 px slab of cool white marble: lit along its top and left edges, a
    grey joint right and bottom. Variants: 1 and 2 veined, 3 worn and cracked."""
    for y in range(16):
        for x in range(16):
            c = "hm1"
            if x == 15 or y == 15:
                c = "hm2"
            elif x == 0 or y == 0:
                c = "hm0"
            L.px(x0 + x, y0 + y, c)
    if variant == 1:
        for i in range(9):
            L.px(x0 + 3 + i, y0 + 4 + i // 2, "hm0")
        L.px(x0 + 9, y0 + 9, "hm0")
    elif variant == 2:
        for i in range(8):
            L.px(x0 + 11 - i, y0 + 3 + i, "hm0")
        L.px(x0 + 4, y0 + 11, "hm0")
        L.px(x0 + 5, y0 + 12, "hm0")
    elif variant == 3:
        L.blit(["k    ", " k   ", "  kk ", "  k k", " k   "], {"k": "hm2"}, x0 + 5, y0 + 6)


def floors():
    s = Struct("floor", "Floor: cool Ionic marble", 6, 1, walk=["......"],
               notes="(0) the void, near-black, for the layout's border (block it); (1) "
                     "marble slab; (2), (3) veined slabs to scatter; (4) a worn, cracked "
                     "slab for the walked lines; (5) a slab inlaid with a small gold wing, "
                     "where the temple's people stand.")
    L = s.B
    L.rect(0, 0, 16, 16, "hk")
    for (x, y) in ((3, 4), (11, 9), (7, 13)):
        L.px(x, y, "hm4")
    for i, v in enumerate((0, 1, 2, 3, 0)):
        floor(L, 16 + i * 16, 0, v)
    L.blit(["   gG", " gGG ", "gG   ", "Gg   "], {"g": "hg0", "G": "hg1"}, 86, 6)
    s.walk = ["X....."]
    s.names = {"void": (0, 0), "slab": (1, 0), "vein_a": (2, 0), "vein_b": (3, 0),
               "worn": (4, 0), "wing": (5, 0)}
    return s


# --------------------------------------------------------------------------
# The racetrack inlay
# --------------------------------------------------------------------------

def _lane_px(L, x0, y0, inside):
    """Paint a lane: inside(x, y) -> 0 outside, 1 gold edge, 2 porphyry."""
    for y in range(16):
        for x in range(16):
            v = inside(x, y)
            if v == 1:
                L.px(x0 + x, y0 + y, "hg0")
            elif v == 2:
                L.px(x0 + x, y0 + y, "hp1" if (x + y) % 7 else "hp0")
            elif v == 3:
                L.px(x0 + x, y0 + y, "hp2")


def lanes():
    """A lane of red porphyry ten px wide edged with gold, laid through the
    middle of each cell, with turns, the starting sill and chevrons."""
    s = Struct("lane", "The racetrack inlay: lanes, turns, the starting sill, chevrons", 8, 2,
               walk=["........", "........"],
               notes="A lane of red porphyry edged in gold, inlaid in the floor. Row 0: east-west "
                     "run, north-south run, the four turns (joining N-E, E-S, S-W, W-N), a "
                     "crossing, and the starting sill across an east-west lane (white stone, "
                     "two grooves). Row 1: chevrons pointing north, east, south and west (the "
                     "way the run goes, or a turnstile's way), the starting sill across a "
                     "north-south lane, a turning post's disc (the kampter, where the lane "
                     "turns at the stadium's end), and two plain slabs. All walkable.")
    L = s.B
    for i in range(16):
        floor(L, i % 8 * 16, i // 8 * 16)

    def band_h(x, y):
        return 1 if y in (3, 12) else 2 if 4 <= y <= 11 else 0

    def band_v(x, y):
        return 1 if x in (3, 12) else 2 if 4 <= x <= 11 else 0

    def turn(cxs, cys):
        # a quarter ring centred on the cell corner (cxs, cys), radius 3.5..12.5
        def f(x, y):
            r = math.hypot(x + 0.5 - cxs, y + 0.5 - cys)
            if 3 <= r < 4 or 12 <= r < 13:
                return 1
            return 2 if 4 <= r < 12 else 0
        return f
    _lane_px(L, 0, 0, band_h)
    _lane_px(L, 16, 0, band_v)
    for i, (cx, cy) in enumerate(((16, 0), (16, 16), (0, 16), (0, 0))):   # NE, ES, SW, WN
        _lane_px(L, 32 + i * 16, 0, turn(cx, cy))
    _lane_px(L, 96, 0, lambda x, y: max(band_h(x, y), band_v(x, y)))
    # the starting sill across an E-W lane: white stone, two grooves
    _lane_px(L, 112, 0, band_h)
    for y in range(2, 14):
        for x in (117, 118, 119, 120, 121, 122):
            L.px(x, y, "hw" if x in (117, 122) or y in (2, 13) else "hm1")
        L.px(119, y, "hm3")
        L.px(120, y, "hm3")
    # row 1: chevrons on an E-W or N-S lane
    for i, (d, base) in enumerate((("n", band_v), ("e", band_h), ("s", band_v), ("w", band_h))):
        x0 = i * 16
        _lane_px(L, x0, 16, base)
        chev = ["   G   ", "  GgG  ", " Gg gG ", "Gg   gG", "g     g"]
        if d == "s":
            chev = chev[::-1]
        if d in ("n", "s"):
            L.blit(chev, {"G": "hg1", "g": "hg0"}, x0 + 4, 16 + 5)
        else:
            rot = ["".join(chev[len(chev) - 1 - j][i2] for j in range(len(chev)))
                   for i2 in range(len(chev[0]))]
            if d == "w":
                rot = [r[::-1] for r in rot]
            L.blit(rot, {"G": "hg1", "g": "hg0"}, x0 + 5, 16 + 4)
    _lane_px(L, 64, 16, band_v)
    for x in range(66, 78):
        for y in (21, 22, 23, 24, 25, 26):
            L.px(x, y, "hw" if y in (21, 26) or x in (66, 77) else "hm1")
        L.px(x, 23, "hm3")
        L.px(x, 24, "hm3")
    # the turning post's disc (kampter): a gold ring with a porphyry boss
    for y in range(16):
        for x in range(16):
            r = math.hypot(x - 7.5, y - 7.5)
            if r < 6.5:
                L.px(80 + x, 16 + y, "hg1" if r >= 5.5 else ("hg0" if r >= 4.5 else
                                                              ("hp2" if x + y < 14 else "hp1")))
    s.names = {"h": (0, 0), "v": (1, 0), "ne": (2, 0), "es": (3, 0), "sw": (4, 0), "wn": (5, 0),
               "cross": (6, 0), "start_h": (7, 0), "arrow_n": (0, 1), "arrow_e": (1, 1),
               "arrow_s": (2, 1), "arrow_w": (3, 1), "start_v": (4, 1), "post": (5, 1),
               "slab": (6, 1), "slab2": (7, 1)}
    return s


# --------------------------------------------------------------------------
# Herald-herms
# --------------------------------------------------------------------------

HEADS = {
    # facing south: brows, eyes, the nose, a full beard
    "s": [
        "    kkkkkk    ",
        "   k333333k   ",
        "  k32222223k  ",
        "  k2kk22kk2k  ",
        "  k22222222k  ",
        "  k32212223k  ",
        "   k333333k   ",
        "   k343343k   ",
        "    k3443k    ",
        "     k44k     ",
        "      kk      ",
    ],
    # in profile, facing east: hair behind, the nose and the beard's point forward
    "e": [
        "    kkkkkk    ",
        "   k333222k   ",
        "  k3332222k   ",
        "  k3322kk2k   ",
        "  k332222221k ",
        "  k3322221kk  ",
        "  k332222k    ",
        "   k33322k    ",
        "   k33333k    ",
        "    k333k     ",
        "     kkk      ",
    ],
    # the back of the head: curls
    "n": [
        "    kkkkkk    ",
        "   k333333k   ",
        "  k33333333k  ",
        "  k34343433k  ",
        "  k33434343k  ",
        "  k34343433k  ",
        "   k333333k   ",
        "   k343343k   ",
        "    k3443k    ",
        "     k44k     ",
        "      kk      ",
    ],
}
HEAD_KEY = {"k": "hk", "1": "hw", "2": "hm1", "3": "hm2", "4": "hm3", " ": None}


def _herm_head(M, x0, facing, oiled):
    rows = HEADS["e" if facing in ("e", "w") else facing]
    if facing == "w":
        rows = [r[::-1] for r in rows]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != " ":
                M.px(x0 + 1 + i, 1 + j, HEAD_KEY[ch])
    # the shoulders: the top of the pillar under the head
    M.rect(x0 + 3, 12, 10, 4, "hm0")
    M.vline(x0 + 3, 12, 15, "hk")
    M.vline(x0 + 12, 12, 15, "hk")
    M.vline(x0 + 4, 12, 15, "hw")
    M.vline(x0 + 11, 12, 15, "hm2")
    M.hline(x0 + 3, x0 + 12, 12, "hk")
    if oiled:
        # oil bright on the head and a laurel wreath on the brow
        for (x, y) in ((5, 3), (6, 2), (9, 4), (10, 7), (4, 6)):
            M.px(x0 + x, y, "hg1")
        for i, x in enumerate(range(x0 + 3, x0 + 13)):
            M.px(x, 3 if 4 < i < 6 else 2 + abs(i - 5) // 3, "hl1" if i % 2 else "hl0")
        M.px(x0 + 3, 4, "hl0")
        M.px(x0 + 12, 4, "hl0")


def _herm_shaft(M, x0, scroll, y0=16):
    """The herm's pillar (the cell under its head), its base and contact shadow,
    and the little niche a delivered scroll is left in."""
    M.rect(x0 + 4, y0, 8, 13, "hm0")
    M.vline(x0 + 3, y0, y0 + 12, "hk")
    M.vline(x0 + 12, y0, y0 + 12, "hk")
    M.vline(x0 + 4, y0, y0 + 12, "hw")
    M.vline(x0 + 11, y0, y0 + 12, "hm2")
    M.vline(x0 + 10, y0, y0 + 12, "hm2")
    M.rect(x0 + 2, y0 + 12, 12, 3, "hm2")
    M.hline(x0 + 2, x0 + 13, y0 + 12, "hm0")
    M.hline(x0 + 2, x0 + 13, y0 + 15, "hk")
    M.vline(x0 + 1, y0 + 12, y0 + 14, "hk")
    M.vline(x0 + 14, y0 + 12, y0 + 14, "hk")
    M.hline(x0 + 3, x0 + 12, y0 + 14, "hm3")
    M.rect(x0 + 6, y0 + 3, 4, 6, "hm3")
    M.hline(x0 + 6, x0 + 9, y0 + 3, "hm4")
    if scroll:
        M.blit(["kkkkkk", "k2112r", "kkkkkk"], {"k": "hk", "1": "hw", "2": "hm0", "r": "hr"},
               x0 + 5, y0 + 5)


def herms():
    s = Struct("herm", "Herald-herms: heads that turn, plain and anointed", 8, 2,
               walk=["XXXXXXXX", "XXXXXXXX"],
               notes="The posts the sealed scrolls are delivered to. A herm is a head cell "
                     "over a shaft cell, both blocking. Row 0, the heads: plain, facing "
                     "south, east, north and west, then anointed (oil-bright, a laurel "
                     "wreath) facing the same four ways. An anointed head turned to face "
                     "the next herm is how it 'points the way' (SYSTEMS.md §12). Row 1, the "
                     "shafts: (0) plain, (1) with a delivered scroll in its niche, (2)-(7) "
                     "plain again (any shaft goes under any head). Swap heads and shafts "
                     "with setmetatile; the west heads are the east heads' tiles flipped.")
    for i in range(16):
        floor(s.B, i % 8 * 16, i // 8 * 16)
    for i, (f, o) in enumerate([(f, o) for o in (False, True) for f in "senw"]):
        _herm_head(s.M, i * 16, f, o)
    for i in range(8):
        _herm_shaft(s.M, i * 16, scroll=(i == 1))
    # shadow on the floor east of each shaft (the light is from the top left)
    s.names = {f"head_{'oiled_' if o else ''}{f}": (i, 0)
               for i, (f, o) in enumerate([(f, o) for o in (False, True) for f in "senw"])}
    s.names.update({"shaft": (0, 1), "shaft_scroll": (1, 1)})
    return s


# --------------------------------------------------------------------------
# Turnstiles and gates
# --------------------------------------------------------------------------

def _turnstile(M, x0, d):
    """Hermes's one-way turnstile seen from above-front: three bronze arms on a
    hub, turning on a slim post set in a bronze ring in the floor, and a gold
    chevron on the floor showing the one way it lets you through."""
    t = K.Layer(16, 16)
    # the ring in the floor
    for y in range(16):
        for x in range(16):
            r = math.hypot((x - 7.5) / 5.5, (y - 10.5) / 2.6)
            if 0.82 <= r < 1.12:
                t.px(x, y, "hz1" if y > 10 else "hz2")
    # the post
    for y in range(6, 12):
        t.px(7, y, "hz3")
        t.px(8, y, "hz1")
    # three arms from the hub: back left, back right, and toward the viewer
    for (ax, ay) in ((2, 4), (13, 4), (8, 12)):
        for k in range(12):
            u = k / 11
            x = 7.5 + (ax - 7.5) * u
            y = 6 + (ay - 6) * u
            t.px(int(round(x)), int(round(y)), "hz2")
            t.px(int(round(x)), int(round(y)) + 1, "hz1")
        t.px(ax, ay, "hg1")
    t.blit([" kk ", "kGgk", "kgzk", " kk "], {"k": "hk", "G": "hg1", "g": "hz3", "z": "hz2"}, 6, 4)
    obj = K.Layer(16, 16)
    obj.a[:] = t.a
    E.silhouette_outline(obj, (0, 0, 16, 16), "hk")
    # keep the ring thin: only the arms, post and hub get the outline
    ring = np.zeros((16, 16), bool)
    for y in range(16):
        for x in range(16):
            r = math.hypot((x - 7.5) / 5.5, (y - 10.5) / 2.6)
            ring[y, x] = 0.82 <= r < 1.12
    for y in range(16):
        for x in range(16):
            if ring[y, x] and t.a[y, x, 3]:
                obj.a[y, x] = t.a[y, x]
    m = obj.a[..., 3] > 0
    M.a[0:16, x0:x0 + 16][m] = obj.a[m]
    chev = {"n": ["  G  ", " GgG ", "Gg gG"], "s": ["Gg gG", " GgG ", "  G  "],
            "e": ["G  ", "gG ", " gG", "gG ", "G  "], "w": ["  G", " Gg", "Gg ", " Gg", "  G"]}[d]
    pos = {"n": (5, 0), "s": (5, 13), "e": (13, 1), "w": (0, 1)}[d]
    M.blit(chev, {"G": "hg1", "g": "hz2"}, x0 + pos[0], pos[1])


def _gate(M, x0, orient, shut):
    """A bronze lattice gate in a gap of the balustrade: across an east-west run
    (orient 'h') or a north-south one ('v'), shut or swung open."""
    if orient == "h":
        for x in (0, 1, 14, 15):
            M.vline(x0 + x, 4, 15, "hz1" if x in (1, 14) else "hk")
        M.hline(x0, x0 + 15, 3, "hk")
        if shut:
            for x in range(2, 14):
                for y in range(5, 14):
                    if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                        M.px(x0 + x, y, "hz2")
            M.hline(x0 + 2, x0 + 13, 4, "hz3")
            M.hline(x0 + 2, x0 + 13, 14, "hz1")
            M.px(x0 + 8, 9, "hg1")
        else:
            for y in range(5, 14):
                M.px(x0 + 2, y, "hz2")
                M.px(x0 + 3, y, "hz1" if y % 2 else "hz2")
            M.hline(x0 + 2, x0 + 3, 4, "hz3")
    else:
        for y in (0, 1, 14, 15):
            M.hline(x0 + 5, x0 + 10, y, "hz1" if y in (1, 14) else "hk")
        if shut:
            for y in range(2, 14):
                M.px(x0 + 7, y, "hz2")
                M.px(x0 + 8, y, "hz1")
                if y % 3 == 0:
                    M.hline(x0 + 6, x0 + 9, y, "hz3")
            M.vline(x0 + 6, 2, 13, "hk")
            M.vline(x0 + 9, 2, 13, "hk")
        else:
            for x in range(5, 11):
                M.px(x0 + x, 2, "hz2")
                M.px(x0 + x, 3, "hz1")


def turnstiles():
    s = Struct("turnstile", "One-way turnstiles and lattice gates", 8, 1, walk=["........"],
               notes="(0)-(3) Hermes's turnstiles, each letting you through one way only: the "
                     "gold chevron shows the way (north, east, south, west). The one-way rule "
                     "and the reversing turnstiles of the upper colonnade are scripts (a step "
                     "hook); to reverse one, swap in the opposite direction's metatile. (4)-(7) "
                     "bronze lattice gates in a gap of the balustrade: across an east-west run "
                     "shut (block it) and open, across a north-south run shut and open. Set the "
                     "turnstiles' collision in the scripts' terms; the gates block when shut.")
    for i in range(8):
        floor(s.B, i * 16, 0)
    for i, d in enumerate("nesw"):
        _turnstile(s.M, i * 16, d)
    _gate(s.M, 64, "h", True)
    _gate(s.M, 80, "h", False)
    _gate(s.M, 96, "v", True)
    _gate(s.M, 112, "v", False)
    s.walk = ["....X.X."]
    s.names = {"turn_n": (0, 0), "turn_e": (1, 0), "turn_s": (2, 0), "turn_w": (3, 0),
               "gate_h_shut": (4, 0), "gate_h_open": (5, 0), "gate_v_shut": (6, 0),
               "gate_v_open": (7, 0)}
    return s


# --------------------------------------------------------------------------
# The balustrade
# --------------------------------------------------------------------------

BAL_ORDER = ["NS", "N", "S", "EW", "E", "W", "ES", "SW", "NE", "NW", "NES", "ESW", "NSW", "NEW",
             "NESW", "post"]


def _balustrade(M, x0, arms):
    """A low marble parapet with balusters, its arms reaching the named sides."""
    def ew(xa, xb):
        for x in range(xa, xb + 1):
            M.px(x0 + x, 5, "hk")
            M.px(x0 + x, 6, "hw")
            M.px(x0 + x, 7, "hm0")
            for y in range(8, 14):
                M.px(x0 + x, y, "hm2" if x % 3 == 0 else "hm1")
            M.px(x0 + x, 8, "hm3")
            M.px(x0 + x, 13, "hm3")
            M.px(x0 + x, 14, "hm3")
            M.px(x0 + x, 15, "hk")

    def ns(ya, yb):
        for y in range(ya, yb + 1):
            M.px(x0 + 4, y, "hk")
            M.px(x0 + 5, y, "hw")
            M.px(x0 + 6, y, "hm0")
            M.px(x0 + 7, y, "hm0")
            M.px(x0 + 8, y, "hm1")
            M.px(x0 + 9, y, "hm2")
            M.px(x0 + 10, y, "hm3")
            M.px(x0 + 11, y, "hk")
    if "N" in arms:
        ns(0, 8)
    if "S" in arms:
        ns(8, 15)
    if "W" in arms:
        ew(0, 8)
    if "E" in arms:
        ew(7, 15)
    if arms in ("N", "S", "E", "W", "post") or len(arms) >= 2 and arms not in ("NS", "EW"):
        # a pedestal where the parapet ends or turns
        M.rect(x0 + 4, 4, 8, 11, "hm1")
        M.hline(x0 + 4, x0 + 11, 4, "hw")
        M.hline(x0 + 4, x0 + 11, 5, "hm0")
        M.vline(x0 + 4, 4, 14, "hw")
        M.vline(x0 + 11, 4, 14, "hm3")
        M.hline(x0 + 4, x0 + 11, 14, "hm3")
        M.hline(x0 + 3, x0 + 12, 3, "hk")
        M.hline(x0 + 3, x0 + 12, 15, "hk")
        M.vline(x0 + 3, 3, 15, "hk")
        M.vline(x0 + 12, 3, 15, "hk")
        M.blit(["gG", "Gg"], {"g": "hg0", "G": "hg1"}, x0 + 7, 8)


def balustrade():
    s = Struct("balustrade", "The switchback stoa's balustrade, every join", 8, 2,
               walk=["XXXXXXXX", "XXXXXXXX"],
               notes="A low marble parapet with balusters, for the walls of the switchback "
                     "stoa. Sixteen pieces named by the sides they join (N E S W), so it runs, "
                     "turns, branches and ends anywhere; a gilded pedestal stands at every end "
                     "and turn. Set them all impassable. Pieces: " +
                     ", ".join(f"`{n}` ({i % 8},{i // 8})" for i, n in enumerate(BAL_ORDER)) + ".")
    for i in range(16):
        floor(s.B, i % 8 * 16, i // 8 * 16)
    tmp = Struct("_bal", "", 16, 1)
    for i, arms in enumerate(BAL_ORDER):
        _balustrade(tmp.M, i * 16, "" if arms == "post" else arms)
        if arms == "post":
            _balustrade(tmp.M, i * 16, "post")
    for i in range(16):
        s.M.a[(i // 8) * 16:(i // 8) * 16 + 16, (i % 8) * 16:(i % 8) * 16 + 16] = \
            tmp.M.a[:, i * 16:i * 16 + 16]
    s.names = {n: (i % 8, i // 8) for i, n in enumerate(BAL_ORDER)}
    return s


# --------------------------------------------------------------------------
# Torches, the step-glass, oil
# --------------------------------------------------------------------------

def _flame(M, x, y):
    M.blit(["   f   ", "  fcf  ", " fcycf ", "fcyyycf", " fcycf "],
           {"f": "hf0", "c": "hg1", "y": "hf1"}, x, y)


def props():
    s = Struct("props", "Relay torches, the step-glass and the anointing oil", 5, 2,
               walk=["XXXXX", "XXXXX"],
               notes="(0) a relay torch's bowl, lit, (1) the same cold, over (0,1) its bronze "
                     "stand: the torches of the torch race, lit as the run goes on; swap the "
                     "bowl to light one. (2) the step-glass: a bronze klepsydra, water running "
                     "from its upper bowl to its lower, over (2,1) its stand (Kerykos's glass "
                     "of steps, SYSTEMS.md §12). (3) a stand of anointing oil, a clay lekythos "
                     "on a cedar tripod, one cell, over (3,1) plain floor. (4) a scroll basket "
                     "with sealed scrolls, over (4,1) the same basket emptied.")
    for i in range(10):
        floor(s.B, i % 5 * 16, i // 5 * 16)
    M = s.M
    for x0, lit in ((0, True), (16, False)):
        # the bowl
        M.blit(["kkkkkkkkkk", "kGzzzzzzgk", " kzzzzzzk ", "  kkkkkk  ", "    kk    "],
               {"k": "hk", "G": "hz3", "z": "hz2", "g": "hz1"}, x0 + 3, 9)
        if lit:
            _flame(M, x0 + 4, 4)
            M.px(x0 + 7, 3, "hf0")
        else:
            M.hline(x0 + 5, x0 + 10, 9, "hd0")
            M.px(x0 + 7, 8, "hm3")
    # the torch stand, under either bowl
    for y in range(16, 30):
        M.px(7, y, "hz2")
        M.px(8, y, "hz1")
        M.px(6, y, "hk")
        M.px(9, y, "hk")
    M.blit(["  kkkk  ", " kzzzzk ", "kzzzzzzk", "kkkkkkkk"], {"k": "hk", "z": "hz1"}, 4, 28)
    # the step-glass
    M.blit([" kkkkkkkkkkkk ", "kGzzzzzzzzzzgk", "kzbbbbbbbbbbzk", " kzbbbbbbbbzk ",
            "  kzzbbbbzzk  ", "    kkzzkk    ", "      kb      ", "      kb      "],
           {"k": "hk", "G": "hz3", "z": "hz2", "g": "hz1", "b": "hb1"}, 33, 2)
    M.px(40, 3, "hb2")
    M.px(39, 4, "hw")
    M.blit(["      kb      ", "  kkkkbkkkk   ", " kzzzbbbzzzk  ", " kzbbbbbbbzk  ", "  kzzbbbzzk   ",
            "   kkkkkkk    "], {"k": "hk", "z": "hz2", "b": "hb1"}, 33, 16)
    for y in range(22, 30):
        M.px(36, y, "hz1")
        M.px(43, y, "hz1")
    M.hline(34, 45, 30, "hk")
    M.hline(35, 44, 29, "hz2")
    # the anointing oil: a lekythos on a little tripod
    M.blit(["   kk   ", "   kk   ", "  k22k  ", "  k21k  ", " k2211k ", " k2111k ", " k2111k ",
            "  k11k  ", "  kkkk  ", " k1  1k ", "k1    1k"], {"k": "hk", "2": "hc1", "1": "hc0"}, 52, 3)
    M.px(55, 2, "hy1")
    # scroll baskets, full and empty
    for y0, full in ((0, True), (16, False)):
        M.blit(["  kkkkkkkkkk  ", " kdddddddddk ", "kd1d1d1d1d1dk", "kd1d1d1d1d1dk",
                " kdddddddddk ", "  kkkkkkkkkk  "], {"k": "hk", "d": "hd2", "1": "hd1"}, 65, y0 + 9)
        if full:
            for x in (68, 71, 74):
                M.blit(["kk", "yk", "yr", "yk"], {"k": "hk", "y": "hy1", "r": "hr"}, x, y0 + 5)
    s.names = {"torch_lit": (0, 0), "torch_cold": (1, 0), "torch_stand": (0, 1),
               "glass_top": (2, 0), "glass_stand": (2, 1), "oil": (3, 0), "floor": (3, 1),
               "basket_full": (4, 0), "basket_empty": (4, 1)}
    s.walk = ["XXXXX", "XXX.X"]
    return s


# --------------------------------------------------------------------------
# Pigeonholes and the scroll table
# --------------------------------------------------------------------------

def _cubbies(M, x0, y0, w, h, full=True, gaps=()):
    """Cedar pigeonholes, cells 5 px wide and 4 tall, each with a scroll's end."""
    M.rect(x0, y0, w, h, "hd1")
    E.outline_rect(M, x0, y0, w, h, "hk")
    k = 0
    for yy in range(y0 + 2, y0 + h - 4, 5):
        for xx in range(x0 + 2, x0 + w - 4, 5):
            M.rect(xx, yy, 4, 4, "hd0")
            if full and k not in gaps:
                M.blit([" yy ", "yhhy", "yhry", " yy "], {"y": "hy0", "h": "hy1", "r": "hr"}, xx, yy)
            k += 1
    M.hline(x0 + 1, x0 + w - 2, y0 + 1, "hd2")


def pigeonholes():
    s = Struct("pigeonholes", "Scroll pigeonholes, in the wall and as a cabinet", 6, 2,
               walk=["XXXXXX", "XXXXXX"],
               notes="(0)-(1) pigeonholes set in the wall: put the pair over the frieze and "
                     "lower-wall rows (rows 1-2 of the wall), two cells wide. (2)-(3) a "
                     "free-standing cedar cabinet of pigeonholes, full of sealed scrolls, two "
                     "cells wide by two tall. (4)-(5) the same cabinet with its scrolls taken: "
                     "swap its top row in once the scrolls go out. All impassable.")
    for i in range(12):
        floor(s.B, i % 6 * 16, i // 6 * 16)
    # the wall-set pigeonholes are drawn on the wall's own plaster
    wall_rows(s.B, 0, 32, 1)
    s.B.a[16:32, 0:32] = 0
    wall_rows(s.B, 0, 32, 2, y0=16)
    _cubbies(s.M, 1, 1, 30, 30, full=True, gaps=(4,))
    for x0, full in ((32, True), (64, False)):
        M = s.M
        M.rect(x0 + 1, 2, 30, 4, "hd2")
        M.hline(x0 + 1, x0 + 30, 2, "hk")
        M.hline(x0, x0 + 31, 5, "hk")
        _cubbies(M, x0 + 1, 6, 30, 22, full=full)
        for fx in (x0 + 3, x0 + 26):
            M.rect(fx, 28, 3, 3, "hd0")
            M.hline(fx, fx + 2, 31, "hk")
    s.names = {"wall_tl": (0, 0), "wall_tr": (1, 0), "wall_bl": (0, 1), "wall_br": (1, 1),
               "cab_tl": (2, 0), "cab_tr": (3, 0), "cab_bl": (2, 1), "cab_br": (3, 1),
               "cab_empty_tl": (4, 0), "cab_empty_tr": (5, 0), "cab_empty_bl": (4, 1),
               "cab_empty_br": (5, 1)}
    return s


def table():
    s = Struct("scroll_table", "Kerykos's table of sealed scrolls", 4, 1, walk=["XXXX"],
               notes="(0)-(1) a cedar table laid with sealed scrolls, red wax and ribbons, where "
                     "Kerykos hands them out; (2)-(3) the same table once they're taken.")
    for i in range(4):
        floor(s.B, i * 16, 0)
    for x0, full in ((0, True), (32, False)):
        M = s.M
        M.rect(x0 + 1, 4, 30, 6, "hd2")
        M.hline(x0 + 1, x0 + 30, 4, "hy0")
        M.hline(x0, x0 + 31, 3, "hk")
        M.hline(x0, x0 + 31, 10, "hk")
        M.vline(x0, 3, 10, "hk")
        M.vline(x0 + 31, 3, 10, "hk")
        M.rect(x0 + 1, 11, 30, 2, "hd1")
        for lx in (x0 + 2, x0 + 27):
            M.rect(lx, 11, 3, 4, "hd0")
            M.hline(lx, lx + 2, 15, "hk")
        if full:
            for i, sx in enumerate((x0 + 3, x0 + 12, x0 + 21)):
                M.blit(["kkkkkkk", "kyyyhrk", "kkkkkkk"], {"k": "hk", "y": "hy0", "h": "hy1", "r": "hr"},
                       sx, 3 + (i % 2))
    s.names = {"full_l": (0, 0), "full_r": (1, 0), "empty_l": (2, 0), "empty_r": (3, 0)}
    return s


# --------------------------------------------------------------------------
# Columns, the statue, the rostrum
# --------------------------------------------------------------------------

COLS = ("hm3", "hm2", "hm1", "hm0", "hw")


def columns_and_statue():
    s = Struct("column", "Ionic column and the statue of Hermes", 3, 3,
               walk=["XXX", "XXX", "XXX"],
               notes="(0,0) over (0,1): a free-standing Ionic column, both cells blocking; "
                     "(0,2) a column's base alone, for a broken colonnade. (1,0)-(1,2): the "
                     "statue of Hermes on his plinth, the petasos on his head and the "
                     "caduceus in his hand, three cells tall: flank the rostrum with him. "
                     "(2,0)-(2,2): plain floor, kept to align the sheet.")
    for i in range(9):
        floor(s.B, i % 3 * 16, i // 3 * 16)
    M = s.M
    sh = Struct("_c", "", 1, 2)
    E.shaft(sh.M, 3, 5, 10, 22, ramp=COLS, outline="hk")
    sh.M.rect(1, 0, 14, 2, "hm0")
    sh.M.hline(1, 14, 0, "hk")
    sh.M.hline(2, 13, 1, "hw")
    sh.M.rect(2, 2, 12, 2, "hm1")
    for vx in (0, 13):
        sh.M.blit(["kkk", "kgk", "kkk"], {"k": "hk", "g": "hg0"}, vx, 1)
    sh.M.hline(3, 12, 4, "hm2")
    sh.M.rect(1, 27, 14, 2, "hm1")
    sh.M.hline(1, 14, 27, "hw")
    sh.M.rect(0, 29, 16, 2, "hm2")
    sh.M.hline(0, 15, 31, "hk")
    sh.M.vline(0, 29, 31, "hk")
    sh.M.vline(15, 29, 31, "hk")
    M.a[0:32, 0:16] = sh.M.a
    M.a[32:48, 0:16] = sh.M.a[16:32]
    M.a[32:40, 0:16] = 0
    M.rect(3, 40, 10, 3, "hm1")
    M.hline(3, 12, 40, "hk")
    # the statue of Hermes
    fig = [
        "   kkkkkkkk   ",
        "  kGgggggggk  ",
        " kkkkkkkkkkkk ",
        "    k1111k    ",
        "    k1k1kk    ",
        "    k1111k    ",
        "     k11k     ",
        "   kk1111kk   ",
        "  k11111111k G",
        "  k1k1111k1kGg",
        "  k1k1111k1k g",
        "  k1k1111kk1kg",
        "  kk111111k  g",
        "   k111111k  g",
        "   k111111k  g",
        "   k11kk11k  g",
        "   k11kk11k   ",
        "  kG1k  k1Gk  ",
        "  kkkk  kkkk  ",
    ]
    M.blit(fig, {"k": "hk", "1": "hm0", "G": "hg1", "g": "hg0"}, 17, 6)
    # wings on the petasos
    M.blit(["k", "Gk", "gG"], {"k": "hk", "G": "hg1", "g": "hg0"}, 17, 3)
    M.blit([" k", "kG", "Gg"], {"k": "hk", "G": "hg1", "g": "hg0"}, 29, 3)
    # the plinth
    M.rect(18, 26, 12, 20, "hm1")
    M.hline(17, 30, 25, "hk")
    M.hline(18, 29, 26, "hw")
    M.vline(17, 25, 46, "hk")
    M.vline(30, 25, 46, "hk")
    M.vline(18, 27, 45, "hw")
    M.vline(29, 27, 45, "hm2")
    M.hline(17, 30, 46, "hk")
    M.hline(18, 29, 45, "hm3")
    M.blit(["  G  ", "GgGgG", "  G  "], {"G": "hg1", "g": "hg0"}, 21, 34)
    s.walk = ["XX.", "XX.", "XX."]
    s.names = {"col_top": (0, 0), "col_bot": (0, 1), "col_base": (0, 2), "statue_top": (1, 0),
               "statue_mid": (1, 1), "statue_bot": (1, 2)}
    return s


def rostrum():
    s = Struct("rostrum", "The herald's rostrum: platform, risers, steps, lectern", 8, 2,
               walk=["...XX.X.", "XXX....."],
               notes="A raised marble platform at the head of the stoa's steps, for Kerykos "
                     "and for the upper colonnade. Row 0: (0) the platform's floor, (1) the "
                     "same with a gold-and-blue winged roundel for under Kerykos, (2) its front "
                     "lip with a gold key (walkable), (3) its west edge and (4) east edge "
                     "(block them, so no one climbs on from the side), (5) the lectern, "
                     "MB_COUNTER: Kerykos stands north of it and the player speaks across it, "
                     "(6) the platform's floor with a cold lampstand, (7) the stair's head. Row "
                     "1: (0) the riser's face, (1) its west and (2) east corners (all block), "
                     "(3) steps climbing north through the riser (walkable), (4)-(7) a winged "
                     "caduceus mosaic for the hall's floor, a 2x2 roundel laid as (4) (5) over "
                     "(6) (7).")
    L, M = s.B, s.M

    def dais(x0, y0):
        # the platform is floored like the hall, so every object stands on either;
        # its gold lip, riser and edges show the height
        floor(L, x0, y0)
    for i in range(8):
        dais(i * 16, 0)
    # (1) the roundel
    for y in range(16):
        for x in range(16):
            r = math.hypot(x - 7.5, y - 7.5)
            if r < 7:
                L.px(16 + x, y, "hg0" if r >= 6 else "hb1" if r >= 4.5 else "hg1" if r < 1.5 else "hb0")
    L.blit(["G       G", " Gg   gG ", "  GgggG  "], {"G": "hg1", "g": "hg0"}, 19, 6)
    # (2) the front lip
    for x in range(32, 48):
        L.px(x, 12, "hk")
        L.px(x, 13, "hg1" if x % 4 in (0, 1) else "hg0")
        L.px(x, 14, "hg0" if x % 4 in (0, 1) else "hg1")
        L.px(x, 15, "hm2")
    # (3), (4) the side edges
    for y in range(16):
        L.px(48, y, "hk")
        L.px(49, y, "hm2")
        L.px(50, y, "hm3")
        L.px(79, y, "hk")
        L.px(78, y, "hm3")
        L.px(77, y, "hm2")
    # (5) the lectern
    M.blit([
        "kkkkkkkkkkkkkkkk",
        "kwwwwwwwwwwwwwwk",
        "k00000000000000k",
        "kkkkkkkkkkkkkkkk",
        " k111111111111k ",
        " k1GgggggggggG1k",
        " k1g        g1k ",
        " k1g G    G g1k ",
        " k1g  GggG  g1k ",
        " k1g        g1k ",
        " k1GgggggggggG1k",
        " k111111111111k ",
        " k222222222222k ",
        " kkkkkkkkkkkkkk ",
    ], {"k": "hk", "w": "hw", "0": "hm0", "1": "hm1", "2": "hm2", "G": "hg1", "g": "hg0"}, 80, 1)
    # (6) a lampstand, cold
    for y in range(4, 15):
        M.px(103, y, "hz1")
        M.px(104, y, "hz2")
    M.blit(["kkkkk", " kzk "], {"k": "hk", "z": "hz2"}, 101, 2)
    M.blit(["k kk k", "kkkkkk"], {"k": "hk"}, 101, 14)
    # (7) the stair's head: the top tread
    for x in range(112, 128):
        L.px(x, 13, "hm1")
        L.px(x, 14, "hm2")
        L.px(x, 15, "hm3")
    # row 1: the riser (0), its corners (1), (2), the steps (3)
    for x in range(64):
        for y in range(16, 32):
            Y = y - 16
            c = "hm1" if Y < 13 else "hm2"
            if Y == 0:
                c = "hw"
            if Y in (5, 10):
                c = "hm2"
            if Y == 15:
                c = "hk"
            L.px(x, y, c)
    for x0 in (16, 32):
        lit = x0 == 16
        L.vline(x0 + (0 if lit else 15), 16, 31, "hk")
        L.vline(x0 + (1 if lit else 14), 16, 30, "hw" if lit else "hm3")
    for k in range(3):
        y = 16 + k * 5
        L.rect(48, y, 16, 5, "hm0")
        L.hline(48, 63, y, "hw")
        L.hline(48, 63, y + 3, "hm1")
        L.hline(48, 63, y + 4, "hm3")
    L.hline(48, 63, 31, "hm2")
    # (4)-(7) the winged caduceus mosaic, a 2x2 roundel, mirrored
    # drawn into a scratch 32x32, then its quadrants placed
    q = K.Layer(32, 32)
    for y in range(32):
        for x in range(32):
            r = math.hypot(x - 15.5, y - 15.5)
            c = "hm0" if (x // 4 + y // 4) % 2 else "hw"
            if r >= 15.5:
                c = "hm1"
            elif r >= 14:
                c = "hb0"
            elif r >= 13:
                c = "hg1"
            elif r >= 12:
                c = "hb1"
            q.px(x, y, c)
    for i in range(14):
        h = 1 + (i * 4) // 14
        for j in range(h):
            q.px(15 - i, 15 - j - (14 - i) // 4, "hg1" if j < h - 1 else "hg0")
    for y in range(6, 27):
        q.px(15, y, "hg0")
    q.blit(["kGk", "GkG", "kgk"], {"k": "hb0", "G": "hg1", "g": "hg0"}, 14, 5)
    q.blit(["G G", " g ", "g g", " G "], {"G": "hg1", "g": "hg0"}, 13, 12)
    E.mirror_half(q, 0, 32, 0, 32)
    L.a[16:32, 64:80] = q.a[0:16, 0:16]
    L.a[16:32, 80:96] = q.a[0:16, 16:32]
    L.a[16:32, 96:112] = q.a[16:32, 0:16]
    L.a[16:32, 112:128] = q.a[16:32, 16:32]
    s.behaviors[(5, 0)] = "MB_COUNTER"
    s.names = {"dais": (0, 0), "dais_roundel": (1, 0), "dais_lip": (2, 0), "edge_w": (3, 0),
               "edge_e": (4, 0), "lectern": (5, 0), "dais_lamp": (6, 0), "stair_head": (7, 0),
               "riser": (0, 1), "riser_w": (1, 1), "riser_e": (2, 1), "steps": (3, 1),
               "mosaic_tl": (4, 1), "mosaic_tr": (5, 1), "mosaic_bl": (6, 1), "mosaic_br": (7, 1)}
    return s


# --------------------------------------------------------------------------
# Walls and the doormat
# --------------------------------------------------------------------------

FRIEZE = {
    "wings": ["bbbbbbbbbbbbbbbb", "bGbbbbbbbbbbbbGb", "bGGbbbbbbbbbbGGb", "bbGGGbbbbbbGGGbb",
              "bbbGGGGggGGGGbbb", "bbbbgggGGgggbbbb", "bbbbbbbggbbbbbbb", "bbbbbbbbbbbbbbbb"],
    "caduceus": ["bbbbbbbGGbbbbbbb", "bbbbGGbgGbGGbbbb", "bbbbbgGgGGgbbbbb", "bbbbbbbgGbbbbbbb",
                 "bbbbbbGgGGbbbbbb", "bbbbbGbgGbGbbbbb", "bbbbbbGgGGbbbbbb", "bbbbbbbgGbbbbbbb"],
    "petasos": ["bbbbbbbbbbbbbbbb", "bbGbbbbGGbbbbGbb", "bbGGbbGggGbbGGbb", "bbbGGGggggGGGbbb",
                "bbbbGGGGGGGGbbbb", "bbbGGGGGGGGGGbbb", "bbbbbbbbbbbbbbbb", "bbbbbbbbbbbbbbbb"],
    "talaria": ["bbbbbbbbbbbbbbbb", "bbbbGbbbbbbbbbbb", "bbbGGbbbbbbbbbbb", "bbGGgwwwwbbbbbbb",
                "bbbbgwwwwwwwbbbb", "bbbbbwwwwwwwwwbb", "bbbbbbbbbbbbbbbb", "bbbbbbbbbbbbbbbb"],
    "lyre": ["bbbbbbbbbbbbbbbb", "bbbbbGbbbbGbbbbb", "bbbbbGbbbbGbbbbb", "bbbbbGGGGGGbbbbb",
             "bbbbbGwbwbGbbbbb", "bbbbGwwwwwwGbbbb", "bbbbbGwwwwGbbbbb", "bbbbbbGGGGbbbbbb"],
    "runner_l": ["bbbbbbbbbbbbbbbb", "bbbbbbbbbbbbbGGb", "bbbbbbbbbbbbGkkG", "bbbbbbbbbbbbbkkb",
                 "bbbbbbbbGGgggkkk", "bbbbbbbbbbbbbkkk", "bbbbbbbbbbbbkbbk", "bbbbbbbbbbbkbbbk"],
    "runner_r": ["bbbbbbbbbbbbbbbb", "bbbbbbbbbbbbbbbb", "bbbbbbbbbbbbbbbb", "kkbbbbbbbbbbbbbb",
                 "kbkbbbbbbbbbbbbb", "kbbkbbbbbbbbbbbb", "bbbbkbbbbbbbbbbb", "bbbbbkbbbbbbbbbb"],
}


def wall_rows(L, x0, w, row, y0=0):
    """The three rows of a wall, for cells x0..x0+w-1: 0 the cornice under the
    roof's shadow, 1 the frieze's ground (blue between marble fillets), 2 the
    lower wall (marble panels over a blue dado)."""
    for y in range(16):
        for x in range(x0, x0 + w):
            X = x % 16
            if row == 0:
                c = "hm4" if y < 5 else "hk" if y == 5 else "hw" if y == 6 else \
                    "hm0" if y == 7 else ("hm2" if X % 4 in (1, 2) else "hm0") if y in (8, 9) else \
                    "hm1" if y < 13 else "hm2" if y < 15 else "hm3"
                if y < 5 and (X + y) % 8 == 0:
                    c = "hk"
            elif row == 1:
                c = "hm0" if y in (0, 15) else "hw" if y == 1 else "hm2" if y == 14 else "hb0"
            else:
                c = "hm1"
                if y == 0:
                    c = "hm2"
                elif y == 1:
                    c = "hw"
                elif X in (1, 14) and 3 <= y <= 9:
                    c = "hm2"
                elif 2 <= X <= 13 and y in (3, 9):
                    c = "hm2"
                elif y in (10, 11):
                    c = "hb1" if y == 10 else "hb0"
                elif y >= 12:
                    c = "hm2" if y < 15 else "hm3"
            L.px(x, y0 + y, c)


def walls():
    s = Struct("wall", "Walls: cornice, the winged frieze, the lower wall, the doormat", 8, 4,
               walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXX...."],
               notes="A room shows three wall rows: the cornice (row 0 of the map), the frieze, "
                     "then the lower wall. Row 0: cornice, its west and east corners, the side "
                     "walls' tops (west, east) for the map's edges, the void's border, and two "
                     "cornice variants with a gilded acroterion. Row 1, the frieze: gold on "
                     "Aegean blue: spread wings, the caduceus, the petasos, the winged sandals, "
                     "the tortoise lyre, Hermes running (two cells, left then right), and the "
                     "plain blue band. Row 2, the lower wall: plain, a wall torch burning, a "
                     "niche with a little herm bust, a plaque, and the side walls' faces. Row 3: "
                     "the doormat (west, middle, east, single; MB_SOUTH_ARROW_WARP: put it on "
                     "the map's bottom row with warps), and four more plain lower walls.")
    L, M = s.B, s.M
    wall_rows(L, 0, 128, 0, 0)
    # corners and side walls (row 0 cells 1, 2, 3, 4; row 2 cells 6, 7)
    for x0, west in ((16, True), (32, False)):
        for y in range(16):
            L.px(x0 + (0 if west else 15), y, "hk")
            L.px(x0 + (1 if west else 14), y, "hm2")
    for x0, west in ((48, True), (64, False)):
        for y in range(16):
            for x in range(16):
                L.px(x0 + x, y, "hm4" if (x < 10 if west else x > 5) else "hk")
            L.px(x0 + (10 if west else 5), y, "hm2")
            L.px(x0 + (11 if west else 4), y, "hm0")
    L.rect(80, 0, 16, 16, "hk")
    for x0 in (96, 112):
        M.blit(["   kk   ", "  kGGk  ", " kGggGk ", "kGgkkgGk"], {"k": "hk", "G": "hg1", "g": "hg0"},
               x0 + 4, 0)
    # row 1: the frieze
    wall_rows(L, 0, 128, 1, 16)
    for i, k in enumerate(("wings", "caduceus", "petasos", "talaria", "lyre", "runner_l",
                           "runner_r")):
        L.blit(FRIEZE[k], {"b": "hb0", "G": "hg1", "g": "hg0", "w": "hw", "k": "hk"},
               i * 16, 20)
    # row 2: the lower wall
    wall_rows(L, 0, 128, 2, 32)
    # a wall torch burning in its bronze sconce (cell 1)
    M.blit(["   f   ", "  fcf  ", " fcycf ", " fcycf ", "kkkkkkk", " kzzzk ", "  kzk  ", "  kzk  "],
           {"f": "hp2", "c": "hg1", "y": "hw", "k": "hk", "z": "hg0"}, 20, 32)
    # a niche with a herm bust (cell 2)
    L.rect(36, 34, 8, 10, "hm3")
    L.hline(36, 43, 34, "hm4")
    M.blit(["  kk  ", " kppk ", "kpkkpk", "kpprpk", " kppk ", "  kk  "], {"k": "hk", "p": "hp1", "r": "hr"},
           37, 37)
    # a plaque (cell 3)
    L.rect(52, 34, 8, 6, "hw")
    for x in range(53, 59, 2):
        L.px(x, 36, "hm3")
        L.px(x, 38, "hm3")
    # side walls' faces (cells 6, 7)
    for x0, west in ((96, True), (112, False)):
        for y in range(32, 48):
            for x in range(16):
                if (x < 10 if west else x > 5):
                    L.px(x0 + x, y, "hm4")
            L.px(x0 + (10 if west else 5), y, "hm2")
            L.px(x0 + (11 if west else 4), y, "hm0")
    # row 3: the doormat (woven rush), then plain lower walls
    for x0 in range(0, 64, 16):
        for y in range(48, 64):
            for x in range(16):
                L.px(x0 + x, y, "hy0" if (x + y) % 3 else "hy1")
        for x in range(x0, x0 + 16):
            L.px(x, 50, "hd1")
            L.px(x, 61, "hd1")
    for x0, left, right in ((0, True, False), (16, False, False), (32, False, True),
                            (48, True, True)):
        if left:
            L.vline(x0 + 1, 50, 61, "hd1")
        if right:
            L.vline(x0 + 14, 50, 61, "hd1")
    wall_rows(L, 64, 64, 2, 48)
    s.walk = ["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "....XXXX"]
    for i in range(4):
        s.behaviors[(i, 3)] = "MB_SOUTH_ARROW_WARP"
    s.names = {"cornice": (0, 0), "cornice_w": (1, 0), "cornice_e": (2, 0), "side_w": (3, 0),
               "side_e": (4, 0), "void_wall": (5, 0), "cornice_acro": (6, 0),
               "frieze_wings": (0, 1), "frieze_caduceus": (1, 1), "frieze_petasos": (2, 1),
               "frieze_talaria": (3, 1), "frieze_lyre": (4, 1), "frieze_runner_l": (5, 1),
               "frieze_runner_r": (6, 1), "frieze": (7, 1),
               "lower": (0, 2), "lower_torch": (1, 2), "lower_niche": (2, 2), "lower_plaque": (3, 2),
               "side_face_w": (6, 2), "side_face_e": (7, 2),
               "mat_l": (0, 3), "mat_m": (1, 3), "mat_r": (2, 3), "mat_single": (3, 3)}
    return s


def build():
    out = [floors(), lanes(), walls(), herms(), turnstiles(), balustrade(), props(),
           pigeonholes(), table(), columns_and_statue(), rostrum()]
    for s in out:
        E.finish(s)
    return [(0, out)]


def write_catalog(used, structs):
    import temple_hermes_catalog
    temple_hermes_catalog.main(used, structs)
