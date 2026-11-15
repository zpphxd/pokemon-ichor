"""The pieces of the four places: the Kronion Crypt and the sea grottos.

Two wall styles join the cave's own:

  crypt  Kronion's rock-cut room under the hill: the cave's rock recolored
         to poros (it shares the cave's tiles under its own palette), with
         cut faces of its own: a cornice, a painted band and ashlar courses,
         over a floor of slabs.
  wet    the sea grottos: the cave's rock and faces recolored to wet,
         weed-dark stone (sharing the cave's tiles), plus a seep and a weedy
         tide line among the faces.

Style cells are keyed '<style>:<kit key>'; the build files them under
catalog["styles"], and the autotiler looks there first.
"""
from __future__ import annotations

import math

import numpy as np

import cave_dark_kit as kit
import cave_dark_props as props
from cave_dark_lib import POROS, WET, C, Layer, Struct, one
from cave_dark_props import ellipse_mask, on_floor, shade, shadow


def recolor(arr, table):
    L = Layer(arr.shape[1], arr.shape[0])
    L.a[:] = arr
    L.recolor(table)
    return L.a


# --------------------------------------------------------------------------
# The crypt: cut faces, slab floor
# --------------------------------------------------------------------------

CRYPT_C = {"x": "k0", "k": "sk", "0": "s0", "1": "s1", "2": "s2", "3": "s3", "4": "s4", "5": "s5",
           "t": "tc", "o": "ochre", "e": "e1"}
DARKER = {"5": "4", "4": "3", "3": "2", "2": "1", "1": "0", "0": "k", "k": "k", "t": "e", "o": "t",
          "e": "0", "x": "x"}
LIGHTER = {"k": "0", "0": "1", "1": "2", "2": "3", "3": "4", "4": "5", "5": "5", "t": "o", "e": "t",
           "o": "o", "x": "x"}

# Rows 2-31 of the two ashlar strips. A starts the lower course's block, B
# the upper's, so the courses stagger by 8 px.
ASHLAR = {
    "A": ["xxxxxxxx", "55555555", "44444444", "22222222", "11111111", "34444443", "tttttttt",
          "22222222", "33433343", "34333433", "33343334", "33433343", "34333433", "22222222",
          "14444444", "14333333", "14333333", "14333433", "14333333", "12222222", "11111111",
          "44444442", "33333332", "33343332", "33333332", "22222222", "11111111", "22222222",
          "kkkkkkkk", "xxxxxxxx"],
    "B": ["xxxxxxxx", "55555555", "44444444", "22222222", "11111111", "34444443", "tttttttt",
          "22222222", "34333433", "33343334", "33433343", "34333433", "33343334", "22222222",
          "44444442", "33333332", "33333332", "33343332", "33333332", "22222222", "11111111",
          "14444444", "14333333", "14333433", "14333333", "12222222", "11111111", "22222222",
          "kkkkkkkk", "xxxxxxxx"],
}
for _r in ASHLAR.values():
    assert len(_r) == 30 and all(len(x) == 8 for x in _r)


def ashlar(variant, x0=0):
    """8x32 strip of the crypt's cut face. variant: 'A', 'B', 'end' or 'inner'
    with a side, e.g. ('end', 'w')."""
    if isinstance(variant, tuple):
        kind, side = variant
        rows = [list(r) for r in ASHLAR["A" if side == "w" else "B"]]
        for r in rows[1:]:
            if kind == "end" and side == "w":
                r[0], r[1] = "x", LIGHTER[LIGHTER[r[1]]] if r[1] not in "x" else r[1]
            elif kind == "end":
                r[7], r[6], r[5] = "x", DARKER[DARKER[r[6]]], DARKER[r[5]]
            elif side == "w":
                r[0], r[1], r[2] = "k", DARKER[DARKER[r[1]]], DARKER[r[2]]
            else:
                r[7], r[6] = "k", DARKER[DARKER[r[6]]]
        rows = ["".join(r) for r in rows]
    else:
        kind, side, rows = variant, None, ASHLAR[variant]
    L = Layer(8, 32)
    for y in range(32):
        for x in range(8):
            if y < 2:
                if kind == "end":
                    if side == "w":
                        d = x + 0.5 - kit.wob16(y, 7) * 0.6
                        ramp = kit.RAMP_W
                    else:
                        d = 8 - (x + 0.5) - kit.wob16(y, 11) * 0.6
                        ramp = kit.RAMP_E
                    c = ramp[max(0, int(d))] if d < kit.RIM else kit.tex(kit.MASS, kit.MASS_C, x0 + x, y)
                else:
                    c = kit.tex(kit.MASS, kit.MASS_C, x0 + x, y)
                c = POROS[c]
            else:
                c = CRYPT_C[rows[y - 2][x]]
            L.px(x, y, c)
    return L.a


