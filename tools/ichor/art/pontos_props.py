"""Pontos's sea, rocks, flora and the lanes' landmarks.

- The Pontic sea: aethos's animated water metatiles re-pointed at palette 12
  (pontos_lib.PONTIC), so the Black Sea is dark green and still moves.
- Crags: white chalk stacks and the Kyaneai's blue-black rocks, as akti_coast
  draws its limestone, in Pontos's palettes.
- The Clashing Rocks' scar: a dove's tail feathers caught in a crack where the
  rocks last met (Argonautica 2.598-602).
- Whirlpools (Triton's Conch's stub), sea-marks, a lighthouse, the Bosporus
  mouth's shrine of Zeus of the Fair Wind, the Acherusian cave at Herakleia.
- The Isle of Ares: the Amazons' black stone (Argonautica 2.1169-1176), the
  birds' feathers stuck in the ground like arrows, a bronze shield on a post
  (the Argonauts clashed theirs to drive the birds off, 2.1047-1089), and the
  great roost on the peak.
- The Pontic woods (oak and beech), hazel, and the Phasis's reeds.
"""
from __future__ import annotations

import random

import numpy as np
from PIL import Image, ImageDraw

import pontos_lib as P
from pontos_lib import Struct, derived, finish

# --------------------------------------------------------------------------
# The Pontic sea (derived: no tiles)
# --------------------------------------------------------------------------

SAND_EDGES = {   # aethos's sand island in the sea, TL T TR / L R / BL B BR, inner corners
    "tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "r": 0x125, "bl": 0x12B, "b": 0x12C,
    "br": 0x12D, "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146,
}


def build_sea():
    out = [derived("psea", "The Pontic sea (aethos 0x170, palette 12)", [0x170], ["."],
                   notes="Open water, animated, dark sea green."),
           derived("psea_rough", "Rough water (aethos 0x14E, palette 12)", [0x14E], ["."],
                   notes="Currents in the strait.")]
    for part, mid in SAND_EDGES.items():
        walk = "."
        out.append(derived(f"beach_{part}", f"Beach edge {part} (aethos 0x{mid:03X}, palette 12)",
                           [mid], [walk], notes="aethos's sand-in-sea edge, its surf in the Pontic sea."))
    out.append(derived("sea_rock", "Rock in the sea (aethos 0x18C, palette 12)", [0x18C], ["X"]))
    out.append(derived("sea_boulder", "Boulder in the sea, foam ring (aethos 0x0C5, palette 12)",
                       [0x0C5], ["X"]))
    return out


# --------------------------------------------------------------------------
# Crags
# --------------------------------------------------------------------------

CHALK = {"hi": "w0", "lit": "ck4", "mid": "ck3", "dark": "ck2", "crack": "ck1", "line": "ck0",
         "face": ("ck3", "ck2"), "strata": "ck1", "wet": "wt", "weed": "wg", "foam": ("w0", "pf"),
         "shrub": ("gs", "gr1")}
KYAN = {"hi": "ky4", "lit": "ky3", "mid": "ky2", "dark": "ky1", "crack": "ky0", "line": "ink",
        "face": ("ky1", "ky0"), "strata": "ky0", "wet": "wt", "weed": "wg", "foam": ("w0", "pf"),
        "shrub": ("gs", "gr1")}


def _mask(w, h, pts):
    m = Image.new("1", (w, h), 0)
    ImageDraw.Draw(m).polygon(pts, fill=1)
    return np.array(m)


