"""The cave's furniture: stone, ledges, mouths, fire, webs, Hecate's pieces.

Everything that stands on the floor keeps the kit's plain floor in the bottom
layer and draws itself in the middle layer (or the top layer, for parts the
player walks behind), so it costs only its own tiles and needs only its own
palette group.
"""
from __future__ import annotations

import math

import numpy as np

import cave_dark_kit as kit
from cave_dark_lib import C, Layer, Struct, grid_art

FLOOR = kit.floor_cell()
LIT = kit.lit_cell(False, False, False, False)
FLOOR_N = kit.floor_cell(N=True)


def tiled(cell, w, h):
    """A w x h cell area of one repeated 16x16 RGBA cell."""
    return np.tile(cell, (h, w, 1))


def on_floor(key, title, w, h, walk, art, section="cave", notes="", names=None, ground=None,
             floor_mb="MB_CAVE"):
    """A structure standing on the floor. art: RGBA (h*16, w*16); cells whose
    walk code is T put their art in the top layer (drawn over the player)."""
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names, floor_mb=floor_mb)
    g = FLOOR if ground is None else ground
    s.B.a[:] = tiled(g, w, h) if g.shape[:2] == (16, 16) else g
    for cy in range(h):
        for cx in range(w):
            part = art[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            layer = s.T if walk[cy][cx] == "T" else s.M
            layer.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = part
    return s


# --------------------------------------------------------------------------
# Shading helpers
# --------------------------------------------------------------------------

ROCK_RAMP = ["k8", "k7", "k6", "k5", "k4", "k3", "k2"]


def shade(L, mask, ramp=ROCK_RAMP, ox=0, oy=0, outline="k0", hi=(0.3, 0.25), bias=0.0):
    """Shade a convex-ish mask lit from the upper left, with an outline."""
    hh, ww = mask.shape
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return
    for y, x in zip(ys, xs):
        row = np.nonzero(mask[y])[0]
        col = np.nonzero(mask[:, x])[0]
        u = (x - row.min()) / max(1, row.max() - row.min())
        v = (y - col.min()) / max(1, col.max() - col.min())
        d = math.hypot(u - hi[0], (v - hi[1]) * 0.8)
        score = 0.5 * u + 0.35 * v + 0.6 * d - 0.15 + bias
        i = int(max(0, min(len(ramp) - 1, round(score * (len(ramp) - 1)))))
        L.px(ox + x, oy + y, ramp[i])
    if outline:
        pad = np.pad(mask, 1)
        edge = mask & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        for y, x in zip(*np.nonzero(edge)):
            L.px(ox + x, oy + y, outline)


def ellipse_mask(w, h, cx, cy, rx, ry):
    yy, xx = np.mgrid[0:h, 0:w]
    return ((xx + 0.5 - cx) / rx) ** 2 + ((yy + 0.5 - cy) / ry) ** 2 <= 1.0


def profile_mask(w, h, cx, widths, y0=0):
    """A vertical solid: widths[i] is the half-width at row y0+i."""
    m = np.zeros((h, w), bool)
    for i, hw in enumerate(widths):
        if hw <= 0:
            continue
        y = y0 + i
        if 0 <= y < h:
            a, b = int(round(cx - hw)), int(round(cx + hw))
            m[y, max(0, a):min(w, b)] = True
    return m


def shadow(L, mask, ox, oy, c="k1", dx=2, dy=1):
    """A contact shadow cast down-right on the floor, under the object."""
    hh, ww = mask.shape
    m2 = np.zeros_like(mask)
    m2[dy:, dx:] = mask[:hh - dy, :ww - dx]
    base = np.zeros_like(mask)
    rows = np.nonzero(mask.any(axis=1))[0]
    if not len(rows):
        return
    bottom = rows.max()
    for y in range(max(0, bottom - 2), hh):
        base[y] = m2[y]
    for y, x in zip(*np.nonzero(base & ~mask)):
        L.px(ox + x, oy + y, c)


# --------------------------------------------------------------------------
# Stone
# --------------------------------------------------------------------------

def cone(w, h, cx, top, bottom, base_hw, rings=()):
    hw = [max(0.0, (y - top) / max(1, bottom - top) * base_hw + 0.6) if y >= top else 0 for y in range(h)]
    m = profile_mask(w, h, cx, hw)
    m[bottom + 1:] = False
    return m


def stalagmite():
    L = Layer(16, 16)
    m = cone(16, 16, 7.5, 1, 14, 5.5)
    shadow(L, m, 0, 0)
    shade(L, m)
    for y in (6, 10):
        row = np.nonzero(m[y])[0]
        L.px(int(row.max()) - 1, y, "k3")
    return L.a


def stalagmite_pair():
    L = Layer(16, 16)
    a = cone(16, 16, 5, 3, 14, 4.5)
    b = cone(16, 16, 11, 7, 14, 3.5)
    shadow(L, a | b, 0, 0)
    shade(L, a)
    shade(L, b)
    return L.a


def stalagmite_tall():
    L = Layer(16, 32)
    m = cone(16, 32, 7.5, 2, 30, 6.5)
    shadow(L, m, 0, 0)
    shade(L, m, bias=-0.05)
    for y in (9, 15, 22):
        row = np.nonzero(m[y])[0]
        for x in range(int(row.min()) + 1, int(row.max())):
            if (x + y) % 3 == 0:
                L.px(x, y, "k4")
    return L.a


def column():
    """A column, where a stalactite met its stalagmite long ago."""
    L = Layer(16, 32)
    hw = [7, 7, 6.5, 6, 5, 4.5, 4, 3.5, 3.2, 3, 3, 3, 3, 3, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2,
          4.5, 4.8, 5, 5.3, 5.6, 6, 6.3, 6.6, 7, 7, 7]
    m = profile_mask(16, 32, 8, hw)
    shadow(L, m, 0, 0)
    shade(L, m, bias=-0.05)
    for y in (12, 13):
        row = np.nonzero(m[y])[0]
        L.px(int(row.min()) + 1, y, "k8")
    for y in (5, 19, 25):
        row = np.nonzero(m[y])[0]
        for x in range(int(row.min()) + 1, int(row.max())):
            L.px(x, y, "k4" if x > 8 else "k5")
    return L.a


def boulder():
    L = Layer(16, 16)
    m = ellipse_mask(16, 16, 7.5, 9, 7, 6)
    shadow(L, m, 0, 0)
    shade(L, m)
    L.line(9, 6, 11, 10, "k3"), L.px(8, 6, "k3")
    return L.a


def rock_pile():
    L = Layer(16, 16)
    parts = [ellipse_mask(16, 16, 5, 11, 4.5, 3.8), ellipse_mask(16, 16, 11, 11.5, 4.5, 3.5),
             ellipse_mask(16, 16, 8, 6.5, 4, 3.5)]
    allm = parts[0] | parts[1] | parts[2]
    shadow(L, allm, 0, 0)
    for m in parts:
        shade(L, m)
    return L.a


def pebbles():
    L = Layer(16, 16)
    for x, y, big in ((3, 4, 1), (11, 3, 0), (7, 9, 1), (13, 11, 0), (2, 12, 0), (9, 14, 0)):
        if big:
            L.px(x, y, "k6"), L.px(x + 1, y, "k5"), L.px(x, y + 1, "k5"), L.px(x + 1, y + 1, "k4")
            L.px(x + 2, y + 1, "k1"), L.px(x + 1, y + 2, "k1")
        else:
            L.px(x, y, "k5"), L.px(x + 1, y, "k4"), L.px(x + 1, y + 1, "k1")
    return L.a


def slab():
    """A slab fallen from the roof, 2x1."""
    L = Layer(32, 16)
    top = np.zeros((16, 32), bool)
    for y in range(3, 10):
        a = 3 + (9 - y) // 2
        b = 28 - (y - 3) // 3
        top[y, a:b] = True
    front = np.zeros((16, 32), bool)
    for y in range(10, 14):
        front[y, 2:27] = True
    shadow(L, top | front, 0, 0)
    shade(L, top, ramp=["k8", "k7", "k6", "k6", "k5"], outline=None)
    shade(L, front, ramp=["k4", "k3", "k3", "k2"], outline=None)
    allm = top | front
    pad = np.pad(allm, 1)
    edge = allm & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "k0")
    L.line(12, 5, 15, 9, "k4"), L.line(15, 9, 14, 12, "k1")
    return L.a