def crypt_face(kind, left, right):
    out = np.zeros((16, 16, 4), np.uint8)
    y0 = 0 if kind == "ft" else 16
    for half, st, side in ((0, left, "w"), (1, right, "e")):
        v = (st, side) if st in ("end", "inner") else st
        out[:, half * 8:half * 8 + 8] = ashlar(v, half * 8)[y0:y0 + 16]
    return out


# Big worn flagstones: a quiet joint, a lit edge, a few pits and stains.
SLABS = [
    "1111111111111111",
    "1333333333333332",
    "1322222222222222",
    "1322222222221222",
    "1322222222222222",
    "1322212222222222",
    "1322222222222222",
    "1322222222222222",
    "1322222222222222",
    "1322222222222122",
    "1322222222222222",
    "1322221222222222",
    "1322222222222222",
    "1322222222222222",
    "1222222222222222",
    "1222222222222222",
]
SLABS2 = [
    "1111111111111111",
    "1333333333333332",
    "1322222222222222",
    "1322222222222222",
    "1322222222212222",
    "1322222222122222",
    "1322222221222222",
    "1322222212222222",
    "1322222122222222",
    "1322222122222222",
    "1322221222222222",
    "1322212222222222",
    "1322222222222122",
    "1322222222222222",
    "1222222222222222",
    "1222222222222222",
]
SLAB_C = {"0": "s0", "1": "s1", "2": "s2", "3": "s3"}


def crypt_floor(N=False, W=False, nw=False, rows=None):
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            c = SLAB_C[(rows or SLABS)[y][x]]
            d = 99
            if N:
                d = min(d, y)
            if W:
                d = min(d, x)
            if nw:
                d = min(d, int(math.hypot(x + 0.5, y + 0.5)))
            if d == 0:
                c = "sk"
            elif d == 1:
                c = "s0"
            elif d == 2 and (x + y) % 2 == 0:
                c = "s1"
            L.px(x, y, c)
    return L.a


CRYPT_FLOOR = crypt_floor()


def crypt_style():
    out = []
    for key, (N, W, E, nubs) in kit.mass_keys():
        if len(nubs) > 1:
            continue
        out.append(one(f"crypt:{key}", key, "places", {"bottom": recolor(kit.mass_cell(N, W, E, nubs), POROS)},
                       walk="X"))
    for kind in ("ft", "fb"):
        for l in ("A", "end", "inner"):
            for r in ("B", "end", "inner"):
                key = f"{kind}|{l}|{r}"
                out.append(one(f"crypt:{key}", key, "places", {"bottom": crypt_face(kind, l, r)}, walk="X"))
    for N, W, nw in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1)):
        key = kit.floor_key(bool(N), bool(W), bool(nw))
        out.append(one(f"crypt:{key}", key, "places", {"bottom": crypt_floor(N, W, nw)}, walk=".",
                       floor_mb="MB_CAVE"))
    key = kit.floor_key(False, False, False, True)
    out.append(one(f"crypt:{key}", key, "places", {"bottom": crypt_floor(rows=SLABS2)}, walk=".",
                   floor_mb="MB_CAVE"))
    return out