def crag(L, pts, face, pal, seed=0, foam=True, wet=True, shrub=0):
    """A crag: `pts` outline its top; its south face hangs `face` px below; foam
    rings its foot. As akti_coast.crag, in a Pontos palette."""
    from kalliste_parts import voronoi_labels
    rng = random.Random(seed)
    w, h = L.w, L.h
    top = _mask(w, h, pts)
    body = top.copy()
    for d in range(1, face + 1):
        body[d:] |= top[:-d]
    face_m = body & ~top
    ys, xs = np.nonzero(body)
    if not len(xs):
        return
    if foam:
        ring = np.zeros_like(body)
        ring[1:] |= body[:-1]
        ring[:, 1:] |= body[:, :-1]
        ring[:, :-1] |= body[:, 1:]
        ring &= ~body
        ring2 = np.zeros_like(ring)
        ring2[1:] |= ring[:-1]
        ring2[:, 1:] |= ring[:, :-1]
        ring2[:, :-1] |= ring[:, 1:]
        ring2 &= ~body & ~ring
        for y, x in zip(*np.nonzero(ring)):
            if y > ys.min() + 2:
                L.px(x, y, pal["foam"][0] if rng.random() < 0.7 else pal["foam"][1])
        for y, x in zip(*np.nonzero(ring2)):
            if y > ys.min() + 4 and rng.random() < 0.45:
                L.px(x, y, pal["foam"][1])
    tys, txs = np.nonzero(top)
    n_seeds = max(3, int(top.sum() // 28))
    seeds = [(int(txs[i]), int(tys[i])) for i in rng.sample(range(len(txs)), min(n_seeds, len(txs)))]
    lab = voronoi_labels(w, h, seeds, wrap=False, stretch=(1.0, 1.3))
    tones = [pal["hi"], pal["lit"], pal["lit"], pal["mid"], pal["lit"], pal["mid"]]
    tilt = [rng.choice(tones) for _ in seeds]
    lo = {pal["hi"]: pal["lit"], pal["lit"]: pal["mid"], pal["mid"]: pal["dark"]}
    hi = {pal["lit"]: pal["hi"], pal["mid"]: pal["lit"], pal["hi"]: pal["hi"]}
    for y, x in zip(tys, txs):
        k = lab[y, x]
        c = tilt[k]
        right = x + 1 < w and lab[y, x + 1] != k and top[y, x + 1]
        down = y + 1 < h and lab[y + 1, x] != k and top[y + 1, x]
        left = x > 0 and lab[y, x - 1] != k
        up = y > 0 and lab[y - 1, x] != k
        if right or down:
            c = pal["crack"] if (right and down) or rng.random() < 0.6 else pal["dark"]
        elif left or up:
            c = hi.get(c, c)
        elif (x + y * 3 + k) % 9 == 0:
            c = lo.get(c, c)
        if not top[max(0, y - 1), x] or not top[y, max(0, x - 1)]:
            c = pal["hi"]
        elif not top[min(h - 1, y + 1), x] or not top[y, min(w - 1, x + 1)]:
            c = pal["dark"]
        L.px(x, y, c)
    for y, x in zip(*np.nonzero(face_m)):
        depth = 0
        while depth < face and y - depth - 1 >= 0 and face_m[y - depth - 1, x]:
            depth += 1
        below = y + 1 >= h or not body[y + 1, x]
        c = pal["face"][0] if (x * 3 + seed) % 7 else pal["face"][1]
        if depth == 0:
            c = pal["lit"]
        if (x + depth) % 5 == 0:
            c = pal["strata"]
        if wet and below:
            c = pal["wet"]
        elif wet and (y + 2 < h and not body[min(h - 1, y + 2), x]):
            c = pal["weed"] if (x + seed) % 3 else pal["wet"]
        L.px(x, y, c)
    pad = np.pad(body, 1)
    edge = body & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if L.get(x, y) != pal["hi"]:
            L.px(x, y, pal["line"])
    for _ in range(shrub):
        tys, txs = np.nonzero(top)
        i = rng.randrange(len(txs))
        x, y = int(txs[i]), int(tys[i])
        for (dx, dy, c) in ((0, 0, 1), (1, 0, 1), (-1, 1, 1), (0, 1, 0), (1, 1, 0), (2, 1, 1), (0, -1, 1)):
            if top[min(h - 1, max(0, y + dy)), min(w - 1, max(0, x + dx))]:
                L.px(x + dx, y + dy, pal["shrub"][c])


def build_rocks():
    out = []
    s = Struct("stack", "Chalk sea stack", 1, 2, walk=["X", "X"], ground="psea",
               notes="A white stack standing in the dark sea, scrub on its top.")
    crag(s.M, [(3, 3), (9, 1), (14, 4), (14, 12), (9, 14), (2, 11)], 14, CHALK, seed=3, shrub=2)
    out.append(finish(s))
    s = Struct("rocks", "Chalk rocks awash", 1, 1, walk=["X"], ground="psea")
    crag(s.M, [(2, 7), (6, 5), (9, 7), (7, 9), (3, 10)], 3, CHALK, seed=12)
    crag(s.M, [(10, 3), (13, 2), (15, 4), (13, 5)], 2, CHALK, seed=13)
    out.append(finish(s))
    s = Struct("kyrocks", "Kyanean rocks awash", 1, 1, walk=["X"], ground="psea",
               notes="Blue-black rocks: the Clashing Rocks' smaller kin, and the side channel's.")
    crag(s.M, [(1, 6), (7, 3), (12, 6), (10, 10), (3, 11)], 4, KYAN, seed=21)
    crag(s.M, [(11, 11), (14, 10), (15, 13), (12, 14)], 2, KYAN, seed=22)
    out.append(finish(s))
    return out


def feathers():
    """A dove's tail feathers caught in a crack of the Clashing Rocks' face: they
    shut on her tail and she flew on (Argonautica 2.598-602). It replaces the plain
    kyanean face piece below a rock's south edge."""
    import pontos_coast as C
    key = "111000000"
    art, kind, _ = C.draw(key, "kyanean")
    s = Struct("kyanean_feathers", "Clashing Rocks' face: a dove's feathers in a crack", 1, 1,
               walk=["X"], ground="psea",
               notes=f"Stands in for the kyanean piece of neighbourhood {key}; read it (a bg sign).")
    for y in range(16):
        for x in range(16):
            if art[y][x]:
                s.M.px(x, y, art[y][x])
    s.M.line(4, 1, 9, 7, "ink")                  # the crack where the rocks met
    s.M.line(9, 7, 7, 9, "ink")
    for (x, y) in ((6, 3), (8, 5), (7, 7)):
        s.M.blit(["w ", "ww", " w", "kw"], {"w": "w0", "k": "ky1"}, x - 1, y - 2)
    s.M.px(10, 8, "w0")
    return [finish(s)]


def whirlpool():
    """A whirlpool: the water turning in a ring round a dark eye. Solid. Calmed by
    Triton's Conch when it exists (ICHOR_STUB_RELIC)."""
    s = Struct("whirlpool", "Whirlpool", 1, 1, walk=["X"], ground="psea")
    M = s.M
    cx, cy = 7.5, 7.5
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy
            r = (dx * dx + dy * dy) ** 0.5
            if r > 7.6:
                continue
            a = np.arctan2(dy, dx)
            phase = (a * 2 / np.pi + r / 2.2) % 2
            if r < 1.8:
                M.px(x, y, "wt")
            elif phase < 0.45:
                M.px(x, y, "w0" if r > 3 else "pf")
            elif phase < 0.7:
                M.px(x, y, "pf")
    return [finish(s)]


# --------------------------------------------------------------------------
# Landmarks on the shore
# --------------------------------------------------------------------------

def lighthouse():
    """A colony's light: a round stone tower, its fire basket on top. 1 x 3."""
    s = Struct("lighthouse", "Colony lighthouse", 1, 3, walk=["X", "X", "X"], ground="grass")
    M = s.M
    for y in range(16, 48):
        for x in range(3, 13):
            k = x - 3
            c = "ck4" if k < 3 else ("ck3" if k < 7 else "ck2")
            if (y - 16) % 6 == 5:
                c = "ck1"
            M.px(x, y, c)
    M.vline(2, 16, 47, "ck0")
    M.vline(13, 16, 47, "ck0")
    M.rect(6, 24, 3, 4, "ck0")
    M.rect(6, 36, 3, 4, "ck0")
    M.hline(1, 14, 47, "wt")
    # the fire basket on its bronze cap (row 0), all in the bronze group
    M.rect(2, 12, 12, 4, "bz1")
    M.hline(2, 13, 12, "bz3")
    M.hline(2, 13, 15, "bz0")
    M.rect(4, 8, 8, 4, "bz2")
    M.hline(4, 11, 8, "bz4")
    M.blit(["   f  f   ", "  ffo ff  ", " fooyofo  ", " foyyyof  ", "  fooof   "],
           {"f": "fire", "o": "oil", "y": "bz4"}, 3, 3)
    return [finish(s)]


def cave_mouth():
    """The Acherusian cave at Herakleia, where Herakles hauled Kerberos up into the
    light: a dark arch at the foot of a chalk cliff's face. It replaces the chalk
    piece of neighbourhood 111000000 (a face under a south-facing cliff)."""
    import pontos_coast as C
    key = "111000000"
    art, kind, _ = C.draw(key, "chalk")
    s = Struct("acheron", "The Acherusian cave in a chalk face", 1, 1, walk=["X"], ground="psea",
               notes=f"Stands in for the chalk piece of neighbourhood {key}; read it (a bg sign).")
    for y in range(16):
        for x in range(16):
            if art[y][x]:
                s.M.px(x, y, art[y][x])
    s.M.ellipse(3, 1, 12, 14, "ck0")
    s.M.ellipse(4, 3, 11, 14, "ink")
    s.M.hline(4, 11, 10, "wt")
    s.M.px(7, 6, "ck1")
    return [finish(s)]


# --------------------------------------------------------------------------
# The Isle of Ares
# --------------------------------------------------------------------------

def ares_stone():
    """The Amazons' black stone on the Isle of Ares, where they sacrificed horses
    (Argonautica 2.1172-1176): a black boulder on a ring of gray stones, a spear
    leaning on it, a red cloth. 1 x 2."""
    s = Struct("ares_stone", "The black stone of Ares", 1, 2, walk=["X", "X"], ground="grass")
    M = s.M
    M.ellipse(0, 22, 15, 31, "gy0")
    for (x, y) in ((3, 25), (8, 28), (13, 25)):
        M.ellipse(x - 2, y - 2, x + 2, y + 1, "gy1")
    M.poly([(2, 26), (1, 12), (5, 5), (11, 4), (14, 10), (14, 26)], "blk")
    M.line(5, 5, 11, 4, "gy0")
    M.line(5, 6, 3, 13, "gy0")
    M.px(7, 8, "gy1")
    M.line(15, 30, 9, 0, "wd2")
    M.px(9, 0, "gy1")
    M.rect(4, 17, 7, 5, "mad")
    M.hline(4, 10, 17, "mad2")
    return [finish(s)]


def feather_stakes():
    """Feathers of the birds of Ares, shot down like arrows into the turf
    (Argonautica 2.1033-1046). Bronze-edged."""
    s = Struct("feathers_ground", "Bird of Ares feathers stuck in the ground", 1, 1, walk=["X"],
               ground="grass")
    M = s.M
    for (x, y, lean) in ((3, 2, 1), (9, 0, -1), (12, 5, 1)):
        for k in range(11):
            xx = x + (k * lean) // 4
            M.px(xx, y + k, "bz3" if k < 7 else "bz1")
            if k < 7:
                M.px(xx + 1, y + k, "bz2")
                if k % 2 == 0:
                    M.px(xx - 1, y + k, "bz4")
        M.px(x + (10 * lean) // 4, y + 11, "bz0")
    return [finish(s)]


def shield_post():
    """A dented bronze shield hung on a post: clash it and the birds scatter."""
    s = Struct("shield_post", "Bronze shield on a post", 1, 2, walk=["X", "X"], ground="grass")
    M = s.M
    M.rect(7, 10, 2, 22, "bz0")
    M.ellipse(1, 2, 14, 15, "bz1")
    M.ellipse(2, 3, 13, 14, "bz3")
    M.ellipse(5, 6, 10, 11, "bz2")
    M.ellipse(6, 7, 8, 9, "bz4")
    M.px(4, 5, "bz4")
    M.line(10, 4, 12, 7, "bz1")                    # a dent from a feather
    M.hline(5, 10, 31, "bz0")
    return [finish(s)]


def roost():
    """The roost on the isle's peak, on the dark rock's top: a nest of sticks and one
    great black feather. Something too big for the birds of Ares sleeps here
    (ICHOR_STUB_LEGEND: Yveltal). It replaces the plain kyanean interior piece."""
    import pontos_coast as C
    art, kind, _ = C.draw("1" * 9, "kyanean")
    s = Struct("roost", "The great roost", 1, 1, walk=["X"], ground="psea",
               notes="Stands in for the plain kyanean interior; read it (a bg sign).")
    for y in range(16):
        for x in range(16):
            s.M.px(x, y, art[y][x])
    s.M.ellipse(1, 6, 14, 14, "ky0")
    for k in range(0, 12, 2):
        s.M.line(2 + k, 8 + (k % 4), 4 + k, 12 - (k % 3), "ky2")
    s.M.line(8, 9, 15, 0, "ink")
    s.M.line(9, 9, 15, 2, "ky0")
    s.M.line(7, 9, 13, 0, "ink")
    return [finish(s)]


def snag():
    """A dead tree on the isle, stripped by the birds: a perch. 1 x 2."""
    s = Struct("snag", "Dead tree, a perch", 1, 2, walk=["X", "X"], ground="grass")
    M = s.M
    M.rect(7, 8, 3, 24, "gy0")
    M.vline(7, 8, 31, "gy1")
    M.line(8, 12, 2, 4, "gy0")
    M.line(9, 10, 14, 2, "gy0")
    M.line(3, 5, 1, 1, "gy0")
    M.line(13, 3, 15, 0, "gy0")
    M.line(8, 18, 13, 14, "gy0")
    M.px(2, 4, "gy1")
    M.hline(5, 11, 31, "gy0")
    return [finish(s)]


# --------------------------------------------------------------------------
# Flora
# --------------------------------------------------------------------------

def oak():
    """A Pontic oak, dark and round, the wet coast's woods. 2 x 2."""
    s = Struct("oak", "Pontic oak", 2, 2, walk=["XX", "XX"], ground="grass")
    M = s.M
    M.rect(13, 20, 6, 11, "tr0")
    M.vline(13, 20, 30, "tr1")
    M.hline(9, 22, 31, "gs")
    rng = random.Random(4)
    for (x, y, r) in ((16, 11, 12), (7, 14, 7), (25, 14, 7), (12, 5, 6), (21, 5, 6)):
        M.ellipse(x - r, y - r, x + r, y + r, "fg1")
    for (x, y, r) in ((14, 9, 8), (8, 12, 4), (22, 8, 5), (11, 4, 4)):
        M.ellipse(x - r, y - r + 1, x + r - 2, y + r - 2, "fg2")
    for _ in range(26):
        x, y = rng.randrange(4, 26), rng.randrange(2, 20)
        if M.get(x, y) == "fg2":
            M.px(x, y, "fg3")
        elif M.get(x, y) == "fg1" and rng.random() < 0.5:
            M.px(x, y, "fg0")
    for y in range(32):
        for x in range(32):
            if M.get(x, y) == "fg1" and (y > 20 or M.get(x, y + 1) is None):
                M.px(x, y, "fg0")
    return [finish(s)]


def hazel():
    s = Struct("hazel", "Hazel bush", 1, 1, walk=["X"], ground="grass")
    M = s.M
    M.ellipse(1, 2, 14, 15, "fg1")
    M.ellipse(2, 2, 12, 12, "fg2")
    for (x, y) in ((4, 4), (9, 3), (6, 8), (11, 7)):
        M.px(x, y, "fg3")
    for (x, y) in ((5, 11), (10, 10)):
        M.blit(["rr", "r "], {"r": "rd0"}, x, y)
    M.hline(2, 13, 15, "fg0")
    return [finish(s)]


def reeds(water=False):
    """The Phasis's reeds, where the pheasants live: on the bank, or standing in
    the shallows."""
    key = "reeds_water" if water else "reeds"
    s = Struct(key, "Reeds in the shallows" if water else "Reeds on the bank", 1, 1, walk=["X"],
               ground="psea" if water else "grass")
    M = s.M
    rng = random.Random(9 if water else 8)
    for i in range(9):
        x = 1 + i * 2 - (i % 2) + rng.randrange(0, 2)
        top = rng.randrange(0, 5)
        for y in range(top, 16 if not water else 13):
            M.px(x, y, "fg2" if y > top + 3 else ("rd1" if i % 2 else "rd0"))
        M.px(x, top, "rd0")
        M.px(x + 1, top + 1, "rd1")
    if water:
        M.hline(0, 15, 13, "fg1")
    else:
        M.hline(0, 15, 15, "gs")
    return [finish(s)]


def build_shore():
    return lighthouse() + cave_mouth() + whirlpool() + feathers()


def build_isle():
    return ares_stone() + feather_stakes() + shield_post() + roost() + snag()


def build_flora():
    return oak() + hazel() + reeds() + reeds(water=True)