# --------------------------------------------------------------------------
# Ledges
# --------------------------------------------------------------------------

LEDGE_FACE = ["k7", "k5", "k4", "k4", "k3", "k3", "k3", "k2", "k2"]


def ledge(part):
    """A low rock step to jump down, south: lip, a short face, its shadow.
    part: 'w' (west end), 'a', 'b' (middles), 'e' (east end)."""
    L = Layer(16, 16)
    for x in range(16):
        top = 5 + (1 if (part == "b" and 5 <= x <= 10) else 0) + (1 if (part == "a" and 11 <= x <= 13) else 0)
        bot = 15
        if part == "w" and x < 6:
            top += (6 - x) // 2 + 1
            bot -= 0
        if part == "e" and x > 9:
            top += (x - 9) // 2 + 1
        if top >= bot - 2:
            continue
        L.px(x, top, "k0")
        for i, y in enumerate(range(top + 1, bot - 1)):
            c = LEDGE_FACE[min(i, len(LEDGE_FACE) - 1)]
            if i > 2 and (x * 5 + y * 3) % 11 == 0:
                c = "k3"
            L.px(x, y, c)
        L.px(x, bot - 1, "k1")
        L.px(x, bot, "k1" if (x + bot) % 2 else None)
    if part in ("w", "e"):
        xs = range(0, 6) if part == "w" else range(10, 16)
        for x in xs:
            col = [y for y in range(16) if L.get(x, y)]
            if col:
                L.px(x, col[0], "k0")
                L.px(x, col[0] + 1, "k6")
    return L.a


def ledge_side(east):
    """A low step to jump down east (or west): the lip runs down the cell's
    side, its shadow on the lower floor."""
    L = Layer(16, 16)
    for y in range(16):
        x0 = 8 + (1 if 4 <= y <= 9 else 0)
        L.px(x0, y, "k0")
        L.px(x0 + 1, y, "k7" if y % 5 else "k6")
        L.px(x0 + 2, y, "k5")
        L.px(x0 + 3, y, "k4")
        L.px(x0 + 4, y, "k2")
        L.px(x0 + 5, y, "k1")
        if y % 2:
            L.px(x0 + 6, y, "k1")
    if not east:
        L.a[:] = L.a[:, ::-1]
    return L.a


# --------------------------------------------------------------------------
# A mouth to daylight in a north face, and a hole down
# --------------------------------------------------------------------------