# --------------------------------------------------------------------------
# The crypt's pieces
# --------------------------------------------------------------------------

def crypt_stair():
    """2x2 in the north face: steps cut up through the rock to the hill above."""
    face = np.concatenate([np.concatenate([crypt_face("ft", "A", "B"), crypt_face("ft", "A", "B")], 1),
                           np.concatenate([crypt_face("fb", "A", "B"), crypt_face("fb", "A", "B")], 1)], 0)
    L = Layer(32, 32)
    L.a[:] = face
    x0, x1 = 6, 26
    # the cut: jambs, a lintel, and the treads climbing toward daylight
    for y in range(5, 32):
        L.px(x0 - 1, y, "k0"), L.px(x1, y, "k0")
        L.px(x0 - 2, y, "s5" if y > 6 else "s4"), L.px(x1 + 1, y, "s1")
    for x in range(x0 - 2, x1 + 2):
        L.px(x, 4, "k0"), L.px(x, 5, "s5"), L.px(x, 6, "s3")
    treads = [(7, "s5", "s5"), (10, "s5", "s4"), (13, "s4", "s3"), (16, "s4", "s2"), (19, "s3", "s2"),
              (22, "s3", "s1"), (25, "s2", "s1"), (28, "s2", "s0")]
    y = 7
    for top, tread, riser in treads:
        for yy in range(top, top + 3):
            for x in range(x0, x1):
                L.px(x, yy, tread if yy == top else riser if yy == top + 2 else tread)
        for x in range(x0, x1):
            L.px(x, top + 2, "s1" if top > 12 else "s3")
    for yy in range(7, 10):
        for x in range(x0, x1):
            L.px(x, yy, "s5")
    for x in range(x0, x1):
        L.px(x, 31, "s0")
    return L.a


def sarcophagus():
    """3x2: an old poros sarcophagus with a gabled lid and a painted band."""
    L = Layer(48, 32)
    lid = np.zeros((32, 48), bool)
    lid[3:15, 2:46] = True
    body = np.zeros((32, 48), bool)
    body[15:29, 3:45] = True
    shadow(L, lid | body, 0, 0, c="sk", dx=2, dy=1)
    shade(L, body, ramp=["s4", "s3", "s3", "s2", "s2", "s1"], hi=(0.15, 0.2))
    # the gabled lid: the ridge runs along its length
    for y in range(3, 15):
        for x in range(2, 46):
            c = "s5" if y < 8 else ("s3" if y < 9 else "s2")
            if y == 8:
                c = "s4"
            L.px(x, y, c)
    for x in range(2, 46):
        L.px(x, 2, "k0"), L.px(x, 15, "k0"), L.px(x, 14, "s1")
    for y in range(3, 15):
        L.px(1, y, "k0"), L.px(46, y, "k0")
    # acroteria at the corners
    for x in (2, 3, 44, 45):
        L.px(x, 3, "s5"), L.px(x, 4, "s4")
    L.px(2, 2, "s4"), L.px(45, 2, "s3")
    # the painted band on the chest: a red meander on ochre
    for x in range(4, 44):
        L.px(x, 18, "ochre")
        L.px(x, 19, "tc" if x % 4 in (0, 1) else "ochre")
        L.px(x, 20, "tc" if x % 4 == 0 else "ochre")
        L.px(x, 21, "tc")
    for x in range(3, 45):
        L.px(x, 28, "s1"), L.px(x, 29, "k0")
    for y in range(15, 29):
        L.px(2, y, "k0"), L.px(45, y, "k0")
    props.mirror_left(L)
    return L.a


def altar_stone():
    """2x1: a rough block with a hollow for libations, stained dark."""
    L = Layer(32, 16)
    top = np.zeros((16, 32), bool)
    top[2:8, 3:29] = True
    front = np.zeros((16, 32), bool)
    front[8:14, 3:29] = True
    shadow(L, top | front, 0, 0, c="sk")
    shade(L, front, ramp=["s3", "s2", "s2", "s1", "s1", "s0"], outline=None)
    shade(L, top, ramp=["s5", "s4", "s4", "s3", "s3"], outline=None)
    hole = ellipse_mask(32, 16, 16, 5, 6, 1.8)
    for y, x in zip(*np.nonzero(hole)):
        L.px(x, y, "sk" if y > 4 else "s0")
    for x, y in ((11, 8), (12, 9), (12, 10), (19, 8), (19, 9), (20, 11)):
        L.px(x, y, "e1")
    allm = top | front
    pad = np.pad(allm, 1)
    edge = allm & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "k0")
    for x in range(4, 28):
        L.px(x, 8, "s2")
    return L.a


RELIEF = [
    "................................",
    "................................",
    "...................55...........",
    "..................5443..........",
    "..55.............543332.........",
    ".5443............4x1x32.........",
    ".4332...........43000032........",
    ".43x2..........4300k00332.......",
    "..32...........4300000032.......",
    ".5443..553......4300003332......",
    "54333.54433......43333333332....",
    "4332254333332.....4333333332....",
    "43322433222332...5433333332.....",
    "43322.4322.433..54333333332.....",
    "4332...432..4335433333333332....",
    "4332...4322.5443333333333332....",
    "4322...43322.4333333333333332...",
    "4322...4333..433333333333332....",
    "4322..43332...433333333332......",
    "4322..43332...43333333332.......",
    "43322.433332..43333333332.......",
    "433322433332..433333333332......",
    ".222222222222..2222222222222....",
    "................................",
]


def relief():
    """2x2 in a face: Rhea hands Kronos a stone in swaddling; he opens wide."""
    face = np.concatenate([np.concatenate([crypt_face("ft", "A", "B"), crypt_face("ft", "A", "B")], 1),
                           np.concatenate([crypt_face("fb", "A", "B"), crypt_face("fb", "A", "B")], 1)], 0)
    L = Layer(32, 32)
    L.a[:] = face
    # the sunk panel
    for y in range(8, 30):
        for x in range(2, 30):
            L.px(x, y, "s2")
    for x in range(2, 30):
        L.px(x, 7, "s0"), L.px(x, 30, "s4")
    for y in range(7, 31):
        L.px(1, y, "s0"), L.px(30, y, "s4")
    L.blit(RELIEF, {"5": "s5", "4": "s4", "3": "s3", "2": "s1", "0": "s0", "k": "sk", "x": "k0"}, 0, 7)
    return L.a


def dig(crypt=False):
    """A fixed dig spot: turned earth and a few stones (Alethea's Trowel)."""
    L = Layer(16, 16)
    m = ellipse_mask(16, 16, 8, 8.5, 6.5, 5)
    pal = (["s0", "s1", "e1", "s2", "s3"] if crypt else ["f1", "f2", "f3", "f4", "f5"])
    for y, x in zip(*np.nonzero(m)):
        L.px(x, y, pal[(x * 7 + y * 3) % 3])
    for x, y in ((5, 6), (9, 8), (7, 11), (11, 10)):
        L.px(x, y, pal[4]), L.px(x + 1, y, pal[3]), L.px(x + 1, y + 1, pal[0])
    for x in range(3, 13):
        L.px(x, 13, pal[0])
    return L.a