def mouth():
    """2x2: an opening in a north face, daylight beyond. Returns (bottom, middle)."""
    base = np.concatenate([np.concatenate([kit.face_cell("ft", "A", "B"), kit.face_cell("ft", "C", "A")], 1),
                           np.concatenate([kit.face_cell("fb", "A", "B"), kit.face_cell("fb", "C", "A")], 1)], 0)
    face = Layer(32, 32)
    face.a[:] = base
    hole = np.zeros((32, 32), bool)
    for y in range(7, 32):
        if y < 13:
            r = 9.5 * math.sqrt(max(0.0, 1 - ((13 - y) / 6.5) ** 2))
        else:
            r = 9.5 + (1 if y > 27 else 0)
        hole[y, int(round(16 - r)):int(round(16 + r))] = True
    haze = ["k7", "k8", "wh"]
    for y, x in zip(*np.nonzero(hole)):
        d = min(x - (16 - 10), (16 + 10) - x, y - 7)
        face.px(x, y, haze[min(2, max(0, d // 2))] if y < 16 else None)
    pad = np.pad(hole, 1)
    for y in range(32):
        for x in range(32):
            if hole[y, x]:
                continue
            nb = [pad[y + 1 + dy, x + 1 + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if any(nb):
                face.px(x, y, "k0")
    # a lit lip on the opening's west edge, shadow on the east
    for y in range(8, 32):
        row = np.nonzero(hole[y])[0]
        if len(row):
            face.px(int(row.min()) - 2, y, "k7")
            face.px(int(row.max()) + 2, y, "k2")
    bottom = np.zeros((32, 32, 4), np.uint8)
    bottom[:16] = face.a[:16]
    mid = np.zeros((32, 32, 4), np.uint8)
    mid[16:] = face.a[16:]
    lit = Layer(32, 16)
    for y in range(16):
        for x in range(32):
            c = kit.tex(kit.FLOOR, kit.LIT_C, x, y)
            if y < 4:
                c = "dl"
            elif y < 7:
                c = "dl" if (x + y) % 2 else "mn2"
            elif y < 10 and c == "mn1" and (x + y) % 2:
                c = "mn2"
            lit.px(x, y, c)
    bottom[16:] = lit.a
    return bottom, mid


def daylight():
    """2x1: daylight pouring in at an east mouth, brightest at the map's edge.
    Mirrored for the west; turned for the south and north."""
    L = Layer(32, 16)
    levels = [kit.FLOOR_C, {"2": "f3", "3": "f4", "4": "mn1", "5": "mn2"}, kit.LIT_C,
              {"2": "mn1", "3": "mn2", "4": "dl", "5": "dl"}, {"2": "mn2", "3": "dl", "4": "dl", "5": "dl"}]
    for y in range(16):
        for x in range(32):
            t = (x + 0.5) / 32 * (len(levels) - 0.6) + 0.15 * kit.wob16(y, 3)
            i = int(t)
            frac = t - i
            if frac > 0.55 and (x + y) % 2 == 0:
                i += 1
            i = max(0, min(len(levels) - 1, i))
            L.px(x, y, kit.tex(kit.FLOOR, levels[i], x, y))
    return L.a


def hole_down():
    """A pit with rough steps going down into black."""
    L = Layer(16, 16)
    m = ellipse_mask(16, 16, 8, 8.5, 7, 6)
    for y, x in zip(*np.nonzero(m)):
        L.px(x, y, "k0")
    for y, (a, b), c in ((4, (4, 12), "k5"), (5, (4, 12), "k3"), (7, (5, 11), "k4"), (8, (5, 11), "k2"),
                         (10, (6, 10), "k3"), (11, (6, 10), "k1")):
        for x in range(a, b):
            L.px(x, y, c)
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, "k6" if y < 8 else "k2")
    return L.a


# --------------------------------------------------------------------------
# Fire: the bronze brazier, 2x2
# --------------------------------------------------------------------------

def mirror_left(L):
    """Make a layer left-right symmetric from its left half, so Porytiles
    stores the right half as flipped tiles."""
    w = L.w
    L.a[:, w // 2:] = L.a[:, :w // 2][:, ::-1]


def cylinder(L, mask, ramp, outline="k0"):
    """Shade a mask as a body lit from the front: bright down the middle."""
    for y in range(mask.shape[0]):
        row = np.nonzero(mask[y])[0]
        if not len(row):
            continue
        a, b = row.min(), row.max()
        c = (a + b) / 2
        hw = max(1.0, (b - a) / 2)
        for x in row:
            t = abs(x - c) / hw
            L.px(x, y, ramp[min(len(ramp) - 1, int(t * (len(ramp) - 0.01)))])
    if outline:
        pad = np.pad(mask, 1)
        edge = mask & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        for y, x in zip(*np.nonzero(edge)):
            L.px(x, y, outline)


BRAZIER_FLAMES = [
    ["........r.......r.......",
     ".......rr......ryr......",
     "...r...ryr....ryyr...r..",
     "...rr..ryyr...ryyr..rr..",
     "..ryr.ryyyr..ryywyr.ryr.",
     "..ryyrryywyr.rywwyrryyr.",
     ".ryyyryywwyrryywwyrryyr.",
     ".ryywyyywwyyyyywwyyyywyr",
     "rryywwywwwwyywwwwwyywwyr",
     "ryywwwwwwwwwwwwwwwwwwwyr",
     "ryyywwwwwwwwwwwwwwwwyyyr"],
    ["......r........r........",
     "......rr......ryr.......",
     "..r...ryr.....ryyr....r.",
     "..rr..ryyr...ryyyr...rr.",
     "..ryr.ryyyr..ryywyr..ryr",
     ".ryyrryywyr.rywwyrr.ryyr",
     ".ryyyryywwyrryywwyrryyyr",
     "rryywyyywwyyyyywwyyyywyr",
     "rryywwywwwwyywwwwwyywwyr",
     "ryywwwwwwwwwwwwwwwwwwwyr",
     "ryyywwwwwwwwwwwwwwwwyyyr"],
    [".........r.......r......",
     "........rr.......rr.....",
     "....r...ryr.....ryr..r..",
     "...rr..ryyr....ryyr.rr..",
     "...ryr.ryyyr..ryywyrryr.",
     "..ryyrryywyr.rywwyrryyr.",
     ".ryyyryywwyrryywwyyryyr.",
     ".ryywyyywwyyyyywwyyyywyr",
     "rryywwywwwwyywwwwwyywwyr",
     "ryywwwwwwwwwwwwwwwwwwwyr",
     "ryyywwwwwwwwwwwwwwwwyyyr"],
]
BRAZIER_SPARKS = [((6, 0), (24, 2), (15, 0)), ((9, 1), (21, 0), (3, 3)), ((13, 0), (26, 1), (17, 2))]


def brazier(lit, frame=0):
    """2x2: a deep bronze bowl on a lion-footed tripod. Symmetric, so its
    right half costs nothing; only the flames are drawn free. frame: which of
    the three flame frames (the tileset animates them)."""
    L = Layer(32, 32)
    # the tripod: two splayed legs and one to the front, a ring between them
    for (x0, y0), (x1, y1) in (((10, 20), (5, 28)),):
        L.line(x0, y0, x1, y1, "b1")
        L.line(x0 + 1, y0, x1 + 1, y1, "b2")
        L.line(x0 + 2, y0, x1 + 2, y1, "b0")
    for y in range(21, 30):
        L.px(15, y, "b2"), L.px(16, y, "b1")
    L.rect(3, 28, 4, 2, "b1"), L.px(3, 28, "b3"), L.px(4, 28, "b2"), L.px(6, 29, "b0")
    L.rect(14, 29, 2, 2, "b1"), L.px(14, 29, "b3")
    for x in range(8, 16):
        L.px(x, 24, "b2"), L.px(x, 25, "b0")
    # the bowl: deep, with a thick flared lip
    body = np.zeros((32, 32), bool)
    for y in range(12, 22):
        hw = 13 - max(0, y - 14) ** 1.35 * 0.55
        body[y, int(round(16 - hw)):16] = True
    cylinder(L, body | body[:, ::-1], ["b3", "b2", "b2", "b1", "b1", "b0"])
    for x in range(5, 16, 3):
        L.px(x, 16, "b0"), L.px(x + 1, 16, "b3")
    rim = ellipse_mask(32, 32, 16, 12, 14, 3.2)
    inner = ellipse_mask(32, 32, 16, 11.8, 11.5, 2.0)
    for y, x in zip(*np.nonzero(rim & ~inner)):
        L.px(x, y, "b3" if y >= 12 else "b1")
    for y, x in zip(*np.nonzero(inner)):
        L.px(x, y, ("fr1" if (x + y) % 3 else "fr2") if lit else ("ash" if (x * 3 + y) % 4 else "ash2"))
    m = rim | body | body[:, ::-1]
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if y >= 10:
            L.px(x, y, "k0")
    if not lit:
        for x, y in ((11, 11), (13, 12)):
            L.px(x, y, "b0")
    mirror_left(L)
    if lit:
        for x in range(6, 26, 4):
            L.px(x, 12, "fr3")
        leg = {"r": "fr2", "y": "fr3", "w": "fr4"}
        for j, row in enumerate(BRAZIER_FLAMES[frame]):
            for i, ch in enumerate(row):
                if ch in leg:
                    L.px(4 + i, j + 1, leg[ch])
        for x, y in BRAZIER_SPARKS[frame]:
            L.px(x, y, "fr3")
        for x in range(8, 24):
            if x % 4:
                L.px(x, 13, "fr1")
    return L.a


# --------------------------------------------------------------------------
# Webs
# --------------------------------------------------------------------------

WEB_H = 32


def web_anchors(W, H=WEB_H):
    """Where an orb web's spokes meet the walls, roof and floor of a passage W px wide."""
    pts = [(0, 0), (0, 9), (0, 19), (0, H - 3), (W - 1, 0), (W - 1, 9), (W - 1, 19), (W - 1, H - 3)]
    for f in (0.25, 0.5, 0.75):
        pts.append((round(W * f), 0))
    for f in (0.3, 0.7):
        pts.append((round(W * f), H - 1))
    return pts


def web(width, torn=False):
    """A cobweb curtain hung across a passage `width` cells wide and two cells
    deep: an orb web strung from wall to wall, roof to floor. torn: what
    Hecate's Torch leaves, ragged spokes at the walls and roof, scorched ends,
    ash on the floor."""
    W, H = width * 16, WEB_H
    L = Layer(W, H)
    hx, hy = (W - 1) / 2, 12.5
    spokes = sorted(web_anchors(W), key=lambda p: math.atan2(p[1] - hy, p[0] - hx))
    if not torn:
        for ax, ay in spokes:
            L.line(int(round(hx)), int(round(hy)), int(ax), int(ay), "k6")
        for i, f in enumerate((0.12, 0.24, 0.36, 0.5, 0.64, 0.78, 0.9)):
            ring = [(hx + (ax - hx) * f * (1 + 0.05 * ((j * 7 + i) % 3 - 1)),
                     hy + (ay - hy) * f) for j, (ax, ay) in enumerate(spokes)]
            for j in range(len(ring)):
                if (j * 3 + i) % 7 == 0 and i > 2:
                    continue                      # a broken thread here and there
                x0, y0 = ring[j]
                x1, y1 = ring[(j + 1) % len(ring)]
                L.line(int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)),
                       "wh" if i < 4 else "k7")
        L.px(int(round(hx)), int(round(hy)), "wh")
        # old wrapped prey, and the dust the lowest strands hold
        L.rect(int(hx) + 3, 18, 2, 3, "k7"), L.px(int(hx) + 3, 18, "wh"), L.px(int(hx) + 4, 21, "k5")
        for x in range(3, W - 3, 6):
            L.px(x, H - 4, "k5"), L.px(x + 1, H - 3, "k5")
    else:
        for ax, ay in spokes:
            if ay == H - 1 and 0 < ax < W - 1:
                continue
            n = 4 + (int(ax) + int(ay)) % 4
            dx = (hx - ax) / max(1.0, math.hypot(hx - ax, hy - ay))
            dy = (hy - ay) / max(1.0, math.hypot(hx - ax, hy - ay))
            for k in range(n):
                x, y = int(round(ax + dx * k)), int(round(ay + dy * k + k * 0.7))
                L.px(x, y, "k7" if k < n - 2 else ("k4" if k < n - 1 else "k2"))
        # shreds of the curtain still hanging from the roof
        for x in range(4, W - 3, 7):
            for y in range(0, 5 + x % 4):
                L.px(x, y, "k6" if y < 3 else "k4")
            L.px(x, 5 + x % 4, "k2")
        for x in range(4, W - 4, 5):
            L.px(x, H - 2, "k2"), L.px(x + 1, H - 1, "k3"), L.px(x + 2, H - 2, "k1")
    return L.a


def web_corner(side):
    """Old webbing in the corner where the floor meets a face, on a shadowed floor cell."""
    L = Layer(16, 16)
    hx, hy = (0, 0) if side == "w" else (15, 0)
    for k in range(5):
        a = math.pi / 2 * k / 4
        ex = hx + (13 * math.cos(a) if side == "w" else -13 * math.cos(a))
        ey = hy + 11 * math.sin(a)
        L.line(hx, hy, int(ex), int(ey), "k6")
    for r in (4, 7, 10):
        prev = None
        for k in range(9):
            a = math.pi / 2 * k / 8
            x = hx + (r * math.cos(a) if side == "w" else -r * math.cos(a))
            y = hy + r * 0.85 * math.sin(a)
            if prev:
                L.line(int(prev[0]), int(prev[1]), int(x), int(y), "wh" if r == 4 else "k7")
            prev = (x, y)
    return L.a


# --------------------------------------------------------------------------
# Hecate's supper: the offering niche, and her chalk
# --------------------------------------------------------------------------

def niche(kind="supper"):
    """1x2 in a face: a niche with a dog's bowl on its sill. Returns (bottom, middle)
    16x32 arrays. kind: 'supper' (laid), 'empty' (eaten), 'shells' (Glaukos's shrine)."""
    col = Layer(16, 32)
    col.a[:, :8] = kit.flute("A", 0)
    col.a[:, 8:] = kit.flute("C", 8)
    hole = np.zeros((32, 16), bool)
    for y in range(9, 26):
        if y < 14:
            r = 5.5 * math.sqrt(max(0.0, 1 - ((14 - y) / 5.0) ** 2))
        else:
            r = 5.5
        hole[y, int(round(8 - r)):int(round(8 + r))] = True
    for y, x in zip(*np.nonzero(hole)):
        col.px(x, y, "k1" if y < 22 else "k2")
        if y >= 12 and x == np.nonzero(hole[y])[0].max():
            col.px(x, y, "k0")
    pad = np.pad(hole, 1)
    for y in range(32):
        for x in range(16):
            if not hole[y, x] and any(pad[y + 1 + dy, x + 1 + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                col.px(x, y, "k0" if x >= 8 or y > 24 else "k7")
    # the sill
    for x in range(1, 15):
        col.px(x, 25, "k7" if x < 12 else "k6")
        col.px(x, 26, "k5")
        col.px(x, 27, "k3")
    col.px(0, 25, "k0"), col.px(15, 25, "k0")
    mid = Layer(16, 32)
    if kind in ("supper", "empty"):
        for x in range(4, 12):
            mid.px(x, 24, "b2" if x < 9 else "b1")
            mid.px(x, 23, "b3" if x == 5 else "b2")
        mid.px(3, 23, "b1"), mid.px(12, 23, "b1"), mid.px(4, 22, "b1"), mid.px(11, 22, "b1")
        for x in range(5, 11):
            mid.px(x, 22, "b0")
        if kind == "supper":
            # a loaf and two eggs
            for x, y, c in ((5, 20, "b2"), (6, 19, "b3"), (7, 19, "b3"), (8, 20, "b2"), (6, 20, "b3"),
                            (7, 20, "b2"), (5, 21, "b1"), (6, 21, "b2"), (7, 21, "b2"), (8, 21, "b1"),
                            (9, 20, "fr4"), (10, 20, "ash2"), (9, 21, "fr4"), (10, 21, "fr4"),
                            (10, 19, "fr4")):
                mid.px(x, y, c)
        else:
            mid.px(6, 21, "b1"), mid.px(9, 21, "b0")
    elif kind == "shells":
        for x, y, c in ((3, 23, "sf"), (4, 23, "an"), (5, 22, "sf"), (6, 23, "f4"), (7, 22, "an"),
                        (8, 23, "sf"), (9, 22, "f4"), (10, 23, "an"), (11, 22, "sf"), (12, 23, "f4"),
                        (5, 20, "f4"), (6, 19, "f3"), (7, 20, "sf"), (8, 19, "an"), (9, 20, "f4"),
                        (10, 20, "f3"), (6, 16, "f2"), (7, 15, "f2"), (8, 16, "f2"), (9, 15, "f3")):
            mid.px(x, y, c)
    return col.a, mid.a


CHALK_WHEEL = [
    "................",
    "......2222......",
    "....22....22....",
    "...2..1221..2...",
    "..2..2....2..2..",
    "..2.2..22..2.2..",
    "..2.2.2..2.2.2..",
    "..2.2..2.2.2.2..",
    "..2..2...2..2...",
    "...2..222..2....",
    "....22....22....",
    "......2222......",
    ".......2........",
    "......222.......",
    ".....2.2.2......",
    ".......2........",
]
CHALK_ARROWS = {
    "n": ["................", "................", ".......2........", "......222.......",
          ".....2.2.2......", "....2..2..2.....", ".......2........", ".......2........",
          ".......1........", ".......2........", ".......2........", "................",
          "................", "................", "................", "................"],
}
CHALK_TRIANGLE = [
    "................",
    "................",
    ".......22.......",
    "......2..2......",
    "......2..2......",
    ".....2....2.....",
    ".....2.22.2.....",
    "....2..22..2....",
    "....2......2....",
    "...2........2...",
    "...2222222222...",
    "................",
    "..2....2....2...",
    "................",
    "................",
    "................",
]


def chalk(rows, leg=None):
    return grid_art(rows, leg or {"2": "ch2", "1": "ch1"})


def arrow(direction):
    a = chalk(CHALK_ARROWS["n"])
    if direction == "s":
        a = a[::-1]
    elif direction == "e":
        a = np.transpose(a, (1, 0, 2))[:, ::-1]
    elif direction == "w":
        a = np.transpose(a, (1, 0, 2))
    return np.ascontiguousarray(a)


# --------------------------------------------------------------------------
# The Hekataion: Hecate's three-faced pillar, 3x4
# --------------------------------------------------------------------------

MARBLE = ["m4", "m4", "m3", "m3", "m2", "m2", "m1"]


def figure(facing, h=44):
    """One of the three women of the Hekataion: a polos crown, a veil over the
    head and shoulders, a peplos belted with an overfold, falling in folds to
    the feet. facing 'front' or 'left' (the right one is the left mirrored).
    Returns RGBA (h, 20); a front figure is symmetric about x = 10."""
    w, cx = 20, 10.0
    L = Layer(w, h)
    hw = {}
    for y in range(h):
        if y < 4:
            v = 2.5                                  # polos
        elif y < 5:
            v = 2.8
        elif y < 11:
            v = 3.1                                  # veiled head
        elif y < 12:
            v = 2.6
        elif y < 13:
            v = 1.8                                  # neck under the veil
        elif y < 14:
            v = 5.0                                  # shoulders
        elif y < 21:
            v = 5.8 - (y - 14) * 0.12                 # arms at the sides, breast
        elif y < 22:
            v = 4.6                                   # the belt
        elif y < 25:
            v = 5.4                                   # the overfold
        else:
            v = 5.0 + (y - 25) / max(1, h - 27) * 2.2  # the skirt falls to the hem
        hw[y] = v
    body = np.zeros((h, w), bool)
    for y, v in hw.items():
        body[y, int(round(cx - v)):int(round(cx + v))] = True
    cylinder(L, body, MARBLE, outline="k0")
    # the veil frames the face and falls to the shoulders
    for y in range(4, 15):
        v = hw[y]
        a, b = int(round(cx - v)), int(round(cx + v)) - 1
        L.px(a + 1, y, "m1"), L.px(b - 1, y, "m1")
        if y >= 5:
            L.px(a + 2, y, "m2"), L.px(b - 2, y, "m2")
    for x in range(int(cx - 3), int(cx + 3)):
        L.px(x, 4, "m2")
    # shoulders catch the light from above; the arms hang at the sides
    for x in range(int(cx - 5), int(cx + 5)):
        if body[13, x] and L.get(x, 13) != "k0":
            L.px(x, 13, "m5" if abs(x + 0.5 - cx) < 3.5 else "m4")
    for y in range(15, 22):
        for x in (int(round(cx - 3.5)), int(round(cx + 3.5)) - 1):
            L.px(x, y, "m1")
    # polos crown: lit rim, dark band
    for x in range(int(cx - 2.5), int(cx + 2.5)):
        L.px(x, 0, "m5"), L.px(x, 1, "m4"), L.px(x, 3, "m1")
    # belt and overfold
    for x in range(int(cx - 4), int(cx + 4)):
        L.px(x, 21, "m1"), L.px(x, 22, "m4"), L.px(x, 24, "m2")
    # folds of the skirt, gathering toward the belt
    for f in (-1, 1):
        for y in range(26, h - 1):
            t = (y - 26) / max(1, h - 27)
            for off, c in ((1.5 + t * 1.2, "m2"), (3.6 + t * 2.4, "m2")):
                x = int(round(cx + f * off - (1 if f < 0 else 0)))
                if body[y, x]:
                    L.px(x, y, c)
                    xi = x + (1 if f < 0 else -1)
                    if body[y, xi] and L.get(xi, y) not in ("m0",):
                        L.px(xi, y, "m4")
    for x in range(int(cx - 7), int(cx + 7)):
        if body[h - 1, x]:
            L.px(x, h - 1, "m1")
    if facing == "front":
        # a calm frontal face in the veil's shadow
        for y in range(5, 12):
            for x in range(8, 12):
                L.px(x, y, "m4" if y < 9 else "m3")
        L.px(8, 7, "k0"), L.px(11, 7, "k0")
        L.px(9, 8, "m5"), L.px(10, 8, "m3")
        L.px(9, 10, "m1"), L.px(10, 10, "m1")
        L.px(8, 11, "m2"), L.px(11, 11, "m2")
    else:
        # in profile, looking west: brow, nose, lips, chin; the veil behind
        for y in range(5, 12):
            L.px(6, y, "m4"), L.px(7, y, "m3")
        L.px(5, 8, "m4"), L.px(5, 9, "m3"), L.px(6, 11, "m2")
        L.px(7, 7, "k0"), L.px(6, 10, "m1")
        for y in range(5, 14):
            L.px(11, y, "m1"), L.px(12, y, "m1"), L.px(10, y, "m2")
    return L.a


TORCH_CUP = [          # rows 6-10 of a torch: the cup's rim round its sooty mouth, on a shaft
    ".cccc.",
    "c0000c",
    "xBBBbx",
    ".xBbx.",
    "..Bb..",
]
TORCH_C = {"x": "k0", "0": "m0", "c": "ck", "B": "b2", "b": "b1"}


TORCH_FLAMES = [
    ["..r...", "..rr..", ".ryr..", ".ryyr.", "ryywr.", "rywwyr", "rywwyr"],
    ["...r..", "..rr..", "..ryr.", ".ryyr.", ".rywyr", "rywwyr", "rywwyr"],
    ["......", ".r.r..", ".ryr..", "ryyr..", "ryywr.", "rywwyr", "rywwyr"],
]


def torch(state, shaft=10, frame=0):
    """A bronze torch, cup up: 6 wide, (shaft + 11) tall. state 'cold' or 'lit'."""
    h = shaft + 11
    L = Layer(6, h)
    for y in range(11, h):
        L.px(2, y, "b2"), L.px(3, y, "b1")
    L.blit(TORCH_CUP, TORCH_C, 0, 6)
    if state == "lit":
        fl = TORCH_FLAMES[frame]
        leg = {"r": "fr2", "y": "fr3", "w": "fr4"}
        for j, row in enumerate(fl):
            for i, ch in enumerate(row):
                if ch in leg:
                    L.px(i, j, leg[ch])
    return L.a


SIDE_TORCH = (1, 1)      # where the west torch sits (its cup over x 1-6)
FRONT_TORCH = (17, -1)   # the front figure's left-hand torch (cup over x 17-22)


def hekataion(west="cold", front="cold", east="cold", cake=True, frame=0):
    """48x64 RGBA of the Hekataion. Drawn as a left half and mirrored, so it
    costs half its tiles; the torches go on after, each in its own top cell.
    front: 'cold', 'lit', or 'taken' (her right-hand torch gone, the other lit)."""
    L = Layer(48, 64)
    # the plinth: a round three-stepped base with an offering ledge
    top = ellipse_mask(48, 64, 24, 50, 23, 5.5)
    front_m = np.zeros((64, 48), bool)
    for y in range(50, 62):
        v = 23 - max(0, y - 58) * 1.6
        front_m[y, int(round(24 - v)):int(round(24 + v))] = True
    cylinder(L, front_m & ~top, ["m3", "m2", "m2", "m1", "m1", "m0"])
    cylinder(L, top, ["m5", "m4", "m4", "m3", "m3", "m2"])
    for x in range(1, 47):
        if L.get(x, 57):
            L.px(x, 57, "m1")
        if L.get(x, 56):
            L.px(x, 56, "m3")
    # the water that runs down the faces gathers in a channel round the base
    for x in range(8, 40):
        if top[52, x]:
            L.px(x, 52, "w3" if x % 4 else "m4")
    # the pillar the three stand against
    pillar = np.zeros((64, 48), bool)
    pillar[8:50, 17:31] = True
    cylinder(L, pillar, ["m2", "m1", "m1", "m0", "m0"], outline="k0")
    # the west face (mirrored to the east), then the front one over both
    L.paste(figure("left", 42), 0, 8)
    L.a[:, 24:] = L.a[:, :24][:, ::-1]
    L.paste(figure("front", 44), 14, 6)
    # arms raised to the torches: the west figure's outer arm, the front
    # figure's two; each arm a lit stroke with a shadowed edge and a hand
    for (sx, sy), (hx, hy) in (((6, 22), (3, 16)), ((19, 20), (20, 14))):
        for (ax, ay), (bx, by), o in (((sx, sy), (hx, hy), -1), ((47 - sx, sy), (47 - hx, hy), 1)):
            L.line(ax + o, ay, bx + o, by, "k0")
            L.line(ax, ay, bx, by, "m4")
            L.line(ax - o, ay, bx - o, by, "m2")
            L.px(bx, by, "m5")
    # the spring: water runs down the pillar between the women, into the channel
    for x in (17, 30):
        for y in range(28, 50):
            if L.get(x, y) in ("m0", "m1", "m2"):
                L.px(x, y, "w3" if y % 2 else "m1")
    # the offering ledge, and the barley cake on it
    for x in range(18, 30):
        L.px(x, 54, "m5"), L.px(x, 55, "m3")
    if cake:
        for x, y, c in ((21, 52, "ck2"), (22, 51, "ck"), (23, 51, "ck"), (24, 51, "ck"), (25, 51, "ck"),
                        (26, 52, "ck2"), (21, 53, "ck2"), (22, 52, "ck"), (23, 52, "m5"), (24, 52, "m5"),
                        (25, 52, "ck"), (22, 53, "ck2"), (23, 53, "ck2"), (24, 53, "ck2"), (25, 53, "ck2"),
                        (26, 53, "ck2"), (23, 50, "ck2"), (24, 50, "ck2")):
            L.px(x, y, c)
    # the torches: west, the front pair, east
    sx, sy = SIDE_TORCH
    fx, fy = FRONT_TORCH
    L.paste(torch(west, 16, frame), sx, sy)
    L.paste(torch(east, 16, (frame + 1) % 3)[:, ::-1], 47 - sx - 5, sy)
    if front == "taken":
        L.paste(torch("lit", 6, (frame + 2) % 3), fx, fy)
        L.px(47 - fx - 2, 15, "m4"), L.px(47 - fx - 3, 15, "m3")
    else:
        L.paste(torch(front, 6, (frame + 2) % 3), fx, fy)
        L.paste(torch(front, 6, frame)[:, ::-1], 47 - fx - 5, fy)
    return L.a


# --------------------------------------------------------------------------
# Building the structures
# --------------------------------------------------------------------------

def bones():
    """Old bones on the floor: a dog's, by the look of the skull."""
    L = Layer(16, 16)
    art = [
        "................",
        "................",
        "...x...........",
        "..x5x4433x......",
        "...x...x.x......",
        "..........x.....",
        "....xx.........",
        "...x544x....x...",
        "...x4432x..x5x..",
        "....x22xx...x4x.",
        ".....xx.......x3x",
        "...........x...x.",
        "..x............",
        ".x5433333x......",
        "..x.......x.....",
        "................",
    ]
    L.blit(art, {"x": "m0", "5": "m5", "4": "m4", "3": "m3", "2": "m2"}, 0, 0)
    L.px(4, 8, "k0"), L.px(6, 8, "k0")
    return L.a


def stele():
    """A small stone at a cave mouth, its name cut into it."""
    L = Layer(16, 16)
    m = np.zeros((16, 16), bool)
    m[3:14, 4:12] = True
    m[2, 5:11] = True
    m[1, 6:10] = True
    shadow(L, m, 0, 0)
    shade(L, m, ramp=["k7", "k7", "k6", "k6", "k5", "k4", "k3"])
    for y in (5, 7, 9, 11):
        for x in range(6, 10 if y != 11 else 8):
            if (x + y) % 3:
                L.px(x, y, "k3")
    return L.a


def dish_covered():
    """The old woman's covered dish: Hecate's supper on its way to the crossroads."""
    L = Layer(16, 16)
    body = ellipse_mask(16, 16, 8, 11, 6.5, 3)
    shade(L, body, ramp=["b3", "b2", "b2", "b1", "b0"])
    cloth = ellipse_mask(16, 16, 8, 8.5, 5.5, 3.5)
    shade(L, cloth, ramp=["fr4", "fr4", "ash2", "ash2", "ash"], outline="k0")
    L.px(8, 5, "k0"), L.px(7, 6, "ash"), L.px(9, 6, "ash")
    return L.a


def stone_structs():
    out = []
    out.append(on_floor("bones", "Old bones", 1, 1, ["."], bones(),
                        notes="A dog's bones and skull, walkable. Near Hecate's niche."))
    out.append(on_floor("stele", "Name stone", 1, 1, ["X"], stele(),
                        notes="A small stele with the place's name cut in it: the sign at a mouth."))
    out.append(on_floor("dish_covered", "A covered dish", 1, 1, ["X"], dish_covered(),
                        notes="The old woman's dish (beat 18), at her feet by the east mouth."))
    for d, code in (("n", "^"), ("s", "v"), ("w", "["), ("e", "]")):
        out.append(on_floor(f"lit_warp_{d}", f"Daylit floor, exit {d}", 1, 1, [code], np.zeros((16, 16, 4), np.uint8),
                            ground=LIT, floor_mb=None,
                            notes="Lit floor at a map edge, an arrow warp to the outside."))
    out.append(on_floor("stalagmite", "Stalagmite", 1, 1, ["X"], stalagmite(),
                        notes="A single stalagmite. Impassable."))
    out.append(on_floor("stalagmites", "Two stalagmites", 1, 1, ["X"], stalagmite_pair(),
                        notes="A pair, one tall, one short. Impassable."))
    out.append(on_floor("stalagmite_tall", "Tall stalagmite", 1, 2, ["T", "X"], stalagmite_tall(),
                        notes="Its tip is drawn over the player, who can walk behind it."))
    out.append(on_floor("column", "Column", 1, 2, ["T", "X"], column(),
                        notes="A stalactite and stalagmite grown together. Walk behind its top."))
    out.append(on_floor("boulder", "Boulder", 1, 1, ["X"], boulder(), notes="Impassable."))
    out.append(on_floor("rock_pile", "Rubble heap", 1, 1, ["X"], rock_pile(),
                        notes="Broken limestone fallen from the roof. Impassable."))
    out.append(on_floor("pebbles", "Pebbles", 1, 1, ["."], pebbles(), notes="Scatter on open floor; walkable."))
    out.append(on_floor("slab", "Fallen slab", 2, 1, ["XX"], slab(), notes="A slab fallen from the roof."))
    for part in ("w", "a", "b", "e"):
        out.append(on_floor(f"ledge_{part}", f"Ledge ({part})", 1, 1, ["J"], ledge(part),
                            notes="A low rock step: jump south. West end, two middles, east end.",
                            floor_mb=None))
    out.append(on_floor("ledge_east", "Ledge, jump east", 1, 1, [">"], ledge_side(True), floor_mb=None))
    out.append(on_floor("ledge_west", "Ledge, jump west", 1, 1, ["<"], ledge_side(False), floor_mb=None))
    return out


def mouth_structs():
    out = []
    b, m = mouth()
    s = Struct("mouth", "Cave mouth to daylight", 2, 2, "cave", walk=["XX", "^^"],
               notes="Set into a north face over its ft/fb cells. The bottom row is the exit: "
                     "MB_NORTH_ARROW_WARP. Lead up to it with lit floor.")
    s.B.a[:] = b
    s.M.a[:] = m
    out.append(s)
    s = on_floor("hole_down", "Hole with steps down", 1, 1, ["."], hole_down(), floor_mb=None,
                 notes="A pit with rough steps into the dark: MB_NON_ANIMATED_DOOR, warp on it.")
    s.behaviors[(0, 0)] = "MB_NON_ANIMATED_DOOR"
    out.append(s)
    day = daylight()
    for key, w, h, walk, art in (
            ("daylight_e", 2, 1, [".]"], day),
            ("daylight_w", 2, 1, ["[."], day[:, ::-1]),
            ("daylight_s", 1, 2, [".", "v"], np.ascontiguousarray(np.transpose(day, (1, 0, 2)))),
            ("daylight_n", 1, 2, ["^", "."], np.ascontiguousarray(np.transpose(day, (1, 0, 2))[::-1]))):
        s = Struct(key, f"Daylight at a mouth, {key[-1]}", w, h, "cave", walk=walk,
                   floor_mb="MB_NORMAL",
                   notes="Daylight pouring in where a passage leaves the map; the edge cell is the "
                         "arrow warp out. Lead into it with lit floor.")
        s.B.a[:] = art
        out.append(s)
    return out


def fire_structs():
    out = []
    for state in ("cold", "lit"):
        out.append(on_floor(f"brazier_{state}", f"Bronze brazier, {state}", 2, 2, ["XX", "XX"],
                            brazier(state == "lit"),
                            notes="2x2, all impassable. Swap all four tiles: lit = cold + its offset "
                                  "(see the labels)."))
    return out


def web_structs():
    out = []
    for torn in (False, True):
        tag = "torn" if torn else "web"
        walk = "." if torn else "X"
        note = ("Hung across a passage two cells deep. Intact it blocks; Hecate's Torch burns it "
                "(swap in the burnt piece, which is walkable)." if not torn else
                "What the torch leaves: shreds at the walls and roof, ash on the floor. Walkable.")
        out.append(on_floor(f"{tag}_1", f"Cobweb across a 1-wide passage{' (burnt)' if torn else ''}", 1, 2,
                            [walk, walk], web(1, torn), notes=note))
        out.append(on_floor(f"{tag}_2", f"Cobweb across a 2-wide passage{' (burnt)' if torn else ''}", 2, 2,
                            [walk * 2, walk * 2], web(2, torn), notes=note))
    out.append(on_floor("web_corner_w", "Old webbing, west corner", 1, 1, ["."], web_corner("w"),
                        ground=FLOOR_N, notes="On the floor row under a face, against a west wall."))
    out.append(on_floor("web_corner_e", "Old webbing, east corner", 1, 1, ["."], web_corner("e"),
                        ground=FLOOR_N))
    return out


def hecate_structs():
    out = []
    # the niche: 1x2 in a face; three states share the top cell
    for kind in ("supper", "empty"):
        b, m = niche(kind)
        s = Struct(f"niche_{kind}", f"Hecate's niche, {'her supper laid' if kind == 'supper' else 'the bowl empty'}",
                   1, 2, "cave", walk=["X", "X"],
                   notes="1x2, set into a face over its ft and fb cells. A dog's bowl on the sill.")
        s.B.a[:] = b
        s.M.a[:] = m
        out.append(s)
    # chalk on the walls (over a face) and on the floor
    face = np.concatenate([kit.face_cell("ft", "A", "B"), kit.face_cell("fb", "A", "B")], 0)
    wheel = np.zeros((32, 16, 4), np.uint8)
    wheel[8:24] = chalk(CHALK_WHEEL)
    seep = Struct("seep", "A seep: the spring weeping from the rock", 1, 2, "cave", walk=["X", "X"],
                  notes="1x2 in a face, over a pool: the underground spring's source. Its tiles are "
                        "the wet grottos' seep, so it costs nothing.")
    seep.B.a[:] = np.concatenate([kit.face_cell("ft", "wet", "wet"), kit.face_cell("fb", "wet", "wet")], 0)
    out.append(seep)
    s = Struct("chalk_wheel", "Hecate's wheel in chalk, on a face", 1, 2, "cave", walk=["X", "X"],
               notes="The strophalos, drawn in Hecate's chalk: faint in light, glowing when doused.")
    s.B.a[:] = face
    s.M.a[:] = wheel
    out.append(s)
    for d in ("n", "e", "s", "w"):
        out.append(on_floor(f"chalk_arrow_{d}", f"Chalk arrow, {d}", 1, 1, ["."], arrow(d),
                            notes="Glow-paint on the floor."))
    out.append(on_floor("chalk_triangle", "The Three Roads, in chalk", 1, 1, ["."], chalk(CHALK_TRIANGLE),
                        notes="Hecate's sign for a crossroads: three roads, three points."))
    # the same marks and scatter on lit floor (the art is shared; only the ground differs)
    for key, art in (("chalk_triangle", chalk(CHALK_TRIANGLE)), ("chalk_arrow_n", arrow("n")),
                     ("chalk_arrow_s", arrow("s")), ("bones", bones()), ("pebbles", pebbles())):
        out.append(on_floor(f"{key}_lit", f"{key.replace('_', ' ')}, on lit floor", 1, 1, ["."], art,
                            ground=LIT, floor_mb="MB_NORMAL"))
    # the Hekataion, 3x4, on lit floor; row 0 is drawn over the player
    walk = ["TTT", "XXX", "XXX", "XXX"]
    s = on_floor("hekataion", "The Hekataion: three faces, three torches", 3, 4, walk, hekataion(),
                 ground=LIT, floor_mb="MB_NORMAL",
                 notes="Three women back to back, one looking down each road, each holding a cold "
                       "bronze torch. Stand it in lit floor. Row 0 (heads and torches) is drawn over "
                       "the player; the 3x3 below blocks.")
    out.append(s)
    # swaps: each torch lit, the middle torch taken, the cake eaten
    lit = hekataion("lit", "lit", "lit")
    taken = hekataion("lit", "taken", "lit")
    nocake = hekataion(cake=False)
    for i, name in enumerate(("w", "s", "e")):
        out.append(on_floor(f"hekataion_torch_{name}_lit", f"Hekataion, the {name} torch lit", 1, 1, ["T"],
                            lit[0:16, i * 16:i * 16 + 16], ground=LIT, floor_mb="MB_NORMAL"))
    out.append(on_floor("hekataion_torch_s_gone", "Hekataion, the middle torch taken", 1, 1, ["T"],
                        taken[0:16, 16:32], ground=LIT, floor_mb="MB_NORMAL"))
    out.append(on_floor("hekataion_no_cake", "Hekataion, the ledge bare", 1, 1, ["X"],
                        nocake[48:64, 16:32], ground=LIT))
    return out


def build():
    return stone_structs() + mouth_structs() + fire_structs() + web_structs() + hecate_structs()