def crypt_pieces():
    out = []
    s = Struct("crypt_stair", "The crypt's stair up to Kronion Hill", 2, 2, "places", walk=["XX", "^^"],
               notes="2x2 in the crypt's north face. The bottom row is the way out: "
                     "MB_NORTH_ARROW_WARP, to the dig pit on Kronion Hill.")
    s.B.a[:] = crypt_stair()
    out.append(s)
    s = Struct("crypt_relief", "The relief: Rhea's stone for Kronos", 2, 2, "places", walk=["XX", "XX"],
               notes="2x2 in a crypt face. Give it a bg event with the relief's text (SCRIPT.md).")
    s.B.a[:] = relief()
    out.append(s)
    out.append(on_floor("sarcophagus", "Sarcophagus", 3, 2, ["XXX", "XXX"], sarcophagus(), section="places",
                        ground=CRYPT_FLOOR, notes="Old poros, the lid a little askew."))
    out.append(on_floor("altar_stone", "Altar stone", 2, 1, ["XX"], altar_stone(), section="places",
                        ground=CRYPT_FLOOR, notes="A rough block with a libation hollow."))
    out.append(on_floor("dig_crypt", "Dig spot, on the slabs", 1, 1, ["."], dig(True), section="places",
                        ground=CRYPT_FLOOR, notes="The crypt's fixed dig (a Kronos sherd)."))
    out.append(on_floor("dig", "Dig spot", 1, 1, ["."], dig(False), section="places",
                        notes="A fixed dig in a cave or grotto floor."))
    return out


# --------------------------------------------------------------------------
# The sea grottos
# --------------------------------------------------------------------------

WET_FACES = (["A", "wet", "end", "inner"], ["C", "weed", "end", "inner"])


def wet_style():
    out = []
    for key, (N, W, E, nubs) in kit.mass_keys():
        if len(nubs) > 1:
            continue
        out.append(one(f"wet:{key}", key, "places", {"bottom": recolor(kit.mass_cell(N, W, E, nubs), WET)},
                       walk="X"))
    for kind in ("ft", "fb"):
        for l in WET_FACES[0]:
            for r in WET_FACES[1]:
                key = f"{kind}|{l}|{r}"
                out.append(one(f"wet:{key}", key, "places",
                               {"bottom": recolor(kit.face_cell(kind, l, r), WET)}, walk="X"))
    return out


def boat():
    """3x2: a fisher's boat, moored and very still: bow west with its painted
    eye, a square stern, two thwarts and an oar shipped along the side."""
    L = Layer(48, 32)
    x0, x1, cy, half = 4, 44, 14.5, 8.0
    deck = np.zeros((32, 48), bool)      # what we see from above, inside the gunwale
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        if t < 0.35:
            v = half * (t / 0.35) ** 0.6       # the bow narrows to a point
        elif t > 0.9:
            v = half * 0.85                     # a squared stern
        else:
            v = half
        deck[int(round(cy - v)):int(round(cy + v)), x] = True
    side = np.zeros_like(deck)            # the near side of the hull, below the gunwale
    for x in range(x0, x1):
        col = np.nonzero(deck[:, x])[0]
        if len(col):
            side[col.max() + 1:col.max() + 5 - (1 if x < x0 + 6 else 0), x] = True
    for y, x in zip(*np.nonzero(side)):
        L.px(x, y, "b2" if y == np.nonzero(side[:, x])[0].min() else "b1")
    for y, x in zip(*np.nonzero(deck)):
        L.px(x, y, "b1" if (y - int(cy)) % 3 else "b0")
    hull = deck | side
    pad = np.pad(hull, 1)
    for y, x in zip(*np.nonzero(hull & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:]))):
        L.px(x, y, "k0")
    # the gunwale, lit along its top
    for x in range(x0 + 1, x1 - 1):
        col = np.nonzero(deck[:, x])[0]
        if len(col) > 2:
            L.px(x, col.min(), "b3"), L.px(x, col.max(), "b2")
    # thwarts across the boat
    for tx in (18, 31):
        col = np.nonzero(deck[:, tx])[0]
        for y in range(col.min() + 1, col.max()):
            L.px(tx, y, "b3"), L.px(tx + 1, y, "b2"), L.px(tx + 2, y, "b0")
    # an oar shipped along the near side, its blade at the stern
    for x in range(12, 40):
        L.px(x, 18, "b3" if x % 2 else "b2")
    L.rect(38, 17, 4, 3, "b2"), L.px(38, 17, "b3")
    # a coil of rope in the bow, a basket of net in the stern
    for x, y in ((12, 12), (13, 11), (14, 11), (15, 12), (14, 13), (13, 13)):
        L.px(x, y, "ash2")
    L.rect(34, 11, 4, 3, "ash"), L.px(35, 11, "ash2"), L.px(36, 12, "ash2")
    # the painted eye at the bow
    L.px(9, 16, "fr4"), L.px(10, 16, "fr4"), L.px(11, 16, "fr4"), L.px(10, 17, "fr4")
    L.px(10, 16, "k0"), L.px(9, 15, "k0"), L.px(11, 15, "k0")
    # the mooring line, off to the west
    L.line(4, 14, 0, 12, "ash2")
    # its stillness: a dark reflection of the hull on the water
    for x in range(x0 + 4, x1 - 1, 2):
        col = np.nonzero(hull[:, x])[0]
        L.px(x, col.max() + 1, "k0")
    return L.a


def mooring_post():
    L = Layer(16, 16)
    m = np.zeros((16, 16), bool)
    m[3:14, 6:10] = True
    shadow(L, m, 0, 0, c="f1")
    shade(L, m, ramp=["b3", "b2", "b2", "b1", "b0"])
    for x in range(5, 11):
        L.px(x, 7, "ash2" if x % 2 else "ash")
        L.px(x, 9, "ash" if x % 2 else "ash2")
    L.line(10, 8, 15, 10, "ash2")
    return L.a


def tide_pool():
    """3x2: a rock pool on the grotto floor: anemones, a starfish, weed."""
    L = Layer(48, 32)
    rim = ellipse_mask(48, 32, 24, 16, 22, 13)
    pool = ellipse_mask(48, 32, 24, 17, 18.5, 9.5)
    for y, x in zip(*np.nonzero(rim & ~pool)):
        L.px(x, y, "f4" if y < 12 else ("f3" if y < 22 else "f2"))
    for y, x in zip(*np.nonzero(pool)):
        d = math.hypot((x - 24) / 18.5, (y - 17) / 9.5)
        L.px(x, y, "w4" if d > 0.85 and y < 14 else ("w3" if d > 0.6 else "w2"))
    pad = np.pad(rim, 1)
    for y, x in zip(*np.nonzero(rim & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:]))):
        L.px(x, y, "k0")
    pad = np.pad(pool, 1)
    for y, x in zip(*np.nonzero(pool & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:]))):
        L.px(x, y, "f1" if y < 17 else "f2")
    for x, y in ((12, 20), (14, 21), (13, 22), (11, 21)):
        L.px(x, y, "an")
    L.px(12, 21, "f4")
    for x, y in ((31, 14), (30, 15), (31, 15), (32, 15), (31, 16), (29, 16), (33, 16)):
        L.px(x, y, "sf")
    for x in range(18, 26, 2):
        L.px(x, 22, "al2"), L.px(x, 23, "al1"), L.px(x + 1, 21, "al1")
    for x, y in ((36, 21), (37, 20), (35, 22)):
        L.px(x, y, "an")
    L.px(22, 13, "w5"), L.px(23, 13, "w5"), L.px(27, 18, "w4")
    return L.a


def salt_floor():
    L = Layer(16, 16)
    for x, y in ((2, 3), (3, 3), (3, 4), (7, 2), (12, 4), (13, 4), (12, 5), (5, 9), (6, 9), (6, 10),
                 (10, 11), (11, 11), (11, 12), (14, 9), (2, 13), (3, 13), (8, 14)):
        L.px(x, y, "dl" if (x + y) % 2 else "mn2")
    for x, y in ((4, 4), (13, 5), (7, 10), (12, 12), (4, 13)):
        L.px(x, y, "f2")
    return L.a


def shingle():
    """Sea-worn pebbles, rounded and pale, packed at a grotto's shore."""
    L = Layer(16, 16)
    for i, (x, y, r) in enumerate(((2, 2, 2), (7, 1, 1), (11, 3, 2), (4, 6, 1), (8, 7, 2), (13, 8, 1),
                                   (2, 10, 2), (6, 12, 1), (10, 12, 2), (14, 13, 1), (12, 1, 1), (5, 15, 1))):
        m = ellipse_mask(16, 16, x + 0.5, y + 0.5, r + 0.6, r + 0.3)
        for yy, xx in zip(*np.nonzero(m)):
            dx, dy = xx - x, yy - y
            c = "f5" if dx + dy < 0 else ("f4" if dx + dy <= 1 else "f2")
            L.px(xx, yy, c)
        L.px(x + r, y + r, "f1")
    return L.a


def grotto_pieces():
    out = []
    water = kit.water_cell(False, False, False, False)
    out.append(on_floor("boat", "A fisher's boat, moored", 3, 2, ["XXX", "XXX"], boat(), section="places",
                        ground=water, floor_mb=None,
                        notes="On still water, bow west, rope to a mooring post. Impassable."))
    out.append(on_floor("mooring_post", "Mooring post", 1, 1, ["X"], mooring_post(), section="places",
                        notes="The boat's rope is tied here; set it on the shore west of the bow."))
    out.append(on_floor("tide_pool", "Tide pool", 3, 2, ["XXX", "XXX"], tide_pool(), section="places",
                        notes="A rock pool with anemones, a starfish and weed. Impassable."))
    out.append(on_floor("salt", "Salt crust", 1, 1, ["."], salt_floor(), section="places",
                        notes="The Salt Grotto's floor, crusted white. Walkable."))
    out.append(on_floor("shingle", "Shingle", 1, 1, ["."], shingle(), section="places",
                        notes="Sea-worn pebbles at a grotto's shore. Walkable."))
    b, m = props.niche("shells")
    s = Struct("shell_shrine", "Glaukos's shrine of shells", 1, 2, "places", walk=["X", "X"],
               notes="1x2 in a wet face. A tiny shrine of shells; someone scratched a name: GLAUKOS.")
    s.B.a[:] = recolor(b, WET)
    s.M.a[:] = m
    out.append(s)
    return out


def build():
    return crypt_style() + wet_style() + crypt_pieces() + grotto_pieces()


# --------------------------------------------------------------------------
# Mock-ups (rendered by cave_dark_mockups.py)
# --------------------------------------------------------------------------

def mockups(Room, sprites):
    out = []
    rm_ = Room("crypt", """
###############
###############
###############
###############
###.........###
###.........###
###.........###
###.........###
###.........###
###.........###
###############
###############
""", style="crypt")
    rm_.put("crypt_stair", 6, 2).put("crypt_relief", 9, 2)
    rm_.put("sarcophagus", 3, 4).put("altar_stone", 7, 6).put("dig_crypt", 10, 8)
    rm_.put("kit:floor|..", 6, 4)
    rm_.player = (7, 8)
    out.append(rm_)

    rm_ = Room("sea_grotto", """
###########################
###########################
###########################
#####.....######.....######
####.......####.......#####
###.........##..........###
###...~~~~~~~~~~~~~.....###
##...~~~~~~~~~~~~~~~~....##
##...~~~~~~~~~~~~~~~~~...##
##....~~~~~~~~~~~~~~~~...##
###.....~~~~~~~~~~~~.....##
####........~~~~~.......###
#####...................###
######.......#####....#####
###########..##############
###########..##############
""", style="wet")
    rm_.put("daylight_s", 11, 14).put("daylight_s", 12, 14)
    rm_.put("boat", 6, 7).put("mooring_post", 4, 8).put("shingle", 4, 9).put("shingle", 5, 10)
    rm_.put("shingle", 4, 7).put("tide_pool", 19, 11)
    rm_.put("shell_shrine", 8, 2).put("brazier_lit", 18, 3).put("brazier_cold", 3, 11)
    rm_.put("dig", 15, 12).put("pebbles", 9, 12)
    rm_.player = (10, 12)
    rm_.halos = [(18 * 16 + 16, 3 * 16 + 14), (12 * 16, 16 * 16, 44)]
    out.append(rm_)
    return out
